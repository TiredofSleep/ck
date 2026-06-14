"""tig_probe_deep.py -- a THOROUGH interrogation of whether any TIG structure
lives inside CK (which was trained on books with zero knowledge of TIG).

Goes well beyond the first probe:
  1. ATOMS, every layer + decoded. VQ atoms at every residual depth; held-out
     MI(atom; next/current token, position); robustness over seeds and K; and for
     the most-informative layer, DECODE the top tokens per atom -- so we SEE what CK
     actually organizes by.
  2. sigma DYNAMICS, fairly. Per layer, the full atom-transition matrix; identity
     (self-loop) mass; and sigma given its BEST-CASE cluster->residue alignment
     (a quadratic-assignment local search), scored against a null of random target
     permutations -- both unconditional and CONDITIONED on the atom actually
     changing (which removes residual-stream persistence and gives sigma its best
     shot).
  3. TSML COMPOSE (the test skipped before). Compare the structure of CK's
     same-layer atom-adjacency matrix to the TSML composition table under best
     alignment vs a null. Reported with its honest methodological limits.

CPU-only; snapshot of the live checkpoint; does not disturb training.
  python tig_probe_deep.py
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

HERE = os.path.dirname(os.path.abspath(__file__))
SIGMA = [0, 7, 1, 3, 2, 4, 5, 6, 8, 9]
DEV = "cpu"
NSEQ, T = 160, 128


def load_model():
    snap = G.CKPT + ".dprobe"
    ck = None
    for _ in range(5):
        try:
            shutil.copyfile(G.CKPT, snap); ck = torch.load(snap, map_location="cpu"); break
        except Exception as e:
            print("ckpt retry:", e, flush=True); time.sleep(3)
    m = G.GrowGPT(G.INIT_LAYERS).to(DEV)
    while len(m.blocks) < ck["n_layers"]:
        m.grow()
    while len(m.folded) < ck.get("n_folded", 0):
        m.folded.append(G.ReZeroBlock().to(DEV))
    m.load_state_dict(ck["model"]); m.eval()
    try:
        os.remove(snap)
    except OSError:
        pass
    return m, ck["step"], len(m.blocks)


@torch.no_grad()
def collect(m):
    data = np.memmap(G.DATABIN, dtype=np.uint16, mode="r")
    val = data[-min(2_000_000, len(data) // 20):]
    rng = np.random.default_rng(0)
    starts = rng.integers(0, len(val) - T - 1, NSEQ)
    per = None; cur = []; nxt = []; pos = []
    for s in starts:
        idx = torch.from_numpy(val[s:s + T].astype(np.int64))[None, :]
        x = m.tok(idx) + m.pos(torch.arange(T))
        snaps = [x[0].clone()]
        for b in m.blocks:
            x = b(x); snaps.append(x[0].clone())
        if per is None:
            per = [[] for _ in snaps]
        for li, sx in enumerate(snaps):
            per[li].append(sx.numpy())
        cur.append(val[s:s + T].astype(np.int64))
        nxt.append(val[s + 1:s + 1 + T].astype(np.int64))
        pos.append(np.arange(T))
    per = [np.concatenate(p, 0) for p in per]
    return per, np.concatenate(cur), np.concatenate(nxt), np.concatenate(pos)


def _d(X, c):
    return (X * X).sum(1)[:, None] - 2 * X @ c.T + (c * c).sum(1)[None, :]


def kmeans(X, k, iters=30, seed=0):
    rng = np.random.default_rng(seed)
    c = X[rng.choice(len(X), k, replace=False)].copy()
    for _ in range(iters):
        lab = _d(X, c).argmin(1)
        for j in range(k):
            if (lab == j).any():
                c[j] = X[lab == j].mean(0)
    return lab, c


def mi(a, b):
    """mutual information I(a;b) in bits from integer label arrays."""
    a = a.astype(np.int64); b = b.astype(np.int64)
    na, nb = a.max() + 1, b.max() + 1
    j = np.zeros((na, nb))
    np.add.at(j, (a, b), 1)
    j /= j.sum()
    pa = j.sum(1, keepdims=True); pb = j.sum(0, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        v = j * np.log2(j / (pa * pb + 1e-12) + 1e-12)
    return float(v[j > 0].sum())


def best_sigma_align(T, target, restarts=120, seed=0):
    """Max over cluster->residue bijections m of sum_c T[c, m^{-1}(target[m(c)])].
    Local search (pairwise swaps), many restarts. Returns best score."""
    rng = np.random.default_rng(seed)
    K = len(target)
    tgt = np.array(target)
    best = -1.0
    for _ in range(restarts):
        m = rng.permutation(K)            # m[c] = residue of cluster c
        inv = np.argsort(m)               # inv[r] = cluster with residue r
        def score(m, inv):
            succ = inv[tgt[m]]            # predicted successor cluster of each c
            return T[np.arange(K), succ].sum()
        s = score(m, inv); improved = True
        while improved:
            improved = False
            for i in range(K):
                for j in range(i + 1, K):
                    m2 = m.copy(); m2[i], m2[j] = m2[j], m2[i]
                    inv2 = np.argsort(m2)
                    s2 = score(m2, inv2)
                    if s2 > s + 1e-12:
                        m, inv, s = m2, inv2, s2; improved = True
        best = max(best, s)
    return best


def sigma_test(T, label, seed=0):
    """sigma's best-align score vs identity mass vs null of random permutations."""
    K = len(SIGMA)
    ident_mass = float(np.trace(T))                    # labeling-invariant
    s_sigma = best_sigma_align(T, SIGMA, seed=seed)
    rng = np.random.default_rng(seed + 1)
    nulls = np.array([best_sigma_align(T, list(rng.permutation(K)), restarts=40,
                                       seed=seed + 2 + i) for i in range(60)])
    p = float((nulls >= s_sigma).mean())
    return dict(label=label, identity_mass=round(ident_mass, 3),
                sigma_bestalign=round(float(s_sigma), 3),
                null_mean=round(float(nulls.mean()), 3),
                null_max=round(float(nulls.max()), 3), sigma_p=round(p, 3))


def main():
    m, step, nL = load_model()
    print(f"=== DEEP TIG PROBE: CK @ step {step}, {nL} active layers ===\n", flush=True)
    per, cur, nxt, pos = collect(m)
    N = len(cur); half = N // 2
    posb = (pos // (T // 8)).astype(np.int64)          # 8 position buckets
    L = len(per)

    # ---------- Investigation 1: atoms at every layer ----------
    print("[1] ATOM INFORMATIVENESS BY LAYER (held-out MI in bits, K=10)", flush=True)
    print(f"{'layer':>6} {'MI(next)':>9} {'MI(curr)':>9} {'MI(pos)':>8}", flush=True)
    inf = []
    for li in range(L):
        X = per[li]; mu, sd = X[:half].mean(0), X[:half].std(0) + 1e-6
        lab_tr, c = kmeans((X[:half] - mu) / sd, 10, seed=0)
        lab_te = _d((X[half:] - mu) / sd, c).argmin(1)
        miN = mi(lab_te, nxt[half:]); miC = mi(lab_te, cur[half:]); miP = mi(lab_te, posb[half:])
        inf.append((li, miN, miC, miP))
        print(f"{li:>6} {miN:>9.3f} {miC:>9.3f} {miP:>8.3f}", flush=True)
    best_layer = max(inf, key=lambda r: r[1])[0]
    print(f"\n  most next-token-informative layer: {best_layer}", flush=True)

    # robustness of best layer over seeds and K
    print(f"  robustness @ layer {best_layer}:", flush=True)
    X = per[best_layer]; mu, sd = X[:half].mean(0), X[:half].std(0) + 1e-6
    for K in (10, 16, 32):
        vals = []
        for sd_ in (0, 1, 2):
            lt, c = kmeans((X[:half] - mu) / sd, K, seed=sd_)
            le = _d((X[half:] - mu) / sd, c).argmin(1)
            vals.append(mi(le, nxt[half:]))
        print(f"    K={K:>2}: MI(next)={np.mean(vals):.3f}+/-{np.std(vals):.3f}", flush=True)

    # decode atoms at best layer
    print(f"\n  WHAT THE ATOMS ARE (top current-tokens per atom, layer {best_layer}, K=10):", flush=True)
    try:
        from tokenizers import Tokenizer
        tk = Tokenizer.from_file(os.path.join(HERE, "ck_bpe.json"))
        def dec(i): return tk.id_to_token(int(i)) or "?"
    except Exception as e:
        print("   (tokenizer unavailable:", e, ")", flush=True); dec = lambda i: str(i)
    lab_tr, c = kmeans((X[:half] - mu) / sd, 10, seed=0)
    for a in range(10):
        toks = cur[:half][lab_tr == a]
        if not len(toks):
            continue
        top = np.bincount(toks).argsort()[::-1][:8]
        shown = " ".join(repr(dec(t).replace("Ġ", "_")) for t in top if (toks == t).any())
        print(f"    atom {a} (n={len(toks):>5}): {shown}", flush=True)

    # ---------- Investigation 2: sigma dynamics, fairly ----------
    print("\n[2] sigma DYNAMICS -- best-align score vs identity vs random-perm null", flush=True)
    allX = np.concatenate(per, 0); amu, asd = allX.mean(0), allX.std(0) + 1e-6
    lab_all, _ = kmeans((allX - amu) / asd, 10, seed=2)
    pl = [lab_all[i * N:(i + 1) * N] for i in range(L)]
    Tm = np.zeros((10, 10))
    for li in range(L - 1):
        np.add.at(Tm, (pl[li], pl[li + 1]), 1)
    Trow = Tm / (Tm.sum(1, keepdims=True) + 1e-9)
    r_uncond = sigma_test(Trow, "unconditional")
    Tc = Tm.copy(); np.fill_diagonal(Tc, 0)              # condition on atom CHANGING
    Tcr = Tc / (Tc.sum(1, keepdims=True) + 1e-9)
    r_cond = sigma_test(Tcr, "conditional-on-change")
    succ = Trow.argmax(1)
    # cycle type of the empirical successor map
    seen = set(); cyc = []
    for s0 in range(10):
        if s0 in seen:
            continue
        cc = []; x = s0
        while x not in seen:
            seen.add(x); cc.append(x); x = int(succ[x])
        cyc.append(len(cc))
    for r in (r_uncond, r_cond):
        print(f"  {r['label']:>22}: identity_mass={r['identity_mass']}  "
              f"sigma_bestalign={r['sigma_bestalign']}  null_mean={r['null_mean']} "
              f"null_max={r['null_max']}  p={r['sigma_p']}", flush=True)
    print(f"  empirical successor-map cycle type: {sorted(cyc, reverse=True)} "
          f"(sigma is [6,1,1,1,1])", flush=True)

    # ---------- Investigation 3: TSML compose (honest, limited) ----------
    print("\n[3] TSML COMPOSE -- same-layer atom adjacency vs TSML structure (best align)", flush=True)
    TSML = [[0, 0, 0, 0, 0, 0, 0, 7, 0, 0], [0, 7, 3, 7, 7, 7, 7, 7, 7, 7],
            [0, 3, 7, 7, 4, 7, 7, 7, 7, 9], [0, 7, 7, 7, 7, 7, 7, 7, 7, 3],
            [0, 7, 4, 7, 7, 7, 7, 7, 8, 7], [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],
            [0, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
            [0, 7, 7, 7, 8, 7, 7, 7, 7, 7], [0, 7, 9, 3, 7, 7, 7, 7, 7, 7]]
    TS = np.array(TSML, float)
    Madj = np.zeros((10, 10))
    base = pl[best_layer]
    np.add.at(Madj, (base[:-1], base[1:]), 1)
    Madj = (Madj + Madj.T)                                # symmetric, like TSML
    Madj /= Madj.sum()
    # best-align correlation of Madj to TSML over cluster->residue bijections
    def align_corr(M, target, restarts=120, seed=7):
        rng = np.random.default_rng(seed); K = 10; best = -1
        tv = target[np.triu_indices(K)]
        for _ in range(restarts):
            p = rng.permutation(K); s = np.corrcoef(M[np.ix_(p, p)][np.triu_indices(K)], tv)[0, 1]
            imp = True
            while imp:
                imp = False
                for i in range(K):
                    for j in range(i + 1, K):
                        p2 = p.copy(); p2[i], p2[j] = p2[j], p2[i]
                        s2 = np.corrcoef(M[np.ix_(p2, p2)][np.triu_indices(K)], tv)[0, 1]
                        if s2 > s + 1e-9:
                            p, s = p2, s2; imp = True
            best = max(best, s)
        return best
    c_ts = align_corr(Madj, TS)
    rng = np.random.default_rng(11)
    nullc = np.array([align_corr(Madj, np.array(TS)[np.ix_(rng.permutation(10), rng.permutation(10))],
                                 restarts=30, seed=20 + i) for i in range(30)])
    print(f"  best-align corr(adjacency, TSML)={c_ts:.3f}  null_mean={nullc.mean():.3f} "
          f"null_max={nullc.max():.3f}  p={(nullc >= c_ts).mean():.3f}", flush=True)
    print("  (caveat: COMPOSE needs a principled atom->operator identity; this tests "
          "structural similarity only, not exact composition.)", flush=True)

    out = dict(step=int(step), n_layers=int(nL), best_layer=int(best_layer),
               atom_MI_by_layer=[(li, round(a, 3), round(b, 3), round(c2, 3)) for li, a, b, c2 in inf],
               sigma_uncond=r_uncond, sigma_cond=r_cond,
               empirical_cycle_type=sorted(cyc, reverse=True),
               tsml_bestalign_corr=round(float(c_ts), 3),
               tsml_null_mean=round(float(nullc.mean()), 3))
    json.dump(out, open(os.path.join(HERE, "tig_probe_deep_result.json"), "w"), indent=1)
    print("\nsaved tig_probe_deep_result.json", flush=True)


if __name__ == "__main__":
    main()
