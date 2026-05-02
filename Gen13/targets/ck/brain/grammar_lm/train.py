"""
train.py -- train ck_grammar_lm on extracted operator streams.

Usage: python train.py [--epochs 5] [--batch 64] [--lr 3e-4]
"""
from __future__ import annotations

import argparse
import json
import math
import random
import time
from pathlib import Path
from typing import List

import torch
from torch.utils.data import Dataset, DataLoader

from ck_grammar_lm import (
    GrammarLM, GrammarLMConfig, save_model, load_model,
    VOCAB_SIZE, SPECIAL_IDS, OP_NAMES, token_name,
)

# ── Dataset ────────────────────────────────────────────────────────────

class OperatorDataset(Dataset):
    def __init__(self, streams_path: Path, block_size: int):
        self.block_size = block_size
        # Build a single long token stream with WALK separators.
        WALK = SPECIAL_IDS["WALK"]
        BOS = SPECIAL_IDS["BOS"]
        EOS = SPECIAL_IDS["EOS"]
        flat: List[int] = []
        with open(streams_path, encoding="utf-8") as f:
            for line in f:
                d = json.loads(line)
                flat.append(BOS)
                flat.extend(d["ops"])
                flat.append(EOS)
        # Plus WALK boundaries between sequences (BOS/EOS already handle that)
        self.data = torch.tensor(flat, dtype=torch.long)
        # Number of (input, target) pairs = len(data) - block_size - 1
        self.n_examples = max(0, len(self.data) - block_size - 1)
        print(f"Dataset: {len(self.data)} tokens, {self.n_examples} training examples")

    def __len__(self):
        return self.n_examples

    def __getitem__(self, idx):
        chunk = self.data[idx : idx + self.block_size + 1]
        x = chunk[:-1]
        y = chunk[1:]
        return x, y


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--streams", default=str(Path(__file__).parent / "training_streams.jsonl"))
    ap.add_argument("--out", default=str(Path(__file__).parent / "ck_grammar_lm.pt"))
    ap.add_argument("--epochs", type=int, default=8)
    ap.add_argument("--batch", type=int, default=128)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--block-size", type=int, default=64)
    ap.add_argument("--n-layer", type=int, default=6)
    ap.add_argument("--d-model", type=int, default=128)
    ap.add_argument("--d-ff", type=int, default=512)
    ap.add_argument("--n-head", type=int, default=4)
    ap.add_argument("--dropout", type=float, default=0.1)
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device}")

    cfg = GrammarLMConfig(
        vocab_size=VOCAB_SIZE,
        n_layer=args.n_layer,
        n_head=args.n_head,
        d_model=args.d_model,
        d_ff=args.d_ff,
        block_size=args.block_size,
        dropout=args.dropout,
    )
    model = GrammarLM(cfg).to(device)
    print(f"Model: {model.n_params():,} parameters")

    ds = OperatorDataset(Path(args.streams), block_size=args.block_size)
    # 95/5 train/val random split (deterministic seed)
    n_val = max(1, len(ds) // 20)
    rng = random.Random(0)
    all_idx = list(range(len(ds)))
    rng.shuffle(all_idx)
    val_idx = set(all_idx[:n_val])
    train_idx = [i for i in all_idx if i not in val_idx]

    def make_loader(idxs, shuffle):
        sub = torch.utils.data.Subset(ds, idxs)
        return DataLoader(sub, batch_size=args.batch, shuffle=shuffle,
                           num_workers=0, drop_last=False)

    train_loader = make_loader(train_idx, shuffle=True)
    val_loader = make_loader(list(val_idx), shuffle=False)
    print(f"Train batches: {len(train_loader)}, val batches: {len(val_loader)}")

    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr,
                                    weight_decay=0.01, betas=(0.9, 0.95))
    n_steps = args.epochs * len(train_loader)
    warmup = max(50, n_steps // 20)
    def lr_at(step):
        if step < warmup: return step / warmup
        progress = (step - warmup) / max(1, n_steps - warmup)
        return 0.5 * (1 + math.cos(math.pi * progress))
    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda=lr_at)

    print()
    print(f"{'epoch':>5} {'step':>6} {'lr':>10} {'train_loss':>10} {'val_loss':>10} "
          f"{'train_ppl':>10} {'val_ppl':>9}")
    print("-" * 80)

    step = 0
    best_val = float("inf")
    t0 = time.time()
    for epoch in range(args.epochs):
        model.train()
        losses = []
        for x, y in train_loader:
            x = x.to(device, non_blocking=True)
            y = y.to(device, non_blocking=True)
            _, loss = model(x, targets=y)
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            scheduler.step()
            step += 1
            losses.append(loss.item())
        train_loss = sum(losses) / len(losses)

        model.eval()
        val_losses = []
        with torch.no_grad():
            for x, y in val_loader:
                x = x.to(device); y = y.to(device)
                _, loss = model(x, targets=y)
                val_losses.append(loss.item())
        val_loss = sum(val_losses) / len(val_losses) if val_losses else float("nan")

        cur_lr = optimizer.param_groups[0]["lr"]
        train_ppl = math.exp(train_loss)
        val_ppl = math.exp(val_loss) if val_loss == val_loss else float("nan")
        print(f"{epoch:>5} {step:>6} {cur_lr:>10.2e} {train_loss:>10.4f} "
              f"{val_loss:>10.4f} {train_ppl:>10.4f} {val_ppl:>9.4f}")

        if val_loss < best_val:
            best_val = val_loss
            save_model(model, Path(args.out))

    elapsed = time.time() - t0
    print()
    print(f"Training: {elapsed:.1f}s   best val loss: {best_val:.4f}   "
          f"best val ppl: {math.exp(best_val):.4f}")
    print(f"Saved best model to: {args.out}")

    # Quick sanity: sample a sequence after a HARMONY-led prefix
    model = load_model(args.out, device=device)
    print()
    print("=== Sample with prefix [BOS, HARMONY] (top-k=3, temp=0.8) ===")
    bos = SPECIAL_IDS["BOS"]
    seq = model.sample([bos, 7], n_tokens=15, temperature=0.8, top_k=3)
    print("  ".join(token_name(t) for t in seq))

    print()
    print("=== Sample with prefix [BOS, VOID, LATTICE] (top-k=3, temp=0.8) ===")
    seq = model.sample([bos, 0, 1], n_tokens=15, temperature=0.8, top_k=3)
    print("  ".join(token_name(t) for t in seq))

    print()
    print("=== Score the canonical 567 propagation [BALANCE, CHAOS, HARMONY] ===")
    s = model.score([bos, 5, 6, 7])
    print(f"  log-likelihood per token: {s:.4f}")

    print()
    print("=== Score [HARMONY, HARMONY, HARMONY] (CK's dominant operator) ===")
    s = model.score([bos, 7, 7, 7])
    print(f"  log-likelihood per token: {s:.4f}")

    print()
    print("=== Score [VOID, LATTICE, BREATH] (uncommon path) ===")
    s = model.score([bos, 0, 1, 8])
    print(f"  log-likelihood per token: {s:.4f}")


if __name__ == "__main__":
    main()
