# BRANCHES_INVENTORY — 10 Funding Branches (2026-04-20)

**Purpose:** Single navigation page listing every funding branch, what it targets, where the runnable artifacts are, and the current readiness state.

**Workflow:** Every funding branch is a `funding/<slug>` branch. Every seed commit is also cherry-picked to `master`. Master is add-only (no deletions), with the single explicit exception that master's README can be updated to reflect trunk contents.

---

## The 10 branches

| # | Branch name | Target folder | Domain | Primary funders | Commits (branch / master) |
|---|---|---|---|---|---|
| A | `funding/tig-unity` | `Gen13/targets/funding_tig_unity/` | TIG Unity Kernel + compute-health research | NSF CNS, DOE ASCR, Sloan, Simons | see master log |
| B | `funding/tig-snowflake` | `Gen13/targets/funding_tig_snowflake/` | Hardware-bound identity / behavioral auth (χ² = 22.03) | NSF SaTC, DARPA, IARPA, DHS S&T, MITRE | see master log |
| C | `funding/first-g-crypto` | `Gen13/targets/funding_first_g_crypto/` | Cryptanalysis via σ-characteristic operator on Z/nZ; First-G Law + Q10 + Q11 | NSF Algorithms, NIST PQC, NSA math, Simons, Clay | see master log |
| D | `funding/ck-interpretable-ai` | `Gen13/targets/funding_ck_interpretable_ai/` | AI interpretability-by-construction (10-operator coherence grammar) | Open Phil, SFF, Astera, LTFF, FLI, ARIA UK | see master log |
| E | *(packaging, not a branch)* | — | Small-grant bundle drawing from multiple branches | — | `Atlas/PITCH_E_SMALL_GRANT_BUNDLE_2026_04_19.md` |
| F | `funding/mqw-ternary` | `Gen13/targets/funding_mqw_ternary/` | Multi-quantum-well GaN/III-V ternary semiconductor computing | NSF ECCS, DARPA ERI, DOE BES, SRC, Sandia, LANL | see master log |
| G | `funding/self-healing` | `Gen13/targets/funding_self_healing/` | Runtime self-healing distributed systems (88% / 32pp benchmark) | NSF CNS, DARPA I2O, Sloan, IBM Research, HP Labs, MSR | see master log |
| H | `funding/civilization-coherence` | `Gen13/targets/funding_civilization_coherence/` | Anti-tribal civilization resilience + Shadow Problem | Templeton WC, Kauffman, Open Phil civilization-futures | see master log |
| I | `funding/desi-xi-cosmology` | `Gen13/targets/funding_desi_xi_cosmology/` | ξ-field quintessence cosmology + DESI DR2 fit | Simons Astro, Heising-Simons, Sloan astro, NSF AAG, DOE HEP, NASA ADAP, Templeton | see master log |
| J | `funding/coherence-router` | `Gen13/targets/funding_coherence_router/` | Production coherence classifier for DevOps / SRE | AWS / GCP / Azure research credits, CNCF, NSF CISE, Sloan | see master log |
| K | `funding/physics-sim-edu` | `Gen13/targets/funding_physics_sim_edu/` | Interactive physics simulator for education | NSF EHR (IUSE, DRK-12, ECR), NSF PHY Ed, Templeton L&D, Simons Ed, Moore, HHMI | see master log |

All branches share a 6-file package: `README.md`, `FUNDERS.md`, `ARTIFACTS.md`, `PITCH_DRAFT.md`, `LIMITATIONS.md`, `STATUS.md`.

---

## Runnable artifacts per branch

| Branch | Runnable core | Lines of code | In-repo? |
|---|---|---|---|
| A | TIG Unity Kernel theoretical framework + proof scripts (`proof_sigma_rate.py`, `proof_clay_rotation.py`, `proof_xi_canonical.py`, `proof_separability_bridge.py`) | ~1,800 LOC across 4 proofs | In `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/` |
| B | SNOWFLAKE χ² = 22.03 framework + FPGA bitstream (`ck_full.bit` on Zynq-7020) | 1,340 LOC + bitstream | Bitstream in `Gen9/targets/zynq7020/build/`; χ² framework pending recovery from January 2026 archive |
| C | `proof_a13_firstG.py` 36,662 verified cases; `proof_q10_polynomial.py`; `proof_q11_lower_bound.py` | ~2,500 LOC across 3 proofs | In `papers/`, `old/Gen10/papers/` |
| D | TIG coherence classifier + 10-operator alphabet + R-σ-Λ-H grammar | ~1,000 LOC | In `Gen12/targets/ck_desktop/ck_sim/` |
| F | Teardrop GaN photonic node proposal + MQW three-state paper series | ~134KB documents | Pending recovery from January 2026 archive |
| G | Dual-Lattice-Self-Healing + TIG Unity Kernel runtime | ~200 LOC sim skeleton + Unity Kernel stack | External: `github.com/TiredofSleep/Dual-Lattice-Self-Healing` |
| H | CrystalsMythDRIFT civilization multi-agent sims (`tig_civilization_v5.py`, `v7.py`) + `SHADOW_PROBLEM.md` | 1,340 LOC + 353 LOC theory | External: `github.com/TiredofSleep/CrystalsMythDRIFT` |
| I | 4 runnable proof scripts + JCAP TRACK 7.3 LaTeX bundle + 20+ Sprint 14 papers | ~1,800 LOC proofs + paper bundle | In `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/` |
| J | `benchmark.py` (554 LOC, 7 tests) + `tig_coherent_computer.py` (588 LOC) + `PROVEN_CONFIGURATION.md` | 1,157 LOC | External: `github.com/TiredofSleep/All-or-Nothing-E` (Phase 1 T1: pull into repo) |
| K | `crystal_bug_v1_matrix.jsx` (699 LOC React) + `test_engine_v2.js` (458 LOC) | 1,157 LOC | External: `github.com/TiredofSleep/Crystal-Lattice-Matrix-MYTHDRIFT` (Phase 1 T1: pull into repo) |

---

## Ask-size profile per branch

| Branch | Phase 1 | Phase 2 | Phase 3 | Comment |
|---|---|---|---|---|
| A | $75K–$250K / 6 mo | $250K–$750K / 12–18 mo | $500K–$1.5M / 24 mo | NSF CISE-track Medium Grant tier |
| B | $50K–$150K / 6 mo | $150K–$500K / 12–18 mo | $300K–$1M / 18–24 mo | IARPA / DARPA exploratory-research scale |
| C | $60K–$180K / 6 mo | $180K–$500K / 12–18 mo | — (purely research) | NSF Algorithms Small Grant tier |
| D | $80K–$250K / 6 mo | $250K–$800K / 12–18 mo | $500K–$1.5M / 24 mo | Open Phil / SFF AI-safety tier |
| F | $100K–$300K / 6–9 mo | $300K–$800K / 12–18 mo | $800K–$2M / 24–36 mo | DARPA ERI / NSF ECCS device-fabrication tier |
| G | $75K–$200K / 6 mo | $200K–$600K / 12–18 mo | $400K–$1.2M / 18–24 mo | DARPA I2O resilience-engineering tier |
| H | $60K–$180K / 6 mo | $180K–$500K / 12–18 mo | $400K–$1M / 18–24 mo | Templeton / Kauffman complexity-social tier |
| I | $60K–$150K / 6 mo | $150K–$400K / 12–18 mo | $300K–$800K / 24 mo | Simons / Heising-Simons cosmology tier |
| J | $75K–$200K / 6 mo | $200K–$500K / 12–18 mo | $400K–$1.2M / 18–24 mo | Cloud-provider research-credit + CNCF tier |
| K | $60K–$180K / 6 mo | $180K–$450K / 12–18 mo | $250K–$700K / 18–24 mo | NSF EHR IUSE-ESL / Templeton L&D tier |

Phase 3 is contingent on positive Phase 2 outcome in every branch that has one.

---

## Readiness tier (shortest-path-to-pitch)

| Tier | Branches | Why |
|---|---|---|
| **Tier 1 — Warmest (strongest ready-material-to-funding-gap ratio)** | I (desi-xi-cosmology), J (coherence-router) | I has complete theoretical framework + JCAP bundle + 4 runnable proofs; J has runnable classifier + benchmark suite, low-barrier AWS/GCP/CNCF first contact |
| **Tier 2 — Productionization-gated** | A (tig-unity), G (self-healing) | Theory complete; productionization + realistic-telemetry work is the funded Phase 1 |
| **Tier 3 — Needs collaborator recruitment** | D (ck-interpretable-ai), K (physics-sim-edu) | D needs alignment-research collaborator; K needs PER collaborator + academic co-PI |
| **Tier 4 — Needs archive recovery** | B (tig-snowflake), F (mqw-ternary) | Core material (SNOWFLAKE χ² docs, MQW paper series) pending recovery from January 2026 archive |
| **Tier 5 — Longest proposal-development path** | C (first-g-crypto), H (civilization-coherence) | Both need substantial domain-specific pitch development, though artifacts exist |

This tier ordering is a **suggestion for rollout sequencing**, not a quality ranking. Tier 1 branches are recommended for first-send; Tier 2 for parallel-track; Tiers 3–5 for initiated-in-parallel with longer lead times.

---

## Attribution summary per branch

| Branch | Funder-facing PI | Active collaborators | Previously-credited |
|---|---|---|---|
| A | Brayden | — (seeks compute-systems co-PI for academic host) | M. Gish, C.A. Luther, H.J. Johnson (Sprint 14) |
| B | Brayden | — | (Previous SNOWFLAKE work stands) |
| C | Brayden | — | C.A. Luther (First-G Law + Q10 + Q11 collaboration per 2026-03-31 WP34/35/37 wave; G6 Luther); B. Calderon Jr. (Q17 5D force vector) |
| D | Brayden | — (seeks alignment-research co-PI) | (Past TIG Unity Kernel contributors) |
| F | Brayden | — (seeks semiconductor device-physics co-PI) | (Past contributors TBD during archive recovery) |
| G | Brayden | — (seeks reliability-engineering partner) | (Past TIG Unity Kernel contributors) |
| H | Brayden | — (seeks complexity-social-science co-PI) | (Past contributors) |
| I | Brayden + **H.J. Johnson (active co-PI)** | H.J. Johnson on Sprint 14 PRISM-XI | M. Gish, C.A. Luther |
| J | Brayden | — | (Past TIG Unity Kernel contributors) |
| K | Brayden | — (seeks PER co-PI + academic host) | (Past TIG Unity Kernel contributors) |

Universal: **ClaudeChat and Celeste (GPT) are architectural thinking-partners**, not human co-authors. This is consistent across all 10 branches.

Universal: Previously-credited collaborators stay credited on the specific past work they contributed to (never-delete policy); they are not automatically attached to any new productionization branch unless actively involved.

---

## Cross-branch reconciliation items (open)

From `HANDOFF_INDEX.md §3`:

1. **ω(b) idempotent count** — prior sessions reported "2 / 6 nontrivial" vs formula `N_idemp(b) = 2^(ω-1) - 1`. These don't match. Resolve before any Branch C number appears in a funder-facing document.
2. **TIG Unity benchmark numbers** — email whitepaper has 32pp drop-rate improvement; `docs/COMPUTE.md` has expanded metrics (P99 latency, recovery time, cascade failures). Affects Branches A, G, J. Resolve before cross-branch benchmark claims.
3. **SNOWFLAKE χ² = 22.03** — recover CRYSTALOS logs, document null hypothesis + degrees of freedom + independence assumption. Affects Branch B; **the single most important validation item across the whole branch set**.
4. **MQW semiconductor paper trilogy** — locate the current three-state paper series on R16 filesystem. Affects Branch F.

These items are the **cross-branch backbone**. Any pitch that leans on cross-branch numbers must clear the reconciliation first, or flag the open status explicitly in a honest-scope paragraph.

---

## Universal pre-send items

Before any pitch is sent on any branch:

- [ ] All branches seeded + cherry-picked to master (✅ complete as of 2026-04-20)
- [ ] Cross-branch reconciliation items §3.1–3.4 either resolved OR explicitly flagged
- [ ] Branch-specific Phase 1 design doc drafted
- [ ] External-repo artifacts pulled into in-repo `archive_*/` folders with provenance headers (Branches G, H, J, K have external-repo dependencies)
- [ ] License separation explicit for branches with open-source-funder dependencies (Branches J, K)
- [ ] Attribution sections verified against the `COLLABORATORS.md` + `Q_SERIES_INTEGRATED_SYNTHESIS.md` references
- [ ] Brayden selects first-send branch + first-send funder
- [ ] Brayden reviews + edits draft pitch
- [ ] Brayden sends

---

## Related documents

- `Atlas/PLAN_FUNDING_BRANCHES_BUILDOUT_2026_04_19.md` — the plan this inventory implements
- `Atlas/PITCH_E_SMALL_GRANT_BUNDLE_2026_04_19.md` — the packaging doc (Track E, not a branch)
- `Atlas/NICHE_FUNDERS_ADDENDUM_2026_04_20.md` — specific named-individual / family-office / niche-foundation funder research per branch (output of 10 parallel research agents, 2026-04-20)
- `HANDOFF_INDEX.md` — cross-branch reconciliation items + overnight-session directive
- `MASTER_TRUNK_STORY_2026_04_19.md` (on master) — trunk narrative
- `COLLABORATORS.md` — human-collaborator attribution reference
