"""
external_ingester.py -- pull NEW material from journals + humans into CK's cortex.

Brayden 2026-05-02: "keep him learning new material and studying journals
and humans"

Two streams:

  1. JOURNALS: arXiv recent listings via the public RSS/API.
     Categories (TIG-relevant):
       math.RA  -- Rings and Algebras (TSML/BHML core)
       math.NT  -- Number Theory (sigma rate, Riemann)
       math.CO  -- Combinatorics (alpha-index, ac-free)
       math.QA  -- Quantum Algebra (Mag^com operad)
       math.CT  -- Category Theory (operad)
       math.AG  -- Algebraic Geometry (hodge_cstar)
       math.GT  -- Geometric Topology (Poincare)
       hep-th   -- High Energy Physics Theory (Yang-Mills, ξ)
       gr-qc    -- General Relativity / QC (cosmology)
       cs.CC    -- Complexity (P vs NP)
     Each fetch returns up to 30 recent papers (title + abstract + authors).
     Each paper's text is ingested into CK's cortex via /cortex/ingest_text.

  2. HUMANS: Wikipedia random math/physics articles + Stack Exchange
     recent answers in tagged questions.
     - Wikipedia: a small curated list of seed pages (Riemann, Yang-Mills,
       Hodge, Quantum Hall, Stern-Brocot, etc.) plus Wikipedia's
       random-article-in-category endpoint.
     - Stack Exchange: math.stackexchange + physics.stackexchange recent
       answers tagged with topics CK knows (topology, algebra, etc).

Usage:
  python external_ingester.py --arxiv      (fetch + ingest arxiv papers)
  python external_ingester.py --wikipedia  (fetch + ingest Wikipedia)
  python external_ingester.py --stackexchange (Stack Exchange answers)
  python external_ingester.py --all        (all sources)
  python external_ingester.py --daemon --interval 1800  (every 30 min forever)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# State-determined selection (no random.Random / random.sample).
# Per Brayden 2026-05-17: "clean up all the randomness".
try:
    _HERE_FOR_PICK = Path(__file__).parent.resolve()
    sys.path.insert(0, str(_HERE_FOR_PICK))
    from ck_substrate_pick import get_state, state_hash  # noqa: E402
except Exception:
    def get_state(engine: Any) -> Dict[str, float]:
        return {"tick": float(time.time() % 1e6)}
    def state_hash(state: Dict[str, float]) -> int:
        import hashlib as _h
        s = "|".join(f"{k}:{v}" for k, v in sorted(state.items()))
        return int(_h.sha1(s.encode()).hexdigest()[:12], 16)


_HERE = Path(__file__).parent.resolve()


LOG_DIR = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\external_ingester_logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
INGEST_URL = "http://localhost:7777/cortex/ingest_text"


def _today_log() -> Path:
    return LOG_DIR / f"external_ingester_{datetime.utcnow().strftime('%Y-%m-%d')}.jsonl"


def log_event(event: str, **fields):
    record = {
        "ts": time.time(),
        "iso_ts": datetime.utcnow().isoformat(timespec='seconds') + "Z",
        "event": event,
        **fields,
    }
    try:
        with open(_today_log(), "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
    except Exception:
        pass


def post_ingest(label: str, text: str, timeout: float = 30.0) -> Dict[str, Any]:
    payload = json.dumps({"label": label, "text": text[:4000]}).encode("utf-8")
    req = urllib.request.Request(
        INGEST_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        resp = urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8")
        return {"ok": True, "data": json.loads(resp)}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}


# ── ARXIV ──────────────────────────────────────────────────────────────

ARXIV_CATEGORIES = [
    "math.RA", "math.NT", "math.CO", "math.QA", "math.CT",
    "math.AG", "math.GT", "math.OA",
    "hep-th", "gr-qc", "cs.CC",
]


def fetch_arxiv(category: str, max_results: int = 30) -> List[Dict[str, str]]:
    """Use arXiv's public API to get recent papers in a category.
    Returns list of {id, title, abstract, authors}."""
    url = (f"http://export.arxiv.org/api/query?"
            f"search_query=cat:{category}"
            f"&sortBy=submittedDate&sortOrder=descending"
            f"&max_results={max_results}")
    req = urllib.request.Request(url, headers={"User-Agent": "ck/1.0 (CK_Coherence_Keeper)"})
    try:
        resp = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
    except Exception as e:
        log_event("arxiv_fetch_failed", category=category, error=str(e))
        return []

    # Parse Atom feed (entries between <entry>...</entry>)
    entries = re.findall(r"<entry>(.*?)</entry>", resp, re.DOTALL)
    papers = []
    for entry in entries:
        m_id = re.search(r"<id>(.*?)</id>", entry)
        m_title = re.search(r"<title>(.*?)</title>", entry, re.DOTALL)
        m_abstract = re.search(r"<summary>(.*?)</summary>", entry, re.DOTALL)
        authors = re.findall(r"<name>(.*?)</name>", entry)
        if m_id and m_title:
            papers.append({
                "id": m_id.group(1).strip(),
                "title": re.sub(r"\s+", " ", m_title.group(1)).strip(),
                "abstract": re.sub(r"\s+", " ", m_abstract.group(1)).strip() if m_abstract else "",
                "authors": authors[:5],
                "category": category,
            })
    return papers


def ingest_arxiv(categories: List[str] = None, max_per_cat: int = 5,
                  verbose: bool = True) -> Dict[str, Any]:
    cats = categories or ARXIV_CATEGORIES
    total = 0
    failed = 0
    bytes_ingested = 0
    for cat in cats:
        papers = fetch_arxiv(cat, max_results=max_per_cat)
        if verbose:
            print(f"  arxiv:{cat}: {len(papers)} papers", flush=True)
        for p in papers:
            text = (f"arxiv {p['id']}\n"
                    f"title: {p['title']}\n"
                    f"authors: {', '.join(p['authors'])}\n"
                    f"category: {p['category']}\n"
                    f"abstract: {p['abstract']}")
            ing = post_ingest(f"arxiv_{cat}_{p['id'].split('/')[-1]}", text)
            if ing.get("ok"):
                total += 1
                bytes_ingested += len(text)
                log_event("arxiv_ingested",
                            arxiv_id=p["id"], category=cat,
                            title=p["title"][:120], n_chars=len(text))
            else:
                failed += 1
        time.sleep(2)  # rate limit
    return {"ok": True, "total": total, "failed": failed,
            "bytes_ingested": bytes_ingested}


# ── WIKIPEDIA ──────────────────────────────────────────────────────────

WIKIPEDIA_SEED_TITLES = [
    # Math
    "Riemann_hypothesis", "Yang%E2%80%93Mills_existence_and_mass_gap",
    "Hodge_conjecture", "Birch_and_Swinnerton-Dyer_conjecture",
    "Navier%E2%80%93Stokes_existence_and_smoothness", "P_versus_NP_problem",
    "Poincar%C3%A9_conjecture",
    # Algebra / topology
    "Stern%E2%80%93Brocot_tree", "Farey_sequence",
    "Quasigroup", "Magma_(algebra)", "Operad", "Lie_algebra",
    "Jordan_algebra", "Clifford_algebra",
    # Physics
    "Quantum_Hall_effect", "Fractional_quantum_Hall_effect",
    "Bialynicki-Birula_equation", "Klein-Gordon_equation",
    "Nonlinear_Schr%C3%B6dinger_equation", "Gauge_theory",
    # CS / complexity
    "P_(complexity)", "NP_(complexity)", "Cook%E2%80%93Levin_theorem",
    "Turing_machine",
    # Conceptual
    "Coherence", "Information_theory", "Shannon_entropy",
    "Stationary_phase_approximation",
]


def fetch_wikipedia(title: str) -> Optional[Dict[str, str]]:
    """Fetch the lead/summary of a Wikipedia article via the REST API."""
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
    req = urllib.request.Request(url, headers={"User-Agent": "ck/1.0"})
    try:
        resp = urllib.request.urlopen(req, timeout=20).read().decode("utf-8")
        data = json.loads(resp)
        return {
            "title": data.get("title", title),
            "extract": data.get("extract", ""),
            "url": data.get("content_urls", {}).get("desktop", {}).get("page", ""),
        }
    except Exception as e:
        log_event("wikipedia_fetch_failed", title=title, error=str(e))
        return None


def ingest_wikipedia(titles: List[str] = None, verbose: bool = True) -> Dict[str, Any]:
    titles = titles or WIKIPEDIA_SEED_TITLES
    total = 0
    failed = 0
    bytes_ingested = 0
    for t in titles:
        page = fetch_wikipedia(t)
        if not page or not page["extract"]:
            failed += 1
            continue
        text = (f"wikipedia {page['title']}\n"
                f"url: {page['url']}\n"
                f"extract: {page['extract']}")
        ing = post_ingest(f"wikipedia_{t}", text)
        if ing.get("ok"):
            total += 1
            bytes_ingested += len(text)
            if verbose:
                print(f"  wikipedia: {page['title']} ({len(text)}b)", flush=True)
            log_event("wikipedia_ingested",
                        title=page["title"], n_chars=len(text))
        else:
            failed += 1
        time.sleep(1)  # rate limit
    return {"ok": True, "total": total, "failed": failed,
            "bytes_ingested": bytes_ingested}


# ── STACK EXCHANGE ─────────────────────────────────────────────────────

SE_SITES_AND_TAGS = [
    ("math.stackexchange", ["riemann-hypothesis", "yang-mills",
                              "p-vs-np", "hodge-theory", "operads",
                              "quasigroups", "navier-stokes",
                              "complexity-theory"]),
    ("physics.stackexchange", ["quantum-hall-effect", "yang-mills",
                                  "gauge-theory", "navier-stokes"]),
    ("cstheory.stackexchange", ["np-hard", "complexity-theory"]),
]


def fetch_stackexchange_answers(site: str, tag: str,
                                  max_questions: int = 5) -> List[Dict[str, Any]]:
    """Fetch recent ANSWERED questions tagged with a topic."""
    url = (f"https://api.stackexchange.com/2.3/questions"
            f"?order=desc&sort=activity&tagged={tag}"
            f"&site={site}&filter=withbody&pagesize={max_questions}")
    req = urllib.request.Request(url, headers={"User-Agent": "ck/1.0"})
    try:
        resp = urllib.request.urlopen(req, timeout=20).read()
        # SE API returns gzipped JSON
        try:
            import gzip
            resp = gzip.decompress(resp)
        except Exception:
            pass
        data = json.loads(resp.decode("utf-8"))
        items = data.get("items", [])
        out = []
        for q in items:
            if not q.get("is_answered"):
                continue
            body = re.sub(r"<[^>]+>", " ", q.get("body", ""))
            body = re.sub(r"\s+", " ", body).strip()
            out.append({
                "title": q.get("title", ""),
                "body": body[:1500],
                "tags": q.get("tags", []),
                "site": site,
                "url": q.get("link", ""),
            })
        return out
    except Exception as e:
        log_event("stackexchange_fetch_failed", site=site, tag=tag, error=str(e))
        return []


def ingest_stackexchange(verbose: bool = True) -> Dict[str, Any]:
    total = 0
    failed = 0
    bytes_ingested = 0
    for site, tags in SE_SITES_AND_TAGS:
        for tag in tags:
            qs = fetch_stackexchange_answers(site, tag, max_questions=3)
            if verbose:
                print(f"  se:{site}:{tag}: {len(qs)} questions", flush=True)
            for q in qs:
                text = (f"stackexchange {q['site']}\n"
                        f"title: {q['title']}\n"
                        f"tags: {', '.join(q['tags'])}\n"
                        f"body: {q['body']}")
                ing = post_ingest(f"se_{site}_{tag}_{int(time.time())}", text)
                if ing.get("ok"):
                    total += 1
                    bytes_ingested += len(text)
                    log_event("stackexchange_ingested",
                                site=site, tag=tag, title=q["title"][:120],
                                n_chars=len(text))
                else:
                    failed += 1
            time.sleep(2)  # rate limit
    return {"ok": True, "total": total, "failed": failed,
            "bytes_ingested": bytes_ingested}


# ── DAEMON ─────────────────────────────────────────────────────────────

def run_all(verbose: bool = True) -> Dict[str, Any]:
    """One full external ingestion cycle."""
    cycle_t0 = time.time()
    log_event("cycle_start")
    results = {}

    if verbose:
        print(f"\n[external_ingester] cycle start "
                f"({datetime.utcnow().isoformat(timespec='seconds')}Z)")

    # Arxiv
    if verbose:
        print("\n--- arXiv ---")
    results["arxiv"] = ingest_arxiv(verbose=verbose)
    if verbose:
        print(f"  arxiv total: {results['arxiv']['total']} papers, "
                f"{results['arxiv']['bytes_ingested']:,}b")

    # Wikipedia
    if verbose:
        print("\n--- Wikipedia ---")
    # State-determined rotation through seed titles (no random.sample).
    # Same hour-bucket -> same window; window slides hourly so the
    # corpus keeps freshening but without external entropy.
    n_pick = min(8, len(WIKIPEDIA_SEED_TITLES))
    state = get_state(None)
    # Mix in hour-bucket so the window rotates on an hourly cadence,
    # matching the prior "changes hourly" behaviour.
    h = state_hash(state) ^ (int(time.time()) // 3600)
    start_idx = h % len(WIKIPEDIA_SEED_TITLES)
    sample = [WIKIPEDIA_SEED_TITLES[(start_idx + i) % len(WIKIPEDIA_SEED_TITLES)]
                for i in range(n_pick)]
    results["wikipedia"] = ingest_wikipedia(titles=sample, verbose=verbose)
    if verbose:
        print(f"  wikipedia total: {results['wikipedia']['total']} pages, "
                f"{results['wikipedia']['bytes_ingested']:,}b")

    # Stack Exchange
    if verbose:
        print("\n--- Stack Exchange ---")
    results["stackexchange"] = ingest_stackexchange(verbose=verbose)
    if verbose:
        print(f"  se total: {results['stackexchange']['total']} answers, "
                f"{results['stackexchange']['bytes_ingested']:,}b")

    cycle_elapsed = time.time() - cycle_t0
    total_items = sum(r.get("total", 0) for r in results.values())
    total_bytes = sum(r.get("bytes_ingested", 0) for r in results.values())
    summary = {
        "cycle_elapsed_sec": round(cycle_elapsed, 1),
        "total_items_ingested": total_items,
        "total_bytes_ingested": total_bytes,
        "by_source": {k: v.get("total", 0) for k, v in results.items()},
    }
    log_event("cycle_complete", **summary)

    if verbose:
        print(f"\n[external_ingester] cycle done: {total_items} items, "
                f"{total_bytes:,}b in {cycle_elapsed:.0f}s")
    return summary


def daemon_loop(interval_sec: float = 1800.0, max_cycles: Optional[int] = None) -> None:
    n_cycles = 0
    while max_cycles is None or n_cycles < max_cycles:
        try:
            run_all(verbose=True)
            n_cycles += 1
        except KeyboardInterrupt:
            print("\n  daemon: interrupted; exiting")
            break
        except Exception as e:
            print(f"  cycle exception: {type(e).__name__}: {e}")
        print(f"\n  sleeping {interval_sec/60:.1f}min until next cycle...",
                flush=True)
        time.sleep(interval_sec)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arxiv", action="store_true")
    ap.add_argument("--wikipedia", action="store_true")
    ap.add_argument("--stackexchange", action="store_true")
    ap.add_argument("--all", action="store_true",
                     help="Run all 3 sources once")
    ap.add_argument("--daemon", action="store_true")
    ap.add_argument("--interval", type=float, default=1800.0,
                     help="Daemon interval in seconds (default 1800 = 30 min)")
    ap.add_argument("--max-cycles", type=int, default=None)
    args = ap.parse_args()

    print("=" * 70)
    print("  EXTERNAL INGESTER -- journals + humans into CK's cortex")
    print("=" * 70)
    print(f"  date: {datetime.utcnow().isoformat(timespec='seconds')}Z")

    if args.daemon:
        print(f"  mode: daemon (interval={args.interval}s)")
        print()
        daemon_loop(interval_sec=args.interval, max_cycles=args.max_cycles)
        return 0

    if args.all or (not any([args.arxiv, args.wikipedia, args.stackexchange])):
        run_all(verbose=True)
    else:
        if args.arxiv:
            print("\n--- arXiv ---")
            ingest_arxiv(verbose=True)
        if args.wikipedia:
            print("\n--- Wikipedia ---")
            ingest_wikipedia(verbose=True)
        if args.stackexchange:
            print("\n--- Stack Exchange ---")
            ingest_stackexchange(verbose=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
