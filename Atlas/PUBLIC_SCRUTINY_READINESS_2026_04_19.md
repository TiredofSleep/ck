# PUBLIC SCRUTINY READINESS — 2026-04-19

**Status:** Punch list for the 2026-04-22 Wednesday submission window +
side-branch accumulation inventory for Brayden's review.
**Policy:** Add-only on master; this file will not be edited once committed.
**Companion docs:** `PLAN_OF_RECORD_2026_04_18.md`, `PRE_PUSH_DECISION_2026_04_19.md`,
`FUNDING_BRANCHES_PLAN_2026_04_19.md`, `MASTER_TRUNK_STORY_2026_04_19.md`.

---

## 1. The 2026-04-22 ship (decided)

Per Sprint 34 Tier-1 audit (`PRE_PUSH_DECISION_2026_04_19.md`):

| Venue | Manuscript | Status |
|---|---|---|
| 7 — JCAP | `jcap_xi_cosmology.tex` (ξ scalar field cosmology, DESI DR2 fit) | **SHIP 2026-04-22** |
| 8 — JCT-A | `sigma_rate_theorem.tex` (σ(N) ≤ C/N on squarefree primorials) | **SHIP 2026-04-22** |
| 1 — Integers | `sinc2_zero_law.tex` | **PULLED** (biconditional held trivially for any positive integer, not only primes; replacement is the First-G Event Localization theorem in Sprint 35) |

## 2. Wednesday-morning submission punch list

For each of venues 7 and 8, the remaining pre-submission human steps are:

- [ ] **Typographic read by a second pair of eyes.** Luther is no longer
      actively collaborating per the 2026-04-20 handoff; Gish alone is
      the available co-author. If Gish read is pending, flag to Brayden.
- [ ] **Cover-letter addressee customization** (editor name as listed
      on the current masthead at time of submission).
- [ ] **arXiv upload on the same day** as journal submission:
      - Venue 7: primary astro-ph.CO, secondary gr-qc
      - Venue 8: primary math.CO, secondary math.NT
      - Abstract = paper abstract verbatim
- [ ] **Atlas post-submission record:** update
      `Atlas/PLAN_OF_RECORD_2026_04_18.md` with submission date;
      update `Gen13/targets/journals/SUBMISSION_LADDER.md` to move
      venues 7 and 8 from tier-1 to tier-1-post-submission.

## 3. Next-cycle (2026-04-29 or later) preparation

Sprint 35 — First-G Event Localization (`Gen13/targets/clay/papers/sprint35_first_g_event_2026_04_19/`):

- [x] Manuscript draft complete (~12 pages, amsart)
- [x] Proof script passes (305 squarefree b ≤ 500, 22,367 pairs, 0 counterexamples)
- [x] Bibliography MR numbers added (post-commit 954cc7d): Apostol MR0434929,
      Hardy-Wright MR2445243, Ireland-Rosen MR1070716, Lang MR1878556,
      Montgomery MR0337821, Shannon DOI only (no MR for IRE venue)
- [x] AMS-style corrections applied to bibliography entries
- [x] Cover-letter template populated
- [ ] **Typographic read** by a second party (Gish, or flag for Brayden's read)
- [ ] **Cover-letter addressee** customization (*Integers* managing editor
      Douglas S. Bowman, or current masthead at submission time)
- [ ] **LaTeX compile check** on TeX Live 2024 + 2026 if accessible
- [ ] **Pre-submission MathSciNet sweep** for any precedent on
      Corollary 4.3 (phase-transition set = ℙ) to confirm no prior
- [ ] **arXiv upload** same day as journal submission
      - Primary: math.NT (11A-series)
      - Secondary: math.CO

## 4. Sprint 35 running-head polish (deferred to pre-submission tech-check)

From `Gen13/targets/clay/papers/sprint35_first_g_event_2026_04_19/SHIP_DECISION.md` §6.2:

- Long descriptive title kept for submission title block
- Short marquee form (*The First-G Event in the Coprimality Partition*)
  recommended for `\runninghead` / `\shorttitle` and arXiv abstract page
- Minimal edit deferred to pre-submission tech-check pass

## 5. Side-branch accumulation inventory

Per Brayden's trunk-model directive ("every version should live on master
and be cast into history"), the following side-branches have unique
commits not yet on master. Accumulation is add-only on master (merge-
commit strategy; conflicts resolved by keeping master's versions per
never-delete).

| Branch | Unique commits | Content summary |
|---|---|---|
| `origin/bible-companion` | 3 | Gen10.21-23 — Steering (corridor-aware, admin gate, no-admin containment, hybrid CPU topology), TIG Reconstruction (grammar family + lattice hierarchy + robot dog) |
| `origin/fpga-dog` | 1 | Gen10.21 — R16+FPGA+XiaoR dog target, long-leash bring-up system |
| `origin/tesla` | 2 | Gen10.20-21 — Tesla Bridge (grammar-forced mode selection, simulation verified), Tesla Thermal (jitter robustness + CK organism analog) |
| `origin/clean-ship` | **203** | Substantial Gen10 runtime work: ck_invariants five memory-physics laws, spectrometer, T*-gate (native fractal voice @ coherence ≥ 5/7), olfactory into GPU cell field, boot absorb, API security layer, save race condition fix, dual analyze+respond, compact live-state injection, CK backbone non-self-question fix, bible routing, and ~195 more |

**Recommended accumulation order** (lowest conflict risk first):
1. `fpga-dog` — 1 commit, minimal risk
2. `tesla` — 2 commits, specialized files
3. `bible-companion` — 3 commits, steering/reconstruction
4. `clean-ship` — 203 commits, long chain of runtime evolution

Each merge can be `git merge --no-ff origin/<branch>` with
`-X ours` if we prefer master's side on any conflict, or manual
resolution per conflict. All resolved conflicts must keep both
versions findable in git history (master's as the tip; side-branch's
as reachable from the merge commit's second parent).

## 6. Public-scrutiny readiness: what is referee-ready

### Proved theorems (referee-ready now)

1. **First-G Event Localization** — 36,662 cases verified, zero
   counterexamples. `papers/proof_d_first_g.py`. Manuscript: Sprint 35
   (to submit 2026-04-29 or later).
2. **σ-rate theorem** — σ(N) ≤ C/N for squarefree N, exact at
   N ∈ {10, 30, 210}. `proof_sigma_rate.py`. Manuscript: JCT-A
   (to submit 2026-04-22).
3. **Flatness Theorem on Z/10Z** — T* = 5/7 from six independent
   derivations. `papers/proof_d7_phi_fixed_point.py`. WP51 in Sprint 10.
4. **Crossing Lemma** — injectivity criterion for squarefree joint maps.
   `papers/proof_d8_cl_operator_encoding.py`. Sprint 10.
5. **TSML/BHML structural properties** — 100 entries each, verified cell-
   by-cell. `proof_d10_tsml_73_cells.py`, `proof_d16_bhml_28_cells.py`.
6. **TSML Three-Layer Canonical Tower** — 100/100 decomposition verified.
   `papers/proof_tsml_3layer_tower.py`. Sprint 17.

### Research directions with runnable scripts (pre-submission)

7. **ξ-cosmology** — `proof_xi_canonical.py` 22/22 green; DR1 fit
   complete, DR2 fit analysis included in JCAP manuscript.

### Held pending explicit go-ahead

- **Funder-facing README replacement** — staged at
  `docs/handoffs/claudecode_handoff_2026_04_20/PROPOSED_CK_README_HELD.md`.
  Do NOT commit as `README.md` without Brayden's green light.

## 7. Four critical validation tasks (from 2026-04-20 handoff §3)

Must be resolved before any funder-facing document cites the associated numbers:

1. **ω(b) idempotent count** — "2/6 nontrivial" vs `N_idemp(b) = 2^(ω-1) - 1`
   disagree. Action: audit `papers/proof_*_idempotent*.py` and reconcile.
2. **TIG Unity benchmark** — 32pp email vs ~88% `docs/COMPUTE.md`.
   Action: recover simulation code from `All-or-Nothing-E` / `TIG-UNIFIED-THEORY-under-scrutinyMYTHDRIFT` and reproduce.
3. **SNOWFLAKE χ² = 22.03** — test specification (null hypothesis, dof,
   baseline distribution, independence assumption) must be clear.
   Action: recover CRYSTALOS logs; re-run analysis with explicit
   specification.
4. **MQW paper trilogy** — one Nakamura-related paper exists on
   Brayden's GitHub; full trilogy location unknown. Action: R16
   filesystem search per handoff §2.2 Priority 8.

## 8. January 2026 recovery (handoff JAN2026_RECOVERY_MANIFEST.md)

Recovery priorities (lowest-risk first):

- **P1** — 233-page `How_to_use_the_Lattice__full_derivations.pdf`
  (originally uploaded Jan 29, 2026). Primary target. R16 search.
- **P2** — TIG Unity Kernel deliverables (`tig9*` series). Recover from
  MYTHDRIFT repo `docs/COMPUTE.md`.
- **P3** — Trifecta (V20 Consciousness-Anchored Scaling Laws, Hardware
  Embodiment Safety Case v1.0, Comparative Field Theory Review) — 11
  documents, ~134 KB. Recover from `/home/claude/tig_*/` locations or
  R16 filesystem.
- **P4** — TIG Trinity canonical definition from Thread 4 (2026-01-29).
  Already preserved in memory (`memory/MEMORY.md`); verify against
  conversation archive.
- **P5** — SNOWFLAKE framework with empirical χ² = 22.03 — see §7 above.

Commits into `docs/archive_jan2026/` with provenance headers per
never-delete. Original binaries unchanged.

## 9. What this file does NOT do

- Does NOT commit the HELD README.
- Does NOT create any new funding branches.
- Does NOT merge side-branches into master (inventory only).
- Does NOT resolve the four validation tasks (requires external files
  + Brayden's input).
- Does NOT draft any funder-facing pitch letter.

## 10. The single next action

Ship venues 7 + 8 on Wednesday 2026-04-22. Everything else is preparation
or follow-on. The Sprint 34 pre-push audit has already fixed the ship
list; the typographic read + cover-letter addressee + arXiv upload are
the remaining humanly-required steps for that Wednesday.

---

*Add-only. Any future readiness snapshot = new dated file like
`Atlas/PUBLIC_SCRUTINY_READINESS_2026_MM_DD.md`.*
