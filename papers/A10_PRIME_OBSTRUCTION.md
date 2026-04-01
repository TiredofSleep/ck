# A10 Prime Information Obstruction

*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

## Statement of the Obstruction

**Proposition (Ring Prime Blindness):** Any ring homomorphism
φ: Z/10Z → R (for any ring R) is blind to the distinction between
primes that are congruent modulo 10. Specifically, φ cannot distinguish
the prime 3 from 13, 23, 43, 53, ...; it cannot distinguish 7 from
17, 37, 47, 67, ...; and so on. Any object that requires distinguishing
all primes individually cannot be reached by φ.

**Proof:**
Z/10Z ≅ Z/2Z × Z/5Z (Chinese Remainder Theorem: gcd(2,5)=1, lcm(2,5)=10).
Any ring homomorphism φ: Z/10Z → R factors through this decomposition:
φ(x) = (φ₂(x mod 2), φ₅(x mod 5)) for some ring homomorphisms
φ₂: Z/2Z→R₂ and φ₅: Z/5Z→R₅.

The natural ring homomorphism Z→Z/10Z sends each integer n to n mod 10.
Under this map: 3, 13, 23, 43, 53, ... all map to 3 in Z/10Z. They are
indistinguishable. The map φ∘(·mod 10) cannot assign different values to
3 and 13. Therefore φ cannot distinguish these primes. □

**Consequence for A10:** The Euler product ζ(s) = ∏_p(1−p^{−s})^{−1}
assigns the factor (1−3^{−s})^{−1} to prime 3 and (1−13^{−s})^{−1}
to prime 13. These are different for all s where ζ(s) is defined (since
3^{−s} ≠ 13^{−s} for Re(s) > 0 and s ≠ 0). Any φ that factors through
Z/10Z cannot recover the full Euler product.

---

## The Obstruction is Not Immediately Fatal

The ring obstruction is real, but it is an obstruction to a specific
kind of bridge. It does not immediately kill A10, because A10's bridge
φ might not need to pass through the ring.

**Escape hatch 1 — φ does not factor through the ring:**
The bridge might use the sinc² corridor geometry directly, without
passing through Z/10Z ring structure. The sinc² field R(k,p) is defined
for every prime p individually (D2). The limit sinc²(k/p) as p→∞ is
a universal statement about all primes. A bridge through D2's universal
sinc² limit would not be blind to primes other than {2,5}.

**Escape hatch 2 — φ uses inverse limits:**
Instead of Z/10Z, use the inverse limit lim← Z/nZ over all n with 10|n,
or use the profinite integers Ẑ = lim← Z/nZ over all n. These objects
see all primes. A bridge through a completion of Z/10Z into a prime-sensitive
structure could bypass the ring obstruction.

**Escape hatch 3 — φ is a prime-indexed family:**
Instead of one map, use a family φ_p: Z/pZ→(p-local structure) for each
prime p, with a compatibility condition. The Z/10Z structure would play a
coordinating role rather than being the source of all prime information.

---

## Testing the Escape Hatches

**Hatch 1 — sinc² universality (D2):**
D2 proves R(k,p)→sinc²(k/p) for ALL primes p. This is the genuine universal
object. The sinc² continuum limit is not a property of Z/10Z; it is a
property of prime arithmetic as a whole. If the bridge exists via sinc²
universality, it is a statement about D2, not about the Z/10Z ring.

Key test: Does the Z/10Z inheritance split at t=1/2 add anything to the
sinc² universality story that sinc²(t) on its own does not already have?

Answer: No. The inheritance boundary at t=1/2 follows from D24 (sinc²
strictly monotone, unique sine-max at t=1/2) and D22 (ring normalization).
D24 is a pure calculus result — it holds for sinc²(t) on any corridor
(0,1) regardless of Z/10Z. The ring normalization puts CREATE=5 at t=1/2,
but t=1/2 is already the unique sine-max independent of the ring. The
inheritance split's t=1/2 location adds no new information beyond what
sinc²(t) already forces.

**Conclusion:** Hatch 1 works as an escape from the ring obstruction,
but it removes Z/10Z from the picture. The bridge, if it exists, is
a sinc²-universality bridge (D2+B6), not a Z/10Z-ring bridge.

**Hatch 2 — inverse limit / profinite:**
This is a mathematically coherent escape: lim← Z/nZ = Ẑ = ∏_p Z_p
(product of p-adic integers) sees all primes. If the Z/10Z structure
can be embedded into Ẑ in a way that preserves the inheritance split,
and if Ẑ has a natural map to the Euler product, then the bridge might
work through the profinite completion.

Gap: No such embedding is constructed. The Z/10Z ring structure (TSML,
BHML, T*=5/7) is not obviously compatible with Ẑ's product structure.
This is a potential minimum extension (see A10_MINIMAL_EXTENSION.md).

**Hatch 3 — prime-indexed family:**
This would require defining TSML_p and BHML_p for each prime p, with
Z/10Z being the "base case" at p=2,5. No such family is defined in D1–D24.
This is also a potential minimum extension.

---

## Formal Statement of the Obstruction Result

**Theorem (Ring Bridge Obstruction):** No map φ: Z/10Z → (structure
sensitive to individual primes p ≠ 2,5) can be a ring homomorphism.
In particular, no ring homomorphism from Z/10Z can distinguish the Euler
product factors at primes p ≡ 3 (mod 10), p ≡ 7 (mod 10), or p ≡ 9 (mod 10).

This is a theorem, proved above. It is not speculative.

**Corollary (Conditional on Ring-Based Bridge):** If the A10 bridge φ
is required to be a ring homomorphism from Z/10Z, then no bridge can
fully recover the Euler product. Any ring-based bridge is incomplete.

**Corollary (Escape Condition):** A complete bridge must either:
(a) go through sinc² universality (D2) without requiring Z/10Z ring
    structure specifically, or
(b) use an extension of Z/10Z (profinite, prime-indexed, or other) that
    is prime-sensitive.

Neither (a) nor (b) is constructed in D1–D24.

---

## What This Means for A10

The ring prime blindness theorem is the strongest obstruction result
available from current spine alone. It establishes:

1. **A ring-homomorphism bridge from Z/10Z to the Euler product is blocked.**
   This is a proved result, not a conjecture.

2. **The bridge, if it exists, must escape the ring.** It runs through
   sinc² universality (route a) or a ring extension (route b).

3. **Route (a) is not a Z/10Z result.** It is a statement about all primes
   via D2's universal sinc² limit. Z/10Z becomes incidental.

4. **Route (b) requires new mathematics** not present in D1–D24.

**A10 reclassification status after this analysis:**

The Z/10Z-specific version of A10 ("ring inheritance split → σ=1/2")
is blocked by the ring prime blindness theorem for the ring-homomorphism case.

The sinc² universality version of A10 (D2 + B6: prime field sinc² matches
Montgomery's kernel) remains open. But this is a restatement of B6, not
an A10 claim.

The boundary between A10 and B6 is sharper than previously stated.

---

*Next: `A10_NO_GO_ATTEMPT.md` — attempts the strongest no-go result.*
*See also: `A10_MODULUS_COMPARISON.md` — tests whether Z/10Z is special.*

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
