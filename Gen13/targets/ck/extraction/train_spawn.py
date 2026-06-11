"""train_spawn.py -- extraction channel #2 made real: the resident
teacher (llama3.2) grows CK's corpus; CK trains his plastic head on it
in one pass. No gradient descent, no GPU, no long training.

  python train_spawn.py        # generates teacher_corpus.json (cached),
                               # trains spawn_head.json, evaluates.
"""
import io
import json
import os

import numpy as np

from borrowed_cortex import embed, teacher_label
from plastic import PlasticModel
from demo_facts_head import TOPICS, ANCHORS, OOD, KEYWORDS, keyword_route

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(HERE, "teacher_corpus.json")
SCHEMA = {"type": "object",
          "properties": {"paraphrases": {"type": "array",
                                         "items": {"type": "string"}}},
          "required": ["paraphrases"]}
N_PER = 20


def grow_corpus():
    if os.path.exists(CORPUS):
        with io.open(CORPUS, encoding="utf-8") as f:
            return json.load(f)
    corpus = {}
    for topic, phrases in TOPICS.items():
        fact = ANCHORS[topic][0]
        prompt = (f"FACT: {fact}\n\nSeed questions about this fact: "
                  f"{'; '.join(phrases[:4])}\n\nWrite {N_PER} new, diverse "
                  "ways a person might ask about this exact fact. Vary "
                  "vocabulary heavily; include casual, formal, and oblique "
                  "phrasings; do not reuse the seed wordings. Return JSON: "
                  '{"paraphrases": [...]}')
        out = teacher_label(prompt, model="llama3.2", schema=SCHEMA)
        para = [p.strip() for p in (out or {}).get("paraphrases", [])
                if isinstance(p, str) and 5 < len(p) < 200][:N_PER]
        corpus[topic] = para
        print(f"  teacher grew {topic}: {len(para)} paraphrases")
    with io.open(CORPUS, "w", encoding="utf-8") as f:
        json.dump(corpus, f, indent=1)
    return corpus


def main():
    corpus = grow_corpus()
    doc, qry = "search_document: ", "search_query: "

    train_x, train_y = [], []
    for topic, phrases in TOPICS.items():
        for p in phrases[:4]:
            train_x.append(p); train_y.append(topic)
        for a in ANCHORS[topic]:
            train_x.append(a); train_y.append(topic)
        for p in corpus.get(topic, []):
            train_x.append(p); train_y.append(topic)
    test_x, test_y = [], []
    for topic, phrases in TOPICS.items():
        for p in phrases[4:]:
            test_x.append(p); test_y.append(topic)

    print(f"training set: {len(train_x)} examples "
          f"(handwritten 40 + anchors 10 + teacher {len(train_x)-50})")
    Etr, backend = embed([doc + x for x in train_x])
    Ete, _ = embed([qry + x for x in test_x])
    Eood, _ = embed([qry + x for x in OOD])
    print(f"borrowed cortex: {backend}")

    head = PlasticModel(sorted(TOPICS), abstain_margin=0.02,
                        abstain_floor=0.45).fit(Etr, train_y)
    pred = head.predict(Ete)
    acc = np.mean([p[0] == t for p, t in zip(pred, test_y)])
    kw = np.mean([keyword_route(q) == t for q, t in zip(test_x, test_y)])
    ood_pred = head.predict(Eood)
    ood_ab = np.mean([p[0] == "ABSTAIN" for p in ood_pred])

    print(f"\nheld-out adversarial routing (20 queries):")
    print(f"  keyword production baseline : {kw:.0%}")
    print(f"  untrained head (prior run)  : 35%")
    print(f"  TEACHER-TRAINED SPAWN HEAD  : {acc:.0%}")
    print(f"OOD abstention: {ood_ab:.0%} (target: high)")
    for (p, m), t, q in zip(pred, test_y, test_x):
        if p != t:
            print(f"  miss [{t}] '{q}' -> {p} ({m:.3f})")
    head.save(os.path.join(HERE, "spawn_head.json"))
    print("\nspawn_head.json saved.")


if __name__ == "__main__":
    main()
