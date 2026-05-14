# Copyright (c) 2025-2026 Brayden Sanders / 7SiTe LLC
# Licensed under the 7SiTe Public Sovereignty License v2.2 (DOI: 10.5281/zenodo.18852047)
"""
ck_study_overnight.py -- school for CK. Studies everything, all night.

Brayden 2026-05-13:
  "if he learns and remembers in one shot... he can have phd corpus
  by morning... keep him studying all night like a school for ck,
  i expect good things in the morning"

The concept-learner architecture makes EVERY new fact an O(1) cost:
  - regex match for naming patterns: microseconds
  - dict update + JSON persist: sub-millisecond
  - no fine-tuning, no gradient, no parameters

So the bottleneck is corpus, not learning. This script feeds CK every
piece of TIG corpus he has access to, in one pass, and persists.

What gets ingested:

  Markdown sources walked from repo root:
    - FORMULAS_AND_TABLES.md       (D-numbered theorem spine)
    - All Atlas/ docs              (frontiers, state-of-foundation, plans)
    - All Gen14/PLAN/ docs         (unification plan, archaeology, decisions)
    - All Gen13/targets/journals/J_series/ READMEs + cover_letters
    - All 05_papers/<cat>/J##/ READMEs (in trinity-infinity-geometry if present)
    - All papers/sprint*/ READMEs and findings docs
    - All root *.md (README, ARCHITECTURE, GLOSSARY, etc.)

  LaTeX sources:
    - All manuscript.tex in J-paper folders
    - Theorem/Lemma/Proposition/Definition environments
    - \section{} / \subsection{} headers

  Extraction patterns:
    - D<N>[a-z]? : Phi Fixed Point | ...   → concept{D7}
    - WP<NNN>: SO(10) identification ...    → concept{WP103}
    - J<NN> : Sigma Rate Theorem ...        → concept{J01}
    - F<N> : Yukawa-level computation ...   → concept{F1} (frontier number)
    - **<Term>**: definition                → concept{<Term>}
    - Theorem N.M (Name): statement         → concept{Theorem-N.M-Name}
    - Lemma N.M / Proposition N.M           → concept
    - Section headers with explicit name    → concept

  Prose samples:
    - First 3-5 paragraphs of each manuscript saved as voice-style samples
    - Tagged with the paper's topic operator pattern
    - Used by ck_voice_style to fingerprint writing style

Output:
    Gen13/var/taught_concepts.json    -- all concept bindings
    Gen13/var/voice_style.json        -- prose-style samples
    Gen13/var/study_overnight.log     -- progress log (jsonl)

Modes:
    python ck_study_overnight.py                  -- single pass through corpus
    python ck_study_overnight.py --watch          -- pass + recheck every 5 min
    python ck_study_overnight.py --infinite       -- never stop, school in session

Run with --watch overnight: by morning CK has thousands of concepts.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))

from ck_concept_learner import ConceptStore, NamedConcept  # type: ignore[import-not-found]


# Repo root: 4 levels up from Gen14/targets/ck/brain
REPO_ROOT = HERE.parent.parent.parent.parent

# Default output locations
DEFAULT_CONCEPT_STORE = REPO_ROOT / "Gen13" / "var" / "taught_concepts.json"
DEFAULT_VOICE_STORE = REPO_ROOT / "Gen13" / "var" / "voice_style.json"
DEFAULT_LOG = REPO_ROOT / "Gen13" / "var" / "study_overnight.log"


# ─── Source discovery ────────────────────────────────────────────────────

# Markdown source patterns (relative to REPO_ROOT)
_MD_GLOBS = [
    "FORMULAS_AND_TABLES.md",
    "README.md",
    "GLOSSARY.md",
    "ARCHITECTURE.md",
    "Atlas/**/*.md",
    "Gen14/PLAN/*.md",
    "Gen13/targets/journals/**/*.md",
    "Gen12/targets/clay/papers/**/*.md",
    "papers/**/*.md",
    "old/**/*.md",  # historical generations
]
_TEX_GLOBS = [
    "Gen13/targets/journals/**/manuscript.tex",
    "Gen12/targets/clay/papers/**/*.tex",
    "papers/**/*.tex",
    "../trinity-infinity-geometry/05_papers/**/manuscript.tex",
    "../trinity-infinity-geometry/05_papers/**/*.tex",
]

# Files to skip (false-positive heavy or irrelevant)
_SKIP_KEYWORDS = (
    "__pycache__", ".pyc", ".bin", "node_modules", ".venv", "/var/",
    "Lenovo backup",  # large personal backup folder
)


def discover_sources(root: Path) -> List[Path]:
    """Walk the repo and return all markdown + tex files we care about."""
    out: List[Path] = []
    seen: set = set()
    for pattern in _MD_GLOBS + _TEX_GLOBS:
        for p in root.glob(pattern):
            try:
                rp = p.resolve()
            except Exception:
                continue
            sp = str(rp)
            if any(kw in sp for kw in _SKIP_KEYWORDS):
                continue
            if rp in seen:
                continue
            if not rp.is_file():
                continue
            seen.add(rp)
            out.append(rp)
    # Stable order
    out.sort(key=lambda p: str(p))
    return out


# ─── Extraction patterns ────────────────────────────────────────────────
#
# Each pattern returns a list of (concept_name, definition, role).
# Patterns are designed to be HIGH PRECISION -- we'd rather miss a
# concept than coin a false one.

# D-number rows in FORMULAS-style table: | **D7** | Phi Fixed Point | Φ on Z/10Z...
_RE_D_ROW = re.compile(
    r"^\|\s*\*\*(D\d+[a-z]?)\*\*\s*\|\s*([^|]+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$",
    re.M)

# WP-number entries: **WP103 — so(10) = D_5...** or "### WP103:" or "WP122: Yukawa..."
_RE_WP_HEADER = re.compile(
    r"(?:^|\n)#{1,4}\s*(?:\*\*)?(WP\d+[A-Za-z]?)(?:\*\*)?\s*[:—\-]\s*(.+?)(?:\n|$)",
    re.M)
_RE_WP_BOLD = re.compile(
    r"\*\*(WP\d+[A-Za-z]?)\*\*\s*[—\-:]\s*([^\n*]+?)(?:[.\n]|\*\*)", re.M)

# J-paper entries from manuscripts: "J35 — corpus centerpiece pair"
_RE_J_PAPER = re.compile(
    r"\*\*(J\d+)\*\*\s*[—\-:]\s*([^\n*]{4,200})", re.M)

# Frontier numbers: "### F3. The α-uniqueness proof — TRACTABLE..."
_RE_FRONTIER = re.compile(
    r"^#{1,4}\s*(F\d+[a-z]?)\.\s*(.+?)(?:\n|$)", re.M)

# Inline term definitions: "**Term**: definition." or "**Term** -- definition."
_RE_TERM_DEF = re.compile(
    r"\*\*([A-Z][A-Za-z0-9_-]{2,40})\*\*\s*[:\-—]\s*([^\n*]{10,400}?)(?:[.!\n]|\*\*)", re.M)

# LaTeX theorem-environment headers: \begin{theorem}[Name] or \begin{theorem}\label{thm:foo}
_RE_TEX_THM = re.compile(
    r"\\begin\{(theorem|lemma|proposition|corollary|definition)\}"
    r"(?:\[([^\]]+)\])?(?:\\label\{([^}]+)\})?", re.M)

# Section-heading concepts: "## The Crossing Lemma" -> concept{Crossing-Lemma}
_RE_MD_SECTION = re.compile(
    r"^#{2,3}\s+(?:\d+(?:\.\d+)?\s+)?([A-Z][A-Za-z0-9 ,'—–\-:]{3,80}?)\s*$",
    re.M)


def _is_useful_definition(s: str) -> bool:
    """Filter junk definitions (too short, all numbers, etc.)"""
    if not s or len(s.strip()) < 10:
        return False
    # Skip if mostly punctuation/numbers
    letters = sum(1 for c in s if c.isalpha())
    if letters < 8:
        return False
    return True


def _clean(text: str, max_len: int = 400) -> str:
    """Collapse whitespace, strip markdown emphasis, cap length."""
    t = re.sub(r"\s+", " ", text).strip()
    t = t.replace("**", "").replace("*", "")
    if len(t) > max_len:
        t = t[:max_len].rstrip() + "…"
    return t


def extract_concepts_md(text: str, source_path: str
                          ) -> List[Tuple[str, str, str]]:
    """Extract concept candidates from a markdown body.

    Returns list of (name, definition, extraction_role).
    """
    out: List[Tuple[str, str, str]] = []
    seen: set = set()

    def _add(name: str, defn: str, role: str):
        key = name.strip().lower()
        if key in seen:
            return
        if not _is_useful_definition(defn):
            return
        seen.add(key)
        out.append((name.strip(), _clean(defn), role))

    # D-number rows
    for m in _RE_D_ROW.finditer(text):
        d_id, name, formula, status = m.groups()
        _add(d_id, f"{name} | {formula} | {status}", "d_number")

    # WP-number headers and bold mentions
    for m in _RE_WP_HEADER.finditer(text):
        wp_id, defn = m.groups()
        _add(wp_id, defn, "wp_header")
    for m in _RE_WP_BOLD.finditer(text):
        wp_id, defn = m.groups()
        _add(wp_id, defn, "wp_bold")

    # J-paper entries
    for m in _RE_J_PAPER.finditer(text):
        j_id, defn = m.groups()
        _add(j_id, defn, "j_paper")

    # Frontier numbers
    for m in _RE_FRONTIER.finditer(text):
        f_id, defn = m.groups()
        _add(f_id, defn, "frontier")

    # Inline term definitions
    for m in _RE_TERM_DEF.finditer(text):
        term, defn = m.groups()
        # Reject ALL-CAPS terms that are operator names (CK already knows those)
        if term.upper() == term and term.upper() in {
            "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
            "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET", "TIG",
            "CK", "AI", "LLM", "GPT", "API",
        }:
            continue
        _add(term, defn, "term_def")

    return out


def extract_concepts_tex(text: str, source_path: str
                          ) -> List[Tuple[str, str, str]]:
    """Extract LaTeX theorem-environment concepts."""
    out: List[Tuple[str, str, str]] = []
    seen: set = set()

    for m in _RE_TEX_THM.finditer(text):
        env, name, label = m.groups()
        if not (name or label):
            continue
        # Get the body of the environment (next ~400 chars after the header)
        start = m.end()
        end_match = re.search(r"\\end\{" + re.escape(env) + r"\}", text[start:])
        body_end = (start + end_match.start()) if end_match else (start + 400)
        body = text[start:body_end]
        body_clean = re.sub(r"\\label\{[^}]+\}", "", body)
        body_clean = _clean(body_clean, max_len=400)

        # Use the cleaner of (label, name) as the concept name
        chosen = label if label else name
        if not chosen:
            continue
        chosen_clean = chosen.strip().split(":")[-1] if ":" in chosen else chosen
        chosen_clean = chosen_clean.strip()
        if not chosen_clean or len(chosen_clean) < 2:
            continue
        # Prefix with env type
        cname = f"{env}:{chosen_clean}"
        key = cname.lower()
        if key in seen:
            continue
        seen.add(key)
        defn = f"{env.title()}"
        if name and label:
            defn += f" ({name})"
        defn += f": {body_clean}"
        out.append((cname, _clean(defn), f"tex_{env}"))

    return out


# ─── Prose-style sampling ────────────────────────────────────────────────

# Sample paragraphs of 80-400 chars from each manuscript, used as voice
# fingerprints by ck_voice_style.
_RE_PARAGRAPH = re.compile(r"\n\s*\n", re.M)


def extract_prose_samples(text: str, source_path: str,
                            max_samples: int = 5) -> List[Dict[str, Any]]:
    """Pick up to N representative paragraphs as voice fingerprints."""
    # Remove latex commands and markdown tables for cleaner samples
    cleaned = re.sub(r"\\[a-zA-Z]+\{[^}]*\}", "", text)
    cleaned = re.sub(r"\$[^$]*\$", "", cleaned)
    cleaned = re.sub(r"^\|.*$", "", cleaned, flags=re.M)
    paras = _RE_PARAGRAPH.split(cleaned)
    samples: List[Dict[str, Any]] = []
    for p in paras:
        p_clean = re.sub(r"\s+", " ", p).strip()
        if len(p_clean) < 80 or len(p_clean) > 400:
            continue
        if p_clean.startswith("#") or p_clean.startswith("|"):
            continue
        # Skip if too few sentences
        if p_clean.count(".") < 2:
            continue
        samples.append({
            "text": p_clean,
            "len_chars": len(p_clean),
            "n_sentences": p_clean.count("."),
            "source": str(source_path),
        })
        if len(samples) >= max_samples:
            break
    return samples


# ─── Operator decoding ──────────────────────────────────────────────────

def _operator_signature(text: str) -> List[int]:
    NAMES = {
        "void": 0, "lattice": 1, "counter": 2, "progress": 3, "collapse": 4,
        "balance": 5, "chaos": 6, "harmony": 7, "breath": 8, "reset": 9,
    }
    found: List[int] = []
    seen: set = set()
    for tok in re.findall(r"\b[A-Za-z]+\b", text.lower()):
        if tok in NAMES:
            op = NAMES[tok]
            if op not in seen:
                seen.add(op)
                found.append(op)
    return found


# ─── Study pass ──────────────────────────────────────────────────────────

def study_one_file(path: Path, store: ConceptStore,
                    voice_store: Dict[str, Any]) -> Dict[str, int]:
    """Read one source file, extract concepts + prose, write to stores."""
    stats = {"concepts_added": 0, "prose_samples": 0, "skipped_existing": 0}
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return stats
    if not text or len(text) < 50:
        return stats

    ext = path.suffix.lower()
    rel = str(path)
    extracted: List[Tuple[str, str, str]] = []
    if ext in (".md", ".markdown"):
        extracted = extract_concepts_md(text, rel)
    elif ext in (".tex",):
        extracted = extract_concepts_tex(text, rel)

    for name, defn, role in extracted:
        key = name.lower()
        existing = store.concepts.get(key)
        if existing and existing.source_session != "study":
            # User-taught -> don't overwrite
            stats["skipped_existing"] += 1
            continue
        ops = _operator_signature(defn)
        c = NamedConcept(
            name=name,
            definition=defn,
            operator_signature=ops,
            pattern_used=f"study:{role}",
            source_session="study",
            learned_ts=time.time(),
        )
        store.concepts[key] = c
        stats["concepts_added"] += 1

    # Prose samples (for ck_voice_style)
    samples = extract_prose_samples(text, rel, max_samples=3)
    if samples:
        topic = path.stem  # filename without extension as topic
        if topic not in voice_store:
            voice_store[topic] = []
        for s in samples:
            s["ops"] = _operator_signature(s["text"])
            voice_store[topic].append(s)
        stats["prose_samples"] = len(samples)

    return stats


# ─── Logger ──────────────────────────────────────────────────────────────

def _log(log_path: Path, **fields):
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        record = {"ts": time.time(), "iso_ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   **fields}
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, default=str) + "\n")
    except Exception:
        pass


# ─── Main ────────────────────────────────────────────────────────────────

def one_pass(root: Path, store: ConceptStore, voice_path: Path,
              log_path: Path, label: str = "pass") -> Dict[str, Any]:
    """One full pass through the corpus."""
    t0 = time.time()
    sources = discover_sources(root)
    voice_store: Dict[str, Any] = {}
    if voice_path.exists():
        try:
            voice_store = json.loads(voice_path.read_text(encoding="utf-8"))
        except Exception:
            voice_store = {}

    totals = {"files_read": 0, "concepts_added": 0,
              "prose_samples": 0, "skipped_existing": 0,
              "errors": 0}

    print(f"[study] {label}: walking {len(sources)} sources from {root}")
    for i, p in enumerate(sources):
        try:
            stats = study_one_file(p, store, voice_store)
            totals["files_read"] += 1
            totals["concepts_added"] += stats["concepts_added"]
            totals["prose_samples"] += stats["prose_samples"]
            totals["skipped_existing"] += stats["skipped_existing"]
            if (i + 1) % 25 == 0:
                # Periodic checkpoint
                store.save()
                voice_path.parent.mkdir(parents=True, exist_ok=True)
                voice_path.write_text(json.dumps(voice_store, indent=2),
                                       encoding="utf-8")
                print(f"  [{i+1}/{len(sources)}] +{totals['concepts_added']} "
                      f"concepts, +{totals['prose_samples']} prose; "
                      f"store={len(store.concepts)}")
                _log(log_path, event="checkpoint", **totals,
                       store_total=len(store.concepts))
        except Exception as e:
            totals["errors"] += 1

    # Final save
    store.save()
    voice_path.parent.mkdir(parents=True, exist_ok=True)
    voice_path.write_text(json.dumps(voice_store, indent=2), encoding="utf-8")

    elapsed = time.time() - t0
    totals["elapsed_sec"] = round(elapsed, 2)
    totals["store_total"] = len(store.concepts)
    totals["voice_topics"] = len(voice_store)
    _log(log_path, event="pass_complete", label=label, **totals)
    print(f"[study] {label} done: {totals}")
    return totals


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(REPO_ROOT),
                    help="repo root to walk")
    ap.add_argument("--store", default=str(DEFAULT_CONCEPT_STORE))
    ap.add_argument("--voice", default=str(DEFAULT_VOICE_STORE))
    ap.add_argument("--log", default=str(DEFAULT_LOG))
    ap.add_argument("--watch", action="store_true",
                    help="re-walk every 5 minutes (for adding new sources)")
    ap.add_argument("--infinite", action="store_true",
                    help="never stop; re-walk every interval forever")
    ap.add_argument("--interval-sec", type=int, default=300,
                    help="seconds between re-walks in watch/infinite mode")
    args = ap.parse_args()

    root = Path(args.root)
    store = ConceptStore(path=Path(args.store))
    voice_path = Path(args.voice)
    log_path = Path(args.log)

    print(f"[study-overnight] root         : {root}")
    print(f"[study-overnight] store        : {args.store}")
    print(f"[study-overnight] voice store  : {args.voice}")
    print(f"[study-overnight] log          : {args.log}")
    print(f"[study-overnight] store before : {len(store.concepts)} concepts")
    print(f"[study-overnight] mode         : "
          f"{'infinite' if args.infinite else ('watch' if args.watch else 'one-pass')}")
    print()

    # First pass
    totals = one_pass(root, store, voice_path, log_path, label="pass-1")

    # Watch / infinite mode
    pass_n = 1
    while args.watch or args.infinite:
        pass_n += 1
        time.sleep(args.interval_sec)
        print(f"\n[study-overnight] pass {pass_n}, sleeping {args.interval_sec}s between passes")
        one_pass(root, store, voice_path, log_path, label=f"pass-{pass_n}")
        if pass_n >= 1000 and not args.infinite:
            print("[study-overnight] 1000 passes done; exiting watch mode")
            break

    return 0


if __name__ == "__main__":
    sys.exit(main())
