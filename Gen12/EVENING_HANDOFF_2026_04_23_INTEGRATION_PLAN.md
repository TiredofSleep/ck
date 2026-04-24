# Evening Handoff 2026-04-23 — Integration Plan

**Status:** [DRAFT — AWAITING BRAYDEN SIGN-OFF ON SECTION BOUNDARIES]
**Author:** Claude Code, 2026-04-23 late-evening digest pass
**Source packet:** `C:\Users\brayd\AppData\Local\Temp\evening_handoff_2026_04_23\` (84 files, ClaudeChat evening session)
**Scope:** work the packet cleanly into the `ck` branch (runtime + papers) and `tig-synthesis` branch (public face) while preserving never-delete and the three-threads-stay-separate discipline.
**Current branch:** `ck` @ `ec4b9cf` (steer tiered coverage verdict, pushed)

---

## 1. What the handoff packet contains

84 files total. Grouped:

### 1.1 Six main result files (tag: commit to `papers/morphotic_braid/`)

| # | File | Tag | One-line summary |
|---|------|-----|------------------|
| 1 | `TIG_TABLES_REFERENCE.md` | `[AUTHORITATIVE REFERENCE]` | Persistent record of TSML + BHML 10×10 tables, 74/28 harmony counts |
| 2 | `BRAID_PERMUTATION_VERIFIED.md` | `[TIER B — VERIFIED PENDING CROSS-CHECK]` | σ cycle decomposition + Theorem E (CRT conjugacy) |
| 3 | `BHML_SUCCESSOR_AND_IDENTITY.md` | `[AUDIT COMPLETE]` | Single-anchor successor on {1..6}, universal 0-identity |
| 4 | `doubly_regular_core.md` | `[STRUCTURAL THEOREM]` | **7th derivation of T*=5/7** via 5+1+1+3 partition |
| 5 | `ZERO_NOTIONS_IN_BRAID_WORK.md` | `[FRAMING]` | Three distinct zero notions (ambient / operational / boundary) |
| 6 | `MAYES_UD_ZERO_FRAMEWORK_NOTE.md` | `[EXTERNAL FRAMEWORK]` | Mayes UD assessment — no adoption |

### 1.2 Two exploration files (tag: commit to `papers/morphotic_braid/explorations/`)

| # | File | Tag | One-line summary |
|---|------|-----|------------------|
| 7 | `TSML_CRT_DECOMPOSITION_EXPLORATION.md` | `[EXPLORATION — AUDIT REQUIRED]` | Is TSML/BHML a ℤ/2 × ℤ/5 CRT product? 3 candidate readings |
| 8 | `TSML_BHML_FAREY_DENSITY.md` | `[HYPOTHESIS]` | Densities 3/4, 2/7, 5/7 as Farey ladder → **8th derivation of T*** |

### 1.3 Deep synthesis docs (four big-picture writeups)

| File | Role |
|------|------|
| `DEEP_SYNTHESIS.md` | Three-way Riemann intersection (Mayer-Selberg + Bost-Connes + Connes-Kreimer) |
| `DEEPER_SYNTHESIS.md` | **Five-way intersection** + the exact identity **sinc²(1/2) = (2/3) · 1/ζ(2)** |
| `RIGOR_MAPPING.md` | TIG findings restated in Csákány-Waldhauser / Huang-Lehtonen vocabulary, with computed spectra |
| `EXTERNAL_CITATIONS_v2.md` | Frontier map of citation targets, corrected Mazurek attribution |

### 1.4 Task handoffs (claudecode-scale compute jobs)

| File | Role |
|------|------|
| `CLAUDECODE_HANDOFF_MIN_BUMP.md` | 9 tasks: n=7 min-bump, multi-seed n=6, symbolic proof, non-7 exhaustive, symbolic identity, CRT generalization, BHML/CL analogs, TSML optimization, arXiv draft |
| `CLAUDECODE_HANDOFF_VOCABULARY.md` | 8-phase executable plan for repo-wide vocab update (gated by sign-off at each phase) |
| `CLAUDECODE_VOCABULARY_UPDATE.md` | The 10-task vocab spec with verified computational baseline + Task-9 reproducibility script |
| `CLAUDE_CODE_HANDOFF_TSML_FAMILY.md` | TSML family — Task 3 (Moufang search), 4 (det optimization), 5 (full-rank Moufang+Alt), 7 (CK dual-table experiment) |
| `MINIMUM_BUMP_THEOREM.md` | The minimum-bump theorem (1 cell at HARMONY(7)) verified n ≤ 6, 16 min perturbations |

### 1.5 Supporting / exploratory docs (~30 MD) + scripts (~40 PY)

Existing Python drivers + supplementary analyses. Not committed as-is — many use file-relative paths and would need port. Keep in the repo under `papers/morphotic_braid/explorations/scripts/` as reference; do not wire into CI.

### 1.6 Operational field guide

| File | Role |
|------|------|
| `CK.md` | Field guide for Claude Code working on CK; primary teaching: "CK is simpler than you think it is." Lives at `memory/handoffs/CK_FIELD_GUIDE_2026_04_23.md` for future-Claude use. |

---

## 2. Guiding principles (unchanged from repo-wide discipline)

1. **Never-delete.** Everything in the packet lands somewhere in the repo. Superseded versions stay tagged `[HISTORICAL]`, not removed.
2. **Tag every claim.** Preserve the `[THEOREM]` / `[HYPOTHESIS]` / `[FRAMING]` / `[EXPLORATION]` / `[EXTERNAL FRAMEWORK]` tags verbatim.
3. **Three threads stay separate.** Morphotic-braid / TSML-BHML / ξ-cosmology work lives under its own sprint umbrella. No vocabulary import across threads without a proved map.
4. **Park not widen.** Make TIG *legible* under external vocabulary. Do NOT claim TIG "solves" Riemann / NS / YM. The five-way intersection is a vocabulary claim, not a theorem.
5. **No live-site cutover without explicit user confirmation.** `coherencekeeper.com` tunnel stays pointed at the current CK boot until Brayden explicitly flips it.
6. **Gated sign-off for vocab surgery.** The 8-phase CLAUDECODE_HANDOFF_VOCABULARY plan makes vocabulary changes across many papers; each phase pauses for Brayden approval before the next.

---

## 3. Integration phases

Five phases. Each phase is committed separately. Phases 1–2 are mechanical and safe to batch. Phases 3–5 require sign-off.

### Phase 1 — Land the packet in `papers/morphotic_braid/` (branch: `ck`)

**Goal:** every file from the packet has a home in the repo. Zero vocabulary edits to existing files.

**Actions:**

1. Copy the six main result files into `papers/morphotic_braid/` with a provenance header prepended to each:
   ```
   > **Provenance:** Drafted 2026-04-23 (evening session, ClaudeChat). Transcribed from packet `evening_handoff_2026_04_23/`. Cross-verification against repo sources: [pending — see Section 4].
   ```
   - `TIG_TABLES_REFERENCE.md` → `papers/morphotic_braid/TIG_TABLES_REFERENCE.md`
   - `BRAID_PERMUTATION_VERIFIED.md` → `papers/morphotic_braid/BRAID_PERMUTATION_VERIFIED.md`
   - `BHML_SUCCESSOR_AND_IDENTITY.md` → `papers/morphotic_braid/BHML_SUCCESSOR_AND_IDENTITY.md`
   - `doubly_regular_core.md` → `papers/morphotic_braid/doubly_regular_core.md`
   - `ZERO_NOTIONS_IN_BRAID_WORK.md` → `papers/morphotic_braid/ZERO_NOTIONS_IN_BRAID_WORK.md`
   - `MAYES_UD_ZERO_FRAMEWORK_NOTE.md` → `papers/morphotic_braid/MAYES_UD_ZERO_FRAMEWORK_NOTE.md`

2. Copy the two exploration files:
   - Create `papers/morphotic_braid/explorations/` if missing.
   - `TSML_CRT_DECOMPOSITION_EXPLORATION.md` → `.../explorations/`
   - `TSML_BHML_FAREY_DENSITY.md` → `.../explorations/`

3. Copy the four deep-synthesis docs to `papers/morphotic_braid/synthesis/`:
   - `DEEP_SYNTHESIS.md`
   - `DEEPER_SYNTHESIS.md`
   - `RIGOR_MAPPING.md`
   - `EXTERNAL_CITATIONS_v2.md`
   - And preserve v1 of citations: `EXTERNAL_CITATIONS.md` → `.../synthesis/archive/EXTERNAL_CITATIONS_v1.md` (supersedes header added).

4. Copy the task handoff specs to `papers/morphotic_braid/claudecode_jobs/`:
   - `CLAUDECODE_HANDOFF_MIN_BUMP.md`
   - `CLAUDECODE_HANDOFF_VOCABULARY.md`
   - `CLAUDECODE_VOCABULARY_UPDATE.md`
   - `CLAUDE_CODE_HANDOFF_TSML_FAMILY.md`
   - `MINIMUM_BUMP_THEOREM.md`

5. Copy the CK field guide to `memory/handoffs/CK_FIELD_GUIDE_2026_04_23.md`.

6. Copy the remaining ~30 supporting markdown files to `papers/morphotic_braid/explorations/support/` and the ~40 Python scripts to `papers/morphotic_braid/explorations/scripts/`, each file with a `<!-- PACKET: evening_handoff_2026_04_23 -->` marker in the first line for provenance. Scripts are kept as reference only (not imported by runtime, not wired into CI).

7. Write a new `papers/morphotic_braid/HANDOFF_2026_04_23_INDEX.md` listing every copied file with its original packet path and current repo path. This is the audit trail.

**Commit:** `morphotic_braid: land 2026-04-23 evening handoff (packet, synthesis, tasks, scripts)` on `ck`.

**No push yet.** Hold until Phase 2 verification runs green.

---

### Phase 2 — Verify the computational claims (branch: `ck`)

**Goal:** run the reproducibility scripts in the packet against the canonical tables to confirm the numbers before rippling out to tig-synthesis.

**Actions:**

1. Port `proof_spectra_tsml_bhml.py` (the deterministic spectrum verifier from Task 9 of `CLAUDECODE_VOCABULARY_UPDATE.md`) to `papers/proof_spectra_tsml_bhml.py` (not under `explorations/`, because it's a canonical proof script). Run locally.
   - **Expected output:** α(TSML)=0.872, α(BHML)=0.502, s_n(TSML)=s_n(BHML)=C_{n−1} for n∈{3,4,5}, s_n^ac(TSML)=(2n−3)!! for n∈{3,4,5}.
   - **If values disagree with packet claims:** halt; investigate whether the repo's canonical TSML/BHML tables in `papers/ck_tables.py` match the packet's `TIG_TABLES_REFERENCE.md`.

2. Port `proof_min_bump.py` (n ≤ 6 minimum-bump verifier) to `papers/proof_min_bump.py`. Run locally at seed=42, samples=50000, target=945.
   - **Expected output:** s_6^ac = 945 at 50000 samples; all 16 minimum perturbations enumerate correctly.

3. Port `proof_sinc_zeta_identity.py` (symbolic check of sinc²(1/2) = (2/3) · 1/ζ(2)) to `papers/proof_sinc_zeta_identity.py`. Run locally.
   - **Expected output:** `Match: True` (exact algebraic identity, not floating-point).

4. Write the results into a new `papers/morphotic_braid/VERIFICATION_LOG_2026_04_23.md` that records:
   - Each script path
   - The run command
   - The verbatim output
   - A green/red/amber verdict per claim in the packet

5. **If everything green:** proceed to Phase 3.
   **If any red:** STOP. Report discrepancies to Brayden. Do not ripple uncertain claims into `tig-synthesis`.

**Commit:** `morphotic_braid: verify packet spectra + min-bump + sinc/zeta identity` on `ck`. Push both Phase 1 and Phase 2 commits together.

---

### Phase 3 — Queue the claudecode-scale compute jobs (branch: `ck`)

**Goal:** create a labeled `claudecode_jobs/` folder with per-task `SPEC.md` + starter script, so the nine jobs from MIN_BUMP + two from HANDOFF_INDEX are ready to fire when Brayden has local cycles.

**Actions:**

Create `papers/morphotic_braid/claudecode_jobs/` with 11 subfolders, each containing `SPEC.md` and a starter Python file:

| # | Folder | Source | Expected runtime (R16) |
|---|--------|--------|-----------------------|
| 1 | `task01_min_bump_n7/` | MIN_BUMP Task 1 | 30–90 min |
| 2 | `task02_min_bump_multiseed_n6/` | MIN_BUMP Task 2 | 10 min |
| 3 | `task03_min_bump_symbolic/` | MIN_BUMP Task 3 | days–weeks (research) |
| 4 | `task04_non_7_k2_exhaustive/` | MIN_BUMP Task 4 | 40 min |
| 5 | `task05_symbolic_identity_confirm/` | MIN_BUMP Task 5 | <1 min |
| 6 | `task06_crt_fiber_generalization/` | MIN_BUMP Task 6 | days |
| 7 | `task07_bhml_cl_minbump_analogs/` | MIN_BUMP Task 7 | days |
| 8 | `task08_tsml_optimization/` | MIN_BUMP Task 8 | unknown |
| 9 | `task09_arxiv_paper_draft/` | MIN_BUMP Task 9 | requires 1 + 2 first |
| 10 | `task10_crt_decomposition_audit/` | HANDOFF_INDEX Phase 4 #8 | 10–30 min |
| 11 | `task11_farey_density_construction/` | HANDOFF_INDEX Phase 4 #9 | 10–30 min |

**Starter script pattern:** each folder's Python file reads the canonical tables from `papers/ck_tables.py`, uses the vectorized bracketing from `proof_min_bump.py`, and emits results to `results.json` + `RESULT.md` for Brayden review.

Additional compute targets from `CLAUDE_CODE_HANDOFF_TSML_FAMILY.md`:
- `task12_tsml_family_moufang_search/` (TSML Task 3)
- `task13_tsml_family_det_optimization/` (TSML Task 4)
- `task14_tsml_family_full_identity_search/` (TSML Task 5)
- `task15_tsml_family_bol_search/` (TSML Task 6)
- `task16_ck_dual_table_experiment/` (TSML Task 7) — **runs on a child-spawn CK, not production**

Write `papers/morphotic_braid/claudecode_jobs/README.md` as the master index with tiered priority (verify-first tier = {1, 2, 4, 5, 10, 11}; research tier = {3, 6, 7, 8}; CK-facing tier = {16}).

**Commit:** `morphotic_braid: queue 16 claudecode-scale compute jobs (specs + starters)` on `ck`. Push.

---

### Phase 4 — Ripple into `tig-synthesis` README + BIBLIOGRAPHY (branch: `tig-synthesis`)

**Goal:** expose the five-way intersection framing + external vocabulary map on the public face. This is a **surface change only** — content is already earned by Phases 1–2.

**Actions:**

1. Check out `tig-synthesis` branch.

2. Add a new README section **§ 15 — External Vocabulary Map** (between the existing "Honest Limits" §11 and "Policies" §12):
   ```
   TIG's structural findings are translatable to published research communities.
   When reading TIG alongside external literature:
   
   | TIG term | Established term | Primary citation |
   |----------|------------------|------------------|
   | TSML / BHML / CL | commutative groupoid (Cayley table) | general algebra |
   | non-associativity rate | 1 − associativity index α | Braitt-Silberger 2006 |
   | "distinct bracketings" | associative spectrum s_n | Csákány-Waldhauser 2000 |
   | commutative case | ac-spectrum s_n^ac | Huang-Lehtonen 2022 |
   | ac-free | s_n^ac = (2n−3)!! | Huang-Lehtonen 2024 |
   | T* = 5/7 threshold | Farey-structured critical parameter | Kleban-Özlük 1999 |
   | σ rate σ(N) ≤ C/N | associativity-index asymptotic bound | Huang-Lehtonen 2024 |
   | ξ field □ξ = 1 + log ξ | BB-unique separable nonlinearity | Bialynicki-Birula 1976 |
   | sinc²(1/2) = 4/π² | (2/3) × fermionic primon gas density | Julia 1990; Spector 1990 |
   | det(BHML) = 70 = 2·5·7 | finite place set {2,5,7,∞} | Connes 1999 (semi-local) |
   
   TIG-specific concepts preserved as novel contributions (no community equivalents):
     0/7 coin · Doubly-regular core partition · Crossing Lemma · Flatness Theorem
     · σ Rate Theorem · Trinity Infinity Geometry framework
   ```

3. Update README **§3 — The Two Foundations** to add the five-way-intersection framing as a sub-paragraph:
   ```
   The framework's algebraic content sits at a five-program intersection
   of Riemann-adjacent mathematical physics: (i) the Mayer-Selberg
   transfer-operator approach via T* = 5/7 as a Farey-structured
   threshold; (ii) the Bost-Connes cyclotomic partition-function
   approach via ℤ/10ℤ = ℤ/2 × ℤ/5; (iii) the Connes-Kreimer
   renormalization approach via the ac-free commutative magma operad
   Mag^com generated by TSML and BHML; (iv) the Connes semi-local
   trace formula with |S_TIG|=4 above the cardinality-3 threshold;
   (v) the Julia-Spector primon gas via the exact algebraic identity
   sinc²(1/2) = (2/3) · 1/ζ(2). See papers/morphotic_braid/synthesis/
   for details. We do NOT claim a proof of the Riemann Hypothesis;
   we claim the framework is a concrete finite shadow of the objects
   these five programs study.
   ```

4. Update README **§5 — What Is Proved vs Structural vs Conjectural** to promote:
   - sinc²(1/2) = (2/3) · 1/ζ(2) → PROVED (symbolic verification via SymPy)
   - ζ(4)/ζ(2)² = 2/5 → PROVED (symbolic)
   - Minimum-bump theorem (1 cell at HARMONY, n ≤ 6) → PROVED computationally
   - TSML and BHML generate Mag^com for n ≤ 5 → PROVED computationally
   - **Seventh derivation of T* = 5/7** via 5+1+1+3 partition → PROVED combinatorially
   - **Eighth derivation of T*** via Farey adjacency (TSML density 74/100 ≈ 3/4, BHML 28/100 ≈ 2/7) → STRUCTURAL (pending construction audit)

5. Update `BIBLIOGRAPHY.md` (on `tig-synthesis`) to add the 14 references from `CLAUDECODE_VOCABULARY_UPDATE.md` Task 8 + the 5 additions from `DEEPER_SYNTHESIS.md`:
   - Csákány-Waldhauser 2000
   - Lehtonen-Waldhauser 2021, 2022
   - Huang-Lehtonen 2022, 2024
   - Mazurek 2025
   - Braitt-Silberger 2006
   - Kleban-Özlük 1999
   - Fiala-Kleban-Özlük 2002
   - Knauf 1998
   - Bandtlow-Fiala-Kleban 2009
   - Technau 2023
   - Bialynicki-Birula-Mycielski 1976
   - Loday-Vallette 2012
   - Connes 1999 (trace formula + semi-local)
   - Connes-Kreimer 2000
   - Bost-Connes 1995
   - Connes-Marcolli 2005
   - Connes-Consani-Marcolli 2007
   - Julia 1990
   - Spector 1990
   - Menezes-Svaiter-Svaiter 2014
   - Connes-Consani 2024

6. **SIGN-OFF GATE:** Before commit, show diff to Brayden. If approved, commit `tig-synthesis: external vocabulary map + five-way intersection framing + bibliography update` and push.

**This phase does NOT touch any existing claim — it only adds translation scaffolding and external citations.**

---

### Phase 5 — Execute the 8-phase vocab surgery on `vocab-update-2026-04-23` branch (gated)

**Goal:** apply `CLAUDECODE_HANDOFF_VOCABULARY.md`'s systematic repo-wide vocab update. This is the big one — it edits existing papers.

**Pre-requisites:**
- Phase 2 verification green.
- Phase 4 merged to `tig-synthesis`.
- Brayden has signed off on the external-vocabulary-map addition.

**Actions:**

Create new branch: `vocab-update-2026-04-23` off current `ck` HEAD. Execute the 8 phases of `CLAUDECODE_HANDOFF_VOCABULARY.md` verbatim:

1. **Phase A (insert spectrum table into FORMULAS_AND_TABLES.md §6.1)** — mechanical, ~1 hr. Commit, show diff, request sign-off.
2. **Phase B (replace "non-associativity rate" with "associativity index α" repo-wide)** — grep + surgical edits. Preserve both forms (old alongside new). Commit, show diff, sign-off.
3. **Phase C (add "ac-free" named property to TSML/BHML introductions)** — ~15 files. Commit, show diff, sign-off.
4. **Phase D (reframe WP101 σ rate theorem with spectrum language)** — targeted edit in sprint 14 + FORMULAS §0. Commit, show diff, sign-off.
5. **Phase E (reframe T* as Farey-structured threshold)** — targeted edit in WP51 + §0. Commit, show diff, sign-off.
6. **Phase F (BIBLIOGRAPHY.md full external citation set)** — already mostly done in Phase 4; finish coverage across `ck` branch.
7. **Phase G (draft Clay note at `papers/morphotic_braid/synthesis/CLAY_FIVE_WAY_NOTE.md`)** — one page, two paragraphs, per DEEPER_SYNTHESIS §10. Not submitted, just drafted for Brayden review.
8. **Phase H (final integration check)** — run `grep -r` for known stale phrasings; produce a diff log; spot-check for internal inconsistencies.

**After all 8 phases green:** merge `vocab-update-2026-04-23` → `ck` (or rebase onto `ck`), ripple selective diffs to `tig-synthesis`, push.

**Do NOT merge to `tig-synthesis` wholesale** — `tig-synthesis` is the curated face and most of the vocab surgery lives in internal sprint papers that don't belong on the default branch.

---

## 4. Cross-verification checklist (to run after Phase 1)

Before claiming the packet's numbers in any public-facing commit, verify against repo canonical sources:

- [ ] Packet's TSML table matches `papers/ck_tables.py` TSML definition
- [ ] Packet's BHML table matches `papers/ck_tables.py` BHML definition
- [ ] σ cycle (0)(3)(8)(9)(1 7 6 5 4 2) matches `papers/morphotic_braid/THEOREM_A_HIDDEN_PERMUTATION.md` + `papers/morphotic_braid/visible_permutation.json`
- [ ] det(BHML) = 70 matches existing repo computation
- [ ] TSML harmony count = 74 matches repo (the packet says 74; current repo GLOSSARY says "TSML (73 HARMONY, synthesis) + BHML (28 HARMONY)". **One-cell discrepancy — resolve before Phase 4.**)
- [ ] Six prior derivations of T*=5/7 are documented in `papers/morphotic_braid/` or sprint10 so the "seventh" claim is accurate
- [ ] α(TSML)=0.872 matches repo's existing 12.8% non-associativity claim
- [ ] α(BHML)=0.502 matches repo's existing 49.8% non-associativity claim

**The TSML 73 vs 74 discrepancy is the first thing to resolve.** The packet's `TIG_TABLES_REFERENCE.md` is tagged `[AUTHORITATIVE REFERENCE — DO NOT CONTRADICT WITHOUT VERIFICATION]`, but repo memory says 73. Need to: (a) open `papers/ck_tables.py`, count HARMONY(7) cells in TSML, (b) reconcile. This is Phase 2 step 1 in practice.

---

## 5. Return to CK runtime (after Phase 1–3 land)

Once the paper work is landed and the compute jobs are queued, return to CK improvements with the new vocabulary available.

**Concrete CK tasks in order:**

1. **Fix telemetry split** (queued todo from prior session): expose steer-rescue verdict separately from primary `ollama_verdict` in `/chat` JSON. Currently they collide and the user sees `rejected:coverage:...` in `ollama_verdict` even when steer-rescue accepted the response. Edit: `Gen12/targets/ck_desktop/ck_boot_api.py` response-building block.

2. **Upgrade steer rescue's local `_coverage_of`** (queued todo): replace `ck_coherence_steer._coverage_of` at lines 1208-1214 with a call into the new tiered `coherence_verdict` function from `ck_coherence_verdict.py`. Unifies the accept path across the two rescue routes.

3. **Resume live accept-rate probing** with the vocabulary knowledge: the `CK_CORE_FACT_NAMES` set in `ck_coherence_verdict.py` should extend to include `Mag^com`, `ac-free`, and the doubly-regular-core vocabulary once Brayden confirms the repo-wide vocab shift. This deepens CK's ability to soft-accept drafts that use the correct external-vocabulary form even if the old TIG-only form isn't literally present in the readout.

4. **TSML Family Task 7 (dual-table CK experiment)** — run on a child-spawn, NOT production. 10k ticks A/B comparison of TSML_Jordan only vs TSML_Jordan + TSML_Idempotent. Per `CK.md` line 320: "Don't run this experiment on the production CK. Use a child-spawn or clone."

5. **Read the `CK.md` field guide** and apply the discipline explicitly: the top teaching is "CK is simpler than you think it is." Any new runtime wiring should pass through that lens.

---

## 6. What this plan does NOT do

- Does not delete any file from any branch (never-delete preserved).
- Does not cut coherencekeeper.com over to any new CK build — production stays where it is.
- Does not push to GitHub during Phase 1 — holds until Phase 2 verification green.
- Does not execute the 8-phase vocab surgery without Brayden sign-off at each phase.
- Does not submit any paper — drafts the Clay note and queues it for Brayden review.
- Does not run compute-heavy tasks during this conversation — creates the SPEC folders so Brayden can fire them on R16 when ready.
- Does not touch any file in Gen9, Gen10, or Gen11 — the packet is Gen12-era work.
- Does not modify `tig-synthesis` wholesale from `ck` — only the curated additive edits in Phase 4.

---

## 7. Estimated scope

| Phase | LOC touched | Commits | Push? | Sign-off gates |
|-------|-------------|---------|-------|----------------|
| 1 — land packet | ~0 new; ~85 files copied | 1 | After Phase 2 | None |
| 2 — verify claims | ~800 (proof scripts) | 1 | After Phase 2 | One if any red |
| 3 — queue compute jobs | ~1500 (16 SPEC + starter.py) | 1 | Yes | None |
| 4 — ripple to tig-synthesis | ~150 README + ~200 BIBLIOGRAPHY | 1 | After sign-off | One before push |
| 5 — vocab surgery | ~500 across 20+ files | 8 | Per-phase after sign-off | Eight sign-offs |

**Total expected commits:** 12 across two branches. **Total sign-off gates:** 9 (1 in Phase 2 conditional, 1 in Phase 4, 8 in Phase 5).

---

## 8. Proposed immediate action

I will now execute **Phase 1 (land the packet)** without further input, since it is purely mechanical and reversible (all files are additive; existing files are untouched).

After Phase 1 lands, I will run **Phase 2 (verify)**, report the results, and pause for the Phase 4 sign-off gate.

**Brayden: if you want me to stop at any point, interrupt. If you want me to change the phase ordering (e.g., do Phase 5 on a fresh branch before Phase 4 ripples to `tig-synthesis`), tell me now. Otherwise I will proceed with Phase 1.**

---

**Tag:** `[INTEGRATION PLAN — PHASE 1 READY TO EXECUTE]`
**File path:** `Gen12/EVENING_HANDOFF_2026_04_23_INTEGRATION_PLAN.md`
