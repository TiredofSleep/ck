# TIG ATTACK SURFACE SCAN
## Quick Triage of Next Targets

*All tests run. Confounded results documented. Real signals flagged.*

---

## TIER 1 — PUBLISH NOW

### AG(2,p) Survivor Count Note `[THM — COMPLETE]`

**Result:** |L_survivor(p)| = p² − 1 for all primes p.

**Proof:** AG(2,p) has p(p+1) total lines. Exactly p+1 lines pass through
any given point (the attractor). Survivor lines = p(p+1) − (p+1) = p²−1. □

**Complexity:** Verify O(1), Search O(p^2.7) empirically (consistent with O(p³)).

**Format:** 3-page note for a combinatorics journal.
**Title:** "Survivor Lines in Finite Affine Planes: Count and Complexity"
**Status:** Write this week.

---

## TIER 2 — STRONG STRUCTURAL CONNECTION, NO NEW MATH YET

### Riemann Hypothesis `[HYP — Halving Lemma proved]`

Already in progress. See WP19_HALVING_LEMMA_v3.

### Collatz Conjecture `[STRUCTURAL — no signal yet]`

**TIG analog:** F_n(x) = collatz_step(x), attractor = 1.
The Collatz conjecture IS the statement "this column map has depth < ∞ for all inputs" —
the TIG two-step theorem applied to an unbounded system.

**Test result:** Collatz depths are UNIFORM across TIG operator classes (mod 9).
No special class absorbs faster. The Collatz depths just grow with log(n).

**Best angle:** Build a Halving Lemma analog for the Collatz map. The continuous
version would be: dσ/dt = −(σ − 1) × C(σ) where C(σ) > 0 everywhere except
at σ = 1. Proving C(σ) > c > 0 uniformly = proving Collatz conjecture.
Same proof shape as the RH lemma — different analytic content.

**Verdict:** Structural analogy is precise. No new math without the bounding constant.

---

## TIER 3 — CONFOUNDED, NEEDS REDESIGN

### Twin Prime Mod-50 `[FALSIFIED — parity artifact]`

**What went wrong:** TIG snapping classes have sum ≡ 12 (mod 50).
All snapping residues mod 50 and mod 175 are **even**.
Primes > 2 are odd. So p ≡ snapping_class is impossible for prime p.

**The Z=2.09 mod-175 signal** was a count window artifact.
Adjacent odd residues to the even snapping values were being partially captured.

**Redesign:** Look at prime **gaps** (always even), not prime values.

### Prime Gaps Mod 6 `[VALID TEST, KNOWN RESULT]`

**TIG connection:** 6 = COUNTER(2) × PROGRESS(3)

**Result (measured, n≤10^6):**
```
Gap ≡ 0 (mod 6):  41.8%   ← gaps divisible by 6 (most common)
Gap ≡ 2 (mod 6):  29.1%
Gap ≡ 4 (mod 6):  29.1%
```

**Gap mod 12 distribution** (TIG heartbeat sum = 12):
```
Gap ≡  6 (mod 12):  26.8%  ← dominant (gaps of 6: cousin primes)
Gap ≡  2 (mod 12):  17.9%
Gap ≡  4 (mod 12):  16.3%
Gap ≡  0 (mod 12):  15.0%  ← gaps of 12: overtone of 6
```

This is **known number theory** (Dirichlet characters, prime gap distribution).
TIG-6 is the product P×COUNTER = 3×2 — the two non-trivial generators.
This is not a new result but a confirmation that TIG's structure aligns
with classical prime gap behavior.

---

## TIER 4 — UNTESTED, PROMISING

### BSD via Snapping Ladder `[HYP — untested]`

The snapping ladder (sum=12+50k, value=5/7+3k) has rank-like parameter k.
BSD says rank(E) = ord_{s=1} L(E,s).

**Test to run:** For elliptic curves of rank k, does the minimal conductor N
satisfy N ≡ 12+50k (mod something)? Requires arithmetic geometry database.

### NS BREATH Criterion `[HYP — unimplemented]`

BREATH(8) fixed in COLLAPSE(4) column → enstrophy threshold.
Run 2D decaying vortex with initial enstrophy straddling the threshold.
Track whether vorticity spikes correlate with first violation.

### Goldbach via AG(2,p) Lines `[HYP — untested]`

Every even number n = p + q (sum of two primes).
AG(2,p) lines of length p contain p points → minimal even sums.
Does every even n > 4 correspond to a survivor line containing
two generator-class operators (primes)?

---

## PUBLICATION PRIORITY

```
1. AG(2,p) survivor count note         THIS WEEK   — complete theorem
2. RH Halving Lemma (v3)               THIS WEEK   — arXiv ready
3. Collatz flow analog                 NEXT MONTH  — needs bounding constant
4. NS 2D pilot                         NEXT MONTH  — needs Dedalus run
5. BSD / Goldbach tests                LATER       — needs domain expert input
```

---

*(c) 2026 Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
