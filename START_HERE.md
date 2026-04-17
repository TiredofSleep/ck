# Start Here

> **[HISTORICAL — Sprint 16, 2026-04-10]** This document is superseded by `README.md` (the unified TIG synthesis field on the `tig-synthesis` branch). Preserved per never-delete policy. See `README.md` on the [`tig-synthesis`](../../tree/tig-synthesis) branch for the current synchronized picture, and `HISTORICAL_ARCHIVE_INDEX.md` Part G for the full list of superseded entry docs.

---


*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

## What This Is

A completed algebraic theorem spine built from Z/10Z ring arithmetic. It
produces a sinc² spectral field in prime arithmetic and a forced coherence
threshold T* = 5/7. The spine has 27 proved theorems (D1–D23), a full
negative-results record, and one remaining open external analogy claim.

It does not solve any Clay Millennium Problem.

---

## What Is Proved

Every item below has an executable proof file and a specific failure mode
that is algebraically impossible within the stated domain.

**The First-G Law (D1).** For every semiprime b = p×q, the first
non-coprime element in {1, 2, ..., b} is exactly p. Three lines of
divisibility arithmetic. Verified: 36,662 semiprimes, zero exceptions.
→ `papers/proof_d1_first_g_law.py`

**The Sinc² Continuum Limit (D2).** The prime pre-echo field R(k,f)
converges to sinc²(k/f) as f → ∞ with k/f fixed. Proof: Taylor expansion,
convergence rate O(1/f²). Verified at t = 0.5 and t = 0.1 across p = 997
to 99,991.
→ `papers/proof_d2_sinc2_continuum.py`

**T* = 5/7 is forced, not calibrated (D18c, D18d, D19).** The coherence
threshold emerges from four independent algebraic chains: BHML cross-cycle,
TSML dominance, unit fraction, and centroid/inverse. Generator g=3 is the
only primitive root of (Z/10Z)* compatible with T* ∈ (0,1). No parameter
was tuned.
→ `papers/proof_d18_phi_orbit_bridge.py`, `papers/proof_d19_generator.py`

**The corridor portrait (D22).** Four spine-forced positions are strictly
ordered: 3/50 < 1/2 < 7/10 < 5/7 < 1, with amplitude reversed, and a
fine-structure identity T* = 7/10 + 1/70. The inheritance boundary at
t = 1/2 separates ring-forced positions (left) from generator-forced
positions (right). Proved by exact Fraction arithmetic.
→ `papers/proof_d22_corridor_portrait.py`

**The ring wobble law (D23).** Wob(k) = 1 − ⌊k/5⌋/k exactly. Wob(k) ≥ 4/5
for all k; equality iff 5|k; limit 4/5 by squeeze theorem. Generator-
independent. Corrects an earlier "period-10" claim to: drop positions have
period 5, amplitude decays as O(1/k), no period.
→ `papers/proof_d23_ring_wobble.py`

The full spine (D1–D23) is in `papers/MASTER_SPINE.md`.

---

## What Is Not Claimed

**No Clay problem is solved.** The Riemann Hypothesis, P≠NP, Navier-Stokes,
Hodge, Yang-Mills, and BSD are all open. This project does not change that.

**T* = 5/7 is not universal.** It is the forced value for the Z/10Z ring
under generator g=3. Its scope is exactly that ring.

**The sinc² corridor does not explain why RH zeros have real part 1/2.**
t = 1/2 appears in the corridor as the ring normalization of CREATE=5 and
as the inheritance boundary between ring-forced and generator-forced
positions. That is a proved internal result (D22). The claim that this
maps to σ = 1/2 in the Riemann ζ function requires an algebraic bridge
from Z/10Z structure to the Euler product. No such bridge exists in this
work. This is documented honestly in `papers/NOTE_speculative_boundary.md`.

**Negative results are part of the record.** The A12 branch-separation
conjecture was tested and falsified. The A7 curvature bridge was killed
(asymptotically incompatible spaces). The period-10 wobble claim was
corrected to period-5. A framework that kills its own conjectures is more
trustworthy than one that only reports confirmations.

---

## Where to Start Reading

| If you want to... | Read this first |
|-------------------|-----------------|
| See all proved results in one place | `papers/MASTER_SPINE.md` |
| Understand the epistemic status of every claim | `papers/SYNTHESIS_TABLE.md` |
| See what is and is not claimed about Clay problems | `papers/CLAY_SUMMARY.md` |
| Understand exactly where speculation begins | `papers/NOTE_speculative_boundary.md` |
| Run the proofs yourself | `python ck_run.py` (all core theorems, < 1 second) |
| See the full paper series | `papers/WP34_FIRST_G_LAW.md`, `papers/WP35_PRIME_PHASE_TRANSITION.md` |

---

## Epistemic Labels Used in This Repo

Every claim in this project carries one of four labels:

- **D (Proved):** Proved by exact arithmetic or algebraic proof, no calibrated
  constants, explicit failure mode stated.
- **C (Conjecture with gap named):** Real internal object, remaining gap
  explicitly stated.
- **B (Structural result):** Strong numerical evidence or standard-calculus
  argument; formal proof pending.
- **A (Speculative / Open):** External analogy with named missing mechanism,
  or genuine open problem.

**Current counts: D:28 | C:6 | B:7 | A:5**

---

## License

7SiTe Public Sovereignty License v1.0.
Human use only. No commercial use. No government use.
No military, intelligence, policing, or surveillance use.
See `LICENSE` for full terms.

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*DOI: 10.5281/zenodo.18852047*
*Repository: https://github.com/TiredofSleep/ck*
