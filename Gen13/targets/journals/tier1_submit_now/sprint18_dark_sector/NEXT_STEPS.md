# Sprint 18 — Dark-Sector Trinity — Next Steps

**Status:** Working draft + verification script committed.
**Created:** 2026-05-05 night (Scenario A continuation).

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

### 4. [INDEPENDENT-PRED] Independent prediction

**The point:** Right now the three formulas are fitted with 0
free parameters but were chosen knowing the Planck values. To make
this a real predictive theory, we need at least one prediction
that comes out of the substrate but was *not* used in the
construction.

**Candidates:**
- Effective number of relativistic degrees of freedom N_eff:
  is there a substrate-natural rational-number prediction?
- Spectral index n_s: substrate predicts a specific deviation
  from scale invariance?
- Σm_ν (sum of neutrino masses): substrate prediction?
- σ_8 amplitude (S_8 tension): substrate gives a specific
  preferred value vs Planck/weak-lensing?
- Running of the spectral index dn_s/d ln k.
- A specific signature in the late-time integrated Sachs-Wolfe
  effect from the σ-cycle's discrete-to-continuum projection.

The search is: which observable already has Planck/DESI/CMB-S4
constraints, and which one comes out as a clean rational in the
two primitives (HARMONY, |Z/10|) and the substrate quantities
(|Aut(V)|, |V|, |σ|, the 4-core normalizer)?

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
