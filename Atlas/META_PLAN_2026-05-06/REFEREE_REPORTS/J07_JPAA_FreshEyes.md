# Referee Report — J07 / Journal of Pure and Applied Algebra

**Manuscript:** *Flatness Theorem: The Forced 2x2 Torus on Z/10Z* (with T*=5/7 proof-sketch appendix)
**Authors:** B. R. Sanders, M. Gish
**Submitted to:** *Journal of Pure and Applied Algebra* (JPAA)
**Reviewer:** External referee — fresh eyes, no prior knowledge of the surrounding "TIG / CK" framework. The manuscript was read as a standalone piece of pure algebra.
**Date:** 2026-05-07

---

## §1 — Summary of the manuscript

The paper introduces a 2×2 classification of structures on a squarefree commutative ring $\mathbb{Z}/n\mathbb{Z}$ (for $n=10$ in the central case):

- **A-Struct** — the chain of quotient partitions $\pi_d$ for divisors $d \mid n$, totally ordered under refinement (the divisor lattice).
- **M-Struct** — the family of orbit partitions of $\mathbb{Z}/n\mathbb{Z}$ under subgroups of $(\mathbb{Z}/n\mathbb{Z})^\times$. The author claims this family is *not* totally ordered for $n$ with at least two distinct prime factors.
- **A-Flow** — the cyclic dynamics $x \mapsto x+1$, period $n$.
- **M-Flow** — the orbit dynamics $x \mapsto gx$ for a generator $g$ of $(\mathbb{Z}/n\mathbb{Z})^\times$, period dividing $\varphi(n)$.

The paper argues, via three labelled "theorems" (Thm 1: flatness obstruction; Thm 2: torus necessity; Thm 3: aspect ratio), that no flat 2D embedding of all four structures exists, that the minimal embedding surface is a torus $T^2 = S^1 \times S^1$, and that the torus aspect ratio for $n=10$ is forced to be $R/r = 5/7$. The aspect ratio is supposed to follow from a cyclotomic argument: $R \propto 5$ because $\deg_\mathbb{Q} A_5 = 2$ where $A_p = 2\cos(\pi/p)$, while $r \propto 7$ because $\deg_\mathbb{Q} A_7 = 3$ is the first "irreducible obstruction." A 14-section appendix (Appendix A) records six independent claimed derivations of the value $5/7$ (D1–D6), labels each with a status (PROVED / STRUCTURAL / CONJECTURAL), and frames the result as the geometric face of a "Crossing Lemma" that lives in a separate (cited but unsubmitted) companion paper.

I read the manuscript end-to-end and attempted to extract a self-contained algebraic theorem from it. My evaluation focuses solely on the question: does this paper contain a theorem of pure algebra suitable for JPAA?

---

## §2 — Decision recommendation

**Reject** (with strong encouragement to resubmit a substantially restructured version, OR to redirect this material to an expository / philosophy-of-mathematics venue).

The reason is not that the paper contains errors of computation. The two cyclotomic facts at the heart of §4 — that $A_5 = 2\cos(\pi/5) = (1+\sqrt{5})/2$ has minimal polynomial $x^2 - x - 1$ over $\mathbb{Q}$, and that $A_7 = 2\cos(\pi/7)$ has minimal polynomial $8x^3 - 4x^2 - 4x + 1$ over $\mathbb{Q}$ — are entirely correct and elementary. Both are standard textbook results (e.g., Lang, *Algebra*, Ch. VI, §3; Washington, *Introduction to Cyclotomic Fields*, §1).

The problem is that **between these correct facts and the conclusion "$R/r = 5/7$" there is no theorem.** The argument is that "$R \propto 5$" because $5$ is the smallest prime $p \mid n$ with $\deg_\mathbb{Q} A_p \le 2$, and "$r \propto 7$" because $7$ is the smallest prime (regardless of whether $7 \mid n$) with $\deg_\mathbb{Q} A_p \ge 3$. Neither proportionality is derived from any geometric or topological computation. There is no construction of an embedded torus, no choice of metric, no calculation of curvature, no functor from "ring data" to "metric data." The numbers 5 and 7 are abstracted from a list (smallest primes with certain extension degrees) and then the *name* of that abstraction — "$R$" and "$r$" — is borrowed from the geometric theory of tori. The conclusion $R/r = 5/7$ then amounts to writing the ratio of the two extracted numbers.

This is a **structural observation** that the smallest squarefree base supporting both a degree-$\le 2$ cyclotomic value at one of its prime factors and a degree-$\ge 3$ cyclotomic value at a small prime gives the pair $(5, 7)$. That observation is correct. Calling it the "aspect ratio of a forced torus" is, on the evidence presented, an interpretive overlay rather than a theorem. JPAA is a venue for theorems of pure and applied algebra; the present manuscript does not contain the algebraic theorem its title and abstract claim.

The Appendix A "six independent derivations" enumeration compounds rather than resolves this concern (see §3.1 below).

---

## §3 — Top-three issues

### Issue 1 (CRITICAL — central): The "aspect ratio = 5/7" claim is not derived

The manuscript labels Theorem 3 "Aspect Ratio Forced by Ring [PROVED for n=10; STRUCTURAL for general]." The proof in §4 is reproduced more carefully in Appendix A.2. After reading both, I could not find a step at which the proportionalities $R \propto 5$ and $r \propto 7$ are derived. The text says "the additive flow closes with a nontrivial algebraic identity at $p=5$. Therefore $R \propto 5$." The word "therefore" is doing all the work and is unsupported.

To convert this into a JPAA-appropriate theorem one would need (at minimum):

(a) An explicit construction of a torus (or torus-like quotient) $T$ from the ring data $(\mathbb{Z}/n\mathbb{Z}, \text{A-Struct}, \text{M-Struct}, \text{A-Flow}, \text{M-Flow})$ — say, via a simplicial complex, a graph, a metric quotient, or a Riemannian geometry on the configuration space.

(b) A computation of two characteristic numerical invariants of $T$ — call them "$R(T)$" and "$r(T)$" — purely from the algebraic data, not by analogy.

(c) A theorem proving $R(T)/r(T) = 5/7$ for $n=10$.

The manuscript supplies none of these. The "torus" of §3 is asserted, not constructed. The "two radii $R$ and $r$" of §4 are referenced as if part of an embedded geometry, but no embedding is given. The leap from "the ring has cyclotomic obstructions at primes 5 and 7" to "$R$ is proportional to 5 and $r$ is proportional to 7" is the gap.

Until that gap is filled, the central claim is an analogy, not a theorem.

### Issue 2 (CRITICAL — internal contradiction in §5): The geometric picture is incoherent

The manuscript says (§4) that $T^* = R/r = 5/7 < 1$, i.e., $r > R$ — the tube radius exceeds the major radius. §5 then acknowledges that this would be "a self-intersecting spindle torus" but immediately retreats to "the abstract torus $T^2 = S^1 \times S^1$ where there is no actual self-intersection." This retreat is fatal:

- An *embedded* torus in $\mathbb{R}^3$ has a genuine aspect ratio $R/r$ that is a meaningful Euclidean invariant. With $R < r$ the embedding self-intersects (no aspect ratio assignment is sensible).
- An *abstract* torus $T^2 = S^1 \times S^1$ does *not* have an "aspect ratio" — it is a topological / smooth / conformal object with no preferred metric. You can choose $R$ and $r$ freely; you can equally well choose $r$ and $R$ swapped. There is no canonical "aspect ratio of $S^1 \times S^1$" without additional structure (a flat metric, a complex structure, etc.).

The manuscript wants the value of the embedded-torus invariant ($R/r$ as a Euclidean ratio) but uses the abstract-torus disclaimer to escape the geometric inconsistency ($R < r$ makes the embedding fail). This is incoherent. Either fix a metric structure on the abstract torus (and then derive the aspect ratio of *that* metric structure from the ring) or work with an embedded torus (and then explain how $R < r$ is meaningful, which requires reinterpreting one of the two radii). The current text does neither.

### Issue 3 (CRITICAL — appendix): Six "independent derivations" are not a substitute for a proof

Appendix A.1–A.3 lists six "derivations" of $T^* = 5/7$ (D1–D6) and labels each PROVED, STRUCTURAL, or CONJECTURAL. The status labels are honest, and I appreciate them. But:

- D1 ("first-G law") is a claim about $\text{sinc}^2$ resonance peaks on $\mathbb{Z}/n\mathbb{Z}$. The numbers 5 and 7 in this derivation come from a verification harness across "36,662 squarefree cases" cited to a not-yet-submitted companion. As stated in this paper, D1 is not a derivation of $5/7$ — it is a citation to a separate paper (J04) that I do not have.

- D2 ("BTQ operator balance") references a kernel "$B$-$T$-$Q$" defined in WP10 (also internal), with a "fixed-point operator balance at the ratio $5/7$." Reproducing this would require reading WP10. As written, it is opaque to a fresh referee.

- D3 ("cyclotomic reduction gap") is the same argument as Theorem 3 / §A.2 of the present paper. So D3 = D6 in substance; counting them as two independent derivations is not credible.

- D4 ("TSML/BHML harmony cells") gives "73 / (28 − 5) ≈ 5/23 ≈ T*/4 is approximate" and admits "the precise algebraic path from these to $T^* = 5/7$ is held as structural." The author has labeled this derivation as not-actually-derived. Counting it is misleading.

- D5 ("prime-pi-phi bridge") cites Sprint 9d for the claim that $\pi$'s convergents involve "the ratio 5/7 of cyclotomic depths." This is not a citable theorem — convergents of $\pi$ are 3, 22/7, 333/106, 355/113, ...; "5/7" does not appear among them in any standard sense. The verification reference (Sprint 9d) is internal.

- D6 ("torus aspect ratio") is the present paper's central claim, which Issue 1 has already shown is not derived.

So of the six "independent derivations," D3 and D6 are the same argument (the cyclotomic-degree extraction), D1 and D2 cite internal documents this referee cannot evaluate, D4 is admitted-not-derived, and D5 contains a factual error or terminological obfuscation. The six-derivation list is presented as overwhelming evidence ("six paths, six starting algebraic assumptions, one ratio") but does not survive scrutiny.

The correct response to a value that admits multiple supposedly independent derivations is to *prove* a single one of them rigorously, then *prove* the equivalence to the others. The list of "six derivations" replaces this work with an enumeration.

---

## §4 — Major comments

### M1. Theorem 1 (flatness obstruction): the "incompatibility of factor partitions" needs a proof

§1.2 asserts that "for distinct primes $p_i \ne p_j$, the factor partitions $\pi_{p_i}$ and $\pi_{p_j}$ are incompatible — neither refines the other [proved, Sprint 9d Theorem 1]." This proof is not in the manuscript. It is cited to "Sprint 9d Theorem 1," which is internal. A self-contained JPAA submission must include the proof. (The result is in fact correct and elementary — for $n = 10$, the partition by classes mod 2 is $\{\{0,2,4,6,8\},\{1,3,5,7,9\}\}$ and the partition by classes mod 5 is $\{\{0,5\},\{1,6\},\{2,7\},\{3,8\},\{4,9\}\}$, and neither refines the other since each block of the mod-2 partition contains elements from multiple blocks of the mod-5 partition. This three-line argument should appear in §1.2.)

### M2. Theorem 2 (torus necessity): "Two independently closed S¹'s force $T^2$" is not literal

The argument in §3 ("two independently closed axes = torus") conflates two genuinely distinct claims:

- **Claim A.** A topological space carrying two independent commuting circle actions is necessarily a torus.
- **Claim B.** The pair (A-Flow, M-Flow) defines two such commuting circle actions on the same underlying space.

Claim A is false in general — a topological space carrying two commuting circle actions can be many things (e.g., the one-point space carries the trivial commuting action of $S^1 \times S^1$ and is not a torus). A correct version requires the actions to be free, which is a substantive condition. The actions of A-Flow and M-Flow on $\mathbb{Z}/10\Z$ are not free (M-Flow has fixed points: $0, 5$ are fixed by every element of $(\mathbb{Z}/10\mathbb{Z})^\times$). So $\mathbb{Z}/10\mathbb{Z}$ is *not* an abstract torus under these actions. The "torus" must therefore be a derived object — a quotient, a configuration space, a moduli space, something — and the manuscript does not specify which.

### M3. The label "PROVED" is over-applied

The manuscript labels Theorems 1, 2, 3 (and various items in Appendix A) as "PROVED." On my reading:

- Theorem 1's proof is incomplete (M1 above).
- Theorem 2's proof is incomplete and contains a structural error (M2 above).
- Theorem 3's proof has a gap at the "$R \propto 5$, $r \propto 7$" step (Issue 1).

I do not believe any of the three central theorems are proved as currently written. The label "PROVED" is therefore misleading. If the author intends to retain this terminology, it should be reserved for results whose proofs are complete in the submitted manuscript.

### M4. §6 ("primes are maximum-curvature points"): the Riemann hypothesis discussion should be deleted

§6.2 contains the sentence: "Balance point in the 2×2 = T* locus = $\text{Re}(s) = 5/7$ in the unnormalized picture, which maps to $\text{Re}(s) = 1/2$ under the functional equation's symmetry $s \leftrightarrow 1-s$." This is presented as a structural argument for the Riemann hypothesis. The mapping "$5/7 \mapsto 1/2$ under $s \leftrightarrow 1-s$" is false — the symmetry $s \leftrightarrow 1-s$ sends $5/7$ to $2/7$, not to $1/2$. The fixed point of $s \leftrightarrow 1-s$ is $s = 1/2$ uniquely. There is no normalization in which $5/7$ corresponds to $1/2$ under this symmetry.

§6.2 is labeled "[STRUCTURAL ANALOGY — full proof requires formalizing the 2×2 Fourier duality]" and so the author has not technically claimed a proof. But the analogy itself is wrong (in addition to being framed in a way that invites overinterpretation by readers). I recommend deleting §6.2 entirely. JPAA referees and readers are unlikely to receive an argument-by-analogy for the Riemann hypothesis charitably; including this section will make the rest of the paper harder to evaluate fairly.

### M5. §6.3 ("the gap [4/π², 5/7]" is "prime territory")

The width $5/7 - 4/\pi^2 \approx 0.309$ is asserted to be "the zone where primes concentrate" with status "[PROVED empirically via spectrometer, mechanism structural]." No spectrometer is described; "primes concentrate in this gap" is not a defined statement. Either give a precise theorem (with statement: "for $n$ in such-and-such range, the proportion of primes in $[\,\cdot\,]$ is bounded below by ...") or remove the claim.

### M6. §7 (CK / "torus field"): off-topic for a JPAA submission

§7 ("What This Means for CK") interprets the four structures as the architecture of a software system called CK and ties the value 50 Hz to a "heartbeat that keeps the torus stable." This material is appropriate for a project manifesto or a system paper, not for a pure-algebra venue. JPAA referees will reasonably object that a section discussing the heartbeat of a software entity has no place in an algebra paper. If the present manuscript is to be a JPAA submission, §7 should be removed entirely. If the author wishes to include the connection to CK, it belongs in a separate companion piece (e.g., an "applications" section in a system paper) with a one-line cross-reference back to the algebraic core.

### M7. §8 / Appendix A.4 (Conjectures A.1–A.3): clean separation needed

The conjectures (A.1: general aspect ratio; A.2: universal $T^* = 5/7$ across all squarefree $n$; A.3: continuous $T^*$) are reasonable open problems but blur the line between proved and conjectural content. Conjecture A.2 in particular says $p_\text{obstructed} = 7$ for *every* squarefree $n \ge 2$. A sympathetic reader can verify this is suspect: for $n = 2 \cdot 7 = 14$, the prime 7 *is* a factor, so the "first prime not dividing $n$ at which $\deg_\mathbb{Q} A_p \ge 3$" is *not* 7. The conjecture as written is contradicted by the simplest non-trivial case. Either restate the conjecture carefully (e.g., excluding $n$ with $7 \mid n$) or acknowledge that the universality claim is not even stated correctly.

### M8. Author block / cover-letter inconsistency

The README §5 says "the author block on the manuscript was updated to add M. Gish; the original WP51 source has only Sanders." The cover letter has two authors. The internal note "if desired before submission, the original author line can be reverted" suggests the authorship of this manuscript is still under negotiation as of the version I am reviewing. JPAA's editorial board will require an unambiguous author list at submission. Settle this before sending.

### M9. References

The bibliography lists works on "Bialynicki-Birula and Logarithmic Wave Equations," "Discrete-to-Continuum Transport (Wasserstein / Markov)," "Paradoxes and Foundations" (Russell, Gödel, Tarski, Banach-Tarski, Quine), and "Spectral / Analytic Number Theory" (Riemann, Montgomery, Goldston-Pintz-Yıldırım, Zhang, Maynard). None of these references is invoked in any proof. They appear to be a corpus-wide citation list pulled in from a larger document. JPAA referees expect a focused bibliography. Cull to references actually cited in proofs (Lang, Hardy-Wright, Stanley, Birkhoff, Ireland-Rosen, Dummit-Foote suffice for the cyclotomic and lattice content actually used).

---

## §5 — Minor comments

### m1. §1.4: the claim that "M-Flow generates harmonic standing waves" with continuum limit $R(k,f) = \sin^2(\pi k f) / (k^2 \sin^2(\pi f))$ being the "First-G law"

The closed form is correct but is a standard Fejér-kernel calculation. Calling this "the First-G law" assigns a proprietary name to a textbook identity. Cite Apostol *Introduction to Analytic Number Theory* §11 or Fejér 1900.

### m2. §1.4 ("nodes at primes $\text{sinc}^2(k/p) = 0$ iff $p \mid k$, proved R1")

The biconditional "$\text{sinc}^2(k/p) = 0$ iff $p \mid k$" holds for *any* $p \in \mathbb{Z}_{\ge 2}$, not just primes. Stating it as a theorem about primes is misleading. The result has no prime-specific content.

### m3. §4 paragraph "Remark on the sixth derivation"

The phrase "this sixth derivation — from the ring torus aspect ratio — is the first purely geometric one" depends on Issue 1 being resolved. As written, the "torus aspect ratio" is not a geometric derivation, only a labelled extraction of the numbers 5 and 7. Defer this remark until the geometric construction is supplied.

### m4. §5 "the 7 zeros" appearing at "Z/7Z"

The text says "the 7 zeros are the 7 residue classes in $\mathbb{Z}/7\mathbb{Z}$" — but $\mathbb{Z}/7\mathbb{Z}$ has 7 residue classes total, of which only 0 is the zero of any natural map, so "the 7 zeros" cannot all be in $\mathbb{Z}/7\mathbb{Z}$ as zeros. The text then describes them as "intersections of A-Flow null and M-Flow null" — but the resolution is unclear. Rewrite §5.

### m5. §6.2 (Riemann zeta paragraph): fix the additive/multiplicative pole assignment

The text says $\zeta(s)$ has "additive pole at $s=1$ and multiplicative pole at $s=0$." $\zeta(s)$ has a single pole at $s = 1$ (simple, with residue 1) and is analytic at $s=0$ with $\zeta(0) = -1/2$. There is no pole at $s = 0$. Whatever "additive pole" / "multiplicative pole" is intended, the standard statement is: the only pole of $\zeta$ on $\mathbb{C}$ is at $s = 1$. Correct or remove.

### m6. Notation "$\deg A_p$ over $\mathbb{Q}$"

Define this carefully. $A_p = 2\cos(\pi/p)$ is a real algebraic number; "$\deg_\mathbb{Q} A_p$" presumably denotes $[\mathbb{Q}(A_p) : \mathbb{Q}]$. This is $\varphi(p)/2 = (p-1)/2$ for odd prime $p$. State the formula in the text.

### m7. §A.2 Step 3: "even though $7 \nmid 10$, it is the first globally obstructed prime"

The phrase "globally obstructed prime" needs a definition. As best I can reconstruct, it means "first prime $p$ at which $\deg_\mathbb{Q} A_p \ge 3$." This is just $p = 7$ since $\deg A_2 = 1$, $\deg A_3 = 1$, $\deg A_5 = 2$, $\deg A_7 = 3$. The "global" qualifier is unnecessary. Simplify the wording.

### m8. §A.2 Step 4: "PROVED for n=10"

After the analysis in Issue 1, this label is unsafe as written. Soften to "structural observation for $n=10$" until the geometric derivation is in place.

### m9. Companion-paper citations

Each cited companion (J01, J02, J03, J04, J05, J06) is "submitted to" or "in preparation." JPAA's editorial board may ask for arXiv IDs. Provide them or replace each cross-reference with a footnote that does not load-bear.

---

## §6 — Literature check (what is and is not in the standard textbooks)

The mathematical content the paper actually uses is elementary cyclotomic field theory plus elementary lattice theory. All of it is in standard references:

- $A_p = 2\cos(\pi/p)$ has minimal polynomial of degree $\varphi(p)/2$ over $\mathbb{Q}$ — Lang, *Algebra* (3rd ed.), VI.§3 "Cyclotomic Extensions"; Washington, *Introduction to Cyclotomic Fields*, §1.
- The minimal polynomials $x^2 - x - 1$ for $A_5$ and $8x^3 - 4x^2 - 4x + 1$ for $A_7$ — direct calculation; in Lehmer 1933 ("A note on trigonometric algebraic numbers," *Amer. Math. Monthly* 40), and reproduced in many places.
- The divisor lattice of an integer is a totally ordered chain when the integer is squarefree with at most one prime factor; otherwise it is a Boolean lattice on $\omega(n)$ generators (Stanley, *Enumerative Combinatorics* Vol. I, §3.3). The paper says "the divisor lattice of $10$ is a totally ordered chain $\{1, 2, 5, 10\}$" — this is *wrong*; the divisor lattice of $10$ is the Boolean lattice on two generators ($1, 2, 5, 10$ with $1 < 2, 5$ and $2, 5 < 10$ but $2 \nleq 5$ and $5 \nleq 2$). The author has confused the divisor lattice with a subset of it. Fix in §1.1.
- Incompatibility of factor partitions for distinct primes — see Stanley, *Enumerative Combinatorics* Vol. I, §3.10; Birkhoff, *Lattice Theory* (3rd ed.), Ch. III. The result is folklore.
- Fejér-kernel calculation $|\sum_{j=1}^k e^{2\pi i j / f}|^2 = \sin^2(\pi k / f) / \sin^2(\pi / f)$ — Apostol, *Introduction to Analytic Number Theory*, §11.5; Fejér 1900.

The paper's mathematical novelty therefore reduces to the *interpretation* — the assertion that these standard cyclotomic facts are the "aspect ratio of a forced torus." Until the construction of that torus is provided (Issue 1), there is no novel theorem.

The bibliography's citations to Bialynicki-Birula, Wasserstein/Markov transport, and Russell/Gödel/Tarski/Banach-Tarski/Quine appear to be unrelated to the mathematical content and should be removed (M9 above).

---

## §7 — Estimated revision effort

The author has two coherent paths forward:

**Path A — supply the geometric construction.** Write a precise definition of a "torus-shaped configuration space" $T(\mathbb{Z}/n\mathbb{Z})$ as a topological / smooth / combinatorial object built from the four structures, equipped with metric data $R(T)$ and $r(T)$ derived purely from the algebra, and prove $R/r = 5/7$ for $n = 10$ as a theorem about $T(\mathbb{Z}/10\mathbb{Z})$. This is real mathematics; it is also genuinely interesting if it works. Estimated effort: 6–12 months of focused work; possibly a Ph.D.-style program. The result, if it exists, would likely be a strong JPAA submission.

**Path B — drop the geometric framing entirely and submit a different paper.** Write a paper titled something like "The smallest squarefree $n$ admitting both a degree-2 cyclotomic resonance at one of its prime factors and a small-prime degree-3 cyclotomic obstruction is $n = 10$" or equivalent. The result is small but honest, clearly stated, and provable from the textbook facts already in §A.2. This would be a 4–6 page note appropriate for *INTEGERS*, *Amer. Math. Monthly*, or *Mathematics Magazine*, not JPAA. Estimated effort: 2–4 weeks.

Path A is the JPAA-appropriate option but requires substantial new mathematics. Path B is achievable quickly but redirects the manuscript to a different venue.

The current manuscript's "fix in revision" surface area (Issues 1–3, M1–M9, m1–m9) is large enough that I do not see a "Major Revisions" pathway to JPAA acceptance. The structural problems are not exposition issues; they are mathematical content gaps. Revision must therefore be a rewrite, not an edit.

---

## §8 — Venue bar: does this clear JPAA?

JPAA publishes papers in pure algebra and applied algebra (algebraic topology, algebraic geometry, ring theory, lattice theory, category theory, etc.). The bar is roughly: a clearly stated theorem in algebra, with a complete proof, that is either new or substantially generalizes a known result, with citations to the prior literature and a clear statement of the contribution.

The present manuscript does not clear this bar:

- The central theorem (Theorem 3, $R/r = 5/7$) is not proved (Issue 1).
- The supporting theorems (Theorems 1, 2) have incomplete proofs (M1, M2).
- The "prior literature" framing places the work in conversation with the Russell paradox, Gödel's incompleteness, Riemann's hypothesis, and Bialynicki-Birula's nonlinear Schrödinger equation; none of these is mathematically connected to the actual content (cyclotomic fields, divisor lattices). The bibliography is decorative rather than functional (M9).
- The contribution is interpreted as the "geometric face of the Crossing Lemma," but the Crossing Lemma is in a separate, unsubmitted paper. JPAA cannot referee a paper whose meaning depends on a parallel submission the editor has not seen.

I do not recommend acceptance at JPAA in any form. The honest paths are: (a) rewrite as Path A and resubmit to JPAA after the geometric construction is in place; or (b) rewrite as Path B and submit the small honest result to a venue at the appropriate scale (*INTEGERS*, *Math. Mag.*, *Amer. Math. Monthly*).

---

**End of report.**

*Reviewer disclaimer: I have read this manuscript in good faith as an algebraist with no prior exposure to the broader research framework cited as "TIG" / "CK." The references to internal sprint numbers, working-paper IDs, and a software system called CK were treated as undefined; I evaluated only the mathematical content presented in the submitted file. Where I could not verify a claim from the file alone, I have said so.*
