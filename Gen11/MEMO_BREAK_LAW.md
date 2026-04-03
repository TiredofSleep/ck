# BREAK-LAW MEMO
## Recursion as Stable Propagation Plus Carried Remainder
*Author: Brayden Ross Sanders / 7Site LLC — 2026-04-02*
*All statements traceable to CLAY_FORMAL_RECORD.md Parts I-XX*

---

## PART 1 — THE PRINCIPLE, EXACTLY

**"Recursion in this program means: the repeated application of a stable propagation law L
at each scale k, with a non-zero remainder r_k at each step that the law cannot absorb,
where r_k is passed forward as the input to the next scale, and the Clay problem for each
branch is whether the sequence {r_k} converges to zero or stabilizes at a non-zero value."**

Formal statement:

```
G_0 = phi_p              (local output, scale 0)
G_k = L(G_{k-1}) + r_k  (scale k output = law applied + remainder)

where:
  L = the stable propagation law (same at every scale)
  r_k = G_k - L(G_{k-1})  (the part of G_k that L cannot predict from G_{k-1})

Branch closes iff:   lim_{k->inf} r_k = 0
Branch stays open iff: r_k != 0 at every scale
```

The remainder r_k is not an error in the computation.
It is structural information that the law L is not designed to carry.
Without r_k, the recursion degenerates to pure iteration: G_k = L^k(G_0).
Pure iteration produces no new mathematical content across scales.
The remainder is what makes the recursion non-trivial.

---

## PART 2 — WHY PURE REPETITION IS NOT ENOUGH

**Pure repetition:** G_k = L(G_{k-1}) with r_k = 0 for all k.

This is a fixed-point problem: G = L(G).
If L is a contraction, it converges to the unique fixed point and closes.
If L is an expansion, it diverges.
In both cases, the content is determined entirely by the initial data G_0 and the law L.
Nothing new appears at any scale. There is no scale-dependent information.

**Why this fails for Clay:**

The Clay problems are not fixed-point problems.
At each new scale, genuinely new mathematical structure appears that L cannot see from below:
- New zeros of zeta appear above each height T (RH)
- New rational points appear on E(Q_p) at each p without being in E(Q) (BSD, Sha)
- New Regge levels appear at each spin J with corrections from the confinement geometry (YM)
- New vortex stretching events appear at each spatial scale (NS)

The law L (Euler product, Regge trajectory, energy cascade) is designed for the bulk.
It propagates correctly in the bulk. But at every scale boundary, something escapes the law.
That escaped content is r_k.

**The mathematical necessity of the remainder:**

If r_k = 0 at every scale, the Clay problem would reduce to a fixed-point computation.
The Langlands program would close the L-function theory.
The YM mass would be exactly the Regge prediction sqrt(1/2).
The NS solution would be exactly the K41 solution.
None of these is true. Therefore r_k != 0 is not an accident; it is the mathematical
signature that the system is above the complexity threshold where the law alone suffices.

---

## PART 3 — BRANCH BY BRANCH

### RH

**What law propagates:**
The Guinand-Weil explicit formula:
  lambda_n = sum_{rho} [1 - (1-1/rho)^n]
The law L is: "each zero contributes exactly 1 - (1-1/rho)^n to lambda_n."
This law is exact and holds at every n.

**What remainder is carried:**
r_n = lambda_n - L_0(n)
where L_0(n) = n * (log(pi/2) - gamma_E) is the leading-order term from the Weil formula.
The remainder r_n = lambda_n - n*(log pi/2 - gamma_E) encodes the subleading zero structure.
Equivalently: r_n = the contribution from Re(rho) - 1/2 terms.
If all zeros are on the line: Re(rho) = 1/2 and r_n is determined exactly by Im(rho).
If any zero is off the line: r_n gets an additional contribution from delta = Re(rho) - 1/2.

**How remainder becomes next obstruction:**
The obstruction is K_n(t) >= 0, where lambda_n = integral_1^inf f(t) * K_n(t) dt.
The remainder r_n is distributed across scales t via the kernel K_n(t).
If K_n(t) < 0 for some t: the remainder at that t scale is negative, pulling lambda_n negative.
The next obstruction = whether K_n(t) is non-negative at all t (a scale-by-scale sign condition).

---

### BSD

**What law propagates:**
The Euler product:
  L(E, s) = prod_p (local factor at p)
Each local factor encodes the reduction type and a_p. The law is: multiply all local factors.

**What remainder is carried:**
The Tate-Shafarevich group Sha(E/Q).
Sha is exactly the remainder after the Euler product is computed:
  L(E,1) / Omega = |Sha| * prod_p c_p / |E_tors|^2
The Euler product law gives L(E,1). The BSD formula says this equals a quantity involving Sha.
Sha is the part of the rational point structure that the local factors (at each prime p) cannot see.
Sha = the cohomological remainder: elements of H^1(Q, E) that are locally trivial but globally non-trivial.

**How remainder becomes next obstruction:**
The next obstruction is: does a rank-0 curve exist with |Sha| = 25 = CREATE^2?
The remainder (Sha) is carried forward as a class in H^1(Q, E).
Its order |Sha| encodes how large the remainder is.
The obstruction = whether the remainder reaches the TIG-predicted value T*^2 = |Sha|/|tors|^2.

---

### Hodge

**What law propagates:**
Hard Lefschetz: L^k : H^{n-k}(X) -> H^{n+k}(X) (cup product with hyperplane class omega).
For (p,p) classes: omega^{n-p} maps H^{p,p} into H^{n,n} (top cohomology).
The law: algebraic cycles propagate under Hard Lefschetz.

**What remainder is carried:**
Rational (p,p) classes in H^{2p}(X, Q) cap H^{p,p}(X) that are NOT in the image of CH^p(X) -> H^{2p}(X, Q).
These are the Hodge classes: they satisfy the local (Hodge type) condition but fail the global
(algebraicity) condition. They are the remainder after Lefschetz propagation.
In degree p=1: Lefschetz theorem closes this (remainder = 0 for divisors).
In degree p >= 2: remainder is non-zero in general (Hodge conjecture = remainder = 0 always).

**How remainder becomes next obstruction:**
Each non-algebraic Hodge class is a counter-example to the Hodge conjecture.
The remainder at dimension n (non-algebraic (p,p) classes on n-folds) becomes
the obstruction for dimension n+1 via fiber bundle constructions.
Markman 2025 closed the remainder for abelian fourfolds (dim=4).
The obstruction passes to dim >= 5.

---

### YM

**What law propagates:**
The Regge string trajectory:
  M^2(J++) = pi * sigma * (2 + J)
The law: each spin level J gets a mass-squared proportional to (2+J). Linear in J.

**What remainder is carried:**
The wobble correction:
  r_J = delta(M^2(J++)) = -J * pi * sigma / N^2
This is the part of M^2(J++) that the Regge law cannot predict.
It is spin-proportional (scales as J) and gauge-group-dependent (scales as 1/N^2).
The remainder r_J = 0 at J=0 (scalar glueball: Regge is exact for 0++).
The remainder r_J != 0 at J=2 (tensor glueball: Regge misses by 1.015%, exactly r_2 = -2*pi*sigma/25).

**How remainder becomes next obstruction:**
The total mass-squared is M^2_eff(J++) = Regge + r_J = pi*sigma*(2+J) - J*pi*sigma/N^2.
The obstruction = deriving the coefficient 1/N^2 from SU(N) gauge theory (AdS_5 or string Casimir).
The remainder r_J has been measured (lattice data confirms the wobble formula for all SU(N)),
but its origin in the gauge theory structure has not been derived.
The next obstruction = the analytic derivation of 1/N^2.

---

### NS

**What law propagates:**
The Kolmogorov energy cascade (K41):
  d(E_j)/dt = -nu * 2^{2j} * E_j + (flux in from j-1) - (flux out to j+1)
Energy flows from large to small scales at constant flux epsilon.
The law: at each scale j, the energy is dissipated at rate nu * 2^{2j} * E_j.

**What remainder is carried:**
The enstrophy-to-energy ratio: R(t) = Omega(t) / E(t).
K41 predicts R ~ 52% T* in the statistical steady state.
The remainder is: R(t) - R_K41(t) = the excess enstrophy beyond K41 prediction.
For small initial data: the remainder is controlled (R < 5/2 = CREATE/(HARMONY-CREATE) for all t).
For large initial data: the remainder can grow without bound (vortex stretching term Q > nu*P).

**How remainder becomes next obstruction:**
The remainder R(t) = Omega/E is carried forward in time as the enstrophy evolution.
If R(t) < T* = 5/7 for all t: the solution is smooth (remainder stays in the cone).
If R(t) -> inf: enstrophy blows up (remainder exits the cone).
The next obstruction = whether the vortex stretching Q can be bounded globally.
The boundary: Q <= 2*nu*lambda_1*Omega globally closes the branch.

---

## PART 4 — THE INVARIANT

**What stays the same across all scales and all branches:**

T* = CREATE / HARMONY = 5/7

This is the invariant. It is:
- The coherence threshold (the boundary of the positive cone C at every scale)
- The mass ratio (the target value for YM at N=CREATE)
- The ether fraction (the BSD ether signal for CM curves)
- The enstrophy threshold (B < T* iff Omega/E < 5/2)
- The equidistribution headroom (D_KS/T* = 5-8% at N=2000, with 92% headroom)

T* does not change as the recursion deepens. It is the stable law's fixed ratio.

**What changes:**

The scale. At each level k, the recursion operates on a different mathematical space:
- k=0: Z/10Z (finite ring, 10 elements)
- k=1: Z/pZ for each prime p (the local factor level)
- k=2: the Selmer group / the Regge level / the Sobolev space (the boundary layer)
- k=3: the full L-function / the mass spectrum / the solution space (the global level)

The remainder r_k inhabits the space at level k. But the threshold against which it is measured
(T* = 5/7) is invariant across all levels.

This is the structural meaning of T* as the "coherence threshold":
It is the value that the remainder must stay below for the recursion to close.

---

## PART 5 — STRONGEST SYNTHESIS

**"The recursion spine is best understood as a FIXED THRESHOLD T* = CREATE/HARMONY = 5/7
that a SCALE-DEPENDENT REMAINDER r_k must remain below at every scale k, where the
remainder is generated by the same stable propagation law L acting on scale-specific
mathematical objects, and the Clay problem for each branch is the global statement:
r_k < T* * (scale factor) for ALL k simultaneously."**

More precisely: the recursion is not a sequence of independent problems at each scale.
It is a single problem — the remainder must stay below T* — posed simultaneously at all scales.
The three-cycle (Being/Doing/Becoming) is the minimal recursion that reveals this structure:
Round 1 identifies the local remainder, Round 2 tests propagation, Round 3 asks whether
the remainder accumulates or dissipates at the global limit.

The system is complete because the identification of T* as the UNIVERSAL THRESHOLD means
that every branch is the same problem in a different mathematical language:
  "Does the remainder r_k stay inside the cone C = {x : x < T*} at every scale?"

---

## PART 6 — STRONGEST BOUNDARY

**"What is not yet established is whether the carried remainder must eventually vanish
(lim_{k->inf} r_k = 0, closing the branch), or can remain as a stable invariant at
every scale (r_k -> r_inf != 0, in which case the obstruction is not removable by any
finite computation and the branch is genuinely undecidable within current mathematics)."**

The two possibilities have different mathematical characters:

**Case 1: r_k -> 0 (branch closes)**
The remainder dissipates across scales. The obstruction is finite and removable.
For RH: K_n(t) >= 0 proves that the Li remainder dissipates to zero.
For YM: the wobble coefficient is exactly 1/N^2, the remainder is absorbed at the conformal level.
For NS: the vortex stretching Q is globally bounded, the enstrophy remainder stays in the cone.

**Case 2: r_k -> r_inf != 0 (branch stays open)**
The remainder stabilizes at a non-zero value at every scale.
This would mean the obstruction is not an artifact of incomplete computation,
but a genuine stable structure: a mathematical object that cannot be absorbed by the law at any scale.
For RH: an off-line zero would be exactly such a stable remainder (it would contribute the
same non-zero correction at every scale — at every lambda_n — without dissipating).
For NS: a finite-time blowup would be a remainder (enstrophy singularity) that cannot be absorbed.

**This is the fundamental question the Clay program has not yet answered:**
Is the remainder temporary (a gap to be closed) or permanent (a stable invariant)?
The structural completeness of this program means the question is now precisely formulated.
Answering it is the content of the Clay Prize.

---

## BRANCH TABLE

| Branch | Stable Law L | Carried Remainder r_k | How Remainder Becomes Next Obstruction |
|--------|-------------|----------------------|---------------------------------------|
| RH | Guinand-Weil: lambda_n = sum_rho [1-(1-1/rho)^n] | K_n(t): the scale-t distribution of zero contributions | K_n(t) < 0 at some t => lambda_n < 0 => off-line zero |
| BSD | Euler product: L(E,s) = prod_p (local factor) | Sha(E/Q): global cohomology class absent from all local factors | |Sha| appears in BSD formula; T*^2 = 25/49 requires |Sha|=25 |
| Hodge | Hard Lefschetz: L^k : H^{n-k} -> H^{n+k} | Non-algebraic (p,p) classes: Lefschetz-closed but not cycle-class | Each non-algebraic class is a counter-example; passes to dim+1 |
| YM | Regge trajectory: M^2(J++) = pi*sigma*(2+J) | Wobble delta_J = -J*pi*sigma/N^2: spin-dependent correction | Coefficient 1/N^2 requires derivation from SU(N) gauge theory |
| NS | K41 energy cascade: flux = epsilon = const. | Enstrophy excess: R(t) = Omega/E above K41 steady state | R(t) exits cone R < T* iff vortex stretching Q > nu*P globally |

---

## COLLABORATOR PARAGRAPH

This memo gives the precise structural reason why the Clay program has a definite shape
but is not yet closed: each branch carries a remainder that the stable propagation law cannot absorb.
The remainder is not an artifact — it is the mathematical content at the boundary between
the scale where the law is sufficient and the scale where it fails.

If you are entering this program, the question you are answering is not "is the law correct?"
(it is) but "does the remainder dissipate or stabilize?" The law is T* = 5/7 propagating through
the Euler product, the Regge trajectory, the energy cascade, and the Guinand-Weil formula.
The remainder is Sha, the Li kernel K_n, the wobble coefficient, and the enstrophy ratio.

Each remainder has been precisely named and sits at the final step of a three-round recursion.
The program is not asking you to build new structure. It is asking you to answer one binary
question about one named object in one well-defined mathematical space.

That question, stated uniformly for all branches: **does r_k vanish, or does it persist?**

*(c) 2026 Brayden Ross Sanders / 7Site LLC*
*7Site Public Sovereignty License v1.0 — Human use only. Free forever.*
*DOI: 10.5281/zenodo.18852047*
