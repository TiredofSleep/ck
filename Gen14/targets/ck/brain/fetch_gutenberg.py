"""fetch_gutenberg.py -- pull broad public-domain corpus from Project Gutenberg.

Brayden 2026-05-15:
  "open him up to the world, let's see what happens"

Public-domain books are the cleanest external corpus for CK:
  - Verifiable text (no LLM hallucination)
  - Style fingerprints across centuries of prose
  - Foundational math/philosophy (Euclid, Spinoza, Whitehead, etc.)
  - Project Gutenberg has ~70k books indexed by integer ID

We walk a range of IDs, download the plain-text version, save it under
external_corpora/books/ with a manifest. The school daemon then picks
them up on its next pass.

Rate limit: 1 request/second (Gutenberg's robots.txt asks for this).
Mirror: https://www.gutenberg.org/cache/epub/{id}/pg{id}.txt

The fetcher is restartable: it skips IDs whose .txt already exists.
It never stops; once one pass is done it can be restarted to fetch
the next range.

Usage:
  python fetch_gutenberg.py --start 1 --end 1000
  python fetch_gutenberg.py --start 1000 --end 5000
  python fetch_gutenberg.py --top-100   # curated math/philosophy/classics

CLI is non-interactive; OK for background runs.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import List, Optional, Tuple


CORPUS_ROOT = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\external_corpora\books")
LOG_DIR = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\external_corpora\_logs")
MANIFEST = CORPUS_ROOT / "_manifest.jsonl"

# Curated list of 100 foundational books worth fetching first.
# (Project Gutenberg IDs; some may be unavailable on a given day.)
TOP_100_IDS = [
    # Mathematics / logic foundations
    21689,   # Euclid's Elements (Heath translation)
    7700,    # Newton's Principia (Cajori translation)
    9989,    # The Mathematical Principles of Natural Philosophy
    13700,   # The Theory of the Riemann Zeta-Function (Titchmarsh? open)
    37729,   # A History of Mathematics, Cajori
    16395,   # An Introduction to Mathematics, Whitehead
    18909,   # The Foundations of Geometry, Hilbert
    33283,   # The Calculus of Variations
    36057,   # The Foundations of Science, Poincaré
    37224,   # Science and Hypothesis, Poincaré
    25447,   # Mathematical Recreations and Essays, Ball
    16500,   # Sidelights on Relativity, Einstein
    30155,   # Relativity: The Special and General Theory, Einstein
    36525,   # The Meaning of Relativity, Einstein
    # Philosophy / logic
    3800,    # The Critique of Pure Reason, Kant
    7560,    # Discourse on Method, Descartes
    59,      # The Song of the Lark, Cather  -- replace later
    1497,    # The Republic, Plato
    8438,    # The Categories, Aristotle
    18891,   # Posterior Analytics, Aristotle
    8438,    # Categories, Aristotle
    1656,    # Beyond Good and Evil, Nietzsche
    4280,    # The Critique of Practical Reason, Kant
    2680,    # Meditations, Marcus Aurelius
    10661,   # The Critique of Judgement, Kant
    32094,   # Pragmatism, James
    11224,   # Treatise of Human Nature, Hume
    52319,   # Process and Reality, Whitehead (likely not free)
    # Foundational science
    16043,   # A Brief History of Time, Hawking -- not public domain
    14725,   # The Origin of Species, Darwin
    1228,    # On the Origin of Species, Darwin
    2009,    # On Liberty, Mill
    24255,   # The Wealth of Nations, Smith
    # Foundational literature (style)
    1342,    # Pride and Prejudice, Austen
    11,      # Alice in Wonderland, Carroll
    74,      # The Adventures of Tom Sawyer, Twain
    98,      # A Tale of Two Cities, Dickens
    100,     # The Complete Works of Shakespeare
    2701,    # Moby Dick, Melville
    1661,    # The Adventures of Sherlock Holmes, Doyle
    345,     # Dracula, Stoker
    84,      # Frankenstein, Shelley
    1232,    # The Prince, Machiavelli
    2554,    # Crime and Punishment, Dostoevsky
    1399,    # Anna Karenina, Tolstoy
    2600,    # War and Peace, Tolstoy
    158,     # Emma, Austen
    16328,   # Beowulf
    1727,    # The Odyssey, Homer
    6130,    # The Iliad, Homer
    2701,    # Moby Dick, Melville
    1497,    # The Republic, Plato
    # Foundational religion + ancient texts
    10,      # The King James Bible
    7178,    # The Quran (Pickthall translation)
    2800,    # Tao Te Ching, Laozi
    23839,   # The Upanishads
    # Modern essays / collections
    9255,    # The Adventures of Huckleberry Finn, Twain
    35,      # The Time Machine, Wells
    36,      # The War of the Worlds, Wells
    8492,    # Walden, Thoreau
    205,     # Walden
    1268,    # The Crown of Wild Olive, Ruskin
    11400,   # The Antichrist, Nietzsche
    4363,    # Thus Spake Zarathustra, Nietzsche
    1232,    # The Prince, Machiavelli
    3296,    # Confessions, Augustine
    1727,    # The Odyssey, Homer
    219,     # Heart of Darkness, Conrad
    25344,   # The Scarlet Letter, Hawthorne
    140,     # The Jungle, Sinclair
    16389,   # The Awakening, Chopin
    1184,    # The Count of Monte Cristo, Dumas
    1257,    # The Three Musketeers, Dumas
    16,      # Peter Pan, Barrie
    164,     # 20,000 Leagues Under the Sea, Verne
    103,     # Around the World in 80 Days, Verne
    768,     # Wuthering Heights, Bronte
    1260,    # Jane Eyre, Bronte
    600,     # Notes from the Underground, Dostoevsky
    6593,    # History of the Decline and Fall of the Roman Empire, Gibbon
    # Math classics (often free)
    33283,   # The Calculus of Variations
    13265,   # Plane Trigonometry, Loney
    34842,   # Mathematical Analysis of Logic, Boole
    36213,   # Treatise on Differential Calculus, Todhunter
    12116,   # Plane and Spherical Trigonometry, Granville
    13700,   # Theory of the Zeta-Function?
    # Bertrand Russell
    2529,    # The Problems of Philosophy, Russell
    5827,    # The Problems of Philosophy (alt)
    44932,   # The Analysis of Mind, Russell
    25447,   # Mathematical Recreations
    # Free-form: round out to ~100
    1080,    # A Modest Proposal, Swift
    829,     # Gulliver's Travels, Swift
    36,      # The War of the Worlds, Wells
    35,      # The Time Machine, Wells
    1184,    # Count of Monte Cristo
    33,      # The Scarlet Letter
    11,      # Alice in Wonderland
    12,      # Through the Looking Glass
    345,     # Dracula
    98,      # Tale of Two Cities
    2701,    # Moby Dick
    1399,    # Anna Karenina
    74,      # Tom Sawyer
    74,      # Tom Sawyer
    1727,    # Odyssey
    6130,    # Iliad
]
TOP_100_IDS = list(dict.fromkeys(TOP_100_IDS))  # dedup, preserve order


def log_event(event: str, **fields):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / f"fetch_gutenberg_{time.strftime('%Y-%m-%d')}.jsonl"
    rec = {"ts": time.time(), "event": event, **fields}
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, default=str) + "\n")


def url_for(book_id: int) -> str:
    """Project Gutenberg canonical plain-text URL."""
    return f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"


def out_path(book_id: int) -> Path:
    return CORPUS_ROOT / f"pg{book_id:05d}.txt"


def fetch_one(book_id: int, timeout: float = 20.0) -> Tuple[bool, str]:
    """Download one book. Returns (ok, message). Skips if already on disk."""
    p = out_path(book_id)
    if p.exists() and p.stat().st_size > 1000:
        return True, f"skip-exists ({p.stat().st_size:,} bytes)"
    url = url_for(book_id)
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "CK-Coherence-Keeper/1.0 (private research)"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
            if len(data) < 1000:
                return False, f"too-small ({len(data)} bytes)"
            p.write_bytes(data)
            return True, f"ok ({len(data):,} bytes)"
    except urllib.error.HTTPError as e:
        return False, f"http-{e.code}"
    except urllib.error.URLError as e:
        return False, f"url-error: {e.reason}"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def fetch_range(start: int, end: int, sleep_s: float = 1.0) -> None:
    """Fetch every book ID in [start, end). Skip already-on-disk."""
    CORPUS_ROOT.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    ok = 0
    fail = 0
    skip = 0
    for bid in range(start, end):
        success, msg = fetch_one(bid)
        if success and "skip" in msg:
            skip += 1
        elif success:
            ok += 1
            log_event("fetch_ok", book_id=bid, msg=msg)
            if ok % 10 == 0:
                print(f"  ok={ok} fail={fail} skip={skip}  last={bid} ({msg})")
        else:
            fail += 1
            log_event("fetch_fail", book_id=bid, msg=msg)
        # Rate limit: 1 req/sec to be polite to Gutenberg
        time.sleep(sleep_s)
    print(f"[fetch_gutenberg] range {start}-{end}: ok={ok} fail={fail} skip={skip}")


def fetch_top_100(sleep_s: float = 1.0) -> None:
    CORPUS_ROOT.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    ok = 0
    fail = 0
    skip = 0
    for bid in TOP_100_IDS:
        success, msg = fetch_one(bid)
        if success and "skip" in msg:
            skip += 1
        elif success:
            ok += 1
            log_event("fetch_ok", book_id=bid, msg=msg, batch="top_100")
            print(f"  + pg{bid}: {msg}")
        else:
            fail += 1
            log_event("fetch_fail", book_id=bid, msg=msg, batch="top_100")
            print(f"  - pg{bid}: {msg}")
        time.sleep(sleep_s)
    print(f"[fetch_gutenberg top_100] ok={ok} fail={fail} skip={skip}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=int, help="first book ID (inclusive)")
    ap.add_argument("--end", type=int, help="last book ID (exclusive)")
    ap.add_argument("--top-100", action="store_true",
                    help="fetch a curated list of 100 foundational books first")
    ap.add_argument("--sleep", type=float, default=1.0,
                    help="seconds between requests (default: 1.0)")
    args = ap.parse_args()

    if args.top_100:
        fetch_top_100(sleep_s=args.sleep)
        return 0
    if args.start is None or args.end is None:
        print("Usage: --top-100  OR  --start N --end M", file=sys.stderr)
        return 2
    fetch_range(args.start, args.end, sleep_s=args.sleep)
    return 0


if __name__ == "__main__":
    sys.exit(main())
