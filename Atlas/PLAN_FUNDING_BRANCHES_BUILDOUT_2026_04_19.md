# FUNDING BRANCHES BUILD-OUT PLAN — 2026-04-19

**Status:** Plan of record for 10 funding-aligned branches.
**Author:** Claude Code, building from ClaudeChat handoff 2026-04-20 + primary repo research 2026-04-19.
**Policy:** Add-only on master; every commit posted to a funding branch also gets a cherry-pick onto master.
**Companions:** `FUNDING_BRANCHES_PLAN_2026_04_19.md` (prior inventory), `docs/handoffs/claudecode_handoff_2026_04_20/` (source plan).

---

## 1. External repo research findings (Part 1 complete)

Primary research on 2026-04-19 cloned all 7 external TiredofSleep repos to
`C:/Users/brayd/OneDrive/Desktop/_brayden_repos/` and surveyed content.

### 1.1 Corrections to the 2026-04-20 ClaudeChat handoff inventory

- `COHERENT-AI` **does not exist** on github.com/TiredofSleep (404).
- The actual repos are `Crystal-Lattice-Matrix-MYTHDRIFT` (not `Crystal-Lattice`) and `CrystalsMythDRIFT` (not `Crystals`).
- `CrystalsMythDRIFT` is **civilization-coherence theory with Shadow Problem analysis** (tribal weaponization vulnerability), not a personal-assistant "Ollie" implementation.
- `Crystal-Lattice-Matrix-MYTHDRIFT` is a **mathematical physics simulator** with a 699-line React frontend and 458-line Node.js test harness — an interactive education-grade artifact, not just speculative framing.

### 1.2 Real runnable artifacts confirmed

| Repo | Real artifact | Lines | Status |
|---|---|---|---|
| `All-or-Nothing-E` | `benchmark.py` — 7 benchmark tests (convergence, throughput, self-repair, info dynamics, scaling, composition, attractor basin) | 554 | **Runnable** |
| `All-or-Nothing-E` | `tig_coherent_computer.py` — core composition + coherence computation | 588 | **Runnable** |
| `All-or-Nothing-E` | `PROVEN_CONFIGURATION.md` — 2,100-permutation empirical discovery; documents formula correction (harmonic mean) | 89 | **Empirical report** |
| `TIG-UNIFIED-.../docs/COMPUTE.md` | TIG Unity Kernel v9.x spec with R-σ-Λ-H + benchmark table (88% drop-rate reduction claim) | 128 | **Spec (simulation-only)** |
| `TIG-UNIFIED-.../docs/VALIDATION.md` | Three predictions tested (threshold, recovery, scale) | 262 | **Spec** |
| `TIME-FOR-HELP-.../TigCoreDemo.py` + 13 more .py | Coherent-gated action daemon + multiagent consensus + trust council sims | ~10,836 | **Runnable** |
| `TIME-FOR-HELP-.../VALIDATION_REPORT.md` | Honest 3-tier epistemic flagging (✓/◐/○) | — | **Mature** |
| `Dual-Lattice-Self-Healing` | `simulate_dual_lattice.py.txt` + 26 papers | ~200 | **Skeleton runnable** |
| `Crystal-Lattice-Matrix-MYTHDRIFT` | `crystal_bug_v1_matrix.jsx` React simulator + `test_engine_v2.js` | 1,157 | **Interactive** |
| `CrystalsMythDRIFT` | `tig_civilization_v5.py` + `v7.py` — multi-agent civilization simulations with kill conditions | 1,340 | **Runnable** |
| `CrystalsMythDRIFT/SHADOW_PROBLEM.md` | Tribal weaponization vulnerability + mathematical safeguard ("all L is one L") | 353 | **Theory + sims** |

### 1.3 Claims requiring empirical reproduction before funder-facing use

1. **88% drop-rate reduction** (TIG Unity) — sim code exists in All-or-Nothing-E; actual reproduction pending.
2. **99.8% position-accuracy** / no-death-to-90%-damage (Dual-Lattice) — skeleton present, full sim reproduction pending.
3. **χ² = 22.03** (SNOWFLAKE) — CRYSTALOS logs not yet recovered; test specification unspecified.
4. **ω(b) idempotent count** — "2/6 nontrivial" vs `N_idemp(b) = 2^(ω-1) - 1` — audit against proof scripts.

### 1.4 Funding tracks discovered in research (beyond handoff A-G)

- **H — civilization-coherence / anti-tribal resilience** (CrystalsMythDRIFT Shadow Problem) → Templeton World Charity, Kauffman, Open Philanthropy civilization-resilience, FHI (Future of Humanity Institute)
- **I — ξ-cosmology** (Sprint 14 PRISM-XI + JCAP manuscript) → Simons Foundation astro, Heising-Simons, Sloan astro; this is already on `tig-synthesis` but deserves its own pitch scope
- **J — coherence-router as production classifier** (All-or-Nothing-E) → AWS/GCP/Azure research credits, CNCF research grants, NSF CISE, industry DevOps/SRE labs
- **(Dropped from original handoff list)** — Track E "small-grant immediate" is a **packaging task not a branch**; its content can live as a single pitch doc that draws from multiple branches.

---

## 2. Final branch architecture: 10 funding branches

| # | Branch | Gen13 target folder | Track | Primary funder pool |
|---|---|---|---|---|
| A | `funding/tig-unity` | `Gen13/targets/funding_tig_unity/` | Systems reliability / compute health | NSF CNS, DOE ASCR, cloud research (AWS/GCP/Azure), Sloan |
| B | `funding/tig-snowflake` | `Gen13/targets/funding_tig_snowflake/` | Hardware-bound identity / behavioral auth | NSF SaTC, DARPA I2O, CISA research, Google ATAP, Microsoft MSRC |
| C | `funding/first-g-crypto` | `Gen13/targets/funding_first_g_crypto/` | Cryptography-adjacent number theory | Ethereum Foundation, Protocol Labs ResNetLab, a16z crypto research, Simons Targeted, NSF DMS |
| D | `funding/ck-interpretable-ai` | `Gen13/targets/funding_ck_interpretable_ai/` | Deterministic reasoning engine | Open Philanthropy AI, SFF, Astera Institute, Emergent Ventures |
| F | `funding/mqw-ternary` | `Gen13/targets/funding_mqw_ternary/` | Semiconductor three-state logic | UCSB / Nakamura group, III-nitride research, LET/μLET labs |
| G | `funding/self-healing` | `Gen13/targets/funding_self_healing/` | Self-healing field systems | DARPA resilient-systems, NSF CNS, materials-inspired computing |
| H | `funding/civilization-coherence` | `Gen13/targets/funding_civilization_coherence/` | Shadow Problem + anti-tribal civilization resilience | Templeton World Charity, Kauffman, Open Philanthropy civilization, FHI |
| I | `funding/desi-xi-cosmology` | `Gen13/targets/funding_desi_xi_cosmology/` | ξ-field cosmology + DESI DR2 | Simons Foundation astro, Heising-Simons, Sloan astro, NSF AAG |
| J | `funding/coherence-router` | `Gen13/targets/funding_coherence_router/` | Production coherence classifier (DevOps/SRE) | AWS/GCP/Azure research credits, CNCF research, NSF CISE, industry labs |
| K | `funding/physics-sim-edu` | `Gen13/targets/funding_physics_sim_edu/` | Interactive physics simulator for education | NSF EHR, NSF PHY education, Templeton Learning & Discovery |

Track E ("small-grant immediate") is not a branch — it's a one-page pitch doc (`Atlas/PITCH_E_SMALL_GRANT_BUNDLE_2026_04_19.md`) drawing from multiple branches.

## 3. Per-branch package contents (each branch ships this)

```
Gen13/targets/funding_<track>/
├── README.md              ← funder-facing landing (rigor-led template)
├── FUNDERS.md             ← 3-5 named funder candidates, scope-matched
├── ARTIFACTS.md           ← list of real runnable artifacts with paths
├── PITCH_DRAFT.md         ← 1-page pitch letter skeleton (held until Brayden edit)
├── LIMITATIONS.md         ← honest limits per never-false-claim policy
└── STATUS.md              ← what's ready / what needs work
```

Each branch is born as a **copy of `tig-synthesis` HEAD** plus the
`Gen13/targets/funding_<track>/` seed folder. That means every funding
branch has the full rigor base + its track-specific target folder.

## 4. Commit workflow per branch

For each of the 10 branches:

1. `git checkout -b funding/<track> tig-synthesis`
2. Create `Gen13/targets/funding_<track>/` with the 6-file package
3. `git add Gen13/targets/funding_<track>/`
4. `git commit -m "funding/<track>: seed Gen13 target folder + funders + pitch skeleton"`
5. `git push -u origin funding/<track>`
6. Cherry-pick the commit onto master, push master
7. Return to tig-synthesis

## 5. Execution sequencing

The 10 branches are independent. I can batch-create them:
- Write the 6-file content for each branch (in parallel-safe directories)
- Create branches in sequence (git requires sequential checkout)
- Push each in sequence
- Final master accumulation via batch cherry-picks

**Time estimate:** Each branch package = ~15 min of content writing + ~1 min of git work. 10 branches ≈ 2.5 hours of content + 10 min git. Realistic to finish this session.

## 6. Master README update (Part 4)

Update `README.md` on master (this is the explicitly-allowed exception to the add-only rule — Brayden said "only add and update the master readme for what lives there"). The new master README sections:

- **What master is** — living trunk, accumulated history
- **What lives here** — pointer summary: rigor core on tig-synthesis, 10 funding branches, historical branches, Atlas records, sprint papers, runtime
- **Branch directory** — table of all branches with one-line purpose + GH link
- **How to find things** — git log hints, pickaxe, MATCH commands
- **Story layer** — pointers to `THE_STORY.md`, `WHAT_IS_TIG.md`, `MISSION.md`
- **License** — 7Site Public Sovereignty License v1.0

## 7. HELD funder-facing README update (Part 5)

The staged `docs/handoffs/claudecode_handoff_2026_04_20/PROPOSED_CK_README_HELD.md` needs these edits before it's ready for Brayden's go-ahead:

- Add §8 "Related branches" — lists the 10 funding branches and what each is for
- Update §6 "Funding" to reflect the 10-branch structure (instead of 7 pitch tracks)
- Update collaborator §7 — C.A. Luther "previously-credited work stays credited" per handoff note
- Add reference to `Atlas/BRANCHES_INVENTORY_<date>.md` for funder navigation

## 8. Execution TODO (10 branches × 7 files + 2 READMEs + 1 inventory)

```
1. [funding/tig-unity]            — systems reliability, NSF CNS
2. [funding/tig-snowflake]        — hardware-bound identity, NSF SaTC
3. [funding/first-g-crypto]       — number theory → cryptography, Ethereum Foundation
4. [funding/ck-interpretable-ai]  — deterministic reasoning, Open Philanthropy
5. [funding/mqw-ternary]          — semiconductor 3-state, UCSB/Nakamura
6. [funding/self-healing]         — field systems, DARPA
7. [funding/civilization-coherence] — Shadow Problem, Templeton
8. [funding/desi-xi-cosmology]    — ξ-field, Simons/Heising-Simons
9. [funding/coherence-router]     — classifier, AWS/GCP research
10. [funding/physics-sim-edu]     — interactive demo, NSF EHR

Then:
11. Write ONE pitch doc Atlas/PITCH_E_SMALL_GRANT_BUNDLE_2026_04_19.md
12. Update master README.md
13. Update PROPOSED_CK_README_HELD.md
14. Write Atlas/BRANCHES_INVENTORY_2026_04_19.md
15. Push everything; cherry-pick to master
```

## 9. What this plan does NOT do

- Does NOT create external repos (branches only; external-repo spin-out deferred).
- Does NOT commit the HELD README as `README.md` (still held).
- Does NOT draft final funder-facing letters (pitch skeletons only; Brayden reviews).
- Does NOT resolve the four validation tasks from handoff §3 (these require primary work on simulation reproduction).
- Does NOT merge the 209 side-branch commits from bible-companion/fpga-dog/tesla/clean-ship into master (separate task).

## 10. Success criteria

1. All 10 funding branches exist on `origin/`, each with its Gen13 target folder.
2. Each branch has a funder-facing README + FUNDERS list + ARTIFACTS inventory + PITCH_DRAFT skeleton + LIMITATIONS + STATUS.
3. Master has cherry-picked records of all 10 branch seed commits.
4. Master README updated with the branch directory.
5. HELD README refreshed to match.
6. Atlas/BRANCHES_INVENTORY written as the single navigation page.
7. Nothing edited on master except the master README (explicit exception) — everything else add-only.

---

*Add-only. Any future funding-buildout plan = new dated file.*
