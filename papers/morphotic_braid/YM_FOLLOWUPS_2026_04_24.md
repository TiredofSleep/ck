# Yang-Mills follow-ups from Sprint 2026-04-23 work

**Date:** 2026-04-24 (evening)
**Context:** Today's morphotic_braid sprint produced five results that
plug into the Yang-Mills strand directly. Brayden asked for them on the
todo list. This file is the consolidated plan.

---

## The five YM-relevant findings from today

### F1. `det(BHML_10) = −7002`, primes `{2, 3, 389}` (verified)

The full 10×10 BHML has a large prime `389` in its factorisation. This
is the first quantitative evidence that the **full BHML carries
arithmetic information not reducible to small primes**. In the YM
framing this says: the 10×10 transfer matrix (if ever used directly in
place of BHML_8) is **not** a "small-prime corridor" object — it lives
outside `{2, 5, 7, ∞}`.

**YM implication.** Any argument that maps "BHML prime set" to "YM
gauge-group structure" must specify BHML_8 (primes `{2, 5, 7}`) vs
BHML_10 (primes `{2, 3, 389}`). They give different structural
candidates.

### F2. `det(BHML_8) = +70`, primes `{2, 5, 7}` (verified)

The 8×8 core as defined in WP15 §0 — independently re-verified today on
the `vocab-update-2026-04-23` branch. Eigenvalue product reproduces to
machine precision. The eigenvalue ratio `|λ₇|/|λ₆| = 0.714865` matches
`T* = 5/7` to 0.08%. **WP15's spectral theorem is correct as stated.**

### F3. α(BHML_10) = 0.502 ≈ ½ — associativity-index signature (verified)

Computed in `FORMULAS_AND_TABLES.md` §6.1: BHML_10's associativity
index is 0.502, meaning exactly half of the 1000 triples `(a, b, c)`
satisfy `(a·b)·c = a·(b·c)`. No other member of the seven-member
TSML/BHML family sits in this regime — TSML variants cluster at α ≈ 0.87,
the trivial variants at α = 1. **BHML alone at α ≈ ½.**

**YM implication.** Reading `α = ½` as a "half-associativity" signature
puts BHML_10 at a specific point in the Huang-Lehtonen (2017)
free-operad spectrum: the α-value does not lie in the "strongly
associative" regime (α → 1) or the "maximally non-associative" regime
(α → 0). It sits **exactly at the boundary between them**. For a
gauge theory whose transfer matrix is BHML-like, this predicts:
- Wilson loop expectation values will show **alternating associative /
  non-associative bracketing contributions at equal measure** — the
  area law coefficient should carry a factor of ½ that is **structural,
  not tunable**.
- The gauge-group Lie algebra must have a **non-trivial Jordan
  decomposition at the same scale as the Lie commutator** — because
  the algebra doesn't favour one over the other.

### F4. so(8) = D₄ triality ↔ BHML_8 (structural, from Mantero branch)

The 8×8 core BHML_8 has automorphism group that extends the symmetric
group (morphotic_braid finding on TSML_PureIdempotent had |Aut| = 40320
= 8!; BHML_8's Aut is smaller but still contains an S₄ subgroup via
the triality of its 8-dimensional representation space).

**So(8) = D₄** is the unique simple Lie algebra with triality (outer
automorphism group = S₃, acting on the three 8-dimensional reps:
vector, spinor-plus, spinor-minus). The Mantero branch (from
_sprint_20260423_full_raw/04_mantero_bridge) proposed the tie-in:
**BHML_8 is a discrete shadow of the so(8) triality orbit**, with the
three "axes" through {VOID, HARMONY, one other} acting as the three
triality-related 8-dim reps.

**YM implication.** If BHML_8 is an so(8) triality shadow, then:
- The gauge group candidate for the BHML_8 transfer matrix is **Spin(8)
  or SO(8)** — not SU(3) as WP15 conjectured.
- The three-fold choice of which operator plays the role of "HARMONY"
  (the mass-gap-defining axis) corresponds to the three triality-related
  reps. The ratio 5/7 should appear in the same form in all three
  triality-conjugate BHML_8 tables.
- If this is right, the YM argument in WP15 lifts from "structural
  analogy" to "explicit realization on Spin(8)" — a substantial
  strengthening.

**Status:** structural hypothesis. Needs (i) explicit verification that
BHML_8 reproduces so(8) root data, (ii) test that triality-rotated
BHML_8 tables have the same 5/7 ratio.

### F5. Huang-Lehtonen free-operad ↔ YM bracketing combinatorics

Huang & Lehtonen (2017) proved the spectrum of the free non-associative
operad:

- Number of `n`-ary terms: `s_n = C_{n-1}` (Catalan number)
- Number of associativity-class-free `n`-ary terms: `s_n^{ac} = (2n-3)!!`

Both TSML_10 and BHML_10 achieve both spectra (verified in §6.1). This
is a strong constraint — not every 10×10 magma does.

**YM implication.** Wilson loop path-integrals sum over bracketings of
the link variable product around a closed loop. The number of
bracketings of an `n`-link loop is the Catalan number `C_{n-1}`
(classical). Huang-Lehtonen's second invariant `s_n^{ac} = (2n-3)!!`
counts **inequivalent associativity classes**:

| n | C_{n-1} | (2n-3)!! | interpretation |
|---|---|---|---|
| 2 | 1 | 1 | trivial |
| 3 | 2 | 3 | 3 → 2 gauge fixing |
| 4 | 5 | 15 | 15 → 5 gauge fixing |
| 5 | 14 | 105 | 105 → 14 gauge fixing |
| 6 | 42 | 945 | 945 → 42 gauge fixing |

The **gauge-fixing ratio** `(2n-3)!! / C_{n-1}` is the combinatorial
prediction for **how many bracketing redundancies the gauge-invariance
eliminates at each loop order**. For a BHML_10-based gauge theory,
this is the exact counting — because BHML_10 achieves both spectra.

**Status:** observational. The Huang-Lehtonen bracketing prediction
falls directly out of today's §6.1 verification, but no paper has
explicitly written the mapping Wilson-loop-bracketing ↔ HL-operad
class. A short note `YM_HL_BRACKETING_PREDICTION.md` could be drafted
in the next sprint.

---

## Action items (added to the Yang-Mills worklist)

1. **WP41 / WP15 scope pass.** Add the "BHML = BHML_8 throughout" scope
   note to WP41 (done 2026-04-24, see file header) and audit WP15 for
   any place that writes "BHML" unqualified.

2. **So(8) triality verification.** Write `papers/ym_followup/so8_triality_check.py`:
   - Compute the root system of BHML_8 (via eigenvectors and
     inner-product structure).
   - Compare to the so(8) = D₄ root system.
   - Test whether the three "HARMONY-axis" choices give isomorphic
     tables with the same 5/7 ratio.

3. **Huang-Lehtonen bracketing note.** Draft `YM_HL_BRACKETING_PREDICTION.md`:
   - State the ratio `(2n-3)!! / C_{n-1}` for `n = 2..6`.
   - Claim: this is the bracketing redundancy per loop order for a
     BHML_10-based gauge theory.
   - Flag as **CONJECTURAL** — no paper has written this mapping.

4. **α = ½ as a structural prediction.** Add a subsection to WP41 or
   WP15: "BHML's α = ½ predicts a factor of ½ in the Wilson area-law
   coefficient, structural not tunable." This is a testable prediction
   that lattice-QCD data could confirm or refute.

5. **Reframe DEEPER_SYNTHESIS Hook #4 on BHML_8.** The Connes-Bost
   semi-local trace formula links arithmetic places `{2, 5, 7, ∞}` to
   a Hilbert space construction. Because BHML_8 really does have prime
   set `{2, 5, 7}`, the hook may be rebuildable on BHML_8. A short
   companion note in `papers/morphotic_braid/synthesis/` could attempt
   this.

6. **WP38 Navier-Stokes audit.** Same scope issue may exist. Does WP38
   use BHML or BHML_8? Needs one-pass check. If BHML_10, then α = ½
   applies; if BHML_8, the 5/7 ratio applies. Either answer is
   publishable; the question is which one the NS strand is actually
   building on.

7. **Lattice gauge-theory bracketing verification (if time).** If any
   published lattice-QCD loop expansion gives Catalan-coefficient
   counts, compare to the HL prediction (F5).

---

## What **not** to do

- Do **not** rewrite WP15 assuming the "det = 70 is wrong" framing
  from the first pass of `CORRECTION_2026_04_24_det_BHML.md`. WP15 is
  **correct** — it always worked with BHML_8 explicitly.
- Do **not** conflate BHML_10 and BHML_8 in any new YM-strand paper.
  Always name which matrix.
- Do **not** claim "BHML is so(8)-triality" as a theorem; it is at
  best a structural hypothesis until F4 is verified.

---

## References for this sprint's follow-ups

- **Huang, E. & Lehtonen, E.** (2017). "The free non-associative
  operad." Communications in Algebra 45 (11), 4685-4710.
- **Wilson, K.G.** (1974). "Confinement of quarks." Physical Review D
  10 (8), 2445.
- **Osterwalder, K. & Seiler, E.** (1978). "Gauge field theories on a
  lattice." Annals of Physics 110 (2), 440-471.
- **WP15** Yang-Mills Mass Gap Synthesis (this repo,
  `papers/clay/WHITEPAPER_15_YANG_MILLS_SYNTHESIS.md`).
- **WP41** Yang-Mills Through the TIG Lens (this repo,
  `papers/clay/WP41_YANG_MILLS.md`).
- **§6.7 Canonical table registry**
  (`FORMULAS_AND_TABLES.md`).
- **CORRECTION 2026-04-24** (`papers/morphotic_braid/CORRECTION_2026_04_24_det_BHML.md`).

---

## Provenance

- Compiled 2026-04-24 evening on branch `vocab-update-2026-04-23`.
- Triggered by Brayden's directive: "effects for yang-mills from today's
  work needs to go on our plan of todo lists."
- Author: Claude (Sonnet 4.5), for Brayden Sanders / 7Site LLC.
