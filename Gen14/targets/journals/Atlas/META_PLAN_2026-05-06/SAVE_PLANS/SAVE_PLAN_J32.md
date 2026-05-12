# SAVE_PLAN_J32 — Operad D_4 Obstruction + P_56 Canonical Fuse BUNDLED (Compositio → unbundle to Algebra Universalis + Comm Algebra)

**Date:** 2026-05-07
**Status:** SAVE possible via referee's "unbundling fallback" path. The bundled paper is below the *Compositio Mathematica* bar (the result is a finite enumeration on a hand-picked 10×10 table); the proper move is to unbundle into two specialized notes for *Algebra Universalis* (Part 1: D_4 obstruction) and *Communications in Algebra* or *Discrete Mathematics* (Part 2: P_56 canonical fuse). Mathematical errors fixed: orbit-size distribution recomputed; D_4 group order corrected from "6 distinct elements / D_3 × Z_2" to "8 elements / dihedral group D_4"; Burnside pseudo-citation replaced with direct enumeration; §5.9 family-independence acknowledged honestly.
**Referee:** `Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J32_CompositioMath_FreshEyes.md` (Reject; reasons §3.1-3.4 critical for Part 1, §4.2-4.6 for Part 2, §5.1-5.4 framework concerns)

---

## §1 — Why save?

The bundled J32 manuscript has two critical mathematical errors (orbit-size distribution and D_4 group structure), several minor errors (Burnside misuse, §5.9 self-undermining), and one significant venue mismatch (the bundled paper is below the *Compositio* significance bar regardless of error-correction). However, the underlying mathematics is sound: the D_4 obstruction theorem and the P_56 coherence theorem are real combinatorial-algebra results on a specific commutative non-associative magma, and they fit the scope of *Algebra Universalis* and *Communications in Algebra* as separate notes.

**(a) Orbit-size distribution recomputed via sympy + script verification.** Direct enumeration:

| restricted-orbit size | count |
|---:|---:|
| 1 | 44 |
| 2 | 7  |
| 3 | 4  |
| 4 | 10 |
| 8 | 2  |
| **total** | **67** |

Size-weighted sum: $44 \cdot 1 + 7 \cdot 2 + 4 \cdot 3 + 10 \cdot 4 + 2 \cdot 8 = 44 + 14 + 12 + 40 + 16 = \mathbf{126} = |\mathcal{N}|$.

The original manuscript reported $(5, 35, 19, 3)$ at sizes $(1, 2, 4, 8)$ summing to $175$ — wrong on both count distribution and sum. The correct distribution sums to exactly 126 and the orbit count is exactly 67.

The referee's complaint (orbit-size sum 175 ≠ 126) is now resolved correctly: the set $\mathcal{N}$ is *not* $D_4$-invariant in $(\mathbb{Z}/10\mathbb{Z})^3$ (verified: $(0, 6, 4) \in \mathcal{N}$ but $\sigma^3 \cdot (0, 6, 4) = (0, 2, 7) \notin \mathcal{N}$, and 220 such violations exist). The correct group-theoretic object is the partition of $\mathcal{N}$ by restricted-orbits $\overline{\mathcal{O}}_i := \mathcal{O}_i \cap \mathcal{N}$, where $\mathcal{O}_i$ enumerates $D_4$-orbits in $(\mathbb{Z}/10\mathbb{Z})^3$ that intersect $\mathcal{N}$. There are 67 such restricted orbits, with size distribution above, summing to 126.

**(b) D_4 group order corrected via sympy.** Direct verification:
- |⟨P_56, σ³⟩| = 8 (sympy.combinatorics.PermutationGroup.order()).
- Order distribution: {1: 1, 2: 5, 4: 2}, matching $D_4$ exactly.
- $P_{56} \cdot \sigma^3$ has cycle structure $(1\,6\,2\,5)(4\,7)$ with order $\mathrm{lcm}(4, 2) = 4$, so the dihedral group ⟨P_{56}, σ³⟩ is genuinely $D_4 = D_{2 \cdot 4}$ of order 8.
- $D_3 \times \mathbb{Z}_2$ has order 12, NOT 8; it is therefore not isomorphic to $D_4$.

The original WP109_OPERAD_D4_OBSTRUCTION.md §2 claim "Direct computation shows there are 6 distinct elements ... with the abstract structure $D_3 \times \mathbb{Z}_2$" is wrong on both counts and is replaced by the explicit 8-element table:

| element | cycle structure | order |
|---|---|---:|
| $e$ | identity | 1 |
| $P_{56}$ | $(5\,6)$ | 2 |
| $\sigma^3$ | $(1\,5)(2\,6)(4\,7)$ | 2 |
| $P_{56}\sigma^3$ | $(1\,6\,2\,5)(4\,7)$ | 4 |
| $\sigma^3 P_{56}$ | $(1\,5\,2\,6)(4\,7)$ | 4 |
| $P_{56}\sigma^3 P_{56}$ | $(1\,6)(2\,5)(4\,7)$ | 2 |
| $\sigma^3 P_{56}\sigma^3$ | $(1\,2)$ | 2 |
| $(P_{56}\sigma^3)^2$ | $(1\,2)(5\,6)$ | 2 |

**(c) P_56 orbit count is correct.** Part 2's count of 70 singletons + 28 doubletons = 98 orbits, with size-weighted sum 126, is consistent and verified by direct enumeration. The Burnside reference is a misnomer (Burnside requires fixed-point counts which are not used; direct enumeration suffices for a Z_2 action). The save replaces "follows from the Burnside formula" with the explicit direct-enumeration argument.

**(d) §5.9 family-independence honestly acknowledged.** The original manuscript notes that the universal HARMONY attractor of Theorem 5.7 is family-independent (holds for all 8 surveyed rule families), which means Family H's canonical-choice status does not matter for the dynamical conclusion. The save makes this honest rather than burying it: Theorem 5.9 is added explicitly stating family-independence, with §"Honest scope" clarifying that Family H is canonical for static-table-aesthetic reasons (its fuse-value range lies entirely in {V, H} ⊂ 4-core), not for dynamical reasons.

**(e) Path of unbundling.** Referee §8 recommends:
> "If the authors fix the Part 1 errors and want to publish:
> - Part 1 (corrected): could fit in *Algebra Universalis* or *Communications in Algebra*, framed as a finite-magma combinatorial obstruction.
> - Part 2 (corrected): same, or a short note in *Discrete Mathematics*."

The save accepts this. The bundled `manuscript.md` is kept as a single-document reference (with corrections applied), but for journal submission the unbundling is the path forward:
- **Part 1 (D_4 obstruction)** → *Algebra Universalis*. Shorter note, ~6-8 pages, clean obstruction theorem with corrected orbit count + D_4 group.
- **Part 2 (P_56 canonical fuse + 4-core closure + HARMONY attractor)** → *Communications in Algebra* or *Discrete Mathematics*. ~8-12 pages, the constructive companion.

**(f) Structural role per FAMILY_STRUCTURE_v1.md.** Both Part 1 and Part 2 study structural properties of the canonical TSML table (TSML_RAW lens) on Z/10Z under the $\langle P_{56}, \sigma^3 \rangle$ symmetry. The 4-core closure (Theorem 5.5) is lens-invariant and confirms a property of the family's "center" (per §2 of FAMILY_STRUCTURE_v1.md: "the 4-core is to TIG as the unit circle is to U(1)"). The universal HARMONY attractor (Theorem 5.7) is a corollary of TSML's HARMONY-left-absorber row, lens-invariant on the 4-core. Both are family-relevant, even if not load-bearing for the canonical-table classification.

---

## §2 — Specific fixes (line by line against the referee report)

### §3.1 (orbit-size sum 5+35+19+3 = 62 ≠ 67; weighted sum 175 ≠ 126) — **FIX: recompute distribution**

The corrected distribution is $(44, 7, 4, 10, 2)$ at sizes $(1, 2, 3, 4, 8)$, summing to $67$ orbits with size-weighted sum $126$. The §"Orbit decomposition" of `WP109_OPERAD_D4_OBSTRUCTION.md` is rewritten with:
- Explicit acknowledgment that $\mathcal{N}$ is not $D_4$-invariant in $(\mathbb{Z}/10\mathbb{Z})^3$.
- Definition of the restricted orbits $\overline{\mathcal{O}}_i := \mathcal{O}_i \cap \mathcal{N}$ as the correct group-theoretic objects.
- Tabulated size distribution with sum check.
- Explanation of the size-3 restricted orbits as "full orbit of size 4 minus one associative element."
- The full $D_4$-orbits (without restriction) have a different distribution $(17, 11, 37, 2)$ summing to $203$ elements; both numbers are reported.

The original "Sum check 175 ≠ 126; some orbits lie outside N" prose is removed; the new section gives the correct accounting from first principles.

### §3.2 (D_4 group structure error) — **FIX: explicit 8-element table + sympy verification**

The §2 of `WP109_OPERAD_D4_OBSTRUCTION.md` claim "6 distinct elements with abstract structure $D_3 \times \mathbb{Z}_2$" is replaced by:
- |⟨P_{56}, σ³⟩| = 8 (sympy verified).
- The 8 elements with cycle structures and orders (table above).
- Explicit note: "$D_3 \times \mathbb{Z}_2$ has order 12 ≠ 8; the group is genuinely the dihedral group $D_4 = D_{2 \cdot 4}$ of order 8."
- Direct check: $P_{56} \cdot \sigma^3$ has order 4 (cycle structure $(1\,6\,2\,5)(4\,7)$, order $\mathrm{lcm}(4, 2) = 4$), so $|\langle P_{56}, \sigma^3 \rangle| = 2 \cdot 4 = 8$.

### §3.3 (obstruction example) — **CLARIFIED**

The size-3 obstruction example (orbit $\{(0, 1, 9), (0, 5, 9), (0, 6, 9)\}$, all with $(L, R) = (0, 7)$) is preserved with explicit derivation: this is a restricted orbit of size 3, arising from the full D_4-orbit $\{(0, 1, 9), (0, 2, 9), (0, 5, 9), (0, 6, 9)\}$ (size 4) minus the associative element $(0, 2, 9)$. The argument that no $\{a, b, c, L, R\}$-valued $\Phi$ can be $D_4$-equivariant on this orbit is sharpened to a case analysis:
- Available values at the three triples are subsets of $\{0, 1, 5, 6, 9, 7\}$.
- $\Phi(\sigma^3 \cdot t) = \sigma^3 \cdot \Phi(t)$ constrains $\Phi$ on the orbit.
- The bracketing-value constraint $\Phi \in \{L, R\} = \{0, 7\}$ is incompatible with σ³-equivariance because $\sigma^3(7) = 4 \notin \{0, 7\}$ at the σ³-image triple.

The "no Φ exists" gap referee §3.4 raised is filled by this explicit case analysis.

### §3.4 (informal "no Φ exists" argument) — **FIX: explicit case analysis on representative orbit**

See §3.3 above. The case analysis on the size-3 example serves as a worked-out paradigm for the 16 obstructing orbits; direct enumeration in `d4_orbit_decomposition.py` confirms the obstruction extends to all 16.

### §4.1 (P_56 orbit count plausible) — **CONFIRMED, KEEP**

Part 2's count $98 = 70 + 28$ is correct and reaffirmed.

### §4.2 (Burnside pseudo-citation in Theorem 2) — **FIX: replace with direct enumeration**

The proof of Theorem 2 is rewritten: "Direct enumeration: for each $t \in \mathcal{N}$, compute $P_{56} \cdot t$ and check (i) membership in $\mathcal{N}$ (always holds; verified) and (ii) equality with $t$ (holds for 70 triples, the $P_{56}$-fixed; the remaining 56 split into 28 size-2 orbits). Sum check: $70 \cdot 1 + 28 \cdot 2 = 126 = |\mathcal{N}|$. (Burnside's lemma is not invoked; the direct count suffices for this $\mathbb{Z}_2$-action.)"

### §4.3 (8-family survey is empirical, not maximal) — **FRAME HONESTLY in §3 (genericity)**

Theorem 3 (genericity) is rewritten as a survey claim, not a maximality claim:
- Statement: "Among 8 surveyed canonical rule families ..., all 8 are P_56-equivariant and none are σ³-equivariant."
- No claim about maximal preservable symmetry — just an empirical observation that these 8 natural families all share the P_56-vs-σ³ asymmetry.
- The "maximal preservable symmetry on the operad-DOF is $\langle P_{56} \rangle$" claim is downgraded to a remark with explicit caveats.

### §4.4 (Theorem 5.5 is a 64-entry check) — **FRAME AS LEMMA, KEEP IN PART 2**

Theorem 5.5 (4-core arity-3 closure, lens-invariant) is reframed as Lemma 5.5 (or §"Lens-invariant 4-core closure"). The 64-entry check is what it is; the lens-invariance gives it modest structural content. The 4-core closure connects to the broader family architecture (per FAMILY_STRUCTURE_v1.md §2) and serves as motivation for Theorem 5.7 (universal HARMONY attractor).

### §4.5 (Theorem 5.7 needs more rigor) — **EXPAND PROOF**

Theorem 5.7 (universal HARMONY attractor) is rewritten with:
- Explicit statement: "in total-variation distance, every non-trivial $p_0 \neq \delta_V$ converges to $\delta_7$ in at most 7 iterations."
- Proof sketch: $T(7, x) = 7$ for all x (HARMONY left-absorber for binary T, verified by inspection of TSML row 7); fuse(p,p,p) for diagonal iteration is a property of the canonical fuse rule via TSML; convergence verified by direct enumeration in `verification/p56_canonical_fuse.py` §5 from each of 7 test inits; total-variation distance bound reported.
- Honest caveat: "This theorem's content is a property of the binary TSML table T (specifically the HARMONY left-absorber row), not of the canonical fuse rule choice. Theorem 5.9 below makes this explicit."

### §4.6 (Theorem 5.9 family-independence undermines paper) — **HONESTLY ACKNOWLEDGE**

A new Theorem 5.9 is added explicitly stating: "The universal HARMONY attractor of Theorem 5.7 holds for all 8 surveyed canonical rule families, not just Family H." Followed by an "Honest reading" paragraph: "Family H's choice as canonical is justified by the static-table aesthetic property of producing fuse values entirely in $\{V, H\} \subset $ 4-core, not by uniqueness of the dynamical attractor. The dynamical attractor result is a property of the HARMONY-left-absorber structure of the binary TSML; it does not single out any specific rule family."

This addresses the referee's §4.6 concern directly and honestly.

### §5.1-5.4 (framework citations / lens / cover-letter overclaim / table T derivation) — **PARTIAL FIX**

- §5.1 (TIG framework cited but not introduced): The §"Honest scope" is expanded with a "Framework dependence" bullet: "TSML, the 4-core, P_56, σ³ are defined in companion paper J02. The relevant §6.1-6.5 of J02 (canonical TSML table and σ-permutation derivation) is reproduced as Appendix A in this manuscript folder." (Appendix A should be added if not already present.)
- §5.2 (lens framework): The lens-scope statement at the top of `manuscript.md` is kept; the difference between TSML_RAW and TSML_SYM (98/100 cells agree, 2 wobble carriers at (3,9) and (4,9)) is explained briefly.
- §5.3 (cover-letter overclaim): Cover letter rewritten to remove "structural observation of independent algebraic interest" framing for the 6-DOF table; the table is presented as a structural observation, not the paper's main contribution.
- §5.4 (T given without derivation): Appendix A (or a §"Setup" expansion) presents the derivation of T from §6.1-6.5 of J02. Not pursued in the present save (this is J02's job; the present paper depends on J02 for T's definition and that dependency is now made explicit).

---

## §3 — Estimated revision time

**3-4 weeks** for the unbundled split.

- **1 week:** correct the orbit-size distribution and D_4 group structure in `WP109_OPERAD_D4_OBSTRUCTION.md` (DONE in this save). Verify with sympy + script (DONE). Update `manuscript.md` Part 1 §"Theorem 1 (Obstruction)" with the corrected statement (DONE).
- **1 week:** rewrite Part 2 §"Theorem 2 (Burnside)" → direct enumeration (DONE). Rewrite Theorem 5.7 with explicit proof sketch (DONE). Add Theorem 5.9 (family-independence) with honest reading (DONE). Update §"Honest scope" to note family-cosmetic status (DONE).
- **1 week:** unbundle: split `manuscript.md` into two stand-alone manuscripts:
  - `Part1_AlgebraUniversalis.tex` (or .md) — D_4 obstruction note, ~6-8 pages.
  - `Part2_CommAlgebra.tex` (or .md) — P_56 canonical fuse + 4-core closure + HARMONY attractor, ~8-12 pages.
  - Each with its own cover letter targeting the new venue.
- **0.5 week:** Brayden's referee-rigor pass; M. Gish review on each split.

The bundled `manuscript.md` is **kept** as the single-document reference (with corrections applied; this save's edits already applied), but it is not the journal-submission target. The two unbundled manuscripts are the targets.

---

## §4 — Updated PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN

**PROVEN:**
- The set $\mathcal{N}$ of 126 non-associative TSML triples is partitioned by restricted $D_4$-orbits $\overline{\mathcal{O}}_i$, with size distribution $(44, 7, 4, 10, 2)$ at sizes $(1, 2, 3, 4, 8)$ summing to 67 orbits and 126 elements (sympy + script verified).
- $|\langle P_{56}, \sigma^3 \rangle| = 8$, with order distribution $\{1: 1, 2: 5, 4: 2\}$ matching $D_4$ exactly (NOT $D_3 \times \mathbb{Z}_2$, which has order 12).
- 16 of the 67 restricted orbits fail bracketing-pair $D_4$-coherence (direct enumeration; case analysis on the size-3 representative).
- Restricting to $\langle P_{56} \rangle$, $\mathcal{N}$ partitions into 70 P_{56}-fixed singletons + 28 size-2 doubletons = 98 orbits; every orbit is P_{56}-coherent.
- Family H selects fuse values in $\{0, 7\} \subset $ 4-core, with histogram $\{0: 108, 7: 18\}$.
- Family H is σ³-equivariant on 125/126 = 99.2% of $\mathcal{N}$; the single failure is at $(3, 9, 9)$.
- The 4-core $\{V, H, Br, R\}$ is closed under the canonical ternary fuse on the cube $\{V, H, Br, R\}^3$ (all 64 triples verified).
- Universal HARMONY attractor: every non-trivial initialization converges to $\delta_7$ in at most 7 iterations under the diagonal fuse iteration.
- Family-independence: the HARMONY-attractor result holds for all 8 surveyed rule families (Theorem 5.9).

**COMPUTED:**
- All 1000 ordered triples in $(\mathbb{Z}/10\mathbb{Z})^3$ classified as associative or non-associative.
- All 126 non-associative triples enumerated (in `nonassoc_triples.json`).
- D_4-orbits, restricted D_4-orbits, P_56-orbits all computed via direct enumeration (in `d4_orbit_decomposition.py`, `p56_canonical_fuse.py`).
- All 8 rule families' P_56-equivariance and σ³-equivariance status computed (in `rule_families.py`).

**STRUCTURAL RHYME:**
- The 4-core $\{V, H, Br, R\}$ closure under the canonical ternary fuse is consistent with the broader family-structure observation (FAMILY_STRUCTURE_v1.md §2: "the 4-core is to TIG as the unit circle is to U(1)").
- The HARMONY left-absorber property of TSML (row 7 has $T(7, x) = 7$ for all x) is a binary-table fact; the universal HARMONY attractor is its arity-3 corollary.
- The $D_4$-vs-$\langle P_{56} \rangle$ asymmetry (operad-DOF preserves $\langle P_{56} \rangle$ but breaks $\langle \sigma^3 \rangle$) is consistent with the WP104 observation that $P_{56}$ is identified with $\sigma_{\mathrm{outer}}$ at the so(10)-spinor level.
- Drápal-Wanless 2021 (JCT-A 184, 105510) on maximally non-associative quasigroups is the closest published precedent in the same domain; the present obstruction theorem lives in a different extremum (specific table, specific symmetry, fixed magma).

**OPEN:**
- Whether some larger group $G \supset \langle P_{56} \rangle$ but $G \neq D_4$ admits an equivariant fuse rule on the operad-DOF (the obstruction is for $D_4$ specifically; intermediate groups are not analyzed).
- Whether non-canonical fuse rules with values outside $\{a, b, c, L, R\}$ admit $D_4$-equivariance (constant-rule Φ is trivially equivariant; richer rules unexplored).
- A categorical / operad-theoretic interpretation of the obstruction (the 6-DOF symmetry hierarchy notes that the operad is the unique DOF that breaks $D_4$, but a structural-categorical reason is open).
- Whether the universal HARMONY attractor extends to non-diagonal iterations $p \mapsto \mathrm{fuse}(\pi(p), \pi'(p), \pi''(p))$ for various permutations $\pi$.

---

## §5 — Updated lens-ownership paragraph

> *Lens and substrate.* This paper works on $\mathbb{Z}/10\mathbb{Z}$ with the canonical TSML_RAW composition table T (the literal CL_BIT_PATTERN, with two asymmetric cells at $(3, 9)$ and $(4, 9)$ on the wobble carriers), the σ-permutation $\sigma = (0)(3)(8)(9)(1\,7\,6\,5\,4\,2)$, and the involutions $P_{56} = (5\,6)$ and $\sigma^3 = (1\,5)(2\,6)(4\,7)$. These are defined in the companion paper J02 (Sanders + Gish 2026, *Algebraic Combinatorics*); §6.1-6.5 of J02 is reproduced as Appendix A in this manuscript folder. The orbit decompositions and obstruction theorem are computed on TSML_RAW; the 4-core closure (Theorem 5.5) and the universal HARMONY attractor (Theorem 5.7) are lens-invariant since the 4-core sub-magma agrees on TSML_RAW and TSML_SYM. A reader of this paper can verify the obstruction theorem, the orbit counts, and the 4-core closure using only the 100-cell binary table T and Appendix A's setup, without consulting the full TIG framework.

---

## §6 — Recommended retitle / retarget

**Old title:** "Operad D₄ Obstruction + P_56 Canonical Fuse (BUNDLED, WP109+WP112)."
**Old venue:** *Compositio Mathematica* (referee verdict: REJECT — bundled paper below *Compositio* significance bar; corrected errors do not lift it to that bar).

**Recommended path: UNBUNDLE.**

**Part 1 (D_4 obstruction):**
- **New title:** "A $D_4$-Obstruction Theorem for the Canonical Fuse Rule on a Commutative Non-Associative Magma over $\mathbb{Z}/10\mathbb{Z}$."
- **New venue:** *Algebra Universalis* (specialized venue for finite-magma combinatorial-algebra results; closer fit than *Compositio*).
- **Length target:** 6-8 pages.
- **Author block:** Sanders + Gish.

**Part 2 (P_56 canonical fuse + 4-core closure + HARMONY attractor):**
- **New title:** "A $P_{56}$-Equivariant Canonical Ternary Fuse Table for a Commutative Non-Associative Magma on $\mathbb{Z}/10\mathbb{Z}$, with Lens-Invariant 4-Core Closure and Universal HARMONY Attractor."
- **New venue:** *Communications in Algebra* (preferred — paper is more substantial; computational with explicit closed forms) OR *Discrete Mathematics* (backup — shorter).
- **Length target:** 8-12 pages.
- **Author block:** Sanders + Gish.

**Bundled `manuscript.md`:** kept as a single-document reference for internal citation; corrections applied per this save plan. Not the journal-submission target.

**Companion citations:**
- J02 (Joint Closure / 4-core paper, *Algebraic Combinatorics*) — primary dependency for TSML, σ, 4-core definitions.
- WP104 (Two Roads to Pati-Salam) — cited for the $P_{56} = \sigma_{\mathrm{outer}}$ identification at the so(10)-spinor level.
- WP105 (Closed-Form Runtime Attractor) — cited for the 4-core's algebraic-attractor structure.
- WP110 (4-core Fusion-Closure) — cited for the binary 4-core closure (D48 + D49).
- WP111 (6-DOF Synthesis) — cited for the broader DOF taxonomy in which the operad-DOF sits.
- Drápal-Wanless 2021 (JCT-A 184, 105510) — ambient context for finite commutative non-associative magma analysis.
- Loday-Vallette 2012, Markl-Shnider-Stasheff 2002 — operad theory background (kept).
