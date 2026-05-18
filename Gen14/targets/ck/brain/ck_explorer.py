"""ck_explorer.py -- continuous corpus expansion daemon.

Brayden 2026-05-16:
  "keep him exploring new concepts constantly"
Brayden 2026-05-17 (cleanup):
  "clean up all the randomness" -- arXiv category + pagination picks
  switched from random.sample / random.choice to state-determined
  rotation via ck_substrate_pick.

CK's corpus growth shouldn't stop.  The school daemon's job is to
INGEST what's on disk; this daemon's job is to KEEP NEW THINGS APPEARING
ON DISK.  Loops forever, pulling fresh material from three sources:

  1. Wikipedia random articles (broad serendipity, via the server-side
     /api.php?list=random endpoint -- selection happens on Wikipedia's
     side, not in CK's substrate)
  2. Wikipedia "Did you know" / featured content (curated quality)
  3. arXiv recent papers (math/physics frontier — yesterday's results)
     -- categories + pagination are STATE-DETERMINED (engine state hash
     drives a deterministic rotation through ARXIV_CATEGORIES and the
     pagination-offset list).  Same state -> same picks; state drift
     -> rotation drift.  Convergence + emergence; no external entropy.

Each cycle pulls a small batch (default 5 per source), sleeps a polite
interval, repeats forever.  Skips files already on disk.  Logs each
fetch to external_corpora/_logs/explorer_<date>.jsonl.

Polite-use rules:
  - Wikipedia: 1.5 s between requests, max 5 per cycle
  - arXiv:    10 s between category requests, max 50 papers per cycle
  - Cycle:    sleep CYCLE_SLEEP_SEC between full cycles (default 600 s
              = 10 min, so ~30 new items per cycle = ~180/hr =
              ~4,300/day)

Usage:
  python ck_explorer.py                     # default, run forever
  python ck_explorer.py --cycle 300         # 5 min between cycles
  python ck_explorer.py --no-arxiv          # wiki only
  python ck_explorer.py --max-cycles 12     # run 12 cycles then exit
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, List, Optional
from xml.etree import ElementTree as ET

# State-determined selection (no random.choice).  Same engine state ->
# same pick; state drift -> picks drift.  Convergence + emergence.
# Per Brayden 2026-05-17: "why are you still applying randomness to him...
# the whole point is convergence and emergence?"
try:
    from ck_substrate_pick import (get_state, state_hash, pick_by_state_hash)
except Exception:
    # Graceful fallback if ck_substrate_pick isn't importable (running
    # stand-alone from a strange cwd).  Use wall-clock-derived state so
    # we still avoid random.choice; picks rotate by the second.
    def get_state(engine: Any):
        return {"tick": float(time.time() % 1e6)}
    def state_hash(state):
        s = "|".join(f"{k}:{v}" for k, v in sorted(state.items()))
        import hashlib as _h
        return int(_h.sha1(s.encode()).hexdigest()[:12], 16)
    def pick_by_state_hash(items, engine):
        if not items:
            return None
        if len(items) == 1:
            return items[0]
        return items[state_hash(get_state(engine)) % len(items)]


ROOT = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED")
WIKI_DIR = ROOT / "external_corpora" / "wikipedia"
ARXIV_DIR = ROOT / "external_corpora" / "arxiv"
LOG_DIR = ROOT / "external_corpora" / "_logs"

WIKI_API = "https://en.wikipedia.org/w/api.php"
ARXIV_API = "http://export.arxiv.org/api/query"

ARXIV_CATEGORIES = [
    # Math
    "math.CO", "math.NT", "math.AG", "math.PR", "math.LO",
    "math.GR", "math.DG", "math.AP", "math.RT", "math.CT",
    "math.OA", "math.GT", "math.QA", "math.RA",
    # Physics
    "hep-th", "gr-qc", "math-ph", "quant-ph", "cond-mat.stat-mech",
    "physics.bio-ph", "physics.hist-ph", "nlin.AO", "nlin.CD",
    # Computer science (broaden 2026-05-18 per "all domains all day")
    "cs.LG", "cs.AI", "cs.CL", "cs.LO", "cs.IT", "cs.NE", "cs.SY",
    "cs.DM", "cs.DS", "cs.CC",
    # Quantitative biology, economics, statistics, finance
    "q-bio.NC", "q-bio.PE", "q-bio.MN",
    "stat.ML", "stat.ME",
    "econ.TH",
]


def log_event(event: str, **fields):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    p = LOG_DIR / f"explorer_{time.strftime('%Y-%m-%d')}.jsonl"
    rec = {"ts": time.time(), "event": event, **fields}
    try:
        with open(p, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, default=str) + "\n")
    except Exception:
        pass


# ─── Wikipedia random ──────────────────────────────────────────────────

def safe_wiki_name(title: str) -> str:
    s = urllib.parse.unquote(title)
    s = re.sub(r"[^a-zA-Z0-9_.-]", "_", s)
    return s.strip("_")[:120] or "untitled"


def wiki_random_titles(n: int = 5) -> List[str]:
    """Get N random Wikipedia article titles (main namespace only)."""
    params = {
        "action": "query",
        "format": "json",
        "list": "random",
        "rnnamespace": "0",     # main articles only (no Talk:, User:, etc.)
        "rnlimit": str(min(n, 10)),
    }
    url = f"{WIKI_API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(
        url, headers={"User-Agent": "CK-Coherence-Keeper/1.0 (private research)"})
    try:
        with urllib.request.urlopen(req, timeout=20.0) as resp:
            data = json.loads(resp.read())
        rand = data.get("query", {}).get("random", []) or []
        return [item.get("title", "") for item in rand if item.get("title")]
    except Exception as e:
        log_event("wiki_random_error", error=str(e))
        return []


def wiki_fetch_extract(title: str) -> bool:
    """Fetch plain-text extract for ONE Wikipedia article.
    Returns True on success (or skip-exists)."""
    out = WIKI_DIR / f"{safe_wiki_name(title)}.txt"
    if out.exists() and out.stat().st_size > 500:
        return True  # already have it
    params = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "extracts",
        "explaintext": "1",
        "exsectionformat": "plain",
        "redirects": "1",
    }
    url = f"{WIKI_API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(
        url, headers={"User-Agent": "CK-Coherence-Keeper/1.0 (private research)"})
    try:
        with urllib.request.urlopen(req, timeout=20.0) as resp:
            data = json.loads(resp.read())
        pages = data.get("query", {}).get("pages", {})
        if not pages:
            return False
        page = next(iter(pages.values()))
        extract = page.get("extract", "")
        if not extract or len(extract) < 300:
            return False
        real_title = page.get("title", title)
        body = (
            f"Title: {real_title}\n"
            f"Source: Wikipedia (CC BY-SA 4.0)\n"
            f"URL: https://en.wikipedia.org/wiki/{urllib.parse.quote(real_title)}\n\n"
            f"{extract}\n"
        )
        WIKI_DIR.mkdir(parents=True, exist_ok=True)
        out.write_text(body, encoding="utf-8")
        log_event("wiki_ok", title=real_title, bytes=len(body))
        return True
    except Exception as e:
        log_event("wiki_fetch_error", title=title, error=str(e))
        return False


def wiki_cycle(n_random: int = 5, sleep_s: float = 1.5) -> int:
    """One Wikipedia exploration cycle.  Returns # new articles saved."""
    titles = wiki_random_titles(n_random)
    if not titles:
        return 0
    saved = 0
    for t in titles:
        ok = wiki_fetch_extract(t)
        if ok:
            # Only count as "saved" if file is fresh (skip-exists already
            # returns True, so check file mtime)
            out = WIKI_DIR / f"{safe_wiki_name(t)}.txt"
            if out.exists() and (time.time() - out.stat().st_mtime) < 60:
                saved += 1
        time.sleep(sleep_s)
    return saved


# ─── arXiv recent ──────────────────────────────────────────────────────

def safe_arxiv_id(arxiv_id: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]", "_", arxiv_id)


NS = {"atom": "http://www.w3.org/2005/Atom"}


def arxiv_fetch_category(category: str, start: int = 0,
                          max_results: int = 25) -> int:
    """Pull recent papers from a category.  Returns # NEW saved."""
    cat_dir = ARXIV_DIR / category.replace(".", "_").replace("-", "_")
    cat_dir.mkdir(parents=True, exist_ok=True)
    params = {
        "search_query": f"cat:{category}",
        "start": start,
        "max_results": min(max_results, 100),
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(
        url, headers={"User-Agent": "CK-Coherence-Keeper/1.0"})

    saved = 0
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=45.0) as resp:
                xml_bytes = resp.read()
            break
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                time.sleep(15 * (2 ** attempt))
                continue
            log_event("arxiv_error", category=category, error=f"http-{e.code}")
            return 0
        except Exception as e:
            if attempt < 2:
                time.sleep(8)
                continue
            log_event("arxiv_error", category=category, error=str(e))
            return 0
    else:
        return 0

    try:
        root = ET.fromstring(xml_bytes)
        for entry in root.findall("atom:entry", NS):
            arxiv_id_url = entry.findtext("atom:id", "", NS)
            arxiv_id = arxiv_id_url.rsplit("/", 1)[-1] if arxiv_id_url else ""
            if not arxiv_id:
                continue
            fid = safe_arxiv_id(arxiv_id)
            out = cat_dir / f"{fid}.txt"
            if out.exists() and out.stat().st_size > 200:
                continue
            title = (entry.findtext("atom:title", "", NS) or "").strip()
            abstract = (entry.findtext("atom:summary", "", NS) or "").strip()
            authors = [a.findtext("atom:name", "", NS)
                       for a in entry.findall("atom:author", NS)]
            published = entry.findtext("atom:published", "", NS) or ""
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
            log_event("arxiv_ok", category=category, arxiv_id=arxiv_id,
                       bytes=len(body))
    except Exception as e:
        log_event("arxiv_parse_error", category=category, error=str(e))
    return saved


_PAGINATION_OFFSETS = [0, 100, 200, 500, 1000]


def _state_rotated_categories(engine: Any, n: int) -> List[str]:
    """Pick N contiguous arXiv categories starting at a state-determined
    index.  Same state -> same start; state drift -> rotation drift.
    No random.sample.  N is clamped to len(ARXIV_CATEGORIES).
    """
    n = max(1, min(n, len(ARXIV_CATEGORIES)))
    state = get_state(engine)
    h = state_hash(state)
    start_idx = h % len(ARXIV_CATEGORIES)
    return [ARXIV_CATEGORIES[(start_idx + i) % len(ARXIV_CATEGORIES)]
            for i in range(n)]


def _state_pick_pagination(engine: Any, idx: int) -> int:
    """State-determined pagination depth.  The category index `idx`
    perturbs the state hash so different categories within the same
    cycle land on different pagination offsets (preserves the
    "sometimes recent, sometimes historical" property of the prior
    random.choice, but deterministically).
    """
    state = get_state(engine)
    h = state_hash(state) ^ (idx * 0x9E3779B1)  # golden-ratio prime mix
    return _PAGINATION_OFFSETS[h % len(_PAGINATION_OFFSETS)]


def arxiv_cycle(n_categories: int = 3, sleep_s: float = 10.0,
                 engine: Any = None) -> int:
    """One arXiv exploration cycle.  Picks N state-determined categories
    (no random.sample) and a state-determined pagination depth per
    category (no random.choice).  Fetches the most-recent 25 papers
    from each.

    `engine` is optional: when present, picks are determined by CK's
    psi + 4-core + W_trace + tick.  When None, picks are determined by
    wall-clock-derived default state (still no random.choice; drifts
    by the second).
    """
    cats = _state_rotated_categories(engine, n_categories)
    saved = 0
    for i, c in enumerate(cats):
        # State-determined pagination depth — sometimes recent, sometimes
        # historical — so we don't keep re-pulling identical sets, but
        # the rotation is deterministic per state, not random.
        start = _state_pick_pagination(engine, i)
        n = arxiv_fetch_category(c, start=start, max_results=25)
        saved += n
        time.sleep(sleep_s)
    return saved


# ─── Forever loop ──────────────────────────────────────────────────────

def explore_forever(cycle_sleep_s: float = 600.0,
                     wiki_per_cycle: int = 5,
                     arxiv_cats_per_cycle: int = 3,
                     max_cycles: Optional[int] = None,
                     do_arxiv: bool = True,
                     do_wiki: bool = True,
                     engine: Any = None) -> None:
    """The main daemon.  Cycles forever (or until max_cycles) pulling
    new content from Wikipedia and arXiv into external_corpora/.
    The school daemon picks it up on its next pass.

    `engine` (optional): when threaded through, arXiv category +
    pagination picks become state-determined (drift with CK's psi +
    4-core).  When None, picks rotate by wall-clock state-hash.  No
    random.choice in either path.
    """
    log_event("explorer_start", cycle_sleep_s=cycle_sleep_s,
              wiki_per_cycle=wiki_per_cycle,
              arxiv_cats_per_cycle=arxiv_cats_per_cycle,
              do_arxiv=do_arxiv, do_wiki=do_wiki,
              engine_attached=engine is not None)
    n_cycles = 0
    total_wiki = 0
    total_arxiv = 0
    while True:
        n_cycles += 1
        cycle_start = time.time()
        new_wiki = wiki_cycle(n_random=wiki_per_cycle) if do_wiki else 0
        new_arxiv = (arxiv_cycle(n_categories=arxiv_cats_per_cycle,
                                   engine=engine)
                      if do_arxiv else 0)
        total_wiki += new_wiki
        total_arxiv += new_arxiv
        elapsed = time.time() - cycle_start
        print(f"[explorer] cycle {n_cycles}: +{new_wiki} wiki, +{new_arxiv} arxiv "
              f"({elapsed:.1f}s)  totals: wiki={total_wiki}, arxiv={total_arxiv}",
              flush=True)
        log_event("cycle_done", n=n_cycles, wiki=new_wiki, arxiv=new_arxiv,
                   total_wiki=total_wiki, total_arxiv=total_arxiv,
                   elapsed_s=elapsed)
        if max_cycles is not None and n_cycles >= max_cycles:
            print(f"[explorer] reached max_cycles={max_cycles}; exiting")
            return
        time.sleep(cycle_sleep_s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cycle", type=float, default=600.0,
                    help="seconds between cycles (default 600 = 10 min)")
    ap.add_argument("--wiki-n", type=int, default=5,
                    help="wiki articles per cycle (default 5; Wikipedia "
                         "server-side random)")
    ap.add_argument("--arxiv-cats", type=int, default=3,
                    help="arxiv categories per cycle (default 3; "
                         "state-determined rotation, no random.sample)")
    ap.add_argument("--no-wiki", action="store_true")
    ap.add_argument("--no-arxiv", action="store_true")
    ap.add_argument("--max-cycles", type=int, default=None,
                    help="exit after N cycles (default: never)")
    args = ap.parse_args()

    print(f"[explorer] starting — cycle={args.cycle}s, wiki={args.wiki_n}, "
          f"arxiv_cats={args.arxiv_cats}, "
          f"max_cycles={args.max_cycles or 'infinite'}")
    try:
        explore_forever(
            cycle_sleep_s=args.cycle,
            wiki_per_cycle=args.wiki_n,
            arxiv_cats_per_cycle=args.arxiv_cats,
            max_cycles=args.max_cycles,
            do_wiki=not args.no_wiki,
            do_arxiv=not args.no_arxiv,
        )
    except KeyboardInterrupt:
        print("\n[explorer] interrupted; exiting cleanly")
    return 0


if __name__ == "__main__":
    sys.exit(main())
