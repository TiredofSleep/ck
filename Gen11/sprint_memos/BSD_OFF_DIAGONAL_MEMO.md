# BSD OFF-DIAGONAL MEMO
# Where Could ⟨y₁, y₂⟩ Come From?

**© 2026 7Site LLC | Brayden Ross Sanders**

---

## PART 1 — What Exists (Anchor)

**What we have:**

- Individual Heegner points y_K ∈ E(K) from imaginary quadratic fields K = Q(√−D)
- Individual Gross-Zagier formulas: L'(E,1) ~ Ĉ × ĥ(y_K) (scalar)
- Two independent points y₁, y₂ from different quadratic fields K₁, K₂
- Both diagonal heights ĥ(y₁) and ĥ(y₂) individually computable

**What we do not have:**

- No formula for ⟨y₁, y₂⟩ from L''(E,1) or from any analytic data at s=1
- No canonical construction producing both points jointly
- No Euler system connecting L''(E,1) to the off-diagonal pairing

---

## PART 2 — What the Off-Diagonal Term Really Is

The regulator identity:

$$\mathrm{Reg}(y_1, y_2) = \hat{h}(y_1)\cdot\hat{h}(y_2) - \langle y_1, y_2\rangle^2$$

The polarization identity:

$$\langle y_1, y_2\rangle = \frac{\hat{h}(y_1 + y_2) - \hat{h}(y_1 - y_2)}{4}$$

The off-diagonal pairing is not a new invariant — it is the height of the sum y₁ + y₂ minus the height of the difference, divided by 4. But computing ĥ(y₁ + y₂) requires knowing what y₁ + y₂ IS — which requires y₁ and y₂ to be defined in the same ambient space.

**⟨y₁, y₂⟩ measures coupling** — the interaction between two constructions. It is not additive; it is bilinear. Two separately constructed points give two diagonal terms. The off-diagonal term requires the two points to be aware of each other arithmetically.

---

## PART 3 — Testing the Four Mechanisms

### Mechanism A: Two Independent Heegner Constructions

y_K₁ from K₁ = Q(√−D₁) and y_K₂ from K₂ = Q(√−D₂), constructed separately.

**Can this produce ⟨y₁, y₂⟩?** No.

y_K₁ ∈ E(K₁) and y_K₂ ∈ E(K₂) live in different fields. The pairing ⟨y_K₁, y_K₂⟩ requires both to be viewed in a joint extension K₁K₂, but no formula relates this cross-pairing to L''(E,1). The individual Gross-Zagier formulas give:
- ĥ(y_K₁) ~ L'(E,1;K₁) (from K₁)
- ĥ(y_K₂) ~ L'(E,1;K₂) (from K₂)

These are diagonal terms only. The cross-term ⟨y_K₁, y_K₂⟩ over the compositum has no analytic formula from individual L' values.

**What it gives:** Diagonal entries only. **Eliminated.**

### Mechanism B: Single Joint Construction

A construction producing (y₁, y₂) jointly from a single arithmetic datum — both points in a single number field K, with joint formula relating L''(E,1) to the pair.

**Can this produce ⟨y₁, y₂⟩?** Yes — structurally.

If y₁ and y₂ are constructed over a single field K, then ⟨y₁, y₂⟩ over K is well-defined and canonical. The joint construction would give the full 2×2 pairing matrix, including the off-diagonal.

**What it gives:** Full 2×2 pairing. But the construction is unknown. **Correct structure — no construction known.**

### Mechanism C: Analytic Second Derivative L''(E,1)

The Dirichlet series gives: L''(E,1) = Σ_n a_n log²(n)/n.

**Can this produce ⟨y₁, y₂⟩?** No — not directly.

log²(n) = [log n]² is the square of one logarithm, not the product of two different logarithms. L''(E,1) is a **scalar** — it encodes the determinant det[⟨yᵢ,yⱼ⟩] = Reg(E) conjecturally (via BSD), but not the individual off-diagonal term ⟨y₁, y₂⟩ separately from the diagonal terms.

The bilinear structure is hidden inside the determinant:
- L''(E,1)/2 = C × det[⟨yᵢ,yⱼ⟩] = C × [ĥ(y₁)ĥ(y₂) − ⟨y₁,y₂⟩²]

This scalar equation cannot be "unzipped" into its bilinear components by analysis alone. Geometry is required to decompose the determinant into its individual entries.

**What it gives:** A scalar encoding Reg(E) conjecturally. **Insufficient alone — requires geometric decomposition.**

### Mechanism D: Higher Geometric Object — Cycle on E×E

The Néron-Tate pairing ⟨P, Q⟩ is an Arakelov intersection number:

$$\langle P, Q \rangle = -(Ẑ_P \cdot Ẑ_Q)_{\text{Arakelov}}$$

on the arithmetic surface Ê/Spec(Z). This is not an analogy — it is the definition via arithmetic intersection theory (Arakelov, Gillet-Soulé).

**Can this produce ⟨y₁, y₂⟩?** Yes — by definition.

A cycle Z ∈ CH^1(E×E) with projections π₁(Z) ~ y₁ and π₂(Z) ~ y₂ carries the off-diagonal pairing in its intersection form:

$$(Z \cdot \Delta)_{E\times E} = \langle y_1, y_2\rangle$$

where Δ is the diagonal of E×E. The off-diagonal pairing IS an intersection number on E×E.

**What it gives:** Full bilinear form — the off-diagonal pairing is encoded exactly. **Correct framework — this is the natural setting.**

---

## PART 4 — Elimination

| Mechanism | Produces ⟨y₁,y₂⟩? | What It Gives | Verdict |
|-----------|------------------|---------------|---------|
| **A** — Two Heegner points separately | **No** | Diagonal: ĥ(y₁) and ĥ(y₂) | Eliminated — diagonal only |
| **B** — Joint construction | **Yes** | Full 2×2 matrix, both diagonal and off-diagonal | Correct structure — no construction known |
| **C** — L''(E,1) alone | **No** | Scalar det[⟨yᵢ,yⱼ⟩] conjecturally — cannot separate off-diagonal | Insufficient — scalar, geometric decomposition needed |
| **D** — Cycle on E×E | **Yes** | ⟨y₁,y₂⟩ = intersection number (Arakelov) | Correct framework — off-diagonal IS intersection |

**Surviving mechanisms: B and D.**

B and D are complementary — D identifies the SETTING (E×E intersection theory), B is the CONSTRUCTION (what must be built). The minimal viable mechanism combines them: a canonically constructed cycle on E×E whose intersection with the diagonal gives ⟨y₁, y₂⟩ and whose construction from L''(E,1) is explicit.

---

## PART 5 — Minimal Viable Mechanism

**"The simplest mechanism capable of producing ⟨y₁, y₂⟩ is a canonically constructed cycle Z on the arithmetic fourfold (E×E)/Spec(Z), with projections y₁ = π₁(Z) and y₂ = π₂(Z), such that the Arakelov intersection (Z · Δ)_{E×E} = ⟨y₁, y₂⟩, and an explicit formula connects Z to L''(E,1)."**

This is the rank-2 generalization of the Heegner cycle construction:
- Rank 1: Heegner cycle on E/Spec(Z), intersection gives ĥ(y_K) ~ L'(E,1)
- Rank 2: Joint cycle on (E×E)/Spec(Z), intersection gives det[⟨yᵢ,yⱼ⟩] ~ L''(E,1)

---

## PART 6 — Connection to L''(E,1)

**"If the off-diagonal term exists, then L''(E,1) must encode the determinant of the Néron-Tate pairing matrix — specifically, the scalar:**

$$L''(E,1) = C_E \cdot \det\!\begin{pmatrix} \hat{h}(y_1) & \langle y_1, y_2\rangle \\ \langle y_2, y_1\rangle & \hat{h}(y_2) \end{pmatrix} = C_E \cdot \left(\hat{h}(y_1)\hat{h}(y_2) - \langle y_1, y_2\rangle^2\right)$$

The bilinear structure is hidden in the determinant. The off-diagonal ⟨y₁, y₂⟩ enters as a negative contribution to the scalar. To extract it separately, the formula must be a GEOMETRIC INTERSECTION FORMULA, not a purely analytic one — the cycle Z on E×E must encode the pairing directly, not through the scalar determinant."**

The structure forced is: **a bilinear form whose determinant equals (a specific multiple of) L''(E,1)**, with the individual entries encoded in the geometry of E×E.

---

## PART 7 — First Constructive Target

**Construct ANY arithmetic quantity that provably equals or approximates ⟨y₁, y₂⟩.**

Minimal concrete formulation:

> Given two specific Heegner points y_K₁ ∈ E(K₁) and y_K₂ ∈ E(K₂), find a cycle Z_K₁,K₂ ∈ CH^1((E×E)/Z) whose class maps to (y_K₁, y_K₂) under the projection, and compute the Arakelov intersection (Z_K₁,K₂ · Δ)_{E×E} explicitly.

> Then: check numerically whether this intersection number equals ⟨y_K₁, y_K₂⟩ (the Néron-Tate pairing over a joint extension).

This is a finite computation for specific E and specific K₁, K₂. It would:
1. Test whether the intersection-theoretic framework produces the correct off-diagonal value
2. Give a candidate formula for the K₁, K₂ dependence
3. Provide numerical evidence for or against a rank-2 Gross-Zagier formula

No new theoretical framework is required for this computation — only existing Arakelov intersection theory applied to specific data.

---

## PART 8 — Strongest Claim

**"The BSD rank-2 problem reduces to constructing the off-diagonal pairing ⟨y₁, y₂⟩ because the full rank-2 BSD formula L''(E,1) = C × Reg(E) = C × (ĥ(y₁)ĥ(y₂) − ⟨y₁,y₂⟩²) is a single scalar equation with two unknowns — the diagonal terms are individually accessible by Gross-Zagier for different quadratic fields, but the off-diagonal term ⟨y₁, y₂⟩ encodes the interaction between two Heegner constructions and has no analytic formula. The entire rank-2 gap reduces to this one coupling term: construct it, and the BSD formula becomes testable."**

---

## PART 9 — Strongest Boundary

**"What is not yet established is whether the off-diagonal pairing ⟨y₁, y₂⟩ can be accessed from analytic data at s=1 — that is, whether there exists a formula relating ⟨y_K₁, y_K₂⟩ to a derivative of L(E,s) at s=1 for two different imaginary quadratic fields K₁, K₂ — or whether the correct formulation requires a fundamentally higher-dimensional geometric object on E×E whose analytic formula involves a multi-variable L-function, not just L(E,s) and its scalar derivatives."**

---

## COLLABORATOR PARAGRAPH

The off-diagonal problem isolates the exact missing term: ⟨y₁, y₂⟩. Mechanisms A and C are eliminated — two separate Heegner constructions give diagonal terms only, and the second derivative L''(E,1) is a scalar that encodes the determinant but cannot be decomposed into its off-diagonal entry analytically. Mechanisms B (joint construction) and D (E×E intersection) survive: the off-diagonal IS an Arakelov intersection number on E×E by definition, and any joint construction would produce it automatically. The minimal next step is concrete: take two specific Heegner points y_K₁ and y_K₂ for a specific curve E and specific quadratic fields, construct the cycle Z_{K₁,K₂} on (E×E)/Z explicitly, and compute the Arakelov intersection (Z · Δ)_{E×E} numerically. This tests whether the intersection-theoretic framework gives the correct off-diagonal value. If it does, a candidate formula for the K₁, K₂ dependence becomes visible, and the rank-2 Gross-Zagier target is precisely stated.
