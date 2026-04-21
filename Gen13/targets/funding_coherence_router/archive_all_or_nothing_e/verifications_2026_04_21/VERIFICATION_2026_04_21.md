# Verification 2026-04-21 — funding/coherence-router

**Branch:** `funding/coherence-router`
**Archive:** `Gen13/targets/funding_coherence_router/archive_all_or_nothing_e/`
**Verifier:** Brayden Sanders (with Claude assist)
**Environment:** Python 3.13 on Windows 11, NumPy, `PYTHONIOENCODING=utf-8`

---

## Scripts executed

| Script | Status | Output |
|---|---|---|
| `tig_coherent_computer.py` | ran cleanly (20 ticks after GFM seed) | `tig_coherent_computer_stdout.txt` |
| `benchmark.py` | ran cleanly (full 8-test suite) | `benchmark_stdout.txt` |
| `test_engine_v2.js` | NOT RUN — Node/Bun/Deno not in env | see funding/physics-sim-edu verification |

Post-run lattice snapshot: `tig_lattice_after_run.bin` (3024 bytes, md5 `c544021edceb516f4e5dea36a7ddb8da`). Pre-run committed snapshot was restored in the working tree (md5 `c90a8f98f312e88ecda200911c50f6e6`).

---

## Run 1 — `tig_coherent_computer.py` (PROVEN configuration)

18×14 lattice (252 cells), harmonic-mean S*, Moore neighborhood, majority-vote dynamics, GFM-seeded init with generators `{012, 071, 123}`.

| Metric | Value |
|---|---|
| Boot S* (before GFM injection) | 0.7453 — already in basin |
| Tick 3 S* | 0.9970 (peak) |
| Tick 20 S* | 0.9793 |
| State distribution @ tick 20 | BREATH 79.4 %, HARMONY 15.5 %, FRUIT 5.2 % |
| Mean H @ tick 20 | −0.5472 |
| Hook capture | `['0.9943', '0.9793', '0.9943']` (7↔8 heartbeat) |
| Output words | `HARMONY HARMONY BREATH BREATH BREATH BREATH BREATH HARMONY HARMONY HARMONY HARMONY BREATH HARMONY HARMONY` |

**Verdict:** The proven configuration converges to and stays within the attractor basin. Matches claims in `PROVEN_CONFIGURATION.md` (mean S* ≈ 0.9668, sustained above T*).

---

## Run 2 — `benchmark.py` (8-test comparative suite)

14×12 lattice (168 cells). Deterministic snake-init `cells[i,j] = (i·cols+j) mod 10` for Tests 1-5; random init for Test 7 (attractor basin).

### Test 1 — Convergence race (100 ticks)

| Strategy | Final S* | Peak S* | Avg S* | Reached T*=0.714? | Runtime |
|---|---|---|---|---|---|
| TIG | 0.1546 | 0.3780 | 0.2568 | **NEVER** | 0.136 s |
| Round-robin | 0.2313 | 0.2313 | 0.2292 | NEVER | 0.053 s |
| Random | 0.2416 | 0.2893 | 0.2330 | NEVER | 0.375 s |

TIG vs round-robin = 1.1× average; TIG vs random = 1.1× average.

### Test 2 — Throughput (50 ticks)

| Strategy | Cell-ops/sec | Transitions | Churn |
|---|---|---|---|
| TIG | 159,390 | 6,703 | 79.8 % |
| Round-robin | 2,204,352 | 8,400 | 100.0 % |
| Random | 9,805,776 | 7,566 | 90.1 % |

### Test 3 — Self-repair (50 % chaos injection)

| Strategy | Before | Damaged | After | Recovery | Recovered tick |
|---|---|---|---|---|---|
| TIG | 0.1588 | 0.2171 | 0.1909 | 120 % | 1 |
| Round-robin | 0.2313 | 0.1986 | 0.1986 | 86 % | 1 |
| Random | 0.2450 | 0.2313 | 0.2347 | 96 % | 3 |

Note: "120 % recovery" here means `after > before` but starting from a very low baseline (0.1588) that was already below all other strategies. Not a strong claim.

### Test 4 — Information dynamics (50 ticks)

| Strategy | Entropy (start → end) | Autocorr (start → end) | Unique states |
|---|---|---|---|
| TIG | 1.825 → 1.861 | 0.310 → 0.332 | 5/10 |
| Round-robin | 3.322 → 3.322 | 0.225 → 0.265 | 10/10 |
| Random | 3.285 → 3.278 | −0.001 → −0.027 | 10/10 |

TIG visits only half the state alphabet under this init.

### Test 5 — Scaling (30 ticks/size, TIG only)

| Size | Cells | Final S* | Reached T*? | Throughput |
|---|---|---|---|---|
| 6×4 | 24 | 0.2922 | NEVER | 113,765 ops/s |
| 10×8 | 80 | 0.1986 | NEVER | 119,847 ops/s |
| 14×12 | 168 | 0.1671 | NEVER | 120,963 ops/s |
| 18×14 | 252 | 0.3695 | NEVER | 122,789 ops/s |
| 24×18 | 432 | 0.1820 | NEVER | 120,815 ops/s |
| 32×24 | 768 | 0.4039 | NEVER | 122,388 ops/s |

No size reaches T*. Throughput is size-insensitive (~120 K ops/s).

### Test 6 — Composition depth

Cross-composition matrix (steps to reach state 7) captured verbatim in stdout; all non-absorbing states reach HARMONY in 1–6 steps via self-composition. Matches theory.

### Test 7 — Attractor basin (1000 random initial states × 50 ticks)

| Strategy | Reached T* | Mean S* | Std |
|---|---|---|---|
| TIG | **0 / 1000 (0.0 %)** | 0.3097 | 0.0427 |
| Round-robin | 0 / 1000 (0.0 %) | 0.2283 | 0.0211 |
| Random | ~0 / 1000 (structural) | — | — |

**Zero of 1000 random starts reached T* under benchmark.py's S* formula.**

### Test 8 — Ollama tie-in assessment (narrative only)

Prose section; no measurements.

---

## The summary-vs-data contradiction

`benchmark.py` lines 517–529 print this *hardcoded* "KEY FINDINGS" block after the numeric results:

> COHERENCE (100 ticks, 14×12 lattice):
>   TIG:         S* = 0.1546
>   Round Robin: S* = 0.2313
>   Random:      S* = 0.2416
>
> KEY FINDINGS:
>   • TIG is the ONLY strategy that reaches coherence (S* > T*)
>   ...

The first bullet is **literally false for this run**. TIG finishes at 0.1546 — below round-robin (0.2313) and below random (0.2416), and far below T*=0.714. Test 7 confirms it on 1000 random inits (0/1000 reached T*).

## Root cause

`benchmark.py:81-106` (`compute_coherence`) uses the **superseded iterated-fixed formula**:

```python
s_star = D_STAR
for _ in range(20):
    s_new = SIGMA * (1 - s_star) * v_star * a_star
    ...
```

This is the formula that `PROVEN_CONFIGURATION.md` explicitly flags as broken:

> Even with V*=A*=1: `S* = 0.991/1.991 = 0.4977`
> **T* = 0.714. The ceiling is 0.4977. It is mathematically impossible to breach threshold.**

The ceiling is 0.4977. The benchmark can never show S* > T* because the formula it uses cannot produce S* > 0.4977 under any input.

Additional discrepancies from the proven configuration:

| Component | `benchmark.py` uses | `tig_coherent_computer.py` / PROVEN uses |
|---|---|---|
| S* formula | iterated fixed-point `σ(1−S*)V*A*` (ceiling 0.4977) | harmonic mean `3/(1/σ + 1/V* + 1/A*)` |
| A* definition | fraction in states {5,6,7} | fraction in states {4,5,6,7,8} (full funnel) |
| Neighborhood | Von Neumann (4 neighbors, lines 53–58) | Moore (8 neighbors) per PROVEN |

All three shortcuts depress the measured S* relative to the proven configuration.

## Prescription (not applied in this commit — recording the finding)

Two options, either is acceptable; user decides:

1. **Update `benchmark.py`** — replace `compute_coherence`, `a_star` definition, and neighborhood to match `tig_coherent_computer.py`. Re-run to show whether TIG then actually beats round-robin/random.
2. **Keep `benchmark.py` as-is** — add a `DEPRECATED_FORMULA.md` or header comment explaining that this benchmark measures the *pre-fix* routing and is preserved for historical comparison. Strip or rewrite the hardcoded "KEY FINDINGS" prose so the file stops printing a conclusion the numbers do not support.

Neither option changes the physics claim of the proven configuration (which is validated by `tig_coherent_computer.py` in Run 1). The `all_or_nothing_e` archive folder is preserved per never-delete; this doc records what is and is not reproducible from it.

---

## Reproduction

```bash
cd Gen13/targets/funding_coherence_router/archive_all_or_nothing_e/
PYTHONIOENCODING=utf-8 python tig_coherent_computer.py   # → S*=0.9793 in attractor
PYTHONIOENCODING=utf-8 python benchmark.py               # → TIG NEVER reaches T* under its own metric
```

Both stdout logs in this directory are verbatim captures from the runs on 2026-04-21.

---

## Honest summary

- **Attractor basin is real.** `tig_coherent_computer.py` reaches and sustains S* ≈ 0.98 under the proven configuration from a GFM-seeded init.
- **`benchmark.py` as shipped does not demonstrate what its printed summary claims.** Its metric has a mathematical ceiling below the threshold it tests against. Zero of 1000 random inits clear T* in its own Test 7.
- **Both files belong in the archive.** The tension between them is informative: it shows which configuration was kept (proven) and which was abandoned (benchmark). Recording this is preferable to removing the benchmark.
