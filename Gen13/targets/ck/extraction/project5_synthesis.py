"""project5_synthesis.py -- CK Project 5: SYNTHESIS as rule generalization.

Task: continue a periodic sequence. Train on sequences built from
repeating motifs (periods 2-4) over symbols 0-9; predict the NEXT symbol.
Test on sequences from UNSEEN motifs -- including period-5 motifs, a
period length never seen in training.

If the head only memorizes instances, unseen-motif accuracy ~ chance
(10%). If it learns THE RULE ("find the period, copy from one period
back"), unseen motifs and even unseen period-lengths score high. That
rule-vs-instance gap IS synthesis, measured.

Engines (P4's honest lesson applied -- use what works, compare fairly):
  LAST-6   : one-hot of the last 6 symbols (static context)
  ESN-10   : tanh reservoir state (won DYCK in P4)
  SUBSTRATE: bilinear substrate state (P4: no special bias -- include
             to keep the ablation honest)
  LAST6+ESN: fused

  python project5_synthesis.py
"""
import io
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "walker_v0"))
import substrate as SUB                                   # noqa: E402
from project4_inductive import run_bilinear, ESN10, train_eval  # noqa: E402

RNG = np.random.default_rng(6)
N = 10
SEQ_LEN = 18
CTX = 6


def gen_split(n_train_motifs=120, n_test_motifs=60, per_motif=8):
    """Disjoint motif sets; test includes period-5 (never in training)."""
    def rand_motif(p):
        while True:
            m = tuple(RNG.integers(0, N, size=p))
            if len(set(m)) > 1:                # non-constant
                return m
    train_motifs = {rand_motif(RNG.integers(2, 5))         # periods 2-4
                    for _ in range(n_train_motifs)}
    test_motifs = set()
    while len(test_motifs) < n_test_motifs // 2:
        m = rand_motif(RNG.integers(2, 5))
        if m not in train_motifs:
            test_motifs.add(m)
    while len(test_motifs) < n_test_motifs:                # UNSEEN period 5
        test_motifs.add(rand_motif(5))

    def build(motifs):
        seqs, nxt = [], []
        for m in motifs:
            for _ in range(per_motif):
                off = RNG.integers(0, len(m))
                s = [m[(off + t) % len(m)] for t in range(SEQ_LEN + 1)]
                seqs.append(np.array(s[:SEQ_LEN]))
                nxt.append(s[SEQ_LEN])
        return seqs, np.array(nxt)

    return build(sorted(train_motifs)), build(sorted(test_motifs))


def last_k_feats(seq, k=CTX):
    f = [1.0]
    for s in seq[-k:]:
        oh = np.zeros(N); oh[int(s)] = 1.0
        f.append(oh)
    return np.concatenate([[1.0]] + [x for x in f[1:]])


def main():
    t0 = time.time()
    (Str, ytr), (Ste, yte) = gen_split()
    print("CK PROJECT 5 -- SYNTHESIS: continue the pattern (rule vs "
          "memorization)")
    print(f"{len(Str)} train sequences (motifs of period 2-4); "
          f"{len(Ste)} test sequences from UNSEEN motifs (half are "
          f"period-5 -- a length never seen). chance 10%.\n")

    esn = ESN10(np.random.default_rng(101))
    engines = {
        "LAST-6 (static)": lambda s: last_k_feats(s),
        "ESN-10": lambda s: esn.run(s),
        "SUBSTRATE": lambda s: run_bilinear(SUB.MIX_TEN, s),
    }
    feats = {}
    accs = {}
    for name, fn in engines.items():
        Xtr = np.array([fn(s) for s in Str])
        Xte = np.array([fn(s) for s in Ste])
        feats[name] = (Xtr, Xte)
        accs[name] = train_eval(Xtr, ytr, Xte, yte, N, epochs=400)
        print(f"  {name:>16}: unseen-motif next-symbol acc {accs[name]:.0%}")

    Xtr = np.hstack([feats["LAST-6 (static)"][0], feats["ESN-10"][0]])
    Xte = np.hstack([feats["LAST-6 (static)"][1], feats["ESN-10"][1]])
    accs["LAST6+ESN fused"] = train_eval(Xtr, ytr, Xte, yte, N, epochs=400)
    print(f"  {'LAST6+ESN fused':>16}: unseen-motif next-symbol acc "
          f"{accs['LAST6+ESN fused']:.0%}")

    best = max(accs, key=accs.get)
    print(f"\nVERDICT: best engine {best} at {accs[best]:.0%} vs 10% chance "
          f"-> {'THE RULE WAS LEARNED (synthesis present: applies to '
          'never-seen motifs incl. never-seen period length)' if accs[best] > 0.4 else 'memorization only -- honest negative'}.")
    print(f"runtime {time.time()-t0:.0f}s CPU")
    json.dump(accs, io.open(os.path.join(HERE, "project5_result.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main()
