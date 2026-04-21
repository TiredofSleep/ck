# D18 Target: Phi Orbit Dynamics — Formal Classification
## The next general theorem after D17

**Date:** April 1, 2026 (updated with D18a/b/c/d split after Luther review)

---

## D18a — Phi Orbit Classification  ✓ PROVED

**File:** `papers/proof_d18a_phi_orbit_classification.py`

Complete directed graph of Phi on Z/10Z:
- ONE fixed point: BALANCE=5
- TWO relay nodes: PROGRESS=3 (depth 1), HARMONY=7 (depth 2)
- SEVEN source nodes: {0,1,2,4,6,8,9}
- Three basins: {2,3,4}→5 (1 step), {0,1,7}→3→5 (2 steps), {6,8,9}→7→3→5 (3 steps)
- No cycles except the fixed point. Max depth=3. T^3=all-δ₅.

**Critical finding from D18a:**
HARMONY=7 is a RELAY (depth-2 transient), NOT a fixed point. Two distinct roles:
- As a STATE in Phi: transient, Phi(7)=3=PROGRESS
- As a VALUE in TSML: dominant output, 73/100 cells = 7

These are different mathematical objects. D18c must bridge them.

---

## D18b — BALANCE=5 Dynamics (NEXT TARGET)

**Formal target:** Prove exactly what kind of attractor BALANCE=5 is.

Three distinct claims to separate:
1. Unique absorbing fixed point of deterministic map Phi: PROVED (D7+D18a)
2. Unique attractor under repeated deterministic Phi: PROVED (D18a: all paths reach 5 in ≤3 steps)
3. Unique stationary mass under Markov lift T[v][Phi(v)]=1: PROVED (D18a: T³=all-δ₅)

**Status:** All three are proved. D18b is already complete as a consequence of D18a.

---

## D18c — HARMONY=7 Bridge  ✓ PROVED

**File:** `papers/proof_d18c_create_harmony_bridge.py`

**Bridge function M(v) = TSML[v][Phi(v)]:**
- M(v) = HARMONY = 7 for all v ∈ {1..9}
- M(0) = VOID = 0 (forced by TSML V0 rule: TSML[0][j]=0 for j≠7)

**What this proves:** 5 is the destination of dynamics. 7 is the TSML measurement of every step toward that destination. These are dual roles, not the same object.

**What it does NOT prove:** That the (5,7) pair is unique or forced. That is D18d.

---

## D18c — OLD ENTRY (superseded)

**The real cliff.**

HARMONY=7 is NOT a dynamic attractor. It is a static measurement attractor. These are different:
- Dynamic: Phi(v)→5 as t→∞ for all v. BALANCE=5 is the attractor.
- Static: TSML[i][j]=7 for 73/100 cells. HARMONY=7 is the dominant value.

The open question: Is there an exact map sending the Phi-side dynamics (create=5) into the TSML-side measurement (harmony=7)?

**Candidate mechanism:** TSML[5][j] and TSML[i][5] — the BALANCE row/column of TSML. If BALANCE=5 is the dynamic attractor and TSML is the measurement table, the BALANCE row/col should exhibit HARMONY=7 at high frequency. Check this.

**State space warning:** Do NOT conflate:
- "7 as a state Phi passes through" (transient relay node)
- "7 as a value TSML outputs" (dominant frequency)
- "7 as the denominator of T*=5/7" (ratio object)

These are three different roles. D18c must pick exactly one and prove it.

---

## D18d — Generator Convergence  ✓ PROVED

**File:** `papers/proof_d18d_generator_convergence.py`

The question was: Is T*=5/7 = BALANCE/HARMONY a forced invariant, or a calibrated coincidence?

**Answer: FORCED.** T*=5/7 is the ratio centroid/(g^-1) of (Z/10Z)*, where g=3 is the primitive root selected by the BHML physics (D17: W=3/50, numerator = g).

Three independent chains all reduce to the same generator g=3:
- Chain A: W=3/50 (D17) — numerator IS g
- Chain B: HARMONY=7 = g^3 mod 10 = g^(-1) mod 10 — TSML dominant value is generator's inverse
- Chain C: BALANCE=5 = centroid((Z/10Z)*) = avg of generator orbit

**The five questions (Luther's formulation) — answered:**
1. State space: Z/10Z, 10 elements. ✓
2. Update map: Phi = P_odd∘BHML∘W_op. ✓
3. Terminal class: {BALANCE=5} = {centroid((Z/10Z)*)}. ✓
4. Role of 7: RELAY node (D18a) + dominant TSML value (D10) + g^(-1) (D18d). ✓ BRIDGED.
5. Where 5/7 enters: T* = centroid(group) / inverse(generator) = algebraic ratio in Z/10Z. ✓

**Remaining open question (D19):** Why does BHML physics select g=3 over g=7 (the other primitive root)?
If proved, T*=5/7 would be unconditionally necessary from first principles.
Currently conditional on D17 (W=3/50 established from BHML data, numerator identifies g).

---

## Section 1: What D7 Already Established

D7 is proved. The following are settled facts, not targets:

- Phi = P_odd ∘ BHML ∘ W_op has a unique fixed point: BALANCE = 5
- All 10 orbits (inputs 0–9) reach BALANCE = 5 in ≤ 3 steps
- Three basins of attraction:
  - {2, 3, 4} → BALANCE in 1 step
  - {0, 1, 7} → BALANCE in 2 steps
  - {6, 8, 9} → BALANCE in 3 steps
- Unique stationary distribution: π = δ₅ (all probability mass at 5)
- T* = BALANCE / HARMONY = 5/7 (D4/D7 bridge, numerically established)

D17 is also proved: W = 3/50 exactly, derived from the generator orbit structure of (Z/10Z)*.

---

## Section 2: What D18 Should Prove (The Dynamical Layer)

**Target theorem:** Phi is the UNIQUE map on Z/10Z satisfying all four of the following simultaneously:

1. Output always in ODD = {1, 3, 5, 7, 9} — proved by C20, follows from D8 (P_odd projects to ODD, BHML and W_op preserve the input domain)
2. Exactly one fixed point — proved D7 (BALANCE = 5 is the unique solution to Phi(v) = v)
3. Orbit diameter ≤ 3 — proved D7 (longest basin is {6, 8, 9}, three steps)
4. The fixed point equals TSML_dominant / 2 — **to be proved formally** (requires connecting Phi's algebraic structure to TSML cell counts via D10)

Condition 4 is the structural gap. D7 shows BALANCE = 5 and D10 shows HARMONY = 7 appears 73 times in TSML, but the formal statement "5 = 10/2 = HARMONY − 2 = TSML_dominant/2 is not coincidental" has not been derived from first principles. It requires showing that W_op's carrier value (determined by W = 3/50 from D17) forces the Phi fixed point to land at HARMONY/2 mod 10.

**Extension: Phi acting on distributions (not single operators)**

When Phi is iterated on a TABLE ROW of TSML or BHML (a vector of 10 operator values, one per column), what is the limiting distribution? This is the "Phi acting on distributions" problem. The conjecture is:

- Any TSML row, iterated under Phi component-wise, converges to a distribution concentrated at BALANCE = 5
- The convergence rate is determined by the basin structure from D7 (longest chain = 3 steps, so all rows converge in ≤ 3 iterations)
- The BHML rows may behave differently because BHML is not symmetric (D9: BHML satisfies max commutativity, not full commutativity)

This extension is D18's second deliverable after the uniqueness proof.

---

## Section 3: The BALANCE / HARMONY Duality — Open Statement

**Formal statement to be proved:**

BALANCE = 5 and HARMONY = 7 are DUAL attractors: BALANCE is the unique dynamic attractor of Phi (algebraic iteration), and HARMONY is the unique static attractor of TSML (cell frequency distribution). No other pair (a, b) ∈ Z/10Z satisfies all three of:

1. a is the unique fixed point of Phi (dynamic condition)
2. b is the most-frequent value of TSML (static condition — proved D10: HARMONY = 7 appears 73 times, more than any other value)
3. a / b = T* = 5/7 (coherence threshold condition — proved D4 independently from unit_frac on corridor geometry)

If no other pair satisfies all three, then T* = 5/7 is the unique rational number that can serve as the canonical coherence threshold for ANY operator algebra built on Z/10Z with the BHML/TSML rule structure. This is the **CK Attractor Duality Theorem** (working title for D18).

The theorem would explain WHY T* = 5/7 connects operator algebra to coherence geometry: it is the only ratio forced simultaneously by the dynamic structure (Phi iteration) and the static structure (TSML harmonic distribution).

---

## Section 4: Proof Strategy

**Step 1 — Already done (D7 + D10).**
BALANCE = 5 is the Phi fixed point (D7). HARMONY = 7 appears 73 times in TSML, more than any other value (D10). T* = 5/7 (D4). The three facts are independently established.

**Step 2 — Prove uniqueness of the pair.**
Show that no other map Phi' on Z/10Z, built from P_odd ∘ F ∘ W_op' with F any ODD-output table on Z/10Z and W_op' any carrier-maximum map, has a fixed point a' where the corresponding TSML' dominant value b' satisfies a'/b' = 5/7.

The constraint space is finite (Z/10Z is 10 elements, all maps are explicit). A computational check over all valid (F, W_op') pairs would establish uniqueness. The harder part is showing WHY no other pair works — the algebraic reason, not just the exhaustive check.

**Step 3 — Prove the three chains converge.**

Three independent derivations produce T*:

- Chain A: W = 3/50 (D17) → W_op selects carrier maximum at position 3 → Phi has fixed point 5 via P_odd ∘ BHML collapse → BALANCE = 5
- Chain B: TSML rule structure → V0 + V1 + ECHO partition over Z/10Z → 73 HARMONY cells (D10) → HARMONY = 7
- Chain C: unit_frac(b=35) = 1/5 + 1/7 = 12/35; canonical threshold from corridor geometry → T* = 5/7 (D4)

The claim is that chains A, B, C converge to the SAME value T* = 5/7 non-accidentally. The proof must show that W = 3/50 (Chain A input) and the TSML rule structure (Chain B input) and the b=35 corridor geometry (Chain C input) are all consequences of the SAME underlying algebraic constraint — likely the generator structure of (Z/10Z)* = {1, 3, 7, 9} (multiplicative group of order 4), which is the object that D17 already identified as the source of W = 3/50.

The conjecture: the generator 3 of (Z/10Z)* is the single object that forces all three chains. If true, D18 reduces to: "3 generates (Z/10Z)*, and this single fact forces BALANCE = 5, HARMONY = 7, and T* = 5/7 simultaneously."

---

## Section 5: Why This Matters

If D18 is proved, T* = 5/7 is no longer a calibrated constant — it is a structural NECESSITY of the operator algebra, forced by the generator structure of (Z/10Z)* and not adjustable without abandoning the BHML/TSML framework entirely. That changes the scientific status of every CK claim that uses T*: they become consequences of the algebra, not assumptions about coherence geometry.
