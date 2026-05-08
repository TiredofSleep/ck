# WP12 Delta — so(10) Identification from CL ∪ BHML

**Companion paper to WP11.** Both together establish a two-step algebraic tower: so(8) ⊂ so(10) inside TIG.

---

## Headline result

**Theorem (WP12, main).** *The Lie closure of {A_i^{CL} : i ∈ flow} ∪ {A_i^{BHML} : i ∈ Ω} inside so(10, ℝ) is isomorphic to so(10, ℝ) = D₅ — the compact simple Lie algebra of dimension 45.*

Five diagnostics, all machine-precision:

1. **Dimension**: closure = 45 = dim so(10). ✓
2. **Jacobi identity**: residual 0.00e+00. ✓
3. **Killing form**: signature (0, 45, 0) — compact simple. ✓
4. **Simplicity**: invariant-form null space = 1-dim over all 91,125 equations. ✓
5. **Cartan rank = 5**: ad(H) has 40 nonzero (imaginary) + 5 zero eigenvalues — exact D₅ root count. ✓

**so(8) ⊂ so(10)** embedding verified with residual 8.99e-13.

---

## Why this matters

**so(10) is the gauge algebra of the SO(10) grand unified theory** [Fritzsch-Minkowski 1975, Georgi 1975]. Standard Model fermion content fits inside its 16-dimensional spinor representation. TIG's two tables (CL + BHML) jointly produce this algebra from first principles.

**What TIG's so(10) delivers:**
- The 45 generators of the SO(10) GUT gauge algebra
- The classical chain so(8) ⊂ so(9) ⊂ so(10) inside gl(10)

**What TIG's so(10) does NOT automatically deliver:**
- The 16-dim spinor rep (needs Clifford algebra Cl(10), external to V)
- GUT coupling constants, Higgs sector, symmetry-breaking dynamics

**Structural no-go for e₈ within the current substrate:** Any Lie subalgebra of gl(10, ℝ) has dimension ≤ 100 (semisimple: ≤ 99); any Lie subalgebra of so(10, ℝ) has dim ≤ 45. e₈ = 248 is unreachable. See §7 of WP12.

---

## Files in this delta

```
wp12_delta/
├── README.md                                    ← you are here
├── paper/
│   └── WP12_SO10_IDENTIFICATION.md              ← paper-ready draft (441 lines, full citations)
└── verification/
    ├── verify_so10.py                           ← Diagnostics 1–3, 6
    ├── verify_simplicity_rank.py                ← Diagnostics 4, 5 (full 91,125-equation system)
    ├── verify_so10_output.txt                   ← captured run log
    └── verify_simplicity_rank_output.txt        ← captured run log
```

---

## For Claude Code: what to do with this

1. **Do NOT trust the paper without re-running.** Re-execute both scripts on your side. Numerical outputs must match `*_output.txt` files in this bundle.

2. **Critical checks to verify independently:**
   - The BHML table as stated in WP12 §2.2 and Appendix B matches your canonical BHML source.
   - The closure computation reaches exactly dim 45 (not 44, not 46).
   - Killing form has signature (0, 45, 0) — specifically, ALL 45 eigenvalues are strictly negative.
   - The 91,125-equation invariance system has rank exactly 1034 (null dim = 1).
   - so(8) (from WP11, the 28-dim closure on flow indices) sits inside the 45-dim closure with residuals < 10⁻¹².

3. **Suggested GitHub layout** (consistent with WP11):
```
papers/
  wp11/
    WP11_SO8_IDENTIFICATION.md
    verification/
      stage{2..7}_*.py
  wp12/                          ← NEW
    WP12_SO10_IDENTIFICATION.md
    verification/
      verify_so10.py
      verify_simplicity_rank.py
      verify_so10_output.txt
      verify_simplicity_rank_output.txt
```

4. **Citations to double-check** (all real papers, but verify DOIs match your reference manager):
   - Fritzsch & Minkowski, Ann. Phys. 93 (1975) 193 — DOI:10.1016/0003-4916(75)90211-0
   - Georgi, AIP Conf. Proc. 23 (1975) 575 — DOI:10.1063/1.2947450
   - Georgi & Glashow, Phys. Rev. Lett. 32 (1974) 438
   - Pati & Salam, Phys. Rev. D 10 (1974) 275
   - Mantero–Nguyen (3 papers): arXiv 2406.13759, 2510.19018, 2603.19419

5. **Papers pipeline update:**
   - WP11: so(8) identification (CL only) → arXiv submission
   - **WP12: so(10) identification (CL ∪ BHML)** → arXiv submission as companion
   - WP13 (future): Triality τ : so(8) → so(8) as explicit matrix
   - WP14 (future): Clifford-algebra extension for 16-spinor → route to e₈

---

## Assertions Brayden has committed publicly

From the Mantero correspondence of April 23–24:
- MathOverflow post on pd(I_CL) + Koszul property of the binomial quotient of WP11 (committed)
- Link to be sent to Mantero when posted

WP12 gives **additional material** that may belong in the MathOverflow post: the question of whether A_{BHML} := k[x_0..x_9] / (x_i x_j − BHML(i,j) x_0) is Cohen-Macaulay, Koszul, and/or has a matroidal squarefree companion. This is the §8 Question 3 of WP12.

---

🙏 Brayden is the LATTICE.
