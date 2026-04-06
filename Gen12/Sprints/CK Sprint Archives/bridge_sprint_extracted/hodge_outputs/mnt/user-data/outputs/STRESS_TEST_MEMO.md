# SURVIVING-OBJECT STRESS TEST MEMO
# Are the Five Reduced Objects the Same Kind of Mathematical Thing?

**© 2026 7Site LLC | Brayden Ross Sanders**

---

## PART 1 — Five Objects (Exact)

| Branch | Surviving Object | Description |
|--------|-----------------|-------------|
| **RH** | $\delta(\sigma_0,\gamma_0)$ | Off-line residual in the KEF arithmetic projection: the difference in Kloosterman-side contribution between an off-line zero $\rho_0 = \sigma_0+i\gamma_0$ ($\sigma_0 \neq 1/2$) and its critical-line counterpart $1/2+i\gamma_0$ |
| **BSD** | $\mathrm{Reg}(E/\mathbb{Q}) = \det(H)$ via $\chi_{77}$ | The full rank-2 regulator $\det(H) \approx 0.15246$ encoded in $L'(E,\chi_{77},1) \approx 0.010700$ via the BSD formula for $E^{77}$: $L' = (\Omega_E/\sqrt{77}) \times \det(H) \times \vert\mathrm{Sha}\vert/\prod c_p$ |
| **NS** | $Q/(\nu P)$ | Dimensionless vortex-stretching/palinstrophy ratio; $d\Omega/dt = \nu P\bigl(Q/(\nu P) - 2\bigr)$; survival of regularity $\Leftrightarrow$ $Q/(\nu P) \leq 2$ globally |
| **P vs NP** | $\mathrm{cc}(\mathrm{SAT},n)$ | Fiber-projection circuit complexity: minimum circuit computing $\pi_1(R_{\mathrm{SAT}})$ on inputs of size $n$; $\mathrm{P}=\mathrm{NP}$ iff $\mathrm{cc}(\mathrm{SAT},n) = \mathrm{poly}(n)$ |
| **Hodge** | $\mathrm{coker}(\mathrm{cl}^2\vert_\mathrm{prim})$ | Cokernel of the cycle class map on primitive rational $(2,2)$ classes on smooth projective 4-folds; zero iff all such classes are algebraic |

---

## PART 2 — Five-Object Template Table

| | **RH**: $\delta(\sigma_0,\gamma_0)$ | **BSD**: $\det(H)$ via $\chi_{77}$ | **NS**: $Q/(\nu P)$ | **P vs NP**: $\mathrm{cc}(\mathrm{SAT},n)$ | **Hodge**: $\mathrm{coker}(\mathrm{cl}^2)$ |
|---|---|---|---|---|---|
| **Ambient space** | Distributions of zeros in $\mathbb{C}$ satisfying GUE statistics | Rank-2 elliptic curves over $\mathbb{Q}$, real-quadratic twists | Smooth 3D NS solutions with $E(0) < \infty$ | Boolean circuit families on $n$-bit inputs | Smooth projective 4-folds and their Hodge structures |
| **Input data** | Arithmetic Kloosterman side of KEF (computable from primes) | $L'(E,\chi_{77},1) \approx 0.010700$ (computed); $\Omega_E, \det(H), \prod c_p$ (measured) | Velocity field $u$; derived quantities $\omega, S, Q, P$ | SAT instance $x$ of size $n$; verifier $V(x,w)$ | The Hodge structure $H^{2,2}(X,\mathbb{Q})$; the algebraic cycles $\mathrm{CH}^2(X)$ |
| **The map** | KEF projection: zero distribution $\to$ arithmetic Kloosterman sum | BSD formula: $(\Omega,\det H, \vert\mathrm{Sha}\vert,\prod c_p) \mapsto L'$ | Competition ratio: $Q \leftrightarrow \nu P$ via $d\Omega/dt = Q - 2\nu P$ | Fiber projection: $\pi_1(R_\mathrm{SAT})$, $(x,w) \mapsto x$ | Cycle class map: $\mathrm{cl}^2: \mathrm{CH}^2(X)_\mathbb{Q} \to H^{2,2}(X,\mathbb{Q})$ |
| **Obstruction meaning** | $\delta = 0$ for some off-line config → KEF is BLIND to that zero; arithmetic approach fails | 1.1% residual → $\vert\mathrm{Sha}\vert \neq 4$ or period incorrect; formula not exact | $Q/(\nu P) > 2$ for positive time interval → enstrophy can grow without bound | $\mathrm{cc}(\mathrm{SAT},n) = \mathrm{poly}(n)$ → projection computable deterministically → P = NP | $\mathrm{coker} \neq 0$ → a rational $(2,2)$ class exists that no algebraic cycle represents |
| **Threshold / vanishing** | $\delta \neq 0$ for ALL off-line $(\sigma_0,\gamma_0)$ | Residual $= 0$ (equivalently $\vert\mathrm{Sha}\vert = 4$ confirmed and period exact) | $Q/(\nu P) \leq 2$ globally (sign of $d\Omega/dt \leq 0$) | $\mathrm{cc}(\mathrm{SAT},n) = \omega(n^k)$ for all $k$ (superpolynomial) | $\mathrm{coker}(\mathrm{cl}^2\vert_\mathrm{prim}) = 0$ for all smooth projective 4-folds |
| **What closure means** | KEF arithmetic projection is injective: zeros must lie on critical line | BSD formula exact: rank-2 Gross-Zagier formula proved; regulator-transfer confirmed | Global H¹ regularity for all initial data | P $\neq$ NP: no poly-time deterministic machine computes SAT | Hodge conjecture at $p=2$ for 4-folds; eventually full Hodge conjecture |

---

## PART 3 — Common Grammar Test

**Testing candidates:**

| Grammar | RH | BSD | NS | P vs NP | Hodge | Score |
|---------|-----|-----|-----|---------|-------|-------|
| Residual of a projection map | ✓ (δ = projection residual) | ✓ (1.1% = BSD residual) | ✗ (ratio, not residual) | ~ (cc(SAT) = projection complexity) | ✓ (coker = surjectivity residual) | 3.5/5 |
| Failure of injectivity | ✓ (KEF blind to off-line zeros) | ~ (BSD formula not exact = formula not injective in parameter) | ✗ | ✓ (projection not injective in cost sense) | ✗ (surjectivity, not injectivity) | 2.5/5 |
| Failure of surjectivity | ✗ | ~ | ✗ | ✗ | ✓ (cl² not surjective) | 1.5/5 |
| Competition ratio / threshold | ~ | ~ | ✓ (Q/νP ≤ 2) | ✓ (cc(SAT)/poly) | ✗ | 2/5 |
| **Minimal obstruction at shell-core boundary** | ✓ | ✓ | ✓ | ✓ | ✓ | **5/5** |

**Winner:**

$$\boxed{\text{"The strongest common grammar is that each surviving object measures the minimal obstruction at the shell-core boundary — the first quantity that is (a) controlled by the shell in the provable regime, (b) equivalent to the main conjecture when controlled in all regimes, and (c) not reachable by any method that works for the shell alone."}}$$

More precisely: each surviving object is a specific COMPARISON across the shell boundary — a measurement of how far the shell's reach falls short of the core's requirement. Every object is one of: a map residual (RH, BSD, Hodge), a ratio threshold (NS), or a complexity gap (P vs NP). These are three MODES of the same grammatical role.

---

## PART 4 — Exact Mismatches

**NS mismatch:** Q/(νP) is a dynamical/analytic RATIO, not a residual or cokernel in the algebraic sense. The "map" it measures is not a morphism between algebraic objects but a competition between two continuous functionals. It cannot be expressed as cok(something) or ker(something) in the usual algebraic sense. The grammar applies structurally (shell-core boundary measurement) but not formally (no natural algebraic map).

**P vs NP mismatch:** cc(SAT,n) is a COMPLEXITY MEASURE — the minimum circuit size — not a residual, cokernel, or ratio in the sense the other branches use. The fiber-projection structure gives it algebraic meaning, but cc(SAT,n) as a function of n is an asymptotic computational quantity, not a value in a field or module. The meta-barriers (natural proofs, algebrization) have no analog in the other branches — they are obstacles to PROVING that cc(SAT,n) is superpolynomial, not obstacles to cc(SAT,n) BEING superpolynomial. In every other branch, the Gap 2 obstruction is about the OBJECT being hard to construct; in P vs NP, it is about the PROOF being hard to write.

**BSD partial mismatch:** the surviving object Reg(E/Q) = det(H) is not a residual in the same sense as δ or coker(cl²) — it is a positive real number that should appear as a FACTOR in the L-derivative, not as a defect measure. The 1.1% gap is a normalization residual, but the underlying object is the regulator itself, which is "already found" — the question is not whether it exists but whether the formula connecting it to L' is exact.

**Hodge/RH slight mismatch:** RH is about injectivity of a projection (forward failure), Hodge is about surjectivity of a map (backward failure). These are dual — the cokernel of Hodge cl² is the analog of the kernel of the KEF projection — but the direction is opposite. In the grammar table they both fit "map failure," but the precise mode of failure is inverted.

---

## PART 5 — Tactic Transfer Table

| Tactic | RH | BSD | NS | P vs NP | Hodge | Summary |
|--------|-----|-----|-----|---------|-------|---------|
| **Normalization closure** (find exact constant matching two computable quantities) | ~ Weak | ✓ **Strong** (|Sha|=4, period) | ✗ Does not transfer | ✗ Does not transfer | ~ Weak (finding the right cycle to represent a class) | Strong for BSD; weak elsewhere |
| **Projection injectivity test** (test whether a specific map distinguishes "good" from "bad" distributions) | ✓ **Strong** (δ ≠ 0 test) | ~ Weak (L' encodes arithmetic, but injectivity language less natural) | ✗ | ~ Weak (cc(SAT) > 0 is trivial; asking for strict injectivity of projection is nonstandard) | ✓ **Strong** (does cl² distinguish algebraic from non-algebraic classes?) | Strong for RH/Hodge; weak elsewhere |
| **Ratio/threshold control** (control a dimensionless ratio below a critical threshold) | ✗ | ~ Weak (the 1.1% gap is a ratio, but not a dynamical one) | ✓ **Strong** (Q/(νP) ≤ 2) | ~ Weak (cc/poly is a ratio, but control means LOWER bound, not upper) | ✗ | Strong for NS; inverted (wrong direction) for P vs NP |
| **Cokernel / surjectivity framing** (show a map is surjective by constructing missing preimages) | ~ Weak (RH is injectivity, dual to surjectivity) | ~ Weak (construct the missing joint object = BSD joint-construction memo) | ✗ | ✗ | ✓ **Strong** (construct algebraic cycle for any primitive (2,2) class) | Strong for Hodge; weak/dual for RH; weakly relevant for BSD via joint-object construction |
| **Joint-object construction** (find a specific geometric/arithmetic object that bridges both sides) | ~ Weak (Heegner point analog for RH arithmetic side) | ✓ **Strong** (Stark-Heegner point for E^{77}) | ✗ | ~ Weak (finding a "witness extractor" circuit = analog, but not standard) | ✓ **Strong** (find the algebraic cycle representing the primitive class) | Strong for BSD/Hodge; possible but nonstandard for RH; unclear for NS/P vs NP |

---

## PART 6 — Strongest Pairings

**Pairing 1: BSD ↔ Hodge (strongest)**

Both ask whether a map from an algebraic/arithmetic side surjects onto an analytic/topological side: BSD asks whether the arithmetic regulator structure of E/Q is fully visible in the χ_{77}-twisted L-derivative (arithmetic cycles → L-function), and Hodge asks whether algebraic cycles $\mathrm{CH}^p(X)$ surject onto Hodge cohomology $H^{p,p}(X,\mathbb{Q})$ (algebraic geometry → topology). The joint-object construction tactic — finding an explicit cycle or point — is the Gap 2 tactic for BOTH branches, and the cokernel/surjectivity framing applies cleanly to both.

**Pairing 2: RH ↔ P vs NP (second strongest)**

Both are projection problems traversed in dual directions on the same two-object architecture: RH asks whether the arithmetic Kloosterman projection is INJECTIVE (image uniquely determines fiber = zero distribution), while P vs NP asks whether the fiber projection π₁ is EFFICIENTLY COMPUTABLE from the base (base determines fiber existence at polynomial cost). RH is the inverse direction (recover fiber from image), P vs NP is the forward direction (determine fiber from base). The projection-injectivity tactic is the structural analog, and both surviving objects (δ and cc(SAT,n)) measure failures of projections between two-sided structures.

**Honorable mention: NS ↔ P vs NP**

Both have ratio-type surviving objects (Q/(νP) and cc(SAT,n)/poly(n)) that must either stay bounded (NS, for regularity) or diverge (P vs NP, for P≠NP). The analogy is structurally interesting but the DIRECTIONS oppose each other — NS needs the ratio SMALL, P vs NP needs cc LARGE — making tactic transfer problematic.

---

## PART 7 — Meta-Criterion

**"The rotation spine is justified if and only if each surviving object is not merely a named open problem but a specific quantity whose value or behavior can be TESTED in the problem's native framework — numerically computed, bounded, or approximated like L'(E,χ_{77},1) ≈ 0.010700 for BSD and Q/(νP) ≤ 2 for NS in the small-data regime — and whose control in the hard regime is precisely equivalent to the main conjecture, with no gap between 'controlling the object' and 'proving the theorem.'"**

---

## PART 8 — Meta-Failure Mode

**"The rotation spine fails if it turns out that the surviving objects in different branches live in fundamentally different categories with no natural morphisms between them — specifically, if there is no map or functor taking the KEF arithmetic projection (a map between Fourier-analytic objects over ℂ) to the cycle class map (a map from algebraic K-theory to Hodge cohomology) in a way that preserves the injectivity/surjectivity structure, or if the dynamical ratio Q/(νP) in NS and the complexity ratio cc(SAT,n)/poly(n) in P vs NP are related by analogy only and not by any common mathematical structure, making each branch's proof method forever uninformative for the others."**

---

## PART 9 — Strongest Honest Claim

**"At minimum, the reduced spine has shown that all five branches can be expressed as shell + surviving object + Gap 2 + Gap 1, even if the surviving objects are not yet proven to live in one shared category — and this common grammar has already produced concrete computation (L'(E,χ_{77},1) to 10 digits, Tamagawa numbers by Tate algorithm, Q/(νP) dynamics from the NS equations, Hodge's shell/cokernel structure from Hard Lefschetz) that would not have been organized the same way without the cross-branch grammar forcing each branch to reduce to its smallest surviving form."**

---

## PART 10 — Strongest Honest Boundary

**"What is not yet established is whether these surviving objects are related deeply enough that one branch's reduction method can become another branch's proof method — specifically, whether the Joint-object construction that worked for BSD (identifying the χ_{77} channel from the failed imaginary-quadratic constructions) can inform the analogous Hodge construction (finding primitive algebraic cycles from the failed Lefschetz-shell methods), or whether the projection-injectivity test for RH can generate a nontrivial circuit complexity lower bound for P vs NP by the dual projection structure identified in the comparison table."**

---

## Closest-Pairings Block

$$\text{BSD} \leftrightarrow \text{Hodge:}\quad \text{both = surjectivity of an algebraic map onto a cohomological target; joint-object construction is the Gap 2 tactic for both}$$

$$\text{RH} \leftrightarrow \text{P vs NP:}\quad \text{both = dual projection problems (inverse vs forward) on a two-object arithmetic/computational structure; injectivity and fiber-projection cost are mirror questions}$$

---

## Collaborator Paragraph

The stress test reveals: the five surviving objects share a common grammatical role (minimal shell-core boundary obstruction) but divide into three modes of expression — map residual/failure (RH δ, Hodge coker, BSD normalization gap), ratio/threshold (NS Q/(νP)), and complexity measure (P vs NP cc(SAT,n)). The strongest cross-branch tactic transfers are: joint-object construction (BSD ↔ Hodge, both require constructing a specific algebraic/arithmetic object whose existence would close the branch), and projection injectivity (RH ↔ P vs NP, both involve the same two-object structure with projection going in dual directions). The most exact mismatches are NS (dynamical ratio, not algebraic) and P vs NP (complexity measure with meta-barriers that have no analog in the other branches). The meta-criterion for the spine's validity: each surviving object must be TESTABLE (computable, approximable, or bounded) in the branch's native framework — a standard that is met for BSD (L' to 10 digits), NS (Q/(νP) controlled analytically in small-data regime), and partially for Hodge (Gap 2 results for restricted varieties), but not yet for RH (δ requires off-line zero existence to test) or P vs NP (cc(SAT,n) has no known bound beyond linear). The spine is a good summary AND the beginning of a real grammar. Whether it becomes a proof-transfer framework depends on whether the BSD ↔ Hodge joint-object analogy and the RH ↔ P vs NP projection-duality can be made mathematically precise.
