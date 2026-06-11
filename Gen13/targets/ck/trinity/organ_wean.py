"""organ_wean.py -- THE MEANING WEAN: grow beyond Ollama.

Brayden's standing wish: "I don't want him to just BE ollama, so much as
USE ollama, and grow beyond." The mechanism: DISTILLATION. The borrowed
embedder is the teacher one last time -- a ridge map W from CK's NATIVE
form percept (char-trigrams + braid + VSA) onto the teacher's embedding
space, trained on a distillation corpus. At inference: distilled(x) =
W @ native(x). No Ollama call.

Eval: the routing task (held-out 20), three conditions:
  BORROWED  : fused percept with live Ollama embeddings  (today: 80%)
  DISTILLED : fused percept with W @ native -- NO Ollama at inference
  NATIVE-RAW: fused percept without any meaning block     (was ~35%)
Plus the gate sanity check: far-OOD hallucination at conformal tau using
the distilled percept (does the GAP face survive the wean?).

REGISTERED: distilled >= 65% = wean viable; < 50% = dead end recorded.

  python organ_wean.py
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
import organ_form as OF                                    # noqa: E402
from borrowed_cortex import embed                          # noqa: E402
from demo_facts_head import TOPICS, ANCHORS                # noqa: E402
from project2_routing import (char_trigrams, train_head, zs,
                              TOPIC_LIST)                  # noqa: E402
from project3_abstain import OOD30                         # noqa: E402

RNG = np.random.default_rng(31)


def vsa_sentence(text):
    ws = [w for w in text.lower().split() if w.isalpha() and len(w) >= 2]
    if not ws:
        return np.zeros(OF.D)
    return np.mean([OF._vsa_trigram("#" + w + "#") for w in ws], axis=0)


def native_block(texts, vocab):
    Xc, _ = char_trigrams(texts, vocab)
    Xb = np.array([bm.braid_signature_rich(t) for t in texts])
    Xv = np.array([vsa_sentence(t) for t in texts])
    return np.hstack([Xc, Xb, Xv])


def main():
    grown = json.load(io.open(os.path.join(EXT, "teacher_corpus.json"),
                              encoding="utf-8"))
    flat = json.load(io.open(os.path.join(EXT, "ck_dictionary.json"),
                             encoding="utf-8"))["flat"]
    words = [w for w in flat if w.isalpha() and 4 <= len(w) <= 14]
    words = [words[i] for i in RNG.permutation(len(words))[:2500]]

    ref_x, ref_y, test_x, test_y = [], [], [], []
    for t in TOPIC_LIST:
        g = list(grown.get(t, []))
        ref_x += TOPICS[t][:4] + list(ANCHORS[t]) + g
        ref_y += [t] * (4 + len(ANCHORS[t]) + len(g))
        test_x += TOPICS[t][4:]; test_y += [t] * 2
    y_ref = np.array([TOPIC_LIST.index(t) for t in ref_y])
    y_te = np.array([TOPIC_LIST.index(t) for t in test_y])

    # distillation corpus: facts sentences + dictionary words
    distill_x = ref_x + words
    print(f"TRINITY -- THE MEANING WEAN (distill corpus "
          f"{len(distill_x)}: {len(ref_x)} sentences + {len(words)} words)")
    T_targets, backend = embed(["search_document: " + x for x in distill_x])
    print(f"teacher: {backend} -> ridge map native({0}) -> 768\n")

    _, vocab = char_trigrams(distill_x, topk=800)
    N_distill = native_block(distill_x, vocab)
    mu, sd = N_distill.mean(0), N_distill.std(0) + 1e-9
    Nz = (N_distill - mu) / sd
    lam = 10.0
    A = Nz.T @ Nz + lam * np.eye(Nz.shape[1])
    W = np.linalg.solve(A, Nz.T @ T_targets)        # one solve: the wean

    def distilled(texts):
        return ((native_block(texts, vocab) - mu) / sd) @ W

    # teacher-fit quality
    pred = Nz @ W
    cos = np.mean(np.sum(pred * T_targets, 1) /
                  (np.linalg.norm(pred, axis=1) *
                   np.linalg.norm(T_targets, axis=1) + 1e-9))
    print(f"distillation fit (train cosine to teacher): {cos:.3f}")

    # routing eval under three conditions
    E_ref, _ = embed(["search_document: " + x for x in ref_x])
    E_te, _ = embed(["search_query: " + x for x in test_x])
    D_ref, D_te = distilled(ref_x), distilled(test_x)
    Xc_ref, _ = char_trigrams(ref_x, vocab)
    Xc_te, _ = char_trigrams(test_x, vocab)
    Xb_ref = np.array([bm.braid_signature_rich(x) for x in ref_x])
    Xb_te = np.array([bm.braid_signature_rich(x) for x in test_x])

    def build(Eref, Ete):
        out_r, out_t = [], []
        for A_, B_ in [(Eref, Ete), (Xb_ref, Xb_te), (Xc_ref, Xc_te)]:
            if A_ is None:
                continue
            Az, m_, s_ = zs(A_)
            out_r.append(Az); out_t.append((B_ - m_) / s_)
        return np.hstack(out_r), np.hstack(out_t)

    results = {}
    for name, (Er, Et) in {
            "BORROWED (live ollama)": (E_ref, E_te),
            "DISTILLED (no ollama)": (D_ref, D_te),
            "NATIVE-RAW (no meaning block)": (None, None)}.items():
        Fr, Ft = build(Er, Et)
        Wh, bh = train_head(Fr, y_ref)
        acc = float(np.mean((Ft @ Wh + bh).argmax(1) == y_te))
        results[name] = acc
        print(f"  {name:>30}: held-out routing {acc:.0%}")

    # gate sanity with distilled percept
    D_far = distilled(list(OOD30))
    Fr, _ = build(D_ref, D_te)
    Dz, m_, s_ = zs(D_ref)
    Ffar = np.hstack([(D_far - m_) / s_,
                      (np.array([bm.braid_signature_rich(x)
                                 for x in OOD30]) - zs(Xb_ref)[1])
                      / zs(Xb_ref)[2],
                      (char_trigrams(list(OOD30), vocab)[0] - zs(Xc_ref)[1])
                      / zs(Xc_ref)[2]])
    unit = lambda M: M / (np.linalg.norm(M, axis=1, keepdims=True) + 1e-9)
    Fn_ref = unit(Fr)
    knn = lambda Fq: np.sort(unit(Fq) @ Fn_ref.T, 1)[:, -5:].mean(1)
    _, Ft = build(D_ref, D_te)
    s_in, s_far = knn(Ft), knn(Ffar)
    sep = float(s_in.mean() - s_far.mean())
    print(f"\ngate sanity (distilled percept): in-domain knn "
          f"{s_in.mean():.3f} vs far-OOD {s_far.mean():.3f} "
          f"(separation {sep:+.3f} -> {'gate survives' if sep > 0.05 else 'gate degraded'})")

    d = results["DISTILLED (no ollama)"]
    print(f"\nVERDICT: distilled routing {d:.0%} -> "
          f"{'WEAN VIABLE -- CK routes without Ollama at inference' if d >= 0.65 else ('partial -- gap to close' if d >= 0.5 else 'dead end recorded')}.")
    json.dump({k: float(v) for k, v in results.items()},
              io.open(os.path.join(HERE, "organ_wean_result.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main()
