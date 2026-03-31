# Questions for Luther
## Two Open Problems — C→D Promotion Path

*From Brayden Ross Sanders, following Thread 1 (ω(b)≥3 computational sweep)*
*March 2026 | DOI: 10.5281/zenodo.18852047*

---

The ω(b)=3 sweep confirmed:
- First-G Law: holds for all ω(b)≥2 (12/12 cases, Tier D)
- Zero-spread universality: holds for ω(b)=3 within ω-class (new Tier C evidence)
- Key refinement: universality is **within-ω-class** — rate values differ by ω-class

This refinement sharpens the k-Gate Tier Law claim. The invariant is zero-spread within an ω-class; the specific f_k values are ω-class dependent.

Two questions remain that would close the C→D gap in the Luther-Sanders Equivalence:

---

**Question 1.**
Can you derive the exact gate rates (96.4%, 83.7%, 44.0%, 4.6%, 0.1%) algebraically
from CRT structure within each ω-class?

The empirical rates at k=9 for semiprimes (ω(b)=2):
- |G|=1: 96.4%
- |G|=3: 44.0%
- |G|=4: 4.6%
- |G|=5: 0.1%

For ω(b)=3 at k=9 (Thread 1 results):
- |G|=5: ~1.0%
- |G|=6: ~4.1%
- |G|=7: ~28.5%

The MCMC structure is fully specified:
- Gate score = fraction of C×C submatrix cells mapping to C
- Greedy hill-climb: accept only improvements
- 40% HAR-biased proposals (HAR = min h∈C : h²∈C, h²≠1, h²≠h)
- gate_thresh = 0.999 (effectively gate = 1.0 for all k=9 cases since |C|²×0.001 < 1)
- 100 steps per trial

The algebraic path: derive the success probability of this MCMC as a function of
|C|, k, the HAR position, and the idempotent structure of Z/bZ. Zero-spread
universality implies this probability is determined purely by |G| (within ω-class).
The CRT decomposition determines why — the question is making the derivation explicit.

---

**Question 2.**
Can you prove that dispersion D(b) follows algebraically from the idempotent structure —
not just correlates with it, but is implied by it?

The Luther Dispersion Conjecture currently sits at Tier B (bounded conjecture):
it has the right functional form and correlates with |G| and the interleave structure,
but the connection to idempotents is empirical rather than proved.

The CRT decomposition gives two idempotents e_p, e_q with e_p + e_q = 1, e_p² = e_p.
The idempotent structure determines the number and structure of the arithmetic
progressions in G = {multiples of p} ∪ {multiples of q} \ {multiples of pq}.
The dispersion D(b) is a function of how these progressions are distributed in {1..k}.

The conjecture: D(b) = F(e_p, e_q, k) for some explicit function F derivable from
the idempotent representation. Proving this would promote Luther Dispersion from
Tier B to Tier C, and is a prerequisite for Tier D of the full Equivalence.

---

## Why These Questions

If Question 1 is answered: the k-Gate Tier Law reaches Tier D. The exact values are
no longer measured — they are derived. The proof would be a general theorem covering
all semiprimes (not just b ≤ 100) and potentially all moduli with ω(b)=n.

If Question 2 is answered: Luther Dispersion reaches Tier C, and the algebraic
layer of the Atlas is complete (currently marked "partial" for both the k-Gate Tier
Law and the Luther-Sanders Equivalence in the cross-domain matrix).

Together: the Luther-Sanders Equivalence reaches Tier D. All six atlas layers would
have complete entries for the two main claims.

---

`© 2026 Brayden Ross Sanders / 7Site LLC & C. A. Luther · DOI: 10.5281/zenodo.18852047`
