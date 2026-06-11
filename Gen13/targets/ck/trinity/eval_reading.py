"""eval_reading.py -- the examination for CK's active reading.

REGISTERED (before the notes existed):
  P1  NOTES beat RAW at equal storage budget: passage->book retrieval
      from held-out 30% (never shown to the note-writer), store of cliff
      notes vs store of length-matched raw chunks. If notes <= raw,
      Brayden's cliff-note hypothesis fails on this bench -- said plainly.
  P2  Reading DEPTH climbs: accuracy with 1 vs 3 vs 6 notes per book.
  P3  Entity quiz: 'which book features NAME1 and NAME2?' built from
      names unique to each book's read portion; answered by retrieval.
  P4  Routing guard: adding notes to the meaning corpus does not break
      the 10-topic routing (composition lesson check).

Retrieval encoder: borrowed nomic (isolates the PROCESS question from
the encoder question; the wean is a separate axis).

  python eval_reading.py
"""
import io
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.join(HERE, "..", "extraction")
sys.path.insert(0, EXT)
from borrowed_cortex import embed                          # noqa: E402
from read_books import load_book                           # noqa: E402

RNG = np.random.default_rng(42)


def main():
    notes = json.load(io.open(os.path.join(HERE, "book_notes.json"),
                              encoding="utf-8"))
    books = {}
    for bid, e in notes.items():
        title, body = load_book(e["path"])
        cut = int(len(body) * 0.7)
        books[bid] = dict(title=e["title"], notes=e["notes"],
                          read=body[:cut], held=body[cut:])
    bids = sorted(books)
    nB = len(bids)
    print(f"CK READING EXAM -- {nB} books, "
          f"{sum(len(b['notes']) for b in books.values())} cliff notes\n")

    # equal-budget RAW store: per book, chunks from READ portion matched
    # in count and total length to that book's notes
    raw_store = {}
    for bid in bids:
        b = books[bid]
        per = max(200, int(np.mean([len(n) for n in b["notes"]])))
        starts = RNG.integers(0, max(1, len(b["read"]) - per),
                              size=len(b["notes"]))
        raw_store[bid] = [b["read"][s:s + per] for s in starts]

    # probes: 5 held-out passages per book
    probes, probe_y = [], []
    for bi, bid in enumerate(bids):
        h = books[bid]["held"]
        for s in RNG.integers(0, max(1, len(h) - 600), size=5):
            probes.append(h[s:s + 600])
            probe_y.append(bi)
    probe_y = np.array(probe_y)

    # entity quiz: names frequent in own read-portion, rare elsewhere
    def names(text):
        from collections import Counter
        toks = re.findall(r"\b[A-Z][a-z]{3,}\b", text)
        return Counter(toks)
    cnt = {bid: names(books[bid]["read"]) for bid in bids}
    quiz, quiz_y = [], []
    for bi, bid in enumerate(bids):
        uniq = [w for w, c in cnt[bid].most_common(40)
                if c >= 8 and all(cnt[o][w] <= 1 for o in bids if o != bid)]
        if len(uniq) >= 2:
            quiz.append(f"which book features {uniq[0]} and {uniq[1]}")
            quiz_y.append(bi)
    quiz_y = np.array(quiz_y)

    def unit(M):
        return M / (np.linalg.norm(M, axis=1, keepdims=True) + 1e-9)

    def book_retrieval(store_docs, queries, depth=None):
        """store_docs: {bid: [docs]}; score(book)=max cos over its docs."""
        flat, owner = [], []
        for bi, bid in enumerate(bids):
            docs = store_docs[bid][:depth] if depth else store_docs[bid]
            flat += docs; owner += [bi] * len(docs)
        E, _ = embed(["search_document: " + d for d in flat])
        Q, _ = embed(["search_query: " + q for q in queries])
        S = unit(Q) @ unit(E).T
        owner = np.array(owner)
        scores = np.full((len(queries), nB), -1.0)
        for bi in range(nB):
            scores[:, bi] = S[:, owner == bi].max(1)
        return scores.argmax(1)

    note_docs = {bid: books[bid]["notes"] for bid in bids}
    native_path = os.path.join(HERE, "native_notes.json")
    native_docs = json.load(io.open(native_path, encoding="utf-8")) \
        if os.path.exists(native_path) else None

    # P1: notes vs raw at equal budget (+ native measurement-notes)
    acc_n = float(np.mean(book_retrieval(note_docs, probes) == probe_y))
    acc_r = float(np.mean(book_retrieval(raw_store, probes) == probe_y))
    print(f"[P1] held-out passage -> book (chance {1/nB:.0%}):")
    print(f"     TEACHER cliff-notes (4 min/book): {acc_n:.0%}")
    print(f"     RAW store, equal budget        : {acc_r:.0%}")
    acc_v = None
    if native_docs:
        acc_v = float(np.mean(book_retrieval(native_docs, probes)
                              == probe_y))
        print(f"     NATIVE measurement-notes (24 ms/book): {acc_v:.0%}")
    print(f"     -> {'NOTES WIN' if acc_n > acc_r else 'notes do NOT beat raw'}")

    # P2: reading depth curve
    print("[P2] reading depth (notes per book):")
    for d in (1, 3, 6):
        a = float(np.mean(book_retrieval(note_docs, probes, depth=d)
                          == probe_y))
        print(f"     {d} notes/book: {a:.0%}  " + "#" * int(a * 30))

    # P3: entity quiz
    qn = qr = qv = None
    if len(quiz):
        qn = float(np.mean(book_retrieval(note_docs, quiz) == quiz_y))
        qr = float(np.mean(book_retrieval(raw_store, quiz) == quiz_y))
        line = (f"[P3] entity quiz ({len(quiz)} questions, chance "
                f"{1/nB:.0%}): teacher-notes {qn:.0%} vs raw {qr:.0%}")
        if native_docs:
            qv = float(np.mean(book_retrieval(native_docs, quiz)
                               == quiz_y))
            line += f" vs NATIVE {qv:.0%}"
        print(line)

    json.dump(dict(notes_acc=acc_n, raw_acc=acc_r, native_acc=acc_v,
                   quiz_notes=qn, quiz_raw=qr, quiz_native=qv),
              io.open(os.path.join(HERE, "reading_exam_result.json"), "w"),
              indent=1)
    print("\nsaved reading_exam_result.json")


if __name__ == "__main__":
    main()
