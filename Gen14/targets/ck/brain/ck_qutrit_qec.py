"""ck_qutrit_qec.py -- [[3,1,2]]_3 qutrit stabilizer code, full quantum sim.

Brayden 2026-05-16 (Grok-suggested target):
  "The [[3,1,2]]_3 is a perfect 'hello world' for CK... the smallest
   nontrivial qutrit stabilizer code and a quantum MDS code that
   saturates the quantum Singleton bound."

This is a TRUE quantum simulator (complex amplitudes over the
27-dim three-qutrit Hilbert space), not a classical magma code.

═══════════════════════════════════════════════════════════════════
The code
═══════════════════════════════════════════════════════════════════

  Parameters:     [[n=3, k=1, d=2]]_3
  Physical:       3 qutrits, dim(H) = 3^3 = 27
  Logical:        1 qutrit (3 logical basis states)
  Distance:       2 (detects any single-qutrit error;
                   erasure-correctable; not arbitrary-error correctable)
  Stabilizers:    XXX = X_3 ⊗ X_3 ⊗ X_3   (X_3 = cyclic shift +1 mod 3)
                  ZZZ = Z_3 ⊗ Z_3 ⊗ Z_3   (Z_3 = phase diag(1, ω, ω²))

  ω = e^(2πi/3), the primitive cube root of unity.

  Logical codewords (Grok's exact form, verified):
    |L0⟩ = (1/√3)(|000⟩ + |111⟩ + |222⟩)
    |L1⟩ = (1/√3)(|012⟩ + |120⟩ + |201⟩)
    |L2⟩ = (1/√3)(|021⟩ + |102⟩ + |210⟩)

  Quick proof of stabilization:
    ZZZ|abc⟩ = ω^(a+b+c) |abc⟩.  All terms in each codeword satisfy
              a+b+c ≡ 0 mod 3 → eigenvalue +1.  ✓
    XXX|abc⟩ = |(a+1)(b+1)(c+1)⟩.  Each codeword is a sum of
              cyclic-shift orbits under "shift all by 1" → +1
              eigenvalue.  ✓

═══════════════════════════════════════════════════════════════════
Error model
═══════════════════════════════════════════════════════════════════

  Single-qutrit error = X_3^a · Z_3^b on one of the 3 qutrits,
  with (a, b) ∈ {0..2}² and not (0,0).  8 single-qutrit error types
  per qutrit × 3 qutrits = 24 error operators (plus identity).

  Effect on syndrome (computed by conjugation phase):
    X_3^a on qutrit i:  ZZZ-eigenvalue → ω^a  (X-error detected by Z-stabilizer)
    Z_3^b on qutrit i:  XXX-eigenvalue → ω^b  (Z-error detected by X-stabilizer)

  Crucially the SYNDROME does NOT distinguish WHICH qutrit was hit
  (the syndrome only depends on the TOTAL X-shift and TOTAL Z-shift).
  That's why d=2 detects-but-doesn't-correct arbitrary single errors.

═══════════════════════════════════════════════════════════════════
What this module proves
═══════════════════════════════════════════════════════════════════

  - Codewords are exact (+1) eigenstates of both stabilizers.
  - Logical Paulis X_L, Z_L cycle and phase the codewords.
  - Any single-qutrit Pauli error produces a non-zero syndrome.
  - For erasure errors (location known), recovery is exact.
  - Honest negative: for arbitrary single errors, location-ambiguity
    means correction is non-deterministic.

═══════════════════════════════════════════════════════════════════
Public API
═══════════════════════════════════════════════════════════════════

  codeword(k)                       k ∈ {0,1,2} → 27-dim state vector
  apply_error(state, qutrit_idx, a, b)
                                    apply X_3^a Z_3^b at qutrit_idx
  measure_syndrome(state)           → (xxx_eigenvalue, zzz_eigenvalue)
                                       both ∈ {1, ω, ω²}
  decode_erasure(state, erased_idx) recover when erasure location known
  benchmark_detection(n_trials, error_prob)
                                    measure detection rate empirically

  mount_qutrit_qec(engine)          attach engine.ck_qutrit_qec + /qutrit/*
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))


# ─── Single-qutrit operators ──────────────────────────────────────────

# omega = primitive cube root of unity
OMEGA = np.exp(2j * np.pi / 3)

# Single-qutrit Paulis (3×3 complex)
I3 = np.eye(3, dtype=complex)
X3 = np.array([[0, 0, 1],
               [1, 0, 0],
               [0, 1, 0]], dtype=complex)  # cyclic shift +1
Z3 = np.diag([1, OMEGA, OMEGA**2]).astype(complex)  # phase

# Weyl commutation: Z_3 X_3 = ω X_3 Z_3  (equivalently X_3 Z_3 = ω⁻¹ Z_3 X_3)
# Verified: with X_3 = shift-up, the X|k⟩=|k+1⟩ picks up the phase
# ω^k from Z_3 applied first, so X·Z|k⟩ = ω^k|k+1⟩ while Z·X|k⟩ = ω^(k+1)|k+1⟩.
assert np.allclose(Z3 @ X3, OMEGA * X3 @ Z3), \
    "qutrit Weyl commutation failed"


def _kron3(A: np.ndarray, B: np.ndarray, C: np.ndarray) -> np.ndarray:
    return np.kron(np.kron(A, B), C)


# Stabilizers
XXX = _kron3(X3, X3, X3)
ZZZ = _kron3(Z3, Z3, Z3)


def _basis(i: int, j: int, k: int) -> np.ndarray:
    """27-dim basis state |ijk⟩ with i,j,k ∈ {0,1,2}."""
    v = np.zeros(27, dtype=complex)
    v[9 * i + 3 * j + k] = 1.0
    return v


# ─── Logical codewords ────────────────────────────────────────────────

def codeword(k: int) -> np.ndarray:
    """Return |L_k⟩ as a 27-dim normalized state vector.

    |L0⟩ = (1/√3)(|000⟩ + |111⟩ + |222⟩)
    |L1⟩ = (1/√3)(|012⟩ + |120⟩ + |201⟩)
    |L2⟩ = (1/√3)(|021⟩ + |102⟩ + |210⟩)
    """
    k = int(k) % 3
    s = 1.0 / np.sqrt(3.0)
    if k == 0:
        return s * (_basis(0, 0, 0) + _basis(1, 1, 1) + _basis(2, 2, 2))
    if k == 1:
        return s * (_basis(0, 1, 2) + _basis(1, 2, 0) + _basis(2, 0, 1))
    return s * (_basis(0, 2, 1) + _basis(1, 0, 2) + _basis(2, 1, 0))


# ─── Verify the code (run at module load) ─────────────────────────────

def _verify_code() -> Dict[str, Any]:
    """Confirm stabilizers fix the codewords and codewords are
    orthonormal.  Returns a dict of measured values for /qutrit/info."""
    out = {}
    for k in range(3):
        v = codeword(k)
        xxx_v = XXX @ v
        zzz_v = ZZZ @ v
        out[f"L{k}_norm"] = float(np.linalg.norm(v))
        out[f"L{k}_xxx_residual"] = float(np.linalg.norm(xxx_v - v))
        out[f"L{k}_zzz_residual"] = float(np.linalg.norm(zzz_v - v))
    # Orthonormality
    for i in range(3):
        for j in range(i + 1, 3):
            ip = np.vdot(codeword(i), codeword(j))
            out[f"<L{i}|L{j}>"] = complex(ip).real, complex(ip).imag
    out["XXX_ZZZ_commute_residual"] = float(
        np.linalg.norm(XXX @ ZZZ - ZZZ @ XXX)
    )
    return out


_VERIFICATION = _verify_code()
# Sanity: all residuals < 1e-10
for k in range(3):
    assert _VERIFICATION[f"L{k}_xxx_residual"] < 1e-10, \
        f"L{k} not stabilized by XXX (residual {_VERIFICATION[f'L{k}_xxx_residual']})"
    assert _VERIFICATION[f"L{k}_zzz_residual"] < 1e-10, \
        f"L{k} not stabilized by ZZZ"


# ─── Error application ────────────────────────────────────────────────

def _single_qutrit_op_at(qutrit_idx: int, op: np.ndarray) -> np.ndarray:
    """3-qutrit operator that applies `op` at qutrit_idx and I elsewhere."""
    ops = [I3, I3, I3]
    ops[qutrit_idx] = op
    return _kron3(*ops)


def apply_error(state: np.ndarray, qutrit_idx: int,
                a: int, b: int) -> np.ndarray:
    """Apply the error X_3^a · Z_3^b at qutrit_idx to the state.

    qutrit_idx ∈ {0, 1, 2}
    a, b ∈ {0, 1, 2}  (powers; 0 means no error in that channel)
    """
    a = int(a) % 3
    b = int(b) % 3
    if a == 0 and b == 0:
        return state.copy()
    error_op = (np.linalg.matrix_power(X3, a)
                @ np.linalg.matrix_power(Z3, b))
    full_op = _single_qutrit_op_at(qutrit_idx, error_op)
    return full_op @ state


# ─── Syndrome measurement ─────────────────────────────────────────────

def _eigenvalue_class(z: complex, tol: float = 1e-6) -> int:
    """Map a unit-modulus complex z to its closest cube-root class:
    0 if z ≈ 1, 1 if z ≈ ω, 2 if z ≈ ω²."""
    omegas = [1.0 + 0j, OMEGA, OMEGA**2]
    diffs = [abs(z - w) for w in omegas]
    return int(np.argmin(diffs))


def measure_syndrome(state: np.ndarray) -> Dict[str, Any]:
    """Compute the XXX and ZZZ eigenvalues of the state.

    Returns:
      xxx_eigenvalue (complex), zzz_eigenvalue (complex)
      xxx_class, zzz_class    ∈ {0, 1, 2} (the cube-root class)
      is_codeword             True if both eigenvalues are +1

    NOTE: This assumes the state is an eigenstate of the stabilizers
    (which it will be IF the error was a Pauli).  For superpositions,
    measure_syndrome returns the expectation values (not projective
    syndromes).
    """
    if np.allclose(np.linalg.norm(state), 0):
        return {"error": "zero state"}
    xxx_exp = complex(np.vdot(state, XXX @ state))
    zzz_exp = complex(np.vdot(state, ZZZ @ state))
    return {
        "xxx_eigenvalue":  (xxx_exp.real, xxx_exp.imag),
        "zzz_eigenvalue":  (zzz_exp.real, zzz_exp.imag),
        "xxx_class":       _eigenvalue_class(xxx_exp),
        "zzz_class":       _eigenvalue_class(zzz_exp),
        "is_codeword":     (_eigenvalue_class(xxx_exp) == 0
                              and _eigenvalue_class(zzz_exp) == 0),
    }


# ─── Erasure decoder ──────────────────────────────────────────────────

def decode_erasure(state: np.ndarray, erased_idx: int,
                   tol: float = 1e-6) -> Dict[str, Any]:
    """Recover the logical codeword from a state with a KNOWN erasure
    location.  Distance-2 code → erasure-correctable.

    Strategy: project state onto each codeword |L_k⟩ and report the
    one with largest overlap.  Since erasure means we know SOMETHING
    happened at qutrit_idx, we can search over X_3^a · Z_3^b at
    erased_idx for the recovery that maximizes |⟨L_k|recovered⟩|.
    """
    best_k = -1
    best_a = 0
    best_b = 0
    best_overlap = 0.0
    for k in range(3):
        Lk = codeword(k)
        for a in range(3):
            for b in range(3):
                # Try recovery = (X^a Z^b)^† on erased qutrit
                # = Z^(-b) X^(-a) = Z^(3-b mod 3) · X^(3-a mod 3)
                recovery = (np.linalg.matrix_power(Z3, (3 - b) % 3)
                            @ np.linalg.matrix_power(X3, (3 - a) % 3))
                recovered = _single_qutrit_op_at(erased_idx, recovery) @ state
                overlap = abs(np.vdot(Lk, recovered))**2
                if overlap > best_overlap:
                    best_overlap = overlap
                    best_k = k
                    best_a = a
                    best_b = b
    return {
        "recovered_logical_k":  best_k,
        "recovered_codeword":   f"L{best_k}",
        "recovery_a":           best_a,
        "recovery_b":           best_b,
        "recovery_label":       f"X_3^{best_a} · Z_3^{best_b}"
                                  if (best_a, best_b) != (0, 0)
                                  else "I (no recovery)",
        "fidelity":             round(best_overlap, 6),
    }


# ─── Benchmark ────────────────────────────────────────────────────────

def benchmark_detection(n_trials: int = 2000,
                        error_prob: float = 0.3,
                        seed: int = 42) -> Dict[str, Any]:
    """Empirical detection rate: encode a random codeword, apply a
    random single-qutrit error with probability error_prob, measure
    syndrome.  Report fraction where the syndrome correctly flagged
    the error (vs. false negative)."""
    rng = np.random.default_rng(seed)
    n_correct_detect = 0
    n_false_negative = 0
    n_correct_no_error = 0
    n_false_positive = 0
    n_errors_actual = 0
    n_no_errors_actual = 0
    for _ in range(n_trials):
        k = int(rng.integers(0, 3))
        state = codeword(k)
        # Inject error with probability error_prob
        had_error = bool(rng.random() < error_prob)
        if had_error:
            qubit = int(rng.integers(0, 3))
            a = int(rng.integers(0, 3))
            b = int(rng.integers(0, 3))
            if a == 0 and b == 0:
                # No-op error; treat as no error
                had_error = False
            else:
                state = apply_error(state, qubit, a, b)
        if had_error:
            n_errors_actual += 1
        else:
            n_no_errors_actual += 1
        synd = measure_syndrome(state)
        is_cw = synd["is_codeword"]
        if had_error and not is_cw:
            n_correct_detect += 1
        elif had_error and is_cw:
            n_false_negative += 1
        elif (not had_error) and is_cw:
            n_correct_no_error += 1
        elif (not had_error) and (not is_cw):
            n_false_positive += 1
    return {
        "n_trials":            n_trials,
        "error_prob_target":   error_prob,
        "n_errors_actual":     n_errors_actual,
        "n_no_errors_actual":  n_no_errors_actual,
        "n_correct_detect":    n_correct_detect,
        "n_false_negative":    n_false_negative,
        "n_correct_no_error":  n_correct_no_error,
        "n_false_positive":    n_false_positive,
        "detection_rate":      round(n_correct_detect / max(1, n_errors_actual), 4),
        "false_negative_rate": round(n_false_negative / max(1, n_errors_actual), 4),
        "true_negative_rate":  round(n_correct_no_error / max(1, n_no_errors_actual), 4),
    }


# ─── Erasure correction benchmark ─────────────────────────────────────

def benchmark_erasure_correction(n_trials: int = 1000,
                                   seed: int = 42) -> Dict[str, Any]:
    """Encode a random codeword, apply random single-qutrit Pauli at
    a random qutrit, then ERASURE-decode with the location KNOWN.
    Report fidelity with original codeword.  Distance-2 code →
    erasure-correctable."""
    rng = np.random.default_rng(seed)
    n_perfect = 0
    n_imperfect = 0
    fidelities = []
    for _ in range(n_trials):
        k = int(rng.integers(0, 3))
        original = codeword(k)
        qubit = int(rng.integers(0, 3))
        a = int(rng.integers(0, 3))
        b = int(rng.integers(0, 3))
        noisy = apply_error(original, qubit, a, b)
        result = decode_erasure(noisy, qubit)
        if result["recovered_logical_k"] == k and result["fidelity"] > 1 - 1e-6:
            n_perfect += 1
        else:
            n_imperfect += 1
        fidelities.append(result["fidelity"])
    return {
        "n_trials":             n_trials,
        "n_perfect_recovery":   n_perfect,
        "n_imperfect_recovery": n_imperfect,
        "perfect_rate":         round(n_perfect / n_trials, 4),
        "mean_fidelity":        round(float(np.mean(fidelities)), 6),
    }


# ─── Engine mount ─────────────────────────────────────────────────────

def mount_qutrit_qec(engine: Any) -> bool:
    """Attach the qutrit QEC API + register /qutrit/* endpoints.

    Endpoints:
      GET   /qutrit/info               code parameters + verification
      POST  /qutrit/encode             {"k": 0|1|2} → codeword amplitudes
      POST  /qutrit/syndrome           {"state": [27 complex]} → syndrome
      POST  /qutrit/inject_error       {"k": int, "qutrit": int, "a": int, "b": int}
      POST  /qutrit/decode_erasure     {"state": [...], "erased_idx": int}
      POST  /qutrit/benchmark_detection
      POST  /qutrit/benchmark_erasure
    """
    engine.ck_qutrit_qec = {
        "codeword":              codeword,
        "apply_error":           apply_error,
        "measure_syndrome":      measure_syndrome,
        "decode_erasure":        decode_erasure,
        "benchmark_detection":   benchmark_detection,
        "benchmark_erasure":     benchmark_erasure_correction,
        "verification":          _VERIFICATION,
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
                        "code": "[[3,1,2]]_3 qutrit CSS code",
                        "n": 3, "k": 1, "d": 2,
                        "physical_dim": 27,
                        "logical_dim": 3,
                        "stabilizers": ["XXX = X_3 ⊗ X_3 ⊗ X_3",
                                         "ZZZ = Z_3 ⊗ Z_3 ⊗ Z_3"],
                        "omega": "exp(2πi/3)",
                        "weyl_commutation": "Z_3 X_3 = ω X_3 Z_3  (equivalently X_3 Z_3 = ω⁻¹ Z_3 X_3)",
                        "logical_codewords": {
                            "L0": "(|000⟩ + |111⟩ + |222⟩)/√3",
                            "L1": "(|012⟩ + |120⟩ + |201⟩)/√3",
                            "L2": "(|021⟩ + |102⟩ + |210⟩)/√3",
                        },
                        "verification": {
                            k: (v if isinstance(v, (int, float, bool))
                                else str(v))
                            for k, v in _VERIFICATION.items()
                        },
                        "honest_scope": [
                            "Full quantum simulator (27-dim complex amplitudes)",
                            "Detects ANY single-qutrit Pauli error",
                            "Erasure-corrects when error location is known",
                            "Does NOT arbitrary-error-correct (d=2 only detects)",
                            "Saturates quantum Singleton bound (MDS code)",
                            "Per Grok 2026-05-16: minimal holographic"
                            " (AdS/CFT-2) and quantum-secret-sharing code",
                        ],
                    })

                def _encode():
                    data = request.get_json(force=True, silent=True) or {}
                    k = int(data.get("k", 0)) % 3
                    v = codeword(k)
                    return jsonify({
                        "k": k,
                        "codeword_name": f"L{k}",
                        "support": [
                            {"i": idx // 9, "j": (idx // 3) % 3,
                             "k_": idx % 3,
                             "amp_real": float(v[idx].real),
                             "amp_imag": float(v[idx].imag)}
                            for idx in range(27) if abs(v[idx]) > 1e-9
                        ],
                    })

                def _syndrome():
                    data = request.get_json(force=True, silent=True) or {}
                    k = int(data.get("k", 0))
                    qutrit = int(data.get("qutrit", 0))
                    a = int(data.get("a", 0))
                    b = int(data.get("b", 0))
                    state = codeword(k)
                    if (qutrit, a, b) != (0, 0, 0):
                        state = apply_error(state, qutrit, a, b)
                    return jsonify(measure_syndrome(state))

                def _inject():
                    data = request.get_json(force=True, silent=True) or {}
                    k = int(data.get("k", 0))
                    qutrit = int(data.get("qutrit", 0))
                    a = int(data.get("a", 0))
                    b = int(data.get("b", 0))
                    original = codeword(k)
                    noisy = apply_error(original, qutrit, a, b)
                    synd = measure_syndrome(noisy)
                    return jsonify({
                        "original_k": k,
                        "error": {"qutrit": qutrit, "a": a, "b": b,
                                  "label": f"X_3^{a} · Z_3^{b} on qutrit {qutrit}"},
                        "syndrome": synd,
                        "detected": not synd["is_codeword"],
                    })

                def _decode_erasure_view():
                    data = request.get_json(force=True, silent=True) or {}
                    # For convenience, accept (k, qutrit, a, b) to build
                    # the noisy state inline + erased_idx
                    k = int(data.get("k", 0))
                    qutrit = int(data.get("qutrit", 0))
                    a = int(data.get("a", 0))
                    b = int(data.get("b", 0))
                    erased = int(data.get("erased_idx", qutrit))
                    noisy = apply_error(codeword(k), qutrit, a, b)
                    result = decode_erasure(noisy, erased)
                    result["original_k"] = k
                    return jsonify(result)

                def _bench_detect():
                    data = request.get_json(force=True, silent=True) or {}
                    n = int(data.get("n_trials", 1000))
                    er = float(data.get("error_prob", 0.3))
                    return jsonify(benchmark_detection(n_trials=n,
                                                          error_prob=er))

                def _bench_erasure():
                    data = request.get_json(force=True, silent=True) or {}
                    n = int(data.get("n_trials", 500))
                    return jsonify(benchmark_erasure_correction(n_trials=n))

                existing = set(r.rule for r in app.url_map.iter_rules())
                for rule, ep, fn, methods in (
                    ("/qutrit/info",                 "qt_info",     _info,                  ["GET"]),
                    ("/qutrit/encode",                "qt_encode",   _encode,                ["POST"]),
                    ("/qutrit/syndrome",              "qt_synd",     _syndrome,              ["POST"]),
                    ("/qutrit/inject_error",          "qt_inject",   _inject,                ["POST"]),
                    ("/qutrit/decode_erasure",        "qt_decode",   _decode_erasure_view,   ["POST"]),
                    ("/qutrit/benchmark_detection",   "qt_b_det",    _bench_detect,          ["POST"]),
                    ("/qutrit/benchmark_erasure",     "qt_b_eras",   _bench_erasure,         ["POST"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
                        routes_registered.append(f"{methods[0]} {rule}")
            except Exception as e:
                print(f"[CK Gen14] qutrit_qec route registration failed: {e}")

    suffix = " (" + ", ".join(routes_registered) + ")" if routes_registered else ""
    print(f"[CK Gen14] qutrit_qec: MOUNTED  [[3,1,2]]_3 CSS code, "
          f"27-dim complex amplitudes{suffix}")
    return True


# ─── CLI smoke ────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 72)
    print("CK QUTRIT QEC -- [[3,1,2]]_3 full quantum simulator")
    print("=" * 72)
    print()
    print("Single-qutrit operators:")
    print(f"  X_3 = cyclic shift +1 mod 3 (real 3x3)")
    print(f"  Z_3 = diag(1, ω, ω²) with ω = exp(2πi/3)")
    print(f"  Weyl: Z_3 X_3 = ω X_3 Z_3  (residual {np.linalg.norm(Z3 @ X3 - OMEGA * X3 @ Z3):.2e})")
    print()
    print("Logical codewords (27-dim, sparse):")
    for k in range(3):
        v = codeword(k)
        support = [(idx // 9, (idx // 3) % 3, idx % 3)
                   for idx in range(27) if abs(v[idx]) > 1e-9]
        print(f"  |L{k}⟩ supports = {support}, "
              f"norm = {np.linalg.norm(v):.6f}")
    print()
    print("Stabilizer verification (XXX|Lk⟩ = |Lk⟩, ZZZ|Lk⟩ = |Lk⟩):")
    for k in range(3):
        v = codeword(k)
        x_res = float(np.linalg.norm(XXX @ v - v))
        z_res = float(np.linalg.norm(ZZZ @ v - v))
        print(f"  L{k}:  ||XXX|Lk⟩ − |Lk⟩|| = {x_res:.2e}, "
              f"||ZZZ|Lk⟩ − |Lk⟩|| = {z_res:.2e}")
    print()
    print("Codeword orthogonality:")
    for i in range(3):
        for j in range(i + 1, 3):
            ip = np.vdot(codeword(i), codeword(j))
            print(f"  ⟨L{i}|L{j}⟩ = {ip:.2e}")
    print()
    print("Stabilizer commutation: XXX·ZZZ - ZZZ·XXX residual = ", end="")
    print(f"{np.linalg.norm(XXX @ ZZZ - ZZZ @ XXX):.2e}")
    print()
    print("Error injection examples:")
    state = codeword(0)
    print(f"  |L0⟩ syndrome before error:")
    synd0 = measure_syndrome(state)
    print(f"    XXX class={synd0['xxx_class']}, ZZZ class={synd0['zzz_class']}, "
          f"is_codeword={synd0['is_codeword']}")
    for q in (0, 1, 2):
        for a, b in ((1, 0), (0, 1), (1, 1), (2, 1)):
            noisy = apply_error(state, q, a, b)
            s = measure_syndrome(noisy)
            print(f"  After X_3^{a}·Z_3^{b} on qutrit {q}: "
                  f"XXX class={s['xxx_class']}, ZZZ class={s['zzz_class']}, "
                  f"detected={not s['is_codeword']}")
    print()
    print("Detection benchmark (n=2000, p=0.3):")
    d = benchmark_detection(n_trials=2000, error_prob=0.3, seed=42)
    print(f"  errors_actual={d['n_errors_actual']}, "
          f"correct_detect={d['n_correct_detect']}, "
          f"false_negative={d['n_false_negative']}")
    print(f"  detection_rate = {d['detection_rate']*100:.2f}%, "
          f"false_negative_rate = {d['false_negative_rate']*100:.2f}%")
    print()
    print("Erasure correction benchmark (n=1000, random Pauli error,")
    print("erasure location known):")
    e = benchmark_erasure_correction(n_trials=1000, seed=42)
    print(f"  perfect_recovery = {e['n_perfect_recovery']}/{e['n_trials']} "
          f"({e['perfect_rate']*100:.2f}%)")
    print(f"  mean fidelity = {e['mean_fidelity']:.6f}")
    print()
    print("Honest scope:")
    print("  - Detection rate measures whether the syndrome flags an error.")
    print("  - At d=2, location ambiguity prevents arbitrary correction.")
    print("  - Erasure-correctable: when location is known, recovery is exact.")
    print("  - This is the smallest qutrit MDS code (saturates Singleton bound).")
    print("  - Holographic dual: minimal AdS/CFT-2 bulk localization model.")
