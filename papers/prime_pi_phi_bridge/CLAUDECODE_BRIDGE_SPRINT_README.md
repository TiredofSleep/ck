# CLAUDECODE SPRINT HANDOFF
## Task: Prime–π–φ Bridge Submission Hardening

**From:** Claude (claude.ai session)  
**To:** ClaudeCode  
**Date:** 2026-04-04  
**Priority:** Medium — submission prep, not urgent infrastructure  
**Estimated effort:** 1–2 sessions  

---

## CONTEXT

This sprint formalizes a mathematical research memo for external scrutiny and eventual submission. The memo documents structural relationships between:

1. **Finite arithmetic side:** Algebraic degree of 2cos(π/p) for primes p — specifically that p=5 is the first prime yielding the golden ratio φ via roots of unity
2. **Analytic side:** The sinc² operator at the critical-line fold threshold r=1/2
3. **Bridge:** One exact mixed formula and one strong numerical approximation connecting them

The research session produced a hardened memo (`PRIME_PI_PHI_BRIDGE_HARDENED.md`) with all claims graded as Theorem / Corollary / Proposition / Approximation / Non-result / Open Question.

---

## FILES IN THIS PACKAGE

```
CLAUDECODE_BRIDGE_SPRINT_README.md       ← this file
PRIME_PI_PHI_BRIDGE_HARDENED.md         ← the submission-grade memo
PRIME_PI_PHI_BRIDGE_MEMO.md             ← original draft (kept for reference)
```

---

## TASK DESCRIPTION

### Primary task: Formalize and verify all proofs in the memo

The hardened memo contains 7 items in the proof register (A1–B3). ClaudeCode should:

1. **Verify each proof sketch using SymPy (symbolic):**

   - A1: Cyclotomic polynomial degree computation  
     `sympy.cyclotomic_poly(2*p, x).degree()` and Euler phi comparison
   
   - A2: Minimal polynomial of `2*cos(pi/5)` equals `x**2 - x - 1`  
     `sympy.minimal_polynomial(2*cos(pi/5), x)` should return `x**2 - x - 1`
   
   - A3: Gauss sum for Legendre symbol mod 5 equals √5  
     Manual computation: `sum(legendre_symbol(k,5)*exp(2πik/5) for k in range(5))`
   
   - B1: `sinc²(1/2) = 4/π²`  
     Symbolic: `sin(pi/2)**2 / (pi/2)**2 == 4/pi**2`
   
   - B2: `d/dr sinc²(r)` at `r=1/2` equals `−16/π²`  
     Symbolic differentiation and substitution
   
   - B3: `sinc²(1/5) = 25(3−φ)/(4π²)`  
     Symbolic: verify `sin**2(pi/5) == (3 - (1+sqrt(5))/2)/4`

2. **Generate a verification script** (`verify_bridge.py`) that:
   - Runs all 7 proofs symbolically via SymPy where possible
   - Falls back to high-precision numerical verification (mpmath, 50+ decimal places) where symbolic is difficult
   - Reports PASS/FAIL for each claim
   - Outputs a clean summary table

3. **Extend the approximation audit:**
   The current audit compares 16/π² to ~10 candidates. Extend to 30+ simple irrationals and algebraic constants with height ≤ 3. Use the `sympy.nthroot_mod` and algebraic number infrastructure to be systematic. Output a ranked table of closest matches. Goal: confirm or challenge whether φ is genuinely the best simple match.

---

## SECONDARY TASKS (if time allows)

### Task 2: Check open question E2

"For each prime p ≤ 20, compute sinc²(1/p) = p²·sin²(π/p)/π² and express sin²(π/p) symbolically in terms of 2cos(π/p)."

The expected pattern: sin²(π/p) = (something involving the minimal polynomial root). Document whether a clean π–algebraic mixed formula exists for each p or only for p=5.

### Task 3: Verify the GUE test independently

Rerun the KS test for zero spacings vs Wigner surmise using a larger zero table if available. The current test uses n=49 (low power). If Odlyzko's table of 10⁵ zeros is accessible, rerun and report updated statistics. If not, note the power limitation explicitly in the memo.

### Task 4: Flag any invalid statements

Read the full hardened memo and flag any statement that:
- Exceeds its claimed precision
- Uses informal language in a theorem-marked block
- Has a proof sketch that is actually wrong or incomplete
- Could be misread as an RH-relevant claim

Return a list of flagged items with suggested fixes.

---

## CONSTRAINTS

- No RH claims — any statement that could be read as implying anything about RH must be removed or explicitly negated
- No "named constant" rhetoric in theorem statements — exact algebraic characterizations only
- No π digit patterns — all work is on algebraic/analytic structure
- No overstating the approximation — 16/π² ≈ φ must never appear in theorem-labeled blocks
- 16/π² is transcendental — the invalid minimal polynomial question has been removed; do not reintroduce it

---

## EXACT IDENTITIES TO VERIFY (quick reference)

```python
from sympy import *
x = symbols('x')
phi = (1+sqrt(5))/2
pi_s = pi

# A2: minimal poly of 2cos(π/5)
assert minimal_polynomial(2*cos(pi_s/5), x) == x**2 - x - 1

# B1:
assert simplify(sin(pi_s/2)**2 / (pi_s/2)**2 - Rational(4,1)/pi_s**2) == 0

# B2:
r = symbols('r', positive=True)
f = sin(pi_s*r)**2 / (pi_s*r)**2
df = diff(f, r)
assert simplify(df.subs(r, Rational(1,2)) + 16/pi_s**2) == 0

# B3:
assert simplify(sin(pi_s/5)**2 - (3-phi)/4) == 0
```

---

## DELIVERABLES FROM CLAUDECODE

1. `verify_bridge.py` — verification script, all 7 proofs
2. `audit_approximation.py` — extended 30+ candidate approximation audit
3. `BRIDGE_VERIFICATION_REPORT.md` — PASS/FAIL table with any corrections
4. Updated `PRIME_PI_PHI_BRIDGE_HARDENED.md` — with any corrections applied

---

## WHAT SUCCESS LOOKS LIKE

All 7 proof items verified PASS (or corrected with explanation). Approximation audit confirms φ is closest or documents a closer candidate honestly. Memo is clean, submission-ready, and would survive a referee who is specifically looking for overclaims. The word "golden tangent" appears only in informal text, never in theorem statements.
