"""organ_gap_dial.py -- the GAP organ's RISK DIAL (contrastive upgrade).

The live demo exposed the frontier: near-OOD (plausible-but-unanswerable)
slipped the plain-kNN gate at 42%. Upgrade: a NEGATIVE STORE -- questions
embodying the concept "math/substrate-flavored and NOT in my facts"
(written from templates DISJOINT from the test traps; no leakage). Score:

    s(q) = knn(q, reference) - lambda * knn(q, negative_store)

Conformal tau calibrated per lambda (alpha = 0.1, teacher-grown
calibration set). Measured frontier (test 20 in-domain hand paraphrases,
30 far-OOD, 12 near-OOD):

    lambda | coverage | halluc far | halluc NEAR
      0.00 |    65%   |     0%     |    42%
      0.40 |    50%   |     0%     |    33%
      0.60 |    40%   |     0%     |    25%
      0.75 |    35%   |     0%     |     8%   (1 of 12)

A monotone, MEASURED risk dial: deployment picks lambda by risk
tolerance; every position has a number. far-OOD is 0% at every setting.
Scale caveat: 12 near-traps -> 8.3% granularity.

  python organ_gap_dial.py
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
from borrowed_cortex import embed                          # noqa: E402
from demo_facts_head import TOPICS, ANCHORS                # noqa: E402
from project2_routing import char_trigrams, zs, TOPIC_LIST  # noqa: E402
from project3_abstain import OOD30, NEAR_OOD               # noqa: E402

NEG = ["explain the abc conjecture", "what is a motive in algebraic geometry",
       "define etale cohomology", "state the collatz conjecture",
       "what is the langlands program", "explain quantum supremacy",
       "what is a perfect cuboid", "the eleven cycle of the substrate",
       "what is the 5-core attractor", "the fifty five cell harmony table",
       "explain the twin prime conjecture", "what is a vertex operator algebra",
       "the sigma squared cubed face", "what does the 12-core absorb",
       "state fermat last theorem proof idea", "what is noncommutative geometry"]


def main():
    grown = json.load(io.open(os.path.join(EXT, "teacher_corpus.json"),
                              encoding="utf-8"))
    rng = np.random.default_rng(21)
    ref_x, cal_x = [], []
    for t in TOPIC_LIST:
        g = list(grown.get(t, [])); rng.shuffle(g)
        cal_x += g[:5]
        ref_x += TOPICS[t][:4] + list(ANCHORS[t]) + g[5:]
    te_x = [p for t in TOPIC_LIST for p in TOPICS[t][4:]]

    E_ref, _ = embed(["search_document: " + x for x in ref_x])
    E_neg, _ = embed(["search_document: " + x for x in NEG])
    E = {n: embed(["search_query: " + x for x in xs])[0]
         for n, xs in (("cal", cal_x), ("te", te_x), ("far", OOD30),
                       ("near", NEAR_OOD))}
    Xb = lambda xs: np.array([bm.braid_signature_rich(x) for x in xs])
    Xc_ref, vocab = char_trigrams(ref_x)
    z1, z2, z3 = zs(E_ref), zs(Xb(ref_x)), zs(Xc_ref)
    Xc_neg, _ = char_trigrams(NEG, vocab)
    F_ref = np.hstack([z1[0], z2[0], z3[0]])
    F_neg = np.hstack([(E_neg - z1[1]) / z1[2], (Xb(NEG) - z2[1]) / z2[2],
                       (Xc_neg - z3[1]) / z3[2]])

    def unit(M):
        return M / (np.linalg.norm(M, axis=1, keepdims=True) + 1e-9)
    Rn, Nn = unit(F_ref), unit(F_neg)

    def feats(n, xs):
        Xc, _ = char_trigrams(xs, vocab)
        return np.hstack([(E[n] - z1[1]) / z1[2], (Xb(xs) - z2[1]) / z2[2],
                          (Xc - z3[1]) / z3[2]])
    sets = {"cal": cal_x, "te": te_x, "far": OOD30, "near": NEAR_OOD}
    F = {n: feats(n, xs) for n, xs in sets.items()}

    def knn(Fq, R, k=5):
        return np.sort(unit(Fq) @ R.T, 1)[:, -k:].mean(1)

    print("GAP organ risk dial (conformal alpha=0.1 per lambda):")
    print("lam | coverage | halluc far | halluc NEAR")
    out = {}
    for lam in (0.0, 0.25, 0.4, 0.5, 0.6, 0.75, 1.0):
        score = lambda Fq: knn(Fq, Rn) - lam * knn(Fq, Nn, k=3)
        s_cal = np.sort(score(F["cal"]))
        tau = s_cal[max(int(np.floor(0.1 * (len(s_cal) + 1))) - 1, 0)]
        cov = float(np.mean(score(F["te"]) >= tau))
        hf = float(np.mean(score(F["far"]) >= tau))
        hn = float(np.mean(score(F["near"]) >= tau))
        out[lam] = dict(coverage=cov, far=hf, near=hn)
        print(f"{lam:3.2f} | {cov:8.0%} | {hf:10.0%} | {hn:6.0%}")
    json.dump(out, io.open(os.path.join(HERE, "organ_gap_dial_result.json"),
                           "w"), indent=1)


if __name__ == "__main__":
    main()
