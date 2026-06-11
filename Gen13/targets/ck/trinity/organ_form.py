"""organ_form.py -- TRINITY organ 1: FORM (edit-robust addressing).

Head-to-head, same protocol, winner takes the seat:
  BRAID        : CK's Burau + abelianized fused signature (ours)
  VSA-position : hyperdimensional position-bundling (Kanerva school) --
                 word = sum_i roll(L[c_i], i), bipolar D=2048
  VSA-trigram  : classic HDC text encoding -- word = sum over trigrams of
                 L[a] * roll(L[b],1) * roll(L[c],2)

Protocol (identical to braid_resonance Part A): store 600 dictionary
words; query with 1-edit perturbations (substitute / swap / delete);
top-1 / top-5 recall; chance = 1/600 = 0.17%.

REGISTERED (before run): VSA-position should win substitutions (positions
independent), braid should keep its swap edge (abelianized invariance is
EXACT under swaps), trigram should be best on deletions. Winner overall
takes the organ; per-type strengths recorded for a possible hybrid.

  python organ_form.py
"""
import io
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.join(HERE, "..", "extraction")
sys.path.insert(0, EXT)
import braid_memory as bm                                  # noqa: E402

RNG = np.random.default_rng(3)
D = 2048                                   # hypervector dim (field standard)
ALPHA = "abcdefghijklmnopqrstuvwxyz"
LETTER_HV = {c: RNG.choice([-1.0, 1.0], size=D) for c in ALPHA}


def vsa_position(word):
    v = np.zeros(D)
    for i, c in enumerate(word):
        v += np.roll(LETTER_HV[c], i)      # permutation encodes position
    return v


def vsa_trigram(word):
    s = "#" + word + "#"
    hv = {**LETTER_HV, "#": RNG.choice([-1.0, 1.0], size=D)}
    # note: '#' hv fixed once per call site -- make deterministic:
    return _vsa_trigram(s)


_PAD = RNG.choice([-1.0, 1.0], size=D)
_HV = dict(LETTER_HV)
_HV["#"] = _PAD


def _vsa_trigram(s):
    v = np.zeros(D)
    for i in range(len(s) - 2):
        a, b, c = s[i], s[i + 1], s[i + 2]
        v += _HV[a] * np.roll(_HV[b], 1) * np.roll(_HV[c], 2)
    return v


def perturb(w, kind, rng):
    i = int(rng.integers(0, len(w)))
    if kind == "sub":
        repl = ALPHA[int(rng.integers(0, 26))]
        return w[:i] + repl + w[i + 1:]
    if kind == "swap":
        if len(w) < 2:
            return w
        i = int(rng.integers(0, len(w) - 1))
        return w[:i] + w[i + 1] + w[i] + w[i + 2:]
    if len(w) < 4:
        return w
    return w[:i] + w[i + 1:]               # del


def topk_recall(store_vecs, words, queries, q_vecs, k=5):
    S = np.array(store_vecs)
    S = S / (np.linalg.norm(S, axis=1, keepdims=True) + 1e-9)
    t1 = t5 = 0
    for (orig, qv) in zip(queries, q_vecs):
        q = qv / (np.linalg.norm(qv) + 1e-9)
        sims = S @ q
        order = np.argsort(-sims)
        if words[order[0]] == orig:
            t1 += 1
        if orig in [words[j] for j in order[:k]]:
            t5 += 1
    return t1 / len(queries), t5 / len(queries)


def main():
    flat = json.load(io.open(os.path.join(EXT, "ck_dictionary.json"),
                             encoding="utf-8"))["flat"]
    words = [w for w in flat if w.isalpha() and 5 <= len(w) <= 12]
    words = [words[i] for i in RNG.permutation(len(words))[:600]]

    encoders = {
        "BRAID (ours)": lambda w: np.concatenate(
            [bm.abelianized_key(w), bm.braid_signature(w)]),
        "VSA-position": vsa_position,
        "VSA-trigram": _vsa_trigram,
    }
    print("TRINITY ORGAN 1 -- FORM: braid vs the VSA/HDC field "
          f"(600 words, 1-edit queries, chance 0.17%)\n")
    results = {}
    qrng = np.random.default_rng(5)
    queries = {kind: [(w, perturb(w, kind, qrng)) for w in words[:300]]
               for kind in ("sub", "swap", "del")}

    for name, enc in encoders.items():
        store = [enc(w) for w in words]
        # whiten like BraidMemory does (remove common cone) -- same favor
        # to every encoder
        S = np.array(store)
        mu, sd = S.mean(0), S.std(0) + 1e-9
        store_w = [(v - mu) / sd for v in store]
        per = {}
        for kind, qs in queries.items():
            qv = [(enc(q) - mu) / sd for _, q in qs]
            t1, t5 = topk_recall(store_w, words, [w for w, _ in qs], qv)
            per[kind] = (t1, t5)
        mean1 = float(np.mean([per[k][0] for k in per]))
        results[name] = dict(per={k: [float(a), float(b)]
                                  for k, (a, b) in per.items()},
                             mean_top1=mean1)
        print(f"{name:>14}: " + "  ".join(
            f"{k} {per[k][0]:4.0%}/{per[k][1]:4.0%}" for k in
            ("sub", "swap", "del")) + f"   MEAN top-1 {mean1:.0%}")

    winner = max(results, key=lambda k: results[k]["mean_top1"])
    print(f"\nWINNER (organ seat): {winner} "
          f"({results[winner]['mean_top1']:.0%} mean top-1)")
    per_type = {k: max(results, key=lambda n: results[n]["per"][k][0])
                for k in ("sub", "swap", "del")}
    print("per-edit-type winners:", per_type)
    json.dump(results, io.open(os.path.join(HERE, "organ_form_result.json"),
                               "w"), indent=1)


if __name__ == "__main__":
    main()
