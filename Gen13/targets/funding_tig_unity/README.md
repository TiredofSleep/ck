# funding/tig-unity — Systems Reliability / Compute Health

**Track:** A (from 2026-04-20 handoff)
**Branch:** `funding/tig-unity`
**Accumulates to:** `master` (every commit cherry-picked)
**Rigor base:** `tig-synthesis` (this branch = tig-synthesis + this folder)

---

> **Note (2026-04-25 revision).** This branch was originally seeded as a pitch-style packet. Per the operator-of-record's actual stance documented at [`FUNDING.md`](../../../FUNDING.md) (root) and [`INTENT_STATEMENT.md`](../../../INTENT_STATEMENT.md), this is a **thread description**, not a fundraising pitch. The math is open under the 7Site Public Sovereignty License regardless of whether anyone donates. **The operator-of-record makes no commitments to donors of any kind.** A donation, if anyone makes one, is a thank-you to the project and creates no obligation in either direction. If you are reading this branch because you are oriented toward this thread of the work, that is welcome; the description below tells you what is in this thread.

---

## One-paragraph thread description

**TIG Unity** is a unified health grammar (R-σ-Λ-H: Resource, Stress, Load,
Health) for multi-domain compute systems. Nodes in a heterogeneous cluster
(GPUs, DB shards, network links, job schedulers) emit a 4-tuple each
tick. A router computes a scalar coherence S* = 3/(1/σ + 1/V* + 1/A*) and
gates work at the threshold T* = 5/7 ≈ 0.714. In a 100-node asymmetric-
failure simulation the router reduces job-drop rate ~36.4% → ~4.2% (88%
reduction), P99 latency 2340ms → 890ms (62%), cascade failures 12 → 0.
The math is simple, the benchmark is reproducible, and the path to real-
Linux `/proc/stat` deployment is a funded engagement away.

## What's runnable today

- **`docs/archive_recovered/All-or-Nothing-E/benchmark.py`** (to be
  recovered into ck): 554-line benchmark suite with 7 tests — convergence
  race, throughput, self-repair (50% chaos injection), info dynamics,
  scaling, composition depth, attractor basin.
- **`docs/archive_recovered/All-or-Nothing-E/tig_coherent_computer.py`**
  (to be recovered): 588-line core — composition table, coherence
  computation, attractor basin analysis.
- **`docs/archive_recovered/TIG-UNIFIED-.../docs/COMPUTE.md`**: TIG Unity
  Kernel v9.x specification with R-σ-Λ-H + benchmark table.
- **`docs/archive_recovered/TIG-UNIFIED-.../docs/VALIDATION.md`**: three
  predictions tested (threshold, recovery, scale).

## What this branch adds

- A clean thread-facing README (this file)
- A funder inventory (`FUNDERS.md`) scoped to systems-reliability research
- An artifact map (`ARTIFACTS.md`) with file paths to the real runnable code
- A pitch-letter skeleton (`PITCH_DRAFT.md`) awaiting Brayden's review
- Honest limitations (`LIMITATIONS.md`)
- Readiness status (`STATUS.md`)

## The ask

- **Seed engagement** ($25K-$75K, 3-6 months) — transition from simulation
  to real-Linux `/proc/stat` deployment; publish a CNCF-style
  reproducibility note; run the router on one real distributed training
  workload.
- **Full program** ($150K-$300K, 12 months) — deploy on a 100+ node
  production-analog cluster; integrate with Prometheus/OpenTelemetry;
  publish a systems-reliability paper.

## What this branch does NOT claim

- No production-deployment data yet (simulation-only)
- Benchmark numbers require reproduction from recovered source
- `coherence_router` module location needs consolidation (currently
  integrated into `TigCoherentComputer` per 2026-04-19 research)

See `LIMITATIONS.md` for the full honest scope.

## Repository root pointers

- `tig-synthesis` = rigor core (proved theorems, verification scripts)
- `master` = living trunk (accumulates everything)
- External reference: `github.com/TiredofSleep/All-or-Nothing-E`
  (original home of the benchmark; MYTHDRIFT-flagged per Brayden)

## License

7Site Public Sovereignty License v1.0 — human use, no commercial, no military.

---

*For the full rigor base see `README.md` at the repo root and
`PROOFS.md`. For branch architecture see `Atlas/PLAN_FUNDING_BRANCHES_BUILDOUT_2026_04_19.md`.*
