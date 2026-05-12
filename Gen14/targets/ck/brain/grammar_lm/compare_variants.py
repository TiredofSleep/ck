"""
compare_variants.py -- train and compare three operator-LM variants:

  v1 (mixed)     -- the current model: real + synthetic walks (154k tokens)
  v2 (real-only) -- only the 621 real-data tokens; will overfit
  v3 (curriculum) -- pretrain on synth (153k tokens), finetune on real (621)

Test set: held-out canonical paths + held-out real pairs + anti-canon.
Compute average log-likelihood per token and rank-1 prediction accuracy.

The point: does training on REAL only (or curriculum) better capture
CK's actual behavior than the mixed corpus that dilutes real with
algebra walks?
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import torch

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from ck_grammar_lm import (
    GrammarLM, GrammarLMConfig, save_model, load_model,
    OP_NAMES, NAME_TO_ID, SPECIAL_IDS, VOCAB_SIZE, token_name,
)
from train import OperatorDataset


def make_streams_subset(src_filter, out_path: Path):
    """Filter training_streams.jsonl by 'src' field; write to a new file."""
    in_path = HERE / "training_streams.jsonl"
    n = 0
    with open(in_path, encoding="utf-8") as fin, open(out_path, "w", encoding="utf-8") as fout:
        for line in fin:
            d = json.loads(line)
            if src_filter(d.get("src", "")):
                fout.write(line); n += 1
    return n


def quick_train(streams_path: Path, out_path: Path, epochs: int = 8,
                  batch: int = 64, lr: float = 3e-4,
                  init_from: Path = None):
    """Train an LM on the given stream file. Optionally init from a checkpoint."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if init_from is not None and init_from.exists():
        model = load_model(init_from, device=device)
        print(f"  init from: {init_from.name}")
    else:
        cfg = GrammarLMConfig()
        model = GrammarLM(cfg).to(device)
        print(f"  init random")

    ds = OperatorDataset(streams_path, block_size=model.cfg.block_size)
    if len(ds) == 0:
        print("  (no training examples)")
        return None

    from torch.utils.data import DataLoader
    loader = DataLoader(ds, batch_size=min(batch, max(1, len(ds))),
                        shuffle=True, drop_last=False)
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01,
                              betas=(0.9, 0.95))
    n_steps = max(1, epochs * len(loader))
    sched = torch.optim.lr_scheduler.LambdaLR(
        opt, lambda step: max(1e-3, math.cos(math.pi * step / (2 * n_steps))))

    losses = []
    for epoch in range(epochs):
        model.train()
        for x, y in loader:
            x = x.to(device); y = y.to(device)
            _, loss = model(x, targets=y)
            opt.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step(); sched.step()
            losses.append(loss.item())
    final_loss = sum(losses[-50:]) / len(losses[-50:]) if losses else float('nan')
    save_model(model, out_path)
    return model, final_loss


def evaluate(model, test_seqs):
    """Return (mean log-lik per token, mean top-1 accuracy)."""
    if model is None: return float('nan'), float('nan')
    model.eval()
    device = next(model.parameters()).device
    log_liks = []
    correct = 0; n_pred = 0
    with torch.no_grad():
        for seq in test_seqs:
            ids = [SPECIAL_IDS["BOS"]] + seq
            if len(ids) < 2: continue
            t = torch.tensor(ids, dtype=torch.long, device=device).unsqueeze(0)
            t = t[:, -model.cfg.block_size:]
            x = t[:, :-1]; y = t[:, 1:]
            logits, _ = model(x)
            import torch.nn.functional as F
            log_p = F.log_softmax(logits, dim=-1)
            ll = log_p.gather(2, y.unsqueeze(-1)).squeeze(-1).mean().item()
            log_liks.append(ll)
            pred = logits.argmax(dim=-1)
            correct += (pred == y).sum().item()
            n_pred += y.numel()
    mean_ll = sum(log_liks) / len(log_liks) if log_liks else float('nan')
    acc = correct / n_pred if n_pred else 0.0
    return mean_ll, acc


def main():
    print("=" * 80)
    print("Compare LM variants: mixed vs real-only vs curriculum")
    print("=" * 80)

    # Build subset corpora
    real_path = HERE / "training_streams_real.jsonl"
    synth_path = HERE / "training_streams_synth.jsonl"
    n_real = make_streams_subset(
        lambda s: s in ("dream_journal", "crystal_op_sig", "cortex_history", "canon"),
        real_path)
    n_synth = make_streams_subset(
        lambda s: s in ("tsml_walk", "bhml_walk", "tb_mix_walk"),
        synth_path)
    print(f"\nReal-only sequences:  {n_real}")
    print(f"Synth-only sequences: {n_synth}")

    # ── Test set ──────────────────────────────────────────────────────
    OP = NAME_TO_ID
    canon_test = [
        [OP["VOID"], OP["LATTICE"], OP["COUNTER"]],         # 012
        [OP["BALANCE"], OP["CHAOS"], OP["HARMONY"]],        # 567
        [OP["HARMONY"], OP["BREATH"], OP["RESET"]],         # 789
        [OP["LATTICE"], OP["PROGRESS"], OP["RESET"], OP["HARMONY"]],  # 1397
        [OP["COUNTER"], OP["COLLAPSE"], OP["BREATH"], OP["CHAOS"]],   # 2486
    ]
    real_test = [
        [OP["HARMONY"], OP["HARMONY"]],   # 256x in dream_journal
        [OP["HARMONY"], OP["COUNTER"]],   # 8x
        [OP["LATTICE"], OP["BALANCE"]],   # 6x
        [OP["HARMONY"], OP["PROGRESS"]],  # 3x
        [OP["LATTICE"], OP["COUNTER"]],   # 1x
    ]
    anti_test = [
        [OP["RESET"], OP["BREATH"], OP["LATTICE"]],
        [OP["BREATH"], OP["LATTICE"], OP["COUNTER"]],
        [OP["LATTICE"], OP["LATTICE"], OP["LATTICE"]],
    ]
    random_test = [
        [OP["VOID"], OP["BALANCE"], OP["BREATH"]],
        [OP["RESET"], OP["VOID"], OP["COUNTER"]],
        [OP["COLLAPSE"], OP["LATTICE"], OP["RESET"]],
    ]

    # ── Variant 1: mixed (already trained at ck_grammar_lm.pt) ───────
    print("\n--- v1: MIXED (pre-trained, both real+synth) ---")
    v1 = load_model(HERE / "ck_grammar_lm.pt")
    print(f"  params: {v1.n_params():,}")

    # ── Variant 2: real-only ─────────────────────────────────────────
    print("\n--- v2: REAL-ONLY (621 tokens, will overfit) ---")
    v2_path = HERE / "ck_grammar_lm_real_only.pt"
    v2_train = quick_train(real_path, v2_path, epochs=20, batch=16, lr=3e-4)
    if v2_train: v2, v2_loss = v2_train; print(f"  final loss: {v2_loss:.4f}")
    else: v2 = None

    # ── Variant 3: curriculum (synth pretrain -> real finetune) ──────
    print("\n--- v3: CURRICULUM (synth pretrain -> real finetune) ---")
    v3_pretrain_path = HERE / "ck_grammar_lm_synth_pretrain.pt"
    print("  Pretraining on synthetic walks...")
    v3_pre = quick_train(synth_path, v3_pretrain_path, epochs=4, batch=128, lr=3e-4)
    if v3_pre:
        v3p, v3p_loss = v3_pre
        print(f"  pretrain final loss: {v3p_loss:.4f}")
    print("  Finetuning on real data...")
    v3_path = HERE / "ck_grammar_lm_curriculum.pt"
    v3_train = quick_train(real_path, v3_path, epochs=15, batch=16, lr=1e-4,
                            init_from=v3_pretrain_path)
    if v3_train: v3, v3_loss = v3_train; print(f"  finetune final loss: {v3_loss:.4f}")
    else: v3 = None

    # ── Evaluate all variants ────────────────────────────────────────
    print("\n" + "=" * 80)
    print(f"{'set':<14} {'v1 mixed':>20} {'v2 real':>20} {'v3 curric':>20}")
    print("-" * 80)
    for name, test in [("canon", canon_test), ("real", real_test),
                        ("anti-canon", anti_test), ("random", random_test)]:
        v1_ll, v1_acc = evaluate(v1, test)
        v2_ll, v2_acc = evaluate(v2, test)
        v3_ll, v3_acc = evaluate(v3, test)
        print(f"  {name:<12} ll={v1_ll:>+6.2f} acc={v1_acc:.2f}   "
              f"ll={v2_ll:>+6.2f} acc={v2_acc:.2f}   "
              f"ll={v3_ll:>+6.2f} acc={v3_acc:.2f}")

    # ── Predict-next on key prefixes ─────────────────────────────────
    print("\n=== Top-3 predictions on canonical prefixes ===")
    prefixes = [
        ("VOID-LATTICE",   [SPECIAL_IDS["BOS"], OP["VOID"], OP["LATTICE"]]),
        ("BALANCE-CHAOS",  [SPECIAL_IDS["BOS"], OP["BALANCE"], OP["CHAOS"]]),
        ("HARMONY-HARMONY", [SPECIAL_IDS["BOS"], OP["HARMONY"], OP["HARMONY"]]),
        ("RESET-BREATH",   [SPECIAL_IDS["BOS"], OP["RESET"], OP["BREATH"]]),
    ]
    for label, prefix in prefixes:
        print(f"\n  After {label}:")
        for tag, m in [("v1 mixed", v1), ("v2 real", v2), ("v3 curric", v3)]:
            if m is None: continue
            preds = m.predict_next(prefix, top_k=3)
            preds_str = ", ".join(f"{token_name(i)}({p:.2f})" for i, p in preds)
            print(f"    {tag:11s}  {preds_str}")


if __name__ == "__main__":
    main()
