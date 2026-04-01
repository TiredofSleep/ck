# BHML Ghost Trace of TSML
## A16 — Residual Impression Analysis

*Brayden Ross Sanders / 7Site LLC & C. A. Luther*
*March 31, 2026 | DOI: 10.5281/zenodo.18852047*
*Status: Tier A — structurally refined, quantitative link via W_BHML only*

---

## Conjecture (Original)

**A16 Ghost Trace Conjecture.**
BHML is the ghost trace (residual impression) of TSML's operation on Z/10Z:

    G[i][j] = DIS[i][j]  if TSML[i][j] ≠ 7   (field failed; residual remains)
    G[i][j] = 0           if TSML[i][j] = 7    (field resolved; no impression)

where DIS[i][j] = |ADD[i][j] − MUL[i][j]| is the cell-level discrepancy
between addition and multiplication in Z/10Z.

The conjecture: BHML[i][j] is algebraically determined by G[i][j] up to the
C8-proved W_BHML = 3/50 normalization.

---

## Test Results (March 31, 2026)

### What is confirmed

**W_BHML is the normalized ghost amplitude.**

Ghost pressure at C×D (cross-cycle) = Σ DIS[c][d] = 44.
Symmetric expectation (if ADD = MUL everywhere) = 50.
Deviation = |44 − 50| = 6.
W_BHML = deviation / n² = 6/100 = 3/50. ✓

This IS the C8 proof in ghost language: W_BHML is the per-cell friction
at the C×D interaction zone, read directly from the ghost matrix.

Montgomery dual: R₂(W_BHML) = 1 − sinc²(3/50) = 0.01179.
At t = 3/50, 98.8% of the corridor survives the wobble field.

**BHML harmony cells sit exactly where G = 0.**

BHML = 7 (harmony) at 28 cells.
G = 0 at all 28 BHML harmony cells. 100%.
Mean G at BHML=7 cells: 0.000.
Mean G at BHML≠7 cells: 1.472.

The 28 BHML harmony cells are precisely the cells with zero ghost residual.
This is not a coincidence — it is the BHML operator identity law (C9):
BHML produces harmony where the friction field is absent.

**BHML matches DIS at VOID cells (63% overall).**

At 9 VOID column cells (i=0, j=1..9):
BHML[0][j] = j = DIS[0][j] for all j. 9/9. 100%.
At other non-harmony cells: 17/27 match rate (63%).

### What is not confirmed

**BHML is NOT the ghost trace directly.**

Pearson r(G, BHML) = 0.133. Weak. No algebraic function f with BHML = f(G).
The ghost trace matrix G and BHML are structurally independent as matrices.

**DIS does not determine BHML at non-harmony cells.**

BHML = DIS at 17/27 non-harmony cells. At 10/27 (the ECHO cells), BHML
ignores the friction and follows max(i,j)+1.

**Circulation operators F3, F4 are independent of G.**

r(F3, G) = −0.089. r(F4, G) = −0.366. Neither exceeds |0.5|.
The A15 circulation candidates do not live in the ghost-trace space.

---

## Refined Framing (stronger than ghost trace, weaker than derivation)

**BHML is the arithmetic baseline that the ghost cannot disturb.**

Three zones partition Z/10Z:

| Zone | Cells | TSML | Ghost G | BHML rule |
|------|-------|------|---------|-----------|
| VOID | i=0 or j=0 | mostly 0 | G = DIS = identity | BHML = identity (Rule A) |
| HARMONY | TSML=7, non-VOID | 7 | G = 0 | BHML = 7 OR max(i,j)+1 (Rules B, C) |
| ECHO | TSML≠7, non-VOID | 3,4,8,9 | G = DIS (friction) | BHML = max(i,j)+1 IGNORES friction |

At ECHO cells — the 10 resistance pairs — BHML holds to max(i,j)+1 regardless
of what the ghost records. The arithmetic max is a fixed point under TSML friction.
BHML is not shaped by the ghost; it is the substrate the ghost operates on.

This is the correct framing:
- The ghost IS W_BHML (scalar measure of total friction).
- BHML is what Z/10Z arithmetic IS, below the ghost.
- TSML is the ghost generator; BHML is the ghost floor.

---

## Three-Zone Correspondence (Tier B Target)

The path to Tier B: prove the three BHML rules each correspond to a distinct ghost zone.

| Rule | Zone | Ghost condition | Algebraic target |
|------|------|-----------------|-----------------|
| Rule A (VOID identity): BHML[0][j]=j | VOID | G = DIS = raw identity | Prove: VOID implies G=DIS AND BHML=DIS; joint identity |
| Rule B (axis saturation): BHML[i][j]=max(i,j)+1 | HARMONY | G = 0 | Prove: G=0 at non-VOID harmony cells iff Rule B |
| Rule C (operator identity): BREATH/RESET×TRANS=HARMONY | ECHO | G = DIS (friction) | Prove: G>0 implies BHML overrides friction with max(i,j)+1; friction is recorded in G, not absorbed into BHML |

If all three proved: BHML is the ghost floor theorem: *three rules, three zones, one ghost*.

This is a Tier C target (domain: Z/10Z).

---

## Connection to Existing Proved Results

| Result | Connection |
|--------|-----------|
| C8 — W_BHML = 3/50 (cross-cycle friction) | Ghost amplitude: W_BHML = ghost(C×D deviation)/n². Ghost framing = derivation 1 restated |
| C9 — BHML 28-cell derivation | 28 BHML harmony cells = cells with G=0. Rules A/B/C partition ghost zones |
| C10 — TSML 73-cell derivation | 73 harmony cells = cells where ghost G=0; 27 non-harmony = cells where ghost≥0 |
| C11 — Both tables symmetric | G is also symmetric (tested): G[i][j] = G[j][i] for all i,j |
| A14 — Generator wobble loop | TSML generates → W_BHML is ghost amplitude → BHML is ghost floor → DOING = ghost trace distribution |
| A15 — Circulation operator | r(F3,G)=−0.089, r(F4,G)=−0.366; circulation is not in ghost-trace space; A15 and A16 are structurally separate |

---

## Ghost Matrix G (for reference)

```
     0   1   2   3   4   5   6   7   8   9
 0:  0   1   2   3   4   5   6   0   8   9
 1:  1   0   1   0   0   0   0   0   0   0
 2:  2   1   0   0   2   0   0   0   0   7
 3:  3   0   0   0   0   0   0   0   0   5
 4:  4   0   2   0   0   0   0   0   0   0
 5:  5   0   0   0   0   0   0   0   0   0
 6:  6   0   0   0   0   0   0   0   0   0
 7:  0   0   0   0   0   0   0   0   0   0
 8:  8   0   0   0   0   0   0   0   0   0
 9:  9   0   7   5   0   0   0   0   0   0
```

Nonzero cells: 24. G_sum = 106. Sparse — most of Z/10Z is ghost-free.
Row 7 (HARMONY operator): zero ghost everywhere. The HARMONY operator
leaves no residual impression in any interaction.

---

## Formal Status

**A16 — Tier A** (as of March 31, 2026).

What is proved (Tier C):
- W_BHML = ghost amplitude at C×D zone (= C8, restated in ghost language).
- BHML harmony cells (28) coincide with G=0 cells (100%, exact).

What is structurally observed but unproved:
- Three-zone correspondence (VOID/HARMONY/ECHO ↔ Rules A/B/C).
- BHML as arithmetic floor invariant under ghost friction.

Kill condition: show BHML[i][j] is algebraically determined by G[i][j]
with zero residual across all 100 cells (currently fails: r=0.133, not 1.0).

Promote to Tier B: prove three-zone correspondence (VOID rule ↔ G=0 at VOID;
Rule B ↔ G=0 at harmony; operator identity ↔ G=max at ECHO).

Promote to Tier C: derive Rules A/B/C from ghost zone definition alone,
without referencing BHML multiplication table directly.

---

`© 2026 Brayden Ross Sanders / 7Site LLC & C. A. Luther · DOI: 10.5281/zenodo.18852047`
