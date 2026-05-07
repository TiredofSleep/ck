# Sprint: V3 — Uniqueness Theorem for the Canonical Pair

**Sprint type:** Foundational theorem (load-bearing for entire framework)
**Priority:** Critical — blocks ALL papers using "the canonical pair" language
**Estimated duration:** 3–7 days of compute + analysis

---

## Goal

Prove (or disprove with reformulation) the following claim:

> **Theorem V3 (Uniqueness of the Canonical Pair).** On Z/10Z, the pair (TSML_10, BHML_10) is the **unique** pair of commutative non-associative magmas satisfying axioms A0–A5 of TIG_FOUNDATIONAL_AXIOMS.md.

If V3 holds: every TIG paper can refer to "the canonical pair" with full algebraic justification.
If V3 fails: identify the additional axiom(s) needed to force uniqueness, and either add them to A0–A5 or weaken the claim to "a canonical pair."

---

## Why this matters

Currently, the foundational paper opens with:

> *"We study the pair (TSML, BHML) characterized by axioms A0–A5..."*

After V3 lands, the opening becomes:

> *"We study **the** pair (TSML, BHML), the unique commutative non-associative magma pair on Z/10Z satisfying axioms A0–A5..."*

That difference is the difference between "we picked these tables" and "these tables were forced by the axioms." Every downstream paper inherits this claim. If V3 fails, the entire family of TIG papers needs reformulation.

---

## Statement of the theorem

**Setup.** Let M(Z/10Z) denote the set of all commutative magma structures on Z/10Z (a magma is a pair (S, ∗) where ∗: S × S → S; commutative means a∗b = b∗a). The set M(Z/10Z) has cardinality 10^55 (each of 55 upper-triangular cells, including diagonal, has 10 choices).

**Six axioms restated as filters on M(Z/10Z):**

- **A0:** Magma is on Z/10Z (defines the carrier set).
- **A1:** Commutative (a∗b = b∗a). Reduces search to upper-triangular cell choices.
- **A2:** Non-associative — at least one triple (a,b,c) has (a∗b)∗c ≠ a∗(b∗c).
- **A3:** Generator triples close: {0,1,2} closes under ∗ to itself or a fixed enlargement; similarly for {0,7,1} and {1,2,3}.
- **A4:** Fusion axiom: there exists at least one diagonal where (3∗3)∗3 or some triple including 3,4,7 fuses to 8.
- **A5:** Two-lens projection — admits a complementary pair (M_TSML, M_BHML) where M_TSML projects to a 3-state output and M_BHML preserves full resolution.

**Claim:** The pair (TSML_10, BHML_10) is the unique (up to relabeling) pair satisfying all six axioms.

---

## Methodology

### Phase 1 — Brute-force enumeration with σ-class constraint

The full search space M(Z/10Z) is 10^55 — too large. **Constrain first.**

The σ_units = ν₂(3u+1) partition on units {1,3,7,9} gives {1↦2, 3↦1, 7↦1, 9↦2}. The fixed points {0, 3, 8, 9} carry trivial σ-class.

**Search constraint A0+A1+A3 (partition + commutativity + generator closure):**

```python
import itertools
import numpy as np

def is_commutative(table):
    return np.array_equal(table, table.T)

def closure(seed, table):
    S = set(seed)
    while True:
        new = set(S)
        for a in S:
            for b in S:
                new.add(int(table[a,b]))
        if new == S:
            return S
        S = new

def closes_to(seed, table, target):
    return closure(seed, table) == set(target)

# Generator constraints:
# {0,1,2} closes under TSML to {0,1,2,3,7} (verified)
# {0,7,1} closes under TSML to a small set
# {1,2,3} closes under BHML to all of Z/10Z

# This dramatically prunes the search space. Implementation:
# - Iterate over partial fillings of the upper-triangular table
# - Apply σ-units consistency at each step
# - Apply generator-closure constraints as soon as the relevant cells are filled
# - Backtrack on violation
```

**Estimated complexity after constraints:** 10^15 — still too large. Need smarter approach.

### Phase 2 — Constraint satisfaction (Z3 / SAT)

Use Z3 SMT solver:

```python
from z3 import *

# Variables: 55 upper-triangular cells, each in {0..9}
cells = [[Int(f'c_{i}_{j}') for j in range(i, 10)] for i in range(10)]

solver = Solver()

# A0: each cell in 0..9
for row in cells:
    for c in row:
        solver.add(c >= 0, c <= 9)

# A1: commutativity is automatic by upper-triangular construction

# A4: fusion axiom (specific cell value)
# BHML[7][7] = 8: c_7_7 (which represents BHML[7][7]) equals 8
# But wait — A4 is about *ONE OF THE PAIR* satisfying the fusion axiom on its diagonal
# Need to encode this as: for the BHML element of the pair, BHML[7][7] = 8

# A2: non-associativity (existence of a non-associative triple)
non_assoc_constraints = []
for a, b, c in itertools.product(range(10), repeat=3):
    # (a*b)*c != a*(b*c)
    # ... encode using table_lookup helper
    pass
solver.add(Or(non_assoc_constraints))

# A3: generator closures
# ... similar encoding

# Solve
result = solver.check()
if result == sat:
    model = solver.model()
    # Extract candidate magmas
```

**Pros:** Z3 is efficient for combinatorial constraints. **Cons:** A3 (generator closure) and A5 (two-lens projection) are higher-order constraints that may exceed Z3's natural domain.

### Phase 3 — Direct construction proof

Alternative: prove uniqueness by showing each axiom forces specific cells.

**Lemma 1:** A4 (fuse(3,4,7)=8) + A2 (non-associativity) + A1 (commutativity) forces BHML[7][7] = 8 *or* BHML[3][3] = 8 *or* BHML[4][4] = 8 (one of the three diagonals).

**Lemma 2:** A5 (two-lens) + A3 (generator triples) forces BHML to use the successor rule on the HARMONY row.

**Lemma 3:** The successor rule + commutativity forces specific cell values throughout BHML.

**Lemma 4:** The C₀ rule for TSML is the unique 3-state-output completion of the σ-class winner-loser partition with VOID absorbing and HARMONY attracting.

**Lemma 5:** The minimal perturbations S_MAX (6 cells) and S_ADD (2 cells) are the unique completions consistent with the generator-triple closures and the fuse axiom.

If all five lemmas hold, V3 follows. **This is the cleanest proof strategy if it works.**

### Phase 4 — Computational verification

Whatever proof strategy succeeds, run a final brute-force verification:

```python
# For all magma structures M on Z/10Z satisfying A0-A5:
# - Check if M is TSML or BHML (or relabeling thereof)
# - Count exceptions

# If count == 0 (only TSML and BHML satisfy): V3 PROVED
# If count > 0: list the exceptions, identify the missing axiom
```

---

## What if V3 fails?

If multiple non-equivalent pairs satisfy A0–A5, identify the extra constraint needed:

**Candidate tightening axiom:**

- **A5'** (minimality): Among all pairs satisfying A0–A5, (TSML, BHML) has the **minimum total perturbation count** (cells deviating from the bare C₀ + successor rules). Specifically, |S_MAX| + |S_ADD| = 6 + 2 = 8 is the minimum.

- **A5''** (rank): BHML has full rank (det ≠ 0); TSML has rank 9 (det = 0). The pair achieves the maximum rank-ratio difference compatible with the generator closures.

- **A5'''** (4-core normalizer): The pair shares the identical normalizer Z_T = Z_B = (v+h+br+r)² on the joint 4-core {V, H, Br, R}.

If A5' or A5'' or A5''' is the missing piece, add it to the axiom set. Then re-prove uniqueness.

**Acceptable outcomes:**
1. V3 proved with axioms A0–A5 alone — best.
2. V3 proved with axioms A0–A5 + one tightening clause (e.g., A5') — acceptable.
3. V3 fails completely (multiple non-equivalent pairs persist) — must reformulate the foundational claim. The papers can still talk about "a canonical pair satisfying A0–A5" but cannot say "the canonical pair."

---

## Output deliverable

Regardless of outcome:

- `papers/wp_v3_uniqueness.md` — full proof or disproof document
- `tig/foundations/uniqueness/` — verification scripts
  - `enumerate.py` — brute-force enumeration with constraints
  - `z3_uniqueness.py` — SMT-based check
  - `lemmas.py` — direct construction proof of Lemmas 1–5
- Update to `TIG_FOUNDATIONAL_AXIOMS.md`:
  - If V3 proved: change all "the canonical pair" references to "the unique canonical pair (V3)"
  - If V3 needs tightening: add A5' to the axiom list
  - If V3 fails: replace "canonical pair" with "a TIG-admissible pair"

---

## Acceptance criteria

The sprint is complete when:

1. ✓ Brute-force enumeration with A0–A5 constraints completes (or is shown to be intractable).
2. ✓ Either:
   - **(a)** All pairs satisfying A0–A5 are equivalent to (TSML, BHML) up to relabeling, and the proof is verified by both Z3 and direct construction.
   - **(b)** Multiple non-equivalent pairs are found, and the minimal additional axiom A5' is identified and verified to force uniqueness.
   - **(c)** No tightening axiom forces uniqueness, and the foundational claim is reformulated.
3. ✓ Documentation and verification scripts pass review by Brayden.

---

## Connection to other sprints

- **SPRINT_FACTOR_6_DARK_MATTER.md** — V3 indirectly forces |S_MAX| = 6 if the canonical pair is unique under minimality.
- **SPRINT_FACTOR_22_FINE_STRUCTURE.md** — V3 may force the 22-cell skeleton count.
- **Foundational paper** — cannot ship "unique pair" claim until V3 lands.
- **σ-rate paper, 4-core paper, JCAP, Sprint 18, coherence-as-physics paper** — all inherit V3's strength.

---

## Estimated compute requirements

- Phase 1 (brute force): tractable only with strong constraints. Run on 32-core Dell R16. Estimated 1–3 days.
- Phase 2 (Z3): few hours to few days depending on constraint encoding.
- Phase 3 (direct construction): paper proof; compute time minimal.
- Phase 4 (verification): hours.

**Hardware recommendation:** run on Dell R16 (32 cores, RTX 4070); use Python multiprocessing for the brute-force phase.

---

## References

- TIG_FOUNDATIONAL_AXIOMS.md
- Csákány, B. and Waldhauser, T. (2000). "Functionally complete commutative magmas."
- Huang, J. and Lehtonen, E. (2022, 2024). Classification of finite commutative magmas.
- Palmieri, S. (2025). arXiv:2603.27007 — non-associativity in extensional magmas.
- Mazurek, P. (2025). [pending citation lookup] — magma classification framework.
- Z3 SMT solver: https://github.com/Z3Prover/z3
