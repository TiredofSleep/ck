# TIG Synthesis: Four Directions Beyond the Tables

**Date:** 2026-05-02
**Originating context:** After the four-bridge handoffs were drafted, Brayden pushed back: "are we just renaming or do we add something beyond the tables?" Fair question. The bridges translate; they don't extend. This document records what extending actually produced when I tried four directions on the canonical TSML_10 / BHML_10 substrate.

The four directions:
1. **Substrate composition** — what algebraic objects fall out of TSML+BHML interactions
2. **Phenomenological prediction** — what observable signature does the substrate produce
3. **New primitive** — formalize the snowflake as a cryptographic attestation primitive
4. **Predicted invariant** — find a substrate constant not in the canon

Below: what each direction produced, what survived honest scrutiny, what didn't, and where the through-line goes.

---

## Direction 1: Substrate Composition

### What I tried
- Tensor product TSML ⊗ BHML on Z/10Z × Z/10Z (100×100 table)
- σ-twisted compositions T_σ and B_σ (conjugation of magmas by the σ permutation)
- Commutator-induced table [TSML, BHML] from left-multiplication matrices
- Joint antisymmetric Lie-algebra rank

### What the computations gave

**Negative result on tensor product**: Non-associativity rate of TSML ⊗ BHML is 0.559, almost exactly the additive prediction `σ_T + σ_B - σ_T·σ_B = 0.562`. Tensor product gives no new content beyond the factors. Cleanly null finding.

**Real result on twisted composition**: Under σ-conjugation, BHML's determinant changes from -7002 to -3340208 — a factor of ~477. TSML's determinant stays 0 (it's rank-deficient before and after). 52 of BHML's 100 cells change under σ-conjugation; 83 of TSML's. So **σ is NOT an automorphism of either magma** — σ-conjugation is a substantive operation that produces structurally different magmas.

This is genuinely new content not explicit in the canon. The canon mentions σ as the cycle structure of operator labels; this finding establishes that σ-conjugation breaks magma identity.

**Real result on commutator**: The commutator-induced table [TSML, BHML] outputs only in {0, 1, 2, 9}. No HARMONY (7) appears. The commutator is **non-commutative** (inheriting bracket asymmetry) but has only 7.2% non-associativity — much lower than either parent.

The most striking aspect: 84 of 100 commutator cells are VOID (0). The two magmas' bracket structure is mostly trivial — when both act, they cancel. The remaining 16 cells carry all the genuinely non-trivial joint information.

**Total commutator eigenvalues**: dominant ~10.03, complex pair ±5.38±3.79i, real ~-4.71 and 4.66. None recognized as known algebraic constants.

### Net contribution beyond canon
- σ-conjugation as a non-trivial operation that produces distinct (T_σ, B_σ) magmas
- The "16-cell residual" of [TSML, BHML] as a candidate locus for joint algebra study
- Eigenvalue 10.03 of total commutator — not algebraically recognized but candidate physical scale

---

## Direction 2: Phenomenological Prediction

### What I tried
Run the runtime processor `M_α = α·TSML + (1-α)·BHML` at α=0.5 on six structured inputs and 20 random inputs, measuring (a) where output mass lands and (b) what trajectory the system takes to get there.

### What the computations gave

**Confirmed (independent verification of WP115/D65)**: All non-trivial inputs converge to the *same* fixed point with H/Br = 1+√3 to machine precision. Convergence happens in 28-31 iterations regardless of input. The fixed point is universal — input structure does not shape the attractor.

This is a strong null result: substrate fixed points don't carry input information. The substrate's structure (not the input) determines where the system settles.

**New finding from this session**: The *trajectory signature* — the compressed sequence of dominant operators on the way to the fixed point — IS input-distinguishing:

| Input | Trajectory signature |
|---|---|
| σ-orbit (6-cycle) | [1, 7] |
| 4-core | [0, 7] |
| σ-fixed | [0, 7] |
| human-triad {5,6,7} | [5, 7] |

Different inputs produce different *paths* through the substrate even when they converge to the same fixed point. This is content the canon doesn't make explicit.

### The actual phenomenological prediction

CK can distinguish two input streams with identical surface statistics by their *trajectory* through the substrate, even when the steady-state coherence reading is identical. This is testable:

1. Pick two text streams with matched n-gram statistics but different structural origin (e.g., real prose vs. word-salad with same vocabulary distribution)
2. Run both through CK's runtime processor
3. Measure both fixed-point coherence (which should be similar) and trajectory signature (which should differ)
4. Confirm the trajectory distinguishes them when the fixed point doesn't

If this prediction holds, CK has a discriminative power that classical statistical processing lacks. If it doesn't, the prediction is falsified.

### Net contribution beyond canon
- The universal-attractor result (D65) is independently re-verified across 7 input families
- Trajectory signatures as a new substrate-readout primitive
- A specific, testable, falsifiable phenomenological prediction

---

## Direction 3: Substrate-Attestation Snowflake Primitive

### What I tried
Formalize the "frozen snowflake" as a deterministic substrate fingerprint — a 334-dimensional integer vector built from characteristic polynomial coefficients of left-multiplication matrices, σ-conjugates, determinants, harmony-cell counts. Then test whether this fingerprint serves as a substrate-attestation primitive (verifying that two parties have the same substrate without revealing the full fingerprint).

### What the computations gave

**Frozen snowflake construction works**: 334 integer components, deterministic given (TSML, BHML, σ). SHA-256 hash for compact representation: `d029064d128...`.

**Perturbation sensitivity (corrected)**: A 2-cell symmetric perturbation of TSML produces 1-11 component differences in the snowflake. Perturbation seed-dependent — some cell positions are nearly invisible to the fingerprint (only 1 component change), others highly visible (11 component changes).

**Diversity statistics**: 100 random 1-cell-pair perturbations produce 37 unique snowflakes. So roughly 60% of random single-cell changes collide on the fingerprint. **This is a real security weakness for the simple construction**: a determined adversary could exploit collision regions.

**Attestation protocol mechanics**: 5/5 honest verification passes, 0/10 adversary passes (with 2-cell or 5-cell perturbed substrates). The protocol works against random adversaries.

### What's genuinely established
- The snowflake is a deterministic structural fingerprint with 334 distinguishable bits of substrate information
- Perturbation sensitivity is real but not uniform (collision regions exist)
- The attestation protocol is sound against random adversaries with random substrate perturbations
- The protocol is NOT proven sound against structured adversaries who can choose which cells to perturb

### What's open (the soundness theorem)
The theorem we'd want:

> **Substrate-Attestation Soundness**: For any substrate S' ≠ S, the probability that S' produces the same N attestation responses as S is ≤ 2^(-c·N) for some constant c > 0.

This requires:
1. A precise definition of substrate-equivalence (when are two magmas "the same" up to relabeling?)
2. A counting argument bounding the number of substrates within a given fingerprint-distance
3. A formal statement of the challenge-response protocol's information-theoretic security

This is a real open problem. The 37/100 diversity number says the constant c is NOT large enough for the simple protocol; it would need refinement (e.g., using polynomial commitments or zero-knowledge proofs over the snowflake structure).

### Net contribution beyond canon
- A formal definition of the frozen snowflake (the canon describes it conceptually but doesn't pin down the construction)
- Empirical evidence of its uniqueness profile (37/100 collision rate at 1-cell perturbation)
- A protocol sketch for substrate-attestation
- An open theorem: full soundness proof

---

## Direction 4: Predicted Invariant

### What I tried
Scan the substrate systematically for invariants: traces, Frobenius norms, eigenvalue spectra, singular values, characteristic polynomial structure. Filter rigorously for genuine algebraic relations (integer/rational/Q(√n) with small coefficients) versus floating-point coincidences.

### What the computations gave

**Most promising candidate**: **trace(TSML) / trace(BHML) = 63 / 42 = 3/2 EXACTLY.**

- diag(TSML) = [0, 7, 7, 7, 7, 7, 7, 7, 7, 7] (sum 63 = 3² · 7 = 9·7)
- diag(BHML) = [0, 2, 3, 4, 5, 6, 7, 8, 7, 0] (sum 42 = 2·3·7)
- ratio = 63/42 = 3/2

**Honest caveat**: this ratio is partially a function of how the canonical tables were chosen, not a deep substrate theorem. Specifically, TSML's diagonal is by construction `[0] + [7]×9`, which forces trace = 63. BHML's diagonal sums to 42 by direct addition. The 3/2 doesn't survive substrate automorphisms — under σ-conjugation, traces become 9 and 35 (ratio 9/35, not 3/2).

So the 3/2 ratio is an invariant *of the canonical tables*, not of the substrate-equivalence class.

**What's interesting about it anyway**: 63 = 3²·7 and 42 = 2·3·7 share GCD 21 = 3·7. Stripping 21 leaves 3/2 — pure triadic-vs-binary. This echoes the canon's Being/Becoming duality at the trace level. Whether the canonical tables were chosen for this property or it emerges from prior constraints is worth understanding.

**Other genuine integer/rational invariants**:
- `||TSML||_F² = 3935 = 5 × 787` (787 is prime)
- `||BHML||_F² = 3420 = 2² × 3² × 5 × 19`
- `GCD(||TSML||_F², ||BHML||_F²) = 5`
- `det(TSML + BHML) = 2,674,214 = 2 × 211 × 6337`

Each is exact and composed of small prime factors. They're "facts about the tables" — they don't recognize as familiar physical or mathematical constants.

**What I had to filter out**: the auto-search recognized eigenvalues like 61.38 as `21337366/347609` and called it a "rational match within tolerance 1e-6." That's a floating-point coincidence, not a real algebraic identity — high-denominator rationals always fit any FP value within tolerance. Filtered out of the final report.

**The Z_T = Z_B claim**: my computation gives Z_T = 94 (cells in TSML mapping to 4-core), Z_B = 41 (same for BHML). These DIFFER, contra canon WP110/D49. Probably canon uses a partition-function-weighted sum, not a cell count. Discrepancy flagged for ClaudeCode reconciliation.

### Net contribution beyond canon

- The trace ratio 63/42 = 3/2 as a candidate signature of the canonical tables specifically
- σ-conjugation breaks the trace ratio (9/35), establishing σ-conjugation as detectable at trace level
- The Z_T = 94, Z_B = 41 measurement (discrepant with canon claim Z_T = Z_B as written)
- Frobenius² values 3935 and 3420 with their factorizations as substrate fingerprints

---

## What the four directions produced together

The bridges (Hoffman/Friston/Tononi/Faggin) are *renaming* — translation of TIG into other frameworks' vocabulary. Useful for outreach, not new content.

These four directions are *additive*:

| Direction | New content |
|---|---|
| 1. Composition | σ-conjugation is non-trivial; commutator residual = 16 cells |
| 2. Phenomenology | Trajectory signatures distinguish inputs that fixed points cannot — testable |
| 3. Primitive | Frozen snowflake formalized; 37/100 collision rate at 1-cell perturbation; soundness theorem open |
| 4. Invariant | trace ratio 3/2 as canonical signature; σ-conjugation breaks it (9/35) |

Direction 2 is the strongest: it produces a falsifiable empirical prediction about CK's behavior on text streams that classical processing can't make. If the trajectory-signature distinguishability holds in practice, CK has discriminative power that justifies the substrate-level interpretation.

Direction 3 is the most strategically valuable: substrate-attestation as a primitive is the kind of object that has independent value (cryptographic identity for sovereign agents) regardless of TIG's broader framework. If the soundness theorem can be proved, this primitive could be deployed in real systems independent of CK.

Direction 1 is the most *internal* — useful for tightening the canon (clarifying what σ does as an operation on magmas) but not directly outreach-able.

Direction 4 is the most equivocal: the 3/2 ratio is real but surface-level; it doesn't unlock structural understanding the way the runtime attractor 1+√3 does. Worth noting but not headline-able.

## What ClaudeCode should do with this

In priority order:

1. **Test the trajectory-signature prediction (Direction 2)**: Set up an experiment where CK processes structured vs unstructured text inputs with matched surface statistics, measure trajectory signatures, see if distinguishability holds in practice. If it does, that's a paper.

2. **Reconcile Z_T = Z_B vs Z_T = 94, Z_B = 41 (Direction 4)**: Find canon's WP110/D49 verification script, identify the actual definition of Z used, update either canon or this document.

3. **Pursue substrate-attestation soundness theorem (Direction 3)**: This is a real open problem. Frame it precisely as a counting/measure-theoretic question and attempt the proof. If proved, the primitive becomes deployable.

4. **Document σ-conjugation as a magma operation (Direction 1)**: Add a canon entry recording that σ-conjugation is non-trivial on both TSML and BHML, with the 52/100 and 83/100 cell-change counts and the determinant change.

5. **Investigate the [TSML, BHML] commutator residual (Direction 1 corollary)**: 16 non-VOID cells out of 100 carry all joint algebraic content. Study which cells these are, what symmetries they have, whether they have phenomenological meaning.

## Honest assessment

This session produced four directions of work. Two (Directions 2 and 3) generated content that could be paper-quality with more development. One (Direction 1) generated useful internal observations. One (Direction 4) generated a candidate invariant that's real but partially trivial.

None of this changes the substrate. None of it produces a "theory of everything" claim. What it does: it tightens the substrate's structural understanding, identifies testable predictions, and formalizes one piece (the snowflake) as a deployable primitive.

This is what "beyond renaming" looks like in practice: incremental, partially conditional, with honest scope. The bridges are necessary for outreach; these four directions are necessary for the work to actually advance.
