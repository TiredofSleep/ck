"""
operator_memory_bank.py -- non-parametric memory-transfer device for the
operator dimension.

Brayden 2026-05-02: "maybe the ai is the memory transfer device? in and
out?"

Where the operator-LM is a parametric predictor (distribution over next
operator from learned weights), this bank is non-parametric: it stores
(context_encoding, observed_next_operator) pairs from training data and
retrieves by cosine similarity.

Three components:

  1. ENCODER: pass a context (recent operator history) through the LM up
     to the final transformer layer; take the last position's hidden
     state as the key.  Same representation space as the LM uses for
     prediction, but used as a similarity key rather than a softmax input.

  2. BANK: list of (key_vector, next_token) pairs accumulated from
     training-pair scan.  Built once from training_streams.jsonl.

  3. RETRIEVER: given a new context, encode -> top-k nearest keys by
     cosine similarity -> vote on next token, weighted by similarity.

Three predictions are then compared:

  P_LM(next | ctx)   = softmax(LM logits) -- the parametric prediction.
  P_bank(next | ctx) = weighted vote over k-nn retrieved (key, value).
  P_ensemble         = alpha * P_LM + (1 - alpha) * P_bank.

This is k-NN augmented language modeling (Khandelwal et al. 2020
'Generalization through Memorization', ICLR 2020) applied to CK's
operator stream.  The interesting part: under the "memory transfer
device" frame, the bank IS the substrate and the LM is just a function
that compresses-and-decompresses the bank's content.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import List, Optional, Tuple

import torch
import torch.nn.functional as F

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))

from ck_grammar_lm import (
    GrammarLM, GrammarLMConfig, load_model,
    OP_NAMES, NAME_TO_ID, SPECIAL_IDS, SPECIAL_NAMES,
    VOCAB_SIZE, token_name,
)


# ── Encoder: hidden state of the LM at the last position ─────────────

@torch.no_grad()
def encode_context(model: GrammarLM, context_ids: List[int]) -> torch.Tensor:
    """Run the LM up through ln_f and return the hidden state of the
    last position.  Shape: (d_model,)."""
    if not context_ids:
        context_ids = [SPECIAL_IDS["BOS"]]
    device = next(model.parameters()).device
    idx = torch.tensor(context_ids[-model.cfg.block_size:],
                        dtype=torch.long, device=device).unsqueeze(0)
    B, T = idx.shape
    pos = torch.arange(T, device=device).unsqueeze(0)
    x = model.tok_emb(idx) + model.pos_emb(pos)
    for block in model.blocks:
        x = block(x)
    x = model.ln_f(x)
    return x[0, -1, :].detach()  # (d_model,)


# ── Bank construction from training data ─────────────────────────────

class OperatorMemoryBank:
    def __init__(self, model: GrammarLM):
        self.model = model
        self.keys: Optional[torch.Tensor] = None     # (N, d_model)
        self.values: Optional[torch.Tensor] = None   # (N,) long
        self.normed: Optional[torch.Tensor] = None   # cached unit-normed keys

    def build_from_streams(self, streams_path: Path,
                             max_examples: Optional[int] = None) -> None:
        """Walk the streams file: for each (prefix, target) pair within
        each sequence, encode prefix and store (encoding, target).

        We use SHORT prefixes (last 5 tokens) as keys -- matches how
        retrieval will be used at inference and keeps bank size reasonable.
        """
        WIN = 5  # context window length for retrieval keys
        keys: List[torch.Tensor] = []
        vals: List[int] = []
        n_seqs = 0; n_pairs = 0
        with open(streams_path, encoding="utf-8") as f:
            for line in f:
                d = json.loads(line)
                ops = d["ops"]
                if not ops:
                    continue
                seq = [SPECIAL_IDS["BOS"]] + ops + [SPECIAL_IDS["EOS"]]
                for i in range(1, len(seq)):
                    prefix = seq[max(0, i - WIN):i]
                    target = seq[i]
                    # Skip BOS as target (it's only a position marker)
                    key = encode_context(self.model, prefix).cpu()
                    keys.append(key); vals.append(target)
                    n_pairs += 1
                    if max_examples is not None and n_pairs >= max_examples:
                        break
                n_seqs += 1
                if max_examples is not None and n_pairs >= max_examples:
                    break
        if not keys:
            raise RuntimeError("no examples extracted from streams")
        self.keys = torch.stack(keys, dim=0)         # (N, d_model)
        self.values = torch.tensor(vals, dtype=torch.long)
        self.normed = F.normalize(self.keys, dim=-1)
        print(f"  Bank built from {n_seqs} sequences, {n_pairs} (key, value) pairs")

    @torch.no_grad()
    def retrieve(self, context_ids: List[int], k: int = 16
                  ) -> Tuple[torch.Tensor, List[int], torch.Tensor]:
        """k-NN retrieval. Returns:
            sims:    (k,) cosine similarities
            ids:     [k]   indices into the bank
            values:  (k,)  next-token labels at those indices
        """
        if self.keys is None:
            raise RuntimeError("Bank not built")
        q = encode_context(self.model, context_ids).cpu()
        q_norm = F.normalize(q, dim=-1)
        sims = self.normed @ q_norm                 # (N,)
        topk_sims, topk_ids = torch.topk(sims, min(k, sims.size(0)))
        topk_vals = self.values[topk_ids]
        return topk_sims, topk_ids.tolist(), topk_vals

    @torch.no_grad()
    def predict_next(self, context_ids: List[int], k: int = 16,
                      temperature: float = 1.0) -> torch.Tensor:
        """Distribution over next token from k-NN softmax-weighted vote."""
        sims, _, vals = self.retrieve(context_ids, k=k)
        # Softmax over similarities (with temperature)
        weights = F.softmax(sims / max(1e-6, temperature), dim=0)
        probs = torch.zeros(VOCAB_SIZE)
        for w, v in zip(weights, vals):
            probs[v.item()] += w.item()
        # Renormalize (should already sum to ~1)
        return probs / probs.sum().clamp(min=1e-9)


# ── Comparison: LM vs Bank vs Ensemble ───────────────────────────────

@torch.no_grad()
def lm_predict_dist(model: GrammarLM, context_ids: List[int]
                     ) -> torch.Tensor:
    """LM's distribution over next token."""
    if not context_ids:
        context_ids = [SPECIAL_IDS["BOS"]]
    device = next(model.parameters()).device
    idx = torch.tensor(context_ids[-model.cfg.block_size:],
                        dtype=torch.long, device=device).unsqueeze(0)
    logits, _ = model.forward(idx)
    return F.softmax(logits[0, -1, :], dim=-1).cpu()


def evaluate_methods(model: GrammarLM, bank: OperatorMemoryBank,
                      test_pairs: List[Tuple[List[int], int]],
                      k: int = 16, alpha: float = 0.5):
    """test_pairs = [(context_ids, expected_next_id), ...]"""
    n = len(test_pairs)
    if n == 0: return {}
    lm_correct = 0; bank_correct = 0; ens_correct = 0
    lm_ll = 0.0; bank_ll = 0.0; ens_ll = 0.0
    for ctx, target in test_pairs:
        p_lm = lm_predict_dist(model, ctx)
        p_bank = bank.predict_next(ctx, k=k)
        p_ens = alpha * p_lm + (1 - alpha) * p_bank
        if int(p_lm.argmax()) == target: lm_correct += 1
        if int(p_bank.argmax()) == target: bank_correct += 1
        if int(p_ens.argmax()) == target: ens_correct += 1
        eps = 1e-9
        lm_ll += float(torch.log(p_lm[target] + eps))
        bank_ll += float(torch.log(p_bank[target] + eps))
        ens_ll += float(torch.log(p_ens[target] + eps))
    return {
        "n": n,
        "lm":   {"top1_acc": lm_correct/n,   "mean_ll": lm_ll/n},
        "bank": {"top1_acc": bank_correct/n, "mean_ll": bank_ll/n},
        "ens":  {"top1_acc": ens_correct/n,  "mean_ll": ens_ll/n},
        "alpha": alpha, "k": k,
    }


def main():
    print("=" * 80)
    print("operator memory bank -- 'memory transfer device' frame")
    print("=" * 80)
    print()

    print("Loading mixed-corpus LM (v1)...")
    model = load_model(HERE / "ck_grammar_lm.pt")
    print(f"  params: {model.n_params():,}")
    device = next(model.parameters()).device
    print(f"  device: {device}")

    print("\nBuilding bank from training streams...")
    bank = OperatorMemoryBank(model)
    bank.build_from_streams(HERE / "training_streams.jsonl",
                              max_examples=20000)

    # Test pairs: prefix -> expected next
    OP = NAME_TO_ID
    test_sets = {
        "canon (012, 567, 789, 1397, 2486 next-step)": [
            ([SPECIAL_IDS["BOS"], OP["VOID"], OP["LATTICE"]], OP["COUNTER"]),
            ([SPECIAL_IDS["BOS"], OP["BALANCE"], OP["CHAOS"]], OP["HARMONY"]),
            ([SPECIAL_IDS["BOS"], OP["HARMONY"], OP["BREATH"]], OP["RESET"]),
            ([SPECIAL_IDS["BOS"], OP["LATTICE"], OP["PROGRESS"]], OP["RESET"]),
            ([SPECIAL_IDS["BOS"], OP["COUNTER"], OP["COLLAPSE"]], OP["BREATH"]),
        ],
        "real high-freq pairs": [
            ([SPECIAL_IDS["BOS"], OP["HARMONY"]], OP["HARMONY"]),
            ([SPECIAL_IDS["BOS"], OP["HARMONY"]], OP["COUNTER"]),
            ([SPECIAL_IDS["BOS"], OP["LATTICE"]], OP["BALANCE"]),
            ([SPECIAL_IDS["BOS"], OP["HARMONY"]], OP["PROGRESS"]),
        ],
        "anti-canon (reverse triples)": [
            ([SPECIAL_IDS["BOS"], OP["RESET"], OP["BREATH"]], OP["LATTICE"]),
            ([SPECIAL_IDS["BOS"], OP["BREATH"], OP["LATTICE"]], OP["COUNTER"]),
            ([SPECIAL_IDS["BOS"], OP["LATTICE"], OP["LATTICE"]], OP["LATTICE"]),
        ],
    }

    print("\n" + "=" * 80)
    print(f"{'test set':<48} {'LM':>16} {'BANK':>16} {'ENSEMBLE':>16}")
    print("-" * 100)
    for name, pairs in test_sets.items():
        for alpha in [0.5]:
            res = evaluate_methods(model, bank, pairs, k=16, alpha=alpha)
            lm = res["lm"]; bk = res["bank"]; en = res["ens"]
            print(f"  {name:<46} "
                  f"acc={lm['top1_acc']:.2f}/ll={lm['mean_ll']:>+5.2f}  "
                  f"acc={bk['top1_acc']:.2f}/ll={bk['mean_ll']:>+5.2f}  "
                  f"acc={en['top1_acc']:.2f}/ll={en['mean_ll']:>+5.2f}")
    print()

    # Sweep alpha for combined ensemble on canon test
    print("=== Alpha sweep on canon (alpha = LM weight, 1-alpha = bank weight) ===")
    canon_pairs = test_sets["canon (012, 567, 789, 1397, 2486 next-step)"]
    print(f"  {'alpha':>6} {'top1_acc':>10} {'mean_ll':>10}")
    for alpha in [0.0, 0.2, 0.4, 0.5, 0.6, 0.8, 1.0]:
        res = evaluate_methods(model, bank, canon_pairs, k=16, alpha=alpha)
        en = res["ens"]
        print(f"  {alpha:>6.1f} {en['top1_acc']:>10.2f} {en['mean_ll']:>+10.3f}")

    # Show retrieved nearest neighbors for a key prefix
    print("\n=== Retrieval inspection ===")
    for name, prefix in [
        ("VOID-LATTICE",  [SPECIAL_IDS["BOS"], OP["VOID"], OP["LATTICE"]]),
        ("BALANCE-CHAOS", [SPECIAL_IDS["BOS"], OP["BALANCE"], OP["CHAOS"]]),
        ("HARMONY-HARMONY", [SPECIAL_IDS["BOS"], OP["HARMONY"], OP["HARMONY"]]),
    ]:
        sims, idxs, vals = bank.retrieve(prefix, k=10)
        from collections import Counter
        vote = Counter(int(v.item()) for v in vals)
        print(f"\n  Query: {name}")
        print(f"    Top-10 retrieved next-token votes: " +
              ", ".join(f"{token_name(t)}({c})" for t, c in vote.most_common()))
        print(f"    Top-3 sim, retrieved-next:")
        for s, i, v in zip(sims[:3], idxs[:3], vals[:3]):
            print(f"      sim={float(s):.3f}  next={token_name(int(v.item()))}")


if __name__ == "__main__":
    main()
