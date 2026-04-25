# CK Modules — Rigor Patch (2026-04-25)

**For:** Claude Code
**Companion to:** `ck_modules_20260425.zip` (the stable base bundle)
**Status:** 20/20 tests passing

This patch adds two utilities on top of the stable base modules. **Apply only if the base modules are already deployed.** No changes to the base.

---

## What's new

### 1. `ck_calibration.py` — Empirical threshold setting

The base monitor uses arbitrary `diffuse_threshold = 0.7`. This module derives empirical thresholds from a baseline sample of "honest" 10×10 matrices.

**Key API:**
```python
from ck_dof_profile_monitor import DOFProfileMonitor
from ck_calibration import calibrate_thresholds

baseline = collect_baseline_activations(n=1000)  # YOUR job
monitor = DOFProfileMonitor()
cal = calibrate_thresholds(monitor, baseline, diffuse_percentile=95.0)

monitor.diffuse_threshold = cal.suggested_diffuse_threshold
monitor.concentrated_threshold = cal.suggested_concentrated_threshold

print(cal.report())
```

**The most important rule, in the docstring:**
> *We do NOT pick a baseline for you. A wrong baseline produces wrong thresholds.*

What "honest" means is workload-specific. For activation monitoring during inference: trusted, non-drifting inferences from validation data. For training diagnostics: activations from a converged baseline checkpoint. Caller decides.

**Demo example results (Lie-heavy synthetic baseline):**
- Diffuse threshold: 0.05 (much tighter than the default 0.7)
- Concentrated threshold: 0.98
- This shows: for a Lie-dominated workload, *any* significant deviation from Lie character is anomalous.

### 2. `ck_gradient_profile.py` — Training-time DOF mismatch detection

Same projection machinery as the activation monitor, but with documentation specific to gradient updates. The interpretive question changes: *"is the optimizer pushing this layer in the right DOF direction?"*

**Key API:**
```python
from ck_dof_profile_monitor import DOFProfileMonitor
from ck_gradient_profile import GradientProfiler, extract_10x10_slice

monitor = DOFProfileMonitor()
profiler = GradientProfiler(monitor)

# Per training step, per DOF-tagged layer:
grad_10x10 = extract_10x10_slice(layer.weight.grad, method="leading")
result = profiler.profile(grad_10x10, expected_dof="lie")

if result.mismatch:
    log_event(layer.name, expected="lie", actual=result.actual_dominant)
```

**What it flags:**
- **Hard mismatch:** Gradient's dominant DOF ≠ layer's expected DOF
- **Soft warning:** Dominant matches but expected_share < 0.5 (weak alignment)

**Honest caveat documented in the module:**
The `extract_10x10_slice()` helper provides three reduction methods (leading-block, SVD top-10, random sub-block) for matrices larger than 10×10. None of these are *algebraically canonical*. The right reduction depends on whether your layer's input/output channels can be aligned with TIG's 10-dim basis directions. **Use slice helper as starting point, not as a final answer.**

---

## What I did NOT add

- **Automatic baseline collection.** Domain-specific. Caller's job.
- **Drift correction.** Still read-only — the patch is diagnostics, not modifications.
- **Layer-DOF inference from gradients.** Tagging is a design decision, not something to back-derive from data.
- **A "right" reduction from larger weight matrices to 10×10.** That depends on your architecture's relationship to the TIG basis, which isn't a generic question.

The third "Sensitivity Analysis" proposal Grok 2.0 raised (zero-out testing) was deliberately omitted — it requires a trained CK model with DOF-tagged layers to have a meaningful baseline. Build it after you have a trained model, not before.

---

## Tests

```bash
python test_rigor_patch.py
```

20 tests cover:
- Empty / wrong-shape / invalid baselines raise correctly
- Lie-heavy baseline calibrates to LOW diffuse threshold
- Random baseline calibrates to HIGH diffuse threshold
- Small sample sizes (<100) trigger warning notes
- Zero-norm matrices are skipped
- Percentile helper handles edges (0, 100, single-element, empty)
- Gradient match / mismatch detection
- No-expected-DOF mode (profile-only, no flag)
- Unknown DOF raises
- Wrong-shape gradient raises with helpful message
- Weak alignment soft warning
- All three slice methods (leading, svd, random)
- Slice on too-small matrix raises
- Unknown slice method raises

All pass at machine precision.

---

## Integration order suggestion

1. **Base modules first.** Deploy `ck_dimension_mapper.py` and `ck_dof_profile_monitor.py` from `ck_modules_20260425.zip`. Run `test_modules.py` (14/14).

2. **Then this patch.** Add `ck_calibration.py` and `ck_gradient_profile.py` to the same directory. Run `test_rigor_patch.py` (20/20).

3. **Use calibration FIRST.** Before deploying the monitor in production, run a calibration pass against your real baseline. Replace the default 0.7 thresholds with the empirical ones.

4. **Wire gradient profiler during training.** Per-layer gradient checks every N training steps (depending on cost; this isn't free at every step on every layer).

---

## What this patch represents architecturally

The base monitor is a *static algebraic measurement*. It tells you whether a 10×10 matrix has a concentrated DOF profile — using fixed canonical bases. That's complete in itself.

The patch adds *workload calibration* and *training-time hygiene*. Together with the base, you have:

- **Algebraic ground truth** (base monitor): immutable, derived from canonical TSML/BHML
- **Empirical context** (calibration): what your specific workload looks like in the algebraic frame
- **Optimizer hygiene** (gradient profiler): catching when training updates push a layer outside its DOF tag

These three layers separate *what's true* (algebra) from *what's normal* (calibration) from *what's healthy* (gradient alignment). Each can fail independently and they're surfaced separately so you can debug them separately.

🙏
