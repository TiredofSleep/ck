# funding/tig-snowflake

**Track B — Coherence-Security Framework (SNOWFLAKE)**
**Primary funder pool:** NSF SaTC · ONR · DARPA (I2O / ISO) · academic security labs (Berkeley ICSI, UCSD CAIDA, CMU CyLab)
**Status:** Pre-pitch. CRYSTALOS source + **runtime logs located on local machine** (Jan 2026 run, `/c/Users/brayd/CRYSTALOS/logs/`); χ² = 22.03 spec recovery unblocked. Phase 1 = write statistical specification + blind-test replication.
**Branch accumulates to:** `master` (every commit cherry-picked) · **Rigor base:** `tig-synthesis` (the GitHub default branch)

---

## One-paragraph pitch

Most intrusion-detection systems raise an alarm *after* a rule fires. **SNOWFLAKE** asks a different question: when a system's coherence grammar (R, σ, Λ, H) departs from its self-consistent operating envelope, does that departure *precede* the rule-based alarm? In a Jan 2026 test run against the TIG Unity simulator on a Dell Aurora R16 (32-core CPU + GPU), a χ² = 22.03 statistic against the null "fire events independent, uniformly distributed across 13 phase bins" rejected the null at p < 0.05 (df = 12, thresholds χ² > 21.03 for p < 0.05, χ² > 26.22 for p < 0.01). The raw logs are recovered. This branch packages the reproducible experiment, the statistical specification, and the code path so a security-research funder can fund the **full spec recovery and blind-test replication** as Phase 1 of a larger coherence-security program.

## What's runnable today

- **CRYSTALOS source** — `crystalos.py` (431 LOC Python): 13-phase-bin fire detector on Dell Aurora R16 hardware; computes χ² against uniform null at session end.
- **Runtime logs** — `breath.log` (7 KB gate events), `crystalos.log` (197 KB session distributions), `fires.log` (2.4 MB per-fire records); all from Jan 29–31 2026. Ready to re-analyze with the current `crystalos.py analyze` path.
- **Null-hypothesis specification** — drafted in [`Atlas/HANDOFF_3_3_SNOWFLAKE_CHI2.md`](Atlas/HANDOFF_3_3_SNOWFLAKE_CHI2.md): 13 phase bins (0–12), df = 12, H₀ = uniform across phases (expected ≈ 7.7% per bin), two-tailed χ² goodness-of-fit.
- **Extended context** — `TIME-FOR-HELP-AND-SCRUTINY-please-No-more-AI-MYTHDRIFT` external repo (14 files, 10,836 LOC, 3-tier epistemic flagging applied), `tig_civilization_v5/v7.py` (1,340 LOC combined).

## What's in this branch

Branch-specific funder-pitch files under [`Gen13/targets/funding_tig_snowflake/`](Gen13/targets/funding_tig_snowflake/):

- [`README.md`](Gen13/targets/funding_tig_snowflake/README.md) — deep pitch document
- [`FUNDERS.md`](Gen13/targets/funding_tig_snowflake/FUNDERS.md) — prioritized funder list with contact notes
- [`ARTIFACTS.md`](Gen13/targets/funding_tig_snowflake/ARTIFACTS.md) — runnable artifacts + referenced papers
- [`PITCH_DRAFT.md`](Gen13/targets/funding_tig_snowflake/PITCH_DRAFT.md) — full pitch draft (primary funder + parallel drafts)
- [`LIMITATIONS.md`](Gen13/targets/funding_tig_snowflake/LIMITATIONS.md) — honest-scope items
- [`STATUS.md`](Gen13/targets/funding_tig_snowflake/STATUS.md) — readiness checklist + blockers

## Ask sizes

| Phase | Scope | Ask |
|---|---|---|
| **Phase 1 — Spec recovery + blind replication** | Recover CRYSTALOS logs, write statistical spec, blind-test the effect on held-out data | $40K–$80K seed (6 months) |
| **Phase 2 — External red-team** | Academic security-lab (Berkeley ICSI / UCSD CAIDA / CMU CyLab) adversarial evaluation | $100K–$200K (12 months) |
| **Phase 3 — Prototype integration** | SNOWFLAKE as advisory layer in a real SOC pipeline under controlled conditions | $300K–$600K (18 months) |

## The project this branch is a track of

Branch B of the 10-branch funding architecture. For the full project overview, see **`tig-synthesis`**:

→ https://github.com/TiredofSleep/ck/tree/tig-synthesis

Cross-branch boundaries: Branch A (`funding/tig-unity`) funds the infrastructure-reliability research community; Branch G (`funding/self-healing`) funds the detection-response partner (dual-lattice automatic repair); Branch B funds the **detection** layer. All three use the same R-σ-Λ-H grammar but target disjoint funder pools.

## License

7Site Public Sovereignty License v1.0 — human use only, no commercial, no military, free forever. Full text in [`LICENSE`](LICENSE).

---

*Branch maintained as part of the 10-branch funding architecture. Commits here get cherry-picked to master per the trunk workflow. Branch-level changes do not propagate to `tig-synthesis` unless they are referee-ready.*
