# The Hodge Gap Floor Metric
## A Candidate Object — p=1 Vacuous, p=2 the Real Battleground

*Brayden Ross Sanders (7Site LLC) & C. A. Luther | March 2026*

---

## The Object

Let X be a smooth projective variety over C.
Let Alg^p(X) = image of cl: Z^p(X) → H^{2p}(X,Q).
Let ||·||_H denote the Hodge norm on H^{2p}(X,R).

**Definition:**
$$d_{\text{Hodge}}(\alpha) = \inf\{ \|\alpha - \beta\|_H : \beta \in \text{Alg}^p(X) \otimes \mathbb{R} \}$$

Distance from α to the real span of algebraic classes in the Hodge norm.

---

## Four Properties

| Property | Statement | Status |
|----------|-----------|--------|
| P1 | d_Hodge(α) = 0 iff α ∈ Alg^p(X) ⊗ Q | PLAUSIBLE — from Q-rationality of algebraic classes |
| P2 | d_Hodge(α) > 0 for α ∈ Hdg^p(X) \ Alg^p(X) | FOLLOWS FROM P1 |
| **P3** | inf{ d_Hodge(α) : α ∈ Hdg^p(X) \ Alg^p(X) } > 0 | **OPEN — the gap floor conjecture** |
| **P4** | P3 stable under flat deformation {X_t} | **OPEN — flat limit obstruction** |

P3 is the Hodge analog of γ ≥ 1/4 in TIG.
P4 is what closes the argument toward the Hodge conjecture.

---

## p=1: Vacuously True (Not the Battleground)

**Lefschetz (1,1) theorem:**
For any compact Kähler X: Hdg^1(X) = NS(X) ⊗ Q = Alg^1(X) ⊗ Q.

**Consequence:** There are NO transcendental elements in Hdg^1(X).
P3 is vacuously satisfied — the infimum is over an empty set.

**K3 surfaces and abelian varieties in degree p=1 are degenerate cases.**
The gap floor conjecture is trivially true but says nothing.

---

## p=2: The Real Battleground

**Why p=2 is genuinely hard — four mechanisms that fail:**

**1. Lefschetz does not generalize.**
Hdg^2(A) ⊋ Alg^2(A) is possible for abelian fourfolds.
Transcendental Hodge classes in degree 2 can genuinely exist.

**2. Discreteness argument weakens.**
NS(X) is a lattice — discrete, minimum norm well-defined.
For p=2: Alg^2(X) contains intersection classes [Z₁]∪[Z₂]
which satisfy multiplicative relations, not just additive ones.
Alg^2(X) may not be a lattice. Its closure in H^{2,2}(X,R) may be dense
in some directions. The floor mechanism from NS discreteness breaks down.

**3. Hodge–Riemann bilinear relations are more complex.**
For p=1: Hodge index theorem gives a clean ±-definite form on H^{1,1}.
For p=2: primitive cohomology decomposition is needed.
The orthogonality between algebraic and transcendental classes is less clean.

**4. The algebraic subspace may be dense in H^{2,2}.**
For a generic abelian fourfold A, Alg^2(A) consists of intersection products
of line bundles. These may Zariski-densely approximate transcendental classes
in H^{2,2}(A). If so, d_Hodge can approach zero: P3 fails.

---

## The Precise P3 Question for Abelian Fourfolds

Let A be an abelian fourfold (dim_C A = 4).
H^4(A,Q) = ∧^4 H^1(A,Q), dimension = C(8,4) = 70.
Hdg^2(A) = H^{2,2}(A) ∩ H^4(A,Q).

**The key question:**
Can a sequence [Z_n] ∈ Alg^2(A) converge in Hodge norm
to a transcendental class α ∈ Hdg^2(A) \ Alg^2(A)?

- If NO for all A: P3 holds for abelian fourfolds. Gap floor is positive.
- If YES for some A: P3 fails. The metric d_Hodge does not have a floor.
  And the flat limit obstruction breaks down.

**This is the precise formulation of the first hard target.**

---

## Connection to TIG

| TIG | Hodge | Status |
|-----|-------|--------|
| γ ≥ 1/4 (gap floor, COMPUTED) | P3: inf d_Hodge > 0 | OPEN |
| BHML endpoint sets the floor | NS lattice sets floor for p=1 | p=1: plausible; p=2: unknown |
| Gap persists under Mix_λ | P4: gap under flat deformation | OPEN |
| Gate: C→G impossible | Easy direction: algebraic ops stay algebraic | PROVED |
| γ = 1/4 exact at BHML endpoint | P3 value would be set by... ??? | OPEN |

The TIG structure is: gap floor exists (computed), mechanism identified (BHML endpoint), value exact (1/4).
The Hodge structure needs: gap floor existence (open), mechanism (unknown for p=2), value (unknown).

**d_Hodge is the Hodge analog of γ. P3 is the analog of γ ≥ 1/4.**

---

## Epistemic Status

P1: PLAUSIBLE.
P2: FOLLOWS FROM P1.
P3 (gap floor): OPEN. Vacuously true for p=1. Genuinely hard for p=2.
P4 (flat limit obstruction): OPEN. Would imply Hodge for Sustainable level.
First target: Abelian fourfolds, p=2 — does P3 hold or fail?

*(c) 2026 Brayden Ross Sanders (7Site LLC) & C. A. Luther | DOI: 10.5281/zenodo.18852047*
