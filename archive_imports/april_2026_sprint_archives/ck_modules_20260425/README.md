# CK Modules — Dimension Mapper & DOF Profile Monitor

**For:** Claude Code (review & integration)
**Source session:** 2026-04-25 so(10) sprint
**Status:** Both modules pass full test suite (14/14)

---

## What's here

Two standalone Python modules for CK, each implementing one of the proposals from the meta-note review (with corrections). No third-party dependencies beyond `numpy`.

### 1. `ck_dimension_mapper.py` — LoRA rank distribution from canonical DOF dims

Maps verified TIG DOF subspace dimensions to per-layer LoRA ranks. You tag each layer with a DOF, the module distributes a rank budget proportional to canonical dimensions (Lie 28, Jordan 55, Clifford 36, Permutation_vector 9, Lattice 4, total 132).

**Key API:**
```python
from ck_dimension_mapper import compute_lora_ranks

config = compute_lora_ranks(
    layer_dof_assignments={
        "attn.q_proj": "lie",
        "attn.k_proj": "lie",
        "attn.v_proj": "jordan",
        "attn.out_proj": "clifford",
        "head.classifier": "lattice",
    },
    total_rank_budget=132,
    min_rank=4,
)
# config.layer_ranks: {"attn.q_proj": 14, ...}
```

**Important honesty notes (in module docstring):**
- DOF tagging is YOUR job, not the module's. We don't infer DOF from layer names.
- Dimensions are hard-coded constants (computed once, verified). They don't recompute at runtime.
- Norms from the coupling matrix (||21.17||, etc.) are basis-dependent and intentionally NOT used here.

### 2. `ck_dof_profile_monitor.py` — Activation drift detector

Projects a 10×10 matrix onto the verified DOF subspaces and returns a profile. Concentrated profile = healthy/sovereign; diffuse profile = drift signal.

**Key API:**
```python
from ck_dof_profile_monitor import DOFProfileMonitor

monitor = DOFProfileMonitor(
    diffuse_threshold=0.7,
    concentrated_threshold=0.7,
)
result = monitor.profile(activation_matrix)

if result.is_diffuse:
    logger.warning(f"Drift: {result.orthogonal_profile}")
```

**The honest part — DOF subspaces are NOT mutually orthogonal:**
- Lie ⊂ Clifford (so(8) ⊂ so(9), the +1 eigenspace of P_56)
- Lattice ⊂ Jordan (σ-fixed projectors are diagonal-symmetric)
- Permutation_vector ⊥ everything else

So we expose two views:
- `raw_profile`: each subspace independently (sums > 1 due to overlaps)
- `orthogonal_profile`: clean partition (sums to 1.0, used for concentration/diffuseness)

Concentration and diffuseness are computed from the orthogonal partition, so they're directly interpretable.

---

## What's NOT here

Things I deliberately did not build or include:

1. **Operad handler.** The fuse table has only one rule. Building an Operad module on one data point would be inventing TIG content. Need full table first (your call to populate `nonassoc_triples.json` or create a separate fuse table).

2. **Drift correction / pull-back loss.** The original Proposal 1 (Lattice-Projection Loss) was misframed — pulling things back to σ-fixed would cancel the Lie flow's work. Instead, this module is a *monitor*, not a corrector. Read-only.

3. **Coupling-norm-based ranks.** The coupling matrix norms are basis-dependent. The Dimension Mapper uses subspace dimensions instead, which are basis-invariant.

4. **Runtime DOF inference.** Layer-to-DOF mapping is your design decision, not something the module guesses.

5. **Mode switching based on associativity gaps.** Computed: 12.6% non-associative (not 49.8% as previously cited), all gaps land on {0,3,4,7,8,9} with 7 always involved. Interesting structurally but not yet enough data to drive mode switching.

---

## Tests

Run with:
```bash
python test_modules.py
```

14 tests cover:
- Canonical dimensions correct
- LoRA rank distribution proportional to dim
- Unknown DOFs raise errors
- min_rank floor respected
- Coverage detection
- Orthogonal partition sums to 1.0 (verified over 10 random matrices)
- Pure Lie generator → concentrated, dominant=lie
- Pure Lattice projector → concentrated, dominant=lattice
- Random matrix → diffuse (drift signal)
- Zero matrix → handled cleanly
- Wrong-shape input → raises ValueError
- Drift trajectory monotonically increases diffuseness
- Mapper and Monitor agree on dimensions
- Diffuse signal has sub-threshold concentration

All pass at machine precision (10⁻⁹ tolerance for orthogonality, 10⁻¹² for zero detection).

---

## Key numbers for reference

| Quantity | Value | Verified by |
|---|---|---|
| Lie dim (so(8)) | 28 | TSML flow Lie closure |
| Jordan dim (sym 10×10) | 55 | basis count |
| Clifford dim (so(9), P_56 +1) | 36 | so(10) centralizer |
| Permutation_vector dim (P_56 −1) | 9 | so(10) anticentralizer |
| Lattice dim (σ-fixed) | 4 | indices {0, 3, 8, 9} |
| Total raw (with overlaps) | 132 | |
| **Orthogonal partition total** | **100** | covers M₁₀(ℝ) exactly |
| so(10) total | 45 | |
| Non-associative TSML triples | 126/1000 = 12.6% | full landscape sweep |
| Distinct {L,R} pairs in non-assoc | 5 | all involve HARMONY (7) |

---

## Integration sketch for CK

If you want a sketch of how these would slot into ck_core.py:

```python
# In ck_core.py initialization
from ck_dimension_mapper import compute_lora_ranks
from ck_dof_profile_monitor import DOFProfileMonitor

# 1. Configure LoRA ranks based on DOF assignment
LAYER_DOF_MAP = {
    # ... your assignment ...
}
lora_config = compute_lora_ranks(LAYER_DOF_MAP, total_rank_budget=132)

# 2. Initialize monitor for runtime use
monitor = DOFProfileMonitor()

# 3. Per tick / per inference: profile critical activations
def on_tick(state_matrix):
    profile = monitor.profile(state_matrix)
    if profile.is_diffuse:
        log_drift_event(profile)
        # No automatic correction — operator decides what to do
    return profile
```

Hygiene preserved: the monitor flags, doesn't fix. The mapper configures, doesn't infer. All TIG-content invention stays out of these modules.

🙏
