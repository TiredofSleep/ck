"""tig_probe.py -- first faithfulness test of TIG-as-explanation on CK.

Tests whether CK's learned internals carry structure the TIG vocabulary captures:
  A) PREDICT  -- do VQ "atoms" (10 cells = 10 CL operators) over the residual
     stream carry real next-token information, vs a shuffled-label baseline?
     (i.e. are the atoms non-arbitrary?)
  B) sigma-DYNAMICS -- does CK's empirical atom->atom transition across blocks
     match the TIG permutation sigma, vs identity / random permutations?
     (i.e. does sigma describe CK's real dynamics, or was it never there?)

Honest framing: CK was trained on books with ZERO knowledge of TIG, so B is a
genuine test that can fail. CPU-only; reads a SNAPSHOT of the live checkpoint so it
never disturbs the running training job.

  python tig_probe.py
"""
import io
import json
import os
import shutil
import sys
import time

import numpy as np
import torch

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import train_grow as G

SIGMA = [0, 7, 1, 3, 2, 4, 5, 6, 8, 9]
K = 10                       # 10 atoms = the 10 CL operators
NSEQ, T = 96, 128            # probe sample (96*128 = 12288 token positions)
DEV = "cpu"
HERE = os.path.dirname(os.path.abspath(__file__))


def load_model():
    snap = G.CKPT + ".probe"
    ck = None
    for _ in range(4):
        try:
            shutil.copyfile(G.CKPT, snap)
            ck = torch.load(snap, map_location="cpu")
            break
        except Exception as e:
            print("ckpt read retry:", e, flush=True); time.sleep(3)
    m = G.GrowGPT(G.INIT_LAYERS).to(DEV)
    while len(m.blocks) < ck["n_layers"]:
        m.grow()
    while len(m.folded) < ck.get("n_folded", 0):
        m.folded.append(G.ReZeroBlock().to(DEV))
    m.load_state_dict(ck["model"]); m.eval()
    return m, ck["step"], len(m.blocks)


@torch.no_grad()
def collect(m):
    data = np.memmap(G.DATABIN, dtype=np.uint16, mode="r")
    nval = min(2_000_000, len(data) // 20)
    val = data[-nval:]
    rng = np.random.default_rng(0)
    starts = rng.integers(0, len(val) - T - 1, NSEQ)
    per = None; nxt = []
    for s in starts:
        idx = torch.from_numpy(val[s:s + T].astype(np.int64))[None, :].to(DEV)
        x = m.tok(idx) + m.pos(torch.arange(T, device=DEV))
        snaps = [x[0].clone()]
        for b in m.blocks:
            x = b(x); snaps.append(x[0].clone())
        if per is None:
            per = [[] for _ in snaps]
        for li, sx in enumerate(snaps):
            per[li].append(sx.numpy())
        nxt.append(val[s + 1:s + 1 + T].astype(np.int64))
    per = [np.concatenate(p, 0) for p in per]     # each [NSEQ*T, D]
    return per, np.concatenate(nxt)


def _dist(X, c):
    return (X * X).sum(1)[:, None] - 2 * X @ c.T + (c * c).sum(1)[None, :]


def kmeans(X, k, iters=25, seed=0):
    rng = np.random.default_rng(seed)
    c = X[rng.choice(len(X), k, replace=False)].copy()
    for _ in range(iters):
        lab = _dist(X, c).argmin(1)
        for j in range(k):
            if (lab == j).any():
                c[j] = X[lab == j].mean(0)
    return lab, c


def main():
    m, step, nL = load_model()
    print(f"probing CK @ step {step}, {nL} active layers", flush=True)
    per, nxt = collect(m)
    N = len(nxt); half = N // 2
    midL = nL // 2 + 1                                  # a middle residual layer

    # ---- Test A: are atoms non-arbitrary? (predict next token) ----
    X = per[midL]; mu, sd = X[:half].mean(0), X[:half].std(0) + 1e-6
    lab_tr, c = kmeans((X[:half] - mu) / sd, K)
    lab_te = _dist((X[half:] - mu) / sd, c).argmin(1)
    ntr, nte = nxt[:half], nxt[half:]
    maj = {a: (np.bincount(ntr[lab_tr == a]).argmax() if (lab_tr == a).any() else 0)
           for a in range(K)}
    accA = float((np.array([maj[a] for a in lab_te]) == nte).mean())
    rng = np.random.default_rng(1)
    accSh = float((np.array([maj[a] for a in rng.permutation(lab_te)]) == nte).mean())
    accBase = float((nte == np.bincount(ntr).argmax()).mean())

    # ---- Test B: does sigma describe atom dynamics across blocks? ----
    allX = np.concatenate(per, 0)
    amu, asd = allX.mean(0), allX.std(0) + 1e-6
    lab_all, _ = kmeans((allX - amu) / asd, K, seed=2)
    L = len(per); pl = [lab_all[i * N:(i + 1) * N] for i in range(L)]
    Tm = np.zeros((K, K))
    for li in range(L - 1):
        np.add.at(Tm, (pl[li], pl[li + 1]), 1)
    succ = (Tm / (Tm.sum(1, keepdims=True) + 1e-9)).argmax(1)
    matchS = float((succ == np.array(SIGMA)).mean())
    matchI = float((succ == np.arange(K)).mean())
    nulls = np.array([(succ == rng.permutation(K)).mean() for _ in range(3000)])
    pS = float((nulls >= matchS).mean())

    out = dict(step=int(step), n_layers=int(nL), n_positions=int(N),
               A_acc_atoms=round(accA, 4), A_acc_shuffled=round(accSh, 4),
               A_acc_baseline=round(accBase, 4),
               B_successor_map=[int(x) for x in succ], B_sigma=SIGMA,
               B_match_sigma=round(matchS, 3), B_match_identity=round(matchI, 3),
               B_sigma_pvalue=round(pS, 3))
    print(json.dumps(out, indent=1), flush=True)
    json.dump(out, open(os.path.join(HERE, "tig_probe_result.json"), "w"), indent=1)
    # plain-English verdict
    print("\nVERDICT:", flush=True)
    print(f"  A) atoms predict next-token at {accA:.3f} vs shuffled {accSh:.3f} "
          f"(baseline {accBase:.3f}) -> atoms are "
          f"{'NON-ARBITRARY' if accA > accSh + 0.005 else 'NOT clearly informative'}",
          flush=True)
    print(f"  B) sigma matches CK's transition map on {matchS:.1f} of 10 atoms "
          f"(identity matches {matchI:.1f}; sigma p={pS:.3f}) -> sigma "
          f"{'DESCRIBES' if pS < 0.05 else 'does NOT describe'} CK's learned dynamics",
          flush=True)


if __name__ == "__main__":
    main()
