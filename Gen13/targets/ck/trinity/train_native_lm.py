"""train_native_lm.py -- THE BIG THING: CK's own native language model,
trained from scratch on his life-corpus, at FOUR sizes -- his own
measured SCALING CURVE (the frontier's central instrument, Kaplan/
Chinchilla, run on his own existence).

Char-level mini-GPT (causal transformer), identical data and steps per
size; held-out split never trained on. Deliverables:
  (1) CK's scaling curve: val bits-per-char vs parameter count
  (2) meaning organ v3 candidate: mean-pooled hidden states -> routing
      eval. REGISTERED: >=70% upgrades the seat; below 65% and PPMI-SVD
      keeps it (abilities earn places).

  python train_native_lm.py        (RTX 4070, ~minutes per size)
"""
import io
import json
import math
import os
import sys
import time

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as Fn

HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.join(HERE, "..", "extraction")
sys.path.insert(0, EXT)
import organ_meaning_native as OMN                         # noqa: E402

DEV = "cuda" if torch.cuda.is_available() else "cpu"
CTX, BATCH, STEPS, LR = 192, 64, 3000, 3e-4
torch.manual_seed(0)

SIZES = {                       # name: (d_model, layers, heads)
    "S1-100K": (64, 2, 2),
    "S2-430K": (128, 3, 4),
    "S3-1.7M": (256, 4, 4),
    "S4-6.5M": (384, 6, 6),
}


class Block(nn.Module):
    def __init__(self, d, h):
        super().__init__()
        self.ln1 = nn.LayerNorm(d)
        self.att = nn.MultiheadAttention(d, h, batch_first=True)
        self.ln2 = nn.LayerNorm(d)
        self.mlp = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(),
                                 nn.Linear(4 * d, d))

    def forward(self, x, mask):
        a, _ = self.att(self.ln1(x), self.ln1(x), self.ln1(x),
                        attn_mask=mask, need_weights=False)
        x = x + a
        return x + self.mlp(self.ln2(x))


class MiniGPT(nn.Module):
    def __init__(self, vocab, d, layers, heads):
        super().__init__()
        self.tok = nn.Embedding(vocab, d)
        self.pos = nn.Embedding(CTX, d)
        self.blocks = nn.ModuleList(Block(d, heads) for _ in range(layers))
        self.lnf = nn.LayerNorm(d)
        self.head = nn.Linear(d, vocab, bias=False)
        mask = torch.triu(torch.full((CTX, CTX), float("-inf")), 1)
        self.register_buffer("mask", mask)

    def hidden(self, ix):
        T = ix.shape[1]
        x = self.tok(ix) + self.pos(torch.arange(T, device=ix.device))
        for b in self.blocks:
            x = b(x, self.mask[:T, :T])
        return self.lnf(x)

    def forward(self, ix):
        return self.head(self.hidden(ix))


def get_corpus():
    text = OMN.gather_corpus()
    for fn in ("synthetic_curriculum.json", "synthetic_curriculum_big.json"):
        p = os.path.join(HERE, fn)
        if os.path.exists(p):
            cur = json.load(io.open(p, encoding="utf-8"))
            synth = "\n".join(t for ts in cur.values() for t in ts).lower()
            text += ("\n" + synth) * 6
    return text


def encode_setup(text):
    chars = sorted(set(text))
    if len(chars) > 200:                      # clip exotic chars
        from collections import Counter
        keep = set(c for c, _ in Counter(text).most_common(160))
        text = "".join(c for c in text if c in keep)
        chars = sorted(set(text))
    stoi = {c: i for i, c in enumerate(chars)}
    data = torch.tensor([stoi[c] for c in text], dtype=torch.long)
    n_val = len(data) // 20
    return data[:-n_val], data[-n_val:], stoi


def batch(data):
    ix = torch.randint(len(data) - CTX - 1, (BATCH,))
    x = torch.stack([data[i:i + CTX] for i in ix]).to(DEV)
    y = torch.stack([data[i + 1:i + CTX + 1] for i in ix]).to(DEV)
    return x, y


@torch.no_grad()
def val_bpc(model, vdata, iters=40):
    model.eval()
    losses = []
    for _ in range(iters):
        x, y = batch(vdata)
        loss = Fn.cross_entropy(model(x).view(-1, model.head.out_features),
                                y.reshape(-1))
        losses.append(loss.item())
    model.train()
    return float(np.mean(losses) / math.log(2))


def train_one(name, dims, tdata, vdata, vocab):
    d, L, h = dims
    m = MiniGPT(vocab, d, L, h).to(DEV)
    n_par = sum(p.numel() for p in m.parameters())
    opt = torch.optim.AdamW(m.parameters(), lr=LR, weight_decay=0.01)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, STEPS)
    t0 = time.time()
    for step in range(STEPS):
        x, y = batch(tdata)
        loss = Fn.cross_entropy(m(x).view(-1, vocab), y.reshape(-1))
        opt.zero_grad(); loss.backward(); opt.step(); sched.step()
    bpc = val_bpc(m, vdata)
    print(f"  {name}: {n_par:,} params | val {bpc:.3f} bits/char | "
          f"{time.time()-t0:.0f}s")
    return m, n_par, bpc


def sent_embed(model, stoi, texts):
    vecs = []
    with torch.no_grad():
        for t in texts:
            ix = torch.tensor([[stoi[c] for c in t.lower()[:CTX]
                                if c in stoi]], dtype=torch.long).to(DEV)
            if ix.shape[1] < 2:
                ix = torch.zeros((1, 2), dtype=torch.long, device=DEV)
            vecs.append(model.hidden(ix)[0].mean(0).cpu().numpy())
    return np.array(vecs)


def routing_eval(model, stoi):
    from demo_facts_head import TOPICS, ANCHORS
    from project2_routing import char_trigrams, train_head, zs, TOPIC_LIST
    import braid_memory as bm
    grown = json.load(io.open(os.path.join(EXT, "teacher_corpus.json"),
                              encoding="utf-8"))
    ref_x, ref_y, test_x, test_y = [], [], [], []
    for t in TOPIC_LIST:
        g = list(grown.get(t, []))
        ref_x += TOPICS[t][:4] + list(ANCHORS[t]) + g
        ref_y += [t] * (4 + len(ANCHORS[t]) + len(g))
        test_x += TOPICS[t][4:]; test_y += [t] * 2
    y_ref = np.array([TOPIC_LIST.index(t) for t in ref_y])
    y_te = np.array([TOPIC_LIST.index(t) for t in test_y])
    M_ref, M_te = sent_embed(model, stoi, ref_x), sent_embed(model, stoi,
                                                             test_x)
    Xb = lambda xs: np.array([bm.braid_signature_rich(x) for x in xs])
    Xc_ref, vocab = char_trigrams(ref_x)
    Xc_te, _ = char_trigrams(test_x, vocab)
    out_r, out_t = [], []
    for A_, B_ in [(M_ref, M_te), (Xb(ref_x), Xb(test_x)),
                   (Xc_ref, Xc_te)]:
        Az, m_, s_ = zs(A_)
        out_r.append(Az); out_t.append((B_ - m_) / s_)
    Fr, Ft = np.hstack(out_r), np.hstack(out_t)
    Wh, bh = train_head(Fr, y_ref)
    return float(np.mean((Ft @ Wh + bh).argmax(1) == y_te))


def main():
    print(f"CK NATIVE LM -- scaling ladder on {DEV.upper()} "
          f"({torch.cuda.get_device_name(0) if DEV=='cuda' else 'cpu'})")
    text = get_corpus()
    tdata, vdata, stoi = encode_setup(text)
    print(f"corpus {len(text)/1e6:.1f}M chars, vocab {len(stoi)}, "
          f"train {len(tdata)/1e6:.1f}M / val {len(vdata)/1e6:.2f}M chars; "
          f"{STEPS} steps x batch {BATCH} x ctx {CTX} each\n")
    curve, models = {}, {}
    for name, dims in SIZES.items():
        m, n_par, bpc = train_one(name, dims, tdata, vdata, len(stoi))
        curve[name] = dict(params=n_par, val_bpc=bpc)
        models[name] = m
    print("\nCK'S SCALING CURVE (val bits/char vs params):")
    for name, r in curve.items():
        bar = "#" * int((4.0 - r["val_bpc"]) * 12)
        print(f"  {r['params']:>9,}: {r['val_bpc']:.3f}  {bar}")

    best = min(curve, key=lambda k: curve[k]["val_bpc"])
    print(f"\nbest LM: {best} -- evaluating as meaning organ v3 "
          f"(mean-pooled hidden states)...")
    acc = routing_eval(models[best], stoi)
    print(f"ROUTING with native-LM embeddings: {acc:.0%} "
          f"(PPMI-SVD v2: 65% | borrowed: 80%)")
    print(f"VERDICT: {'ORGAN UPGRADED' if acc >= 0.70 else ('matches seat-holder' if acc >= 0.65 else 'PPMI-SVD keeps the seat')}")
    curve["routing_v3"] = acc
    json.dump(curve, io.open(os.path.join(HERE, "native_lm_result.json"),
                             "w"), indent=1)
    torch.save({"model": models[best].state_dict(), "stoi": stoi,
                "dims": SIZES[best]},
               os.path.join(HERE, "ck_native_lm.pt"))
    print("saved ck_native_lm.pt")


if __name__ == "__main__":
    main()
