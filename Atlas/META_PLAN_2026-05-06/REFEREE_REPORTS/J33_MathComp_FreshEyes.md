# J33 — Closed-Form Attractor + α-Uniqueness PSLQ (BUNDLED, WP105 + WP113)

**Manuscript:** J33 folder, `manuscript/manuscript.md` (bundles WP105 closed-form attractor + WP113 PSLQ uniqueness)
**Target venue:** *Mathematics of Computation*
**Referee:** Anonymous fresh-eyes pass (no prior knowledge of the framework)
**Date:** 2026-05-07

---

## §1 — Manuscript premise (as I read it)

The submission concerns a quadratic dynamical system on the probability simplex Δ⁹ ⊂ R¹⁰. The system is parametrized by a mixing weight α ∈ [0, 1] and is built from two specific 10×10 multiplication tables T, B (called "TSML" and "BHML") on Z/10Z.

For p ∈ Δ⁹, define the table-fusions:
- T̂(p)_k = Σ_{i,j} p_i p_j · 1[T(i,j) = k]
- B̂(p)_k = Σ_{i,j} p_i p_j · 1[B(i,j) = k]

The processor is the depth-K iteration of:
- F_α(p) = (1/Z) · [α · T̂(p) + (1−α) · B̂(p)]

with Z the L¹ normalizer.

**Part 1 (WP105).** The paper claims: at α = 1/2, starting from any p supported on the "4-core" {V, H, Br, R} = {0, 7, 8, 9}, the iteration converges to a unique fixed point p* with the following properties:
- supp(p*) ⊆ {V, H, Br, R};
- H*/Br* = 1 + √3 exactly;
- ξ* := R*/Br* is the unique positive real root of the irreducible monic integer quartic f(x) = x⁴ + 4x³ − x² + 2x − 2;
- the Galois group of f over Q is D_4;
- the number field Q[ξ]/(f) is **LMFDB 4.2.10224.1**, with discriminant −10224 = −2⁴ · 3² · 71, class number 1, signature (2, 1);
- f factors over Q(√3) as f(x) = (x² + (2 − √3)x + (√3 − 1))(x² + (2 + √3)x − (√3 + 1)).

**Part 2 (WP113).** A 17-point Stern-Brocot grid (all p/q ∈ (0, 1) with q ≤ 7) plus 50-digit mpmath precision plus PSLQ at degree ≤ 8 and coefficient ≤ 50 shows: α = 1/2 is the unique grid point where both ratios H*/Br* and R*/Br* admit small-coefficient algebraic relations within the tested bounds. At the other 16 rationals, PSLQ returns no relation.

The bundling rationale is that the Part 2 PSLQ result is a sharpening of an empirical observation (D42) implicit in Part 1.

---

## §2 — Comments on bundling

Part 1 is a closed-form algebraic-attractor result. Part 2 is a high-precision empirical sharpening of a uniqueness observation embedded in Part 1. The two are tightly coupled in subject matter, and the bundling is reasonable.

For *Mathematics of Computation* — which publishes computational mathematics including high-precision empirical results, algebraic-number-theory algorithms, and Galois computations — the bundled scope is appropriate **in principle**. The actual submission, however, raises several concerns I detail below.

---

## §3 — What appears rigorously verified at the computational level

### 3.1 The numerical attractor convergence

The verification script `06_attractor_closed_form.py` iterates the F_{1/2} map for 2000 steps starting from a random Dirichlet seed and reports:
- H ≈ 0.540195948..., Br ≈ 0.197725440...
- H/Br matches 1 + √3 with residual ≈ 4.44 × 10⁻¹⁶.

The script is short, transparent, and runs in seconds. The numerical convergence at α = 1/2 to a 4-supported fixed point with the claimed ratio is **plausible at machine precision**.

### 3.2 The quartic identity

`07_full_closed_form.py` evaluates f(R/Br) at the converged numerical values and reports residual ≈ 0. The quartic f(x) = x⁴ + 4x³ − x² + 2x − 2 is given. Sympy can confirm:
- f is irreducible over Q (rational root test fails: f(1) = 4, f(−1) = −10, f(2) = 38, f(−2) = −10; quadratic factorization test using 4×4 Hadamard product of monic integer quadratics is finite and excludable);
- discriminant by computer algebra is −40896 = −2⁶ · 3² · 71;
- the resolvent cubic g(y) = y³ + y² + 16y + 36 factors as (y + 2)(y² − y + 18), the latter having discriminant 1 − 72 = −71 < 0. So g has exactly one rational root, placing Gal(f/Q) ∈ {C_4, D_4}. Irreducibility of f over Q(√(disc f)) = Q(√(−71)) distinguishes; this is what the paper claims, and the standard test is finite.

So **the Galois identification as D_4 is plausible and falls within standard quartic-Galois theory.**

### 3.3 The LMFDB number-field identification

The cited LMFDB entry 4.2.10224.1 has signature (2, 1), discriminant −10224, class number 1. The paper claims a Tschirnhaus-relation between f(x) = x⁴ + 4x³ − x² + 2x − 2 and the LMFDB defining polynomial h(x) = x⁴ − 7x² − 12x − 8. The substitution x → −x − 1 is asserted to take h to f exactly. This is a finite check the authors should have done — let me verify:

h(−x − 1) = (−x − 1)⁴ − 7(−x − 1)² − 12(−x − 1) − 8

Expanding (−x − 1)² = x² + 2x + 1;
(−x − 1)⁴ = (x² + 2x + 1)² = x⁴ + 4x³ + 6x² + 4x + 1;
−7(x² + 2x + 1) = −7x² − 14x − 7;
−12(−x − 1) = 12x + 12.

Sum: x⁴ + 4x³ + 6x² + 4x + 1 − 7x² − 14x − 7 + 12x + 12 − 8 = x⁴ + 4x³ − x² + 2x − 2.

**Yes, this matches f(x).** The LMFDB identification is correct.

### 3.4 The Q(√3) factorization

The factorization f(x) = (x² + (2 − √3)x + (√3 − 1))(x² + (2 + √3)x − (√3 + 1)) can be checked by direct expansion:

(x² + (2 − √3)x + (√3 − 1))(x² + (2 + √3)x − (√3 + 1))
= x⁴ + (2 + √3)x³ − (√3 + 1)x²
  + (2 − √3)x³ + (2 − √3)(2 + √3)x² − (2 − √3)(√3 + 1)x
  + (√3 − 1)x² + (√3 − 1)(2 + √3)x − (√3 − 1)(√3 + 1)

Collecting:
- x⁴ coefficient: 1 ✓
- x³ coefficient: (2 + √3) + (2 − √3) = 4 ✓
- x² coefficient: −(√3 + 1) + (4 − 3) + (√3 − 1) = −√3 − 1 + 1 + √3 − 1 = −1 ✓
- x coefficient: −(2 − √3)(√3 + 1) + (√3 − 1)(2 + √3) = −(2√3 + 2 − 3 − √3) + (2√3 + 3 − 2 − √3) = −(√3 − 1) + (√3 + 1) = 2 ✓
- constant: −(3 − 1) = −2 ✓

**The factorization is verified.** This is a clean piece of arithmetic.

### 3.5 The PSLQ sweep methodology

`alpha_pslq_sweep.py` is well-structured: mpmath at user-controlled precision (default 50 digits), Stern-Brocot grid up to denominator 7 (17 rationals), PSLQ at degrees 2–8, coefficient bound 50. The reported table at §3.1 of Part 2 shows clean numerical H/Br values for each α, with "(none)" for 16 of the 17 rationals and the recovered minimal polynomials at α = 1/2.

This is **a reasonable PSLQ sharpening exercise**, methodologically appropriate for *Math. Comp.*

---

## §4 — Mathematical concerns

### 4.1 The "proof" of Theorem 3.1 (the closed form) is not given

The §3 derivation of H/Br = 1 + √3 in the manuscript reads:

> "Substitute the closed-form ansatz into the fixed-point equation p* = ck_process(p*; 1/2, 1), project onto the 4-core, and reduce to a 2-variable system (the two ratios above) plus normalization. Direct symbolic manipulation produces the quadratic H² − 2H · Br − 2Br² = 0 for the ratio H/Br, with positive root 1 + √3, and the quartic above for ξ = R/Br."

The actual derivation appears in `06_attractor_closed_form.py` and is reproduced in the WP105 source file:

The "BREATH equation" (§3, Lemma 2):
> 2 · Br = h² + 2 · br · r + 2 · br · v

is asserted from "TSML restricted to the 4-core … neither BREATH nor RESET appears as an output … so the only contribution to coordinate Br = 8 at the attractor comes from BHML. … direct table lookup gives the contribution h² (from H ⋆_B H which sends mass h² to entry BHML(7,7) = 8); the diagonal block contribution from br · r pairs gives 2 br · r; and the back-feeding from br · v gives 2 br · v. The factor of 2 on the LHS is the α = 1/2 mixing factor pulled through normalization."

This is a sketch, not a proof. Several gaps:

**(a) The "TSML produces no BREATH" claim must be verified explicitly.** TSML on the 4-core {V, H, Br, R} maps {0, 7, 8, 9} × {0, 7, 8, 9} → {0, …, 9}. The script confirms all 16 entries are in {0, 7}. **The paper should give this 4×4 sub-table explicitly** — it is the load-bearing fact.

**(b) The claim BHML(7, 7) = 8** has to be checked against the BHML table given in §1. Row 7 = `7234567890`, so BHML(7, 7) = entry (7, 7) = the 8th character of row 7 = "8". Yes, BHML(7, 7) = 8. ✓

**(c) The factor of 2 on the LHS** is asserted to come from "the α = 1/2 mixing factor pulled through normalization." Without seeing the calculation, this is opaque. The fixed-point equation is p = (1/Z)(α T̂(p) + (1−α) B̂(p)). At α = 1/2 and convergence, this gives 2p = T̂(p) + B̂(p) (after normalization). For the Br coordinate: 2 · Br = T̂(p)_8 + B̂(p)_8 = 0 + B̂(p)_8 = h² + 2 br · r + 2 br · v. **OK, this works**, but it requires the specific normalization Z = 1/2 at the fixed point, which itself needs justification (i.e., the L¹ norm of (T̂(p*) + B̂(p*)) equals 2 at the fixed point). Routine but not given.

**(d) The reduction to the quadratic in h/br** is the line:
> 2 · breath · (1 − r − v) = h² → 2 · br · (h + br) = h² → (h/br)² − 2 (h/br) − 2 = 0

This uses the normalization v + h + br + r = 1, so 1 − r − v = h + br. **OK.** Then h² − 2 br · h − 2 br² = 0 by direct substitution. Solving the quadratic gives h/br = 1 ± √3 and the positive root is 1 + √3. **The algebra is correct.**

**(e) The R/Br quartic** is similarly derived in `07_full_closed_form.py`:
> The RESET equation: r(1 − v) = br · h.
> Combined with h = (1 + √3) br: x² + (2 + √3) x − (1 + √3) = 0 over Q(√3).
> Squaring to eliminate √3 from (x² + 2x − 1) + √3 (x − 1) = 0, taking √3 = −(x² + 2x − 1)/(x − 1), squaring 3(x − 1)² = (x² + 2x − 1)² gives x⁴ + 4x³ − x² + 2x − 2 = 0.

**This is a genuinely closed-form computation.** It depends on the BHML table values feeding the RESET coordinate; those values are visible in BHML's row 9 (`9666777080`) and across the table.

**Recommendation for §3-§4:** the paper should write out the BREATH equation and RESET equation derivations carefully, showing the specific BHML cell counts. This is one page of careful bookkeeping. As written, the proof is folded into the verification script and is not visible in the manuscript.

### 4.2 The 4-core support claim (§2) needs better justification

§2's "Lemma 1" (4-core support of p*) is proven by direct computation: starting from random Dirichlet initial conditions, the iterate F_{1/2}^{20}(p) has |p_5* + p_6*| < 10⁻¹² and stays at machine zero thereafter. This is **empirical convergence**, not a structural proof.

For a clean mathematical proof of why the support is exactly the 4-core (with no mass leakage to {B, S} = {5, 6}), the authors should:
- Identify the cells of T and B that produce outputs in {5, 6}.
- Show that, restricted to inputs in the 4-core, neither T̂ nor B̂ produces nonzero output in {5, 6}.

For T: row 0 = `0000000700`, so T(0, j) ∈ {0, 7} for all j. Row 7 = `7777777777`, so T(7, j) = 7 for all j. Row 8 = `0777877777`, so T(8, j) ∈ {0, 7, 8}. Row 9 = `0797377777`, so T(9, j) ∈ {0, 3, 7, 9}. So **T does not produce 5 or 6 from 4-core inputs.** ✓

For B: row 0 = `0123456789` — but the input is not in 4-core, so this isn't relevant. Wait — for the 4-core inputs (a, b) ∈ {0, 7, 8, 9}², we need to check those 16 cells. From BHML rows 0, 7, 8, 9 columns 0, 7, 8, 9:
- B(0, 0) = 0, B(0, 7) = 7, B(0, 8) = 8, B(0, 9) = 9.
- B(7, 0) = 7, B(7, 7) = 8, B(7, 8) = 9, B(7, 9) = 0.
- B(8, 0) = 8, B(8, 7) = 9, B(8, 8) = 7, B(8, 9) = 8.
- B(9, 0) = 9, B(9, 7) = 0, B(9, 8) = 8, B(9, 9) = 0.

So the 16 cells take values in {0, 7, 8, 9}. **B also does not produce 5 or 6 from 4-core inputs.** ✓

Therefore the 4-core is **invariant under both T̂ and B̂** (when supported on the 4-core). This is what justifies starting in the 4-core and staying there. Note this is **a structural invariance**, not an empirical observation. The manuscript should argue this directly rather than appealing to numerical iteration.

A separate question is whether the 4-core is **attracting** for the full Δ⁹ dynamics. The paper appeals to spectral-radius checks for global attraction, which is empirical. This is acceptable for an empirical paper but should be flagged as such.

### 4.3 The "uniqueness of the fixed point" claim

§2's Theorem 2.1 says the fixed point is unique. The proof appeals to Brouwer's fixed-point theorem (degree-2 self-map of compact convex set has a fixed point), but Brouwer gives **existence**, not uniqueness. The uniqueness claim is verified numerically. For a *Math. Comp.* paper this is acceptable; the manuscript should state it as "verified numerically, not proven structurally" — currently it states "uniqueness and convergence are verified numerically" in §2's parenthesis, but then carries through as if uniqueness were established.

### 4.4 The "Privileged-α uniqueness" of Part 1 §"Headline" is undisciplined

§Headline's last paragraph reads:

> "A sweep over α ∈ [0.05, 0.95] with 19 sample points confirms that α = 1/2 is the unique mixing weight in this range at which H*/Br* satisfies a small-coefficient quadratic (|c| ≤ 10) AND R*/Br* satisfies a small-coefficient quartic (|c| ≤ 5)."

A 19-point sweep on a 1-dimensional continuum is a very weak check. The paper doesn't pretend otherwise (§6 admits the empirical nature), but the phrasing in §Headline overstates: "is the unique mixing weight" should be "is the unique sample point in the 19-point sweep." Part 2 sharpens this with PSLQ on a denser grid; the §Headline statement should defer to Part 2 instead of claiming uniqueness on its own.

### 4.5 Part 2's empirical-strength claim is over-stated

§3.2 of Part 2 reads:

> "Theorem 3.2. Among the 17-point Stern-Brocot grid G above, α = 1/2 is the unique rational at which both R_{H/Br}(α) and R_{r/br}(α) are PSLQ-detectable algebraic over Q within (degree ≤ 8, coefficient ≤ 50)."

This is fine. But the §4.2 "Conjecture" is:

> "For every rational α ∈ (0, 1) ∖ {1/2}, the runtime attractor coordinates p_i*(α) are transcendental over Q."

This is a vastly stronger claim than the empirical evidence supports. PSLQ at finite precision and finite degree/coefficient bound cannot distinguish "transcendental" from "high-degree algebraic" or "low-degree algebraic with large coefficients." The authors acknowledge this in §4.1, but then state the conjecture in maximally strong form. **Strength of conjecture should match strength of evidence.** A more measured conjecture would be:

> "For every rational α ∈ (0, 1) ∖ {1/2}, the runtime attractor coordinates p_i*(α) are not algebraic of degree ≤ d and coefficient ≤ c, for moderate d and c."

The "transcendental over Q" version requires structural insight not provided.

### 4.6 The "Conjecture: Galois D_4 of f matches D_4 of ⟨P_56, σ³⟩" implication

§4.3 of Part 2 says:

> "(iii) Dirichlet/Galois cleanup. The closed form 1 + √3 (and the quartic in LMFDB 4.2.10224.1 with Galois D_4) sit in a number field whose Galois group matches the D_4 = ⟨P_56, σ³⟩ symmetry of WP104. At α = 1/2, the runtime DOF and the gauge-symmetry DOF agree on the same Galois group."

This is an aesthetic observation — the dihedral group D_4 appears in two places (Galois group of f, conjectural symmetry group on the so(10) algebra) — but the paper offers no causal connection. The two D_4's are abstract dihedral groups of order 8; many objects have D_4 symmetry. Without structural argument, the parallel is **suggestive but not informative**. For a *Math. Comp.* paper this should be phrased as "we conjecture [structural reason]" or omitted; as is, it overclaims.

---

## §5 — Concerns about scope and motivation

### 5.1 Why these tables T and B?

The single biggest unanswered question for an external reader: **why these specific 10×10 tables?** The paper does not derive T or B from any universal property; they are presented as "the canonical TSML/BHML composition tables on Z/10Z" with reference to FORMULAS_AND_TABLES.md, which is not part of the submission.

For *Math. Comp.*, the result is approximately:
> "For one specific quadratic dynamical system on the 10-simplex, the attractor at α = 1/2 lies in the specific number field LMFDB 4.2.10224.1."

If T and B were constructed by some natural / universal procedure, this would be a valuable contribution: a "natural" route to a specific cataloged number field. As is, T and B look hand-picked, and the result reads as "we built one system, found one number field; here it is." The novelty is unclear.

### 5.2 The "TIG" framework is invoked but not introduced

Throughout, the paper invokes "TIG" (Trinity Infinity Geometry) and references companion papers WP102, WP103, WP104 as `papers/wp102/`, `papers/wp103/`, etc. None of these is a refereed source. The 4-core, 8-magma core, σ-permutation, σ³ — all are TIG-internal terminology. The cover letter cites "J02 (Sanders + Gish 2026, *Algebraic Combinatorics*)" as a companion, suggesting that the foundational paper is in submission elsewhere; if so, this submission depends on the parallel acceptance of J02, which is not under *Math. Comp.*'s control.

### 5.3 The "lens" framework is undefined

Both Part 1 and Part 2 say "lens scope: TSML_SYM," with the 4-core results "lens-invariant." This is referenced to `Atlas/LENS_TAXONOMY_2026-05-06/TABLE_INDEPENDENCE_LEDGER.md §5.2 claim #47`, not part of the submission. **A reader cannot evaluate which results survive the lens choice without this document.** For *Math. Comp.*, the relevant table T must be specified once and not require additional documentation to interpret.

---

## §6 — Concerns about what is genuinely novel

The paper is essentially:

1. **One quadratic dynamical system** with a specific fixed point at α = 1/2 (Part 1, §1-§3).
2. **One number field LMFDB 4.2.10224.1** identified as the field of the attractor coordinates (Part 1, §4).
3. **One PSLQ uniqueness check** showing that 16 other rationals don't yield small-coefficient algebraic relations (Part 2).
4. **One Galois identification** (D_4) of the quartic (Part 1, §4).

Each of these is a finite check. The paper packages them with claims of "structural significance" connected to the (uncited) WP102-WP104 line:

- "TIG's bipartite TSML/BHML structure singles out the same 54-Higgs route…"
- "the runtime DOF and the gauge-symmetry DOF agree on the same Galois group"
- "the integer 13 — appearing in ‖VEV‖² = 13/4, κ_ξ = 13/(4e), and the 26 σ_outer-asymmetric BHML cells — is the same integer in all three places"

These claims are **outside the scope of *Math. Comp.*** and should be excised from the manuscript or moved to a brief "context" remark referencing the WP102-WP104 line. *Math. Comp.* does not publish manifestos; it publishes computational results.

A revised submission focusing **only** on the closed-form attractor + PSLQ uniqueness, with the table T given concretely and the result framed as "one route to LMFDB 4.2.10224.1," might fit *Math. Comp.* if:
- the algebraic derivation of H/Br = 1 + √3 is worked out in the manuscript;
- the 4-core invariance is proven (as in §4.2 above);
- the PSLQ uniqueness is presented as a finite empirical verification, not a transcendence conjecture;
- the connection to "TIG" is reduced to a brief remark.

---

## §7 — Reproducibility

Strengths:
- Verification scripts are present and well-commented.
- mpmath-based PSLQ at user-controlled precision is the right tool.
- Wall-clock under 5 minutes for the full PSLQ sweep is reasonable.
- The supplementary script directory (depth-2/3 primitives, Jacobian checks, LMFDB depth analysis) shows the authors have explored the question extensively.

Concerns:
- Some script paths reference `papers/wp105_closed_form_attractor/` and `papers/wp113_alpha_uniqueness/`, internal-repo paths.
- A clean reproducibility package — one folder, one make-all script, all tables T and B inline — would help.

This part of the submission is generally **strong** and represents the most credible component.

---

## §8 — Recommendation

**Major revisions required, with conditional acceptance possible if revisions are substantive.**

The submission has a genuine mathematical core (the closed-form attractor at α = 1/2; the LMFDB identification; the Q(√3) factorization; the D_4 Galois) that fits *Math. Comp.*'s scope. The PSLQ sharpening is methodologically sound. The Tschirnhaus relation to LMFDB 4.2.10224.1 is verified.

The submission has problems that must be addressed before acceptance:

1. **The proof of Theorem 3.1** is not in the manuscript; it is only in the verification script. The BREATH equation and RESET equation derivations need to be written out explicitly.
2. **The 4-core invariance** must be proven (it follows from a 16-cell check on each table) rather than claimed empirically.
3. **The "TIG" framework, the "lens" formalism, and the references to WP102-WP104** must be excised or made citable. The paper must stand on its own.
4. **The "Conjecture 4.2"** on transcendence must be weakened to match the empirical evidence.
5. **Why these tables?** A motivation for the specific T and B is needed (or a frank acknowledgment that the tables are hand-picked, with the result framed as a case study).
6. **The bundled paper should be tightened**: drop the structural-significance language ("the runtime DOF and gauge-symmetry DOF agree on the same Galois group") that requires a separate paper to evaluate.

If the authors substantially restructure along these lines, a paper of the form **"A finite quadratic dynamical system with attractor in LMFDB 4.2.10224.1, sharpened by PSLQ"** could be accepted. As currently written, it is a good draft attached to a manifesto and depends on a not-yet-published companion (WP102-WP104).

---

## §9 — Specific action items for authors

| Item | Severity | Effort |
|------|----------|--------|
| Write out the BREATH equation derivation in the manuscript (not just the script) | major | low |
| Write out the RESET / quartic derivation in the manuscript | major | low |
| Prove the 4-core invariance from the 16-cell sub-tables (instead of empirical iteration) | moderate | low |
| Excise "TIG", "lens", "operad-DOF", WP102-WP104 references that the paper depends on but cannot cite | major | medium |
| Weaken Conjecture 4.2 from "transcendental" to "no algebraic relation of bounded degree/coefficient" | minor | low |
| Justify or acknowledge hand-picked-ness of T, B | major | medium |
| Fix the §Headline overstatement of 19-point sweep "uniqueness" | minor | low |
| Excise the §4.3 "two D_4's match" speculation, or argue causation | minor | low |
| Verify (numerically or symbolically) the spectral-radius < 1 claim that justifies global attraction | minor | medium |
| Polish reproducibility package (one folder, one Makefile, no external paths) | minor | low |

**Estimated effort to address all major and moderate items: 2-4 weeks of focused work.**

**Disposition:** Major revision. With substantive revisions along the lines above, this paper could be accepted at *Math. Comp.* The mathematical core is sound and the methods are appropriate; the framing needs to be stripped of TIG-internal scaffolding and re-grounded in standard computational-mathematics narrative.

If the revisions cannot strip the TIG framing without losing the paper's identity, the authors should consider *Experimental Mathematics* (PSLQ + closed-form computational sharpening fits that venue) or a more applied venue.
