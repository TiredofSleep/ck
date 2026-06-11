"""organ_induction.py -- opening the parity dead end with DISCRETE
automaton induction (the gap-router's Type-II diagnosis made concrete).

Parity-20 @ N=1000 defeated every gradient engine (one-shot 53%,
TRM-refiner 53%, GRU 49% -- all memorizing). Diagnosis: Type-II, a
MISSING INVARIANT -- the hypothesis class was wrong, not the data size.
Parity is a 2-state automaton; the right class is DISCRETE state
machines.

Method: Occam enumeration (the simplest honest automaton induction --
scalable versions are RPNI state-merging and spectral WFA learning):
enumerate ALL DFAs with k <= 3 states over the binary alphabet, pick
minimal training error, evaluate ONCE on test.

REGISTERED: some 2-state DFA hits ~0% train error and ~100% test --
from the SAME 1000 examples where neural engines sat at chance.

  python organ_induction.py
"""
import io
import itertools
import json
import os
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RNG = np.random.default_rng(9)             # SAME data as organ_recursion
L, NTR, NTE = 20, 1000, 500


def data():
    X = RNG.choice([-1.0, 1.0], size=(NTR + NTE, L))
    y = ((X > 0).sum(1) % 2).astype(int)
    bits = (X > 0).astype(int)
    return bits[:NTR], y[:NTR], bits[NTR:], y[NTR:]


def run_dfa(delta, start, bits):
    """delta: (2, k) int array; vectorized over all strings."""
    s = np.full(len(bits), start, dtype=int)
    for t in range(bits.shape[1]):
        s = delta[bits[:, t], s]
    return s


def main():
    t0 = time.time()
    btr, ytr, bte, yte = data()
    print("TRINITY -- automaton induction at the parity dead end")
    print(f"same {NTR} train / {NTE} test as organ_recursion "
          f"(gradient engines: 49-53%)\n")

    best = (1.0, None)                      # (train error, model)
    n_checked = 0
    for k in (2, 3):
        for flat in itertools.product(range(k), repeat=2 * k):
            delta = np.array(flat).reshape(2, k)
            for start in range(k):
                sf = run_dfa(delta, start, btr)
                for mask in itertools.product((0, 1), repeat=k):
                    acc = np.array(mask)
                    err = float(np.mean(acc[sf] != ytr))
                    n_checked += 1
                    if err < best[0]:
                        best = (err, (k, delta.copy(), start, acc.copy()))
            if best[0] == 0.0:
                break
        if best[0] == 0.0:
            break

    err, (k, delta, start, acc) = best
    sf_te = run_dfa(delta, start, bte)
    test_acc = float(np.mean(acc[sf_te] == yte))
    print(f"checked {n_checked:,} (DFA, start, acceptance) hypotheses")
    print(f"best: k={k} states, train error {err:.1%}, "
          f"TEST ACCURACY {test_acc:.1%}")
    print(f"transitions delta[bit][state] = {delta.tolist()}, "
          f"start={start}, accept={acc.tolist()}")
    print(f"\nVERDICT: {'DEAD END OPENED -- the right hypothesis class '
          '(discrete states) solves from the same data where gradient '
          'engines memorized. Type-II confirmed: missing invariant, '
          'not missing data.' if test_acc > 0.99 else
          'still unsolved -- record honestly'}")
    print(f"white-box bonus: the induced machine IS the explanation "
          f"(2 states = even/odd).")
    print(f"runtime {time.time()-t0:.0f}s")
    json.dump(dict(k=k, train_err=err, test_acc=test_acc,
                   delta=delta.tolist(), start=int(start),
                   accept=acc.tolist(), n_checked=n_checked),
              io.open(os.path.join(HERE, "organ_induction_result.json"),
                      "w"), indent=1)


if __name__ == "__main__":
    main()
