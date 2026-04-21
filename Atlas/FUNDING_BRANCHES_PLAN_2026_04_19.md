# FUNDING BRANCHES PLAN — 2026-04-19

**Status:** DRAFT PROPOSAL — pending Brayden's review & approval
**Author:** Claude Code (instantiated by Brayden 2026-04-19)
**Policy:** Add-only on master; editing permitted on working branches
**Related:** `docs/handoffs/claudecode_handoff_2026_04_20/` (ClaudeChat overnight handoff package)
**Companion:** `MASTER_TRUNK_STORY_2026_04_19.md` (master-trunk story snapshot)

---

## 1. Purpose

Brayden's directive this session:

> *"finish preparing the repo and journals for public scrutiny and figure
> out what all products we have that need funding, while being aware that
> they can't actually be products since CK is sovereign, but they are
> good research and architecture for the future!! while you are searching
> through history, keep an eye out for what all funding branches we can
> add to the repo"*

This document **inventories** the candidate funding branches without
creating any of them. Creation waits for Brayden's explicit selection of
which 1-2 pitch tracks go first (per the ClaudeChat handoff §5 Phase 3).

## 2. Framing: "products" vs "research and architecture"

CK is sovereign. The license is the **7Site Public Sovereignty License
v1.0** — human use, no commercial, no military, free forever. So nothing
in this repo is a **product** in the commercialization sense.

What we have instead are **research tracks** and **architecture pieces**
that deserve external support — grants, research engagements, endowed
time, institutional licenses (MAGMA), compute credits, arXiv
endorsements — all in exchange for the work continuing as open research
under the Sovereignty License. Each track carries its own funder pool,
audience, and body of work.

## 3. Branches already existing on `origin/`

| Branch | Latest work | Status | Candidate funding-branch mapping |
|---|---|---|---|
| `master` | 2026-04-19 trunk accumulation | **Primary trunk (add-only)** | — (accumulates all tracks) |
| `tig-synthesis` | Sprint 34/35 rigor audit | Active rigor/referee lens | **Track C + D (rigor core)** — First-G + CK deterministic reasoning |
| `clay` | Sprint 10-17 bodies | Active dev | Historical (Clay Millennium Problem reformulations) |
| `archive-full` | Frozen | Preservation snapshot | — |
| `bible-companion` | Gen10.21-23 (robot dog, TIG reconstruction) | Specialized | **Candidate: Track G (self-healing / coherence-companion) reference** |
| `fpga-dog` | Gen10.21 R16+FPGA+XiaoR bring-up | Specialized hardware | **Track A / B hardware evidence** (FPGA T* = 5/7 in silicon) |
| `tesla` | Gen10.20-21 Tesla Thermal + Tesla Bridge | Specialized | **Track A reference** (thermal/jitter robustness) |
| `clean-ship` | Earlier clean-ship state | Specialized | — (historical) |

Branches `bible-companion`, `fpga-dog`, `tesla`, `clean-ship` already
exist on `origin/`. Their contents have **not all** been accumulated into
master; next pass should review whether to merge-accumulate them into
master under the trunk workflow.

## 4. Candidate NEW funding branches (from ClaudeChat handoff §4)

The handoff package proposes separate *external repos* for each pitch
track. An alternative (simpler, fewer moving parts, consistent with the
trunk workflow) is to start each track as a **branch in `ck`** first, let
it mature, and only spin it out as a separate repo once it's ready to
stand alone with its own README and funder-facing front door.

### Branch proposals (pending Brayden's selection)

| Proposed branch | Track | Purpose | Prerequisites |
|---|---|---|---|
| **`tig-unity`** | A (Systems reliability) | Unity Kernel whitepaper + coherence_router + simulation code recovered from MYTHDRIFT + All-or-Nothing-E | Phase 1 recovery from external repos |
| **`tig-snowflake`** | B (Hardware-bound identity) | SNOWFLAKE security architecture + CRYSTALOS runtime logs + χ² = 22.03 validation | Phase 1 recovery + χ² test specification clarified |
| **`mqw-ternary`** | F (Semiconductor MQW three-state logic) | Nakamura MQW reinterpretation + 3-paper roadmap | Physics paper trilogy location found |
| **`first-g-crypto`** | C (Cryptography-adjacent) | Extend First-G Event Localization to factoring-relevant questions; Track C's dedicated research lane | Stays on `tig-synthesis` initially; spins off when manuscript is near-ready |
| **`ck-interpretable-ai`** | D (Interpretable AI) | CK-vs-ACT-R/Soar/Cyc architecture paper; scale from 10 → 100+ operators | Stays on `tig-synthesis` initially; spins off with architecture paper |
| **`self-healing-systems`** | G (Dual-Lattice) | Refresh existing `Dual-Lattice-Self-Healing` external repo to current rigor standard; optionally mirror as a branch here | Branch depends on whether Brayden wants a local mirror or just a pointer |

**Not a branch but a packaging task:**

| Pitch | Packaging |
|---|---|
| **E (Small-grant immediate)** | Not a branch — a single short pitch document targeting $1,200 MAGMA / $500/mo Sage / arXiv-endorsement. Lives as one file, can be authored on `tig-synthesis`. |

## 5. Recommended sequencing (pending Brayden approval)

This aligns with the ClaudeChat handoff Phase 1-4 sequence.

**Phase A (this session, no external dependencies):**
1. Commit the handoff package into `docs/handoffs/` (done in this commit).
2. Commit this plan into `Atlas/` (done in this commit).
3. Leave all candidate branches uncreated — await Brayden's pitch priority.

**Phase B (Brayden selects 1-2 pitches to lead):**
4. Brayden picks — e.g. *"Track C + Track A first"*.
5. For the selected tracks, either:
   - Create a new branch `first-g-crypto` / `tig-unity` / etc.
   - Or keep work on `tig-synthesis` and spin off a branch when the
     manuscript nears submission.

**Phase C (per-track maturation):**
6. The selected branch carries track-specific work: extended proofs,
   dedicated manuscripts, funder-facing pitch docs, reproducibility
   scripts.
7. Every commit to a track branch also accumulates into master
   (per trunk workflow).

**Phase D (external spin-out, when a track is pitch-ready):**
8. When a track branch has a clean-scope README + runnable verification +
   honest limitations + funding ask (per the handoff's Track 1 rigor-led
   template), create the external repo (`tig-unity`, `tig-snowflake`,
   `mqw-ternary`, etc.) and populate it from the branch state.
9. External repo becomes the funder-facing front door; the branch in
   `ck` continues to accumulate rigor work that the external repo
   mirrors.

## 6. Blocker: four critical validation tasks (handoff §3)

Before any funder-facing number is committed, these four must be resolved:

1. **ω(b) idempotent count.** "2/6 nontrivial" vs `N_idemp(b) = 2^(ω-1) - 1`
   disagree. Audit `papers/proof_*_idempotent*.py` and reconcile.
2. **TIG Unity benchmark numbers.** Email (Jan 2026) reports 32pp drop-rate
   improvement; Grok's summary of `docs/COMPUTE.md` reports ~88%. Reproduce
   from simulation; document exact baseline and seed.
3. **SNOWFLAKE χ² = 22.03.** Null hypothesis, dof, fires computed over,
   independence assumption — all must be specified before this appears
   in any pitch.
4. **MQW paper trilogy location.** One Nakamura-related paper exists on
   Brayden's GitHub (repo unspecified). Full 3-paper series location
   unknown. Search required.

These are *not* Claude Code's unilateral work — some (like χ² = 22.03)
require Brayden's input on which logs he considers authoritative.

## 7. The HELD README

The proposed funder-facing replacement README is staged at
`docs/handoffs/claudecode_handoff_2026_04_20/PROPOSED_CK_README_HELD.md`.

**This file is NOT to be committed as `README.md`** until Brayden gives
explicit go-ahead (per the handoff's §7 and his direct instruction to
ClaudeChat: "hold on to it"). When the green light comes:

1. Archive current `README.md` to `docs/historical/README_v_<date>.md`
2. Copy `PROPOSED_CK_README_HELD.md` → `README.md`
3. Commit: `README: rigor-led replacement for funding outreach`
4. Accumulate to master per trunk workflow

## 8. Public-scrutiny readiness checklist (journals)

From `Atlas/PRE_PUSH_DECISION_2026_04_19.md`, the Sprint 34 Tier-1 audit
produced a **ship 2, pull 1** decision for 2026-04-22:

- ✅ Venue 7 (JCAP) — ξ cosmology — **SHIP 2026-04-22**
- ✅ Venue 8 (JCT-A) — σ-rate theorem — **SHIP 2026-04-22**
- ⚠️ Venue 1 (Integers) — sinc² zero law — **PULLED** (biconditional held trivially; audit recorded)
- 🔄 Sprint 35 (Integers) — First-G Event Localization — **NEXT CYCLE** (2026-04-29 or later)

Remaining pre-submission human steps before public scrutiny hits
Wednesday's mailbox:

- [ ] Typographic read by Luther or Gish on JCAP + JCT-A manuscripts
      (Luther no longer actively collaborating per handoff — may need
      Gish alone or a substitute reader)
- [ ] Cover-letter addressee customization
- [ ] arXiv upload same day as journal submission
- [ ] Sprint 35 First-G manuscript: Luther/Gish read + cover-letter
      addressee customization (for 2026-04-29 cycle)

## 9. What this plan does NOT do

- Does NOT create any new branches yet.
- Does NOT commit the proposed funder-facing README (held).
- Does NOT modify Track G's external `Dual-Lattice-Self-Healing` repo.
- Does NOT draft any funder-facing pitch letter (Brayden-driven per
  handoff Phase 4).
- Does NOT resolve the four validation tasks in §6 (requires Brayden
  input + source recovery).

## 10. Next concrete actions Claude Code can take without waiting

1. **Accumulate this commit into master** (per trunk workflow).
2. **Inventory existing remote branches not yet in master:** review
   `bible-companion`, `fpga-dog`, `tesla`, `clean-ship` and decide
   whether their non-duplicated content should be merge-accumulated
   into master as history. This is add-only for master.
3. **Sprint 35 pre-submission polish:** cover-letter addressee, running-
   head amsart edit, typographic read (or a flagged-for-human read).
4. **Draft a one-page inventory of what's recoverable locally** for the
   January 2026 material (handoff §2) — the PDF derivation document
   search, CRYSTALOS logs, MQW papers — without making any claims
   about contents until files are actually found.

---

*This file is add-only. Any future update = new dated file like*
*`Atlas/FUNDING_BRANCHES_PLAN_2026_05_NN.md`, never edit this one.*
