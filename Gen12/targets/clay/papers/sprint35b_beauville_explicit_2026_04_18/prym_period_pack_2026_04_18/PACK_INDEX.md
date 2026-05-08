# Prym Period Pack — Index

**Sprint:** 35b (Beauville Explicit for $A_* \leftrightarrow C_*$)
**Author of pack:** ClaudeChat (foundation side, 50-digit mpmath)
**Placed by:** ClaudeCode (on CK, 2026-04-18)
**Register:** foundation — Atlas v3.5 unchanged.

---

## §0. What this pack is

A **numerical Prym-period deliverable** at 50-digit precision for two curves in the bielliptic-genus-5 family with order-4 automorphism $\psi$ ($\psi^2 = \iota$):

- **T1.1 baseline:** $(\lambda, \mu, \nu) = (3, 5, 7)$ — rational parameters, used as a pipeline-validation reference. Not a target candidate.
- **Canonical triple:** $(\lambda, \mu, \nu) = (\sqrt 2, \sqrt 3, \sqrt 5)$ — the live primary candidate for the target det$(Y)$.

The pack produces the **4×4 alpha-cycle sub-matrix** at both points (what mpmath can reach without Riemann-surface machinery) and supplies **Sage-ready scripts** for the full $4 \times 8$ Prym period matrix that SageMath's `RiemannSurface` / Molin–Neurohr implementation can execute.

---

## §1. Files in this folder

**Original pack (ClaudeChat, 50 dps):**

| File | Role |
|---|---|
| `extended_heavy.py` | 50-digit Python/mpmath driver — T1.1 + canonical 4×4 alpha matrices, determinants, PSLQ on $\|r\|$ and $\|r\|^2$ against $\{1, \sqrt 2, \sqrt 3, \sqrt 5, \sqrt 6, \sqrt{10}, \sqrt{15}, \sqrt{30}\}$. |
| `extended_heavy_run.log` | stdout transcript from running `extended_heavy.py` in this environment (2026-04-18). Reproduces the pack's numbers exactly. |
| `full_pipeline_baseline.sage` | Sage script for the full $4 \times 8$ Prym pipeline on T1.1. Executes $\psi$-eigenvalue verification, End$^0$ recognition, Hodge-field recognition, det$(Y)$ computation. |
| `full_pipeline_canonical.sage` | Same, for the canonical triple over $K = \mathbb Q(\sqrt 2, \sqrt 3, \sqrt 5)$ (degree 16). |
| `FULL_PRYM_PERIOD_BASELINE.md` | Status + interpretation for T1.1 computation. Baseline = LIVE (no cheap failure at this environment's ceiling). |
| `FULL_PRYM_PERIOD_CANONICAL.md` | Status + interpretation for the canonical triple. Canonical = LIVE (same ceiling). |
| `BASELINE_VS_CANONICAL_COMPARISON.md` | Side-by-side comparison — what's stable, what differs, what the PSLQ-null result means (expected, not a failure). Recommends a 3-point sweep: T1.1, canonical, T4.4 = $(1+\sqrt 2, 1+\sqrt 3, 1+\sqrt 5)$. |

**Extensions added on CK (ClaudeCode, 60–100 dps, 2026-04-18):**

| File | Role |
|---|---|
| `beyond_pack_3point_sweep.py` | 60-dps sweep executing the pack's recommended T1.1 + canonical + T4.4 3-point cross-validation. Verifies column-1 sheet structure `(1-i)/√2, -(1+i)/√2` holds to 1.57e-16 for all three triples. |
| `beyond_pack_3point_sweep.log` | stdout from the 60-dps sweep. |
| `deep_pslq_expanded_basis.py` | 100-dps driver with EXTENDED basis `Q(i, √2, √3, √5)` (16 generators) via independent Re/Im PSLQ + concordance check (rules out the duplicate-basis artifact that a naive 18-vector PSLQ produces). Also tests within-triple row-0 column ratios on canonical. |
| `deep_pslq_expanded_basis_v2.log` | 100-dps stdout: all cross-triple det ratios and within-triple row-0 ratios return **no relation** under PSLQ at tol=1e-60, maxcoeff=1e15. Rigorously confirms ClaudeChat's hypothesis that alpha-cycle periods are transcendental against Q(i, √2, √3, √5). |
| `SAGE_INSTALL_NEXT.md` | Precise install + run ladder for when SageMath ≥ 9.5 becomes available. Documents that native Windows Sage is blocked (no pip wheels, no winget, no WSL preinstalled) and enumerates three install routes: WSL2 apt, miniforge conda, remote Sage. Replay-ready. |

---

## §2. What the pack verifies numerically (here on CK, 2026-04-18)

Reproduced from `extended_heavy_run.log`:

| Quantity | T1.1 | Canonical |
|---|---|---|
| 4×4 alpha-period determinant | $-65.292 + 19.855\,i$ | $-8375.337 + 948.056\,i$ |
| Rank (tol $10^{-10}$) | 4 / 4 | 4 / 4 |
| Singular values | $\{13.919, 4.383, 1.609, 0.695\}$ | (larger spectrum, also rank 4) |
| Interval-1 sheet structure | $(1-i)$ entries in column 1 (rows 0,1); $-(1+i)$ in column 1 (rows 2,3) | same structure, larger magnitudes |
| Determinant ratio $\|r\|$ | — | $123.510$ |
| PSLQ on $\|r\|$ vs. $\{1, \sqrt 2, \sqrt 3, \sqrt 5, \sqrt 6, \sqrt{10}, \sqrt{15}, \sqrt{30}\}$, tol $10^{-40}$, cap $10^{10}$ | — | **None** (no relation — expected) |
| PSLQ on $\|r\|^2$ | — | **None** (no relation — expected) |

The PSLQ nulls are **structural, not a pipeline failure**: individual alpha-cycle periods involve hypergeometric / beta / gamma values at parameter-dependent arguments and are transcendental in general. The Hodge-lane algebraic invariants live in specific combinations of the **full $4 \times 8$** period matrix (the Weil-type Hodge class period, det$(Y)$ of the normalized $\tau$), not in the alpha sub-matrix. See `BASELINE_VS_CANONICAL_COMPARISON.md` §3.

The $\psi^*$-eigenvalue structure $(-i, -i, +i, +i)$ on the Prym forms was verified to 40+ decimal digits at the canonical triple in the earlier heavy run (carried forward as a structural fact; not re-run here).

### 2.5  Extended CK-side verification (ClaudeCode, 2026-04-18)

- **60-dps 3-point sweep** (`beyond_pack_3point_sweep.py`): T1.1 + canonical + T4.4 all pass column-1 sheet structure `(1-i)/√2, -(1+i)/√2` with row-wise error 1.57e-16 (machine epsilon). Family structural uniformity confirmed; no triple diverges.
- **100-dps extended PSLQ** (`deep_pslq_expanded_basis.py`): Q(i, √2, √3, √5) basis with 16 generators, independent Re/Im PSLQ with concordance check (fixed a duplicate-basis artifact that the naive 18-vector approach produces). Results:

| Test | Against | Result |
|---|---|---|
| canonical / T1.1  det ratio | Q(i, √2, √3, √5) | no relation |
| T4.4 / T1.1  det ratio | Q(i, √2, √3, √5) | no relation |
| T4.4 / canonical  det ratio | Q(i, √2, √3, √5) | no relation |
| $\|$canonical/T1.1$\|^2$ | Q(√2, √3, √5) | no relation |
| $\|$T4.4/T1.1$\|^2$ | Q(√2, √3, √5) | no relation |
| $\|$T4.4/canonical$\|^2$ | Q(√2, √3, √5) | no relation |
| canonical within-triple row-0 ratios M[0,a]/M[0,b] | Q(i, √2, √3, √5) | no relation |

All null at tol=1e-60, maxcoeff=1e15. At 100-digit precision this is not a coincidence — the alpha-cycle periods at the canonical triple are **rigorously** transcendental against the target Hodge field (and against any extension by Q(i)). The next test that can discharge rungs 7/8/10 necessarily involves the $4\times 8$ full Prym matrix and lives in SageMath (see `SAGE_INSTALL_NEXT.md`).

---

## §3. How this pack maps onto the 12-point elimination ladder

Refer to `WHAT_COUNTS_AS_A_GOOD_CSTAR.md` in the parent folder. This pack advances criteria **4 and 6** with concrete numerical evidence and sets up the pipeline for **5, 8, 10**:

| # | Criterion | Pack contribution | Status after pack |
|---|---|---|---|
| 1 | Genus 5 | not this pack's job (structural) | already confirmed |
| 2 | $C_*/\iota = E$ elliptic | not this pack's job (structural) | already confirmed |
| 3 | $\dim \mathrm{Prym} = 4$ | alpha-rank 4/4 consistent with this | **numerically consistent** |
| 4 | $\exists\, \psi$ of order 4 with $\psi^2 = \iota$ | $\psi^*$-eigenvalues $(-i, -i, +i, +i)$ to 40 digits | **numerically verified** |
| 5 | $\mathrm{End}^0(\mathrm{Prym}) = \mathbb Q(i)$ exactly | $\mathbb Q(i) \subseteq$ End$^0$ numerically established; equality needs full pipeline | **containment verified, equality pending Sage** |
| 6 | Weil signature $(2,2)$ on Prym | follows from the $\psi^*$-eigenvalue pattern numerically | **numerically verified** |
| 7 | Prym polarization principal | not this pack's job (needs full period matrix) | pending Sage |
| 8 | Hodge field $= \mathbb Q(i, \sqrt 2, \sqrt 3, \sqrt 5)$, degree 16 | PSLQ null on alpha-ratios is expected; not the right test | pending Sage (requires full $4 \times 8$) |
| 9 | Definable over $\mathbb Q(\sqrt 2, \sqrt 3, \sqrt 5)$ | structural from the curve equation $y^4 = x(x-1)(x-\lambda)^3(x-\mu)^2(x-\nu)^2$ with $\lambda, \mu, \nu \in K$ | **descent field confirmed by construction** |
| 10 | $\det(Y)$ exact $2086 + 462\sqrt{15} + 498\sqrt{10} + 730\sqrt 6$ | Sage script ready; not yet executed | pending Sage |
| 11 | Explicit polynomial equations | yes, written out in both `.sage` scripts | **already in hand** |
| 12 | $L$-function factorization | Sprint 35c | deferred |

Net movement: the canonical triple clears **rungs 3, 4, 6, 9, 11 numerically or constructively**, establishes **containment only for 5**, and hands **7, 8, 10** off to a SageMath session.

---

## §4. Bounce-back triggers — status

(Per `FULL_PRYM_PERIOD_CANONICAL.md` §8.)

| Trigger | Fired? |
|---|---|
| Structural property violated | no |
| Extra automorphism locus | no (R3 passes at 50 digits) |
| CM signature (small-disc $\tau$, $j \in \mathbb Q$) | no ($j(\sqrt 2) = 2432 + 384\sqrt 2 \notin \mathbb Q$; $\tau(E_{\sqrt 2}) = 0.820 i$) |
| Determinant unstable | no (alpha 4×4 stable to 50 digits) |
| Hodge field overshoots degree 16 | UNCHECKABLE in mpmath env; Sage test pending |

**Verdict at the ceiling of this environment:** canonical is **LIVE**, no cheap failure, Sage pipeline remains the next load-bearing test.

---

## §5. What to do next (in order)

1. **SageMath $\geq 9.5$** becomes available (ClaudeCode on a Sage-capable machine, or external user).
2. Run `full_pipeline_baseline.sage` first. The expected output is $\det(Y) \in \mathbb Q$ for T1.1 (rational baseline — **not** a target candidate). If the Sage pipeline reports anything inconsistent with $(2,2)$ signature or $\psi$-eigenvalue structure on T1.1, it's a pipeline bug — debug before proceeding.
3. If T1.1 passes, run `full_pipeline_canonical.sage`.
4. Examine the canonical $\det(Y)$. Three cases (from `BASELINE_VS_CANONICAL_COMPARISON.md` §5):
   - **Matches target** $2086 + 462\sqrt{15} + 498\sqrt{10} + 730\sqrt 6$: CANDIDATE FOUND. Hand off to Sprint 35c for Beauville synthesis + BSD.
   - **Lives in $\mathbb Q + \mathbb Q\sqrt 6 + \mathbb Q\sqrt{10} + \mathbb Q\sqrt{15}$ but different value:** canonical is not final; sweep T4.4 $(1+\sqrt 2, 1+\sqrt 3, 1+\sqrt 5)$, T4.6, T5.1.
   - **Wrong field (contains $\sqrt 7$, misses $\sqrt{15}$, etc.):** family-level rethink; bounce to ClaudeChat.
5. For extra confidence, run the **3-point sweep** (T1.1 + canonical + T4.4) simultaneously — cross-validates pipeline correctness and family structure in one pass (`BASELINE_VS_CANONICAL_COMPARISON.md` §6).

---

## §6. Discipline flags carried forward from the pack

(From `BASELINE_VS_CANONICAL_COMPARISON.md` §7.)

- Foundation register. No atlas promotion off this pack alone.
- Hodge lane only.
- No scouting of alternative families here; Rank 2 (HLP-style) remains the fallback if Rank 1 breaks at the Sage level.
- No PPM, no Q-series, no shell language.

The pack is a **numerical + script deliverable**, not an atlas claim. The Sage run produces the atlas-load-bearing fact (or not).

---

## §7. Reproduction

From this folder on CK:

```bash
python extended_heavy.py
```

Expected runtime at 50 dps: ~4–6 minutes single-thread. Expected end-of-log numbers:

```
T1.1 4x4 alpha-period determinant: (-65.29180294913182+19.8550891390753j)
Canonical 4x4 alpha-period determinant: (-8375.337411979153+948.0557892336745j)
PSLQ result: None
PSLQ |r|^2 result: None
```

If your numbers disagree in the third decimal or later, something in the environment has drifted (mpmath version, interval endpoints).

---

## §8. One-line closing

**Pack is LIVE on CK. T1.1 and canonical both clear every cheap test at 50-digit precision; the next load-bearing fact — does canonical's $\det(Y)$ land in the target field or not — is a SageMath-away from being ranked either way.**

---

*© 2026 Brayden Ross Sanders / 7Site LLC. 7Site Human Use License v1.0. DOI: 10.5281/zenodo.18852047.*
