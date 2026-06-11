"""reader_v3_pretrained.py -- PRETRAIN THEN FINE-TUNE (the field's core
recipe, at miniature, on HIS books).

v1 (3 ep): val 0.722 / dev 0.620.  v2 (9 ep): val 0.772 / dev 0.601 --
more exam-prep made transfer WORSE. Proven: the reader needs general
language before exam skills. So: masked-word pretraining (BERT recipe)
on his shelved books + SQuAD passages, transfer the encoder into the
Reader, short fine-tune (3 ep, the schedule that transferred best),
re-sit the identical 1000 dev questions.

REGISTERED: dev AUROC > 0.65 = pretraining recipe confirmed at
miniature; <= 0.62 = honest negative (miniature pretrain insufficient).

  python reader_v3_pretrained.py     (background, ~25-40 min)
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
import reader_training as RT                                # noqa: E402
from squad2_selective import fetch, auroc                   # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
BOOKS = os.path.join(ROOT, "external_corpora", "books")
DEV = "cuda"
D, PL, QL = RT.D, RT.PL, RT.QL
torch.manual_seed(0)
PRE_STEPS, FT_EPOCHS = 4000, 3


def book_text(n=40, per=300_000):
    out = []
    for f in sorted(os.listdir(BOOKS))[:n]:
        raw = io.open(os.path.join(BOOKS, f), encoding="utf-8",
                      errors="ignore").read()[:per]
        out.append(raw.lower())
    return " ".join(out)


class PretrainNet(nn.Module):
    """Same names/shapes as Reader's passage stack -> transferable."""

    def __init__(self, V):
        super().__init__()
        self.emb = nn.Embedding(V, D, padding_idx=0)
        self.ppos = nn.Embedding(PL, D)
        enc = nn.TransformerEncoderLayer(D, 4, 4 * D, batch_first=True,
                                         dropout=0.1)
        self.penc = nn.TransformerEncoder(enc, 2)
        self.lm = nn.Linear(D, V)

    def forward(self, x):
        h = self.emb(x) + self.ppos(torch.arange(x.shape[1],
                                                 device=x.device))
        return self.lm(self.penc(h, src_key_padding_mask=(x == 0)))


def main():
    t0 = time.time()
    rows = RT.fetch_train()
    rng = np.random.default_rng(0)
    rows = [rows[i] for i in rng.permutation(len(rows))]

    # vocab over BOOKS + squad (shared literacy)
    c = Counter(RT.TOK.findall(book_text(25)[:8_000_000]))
    for q, ctx, _ in rows[:40000]:
        c.update(RT.TOK.findall(q.lower()))
        c.update(RT.TOK.findall(ctx.lower()[:1200]))
    itos = ["<pad>", "<unk>", "<mask>"] + \
        [w for w, _ in c.most_common(RT.VOCAB - 3)]
    stoi = {w: i for i, w in enumerate(itos)}
    MASK = 2

    # ---- pretrain corpus: book chunks + squad passages, as id rows
    text_ids = [stoi.get(w, 1) for w in RT.TOK.findall(book_text(40))]
    sq_ids = []
    for _, ctx, _ in rows[:20000:4]:
        sq_ids += [stoi.get(w, 1) for w in
                   RT.TOK.findall(ctx.lower())][:PL]
    pool = np.array(text_ids + sq_ids, dtype=np.int64)
    print(f"pretrain pool {len(pool)/1e6:.1f}M words, vocab {len(stoi)}",
          flush=True)

    pn = PretrainNet(len(stoi)).to(DEV)
    opt = torch.optim.AdamW(pn.parameters(), lr=3e-4, weight_decay=0.01)
    ce = nn.CrossEntropyLoss(ignore_index=-100)
    for step in range(PRE_STEPS):
        ix = np.random.randint(0, len(pool) - PL, size=48)
        x = torch.tensor(np.stack([pool[i:i + PL] for i in ix])).to(DEV)
        tgt = torch.full_like(x, -100)
        mask = torch.rand_like(x, dtype=torch.float) < 0.15
        tgt[mask] = x[mask]
        x = x.clone(); x[mask] = MASK
        loss = ce(pn(x).view(-1, len(stoi)), tgt.view(-1))
        opt.zero_grad(); loss.backward(); opt.step()
        if step % 500 == 0:
            print(f"  [pretrain {step}/{PRE_STEPS}] mlm loss "
                  f"{loss.item():.3f} ({(time.time()-t0)/60:.0f} min)",
                  flush=True)

    # ---- transfer into Reader
    m = RT.Reader(len(stoi)).to(DEV)
    m.emb.load_state_dict(pn.emb.state_dict())
    m.ppos.load_state_dict(pn.ppos.state_dict())
    m.penc.load_state_dict(pn.penc.state_dict())
    m.qenc.load_state_dict(pn.penc.state_dict())     # same shapes
    print("encoder transferred into Reader; fine-tuning...", flush=True)

    n_val = 4000
    val, tr = rows[:n_val], rows[n_val:]

    def tensorize(batch):
        q = torch.tensor([RT.encode(r[0], stoi, QL) for r in batch])
        p = torch.tensor([RT.encode(r[1], stoi, PL) for r in batch])
        y = torch.tensor([float(r[2]) for r in batch])
        return q.to(DEV), p.to(DEV), y.to(DEV)

    opt = torch.optim.AdamW(m.parameters(), lr=2e-4, weight_decay=0.01)
    bce = nn.BCEWithLogitsLoss()
    BS = 96
    steps_per = len(tr) // BS
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(
        opt, FT_EPOCHS * steps_per)

    @torch.no_grad()
    def val_auroc():
        m.eval(); s, ys = [], []
        for st in range(0, n_val, 256):
            q, p, y = tensorize(val[st:st + 256])
            s.append(torch.sigmoid(m(q, p)).cpu().numpy())
            ys.append(y.cpu().numpy())
        m.train()
        return auroc(np.concatenate(s), np.concatenate(ys))

    best = 0.0
    for ep in range(FT_EPOCHS):
        perm = np.random.permutation(len(tr))
        for si in range(steps_per):
            batch = [tr[i] for i in perm[si * BS:(si + 1) * BS]]
            q, p, y = tensorize(batch)
            loss = bce(m(q, p), y)
            opt.zero_grad(); loss.backward(); opt.step(); sched.step()
        a = val_auroc()
        print(f"fine-tune epoch {ep}: val AUROC {a:.3f}", flush=True)
        if a > best:
            best = a
            torch.save({"model": m.state_dict(), "stoi": stoi},
                       os.path.join(HERE, "ck_reader_v3.pt"))

    # ---- identical re-sit
    dev_rows = fetch()
    idx = np.random.default_rng(2026).permutation(len(dev_rows))[:3000]
    te = [dev_rows[i] for i in idx][2000:]
    ck = torch.load(os.path.join(HERE, "ck_reader_v3.pt"),
                    weights_only=False)
    m.load_state_dict(ck["model"]); m.eval()
    s, ys = [], []
    with torch.no_grad():
        for st in range(0, len(te), 256):
            q, p, y = tensorize(te[st:st + 256])
            s.append(torch.sigmoid(m(q, p)).cpu().numpy())
            ys.append(y.cpu().numpy())
    sc, yv = np.concatenate(s), np.concatenate(ys)
    a = auroc(sc, yv)
    print(f"\nRE-SIT v3 (same 1000 dev questions): AUROC {a:.3f} | "
          f"acc {float(np.mean((sc>0.5)==yv)):.1%}")
    print(f"  lineage: retrieval 0.602 | v1 0.620 | v2 0.601 | v3 {a:.3f}")
    o = np.argsort(-sc); base = float(1 - yv.mean())
    rc = {c_: float(1 - yv[o[:int(len(o)*c_)]].mean())
          for c_ in (0.8, 0.6, 0.4)}
    print("  risk@coverage: 100%:" + f"{base:.0%} " +
          " ".join(f"{int(c_*100)}%:{r:.0%}" for c_, r in rc.items()))
    print(f"VERDICT: {'PRETRAINING CONFIRMED at miniature (>0.65)' if a > 0.65 else ('small gain' if a > 0.62 else 'honest negative -- miniature pretrain insufficient')}; "
          f"total {(time.time()-t0)/60:.0f} min")
    json.dump(dict(dev_auroc=a, val_auroc=best, risk=rc),
              io.open(os.path.join(HERE, "squad2_v3_result.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main()
