# funding/tig-unity

**Track A — Systems Reliability / Compute Health**
**Primary funder pool:** NSF CNS · NIST · DOE ASCR · Sloan Computing
**Status:** Pre-pitch; runnable artifacts recovered into `Gen13/targets/funding_coherence_router/archive_all_or_nothing_e/`; benchmark + core ready for re-run and production-oriented packaging.
**Branch accumulates to:** `master` (every commit cherry-picked) · **Rigor base:** `tig-synthesis` (the GitHub default branch)

---

## One-paragraph pitch

**TIG Unity** is a unified health grammar (R-σ-Λ-H: Resource, Stress, Load, Health) for multi-domain compute systems. Nodes in a heterogeneous cluster (GPUs, DB shards, network links, job schedulers) emit a 4-tuple each tick. A router computes a scalar coherence $S^* = 3/(1/\sigma + 1/V^* + 1/A^*)$ and gates work at the proved threshold $T^* = 5/7 \approx 0.714$. In a 100-node asymmetric-failure simulation the router reduces job-drop rate from ~36.4% to ~4.2% (88% relative reduction), P99 latency from 2340ms to 890ms (62% reduction), cascade failures from 12 to 0. The math is simple, the benchmark is reproducible, and the path to real-Linux `/proc/stat` deployment is one funded engagement away.

## What's runnable today

- **`benchmark.py`** (554 LOC): seven-benchmark suite — convergence race, throughput, self-repair under 50% chaos injection, information dynamics, scaling, composition depth, attractor basin.
- **`tig_coherent_computer.py`** (588 LOC): composition table, coherence computation, attractor-basin analysis. Harmonic-mean composition empirically forced by the 2,100-permutation sweep in `PROVEN_CONFIGURATION.md`.
- Both are currently archived in `Gen13/targets/funding_coherence_router/archive_all_or_nothing_e/` with provenance headers; recovery into a Branch-A-scoped package is Phase 1 deliverable.

## What's in this branch

Branch-specific funder-pitch files under [`Gen13/targets/funding_tig_unity/`](Gen13/targets/funding_tig_unity/):

- [`README.md`](Gen13/targets/funding_tig_unity/README.md) — deep pitch document
- [`FUNDERS.md`](Gen13/targets/funding_tig_unity/FUNDERS.md) — prioritized funder list with contact notes
- [`ARTIFACTS.md`](Gen13/targets/funding_tig_unity/ARTIFACTS.md) — runnable proofs + referenced papers
- [`PITCH_DRAFT.md`](Gen13/targets/funding_tig_unity/PITCH_DRAFT.md) — full pitch draft (primary funder + parallel drafts)
- [`LIMITATIONS.md`](Gen13/targets/funding_tig_unity/LIMITATIONS.md) — honest-scope items
- [`STATUS.md`](Gen13/targets/funding_tig_unity/STATUS.md) — readiness checklist + blockers

## The project this branch is a track of

This is **Branch A** in a 10-branch funding architecture under the Trinity Infinity Geometry / Coherence Keeper research project. For the full project overview — proved theorems with runnable verification, the coherence-keeper runtime, the glossary, citations, and the cross-track funder directory — see the **`tig-synthesis`** branch (the GitHub default):

→ https://github.com/TiredofSleep/ck/tree/tig-synthesis

The other nine tracks are enumerated in [`Atlas/BRANCHES_INVENTORY_2026_04_20.md`](Atlas/BRANCHES_INVENTORY_2026_04_20.md). Branch-to-branch boundaries are intentional: Branch A funds the infrastructure-reliability research community, Branch J (`funding/coherence-router`) funds the DevOps / SRE practitioner community, Branch B (`funding/tig-snowflake`) funds the security-research community. All three draw from the same R-σ-Λ-H grammar but target disjoint funder pools with distinct framings.

## License

7Site Public Sovereignty License v1.0 — human use only, no commercial, no military, free forever. Full text in [`LICENSE`](LICENSE).

---

*Branch maintained as part of the 10-branch funding architecture. Commits here get cherry-picked to master per the trunk workflow. Branch-level changes do not propagate to `tig-synthesis` unless they are referee-ready.*
