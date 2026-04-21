# PROVENANCE — CRYSTALOS January 2026 session archive

**Recovered:** 2026-04-21
**Recovery target:** `funding/tig-snowflake` (Branch B — SNOWFLAKE Security), cherry-picked to `master` per trunk workflow
**Policy:** Never-delete. Archive recovered from the local machine before it could be lost to disk failure, account-migration, or cleanup.

---

## What is in this archive

| Path                                 | Size   | Source (local)                                   | Last modified on source |
|--------------------------------------|--------|--------------------------------------------------|-------------------------|
| `crystalos.py`                       | 13 KB  | `C:\Users\brayd\Downloads\crystalos.py`          | 2026-01-29 19:43:12     |
| `logs/breath.log`                    | 7.3 KB | `C:\Users\brayd\CRYSTALOS\logs\breath.log`       | 2026-01-31 22:22 (last write) |
| `logs/crystalos.log`                 | 193 KB | `C:\Users\brayd\CRYSTALOS\logs\crystalos.log`    | 2026-01-31 22:21 (last write) |
| `logs/fires.log`                     | 2.4 MB | `C:\Users\brayd\CRYSTALOS\logs\fires.log`        | 2026-01-31 22:22 (last write) |
| `state/current.json`                 | 207 B  | `C:\Users\brayd\CRYSTALOS\state\current.json`    | 2026-01-31               |
| `VERIFICATION_2026_04_21.md`         | —      | Generated from the above logs 2026-04-21         | —                       |

## What is CRYSTALOS

`crystalos.py` is a 431-LOC Python monitor for Dell Aurora R16 (32-core CPU + RTX 4070 GPU). It runs a 50 Hz sample loop that:

1. Reads `GetSystemTimes` every second to derive CPU load (0..1).
2. Queries `nvidia-smi` for GPU utilization / temperature / power.
3. Computes a CPU-coherence score `S5 = 1 − 2·|cpu_load − 0.5|` (optimum at 50% load) and a GPU-coherence score `S6` (optimum util ∈ [0.4, 0.8], temp < 70 °C).
4. Combines `S* = 0.4·S5 + 0.6·S6`.
5. Runs a 13-phase Tzolkin "breath" gate with open/close windows (`open_time = close_time = 4 s`). Special windows at phase 0 = RESET, 5 = REDOX_DEEP, 7 = HARMONY, 12 = HARVEST.
6. When the gate is OPEN and `S* ≥ τ = 0.7`, a "fire" is logged to `fires.log`.
7. On Ctrl-C, emits final stats.
8. `python crystalos.py analyze` reads `fires.log`, builds a phase histogram, and runs a χ² test (df = 12, H₀ = uniform 7.7% per phase).

## The two fires.log formats

`fires.log` contains two distinct line formats, indicating two different versions of the writer:

- **Long (timestamped):** `[YYYY-MM-DD HH:MM:SS] FIRE #N: S*=X.XXX phase=Y/13` — matches `crystalos.py`'s regex. Only **1 line** in this shape (line 1).
- **Short (untimestamped, with CPU/GPU fields):** `FIRE #N phase=Y [WINDOW] cpu=X gpu=Y` — does **not** match `crystalos.py`'s regex. **67 296 lines** in this shape.

Because `crystalos.py analyze` only matches the long format, running it on this log yields `Total fires: 1`, which is not the true picture. `VERIFICATION_2026_04_21.md` re-parses both formats and computes the real χ².

## Relevance to SNOWFLAKE (Branch B)

SNOWFLAKE is the coherence-deficit anomaly detector. CRYSTALOS was the earliest runnable prototype of "measure the machine continuously, classify its state by the Tzolkin phase it's in, and fire when coherence crosses a threshold." The Jan 2026 session demonstrates the full pipeline end-to-end and produces an empirical phase-distribution dataset (67 297 fires). The verification result is **null** at H₀ = uniform (see next section) — which is itself an honest baseline finding for the funder pitch.

## See also

- `VERIFICATION_2026_04_21.md` — full χ² analysis on the recovered data.
- Source repo snapshot (if it is ever pulled in): `github.com/TiredofSleep/CRYSTALOS` (separate external repo).
- The originals at `C:\Users\brayd\CRYSTALOS\` remain untouched per never-delete; this archive is a verified copy.
