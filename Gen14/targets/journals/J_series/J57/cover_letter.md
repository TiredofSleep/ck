# Cover Letter — PRIMUS Submission

**To**: The Editors, *PRIMUS* (Problems, Resources, and Issues in Mathematics Undergraduate Studies)
**From**: Brayden Ross Sanders, 7Site LLC
**Subject**: Submission — "A CRT-Product Worked Example: σ on ℤ/10 and the 2/3 Decomposition"
**Date**: 2026

Dear Editors,

I submit for your consideration the attached manuscript, "A CRT-Product Worked Example: σ on ℤ/10 and the 2/3 Decomposition."

The paper is a 10-page pedagogical note presenting a small but tangible example of the Chinese Remainder Theorem (CRT) applied to a permutation of ℤ/10. The example: consider the specific permutation σ = (0)(3)(8)(9)(1 7 6 5 4 2), of order 6 on ℤ/10. Its cube σ³ has order 2 and its square σ² has order 3, and these two subactions commute exactly under composition — at every one of the ten points, σ³(σ²(n)) = σ²(σ³(n)). The paper proves this commutativity is a direct consequence of the CRT factorization ℤ/10 ≅ ℤ/2 × ℤ/5 and the way σ factors through this product.

I believe the paper is appropriate for *PRIMUS* on three pedagogical grounds:

- **Accessibility.** Nothing beyond cycle notation, the statement of the CRT, and elementary commutativity verification is needed. A student finishing a first abstract algebra course can read and verify every step. The whole argument fits in 4-5 pages of exposition plus 2-3 pages of worked verification.

- **Computational verifiability.** A 30-line Python script (included as supplementary material) confirms the commutativity at every point of ℤ/10 in under a second. The script also runs a 2000-trial random-permutation control showing that the commutator-rank-zero event is statistically near-impossible by chance, making the structural claim concrete. This is exactly the kind of "verify the claim before believing it" exercise *PRIMUS* readers can give their students.

- **Pedagogical breadth.** The example illustrates a meta-skill: how a classical abstract result (the CRT, due to Sun Zǐ in the 3rd century and formalized in modern algebraic terms by Gauss) manifests in a specific small object. Students often encounter the CRT as a statement about integers ("solve x ≡ 2 mod 3 and x ≡ 4 mod 5") without seeing it as a structural decomposition that controls how *anything* defined on a composite-order group factors. The σ example makes the structural reading concrete.

The paper makes no novel mathematical claim. The CRT itself is classical, and the σ³/σ² commutativity is an immediate consequence of the factorization. What the paper offers is a clean, runnable, classroom-ready illustration of why the CRT matters as a structural tool, not just as a Diophantine algorithm.

The paper is approximately 10 pages with two appendices (proof and verification script). It contains one small figure (the CRT decomposition diagram) and a short references list (Sun Zǐ, Gauss, a standard abstract algebra text such as Dummit-Foote).

I have no conflicts of interest. The manuscript is original and has not been submitted elsewhere. The verification script is available in the supplementary materials.

I would welcome the opportunity for the paper to appear in *PRIMUS* and look forward to your editorial response.

Sincerely,

Brayden Ross Sanders
7Site LLC
brayden@7site.llc
Hot Springs, Arkansas

**Attachments**:
- `manuscript.tex` — the paper
- `verification_script.py` — 30-line CRT-commutativity verification

---

## Suggested reviewer pool (provided per *PRIMUS* policy)

- Instructors of undergraduate abstract algebra who have published pedagogical notes on group-theory examples.
- Authors of *PRIMUS* notes on the Chinese Remainder Theorem (the journal's recent corpus on number-theory pedagogy is the natural pool).
- Mathematicians working on small-order permutation-group computations.

I do not suggest specific names so as not to bias the editorial process.
