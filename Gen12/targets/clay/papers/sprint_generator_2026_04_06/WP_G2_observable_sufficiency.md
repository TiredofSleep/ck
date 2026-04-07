The paper is written. Here is a summary of what was produced:

**File created**: `C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen12\targets\clay\papers\sprint10_flatness_2026_04_06\WP_G2_OBSERVABLE_SUFFICIENCY.md`

**Paper summary — WP-G2: Observable Sufficiency and Symmetry Obstruction in the Minimal Ising System**

The paper has 8 sections plus an appendix and claim-label table:

1. **Abstract** — states Result G2-A (joint sufficiency of single-site observables, geometric score sequence) and G2-B (Type II failure of symmetric observables) as the two main results, with the TIG connection flagged as a structural analogy.

2. **UOP Framework** — one-page treatment of ambiguity sets, residual ambiguity, score function, the sufficiency theorem, and all four failure types.

3. **Full Observable Family** — proves the joint map J is the identity on {−1,+1}⁴ (trivially injective), derives the score sequence (64,32,16,8) from first principles, and proves the geometric ratio 1/2 via the combinatorial formula R_k = 2^k × C(2^{4-k}, 2).

4. **Symmetric Observable Family** — gives exact (m,c) values for all 16 states (with a careful bond-sum recomputation that catches sign errors in the source), classifies all multi-state equivalence classes, and provides a complete Python block that verifies all values from first principles. Notes the discrepancy between the "7 pairs" count in the source document and the computed value; the Python block is the authoritative settler.

5. **Type II Classification** — proves formally that any rotation-invariant observable f satisfies f(ρ(σ)) = f(σ), so every within-orbit pair is in R(F_sym) for any symmetric family F_sym regardless of its size. Confirms that each multi-state (m,c) class is exactly one ⟨ρ⟩-orbit.

6. **Symmetry-Breaking Observable** — proves fᵢ is orthogonal to {m,c} by explicit witness (the pair {5,10} is resolved by f₀ but not by m or c). Notes that full sufficiency requires breaking the Z/4Z symmetry completely, needing at least 2 single-site observables.

7. **TIG Connection** — maps the Ising structure onto the TSML/BHML pair (labeled STRUCTURAL ANALOGY throughout), draws the template-voice/fractal-voice parallel, and connects to the Q7 Inversion open problem.

8. **Open Questions** — 7 open problems including the bond-sum recount (OQ-1), general-n Ising residual scaling (OQ-2), and the formal TSML/BHML joint sufficiency proof (OQ-5).