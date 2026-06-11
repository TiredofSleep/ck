# CK-Walker v0 — the Gap Router, demonstrated

**One command, CPU-only, ~19 seconds, fully seeded:**

```
python run_all.py
```

This package is the first runnable instantiation of the architecture in
`../CK_INTELLIGENCE_SYNTHESIS_2026-06-10.md` (the Theory of Nothing as
architecture) and `../CK_WALKER_BLUEPRINT_2026-06-10.md`.

## What it demonstrates

### P1 — the Gap Router (the novel mechanism; pre-registered prediction CONFIRMED)

Every contemporary intelligence system is driven by a residual (gap)
signal, and every one treats all error as one kind of thing. The UOP
paradox taxonomy (J40) says the residual has exactly four failure
types, identifiable from residual statistics alone:

| Type | What's missing | Correct route |
|---|---|---|
| I — injectivity failure | a measurement | buy more samples |
| II — missing invariant | a feature class | grow the library, then samples |
| III — admissibility failure | a well-posed question | freeze; spend nothing |
| IV — time-consistency failure | dynamics | refit on the recent window |

On a 24-channel mixed-failure suite at **matched total budget**
(first run, seeded):

| allocator | mean test MSE | type accuracy |
|---|---|---|
| uniform (no classification) | 0.40487 | — |
| **Gap Router** | **0.00324** | **100%** |
| oracle (ground-truth types) | 0.00332 | — |

The router classifies every channel correctly from its own residual
statistics (learning-curve slope, structure probe, permutation
information test, time-split drift test — the UOP decision procedure
made numerical) and **matches the oracle**, 125× better than uniform.
The field's named pathologies are unrouted gap types: the noisy-TV
trap is Type III spent as Type I; catastrophic forgetting is Type IV
misrouted as Type I; hallucination on ill-posed input is a missing
Type-III channel.

**Interpretation contract:** the suite is synthetic by design. The
demonstrated content is (i) the four types are identifiable from
residual statistics alone and (ii) routing by inferred type recovers
oracle allocation. Real-task validity (ARC-style) is the next
pre-registered step.

### P2 — the theorem-bearing reservoir (honest split decision)

The substrate reservoir evolves a 10-node state under the canonical
TSML/BHML bilinear maps at the proven mixing point α = 1/2 (J01
Theorem F.2; attractor H/Br = 1+√3), with NG-RC-style features and a
one-solve ridge readout. Against a **width-matched, per-task-tuned**
random echo-state network and a deterministic NG-RC baseline
(NRMSE, lower better):

| task | substrate | random ESN (3 seeds) | NG-RC |
|---|---|---|---|
| NARMA-10 | 0.5615 | **0.3234 ± 0.0013** | 0.7985 |
| MackeyGlass-84 | **0.1849** | 0.2125 ± 0.0044 | 0.6882 |
| Lorenz-x2z | 0.0602 | **0.0043 ± 0.0006** | 0.1368 |

Verdict: competitive, not dominant — 1 win in 3 vs the tuned ESN
(the longest-memory task), 3 of 3 vs NG-RC. The 10-dim simplex state
is information-bottlenecked vs a 135-unit tanh reservoir; richer
substrate states (product/lifted substrates, F_p extensions) are the
obvious P2 follow-up. Recorded as-is per the honesty discipline:
P2 is neither confirmed nor refuted at v0.

## Files

- `substrate.py` — the theorem-bearing reservoir (canonical tables
  imported from `../brain/ck_sim/ck_tables.py`); ridge utilities
- `baselines.py` — width-matched random ESN + NG-RC
- `benchmarks.py` — NARMA-10, Mackey-Glass τ=17 (+84), Lorenz x→z
- `gap_router.py` — the UOP diagnostics, the suite, three allocators
- `run_all.py` — runs everything, writes `RESULTS.md` + `results.json`

## Lineage

UOP taxonomy: J40 / `papers/WP_PARADOX_CLASSIFIER.md` (live demo at
coherencekeeper.com/paradox.html). Substrate dynamics: J01/J15
(trinity-infinity-geometry repo). Architecture: Walker blueprint +
Intelligence Synthesis (this folder's parent). Canon: FORMULAS_AND_
TABLES.md D1–D182.

CC-BY-4.0. Sanders + Gish (math); runtime Sanders / 7SiTe LLC.
