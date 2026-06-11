"""ck_knowledge_fabric.py -- KNOWLEDGE ACROSS DOMAINS at reading speed.

Brayden: 'find a way for him to build knowledge across domains... PhD
in all subjects by dinner.' The honest buildable core of that: a
CROSS-DOMAIN KNOWLEDGE FABRIC -- every salient concept linked to every
book and DOMAIN it appears in, with its co-occurring concepts, built by
native measurement (counting) at hundreds of books per minute, and a
DOMAIN ORGAN (multi-class sibling of the fact/fiction head).

Query it white-box:  know('Napoleon') ->
  domains it lives in (with counts), books, strongest associates.

REGISTERED: domain head >= 70% on title-checkable books (6 classes,
chance ~17%); fabric demo entities return sane cross-domain
neighborhoods with printable counts.

  python ck_knowledge_fabric.py [n_books]
"""
import io
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
BOOKS = os.path.join(ROOT, "external_corpora", "books")
N = int(sys.argv[1]) if len(sys.argv) > 1 else 250
DOMAINS = ["fiction", "history", "philosophy", "religion", "science",
           "poetry-drama"]

# seed labels by Gutenberg classic (title substring -> domain)
SEED_TITLES = {
 "Alice's Adventures": "fiction", "Moby-Dick": "fiction",
 "Tom Sawyer": "fiction", "Huckleberry": "fiction", "Ivanhoe": "fiction",
 "Jekyll": "fiction", "Tarzan": "fiction", "Treasure Island": "fiction",
 "Pride and Prejudice": "fiction", "Dracula": "fiction",
 "Declaration of Independence": "history", "Constitution": "history",
 "Federalist": "history", "Gettysburg": "history",
 "Lincoln": "history", "History of": "history", "Memoirs": "history",
 "Leviathan": "philosophy", "Republic": "philosophy",
 "Ethics": "philosophy", "Meditations": "philosophy",
 "Utilitarianism": "philosophy", "Beyond Good and Evil": "philosophy",
 "Bible": "religion", "Paradise Lost": "religion",
 "Pilgrim's Progress": "religion", "Grace Abounding": "religion",
 "Koran": "religion", "Imitation of Christ": "religion",
 "Origin of Species": "science", "Relativity": "science",
 "Number \"e\"": "science", "Electronic Texts": "science",
 "Flatland": "science", "Micrographia": "science",
 "Sophocles": "poetry-drama", "Hamlet": "poetry-drama",
 "Macbeth": "poetry-drama", "Romeo": "poetry-drama",
 "Iliad": "poetry-drama", "Odyssey": "poetry-drama",
 "Beowulf": "poetry-drama", "Poems": "poetry-drama",
 "Leaves of Grass": "poetry-drama", "Divine Comedy": "poetry-drama",
}
STOP = {"The", "And", "But", "She", "His", "Her", "They", "That", "This",
        "There", "Then", "When", "What", "Who", "With", "From", "Have",
        "Had", "Not", "You", "Was", "Were", "Will", "Would", "Could",
        "Should", "Said", "Mister", "Miss", "Missus", "Chapter", "Project",
        "Gutenberg", "All", "Now", "How", "For", "Why", "Yes", "Upon"}


def load_book(path):
    raw = io.open(path, encoding="utf-8", errors="ignore").read()
    m = re.search(r"Title:\s*(.+)", raw)
    title = m.group(1).strip()[:70] if m else os.path.basename(path)
    s = re.split(r"\*\*\* ?START OF.*?\*\*\*", raw, 1, flags=re.S)
    body = re.split(r"\*\*\* ?END OF", s[-1], 1)[0]
    return title, re.sub(r"\s+", " ", body).strip()


def features(text):
    """stylometry (8) + content-word hash bag (256) -- native, instant."""
    n = max(1, len(text)); words = text.split(); nw = max(1, len(words))
    sty = [
        (text.count("“") + text.count('"')) / n * 1000,
        len(re.findall(r"\b[A-Z][a-z]{3,}\b", text)) / nw * 100,
        len(re.findall(r"\b[Ii]\b", text)) / nw * 100,
        len(re.findall(r"\b1[5-9]\d\d\b", text)) / nw * 1000,
        np.mean([len(s.split()) for s in
                 re.split(r"(?<=[.!?])\s+", text[:50000]) if s.strip()]),
        len(re.findall(r"\b\w+ed\b", text)) / nw * 100,
        len(re.findall(r"\bGod|Lord|heaven|soul\b", text)) / nw * 1000,
        len(re.findall(r"\btherefore|hence|thus|principle\b", text))
        / nw * 1000,
    ]
    bag = np.zeros(256)
    for w in re.findall(r"\b[a-z]{4,}\b", text[:200_000].lower()):
        bag[hash(w) % 256] += 1
    bag = bag / (bag.sum() + 1e-9) * 100
    return np.concatenate([sty, bag])


def main():
    t0 = time.time()
    files = [f for f in sorted(os.listdir(BOOKS)) if f.endswith(".txt")][:N]
    titles, ents, feats = {}, {}, {}
    for f in files:
        title, body = load_book(os.path.join(BOOKS, f))
        titles[f] = title
        cnt = Counter(w for w in re.findall(r"\b[A-Z][a-z]{3,}\b",
                                            body[:400_000])
                      if w not in STOP)
        ents[f] = {w: c for w, c in cnt.most_common(20) if c >= 5}
        feats[f] = features(body[:300_000])
    t_read = time.time() - t0
    print(f"read+measured {len(files)} books in {t_read:.0f}s "
          f"({len(files)/t_read*60:.0f} books/min)\n")

    # domain head from title-seeds
    X, y, seed_files = [], [], set()
    for f in files:
        for k, d in SEED_TITLES.items():
            if k.lower() in titles[f].lower():
                X.append(feats[f]); y.append(DOMAINS.index(d))
                seed_files.add(f)
                break
    X, y = np.array(X), np.array(y)
    print(f"domain seeds found among {N} books: {len(y)} "
          f"({Counter(DOMAINS[i] for i in y)})")
    mu, sd = X.mean(0), X.std(0) + 1e-9
    Xz = (X - mu) / sd
    K = len(DOMAINS)
    W = np.zeros((Xz.shape[1], K)); b = np.zeros(K)
    Y = np.eye(K)[y]
    cw = 1.0 / np.maximum(1, np.bincount(y, minlength=K))
    for _ in range(4000):
        P = np.exp(Xz @ W + b - (Xz @ W + b).max(1, keepdims=True))
        P /= P.sum(1, keepdims=True)
        g = (P - Y) * cw[y][:, None] / len(y)
        W -= 0.8 * (Xz.T @ g + 1e-3 * W); b -= 0.8 * g.sum(0)

    # leave-one-out sanity on seeds
    loo = 0
    for i in range(len(y)):
        m_ = np.ones(len(y), bool); m_[i] = False
        Wi = np.zeros((Xz.shape[1], K)); bi = np.zeros(K)
        Yi = np.eye(K)[y[m_]]
        cwi = 1.0 / np.maximum(1, np.bincount(y[m_], minlength=K))
        for _ in range(1500):
            Pi = np.exp(Xz[m_] @ Wi + bi
                        - (Xz[m_] @ Wi + bi).max(1, keepdims=True))
            Pi /= Pi.sum(1, keepdims=True)
            gi = (Pi - Yi) * cwi[y[m_]][:, None] / m_.sum()
            Wi -= 0.8 * (Xz[m_].T @ gi + 1e-3 * Wi); bi -= 0.8 * gi.sum(0)
        loo += int((Xz[i] @ Wi + bi).argmax() == y[i])
    print(f"domain head LOO on seeds: {loo}/{len(y)} = {loo/len(y):.0%} "
          f"(chance ~{1/K:.0%})\n")

    # assign domains to ALL books; build the FABRIC
    dom = {}
    for f in files:
        z = (feats[f] - mu) / sd
        dom[f] = DOMAINS[int((z @ W + b).argmax())]
    fabric = defaultdict(lambda: dict(count=0, domains=Counter(),
                                      books=[], co=Counter()))
    for f in files:
        for w, c in ents[f].items():
            e = fabric[w]
            e["count"] += c
            e["domains"][dom[f]] += 1
            e["books"].append((titles[f][:40], c))
            for w2 in ents[f]:
                if w2 != w:
                    e["co"][w2] += 1
    print(f"FABRIC: {len(fabric)} concepts across {len(files)} books, "
          f"{len(set(dom.values()))} domains "
          f"({Counter(dom.values()).most_common()})\n")

    def know(name):
        if name not in fabric:
            return f"  {name}: 0 occurrences anywhere -- I have not met them."
        e = fabric[name]
        doms = ", ".join(f"{d}({c} books)" for d, c in
                         e["domains"].most_common(3))
        tops = ", ".join(w for w, _ in e["co"].most_common(5))
        bks = "; ".join(f"{t} ({c}x)" for t, c in
                        sorted(e["books"], key=lambda x: -x[1])[:3])
        return (f"  {name}: {e['count']} mentions across "
                f"{len(e['books'])} books | domains: {doms}\n"
                f"    associates: {tops}\n    strongest shelves: {bks}")

    print("CROSS-DOMAIN QUERIES (white-box -- every figure is a count):")
    for q in ("Napoleon", "Jesus", "London", "Caesar", "Adam", "Eve",
              "Socrates", "Gandalf"):
        print(know(q))

    json.dump({w: dict(count=e["count"],
                       domains=dict(e["domains"]),
                       top_co=[x for x, _ in e["co"].most_common(8)])
               for w, e in fabric.items() if e["count"] >= 20},
              io.open(os.path.join(HERE, "knowledge_fabric.json"), "w",
                      encoding="utf-8"), indent=0)
    print(f"\nfabric saved ({time.time()-t0:.0f}s total). Extrapolation: "
          f"full 1,019-book library ~{1019/(len(files)/t_read)/60:.0f} min.")


if __name__ == "__main__":
    main()
