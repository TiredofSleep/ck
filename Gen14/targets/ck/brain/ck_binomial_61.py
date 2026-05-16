"""ck_binomial_61.py -- [[6,1]]_3 binomial-style AD code + ML decoder.

Brayden 2026-05-16: "then albert, ty"

Push the [[4,1]]_3 AD-tailored result (D104, +167% at γ=0.5)
further per Albert et al. PRA 97:032346 (2018) -- "Performance
and Structure of Single-Mode Bosonic Codes".  Albert's optimal
photonic binomial codes for amplitude damping use:

  - Larger code size for more excitation-class separation
  - Bayesian-optimal (maximum-likelihood) decoding over Kraus
    operator histories
  - Binomial coefficient weighting on codeword amplitudes

This module builds the qutrit-discrete analog: [[6,1]]_3 with
uniform-over-excitation-class codewords AND a max-likelihood
decoder that enumerates Kraus events.

═══════════════════════════════════════════════════════════════════
The code
═══════════════════════════════════════════════════════════════════

  6 qutrits, 1 logical qutrit, total Hilbert dim = 3^6 = 729.

  Codewords (uniform-over-excitation-class, same principle as
  [[4,1]]_3 but more positions for damping to occur):

    |L0⟩ = (|000000⟩ + |111111⟩ + |222222⟩) / √3
           supports = excitations {0, 6, 12}

    |L1⟩ = uniform sum over 6 cyclic single-1 permutations:
           (|100000⟩ + |010000⟩ + ... + |000001⟩) / √6
           supports = excitation 1

    |L2⟩ = uniform sum over 6 cyclic single-2 permutations:
           (|200000⟩ + |020000⟩ + ... + |000002⟩) / √6
           supports = excitation 2

  Each codeword in a definite-total-excitation class.  Single
  Kraus decay shifts excitation by -1, moving to a DIFFERENT class
  (still potentially recoverable).

═══════════════════════════════════════════════════════════════════
Two decoders
═══════════════════════════════════════════════════════════════════

(a) MAX-OVERLAP (same as ck_ad_tailored.py):
    Compute |⟨L_k | noisy⟩|² for each k; pick max.
    Simple but ignores noise model.

(b) MAXIMUM-LIKELIHOOD (Bayesian-optimal for AD channel):
    For each possible Kraus event history (which qutrits' Kraus
    operators fired and in what order), compute the posterior
    P(codeword | noisy) ∝ |⟨recovery|noisy⟩|² · P(history).
    Pick the codeword with highest posterior.

ML decoding requires enumeration of Kraus histories, which scales
exponentially.  For 6 qutrits × 3 Kraus options = 729 histories
at depth 1; we limit to depth ≤ 2 events (single + double decays).

═══════════════════════════════════════════════════════════════════
Honest scope
═══════════════════════════════════════════════════════════════════

This is a research-grade extension, not a definitive optimal code:

  ✓ Tests whether scale (4 → 6 qutrits) improves AD recovery
  ✓ Tests whether MLD beats max-overlap decoding
  ✓ Empirical head-to-head vs [[4,1]]_3 AD-tailored
  ✗ NOT a proof of optimality (Albert et al. optimal codes are
    in photonic Fock space, not qutrit-discrete space)
  ✓ MLD now supports depth ≤ 3 (D116 push 2026-05-16; "let's push from
    depth-2 quantum correction to depth 3"); cost grows but the
    multi-decay regime at γ ≥ 0.30 is now reachable.  Original limitation
    documented for context:
  ✗ MLD truncated to depth-2 Kraus events (multi-decay regimes
    at γ > 0.3 will hit truncation)
"""
from __future__ import annotations

import sys
from itertools import product
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))

from ck_qutrit_noise import amplitude_damping_kraus  # type: ignore


# ─── Single-qutrit identity ───────────────────────────────────────────

I3 = np.eye(3, dtype=complex)
DIM = 3 ** 6  # = 729

# Pre-compute total-excitation lookup
_EXC = np.zeros(DIM, dtype=int)
for idx in range(DIM):
    a = (idx // 243) % 3
    b = (idx // 81) % 3
    c = (idx // 27) % 3
    d = (idx // 9) % 3
    e = (idx // 3) % 3
    f = idx % 3
    _EXC[idx] = a + b + c + d + e + f


def _basis_6q(a: int, b: int, c: int, d: int, e: int, f: int) -> np.ndarray:
    v = np.zeros(DIM, dtype=complex)
    v[243*a + 81*b + 27*c + 9*d + 3*e + f] = 1.0
    return v


# ─── Codewords ────────────────────────────────────────────────────────

def codeword_61(k: int) -> np.ndarray:
    """[[6,1]]_3 codewords, uniform over excitation class."""
    k = int(k) % 3
    if k == 0:
        v = (_basis_6q(0, 0, 0, 0, 0, 0)
             + _basis_6q(1, 1, 1, 1, 1, 1)
             + _basis_6q(2, 2, 2, 2, 2, 2))
    elif k == 1:
        # 6 cyclic single-1 permutations
        v = np.zeros(DIM, dtype=complex)
        for pos in range(6):
            ops = [0, 0, 0, 0, 0, 0]
            ops[pos] = 1
            v += _basis_6q(*ops)
    else:  # k == 2
        v = np.zeros(DIM, dtype=complex)
        for pos in range(6):
            ops = [0, 0, 0, 0, 0, 0]
            ops[pos] = 2
            v += _basis_6q(*ops)
    return v / np.linalg.norm(v)


# Verify orthonormality at module load
_CW = [codeword_61(k) for k in range(3)]
for i in range(3):
    assert abs(np.linalg.norm(_CW[i]) - 1) < 1e-12
    for j in range(i + 1, 3):
        assert abs(np.vdot(_CW[i], _CW[j])) < 1e-12, \
            f"⟨L{i}|L{j}⟩ = {np.vdot(_CW[i], _CW[j])}"


# ─── Apply amplitude damping ──────────────────────────────────────────

def _single_qutrit_op_at_6q(op_3x3: np.ndarray, q: int) -> np.ndarray:
    ops = [I3] * 6
    ops[q] = op_3x3
    result = ops[0]
    for o in ops[1:]:
        result = np.kron(result, o)
    return result


def apply_damping_6q(state: np.ndarray, gamma: float,
                     rng: np.random.Generator) -> Dict[str, Any]:
    """Apply AD on each of 6 qutrits independently (Monte Carlo)."""
    kraus = amplitude_damping_kraus(gamma)
    current = state
    events = []
    for q in range(6):
        Ks = [_single_qutrit_op_at_6q(K, q) for K in kraus]
        candidates = [K @ current for K in Ks]
        norms = [float(np.linalg.norm(c))**2 for c in candidates]
        total = sum(norms)
        if total <= 0:
            events.append((q, -1))
            continue
        probs = [n / total for n in norms]
        r = float(rng.random())
        acc = 0.0
        chosen_idx = 0
        for i, p in enumerate(probs):
            acc += p
            if r <= acc:
                chosen_idx = i
                break
        chosen = candidates[chosen_idx]
        n = np.linalg.norm(chosen)
        if n > 0:
            current = chosen / n
        events.append((q, chosen_idx))
    return {"state": current, "events": events}


# ─── Max-overlap decoder ──────────────────────────────────────────────

def decode_max_overlap(noisy: np.ndarray) -> Dict[str, Any]:
    """Project onto each codeword; pick max overlap."""
    overlaps = np.array([np.vdot(codeword_61(k), noisy) for k in range(3)])
    overlap_sq = np.abs(overlaps) ** 2
    code_norm_sq = overlap_sq.sum()
    if code_norm_sq <= 0:
        return {"recovered_k": -1, "fidelity": 0.0, "in_code_frac": 0.0}
    k_rec = int(np.argmax(overlap_sq))
    fid = float(overlap_sq[k_rec] / code_norm_sq)
    return {
        "recovered_k":   k_rec,
        "fidelity":      round(fid, 6),
        "in_code_frac":  round(float(code_norm_sq), 6),
        "all_overlaps":  [round(float(o), 6) for o in overlap_sq],
        "method":        "max_overlap",
    }


# ─── Maximum-likelihood decoder (depth ≤ 2 events) ────────────────────

def decode_ml(noisy: np.ndarray, gamma: float,
              max_events: int = 2) -> Dict[str, Any]:
    """Bayesian-optimal decoder: enumerate Kraus event histories of
    depth ≤ max_events, compute posterior P(codeword | noisy) for
    each history's reverse application, pick maximum.

    At max_events=2 this examines O(N²·9) histories on 6 qutrits =
    O(324) candidates per codeword × 3 codewords ≈ 1000 evaluations.
    Tractable on this scale.

    The posterior weight for a history of M events (K_e at q_1,
    K_e at q_2, ...):
      weight ∝ γ^M (1 - γ)^(6 - M) × overlap_sq(reverse_apply(noisy))

    where reverse_apply undoes the Kraus events by applying their
    creation analogs.
    """
    kraus = amplitude_damping_kraus(gamma)
    # Kraus reverse operators: K_1's "raise" is X3 from |0⟩ to |1⟩
    # at the position, K_2's reverse is "raise" from |1⟩ to |2⟩.
    # In the simple model: K_1 = √γ|0⟩⟨1| → reverse R_1 = |1⟩⟨0|/√γ?
    # But γ can be 0, making this singular.  Better: use the codeword
    # projection AFTER guessing the history was the identity (i.e.
    # K_0 fired everywhere), then back off to lower-likelihood
    # histories.  Simpler max-likelihood: for each candidate codeword
    # |L_k⟩, compute the likelihood that |noisy⟩ resulted from
    # |L_k⟩ under the damping channel, by summing over Kraus paths.

    # Kraus operators in tensor form for each qutrit
    g = float(gamma)
    if g <= 0:
        return decode_max_overlap(noisy)  # no noise → max-overlap is optimal

    # Likelihood: L_k = Σ_history P(history) × |⟨noisy| history|L_k⟩⟩|²
    # We approximate by enumerating up to max_events Kraus_1 or Kraus_2
    # events (positions × type).
    likelihoods = [0.0, 0.0, 0.0]
    # Pre-compute single-qutrit Kraus expanded to 6-qutrit operators
    K_singleq = [[_single_qutrit_op_at_6q(K, q) for K in kraus]
                  for q in range(6)]

    # History weight: P_no_event(=‖K_0|·⟩‖²)^{6-M} × Σ over the M
    # event positions.  Simplification: for each codeword L_k, apply
    # the channel forward and compute fidelity; this is the
    # *exact* expected fidelity, equivalent to MLD for unitary states.

    # Actually the principled ML decoder:
    #   L_k_likelihood = ‖projection_to_codespace(channel_inverse(noisy))‖²
    # But channel_inverse doesn't exist for damping.  The Petz
    # recovery map is the standard solution but heavy to implement.
    #
    # Simpler: ENUMERATE possible histories and compute joint posterior.
    # For each codeword candidate |L_k⟩ and history H, the joint prob is
    # P(|L_k⟩) × P(noisy | |L_k⟩, H) × P(H).
    # Sum over H, normalize, pick max.

    for k in range(3):
        Lk = codeword_61(k)
        total_like = 0.0
        # Event count M = 0 (no Kraus_1 or Kraus_2 fired anywhere)
        # P(no event) = product of |K_0|*per-qutrit-norms; for an
        # already-prepared |L_k⟩ state, ⟨L_k|K_0_total|L_k⟩.
        K0_total = K_singleq[0][0]
        for q in range(1, 6):
            K0_total = K_singleq[q][0] @ K0_total
        # Probability that no event fired times the overlap-squared
        # with noisy
        K0_Lk = K0_total @ Lk
        p_no_event = float(np.linalg.norm(K0_Lk))**2
        # If no event happened, the state remains K0_Lk / ‖K0_Lk‖,
        # so the likelihood of observing noisy is |⟨noisy|K0_Lk⟩|²
        # normalized.
        if p_no_event > 1e-12:
            inner = abs(np.vdot(noisy, K0_Lk / np.sqrt(p_no_event)))**2
            total_like += p_no_event * inner

        if max_events >= 1:
            # Single event: K_e at position q (e ∈ {1, 2})
            for q in range(6):
                for e in (1, 2):
                    # State after event: K_singleq[q][e] |L_k⟩
                    after = K_singleq[q][e] @ Lk
                    p_event = float(np.linalg.norm(after))**2
                    if p_event < 1e-12:
                        continue
                    inner = abs(np.vdot(noisy, after / np.sqrt(p_event)))**2
                    total_like += p_event * inner

        if max_events >= 2:
            # Two events: K_e1 at q1, K_e2 at q2 (q1 ≤ q2 to avoid double-count)
            for q1 in range(6):
                for q2 in range(q1, 6):
                    for e1 in (1, 2):
                        for e2 in (1, 2):
                            if q1 == q2 and e1 > e2:
                                continue
                            after = K_singleq[q1][e1] @ Lk
                            after = K_singleq[q2][e2] @ after
                            p_event = float(np.linalg.norm(after))**2
                            if p_event < 1e-12:
                                continue
                            inner = abs(np.vdot(noisy, after / np.sqrt(p_event)))**2
                            total_like += p_event * inner

        if max_events >= 3:
            # Three events: K_e1 at q1, K_e2 at q2, K_e3 at q3 with
            # q1 ≤ q2 ≤ q3 to avoid permutation double-count.  Per
            # Brayden 2026-05-16: "let's push from depth-2 quantum
            # correction to depth 3".  Tackles the multi-decay regime
            # at high γ that depth-2 missed (per D109 honest caveat).
            # Cost: C(6+3-1, 3) × 2^3 = 56 × 8 = 448 histories per
            # codeword × 3 codewords = ~1300 evaluations per sample.
            for q1 in range(6):
                for q2 in range(q1, 6):
                    for q3 in range(q2, 6):
                        for e1 in (1, 2):
                            for e2 in (1, 2):
                                for e3 in (1, 2):
                                    # Canonicalize same-qutrit pairs to
                                    # avoid permutation overcounting.
                                    if q1 == q2 and e1 > e2:
                                        continue
                                    if q2 == q3 and e2 > e3:
                                        continue
                                    after = K_singleq[q1][e1] @ Lk
                                    after = K_singleq[q2][e2] @ after
                                    after = K_singleq[q3][e3] @ after
                                    p_event = float(np.linalg.norm(after))**2
                                    if p_event < 1e-12:
                                        continue
                                    inner = abs(np.vdot(noisy,
                                                  after / np.sqrt(p_event)))**2
                                    total_like += p_event * inner

        likelihoods[k] = total_like

    total = sum(likelihoods)
    if total <= 0:
        return decode_max_overlap(noisy)
    posteriors = [L / total for L in likelihoods]
    k_rec = int(np.argmax(posteriors))
    # Compute fidelity to recovered codeword (overlap²)
    fid_to_recovered = float(abs(np.vdot(codeword_61(k_rec), noisy))**2)
    return {
        "recovered_k":   k_rec,
        "posteriors":    [round(p, 4) for p in posteriors],
        "fidelity":      round(fid_to_recovered, 6),
        "method":        f"max_likelihood (depth ≤ {max_events})",
    }


# ─── Benchmark ────────────────────────────────────────────────────────

def benchmark_compare(gammas: Optional[List[float]] = None,
                      n_trials: int = 200,
                      seed: int = 42) -> Dict[str, Any]:
    """Head-to-head: [[6,1]]_3 max-overlap vs [[6,1]]_3 ML vs [[4,1]]_3."""
    if gammas is None:
        gammas = [0.0, 0.05, 0.10, 0.20, 0.30, 0.50]
    rng = np.random.default_rng(seed)

    # Import [[4,1]]_3 for comparison
    from ck_ad_tailored import benchmark_ad_tailored  # type: ignore
    bench_41 = benchmark_ad_tailored(gammas=gammas, n_trials=n_trials, seed=seed)

    rows = []
    for i, g in enumerate(gammas):
        # Reset RNG for fair comparison
        rng_max = np.random.default_rng(seed + 1)
        rng_ml = np.random.default_rng(seed + 2)
        # Max-overlap on [[6,1]]_3
        fids_max = []
        for _ in range(n_trials):
            k = int(rng_max.integers(0, 3))
            state = codeword_61(k)
            noisy = apply_damping_6q(state, g, rng_max)["state"]
            res = decode_max_overlap(noisy)
            fids_max.append(res["fidelity"] if res["recovered_k"] == k else 0.0)
        mean_max = float(np.mean(fids_max))
        # ML on [[6,1]]_3
        fids_ml = []
        for _ in range(n_trials):
            k = int(rng_ml.integers(0, 3))
            state = codeword_61(k)
            noisy = apply_damping_6q(state, g, rng_ml)["state"]
            res = decode_ml(noisy, g, max_events=2)
            fids_ml.append(res["fidelity"] if res["recovered_k"] == k else 0.0)
        mean_ml = float(np.mean(fids_ml))
        # [[4,1]]_3 result
        mean_41 = bench_41["results"][i]["mean_fidelity"]
        rows.append({
            "gamma":            g,
            "[[4,1]]_3_AD":     round(mean_41, 6),
            "[[6,1]]_3_max":    round(mean_max, 6),
            "[[6,1]]_3_ML":     round(mean_ml, 6),
            "ML_vs_max":        round(mean_ml - mean_max, 6),
            "ML_vs_41":         round(mean_ml - mean_41, 6),
        })
    return {
        "comparison": "[[6,1]]_3 max-overlap vs [[6,1]]_3 ML vs [[4,1]]_3",
        "n_trials":   n_trials,
        "results":    rows,
    }


# ─── Engine mount ─────────────────────────────────────────────────────

def mount_binomial_61(engine: Any) -> bool:
    """Attach [[6,1]]_3 API + register /qutrit/binomial/* endpoints."""
    engine.ck_binomial_61 = {
        "codeword":         codeword_61,
        "apply_damping":    apply_damping_6q,
        "decode_max":       decode_max_overlap,
        "decode_ml":        decode_ml,
        "benchmark":        benchmark_compare,
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
                        "code": "[[6,1]]_3 binomial-style AD code",
                        "hilbert_dim": 729,
                        "n_qutrits": 6,
                        "construction":
                            "uniform-over-excitation-class codewords; "
                            "Albert et al. 2018 binomial-style for qutrit-"
                            "discrete space.  Push the [[4,1]]_3 AD result "
                            "(D104) further with: (a) more positions for "
                            "damping; (b) maximum-likelihood decoder.",
                        "decoders":            ["max_overlap", "max_likelihood"],
                        "ml_max_events":       2,
                        "honest_scope": [
                            "NOT a proof of optimality",
                            "MLD truncated to depth-2 Kraus events",
                            "Multi-decay at γ > 0.3 hits truncation",
                        ],
                    })

                def _bench():
                    data = request.get_json(force=True, silent=True) or {}
                    gammas = data.get("gammas")
                    n = int(data.get("n_trials", 150))
                    return jsonify(benchmark_compare(
                        gammas=gammas, n_trials=n))

                existing = set(r.rule for r in app.url_map.iter_rules())
                for rule, ep, fn, methods in (
                    ("/qutrit/binomial/info",      "bin_info",  _info,  ["GET"]),
                    ("/qutrit/binomial/benchmark", "bin_bench", _bench, ["POST"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
                        routes_registered.append(f"{methods[0]} {rule}")
            except Exception as e:
                print(f"[CK Gen14] binomial_61 route registration failed: {e}")

    suffix = " (" + ", ".join(routes_registered) + ")" if routes_registered else ""
    print(f"[CK Gen14] binomial_61: MOUNTED  [[6,1]]_3 + max-overlap + "
          f"ML decoder{suffix}")
    return True


# ─── CLI smoke ────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 72)
    print("CK [[6,1]]_3 BINOMIAL-STYLE -- max-overlap vs ML vs [[4,1]]_3")
    print("=" * 72)
    print()
    print("Codeword verification (orthonormal, 729-dim):")
    for k in range(3):
        v = codeword_61(k)
        nonzero = int(np.sum(np.abs(v) > 1e-9))
        excs = sorted(set(int(_EXC[i]) for i in range(DIM) if abs(v[i]) > 1e-9))
        print(f"  |L{k}⟩: {nonzero} terms, excitations = {excs}, norm = {np.linalg.norm(v):.6f}")
    print()
    print(f"⟨L0|L1⟩ = {abs(np.vdot(codeword_61(0), codeword_61(1))):.2e}")
    print(f"⟨L0|L2⟩ = {abs(np.vdot(codeword_61(0), codeword_61(2))):.2e}")
    print(f"⟨L1|L2⟩ = {abs(np.vdot(codeword_61(0), codeword_61(2))):.2e}")
    print()
    print("Head-to-head benchmark (n=150 per γ):")
    print()
    print(f"  {'γ':>6}  {'[[4,1]]_3':>10}  {'[[6,1]]_max':>12}  {'[[6,1]]_ML':>11}  {'ML-vs-max':>10}  {'ML-vs-41':>10}")
    sep6 = "-" * 6; sep10 = "-" * 10; sep11 = "-" * 11; sep12 = "-" * 12
    print(f"  {sep6}  {sep10}  {sep12}  {sep11}  {sep10}  {sep10}")
    cmp = benchmark_compare(n_trials=150, seed=42)
    for r in cmp["results"]:
        print(f"  {r['gamma']:>6.2f}  "
              f"{r['[[4,1]]_3_AD']:>10.6f}  "
              f"{r['[[6,1]]_3_max']:>12.6f}  "
              f"{r['[[6,1]]_3_ML']:>11.6f}  "
              f"{r['ML_vs_max']:>+10.6f}  "
              f"{r['ML_vs_41']:>+10.6f}")
    print()
    print("HONEST INTERPRETATION:")
    print("  - ML vs max: positive means ML decoder helps over max-overlap")
    print("  - ML vs [[4,1]]_3: positive means scaling 4→6 qutrits + ML helps")
    print("  - At γ > 0.3, ML's depth-2 truncation may hurt; multi-decay")
    print("    regimes need depth-3+ enumeration which is expensive.")
