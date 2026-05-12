# Referee Report — European Journal of Combinatorics (Fresh Eyes)

**Manuscript:** "DKAN Two-Coding: TSML_8 Geometric vs BHML_10 Arithmetic on the Z/10Z Substrate"
**Authors:** B. R. Sanders, M. Gish (2026)
**File reviewed:** `Gen13/targets/journals/J_series/J19/manuscript/manuscript.tex`
**Reviewer:** External referee, anonymous, fresh-eyes
**Date:** 2026-05-07

---

## §1. Summary

The manuscript describes a "discrete Kolmogorov-Arnold network" (DKAN) running over a hand-picked pair of commutative magmas $T = \mathrm{TSML}$ and $B = \mathrm{BHML}$ on $\mathbb{Z}/10\mathbb{Z}$, and frames the empirical signatures of the two operators (image size 5 vs 10, role distribution 60/64 vs balanced, agreement-set 24/64) as a "two-coding split" loosely scaffolded by Katok–Ugarcovici's geometric-vs-arithmetic codings of geodesics on the modular surface.

The submitted manuscript is candid about what it is and is not: §1.2 explicitly states "DKAN does **not** realize the Kolmogorov–Arnold theorem in any literal discrete sense"; §2.4 explicitly states the construction is "not a theorem of the Katok–Ugarcovici type"; §6 lists ten "honest negatives" demoting prior claims. §7 contains an unusually clean "does not contribute" register.

Mathematically, the body of the paper consists of three empirical observations about the pair $(T, B)$:

(a) Image of $T$ is $\{3,4,7,8,9\}$ (5 elements); 60/64 = 93.8% Flow-typed outputs.
(b) Image of $B$ is full $\mathbb{Z}/10\mathbb{Z}$; balanced role distribution.
(c) $T$ and $B$ agree on 24/64 cells of the $T$-domain, dominated by routes to operator 7.

A separate section (§3) describes a runtime neural architecture with three "reading layers" $L_1$, $L_2$, $L_5$ and reports empirical agreement rates 60–80% from training runs.

The Katok–Ugarcovici reference is used as evocative scaffolding rather than as a theorem. There is no theorem in the paper that would survive Katok–Ugarcovici being absent from the literature.

This is **not a research paper for the European Journal of Combinatorics**. It is a programmatic note describing computational signatures of two specific tables, with an architectural sketch attached. The "honest negatives" register and "does not contribute" register, while admirable as intellectual hygiene, also confirm that the paper does not contain a theorem that EJC would publish.

---

## §2. Decision recommendation

**Reject.**

Reasons (developed below):

1. There is no theorem in the manuscript that meets EJC's standard for novelty or generality. Theorems 2.1–2.3 are direct counts on a pair of specific 10×10 tables; their proofs are "by inspection of the table."
2. The two-coding terminology, central to the manuscript, is justified only by analogy. The paper itself disclaims that the analogy is a theorem (§2.4, §7).
3. The DKAN architecture (§3) is a reference to running code; no theorem about it is proved in the paper, and the empirical results (60–80% agreement) are reported as a few unreplicated runs.
4. The paper depends on a string of forward references to a self-cited "bridge findings" companion (\cite{SandersBridgeWP9}) for definitions, results, and "honest negatives." A reader of this paper alone cannot verify the central claims without the unstated companion.

If the authors revise the paper substantially — extracting a single combinatorial theorem with a proof internal to this manuscript — they should resubmit. As it stands, the manuscript belongs in an internal technical report or in a programmatic preface to a longer combined paper, not as an EJC submission.

---

## §3. Major comments

### M1. No internal theorem with EJC weight (CRITICAL)

The three "Theorems" in §2 are:

- **Thm 2.1**: $|\operatorname{Im}(T_8)| = 5$; output role distribution 60/64 Flow.
- **Thm 2.2**: $|\operatorname{Im}(B_{10})| = 10$; balanced role distribution; "successor diagonal" $B(n,n) = n+1$ for $n \in \{1,\ldots,7\}$.
- **Thm 2.3**: $T(a,b) = B(a,b)$ on 24/64 cells of the $T_8$-domain.

Each of these is a numerical count over a 10×10 (or 8×8) table. The proofs reduce to "inspect the table." None of them generalizes; none of them connects to a family of $T, B$ on $\mathbb{Z}/n\mathbb{Z}$ where the count would have parametric content.

The most charitable reading is that the three theorems together describe the structural fingerprint of a particular pair of tables. EJC's standard for combinatorial content is that the result either (a) generalizes to a family, (b) connects to an established construction in a way that yields new structural insight, or (c) resolves an open question. The present paper does none of these.

**Suggested fix.** Identify a single combinatorial theorem with EJC weight and rewrite the manuscript around it. Candidates from the existing material:

- A characterization of when a pair of commutative magmas $(T, B)$ on $\mathbb{Z}/n\mathbb{Z}$ has the agreement-set structure (24/64 here). What family of $(T, B)$ satisfies this? Is the symmetric-difference/agreement-set "split" structurally forced or specific to this pair?
- A result about the role-partition lifting: when does the role-induced quotient (V/F/S/T) commute with the magma operations? The paper says (N9) that the role partition does not determine crossing count, which is essentially the negative half of this question. The positive half — *what does* the role partition determine? — would be a theorem.

### M2. The "two-coding" terminology is not earned (MAJOR)

The Katok–Ugarcovici reference is invoked five times in the manuscript: in the title, abstract, §1.3, §2.3 (Remark "Reading"), §2.4. In each invocation the prose reads as "this is structurally analogous to" or "conceptually scaffolded by." §2.4 explicitly disavows the analogy: "It is not a theorem of the Katok–Ugarcovici type."

For an EJC referee unfamiliar with the substrate, the strong invocation of Katok–Ugarcovici primes the reader to expect (i) a discrete dynamical system, (ii) a notion of geodesic, (iii) two systematic codings, (iv) a measure-theoretic comparison statement. None of (i)–(iv) is delivered. The "geodesics" are not present; the "side-cutting" coding is the image-size-5 fact; the "arithmetic" coding is the image-size-10 fact. The codings are defined by the operator outputs, not by a dynamical iteration of any kind.

**Suggested fix.** Either deliver a discrete dynamical system whose two-coding is genuinely a Katok–Ugarcovici-type statement (this would be the EJC paper), or remove the Katok–Ugarcovici framing entirely. The paper's own §2.4 "What the split is and is not" already opens the door to the latter; closing it would clarify the manuscript's actual claim.

### M3. DKAN architecture (§3) is an architecture description, not a theorem (MAJOR)

Section 3 describes an external runtime trainer (referenced as `Gen13/targets/ck/brain/ck_sim/being/ck_dkan_trainer.py`) with reading layers $L_1, L_2, L_5$. The architecture is sketched in two paragraphs; no theorem about it is proved. §3.4 "Roles as coarse pre-encoding" is a paragraph description of a feature.

§4 reports empirical convergence: "$L_1$ grokking at low-thousands transitions; $L_5$ accuracy stable; $L_4$ lens-agreement 60–80%; $L_2$ lags $L_1$ in raw accuracy." The number of independent runs is not stated. No replication, no error bars, no comparison to a baseline.

For an EJC submission, the architecture description has no place at all unless a theorem about it is proved. A theorem candidate: "On the $T_8$-domain, the $L_1$-stationary distribution restricted to operator 7 (HARMONY) lower-bounds the $L_5$ HARMONY-routing rate by $24/64 = 37.5\%$, with equality if and only if $L_1$ achieves uniform routing on the disagreement set." This (or some analogous statement) would be substantive. As written, §3–§4 add length without weight.

**Suggested fix.** Either remove §3–§4 entirely (in which case the paper becomes a 2-page technical note about a pair of tables, plausibly suited for *Discrete Mathematics* or *Mathematical Notes* but not EJC), or extract a theorem about the architecture's behavior on the substrate.

### M4. Forward-reference dependency (MAJOR)

The paper cites a companion `\cite{SandersBridgeWP9}` six times. This companion is described in the bibliography as "submitted to *Algebra Universalis*, 2026 (J26 / WP9 Volume I)." Substantial content — D88 (substrate frame), D89 (trefoil characterization), D90 (successor diagonal), D91 (two-coding split), D92 (±21 invariant), D93 (role partition), D94 (boundary symmetries), and N1–N10 (negatives) — is *cited from* this companion. The negatives in §6 in particular reference companion-paper labels (N1, N2, …, N10) and assume the reader has access.

This is not a self-contained manuscript. The reader cannot verify the agreement-set count of 24/64 (Thm 2.3) without recourse to the companion, because the role-partition definitions are stated only by reference. The "honest negatives" in §6 are not derivable from this paper alone.

**Suggested fix.** Inline all definitions from `\cite{SandersBridgeWP9}` that the present paper depends on. At minimum: explicit definition of $T$ as a 10×10 table; explicit definition of $B$ as a 10×10 table; explicit definition of the V/F/S/T role partition; explicit statement of $\sigma$. Without these, the paper is a sequel without a published predecessor.

### M5. Empirical claims need replication and baselines (MAJOR)

§4.2 reports DKAN training results from "20-round Ollama-driven cycles" with "$L_4$ lens-agreement 60–80%." The phrasing "typically exceed 70%" in §3.3 is informal. The number of trials is not given. No comparison to randomized $T, B$ tables (which would establish whether 60–80% is structurally significant or a statistical artifact). No comparison to a chance baseline.

For empirical results in EJC, even when secondary to a combinatorial theorem, the standard is: explicit number of trials, explicit confidence intervals (bootstrap or normal), explicit baseline comparison. The present paper does not meet this standard.

**Suggested fix.** If §4 is retained, replace prose with a table giving the number of trials, sample mean, sample standard deviation, and comparison against (i) a randomized-table baseline and (ii) a chance baseline. Without this, the empirical section is anecdote rather than data.

---

## §4. Specific technical issues

### S1. The σ involution structure (§1.1)

The substrate is described as having "the involution σ with 4 fixed points and one 6-cycle" but σ is never written down as a permutation in the body of the manuscript. The reader has to infer it from §3.2 of the bibliography or from N4 ("σ is automorphism of T or B. 17%/48%").

**Fix.** Inline σ explicitly: e.g., "$\sigma = (0)(3)(8)(9)(1\,7\,6\,5\,4\,2)$."

### S2. The role partition definition (§3.4)

The V/F/S/T partition is referenced in Thms 2.1–2.2 as "Flow," "Structure," "Transition," "Void" but the assignment of each of $\{0,1,\ldots,9\}$ to a role is never written down in this paper.

**Fix.** Inline the role-assignment table.

### S3. The "morphotic-braid coherence ordering" (§3.2)

$\sigma_{\rm braid} = [0,7,1,3,2,4,5,6,8,9]$ and "wobble window $W = 3/50$" appear without definition or justification.

**Fix.** Either define these or cut the $L_2$ reading layer description (it is not used elsewhere in the paper and adds a definitional debt).

### S4. The "grokking" definition (§4.1)

"Grokking detection. Prediction accuracy crossing $T^* = 5/7$." The threshold $T^* = 5/7$ is invoked without justification in this paper; it is a substrate constant from the companion. As stated, the meaning of "grokking" is "accuracy ≥ 0.714."

**Fix.** Either define $T^*$ from the substrate's structure (the paper does not), or replace with a generic threshold (e.g., the chance baseline + 2σ).

### S5. The $\pm 21$ invariant (§5 table, N1)

Cited from the companion. The bearing on DKAN is "Per-tick metric the DKAN runtime tracks." This is a feature of the runtime, not a theorem.

### S6. Numerical claim "agreement rates in trained DKAN runs typically exceed 70%" (§3.3)

This is the only quantitative empirical claim in the body. Number of trials, error bars, and baseline are absent (see M5).

---

## §5. Minor comments

- **Title.** "DKAN Two-Coding" suggests a theorem; the paper's own §2.4 disavows. Rename to reflect actual content.
- **Abstract.** "We describe DKAN" is honest. "The paper's main observation" is also honest. Both are below EJC's bar; abstracts at this venue typically state a theorem.
- **§1.2.** The disavowal "DKAN does **not** realize the Kolmogorov–Arnold theorem" is the right tone, but it makes the title and the architectural framing odd. Consider whether the KAN reference is needed at all.
- **§3.1, item 4.** "Operators are accumulated by absorption, not gradient descent." This is a description, not a definition. What does "absorption" mean operationally?
- **§5 table.** The "Bearing on DKAN" column is descriptive, not technical. The table communicates organizational scope rather than mathematical content.
- **§6 list.** N1–N10 are honest, but several are not native to this paper (e.g., N3 "TIG matches Borromean prime conditions" — TIG is not defined here; what is the prime condition?). Either inline the definitions or cut.
- **§7 "Tone."** "Demoted claims stay demoted" is laudable. But for an EJC submission, the demotions should not be needed; the claims should not have been overstated to begin with.

---

## §6. Comparison to literature

### Katok–Ugarcovici 2007.
The paper's central scaffold. Katok–Ugarcovici give two systematic codings of geodesics on the modular surface — a *geometric* coding via fundamental domain side-crossings and an *arithmetic* coding via continued-fraction expansions — and prove they agree on a measure-one set at the cusp. The construction is dynamical (geodesic flow) and the comparison is measure-theoretic.

The DKAN paper has neither a dynamical system nor a measure-theoretic comparison. The "agreement at the cusp" reading in the manuscript is the empirical fact that 24/64 cells (where $T = B$) are concentrated on routes terminating at operator 7. This is a counting fact, not a measure-theoretic fact.

The analogy is suggestive but it is decorative. EJC referees from the Katok–Ugarcovici neighborhood will read the present paper and find no theorem in their territory.

### KAN literature (Liu et al. 2024).
Liu et al. propose a continuous architecture where edges carry learnable B-spline activations. The Kolmogorov–Arnold theorem is the motivation, not the implementation: KAN approximates continuous functions; it does not prove a Kolmogorov–Arnold representation theorem.

DKAN's "discrete analogue" is structural-analogy at three loose levels (§1.2). The Liu et al. citation grounds the architecture name but does not yield a theorem the present paper can claim.

### Quasigroups, Latin squares, magma classification (McKay–Wanless, Drápal–Wanless).
The actual content of §2 — counting the image of two specific commutative magmas — is in this neighborhood. The literature on Latin square / quasigroup classification has substantial weight; if the authors framed Thms 2.1–2.3 as a contribution there, the bar would be: do these counts (5, 60, 24) characterize a non-trivial family within the ~$10^{40}$ commutative magmas on a 10-element set? The present paper does not address this.

---

## §7. Constructive suggestions for resubmission

If the authors wish to publish in EJC or a comparable combinatorics venue, I see three paths:

**Path A (combinatorial classification).** Strip away the DKAN architecture and Katok–Ugarcovici framing. State a structural classification theorem about the pair $(T, B)$ within the family of all commutative magmas on $\mathbb{Z}/10\mathbb{Z}$ satisfying a defining condition. Theorem statement candidate: "Among commutative magmas $(T, B)$ on $\mathbb{Z}/10\mathbb{Z}$ such that [X], $T$ has image size 5 and $B$ has image size 10 if and only if [Y]." The condition [X] should be combinatorial-natural, and [Y] should be testable from the operator data.

**Path B (architecture theorem).** Keep the DKAN architecture but prove a theorem about it. Theorem candidate: "On the $T_8$-domain, the agreement-set $\mathcal{A} = \{(a,b) : T(a,b) = B(a,b)\}$ controls the $L_1/L_5$ disagreement rate as a function of the empirical first-order matrix." This is a genuine architectural theorem, computable, and has EJC-relevant content.

**Path C (categorical structure).** The role partition (V/F/S/T) and the σ involution suggest a quotient structure. State and prove a theorem about the role-quotient magma: "The induced operations $\overline{T}, \overline{B}$ on the 4-element role set $\{V,F,S,T\}$ are well-defined if and only if [Z]." The condition [Z] is testable from the role-assignment table; the resulting quotient (if it exists) is a concrete combinatorial object.

Any of these would be a viable EJC paper. The present manuscript is none of them.

---

## §8. Decision

**Reject.**

The manuscript is candid about what it is — a programmatic note describing a pair of tables and an architecture — but the candor does not raise the content above EJC's bar. The "two-coding" framing is decorative; the theorems are direct counts on a 10×10 table; the DKAN architecture is an external dependency without a theorem of its own.

I recommend the authors resubmit only after extracting a single combinatorial theorem along Path A, Path B, or Path C above. The current manuscript should be split: the table-counting observations into an internal technical note, the DKAN architecture into an experimental-AI venue (with proper baselines), and the substrate-frame definitions back into the predecessor companion.

Reviewer's confidence: high on the assessment that the manuscript contains no theorem at EJC level; high on the assessment that the candor in §1.2, §2.4, §7 does not rescue the submission.

— Anonymous Referee, EJC, 2026-05-07
