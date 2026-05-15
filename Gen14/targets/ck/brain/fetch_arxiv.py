"""fetch_arxiv.py -- harvest math + physics papers from arXiv.

Brayden 2026-05-15:
  "open him up to the world"

Uses arXiv's OAI-PMH-like ATOM API (http://export.arxiv.org/api/query).
We pull papers from math.CO, math.NT, math.AG, math.PR, math.LO,
and select physics (hep-th, gr-qc, math-ph). Each paper gets:
  - title
  - abstract (the prose CK can extract definitions from)
  - authors
  - id (arxiv ID)
  - categories

Stored as one .txt per paper under external_corpora/arxiv/<cat>/<id>.txt,
plus a manifest JSONL. The school daemon picks up new files.

Rate limit: per arxiv terms, 1 req every 3 sec, 2000 results/window max.

Restartable: skips IDs already on disk.

Usage:
  python fetch_arxiv.py --categories math.CO,math.NT --max 500
  python fetch_arxiv.py --recent          # last 7 days, all default cats
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import List, Optional
from xml.etree import ElementTree as ET


CORPUS_ROOT = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\external_corpora\arxiv")
LOG_DIR = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\external_corpora\_logs")

ARXIV_API = "http://export.arxiv.org/api/query"

DEFAULT_CATEGORIES = [
    # Math (broad coverage of TIG-relevant areas)
    "math.CO",  # combinatorics
    "math.NT",  # number theory
    "math.AG",  # algebraic geometry
    "math.PR",  # probability
    "math.LO",  # logic
    "math.GR",  # group theory
    "math.RA",  # rings and algebras
    "math.QA",  # quantum algebra
    "math.RT",  # representation theory
    "math.DG",  # differential geometry
    "math.AP",  # analysis of PDEs
    # Physics (TIG also touches these)
    "hep-th",   # high-energy theory
    "gr-qc",    # general relativity
    "math-ph",  # mathematical physics
    "quant-ph", # quantum
]

NS = {"atom": "http://www.w3.org/2005/Atom",
      "arxiv": "http://arxiv.org/schemas/atom"}


def log_event(event: str, **fields):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    p = LOG_DIR / f"fetch_arxiv_{time.strftime('%Y-%m-%d')}.jsonl"
    with open(p, "a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": time.time(), "event": event, **fields},
                            default=str) + "\n")


def safe_id(arxiv_id: str) -> str:
    """Make an arxiv ID filesystem-safe."""
    # IDs look like '2401.12345v2' or 'math/0507231'
    return re.sub(r"[^a-zA-Z0-9._-]", "_", arxiv_id)


def category_dir(cat: str) -> Path:
    d = CORPUS_ROOT / cat.replace(".", "_").replace("-", "_")
    d.mkdir(parents=True, exist_ok=True)
    return d


def fetch_category(category: str, max_results: int = 100,
                    start: int = 0, sort: str = "submittedDate") -> int:
    """Fetch up to max_results papers from a category. Returns # saved."""
    params = {
        "search_query": f"cat:{category}",
        "start": start,
        "max_results": min(max_results, 100),  # arxiv hard-caps at 100/page
        "sortBy": sort,
        "sortOrder": "descending",
    }
    url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(
        url, headers={"User-Agent": "CK-Coherence-Keeper/1.0"})
    cdir = category_dir(category)
    saved = 0
    try:
        with urllib.request.urlopen(req, timeout=30.0) as resp:
            xml_bytes = resp.read()
        root = ET.fromstring(xml_bytes)
        for entry in root.findall("atom:entry", NS):
            arxiv_id_url = entry.findtext("atom:id", "", NS)
            arxiv_id = arxiv_id_url.rsplit("/", 1)[-1] if arxiv_id_url else ""
            if not arxiv_id:
                continue
            title = (entry.findtext("atom:title", "", NS) or "").strip()
            abstract = (entry.findtext("atom:summary", "", NS) or "").strip()
            authors = [a.findtext("atom:name", "", NS)
                       for a in entry.findall("atom:author", NS)]
            published = entry.findtext("atom:published", "", NS) or ""

            fid = safe_id(arxiv_id)
            out = cdir / f"{fid}.txt"
            if out.exists() and out.stat().st_size > 200:
                continue

            # Compose a clean text record.  CK's extractor reads prose,
            # so we put title/authors/abstract in a definition-friendly
            # layout.
            body = (
                f"Title: {title}\n\n"
                f"Authors: {', '.join(authors)}\n\n"
                f"arXiv ID: {arxiv_id}\n"
                f"Category: {category}\n"
                f"Published: {published}\n\n"
                f"Abstract: {abstract}\n"
            )
            out.write_text(body, encoding="utf-8")
            saved += 1
            log_event("arxiv_saved", category=category, arxiv_id=arxiv_id,
                      bytes=len(body))
        return saved
    except Exception as e:
        log_event("arxiv_error", category=category, error=str(e))
        return saved


def fetch_default(max_per_cat: int = 100, sleep_s: float = 3.5) -> None:
    """Fetch the most recent <max_per_cat> from each default category."""
    CORPUS_ROOT.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    total = 0
    for cat in DEFAULT_CATEGORIES:
        print(f"[fetch_arxiv] {cat}: pulling up to {max_per_cat}...")
        n = fetch_category(cat, max_results=max_per_cat)
        total += n
        print(f"  + {n} new")
        time.sleep(sleep_s)  # arxiv asks for >=3s between calls
    print(f"[fetch_arxiv] total new papers saved: {total}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--categories", default=None,
                    help="comma-separated list (default: all 15 cats)")
    ap.add_argument("--max", type=int, default=100,
                    help="max papers per category (default 100, arxiv hard cap)")
    ap.add_argument("--sleep", type=float, default=3.5)
    ap.add_argument("--start", type=int, default=0,
                    help="pagination offset for a single category")
    args = ap.parse_args()

    if args.categories:
        cats = [c.strip() for c in args.categories.split(",") if c.strip()]
    else:
        cats = DEFAULT_CATEGORIES

    CORPUS_ROOT.mkdir(parents=True, exist_ok=True)
    total = 0
    for cat in cats:
        print(f"[fetch_arxiv] {cat}: pulling up to {args.max} (start={args.start})...")
        n = fetch_category(cat, max_results=args.max, start=args.start)
        total += n
        print(f"  + {n} new")
        time.sleep(args.sleep)
    print(f"[fetch_arxiv] DONE. total new papers: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
