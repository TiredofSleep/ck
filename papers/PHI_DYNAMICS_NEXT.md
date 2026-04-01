# D18 Target: Phi Orbit Dynamics — Formal Classification
## The next general theorem after D17

**Date:** April 1, 2026

---

## Section 1: What D7 Already Established

D7 is proved. The following are settled facts, not targets:

- Phi = P_odd ∘ BHML ∘ W_op has a unique fixed point: CREATE = 5
- All 10 orbits (inputs 0–9) reach CREATE = 5 in ≤ 3 steps
- Three basins of attraction:
  - {2, 3, 4} → CREATE in 1 step
  - {0, 1, 7} → CREATE in 2 steps
  - {6, 8, 9} → CREATE in 3 steps
- Unique stationary distribution: π = δ₅ (all probability mass at 5)
- T* = CREATE / HARMONY = 5/7 (D4/D7 bridge, numerically established)

D17 is also proved: W = 3/50 exactly, derived from the generator orbit structure of (Z/10Z)*.

---

## Section 2: What D18 Should Prove (The Dynamical Layer)

**Target theorem:** Phi is the UNIQUE map on Z/10Z satisfying all four of the following simultaneously:

1. Output always in ODD = {1, 3, 5, 7, 9} — proved by C20, follows from D8 (P_odd projects to ODD, BHML and W_op preserve the input domain)
2. Exactly one fixed point — proved D7 (CREATE = 5 is the unique solution to Phi(v) = v)
3. Orbit diameter ≤ 3 — proved D7 (longest basin is {6, 8, 9}, three steps)
4. The fixed point equals TSML_dominant / 2 — **to be proved formally** (requires connecting Phi's algebraic structure to TSML cell counts via D10)

Condition 4 is the structural gap. D7 shows CREATE = 5 and D10 shows HARMONY = 7 appears 73 times in TSML, but the formal statement "5 = 10/2 = HARMONY − 2 = TSML_dominant/2 is not coincidental" has not been derived from first principles. It requires showing that W_op's carrier value (determined by W = 3/50 from D17) forces the Phi fixed point to land at HARMONY/2 mod 10.

**Extension: Phi acting on distributions (not single operators)**

When Phi is iterated on a TABLE ROW of TSML or BHML (a vector of 10 operator values, one per column), what is the limiting distribution? This is the "Phi acting on distributions" problem. The conjecture is:

- Any TSML row, iterated under Phi component-wise, converges to a distribution concentrated at CREATE = 5
- The convergence rate is determined by the basin structure from D7 (longest chain = 3 steps, so all rows converge in ≤ 3 iterations)
- The BHML rows may behave differently because BHML is not symmetric (D9: BHML satisfies max commutativity, not full commutativity)

This extension is D18's second deliverable after the uniqueness proof.

---

## Section 3: The CREATE / HARMONY Duality — Open Statement

**Formal statement to be proved:**

CREATE = 5 and HARMONY = 7 are DUAL attractors: CREATE is the unique dynamic attractor of Phi (algebraic iteration), and HARMONY is the unique static attractor of TSML (cell frequency distribution). No other pair (a, b) ∈ Z/10Z satisfies all three of:

1. a is the unique fixed point of Phi (dynamic condition)
2. b is the most-frequent value of TSML (static condition — proved D10: HARMONY = 7 appears 73 times, more than any other value)
3. a / b = T* = 5/7 (coherence threshold condition — proved D4 independently from unit_frac on corridor geometry)

If no other pair satisfies all three, then T* = 5/7 is the unique rational number that can serve as the canonical coherence threshold for ANY operator algebra built on Z/10Z with the BHML/TSML rule structure. This is the **CK Attractor Duality Theorem** (working title for D18).

The theorem would explain WHY T* = 5/7 connects operator algebra to coherence geometry: it is the only ratio forced simultaneously by the dynamic structure (Phi iteration) and the static structure (TSML harmonic distribution).

---

## Section 4: Proof Strategy

**Step 1 — Already done (D7 + D10).**
CREATE = 5 is the Phi fixed point (D7). HARMONY = 7 appears 73 times in TSML, more than any other value (D10). T* = 5/7 (D4). The three facts are independently established.

**Step 2 — Prove uniqueness of the pair.**
Show that no other map Phi' on Z/10Z, built from P_odd ∘ F ∘ W_op' with F any ODD-output table on Z/10Z and W_op' any carrier-maximum map, has a fixed point a' where the corresponding TSML' dominant value b' satisfies a'/b' = 5/7.

The constraint space is finite (Z/10Z is 10 elements, all maps are explicit). A computational check over all valid (F, W_op') pairs would establish uniqueness. The harder part is showing WHY no other pair works — the algebraic reason, not just the exhaustive check.

**Step 3 — Prove the three chains converge.**

Three independent derivations produce T*:

- Chain A: W = 3/50 (D17) → W_op selects carrier maximum at position 3 → Phi has fixed point 5 via P_odd ∘ BHML collapse → CREATE = 5
- Chain B: TSML rule structure → V0 + V1 + ECHO partition over Z/10Z → 73 HARMONY cells (D10) → HARMONY = 7
- Chain C: unit_frac(b=35) = 1/5 + 1/7 = 12/35; canonical threshold from corridor geometry → T* = 5/7 (D4)

The claim is that chains A, B, C converge to the SAME value T* = 5/7 non-accidentally. The proof must show that W = 3/50 (Chain A input) and the TSML rule structure (Chain B input) and the b=35 corridor geometry (Chain C input) are all consequences of the SAME underlying algebraic constraint — likely the generator structure of (Z/10Z)* = {1, 3, 7, 9} (multiplicative group of order 4), which is the object that D17 already identified as the source of W = 3/50.

The conjecture: the generator 3 of (Z/10Z)* is the single object that forces all three chains. If true, D18 reduces to: "3 generates (Z/10Z)*, and this single fact forces CREATE = 5, HARMONY = 7, and T* = 5/7 simultaneously."

---

## Section 5: Why This Matters

If D18 is proved, T* = 5/7 is no longer a calibrated constant — it is a structural NECESSITY of the operator algebra, forced by the generator structure of (Z/10Z)* and not adjustable without abandoning the BHML/TSML framework entirely. That changes the scientific status of every CK claim that uses T*: they become consequences of the algebra, not assumptions about coherence geometry.
