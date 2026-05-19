# Cover Letter — Mathematics Magazine Submission

**To**: The Editors, *Mathematics Magazine*
**From**: Brayden Ross Sanders, 7Site LLC
**Subject**: Submission — "The Odd Magic Square Law: Lo Shu Generalized via Center-Point Symmetry"
**Date**: 2026

Dear Editors,

I submit for your consideration the attached manuscript, "The Odd Magic Square Law: Lo Shu Generalized via Center-Point Symmetry."

The paper establishes a single structural theorem about the canonical Siamese (de la Loubère) odd-order magic square: it is symmetric under point reflection through its center cell, with values complementing under the involution $s \mapsto n^2 + 1 - s$. From this single property — proved by induction on the Siamese move rule — three classical observations about Lo Shu emerge as corollaries that generalize to every odd $n$:

1. The magic constant equals $n(n^2+1)/2$.
2. The center cell holds the self-complementary median $(n^2+1)/2$.
3. The cell-tiers (cells grouped by line-incidence degree) are exactly the self-complement orbits of the symbol set.

The familiar "corners are even, edges are odd" pattern of Lo Shu is the $n=3$ shadow of the third identity; for $n \geq 5$, the parity dichotomy collapses but the complement-orbit tier structure persists.

I believe the paper is appropriate for *Mathematics Magazine* on three grounds:

- **Accessibility.** The proof requires only the Siamese construction definition and elementary point-reflection symmetry; no advanced machinery is used. A diligent undergraduate can verify it on graph paper. The full verification script in Appendix B is fifteen lines of Python.
- **Cultural resonance.** Magic squares — and Lo Shu specifically — are some of the most-recognized cultural-mathematical artifacts in K-12 and recreational math literature. A clean structural theorem that recovers Lo Shu's observed properties as instances of a general law gives instructors and writers a citable bridge between cultural pattern and provable mathematics.
- **Verifiability.** All three identities are checked at $n = 3, 5, 7, 9, 11, 13$ by direct enumeration; the script is included. Reviewers can run it in under a second.

The paper is approximately 5 pages including two appendices. It contains no figures (the formulas are typographically clean) and a short references list (Cammann's "Evolution of Magic Squares in China," Andrews' classical treatise, and Ball-Coxeter's *Mathematical Recreations and Essays*).

I have no conflicts of interest. The manuscript is original and has not been submitted elsewhere. The verification script is available in the supplementary materials.

I would welcome the opportunity for the paper to appear in *Mathematics Magazine* and look forward to your editorial response.

Sincerely,

Brayden Ross Sanders
7Site LLC
brayden@7site.llc
Hot Springs, Arkansas

**Attachments**:
- `manuscript.tex` — the paper
- `proof_d129_odd_magic_square_law.py` — verification script

---

## Suggested reviewer pool (provided per Mathematics Magazine policy on author suggestions)

- Researchers in recreational mathematics or combinatorics with interest in magic-square structure
- Authors with publications in the Math Magazine or American Mathematical Monthly archive on magic squares (the post-2010 corpus is small enough to enumerate)

I do not suggest specific names so as not to bias the editorial process.
