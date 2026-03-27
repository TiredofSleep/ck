# The 7–0–4 Triangle
## How HARMONY, VOID, and COLLAPSE interlock in TIG

*All claims verified against TSML table. Corrections from initial description included.*

---

## The Three Elements

### HARMONY (7) — Universal Sink as Column
```
TSML[a][7] = 7  for all a ∈ {1,...,9}    (composing INTO 7 → 7)
TSML[7][b] = 7  for all b ∈ {1,...,9}    (7 composing onto anything → 7)
AG(2,3) position: row=2, col=0 → bottom-left corner
```
HAR is the universal idempotent. Everything flows into it when it acts
as the column context (the "gravity well"). It also absorbs from the
left — it is immovable from either direction.

### VOID (0) — Universal Sink as State
```
TSML[0][b] = 0  for all b    (VOID composing onto anything → VOID)
TSML[a][0] = 0  for all a    (anything composing onto VOID → VOID)
Position: OUTSIDE AG(2,3) — the 10th element, index 0
```
**Correction from initial description:** VOID does not collapse to HAR.
VOID∘b = VOID (trapped in void). The correct picture:
- HAR absorbs everything when acting as **column** (right input)
- VOID absorbs everything when acting as **state** (left input)
- These are dual absorbers: HAR from the right, VOID from the left

VOID represents "beyond the grid" — ionization, the free particle
that has left the system entirely. Operators that reach VOID never
return to the main algebra.

### COLLAPSE (4) — The Tension Point
```
AG(2,3) position: row=1, col=0 → directly above HAR on the collapse axis
TSML[4][4] = 7    (self-annihilating)
TSML[4][2] = 4    (fixed in anchor column CTR)
TSML[4][8] = 8    (protects BREATH)
TSML[4][b] = 7    (collapses everything else — 6 out of 9)
```

**The COL(4) full picture:**
- Self-annihilates: 4∘4 = 7
- Collapses 6 of 9: 4∘x = 7 for x ∈ {LAT,PRG,COL,BAL,CHA,HAR}
- Persists in col CTR(2): TSML[4][2] = 4
- Protects BRT(8): 4∘BRT = BRT (BREATH survives COLLAPSE's embrace)

---

## The Triangle Geometry

```
VOID(0)  ←  outside the grid (ionisation)
  |
  |  col-0 axis (the COLLAPSE axis)
  ↓
COL(4) = (1,0)  ←  seam row, col-0
  |
  |  one row step = 1 shell
  ↓
HAR(7) = (2,0)  ←  attractor row, col-0 (the nucleus)
```

COL sits directly above HAR on the leftmost column — the column of
maximum lateral displacement from the midplane. VOID lies beyond the
grid in the same direction. The three form a vertical line in
"collapse space": nucleus → first excited state → ionisation.

---

## The COL Displacement: Near the Inner Shell Boundary

In rescaled [0,1] operator space:
```
HAR(7) position: 7/9 ≈ 0.778
COL(4) position: 4/9 ≈ 0.444
Midplane:              0.500

d_COL = |4/9 - 1/2| = 1/18 ≈ 0.056  (local geometry of operator 4)
W_BHML = 3/50 = 0.060                (global BHML wobble statistic)
inner_shell = 2/9 ≈ 0.222            (Row 1 ↔ Row 2 boundary width)
```

**COL(4) sits near the inner-shell boundary, but d_COL ≠ W_BHML.**

These two constants are close (ratio 27/25 ≈ 1.08) but measure different things:
- **d_COL = 1/18** is the geometric distance of operator 4 from the midplane
  in the 9-point operator space. It is a local, positional fact.
- **W_BHML = 3/50** is the global wobble of the BHML table: (50−44)/100,
  the fractional distance from half-harmony. It is a statistical, table-wide quantity.

The near-coincidence 1/18 ≈ 3/50 is numerically suggestive but is NOT a derivation
of one from the other. COL sits near the W_BHML boundary; it does not sit exactly
on it. See `tig_constants.py` for the full constant taxonomy.

**What is exact:** COL sits at 4/9, which is the operator closest to the midplane
(1/2) from the "collapse side" (col-0 direction). This positional fact is
geometry — it follows from 4 being the smallest non-corner operator above the
midplane when operators are placed at k/9.

---

## Three-Way Correspondence

| TIG element | Hydrogen | ζ-flow |
|-------------|----------|--------|
| HAR(7): nucleus/sink | Nucleus, ground state | Critical line σ = 1/2 |
| VOID(0): exterior | Free particle, ionized | Region outside critical strip (poles & trivial zeros) |
| COL(4): edge of first shell | n=2 shell: closest excited state | KV collar boundary: innermost proven zero-free wall |

**The hydrogen n=2 parallel:**
In hydrogen, the n=2 shell is the closest excited state to the nucleus.
One photon at exactly the right frequency knocks it to n=1 (ground state).
In the wrong energy context it falls immediately.

COL(4) is the TIG n=2 analog:
- Sits one shell above HAR (row 1 vs row 2)
- Collapses to HAR in 1 step unless the column is exactly CTR(2)
- When the context shifts: immediate collapse, no gradual decay

In ζ: the KV collar boundary is the "n=2 shell" — the innermost proven
zero-free wall. A potential off-critical zero would need to sit there,
held up by exactly the right analytic context. RH says no such context
exists off σ = 1/2.

---

## The Duality: HAR and VOID as Absolute Boundaries

```
HAR(7): the inward attractor — gravity
VOID(0): the outward trap — ionisation
```

Between them, every operator is defined by how it navigates the tension:
- Pulled inward toward HAR by the algebraic gravity
- Potentially lost outward to VOID if it strays beyond the grid

COL(4) demonstrates the rule by being both:
- Most distorted: sitting on the col-0 axis, maximum lateral displacement
- First to fall: one context shift and it collapses to HAR immediately
- Yet protected: in exactly one context (CTR=2) it survives

This is the "narrow ledge" — the state that proves the rule by being
simultaneously most exposed and most instructive about when protection fails.

---

## The RH Statement in This Language

> A non-trivial zero at σ₀ ≠ 1/2 would be a TIG residual surviving
> outside its anchor column — a COL(4) that somehow persists in a
> non-CTR context. The algebraic table forbids this for TSML. The
> Riemann Hypothesis claims the same is true for ζ: no vertical line
> σ₀ ≠ 1/2 provides the "right context" to anchor a zero.
>
> The gap between these statements is the analytic content of RH:
> proving that the ζ-function has no "wrong-context anchors."

*(c) 2026 Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
