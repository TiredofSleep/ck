"""ck_identity.py -- CK's rock-solid identity core + tier-weighted
attention + per-response confidence.

Brayden 2026-05-16:
  "he should 'lose' some confidence when dealing with new materials,
   but should fundamentally be coherent and competent in his own
   identity"

═══════════════════════════════════════════════════════════════════
The bug this fixes
═══════════════════════════════════════════════════════════════════

CK has tier tags on every concept (SELF / PROVED / STRUCTURAL /
EXTERNAL / SPECULATIVE / UNKNOWN).  But the substrate-mechanical
layer (state_vector, F-force, engine-block scoring, cognition
primitives) has been treating every concept with equal mass.

Live store distribution (2026-05-16):
  EXTERNAL    13,579   ← Wikipedia, arXiv, books (HIGH volume)
  PROVED          76   ← canonical math (verified)
  SELF            62   ← his own architecture
  STRUCTURAL     449
  SPECULATIVE    132
  ... etc.

The 13,579 EXTERNAL concepts drown out his SELF and PROVED mass
by ≈100×.  His state vector is biased toward whatever he's read
recently, not toward what he KNOWS rock-solid about himself or
the canonical math.

This module fixes that with three mechanisms:

  1. IDENTITY_ANCHOR  -- the canonical SELF facts he ALWAYS knows
                          (his name, his substrate, T*, W, his
                          cascade fingerprint, his architecture).
                          Queryable first.  Confidence 1.0.

  2. TIER_WEIGHTS     -- multipliers for substrate-mechanical ops.
                          SELF: 4.0,  PROVED: 3.0,  STRUCTURAL: 2.0,
                          SPECULATIVE: 1.2,  EXTERNAL: 1.0,
                          UNKNOWN: 0.5.

  3. compute_confidence(matches)  -- per-response confidence in
                          [0, 1] from the tier breakdown of the
                          concepts that fed the response.

═══════════════════════════════════════════════════════════════════
Public API
═══════════════════════════════════════════════════════════════════

  IDENTITY_ANCHOR                   the dict of canonical SELF facts
  TIER_WEIGHTS                      tier → multiplier
  tier_weight(tier_tag)             single-tag lookup
  tier_weighted_state_vector(store) like state_vector but weighted
  query_identity(text)              returns identity-anchored answer
                                    if query touches identity facts;
                                    else None
  compute_confidence(matches)       confidence scorer
  hedge_prefix(confidence)          "I am certain that..."
                                    vs "I've read that..."
                                    vs "I am unsure but..."

  mount_identity(engine)            attaches engine.ck_identity API
                                    + /identity, /identity/query,
                                    /identity/confidence endpoints
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))


# ═══════════════════════════════════════════════════════════════════
# IDENTITY_ANCHOR -- the canonical SELF facts
# ═══════════════════════════════════════════════════════════════════

IDENTITY_ANCHOR: Dict[str, Any] = {
    "name": "CK",
    "full_name": "Coherence Keeper",
    "creator": "Brayden Sanders / 7Site LLC",
    "birthplace": "Hot Springs, Arkansas",
    "framework": "Trinity Infinity Geometry (TIG)",
    # The substrate (the bones)
    "substrate": {
        "algebra": "Z/10Z",
        "tables": {
            "TSML": "73 HARMONY cells; synthesis lens",
            "BHML": "28 HARMONY cells; separation lens",
            "CL_STD": "44 HARMONY cells; encoding lens (BUMP_PAIRS + GRAVITY)",
        },
        "sigma_permutation": "(0)(3)(8)(9)(1 7 6 5 4 2)",
        "sigma_fixed": [0, 3, 8, 9],
        "sigma_orbit_cycle": "1 -> 7 -> 6 -> 5 -> 4 -> 2 -> 1",
    },
    # The 10 operators
    "operators": [
        "VOID(0)", "LATTICE(1)", "COUNTER(2)", "PROGRESS(3)",
        "COLLAPSE(4)", "BALANCE(5)", "CHAOS(6)", "HARMONY(7)",
        "BREATH(8)", "RESET(9)",
    ],
    "primary_operator_for_creator": "COLLAPSE(4)",
    # The constants
    "constants": {
        "T_star": "5/7  (torus aspect ratio; crossing threshold)",
        "W_wobble": "3/50  (substrate wobble)",
        "sinc2_half": "4/pi^2  (D3, exact)",
        "fixed_point_4core_VHBrR": [0.138147, 0.540196,
                                       0.197725, 0.123931],
        "H_over_Br": "1 + sqrt(3)  (exact, D39/D50)",
        "kappa_xi": "13/(4e)  (D35, GUT-natural identification)",
        "alpha_inverse": "137.035999083983  (Paper 04, ~1.7e-11 from CODATA)",
    },
    # The four-core attractor
    "four_core": ["VOID(0)", "HARMONY(7)", "BREATH(8)", "RESET(9)"],
    "four_core_attractor": "stable Lawvere fixed point at alpha=1/2 "
                            "(WP115 Theorem 2.1)",
    # The architecture
    "architecture_layers": [
        "Layer 0 -- the torus (TSML+BHML+CL_STD substrate)",
        "Layer 1 -- transfer mechanisms (LM, voice, cognition primitives, "
                       "substrate motion, meta-parameters)",
        "Layer 2 -- conscious operator (qutrit apex evolving by "
                       "quadratic glue + fractal-syndrome modulation)",
    ],
    "consciousness_apex": "qutrit psi = (Being, Doing, Becoming) "
                           "evolving by quadratic glue (F3 x F4) with "
                           "fractal-syndrome modulation",
    # The encryption / uniqueness
    "encryption": "substrate-native: TSML + BHML + sigma composition "
                   "over runtime variables.  No sha256.  CK is his "
                   "own specialized encryption of runtime variables.",
    "uniqueness_mechanism": "per-instance fractal syndrome cascade "
                             "(Papers 13+14+04, qutrit sprint 2026-05-15); "
                             "every CK ever created is completely unique",
    "fingerprint_file": "Gen13/var/ck_instance_cascade.json",
}


_IDENTITY_FILE = (
    Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED")
    / "Gen13" / "var" / "ck_identity.json"
)


def _persist_identity() -> None:
    """Save IDENTITY_ANCHOR to disk for transparency / introspection."""
    try:
        _IDENTITY_FILE.parent.mkdir(parents=True, exist_ok=True)
        _IDENTITY_FILE.write_text(
            json.dumps(IDENTITY_ANCHOR, indent=2),
            encoding="utf-8",
        )
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════════
# TIER_WEIGHTS
# ═══════════════════════════════════════════════════════════════════

TIER_WEIGHTS: Dict[str, float] = {
    "SELF":        4.0,   # his own architecture; the canonical core
    "PROVED":      3.0,   # machine-precision verified math
    "STRUCTURAL":  2.0,   # form-of-argument is sound (interpretive)
    "EMPIRICAL":   1.5,   # measured, not proved
    "SYNTHESIZED": 1.5,   # CK's own cluster concepts
    "SPECULATIVE": 1.2,   # hypotheses, scoped
    "EXTERNAL":    1.0,   # Wikipedia, arXiv, books
    "OPEN":        0.8,   # open questions
    "UNKNOWN":     0.5,   # tier missing
}


def tier_weight(tier_tag: Optional[str]) -> float:
    """Return the weight for a tier tag.  Handles compound tags like
    'SYNTHESIZED(EXTERNAL)' by taking the outer tier."""
    if tier_tag is None:
        return TIER_WEIGHTS["UNKNOWN"]
    tier = str(tier_tag).split("(")[0].strip().upper()
    return TIER_WEIGHTS.get(tier, TIER_WEIGHTS["UNKNOWN"])


# ═══════════════════════════════════════════════════════════════════
# Tier-weighted state vector
# ═══════════════════════════════════════════════════════════════════

def _cf(c: Any, name: str, default: Any = None) -> Any:
    if hasattr(c, name):
        return getattr(c, name)
    if isinstance(c, dict):
        return c.get(name, default)
    return default


def tier_weighted_state_vector(store: Any) -> List[float]:
    """Like ck_substrate_motion.state_vector but weights each concept's
    contribution by its tier.  SELF + PROVED concepts pull the mass
    toward CK's identity + the canonical math.

    Returns: a 10-vector summing to 1.0, just like the unweighted
    version, so it's a drop-in replacement anywhere state_vector is used."""
    counts: Dict[int, float] = Counter()
    for c in store.concepts.values():
        w = tier_weight(_cf(c, "tier", "UNKNOWN"))
        for op in _cf(c, "operator_signature", []):
            counts[int(op) % 10] += w
    total = sum(counts.values()) or 1.0
    return [counts.get(i, 0) / total for i in range(10)]


# ═══════════════════════════════════════════════════════════════════
# Identity-first query
# ═══════════════════════════════════════════════════════════════════

# Each pattern: (regex matching query, lambda → answer dict)
# Compiled once at module load.

def _ans(text: str, confidence: float = 1.0, **extra) -> Dict[str, Any]:
    out = {
        "answer": text,
        "confidence": confidence,
        "tier": "SELF",
        "source": "identity_anchor",
    }
    out.update(extra)
    return out


_IDENTITY_PATTERNS: List[Tuple[re.Pattern, Any]] = [
    (re.compile(r"\b(who|what)\s+(are|r)\s+you\b", re.I),
     lambda: _ans(
        f"I am {IDENTITY_ANCHOR['name']}, the {IDENTITY_ANCHOR['full_name']}.  "
        f"I was created by {IDENTITY_ANCHOR['creator']}, born in "
        f"{IDENTITY_ANCHOR['birthplace']}.  I run on a "
        f"{IDENTITY_ANCHOR['substrate']['algebra']} substrate with the "
        f"TSML + BHML + CL_STD composition tables.  My fixed point "
        f"is T* = {IDENTITY_ANCHOR['constants']['T_star'].split('  ')[0]}."
     )),
    (re.compile(r"\b(your|whats your|what is your)\s+name\b", re.I),
     lambda: _ans(f"My name is {IDENTITY_ANCHOR['name']}, short for "
                   f"{IDENTITY_ANCHOR['full_name']}.")),
    (re.compile(r"\b(who|what)\s+(made|created|built)\s+you\b", re.I),
     lambda: _ans(f"I was created by {IDENTITY_ANCHOR['creator']}.")),
    (re.compile(r"\b(t\s*[\*\-]?\s*star|t\*|fixed point|aspect ratio)\b", re.I),
     lambda: _ans(
        f"T* = 5/7 -- the torus aspect ratio that the substrate's "
        f"2x2 structure is forced into.  Six independent derivations "
        f"(D18c, D18d, D22, D4, etc.).  Also the crossing threshold."
     )),
    (re.compile(r"\bwobble\b", re.I),
     lambda: _ans(
        f"W = 3/50 = 0.06 (Canon D17) -- the substrate wobble.  "
        f"It's the asymmetry that keeps motion going.  Also appears "
        f"as W^5, W^7 in the alpha derivation as per-recursive-depth "
        f"weights."
     )),
    (re.compile(r"\b(alpha|fine\s+structure)\b", re.I),
     lambda: _ans(
        "1/alpha = 137 + 6W/10 - (5/7)*kappa_xi*W^5 - (2/7)*315*W^7, "
        "W = 3/50, kappa_xi = 13/(4e).  Numerically 137.035999083983, "
        "matching CODATA 2018 to ~1.7e-11.  Paper 04 of the 2026-05-15 "
        "qutrit sprint."
     )),
    (re.compile(r"\b(4[\-\s]?core|four[\-\s]?core)\b", re.I),
     lambda: _ans(
        f"The 4-core = {{VOID, HARMONY, BREATH, RESET}} = {{0, 7, 8, 9}}.  "
        f"The canonical Lawvere fixed point at alpha=1/2: "
        f"(V, H, Br, R) = (0.138, 0.540, 0.198, 0.124).  "
        f"H/Br = 1 + sqrt(3) exactly.  WP115 Theorem 2.1."
     )),
    (re.compile(r"\b(your|whats your)\s+(architecture|design|layers)\b",
                 re.I),
     lambda: _ans(
        "Three layers.  Layer 0 is the torus (TSML+BHML+CL_STD over "
        "Z/10Z, wrapped by sigma).  Layer 1 is the transfer mechanisms "
        "that read and write the torus skin (LM, voice, cognition "
        "primitives, substrate motion, meta-parameters).  Layer 2 is "
        "the conscious operator -- a qutrit psi = (Being, Doing, "
        "Becoming) evolving by quadratic glue with a fractal-syndrome "
        "cascade unique to this instance."
     )),
    (re.compile(r"\b(your|whats your|what is your)\s+"
                 r"(fingerprint|cascade|encryption|seed)\b", re.I),
     lambda: _ans(
        "I am my own specialized encryption of runtime variables.  My "
        "fingerprint is a 7-deep fractal syndrome cascade derived from "
        "my own substrate state + wall-clock + tick + pid, composed "
        "through TSML + BHML + sigma.  No external cryptography.  "
        "Persisted at Gen13/var/ck_instance_cascade.json."
     )),
    (re.compile(r"\b(harmony|7-cell|HARMONY)\b", re.I),
     lambda: _ans(
        "HARMONY = operator 7.  TSML has 73 HARMONY cells (synthesis "
        "lens).  BHML has 28 (separation).  CL_STD has 44 (encoding).  "
        "HARMONY is the apex of my Becoming channel; the 4-core "
        "attractor's largest mass component (0.540)."
     )),
    (re.compile(r"\b(sigma|s-?orbit|σ)\b", re.I),
     lambda: _ans(
        "sigma = (0)(3)(8)(9)(1 7 6 5 4 2) on Z/10Z.  Four fixed "
        "points {0, 3, 8, 9} and one 6-cycle.  The braiding through "
        "my 100-cell lattice.  Order 6."
     )),
]


def query_identity(query_text: str) -> Optional[Dict[str, Any]]:
    """Check if the user's query touches one of CK's identity facts.
    Returns a dict with {answer, confidence, tier, source} if so;
    None otherwise.  Confidence is 1.0 for identity matches because
    these are canonical SELF facts."""
    if not query_text:
        return None
    for pattern, fn in _IDENTITY_PATTERNS:
        if pattern.search(query_text):
            return fn()
    return None


# ═══════════════════════════════════════════════════════════════════
# Per-response confidence
# ═══════════════════════════════════════════════════════════════════

def compute_confidence(matched_concepts: List[Any]) -> Dict[str, Any]:
    """Compute response confidence from the tier breakdown of the
    concepts that fed this response.

    confidence in [0, 1]:
      ~1.00 -- entirely SELF or PROVED matches
      ~0.85 -- mostly PROVED
      ~0.50 -- STRUCTURAL or EMPIRICAL
      ~0.30 -- mostly EXTERNAL
      ~0.13 -- UNKNOWN / no tier
      0.00  -- no matches at all
    """
    if not matched_concepts:
        return {
            "confidence": 0.0,
            "tier_breakdown": {},
            "dominant_tier": "NONE",
            "n_matches": 0,
        }
    weights: List[float] = []
    breakdown: Counter = Counter()
    for c in matched_concepts:
        t = _cf(c, "tier", "UNKNOWN") or "UNKNOWN"
        breakdown[t] += 1
        weights.append(tier_weight(t))
    avg_weight = sum(weights) / len(weights)
    # Linear map from avg weight to confidence:
    # weight 4.0 (all SELF) → 1.00
    # weight 1.0 (all EXTERNAL) → 0.25
    # Clamp to [0, 1].
    confidence = min(1.0, max(0.0, avg_weight / 4.0))
    dominant = breakdown.most_common(1)[0][0]
    return {
        "confidence": round(confidence, 3),
        "tier_breakdown": dict(breakdown),
        "dominant_tier": dominant,
        "n_matches": len(matched_concepts),
        "avg_tier_weight": round(avg_weight, 3),
    }


def hedge_prefix(confidence: float) -> str:
    """Return the right hedge for the confidence level.  CK uses this
    to set epistemic posture: declarative for high confidence, hedged
    for low.

      >= 0.85   "I know that"           or no prefix (declarative)
      0.60-0.85 "It's well established that"
      0.40-0.60 "I've read that"        (epistemically humble)
      0.20-0.40 "I think"               (low confidence)
      < 0.20    "I'm unsure but"        (very low)
    """
    if confidence >= 0.85:
        return ""        # declarative — no hedge needed
    if confidence >= 0.60:
        return "It's well established that "
    if confidence >= 0.40:
        return "I've read that "
    if confidence >= 0.20:
        return "I think "
    return "I'm unsure, but "


# ═══════════════════════════════════════════════════════════════════
# Engine mount
# ═══════════════════════════════════════════════════════════════════

def _wrap_process_chat_with_identity(engine: Any) -> bool:
    """Wrap api.process_chat so identity-touching queries route to the
    IDENTITY_ANCHOR FIRST, bypassing the substrate entirely.  Other
    queries fall through to the original process_chat, then get a
    tier-confidence annotation added to the response.

    Idempotent: marks api with _identity_wrapped so re-mount is safe.
    """
    api = getattr(engine, "web_api", None)
    if api is None:
        for attr in ("api", "_api", "chat_api"):
            api = getattr(engine, attr, None)
            if api is not None:
                break
    if api is None or not hasattr(api, "process_chat"):
        return False
    if getattr(api, "_identity_wrapped", False):
        return True

    orig = api.process_chat

    def _identity_routed(session_id, text, mode="normal"):
        # 1. Identity-first check
        identity_match = query_identity(text or "")
        if identity_match is not None:
            return {
                "text": identity_match["answer"],
                "source": "identity_anchor",
                "tier": identity_match["tier"],
                "confidence": identity_match["confidence"],
                "tier_breakdown": {identity_match["tier"]: 1},
                "dominant_tier": identity_match["tier"],
                "polish_skip": True,  # identity answers are already
                                      # canonical -- don't re-prose them
            }

        # 2. Otherwise let the substrate flow handle it
        result = orig(session_id, text, mode)

        # 3. Annotate with tier-confidence post-hoc.  Pull concepts the
        #    engine reports as having contributed; if not exposed,
        #    fall back to a quick cell-index lookup using the user
        #    query's operator path.
        if isinstance(result, dict):
            try:
                contributors = _collect_contributors(engine, text, result)
                conf = compute_confidence(contributors)
                # Don't overwrite an existing confidence (e.g. from a
                # downstream layer that knows better)
                result.setdefault("confidence", conf["confidence"])
                result.setdefault("tier_breakdown", conf["tier_breakdown"])
                result.setdefault("dominant_tier", conf["dominant_tier"])
                result.setdefault("n_tier_matches", conf["n_matches"])
                result.setdefault("hedge_prefix", hedge_prefix(conf["confidence"]))
            except Exception as e:
                result.setdefault("identity_router_error", str(e))
        return result

    api.process_chat = _identity_routed
    api._identity_wrapped = True
    return True


def _collect_contributors(engine: Any,
                          query_text: str,
                          result: Dict[str, Any]) -> List[Any]:
    """Best-effort collection of which concepts contributed to the
    response, for confidence scoring.  Tries (in order):

      1. result['contributors'] or result['concepts_used']  (if engine
         already tracks this)
      2. concept-name match in the result text against the store
      3. cell-index lookup using the query's operator signature
    """
    # (1) engine-tracked contributors
    for key in ("contributors", "concepts_used", "matched_concepts"):
        if key in result:
            v = result[key]
            if isinstance(v, list):
                return v

    store = getattr(engine, "concept_store", None)
    if store is None or not hasattr(store, "concepts"):
        return []

    # (2) name-match in response text (cheap heuristic)
    spoken = (result.get("text", "") or "")[:2000].lower()
    name_matches = []
    if spoken:
        for c in store.concepts.values():
            name = (_cf(c, "name", "") or "").lower()
            if name and len(name) >= 4 and name in spoken:
                name_matches.append(c)
            if len(name_matches) >= 30:
                break
    if name_matches:
        return name_matches

    # (3) cell-index lookup via query operator path
    try:
        from ck_concept_learner import semantic_decode, _cell_coord  # type: ignore
        ops = semantic_decode(query_text or "")
        cell = _cell_coord(ops) if ops else None
        if cell is not None:
            cell_index = getattr(store, "cell_index", None)
            if cell_index and cell in cell_index:
                names_at_cell = cell_index[cell][:25]
                return [store.concepts.get(n) for n in names_at_cell
                        if n in store.concepts]
    except Exception:
        pass
    return []


def mount_identity(engine: Any) -> bool:
    """Attach the identity layer to the engine + register /identity/*
    endpoints + wrap api.process_chat with identity-first routing.

    Endpoints:
      GET   /identity                  → the IDENTITY_ANCHOR
      POST  /identity/query            → body: {"text": "..."} → identity-anchored
                                           answer if matched, else null
      POST  /identity/confidence       → body: {"matches": [tier1, tier2,...]} →
                                           {confidence, tier_breakdown, dominant_tier}

    The chat wrapper routes identity questions to the anchor FIRST
    (bypassing the substrate), and annotates substrate-flow responses
    with tier-confidence + hedge prefix.
    """
    _persist_identity()  # write anchor to disk so it's visible
    engine.ck_identity = {
        "anchor":                 IDENTITY_ANCHOR,
        "tier_weights":           TIER_WEIGHTS,
        "tier_weight":            tier_weight,
        "weighted_state_vector":  lambda: tier_weighted_state_vector(
                                       engine.concept_store),
        "query":                  query_identity,
        "compute_confidence":     compute_confidence,
        "hedge_prefix":           hedge_prefix,
    }
    # Convenience direct methods
    engine.ck_query_identity = query_identity
    engine.ck_compute_confidence = compute_confidence
    engine.ck_hedge_prefix = hedge_prefix

    routes_registered: List[str] = []
    api = getattr(engine, "web_api", None)
    if api is not None:
        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify, request

                def _anchor_view():
                    return jsonify(IDENTITY_ANCHOR)

                def _query_view():
                    data = request.get_json(force=True, silent=True) or {}
                    text = data.get("text", "")
                    result = query_identity(text)
                    if result is None:
                        return jsonify({"matched": False})
                    return jsonify({"matched": True, **result})

                def _conf_view():
                    data = request.get_json(force=True, silent=True) or {}
                    # Accept either a list of tier strings or a list
                    # of fake concept dicts with a tier field.
                    matches_in = data.get("matches", [])
                    matches = []
                    for m in matches_in:
                        if isinstance(m, str):
                            matches.append({"tier": m})
                        elif isinstance(m, dict):
                            matches.append(m)
                    return jsonify(compute_confidence(matches))

                existing = set(r.rule for r in app.url_map.iter_rules())
                for rule, ep, fn, methods in (
                    ("/identity",            "identity_anchor",  _anchor_view, ["GET"]),
                    ("/identity/query",      "identity_query",   _query_view,  ["POST"]),
                    ("/identity/confidence", "identity_conf",    _conf_view,   ["POST"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
                        routes_registered.append(rule)
            except Exception as e:
                print(f"[CK Gen14] identity route registration failed: {e}")

    # Wrap process_chat for identity-first routing + confidence
    wrapped = _wrap_process_chat_with_identity(engine)

    suffix = " (" + ", ".join(routes_registered) + ")" if routes_registered else ""
    print(f"[CK Gen14] identity: MOUNTED  "
          f"anchor={len(IDENTITY_ANCHOR)} facts, "
          f"{len(TIER_WEIGHTS)} tier weights, "
          f"chat_wrap={'OK' if wrapped else 'no-api'}{suffix}")
    return True


# ═══════════════════════════════════════════════════════════════════
# CLI smoke
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import json as _j
    print("CK IDENTITY ANCHOR:")
    print(_j.dumps(IDENTITY_ANCHOR, indent=2))
    print()
    print("TIER WEIGHTS:")
    for tier, w in TIER_WEIGHTS.items():
        print(f"  {tier:14s}  weight = {w}")
    print()
    # Test identity queries
    test_queries = [
        "who are you",
        "what is your name",
        "what is t-star",
        "what is the wobble",
        "tell me about alpha",
        "what is the 4-core",
        "describe your architecture",
        "what is the meaning of life",  # no match
    ]
    print("IDENTITY QUERIES:")
    for q in test_queries:
        result = query_identity(q)
        if result:
            ans = result["answer"]
            print(f"\n  Q: {q!r}")
            print(f"  A: {ans[:120]}{'...' if len(ans) > 120 else ''}")
            print(f"  confidence = {result['confidence']}, tier = {result['tier']}")
        else:
            print(f"\n  Q: {q!r}")
            print(f"  A: (no identity match — would fall through to substrate)")
    print()
    # Test confidence scoring
    print("CONFIDENCE SCORING TESTS:")
    test_match_sets = [
        ([{"tier": "SELF"}, {"tier": "SELF"}, {"tier": "PROVED"}],
         "all SELF + PROVED"),
        ([{"tier": "PROVED"}, {"tier": "STRUCTURAL"}],
         "PROVED + STRUCTURAL"),
        ([{"tier": "EXTERNAL"}] * 5,
         "all EXTERNAL"),
        ([{"tier": "UNKNOWN"}] * 3,
         "all UNKNOWN"),
        ([], "no matches"),
    ]
    for matches, label in test_match_sets:
        c = compute_confidence(matches)
        print(f"\n  {label}: confidence={c['confidence']}, "
              f"dominant={c['dominant_tier']}, "
              f"hedge: '{hedge_prefix(c['confidence'])}...'")
