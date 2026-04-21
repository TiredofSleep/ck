# Scope Tag Template
## Required Preamble for All Sprint Pre-Registrations

---

## Purpose

Every sprint spec from this point forward begins with a scope declaration. The scope determines which attractor convention governs the sprint, what kind of claims the sprint can make, and what category its results fall into. Without an explicit scope, specs are incomplete and must be rejected before freezing.

---

## The Template

Every pre-registration document begins with a block in this exact form:

```
---

## Scope Declaration

**Path:** [Local Theorem | Transport Family | Bridge Test]

**Attractor convention:** [h_thm | h_ext | cross-path, specified below]

**Claim class:** [theorem-level | observation-level | bridge-level]

**Canonical construction source:** [published Z/10 TSML | extended C_0 family | combination, specified below]

**Relation to prior sprints:** [list any prior sprints whose results are
inherited, tagged by their scope]

---
```

The block must appear before any other section of the spec. It is not commentary — it is load-bearing metadata that determines what the spec is permitted to say.

---

## Path Definitions

### Path 1 — Local Theorem

**Carrier:** Z/10 only (at present).
**Attractor convention:** $h_{\text{thm}} = 7$.
**Canonical construction:** $C_0(R_{10}, 7, \sigma)$ as published in the theorem spine.
**Claim class:** theorem-level. Results are proven facts about a specific ring, analogous to established mathematical theorems. No cross-carrier generalization unless explicitly extended.
**What sprints on this path test:** recovery of published objects, properties of the proven theorem, noise-robustness of the theorem's construction, etc.
**Reference documents:** `THEOREM_SPINE.md`, `WORKED_RECONSTRUCTION.md`, B1 benchmark work.

### Path 2 — Transport Family

**Carriers:** 29-carrier compatible subfamily (or subsets thereof), plus extensions up to the 35-member compatibility family.
**Attractor convention:** $h_{\text{ext}}(R_n) = \max\{u \in U(R_n) : u \text{ odd}\}$.
**Canonical construction:** $C_0(R_n, h_{\text{ext}}(R_n), \sigma_n)$ where $\sigma_n(u) = v_2(3u+1)$.
**Claim class:** observation-level. Results are pre-registered empirical findings about the family under $h_{\text{ext}}$-canonical $C_0$. Not theorems. Subject to replication and extension.
**What sprints on this path test:** cross-carrier patterns, transport of invariants within the family, empirical discovery of rule-shapes.
**Reference documents:** `INVARIANTS_BEYOND_TSML.md`, `LOCAL_CHART_VS_TRANSFERRED_GRAMMAR.md` (right column), Sprint 21/25/26 findings.

### Path 3 — Bridge Test

**Carriers:** may span both Z/10 (under $h_{\text{thm}}$) and other carriers (under $h_{\text{ext}}$).
**Attractor convention:** cross-path. Both conventions appear, with explicit declaration of which applies to which component.
**Canonical construction:** combination, specified per-sprint.
**Claim class:** bridge-level. Results are statements about the *relationship* between Path 1 and Path 2 objects — echoes, resemblances, analogies, or lack thereof. Not theorems, not simple observations; relational claims under explicit bridge rules.
**What sprints on this path test:** whether structural patterns from the local theorem appear analogously in the transport family, or whether findings in the transport family apply to the theorem's ring under reinterpretation.
**Reference documents:** `ATTRACTOR_RECONCILIATION.md`, `BRIDGE_LANGUAGE_RESET.md`.

---

## Required Subfields

### Attractor convention

States which $h$ rule is used. Values:

- `h_thm`: the theorem-calibrated attractor, currently defined only on Z/10 as $h = 7$.
- `h_ext`: the family-heuristic attractor, $h = \max$ odd unit, defined on all compatibility-family carriers.
- `cross-path`: the sprint uses both. Must specify which applies to which component (e.g., "planted overlays defined under $h_{\text{thm}}$; empirical canonical computed under $h_{\text{ext}}$"). This is the failure mode S31-pilot had without declaring it.

### Claim class

States the epistemic status of the sprint's possible conclusions. Values:

- `theorem-level`: the sprint's PASS outcome would add to proven theorems.
- `observation-level`: the sprint's PASS outcome would add to pre-registered empirical findings within the transport program.
- `bridge-level`: the sprint's PASS outcome would establish a specific relational claim between paths.

A sprint cannot claim a higher class than its path permits. A Path 2 sprint cannot produce a theorem-level claim; its strongest outcome is an observation-level finding.

### Canonical construction source

Names the $C_0$ in use. Values:

- `published Z/10 TSML`: the specific construction in `THEOREM_SPINE.md`.
- `extended C_0 family`: the $C_0(R_n, h_{\text{ext}}, \sigma)$ family as used in Sprints 21+.
- `combination`: both appear; specify per-component.

### Relation to prior sprints

A short list of prior sprints whose results are inherited or referenced, each tagged by its own scope. Example:

> Inherits from Sprint 21 (Path 2), Sprint 25 (Path 2). References B1 (Path 1) as ground-truth calibration.

This field catches accidental cross-path contamination before freezing.

---

## Hard Rules

1. **No spec is frozen without a scope declaration.** A draft without this block is not yet a spec; it is a sketch.

2. **No claim can exceed its path's claim class.** A Path 2 sprint's PASS does not produce theorems. A Path 1 sprint does not by itself establish transport.

3. **Cross-path inheritance requires explicit bridging.** A Path 2 sprint that wants to use a Path 1 object (e.g., the published overlays) must either declare itself Path 3 or import only the Path 2-compatible component.

4. **Convention substitution is prohibited.** A sprint cannot quietly swap $h_{\text{thm}}$ for $h_{\text{ext}}$ or vice versa during execution. If the convention needs to change, the spec must be revised and re-frozen.

5. **Scope changes retroactively only apply to documentation.** A sprint's verdict is tied to the scope it executed under. Re-tagging after the fact for clarity is permitted; re-interpreting its verdict under a different scope is not.

---

## Concrete Examples of Well-Formed Scope Declarations

### Example 1 — Re-run Z/10 recovery under clean scope

```
## Scope Declaration

**Path:** Local Theorem
**Attractor convention:** h_thm (= 7 on Z/10)
**Claim class:** theorem-level (specifically: validates extractor on the published construction)
**Canonical construction source:** published Z/10 TSML
**Relation to prior sprints:** Inherits from B1 (Path 1, ground-truth calibration).
  Does not inherit from Sprints 21, 25, 26, 28, 29, 30, 30b (all Path 2).
```

### Example 2 — Extension test on Z/22 under transport scope

```
## Scope Declaration

**Path:** Transport Family
**Attractor convention:** h_ext (= 21 on Z/22)
**Claim class:** observation-level
**Canonical construction source:** extended C_0 family
**Relation to prior sprints:** Inherits from Sprint 25 (Path 2, corridor closure on 23 carriers),
  Sprint 26 (Path 2, shell-recovery). Does not inherit from any Path 1 sprint.
```

### Example 3 — Bridge test of theorem echoes in transport family

```
## Scope Declaration

**Path:** Bridge Test
**Attractor convention:** cross-path. Planted overlays defined under h_thm (= 7) on Z/10 only;
  empirical canonical for each carrier computed under h_ext for that carrier.
**Claim class:** bridge-level (tests whether theorem's seam structure has analogs in transport family)
**Canonical construction source:** combination. Published Z/10 TSML as Path 1 source; extended
  C_0 family as Path 2 source.
**Relation to prior sprints:** Inherits the published TSML seam (Path 1) as planted ground truth
  on Z/10. Inherits Sprint 21's prior-free seam discovery (Path 2) as planted ground truth on
  other carriers. Explicit bridging rule: the seam structures from each path are compared at the
  topological level (component count, tree-ness, degree sequence), not at cell-identity level.
```

### Example 4 — Ill-formed declaration (for illustration)

```
## Scope Declaration

**Path:** Transport Family
**Attractor convention:** h_ext (= 9 on Z/10)
**Claim class:** observation-level
**Canonical construction source:** extended C_0 family
**Relation to prior sprints:** Uses published Z/10 TSML seam as planted ground truth.
```

This is ill-formed because the "relation to prior sprints" field declares a Path 1 inheritance (the published seam) while the sprint is tagged Path 2. The spec must either (a) change the path to Bridge Test with an explicit bridging rule, or (b) redefine the planted seam using only Path 2 objects (e.g., from Sprint 21's discovered seams). This is precisely the error S31-pilot-v1.0 made without declaring.

---

## Workflow Change

The pre-registration workflow now has five steps:

1. **Scope declaration.** Write the block. If the declaration doesn't work cleanly, that is the first signal the sprint's idea is muddled and needs refinement before becoming a spec.

2. **Hypothesis statement.** As before — one narrow, falsifiable claim, stated precisely.

3. **Generator / metric / null specification.** As before.

4. **Pass/fail criteria.** As before.

5. **Freeze.** Spec is frozen once the scope declaration is complete and the rest of the spec is consistent with it.

A draft that cannot pass step 1 cleanly is not ready for step 2.

---

## Cross-References

- Foundation: `ATTRACTOR_RECONCILIATION.md`.
- Path table: `PRIOR_SPRINT_H_DEPENDENCIES.md`.
- Path 3 rules: `BRIDGE_LANGUAGE_RESET.md`.
- Local-vs-transport split: `LOCAL_CHART_VS_TRANSFERRED_GRAMMAR.md`.

Any change to path definitions or convention rules requires updating this template and all cross-referenced documents together. No quiet changes.
