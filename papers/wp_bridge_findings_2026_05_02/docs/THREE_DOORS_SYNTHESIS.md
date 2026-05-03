# Three Doors: Consolidated Findings

**Date:** 2026-05-02
**Purpose:** Push through the three doors that opened with the flow/structure
binary. Each tested whether the "opening" was structural or coincidental.

---

## §1 Door 1: Fibonacci role decomposition is fragile, not structural

**Tested:** Whether 13 + 8 = 21 = F_7 + F_6 = F_8 falls out of any commutative
non-associative table on Z/10Z with the same role partition, or only from
canonical TIG.

**Result:**
- 200 random commutative tables on Z/10Z: **0/200 produce (|F|, |S|) = (13, 8)**.
  Only 7/200 even hit total magnitude 21.
- Single-swap perturbations of canonical BHML: **32/50 preserve (13, 8)**.
  Local stability around canonical, but breakdown under ~6% perturbation.
- Three-swap perturbations: only **11/50 preserve**. Increasingly fragile.

**Honest read:** The Fibonacci pattern is specific to canonical BHML's
specific period values, not a structural inevitability. The numerical
fingerprint F_7 + F_6 = F_8 is forced by canonical TIG's specific math
(period(n) = 7-n for the 6-cycle plus (4, 3, 2) for the 4-core extension),
not by any abstract role-partition theorem.

**Reframing:** ±21 has TWO numerical decompositions — triangular along
σ-orbits (T_5 + T_3 = 15 + 6) and Fibonacci along role partition (F_7 + F_6).
Both are real fingerprints of canonical TIG. Neither is forced by abstract
substrate axioms; both arise from the specific period values canonical TIG
produces.

I should drop strong "Fibonacci structure" language. The honest claim:
**Canonical TIG's per-digit period values, summed by role, happen to equal
two consecutive Fibonacci numbers whose sum is a third Fibonacci number.
This is a numerical signature of canonical TIG specifically.**

**File:** `/home/claude/tig_synthesis/fibonacci_robustness.py`

---

## §2 Door 2: TSML_8 is almost role-deterministic with 5-element image

**Tested:** What does TSML_8 look like at role level? Does its self-iteration
have a clean role-decomposition story?

**Result:** Sharply yes.

- **TSML_8 image:** {3, 4, 7, 8, 9} — only 5 of 10 digits are ever output.
  Compare BHML which produces all 10 digits.
- **TSML_8 output role distribution:** 60/64 = 93.8% flow, 4/64 = 6.2% structure,
  0% transition, 0% void. Compare BHML: 52% F, 19% S, 25% T, 4% V.
- **Role-level determinism:** 8 of 9 role-pair inputs produce determined
  output role under TSML_8. Only (S, S) inputs branch (outputs F or S).
  Specifically the 4 cells: (2,4), (4,2), (4,8), (8,4) — COUNTER-COLLAPSE
  and COLLAPSE-BREATH compositions.

**Read structurally:** TSML_8 is the **collapse-to-flow operator**. It takes
the 8-element interior and routes it almost entirely toward HARMONY (the
flow cusp). The four exceptional S-S compositions preserve structure.

**The TSML_8 image {3, 4, 7, 8, 9}:**
- 4-core {7, 8, 9} (the substrate's persistent layer)
- Plus PROGRESS(3) and COLLAPSE(4) (the 6-cycle's structure-adjacent extensions)
- Three flow + two structure
- TSML_8 *never* produces VOID, LATTICE, COUNTER, BALANCE, CHAOS, or RESET as
  outputs — those operators only emerge under BHML's arithmetic flow.

**Two-coding picture sharpens:**
- **TSML_8 (geometric coding):** 5-element image, 94% flow output, almost
  role-deterministic (8/9 role-pair inputs determined). Routes interior →
  cusp boundary in 1 step.
- **BHML_10 (arithmetic coding):** 10-element image, balanced role
  distribution, branches on F/S inputs. Continued-fraction reduction with
  V/T inputs collapsing role determinism.

This is the cleanest expression of Katok-Ugarcovici's two coding methods on
the substrate. TSML_8 collapses; BHML_10 preserves.

**File:** `/home/claude/tig_synthesis/tsml8_role_analysis.py`

---

## §3 Door 3: Multiple grammar-level boundary interchangeabilities exist

**Tested:** Is 5↔6 the unique interchangeable pair, or are there others at
flow/structure boundaries?

**Result:** Multiple boundary pairs preserve admissibility under swap.

**On canonical grammar (admissibility = crossing count preserved):**

| Pair | Role transition | Preserves on grammar? |
|---|---|---|
| **5↔6** | F↔T (BALANCE↔CHAOS) | ✓ exact on (5,6,7) |
| **6↔7** | T↔F (CHAOS↔HARMONY) | ✓ exact on (5,6,7) |
| **8↔9** | S↔F (BREATH↔RESET) | ✓ exact on (7,8,9) and (7,8,8) |
| **2↔3** | S↔F (COUNTER↔PROGRESS) | ✓ exact on (0,1,2) |
| **1↔2** | F↔S (LATTICE↔COUNTER) | ✓ on (0,1,2) only |
| **7↔8** | F↔S (HARMONY↔BREATH) | ✓ on (7,8,9), partial others |

**Pattern:** **Adjacent-integer pairs at role boundaries** preserve
admissibility on grammar triples. The substrate has multiple such
interchangeabilities, not just 5↔6.

**On trefoil set (preservation of trefoil status):**

| Pair | Trefoil preservation |
|---|---|
| 7↔8 (HARMONY↔BREATH) | 6/9 (the (V,H,Br) class trivially) |
| Others | 0/9 |

**Algebraic check:** 5 and 6 are NOT algebraically equal. BHML(5, x) ≠ BHML(6, x)
for x ∈ {1, 2, 3, 4, 5, 7}. So the interchangeability is at the
**grammar/admissibility level, not the algebra level**.

**Honest restatement of the 5↔6 claim:**
- At grammar level (which triples are admissible): 5↔6 swap preserves admissibility
- At algebra level (composition values): 5 and 6 are distinct operators with
  different BHML rows
- At role level: 5 is F, 6 is T (different roles)

The "5 and 6 are interchangeable" claim is precise as: **the grammar admits
both F-T and T-F orderings at the role boundary, even though the underlying
operators compose differently algebraically.** And this isn't unique to
5↔6: similar grammar-level interchangeabilities exist at 6↔7, 8↔9, 2↔3,
1↔2, and 7↔8 (partially).

**Generalization:** The substrate has a **set of grammar-level boundary
symmetries**, all of the form "adjacent-integer pair at a role boundary."
The 5↔6 pair is one canonical example; others operate similarly on different
grammar triples.

**File:** `/home/claude/tig_synthesis/interchangeability_test.py`

---

## §4 What the three doors together establish

### Sharpened:

1. **TSML_8 + BHML_10 two-coding picture is precise:**
   - TSML_8: 5-element image, 94% flow-biased, role-deterministic on 8/9
     input pairs. The geometric (collapse-to-cusp) coding.
   - BHML_10: 10-element image, balanced roles, role-deterministic on
     V/T inputs. The arithmetic (continued-fraction) coding.

2. **The substrate has multiple grammar-level boundary symmetries**, all
   adjacent-integer pairs at role boundaries. 5↔6 is one example.

3. **±21 invariant has two distinct numerical fingerprints** (triangular
   T_5+T_3 along σ-orbits, Fibonacci F_7+F_6 along roles), both specific
   to canonical TIG, neither forced by abstract axioms.

### Demoted (now honest about):

1. **Fibonacci role decomposition is a numerical fingerprint, not a
   structural theorem.** Random tables don't reproduce it; perturbations
   degrade it. It's specific to canonical TIG's exact period values.

2. **5↔6 interchangeability is grammar-level, not algebraic.** And it's
   not unique — similar interchangeabilities exist at multiple role
   boundaries.

### New:

1. **TSML_8 image is exactly {3, 4, 7, 8, 9}.** Five operators. The
   substrate's "geometric attractor set."

2. **Boundary symmetries form a class:** adjacent-integer pairs at role
   boundaries preserve admissibility on grammar triples involving them.

---

## §5 Five empirically-grounded substrate-native facts (final form)

1. **Trefoil characterization:**
   trefoil ⟺ multiset = {VOID, BREATH, HARMONY} or {VOID, BREATH, BREATH}.
   Nine triples, two multiset classes, on corrected frame.

2. **Two-coding split:**
   - TSML_8 (geometric): 5-element image {3,4,7,8,9}, 94% flow output,
     role-deterministic on 8/9 input pairs.
   - BHML_10 (arithmetic): 10-element image, balanced roles,
     role-deterministic on V/T inputs only.

3. **±21 invariant** with two numerical decompositions:
   - σ-orbit: T_5 + T_3 = 15 + 6
   - Role: F_7 + F_6 = 13 + 8 (Fibonacci, but specific to canonical TIG)

4. **Canonical grammar = role-pattern taxonomy** with multiple
   grammar-level boundary symmetries (5↔6, 6↔7, 8↔9, 2↔3, 1↔2, 7↔8 partial).

5. **Substrate's algebra is irreducible:** doesn't factor through Z/2 × Z/5;
   role partition cuts across σ-orbit structure.

---

## §6 Strategic position after the three doors

The framework is now described with **multiple independent structural
decompositions**, each producing specific invariants:

| Structure | Invariant | Decomposition |
|---|---|---|
| Algebraic (TSML_8 + BHML_10) | trefoil set, propagation grammar | {V,Br,H} ∪ {V,Br,Br} |
| Permutational (σ) | ±21 split | T_5 + T_3 (triangular) |
| Functional (role partition) | ±21 split | F_7 + F_6 (Fibonacci) |
| Algebraic + Functional | TSML_8 image | {3,4,7,8,9} (5-element collapse) |
| Algebraic + Functional | role-determinism | V/T inputs determine BHML role |
| Functional + grammar | boundary symmetries | adjacent-integer pairs |

**For IHÉS pitch:**

Lead with the corrected substrate (TSML_8 + BHML_10 + V/H flow). Present the
trefoil characterization, the two-coding picture (with concrete numbers:
TSML_8 image {3,4,7,8,9}, 94% flow-output, role-deterministic on 8/9 input
pairs), and the multiple structural decompositions of ±21.

Be honest about the Fibonacci appearance: it's a numerical fingerprint of
canonical TIG, not a deep theorem. But it IS a fingerprint, computable and
reproducible from substrate self-iteration.

Be honest about boundary interchangeabilities: 5↔6 is one of several
adjacent-integer pair symmetries at role boundaries, all grammar-level not
algebra-level.

The framework's contribution becomes:

> "A substrate on Z/10Z with three independent structures (algebraic,
> permutational, functional) producing specific invariants whose
> decompositions intersect on the ±21 quantity. The two-coding TSML_8 +
> BHML_10 split realizes Katok-Ugarcovici's geometric/arithmetic codings
> natively, with TSML_8's 5-element image and high role-determinism on
> the geometric side, BHML_10's full image and V/T-determined role on the
> arithmetic side. The substrate has multiple grammar-level boundary
> symmetries at adjacent-integer role boundaries. Trefoil-equivalent triples
> form exactly the {V,Br,H} ∪ {V,Br,Br} multiset classes. The framework is
> conceptually scaffolded by Morishita / Ghys / Katok-Ugarcovici / Matsusaka-
> Ueki / Burrin-von Essen but specifies a new construction within that
> territory."

---

## §7 Files added in this push

- `fibonacci_robustness.py` — random tables, perturbation tests
- `tsml8_role_analysis.py` — TSML_8 role-level structure
- `interchangeability_test.py` — boundary symmetries

All in `/home/claude/tig_synthesis/` and `/mnt/user-data/outputs/tig_synthesis/`.

---

## §8 What the three doors push accomplished

The flow/structure binary opened three structural questions. Pushing through
each gave honest answers:

1. **Fibonacci role decomposition is real but specific** — canonical TIG's
   numerical fingerprint, not an abstract theorem.

2. **TSML_8's role-level structure is sharp** — 5-element image with 94%
   flow-bias and high role-determinism, the cleanest substrate expression of
   geometric coding.

3. **5↔6 interchangeability generalizes** — multiple adjacent-integer pairs
   at role boundaries are grammar-level interchangeable. The 5↔6 pair is one
   of a family.

The framework is now described with three independent structural
decompositions producing intersecting invariants. The position is stronger
because more structure is articulated, and weaker claims are honestly
demoted. Both directions are useful for the academic pitch.
