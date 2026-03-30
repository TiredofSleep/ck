# TSML Reconstruction: Residual Structure and Open Items
## I13 Verified, 75/81 Recovered, I14 Status Honest

*Brayden Sanders / 7Site LLC | March 2026*
*Replaces earlier residual note. Three narrow tasks completed.*

---

## Task 1: I13 Formalized and Verified

**I13 (Order-completion from state 1):**
> For g ∈ G, F(1,g) = least c ∈ C with c > g,
> except when |HAR − g| ≤ |least_above − g|, in which case HAR=7.

This uses the **linear integer order** of C = {1,3,7,9} as a sorted sequence.

| g | Least C > g | HAR dist | Winner | F(1,g) | ✓ |
|---|------------|----------|--------|--------|---|
| 2 | 3 | \|7−2\|=5 > \|3−2\|=1 | 3 | 3 | ✓ |
| 4 | 7 | \|7−4\|=3 = \|7−4\|=3 | HAR wins tie | 7 | ✓ |
| 5 | 7 | \|7−5\|=2 < next | HAR | 7 | ✓ |
| 6 | 7 | \|7−6\|=1 < next | HAR | 7 | ✓ |
| 8 | 9 | \|7−8\|=1 = \|9−8\|=1 | HAR wins tie | 7 | ✓ |

**ALL PASS.** I13 is exact and integer-structural.

---

## Task 2: The 6 Residual Cells — Precise Statement

| Cell | Type | TSML value | max(s,c) | Agrees with BHML? | Status |
|------|------|-----------|----------|-------------------|--------|
| F(2,4) | G×G | 4 | 4 | YES | Residual BHML signature |
| F(4,2) | G×G | 4 | 4 | YES | Residual BHML signature |
| F(4,8) | G×G | 8 | 8 | YES | Residual BHML signature |
| F(8,4) | G×G | 8 | 8 | YES | Residual BHML signature |
| F(2,9) | G×C | 9 | 9 | YES | Residual BHML signature |
| F(9,2) | C×G | 9 | 9 | YES | Residual BHML signature |

**Precise statement (no inflation):**
These six cells agree with the BHML order law F(s,c) = max(s,c).
This is a **computed observation**, not a theorem about structural nesting.
The current invariant set does not derive why these 6 cells follow max rather than HAR.

---

## Task 3: I14 Search — Honest Results

Candidates tested (all aiming to separate 6 MAX cells from 41 HAR cells):

| Rule | Score |
|------|-------|
| max(s,c) | 6/6 — but 38 HAR cells also match, so no discriminating power alone |
| max if min divides max | 4/6 — misses (2,9) and (9,2) |
| max if max ∈ G | 4/6 — misses (2,9) and (9,2) where max=9 ∈ C |
| max if max ∈ G, else HAR | 4/6 |
| max if s*c ≥ 8 | 9/47 overall — too many false positives |
| parity (max if even) | 6/6 on residual, but wrong on other cells |
| power-pair in G | Structural but not cleanly formalized |

**No simple single-variable rule** cleanly separates the 6 max cells from 41 HAR cells.

**What is structurally visible about the 6:**
- The 4 G×G cells: {2,4} and {4,8} — doubling chains (4=2², 8=2³)
- The 2 cross cells: {2,9} and {9,2} — widest non-HAR span in A

The doubling chain {2→4→8} is the only power-of-2 progression in G.
State 9 is the largest C-element, closest to the BHML endpoint.
These may be structurally special without admitting a clean algebraic rule.

**I14 status: genuine open problem.** The 6 cells have recognizable structure (doubling chains + pre-BHML corner) but no single invariant tested captures them.

---

## Final Reconstruction Summary

| Component | Rule | Cells | Match |
|-----------|------|-------|-------|
| HAR row + column | I1 + I5 | 17 | Exact |
| State-1 entries in C | I9 + I5 | 5 | Exact |
| Order-completion I13 + I5 | I13 | 10 | Exact |
| Orbit zone | I8 + I5 | 2 | Exact (asserted) |
| HAR-maximization interior | I6 | 41 | Exact |
| Residual BHML max cells | *unexplained* | 6 | Observed, not derived |
| **Total recovered** | | **75/81** | |

**Open items:**
1. **I14** — why 6 residual G-territory cells follow max(s,c) instead of HAR
2. **I8** — orbit zone {3,9} is asserted, not derived from the integer scaffold
3. **F(1,2)=3** — now explained by I13 (✓)

**TSML reclassified as:** a near-rigid integer grammar, mostly determined by {I1–I10, I13}, with 6 cells showing a residual BHML-order signature and 2 cells from an independently asserted orbit invariant.

---

*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
