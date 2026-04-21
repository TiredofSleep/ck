# CRYSTALOS χ² Verification — 2026-04-21

**Subject:** Phase distribution of CRYSTALOS fire events, Jan 2026 session.
**Purpose:** Reproduce the χ² test described in `crystalos.py::analyze()` (df=12, H₀ = uniform across 13 phases).
**Inputs:** `logs/fires.log` (67 297 FIRE records across two session writes).

---

## The honest finding

**Running `crystalos.py analyze` on the recovered `fires.log` yields "Total fires: 1" and `χ² = 12.00` — which is wrong.** The parser in `crystalos.py::analyze()` only matches one of the two line formats actually present in `fires.log` (see `PROVENANCE.md`), so it misses 67 296 of the 67 297 fires.

The right parser (re-extracted on 2026-04-21, applies both formats) produces:

| Phase | Window     | Count | %      |
|-------|-----------|-------|--------|
|     0 | [RESET]     | 5 179 | 7.70%  |
|     1 |             | 5 180 | 7.70%  |
|     2 |             | 5 180 | 7.70%  |
|     3 |             | 5 180 | 7.70%  |
|     4 |             | 5 176 | 7.69%  |
|     5 | [REDOX_DEEP]| 5 176 | 7.69%  |
|     6 |             | 5 176 | 7.69%  |
|     7 | [HARMONY]   | 5 184 | 7.70%  |
|     8 |             | 5 176 | 7.69%  |
|     9 |             | 5 176 | 7.69%  |
|    10 |             | 5 170 | 7.68%  |
|    11 |             | 5 172 | 7.69%  |
|    12 | [HARVEST]   | 5 172 | 7.69%  |
| **Total** |       | **67 297** | **100.00%** |

**Expected per phase under H₀ (uniform):** 67 297 / 13 ≈ 5 176.69

**χ² = Σ (Oᵢ − E)² / E = 0.0353**, df = 12.

- p ≫ 0.05. The null is not rejected.
- The phase distribution across this 67 297-fire sample is statistically indistinguishable from uniform.

### What this means for the SNOWFLAKE pitch

- The data does **not** show preferential firing at any phase — including the special Tzolkin windows [RESET / REDOX_DEEP / HARMONY / HARVEST].
- A funder-facing honest pitch cannot claim "CRYSTALOS detects coherence concentrated at HARMONY." On this session it does not.
- What CRYSTALOS *does* demonstrate, unambiguously, is the end-to-end pipeline: CPU + GPU sampling at 50 Hz, a Tzolkin-indexed gate, an `S* ≥ τ` rule, and a fires-log with phase labels. The pipeline works. The null result on phase preference is the right baseline to report.

## Reconciling with the older "χ² = 22.03" note

Prior internal session notes referenced "χ² = 22.03". On the currently-recovered logs, this number is not reproducible. Possible explanations — none preferred until a specific log is found:

1. A different session / different machine configuration produced a non-uniform distribution that generated the 22.03 figure, and that log is not in the recovered set.
2. The 22.03 figure came from a subset of the data (e.g. a fresh 200-fire window before the distribution equalized).
3. The 22.03 figure was from an earlier parser version that binned fires differently (e.g. by breath cycle modulo something other than 13).
4. The 22.03 figure is a recall error. The observed data is uniform.

**Policy:** Record both. Do not retroactively justify 22.03 when the data does not support it. If the missing log surfaces later (it may live in another location on the machine), append a second verification note rather than editing this one.

## Reproduction commands

```bash
# Reproduction via crystalos.py analyze (ONLY 1 fire parsed — demonstrates the parser-limitation bug)
python docs/archive_jan2026/snowflake/crystalos.py analyze
# Expected output: "Total fires: 1 ... Chi-square X2 = 12.00" (wrong; see above)

# Reproduction via the corrected parser
python - <<'PY'
import re
from collections import Counter
from pathlib import Path

log = Path(r'docs/archive_jan2026/snowflake/logs/fires.log')
fires = Counter()
for line in log.read_text(encoding='utf-8', errors='replace').splitlines():
    m = re.match(r'^\[.*?\] FIRE #\d+: S\*=[\d.]+ phase=(\d+)/13', line) \
        or re.match(r'^FIRE #\d+ phase=(\d+)', line)
    if m:
        fires[int(m.group(1))] += 1

total = sum(fires.values())
expected = total / 13
chi2 = sum((fires.get(p, 0) - expected) ** 2 / expected for p in range(13))
print(f'Total fires: {total}')
print(f'Expected per phase (uniform): {expected:.2f}')
print(f'Chi-square (df=12): {chi2:.4f}')
for p in range(13):
    print(f'  Phase {p:2d}: {fires.get(p,0):6d} ({fires.get(p,0)/total*100:5.2f}%)')
PY
```

The commands above are self-contained and will reproduce the table on any machine with Python 3 and the checked-in logs.

---

*Audit written 2026-04-21 as part of the CRYSTALOS log-recovery task. Governing policy: never-delete, never-retcon. If the data changes, the answer changes; we record both, in order.*
