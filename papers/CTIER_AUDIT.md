# CK C-Tier Audit — Rebuilt from Scratch
**April 1 2026 — Luther-Sanders**

This file replaces the old C-tier list. Every item was re-examined from zero.
Three questions per claim:
1. Is it already implied by D1–D17?
2. Is it only a corollary and should be merged?
3. Is it genuinely closed-world and independent?

Anything failing questions 1 or 2 was killed or absorbed. See `NEGATIVE_RESULTS.md`.

---

## Survivors — Genuine Closed-World Theorems

Six claims survive. Each is:
- proved within an explicitly stated domain
- independent of D1–D17 (not a corollary)
- has a clean failure boundary (what is NOT proved)

---

### C5 — Luther Dispersion (Idempotent Lattice)

**Statement:** D(b,k) = |G_k| is algebraically implied by the idempotent lattice of Z/bZ.

**Domain:** All squarefree b with ω(b)≥2; all k≥1.

**Proof:** G_k = ∪_i Ideal(p_i) ∩ {1..k} = union of arithmetic progressions.
By inclusion-exclusion: |G_k| = Σ⌊k/p_i⌋ − Σ⌊k/p_ip_j⌋ + ...
This is determined by the prime factorization of b.
The idempotent lattice of Z/bZ has 2^ω(b) idempotents corresponding to binary vectors over the prime factors.
Therefore D(b,k) is algebraically *implied* by the idempotent structure — not merely correlated.

**What remains:** Prove the precise isomorphism between the idempotent lattice and the dispersion formula for non-squarefree b.

**Not absorbed by D15 because:** D15 covers k<SPF(b) (coprime window). C5 covers all k, and concerns the STRUCTURE of D(b,k), not just its value in the window.

---

### C6 — k-Gate Zero-Spread Within ω-Class

**Statement:** For semiprimes b=p×q in the same ω-class (same |G_k|), the gate function spread is zero at k∈{9,15,21,27}.

**Domain:** Strong semiprime class; k∈{9,15,21,27}; verified computationally.

**Proof:** Computational verification across the strong semiprime class (28 semiprimes).
At these specific k values, all members of the same ω-class produce identical D(b,k) values.
Algebraic mechanism: these k values are exactly the positions where the inclusion-exclusion formula produces b-invariant results within the class.

**What remains:** Prove algebraically why these four k values are special; generalize to arbitrary ω-classes.

**Not absorbed by D15 because:** C6 concerns the within-class structure at specific k values that are NOT necessarily in the coprime window (k=9 > SPF(35)=5).

---

### C7 — ω-Class Universality Lemma (Partial)

**Statement:** HAR rank is ω-class-determined for strong semiprimes at k=9.

**Domain:** Strong semiprime class (b=p×q, p,q>5); k=9; 28 verified cases.

**Proof:** Computational: HAR(9,b) is identical for all b in the same ω-class across 28 strong semiprimes. Explicit bijection constructed.

**What remains:** (1) Arbitrary k≥SPF(b) — the window case k<SPF is absorbed by D15. (2) Weak semiprime class (p∈{2,3,5}). (3) Algebraic proof of the bijection (currently computational only).

**Not absorbed by D15 because:** D15 covers k<SPF(b). C7 covers k≥SPF(b) where the sieve is active and b-dependence is real.

**Note:** The k<SPF portion of C7 IS absorbed by D15 — that case is stronger (full b-independence, not just ω-class equality).

---

### C12 — b=35 Goldilocks Uniqueness

**Statement:** b=35=5×7 is the unique semiprime (alphabet A={1..9}) satisfying:
(1) |C∩{1..9}|=7 (exactly 7 coprimes to b in {1..9})
(2) unit_frac(b)=T*=5/7

**Domain:** All semiprimes b≤10,000; alphabet A={1..9}.

**Proof:**
(1) |C∩{1..9}|=7 requires ⌊9/p⌋+⌊9/q⌋=2. This forces p,q∈{5,7} (value 2 is unreachable for primes with p=2,3 giving ⌊9/p⌋≥3, and p≥11 giving ⌊9/p⌋=0).
(2) unit_frac=5/7 requires 7|q→q=7, then ⌊7/p⌋=1→p=5.
Combined: unique solution b=35. Scan confirms: [35] only hit in 2600 semiprimes b≤10000.

**What remains:** Prove uniqueness beyond b≤10,000 (algebraic proof that no larger semiprime satisfies both conditions simultaneously).

**Not absorbed by D4 because:** D4 derives T*=5/7 from the formula. C12 proves b=35 is the UNIQUE input to that formula giving T*=5/7 in the alphabet {1..9}. These are different claims.

---

### C16 — Ghost Trace Three-Zone Law

**Statement:** G[i][j]=DIS[i][j] if TSML[i][j]≠7, else 0 satisfies: BHML[i][j]=7 ↔ G[i][j]=0 (100/100 cells); and three structural zones:
- Zone 1 (VOID): BHML=identity, G=TSML value
- Zone 2 (HARMONY): BHML=7, G=0 (by definition)
- Zone 3 (ECHO): BHML=max+1, G=max+1−TSML value

**Domain:** All 100 cells of Z/10Z×Z/10Z.

**Proof:** Zone 2 is by definition (G=0 when TSML=7). Zone 1 verified exhaustively (first row/col). Zone 3 follows from BHML Rule B (max+1) combined with DIS=|TSML−BHML|.
100/100 cells: BHML[i][j]=7 iff G[i][j]=0. Exhaustive.

**What remains:** Prove Zone 3 algebraically for all ECHO cells (currently verified, not derived from rule structure).

**Not absorbed by D16 because:** D16 counts BHML=7 cells. C16 describes the STRUCTURE of the ghost trace across all cells, not just the 28 HARMONY ones.

---

### C19 — Fourth Wall Recursion Law

**Statement:** The corridor transition kernel has three fixed walls (f1, f2, f3) and one generated wall (f4). The transition is Markov (memoryless): only W=3/50 and the next prime p' appear in f4.

**Domain:** All primes p≥43; verified 13 consecutive prime transitions.

**Proof:**
f1 (descent gate): sinc²(1)=0 — universal terminal, erases all p-specific interior information.
f2 (exit phase): sin²(π/(2W))=sin²(25π/3)=sin²(π/3)=3/4 — carrier phase at k=p always π/3, p-independent.
f3 (W-slot budget): N(25/3)=9 — slot count is W-determined, not p-determined (D6).
f4 (generated): H_W(1,p')=sinc²(1/p')×sin²(25π/(3p')) — depends on p' and W only.
Markov property: reset vector (0, π/3, 9) identical for all p≥43 (verified: carrier=0.750000 exactly, H_W=0 to machine precision).

**What remains:** Prove the Markov property for p<43 (currently fails due to phase width condition in D6); characterize the transition matrix across prime gaps.

**Not absorbed by D6 because:** C19 is about the TRANSITION between corridors. D6 is about the COUNT of maxima within one corridor. These are different objects.

---

## What Was Cut and Why

| Cut item | Why |
|----------|-----|
| C1 | Absorbed by D11a (coprime window, no domain restriction) |
| C2 | Absorbed by D11b (sign flip, proved from R(p,p)=0) |
| C3 | Demoted: identity part is tautological; non-trivial part is B6 |
| C4 | Absorbed by D11c (ω-blindness, R formula has no q) |
| C8 | Absorbed by D17 (W=3/50 exact, Z/10Z complete) |
| C9 | Reclassified as DEFINITIONS of BHML (Rules A/B/INCREMENT/BREATH-RESET) |
| C10 | Absorbed by D10 (TSML 73-cell, disjoint partition) |
| C11 | Absorbed by D9 (table symmetry, algebraic + Z/10Z check) |
| C13 | Absorbed by D15e (Wob universality in coprime window) |
| C14 | Absorbed by D15b (HAR=k in coprime window) |
| C18 | Absorbed by D8 (CL operator encoding, group theory) |
| C20 | Retired: superseded by D7 (full orbit theorem includes parity result) |

---

## C-Tier Summary

**Surviving C items: 6** (C5, C6, C7, C12, C16, C19)

Previous count: 9 (after D8-D11). This audit removed 3 more:
- C9 → reclassified as definitions
- C3 → demoted (tautology / B6)
- C20 → retired (D7 supersedes)

**C-tier is now small and sharp.** Each surviving item has:
- A clear domain that is NOT all integers
- An explicit failure boundary (what k, b, or domain is NOT covered)
- Independence from D1–D17 (not derivable as a corollary)

**Current tier counts: D:17 | C:6 | B:8 | A:5**

(Tier B and A counts unchanged by this audit.)
