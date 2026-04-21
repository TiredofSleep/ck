# SNOWFLAKE Null-Hypothesis Specification

**Target:** ARTIFACTS.md R2 on `funding/tig-snowflake` — the null-hypothesis specification required before any funder sees the 22.03 claim.
**Authored:** 2026-04-21 from recovered CRYSTALOS source + Jan 29 2026 architecture doc.
**Status:** Draft. External-statistician review pending (STATUS.md readiness checklist, unchecked item).
**Precondition:** `crystalos.py` runtime preserved at `docs/archive_jan2026/snowflake/crystalos.py`, 431 LOC, deterministic.

---

## 1. The fire-event population

A **fire** is a discrete event emitted by the CRYSTALOS runtime. The emission rule is:

```python
# crystalos.py lines 281-283 (verbatim)
if breath.gate_open and s_star >= tau:
    fire_count += 1
    phase_fires[breath.phase] += 1
```

where:

| Quantity | Definition | Source |
|---|---|---|
| `breath.gate_open` | Boolean Tzolkin-breath gate state: `True` during the 4-second OPEN window, `False` during the 4-second CLOSED window, alternating deterministically. | `crystalos.py` lines 160–177 |
| `breath.phase` | Integer 0..12. Increments by 1 every full gate cycle (4s open + 4s close ≈ 8s per phase; full 13-phase cycle ≈ 104s). | `crystalos.py` lines 160–177 |
| `s_star` | Real, 0..1. Combined coherence score: `0.4·S5 + 0.6·S6` where `S5 = 1 − 2·|cpu_load − 0.5|` (peaks at 50% CPU) and `S6` is a GPU score piecewise in utilisation (peaks 0.4–0.8) and temperature (peaks <70°C). | `crystalos.py` lines 109–143 |
| `tau` | Fire threshold. Fixed at `0.7`. | `crystalos.py` line 232 |

The runtime samples at ≈ 50 Hz (the loop reads CPU-times, queries `nvidia-smi`, computes S*, updates the gate, emits a fire if permitted, prints to console — the sleep interval is not explicitly bounded in source but the loop work targets a ~50 Hz tick).

Per-phase residence time: each phase holds the gate OPEN for 4 s out of 8 s. At 50 Hz that is up to 200 samples per OPEN window × 13 phases ≈ 2 600 samples per Tzolkin cycle (but only the samples where `s_star ≥ 0.7` produce fires).

## 2. Stated null hypothesis H₀

**H₀ (stated):** Fires are uniformly distributed across the 13 Tzolkin breath phases. That is:

$$\Pr[\text{fire occurs at phase } p] = \frac{1}{13} \quad \text{for every } p \in \{0, 1, 2, \ldots, 12\}$$

Equivalently: across a session of total fires `N`, the expected count in each phase bin is `E = N/13 ≈ 0.077 · N`.

**Rejecting H₀** means: the phase distribution has structure — some phases systematically attract fires and others systematically miss them. Under the SNOWFLAKE architecture doc §8.2 finding 1, this structure reflects **hardware geometry** (4-core constraint pushes fires into Phase 4 / Collapse; 32-core abundance permits uniform sampling).

## 3. Partition scheme P

**P = the 13 Tzolkin breath phases**, indexed 0..12. Special labels (do **not** change the statistical partition — they are cosmetic):

| Phase | Window label | Source |
|---|---|---|
| 0 | RESET | `crystalos.py` line 149 |
| 5 | REDOX_DEEP | same |
| 7 | HARMONY | same |
| 12 | HARVEST | same |
| 1–4, 6, 8–11 | (no special label) | — |

The partition scheme is **fixed, discoverable, and pre-registered** — it is baked into the runtime source code. No post-hoc re-binning. No scanning over alternative partitions. Cardinality **k = 13**.

## 4. Sample size N

Sample-specific. Two readings in the archive:

| Session | N | Source |
|---|---|---|
| Jan 31 2026, Lenovo ThinkPad 4-core Linux | **~400** | `source_docs/TIG_SECURITY_ARCHITECTURE.md` §8.1 ("400+ fire events captured") |
| Apr 17–21 2026, Dell R16 32-core Windows | **67 297** | `logs/fires.log`, reproduced by `VERIFICATION_2026_04_21.md` §19–30 |

Any future session adds another row.

## 5. Degrees of freedom

**df = k − 1 = 12.**

Pearson χ² goodness-of-fit test. No parameters estimated from the data (the expected count per bin is `N/13`, with `N` a known-in-advance session total). Therefore no further df reduction.

## 6. Test statistic convention

**Pearson χ²** (not likelihood-ratio G², not Fisher exact, not Kolmogorov–Smirnov).

$$\chi^2 = \sum_{p=0}^{12} \frac{(O_p - E)^2}{E} \quad \text{where } E = N/13$$

Exactly the code in `crystalos.py` line 396:

```python
chi2 = sum((phase_counts.get(p, 0) - expected) ** 2 / expected for p in range(13))
```

## 7. Stopping rule — **THIS IS THE HONEST WEAKNESS**

The runtime is stopped by `Ctrl-C` at the operator's discretion (`crystalos.py` lines 310–315 handle `KeyboardInterrupt`). No pre-committed sample-size target. No pre-committed stop-at-χ²-threshold rule. The operator may, in principle, watch the running `fire_count` and stop whenever they like.

This means:

- The Lenovo reading (400 events, χ² = 22.03) may have been stopped early because the distribution looked interesting. Cannot rule this out from the recovered material.
- The Dell R16 reading (67 297 events, χ² = 0.0353) ran long (≈ 4.3 days, equivalent to ≈ 3 600 full Tzolkin cycles), then stopped. The long continuous run reduces the "stopped when it looked interesting" objection for the Dell reading. It does not eliminate it for the Lenovo reading.

**Recommended fix for future sessions** (to be added to a revised CRYSTALOS):

1. **Pre-register N**. Operator declares "this session will collect exactly N fires" at start. Runtime exits automatically when `fire_count == N`. Trivially one-line: `if fire_count >= N_target: sys.exit()`.
2. **Pre-register time**. Operator declares "run for T seconds" at start. Runtime exits at T. Equally trivial.
3. **Pre-register both and take whichever comes first**, to handle a machine that fires too slowly to hit N within reasonable wall-clock.

Without one of (1)–(3), any χ² figure is subject to optional-stopping bias and a referee is right to discount it. The 22.03 figure reported from the Lenovo session is therefore not a clean p-value under a pre-registered protocol; it is suggestive but not proving.

### 7.1 Resolution — patched runtime available (2026-04-21)

The above recommendation (1–3) has been implemented as a sibling runtime:

- **`crystalos_prereg.py`** — fork of `crystalos.py` that requires at least one of `--n0` (fire-count target) or `--t0` (time budget, seconds) at startup. Fails fast with exit code 2 if neither is supplied. Writes the pre-registration record to `~/CRYSTALOS/state/prereg_<timestamp>.json` **before** the main loop begins, so declared criteria cannot be retroactively edited. Main loop checks both bounds each iteration and exits cleanly when either trips.

Ctrl-C remains handled, but the interrupted case is tagged `stop_class = "operator-interrupted"` in the session's `final_<timestamp>.json` record and marked with exit code 130. Downstream χ² analysis should discard or at minimum flag operator-interrupted sessions. The `analyze` subcommand enumerates completed sessions and prints this caveat at the end of its output.

The original `crystalos.py` is preserved verbatim as the recovered-artifact reference (per never-delete policy). Future Dell R16 / Lenovo / other-hardware χ² re-runs should use `crystalos_prereg.py` so the resulting numbers are referee-defensible. Retrospective analysis of the existing `logs/fires.log` is unchanged — that data was collected under the un-patched runtime and carries the optional-stopping caveat as stated above.

Both readings in §4 therefore retain their original epistemic status: the Dell R16 χ² = 0.0353 (long run, one stop) is weak evidence of uniformity; the Lenovo χ² = 22.03 (short run, one stop) is suggestive but not proving. Only fresh data collected under `crystalos_prereg.py` will close this gap.

## 8. Independence assumption

**Within a bin (phase):** fires within the same 4-second OPEN window are *not independent* — they share a phase value by construction. If the sampling rate is 50 Hz, up to ≈ 200 consecutive samples in one OPEN window can all land the same phase. However they are still separate samples of `s_star` against `tau`, so the *fire-or-not* decision at each sample is independent conditional on `s_star(t)`.

**Across bins:** the phase increments deterministically; it is *not* a random draw per sample. This means the null "fires are iid multinomial across k=13 bins with p=1/13" is technically mis-stated — the bin labels are visited in a cycle, not sampled iid. The cleaner statement of H₀ is: *"over long sessions the number of fires accumulated per phase converges to the same long-run rate."* Under that statement, χ² goodness-of-fit is the right test and df=12 is the right df.

**Correction for within-bin clustering:** not applied in `crystalos.py`. An effective-sample-size adjustment would replace N with N/clustering-factor. On the Dell R16 reading the fact that χ² = 0.0353 is much smaller than the expected χ² under the null (which, under pure iid multinomial, would have mean df = 12) is itself evidence that the reading is *more uniform than random multinomial sampling predicts* — consistent with the cyclic-scheduler nature of the process, where long-run averaging visits each bin equally by construction.

## 9. Multiple-comparisons situation

**Only one χ² is computed per session** — on the full log, at analysis time. No scanning over sub-windows. No scanning over alternative partition schemes. No Bonferroni correction required.

**Cross-session**: if the funder pitch cites two readings (Lenovo + Dell), that is *k = 2 tests*. Strict Bonferroni would require each to be rejected at α/2 = 0.025 rather than α = 0.05 for joint significance. The Lenovo reading at χ² = 22.03, df = 12 gives p ≈ 0.037 — which rejects at α = 0.05 but *not* at α = 0.025 after Bonferroni correction for the 2-test family. The funder-pitch language must reflect this; see `LIMITATIONS.md` §1, §2.

## 10. What must still be done

- [ ] External-statistician review of this document before any funder sees the 22.03 claim. (`STATUS.md` readiness checklist.)
- [ ] Patch `crystalos.py` to support pre-registered N or T, eliminating the stopping-rule weakness for future sessions.
- [ ] Recover the Lenovo Jan 31 2026 log so the Lenovo reading is re-derivable from raw events, not just documented in a design file.
- [ ] If the patch in (2) is merged, re-run a constrained (pre-registered) session on both Lenovo and Dell R16 for the blind-test replication required by ARTIFACTS.md R3.

---

## Cross-references

- Runtime source: `docs/archive_jan2026/snowflake/crystalos.py` (431 LOC)
- Primary verification: `docs/archive_jan2026/snowflake/VERIFICATION_2026_04_21.md`
- Resolution / second note: `docs/archive_jan2026/snowflake/SNOWFLAKE_CHI2_RESOLVED_2026_04_21.md`
- Architecture source (the 22.03 citation): `docs/archive_jan2026/snowflake/source_docs/TIG_SECURITY_ARCHITECTURE.md` §8.1
- Atlas blocker (resolved): `Atlas/HANDOFF_3_3_SNOWFLAKE_CHI2.md`
- Funding branch STATUS / ARTIFACTS / LIMITATIONS: `Gen13/targets/funding_tig_snowflake/`

*Per repo policy: this file is the initial null-spec draft; subsequent drafts append revision notes rather than overwriting. Treat the statistician-review signoff as the checkpoint for "frozen" status.*
