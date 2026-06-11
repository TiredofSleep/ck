"""her_training.py -- THE GPU SPINS, HER CONFIGURES, CK LEARNS.

Hindsight Experience Replay (his own organ -- ck_hindsight_replay.py,
Gen11 brain, replay_impact 0.976 in the bdc logs) wired into native LM
training: sequences the model MISSES (top-quartile loss) enter a
priority buffer; every batch mixes fresh text with replayed misses.
The brain's trick: practice hardest what you got wrong.

REGISTERED: HER vs uniform-sampling control, same data/steps/seed.
replay_impact = bpc(control) - bpc(HER). Positive = HER earns the seat
in the training loop; ~zero/negative = honest negative, recorded.

Corpus: his life-text + curricula + tonight's study journal + a books
slice (the expanding life).

  python her_training.py
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
sys.path.insert(0, os.path.join(HERE, "..", "extraction"))
import train_native_lm as TNL                              # noqa: E402

DEV = "cuda"
torch.manual_seed(0)
STEPS, CTX, BATCH = 1500, 192, 64
REPLAY_FRAC, BUF_CAP = 0.25, 4096


def corpus():
    text = TNL.get_corpus()
    jp = os.path.join(HERE, "study_journal.jsonl")
    if os.path.exists(jp):
        J = " ".join(json.loads(l)["journal"]
                     for l in io.open(jp, encoding="utf-8"))
        text += ("\n" + J.lower()) * 4
    bdir = os.path.join(HERE, "..", "..", "..", "..", "external_corpora",
                        "books")
    for f in sorted(os.listdir(bdir))[:4]:
        text += io.open(os.path.join(bdir, f), encoding="utf-8",
                        errors="ignore").read()[:500_000].lower()
    return text


def train(tdata, vdata, vocab, use_her):
    torch.manual_seed(0)
    m = TNL.MiniGPT(vocab, 256, 4, 4).to(DEV)        # S3-class, 3.3M
    opt = torch.optim.AdamW(m.parameters(), lr=3e-4, weight_decay=0.01)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, STEPS)
    buf_x, buf_y, buf_loss = [], [], []
    t0 = time.time()
    tag = "HER" if use_her else "CTL"
    for step in range(STEPS):
        n_replay = int(BATCH * REPLAY_FRAC) if use_her and len(buf_x) >= 64 \
            else 0
        n_fresh = BATCH - n_replay
        ix = torch.randint(len(tdata) - CTX - 1, (n_fresh,))
        x = torch.stack([tdata[i:i + CTX] for i in ix]).to(DEV)
        y = torch.stack([tdata[i + 1:i + CTX + 1] for i in ix]).to(DEV)
        if n_replay:
            pr = torch.tensor(buf_loss); pr = (pr / pr.sum())
            ri = torch.multinomial(pr, n_replay, replacement=True)
            x = torch.cat([x, torch.stack([buf_x[i] for i in ri]).to(DEV)])
            y = torch.cat([y, torch.stack([buf_y[i] for i in ri]).to(DEV)])
        logits = m(x)
        per_seq = Fn.cross_entropy(
            logits.view(-1, vocab), y.reshape(-1),
            reduction="none").view(len(x), -1).mean(1)
        loss = per_seq.mean()
        opt.zero_grad(); loss.backward(); opt.step(); sched.step()
        if use_her:                       # misses -> buffer (the HER write)
            thresh = per_seq[:n_fresh].quantile(0.75)
            for k in range(n_fresh):
                if per_seq[k] > thresh:
                    buf_x.append(x[k].cpu()); buf_y.append(y[k].cpu())
                    buf_loss.append(float(per_seq[k]))
            if len(buf_x) > BUF_CAP:
                buf_x, buf_y, buf_loss = (buf_x[-BUF_CAP:],
                                          buf_y[-BUF_CAP:],
                                          buf_loss[-BUF_CAP:])
        if step % 300 == 0 or step == STEPS - 1:
            miss = float((per_seq[:n_fresh] > per_seq[:n_fresh]
                          .quantile(0.75)).float().mean())
            print(f"  [{tag} {step:>4}] loss {loss.item():.3f} | "
                  f"buffer {len(buf_x):>4} | miss_rate {miss:.2f} | "
                  f"replayed {n_replay}/batch | "
                  f"{(step+1)/(time.time()-t0):.1f} steps/s", flush=True)
    bpc = TNL.val_bpc(m, vdata)
    return bpc


def main():
    text = corpus()
    tdata, vdata, stoi = TNL.encode_setup(text)
    print(f"CK LEARNING SESSION -- corpus {len(text)/1e6:.1f}M chars "
          f"(life + journal + books), vocab {len(stoi)}, "
          f"S3-class LM, {STEPS} steps x2 on "
          f"{torch.cuda.get_device_name(0)}\n")
    print("control (uniform sampling):")
    bpc_ctl = train(tdata, vdata, len(stoi), use_her=False)
    print(f"  -> control val: {bpc_ctl:.3f} bits/char\n")
    print("HER (miss-priority replay, his own organ):")
    bpc_her = train(tdata, vdata, len(stoi), use_her=True)
    print(f"  -> HER val: {bpc_her:.3f} bits/char\n")
    impact = bpc_ctl - bpc_her
    print(f"REPLAY_IMPACT = {impact:+.4f} bits/char -> "
          f"{'HER EARNS THE TRAINING-LOOP SEAT' if impact > 0.005 else ('tie -- seat undecided at this scale' if impact > -0.005 else 'honest negative at this scale')}")
    json.dump(dict(control_bpc=bpc_ctl, her_bpc=bpc_her,
                   replay_impact=impact),
              io.open(os.path.join(HERE, "her_training_result.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main()
