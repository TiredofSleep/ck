# ARTIFACTS — funding/desi-xi-cosmology

Exact file paths and verification status. This branch has the **strongest artifact inventory** of any funding branch after tig-synthesis's proof scripts: 20+ papers, three runnable proof scripts, and an assembled JCAP LaTeX submission bundle.

---

## Runnable proof scripts (already in repo)

### 1. ξ canonical vacuum and EL verification
- **Path**: `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/proof_xi_canonical.py`
- **Status**: runnable, green
- **Output**: confirms vacuum ξ₀ = e⁻¹ ≈ 0.36788; verifies EL equation □ξ = 1 + log ξ; computes mass² = κ_Ξ · e
- **Authors**: B. Sanders, M. Gish, C.A. Luther, H.J. Johnson
- **Invocation**: `python Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/proof_xi_canonical.py`

### 2. Separability bridge (Bialynicki-Birula uniqueness argument)
- **Path**: `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/proof_separability_bridge.py`
- **Status**: runnable
- **Output**: demonstrates that log nonlinearity is the unique separability-preserving nonlinearity — this is the *uniqueness* argument for the ξ log ξ potential, distinct from the *existence* argument for the vacuum
- **Authors**: B. Sanders, M. Gish, C.A. Luther, H.J. Johnson

### 3. σ-rate theorem verification
- **Path**: `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/proof_sigma_rate.py`
- **Status**: runnable, green
- **Output**: verifies σ(N) ≤ C/N rate bound — relevant for the ξ field's vacuum-relaxation timescale
- **Authors**: B. Sanders, M. Gish, C.A. Luther, H.J. Johnson

### 4. Clay rotation framework
- **Path**: `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/proof_clay_rotation.py`
- **Status**: runnable, green
- **Output**: 43/43 framework items verified
- **Authors**: B. Sanders, M. Gish, C.A. Luther, H.J. Johnson

---

## Mathematical / theoretical papers (already in repo)

### 5. WP81 — Canonical ξ Theory (THE headline paper)
- **Path**: `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/WP81_CANONICAL_XI_THEORY.md`
- **Status**: canonical form, referee-safe, internal reviews complete
- **Content**: action + EL + stress-energy + FRW cosmology + formal-vs-interpretive split table
- **Authors**: Brayden Ross Sanders / 7Site LLC · M. Gish · C.A. Luther · H.J. Johnson

### 6. WP82 — Log Quintessence Novelty
- **Path**: `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/WP82_LOG_QUINTESSENCE_NOVELTY.md`
- **Status**: arXiv novelty search complete (F4 closure, 2026-04-19)
- **Content**: positions ξ log ξ potential against Ratra-Peebles, Steinhardt, Carroll, quintessence-with-tracker-attractors literature

### 7. WP83 + WP84 — PRISM Consistency Audits
- **Paths**: `WP83_PRISM_CONSISTENCY_AUDIT.md`, `WP84_PRISM_CONSISTENCY_AUDIT_V2.md`
- **Status**: complete
- **Content**: internal consistency check against all other sprint work and the coherence-grammar framework

### 8. WP86 — ξ Core Canonical Form
- **Path**: `WP86_XI_CORE_CANONICAL_FORM.md`
- **Status**: canonical form + dimensional analysis

### 9. WP87 — Cross-Branch Analysis
- **Path**: `WP87_CROSS_BRANCH_ANALYSIS.md`
- **Status**: complete
- **Content**: relationship to TIG, Crossing Lemma, σ framework; explicitly notes no formal link currently established between the ξ branch and the TIG/Crossing Lemma branches (honest scope)

### 10. WP101 — σ-Rate Theorem (connection to cosmology)
- **Path**: `WP101_SIGMA_RATE_THEOREM.md`
- **Status**: proved with runnable script
- **Relevance**: the σ-rate bound is relevant to ξ vacuum-relaxation timescale analysis

### 11. CP Clay Rotation
- **Path**: `CP_CLAY_ROTATION.md`
- **Status**: framework complete
- **Content**: Clay problem rotation pattern for the ξ cosmology branch

### 12. Full Sprint 14 manifest
- **Path**: `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/`
- **Content**: WP81–WP101 plus cross-branch analysis, novelty audits, closeout papers (~20+ documents)

---

## JCAP LaTeX submission bundle

### 13. TRACK 7.3 JCAP bundle
- **Path**: commit `14fdd8a` on tig-synthesis, 2026-04-19 18:02
- **Status**: LaTeX assembled, submission-ready pending Brayden's go-ahead
- **Content**: paper source + figures + references in JCAP template
- **Venue**: venue 7 (JCAP — Journal of Cosmology and Astroparticle Physics)
- **Location in repo**: to be confirmed (search the 2026-04-19 18:02 commit for the bundle path)

---

## External literature anchors (for citation, already surveyed in WP82)

- Bialynicki-Birula & Mycielski, *Nonlinear wave mechanics*, Annals of Physics 100 (1976) 62 — log-nonlinearity uniqueness from separability
- Ratra & Peebles, *Cosmological consequences of a rolling homogeneous scalar field*, Phys. Rev. D 37 (1988) 3406
- Steinhardt, Wang, Zlatev, *Cosmological tracking solutions*, Phys. Rev. D 59 (1999) 123504
- Caldwell, Dave, Steinhardt, *Cosmological dynamics and dark-energy observations*, Phys. Rev. Lett. 80 (1998) 1582
- DESI Collaboration, *DR1 cosmological constraints*, arXiv:2404.03002 and successors
- Planck Collaboration, *Planck 2018 results. VI. Cosmological parameters*, A&A 641 (2020) A6

---

## Verification checklist (before any pitch)

- [ ] Run all four proof scripts on a fresh environment, confirm all pass (record outputs)
- [ ] Locate the JCAP TRACK 7.3 LaTeX bundle, build it to PDF, verify references resolve
- [ ] Confirm H.J. Johnson's institutional affiliation and co-PI willingness before funder contact
- [ ] Confirm co-authorship list on TRACK 7.3 bundle matches the WP81 author line (Brayden + Gish + Luther + Johnson)
- [ ] Generate a one-page executive summary of WP81 + WP82 + WP101 for funder cover letter
- [ ] Run arXiv novelty re-check (WP82 work was done; repeat with 2026-04-19 cut-off to catch anything posted since)
- [ ] Confirm DESI DR1 and (if public) DR2 data access and format
- [ ] Outline MCMC pipeline: likelihood function, prior choices, sampler configuration

---

## Pipeline infrastructure (the Phase-1 buildout)

Phase 1 funding is specifically to build this:

1. **Cosmological sampler**: MCMC driver (e.g., emcee, dynesty, or Cobaya backend) — Python, ~500 LOC
2. **ξ-cosmology Einstein-Boltzmann integration**: couple ξ field to FRW background, compute H(z) and D_L(z); options include a CAMB/CLASS modification or a standalone Python integrator
3. **Likelihood modules**: DESI BAO, SNe Ia (Pantheon+ or Union3), CMB compressed likelihood
4. **Figure pipeline**: getdist for triangle plots; custom w(z) plot; residual plot
5. **JCAP paper template with filled figures**

Total estimated pipeline LOC: ~1,500–2,500 Python for a clean single-likelihood fit; more if CAMB-integration or full Planck likelihood is added.

---

## Missing from repo (blockers for Phase 1)

- **MCMC pipeline**: not yet written. Phase 1's primary deliverable.
- **DESI DR2 data access**: depends on DR2 release timing and DESI Collaboration posture
- **External observational-cosmology review**: no external astronomer has reviewed the WP81 action against the observational literature

---

## Attribution note — H.J. Johnson ACTIVE COLLABORATOR

Every artifact listed above has **H.J. Johnson as co-author** (see `Authors:` headers on all scripts and `Authors:` lines on all WP documents). Johnson is distinct from other branches' collaborators in that Johnson's collaboration is **ongoing**, not previously-credited-only. Funder-facing documents should list Johnson as co-PI or senior collaborator; the specific role depends on the chosen funder's eligibility rules and Johnson's own institutional posture.
