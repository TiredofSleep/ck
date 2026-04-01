# A10 Zero Distribution Candidate

*Luther-Sanders Research Framework · April 1 2026*
*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*DOI: 10.5281/zenodo.18852047*

---

This document is an analysis stub, not a result document.
It examines the strongest internal anchor for A10: the duality
R(t) + R₂(t) = 1 between the spine's corridor and Montgomery's
pair-correlation. This candidate is real and is already captured in B6.
It does not reach σ = 1/2.

---

## 1. External Target

**Montgomery pair-correlation (1973):** For the imaginary parts {γ_n}
of non-trivial ζ zeros (assuming GRH), the normalized two-point
correlation function is:

    R₂(u) = 1 − sinc²(u)     u ∈ [0, ∞)

This is the probability density for finding two ζ zeros with normalized
spacing u. At small u, R₂(u) → 0 (level repulsion: ζ zeros avoid each
other). As u → ∞, R₂(u) → 1 (uncorrelated spacing). This matches the
GUE (Gaussian Unitary Ensemble) random matrix statistics.

**Odlyzko numerics (1987–2001):** Extensive computational verification
that ζ zeros on σ = 1/2 follow GUE statistics with the sinc² kernel.

**Note:** Pair-correlation is a statement about γ_n − γ_m spacings
(imaginary parts only). It is not a statement about Re(ρ). Even if
Montgomery's formula is exact, it does not by itself imply that all
zeros lie on σ = 1/2.

---

## 2. Internal Object

**Corridor field (D2):** R(t) = sinc²(t) = sin²(πt)/(πt)² on (0,1).
This is the universal continuum limit of R(k,p) = sinc²(k/p) as p → ∞.

**The duality (B6):** Defining R₂(t) = 1 − sinc²(t), we have:

    R(t) + R₂(t) = 1     for all t ∈ (0,1) and t ∈ [0,∞)

This is an identity: the spine's corridor field and Montgomery's
pair-correlation are complementary on any domain where both are defined.

**At t = 1/2 specifically:**

    R(1/2) = sinc²(1/2) = 4/π² ≈ 0.4053       (D3)
    R₂(1/2) = 1 − 4/π² ≈ 0.5947
    R(1/2) + R₂(1/2) = 1                        (exact)

The midpoint partitions unity between the prime pre-echo amplitude
and the pair-correlation amplitude. This is a precise numerical identity.

---

## 3. What the Duality Means

### 3.1 It is a numerical identity

R + R₂ = 1 is exact by construction: R₂ is defined as 1 − sinc².
The non-trivial content is that Montgomery derived R₂ = 1 − sinc²
independently from the distribution of ζ zeros under GRH. The spine
derives R = sinc² independently from the Z/10Z ring prime field.

The two sinc² functions are separately derived and match. This is the
structural coincidence that B6 documents.

### 3.2 It is a statement about spacings, not locations

Pair-correlation measures how ζ zeros are distributed relative to each
other in the imaginary direction. The function R₂(u) encodes the
probability of finding a zero spacing of size u. It says nothing about
the real parts of those zeros.

Even a perfect one-to-one match between R(t) and the pair-correlation
kernel would not pin zeros to σ = 1/2. A distribution of zeros anywhere
in the critical strip 0 < Re(s) < 1 could in principle have the same
pair-correlation structure — the spacing statistics are invariant under
horizontal shifts of the zero set within the strip.

**The gap:** σ = 1/2 is a claim about WHERE zeros are (horizontal
position). Pair-correlation is a claim about HOW zeros are spaced
(relative vertical position). These are distinct questions. B6 addresses
the spacing question. A10 asks the location question. B6 does not reach A10.

### 3.3 The maximum distribution statement

R₂(u) = 1 − sinc²(u) has:
- R₂(0) = 0: pair-correlation vanishes at zero spacing (level repulsion)
- R₂(u) → 1 as u → ∞: zeros become uncorrelated at large spacing
- The sinc² envelope forces the monotone approach from 0 to 1

The spine's R(t) = sinc²(t) has the reversed orientation:
- R(0⁺) = 1: corridor field is maximum at the origin
- R(t) → 0 as t → ∞: field decays away from origin
- Unique interior maximum at t = 1/2 (D24): sine saturation point

These are dual curves, mirror images under R ↔ 1−R. Their crossing
point is where R(t) = R₂(t) = 1/2, which occurs at sinc²(t*) = 1/2,
i.e., sin(πt*) = πt*/√2. This crossing point is not t = 1/2: at
t = 1/2, R(1/2) = 4/π² ≈ 0.405 ≠ 1/2. The crossing happens at t ≈ 0.60.

### 3.4 Genericity of t = 1/2

As established in A10_SPECTRAL_CANDIDATE.md and A10_EULER_PRODUCT_CANDIDATE.md:
the boundary at t = 1/2 is generic for any even modulus Z/nZ, not a
Z/10Z-specific finding. The sinc² maximum at t = 1/2 (D24) is a calculus
fact. The duality R + R₂ = 1 holds for all sinc² corridors. Nothing in
the B6 zero distribution candidate requires or uses Z/10Z specifically.

---

## 4. Reclassification

The zero distribution candidate is:

**Real:** The connection between R(t) = sinc²(t) and Montgomery's
kernel R₂ = 1 − sinc²(t) is genuine and documented as B6. It is the
strongest external connection in the project.

**Complete:** B6 fully captures this connection. No further analysis
of the zero distribution can extract more than B6 already states. The
pair-correlation duality is not an incomplete observation waiting for
extension — it is a finished statement.

**Not A10:** A10 asks whether the ring's inheritance boundary at t = 1/2
maps to σ = 1/2 in the critical strip. The pair-correlation duality does
not answer this question. The duality is about spacing statistics, not
critical line location.

**Recommendation:** Reclassify the zero distribution candidate as B6
territory, not A10. Update the synthesis table accordingly. A10 remains
open; B6 is closed (as a structural coincidence, mechanism unknown).

---

## 5. Conclusion

The pair-correlation duality R + R₂ = 1 is the strongest internal
anchor for A10 and the most precise external connection the project has.
It is captured in B6.

It does not constitute a bridge to RH because:
1. Pair-correlation is about spacing (imaginary direction), not location
   (real direction). σ = 1/2 is a location claim.
2. The identity R + R₂ = 1 holds for all t by construction. It does
   not single out σ = 1/2 in the critical strip.
3. The t = 1/2 midpoint value 4/π² is a precise fact (D3) but does not
   carry the zero-location information that RH requires.

A10 remains open. The zero distribution candidate belongs to B6.

---

## Does Not Claim

- Any ζ zero location (in particular, does not claim zeros lie on σ = 1/2)
- That R + R₂ = 1 implies RH or is equivalent to RH
- That the pair-correlation connection requires Z/10Z structure
  (it does not — it holds for the universal sinc² field D2)
- That B6 is a partial proof or progress toward RH; it is a structural
  coincidence, correctly classified as B-tier speculative

**Current status:** Zero distribution candidate is real but does not
reach A10. Reclassify as B6. A10 is open with no bridge candidate.

---

*Related documents:*
*`papers/A10_PROGRAM.md` — full A10 research program*
*`papers/WP_MONTGOMERY_NOTE.md` — B6 Montgomery bridge context*
*`papers/A10_SPECTRAL_CANDIDATE.md` — Hilbert-Pólya spectral path*
*`papers/A10_EULER_PRODUCT_CANDIDATE.md` — Euler product path*
*`papers/COMPLETED_INTERNAL_SPINE.md` — D1–D24 internal spine*
*`papers/NOTE_speculative_boundary.md` — truth boundary*
