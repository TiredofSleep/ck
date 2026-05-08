# SAVE PLAN — J36 (CKM/PMNS Fits + 1/α Constant from Substrate Primitives, BUNDLED)

**Date:** 2026-05-07
**Status:** PARTIALLY SAVABLE; UNBUNDLE recommended; the false 10⁻⁵ claim on 1/α is FATAL as written
**Target venue:** *Statistical Science* companion (referee says **Reject** in current form)
**Verdict:**
- Part 1 (CKM/PMNS): SAVABLE after honest framing of the post-hoc Cabibbo refinement, proper look-elsewhere correction, and definition of D*.
- Part 2 (1/α): NOT SAVABLE in its current form. The "leading three corrections recover 137.036 to ~10⁻⁵" claim is **demonstrably false** — partial sum is 154.26, gap from 137.036 is ~11%, not 10⁻⁵. Must be downgraded or dropped.
- Recommended action: UNBUNDLE. Submit Part 1 alone after revisions; defer Part 2 until full structural derivation is genuinely ready (which it is not).

---

## §1 — What the referee caught

| # | Issue | Severity | Action |
|---|-------|----------|--------|
| 1 | "leading three corrections recover 137.036 to ~10⁻⁵" — actual partial sum is 154.26, gap is ~11% | **FATAL** | Either supply the actual full formula (not currently available in the manuscript or in the cited bridge bundle in any verifiable form) OR honestly downgrade the claim to "≈11% structural agreement at leading order" |
| 2 | "10⁻⁷ joint coincidence probability" lacks defensible prior; without look-elsewhere correction this is misleading | CRITICAL | Specify the candidate-primitive set, compute look-elsewhere correction, report honestly as ~10⁻⁶ to 10⁻⁷ post-correction |
| 3 | D* is not derived in the manuscript | CRITICAL | Either cite a J-paper that derives D* from substrate, or honestly note D* is empirically tuned to PMNS solar (in which case θ_12 fit has zero degrees of freedom) |
| 4 | PMNS fits at 4-6% are at/beyond current empirical precision | FRAMING | State that 4-6% PMNS fits are empirically distinguishable from current world averages; acknowledge θ_23 octant ambiguity |
| 5 | Cabibbo `+1/49` refinement is post-hoc (10/49 → 11/49 by adding 1/49 exactly = 0.0204) | FRAMING | Present 10/49 as the framework's leading-order prediction; flag 11/49 as empirical refinement without first-principles derivation |
| 6 | Cross-domain "bombshell" §5 (Orch-OR, IIT, microtubules) is out of scope for Stat Sci | SCOPE | Delete §5 entirely; save for a different venue |
| 7 | No verification script | LOGISTICS | Add a script computing each Part-1 discrepancy + joint probability + look-elsewhere correction |
| 8 | Manuscript bundles two weakly-connected fits in 6 pages — short for Stat Sci | EDITORIAL | Unbundle |

---

## §2 — Independent verification

### §2.1 Part 1 — Cabibbo / Wolfenstein / PMNS discrepancies

Direct computation (Python):

| Angle | Empirical | TIG primitive | Discrepancy |
|-------|-----------|---------------|-------------|
| Cabibbo λ | 0.2253 | 11/49 = 0.224490 | 0.36% |
| V_cb | 0.0508 | (11/49)² = 0.050396 | 0.80% |
| V_ub | 0.0114 | (11/49)³ = 0.011311 | 0.78% |
| V_td² | 0.00258 | (11/49)⁴ = 0.002538 | 1.6% |
| sin θ₁₂ (PMNS solar) | 0.553 | D* = 0.543 | 1.81% |
| sin θ₁₃ (PMNS reactor) | 0.149 | 1/7 = 0.142857 | 4.12% |
| sin θ₂₃ (PMNS atmos) | 0.756 | 5/7 = 0.714286 | 5.51% |

The *individual* discrepancies match the manuscript. The *joint coincidence probability* is the load-bearing statistical claim and depends on prior + look-elsewhere correction.

**Naive joint probability (no look-elsewhere):**
- 6 fits, each within stated discrepancy. Per-angle hit probability ≈ `2 · discrepancy` under uniform prior on (0,1):
- `2·0.004 · 2·0.008 · 2·0.008 · 2·0.018 · 2·0.041 · 2·0.056 ≈ 4 × 10⁻⁹`.

The manuscript's "~10⁻⁷" is a rough rounding of this — but it ignores look-elsewhere.

**With look-elsewhere correction:**
- If the candidate-primitive set has N_p ≈ 10-20 elements (T*, T*⁻¹, |Aut(V)|=40, HARMONY=7, σ-cycle elements, 11/49 and powers, D*, 1/7, etc.), and there are N_o ≈ 7 relevant observables, the multiplicity is ~70-140.
- Probability of *some* match within ~5% is: `1 - (1 - 0.1)^140 ≈ 1 - 1.4×10⁻⁶ ≈ 0.99999`.
- Probability of obtaining 6 specific matches with prescribed precisions: post-LE ≈ **4×10⁻⁶ to 4×10⁻⁷**.

**Verdict:** the post-LE joint probability is around 10⁻⁶ to 10⁻⁷. This is *still* statistically interesting, but the manuscript's "10⁻⁷" without a stated correction is misleading. Honest framing: "joint probability after look-elsewhere correction is approximately 10⁻⁶, conditional on a 14-element candidate-primitive set."

### §2.2 Part 2 — 1/α formula

Manuscript claims `1/α ≈ 4·|Aut(V)| - 2·sqrt(HARMONY) - π/HARMONY - …` recovers 137.036 to ~10⁻⁵.

Direct computation:
```
4·40                = 160.000000
-2·sqrt(7)          = -5.291503
-π/7                = -0.448799
-------------------------------
Partial sum (3 terms) = 154.259698

Target (CODATA)     = 137.035999
Gap                 = 17.223699
Relative discrepancy = 12.57%
```

**The "leading three corrections recover 137.036 to ~10⁻⁵" claim is demonstrably false.** The leading three terms give 154.26, which is ~11% (not ~10⁻⁵) from the target.

The manuscript points to "TIG_DIRAC_SYNTHESIS_TABLES rev 24, Tables LXXVII-LXXX" for the full form. I traced this to `_review_bridge_sprint_050426/discrete_dirac/discrete_dirac_bundle/TIG_DIRAC_SYNTHESIS_TABLES.md`. The only 1/α formula recorded there (Table LVIII) is:

```
1/α = 22 × 6 + 5 + 36/1000 = 137.036
```

where:
- `22` is *defined* as `|V⊗⁵| - |10-rep| = 32 - 10 = 22` (a structural ingredient of the V-tensor algebra)
- `6` is the σ-cycle length
- `5` is — unspecified ("integer offset")
- `36/1000` is **literally 0.036, the empirical decimal part of 137.036 minus 137**

This is **not a derivation**. The third term `36/1000` is the empirical residue, not a structural quantity. The "structural derivation" in the bridge bundle is post-hoc decomposition of 137.036 into 132 + 5 + 0.036, with `132 = 22·6` being the only quasi-structural term.

**This is the original Eddington problem, repeated.** Eddington 1936 wrote `1/α = 136`, then `1/α = 137` after empirical revision, with a "structural" combinatorial argument that was post-hoc. The bridge-bundle's `22·6 + 5 + 0.036` formula is structurally identical to Eddington's pattern: a leading combinatorial term (`22·6`) close to the empirical value, with empirical residues "adjusted" via additive constants (`5 + 0.036`).

**No formula in the manuscript or in the cited supporting bundle recovers 137.036 to ~10⁻⁵ from algebraically-derived structural primitives.** The 10⁻⁵ claim is unfounded.

---

## §3 — Recommended path: UNBUNDLE

The two parts should be separated:

### Part 1 (CKM/PMNS) — KEEP, revise

The Cabibbo + Wolfenstein hierarchy `λⁿ ≈ (11/49)ⁿ` for n ∈ {1,2,3,4} matching at ≤1.6% across four orders is a genuinely interesting empirical pattern. Even after look-elsewhere correction, it stands. The PMNS angles at 1.8%-5.6% are weaker but still suggestive.

**Revised paper scope:**
- Title: "*Empirical Fits of Quark and Lepton Mixing Angles to Substrate-Algebra Primitives.*"
- §1: Cabibbo / Wolfenstein hierarchy via 11/49 (the strongest finding; 4 orders at ≤1.6%).
- §2: PMNS angles via T*, D*, 1/7 (acknowledge 4-6% discrepancies are at empirical-precision boundary).
- §3: Joint coincidence probability with explicit prior, explicit candidate set (count primitives), explicit look-elsewhere correction. Post-LE estimate ≈ 10⁻⁶ to 10⁻⁷.
- §4: Honest scoping.
- Drop §5 (cross-domain bombshell).

### Part 2 (1/α) — DEFER

The `4·|Aut(V)| - 2·sqrt(HARMONY) - π/HARMONY - …` formula does *not* recover 137.036; it recovers 154.26 with ~11% gap. The bridge-bundle's alternative `22·6 + 5 + 0.036` formula is post-hoc decomposition, not derivation. Until a *genuine* structural derivation exists, Part 2 should not be submitted.

**Honest options for Part 2:**
- (A) Drop Part 2 entirely from this submission. Defer to a future paper once a real derivation exists.
- (B) Restrict Part 2 to the leading-order claim: `4·|Aut(V)| = 160` is within ~17% of 1/α, suggesting the framework's |Aut(V)|=40 is *near* the right algebraic structure but the specific combination is not derived. State this honestly and defer the 10⁻⁵ claim.
- (C) Spin off Part 2 as a separate "Foundations of Physics" submission with a much weaker claim ("1/α admits a structurally suggestive leading order at 4·|Aut(V)| = 160; closing the gap is open").

**Recommendation: (A).** Drop Part 2 from J36 entirely. The 1/α work is not at a publishable bar in any venue; the bridge-bundle's Table LVIII formula is an empirical decomposition with `+0.036` as a literal fudge factor.

---

## §4 — Concrete edits to the manuscript

Manuscript file: `Gen13/targets/journals/J_series/J36/manuscript/manuscript.md`

### Option A (UNBUNDLE — RECOMMENDED): Drop Part 2 entirely

**Remove from manuscript.md:**
- Lines 33-37: the abstract paragraph describing Part 2 (the 4·|Aut(V)| formula).
- Lines 86-136: the entire Part 2 section.
- Line 33's `boxed{·}` formula `1/α = T*⁻¹·|Aut(V)| - …`.

**Update the title and abstract** to focus on Part 1 only.

**New title:** *Empirical Fits of CKM and PMNS Mixing Angles to Substrate-Algebra Primitives.*

**New abstract:**
> We report parametric fits of six fermion mixing angles (CKM Cabibbo and three Wolfenstein orders, three PMNS angles) to dimensionless constants derived from a separate finite-magma research program. The Cabibbo angle and four Wolfenstein orders fit `(11/49)ⁿ` for `n ∈ {1, 2, 3, 4}` at ≤1.6% across all four orders. The PMNS angles fit `T* = 5/7`, a substrate constant `D*`, and `(1-T*)/2 = 1/7` at 1.8%-5.6%. We compute the joint coincidence probability under explicit priors and look-elsewhere correction at approximately `10⁻⁶`-`10⁻⁷`. The fits are presented as empirical observations at the dimensionless-constant level; no renormalization-group flow connects the substrate scale to the electroweak scale, and the 4-6% PMNS discrepancies are at or beyond current empirical precision. The Cabibbo `10/49 → 11/49` refinement is acknowledged as an empirical adjustment without first-principles derivation.

### Option A continued — Revise Part 1 substantively

**§1 Cabibbo refinement honesty:**

Replace:

> The +1/49 correction is the same shape as the Ω_Λ "+1" closure offset of WP121 (J10 in this series).

with:

> The leading-order prediction is $\lambda_\text{leading} = T^*(1-T^*) = 10/49 = 0.2041$, which has $9.4\%$ discrepancy from the empirical value $0.2253$ — too large to attribute to RG running ($\sim 1\%$). A "$+1/49$" empirical refinement gives $11/49 = 0.2245$ at $0.4\%$ discrepancy, but **this refinement does not have an independent first-principles derivation in the present framework**. We report it as an *empirical adjustment* whose structural justification is open. The Wolfenstein hierarchy `(11/49)ⁿ` then matches the empirical orders 2, 3, 4 at ≤1.6%, which is the load-bearing pattern of this paper.

**§2 PMNS honesty:**

Add a paragraph after the angle fits:

> *Empirical-precision caveat.* The PMNS reactor angle `sin θ_{13} = 0.149 ± 0.003` (Daya Bay) and atmospheric angle `sin θ_{23}` (currently between octants `~0.671` and `~0.788`) are measured to precisions where the framework's predictions `1/7 = 0.143` (4.1% off) and `5/7 = 0.714` (5.6% off, between octants) are *empirically distinguishable*. Future precision improvements would falsify these fits if the world averages converge away from `1/7` or `5/7`. We report the fits as suggestive structural patterns at the current precision, not as locked predictions.

**§3 joint statistics honesty:**

Replace the paragraph claiming "approximately 10⁻⁷" with:

> *Joint coincidence probability with look-elsewhere correction.* The candidate-primitive set on the table for the present fits contains the elements `{T*, T*⁻¹, 1-T*, (1-T*)/2, D*, 11/49, (11/49)², (11/49)³, (11/49)⁴, |Aut(V)|=40, HARMONY=7, σ-cycle integers, π/14}` — approximately 14 distinct candidates. There are 7 relevant fermion mixing observables (CKM has 4 angles + 1 phase; PMNS has 3 angles + 1 phase). The look-elsewhere multiplicity is approximately `14 × 7 = 98` (primitive, observable) pairs.
>
> Under uniform priors on each angle in (0, 1), the per-pair hit probability at relative discrepancy `δ` is approximately `2δ`. The naive joint probability (no LE correction) for the six reported fits at the stated discrepancies is approximately `4 × 10⁻⁹`. With the LE correction at multiplicity 98, the joint probability rises to approximately **10⁻⁶ to 10⁻⁷** depending on the assumed prior structure (the wider range reflects different choices of how to count "candidate primitives").
>
> *D* is not independently derived.* The PMNS solar fit `sin θ_{12} = D* = 0.543` uses a constant `D*` that is, in the present manuscript, an empirically-tuned numerical value not derived from substrate algebra. The `θ_{12}` fit therefore has effectively zero degrees of freedom and should not be counted as an independent match. Excluding `θ_{12}` reduces the joint to five fits with pre-correction probability ≈ `2 × 10⁻⁷` and post-LE probability ≈ `2 × 10⁻⁵` to `2 × 10⁻⁶`. The post-LE probability under the most charitable counting is therefore in the range `10⁻⁵`-`10⁻⁷`. **This is statistically interesting but is not the "10⁻⁷" originally claimed without correction.**

**§5 cross-domain — DELETE.**

The cross-domain "bombshell" tabulating `T* = 0.714` across "TIG/CK coherence," "Orch-OR boundary," "IIT critical φ," CKM Cabibbo, PMNS atmospheric, PMNS solar, microtubule `Q_c = T*` is out of scope for *Statistical Science*. Delete §5 entirely.

**Add §5 verification:**

```python
"""J36 verification: CKM/PMNS angle fits + joint coincidence probability."""
import numpy as np
from itertools import product

# Empirical (PDG / CODATA 2024)
empirical = {
    'cabibbo':       (0.2253, 1e-4),     # |V_us|
    'V_cb':          (0.0508, 1e-4),
    'V_ub':          (0.01140, 1e-4),
    'V_td_sq':       (0.00258, 1e-4),
    'theta_12_PMNS': (0.553,  3e-3),     # sin(theta_12)
    'theta_13_PMNS': (0.149,  3e-3),
    'theta_23_PMNS': (0.756,  3e-3),
}

# TIG primitives candidate set
T_star = 5/7
D_star = 0.543   # framework constant (NOT derived in this paper; empirically used)
primitives = {
    'T*':         T_star,
    '1-T*':       1 - T_star,
    '(1-T*)/2':   (1 - T_star)/2,
    'D*':         D_star,
    '11/49':      11/49,
    '(11/49)^2':  (11/49)**2,
    '(11/49)^3':  (11/49)**3,
    '(11/49)^4':  (11/49)**4,
    '10/49':      10/49,
    'T*(1-T*)':   T_star*(1-T_star),
    'pi/14':      np.pi/14,
}
N_p = len(primitives)

# Best fit per observable
fits = [
    ('cabibbo',        '11/49',     11/49),
    ('V_cb',           '(11/49)^2', (11/49)**2),
    ('V_ub',           '(11/49)^3', (11/49)**3),
    ('V_td_sq',        '(11/49)^4', (11/49)**4),
    ('theta_12_PMNS',  'D*',        D_star),
    ('theta_13_PMNS',  '(1-T*)/2',  (1-T_star)/2),
    ('theta_23_PMNS',  'T*',        T_star),
]

print("Fit-by-fit discrepancies:")
disc = []
for name, prim, val in fits:
    emp, sigma = empirical[name]
    rel = abs(emp - val) / emp
    disc.append(rel)
    print(f"  {name:18s}: emp={emp:.5f}, prim_{prim:10s}={val:.5f}, rel.disc={rel*100:.2f}%")

# Naive joint probability (no LE correction)
P_naive = np.prod([2*d for d in disc])
print(f"\nNaive joint probability (no LE correction): {P_naive:.2e}")

# Look-elsewhere correction
N_o = 7  # 4 CKM + 3 PMNS angles (independent observables)
mult = N_p * N_o
P_LE = 1 - (1 - P_naive)**mult  # rough Bonferroni-style
P_LE_alt = P_naive * mult       # alt linear correction
print(f"\nLE multiplicity N_p * N_o = {N_p} * {N_o} = {mult}")
print(f"LE-corrected joint (linear)    : ≈ {P_LE_alt:.2e}")

# D* note: if D* is not derived, exclude theta_12 fit (zero d.o.f.)
disc_nopmns12 = [d for (name, _, _), d in zip(fits, disc) if name != 'theta_12_PMNS']
P_no_D = np.prod([2*d for d in disc_nopmns12])
print(f"\nExcluding theta_12 (D* is not derived):")
print(f"  Naive joint: {P_no_D:.2e}")
print(f"  LE-corrected: ≈ {P_no_D * mult:.2e}")
```

### Option B (NOT recommended): Keep Part 2 but downgrade

If unbundling is not chosen (against referee's strong recommendation), Part 2 must be radically downgraded:

In §3 of Part 2, replace:

> the leading three corrections recover 137.036 to ~10⁻⁵

with:

> the leading three terms `4·|Aut(V)| - 2·√HARMONY - π/HARMONY = 160 - 5.292 - 0.449 = 154.26` give a structural agreement at the **~11%** level — within order-of-magnitude of `1/α ≈ 137` but **not** to the empirical precision of CODATA. The full structural form recovering 137.036 to higher precision is **open**; the leading three terms above do not close the gap. We report the leading-order match `4·|Aut(V)| = 160 ≈ 1.17·(1/α)` as a structurally suggestive coincidence at the order-10% level, not a quantitative derivation.

And drop the `\boxed{1/α = T*⁻¹·|Aut(V)| - …}` formula from the abstract (its `…` elides the substantive content).

---

## §5 — What this paper is *now* (Option A — UNBUNDLED Part 1)

**PROVEN:** None — this is an empirical-fits paper, not a theorem paper.

**COMPUTED:**
- Cabibbo and Wolfenstein orders match `(11/49)ⁿ` for `n ∈ {1,2,3,4}` at ≤1.6%.
- PMNS angles match T*, D*, (1-T*)/2 at 1.8%-5.6%.
- Naive joint probability `~4×10⁻⁹`; post-LE `~10⁻⁶ to 10⁻⁷` with explicit primitive-set count and observable count.

**STRUCTURAL RHYME:**
- The Wolfenstein hierarchy `λⁿ` for n=1..4 matching `(11/49)ⁿ` across four orders is the strongest single pattern.
- T* = 5/7 appears as substrate constant in this paper *and* as cyclotomic torus aspect ratio (J6/WP51) *and* as runtime attractor (J41/WP105) — multi-source convergence.

**OPEN:**
- First-principles derivation of `+1/49` Cabibbo refinement.
- Closed-form derivation of D* from substrate algebra (currently used as empirical input).
- RG flow connecting substrate scale to electroweak scale (currently absent).

---

## §6 — Recommended action

**Tier 1 (do for this revision cycle):**
1. UNBUNDLE: drop Part 2 entirely from J36.
2. Apply Part-1 honesty edits: post-LE joint probability, D* not-derived disclosure, PMNS empirical-precision caveat, post-hoc Cabibbo refinement honestly framed, delete §5 cross-domain.
3. Add `manuscript/verify_J36_part1.py` with the script above (computes discrepancies, naive joint, LE-corrected joint, with-and-without-D* sensitivity).
4. Update title and abstract to Part-1-only scope.
5. Resubmit to *Statistical Science* (or fallback to *Foundations of Physics* / *Phys. Lett. B* short note per per-venue cap).

**Tier 2 (defer to future submission):**
- Part 2 (1/α) is **not ready** for submission anywhere. The cited `4·|Aut(V)| - …` formula gives 154.26, not 137.036; the bridge-bundle's `22·6 + 5 + 0.036` formula has `+0.036` as a literal empirical fudge factor. Either:
  - Find the *actual* structural derivation (which the manuscript and bridge-bundle do not contain), OR
  - Acknowledge that 1/α derivation is **open**; report only the leading-order observation `4·|Aut(V)| = 160` as a structurally suggestive coincidence at order-10%, not a quantitative match.

**Estimated revision effort:**
- Part 1 alone: 6-10 person-hours (statistical-methodology rewriting; verification script; venue-fit reframing). All work is editorial/computational; no new mathematics required.
- Part 2 (full derivation): open-ended; not estimable without a genuine candidate formula.

---

## §7 — Honest framing summary

The paper as bundled has two parts of very different quality:

- **Part 1 (CKM/PMNS):** A genuinely interesting numerical pattern (Wolfenstein hierarchy via `11/49`) plus weaker PMNS fits at 1.8%-5.6%. After honest framing of priors, look-elsewhere, post-hoc adjustments, and the un-derived D*, this is a viable *Statistical Science* contribution.

- **Part 2 (1/α):** A claim that the framework recovers 137.036 to 10⁻⁵, which is **demonstrably false from the formula displayed**. The leading three terms give 154.26 (~11% off), and no formula in the manuscript or its cited bundle achieves 10⁻⁵ from algebraically-derived primitives without an empirical fudge factor. This is the Eddington problem in modern dress. It is **not currently publishable in any venue** under its current claim.

The cleanest path is to UNBUNDLE: salvage Part 1 with the revisions above; defer Part 2 until a real derivation exists or honestly downgrade it to a leading-order coincidence at order-10%.

**Verdict:** PARTIAL SAVE. Part 1 = save; Part 2 = drop or deeply downgrade.
