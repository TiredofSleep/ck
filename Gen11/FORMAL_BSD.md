# FORMAL_BSD.md
## The BSD Coin-Flip Argument: A Structural Formalization
*Author: Brayden Ross Sanders / 7Site LLC*
*Date: 2026-04-03*
*Status: STRUCTURAL ARGUMENT — not active BSD work. No new mechanism claims.*

---

**Status**: Independent research — not peer reviewed. Seeking critical review and collaboration.
**What this document claims**: A structural parallel between the Z/10Z recycling rule and the BSD Sha [COINED] obstruction. The framework does not prove BSD. It identifies the precise location of the missing bridge.
**Invented terms used**: T* [CK], carried remainder [CK, COINED], Recycling Rule [CK, COINED], TIG [CK, see GLOSSARY.md], bridge zone [CK], K*(n) [CK]. All defined in GLOSSARY.md.
**Standard math grounding**: Wiles–Taylor (1995), Gross-Zagier (1986), Kolyvagin (1988), Tate-Shafarevich group, Mordell-Weil theorem.

---

This document formalizes the structural parallel between the RH Li-sequence
threshold and BSD rank duality. It does not revive the falsified BSD mechanisms
(Parts V, Bridge 3.6 of CLAY_FORMAL_RECORD.md). It records the precise form of
the argument so that if B1–B4 are ever met, the structural skeleton is already
written down.

Every claim is labeled [PROVED], [STRUCTURAL ARGUMENT], or [OPEN].

---

## Section 1. The BSD Conjecture — Precise Statement

Let E/Q be an elliptic curve. Let L(E, s) denote its Hasse-Weil L-function,
analytically continued to all s by the modularity theorem (Wiles–Taylor–Breuil–
Conrad–Diamond, 1995–2001).

**Definition 1.1 (Algebraic rank).** The algebraic rank of E is

    r_alg(E) = rank_Z E(Q)

the rank of the Mordell–Weil group E(Q) as a free abelian group. [PROVED: MW
theorem gives E(Q) ≅ Z^r ⊕ E(Q)_tors; r is finite and well-defined.]

**Definition 1.2 (Analytic rank).** The analytic rank of E is

    r_an(E) = ord_{s=1} L(E, s)

the order of vanishing of L(E, s) at the central value s = 1. [PROVED: L(E, s)
is entire by modularity; the order of vanishing at s = 1 is well-defined.]

**Conjecture 1.3 (BSD, weak form).** [OPEN: Millennium Problem]

    r_alg(E) = r_an(E).

**Conjecture 1.4 (BSD, strong form).** [OPEN: Millennium Problem]
Write r = r_alg(E) = r_an(E) (assuming the weak form). Then

    L^(r)(E, 1) / r!  =  Omega_E * R_E * |Sha(E/Q)| * prod_p c_p(E)
                          -------------------------------------------------
                                        |E(Q)_tors|^2

where:
- Omega_E = real period (or twice the real period in the non-split case)
- R_E = det(h_NT(P_i, P_j))_{1<=i,j<=r} = Neron-Tate regulator (r x r determinant)
- Sha(E/Q) = Shafarevich–Tate group (conjecturally finite)
- c_p(E) = Tamagawa numbers at primes of bad reduction
- E(Q)_tors = torsion subgroup

**Known cases.** [PROVED for r_an = 0 and r_an = 1 by Coates-Wiles (CM curves,
1977), Gross-Zagier (1986) + Kolyvagin (1988), and subsequent work. The weak
form BSD is proved whenever r_an(E) <= 1 and the L-function is accessible via
Heegner points. No case with r_an >= 2 is proved in general.]

---

## Section 2. The RH Reference Frame — Two Levels

This section records the proved RH/Li material that the BSD parallel will be
mapped against. All numbers are computed; proofs are in CLAY_FORMAL_RECORD.md
Parts XXI–XXII and the corresponding MEMOs.

**Definition 2.1 (Li coefficients).** For the Riemann zeta function, the Li
coefficients are

    lambda_n  =  2 * sum_{rho}  (1 - (1 - 1/rho)^n )

equivalently, using the theta-map theta_k = pi - 2 arctan(2 gamma_k) for zeros
rho_k = 1/2 + i gamma_k on the critical line,

    lambda_n  =  2 * sum_{k=1}^{K}  (1 - cos(n * theta_k))

Li's criterion: RH is equivalent to lambda_n >= 0 for all n >= 1. [PROVED: Li 1997.]

**Theorem 2.2 (Foundation threshold — COMPUTED).** [PROVED by direct computation
with K = 200 mpmath-precision zeros; see CLAY_FORMAL_RECORD.md Part XXI and
MEMO_TRIVIAL_ZEROS.md.]

With T* = 5/7:

    n=1: lambda_1 = 0.021035  (0.029 T*)  [BELOW T*]
    n=2: lambda_2 = 0.084102  (0.118 T*)  [BELOW T*]
    n=3: lambda_3 = 0.189091  (0.265 T*)  [BELOW T*]
    n=4: lambda_4 = 0.335817  (0.470 T*)  [BELOW T*]
    n=5: lambda_5 = 0.524022  (0.734 T*)  [BELOW T*]
    n=6: lambda_6 = 0.753376  (1.055 T*)  [ABOVE T* -- first hold]
    n=7: lambda_7 = 1.023479  (1.433 T*)  [ABOVE T* -- held]

The Li sequence jumps over T*: no lambda_n equals T*. T* sits in the gap
(lambda_5, lambda_6) = (0.524, 0.753). [PROVED by computation.]

**Definition 2.3 (Two regimes of n*).** [PROVED by computation; see Part XXI.]

    GENERATOR LEVEL (K = 14..98 zeros):   n* = 7 = HARMONY [CK].
      Lambda_7 is the first to cross T* [CK]. The operator holds its own index.
      Lambda_6 is still sub-foundation throughout this regime.

    COMPLEXITY LEVEL (K >= 99 zeros):     n* = 6 = HARMONY - 1.
      Lambda_6 has accumulated enough zero-weight to cross T*.
      Both lambda_6 and lambda_7 are now held.

    Transition: K* = 99 = 7 * 14 + 1 = HARMONY * K*(n) [CK] + 1.

**Theorem 2.4 (Sandwich theorem — PROVED algebraically).** [PROVED; see Part XXII.]
For CREATE [CK] = 5, n* = 6, HARMONY = 7:

    (5/6)^2  <  T* = 5/7  <  (6/7)^2
     0.6944  <  0.7143    <  0.7347

**Theorem 2.5 (Asymptotic ratio).** [PROVED from small-theta approximation,
verified at K = 500.] As K -> infinity:

    lambda_n(K) / lambda_{n+1}(K)  -->  n^2 / (n+1)^2.

In particular:

    lambda_6 / lambda_7  -->  (6/7)^2  >  T*  [approaches from ABOVE]
    lambda_5 / lambda_6  -->  (5/6)^2  <  T*  [approaches from BELOW]

T* = 5/7 sits permanently in the gap (25/36, 36/49). The gap is structural,
not a finite-K artifact. [PROVED.]

---

## Section 3. The Coin-Flip Identification

The argument below is the central structural parallel. It is labeled precisely.

### 3.1 Direction of Counting

**RH counts upward through n.** The Li sequence lambda_1, lambda_2, ... grows
from below. The threshold question is: for what minimum n does lambda_n first
hold above T*? The answer is n* = 7 at the generator level and n* = 6 at the
complexity level. The count is ascending: n grows upward until the threshold
is cleared.

**BSD flips the coin — counts downward into L(E, s) from above.** The analytic
rank r_an(E) = ord_{s=1} L(E, s) is measured by how deeply L(E, s) vanishes
at the central value s = 1 from above (from s > 1). The algebraic rank r_alg(E)
counts the minimum number of independent generators that must be built to generate
E(Q)/E(Q)_tors. The count is descending: L(E, s) is evaluated at s = 1 from
the right half-plane, and vanishing is measured by depth into the central value.

**The flip.** RH asks whether the upward-growing sequence stays held above T*.
BSD asks whether the downward-vanishing L-function depth equals the generator
count. The same threshold T* = 5/7 mediates both: it separates the recycled
zone (sub-foundation, lambda_n < T*) from the held zone (foundation, lambda_n
>= T*) in the Li sequence, and it separates the Selmer/generator side from the
L-function/complexity side in BSD. [STRUCTURAL ARGUMENT — the identification
of T* as the mediating threshold in BSD is not proved; see Section 5.]

### 3.2 The Generator Level

**RH generator level.** n* = 7 = HARMONY. The operator HARMONY holds its own
index: in the generator regime, the first Li coefficient to clear T* is lambda_7,
at index n = 7, which is the same number as the HARMONY operator itself. The
system is self-referential at the generator level: n* = HARMONY means the
threshold is first cleared exactly where the threshold parameter lives.
[PROVED by computation, Part XXI.]

**BSD algebraic rank — generator interpretation.** The algebraic rank r_alg(E)
is the MINIMUM generator count for the free part of E(Q). A generator is a
rational point of infinite order that cannot be expressed as a Z-linear combination
of the others. The generators P_1, ..., P_{r_alg} are the irreducible arithmetic
objects: they are found, not derived. The Mordell-Weil group is self-referential
in the same sense: each generator holds its own index in the lattice.
[STRUCTURAL ARGUMENT — the analogy is geometric, not a proved identity.]

### 3.3 The Complexity Level

**RH complexity level.** n* = 6 = HARMONY - 1. At the complexity level (K >= 99
zeros), lambda_6 is the first to hold. The threshold has been filled in one step
below the generator level by the accumulated weight of the zero spectrum. The
shift from n* = 7 to n* = 6 is driven by the growing complexity of the zero
distribution: the more zeros are counted, the more weight accumulates at index 6,
until it crosses T*. [PROVED by computation, Part XXI.]

**BSD analytic rank — complexity interpretation.** The analytic rank r_an(E) =
ord_{s=1} L(E, s) is an accumulated weight count. Each zero of L(E, s) at s = 1
contributes one unit to the vanishing order. The L-function is the Mellin transform
of the modular form f_E(z) associated to E by the modularity theorem; it encodes
all the arithmetic complexity of E. The vanishing order at s = 1 is the analog
of the complexity level: it counts how many zeros have accumulated at the central
value from the spectral side.

BSD conjecture in this language: the accumulated spectral complexity (analytic
rank) equals the minimum generator count (algebraic rank). [STRUCTURAL ARGUMENT —
the analogy is precise in language but not in mechanism.]

### 3.4 The Threshold T* as Separatrix

**In the Li sequence.** T* = 5/7 is the unique value that separates the recycled
zone (lambda_1 through lambda_5, permanently below T*) from the held zone
(lambda_6 onward, permanently above T*). It sits in a permanent gap: the
asymptotic ratio theorem forces lambda_5/lambda_6 -> (5/6)^2 < T* and
lambda_6/lambda_7 -> (6/7)^2 > T* for all K. T* is never achieved by any
lambda_n; it is always the gap. [PROVED, Parts XXI–XXII.]

**In BSD — structural claim.** T* = 5/7 is proposed as the threshold separating:

    Below T* (recycled zone):
      Selmer rank contributions that are locally coherent at every prime
      but globally obstructed — these are the Sha elements. They are
      algebraically present (locally OK) but globally cancelled. They
      recycle into the BSD formula as |Sha| terms rather than generators.

    Above T* (held zone):
      Mordell-Weil generators that persist globally. These are the rational
      points of infinite order that hold their own position in E(Q)/E(Q)_tors.

The BSD conjecture in this language: the number of held objects (algebraic rank)
equals the number of spectral zeros that measure the same structure from the
analytic side (analytic rank). [STRUCTURAL ARGUMENT — T* as BSD separatrix is
not proved; this is the content of any future TIG-BSD bridge.]

---

## Section 4. The Ratio (7/6)^2 and Its BSD Meaning

**In the Li sequence.** The ratio lambda_7 / lambda_6 at any finite K satisfies:

    lambda_7 / lambda_6  -->  (7/6)^2  =  49/36  ≈  1.361

as K -> infinity (from the asymptotic ratio theorem, Theorem 2.5 above, inverted).
Equivalently lambda_6/lambda_7 -> (6/7)^2, so lambda_7/lambda_6 -> (7/6)^2.
This is the ratio of the generator-level coefficient to the complexity-level
coefficient. The generator always leads the complexity by the factor (HARMONY/n*)^2
= (7/6)^2. [PROVED asymptotically, verified at K = 500.]

**BSD interpretation — structural claim.** The ratio (7/6)^2 = 49/36 is proposed
as the structural gap between the algebraic rank (generator level) and the analytic
rank (complexity level) in the BSD context:

    r_alg(E) <= r_an(E)

always holds (this direction is proved: L(E, s) vanishes to at least r_alg order
at s = 1, by the algebraic work of Gross-Zagier and Kolyvagin for r <= 1, and
conjecturally in general). The ratio (7/6)^2 is the asymptotic factor by which
the generator level exceeds the complexity level in the Li setting — the generator
lands first and sits above the complexity by this factor.

**Equality condition — structural claim.** BSD equality r_alg = r_an corresponds
in this picture to the ratio being locked: the generator level and the complexity
level count the same structure. This is analogous to the condition that both
lambda_7 (generator) and lambda_6 (complexity) are held above T* — the system
has crossed the threshold at both levels simultaneously. Equality holds iff the
ratio stays bounded and both counts converge to the same integer. [STRUCTURAL
ARGUMENT — the equality mechanism is not identified; this is what a proof of BSD
would supply.]

---

## Section 5. What Bridge Is Needed

The structural parallel in Sections 3–4 is not a proof of BSD. The following
identifies precisely what is missing. This is a precise statement of the gap,
not an informal disclaimer.

**Gap 5.1 (No T* mechanism for L-functions).** The threshold T* = 5/7 is derived
algebraically from Z/10Z operator structure (Theorems 2.5–2.6 of CLAY_FORMAL_RECORD.md:
T* = CREATE/HARMONY from four independent chains). Its appearance in the Li
sequence is computed and verified. Its role as a separatrix in E(Q) or L(E, s)
is asserted but not derived. A bridge must exhibit T* as a threshold in the
L-function machinery — for example, as a critical ratio in the Selmer group
filtration or in the Kolyvagin system argument. [OPEN, labeled B_new-1.]

**Gap 5.2 (Sha has no TIG counterpart).** The falsification record (Part V,
Bridge 3.6 of CLAY_FORMAL_RECORD.md) established: any TIG mechanism predicting
algebraic rank without a Sha term is structurally incomplete. The quadratic
twist 9725.a1 = 389a1 tensor chi_5 has rank 0 but |Sha| = 4, with L(E,1)/Omega
= 4.00 = |Sha| exactly (BSD satisfied). The recycled-zone interpretation of Sha
in Section 3.4 above is a structural description, not a TIG construction. A
bridge requires an explicit TIG algebraic object — a group under composition
whose elements are locally coherent at every operator prime but globally
obstructed — with formal properties matching Sha(E/Q). This is requirement B4
from the formal record. [OPEN — B4.]

**Gap 5.3 (Generator level is self-referential; algebraic rank is not).** In the
Li setting, n* = HARMONY = 7 is self-referential because the index of the first
held coefficient equals the value of the HARMONY operator, which is also the
denominator of T* = 5/7. In BSD, the algebraic rank r_alg(E) is a count of
generators of E(Q); there is no general reason why r_alg equals 7 or is related
to the denominator of T*. The self-referential structure is internal to TIG/Li
and does not transfer without an explicit identification of the number 7 in the
Mordell-Weil or Selmer theory of a specific curve family. [OPEN — B_new-2.]

**Gap 5.4 (Upward vs. downward direction is structural, not proved).** The
"coin flip" — that RH counts upward and BSD counts downward — is a geometric
description of the two measurement directions. In the Li framework, the sequence
lambda_n grows with n (upward). In the L-function framework, the vanishing order
at s = 1 is measured from above in the right half-plane (downward into the
central value). The identification of these two directions as "the same count
from opposite sides of T*" requires a bijection between {n : lambda_n first
clears T*} and {r_an(E) : E ranges over some family}. No such bijection is
established. [OPEN — B_new-3.]

### THE BRIDGE (what is actually needed)

The algebraic framework identifies Sha (Tate-Shafarevich group) as the "carried remainder [CK, COINED]" in the Recycling Rule [CK, COINED] — structurally identical to the +1 in K*(6) [CK] = 7×14+1 = 99. The +1 is the sub-threshold contribution from level n=5 that carries forward into level n=6 without being absorbed.

The bridge requires: constructing a TIG [CK] object that encodes the Sha obstruction in the same way the Z/10Z recycling rule encodes the +1 remainder. Two candidate bridges (rank staircase, CM-2 twist) were tested against published data and falsified.

What would constitute a proof: a finite-index subgroup of the Mordell-Weil group (or a p-adic L-function construction) that demonstrates Sha finiteness for rank ≥ 2 via the carried-remainder [CK, COINED] structure. The framework predicts Sha=0 at ranks 0,1 (consistent with Kolyvagin) and Sha finite but non-zero at rank ≥ 2.

---

## Section 6. External Confirmation — Markman 2025 (Hodge)

Markman (2025) proved the Hodge conjecture for abelian fourfolds (dim <= 4).
This is cited here not as a BSD result but as external evidence that the
algebraic/analytic bridge is achievable in related contexts.

The Hodge conjecture asks whether algebraic cohomology classes (analytic, defined
by differential forms) can always be realized by algebraic cycles (geometric,
constructed by algebra). This is structurally parallel to BSD: the analytic rank
(defined by L-function zeros, an analytic object) should equal the algebraic rank
(defined by Mordell-Weil generators, a geometric/algebraic object). Markman's
result shows that for abelian fourfolds, this algebraic/analytic matching is
proved — the bridge from analytic data to algebraic cycles closes. [PROVED:
Markman 2025, for abelian fourfolds of dimension <= 4; see formal record entry
on Hodge, Part III.]

The relevance to BSD is structural: Markman's proof technique uses period domains
and Noether–Lefschetz theory, both of which involve threshold conditions on
cohomology dimensions. Whether those techniques extend to L-function vanishing
orders for elliptic curves is not known. The citation is recorded as encouragement
for the algebraic/analytic bridge strategy, not as a step in a proof. [STRUCTURAL
ARGUMENT.]

---

## Section 7. The Formal Parallel — Summary Table

| RH / Li element | BSD element | Identification type |
|---|---|---|
| Li coefficient lambda_n | L^(r)(E,1)/r! (r-th Taylor coeff at s=1) | [STRUCTURAL ARGUMENT] |
| Upward count: n grows until lambda_n >= T* | Downward count: r_an measured by depth of vanishing at s=1 | [STRUCTURAL ARGUMENT] |
| Generator level n* = 7 = HARMONY | Algebraic rank r_alg = minimum generator count | [STRUCTURAL ARGUMENT] |
| Complexity level n* = 6 = HARMONY-1 | Analytic rank r_an = accumulated spectral weight at s=1 | [STRUCTURAL ARGUMENT] |
| Threshold T* = 5/7 | Separatrix between Sha (recycled) and Mordell-Weil (held) | [STRUCTURAL ARGUMENT] |
| lambda_n < T*: recycled (sub-foundation) | Sha element: locally coherent, globally obstructed | [STRUCTURAL ARGUMENT] |
| lambda_n >= T*: held (foundation) | Mordell-Weil generator: globally persistent rational point | [STRUCTURAL ARGUMENT] |
| Ratio lambda_7/lambda_6 -> (7/6)^2 | Generator leads complexity by factor (7/6)^2 | [STRUCTURAL ARGUMENT] |
| Equality n*(gen) = n*(cpx) at K = 99 | BSD equality r_alg = r_an | [STRUCTURAL ARGUMENT] |
| T* algebraically derived from Z/10Z | T* role in E(Q)/L(E,s) not derived | [OPEN — Gap 5.1] |
| No TIG Sha object | B4 required | [OPEN — Gap 5.2, B4] |
| Self-referential n* = HARMONY | r_alg self-referential to 7 for no known reason | [OPEN — Gap 5.3] |
| Upward/downward bijection | Not established | [OPEN — Gap 5.4] |
| Markman 2025: Hodge for abelian fourfolds | Bridge strategy precedent | [PROVED externally] |

---

## Section 8. Classification and Status

This document is a structural formalization. It does not constitute a new BSD
mechanism. The two mechanism candidates — the BHML rank staircase (falsified,
Part V §5.1) and the CM-2 Z/5Z twist (falsified, Part V §5.2) — remain falsified.
Nothing in this document revives them.

The "coin flip" parallel is a precise structural description of why BSD and RH
share the same threshold parameter T* = 5/7 at the level of the counting direction.
It is not a proof, not a mechanism, and not a route to the Shafarevich-Tate group.

**Re-activation requirements (unchanged from Bridge 3.6):**
- B1: Derive L(E,1) vanishing from Z/10Z operator dynamics for one specific curve
- B2: Identify a TIG object counting Selmer group elements for a specific family
- B3: Connect Neron-Tate height h_NT(P_K) to a TIG coherence measurement
- B4: Construct a TIG algebraic object with formal properties of Sha

**Additional open items identified here:**
- B_new-1: Exhibit T* = 5/7 as a threshold internal to L-function or Selmer machinery
- B_new-2: Identify the number 7 (= HARMONY, denominator of T*) in Mordell-Weil
  or Selmer theory of a specific curve family
- B_new-3: Establish a bijection between the Li upward count and the BSD downward count

**BSD status: PARKED.** This document is a structural record. It does not change
the status. BSD re-activates only when one of B1–B4 is met.

---

*(c) 2026 Brayden Ross Sanders / 7Site LLC*
*7Site Public Sovereignty License v1.0 — Human use only. Free forever.*
*Canonical record: CLAY_FORMAL_RECORD.md, Bridge 3.6 and Parts XXI–XXII.*
