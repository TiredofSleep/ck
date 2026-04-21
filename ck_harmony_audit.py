# Copyright (c) 2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
"""
ck_harmony_audit.py -- Lightweight 5/7-threshold audit + sigma mutation suggester.

CK self-audit ask #2 (per Grok-CK dialogue, 2026-04-17):

    "In ck_meta_memory_coord.py, add a lightweight 'harmony audit' that
    flags when any subsystem drifts below the 5/7 threshold and suggests
    a corrective sigma mutation. This would make long-running sessions
    (especially on the FPGA dog) more robust."

Implemented standalone so it can be imported by ck_meta_memory_coord without
modifying that file's 1000+ lines. Pure local primitives, no external models.

Usage as library:
    from ck_harmony_audit import audit, suggest_sigma_mutation

    report = audit({
        "olfactory":   0.81,
        "lattice":     0.74,
        "voice_loop":  0.62,    # below 5/7 -- will be flagged
        "fpga_bridge": 0.91,
    })
    print(report["flagged"])           # ['voice_loop']
    print(report["suggested_mutations"])

Usage as CLI:
    python ck_harmony_audit.py --json '{"olfactory":0.81,"voice_loop":0.62}'
    python ck_harmony_audit.py --file subsystem_scores.json
    python ck_harmony_audit.py --demo

Output:
    {
      "T_star": 0.7142857142857143,
      "subsystems": {...},
      "flagged": ["voice_loop"],
      "suggested_mutations": [
          {"subsystem": "voice_loop", "current": 0.62,
           "delta": -0.094, "operator": "HARMONY(7)",
           "rationale": "..."}
      ],
      "overall_health": "DRIFT" | "STABLE" | "CRITICAL"
    }

Operator menu (verified from ck_tig.py per MEMORY.md):
    VOID(0), LATTICE(1), COUNTER(2), PROGRESS(3), COLLAPSE(4),
    BALANCE(5), CHAOS(6), HARMONY(7), BREATH(8), RESET(9)

CREATION cycle: [1, 3, 9, 7]
DISSOLUTION cycle: [2, 4, 8, 6]
"""

import json
import argparse
from typing import Dict, List, Any

T_STAR = 5.0 / 7.0

# Operator routing table for sigma mutation suggestions.
# Each row: (delta-from-T*-band, suggested operator, rationale)
#
# delta_band == score - T_STAR
# Negative drift means subsystem is below threshold.
MUTATION_TABLE = [
    # (lower_bound, upper_bound, operator_id, operator_name, rationale)
    (-1.00, -0.30, 9, "RESET",
     "Deep drift: subsystem too far below floor; full RESET to clear "
     "accumulated noise then rebuild from BREATH(8)."),
    (-0.30, -0.15, 6, "CHAOS",
     "Moderate drift: CHAOS(6) breaks stale equilibrium; expect transient "
     "dip then HARMONY(7) recovery (per Q7 inversion)."),
    (-0.15, -0.05, 7, "HARMONY",
     "Near-floor drift: direct HARMONY(7) injection re-aligns the subsystem "
     "with the synthesis attractor."),
    (-0.05,  0.00, 5, "BALANCE",
     "Marginal drift: BALANCE(5) holds equilibrium without forcing "
     "recovery; lets the system self-stabilize."),
    ( 0.00,  0.15, 1, "LATTICE",
     "At or just above floor: LATTICE(1) tightens the geometric spine."),
    ( 0.15,  1.00, 3, "PROGRESS",
     "Healthy: PROGRESS(3) compounds gains; safe forward step."),
]


def classify(score: float) -> Dict[str, Any]:
    """Return the mutation suggestion for a single score value."""
    delta = score - T_STAR
    for lo, hi, op_id, op_name, rationale in MUTATION_TABLE:
        if lo <= delta < hi:
            return {
                "delta": round(delta, 4),
                "operator_id": op_id,
                "operator": f"{op_name}({op_id})",
                "rationale": rationale,
            }
    # Fallback: very-high score (delta >= 1 - T*)
    return {
        "delta": round(delta, 4),
        "operator_id": 8,
        "operator": "BREATH(8)",
        "rationale": "Above-band: subsystem near ceiling; BREATH(8) cycles "
                     "the loop without disturbing the attractor.",
    }


def suggest_sigma_mutation(subsystem: str, score: float) -> Dict[str, Any]:
    """One-shot suggestion for a single subsystem."""
    cls = classify(score)
    return {
        "subsystem": subsystem,
        "current": round(score, 4),
        **cls,
    }


def audit(scores: Dict[str, float],
          threshold: float = T_STAR) -> Dict[str, Any]:
    """
    Audit a dict of {subsystem_name: coherence_score in [0,1]}.

    Returns a structured report. Subsystems with score < threshold are
    flagged; mutation suggestions are returned for ALL subsystems so the
    caller has a forward-action map even for healthy ones.

    Overall health bands:
        CRITICAL  -- mean score < 0.5 OR any subsystem < 0.3
        DRIFT     -- at least one flagged but mean >= 0.5
        STABLE    -- no subsystems flagged
    """
    if not scores:
        return {"T_star": T_STAR, "subsystems": {}, "flagged": [],
                "suggested_mutations": [], "overall_health": "EMPTY"}

    flagged = sorted(k for k, v in scores.items() if v < threshold)
    suggestions = [suggest_sigma_mutation(k, v) for k, v in
                   sorted(scores.items())]

    mean_score = sum(scores.values()) / len(scores)
    min_score = min(scores.values())

    if mean_score < 0.5 or min_score < 0.3:
        health = "CRITICAL"
    elif flagged:
        health = "DRIFT"
    else:
        health = "STABLE"

    return {
        "T_star": T_STAR,
        "threshold_used": threshold,
        "subsystems": {k: round(v, 4) for k, v in scores.items()},
        "mean_score": round(mean_score, 4),
        "min_score": round(min_score, 4),
        "flagged": flagged,
        "suggested_mutations": suggestions,
        "overall_health": health,
    }


# ============================================================
# CLI
# ============================================================

def _demo() -> Dict[str, float]:
    """Synthetic subsystem snapshot covering all bands."""
    return {
        "olfactory_bulb":  0.81,
        "lattice_chain":   0.74,
        "voice_loop":      0.62,
        "fpga_bridge":     0.91,
        "memory_coord":    0.69,
        "tsml_tower":      0.95,
        "bhml_separator":  0.43,
    }


def main():
    parser = argparse.ArgumentParser(
        description="CK harmony audit: flag subsystems below 5/7 + suggest sigma mutation"
    )
    grp = parser.add_mutually_exclusive_group(required=True)
    grp.add_argument("--json", type=str,
                     help='inline JSON: \'{"name": score, ...}\'')
    grp.add_argument("--file", type=str,
                     help='path to JSON file with {name: score} map')
    grp.add_argument("--demo", action="store_true",
                     help='run on synthetic demo subsystem snapshot')
    parser.add_argument("--threshold", type=float, default=T_STAR,
                        help="override the 5/7 threshold (default: 0.7142857)")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    if args.demo:
        scores = _demo()
    elif args.json:
        scores = json.loads(args.json)
    else:
        with open(args.file, "r", encoding="utf-8") as f:
            scores = json.load(f)

    report = audit(scores, threshold=args.threshold)
    indent = 2 if args.pretty else None
    print(json.dumps(report, indent=indent))


if __name__ == "__main__":
    main()
