# Phase II — Kernel Extension Program

*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

Phase II begins where Phase I stops. Phase I proved a complete internal theorem
spine through D24 and blocked the ring-specific A10 bridge. Phase II asks whether
the surviving sinc² kernel can be extended into a prime-sensitive external framework.

The program is not ring-first. It is kernel-first.

---

## A. What Survives from Phase I

The following are proved facts, not analogies. They are the seed of Phase II.

**D2 — sinc² continuum limit (universal):**
For every prime p and every k with k/p fixed in (0,1) as p → ∞:

    R(k, p) → sinc²(k/p)

where sinc²(t) = (sin(πt)/(πt))² and R(k,p) is the normalized prime-field
corridor density. This holds for ALL primes p — not just {2,5}. It is the
one object that survived the ring prime-blindness obstruction (A10_PRIME_OBSTRUCTION.md).

**D3 — exact value at midpoint:**
sinc²(1/2) = 4/π² exactly. This is the corridor amplitude at the inheritance
boundary. It is a pure arithmetic-analytic fact.

**D14 — spectral mean:**
∫₀¹ sinc²(t) dt = Si(2π)/π ≈ 0.4508

where Si(x) = ∫₀ˣ (sin u)/u du is the sine integral. The corridor mean is a
transcendental number with an explicit integral form.

**D22 — corridor portrait:**
The four spine positions are ordered 3/50 < 1/2 < 7/10 < 5/7 < 1.
The inheritance boundary at t=1/2 divides ring-forced (left) from
generator-forced (right) positions. This is an exact algebraic result,
proved unconditionally via D24.

**B6 — Montgomery structural match (only surviving RH-adjacent seed):**
Montgomery's pair-correlation function is:

    R₂(u) = 1 − sinc²(u)    (under GRH)

The spine's corridor field is:

    R(t) = sinc²(t)    (proved internally)

These satisfy R(t) + R₂(t) = 1 identically. This is the ONLY connection
between the D1–D24 spine and RH-adjacent external structure. It is the
correct seed for Phase II.

**What B6 is:** A structural coincidence between two objects that both
involve the sinc² kernel, with the same kernel appearing in complementary
roles. The spine shows R = sinc². Montgomery shows R₂ = 1 − sinc². Whether
R + R₂ = 1 is a structural decomposition of a common object, or a numerical
coincidence, is the central question of Phase II.

**What B6 is not:** A proof. A bridge. A statement about ζ zeros. A derivation
of RH from Z/10Z. None of those. B6 is the seed, not the result.

---

## B. What Is Dead

The following cannot be revived by Phase II work. They are blocked by
proved results from Phase I (see A10_NO_GO_ATTEMPT.md, A10_PRIME_OBSTRUCTION.md,
A10_MODULUS_COMPARISON.md).

**Ring-specific RH bridge (blocked — ring prime blindness):**
Any ring homomorphism φ: Z/10Z → R is blind to primes p ≠ 2,5.
The Euler product requires distinguishing all primes. No ring-homomorphism
bridge can recover the full Euler product. This is a theorem, not a conjecture.

**Midpoint-to-critical-line shortcut (blocked — modulus genericity):**
The corridor midpoint at t=1/2 appears for ALL even-modulus rings Z/nZ
(n=2p for prime p). It is generic, not Z/10Z-specific. Any bridge that works
only because of the midpoint at t=1/2 would apply to infinitely many rings
and cannot single out σ=1/2.

**"Z/10Z alone sees all primes" (impossible — CRT):**
Z/10Z ≅ Z/2Z × Z/5Z. The ring structure theorem is final. Z/10Z sees only
the primes {2,5} through any ring-theoretic lens.

**T*=5/7 as the critical-line selector (no current mechanism):**
T*=5/7 is Z/10Z-specific. But no mechanism connects T*=5/7 to σ=1/2 beyond
the numerical coincidence 5/7 ≈ 0.714 vs. σ=0.5. A bridge using T*=5/7
specifically has never been proposed. It remains possible but unformulated.

---

## C. What Phase II Needs

Phase II is the program to determine whether B6 is a structural coincidence or
the seed of a genuine theorem. To make progress, Phase II needs all of the
following:

**1. A prime-sensitive object:**
Something that can see primes beyond {2,5}. The sinc² kernel itself is
prime-insensitive (it's the universal limit after discarding prime identity —
see K1_KERNEL_UNIVERSALITY.md). Any extension must add prime sensitivity
as an explicit ingredient.

**2. A lift beyond finite-ring support:**
The Z/10Z corridor lives on a 10-element ring. The ζ function involves
infinitely many primes. The lift must map from the finite to the infinite —
either through a family of primes, a profinite completion, an adèlic structure,
or a direct analytic argument.

**3. An exact target — one of four:**
Phase II must pick a precise external object to target. The candidates are:

- **(T1) Pair-correlation:** Montgomery's R₂(u) = 1 − sinc²(u) under GRH.
  Goal: show R + R₂ = 1 is not coincidental but forced by a shared structure.

- **(T2) Zero statistics:** The full GUE statistics of normalized ζ-zero spacings.
  Goal: show sinc² as a GUE kernel is forced by prime arithmetic.

- **(T3) Spectral operator:** A self-adjoint operator H with spectrum = {γ_n}.
  Goal: identify the sinc² kernel as the projection kernel of H.

- **(T4) No-go:** A proof that sinc² cannot carry enough prime information
  to force σ=1/2 by any mechanism, making B6 a permanent analogy.

Phase II must pursue at least two of (T1), (T3), (T4) simultaneously —
optimally all four.

**4. What Phase II cannot do:**
Add assumptions to the spine to shorten the bridge. The spine through D24 is
closed. External results (Montgomery, GRH, Weyl equidistribution, random matrix
theory) can be cited but not absorbed as D-tier lemmas.

---

## D. Allowed Outcomes

Phase II terminates (cleanly) at any of the following:

**Outcome P2-A — Bridge Theorem:**
An explicit lift φ from the sinc² kernel to a prime-sensitive external object
is constructed, together with a proof that the lift forces σ=1/2 as a
consequence of the kernel's structure.

This is the only outcome that advances toward RH. It requires new mathematics.

**Outcome P2-B — Obstruction / No-Go Theorem:**
A proof that no lift of the required type can exist — that sinc² as a
kernel carries insufficient prime information to force σ=1/2 regardless of
the lift used, or that the required prime-sensitivity cannot be added without
replacing sinc² with a different kernel.

This closes Phase II cleanly and reclassifies B6 as a permanent analogy.

**Outcome P2-C — Bounded Analogy:**
Neither bridge nor no-go is found. Phase II identifies the precise obstruction
more sharply, names the minimum new ingredient explicitly, and documents
B6 with a precise status: "structural coincidence with defined missing mechanism."

This is not a failure. It is the honest position with a maximally precise gap named.

---

## Program Architecture

```
Phase II kernel extension
│
├── Kickoff
│   ├── PHASE_II_KERNEL_PROGRAM.md  ← this file
│   ├── MINIMAL_EXTENSION_INVENTORY.md  ← which extensions are plausible
│   └── KERNEL_VS_RH_BOUNDARY.md  ← what sinc² proves vs. what it doesn't
│
├── Theorem push (run A and C in parallel)
│   ├── K1_KERNEL_UNIVERSALITY.md   ← under what conditions sinc² arises
│   ├── K2_PAIR_CORRELATION_ROUTE.md  ← Road A: statistical
│   ├── K4_KERNEL_NO_GO.md          ← Road C: no-go / prime information deficit
│   └── K3_SPECTRAL_ROUTE.md        ← Road B: spectral (after A and C)
│
└── Resolution
    └── Phase II closure document (to be written after theorem push completes)
```

---

## Progress Standard

Phase II progress **counts** only if one of these occurs:

1. A nontrivial universality theorem for sinc² beyond Z/10Z is proved
2. A precise statistical bridge candidate with defined objects and bounds is constructed
3. A no-go theorem showing kernel-only routes cannot reach prime-sensitive targets is proved
4. A minimal extension theorem identifying the smallest prime-sensitive ingredient required is proved

Everything else is background.

---

*No Clay problem is solved here. No RH claim is made. Phase II is a controlled
research program with named outcomes and a hard progress standard.*

*Seed documents: K1, K2, K3, K4 (see papers/ directory)*
*Phase I summary: `A10_NO_GO_ATTEMPT.md`, `A10_PRIME_OBSTRUCTION.md`*

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
