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

from ck_concept_learner import (  # type: ignore[import-not-found]
    ConceptStore, NamedConcept, _extract_from_research, semantic_decode,
    auto_learn_from_text,
)


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
    "Gen13/**/*.md",                       # broaden: all Gen13 markdown
    "Gen12/targets/**/*.md",               # broaden
    "papers/**/*.md",
    "old/**/*.md",                          # historical generations
    "*.md",                                  # any root-level
    # public repo (if mounted as sibling)
    "../trinity-infinity-geometry/**/*.md",
    # other text formats CK can read
    "**/*.txt",
    "**/*.rst",
    # External corpora (world ingest, tier=EXTERNAL by default)
    "external_corpora/**/*.txt",
    "external_corpora/**/*.md",
]
_TEX_GLOBS = [
    "Gen13/**/*.tex",
    "Gen12/targets/clay/papers/**/*.tex",
    "papers/**/*.tex",
    "../trinity-infinity-geometry/**/*.tex",
]
# Python sources for docstring extraction (CK's own architecture is a corpus)
_PY_GLOBS = [
    "Gen14/targets/ck/brain/*.py",          # the Gen14 brain modules themselves
    "Gen13/targets/ck/brain/*.py",
    "Gen12/targets/ck_desktop/ck_sim/**/*.py",
]

# Files to skip (false-positive heavy or irrelevant)
_SKIP_KEYWORDS = (
    "__pycache__", ".pyc", ".bin", "node_modules", ".venv", "/var/",
    "Lenovo backup",  # large personal backup folder
)


def discover_sources(root: Path, include_python: bool = True) -> List[Path]:
    """Walk the repo and return all markdown + tex + (optionally) py files."""
    out: List[Path] = []
    seen: set = set()
    globs = _MD_GLOBS + _TEX_GLOBS
    if include_python:
        globs = globs + _PY_GLOBS
    for pattern in globs:
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
            # Reject very large files (>2MB) -- usually data dumps not prose
            try:
                if rp.stat().st_size > 2_000_000:
                    continue
            except Exception:
                pass
            seen.add(rp)
            out.append(rp)
    out.sort(key=lambda p: str(p))
    return out


# ─── Fact-tier detection (fact vs fiction) ──────────────────────────────
#
# Each file's path implies a default epistemic tier. Speculative folders
# (04_meta, 09_seekers, philosophy, mythology) default to SPECULATIVE.
# Verified-papers folders (05_papers/, J_series/) default to STRUCTURAL
# or PROVED depending on individual entries. Old/historical content
# defaults to EXTERNAL (someone-else's-claim).

_SPECULATIVE_PATH_KEYWORDS = (
    "04_meta", "09_seekers", "philosophy", "mythology",
    "SPECULAT", "speculation", "TIER_C", "tier_c", "Tier C",
    "/old/", "Old Knowledge", "_HISTORICAL",
)
_PROVED_PATH_KEYWORDS = (
    "05_papers/", "J_series/", "verification/", "proof_", "verify_",
    "FORMULAS_AND_TABLES",
)
# Status keywords found INLINE in a formula's status_file column
_STATUS_KEYWORD_TO_TIER = {
    "PROVED": "PROVED",
    "PROOF": "PROVED",
    "VERIFIED": "PROVED",
    "STRUCTURAL": "STRUCTURAL",
    "EMPIRICAL": "EMPIRICAL",
    "EMPIRICALLY": "EMPIRICAL",
    "OPEN": "OPEN",
    "CONJECTURAL": "OPEN",
    "TBD": "OPEN",
    "SPECULAT": "SPECULATIVE",
    "TIER C": "SPECULATIVE",
    "TIER-C": "SPECULATIVE",
    "HYPOTHESI": "OPEN",
}


def detect_tier_from_path(source_path: str) -> str:
    """Default tier based on the file's location in the repo."""
    sp = str(source_path).replace("\\", "/")
    # External-world corpus (Gutenberg, arXiv, Wikipedia, etc.)
    if "external_corpora/" in sp or "external_corpora\\" in str(source_path):
        return "EXTERNAL"
    for kw in _SPECULATIVE_PATH_KEYWORDS:
        if kw in sp:
            return "SPECULATIVE"
    for kw in _PROVED_PATH_KEYWORDS:
        if kw in sp:
            return "STRUCTURAL"  # default to STRUCTURAL; per-row PROVED check can override
    return "UNKNOWN"


def detect_tier_from_status_text(status_text: str) -> Optional[str]:
    """Promote/demote tier based on inline status keywords ('PROVED', 'OPEN', etc.).

    Uses word-boundary matching so 'PROVED' in 'imPROVED' doesn't trigger.
    """
    if not status_text:
        return None
    upper = status_text.upper()
    # Order matters: more specific first
    for kw, tier in _STATUS_KEYWORD_TO_TIER.items():
        # Word-boundary match: kw must be flanked by non-letter chars
        pattern = r"(?<![A-Z])" + re.escape(kw) + r"(?![A-Z])"
        if re.search(pattern, upper):
            return tier
    return None


def merge_tier(path_tier: str, status_tier: Optional[str]) -> str:
    """Combine a path-derived tier with a status-extracted tier.

    Rule:
      - If path_tier is EXTERNAL (concept from external_corpora), the
        path tier is AUTHORITATIVE.  Inline mentions of "PROVED" or
        "STRUCTURAL" in a Gutenberg-book prose passage do not promote
        the resulting concept above EXTERNAL.  This prevents Darwin's
        "improved" or a README mentioning "tier=PROVED" from
        contaminating CK's PROVED set.
      - For all other paths, status_tier (if detected) wins over
        path_tier.  Inside CK's own sprint papers, an inline "PROVED"
        IS authoritative.
    """
    if path_tier == "EXTERNAL":
        return "EXTERNAL"
    if status_tier:
        return status_tier
    return path_tier or "UNKNOWN"


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


# Stopwords + content-free words to NEVER coin as concepts.
# These show up in **Word**: prose patterns and would create false
# concepts like "What", "Note", "Plan" if not filtered.
_STUDY_STOPWORDS = frozenset({
    "what", "who", "when", "where", "why", "how", "which", "that", "this",
    "these", "those", "the", "an", "and", "or", "but", "for", "in", "of", "to",
    "with", "on", "at", "by", "as", "is", "are", "was", "were", "be", "been",
    "have", "has", "had", "do", "does", "did", "will", "would", "should",
    "shall", "may", "might", "must", "can", "could", "yes", "no", "not",
    "so", "if", "then", "else", "i", "we", "you", "they", "he", "she", "it",
    "me", "us", "them", "him", "her",
    # Common content-free section/list words
    "note", "see", "also", "now", "today", "here", "there", "still", "just",
    "recipe", "kind", "thing", "way", "idea", "fact", "goal", "plan",
    "output", "input", "result", "finding", "name", "value", "state", "mode",
    "file", "line", "edit", "add", "use", "yes", "no",
    "tldr", "tldr;", "summary", "abstract", "introduction", "conclusion",
    "context", "scope", "status", "purpose", "rationale", "note",
})

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
        # Reject stopwords / content-free words ("What", "Note", "Plan", ...)
        if term.lower() in _STUDY_STOPWORDS:
            continue
        # Reject ALL-CAPS terms that are operator names (CK already knows those)
        if term.upper() == term and term.upper() in {
            "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
            "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET", "TIG",
            "CK", "AI", "LLM", "GPT", "API",
        }:
            continue
        # Reject very short captures (less than 2 letters of content)
        letters = sum(1 for c in term if c.isalpha())
        if letters < 2:
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
    """Decode text -> operator stream.

    Tries the semantic decoder first (word-class -> op mapping over a
    ~200-word vocabulary across all 10 operators); falls back to literal
    op-name scan if nothing matches.  This populates the cell-index
    coordinate for every concept extracted from prose.
    """
    # Primary path: semantic decoder (handles natural-language prose)
    ops = semantic_decode(text, max_ops=6)
    if ops:
        return ops
    # Fallback: literal CK op-name scan
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

def extract_concepts_py(text: str, source_path: str
                          ) -> List[Tuple[str, str, str]]:
    """Extract module-level docstring concept (one per file).

    A Python module's docstring is its self-description -- that's
    a concept named after the module file.
    """
    m = re.match(r'^\s*"""(.+?)"""', text, re.S)
    if not m:
        return []
    docstring = m.group(1).strip()
    if not _is_useful_definition(docstring) or len(docstring) < 60:
        return []
    # Use the module name (filename without extension) as the concept name
    name = Path(source_path).stem
    # Skip obviously-irrelevant ones
    if name.startswith("_") or name in ("test", "tests", "setup"):
        return []
    defn = _clean(docstring, max_len=400)
    return [(name, defn, "py_docstring")]


# Words whose presence in the first 5KB of a text signals it's a math /
# philosophy / science work where the prose extractor will yield real
# definitions rather than narrative.  Fiction-only books lack these.
_SCIENTIFIC_MARKERS = (
    'theorem', 'lemma', 'proof', 'corollary', 'proposition',
    'definition', 'axiom', 'postulate', 'hypothesis',
    'equation', 'inequality', 'formula', 'function',
    'philosophy', 'philosophical', 'metaphysics', 'epistemology',
    'logic', 'reason', 'reasoning', 'syllogism', 'inference',
    'mathematics', 'mathematical', 'calculus', 'algebra', 'geometry',
    'number theory', 'probability', 'statistics',
    'physics', 'physical', 'chemistry', 'biology', 'science',
    'algorithm', 'computation', 'set theory', 'topology',
    'principia', 'critique', 'discourse', 'treatise', 'essay',
    'analysis', 'synthesis', 'category',
    # arxiv-style markers
    'abstract:', 'arxiv id:', 'category: math', 'category: hep', 'category: gr-',
    'category: quant', 'category: cond-', 'doi:', 'preprint',
)


def looks_scientific(text: str, sample_chars: int = 6000) -> bool:
    """Return True if the first ~6KB of text looks like math/philosophy/science.

    Used to gate the prose-definition extractor: we only run it on books
    that contain technical vocabulary, otherwise the regex picks up
    narrative grammatical "X is Y" patterns that aren't real concepts.
    """
    if not text:
        return False
    sample = text[:sample_chars].lower()
    hits = sum(1 for m in _SCIENTIFIC_MARKERS if m in sample)
    return hits >= 2  # need at least 2 distinct markers to be confident


def extract_concepts_prose(text: str, source_path: str
                             ) -> List[Tuple[str, str, str]]:
    """Pull (name, definition, role) triples from natural prose.

    Brayden 2026-05-16: stripped the looks_scientific gate.  The math
    distinguishes — fiction's "Captain Lloyd" and physics's "Hilbert
    space" land in DIFFERENT cells; the substrate sorts genre by
    cell-occupancy.  No reason to pre-filter sources.
    """
    out: List[Tuple[str, str, str]] = []
    if not text or len(text) < 50:
        return out
    # Trim Gutenberg headers/footers
    SP = text
    s = SP.find("*** START OF")
    if s >= 0:
        e = SP.find("\n", s)
        if e > 0:
            SP = SP[e + 1:]
    f = SP.find("*** END OF")
    if f >= 0:
        SP = SP[:f]
    for name, defn in _extract_from_research(SP):
        out.append((name, defn, "prose:definition"))
    return out


def study_one_file(path: Path, store: ConceptStore,
                    voice_store: Dict[str, Any],
                    voice_seen: Optional[set] = None) -> Dict[str, int]:
    """Read one source file, extract concepts + prose, write to stores."""
    stats = {"concepts_added": 0, "prose_samples": 0, "skipped_existing": 0,
              "vocab_learned": 0,
              "tier_distribution": {}}
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return stats
    if not text or len(text) < 50:
        return stats

    ext = path.suffix.lower()
    rel = str(path)
    is_external = "/external_corpora/" in rel.replace("\\", "/")

    # SELF-LEARN vocabulary from the first 8KB of every source.  Capped
    # at 6 new words per file to avoid one giant book dumping thousands
    # of false-positive nouns; over a full pass this still adds 1000s
    # of new tokens across the corpus.
    try:
        n_new = auto_learn_from_text(text[:8000], max_new=6)
        if n_new:
            stats["vocab_learned"] = n_new
    except Exception:
        pass
    extracted: List[Tuple[str, str, str]] = []
    if ext in (".md", ".markdown", ".rst", ".txt"):
        extracted = extract_concepts_md(text, rel)
    elif ext in (".tex",):
        extracted = extract_concepts_tex(text, rel)
    elif ext == ".py":
        extracted = extract_concepts_py(text, rel)

    # For external-corpus files, ALSO run the natural-prose extractor.
    # The markdown extractor catches **bold** terms and theorem tables;
    # extract_concepts_prose catches "X is Y." natural-language defs.
    # Both feed the same dedup/tier logic below.
    if is_external:
        prose_hits = extract_concepts_prose(text, rel)
        # Dedup by name (lower) so we don't double-count
        seen_names = {n.lower() for n, _, _ in extracted}
        for n, d, r in prose_hits:
            if n.lower() not in seen_names:
                extracted.append((n, d, r))
                seen_names.add(n.lower())

    path_tier = detect_tier_from_path(rel)
    tier_dist: Dict[str, int] = {}

    for name, defn, role in extracted:
        key = name.lower()
        existing = store.concepts.get(key)
        # NEVER overwrite a user-taught concept
        if existing and existing.source_session != "study":
            stats["skipped_existing"] += 1
            continue
        ops = _operator_signature(defn)
        # Per-row tier from inline status (PROVED, STRUCTURAL, etc.)
        status_tier = detect_tier_from_status_text(defn)
        tier = merge_tier(path_tier, status_tier)
        c = NamedConcept(
            name=name,
            definition=defn,
            operator_signature=ops,
            pattern_used=f"study:{role}",
            source_session="study",
            learned_ts=time.time(),
            tier=tier,
            source_file=rel,
        )
        store.concepts[key] = c
        stats["concepts_added"] += 1
        tier_dist[tier] = tier_dist.get(tier, 0) + 1

    stats["tier_distribution"] = tier_dist

    # Prose samples (for ck_voice_style) -- with dedup
    if voice_seen is None:
        voice_seen = set()
    samples = extract_prose_samples(text, rel, max_samples=3)
    new_samples: List[Dict[str, Any]] = []
    for s in samples:
        h = hash(s["text"])
        if h in voice_seen:
            continue
        voice_seen.add(h)
        s["ops"] = _operator_signature(s["text"])
        s["tier"] = path_tier
        new_samples.append(s)
    if new_samples:
        topic = path.stem
        if topic not in voice_store:
            voice_store[topic] = []
        voice_store[topic].extend(new_samples)
        stats["prose_samples"] = len(new_samples)

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
              log_path: Path, label: str = "pass",
              reset_voice: bool = False) -> Dict[str, Any]:
    """One full pass through the corpus."""
    t0 = time.time()
    sources = discover_sources(root)

    # Voice store: reset each pass to prevent unbounded growth.
    # The samples are paragraphs that already exist in the corpus;
    # they don't need to accumulate across passes.
    voice_store: Dict[str, Any] = {}
    voice_seen: set = set()  # hash dedup within this pass
    if not reset_voice and voice_path.exists():
        try:
            existing = json.loads(voice_path.read_text(encoding="utf-8"))
            # Reload with dedup
            for topic, samples in existing.items():
                if not isinstance(samples, list):
                    continue
                unique = []
                for s in samples:
                    if not isinstance(s, dict):
                        continue
                    h = hash(s.get("text", ""))
                    if h in voice_seen:
                        continue
                    voice_seen.add(h)
                    unique.append(s)
                if unique:
                    voice_store[topic] = unique
        except Exception:
            voice_store = {}
            voice_seen = set()

    totals = {"files_read": 0, "concepts_added": 0,
              "prose_samples": 0, "skipped_existing": 0,
              "errors": 0, "tier_distribution": {}}

    print(f"[study] {label}: walking {len(sources)} sources from {root}")
    for i, p in enumerate(sources):
        try:
            stats = study_one_file(p, store, voice_store, voice_seen=voice_seen)
            totals["files_read"] += 1
            totals["concepts_added"] += stats["concepts_added"]
            totals["prose_samples"] += stats["prose_samples"]
            totals["skipped_existing"] += stats["skipped_existing"]
            # Accumulate tier distribution
            for t, n in (stats.get("tier_distribution") or {}).items():
                totals["tier_distribution"][t] = (
                    totals["tier_distribution"].get(t, 0) + n)
            if (i + 1) % 50 == 0:
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
    totals["voice_unique_samples"] = sum(len(v) for v in voice_store.values())
    _log(log_path, event="pass_complete", label=label, **totals)
    print(f"[study] {label} done: store={totals['store_total']} "
          f"concepts, voice={totals['voice_unique_samples']} unique, "
          f"tiers={totals['tier_distribution']}, "
          f"{totals['elapsed_sec']}s")
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

    # One-time re-index: any concept with empty operator_signature gets
    # semantic_decode applied to its definition, so the cell index is
    # dense before the first retrieval pass.
    updated = store.reindex_signatures_from_text(persist=True)
    if updated:
        print(f"[study-overnight] reindexed    : {updated:,} concepts got new signatures")
    print(f"[study-overnight] cell index   : {store.cell_stats()}")
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

        # PERIODIC SYNTHESIZER (1/3 wobble per CK_FRACTAL_CREATURE_DESIGN):
        # Every 3 passes, run the cross-concept synthesizer to form
        # pattern-cluster meta-concepts.  This is the consolidation
        # the wobble was missing.
        if pass_n % 3 == 0:
            try:
                from ck_synthesizer import synthesize, promote_to_store  # type: ignore
                new_synths = synthesize(store, min_cluster_size=3)
                if new_synths:
                    n_added = promote_to_store(store, new_synths)
                    print(f"[study-overnight] synthesizer pass: "
                          f"+{n_added} new cluster concepts "
                          f"(triggered every 3 passes per wobble cadence)")
            except Exception as e:
                print(f"[study-overnight] synthesizer failed: {e}")

        if pass_n >= 1000 and not args.infinite:
            print("[study-overnight] 1000 passes done; exiting watch mode")
            break

    return 0


if __name__ == "__main__":
    sys.exit(main())
