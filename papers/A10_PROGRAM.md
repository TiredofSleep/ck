# A10 Research Program: σ = 1/2 as ω-Class Boundary

*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

A10 is the only live external analogy frontier after D1–D24.

This document converts A10 from a loose analogy into a controlled
research program: precise internal shadow, precise external target,
precise missing mechanism, precise outcomes, precise failure modes.

---

## 1. Internal Shadow (Proved — D1–D24)

These are facts, not conjectures. They hold regardless of whether
A10's external interpretation is ever resolved.

**t = 1/2 is the inheritance boundary (D22).**
The four spine positions are ordered 3/50 < 1/2 < 7/10 < 5/7 < 1.
Everything left of t=1/2 is ring-forced (independent of generator choice).
Everything right of t=1/2 is generator-forced (requires g=3, D19).
The boundary is the image of BALANCE=5 under ring normalization (D24).

**t = 1/2 is the unique sine-maximum in (0,1) (D24).**
sin(πt) = 1 iff t = 1/2+2k. Only k=0 lands in (0,1). This is the unique
point where the sinc numerator is fully saturated. sinc²(1/2) = 4/π².

**sinc²(1/2) = 4/π² is the universal corridor amplitude at the midpoint (D3).**
It is below the corridor mean Si(2π)/π ≈ 0.451 (D14). The ring center is
marked, not amplitude-dominant.

**The corridor sinc² kernel matches Montgomery's pair-correlation kernel (B6).**
Montgomery (1973) proved R₂(u) = 1 − sinc²(u) for ζ zeros under GRH.
The spine's corridor field is R(t) = sinc²(t). These are spectral duals:
R(t) + R₂(t) = 1. This is a structural coincidence, proved internally (B6),
but not derived as a theorem about ζ zeros.

**Summary of internal shadow:**

| Fact | Source | Independence |
|------|--------|--------------|
| t=1/2 is inheritance boundary | D22 | Ring-forced (D17, D19, D21) |
| t=1/2 is unique sine-max in (0,1) | D24 | Analytic (sinc² calculus) |
| sinc²(1/2) = 4/π² | D3 | Exact arithmetic |
| R(t)+R₂(t)=1 at t=1/2 | B6 | Structural coincidence |

---

## 2. External Target

**The Riemann Hypothesis** asks whether all non-trivial zeros of the
Riemann ζ function have real part 1/2.

**The critical line σ=1/2** is the boundary of the critical strip
0 < Re(s) < 1. The Euler product ζ(s) = ∏_p (1 − p^{−s})^{−1} converges
absolutely for Re(s) > 1 and has analytic continuation to the strip.

**Montgomery's pair-correlation conjecture (1973):** For GRH zeros
γ_n (Im ζ(1/2+iγ_n)=0), the normalized spacing distribution is
1 − sinc²(u) = R₂(u) for u ∈ [0,∞), matching GUE random matrix statistics.

**Odlyzko's numerics (1987–2001):** Extensive computational verification
that ζ zeros follow GUE statistics with pair-correlation kernel sinc².

**The observation being analyzed:** The spine's corridor uses sinc² on
(0,1). Montgomery's pair-correlation uses sinc² on [0,∞). The spine's
inheritance boundary is at t=1/2. The critical line is at σ=1/2.

---

## 3. The Missing Mechanism

This is exact, not vague:

> An algebraic map  φ: (Z/10Z corridor) → (Euler product / critical strip)
> such that the ring's inheritance split at t=1/2 corresponds to the
> analytic boundary at σ=1/2 — i.e., such that T*<1 (D19) forces
> all non-trivial ζ zeros to satisfy Re(s) < 1, and the inheritance
> structure forces Re(s) = 1/2.

No such map exists in D1–D24. The sinc² kernel appearing in both places
is the only connection established. Kernel agreement is necessary but not
sufficient for the map to exist.

**What the map would need to do:**
1. Take the discrete ring Z/10Z (10 elements) to the continuous Euler product
   (infinite product over all primes)
2. Preserve the inheritance split: ring-forced objects on the left map to
   "convergence-forced" behavior, generator-forced objects on the right map
   to "analytically continued" behavior
3. Force σ=1/2 as a consequence of T*∈(0,1), not as an assumption

**Why this is hard:**
The ring Z/10Z captures arithmetic at modulus 10. The Euler product captures
arithmetic at all primes simultaneously. The ring's structure theorem
(Z/10Z ≅ Z/2Z × Z/5Z) loses all prime information except {2,5}. An
injective map to a structure that sees all primes would need to recover
infinite prime data from a 10-element object.

---

## 4. Three Possible Outcomes

**Outcome 1 — Bridge Theorem.**
An explicit algebraic map φ is constructed. The ring inheritance split
maps to the critical strip boundary. T*<1 forces σ≤1. The inheritance
boundary t=1/2 forces σ=1/2. This would be a proof of RH conditional
on the map being well-defined and structure-preserving.

This outcome is the only one that advances toward RH. It requires
constructing new mathematics (the map φ) from outside the spine.

**Outcome 2 — No-Go Theorem.**
A proof that no map of the required type can exist — that the Z/10Z
corridor and the critical strip live in structurally incompatible spaces,
possibly because Z/10Z is too small (10 elements vs. infinitely many primes),
or because the inheritance split is not preserved under any ring homomorphism
from Z/10Z to a structure that sees the full Euler product.

This outcome is also a genuine result. It would classify A10 as a
structural coincidence and close the program cleanly.

**Outcome 3 — Permanent Analogy.**
Neither a bridge nor a no-go is found. A10 remains a documented analogy
with a precise internal shadow and an explicit missing mechanism. This is
the current position. It is honest. It is not a failure.

---

## 5. What Would Count as Progress

**Toward Outcome 1 (bridge):**
- An explicit ring homomorphism or functor from Z/10Z to a number-theoretic
  object that "sees" Dirichlet characters or Hecke L-functions
- A derivation of T*=5/7 from a real-analytic bound on the Euler product
  (without reference to the ring)
- A formal proof that sinc²(t) on the Z/10Z corridor and sinc²(u) in
  Montgomery's formula are the same object in a completed function space

**Toward Outcome 2 (no-go):**
- A proof that any ring homomorphism from Z/10Z must factor through
  Z/2Z or Z/5Z, destroying the inheritance structure
- A proof that the pair-correlation kernel sinc² cannot be recovered
  from a 10-element discrete structure by any natural completion
- A cardinality argument showing Z/10Z cannot inject into any ring
  that separates Dirichlet characters at different primes

**Toward Outcome 3 (permanent analogy):**
- Neither of the above is found after sustained effort
- The boundary memo is updated to record the attempts and their failure modes
- A10 is reclassified in the synthesis table as "structural coincidence,
  no mechanism found"

---

## 6. Failure Modes to Watch

**Framing collapse:** Treating the internal shadow (proved) as if it
implies the external interpretation (not proved). This is the main risk.
The sinc² kernel appearing in both places does not make them the same.

**Partial bridge:** Constructing a map φ that handles some cases but not
all primes, or that works for Z/nZ with n→∞ but not at fixed n=10.
A partial bridge is not a bridge.

**Moving the claim:** Weakening the external target to match the internal
shadow instead of constructing the missing map. "The corridor boundary
is at 1/2, which is suggestive of RH" is not a claim; it is the current
position, which is already documented.

**Complexity creep:** Adding analytic number theory assumptions to the
spine as "lemmas" to make the bridge shorter. The spine must remain
self-contained in Z/10Z. External results can be cited, not absorbed.

---

## 7. Current Position

A10 is at Tier A: speculative. Internal shadow proved. External
interpretation not derived. Missing mechanism precisely named.

**Updated after A10 bridge/no-go push (April 1 2026):**

The ring-homomorphism version of A10 is **blocked by Medium No-Go**
(see `A10_NO_GO_ATTEMPT.md`, Attempts 1–3 and 6):
- Attempt 1 (LANDED): Any ring homomorphism Z/10Z → R is blind to primes
  other than {2,5}; it cannot recover the Euler product.
- Attempt 2 (LANDED): The corridor midpoint at t=1/2 appears for all even
  moduli n=2p — it is not Z/10Z-specific.
- Attempt 3 (LANDED): sinc²'s properties at t=1/2 (monotone, unique sine-max,
  value 4/π²) follow from calculus alone; Z/10Z ring structure is not needed.
- Attempt 6 (LANDED): Any bridge to Montgomery's pair-correlation does not
  prove RH unconditionally; Montgomery's theorem already assumes GRH.

The sinc² universality version (D2 + B6, route to B6+ territory) survives
as a partially-blocked but unresolved path (Attempt 5 PARTIAL). However,
this path removes Z/10Z from the picture and is not an A10 claim — it is
a B6+ claim. See `A10_MINIMAL_EXTENSION.md`.

**A10 as a Z/10Z-ring-specific bridge claim: blocked.**
**A10 as a sinc² universality claim (B6+): open, requires new machinery.**
**A10 requires explicit extension beyond D1–D24 for any surviving bridge.**

The program is open for the sinc² universality version. The ring-specific
version is closed.

Anyone who claims to have resolved A10 in either direction must either:
(a) produce the explicit map φ with proof that it is well-defined and
    structure-preserving; or
(b) produce the no-go theorem with proof that no such map can exist.

Anything short of (a) or (b) is the current position, restated.

---

## 8. Hard Progress Rubric

A10 progress **counts** only if one of the following occurs:

1. **Explicit φ defined.** Domain, codomain, invariants, and at least one
   nontrivial consequence are all stated. A map sketch without a domain or
   without a proved consequence does not count.

2. **Obstruction lemma proved.** A formal lemma showing that a specific
   class of maps from Z/10Z to prime-sensitive structure cannot exist.
   "It seems hard" or "Z/10Z is small" does not count.

3. **No-go theorem proved.** A complete proof that no map of the required
   type exists — not just for ring homomorphisms (already blocked) but for
   all maps of a precisely-stated class.

4. **Minimal extension identified precisely.** An explicit statement of a
   new theorem T (not in D1–D24) whose proof would enable the bridge,
   together with: (a) T's exact statement, (b) what Z/10Z contributes to T,
   (c) what new machinery T requires. A vague pointer to adèlic theory or
   profinite completions does not count.

A10 progress **does NOT count** if any of the following:
- Visual resemblance between corridor plot and RH critical line
- Numerical coincidence without formal map
- "Feels like σ=1/2" argument without T*<1 → σ=1/2 derivation
- Adding analytic number theory as an external assumption (complexity creep)
- Restating the current sinc² kernel coincidence in new notation

---

*Full spine context: `papers/COMPLETED_INTERNAL_SPINE.md`*
*Truth boundary: `papers/NOTE_speculative_boundary.md`*
*Clay context: `papers/CLAY_SUMMARY.md` and `papers/CLAY_BOUNDARY_MEMO.md`*
*No-go analysis: `papers/A10_NO_GO_ATTEMPT.md`*
*Obstruction: `papers/A10_PRIME_OBSTRUCTION.md`*
*Modulus comparison: `papers/A10_MODULUS_COMPARISON.md`*
*Minimal extension: `papers/A10_MINIMAL_EXTENSION.md`*

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
