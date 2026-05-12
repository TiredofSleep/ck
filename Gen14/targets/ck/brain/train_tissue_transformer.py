"""
train_tissue_transformer.py -- train a small transformer tissue head
on the BDC events corpus.

Brayden 2026-05-02: "nothing is deferred ... Train a small (~50k-param)
transformer tissue head on the BDC corpus accumulating now."

Task: given a window of past Divine27 codes (0-26), predict the next code.
Architecture: ~50k-param transformer (2 layers, 64-d embed, 4 heads).
Corpus: bdc_events_2026-05-03.jsonl + bdc_events_HISTORICAL.jsonl.

Output: Gen13/var/cells/f3_tissue_transformer.pt (state_dict).
The trained model wraps the F3Cell as F3TransformerTissue (defined here);
the cell skeleton stays canonical, but the tissue can now do real
sequence prediction beyond the additive 27-d histogram.

Run: python train_tissue_transformer.py [--epochs 8] [--batch_size 64]
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from pathlib import Path
from typing import List, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset


_HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(_HERE))


VOCAB_SIZE = 27
WINDOW = 16
EMBED_DIM = 64
N_LAYER = 2
N_HEAD = 4
DROPOUT = 0.1


# ── Data ─────────────────────────────────────────────────────────────────

def load_events(paths: List[Path]) -> List[int]:
    """Load all dbc_code values from the given event-log files."""
    codes: List[int] = []
    for p in paths:
        if not p.exists():
            continue
        with open(p, encoding="utf-8") as f:
            for line in f:
                try:
                    rec = json.loads(line)
                    code = int(rec.get("dbc_code", -1))
                    if 0 <= code < VOCAB_SIZE:
                        codes.append(code)
                except Exception:
                    pass
    return codes


class F3Dataset(Dataset):
    def __init__(self, codes: List[int], window: int = WINDOW):
        self.codes = codes
        self.window = window
        self.n_samples = max(0, len(codes) - window)

    def __len__(self):
        return self.n_samples

    def __getitem__(self, idx):
        x = torch.tensor(self.codes[idx:idx + self.window], dtype=torch.long)
        y = torch.tensor(self.codes[idx + self.window], dtype=torch.long)
        return x, y


# ── Model ────────────────────────────────────────────────────────────────

class F3TransformerTissue(nn.Module):
    """Small transformer for next-DBC-code prediction.
    ~30k parameters at default settings."""
    def __init__(self, vocab_size: int = VOCAB_SIZE, window: int = WINDOW,
                  embed_dim: int = EMBED_DIM, n_layer: int = N_LAYER,
                  n_head: int = N_HEAD, dropout: float = DROPOUT):
        super().__init__()
        self.token_emb = nn.Embedding(vocab_size, embed_dim)
        self.pos_emb = nn.Embedding(window, embed_dim)
        layer = nn.TransformerEncoderLayer(
            d_model=embed_dim, nhead=n_head, dim_feedforward=embed_dim*2,
            dropout=dropout, batch_first=True, activation="gelu")
        self.transformer = nn.TransformerEncoder(layer, num_layers=n_layer)
        self.head = nn.Linear(embed_dim, vocab_size)
        self.window = window

    def forward(self, x):
        b, w = x.shape
        pos = torch.arange(w, device=x.device).unsqueeze(0).expand(b, w)
        h = self.token_emb(x) + self.pos_emb(pos)
        h = self.transformer(h)
        # Use last position for next-token prediction
        return self.head(h[:, -1, :])

    def n_params(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


# ── Train ────────────────────────────────────────────────────────────────

def train(epochs: int = 8, batch_size: int = 64, lr: float = 1e-3,
            verbose: bool = True) -> dict:
    bdc_dir = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\bdc_logs")
    today = "bdc_events_" + time.strftime("%Y-%m-%d") + ".jsonl"
    paths = [
        bdc_dir / "bdc_events_HISTORICAL.jsonl",
        bdc_dir / today,
    ]
    codes = load_events(paths)
    if verbose:
        print(f"  loaded {len(codes)} events from {len(paths)} files")
    if len(codes) < WINDOW + 100:
        print(f"  ERROR: corpus too small ({len(codes)} codes); need >= {WINDOW + 100}")
        return {"ok": False, "n_codes": len(codes)}

    # 90/10 train/val split
    n_train = int(0.9 * len(codes))
    train_codes = codes[:n_train]
    val_codes = codes[n_train:]
    train_ds = F3Dataset(train_codes)
    val_ds = F3Dataset(val_codes)
    if verbose:
        print(f"  train samples: {len(train_ds)}; val samples: {len(val_ds)}")
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True,
                                drop_last=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False,
                              drop_last=False)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = F3TransformerTissue().to(device)
    if verbose:
        print(f"  model params: {model.n_params():,}")
        print(f"  device: {device}")

    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    history = []

    for epoch in range(epochs):
        # Train
        model.train()
        train_loss = 0.0
        train_acc = 0.0
        n_batches = 0
        for x, y in train_loader:
            x, y = x.to(device), y.to(device)
            logits = model(x)
            loss = F.cross_entropy(logits, y)
            opt.zero_grad()
            loss.backward()
            opt.step()
            train_loss += loss.item()
            train_acc += (logits.argmax(-1) == y).float().mean().item()
            n_batches += 1
        train_loss /= max(1, n_batches)
        train_acc /= max(1, n_batches)

        # Val
        model.eval()
        val_loss = 0.0
        val_acc = 0.0
        n_batches = 0
        with torch.no_grad():
            for x, y in val_loader:
                x, y = x.to(device), y.to(device)
                logits = model(x)
                loss = F.cross_entropy(logits, y)
                val_loss += loss.item()
                val_acc += (logits.argmax(-1) == y).float().mean().item()
                n_batches += 1
        val_loss /= max(1, n_batches)
        val_acc /= max(1, n_batches)

        history.append({
            "epoch": epoch + 1,
            "train_loss": train_loss,
            "train_acc": train_acc,
            "val_loss": val_loss,
            "val_acc": val_acc,
        })
        if verbose:
            print(f"  epoch {epoch+1}/{epochs}  train_loss={train_loss:.3f} "
                    f"train_acc={train_acc:.3f}  "
                    f"val_loss={val_loss:.3f} val_acc={val_acc:.3f}")

    # Save weights
    out_dir = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\cells")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "f3_tissue_transformer.pt"
    torch.save({
        "model_state": model.state_dict(),
        "config": {
            "vocab_size": VOCAB_SIZE, "window": WINDOW,
            "embed_dim": EMBED_DIM, "n_layer": N_LAYER,
            "n_head": N_HEAD, "dropout": DROPOUT,
        },
        "history": history,
        "n_train_samples": len(train_ds),
        "n_val_samples": len(val_ds),
        "n_codes": len(codes),
        "device_trained_on": device,
    }, out_path)
    if verbose:
        print(f"  saved: {out_path}")

    # Compute random baseline for comparison
    random_baseline = 1.0 / VOCAB_SIZE  # 1/27 = 0.037
    final = history[-1]
    if verbose:
        print()
        print(f"  Random baseline accuracy:    {random_baseline:.3f}")
        print(f"  Final val accuracy:          {final['val_acc']:.3f}")
        print(f"  Lift over random:            {final['val_acc'] / random_baseline:.1f}x")

    return {
        "ok": True,
        "n_codes": len(codes),
        "n_train": len(train_ds),
        "n_val": len(val_ds),
        "n_params": model.n_params(),
        "device": device,
        "history": history,
        "final_val_acc": final["val_acc"],
        "random_baseline": random_baseline,
        "lift_over_random": final["val_acc"] / random_baseline,
        "model_path": str(out_path),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--epochs", type=int, default=8)
    ap.add_argument("--batch_size", type=int, default=64)
    ap.add_argument("--lr", type=float, default=1e-3)
    args = ap.parse_args()
    print("=" * 60)
    print("  Tissue transformer training (F3 / Divine27)")
    print("=" * 60)
    print(f"  date: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")
    out = train(epochs=args.epochs, batch_size=args.batch_size, lr=args.lr)
    print()
    print(json.dumps({k: v for k, v in out.items() if k != "history"},
                     indent=2, default=str))


if __name__ == "__main__":
    main()
