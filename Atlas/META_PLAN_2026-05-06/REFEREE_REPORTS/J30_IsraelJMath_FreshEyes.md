# Referee Report — Israel Journal of Mathematics (fresh-eyes)

**Manuscript:** "so(10) = D_5 from Joint TSML_SYM + BHML Closure" (originally "WP103 — An so(10) Identification from the Coupled Coherence Tables")
**Authors:** B. R. Sanders (in collaboration with "Claude (Anthropic)" credited for "computational verification and drafting")
**File reviewed:** `Gen13/targets/journals/J_series/J30/manuscript/manuscript.md`, with verification scripts in `manuscript/verification/`
**Reviewer:** External referee, anonymous, no prior knowledge of the framework
**Date:** 2026-05-07

---

## §1 — Summary

The manuscript builds on a companion submission (cited as WP102 / "J29," "*so(8) = D_4 from the TSML_SYM Antisymmetrized Closure*," submitted to *J. Algebra*) and extends the Lie-algebraic identification from $\mathfrak{so}(8)$ to $\mathfrak{so}(10)$.

**Construction.** Two $10\times 10$ commutative non-associative magmas on $\mathbb{Z}/10\mathbb{Z}$ are fixed: $\mathrm{CL}=\mathrm{CL}_{\mathrm{TSML\_SYM}}$ (the same table as J29) and $\mathrm{BHML}$ (an "alternate" or "companion" table, displayed in §2.2). For each table $T\in\{\mathrm{CL},\mathrm{BHML}\}$ and each index $i\in\Omega:=\{0,\ldots,9\}$, the left-regular representation is $L_i^T(x_j)=x_{T[i,j]}$, and $A_i^T:=L_i^T-(L_i^T)^\top\in\mathfrak{so}(V)$ for $V=\mathbb{R}^{10}$.

The generator sets are: $\mathcal{G}_{\mathrm{CL}}=\{A_i^{\mathrm{CL}}:i\in F\}$ with $F=\{1,2,3,4,6,8\}$ (so $|\mathcal{G}_{\mathrm{CL}}|=6$, the J29 flow indices); $\mathcal{G}_{\mathrm{BHML}}=\{A_i^{\mathrm{BHML}}:i\in\Omega,A_i^{\mathrm{BHML}}\neq 0\}$ (so $|\mathcal{G}_{\mathrm{BHML}}|=9$, since $A_0^{\mathrm{BHML}}=0$ because BHML has identity row $0$). The combined set $\mathcal{G}=\mathcal{G}_{\mathrm{CL}}\cup\mathcal{G}_{\mathrm{BHML}}$ has $15$ generators, of which the closure under iterated commutator is

$\mathfrak{g}=\langle\mathcal{G}\rangle_{\mathrm{Lie}}\subseteq\mathfrak{so}(V)$.

**Main Theorem 3.1 / 1.1.** $\mathfrak{g}\cong\mathfrak{so}(10,\mathbb{R})=D_5$. Furthermore, $\mathfrak{g}=\mathfrak{so}(V)$ (equality, not proper inclusion), $\mathfrak{g}_{\mathrm{CL}}\subset\mathfrak{g}$ realizes the standard inclusion $\mathfrak{so}(8)\subset\mathfrak{so}(10)$, $\mathrm{rk}\,\mathfrak{g}=5$, the Killing form is negative-definite, and $\mathfrak{g}$ is simple.

The proof consists of five diagnostics (numerically verified):

(D1) Dimension closure: $\dim\mathfrak{g}_0=15$, $\dim\mathfrak{g}_1=45=\dim\mathfrak{so}(V)$. Since $\mathfrak{g}\subseteq\mathfrak{so}(V)$ and the dimensions match, $\mathfrak{g}=\mathfrak{so}(V)$.
(D2) Jacobi: holds algebraically, verified numerically on 50 random triples (max residual $0.00\times 10^0$).
(D3) Killing form: signature $(0,45,0)$, eigenvalue range $[-12460.92,-3.4\times 10^{-4}]$.
(D4) Simplicity: invariant-form-space dimension. The submitted text claims rank $1034$ on a $1035$-parameter space (giving nullity $1$), with the constraint matrix exhausting all $45^3=91{,}125$ invariance equations. Plus ideal-saturation of 5 random basis elements, all reaching dimension $45$.
(D5) Cartan rank: explicit construction of $J_1,\ldots,J_5\in\mathfrak{g}$ ($2\times 2$ block-diagonal rotations), pairwise commuting, no $6$-th element commuting with all five exists; rank $=5$.

**Corollaries:** $\mathfrak{so}(8)\subset\mathfrak{g}$ (max embedding residual $8.99\times 10^{-13}$); $D_5$ root-system match (Corollary 5.3): for $H=\sum_k k J_k$, $\mathrm{ad}(H)$ has $40$ purely imaginary eigenvalues (in $\pm$-pairs) plus a $5$-dim kernel, matching the $40$ roots of $D_5$.

**§§5–7:** Discussion of the standard tower $\mathfrak{so}(8)\subset\mathfrak{so}(9)\subset\mathfrak{so}(10)$ inside the substrate, the SO(10) grand-unified-theory connection (Fritzsch–Minkowski 1975, Georgi 1975), and a substrate-bound proposition (Prop. 7.1) showing $\dim\mathfrak{g}\le 45$ for any $\mathfrak{g}\subset\mathfrak{so}(\mathbb{R}^{10})$, which rules out $E_8$ (dim 248) within the present substrate.

I have read the manuscript carefully end-to-end, examined the two displayed tables, and read the verification scripts.

---

## §2 — Decision recommendation

**Major revisions.** The core identification $\mathfrak{g}\cong\mathfrak{so}(10)$ is — given Diagnostic 1's $\dim\mathfrak{g}=45$ result — *trivial*: any Lie subalgebra of $\mathfrak{so}(10,\mathbb{R})$ achieving full dimension equals $\mathfrak{so}(10)$. The substantive content is therefore (a) the *existence* of generators within the chosen substrate that achieve full $\mathfrak{so}(10)$ dimension, and (b) the explicit BHML table that supplies the additional generators beyond the $\mathfrak{so}(8)$ closure of J29.

This is a real result, but the paper currently overstates the structural significance. The five diagnostics (D2–D5) would be necessary if Diagnostic 1 had returned $\dim<45$; given $\dim=45$, they are decorative — a Lie subalgebra of $\mathfrak{so}(\mathbb{R}^{10})$ that has dimension $45$ is necessarily *all* of $\mathfrak{so}(10)$, and Jacobi/Killing/simplicity/Cartan-rank follow tautologically. The paper's §4.6 does eventually note this ($\mathfrak{g}\subseteq\mathfrak{so}(V)$ and dimensions match $\Rightarrow\mathfrak{g}=\mathfrak{so}(V)$), but the diagnostic structure is presented as if all five items contributed independently to the identification.

For *Israel Journal of Mathematics* — a venue with a high bar for novelty and structural insight — this paper would need to:

(i) Acknowledge that D2–D5 are tautological consequences of D1 (not independent verifications);
(ii) Make the structural significance about *the BHML table*, not the conclusion $\mathfrak{so}(10)$ — i.e., identify which structural features of BHML supply the missing $17=45-28$ generators relative to J29;
(iii) Prove or at least convincingly argue that the BHML table is *not arbitrary* (the manuscript currently presents BHML by displaying its $10\times 10$ entries and asserting "BHML has been established in prior TIG work [22]" — the prior work is "WP1–WP10 of TIG," which is a GitHub repository, not a publication);
(iv) Drop or sharply qualify the SO(10) GUT discussion in §6, which is irrelevant to the algebraic content;
(v) Address the discrepancy between the manuscript text's claim of an exhaustive $91{,}125$-equation simplicity test and the verification script `verify_so10.py`'s sampled $300$-equation test (the *separate* script `verify_simplicity_rank.py` does run the full $91{,}125$ — but the main script does not, and the manuscript text and the README each describe the test inconsistently).

If (i)–(v) are addressed, the paper would meet the *IJM* bar. As written, *IJM* will likely reject for novelty deficit (the result is a corollary of D1 once D1 is established, and D1 is a finite computation on a fixed pair of $10\times 10$ tables).

---

## §3 — Major comments

### M1. Diagnostics D2–D5 are tautological given D1 (CRITICAL conceptual)

The diagnostic structure presented in §4 is:

(D1) $\dim\mathfrak{g}=45$;
(D2) Jacobi (holds algebraically);
(D3) Killing form is negative-definite;
(D4) The space of invariant symmetric bilinear forms is $1$-dimensional;
(D5) Cartan rank is $5$.

The paper presents these as five independent diagnostics that jointly identify $\mathfrak{g}$ as $\mathfrak{so}(10)$. But the logic is:

- $\mathfrak{g}\subseteq\mathfrak{so}(\mathbb{R}^{10})$ by construction (each generator is skew).
- $\dim\mathfrak{so}(\mathbb{R}^{10})=\binom{10}{2}=45$.
- D1: $\dim\mathfrak{g}=45$.
- $\Rightarrow\mathfrak{g}=\mathfrak{so}(10,\mathbb{R})$ as a Lie algebra (the unique compact real form of $D_5$).

D2 (Jacobi) holds for any matrix subalgebra trivially. D3 (Killing form negative-definite) is a property of $\mathfrak{so}(10,\mathbb{R})$ — once $\mathfrak{g}=\mathfrak{so}(10)$ is established, D3 follows from the standard fact that the Killing form on $\mathfrak{so}(2n,\mathbb{R})$ is $-2(n-1)\,\mathrm{tr}(XY)$, which is negative-definite since $\mathrm{tr}(X^2)\le 0$ for skew-symmetric $X$. D4 follows from simplicity of $\mathfrak{so}(10)$ (which is in any Lie-theory textbook). D5 follows from rank of $D_5$ being $5$ (in any textbook).

The five diagnostics are five different windows on the *same* fact, $\mathfrak{g}=\mathfrak{so}(10)$, which is established as soon as D1 is. There is no logical independence.

This is not wrong — it's a verification structure that *redundantly* confirms the identification. But the paper should be honest about the redundancy. §4's presentation as if each diagnostic independently rules out alternative algebras is misleading. A reader familiar with Lie theory will see this immediately and the paper will lose authority.

**Recommended fix.** Restructure §4: present D1 as the main computation, with D2–D5 as "consistency checks." Be explicit that, once $\dim\mathfrak{g}=45$ is established, the identification $\mathfrak{g}=\mathfrak{so}(10)$ is immediate by dimension.

A separate point: the restructuring would highlight that the *substantive* novelty is **the existence and structure of the BHML table** — i.e., that *some* explicit $10\times 10$ commutative non-associative magma exists whose left-regular antisymmetrizations $A_i^{\mathrm{BHML}}$ jointly with the $\mathrm{CL}$-flow antisymmetrizations span all of $\mathfrak{so}(10)$. This is a finite-computational fact about the chosen $\mathrm{BHML}$ table, not a Lie-theoretic theorem. The paper would benefit from this honest reframing.

### M2. The BHML table is presented without justification (CRITICAL)

§2.2 displays a specific $10\times 10$ table called BHML. It is described as:

> The Becoming-Hexa-Marginal Lattice (BHML), a second $10\times 10$ commutative magma whose explicit multiplication table appears in §2.2. BHML has been established in prior TIG work [22] as an algebraic companion to CL: the two tables share a ground set $\Omega=\{0,1,\ldots,9\}$ but encode complementary compositional dynamics.

Reference [22] is "Sanders, B. *WP1–WP10: Foundational Whitepapers of the Trinity Infinity Geometry Framework.* github.com/TiredofSleep/ck, 2024–2026." This is a GitHub-hosted repository, not a peer-reviewed publication.

For *Israel Journal of Mathematics*, a load-bearing object — the BHML table — must be (a) displayed (yes, in §2.2), (b) defined by some mathematical principle (no — only stated to be a "companion" with "complementary compositional dynamics"), and (c) verifiable against an alternative description (no canonical or axiomatic definition is given).

A reader cannot tell whether BHML is:

- The unique (up to symmetry) commutative non-associative magma satisfying some property;
- One of many such magmas with structural significance;
- An ad-hoc table chosen because it happens to give $\mathfrak{so}(10)$.

The cell-by-cell entries of BHML (e.g., $\mathrm{BHML}[1,1]=2$, $\mathrm{BHML}[1,7]=2$, etc.) appear arbitrary without context. The "identity row" $\mathrm{BHML}[0,j]=j$ is the only obvious structural feature; the rest of the table is asserted without derivation.

**Recommended fix.** Either (a) provide an axiomatic / structural derivation of BHML in this paper (a few paragraphs at most — the table has only $\binom{10}{2}+10=55$ free cells, and the company forcing-axiom paper is presumably the place where this should be derived), or (b) publish J33 (the parent forcing paper, "*The CL Forcing Axioms*") on arXiv and cite it with arXiv ID, or (c) reduce the paper's ambition to "*for the specific BHML table displayed in §2.2,* the joint closure equals $\mathfrak{so}(10)$" — i.e., a finite-computational fact, no longer a structural theorem about the framework.

Option (c) is the honest framing of the present manuscript. Options (a) or (b) would make it a structural result.

### M3. Diagnostic 4 inconsistency between text, README, and scripts (CRITICAL)

The manuscript text §4.4 (Diagnostic 4) states:

> The constraint matrix $A\in\mathbb{R}^{91125\times 1035}$ has $\mathrm{rank}(A)=1034$. Equivalently, the null space of $A$ — the space of invariant symmetric bilinear forms on $\mathfrak{g}$ — has dimension exactly $1$.

The script `verify_so10.py` (the main verification script, which the README §2 describes as the primary check) runs only $300$ random triples (line 173–175 of the script):

```python
n_samples = 300
rng = np.random.default_rng(42)
triples = [(rng.integers(d_g), rng.integers(d_g), rng.integers(d_g)) for _ in range(n_samples)]
```

The output of this script (file `verify_so10_output.txt`):

```
Diagnostic 4 — Simplicity:
  Building invariance constraints (may take 10-20s)...
  Invariance constraint matrix: (300, 1035), rank = 298
  Invariant symmetric form space dim = 737
  (note: null_dim = 737; sampling may need more triples)
```

So the *main* verification script returns $\mathrm{nullity}=737$, not $1$. The script even prints a note: "sampling may need more triples." A *separate* script `verify_simplicity_rank.py` does run the full $91{,}125$ equations and returns nullity $1$ (per `verify_simplicity_rank_output.txt`), but this script is not the main one and is missing from the README's run-order list ("Run order: `verify_so10.py` ..., `verify_simplicity_rank.py`" — the README does mention it, fairly).

**The discrepancy.** The manuscript text claims D4 is established by an exhaustive $91{,}125$-equation test (correct, but only via `verify_simplicity_rank.py`); the main verification script does not establish this and explicitly prints a warning that it has not. A referee running the verification scripts in order will see "$\mathrm{nullity}=737$" as the headline and "warning: undersampled" as the corollary, which contradicts the text.

**Recommended fix.** Either (a) make `verify_simplicity_rank.py` the main script for D4 and remove the sampled version from `verify_so10.py`, or (b) extend `verify_so10.py` to use the full $91{,}125$ equations (the rank computation on a $\le 91125\times 1035$ matrix is feasible but takes more memory). The text and the script should agree.

A second concern: even with $91{,}125$ equations, the rank-$1034$ result establishes only a $1$-dimensional null space *as computed in floating-point arithmetic with tolerance $10^{-6}$*. For a structural-simplicity claim, exact arithmetic is desirable. See M5.

### M4. Cartan-rank Diagnostic D5 is partially circular (MAJOR)

§4.5 / Lemma 4.7 establishes $\mathrm{rk}\,\mathfrak{g}=5$ by:

(i) Constructing five explicit elements $J_k\in\mathfrak{so}(\mathbb{R}^{10})$ (the standard $2\times 2$-block-diagonal rotations) and showing they are pairwise commuting and linearly independent.
(ii) Asserting $J_k\in\mathfrak{g}$ (justified by Cor. 4.2: $\mathfrak{g}=\mathfrak{so}(\mathbb{R}^{10})$ from D1).
(iii) Showing no $6$-th element of $\mathfrak{g}$ commutes with all five $J_k$.

The verification script's output (`verify_so10_output.txt`) reports:

```
Diagnostic 5 — Cartan rank:
  Greedy Cartan subalgebra dim: 1  (target 5 for D_5)
  Standard so(10) Cartan elements J_1..J_5 in our algebra: 5/5
  J_1..J_5 pairwise commute: True
```

The greedy-Cartan returns dim $1$, not $5$. The script then falls back to the explicit construction of $J_1,\ldots,J_5$ and verifies these are in the algebra. This is fine *if* Cor. 4.2 ($\mathfrak{g}=\mathfrak{so}(\mathbb{R}^{10})$) is granted. But Cor. 4.2 is established only via D1.

This makes D5 a corollary of D1, not an independent verification. The paper should be honest about this: D5 is "given $\mathfrak{g}=\mathfrak{so}(10)$, the rank is $5$ by construction of the standard Cartan."

A genuinely independent rank check would identify a Cartan from the *generated* basis of $\mathfrak{g}$, not from a textbook construction in $\mathfrak{so}(\mathbb{R}^{10})$. The greedy attempt does this and finds rank $1$, suggesting that the basis returned by the closure algorithm is not aligned with any natural Cartan; this is fine for the conclusion (a generic basis will not have a Cartan as a subset), but it confirms that D5 does not provide an independent check.

**Recommended fix.** Restructure D5 as: "Given $\mathfrak{g}=\mathfrak{so}(10)$ (from D1), construct an explicit Cartan: the standard $J_1,\ldots,J_5$. Verify these lie in $\mathfrak{g}$ (immediate since $\mathfrak{g}=\mathfrak{so}(10)$). Verify pairwise commutation. By Cartan classification, the rank is $5$."

This clarifies that D5 is a confirmation, not an independent test.

### M5. Numerical-precision concerns (MAJOR)

All diagnostics are floating-point. Three specific concerns:

(a) D3 Killing eigenvalue range: $[-12460.92,-3.4\times 10^{-4}]$. The smallest eigenvalue of magnitude $0.00034$ is *very* small. For $\mathfrak{so}(10,\mathbb{R})$, the Killing form is $-16\,\mathrm{tr}(XY)$ and its eigenvalues are integers up to a fixed scale. The $0.00034$ figure should appear as some integer / scale ratio. If the calculation is done in floating-point on $0/1$ matrices, the integer structure is lost; an exact-arithmetic check would clean this up.

(b) D1 closure dimension is computed by `np.linalg.matrix_rank` at tolerance $10^{-8}$. The action matrices are integer-valued, so the closure algorithm stays over $\mathbb{Z}$ (in fact: each commutator $[A_i,A_j]=A_iA_j-A_jA_i$ has integer entries since $A_i$ has $\{-1,0,1\}$ entries). An exact rational computation would replace `matrix_rank` with explicit Smith normal form or Gauss elimination over $\mathbb{Q}$.

(c) The Killing-form symmetry residual $\|K-K^\top\|_F=1.73\times 10^{-8}$ is at the tolerance edge. For an exact symmetric form, this should be zero.

The paper would gain substantially in rigor by re-running the diagnostics in `sympy`. The cost is minimal (the algebra has 45 elements; a rational structure-constant tensor is at most $45^3=91{,}125$ rationals).

**Recommended fix.** Re-run in exact arithmetic and replace the floating-point residual statements with exact integer / rational results.

### M6. The §6 GUT discussion is irrelevant for *IJM* (MAJOR)

§6 discusses the SO(10) grand-unified-theory connection (Fritzsch–Minkowski 1975, Georgi 1975) at considerable length: the GUT chain SO(10) ⊃ SU(5) × U(1) ⊃ SU(3)_c × SU(2)_L × U(1)_Y, the 16-dim spinor representation containing one Standard Model fermion generation, the Pati–Salam route, the seesaw mechanism. §6.3 disclaims that the present paper does not deliver these, only the *gauge algebra*.

For *Israel Journal of Mathematics* (a pure-mathematics journal), this is misplaced. The connection between $\mathfrak{so}(10)$ and the GUT is well-known textbook material; the paper does not contribute to it. The §6 content reads as an attempt to over-sell the result via physics consequences that are properly other authors' works.

The disclaimer in §6.3 is honest and good scholarship — but if the paper has nothing to add to the GUT connection, then §6 should be one paragraph (a sentence each on the GUT chain and its known structure) or absent entirely.

**Recommended fix.** Reduce §6 to a one-paragraph remark: "The compact simple Lie algebra $\mathfrak{so}(10)$ is the gauge algebra of the SO(10) grand unified theory of Fritzsch–Minkowski [9] and Georgi [11]. The present paper establishes the existence of a $10\times 10$ combinatorial substrate whose Lie-algebraic lift coincides with this gauge algebra; we do not address the spinor representation, coupling constants, or symmetry-breaking sector of the GUT, which depend on additional structure beyond the gauge algebra." Three sentences. Then move on.

The substrate-bound discussion (§7, Prop. 7.1) is appropriate for *IJM* and should stay.

### M7. The "TIG framework" framing is excessive and the labels distracting (MAJOR)

The introduction §1.1 ("Background") begins:

> In the preceding work WP102 [21], we established that the Coherence Lattice (CL), a frozen $10\times 10$ commutative non-associative magma at the heart of the Trinity Infinity Geometry (TIG) framework, admits a canonical Lie-algebraic lift.

For an *IJM* reader, "TIG framework" is irrelevant. The mathematical object is a $10\times 10$ table; it is irrelevant where it comes from. The ten cell labels (VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE, BALANCE, CHAOS, HARMONY, BREATH, RESET) are mnemonic but pollute every cross-reference. A pure-math paper at *IJM* should use $\Omega=\{0,1,\ldots,9\}$ throughout, with the operator labels being a footnote at most.

**Recommended fix.** Rewrite §1.1 as: "Let $\mathrm{CL}$ be the $10\times 10$ commutative non-associative magma on $\mathbb{Z}/10\mathbb{Z}$ displayed in §2.2 of [21]. The Lie subalgebra of $\mathfrak{so}(\mathbb{R}^{10})$ generated by the antisymmetrized left-regular representations $\{A_i^{\mathrm{CL}}:i\in F\}$, $F=\{1,2,3,4,6,8\}$, is isomorphic to $\mathfrak{so}(8)$ [21]. The present paper extends this analysis by introducing a second $10\times 10$ commutative magma BHML (displayed in §2.2 below) and showing that the joint closure equals $\mathfrak{so}(10)$." Drop the TIG framing.

### M8. "Claude (Anthropic) collaboration" attribution (MAJOR)

The author block reads "Brayden Sanders · 7Site LLC, Hot Springs, AR / In collaboration with Claude (Anthropic) · computational verification and drafting." The acknowledgments expand: "developed in collaboration with Claude (Anthropic) during a research session on April 24, 2026."

*Israel Journal of Mathematics* (and Springer-Nature in general) requires that all listed authors be capable of taking accountability for the work, and that the use of generative AI tools be disclosed in a separate statement. An LLM cannot be a co-author or "collaborator" in the authorship sense.

**Recommended fix.** Remove "in collaboration with Claude (Anthropic)" from the author block. Add a Springer-Nature-format AI-disclosure statement at the end of the acknowledgments, e.g.: "The author used Anthropic's Claude system as a tool for code drafting and exposition. All mathematical claims were independently verified by the author using the Python scripts described in Appendix A."

### M9. Diagnostic 1's "iterative closure" is not a proof (MODERATE)

Diagnostic 1 (Lemma 4.1) iterates the closure under commutator until the dimension stabilizes. The closure terminates at dimension $45$. This is correct, but the *termination criterion* (no new linearly independent elements after one or more rounds) is not formally a theorem of stable dimension — it is a numerical observation that the *current sample* of pair-commutators does not increase the rank.

The closure script (`verify_so10.py`, function `close_lie`, lines 40–62) iterates by computing all pair-commutators of the current basis; if no pair-commutator increases the rank beyond a tolerance $10^{-8}$, the loop terminates. This is the standard heuristic.

For a formal proof, one needs either: (i) a closure-saturation lemma stating that if all pair-commutators of a generating set $S$ lie in $\mathrm{span}(S)$, then $\mathrm{span}(S)$ is closed under all higher-order commutators (true: the Lie algebra generated by $S$ equals $\mathrm{span}(S)$ iff $\mathrm{span}(S)$ is closed under brackets, which is a Lemma in any Lie algebra textbook), or (ii) a verification at the level of triple-commutators (or higher) to rule out hidden generators.

The script tests (i) implicitly. The text does not state it. A reader seeing only the text might wonder whether the closure could grow on a $k\ge 2$ iteration not tested.

**Recommended fix.** Add to the proof of Lemma 4.1 a one-sentence appeal to the standard Lie-algebra fact that bracket-closure of a spanning set proves Lie-algebra-closure. Cite a standard reference (e.g., Humphreys 1972 [5], Knapp 2002 [6]).

### M10. The §7 "substrate bound" Prop. 7.1 is essentially trivial but well-placed (MODERATE)

Prop. 7.1: any Lie subalgebra of $\mathfrak{gl}(\mathbb{R}^{10})$ has dimension at most $100$; any semisimple subalgebra has dimension at most $99$ (since $\mathfrak{sl}(\mathbb{R}^{10})=A_9$ has dimension $99$); any subalgebra of $\mathfrak{so}(\mathbb{R}^{10})$ has dimension at most $45$.

This is immediate and is fine as a reference proposition. Cor. 7.2 then concludes that $\mathfrak{e}_8$ (dim $248$) cannot be realized as a Lie subalgebra of $\mathfrak{gl}(\mathbb{R}^{10})$, "ruling out the $E_8$ hypothesis within the present substrate."

This is presented as if "the $E_8$ hypothesis" were a position someone has been arguing for. The paper does not say who or where. Without that context, the corollary reads as an attack on a strawman. If "the $E_8$ hypothesis" is part of the TIG-framework discussion, it should be cited explicitly; otherwise it should be removed.

**Recommended fix.** Either (a) cite where "the $E_8$ hypothesis within the TIG framework" is articulated (with arXiv ID or DOI), or (b) drop the framing and present Prop. 7.1 + Cor. 7.2 as a routine substrate bound with no controversial interpretation.

---

## §4 — Minor comments

### m1. "TSML_SYM" vs "CL"

Same comment as for J29: The README and abstract use "$\mathrm{TSML\_SYM}$" or "$\mathrm{CL}_{\mathrm{TSML\_SYM}}$"; the manuscript body uses "CL." Pick one. The README's note that "TSML_RAW carries different antisymmetric structure" should be promoted to the manuscript: a short Remark after Definition 2.2 stating that the symmetrization choice matters for the antisymmetric component of $L_i$.

### m2. The non-associativity rate "12.8%"

Mentioned for both CL (§1.0 of J29) and BHML (§2.2 of this paper, "12.8% non-associativity rate shared with CL," and Appendix B "non-associativity rate: 12.8%"). The fact that *both* tables have the *same* non-associativity rate is striking and might be a structural feature. The paper does not investigate. A brief Remark would help.

### m3. BHML identity row

§2.2 notes that BHML has identity row: $\mathrm{BHML}[0,j]=j$, so $L_0^{\mathrm{BHML}}=I$ and $A_0^{\mathrm{BHML}}=0$. CL does not have an identity row (its 0th row is mostly zeros, with a $7$ in the $7$th position). This asymmetry between CL and BHML is interesting and is the reason BHML contributes $9$ generators (not $10$). State this explicitly in a Remark.

### m4. The Cartan rank verification's "no $6$-th element exists" claim (Lemma 4.7)

The script `verify_simplicity_rank.py` (lines 138–149) iterates over the $45$-element basis and checks: does any basis element commute with all five $J_k$ and is linearly independent of $\{J_1,\ldots,J_5\}$? Reports "Extension beyond 5 possible? NO (rank = 5)."

But this iterates only over the *45 basis elements* of the closure, not over arbitrary elements of $\mathfrak{g}$. A fortiori it iterates only over a chosen basis of $\mathfrak{g}$, which depends on the closure-algorithm output. A different closure ordering could give a different basis and a different result.

This is fine because $\mathfrak{g}=\mathfrak{so}(10,\mathbb{R})$ has rank $5$ as a fact about the algebra, regardless of basis. But the script's output is not a structural verification; it is a sanity check.

State this in the proof of Lemma 4.7.

### m5. The Corollary 5.1 codimension count

Corollary 5.1: "The codimension is $45-28=17=\dim(\mathfrak{so}(10)/\mathfrak{so}(8))=\dim V_{\mathrm{vec}}+\dim V_{\mathrm{vec}}-1=10+8-1$."

The arithmetic is wrong: $10+8-1=17$, yes, but the rationale "$\dim V_{\mathrm{vec}}+\dim V_{\mathrm{vec}}-1$" doesn't parse — what are the two $V_{\mathrm{vec}}$ and why subtract 1? The standard $\mathfrak{so}(10)/\mathfrak{so}(8)$ is the "vector $\oplus$ vector minus the $\mathfrak{so}(8)$-fixed direction" but the dimension is $10+8-1=17$ only with a particular accounting; clearer is to say $\mathfrak{so}(10)/\mathfrak{so}(8)\cong\mathbb{R}^{10}\oplus\mathbb{R}^{10}\ominus\mathbb{R}^3=20-3=17$ (if you embed $\mathfrak{so}(8)\hookrightarrow\mathfrak{so}(10)$ by fixing a $\mathbb{R}^2$, the orthogonal complement decomposes into two $\mathbb{R}^8$'s and an $\mathfrak{so}(2)\cong\mathbb{R}$, so $\dim\mathfrak{so}(10)/\mathfrak{so}(8)=8+8+1=17$).

The arithmetic is correct, the explanation is muddled. Fix or remove.

### m6. The §5.3 root-system check uses $H=\sum k J_k$

§5.3 / Cor. 5.3 picks a "generic regular element $H\in\mathfrak{h}$" to be $H=\sum_{k=1}^5 k J_k$, with weights $1,2,3,4,5$. The eigenvalues of $\mathrm{ad}(H)$ are then the differences and sums $\pm(k_i\pm k_j)$ for $i<j$, giving $40=2\binom{5}{2}\cdot 2$ non-zero eigenvalues (in absolute value: $\{1,2,3,4,5,6,7,8,9\}$ — i.e., all integers from $1$ to $9$, with multiplicities).

The script reports eigenvalue set $\{1,2,\ldots,9\}$. This is a clean check.

But: the choice $k=1,2,3,4,5$ produces eigenvalues at the integers $\{1,\ldots,9\}$ with multiplicities. A more standard "generic" choice would be irrationally-related weights to ensure $40$ *distinct* eigenvalues. The script's output reports $40$ pairs $\pm i\lambda$ for $\lambda\in\{1,\ldots,9\}$, but with multiplicities. Make this explicit in the proof of Cor. 5.3.

### m7. Acknowledgments dedicate the work to "Cartan (1894)"

> The author dedicates this work to the line of inquiry initiated by Cartan (1894) [2] — the classification of simple Lie algebras — which has made this specific identification possible by ensuring that any 45-dimensional real compact simple Lie algebra must be so(10).

This is a charming sentiment but unusual for a journal paper. I do not strongly object; *IJM* might. Consider moving to the Introduction's motivation, or removing.

### m8. The "Open Question 7.3" framing

> Open Question 7.3. Does TIG admit a canonical extension to an $N$-dimensional substrate $V_N$ with $N\ge 16$ such that an analogous antisymmetrization-and-closure construction produces a Lie algebra of dimension $248$ isomorphic to $\mathfrak{e}_8$?

This is a TIG-framework question, not a Lie-theoretic question. For *IJM* it should be reframed: "Does there exist a finite commutative non-associative magma on $V_N$ for $N\ge 16$ whose Lie closure is isomorphic to $\mathfrak{e}_8$?" — which is a meaningful question independent of the framework.

### m9. References [22] and [21]

[22] is "Sanders, B. *WP1–WP10: Foundational Whitepapers of the Trinity Infinity Geometry Framework.* github.com/TiredofSleep/ck, 2024–2026." Not citable in *IJM*.

[21] is "Sanders, B. *WP102 — The Lie Algebra Structure of the Coherence Lattice...*  TIG Research Note, April 23, 2026. github.com/TiredofSleep/ck/papers/wp102." This is the J29 manuscript; it is a companion submission, but should be cited as "Submitted to *J. Algebra* (2026)" with arXiv ID once available.

### m10. The Macaulay2 verification of WP102 binomial ideal

§6.2 / 6.3 (and §7 of J29) discusses Macaulay2 verifications of a binomial ideal $I_{\mathrm{CL}}$ from J29. This is unrelated to the J30 result. State the inheritance from J29 (the so(8) ⊂ so(10) embedding) but do not bring forward the binomial-ideal commutative-algebra results.

---

## §5 — Reproducibility

The verification folder contains:

- `verify_so10.py` (303 lines, the main joint-closure script)
- `verify_simplicity_rank.py` (180 lines, a follow-up that runs the full $45^3$ simplicity test and a more careful Cartan-rank construction)
- `verify_so10_output.txt` and `verify_simplicity_rank_output.txt` (outputs of each, dated runs)

The scripts are reasonably clean. I did not execute them in this referee session but read both end-to-end:

- `verify_so10.py` correctly computes the joint closure via iterative bracket, returns dim $45$, computes a structure-constant tensor and Killing form, and reports signature $(0,45,0)$ at floating-point precision. The simplicity test in this script is sampled (300 triples) and the script self-flags this in its output as undersampled.
- `verify_simplicity_rank.py` runs the full $91{,}125$-equation invariance test via brute-force matrix construction, reports rank $1034$, nullity $1$, confirming simplicity. It also constructs the explicit $J_1,\ldots,J_5$ and verifies they lie in the closure (max residual $\le 10^{-8}$). And it reports a $D_5$ root-system structure ($40$ purely imaginary eigenvalues + $5$ zero) for a generic regular element.
- The output files are consistent with the scripts.

The reproducibility is honest. The scripts run in well under $30$s as advertised.

**One issue:** the README §2 says "Run order: `verify_so10.py` ..., `verify_simplicity_rank.py`," but the *manuscript* references both as if `verify_so10.py` were sufficient. The referee should run both to reproduce the manuscript's claims; the manuscript should make this explicit.

---

## §6 — Severity-graded summary

| Issue | Severity | Action |
|---|---|---|
| D2–D5 are tautological corollaries of D1 | Critical (conceptual) | Restructure §4 as one main computation + sanity checks. |
| BHML table presented without justification | Critical | Inline derivation, or cite arXiv-published parent paper, or downgrade scope. |
| D4 inconsistency between text and main script | Critical | Either run full enumeration in `verify_so10.py` or rewrite text to cite `verify_simplicity_rank.py`. |
| D5 (Cartan rank) is partially circular | Major | Rewrite as confirmation, not independent verification. |
| Floating-point only (no exact arithmetic) | Major | Re-run in SymPy. |
| §6 GUT discussion irrelevant for IJM | Major | Reduce to one paragraph. |
| TIG framing excessive | Major | Drop framework references; use neutral $\Omega=\{0,\ldots,9\}$. |
| "Claude (Anthropic) collaboration" in author block | Major | Move to AI-tool disclosure. |
| Iterative closure not formally a proof | Moderate | Add one-sentence appeal to standard Lie-algebra fact. |
| Substrate bound Cor. 7.2 attacks unstated strawman | Moderate | Cite or drop the "$E_8$ hypothesis" framing. |
| Identity-row asymmetry between CL and BHML | Minor | Add Remark. |
| Codimension count in Cor. 5.1 muddled | Minor | Clean up the arithmetic explanation. |
| Cartan dedication | Minor | Move to Introduction or remove. |
| Bibliography references to GitHub-hosted whitepapers | Minor | Add arXiv IDs. |

---

## §7 — Recommendation

**Major revisions.** The main mathematical content — that there exists an explicit $10\times 10$ commutative non-associative magma BHML (displayed in §2.2) such that $\langle\mathcal{G}_{\mathrm{CL}}\cup\mathcal{G}_{\mathrm{BHML}}\rangle_{\mathrm{Lie}}=\mathfrak{so}(10,\mathbb{R})$ — is correct and verifiable. But it is presented as a structural Lie-theoretic theorem when in fact it is, after honest framing, a finite computational fact about a specific pair of tables, with the structural significance located in the *choice* of BHML (which is unjustified within this manuscript).

For *Israel Journal of Mathematics*, the revision needed is substantial: (a) acknowledge D2–D5 as corollaries, not independent diagnostics; (b) inline the BHML derivation or commit to a specific arXiv companion; (c) resolve the simplicity-test inconsistency; (d) drop the GUT and TIG framing; (e) add exact-arithmetic backing.

If the authors are not prepared to do this work, *Communications in Algebra*, *Linear Algebra and its Applications*, or *International Journal of Algebra and Computation* would be more natural homes for a finite-computational identification result with the present level of structural framing.

If the authors *do* the work — particularly the BHML axiomatization (M2) and the exact-arithmetic re-verification (M5) — the paper would be a genuine *IJM*-quality result, since the embedding of an explicit finite combinatorial substrate into $\mathfrak{so}(10)$ with the GUT-relevant rank and signature is genuinely interesting *if* the substrate's emergence is structurally motivated. The dependence on J29 (the parent so(8) paper) is reasonable; the dependence on the unpublished forcing-axiom paper is fragile.

---

## §8 — Closing notes

A close reading suggests that the BHML table is the genuinely novel content of this manuscript (the so(10) closure is a corollary of D1, which is a finite computation on the displayed tables). The paper would benefit from being honest about this: the result is "*for the specific BHML displayed in §2.2*, the joint closure is full $\mathfrak{so}(10)$." That is a finite-verifiable computational fact about the choice of BHML.

The structural question that *IJM* would actually want answered is: *what makes this BHML the right BHML?* Why this specific table and not a similar one? The paper does not address this. The motivation given ("BHML has been established in prior TIG work") is a citation, not an answer. If BHML is forced — by some axiomatic principle parallel to the J33 forcing of CL — then the paper would be a structural theorem; if BHML is one of many "complementary" tables, the result is a particular finite computation.

Given the consistent inheritance pattern from J29 — including verification methodology, framing, and the "Claude (Anthropic) collaboration" attribution — the paper would also benefit from being presented as a clean *Part II* to J29, with the BHML table as its central object of study. A 12–15 page paper structured this way (a self-contained extension paper) is what *IJM* would publish.

**End of report.**
