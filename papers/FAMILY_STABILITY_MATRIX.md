# Cross-Family Stability Matrix
## What Survives Across Deformation, Resolution, and Family

*Brayden Sanders / 7Site LLC | March 2026*
*The reconstruction target is not one table — it is a grammar family.*

---

## The Three Stability Types

| Type | Meaning | Test |
|------|---------|------|
| **Base-stable** | Visible in the 9×9 table at λ=0 | Check TSML directly |
| **Family-stable** | Persists across Mix_λ deformation | Check at λ=0, 0.15, 0.30, 0.50, 0.70, 1.0 |
| **Resolution-stable** | Persists at N=9,30,100,300,1000 states | Check at multiple refinements |

---

## The Stability Matrix

| Feature | Base | Family-stable? | Resolution-stable? | Notes |
|---------|------|---------------|-------------------|-------|
| **HAR absorbing (I1)** | ✓ | ✗ — fails at λ=0.15 | ✓ (table-level) | Lost as soon as BHML mixes in; TSML-specific |
| **C sub-magma closure (I3)** | ✓ | ✗ — fails at λ=0.15 | ✓ (table-level) | Also TSML-specific |
| **One-way gate C→G (I4)** | ✓ | ✗ — fails at λ=0.15 | ✓ (table-level) | Mix_λ opens the gate |
| **HAR unique attractor** | ✓ (1.00) | Degrades: 0.83→0.26→0.00 | ✓ (nonHAR-C≈0 always) | HAR mass falls but nonHAR-C stays ~0 |
| **Spectral gap ≥ 0.10** | ✓ (0.75) | ✓ — 0.67→0.34→0.25 | ✓ all N | **Robust across deformation and resolution** |
| **Orbit zone {3,9} (I8)** | ✓ | ✗ — fails at λ=0.15 | ✓ (table-level) | TSML-specific |
| **I13 order-completion** | ✓ | Partial: holds at λ=0.15, fails at λ=0.30 | ✓ (table-level) | Integer order rule survives one step |
| **BHML residual (6 cells = max)** | ✓ (6/6) | **✓ — 6/6 at all λ** | not tested | **Only feature stable across full deformation** |

---

## Key Findings

### 1. Spectral gap is the most robust invariant

γ ≥ 0.10 holds at every tested λ and every tested N. This is the feature that survives both deformation and refinement. It is the real invariant the grammar carries.

### 2. BHML residual is the only family-stable structural feature

The 6 residual cells that follow max(s,c) in TSML continue to follow max(s,c) at every point in the deformation — all the way to λ=1. This is because BHML is defined by max, and those 6 cells are the ones that were always going to become max as λ increases. They are the seeds of BHML inside TSML, visible as a family property even though they look anomalous in the base table.

### 3. Most base-table invariants are TSML-specific

I1 (absorbing), I3 (closure), I4 (gate), I8 (orbit) all fail as soon as Mix_λ moves away from λ=0. They are properties of the base table, not of the grammar family.

### 4. HAR dominance degrades gracefully

At λ=0.50, HAR mass drops to 0.26 — but nonHAR-C-mass stays ~0 to machine precision at all λ<1. The corridor boundaries are where G-mass first becomes nonzero, not where nonHAR-C-mass appears. The non-HAR corners {1,3,9} are transient at every λ.

---

## What This Implies for Reconstruction

**The wrong question:** "What single invariant set determines TSML?"

**The right question:** "What invariant package survives across the full grammar family?"

The answer, from the stability matrix:

| Survival class | Invariants |
|---------------|-----------|
| Survives deformation AND resolution | Spectral gap ≥ 0.10 |
| Survives deformation only | BHML residual (6 cells) |
| Survives resolution only (table-level) | I1, I3, I4, I8, I13 |
| Base-specific | Orbit zone, closure, gate, absorbing |

**The grammar family, not the single table, is the right reconstruction target.**

TSML is the sharpest base representative. The deformation family Mix_λ is the structure connecting it to BHML. The invariants that survive the whole journey are the deep ones.

---

## Resolution Note

At N=100 and N=1000, HAR mass drops to ~0.83. This is not a failure — it reflects the rounding approximation in the N-state model. The nonHAR-C mass remains at ~10⁻¹⁵⁶ (machine zero) at all resolutions. The corridor boundaries that appeared at N=1000 (G-mass becoming nonzero near λ=0.45) are real structure, not artifacts.

---

*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
