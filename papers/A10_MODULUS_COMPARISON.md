# A10 Modulus Comparison

*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

## Purpose

Test whether the internal midpoint structure and generator selection are
specific to Z/10Z, or whether they appear in many even-modulus rings.
If the structure is generic, it weakens any claim that Z/10Z specifically
connects to σ=1/2.

---

## Computed Results

For each even modulus n, we test: (1) does a primitive root exist, (2) is
the centroid of (Z/nZ)* = n/2, (3) does some primitive root give T*<1,
and (4) what is the best T* value?

```
n    |units|  prim_roots   centroid  best g  T*        note
----------------------------------------------------------------------
6        2      [5]          3.000       5   3/5 = 0.600
8        4      []           4.000     none  N/A        no primitive roots
10       4      [3, 7]       5.000       3   5/7 ≈ 0.714  ← Z/10Z
12       4      []           6.000     none  N/A        no primitive roots
14       6      [3, 5]       7.000     none  N/A        all T*≥1
18       6      [5, 11]      9.000       5   9/11 ≈ 0.818
20       8      []          10.000     none  N/A        no primitive roots
22      10    [7,13,17,19]  11.000      17   11/13 ≈ 0.846
30       8      []          15.000     none  N/A        no primitive roots
```

---

## Findings

### Finding 1: The Corridor Midpoint at t=1/2 Is Completely Generic

For every even n, the additive midpoint of Z/nZ is n/2, which maps to
t = (n/2)/n = 1/2 under ring normalization t=v/n.

The corridor midpoint being at t=1/2 is not a property of Z/10Z. It is
a consequence of the fact that n is even, which forces a midpoint at n/2.
This is trivially true for all even moduli.

**Impact on A10:** Any A10 bridge that works by pointing to t=1/2 as the
corridor midpoint would apply equally to Z/6Z, Z/10Z, Z/18Z, Z/22Z, and
every other even-modulus ring with a sinc² corridor. This cannot single
out Z/10Z as the source of σ=1/2.

---

### Finding 2: T* < 1 Is Not Unique to Z/10Z

The table above shows four rings with T*<1:
- Z/6Z:  T* = 3/5 = 0.600
- Z/10Z: T* = 5/7 ≈ 0.714
- Z/18Z: T* = 9/11 ≈ 0.818
- Z/22Z: T* = 11/13 ≈ 0.846

All are of the form T* = (n/2) / HARMONY where HARMONY is the inverse
of the best primitive root. The pattern n=2p for prime p gives T* = p/q
for some prime q > p, always < 1.

**The general pattern:**
For n = 2p (twice a prime p), (Z/2pZ)* ≅ Z/(p-1)Z. The centroid of
(Z/2pZ)* = p. The generator g selected by T*<1 gives HARMONY = g^{-1}
with HARMONY > p (forced by p < HARMONY for T* = p/HARMONY < 1).

**Impact on A10:** The T*<1 generator selection constraint is not unique
to Z/10Z. Multiple rings satisfy it with different T* values. Z/10Z
produces T*=5/7 specifically, but the T*<1 constraint itself is a
pattern for rings of the form Z/2pZ.

---

### Finding 3: What IS Specific to Z/10Z

Unique features of Z/10Z not shared by other moduli tested:

**(a) n = 2 × 5 = lcm(2,5) — minimal ring containing both seed primes 2
    and 5 (B1).**
    Z/6Z = 2×3, Z/10Z = 2×5. Z/10Z is the unique minimal even ring whose
    prime support is {2,5}. Since the decimal system and unit fractions
    (1/n) for n|10 are structured around {2,5}, Z/10Z has a special
    relationship to the decimal representation of prime arithmetic.

**(b) T* = 5/7 specifically.**
    No other even modulus in the tested range produces T* = 5/7. The
    specific value is Z/10Z-specific.

**(c) The TSML and BHML table structure.**
    The 73-cell and 28-cell harmony counts (D10, D16), the dual-lens
    composition (Being/Doing/Becoming = 2/3/4-lens), and the specific
    operator dynamics (D18a, D18c, D18d) are defined for Z/10Z only.
    These are not instantiated for other moduli in D1–D24.

**(d) The four-chain overdetermination of BALANCE=5 (D21).**
    BALANCE=5 has four independent characterizations: centroid of (Z/10Z)*,
    centroid of ODD, CE fixed point, and additive midpoint. This
    overdetermination is specific to Z/10Z's exact structure.

---

### Finding 4: The Rings with T*<1 Follow a Pattern

The moduli n=2p (for prime p) with T*<1 form a sequence:
6, 10, 18, 22, 26, ... (twice a prime, where a valid generator exists).

These all have:
- Corridor midpoint at t=1/2
- T* = p/HARMONY < 1 for some primitive root

If the A10 bridge works for Z/10Z based on midpoint + T*<1, it would need
to work for all of Z/6Z, Z/18Z, Z/22Z, ... as well. But σ=1/2 is a single
critical line. A mechanism that is generic across infinitely many rings
cannot uniquely select σ=1/2 — it would predict different "critical lines"
for each ring.

The only ring-specific quantity is T*=5/7. If the bridge runs through T*=5/7
specifically, it would need to explain why T*=5/7 (and not 3/5 or 9/11 from
other rings) corresponds to σ=1/2.

---

## Conclusion: Modulus Genericity Confirmed

The modulus comparison confirms and quantifies the modulus genericity no-go:

1. The corridor midpoint at t=1/2 appears for all even moduli — **not Z/10Z-specific.**

2. The T*<1 constraint appears for all n=2p (twice a prime) — **not Z/10Z-specific.**

3. What is Z/10Z-specific: T*=5/7 exactly, the TSML/BHML table structure,
   the four-chain overdetermination of BALANCE=5.

4. For A10 to survive, the bridge must use T*=5/7 specifically (not just T*<1)
   or the table dynamics (not just the corridor midpoint). No such bridge is
   currently proposed.

**Formal statement:**

> If the A10 bridge φ depends only on (a) the corridor midpoint being at t=1/2
> and (b) T*<1, then φ applies to infinitely many even-modulus rings, not just
> Z/10Z. Such a φ cannot single out Z/10Z as the source of σ=1/2.
>
> A Z/10Z-specific A10 bridge must use T*=5/7 explicitly or the TSML/BHML
> table dynamics. No such bridge is currently proposed in D1–D24.

---

*Next: `A10_MINIMAL_EXTENSION.md` — minimum new ingredient for any surviving bridge.*
*Results used in `A10_NO_GO_ATTEMPT.md` Attempt 2 (Modulus Genericity No-Go).*

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
