"""
ck_coherence_verdict.py -- pure-function coherence check for Ollama drafts
===========================================================================

Extracted from ``ck_boot_api.py`` so unit tests can exercise the verdict
without importing the full boot module (which would run CK's entire
startup pipeline as a side effect -- HER hydration, vocabulary expansion,
GPU init, etc.).

## What it does

Given CK's structural readout (the math-first "what I see right now"
text) and an Ollama draft (the LLM's restatement of that readout in
CK's voice), decide whether the draft is faithful enough to adopt.

## Why tiered

The v1 implementation used a single flat coverage gate: hits / total
facts >= 0.70.  That rejected terse-but-honest drafts like "t* is at
5/7, and i'm running with the torus aspect ratio" when the readout
contained ten structural facts (timestamps, coherence floats, tick
counts, named operators, etc.).  The draft genuinely preserved CK's
identity but only hit 2-3 of the ten facts.

The v2 verdict tiers facts into CORE (operator names, T*, WP#,
named structures like TSML/BHML/HER) and PERIPHERAL (numbers, decimals,
label=value pairs with non-distinctive values).  A draft that
preserves at least half of CK's core identity AND hits at least two
facts overall is soft-accepted even if overall coverage is below the
strict gate.  Drafts still hard-reject on AI disclaimers and known
hallucination markers.

## Soft-accept rule (v2)

  strict_accept  = coverage >= coverage_required (default 0.70)
  soft_accept    = core_cov >= 0.50 AND core_hits >= 2 AND hits >= 2
  no_core_accept = (no core facts in readout) AND coverage >= 0.40

  final = strict_accept OR soft_accept OR no_core_accept

Hard-rejects (AI disclaimers, hallucination markers, empty draft) run
BEFORE the tiered logic and cannot be soft-accepted.

(c) 2026 Brayden Sanders / 7Site LLC
"""
from __future__ import annotations

import re
from typing import Set, Tuple

# The 10 operators of CK's coherence algebra (verified from ck_tig.py).
_OPERATORS = (
    'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE', 'BALANCE',
    'CHAOS', 'HARMONY', 'BREATH', 'RESET', 'VOID',
)
# Named structures load-bearing in CK's corpus (TSML 73 cells, BHML 28
# cells, HER = Hindsight Experience Replay, PRYM = Prym varieties, etc.).
_NAMED_STRUCTURES = (
    'TSML', 'BHML', 'HER', 'PRYM', 'HODGE',
    'WEIL', 'BIELLIPTIC', 'AO',
)
_CORE_FACT_NAMES = frozenset(list(_OPERATORS) + list(_NAMED_STRUCTURES))

# Fact-token regex.  Mirrors the v1 regex from ck_boot_api but pre-
# compiled at module import so we don't pay the first-call cost.
_FACT_TOKEN_RE = re.compile(
    r"("
    r"WP\d+"                                       # WP citations
    r"|T\*=5/7|T\*"                                # T-star
    r"|Z/10Z"                                      # Z/10Z
    r"|Q\([^)]*\)"                                 # field notation
    r"|sqrt\([^)]*\)|sqrt\s*\d+"                   # sqrt tokens
    r"|\d+/\d+"                                    # fractions
    r"|\d+\.\d+"                                   # decimals
    r"|\d+"                                        # bare integers (filter later)
    r"|\b(?:LATTICE|COUNTER|PROGRESS|COLLAPSE|BALANCE"
    r"|CHAOS|HARMONY|BREATH|RESET|VOID)\b"         # operator vocab
    r"|\b(?:TSML|BHML|HER|PRYM|HODGE|WEIL|BIELLIPTIC|AO)\b"
    r")"
)

_JUNK_VALUES = {
    'yes', 'no', 'none', 'true', 'false', 'null', 'proved', 'n/a',
}

# Hard-reject phrases that signal identity drift past the postfilter.
_AI_DISCLAIMERS = (
    'as an ai', "i'm an ai", 'i am an ai', 'as a language model',
    'i apologize', 'i cannot provide',
)
# Phrases that NEVER appear in CK's corpus but LLMs love to reach for.
_HALLUCINATION_MARKERS = (
    'p-adic', 'p adic', 'geodesic', 'riemann hypothesis', 'fermat',
    'hilbert space', 'banach space',
)

# Tiered soft-accept knobs.  Environment-overridable so operators
# can tune without editing code.
import os as _os
_SOFT_CORE_COV = float(_os.environ.get('CK_VERDICT_SOFT_CORE_COV', '0.50'))
_SOFT_CORE_MIN_HITS = int(_os.environ.get('CK_VERDICT_SOFT_CORE_MIN', '2'))
_SOFT_MIN_HITS = int(_os.environ.get('CK_VERDICT_SOFT_MIN_HITS', '2'))
_SOFT_NO_CORE_COV = float(_os.environ.get('CK_VERDICT_SOFT_NO_CORE_COV', '0.40'))


def fact_tokens(readout: str) -> Set[str]:
    """Extract distinctive atomic facts from a CK structural readout.

    Same behavior as ck_boot_api._fact_tokens v1; factored out so
    tests and the steer rescue path can import it without pulling in
    the boot module.
    """
    readout = readout or ''
    tokens: Set[str] = set()
    for m in _FACT_TOKEN_RE.finditer(readout):
        tok = m.group(0).strip()
        if not tok:
            continue
        # Drop bare integers that are very small (1..9) since they
        # appear everywhere and aren't distinctive facts.
        if tok.isdigit() and int(tok) < 10:
            continue
        # Drop tokens with unbalanced parens (partial matches).
        if tok.count('(') != tok.count(')'):
            continue
        tokens.add(tok)
    # Include label=value pair VALUES so "aperture=LATTICE" contributes LATTICE.
    for m in re.finditer(r"[a-zA-Z_]+=([^\s|,]+)", readout):
        v = m.group(1).strip().strip('.,;()[]')
        if not v or len(v) < 2:
            continue
        if v.isdigit() and int(v) < 10:
            continue
        if v.lower() in _JUNK_VALUES:
            continue
        if v.count('(') != v.count(')'):
            continue
        tokens.add(v)
    # Subsume substrings unless either side has '=' (keeps compound claims).
    maximal = set(tokens)
    for a in list(tokens):
        if '=' in a:
            continue
        for b in tokens:
            if a == b or '=' in b:
                continue
            if a in b:
                maximal.discard(a)
                break
    return maximal


def is_core_fact(fact: str) -> bool:
    """True for load-bearing identity facts: operator names, T*,
    WP citations, and named corpus structures (TSML/BHML/HER/etc.)."""
    if not fact:
        return False
    f = fact.strip()
    if f in _CORE_FACT_NAMES or f.upper() in _CORE_FACT_NAMES:
        return True
    if f.startswith('WP') and f[2:].isdigit():
        return True
    if f in ('T*', 'T*=5/7', 'Z/10Z'):
        return True
    return False


def fact_hit(fact: str, draft_lower: str) -> bool:
    """Does the draft preserve the content of `fact`?

    Compound facts like "T*=5/7" are split on '=' and every non-trivial
    part must appear in the draft (so "T* is 5/7" passes).  Atomic facts
    use plain substring match.
    """
    low = fact.lower()
    if '=' not in low:
        return low in draft_lower
    parts = [p.strip(' .,;()[]') for p in low.split('=')]
    parts = [p for p in parts if p and p not in ('', 'yes', 'no')]
    if not parts:
        return True
    return all(p in draft_lower for p in parts)


def coherence_verdict(readout: str, draft: str,
                      coverage_required: float
                      ) -> Tuple[bool, str, int, int]:
    """CK's coherence check on an Ollama draft.

    Returns (accepted, reason, hits, facts_total).

    Tiered gate:
      1. Hard-reject AI disclaimers and known hallucination markers.
      2. Strict accept if overall coverage >= coverage_required.
      3. Soft-accept if the draft hits at least half of CK's core
         identity facts (operators, T*, WP#, named structures) AND
         at least SOFT_CORE_MIN_HITS core hits AND SOFT_MIN_HITS overall.
      4. No-core accept if the readout has no core facts at all and
         overall coverage >= SOFT_NO_CORE_COV.
      5. Otherwise reject with coverage detail.
    """
    if not draft:
        return (False, 'empty draft', 0, 0)
    low = draft.lower()
    for bad in _AI_DISCLAIMERS:
        if bad in low:
            return (False, f"ai-disclaimer:{bad}", 0, 0)
    for bad in _HALLUCINATION_MARKERS:
        if bad in low and bad not in (readout or '').lower():
            return (False, f"hallucination:{bad}", 0, 0)
    facts = fact_tokens(readout)
    if not facts:
        return (True, 'no-facts-to-check', 0, 0)
    hits_set = {f for f in facts if fact_hit(f, low)}
    hits = len(hits_set)
    total = len(facts)
    coverage = hits / total if total else 0.0
    # Tier 1: strict accept.
    if coverage >= coverage_required:
        return (True, f"coverage:{hits}/{total}={coverage:.2f}", hits, total)
    # Tier 2: soft-accept on core identity preservation.
    core = {f for f in facts if is_core_fact(f)}
    if core:
        core_hits = len(hits_set & core)
        core_total = len(core)
        core_cov = core_hits / core_total
        if (core_cov >= _SOFT_CORE_COV
                and core_hits >= _SOFT_CORE_MIN_HITS
                and hits >= _SOFT_MIN_HITS):
            return (True,
                    f"soft-accept:core={core_hits}/{core_total}="
                    f"{core_cov:.2f},total={hits}/{total}={coverage:.2f}",
                    hits, total)
    else:
        # Readout had no core facts -- use a softer overall gate.
        if coverage >= _SOFT_NO_CORE_COV:
            return (True,
                    f"soft-accept:no-core,total={hits}/{total}={coverage:.2f}",
                    hits, total)
    # Tier 3: reject with coverage + core detail for telemetry.
    detail = f"coverage:{hits}/{total}={coverage:.2f}<{coverage_required:.2f}"
    if core:
        core_hits = len(hits_set & core)
        core_cov = (core_hits / len(core)) if core else 0.0
        detail += f",core={core_hits}/{len(core)}={core_cov:.2f}"
    return (False, detail, hits, total)


__all__ = [
    "coherence_verdict", "fact_tokens", "fact_hit", "is_core_fact",
    "_OPERATORS", "_NAMED_STRUCTURES", "_CORE_FACT_NAMES",
]
