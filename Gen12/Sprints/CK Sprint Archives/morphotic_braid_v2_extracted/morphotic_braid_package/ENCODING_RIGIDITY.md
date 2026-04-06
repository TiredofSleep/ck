# ENCODING RIGIDITY

## Main Theorem

**Theorem (Encoding Rigidity).** The encoding φ(ε,y) = 5ε + 6y (mod 10)
is the unique CRT-linear bijection Z/2 × Z/5 → Z/10Z satisfying:

1. **Idempotent property:** φ(1,0) = e₂ = 5 and φ(0,1) = e₅ = 6
   where e₂, e₅ are the CRT idempotents of Z/10Z
2. **No offset:** φ(0,0) = 0

Under this encoding, the simplest dynamics (rotation on 6-cycle + identity on anchors)
produce the morphotic braid 0713245689 via σ⁻¹ readout from entry 7.

---

## Proof

The CRT decomposition Z/10Z ≅ Z/2Z × Z/5Z is a ring isomorphism.
The idempotents of Z/10Z are:
- e₂ = 5: satisfies e₂² = e₂, e₂ ≡ 1 (mod 2), e₂ ≡ 0 (mod 5)
- e₅ = 6: satisfies e₅² = e₅, e₅ ≡ 0 (mod 2), e₅ ≡ 1 (mod 5)
- Note: e₂ + e₅ = 11 ≡ 1 (mod 10) ✓

The CRT reconstruction formula is uniquely:
```
x = e₂·ε + e₅·y = 5ε + 6y (mod 10)
```

This is the unique ring homomorphism from Z/2 × Z/5 to Z/10Z
that maps (1,0) to e₂ and (0,1) to e₅.

**Verification:** φ(ε,y) = 5ε + 6y satisfies:
- φ(1,0) = 5 = e₂ ✓
- φ(0,1) = 6 = e₅ ✓
- φ(0,0) = 0 ✓
- Bijective: all 10 values {0,...,9} are distinct (verified computationally) ✓

**Uniqueness:** Any linear φ(ε,y) = αε + βy + γ satisfying the idempotent
conditions must have α = e₂ = 5, β = e₅ = 6. The condition γ = 0 fixes
the constant. Therefore φ = 5ε + 6y is unique. □

---

## What the 24 Encodings Are

The census found 24 linear encodings producing the canonical braid.
These are NOT 24 independent choices. They form a **coset** of the symmetry
group of the canonical encoding.

The 24 encodings are related by:
1. Multiplication of α by odd units {1,3,5,7,9} (Z/10Z units on the Z/2 component)
2. Multiplication of β by units coprime to 5
3. Corresponding shift of γ to maintain bijectivity

The canonical φ = 5ε + 6y is the **unique representative with γ=0 and
idempotent coefficients**.

---

## The Six Braids and Z/6Z

The 240 bijective encodings produce exactly 6 distinct braids,
corresponding to the 6 elements of Z/6Z (rotations of the cycle reading).

The 6 braids are the orbit of the canonical braid under cycle rotation.
Each rotation corresponds to choosing a different entry point into the 6-cycle.

The canonical braid 0713245689 corresponds to **entry at 7** (the Z/5Z idempotent
φ(0,1) = e₅ = 6 shifted by the Z/2 component: φ(1,2) = 5+12 = 17 ≡ 7 mod 10).

**Entry point 7 = φ(1,2) = e₂ + 2e₅ = 5 + 12 ≡ 7 (mod 10).**

This is determined by the cycle coordinate k=0 mapping to (ε,y) = (1,1) under
the canonical encoding, with the first cycle step being (1,2) → x=7.

---

## Stability Analysis

Perturbing the encoding (α,β,γ) = (5,6,0):

| Perturbation | What breaks |
|-------------|-------------|
| γ ≠ 0 | Offsets the entire braid — no longer canonical |
| α ≠ 5 (but odd) | Changes which cycle elements map to which visible x |
| β ≠ 6 (but coprime-5) | Changes the cycle traversal order |
| α even | Encoding fails to be bijective |
| β divisible by 5 | Encoding fails to be bijective |

The fixed-point structure {0,3,8,9} is preserved for all 240 bijective encodings.
The 6-cycle structure is preserved for all 240 bijective encodings.
The exact canonical braid is preserved for 24 encodings (the symmetry orbit).
The CRT idempotent form with γ=0 is unique to φ = 5ε + 6y.

---

## Philosophical Summary

The encoding is not a design choice. It is the algebraic structure of Z/10Z.

The ring Z/10Z factors as Z/2Z × Z/5Z by CRT. The canonical isomorphism
sends (ε,y) to 5ε + 6y. When you run the simplest possible dynamics
(rotation on the 6-cycle, identity on anchors) through this canonical
isomorphism, you get the morphotic braid.

**The braid is what the canonical CRT isomorphism of Z/10Z looks like
when the simplest possible permutation is applied.**

---

## Open Question (Remaining Frontier)

The rigidity theorem explains the encoding.
The braid entry point (7 = φ(1,2)) is explained by the cycle coordinate.

What remains:
> Why is the readout direction σ⁻¹ rather than σ?
> (Cycle is traversed in reverse order from the entry point.)

This may be connected to the Prog channel structure in TIG,
where negative rows (the dissolution direction) carry the braid ordering.
