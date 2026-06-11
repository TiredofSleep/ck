"""cross_language.py -- "across languages the parallels should hold if you
take enough measurements -- not to see letters, but to see FORM."

Test: a concept in several languages should braid into PARALLEL pathways.
CK measures each translated word's FORM (braid_signature_rich -- Burau at
the 4 primitive 10th roots, 'enough measurements'), never a per-language
dictionary. If form-resonance is translation-invariant, the translations
of one concept cluster together above chance.

Honest design: Latin-script Indo-European (en/es/fr/it/de) so the
letter->operator measurement applies; concepts SPLIT into cognate-heavy
vs non-cognate so the truth shows (cognates share form trivially; the
real test is whether non-cognates still parallel). Metric: cross-language
nearest-neighbour retrieval (is a word's nearest foreign word its own
translation?) vs chance, + concept-cluster silhouette, + shuffle control.

  python cross_language.py
"""
import io
import json
import os
import unicodedata

import numpy as np

import braid_memory as bm

HERE = os.path.dirname(os.path.abspath(__file__))
RNG = np.random.default_rng(13)

# concept -> {lang: word}; langs en es fr it de
CONCEPTS = {
 "mother": dict(en="mother", es="madre", fr="mere", it="madre", de="mutter"),
 "night":  dict(en="night",  es="noche", fr="nuit",  it="notte", de="nacht"),
 "sun":    dict(en="sun",    es="sol",   fr="soleil",it="sole",  de="sonne"),
 "fire":   dict(en="fire",   es="fuego", fr="feu",   it="fuoco", de="feuer"),
 "light":  dict(en="light",  es="luz",   fr="lumiere",it="luce", de="licht"),
 "star":   dict(en="star",   es="estrella",fr="etoile",it="stella",de="stern"),
 "bread":  dict(en="bread",  es="pan",   fr="pain",  it="pane",  de="brot"),
 "book":   dict(en="book",   es="libro", fr="livre", it="libro", de="buch"),
 "cold":   dict(en="cold",   es="frio",  fr="froid", it="freddo",de="kalt"),
 "new":    dict(en="new",    es="nuevo", fr="nouveau",it="nuovo",de="neu"),
 # harder non-cognate concepts:
 "water":  dict(en="water",  es="agua",  fr="eau",   it="acqua", de="wasser"),
 "dog":    dict(en="dog",    es="perro", fr="chien", it="cane",  de="hund"),
 "house":  dict(en="house",  es="casa",  fr="maison",it="casa",  de="haus"),
 "tree":   dict(en="tree",   es="arbol", fr="arbre", it="albero",de="baum"),
 "love":   dict(en="love",   es="amor",  fr="amour", it="amore", de="liebe"),
}
COGNATE = {"mother", "night", "sun", "fire", "star", "bread", "book",
           "cold", "new", "light"}        # share Indo-European roots
NONCOG = {"water", "dog", "house", "tree", "love"}   # weakly/non shared
LANGS = ["en", "es", "fr", "it", "de"]


def deaccent(w):
    return "".join(c for c in unicodedata.normalize("NFKD", w)
                   if not unicodedata.combining(c))


def whiten(M):
    M = (M - M.mean(0)) / (M.std(0) + 1e-9)
    return M / (np.linalg.norm(M, axis=1, keepdims=True) + 1e-9)


def retrieval(concepts):
    """For each (concept, langA) word, rank all langB words by braid sim;
    is the true translation top-1? Averaged over ordered language pairs."""
    rows, meta = [], []
    for c in concepts:
        for lg in LANGS:
            rows.append(bm.braid_signature_rich(deaccent(CONCEPTS[c][lg])))
            meta.append((c, lg))
    W = whiten(np.array(rows))
    S = W @ W.T
    nC = len(concepts)
    top1 = top3 = tot = 0
    for i, (ci, li) in enumerate(meta):
        for lj in LANGS:
            if lj == li:
                continue
            cand = [k for k, (ck, lk) in enumerate(meta) if lk == lj]
            sims = [(S[i, k], meta[k][0]) for k in cand]
            sims.sort(reverse=True)
            tot += 1
            if sims[0][1] == ci:
                top1 += 1
            if ci in [c for _, c in sims[:3]]:
                top3 += 1
    return top1 / tot, top3 / tot, 1.0 / nC


def silhouette(concepts):
    rows, lab = [], []
    for c in concepts:
        for lg in LANGS:
            rows.append(bm.braid_signature_rich(deaccent(CONCEPTS[c][lg])))
            lab.append(c)
    W = whiten(np.array(rows))
    S = W @ W.T
    lab = np.array(lab)
    within, between = [], []
    for i in range(len(W)):
        same = (lab == lab[i]); same[i] = False
        if same.any():
            within.append(S[i, same].mean())
            between.append(S[i, ~same & (np.arange(len(W)) != i)].mean())
    return float(np.mean(within)), float(np.mean(between))


def main():
    print("=" * 66)
    print("CK CROSS-LANGUAGE FORM PARALLELS  (white-box, no per-lang dict)")
    print("=" * 66)
    allc = list(CONCEPTS)
    print(f"{len(allc)} concepts x {len(LANGS)} languages (en/es/fr/it/de);")
    print("CK measures FORM via braid at 4 primitive 10th roots -- never a "
          "translation table.\n")

    for label, subset in (("ALL concepts", allc),
                          ("COGNATE-heavy", [c for c in allc if c in COGNATE]),
                          ("NON-COGNATE", [c for c in allc if c in NONCOG])):
        t1, t3, ch = retrieval(subset)
        wi, bw = silhouette(subset)
        print(f"{label} (n={len(subset)}):")
        print(f"   cross-language top-1 retrieval {t1:.0%}, top-3 {t3:.0%}  "
              f"(chance {ch:.0%})")
        print(f"   concept cluster: within-sim {wi:+.3f} vs between {bw:+.3f}"
              f"  (gap {wi-bw:+.3f})")

    # shuffle control on ALL
    rows = [bm.braid_signature_rich(deaccent(CONCEPTS[c][lg]))
            for c in allc for lg in LANGS]
    W = whiten(np.array(rows))
    S = W @ W.T
    lab = np.array([c for c in allc for lg in LANGS])
    real_gap = []
    for i in range(len(W)):
        same = (lab == lab[i]); same[i] = False
        oth = ~same & (np.arange(len(W)) != i)
        real_gap.append(S[i, same].mean() - S[i, oth].mean())
    real_gap = np.mean(real_gap)
    shuf = []
    for _ in range(500):
        pl = lab[RNG.permutation(len(lab))]
        g = []
        for i in range(len(W)):
            same = (pl == pl[i]); same[i] = False
            oth = ~same & (np.arange(len(W)) != i)
            if same.any():
                g.append(S[i, same].mean() - S[i, oth].mean())
        shuf.append(np.mean(g))
    shuf = np.array(shuf)
    p = (np.sum(shuf >= real_gap) + 1) / (len(shuf) + 1)
    print(f"\nconcept-cluster gap (ALL): real {real_gap:+.3f} vs "
          f"shuffle {shuf.mean():+.3f}; permutation p = {p:.3f}")

    # white-box: orange across languages (it's in the color set, add here)
    orange = {"en": "orange", "es": "naranja", "fr": "orange",
              "it": "arancione", "de": "orange"}
    print("\nWHITE-BOX: 'orange' across languages -- braid trace-phase "
          "invariant (root k=1):")
    for lg, w in orange.items():
        ph = bm.braid_signature_rich(deaccent(w))[1]
        print(f"   {lg}: {w:>10}  phase {ph:+.4f}")

    print(f"\nverdict: cross-language form-parallelism is "
          f"{'PRESENT' if p < 0.05 else 'weak'} "
          f"(p={p:.3f}); cognate vs non-cognate split shows how much is "
          f"shared-root form vs deeper. Indo-European Latin-script only -- "
          f"the universal claim (unrelated families/scripts) is bigger and "
          f"flagged.")
    json.dump({"all_p": float(p), "real_gap": float(real_gap)},
              io.open(os.path.join(HERE, "crosslang_result.json"), "w"), indent=1)
    print("saved crosslang_result.json")


if __name__ == "__main__":
    main()
