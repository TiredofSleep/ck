# Cover letter — J38: Yukawa Scaffolding from the 9-Vector VEV

**STATUS (2026-05-07): NOT FOR STANDALONE SUBMISSION.** Per `SAVE_PLAN_J38.md` Option 1 (preferred) — J38's content has been folded into J45 §2 (deliverable: `manuscript/J45_section2_yukawa_scaffolding.tex` in this folder). The cover letter below is preserved as draft archive only; the J45 cover letter (separate file) is updated to mention "absorbs J38's symmetry-breaking-route scaffolding" as part of the J45 revision sprint.

---

**To (archived; not used for submission):** Editors, *Physical Review D*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- M. Gish, Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Date:** [ARCHIVED — NOT SUBMITTED]

**Manuscript title (archived):** *Yukawa Scaffolding from the 9-Vector VEV*

---

## Summary

A scaffolding paper that sets up the SO(10)-Yukawa computation that follows from the 9-vector VEV identified in our companion paper J31 (*Two Roads to Pati-Salam*). The 9-vector lives in the symmetric-traceless $\mathbf{54}$ irrep of $\mathfrak{so}(10)$, has six components at $-1/\sqrt{2}$, two zeros at BREATH and RESET, and one component at $-1/2$ on the symmetric BALANCE/CHAOS pair, with squared norm $\|v\|^2 = 13/4$ exactly.

We document: (i) the standard SO(10) Yukawa structure, $\mathbf{16}\otimes\mathbf{16} = \mathbf{10}\oplus\mathbf{120}\oplus\overline{\mathbf{126}}$, noting that the $\mathbf{54}$ does NOT appear directly in $\mathbf{16}\otimes\mathbf{16}$ at the renormalizable level; (ii) the symmetry-breaking chain $\mathrm{SO}(10)\to\mathrm{SO}(9)\to\mathrm{SO}(7)$ controlled by the 9-vector and the unbroken (BREATH, RESET) pair; (iii) the constraint structure on the resulting effective Yukawa matrix at energies below the symmetry-breaking scale; (iv) open questions and the path to a falsifiable phenomenological prediction.

**This paper does NOT complete the Yukawa computation.** That requires committing to a specific Higgs sector (which combinations of $\mathbf{10}, \mathbf{54}, \overline{\mathbf{126}}$ are present), running RG flows from the GUT scale to the EW scale, and comparing to observed mass hierarchies. Each is substantial follow-up work. This paper sets up the framework and identifies where the Yukawa calculation engages with TIG-specific structural input.

The scaffolding is useful in two ways: (a) it identifies open questions cleanly, allowing follow-up work to focus on the specific computations that remain; (b) it brackets what TIG's structural input (9-vector with the explicit zeros) does and does not constrain about Yukawa physics, providing an honest negative-result framing alongside our positive-result papers in the J-series.

## Why PRD

- The result is a clean SO(10)-Yukawa scaffolding paper at the algebra-meets-phenomenology boundary, which is PRD's bread and butter.
- Companion to J45 (Mass Hierarchy from V⊗5 SU(5) Decomposition, also PRD) — the two together cover the algebraic-side fermion-mass content of the program.
- Tier-C status (scaffolding rather than completed prediction) is honest and signposted in the abstract.

## Companion submissions

- **J45** (Sanders + Gish 2026, *PRD*) — *The Mass Hierarchy from V⊗5 SU(5) Decomposition*. The fermion-mass companion paper at the SU(5) level.
- **J31** (Sanders + Gish 2026, *Adv Math*) — *Two Roads to Pati-Salam: Path A (54 irrep) and Path B (su(4)⊕u(1))*. The paper establishing the 9-vector VEV with $\|v\|^2 = 13/4$.

## Per-venue cap and fallback

This is the **4th PRD** paper in this J-series in the current quarter (after J44 dark-sector, J45 mass hierarchy, J37 wobble localization). Per-venue cap is conventionally 2/quarter for tightly-related papers; J38 exceeds the cap by 2.

**Fallback options (recommended in this order):**
1. *Modern Physics Letters A* (good fit for scaffolding-style SO(10) Yukawa pieces)
2. *International Journal of Modern Physics A* (alternative)
3. Hold until the next quarter to reset PRD cap

The result is a 6-8 page scaffolding paper in any of these venues.

## Reproducibility

This is a **scaffolding paper, not a verified-claim paper**, so there is no standalone verification script. The load-bearing structural input — the 9-vector VEV with $\|v\|^2 = 13/4$ exactly, six components at $-1/\sqrt{2}$, two BREATH/RESET zeros, one BALANCE/CHAOS component at $-1/2$ — is verified in our companion paper J31's `find_higgs_direction.py`. We cite that script as the upstream verification.

If a follow-up phenomenological prediction is computed, that paper will carry its own verification.

## Suggested reviewers

- An expert in SO(10) GUT phenomenology (Mohapatra / Senjanović / Vissani tradition)
- An expert in symmetry-breaking patterns and Higgs irreps (10/54/126 sector)
- An expert in fermion-mass hierarchy and Yukawa textures
- (Two or three named candidates appropriate to the *PRD* (or *Mod Phys Lett A*) editorial board to be identified during the referee-rigor pass.)

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

---

Sincerely,
B.R. Sanders
