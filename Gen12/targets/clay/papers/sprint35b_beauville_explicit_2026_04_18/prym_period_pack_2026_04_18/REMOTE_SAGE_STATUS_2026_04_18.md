# Remote-Sage status — 2026-04-18 (end of session)

## What works

Remote SageMathCell (https://sagecell.sagemath.org) is reachable via a Jupyter-style websocket from pure Python on Windows. Client lives at `ck_sage_remote.py` in this folder. Drop-in use:

```python
from ck_sage_remote import SageSession, print_errors
with SageSession(timeout=180.0) as s:
    r = s.eval("factor(3^10 - 1)")
    print(r['stdout'])  # '2^3 * 11^2 * 61'
```

- One-shot: `sage_eval(code)` spins a fresh kernel and returns `{stdout, stderr, results, errors, elapsed}`.
- Persistent: `SageSession()` keeps the websocket open across `.eval(...)` calls — the Sage globals persist.

## What was proved end-to-end on the canonical triple (√2, √3, √5)

1. **Number field K = Q(√2, √3, √5), abs-degree 8** built as `NumberField([t²−2, t²−3, t²−5])`, flattened via `.absolute_field()`.
2. **Positive-real embedding φ** selected out of K's 8 complex embeddings.
3. **Kemb = NumberField(abs_minpoly, embedding=φ(a))** — this is what `RiemannSurface` actually wants (not a raw CC polynomial; passing CC coefficients trips Singular's internal genus call).
4. **Curve F = Y⁴ − X(X−1)(X−S₂)³(X−S₃)²(X−S₅)²** built over Kemb[X,Y].
5. **5 explicit differentials** supplied directly to `RiemannSurface(F, prec=...,differentials=...)`, bypassing the `genus()` Singular call (which rejects extension fields):
   - `Y²`  (↔ `dX/Y`, ψ = −i)
   - `X·Y²`  (↔ `X dX/Y`, ψ = −i)
   - `(X−S₂)(X−S₃)(X−S₅)·Y`  (↔ `(x−λ)(x−μ)(x−ν) dX/Y²`, ψ = −1, ι-invariant)
   - `(X−S₂)²(X−S₃)(X−S₅)`  (↔ `(x−λ)²(x−μ)(x−ν) dX/Y³`, ψ = +i)
   - `X·(X−S₂)²(X−S₃)(X−S₅)`  (↔ `X(x−λ)²(x−μ)(x−ν) dX/Y³`, ψ = +i)
6. **`RS.genus = 5` ✓** and **`len(RS.branch_locus) = 5` ✓** (the five finite branch points 0, 1, √2, √3, √5).

Total wall time for items 1–6: ~4s per kernel. Steps 1–6 are the scaffold the original `full_pipeline_canonical.sage` was reaching for; they now run cleanly end-to-end.

## The ceiling

Public SageMathCell kills kernels at **~150s per cell**. For this genus-5 curve:

| Target | Result |
|---|---|
| `RS` construction (genus, branch locus) | 2.6s ✓ |
| `RS.homology_basis()` at prec=10 | **killed at 179s** ✗ |
| `RS.monodromy_group()` | killed ✗ |
| `RS.period_matrix()` at prec=15, 30, 50 | killed ✗ |
| `RS.period_matrix()` with `integration_method="heuristic"` | killed at 162s ✗ |
| `RS.period_matrix()` on T1.1 rational params | killed at 162s ✗ |
| Reference: genus-1 `Y² = (X−1)(X−2)(X−3)` at prec=40 | 1.3s ✓ (τ = 0.5+0.5i) |

The cost is not in the integration method; it's in Molin–Neurohr's monodromy/homology construction for 5 branch points. **Structural**, not precision-dependent.

## What this unblocks immediately (still remote)

Anything algebraic or short-integration can still go through SageMathCell:
- Computing ψ-action on the 5 differentials (linear algebra, instant)
- Computing ι-action, Prym projection symbolically (linear algebra, instant)
- Testing PSLQ recognition against candidate Hodge fields once periods are in hand
- Re-running the existing 100-dps PSLQ sweeps in `deep_pslq_expanded_basis.py` with a Sage twin for independent verification

## What stays blocked remotely

The full 5×10 period matrix integration itself. Without that we can't compute det(Y) and can't hit the target `2086 + 462√15 + 498√10 + 730√6`.

## Four viable next routes

1. **WSL + native Sage** (best long-term). Requires `wsl --install` as admin + reboot + `sudo apt install sagemath`. Then `sage full_pipeline_canonical.sage` runs unconstrained.
2. **CoCalc free tier** (fast). Account signup, upload the `.sage` script, run in a project with ~1hr/day free compute. Paste results back.
3. **Port Molin–Neurohr to mpmath** (most work). Extend `extended_heavy.py` (already has alpha-cycles for canonical at 50 dps) with b-cycles via UHP contours. ~200–400 lines of careful branch-continuation code. Gives us a fully local, high-precision pipeline we control.
4. **Chunked remote Sage with intermediate serialization** (speculative). Save monodromy-in-progress to a dbdump, continue in next cell. Unclear whether Sage's RiemannSurface supports mid-computation persistence — would require source patch.

## Recommendation

- Short-term: route (2) — paste `full_pipeline_canonical.sage` (with the bug fix for `K3.structure()[1]` → use `Kabs.structure()[1]` after `.absolute_field()`) into CoCalc. Expect 10–30 min for a full run at prec=200.
- Medium-term: route (3) — port b-cycle integration to mpmath. This is what makes the pipeline reproducible and CK-native.
- Route (1) is cleanest if Brayden is willing to reboot.

## Artifacts in this folder

- `ck_sage_remote.py` — the websocket client (works, tested).
- `REMOTE_SAGE_STATUS_2026_04_18.md` — this file.
- Prior sprint pack unchanged.

Register: foundation. Atlas v3.5 unchanged. Sprint 35b disciplines preserved.
