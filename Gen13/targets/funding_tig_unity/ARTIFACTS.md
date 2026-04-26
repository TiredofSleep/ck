# ARTIFACTS — funding/tig-unity

**Purpose:** Exhaustive inventory of runnable code, specifications,
and supporting documentation for the TIG Unity track. Funders can
point here to verify what exists before committing resources.

---

> **Note (2026-04-25 revision).** This file was originally drafted as part of a pitch-style packet. Per the operator-of-record's actual stance documented at [`FUNDING.md`](../../../FUNDING.md) (root) and [`INTENT_STATEMENT.md`](../../../INTENT_STATEMENT.md), this is **thread documentation**, not a fundraising pitch. The operator-of-record makes **no commitments to donors of any kind**. Any dollar amounts, time scopes, or "ask" framings appearing below are **scope estimates of the work this thread would cover**, not price tags or commitments.

---

## Primary artifacts (runnable)

### `benchmark.py` (554 lines)
- **Source:** `github.com/TiredofSleep/All-or-Nothing-E/benchmark.py`
- **Runs:** 7 benchmark tests — convergence race (TIG vs Round-Robin vs Random), throughput, self-repair (50% chaos injection), info dynamics (entropy, autocorrelation, state diversity), scaling (6×4 to 32×24 lattices), composition depth, attractor basin (1000 random inits)
- **Dependencies:** NumPy only
- **Reproducibility:** deterministic with fixed seed
- **Reported results:** S* = 0.9668 (mean), self-repair in 1 tick, 100/100 ticks above T* = 0.714
- **Recovery status:** to be copied into `ck/docs/archive_recovered/All-or-Nothing-E/benchmark.py` with provenance header

### `tig_coherent_computer.py` (588 lines)
- **Source:** `github.com/TiredofSleep/All-or-Nothing-E/tig_coherent_computer.py`
- **Purpose:** core composition table + coherence computation + attractor basin analysis
- **`coherence_router` status:** per 2026-04-19 research, refactored into this class (not a standalone module as the handoff suggested)

### `test_coherence_router.py` (134 lines)
- **Source:** `github.com/TiredofSleep/All-or-Nothing-E/test_coherence_router.py`
- **Purpose:** pytest-compatible test suite for router invariants
- **Functions tested:** `classify`, `classify_multi`, `coherence`, `explain`, `explain_coherence`

## Secondary artifacts (specifications)

### `docs/COMPUTE.md` (128 lines)
- **Source:** `github.com/TiredofSleep/TIG-UNIFIED-THEORY-under-scrutinyMYTHDRIFT/docs/COMPUTE.md`
- **Content:** TIG Unity Kernel v9.x spec — R-σ-Λ-H signal structure, Ω̂ Operator, benchmark table (88% drop-rate reduction, 62% P99 latency, 100% cascade elimination)
- **Caveat:** benchmark numbers claimed simulated, not production-measured

### `docs/VALIDATION.md` (262 lines)
- **Source:** same repo, `docs/VALIDATION.md`
- **Content:** three core predictions with test results — threshold T*=0.714 (22.5× failure-rate ratio), recovery V* → time inverse (R² = 0.97), scale invariance across 4-12 scales

### `PROVEN_CONFIGURATION.md` (89 lines)
- **Source:** `All-or-Nothing-E/PROVEN_CONFIGURATION.md`
- **Content:** empirical discovery report from 2,100-permutation sweep; documents formula correction (original S*=σ(1-σ*)V*A* had ceiling 0.4977 < T*; corrected harmonic-mean formula achieves mean S*=0.9668)
- **Value for funder:** demonstrates honest self-correction in the face of empirical evidence — this is mature research practice

## Associated papers (PDF, in-repo)

| File | Lines / KB | Topic |
|---|---|---|
| `paper1_codec.pdf` | 15 KB | Encoder/decoder for system dynamics |
| `paper2_routing.pdf` | 18 KB | Composition table routing logic |
| `paper3_dynamics.pdf` | 22 KB | Quadratic maps & Lyapunov exponents |
| `paper4_addendum.pdf` | 12 KB | Corrections to core model |
| `paper5_koopman_bridge.pdf` | 12 KB | Connection to Koopman operator theory |
| `paper6_coherent_intelligence.pdf` | 23 KB | Application to AI systems |

## Rigor-base pointers (on `tig-synthesis`)

- `papers/proof_d7_phi_fixed_point.py` — T*=5/7 derivation
- `papers/proof_d10_tsml_73_cells.py` — TSML structural verification
- `Atlas/PLAN_OF_RECORD_2026_04_18.md` — current sprint queue
- `Atlas/FRONTIER_ALIGNMENT_2026_04_19.md` — status relative to current frontier

## Recovery tasks (before first pitch goes out)

1. [ ] Copy `benchmark.py` + `tig_coherent_computer.py` into
      `docs/archive_recovered/All-or-Nothing-E/` with provenance header.
2. [ ] Run `python benchmark.py` on a clean machine; record exact output
      in `REPRODUCTION_LOG.md`.
3. [ ] Reconcile the two headline numbers: "88% drop-rate reduction" in
      COMPUTE.md vs "32pp" in the January 2026 email — both must trace
      to actual simulation output with specified seeds.
4. [ ] Consolidate `coherence_router` into a standalone module or
      document the refactor explicitly so funders can point at a named
      artifact.

---

*Update this file when artifacts are recovered or new ones land.*
