"""
train_bdc.py -- train a BDC-LM on accumulated bdc_logs/.

Brayden 2026-05-02: "BDC-LM training after a week of accumulated
bdc_log_*.jsonl data".  This script is the trainer.  It is RUNNABLE
TODAY but currently only on the ~3 records the BDC logger has captured
since it went live -- nowhere near enough to train.

Run after a week of normal use:
    python train_bdc.py --min-records 1000

The script implements multi-task training using MultiHeadGrammarLM
(see multi_head_lm.py): operator stream as input, with auxiliary
(B, D, B') prediction targets.

Schema mapping from bdc_log records:
  input:  doing.input_ops   (operator stream of the user's text)
  target_op:  becoming "next consensus operator"  (per-turn)
  target_attractor: becoming.attractor_layer
  target_breath: being.breath
  target_role: V/F/S/T of consensus
  target_band: becoming.band

Cross-turn context: each chat turn is one training example;
sequences are short (10-20 ops typically).

Loss: weighted sum of cross-entropy per active head.  Head weights
adjustable via --head-weight-op, etc.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import torch
from torch.utils.data import Dataset, DataLoader

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))

from ck_grammar_lm import (
    OP_NAMES, NAME_TO_ID, SPECIAL_IDS, VOCAB_SIZE as OP_VOCAB_SIZE,
)
from multi_head_lm import (
    MultiHeadGrammarLM, MultiHeadConfig,
    ATTRACTOR_VOCAB, BREATH_VOCAB, ROLE_VOCAB, BAND_VOCAB,
)
from ck_invariants_bridge import role as op_role


# Vocab indexers
ATTR_TO_ID = {n: i for i, n in enumerate(ATTRACTOR_VOCAB)}
BREATH_TO_ID = {n: i for i, n in enumerate(BREATH_VOCAB)}
ROLE_TO_ID = {n: i for i, n in enumerate(ROLE_VOCAB)}
BAND_TO_ID = {n: i for i, n in enumerate(BAND_VOCAB)}


def load_bdc_records(log_dir: Path, min_records: int = 0
                      ) -> List[Dict]:
    records = []
    for p in sorted(log_dir.glob("bdc_log_*.jsonl")):
        try:
            with open(p, encoding='utf-8') as f:
                for line in f:
                    try:
                        records.append(json.loads(line))
                    except Exception:
                        pass
        except Exception:
            pass
    if len(records) < min_records:
        return []
    return records


def record_to_example(rec: Dict) -> Optional[Dict]:
    """Convert one BDC record to a training example dict.

    Returns None if essential fields missing.
    """
    if rec.get('trigger') != 'chat_turn':
        return None
    doing = rec.get('doing', {})
    becoming = rec.get('becoming', {})
    being = rec.get('being', {})
    input_ops = doing.get('input_ops', [])
    if not input_ops:
        return None
    # Convert input_ops (could be names or ids) to ids
    op_ids = []
    for op in input_ops:
        if isinstance(op, str) and op in NAME_TO_ID:
            op_ids.append(NAME_TO_ID[op])
        elif isinstance(op, int) and 0 <= op < 10:
            op_ids.append(op)
    if not op_ids:
        return None
    # Targets
    consensus = doing.get('consensus', '')
    target_op_id = NAME_TO_ID.get(consensus, -100)  # -100 = ignore_index
    target_role_id = ROLE_TO_ID.get(op_role(target_op_id) if target_op_id >= 0 else "", -100)
    if target_role_id == -100 and target_op_id >= 0:
        target_role_id = ROLE_TO_ID.get(op_role(target_op_id), -100)
    target_attractor_id = ATTR_TO_ID.get(becoming.get('attractor_layer', ''), -100)
    target_breath_id = BREATH_TO_ID.get(being.get('breath', 'NONE'), BREATH_TO_ID['NONE'])
    target_band_id = BAND_TO_ID.get(becoming.get('band', 'NONE'), BAND_TO_ID['NONE'])
    return {
        "ops": op_ids,
        "target_op": target_op_id,
        "target_attractor": target_attractor_id,
        "target_breath": target_breath_id,
        "target_role": target_role_id,
        "target_band": target_band_id,
    }


class BDCDataset(Dataset):
    def __init__(self, examples: List[Dict], block_size: int = 64):
        self.examples = examples
        self.block_size = block_size

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        ex = self.examples[idx]
        ops = [SPECIAL_IDS['BOS']] + ex['ops'] + [SPECIAL_IDS['EOS']]
        ops = ops[:self.block_size + 1]
        # Pad to block_size + 1 if needed for batching
        x = torch.tensor(ops[:-1], dtype=torch.long)
        # For per-token op prediction (next-op LM), targets shift by 1
        next_ops = torch.tensor(ops[1:], dtype=torch.long)
        # The aux targets (attractor, breath, role, band) are PER-TURN, so
        # broadcast to all positions (shape T) as the same value.
        T = x.size(0)
        attr = torch.full((T,), ex['target_attractor'], dtype=torch.long)
        breath = torch.full((T,), ex['target_breath'], dtype=torch.long)
        role_t = torch.full((T,), ex['target_role'], dtype=torch.long)
        band = torch.full((T,), ex['target_band'], dtype=torch.long)
        return x, {
            "op": next_ops,
            "attractor": attr,
            "breath": breath,
            "role": role_t,
            "band": band,
        }


def collate(batch):
    # Variable-length sequences -- pad to longest in batch
    max_len = max(b[0].size(0) for b in batch)
    xs = []; tgts = {k: [] for k in batch[0][1].keys()}
    for x, t in batch:
        pad = max_len - x.size(0)
        if pad > 0:
            x = torch.cat([x, torch.full((pad,), SPECIAL_IDS['EOS'], dtype=torch.long)])
            for k in tgts:
                t[k] = torch.cat([t[k], torch.full((pad,), -100, dtype=torch.long)])
        xs.append(x)
        for k in tgts:
            tgts[k].append(t[k])
    X = torch.stack(xs, dim=0)
    T = {k: torch.stack(v, dim=0) for k, v in tgts.items()}
    return X, T


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--log-dir",
                    default=str(Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\bdc_logs")))
    ap.add_argument("--out", default=str(HERE / "bdc_lm.pt"))
    ap.add_argument("--epochs", type=int, default=10)
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--min-records", type=int, default=200,
                    help="Refuse to train with fewer records than this")
    ap.add_argument("--head-weight-op", type=float, default=1.0)
    ap.add_argument("--head-weight-attractor", type=float, default=0.5)
    ap.add_argument("--head-weight-breath", type=float, default=0.3)
    ap.add_argument("--head-weight-role", type=float, default=0.3)
    ap.add_argument("--head-weight-band", type=float, default=0.3)
    args = ap.parse_args()

    records = load_bdc_records(Path(args.log_dir), min_records=args.min_records)
    if not records:
        print(f"Insufficient BDC records (< {args.min_records}). "
              f"Check {args.log_dir}/bdc_log_*.jsonl.")
        print(f"  Found total records: "
              f"{sum(1 for _ in Path(args.log_dir).glob('bdc_log_*.jsonl'))}")
        print("  Run normal CK chat for a week or so to accumulate data, "
              "then re-run.")
        return

    examples = [record_to_example(r) for r in records]
    examples = [e for e in examples if e is not None]
    print(f"Loaded {len(examples)} usable training examples from "
          f"{len(records)} records")

    cfg = MultiHeadConfig()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = MultiHeadGrammarLM(cfg).to(device)
    print(f"Model: {model.n_params():,} params on {device}")

    ds = BDCDataset(examples, block_size=cfg.block_size)
    loader = DataLoader(ds, batch_size=args.batch, shuffle=True,
                         collate_fn=collate, drop_last=False)

    opt = torch.optim.AdamW(model.parameters(), lr=args.lr,
                              weight_decay=0.01, betas=(0.9, 0.95))

    head_weights = {
        "op": args.head_weight_op,
        "attractor": args.head_weight_attractor,
        "breath": args.head_weight_breath,
        "role": args.head_weight_role,
        "band": args.head_weight_band,
    }

    print(f"\nTraining {args.epochs} epochs with head weights: {head_weights}")
    print(f"{'epoch':>5} {'loss':>10}")
    print("-" * 30)
    t0 = time.time()
    for epoch in range(args.epochs):
        model.train()
        losses = []
        for x, tgts in loader:
            x = x.to(device)
            tgts = {k: v.to(device) for k, v in tgts.items()}
            _, loss = model(x, targets=tgts, head_weights=head_weights)
            opt.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            losses.append(loss.item())
        avg = sum(losses) / len(losses) if losses else float('nan')
        print(f"{epoch:>5} {avg:>10.4f}")

    elapsed = time.time() - t0
    print(f"\nTrained in {elapsed:.1f}s")
    torch.save({"cfg": cfg.__dict__, "state_dict": model.state_dict()},
                Path(args.out))
    print(f"Saved to {args.out}")


if __name__ == "__main__":
    main()
