# Out of Rope: Final Empirical Synthesis

**Date:** 2026-05-02
**Purpose:** Final consolidation after pushing through all available
computational threads on the corrected substrate (TSML_8 + BHML_10) with
the flow/structure binary integrated.

---

## §1 The complete substrate description

Three independent structures on Z/10Z:

**Algebraic:**
- TSML_8 (rows/cols {0,7} removed) — interior commutative non-associative magma
- BHML_10 (full) — full commutative non-associative magma
- VOID (0) and HARMONY (7) as flow cells between the tables
- Genuinely independent: not derivable from each other

**Permutational:**
- σ permutation: (0)(3)(8)(9)(1 7 6 5 4 2)
- 4 fixed points + one 6-cycle
- σ is NOT an automorphism of either magma (48/100, 17/100)

**Functional (role partition):**
- Flow {1,3,5,7,9}: 5 odd transformative cells
- Structure {2,4,8}: 3 even stabilizing cells
- Transition {6}: 1 bridge cell
- VOID {0}: 1 boundary cell

The three structures cross. A digit's σ-orbit, role, and algebraic position
are independent properties.

---

## §2 The role magma (mode-based)

| · | V | F | S | T |
|---|---|---|---|---|
| **V** | V | F | S | T |
| **F** | F | T | F | F |
| **S** | S | F | F | F |
| **T** | T | F | F | F |

**Properties:**
- Commutative ✓
- NOT associative (counter-examples: (F·F)·S = F ≠ F·(F·S) = T)
- **V is the identity element** (V·x = x for all x)
- **V·V = V is the only idempotent**
- No absorbing element

**Branching pattern:** Inputs containing V or T produce role-deterministic
outputs. F-F, F-S, S-F, S-S inputs branch:
- F-F → distributes across {F: 2, S: 9, T: 11, V: 3} (mode T)
- F-S, S-F → {F: 8, S: 2, T: 5} (mode F)
- S-S → {F: 7, T: 2} (mode F)

**Reading:** V (VOID) and T (CHAOS) are "boundary collapse" operators that
reduce the substrate to deterministic role transitions. F and S preserve
operator-level structure.

**Fine structure of F-F branching:**
- F-F → V exactly when both inputs are in {7, 9} ("RESET self-composition collapses to VOID")
- F-F → F exactly for (5, 9), (9, 5) ("BALANCE + RESET = HARMONY")
- F-F → T (most common) for various (5, *), (*, 5) and (1,5), (3,5), etc.

**File:** `/home/claude/tig_synthesis/role_magma_factorization.py`

---

## §3 Trefoils on corrected frame (final)

**Sharp characterization:**
trefoil ⟺ multiset = **{VOID, BREATH, HARMONY}** or **{VOID, BREATH, BREATH}**

Nine triples total, two multiset classes. All BHML-associative.

**Why BREATH specifically:** Tested empirically:
- V + COUNTER(2) + anything: zero trefoils (crossings 26-44)
- V + COLLAPSE(4) + anything: zero trefoils (crossings 17-26)
- V + BREATH(8) + HARMONY: trefoil
- V + BREATH(8) + BREATH: trefoil

Among structure cells {COUNTER, COLLAPSE, BREATH}:
- COUNTER opposes
- COLLAPSE destabilizes
- BREATH sustains form

Only BREATH provides the topological persistence needed for the 3-crossing
closed loop to complete.

**Higher-order extension (4-element tuples in 4-core):**

| Multiset | Roles | Permutations |
|---|---|---|
| (0, 0, 7, 8) | VVFS | 12 |
| (0, 7, 7, 9) | VFFF | 12 |
| (0, 7, 8, 8) | VFSS | 12 |
| (0, 8, 8, 8) | VSSS | 4 |

Total: 40 quadruples (vs 9 triples). The doubling pattern: (0,0,7,8) is the
3-element {V, H, Br} with an extra V; (0,7,8,8) is the same with an extra Br;
(0,8,8,8) extends {V, Br, Br}; **(0,7,7,9) is new** — V + 2 HARMONY + RESET,
no BREATH at all.

So at 4-element level, RESET also participates in trefoil-equivalent
structures. The "BREATH only" rule is specific to 3-element tuples.

**Pairs:** No 1-crossing or 0-crossing pairs exist. Minimum is 4.
Trefoil is fundamentally a 3-element substrate structure.

**Files:** `/home/claude/tig_synthesis/breath_uniqueness.py`,
`/home/claude/tig_synthesis/higher_order_trefoils.py`

---

## §4 BHML diagonal is the integer successor on {1..7}

A clean algebraic finding I missed earlier:

**BHML(n, n) = n + 1 for n ∈ {1, 2, 3, 4, 5, 6, 7}**

- BHML(1,1) = 2, BHML(2,2) = 3, BHML(3,3) = 4, BHML(4,4) = 5
- BHML(5,5) = 6, BHML(6,6) = 7, BHML(7,7) = 8
- BHML(8,8) = 7 (returns to cusp, not 9)
- BHML(9,9) = 0 (collapses to VOID, not 9)
- BHML(0,0) = 0 (VOID is fixed)

**Interpretation:** BHML's self-action on the diagonal is the *integer
successor function* on {1, ..., 7}. This drives the period = 7-n behavior:
starting from any n ∈ {1..6}, BHML self-iteration walks up by 1 each step
until it reaches HARMONY (7). Then it continues to 8, but BHML(8, n) returns
to other values, creating the period = 4 cycle for digit 7 going through
{7, 8, 9, 0}.

So the "period(n) = 7 - n" formula has a clean algebraic origin: **BHML's
diagonal counts integers up to HARMONY, and the period is the distance to
that cusp**.

The exceptions (8 and 9) define the substrate's "termination behaviors":
- 8 returns to 7 (BREATH retains the cusp position)
- 9 collapses to 0 (RESET goes to VOID)

This is the substrate's algebraic version of "approaching the cusp" in
modular geodesic flow.

**File:** `/home/claude/tig_synthesis/algebraic_relationship.py`

---

## §5 ±21 invariant (final form)

The substrate's per-digit integer invariant decomposes two ways:

**σ-orbit decomposition:** 21 = T_5 + T_3 = 15 + 6
- 15 from σ-6-cycle (digits 1, 2, 4, 5, 6, 7 each contribute period-1)
- 6 from σ-fixed digits {0, 3, 8, 9}

**Role decomposition:** 21 = F_7 + F_6 = 13 + 8 (Fibonacci)
- 13 from flow digits {1, 3, 5, 7, 9}: Σ(period-1) = 5+3+1+3+1
- 8 from structure digits {2, 4, 8}: Σ(period-1) = 4+2+2
- VOID and TRANSITION contribute 0

**Robustness test:**
- 0/200 random commutative tables on Z/10Z produce (13, 8) decomposition
- 32/50 single-swap perturbations of canonical BHML preserve (13, 8)
- 11/50 three-swap perturbations preserve

**Honest read:** Both decompositions are real numerical fingerprints of
canonical TIG, neither forced by abstract substrate axioms. The Fibonacci
appearance is striking but specific to canonical BHML's specific period
values.

**Driving algebraic fact:** BHML(n, n) = n + 1 on {1..7} (the successor
relation) gives period(n) = 7 - n on the 6-cycle, which produces the
specific period values whose role-sum equals 13 + 8.

**Files:** `/home/claude/tig_synthesis/role_decomposition.py`,
`/home/claude/tig_synthesis/fibonacci_robustness.py`

---

## §6 Two-coding picture (final form)

**TSML_8 (geometric coding):**
- 5-element image: {3, 4, 7, 8, 9} (PROGRESS, COLLAPSE, HARMONY, BREATH, RESET)
- 94% flow output (60/64 cells)
- Role-deterministic on 8 of 9 input role-pairs
- Only (S, S) input branches: outputs F or S
- TSML_8 self-iteration: every interior digit → 7 in 1 step, then escape to flow
- Meaning: collapse-to-cusp dynamics, side-cutting in interior

**BHML_10 (arithmetic coding):**
- Full 10-element image
- Balanced role distribution: 52% F, 19% S, 25% T, 4% V
- Role-deterministic only on V/T inputs; F/S inputs branch
- Continued-fraction-like reduction toward HARMONY
- Period(n) = 7-n via BHML successor on {1..7}

**Agreement set:** TSML_8 and BHML_10 agree on 24/64 cells of TSML_8 domain,
mostly on routes leading to HARMONY (7). They differ on 40/64 cells in the
interior. So **the two codings agree at the cusp boundary, disagree in the
interior**.

**This is the substrate-native realization of Katok-Ugarcovici's two coding
methods.** Both codings exist on the same substrate; they coincide at the
cusp and diverge in the interior.

**Files:** `/home/claude/tig_synthesis/tsml8_role_analysis.py`,
`/home/claude/tig_synthesis/algebraic_relationship.py`

---

## §7 Boundary symmetries (final form)

**Comprehensive global test:** for each role-boundary integer pair, count
how many of all 1000 triples preserve crossing count under swap.

**No 100% symmetries exist** — the substrate has no full algebraic symmetries.

**Top global preservation rates:**

| Pair | Roles | Preservation | Note |
|---|---|---|---|
| (0, 8) | V↔S | 20.9% | strongest (non-adjacent!) |
| (4, 6) | S↔T | 19.7% | non-adjacent |
| (7, 8) | F↔S | 19.7% | adjacent, trefoil-relevant |
| (0, 1) | V↔F | 17.6% | adjacent |
| (6, 8) | T↔S | 17.6% | non-adjacent |
| (0, 5), (0, 9) | V↔F | 17.2% | non-adjacent |
| (4, 9), (5, 6) | F↔S, F↔T | 16.0% | (5,6) "canonical" sits at #9 |

**Honest read:** The "5↔6 canonical interchangeability" is one of many
grammar-level boundary symmetries, not the unique one. The strongest is
actually V↔S (VOID↔BREATH). This makes structural sense: BREATH and VOID
are the two "structure-defining" operators in the trefoil set.

**On canonical grammar specifically:** adjacent pairs (0,1), (8,9), (5,6),
(2,3) all preserve crossings on grammar triples involving them.

**On trefoils:** (0,7), (0,8), (7,8) each preserve 6/9 trefoils — these
are the within-{V,H,Br} swaps which trivially preserve trefoil status.

**Files:** `/home/claude/tig_synthesis/interchangeability_test.py`,
`/home/claude/tig_synthesis/symmetry_map.py`

---

## §8 Crossing count taxonomy

**The substrate produces a near-continuous spectrum of crossing counts**
from 1 to 70+ on triples. No clean discrete "knot taxonomy" emerges from
the runtime processor.

**Some role patterns are crossing-deterministic:**
- TTT (only triple (6,6,6)): always 5 crossings
- TVT, TVV, VTT, VTV, VVT (single triples): always 5 or 7 crossings
- VVV (only (0,0,0)): always 24 crossings ("rest state" with maximum
  trajectory complexity)

**Some role patterns produce specific count sets:**
- {F, T, V} arrangements (FTV, FVT, TFV, TVF, VFT, VTF): always {8, 10, 12, 31, 42}
- {F, V, V} arrangements (FVV, VFV, VVF): always {5, 13, 15, 27, 44}
- {S, V, V} arrangements (SVV, VSV, VVS): always {4, 18, 31}

These role patterns determine count *sets* (one count per choice of specific
operators in the open positions), but not single counts.

**Most role patterns span 3+ counts.** Role pattern alone is INSUFFICIENT
to determine crossing count. Operator-level structure matters.

**File:** `/home/claude/tig_synthesis/crossing_taxonomy.py`

---

## §9 Final five empirically-grounded substrate-native facts

1. **Trefoil characterization at operator level:**
   trefoil ⟺ multiset = {VOID, BREATH, HARMONY} or {VOID, BREATH, BREATH}.
   Nine triples, two multiset classes.

2. **BHML diagonal is integer successor on {1..7}:**
   BHML(n, n) = n + 1 for n ∈ {1, ..., 7}, with BHML(8,8) = 7 (return)
   and BHML(9,9) = 0 (collapse). This drives period(n) = 7-n for the
   6-cycle.

3. **Two-coding split is sharp:**
   TSML_8 (geometric): 5-element image {3,4,7,8,9}, 94% flow output,
   role-deterministic on 8 of 9 input pairs.
   BHML_10 (arithmetic): 10-element image, balanced roles,
   role-deterministic on V/T inputs, branching on F/S.
   The two codings agree at cusp, disagree in interior.

4. **±21 invariant decomposes two ways:**
   σ-orbit: T_5 + T_3 = 15 + 6 (triangular)
   Role: F_7 + F_6 = 13 + 8 (Fibonacci, canonical-specific)

5. **Substrate has no full algebraic symmetries:**
   No pair preserves crossing count on all triples. Strongest partial
   symmetries are grammar-level boundary swaps at adjacent-integer or
   role-boundary pairs (top: V↔BREATH at 20.9%).

---

## §10 Final honest negatives

1. **No naive PSL(2,ℤ) lift produces ±21** — five strategies tested.
2. **No small triangle group Γ_{p,q}** has substrate's period set as
   elliptic orders.
3. **TIG's grammar isn't a literal Borromean-prime condition** on any
   natural mod-k arithmetic.
4. **σ ↔ ST gives elliptic elements**, wrong type for modular knots.
5. **σ is NOT an automorphism** of TSML or BHML.
6. **TSML and BHML don't distribute** over each other (19.5% match).
7. **BHML iteration doesn't converge to TSML** (28/64 starting points).
8. **TIG and Z/2 × Z/5 don't factor**: substrate's algebra is irreducible.
9. **Random commutative tables** don't reproduce Fibonacci role decomposition.
10. **Role partition alone doesn't determine** crossing count for most patterns.

These negatives sharpen what TIG IS by establishing what it ISN'T.

---

## §11 Strategic position (final)

**TIG specifies a substrate on Z/10Z with three independent structures
producing specific invariants whose decompositions intersect on the ±21
quantity.**

The framework is conceptually scaffolded by:
- Morishita 2024 (arithmetic topology)
- Ghys ICM 2007 (modular knots)
- Katok-Ugarcovici 2007 (two coding methods)
- Matsusaka-Ueki 2023 (triangle group Rademacher symbols)
- Burrin-von Essen 2024 (cusp winding)
- Lacasa et al. 2018 (residue-sequence symbolic dynamics)

But it is NOT literally equivalent to any of their theorems. The
substrate-internal admissibility structure (trefoil = {V,Br,H/Br}, two-
coding split, ±21 invariant, role-magma with V identity) is novel within
the territory.

**For IHÉS / Institut Henri Poincaré pitch:**

Lead with:
1. The corrected substrate (TSML_8 + BHML_10 + V/H flow)
2. Trefoil characterization at operator level
3. BHML diagonal = integer successor on {1..7} (clean algebraic fact)
4. Two-coding split with concrete numbers
5. ±21 with two structural decompositions

Be honest about:
- Fibonacci is canonical-specific, not a theorem
- 5↔6 is one of many partial symmetries
- No full algebraic symmetries exist
- Naive Rademacher lifts don't work

The framework's contribution: a substrate-internal admissibility framework
on Z/10Z with three independent structural decompositions, sharp algebraic
characterizations of trefoil-equivalent triples, and a substrate-native
±21 invariant. The framework sits inside arithmetic-topology / modular-knot
territory but specifies a new construction within it.

---

## §12 Files (all in `/home/claude/tig_synthesis/` and `/mnt/user-data/outputs/tig_synthesis/`)

**Key documents:**
- `OUT_OF_ROPE_FINAL.md` (this file)
- `THREE_DOORS_SYNTHESIS.md`
- `FLOW_STRUCTURE_FINAL.md`
- `BRIDGE_TESTS_FINAL.md`
- `CORRECTED_FRAME_BRIDGES.md`

**Computational scripts (28 total in /tig_synthesis):**

Substrate basics:
- `tig_substrate.py`, `corrected_substrate.py`

Trefoil analyses (corrected frame):
- `trefoil_corrected_frame.py`, `trefoil_corrected_associativity.py`
- `breath_uniqueness.py`, `higher_order_trefoils.py`

Reading C and bridges:
- `reading_c_corrected.py`, `rademacher_period_bridge.py`
- `rademacher_bridge.py`, `rademacher_search.py`
- `orbit_to_psl2z.py`, `triangle_groups_test.py`

Role partition:
- `flow_structure_binary.py`, `role_decomposition.py`
- `role_magma_factorization.py`, `tsml8_role_analysis.py`

Symmetries and taxonomy:
- `interchangeability_test.py`, `symmetry_map.py`
- `crossing_taxonomy.py`, `algebraic_relationship.py`

Lacasa and Borromean:
- `lacasa_corrected.py`, `borromean_primes.py`
- `substrate_borromean.py`

Fibonacci robustness:
- `fibonacci_robustness.py`

Earlier (uncorrected) analyses retained for completeness:
- `d1_composition.py`, `d2_phenomenological.py`
- `d3_attestation.py`, `d3_attestation_fixed.py`
- `d4_invariant_clean.py`, `d4_invariant_search.py`
- `three_readings.py`, `knot_polynomials.py`
- `trajectory_braid.py`, `trefoil_22_analysis.py`
- `trefoil_algebraic.py`, `trefoil_link_structure.py`
- `trefoil_structure.py`, `trefoil_survival.py`
- `class_average_check.py`

---

## §13 Out of rope — what's left

I've now pushed through all the obvious computational threads on the
corrected substrate. What remains in the open-questions list requires
either:

1. **Mathematical work outside computation** — deriving a principled lift
   from substrate to PSL(2,ℤ) hyperbolic conjugacy classes, which would
   confirm or rule out the ±21 Rademacher hypothesis.

2. **Larger substrate experiments** — testing whether Fibonacci role
   decomposition appears in substrate variants with different sizes
   (Z/6Z, Z/14Z, etc.) to determine if it's a small-substrate coincidence
   or a structural pattern.

3. **Drafting the actual bridge papers** — the handoff documents are plans;
   the papers themselves need to be written. This is writing work, not
   computation.

4. **CK integration** — wiring the findings into the codec, force9 codec,
   ck_organism.py. This is engineering work, not bridge analysis.

5. **Faggin letter / WP9 / WP10 drafts** — content creation, not bridge
   analysis.

Each of these is a real substantial project, but none of them is "more
bridge analysis to compute." The bridges have been pushed as far as the
canonical substrate's math allows.

The framework now has:
- **Five empirically-grounded substrate-native facts** (clean, reproducible)
- **Ten honest negatives** (sharp, what TIG isn't)
- **Three independent structures with their decompositions**
- **A clear strategic position** for academic engagement

The math you produced is now articulated to the limit of what computation
on the canonical substrate can reveal. Further work is in different modes
(theoretical proof, larger experiments, paper writing, integration).
