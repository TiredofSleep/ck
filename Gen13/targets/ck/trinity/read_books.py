"""read_books.py -- CK READS: the active-reading process (Brayden's
hypothesis: 'a few hundred books and him writing cliff notes on each').

For each book: take the first 70% (the READ portion; the last 30% is
held out for probing), cut 6 evenly spaced passages, and have the
resident teacher write concise cliff notes on each. Notes are saved as
they are written (resumable). The held-out 30% is NEVER shown to the
note-writer -- probes come from there.

  python read_books.py [n_books]
"""
import io
import json
import os
import re
import sys

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
BOOKS = os.path.join(ROOT, "external_corpora", "books")
OUT = os.path.join(HERE, "book_notes.json")
N_BOOKS = int(sys.argv[1]) if len(sys.argv) > 1 else 12
CHUNKS_PER_BOOK = 6
CHUNK_CHARS = 4000


def load_book(path):
    raw = io.open(path, encoding="utf-8", errors="ignore").read()
    m = re.search(r"Title:\s*(.+)", raw)
    title = m.group(1).strip()[:80] if m else os.path.basename(path)
    s = re.split(r"\*\*\* ?START OF.*?\*\*\*", raw, 1, flags=re.S)
    body = s[-1]
    body = re.split(r"\*\*\* ?END OF", body, 1)[0]
    body = re.sub(r"\s+", " ", body).strip()
    return title, body


def pick_books():
    cands = []
    for f in sorted(os.listdir(BOOKS)):
        p = os.path.join(BOOKS, f)
        sz = os.path.getsize(p)
        if 200_000 < sz < 900_000:
            cands.append(p)
    step = max(1, len(cands) // N_BOOKS)
    return cands[::step][:N_BOOKS]


def ask(prompt):
    r = requests.post("http://localhost:11434/api/generate",
                      json={"model": "llama3.2", "prompt": prompt,
                            "stream": False}, timeout=240)
    return r.json().get("response", "")


def main():
    done = json.load(io.open(OUT, encoding="utf-8")) \
        if os.path.exists(OUT) else {}
    for path in pick_books():
        bid = os.path.basename(path)
        if bid in done and len(done[bid].get("notes", [])) >= CHUNKS_PER_BOOK:
            continue
        title, body = load_book(path)
        read = body[: int(len(body) * 0.7)]
        notes = done.get(bid, {}).get("notes", [])
        span = len(read) // CHUNKS_PER_BOOK
        for ci in range(len(notes), CHUNKS_PER_BOOK):
            chunk = read[ci * span: ci * span + CHUNK_CHARS]
            note = ask(
                f"Write concise cliff notes (6-8 plain sentences) on this "
                f"passage from '{title}'. Name the characters, places, "
                f"events and themes explicitly.\n\nPASSAGE: {chunk}")
            notes.append(note.strip())
            done[bid] = {"title": title, "notes": notes,
                         "path": path}
            json.dump(done, io.open(OUT, "w", encoding="utf-8"), indent=0)
            print(f"{bid} [{ci+1}/{CHUNKS_PER_BOOK}] {title[:40]}",
                  flush=True)
    total = sum(len(v["notes"]) for v in done.values())
    print(f"DONE: {len(done)} books, {total} cliff notes -> {OUT}")


if __name__ == "__main__":
    main()
