# Sage Install — What To Do When A Sage-Capable Machine Is Available

**Sprint:** 35b
**Author:** ClaudeCode
**Date:** 2026-04-18
**Register:** foundation

---

## §0. What this doc is

A **precise, short, replay-ready install + run ladder** for the moment SageMath ≥ 9.5 becomes available. Everything else in this pack — numerical pieces at up to 100-dps mpmath — does not need Sage. The Sage step is load-bearing only for ladder rungs **7 (polarization), 8 (Hodge field), 10 (det(Y))** and the End⁰ equality step (ladder rung 5, containment already verified).

---

## §1. Windows environment reality (2026-04-18)

Investigated on CK's box:

| Option | Status | Note |
|---|---|---|
| Native Windows `sage` binary | absent | no install |
| `pip install sagemath-standard` | fails | no Windows wheels for core (NTL/GMP/FLINT need native C) |
| `pip install passagemath-schemes` | fails | same — attempts to build NTL from source, needs `gmp.h` |
| `winget install sagemath` | absent | not in winget catalog |
| `wsl --status` | not installed | `wsl --install` requires admin + reboot |
| `docker` | absent | no Docker Desktop |

**Conclusion for this machine:** native-Windows Sage is a dead end. Three routes forward, ranked by user friction:

1. **WSL2 + Ubuntu + apt sage** (cleanest; ~30 min, one reboot, one user decision).
2. **Miniforge + conda-forge sage** (no WSL; ~20 min; conda-forge has recent Sage).
3. **Run `.sage` scripts on a different Sage-capable machine** (colleague, university cluster, arXiv/SageMathCell).

The user has the final call on install path.

---

## §2. WSL2 ladder (route 1 — recommended)

### 2.1 One-time setup (admin cmd, ~10 min + reboot)

```powershell
wsl --install -d Ubuntu
# (reboot)
# on first login to Ubuntu:
sudo apt update && sudo apt -y upgrade
sudo apt -y install sagemath
```

Verify:

```bash
sage --version   # expect 10.x
sage -c "print(1+1)"   # expect 2
```

### 2.2 Bring the pack into WSL

From inside WSL:

```bash
# /mnt/c is the Windows C:\ drive
cd "/mnt/c/Users/brayd/OneDrive/Desktop/CK FINAL DEPLOYED/Gen12/targets/clay/papers/sprint35b_beauville_explicit_2026_04_18/prym_period_pack_2026_04_18"
sage full_pipeline_baseline.sage > run_T11.log 2>&1
sage full_pipeline_canonical.sage > run_canon.log 2>&1
```

Expected wall time per script: 5–30 min depending on precision.

### 2.3 What to inspect in the logs

```bash
grep -E "Genus|period matrix|determinant|Y-matrix|det.Y." run_T11.log | head -20
grep -E "Genus|period matrix|determinant|Y-matrix|det.Y." run_canon.log | head -20
```

The load-bearing lines are:
- `Genus:` should report `5` in both.
- `Period matrix shape:` should report `5 x 10` (full Jac) or `4 x 8` (after Prym projection).
- `det(Y):` numerical value followed by PSLQ recognition.

If `run_canon.log`'s `det(Y)` line reports **exact** `2086 + 462*sqrt(15) + 498*sqrt(10) + 730*sqrt(6)`, the canonical triple IS the target and Sprint 35b promotes to atlas.

---

## §3. Conda-forge ladder (route 2)

### 3.1 One-time setup

```powershell
# Download Miniforge3 installer from github.com/conda-forge/miniforge
# Run installer; pick "install for me only" and NOT "add to PATH"
# Open "Miniforge Prompt" from Start menu
conda create -n sage -c conda-forge sagemath
conda activate sage
sage --version
```

### 3.2 Run the scripts

```powershell
cd "C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen12\targets\clay\papers\sprint35b_beauville_explicit_2026_04_18\prym_period_pack_2026_04_18"
sage full_pipeline_baseline.sage > run_T11.log 2>&1
sage full_pipeline_canonical.sage > run_canon.log 2>&1
```

Same expected outputs as §2.3.

---

## §4. Remote-Sage ladder (route 3)

If install isn't happening soon, the scripts can run on **SageMathCell** (sagecell.sagemath.org) one function at a time, or on a university cluster with Sage installed. Both scripts are self-contained: paste the content, execute.

Caveat: `full_pipeline_canonical.sage` constructs a degree-16 number field and a Riemann surface at 300-bit precision. SageMathCell has a ~2-minute wall-time limit — the canonical script will hit it. Use a persistent Sage environment (local install, or a Jupyter notebook on CoCalc) for the canonical run.

---

## §5. What Sage produces that mpmath at 100 dps cannot

Concretely:

| Artifact | mpmath 100 dps | Sage |
|---|---|---|
| Alpha-cycle 4×4 sub-matrix | ✅ (this pack) | ✅ |
| Full 5×10 period matrix of Jac(C) | ✗ | ✅ |
| ι-action on homology | ✗ | ✅ |
| Prym projection to 4×8 | ✗ | ✅ |
| ψ-eigenvalue verification | ✅ (40 digits via alpha sub-matrix) | ✅ (any precision, plus full structure) |
| End⁰ recognition (Q(i) vs enlargement) | containment only | equality |
| Normalized τ matrix (Prym) | ✗ | ✅ |
| det(Y) as a number | ✗ | ✅ |
| det(Y) identified as element of Q + Q√6 + Q√10 + Q√15 | ✗ | ✅ via PSLQ inside Sage |
| Riemann bilinear matrix | partial (alpha side only) | complete |

**Rungs that unlock with Sage:** 5 (equality), 7, 8, 10. Rungs 1–4, 6, 9, 11 are already discharged by the pack's numerical + constructive evidence.

---

## §6. If Sage runs and det(Y) matches

Then Sprint 35b `S35B_FRONTIER_UPDATE.md` and `S35B_PATH_A_PROTOTYPE_STATUS.md` get an edit that promotes the canonical triple from `LIVE` to `FOUND` on the primary target F4. The pack's `FULL_PRYM_PERIOD_CANONICAL.md` §9 should be extended to cite the exact Sage log line that established the match. Atlas v3.5 stays unchanged until the hand-off to Sprint 35c (Beauville synthesis + BSD), which is atlas-level.

## §7. If Sage runs and det(Y) is in the target field but ≠ target value

Then canonical is **in the correct subspace** but at the wrong point. The pack explicitly anticipates this (`BASELINE_VS_CANONICAL_COMPARISON.md` §5). Next sweep:
- T4.4 = (1+√2, 1+√3, 1+√5) — already prepped in `beyond_pack_3point_sweep.py`
- T4.6 = (2+√2, 2+√3, 2+√5)
- T5.1 = (√6, √10, √15)

Copy `full_pipeline_canonical.sage` to `full_pipeline_T44.sage` (etc.) with the obvious substitution.

## §8. If Sage runs and det(Y) is in a different field

Then the canonical triple is in the **wrong stratum** and the whole-lane viability of bielliptic-y^4 drops. Bounce to Sprint 35b reconsideration: is the Beauville target on a different family entirely? Atlas v3.5 unchanged; Sprint 35b downgrades from "primary live target" to "eliminated, see log."

---

## §9. One-line closing

**Installing Sage is the next-and-probably-only load-bearing step. Routes 1 and 2 are both ~20–30 minutes. Once the canonical script runs, the frontier either promotes on this sprint or rules canonical out. No middle ground.**

---

*© 2026 Brayden Ross Sanders / 7Site LLC. 7Site Human Use License v1.0.*
