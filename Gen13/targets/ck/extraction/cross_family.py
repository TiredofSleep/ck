"""cross_family.py -- THE decisive test: is the geometry of information a
real PRE-LANGUAGE substrate?

Last session's cross-language p=0.006 was Indo-European Latin-script only,
where shared etymology could drive it. The real test of "pre-language":
does a concept's FORM-geometry survive across UNRELATED language families
(no shared roots) AND beat a dumb string-similarity baseline?

  8 languages, 5 unrelated families:
    Indo-European : en es de
    Uralic        : fi hu
    Turkic        : tr
    Niger-Congo   : sw (Swahili)
    Austronesian  : id (Indonesian)

  Decisive statistic: CROSS-FAMILY-ONLY concept-cluster gap -- within-
  concept similarity vs between-concept similarity, counting ONLY pairs
  whose languages are in DIFFERENT families (same-family pairs excluded,
  so cognates cannot help). Permutation p-value + two baselines:
    SHUFFLE (concept labels permuted) -- the null floor
    CHAR-TRIGRAM (bag of character 3-grams) -- "is the braid just string
      overlap?" If braid > char-trigram cross-family, the braid sees FORM
      beyond surface letters = pre-language geometry.

  KILL CRITERION: if the cross-family braid gap is at chance (p>0.05) OR
  not above the char-trigram baseline, the pre-language claim is an
  artifact -- honest negative, stated.

Translations are best-effort; errors add noise (work AGAINST finding an
effect) so the test is conservative.

  python cross_family.py
"""
import io
import json
import os
import unicodedata

import numpy as np

import braid_memory as bm

HERE = os.path.dirname(os.path.abspath(__file__))
RNG = np.random.default_rng(17)

FAMILY = {"en": "IE", "es": "IE", "de": "IE", "fi": "Ural", "hu": "Ural",
          "tr": "Turk", "sw": "Bantu", "id": "Austro"}
LANGS = list(FAMILY)

CONCEPTS = {
 "water":  dict(en="water", es="agua", de="wasser", fi="vesi", hu="viz",
                tr="su", sw="maji", id="air"),
 "fire":   dict(en="fire", es="fuego", de="feuer", fi="tuli", hu="tuz",
                tr="ates", sw="moto", id="api"),
 "mother": dict(en="mother", es="madre", de="mutter", fi="aiti", hu="anya",
                tr="anne", sw="mama", id="ibu"),
 "sun":    dict(en="sun", es="sol", de="sonne", fi="aurinko", hu="nap",
                tr="gunes", sw="jua", id="matahari"),
 "night":  dict(en="night", es="noche", de="nacht", fi="yo", hu="ej",
                tr="gece", sw="usiku", id="malam"),
 "eye":    dict(en="eye", es="ojo", de="auge", fi="silma", hu="szem",
                tr="goz", sw="jicho", id="mata"),
 "house":  dict(en="house", es="casa", de="haus", fi="talo", hu="haz",
                tr="ev", sw="nyumba", id="rumah"),
 "dog":    dict(en="dog", es="perro", de="hund", fi="koira", hu="kutya",
                tr="kopek", sw="mbwa", id="anjing"),
 "tree":   dict(en="tree", es="arbol", de="baum", fi="puu", hu="fa",
                tr="agac", sw="mti", id="pohon"),
 "hand":   dict(en="hand", es="mano", de="hand", fi="kasi", hu="kez",
                tr="el", sw="mkono", id="tangan"),
 "big":    dict(en="big", es="grande", de="gross", fi="iso", hu="nagy",
                tr="buyuk", sw="kubwa", id="besar"),
 "fish":   dict(en="fish", es="pez", de="fisch", fi="kala", hu="hal",
                tr="balik", sw="samaki", id="ikan"),
}


def deaccent(w):
    return "".join(c for c in unicodedata.normalize("NFKD", w.lower())
                   if not unicodedata.combining(c) and c.isalpha())


def whiten(M):
    M = (M - M.mean(0)) / (M.std(0) + 1e-9)
    return M / (np.linalg.norm(M, axis=1, keepdims=True) + 1e-9)


def char_trigrams(words):
    vocab = {}
    for w in words:
        s = "##" + w + "##"
        for i in range(len(s) - 2):
            vocab.setdefault(s[i:i + 3], len(vocab))
    M = np.zeros((len(words), len(vocab)))
    for r, w in enumerate(words):
        s = "##" + w + "##"
        for i in range(len(s) - 2):
            M[r, vocab[s[i:i + 3]]] += 1.0
    return M


def build():
    rows, concept, lang = [], [], []
    for c in CONCEPTS:
        for lg in LANGS:
            rows.append(deaccent(CONCEPTS[c][lg]))
            concept.append(c); lang.append(lg)
    return rows, np.array(concept), np.array(lang)


def crossfam_gap(S, concept, lang, labels=None):
    """within-concept minus between-concept similarity, CROSS-FAMILY pairs
    only (same-family pairs masked out)."""
    if labels is None:
        labels = concept
    fam = np.array([FAMILY[l] for l in lang])
    n = len(labels)
    gaps = []
    for i in range(n):
        crossfam = (fam != fam[i])
        same = crossfam & (labels == labels[i])
        diff = crossfam & (labels != labels[i])
        if same.any() and diff.any():
            gaps.append(S[i, same].mean() - S[i, diff].mean())
    return float(np.mean(gaps))


def perm_p(S, concept, lang, real, n=1000):
    cnt = 0
    for _ in range(n):
        pl = concept[RNG.permutation(len(concept))]
        if crossfam_gap(S, concept, lang, pl) >= real:
            cnt += 1
    return (cnt + 1) / (n + 1)


def crossfam_retrieval(S, concept, lang):
    """for each word, nearest CROSS-FAMILY word -- is it the same concept?"""
    fam = np.array([FAMILY[l] for l in lang])
    t1 = t3 = tot = 0
    for i in range(len(concept)):
        cand = [j for j in range(len(concept))
                if fam[j] != fam[i]]
        cand.sort(key=lambda j: -S[i, j])
        tot += 1
        if concept[cand[0]] == concept[i]:
            t1 += 1
        if concept[i] in concept[cand[:3]]:
            t3 += 1
    return t1 / tot, t3 / tot


def main():
    rows, concept, lang = build()
    nC = len(CONCEPTS)
    print("=" * 68)
    print("PRE-LANGUAGE GEOMETRY TEST -- concept form across UNRELATED "
          "families")
    print("=" * 68)
    print(f"{nC} concepts x {len(LANGS)} languages, {len(set(FAMILY.values()))}"
          f" families (IE/Uralic/Turkic/Bantu/Austronesian)")
    print("decisive stat: CROSS-FAMILY-only concept clustering "
          "(same-family pairs excluded -> cognates cannot help)\n")

    # three representations
    reps = {
        "braid (1 root)":  np.array([bm.braid_signature(w) for w in rows]),
        "braid (4 roots)": np.array([bm.braid_signature_rich(w) for w in rows]),
        "char-trigram":    char_trigrams(rows),
    }
    # CONTROL: does a borrowed embedding capture cross-family concept
    # clustering where the braid can't? Tells us if the signal exists at
    # all offline (CK-fails) vs the task is impossible here (everyone-fails).
    try:
        from borrowed_cortex import embed as bce
        E, backend = bce(["search_document: " + w for w in rows])
        reps[f"borrowed({backend.split(':')[1][:6]})"] = E
    except Exception:
        pass
    results = {}
    for name, M in reps.items():
        W = whiten(M)
        S = W @ W.T
        gap = crossfam_gap(S, concept, lang)
        p = perm_p(S, concept, lang, gap)
        t1, t3 = crossfam_retrieval(S, concept, lang)
        results[name] = dict(gap=gap, p=p, top1=t1, top3=t3)
        print(f"{name:>16}:  cross-family gap {gap:+.4f}  p={p:.3f}   "
              f"retrieval top1 {t1:.0%} top3 {t3:.0%}  (chance {1/nC:.0%})")

    braid = results["braid (4 roots)"]
    char = results["char-trigram"]
    print("\n" + "-" * 68)
    real_signal = braid["p"] < 0.05
    beats_string = braid["gap"] > char["gap"] + 0.005
    multiroot_helps = (results["braid (4 roots)"]["gap"]
                       > results["braid (1 root)"]["gap"])
    print(f"cross-family signal present (braid p<0.05): {real_signal}")
    print(f"braid beats char-trigram (sees FORM, not letters): {beats_string}"
          f"  (braid {braid['gap']:+.4f} vs char {char['gap']:+.4f})")
    print(f"more measurements help (4 roots > 1 root): {multiroot_helps}")

    if real_signal and beats_string:
        verdict = ("PRE-LANGUAGE GEOMETRY: SUPPORTED -- concept form "
                   "survives across unrelated families AND beats string "
                   "overlap.")
    elif real_signal:
        verdict = ("PARTIAL -- cross-family signal exists but does not "
                   "clearly beat char-trigram; may be residual sound/string "
                   "structure, not pre-language geometry.")
    else:
        verdict = ("HONEST NEGATIVE -- no cross-family signal; the prior "
                   "Indo-European result was shared etymology, not "
                   "pre-language geometry.")
    print(f"\nVERDICT: {verdict}")
    print("scope: 8 languages, best-effort translations (errors are "
          "conservative); Latin/transliterated only. Bigger test = more "
          "languages, native scripts via codepoint-ruler atoms.")

    json.dump(results, io.open(os.path.join(HERE, "crossfam_result.json"),
                               "w"), indent=1)
    print("saved crossfam_result.json")


if __name__ == "__main__":
    main()
