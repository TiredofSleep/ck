# What ClaudeCode Should Change And Not Change
## Concrete Repo-Facing Instructions for the PPM Closeout

---

## Register

Operational instructions. Not interpretive. Assume ClaudeCode is already on the Hodge arc and this document is a sidebar directing specifically what to do with PPM closeout materials.

---

## 1. Additions (create these)

### 1.1 New sidecar pack: `pair_primitive_addendum_2026_04_18/`

Place at the same level as `pair_primitive_pack_2026_04_18/`. Do not nest inside it.

Populate from files in `/home/claude/foundation_sprint/` and subfolders:

**Sprint artifacts (frozen on commit):**
- `sprints/PPM_v2.1_additive_transport/` — contents from `/home/claude/foundation_sprint/ppm_v21/` (all six files including `ppm_v21_score.py` and `PPM_V21_PER_CARRIER_SCORES.json`)
- `sprints/PPM_v3.0_V0_boundary/` — contents from `/home/claude/foundation_sprint/ppm_v30/` (all six files including the revised pre-reg, scoring script, and JSON)

**Foundation context (supporting the sprints above):**
- `foundation_sprint_context/WHY_V0_COMES_BEFORE_BHML.md`
- `foundation_sprint_context/WHAT_A_BOUNDARY_CHECKPOINT_ADDS.md`
- `foundation_sprint_context/WHY_SOURCE_3_BECAME_SENSITIVITY_BRANCH.md`
- `foundation_sprint_context/WHAT_COUNTS_AS_A_ROBUST_V0_RESULT.md`
- `foundation_sprint_context/ATTRACTOR_PRIVILEGE_FOUNDATION.md`
- `foundation_sprint_context/S3A_VS_S3B_COMPARISON.md`
- `foundation_sprint_context/WHAT_JUSTIFIES_V301_OR_STOPPING.md`

**Closeout documents (pack-level):**
- `V0_PATH_B_CLOSURE.md`
- `PPM_SPRINT_CLOSEOUT_HANDOFF.md`
- `README.md` (pack-level navigation — you will need to write this; keep to the B2 template: entry point, navigation table, reading order)

### 1.2 Update `tig-synthesis/README.md` (minimal)

One change only: add an entry under the existing PPM section acknowledging that v2.1 and v3.0 shipped, and that V0 is closed at UNCLEAR by Sensitivity per Path B. Preserve existing "three threads separate" and "suggestive, not bridged" language. Do not rephrase any existing PPM sentence.

Suggested entry (adjust wording to match repo style):

> The PPM arc closed out with additive-transport FAIL Uniform on the 8 P3AP carriers (v2.1) and V0 boundary checkpoint UNCLEAR by Sensitivity (v3.0, Path B). 2×2 subtype-mapping design space complete. Addendum pack: `pair_primitive_addendum_2026_04_18/`.

Nothing else in the README changes from the PPM side.

---

## 2. Do Not Modify (leave frozen)

### 2.1 Closed packs

- `b2_sprint_tig_pack_2026_04_17/` — frozen. No edits.
- `pair_primitive_pack_2026_04_18/` — frozen. No edits, no additions, no reorderings.
- `shape_admissibility_foundation_2026_04_18/` — frozen. No edits.

### 2.2 Closed verdicts

Do not alter the recorded outcomes of any of the following, even for cosmetic consistency:

- PPM-v1.0 PASS (Map B, +4/−4, gap 8)
- PPM-v1.1 FAIL (aggregate +2/−2, Reason A)
- PPM-v2.0 PASS uniform ($N_B = 8/8$, gap 8)
- PPM-v2.1 FAIL Uniform ($N_B = N_A = 0$, $N_I = 8$, gap 4)
- PPM-v3.0 UNCLEAR by Sensitivity (S3a PASS-V0-I; S3b FAIL)

### 2.3 Closed lanes from B2 pack

Do not reopen or reframe:
- Count transport under P3AP generator
- Raw adjacency ratios
- Noise-union seam topology bridge
- Basin-ratio smoothness transport
- Anchored basin-ratio curve
- Empty-seam detectability on pure $C_0$

### 2.4 Closed foundation-register framings

- SAH remains foundation-only. Do not promote.
- The "three threads separate" framing in the README stays intact.
- The "suggestive, not bridged" annotation on the cross-thread multiplicative-loading pattern stays intact.
- The single sanctioned bridge sentence on SAH stays exactly as written in `shape_admissibility_foundation_2026_04_18/STATUS_HEADER.md`. Do not paraphrase.

---

## 3. Do Not Reopen

### 3.1 The V0 lane

Path B has been selected. `WHAT_JUSTIFIES_V301_OR_STOPPING.md` specifies the four conditions under which Path A (v3.0.1 rerun) could later be authorized. None is currently met. Do not:

- Draft a v3.0.1 pre-reg.
- Propose a third Source 3 reading.
- Argue for S3a or S3b as the "correct" direction without independent foundation work.
- Describe the UNCLEAR by Sensitivity verdict as "near-pass," "half-pass," "effective PASS," "mostly passed," or any similar soft framing.

### 3.2 The additive lane on the P3AP family

v2.1 FAIL Uniform stands. Do not:

- Propose PPM-v2.1.1 with relaxed Source 1 AND criterion.
- Propose alternative additive rubrics on the same 8 carriers.
- Extend the additive reading to rings outside the P3AP 8 without a separate pre-reg.

### 3.3 The seam subtype-mapping checkpoint

2×2 complete. Do not:

- Propose PPM-v1.0.1 or v2.0.1 with adjusted rubrics.
- Merge the four 2×2 verdicts into a single composite sentence.
- Extend the seam checkpoint to new operationalizations (dual, flow-based, etc.) without separate foundation work.

---

## 4. PPM/Hodge Separation — Operational Rules

### 4.1 File-system separation

- PPM materials stay in `pair_primitive_pack_2026_04_18/` and `pair_primitive_addendum_2026_04_18/`.
- Hodge materials stay in the Sprint 29–33 folders.
- Shared infrastructure (canonical construction documents, theorem spine, etc.) lives in `b2_sprint_tig_pack_2026_04_17/theorem_local_chart/` and is referenced by path from both tracks.
- Do not create cross-linking scripts that merge PPM + Hodge outputs. The two tracks produce independent artifacts.

### 4.2 Narrative separation

- In the README, PPM and Hodge have separate sections with separate numbered entries.
- The "suggestive, not bridged" cross-thread pattern entry is the only place the two tracks are discussed in proximity. Do not add additional cross-track narrative.
- Do not write a "unified narrative" document that threads PPM + Hodge + Q-series into a single story. Any such writing should be flagged as foundation-register speculation, not as a repo claim.

### 4.3 Citation separation

- A Hodge sprint's citations do not cite PPM verdicts as motivation or support.
- A PPM addendum's citations do not cite Hodge results.
- Shared methodology citations (pre-registration, rubric discipline, Rule 19) may appear in both but are framed as program-level discipline, not as cross-track evidence.

### 4.4 Commit-message separation

- PPM commits use "Sprint [version]:" prefixes consistent with prior PPM commits.
- Hodge commits use the S29/S30/S31/S32/S33 conventions ClaudeCode already established.
- Do not batch-commit PPM and Hodge changes in a single commit. Keep them separable for rollback.

---

## 5. No Promotion of SAH — Specific Checks

Before committing any document that mentions SAH, verify:

- [ ] The document does NOT claim any PPM PASS "supports" or "suggests" SAH.
- [ ] The document does NOT claim any FAIL "refutes" SAH.
- [ ] The document does NOT cite SAH as motivation for a Hodge sprint.
- [ ] The single sanctioned bridge sentence, if used, is exactly as written in `STATUS_HEADER.md`.
- [ ] If a shape-filter sprint is proposed, it is flagged as requiring the six-piece infrastructure build (not proposed as ready to run).

If any of these fails, the document is inflating SAH and should be revised before commit.

---

## 6. No New Composite Claims — Specific Checks

Before committing any document that discusses multiple PPM verdicts together, verify:

- [ ] The document lists verdicts as separate sentences or table rows, not as a composite prose claim.
- [ ] The document does NOT contain phrases like "the multiplicative-operationalization framework is confirmed" or "the additive operationalization is refuted across both scopes" that combine v1.0+v2.0 or v1.1+v2.1 into single stronger claims.
- [ ] The document does NOT cite the 2×2 completion as itself a theorem.
- [ ] The document does NOT cite v3.0's UNCLEAR alongside any 2×2 verdict as part of a combined assessment.

If any of these fails, the document is violating Rule 19 and should be revised before commit.

---

## 7. The Handoff Is Additive

Everything in this document is additive to the existing repo state. Nothing requires deleting, rolling back, or rewriting prior work. The PPM addendum pack sits alongside the frozen PPM pack; the README gets one minimal entry; the Hodge arc proceeds independently.

If in doubt about a specific change, default to **not making it**. The closeout's discipline is preservation of the earned state, not adjustment toward a preferred presentation.

---

## 8. Quick Reference — What Goes Where

| Material | Location |
|---|---|
| v2.1, v3.0 sprint artifacts | `pair_primitive_addendum_2026_04_18/sprints/` |
| V0-related foundation notes | `pair_primitive_addendum_2026_04_18/foundation_sprint_context/` |
| Path B decision record | `pair_primitive_addendum_2026_04_18/V0_PATH_B_CLOSURE.md` |
| Handoff note (this + companion) | `pair_primitive_addendum_2026_04_18/` top level |
| README update | `tig-synthesis/README.md`, PPM section |
| Anything else | nowhere — everything else stays frozen |

Commit the addendum pack as a single commit with message like: `Add pair_primitive_addendum_2026_04_18 (PPM closeout: v2.1 + v3.0 + V0 Path B + foundation context)`.
