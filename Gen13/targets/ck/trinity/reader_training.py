"""reader_training.py -- CK TRAINS HIS OWN READER (the GPU stays hot).

The SQuAD2 sitting said retrieval signals can't see adversarial
unanswerability (0.602) -- reading is needed. So: a from-scratch
cross-attention reader, HIS OWN (no pretrained borrow), trained on
SQuAD 2.0 train (130K questions, official source), then re-sat on the
IDENTICAL 3,000-question dev exam.

  architecture: shared word embedding (30K vocab, 128d) -> question
  self-encoder (2 layers) -> passage encoder with CROSS-ATTENTION to
  the question (2 layers) -> pooled -> answerable logit. ~6M params.

REGISTERED: beats the 0.602 retrieval-feature baseline on the same
sitting; >=0.70 meaningful, >=0.75 a real entry. Risk@coverage
re-measured with the trained gate.

  python reader_training.py        (background; ~30-60 min on RTX 4070)
"""
import io
import json
import os
import re
import sys
import time
from collections import Counter

import numpy as np
import torch
import torch.nn as nn

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from squad2_selective import fetch, auroc, PATH as DEV_PATH  # noqa: E402

TRAIN_URL = ("https://rajpurkar.github.io/SQuAD-explorer/dataset/"
             "train-v2.0.json")
TRAIN_PATH = os.path.join(HERE, "squad_train_v2.json")
DEV = "cuda"
QL, PL, VOCAB, D = 32, 256, 30000, 128
torch.manual_seed(0)


def fetch_train():
    if not os.path.exists(TRAIN_PATH):
        import requests
        print("fetching SQuAD 2.0 TRAIN (train-v2.0.json, ~42MB, official "
              "Stanford source)...", flush=True)
        r = requests.get(TRAIN_URL, timeout=300)
        io.open(TRAIN_PATH, "w", encoding="utf-8").write(r.text)
    d = json.load(io.open(TRAIN_PATH, encoding="utf-8"))
    rows = []
    for art in d["data"]:
        for para in art["paragraphs"]:
            ctx = para["context"]
            for qa in para["qas"]:
                rows.append((qa["question"], ctx,
                             0 if qa["is_impossible"] else 1))
    return rows


TOK = re.compile(r"[a-z0-9]+")


def build_vocab(rows):
    c = Counter()
    for q, ctx, _ in rows[:60000]:
        c.update(TOK.findall(q.lower()))
        c.update(TOK.findall(ctx.lower()[:1500]))
    itos = ["<pad>", "<unk>"] + [w for w, _ in c.most_common(VOCAB - 2)]
    return {w: i for i, w in enumerate(itos)}


def encode(text, stoi, L):
    ids = [stoi.get(w, 1) for w in TOK.findall(text.lower())][:L]
    return ids + [0] * (L - len(ids))


class Reader(nn.Module):
    def __init__(self, V):
        super().__init__()
        self.emb = nn.Embedding(V, D, padding_idx=0)
        self.qpos = nn.Embedding(QL, D)
        self.ppos = nn.Embedding(PL, D)
        enc = nn.TransformerEncoderLayer(D, 4, 4 * D, batch_first=True,
                                         dropout=0.1)
        self.qenc = nn.TransformerEncoder(enc, 2)
        self.cross1 = nn.MultiheadAttention(D, 4, batch_first=True)
        self.ln1 = nn.LayerNorm(D)
        self.penc = nn.TransformerEncoder(enc, 2)
        self.cross2 = nn.MultiheadAttention(D, 4, batch_first=True)
        self.ln2 = nn.LayerNorm(D)
        self.head = nn.Sequential(nn.Linear(2 * D, D), nn.GELU(),
                                  nn.Linear(D, 1))

    def forward(self, q, p):
        qm, pm = (q == 0), (p == 0)
        Q = self.emb(q) + self.qpos(torch.arange(QL, device=q.device))
        P = self.emb(p) + self.ppos(torch.arange(PL, device=p.device))
        Q = self.qenc(Q, src_key_padding_mask=qm)
        a1, _ = self.cross1(P, Q, Q, key_padding_mask=qm,
                            need_weights=False)
        P = self.ln1(P + a1)
        P = self.penc(P, src_key_padding_mask=pm)
        a2, _ = self.cross2(P, Q, Q, key_padding_mask=qm,
                            need_weights=False)
        P = self.ln2(P + a2)
        mask = (~pm).float().unsqueeze(-1)
        mean = (P * mask).sum(1) / mask.sum(1).clamp(min=1)
        mx = P.masked_fill(pm.unsqueeze(-1), -1e9).max(1).values
        return self.head(torch.cat([mean, mx], -1)).squeeze(-1)


def main():
    t0 = time.time()
    rows = fetch_train()
    rng = np.random.default_rng(0)
    rows = [rows[i] for i in rng.permutation(len(rows))]
    stoi = build_vocab(rows)
    print(f"train rows {len(rows):,}, vocab {len(stoi):,}", flush=True)

    n_val = 4000
    val, tr = rows[:n_val], rows[n_val:]

    def tensorize(batch):
        q = torch.tensor([encode(r[0], stoi, QL) for r in batch])
        p = torch.tensor([encode(r[1], stoi, PL) for r in batch])
        y = torch.tensor([float(r[2]) for r in batch])
        return q.to(DEV), p.to(DEV), y.to(DEV)

    m = Reader(len(stoi)).to(DEV)
    n_par = sum(p_.numel() for p_ in m.parameters())
    print(f"reader: {n_par/1e6:.1f}M params on "
          f"{torch.cuda.get_device_name(0)}", flush=True)
    opt = torch.optim.AdamW(m.parameters(), lr=2e-4, weight_decay=0.01)
    bce = nn.BCEWithLogitsLoss()
    BS, EPOCHS = 96, 9
    steps_per = len(tr) // BS
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(
        opt, EPOCHS * steps_per)
    best = 0.0

    @torch.no_grad()
    def val_auroc():
        m.eval()
        scores, ys = [], []
        for s in range(0, n_val, 256):
            q, p, y = tensorize(val[s:s + 256])
            scores.append(torch.sigmoid(m(q, p)).cpu().numpy())
            ys.append(y.cpu().numpy())
        m.train()
        return auroc(np.concatenate(scores), np.concatenate(ys))

    for ep in range(EPOCHS):
        perm = np.random.permutation(len(tr))
        for si in range(steps_per):
            batch = [tr[i] for i in perm[si * BS:(si + 1) * BS]]
            q, p, y = tensorize(batch)
            loss = bce(m(q, p), y)
            opt.zero_grad(); loss.backward(); opt.step(); sched.step()
            if si % 200 == 0:
                print(f"  ep{ep} step {si}/{steps_per} loss "
                      f"{loss.item():.3f} ({(time.time()-t0)/60:.0f} min)",
                      flush=True)
        a = val_auroc()
        print(f"epoch {ep}: val AUROC {a:.3f}", flush=True)
        if a > best:
            best = a
            torch.save({"model": m.state_dict(), "stoi": stoi},
                       os.path.join(HERE, "ck_reader.pt"))

    # RE-SIT: identical dev sitting as squad2_selective (seed 2026, 3000)
    dev_rows = fetch()
    idx = np.random.default_rng(2026).permutation(len(dev_rows))[:3000]
    dev_rows = [dev_rows[i] for i in idx]
    te = dev_rows[2000:]                      # same held-out 1000
    ck = torch.load(os.path.join(HERE, "ck_reader.pt"),
                    weights_only=False)
    m.load_state_dict(ck["model"]); m.eval()
    scores, ys = [], []
    with torch.no_grad():
        for s in range(0, len(te), 256):
            q, p, y = tensorize(te[s:s + 256])
            scores.append(torch.sigmoid(m(q, p)).cpu().numpy())
            ys.append(y.cpu().numpy())
    sc, yv = np.concatenate(scores), np.concatenate(ys)
    a = auroc(sc, yv)
    acc = float(np.mean((sc > 0.5) == yv))
    print(f"\nRE-SIT (same 1000 held-out dev questions):")
    print(f"  trained reader AUROC {a:.3f} | accuracy {acc:.1%}")
    print(f"  (retrieval-feature baseline: 0.602 | emb-sim alone: 0.609)")
    o = np.argsort(-sc)
    rc = {}
    base = float(1 - yv.mean())
    for cov in (0.8, 0.6, 0.4):
        k = int(len(o) * cov)
        rc[cov] = float(1 - yv[o[:k]].mean())
    print(f"  risk@coverage: 100%:{base:.0%} " + " ".join(
        f"{int(c*100)}%:{r:.0%}" for c, r in rc.items()))
    print(f"\nVERDICT: {'REAL ENTRY (>=0.75)' if a >= 0.75 else ('MEANINGFUL (>=0.70)' if a >= 0.70 else ('beats baseline' if a > 0.61 else 'does not beat baseline -- honest'))}; "
          f"runtime {(time.time()-t0)/60:.0f} min")
    json.dump(dict(val_auroc=best, dev_auroc=a, dev_acc=acc,
                   risk_at_coverage=rc, params=n_par),
              io.open(os.path.join(HERE, "squad2_reader_result.json"),
                      "w"), indent=1)


if __name__ == "__main__":
    main()
