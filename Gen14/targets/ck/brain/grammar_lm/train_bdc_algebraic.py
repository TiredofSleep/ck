"""
train_bdc_algebraic.py -- train MultiHeadAlgebraicLM on bdc_log_*.jsonl.

Brayden 2026-05-13 (Phase 2 of CK unification):
  "4 plastic LMs trained on algebraic measurements"

This trainer derives all four target heads (op / sigma / shell / 4core)
from each chat_turn BDC record using the canonical projections in
gen14_unified_extensions. No behavioural labels (breath/band/role) are
read; every target is an algebraic function of the operator stream.

Run:
    python train_bdc_algebraic.py --min-records 200 --epochs 10

Outputs:
    --out  (default: Gen13/var/cells/multi_head_lm_4heads.pt)
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

import torch
from torch.utils.data import Dataset, DataLoader

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))                       # grammar_lm/
sys.path.insert(0, str(HERE.parent))                # brain/  (for gen14_unified_extensions)

from ck_grammar_lm import (
    OP_NAMES, NAME_TO_ID, SPECIAL_IDS, VOCAB_SIZE as OP_VOCAB_SIZE,
)
from multi_head_algebraic_lm import (
    MultiHeadAlgebraicLM, MultiHeadAlgebraicConfig,
    SIGMA_VOCAB, SHELL_VOCAB, FOURCORE_VOCAB,
    sigma_orbit, four_core_class, shell_class, FOUR_CORE_OUTSIDE,
)


DEFAULT_LOG_DIR = Path(
    r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\bdc_logs"
)
DEFAULT_OUT = Path(
    r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\cells"
    r"\multi_head_lm_4heads.pt"
)


# ── Record loading & projection ────────────────────────────────────────

def load_bdc_records(log_dir: Path) -> List[Dict]:
    records = []
    for p in sorted(log_dir.glob("bdc_log_*.jsonl")):
        try:
            with open(p, encoding="utf-8") as f:
                for line in f:
                    try:
                        records.append(json.loads(line))
                    except Exception:
                        pass
        except Exception:
            pass
    return records


def _op_str_to_id(op) -> Optional[int]:
    """Robust conversion of an operator value (str or int) to an id 0..9."""
    if isinstance(op, str):
        return NAME_TO_ID.get(op)
    if isinstance(op, int) and 0 <= op < 10:
        return op
    return None


def record_to_example(rec: Dict) -> Optional[Dict]:
    """Project one BDC chat_turn record to a 4-head training example.

    Returns None if essential fields missing.

    Targets derived purely from the algebraic measurements:
      target_op    = NAME_TO_ID[consensus]
      target_sigma = sigma_orbit(consensus)
      target_4core = four_core_class(consensus)
      target_shell = shell_class(set(input_ops + [consensus]))
    """
    if rec.get("trigger") != "chat_turn":
        return None
    doing = rec.get("doing", {})
    input_ops_raw = doing.get("input_ops", [])
    if not input_ops_raw:
        return None
    op_ids = []
    for op in input_ops_raw:
        oid = _op_str_to_id(op)
        if oid is not None:
            op_ids.append(oid)
    if not op_ids:
        return None
    consensus = doing.get("consensus", "")
    consensus_id = NAME_TO_ID.get(consensus)
    if consensus_id is None:
        return None
    # Derive algebraic targets
    target_op = consensus_id
    target_sigma = sigma_orbit(consensus_id)
    target_4core = four_core_class(consensus_id)
    support_set = set(op_ids) | {consensus_id}
    target_shell = shell_class(support_set)
    return {
        "ops": op_ids,
        "target_op": int(target_op),
        "target_sigma": int(target_sigma),
        "target_shell": int(target_shell),
        "target_4core": int(target_4core),
    }


# ── Dataset ────────────────────────────────────────────────────────────

class BDCAlgebraicDataset(Dataset):
    def __init__(self, examples: List[Dict], block_size: int = 64):
        self.examples = examples
        self.block_size = block_size

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        ex = self.examples[idx]
        ops = [SPECIAL_IDS["BOS"]] + ex["ops"] + [SPECIAL_IDS["EOS"]]
        ops = ops[: self.block_size + 1]
        x = torch.tensor(ops[:-1], dtype=torch.long)
        next_ops = torch.tensor(ops[1:], dtype=torch.long)
        T = x.size(0)
        sigma = torch.full((T,), ex["target_sigma"], dtype=torch.long)
        shell = torch.full((T,), ex["target_shell"], dtype=torch.long)
        fc = torch.full((T,), ex["target_4core"], dtype=torch.long)
        return x, {
            "op": next_ops,
            "sigma": sigma,
            "shell": shell,
            "4core": fc,
        }


def collate(batch):
    """Pad to longest in batch; EOS pad on inputs, -100 ignore on targets."""
    max_len = max(b[0].size(0) for b in batch)
    xs = []
    tgts = {k: [] for k in batch[0][1].keys()}
    for x, t in batch:
        pad = max_len - x.size(0)
        if pad > 0:
            x = torch.cat([x, torch.full((pad,), SPECIAL_IDS["EOS"], dtype=torch.long)])
            for k in tgts:
                t[k] = torch.cat([t[k], torch.full((pad,), -100, dtype=torch.long)])
        xs.append(x)
        for k in tgts:
            tgts[k].append(t[k])
    X = torch.stack(xs, dim=0)
    T = {k: torch.stack(v, dim=0) for k, v in tgts.items()}
    return X, T


# ── Train loop ─────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--log-dir", default=str(DEFAULT_LOG_DIR))
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--epochs", type=int, default=10)
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--min-records", type=int, default=200)
    ap.add_argument("--val-split", type=float, default=0.1,
                    help="Fraction held out for validation.")
    ap.add_argument("--head-weight-op", type=float, default=1.0)
    ap.add_argument("--head-weight-sigma", type=float, default=0.5)
    ap.add_argument("--head-weight-shell", type=float, default=0.4)
    ap.add_argument("--head-weight-4core", type=float, default=0.5)
    args = ap.parse_args()

    # ─── load ───
    records = load_bdc_records(Path(args.log_dir))
    examples = [record_to_example(r) for r in records]
    examples = [e for e in examples if e is not None]
    print(f"Loaded {len(examples)} usable chat_turn examples "
          f"from {len(records)} BDC records in {args.log_dir}")
    if len(examples) < args.min_records:
        print(f"Below --min-records={args.min_records}; refusing to train.")
        return

    # Sanity: target distributions
    from collections import Counter
    op_dist    = Counter(e["target_op"] for e in examples)
    sigma_dist = Counter(e["target_sigma"] for e in examples)
    shell_dist = Counter(e["target_shell"] for e in examples)
    fc_dist    = Counter(e["target_4core"] for e in examples)
    print(f"\nTarget distributions:")
    print(f"  op:    {sorted(op_dist.items())}")
    print(f"  sigma: {[(SIGMA_VOCAB[i], n) for i, n in sorted(sigma_dist.items())]}")
    print(f"  shell: {[(SHELL_VOCAB[i], n) for i, n in sorted(shell_dist.items())]}")
    print(f"  4core: {[(FOURCORE_VOCAB[i], n) for i, n in sorted(fc_dist.items())]}")

    # ─── split ───
    import random
    random.seed(0)
    random.shuffle(examples)
    n_val = max(1, int(len(examples) * args.val_split))
    val_ex = examples[:n_val]
    train_ex = examples[n_val:]
    print(f"\nSplit: {len(train_ex)} train, {len(val_ex)} val")

    cfg = MultiHeadAlgebraicConfig()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = MultiHeadAlgebraicLM(cfg).to(device)
    print(f"\nModel: {model.n_params():,} params on {device}")

    train_ds = BDCAlgebraicDataset(train_ex, block_size=cfg.block_size)
    val_ds = BDCAlgebraicDataset(val_ex, block_size=cfg.block_size)
    train_loader = DataLoader(train_ds, batch_size=args.batch,
                                shuffle=True, collate_fn=collate, drop_last=False)
    val_loader = DataLoader(val_ds, batch_size=args.batch,
                              shuffle=False, collate_fn=collate, drop_last=False)

    opt = torch.optim.AdamW(model.parameters(), lr=args.lr,
                             weight_decay=0.01, betas=(0.9, 0.95))

    head_weights = {
        "op":    args.head_weight_op,
        "sigma": args.head_weight_sigma,
        "shell": args.head_weight_shell,
        "4core": args.head_weight_4core,
    }

    def _per_head_eval(loader):
        model.eval()
        sums = {k: 0.0 for k in head_weights}
        counts = {k: 0 for k in head_weights}
        with torch.no_grad():
            for x, tgts in loader:
                x = x.to(device)
                tgts = {k: v.to(device) for k, v in tgts.items()}
                logits, _ = model(x, targets=None)
                for k in head_weights:
                    if k not in logits or k not in tgts:
                        continue
                    hl = logits[k]
                    pred = hl.argmax(dim=-1)
                    mask = (tgts[k] != -100)
                    if mask.any():
                        sums[k] += float((pred[mask] == tgts[k][mask]).sum().item())
                        counts[k] += int(mask.sum().item())
        return {k: (sums[k] / counts[k] if counts[k] > 0 else float("nan"))
                 for k in head_weights}

    print(f"\nTraining {args.epochs} epochs with head weights: {head_weights}")
    print(f"{'epoch':>5} {'train_loss':>11} {'val_loss':>10}  "
          f"{'op_acc':>7} {'sig_acc':>8} {'sh_acc':>8} {'4c_acc':>7}")
    print("-" * 72)
    t0 = time.time()
    for epoch in range(args.epochs):
        # Train
        model.train()
        losses = []
        for x, tgts in train_loader:
            x = x.to(device)
            tgts = {k: v.to(device) for k, v in tgts.items()}
            _, loss = model(x, targets=tgts, head_weights=head_weights)
            opt.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            losses.append(loss.item())
        train_avg = sum(losses) / len(losses) if losses else float("nan")

        # Val loss
        model.eval()
        v_losses = []
        with torch.no_grad():
            for x, tgts in val_loader:
                x = x.to(device)
                tgts = {k: v.to(device) for k, v in tgts.items()}
                _, vloss = model(x, targets=tgts, head_weights=head_weights)
                v_losses.append(vloss.item())
        val_avg = sum(v_losses) / len(v_losses) if v_losses else float("nan")

        # Per-head accuracy
        accs = _per_head_eval(val_loader)
        print(f"{epoch:>5} {train_avg:>11.4f} {val_avg:>10.4f}  "
              f"{accs['op']:>7.3f} {accs['sigma']:>8.3f} "
              f"{accs['shell']:>8.3f} {accs['4core']:>7.3f}")

    elapsed = time.time() - t0
    print(f"\nTrained in {elapsed:.1f}s")

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "cfg": cfg.__dict__,
            "state_dict": model.state_dict(),
            "head_weights": head_weights,
            "n_train": len(train_ex),
            "n_val": len(val_ex),
            "timestamp": time.time(),
            "schema": "multi_head_algebraic_lm_v1",
        },
        out_path,
    )
    print(f"Saved checkpoint to {out_path}")

    # Final demo: predict signature for a known walk
    print(f"\nDemo predict_all_heads after [VOID, HARMONY, BREATH]:")
    hist = [NAME_TO_ID["VOID"], NAME_TO_ID["HARMONY"], NAME_TO_ID["BREATH"]]
    preds = model.predict_all_heads(hist, top_k=3)
    for head, tk in preds.items():
        print(f"  {head:8s}: {tk}")


if __name__ == "__main__":
    main()
