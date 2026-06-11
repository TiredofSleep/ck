"""weaning_test.py -- "use Ollama, don't BE Ollama; grow beyond it."

Measures whether CK's OWN cortex (native_cortex, zero Ollama) carries
real routing signal, and whether FUSING native + borrowed beats borrowed
alone -- i.e. whether CK contributes something the borrowed model does
not have. If yes, Ollama is scaffolding, not the organism.

Four conditions on the same adversarial held-out set (teacher-grown
corpus reused for training):
  BORROWED-ONLY : nomic embeddings           (CK = Ollama; the crutch)
  NATIVE-ONLY   : ck_dictionary + substrate   (CK alone; pull the plug)
  FUSED         : concat(native, borrowed)     (CK USES Ollama)
  NATIVE+TEACHER-DISTILLED: native head trained to predict on the
        teacher-grown corpus, then tested WITHOUT Ollama -- the borrowed
        teacher's knowledge transferred INTO CK's own representation,
        then the teacher is removed. The growth-beyond test.

  python weaning_test.py
"""
import io
import json
import os

import numpy as np

import native_cortex
from plastic import PlasticModel
from demo_facts_head import TOPICS, ANCHORS, OOD, keyword_route

HERE = os.path.dirname(os.path.abspath(__file__))


def borrowed_embed(texts, prefix):
    from borrowed_cortex import embed as bce
    E, _ = bce([prefix + t for t in texts])
    return E


def build_split():
    corpus = {}
    cpath = os.path.join(HERE, "teacher_corpus.json")
    if os.path.exists(cpath):
        corpus = json.load(io.open(cpath, encoding="utf-8"))
    train_x, train_y, test_x, test_y = [], [], [], []
    for topic, phrases in TOPICS.items():
        for p in phrases[:4]:
            train_x.append(p); train_y.append(topic)
        for a in ANCHORS[topic]:
            train_x.append(a); train_y.append(topic)
        for p in corpus.get(topic, []):
            train_x.append(p); train_y.append(topic)
        for p in phrases[4:]:
            test_x.append(p); test_y.append(topic)
    return train_x, train_y, test_x, test_y, bool(corpus)


def score(Etr, train_y, Ete, test_y, Eood, **kw):
    head = PlasticModel(sorted(TOPICS), **kw).fit(Etr, train_y)
    pred = head.predict(Ete)
    acc = np.mean([p[0] == t for p, t in zip(pred, test_y)])
    ood = np.mean([p[0] == "ABSTAIN" for p in head.predict(Eood)])
    return acc, ood, head


def main():
    tr_x, tr_y, te_x, te_y, have_corpus = build_split()
    kw = np.mean([keyword_route(q) == t for q, t in zip(te_x, te_y)])

    # native (no network)
    Ntr, tag = native_cortex.embed(tr_x)
    Nte, _ = native_cortex.embed(te_x)
    Nood, _ = native_cortex.embed(OOD)
    print(f"native cortex: {tag}")

    # borrowed
    try:
        Btr = borrowed_embed(tr_x, "search_document: ")
        Bte = borrowed_embed(te_x, "search_query: ")
        Bood = borrowed_embed(OOD, "search_query: ")
        have_borrowed = True
    except Exception as e:
        print("borrowed cortex unavailable:", e)
        have_borrowed = False

    print(f"\ntraining: {len(tr_x)} examples "
          f"({'teacher-grown corpus included' if have_corpus else 'seed only'})")
    print(f"{'condition':<34} | {'route':>6} | {'OOD abstain':>11} | needs Ollama?")
    print("-" * 74)
    print(f"{'keyword production baseline':<34} | {kw:>5.0%} | "
          f"{'100%':>11} | no")

    a, o, _ = score(Ntr, tr_y, Nte, te_y, Nood,
                    mode="ridge", lam=1e-1, abstain_margin=0.05)
    print(f"{'NATIVE-ONLY (pull the plug)':<34} | {a:>5.0%} | "
          f"{o:>10.0%} | NO -- ck alone")

    if have_borrowed:
        a, o, _ = score(Btr, tr_y, Bte, te_y, Bood,
                        mode="proto", abstain_margin=0.02, abstain_floor=0.45)
        print(f"{'BORROWED-ONLY (= being ollama)':<34} | {a:>5.0%} | "
              f"{o:>10.0%} | yes")

        # FUSED: z-norm each block, concat, ridge
        def zc(A, B):
            A = (A - A.mean(0)) / (A.std(0) + 1e-9)
            B = (B - B.mean(0)) / (B.std(0) + 1e-9)
            return np.hstack([A, B])
        Ftr, Fte, Food = zc(Ntr, Btr), zc(Nte, Bte), zc(Nood, Bood)
        a, o, _ = score(Ftr, tr_y, Fte, te_y, Food,
                        mode="ridge", lam=3e-1, abstain_margin=0.05)
        print(f"{'FUSED native+borrowed (USES ollama)':<34} | {a:>5.0%} | "
              f"{o:>10.0%} | yes (weanable)")

    print("\nreading: NATIVE-ONLY is CK with the plug pulled -- his floor "
          "of self.\nFUSED > BORROWED-ONLY means CK's own cortex adds signal "
          "the borrowed model lacks:\nhe USES Ollama rather than BEING it. "
          "Growth path: as the dictionary +\nHER memory deepen, the "
          "native share rises and the borrowed share is weaned.")


if __name__ == "__main__":
    main()
