"""native_notes.py -- CK takes his OWN notes: no teacher, pure
measurement, milliseconds per book ('hauling ass, placing his
measurements on the wheel').

Extractive cliff notes, fully white-box: split the read-portion into
sentences; score each by ENTITY SALIENCE (names frequent in THIS book,
rare in the others -- the same uniqueness measurement the quiz uses) +
content density; greedily pick 6 sentences that cover distinct entities
and distinct regions of the book. Every choice is a printable number.

  python native_notes.py
"""
import io
import json
import os
import re
import time
from collections import Counter

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def native_notes_for(read_texts):
    """read_texts: {bid: read_portion}. Returns {bid: [6 note sentences]}."""
    name_counts = {bid: Counter(re.findall(r"\b[A-Z][a-z]{3,}\b", t))
                   for bid, t in read_texts.items()}
    out = {}
    for bid, text in read_texts.items():
        own = name_counts[bid]
        sal = {w: c / (1 + sum(name_counts[o][w] for o in read_texts
                               if o != bid))
               for w, c in own.items() if c >= 3}
        sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text)
                 if 80 <= len(s.strip()) <= 320]
        n = len(sents)
        covered = set()
        notes = []
        # greedy: best salience-sum of UNCOVERED entities, spread over book
        regions = np.array_split(np.arange(n), 6)
        for reg in regions:
            best, best_s = None, -1.0
            for i in reg:
                ents = set(re.findall(r"\b[A-Z][a-z]{3,}\b", sents[i]))
                score = sum(sal.get(e, 0) for e in ents - covered)
                if score > best_s:
                    best, best_s = i, score
            if best is not None:
                notes.append(sents[best])
                covered |= set(re.findall(r"\b[A-Z][a-z]{3,}\b",
                                          sents[best]))
        out[bid] = notes
    return out


def main():
    from read_books import load_book
    teacher = json.load(io.open(os.path.join(HERE, "book_notes.json"),
                                encoding="utf-8"))
    reads = {}
    for bid, e in teacher.items():
        _, body = load_book(e["path"])
        reads[bid] = body[: int(len(body) * 0.7)]
    t0 = time.time()
    notes = native_notes_for(reads)
    dt = time.time() - t0
    json.dump(notes, io.open(os.path.join(HERE, "native_notes.json"), "w",
                             encoding="utf-8"), indent=0)
    per = dt / max(1, len(notes))
    print(f"NATIVE notes: {len(notes)} books in {dt:.2f}s "
          f"({per*1000:.0f} ms/book -> 1,019 books in "
          f"{1019*per/60:.1f} min)")
    bid = sorted(notes)[0]
    print(f"sample ({teacher[bid]['title'][:30]}): {notes[bid][0][:110]}")


if __name__ == "__main__":
    main()
