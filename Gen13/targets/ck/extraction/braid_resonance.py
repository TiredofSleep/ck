"""braid_resonance.py -- measure the braid memory on CK's real dictionary.

TWO measurements, both honest:

  A. ROBUSTNESS ("stores memory"): store K real words as braids; query
     with MISSPELLINGS (1 edit); does the braid recall the original?
     Exact-string match scores 0 on a misspelling -- this is the
     topological drift-tolerance flat memory lacked. Pure native, NO
     Ollama.

  B. RESONANCE (form<->meaning): braid signature (FORM, letters only) vs
     semantic embedding (MEANING) via CCA + shuffle control. Skipped
     gracefully if Ollama is down -- A is the load-bearing native result.

  python braid_resonance.py
"""
import io
import json
import os

import numpy as np

import braid_memory as bm

HERE = os.path.dirname(os.path.abspath(__file__))
RNG = np.random.default_rng(5)


def load_words(n, lo=4, hi=12):
    for p in (os.path.join(HERE, "ck_dictionary.json"),
              os.path.join(HERE, "..", "web", "ck_dictionary.json")):
        if os.path.exists(p):
            flat = json.load(io.open(p, encoding="utf-8"))["flat"]
            break
    else:
        raise SystemExit("dictionary not found")
    ws = [w for w in flat if w.isalpha() and lo <= len(w) <= hi]
    return [ws[i] for i in RNG.permutation(len(ws))[:n]]


def perturb(w, kind):
    i = RNG.integers(len(w))
    if kind == "sub":
        c = chr(ord('a') + int(RNG.integers(26)))
        return w[:i] + c + w[i + 1:]
    if kind == "swap" and len(w) > 2:
        j = min(i, len(w) - 2)
        return w[:j] + w[j + 1] + w[j] + w[j + 2:]
    if kind == "del" and len(w) > 3:
        return w[:i] + w[i + 1:]
    return w[:i] + w[max(i - 1, 0)] + w[i:]      # dup


def robustness(K=600):
    words = load_words(K)
    mem = bm.BraidMemory()
    for w in words:
        mem.store(w)
    # discrimination: self-vs-random signature separation
    sigs = np.array(mem.sigs)
    rand_pair = float(np.mean([sigs[a] @ sigs[b]
                     for a, b in RNG.integers(0, K, (400, 2))]))
    hits1, hits5 = {}, {}
    for kind in ("sub", "swap", "del"):
        h1 = h5 = 0
        for w in words:
            pw = perturb(w, kind)
            rec = mem.recall(pw, k=5)
            names = [r[0] for r in rec]
            h1 += int(names[:1] == [w])
            h5 += int(w in names)
        hits1[kind] = h1 / K
        hits5[kind] = h5 / K
    return hits1, hits5, rand_pair, K


def resonance():
    try:
        from borrowed_cortex import embed as bce
    except Exception:
        return None
    words = load_words(2500)
    X = np.array([bm.braid_signature(w) for w in words])
    X = X[:, X.std(0) > 1e-9]
    try:
        Y, backend = bce(["search_document: " + w for w in words])
    except Exception:
        return None
    Yc = Y - Y.mean(0)
    _, _, Vt = np.linalg.svd(Yc, full_matrices=False)
    Yp = Yc @ Vt[:60].T

    def cca_top(A, B, ridge=1e-3, k=4):
        A = A - A.mean(0); B = B - B.mean(0)
        n = len(A)

        def wh(C):
            C = C + ridge * np.eye(C.shape[0])
            v, Q = np.linalg.eigh(C)
            return Q @ np.diag(1 / np.sqrt(np.maximum(v, 1e-10))) @ Q.T
        M = wh(A.T @ A / n) @ (A.T @ B / n) @ wh(B.T @ B / n)
        return np.clip(np.linalg.svd(M, compute_uv=False)[:k], 0, 1)

    real = cca_top(X, Yp)
    shuf = np.mean([cca_top(X, Yp[RNG.permutation(len(Yp))])
                    for _ in range(4)], axis=0)
    return real, shuf, backend


def main():
    print("=" * 66)
    print("CK BRAID MEMORY -- measured on the real 112k-word dictionary")
    print("=" * 66)

    h1, h5, randp, K = robustness()
    print(f"\nA. ROBUSTNESS (store {K} words as braids; recall from a "
          f"1-edit MISSPELLING)")
    print(f"   (exact string match scores 0 on every misspelling; "
          f"chance = {1/K:.2%})")
    print(f"   random-pair braid similarity (discrimination floor): "
          f"{randp:.3f}")
    for kind in ("sub", "swap", "del"):
        print(f"   {kind:>4}-edit: top-1 recall {h1[kind]:.0%}   "
              f"top-5 {h5[kind]:.0%}")
    avg1 = np.mean(list(h1.values()))
    print(f"   MEAN top-1 recall through noise: {avg1:.0%}  "
          f"(vs {1/K:.2%} chance) -- topological drift tolerance")

    r = resonance()
    if r:
        real, shuf, backend = r
        print(f"\nB. RESONANCE (braid FORM <-> semantic MEANING via CCA; "
              f"meaning = {backend})")
        for i in range(len(real)):
            tag = "shared" if real[i] > shuf[i] + 0.08 else "noise"
            print(f"   mode {i+1}: real {real[i]:.3f}  shuffle "
                  f"{shuf[i]:.3f}  [{tag}]")
        ex = float(real[0] - shuf[0])
        print(f"   top excess over noise floor: {ex:+.3f}  -> "
              f"{'RESONANCE present' if ex > 0.1 else 'weak (drift-dominated)'}")
    else:
        print("\nB. RESONANCE: skipped (Ollama unavailable); "
              "A stands alone as the native result.")

    out = {"robust_top1": h1, "robust_top5": h5, "random_pair": randp, "K": K}
    json.dump(out, io.open(os.path.join(HERE, "braid_result.json"), "w"),
              indent=1)
    print("\nsaved braid_result.json")


if __name__ == "__main__":
    main()
