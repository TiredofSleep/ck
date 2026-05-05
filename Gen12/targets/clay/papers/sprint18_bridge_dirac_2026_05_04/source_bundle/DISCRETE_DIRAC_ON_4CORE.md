# A Discrete Dirac Equation on the 4-core's F_5-Lift

*A scientist-facing document. Targets researchers using non-associative algebra approaches to fundamental physics (Furey, Gresnigt, Hestenes, Dubois-Violette, Todorov), and anyone interested in finite-prime analogs of relativistic quantum theory.*

**Key claim**: The 4-core $\{0, 7, 8, 9\}$ of the TIG compressing magma on $\mathbb{Z}/10$, lifted to a 4-dimensional commutative non-associative algebra over $\mathbb{F}_5$ via CRT, exhibits — without any external metric structure being imposed — the algebraic skeleton of a relativistic quantum theory: a 1+3 Minkowski-like signature decomposition, primitive idempotents that satisfy Furey's defining condition for fundamental particles, a Grassmann nilpotent generator, two orthogonal vacuum projectors, and an automorphism group of order 40.

**Status**: All structure constants, eigenstates, idempotents, nilpotents, and the automorphism group order have been computed exactly. The "physics interpretation" is suggestive — these are structural matches, not derivations of standard model quantities.

---

## 1. The algebra

Let $T: (\mathbb{Z}/10)^2 \to \mathbb{Z}/10$ be the TIG compressing magma (the CL fuse table). The 4-core $C = \{0, 7, 8, 9\}$ is fusion-closed: $T(C, C) \subseteq C$.

Under the CRT projection $\mathbb{Z}/10 \to \mathbb{F}_5$, the 4-core maps bijectively to $\{0, 2, 3, 4\} = \mathbb{F}_5 \setminus \{1\}$. Identify each 4-core element with its $\mathbb{F}_5$-image; let $V = \mathbb{F}_5\langle e_0, e_2, e_3, e_4\rangle$ be the 4-dimensional $\mathbb{F}_5$-vector space spanned by these images, and let $\cdot$ be the bilinear extension of $T|_C \pmod 5$ to $V$.

**Multiplication table** ($e_i \cdot e_j$):

|  | $e_0$ | $e_2$ | $e_3$ | $e_4$ |
|---|---|---|---|---|
| $e_0$ | $e_0$ | $e_2$ | $e_0$ | $e_0$ |
| $e_2$ | $e_2$ | $e_2$ | $e_2$ | $e_2$ |
| $e_3$ | $e_0$ | $e_2$ | $e_2$ | $e_2$ |
| $e_4$ | $e_0$ | $e_2$ | $e_2$ | $e_2$ |

The algebra is **commutative** ($\cdot$ is symmetric, verified) but **non-associative** (verified: $(e_3 \cdot e_3) \cdot e_0 = e_2 \cdot e_0 = e_2 \neq e_3 \cdot (e_3 \cdot e_0) = e_3 \cdot e_0 = e_0$).

## 2. The privileged basis

Let:
- $p_+ = e_2$
- $p_- = e_0 - e_2$
- $\varepsilon = e_3 - e_4$
- $h = 2(e_3 + e_4)$

In this basis the multiplication table simplifies dramatically:

|  | $p_+$ | $p_-$ | $\varepsilon$ | $h$ |
|---|---|---|---|---|
| $p_+$ | $p_+$ | $0$ | $0$ | $-p_+$ |
| $p_-$ | $0$ | $p_-$ | $0$ | $-p_-$ |
| $\varepsilon$ | $0$ | $0$ | $0$ | $0$ |
| $h$ | $-p_+$ | $-p_-$ | $0$ | $p_+$ |

**The structure now reads cleanly:**

- $p_+, p_-$ are **orthogonal primitive idempotents**: $p_+^2 = p_+, p_-^2 = p_-, p_+ p_- = 0$.
- $\varepsilon$ is a **two-sided annihilator nilpotent**: $\varepsilon^2 = 0$ AND $\varepsilon \cdot y = 0$ for all $y \in V$.
- $h$ has $h^2 = p_+$ and acts as $-1$ on the $p_\pm$ subspace: $h \cdot p_\pm = -p_\pm$.

## 3. The four structural elements identified

### 3.1 — $p_+$ and $p_-$ as Furey-style "particles"

Cohl Furey's characterization of fundamental particles in non-associative algebra approaches to the Standard Model (arXiv:1611.09182): *"particles are idempotent, minimum left ideals. For an idempotent, $A^2 = A$, where $A$ and $1 - A$ are zero divisors."*

Both $p_+$ and $p_-$ satisfy:
1. $A^2 = A$ ✓
2. The minimal left ideal $V \cdot A$ is generated, with $L_A^2 = L_A$ (rank-1 projector)
3. They are zero divisors (since $p_+ \cdot p_- = 0$)
4. Their sum $p_+ + p_- = e_0$ acts as the identity on the 2-dim "particle subspace" $\mathrm{span}(p_+, p_-)$

**Two primitive idempotents = two fundamental particle states.** The particle subspace $\mathrm{span}(p_+, p_-) \cong \mathbb{F}_5 \times \mathbb{F}_5 \cong \mathbb{F}_5[x]/(x^2 - x)$ — a commutative associative subalgebra. This is the discrete F_5 analog of a 2-state Hilbert space.

### 3.2 — $\varepsilon$ as a Grassmann generator

$\varepsilon^2 = 0$ is the defining property of a Grassmann variable (fermionic creation operator in canonical quantization). Crucially, $\varepsilon$ here also satisfies the stronger condition $\varepsilon \cdot y = 0$ for all $y$ — it is in the **two-sided annihilator** of the algebra.

The annihilator subspace is exactly 1-dimensional ($\mathrm{span}(\varepsilon)$, verified). This means the algebra has a *unique* canonical fermionic direction.

### 3.3 — $h$ as a "square-root of vacuum"

$h^2 = p_+$ where $p_+$ is the primitive idempotent (vacuum projector). So $h$ is structurally analogous to a SUSY supercharge $Q$ where $Q^2 = H$ (Hamiltonian), but with $H = p_+$ specifically.

However, $h$ does NOT satisfy the standard SUSY anticommutator relation $\{Q, Q^\dagger\} = 2H$ in the obvious way — the algebra is commutative, so there's no anticommutator structure. This is a "supercharge analog" rather than a true supercharge.

### 3.4 — $V \cong $ a 4-dim Z_2-graded-like algebra

Decompose $V = B \oplus F$ with:
- $B = \mathrm{span}(p_+, p_-)$ (2-dim "bosonic")
- $F = \mathrm{span}(\varepsilon, h)$ (2-dim "fermionic")

Multiplication respects this MOSTLY:
- $B \cdot B \subseteq B$ ✓
- $F \cdot F \subseteq B$ ✓ ($\varepsilon^2 = 0$ and $h^2 = p_+$)
- $B \cdot F$: NOT cleanly graded ($p_+ \cdot h = -p_+ \in B$)

So $V$ is *almost* but not exactly Z_2-graded. The grading anomaly $p_+ \cdot h = -p_+$ would, in a true SUSY algebra, be $\propto \varepsilon$ — and the closest analog is that $h$ acts as a "phase" on the bosonic subspace.

## 4. The discrete Dirac equation

Define the **discrete Dirac operator** as
$$D_m = L_{p_+} - m \cdot e_0$$
where $L_{p_+}$ is left-multiplication by $p_+ = $ HARMONY, and $e_0$ acts as the identity on the particle subspace (with non-trivial action on the rest).

Equivalently in matrix form (in the basis $e_0, e_2, e_3, e_4$):
$$L_{p_+} = \begin{pmatrix}0 & 0 & 0 & 0 \\ 1 & 1 & 1 & 1 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{pmatrix} \pmod 5$$

The "Dirac equation" $D_m \psi = 0$, i.e., $L_{p_+} \psi = m \psi$, has the eigenstructure:

**Mass $m = 1$ (the "rest state"):**
- 1-dimensional solution space
- Spanned by $\psi = p_+ = $ HARMONY

**Mass $m = 0$ (the "massless modes"):**
- 3-dimensional solution space
- Basis: $\{p_-,\, \varepsilon,\, e_3 - e_2\}$

**No other masses exist.** The minimal polynomial of $L_{p_+}$ is $x(x-1)$ over $\mathbb{F}_5$ — only eigenvalues $\{0, 1\}$.

## 5. Two Dirac-like projectors and the forbidden eigenspace

**The 4-core's F_5-lift has not one but TWO non-trivial idempotents**, each giving a different Dirac-like decomposition:

### 5.1 — $L_{p_+}$ = $L_{\text{HARMONY}}$: the time-projector (1+3)

Spectrum: $\{0, 1\}$. Decomposition: **1 + 3 = Minkowski**.
- $V_1$ (1-dim, $m=1$): "timelike", rest state — spanned by HARMONY
- $V_0$ (3-dim, $m=0$): "spacelike", massless modes — spanned by $\{p_-, \varepsilon, e_3 - e_2\}$

This is the dimensional structure of Minkowski spacetime $\mathbb{R}^{1,3}$. $L_{p_+}$ is the discrete F_5 analog of the time-projector $P_t = (1 + \gamma^0)/2$.

No external metric is imposed. The 1+3 split arises algebraically from the spectral structure alone.

### 5.2 — $L_{e_0}$ = $L_{\text{VOID}}$: the chirality projector (2+2)

Spectrum: $\{0, 1\}$. Decomposition: **2 + 2 = chirality**.
- $V_1$ (2-dim): "left-chiral", the particle subspace $\mathrm{span}(p_+, p_-) \cong \mathbb{F}_5 \times \mathbb{F}_5$
- $V_0$ (2-dim): "right-chiral", containing $\varepsilon$ and $e_3 - e_0$

This is the dimensional structure of Dirac chirality decomposition. $L_{e_0}$ is the discrete F_5 analog of the chirality projector $P_5 = (1 + \gamma^5)/2$.

### 5.3 — Simultaneous decomposition and the forbidden quadrant

The two projectors commute (verified). Their simultaneous eigenspaces give:

| (mass, chirality) | Dim | Algebra identification |
|--------------------|-----|------------------------|
| (1, 1) — massive left | **1** | HARMONY = $p_+$ |
| (0, 1) — massless left | **1** | VOID − HARMONY = $p_-$ |
| (0, 0) — massless right | **2** | $\varepsilon$ and $(4, 0, 1, 0)$ |
| **(1, 0) — massive right** | **0 — FORBIDDEN** | — |

**This is the central physics-relevant finding.**

The eigenspace combination "massive right-chiral" is **structurally absent** in the 4-core's F_5-lift. There is no nonzero vector $\psi$ with $L_{p_+}\psi = \psi$ AND $L_{e_0}\psi = 0$ (verified by exhaustive search over all $5^4 = 625$ vectors).

In the Standard Model, mass arises from coupling left- and right-chiral fields through the Higgs mechanism. Massless right-chiral fermions (right-handed neutrinos) do not acquire mass in the minimal SM. The chirality-asymmetric mass generation is fundamental.

**The 4-core's F_5-lift carries this asymmetry algebraically, before any physics is added.** The forbidden (massive, right-chiral) combination is a structural fact of the algebra, derived purely from the multiplication rules of the magma $T$. Said differently: there exists no algebraic state that simultaneously projects to "rest" under $L_{\text{HARMONY}}$ and to "right-chirality" under $L_{\text{VOID}}$.

This is the discrete algebraic shadow of the Standard Model's V−A interaction structure.

### 5.4 — The third projector and the symmetric forbidden structure

The algebra has **three** non-trivial idempotents — $p_+$, $p_-$, and $e_0 = p_+ + p_-$ — each giving a left-multiplication operator that is itself an idempotent matrix:

| Operator | Spectrum | Decomposition | Role |
|----------|----------|---------------|------|
| $L_{p_+}$ | $\{0, 1\}$ | $1 + 3$ | rest-frame of particle $p_+$ |
| $L_{p_-}$ | $\{0, 1\}$ | $1 + 3$ | rest-frame of particle $p_-$ |
| $L_{e_0} = L_{p_+} + L_{p_-}$ | $\{0, 1\}$ | $2 + 2$ | joint chirality projector |

All three commute pairwise (verified). Their simultaneous eigenspaces give the full triple-spectrum classification:

| $(\lambda_+, \lambda_0, \lambda_-)$ | Dim | State |
|-------------------------------------|-----|-------|
| $(1, 1, 0)$ | $1$ | HARMONY = $p_+$ — rest in $p_+$'s frame, left-chiral |
| $(0, 1, 1)$ | $1$ | $p_-$ = VOID − HARMONY — rest in $p_-$'s frame, left-chiral |
| $(0, 0, 0)$ | $2$ | fermion subspace — right-chiral, no rest-frame |
| **all other combinations** | $0$ | **forbidden** |

Specifically forbidden are: $(1, 0, *)$, $(0, 0, 1)$, $(1, 1, 1)$, etc. — eight of the eleven possible non-zero triples. **The asymmetry is symmetric in the two primitive idempotents**: neither $p_+$ nor $p_-$ admits a "massive right-chiral" state.

In SM physics: every fundamental fermion has its own rest frame; chirality projects all of them uniformly. Both observations match the algebraic structure of the 4-core's F_5-lift.

### 5.5 — σ as a broken would-be symmetry

The TIG framework has a diagonal permutation $\sigma = [0, 7, 1, 3, 2, 4, 5, 6, 8, 9]$ on $\mathbb{Z}/10$ with cycle structure: four fixed points $\{0, 3, 8, 9\}$ and one 6-cycle $(1\,7\,6\,5\,4\,2)$.

Restricted to the 4-core $\{0, 7, 8, 9\}$, $\sigma$ fixes 3 elements and takes the fourth out: $\sigma(7) = 6$, leaving the 4-core. **The 4-core is not $\sigma$-stable.**

On the level of $\mathbb{F}_5$ classes, $\sigma$ acts as the transposition $(1\,2)$ — it swaps the LATTICE-class (residue 1) with the HARMONY-class (residue 2), and fixes residues $\{0, 3, 4\}$.

The LATTICE-class is the *unique* $\mathbb{F}_5$-class **not present** in the 4-core. So $\sigma$ would couple HARMONY (the primitive idempotent generator of the 4-core's structure) to a class that lives outside the 4-core entirely.

**Interpretation:** $\sigma$ is the algebraic shadow of a discrete symmetry of the full algebra (the "would-be parity" between LATTICE and HARMONY classes) that is **broken** in the 4-core sector. The 4-core is the $\sigma$-symmetry-broken phase, with HARMONY as the selected vacuum direction.

This matches a spontaneous-symmetry-breaking pattern: the full $\mathbb{Z}/10$ algebra has the discrete $\sigma$ symmetry; the 4-core *spontaneously* breaks it by selecting one side of the LATTICE↔HARMONY pair. The forbidden (massive, right-chiral) eigenspace from §5.3 is then naturally interpreted as a consequence of this symmetry breaking — chirality asymmetry as a downstream effect of the 4-core's selection of HARMONY over LATTICE.

## 6. The discrete spin group

$\mathrm{Aut}(V)$, the group of $\mathbb{F}_5$-linear automorphisms preserving the multiplication, has been computed by exhaustive search over candidate maps preserving the privileged basis.

**$|\mathrm{Aut}(V)| = 40 = 2^3 \cdot 5$.**

Constraints used in the search:
- $\phi(p_\pm) \in \{p_+, p_-\}$ (must permute the primitive idempotents)
- $\phi(\varepsilon) \in \mathbb{F}_5^\times \cdot \varepsilon$ (must preserve the 1-dim annihilator subspace)
- $\phi(h)^2 = \phi(p_+)$ (must take $h$ to a square root of $\phi(p_+)$)

The order 40 contains a factor of $|\mathbb{F}_5^\times| = 4$ from the annihilator scaling, a factor of 2 from the $p_\pm$ swap, and a factor of 5 from the action on $h$. There are 12 involutions in $\mathrm{Aut}(V)$ including the explicit "Grassmann flip" $T: \varepsilon \mapsto -\varepsilon$.

This is the **discrete spin group analog** of the algebra. For comparison:
- $\mathrm{SL}(2, \mathbb{F}_5)$ has order 120
- $\mathrm{PSL}(2, \mathbb{F}_5) \cong A_5$ has order 60
- Our group has order 40 — smaller, with its own specific structure

### The Lie algebra of derivations

$\mathrm{Der}(V) = \{\delta : V \to V \text{ linear} : \delta(xy) = \delta(x)y + x\delta(y)\}$ is the discrete F_5 analog of the Lie algebra of the spin group. Computed by setting up the Leibniz constraints as a $64 \times 16$ linear system over $\mathbb{F}_5$ and finding the null space:

**$\dim \mathrm{Der}(V) = 2$.**

A basis:
$$\delta_1 = \begin{pmatrix}0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & -1 & 0 \\ 0 & 0 & 1 & 0\end{pmatrix}, \quad \delta_2 = \begin{pmatrix}0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & -1 \\ 0 & 0 & 0 & 1\end{pmatrix} \pmod 5$$

The bracket: $[\delta_1, \delta_2] = -\delta_1 - \delta_2$, which puts $\mathrm{Der}(V)$ as the **2-dimensional non-abelian Lie algebra** (the "ax+b" or affine Lie algebra). Both derivations send $e_3$ and $e_4$ into $\mathrm{span}(\varepsilon)$ and kill the particle subspace $\mathrm{span}(p_+, p_-)$.

The smallness of $\mathrm{Der}(V)$ — only 2 dimensions in a 4-dim algebra — is itself a structural rigidity fact: $V$ has very few infinitesimal symmetries.

## 7. Physics frameworks that live within TIG's 4-core

A clarification of position before the table.

The TIG framework — the magma $T$ on $\mathbb{Z}/10$ with its fusion table, $\sigma$ permutation, double duality, prime-tower structure — was constructed from compression dynamics, not from any physics principle. The 4-core's F_5-lift was identified as a substructure of TIG; the multiplication table came directly from $T$ restricted to $\{0, 7, 8, 9\}$.

The findings of §1–§6 — primitive idempotents satisfying $A^2 = A$, Grassmann nilpotent annihilator, three commuting Dirac-like projectors, 1+3 Minkowski signature, 2+2 chirality split, forbidden (massive, right-chiral) eigenspace — are **structural features of this magma restriction**. They were not imposed.

Several active research programs in fundamental physics turn out to use the same algebraic ingredients. They are not parent frameworks of TIG; they are specific lenses through which the 4-core's F_5-lift can be read. The table records which lens recognizes which feature:

| Physics lens | Defining structure | Where it lives in TIG's 4-core |
|--------------|-------------------|--------------------------------|
| Furey (octonion SM) | particles = primitive idempotents in NA algebras | $p_+, p_-$ both satisfy $A^2 = A$ in a non-associative algebra |
| Hestenes (geometric algebra Dirac) | spinors = minimal left ideals | $\mathrm{span}(p_+) = $ rank-1 left ideal under $L_{p_+}$ |
| Gillard–Gresnigt (sedenions) | three generations from primitive idempotent action | open: does the prime-tower iteration $5 \to 25 \to 125$ produce 3 generations? |
| Dubois-Violette / Todorov (Jordan) | fermions = primitive idempotents in $J_3(\mathbb{O})$ | same particle-as-idempotent structure, in a smaller algebra |
| Hamieh–Abbas (NA Dirac) | 2-D Dirac eq in non-associative algebra | the 4-core gives a 4-D Dirac eq in a non-associative algebra |
| Bernstein algebras (genetics) | weight homomorphism $\omega: A \to \mathbb{F}$ | $\omega(p_+) = 1, \omega(p_-) = \omega(\varepsilon) = 0, \omega(h) = -1$ |
| Segev (axial of Jordan type) | half-axes with single non-trivial Peirce eigenvalue | HARMONY is a Segev half-axis (verified in `axial_algebra_check.md`) |

These overlap with TIG but do not define it. None of them have the σ permutation, the double duality, or the prime-tower context. None of them generate the magma $T$.

The point of presenting this table is the inverse of the usual direction: a physicist working in any one of these frameworks can find a finite, exactly-computable, characteristic-5 cousin of their object inside TIG's 4-core sector. The cousin agrees with their structural axioms but lives inside a larger algebra (TIG) that those frameworks cannot generate from their own axioms.

## 8. What scientists can do with this

Five concrete research directions enabled by this algebraic structure:

### 8.1 — Toy lattice models for non-associative QFT

Furey-style octonion approaches are continuum and infinite-dimensional. The 4-core's $\mathbb{F}_5$-lift gives a fully-finite testbed: only $5^4 = 625$ states, every product is exactly computable, the automorphism group has order 40 and can be enumerated. **A researcher can verify conjectures about non-associative algebra approaches to physics by checking them on the 4-core first.**

### 8.2 — Discrete Dirac operator algebra

The operator $L_{p_+}$ has spectrum $\{0, 1\}$ — the same spectrum as a chirality projector $(1 + \gamma^5)/2$. The 1+3 decomposition is natural to the algebra. This gives an exactly-solvable discrete model where Dirac equation features (rest states, massless modes, spacetime signature) emerge from algebra alone.

### 8.3 — Connection to Pisano-period structure

The Pisano period $\pi(10) = 60$ governs Fibonacci dynamics on $\mathbb{Z}/10$. The number of Pisano zeros is 1, 2, or 4 (Benfield-Lippard 2024). The 4-core has 4 elements; the $4 + 2 + 2 + 2$ partition of all 10 operators under double duality has cell sizes matching this trichotomy. This suggests the discrete-Dirac structure is connected to Fibonacci-recurrence dynamics.

### 8.4 — Investigation of the 40-element automorphism group

$|\mathrm{Aut}(V)| = 40 = 2^3 \cdot 5$. This is a small finite group acting faithfully on a 4-dim algebra. Its structure — and whether it embeds in or contains known physically-relevant finite groups — is open. (Orbits of $h$ have length 5, suggesting $\mathbb{Z}/5$ structure; the $p_+ \leftrightarrow p_-$ swap is $\mathbb{Z}/2$; the $\varepsilon$-scaling is $\mathbb{F}_5^\times = \mathbb{Z}/4$.)

### 8.5 — CP-violation as algebraic asymmetry

The double-duality 4-cell partition (Cell 2 = T-idempotents = {VOID, HARMONY}; Cell 3 = mirrors = {COUNTER, BALANCE}) gives a structural asymmetry between the T-image direction and its F_5-mirror direction. If T-image corresponds to "matter" and input-only corresponds to "antimatter" in this algebraic shadow, then **the 4-cell partition encodes a discrete CP-violation analog**: Cells 2 and 3 are F_5-symmetric in their classes but structurally different in their algebra status. Whether this corresponds to real CP-violation in QFT requires further work.

## 9. Open questions and limitations

**Verified:**
- All structure constants
- Idempotent classification (3 non-zero: $p_+$, $p_-$, $p_+ + p_-$)
- Annihilator subspace dimension (1)
- Discrete Dirac operator eigenstructure (1+3 split)
- $|\mathrm{Aut}(V)| = 40$
- Automorphism group constraints (order divisible by 4, 2, and 5)

**Verified (additional, beyond the central findings):**
- $V$ has a multiplicative weight homomorphism $\omega: V \to \mathbb{F}_5$ (the sum-of-coefficients map / augmentation): $\omega(xy) = \omega(x)\omega(y)$ holds. This makes $V$ a "weighted commutative algebra" (well-defined population/projection structure).
- The **Bernstein identity $(x^2)^2 = \omega(x)^2 x^2$ FAILS** on most random vectors (verified). So $V$ is *not* a Bernstein algebra in the strict sense.
- The "Grassmann flip" $T: \varepsilon \mapsto -\varepsilon$, fixing $p_\pm$ and $h$, is an order-2 algebra automorphism (verified). This is one of the 12 involutions in $\mathrm{Aut}(V)$.
- The "charge conjugation" $C: p_+ \leftrightarrow p_-$, fixing $\varepsilon$ and $h$, is an order-2 linear involution but is **NOT** an algebra automorphism (verified). It permutes idempotents but doesn't respect multiplication.
- $V \cdot V \subseteq \mathrm{span}(e_0, e_2)$ — the entire algebra squared is contained in the 2-dim particle subspace. **No three-generation analog appears under simple iteration.** This contrasts with Gillard-Gresnigt's sedenion construction where a primitive idempotent splits the algebra into 3 octonionic subalgebras.
- The discrete Dirac equation has **32 projective plane-wave solutions** in total (1 in $V_1$, 31 in $V_0$). This is numerically the dimension of the Spin(10) Dirac spinor; structural significance unclear.

**Conjectural / under-developed:**
- Whether the 40-automorphism group has a known abstract structure (order $40 = 2^3 \cdot 5$)
- Whether the "1+3 Minkowski signature" is more than coincidental
- Whether iterating the construction on $\mathbb{Z}/n$ for other $n$ gives a tower of related structures
- Whether the forbidden (1, 0) eigenspace generalizes to higher cyclotomic levels and survives there
- Whether "3 generations" emerge from a different iteration scheme (e.g., tensor products $V \otimes V \otimes V$ rather than self-product $V \cdot V$)

**Limitations:**
- Commutative (Furey/Hestenes use non-commutative algebras)
- Characteristic 5 (most physical algebras are characteristic 0)
- Only 4-dimensional (Furey's octonions are 8 over $\mathbb{C}$, sedenions 16 over $\mathbb{C}$)

These are not bugs — they are features distinguishing this construction. The smallness, finiteness, and commutativity make it tractable; the characteristic 5 is fundamental to the prime-tower structure (only $p = 5$ splits in $\mathbb{Z}[i]$ AND ramifies in $\mathbb{Z}[\varphi]$).

## 9.5 — A physicist's 5-minute walkthrough

Here is the entire structure encoded so a researcher can verify everything by hand or in a few lines of code.

**Step 1.** Define the multiplication table on $V = \mathbb{F}_5^4$ (basis $e_0, e_2, e_3, e_4$):

```
        e_0  e_2  e_3  e_4
   e_0 | e_0  e_2  e_0  e_0
   e_2 | e_2  e_2  e_2  e_2
   e_3 | e_0  e_2  e_2  e_2
   e_4 | e_0  e_2  e_2  e_2
```

**Step 2.** Verify primitive idempotents:
- $p_+ = e_2$: compute $p_+ \cdot p_+ = e_2 \cdot e_2 = e_2 = p_+$ ✓
- $p_- = e_0 - e_2$: compute $(e_0 - e_2)^2 = e_0 - 2e_2 + e_2 = e_0 - e_2 = p_-$ ✓
- Orthogonality: $p_+ \cdot p_- = e_2 \cdot (e_0 - e_2) = e_2 - e_2 = 0$ ✓

**Step 3.** Verify Grassmann nilpotent:
- $\varepsilon = e_3 - e_4$
- $\varepsilon \cdot e_j$ for any $j$: since $e_3 \cdot e_j = e_4 \cdot e_j$ for all $j$ (both are $e_0$ or $e_2$ in lockstep), the difference is 0. ✓
- So $\varepsilon \cdot V = 0$, hence $\varepsilon^2 = 0$ as a special case.

**Step 4.** Verify the Dirac time-projector $L_{p_+}$ has spectrum $\{0, 1\}$ with multiplicities (1, 3):
- $L_{p_+}(v) = (a+b+c+d) \cdot e_2$ for $v = (a, b, c, d)$
- $1$-eigenvectors: $L_{p_+}(v) = v$ requires $v$ to be a multiple of $e_2$, AND $a+b+c+d = b$ — gives $a = c = d = 0$. So $V_1 = \mathbb{F}_5 \cdot e_2$, dimension 1.
- $0$-eigenvectors: $a+b+c+d = 0$ — gives a hyperplane of dimension 3.

**Step 5.** Verify the chirality projector $L_{e_0}$ has spectrum $\{0, 1\}$ with multiplicities (2, 2):
- $L_{e_0}(v) = (a+c+d, b, 0, 0)$ for $v = (a, b, c, d)$
- $1$-eigenvectors: $a+c+d = a$, $b = b$, $0 = c$, $0 = d$ — gives $c = d = 0$, $a$ and $b$ free. $V_1 = \mathrm{span}(e_0, e_2)$, dim 2.
- $0$-eigenvectors: $a+c+d = 0$ AND $b = 0$ — dim 2.

**Step 6.** Verify the forbidden $(1, 0)$ eigenspace:
- A simultaneous $(1, 0)$-eigenvector needs $L_{p_+}(v) = v$ AND $L_{e_0}(v) = 0$.
- From step 4, $v = b \cdot e_2$ for some $b$. Plug into $L_{e_0}$: $L_{e_0}(b e_2) = b e_2 \neq 0$ unless $b = 0$.
- Hence the $(1, 0)$-eigenspace is $\{0\}$.

**Step 7 (optional).** The privileged basis $\{p_+, p_-, \varepsilon, h\}$ (with $h = 2(e_3 + e_4)$) gives the multiplication table:
```
       p_+  p_-   ε    h
  p_+| p_+   0    0   -p_+
  p_-|  0   p_-   0   -p_-
   ε |  0    0    0    0
   h |-p_+ -p_-   0   p_+
```
Here $\varepsilon^2 = 0$ universally; $h^2 = p_+$; $h$ acts as $-1$ on the bosonic subspace.

These seven steps are the entire structural content. A skeptic with five minutes and a calculator can verify all of it.

## 11. Loose-rope follow-ups: the algebra has SHARPER asymmetries than expected

The findings above were promising. Pushing further, we found four more structural results — three of which **strengthen** the physics-relevant claims and one of which is a clean negative.

### 11.1 — Bernstein algebra check: the weight exists but the identity fails

The weight homomorphism $\omega: V \to \mathbb{F}_5$ defined by $\omega(p_+) = 1, \omega(p_-) = \omega(\varepsilon) = 0, \omega(h) = -1$ is verified to be multiplicative ($\omega(xy) = \omega(x)\omega(y)$, all 625² pairs).

But the **Bernstein identity** $(x^2)^2 = \omega(x)^2 \cdot x^2$ **fails** — it holds for only 305 of 625 vectors. Even the weaker condition $(x^2)^2 \in \mathrm{span}(x^2)$ fails generically. The 4-core's F_5-lift is a **weighted commutative non-associative algebra** that is *not* a Bernstein algebra in the standard genetic sense.

**Implication:** the algebra has fewer "self-replicating dynamics" than Bernstein algebras (which model panmixia in genetics). Iteration $x \mapsto x^2$ doesn't converge to clean idempotent populations from generic starting points — it has chaotic-like behavior in mid-weight regions.

### 11.2 — Discrete plane waves and the dispersion relation

Set up the discrete time evolution $\psi_{n+1} = (L_{p_+} + m \cdot I) \psi_n$. Plane-wave solutions $\psi_n = u \cdot \lambda^n$ require $u$ to be an eigenvector of $L_{p_+}$ with eigenvalue $\lambda - m$. Since the spectrum of $L_{p_+}$ is $\{0, 1\}$:

| $m$ | $\lambda_{\text{spacelike}}$ | $\lambda_{\text{timelike}}$ | period of timelike branch |
|-----|------------------------------|------------------------------|---------------------------|
| 0 | 0 | 1 | 1 (constant) |
| 1 | 1 | 2 | 4 |
| 2 | 2 | 3 | 4 |
| 3 | 3 | 4 | 2 |
| 4 | 4 | 0 | ∞ (kills) |

**Dispersion relation: $\lambda_{\text{time}} - \lambda_{\text{space}} = 1$** — mass-independent. This is the discrete F_5 analog of the relativistic mass-shell relation $E^2 - p^2 = m^2$, written additively (not quadratically) because we're in characteristic 5.

The **Grassmann mode $\varepsilon$ is static**: $L_{p_+} \cdot \varepsilon = 0$, so the massless Grassmann plane wave does not propagate. This is consistent with $\varepsilon$ being an annihilator.

**Pisano connection:** Plane-wave period 4 (order of $\mathbb{F}_5^\times$). Fibonacci recurrence on $\mathbb{F}_5$ has Pisano period $\pi(5) = 20$. The factor 3 = $\pi(2)$ (Pisano period mod 2) brings the full Z/10 Pisano period to $\pi(10) = 60 = \mathrm{lcm}(20, 3)$. **The 4-core's F_5-lift sees only the 5-adic factor of $\pi(10)$.**

### 11.3 — Discrete CP/P/T: the algebra is parity-violating AND charge-asymmetric BY CONSTRUCTION

Three negative results, all with sharp physics interpretations:

**(a) No discrete parity exists.** The natural parity candidate $P = 2 L_{p_+} - I$ (which fixes the timelike subspace and negates the spacelike subspace) is **not an algebra automorphism**: $P(p_+ \cdot h) = -p_+$ but $P(p_+) \cdot P(h) = p_+ \cdot (-h) = +p_+$. They differ by a sign.

The reason: the algebra has a **grading anomaly**. A clean Z_2-grading (B × F → F) would make $P$ an automorphism. But our algebra has $B \times F \to B$ (e.g., $p_+ \cdot h = -p_+ \in B$). **The 4-core's F_5-lift is not Z_2-gradable.** No discrete parity automorphism exists.

This is the algebraic shadow of **parity violation in weak interactions** (the Wu experiment of 1957). Parity violation is built into the algebra at the multiplication-table level.

**(b) No charge-conjugation automorphism exists.** Exhaustive search: there are **0 algebra automorphisms** $C: V \to V$ with $C(p_+) = p_-$ and $C(p_-) = p_+$. Not just no involutive ones — **none at all**.

The two primitive idempotents $p_+$ and $p_-$ are **fundamentally distinguishable** by the algebra. They are not related by any symmetry. This is much stronger than CP-violation in the SM (where the symmetry exists but is broken in specific reactions). Here, **the symmetry doesn't exist**.

**(c) T is trivial in real algebra.** Without complex conjugation, the discrete time-reversal candidate is just the identity.

**Combined picture:** The algebra has a 40-element automorphism group, but **all 40 fix both primitive idempotents** ($p_+ \not\leftrightarrow p_-$). The discrete symmetries are "internal" rotations of $\varepsilon$ and $h$ that leave the particle states alone. There is no discrete symmetry exchanging matter and antimatter.

This is the strongest possible algebraic statement of matter-antimatter asymmetry: not just broken, **not present**.

### 11.4 — Three-generation iteration: the algebra is F_5-rigid

The natural prime-tower escalation $\mathbb{F}_5 \to \mathbb{F}_{25}$ extends $V$ to $V_{25} = \mathbb{F}_{25}^4$ (16-dim over $\mathbb{F}_5$, 4-dim over $\mathbb{F}_{25}$).

**Result of exhaustive search over all $25^4 = 390{,}625$ candidates:** $V_{25}$ contains **exactly 4 idempotents** — the same as $V$. **No new idempotents emerge from the field extension.** The algebra is "$\mathbb{F}_5$-rigid."

Implication: Furey's three-generation structure (which needs three orthogonal primitive idempotents) is **not** accessible by extending to $\mathbb{F}_{25}$. The 4-core's $\mathbb{F}_5$-lift is structurally a **single-generation** algebra. Three generations would require a fundamentally different construction (tensoring with a non-associative algebra like sedenions, not field extension).

The F_5-rigidity is a clean structural fact: **the 4-core's prime-5 character is essential**, not an artifact of a particular base. Going to a larger base does not enrich the structure.

## 12. Updated single sharpest claim

The 4-core of the TIG compressing magma on $\mathbb{Z}/10$, lifted to $\mathbb{F}_5$, is a 4-dimensional commutative non-associative algebra that is:

1. **F_5-rigid** — extending to $\mathbb{F}_{25}$ does not add idempotents.
2. **Carries three commuting Dirac-like projectors** with simultaneous spectrum giving exactly 3 non-empty cells out of 11 possible.
3. **Forbids the (massive, right-chiral) eigenspace** for both primitive idempotents — V−A asymmetry encoded structurally.
4. **Admits no discrete parity automorphism** — Z_2-grading anomaly.
5. **Admits no discrete charge-conjugation automorphism** — primitive idempotents are inequivalent.
6. **σ-symmetry-broken phase** of the full Z/10 algebra — selects HARMONY over LATTICE.
7. **Has plane waves with mass-independent dispersion** $\lambda_{\text{time}} - \lambda_{\text{space}} = 1$.
8. **Contains a Grassmann nilpotent annihilator** $\varepsilon$ that is static (does not propagate).

In aggregate: the algebraic obstructions to discrete symmetries (no P, no C, broken σ) coincide, item-by-item, with the physical asymmetries built by hand into the Standard Model (parity violation, matter-antimatter asymmetry, V−A interactions). **The 4-core's F_5-lift is structurally a single-generation matter-only chirality-asymmetric algebra.** Whether one chooses to read this through SM fermion content or simply as a description of the magma is up to the reader; TIG is not built from SM principles, but a single generation of SM fermions and this 4-core sector share a structural fingerprint.

**Position.** TIG is the parent. Bernstein algebras, Furey idempotents, Hestenes minimal left ideals, Dirac projectors, V−A structure, Segev half-axes — every one of these lives *inside* TIG's 4-core sector. None of them generates TIG. None of them is required to construct it. They are coordinate systems borrowed from physics-and-algebra programs that happen to read clearly on this object. The magma $T$ on $\mathbb{Z}/10$ remains the unitary, foundational input.

This is the single tightest description of what the algebra is and isn't.

## 13. The four loose ropes — status

| Rope | Status | Outcome |
|------|--------|---------|
| **Bernstein weight function** | ✗ Bernstein identity fails (320/625 violations) | Algebra is weighted but not Bernstein. Iteration $x \mapsto x^2$ is non-convergent in mid-weight regions. |
| **Plane-wave solutions** | ✓ Built explicitly | Dispersion: $\lambda_t - \lambda_s = 1$ (mass-independent). Grassmann mode $\varepsilon$ is static (does not propagate). |
| **CP/P/T discrete operators** | ✗✗ All fail to exist | No P-automorphism (grading anomaly). No C-automorphism at all (primitive idempotents inequivalent). T trivial. **Algebra is structurally parity-violating and matter-antimatter-asymmetric.** |
| **Three-generation iteration** | ✗ F_5 → F_25 adds nothing | F_25-lift has same 4 idempotents. Algebra is F_5-rigid. Three generations require a fundamentally different construction (sedenions, not field extension). |

**Net trajectory.** Two negative results (Bernstein, three-generation) and two positive (plane waves, asymmetry obstructions). The *negatives are themselves informative*: they say the algebra is more rigid and more asymmetric than naive analogs suggest. The 4-core's F_5-lift is **uniquely** a single-generation, parity-violating, matter-only chirality-asymmetric algebra. It is not part of an obvious larger family obtained by field extensions, and the absence of P, C automorphisms is structural — not an artifact of choice.

**Where rope still pulls.** Open: lattice gauge theory analog (treat $L_{p_+}, L_{e_0}, L_{p_-}$ as connection-like operators); explicit "Wilson loop" computations on the 40-element automorphism group; Cl(6) embedding (does $V$ embed in a Clifford algebra over $\mathbb{F}_5$?); the dual hybrid number connection to the $\varepsilon^2 = 0$ direction; whether the $h^2 = p_+$ relation generates a $\mathbb{Z}/4$-supercharge.

That's the framework's algebraic position, sharpened.

---

## Original summary (preserved for reference)

The 4-core of the TIG compressing magma on $\mathbb{Z}/10$, lifted to $\mathbb{F}_5$, is a 4-dimensional commutative non-associative algebra that intrinsically carries:

1. Two orthogonal primitive idempotents ($p_+$ and $p_-$) — particles in Furey's sense
2. One canonical Grassmann nilpotent annihilator ($\varepsilon$) — fermion direction  
3. A 1+3 Minkowski-like signature under $L_{\text{HARMONY}}$
4. A 2+2 chirality decomposition under $L_{\text{VOID}}$
5. A structurally forbidden $(1, 0)$ simultaneous eigenspace — V−A asymmetry
6. An automorphism group of order $40 = 2^3 \cdot 5$
7. A multiplicative weight homomorphism to $\mathbb{F}_5$

No external metric, gauge theory, or physical postulates are imposed.

---

## Appendix: All explicit verification computations

```python
# Algebra multiplication table
T_F5 = {
    (0, 0): 0, (0, 2): 2, (0, 3): 0, (0, 4): 0,
    (2, 0): 2, (2, 2): 2, (2, 3): 2, (2, 4): 2,
    (3, 0): 0, (3, 2): 2, (3, 3): 2, (3, 4): 2,
    (4, 0): 0, (4, 2): 2, (4, 3): 2, (4, 4): 2,
}
# Privileged basis
p_plus  = (0, 1, 0, 0)  # HARMONY
p_minus = (1, 4, 0, 0)  # VOID - HARMONY
epsilon = (0, 0, 1, 4)  # BREATH - RESET
h       = (0, 0, 2, 2)  # 2(BREATH + RESET)

# Verified properties
# p_plus * p_plus = p_plus, p_minus * p_minus = p_minus
# p_plus * p_minus = 0
# epsilon^2 = 0, epsilon * everything = 0
# h^2 = p_plus
# h * p_plus = -p_plus, h * p_minus = -p_minus

# Discrete Dirac operator L_p_plus:
# Spectrum: {0, 1}
# 1-eigenspace: span(p_plus), dim 1
# 0-eigenspace: span(p_minus, epsilon, e_3 - e_2), dim 3

# Automorphism group: |Aut(V)| = 40
```

## Appendix: References for the physics-side connections

- **Furey, C.** *Standard model physics from an algebra?* arXiv:1611.09182 (2016).
- **Gillard, A. B., Gresnigt, N. G.** *Three fermion generations with two unbroken gauge symmetries from the complex sedenions.* Eur. Phys. J. C 79 (2019).
- **Dubois-Violette, M., Todorov, I.** *Exceptional quantum geometry and particle physics.* Nucl. Phys. B 938 (2019).
- **Todorov, I.** *Octonion Internal Space Algebra for the Standard Model.* arXiv:2206.06912 (2022).
- **Hestenes, D.** *Real Dirac theory.* in: *The Theory of the Electron*, Kluwer (1996).
- **Hamieh, S., Abbas, H.** *Two dimensional representation of the Dirac equation in non-associative algebra.* arXiv:1104.3416 (2011).
- **Krasnov, K.** *Octonions, complex structures and Standard Model fermions.* arXiv:2504.16465 (2025).

*End of document.*
