"""gutenberg_fetch.py -- THE GROCERY RUN: bulk-fetch ~10K public-domain
books from Project Gutenberg's official PGLAF mirror into CK's shelf.

Authorized by Brayden 2026-06-11 ("i thought i gave you the keys...
gute it"). Polite: identified UA, sequential-with-small-pool (8
threads), official mirror built for harvesting, resumable (skips
existing), failures logged and skipped.

Books land in external_corpora/books/ as pg{id:05d}.txt -- same naming
as the existing shelf, so the reader daemon and fabric see ONE library.

  python gutenberg_fetch.py [max_id]      (default 14000 -> ~10-11K hits)
"""
import io
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
BOOKS = os.path.join(ROOT, "external_corpora", "books")
MAX_ID = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() \
    else 14000
MIRROR = "https://gutenberg.pglaf.org"
UA = {"User-Agent": "CK-library-builder/1.0 (personal research; "
                    "brayden@7site.io)"}


def gpath(n):
    s = str(n)
    pre = "/".join(s[:-1]) if len(s) > 1 else "0"
    return f"{pre}/{n}"


def fetch_one(n):
    out = os.path.join(BOOKS, f"pg{n:05d}.txt")
    if os.path.exists(out):
        return "have"
    base = f"{MIRROR}/{gpath(n)}"
    for suffix in (f"{n}-0.txt", f"{n}.txt", f"{n}-8.txt"):
        try:
            r = requests.get(f"{base}/{suffix}", headers=UA, timeout=25)
            if r.status_code == 200 and len(r.content) > 20_000:
                tmp = out + ".part"
                with io.open(tmp, "wb") as f:
                    f.write(r.content)
                os.replace(tmp, out)
                return "got"
        except requests.RequestException:
            pass
    return "miss"


def main():
    os.makedirs(BOOKS, exist_ok=True)
    have0 = len([f for f in os.listdir(BOOKS) if f.endswith(".txt")])
    print(f"shelf before: {have0} books; fetching IDs 1..{MAX_ID} "
          f"from {MIRROR} (8 threads, resumable)", flush=True)
    t0 = time.time()
    got = miss = have = 0
    ids = list(range(1, MAX_ID + 1))
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(fetch_one, n): n for n in ids}
        for i, fut in enumerate(as_completed(futs)):
            r = fut.result()
            got += r == "got"; miss += r == "miss"; have += r == "have"
            if (i + 1) % 500 == 0:
                rate = got / max(1e-9, time.time() - t0) * 60
                print(f"  [{i+1}/{len(ids)}] +{got} new, {miss} miss "
                      f"({rate:.0f} books/min dl) "
                      f"({(time.time()-t0)/60:.0f} min)", flush=True)
    have1 = len([f for f in os.listdir(BOOKS) if f.endswith(".txt")])
    gb = sum(os.path.getsize(os.path.join(BOOKS, f))
             for f in os.listdir(BOOKS) if f.endswith(".txt")) / 1e9
    print(f"\nGROCERIES DELIVERED: shelf {have0} -> {have1} books "
          f"({gb:.1f} GB) in {(time.time()-t0)/60:.0f} min; "
          f"{miss} IDs unavailable (normal).", flush=True)
    print("the reader daemon eats these at ~500 books/min; the hourly "
          "keepgoing cycle (or: python ck_reader_daemon.py 99999) "
          "does the rest.", flush=True)


if __name__ == "__main__":
    main()
