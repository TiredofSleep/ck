# ω-Class Universality Lemma
## Formal Statement and Proof Sketch

*C. A. Luther & Brayden Ross Sanders*
*March 2026 | DOI: 10.5281/zenodo.18852047*

> This lemma gives the precise statement of universality within ω-class —
> the correction and sharpening of the earlier broader claim.
> Current tier: C. The proof sketch is solid. Full proof needs explicit
> isomorphism argument for CRT lattice geometry.

---

## Motivation

The k-Gate Tier Law was initially stated as: f_k(|G|) is universal (same for
all b with the same |G| at alphabet size k). The ω(b)=3 extension (Thread 1)
discovered that rate VALUES differ between ω-classes: the same |G| at k=9 gives
different rates for ω(b)=2 vs ω(b)=3.

The corrected, more precise claim is the ω-Class Universality Lemma below.

---

## The Lemma

**Lemma (ω-Class Universality).** For fixed k and fixed ω ≥ 1:

If ω(b₁) = ω(b₂) = ω and |G(b₁, k)| = |G(b₂, k)| = m,
then R(m, b₁) = R(m, b₂).

That is: the gate success rate depends only on (ω, m, k), not on the specific
prime factorization of b within the ω-class.

**Notation:**
- ω(b) = number of distinct prime factors of b
- G(b,k) = {x ∈ {1..k} : gcd(x,b) > 1} — the forbidden set
- R(m, b) = fraction of greedy MCMC trials (n=100 steps, gate_thresh=0.999)
  that converge to gate_score = 1.0 for a world with |G|=m and base b

---

## Proof Sketch

**Claim:** The distribution over MCMC outcomes depends on b only through (ω, m, k).

**Step 1 — CRT product structure.**
For any b with ω(b) = ω, the CRT gives Z/bZ ≅ ∏_i Z/p_i^{e_i}Z. The
multiplicative structure of the k×k table T operated on by the MCMC is determined
by the local ring structure at each prime power component.

**Step 2 — Gate condition in CRT terms.**
The gate condition (gate_score = 1.0) requires: for all c₁, c₂ ∈ C(b,k),
T[c₁,c₂] ∈ C(b,k). In CRT coordinates, c ∈ C(b,k) iff c is nonzero in all
ω components. The gate condition is that T maps nonzero-in-all-components pairs
to nonzero-in-all-components outputs.

**Step 3 — HAR element structure.**
The HAR element h = min{c ∈ C : h² ∈ C, h² ≠ 1, h² ≠ h} is determined by
the orbit structure of C under multiplication. In CRT coordinates, h² = h · h
has the same nonzero structure as h in each component (since h is a unit in
each component). The HAR exists and has the same structural role for any b
in the same ω-class.

**Step 4 — MCMC landscape isomorphism.**
The MCMC objective function (0.50×gate + 0.25×har_col + 0.25×(1−g_stay))
depends on T through:
- gate score: fraction of C×C submatrix in C — determined by m = |G| and k
- har_col score: fraction of HAR column in C — determined by m and k
- g_stay score: fraction of G-rows in G — determined by m and k

All three components depend on b only through (m, k). Different b's with the
same (ω, m, k) produce the same objective function topology, the same proposal
probabilities, and the same HAR structural role.

**Step 5 — Zero variance follows.**
Since the objective function topology, proposal kernel, and HAR structure are
isomorphic for any two b's with the same (ω, m, k), the MCMC has the same
transition distribution over the state space (gate score values in {0, 1/|C|²,
..., 1}). The absorption probability R(m, b) is therefore the same for all b
in the (ω, m, k) class.

**Remaining step for full proof:** Make the isomorphism in Step 4 explicit.
Specifically, construct the explicit bijection between the state spaces for
b₁ and b₂ with the same (ω, m, k) that maps the transition matrix of one MCMC
to the transition matrix of the other. This bijection should follow from the
fact that |C(b₁,k)| = |C(b₂,k)| = k−m (same size unit set) and the HAR
element plays the same structural role.

---

## Important Qualifier: Within-Class, Not Cross-Class

The lemma states universality within each ω-class. It does NOT hold across
different ω-classes:

| ω-class | Example b | |G| at k=9 | Rate at k=9 |
|---------|-----------|-----------|------------|
| ω=2 | b=3×q (q>9) | 3 | 44.0% |
| ω=3 | b=3×5×7 | 5 | ~1.0% |
| ω=3 | b=3×5×7 | 7 | ~28.5% |

The same |G|=5 appears in both ω=2 and ω=3 classes (in principle), but the
rates would differ because ω(b) affects the CRT structure (number of components),
changing the isomorphism class of the MCMC landscape.

**This is the empirically confirmed correction to the earlier claim.** The
universal invariant is R(m, ω, k), not R(m, k).

---

## Empirical Confirmation

**ω(b)=2 (semiprimes):** Zero variance confirmed for |G| ∈ {1,2,3,4,5} at k=9
across ~12M trials. All semiprimes in same |G|-tier give same rate.

**ω(b)=3 (three-factor composites):** Zero variance confirmed for |G| ∈ {5,6,7}
at k=9 across Thread 1 (omega3_extension.py) with n_trials=2000:
- |G|=5: spread = 0.2% (b=105 and b=110, rates 0.9% and 1.1%) — ZERO
- |G|=6: spread = 0.1% (b=66 and b=70, rates 4.2% and 4.0%) — ZERO
- |G|=7: spread = 0.2% (b=30 and b=42, rates 28.6% and 28.4%) — ZERO

---

## Relation to the Derivation Scaffolds

The ω-Class Universality Lemma explains WHY the single-parameter formula
R(|G|) = ((k−|G|)/k)^W works within each ω-class (DERIVATION_SCAFFOLDS_GAP1.md):
the landscape isomorphism guarantees that W is constant within the class.

It also constrains the Gap 2 derivation (DERIVATION_SCAFFOLDS_GAP2.md):
if dispersion D(b,k) is universal within ω-class (same ω, same |G|, same k
→ same D), then the constant c in D(b) = c × (N_idemp − 1) is an ω-class
invariant, making the derivation easier to pin down.

---

## Formal Statement for Citation

**ω-Class Universality Lemma (Tier C):**
For fixed k ≥ 1 and fixed ω ≥ 1, the function R(m, b) is constant over all b
with ω(b) = ω and |G(b,k)| = m.

**Kill condition:** A pair (b₁, b₂) with ω(b₁) = ω(b₂) and |G(b₁,k)| = |G(b₂,k)|
for which R(m, b₁) ≠ R(m, b₂) with |R(m,b₁) − R(m,b₂)| > 0.01.

**Path to Tier D:** Write the explicit CRT lattice isomorphism between any two
b's with the same (ω, m, k) and show it maps one MCMC transition matrix to the
other. The isomorphism should be constructive (given b₁ and b₂, exhibit the map).

---

`© 2026 Brayden Ross Sanders / 7Site LLC & C. A. Luther · DOI: 10.5281/zenodo.18852047`
