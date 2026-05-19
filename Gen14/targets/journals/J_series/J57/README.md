# J57 — A CRT-Product Worked Example: σ on ℤ/10 and the 2/3 Decomposition

**Target venue**: *PRIMUS* (Problems, Resources, and Issues in Mathematics Undergraduate Studies, Taylor & Francis)
**Alternative venues**: *Mathematics Teacher: Learning and Teaching PK-12* (NCTM), *College Mathematics Journal* (MAA), *Mathematics Magazine* (overlap with J56 — pick one venue per submission)
**Status**: Manuscript ready for revision then submission
**Author**: Brayden Ross Sanders / 7Site LLC

## Summary

A 10-page didactic note showing how the Chinese Remainder Theorem (CRT) factorization ℤ/10 ≅ ℤ/2 × ℤ/5 manifests in a specific permutation σ of order 6 acting on ℤ/10, whose binary and ternary subactions commute exactly. This is undergraduate-accessible material: the worked example needs no machinery beyond cycle notation, the CRT statement, and elementary commutativity checks. The novelty is pedagogical, not mathematical — the CRT is itself classical (Sun Zǐ, ~3rd century).

## Why this venue

*PRIMUS* publishes practical pedagogy: worked problems, novel illustrations, classroom-ready material. The paper fits because:
- The example is small enough for a 50-minute class (one permutation, six functions, two cyclic subgroups).
- It bridges abstract algebra (the CRT statement) to concrete pattern-noticing (σ has clean 2×3 structure).
- It includes a verification script (~30 lines of Python) students can run themselves.
- It teaches a meta-skill: how to verify a structural claim computationally before believing it.

## Theorem statement (one sentence)

For the specific permutation σ = (0)(3)(8)(9)(1 7 6 5 4 2) on ℤ/10, the subaction σ³ (order 2) commutes exactly with the subaction σ² (order 3), and this commutativity is a direct consequence of the CRT factorization ℤ/10 ≅ ℤ/2 × ℤ/5.

## Files

- `manuscript.tex` — the LaTeX source
- `cover_letter.md` — submission cover letter
- `README.md` — this file
- `verification_script.py` — the 30-line verification (~1 sec runtime)

## Verification

```bash
python verification_script.py
```

Verifies: σ³ ∘ σ² = σ² ∘ σ³ at every point of ℤ/10; the 2000-trial random-permutation control shows the commutator-rank-zero event has probability ≈ 0 by chance; the CRT decomposition isomorphism is bijective.

## Submission process

1. Compile `manuscript.tex` with `pdflatex` (standard amsmath/amsthm packages).
2. Submit via *PRIMUS* online portal: <https://www.tandfonline.com/journals/upri20>
3. Include the verification script as supplementary material.

## Expected timeline

- Submission to first decision: ~3-5 months
- Revision cycle: ~4-8 weeks
- Acceptance to publication: ~6-12 months

## Related canon entries

- **D86** in `FORMULAS_AND_TABLES.md` — the σ² triadic class structure
- **D131** — single ⊂ face ⊂ lens vocabulary (face is the CRT factor)
- **D140** — CRT relocation thesis
- **D141** — TORUS EXCLUDED (the corrected non-commutativity reading of WP51)

## Honest scope reminder

This is a pedagogical note, not a research paper. The CRT itself is classical. What the paper shows is a small specific instance where the CRT's factorization is *computationally visible* — the σ³/σ² commutativity is a tangible numerical fact a student can verify in five minutes. The paper makes no new mathematical claim; it offers a clean illustration of a classical theorem applied to a specific small example.
