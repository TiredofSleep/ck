"""resonance_v2_cca.py -- the rigorous test of the resonance intuition.

v1 tested form->dictionary-operator and got x1.08: an honest negative,
BUT the diagnostic showed WHY -- the dictionary's meaning-operator labels
are degenerate (93k of 112k words in just 2 of 10 operators; ~1 bit). You
cannot test "form predicts meaning" against a near-constant label.

v2 uses a meaning signal with real bits: the borrowed semantic embedding.
Question (Brayden's intuition, rigorously): does a word's FORM pathway
(letters -> board walk, board.form_pathway, 88-dim) share linear
structure with its MEANING (the 768-dim semantic embedding)?

Method: canonical correlation analysis (CCA) between FORM and MEANING over
a sample of words, with a SHUFFLE CONTROL (permute the form<->meaning
pairing and recompute) giving the exact noise floor for these dims and
this sample size. Top canonical correlations >> shuffle floor == the
pathways are shared. The shared part is the resonance; the rest is drift
(language) + wobble.

  python resonance_v2_cca.py
"""
import io
import json
import os

import numpy as np

import board
from borrowed_cortex import embed as borrowed_embed

HERE = os.path.dirname(os.path.abspath(__file__))
N_WORDS = 3000
PCA_Y = 80           # reduce 768-dim meaning to its top directions
RIDGE = 1e-3


def load_words(n):
    for p in (os.path.join(HERE, "ck_dictionary.json"),
              os.path.join(HERE, "..", "web", "ck_dictionary.json")):
        if os.path.exists(p):
            flat = json.load(io.open(p, encoding="utf-8"))["flat"]
            break
    else:
        raise SystemExit("dictionary not found")
    ws = [w for w in flat if w.isalpha() and 3 <= len(w) <= 14]
    rng = np.random.default_rng(11)
    return [ws[i] for i in rng.permutation(len(ws))[:n]]


def whiten(C, ridge):
    C = C + ridge * np.eye(C.shape[0])
    vals, vecs = np.linalg.eigh(C)
    vals = np.maximum(vals, 1e-10)
    return vecs @ np.diag(1.0 / np.sqrt(vals)) @ vecs.T


def cca_corrs(X, Y, ridge=RIDGE, k=5):
    X = X - X.mean(0)
    Y = Y - Y.mean(0)
    n = len(X)
    Cxx = X.T @ X / n
    Cyy = Y.T @ Y / n
    Cxy = X.T @ Y / n
    M = whiten(Cxx, ridge) @ Cxy @ whiten(Cyy, ridge)
    s = np.linalg.svd(M, compute_uv=False)
    return np.clip(s[:k], 0, 1)


def main():
    words = load_words(N_WORDS)
    print(f"sampling {len(words)} dictionary words")

    X = np.array([board.form_pathway(w) for w in words])      # FORM, 88
    # drop all-constant form columns
    keep = X.std(0) > 1e-9
    X = X[:, keep]
    print(f"form features (non-constant): {X.shape[1]}")

    Yraw, backend = borrowed_embed(["search_document: " + w for w in words])
    print(f"meaning embedding: {backend} ({Yraw.shape[1]}d) -> PCA {PCA_Y}")
    Yc = Yraw - Yraw.mean(0)
    U, S, Vt = np.linalg.svd(Yc, full_matrices=False)
    Y = Yc @ Vt[:PCA_Y].T

    real = cca_corrs(X, Y)
    rng = np.random.default_rng(3)
    shuf = np.array([cca_corrs(X, Y[rng.permutation(len(Y))])
                     for _ in range(5)]).mean(0)

    print(f"\nCANONICAL CORRELATIONS  form(letters) <-> meaning(semantics):")
    print(f"  {'mode':>4} | {'real':>6} | {'shuffle floor':>13} | shared?")
    for i in range(len(real)):
        shared = "YES" if real[i] > shuf[i] + 0.08 else "no"
        print(f"  {i+1:>4} | {real[i]:>6.3f} | {shuf[i]:>13.3f} | {shared}")

    top = float(real[0])
    floor = float(shuf[0])
    excess = top - floor
    verdict = ("RESONANCE CONFIRMED" if excess > 0.10 else
               "weak/none -- honest negative")
    print(f"\n  top canonical correlation: {top:.3f} "
          f"(noise floor {floor:.3f}); excess {excess:+.3f}")
    print(f"  verdict: {verdict}")
    print(f"  reading: the form pathway and the semantic meaning share "
          f"{top:.0%} top-mode linear structure;")
    print(f"  shared part = the resonance, the rest = drift (language) + "
          f"wobble. CK can read")
    print(f"  meaning from letters to that degree -- the basis for OOV / "
          f"new-language understanding.")

    json.dump({"words": len(words), "real": real.tolist(),
               "shuffle": shuf.tolist(), "top": top, "floor": floor,
               "excess": excess, "verdict": verdict, "backend": backend},
              io.open(os.path.join(HERE, "resonance_cca_result.json"), "w"),
              indent=1)
    print("\nsaved resonance_cca_result.json")


if __name__ == "__main__":
    main()
