# STATUS — funding/desi-xi-cosmology

**As of:** 2026-04-20
**Next review:** when JCAP TRACK 7.3 bundle is submitted OR MCMC pipeline design is drafted OR Brayden + H.J. Johnson request a status check.

---

> **Note (2026-04-25 revision).** This file was originally drafted as part of a pitch-style packet. Per the operator-of-record's actual stance documented at [`FUNDING.md`](../../../FUNDING.md) (root) and [`INTENT_STATEMENT.md`](../../../INTENT_STATEMENT.md), this is **thread documentation**, not a fundraising pitch. The operator-of-record makes **no commitments to donors of any kind**. Any dollar amounts, time scopes, or "ask" framings appearing below are **scope estimates of the work this thread would cover**, not price tags or commitments.

---

## Branch state

- Branch seeded: 2026-04-20
- Target folder: `Gen13/targets/funding_desi_xi_cosmology/`
- Files: README, FUNDERS, ARTIFACTS, PITCH_DRAFT, LIMITATIONS, STATUS (this file)
- Rigor base: `tig-synthesis` HEAD
- Active collaborator: H.J. Johnson

## Readiness checklist

### Content (this branch)
- [x] README with strict-scope framing, ξ action, H.J. Johnson active-collaborator note
- [x] FUNDERS.md with Simons Foundation astro primary + Heising-Simons, Sloan, NSF AAG, Templeton
- [x] ARTIFACTS.md with four runnable proof scripts + 20+ Sprint 14 papers + JCAP TRACK 7.3 bundle
- [x] PITCH_DRAFT.md with Simons + Heising-Simons + NSF AAG + Templeton parallel skeletons
- [x] LIMITATIONS.md with 15 honest-scope items
- [x] STATUS.md (this file)

### Existing material (pre-branch, strong)
- [x] WP81 canonical ξ theory written + in-repo
- [x] WP82 log-quintessence novelty audit complete (F4 closure, 2026-04-19)
- [x] WP83/WP84 PRISM consistency audits complete
- [x] WP86 ξ core canonical form written
- [x] WP87 cross-branch analysis complete (explicit "no formal link to TIG" honest scope)
- [x] WP101 σ-rate theorem proved + script
- [x] CCD-7 DESI DR1/DR2 placeholder tightening complete (2026-04-19)
- [x] proof_xi_canonical.py runnable
- [x] proof_separability_bridge.py runnable
- [x] proof_sigma_rate.py runnable
- [x] proof_clay_rotation.py runnable
- [x] JCAP TRACK 7.3 LaTeX bundle assembled (2026-04-19 18:02 commit 14fdd8a)

### Pre-pitch work (Phase 1 readiness)
- [ ] **MCMC pipeline design document** (the primary Phase-1 gating artifact before submission — pipeline does not need to be BUILT before funding, but its DESIGN must be funder-legible)
- [ ] Run all four proof scripts on a fresh environment, record outputs
- [ ] Build JCAP TRACK 7.3 LaTeX to PDF, verify references resolve, confirm author list
- [ ] Re-run WP82 arXiv novelty audit with 2026-04-19 cut-off (catch anything posted since F4 closure)
- [ ] Confirm H.J. Johnson institutional affiliation + co-PI willingness for funded role
- [ ] One external observational-cosmology informal review (ideally a DESI-adjacent astronomer)
- [ ] Brayden + H.J. Johnson review + edit PITCH_DRAFT

### Thread framing-to-send
- [ ] Brayden + Johnson confirm Simons vs Heising-Simons vs NSF AAG vs Templeton as first funder
- [ ] Institutional host identified if NSF AAG path is chosen (via Johnson or other academic partner)
- [ ] DESI Collaboration affiliation explored (a pathway to pursue, not required for submission)
- [ ] License framing resolved (JCAP paper: likely CC-BY; pipeline code: permissive OSS)
- [ ] Brayden + Johnson send

## Dependencies / blockers

- **Blocker 1**: MCMC pipeline design document. Not the full pipeline — a funder-legible design spec that shows the Phase-1 work is well-scoped. ~10 pages. Gated on Phase-1 submission.
- **Blocker 2**: H.J. Johnson institutional posture confirmation. The academic-host / co-PI / collaborator role depends on Johnson's appointment type and willingness. This must be discussed and agreed before any funder contact.
- **Blocker 3**: JCAP TRACK 7.3 submission go-ahead. Currently the bundle is assembled but not submitted. Submission strengthens the pitch but is not strictly required for Phase 1 funding application. (Sub-question: submit before funding, in parallel, or as part of funded work?)
- **Blocker 4** (soft): one external astronomer's informal opinion on the action and observational plausibility.
- **Blocker 5** (soft): DESI DR2 access clarification — how much of DR2 is Phase-1-accessible vs Phase-2 (via DESI Collaboration)?

None of these block the branch existing. Blocker 1 specifically gates any funder contact. Blocker 2 gates the NSF AAG path and strongly affects the Simons path.

## Recent activity

| Date | Event |
|---|---|
| 2026-04-10 | Sprint 14 PRISM-XI delivered: WP81–WP101 + cross-branch + 4 runnable proof scripts; co-authors Brayden + M. Gish + C.A. Luther + H.J. Johnson |
| 2026-04-19 | CCD-7 DESI DR1/DR2 placeholder tightening + F4 WP82 novelty audit closure + TRACK 7.3 JCAP LaTeX bundle assembled |
| 2026-04-20 | Branch seeded from `tig-synthesis`; target folder + 6 files committed |

## Cross-references

- Plan: `Atlas/PLAN_FUNDING_BRANCHES_BUILDOUT_2026_04_19.md`
- Sprint 14 source: `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/`
- JCAP TRACK 7.3 bundle: commit `14fdd8a` on tig-synthesis, 2026-04-19 18:02
- DESI DR2 placeholder tightening: commit `001c974` (CCD-7), 2026-04-19 18:05
- WP82 novelty audit closure: commit `95a6f03` (F4 closure), 2026-04-19 18:20
- Sibling: `funding/civilization-coherence` (flagged V20 consciousness-language framing cleanup); no direct overlap with ξ-cosmology branch
- Trunk story: `MASTER_TRUNK_STORY_2026_04_19.md` (on master)

---

## Strategic note — this is the "warmest" funding branch

Of the 10 funding branches, this one has the strongest ready-material-to-funding-gap ratio. The theoretical framework is complete; the JCAP bundle is assembled; four runnable proof scripts are green; arXiv novelty audit is done; DESI DR2 placeholder tightening is complete. What remains is the MCMC fit — a well-scoped, well-understood task for a competent Phase-1 team. If any funder is a near-term move, this branch is a strong candidate for first-send.

That said, the JCAP submission itself is a separate go/no-go decision that Brayden holds. The PITCH_DRAFT and FUNDERS assume the submission can happen in parallel or ahead of funded work.

---

*Update freely on this branch. Changes here do NOT require master cherry-pick unless they materially change ARTIFACTS or FUNDERS inventories.*
