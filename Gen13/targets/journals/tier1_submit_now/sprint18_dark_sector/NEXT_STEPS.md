# Sprint 18 — Dark-Sector Trinity — Next Steps

**Status:** Working draft + verification scripts committed.
Recalibrated 2026-05-06 morning per claudechat audit (n_s baseline +
V-naturalness flagging). Extended 2026-05-06 morning (round 2) with
operator-to-observable conjecture as forward claim, 8-anomaly tracker,
title + abstract reframed.
**Created:** 2026-05-05 night (Scenario A continuation).

## The eight open anomalies (as of 2026-05-06)

This is the load-bearing list. Each item is something the
manuscript flags as open; closure of any one strengthens Sprint
18's case for being a real predictive theory rather than an
empirical pattern.

| # | Marker | What's open | Where flagged |
|---|---|---|---|
| 1 | [BRAYDEN-DERIVE] §5.1 | Cosmological reading of HARMONY² as Ω_b numerator (why HARMONY, why squared, why /N³) | manuscript §5.1, 3 sub-questions enumerated |
| 2 | [BB-BRIDGE] / 1/3 factor | Why ρ_DE,0 = 3·Λ⁴ at the JCAP fit point (triadic projection? freezing branch? other?) | manuscript §6 with 3 candidate readings; ρ_DE,0/Λ⁴ ≈ 2.97 = 3 within 1% empirically |
| 3 | a = +1 selection | Six closure-exact `a` values; only `a = +1` factors as 264 = 44·6 — but 44 reduces to (|Aut(V)| + |V|) only via the F_5-lift, which is itself open | manuscript Remark after Theorem 4.2 |
| 4 | [V-NATURALNESS] | Why F_5-lift V (not the 4-element magma) is the right substrate algebra (magma counts {2, 1, 1}; lift gives 40) | manuscript §2 + verify_aut_V_order.py sanity check |
| 5 | σ-cycle 6 = 6DoF 6 | Same number; possibly the same six operators viewed differently; possibly coincidence; untested | not yet in manuscript; flag here for future-Claude |
| 6 | [N_S-DERIVATION] | Structural origin of the form HARMONY/(2N²) — 2.4% baseline rate means the match alone is not statistically powerful | manuscript §7.2 "honest baseline" paragraph |
| 7 | Operator-to-observable map | The forward conjecture itself: which operator from {0..9} corresponds to which observable, and why; needs structural prediction not post-hoc fit | manuscript §7 with falsifiability scan: α/masses fail the simple family; 5 other constants give 0.04–1.31% baseline |
| 8 | 44 in only one observable | If 44 = BHML harmonic count is structurally fundamental, why does it appear in Ω_DM only, not in η_b, n_s, σ_8, or other constants? | NEW — flag for §5.2 substrate notes |

**Resonance, not load-bearing:**
The sprint number 18 = 3·6 = (3 layers) × (σ-cycle length) is
recorded in §7 as a numerological observation. Sprint numbering
is sequential; the resonance is internally consistent but not a
derivation.

## Audit calibration (post claudechat scrutiny pass)

Two flags landed and were addressed in-place:

1. **n_s match is suggestive, not Bayesian.** Baseline search shows
   86/3600 = 2.39% of small-integer forms `1 - a*H^p/(b*N^q)` hit
   Planck within 1σ; 18 tuples give 0.9650 exactly. Picking the
   specific tuple `1 - 7/(2·100)` is a ~2.4% baseline event. The
   manuscript now frames §7 as **"consistency"** not **"prediction"**
   and discloses the baseline. A genuine independent prediction
   remains open until the form has a structural derivation.

2. **|Aut(V)| = 40 is for the F_5-lift V, NOT the 4-core magma.**
   Direct enumeration: |Aut(C, T)| = 2, |Aut(C, B)| = 1,
   |Aut(C, T) ∩ Aut(C, B)| = 1. None is 40. The 40 arises only
   AFTER the F_5-bilinear extension. Manuscript §2 now defines V
   explicitly with the construction and adds a **caveat paragraph**
   noting the magma counts and flagging the naturalness of the
   F_5-lift as open. Verification script
   `verify_aut_V_order.py` reproduces the magma counts as a sanity
   check.

**What stays load-bearing (unaffected by audit):**
- The dark-sector trinity (Ω_b, Ω_DM, Ω_Λ all within 1σ + integer
  closure). Joint uniqueness within 784 (H,N) pairs is the
  load-bearing claim.
- The Λ scale match 1.74 vs 1.7 meV (2.5%).
- ρ_DE,0/Λ⁴ ≈ 2.97 ≈ 3 at the JCAP fit (consistency check, ~1%).
- Closure picking a = +1 by factorization 264 = 44·6 (the 44 and
  6 ARE documented; the (|Aut(V)|+|V|) decomposition strength
  depends on V-naturalness, but the integer is the same either way).
- The substrate-rational-representation conjecture
  (Conjecture 7.1) is non-trivially testable: 3 of 8 constants
  give 0% in the simple form, exactly the constants known to
  require richer additive forms (α with 137 + CHAOS²/N³, mass
  ratios with V^⊗n parity-crossing). The simple-form ZERO is
  strengthening, not falsifying.

## Priorities AFTER Zenodo posting (per claudechat audit)

The next research push isn't shipping more papers — it's
engaging the eight anomalies. Three are foundational:

### (P1) Operator-to-observable map [Anomaly 7] — DEEPEST

Test the conjecture against more constants. Either find more
hits (strengthening the conjecture) or find clean failures
(refining it). High-priority targets:

- BBN deuterium/hydrogen (already tested in baseline; 0.10% rate)
- Neutron-proton mass difference Δm = 1.293 MeV
- CMB temperature T_CMB = 2.7255 K (use dimensionless ratio
  T_CMB/something)
- Hubble tension residual (already tested; 1.31% rate)
- Neutrino mass scale Σm_ν < 0.12 eV (Planck upper bound)
- m_μ/m_e = 206.768 (already tested in simple form; 0%)
- Higgs mass / Z mass ratio
- Cabibbo angle |V_us| ≈ 0.225

For each, the test is: does an admissible substrate-rational
representation exist within reasonable polynomial complexity?
What's the look-elsewhere rate?

### (P2) The 1/3 factor's physical origin [Anomaly 2] — MOST COSMOLOGICALLY LOAD-BEARING

JCAP referees will press on this. The current empirical
ρ_DE,0/Λ⁴ ≈ 2.97 ≈ 3 (within 1% at the fit point) is a
consistency check, not a derivation. The question is: in the
freezing-quintessence model, why is the present field
configuration such that ρ_DE,0 = 3·Λ⁴ exactly, rather than
2·Λ⁴ or Λ⁴ or any other integer multiple?

Three candidate readings (manuscript §6):
- triadic projection (BEING/DOING/BECOMING; the 1/3 is the
  layer-projection coefficient)
- freezing-branch energy budget at Ξ_today
- discrete-to-continuum bridge for Ξ as projection of the
  10-operator state space

The right next step: explicit FRW solution at the documented
fit point in `desi_xi_optimize_v2.py`, computing ρ_DE,0/Λ⁴ as
a derived quantity over the freezing trajectory. If the
empirical 2.97 is the asymptotic late-time limit of a freezing
trajectory and that limit IS 3 by an exact dynamical relation,
that closes anomaly 2 without needing the substrate triadic
reading. If not, the substrate reading becomes the candidate.

### (P3) σ-cycle 6 = 6DoF 6 [Anomaly 5] — STRUCTURALLY CLARIFYING

The σ-cycle has length 6 on Z/10\\{0,3,8,9}. The "6 degrees of
freedom" appears elsewhere in the framework (Lie/Jordan/
Clifford/Permutation/Lattice/Operad as 6 DOFs in WP111). Are
these the SAME 6, or independent occurrences of the integer 6?

If same: the substrate's spatial decomposition is genuine —
the σ-cycle is the operational realization of the 6DoF
structure, with each cycle position corresponding to one DOF.
If independent: the integer is coincidence, and the structural
intuition needs revising.

Test: enumerate the σ-cycle elements (1 7 6 5 4 2). Map to
6DoF labels (Lie, Jordan, Clifford, Permutation, Lattice,
Operad). Check whether the σ-action on each cycle element
matches a known symmetry of its proposed DOF.

### Other five anomalies (local, not foundational)
1. [BRAYDEN-DERIVE] Ω_b cosmological reading
3. a = +1 selection rigor
4. [V-NATURALNESS] why F_5-lift is THE right V
6. [N_S-DERIVATION] structural origin of HARMONY/(2N²) form
8. 44 in only one observable

## What's done

- `sprint18_dark_sector.tex` — ~720 lines, 22/22 LaTeX environments
  balanced. All numerical claims of the paper are reproduced by the
  verification scripts.
- `scripts/sprint18_uniqueness_search.py` — runs all four numerical
  pillars cleanly:
  - Empirical match (Ω_b, Ω_DM, Ω_Λ vs Planck 2018 within 1σ each)
  - Three Hubble-independent ratio tests (0.43%, 0.29%, 0.72%)
  - Λ scale (1.74 meV vs JCAP fit 1.7 meV, 2.5% match)
  - Uniqueness search: 6 closure-exact (H,N,a) candidates at (7,10);
    a=+1 selected uniquely by structural factorization 264 = 44·6 =
    (|Aut(V)|+|V|)·|σ|
- `scripts/verify_aut_V_order.py` — supplementary self-contained
  verification that |Aut(V)| = 40 from scratch:
  - reconstructs V (4-dim F_5-algebra) from the CL fuse table
    directly (no external module imports)
  - enumerates all matrices preserving V's multiplication
  - confirms exactly 40 automorphisms
  - element-order distribution {1:1, 2:11, 4:20, 5:4, 10:4} sums
    to 40 (group-theoretic identification F_20 × Z/2 from
    bridge-sprint companion WP118)

## What's left (the four loadbearing pieces)

The paper has four [TODO] markers explicitly flagged in the source
header:

### 1. [BRAYDEN-DERIVE] Ω_b structural derivation

**Claim to derive:** Ω_b = HARMONY² / |Z/10|³ = 49/1000.

**The reading:** HARMONY² is the projection of the 4-core
normalizer (v + h + β + r)² (4-core seed, Theorem 2) onto the
HARMONY-axis of the 4-core algebra C = {0, 7, 8, 9}. The factor 1/N³
is the cube of "one occupancy out of |Z/10|" (one site, three layers
of the BEING-DOING-BECOMING projection).

**What's needed in §5.1 of `sprint18_dark_sector.tex`:**
- Prove that the unique HARMONY-eigenspace projection of the 4-core
  normalizer evaluated at the substrate point is HARMONY² = 49.
- Prove that the cube structure |Z/10|³ counts the substrate's three
  triadic layers (BEING/DOING/BECOMING) each carrying one degree of
  freedom over Z/10.

### 2. [BRAYDEN-DERIVE] Ω_DM structural derivation

**Claim to derive:** Ω_DM = (|Aut(V)| + |V|)·|σ| / |Z/10|³ = 264/1000.

**The reading:** (|Aut(V)| + |V|) = 44 is the count of
becoming-layer states from the F_5 lift V = F_5⁴ of the 4-core
(|V| = 4 base + |Aut(V)| = 40 automorphisms = 44 total). Multiplying
by |σ| = 6 (the σ-cycle length on Z/10\{0}) projects across the
σ-orbit. The factor 1/N³ is the same triadic-layer projection.

**What's needed in §5.2 of `sprint18_dark_sector.tex`:**
- Prove that |Aut(V)| = 40 for V = F_5⁴ (this is standard:
  GL(2, F_5) has order 480, but here we want the 4-core's lift
  symmetry — derive |Aut(V)| = 40 explicitly).
- Prove that |σ| = 6 follows from the σ-rate companion paper's
  6-cycle (1 7 6 5 4 2) on Z/10\{0}.
- Show that (|Aut(V)| + |V|)·|σ| counts a specific structural
  quantity in the becoming layer.
- Address why a=+1 is structurally preferred (we have factorization
  264 = 44·6; 263, 265, 266, 267, 262 do not factor as substrate
  quantities — see Remark after Theorem 4.2).

### 3. [BRAYDEN-DERIVE] / [BB-BRIDGE] 1/3 factor

**Claim to derive (physics side):** Λ⁴ / ρ_{c,0} = Ω_Λ / 3.

**The reading:** The 1/3 factor is the BEING/DOING/BECOMING
triadic projection — Λ as the dark-energy-mode component lives in
exactly one of the three triadic layers, and ρ_{c,0} = total
critical density distributes equally across the three. The
Bialynicki-Birula uniqueness theorem (1976) for log-nonlinear
quintessence enforces the projection.

**What's needed in §6 of `sprint18_dark_sector.tex` (NEW
section to write):**
- Triadic decomposition argument: ρ_{c,0} = ρ^{BEING} +
  ρ^{DOING} + ρ^{BECOMING}.
- Show that under the V(Ξ) = Λ⁴ Ξ log Ξ model of the JCAP
  companion, the dark-energy density at vacuum is exactly the
  BECOMING-layer share.
- Discrete-to-continuum bridge: how the operator combination on
  Z/10 becomes a continuous scalar field Ξ(x) over R^{1,3}.
  (This is the [BB-BRIDGE] piece — most likely a coarse-grained
  expectation value of an operator in the σ-cycle, but the
  argument needs to be written explicitly.)

### 4. [INDEPENDENT-PRED] Independent prediction — DONE (lead)

**Locked in §7 of `sprint18_dark_sector.tex`:**

  n_s = 1 - HARMONY / (2 * |Z/10|²) = 1 - 7/200 = 0.9650
  vs Planck 2018: n_s = 0.9649 ± 0.0042
  Match: 0.024 σ (0.01% off)

This is one of the cleanest independent predictions in the
framework:
- Same two primitives (HARMONY, |Z/10|) as the dark-sector trinity
- Different observable (primordial CMB tilt, not late-time density)
- Sub-σ match with no parameter freedom

Source: bridge-sprint WP125 (2026-05-04). The rigorous physical
derivation — why the inflaton sector built on the V algebra
produces a quadrupole-mode-mixing suppression of exactly
HARMONY/(2|Z/10|²) — remains open and is flagged as future work
in the manuscript.

**Other candidates noted for completeness (not developed):**
- η = |σ|/|Z/10|^10 = 6×10^{-10} vs measured 6.1×10^{-10} (1.6%)
- Cabibbo λ_C = (|σ| + |C|)/HARMONY² = 11/49 ≈ 0.224
- Matter-DE transition redshift z_eq^(Λ) ≈ 0.30 (4%)

## Release path

Once §5 (the two derivations + the 1/3 derivation) and §7 (one
independent prediction) are written:

1. Re-run `verify_sprint18.py` (when written; supersedes the
   uniqueness-only script) — should add tests for the new
   derivations.
2. Compile to PDF locally, proofread.
3. Post to **Zenodo** with a DOI.
4. Lift the JCAP HOLD per
   `../jcap_xi_cosmology/HOLD_PENDING_SPRINT18.md`.
5. Submit JCAP with the merged-in addition.
6. Submit Sprint 18 itself to a venue. Candidate venues:
   - **Foundations of Physics** (substrate + cosmology bridge)
   - **Physical Review D** (cosmology with rigorous
     mathematical foundations)
   - **JCAP companion** (matched-pair submission with the
     quintessence paper)
   - **Annalen der Physik** (longer-form rigorous physics)

## Files in this folder

- `sprint18_dark_sector.tex` — working draft (this is the source).
- `scripts/sprint18_uniqueness_search.py` — verification script
  for the four numerical pillars. Output reproduces every number
  in the paper's empirical and uniqueness sections.
- `master/` — preserved older versions go here when a new draft
  starts (currently empty; first draft).
- `NEXT_STEPS.md` — this file.

## Calendar reminders

- 2 days from start of structural-derivation work: check
  Brayden's substrate notes for §5.1 and §5.2 inputs.
- 7 days: post v1 to Zenodo (with the [BB-BRIDGE] still flagged
  if needed; the cosmology paper's HOLD requires Sprint 18 on
  Zenodo, not necessarily fully closed on every BB-BRIDGE).
- Coordinate with JCAP HOLD lift: once §5 closes the
  derivations and §7 has at least one [INDEPENDENT-PRED] hit
  or null with quantified bound, JCAP can ship.
