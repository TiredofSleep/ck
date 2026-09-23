"""train_ab.py -- fair A/B: does the geometry-aware optimizer (Muon) teach faster
than AdamW, at OUR scale? Same fixed 3-layer model, same init seed, same data
order; only the optimizer differs. Registered prediction (Geometric Scribe plan):
Muon reaches a target perplexity in materially fewer steps. Kill: if Muon <= Adam,
geometry-aware optimization gives nothing here -- honest negative, keep Adam.

  python train_ab.py adam
  python train_ab.py muon
"""
import io
import json
import os
import sys

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from muon import Muon, split_params

HERE = os.path.dirname(os.path.abspath(__file__))
DATABIN = os.path.join(HERE, "corpus_tokens.bin")
LOG = os.path.join(HERE, "ab_log.jsonl")
DEV, VOCAB, D, NH, CTX = "cuda", 16384, 512, 8, 512
MICROBS, ACCUM, STEPS, EVAL, WARMUP = 24, 2, 1500, 150, 100

opt_name = sys.argv[1] if len(sys.argv) > 1 else "adam"
torch.manual_seed(7)
data = np.memmap(DATABIN, dtype=np.uint16, mode="r")
N = len(data)


def get_batch(gen):
    ix = torch.randint(0, N - CTX - 1, (MICROBS,), generator=gen)
    x = torch.stack([torch.from_numpy(data[i:i + CTX].astype(np.int64)) for i in ix])
    y = torch.stack([torch.from_numpy(data[i + 1:i + CTX + 1].astype(np.int64)) for i in ix])
    return x.to(DEV), y.to(DEV)


class Block(nn.Module):
    def __init__(self):
        super().__init__()
        self.ln1 = nn.LayerNorm(D)
        self.attn = nn.MultiheadAttention(D, NH, batch_first=True)
        self.ln2 = nn.LayerNorm(D)
        self.mlp = nn.Sequential(nn.Linear(D, 4 * D), nn.GELU(), nn.Linear(4 * D, D))
        self.register_buffer("mask", torch.triu(torch.ones(CTX, CTX) * float("-inf"), 1))

    def forward(self, x):
        h = self.ln1(x)
        a, _ = self.attn(h, h, h, attn_mask=self.mask[:x.size(1), :x.size(1)], need_weights=False)
        x = x + a
        return x + self.mlp(self.ln2(x))


class GPT(nn.Module):
    def __init__(self, layers=3):
        super().__init__()
        self.tok = nn.Embedding(VOCAB, D)
        self.pos = nn.Embedding(CTX, D)
        self.blocks = nn.ModuleList([Block() for _ in range(layers)])
        self.ln_f = nn.LayerNorm(D)
        self.lm_head = nn.Linear(D, VOCAB, bias=False)

    def forward(self, x):
        p = torch.arange(x.size(1), device=x.device)
        h = self.tok(x) + self.pos(p)[None]
        for b in self.blocks:
            h = b(h)
        return self.lm_head(self.ln_f(h))


def main():
    model = GPT().to(DEV)
    if opt_name == "adam":
        opts = [torch.optim.AdamW(model.parameters(), lr=5e-4, betas=(0.9, 0.95), weight_decay=0.1)]
        blrs = [5e-4]
    else:
        mp, ap = split_params(model)
        opts = [Muon(mp, lr=0.02, momentum=0.95),
                torch.optim.AdamW(ap, lr=5e-4, betas=(0.9, 0.95), weight_decay=0.1)]
        blrs = [0.02, 5e-4]
    print(f"[{opt_name}] params={sum(p.numel() for p in model.parameters())/1e6:.1f}M "
          f"groups={[len(o.param_groups[0]['params']) for o in opts]}", flush=True)

    val_gen = torch.Generator().manual_seed(999)
    val = [get_batch(val_gen) for _ in range(16)]
    train_gen = torch.Generator().manual_seed(123)

    def evaluate():
        model.eval(); ls = []
        with torch.no_grad():
            for x, y in val:
                with torch.autocast("cuda", dtype=torch.bfloat16):
                    loss = F.cross_entropy(model(x).view(-1, VOCAB), y.view(-1))
                ls.append(loss.item())
        model.train(); return float(np.exp(np.mean(ls)))

    for step in range(1, STEPS + 1):
        sc = min(1.0, step / WARMUP)
        for o, blr in zip(opts, blrs):
            for g in o.param_groups:
                g["lr"] = blr * sc
        for o in opts:
            o.zero_grad(set_to_none=True)
        for _ in range(ACCUM):
            x, y = get_batch(train_gen)
            with torch.autocast("cuda", dtype=torch.bfloat16):
                loss = F.cross_entropy(model(x).view(-1, VOCAB), y.view(-1)) / ACCUM
            loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        for o in opts:
            o.step()
        if step % EVAL == 0:
            ppl = evaluate()
            io.open(LOG, "a", encoding="utf-8").write(json.dumps(dict(opt=opt_name, step=step, val_ppl=round(ppl, 2))) + "\n")
            print(f"[{opt_name}] step {step} ppl {ppl:.2f}", flush=True)


if __name__ == "__main__":
    main()
