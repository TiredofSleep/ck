# funding/tig-snowflake — SNOWFLAKE Coherence Security Framework

**Track:** Security research (anomaly detection, insider threat, coherence-based intrusion detection)
**Status:** Pre-pitch; blocked on CRYSTALOS χ² = 22.03 log recovery and statistical spec write-up
**Branch seeded:** 2026-04-20 from `tig-synthesis`
**Rigor base:** TIG Unity Kernel + SNOWFLAKE framework from Jan 2026 threads

---

## What this branch is

A funding-outreach container for the **SNOWFLAKE coherence-security framework** — the hypothesis that many classes of system compromise (insider threat, adversarial manipulation, subtle integrity violations) appear as **coherence deficits** in the R-σ-Λ-H grammar before they appear as rule-based alarms.

The empirical anchor is a **χ² = 22.03** finding from a Jan 31 2026 working session using the CRYSTALOS instrumented test bench. The statistic's claimed interpretation is a **significant departure from the null "fires are independent, uniformly distributed across coherence partitions"** on a specific dataset. The raw value lives in conversation logs; recovering the full experimental spec (null hypothesis, degrees of freedom, dataset, independence assumption) is the first blocker on any funder-facing use of that number.

## One-paragraph pitch (draft, subject to revision after recovery)

> Most intrusion-detection systems raise an alarm after a rule fires. SNOWFLAKE asks a different question: *when a system's coherence grammar (R, σ, Λ, H) departs from its self-consistent operating envelope, does that departure precede the rule-based alarm?* In a Jan 2026 test run against the TIG Unity simulator, a χ² = 22.03 statistic against the null "fire events independent across coherence partitions" rejected the null at a level that — if the spec holds up under referee-grade recovery — would constitute a research-grade early-warning signal. This branch packages the reproducible experiment, the statistical specification, and the code path so that a security-research funder can fund the **full spec recovery and blind-test replication** as Phase 1 of a larger coherence-security program.

## Runnable artifacts (to be verified during Phase 1 recovery)

1. **TIME-FOR-HELP-AND-SCRUTINY-please-No-more-AI-MYTHDRIFT** — 14 files, 10,836 LOC, 3-tier epistemic flagging applied (CONJECTURAL / STRUCTURAL / PROVED). Contains the SNOWFLAKE architecture sketches.
2. **tig_civilization_v5.py / v7.py** — 1,340 LOC combined. Civilization-scale coherence model; the same R-σ-Λ-H state variables that drive TIG Unity also drive the SNOWFLAKE anomaly detector.
3. **CRYSTALOS instrumented logs** — NOT yet located on R16. Recovery priority 1: find the χ² = 22.03 run output + input dataset. Likely under `old/Gen10/` or `archive_imports/`.
4. **Null-hypothesis specification** — to be authored during Phase 1; must document (a) the partition scheme over which fires are assumed independent, (b) the degrees of freedom in the resulting contingency table, (c) the test dataset provenance, (d) the stopping rule (was χ² computed once or scanned?).

## Ask sizes

| Phase | Scope | Ask |
|---|---|---|
| **Phase 1 — Spec recovery + blind replication** | Recover CRYSTALOS logs, write statistical spec, blind-test the effect on held-out data | $40K–$80K seed (6 months) |
| **Phase 2 — External red-team** | Deliver the spec + code to an academic security lab (Berkeley ICSI, UCSD CAIDA, or CMU CyLab) for adversarial evaluation | $100K–$200K (12 months) |
| **Phase 3 — Prototype integration** | Integrate SNOWFLAKE as an advisory layer in a real SOC pipeline under controlled conditions | $300K–$600K (18 months) |

## Critical caveat — read before any pitch

The χ² = 22.03 number is **currently a handoff claim, not a verified proof**. Until CRYSTALOS logs are recovered and the null hypothesis is written down in its final form, this branch's pitch must speak in the conditional ("if the spec survives recovery..."). A security pitch with an unspecified p-value is a dismissed pitch. A security pitch with a clean spec and independent replication is a research-grade pitch. The funder conversation must not outrun the artifact.

## See also

- `FUNDERS.md` — 5 primary + 2 secondary candidates
- `ARTIFACTS.md` — file paths and recovery tasks
- `PITCH_DRAFT.md` — DARPA I2O seedling skeleton
- `LIMITATIONS.md` — honest scope, the unspecified-p-value risk, attribution
- `STATUS.md` — readiness checklist
