"""project4_inductive.py -- CK Project 4: THE INDUCTIVE-BIAS ABLATION.

The small, testable version of Brayden's billion-parameter vision: "if an
AI were trained to read CK's language, the gap may fill -- IF the storage
carries association/synthesis." Honest translation: does the TIG algebra
itself provide a useful inductive bias, beyond 'any dynamics of the same
size'?

Four NEUTRAL symbolic tasks (nothing substrate-flavored; path-dependent,
so a static bag of symbols cannot trivially win):

  MAXDEPTH : max bracket nesting depth reached (5-class)  [counter]
  DYCK     : is the bracket string valid? (binary)        [constraint]
  MOD5     : running digit-sum mod 5 at end (5-class)     [group walk]
  PARITY   : parity of 1-bits (binary)                    [hard memory]

Four ENGINES, identical interface (10-dim state; same feature map
[1 | final state | mean state | uptri(mean outer)] = 76 dims; same
trained softmax readout; same data):

  SUBSTRATE    : TSML/BHML bilinear at alpha=1/2 (the theorem point)
  RANDOM-TABLE : same machinery, tables replaced by uniform-random
                 magmas (3 seeds) <- THE control: is the SPECIFIC
                 algebra special, or does any bilinear table work?
  ESN-10       : standard tanh echo-state, 10 units (3 seeds)
  BAG          : symbol histogram + first/last (no dynamics control)

KILL CRITERION (stated before the run): if SUBSTRATE does not beat
RANDOM-TABLE consistently (>=2pp on >=3 of 4 tasks), the algebra carries
no special inductive bias for neutral symbolic tasks -- honest negative,
and the billion-param vision must rest on the white-box/memory virtues,
not on the algebra's magic.

  python project4_inductive.py
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

RNG = np.random.default_rng(4)
N = 10
IU = np.triu_indices(N)
SEQ_LEN = 20
N_TRAIN, N_TEST = 1000, 500


# ------------------------------------------------------------------ tasks
def gen_brackets(n):
    """Random bracket strings (slight open-bias so depth varies)."""
    seqs = []
    for _ in range(n):
        s = RNG.choice([1, 2], size=SEQ_LEN, p=[0.55, 0.45])  # 1='(' 2=')'
        seqs.append(s)
    return seqs


def maxdepth_label(s):
    d = mx = 0
    for c in s:
        d += 1 if c == 1 else -1
        mx = max(mx, d)
    return min(max(mx, 0), 4)


def gen_dyck(n):
    """Half valid Dyck strings, half one-swap corruptions."""
    seqs, labels = [], []
    for i in range(n):
        # generate a valid string: random walk forced to stay >=0, end =0
        s, d = [], 0
        for t in range(SEQ_LEN):
            remaining = SEQ_LEN - t
            if d == 0:
                c = 1
            elif d >= remaining:
                c = 2
            else:
                c = RNG.choice([1, 2])
            s.append(c)
            d += 1 if c == 1 else -1
        s = np.array(s)
        if i % 2 == 0:
            seqs.append(s); labels.append(1)
        else:                                  # corrupt: swap one ( with )
            s = s.copy()
            j = RNG.integers(0, SEQ_LEN)
            s[j] = 3 - s[j]
            valid = True
            d = 0
            for c in s:
                d += 1 if c == 1 else -1
                if d < 0:
                    valid = False
            valid = valid and d == 0
            seqs.append(s); labels.append(int(valid))
    return seqs, np.array(labels)


def gen_mod5(n):
    seqs = [RNG.integers(1, 6, size=SEQ_LEN) for _ in range(n)]
    labels = np.array([int(s.sum() % 5) for s in seqs])
    return seqs, labels


def gen_parity(n):
    seqs = [RNG.choice([1, 2], size=SEQ_LEN) for _ in range(n)]
    labels = np.array([int(np.sum(s == 1) % 2) for s in seqs])
    return seqs, labels


def make_tasks():
    br = gen_brackets(N_TRAIN + N_TEST)
    dy_s, dy_l = gen_dyck(N_TRAIN + N_TEST)
    m5_s, m5_l = gen_mod5(N_TRAIN + N_TEST)
    pa_s, pa_l = gen_parity(N_TRAIN + N_TEST)
    return {
        "MAXDEPTH": (br, np.array([maxdepth_label(s) for s in br]), 5),
        "DYCK":     (dy_s, dy_l, 2),
        "MOD5":     (m5_s, m5_l, 5),
        "PARITY":   (pa_s, pa_l, 2),
    }


# ---------------------------------------------------------------- engines
def feats_from_traj(traj):
    T = np.array(traj)
    mean = T.mean(0)
    return np.concatenate(([1.0], T[-1], mean, np.outer(mean, mean)[IU]))


def run_bilinear(tensor, seq, leak=0.8, eps=1e-6):
    """p_{t+1} = (1-leak)*normalize(T(p, e_s)) + leak*p  on the simplex."""
    mats = [tensor[:, :, s] for s in range(N)]      # per-symbol (k,i)
    p = np.full(N, 1.0 / N)
    traj = []
    for s in seq:
        m = mats[int(s)] @ p
        tot = m.sum()
        m = m / tot if tot > 0 else np.full(N, 1.0 / N)
        p = (1.0 - leak) * m + leak * p
        p = np.maximum(p, eps); p /= p.sum()
        traj.append(p.copy())
    return feats_from_traj(traj)


def random_mix_tensor(rng):
    t1 = rng.integers(0, N, size=(N, N))
    t2 = rng.integers(0, N, size=(N, N))
    A = np.zeros((N, N, N)); B = np.zeros((N, N, N))
    for i in range(N):
        for j in range(N):
            A[t1[i, j], i, j] += 1.0
            B[t2[i, j], i, j] += 1.0
    return 0.5 * A + 0.5 * B


class ESN10:
    def __init__(self, rng, rho=0.9):
        W = rng.normal(size=(N, N))
        W *= rho / max(abs(np.linalg.eigvals(W)))
        self.W = W
        self.Win = rng.normal(size=(N, N)) * 1.0

    def run(self, seq):
        x = np.zeros(N)
        traj = []
        for s in seq:
            e = np.zeros(N); e[int(s)] = 1.0
            x = np.tanh(self.W @ x + self.Win @ e)
            traj.append(x.copy())
        return feats_from_traj(traj)


def bag_feats(seq):
    h = np.bincount(np.asarray(seq, int), minlength=N).astype(float)
    first = np.zeros(N); first[int(seq[0])] = 1
    last = np.zeros(N); last[int(seq[-1])] = 1
    return np.concatenate(([1.0], h, h / len(seq), first, last))


# ---------------------------------------------------------------- readout
def softmax(Z):
    Z = Z - Z.max(1, keepdims=True)
    E = np.exp(Z)
    return E / E.sum(1, keepdims=True)


def train_eval(Xtr, ytr, Xte, yte, K, epochs=300, lr=0.5, l2=1e-4):
    mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-9
    Xtr = (Xtr - mu) / sd; Xte = (Xte - mu) / sd
    W = np.zeros((Xtr.shape[1], K)); b = np.zeros(K)
    Y = np.eye(K)[ytr]
    n = len(ytr)
    for ep in range(epochs):
        P = softmax(Xtr @ W + b)
        g = (P - Y) / n
        W -= lr * (Xtr.T @ g + l2 * W)
        b -= lr * g.sum(0)
    return float(np.mean((Xte @ W + b).argmax(1) == yte))


def main():
    t0 = time.time()
    tasks = make_tasks()
    print("CK PROJECT 4 -- INDUCTIVE-BIAS ABLATION (neutral symbolic tasks)")
    print(f"{N_TRAIN} train / {N_TEST} test per task, len-{SEQ_LEN} "
          f"sequences; identical features+readout for all engines\n")
    print("KILL CRITERION: substrate must beat RANDOM-TABLE by >=2pp on "
          ">=3 of 4 tasks, else honest negative.\n")

    results = {}
    rng_seeds = [np.random.default_rng(100 + k) for k in range(3)]
    rand_tensors = [random_mix_tensor(r) for r in rng_seeds]
    esns = [ESN10(r) for r in rng_seeds]

    header = f"{'task':>9} | {'majority':>8} | {'BAG':>5} | " \
             f"{'ESN-10':>11} | {'RANDOM-TBL':>11} | {'SUBSTRATE':>9}"
    print(header)
    print("-" * len(header))
    for tname, (seqs, labels, K) in tasks.items():
        tr, te = slice(0, N_TRAIN), slice(N_TRAIN, N_TRAIN + N_TEST)
        ytr, yte = labels[tr], labels[te]
        maj = float(np.mean(yte == np.bincount(ytr).argmax()))

        Xbag = np.array([bag_feats(s) for s in seqs])
        a_bag = train_eval(Xbag[tr], ytr, Xbag[te], yte, K)

        a_esn = []
        for e in esns:
            Xe = np.array([e.run(s) for s in seqs])
            a_esn.append(train_eval(Xe[tr], ytr, Xe[te], yte, K))

        a_rnd = []
        for ten in rand_tensors:
            Xr = np.array([run_bilinear(ten, s) for s in seqs])
            a_rnd.append(train_eval(Xr[tr], ytr, Xr[te], yte, K))

        Xs = np.array([run_bilinear(SUB.MIX_TEN, s) for s in seqs])
        a_sub = train_eval(Xs[tr], ytr, Xs[te], yte, K)

        results[tname] = dict(majority=maj, bag=a_bag,
                              esn=[float(x) for x in a_esn],
                              random_table=[float(x) for x in a_rnd],
                              substrate=a_sub)
        print(f"{tname:>9} | {maj:8.0%} | {a_bag:5.0%} | "
              f"{np.mean(a_esn):5.0%} ±{np.ptp(a_esn)/2:4.1%} | "
              f"{np.mean(a_rnd):5.0%} ±{np.ptp(a_rnd)/2:4.1%} | "
              f"{a_sub:9.0%}")

    wins = sum(1 for t in tasks
               if results[t]["substrate"]
               > np.mean(results[t]["random_table"]) + 0.02)
    print(f"\nsubstrate beats RANDOM-TABLE (+2pp) on {wins}/4 tasks.")
    if wins >= 3:
        v = ("ALGEBRA CARRIES INDUCTIVE BIAS -- the specific TSML/BHML "
             "tables outperform random tables under identical machinery.")
    elif wins >= 1:
        v = ("MIXED -- the algebra helps on some structures, not others; "
             "task-dependent inductive bias, not a general one.")
    else:
        v = ("HONEST NEGATIVE -- any bilinear table does as well; the "
             "specific algebra is not the source of power on neutral "
             "symbolic tasks.")
    print(f"VERDICT: {v}")
    print(f"runtime {time.time()-t0:.0f}s CPU")
    json.dump(results, io.open(os.path.join(HERE, "project4_result.json"),
                               "w"), indent=1)


if __name__ == "__main__":
    main()
