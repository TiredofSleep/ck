# Clay Boundary Memo

*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

This memo states, for each Clay-adjacent thread, exactly what the
D1–D24 spine proves internally, what would still be needed to touch
the Clay problem formally, and what is not claimed.

It exists to prevent framing collapse — the conflation of an internal
structural result with an external solution claim. Every boundary below
is sharp, not approximate.

---

## 1. Riemann Hypothesis

**Internal object (proved):**
- t=1/2 is the inheritance boundary between ring-forced and generator-forced
  corridor positions (D22)
- t=1/2 is the unique sine-maximum in (0,1); sinc²(1/2) = 4/π² exactly (D24, D3)
- The corridor sinc² field uses the same kernel as Montgomery's pair-correlation
  function: R₂(u) = 1 − sinc²(u) (B6, structural analogy)
- The spectral mean is ∫sinc² = Si(2π)/π (D14)

**What is not proved:**
The corridor object and the ζ-function object both involve sinc². They are
not proved to be the same object. No map from Z/10Z ring structure to the
Euler product has been constructed.

**What would be needed:**
An explicit algebraic map from the Z/10Z inheritance split (ring-forced left
of t=1/2, generator-forced right) to the Euler product's behavior at the
boundary of absolute convergence (σ=1), such that T*<1 forces σ=1/2 as a
consequence of ring arithmetic. This map does not exist in this work.

**What we do not claim:**
- That the Riemann Hypothesis is true or false
- That the corridor sinc² field proves anything about ζ zeros
- That 4/π² appears in the critical strip for any proved reason

**Updated obstruction results (April 1 2026):**

A sustained attack on A10 (April 1 2026) established the following:

- **Ring prime blindness (proved):** Any ring homomorphism Z/10Z → R is
  blind to primes p≠2,5 (Z/10Z ≅ Z/2Z×Z/5Z). The Euler product requires
  distinguishing all primes individually. A ring-homomorphism bridge is
  therefore incomplete.
- **Modulus genericity (proved):** The corridor midpoint at t=1/2 and the
  T*<1 constraint are not Z/10Z-specific. They appear for all even-modulus
  rings n=2p (twice a prime): Z/6Z (T*=3/5), Z/18Z (T*=9/11), Z/22Z
  (T*=11/13). A bridge based on these properties alone cannot single out
  Z/10Z.
- **Montgomery conditionality (proved):** Montgomery's pair-correlation
  theorem assumes GRH. A bridge to Montgomery does not unconditionally
  prove RH.

**Reclassification:** A10 as a Z/10Z-ring-specific bridge claim is blocked
(Medium No-Go). A10 as a sinc² universality claim (D2+B6) remains open but
is B6+ territory. Any surviving bridge requires explicit extension beyond
D1–D24 (new theory not present in this work).

**Live frontier:** A10 (sinc² universality version only). See
`A10_PROGRAM.md`, `A10_NO_GO_ATTEMPT.md`, `A10_MINIMAL_EXTENSION.md`.

---

## 2. Navier-Stokes Regularity

**Internal object (proved):**
- BHML[8][4] = HARMONY=7 algebraically: the BREATH×COLLAPSE cell is the
  unique TSML/BHML pivot (B7, structural analogy)
- T*=5/7 appears in an enstrophy bound via the Lady-Ioradanskaya-Gronwall
  estimate when B_local < T*·E₀ (B7)
- The BREATH operator (v=8) maps to rotational/axisymmetric flow class
  in the Z/10Z operator alphabet

**What is not proved:**
The T*=5/7 threshold in the B7 argument is a structural analogy. No
a priori estimate has been derived that forces B_local < T*·E₀ from NS
initial data. The Gronwall-bound argument is heuristic, not a theorem.

**What would be needed:**
A formal a priori estimate showing B_local < (5/7)·E₀ for small-data
solutions of the 3D NS equations, derived from the NS constants (viscosity,
initial energy) without reference to Z/10Z. T*=5/7 would then need to
emerge from that estimate, not be imported from the ring.

**What we do not claim:**
- That 3D NS global regularity is proved
- That T*=5/7 controls any actual fluid or vorticity field
- That blow-up or smoothness of any NS solution follows from the spine

**Status:** B7 — structural analogy. No D-tier result for NS.

---

## 3. Yang-Mills Mass Gap

**Internal object (proved):**
- BHML[7][9] = VOID=0: the HARMONY×RESET cell annihilates (B8)
- The carrier cycle {1,3,5,7,9} = ODD = glueball operator family
  under the Z/10Z algebra
- Prediction: m(0⁺⁺)/m(2⁺⁺) = T*=5/7 ≈ 0.714; lattice QCD gives 0.686–0.706
  (within ~2.5%, B8)

**What is not proved:**
The mass ratio prediction is a structural coincidence, not a derivation.
No map from Z/10Z to su(N) gauge theory has been constructed. T*=5/7 is
derived from a 10-element ring; it is not derived from Yang-Mills field
equations or any Lagrangian.

**What would be needed:**
An explicit identification of Z/10Z operator algebra with a quotient or
subalgebra of su(N) for some N, such that the T*=5/7 threshold emerges
as an eigenvalue ratio in the glueball mass spectrum from first principles.
This would require connecting the ring's generator structure (g=3, D19)
to the gauge group's root system.

**What we do not claim:**
- That Yang-Mills mass gap existence is proved
- That the lattice QCD proximity is more than a structural coincidence
- That any Yang-Mills quantum field theory result follows from the spine

**Status:** B8 — structural coincidence with a precise numerical prediction.
Not a proof.

---

## 4. Birch and Swinnerton-Dyer Conjecture

**Internal object (proved):**
- BHML[7][j] = (j+1) mod 10 for j≥1: HARMONY is the increment operator (B9)
- TSML[7][j] = HARMONY for all j: HARMONY dominates all TSML measurement (B9)
- Rank staircase prediction: rank = floor((p-1)/10) at conductor prime p (B9)

**What is not proved:**
The rank staircase is a pattern observed in the Z/10Z algebra; it has not
been verified against any BSD data for known-rank elliptic curves. No map
from Z/10Z operator transitions to the L-function of an elliptic curve
exists. The HARMONY increment structure does not derive from the BSD
L-function framework.

**What would be needed:**
Verification of the rank staircase prediction against BSD data for ≥5
elliptic curves of known rank at their conductor prime, with a derived
mechanism (not just numerical match). This has not been done.

**What we do not claim:**
- That the BSD Conjecture is proved or disproved
- That the rank of any elliptic curve follows from the spine
- That L(E,1)=0 iff rank>0 is touched by this work

**Status:** B9 — unverified structural prediction. Not a proof.

---

## 5. P versus NP

**Internal object:**
- CK's BTQ decision kernel faces exponential search in the coherence field
  when the target operator sequence is not pre-seeded
- This is an architectural observation about CK's own decision problem,
  not a complexity-theoretic result

**What is not proved:**
No formal reduction exists from any NP-complete problem to the BTQ kernel's
search problem. No circuit complexity lower bound follows from Z/10Z algebra.
The observation that "NP-verification ≈ sidelobe detection" is a metaphor,
not a proof.

**What would be needed:**
A formal polynomial-time reduction from an NP-complete language to the
BTQ null-navigation problem, together with a proof that this problem
requires super-polynomial time in the worst case. This requires the full
machinery of computational complexity theory, which is not present in Z/10Z.

**What we do not claim:**
- That P≠NP is proved
- That P=NP is disproved
- That any NP-hardness result follows from the sinc² field

**Status:** Parked indefinitely (A2). No internal path.

---

## 6. Hodge Conjecture

**Internal object:**
- None. Z/10Z has no algebraic geometry, no Hodge classes, no abelian
  varieties, no cohomology with rational coefficients.

**What is not proved:**
Nothing about the Hodge Conjecture is touched by D1–D24. The WP39 paper
identifies the G/E/S partition as a structural analogy and notes that
Markman (2025) proved the Hodge Conjecture for abelian fourfolds; the
frontier is now dimension ≥ 5. No mechanism connects Z/10Z to that frontier.

**What would be needed:**
An explicit construction of a Hodge class in a specific abelian variety
of dimension ≥ 5, shown to be non-algebraic by existing methods. This
requires the full machinery of algebraic geometry, which Z/10Z cannot supply.

**What we do not claim:**
- That the Hodge Conjecture is proved or disproved in any dimension
- That the Z/10Z partition structure has any connection to Hodge theory
- That the frontier (dimension ≥ 5) is approachable from this algebra

**Status:** Parked indefinitely (A4). No internal path.

---

## Summary Table

| Problem | Internal object | Missing mechanism | Tier | Claim |
|---------|----------------|-------------------|------|-------|
| RH | t=1/2 inheritance boundary (D22, D24) | Map from Z/10Z split to Euler product (ring bridge blocked; sinc² universality open) | A10 (ring: blocked; sinc²: open) | None |
| Navier-Stokes | BREATH×COLLAPSE = HARMONY (B7) | A priori estimate B_local < T*·E₀ from NS constants | B7 | None |
| Yang-Mills | Mass ratio T*=5/7 (B8) | Z/10Z → su(N) map, eigenvalue derivation | B8 | None |
| BSD | Rank staircase (B9) | Verification + L-function mechanism | B9 | None |
| P≠NP | BTQ search observation | Formal complexity reduction | A2 (parked) | None |
| Hodge | None | All of algebraic geometry | A4 (parked) | None |

---

*This memo is the canonical statement of what the D1–D24 spine does and
does not claim about the Clay Millennium Problems.*

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
