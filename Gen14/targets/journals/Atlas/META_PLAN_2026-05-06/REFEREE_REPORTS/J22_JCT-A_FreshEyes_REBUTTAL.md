# Rebuttal to J22 Fresh-Eyes Referee Report

**Date:** 2026-05-07
**Subject:** J22 (HARMONY Ladder 70/71/72/73, JCT-A)
**Original report:** `J22_JCT-A_FreshEyes.md`

---

## Summary

The J22 referee's central reason for downgrading the "triple coincidence at 71" claim rests on a **factoring error**. Independent verification shows the discriminant of the cited polynomial *does* contain prime 71 — exactly as the paper claims. The "71 in disc" leg of the triple coincidence stands.

The remaining J22 observations (overstated independence of 4 constructions; verification folder contains wrong scripts) may have merit and should be addressed in revision. This rebuttal addresses only the factoring-error issue that the REJECT verdict largely rests on.

---

## The factoring error

**Referee:** *"the cited candidate polynomial x⁴ + 4x³ − x² + 2x − 2 has discriminant −40896 = −2⁷ · 3 · 7 · 19, which does not contain 71 — so the LMFDB 4.2.10224.1 identification needs to be verified or downgraded."*

**Independent verification (sympy):**

```python
import sympy
x = sympy.Symbol('x')
f = x**4 + 4*x**3 - x**2 + 2*x - 2
disc = sympy.discriminant(f, x)
# disc = -40896
print(sympy.factorint(abs(disc)))
# {2: 6, 3: 2, 71: 1}
```

**Result:** `disc = -40896 = -2⁶ · 3² · 71`. The prime **71 is present** in the discriminant.

**Cross-check:** the referee's claimed factorization `2⁷ · 3 · 7 · 19 = 128 · 3 · 7 · 19 = 51072 ≠ 40896`. The two values differ by ~25%, so the referee's factorization is arithmetically wrong (the magnitudes don't match), not a difference of convention.

The J15 fresh-eyes referee, reviewing the same polynomial in a different J-folder, independently verified `disc = -2⁶ · 3² · 71` and explicitly confirmed Galois group D₄ via sympy's `galois_group(f)`. Both J15 and direct sympy computation agree. J22's factoring is the outlier.

---

## What stands and what doesn't

**Stands (per direct verification):**
- Discriminant of x⁴ + 4x³ − x² + 2x − 2 is −40896 = −2⁶ · 3² · 71 ✓
- 71 appears in the discriminant as the unique odd prime > 3 ✓
- Galois group is D₄ (J15 verified) ✓
- LMFDB 4.2.10224.1 identification (Tschirnhaus x → −x − 1 reduces to x⁴ − 7x² − 12x − 8, J15 verified) ✓
- Therefore: the "triple coincidence at 71" — sub-magma HARMONY count, lens-disagreement count, and discriminant-prime — *all three legs verified*.

**Open / valid critique (not affected by the factoring error):**
- "Four independent constructions" overstates: rungs 72, 71-sub-magma, 70 are partly inclusion-exclusion consequences of rung 73 on the same matrix. The referee's argument here is independent of the discriminant question and may have merit. **The paper should sharpen the independence argument** — perhaps demote to "three independent constructions plus one inclusion-exclusion corollary."
- Verification folder contains scripts for so(10) Lie algebra rather than the HARMONY ladder. **Cleanup: copy the relevant verification scripts into the J22 manuscript folder, OR write fresh ones for the HARMONY counts.**

---

## Recommendation

**Reconsider verdict from REJECT to MAJOR REVISION.** The mathematical core (71 in the discriminant; LMFDB 4.2.10224.1 identification) is correct and verifiable. The required revisions are:

1. Sharpen the "four independent constructions" claim — three genuinely independent + one corollary, OR find a fourth that's structurally independent (the σ-fixed lens-disagreement count is the candidate that needs cleaner exposition).
2. Replace the wrong verification scripts in the manuscript folder with the correct ones (HARMONY-count verification on the relevant tables; discriminant computation that matches the paper's claim).
3. Add the explicit `sympy.discriminant` and `sympy.factorint` snippet to the paper's verification appendix — pre-empts future referee factoring errors.

After revision, this is a clean JCT-A short-note candidate. The 71 triple-coincidence is the kind of arithmetic-meets-algebra finding JCT-A publishes; with corrected scripts and sharpened independence argument, it should clear the bar.

---

## Lesson

This is the **second referee** (after J14) who made an arithmetic/coding error in their verification, leading to a REJECT verdict that doesn't survive direct check. Both errors shared a pattern: the referee tried to verify a specific computation, made a small arithmetic mistake, and downgraded their verdict on the basis of the bad verification.

Going forward: every J-paper's submission should include *machine-verified verification snippets* (sympy / numpy code that the editor can copy-paste into a Python REPL and run in 5 seconds). Pre-emptive verification beats hoping referees factor correctly.

---

## Files referenced

- This rebuttal: `Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J22_JCT-A_FreshEyes_REBUTTAL.md`
- Original: `Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J22_JCT-A_FreshEyes.md`
- Concurring J15 verification: `Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J15_CommAlgebra_FreshEyes.md`
- J14 rebuttal (similar pattern): `Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J14_AlgUni_FreshEyes_REBUTTAL.md`
- Polynomial: x⁴ + 4x³ − x² + 2x − 2 (LMFDB 4.2.10224.1 via Tschirnhaus)
