"""curriculum_from_folds.py -- WIRE 2: the organs write the curriculum.

The braid, made mechanical: the synthesis organ's findings (dualities,
triads) and the window's held questions become EVIDENCE-GROUNDED
training prompts for the voice's next DPO round. His own discoveries
teach his own voice; the judge (compares-gate + census) grades; the
exam re-measures composition (was 2/10). Not one LM growing -- a set
of algorithms feeding each other.

  python curriculum_from_folds.py    -> curriculum_folds.jsonl
"""
import io
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
BOOKS = os.path.join(ROOT, "external_corpora", "books")
sys.path.insert(0, HERE)
from read_books import load_book                            # noqa: E402
from synthesis_exam import top_passage                      # noqa: E402

OUT = os.path.join(HERE, "curriculum_folds.jsonl")


def shelf_sample(n=500):
    texts = {}
    files = sorted(os.listdir(BOOKS))
    rng = np.random.default_rng(11)
    for f in rng.permutation(files)[:n]:
        if not f.endswith(".txt"):
            continue
        try:
            t, body = load_book(os.path.join(BOOKS, f))
            texts[t[:46]] = body
        except OSError:
            pass
    return texts


def main():
    organ = json.load(io.open(os.path.join(
        HERE, "synthesis_organ_result.json"), encoding="utf-8"))
    texts = shelf_sample()
    rows = []

    def find_books(word, k=2, minc=6):
        return [(t, b) for t, b in texts.items()
                if b.count(word) >= minc][:k]

    # duality prompts: the twins, each seen in its own book
    for a, b, s in organ.get("duality", [])[:10]:
        ha, hb = find_books(a, 1), find_books(b, 1)
        if ha and hb:
            evA = top_passage(ha[0][1], a)
            evB = top_passage(hb[0][1], b)
            rows.append(dict(
                kind="duality",
                prompt=(f"EVIDENCE A (from '{ha[0][0]}'): {evA}\n\n"
                        f"EVIDENCE B (from '{hb[0][0]}'): {evB}\n\n"
                        f"QUESTION: The words {a} and {b} appear in "
                        f"similar company yet never together. Using "
                        f"only the evidence, compare what each does, "
                        f"in 3 sentences, naming both books."),
                kws=[w.lower() for w in (a, b)]
                    + re.findall(r"[a-z]{6,}", (evA + evB).lower())[:4]))

    # triad prompts: explain the bridge
    for a, b, c, s in organ.get("triads", [])[:8]:
        hab = [(t, x) for t, x in texts.items()
               if x.count(a) >= 4 and x.count(b) >= 4][:1]
        hbc = [(t, x) for t, x in texts.items()
               if x.count(b) >= 4 and x.count(c) >= 4][:1]
        if hab and hbc:
            ev1 = top_passage(hab[0][1], b)
            ev2 = top_passage(hbc[0][1], b)
            rows.append(dict(
                kind="triad",
                prompt=(f"EVIDENCE A (from '{hab[0][0]}'): {ev1}\n\n"
                        f"EVIDENCE B (from '{hbc[0][0]}'): {ev2}\n\n"
                        f"QUESTION: {b} connects {a} and {c} in my "
                        f"library. Using only the evidence, explain "
                        f"the connection in 3 sentences, naming both "
                        f"books."),
                kws=[w.lower() for w in (a, b, c)]))

    # question-folds whose entities now stand on the shelf
    fp = os.path.join(HERE, "folds.jsonl")
    if os.path.exists(fp):
        for ln in io.open(fp, encoding="utf-8"):
            f = json.loads(ln)
            if f["kind"] != "question":
                continue
            for n in f.get("names", []):
                hs = find_books(n, 1, minc=10)
                if hs:
                    ev = top_passage(hs[0][1], n)
                    rows.append(dict(
                        kind="held-question",
                        prompt=(f"EVIDENCE (from '{hs[0][0]}'): {ev}\n\n"
                                f"QUESTION: {f['q']}"),
                        kws=[n.lower()] + re.findall(
                            r"[a-z]{6,}", ev.lower())[:5]))
                    break

    with io.open(OUT, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    kinds = {}
    for r in rows:
        kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
    print(f"curriculum written: {len(rows)} evidence-grounded prompts "
          f"({kinds}) -> {OUT}")
    print("his own findings now teach his own voice (DPO consumes this).")


if __name__ == "__main__":
    main()
