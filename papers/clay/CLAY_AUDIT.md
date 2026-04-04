# CK Clay Series — Precision Audit
## Three Layers Per Problem: Proved / Structural / Belief

*Brayden Ross Sanders / 7SiTe LLC · April 2026*
*This document is the honest reading of WP36–WP42. It names the smoke and keeps the signal.*

---

> The belief system is in `CK_BELIEF_SYSTEM.md`. The proofs are in `papers/proof_*.py`.
> This document sits between them: it audits what the Clay papers actually establish
> versus what they assert with insufficient backing.

---

## How to Read This

Each Clay paper has three layers:

- **Layer 1 — What's proved**: Results with verified proof files or citations to known theorems. These stand regardless of CK.
- **Layer 2 — What's structural**: The geometric/algebraic correspondence being claimed. This is the real CK contribution — naming where each problem lives in the coherence field. It is not a proof; it is a precise map.
- **Layer 3 — What we believe**: The full speculation, stated without hedging. See `CK_BELIEF_SYSTEM.md`.

**Smoke** is language that sounds like Layer 2 but is actually just Layer 1 restated in CK notation. It adds no new content. It is labelled below so the reader can skip it.

---

## WP37 — P vs NP

### Layer 1 — Proved
- First-G event at exactly k = p: proved algebraically, verified 36,662 semiprimes, zero exceptions.
- sinc²(k/p) closed form with exact zeros at k = p: verified across all tested primes.
- Non-associativity rate 49.8% of BHML triples (498/1000): exact table computation. (TSML rate is 12.8% — the DoF claim uses BHML, the physics table.)
- T* = 5/7 algebraic identity: proved (D7, D18c).

### Layer 2 — The Structural Claim (real, not smoke)
**2-SAT is polynomial because 2-variable clause resolution stays in the associative subalgebra of BHML. 3-SAT is NP-complete because 3-variable clause resolution requires the full non-associative BHML algebra, and the non-associative dimension cannot be reduced to the associative subalgebra.**

**Precision note (April 2026):** The associative subalgebra of **TSML** (the harmony/measurement table used in the SAT encoding) is A = {HARMONY(7)} — a single element. The associative subalgebra of **BHML** (the physics table) is A = {VOID(0)} — the identity element. The DoF ladder {4,6,7,10} refers to degrees of freedom in the operator space, not the size of the associative subalgebra. 2-SAT resolution collapses to HARMONY via absorption; 3-SAT unit propagation creates chains through BECOMING/COLLAPSE that exit A = {7}.

This is the CK contribution: a structural reason WHY the P/NP boundary sits at clause width 3. The encoding of SAT into the CL non-associativity framework is stated but the formal reduction (proving SAT requires the 7th DoF) remains open. Until that reduction is proved, this is a precise structural conjecture, not a proof sketch.

**The non-circular anchor:** `sinc²(0.1) ≈ 0.9675` is the same at p = 5 and p = 2^512. The signal does not degrade with scale. The road to the null is `0.9p` steps long at every scale. There is no shortcut geometry in the sinc² field — every path to the null traverses the full corridor. P ≠ NP is the claim that the corridor has no shortcut. This is structural, not circular: it says WHY (corridor geometry forces traversal), not just THAT (P ≠ NP is hard).

### Smoke to Ignore
- "NP-verification is sidelobe detection; P-solving is null navigation" — this just renames the P/NP problem in TIG notation. It does not add content.
- "RSA is hard because the road is long" — true but circular: we said P ≠ NP is hard because the road is long, and P ≠ NP is the claim that the road is long. Needs the structural geometry to escape circularity.
- Barrier evasion claims (relativization, natural proofs, algebrization) — asserted, not derived.

### Layer 3 — Belief
P ≠ NP is physically forced. The sinc² field has no shortcut geometry. The corridor length is the prime. You cannot arrive at a prime without having traversed its corridor. This is what P ≠ NP is.

---

## WP38 — Navier-Stokes Regularity

### Layer 1 — Proved
- TSML[BREATH][COLLAPSE] = BREATH: exact table lookup (trivially true by table definition).
- Zero-width gate at k = p: proved and verified.
- BREATH criterion absolute bound: B_local ≤ 2/7 (derivation from T* = 5/7 algebraic floor).
- All standard NS references (Caffarelli-Kohn-Nirenberg, Grujić UVA work) are correctly cited.

### Layer 2 — The Structural Claim (real, not smoke)
**The TIG prediction: B_local ≤ 2/7 is the regularity threshold, and the gap to close is C ≤ 3.74 in the Gagliardo-Nirenberg interpolation inequality. This is not derived from NS dynamics — it is a prediction from the algebraic coherence floor. If rigorous NS analysis can close that gap (C ≤ 3.74), the TIG threshold and the NS regularity criterion would agree.**

The precise open problem: Can sharp Gagliardo-Nirenberg bounds prove C ≤ 3.74? The current best constant in the interpolation is larger. Grujić's geometric depletion approach (UVA, 2025) is the closest existing work to closing it. The TIG connection to Grujić is:
- Grujić's criterion: geometric depletion of vorticity in the direction of maximum stretching
- TIG criterion: BREATH operator survives COLLAPSE context iff B_local ≤ 2/7
- Both are saying: regularity holds when concentrated vorticity is geometrically constrained

This is a real correspondence. It names the same object from two directions. The mechanism connecting them is not proved.

### Smoke to Ignore
- "BREATH fixed point proves NS regularity" — TSML[BRT][COL] = BRT is a table lookup. It proves the operator is algebraically stable, not that NS solutions stay regular.
- The Lyapunov function argument (§8): assumes B_local is a Lyapunov function, then shows C ≤ 3.74 follows. This is the Clay problem restated, not solved.

### Layer 3 — Belief
In 3D, smooth NS solutions do not blow up. The BREATH criterion enforces this: systems cannot cross the fold threshold Δ¹ = 1/2 in finite time from smooth initial data in L². The proof will be a coherence argument.

---

## WP39 — Hodge Conjecture

### Layer 1 — Proved
- Product-Gap Theorem: C ⊗ C ⊆ C at every tensor depth (corner sub-algebra closed). Gap grows as 9^k − 4^k. Proved for k = 1..4 by direct enumeration.
- ω-Blindness Theorem: R(k, 1/p) is independent of the ring structure {p, q, r...} sharing factor p. Proved in the finite-ring setting.
- Markman (2025): Hodge conjecture for abelian fourfolds of Weil type. External result, correctly cited.
- Balance invisibility: D2 → 0 as q/p → 1. Proved algebraically.

### Layer 2 — The Structural Claim (real, not smoke)
**Markman settled dim = 4 with the Weil symmetry condition. The TIG prediction: the next obstruction appears at dim ≥ 5, and it corresponds to unbalanced prime structure (q/p > 1 significantly). The ω-Blindness theorem is the TIG model of LOCAL-GLOBAL FAILURE: each prime sees a clean signal; the global combination fails to distinguish algebraic from transcendental classes.**

The precise frontier: Markman's technique relies on the Hodge-Riemann bilinear relations in the Weil case. The TIG structural parallel: balanced semiprimes (q ≈ p) have D2 ≈ 0 (balance invisibility) — the curvature signal cannot distinguish the two components, making the algebraic structure transparent. In unbalanced cases (q >> p), D2 ≠ 0, curvature breaks symmetry, and the TIG model predicts the Hodge correspondence fails.

**The 9^k − 4^k gap growth is the sharpest structural claim**: it gives a precise exponential rate at which the unreachable zone grows with tensor depth. Whether this rate maps to the algebraic-transcendental separation in Hodge cohomology at the same rate is the open question.

### Smoke to Ignore
- "G/E/S partition mirrors the Hodge decomposition" — naming parallel structures without proof that the partition rules of one govern the other.
- "1/(p−1)² gap floor explains Hodge hardness growth" — pattern-naming. The gap floor is a TIG observation; its relevance to Hodge is asserted.

### Layer 3 — Belief
The Hodge conjecture is false in dimension ≥ 5 for non-Weil varieties. ω-Blindness is real: there are cohomology classes that are genuine projections from the ether (high-dimensional coherence field) that have no finite algebraic shadow on earth.

---

## WP40 — Riemann Hypothesis

### Layer 1 — Proved
- R(k, f) → sinc²(k/f) in the continuum limit: proved (WP35 Theorem 5).
- R(k, f) has exact zeros at k = f for all primes f tested: verified, max error 4.44×10⁻¹⁶.
- Universal constant 4/π² = sinc²(1/2): exact algebraic identity, verified computationally at all primes p = 5 to 99,991.
- Montgomery (1973): pair correlation of Riemann zeros = 1 − sinc²(u). External theorem, correctly cited.
- R(x) + R₂(x) = 1: arithmetic identity (trivially true: sinc²(x) + (1 − sinc²(x)) = 1).

### Layer 2 — The Structural Claim (real, not smoke)
**The non-trivial observation: 4/π² = sinc²(1/2) appears independently in BOTH frameworks. In TIG prime arithmetic, it is the universal mid-journey amplitude at k/p = 1/2 for ALL large primes, derived from first principles. In Montgomery, it appears as the pair correlation at half-spacing u = 1/2. These are the same constant evaluated at the same fractional position in two completely independent derivations.**

The question is whether this double appearance is a coincidence or a causal connection. The TIG claim: it is causal. The prime sinc² field and the Riemann zero sinc² field are the same field seen from two sides. The Fourier transform connecting the prime distribution to the zero distribution IS the sinc² projection. Proving this is proving RH.

**The fold threshold alignment**: Re(s) = 1/2 is the TIG fold boundary Δ¹. Zeros living on Re(s) = 1/2 would be zeros living on the fold boundary of the coherence field. If zeros can ONLY be on the fold boundary (because the sinc² field enforces it), that is RH. The mechanism: a zero off the critical line would require a sinc² null at a non-fold position, which the prime arithmetic field cannot produce (because sinc² zeros are forced to k = p, never between primes).

### Smoke to Ignore
- "R(x) + R₂(x) = 1 proves a deep connection" — this is arithmetic. Adding sinc² and its complement gives 1. It observes that two independently derived functions are complementary; it does not prove they arise from the same source.
- "Scale-invariance in both frameworks proves universality" — both following power laws doesn't prove they're the same phenomenon.
- Gram's law D1 oscillation matching — pattern-matching, not mechanism.

### Layer 3 — Belief
RH is true. The zeros are on Re(s) = 1/2 because that IS the fold boundary Δ¹ of the coherence field, and the sinc² field enforces its fold through the prime arithmetic structure. A zero off the critical line would be a prime without a corridor — impossible. The Fourier transform connecting Δ¹ to Re(s) = 1/2 is the proof that needs to be formalized.

---

## WP41 — Yang-Mills Mass Gap

### Layer 1 — Proved
- T* = 5/7 algebraic derivation: unit_frac(7, 35) = (7−2)/7 = 5/7. Proved (D7, D18c).
- First-G Law: first non-unit element at k = p. Proved, 36,662 cases.
- BHML determinant det(BHML) = 70: numerical computation.
- Pre-G zone {1, ..., p−1} is 100% coprime to b = p×q: proved (First-G Law).

### Layer 2 — The Structural Claim (real, not smoke)
**T* = 5/7 is the coherence floor. It is not a parameter — it is the algebraically forced threshold of the minimal strong semiprime. The mass gap claim: no coherent excitation can live below T* in the operator field, just as no physical state can live below the Yang-Mills mass gap Δ.**

The precise testable claim: **The BHML spectral gap |λ₆|/|λ₅| ≈ 2/7 = 1 − T* at b = 35. Does this spectral gap persist (or grow monotonically) as b ranges over all semiprimes p×q?** If yes, that is a TIG proof that the coherence floor is structurally maintained as the algebra scales — the analogue of the mass gap persisting in the infinite-volume limit.

The connection to Yang-Mills: non-Abelian gauge theory generates a mass gap because the interaction generates its own energy scale (dimensional transmutation). TIG generates T* = 5/7 because the operator algebra generates its own threshold (algebraic transmutation from the group structure of Z/10Z). These are structurally parallel instances of a system generating its own floor.

**What's not circular here:** the value 5/7 is theoretically grounded, FPGA-verified, and CK-derived independently of Yang-Mills. The claim is not "Yang-Mills has a gap because we say so" — it is "the class of systems that generate their own coherence floor includes Yang-Mills, and TIG is the finite algebraic prototype of that class."

### Smoke to Ignore
- "Wilson lattice ↔ CL composition table" — correspondence stated without proof that gauge integration produces the CL table.
- "det(BHML) > 0 implies reflection positivity" — OS2 reflection positivity is a spectral property not established by a positive determinant.
- "Primality = non-Abelianness" as a causal statement — this is structural naming, not derived.

### Layer 3 — Belief
The mass gap exists. It is Δ = T* − 1/2 = 3/14 in natural units of the operator algebra. The gap is the width of the Δ² zone. No coherent excitation lives in VOID. The minimum energy of anything in the field is the price of crossing from VOID into GAP, which is 3/14 in these units.

---

## WP42 — BSD Conjecture

### Layer 1 — Proved
- T* = 5/7 algebraic identity: proved.
- BSD rank 0 (Kolyvagin 1988) and rank 1 (Gross-Zagier + Kolyvagin): external theorems, correctly cited.
- Average rank ≤ 5/6 for elliptic curves ordered by height (Bhargava-Shankar 2015): external theorem, correctly cited.
- CRT idempotent count = 2^{ω(b)} − 2: exact combinatorial result.
- Balance invisibility (D2 → 0 at q/p → 1): proved algebraically.

### Layer 2 — The Structural Claim (real, not smoke)
**The sharpest CK claim about BSD: the numerator 5 appears in both T* = 5/7 and the Bhargava-Shankar bound average rank ≤ 5/6. TIG predicts the Goldfeld conjecture (average rank = 1/2) from the structure of T*, but the derivation gives ≈ 0.57 rather than exactly 0.5.**

This tension — TIG predicts ~0.57, Goldfeld conjectures exactly 1/2 — is the precise open question. Either:
(a) The TIG derivation has a flaw (wrong units, wrong constant), or
(b) Goldfeld's conjecture is off by a factor related to T*, or
(c) The mapping between rank transitions and TIG operator transitions introduces a correction factor of (1 − T*) = 2/7 that hasn't been derived yet

Until this gap is resolved, the BSD-TIG connection is suggestive but not tight.

**The rank-staircase correspondence is real**: each jump in algebraic rank corresponds to a discrete gate event (k = p, k = q, ...) in the unit fraction field. The BSD claim that analytic rank = algebraic rank is the claim that the L-function zeros count the same gate events as the rational point count. TIG gives a structural reason to expect this: both are counting transitions through the coherence field of the same arithmetic object.

### Smoke to Ignore
- "Rank staircase = sinc² null crossings" — this renames rank transitions in TIG language without showing they're the same count.
- "Tate-Shafarevich = ghost obstructions" — informal analogy, the structure of Ш is not elements of Z/bZ.
- "L(E,1) vanishing = sinc² null at s=1" — stated without connecting the L-function's analytic structure to the TIG field.

### Layer 3 — Belief
BSD is true for all elliptic curves over ℚ. The rank is the number of independent phase transitions the curve undergoes before it reaches HARMONY. The L-function encodes exactly the same transitions from the other side (analytic vs. geometric). They agree because they're both counting the same coherence events in the same field.

---

## Corridor-Zero Theorem: One Key Proved April 2026

*See `papers/proof_corridor_zero_paths.py` — all assertions passing.*

The BHML self-composition cascade from BEING(1) traces the exact positions k=1..8 of sinc²(k/7). The operators ARE the corridor. The path from each operator to VOID(0) via RESET annihilation classifies into four classes — and this classification maps directly to the structure of each Clay problem.

**The four classes (proved):**

| Class | Operators | Steps to VOID | sinc²(n/7) | Character |
|-------|-----------|--------------|-----------|-----------|
| A | BEING(1), DOING(2), BECOMING(3) | 3 | 0.935 / 0.759 / 0.524 — **above fold** | Must cross fold |
| B | COLLAPSE(4), CREATE(5), GAP(6) | 2 | 0.295 / 0.121 / 0.026 — below fold | No fold crossing |
| C | HARMONY(7), RESET(9) | 1 | 0.000 / sidelobe | Direct / gate |
| X | BREATH(8) | never | 0.015 (sidelobe) | **The pole** |

The fold sits between BECOMING(3) and COLLAPSE(4): sinc²(3/7)=0.5243 (above) vs sinc²(4/7)=0.2949 (below).
T* − fold = 5/7 − 1/2 = **3/14** (Class A zone width).
1 − T* = **2/7** (above-T* spectral gap, proved 946/946 semiprimes).

**Revised signal map per Clay problem:**

| Problem | Class A (non-trivial) | Class B (trivial) | Class X (pole/regular) | Open question |
|---------|----------------------|-------------------|----------------------|---------------|
| **RH** | Non-trivial zeros — must cross fold Re(s)=1/2 | Trivial zeros — already below fold, forced by Γ | — | Show fold is the ONLY suspension point |
| **P vs NP** | 3-SAT forces Class A fold-crossing (7th DoF) | 2-SAT stays Class B/C (absorbs to HARMONY) | — | Show Class A step cannot be avoided in poly time |
| **NS** | Blow-up requires entering Class A (above fold) | Regularity = stay in Class B (B_local ≤ 2/7) | BREATH = regularity itself (pole, never zeroes) | Confirm C ≤ 3.74 = cannot cross fold from Class B data |
| **YM** | Non-trivial excitation = Class A, costs ≥ 3/14 | Vacuum = Class B/X (below fold, BREATH oscillation) | BREATH = vacuum oscillation | Map 3/14 gap to dimensionful YM scale |
| **Hodge** | Transcendental classes = Class A (fold-crossing cohomology) | Algebraic classes = Class B (no fold crossing) | — | Show q/p >> 1 forces Class A classes with no algebraic representative |
| **BSD** | Each rank unit = one completed Class A path | Rank 0 curves = no Class A paths completed | — | Derive correction factor from fold boundary (1/2) to TIG prediction (0.57) |

The smoke is still the same: restating the Clay problem in TIG notation adds nothing. The signal is still the same: one field, exact constants, precise thresholds. What is new is the **mechanism**: the fold boundary is not just a location — it is the dividing line between the two path classes. The theorem doesn't prove the Clay problems. It identifies the exact algebraic step that must be formalized for each one.

---

## Summary: The Real Signal Across All Six

The smoke across all six papers is the same smoke: **restating the Clay problem in TIG notation and calling it a framing**. That is not the CK contribution.

The real CK contribution — the signal — is:

1. **A single universal constant** (4/π², T* = 5/7, sinc²(0.1) ≈ 0.9675) appears in both the prime arithmetic and the Clay problem's known structure. These constants are exact, verified, not curve-fitted.

2. **A precise threshold** (T* = 5/7, fold threshold 1/2, Class A zone width 3/14) that the paper predicts as the location of the Clay problem's difficulty. Not "things are hard" but "this specific number is where the structure lives."

3. **A proved classification** (April 2026): the four path classes A/B/C/X under BHML RESET annihilation map the trivial/non-trivial/pole structure of each problem. The fold is the dividing line. BREATH is the pole. The corridor IS the algebra.

4. **A testable next question** for each problem that would either confirm or refute the TIG structural claim. These are listed as the Layer 2 open questions above and in the signal map above.

The six problems are genuinely different. But they share the field. When you strip the smoke, what CK is saying is: **each Clay problem is hard for the same geometric reason — the fold is the only suspension point, Class A paths must cross it, and no shortcut through the corridor exists. The null is at the end of the road. The road is the variable.**

That is not circular. It is a measurement.

---

*© 2026 Brayden Ross Sanders / 7SiTe LLC*
*DOI: 10.5281/zenodo.18852047*
*This document is a precision companion to WP36–WP42. It does not replace them.*
