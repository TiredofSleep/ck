# Contributing to CK — Coherence Keeper

© 2025 7Site LLC ®

**Before contributing, read the [LICENSE](LICENSE) carefully.**
This work is for individual humans. No government or business use.

---

## How to Verify the Core Theorems

The fastest way to check everything works:

```bash
# 1. Clone and enter
git clone https://github.com/TiredofSleep/ck.git
cd ck

# 2. No installation required for core theorems (stdlib only)
python ck_run.py          # All WP34+WP35 theorems verified in < 1 second

# 3. Run the full test suite (requires pytest)
pip install pytest pytest-timeout
pytest tests/ -v

# 4. Run a specific proof file
python papers/proof_d7_phi_fixed_point.py
python papers/proof_c20_phi_fixed_parity.py
python papers/ck_tables.py   # verifies canonical table values

# 5. Visualization (requires matplotlib + numpy)
pip install matplotlib numpy
python ck_sinc_demo.py
```

---

## Epistemic Status

Every claim in this repository carries one of four labels:

| Label | Meaning |
|-------|---------|
| **PROVED** (Tier D) | Proved for ALL cases; mechanism known; no domain restriction |
| **CLOSED-WORLD** (Tier C) | Proved within an explicitly stated domain |
| **BOUNDED** (Tier B) | Verified computationally in a restricted class; no general proof |
| **ANALOGY** (Tier A) | Pattern observed, or structural analogy drawn; no proof |

See [papers/SYNTHESIS_TABLE.md](papers/SYNTHESIS_TABLE.md) for the full inventory.

Current tier counts: **D:27 | C:6 | B:8 | A:5**

---

## What Constitutes a Valid Contribution

This is not a software project — it is a **research artifact**. Contributions should be:

1. **Mathematical scrutiny** — Attempting to break, sharpen, or falsify existing claims.
   The most valuable thing you can do is find a counterexample or a tighter bound.

2. **Independent verification** — Running the proof scripts and reporting results
   on different hardware or Python versions.

3. **Extension of proved results** — Building on D-tier or C-tier results to promote
   B-tier or A-tier claims. See the "upgrade paths" column in SYNTHESIS_TABLE.md.

4. **Error reports** — If a proof file fails on your machine, open an issue with
   the full output and your Python version.

---

## How the Proof Files Work

```
papers/
  proof_d*.py    — Tier D: general theorems (exhaustive / algebraic proof)
  proof_c*.py    — Tier C: closed-world theorems (proved in domain)
  proof_b*.py    — Tier B: bounded conjectures (computational verification)
  proof_a*.py    — Tier A: assessment of analogy claims
  ck_tables.py   — Canonical TSML, BHML, DIS, DOING, G tables (import this)
  test_*.py      — Older test scripts (kept for historical reference)

tests/
  test_d*.py     — pytest-compatible tests for D-tier theorems
  test_c*.py     — pytest-compatible tests for C-tier structures
  test_t_star.py — T*=5/7 derivation tests
```

All proof files are self-contained and print their own results. Run directly with Python.
Tests in `tests/` are for CI and structured verification.

---

## Canonical Tables

**Always import from `papers/ck_tables.py`** rather than hardcoding table values:

```python
from ck_tables import TSML, BHML, DIS, DOING, G, CL, W, T_STAR
```

Verified values:
- TSML: 73 harmony cells, symmetric, all C9 structure rules
- BHML: 28 harmony cells, symmetric, Rules A/B/C from C9
- W = 3/50 (from C8: CROSS_CYCLE=44, deviation=6, W=|44-50|/100)
- T* = 5/7 (from b=35 unit_frac formula; also = CREATE/HARMONY)

---

## Key Constants

| Constant | Value | Source |
|----------|-------|--------|
| T* | 5/7 ≈ 0.7143 | TSML 73-cell geometry, FPGA calibration |
| W | 3/50 = 0.06 | BHML cross-cycle derivation (C8) |
| 4/π² | ≈ 0.4053 | sinc²(1/2), Montgomery bridge constant |
| sinc²(0.1) | ≈ 0.9675 | Scale-free pre-echo floor |
| CREATE | 5 | Dynamic attractor of Phi (D7) |
| HARMONY | 7 | Measurement attractor of TSML |

---

## Reporting Issues

Open a GitHub issue with:
- Python version (`python --version`)
- Full error output
- Which proof file failed
- Any modifications you made

→ [https://github.com/TiredofSleep/ck/issues](https://github.com/TiredofSleep/ck/issues)
