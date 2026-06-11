"""organ_gap.py -- TRINITY organ 2: GAP, with a conformal GUARANTEE.

Upgrade of Project 3 from threshold-sweep (optimistic) to split-conformal
calibration (Vovk; Angelopoulos & Bates): hold out calibration paraphrases
the reference set never sees; set the answer-threshold tau as the
floor(alpha*(n_cal+1))-th smallest calibration score. Exchangeability then
gives the finite-sample guarantee  P(answer | in-domain) >= 1 - alpha  --
no peeking, no sweep.

Then measure, at that FIXED tau: realized in-domain coverage (should be
>= 90%), routing accuracy when answering, and hallucination on far-OOD
(30 traps) and NEAR-OOD (12 math-flavored traps incl. fabricated
substrate-facts). Baseline: conformalized MSP -- same calibration set,
same guarantee, different score. Principle vs principle at equal rigor.

  python organ_gap.py
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
from project2_routing import (char_trigrams, train_head, softmax, zs,
                              TOPIC_LIST, K)               # noqa: E402
from project3_abstain import OOD30, NEAR_OOD               # noqa: E402

ALPHA = 0.10                              # target: >=90% in-domain coverage
N_CAL_PER_TOPIC = 5


def main():
    grown = json.load(io.open(os.path.join(EXT, "teacher_corpus.json"),
                              encoding="utf-8"))
    ref_x, ref_y, cal_x, cal_y, test_x, test_y = [], [], [], [], [], []
    rng = np.random.default_rng(21)
    for t in TOPIC_LIST:
        hand = TOPICS[t]
        g = list(grown.get(t, []))
        rng.shuffle(g)
        cal_x += g[:N_CAL_PER_TOPIC]; cal_y += [t] * len(g[:N_CAL_PER_TOPIC])
        rest = g[N_CAL_PER_TOPIC:]
        ref_x += hand[:4] + list(ANCHORS[t]) + rest
        ref_y += [t] * (4 + len(ANCHORS[t]) + len(rest))
        test_x += hand[4:]; test_y += [t] * 2
    y_ref = np.array([TOPIC_LIST.index(t) for t in ref_y])
    y_te = np.array([TOPIC_LIST.index(t) for t in test_y])

    E_ref, backend = embed(["search_document: " + x for x in ref_x])
    E = {n: embed(["search_query: " + x for x in xs])[0]
         for n, xs in (("cal", cal_x), ("te", test_x), ("far", OOD30),
                       ("near", NEAR_OOD))}
    Xc_ref, vocab = char_trigrams(ref_x)
    Xb = lambda xs: np.array([bm.braid_signature_rich(x) for x in xs])
    sets = {"cal": cal_x, "te": test_x, "far": OOD30, "near": NEAR_OOD}

    Ez, m1, s1 = zs(E_ref); Bz, m2, s2 = zs(Xb(ref_x))
    Cz, m3, s3 = zs(Xc_ref)
    F_ref = np.hstack([Ez, Bz, Cz])
    F = {}
    for n, xs in sets.items():
        Xc, _ = char_trigrams(xs, vocab)
        F[n] = np.hstack([(E[n] - m1) / s1, (Xb(xs) - m2) / s2,
                          (Xc - m3) / s3])

    print(f"TRINITY ORGAN 2 -- GAP with conformal guarantee ({backend})")
    print(f"reference {len(ref_x)} | calibration {len(cal_x)} "
          f"(never in reference) | test {len(test_x)} | far-OOD 30 | "
          f"near-OOD 12 | alpha={ALPHA} -> guaranteed coverage >= "
          f"{1-ALPHA:.0%}\n")

    # heads
    W, b = train_head(F_ref, y_ref)

    def unit(M):
        return M / (np.linalg.norm(M, axis=1, keepdims=True) + 1e-9)
    Fn_ref = unit(F_ref)

    def knn(Fq, k=5):
        return np.sort(unit(Fq) @ Fn_ref.T, 1)[:, -k:].mean(1)

    def msp(Fq):
        return softmax(Fq @ W + b).max(1)

    for name, score in (("CK kNN-distance", knn),
                        ("MSP (conformalized)", msp)):
        s_cal = np.sort(score(F["cal"]))
        j = int(np.floor(ALPHA * (len(s_cal) + 1))) - 1
        tau = s_cal[max(j, 0)]
        cov = float(np.mean(score(F["te"]) >= tau))
        ans = score(F["te"]) >= tau
        acc = float(np.mean((F["te"][ans] @ W + b).argmax(1) == y_te[ans])) \
            if ans.any() else float("nan")
        h_far = float(np.mean(score(F["far"]) >= tau))
        h_near = float(np.mean(score(F["near"]) >= tau))
        print(f"{name:>20}: tau={tau:.3f}  realized coverage {cov:.0%} "
              f"(guaranteed {1-ALPHA:.0%})")
        print(f"{'':>20}  acc-when-answering {acc:.0%} | hallucination: "
              f"far {h_far:.0%}  NEAR {h_near:.0%}")

    print("\n(identical guarantee machinery for both -- only the SCORE "
          "differs: distance-to-the-measured vs head-confidence)")


if __name__ == "__main__":
    main()
