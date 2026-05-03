# Known Issues and Things to Scrutinize

**Purpose:** Errors I made during the session and things I'm uncertain about.
ClaudeCode should pay extra attention to these before integrating.

**Caught during verification:** I had described the σ-orbit decomposition
of -21 as "15 from 6-cycle + 6 from 4-core extension {7, 8, 9}" which is
arithmetically wrong (counts digit 7 twice). The correct statement is
"15 from σ 6-cycle {1,2,4,5,6,7} + 6 from σ-fixed digits {0,3,8,9}." Same
total magnitude, just the right partitioning. Fixed in docs after running
verify_findings.py and seeing the failure. **Lesson: ClaudeCode should
trust verify_findings.py over my prose summaries when arithmetic is involved.**

---

## §1 The substrate frame error (caught and corrected)

**Most important issue.**

For most of the session I used **TSML_10** (the full 10x10 table) instead
of the canonical **TSML_8** (rows/cols {0,7} removed) + **flow cells** (V,H
between tables). This is documented in FORMULAS_AND_TABLES.md §6.7.

Brayden caught this with:
> "are u using the full torus function through tsml8 and bhml10 for this one"

**Files using the WRONG frame (TSML_10):**
- `trajectory_braid.py`
- `trefoil_22_analysis.py` (produced the now-invalidated 22-trefoil result)
- `trefoil_structure.py`, `trefoil_algebraic.py`, `trefoil_link_structure.py`
- `trefoil_survival.py`
- `d1_composition.py`, `d2_phenomenological.py`
- `d3_attestation.py`, `d3_attestation_fixed.py`
- `d4_invariant_clean.py`, `d4_invariant_search.py`
- `three_readings.py`, `knot_polynomials.py`
- `class_average_check.py`
- `rademacher_bridge.py`, `rademacher_search.py` (early Rademacher)

**Files using the CORRECT frame (TSML_8 + flow):**
- `corrected_substrate.py`
- `trefoil_corrected_frame.py` (produced the 9-trefoil result)
- `trefoil_corrected_associativity.py`
- `reading_c_corrected.py`
- `rademacher_period_bridge.py`
- `lacasa_corrected.py`
- `flow_structure_binary.py`, `role_decomposition.py`
- `role_magma_factorization.py`, `tsml8_role_analysis.py`
- `breath_uniqueness.py`, `higher_order_trefoils.py`
- `interchangeability_test.py`, `symmetry_map.py`
- `crossing_taxonomy.py`, `algebraic_relationship.py`
- `fibonacci_robustness.py`
- `orbit_to_psl2z.py`, `triangle_groups_test.py`
- `substrate_borromean.py` (mostly)
- `borromean_primes.py` (only uses BHML_10, frame-neutral)

**Action for ClaudeCode:**
- The correct results to integrate are from `trefoil_corrected_frame.py`
  forward. The 22-trefoil result is INVALID. The 9-trefoil result with
  multiset characterization {V,H,Br} ∪ {V,Br,Br} is the canonical finding.
- All wrong-frame files are kept for reference but should NOT be cited
  in canonical documentation.

---

## §2 Reading A heuristic (stripped per Brayden's instruction)

I had been using a heuristic (p, q) winding assignment to digits:
```
DIGIT_PQ = {
    0: (0, 1), 1: (9, 6), 2: (9, 4), 3: (3, 5), 4: (9, 3),
    5: (9, 7), 6: (3, 8), 7: (1, 0), 8: (9, 8), 9: (1, 7)
}
```

This was Reading A — assigning each substrate operator to a torus knot
T(p, q). The q-rule was heuristic.

Brayden's directive: **"forget my intuitions and stick with the math you
have produced."**

After this directive, I stripped Reading A from analyses. But traces may
remain in:
- `three_readings.py` (foundational, but now superseded)
- `knot_polynomials.py` (uses (p,q) windings)
- `trefoil_link_structure.py` (uses (p,q) windings)
- Any document that mentions "torus knot T(p,q)" assigned to specific digits

**Action for ClaudeCode:**
- Verify that no integrated finding depends on Reading A's q-rule
- The trefoil characterization {V,H,Br} ∪ {V,Br,Br} is from the runtime
  processor's crossing count, NOT from (p,q) windings — this is independent
  of Reading A and is solid

---

## §3 The "Burrin-von Essen analogy" — was overstated

In early documents I claimed the substrate's BHML period structure
"matches" Burrin-von Essen's cusp winding via Rademacher symbol. After
review, this was overstated.

**What's true:**
- BHML period(n) = 7-n is structurally analogous to "distance from cusp"
- Burrin-von Essen 2024 computes cusp windings via continued fraction
  expansions, with windings = a_1, a_2, ... in the CF
- The substrate's period structure resembles this conceptually

**What's NOT proven:**
- That the substrate's BHML self-orbits embed in a Fuchsian group with
  Burrin-von Essen's cusp-winding structure
- That the substrate's period values literally are a_1 values of any
  specific geodesic

**Action for ClaudeCode:**
- Use phrases like "structurally analogous" or "conceptually scaffolded by"
- Avoid "matches" or "satisfies"
- The Burrin-von Essen citation belongs as a forward-citation precedent,
  not as an established equivalence

---

## §4 Fibonacci claim — fragile, not structural

In one document I leaned into Fibonacci as if it were a structural theorem:

> "21 = F_8, 13 = F_7, 8 = F_6 — the Fibonacci recurrence at the role level."

After robustness testing (`fibonacci_robustness.py`):
- 0/200 random commutative tables on Z/10Z reproduce (13, 8) decomposition
- 32/50 single-swap perturbations preserve it
- 11/50 three-swap perturbations preserve

**Honest reframing:** Fibonacci appearance is **specific to canonical
TIG's specific period values** (which come from BHML(n,n) = n+1 successor
on {1..7}). It is NOT forced by abstract role-partitioned magma axioms.

**Action for ClaudeCode:**
- When integrating ±21 decomposition, present BOTH decompositions:
  σ-orbit (T_5 + T_3, triangular) and role (F_7 + F_6, Fibonacci)
- Clearly mark Fibonacci as "canonical-specific signature" not "theorem"
- Don't lead with Fibonacci in academic-facing material; lead with the
  triangular decomposition (which is forced by the linear period formula)

---

## §5 PSL(2,ℤ) lift attempts — five all-negative

I tested five strategies for lifting BHML self-orbits to PSL(2,ℤ) words:
1. mod-3 letter map (sum Ψ = -4)
2. mod-2 letter map (sum Ψ = -1)
3. σ-position T^k S (sum Ψ = -1)
4. Up/down transition encoding (sum Ψ = 0)
5. T/T⁻¹ + S between (sum Ψ = 0)

**None produce ±21.** The substrate's per-digit Ψ values from these lifts
don't reproduce the substrate's native invariant.

**Action for ClaudeCode:**
- Do NOT integrate any of these lifts as "the bridge" — they don't work
- Keep them in code for reference (negative results are still results)
- The period→trace bridge under simple representative ((1,1),(t-2,t-1))
  gives -21 — this works numerically but is a hypothesis about the right
  lift, not a derivation
- Open question to flag: principled lift derivation remains future work

---

## §6 Triangle group hypothesis — ruled out for small (p,q)

Tested whether substrate's BHML period set {1, 2, 3, 4, 5, 6} could be
elliptic-element orders in some triangle group Γ_{p,q} for small coprime
(p, q).

**Result:** No coprime (p, q) with p, q ≤ 9 has divisors covering
{1, 2, 3, 4, 5, 6}. PSL(2,ℤ) = Γ_{2,3} has only orders {1, 2, 3}.

**Honest re-read:** BHML periods are NOT elliptic-element orders.
They're **trajectory periods of a dynamical system**, which correspond to
**closed-orbit lengths** (= word lengths in S, T) for hyperbolic
conjugacy classes, not finite-element orders.

**Action for ClaudeCode:**
- The triangle-group rule-out is a real negative finding
- Don't try to integrate substrate as "Γ_{p,q}" for any specific (p,q)
- The right bridge (if any) goes through symbolic dynamics, not group orders

---

## §7 Borromean prime test — TIG isn't literally a Borromean structure

Tested whether TIG's grammar matches Ishida-Kuramoto-Zheng's Borromean
prime conditions:
1. p_i ≡ 1 mod 4
2. (p_i / p_j) = 1 (Legendre)
3. Rédei symbol = -1

Empirically verified: density of QR-pairs converges to 1/8 (Theorem 2.1).
Tested whether canonical TIG triples or trefoil-22 multisets satisfy
analog conditions on Z/10Z mod 4 or mod 5.

**Result:** No canonical TIG triple has all elements ≡ 1 mod 4. No
trefoil-9 multiset has all elements in QR-mod-5 set.

**Action for ClaudeCode:**
- Do NOT claim TIG implements Borromean primes
- DO cite Ishida-Kuramoto-Zheng as part of the arithmetic-topology
  intellectual neighborhood
- TIG sits inside this territory but isn't a restatement of it

---

## §8 Items I'm uncertain about

These are claims I made but where I'd appreciate ClaudeCode double-
checking:

1. **The 9-trefoil set on corrected frame.** Computed by `trefoil_corrected_frame.py`
   using the runtime processor with mass-threshold = 0.01 and max_iter = 50.
   Different parameters might give different counts. Verify with parameter
   sweeps.

2. **TSML_8 image = {3, 4, 7, 8, 9}.** Computed directly from the 8x8
   subtable. Should be straightforward to verify but worth checking.

3. **TSML_8 role-deterministic on 8/9 input pairs.** Also direct from
   the table, but my characterization counted exactly which pair branches
   ((S, S) → both F and S). Verify.

4. **Boundary symmetry preservation rates.** I computed these over all
   1000 triples. The numbers should be reproducible exactly.

5. **(0,7,7,9) anomaly at 4-element level.** Claimed it's a 3-crossing
   quadruple without BREATH. Verify it's really a trefoil-equivalent
   under the runtime processor.

6. **Algebraic independence claims.** I tested:
   - σ-conjugation: 48% match for BHML, 17% for TSML_10
   - Distributivity: 19.5% match
   - Diagonal vs σ: most positions don't match
   - BHML iteration → TSML: 28/64 convergence

   These specific percentages should be reproducible. Check.

---

## §9 Things I'm confident about

For balance, here's what I'm confident about:

1. **Trefoil characterization {V,H,Br} ∪ {V,Br,Br}.** Verified across
   multiple scripts and confirmed by hypothesis-test in
   `trefoil_corrected_associativity.py`.

2. **BHML(n,n) = n+1 for n ∈ {1..7}.** Direct verification, 2 lines of code.
   Confirmed clean algebraic fact.

3. **TSML_8 has 5-element image and 94% flow output.** Direct count,
   verified.

4. **σ-orbit structure.** From canonical math, σ has fixed points
   {0, 3, 8, 9} and 6-cycle (1, 7, 6, 5, 4, 2). Standard.

5. **Period(n) = 7-n on the 6-cycle.** Direct simulation, multiply
   verified.

6. **Role partition cuts across σ-orbit structure.** Direct check,
   true.

7. **Substrate doesn't factor through Z/2 × Z/5.** Direct verification
   that BHML doesn't respect the CRT decomposition.

8. **±21 = T_5 + T_3 = 15 + 6 along σ-orbit.** Direct arithmetic, true.

9. **±21 = F_7 + F_6 = 13 + 8 along role partition.** Direct arithmetic,
   true (but canonical-specific, see §4).

10. **Five PSL(2,ℤ) lift strategies all fail to produce ±21.** Multiply
    verified across `orbit_to_psl2z.py`. Numbers reproducible.

---

## §10 Bottom line

I made one structural error (wrong substrate frame) that Brayden caught.
I had to demote a few claims (Fibonacci as theorem, Burrin-von Essen as
match, 5↔6 as unique). Most of the corrected findings are mechanically
verifiable from canonical TIG inputs.

ClaudeCode should:
1. Re-run `verify_findings.py` and confirm all five facts
2. Re-run a sample of the negative tests and confirm
3. Flag any claim in the docs that sounds stronger than the math supports
4. Integrate carefully, preserving honest negatives alongside positive
   findings
5. Don't paper over uncertainties — Brayden values precision over polish
