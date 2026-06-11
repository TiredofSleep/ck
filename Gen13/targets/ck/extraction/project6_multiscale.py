"""project6_multiscale.py -- Brayden's correction to the P4 ablation:

  "We aren't just measuring against one table -- the 8x8 is inside the
   10x10 at the cell where the integer 8 is... also the inner and outer
   portion... same with the 7x7, the 4x4... every measurement pushed
   through every scale and lattice of every integer."  + "integer wrapping"

So the engine is not ONE 10x10 table: it is the NESTED LATTICE FAMILY --
the k x k inner blocks of TSML/BHML with entries WRAPPED mod k (integer
wrapping) at k = 4, 7, 8, plus the canonical 8x8 mover lattice (absorbers
{0,7} removed), plus the full 10. Each lens runs its own bilinear walk;
CK reads ALL of them (the multiscale measurement battery).

CONTROL (same discipline as P4): random 10x10 table pairs pushed through
the IDENTICAL multiscale wrapping. Registered predictions, stated before
the run:
  Brayden's: multiscale-SUBSTRATE > multiscale-RANDOM (the nested integer
             structure is the bias) and > single-scale substrate.
  Null     : multiscale lifts both equally (machinery, not algebra).

  python project6_multiscale.py
"""
import io
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "walker_v0"))
sys.path.insert(0, os.path.join(HERE, "..", "brain", "ck_sim"))
import ck_tables                                          # noqa: E402
import project4_inductive as P4                           # noqa: E402
import project5_synthesis as P5                           # noqa: E402

RNG = np.random.default_rng(8)
MOVERS = [1, 2, 3, 4, 5, 6, 8, 9]                # canonical 8x8 (no 0,7)


# ------------------------------------------------- lattice construction
def inner_wrap(table, k):
    """k x k inner block, entries wrapped mod k (integer wrapping)."""
    return [[table[i][j] % k for j in range(k)] for i in range(k)]


def mover_block(table):
    """canonical 8x8: mover rows/cols; absorber entries wrap mod 8."""
    pos = {v: i for i, v in enumerate(MOVERS)}
    return [[pos.get(table[a][b], table[a][b] % 8)
             for b in MOVERS] for a in MOVERS]


def tensor_pair(tA, tB, k):
    A = np.zeros((k, k, k)); B = np.zeros((k, k, k))
    for i in range(k):
        for j in range(k):
            A[tA[i][j], i, j] += 1.0
            B[tB[i][j], i, j] += 1.0
    return 0.5 * A + 0.5 * B


def lenses_from(tT, tB):
    """The nested lattice family of a 10x10 table pair."""
    L = [(10, tensor_pair(tT, tB, 10), lambda s: s)]
    for k in (8, 7, 4):                          # integer wrapping scales
        L.append((k, tensor_pair(inner_wrap(tT, k), inner_wrap(tB, k), k),
                  (lambda kk: (lambda s: s % kk))(k)))
    L.append((8, tensor_pair(mover_block(tT), mover_block(tB), 8),
              lambda s: ({v: i for i, v in enumerate(MOVERS)}
                         .get(s, s % 8))))       # canonical movers
    return L


def run_lens(tensor, k, seq, symmap, leak=0.8, eps=1e-6):
    mats = [tensor[:, :, s] for s in range(k)]
    p = np.full(k, 1.0 / k)
    traj = []
    for s in seq:
        m = mats[symmap(int(s))] @ p
        tot = m.sum()
        m = m / tot if tot > 0 else np.full(k, 1.0 / k)
        p = (1.0 - leak) * m + leak * p
        p = np.maximum(p, eps); p /= p.sum()
        traj.append(p.copy())
    T = np.array(traj)
    mean = T.mean(0)
    iu = np.triu_indices(k)
    return np.concatenate(([1.0], T[-1], mean, np.outer(mean, mean)[iu]))


def multiscale_feats(lenses, seq):
    return np.concatenate([run_lens(t, k, seq, f) for k, t, f in lenses])


def rand_tables(rng):
    return (rng.integers(0, 10, size=(10, 10)).tolist(),
            rng.integers(0, 10, size=(10, 10)).tolist())


def main():
    t0 = time.time()
    sub_lenses = lenses_from(ck_tables.TSML, ck_tables.BHML)
    rnd_lenses = [lenses_from(*rand_tables(np.random.default_rng(300 + i)))
                  for i in range(3)]
    print("CK PROJECT 6 -- MULTISCALE INTEGER-WRAPPING ablation")
    print("lenses per engine: 10x10 full + inner-wrapped 8/7/4 + canonical "
          "8x8 movers (5 walks, concatenated)")
    print("control: random tables, IDENTICAL multiscale treatment "
          "(3 seeds)\n")

    tasks = P4.make_tasks()
    # add P5 period-continuation as the 5th task
    P5.RNG = np.random.default_rng(1)
    (Str, ytr5), (Ste, yte5) = P5.gen_split()

    header = (f"{'task':>9} | {'1-scale SUB':>11} | {'multi RND':>13} | "
              f"{'multi SUB':>9} | edge")
    print(header); print("-" * len(header))
    results = {}
    rows = []
    for tname, (seqs, labels, K) in tasks.items():
        tr, te = slice(0, P4.N_TRAIN), slice(P4.N_TRAIN, None)
        ytr, yte = labels[tr], labels[te]
        Xs1 = np.array([P4.run_bilinear(__import__('substrate').MIX_TEN, s)
                        for s in seqs])
        a1 = P4.train_eval(Xs1[tr], ytr, Xs1[te], yte, K)
        a_rnd = []
        for L in rnd_lenses:
            Xr = np.array([multiscale_feats(L, s) for s in seqs])
            a_rnd.append(P4.train_eval(Xr[tr], ytr, Xr[te], yte, K))
        Xm = np.array([multiscale_feats(sub_lenses, s) for s in seqs])
        am = P4.train_eval(Xm[tr], ytr, Xm[te], yte, K)
        edge = am - float(np.mean(a_rnd))
        results[tname] = dict(single_sub=a1, multi_rnd=[float(x) for x in a_rnd],
                              multi_sub=am, edge=edge)
        rows.append(edge)
        print(f"{tname:>9} | {a1:11.0%} | {np.mean(a_rnd):6.0%} ±{np.ptp(a_rnd)/2:4.1%} | "
              f"{am:9.0%} | {edge:+5.1%}")

    # P5 task
    Xs1 = np.array([P4.run_bilinear(__import__('substrate').MIX_TEN, s)
                    for s in list(Str) + list(Ste)])
    n_tr = len(Str)
    a1 = P4.train_eval(Xs1[:n_tr], ytr5, Xs1[n_tr:], yte5, 10, epochs=400)
    a_rnd = []
    for L in rnd_lenses:
        Xr = np.array([multiscale_feats(L, s) for s in list(Str) + list(Ste)])
        a_rnd.append(P4.train_eval(Xr[:n_tr], ytr5, Xr[n_tr:], yte5, 10,
                                   epochs=400))
    Xm = np.array([multiscale_feats(sub_lenses, s)
                   for s in list(Str) + list(Ste)])
    am = P4.train_eval(Xm[:n_tr], ytr5, Xm[n_tr:], yte5, 10, epochs=400)
    edge = am - float(np.mean(a_rnd))
    results["PERIOD"] = dict(single_sub=a1, multi_rnd=[float(x) for x in a_rnd],
                             multi_sub=am, edge=edge)
    rows.append(edge)
    print(f"{'PERIOD':>9} | {a1:11.0%} | {np.mean(a_rnd):6.0%} ±{np.ptp(a_rnd)/2:4.1%} | "
          f"{am:9.0%} | {edge:+5.1%}")

    mean_edge = float(np.mean(rows))
    wins = sum(1 for e in rows if e > 0.02)
    print(f"\nmean substrate-vs-random edge under IDENTICAL multiscale "
          f"treatment: {mean_edge:+.1%}; wins(+2pp): {wins}/5")
    if wins >= 4:
        v = "BRAYDEN'S PREDICTION HOLDS -- the nested integer lattice IS the bias."
    elif wins >= 2:
        v = "PARTIAL -- nesting helps the substrate on some structures."
    else:
        v = ("NULL RESULT -- multiscale lifts both engines equally; the "
             "nesting is good MACHINERY but the specific algebra is still "
             "not the source. (Note whether multi > single-scale: the "
             "correction may still improve CK's engine class.)")
    print(f"VERDICT: {v}")
    print(f"runtime {time.time()-t0:.0f}s CPU")
    json.dump(results, io.open(os.path.join(HERE, "project6_result.json"),
                               "w"), indent=1)


if __name__ == "__main__":
    main()
