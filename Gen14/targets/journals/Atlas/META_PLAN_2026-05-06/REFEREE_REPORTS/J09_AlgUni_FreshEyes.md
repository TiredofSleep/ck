# Referee Report — J09 / Algebra Universalis

**Manuscript:** *LATTICE: Paradoxical Information Algebras on the Z/10Z Substrate*
**Authors:** B. R. Sanders, M. Gish
**Submitted to:** *Algebra Universalis*
**Reviewer:** External referee — fresh eyes, no prior exposure to the surrounding research framework. The manuscript was read as a standalone piece of universal algebra / magma theory.
**Date:** 2026-05-07

---

## §1 — Summary of the manuscript

The paper studies a finite algebraic substrate built from the underlying set $\mathbb{Z}/10\mathbb{Z}$ together with two distinguished commutative magma operations (denoted $\mathrm{TSML}$, abbreviated $\mathrm{TS}$, and $\mathrm{BHML}$, abbreviated $\mathrm{BH}$) and an involution
$$
\sigma = (0)(3)(8)(9)(1\ 7\ 6\ 5\ 4\ 2)
$$
that fixes the set $\{0, 3, 8, 9\}$ and cycles the remaining six elements. Both magma operations are assumed to be defined explicitly in a companion submission "J02" (Sanders-Gish, "Joint Closure ... attractor on $\mathbb{Z}/10\mathbb{Z}$," cited as submitted to *Algebraic Combinatorics*); the present paper does not redefine them but uses them as given.

The paper introduces:

- A "corrected substrate frame" using $\mathrm{TS}_8$ (the $8 \times 8$ table on the index set $\{1, 2, 3, 4, 5, 6, 8, 9\}$) and the full $\mathrm{BH}_{10}$, with the cells labeled $V = 0$ and $H = 7$ treated as "flow cells between the tables."
- A four-cell role partition $F = \{1, 3, 5, 7, 9\}$, $S = \{2, 4, 8\}$, $T = \{6\}$, $V = \{0\}$.
- A reduction of $\mathrm{BH}$ to a $4 \times 4$ "role magma" $M_R$ on $\{V, F, S, T\}$ defined by mode-output of the role multiset.
- A "$\pm 21$ invariant" computed two ways: (a) row-asymmetry between the $\mathrm{TS}$ and $\mathrm{BH}$ tables (Computation A, summing to $+21$); (b) a period-to-trace map under a specific $2 \times 2$ matrix lift (Computation B, summing to $-21$).
- Four named theorems (Theorem 1.1 = D90 = $\mathrm{BH}$ diagonal as integer successor; Theorem 1.3 = D93 = "V is identity element of role magma"; Theorem 4.1 = trefoil characterization; Theorem 5.2 = $\sigma$-orbit decomposition $T_5 + T_3 = 15 + 6$; Theorem 5.3 = role decomposition $F_7 + F_6 = 13 + 8$ in Fibonacci numbers).
- A "honest negatives" section listing 10 claims (N1–N10) that have been checked and ruled out, with verification numbers attached.

The paper frames its content as sitting "inside" the arithmetic-topology / modular-knot territory of Morishita 2024, Ghys 2007, Katok-Ugarcovici 2007, Matsusaka-Ueki 2023, and Burrin-von Essen 2024, with the explicit and welcome disclaimer that the framework is "structurally analogous to" or "conceptually scaffolded by" these works rather than reproducing any theorem of them.

I read the manuscript end-to-end. The two magma operations are *not defined in the paper*; the paper assumes the reader has the J02 (companion) tables in front of them. I did not have access to J02 during this review and so could not verify the table-based theorems independently. I evaluated what I could from the structural claims and the verification scripts described.

---

## §2 — Decision recommendation

**Major revisions** (border with "Reject and resubmit").

The paper has several genuine pieces of finite algebra, mostly correct as stated:

- The role-magma $M_R$ on $\{V, F, S, T\}$ as defined in §3.1 is a clean object: a $4 \times 4$ commutative non-associative magma with a unique idempotent $V$ and a clear failure of associativity. This is the kind of small finite algebraic example that *Algebra Universalis* publishes regularly.

- The $\sigma$-orbit decomposition $15 + 6 = 21$ as triangular numbers $T_5 + T_3$ is a clean numerical observation, with the attached structural comment that it is forced by the linear period formula being honest.

- The "honest negatives" section (§7) is unusually self-aware for a finite-algebra paper and is a credit to the authors. The format — list of claims that *do not* hold, with verification statistics — is appropriate for *Algebra Universalis*.

But the paper has critical problems that a referee cannot wave through:

- (Issue 1) Neither $\mathrm{TS}$ nor $\mathrm{BH}$ is defined in the paper. The reader is referred to a companion "J02" that is itself a separate submission. *Algebra Universalis* requires self-contained submissions or, at minimum, an appendix or supplementary table giving the operations explicitly. As currently written, an editor cannot verify any computation in the paper without the unavailable companion.

- (Issue 2) The phrase "paradoxical information algebra" appears in the title, the abstract, and Theorem 3.3 (the "semi-factorization" theorem). The phrase is *not defined* in the paper as a class of algebraic structures. It is used as a name for the phenomenon "the role-magma $M_R$ is mode-deterministic on input pairs containing $V$ or $T$, but branches (multiple operator outputs reduce to a single role) on input pairs in $\{F, S\}^2$." This phenomenon is real, but the title's "paradoxical information algebras" suggests a defined class of algebraic objects, of which $M_R$ is an instance. It is not defined as such anywhere in the paper.

- (Issue 3) The "trefoil characterization" (Theorem 4.1) is presented without a notion of "trefoil-equivalent triple" being defined inside the paper. The text says "A triple $(a, b, c)$ is trefoil-equivalent under the runtime processor if and only if its multiset is $\{V, B, H\}$ or $\{V, B, B\}$." But "the runtime processor" is undefined; "trefoil-equivalent" is undefined; and no relation to the topological trefoil knot is established (only "structurally analogous to" — but the analogy is left for the reader to infer). The "proof" is "Parameter sweep over the $10^3 = 1000$ ordered triples; see trefoil_corrected_frame.py."

The paper, in its current form, is not a self-contained piece of universal algebra. It is a fragment of a larger investigation that depends on (a) the companion J02 paper for the magma definitions, (b) a "runtime processor" (which I infer from context is a simulation script) for the trefoil characterization, and (c) a body of "TIG synthesis" terminology (V, F, S, T roles; BREATH, HARMONY, COLLAPSE; "doubly-invariant subalgebra"; "wobble") that is internal to the project.

For *Algebra Universalis*, the paper would need to either (i) absorb J02's magma definitions and the runtime-processor / crossing-count formalism into a self-contained appendix, or (ii) rewrite to focus on just the role-magma $M_R$ as a small finite non-associative algebra, with the rest demoted to motivation or removed.

---

## §3 — Top-three issues

### Issue 1 (CRITICAL): The magma operations $\mathrm{TS}$ and $\mathrm{BH}$ are not defined in the paper

§1.1 ("The framework") references $\mathrm{TS}$ and $\mathrm{BH}$ as "two binary magma operations ... defined" in cite{SandersGishFourCore} (the J02 companion). The companion citation goes only as far as "submitted to *Algebraic Combinatorics*," 2026. No definition is reproduced.

Theorem 1.1 ($\mathrm{BH}$ diagonal as integer successor: $\mathrm{BH}(n, n) = n + 1$ for $n \in \{1, \ldots, 7\}$) is proved by "Direct table verification." Without the table, this proof is a citation to an external resource. Same for:

- Theorem 1.2 (period structure: $\mathrm{period}(n) = 7 - n$ for $n \in \{1, \ldots, 6\}$);
- Theorem 3.1 ($\mathrm{TS}_8$ image is $\{3, 4, 7, 8, 9\}$, $60/64$ Flow output);
- Theorem 6.1 (cusp agreement: 24 cells of $\mathrm{TS}_8$ domain agree, 40 disagree);
- Theorems 7.1, 7.2 (Irreducibility under CRT, no globally crossing-preserving swaps);
- Theorem 7.3 (algebraic independence: $\sigma$ is automorphism of $\mathrm{TS}$ at 17%, of $\mathrm{BH}$ at 48%);
- Honest negatives N4 ($\sigma$ automorphism), N5 (distributivity), N6 ($\mathrm{BH}$ → $\mathrm{TS}$ iteration), N9 (role partition / crossing count).

Each of these requires the explicit $\mathrm{TS}$ and $\mathrm{BH}$ tables. With them, each statement is verifiable in seconds (for two $10 \times 10$ tables on a 10-element set, every claim is a finite computation). Without them, the paper is uncheckable.

A self-contained *Algebra Universalis* submission must provide the tables. Two pages of tables (the $\mathrm{TS}_8$ on $\{1,2,3,4,5,6,8,9\}$ and the $\mathrm{BH}_{10}$ on $\{0,1,2,\ldots,9\}$) would suffice, in an appendix or even in §1 itself. The paper is roughly 12 pages without these tables; with them it is 14 pages and self-contained.

The README §3 says "Dependencies: J06" (the Crossing Lemma companion), but the manuscript itself depends on J02 (for the magma definitions) and J06 (for the Crossing Lemma framework). At minimum, the magma definitions from J02 must be reproduced; the J06 Crossing Lemma framing can stay as a reference if the present paper does not load-bear on it (and it does not — the role-magma analysis is independent of the Crossing Lemma claim in §3.3 Remark).

### Issue 2 (CRITICAL): "Paradoxical information algebras" is a name without a definition

The title is "LATTICE: Paradoxical Information Algebras on the $\mathbb{Z}/10\mathbb{Z}$ Substrate." The phrase "paradoxical information algebra" appears in:

- Title.
- Abstract: "a class of paradoxical information algebras."
- Theorem 3.3 statement: "Semi-factorization / paradoxical information."
- Remark after Theorem 3.3: "We call this a *paradoxical information algebra*: information content depends on whether inputs are at the boundary or in the interior."

The phrase is not defined as a mathematical object. The remark gives an *intuition* — that the role-magma $M_R$ has different behavior on boundary inputs vs. interior inputs — but it does not specify what algebraic structure constitutes a "paradoxical information algebra." Nothing tells the reader what the *class* of paradoxical information algebras is, what other examples exist, what the morphisms are, or whether any non-trivial theorems characterize the class.

For *Algebra Universalis*, this is fatal. *Algebra Universalis* is the venue for universal-algebra papers — papers that study classes of algebraic structures, varieties, free objects, equational theories, congruence lattices, etc. A paper introducing a new class of objects must define the class. The current manuscript names a class but does not define it.

Two paths forward:

(a) **Define the class.** Specify precisely the algebraic conditions under which a magma (or other structure) is "paradoxical-information." Give a formal statement of the boundary-vs-interior dichotomy. Show that $M_R$ satisfies these conditions. Survey other small examples (or prove that there is a smallest non-trivial example). This is real universal-algebra work, and if done well, would be a strong *Algebra Universalis* contribution.

(b) **Drop the class language.** Rewrite the paper as a study of the specific role-magma $M_R$ and its semi-factorization property. Title: "A small commutative non-associative magma on $\{V, F, S, T\}$ with role-deterministic boundary behavior." This is a smaller paper, but it would be a clean, honest *Algebra Universalis* note.

The current manuscript wants the breadth of (a) without the work; submitting it as-is invites a desk-reject for "naming a class without defining it."

### Issue 3 (CRITICAL): The "trefoil characterization" (Theorem 4.1) lacks any definition of trefoil-equivalence

Theorem 4.1 reads: "On the corrected substrate frame, a triple $(a, b, c)$ is *trefoil-equivalent under the runtime processor* if and only if its multiset $\{a, b, c\}$ is $\{V, B, H\}$ or $\{V, B, B\}$."

The proof: "Parameter sweep over the $10^3 = 1000$ ordered triples; see `trefoil_corrected_frame.py`."

What is missing:
- The runtime processor is not defined. It is presumably a piece of computer code that takes a triple of operators on $\mathbb{Z}/10\mathbb{Z}$ and computes some combinatorial / topological quantity. No specification is given.
- "Trefoil-equivalent" is not defined. The intuition (from §1.4 "Intellectual neighborhood" and from the title "trefoil characterization") is that the triple corresponds to a topological trefoil knot under some embedding of the magma into a knot-theoretic structure (e.g., a braid or modular-surface coding). But no embedding is specified.
- "$V$, $B$, $H$" — the elements $0$, $\mathrm{BREATH}=8$, $\mathrm{HARMONY}=7$. The renaming using single letters is opaque. (I had to read §1.1 carefully to decode "$B = 8 = \mathrm{BREATH}$" and "$H = 7 = \mathrm{HARMONY}$.")
- The phrase "All nine are $\mathrm{BH}$-associative" — meaning, presumably, that for each of these triples, $\mathrm{BH}(\mathrm{BH}(a, b), c) = \mathrm{BH}(a, \mathrm{BH}(b, c))$. This is verifiable from the table, *if* the table is provided (Issue 1).

Theorem 4.1 is a piece of empirical combinatorics: a brute-force search over 1000 triples found 9 triples satisfying some predicate that's only computable by a script. As written, it is not a theorem of universal algebra; it is a numerical observation.

For *Algebra Universalis*, the manuscript needs:
- A precise mathematical definition of "trefoil-equivalent" — preferably one that invokes only the magma operations and the involution $\sigma$, without reference to a "runtime processor."
- A proof (or at least a careful enumeration) that the predicate is precisely the set described, derivable from the magma's structure.
- A statement of why trefoil-equivalence is an interesting algebraic property — i.e., what theorem about the magma it expresses.

If trefoil-equivalence is, for instance, "the triple $(a, b, c)$ satisfies $\mathrm{BH}(\mathrm{BH}(a, b), c) = a$" (a 3-cycle / braid relation), then state this. If it's a more complex property of the runtime processor, then either describe the processor formally or remove this section.

The companion citation J06 (Crossing Lemma, Sanders-Mayes 2026, JCT-A or JPAA) is presumably the formal home of "crossing count" and related combinatorics. Reproducing the necessary definitions inline in J09 (one paragraph) would make the trefoil claim tractable. As currently written, the trefoil section is opaque.

---

## §4 — Major comments

### M1. The "$\pm 21$ invariant" is computed two ways with different signs and unclear identification

§5 ("The $\pm 21$ invariant and its two decompositions") computes:

- Computation A (Ghys-analog row-asymmetry): $\Psi_A(n) = \#\{j: \mathrm{TS}(n,j) > \mathrm{BH}(n,j)\} - \#\{j: \mathrm{BH}(n,j) > \mathrm{TS}(n,j)\}$, summing to $+21$.

- Computation B (period-to-trace under simple representative): $M_n = \begin{pmatrix} 1 & 1 \\ t-2 & t-1 \end{pmatrix}$ with $t = \mathrm{period}(n) + 2$, then $\Psi_B(n) = -(\mathrm{period}(n) - 1)$, summing to $-21$.

A "$\pm 21$" sign is not a stable invariant; it depends on a sign convention. The two computations give $+21$ and $-21$, not the same value with the same sign — they differ by an explicit sign flip that the manuscript glosses with the phrase "the $\pm 21$ invariant." Either:

(a) Show that Computations A and B are genuinely related — e.g., that both compute the same algebraic invariant up to a determinable sign — and explain the relation.

(b) Acknowledge that they are two unrelated quantities that happen to have the same absolute value, and explain the coincidence (if any).

The current "two decompositions of the substrate's $\pm 21$ invariant" framing implies (a) without proving it. The triangular decomposition $15 + 6 = 21$ (Theorem 5.2) is structurally forced by the period formula and is a cute observation. The Fibonacci decomposition $13 + 8 = 21$ (Theorem 5.3) is admitted to be canonical-specific (0 of 200 random commutative tables on $\mathbb{Z}/10\mathbb{Z}$ reproduce it; Theorem 5.4 robustness statement). The author has labeled this honestly. But the framing of two decompositions of "the $\pm 21$ invariant" should be tightened.

The §5.4 paragraph ("The lift to PSL(2, Z) — open") is appropriately humble: "Five strategies tested for lifting BH self-orbits to PSL(2, Z) words; none produces ±21 (§7 N1). The period-to-trace bridge under simple representative gives -21 numerically but is one choice of lift among many. Hypothesis, not derivation." This is the right tone, and it is a credit to the authors.

But the result of this paragraph is that the $\pm 21$ invariant has not been derived from any group-theoretic structure; it is a numerical coincidence between two distinct calculations. The paper should be more direct about this in §5: the title "the $\pm 21$ invariant and its two decompositions" should be softened to "two integer-21 calculations and their decompositions."

### M2. The "two-coding picture (TSML$_8$ vs BHML$_{10}$)" cusp-agreement claim (§6) is opaque

Theorem 6.3 ("Cusp agreement"): "The two magmas agree on $24/64$ cells of the $\mathrm{TS}_8$ domain (mostly routes leading to HARMONY) and disagree on $40/64$ in the interior."

This is a count: of the 64 cells in the $\mathrm{TS}_8$ domain, 24 satisfy $\mathrm{TS}(a, b) = \mathrm{BH}(a, b)$ and 40 do not. Without the tables, this is unverifiable. With the tables, it is a finite check.

The structural claim ("structurally analogous to Katok-Ugarcovici's geometric/arithmetic split") is left as analogy. The paper would benefit from:

- (a) Reproducing the tables (Issue 1 above).
- (b) Stating Theorem 6.3 as: "Of the 64 cells $(a, b) \in \{1,2,3,4,5,6,8,9\}^2$, the operations $\mathrm{TS}_8$ and $\mathrm{BH}$ agree on $24$ cells (listed: ...) and disagree on $40$ cells (listed: ...)."
- (c) Explaining why the 24 agreeing cells are "mostly routes leading to HARMONY" — that is, why $\mathrm{HARMONY} = 7$ is involved in many of the agreement cells. (One might guess this from the role partition, but the manuscript should say explicitly.)
- (d) Either removing the Katok-Ugarcovici analogy or giving a precise embedding of the substrate's two-coding picture into Katok-Ugarcovici's framework. Currently the analogy floats.

### M3. The role-magma $M_R$ is the most defensible piece — and should be the focus

§3 ("The role magma") introduces $M_R$ as a $4 \times 4$ commutative non-associative magma on $\{V, F, S, T\}$. Theorem 3.2 (commutativity, non-associativity) is a finite check on the explicitly-displayed table. The example $M_R(M_R(F, F), S) = F \ne T = M_R(F, M_R(F, S))$ is verifiable by hand from the table.

Theorem 3.3 (semi-factorization): "Boundary inputs (V or T) determine output role; interior inputs (F, S) require operator-level identity." This is a structural property of the role-magma that has both a clean statement and a clean proof (read off the $4 \times 4$ table).

§3 alone, expanded with the magma tables and a proper definition of "paradoxical information algebra" as a class, would be a small *Algebra Universalis* paper. I encourage the authors to consider rewriting the manuscript with §3 as the main content, demoting §4 (trefoil), §5 ($\pm 21$ invariants), §6 (two-coding), and §7 (irreducibility) to remarks, applications, or follow-up papers. The paper would then be tighter, more focused, and more clearly *Algebra Universalis* fare.

### M4. References to "TIG synthesis," "Volume H," "WP9," "D89/D90/D92/D93"

The manuscript refers to "Volume I," "WP9," and "D89, D90, D92, D93" in headings. These are internal reference IDs. *Algebra Universalis* readers will have no idea what they refer to. Either:

- (a) Remove these IDs from headings and theorem labels; they belong in a project-internal index, not in a journal submission.
- (b) Add a footnote explaining that these are project-internal IDs that map to the working-paper corpus (with a single citation to the synthesis document).

Option (a) is cleaner. The theorem labels can be plain (Theorem 1.1, 1.2, etc.) without "= D90" annotations.

### M5. "BREATH uniqueness" lemma (§4.2) is a side note that competes with the trefoil claim

The lemma "Among the structure cells {COUNTER, COLLAPSE, BREATH}, BREATH is the unique cell that produces trefoils when combined with VOID" is informative but is a one-line corollary of the trefoil characterization (Theorem 4.1). It does not deserve a separate lemma label. Demote to a remark.

The 4-element-level extension ("$(0, 7, 7, 9)$ is trefoil-equivalent without BREATH") is interesting, but the absence of BREATH from this triple-quadruple shows that the "BREATH only" rule is 3-element-specific (as the paper says) and therefore *not* a structural theorem of the role-magma. Acknowledge in the text that the BREATH-uniqueness rule is fragile.

### M6. The §1.4 "intellectual neighborhood" listing is honest but should be in §10 or removed

§1.4 lists Morishita 2024, Ghys 2007, Katok-Ugarcovici 2007, Matsusaka-Ueki 2023, Burrin-von Essen 2024, Lacasa et al. 2018 as "the territory in which this work sits." This is good context for an algebra paper but should be at the *end* of the paper as "Related work" or in §10 ("Open questions"), not in §1. *Algebra Universalis* readers prefer a tight introduction that gets to the math quickly.

Currently §1.4 sets up an expectation that the paper will engage with knot theory and the modular surface. The body of the paper does not actually do this — it studies a specific small magma and an involution. The §1.4 framing therefore undercuts the paper's actual scope. Move to §10.

### M7. Verification claims

The README mentions a verification script `verify_findings.py` with "0 failures, 0 warnings." The paper itself references `trefoil_corrected_frame.py` (§4), but no verification harness is described in the manuscript. *Algebra Universalis* does not require verification scripts (the venue is for theorem-proof papers), but if the paper is going to rest a theorem on a parameter sweep (as Theorem 4.1 does), the script should be described in a §Verification subsection with clear input-output specification. Otherwise the "proof: parameter sweep" should be replaced with a real proof.

### M8. The §2 "intellectual neighborhood" structural-analogy disclaimer is appropriate but underused

§1.4 last paragraph ("We use phrases like 'structurally analogous to' and 'conceptually scaffolded by' throughout; 'matches' and 'satisfies' are reserved for substrate-internal claims that we prove.") is excellent. The author has set the right epistemic standard. But the body of the paper does not always live up to it:

- Theorem 1.2 ("Period structure ... structurally analogous to cusp-winding step counts ... but the embedding in a specific Fuchsian group is unproven") — appropriately disclaimed.
- §6 "two-coding picture" — disclaimed via "structurally analogous to ... discrete combinatorial realization on $\mathbb{Z}/10\mathbb{Z}$, not a quotient of the modular surface itself."
- §5 "$\pm 21$ invariant" — labeled "Important caveat. The interpretation of $-21$ as a Rademacher invariant remains a hypothesis (see §7 N1)." Good.

These disclaimers are good. The remaining issue is that the paper still uses suggestive terminology ("trefoil-equivalent," "paradoxical information algebra," "the runtime processor") without disclaimers attached. The §1.4 epistemic standard should be applied uniformly to all suggestive terminology.

### M9. Per-venue cap statement

The README §5 says this is "2nd AlgUni paper after J14." If the paper is submitted as J09 and the cap-tracking has J14 first, that ordering makes sense within a project plan but should be clarified in the cover letter. *Algebra Universalis* does not have a per-issue cap on a single research group, but rapid-fire submissions from a single source can attract editorial attention. The cover letter should mention the parallel submissions briefly.

---

## §5 — Minor comments

### m1. The "lattice" in the title is a name, not a structural reference

The paper studies the LATTICE operator (= the index-1 operator of $\mathrm{BH}$), but the word "lattice" in the title evokes lattice theory (partial orders, meets, joins). The manuscript does *not* study lattices in that sense. Consider retitling — e.g., "The LATTICE operator and the role-magma on $\mathbb{Z}/10\mathbb{Z}$" — or providing a one-line clarification in the abstract that "LATTICE" here is a named operator, not a generic order-theoretic structure.

### m2. The $\sigma$ involution

The involution $\sigma = (0)(3)(8)(9)(1\ 7\ 6\ 5\ 4\ 2)$ is described as a 6-cycle plus four fixed points. This is *not* an involution in the standard sense (an element of order 2). A 6-cycle has order 6, not 2. The involutory property "$\sigma^2 = \mathrm{id}$" does not hold here. Either:
- (a) Use the word "permutation" instead of "involution."
- (b) Verify whether $\sigma$ is supposed to denote $\sigma$ or $\sigma^3$ (which would have order 2 and be a genuine involution if $\sigma$ has order 6).

This is a definitional confusion that needs to be sorted out in §1.1.

### m3. The $\mathrm{TS}_8 + \mathrm{BH}_{10} + V/H$ "corrected frame"

§1.2 says: "the substrate uses $\mathrm{TS}_8 = \mathrm{TS}_{10}$ with rows/cols $\{0, 7\}$ removed." This is presumably the result of removing the rows/columns indexed by 0 and 7 from the original $10 \times 10$ table. The rationale for this removal — that "the cells $V = 0$ and $H = 7$ are flow cells between the tables, not interior entries" — is intuitive but not formally specified. The reader should be told *why* removing these rows/columns is the right thing to do (e.g., "$\mathrm{TS}_{10}$ has $V$ and $H$ as absorbing fixed points, and the algebra's interior structure is captured by the restricted table"). Currently this is left for the reader to infer from the surrounding text.

### m4. The Fibonacci numbering

§5.3 (Theorem 5.3): $\sum_{n \in F} \Psi_B(n) = -F_7 = -13$, $\sum_{n \in S} \Psi_B(n) = -F_6 = -8$, total $-F_8 = -21$. The Fibonacci numbering used here is $F_6 = 8, F_7 = 13, F_8 = 21$, which corresponds to the convention $F_1 = 1, F_2 = 1, F_3 = 2, F_4 = 3, F_5 = 5, F_6 = 8, F_7 = 13, F_8 = 21$. (Some texts use $F_0 = 0$ and shift the index by 1.) State the convention.

### m5. The verification statistics N4–N8

The honest negatives say:
- N4: $\sigma$ is automorphism of $\mathrm{TS}$ at 17%, of $\mathrm{BH}$ at 48%.
- N5: $\mathrm{TS}$ and $\mathrm{BH}$ distribute 19.5% (on what space?).
- N6: $\mathrm{BH}$ iteration converges to $\mathrm{TS}$ for 28/64 starts.
- N7: substrate factors through $\mathbb{Z}/2 \times \mathbb{Z}/5$: no.
- N8: Fibonacci role decomposition: 0/200 random tables.

These percentages and counts are suggestive but not quite mathematical statements. "$\sigma$ is automorphism at 17%" is a claim that 17% of cells satisfy $\sigma(\mathrm{TS}(a, b)) = \mathrm{TS}(\sigma(a), \sigma(b))$, which is a precise count if you know the table and the action. State the precise count (e.g., "of the 100 cells of $\mathrm{TS}_{10}$, 17 satisfy the automorphism condition") rather than the percentage.

### m6. Open questions

§8 lists four open questions. They are all sensible. Question 4 ("Burrin-von Essen Fuchsian-group lift") is the most substantive; questions 1 ("Principled lift to PSL(2, Z)") and 4 are essentially the same question phrased differently. Consider merging.

### m7. The bibliography has 10 entries, of which 4 (SandersGishFourCore = J02, SandersMayesCL = J05/J06, TIGsynthesis2026 = the github repo, and the other Sanders/Mayes/Gish self-citations) are internal. The 6 external citations (Burrin-von Essen 2024, Ghys 2007, Ishida-Kuramoto-Zheng 2024, Katok-Ugarcovici 2007, Lacasa et al. 2018, Matsusaka-Ueki 2023, Morishita 2024) are mostly recent papers in modular-surface / Rademacher-symbol / arithmetic-topology.

The Ishida-Kuramoto-Zheng 2024 ("Density of Borromean prime triples") is cited under N3 ("TIG matches Borromean prime conditions"); the citation is appropriate.

The Lacasa 2018 ("Symbolic dynamics on residue sequences") is cited in §1.4 as a member of the intellectual neighborhood. It is invoked nowhere else. If unused, demote to "for further reading" or remove.

The DOI-only citation `10.5281/zenodo.18852047` for "TIG synthesis" is to the project's GitHub repository on Zenodo. *Algebra Universalis* prefers a stable archival reference (a published paper, an arXiv preprint, or a cited DOI for a published artifact). Cite a specific document on the repository (with a path) rather than the bundle DOI.

### m8. Theorem 3.1 statement: $\mathrm{BH}(n, n) = n + 1$ "for each $n \in \{1, ..., 7\}$"

This fails at $n = 8$ because $\mathrm{BH}(8, 8) = 7$ (per the boundary clause). State this directly in the theorem: "$\mathrm{BH}(n, n) = n + 1$ for $n \in \{1, ..., 6\}$, and $\mathrm{BH}(7, 7) = 8$" (if that's the actual value) or specify the boundary clause. The current "for each $n \in \{1, 2, 3, 4, 5, 6, 7\}$" with $\mathrm{BH}(7, 7) = 8$ implicitly is plausible but should be made explicit.

(I am inferring the value at $n = 7$ from the pattern; without the table, I cannot verify it.)

---

## §6 — Literature check

The paper sits in the territory of:

- **Modular surface symbolic dynamics.** Katok and Ugarcovici, "Symbolic dynamics for the modular surface," *Bull. AMS* 44 (2007), 87–132 — the framework of geometric vs. arithmetic codings of the modular surface. The paper cites this and uses "structurally analogous" language correctly.

- **Knot theory and number theory.** Morishita, *Knots and Primes* (2nd ed., 2024). This is the standard reference for the analogy between knots and primes; the paper cites it and uses appropriate scaffolding language.

- **Modular knots and dynamics.** Ghys, "Knots and dynamics," *Proc. ICM Madrid* 2007 — the geometric framework relating modular knots to dynamics on the modular surface. Cited.

- **Rademacher symbols.** Matsusaka and Ueki, "Rademacher symbols for triangle groups," 2023; Burrin and von Essen, "Cusp winding and the Rademacher symbol," 2024. These are recent and cited.

The paper's substrate-internal claims do not depend on the cited literature for proofs (the disclaimer in §1.4 is correct). The cited literature provides analogical scaffolding only. This is appropriate scholarship.

What is *missing* from the literature review:

- **Universal algebra of small magmas.** The paper studies a finite commutative non-associative magma with about 100 cells. There is a sizable literature on small finite magmas (commutative loops, quasigroups, groupoids):
  - Phillips and Vojtěchovský, "C-loops: an introduction," *Publ. Math. Debrecen*, 2006.
  - Drápal, various papers on non-associative magmas (1992, 1990s, 2000s).
  - Smith, *An Introduction to Quasigroups and Their Representations*, Chapman & Hall/CRC, 2007.
  - Mc Inerney and Mc Pherson on small commutative magmas.
  - Stanley, *Enumerative Combinatorics*, Vol. I, ch. 1, on magma counting.

  None of these are cited. *Algebra Universalis* readers will expect at least a brief acknowledgement of the small-magma literature.

- **Role partitions in algebra.** The role partition $F = \{1,3,5,7,9\}$, $S = \{2,4,8\}$, $T = \{6\}$, $V = \{0\}$ is a four-block partition of $\mathbb{Z}/10\mathbb{Z}$. The choice of partition appears to be motivated by external considerations (the TIG framework's "operator roles"). For *Algebra Universalis*, the natural question is: why this partition? Is it a congruence of either magma? (The paper shows in §3 that mode-reduction gives a $4 \times 4$ magma table $M_R$, which is suggestive but not the same as a congruence.) Is it an algebraically meaningful partition or a labeling-by-fiat?

  Bénabou, Mac Lane, and others on partition algebras would be relevant. None are cited.

The paper's intellectual neighborhood section (§1.4) covers modular knots and dynamics — territory adjacent to where the paper claims structural analogies — but does not cover the universal-algebra / small-magma literature where the actual mathematics lives. Add at least one reference to the small-magma / quasigroup literature to ground the paper for an *Algebra Universalis* audience.

---

## §7 — Estimated revision effort

I see two viable revision paths.

**Path A (Major Revisions, ~2 months work).** Make the paper self-contained. This requires:
- Reproducing the $\mathrm{TS}_8$ and $\mathrm{BH}_{10}$ tables in an appendix (1–2 days of typesetting).
- Defining "paradoxical information algebra" as a class of algebraic structures (or removing the term from the title and abstract; ~1 week of conceptual work).
- Defining "trefoil-equivalent" without reference to a "runtime processor" (or removing the trefoil section entirely; ~1 week).
- Resolving the involution / 6-cycle ambiguity in §1.1 (a few hours).
- Tightening the $\pm 21$ framing (a few days).
- Adding a small-magma literature review (a few days).
- General typographical and clarity edits (a week).

After these revisions, the paper would be a credible *Algebra Universalis* submission. The role-magma core (§3) is already strong; the rest of the paper would need to live up to that standard.

**Path B (Reject and resubmit as a smaller paper, ~3 weeks work).** Rewrite the manuscript as a focused study of the role-magma $M_R$. Title: "A small commutative non-associative magma on a four-element set with role-deterministic boundary behavior" or similar. Drop the trefoil, $\pm 21$ invariants, two-coding picture, and irreducibility sections. Result: a 6–8 page note in *Algebra Universalis* (or possibly a shorter venue like *Semigroup Forum*).

I lean toward recommending Path B if the authors are pressed for time. Path A is the right ambition if there is time and motivation; Path B captures the most defensible mathematics quickly.

---

## §8 — Venue bar: does this clear *Algebra Universalis*?

*Algebra Universalis* publishes papers on universal algebra, lattice theory, and related areas. The bar is approximately: a clearly defined class of algebraic structures (or a specific structure of independent interest), with theorems about that class, with proofs that an algebraist can follow without external dependencies.

The present manuscript does *not* clear this bar as currently written, for the reasons in §3:
- Issue 1: the magma tables are not in the paper.
- Issue 2: the named class "paradoxical information algebras" is not defined.
- Issue 3: the trefoil characterization is a numerical observation about an undefined "runtime processor."

After Path A revisions, the paper would clear the bar. After Path B revisions, the paper would clear a slightly lower bar (for a focused note rather than a class-theoretic paper).

I do not recommend acceptance at *Algebra Universalis* in any form without revisions. The honest choices are Path A or Path B above.

---

**End of report.**

*Reviewer disclaimer: I have read this manuscript in good faith as an algebraist with no prior exposure to the broader research framework cited as "TIG / CK." I attempted to evaluate the mathematical content of the submitted file alone, treating the J02 and J06 companion citations as unverified placeholders. I did not have access to the magma tables, so I could not independently check the table-based theorems; I evaluated only the structural content I could verify from the manuscript directly. Where I could not verify a claim from the file alone, I have said so.*
