"""resonance_test.py -- THE TEST of Brayden's intuition, on CK's real
112,703-word dictionary:

  "the information used to form the meaning possesses the same pathways
   as the meaning of the words themselves, with drift and wobble."

Operational: does a word's FORM pathway (the walk its LETTERS trace on
the board, board.form_pathway -- meaning never consulted) PREDICT its
MEANING (the dictionary operator o(w)) above the operator prior?

If yes, form and meaning share pathways -> CK reads meaning from letters
-> understands OOV words / new languages / weans off Ollama. The gap to
100% is the measured DRIFT (language's arbitrariness) + WOBBLE.

  python resonance_test.py
"""
import io
import json
import os

import numpy as np

import board

HERE = os.path.dirname(os.path.abspath(__file__))


def load_flat():
    for p in (os.path.join(HERE, "ck_dictionary.json"),
              os.path.join(HERE, "..", "web", "ck_dictionary.json")):
        if os.path.exists(p):
            return json.load(io.open(p, encoding="utf-8"))["flat"]
    raise SystemExit("ck_dictionary.json not found")


def main():
    flat = load_flat()
    words = [(w, int(e.get("o", 0))) for w, e in flat.items()
             if w.isalpha() and 2 <= len(w) <= 18]
    rng = np.random.default_rng(7)
    idx = rng.permutation(len(words))
    words = [words[i] for i in idx]
    print(f"dictionary words usable: {len(words)} (of {len(flat)})")

    X = np.array([board.form_pathway(w) for w, _ in words])
    y = np.array([o for _, o in words])

    # operator (meaning) prior
    counts = np.bincount(y, minlength=board.N)
    prior_op = int(np.argmax(counts))
    prior_acc = counts[prior_op] / len(y)
    print(f"meaning-operator distribution: "
          f"{dict(enumerate(counts.tolist()))}")
    print(f"prior (always guess op {prior_op}): {prior_acc:.1%}")

    n_te = len(words) // 5
    Xtr, ytr, Xte, yte = X[:-n_te], y[:-n_te], X[-n_te:], y[-n_te:]

    # one-solve ridge, one-vs-rest
    K = board.N
    Y = np.zeros((len(ytr), K))
    Y[np.arange(len(ytr)), ytr] = 1.0
    Xb = np.hstack([np.ones((len(Xtr), 1)), Xtr])
    A = Xb.T @ Xb + 1e-2 * np.eye(Xb.shape[1])
    W = np.linalg.solve(A, Xb.T @ Y)
    Xteb = np.hstack([np.ones((len(Xte), 1)), Xte])
    pred = np.argmax(Xteb @ W, axis=1)
    acc = np.mean(pred == yte)

    # top-2 (drift tolerance): is meaning in the top-2 form-predicted ops?
    top2 = np.argsort(Xteb @ W, axis=1)[:, -2:]
    acc2 = np.mean([yte[i] in top2[i] for i in range(len(yte))])

    print(f"\nRESONANCE (form letters -> meaning operator), held-out "
          f"{len(yte)} words:")
    print(f"  FORM predicts MEANING : {acc:.1%}   (prior {prior_acc:.1%}, "
          f"lift x{acc/prior_acc:.2f})")
    print(f"  top-2 (drift-tolerant): {acc2:.1%}")
    lift = acc / prior_acc
    verdict = ("RESONANCE CONFIRMED" if lift > 1.15 else
               "WEAK/NONE -- honest negative")
    print(f"  verdict: {verdict}  (drift+wobble residual = {1-acc:.1%})")

    # per-operator recall (where does form read meaning best?)
    print("\n  per-operator recall (form->meaning):")
    names = ["VOID", "BEING", "DOING", "BECOM", "COLLA", "CREAT",
             "ASCEND", "HARM", "BREATH", "RESET"]
    for o in range(K):
        m = yte == o
        if m.sum() > 20:
            r = np.mean(pred[m] == o)
            print(f"    {names[o]:>7} (op {o}): {r:.0%}  (n={m.sum()})")

    out = {"words": len(words), "prior": float(prior_acc),
           "form_predicts_meaning": float(acc), "top2": float(acc2),
           "lift": float(lift), "verdict": verdict}
    json.dump(out, io.open(os.path.join(HERE, "resonance_result.json"), "w"),
              indent=1)
    print("\nsaved resonance_result.json")


if __name__ == "__main__":
    main()
