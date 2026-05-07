# Sprint: Factor 6 Derivation in Ω_DM = 44 × 6 / 1000

**Sprint type:** Open derivation (Layer 7 retrospective rigor)
**Priority:** High — blocks JCAP cosmology and Sprint 18 dark sector papers
**Estimated duration:** 1–3 days of compute + analysis

---

## Goal

Identify the canonical algebraic origin of the **factor 6** in the dark matter formula

> Ω_DM = 44 × 6 / 1000 = 264/1000 ≈ 0.264

The 44 is verified (cross-cycle disagreement between Creation cycle {1,3,7,9} and Dissolution cycle {2,4,6,8} in Z/10Z). The 6 is currently asserted as "CHAOS coefficient" without independent derivation. **This sprint locks the 6.**

Acceptance criterion: a single, defensible algebraic origin for the 6 that is forced by axioms A0–A5 and is independently verified by computation.

---

## Background

From Planck 2018 (arXiv:1807.06209), the cosmological matter budget is:

- Ω_b ≈ 0.0490 (visible baryon matter)
- Ω_DM ≈ 0.265 (dark matter)
- Ω_Λ ≈ 0.687 (dark energy)

TIG's algebraic forms match all three to three decimal places:

- Ω_b = 7² / 10³ = 49/1000 ✓
- Ω_DM = 44 × 6 / 1000 = 264/1000 (factor 6 unverified)
- Ω_Λ = (2 · 7³ + 1) / 10³ = 687/1000 ✓
- Closure: 49 + 264 + 687 = 1000 exactly

The factor 44 is forced:

```python
import numpy as np
ADD = np.array([[(i+j)%10 for j in range(10)] for i in range(10)])
MUL = np.array([[(i*j)%10 for j in range(10)] for i in range(10)])
creation = [1, 3, 7, 9]
dissolution = [2, 4, 6, 8]
disagreement = sum(abs(ADD[c,d] - MUL[c,d]) for c in creation for d in dissolution)
assert disagreement == 44  # ✓ verified
```

The factor 6 needs an analogous derivation.

---

## Candidate derivations (test all, lock the strongest)

### Candidate A: σ-cycle length

The σ permutation on Z/10Z has a 6-cycle: (1 7 6 5 4 2). The cycle length is 6.

**Test:** is the dark matter coefficient = |σ-orbit| = 6?

**Plausibility:** High. The σ-cycle is the active operator orbit (the non-fixed elements). Dark matter as "absorbed by TSML" maps to the σ-active orbit's projection.

**Verification script:**

```python
sigma = {0:0, 1:7, 2:1, 3:3, 4:2, 5:4, 6:5, 7:6, 8:8, 9:9}
non_fixed = [k for k in sigma if sigma[k] != k]
assert len(non_fixed) == 6
print(f"σ-cycle length = {len(non_fixed)}")
```

**Decision:** if Ω_DM = (cross-cycle disagreement) × |σ-cycle| / N³, then this is the canonical form.

### Candidate B: S_MAX perturbation cell count

In the TSML 3-layer decomposition TSML_10 = C₀ ⊕ S_MAX ⊕ S_ADD (Sprint 17), S_MAX has exactly 6 cells. These are the perturbation cells where TSML deviates from the C₀ rule via the σ-MAX rule.

**Test:** is the dark matter coefficient = |S_MAX| = 6?

**Plausibility:** Very high. S_MAX is intrinsically tied to the TSML lens construction (A5). The 6 cells of S_MAX are precisely the cells where the C₀ collapse is overridden by σ-resolution. This corresponds physically to "matter visible to the curvature lens but not the position lens."

**Verification script:**

```python
# Reference TSML
TSML = [
    [0,0,0,0,0,0,0,7,0,0],
    [0,7,3,7,7,7,7,7,7,7],
    [0,3,7,7,4,7,7,7,7,9],
    [0,7,7,7,7,7,7,7,7,3],
    [0,7,4,7,7,7,7,7,8,7],
    [0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],
    [7,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,8,7,7,7,7,7],
    [0,7,9,3,7,7,7,7,7,7],
]
# Reference C₀ table needs to be derived from C₀ rule:
# - VOID absorbs (0 ∘ x = 0)
# - off-Core (not in {0,7,8,9}) → HARMONY = 7
# - on-Core: smaller σ_units wins, σ-tie → HARMONY
# - HARMONY row absorbs everything except VOID → also 7
# Build C0_table, then S_MAX = TSML - C0_table at cells where they differ AND C0 < TSML
# Document the 6 cells explicitly.
```

**Action item:** explicitly construct C₀ table from the rule, identify the 6 S_MAX cells by name, and verify they are the perturbation cells claimed.

### Candidate C: Heartbeat sum

The heartbeat sequence [1, 3, 1, 1] has sum 6 and period 4. It encodes the per-cycle structural vibration.

**Test:** is the dark matter coefficient = sum(heartbeat) = 6?

**Plausibility:** Medium-high. The heartbeat is fundamental but its derivation is itself a separate sprint.

**Verification script:**

```python
heartbeat = [1, 3, 1, 1]
assert sum(heartbeat) == 6
assert len(heartbeat) == 4  # period matches S* = 4/7
```

### Candidate D: dim(SU(3)) − dim(SU(2))

In gauge theory, dim SU(3) = 8, dim SU(2) = 3, dim U(1) = 1. Various combinations give 6:
- dim SU(3) − 2 = 6
- dim SU(2) + dim U(1) + 2 = 6
- 2 × (dim SU(2)) = 6

**Plausibility:** Low — too many candidate combinations, no canonical choice forced by TIG axioms.

### Candidate E: Number of off-diagonal generator triple pairs

Each generator triple has 3 elements; pairs (a,b) with a ≠ b within a triple give 3 ordered pairs per triple. Three triples × 3 ordered pairs = 9, not 6. Try: unordered pairs = 3 per triple × 3 triples = 9. Try: 2 elements per triple sharing structure with another = 2 × 3 = 6.

**Plausibility:** Speculative — reverse-engineered to match 6.

### Candidate F: 6 = number of independent T* derivations

History claims six independent derivations of T* = 5/7 (torus aspect ratio, generator centroid/inverse, first-cyclotomic/first-obstruction, universal-semiprime unit density, FPGA silicon, journey/destination).

**Plausibility:** Numerologically suggestive but structurally weak. The number of derivations is not an algebraic invariant of the construction.

---

## Methodology

For each candidate A–F, run the verification script and answer:

1. Is the value 6 forced by the axioms A0–A5, or is it asserted?
2. Does the candidate have a physical interpretation that matches "dark matter as TSML-absorbed mass"?
3. Is there a TIG-internal proof that the candidate's 6 is THE 6 in the formula?

**Decision tree:**

- If exactly one candidate is forced by axioms AND has matching physical interpretation: lock it as canonical.
- If multiple candidates are forced: identify the deepest (most algebraically primitive) one.
- If no candidate is forced: the formula Ω_DM = 44 × 6 / 1000 should be **retracted** in favor of "Ω_DM = (cross-cycle disagreement × undetermined coefficient)" until a derivation is found.

---

## Recommended approach

**Strongest candidate: B (S_MAX perturbation cell count).** This is intrinsically tied to A5 (the two-lens projection construction), has a clear physical interpretation (perturbation = curvature-visible-but-position-invisible matter = dark matter), and is forced by the TSML construction. The fact that |S_MAX| = 6 is non-coincidental: it's the number of σ-MAX overrides needed to complete the table from C₀.

**Plan:**

1. Reconstruct the canonical C₀ table from the C₀ rule (axiomatic, not hardcoded).
2. Compute TSML_10 − C₀ to identify perturbation cells.
3. Classify each perturbation cell as S_MAX or S_ADD.
4. Verify |S_MAX| = 6 cells, |S_ADD| = 2 cells.
5. List the 6 S_MAX cells by their (i, j) coordinates and the σ-units argument that forces each.
6. Connect to the cross-cycle 44: each of the 44 disagreement cells is "scored" by the 6 S_MAX overrides into the dark matter contribution.
7. Run secondary checks: candidates A, C, D should NOT all give the same 6 (otherwise the choice is degenerate).

**Output deliverable:**

- `papers/wp_factor_6_dark_matter.md` — derivation document
- `tig/foundations/derivations/factor_6.py` — verification script
- Update to `TIG_FOUNDATIONAL_AXIOMS.md` Layer 3 table: change Ω_DM status from "Partially derived" to "Verified" with the canonical 6 = |S_MAX| derivation cited.

---

## Acceptance criteria

The sprint is complete when:

1. ✓ Canonical C₀ table is constructed from rules (not hardcoded).
2. ✓ S_MAX cells are identified by coordinates with σ-units justification.
3. ✓ |S_MAX| = 6 verified.
4. ✓ Connection to Ω_DM = 44 × |S_MAX| / 1000 is articulated with physical interpretation.
5. ✓ Alternative candidates (A, C, D) are evaluated and ruled out (or shown to be equivalent).
6. ✓ Verification script runs cleanly and produces the expected output.
7. ✓ Documentation passes review by Brayden.

---

## Connection to other sprints

- **SPRINT_V3_UNIQUENESS_THEOREM.md** — V3 will establish that the canonical pair is unique under axioms A0–A5; the C₀ rule's uniqueness in turn forces |S_MAX| = 6.
- **SPRINT_FACTOR_22_FINE_STRUCTURE.md** — independent. May share computational infrastructure (canonical table construction).
- **JCAP cosmology paper** — depends on this sprint locking. Cannot ship until factor 6 is derived.
- **Sprint 18 dark sector** — depends on this sprint locking.

---

## References

- TIG_FOUNDATIONAL_AXIOMS.md (parent reference)
- FORMULAS_AND_TABLES.md §7 (TSML 3-layer canonical tower)
- WP104 Pati-Salam paper
- Planck Collaboration (2018) arXiv:1807.06209
