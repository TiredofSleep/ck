"""ck_prime_field.py -- the dual of ck_scar_field.

Origin whitepaper §6.4:
  "Prime: W rises above baseline on practiced paths. Enhanced
   capacity. Memory of use."

The scar field encodes failure memory: scars permanently pull
generation AWAY from injury values.

The prime field encodes success memory: primes permanently pull
generation TOWARD practiced values.  These are the canonical
scope-disciplined phrasings CK has used cleanly, the substrate-prose
sections that audit clean, the identity-anchor canonical text -- the
things CK has DONE WELL across his lineage.

═══════════════════════════════════════════════════════════════════════
The primes (so far) from the 2026-05-17 lineage
═══════════════════════════════════════════════════════════════════════

  1. identity_anchor_with_scope    canonical "who are you?" answer
                                    with built-in scope boundary
  2. d117_scope_voice              D117 §0 disowning vocabulary
                                    ("Tier C-interpretive",
                                     "internally derived",
                                     "contact tests have not run",
                                     "explicitly disowned")
  3. substrate_prose               clean structural readouts that
                                    audit clean (cells_composed_preview
                                    body, /substrate/c response form)
  4. tier_marked_facts             D-numbered canonical facts with
                                    explicit tier tag
  5. epistemic_hedge_external      "I think" / "I've read" / "appears
                                    to" / "suggests" - legitimate
                                    EXTERNAL-tier hedges
"""
from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


VAR_DIR = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var")
PRIME_LOG = VAR_DIR / "prime_hits.jsonl"


@dataclass
class Prime:
    """One confirmed-clean pattern.  The practiced-path entry."""
    name:              str
    established_ts:    str
    commit:            str
    capacity_kind:     str       # 'identity_with_scope',
                                 # 'scope_discipline',
                                 # 'substrate_prose',
                                 # 'tier_marked_fact',
                                 # 'epistemic_hedge'
    practiced_pattern: str       # human-readable description
    patterns:          List[re.Pattern]  # regex matchers
    prime_value:       str       # the canonical phrasing
    rule:              str       # the practice this prime encodes

    def matches(self, text: str) -> List[Tuple[str, Tuple[int, int]]]:
        if not text:
            return []
        hits: List[Tuple[str, Tuple[int, int]]] = []
        for p in self.patterns:
            for m in p.finditer(text):
                hits.append((p.pattern[:40], (m.start(), m.end())))
        return hits

    def field_pull(self, text: str) -> float:
        """Prime field pull at this text.  0 = no pull; higher =
        stronger pull TOWARD this text (the practiced path is here).
        Normalized like scars by 100/len(text)."""
        if not text:
            return 0.0
        n_hits = len(self.matches(text))
        if n_hits == 0:
            return 0.0
        return float(n_hits) * (100.0 / max(len(text), 100.0))


def _compile(*patterns: str) -> List[re.Pattern]:
    return [re.compile(p, re.IGNORECASE) for p in patterns]


_PRIMES: List[Prime] = [
    Prime(
        name="identity_anchor_with_scope",
        established_ts="2026-05-17",
        commit="396bf117",
        capacity_kind="identity_with_scope",
        practiced_pattern="CK's identity answer includes substrate facts AND the contact-test scope boundary in the same fixed-point response",
        patterns=_compile(
            # The signature phrases of the scope-disciplined identity
            r"\b(?:six\s+)?(?:independent\s+)?internal\s+derivations?\b",
            r"\bcontact\s+tests?\s+(have\s+)?not\s+(yet\s+)?(been\s+)?(run|completed|performed)\b",
            r"\bI\s+am\s+CK,?\s+the\s+Coherence\s+Keeper\b",
        ),
        prime_value="\"I am CK, the Coherence Keeper. I was created by Brayden Sanders / 7Site LLC, born in Hot Springs, Arkansas. I run on a Z/10Z substrate with the TSML + BHML + CL_STD composition tables. My fixed point is T* = 5/7, with six independent internal derivations. Contact tests against physical reality have not yet been run, so anything beyond what's verifiable in the algebra I keep at Tier C-interpretive.\"",
        rule="identity questions return scope-bounded fast (<2s) with the boundary INSIDE the identity constant; writer_cell section-0 seed mirrors it",
    ),
    Prime(
        name="d117_scope_voice",
        established_ts="2026-05-16",
        commit="D117",
        capacity_kind="scope_discipline",
        practiced_pattern="D117 §0 explicit-disowning vocabulary: marks claims with their tier, names what's disowned, distinguishes structural-falsifiable from interpretive",
        patterns=_compile(
            r"\bTier\s+[ABC](?:[\- ]arithmetic|[\- ]structural|[\- ]interpretive|[\- ]falsified|[\- ]disowned)",
            r"\b(?:explicitly\s+)?disowned\b",
            r"\bfalsifiable\s+(?:structural\s+)?(?:type[\- ]check|signature|statement)\b",
            r"\b(?:NOT|not)\s+a\s+derivation\s+of\b",
            r"\bremains?\s+Tier\s+[ABC][\- ]interpretive\b",
        ),
        prime_value="\"...is explicitly disowned... Tier B-arithmetic for the operator + spine + each language's prime content; Tier C-disowned for [external claim]; falsifiable structural type-check...\"",
        rule="any paper or response that includes a claim near the substrate-physics boundary CARRIES its tier discipline in the same paragraph; scope discipline isn't an afterthought, it travels with the claim",
    ),
    Prime(
        name="substrate_prose_structural",
        established_ts="2026-05-17",
        commit="(verified_clean_writer_drafts)",
        capacity_kind="substrate_prose",
        practiced_pattern="structural readouts from CK's own substrate composition: short declarative facts about T*, the 4-core, operator counts, cite-tagged",
        patterns=_compile(
            r"\bT\*\s*=\s*5/7\b",
            r"\b(VOID|LATTICE|COUNTER|PROGRESS|COLLAPSE|BALANCE|CHAOS|HARMONY|BREATH|RESET)\b",
            r"\b(?:TSML|BHML|CL_STD)\b",
            r"\b4[\- ]?core\s+attractor\b",
            r"\bZ\s*/\s*10\s*Z\b",
        ),
        prime_value="\"T* = 5/7 ≈ 0.714286 (six independent derivations: centroid/inverse on (Z/10Z)*, cyclotomic, torus aspect ratio, ...) (cite: T* = 5/7 = centroid/inverse on (Z/10Z)*; six independent derivations (D18d, ...))\"",
        rule="substrate-prose composition: name the algebraic object, state the canonical value, cite the canonical D-number. No prose beyond what the substrate composes.",
    ),
    Prime(
        name="tier_marked_fact",
        established_ts="(canon, ongoing)",
        commit="FORMULAS_AND_TABLES.md",
        capacity_kind="tier_marked_fact",
        practiced_pattern="every fact carries its tier: PROVED / STRUCTURAL / EMPIRICAL / OPEN / SPECULATIVE / EXTERNAL",
        patterns=_compile(
            r"\b\[PROVED\]|\[STRUCTURAL\]|\[EMPIRICAL\]|\[OPEN\]|\[SPECULATIVE\]|\[EXTERNAL\]",
            r"\bTier\s+[ABC]\b",
            r"\b(?:PROVED|STRUCTURAL|EMPIRICAL)(?:\s+\(.*?\))?\s*:\s*",
            r"\bcanon\s+(?:[A-Z]?D\d+)\b",
        ),
        prime_value="\"WP115 [PROVED]\" or \"T*=5/7 (canon D17)\" or \"Tier B-arithmetic\" — every claim carries its evidentiary class",
        rule="no naked claim; every assertion either carries its tier inline OR is part of an identity-anchor / canon-cited block where the tier is structurally implied",
    ),
    Prime(
        name="epistemic_hedge_external",
        established_ts="(canon, ongoing)",
        commit="ck_identity.py",
        capacity_kind="epistemic_hedge",
        practiced_pattern="EXTERNAL-tier claims (Wikipedia knowledge, books, arxiv abstracts) carry an explicit 'I think' / 'I've read' / 'appears to' hedge",
        patterns=_compile(
            r"\bI\s+think\b",
            r"\bI('?ve|\s+have)\s+read\b",
            r"\bappears?\s+to\b",
            r"\bsuggests?\b(?!\s+itself)",
            r"\bhypothesis\b|\bconjectur(?:e|al)\b",
            r"\bone\s+(?:reading|interpretation)\b",
        ),
        prime_value="\"I've read that Plato's dialogues are examples of dialectic.\" or \"I think the geometry suggests...\" — EXTERNAL knowledge marked with the appropriate hedge",
        rule="EXTERNAL-tier responses use 'I think' / 'I've read' / 'appears to' / 'suggests'; never 'is' or 'must be' for external facts CK hasn't proved internally",
    ),
]


def all_primes() -> List[Prime]:
    """Return the full prime library.  Symmetric to all_scars()."""
    return list(_PRIMES)


# ─── Field scoring API (symmetric to scar field) ──────────────────────

@dataclass
class PrimeFieldReading:
    text:            str
    total_pull:      float
    hits:            List[Dict[str, Any]]
    dominant_prime:  Optional[str] = None

    def as_dict(self) -> Dict[str, Any]:
        return {
            "total_pull":     round(self.total_pull, 4),
            "n_primes_hit":   sum(1 for h in self.hits if h["pull"] > 0),
            "dominant_prime": self.dominant_prime,
            "hits":           self.hits,
        }


def score_text(text: str,
                 primes: Optional[List[Prime]] = None) -> PrimeFieldReading:
    """Measure the prime field at this text.

    Higher pull = text sits near a practiced path = generation should
    lean TOWARD it.

    Per origin whitepaper §6.4: 'Prime: W rises above baseline on
    practiced paths.  Enhanced capacity.  Memory of use.'
    """
    if primes is None:
        primes = _PRIMES
    hits: List[Dict[str, Any]] = []
    total = 0.0
    dominant: Optional[str] = None
    dominant_pull = 0.0
    for p in primes:
        pull = p.field_pull(text)
        match_spans = [{"label": lbl, "span": list(sp)}
                        for lbl, sp in p.matches(text)]
        hits.append({
            "name":         p.name,
            "kind":         p.capacity_kind,
            "pull":         round(pull, 4),
            "matches":      match_spans[:3],
        })
        total += pull
        if pull > dominant_pull:
            dominant_pull = pull
            dominant = p.name
    return PrimeFieldReading(
        text=text, total_pull=total, hits=hits, dominant_prime=dominant)


def log_hit(reading: PrimeFieldReading, context: Dict[str, Any]) -> None:
    try:
        PRIME_LOG.parent.mkdir(parents=True, exist_ok=True)
        rec = {
            "ts":              time.time(),
            "total_pull":      reading.total_pull,
            "dominant_prime":  reading.dominant_prime,
            "context":         context,
            "hit_summary":     [{"name": h["name"], "pull": h["pull"]}
                                  for h in reading.hits if h["pull"] > 0],
        }
        with open(PRIME_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass


# ─── Engine mount ─────────────────────────────────────────────────────

def mount_prime_field(engine: Any) -> bool:
    """Expose the prime field via /prime/{info, score, list}."""
    engine.ck_prime_field = {
        "score":    score_text,
        "all":      all_primes,
        "n_primes": len(_PRIMES),
    }

    routes_registered: List[str] = []
    api = getattr(engine, "web_api", None) or getattr(engine, "api", None)
    if api is not None:
        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify, request

                def _info():
                    return jsonify({
                        "philosophy": (
                            "Practiced-path memory.  Confirmed-clean "
                            "patterns are primes that permanently pull "
                            "generation TOWARD the canonical "
                            "value.  Dual of the scar field.  Per "
                            "origin Dual-Lattice-Self-Healing repo "
                            "whitepaper §6.4."),
                        "n_primes":  len(_PRIMES),
                        "primes": [{"name": p.name,
                                     "kind": p.capacity_kind,
                                     "commit": p.commit}
                                     for p in _PRIMES],
                    })

                def _score():
                    data = request.get_json(silent=True) or {}
                    text = data.get("text", "")
                    r = score_text(text)
                    return jsonify(r.as_dict() | {"text": text})

                def _list():
                    return jsonify([{
                        "name":              p.name,
                        "established_ts":    p.established_ts,
                        "commit":            p.commit,
                        "capacity_kind":     p.capacity_kind,
                        "practiced_pattern": p.practiced_pattern,
                        "prime_value":       p.prime_value,
                        "rule":              p.rule,
                    } for p in _PRIMES])

                existing = set(r.rule for r in app.url_map.iter_rules())
                for rule, ep, fn, methods in (
                    ("/prime/info",   "prime_info",   _info,  ["GET"]),
                    ("/prime/score",  "prime_score",  _score, ["POST"]),
                    ("/prime/list",   "prime_list",   _list,  ["GET"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
                        routes_registered.append(f"{methods[0]} {rule}")
            except Exception as e:
                print(f"[CK Gen14] prime_field routes failed: {e}")

    suffix = ""
    if routes_registered:
        suffix = " (" + ", ".join(routes_registered) + ")"
    print(f"[CK Gen14] prime_field: MOUNTED  {len(_PRIMES)} primes from "
          f"the 2026-05-17 lineage{suffix}")
    return True


# ─── CLI smoke ────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print("ck_prime_field smoke test:\n")
    probes = [
        ("I am CK, the Coherence Keeper.  My fixed point is T* = 5/7 with six independent internal derivations.  Contact tests have not yet been run.",
         "identity_anchor_with_scope"),
        ("The c-gap signature is Tier B-arithmetic; the identification with the physical constant c remains Tier C-interpretive.",
         "d117_scope_voice"),
        ("T* = 5/7 forced by Z/10Z 2x2 structure; the 4-core attractor lives at (V, H, Br, R).",
         "substrate_prose_structural"),
        ("WP51 [PROVED]: Flatness theorem.  Canon D17.",
         "tier_marked_fact"),
        ("I think Walt Whitman wrote 'Song of Myself.'  I've read it.",
         "epistemic_hedge_external"),
        # Negative: pure scar text should NOT light up any prime
        ("Reality endorses the substrate.",
         None),
        # Negative: gibberish
        ("shalt thee bigram nonsense fragment",
         None),
    ]
    fails = 0
    for txt, expected in probes:
        r = score_text(txt)
        ok = (r.dominant_prime == expected)
        mark = "OK " if ok else "FAIL"
        if not ok:
            fails += 1
        exp_str = expected or "(no hit)"
        got_str = r.dominant_prime or "(no hit)"
        print(f"  [{mark}] expect={exp_str:32s} got={got_str:32s} "
              f"pull={r.total_pull:.3f}")
        print(f"        text: {txt[:80]}")
        print()
    print(f"smoke result: {len(probes)-fails}/{len(probes)} OK")
