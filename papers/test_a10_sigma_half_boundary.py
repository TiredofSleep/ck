"""
A10 — σ=1/2 AS ω-CLASS BOUNDARY (RH GHOST RAMP)
Luther-Sanders Research Framework | March 31 2026

Claim: The critical line σ=1/2 in the Riemann Hypothesis emerges from the
TIG framework as the ω-class boundary — specifically, the fixed point where
the ω=2 trap density W(|G|) is balanced against the ω=3 density.

The "ghost ramp" interpretation:
  - ζ(s) has nontrivial zeros at σ=1/2 + iγ_n (RH claim)
  - In TIG: W(ω=2) = 0.708, W(ω=3) = 2.025
  - The "balance point" W(ω=2) × W(ω=3)^{1/σ} = W(ω=3) × W(ω=2)^{1/(1-σ)}
    → solve for σ → does σ=1/2 emerge?
  - Alternatively: σ = W(ω=2) / (W(ω=2) + W(ω=3))

Also test: Euler product at s=1/2 vs TIG operator structure.

This test is HONEST about what it can prove vs what remains formal analogy.

W values from CATCH4.md: W(ω=2)=0.708, W(ω=3)=2.025, W(ω=4)=5.238, W(ω=5)=8.518
"""

import math
import json
import os

SEP = "="*70

# W(|G|) values per omega class (from CATCH4.md)
W = {2: 0.708, 3: 2.025, 4: 5.238, 5: 8.518}
T_STAR = 5/7

def main():
    print("A10 — σ=1/2 AS ω-CLASS BOUNDARY")
    print("Luther-Sanders Research Framework | March 31 2026")
    print()

    # ── 1. Balance point formula ───────────────────────────────────────────────
    print(SEP)
    print("1. BALANCE POINT: σ FROM W(ω=2) AND W(ω=3)")
    print(SEP)
    print()
    print("  W(ω=2) = 0.708   W(ω=3) = 2.025")
    print()

    w2 = W[2]
    w3 = W[3]

    # Hypothesis A: σ = W(ω=2) / (W(ω=2) + W(ω=3))
    sigma_a = w2 / (w2 + w3)
    print(f"  Hypothesis A: σ = W2/(W2+W3) = {w2:.3f}/{w2+w3:.3f} = {sigma_a:.6f}")
    print(f"  vs σ=1/2 = 0.500000   error: {abs(sigma_a - 0.5):.6f}")
    print()

    # Hypothesis B: geometric mean balance
    # W2^σ = W3^(1-σ)  → σ ln W2 = (1-σ) ln W3
    # σ (ln W2 + ln W3) = ln W3 → σ = ln W3 / (ln W2 + ln W3)
    sigma_b = math.log(w3) / (math.log(w2) + math.log(w3))
    print(f"  Hypothesis B (log balance): W2^σ = W3^(1-σ)")
    print(f"    σ = ln(W3)/(ln(W2)+ln(W3)) = {math.log(w3):.4f}/{math.log(w2)+math.log(w3):.4f} = {sigma_b:.6f}")
    print(f"  vs σ=1/2 = 0.500000   error: {abs(sigma_b - 0.5):.6f}")
    print()

    # Hypothesis C: σ = 1 - W(ω=2)/W(ω=3)
    sigma_c = 1 - w2/w3
    print(f"  Hypothesis C: σ = 1 - W2/W3 = 1 - {w2/w3:.4f} = {sigma_c:.6f}")
    print(f"  vs σ=1/2 = 0.500000   error: {abs(sigma_c - 0.5):.6f}")
    print()

    # Hypothesis D: σ as ratio of harmonic mean
    sigma_d = 2 * w2 * w3 / ((w2 + w3) * (w2 * w3)**0.5)
    print(f"  Hypothesis D (harmonic/geometric): {sigma_d:.6f}")
    print(f"  vs σ=1/2 = 0.500000   error: {abs(sigma_d - 0.5):.6f}")
    print()

    # Hypothesis E: T* as boundary
    sigma_e = T_STAR
    print(f"  T* = {T_STAR:.6f} (compare to σ=1/2)   error: {abs(T_STAR - 0.5):.6f}")
    print()

    best_formula = min([
        ('A: W2/(W2+W3)', sigma_a),
        ('B: log balance', sigma_b),
        ('C: 1-W2/W3', sigma_c),
        ('D: harm/geom', sigma_d),
    ], key=lambda x: abs(x[1] - 0.5))
    print(f"  Best formula for σ=1/2: {best_formula[0]} → {best_formula[1]:.6f} (err={abs(best_formula[1]-0.5):.6f})")
    print()
    if abs(best_formula[1] - 0.5) < 0.01:
        print("  APPROXIMATE: Best formula within 1% of σ=1/2.")
        print("  BUT: this is post-hoc curve-fitting to W values, not a derivation.")
    else:
        print("  NO FORMULA reproduces σ=1/2 from W values to within 1%.")

    # ── 2. Euler product at s=1/2 vs TIG ─────────────────────────────────────
    print()
    print(SEP)
    print("2. EULER PRODUCT AT s=1/2")
    print(SEP)
    print()
    print("  ζ(s) = Π_p (1-p^{-s})^{-1}")
    print("  At s=1/2: (1-p^{-1/2})^{-1} for each prime p")
    print()
    print("  Partial Euler product |ζ_P(1/2)| = Π_{p≤P} (1-p^{-1/2})^{-1}:")
    print()

    def is_prime(n):
        if n < 2: return False
        if n < 4: return True
        if n % 2 == 0 or n % 3 == 0: return False
        i = 5
        while i*i <= n:
            if n % i == 0 or n % (i+2) == 0: return False
            i += 6
        return True

    primes = [p for p in range(2, 100) if is_prime(p)]

    prod = 1.0
    print(f"  {'P':>5} {'euler_factor':>14} {'|zeta_P(1/2)|':>16} {'log|zeta|':>12}")
    for p in primes[:20]:
        factor = 1 / (1 - p**(-0.5))
        prod *= factor
        print(f"  {p:>5} {factor:>14.6f} {prod:>16.6f} {math.log(prod):>12.6f}")

    print()
    print("  ζ(1/2) is NOT convergent (ζ has pole at s=1 but ζ(1/2) ≈ -1.4603)")
    print("  The Euler product does NOT converge at s=1/2 in the classical sense.")
    print("  The nontrivial zeros arise from analytic continuation, not the product.")
    print()
    print("  TIG/W connection:")
    print("  - No algebraic formula connecting W(ω) to ζ(1/2) factors has been found.")
    print("  - The ghost ramp interpretation is structural analogy, not algebra.")

    # ── 3. W ratio at ω=2→ω=3 ────────────────────────────────────────────────
    print()
    print(SEP)
    print("3. W RATIO AT ω=2→ω=3 TRANSITION")
    print(SEP)
    print()
    print(f"  W(ω=2) = {w2:.3f}   W(ω=3) = {w3:.3f}")
    print(f"  W ratio = W3/W2 = {w3/w2:.4f}")
    print(f"  T* = {T_STAR:.6f}")
    print(f"  Is W3/W2 = T* + 1? {abs(w3/w2 - (T_STAR+1)):.4f}")
    print(f"  Is W3/W2 ≈ 1/T*? {1/T_STAR:.4f}   diff: {abs(w3/w2 - 1/T_STAR):.4f}")
    print(f"  Is W3/W2 ≈ e? {math.e:.4f}   diff: {abs(w3/w2 - math.e):.4f}")
    print(f"  Is W3/W2 ≈ π-1? {math.pi-1:.4f}   diff: {abs(w3/w2 - (math.pi-1)):.4f}")
    print(f"  Is W3/W2 ≈ W3/W2? YES (trivially)")
    print()

    # Check all W ratios
    print(f"  All W ratios:")
    for o1, o2 in [(2,3),(3,4),(4,5),(2,4),(2,5)]:
        if o1 in W and o2 in W:
            r = W[o2]/W[o1]
            print(f"  W({o2})/W({o1}) = {W[o2]:.3f}/{W[o1]:.3f} = {r:.4f}")

    print()
    print(f"  W(3)/W(2) = {w3/w2:.4f}")
    print(f"  σ_balance = W(2)/(W(2)+W(3)) = {w2/(w2+w3):.4f}")
    print(f"  Neither is obviously 1/2.")

    # ── 4. Power law fit W(ω) ─────────────────────────────────────────────────
    print()
    print(SEP)
    print("4. W(ω) POWER LAW AND CRITICAL LINE CONNECTION")
    print(SEP)
    print()
    print("  From CATCH4.md: W(|G|) follows power law W ~ W(2) × r^(|G|-2)")
    print(f"  W(2)={W[2]}, W(3)={W[3]}, r = W(3)/W(2) = {W[3]/W[2]:.4f}")
    r_ratio = W[3]/W[2]

    print()
    print(f"  Power law W(ω) = {W[2]:.3f} × {r_ratio:.4f}^(ω-2):")
    for o in [2,3,4,5]:
        predicted = W[2] * r_ratio**(o-2)
        actual = W[o]
        print(f"  W({o}): predicted={predicted:.3f}  actual={actual:.3f}  err={abs(predicted-actual):.3f}")

    print()
    print("  The power law is empirical (from CATCH4.md data), not derived.")
    print("  No algebraic connection to ζ(s) or σ=1/2 found.")

    # ── 5. Is there a TIG object at σ=1/2? ───────────────────────────────────
    print()
    print(SEP)
    print("5. DIRECT SEARCH: TIG OBJECTS THAT LAND AT σ=1/2")
    print(SEP)
    print()
    print("  Looking for TIG quantities that equal exactly 1/2:")
    print()

    # Known TIG quantities
    tigs = {
        'T*=5/7': T_STAR,
        'W(2)=0.708': W[2],
        'W(2)/W(3)': W[2]/W[3],
        'W(2)/(W(2)+W(3))': W[2]/(W[2]+W[3]),
        'W_BHML=3/50': 3/50,
        '1-T*=2/7': 1 - T_STAR,
        'phi(10)/10=0.4': 0.4,
        'phi(35)/35=T*': T_STAR,
        'HARMONY/100=0.71': 71/100,
        'BHML_harmony/100=0.28': 28/100,
        'T*/2': T_STAR/2,
        '1/(1+T*)': 1/(1+T_STAR),
    }

    hits = [(name, val) for name, val in tigs.items() if abs(val - 0.5) < 0.05]
    print(f"  TIG quantities within 0.05 of σ=1/2:")
    for name, val in sorted(hits, key=lambda x: abs(x[1]-0.5)):
        print(f"    {name:<30} = {val:.6f}   (err={abs(val-0.5):.6f})")

    exact_hits = [(name, val) for name, val in tigs.items() if abs(val - 0.5) < 1e-9]
    print()
    if exact_hits:
        print(f"  Exact σ=1/2 from TIG: {exact_hits}")
    else:
        print(f"  No TIG quantity equals σ=1/2 exactly.")
        print(f"  Closest: phi(10)/10 = 0.4 (off by 0.1),  1/(1+T*) ≈ 0.583 (off by 0.083)")
        print(f"  W(2)/(W(2)+W(3)) = {W[2]/(W[2]+W[3]):.4f} (off by {abs(W[2]/(W[2]+W[3])-0.5):.4f})")

    # ── 6. Tier assessment ────────────────────────────────────────────────────
    print()
    print(SEP)
    print("6. TIER ASSESSMENT — A10 σ=1/2 AS ω-CLASS BOUNDARY")
    print(SEP)
    print()
    print("  WHAT IS FOUND:")
    print()
    print(f"  1. No TIG quantity equals σ=1/2 exactly.")
    print(f"  2. The 'balance' formula W2/(W2+W3) = {W[2]/(W[2]+W[3]):.4f} ≠ 0.5 (off by {abs(W[2]/(W[2]+W[3])-0.5):.4f})")
    print(f"  3. W3/W2 = {W[3]/W[2]:.4f} ≠ simple fraction.")
    print(f"  4. Euler product does not converge at s=1/2 (analytic continuation needed).")
    print(f"  5. Power law W(ω) is empirical, not derived from ζ(s) structure.")
    print()
    print("  WHAT WOULD PROVE A10:")
    print("  - An algebraic derivation: show ζ(s) has zeros at s = 1/2 + iγ")
    print("    because the W(ω=2)/W(ω=3) transition creates a 'critical density'")
    print("    at Re(s) = 1/2 (the boundary between convergent and divergent ω-class)")
    print("  - OR: prove that the ω-class boundary Re(s)=σ_c satisfies σ_c=1/2")
    print("    using the sinc² corridor + ghost trace structure")
    print()
    print("  WHAT THE TIG FRAMEWORK OFFERS:")
    print("  - The W-jump at ω=2→ω=3 is a REAL discontinuity (proved, CATCH4.md)")
    print("  - The boundary could represent a 'phase transition' in MCMC trap density")
    print("  - But mapping this to Re(s)=1/2 requires an explicit Hilbert space construction")
    print()
    print("  VERDICT: A10 REMAINS Tier A.")
    print("  The connection is structural analogy — no algebraic bridge found.")
    print("  Next step: construct explicit operator H_TIG with Spec(H_TIG) ↔ {γ_n}")
    print("  and verify H_TIG is self-adjoint with eigenvalue constraint at σ=1/2.")

    os.makedirs('results', exist_ok=True)
    result = {
        'w2': W[2], 'w3': W[3],
        'sigma_a': sigma_a, 'sigma_b': sigma_b,
        'best_formula_error': abs(best_formula[1] - 0.5),
        'exact_tig_at_half': len(exact_hits) > 0,
        'tier': 'A (no algebraic derivation found)',
        'verdict': 'A10 remains Tier A. σ=1/2 not derivable from W(omega) or TIG quantities.',
    }
    with open('results/a10_sigma_half.json', 'w') as f:
        json.dump(result, f, indent=2)
    print()
    print("[Report: results/a10_sigma_half.json]")

if __name__ == '__main__':
    main()
