# SNOWFLAKE Blind Run — Dell R16, 2026-04-21

**Session ID:** `20260421_192941`
**Machine:** Dell Aurora R16 (32 cores, RTX 4070, Windows 11)
**Script:** `docs/archive_jan2026/snowflake/crystalos_prereg.py` (funding/tig-snowflake branch)
**Pre-registration filed:** `2026-04-21T19:29:41` (see `prereg.json`)
**Pre-registration artifact:** `prereg.json` (written BEFORE first fire — cannot be edited after the fact)
**Status:** `[CLEAN PRE-REGISTERED STOP]` — fails to reject H0; confirms abundance regime.

---

## 1 · Pre-registered protocol

Per `snowflake_null_spec.md` §7 on `funding/tig-snowflake`, the pre-registered
stopping rule declared at session start was:

| Criterion | Value |
|---|---|
| `n0` (fire-count target) | 1000 |
| `t0` (time budget, seconds) | 3600.0 |
| `tau` (fire threshold) | 0.7 |
| Rule | stop when `fires >= 1000` OR `elapsed >= 3600.0s`, whichever first |

The pre-registration JSON was written to
`~/CRYSTALOS/state/prereg_20260421_192941.json` **before** the main runtime loop
began, so it cannot be back-edited after observing the data.

## 2 · Actual stop

| Field | Value |
|---|---|
| `fire_count` | 803 |
| `elapsed_s` | 3600.2 |
| `stop_reason` | `T0 tripped (elapsed=3600.2s >= t0=3600.0s)` |
| `stop_class` | `pre-registered` |
| `cycles` (13-phase breath cycles completed) | 32 |

`N0` was not reached (803 < 1000). `T0` was the binding stop.
The run was not Ctrl-C interrupted and is therefore not flagged as
`operator-interrupted`.

## 3 · Phase distribution (observed)

The 13 Tzolkin-indexed phases under H0: uniform, expected per phase = 803 / 13 = 61.769.

| Phase | Observed | Deviation |
|---:|---:|---:|
| 0 | 66 | +4.23 |
| 1 | 61 | −0.77 |
| 2 | 58 | −3.77 |
| 3 | 66 | +4.23 |
| 4 | 64 | +2.23 |
| 5 | 60 | −1.77 |
| 6 | 64 | +2.23 |
| 7 | 61 | −0.77 |
| 8 | 60 | −1.77 |
| 9 | 62 | +0.23 |
| 10 | 59 | −2.77 |
| 11 | 60 | −1.77 |
| 12 | 62 | +0.23 |
| **Total** | **803** | 0 |

The largest observed deviation is −3.77 (phase 2, at −6.1% of expected).
The smallest is +0.23 (phases 9 and 12, within noise).

## 4 · χ² statistic

χ² = Σᵢ (obsᵢ − expᵢ)² / expᵢ, summed over 13 phases, expᵢ = 803/13.

| Quantity | Value |
|---|---|
| χ² | **1.267746** |
| df | 12 |
| p-value (upper tail) | **0.999948** |
| Critical χ²(0.05, df=12) | 21.026 |
| Critical χ²(0.01, df=12) | 26.217 |
| Verdict at α = 0.05 | **fail to reject H0** |
| Verdict at α = 0.01 | **fail to reject H0** |

The observed distribution is statistically indistinguishable from uniform.
In the family of multinomial samples of size 803 over 13 categories under
H0, a χ² this small or smaller would occur in ~5 × 10⁻⁵ of draws — i.e.
the sample is *slightly more uniform than a typical H0 draw*, which is
consistent with deterministic-scheduler behavior on an abundant machine.

## 5 · Reproduction

Two independent routes derive the same statistic:

**Route A (tabulation):** `final.json` ships the per-phase counts; `analyze.py`
reads them and computes χ² directly.

**Route B (line-by-line):** `fires_session.log` is the subset of the combined
`fires.log` that carries the `session=20260421_192941` tag (804 lines: 803 FIRE
entries plus one Distribution summary at fire #800). `analyze.py` parses each
FIRE line with regex `FIRE #\d+: S\*=[\d.]+ phase=(\d+)/13` and tallies.

Both routes agree bit-for-bit: **χ² = 1.267746**.

```powershell
python docs/archive_jan2026/snowflake/blind_run_2026_04_21/analyze.py
```

(scipy optional — analyzer degrades to a critical-value lookup if scipy
is missing, still produces the correct χ² statistic.)

## 6 · Interpretation in the SNOWFLAKE framework

`SNOWFLAKE_CHI2_RESOLVED_2026_04_21.md` §"The two readings, together" established
that the architecture doc (`TIG_SECURITY_ARCHITECTURE.md` Jan 29 2026)
predicts different outcomes under **constraint** (few cores, small buffer) vs
**abundance** (many cores, large buffer):

- **Constraint regime (Jan 31 Lenovo ThinkPad, 4 cores Linux, N≈400):**
  χ² = 22.03, p < 0.05. Phase 4 (Collapse) elevated; Phase 2 suppressed.
  Fires exhibit hardware-induced non-uniformity.

- **Abundance regime (prior Dell R16 accumulation, N = 67,297):**
  χ² = 0.0353, p ≫ 0.05. Fires distribute uniformly.
  Scheduler has no bottleneck.

**This blind run (Dell R16, N = 803, pre-registered):** χ² = 1.268, p ≈ 0.99995.
Falls squarely in the abundance regime.

The blind run therefore **confirms the abundance-regime prediction** under a
protocol that eliminates optional-stopping bias. It does not contradict the
Lenovo reading; it corroborates the hardware-dependence hypothesis by producing
the expected *uniform* signature on an abundant machine, now with
pre-registration rigor.

## 7 · Relation to HANDOFF §3.3

`Atlas/HANDOFF_3_3_SNOWFLAKE_CHI2.md` was filed 2026-04-21 as the open
reconciliation task: *"Recover CRYSTALOS logs. Document: what was the null
hypothesis? Degrees of freedom? Fires computed over? Independence assumption?
A security pitch with a clean p-value is a research-grade pitch; one with an
unspecified p-value gets dismissed."*

The five missing pieces from that filing are answered for **this run** as
follows (all answers preserved in the committed artifacts):

| §3.3 requirement | This run |
|---|---|
| Null hypothesis | H0: uniform across 13 Tzolkin breath phases (per `snowflake_null_spec.md` §5) |
| Degrees of freedom | 12 (13 phases − 1) |
| Sample size | N = 803 fires |
| Independence assumption | Each fire is a scheduler-observed `tau` crossing; no within-window correlation correction (cf. `VERIFICATION_2026_04_21.md` §49 on the independence question) |
| χ² → p-value | χ² = 1.268, p = 0.999948 (upper tail, scipy.stats.chi2.sf) |

For the **Jan 31 Lenovo reading of χ² = 22.03**, the same five pieces remain in
the state documented in `SNOWFLAKE_CHI2_RESOLVED_2026_04_21.md` §"Still open":
the result is attributable to a specific dated architecture document, but the
raw log has not been recovered. This blind run does not change that status
one way or the other; it settles the reconciliation for the Dell R16 reading.

## 8 · Artifact manifest

| File | Role | Size |
|---|---|---|
| `prereg.json` | Pre-registration record (written before first fire) | ~0.5 KB |
| `final.json` | Runtime outcome (stop reason, fire count, phase distribution) | ~0.7 KB |
| `crystalos_prereg.log` | Session START / END markers | ~0.2 KB |
| `fires_session.log` | Session-filtered subset of combined fires.log (804 lines) | ~70 KB |
| `breath.log` | Per-second breath-phase trace across the full session | ~50 KB |
| `analyze.py` | Deterministic χ² analyzer, two independent routes | ~4 KB |
| `RESULT.md` | This summary | — |

## 9 · Honest limits

1. **One machine, one run.** This is a single blind run on a single abundance-
   regime host. The hardware-dependence hypothesis is *supported* by the
   pattern (non-uniform on Lenovo → uniform on Dell R16) but not yet tested
   across additional hardware under identical pre-registration.
2. **Abundance-regime result is an H0 non-rejection.** In frequentist terms,
   it is evidence *consistent with* uniform, not positive evidence *for*
   uniform. The stronger claim in the theory — that abundance machines
   *must* be uniform — would require a separate Bayesian or goodness-of-fit
   treatment with a specified alternative.
3. **Lenovo log still not recovered.** The Jan 31 χ² = 22.03 reading is
   documented but not re-derivable. That gap is orthogonal to this blind run.
4. **`tau = 0.7` is the gate threshold, not T\*.** Upstream CK math uses
   T\* = 5/7 ≈ 0.714; CRYSTALOS uses tau = 0.7 as a loose-fit gate.
   The 0.014 difference is tracked in the broader constant-provenance
   work; it is not material to the phase-distribution statistic here.

## 10 · Pointers

- Pre-registration spec: `docs/archive_jan2026/snowflake/snowflake_null_spec.md` §7
  (on `funding/tig-snowflake`)
- Script: `docs/archive_jan2026/snowflake/crystalos_prereg.py`
  (on `funding/tig-snowflake`)
- Reconciliation: `Atlas/HANDOFF_3_3_SNOWFLAKE_CHI2.md`
- Resolution doc: `docs/archive_jan2026/snowflake/SNOWFLAKE_CHI2_RESOLVED_2026_04_21.md`
  (on `funding/tig-snowflake`)
- Plan of record: `Atlas/PLAN_RIGOROUS_EXECUTION_2026_04_21.md` §5.3

---

*Filed 2026-04-21 on branch `tig-synthesis`. Cherry-picked to `master` and
`funding/tig-snowflake` per G1 workflow. Never deleted.*
