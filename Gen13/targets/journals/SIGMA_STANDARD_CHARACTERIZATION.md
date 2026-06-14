# σ, decontextualized: what the "polynomial permutation" actually is

**2026-06-14.** Brayden: *"on the polynomial permutation… if we have only studied
it across our substrate, that is our mistake — take the whole [σ] series out of its
current context and see how it applies to other researchers."* Right. Here is σ
stripped of all TIG framing and described in standard terms, computed from scratch
(`sigma = [0,7,1,3,2,4,5,6,8,9]`).

## The three hard facts (all computed, reproducible)

1. **As an element of S₁₀:** σ = (0)(3)(8)(9)(1 7 6 5 4 2). Cycle type **[6,1,1,1,1]**,
   **order 6**. A 6-cycle plus four fixed points. Elementary; nothing distinguished
   about it as a bare permutation.

2. **σ is NOT a polynomial function over ℤ/10.** By CRT, ℤ/10 ≅ ℤ/2 × ℤ/5, and *any*
   polynomial over ℤ/10 must act independently on the two coordinates (the mod-2 part
   of the output depends only on the mod-2 part of the input). σ violates this: the
   even residues {0,2,4,6,8} map under σ to {0,1,2,5,8}, i.e. to mixed parities. So
   **no integer polynomial represents σ on its own ring.** The name "polynomial
   permutation" is, over ℤ/10, a misnomer.

3. **σ becomes a permutation polynomial only over the field 𝔽₁₁** (extend σ(10)=10).
   There it has degree **8**: σ̂(x) = 8x⁸ + 4x⁶ + 5x⁵ + 3x⁴ + 6x³ + 10x² + 4x over
   𝔽₁₁. Degree 8 is **generic** — not affine, not a Dickson polynomial, not a
   linearized polynomial. A degree-8 permutation polynomial of 𝔽₁₁ is not a
   distinguished object.

## What this means for the in-house framing

The J-series "Layer 1 (polynomial), σ⁶ = id proved by polynomial check" billing
overstates. "σ⁶ = id" is just "σ has order 6" — true, but *every* permutation
satisfies σ^(order) = id, so it carries no special weight. And σ is not a polynomial
over ℤ/10 at all. **Action:** reconcile the exact wording in the σ-polynomial paper
(working-dir J51 / the "G₆" claim) against these facts; keep "order-6 permutation,"
drop or heavily qualify "polynomial."

## Where σ genuinely connects to other researchers

- **As a permutation polynomial of a finite field** (Lidl–Niederreiter, *Finite
  Fields*, ch. 7): the 𝔽₁₁ form is citable, but degree-8 generic PPs are not of
  independent interest. This is **not** the productive door.
- **As the seed of a finite magma / quasigroup** — this *is* the productive door.
  σ's real mathematical life is the order-10 groupoid it generates and that
  structure's closure properties (joint closure, the 4-core attractor). That is
  **finite quasigroup / Latin-square / universal-algebra** territory — exactly the
  Drápal–Wanless line the J-series already cites. The audience that would care about
  this work studies Latin squares, quasigroup identities, and finite magma varieties
  — not permutation polynomials.

## Honest recommendation

Stop presenting σ as "the polynomial permutation." Present it as **an explicit
order-6 permutation of ℤ/10 (cycle type 6+1⁴) that seeds a finite commutative
magma**, and take the *magma and its closure/attractor theorems* to the
quasigroup/Latin-square community. That is where the real, non-numerological results
(joint closure, 4-core attractor, the forcing-axiom family) have a genuine home and
a genuine audience.

**Reproduce:** the computation (cycle type, the ℤ/10 non-polynomiality CRT test, and
the 𝔽₁₁ degree-8 interpolation) is a ~30-line standalone script; no TIG imports.

— Claude (Opus 4.8), with Brayden
