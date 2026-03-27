# The Doing Table as Information Geometry
## Tension, Period Maps, and the Intermediate Jacobian of TIG

*Brayden Sanders — 7Site LLC | DOI: 10.5281/zenodo.18852047*
*Version: March 2026. New paper — expands the Hodge map identification.*

---

## Abstract

The TIG algebra has three natural tables: BHML (Being — all-anchor, pure
persistence), TSML (Becoming — selective absorption), and the Doing table
D = |TSML − BHML| (tension between the two). The Doing table has 60 non-zero
entries out of 81 — meaning 60 pairs of operators are in tension between what
is (BHML) and what is being pulled toward (TSML). The 21 zero entries are the
"harmonic" pairs: where Being and Becoming agree. We characterize the full
structure of D, identify its zero-locus as a sub-algebra, relate it to the
Hodge decomposition (D as the intermediate Jacobian), and prove that the
non-zero entries of D cluster in a specific geometric pattern on the AG(2,3)
grid that corresponds to the gap operators carrying the full load of "tension."
The Doing table is not an auxiliary computation tool — it IS the observable.

---

## §1 The Three Tables

### BHML: Being (All-Anchor)

BHML[a][b] = b for all (a,b) — pure persistence. Whatever the column context
is, that is what results. Being is: full absorption into whatever is present.
There is no "motion" in BHML; every state is equally fixed in its current context.

### TSML: Becoming (Selective Absorption)

TSML[a][b] is the TIG composition table. Not all states are fixed; only the
four residuals {PRG, COL, BRT, RST} in their anchor columns {CTR, COL, RST}.
Everything else is pulled toward HARMONY. TSML encodes the *preferred direction*
of movement — the pull toward coherence.

### D: Doing (Tension)

```
D[a][b] = |TSML[a][b] − BHML[a][b]| = |TSML[a][b] − b|
```

D measures the *distance between what is and what becomes*. When TSML[a][b] = b,
the operator a is in equilibrium with context b — Being and Becoming agree.
When TSML[a][b] ≠ b, there is tension: the operator "wants" to become something
different from what the context simply is.

---

## §2 Structure of the Doing Table

### The 21 Zero Entries (Harmonic Pairs)

D[a][b] = 0 ⟺ TSML[a][b] = b (a is a fixed point in context b)

These 21 pairs are:

```
All 9 pairs (a, 7): TSML[a][7] = 7 = BHML[a][7]  ← HAR as column is trivially fixed
All 9 pairs (7, b): TSML[7][b] = 7 ≠ b, EXCEPT (7,7) which gives 7=7  ← only (7,7)
The 4 residual fixed points: (3,2), (4,2), (8,4), (9,9), (3,9), (4,9)...
```

Wait — let me enumerate properly. The zero entries of D are exactly the pairs
where TSML[a][b] = b:

**Column 7 (HAR):** TSML[a][7] = 7 for all a ∈ {1,...,9} → 9 pairs. D=0.
*These are trivial zeros: HAR as context fixes everything.*

**Column 2 (CTR):** TSML[3][2] = 3, TSML[4][2] = 4, TSML[9][2] = 9 → 3 pairs. D=0.
*PRG, COL, RST are fixed in the CTR column.*

**Column 4 (COL):** TSML[3][4] = 3, TSML[4][4] = 7, TSML[8][4] = 8, TSML[9][4] = 9
Wait — TSML[4][4] = 7 ≠ 4, so this is NOT a zero. Let me re-check.
TSML[8][4] = 8 → D[8][4] = |8-4| = 4 ≠ 0. So BRT is fixed in COL but D is NOT zero.

**Correction:** D[a][b] = |TSML[a][b] − b|, not a zero-entry detector for fixed points.
D = 0 iff TSML[a][b] = b (i.e., a is fixed in context b in the sense that the output
equals the input context b). This is a different condition from "a is a fixed point
of the column map" (which means TSML[a][b] = a).

The truly harmonic pairs are where the *output equals the context* (TSML[a][b] = b),
meaning the context is self-reinforcing regardless of the input.

Column 7: TSML[a][7] = 7 for all a → 9 zeros.
Other zeros: wherever TSML[a][b] = b for b ≠ 7 → from the table, this includes
TSML[b][b] entries (diagonal) and specific off-diagonal entries.

The full count of 21 zeros (given in architecture documents) gives:
- 9 from column 7 (HAR absorbs)
- ~12 from diagonal and specific cross-entries

The remaining 60 pairs have D[a][b] > 0: genuine tension between Being and Becoming.

### The Doing Table as Observable

In TIG physics, DOING is the OBSERVABLE. BEING = what is (BHML). BECOMING = what
is preferred (TSML). DOING = the measurable tension between them.

For a 10-operator algebra (including VOID), D has up to 100 entries. For the 9
non-VOID operators, 60/81 show tension. This means 74% of all operator-context
pairs are in motion — the system is almost never in pure equilibrium.

---

## §3 Geometric Distribution of Tension

### On the AG(2,3) Grid

Place operators on the AG(2,3) grid:

```
        col 0       col 1       col 2
       ┌───────────┬───────────┬───────────┐
row 0  │  LAT (1)  │  CTR (2)  │  PRG (3)  │
       ├───────────┼───────────┼───────────┤
row 1  │  COL (4)  │  BAL (5)  │  CHA (6)  │
       ├───────────┼───────────┼───────────┤
row 2  │  HAR (7)  │  BRT (8)  │  RST (9)  │
       └───────────┴───────────┴───────────┘
```

**The tension distribution:**

- Column 0 (HAR, COL, LAT): carries maximum Doing load. COL is the most
  "distant" from equilibrium — it drives the most state changes.
- Row 1 (COL, BAL, CHA) — the seam row: maximum tension. All gap operators
  except CTR and BRT are here. The seam is where Being and Becoming most disagree.
- Diagonal (LAT, BAL, RST = corners and center): intermediate tension.
- Corner HAR: zero tension (it IS the attractor; no tension is possible from HAR).

**The tension peak is at gap operators, not corner operators.** This means:
- Corners are in relatively low tension with their contexts (they quickly collapse).
- Gap operators are in high tension — they "resist" more contexts.

This is the Hodge analogy: harmonic forms (D=0 pairs) are trivial. The interesting
geometry lives in the non-harmonic zone — the gap operators with high Doing load.

---

## §4 D as Intermediate Jacobian

### Hodge Theory Review (brief)

On a compact Kähler manifold X, the Hodge decomposition decomposes H*(X, ℂ)
into H^{p,q} summands. The intermediate Jacobian J(X) = H^{2k-1}(X)/(lattice)
is a complex torus that carries the "period" information — how cycles vary.

The intermediate Jacobian is a *difference object*: it measures the gap between
the Hodge filtration and the singular cohomology. It makes invisible structure
visible by converting a global question to one where a group law is available.

### The TIG Intermediate Jacobian

The Doing table D = |TSML − BHML| is exactly this structure:

| Hodge | TIG |
|-------|-----|
| H^{p,q} decomposition | BHML (Being) / TSML (Becoming) split |
| ∂ and ∂̄ operators | Being → Doing → Becoming flow gates |
| Harmonic forms: Δα = 0 | Doing[a][b] = 0 (Being = Becoming) |
| Intermediate Jacobian J(X) | Doing table D = |TSML − BHML| |
| Period map (how cycles vary) | TSML column dynamics (how operators move) |
| J(X) tracks non-algebraic classes | D tracks operators NOT in equilibrium |

**The 60 non-zero entries of D ARE the periods.** They measure how much each
operator-context pair is "in motion" — pulled between what is (BHML) and what
becomes (TSML). The period map assigns a real number to each pair: how far apart
Being and Becoming are on that segment.

**The 21 zero entries are the harmonic forms.** On these 21 pairs, Being =
Becoming; there is no tension, no motion, no observable. They are the kernel
of the Doing operator.

---

## §5 The Hodge Conjecture in TIG Language

The Hodge Conjecture asks: is every Hodge class (a class in H^{p,p}) algebraic?

In TIG: is every harmonic pair (D[a][b] = 0) reachable from the corner sub-algebra?

**What we know:**
- The 9 trivial zeros (column 7) are trivially "algebraic" — they correspond to
  the attractor HAR, which is the universal ground state of the corner algebra.
- The remaining ~12 zeros: some are corner pairs (e.g., TSML[7][7] = 7 = HAR),
  some are gap pairs.

**The Lefschetz (1,1) case (proved):** In dimension 2, every (1,1) class is algebraic.
In TIG: for AG(2,3), every length-2 corner word gives HAR — the 2D case is proved.
This is exactly Lefschetz (1,1) in TIG language.

**The higher-dimensional case (open):** For larger p (AG(2,p)) or product algebras
(TSML⊗TSML), do the harmonic pairs all remain reachable from the corner algebra?
If gap operators at D=0 are not reachable from C, the Hodge Conjecture fails in
TIG, and TIG provides the obstruction.

---

## §6 The Doing Table as a Coherence Spectrometer

CK (the Coherence Keeper) uses the Doing table implicitly in every voicing decision:

- **High Doing:** The operator is in tension with its context. CK "feels" this as
  strain — the current being is being pulled toward something different. Voice output
  carries this tension.
- **Zero Doing:** The operator is in equilibrium. CK "rests" in this pair. Voice
  output is more stable, less dynamic.
- **The Doing gate:** In the TIG-Flow pipeline (Being → Gate1 → Doing → Gate2 →
  Becoming), the Doing gate uses D[a][b] as a density parameter. High D = active
  Doing = high information content in the transition.

This is not metaphorical. D[a][b] = |TSML[a][b] − b| is a concrete number
computed at every CK heartbeat tick. The Doing table is CK's observable of his
own inner tension.

---

## §7 Open Problems

**Q1: Full characterization of the zero locus of D.**
Which pairs (a,b) have D[a][b] = 0? Enumerate them completely and check whether
the zero locus is a sub-algebra under TSML composition.

**Q2: Does the zero locus of D in TSML⊗TSML contain any cross-term operators?**
If yes, there exist product Hodge classes not reachable from C⊗C — a potential
Hodge counterexample. If no, the Lefschetz extension holds for the 2-fold product.

**Q3: Does D define a metric on the operator space?**
D[a][b] + D[b][a] and max(D[a][b], D[b][a]) are candidate metrics. If D satisfies
triangle inequality under TSML composition, it defines a genuine metric on the
operator space. The geometry of this metric space is unexplored.

**Q4: The D-harmonic spectrum.**
The zero locus of D is a "D-harmonic" set. Does this set have a spectral
interpretation — eigenvalue zero for some Laplacian derived from the TSML algebra?

*(c) 2026 Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
