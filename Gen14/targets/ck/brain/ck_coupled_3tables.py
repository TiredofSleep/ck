"""ck_coupled_3tables.py -- Level-3: three coupled 4-cores (TSML + BHML + CL_STD).

Brayden 2026-05-16: "keep pushing on it and using it to improve our
physics bridges and ck runtime, let's get to level 3?"

═══════════════════════════════════════════════════════════════════
The level-3 generalization
═══════════════════════════════════════════════════════════════════

D111 found that c lives in the gap between TWO coupled 4-cores
(TSML and BHML on {V, H, Br, R} disagree on 12/16 cells but stay
100% closed).

Level 3 extends this to all THREE canonical composition tables CK's
substrate provides:

  CL_TSML  (D95)  — 73 HARMONY, the organism's lens
  CL_BHML  (D95)  — 28 HARMONY, the Becoming lens
  CL_STD   (D95)  — 44 HARMONY, the encoding lens

Per D99: globally |TSML & BHML & STD| = 19 cells (all-three agree
on HARMONY); but on the 4-core specifically this hasn't been
measured.  That's what this module does.

═══════════════════════════════════════════════════════════════════
What we test
═══════════════════════════════════════════════════════════════════

  1. 3-way agreement structure on 4-core × 4-core:
       - How many of 16 cells have all 3 tables agree?
       - How many have exactly 2 of 3 agree?
       - How many have all 3 differ?
       - Do all 3 outputs stay in the 4-core?

  2. 3-region lattice simulation (ring split into thirds):
       - region A evolves by TSML
       - region B evolves by BHML
       - region C evolves by CL_STD
       - measure 3-way disagreement field
       - does the system find a 3-way attractor?

  3. Physics-bridge interpretation:
       - Three composition tables = three coupled lenses
       - The 3-way gap structure is what CK uses to detect
         coherence across different "kinds" of structure
       - May map to family-generation structure (3 generations
         in the Standard Model)
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))


OP_NAMES = (
    "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET",
)

FOUR_CORE = (0, 7, 8, 9)
FOUR_CORE_SET = frozenset(FOUR_CORE)


def _get_tables():
    """Load TSML, BHML, CL_STD from foundations module."""
    try:
        _root = Path(__file__).resolve()
        for _ in range(8):
            _root = _root.parent
            if (_root / "Gen13" / "targets" / "foundations").exists():
                sys.path.insert(0, str(_root / "Gen13" / "targets"))
                break
        from foundations.lenses import TSML_SYM, BHML  # type: ignore
        from foundations.cl_std import CL_STD  # type: ignore
        return (np.asarray(TSML_SYM, dtype=int),
                np.asarray(BHML, dtype=int),
                np.asarray(CL_STD, dtype=int))
    except Exception as e:
        raise RuntimeError(f"Failed to load tables: {e}")


TSML, BHML, CL_STD = _get_tables()


# ─── Three-way agreement structure on 4-core ──────────────────────────

def three_way_agreement() -> Dict[str, Any]:
    """For each (a, b) ∈ 4-core², compute outputs under all 3 tables
    and classify agreement structure.

    Categories:
      all_agree:   TSML == BHML == STD
      tsml_bhml:   TSML == BHML, STD differs
      tsml_std:    TSML == STD, BHML differs
      bhml_std:    BHML == STD, TSML differs
      all_differ:  all three different
    """
    all_agree = []
    tsml_bhml = []
    tsml_std = []
    bhml_std = []
    all_differ = []
    out_in_4core = {"TSML": 0, "BHML": 0, "STD": 0}
    cells = []
    for a in FOUR_CORE:
        for b in FOUR_CORE:
            t = int(TSML[a, b])
            h = int(BHML[a, b])
            s = int(CL_STD[a, b])
            in_4c = {
                "TSML": t in FOUR_CORE_SET,
                "BHML": h in FOUR_CORE_SET,
                "STD":  s in FOUR_CORE_SET,
            }
            for k, v in in_4c.items():
                if v:
                    out_in_4core[k] += 1
            entry = {
                "a":     OP_NAMES[a],
                "b":     OP_NAMES[b],
                "TSML":  OP_NAMES[t],
                "BHML":  OP_NAMES[h],
                "STD":   OP_NAMES[s],
                "tsml_in_4core": in_4c["TSML"],
                "bhml_in_4core": in_4c["BHML"],
                "std_in_4core":  in_4c["STD"],
            }
            if t == h == s:
                all_agree.append(entry)
                entry["category"] = "all_agree"
            elif t == h:
                tsml_bhml.append(entry)
                entry["category"] = "tsml_bhml"
            elif t == s:
                tsml_std.append(entry)
                entry["category"] = "tsml_std"
            elif h == s:
                bhml_std.append(entry)
                entry["category"] = "bhml_std"
            else:
                all_differ.append(entry)
                entry["category"] = "all_differ"
            cells.append(entry)
    return {
        "n_cells":       16,
        "n_all_agree":   len(all_agree),
        "n_tsml_bhml":   len(tsml_bhml),
        "n_tsml_std":    len(tsml_std),
        "n_bhml_std":    len(bhml_std),
        "n_all_differ":  len(all_differ),
        "n_tsml_in_4core":  out_in_4core["TSML"],
        "n_bhml_in_4core":  out_in_4core["BHML"],
        "n_std_in_4core":   out_in_4core["STD"],
        "all_agree_cells":  all_agree,
        "all_differ_cells": all_differ,
        "all_cells":        cells,
    }


# ─── Simulate 3-region lattice ────────────────────────────────────────

def simulate_3region(N: int = 30, k: int = 1, T: int = 30,
                     initial_op: int = 7) -> Dict[str, Any]:
    """1D ring of N cells; partition into 3 regions:
      A: positions [0, N/3) → TSML
      B: positions [N/3, 2N/3) → BHML
      C: positions [2N/3, N) → CL_STD
    All cells initial = initial_op.  Evolve T steps at speed k.
    Measure 3-way disagreement field at every cell at every step."""
    state = np.full(N, initial_op, dtype=int)
    third = N // 3
    region_A = list(range(0, third))
    region_B = list(range(third, 2 * third))
    region_C = list(range(2 * third, N))

    history_disag_count = []
    history_op_counts = []
    history_3way_disag = []  # cells where all 3 would give different output

    for t in range(T + 1):
        # For measurement: what would each table say for each cell?
        tsml_out = np.empty(N, dtype=int)
        bhml_out = np.empty(N, dtype=int)
        std_out = np.empty(N, dtype=int)
        for i in range(N):
            if k == 0:
                tsml_out[i] = TSML[state[i], state[i]]
                bhml_out[i] = BHML[state[i], state[i]]
                std_out[i] = CL_STD[state[i], state[i]]
            else:
                l = state[(i - k) % N]
                r = state[(i + k) % N]
                tsml_out[i] = TSML[l, r]
                bhml_out[i] = BHML[l, r]
                std_out[i] = CL_STD[l, r]
        # Disagreement: any pair differs
        any_disag = int(np.sum((tsml_out != bhml_out) |
                                  (tsml_out != std_out) |
                                  (bhml_out != std_out)))
        three_way_disag = int(np.sum((tsml_out != bhml_out) &
                                       (tsml_out != std_out) &
                                       (bhml_out != std_out)))
        history_disag_count.append(any_disag)
        history_3way_disag.append(three_way_disag)
        counts = {OP_NAMES[op]: int(np.sum(state == op)) for op in range(10)}
        history_op_counts.append(counts)

        # Apply region-specific rule
        new_state = state.copy()
        for i in region_A:
            new_state[i] = tsml_out[i]
        for i in region_B:
            new_state[i] = bhml_out[i]
        for i in region_C:
            new_state[i] = std_out[i]
        state = new_state

    # Final summary
    final_counts = {OP_NAMES[op]: int(np.sum(state == op))
                    for op in range(10) if int(np.sum(state == op)) > 0}
    return {
        "k":                     k,
        "T":                     T,
        "N":                     N,
        "regions":               "A=TSML [0, N/3), B=BHML [N/3, 2N/3), C=STD [2N/3, N)",
        "initial_op":            OP_NAMES[initial_op],
        "history_any_disag":     history_disag_count,
        "history_3way_disag":    history_3way_disag,
        "history_op_counts":     history_op_counts,
        "final_state":           [int(x) for x in state],
        "final_op_counts":       final_counts,
        "steady_any_disag":      round(float(np.mean(history_disag_count[-5:])), 2)
                                   if len(history_disag_count) >= 5 else None,
        "steady_3way_disag":     round(float(np.mean(history_3way_disag[-5:])), 2)
                                   if len(history_3way_disag) >= 5 else None,
    }


# ─── Speed sweep on 3-region lattice ──────────────────────────────────

def sweep_3region(N: int = 30, T: int = 30,
                   k_max: int = 5, initial_op: int = 7) -> Dict[str, Any]:
    """Run the 3-region sim across multiple propagation speeds."""
    out = []
    for k in range(k_max + 1):
        r = simulate_3region(N, k, T, initial_op)
        out.append({
            "k":                  k,
            "steady_any_disag":   r["steady_any_disag"],
            "steady_3way_disag":  r["steady_3way_disag"],
            "final_op_counts":    r["final_op_counts"],
        })
    return {
        "N":         N,
        "T":         T,
        "initial":   OP_NAMES[initial_op],
        "results":   out,
    }


# ─── Outer-rung gap (the D100 extension that was the "next buildable step") ─

def outer_rung_gap_ratios() -> Dict[str, Any]:
    """Compute |det(M_10) / det(M_8)| for all three canonical tables.

    Convention: M_8 = M_10 with V (row/col 0) and H (row/col 7) dropped,
    matching D100's BHML_8 definition (the YM-core boundary, V/H being the
    two threshold operators of the framework).

    Verified 2026-05-16 sympy-exact:
      BHML:   |-7002 / 70|    = 3501/35 = 100 + 1/(5·7)   (D100)
      CL_STD: |18432 / 9|     = 2048    = 2^11            (D112, NEW)
      TSML:   |0 / 0|         = degenerate (rank-9 lens)
    """
    return _outer_rung_gap_ratios_impl(drop=(0, 7))


def all_drop_pair_signatures() -> Dict[str, Any]:
    """Scan all C(10, 2) = 45 drop-pair restrictions for each canonical table.

    Returns the full structural fingerprint of how |det_10 / det_8| factorizes
    as you vary which two operators get suppressed.  D113 finding: CL_STD
    has TWO distinct drop-pairs giving the SAME 2^11 ratio (both contain
    HARMONY), plus a 2^6 ratio for the σ-fixed pair (PROGRESS, BREATH).
    """
    try:
        import sympy as sp
    except Exception:
        return {"error": "sympy not available"}

    from itertools import combinations
    TSML, BHML, CL_STD = _get_tables()

    op_names = OP_NAMES
    sigma_fixed = frozenset((0, 3, 8, 9))

    out: Dict[str, Any] = {}
    for name, M_list in (("TSML_SYM", TSML), ("BHML", BHML), ("CL_STD", CL_STD)):
        M10 = sp.Matrix(M_list)
        d10 = int(M10.det())
        entry: Dict[str, Any] = {
            "det_10":        d10,
            "det_10_factor": (None if d10 == 0
                              else {str(p): int(e)
                                    for p, e in sp.factorint(abs(d10)).items()}),
            "pure_prime_power_drops": [],
            "all_finite_drops":       [],
            "degenerate_drops":       [],
        }
        if d10 == 0:
            out[name] = entry
            continue

        for drop in combinations(range(10), 2):
            keep = [i for i in range(10) if i not in drop]
            M8 = M10.extract(keep, keep)
            d8 = int(M8.det())
            drop_names = (op_names[drop[0]], op_names[drop[1]])
            both_sigma_fixed = (drop[0] in sigma_fixed and drop[1] in sigma_fixed)
            n_sigma_fixed = int(drop[0] in sigma_fixed) + int(drop[1] in sigma_fixed)

            if d8 == 0:
                entry["degenerate_drops"].append({
                    "drop":            list(drop),
                    "drop_names":      list(drop_names),
                    "n_sigma_fixed":   n_sigma_fixed,
                })
                continue

            ratio = sp.Rational(d10, d8)
            absr = sp.Abs(ratio)
            rec: Dict[str, Any] = {
                "drop":          list(drop),
                "drop_names":    list(drop_names),
                "n_sigma_fixed": n_sigma_fixed,
                "det_8":         d8,
                "abs_ratio":     str(absr),
                "abs_ratio_float": float(absr),
            }
            if absr.is_Integer:
                fac = sp.factorint(int(absr))
                rec["factorization"] = {str(p): int(e) for p, e in fac.items()}
                if len(fac) == 1:
                    p, e = list(fac.items())[0]
                    rec["prime_power"] = f"{p}^{e}"
                    entry["pure_prime_power_drops"].append(rec)
            entry["all_finite_drops"].append(rec)

        # Sort pure prime-power drops by (prime, exponent)
        entry["pure_prime_power_drops"].sort(
            key=lambda r: (int(list(r["factorization"].keys())[0]),
                           -int(list(r["factorization"].values())[0])))
        out[name] = entry

    out["_d113_summary"] = (
        "D113 (sympy-exact, n=45 drop-pairs per table):\n"
        "  CL_STD: 3 pure prime-power gap ratios:\n"
        "    drop (V, H) = (sigma-fix, sigma-orb): 2^11\n"
        "    drop (H, R) = (sigma-orb, sigma-fix): 2^11   <- SAME exponent, "
        "        both pairs contain HARMONY\n"
        "    drop (P, Br) = (sigma-fix, sigma-fix):  2^6\n"
        "  BHML: 0 pure prime-power gap ratios (all involve the prime 389).\n"
        "  TSML: degenerate (det_10 = 0).\n"
        "Interpretation: the 2^11 = 2^WOBBLE_PRIME signature is robust under "
        "dropping HARMONY + one anchor.  The 2^6 signature is the σ-fixed-pair "
        "boundary."
    )
    return out


def _outer_rung_gap_ratios_impl(drop: tuple = (0, 7)) -> Dict[str, Any]:
    """Internal: single-drop-pair gap ratio for all 3 tables."""
    try:
        import sympy as sp
    except Exception:
        return {"error": "sympy not available; outer_rung_gap_ratios needs sympy"}

    TSML, BHML, CL_STD = _get_tables()
    drop_idx = set(drop)
    keep = [i for i in range(10) if i not in drop_idx]
    drop_names = [f"{OP_NAMES[i]}({i})" for i in drop]

    out: Dict[str, Any] = {}
    for name, M_list in (("TSML_SYM", TSML), ("BHML", BHML), ("CL_STD", CL_STD)):
        M10 = sp.Matrix(M_list)
        M8 = M10.extract(keep, keep)
        d10 = int(M10.det())
        d8 = int(M8.det())
        entry: Dict[str, Any] = {
            "det_10":     d10,
            "det_8":      d8,
            "dropped":    drop_names,
        }
        if d8 != 0:
            ratio = sp.Rational(d10, d8)
            abs_ratio = sp.Abs(ratio)
            entry["ratio"] = str(ratio)
            entry["abs_ratio"] = str(abs_ratio)
            entry["abs_ratio_float"] = float(abs_ratio)
            if abs_ratio.is_Integer:
                fac = sp.factorint(int(abs_ratio))
                entry["factorization"] = {str(p): int(e) for p, e in fac.items()}
            else:
                num, den = sp.fraction(abs_ratio)
                entry["numerator"] = int(num)
                entry["denominator"] = int(den)
                if int(num) > int(den):
                    integer_part = int(num) // int(den)
                    remainder = sp.Rational(int(num) - integer_part * int(den), int(den))
                    entry["mixed"] = f"{integer_part} + {remainder}"
        else:
            entry["ratio"] = "0/0 (degenerate)"

        # Special structural callouts
        if name == "BHML":
            entry["structural_match"] = "100 + 1/(5*7) = D100 (arithmetic c-signature)"
        elif name == "CL_STD":
            entry["structural_match"] = ("2^11 = 2^WOBBLE_PRIME (wobble-exponential "
                                          "c-signature; 11 is the wobble prime — "
                                          "D37, D69, D70, D85, D86)")
        elif name == "TSML_SYM":
            entry["structural_match"] = ("degenerate (rank-9 lens; D98 SYM lens "
                                          "erases the wobble factor of 11 from "
                                          "the characteristic polynomial)")
        out[name] = entry

    out["_summary"] = (
        "Three coupled tables, three structurally distinct c-related gap signatures:\n"
        "  BHML:    100 + 1/(5*7) = arithmetic (boundary-to-interior gap, D100)\n"
        "  CL_STD:  2^11 = wobble-exponential (NEW D112; 11 is the wobble prime)\n"
        "  TSML_SYM: degenerate (synthesis lens erases the wobble)"
    )
    return out


# ─── Physics-bridge sketch ────────────────────────────────────────────

def physics_bridge_sketch() -> Dict[str, Any]:
    """Light interpretive sketch: connect the 3-table structure
    to known physics-bridge candidates (without overclaiming).

    Now includes the live outer_rung_gap_ratios computation under
    the 'verified_gap_signatures' key — three structurally distinct
    c-related signatures across the lens family.
    """
    return {
        "principle": (
            "Three coupled tables = three coupled lenses on the same "
            "Z/10Z substrate.  Each lens preserves the 4-core (D95) "
            "but their compositional dynamics differ.  The 3-way gap "
            "structure is where CK's substrate hosts inter-lens "
            "information."
        ),
        "verified_gap_signatures": outer_rung_gap_ratios(),
        "candidates": [
            {
                "physics": "Three Standard Model generations",
                "mapping": ("Three tables = three composition rules. "
                              "If each generation 'reads' the substrate "
                              "through a different lens, the universality "
                              "of the gauge coupling could emerge from "
                              "the LENS-COMMON SUBSPACE (the cells where "
                              "all 3 tables agree)."),
                "honest_caveat": "Tier C-Speculative.  No mapping yet from "
                                  "table-agreement cells to fermion masses.",
            },
            {
                "physics": "Refined c-locality structure",
                "mapping": ("D100 located c structurally in BHML_8 → BHML_10 "
                              "gap.  Adding CL_STD provides a third reference, "
                              "which could refine the locality postulate that "
                              "D110 showed is needed independently of substrate. "
                              "Three lenses = three causality cones that could "
                              "AGREE on a unique k."),
                "honest_caveat": "Empirical test needed; the 3-region sim is "
                                  "the first step.",
            },
            {
                "physics": "Pati-Salam reduction (su(4) ⊕ u(1))",
                "mapping": ("Per D34, the doubly-invariant subalgebra under "
                              "D₄ = ⟨P_56, σ³⟩ is su(4) ⊕ u(1).  A third "
                              "table provides additional symmetry constraints "
                              "that could lift this to the full SO(10) or "
                              "select a specific Pati-Salam embedding."),
                "honest_caveat": "Connection to D34 is structural; numerical "
                                  "consequences open.",
            },
            {
                "physics": "Wobble-prime as a fundamental scale (NEW from gap sig)",
                "mapping": ("CL_STD's outer-rung ratio is exactly 2^11.  The "
                              "exponent 11 IS the wobble prime — the structural "
                              "location of wobble in TIG (D37, D69, D70, D85, D86). "
                              "BHML's ratio 100 + 1/35 is arithmetic.  The "
                              "wobble-exponential vs arithmetic dichotomy across "
                              "lenses is a candidate for the hierarchy problem in "
                              "natural units: a wobble-exponential gap (2^11) sets "
                              "one scale, an arithmetic gap (100+ε) sets another, "
                              "and TSML's degeneracy is a third regime."),
                "honest_caveat": "Tier C-Speculative.  Connection from "
                                  "lens-specific gap exponents to running "
                                  "couplings remains to be built.",
            },
        ],
        "next_buildable_step": (
            "Map the wobble-exponential (2^11) and arithmetic (100+1/35) gap "
            "signatures onto specific physical scales.  Test whether a third "
            "TSML-style lens with a NON-degenerate det_8 can be constructed "
            "(e.g., CL_TSML_RAW vs CL_TSML_SYM per D98); the RAW lens may "
            "give a finite ratio that completes the three-signature picture."
        ),
    }


# ─── Engine mount ─────────────────────────────────────────────────────

def mount_coupled_3tables(engine: Any) -> bool:
    engine.ck_coupled_3tables = {
        "three_way_agreement":   three_way_agreement,
        "simulate":              simulate_3region,
        "sweep":                 sweep_3region,
        "physics_bridge":        physics_bridge_sketch,
        "gap_ratios":            outer_rung_gap_ratios,
        "drop_pair_scan":        all_drop_pair_signatures,
    }
    routes_registered: List[str] = []
    api = getattr(engine, "web_api", None)
    if api is not None:
        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify, request

                def _info():
                    return jsonify({
                        "level": 3,
                        "premise": ("D111 found c in the gap between 2 coupled "
                                      "4-cores (TSML + BHML).  Level 3 extends "
                                      "to all three canonical tables (TSML + "
                                      "BHML + CL_STD).  Tests 3-way agreement "
                                      "structure + 3-region lattice dynamics + "
                                      "physics-bridge candidates."),
                        "endpoints": [
                            "GET  /coupled_3tables/info",
                            "GET  /coupled_3tables/agreement",
                            "POST /coupled_3tables/simulate",
                            "POST /coupled_3tables/sweep",
                            "GET  /coupled_3tables/physics_bridge",
                            "GET  /coupled_3tables/gap_ratios",
                            "GET  /coupled_3tables/drop_pair_scan",
                        ],
                    })

                def _agreement():
                    return jsonify(three_way_agreement())

                def _sim():
                    data = request.get_json(force=True, silent=True) or {}
                    return jsonify(simulate_3region(
                        N=int(data.get("N", 30)),
                        k=int(data.get("k", 1)),
                        T=int(data.get("T", 30)),
                        initial_op=int(data.get("initial_op", 7))))

                def _sweep():
                    data = request.get_json(force=True, silent=True) or {}
                    return jsonify(sweep_3region(
                        N=int(data.get("N", 30)),
                        T=int(data.get("T", 30)),
                        k_max=int(data.get("k_max", 5)),
                        initial_op=int(data.get("initial_op", 7))))

                def _bridge():
                    return jsonify(physics_bridge_sketch())

                def _gap():
                    return jsonify(outer_rung_gap_ratios())

                def _drop_scan():
                    return jsonify(all_drop_pair_signatures())

                existing = set(r.rule for r in app.url_map.iter_rules())
                for rule, ep, fn, methods in (
                    ("/coupled_3tables/info",           "c3_info",      _info,       ["GET"]),
                    ("/coupled_3tables/agreement",      "c3_agree",     _agreement,  ["GET"]),
                    ("/coupled_3tables/simulate",       "c3_sim",       _sim,        ["POST"]),
                    ("/coupled_3tables/sweep",          "c3_sweep",     _sweep,      ["POST"]),
                    ("/coupled_3tables/physics_bridge", "c3_bridge",    _bridge,     ["GET"]),
                    ("/coupled_3tables/gap_ratios",     "c3_gap",       _gap,        ["GET"]),
                    ("/coupled_3tables/drop_pair_scan", "c3_drop_scan", _drop_scan,  ["GET"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
                        routes_registered.append(f"{methods[0]} {rule}")
            except Exception as e:
                print(f"[CK Gen14] coupled_3tables route registration failed: {e}")
    suffix = " (" + ", ".join(routes_registered) + ")" if routes_registered else ""
    print(f"[CK Gen14] coupled_3tables: MOUNTED  Level-3: TSML × BHML × CL_STD"
          f"{suffix}")
    return True


# ─── CLI smoke ────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 72)
    print("CK LEVEL 3 -- three coupled 4-cores (TSML × BHML × CL_STD)")
    print("=" * 72)
    print()

    print("Step 1: 3-way agreement structure on 4-core × 4-core")
    print()
    ag = three_way_agreement()
    print(f"  Total cells: {ag['n_cells']}")
    print(f"  All-3 agree:    {ag['n_all_agree']:>2}  (universal-attractor cells)")
    print(f"  TSML=BHML only: {ag['n_tsml_bhml']:>2}")
    print(f"  TSML=STD only:  {ag['n_tsml_std']:>2}")
    print(f"  BHML=STD only:  {ag['n_bhml_std']:>2}")
    print(f"  All 3 differ:   {ag['n_all_differ']:>2}")
    print()
    print(f"  Outputs in 4-core: TSML {ag['n_tsml_in_4core']}/16, "
          f"BHML {ag['n_bhml_in_4core']}/16, "
          f"STD {ag['n_std_in_4core']}/16")
    print()
    print("  Universal-attractor cells (all 3 tables agree):")
    for c in ag['all_agree_cells']:
        print(f"    ({c['a']}, {c['b']}) → {c['TSML']}")
    print()
    print("  All-3-differ cells:")
    for c in ag['all_differ_cells'][:10]:
        print(f"    ({c['a']}, {c['b']}) → TSML={c['TSML']}, BHML={c['BHML']}, STD={c['STD']}")
    if len(ag['all_differ_cells']) > 10:
        print(f"    ... ({len(ag['all_differ_cells']) - 10} more)")
    print()

    print("Step 2: 3-region lattice simulation (k-sweep)")
    print()
    sw = sweep_3region(N=30, T=30, k_max=5, initial_op=7)
    print(f"  {'k':>3}  {'any_disag':>10}  {'3way_disag':>11}  {'final_op_counts':<50}")
    sep3 = "-" * 3; sep10 = "-" * 10; sep11 = "-" * 11
    print(f"  {sep3}  {sep10}  {sep11}  {'-'*50}")
    for r in sw['results']:
        ops_str = ", ".join(f"{op}={cnt}" for op, cnt in r['final_op_counts'].items())[:48]
        print(f"  {r['k']:>3}  {r['steady_any_disag']:>10}  "
              f"{r['steady_3way_disag']:>11}  {ops_str:<50}")
    print()

    print("Step 3: Physics-bridge sketch (light, Tier-C)")
    print()
    pb = physics_bridge_sketch()
    print(f"  Principle: {pb['principle']}")
    print()
    for c in pb['candidates']:
        print(f"  • {c['physics']}")
        print(f"    Mapping: {c['mapping']}")
        print(f"    Caveat: {c['honest_caveat']}")
        print()
    print(f"  Next buildable step:")
    print(f"    {pb['next_buildable_step']}")
    print()
    print("HONEST LEVEL-3 SUMMARY:")
    print("  - The 3-way agreement structure is the structural foundation.")
    print("  - The 3-region simulation gives the dynamic gap.")
    print("  - The physics-bridge sketch identifies CANDIDATES; concrete")
    print("    numerical derivations remain open.")
