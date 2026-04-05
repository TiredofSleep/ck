# SPRINT ARCHIVE NOTES
## Prime–π–φ Bridge — Discarded Phrasings, Removed Claims, Path Record

---

## DISCARDED PHRASINGS

| Discarded | Reason | Replacement |
|-----------|--------|-------------|
| "self-referential named constant" | Too informal for theorem statements | "first prime for which deg(A_p/ℚ) = 2" |
| "the minimal polynomial can't touch it" | Imprecise — sounds like a reach, not a proof | Degree contradiction argument: if C_p ∈ ℚ+ℚA_p then A_p satisfies a quadratic, contradicting deg ≥ 3 |
| "it falls below the level the minpoly can reach" | Same problem as above | Same replacement |
| "the tangent is the gap" | Not proved; stated as theorem-level | Repositioned as open structural question with exact objects listed |
| "golden tangent" | Informal nickname | Retained in informal text only; removed from any theorem-adjacent context |
| "the bridge" (without qualifier) | Ambiguous — three structurally different bridges exist | Always qualified: finite closure bridge / mixed evaluation bridge / tangent approximation bridge |
| "π repeats itself" | Globally false, meaningless for this bridge | Removed entirely |

---

## INVALID CLAIMS REMOVED

| Claim | Why removed |
|-------|-------------|
| "What is the minimal polynomial of 16/π²?" | 16/π² is transcendental. It has no minimal polynomial over ℚ. Question is malformed. |
| "The tangent encodes the gap" | Not proved. Tangent line approximates r_{T*} to within 0.005 but this is not an exact geometric relationship. Stated as open question only. |
| Zero-spacing correlation with 2cos(π/p) | KS test (n=49, p-value 0.31) found no correlation. The bridge is at the functional/operator level, not the data level. Stated as a non-result. |
| "p=5 is cosmologically or universally special" | Outside scope. Removed. |

---

## WHY THE FINAL BACKBONE WAS CHOSEN

The sprint began with a flat list of identities: 2cos(π/5)=φ, sinc²(1/5)=25(3−φ)/(4π²), 16/π²≈φ. These were correct but structurally opaque — nothing explained why that chain was natural rather than cherry-picked.

The chain identity sinc²(1/p) = p²(4−A_p²)/(4π²) resolved this: it holds for every prime. The question became why p=5 is special within that universal formula. The answer required identifying the algebraic part C_p = 4−A_p², recognizing it as the Pythagorean complement of A_p (Layer 2), and asking whether C_p reduces to first order in A_p.

The reduction test C_p ∈ ℚ + ℚA_p is the exact criterion. Its equivalence to deg(A_p/ℚ) ≤ 2 via the linear independence argument (if A_p² = α+βA_p then A_p satisfies a quadratic, contradicting deg ≥ 3) gave a clean, attack-ready proof structure. This replaced the earlier informal "minpoly can't touch it" wording.

The approximation 16/π² ≈ φ was correctly repositioned as downstream of the exact fold/tangent geometry. The factor 4 in 16/π² = 4×(4/π²) is exact and structural. The proximity to φ is a numerical observation with no current exact proof. It belongs after the exact structure, not at the center.

---

## DOCUMENT EVOLUTION

1. `PRIME_PI_PHI_BRIDGE_MEMO.md` — First draft. Correct identities, incomplete structure.
2. `PRIME_PI_PHI_BRIDGE_HARDENED.md` — Submission-grade triage: exact/approx/non-claim separation. Fixed malformed minimal-polynomial question.
3. `PRIME_PI_PHI_RECURSIVE_OPERATOR_MEMO.md` — Added operator chain. Identified algebraic reduction behavior. Still used informal "minpoly can't touch it" language.
4. `PRIME_PI_PHI_OBSTRUCTION_ADDENDUM.md` — Added four-layer architecture. Identified C_p = 4sin²(π/p) as Pythagorean complement. Named sinc² as minimal analytic normalization. Still slightly informal on Layer 4.
5. `PRIME_PI_PHI_FINAL_TIGHTENING.md` — Replaced all loose wording with exact linear-independence contradiction proof. Reduction test C_p ∈ ℚ + ℚA_p made the backbone. Tangent result correctly positioned as downstream.
