# arXiv Submission Preparation
## WP34 + WP35: First-G Law and Prime Phase Transition

*Brayden Ross Sanders & C. A. Luther*
*Target: arXiv submission | Phase 4 milestone: September 2026*
*DOI: 10.5281/zenodo.18852047*

---

## Overview

Two papers, one submission pair. WP34 proves the foundation; WP35 builds on it.
They cite each other and should be submitted together or in immediate sequence.

**WP34** — The First-G Law and Prime-Forced Dispersion
**WP35** — The Prime Phase Transition: Harmonic Pre-Echo, Zero-Width Gates, and the Geometry of RSA Security

Both papers are proved and verified. Both are frozen.

---

## Submission Checklist

### Content readiness
- [x] Main theorems proved algebraically
- [x] Verification data (36,662 exact computations, 187 semiprimes, zero exceptions)
- [x] Figures/tables: interleave staircase, verification tables, sinc² convergence
- [x] References: Montgomery (1973), Shannon (1949), Riemann (1859) and 18+ others in WP35
- [ ] LaTeX conversion (papers currently in Markdown with inline LaTeX)
- [ ] Author affiliations formatted for arXiv
- [ ] Abstract ≤ 1920 characters verified
- [ ] MSC classification codes added
- [ ] arXiv category selected (see §3)

### Legal/IP
- [x] IP note in WP35: CK, T*, TIG framework IP of Brayden Ross Sanders / 7Site LLC
- [x] Author order and attribution established (Sanders, Luther, Gish)
- [x] DOI: 10.5281/zenodo.18852047 (Zenodo preprint already archived)
- [ ] Confirm co-author approval (Luther, Gish) before arXiv submission

---

## Formatted Abstracts (arXiv-ready)

### WP34 Abstract

**The First-G Law: Prime-Forced Phase Transitions in Modular Alphabets**

For every semiprime b = p × q with p ≤ q, the smallest element of {1,...,k} that
shares a factor with b appears at exactly k = p. We prove this algebraically in three
lines of divisibility reasoning and verify it across all 153 semiprimes b ≤ 500
(36,662 exact computations, zero exceptions). The proof extends immediately to
all composite moduli with any number of distinct prime factors. The law identifies
the smallest prime factor of b as the unique determinant of when modular obstruction
begins in a growing alphabet. Corollaries characterize the stability window {1,...,p-1},
the prime-indexed phase transition structure, and the connection to gate difficulty
in modular optimization. The law is a foundational result for the TIG (Trinity
Infinity Geometry) framework and a prerequisite for the harmonic pre-echo theory
of WP35.

*Character count: ~810*

---

### WP35 Abstract

**Harmonic Pre-Echo, Zero-Width Gates, and the Sinc² Bridge to Montgomery's Pair Correlation**

The First-G Law establishes when prime obstruction begins in a modular alphabet:
at exactly k = p, the smallest prime factor of the modulus. This paper establishes
how it begins. We prove the Harmonic Pre-Echo Countdown Law: every prime factor f
of a modulus b casts a harmonic shadow R(k,f) = sin²(πk/f) / (k² sin²(π/f)) in
the unit alphabet {1,...,k}, reaching minimum 1/(f-1)² at k = f-1 and collapsing
to exactly 0 at k = f. The phase transition has zero width: a perfect step function
in the gate-size sequence. The function R(k,f) is ω-blind — identical for b = p²,
b = p×q, and b = p×q×r — seeing only the prime, not the ring. In the continuum
limit f → ∞, R(k,f) converges to sinc²(k/f) with error O(1/f²), establishing a
structural bridge to Montgomery's pair correlation of Riemann zeros (1973):
R₂(u) = 1 - sinc²(u). The two sum to unity — a complete spectral partition. We
derive T* = 5/7 as the exact unit density of the minimal strong semiprime b = 35
at its second gate event, and connect this to RSA hardness via the RSA Hardness
Inversion Principle. All results verified against 187 semiprimes, zero exceptions.
A third independent derivation of T* = 5/7 emerges from the cyclotomic reduction
test: p = 5 is the first prime where the chain sinc²(1/p) = p²(4−A_p²)/(4π²)
closes nontrivially (A_p = 2cos(π/p)), and p = 7 is the first obstruction. Three
independent chains, same threshold.

*Character count: ~1180*

---

## MSC Classification Codes

### WP34
**Primary:** 11A51 (Factorization; primality)
**Secondary:**
- 11B57 (Farey sequences; the Stern-Brocot tree, etc. — for the interleave partition structure)
- 11N05 (Distribution of primes — for prime-indexed phase transitions)
- 05A17 (Combinatorial aspects of partitions of integers — for C/G partition structure)

### WP35
**Primary:** 11A41 (Primes)
**Secondary:**
- 42A10 (Trigonometric approximation — for sinc² convergence)
- 11M26 (Nonreal zeros of ζ(s) and L-functions — for Montgomery bridge connection)
- 11A07 (Congruences and residues — for modular structure)
- 42B10 (Fourier and Fourier-Stieltjes transforms — for spectral framing)

**Note:** The Montgomery bridge result (§4 of WP35) is labeled Tier A conjecture —
structural analogy, mechanism unknown. MSC 11M26 is appropriate for the Tier A claim
as stated. Do not add MSC codes suggesting the bridge is proved.

---

## arXiv Category

**Primary:** math.NT (Number Theory)
**Cross-list:** math.CO (Combinatorics) — for the partition/interleave structure

Both papers are pure mathematics. Do not cross-list to cs.CR (Cryptography) for the
initial submission — the RSA hardness discussion in WP35 is observational. A later
version can add cs.CR once the cryptographic implications are developed.

---

## Author Affiliations

**Brayden Ross Sanders**
7Site LLC
[City, State — to be provided]
ORCID: [to be registered]

**C. A. Luther**
[Affiliation — to be provided by Luther]
ORCID: [to be registered]

**Monica Gish**
[Affiliation — to be provided]
ORCID: [to be registered]

*Note: Register ORCIDs before submission. arXiv strongly recommends ORCID linking
for author disambiguation.*

---

## LaTeX Conversion Notes

Both papers are in Markdown with inline LaTeX math. For arXiv:
1. Convert to .tex files using pandoc or manually
2. Confirm all math environments: `\[ \]` for display, `$ $` for inline
3. Tables: use `tabular` environment
4. The Proof block in WP34 §3: ensure `\begin{proof}` and `\end{proof}` with QED symbol
5. Figures: the interleave staircase visualization (mentioned in WP34 §4) — needs
   actual figure file (.pdf or .eps). Currently described in text only.
   Options: generate from `tig_algebra.py` data, or submit as text-only first.
6. WP35 uses full bibliography with 21+ references — convert to BibTeX entries
7. The IP note in WP35 can remain as a footnote; arXiv does not require removal
8. Recommended LaTeX class: `amsart` or `amsmath` article

---

## Recommended Submission Order

**Step 1 (immediate):** Submit WP34 to arXiv.
- Shorter paper, self-contained proof, easiest to review
- Establishes the foundation, gets a permanent arXiv ID
- Cite as [arXiv:XXXX.XXXXX] in WP35

**Step 2 (within 2 weeks):** Submit WP35 citing the WP34 arXiv ID.
- WP35 is the longer, richer paper
- Cites WP34 at multiple points — use the arXiv ID not just the DOI

**Step 3 (September 2026 target):** Submit the Luther-Sanders Equivalence joint paper
(LUTHER_SANDERS_MANUSCRIPT.md), citing both WP34 and WP35 arXiv IDs.

---

## Journal Targeting

**Short list (both papers):**
1. **Journal of Number Theory** (Elsevier) — primary target for WP34; well-established,
   appropriate for elementary but non-trivial prime structure results
2. **Experimental Mathematics** (Taylor & Francis) — appropriate for WP35 which has
   both proved theorems and computational verification
3. **Integers: Electronic Journal of Combinatorial Number Theory** — open access,
   lower barrier for WP34 as a short proved result

**For WP35 specifically:**
4. **Acta Arithmetica** — if the Montgomery bridge connection is strengthened to Tier B+
5. **Proceedings of the American Mathematical Society** — for a condensed version of
   the sinc² limit theorem alone

**Note on IHÉS:** Listed in the grant proposal as a presentation target. IHÉS is a
research institute, not a journal. The appropriate path is to present at a seminar
there after arXiv publication. Target after the Luther-Sanders Equivalence paper
is submitted.

---

## What Is and Is Not Ready

### Ready now
- All proved theorems (WP34 §2-3, WP35 §3-5): algebraic proofs complete
- Verification data: exact computation, 36,662 pairs, 187 semiprimes
- Tier D claims labeled correctly: First-G Law, Sinc² Limit, Universal 4/π²
- T* = 5/7 derivation (structural, not empirical)
- Corollaries and implications

### Not ready for the submission (properly labeled in papers, but not ready to claim)
- Montgomery Bridge mechanism: Tier A, structural analogy only
- Luther-Sanders Equivalence: Tier C → listed as future work in WP35 §7
- k-Gate Tier exact values: not in WP34 or WP35, don't add them

### What to NOT include in the arXiv versions
- Clay Millennium Problem connections: Tier A conjectures. Keep in WP36-WP42.
  Do NOT add Clay connections to WP34/WP35 — they will invite referee rejection
  and undermine the genuine results.
- CK organism architecture: internal, not relevant to the number theory papers
- "TIG framework" brand: describe the mathematical setup directly without the
  TIG name in the abstract. The acronym can appear in the introduction but should
  not be the primary framing for the arXiv abstract.

---

## Single Most Important Pre-Submission Action

Read the WP35 abstract one more time with the synthesis framework lens:
- Every sentence in the abstract should correspond to a Tier C or Tier D result
- The Montgomery bridge sentence ("structural bridge to Montgomery's pair correlation")
  is the one sentence that could attract referee attention on epistemics
- Recommend rewording to: "We identify a structural parallel to Montgomery's pair
  correlation of Riemann zeros (1973): R₂(u) = 1 − sinc²(u), where the TIG field
  gives sinc²(u) directly. The mechanism of this parallel is an open question."
- This is honest and still interesting. It does not overclaim.

---

`© 2026 Brayden Ross Sanders / 7Site LLC & C. A. Luther · DOI: 10.5281/zenodo.18852047`
