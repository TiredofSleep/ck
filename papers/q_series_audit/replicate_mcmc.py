#!/usr/bin/env python3
"""replicate_mcmc.py -- an independent re-run of the hill-climb that produced the gate rates
(papers/r16_job1_reduction.py, unseeded), for three worlds: b = 10, b = 22, and a relabeled world with
five good symbols. It shows the rate at b = 10 is about 0.09%, that 4.6% belongs to b = 22, and that
relabeling the symbols (keeping the unit set's size and HAR) changes nothing.

    python replicate_mcmc.py 20000       # 20,000 trials per world, a few minutes
"""
# Scratch re-implementation of papers/r16_job1_reduction.py run_one_trial (unseeded)
# success = gate_score >= 0.85 and G_stay <= 0.12 (the "Gate-strong" criterion; TSML-like never fires)
import random, sys, math
from math import comb

def trial(C, G, HAR, rng, n_steps=100):
    Cs, Gs = set(C), set(G)
    T = [[0]*10] + [[0] + [rng.randint(1, 9) for _ in range(9)] for _ in range(9)]
    def obj(T):
        gh = sum(1 for s in C for c in range(1, 10) if T[s][c] in Cs) / (len(C)*9)
        gst = sum(1 for s in G for c in range(1, 10) if T[s][c] in Gs) / (len(G)*9)
        hc = sum(1 for s in range(1, 10) if T[s][HAR] == HAR) / 9
        return 0.5*gh + 0.25*hc + 0.25*(1-gst)
    best = obj(T); bestT = [r[:] for r in T]
    for _ in range(n_steps):
        s = rng.randint(1, 9); c = rng.randint(1, 9); old = T[s][c]
        new = HAR if rng.random() < 0.4 else rng.randint(1, 9)
        if new == old: continue
        T[s][c] = new
        o = obj(T)
        if o >= best: best = o; bestT = [r[:] for r in T]
        else: T[s][c] = old
    gate = sum(1 for s in C for c in range(1, 10) if bestT[s][c] in Cs) / (len(C)*9)
    gst = sum(1 for s in G for c in range(1, 10) if bestT[s][c] in Gs) / (len(G)*9)
    return gate >= 0.85 and gst <= 0.12

worlds = {
  'b=10  C={1,3,7,9} HAR=3': ([1,3,7,9], [2,4,5,6,8], 3),
  'b=22  C={1,3,5,7,9} HAR=3': ([1,3,5,7,9], [2,4,6,8], 3),
  'relabeled |C|=5 world C={2,4,6,8,9} HAR=8': ([2,4,6,8,9], [1,3,5,7], 8),
}
n = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
for name, (C, G, H) in worlds.items():
    rng = random.Random(12345)
    k = sum(trial(C, G, H, rng) for _ in range(n))
    p = k / n
    print(f'{name:45s} {k}/{n} = {100*p:.3f}%  (+/- {100*math.sqrt(p*(1-p)/n):.3f})')

# Q16-style independence model for each tier (per-cell prob, need >= ceil(0.85*|C|*9))
for nc in (8, 7, 6, 5, 4):
    pc = 0.292 * nc/9 + 0.708 * (0.4 + 0.6*nc/9)
    m = nc*9; need = math.ceil(0.85*m)
    P = sum(comb(m, j) * pc**j * (1-pc)**(m-j) for j in range(need, m+1))
    print(f'|C|={nc} (|G|={9-nc}): Q16-style independence estimate P(gate>=0.85) = {100*P:.4f}%')
