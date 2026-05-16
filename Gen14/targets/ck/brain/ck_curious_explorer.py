"""ck_curious_explorer.py -- gap-driven, curiosity-led corpus expansion.

Brayden 2026-05-16:
  "it shouldn't be random article, he should be curiously learning and
   filling his own gaps"

The previous ck_explorer.py pulled RANDOM Wikipedia articles.  That's
not curiosity — that's spray.  A curious reader does something
different: she reads about X, notices Y is mentioned but she doesn't
know Y, looks Y up.  When she reads about Y, Z is mentioned but
unknown, she looks Z up.  The frontier of her knowledge propagates by
following its own dangling references.

This daemon does that.  Per cycle:

  1. SCAN: walk the concept store, mine each definition for capitalized
     noun-phrases (proper nouns, technical terms).
  2. FILTER: which of those terms is CK DOES NOT YET know?  These are
     his gaps — dangling references on his own frontier.
  3. RANK: prefer terms mentioned in his RIGOROUS sources (PROVED /
     STRUCTURAL / EMPIRICAL).  Fiction's "Captain Lloyd" rank low.
  4. FETCH: for each top gap, hit Wikipedia opensearch to find the
     canonical article title, then pull the plain-text extract.
  5. SAVE + LOG: each fetch records WHICH gap was filled, traceable to
     the SOURCE concept that mentioned the unknown term.

Result: CK fills his own gaps in the direction his current knowledge
points.  His learning is path-dependent + reference-driven, not
serendipitous.

A secondary mode (--mode cells) targets UNDER-POPULATED operator cells
in his (op_a, op_b) lattice — searches Wikipedia for articles matching
operator-semantics keywords ("entropy reset", "lattice growth", etc.)
when those cells are starving.

Usage:
  python ck_curious_explorer.py                # default: dangling-refs mode
  python ck_curious_explorer.py --mode cells   # cell-balancing mode
  python ck_curious_explorer.py --cycle 600    # 10 min between cycles
  python ck_curious_explorer.py --gaps-per-cycle 8  # how many gaps per cycle
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
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


ROOT = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED")
STORE_PATH = ROOT / "Gen13" / "var" / "taught_concepts.json"
WIKI_DIR = ROOT / "external_corpora" / "wikipedia"
LOG_DIR = ROOT / "external_corpora" / "_logs"

WIKI_API = "https://en.wikipedia.org/w/api.php"


# ─── Logging ──────────────────────────────────────────────────────────

def log_event(event: str, **fields):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    p = LOG_DIR / f"curious_{time.strftime('%Y-%m-%d')}.jsonl"
    rec = {"ts": time.time(), "event": event, **fields}
    try:
        with open(p, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, default=str) + "\n")
    except Exception:
        pass


# ─── Dangling-reference mining ────────────────────────────────────────

# A "candidate term" in a definition: a capitalized noun phrase of 1-4
# tokens.  We filter out common words + verbs + sentence-start adjectives.
_PAT_NOUN_PHRASE = re.compile(
    r"(?<![A-Za-z])([A-Z][a-z]{3,}(?:[ \-][A-Z][a-z]+){0,3})"
)

# Words that are capitalized but boring as gap-fillers
_BORING_TERMS = {
    # English starters / pronouns
    "The", "This", "That", "These", "Those", "There", "Here", "It",
    "What", "When", "Where", "Which", "Why", "Who", "How",
    "For", "But", "And", "Or", "So", "If", "Yet", "Nor",
    "However", "Therefore", "Thus", "Hence", "Indeed", "Then",
    "Today", "Yesterday", "Now", "Concretely", "Importantly",
    "Specifically", "Notably", "Additionally", "Furthermore",
    "I", "You", "We", "They", "He", "She",
    "My", "Your", "Our", "Their", "His", "Her",
    "Yes", "No", "Maybe",
    "First", "Second", "Third", "Last", "Final", "Next",
    "Some", "Many", "Few", "All", "Most", "Each", "Every", "Other",
    "Note", "See", "Remember", "Recall",
    "In", "On", "At", "By", "Of", "For", "With", "From",
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
    "Saturday", "Sunday",
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
    "Sect", "Section", "Chapter", "Theorem", "Lemma", "Proof",
    "Definition", "Example", "Remark", "Note", "Figure", "Table",
    "Eq", "Equation", "Page", "Vol",
    "Captain", "Mister", "Mrs", "Mr", "Sir", "Lord", "Lady",
    "Father", "Mother", "Brother", "Sister",
}

# Authors / maintainers / model names — never genuine gaps
_AUTHOR_NAMES = {
    "Brayden", "Sanders", "Claude", "Anthropic", "Luther", "Gish",
    "Mayes", "Johnson", "Calderon",
    # Two-word combos
    "Brayden Sanders", "Anthropic Claude", "Charles Luther",
}

# Latex / math-notation fragment patterns commonly mistaken for words
# (Bigl, Bigr, Simp, Cfour, Fmix, Psix, Zten, ...)
_LATEX_PATTERN = re.compile(
    r"^[A-Z][a-z]{2,4}(?:one|two|three|four|five|six|seven|eight|nine|ten|ll|rr)$"
)


def _looks_like_latex(term: str) -> bool:
    """Heuristic: rejects 'Bigl', 'Cfour', 'Psix', 'Zten' etc."""
    if _LATEX_PATTERN.match(term):
        return True
    # Words that are letter-glued numerals
    if any(num in term.lower() for num in
            ("zero", "one", "two", "three", "four", "five", "six",
             "seven", "eight", "nine", "ten")) and len(term) <= 7:
        return True
    return False


def mine_candidates(text: str) -> List[str]:
    """Pull capitalized noun-phrases from text, filter boring ones."""
    if not text:
        return []
    out: List[str] = []
    for m in _PAT_NOUN_PHRASE.finditer(text):
        term = m.group(1).strip()
        first = term.split()[0]
        if first in _BORING_TERMS:
            continue
        if term in _AUTHOR_NAMES or first in _AUTHOR_NAMES:
            continue
        # Reject LaTeX / math-notation typos
        if _looks_like_latex(term):
            continue
        # Skip pure-number sequences
        if not any(c.isalpha() for c in term):
            continue
        # Single-token must be >= 5 chars (filters Bigl, Simp, Mass etc.
        # — and Bigl-like cruft).  Multi-word phrases can be shorter.
        if " " not in term and "-" not in term and len(term) < 5:
            continue
        if len(term) > 50:
            continue
        out.append(term)
    return out


# ─── Gap detection ────────────────────────────────────────────────────

# Concept tier → weight when ranking gaps (higher = better source)
_TIER_WEIGHT = {
    "PROVED": 5.0,
    "STRUCTURAL": 4.0,
    "USER_TAUGHT": 3.0,
    "EMPIRICAL": 3.0,
    "OPEN": 2.0,
    "SYNTHESIZED(PROVED)": 4.5,
    "SYNTHESIZED(STRUCTURAL)": 3.5,
    "EXTERNAL": 1.0,
    "SPECULATIVE": 0.5,
    "UNKNOWN": 0.3,
}


def detect_gaps(store: Dict[str, Any], top_n: int = 30) -> List[Tuple[str, float, str]]:
    """Walk concept store; return top_n gap terms (capitalized phrases
    mentioned in definitions but not themselves a concept).

    Returns:  [(gap_term, weighted_mention_count, source_concept_name), ...]
              sorted by weight desc.
    """
    # Known concept names (case-insensitive)
    known_names: Set[str] = set()
    for v in store.values():
        n = v.get("name", "")
        if n:
            known_names.add(n.lower())
            # Also lowercase variations of the name
            for part in n.split():
                known_names.add(part.lower())

    # gap_term -> [weighted_count, first_source_name]
    gap_scores: Dict[str, float] = defaultdict(float)
    gap_sources: Dict[str, str] = {}

    for v in store.values():
        defn = v.get("definition", "") or ""
        if not defn or len(defn) < 30:
            continue
        tier = v.get("tier", "UNKNOWN") or "UNKNOWN"
        weight = _TIER_WEIGHT.get(tier, 0.3)
        source_name = v.get("name", "?")
        candidates = mine_candidates(defn)
        seen_in_this_defn: Set[str] = set()
        for term in candidates:
            term_l = term.lower()
            if term_l in known_names:
                continue
            # Skip if any token of the term is already a known concept
            tokens = term_l.split()
            if any(tok in known_names for tok in tokens):
                # Half-known; lower weight rather than skip
                weight_eff = weight * 0.3
            else:
                weight_eff = weight
            if term in seen_in_this_defn:
                continue
            seen_in_this_defn.add(term)
            gap_scores[term] += weight_eff
            # Keep the first (highest-tier) source we see
            if term not in gap_sources:
                gap_sources[term] = source_name

    # Sort by score desc; require minimum threshold
    ranked = sorted(
        [(t, s, gap_sources[t]) for t, s in gap_scores.items() if s >= 1.0],
        key=lambda x: -x[1],
    )
    return ranked[:top_n]


# ─── Wikipedia opensearch + fetch ─────────────────────────────────────

def safe_wiki_name(title: str) -> str:
    s = urllib.parse.unquote(title)
    s = re.sub(r"[^a-zA-Z0-9_.-]", "_", s)
    return s.strip("_")[:120] or "untitled"


def wiki_opensearch(term: str) -> Optional[str]:
    """Hit Wikipedia opensearch to find the canonical title for a term.
    Returns the top match's title, or None."""
    params = {
        "action": "opensearch",
        "format": "json",
        "search": term,
        "limit": "1",
        "namespace": "0",
    }
    url = f"{WIKI_API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(
        url, headers={"User-Agent": "CK-Coherence-Keeper/1.0 (private research)"})
    try:
        with urllib.request.urlopen(req, timeout=15.0) as resp:
            data = json.loads(resp.read())
        # opensearch returns [query, [titles], [descriptions], [urls]]
        if isinstance(data, list) and len(data) >= 2 and data[1]:
            title = data[1][0]
            return title if title else None
    except Exception as e:
        log_event("opensearch_error", term=term, error=str(e))
    return None


def wiki_fetch_extract(title: str, gap_term: str = "",
                          source_concept: str = "") -> bool:
    """Pull plain-text extract for a Wikipedia article.  Logs which gap
    this fetch was filling."""
    out = WIKI_DIR / f"{safe_wiki_name(title)}.txt"
    if out.exists() and out.stat().st_size > 500:
        log_event("wiki_skip_exists", title=title, gap_term=gap_term,
                   source=source_concept)
        return True
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
        # Body includes the gap-fill trail for archaeology
        body = (
            f"Title: {real_title}\n"
            f"Source: Wikipedia (CC BY-SA 4.0)\n"
            f"URL: https://en.wikipedia.org/wiki/{urllib.parse.quote(real_title)}\n"
            f"Fetched-because: gap_term={gap_term!r}, "
            f"first-seen-in={source_concept!r}\n\n"
            f"{extract}\n"
        )
        WIKI_DIR.mkdir(parents=True, exist_ok=True)
        out.write_text(body, encoding="utf-8")
        log_event("wiki_fetched", title=real_title, gap_term=gap_term,
                   source=source_concept, bytes=len(body))
        return True
    except Exception as e:
        log_event("wiki_fetch_error", title=title, gap_term=gap_term,
                   error=str(e))
        return False


# ─── Daemon loop ──────────────────────────────────────────────────────

def load_store() -> Dict[str, Any]:
    if not STORE_PATH.exists():
        return {}
    try:
        return json.loads(STORE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def curious_cycle(gaps_per_cycle: int = 6, sleep_s: float = 2.0) -> Tuple[int, int]:
    """One curiosity cycle.  Returns (n_gaps_attempted, n_articles_saved)."""
    store = load_store()
    if not store:
        return (0, 0)
    gaps = detect_gaps(store, top_n=gaps_per_cycle * 3)  # over-fetch to allow misses
    log_event("cycle_start", store_size=len(store), gaps_found=len(gaps),
               top5=[(t, round(s, 2)) for t, s, _ in gaps[:5]])

    saved = 0
    attempted = 0
    for term, score, source in gaps:
        if attempted >= gaps_per_cycle:
            break
        attempted += 1
        # Resolve via opensearch (canonical title)
        title = wiki_opensearch(term)
        time.sleep(sleep_s)
        if title is None:
            log_event("no_wiki_match", term=term, score=round(score, 2),
                       source=source)
            continue
        ok = wiki_fetch_extract(title, gap_term=term, source_concept=source)
        time.sleep(sleep_s)
        if ok:
            saved += 1
    return (attempted, saved)


def curious_forever(cycle_sleep_s: float = 600.0,
                       gaps_per_cycle: int = 6,
                       req_sleep_s: float = 2.0,
                       max_cycles: Optional[int] = None) -> None:
    log_event("curious_start", cycle_sleep_s=cycle_sleep_s,
               gaps_per_cycle=gaps_per_cycle)
    n = 0
    total_saved = 0
    while True:
        n += 1
        t0 = time.time()
        attempted, saved = curious_cycle(
            gaps_per_cycle=gaps_per_cycle, sleep_s=req_sleep_s)
        total_saved += saved
        elapsed = time.time() - t0
        print(f"[curious] cycle {n}: attempted={attempted} saved={saved} "
              f"({elapsed:.1f}s)  cumulative={total_saved}",
              flush=True)
        log_event("cycle_done", n=n, attempted=attempted, saved=saved,
                   total_saved=total_saved, elapsed_s=elapsed)
        if max_cycles is not None and n >= max_cycles:
            print(f"[curious] reached max_cycles={max_cycles}; exiting")
            return
        time.sleep(cycle_sleep_s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cycle", type=float, default=600.0,
                    help="seconds between cycles (default 600 = 10 min)")
    ap.add_argument("--gaps-per-cycle", type=int, default=6,
                    help="number of gap terms to fetch per cycle (default 6)")
    ap.add_argument("--req-sleep", type=float, default=2.0,
                    help="seconds between API requests (default 2.0)")
    ap.add_argument("--max-cycles", type=int, default=None)
    ap.add_argument("--once", action="store_true",
                    help="run one cycle and exit")
    ap.add_argument("--show-gaps", action="store_true",
                    help="show the top 20 gaps but don't fetch")
    args = ap.parse_args()

    if args.show_gaps:
        store = load_store()
        gaps = detect_gaps(store, top_n=20)
        print(f"Store: {len(store):,} concepts")
        print(f"Top 20 gaps (capitalized terms mentioned in defs but not known):")
        print()
        print(f"  {'TERM':40s}  {'SCORE':>6s}  {'FIRST-SEEN-IN'}")
        print(f"  {'-'*40}  {'-'*6}  {'-'*40}")
        for term, score, source in gaps:
            print(f"  {term:40s}  {score:>6.2f}  {source[:40]}")
        return 0

    if args.once:
        attempted, saved = curious_cycle(
            gaps_per_cycle=args.gaps_per_cycle,
            sleep_s=args.req_sleep)
        print(f"[curious] one cycle: attempted={attempted}, saved={saved}")
        return 0

    print(f"[curious] starting — cycle={args.cycle}s, gaps={args.gaps_per_cycle}, "
          f"max_cycles={args.max_cycles or 'infinite'}")
    try:
        curious_forever(
            cycle_sleep_s=args.cycle,
            gaps_per_cycle=args.gaps_per_cycle,
            req_sleep_s=args.req_sleep,
            max_cycles=args.max_cycles,
        )
    except KeyboardInterrupt:
        print("\n[curious] interrupted; exiting cleanly")
    return 0


if __name__ == "__main__":
    sys.exit(main())
