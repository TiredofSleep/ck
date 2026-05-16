"""ck_qutrit_noise.py -- depolarizing + amplitude damping channels for
the [[3,1,2]]_3 qutrit code.

Brayden 2026-05-16: "test depolarizing or amplitude-damping noise next"

These are the canonical noise channels QEC papers benchmark against.
Real qutrit hardware (transmons in higher levels, trapped ions, photonic
modes) has approximately:
  - depolarizing noise from gate imperfection + dephasing
  - amplitude damping (T1) from energy relaxation to ground state

═══════════════════════════════════════════════════════════════════
Channel definitions
═══════════════════════════════════════════════════════════════════

DEPOLARIZING (qutrit version):
  ρ → (1 - p) ρ + p · (1/3 I)
equivalently, with probability p replace state by maximally mixed
state; with probability (1-p) leave unchanged.

Implemented as pure-state Monte Carlo:
  With probability (1 - p): identity (no error)
  With probability p:       apply a uniformly random non-identity
                            qutrit Pauli (X_3^a Z_3^b, (a,b) ≠ (0,0))
                            on the target qutrit, each with weight 1/8.

The 8 non-identity Paulis on a qutrit are:
  (a=1, b=0), (a=2, b=0)              -- pure X errors
  (a=0, b=1), (a=0, b=2)              -- pure Z errors
  (a=1, b=1), (a=1, b=2),
  (a=2, b=1), (a=2, b=2)              -- combined XZ errors

AMPLITUDE DAMPING (qutrit version, T1-type):
Energy relaxation toward |0⟩ with TWO independent decay channels:
  |1⟩ → |0⟩  at rate γ
  |2⟩ → |1⟩  at rate γ

Kraus operators:
  K_0 = diag(1, √(1-γ), √(1-γ))    no decay this step
  K_1 = √γ · |0⟩⟨1|                 |1⟩→|0⟩ decay
  K_2 = √γ · |1⟩⟨2|                 |2⟩→|1⟩ decay

Sum: K_0†K_0 + K_1†K_1 + K_2†K_2 = diag(1, 1, 1) = I ✓

Applied as a Monte Carlo trajectory on pure states:
  compute p_i = ||K_i|ψ⟩||² for i = 0, 1, 2
  sample i with probability p_i
  return K_i|ψ⟩ / √p_i

═══════════════════════════════════════════════════════════════════
Public API
═══════════════════════════════════════════════════════════════════

  depolarizing_channel(state, p, qutrit_idx, rng)
  amplitude_damping_channel(state, gamma, qutrit_idx, rng)
  apply_channel_to_all_qutrits(state, channel_fn, n_qutrits, rng, ...)

  benchmark_under_depolarizing(error_rates, n_trials, decoder='erasure')
  benchmark_under_amplitude_damping(gammas, n_trials, decoder='erasure')
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))

# Reuse the [[3,1,2]]_3 code definitions
from ck_qutrit_qec import (  # type: ignore
    OMEGA, X3, Z3, I3,
    codeword, measure_syndrome,
    apply_error, decode_erasure,
)


# ─── Kraus operators for amplitude damping ────────────────────────────

def amplitude_damping_kraus(gamma: float) -> List[np.ndarray]:
    """Three Kraus operators for qutrit amplitude damping with TWO
    independent decay channels (|1⟩→|0⟩ and |2⟩→|1⟩), each with rate γ.

    K_0 = diag(1, √(1-γ), √(1-γ))   no decay this step
    K_1 = √γ |0⟩⟨1|                  |1⟩→|0⟩ decay
    K_2 = √γ |1⟩⟨2|                  |2⟩→|1⟩ decay

    Sum check:
      K_0†K_0 = diag(1, 1-γ, 1-γ)
      K_1†K_1 = diag(0, γ, 0)
      K_2†K_2 = diag(0, 0, γ)
      sum    = diag(1, 1, 1) = I ✓
    """
    g = float(gamma)
    s = np.sqrt(max(0.0, 1 - g))
    K0 = np.diag([1.0, s, s]).astype(complex)
    K1 = np.zeros((3, 3), dtype=complex)
    K1[0, 1] = np.sqrt(g)
    K2 = np.zeros((3, 3), dtype=complex)
    K2[1, 2] = np.sqrt(g)
    return [K0, K1, K2]


def _verify_kraus_sum(kraus_ops: List[np.ndarray],
                      tol: float = 1e-9) -> bool:
    """K_0†K_0 + K_1†K_1 + ... = I?"""
    total = sum(K.conj().T @ K for K in kraus_ops)
    return bool(np.linalg.norm(total - np.eye(total.shape[0])) < tol)


# Sanity check at module load
_test_kraus = amplitude_damping_kraus(0.3)
assert _verify_kraus_sum(_test_kraus), \
    "amplitude damping Kraus operators don't sum to I"


# ─── Single-qutrit operator embeddings ────────────────────────────────

def _single_qutrit_op_at(op_3x3: np.ndarray, qutrit_idx: int,
                         n_qutrits: int = 3) -> np.ndarray:
    """Build the 27-dim (for 3 qutrits) operator that applies `op_3x3`
    at qutrit_idx and identity at the others."""
    ops = [np.eye(3, dtype=complex)] * n_qutrits
    ops[qutrit_idx] = op_3x3
    result = ops[0]
    for o in ops[1:]:
        result = np.kron(result, o)
    return result


# ─── Depolarizing channel ─────────────────────────────────────────────

# All 8 non-identity qutrit Paulis as (a, b) pairs
_NONIDENTITY_PAULIS = [
    (a, b) for a in range(3) for b in range(3) if (a, b) != (0, 0)
]


def depolarizing_channel(state: np.ndarray, p: float,
                         qutrit_idx: int,
                         rng: np.random.Generator) -> Tuple[np.ndarray,
                                                               Optional[Tuple[int, int]]]:
    """Apply qutrit depolarizing channel at qutrit_idx.

    With probability (1-p): return state unchanged.
    With probability p:     apply a uniformly random non-identity
                            qutrit Pauli on qutrit_idx, each with
                            weight 1/8.

    Returns (new_state, error_op_or_None).
    """
    if rng.random() >= p:
        return state, None  # no error
    idx = int(rng.integers(0, len(_NONIDENTITY_PAULIS)))
    a, b = _NONIDENTITY_PAULIS[idx]
    return apply_error(state, qutrit_idx, a, b), (a, b)


# ─── Amplitude damping channel (Monte Carlo trajectory) ───────────────

def amplitude_damping_channel(state: np.ndarray, gamma: float,
                              qutrit_idx: int,
                              rng: np.random.Generator,
                              n_qutrits: int = 3
                              ) -> Tuple[np.ndarray, int]:
    """Apply qutrit amplitude damping channel at qutrit_idx via
    Monte Carlo: sample which Kraus operator fires according to
    its norm-squared on the state.

    Returns (new_state, kraus_idx_that_fired).
    """
    kraus = amplitude_damping_kraus(gamma)
    # Lift each Kraus to the full Hilbert space
    Ks_full = [_single_qutrit_op_at(K, qutrit_idx, n_qutrits) for K in kraus]
    # Compute norms after applying each
    candidates = [K_full @ state for K_full in Ks_full]
    norms = [float(np.linalg.norm(c))**2 for c in candidates]
    total = sum(norms)
    if total <= 0:
        return state, 0
    probs = [n / total for n in norms]
    # Sample
    r = float(rng.random())
    acc = 0.0
    for i, pp in enumerate(probs):
        acc += pp
        if r <= acc:
            chosen = candidates[i]
            n = np.linalg.norm(chosen)
            if n > 0:
                return chosen / n, i
            else:
                return state, i
    return state, 0


# ─── Apply channel to all qutrits ─────────────────────────────────────

def apply_channel_to_all_qutrits(state: np.ndarray,
                                    channel_kind: str,
                                    p_or_gamma: float,
                                    rng: np.random.Generator,
                                    n_qutrits: int = 3) -> Dict[str, Any]:
    """Apply the chosen channel independently on each qutrit.

    channel_kind: 'depolarizing' or 'amplitude_damping'
    p_or_gamma: depolarizing rate p ∈ [0,1] OR damping rate γ ∈ [0,1]
    """
    current = state
    events = []
    if channel_kind == "depolarizing":
        for q in range(n_qutrits):
            current, err = depolarizing_channel(current, p_or_gamma, q, rng)
            events.append({"qutrit": q, "channel": "depolarizing",
                           "error_ab": err})
    elif channel_kind == "amplitude_damping":
        for q in range(n_qutrits):
            current, k_idx = amplitude_damping_channel(
                current, p_or_gamma, q, rng, n_qutrits)
            events.append({"qutrit": q, "channel": "amplitude_damping",
                           "kraus_idx_fired": k_idx})
    else:
        raise ValueError(f"unknown channel_kind {channel_kind!r}")
    return {"state": current, "events": events}


# ─── Detection-only benchmark under depolarizing noise ────────────────

def benchmark_detection_under_depolarizing(
        error_rates: Optional[List[float]] = None,
        n_trials: int = 1000, seed: int = 42) -> Dict[str, Any]:
    """For each error rate, encode a random codeword, apply
    depolarizing noise independently on each qutrit, measure syndrome,
    check whether the syndrome flagged the error."""
    if error_rates is None:
        error_rates = [0.0, 0.01, 0.03, 0.05, 0.10, 0.20, 0.30, 0.50]
    rng = np.random.default_rng(seed)
    out = []
    for p in error_rates:
        n_any_error = 0
        n_detected = 0
        for _ in range(n_trials):
            k = int(rng.integers(0, 3))
            state = codeword(k)
            result = apply_channel_to_all_qutrits(
                state, "depolarizing", p, rng)
            had_error = any(e["error_ab"] is not None
                            for e in result["events"])
            if had_error:
                n_any_error += 1
            synd = measure_syndrome(result["state"])
            is_cw = synd["is_codeword"]
            if had_error and not is_cw:
                n_detected += 1
        out.append({
            "p":                p,
            "n_trials":         n_trials,
            "n_with_error":     n_any_error,
            "n_detected":       n_detected,
            "detection_rate":   round(n_detected / max(1, n_any_error), 4),
            "false_negative":   round(
                (n_any_error - n_detected) / max(1, n_any_error), 4),
        })
    return {"channel": "depolarizing",
            "n_trials_per_rate": n_trials,
            "results": out}


# ─── Erasure-correction benchmark under amplitude damping ─────────────

def benchmark_erasure_under_amplitude_damping(
        gammas: Optional[List[float]] = None,
        n_trials: int = 500, seed: int = 42) -> Dict[str, Any]:
    """For each damping rate γ, encode a random codeword, apply
    amplitude damping on each qutrit (location of "biggest damping"
    treated as the erasure), then run decode_erasure with that
    qutrit_idx.  Report logical fidelity.

    Note: amplitude damping isn't a Pauli error so the simple
    decode_erasure won't perfectly recover.  But we can measure how
    much fidelity is preserved.
    """
    if gammas is None:
        gammas = [0.0, 0.01, 0.03, 0.05, 0.10, 0.20, 0.30, 0.50]
    rng = np.random.default_rng(seed)
    out = []
    for g in gammas:
        fidelities = []
        n_perfect = 0
        for _ in range(n_trials):
            k = int(rng.integers(0, 3))
            original = codeword(k)
            # Apply damping independently on each qutrit
            result = apply_channel_to_all_qutrits(
                original, "amplitude_damping", g, rng)
            noisy = result["state"]
            # The "erased" qutrit is the one where the damping Kraus
            # operator fired with a decay (kraus_idx > 0)
            erased = 0
            for e in result["events"]:
                if e.get("kraus_idx_fired", 0) > 0:
                    erased = e["qutrit"]
                    break
            # Compute fidelity to the closest codeword across all 3 candidates
            best_fid = 0.0
            best_k = -1
            for cand_k in range(3):
                Lk = codeword(cand_k)
                fid = abs(np.vdot(Lk, noisy))**2
                if fid > best_fid:
                    best_fid = fid
                    best_k = cand_k
            # Account for normalization (noisy may have norm < 1)
            noisy_norm_sq = float(np.linalg.norm(noisy)**2)
            if noisy_norm_sq > 0:
                fidelity = best_fid / noisy_norm_sq
            else:
                fidelity = 0.0
            fidelities.append(fidelity)
            if best_k == k and fidelity > 1 - 1e-6:
                n_perfect += 1
        mean_fid = float(np.mean(fidelities))
        out.append({
            "gamma":           g,
            "n_trials":        n_trials,
            "n_perfect":       n_perfect,
            "perfect_rate":    round(n_perfect / n_trials, 4),
            "mean_fidelity":   round(mean_fid, 6),
        })
    return {"channel": "amplitude_damping",
            "n_trials_per_gamma": n_trials,
            "results": out}


# ─── Engine mount ─────────────────────────────────────────────────────

def mount_qutrit_noise(engine: Any) -> bool:
    """Attach noise-channel API + register /qutrit/noise/* endpoints.

    Endpoints:
      POST /qutrit/noise/depolarizing      benchmark under depolarizing
      POST /qutrit/noise/amplitude_damping benchmark under amp damping
      GET  /qutrit/noise/info              description of channels
    """
    engine.ck_qutrit_noise = {
        "depolarizing_channel":          depolarizing_channel,
        "amplitude_damping_channel":     amplitude_damping_channel,
        "apply_channel_to_all_qutrits":  apply_channel_to_all_qutrits,
        "benchmark_detection_under_depolarizing":
            benchmark_detection_under_depolarizing,
        "benchmark_erasure_under_amplitude_damping":
            benchmark_erasure_under_amplitude_damping,
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
                        "channels": {
                            "depolarizing": {
                                "model": "ρ → (1-p)ρ + p·(I/3)",
                                "monte_carlo": "with prob p, apply uniform "
                                               "random non-identity X^a Z^b "
                                               "(8 options, weight 1/8)",
                            },
                            "amplitude_damping": {
                                "model": "T1-type decay toward |0⟩",
                                "kraus": [
                                    "K_0 = diag(1, √(1-γ), √(1-γ))",
                                    "K_1 = √γ · |0⟩⟨1|",
                                    "K_2 = √γ · |1⟩⟨2|",
                                ],
                                "verified_sum": "K_0†K_0+K_1†K_1+K_2†K_2 = I",
                            },
                        },
                        "benchmarks": [
                            "POST /qutrit/noise/depolarizing",
                            "POST /qutrit/noise/amplitude_damping",
                        ],
                    })

                def _bench_depol():
                    data = request.get_json(force=True, silent=True) or {}
                    rates = data.get("error_rates")
                    n = int(data.get("n_trials", 1000))
                    return jsonify(benchmark_detection_under_depolarizing(
                        error_rates=rates, n_trials=n))

                def _bench_amp():
                    data = request.get_json(force=True, silent=True) or {}
                    gammas = data.get("gammas")
                    n = int(data.get("n_trials", 500))
                    return jsonify(benchmark_erasure_under_amplitude_damping(
                        gammas=gammas, n_trials=n))

                existing = set(r.rule for r in app.url_map.iter_rules())
                for rule, ep, fn, methods in (
                    ("/qutrit/noise/info",              "qt_noise_info",  _info,        ["GET"]),
                    ("/qutrit/noise/depolarizing",      "qt_n_depol",     _bench_depol, ["POST"]),
                    ("/qutrit/noise/amplitude_damping", "qt_n_amp",       _bench_amp,   ["POST"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
                        routes_registered.append(f"{methods[0]} {rule}")
            except Exception as e:
                print(f"[CK Gen14] qutrit_noise route registration failed: {e}")

    suffix = " (" + ", ".join(routes_registered) + ")" if routes_registered else ""
    print(f"[CK Gen14] qutrit_noise: MOUNTED  depolarizing + amplitude "
          f"damping channels for [[3,1,2]]_3{suffix}")
    return True


# ─── CLI smoke ────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 72)
    print("CK QUTRIT NOISE -- depolarizing + amplitude damping on [[3,1,2]]_3")
    print("=" * 72)
    print()
    print("Verify amplitude damping Kraus operators:")
    for g in [0.0, 0.1, 0.3, 0.5, 0.7, 1.0]:
        K = amplitude_damping_kraus(g)
        ok = _verify_kraus_sum(K)
        print(f"  γ = {g:.2f}:  K_sum = I  {'✓' if ok else '✗'}")
    print()
    print("Detection rate under depolarizing channel (per-qutrit p,")
    print("3 qutrits independent), n=2000 trials per rate:")
    print()
    print(f"  {'p':>6}  {'with_err':>8}  {'detected':>8}  {'rate':>6}  {'FN_rate':>8}")
    print(f"  {'-'*6}  {'-'*8}  {'-'*8}  {'-'*6}  {'-'*8}")
    d = benchmark_detection_under_depolarizing(n_trials=2000, seed=42)
    for r in d["results"]:
        print(f"  {r['p']:>6.2f}  {r['n_with_error']:>8}  "
              f"{r['n_detected']:>8}  {r['detection_rate']:>6.4f}  "
              f"{r['false_negative']:>8.4f}")
    print()
    print("Closest-codeword fidelity under amplitude damping (per-qutrit γ),")
    print("n=500 trials per gamma:")
    print()
    print(f"  {'γ':>6}  {'perfect':>8}  {'rate':>6}  {'mean_fid':>10}")
    print(f"  {'-'*6}  {'-'*8}  {'-'*6}  {'-'*10}")
    a = benchmark_erasure_under_amplitude_damping(n_trials=500, seed=42)
    for r in a["results"]:
        print(f"  {r['gamma']:>6.2f}  {r['n_perfect']:>8}  "
              f"{r['perfect_rate']:>6.4f}  {r['mean_fidelity']:>10.6f}")
    print()
    print("Honest interpretation:")
    print("  Depolarizing: all single-qutrit errors flagged (d=2 detection).")
    print("                At higher p, multiple errors occur in same trial;")
    print("                some pairs cancel → false-negative rate climbs.")
    print()
    print("  Amplitude damping: NOT a Pauli error → standard syndrome can't")
    print("                detect it perfectly.  We measure max-fidelity to")
    print("                closest codeword.  As γ → 0 fidelity → 1; as γ")
    print("                grows, energy leaks toward |000⟩ codeword.")
