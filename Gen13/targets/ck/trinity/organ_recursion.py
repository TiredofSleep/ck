"""organ_recursion.py -- TRINITY organ 3: RECURSION (the TRM lesson).

Task: PARITY-20 at N=1000 -- the bench where EVERY one-shot engine in
Project 4 sat at chance (bag 49%, ESN features 49%, substrate 53%,
random tables 48%). The classic 'needs computation, not features' task.

Engines (~matched parameter budgets, torch CPU, same data):
  ONE-SHOT MLP   : x -> h -> h -> 2. The no-recursion control.
  TRM-REFINER    : tiny weight-shared step  z <- tanh(W[x;z;y]),
                   y <- Vz, K=12 refinement steps on the STATIC input,
                   DEEP SUPERVISION (loss at every step) -- the two
                   ingredients HRM/TRM research says are the real drivers.
  REFINER-NO-DS  : same, loss on final step only (ablation).
  GRU-SEQ        : tiny GRU reading the sequence (the field's native
                   recurrent tool -- the toolbox's sequence specialist).

REGISTERED: refiner+DS cracks parity (>90%) where one-shot fails; no-DS
unstable/worse; GRU solves it natively. If refiner fails after one
honest retune -> dead end recorded.

  python organ_recursion.py
"""
import io
import json
import os
import time

import numpy as np
import torch
import torch.nn as nn

torch.manual_seed(0)
HERE = os.path.dirname(os.path.abspath(__file__))
RNG = np.random.default_rng(9)
L, NTR, NTE = 20, 1000, 500


def data():
    X = RNG.choice([-1.0, 1.0], size=(NTR + NTE, L)).astype(np.float32)
    y = ((X > 0).sum(1) % 2).astype(np.int64)
    return (torch.tensor(X[:NTR]), torch.tensor(y[:NTR]),
            torch.tensor(X[NTR:]), torch.tensor(y[NTR:]))


class OneShot(nn.Module):
    def __init__(self, h=64):
        super().__init__()
        self.f = nn.Sequential(nn.Linear(L, h), nn.Tanh(),
                               nn.Linear(h, h), nn.Tanh(), nn.Linear(h, 2))

    def forward(self, x):
        return [self.f(x)]


class Refiner(nn.Module):
    def __init__(self, hz=48, K=12):
        super().__init__()
        self.K = K
        self.step = nn.Linear(L + hz + 2, hz)
        self.out = nn.Linear(hz, 2)

    def forward(self, x):
        B = x.shape[0]
        z = torch.zeros(B, self.step.out_features)
        y = torch.zeros(B, 2)
        ys = []
        for _ in range(self.K):
            z = torch.tanh(self.step(torch.cat([x, z, y], 1)))
            y = self.out(z)
            ys.append(y)
        return ys


class GRUSeq(nn.Module):
    def __init__(self, h=24):
        super().__init__()
        self.g = nn.GRU(1, h, batch_first=True)
        self.out = nn.Linear(h, 2)

    def forward(self, x):
        o, _ = self.g(x.unsqueeze(-1))
        return [self.out(o[:, -1])]


def train(model, Xtr, ytr, Xte, yte, deep=True, epochs=1500, lr=2e-3):
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    ce = nn.CrossEntropyLoss()
    for ep in range(epochs):
        opt.zero_grad()
        ys = model(Xtr)
        loss = (sum(ce(y, ytr) for y in ys) / len(ys)) if deep \
            else ce(ys[-1], ytr)
        loss.backward()
        opt.step()
    with torch.no_grad():
        acc = float((model(Xte)[-1].argmax(1) == yte).float().mean())
        tr = float((model(Xtr)[-1].argmax(1) == ytr).float().mean())
    return tr, acc


def nparams(m):
    return sum(p.numel() for p in m.parameters())


def main():
    t0 = time.time()
    Xtr, ytr, Xte, yte = data()
    print(f"TRINITY ORGAN 3 -- RECURSION: PARITY-{L}, {NTR} train / "
          f"{NTE} test (P4 one-shot engines: ~50%)\n")
    runs = {
        "ONE-SHOT MLP": (OneShot(), True),
        "TRM-REFINER (K=12, deep sup)": (Refiner(), True),
        "REFINER no deep-sup": (Refiner(), False),
        "GRU-SEQ (field's tool)": (GRUSeq(), True),
    }
    results = {}
    for name, (m, deep) in runs.items():
        tr, te = train(m, Xtr, ytr, Xte, yte, deep=deep)
        results[name] = dict(train=tr, test=te, params=nparams(m))
        print(f"{name:>30}: train {tr:4.0%}  TEST {te:4.0%}  "
              f"({nparams(m):,} params)")

    ref = results["TRM-REFINER (K=12, deep sup)"]["test"]
    one = results["ONE-SHOT MLP"]["test"]
    print(f"\nVERDICT: recursion+deep-supervision "
          f"{'CRACKS parity' if ref > 0.9 else ('beats one-shot' if ref > one + 0.05 else 'FAILS (dead end recorded)')} "
          f"({ref:.0%} vs one-shot {one:.0%}).")
    print(f"runtime {time.time()-t0:.0f}s CPU")
    json.dump(results, io.open(os.path.join(HERE,
              "organ_recursion_result.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
