# B1: Nested Shell Collapse Generator — FROZEN SPEC v1.0
## Implementation-Ready Benchmark for Stage 1A

---

**Spec status:** FROZEN. No changes after this point without bumping to v2.0 and revalidating prior results against the new version.

**Scope:** This document specifies the data generator, ground truth, fitter interface, scoring logic, and run protocol for Benchmark B1. It does NOT specify the fitting algorithm itself. Any fitter that consumes the specified data format and emits the specified output format can be evaluated against this benchmark.

---

## 1. Generator Definition

### 1.1 Carrier

$R := \mathbb{Z}/10\mathbb{Z} = \{0, 1, 2, 3, 4, 5, 6, 7, 8, 9\}$.

### 1.2 Ground-Truth Operator $T_{\text{true}}$

$T_{\text{true}}: R \times R \to R$ defined as the Z/10Z TSML published table, reconstructed via the 3-layer tower $C_0 \oplus C_1 \oplus C_2$.

**Attractor:** $h_{\text{true}} = 7$.

**Units:** $U_{\text{true}} = \{1, 3, 7, 9\}$.

**Shell partition:** $\sigma_{\text{true}}: U_{\text{true}} \to \{1, 2\}$ defined by $\sigma_{\text{true}}(u) = v_2(3u + 1)$:
- $\sigma_{\text{true}}(1) = 2$ (since $3 \cdot 1 + 1 = 4, v_2(4) = 2$)
- $\sigma_{\text{true}}(3) = 1$ (since $3 \cdot 3 + 1 = 10, v_2(10) = 1$)
- $\sigma_{\text{true}}(7) = 1$ (since $3 \cdot 7 + 1 = 22, v_2(22) = 1$)
- $\sigma_{\text{true}}(9) = 2$ (since $3 \cdot 9 + 1 = 28, v_2(28) = 2$)

**Core:** $\text{Core}_{\text{true}} = U_{\text{true}} \setminus \{1\} = \{3, 7, 9\}$.

**Seam sets (ordered pairs):**
- $S_{\text{MAX,true}} = \{(2,4), (4,2), (2,9), (9,2), (4,8), (8,4)\}$ — 6 pairs
- $S_{\text{ADD,true}} = \{(1,2), (2,1)\}$ — 2 pairs
- $S_{\text{true}} = S_{\text{MAX,true}} \cup S_{\text{ADD,true}}$ — 8 pairs, disjoint union

**Canonical construction $C_0$:** For $(x, y) \in R \times R$:

1. If $x = 0$ or $y = 0$:
   - If $(x, y) \in \{(0, 7), (7, 0)\}$: return 7.
   - Else: return 0.
2. Else if $x \in \text{Core}_{\text{true}}$ and $y \in \text{Core}_{\text{true}}$ and $\sigma_{\text{true}}(x) \neq \sigma_{\text{true}}(y)$:
   - Return $x$ if $\sigma_{\text{true}}(x) < \sigma_{\text{true}}(y)$, else $y$.
3. Else: return $h_{\text{true}} = 7$.

**Full operator $T_{\text{true}}$:**

$$T_{\text{true}}(x, y) = \begin{cases}
\max(x, y) & \text{if } (x, y) \in S_{\text{MAX,true}} \\
(x + y) \bmod 10 & \text{if } (x, y) \in S_{\text{ADD,true}} \\
C_0(x, y) & \text{otherwise}
\end{cases}$$

**Reference table (for implementation verification):**

$T_{\text{true}}$ is the published Z/10 TSML. All 100 entries are fully determined and recoverable via the rules above. A reference implementation must verify cell-by-cell equality with the following published values (full 10×10 in row-major order):

```
Row 0: [0, 0, 0, 0, 0, 0, 0, 7, 0, 0]
Row 1: [0, 7, 3, 7, 7, 7, 7, 7, 7, 7]
Row 2: [0, 3, 7, 7, 4, 7, 7, 7, 7, 9]
Row 3: [0, 7, 7, 7, 7, 7, 7, 7, 7, 3]
Row 4: [0, 7, 4, 7, 7, 7, 7, 7, 8, 7]
Row 5: [0, 7, 7, 7, 7, 7, 7, 7, 7, 7]
Row 6: [0, 7, 7, 7, 7, 7, 7, 7, 7, 7]
Row 7: [7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
Row 8: [0, 7, 7, 7, 8, 7, 7, 7, 7, 7]
Row 9: [0, 7, 9, 3, 7, 7, 7, 7, 7, 7]
```

Implementation fails verification if any cell disagrees.

### 1.3 Sampling Distribution for $(x, y)$

For each sample $i$ in $1, \ldots, N$:
- Draw $x_i, y_i$ independently, uniformly at random from $\{0, 1, \ldots, 9\}$.

**Why uniform:** to guarantee every pair has expected coverage $N/100$. No stratification.

---

## 2. Parameter List and Ranges

| Parameter | Symbol | Values for this benchmark | Description |
|---|---|---|---|
| Carrier size | $n$ | 10 | Fixed. |
| Sample count | $N$ | 100000 / 500000 / 1000000 | Varies by noise level. |
| Noise probability | $p_{\text{noise}}$ | 0.05 / 0.15 / 0.30 | Three noise levels. |
| RNG seed | $s$ | 0, 1, 2, 3, 4 | Five seeds per noise level. |

**Total configurations:** 3 noise levels × 5 seeds = **15 benchmark runs.**

| Noise level tag | $p_{\text{noise}}$ | $N$ |
|---|---|---|
| `low` | 0.05 | 100,000 |
| `med` | 0.15 | 500,000 |
| `high` | 0.30 | 1,000,000 |

Higher $N$ at higher noise compensates for reduced signal-to-noise.

---

## 3. Noise Model and Schedule

### 3.1 Noise model: uniform replacement

For each sample $(x_i, y_i)$:
1. Compute $z_i^{\text{true}} = T_{\text{true}}(x_i, y_i)$.
2. Draw $u_i \sim \text{Uniform}[0, 1)$.
3. If $u_i < p_{\text{noise}}$: draw $z_i \sim \text{Uniform}\{0, 1, \ldots, 9\}$ (uniform over the 10 classes, independent of $z_i^{\text{true}}$).
4. Else: $z_i = z_i^{\text{true}}$.

This is "replacement with uniform random output" noise. It is **not** swap-with-other-specific-value. It is **not** additive modular noise.

### 3.2 RNG specification

- Language: Python 3.
- Random source: `numpy.random.default_rng(seed)` for all randomness (both sampling $(x, y)$ and the noise decision).
- Sampling order (deterministic):
  - For $i$ in $0, \ldots, N-1$:
    - $x_i = \text{rng.integers}(0, 10)$
    - $y_i = \text{rng.integers}(0, 10)$
    - $u_i = \text{rng.random}()$
    - If $u_i < p_{\text{noise}}$: $z_i = \text{rng.integers}(0, 10)$
    - Else: $z_i = T_{\text{true}}(x_i, y_i)$
- Reproducibility requirement: given the same $(N, p_{\text{noise}}, s)$ tuple, the identical sequence of $(x_i, y_i, z_i)$ must be produced on any compliant implementation.

### 3.3 Verification sample

For $(N, p_{\text{noise}}, s) = (100000, 0.05, 0)$:
- First 5 triples (0-indexed): implementation must produce these exact values:
  - Generate using the above procedure; record and check against the generating script's output to ensure reproducibility.
  - These values are computed by the reference implementation and are deterministic given the RNG spec. A compliant implementation will produce the same triples.

(Since they depend on the exact NumPy RNG behavior, they are to be emitted by the reference generator and stored as a verification file; see §12.)

---

## 4. Output Data Format

### 4.1 Data file

One file per configuration. Format: CSV with header.

**Filename pattern:**
```
data/nscg_N{N}_p{p_percent:03d}_s{seed}.csv
```
where `p_percent = int(p_noise * 100)` (zero-padded to 3 digits: `005`, `015`, `030`).

**Examples:**
- `data/nscg_N100000_p005_s0.csv`
- `data/nscg_N500000_p015_s3.csv`
- `data/nscg_N1000000_p030_s4.csv`

**Columns:** `x, y, z` (three integers, each in $\{0, \ldots, 9\}$).

**Rows:** exactly $N$ rows, in generation order.

**No other columns.** No timestamps, no derived features, no noise flags.

### 4.2 Data file integrity

- Each data file is SHA-256 hashed at generation time.
- Hashes are stored in `manifest/data_hashes.json`:
  ```json
  {
    "nscg_N100000_p005_s0.csv": "sha256:abc123...",
    ...
  }
  ```
- Fitter scoring verifies hashes match before scoring.

---

## 5. Ground-Truth Fields

### 5.1 Ground-truth file

One file per configuration. Format: JSON.

**Filename pattern:**
```
ground_truth/nscg_N{N}_p{p_percent:03d}_s{seed}.truth.json
```

**Schema:**
```json
{
  "spec_version": "B1-v1.0",
  "config": {
    "n": 10,
    "N": 100000,
    "p_noise": 0.05,
    "seed": 0
  },
  "h_true": 7,
  "sigma_true": {
    "1": 2,
    "3": 1,
    "7": 1,
    "9": 2
  },
  "units_true": [1, 3, 7, 9],
  "core_true": [3, 7, 9],
  "S_MAX_true": [[2,4],[4,2],[2,9],[9,2],[4,8],[8,4]],
  "S_ADD_true": [[1,2],[2,1]],
  "S_true": [[1,2],[2,1],[2,4],[4,2],[2,9],[9,2],[4,8],[8,4]],
  "T_true_matrix": [
    [0,0,0,0,0,0,0,7,0,0],
    [0,7,3,7,7,7,7,7,7,7],
    [0,3,7,7,4,7,7,7,7,9],
    [0,7,7,7,7,7,7,7,7,3],
    [0,7,4,7,7,7,7,7,8,7],
    [0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],
    [7,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,8,7,7,7,7,7],
    [0,7,9,3,7,7,7,7,7,7]
  ],
  "data_file": "data/nscg_N100000_p005_s0.csv",
  "data_sha256": "abc123..."
}
```

### 5.2 Sealing protocol

Ground-truth files are written to a `sealed/` directory **after** data generation. The fitter's process does not have read access to `sealed/`. Enforce at the filesystem level (chmod, separate directory outside the fitter's path).

---

## 6. What Is Hidden from the Fitter

**Absolutely hidden:**
- All files in `sealed/` (all `.truth.json` files).
- The noise level $p_{\text{noise}}$ for each data file.
- The identity of any specific ground-truth seam pair.
- The attractor value $h_{\text{true}}$.
- The shell partition labels $\sigma_{\text{true}}$.

**Practically hidden (discoverable in principle but must not be used):**
- The source code of the generator (fitter must not inspect it during fitting).
- Any pre-generated answer key or intermediate computation products.

**Enforcement:**
- Fitter implementation must load only `data/*.csv` files.
- Fitter implementation must not read `sealed/`, `manifest/`, or the source of the generator.
- Compliance is by code review + filesystem sandbox.

---

## 7. What the Fitter Is Allowed to See

**Explicit inputs:**
- The carrier size $n = 10$ (announced; not secret).
- One data file `data/nscg_N{N}_p{p_percent}_s{seed}.csv` at a time.
- General knowledge:
  - The category: finite commutative ring $\mathbb{Z}/n\mathbb{Z}$.
  - The instrument framework: canonical construction $C_0$ + optional seam layers.
  - The rule space: $C_0$ takes $(n, h, \sigma)$ as parameters; layered rules include MAX and ADD mod $n$.
  - Algorithms for computing $v_2$, $\gcd$, etc.

**Must NOT read:**
- The ground-truth file for the current configuration.
- Other configurations' data or ground-truth files.
- Generator source.

**Outputs** (see §8).

---

## 8. Recovery Targets

The fitter must produce, for each data file, an output JSON with the following fields.

### 8.1 Fitter output schema

**Filename pattern:**
```
results/nscg_N{N}_p{p_percent:03d}_s{seed}.fit.json
```

**Schema:**
```json
{
  "spec_version": "B1-v1.0",
  "data_file": "data/nscg_N100000_p005_s0.csv",
  "data_sha256": "abc123...",
  "algorithm_name": "ReferenceInstrumentFitter",
  "algorithm_version": "1.0.0",
  "h_hat": 7,
  "sigma_hat": {
    "1": 2,
    "3": 1,
    "7": 1,
    "9": 2
  },
  "units_hat": [1, 3, 7, 9],
  "core_hat": [3, 7, 9],
  "S_hat": [[1,2],[2,1],[2,4],[4,2],[2,9],[9,2],[4,8],[8,4]],
  "max_domain_hat": [[2,4],[4,2],[2,9],[9,2],[4,8],[8,4]],
  "add_domain_hat": [[1,2],[2,1]],
  "T_hat_matrix": [[...],[...],...]
}
```

**Field requirements:**
- `h_hat`: integer in $\{0, \ldots, 9\}$.
- `sigma_hat`: dict mapping each unit in `units_hat` to a positive integer shell label.
- `units_hat`: list of integers (the fitter's inferred or hardcoded unit set).
- `core_hat`: list, subset of `units_hat`, excluded elements are treated as non-core by the canonical construction.
- `S_hat`: list of ordered pairs [a, b] where $a, b \in \{0, \ldots, 9\}$, the fitter's inferred seam.
- `max_domain_hat`: subset of `S_hat`, pairs classified as following MAX rule.
- `add_domain_hat`: subset of `S_hat`, pairs classified as following ADD rule.
- `T_hat_matrix`: full 10×10 matrix of the fitter's reconstructed operator.

**Consistency requirements:**
- `max_domain_hat` ∪ `add_domain_hat` = `S_hat` (up to listed order).
- `max_domain_hat` ∩ `add_domain_hat` = ∅.
- `T_hat_matrix` must be consistent with the fitter's $(h, \sigma, S, \text{rule classification})$: for each cell, `T_hat_matrix[x][y]` equals $\max(x,y)$ if $(x,y) \in$ `max_domain_hat`; equals $(x+y) \bmod n$ if $(x,y) \in$ `add_domain_hat`; equals $C_0(x,y;h,\sigma)$ otherwise.

Inconsistency produces an automatic FAIL on all metrics.

---

## 9. Exact Scoring Metrics

### 9.1 Metric A — Attractor recovery

$$A_h = \begin{cases} 1 & \text{if } \hat{h} = h_{\text{true}} \\ 0 & \text{else} \end{cases}$$

### 9.2 Metric B — Shell partition recovery (partition + ordering)

Let $\hat{P}$ and $P_{\text{true}}$ be the partitions of $U_{\text{true}}$ induced by $\hat{\sigma}$ and $\sigma_{\text{true}}$ respectively.

$P_{\text{true}} = \{\{3, 7\}, \{1, 9\}\}$.

**Partition match:** $P_{\text{match}} = 1$ if $\hat{P} = P_{\text{true}}$ as set partitions, else 0.

**Ordering match:** $P_{\text{order}} = 1$ if $\hat{\sigma}(3) < \hat{\sigma}(1)$ (lower-shell class is $\{3, 7\}$), else 0.

$$A_\sigma = P_{\text{match}} \cdot P_{\text{order}}$$

### 9.3 Metric C — Seam set recovery

Interpreting $\hat{S}, S_{\text{true}}$ as sets of ordered pairs:

$$R_{\text{seam}} = \frac{|\hat{S} \cap S_{\text{true}}|}{|S_{\text{true}}|} \quad \text{(recall)}$$

$$P_{\text{seam}} = \frac{|\hat{S} \cap S_{\text{true}}|}{|\hat{S}|} \quad \text{(precision; define } = 1 \text{ if } \hat{S} = \emptyset \text{)}$$

$$F_{\text{seam}} = \begin{cases} 0 & \text{if } R_{\text{seam}} = 0 \text{ or } P_{\text{seam}} = 0 \\ \frac{2 \cdot R_{\text{seam}} \cdot P_{\text{seam}}}{R_{\text{seam}} + P_{\text{seam}}} & \text{else} \end{cases}$$

### 9.4 Metric D — Seam rule classification accuracy

For pairs in $\hat{S} \cap S_{\text{true}}$, check whether the fitter correctly classifies them as MAX or ADD.

Let $C_{\text{rule}} = |\{p \in \hat{S} \cap S_{\text{true}} : \text{class}_{\hat{}}(p) = \text{class}_{\text{true}}(p)\}|$.

$$A_{\text{rule}} = \begin{cases} C_{\text{rule}} / |\hat{S} \cap S_{\text{true}}| & \text{if } |\hat{S} \cap S_{\text{true}}| > 0 \\ 0 & \text{else} \end{cases}$$

### 9.5 Metric E — Full operator recovery

$$A_T = \frac{|\{(x, y) \in R \times R : \hat{T}(x, y) = T_{\text{true}}(x, y)\}|}{100}$$

### 9.6 Metric F — Null-comparison $z$-score (informational only)

Generate 1000 random fit outputs by randomly permuting $z$-values across observed $(x, y)$ pairs; refit $C_0$ to each. Record the null distribution of $A_T$. Report:

$$Z = \frac{A_T - \mu_{\text{null}}}{\sigma_{\text{null}}}$$

Used for diagnostic reporting, not for pass/fail.

---

## 10. Pass / Fail Thresholds

### 10.1 Per-configuration pass criteria

A single configuration $(N, p_{\text{noise}}, s)$ **passes** if ALL of:

| Criterion | Low ($p = 0.05$) | Med ($p = 0.15$) | High ($p = 0.30$) |
|---|---|---|---|
| $A_h$ | $= 1$ | $= 1$ | $= 1$ |
| $A_\sigma$ | $= 1$ | $= 1$ | $= 1$ |
| $R_{\text{seam}}$ | $\geq 0.90$ | $\geq 0.80$ | $\geq 0.60$ |
| $P_{\text{seam}}$ | $\geq 0.75$ | $\geq 0.60$ | $\geq 0.50$ |
| $A_{\text{rule}}$ | $= 1.00$ | $\geq 0.90$ | $\geq 0.80$ |
| $A_T$ | $\geq 0.95$ | $\geq 0.88$ | $\geq 0.75$ |

Any violation → configuration FAIL.

### 10.2 Per-noise-level pass criteria

For a given noise level (5 seeds), the benchmark **passes at that noise level** if:
- At least 4 of 5 seeds pass (≥ 80% pass rate).
- Mean $A_T$ across seeds: above the per-config threshold for that noise level.

### 10.3 Overall B1 pass criteria

B1 **passes overall** if ALL of:
- Low-noise pass rate: 5/5 seeds (strict; any low-noise failure is decisive).
- Medium-noise pass rate: $\geq 4/5$ seeds.
- High-noise pass rate: $\geq 3/5$ seeds.

**Any low-noise seed failure is an automatic overall FAIL.** The instrument must recover structure reliably when the signal is 95% clean. Failure at that level means the instrument has a structural defect.

### 10.4 Failure interpretation guide

| Failure pattern | Likely cause |
|---|---|
| Low-noise $A_h$ fail | Fitter's attractor inference broken, or misreads mode |
| Low-noise $A_\sigma$ fail | Fitter's shell computation incorrect or inconsistent with ring |
| Low-noise $R_{\text{seam}}$ fail | Fitter's seam detection threshold wrong; misses real exceptions |
| Low-noise $P_{\text{seam}}$ fail | Fitter over-flags; includes spurious seam entries |
| Low-noise $A_T$ fail with high $A_h, A_\sigma$ | Seam classification error |
| Degradation only at high noise | Expected; instrument is noise-limited |

---

## 11. Anti-Leakage Rules

### 11.1 Process isolation

- **Generation** runs in process A. Writes `data/` and `sealed/`. Exits.
- **Fitting** runs in process B. Reads only `data/`. No network, no access to `sealed/` or generator source. Writes `results/`.
- **Scoring** runs in process C. Reads `data/`, `sealed/`, `results/`. Writes `scores/`.

### 11.2 Directory permissions

- `data/`: readable by processes A, B, C.
- `sealed/`: readable by A (write-only after generation) and C. **Not** readable by B.
- `results/`: writable by B, readable by C.
- `scores/`: writable by C, readable by all.

Implementation: use separate Unix users or containers with appropriate mount points.

### 11.3 Hash verification

Before scoring, C verifies:
- `manifest/data_hashes.json` hash of each data file matches.
- `manifest/sealed_hashes.json` hash of each ground-truth file matches.
- `results/{...}.fit.json.data_sha256` field matches the data file hash.

Hash mismatch → scoring aborts with error.

### 11.4 No iterative feedback

- Fitter runs once per data file.
- No "preview" of scoring results before final submission.
- No hyperparameter tuning based on per-configuration results.

Tuning based on prior B1 runs is permitted only across spec versions (i.e., after the current spec is closed and a v2.0 is cut). Within spec v1.0, no tuning.

### 11.5 Fitter determinism

Fitter must be deterministic given the data file. If the fitter uses randomness, it must be seeded with a fixed value (documented in `algorithm_version`). This ensures reproducibility of reported results.

---

## 12. Minimal Reproducible Run Protocol

### 12.1 Directory structure

```
benchmark_B1/
├── spec/
│   └── B1_v1.0.md                    ← this document
├── generator/
│   └── generate_nscg.py              ← reference generator (no fitter code)
├── data/                             ← CSV files
├── sealed/                           ← ground-truth JSON files (fitter-invisible)
├── manifest/
│   ├── data_hashes.json
│   └── sealed_hashes.json
├── fitter/
│   └── fit_nscg.py                   ← the fitter (to be implemented)
├── results/                          ← fit JSON files
├── scorer/
│   └── score_nscg.py                 ← scoring script
└── scores/                           ← score JSON + summary
```

### 12.2 Step 1 — Generate

```
python generator/generate_nscg.py --spec spec/B1_v1.0.md
```

This produces:
- 15 CSV files in `data/`
- 15 JSON files in `sealed/`
- `manifest/data_hashes.json`
- `manifest/sealed_hashes.json`
- A verification file `manifest/first5_triples.json` listing first 5 triples of configuration `(N=100000, p=0.05, s=0)` for cross-implementation validation.

### 12.3 Step 2 — Seal

```
chmod 000 sealed/*.truth.json
# or move to a separate filesystem/container
```

Verify fitter process cannot read `sealed/`.

### 12.4 Step 3 — Fit

For each of 15 configurations:
```
python fitter/fit_nscg.py --data data/nscg_N{N}_p{p_pct:03d}_s{seed}.csv \
                          --output results/nscg_N{N}_p{p_pct:03d}_s{seed}.fit.json
```

The fitter must not reference `--p-noise`, `--ground-truth`, or any other configuration parameter. Carrier size $n = 10$ is the only externally-specified parameter.

### 12.5 Step 4 — Score

```
python scorer/score_nscg.py --spec spec/B1_v1.0.md
```

This:
- Verifies all hashes.
- Computes per-configuration metrics.
- Writes per-configuration score JSON to `scores/`.
- Writes `scores/B1_summary.json` with aggregate statistics and overall pass/fail verdict.

### 12.6 Step 5 — Report

`scores/B1_summary.json` format:

```json
{
  "spec_version": "B1-v1.0",
  "run_timestamp": "2026-04-17T18:30:00Z",
  "generator_hash": "sha256:...",
  "fitter_name": "ReferenceInstrumentFitter",
  "fitter_version": "1.0.0",
  "per_config": [
    {
      "config_id": "N100000_p005_s0",
      "A_h": 1, "A_sigma": 1,
      "R_seam": 1.0, "P_seam": 1.0, "F_seam": 1.0,
      "A_rule": 1.0, "A_T": 1.0, "Z_null": 10.4,
      "pass": true
    },
    ...
  ],
  "per_noise_level": {
    "low":  {"pass_rate": 5, "total": 5, "pass": true},
    "med":  {"pass_rate": 4, "total": 5, "pass": true},
    "high": {"pass_rate": 3, "total": 5, "pass": true}
  },
  "overall": {
    "low_noise_strict_pass": true,
    "med_noise_pass": true,
    "high_noise_pass": true,
    "verdict": "PASS"
  }
}
```

---

## Appendix A — Reference Generator Sketch (non-normative)

This pseudocode illustrates the generator. The normative spec is §1–§5 above; implementations must match them.

```python
import numpy as np
import pandas as pd
import hashlib
import json

def T_true(x, y):
    # Tower reconstruction
    S_MAX = {(2,4),(4,2),(2,9),(9,2),(4,8),(8,4)}
    S_ADD = {(1,2),(2,1)}
    if (x, y) in S_MAX: return max(x, y)
    if (x, y) in S_ADD: return (x + y) % 10
    # C_0
    h = 7
    if x == 0 or y == 0:
        if (x, y) in {(0, 7), (7, 0)}: return 7
        return 0
    core = {3, 7, 9}
    sigma = {1: 2, 3: 1, 7: 1, 9: 2}
    if x in core and y in core and sigma[x] != sigma[y]:
        return x if sigma[x] < sigma[y] else y
    return 7

def generate(N, p_noise, seed, outpath):
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(N):
        x = int(rng.integers(0, 10))
        y = int(rng.integers(0, 10))
        u = float(rng.random())
        if u < p_noise:
            z = int(rng.integers(0, 10))
        else:
            z = T_true(x, y)
        rows.append((x, y, z))
    df = pd.DataFrame(rows, columns=['x', 'y', 'z'])
    df.to_csv(outpath, index=False)
    with open(outpath, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

# Run for all 15 configurations
configs = [(N, p, s)
           for (N, p) in [(100_000, 0.05), (500_000, 0.15), (1_000_000, 0.30)]
           for s in range(5)]
for N, p, s in configs:
    p_pct = int(p * 100)
    path = f"data/nscg_N{N}_p{p_pct:03d}_s{s}.csv"
    h = generate(N, p, s, path)
    # ... write ground-truth JSON to sealed/
    # ... append hash to manifest
```

---

## Appendix B — Versioning and Change Control

**Version:** B1-v1.0 (this document).

**Frozen on:** date of ClaudeCode handoff.

**Changes require:** new version tag (B1-v2.0), explicit changelog, revalidation of prior results.

**Changelog template:**
- `[v2.0] YYYY-MM-DD — Reason: …`
- `[v1.0] YYYY-MM-DD — Initial release.`

---

## Appendix C — Discipline Reminders

- **No theory expansion.** This spec does not add new claims about TSML/BHML.
- **No interpretation.** Pass/fail is numerical; interpretation happens afterward.
- **No tuning after seeing results.** If v1.0 fails, diagnose the fitter or cut v2.0 and rerun.
- **Benchmark is blind.** Fitter sees data only; scoring happens in a separate process.

**The point of this benchmark is to put the instrument in a position where it either recovers known structure or exposes a specific defect. Both outcomes are acceptable. What is not acceptable is an inconclusive result produced by spec ambiguity.**
