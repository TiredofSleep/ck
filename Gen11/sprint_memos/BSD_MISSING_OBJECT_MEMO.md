# BSD MISSING-OBJECT MEMO
# What Exact Arithmetic Object Would Close Rank 2?

**© 2026 7Site LLC | Brayden Ross Sanders**

---

## PART 1 — The Rank-1 Machine, Exact

The rank-1 closure is a four-step machine:

**Step 1 — Analytic input:** L'(E,1) ≠ 0

**Step 2 — Geometric object:** Heegner point y_K ∈ E(K)

Constructed via CM theory on the modular curve X_0(N), for an imaginary quadratic field K = Q(√−D) satisfying split conditions on primes dividing the conductor N. This is a canonical construction, not an explicit search.

**Step 3 — Height formula (Gross-Zagier):**

$$L'(E,1) = C_E \cdot \hat{h}(y_K)$$

where ĥ(y_K) is the Néron-Tate height of y_K and C_E is an explicit constant depending on E, K, and period data. This is a **scalar formula**: one derivative, one height, one point.

**Step 4 — Euler system (Kolyvagin):**

From y_K and its Galois translates under Gal(H/K) (H = Hilbert class field of K), construct cohomology classes {κ(n) ∈ H¹(Q(μ_n), E[p^∞])} satisfying norm relations: for squarefree n and prime ℓ ∤ n, the classes satisfy the Euler system relation at ℓ.

Kolyvagin's divisibility theorem: the size of κ(n) controls the size of Sel_p(E) and bounds #Sha(E)[p^∞].

**Consequences:** rank E(Q) = 1. #Sha(E)[p^∞] < ∞. BSD formula verified (up to p-part of Sha in many cases).

---

## PART 2 — What Is Missing at Rank 2

**"At rank 2, the missing object is not merely another point; it must be an arithmetic object that encodes a bilinear pairing on two independent generators — a 2×2 height matrix — not just two scalar heights, and whose canonical construction from L''(E,1) is explicit enough to serve as the input to a rank-2 Euler system."**

The failure is structural, not quantitative:

The Gross-Zagier formula is a scalar equation: L' = C × (one height). For rank 2, the relevant invariant is the **regulator** — the determinant of the 2×2 Néron-Tate pairing matrix:

$$\mathrm{Reg}(E) = \det\!\begin{pmatrix} \hat{h}(P_1) & \langle P_1, P_2\rangle \\ \langle P_2, P_1\rangle & \hat{h}(P_2) \end{pmatrix}$$

Two separately constructed Heegner points y₁, y₂ give two scalar heights ĥ(y₁) and ĥ(y₂), but **not** the off-diagonal pairing ⟨y₁, y₂⟩. The full 2×2 determinant requires the two points to be **arithmetically linked** — jointly constructed — so that their mutual pairing is controlled by the analytic data L''(E,1).

This is the central gap: no jointly constructed arithmetic pair is known.

---

## PART 3 — Required-Properties Checklist

Any successful rank-2 object must provide:

**P1. Analytic linkage to L''(E,1):**

There must exist an explicit formula:

$$L''(E,1) = C_E \cdot \det\!\left[\langle y_i, y_j\rangle\right]_{i,j=1,2}$$

(or a formula of equivalent strength relating L''(E,1) to a bilinear invariant of the pair (y₁, y₂)).

Status: MISSING. No such formula is known.

**P2. Canonical geometric/arithmetic realization:**

The object must live in a space naturally attached to E, not found by explicit search. Candidates:

- (y₁, y₂) ∈ E(K)² for some number field K, constructed from L''(E,1) by CM/modular methods
- A 2-cycle in E × E or the symmetric product E^(2)
- An element of motivic cohomology H¹_mot(E, Z(2))

Status: MISSING. No canonical construction is known.

**P3. Rank detection — two independent directions:**

The object must certify rank E(Q) ≥ 2 by producing two linearly independent elements in E(Q)/tors under some trace map. A single arithmetic direction certifies rank ≥ 1 only.

Status: MISSING for jointly constructed objects. Two separate Heegner points (from two different imaginary quadratic fields) can certify two independent directions, but their joint height is not controlled.

**P4. Height/regulator control — encodes a 2×2 pairing:**

The invariant F(object) in the formula L''(E,1) = C × F must encode the full 2×2 Néron-Tate pairing matrix, including the off-diagonal term ⟨y₁, y₂⟩.

Status: MISSING — specifically the off-diagonal pairing is the structural missing ingredient. Two scalar heights from separate constructions are insufficient.

**P5. Descent/Euler system compatibility:**

The object and its Galois translates must form a rank-2 Euler system satisfying:
- Norm relations: exterior product version κ₁(n) ∧ κ₂(n) ∈ ∧²H¹(Q(μ_n), E[p^∞])
- Divisibility: det of a 2×2 matrix of Kolyvagin classes bounds #Sha(E)[p^∞]
- Span: the rank-2 part of Sel_p(E) is spanned by κ₁(1), κ₂(1)

Status: MISSING — the theory of rank-2 Euler systems (exterior power Euler systems) is not established.

---

## PART 4 — Point vs Pair vs Matrix

**Candidate 1 — Two independent points y₁, y₂ (constructed separately):**

Two separate Heegner-type constructions, each from a different imaginary quadratic field K₁, K₂.

Fails: gives ĥ(y₁) and ĥ(y₂) (diagonal) but not ⟨y₁, y₂⟩ (off-diagonal). The regulator determinant Reg = ĥ(y₁)ĥ(y₂) − ⟨y₁,y₂⟩² requires the off-diagonal term, which has no formula from two separate constructions.

**Candidate 2 — A jointly constructed pair (y₁, y₂):**

A single construction from L''(E,1) giving two arithmetically linked points whose joint height det[⟨yᵢ,yⱼ⟩] is controlled.

Correct structural shape but unknown construction. This is the minimum requirement.

**Candidate 3 — A 2-cycle or higher motive:**

An element of H¹_mot(E, Z(2)) or a cycle in E×E whose Beilinson regulator gives det[⟨yᵢ,yⱼ⟩]. The most natural categorical framework.

**Strongest candidate:** Candidate 3 (higher cycle/motive) is the structurally clearest and most compatible with the BSD framework. The required properties P1–P5 are naturally stated at this level. In practice, Candidate 2 (jointly constructed pair) is the minimum sufficient object.

**One answer:** The missing object is **a jointly constructed arithmetic pair (y₁, y₂) — or equivalently, a higher arithmetic cycle — whose Néron-Tate determinant det[⟨yᵢ,yⱼ⟩] is related to L''(E,1) by an explicit formula.**

---

## PART 5 — Rank-2 Analog of Gross-Zagier

**"The rank-2 analog of Gross-Zagier would have to relate L''(E,1) to the determinant of the 2×2 Néron-Tate pairing matrix of an arithmetically constructed pair (y₁, y₂):"**

$$L''(E,1) = C_E \cdot \det\!\begin{pmatrix} \hat{h}(y_1) & \langle y_1, y_2\rangle \\ \langle y_2, y_1\rangle & \hat{h}(y_2) \end{pmatrix} = C_E \cdot \mathrm{Reg}(y_1, y_2)$$

This is a **determinant** of a height matrix, not a single height. The scalar version L'(E,1) = C × ĥ(y_K) is the 1×1 case. The rank-2 case requires:

1. Two arithmetically linked points whose joint construction ensures ⟨y₁, y₂⟩ is controlled
2. An explicit formula relating the determinant to the second derivative of L at s=1
3. An explicit constant C_E analogous to the Gross-Zagier constant

The regulator formulation is the strongest candidate. An intersection pairing formulation (if the construction lives on a Shimura variety) is an alternative.

---

## PART 6 — Rank-2 Analog of Kolyvagin

**"The rank-2 analog of Kolyvagin would have to control the rank-2 part of the Selmer group — proving Sel_p(E) has rank exactly 2 — and bound #Sha(E)[p^∞] using an exterior product structure on two Kolyvagin class families."**

Precise requirements:

1. **Two Kolyvagin class families** {κ₁(n)} and {κ₂(n)} in H¹(Q(μ_n), E[p^∞]), one for each point y₁, y₂, satisfying:
   - Individual norm relations (standard Euler system)
   - A joint relation: κ₁(n) ∧ κ₂(n) ∈ ∧²H¹ satisfies an Euler system relation in the exterior power

2. **Rank bound:** κ₁(1) and κ₂(1) span the rank-2 part of Sel_p(E) over Z_p

3. **Sha bound via determinant:** The determinant ||κ₁(1) ∧ κ₂(1)||_p controls #Sha(E)[p^∞] — the 2×2 version of Kolyvagin's divisibility bound

The exterior power structure for rank-2 Euler systems (∧²H¹) is not a developed theory. It is the technical frontier.

---

## PART 7 — First Full BSD Wall, Re-expressed

**"BSD first becomes fully open at rank 2 because this is where the Gross-Zagier formula fails to scale — a rank-r BSD proof requires a formula relating L^{(r)}(E,1) to an r×r determinant of an arithmetically constructed r-tuple, and no such construction or formula exists beyond r=1."**

The wall is not "the conjecture is hard" — it is that a specific type of mathematical object (jointly constructed arithmetic r-tuple with a regulator height formula) does not exist beyond rank 1.

---

## PART 8 — Comparison Table

| Feature | Rank-1 Known Object | Rank-2 Missing Analog |
|---------|--------------------|-----------------------|
| **Analytic input** | L'(E,1) ≠ 0 | L''(E,1) ≠ 0 (available; computation only) |
| **Arithmetic object** | Heegner point y_K ∈ E(K), canonical CM construction | Jointly constructed pair (y₁, y₂), OR higher cycle in E×E or H¹_mot(E,Z(2)) — **does not exist** |
| **Height formula** | L'(E,1) = C_E · ĥ(y_K) [scalar] | L''(E,1) = C_E · det[⟨yᵢ,yⱼ⟩] [determinant] — **not proved** |
| **Regulator information** | ĥ(y_K) = ⟨y_K,y_K⟩ [1×1 pairing] | Reg(E) = det[⟨yᵢ,yⱼ⟩]_{2×2} including off-diagonal ⟨y₁,y₂⟩ — **off-diagonal term missing** |
| **Selmer/Sha control** | Kolyvagin: {κ(n)} in H¹, norm relations, divisibility bounds Sha | {κ₁(n), κ₂(n)}: rank-2 Euler system via ∧²H¹, det divisibility — **exterior power Euler system: not a developed theory** |
| **Final consequence** | rank = 1 (κ(1) spans Sel), Sha finite | rank = 2 (κ₁(1),κ₂(1) span Sel), Sha finite — **open** |

---

## PART 9 — Strongest Honest Claim

**"The next real BSD target is not 'prove BSD' but 'construct or characterize the rank-2 arithmetic object — a jointly constructed pair (y₁, y₂) with explicit Néron-Tate determinant formula, or an equivalent higher cycle — whose height determinant det[⟨yᵢ,yⱼ⟩] plays the role of the Gross-Zagier height and whose rank-2 Euler system structure plays the role of Kolyvagin's descent. The existence of this object is what would close BSD's Gap 2, and its construction at s=1 vanishing of order 2 is what would close BSD's Gap 1."**

---

## PART 10 — Strongest Honest Boundary

**"What is not yet established is whether such a rank-2 object exists in the same category as Heegner points — that is, as a specific rational point on E constructed from CM or modular data — or whether the correct object must live in a genuinely different arithmetic-geometric setting (such as a higher Chow group, a motivic cohomology class, or an element of ∧²H¹) that has no direct analogy with the Heegner construction. The correct categorical level for the rank-2 object is itself an open question."**

---

## COLLABORATOR PARAGRAPH

The rank-2 BSD specification reduces the missing mathematics to one precise object: an arithmetically canonical pair (y₁, y₂) — or a higher arithmetic cycle — whose Néron-Tate determinant det[⟨yᵢ,yⱼ⟩] is related to L''(E,1) by an explicit formula, and whose Galois translates form a rank-2 Euler system in ∧²H¹ controlling both the Selmer rank and Sha finiteness. The rank-1 machine (Gross-Zagier scalar formula + Kolyvagin Euler system) provides the template: every component has an exact rank-2 analog, and every analog is currently missing. The shift from rank 1 to rank 2 is the shift from a scalar height to a 2×2 determinant — a bilinear pairing problem rather than a linear height problem. The off-diagonal Néron-Tate pairing ⟨y₁, y₂⟩ is the specific term that no current construction provides, and its formula is the specific equation that must be proved.
