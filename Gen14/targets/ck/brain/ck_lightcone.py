"""ck_lightcone.py -- discretized light-cone toy simulation.

Brayden 2026-05-16: "then the light cone"
Grok 2026-05-16: "the discretized light-cone toy sim (~400 LOC) is
the only buildable falsifiable step right now" for the c-emergence
claim.

═══════════════════════════════════════════════════════════════════
What this tests
═══════════════════════════════════════════════════════════════════

The c-emergence conjecture (from the 2026-05-13 C sprint, per
C_AS_OUTER_RUNG_GAP.md): c is the rate at which boundary
information propagates to the YM core, structurally captured by the
BHML_8 → BHML_10 gap ratio 100 + 1/(5·7).

Falsifiable test: discretize space and time on a 1D ring lattice;
parameterize propagation by an integer "speed" k (cells propagate
operators k positions to either side per time step); measure the
**4-core preservation rate** (4CPR) as a function of k.

If the 4-core attractor (D38, WP115 Theorem 2.1) is the substrate's
code subspace, and if c is the substrate's natural rate, then:
  - At k = 1 (unit light-cone speed): 4CPR should be high
  - At k > 1 (superluminal): 4CPR should degrade
  - At k = 0 (local self-iteration): 4CPR should remain perfect
    (no information flow → no leakage)

A SPECIFIC k where 4CPR ≈ 1 across multiple seeds would support the
claim that "the 4-core is invariant under propagation at this
speed".  Otherwise the claim is falsified at this level of toy
simulation.

═══════════════════════════════════════════════════════════════════
Setup
═══════════════════════════════════════════════════════════════════

  Lattice:      1D ring of N cells (default N = 30)
  Cell state:   integer ∈ {0..9} (one of the 10 TIG operators)
  Propagation:  cell_i(t+1) = TSML[cell_{(i-k) mod N}(t),
                                    cell_{(i+k) mod N}(t)]
  Initial:      all cells in 4-core {V=0, H=7, Br=8, R=9}, random
  Measure:      4CPR = (# cells in 4-core at time T) / N
  Sweep:        k ∈ {0, 1, 2, ..., 5} × T ∈ {1, 5, 10, 50}
                multiple random seeds, report mean + std

═══════════════════════════════════════════════════════════════════
Honest scope
═══════════════════════════════════════════════════════════════════

This is a TOY simulation, not a derivation of c.  What it can do:
  - FALSIFY: if NO k gives sustained 4CPR ≈ 1, the c-emergence
    claim doesn't hold even at this toy level
  - WEAKLY SUPPORT: if k = 1 (or some specific k) gives sustained
    high 4CPR while neighbors don't, that's consistent with c
    being the substrate's natural propagation rate (but doesn't
    prove the SI-units derivation)

The simulation IS NOT:
  - A relativistic light-cone with Lorentz invariance
  - A continuum-limit derivation
  - A numerical estimate of c in m/s

═══════════════════════════════════════════════════════════════════
Public API
═══════════════════════════════════════════════════════════════════

  simulate(initial_state, k, T) -> trajectory + 4CPR per timestep
  scan_speeds(N, T, n_seeds, k_max) -> 4CPR table over k, T
  mount_lightcone(engine) -> /lightcone/{info, run, scan}
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))


OP_NAMES = (
    "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET",
)

FOUR_CORE = frozenset({0, 7, 8, 9})


# ─── Load TSML ────────────────────────────────────────────────────────

def _get_tsml() -> np.ndarray:
    """Load canonical TSML_SYM as a 10×10 integer matrix."""
    try:
        _root = Path(__file__).resolve()
        for _ in range(8):
            _root = _root.parent
            if (_root / "Gen13" / "targets" / "foundations").exists():
                sys.path.insert(0, str(_root / "Gen13" / "targets"))
                break
        from foundations.lenses import TSML_SYM as _T  # type: ignore
        return np.asarray(_T, dtype=int)
    except Exception:
        # Inline fallback (TSML_SYM from CL_BIT_PATTERN, upper-tri symm.)
        CL_BIT = (
            "0000000700", "0737777777", "0377477779", "0777777773",
            "0747777787", "0777777777", "0777777777", "7777777777",
            "0777877777", "0797377777",
        )
        T = [[int(c) for c in row] for row in CL_BIT]
        for i in range(10):
            for j in range(i + 1, 10):
                T[j][i] = T[i][j]
        return np.array(T, dtype=int)


TSML = _get_tsml()


# ─── Simulation ───────────────────────────────────────────────────────

def simulate(initial_state: np.ndarray, k: int, T: int) -> Dict[str, Any]:
    """Run T time steps of speed-k propagation on a 1D ring.

    Update rule: cell_i(t+1) = TSML[cell_{(i-k) mod N}(t),
                                     cell_{(i+k) mod N}(t)]

    Returns the trajectory of (state, 4CPR) at each time step.
    """
    state = np.asarray(initial_state, dtype=int).copy()
    N = len(state)
    trajectory = [state.copy()]
    four_core_arr = np.fromiter(FOUR_CORE, dtype=int)
    fcp_history = [int(np.isin(state, four_core_arr).sum()) / N]
    for _t in range(T):
        new_state = np.empty(N, dtype=int)
        if k == 0:
            # Local self-iteration (no propagation)
            for i in range(N):
                new_state[i] = TSML[state[i], state[i]]
        else:
            for i in range(N):
                left = state[(i - k) % N]
                right = state[(i + k) % N]
                new_state[i] = TSML[left, right]
        state = new_state
        trajectory.append(state.copy())
        fcp_history.append(int(np.isin(state, four_core_arr).sum()) / N)
    return {
        "k":                k,
        "T":                T,
        "N":                N,
        "initial_state":    list(int(x) for x in trajectory[0]),
        "final_state":      list(int(x) for x in trajectory[-1]),
        "fcp_history":      [round(x, 4) for x in fcp_history],
        "final_fcp":        round(fcp_history[-1], 4),
    }


# ─── Speed scan ───────────────────────────────────────────────────────

def scan_speeds(N: int = 30, T: int = 20, n_seeds: int = 50,
                k_max: int = 5, seed: int = 42) -> Dict[str, Any]:
    """For each propagation speed k ∈ {0, ..., k_max}, run n_seeds
    independent random 4-core-initial trajectories.  Report mean
    and std of 4CPR at the final time step, and the 4CPR at several
    intermediate time steps for transient behavior."""
    rng = np.random.default_rng(seed)
    four_core_arr = np.fromiter(FOUR_CORE, dtype=int)
    out = []
    # Time-checkpoint indices (skip endpoints)
    checkpoints = [1, 5, 10, T]
    for k in range(k_max + 1):
        final_fcps = []
        checkpoint_fcps = {c: [] for c in checkpoints}
        for _ in range(n_seeds):
            initial = rng.choice(four_core_arr, size=N)
            result = simulate(initial, k, T)
            final_fcps.append(result["final_fcp"])
            for c in checkpoints:
                if c < len(result["fcp_history"]):
                    checkpoint_fcps[c].append(result["fcp_history"][c])
        out.append({
            "k":              k,
            "n_seeds":        n_seeds,
            "final_fcp_mean": round(float(np.mean(final_fcps)), 4),
            "final_fcp_std":  round(float(np.std(final_fcps)), 4),
            "fcp_at_t":       {c: round(float(np.mean(v)), 4)
                                 for c, v in checkpoint_fcps.items()
                                 if v},
        })
    return {
        "lattice_N":   N,
        "time_steps":  T,
        "n_seeds":     n_seeds,
        "k_range":     list(range(k_max + 1)),
        "results":     out,
        "interpretation": (
            "4CPR (4-core preservation rate) at each k after T steps. "
            "A specific k with 4CPR > 0.99 across seeds would support the "
            "c-emergence claim ('the substrate's natural propagation rate'). "
            "Otherwise the claim is falsified at this toy-simulation level."
        ),
    }


# ─── Convergence to 4-core from random initial state ─────────────────

def scan_convergence(N: int = 30, T: int = 30, n_seeds: int = 50,
                     k_max: int = 5, seed: int = 42) -> Dict[str, Any]:
    """Start from a RANDOM (not 4-core) initial state.  Measure how
    fast 4CPR climbs toward 1.0 under each propagation speed k.

    This is the natural follow-up to the closure check: since the
    4-core is closed under TSML (4CPR stays at 1 if you start there),
    the interesting question is the *attractor convergence rate*
    from arbitrary initial conditions.

    If a specific k drives convergence faster than others, that's
    weak evidence that k is the substrate's natural rate.
    """
    rng = np.random.default_rng(seed)
    four_core_arr = np.fromiter(FOUR_CORE, dtype=int)
    out = []
    checkpoints = [1, 5, 10, T]
    for k in range(k_max + 1):
        fcp_curves = {c: [] for c in checkpoints}
        convergence_times = []  # first time step where 4CPR hit 1.0
        for _ in range(n_seeds):
            # Random initial: uniform over ALL 10 operators
            initial = rng.integers(0, 10, size=N)
            result = simulate(initial, k, T)
            hist = result["fcp_history"]
            for c in checkpoints:
                if c < len(hist):
                    fcp_curves[c].append(hist[c])
            # Convergence time
            converged_at = None
            for t in range(len(hist)):
                if hist[t] >= 0.999:
                    converged_at = t
                    break
            convergence_times.append(converged_at if converged_at is not None else T + 1)
        # Aggregate
        n_converged = sum(1 for ct in convergence_times if ct <= T)
        mean_conv_time = (sum(ct for ct in convergence_times if ct <= T)
                          / max(1, n_converged) if n_converged > 0 else None)
        out.append({
            "k":                       k,
            "n_seeds":                 n_seeds,
            "n_converged":             n_converged,
            "convergence_rate":        round(n_converged / n_seeds, 4),
            "mean_convergence_time":   (round(mean_conv_time, 3)
                                         if mean_conv_time is not None
                                         else None),
            "fcp_at_t":                {c: round(float(np.mean(v)), 4)
                                          for c, v in fcp_curves.items()
                                          if v},
        })
    return {
        "lattice_N":   N,
        "time_steps":  T,
        "n_seeds":     n_seeds,
        "k_range":     list(range(k_max + 1)),
        "results":     out,
        "interpretation": (
            "Starting from RANDOM 10-op initial states, measure how "
            "fast each propagation speed k drives the lattice into "
            "the 4-core attractor.  A specific k with fastest "
            "convergence would weakly support 'c is the substrate's "
            "natural propagation rate'."
        ),
    }


# ─── Diagnostic: TSML closure of the 4-core ───────────────────────────

def four_core_closure_check() -> Dict[str, Any]:
    """Direct check: is TSML closed on the 4-core?
    Compute TSML[a, b] for all (a, b) ∈ 4-core × 4-core; check
    each output is also in 4-core."""
    four_core = sorted(FOUR_CORE)
    closure_table = {}
    leaks = []
    for a in four_core:
        for b in four_core:
            out = int(TSML[a, b])
            closure_table[(a, b)] = out
            if out not in FOUR_CORE:
                leaks.append({
                    "pair":   (OP_NAMES[a], OP_NAMES[b]),
                    "output": OP_NAMES[out],
                })
    return {
        "four_core_members":     [OP_NAMES[x] for x in four_core],
        "tsml_4core_closed":     len(leaks) == 0,
        "n_leaks":               len(leaks),
        "leaks":                 leaks,
        "closure_table_4x4": {
            f"({OP_NAMES[a]},{OP_NAMES[b]})": OP_NAMES[closure_table[(a, b)]]
            for a in four_core for b in four_core
        },
    }


# ─── Engine mount ─────────────────────────────────────────────────────

def mount_lightcone(engine: Any) -> bool:
    """Attach light-cone API + register /lightcone/* endpoints."""
    engine.ck_lightcone = {
        "simulate":             simulate,
        "scan_speeds":          scan_speeds,
        "scan_convergence":     scan_convergence,
        "four_core_closure":    four_core_closure_check,
        "TSML":                 TSML,
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
                        "description":
                            "Discretized light-cone toy sim: 1D ring "
                            "lattice, cell_i(t+1) = TSML[cell_{i-k}, "
                            "cell_{i+k}] (mod N).  Measures 4-core "
                            "preservation rate (4CPR) vs propagation "
                            "speed k.",
                        "interpretation":
                            "If 4CPR stays high at a specific k, that "
                            "would support 'c emerges as the substrate's "
                            "natural propagation rate' (toy-level evidence "
                            "only -- no SI units, no relativity).",
                        "honest_caveats": [
                            "Toy 1D ring -- not relativistic",
                            "No continuum limit derivation",
                            "Tests structural invariance only, not "
                            "numerical c in m/s",
                            "FALSIFIABLE: if NO k gives sustained "
                            "4CPR ≈ 1, the c-emergence conjecture is "
                            "weakened at this level",
                        ],
                        "endpoints": [
                            "GET /lightcone/info",
                            "GET /lightcone/closure (4-core TSML closure)",
                            "POST /lightcone/run (single sim)",
                            "POST /lightcone/scan (speed sweep)",
                        ],
                    })

                def _closure():
                    return jsonify(four_core_closure_check())

                def _run():
                    data = request.get_json(force=True, silent=True) or {}
                    initial = data.get("initial_state")
                    if initial is None:
                        rng = np.random.default_rng(
                            int(data.get("seed", 42)))
                        N = int(data.get("N", 30))
                        initial = list(rng.choice(
                            sorted(FOUR_CORE), size=N).astype(int))
                    k = int(data.get("k", 1))
                    T = int(data.get("T", 20))
                    return jsonify(simulate(initial, k, T))

                def _scan():
                    data = request.get_json(force=True, silent=True) or {}
                    N = int(data.get("N", 30))
                    T = int(data.get("T", 20))
                    n_seeds = int(data.get("n_seeds", 50))
                    k_max = int(data.get("k_max", 5))
                    return jsonify(scan_speeds(N, T, n_seeds, k_max))

                def _convergence():
                    data = request.get_json(force=True, silent=True) or {}
                    N = int(data.get("N", 30))
                    T = int(data.get("T", 30))
                    n_seeds = int(data.get("n_seeds", 50))
                    k_max = int(data.get("k_max", 5))
                    return jsonify(scan_convergence(N, T, n_seeds, k_max))

                existing = set(r.rule for r in app.url_map.iter_rules())
                for rule, ep, fn, methods in (
                    ("/lightcone/info",          "lc_info",   _info,         ["GET"]),
                    ("/lightcone/closure",       "lc_clos",   _closure,      ["GET"]),
                    ("/lightcone/run",           "lc_run",    _run,          ["POST"]),
                    ("/lightcone/scan",          "lc_scan",   _scan,         ["POST"]),
                    ("/lightcone/convergence",   "lc_conv",   _convergence,  ["POST"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
                        routes_registered.append(f"{methods[0]} {rule}")
            except Exception as e:
                print(f"[CK Gen14] lightcone route registration failed: {e}")

    suffix = " (" + ", ".join(routes_registered) + ")" if routes_registered else ""
    print(f"[CK Gen14] lightcone: MOUNTED  discretized 1D ring sim, "
          f"4CPR vs propagation speed k{suffix}")
    return True


# ─── CLI smoke ────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 72)
    print("CK LIGHTCONE TOY SIM -- 4-core preservation vs propagation speed")
    print("=" * 72)
    print()

    # First: direct closure check
    print("Step 1: Is TSML closed on the 4-core?")
    cc = four_core_closure_check()
    print(f"  4-core members:   {cc['four_core_members']}")
    print(f"  TSML closed?      {cc['tsml_4core_closed']}")
    print(f"  Leaks:            {cc['n_leaks']}")
    if cc['leaks']:
        for leak in cc['leaks']:
            print(f"    {leak['pair']} → {leak['output']}")
    print()
    print(f"  Closure table:")
    for k, v in sorted(cc['closure_table_4x4'].items()):
        print(f"    TSML{k} = {v}")
    print()

    # Speed scan
    print("Step 2: Speed scan -- 4CPR after T steps, averaged over seeds")
    print()
    print("Setup: N=30 cells, T=20 steps, 50 seeds per k, initial state in 4-core")
    print()
    sc = scan_speeds(N=30, T=20, n_seeds=50, k_max=5, seed=42)
    print(f"  {'k':>3}  {'fcp@t=1':>9}  {'fcp@t=5':>9}  {'fcp@t=10':>10}  {'fcp@t=T':>9}  {'final_std':>9}")
    sep3 = "-" * 3; sep9 = "-" * 9
    print(f"  {sep3}  {sep9}  {sep9}  ----------  {sep9}  ---------")
    for r in sc['results']:
        fcp_t = r['fcp_at_t']
        print(f"  {r['k']:>3}  "
              f"{fcp_t.get(1, '-'):>9.4f}  "
              f"{fcp_t.get(5, '-'):>9.4f}  "
              f"{fcp_t.get(10, '-'):>10.4f}  "
              f"{r['final_fcp_mean']:>9.4f}  "
              f"{r['final_fcp_std']:>9.4f}")
    print()
    print("Step 2 interpretation:")
    print("  - 4-core stays invariant under ALL k (because TSML is closed")
    print("    on the 4-core: any TSML[a,b] with a,b ∈ 4-core is in 4-core).")
    print("  - This FALSIFIES the simplest c-emergence reading.  The 4-core's")
    print("    closure means no specific k is privileged for staying-in-4-core.")
    print()
    print("Step 3: Convergence scan -- start from RANDOM (mix of all 10 ops)")
    print("        and measure how fast each k drives the lattice INTO the 4-core")
    print()
    print("Setup: N=30 cells, T=30 steps, 50 seeds per k, random uniform initial")
    print()
    cv = scan_convergence(N=30, T=30, n_seeds=50, k_max=5, seed=42)
    print(f"  {'k':>3}  {'conv_rate':>10}  {'mean_t':>8}  {'fcp@1':>7}  {'fcp@5':>7}  {'fcp@10':>8}  {'fcp@T':>7}")
    print(f"  {'-'*3}  {'-'*10}  {'-'*8}  {'-'*7}  {'-'*7}  {'-'*8}  {'-'*7}")
    for r in cv['results']:
        fcp_t = r['fcp_at_t']
        mt = r['mean_convergence_time']
        mt_str = f"{mt:.2f}" if mt is not None else "  --  "
        print(f"  {r['k']:>3}  "
              f"{r['convergence_rate']:>10.4f}  "
              f"{mt_str:>8}  "
              f"{fcp_t.get(1, 0):>7.4f}  "
              f"{fcp_t.get(5, 0):>7.4f}  "
              f"{fcp_t.get(10, 0):>8.4f}  "
              f"{fcp_t.get(30, 0):>7.4f}")
    print()
    print("Step 3 interpretation:")
    print("  - convergence_rate = fraction of random initials that hit 4CPR ≈ 1")
    print("    within T steps.")
    print("  - mean_t = average steps to convergence (when it happens).")
    print("  - Look for: a SPECIFIC k where convergence is fastest.")
    print("    If k=1 (unit speed) dominates, that's the natural rate.")
    print("    If all k converge similarly, no preferred speed emerges.")
    print()
    print("HONEST FALSIFIABILITY VERDICT:")
    print("  Step 2 shows the 4-core IS closed (good).  Step 3 measures whether")
    print("  any propagation speed is PRIVILEGED for pulling outside states INTO")
    print("  the attractor.  Read the results above to see if c-emergence")
    print("  survives at this toy level.")
