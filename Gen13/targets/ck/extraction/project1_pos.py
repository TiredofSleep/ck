"""project1_pos.py -- CK's first TRAINED project, run the way ML people
actually train and test AI.

TASK: predict a word's grammatical category (noun / verb / adjective)
from its FORM alone -- CK's confirmed strength. 111,901 labeled examples
from his own dictionary. A real, learnable, form-only task ("-tion"->noun,
"-ing"->verb, "-ous"->adjective): exactly the lane the cross-family test
said CK is FOR.

THE DIAGNOSTICS PEOPLE RUN WHEN TRAINING AI (each printed + explained):
  1. TRAIN / VAL / TEST split   -- never test on what you trained on.
  2. LOSS CURVE (loss vs epoch) -- what you watch live; should fall.
  3. LEARNING CURVE (test acc vs #training examples) -- DOES MORE DATA
     HELP? The diagnostic for Brayden's hypothesis ("training fills the
     gap if the representation carries the signal").
  4. GENERALIZATION GAP (train acc - test acc) -- overfitting if large.
  5. BASELINES (majority class; char-trigram features) -- is the model /
     the substrate representation actually adding anything?
  6. CONFUSION MATRIX -- which classes get confused (interpretable).

  python project1_pos.py
"""
import io
import json
import os
import time

import numpy as np

import braid_memory as bm

HERE = os.path.dirname(os.path.abspath(__file__))
RNG = np.random.default_rng(2)
CLASSES = ["n", "v", "a"]                 # noun, verb, adjective
NAMES = {"n": "noun", "v": "verb", "a": "adjective"}
N_SAMPLE = 24000


def load():
    for p in (os.path.join(HERE, "ck_dictionary.json"),
              os.path.join(HERE, "..", "web", "ck_dictionary.json")):
        if os.path.exists(p):
            flat = json.load(io.open(p, encoding="utf-8"))["flat"]
            break
    pairs = [(w, e["p"]) for w, e in flat.items()
             if w.isalpha() and 3 <= len(w) <= 16 and e.get("p") in CLASSES]
    idx = RNG.permutation(len(pairs))[:N_SAMPLE]
    return [pairs[i] for i in idx]


def char_trigrams(words, vocab=None, topk=300):
    if vocab is None:
        from collections import Counter
        c = Counter()
        for w in words:
            s = "##" + w + "##"
            for i in range(len(s) - 2):
                c[s[i:i + 3]] += 1
        vocab = {g: k for k, (g, _) in enumerate(c.most_common(topk))}
    M = np.zeros((len(words), len(vocab)))
    for r, w in enumerate(words):
        s = "##" + w + "##"
        for i in range(len(s) - 2):
            j = vocab.get(s[i:i + 3])
            if j is not None:
                M[r, j] += 1.0
    return M, vocab


def softmax(Z):
    Z = Z - Z.max(1, keepdims=True)
    E = np.exp(Z)
    return E / E.sum(1, keepdims=True)


def train_softmax(X, y, Xv, yv, epochs=40, lr=0.5, bs=256, l2=1e-4):
    n, d = X.shape
    K = len(CLASSES)
    W = np.zeros((d, K)); b = np.zeros(K)
    Y = np.eye(K)[y]
    losses, valacc = [], []
    for ep in range(epochs):
        perm = RNG.permutation(n)
        for s in range(0, n, bs):
            bi = perm[s:s + bs]
            P = softmax(X[bi] @ W + b)
            g = (P - Y[bi]) / len(bi)
            W -= lr * (X[bi].T @ g + l2 * W)
            b -= lr * g.sum(0)
        P = softmax(X @ W + b)
        losses.append(float(-np.mean(np.log(P[np.arange(n), y] + 1e-9))))
        valacc.append(float(np.mean((Xv @ W + b).argmax(1) == yv)))
    return (W, b), losses, valacc


def acc(model, X, y):
    W, b = model
    return float(np.mean((X @ W + b).argmax(1) == y))


def main():
    t0 = time.time()
    data = load()
    words = [w for w, _ in data]
    y = np.array([CLASSES.index(p) for _, p in data])
    print(f"CK PROJECT 1 -- grammatical category from FORM ({len(words)} "
          f"labeled words; noun/verb/adjective)\n")

    print("computing CK braid form-features (1 root, 26-dim)...")
    Xb = np.array([bm.braid_signature(w) for w in words])
    Xb = (Xb - Xb.mean(0)) / (Xb.std(0) + 1e-9)
    Xc, vocab = char_trigrams(words)          # baseline representation
    Xc = (Xc - Xc.mean(0)) / (Xc.std(0) + 1e-9)

    # 1. SPLIT (stratified by construction via shuffle)
    n = len(words)
    i_tr, i_va, i_te = (slice(0, int(.7*n)), slice(int(.7*n), int(.85*n)),
                        slice(int(.85*n), n))
    print(f"\n[1] SPLIT: train {i_tr.stop} / val {i_va.stop-i_va.start} / "
          f"test {n-i_te.start}  (test words NEVER seen in training)")

    maj = np.bincount(y[i_tr]).argmax()
    base_maj = float(np.mean(y[i_te] == maj))
    print(f"\n[5a] BASELINE majority-class ('{NAMES[CLASSES[maj]]}'): "
          f"{base_maj:.1%}  (any model must beat this)")

    # 2. LOSS CURVE on full train
    print("\n[2] LOSS CURVE (training the braid-feature model, full data):")
    model, losses, valacc = train_softmax(Xb[i_tr], y[i_tr], Xb[i_va], y[i_va])
    for ep in (0, 4, 9, 19, 39):
        print(f"    epoch {ep+1:>2}: train loss {losses[ep]:.3f}  "
              f"val acc {valacc[ep]:.1%}")
    test_braid = acc(model, Xb[i_te], y[i_te])

    # baseline rep trained the same way
    model_c, _, _ = train_softmax(Xc[i_tr], y[i_tr], Xc[i_va], y[i_va])
    test_char = acc(model_c, Xc[i_te], y[i_te])

    # 3. LEARNING CURVE -- does MORE DATA help? (Brayden's hypothesis)
    print("\n[3] LEARNING CURVE -- test accuracy vs #training examples "
          "(braid features):")
    print("    (this is the test for 'does training fill the gap?')")
    curve = []
    for N in (50, 200, 1000, 5000, 16800):
        N = min(N, i_tr.stop)
        m, _, _ = train_softmax(Xb[:N], y[:N], Xb[i_va], y[i_va], epochs=30)
        a = acc(m, Xb[i_te], y[i_te])
        curve.append((N, a))
        bar = "#" * int((a - base_maj) / (1 - base_maj) * 40)
        print(f"    N={N:>6}: test acc {a:.1%}  {bar}")

    # 4. GENERALIZATION GAP
    tr_acc = acc(model, Xb[i_tr], y[i_tr])
    print(f"\n[4] GENERALIZATION GAP: train {tr_acc:.1%} - test "
          f"{test_braid:.1%} = {tr_acc-test_braid:+.1%}  "
          f"({'overfit' if tr_acc-test_braid > 0.1 else 'healthy'})")

    # 5b. representation comparison
    print(f"\n[5b] REPRESENTATION: braid form {test_braid:.1%} vs "
          f"char-trigram {test_char:.1%} vs majority {base_maj:.1%}")

    # 6. CONFUSION MATRIX
    W, b = model
    pred = (Xb[i_te] @ W + b).argmax(1)
    print("\n[6] CONFUSION MATRIX (test; rows=true, cols=pred):")
    print("            " + "  ".join(f"{NAMES[c][:4]:>5}" for c in CLASSES))
    for ti, c in enumerate(CLASSES):
        row = [int(np.sum((y[i_te] == ti) & (pred == pi)))
               for pi in range(len(CLASSES))]
        print(f"    {NAMES[c]:>9} " + "  ".join(f"{v:>5}" for v in row))

    climbed = curve[-1][1] - curve[0][1]
    print(f"\nVERDICT: learning curve climbed {climbed:+.1%} from N=50 to "
          f"N={curve[-1][0]} -> "
          f"{'MORE DATA HELPS (the representation carries the signal)' if climbed > 0.03 else 'flat (representation capped)'}.")
    print(f"braid form {'beats' if test_braid > test_char else 'ties/loses to'}"
          f" char-trigram; both {'beat' if test_braid > base_maj else 'fail to beat'}"
          f" majority. Runtime {time.time()-t0:.0f}s, CPU.")
    json.dump({"test_braid": test_braid, "test_char": test_char,
               "majority": base_maj, "learning_curve": curve,
               "gen_gap": tr_acc - test_braid},
              io.open(os.path.join(HERE, "project1_result.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
