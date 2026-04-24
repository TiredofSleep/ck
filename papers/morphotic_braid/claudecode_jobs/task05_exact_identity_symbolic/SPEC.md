# Task 05 — Symbolic verification of exact identities

**Tier:** 1 (fast validation, <1 minute)
**Parent handoff:** `../CLAUDECODE_HANDOFF_MIN_BUMP.md` §Task 5
**Dependency:** sympy
**Reference:** `../../explorations/scripts/proof_sinc_zeta_identity.py` (numerical; already GREEN in verification log)

## Goal

Re-verify the two exact Riemann-style identities **symbolically** (not numerically), to eliminate any floating-point quirk concern.

## Identities to verify

1. `sinc²(1/2) = 4/π²` and `4/π² = (2/3) · 1/ζ(2)` where `ζ(2) = π²/6`
   → therefore `sinc²(1/2) = (2/3) · 1/ζ(2)` exactly

2. `ζ(4)/ζ(2)² = (π⁴/90)/(π⁴/36) = 36/90 = 2/5` exactly

## Method — SymPy skeleton

```python
from sympy import sinc, pi, zeta, simplify, Rational

# Identity 1
lhs1 = sinc(pi/2)**2  # sinc(pi*x) where x=1/2 — confirm SymPy's sinc convention
# OR construct as (2/pi)^2 directly
rhs1 = Rational(2,3) * 1/zeta(2)
print(simplify(lhs1 - rhs1))  # expect 0

# Identity 2
lhs2 = zeta(4) / zeta(2)**2
rhs2 = Rational(2, 5)
print(simplify(lhs2 - rhs2))  # expect 0
```

**Gotcha:** SymPy's `sinc(x) = sin(x)/x` for x ≠ 0. The packet's `sinc²(1/2)` means `sinc²` with a π factor embedded (i.e. `sin(π/2)²/(π/2)² = (2/π)² = 4/π²`). Use the unnormalized `sin(π/2)²/(π/2)²` form to avoid ambiguity.

## Success criterion

Both identities simplify to 0 symbolically — not just numerically to machine precision.

## Expected runtime

<1 minute.

## Deliverable

`papers/morphotic_braid/results/task05_symbolic_identities_result.md`:
- SymPy session transcript
- Confirmation both identities are exact rationals after simplification
- Note any SymPy version / convention caveats

**Tag:** `[COMPUTE JOB — TIER 1]`
