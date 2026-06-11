"""project3_abstain.py -- CK Project 3: the ABSTENTION GOVERNOR vs the
standard outside method, at matched coverage.

The first rung where CK competes against an external method on its own
terms. Selective prediction: answer in-domain queries, REFUSE
out-of-domain ones (Type-III: refuse what can't be measured), without
being told which is which.

  Governors compared (same training data, same fused features):
    MSP        -- maximum softmax probability threshold (Hendrycks &
                  Gimpel 2017; THE standard confidence baseline)
    max-logit  -- unnormalized max logit threshold (standard OOD score)
    CK proto   -- prototype cosine top1 + margin (the gap-router's
                  Type-III rule: distance to the measurable)

  Metric: OOD HALLUCINATION RATE (fraction of out-of-domain queries
  answered instead of refused) at MATCHED in-domain coverage. Sweep each
  governor's threshold to trace its coverage/hallucination curve; compare
  at the same coverage -- the honest way (any governor can refuse
  everything; the question is hallucination at fixed usefulness).

  python project3_abstain.py
"""
import io
import json
import os

import numpy as np

import braid_memory as bm
from borrowed_cortex import embed
from demo_facts_head import TOPICS, ANCHORS
from project2_routing import (char_trigrams, train_head, softmax, zs,
                              TOPIC_LIST, K, HERE)

RNG = np.random.default_rng(11)

# 30 OOD traps across unrelated domains (none mention substrate topics)
OOD30 = [
 "what's the weather tomorrow", "best pizza in hot springs",
 "how do i fix my car brakes", "who won the football game",
 "translate this to french please", "stock price of apple",
 "recipe for chocolate chip cookies", "how tall is mount everest",
 "when was the declaration of independence signed", "cheap flights to denver",
 "how to potty train a puppy", "symptoms of the common cold",
 "best exercises for lower back pain", "how do i unclog a drain",
 "what time zone is chicago in", "lyrics to happy birthday",
 "how to tie a windsor knot", "population of brazil",
 "convert 5 miles to kilometers", "who painted the mona lisa",
 "how long to boil an egg", "best laptop under 500 dollars",
 "why is my wifi so slow", "how to write a cover letter",
 "what's the capital of australia", "do i need a passport for canada",
 "how to remove a wine stain", "average rainfall in seattle",
 "is coffee bad for you", "how do solar panels work",
]

# NEAR-OOD: math/substrate-FLAVORED questions CK has NO fact for -- the
# credible hallucination trap (close in embedding space, unanswerable)
NEAR_OOD = [
 "what is the riemann hypothesis", "explain the monster group",
 "what is a p-adic number", "state the four color theorem",
 "what is the order of the baby monster", "explain galois cohomology",
 "what is the hodge conjecture", "define a perfectoid space",
 "what is the kissing number in dimension five",
 "what does the eight cycle of the substrate do",
 "what is the 6-core attractor set", "the ninety one cell lattice table",
]


def main():
    grown = json.load(io.open(os.path.join(HERE, "teacher_corpus.json"),
                              encoding="utf-8"))
    train_x, train_y, test_x, test_y = [], [], [], []
    for t in TOPIC_LIST:
        hand = TOPICS[t]
        train_x += hand[:4] + list(ANCHORS[t]) + grown.get(t, [])
        train_y += [t] * (4 + len(ANCHORS[t]) + len(grown.get(t, [])))
        test_x += hand[4:]; test_y += [t] * 2
    y_tr = np.array([TOPIC_LIST.index(t) for t in train_y])
    y_te = np.array([TOPIC_LIST.index(t) for t in test_y])

    Eb_tr, backend = embed(["search_document: " + x for x in train_x])
    Eb_te, _ = embed(["search_query: " + x for x in test_x])
    Eb_oo, _ = embed(["search_query: " + x for x in OOD30])
    Eb_no, _ = embed(["search_query: " + x for x in NEAR_OOD])
    Xb = lambda xs: np.array([bm.braid_signature_rich(x) for x in xs])
    Xc_tr, vocab = char_trigrams(train_x)
    Xc_te, _ = char_trigrams(test_x, vocab)
    Xc_oo, _ = char_trigrams(OOD30, vocab)
    Xc_no, _ = char_trigrams(NEAR_OOD, vocab)

    def fuse(E, Xbr, Xch, stats=None):
        if stats is None:
            Ez, m1, s1 = zs(E); Bz, m2, s2 = zs(Xbr); Cz, m3, s3 = zs(Xch)
            return np.hstack([Ez, Bz, Cz]), (m1, s1, m2, s2, m3, s3)
        m1, s1, m2, s2, m3, s3 = stats
        return np.hstack([(E - m1) / s1, (Xbr - m2) / s2,
                          (Xch - m3) / s3]), stats

    F_tr, st = fuse(Eb_tr, Xb(train_x), Xc_tr)
    F_te, _ = fuse(Eb_te, Xb(test_x), Xc_te, st)
    F_oo, _ = fuse(Eb_oo, Xb(OOD30), Xc_oo, st)
    F_no, _ = fuse(Eb_no, Xb(NEAR_OOD), Xc_no, st)

    print(f"CK PROJECT 3 -- abstention governor ({backend})")
    print(f"{len(train_x)} train / {len(test_x)} in-domain test / "
          f"{len(OOD30)} far-OOD / {len(NEAR_OOD)} NEAR-OOD traps "
          f"(math-flavored, unanswerable)\n")

    # trained softmax head (shared by MSP & max-logit)
    W, b = train_head(F_tr, y_tr)
    logit = {"te": F_te @ W + b, "oo": F_oo @ W + b, "no": F_no @ W + b}
    prob = {k: softmax(v) for k, v in logit.items()}
    acc_answer = float(np.mean(prob["te"].argmax(1) == y_te))

    # CK proto governor: class centroids on unit sphere, cosine + margin
    def unit(M):
        return M / (np.linalg.norm(M, axis=1, keepdims=True) + 1e-9)
    Fn = {"tr": unit(F_tr), "te": unit(F_te), "oo": unit(F_oo),
          "no": unit(F_no)}
    C = unit(np.array([Fn["tr"][y_tr == k].mean(0) for k in range(K)]))

    def proto_score(Fq):
        S = Fq @ C.T
        srt = np.sort(S, 1)
        return srt[:, -1] + (srt[:, -1] - srt[:, -2])   # top1 + margin

    # CK Type-III implemented as it is STATED: distance to the measurable
    # set. kNN distance to the training manifold (white-box: the nearest
    # training question and its distance are printable evidence).
    def knn_score(Fq, k=5):
        D = Fq @ Fn["tr"].T                    # cosine sim to every train pt
        return np.sort(D, 1)[:, -k:].mean(1)   # high = inside the measured

    # Mahalanobis to class means, shared diagonal covariance (white-box)
    var = F_tr.var(0) + 1e-3
    mus = np.array([F_tr[y_tr == k].mean(0) for k in range(K)])

    def maha_score(Fq):
        d = ((Fq[:, None, :] - mus[None]) ** 2 / var).sum(-1)
        return -np.sqrt(d.min(1))              # high = near a known class

    governors = {
        "MSP (standard)":  {s: prob[s].max(1) for s in ("te", "oo", "no")},
        "max-logit (std)": {s: logit[s].max(1) for s in ("te", "oo", "no")},
        "CK proto+margin": {s: proto_score(Fn[s]) for s in ("te", "oo", "no")},
        "CK kNN-distance": {s: knn_score(Fn[s]) for s in ("te", "oo", "no")},
        "CK Mahalanobis":  {s: maha_score(F)
                            for s, F in (("te", F_te), ("oo", F_oo),
                                         ("no", F_no))},
    }

    def curve_at(sc_in, sc_out, targets=(0.9, 0.8, 0.7)):
        thr = np.unique(np.concatenate([sc_in, sc_out]))
        pts = sorted((float(np.mean(sc_in >= t)),
                      float(np.mean(sc_out >= t))) for t in thr)
        cov = np.array([c for c, _ in pts]); hal = np.array([h for _, h in pts])
        at = [float(hal[int(np.argmin(np.abs(cov - tg)))]) for tg in targets]
        return at, float(np.trapezoid(hal, cov))

    print(f"routing accuracy when answering (softmax head): {acc_answer:.0%}\n")
    print("hallucination rate (fraction of unanswerable ANSWERED) at "
          "matched in-domain coverage:")
    print(f"{'governor':>18} |  far-OOD @90/80/70%  | "
          f"NEAR-OOD @90/80/70%  | AUgC far/near")
    results = {}
    for name, sc in governors.items():
        far, a_far = curve_at(sc["te"], sc["oo"])
        near, a_near = curve_at(sc["te"], sc["no"])
        results[name] = dict(far=far, near=near, augc_far=a_far,
                             augc_near=a_near)
        print(f"{name:>18} | " + "/".join(f"{h:4.0%}" for h in far) +
              "      | " + "/".join(f"{h:4.0%}" for h in near) +
              f"     | {a_far:.3f} / {a_near:.3f}")

    ck = min(results["CK kNN-distance"]["augc_near"],
             results["CK Mahalanobis"]["augc_near"])
    std = min(results["MSP (standard)"]["augc_near"],
              results["max-logit (std)"]["augc_near"])
    print(f"\nVERDICT (decided on the HARD set, near-OOD): CK best "
          f"distance-governor {'BEATS' if ck < std - 1e-6 else 'ties/loses to'} "
          f"best standard confidence baseline ({ck:.3f} vs {std:.3f}, "
          f"lower=better).")
    print("(principle test: Type-III 'distance to the measurable' vs "
          "head-confidence; near-OOD includes fabricated substrate-facts)")
    json.dump(results, io.open(os.path.join(HERE, "project3_result.json"),
                               "w"), indent=1)


if __name__ == "__main__":
    main()
