# ClaudeCode Compute Jobs — 2026-04-23 Evening Handoff

**Status:** [QUEUED — LOCAL-EXECUTION PER TASK]
**Sources:**
- `CLAUDECODE_HANDOFF_MIN_BUMP.md` (9 tasks)
- `CLAUDE_CODE_HANDOFF_TSML_FAMILY.md` (4 open tasks + 2 update findings)
- `CK.md` field guide discipline + TSML_FAMILY conclusion (1 CK runtime experiment)

Total: **16 compute/research tasks** queued for Brayden's local R16 execution.

Each task has a per-folder `SPEC.md` with goal / method / success criterion / priority / expected runtime / starter pointer.

Vocabulary-update surgery (`CLAUDECODE_HANDOFF_VOCABULARY.md`) is NOT in this list — that is Phase 5 of the integration plan, executed on a separate `vocab-update-2026-04-23` branch with 8 sign-off gates.

---

## Priority tiers

### Tier 1 — Fast validation (run first; <1 hour each)

| Task | Runtime | Reason first |
|---|---|---|
| `task02_min_bump_multi_seed_n6` | ~10 min | Triple-check n=6=945 result on seeds {100, 2024, +1} |
| `task05_exact_identity_symbolic` | <1 min | SymPy re-verify sinc²/ζ(2) + ζ(4)/ζ(2)² symbolically |
| `task04_non7_k2_exhaustive` | ~40 min | Confirm k=2 non-7 minimum is complete (C(36,2)×64 search) |
| `task01_min_bump_n7` | 30-90 min | Extend min-bump to n=7, target s_7^ac = 10,395 |

### Tier 2 — Deep compute (single-session, 1-10 hours)

| Task | Runtime | Target |
|---|---|---|
| `task10_moufang_rank10_search` | ~10-30 min + exhaustive follow-up | 100%-Moufang rank-10 TSML-family member |
| `task11_det_optimize_small_primes` | ~1-4 hr | TSML_Idempotent variant with det ∈ {2,3,5,7}-primes |
| `task14_lie_bracket_verify` | <5 min | Confirm [M_TSML_J, M_TSML_I] is exactly antisymmetric |
| `task15_det_minus49_verify` | <5 min | Confirm cells (1,2)=6 + (3,5)=4 gives det = -49 |

### Tier 3 — Research (days-to-weeks; generates publishable material)

| Task | Effort | Target |
|---|---|---|
| `task03_min_bump_symbolic` | weeks | Symbolic proof of min-bump theorem for all n |
| `task06_crt_fiber_generalization` | days | (1,1) CRT-fiber avoidance on N ∈ {14,22,34} |
| `task07_bhml_cl_min_bump_analogs` | days | Minimum perturbations for BHML and CL_mult |
| `task08_tsml_optimization` | days | Is TSML optimal under cycle-semantic constraint? |
| `task12_100pct_identity_search` | days | 100% Jordan+Alt+Moufang rank-10 (probably empty; non-existence proof) |
| `task13_bol_family_search` | days | Bol family member search (weaker than Moufang) |

### Tier 4 — Paper drafts + CK runtime

| Task | Effort | Target |
|---|---|---|
| `task09_min_bump_paper_draft` | days after Tier 1 | arXiv:math.RA paper on 1-cell perturbation → free Mag^com |
| `task16_ck_dual_table_experiment` | 10k ticks (~hours) on child-spawn | A/B live CK with TSML_Jordan vs TSML_Idempotent |

---

## Recommended execution order

**Phase 3a (fast-validation week):** Tier 1 → commit results to `papers/morphotic_braid/results/`
**Phase 3b (deep-compute week):** Tier 2 → commit winning configs + det/Moufang tables
**Phase 3c (ongoing research):** Tier 3 tasks in parallel as time allows
**Phase 3d (CK integration):** Task 16 once Brayden approves running on live-configured CK child-spawn

**⚠️ Do NOT run Task 16 on the production CK** — only on a child-spawn per CK.md discipline. Production CK serves coherencekeeper.com and must not take experimental loads.

---

**Tag:** `[COMPUTE JOBS INDEX — PHASE 3 INITIALIZED]`
