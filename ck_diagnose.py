# Copyright (c) 2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
"""
ck_diagnose.py -- One-command paradox-classifier scan over any input.

CK self-audit ask #1 (per Grok-CK dialogue, 2026-04-17):

    "Extend ck_read_self.py to include a quick paradox classifier scan on
    any input structure (2x2 quadrant balance, corridor leakage risk,
    sigma non-associativity fraction). Make it one command:
    `ck diagnose <object>`."

Implemented as a standalone module to keep ck_read_self.py untouched.
Importable as a function or runnable as a CLI.

Usage:
    python ck_diagnose.py path/to/file.txt
    python ck_diagnose.py path/to/file.json
    python ck_diagnose.py --raw "some inline text"
    python ck_diagnose.py path/to/matrix.csv --shape 10x10

Output: one JSON blob with three diagnostics, each scored against T* = 5/7.

    {
      "object": "...",
      "diagnostics": {
        "quadrant_balance":          { "score": 0..1, "verdict": "..." },
        "corridor_leakage":          { "score": 0..1, "verdict": "..." },
        "sigma_non_associativity":   { "score": 0..1, "verdict": "..." }
      },
      "overall_coherence": 0..1,
      "above_threshold": bool,                # >= 5/7
      "T_star": 0.7142857142857143
    }

Diagnostic interpretation (per TIG / 2x2 framework):

    quadrant_balance        -- For a 2x2 view of the input, are all four
                               quadrants populated above floor? Imbalance
                               flags a flatness-violating mass concentration.

    corridor_leakage        -- For a sigma-classified partition, what
                               fraction of mass leaks across an expected
                               disjoint corridor (e.g., MAX vs ADD seam)?

    sigma_non_associativity -- For ternary samples (a, b, c) projected
                               into Z/10Z, fraction violating
                               (a sigma b) sigma c == a sigma (b sigma c).
                               Pure structural test of the mod-10 sigma.

Sovereignty rule: no external models, pure local primitives.
"""

import json
import os
import sys
import argparse
import hashlib
from collections import Counter
from typing import Any, Dict, List, Tuple

T_STAR = 5.0 / 7.0


# ============================================================
# Input loading
# ============================================================

def load_input(path: str = None, raw: str = None) -> Tuple[str, bytes]:
    """Return (label, bytes). Either a file path or a raw string."""
    if raw is not None:
        return ("<raw>", raw.encode("utf-8", errors="replace"))
    if path is None:
        raise ValueError("must supply path or raw")
    with open(path, "rb") as f:
        data = f.read()
    return (os.path.relpath(path), data)


# ============================================================
# Diagnostic 1: 2x2 quadrant balance
# ============================================================

def quadrant_balance(data: bytes) -> Dict[str, Any]:
    """
    Project the input bytes into a 2x2 grid using two binary axes:

        Axis A (source_side):    bit 7 of each byte
                                  0 -> INTERNAL-leaning (low ASCII)
                                  1 -> EXTERNAL-leaning (high ASCII / binary)

        Axis B (semantic_side):  parity of the byte value
                                  even -> STRUCTURE (operators, brackets)
                                  odd  -> CONTENT   (letters, digits)

    Then check the four-cell mass distribution. A perfectly flat 2x2 has
    each cell at 0.25. The Flatness Theorem says it cannot stay flat -- but
    a healthy structure should still have all four populated above an empty
    floor. The score is min(cell_fraction) / 0.25, capped at 1.0.

    Score 0.0  -> at least one quadrant empty (degenerate)
    Score 1.0  -> all four >= 0.25 (perfectly populated)
    """
    if not data:
        return {"score": 0.0, "verdict": "empty input",
                "quadrants": {"A11": 0, "A12": 0, "A21": 0, "A22": 0}}

    counts = {"A11": 0, "A12": 0, "A21": 0, "A22": 0}
    for b in data:
        a = 1 if (b & 0x80) else 0
        s = 1 if (b & 0x01) else 0
        cell = f"A{a+1}{s+1}"
        counts[cell] += 1

    total = sum(counts.values())
    fractions = {k: v / total for k, v in counts.items()}
    min_frac = min(fractions.values())
    score = min(min_frac / 0.25, 1.0)

    if score == 0.0:
        verdict = "DEGENERATE: at least one quadrant empty"
    elif score < 0.4:
        verdict = "IMBALANCED: heavy mass concentration"
    elif score < T_STAR:
        verdict = "BELOW T*: marginally populated"
    else:
        verdict = "BALANCED: all four quadrants healthy"

    return {
        "score": round(score, 4),
        "verdict": verdict,
        "quadrants": {k: round(v, 4) for k, v in fractions.items()},
    }


# ============================================================
# Diagnostic 2: corridor leakage
# ============================================================

def corridor_leakage(data: bytes) -> Dict[str, Any]:
    """
    Define two disjoint "corridors" by byte value:

        MAX corridor: bytes where (b mod 10) is in {0, 4, 8}
                      (representatives of the additive-seam side)

        ADD corridor: bytes where (b mod 10) is in {1, 2}
                      (representatives of the small-additive-seam side)

    These are CHOSEN to be disjoint by construction. Leakage is the
    fraction of bytes that fall in the symmetric overlap zone {b mod 10
    in {3, 7, 9}} -- the canonical core, which should NOT carry seam mass
    if the structure is clean.

    A clean partition keeps core leakage low. We score
    1.0 - (core_fraction / 0.30), so 30% core mass = score 0, 0% = 1.0.
    """
    if not data:
        return {"score": 1.0, "verdict": "empty input (vacuously clean)",
                "max_fraction": 0.0, "add_fraction": 0.0, "core_fraction": 0.0}

    max_set = {0, 4, 8}
    add_set = {1, 2}
    core_set = {3, 7, 9}

    max_n = sum(1 for b in data if (b % 10) in max_set)
    add_n = sum(1 for b in data if (b % 10) in add_set)
    core_n = sum(1 for b in data if (b % 10) in core_set)
    total = len(data)

    core_frac = core_n / total
    score = max(0.0, 1.0 - core_frac / 0.30)

    if score >= T_STAR:
        verdict = "CLEAN: corridor partition holds"
    elif score >= 0.5:
        verdict = "MILD LEAKAGE: corridor structure mostly preserved"
    elif score >= 0.2:
        verdict = "LEAKING: significant core mass crossing seams"
    else:
        verdict = "BROKEN: corridor partition violated"

    return {
        "score": round(score, 4),
        "verdict": verdict,
        "max_fraction": round(max_n / total, 4),
        "add_fraction": round(add_n / total, 4),
        "core_fraction": round(core_frac, 4),
    }


# ============================================================
# Diagnostic 3: sigma non-associativity
# ============================================================

def sigma_op(x: int, y: int, n: int = 10) -> int:
    """
    Reference sigma operator on Z/nZ used by the diagnostic.

    Defined as the canonical 3-layer tower from Sprint 17:
        if (x, y) in S_MAX  -> max(x, y)
        elif (x, y) in S_ADD -> (x + y) mod n
        else                -> 0   (the C_0 attractor at h=7 collapses to 0
                                     for diagnostic purposes here -- we are
                                     measuring associativity violation rate,
                                     not reconstructing the published TSML)

    For n=10 the sets used are exactly the six MAX seams and two ADD seams
    from the published TSML decomposition.
    """
    S_MAX = {(2, 4), (4, 2), (2, 9), (9, 2), (4, 8), (8, 4)}
    S_ADD = {(1, 2), (2, 1)}
    if (x, y) in S_MAX:
        return max(x, y)
    if (x, y) in S_ADD:
        return (x + y) % n
    return 0


def sigma_non_associativity(data: bytes, n: int = 10) -> Dict[str, Any]:
    """
    Sample triples (a, b, c) from the input bytes mod n and compute the
    fraction violating associativity:

        (a sigma b) sigma c  !=  a sigma (b sigma c)

    Sigma is defined per the Sprint 17 canonical tower (see sigma_op above).
    A high non-associativity fraction means the input is structurally
    INCOMPATIBLE with the canonical tower -- i.e., it is not a clean
    instance of the framework. A low fraction means it sits inside the
    associative span of the seams.

    Score: 1.0 - non_assoc_fraction.
    """
    if len(data) < 3:
        return {"score": 1.0, "verdict": "too few samples (vacuously clean)",
                "non_assoc_fraction": 0.0, "samples": 0}

    samples = []
    # Stride of 3 to get non-overlapping triples
    for i in range(0, len(data) - 2, 3):
        a, b, c = data[i] % n, data[i + 1] % n, data[i + 2] % n
        samples.append((a, b, c))

    violations = 0
    for a, b, c in samples:
        left = sigma_op(sigma_op(a, b, n), c, n)
        right = sigma_op(a, sigma_op(b, c, n), n)
        if left != right:
            violations += 1

    frac = violations / len(samples) if samples else 0.0
    score = max(0.0, 1.0 - frac)

    if score >= T_STAR:
        verdict = "ASSOCIATIVE: sits inside canonical tower span"
    elif score >= 0.5:
        verdict = "PARTIAL: drift from canonical associativity"
    else:
        verdict = "NON-ASSOCIATIVE: incompatible with canonical tower"

    return {
        "score": round(score, 4),
        "verdict": verdict,
        "non_assoc_fraction": round(frac, 4),
        "samples": len(samples),
    }


# ============================================================
# Top-level diagnose
# ============================================================

def diagnose(path: str = None, raw: str = None) -> Dict[str, Any]:
    """Run all three diagnostics. Returns one JSON-serializable dict."""
    label, data = load_input(path=path, raw=raw)

    qb = quadrant_balance(data)
    cl = corridor_leakage(data)
    sn = sigma_non_associativity(data)

    overall = (qb["score"] + cl["score"] + sn["score"]) / 3.0
    digest = hashlib.sha256(data).hexdigest()[:16]

    return {
        "object": label,
        "bytes": len(data),
        "sha256_16": digest,
        "diagnostics": {
            "quadrant_balance": qb,
            "corridor_leakage": cl,
            "sigma_non_associativity": sn,
        },
        "overall_coherence": round(overall, 4),
        "above_threshold": overall >= T_STAR,
        "T_star": T_STAR,
    }


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="CK diagnose: paradox-classifier scan over any input"
    )
    parser.add_argument("path", nargs="?", help="file to diagnose")
    parser.add_argument("--raw", type=str, default=None,
                        help="diagnose an inline string instead")
    parser.add_argument("--pretty", action="store_true",
                        help="pretty-print the JSON")
    args = parser.parse_args()

    if not args.path and args.raw is None:
        parser.error("supply a file path or --raw <string>")

    result = diagnose(path=args.path, raw=args.raw)
    indent = 2 if args.pretty else None
    print(json.dumps(result, indent=indent))


if __name__ == "__main__":
    main()
