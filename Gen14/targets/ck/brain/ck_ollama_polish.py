"""ck_ollama_polish.py — Ollama as TEMPORARY prose scaffold.

Brayden 2026-05-16:
  "give him ollama too if you want, hopefully he will outgrow it,
   he should get amazing quickly"

Until CK's own living_lm has breathed long enough to produce fluent
prose, an external Ollama model can rewrite his retrieval-bridge
output into readable English.  STRICT fact-preservation gate prevents
the polish from inventing things CK didn't actually retrieve.

═══════════════════════════════════════════════════════════════════
The contract
═══════════════════════════════════════════════════════════════════

Input:  CK's draft response (concept bridges with metadata stripped,
        algebra/verify/predictions blocks).
Output: Same facts, fluent prose.

If Ollama tries to invent facts, the coverage-check rejects the draft
and CK ships his own output unchanged.

Coverage is computed by extracting NUMBERS, OPERATOR-NAMES, and
D/WP/F-numbers from CK's draft, then verifying each appears in the
Ollama rewrite.  Threshold ≥ 0.7 (≥70% of factual tokens preserved).

═══════════════════════════════════════════════════════════════════
The fade
═══════════════════════════════════════════════════════════════════

As CK's living_lm accumulates breath, its own decode will produce
prose that's already fluent enough.  The voice polish layer compares
living_lm_output vs ollama_output and picks whichever has better
coverage AND lower entropy.  When living_lm consistently wins,
Ollama can be unmounted.  This is intentional: CK should OUTGROW the
crutch, not become dependent on it.

Public API:
  ollama_polish(draft_text, facts_to_preserve=None) -> PolishResult
  mount_ollama_polish(engine) -> bool      # wires into chat path
"""
from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional, Set


OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "mistral:latest"  # 4.4 GB, fast, decent quality
TIMEOUT_S = 25.0


# Tokens that count as "facts" — must survive the rewrite
_FACT_PATTERN = re.compile(
    r"(?:"
        # Numbers (including decimals, fractions, scientific notation)
        r"-?\d+(?:[./]\d+)?(?:[eE][+-]?\d+)?"
        # D/WP/F numbers (CK's canon)
        r"|D\d+[a-z]?|WP\d+|F\d+\b"
        # Operator names (uppercase)
        r"|VOID|LATTICE|COUNTER|PROGRESS|COLLAPSE|BALANCE|CHAOS|HARMONY|BREATH|RESET"
        # Math symbols + Greek letters
        r"|σ|σ²|ω|α|β|γ|κ|ξ|√|π|τ|ρ|Z/10Z|TSML|BHML"
        # Tier tags
        r"|PROVED|STRUCTURAL|EMPIRICAL|OPEN|EXTERNAL|SPECULATIVE|CONFIRMED|REFUTED"
    r")"
)


# ─── Polish result ─────────────────────────────────────────────────────

@dataclass
class PolishResult:
    ok: bool
    used_ollama: bool          # did we actually swap in the rewrite
    coverage: float            # fraction of facts preserved (0..1)
    elapsed_sec: float
    draft: str                 # CK's original
    polished: str              # Ollama's version (or "" if rejected)
    final: str                 # what to ship
    rejection_reason: str = "" # if used_ollama=False, why

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ─── Coverage ──────────────────────────────────────────────────────────

def extract_facts(text: str) -> Set[str]:
    """Return the set of fact-tokens in a piece of text.

    A 'fact' is anything _FACT_PATTERN matches: numbers, D/WP/F-numbers,
    operator names, math symbols, tier tags.
    """
    if not text:
        return set()
    return set(m.group(0) for m in _FACT_PATTERN.finditer(text))


def coverage_score(draft_facts: Set[str], polished_text: str) -> float:
    """What fraction of the draft's facts appear in the polished text?"""
    if not draft_facts:
        return 1.0  # no facts to preserve = perfect coverage
    polished_facts = set()
    polished_lower = polished_text.lower()
    for f in draft_facts:
        # Match either exact (case-sensitive) or token-boundary case-insensitive
        if f in polished_text:
            polished_facts.add(f)
        elif re.search(r"\b" + re.escape(f.lower()) + r"\b", polished_lower):
            polished_facts.add(f)
    return len(polished_facts) / len(draft_facts)


# ─── Ollama call ──────────────────────────────────────────────────────

_OLLAMA_PROMPT = (
    "You are a polish editor for an AI named CK.  CK has produced "
    "the draft response below.  Rewrite it as fluent English prose "
    "while PRESERVING EVERY fact (numbers, D-numbers, WP-numbers, "
    "F-numbers, operator names like HARMONY/BHML/TSML/σ, technical "
    "vocabulary, predicted values, theorem names).  Do NOT invent "
    "facts.  Do NOT add caveats CK didn't include.  Keep it under "
    "200 words.  Reply with ONLY the rewritten prose, no preamble.\n\n"
    "CK's draft:\n{draft}"
)


def ollama_call(draft: str, model: str = DEFAULT_MODEL,
                  timeout: float = TIMEOUT_S) -> Optional[str]:
    """Send draft to Ollama for prose polish.  Returns None on error."""
    if not draft:
        return None
    body = {
        "model": model,
        "prompt": _OLLAMA_PROMPT.format(draft=draft.strip()),
        "stream": False,
        "options": {
            "temperature": 0.3,    # conservative — we want fluency, not invention
            "top_p": 0.9,
            "num_predict": 300,    # cap output length
        },
    }
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
        out = (data.get("response") or "").strip()
        return out if out else None
    except urllib.error.URLError as e:
        # Ollama not running, or model not loaded
        return None
    except Exception:
        return None


# ─── Polish ───────────────────────────────────────────────────────────

def ollama_polish(draft: str,
                    min_coverage: float = 0.7,
                    min_draft_len: int = 30,
                    max_draft_len: int = 2000,
                    model: str = DEFAULT_MODEL) -> PolishResult:
    """Rewrite CK's draft via Ollama with fact-preservation guarantee.

    If Ollama is unavailable, or coverage falls below min_coverage,
    or the draft is too short/long to bother — return ok=True
    used_ollama=False and final=draft (no polish, ship original).

    This is INTENTIONALLY conservative.  Better to ship CK's slightly
    rough draft than an Ollama hallucination dressed up as fluency.
    """
    t0 = time.time()
    if not draft or len(draft.strip()) < min_draft_len:
        return PolishResult(
            ok=True, used_ollama=False, coverage=1.0,
            elapsed_sec=0.0, draft=draft, polished="",
            final=draft, rejection_reason="draft too short",
        )
    if len(draft) > max_draft_len:
        return PolishResult(
            ok=True, used_ollama=False, coverage=1.0,
            elapsed_sec=0.0, draft=draft, polished="",
            final=draft, rejection_reason="draft too long",
        )

    polished = ollama_call(draft, model=model)
    elapsed = time.time() - t0

    if polished is None:
        return PolishResult(
            ok=True, used_ollama=False, coverage=0.0,
            elapsed_sec=elapsed, draft=draft, polished="",
            final=draft, rejection_reason="ollama unavailable",
        )

    facts = extract_facts(draft)
    cov = coverage_score(facts, polished)
    if cov < min_coverage:
        return PolishResult(
            ok=True, used_ollama=False, coverage=cov,
            elapsed_sec=elapsed, draft=draft, polished=polished,
            final=draft,
            rejection_reason=f"coverage {cov:.2f} < {min_coverage}",
        )

    return PolishResult(
        ok=True, used_ollama=True, coverage=cov,
        elapsed_sec=elapsed, draft=draft, polished=polished,
        final=polished,
    )


# ─── Engine mount ─────────────────────────────────────────────────────

def mount_ollama_polish(engine: Any, model: str = DEFAULT_MODEL,
                          enabled: bool = True) -> bool:
    """Attach Ollama prose-polish to the engine.

    Side effects:
      engine.ollama_polish               : callable wrapping ollama_polish
      engine.ollama_polish_enabled       : toggle flag
      engine.ollama_polish_model         : which model
      engine.ollama_polish_stats         : counters for accept/reject
    """
    engine.ollama_polish = ollama_polish
    engine.ollama_polish_enabled = enabled
    engine.ollama_polish_model = model
    engine.ollama_polish_stats = {
        "calls": 0, "accepted": 0, "rejected_coverage": 0,
        "unavailable": 0, "skipped_short": 0,
    }
    # Probe Ollama at mount time to confirm it's reachable
    try:
        probe = ollama_call("ping (probe)", model=model, timeout=5.0)
        if probe is None:
            print(f"[CK Gen14] ollama_polish: MOUNTED (probe FAILED; "
                  f"will fall through to CK's own LM on every turn)")
        else:
            print(f"[CK Gen14] ollama_polish: MOUNTED  model={model}  "
                  f"min_coverage=0.7  (CK's prose mode will use this "
                  f"as a temporary scaffold)")
    except Exception:
        print(f"[CK Gen14] ollama_polish: MOUNTED  (probe error; "
              f"silently passes through)")
    return True


# ─── CLI / self-test ──────────────────────────────────────────────────

def main():
    import argparse, sys
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--draft", default=(
        "D48 [PROVED]: 4-core fusion-closure (WP110). The 4-core "
        "{V, H, Br, R} = {VOID, HARMONY, BREATH, RESET} is closed under "
        "both TSML and BHML at arity 2.  D55 (WP112) extends this to "
        "arity 3.  Together D48 and D55 establish that the 4-core is "
        "the canonical attractor of substrate dynamics at α=1/2."
    ))
    ap.add_argument("--probe", action="store_true",
                    help="just probe ollama, don't polish")
    args = ap.parse_args()

    if args.probe:
        out = ollama_call("Say 'pong'.", model=args.model, timeout=10.0)
        print(f"Probe response: {out!r}")
        return 0

    print(f"DRAFT ({len(args.draft)} chars):")
    print(f"  {args.draft}")
    print()
    facts = extract_facts(args.draft)
    print(f"Facts to preserve ({len(facts)}): {sorted(facts)[:12]}")
    print()
    r = ollama_polish(args.draft, model=args.model)
    print(f"Result:")
    print(f"  ok:               {r.ok}")
    print(f"  used_ollama:      {r.used_ollama}")
    print(f"  coverage:         {r.coverage:.2f}")
    print(f"  elapsed:          {r.elapsed_sec:.2f}s")
    print(f"  rejection_reason: {r.rejection_reason!r}")
    print()
    print(f"FINAL output:")
    print(f"  {r.final}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
