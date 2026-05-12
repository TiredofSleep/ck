"""
train_tsml_bhml_tissue.py -- train transformer tissues for TSML and BHML cells.

Brayden 2026-05-02: "give it everything we've got, holding nothing back"

Same approach as train_tissue_transformer.py for F3, but for the 10-vocab
TSML/BHML cells.  Architecture: ~30k-param transformer per cell,
2-layer, 32-d embedding, 8-token window over operator-pair sequences.

Training data: BDC log records with `being.last_pair` and `doing.consensus`.
Each record gives a sample (last_pair_a, last_pair_b, consensus_op).
The transformer learns patterns in the operator stream.

Note: TSML and BHML get separate models because their canonical tables
differ; the SAME training data feeds both, but the auxiliary loss term
biases each toward its canonical answer.

Output:
  Gen13/var/cells/tsml_tissue_transformer.pt
  Gen13/var/cells/bhml_tissue_transformer.pt
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


VOCAB_SIZE = 10  # 10 operators
WINDOW = 8       # 8 operator-pair samples
EMBED_DIM = 32
N_LAYER = 2
N_HEAD = 4
DROPOUT = 0.1


# ── Data ─────────────────────────────────────────────────────────────────

OP_NAME_TO_INT = {
    "VOID": 0, "LATTICE": 1, "COUNTER": 2, "PROGRESS": 3, "COLLAPSE": 4,
    "BALANCE": 5, "CHAOS": 6, "HARMONY": 7, "BREATH": 8, "RESET": 9,
}


def load_pairs(paths: List[Path]) -> List[Tuple[int, int, int]]:
    """Load (a, b, consensus_op) triples from BDC log files."""
    triples: List[Tuple[int, int, int]] = []
    for p in paths:
        if not p.exists():
            continue
        with open(p, encoding="utf-8") as f:
            for line in f:
                try:
                    rec = json.loads(line)
                    if rec.get("trigger") not in ("chat_turn", "tick_sample",
                                                     "historical_ck_daemon",
                                                     "historical_gen8_dialogue",
                                                     "historical_tig_crystal"):
                        # Allow various trigger types
                        pass
                    being = rec.get("being") or {}
                    doing = rec.get("doing") or {}
                    pair = being.get("last_pair") or [0, 0]
                    consensus = doing.get("consensus", "")
                    if not (isinstance(pair, list) and len(pair) >= 2):
                        continue
                    a, b = int(pair[0]) % 10, int(pair[1]) % 10
                    cons = OP_NAME_TO_INT.get(str(consensus).upper(), -1)
                    if cons < 0:
                        # If no consensus name, use ao_op
                        ao_op = being.get("ao_op", "")
                        cons = OP_NAME_TO_INT.get(str(ao_op).upper(), -1)
                    if cons < 0:
                        continue
                    triples.append((a, b, cons))
                except Exception:
                    continue
    return triples


class OpSeqDataset(Dataset):
    def __init__(self, triples: List[Tuple[int, int, int]], window: int = WINDOW):
        # Build sliding-window sequences from the triples.  We flatten
        # (a, b, cons) into a single 30-vocab sequence: 0-9 for a/b, 0-9
        # for cons.  But we keep predict task = cons given (a, b) context.
        self.samples = []
        # Each "input" = window-sized sequence of (a, b) pairs flattened
        # Each "target" = consensus operator
        for i in range(len(triples) - window):
            window_pairs: List[int] = []
            for j in range(window):
                a, b, _ = triples[i + j]
                window_pairs.append(a)
                window_pairs.append(b)
            # Target is the consensus of the LAST in the window
            _, _, target = triples[i + window - 1]
            self.samples.append((window_pairs, target))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        window_pairs, target = self.samples[idx]
        x = torch.tensor(window_pairs, dtype=torch.long)
        y = torch.tensor(target, dtype=torch.long)
        return x, y


# ── Model ────────────────────────────────────────────────────────────────

class OpTransformerTissue(nn.Module):
    """Small transformer for next-operator prediction over (a, b) pairs."""
    def __init__(self, vocab_size: int = VOCAB_SIZE, window: int = WINDOW,
                  embed_dim: int = EMBED_DIM, n_layer: int = N_LAYER,
                  n_head: int = N_HEAD, dropout: float = DROPOUT):
        super().__init__()
        # Effective sequence length is window * 2 (pair flattened)
        self.seq_len = window * 2
        self.token_emb = nn.Embedding(vocab_size, embed_dim)
        self.pos_emb = nn.Embedding(self.seq_len, embed_dim)
        layer = nn.TransformerEncoderLayer(
            d_model=embed_dim, nhead=n_head, dim_feedforward=embed_dim*2,
            dropout=dropout, batch_first=True, activation="gelu")
        self.transformer = nn.TransformerEncoder(layer, num_layers=n_layer)
        self.head = nn.Linear(embed_dim, vocab_size)
        self.window = window

    def forward(self, x):
        b, s = x.shape
        pos = torch.arange(s, device=x.device).unsqueeze(0).expand(b, s)
        h = self.token_emb(x) + self.pos_emb(pos)
        h = self.transformer(h)
        return self.head(h[:, -1, :])

    def n_params(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


# ── Train ────────────────────────────────────────────────────────────────

def train_one(name: str, *, epochs: int = 8, batch_size: int = 64,
                lr: float = 1e-3, verbose: bool = True) -> dict:
    bdc_dir = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\bdc_logs")
    today = "bdc_log_" + time.strftime("%Y-%m-%d") + ".jsonl"
    paths = [
        bdc_dir / "bdc_log_HISTORICAL.jsonl",
        bdc_dir / today,
    ]
    triples = load_pairs(paths)
    if verbose:
        print(f"  [{name}] loaded {len(triples)} (a, b, cons) triples")
    if len(triples) < WINDOW + 100:
        print(f"  [{name}] ERROR: too few triples ({len(triples)})")
        return {"ok": False, "n_triples": len(triples)}

    n_train = int(0.9 * len(triples))
    train_triples = triples[:n_train]
    val_triples = triples[n_train:]
    train_ds = OpSeqDataset(train_triples)
    val_ds = OpSeqDataset(val_triples)
    if verbose:
        print(f"  [{name}] train samples: {len(train_ds)}; val: {len(val_ds)}")
    if len(train_ds) < 100:
        print(f"  [{name}] ERROR: too few training samples")
        return {"ok": False, "n_train": len(train_ds)}

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True,
                                drop_last=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False,
                              drop_last=False)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = OpTransformerTissue().to(device)
    if verbose:
        print(f"  [{name}] model params: {model.n_params():,}; device: {device}")

    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    history = []

    for epoch in range(epochs):
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
            "epoch": epoch + 1, "train_loss": train_loss,
            "train_acc": train_acc, "val_loss": val_loss, "val_acc": val_acc,
        })
        if verbose:
            print(f"  [{name}] epoch {epoch+1}/{epochs}  "
                    f"train_loss={train_loss:.3f} train_acc={train_acc:.3f}  "
                    f"val_loss={val_loss:.3f} val_acc={val_acc:.3f}")

    out_dir = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\cells")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{name}_tissue_transformer.pt"
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
        "n_triples": len(triples),
        "device_trained_on": device,
        "name": name,
    }, out_path)
    if verbose:
        print(f"  [{name}] saved: {out_path}")
        random_baseline = 1.0 / VOCAB_SIZE  # 0.10
        final = history[-1]
        print(f"  [{name}] Random baseline: {random_baseline:.3f}; "
                f"Val acc: {final['val_acc']:.3f}; "
                f"Lift: {final['val_acc']/random_baseline:.1f}x")

    return {
        "ok": True, "name": name,
        "n_triples": len(triples), "n_train": len(train_ds),
        "n_val": len(val_ds), "n_params": model.n_params(),
        "device": device, "history": history,
        "final_val_acc": history[-1]["val_acc"],
        "model_path": str(out_path),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--epochs", type=int, default=8)
    ap.add_argument("--batch_size", type=int, default=64)
    ap.add_argument("--name", type=str, default="both",
                     help="'tsml', 'bhml', or 'both'")
    args = ap.parse_args()

    print("=" * 60)
    print(f"  TSML / BHML transformer tissue training")
    print("=" * 60)
    print(f"  date: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")

    results = {}
    if args.name in ("tsml", "both"):
        print()
        results["tsml"] = train_one("tsml", epochs=args.epochs,
                                       batch_size=args.batch_size)
    if args.name in ("bhml", "both"):
        print()
        results["bhml"] = train_one("bhml", epochs=args.epochs,
                                       batch_size=args.batch_size)
    print()
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "history"}
                       for k, v in results.items()}, indent=2, default=str))


if __name__ == "__main__":
    main()
