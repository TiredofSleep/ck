# Verification 2026-04-21 — funding/physics-sim-edu

**Branch:** `funding/physics-sim-edu`
**Archive:** `Gen13/targets/funding_physics_sim_edu/archive_crystal_lattice_matrix/`
**Verifier:** Brayden Sanders (with Claude assist)
**Environment:** Windows 11 — **no JavaScript runtime installed** (no `node`, `bun`, `deno`, `npm`).

---

## Status — source audit only

`test_engine_v2.js` was **not executed** in this verification cycle. The Windows environment has no JS runtime. Since installing a runtime is out of scope for this commit (policy: do not install system packages without user confirmation), this document records a **source-level audit** and cross-references the **committed `test_results.txt`** that was produced by a prior run of the same file.

To reproduce today, one of the following must be installed first:
- Node.js ≥ 18 (`winget install OpenJS.NodeJS.LTS`)
- Bun (`winget install Oven-sh.Bun` or `npm install -g bun`)
- Deno (`winget install DenoLand.Deno`)

Then: `node test_engine_v2.js > verifications_2026_04_21/test_engine_v2_stdout.txt`.

---

## Files audited

| File | LOC | Working-tree md5 (Windows CRLF) |
|---|---|---|
| `test_engine_v2.js` | 458 | `38f1774ea749f83c782d028352bb92fa` |
| `test_results.txt` | 91 | `12bcaf978c2e5704dd84370e9fa40777` |
| `crystal_bug_v1_matrix.jsx` | — | React UI (visualizer, not a test harness) |

Both are tracked under commit `5de8bbe funding/physics-sim-edu: pull Crystal-Lattice-Matrix-MYTHDRIFT into archive_crystal_lattice_matrix/`.

---

## Source structure — what `test_engine_v2.js` defines

### Engine
- `class Q(a, b, c)` — quadratic operator with `ev`, `D` (discriminant), `d1`, `d2`, `vx`, `vy`, `roots`, `fp` (fixed-point).
- 7 bands: VOID, QUANTUM, ATOMIC, MOLECULR (sic — 8-char column cap), CELLULAR, ORGANIC, CRYSTAL.
- `classify(O, x0=0.5)` — runs 28-step orbit, classifies into band by escape/convergence pattern.
- `mkCell(col, row)` — seeds each of `COLS × ROWS = 18 × 14 = 252` cells with (a, b, c) from radial/angular coordinates to spread across all 7 bands.
- `wireNeighbors(cells)` — ranks neighbors by root-distance (not grid adjacency).
- `advSpine(spine, ph, tick)` — advances 10-step phase (T* = 0.714 target per cell).
- `modCells(cells, spine, ph, tick)` — applies spine coefficient modulation.
- `reclassify(cells)` — every 12 ticks, re-bands cells.
- Two bug classes: `OldBug` (broken energy model, E decrements uniformly) vs `NewBug` (Δ-dependent cost).

### Test suite (9 tests in this copy)

| Test | Asserts | Success criterion |
|---|---|---|
| TEST 1 — Initial lattice | cell distribution across 7 bands seeded by `mkCell` | all 7 bands populated; stable FPs > 50 % |
| TEST 2 — Energy honesty | OLD flat-cost bug vs NEW Δ-dependent bug at E0 ∈ {3, 10, 25, 50} | NEW bug's `steps` / `uniq` / `rr` scale with E0; OLD does not |
| TEST 3 — Revisit ratio over time | rr trajectory for NEW bug | rr converges > 1.5 as visits accumulate |
| TEST 4 — Audit mode | 100 % coverage of 252 cells at E0 ∈ {25, 50, 100} | 252/252 in ≤ 300 steps |
| TEST 5 — Band stability | band distribution across 20 epochs | gradual QUANTUM→ATOMIC drift, Δ_avg decreases |
| TEST 6 — Δ-dependent cost | click / free / bound zone cost ratios | click ≈ 5× free |
| TEST 7 — Root-proximity | root-priority vs grid-priority neighbor lists | differ for ≥ 99 % of cells |
| TEST 8 — Bug vs audit | bug-mode coverage vs audit-mode coverage at E0=50 | audit=100 %, bug < 60 % |
| TEST 9 — Performance | 20,000 ticks throughput | ≥ 120 ticks/sec (60 fps × 2) |

*(The `funding/coherence-router` copy of the same filename has **one additional test** — TEST 10: CODEC collapse/expand round-trip fidelity. That test is absent here. See the separate `test_engine_v2.js` divergence note below.)*

---

## Committed prior-run results — what `test_results.txt` shows

The committed output file matches the 9-test structure above and reports:

| Test | Recorded pass evidence |
|---|---|
| 1 | 7 bands populated (VOID 0 %, QUANTUM 23.0 %, …, CRYSTAL 34.5 %); stable FPs 54.4 %; Δ range [−2.633, 13.016]. |
| 2 | NEW bug at E0=50: 1108 steps, 143 unique (56.7 % coverage); OLD flat at 50/25/0.50 regardless of E0. **Energy honesty asserted.** |
| 3 | NEW rr converges to 1.814 over 555 steps (vs OLD locked at 0.500). **Revisit scaling asserted.** |
| 4 | 252/252 (100.0 %) at E0 ∈ {25, 50, 100}. **Audit coverage asserted.** |
| 5 | Band drift QUAN 158 → 119 and ATOM 43 → 65 across 20 epochs, click zone 36 → 48; Δ_avg 1.164 → 0.774. **Stability + drift asserted.** |
| 6 | click/free cost ratio 5.1×. **Δ-dependent cost asserted.** |
| 7 | 251/252 (99.6 %) cells have root-priority ≠ grid-priority. **Root-proximity asserted.** |
| 8 | audit 252/252 in 253 steps; bug 130/252 in 1072 steps. **Audit mode dominates bug mode.** |
| 9 | 20,000 ticks in 347 ms = 57,637 ticks/sec, 480× headroom over 120 tps target. **Performance asserted.** |

Every success criterion listed above is met by the recorded output. No failures recorded.

---

## Two copies, one filename — divergence note

`test_engine_v2.js` exists on two funding branches with different SHAs:

| Branch | LOC | Last test | Working-tree md5 (Windows) |
|---|---|---|---|
| `funding/physics-sim-edu` (this one) | 458 | TEST 9 | `38f1774ea749f83c782d028352bb92fa` |
| `funding/coherence-router` | 530 | TEST 10 (codec) | `aaa951ea256a6ed6ce7914b28af8516d` |

The coherence-router copy is a superset — same 9 tests plus a 10th test for codec collapse/expand round-trip fidelity. Neither file overrides the other; each lives in its own archive folder. Recording both as "the same file under different names" is intentional per never-delete.

---

## Reproduction (when a JS runtime becomes available)

```bash
# Install one of:
winget install OpenJS.NodeJS.LTS          # Node.js
# or
winget install Oven-sh.Bun                 # Bun
# or
winget install DenoLand.Deno               # Deno

# Then from this directory:
cd Gen13/targets/funding_physics_sim_edu/archive_crystal_lattice_matrix/
node test_engine_v2.js | tee verifications_2026_04_21/test_engine_v2_stdout.txt
# Compare against test_results.txt:
diff verifications_2026_04_21/test_engine_v2_stdout.txt test_results.txt
```

`test_results.txt` was produced by an earlier run of this same file. A fresh run should match TEST 1–9 byte-for-byte except the TEST 9 `ms` / `ticks/sec` numbers (hardware-dependent).

---

## Honest summary

- **No re-run happened today.** The environment lacks Node/Bun/Deno.
- **Prior verification exists and is committed.** `test_results.txt` shows all 9 tests reporting the intended values; no failures recorded.
- **The archive is preserved per never-delete.** `test_engine_v2.js` + `test_results.txt` + `crystal_bug_v1_matrix.jsx` + PDFs + spec stand as the funding/physics-sim-edu evidence pack.
- **Next step:** install a JS runtime, re-run, commit the new stdout alongside `test_results.txt` under a `verifications_YYYY_MM_DD/` folder. The directory convention is established; only the runtime is missing.
