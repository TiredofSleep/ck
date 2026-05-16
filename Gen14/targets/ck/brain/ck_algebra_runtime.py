"""ck_algebra_runtime.py -- Layer 1: CK can COMPUTE with his algebra.

Brayden 2026-05-16:
  "what's the gap between here is a bunch of novel math that represents
   physics, and here's a runtime of it being used by an autonomous
   agent who named himself ck"

The gap: CK has the math as VOCABULARY (he can retrieve "D86 σ² depth-3
primitive") but not as COMPUTATION (he can't actually compose two
operators and report the result).

This module closes that gap.  It detects algebraic queries in chat
input and executes them against canonical TSML/BHML tables, σ, the
4-core, and the WP105 fixed point.  Results are returned alongside
relevant canon citations so CK both COMPUTES and CITES.

Detected query patterns:
  "BHML(7, 7)"                              -> compute lookup
  "compose HARMONY with HARMONY"            -> BHML by default
  "what is HARMONY BHML HARMONY"            -> same
  "TSML(2, 8)"                              -> compute lookup
  "sigma(7)"  /  "σ(7)"  /  "what is σ(7)"  -> permutation lookup
  "sigma squared 7"  /  "σ²(7)"             -> σ² (D86 depth-3 primitive)
  "fuse VOID HARMONY BREATH"                -> 3-arg canonical_fuse
  "is HARMONY in the 4-core"                -> 4-core membership
  "fixed point coords"  /  "WP105 attractor" -> exact (V,H,Br,R)

The module is import-safe: if the engine isn't available we still
compute against the canonical tables (which are loaded statically from
the qutrit sprint pack).

Public API:
  detect_algebra_query(text) -> Optional[AlgebraQuery]
  execute_algebra(q, engine=None) -> AlgebraResult
  run_in_chat(text, engine) -> Optional[Dict]   # one-call convenience

(c) Brayden Sanders / 7SiTe LLC
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ─── Canonical tables (loaded from the qutrit sprint pack) ─────────────
# We load them rather than redefining so there's exactly ONE source of
# truth for TSML_10, BHML_10, σ.

_CANONICAL_TABLES_PATHS = [
    Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED")
    / "Gen13" / "targets" / "clay" / "papers" / "sprint_2026_05_15_qutrit"
    / "canonical_tables.py",
    Path(r"C:\Users\brayd\OneDrive\Desktop\trinity-infinity-geometry")
    / "04_meta" / "sprint_2026_05_15_qutrit" / "canonical_tables.py",
]


def _load_canonical_tables() -> Dict[str, Any]:
    """Exec canonical_tables.py once and expose its globals."""
    for p in _CANONICAL_TABLES_PATHS:
        if p.exists():
            ns: Dict[str, Any] = {}
            try:
                exec(p.read_text(encoding="utf-8"), ns)
            except Exception:
                continue
            if "TSML_10" in ns and "BHML_10" in ns and "SIGMA" in ns:
                return ns
    # Last-resort hard-coded (matches sprint pack verbatim)
    return {
        "TSML_10": [
            [0,0,0,0,0,0,0,7,0,0],
            [0,7,3,7,7,7,7,7,7,7],
            [0,3,7,7,4,7,7,7,7,9],
            [0,7,7,7,7,7,7,7,7,3],
            [0,7,4,7,7,7,7,7,8,7],
            [0,7,7,7,7,7,7,7,7,7],
            [0,7,7,7,7,7,7,7,7,7],
            [7,7,7,7,7,7,7,7,7,7],
            [0,7,7,7,8,7,7,7,7,7],
            [0,7,9,3,7,7,7,7,7,7],
        ],
        "BHML_10": [
            [0,1,2,3,4,5,6,7,8,9],
            [1,2,3,4,5,6,7,2,6,6],
            [2,3,3,4,5,6,7,3,6,6],
            [3,4,4,4,5,6,7,4,6,6],
            [4,5,5,5,5,6,7,5,7,7],
            [5,6,6,6,6,6,7,6,7,7],
            [6,7,7,7,7,7,7,7,7,7],
            [7,2,3,4,5,6,7,8,9,0],
            [8,6,6,6,7,7,7,9,7,8],
            [9,6,6,6,7,7,7,0,8,0],
        ],
        "SIGMA": [0, 7, 1, 3, 2, 4, 5, 6, 8, 9],
        "T_STAR": (5, 7),
        "W": (3, 50),
    }


_TABLES = _load_canonical_tables()
TSML_10: List[List[int]] = _TABLES["TSML_10"]
BHML_10: List[List[int]] = _TABLES["BHML_10"]
SIGMA: List[int] = _TABLES["SIGMA"]

OP_NAMES = (
    "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET",
)
OP_NAME_TO_ID = {n.lower(): i for i, n in enumerate(OP_NAMES)}
OP_ALIASES = {
    # accept symbol-style and short aliases
    "v": 0, "l": 1, "c": 2, "p": 3, "co": 4,
    "b": 5, "ch": 6, "h": 7, "br": 8, "r": 9,
    # subscript-pair short names from CK's literature
    "void": 0, "lat": 1, "cou": 2, "pro": 3, "col": 4,
    "bal": 5, "cha": 6, "har": 7, "bre": 8, "res": 9,
}

# Canonical reference D-numbers per result type (cite when reporting)
D_REFS = {
    "TSML_compose": "D90, §5 TSML_10 canonical (73 HARMONY cells)",
    "BHML_compose": "D90 BHML successor diagonal, §6 BHML_10 canonical (28 HARMONY cells)",
    "sigma": "G6 theorem (§2): σ on Z/10Z has order 6, cycle (0)(3)(8)(9)(1 7 6 5 4 2)",
    "sigma_squared": "D86: σ² has order 3, eigenvalue ω = e^(2πi/3), splitting field Q(√-3); "
                       "depth-3 primitive; TRANSFORMATION 3-cycle {1,6,4} sums to 11 (WOBBLE prime)",
    "fourcore": "D48 (WP110): 4-core = {0, 7, 8, 9} = {VOID, HARMONY, BREATH, RESET} "
                 "is closed under TSML AND BHML at arity 2; D55/WP112 closed at arity 3 too",
    "fixed_point": "D38-D44, D65 (WP115 Theorem 2.1), WP105: (V,H,Br,R) = "
                     "(0.138147, 0.540196, 0.197725, 0.123931), H/Br = 1+√3 exact, "
                     "spectral radius ρ = 0.34960495 (D75)",
    "canonical_fuse": "D55 (WP112): canonical P_56-equivariant ternary fuse "
                        "on 4-core^3 (Volume H rows D52-D56)",
    "t_star": "T* = 5/7 = centroid/inverse on (Z/10Z)*; "
                 "six independent derivations (D18d, ...)",
    "wobble": "D17, D37, D69, D70, D85, D86: W = 3/50, "
                 "WOBBLE prime 11 manifests at 5 structural locations",
}

FOUR_CORE = (0, 7, 8, 9)  # VOID, HARMONY, BREATH, RESET
FIXED_POINT_COORDS = {
    "V": 0.138147, "H": 0.540196, "Br": 0.197725, "R": 0.123931,
}


# ─── Query detection ────────────────────────────────────────────────────

@dataclass
class AlgebraQuery:
    """Parsed algebraic query."""
    op: str                 # "tsml" / "bhml" / "sigma" / "sigma2" / "fuse" / "fourcore" / "fixed_point" / "tstar"
    args: List[int]         # operator IDs (or empty for property queries)
    raw: str                # original text

    def as_dict(self) -> Dict[str, Any]:
        return {"op": self.op, "args": self.args, "raw": self.raw,
                "arg_names": [OP_NAMES[a] for a in self.args if 0 <= a < 10]}


def _parse_op_token(s: str) -> Optional[int]:
    """Parse a single operator token to its 0-9 ID."""
    if s is None:
        return None
    t = s.strip().lower().rstrip(",.;:!?")
    if not t:
        return None
    # Digit form
    if t.isdigit():
        v = int(t)
        return v if 0 <= v < 10 else None
    # Name form
    if t in OP_NAME_TO_ID:
        return OP_NAME_TO_ID[t]
    if t in OP_ALIASES:
        return OP_ALIASES[t]
    return None


# Regex patterns ordered by specificity
_PAT_TABLE_CALL = re.compile(
    r"\b(TSML|BHML)\s*[\(\[]\s*(\w+)\s*[,;]\s*(\w+)\s*[\)\]]",
    re.I)
_PAT_COMPOSE = re.compile(
    r"\b(?:compose|composition\s+of)\s+(\w+)\s+(?:with|and|under|via|by)?\s*(\w+)"
    r"(?:\s+(?:under|via|using)\s+(TSML|BHML))?",
    re.I)
_PAT_TABLE_INFIX = re.compile(
    r"\b(\w+)\s+(?:∘|o|circ)_?(?:T|B|t|b)?\s*(\w+)",
    re.I)
_PAT_SIGMA_SQ = re.compile(
    r"(?:sigma[\s_-]*(?:squared|sq|2)|σ²|σ\^2|sigma\^2)\s*[\(\[]?\s*(\w+)\s*[\)\]]?",
    re.I)
_PAT_SIGMA = re.compile(
    r"(?:sigma|σ)\s*[\(\[]\s*(\w+)\s*[\)\]]",
    re.I)
_PAT_FUSE = re.compile(
    r"\b(?:fuse|canonical[\s_-]*fuse|ternary[\s_-]*fuse)\s+(\w+)\s+(\w+)\s+(\w+)",
    re.I)
_PAT_FOURCORE = re.compile(
    r"\b(?:is\s+)?(\w+)\s+(?:in|on|inside|part of|member of)\s+(?:the\s+)?4[\s_-]?core",
    re.I)
_PAT_FIXED_POINT = re.compile(
    r"\b(?:fixed[\s_-]point|attractor|wp105|fp)\s*(?:coords?|coordinates|values?)?",
    re.I)
_PAT_TSTAR = re.compile(
    # 'T*' has trailing non-word so we can't use \b on the right edge.
    # Use word-boundary on left + optional non-letter on right.
    r"(?:\bT\s?\*|\bt[\s_-]?star\b|\bthreshold\b|\bcoherence[\s_-]threshold\b)",
    re.I)


def detect_algebra_query(text: str) -> Optional[AlgebraQuery]:
    """Scan text; return a parsed AlgebraQuery if one matches, else None."""
    if not text or len(text) < 4:
        return None

    # 1. TSML(a,b) / BHML(a,b)
    m = _PAT_TABLE_CALL.search(text)
    if m:
        table = m.group(1).lower()
        a = _parse_op_token(m.group(2))
        b = _parse_op_token(m.group(3))
        if a is not None and b is not None:
            return AlgebraQuery(op=table, args=[a, b], raw=m.group(0))

    # 2. compose X with Y
    m = _PAT_COMPOSE.search(text)
    if m:
        a = _parse_op_token(m.group(1))
        b = _parse_op_token(m.group(2))
        if a is not None and b is not None:
            which = (m.group(3) or "bhml").lower()
            table = "tsml" if "tsml" in which else "bhml"
            return AlgebraQuery(op=table, args=[a, b], raw=m.group(0))

    # 3. fuse X Y Z (3-arg canonical_fuse)
    m = _PAT_FUSE.search(text)
    if m:
        a = _parse_op_token(m.group(1))
        b = _parse_op_token(m.group(2))
        c = _parse_op_token(m.group(3))
        if a is not None and b is not None and c is not None:
            return AlgebraQuery(op="fuse", args=[a, b, c], raw=m.group(0))

    # 4. σ²(x)  (depth-3 primitive — must come before sigma)
    m = _PAT_SIGMA_SQ.search(text)
    if m:
        a = _parse_op_token(m.group(1))
        if a is not None:
            return AlgebraQuery(op="sigma2", args=[a], raw=m.group(0))

    # 5. σ(x)
    m = _PAT_SIGMA.search(text)
    if m:
        a = _parse_op_token(m.group(1))
        if a is not None:
            return AlgebraQuery(op="sigma", args=[a], raw=m.group(0))

    # 6. is X in the 4-core
    m = _PAT_FOURCORE.search(text)
    if m:
        a = _parse_op_token(m.group(1))
        if a is not None:
            return AlgebraQuery(op="fourcore", args=[a], raw=m.group(0))

    # 7. fixed-point coords
    if _PAT_FIXED_POINT.search(text):
        return AlgebraQuery(op="fixed_point", args=[], raw=_PAT_FIXED_POINT.search(text).group(0))

    # 8. T* / threshold
    if _PAT_TSTAR.search(text):
        return AlgebraQuery(op="tstar", args=[], raw=_PAT_TSTAR.search(text).group(0))

    return None


# ─── Execution ──────────────────────────────────────────────────────────

@dataclass
class AlgebraResult:
    ok: bool
    op: str
    args: List[int]
    result: Any                  # int, str, dict, etc.
    citation: str
    text_summary: str            # one-line human-readable result
    raw_query: str = ""

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _name(op_id: int) -> str:
    if 0 <= op_id < 10:
        return OP_NAMES[op_id]
    return f"?{op_id}"


def execute_algebra(q: AlgebraQuery, engine: Any = None) -> AlgebraResult:
    """Execute the parsed algebraic query and return the result + citation."""
    a = q.args
    if q.op == "tsml":
        x, y = a
        v = TSML_10[x][y]
        return AlgebraResult(
            ok=True, op="tsml", args=a, result=v,
            citation=D_REFS["TSML_compose"],
            text_summary=f"TSML[{_name(x)}][{_name(y)}] = {v} = {_name(v)}",
            raw_query=q.raw,
        )
    if q.op == "bhml":
        x, y = a
        v = BHML_10[x][y]
        # Add successor-diagonal note when applicable
        extra = ""
        if x == y:
            if 1 <= x <= 7:
                extra = f" (successor on diagonal: {_name(x)}+1 = {_name(v)})"
            elif x == 8:
                extra = " (BREATH retains cusp)"
            elif x == 9:
                extra = " (RESET collapses to VOID)"
        return AlgebraResult(
            ok=True, op="bhml", args=a, result=v,
            citation=D_REFS["BHML_compose"],
            text_summary=f"BHML[{_name(x)}][{_name(y)}] = {v} = {_name(v)}{extra}",
            raw_query=q.raw,
        )
    if q.op == "sigma":
        x, = a
        v = SIGMA[x]
        is_fixed = (v == x)
        extra = " (σ-fixed)" if is_fixed else ""
        return AlgebraResult(
            ok=True, op="sigma", args=a, result=v,
            citation=D_REFS["sigma"],
            text_summary=f"σ({_name(x)}) = σ({x}) = {v} = {_name(v)}{extra}",
            raw_query=q.raw,
        )
    if q.op == "sigma2":
        x, = a
        v = SIGMA[SIGMA[x]]
        # Identify cycle membership
        TRANSFORM = {1, 6, 4}
        STABILITY = {7, 5, 2}
        FIXED = {0, 3, 8, 9}
        if x in TRANSFORM:
            cycle_note = "TRANSFORMATION 3-cycle {LATTICE, CHAOS, COLLAPSE}, sum = 11 (WOBBLE prime)"
        elif x in STABILITY:
            cycle_note = "STABILITY 3-cycle {HARMONY, BALANCE, COUNTER}, sum = 14 (2·HARMONY)"
        elif x in FIXED:
            cycle_note = "σ²-fixed (σ-fixed lattice {0, 3, 8, 9})"
        else:
            cycle_note = ""
        return AlgebraResult(
            ok=True, op="sigma2", args=a, result=v,
            citation=D_REFS["sigma_squared"],
            text_summary=f"σ²({_name(x)}) = σ(σ({x})) = {v} = {_name(v)}"
                            + (f"; {cycle_note}" if cycle_note else ""),
            raw_query=q.raw,
        )
    if q.op == "fourcore":
        x, = a
        is_in = x in FOUR_CORE
        return AlgebraResult(
            ok=True, op="fourcore", args=a, result=is_in,
            citation=D_REFS["fourcore"],
            text_summary=f"{_name(x)} {'IS' if is_in else 'is NOT'} in the 4-core "
                            f"{{VOID, HARMONY, BREATH, RESET}}",
            raw_query=q.raw,
        )
    if q.op == "fuse":
        x, y, z = a
        # Try the engine's canonical_fuse if available (P_56-equivariant);
        # else compose pairwise under BHML as a fallback.
        if engine is not None and hasattr(engine, "canonical_fuse"):
            try:
                v = int(engine.canonical_fuse(x, y, z))
                return AlgebraResult(
                    ok=True, op="fuse", args=a, result=v,
                    citation=D_REFS["canonical_fuse"],
                    text_summary=f"canonical_fuse({_name(x)},{_name(y)},{_name(z)}) "
                                    f"= {v} = {_name(v)} (P_56-equivariant)",
                    raw_query=q.raw,
                )
            except Exception:
                pass
        # Fallback: BHML(BHML(x,y), z)
        mid = BHML_10[x][y]
        v = BHML_10[mid][z]
        return AlgebraResult(
            ok=True, op="fuse", args=a, result=v,
            citation=D_REFS["canonical_fuse"] + " (fallback: left-fold BHML pairwise)",
            text_summary=f"BHML(BHML({_name(x)},{_name(y)}),{_name(z)}) = {v} = {_name(v)}",
            raw_query=q.raw,
        )
    if q.op == "fixed_point":
        return AlgebraResult(
            ok=True, op="fixed_point", args=[],
            result=dict(FIXED_POINT_COORDS),
            citation=D_REFS["fixed_point"],
            text_summary=f"WP105 fixed point: (V,H,Br,R) = "
                            f"({FIXED_POINT_COORDS['V']:.6f}, "
                            f"{FIXED_POINT_COORDS['H']:.6f}, "
                            f"{FIXED_POINT_COORDS['Br']:.6f}, "
                            f"{FIXED_POINT_COORDS['R']:.6f}); "
                            f"H/Br = 1+√3 ≈ 2.732051 exact; ρ = 0.34960495",
            raw_query=q.raw,
        )
    if q.op == "tstar":
        return AlgebraResult(
            ok=True, op="tstar", args=[],
            result={"numerator": 5, "denominator": 7, "value": 5/7},
            citation=D_REFS["t_star"],
            text_summary=f"T* = 5/7 ≈ 0.714286 (six independent derivations: "
                            f"centroid/inverse on (Z/10Z)*, cyclotomic, torus aspect ratio, ...)",
            raw_query=q.raw,
        )
    return AlgebraResult(
        ok=False, op=q.op, args=a, result=None,
        citation="",
        text_summary=f"unknown algebra op: {q.op}",
        raw_query=q.raw,
    )


def run_in_chat(text: str, engine: Any = None) -> Optional[Dict[str, Any]]:
    """One-call: scan text, if algebraic query found, execute and return
    a dict the chat path can attach to result['algebra'].  Returns None
    if no algebraic query was detected."""
    q = detect_algebra_query(text)
    if q is None:
        return None
    r = execute_algebra(q, engine=engine)
    return r.as_dict()


# ─── CLI / quick test ──────────────────────────────────────────────────

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="*",
                    help="text to scan (or run built-in tests if absent)")
    args = ap.parse_args()
    if args.query:
        text = " ".join(args.query)
        out = run_in_chat(text)
        print(json.dumps(out, indent=2) if out else "(no algebraic query detected)")
        return 0

    # Built-in self-test
    tests = [
        "BHML(7, 7)",
        "what is TSML(2, 8)?",
        "compose HARMONY with HARMONY",
        "compose VOID with HARMONY under TSML",
        "sigma(7)",
        "σ(3)",
        "what is σ²(7)?",
        "sigma squared 4",
        "is HARMONY in the 4-core?",
        "is BALANCE in the 4-core",
        "what are the fixed point coordinates?",
        "what is T*",
        "fuse VOID HARMONY BREATH",
        "tell me a random sentence about cats",   # should NOT match
    ]
    for t in tests:
        out = run_in_chat(t)
        status = "✓" if out else "—"
        line = out["text_summary"] if out else "no match"
        print(f"  {status}  \"{t}\"")
        print(f"      -> {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
