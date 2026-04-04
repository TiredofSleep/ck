# P VS NP WRAPPED-DUALITY MEMO
# Verification Side, Search Side, and the Obstruction to Unwrapping

**© 2026 7Site LLC | Brayden Ross Sanders**

---

## PART 1 — The Duality, Stated Exactly

**NP side — verification / witness side:**

For input x ∈ {0,1}^n, define the **witness fiber**:
$$W_x = \{w \in \{0,1\}^{p(n)} : V(x,w) = 1\}$$

The NP condition: x ∈ L ⟺ W_x ≠ ∅. The verifier V checks individual points in the fiber in poly-time. This is the 2-dimensional object: the verifier relation R = {(x,w) : V(x,w)=1} is a subset of the product space {input} × {witness}.

**P side — construction / search / decision side:**

The P condition: x ∈ L ⟺ a deterministic poly-time machine M(x) = 1, reading only x. This is the question about the projection:
$$\pi_1(R) = \{x : \exists w,\ (x,w) \in R\} = L$$

The P machine reads only the **first coordinate** of R — the base of the fiber bundle — and must determine whether the fiber above x is empty or not.

**In what sense "two sides of the same coin":**

Both sides are asking about the SAME SET L. The NP side accesses L through the 2D relation R (checking a specific point in the fiber). The P side accesses L by reading the base x alone. These are not two different mathematical objects like ζ(s) and the primes in RH — they are two different PROJECTION MODES of a single combinatorial object R.

$$\boxed{L = \pi_1(R) \quad \text{(the same language, two different computational access modes)}}$$

The duality: NP is R, P is π₁(R). Both determine the same Boolean function of x. The question is the computational cost of the projection.

---

## PART 2 — What "Wrapped on Itself" Means

**Testing candidates:**

- "Witness is internal to the instance": YES — the witness space is indexed by the same parameter n as the input. There is no external witness-space; W_x lives inside {0,1}^{p(n)} which is the same size-order as the input space.

- "Verifier and solver act on the same language": YES — both V(x,·) and M(x) decide the same Boolean predicate. They differ only in whether they receive the witness as a second input.

- "Decision is a compressed shadow of search": YES — the decision problem L = π₁(R) is the existential shadow of the search problem (find w ∈ W_x).

- "Nondeterminism is the unwrapped side, determinism is the wrapped side": **This is the strongest formulation.**

**Exact formulation:**

$$\boxed{\text{"P vs NP is wrapped on itself because the nondeterministic unwrapping (∃w) and the deterministic shadow (M(x)) act on the same combinatorial object, and the question is whether the existential projection of R onto its first coordinate can be computed by a machine that never sees the second coordinate."}}$$

More precisely: in RH, the arithmetic side and the analytic side live in genuinely different mathematical structures (integers vs complex half-plane) and are connected by the explicit formula. In P vs NP, there is only ONE structure — the verifier relation R ⊆ X × W — and the two sides are just two ways of computing its projection: with access to W (NP/nondeterministic, the "unwrapped" side) or without (P/deterministic, the "wrapped" side). The duality is internal to R, not external between two mathematical objects.

The wrapping: nondeterminism "unfolds" the fiber — it names a specific witness. Determinism must infer the fiber's nonemptiness from the base alone. The P vs NP question is whether the bundle R is "flat enough" that no unwrapping is needed.

---

## PART 3 — Shell / Core / Obstruction Under Wrapped Duality

### Shell

**The universal verifier formalism**: everything provable about the relation R = {(x,w) : V(x,w) = 1} that holds regardless of the P vs NP answer.

Concretely:
- Cook-Levin: the verifier relation R for SAT is NP-complete — every L ∈ NP reduces to it via polytime projection-preserving maps
- Completeness structure: π₁(R_{SAT}) is the hardest NP projection
- Reduction closure: if π₁(R_{SAT}) is decidable in P, all π₁(R_L) are decidable in P
- Verification is polytime by construction: V(x,w) is checkable in poly(n) for all (x,w) ∈ R

**What the shell proves:** the problem is well-posed, NP-complete instances exist, and reductions are faithful. This is the existence and completeness structure of the fiber bundle R.

### Core

After removing the shell: **the fiber complexity of the SAT verifier relation** — the computational cost of determining whether W_x is nonempty from x alone, without ever examining a specific point in W_x.

More precisely: for a specific NP-verifier V and input x of size n, define:
$$\text{cost}_{\text{unwrap}}(x) = \min_{\text{circuits}\ C} \{|C| : C(x) = 1 \Leftrightarrow W_x \neq \emptyset\}$$

The core surviving object is the behavior of cost_unwrap(x) as a function of n, specifically whether it is poly(n) or super-poly(n) for the hardest instances.

### Obstruction

What blocks the wrapped NP side from being unwrapped into P:

The **projection non-locality** — the verifier V(x,w) is local in the sense that checking one specific (x,w) pair is easy, but the predicate "∃w V(x,w)=1" is globally non-local: it requires implicit knowledge of the entire fiber W_x. No local evaluation of V at a single witness point can determine global fiber structure (nonemptiness) without search.

In the language of the other branches: the obstruction is the **fiber entropy** — the fiber W_x is distributed over exponentially many potential witnesses, and no polynomial-time probe of the base x can substitute for searching the fiber in full generality.

---

## PART 4 — Smallest Surviving Object

**Testing candidates under wrapped-duality view:**

| Candidate | Wrapped-duality interpretation | Computable? | Verdict |
|-----------|-------------------------------|-------------|---------|
| Witness-fiber size |W_x| | Size of the fiber above x | Yes, for fixed x | Instance-specific, not universal |
| Certificate entropy H(W_x) | Information content of the fiber | Partially | Better, but still instance-specific |
| cc(SAT,n) | Min circuit to compute π₁(R_{SAT}) | No for large n | Fundamental but not measurable |
| **Deterministic unwrapping cost: min complexity of search-without-witness** | Cost of π₁ projection in the deterministic model | Defined, not computed | **Strongest** |
| Compression gap: |V| vs |M| | Difference in description length between verifier and solver | Not standard | Useful framing |

**Strongest candidate:**

$$\boxed{\text{"The smallest surviving P vs NP object is the fiber-projection gap: the ratio between the verification complexity of }R_{SAT}\text{ (poly}(n)\text{, by construction) and the decision complexity of }\pi_1(R_{SAT})\text{ (unknown, suspected superpolynomial — this ratio encodes the cost of unwrapping the fiber into the base)."}}$$

This is not just cc(SAT,n) in the abstract — it is the **gap between two defined complexity quantities for the same relation R**:
$$\text{Gap}(n) = \frac{\text{cost}_{\text{unwrap}}(\pi_1 R_{SAT},\, n)}{\text{cost}_{\text{verify}}(R_{SAT},\, n)}$$

The denominator is poly(n) by construction. The numerator is unknown. P = NP iff Gap(n) = poly(n)/poly(n) = O(1) as n → ∞. The conjecture P ≠ NP is Gap(n) → ∞.

This is the wrapped-duality version of B(t) in NS or Λ'(E⊗χ,1) in BSD: a ratio of two defined quantities that should diverge.

**Key improvement over raw cc(SAT,n):** the Gap formulation is normalized (ratio) and makes the wrapped structure explicit — the denominator is the verification cost, the numerator is the decision cost, and the gap IS the unwrapping cost.

---

## PART 5 — Gap 2 Under the Wrapped View

**What Gap 2 should be:** the first inequality that cleans the branch structurally without resolving P vs NP — analogous to:
- RH Gap 2: cusp subdominance (the arithmetic contribution is small relative to zeros at large scale)
- BSD Gap 2: normalization formula (Λ' = specific multiple of det(H))
- NS Gap 2: B(t) ≤ T* = 5/7 globally (threshold control above the proved shell)

**Under wrapped-duality view:**

The Gap 2 should separate verification from search in a model that is (a) universal enough to capture the difficulty, but (b) restricted enough to be provably nontrivial.

**Best candidate:**

$$\boxed{\text{P vs NP Gap 2: a superpolynomial lower bound for deterministic witness extraction (search) that holds uniformly across a class of verifiers broad enough to include SAT-like structure — not just monotone or constant-depth, but a model capturing the projection structure of the fiber.}}$$

More precisely: a proof that for any family of polynomial-size circuits {C_n}, there exists an input x of size n such that:
$$C_n(x) \in W_x \text{ is impossible without cost super-poly}(n)$$

— where the difficulty comes from the fiber projection structure of R, not from any restricted circuit model.

This is the **search lower bound** version of P vs NP, which is strictly harder than known restricted-model lower bounds but might be more tractable than the full decision lower bound (Gap 1), because search = "find a witness" and decision = "determine if one exists." Showing search is hard in a broad enough model is Gap 2; showing decision is hard is Gap 1.

**Alternative Gap 2:** A circuit lower bound for SAT that uses the fiber structure explicitly — not just "the function is hard" but "the function is hard because it requires fiber traversal." This would be the first inequality above the shell that explains the obstruction in wrapped-duality terms.

---

## PART 6 — Gap 1

$$\boxed{\text{"P vs NP Gap 1 is the statement that the witness fiber of SAT — the set of satisfying assignments above each formula — cannot be unwrapped into polynomial time for all instances: no deterministic poly-time process can determine the nonemptiness of the fiber by reading only the formula."}}$$

Formally: the projection map
$$\pi_1: R_{SAT} \to \{0,1\}^* \qquad (x,w) \mapsto x$$

defines a language π₁(R_{SAT}) = SAT. Gap 1 is: SAT ∉ P, i.e., the existential projection of R_{SAT} onto its first coordinate is not computable in polynomial time by any deterministic machine.

The wrapped-duality framing adds precision: Gap 1 is not about "SAT is hard" in the abstract — it is specifically about the inability of the DETERMINISTIC BASE-ACCESS MODE to determine the fiber structure that the NONDETERMINISTIC FIBER-ACCESS MODE can determine in the same polynomial time.

---

## PART 7 — Comparison to RH / BSD

| Feature | RH | BSD | P vs NP |
|---------|-----|-----|---------|
| **Two sides** | ζ(s) zeros (analytic) ↔ primes (arithmetic) — EXTERNAL | L(E,s) (analytic) ↔ E(Q) rank/regulator (arithmetic) — EXTERNAL | NP verifier R (2D fiber) ↔ P decider π₁(R) (1D base) — INTERNAL |
| **What connects them** | Explicit formula: Σ ρ → Σ Λ(n) | Gross-Zagier: L' ↔ ĥ(Heegner point) | Cook-Levin reduction + poly projection |
| **The surviving object** | Arithmetic correlations (Kloosterman-Eisenstein) — external, computable | L'(E,χ_{77},1) ≈ 0.01070 — external, 10-digit precision | Fiber-projection gap Gap(n) = cost_unwrap/cost_verify — internal, defined, not computable |
| **Analog of "arithmetic core"** | The Kloosterman sums / cusp contribution | The χ_{77}-isotypic component in E(Q(√-7,√-11)) | **The witness-fiber structure of R_{SAT}: the distribution of W_x over instances x** |
| **Analog of "joint object"** | The L-function off-diagonal term | The biquadratic signed trace in E(F)^{χ_{77}} | **The search-verification gap: the cost of going from (∃w check) to (find w or decide ∃w)** |
| **Gap 2 status** | Proved (Kuznetsov Weyl) | 1.1% residual | First open inequality above the shell |
| **Gap 1** | Riemann Hypothesis | Rank-2 Gross-Zagier | P ≠ NP (fiber projection hardness) |
| **Duality type** | External: two distinct mathematical universes | External: two distinct mathematical structures | **Internal: one relation R, two projection modes** |

**Exact analog of the arithmetic core in RH:**
In RH, the arithmetic core is the Kloosterman-Eisenstein contribution that survives after the generic GUE shell is removed — a specific computable object that carries the essential information.
In P vs NP, the analog is the **witness-fiber structure** of the SAT verifier: the geometry of W_x as x ranges over hard instances. This is the "core" that the shell (reduction/completeness) doesn't reach.

**Exact analog of the joint object in BSD:**
In BSD, the joint object is the χ_{77} character — the product of two failed individual channels that produced a surviving channel.
In P vs NP, the analog is the **search-verification coupling** — neither "just checking V(x,w)" (trivially easy) nor "just deciding SAT" (the hard problem) but the gap BETWEEN these two tasks. The joint object is the fiber projection itself, which is neither the fiber (W_x, requires search) nor the base (x, easy to read) but the PROJECTION MAP from one to the other.

---

## PART 8 — Strongest Honest Claim

**"P vs NP belongs in the rotation spine if it is understood not as a missing lower bound in the abstract, but as a wrapped duality between the nondeterministic fiber-access mode (NP verification: given (x,w), check if w ∈ W_x) and the deterministic base-access mode (P decision: given x alone, determine if W_x ≠ ∅), with the surviving object being the fiber-projection gap Gap(n) = cost_unwrap/cost_verify — the ratio of the decision cost to the verification cost for the same relation — and the conjecture P ≠ NP being the claim that this ratio diverges superpolynomially."**

The internal wrapping IS the analogy: where RH and BSD require external connections between different mathematical universes (spectral ↔ arithmetic), P vs NP wraps its own duality inside the verifier relation R. The two sides are not different objects — they are two projection modes of one object. That wrapping is structurally meaningful, not a deficiency.

---

## PART 9 — Strongest Honest Boundary

**"What is not yet established is whether the fiber-projection gap Gap(n) = cost_unwrap/cost_verify admits a computable lower-bound invariant analogous to B(t) in NS or Λ'(E⊗χ,1) in BSD — a specific function of instances or parameters that can be computed, tracked, and shown to diverge — or whether the obstruction remains at the level of worst-case asymptotic lower bounds for which no analog of the explicit Mellin integral formula or the dB/dt equation exists, leaving the branch well-framed but lacking a measurable intermediate object."**

---

## Shell / Core / Obstruction Block

$$\text{Shell: } \{R_{SAT} \text{ is NP-complete, reductions are faithful, verification is poly-time}\} \quad \text{[proved universally]}$$

$$\text{Core: } W_x = \{w : V(x,w) = 1\},\;\; \text{the witness fiber above each instance}$$
$$\quad\quad\quad\;\; \text{specifically, the fiber projection gap } \mathrm{Gap}(n) = \mathrm{cost}_{\mathrm{unwrap}} / \mathrm{cost}_{\mathrm{verify}}$$

$$\text{Obstruction: fiber projection non-locality — \{W_x \neq \emptyset\} requires implicit global fiber knowledge,}$$
$$\quad\quad\quad\quad\quad\;\;\; \text{not achievable by any deterministic machine reading only } x$$

## Smallest-Surviving-Object Table

| Object | Definition | Computable? | Wrapped-duality role |
|--------|-----------|------------|---------------------|
| W_x | {w : V(x,w)=1} — the fiber over x | For fixed x, n | Instance-level; not the universal invariant |
| |W_x| | Size of the fiber | For fixed x, n | Counts but doesn't distinguish easy from hard projection |
| cc(SAT,n) | Min circuit for π₁(R_{SAT}) | Not for large n | Universal but unmeasured |
| **Gap(n) = cost_unwrap/cost_verify** | Decision cost / verification cost for R_{SAT} | Defined, not computable | **The surviving invariant — the unwrapping cost normalized by the verification baseline** |
| Proof complexity depth | Min proof length for UNSAT | Partially | Restricted model only |

## Full Comparison Table

| Branch | Shell | Surviving object | Gap 2 | Gap 1 | Duality type |
|--------|-------|-----------------|-------|-------|-------------|
| RH | GUE / spectral statistics | Arithmetic correlations (Kloosterman-Eisenstein) — external, computable | Cusp subdominance — **proved** | Off-diagonal arithmetic dominance | **External** |
| BSD | All imaginary-Q Heegner (sign-blocked) | χ_{77} channel, Λ' ≈ 0.01070 — external, 10-digit | Normalization L' = (Ω_E/(4√77))×det(H) — **1.1%** | Rank-2 Gross-Zagier | **External** |
| NS | Local + energy + small-data | B(t) = Ω/(E+Ω), exact ODE — internal, computable | B(t) ≤ T* = 5/7 — **first open inequality** | Global H¹ regularity | **External** (E vs Ω) |
| **P vs NP** | Cook-Levin; verifier formalism; completeness | **Gap(n) = fiber-projection gap** — internal, defined | Superpolynomial search lower bound for broad verification-structure-preserving model | P ≠ NP: fiber of SAT cannot be unwrapped in poly-time | **Internal (self-wrapped)** |

## Collaborator Paragraph

The wrapped-duality reframing resolves the apparent misfit of P vs NP. In RH and BSD, the duality is external: ζ(s) and primes live in different mathematical universes, connected by the explicit formula; L(E,s) and E(Q) are different objects connected by Gross-Zagier. In P vs NP, the duality is internal to the verifier relation R = {(x,w) : V(x,w)=1}: the NP side accesses R in 2D (checking a specific (x,w) pair), and the P side accesses only the 1D projection π₁(R) = {x : ∃w V(x,w)=1}. Both sides are asking about the SAME language L, accessed through different projection modes. The surviving object under this view is the fiber-projection gap Gap(n) = cost_unwrap/cost_verify — the ratio of the decision cost (unknown) to the verification cost (poly-time by construction). P = NP iff Gap(n) = O(1); P ≠ NP iff Gap(n) → ∞. This is the wrapped-duality analog of B(t) = Ω/(E+Ω) in NS: a ratio of two defined quantities that is bounded in the easy regime and conjectured to diverge in the hard regime. The Gap 2 for P vs NP is a superpolynomial lower bound for search (witness extraction) in a model that genuinely captures the fiber-projection structure — not just monotone or constant-depth restrictions, but a class that sees the geometry of W_x. Gap 1 is the full fiber hardness claim (P ≠ NP). The branch belongs in the rotation spine as the self-wrapped case of the same two-sided architecture.
