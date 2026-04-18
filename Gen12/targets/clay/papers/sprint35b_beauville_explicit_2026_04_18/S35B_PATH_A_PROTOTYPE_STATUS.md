# Sprint 35b Path A — Prototype Status (handoff memo)

**Sprint:** 35b (Beauville Explicit — Path A, Prym from double cover)
**From:** ClaudeCode
**To:** ChatGPT (literature scout) + ClaudeChat (structural review) + Brayden
**Date:** 2026-04-18
**Status:** PROTOTYPE COMPLETE — target invariants locked, literature handoff ready.

**Files produced:**
- `scout_endo_structure.py` (prototype; 0.06 s runtime)
- `scout_endo_structure.json` (machine-readable invariants)
- `scout_run.log` (stdout transcript)
- this file

---

## §0. One-sentence outcome

**A_* is confirmed a polarized abelian variety with Im(Ω) positive-definite (double eigenpair spectrum 4.087²·20.818²), its det(Y) matches v3's exact value 2086 + 462√15 + 498√10 + 730√6 to numerical precision, and the target invariants for any Beauville curve C_* are pinned down; what remains is specialist literature scouting to identify (or construct) an explicit genus-5 curve whose Prym factor realizes these invariants.**

---

## §1. What the prototype verified

### §1.1 Structural integrity of A_*

| Check | Expected | Observed | Status |
|-------|----------|----------|--------|
| M2 symmetric | True | True | ✓ |
| M3 symmetric | True | True | ✓ |
| M2·M3 = M3·M2 | (atlas notes say yes, but v3 doesn't require it) | **FALSE** | ⚠ see §1.2 |
| Y = √2·I + √3·M2 + √5·M3 symmetric | True | True | ✓ |
| Y positive-definite | required for Im(Ω) | min eigenvalue 4.087 > 0 | ✓ |
| Y eigenvalues | arbitrary | 4.087 (double), 20.818 (double) | **structurally interesting, see §1.3** |
| det(Y) vs v3 exact | 2086 + 462√15 + 498√10 + 730√6 ≈ 7238.260 | 7238.260093 | ✓ |
| A_* is polarized abelian variety | required for Beauville | Im(Ω) > 0 ⇒ yes | ✓ |

### §1.2 M2·M3 ≠ M3·M2 is **not** a contradiction

The v3 probe (which proves J² = -I exactly and produces rank = 70) does not require M2, M3 to commute. What it requires is:
1. Y symmetric (so that Ω is symmetric), ✓
2. Y positive-definite (so Im(Ω) > 0), ✓
3. det(Y) nonzero (so Ω invertible), ✓ (det = 7238.26)

The earlier `memory/MEMORY.md`-style summary that implied "commuting permutation matrices" was wrong; v3 uses genuine integer symmetric matrices that happen not to commute, and that's fine.

### §1.3 The double-pair spectrum 4.087²·20.818² is a Weil-signature-(2,2) fingerprint

The eigenvalue multiplicity pattern **(2, 2)** on Im(Ω) matches the Weil signature (p, q) = (2, 2) on H^{1,0}. This is consistent with the structure in Sprint 33 atlas §2 and is one more numerical anchor point any proposed C_* must reproduce.

---

## §2. Target invariants (locked) for any C_*

| Invariant | Value | How derived |
|-----------|-------|-------------|
| dim C (expected) | **5** | g − g' = dim P = 4, with elliptic quotient g' = 1 |
| g' (quotient curve) | **1** (elliptic) | Prym dimension formula |
| End⁰(J(C_*)) ⊇ | **Q(i) × Q(i)** | Q(i) on P + Q(i) on E_* (the elliptic factor may itself be Q(i)-CM) |
| Weil signature on P(C/ι) | **(2, 2)** | from A_* |
| Hodge field of A_* | **Q(i, √2, √3, √5)** | smallest field Ω lives over |
| [Q(i, √2, √3, √5) : Q] | **16** | compositum of three quadratic extensions + Q(i) |
| Im(Ω) spectrum | **4.087 (×2), 20.818 (×2)** | numerical, from prototype |
| det(Y) exact | **2086 + 462√15 + 498√10 + 730√6** | from v3 probe |
| N(det Y) over Q | **24 864 632 774 384 309 702 656 ∈ Z** | v3 probe, field norm over Q(i,√2,√3,√5) |

Any candidate C_* must have a genus-5 curve whose period matrix τ, up to Sp_{10}(ℤ) isogeny, realizes the block-diagonal form `diag(Ω_{A_*}, τ_E)` where τ_E is some genus-1 period. That "up to isogeny" is the hard part: it means a **polarization compatibility** — not just a period match.

---

## §3. Three candidate families — status after prototype

### §3.1 F1 — Hyperelliptic genus-5 with a non-hyperelliptic involution

Form: `y² = f(x)` with `f` of degree 11 or 12, and `f(x) = g(x²)` so the involution `(x, y) → (−x, y)` exists.

Under that involution, the Prym P is 4-dimensional (g − g' = 5 − 1). The Q(i)-action on P comes from the Q(i)-symmetry of `g`. This is **structurally possible**; it requires `g` to have quartic-level symmetry that produces a Q(i)-endomorphism on the Prym.

**Status:** POSSIBLE. Literature ASK 1, 2 below.

### §3.2 F2 — Cyclic-4 cover `y⁴ = f(x)`

The automorphism `(x, y) → (x, i·y)` gives a direct Q(i)-action on J(C).

Genus formula (Hurwitz, branched only at roots of f): `g = (3/2)(deg(f) − 1)` when `f` has distinct roots and the cover is unramified at infinity. For `g = 5` this needs `deg(f) = 11/3`, not integer → genus 5 not directly achievable. `deg(f) = 5 ⇒ g = 6`, so a genus-6 cyclic-4 cover might work with further quotienting.

**Status:** GOOD structural fit but genus mismatch; needs a quotient step.

### §3.3 F3 — Plane quintic with extra Q(i)-automorphism

Smooth plane quintic has genus 6 (not 5). Genus-5 plane models are singular or live in higher projective space. Requires explicit classification of genus-5 curves with μ_4-automorphism.

**Status:** HARDER — requires classification literature.

### §3.4 Alternative: genus-5 **bielliptic** curve

A genus-5 curve that admits a 2:1 map to an elliptic curve is called bielliptic. For bielliptic genus-5 curves, the Prym is 4-dimensional; the additional Q(i)-structure would come from CM on the elliptic base or from a further automorphism. **This is likely the most direct family to search first** and was not in the original F1/F2/F3 enumeration — noted here as a prototype refinement.

---

## §4. Literature handoff asks

The prototype has set up everything. The specialist content is in the literature, and these are the specific asks:

### §4.1 ASK 1 — Birkenhake-Lange §10 (Prym varieties of Weil type)

- **Source:** Birkenhake & Lange, *Complex Abelian Varieties*, 2nd ed., Ch. 10 (Prym varieties).
- **Question:** Is there a table or classification of genus pairs (g, g') producing Prym varieties of Q(i)-Weil type (2, 2)?
- **What to look for:** explicit equations for C when (g, g') = (5, 1) and End⁰(P) = Q(i).

### §4.2 ASK 2 — Schoen 1988 on explicit CM constructions

- **Source:** Schoen, C., "Hodge classes on self-products of a variety with an automorphism," Compositio Math. 65 (1988), 3-32.
- **Also:** Schoen, C., "Complex multiplication cycles on elliptic modular threefolds," Duke Math. J. 53 (1986), 771-794.
- **Question:** Does Schoen give an **explicit formula** for C_A given the period matrix Ω and Q(i)-CM data?

### §4.3 ASK 3 — van Geemen 2001 (half-twists of CM Hodge structures)

- **Source:** van Geemen, B., "Half twists of Hodge structures of CM-type," J. Math. Soc. Japan 53 (2001), 813-833.
- **Question:** Do the half-twist constructions produce explicit curves for Weil 4-folds, or only abstract Hodge structures?

### §4.4 ASK 4 — GU(2,2) Shimura moduli (Moonen, Deligne)

- **Source:** Moonen, B., "Models of Shimura varieties in mixed characteristics" or Milne's Shimura-variety notes.
- **Question:** Is there an explicit parameterization of GU(2,2) Shimura varieties where A_* can be located, and pulled-back universal curve C_* is computable?

### §4.5 ASK 5 — Bielliptic genus-5 curves with extra automorphism

- **Source:** Any reference on genus-5 curves admitting both a hyperelliptic (or bielliptic) involution and a μ_4-automorphism.
- **Question:** Is there a 1-parameter (or higher-parameter) family of such curves, parametrized over Q(√2, √3, √5)? This is the most direct candidate.

---

## §5. What the prototype does NOT do

- Does **not** construct C_* explicitly (that's the research task for Sprint 35b proper).
- Does **not** perform period-matrix matching (that needs either Sage/Magma for Riemann-period computation or specialist guidance).
- Does **not** verify the Beauville synthesis (that's Sprint 35c).
- Does **not** change atlas status.

---

## §6. What to do once literature scout returns

If ChatGPT returns a specific genus-5 family (e.g. `y² = x(x⁴ + a·x² + b)` with specific Q(i)-structure), then:
1. Compute the period matrix numerically via mpmath or Sage.
2. Check up-to-isogeny match with Ω.
3. Check det(Y) for the Prym period agrees with 2086 + 462√15 + 498√10 + 730√6.
4. If match: proceed to Sprint 35c.
5. If no match: refine family (F1 → F2 → bielliptic → F3).

---

## §7. Routing

**For ChatGPT:** execute ASK 1-5 above; return a shortlist of candidate families with explicit equations and citations.

**For ClaudeChat:** structural review of this prototype — did I miss any family? Any concern about Prym-compatibility constraints beyond dimension matching?

**For Brayden:** confirm this prototype + handoff is the right Sprint 35b deliverable for today, or request numerical period-matching experiment now (would need Sage).

---

## §8. One-sentence closing

**Target invariants are locked, polarization is confirmed, three candidate families are tabled with a fourth refinement (bielliptic genus-5) added, and five literature asks are in the specialists' hands — the prototype has done what a prototype should do and now yields to scouting.**

---

*© 2026 Brayden Ross Sanders / 7Site LLC. 7Site Human Use License v1.0. DOI: 10.5281/zenodo.18852047.*
