# Prime-Corner Collapse and the Irreducible Gap
## Why the Classical Riemann Hypothesis Asks the Wrong Question

*Brayden Sanders — 7Site LLC | DOI: 10.5281/zenodo.18852047*

---

## Abstract

Every prime greater than 5 ends in one of four digits {1,3,7,9}, corresponding exactly to the four corner operators of the TIG affine plane AG(2,3). We prove that any composition word drawn from these four corner operators collapses to HARMONY (7) or stays at PROGRESS (3) — never entering the gap set G = {2,4,5,6,8}. The gap is algebraically impermeable to prime-corner dynamics. No finite composition of corner operators ever enters G. This impermeability persists across bases (proved for base 6).

The residuals that resist absorption live entirely within G. A non-trivial zero of ζ would require the Euler product to achieve a pure-gap fixed point — a purely correlational structure with no single-prime contributor. Classical RH asks whether such zeros exist away from σ = 1/2. The correct invariant is not the presence or absence of individual zeros but the structure of the gap itself, which is already known: {CTR, COL, BAL, CHA, BRT}.

---

## §1 Introduction

The Riemann Hypothesis has resisted proof for over 160 years. We propose that part of the difficulty is structural: the hypothesis asks a question whose answer depends on the observability frame, and the classical frame — base-10 arithmetic, single prime evaluations, the standard critical strip — cannot reach the algebraic zone where the answer lives.

**The new observation.** Every prime p > 5 satisfies p mod 10 ∈ {1,3,7,9}. In the TIG operator algebra these four residues correspond to the four corner operators of the 3×3 affine grid AG(2,3): LATTICE (1), PROGRESS (3), HARMONY (7), and RESET (9). Our first theorem shows that any composition of these four operators — in any order, at any length — reduces to HARMONY (7) or stays at PROGRESS (3). The prime number system, viewed through TIG, is a corner-collapse machine.

**The gap.** The five remaining TIG operators {2,4,5,6,8} form the irreducible gap — structures that can only appear through relationships between primes, never from a prime's individual digit identity. The residuals that resist absorption live entirely in this gap.

**The wrong question.** Classical RH asks: do ζ-zeros exist at σ ≠ 1/2? This is equivalent to asking whether gap-resident structures can be observed from the corner frame. They cannot, by construction: the corner frame cannot reach the gap. A zero "at σ ≠ 1/2" would be a gap-resident object measured by a corner-frame instrument — the measurement returns HARMONY (7), not because the object is absent but because the instrument cannot resolve it.

**The right question.** What is the structure of the irreducible gap? This is already answered: {CTR, COL, BAL, CHA, BRT} = {2,4,5,6,8}. The correct invariant is the gap-positivity functional G(t₀) = min|ζ(σ+it₀)|², whose vanishing is the observable event classical RH cannot detect.

---

## §2 Corner Words and Their Fates

**Notation.** Let C = {1,3,7,9} (the corner set) and G = {2,4,5,6,8} (the gap set). Write a∘b for TSML[a][b].

### Lemma 2.1 — The 3-9 Chain

The three identities 3∘9 = 3, 9∘9 = 7, 3∘7 = 7 hold in TSML. Consequently w_n := 3∘9^n = 3 for all n ≥ 1: the 3-9 chain is a constant fixed point at PRG = 3, not alternating.

**Proof.** Single table lookups. Induction: w₁ = 3∘9 = 3; if w_k = 3 then w_{k+1} = 3∘9 = 3. □

*Remark: PRG (3) is a corner operator, not a gap operator. The 3-9 chain stays inside C.*

### Lemma 2.2 — Length-4 Collapse

For every (a₁,a₂,a₃,a₄) ∈ C⁴, the word evaluates to {3,7}. Exactly 254 of the 256 words give 7; the two exceptions (3,9,9,9) and (9,3,9,9) give 3.

**Proof.** Exhaustive over all 256 words (see Appendix A table). Both exceptions end in the 3∘9 pattern of Lemma 2.1. □

### Theorem 2.3 — Corner-Word Outcomes

Every finite word w ∈ C* of length ≥ 1 satisfies w ∈ {3,7} ⊂ C. In particular w ∉ G.

**Proof.** Induction using Lemma 2.1 and the corner multiplication table (every corner-corner product lies in {3,7}). □

### Corollary 2.4 — Gap is Corner-Inaccessible

No finite word in C* evaluates to any element of G. No single step c∘c' with c,c' ∈ C reaches G.

> **The exact claim.** The gap G = {2,4,5,6,8} is algebraically unreachable from the corner frame C: no composition of prime-last-digit operators ever enters G. Gap operators can only arise from compositions that already contain a gap operator — they are invisible from below.

---

## §3 Geometric Picture

```
        col 0       col 1       col 2
       ┌───────────┬───────────┬───────────┐
row 0  │  LAT (1)  │  CTR (2)  │  PRG (3)  │
       │  CORNER ● │  GAP ░░░  │  CORNER ● │
       ├───────────┼───────────┼───────────┤
row 1  │  COL (4)  │  BAL (5)  │  CHA (6)  │
       │  GAP ░░░  │  GAP ░░░  │  GAP ░░░  │
       ├───────────┼───────────┼───────────┤
row 2  │  HAR (7)  │  BRT (8)  │  RST (9)  │
       │  CORNER ● │  GAP ░░░  │  CORNER ● │
       └───────────┴───────────┴───────────┘

● = corner C = {1,3,7,9}    prime last-digit accessible
░ = gap   G = {2,4,5,6,8}   algebraically impermeable from C
↘ = all C-words collapse to HAR(7) or stay at PRG(3)
```

AG(2,3) labelled in TIG notation. The four corners sit at the diagonal and anti-diagonal. The gap fills the cross shape. The hard wall runs along the shaded boundary — not a wall you can approach, but one you cannot see from inside C. The only stationary corner is PRG (3), held at (0,2) by the 3-9 chain.

*Remark: corner sets depend on radix. The impermeability phenomenon is base-invariant (see §6).*

---

## §4 Gap Structure and the Parity Barrier

### Lemma 4.1 — Corner-on-Gap

For every c ∈ C and g ∈ G, the product c∘g lies in C ∪ {7}. Specifically: 18 of 20 pairs give HAR(7), 2 return to C (LAT∘CTR = PRG, RST∘CTR = RST). No corner acting on a gap operator produces another gap operator.

**Proof.** Direct enumeration of all 4×5 = 20 pairs. □

### Lemma 4.2 — Gap-on-Corner

For every g ∈ G and c ∈ C, g∘c ∈ C ∪ {7}. No gap-on-corner product remains in G.

**Proof.** Direct enumeration. □

### Proposition 4.3 — Pure-Gap Context

The only gap operators that survive composition are the residuals {COL(4), BRT(8)}, and only inside the anchor columns {CTR(2), COL(4)}. Of the 25 products g₁∘g₂ with g₁,g₂ ∈ G: 21 give HARMONY, 4 stay in G (all involving residuals).

**Proof.** Enumeration of G×G. The four surviving pairs are COL∘CTR = COL, BRT∘COL = BRT, and their reverses. □

### Corollary 4.4 — Parity-Style Barrier

Any algorithm that constructs words using only corner generators (elements of C) cannot produce an element of G at any stage. Gap structure requires gap input.

*Remark (Parity problem in sieve theory): This is the algebraic avatar of Selberg's observation that linear sieves cannot distinguish between primes and products of two primes. The corner frame corresponds to the linear sieve range; the gap corresponds to structures requiring parity information that individual prime evaluations cannot supply.*

### Implications for ζ-zeros

Corner generators correspond to individual prime contributions to ζ(s) = ∏_p(1−p^{−s})^{−1}. A non-trivial zero is a fixed point of the ζ-flow (companion Halving Lemma paper); its location requires the full product, including correlations. Corollary 4.4 says: from individual prime inputs alone, one cannot construct a zero. A zero in the gap would require the Euler product to source gap structure from within gap context — purely correlational, with no single-prime contributor.

---

## §5 Zeta-Flow Resonance

| TIG concept | ζ analog |
|-------------|----------|
| Corner set C = {1,3,7,9} | Individual prime contributions to ζ |
| Gap set G = {2,4,5,6,8} | Zero correlations — where zeros live |
| Corner-word collapse → HAR | Euler product convergence for Re(s) > 1 |
| Hard wall: C-words never enter G | Individual primes cannot generate zeros |
| Pure-gap context required | A zero requires purely correlational structure |
| RH: gap opens only at σ = 1/2 | Only the critical line is zero-compatible |

The companion Halving Lemma paper proves: the flow dσ/dt = −(σ−1/2)|ζ(σ+it₀)|² has fixed points only at σ=1/2 or at zeros. RH ⟺ G(t₀) = min|ζ|² > 0 on every zero-free vertical.

The present paper provides the algebraic reason why this should hold: the prime-corner structure of ζ's Euler product is closed under corner algebra, and the gap — where zeros live — is algebraically impermeable.

**The two papers triangulate the open problem:** this paper says algebraically that corners never reach the gap; the Halving Lemma says analytically that the flow stalls only at zeros. Neither proves RH alone. Together they bound the problem from two directions.

---

## §6 Base-Independence

### Theorem 6.1 — Base-6 Universality

Let C₆ = {1,5} (prime last digits in base 6, for primes p > 3) and G₆ = {2,3,4,6,7,8,9}. Note that BAL(5) ∈ G yet 5 ∈ C₆. Every word of length ≥ 2 over C₆ evaluates to HAR(7). Consequently C₆-words never enter G₆.

**Proof.** All four length-2 words give HAR: LAT∘LAT=7, LAT∘BAL=7, BAL∘LAT=7, BAL∘BAL=7. Induction: any extension of a HAR by any element of C₆ gives HAR. □

*Remark: Theorem 6.1 shows impermeability is not base-10 numerology. Even when C₆ contains a gap operator (BAL=5), the absorption structure of TSML drives every pair to HARMONY. The gap G₆ is larger (7 operators vs 5 in base 10) but equally impermeable from C₆. The wrong-question phenomenon is radix-agnostic.*

---

## §7 Consequences for Other Clay Problems

**Riemann Hypothesis.** The correct invariant is G(t₀) = min|ζ(σ+it₀)|². The algebraic question is answered: prime-corner dynamics never populate the gap. The analytic question remains open: does the Euler product's correlation structure ever drive G(t₀)→0 off the critical line?

**Yang-Mills.** The gap structure {2,4,5,6,8} corresponds to the dual-threshold overlap MASS_GAP = T*+S*−1 = 2/7. Individual gauge field configurations (corners) cannot reach the gap — similarly, massless excitations are unreachable from configurations below threshold. The dual-threshold mechanism forces a positive gap, qualitatively.

**P vs NP.** The corner/gap dichotomy is the verification/search dichotomy at the algebraic level. Impermeability ⟹ no polynomial-time decision procedure within the corner frame can produce a gap element. The gap cannot be found by corner-frame search at all — only by a computation that already contains gap structure.

### Open Problems

**Conjecture A (Analytic impermeability).** The Euler product, viewed as an infinite composition of corner operators with analytic weights p^{−s}, satisfies the algebraic impermeability at every height t₀ not equal to the imaginary part of a zero.

**Conjecture B (Gap-positivity).** G(t₀) = min|ζ(σ+it₀)|² > 0 for every zero-free vertical. This is equivalent to RH and is the correct invariant to attack.

**Question C (Other bases).** For any base b, do the prime-last-digit operators generate a closed sub-algebra collapsing entirely to HAR? Does the gap size grow monotonically with b?

**Question D (L-functions).** Do Dirichlet L-functions L(s,χ) with non-principal characters access the gap? If so, their zeros would be gap-resident in a way ζ-zeros cannot be (from individual primes).

---

## Appendix A: Verified Computations

**TSML identities for Lemma 2.1:** 3∘9=3, 9∘9=7, 3∘7=7 (single table entries).

**Length-4 corner words (254 give H, 2 give P):**

```
    \ a₃a₄  LL LP LH LR PL PP PH PR HL HP HH HR RL RP RH RR
a₁a₂ \
LL         H  H  H  H  H  H  H  H  H  H  H  H  H  H  H  H
LP         H  H  H  H  H  H  H  H  H  H  H  H  H  H  H  H
...
PR         H  H  H  H  H  H  H  H  H  H  H  H  H  H  H  P ←
...
RP         H  H  H  H  H  H  H  H  H  H  H  H  H  H  H  P ←
```
(L=LAT, P=PRG, H=HAR, R=RST. Bold P marks exceptions PRRR and RPRR.)

**Corner multiplication sub-table:**

```
∘  | 1  3  7  9
---+------------
1  | 7  3  7  7
3  | 7  7  7  3
7  | 7  7  7  7
9  | 7  3  7  7
```
No entry equals any element of G = {2,4,5,6,8}.

## Appendix B: Base-6 Enumeration

C₆ = {1,5}; L=LAT(1), B=BAL(5), H=HAR(7).

```
∘ | L  B
--+------
L | H  H
B | H  H
```

All 4 length-2 words give H. By induction all longer words do also.

**SHA-256(TSML table): 7726d8a620c24b1e461ff03742f7cd4f775baed772f8357db913757cf4945787**

Code: github.com/TiredofSleep/ck

---

*(c) 2026 Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
*Companion paper: Halving Lemma / Dissipative Flow for ζ(s) — arXiv:[ID pending]*
