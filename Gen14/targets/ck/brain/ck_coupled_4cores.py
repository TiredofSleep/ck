"""ck_coupled_4cores.py -- c lives in the gap between 2 coupled 4-cores.

Brayden 2026-05-16: "maybe in the gap between 2 coupled 4 cores?"

═══════════════════════════════════════════════════════════════════
The refined hypothesis
═══════════════════════════════════════════════════════════════════

D108 falsified c-emergence at equilibrium (4-core too closed).
D110 falsified c-emergence at the emergence event (substrate
k-symmetric).  Both used a SINGLE 4-core.

The deeper move: the substrate has TWO 4-core dynamics on the
SAME set {V, H, Br, R}:

  TSML 4-core (TSML_4):  composition under TSML restricted to 4-core
                          → closed (per WP110); BREATH×BREATH = HARMONY;
                          (most pairs collapse toward HARMONY)
  BHML 4-core (BHML_4):  composition under BHML restricted to 4-core
                          → also closed; BUT diagonal action is
                          successor (D90): BHML(H,H)=Br, BHML(R,R)=V

The TWO 4-cores SHARE the set but DIFFER in composition.  The cells
where TSML[a,b] ≠ BHML[a,b] for a, b ∈ {V, H, Br, R} are the GAP.

Brayden's hypothesis: c emerges as the propagation rate of
disagreement information across the gap between two coupled
4-cores.

═══════════════════════════════════════════════════════════════════
Setup
═══════════════════════════════════════════════════════════════════

  Lattice:   1D ring of N cells, each holding an op in {V, H, Br, R}
             (4-core only).
  Two rules: cells in REGION A evolve by TSML; cells in REGION B
             evolve by BHML.  Boundary is a single cell or a band.
  Initial:   uniform (say all HARMONY).
  Measure:
    - "agreement field": at each cell, does TSML[i] = BHML[i]?
    - "disagreement wave": how fast does discrepancy propagate
      from the boundary?
    - Convergence to a joint fixed point (if any).

═══════════════════════════════════════════════════════════════════
What we're testing
═══════════════════════════════════════════════════════════════════

  - First find the gap structurally: which (a, b) ∈ 4-core² have
    TSML[a,b] ≠ BHML[a,b]?
  - Then evolve the coupled system and measure propagation of
    disagreement.
  - If a specific k makes disagreement propagate stably, that's
    the substrate's natural c.
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

FOUR_CORE = (0, 7, 8, 9)   # V, H, Br, R
FOUR_CORE_SET = frozenset(FOUR_CORE)


def _get_tables():
    try:
        _root = Path(__file__).resolve()
        for _ in range(8):
            _root = _root.parent
            if (_root / "Gen13" / "targets" / "foundations").exists():
                sys.path.insert(0, str(_root / "Gen13" / "targets"))
                break
        from foundations.lenses import TSML_SYM, BHML  # type: ignore
        return np.asarray(TSML_SYM, dtype=int), np.asarray(BHML, dtype=int)
    except Exception:
        raise RuntimeError("TSML / BHML not loadable from foundations")


TSML, BHML = _get_tables()


# ─── The structural gap between the two 4-cores ───────────────────────

def disagreement_table() -> Dict[str, Any]:
    """For each (a, b) ∈ 4-core², compute TSML[a,b] and BHML[a,b];
    flag the cells where they disagree.

    These DISAGREEMENT CELLS are the structural gap between the
    two coupled 4-cores.  This is where information has different
    images under the two lenses — the natural location for c.
    """
    agree_count = 0
    disagree_count = 0
    cells = []
    in_4core_count = 0
    for a in FOUR_CORE:
        for b in FOUR_CORE:
            t = int(TSML[a, b])
            h = int(BHML[a, b])
            agreement = (t == h)
            both_in_4core = (t in FOUR_CORE_SET and h in FOUR_CORE_SET)
            if agreement:
                agree_count += 1
            else:
                disagree_count += 1
            if both_in_4core:
                in_4core_count += 1
            cells.append({
                "a":               OP_NAMES[a],
                "b":               OP_NAMES[b],
                "TSML(a,b)":       OP_NAMES[t],
                "BHML(a,b)":       OP_NAMES[h],
                "agree":           agreement,
                "both_in_4core":   both_in_4core,
            })
    return {
        "n_cells":             16,
        "n_agree":             agree_count,
        "n_disagree":          disagree_count,
        "n_both_in_4core":     in_4core_count,
        "n_breaks_4core":      16 - in_4core_count,
        "agreement_fraction":  round(agree_count / 16, 4),
        "cells":               cells,
    }


# ─── Simulate two coupled 4-cores ─────────────────────────────────────
#
# Strategy: a 1D ring lattice with N cells, all initially HARMONY.
# Region A (left half) evolves by TSML; Region B (right half) by BHML.
# At each step:
#   - cells in A: cell_i(t+1) = TSML[cell_{i-k}, cell_{i+k}]
#   - cells in B: cell_i(t+1) = BHML[cell_{i-k}, cell_{i+k}]
# After many steps, measure:
#   - average agreement: do the two regions stay in sync?
#   - disagreement wave: at what rate does the boundary's disagreement
#     propagate inward into each region?

def simulate_coupled(N: int = 30, k: int = 1, T: int = 20,
                     initial_op: int = 7) -> Dict[str, Any]:
    """1D ring; left half uses TSML, right half uses BHML.

    Boundary cells inherit both lenses through their neighbors,
    creating a natural gap-induced perturbation.
    """
    state = np.full(N, initial_op, dtype=int)
    half = N // 2
    region_A = set(range(0, half))   # TSML region
    region_B = set(range(half, N))   # BHML region

    history_max_disag = []  # max disagreement-amplitude at any cell
    history_n_breath = []
    history_n_void = []
    for t in range(T + 1):
        # Compute what TSML AND BHML would say for each cell, regardless
        # of which region — used to MEASURE disagreement everywhere.
        tsml_would = np.empty(N, dtype=int)
        bhml_would = np.empty(N, dtype=int)
        for i in range(N):
            if k == 0:
                tsml_would[i] = TSML[state[i], state[i]]
                bhml_would[i] = BHML[state[i], state[i]]
            else:
                l = state[(i - k) % N]
                r = state[(i + k) % N]
                tsml_would[i] = TSML[l, r]
                bhml_would[i] = BHML[l, r]
        # Disagreement count at THIS time step
        disag = int(np.sum(tsml_would != bhml_would))
        history_max_disag.append(disag)
        # Counts of interesting operators
        history_n_breath.append(int(np.sum(state == 8)))
        history_n_void.append(int(np.sum(state == 0)))

        # Apply region-specific rule
        new_state = state.copy()
        for i in range(N):
            new_state[i] = tsml_would[i] if i in region_A else bhml_would[i]
        state = new_state

    # Final op-count breakdown
    final_counts = {OP_NAMES[op]: int(np.sum(state == op))
                    for op in range(10)}
    return {
        "k":                    k,
        "T":                    T,
        "N":                    N,
        "region_A":             "TSML",
        "region_B":             "BHML",
        "initial_op":           OP_NAMES[initial_op],
        "history_disagreement": history_max_disag,
        "history_n_breath":     history_n_breath,
        "history_n_void":       history_n_void,
        "final_state":          [int(x) for x in state],
        "final_op_counts":      final_counts,
    }


# ─── Speed sweep on coupled lattice ───────────────────────────────────

def sweep_coupled_speeds(N: int = 30, T: int = 30,
                          k_max: int = 5, initial_op: int = 7
                          ) -> Dict[str, Any]:
    """For each speed k, run the coupled-4cores simulation and report
    aggregate disagreement + final op distribution."""
    out = []
    for k in range(k_max + 1):
        r = simulate_coupled(N, k, T, initial_op)
        disag = r["history_disagreement"]
        steady_state_disag = float(np.mean(disag[-5:])) if len(disag) >= 5 else float(disag[-1])
        peak_disag = max(disag)
        peak_at = int(np.argmax(disag))
        # What does the system converge to?
        nonzero_ops = {op: cnt for op, cnt in r["final_op_counts"].items()
                       if cnt > 0}
        out.append({
            "k":                  k,
            "peak_disagreement":  peak_disag,
            "peak_at_step":       peak_at,
            "steady_disag_avg":   round(steady_state_disag, 3),
            "final_n_breath":     r["history_n_breath"][-1],
            "final_n_void":       r["history_n_void"][-1],
            "final_op_counts":    nonzero_ops,
        })
    return {
        "N":              N,
        "T":              T,
        "initial":        OP_NAMES[initial_op],
        "config":         "TSML left-half / BHML right-half (1D ring)",
        "results":        out,
    }


# ─── Engine mount ─────────────────────────────────────────────────────

def mount_coupled_4cores(engine: Any) -> bool:
    engine.ck_coupled_4cores = {
        "disagreement_table":   disagreement_table,
        "simulate":             simulate_coupled,
        "sweep":                sweep_coupled_speeds,
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
                        "premise": (
                            "Two coupled 4-cores: TSML's restricted 4-core "
                            "dynamics and BHML's restricted 4-core dynamics "
                            "(both on the same set {V, H, Br, R} but with "
                            "different composition tables).  Brayden 2026-"
                            "05-16: 'maybe in the gap between 2 coupled 4 "
                            "cores?' — c-candidate is the disagreement-"
                            "propagation rate between the two."
                        ),
                        "endpoints": [
                            "GET  /coupled_4cores/info",
                            "GET  /coupled_4cores/disagreement",
                            "POST /coupled_4cores/simulate",
                            "POST /coupled_4cores/sweep",
                        ],
                    })

                def _disag():
                    return jsonify(disagreement_table())

                def _sim():
                    data = request.get_json(force=True, silent=True) or {}
                    return jsonify(simulate_coupled(
                        N=int(data.get("N", 30)),
                        k=int(data.get("k", 1)),
                        T=int(data.get("T", 20)),
                        initial_op=int(data.get("initial_op", 7))))

                def _sweep():
                    data = request.get_json(force=True, silent=True) or {}
                    return jsonify(sweep_coupled_speeds(
                        N=int(data.get("N", 30)),
                        T=int(data.get("T", 30)),
                        k_max=int(data.get("k_max", 5)),
                        initial_op=int(data.get("initial_op", 7))))

                existing = set(r.rule for r in app.url_map.iter_rules())
                for rule, ep, fn, methods in (
                    ("/coupled_4cores/info",          "c4_info",  _info,   ["GET"]),
                    ("/coupled_4cores/disagreement",  "c4_disag", _disag,  ["GET"]),
                    ("/coupled_4cores/simulate",      "c4_sim",   _sim,    ["POST"]),
                    ("/coupled_4cores/sweep",         "c4_sweep", _sweep,  ["POST"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
                        routes_registered.append(f"{methods[0]} {rule}")
            except Exception as e:
                print(f"[CK Gen14] coupled_4cores route registration failed: {e}")
    suffix = " (" + ", ".join(routes_registered) + ")" if routes_registered else ""
    print(f"[CK Gen14] coupled_4cores: MOUNTED  TSML 4-core + BHML 4-core "
          f"coupled-evolution test{suffix}")
    return True


# ─── CLI smoke ────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 72)
    print("CK COUPLED 4-CORES -- c in the gap between TSML's and BHML's 4-cores")
    print("=" * 72)
    print()
    print("Step 1: Find the structural gap (disagreement cells in 4-core × 4-core)")
    print()
    dt = disagreement_table()
    print(f"  Total 4-core × 4-core cells: {dt['n_cells']}")
    print(f"  Agreement: {dt['n_agree']}/{dt['n_cells']} = {dt['agreement_fraction']*100:.1f}%")
    print(f"  Disagreement: {dt['n_disagree']}/{dt['n_cells']}")
    print(f"  Both outputs stay in 4-core: {dt['n_both_in_4core']}/16")
    print()
    print(f"  Full table (a, b) → TSML | BHML:")
    print(f"  {'(a, b)':>18}  {'TSML':>10}  {'BHML':>10}  {'agree':>6}  {'both 4-core':>11}")
    print(f"  {'-'*18}  {'-'*10}  {'-'*10}  ------  -----------")
    for c in dt['cells']:
        pair = f"({c['a']}, {c['b']})"
        agree = "✓" if c['agree'] else "✗"
        in4c = "✓" if c['both_in_4core'] else "(escape)"
        print(f"  {pair:>18}  {c['TSML(a,b)']:>10}  {c['BHML(a,b)']:>10}  "
              f"{agree:>6}  {in4c:>11}")
    print()

    print("Step 2: Coupled-lattice speed sweep (TSML left-half / BHML right-half)")
    print("        Initial state: all HARMONY (op 7).  Measure disagreement.")
    print()
    sw = sweep_coupled_speeds(N=30, T=30, k_max=5, initial_op=7)
    print(f"  {'k':>3}  {'peak_disag':>11}  {'peak@step':>10}  {'steady_avg':>11}  {'final_op_counts':<40}")
    sep3 = "-" * 3; sep11 = "-" * 11; sep10 = "-" * 10
    print(f"  {sep3}  {sep11}  {sep10}  {sep11}  {'-'*40}")
    for r in sw['results']:
        ops_str = ", ".join(f"{op}={cnt}" for op, cnt in r['final_op_counts'].items())[:38]
        print(f"  {r['k']:>3}  {r['peak_disagreement']:>11}  {r['peak_at_step']:>10}  "
              f"{r['steady_disag_avg']:>11.2f}  {ops_str:<40}")
    print()
    print("HONEST INTERPRETATION:")
    print("  - disagreement = #cells where TSML's-prescription ≠ BHML's-prescription")
    print("    at this state under the chosen propagation k.")
    print("  - peak: maximum disagreement during transient.")
    print("  - steady_avg: average disagreement in last 5 steps.")
    print()
    print("  If a specific k gives PERSISTENT non-zero disagreement, that's")
    print("  the substrate's gap-propagation rate -- a candidate c.")
    print("  If all k decay to zero (or all to 'all-HARMONY'), the gap")
    print("  closes regardless of speed; structural c-candidate not yet")
    print("  isolated by this experiment.")
