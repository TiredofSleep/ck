"""project2_routing.py -- CK Project 2: topic routing, trained properly.

Spawn v1's frozen proto-head routed held-out paraphrases at 50%. Project 2
asks: with a TRAINED head over FUSED representations (braid identity +
char morphology + borrowed meaning) and the teacher-grown corpus as
training data, does the learning curve climb past it?

Same held-out test as demo_facts_head.py (last 2 hand paraphrases per
topic, never trained on), so numbers are comparable.

  python project2_routing.py
"""
import io
import json
import os
import time

import numpy as np

import braid_memory as bm
from borrowed_cortex import embed
from demo_facts_head import TOPICS, ANCHORS, OOD, keyword_route

HERE = os.path.dirname(os.path.abspath(__file__))
RNG = np.random.default_rng(7)
TOPIC_LIST = sorted(TOPICS)
K = len(TOPIC_LIST)


def char_trigrams(texts, vocab=None, topk=600):
    if vocab is None:
        from collections import Counter
        c = Counter()
        for w in texts:
            s = "##" + w.lower() + "##"
            for i in range(len(s) - 2):
                c[s[i:i + 3]] += 1
        vocab = {g: k for k, (g, _) in enumerate(c.most_common(topk))}
    M = np.zeros((len(texts), len(vocab)))
    for r, w in enumerate(texts):
        s = "##" + w.lower() + "##"
        for i in range(len(s) - 2):
            j = vocab.get(s[i:i + 3])
            if j is not None:
                M[r, j] += 1.0
    return M, vocab


def softmax(Z):
    Z = Z - Z.max(1, keepdims=True)
    E = np.exp(Z)
    return E / E.sum(1, keepdims=True)


def train_head(X, y, epochs=120, lr=0.4, l2=1e-3):
    n, d = X.shape
    W = np.zeros((d, K)); b = np.zeros(K)
    Y = np.eye(K)[y]
    for ep in range(epochs):
        P = softmax(X @ W + b)
        g = (P - Y) / n
        W -= lr * (X.T @ g + l2 * W)
        b -= lr * g.sum(0)
    return W, b


def zs(M, mu=None, sd=None):
    if mu is None:
        mu, sd = M.mean(0), M.std(0) + 1e-9
    return (M - mu) / sd, mu, sd


def main():
    t0 = time.time()
    grown = json.load(io.open(os.path.join(HERE, "teacher_corpus.json"),
                              encoding="utf-8"))
    train_x, train_y, test_x, test_y = [], [], [], []
    for t in TOPIC_LIST:
        hand = TOPICS[t]
        train_x += hand[:4]; train_y += [t] * 4
        train_x += [a for a in ANCHORS[t]]; train_y += [t] * len(ANCHORS[t])
        train_x += grown.get(t, []); train_y += [t] * len(grown.get(t, []))
        test_x += hand[4:];  test_y += [t] * 2
    y_tr = np.array([TOPIC_LIST.index(t) for t in train_y])
    y_te = np.array([TOPIC_LIST.index(t) for t in test_y])
    print(f"CK PROJECT 2 -- topic routing: {len(train_x)} train "
          f"(hand+anchors+teacher-grown), {len(test_x)} held-out test, "
          f"{K} topics\n")

    # representations
    Eb_tr, backend = embed(["search_document: " + x for x in train_x])
    Eb_te, _ = embed(["search_query: " + x for x in test_x])
    print(f"borrowed cortex: {backend}")
    Xb_tr = np.array([bm.braid_signature_rich(x) for x in train_x])
    Xb_te = np.array([bm.braid_signature_rich(x) for x in test_x])
    Xc_tr, vocab = char_trigrams(train_x)
    Xc_te, _ = char_trigrams(test_x, vocab)

    reps = {}
    for name, (A, B) in {
            "braid": (Xb_tr, Xb_te), "char-trigram": (Xc_tr, Xc_te),
            "borrowed": (Eb_tr, Eb_te)}.items():
        Az, mu, sd = zs(A); Bz, _, _ = zs(B, mu, sd)
        reps[name] = (Az, Bz)
    reps["FUSED native (braid+char)"] = tuple(
        np.hstack([reps["braid"][i], reps["char-trigram"][i]]) for i in (0, 1))
    reps["FUSED all (+borrowed)"] = tuple(
        np.hstack([reps["FUSED native (braid+char)"][i], reps["borrowed"][i]])
        for i in (0, 1))

    kw = np.mean([keyword_route(q) == t for q, t in zip(test_x, test_y)])
    print(f"\nbaselines: majority {1/K:.0%} | keyword (production) {kw:.0%} | "
          f"spawn v1 frozen proto-head 50%\n")

    print("representation comparison (trained softmax head, full data):")
    accs = {}
    for name, (A, B) in reps.items():
        W, b = train_head(A, y_tr)
        a = float(np.mean((B @ W + b).argmax(1) == y_te))
        accs[name] = a
        print(f"  {name:>28}: held-out {a:.0%}")

    print("\nlearning curve (FUSED all): examples per topic vs held-out acc")
    A, B = reps["FUSED all (+borrowed)"]
    curve = []
    by_topic = {t: np.where(y_tr == TOPIC_LIST.index(t))[0] for t in TOPIC_LIST}
    for npt in (1, 2, 4, 8, 16, 25):
        idx = np.concatenate([by_topic[t][:npt] for t in TOPIC_LIST])
        W, b = train_head(A[idx], y_tr[idx])
        a = float(np.mean((B @ W + b).argmax(1) == y_te))
        curve.append((int(npt), a))
        print(f"  n/topic={npt:>2}: {a:.0%}  " + "#" * int(a * 40))

    best = max(accs.values())
    print(f"\nVERDICT: best trained head {best:.0%} vs spawn v1 50% vs "
          f"keyword {kw:.0%}; learning curve "
          f"{'CLIMBS' if curve[-1][1] > curve[0][1] + 0.05 else 'flat'}. "
          f"native-only (no borrowed) reaches "
          f"{accs['FUSED native (braid+char)']:.0%}. {time.time()-t0:.0f}s")
    json.dump({"accs": accs, "curve": curve, "keyword": float(kw)},
              io.open(os.path.join(HERE, "project2_result.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main()
