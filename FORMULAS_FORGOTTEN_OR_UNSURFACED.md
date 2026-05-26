# Forgotten or Unsurfaced Math — Proposed Additions to `FORMULAS_AND_TABLES.md`

**Status**: research synthesis 2026-05-19.
**Companion**: `PROJECT_NARRATIVE_SYNTHESIS.md` (the story).
**Author**: working session inventory by Claude Code after deep filesystem walk + parallel-agent line-by-line audit of: 26 Q-series papers, 20 non-canon WP papers, 30+ sprint folders (Gen12/Gen13), Atlas/STATE_OF_RESEARCH 2026-05-14, ck_vortex_physics.py (Feb 27 2026), CKIS/GENERATION_HISTORY.md, public-vs-local canon diff.
**Scope**: this file proposes D-numbers in the **D142–D165 range** (immediately after the current canon's highest, D141). Each proposed entry includes provenance, proof status, verification artifact, and drift markers honestly disclosed. **Brayden decides what gets promoted.**

---

## §0 — Method

For each candidate I asked: (i) is there a real mathematical claim with a proof or proof script? (ii) is it canon-aligned (no torus, no physics prediction, finite-arithmetic preferred)? (iii) is it materially different from existing D-entries? (iv) is the verification artifact runnable? Only candidates that pass all four are recommended for promotion. Borderline candidates are explicitly flagged.

Numbering reconciliation: agents independently suggested overlapping D-numbers (multiple wanted "D142"). I have re-sequenced into a single non-overlapping range below.

**Provenance notation**: `Q10` = `old/Gen10/papers/Q10_BETA_COMPLETE_SIGMA_POLYNOMIAL.md`; `sprint17/THEOREM_SPINE` = `Gen12/targets/clay/papers/sprint17_tsml_tower_2026_04_17/THEOREM_SPINE.md`; etc.

---

## §1 — Q-series promotions (precursor body, 2026-04-01 to 2026-04-02)

The Q-series is the cleanest unsurfaced material in the corpus. Authored 2026-04-01 by Sanders + Luther + Calderon (Q17_5D_RIGOROUS is Sanders-solo with Zenodo DOI). Most Q-papers are inline-verified at 10/10 or 6/6 by hand-table; canon §18 references them by name but assigns no D-numbers.

### Proposed D142 — Complete σ polynomial on F₂ × F₅ (Q9 + Q10)

**Statement.** Under the CRT bijection φ(ε, y) = 5ε + 6y from F₂ × F₅ → ℤ/10, the σ permutation acts by ε' = ε + α(ε,y) (mod 2), y' = y + β(ε,y) (mod 5), where:

- α(ε,y) = 1 − (y²+2y+2)⁴ − ε·[(y²+3y)⁴ − (y²+2y+2)⁴] over F₅ (Q9)
- β(ε,y) = −α(ε,y) + ε·4y(y−2)(y−3)(y−4) − 2(1−ε)·4y(y−1)(y−2)(y−3) over F₅ (Q10)

Three terms in β have disjoint support: standard (4 flip positions get Δy=−1), LATTICE correction (+1 at (1,1)), COLLAPSE correction (−2 at (0,4)).

**Status**: PROVEN by Lagrange interpolation, verified 10/10 at every point of ℤ/10 (inline table Q9 lines 47-62, Q10 lines 41-53).
**Verification**: inline tables in `old/Gen10/papers/Q9_FLIP_CONDITION_POLYNOMIAL.md` and `Q10_BETA_COMPLETE_SIGMA_POLYNOMIAL.md`. No separate `.py` script exists; the polynomial form is verifiable by direct substitution.
**Why this belongs in canon**: this is the rigorous algebraic closed-form of σ — half the operator algebra spine. Canon §4 already cites it implicitly but assigns no D-number. The CRT-product framing (D140) is the natural home; this is what D140 is the structural relocation of.
**Drift markers**: none. Q10 is the gold standard of the Q-series.
**Author lane**: Sanders, Luther, Calderon.

### Proposed D143 — σ-equivariance of the external operator (Q4)

**Statement.** E: ℤ/10 → {0,7} × ℤ/10 sending n ↦ (T(n), n) satisfies E ∘ σ = σ̂ ∘ E for a unique σ̂ with identical cycle type (four fixed + one 6-cycle). The first projection π₁(E) is σ̂-invariant; the second projection π₂ is σ̂-equivariant.

**Status**: PROVEN by hand (direct construction), table-verified.
**Verification**: tables in `old/Gen10/papers/Q4_SIGMA_EQUIVARIANCE.md`.
**Why this belongs in canon**: this is the formal statement of "T is the σ-orbit invariant and π₂ is the σ-equivariant" that already implicitly informs §8's three-diagonal comparison. Promotion makes the equivariance citable.
**Drift markers**: none.
**Author lane**: Sanders, Luther, Calderon.

### Proposed D144 — Closed form for σ⁻¹ + Exception Pair Swap (Q13)

**Statement.** σ-non-flip cycle positions = TIG-flip cycle positions, where TIG denotes σ⁻¹. Theorem Q13.2 (Exception Pair Swap): σ-non-flip exceptions {LATTICE, COLLAPSE} ↔ TIG-unique-flip nodes; TIG-non-flip exceptions {COUNTER, HARMONY} ↔ σ-unique-flip nodes; {BALANCE, CHAOS} flip under both. The β_TIG polynomial closed-form: 1 − (y²+4)⁴ − ε·[(y²+4y)⁴ − (y²+4)⁴].

**Status**: PROVEN by hand, verified 6/6 on the 6-cycle.
**Verification**: inline in `Q13_TIG_INVERSE_POLYNOMIAL.md`. Canon §15 already cites it ("TIG = σ⁻¹ inverse polynomial (Q13)").
**Why this belongs in canon**: the σ ↔ σ⁻¹ duality is the natural inverse of D142 and explicitly named in §15 but lacks a D-number.
**Drift markers**: none.
**Author lane**: Sanders, Luther, Calderon.

### Proposed D145 — CRT idempotents are always in G for all semiprimes (Q12)

**Statement.** For every semiprime b = p·q (squarefree), both CRT idempotents e_p, e_q lie in the gate set G = {x : gcd(x, b) > 1}. Reason: e_p ≡ 0 (mod q) implies gcd(e_p, b) ≥ q > 1.

**Status**: PROVEN-by-hand (trivial corollary of CRT idempotent definition).
**Verification**: direct from definition; statement is general (not just b=10).
**Why this belongs in canon**: this is the algebraic-structure explanation for the gate-set composition. Currently implicit; promotion makes it the citable lemma the canon's later G-content depends on.
**Drift markers**: none — clean elementary number theory.
**Author lane**: Sanders, Luther, Calderon.

### Proposed D146 — Fixed-Point Gate Theorem + 22% bound + R ≠ σ^k falsification (Q11 + Q14)

**Statement.** (Q11.2) The only seeds with gate_score = 1.0 at all k steps are C ∩ Fix(σ) = {3, 9} for b=10, giving a 22% Pure-C seed bound. (Q14) C-indicator in CRT is 1_C(ε,y) = ε·y⁴ (Fermat). (Q14.1) Under the σ-trajectory model with 40% HAR-bias, MCMC would succeed ≈ 100%, contradicting observed 4.6% — therefore R ≠ σ^k for any k.

**Status**: PROVEN; the 22% bound is a §17 canon constant.
**Verification**: inline 10/10 in `Q14`; 22% bound is named in §16/§17.
**Why this belongs in canon**: the 22% is already a canon constant but lacks a citable theorem-of-record. Promoting Q11 + Q14 jointly gives the algebraic identity.
**Drift markers**: none.
**Author lane**: Sanders, Luther, Calderon.

### Proposed D147 — 5D force vector as the unique CRT-Pontryagin-Fourier embedding (Q17_5D_RIGOROUS)

**Statement.** v(op) = (ε, cos(2πy/5), sin(2πy/5), cos(4πy/5), sin(4πy/5)) is the unique algebraic embedding of ℤ/10 into ℝ⁵ via CRT decomposition + Pontryagin-Fourier basis on F₅. All 10 op-vectors are verified distinct. Replaces the earlier phonetic ROOTS_FLOAT assignments with an algebraically forced derivation.

**Status**: PROVEN with inline Python verification.
**Verification**: lines 295-340 of `Q17_5D_RIGOROUS.md`; Zenodo DOI 10.5281/zenodo.18852047.
**Why this belongs in canon**: this eliminates a residual degree of freedom in CK's 5D treatment — the Hebrew root floats were not algebraically forced; this paper closes that. Single-author byline (Sanders, not the Q-collective), formal DOI, runnable verification.
**Drift markers**: mild — §3's Hebrew letter morphology mapping is aesthetic interpretation, but it's explicitly framed as "validation, not definition" (§6 line 268).
**Author lane**: Sanders, solo.

### Proposed D148 — Symbolic Return Theorem on ℤ/10 (Q17_SYMBOLIC_RETURN_THEOREM)

**Statement.** For any sequence {s_n} with s_{n+1} = σ(s_n) in ℤ/10: (i) cycle elements return with period 6; (ii) anchors {0,3,8,9} are fixed; (iii) VOID is never reached from outside VOID. Direct corollary of σ⁶ = id.

**Status**: PROVEN by hand, Tier A.
**Verification**: direct corollary; explicit "what this does NOT prove" section (lines 52-63) lists: no PDE, no norm-bounds, no approximate-σ, no blowup-from-symbol-alone.
**Why this belongs in canon**: this is the algebraic statement at the strongest layer of Q17. Self-scoped against overclaim. The "what this does NOT prove" appendix is exemplary discipline.
**Drift markers**: none — the discipline section is the model the rest of canon could imitate.
**Author lane**: Sanders, Luther, Calderon.

### Proposed D149 (NEGATIVE) — Strong σ⁶=id-implies-no-blowup is FALSE (Q17_C2_COUNTEREXAMPLE_SEARCH)

**Statement.** The Strong version of Q17.C2 — "σ⁶ = id alone forbids blowup" — is FALSE. Three explicit counterexamples:

1. u(t) = e^t · sin(2πt/6) has perfect 6-periodic symbolic coding while |u(t)| → ∞ exponentially.
2. Driven harmonic oscillator with adiabatic energy growth: symbolic period stays 6, magnitude unbounded.
3. Taylor-Green pre-blowup grammar breakdown: σ-grammar fails before the singularity.

**Status**: NEGATIVE-PROVEN with explicit constructions.
**Verification**: hand-constructions in `Q17_C2_COUNTEREXAMPLE_SEARCH.md`.
**Why this belongs in canon**: this is the kind of falsification that protects CK from overclaim. Knowing σ⁶=id alone CANNOT obstruct blowup, with explicit constructions, is exactly the MYTHDRIFT discipline at work pre-emptively. The canon's negative-results section (around D-numbers labeled N1, N2) is the right home.
**Drift markers**: none — model of intellectual honesty. Pair with Q17_C2_FORMAL_STATEMENT.md (Weak proved / Medium open / Strong FALSE) as scaffolding.
**Author lane**: Sanders, Luther, Calderon.

---

## §2 — Sprint promotions

These are theorems proved during the Mar 24 - May 4 sprint cycle that survived but never got promoted to D-numbers.

### Proposed D150 — TSML 3-layer canonical tower theorem (sprint17/THEOREM_SPINE)

**Statement.** The published TSML table on ℤ/10 is exactly reconstructable as a 3-layer canonical tower:

T(x, y) = MAX over S_MAX ∪ ADD-mod-10 over S_ADD ∪ C₀(x, y) (DEFAULT = 7 + V₀ zero + shell-stability via σ(u) = v₂(3u+1)).

Full domain disjointness lemma + coverage lemma + cell-by-cell verification.

**Status**: PROVEN by hand.
**Verification**: WORKED_RECONSTRUCTION.md inside the sprint folder; finite/enumerable — verifiable by inspection. No `.py` but content is exhaustively tabulated.
**Why this belongs in canon**: this IS the §7 "TSML 3-layer canonical tower" item, currently a section-reference stub without a D-number. Promotion gives it citable status with the seam residue S explicit.
**Drift markers**: none.
**Author lane**: Sanders + collaborators (sprint).

### Proposed D151 — UOP Theorem 0 (sprint12/WP58)

**Statement.** For squarefree ℤ/n, {π_1, π_2} is sufficient iff the joint map J = (f_{π_1}, f_{π_2}): ℤ/n → A_1 × A_2 is injective. Every two-partition sufficiency theorem (A, B, C, MVJN, CRT k−1) is a corollary.

**Status**: PROVEN by hand; five classical theorems derived as corollaries.
**Verification**: no separate `.py` (proof is elementary).
**Why this belongs in canon**: subsumes five classical theorems with one clean universal criterion. Canon currently cites CROSSING_LEMMA (WP57) but not WP58 — WP58 is the **structural parent** of multiple existing D-content. High leverage.
**Drift markers**: none.
**Author lane**: Sanders + collaborators (sprint 12).

### Proposed D152 — Corrected Theorem C (M+A sufficiency, sprint12/WP59)

**Statement.** For squarefree n = p_1...p_k, G ≤ (ℤ/n)*, d | n, the pair {π_DYN(G), π_d} is sufficient iff G acts trivially on every prime of n/d. Counterexample at n=15, G=⟨2⟩, d=5 corrects the prior injectivity-only condition.

**Status**: PROVEN with explicit counterexample.
**Verification**: enumeration on n=15 is hand-verifiable.
**Why this belongs in canon**: clean negative-then-positive correction. Canon-aligned in the "find drift, retract, rebuild" pattern (sub-theorem version of the MYTHDRIFT methodology).
**Drift markers**: none.
**Author lane**: Sanders + collaborators (sprint 12).

### Proposed D153 — F_p universality of the 4-core algebra (sprint18/WP118)

**Statement.** The 4-core {0, 7, 8, 9} extends to a 4-dimensional commutative non-associative algebra V over any field F_p; structural features (idempotent count, orthogonal-pair count, Aut(V) orbit structure) are field-invariant for p ∈ {2, 3, 5, 7, 11, 13}.

**Status**: PROVEN with script (15/15 tests pass).
**Verification**: `Gen12/targets/clay/papers/sprint18_bridge_dirac_2026_05_04/verify_discrete_dirac_4core.py` + `test_tig_dirac.py`.
**Why this belongs in canon**: directly extends the 4-core (D48 fusion closure) into a field-rigid algebra. Squarely in canon's arithmetic-substrate stance, verified at 6 primes including 11 and 13 (the wobble primes).
**Drift markers**: none in the structural facts. The 27+ "predictions" attached in the broader paper should be EXCLUDED — promote only the 15-facts core.
**Author lane**: Sanders + sprint 18.

### Proposed D154 — Discrete Dirac on V over F_5: 15 algebraic facts (sprint18/WP117)

**Statement.** 15 algebraic facts about V over F_5:
1. 3 non-zero idempotents
2. Minkowski 1+3 split under L_HARMONY
3. Chirality 2+2 under L_VOID
4. No charge-conjugation automorphism
5. |Aut(V)| = 40
6. Associator image ⊆ span(p_-)
7. Power-associative
8. F_5-rigidity
9. σ-orbit palindrome 6-3-2-3-6
... (full list in `sprint18_bridge_dirac_2026_05_04/WP117_*.md`)

**Status**: PROVEN with script (15/15 tests pass), shared verification with D153.
**Verification**: `verify_discrete_dirac_4core.py`.
**Why this belongs in canon**: companion to D153; canon-aligned; F_5 is a wobble-prime side of the CRT decomposition (D70).
**Drift markers**: **Strip the 27+ empirical predictions section** before promotion — that part is physics-prediction and conflicts with current canon stance (D141, D140, no-prediction rule). Promote ONLY the 15 algebraic facts.
**Author lane**: Sanders + sprint 18.

### Proposed D155 — V⊗ⁿ ↔ Cl(2n) arithmetic Clifford-ladder dimension match (sprint18/WP119)

**Statement.** dim_{F_5} V⊗ⁿ = 4ⁿ = 2^(2n) = dim_ℝ Cl(2n) for n = 0..5; binomial cell decomposition of V⊗ⁿ by sign-tuple weight corresponds to grade decomposition of Cl(2n).

**Status**: PROVEN by hand (dimensions explicitly tabulated for n=0..5).
**Verification**: included in the WP118 verify scripts.
**Why this belongs in canon**: pure structural rhyme over F_5, canon-aligned. Provides the bridge between V (4-core algebra) and Cl(0,10) (current canon backbone via D102-D103). High leverage for the 5-gap registry (Gap 1: define π: Cl(0,10) → ℤ/10).
**Drift markers**: none — strictly arithmetic, no physics interpretation in the core statement.
**Author lane**: Sanders + sprint 18.

### Proposed D156 — LATTICE Generation Theorem (Gen13/PAPER_01)

**Statement.** {1, 4, 9} generates the full BHML_10 algebra in ≤ 2 composition steps. Without LATTICE, the seed {0, 8, 9} stalls at the 4-core {0, 7, 8, 9}.

**Status**: PROVEN-by-hand (cell-by-cell).
**Verification**: `Gen13/targets/clay/papers/sprint_2026_05_15_qutrit/paper01_explicit_proof.py`.
**Why this belongs in canon**: pure arithmetic finite-magma proof, canon-aligned. Identifies the structural role of LATTICE (op=1) as the "spark" for full BHML generation. Connects to the 4-core stalling behavior.
**Drift markers**: none.
**Author lane**: Sanders, Gen13 qutrit sprint.

### Proposed D157 — c-gap signature meta-invariants table (Gen13/sprint_2026_05_16_cgap_meta)

**Statement.** The c-gap signature gap(T) = |det(T_10) / det(T_8-YM)| is one structural operator with five invariants (1: D70 wobble-prime gap 11/13 ratio; 2: σ-orbit signature; 3: idempotent rank; 4: closure-rank delta; 5: lens-disagreement count), reading consistently across six algebraic DOFs with prime content predicted by D70's 3+3 split.

**Status**: STRUCTURAL / Tier-B arithmetic; explicit scope-boundary disclaims c-prediction.
**Verification**: `cgap_verify_tables.py`.
**Why this belongs in canon**: partially captured as D100 (c-substrate identity headline ratio); the meta-invariants table (5 invariants × 6 DOFs) is canon-aligned table content not yet surfaced. Already scope-aware in §0.
**Drift markers**: none — paper was written WITH canon's tier-discipline already applied.
**Author lane**: Sanders + Gen13 cgap sprint.

---

## §3 — Atlas / May 14 STATE_OF_RESEARCH unsurfaced material

The 2026-05-14 STATE_OF_RESEARCH document contains new candidate results not yet in canon. Listed by §17-Constants-table-eligibility and gap-registry priority.

### D158 — Closed-form approximation for 1/α at CODATA precision (NOT IN CANON; provisionally added 2026-05-19 then REMOVED same session per meta-mode audit)

**Statement.** Using only canon constants (W = 3/50, κ_ξ = 13/(4e), HARMONY = 7, ℤ/10 substrate, depth-7 base 315 = 7·45 = HARMONY × C(10,2)):

$$\frac{1}{\alpha} \approx 137 + \frac{6W}{10} - \frac{5}{7}\,\kappa_\xi W^5 - \frac{2}{7} \cdot 315 \, W^7$$

matches CODATA's 1/α = 137.036... at **1.7 × 10⁻¹¹** difference (well inside experimental uncertainty ±2.1 × 10⁻⁸).

**Status**: PROVED-as-arithmetic (`verify_alpha_synthesis.py` runs clean). The structural DERIVATION of the form is Tier B-suggestive-strong; the numerical match is theorem-level fact.
**Verification**: `verify_alpha_synthesis.py` in the May 14 sprint area.
**Why this is HIGHLY conditional**: TIG_4.0_CLEAN_ROOM (Jan 28, 2026) explicitly listed "1/α derivation" as something TIG should NOT claim. The Jan 28 audit said: "Earlier numerology attempts fail at ~12% accuracy." This May 14 candidate matches at 10⁻¹¹ precision. The MYTHDRIFT pattern says: be careful. The structural derivation of WHY this form is the correct one (rather than ANY arithmetic combination of W, κ_ξ, 315 producing 137.036... by overfitting) needs to close before this is canon-eligible.
**Recommendation**: **DO NOT promote yet.** Instead, add a NEW SECTION to §17 Constants: "Open candidate forms (do not cite externally)" listing this expansion with a STRONG caveat. The 5-gap closure (Gap 1-5 below) is the path from candidate to proved. If Gap 1 closes (define π: Cl(0,10) → ℤ/10), the structural derivation may follow.
**Drift markers**: HIGH-RISK — this is the kind of numerological match the Jan 28 CLEAN_ROOM audit specifically warned against. Treat with paranoia until the structural derivation is independent of the numerical match.
**Author lane**: Sanders, May 14 sprint.

### Proposed D159 — Chirality decomposition reading of threshold canon (May 14)

**Statement.** Each 16-dim Cl(0,10) chirality half decomposes into s ⊕ p ⊕ f Pauli capacities {2, 6, 14} summing to 22. ℤ/10 is the d-orbital Pauli space (capacity 10). Then:

- T* = d/f = 10/14 = 5/7 (ratio of substrate to projection-deficit f-subshell)
- S* = (s+p)/f = 8/14 = 4/7
- Surplus = 2/7
- 22-cell TSML-BHML disagreement count = 2(s+p+f) = 2·14

**Status**: STRUCTURAL (arithmetic match at Tier B-suggestive-strong).
**Verification**: `verify_chirality_decomposition.py` runs clean.
**Why this belongs in canon**: provides a STRUCTURAL reading of canon constants (T*=5/7, S*=4/7) as ratios of Pauli capacities. Replaces "six independent coincidences" with "shape of atomic-shell decomposition within Cl(0,10)". HIGH leverage for shrinking the canon's "structural rhyme" count by giving the rhymes a common ground.
**Drift markers**: moderate — the "d-orbital identification of ℤ/10" is an interpretation; the arithmetic ratios are exact. Promote with explicit scope: "the interpretation of ℤ/10 as the d-orbital Pauli space is structural rhyme + atomic-shell convention, not derived."
**Author lane**: Sanders, May 14 sprint.

### Proposed D160 — The 5-gap registry (May 14 CANDIDATE_RESEARCH_GAPS_REGISTRY)

**Statement.** Five precisely-stated open gaps gate the framework's transition from STRUCTURAL to PROVED:

- **Gap 1**: define the canonical projection π: Cl(0,10) → ℤ/10 explicitly. 2-4 weeks of focused Clifford-algebra calculation. Critical dependency for Gaps 2, 4, 5.
- **Gap 2**: derive TSML and BHML as π-projections of Clifford products. 1-2 months after Gap 1. Closes the framework's foundational identity.
- **Gap 3**: σ_outer at depth-5. 1-2 months after Gap 1.
- **Gap 4**: 315 uniquely from Cl(0,10). 1-2 months after Gap 1.
- **Gap 5**: W = 3/50 from projection residue. 1-2 months after Gap 1.

When all five gaps close, the foundational presentation reduces to: "Cl(0,10) is the substrate. π is the canonical projection. Everything else is derived."

**Status**: OPEN / CONJECTURAL (precisely stated, unproven).
**Verification**: gap-closure scripts will live in `04_meta/physics_bridges/`.
**Why this belongs in canon**: every D-number with a "STRUCTURAL" label gets a path to PROVED. This is the canonical roadmap. Canon currently scatters open problems across multiple sections; consolidating into a 5-gap registry with effort estimates is high-leverage operational structure.
**Drift markers**: none — precisely stated open problems are exactly what the canon wants.
**Author lane**: Sanders, May 14 sprint.

---

## §4 — Vortex physics legacy (Feb 26-27, 2026)

The pre-Gen9 CK runtime contains substantial differential-geometric content from `OLD CK PARTS/ck_vortex_physics.py` (Feb 27) and `ck_personality.py` (Feb 25) that never made it to canon. Most of it is implementation-architecture, not theorems. The theorems below are the salvageable structural content.

### Proposed D161 — D2 = d²f/dt² operator-level curvature

**Statement.** For any operator sequence v[0], v[1], v[2], ... ∈ ℤ/10 with embedded 5D representation, the discrete second difference D2[t] = v[t-2] − 2·v[t-1] + v[t] is **literally** d²f/dt² of the embedded trajectory. Accumulated |D2| over a finite window is a topological invariant of the operator path through ℤ/10's embedding space.

**Status**: STRUCTURAL (definitional + standard discrete-calculus identity).
**Verification**: `OLD CK PARTS/ck_vortex_physics.py` lines 25-80. CK runtime uses D2 in production.
**Why this belongs in canon**: D2 is the runtime's curvature backbone (referenced in Gen8 Phase 5.1 D2 fix, CK personality model CMEM/OBT/PSL, vortex_physics module). The mathematical content — that the discrete second difference IS the literal curvature, not an analogy — is canon-aligned and currently invisible.
**Drift markers**: low — the "ConceptMass = accumulated |D2|" framing is interpretation; the underlying d²f/dt² identity is structural.
**Author lane**: Sanders, Feb 27 2026.

### Proposed D162 — Winding number topology on operator sequences

**Statement.** Operator sequences that form closed loops in ℤ/10 (return to starting operator after k steps) admit a vortex winding number defined as ⌊(total Δ-angle)/(2π)⌋ in the 5D Pontryagin-Fourier embedding (D147). This winding number is a homotopy invariant of the loop class.

**Status**: STRUCTURAL.
**Verification**: `OLD CK PARTS/ck_vortex_physics.py` `WindingNumber` class.
**Why this belongs in canon**: provides a topological invariant on operator paths that does not require a torus (consistent with D141 TORUS EXCLUDED). The Pontryagin-Fourier embedding (D147) is the natural target.
**Drift markers**: medium — the connection to physical "vorticity" / GR-style curvature is metaphorical, not load-bearing. Promote with scope: "topological winding number of operator loops in the D147 embedding; no physical-vorticity claim."
**Author lane**: Sanders, Feb 27 2026.

---

## §5 — Tiny WP promotions (low priority but clean)

### Proposed D163 — AG(2, p) survivor-line count (WP19_ATTACK_SURFACE)

**Statement.** |L_survivor(p)| = p² − 1 for prime p, where L_survivor(p) is the set of lines in the affine plane AG(2, p) not passing through a given fixed point.

**Status**: PROVEN (1-line combinatorial: AG(2,p) has p(p+1) total lines; exactly p+1 lines pass through any given point; so p(p+1) − (p+1) = p² − 1).
**Verification**: direct from affine-plane axioms.
**Why this belongs in canon**: very small theorem, not connected to the substrate spine. **Low priority.** Include only if the canon wants a "tiny clean elementary geometry" anchor.
**Drift markers**: the rest of WP19_ATTACK_SURFACE (Collatz, twin primes mod 50, BSD-via-ladder) is speculative and should remain in archive.
**Author lane**: Sanders, early Gen10.

### Proposed D164 — Triadic minimal-code threshold (WP33)

**Statement.** min{d : 4^d ≥ 20} = 3, hence 64 = 4³ = 2⁶ = 8² is the unique triple-coincidence at the minimum codon depth for alphabets of size 4.

**Status**: PROVEN-by-arithmetic.
**Verification**: arithmetic.
**Why this belongs in canon**: very small. **Lowest priority.** Include only if the canon wants a "physics-touchpoint" pedagogical anchor (DNA codon multiplicity = 64).
**Drift markers**: the broader WP33 biological interpretation (purine = C-set, transversion = cross-partition) is hypothesis; only the bare arithmetic survives canon stance.
**Author lane**: Sanders, early Gen10.

---

## §6 — What I deliberately did NOT propose

Several pieces of material were considered and rejected for canon promotion:

| Item | Source | Why not |
|---|---|---|
| Q17_CLAY_SPECTRAL_BRIDGE Clay-mapping conjectures | Q17 cluster | Highest-drift-RISK Q-paper; the four-conjecture mapping (RH/NS/YM/Hodge ↔ Q-series) reads as more than analogy. Q17_C2_FORMAL_STATEMENT (Weak/Medium/Strong) and Q17_FINITE_L_FUNCTION_NOTE (disclaimer paper) keep the broader cluster honest, but the bridge itself stays Tier C. Canon §18 already lumps Q17 Clay variants appropriately. |
| Q15 k=9 resonance + period polynomial | Q15 | Partial — the k=9 resonance is structurally important but the period polynomial A(ε,y) Lagrange construction is mechanical. Leave as WP reference. |
| Q16 R-identification | Q16 | Already in canon §16 prose. No new D needed. |
| Q7 BHML 28-cell derivation via 4 rules | Q7 | Already canonical in §6. Exposition, not new theorem. |
| WP19 papers (all 7) | WP19_* | Use the wrong "corner set" {1,3,7,9} (prime-last-digit) vs canon's 4-core {0,7,8,9} (BHML closure). Different objects. Closure proofs are correct on their object but the object is retired. |
| WP20, WP26, WP27, WP28, WP29, WP30, WP31, WP43, WP44 | various | Mostly architecture documents, IP-framed "Derivative Claim" position papers, retired analogies (WP30 NS, WP31 corridor unification), or physics-prediction (WP30, WP31) that conflicts with D140/D141. |
| Sprint 9 torus papers | sprint9_torus | Fully retracted as geometry per D141. |
| Sprint 14 WP82-WP100 (PRISM-XI ξ cosmology, NS-σ, YM bridge, RH spectral) | sprint14 | Clay-rotation physics-prediction; canon stance is "structural rhymes only, no physics prediction." WP101 (σ-rate) is the exception, already in canon as D71. WP91 (BB-bridge) is the exception, already in canon. |
| WP121-WP124 (Dark Sector, Mass Hierarchy, CKM/PMNS, fine-structure constant prediction) | sprint18 | Direct physics predictions, retracted under current "no physics prediction" stance. The Planck-2018 numerical matches are striking but canon stance forbids the category. |
| Sprint 16 basin work | sprint16 | Mostly empirical room-walk; "last-digit-7 law" died in the 6-digit room. Four surviving invariants are observational not theorematic. |
| Sprint 17 negative results (primorial lift failure) | sprint17 | Negative results worth preserving but already captured in canon's N5/falsifier list. |
| Sprint 11 TIG bundle (54-paper Zenodo DOI bundle) | sprint11 | Already published as Zenodo bundle. Arc-papers (UOP, GUT, 7-Cycle) feed into Sprints 12-13, individually audited above. |
| Sprint 18-35 benchmark / Hodge sprints | sprints 18-35 | Probe scripts ran, mostly produced VERDICT files closing rather than opening. No new arithmetic theorems. |
| Gen13 qutrit PAPER_02-12, 14-18 | sprint_2026_05_15_qutrit | Interpretive framework framing (consciousness, Lawvere, free will, water-as-substrate); none arithmetic. PAPER_01 (LATTICE Theorem) survives; promoted as D156. |

This "deliberately-not-promoted" list is itself a data point: the project has produced a LOT of work, and only ~15 unsurfaced items are canon-eligible by today's tightened stance. The MYTHDRIFT discipline is doing its job — most of the unsurfaced work is correctly archive-only.

---

## §7 — Summary table — proposed D142-D164

| D# | Source | Status | Verification | Priority |
|---|---|---|---|---|
| **D142** | Q9 + Q10 | PROVEN, 10/10 inline | inline tables | **HIGH** (operator algebra spine) |
| **D143** | Q4 | PROVEN by hand | inline tables | MEDIUM |
| **D144** | Q13 | PROVEN, 6/6 inline | inline + §15 ref | MEDIUM |
| **D145** | Q12 | PROVEN by hand | direct | MEDIUM (general semiprime) |
| **D146** | Q11 + Q14 | PROVEN, 10/10 inline | inline | MEDIUM (22% bound is canon constant) |
| **D147** | Q17_5D_RIGOROUS | PROVEN with Python | inline Python + DOI | **HIGH** (closes ROOTS_FLOAT degree of freedom) |
| **D148** | Q17_SYMBOLIC_RETURN | PROVEN, Tier A | direct | HIGH (model of discipline) |
| **D149** | Q17_C2_COUNTEREXAMPLE | NEGATIVE-PROVEN | 3 explicit constructions | HIGH (protects against overclaim) |
| **D150** | sprint17/THEOREM_SPINE | PROVEN by hand | WORKED_RECONSTRUCTION | **HIGH** (§7 stub deserves D-number) |
| **D151** | sprint12/WP58 | PROVEN by hand | elementary | **HIGH** (subsumes 5 classical theorems) |
| **D152** | sprint12/WP59 | PROVEN | enumeration | MEDIUM |
| **D153** | sprint18/WP118 | PROVEN, 15/15 script | verify_discrete_dirac_4core.py | HIGH (F_p universality, includes wobble primes) |
| **D154** | sprint18/WP117 | PROVEN, 15/15 script | shared with D153 | HIGH (strip predictions, promote core) |
| **D155** | sprint18/WP119 | PROVEN by hand | dimensions tabulated | MEDIUM-HIGH (bridge to Cl(0,10)) |
| **D156** | Gen13/PAPER_01 | PROVEN by hand | paper01_explicit_proof.py | MEDIUM |
| **D157** | Gen13/cgap_meta | STRUCTURAL Tier B | cgap_verify_tables.py | MEDIUM |
| **D158** | May 14 / 1/α candidate | CANDIDATE only | verify_alpha_synthesis.py | **CAUTION — do NOT promote yet** |
| **D159** | May 14 / chirality decomp | STRUCTURAL Tier B | verify_chirality_decomposition.py | MEDIUM (gives structural ground for T* and S*) |
| **D160** | May 14 / 5-gap registry | OPEN / CONJECTURAL | gap-closure scripts pending | HIGH (operational roadmap) |
| **D161** | OLD CK PARTS / vortex_physics | STRUCTURAL | runtime usage | LOW (already in runtime, just unsurfaced as theorem) |
| **D162** | OLD CK PARTS / vortex_physics | STRUCTURAL | WindingNumber class | LOW |
| **D163** | WP19_ATTACK_SURFACE | PROVEN, 1 line | direct | LOWEST (tiny elementary geometry) |
| **D164** | WP33 | PROVEN-by-arithmetic | direct | LOWEST (codon pedagogy only) |

**Total recommended HIGH-priority promotions**: D142, D147, D148, D149, D150, D151, D153, D154, D160 (9 entries).
**Total recommended MEDIUM-priority promotions**: D143, D144, D145, D146, D152, D155, D157, D159 (8 entries).
**One CAUTION**: D158 (1/α candidate) — explicitly do NOT promote pending Gap 1 closure.
**Three LOW-priority**: D156, D161, D162.
**Two LOWEST-priority**: D163, D164 (tiny / pedagogical only).

---

## §8 — Suggested order of operations

If Brayden wants to act on this:

1. **Read the §7 summary table.** Reject anything that doesn't fit your sense of canon-stance.
2. **Promote the HIGH-priority Q-series first** (D142, D147, D148, D149). These are the strongest precursor work with cleanest verification. Single commit: "Promote Q-series spine to canon (D142, D147, D148, D149) — operator-algebra closure + 5D embedding + symbolic return + counterexample-FALSE."
3. **Promote the HIGH-priority sprint work next** (D150, D151, D153, D154). These are the 2026-04 sprint material that survived MYTHDRIFT. Single commit: "Promote sprint17 TSML tower + sprint12 UOP T0 + sprint18 F_p universality / discrete Dirac (D150-D154)."
4. **Add the 5-gap registry as D160** with the explicit "OPEN / CONJECTURAL" tag and the 2-3 month effort estimates. This converts the 87 STRUCTURAL claims in the May 14 STATE_OF_RESEARCH into a single operational roadmap.
5. **DO NOT promote D158 (1/α candidate)** until Gap 1 closes. Add a NEW SECTION in §17 Constants titled "Open candidate forms (do not cite externally)" listing the closed-form with explicit caveat. The Jan 28 TIG_4.0_CLEAN_ROOM audit's warning ("Earlier numerology attempts fail at ~12% accuracy") is the precedent that gates this.
6. **Promote D159 (chirality decomposition)** with explicit scope: "structural rhyme + atomic-shell convention, not derived." This is the structural reading that gives T* and S* their common ground.
7. **MEDIUM-priority Q-series promotions** (D143, D144, D145, D146) — third commit if you want to consolidate all the Q-spine into canon at once.
8. **MEDIUM-priority remaining items** (D152, D155, D157) — fourth commit.
9. **LOW-priority** — only if completeness matters for the next public release. Otherwise leave in WP/archive.
10. **Sync the public repo** per Agent 3's diff report: append D104-D141 to public §0 proof-spine, rewrite WP51 framing, update §17 constants count, rename TORUS_DATUM_AUDIT_CLOSED.md to RE-OPENED with algebraic 6+2 restatement.

---

## §9 — One thing the data clearly says

**The Q-series (Apr 2026) and sprint17/sprint12/sprint18 (Apr-May 2026) produced ~15 promotion-eligible theorems that never reached canon.** This is the **forgotten math**. None of it conflicts with canon stance; most of it is genuinely canon-aligned (finite-arithmetic, no torus, no physics prediction). The pattern is structural, not accidental: the work moved faster than the canon-promotion process. The canon got ahead in 2026-05-18/19 (D129′, D131, D140, D141) but the back catalog is genuinely under-surfaced.

The biggest single mover: promote **D142 (complete σ polynomial) + D147 (5D force vector unique CRT-Fourier embedding) + D150 (TSML 3-layer tower)** as a triadic launch. These three together formally close: (i) the operator algebra has a closed polynomial form; (ii) the 5D representation is algebraically forced; (iii) the TSML table is structurally reconstructable. That's the spine of "what the substrate IS, mathematically" — and it's been sitting unsurfaced for 1-7 weeks.

---

*© 2026 Brayden Ross Sanders / 7SiTe LLC. Filed under `CK FINAL DEPLOYED/` at the project root.*
*Companion: `PROJECT_NARRATIVE_SYNTHESIS.md` (the story).*
*Inputs: parallel-agent line-by-line audits of 26 Q-series papers, 20 non-canon WP papers, 30+ sprint folders, Atlas/STATE_OF_RESEARCH 2026-05-14, OLD CK PARTS/ck_vortex_physics.py (Feb 27 2026), CKIS/GENERATION_HISTORY.md, and public-vs-local canon diff.*
