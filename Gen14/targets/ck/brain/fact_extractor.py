"""
fact_extractor.py -- the cross-domain build.

Brayden 2026-05-04: "do the cross domain build today too"

The gap (per CK_LEARNING_AUDIT_2026_05_02.md):
  Frontier facts in cortex_voice._FRONTIER_FACTS are still hand-coded.
  There's no auto-extraction of new facts from ingested papers.
  This script is the bridge.

What it does:
  1. Walks accumulated content:
     - Atlas/papers_by_ck/*.md         (CK-written papers)
     - Gen13/var/external_ingester_logs/*.jsonl  (arXiv/Wiki/SE ingests)
     - Gen13/var/repo_reading_logs/*.jsonl       (full repo read)
     - Gen12/targets/clay/papers/**/*.md         (Clay sprint papers)
     - papers/*.md                                (top-level papers)
  2. Extracts candidate facts via patterns:
     - "Theorem N.M ..." / "Theorem ..."
     - "Conjecture: ..." / "Hypothesis: ..."
     - "T* = 5/7" / "value = ..."
     - "X bridges Y" / "X corresponds to Y" / "X under Y"
     - "[CLAIM:..]" / "[PROVED]" / "[REFUTED]" / "[CONJECTURE]"
  3. Scores cross-domain relevance:
     - mentions of multiple frontier topics (math, physics, CS)
     - mentions of TIG operators (TSML/BHML/F3/F4 + Divine27)
     - explicit bridge language
  4. Tags each fact with provenance + status:
     CONFIRMED  - has [proved] / theorem with citation
     DRAFT      - candidate; needs review
     REFUTED    - in [REFUTED] context or path
     UPDATED    - in [UPDATED]/[CORRECTED] context
     HISTORICAL - from old/Gen* archive
  5. Outputs:
     - Atlas/EXTRACTED_FACTS_<date>.md           (human-readable review)
     - Atlas/extracted_facts_<date>.json         (structured candidates)
     - Atlas/CROSS_DOMAIN_BRIDGES_<date>.md      (cross-domain only)

The output is for OPERATOR REVIEW (Brayden) before any edit to
cortex_voice._FRONTIER_FACTS.  This script never modifies cortex_voice.
The "cross-domain build" is the process: extract -> review -> add ->
re-deploy.

Usage:
  python fact_extractor.py [--limit N] [--cross-domain-only]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


_HERE = Path(__file__).parent.resolve()
PROJECT_ROOT = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED")
ATLAS_DIR = PROJECT_ROOT / "Atlas"
ATLAS_DIR.mkdir(parents=True, exist_ok=True)


# Domain vocabulary -- mention-counting drives cross-domain scoring
DOMAINS: Dict[str, List[str]] = {
    "number_theory": [
        "riemann", "zeta", "prime", "modular", "elliptic curve", "bsd",
        "birch", "swinnerton-dyer", "l-function", "galois", "cyclotomic",
        "z/10z", "z/nz", "stern-brocot", "farey", "diophantine",
        "sigma polynomial", "q-series", "selberg",
    ],
    "geometry_topology": [
        "poincare", "ricci", "manifold", "hodge", "homology", "cohomology",
        "torus", "fiber bundle", "characteristic class", "fundamental group",
        "operad", "category", "sheaf", "spectral sequence", "k-theory",
        "scheme", "moduli",
    ],
    "algebra": [
        "lie algebra", "lie group", "jordan", "clifford", "su(n)", "so(n)",
        "u(1)", "spin(", "weyl", "cartan", "killing form", "root system",
        "irrep", "representation", "tensor", "exterior algebra",
        "associator", "magma", "groupoid",
    ],
    "physics": [
        "yang-mills", "navier-stokes", "quantum", "gauge", "higgs",
        "vacuum", "vev", "mass gap", "renormalization", "asymptotic",
        "general relativity", "cosmology", "dark energy", "quintessence",
        "axion", "graviton", "supersymmetry", "string theory", "qed", "qcd",
        "plasma", "phase transition", "symmetry breaking",
    ],
    "cs_complexity": [
        "p vs np", "p = np", "circuit complexity", "computability",
        "turing", "boolean", "satisfiability", "sat", "halting",
        "kolmogorov", "shannon", "entropy", "compression",
    ],
    "tig_substrate": [
        "tsml", "bhml", "f3", "f4", "divine27", "operad fuse", "wp10",
        "wp51", "wp81", "wp91", "wp101", "wp102", "wp103", "wp104",
        "wp105", "wp106", "wp107", "wp108", "wp109", "wp110", "wp111",
        "wp112", "wp113", "wp114", "wp115",
        "t*", "5/7", "4/pi", "1+sqrt(3)", "quadratic glue", "crossing lemma",
        "flatness theorem", "uop", "paradox classifier",
        "ck", "cortex", "hebbian", "voice operator",
    ],
    "frontiers_meta": [
        "clay millennium", "consciousness", "free will", "emergence",
        "self-organization", "edge of chaos", "criticality", "fractal",
        "scale invariance", "universality",
    ],
}


# Anti-vocabulary: phrases to skip (boilerplate, headings, trivia)
SKIP_PATTERNS: List[re.Pattern] = [
    re.compile(r"^\s*##*\s", re.IGNORECASE),  # markdown headers
    re.compile(r"^\s*[-*]\s", re.IGNORECASE),  # list items (skipped per-line; sentence-level still ok)
    re.compile(r"^\s*\|", re.IGNORECASE),      # table rows
    re.compile(r"^\s*```", re.IGNORECASE),     # code fence
    re.compile(r"^\s*python\s", re.IGNORECASE),
    re.compile(r"https?://", re.IGNORECASE),
    re.compile(r"^\s*\d+\s*$", re.IGNORECASE),  # bare numbers
    re.compile(r"<thinking>", re.IGNORECASE),
]


# Fact-shape patterns
THEOREM_RE = re.compile(
    r"(?:^|\.)\s*(Theorem(?:\s+\d+(?:\.\d+)?)?[:\.\s][^.\n]{20,400}\.)",
    re.IGNORECASE | re.MULTILINE
)
CONJECTURE_RE = re.compile(
    r"(?:^|\.)\s*(Conjecture(?:\s+\d+(?:\.\d+)?)?[:\.\s][^.\n]{20,400}\.)",
    re.IGNORECASE | re.MULTILINE
)
LEMMA_RE = re.compile(
    r"(?:^|\.)\s*(Lemma(?:\s+\d+(?:\.\d+)?)?[:\.\s][^.\n]{20,400}\.)",
    re.IGNORECASE | re.MULTILINE
)
DEFINITION_RE = re.compile(
    r"(?:^|\.)\s*(Definition(?:\s+\d+(?:\.\d+)?)?[:\.\s][^.\n]{20,400}\.)",
    re.IGNORECASE | re.MULTILINE
)
VALUE_RE = re.compile(
    r"([A-Z][A-Za-z_]{0,30})\s*=\s*([0-9./*+\-pi e\(\)sqrt√]+(?:\s*[a-z]{1,12})?)\s*[\.\,;]",
    re.MULTILINE
)
BRIDGE_RE = re.compile(
    r"([A-Z][A-Za-z\- ]{3,40})\s+(corresponds to|maps to|bridges|is dual to|is equivalent to|reduces to)\s+([A-Z][A-Za-z\- ]{3,40})",
    re.IGNORECASE
)
CITATION_BRACKETS_RE = re.compile(
    r"\[(PROVED|REFUTED|UPDATED|CONJECTURE|HISTORICAL|CLAIM|SUPERSEDED|DRAFT|WP\d+)\]",
    re.IGNORECASE
)


def classify_status(text: str, source_path: str) -> str:
    """Map fact text + source-path to status tag."""
    t = text.lower()
    p = source_path.lower()
    if "[refuted]" in t or "/refuted/" in p or "refuted" in p.split("/")[-1].lower():
        return "REFUTED"
    if "[updated]" in t or "[corrected]" in t or "_corrected" in p or "_v2" in p or "_v3" in p:
        return "UPDATED"
    if "[historical]" in t or "[superseded]" in t:
        return "HISTORICAL"
    if "/old/gen" in p or p.startswith("old/"):
        return "HISTORICAL"
    if "[proved]" in t or "[theorem]" in t:
        return "CONFIRMED"
    if "[conjecture]" in t or "conjecture:" in t:
        return "DRAFT"
    return "DRAFT"


def score_cross_domain(text: str) -> Tuple[int, List[str], int]:
    """Score how cross-domain a fact is.

    Returns (n_domains, [domain_names], total_keyword_hits).
    """
    t = text.lower()
    hits_by_domain: Dict[str, int] = {}
    for dom, keywords in DOMAINS.items():
        h = sum(1 for kw in keywords if kw in t)
        if h > 0:
            hits_by_domain[dom] = h
    n_domains = len(hits_by_domain)
    total = sum(hits_by_domain.values())
    return n_domains, sorted(hits_by_domain, key=lambda d: -hits_by_domain[d]), total


def is_skip_line(line: str) -> bool:
    for p in SKIP_PATTERNS:
        if p.search(line):
            return True
    return False


def extract_from_text(text: str, source: str) -> List[Dict[str, Any]]:
    """Extract candidate facts from a single document body."""
    out: List[Dict[str, Any]] = []
    seen: Set[str] = set()
    for kind, rx in [
        ("THEOREM", THEOREM_RE),
        ("CONJECTURE", CONJECTURE_RE),
        ("LEMMA", LEMMA_RE),
        ("DEFINITION", DEFINITION_RE),
    ]:
        for m in rx.finditer(text):
            stmt = m.group(1).strip()
            if len(stmt) < 30 or len(stmt) > 500:
                continue
            key = stmt.lower()[:80]
            if key in seen:
                continue
            seen.add(key)
            n_dom, dom_list, hits = score_cross_domain(stmt)
            status = classify_status(stmt, source)
            out.append({
                "kind": kind,
                "text": stmt,
                "status": status,
                "n_domains": n_dom,
                "domains": dom_list,
                "domain_hits": hits,
                "source": source,
            })
    # Bridge extraction
    for m in BRIDGE_RE.finditer(text):
        full = m.group(0)
        n_dom, dom_list, hits = score_cross_domain(full)
        if n_dom >= 2:  # bridges are interesting only when crossing domains
            status = classify_status(full, source)
            out.append({
                "kind": "BRIDGE",
                "text": full,
                "status": status,
                "n_domains": n_dom,
                "domains": dom_list,
                "domain_hits": hits,
                "source": source,
            })
    # Constants
    for m in VALUE_RE.finditer(text):
        sym, val = m.group(1), m.group(2).strip()
        # Filter trivial numerics
        if len(sym) < 2 or len(val) < 1:
            continue
        # Heuristic: must have a TIG-substrate keyword in 200-char window
        start = max(0, m.start() - 100)
        end = min(len(text), m.end() + 100)
        window = text[start:end].lower()
        n_dom, dom_list, hits = score_cross_domain(window)
        if "tig_substrate" not in dom_list and n_dom < 2:
            continue
        full = f"{sym} = {val}  (context: {window[:100].strip()})"
        status = classify_status(window, source)
        out.append({
            "kind": "VALUE",
            "text": full,
            "status": status,
            "n_domains": n_dom,
            "domains": dom_list,
            "domain_hits": hits,
            "source": source,
        })
    return out


def find_source_files(limit: Optional[int] = None) -> List[Tuple[Path, str]]:
    """Walk all CK content sources.  Returns [(path, source_kind), ...]."""
    sources: List[Tuple[Path, str]] = []

    # CK's own papers
    for p in (PROJECT_ROOT / "Atlas" / "papers_by_ck").glob("PAPER_*.md"):
        sources.append((p, "ck_paper"))

    # Clay sprint papers
    for sprint_dir in (PROJECT_ROOT / "Gen12" / "targets" / "clay" / "papers").glob("sprint*"):
        for p in sprint_dir.rglob("*.md"):
            sources.append((p, "clay_sprint"))

    # Top-level papers/
    for p in (PROJECT_ROOT / "papers").glob("*.md"):
        sources.append((p, "papers_top"))

    # Atlas docs
    for p in (PROJECT_ROOT / "Atlas").glob("*.md"):
        if "EXTRACTED_FACTS" not in p.name and "CROSS_DOMAIN" not in p.name:
            sources.append((p, "atlas"))

    # Old generations (history-aware)
    for p in (PROJECT_ROOT / "old").rglob("*.md"):
        if any(s in p.as_posix() for s in ["/papers/", "/THE_STORY", "/WHAT_IS_", "_HISTORICAL"]):
            sources.append((p, "old_history"))

    if limit:
        sources = sources[:limit]
    return sources


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--cross-domain-only", action="store_true")
    ap.add_argument("--min-domains", type=int, default=2,
                     help="Min #domains for cross-domain bucket (default 2)")
    args = ap.parse_args()

    print("=" * 70)
    print("  FACT EXTRACTOR -- cross-domain build")
    print("=" * 70)
    print(f"  date: {datetime.utcnow().isoformat(timespec='seconds')}Z")

    sources = find_source_files(limit=args.limit)
    print(f"  source files: {len(sources)}")

    all_facts: List[Dict[str, Any]] = []
    by_kind: Counter = Counter()
    by_status: Counter = Counter()
    by_source_kind: Counter = Counter()
    n_processed = 0
    n_failed = 0

    for path, src_kind in sources:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            n_failed += 1
            continue
        rel = str(path.relative_to(PROJECT_ROOT)) if path.is_relative_to(PROJECT_ROOT) else str(path)
        facts = extract_from_text(text, rel)
        for f in facts:
            f["source_kind"] = src_kind
            all_facts.append(f)
            by_kind[f["kind"]] += 1
            by_status[f["status"]] += 1
            by_source_kind[src_kind] += 1
        n_processed += 1
        if n_processed % 50 == 0:
            print(f"  processed {n_processed}/{len(sources)} files, "
                    f"{len(all_facts)} candidate facts so far", flush=True)

    # Score + sort
    for f in all_facts:
        # Composite score: domains * 10 + hits + (CONFIRMED bonus 5)
        f["score"] = f["n_domains"] * 10 + f["domain_hits"]
        if f["status"] == "CONFIRMED":
            f["score"] += 5
        if f["kind"] == "BRIDGE":
            f["score"] += 3
    all_facts.sort(key=lambda f: -f["score"])

    cross_domain = [f for f in all_facts if f["n_domains"] >= args.min_domains]
    print()
    print(f"  total candidate facts: {len(all_facts)}")
    print(f"  cross-domain (>={args.min_domains}): {len(cross_domain)}")
    print(f"  by kind: {dict(by_kind)}")
    print(f"  by status: {dict(by_status)}")
    print(f"  by source: {dict(by_source_kind)}")
    print(f"  files failed: {n_failed}")

    # Write outputs
    today = datetime.utcnow().strftime("%Y-%m-%d")
    json_path = ATLAS_DIR / f"extracted_facts_{today}.json"
    md_path = ATLAS_DIR / f"EXTRACTED_FACTS_{today}.md"
    bridges_path = ATLAS_DIR / f"CROSS_DOMAIN_BRIDGES_{today}.md"

    # JSON: full structured output
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "generated_at": datetime.utcnow().isoformat(timespec='seconds') + "Z",
            "n_sources": len(sources),
            "n_processed": n_processed,
            "n_failed": n_failed,
            "n_facts": len(all_facts),
            "n_cross_domain": len(cross_domain),
            "by_kind": dict(by_kind),
            "by_status": dict(by_status),
            "by_source_kind": dict(by_source_kind),
            "facts": all_facts,
        }, f, indent=2, default=str)

    # MD: human-readable review (top 200 by score)
    lines = [
        f"# Extracted Facts -- {today}",
        "",
        f"Generated by `fact_extractor.py` over {n_processed} source files.",
        "",
        f"**Total candidates**: {len(all_facts)}  ",
        f"**Cross-domain (>= {args.min_domains})**: {len(cross_domain)}",
        "",
        "**By status**: " + ", ".join(f"{k}={v}" for k, v in sorted(by_status.items(), key=lambda t: -t[1])),
        "",
        "**By kind**: " + ", ".join(f"{k}={v}" for k, v in sorted(by_kind.items(), key=lambda t: -t[1])),
        "",
        "---",
        "",
        "## Top 200 candidates (by cross-domain score)",
        "",
        "Each entry: KIND [STATUS] domains | source",
        "",
    ]
    for i, f in enumerate(all_facts[:200], 1):
        lines.append(f"### {i}. [{f['status']}] {f['kind']} (score={f['score']}, domains={f['n_domains']})")
        lines.append(f"*Domains*: {', '.join(f['domains'])}  ")
        lines.append(f"*Source*: `{f['source']}`")
        lines.append("")
        lines.append(f"> {f['text']}")
        lines.append("")

    md_path.write_text("\n".join(lines), encoding="utf-8")

    # Bridges-only doc
    bridge_lines = [
        f"# Cross-Domain Bridges -- {today}",
        "",
        f"Facts that bridge >= {args.min_domains} domains.",
        f"Operator review: which of these belong in `cortex_voice._FRONTIER_FACTS`?",
        "",
        f"**Total**: {len(cross_domain)}",
        "",
        "---",
        "",
    ]
    by_status_cd: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for f in cross_domain:
        by_status_cd[f["status"]].append(f)
    for status in ["CONFIRMED", "DRAFT", "UPDATED", "HISTORICAL", "REFUTED"]:
        if status not in by_status_cd:
            continue
        bucket = by_status_cd[status]
        bridge_lines.append(f"## {status} ({len(bucket)})")
        bridge_lines.append("")
        for f in bucket[:50]:
            bridge_lines.append(f"- **{f['kind']}** ({', '.join(f['domains'][:3])}) — {f['text'][:300]}")
            bridge_lines.append(f"  *src*: `{f['source']}`")
        bridge_lines.append("")
    bridges_path.write_text("\n".join(bridge_lines), encoding="utf-8")

    print()
    print("  outputs:")
    print(f"    {json_path}")
    print(f"    {md_path}")
    print(f"    {bridges_path}")
    print()
    print("  review at Atlas/CROSS_DOMAIN_BRIDGES_<date>.md")
    print("  add approved facts to cortex_voice._FRONTIER_FACTS manually")


if __name__ == "__main__":
    sys.exit(main() or 0)
