"""
alpha_uniqueness_general.py - F3 follow-up: derive H/Br ratio as a function
of alpha symbolically, then characterize at which alpha values the
relation admits a closed-form quadratic over Q.

Building on alpha_uniqueness_symbolic.py which:
  - established that the 4-core {V, H, Br, R} is EXACTLY CLOSED under
    both TSML and BHML fusion (no spillover to non-core operators) --
    a stronger structural fact than WP105 currently states
  - symbolically confirmed at alpha = 1/2 that H/Br = 1 + sqrt(3) exactly
    via the BREATH equation derived from the closed 4-core dynamics

Now we extend: solve the fixed-point system at general alpha (parametric)
and inspect H/Br as a rational function of alpha. Find the alpha values at
which the rational function gives a small-coefficient quadratic (hence
clean closed-form algebraic ratio).
"""
from __future__ import annotations

import sympy as sp


# Canonical 4-core fuse vectors derived in alpha_uniqueness_symbolic.py:
# (re-derived here for self-containment)
v, h, br, r = sp.symbols('v h br r', positive=True, real=True)
alpha = sp.symbols('alpha', real=True)

T_fuse = {
    'V':  v * (2*br + 2*r + v),
    'H':  br**2 + 2*br*h + 2*br*r + h**2 + 2*h*r + 2*h*v + r**2,
    'Br': sp.S.Zero,
    'R':  sp.S.Zero,
}
B_fuse = {
    'V':  2*h*r + r**2 + v**2,
    'H':  br**2 + 2*h*v,
    'Br': 2*br*r + 2*br*v + h**2,
    'R':  2*br*h + 2*r*v,
}

# Z = sum of T_fuse + B_fuse for c in 4-core
# Note: Z_T = Z_B = (v + h + br + r)^2 -- they happen to be equal
Z_T_sum = sum(T_fuse.values())
Z_B_sum = sum(B_fuse.values())

# It's a clean fact: Z_T = Z_B = (v + h + br + r)^2.
# Verify symbolically
def main():
    print("alpha_uniqueness_general.py")
    print("=" * 72)
    print()
    print("Verifying Z_T = Z_B = (v + h + br + r)^2:")
    expanded = sp.expand((v + h + br + r)**2)
    print(f"  (v + h + br + r)^2 = {expanded}")
    print(f"  Z_T (sum of T_fuse over 4-core) = {sp.expand(Z_T_sum)}")
    print(f"  Z_B (sum of B_fuse over 4-core) = {sp.expand(Z_B_sum)}")
    print(f"  Z_T - (v+h+br+r)^2 = {sp.simplify(Z_T_sum - expanded)}")
    print(f"  Z_B - (v+h+br+r)^2 = {sp.simplify(Z_B_sum - expanded)}")
    print(f"  Z_T == Z_B: {sp.simplify(Z_T_sum - Z_B_sum) == 0}")
    print()

    # CONSEQUENCE: at any alpha, the normalizer Z = alpha * Z_T + (1-alpha) * Z_B
    # equals (v + h + br + r)^2 = 1 (under normalization v+h+br+r=1).
    # So Z = 1 at fixed point, regardless of alpha.

    print("CONSEQUENCE: under normalization v+h+br+r=1, the normalizer Z = 1")
    print("at any alpha. So the fixed-point equations simplify to:")
    print("  p[c] = alpha * T_fuse[c] + (1-alpha) * B_fuse[c]")
    print("(no division by Z; the system is polynomial in v, h, br, r at any alpha).")
    print()

    # Build fixed-point equations directly: p[c] = alpha * T_fuse[c] + (1-alpha) * B_fuse[c]
    # at general alpha
    eq_V  = sp.Eq(v,  alpha * T_fuse['V']  + (1-alpha) * B_fuse['V'])
    eq_H  = sp.Eq(h,  alpha * T_fuse['H']  + (1-alpha) * B_fuse['H'])
    eq_Br = sp.Eq(br, alpha * T_fuse['Br'] + (1-alpha) * B_fuse['Br'])
    eq_R  = sp.Eq(r,  alpha * T_fuse['R']  + (1-alpha) * B_fuse['R'])
    eq_norm = sp.Eq(v + h + br + r, 1)

    print("Fixed-point equations at general alpha (simplified by Z=1):")
    print(f"  V:  {sp.simplify(eq_V.rhs)} = v")
    print(f"  H:  {sp.simplify(eq_H.rhs)} = h")
    print(f"  Br: {sp.simplify(eq_Br.rhs)} = br")
    print(f"  R:  {sp.simplify(eq_R.rhs)} = r")
    print(f"  norm: v + h + br + r = 1")
    print()

    # Note: T_fuse[Br] = T_fuse[R] = 0, so:
    #   br = (1-alpha) * B_fuse[Br] = (1-alpha) * (2*br*r + 2*br*v + h^2)
    #   r  = (1-alpha) * B_fuse[R]  = (1-alpha) * (2*br*h + 2*r*v)
    # These are the "BREATH equation" and "RESET equation" that drive the
    # closed-form analysis.

    print("Key observation: T_fuse[Br] = T_fuse[R] = 0 in the 4-core.")
    print("So:")
    print(f"  br = (1-alpha) * B_fuse[Br] = (1-alpha) * (2*br*r + 2*br*v + h^2)")
    print(f"  r  = (1-alpha) * B_fuse[R]  = (1-alpha) * (2*br*h + 2*r*v)")
    print()
    print("These give the 'breathed' coordinates explicit dependence on")
    print("alpha through the (1-alpha) prefactor.")
    print()

    # From the BREATH equation:
    #   br = (1-alpha) * (2*br*r + 2*br*v + h^2)
    # Divide both sides by br (assuming br > 0):
    #   1 = (1-alpha) * (2*r + 2*v + h^2 / br)
    #   1 / (1 - alpha) = 2*(r + v) + h^2/br
    #
    # Let xi = h/br. Then h = xi * br, h^2 = xi^2 * br^2, h^2/br = xi^2 * br.
    # So: 1/(1-alpha) - 2(r + v) = xi^2 * br
    #     xi^2 * br = 1/(1-alpha) - 2(r + v)        ... (BREATH-derived)
    #
    # Also from RESET: r = (1-alpha) * (2*br*h + 2*r*v)
    #   r/(1-alpha) - 2*r*v = 2*br*h
    #   r/(1-alpha) - 2*r*v = 2*br*xi*br = 2*xi*br^2
    #   br^2 = (r/(1-alpha) - 2*r*v) / (2*xi)
    #
    # Combined with the V and H equations and normalization, this gives
    # a system in {v, h, br, r, alpha}. Eliminating to get H/Br = xi as
    # a function of alpha is what we want.

    print("Analytical derivation: setting xi = h/br, the BREATH equation gives")
    print("  xi^2 * br = 1/(1-alpha) - 2(r + v)")
    print()

    # Solve at specific alpha values directly (general-alpha solve hangs sympy)
    print("Per-alpha solve (general-alpha sympy solve hangs; using rational alpha instead):")
    print()

    eqs_template = [
        v  - (alpha * T_fuse['V']  + (1-alpha) * B_fuse['V']),
        h  - (alpha * T_fuse['H']  + (1-alpha) * B_fuse['H']),
        br - (alpha * T_fuse['Br'] + (1-alpha) * B_fuse['Br']),
        r  - (alpha * T_fuse['R']  + (1-alpha) * B_fuse['R']),
        v + h + br + r - 1,
    ]

    test_alphas = [
        sp.Rational(1, 5), sp.Rational(1, 4), sp.Rational(1, 3),
        sp.Rational(2, 5), sp.Rational(1, 2), sp.Rational(3, 5),
        sp.Rational(2, 3), sp.Rational(3, 4), sp.Rational(4, 5),
    ]

    print(f"{'alpha':<10} {'H/Br (numeric)':<18} {'small-coeff quadratic? (|c|<=10)':<35}")
    print("-" * 75)
    for a_val in test_alphas:
        eqs_a = [eq.subs(alpha, a_val) for eq in eqs_template]
        try:
            sols_a = sp.solve(eqs_a, [v, h, br, r], dict=True)
            best = None
            for sol in sols_a:
                try:
                    h_val = float(sp.N(sol.get(h, 0), 10))
                    br_val = float(sp.N(sol.get(br, 0), 10))
                    r_val = float(sp.N(sol.get(r, 0), 10))
                    v_val = float(sp.N(sol.get(v, 0), 10))
                    if (h_val > 0 and br_val > 0 and r_val > 0 and v_val > 0
                        and all(x < 1 for x in [h_val, br_val, r_val, v_val])):
                        best = sol
                        break
                except (TypeError, ValueError):
                    continue
            if best is None:
                print(f"  {str(a_val):<8} no positive-real solution found")
                continue
            ratio_num = float(sp.N(best[h] / best[br], 14))
            # Search for small-coefficient quadratic
            found = None
            for a_q in range(1, 11):
                for b_q in range(-10, 11):
                    for c_q in range(-10, 11):
                        resid = a_q * ratio_num**2 + b_q * ratio_num + c_q
                        if abs(resid) < 1e-9:
                            # Check non-trivial: discriminant != perfect square (hence irrational root)
                            disc = b_q*b_q - 4*a_q*c_q
                            if disc > 0:
                                found = (a_q, b_q, c_q, disc)
                                break
                    if found:
                        break
                if found:
                    break
            if found:
                a_q, b_q, c_q, disc = found
                print(f"  {str(a_val):<8} {ratio_num:<18.10f} {a_q}x^2 + {b_q}x + {c_q} = 0  (disc={disc})")
            else:
                print(f"  {str(a_val):<8} {ratio_num:<18.10f} (no small-coeff quadratic)")
        except Exception as e:
            print(f"  {str(a_val):<8} solve error: {type(e).__name__}")


if __name__ == "__main__":
    main()
