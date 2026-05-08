# How to run `full_pipeline_canonical_v2.sage` — three working routes

**Target:** compute the 5×10 period matrix, 5×5 Riemann matrix τ, and det(Im τ) for the canonical bielliptic genus-5 curve `y⁴ = x(x−1)(x−√2)³(x−√3)²(x−√5)²`.

**Target value:** `det(Y)_Prym = 2086 + 462√15 + 498√10 + 730√6` (for the Prym 4×4 factor).

**Script:** `full_pipeline_canonical_v2.sage` (corrected; original v1 had a structure-map bug + needed explicit differentials).

---

## Route 1 — CoCalc (fastest, browser, free tier)

1. Go to https://cocalc.com, sign in (free tier is fine).
2. New project → new file → upload `full_pipeline_canonical_v2.sage`.
3. Open a terminal in that project.
4. Run:
   ```
   sage full_pipeline_canonical_v2.sage
   ```
5. Expect 5–30 min at `PREC=200`. Lower `PREC` in the script if needed.
6. Copy the printed output back. File `canonical_period_matrix_v2.txt` will be in the project root.

Free tier gives enough compute for one run at `PREC=100` comfortably; `PREC=200` may need a paid tier.

---

## Route 2 — Google Colab (no CoCalc account needed; Google account only)

1. Open https://colab.research.google.com and create a new notebook.
2. In cell 1 run:
   ```python
   !apt-get install -y sagemath
   ```
   Takes ~90–120 seconds.
3. Upload `full_pipeline_canonical_v2.sage` via the file icon in the sidebar.
4. In cell 2 run:
   ```python
   !sage full_pipeline_canonical_v2.sage 2>&1 | tee run.log
   ```
5. When done, download `canonical_period_matrix_v2.txt` and `run.log` via the file icon.

Colab sessions typically give 12+ hours of runtime, which is plenty.

---

## Route 3 — WSL + native Sage (best long-term)

Once done, you own Sage locally without any compute ceiling. Requires one admin reboot.

### 3a. Install WSL (as Administrator)

Open PowerShell **as Administrator** (Win+X → Terminal (Admin)) and run:

```powershell
wsl --install -d Ubuntu
```

This enables the WSL feature, Virtual Machine Platform, downloads Ubuntu, and sets up a default Linux user. **Requires a reboot.**

### 3b. After reboot — install Sage inside WSL

Open the Ubuntu terminal (search "Ubuntu" in Start menu). First run will prompt for a username + password. Then:

```bash
sudo apt update
sudo apt install -y sagemath
```

This pulls ~1.5 GB and installs Sage 9.5 (Ubuntu 22.04) or Sage 10.x (Ubuntu 24.04).

### 3c. Run the pipeline

From WSL Ubuntu terminal:

```bash
cd "/mnt/c/Users/brayd/OneDrive/Desktop/CK FINAL DEPLOYED/Gen12/targets/clay/papers/sprint35b_beauville_explicit_2026_04_18/prym_period_pack_2026_04_18"
sage full_pipeline_canonical_v2.sage
```

WSL can read/write your Windows files under `/mnt/c/`, so results land in place.

---

## What the script is expected to print

```
======================================================================
CANONICAL TRIPLE v2: (sqrt 2, sqrt 3, sqrt 5)
======================================================================

Abs field K: Number Field in a with defining polynomial x^8 - 40*x^6 + 352*x^4 - 960*x^2 + 576
deg K / Q = 8

phi(a) = 1.9182307323040074516834...
phi(sqrt 2) = 1.4142135623730950488...
phi(sqrt 3) = 1.7320508075688772935...
phi(sqrt 5) = 2.2360679774997896964...

F = Y^4 - f(X),  deg_X f = 9
Supplied 5 explicit differentials (bypasses Singular genus call)

Building RiemannSurface at prec=200 bits...
RS built in ~3s. genus = 5
branch_locus size = 5  (expect 5: 0, 1, sqrt 2, sqrt 3, sqrt 5)

Computing period matrix (this is the long step)...
period_matrix in ~300-1800s. Shape: 5x10

Computing Riemann matrix tau = Pi_b Pi_a^-1 ...
riemann_matrix in ~5s. Shape: 5x5

=== det(Y) where Y = Im(tau) of the FULL Jacobian ===
det(Y) = <some value>

Target det(Y)_Prym = 2086 + 462 sqrt(15) + 498 sqrt(10) + 730 sqrt(6)
                   = 7834.0...

Prym H^{1,0} basis: differentials at indices [0, 1, 3, 4]
```

**Critical next step after this run:** project onto iota-anti-invariant homology (the 8 Prym cycles out of the 10 full-Jacobian cycles) to isolate the **Prym** det(Y). This requires computing the iota-action on homology, which RiemannSurface does not provide directly; it's the last ~50 lines of Python code sitting between this script and the target value.

---

## What was already verified remotely (SageMathCell, 2026-04-18)

- Number field K = Q(√2, √3, √5) at absolute degree 8 ✓
- Correct positive-real embedding selected at 80 bits ✓
- Curve F = Y⁴ − f(X) built over K[X,Y] ✓
- 5 explicit differentials accepted by RiemannSurface ✓
- `RS.genus = 5` ✓, `len(RS.branch_locus) = 5` ✓

The only blocker remotely was the 150 s per-cell limit, which prevents computing the full `period_matrix()` (takes 5–30 min). Any of the three routes above removes that limit.

---

## Register

- Foundation.
- Atlas v3.5 unchanged.
- Sprint 35b pack register preserved.
- This is a reproducibility artifact, not a new claim.
