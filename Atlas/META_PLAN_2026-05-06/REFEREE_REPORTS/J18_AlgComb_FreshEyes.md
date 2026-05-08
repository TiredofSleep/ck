# Referee Report: J18 / Algebraic Combinatorics

**Manuscript:** "The $\sigma^2$-Triadic Decomposition: Conservation/Manifestation Duality on $\mathbb{Z}/10\mathbb{Z}$"
**Authors:** B. R. Sanders, M. Gish
**Submitted to:** Algebraic Combinatorics
**Reviewer:** Anonymous external referee (fresh-eyes; no prior contact with the framework)
**Date:** 2026-05-07

---

## 1. Summary of the manuscript

The manuscript studies a specific involution $\sigma$ on the residue ring $\mathbb{Z}/10\mathbb{Z}$ with cycle structure $(0)(3)(8)(9)(1\,7\,6\,5\,4\,2)$ — four fixed points and one 6-cycle. Its square $\sigma^2$ partitions the 6-cycle into two triangular orbits:
$$O_1 = \{1, 6, 4\}, \qquad O_2 = \{7, 5, 2\},$$
and acts trivially on the four fixed points.

The authors claim three results about a quantity $\Psi_B : \mathbb{Z}/10\mathbb{Z} \to \mathbb{Z}$ defined as $\Psi_B(n) = -(\mathrm{period}(n) - 1)$, where "$\mathrm{period}$" is a per-element function defined by reference to a companion paper [SandersBridgeWP9]:

- **Theorem 3.1 ($\sigma$-orbit triangular decomposition):** $\sum_{n \in \sigma\text{-cycle}} \Psi_B(n) = -T_5 = -15$ and $\sum_{n \in \sigma\text{-fixed}} \Psi_B(n) = -T_3 = -6$, with $T_k$ denoting the triangular numbers.

- **Theorem 3.2 (role-Fibonacci decomposition):** With a "role partition" $F = \{1,3,5,7,9\}$, $S = \{2,4,8\}$, $T = \{6\}$, $V = \{0\}$ (pre-defined in [SandersBridgeWP9]), $\sum_F \Psi_B = -F_7 = -13$ and $\sum_S \Psi_B = -F_6 = -8$, with $F_k$ Fibonacci.

- **Theorem 5.5 ($\sigma^2$-form ledger):** Combines the above into a 3-component ledger $-6 + (-8) + (-7) = -21$ with the σ-fixed contribution, $O_1$ contribution, $O_2$ contribution, all "structurally forced".

Theorem 3.2 has an attached "canonical-specificity" claim: $0/200$ random commutative tables on $\mathbb{Z}/10\mathbb{Z}$ reproduce the $(13, 8)$ split (cited to [SandersBridgeWP9] N8).

The "conservation/manifestation duality" of the title is presented as the relationship between Theorem 3.1 (forced by a "linear period formula") and Theorem 3.2 (canonical-specific). The σ²-orbit decomposition (Section 5) sharpens the σ-orbit side of this picture into the two triangular triples.

I have read the manuscript end-to-end and attempted to verify the σ²-orbit computation. **Several substantive issues are found.**

---

## 2. Decision recommendation

**Reject** (with substantial reservations about the underlying claims). The manuscript has multiple serious problems:

- **Problem A (fatal):** The central object $\Psi_B(n)$ depends on a "period formula" defined in a companion paper [SandersBridgeWP9] that is not present at refereeing. The paper as submitted is not self-contained — without [SandersBridgeWP9], the $\Psi_B$ function is undefined for most $n$, and the central claims of Theorems 3.1, 3.2, and 5.5 cannot be checked.

- **Problem B (fatal):** Proposition 5.4 contains an internal contradiction. Its statement says $\sum_{O_1} \Psi_B = -7$ and $\sum_{O_2} \Psi_B = -8$. Its own proof computes $\sum_{O_1} = -8$ and $\sum_{O_2} = -7$. The downstream Theorem 5.5 ledger uses $O_1 = -8$ and $O_2 = -7$ (consistent with the proof but not with the proposition's statement).

- **Problem C (fatal):** Proposition 5.4's proof claims to use "the linear period formula $\mathrm{period}(n) = 7 - n$" but then asserts $\mathrm{period}(7) = 4$, $\mathrm{period}(5) = 2$, $\mathrm{period}(2) = 4$. None of these match $7 - n$: $7 - 7 = 0$, $7 - 5 = 2$ (this one matches), $7 - 2 = 5$ (does not match $4$). The proof says "we use $\mathrm{period}(7) = 4$ from the boundary formula [SandersBridgeWP9] Corollary 2.2", contradicting the linear formula stated as the basis of computation.

- **Problem D (fatal):** "Conservation/manifestation duality" is not given a mathematical definition in the paper. The phrase is used as a label for the relationship between two decompositions of the $\pm 21$ invariant, but no theorem says what makes a decomposition "conservation" vs. "manifestation". The status labels ("forced" vs. "canonical-specific") are claimed without precise definitions of either term.

- **Problem E:** The σ²-triadic decomposition itself, when properly set up, is just the standard observation that $\sigma$ has order $6$ on the 6-cycle, so $\sigma^2$ has order $3$ and partitions the cycle into two 3-orbits. This is elementary and the choice "decompose the cycle by $\sigma^2$" is purely descriptive — the *theorem* would have to be about *what* the decomposition reveals, not the existence of the decomposition.

The paper has flashes of interesting structural observations (the $T_3 + T_5 = 21$ and $F_6 + F_7 = 21$ coincidence is striking), but the manuscript is not in a state to be evaluated. The cited [SandersBridgeWP9] needs to be public for refereeing to proceed. Beyond that, the internal contradictions in Proposition 5.4 are unforced errors that should not appear in a journal submission.

---

## 3. Major comments

### M1. The paper is not self-contained. (**fatal**)

The $\Psi_B$ function — central to all three theorems — is defined as $\Psi_B(n) = -(\mathrm{period}(n) - 1)$, where $\mathrm{period}$ is described as "the per-element period-to-trace contribution of [SandersBridgeWP9] eq. (B)". This referee cannot access [SandersBridgeWP9] and therefore cannot evaluate whether:
- $\Psi_B$ is well-defined.
- The "linear period formula $\mathrm{period}(n) = 7 - n$" used in Proposition 5.4's proof is correct.
- The "boundary formula" appealed to for $\mathrm{period}(7) = 4, \mathrm{period}(5) = 2, \mathrm{period}(2) = 4$ is correct.
- The role partition $F/S/T/V$ is well-defined.

For *Algebraic Combinatorics*, a paper must be self-contained at the level of definitions, even if proofs reference a companion. Currently neither $\Psi_B$ nor the role partition is defined in the manuscript; both are quoted from a paper not accessible to the referee.

**Recommended fix.** Either (a) include the definitions of $\Psi_B$ and the role partition in the manuscript (with at most 1 page of background from [SandersBridgeWP9] reproduced), or (b) hold the submission until [SandersBridgeWP9] is publicly available with a citable arXiv ID.

The current state — central definitions deferred to an inaccessible companion paper — makes refereeing impossible.

### M2. Proposition 5.4 has a sign-swap error in its statement. (**fatal**)

Proposition 5.4's statement reads:

> $\sum_{n \in O_1} \Psi_B(n) = -7$, $\sum_{n \in O_2} \Psi_B(n) = -8$, with $O_1 + O_2 = -15 = -T_5$.

Its proof computes:

> $O_1 = \{1, 6, 4\}$: $\Psi_B(1) + \Psi_B(6) + \Psi_B(4) = -5 + (-1) + (-2) = -8$
> $O_2 = \{7, 5, 2\}$: $\Psi_B(7) + \Psi_B(5) + \Psi_B(2) = (-3) + (-1) + (-3) = -7$

So the proof says $O_1 = -8$ and $O_2 = -7$. The proposition's statement says $O_1 = -7$ and $O_2 = -8$. These are inconsistent.

Theorem 5.5's ledger says:

> $O_1$ contribution $-8$, $O_2$ contribution $-7$.

This matches the *proof* of Proposition 5.4 but contradicts the *statement* of Proposition 5.4.

So either (a) the proposition's statement has a typo and should read $O_1 = -8, O_2 = -7$, or (b) the proof is wrong and the ledger uses a wrong value. The Remark following Proposition 5.4 says "The per-orbit values $\{-7, -8\}$ are the canonical TIG primes HARMONY $= 7$ and BREATH $= 8$ in negated form" — this is symmetric in the two values and doesn't disambiguate.

Independent computation by this referee, using the stated $\Psi_B$ values, yields $O_1 = -8$ and $O_2 = -7$. The proposition's statement is wrong.

**Recommended fix.** Correct the typo in Proposition 5.4: $\sum_{O_1} = -8$ and $\sum_{O_2} = -7$.

This is a careless but unambiguous error. It must be fixed before camera-ready.

### M3. Proposition 5.4's proof cites two contradictory period formulas. (**fatal**)

The proof says:

> Direct computation from the linear period formula $\mathrm{period}(n) = 7 - n$ and $\Psi_B(n) = -(\mathrm{period}(n) - 1)$:
> ...
> (Where we use $\mathrm{period}(7) = 4$, $\mathrm{period}(5) = 2$, $\mathrm{period}(2) = 4$ from the boundary formula [SandersBridgeWP9] Corollary 2.2.)

The linear formula $\mathrm{period}(n) = 7 - n$ gives:
- $\mathrm{period}(1) = 6$, $\Psi_B(1) = -5$ ✓ (matches the proof's value)
- $\mathrm{period}(2) = 5$, $\Psi_B(2) = -4$. The proof uses $\Psi_B(2) = -3$, which would require $\mathrm{period}(2) = 4$, not $5$. **Contradicts $7 - n$.**
- $\mathrm{period}(4) = 3$, $\Psi_B(4) = -2$ ✓
- $\mathrm{period}(5) = 2$, $\Psi_B(5) = -1$ ✓
- $\mathrm{period}(6) = 1$, $\Psi_B(6) = 0$. The proof uses $\Psi_B(6) = -1$, which would require $\mathrm{period}(6) = 2$, not $1$. **Contradicts $7 - n$.**
- $\mathrm{period}(7) = 0$, $\Psi_B(7) = 1$. The proof uses $\Psi_B(7) = -3$, which would require $\mathrm{period}(7) = 4$, not $0$. **Contradicts $7 - n$.**

So the proof claims to use $\mathrm{period}(n) = 7 - n$ but actually uses different values for $n = 2, 6, 7$. The parenthetical attempts to rescue this by appealing to a "boundary formula" from the companion — but the proof's stated method ("direct computation from the linear period formula") is then inconsistent with what is actually computed.

This is more than a typo. The proof is using a different formula than the one stated. Either:
(a) The "linear period formula $\mathrm{period}(n) = 7 - n$" is the wrong definition and there is some other rule for $\Psi_B$ that gives $\Psi_B(2) = -3$, $\Psi_B(6) = -1$, $\Psi_B(7) = -3$. The proof should cite this correct rule.
(b) The values $\Psi_B(2) = -3$, etc., are wrong and should be $-4$, $0$, $1$ per the linear formula. Then the sums $O_1 = -5 + 0 + (-2) = -7$ and $O_2 = 1 + (-1) + (-4) = -4$, giving total $-11 \ne -15$, breaking Theorem 3.1.

Without [SandersBridgeWP9] available, this referee cannot tell which is correct. The proof as written is internally inconsistent; *some* version of it must be wrong.

**Recommended fix.** State the correct definition of $\Psi_B$ (i.e., the actual rule, not a "linear formula" that doesn't apply to all $n$). Reproduce or cite the boundary-formula values explicitly. Recompute the sums.

### M4. "Conservation/manifestation duality" is undefined. (**fatal**)

The paper's title and abstract present "conservation/manifestation duality" as the central object of study. The introduction (§1.3) describes:

> Each triple carries a different kind of substrate-invariant content. The conservation triple ($\{1, 6, 4\}$) carries quantities that are forced by the linear period structure of [SandersBridgeWP9] (the BH successor diagonal and the linear period formula are the load-bearing inputs). The manifestation triple ($\{7, 5, 2\}$) carries quantities that emerge as canonical-specific signatures: they are present for the canonical $\mathrm{TS}_8, \mathrm{BH}_{10}$ tables but $0/200$ random commutative tables on $\mathbb{Z}/10\mathbb{Z}$ reproduce them.

This is the only place the duality is described. There is no definition of:
- What "conservation" means as a mathematical property.
- What "manifestation" means as a mathematical property.
- What it means for a triple to "carry" a quantity.
- The duality between them — what is dual?

In the body of the paper (Theorems 3.1, 3.2, 5.5, Corollary 3.3), the words "conservation" and "manifestation" appear as labels but never as definitions. Corollary 3.3 says:

> The two decompositions of the $\pm 21$ invariant cross. The σ-orbit decomposition is structurally forced by the linear period formula (conservation: forced regardless of any canonical-specific table choice). The role-Fibonacci decomposition is a canonical-specific signature (manifestation: present in the canonical $\mathrm{TS}_8, \mathrm{BH}_{10}$ substrate but not preserved under random-table perturbation).

So "conservation" = "forced" and "manifestation" = "canonical-specific". These are the same labels with different names.

For *Algebraic Combinatorics*, a paper centered on a "duality" must define the duality precisely. Without a definition:
- It is unclear whether the duality is a structural fact about $\sigma$ on $\mathbb{Z}/10$ (which would be checkable by enumeration), about a class of tables (which random tables can sample), or about something else.
- The relationship between the two decompositions ($\sigma$-orbit and role-Fibonacci) is empirical (one always gives $T_5 + T_3$, the other gives $F_7 + F_6$) but the title's "duality" suggests something stronger.

**Recommended fix.** Provide a precise definition of the duality. State what it is, mathematically: an isomorphism, a Galois-style correspondence, an exact sequence, etc. Or rename the paper to drop "duality" from the title.

### M5. The σ²-triadic decomposition is the standard observation that $\sigma^2$ has order 3 on a 6-cycle. (**important**)

§4 derives that $\sigma^2$ partitions $\{1,7,6,5,4,2\}$ into the two 3-orbits $O_1 = \{1, 6, 4\}$ and $O_2 = \{7, 5, 2\}$. This is correct, and follows immediately from $\sigma$ being a 6-cycle: $\sigma^2$ has order 3 on the cycle, hence 2 orbits of size 3.

For *Algebraic Combinatorics*, observing the cycle structure of $\sigma^2$ is not a theorem — it is a 1-line consequence of the cycle structure of $\sigma$. The paper should not present it as a "decomposition theorem" without further structural content.

The paper's structural content is in Theorem 5.5's ledger ($-6 -8 -7 = -21$) — but as M2 and M3 show, the ledger's per-orbit values come from a $\Psi_B$ rule that is inconsistently stated.

**Recommended fix.** Remove the σ²-triadic decomposition as a "theorem" and present it as a basic fact in §2 setup. Then the paper's content is concentrated in (i) the $T_5 + T_3 = 21$ identity (Theorem 3.1), (ii) the $F_7 + F_6 = 21$ identity (Theorem 3.2), and (iii) their joint structure (Corollary 3.3 + Theorem 5.5 ledger). These are the substantive claims.

### M6. The "canonical-specificity" claim relies on an empirical statement (0/200) without methodology. (**important**)

Theorem 3.2 ends with:

> The Fibonacci role decomposition is canonical-specific: $0/200$ random commutative tables on $\mathbb{Z}/10\mathbb{Z}$ reproduce $(|F|, |S|) = (13, 8)$. Single-swap perturbations preserve the decomposition in $32/50$ trials; three-swap in $11/50$.

This is the load-bearing claim distinguishing "manifestation" from arbitrary identities. But the methodology is not described:
- What is the random-table sampling distribution? Uniform over $10^{50} \cdot 2^{10} \cdot \ldots$ commutative tables? Tables with specific row/column constraints?
- What is the role partition for a *random* table? Is it computed table-by-table or fixed at the canonical $F = \{1,3,5,7,9\}, S = \{2,4,8\}, T = \{6\}, V = \{0\}$?
- What does "single-swap perturbation" mean precisely?
- What is the test statistic ($(|F|, |S|) = (13, 8)$ on what)?

For an empirical claim to be load-bearing on a journal theorem, the methodology must be specified. Currently this is deferred to [SandersBridgeWP9] N8 (inaccessible to the referee).

**Recommended fix.** Reproduce the methodology from [SandersBridgeWP9] N8 in this paper, or remove the canonical-specificity claim and reduce Theorem 3.2 to an algebraic identity that doesn't depend on random-table evidence.

### M7. The connection to modular surface and knots (citations Burrin, Katok, Morishita) is not developed. (**minor**)

The bibliography includes Burrin–von Essen 2024 (Rademacher symbol), Katok–Ugarcovici 2007 (modular surface), Morishita 2024 (Knots and Primes). None is engaged with in the body. If these are intended as suggested connections to existing literature, a 1-paragraph remark would help. Otherwise, remove.

---

## 4. Minor comments

### m1. Lens-scope statement.

§1.4 includes a "lens-scope statement":

> This paper uses only lens-invariant structural facts about the σ²-orbit decomposition and the role partition. It does not commit to any single canonical σ²-triadic BHML projection.

The terminology "lens-invariant", "σ²-triadic BHML projection", "Tier-D", and "candidate" are used without definition. They appear to be internal to the framework's tiering system [Atlas2026Tiering]. For *Algebraic Combinatorics*, this is incomprehensible without the framework background.

**Recommended fix.** Either (a) remove the lens-scope statement from the published version (it is a meta-comment about the framework, not a result), or (b) provide a brief explanation of what "lens-invariance" means in concrete combinatorial terms. The current state imposes a reading-comprehension burden on the journal reader that doesn't repay itself.

### m2. The role partition.

§2.2 states:

> The functional role partition is $F = \{1,3,5,7,9\}$, $S = \{2,4,8\}$, $T = \{6\}$, $V = \{0\}$ ... The partition is functional, not algebraic: it crosses σ-orbit decomposition.

"Functional, not algebraic" is asserted but not motivated. Why is this the right partition? What is its origin? The text says "the partition is functional", but does not explain what function $F, S, T, V$ play. This is a gap that should be filled — at least one paragraph explaining the origin of the partition (presumably from the substrate operators $\mathrm{TS}_8, \mathrm{BH}_{10}$).

### m3. Notation.

- $\Psi_B$ is referenced as "eq. (B)" of [SandersBridgeWP9], but the paper uses it without internal definition. Reproduce the definition.
- $T_k$ for triangular and $F_k$ for Fibonacci is reasonable, but write the formulas at first use.
- $\mathrm{TS}_8$, $\mathrm{BH}_{10}$ are used without explanation. They are the substrate operators of [SandersGishFourCore], but the present paper should either define them or remove them.

### m4. The boundary formula.

The "boundary formula" cited as [SandersBridgeWP9] Corollary 2.2 is the rule that gives $\mathrm{period}(7) = 4$, $\mathrm{period}(5) = 2$, $\mathrm{period}(2) = 4$. The "linear period formula" gives $\mathrm{period}(n) = 7 - n$ for some range. The two cannot both apply to $n = 2$ (linear gives $5$, boundary gives $4$). The paper does not state which range each formula applies to.

**Recommended fix.** Specify the domain of each formula. (e.g., "linear period formula on $\{1, 3, 4, 5, 6\}$" or "$\{1, 4, 6\}$" — narrow it down.)

### m5. Bibliography reference [Atlas2026Tiering].

The reference [Atlas2026Tiering] points to a repository directory ("Atlas/LENS\_TAXONOMY\_2026-05-06") with a DOI. This is unusual for a journal submission. *Algebraic Combinatorics* may or may not accept repository-directory citations. Confirm the editorial policy.

---

## 5. Independent verification summary

I performed the following independent computations:

1. **σ cycle structure on $\mathbb{Z}/10$:** $\sigma = [0, 7, 1, 3, 2, 4, 5, 6, 8, 9]$ has cycles $(0)(3)(8)(9)(1\,7\,6\,5\,4\,2)$. ✓ Matches the paper.

2. **σ² cycle structure:** $\sigma^2 = [0, 6, 7, 3, 1, 2, 4, 5, 8, 9]$ has cycles $(0)(3)(8)(9)(1\,6\,4)(2\,7\,5)$. The two 3-orbits on the σ-cycle are $O_1 = \{1, 6, 4\}$ and $O_2 = \{2, 5, 7\} = \{7, 5, 2\}$. ✓ Matches the paper's $O_1, O_2$.

3. **σ² per-orbit sums (using stated $\Psi_B$ values $\{1: -5, 2: -3, 4: -2, 5: -1, 6: -1, 7: -3\}$):**
   - $\sum_{O_1} \Psi_B = -5 + (-1) + (-2) = -8$
   - $\sum_{O_2} \Psi_B = -3 + (-1) + (-3) = -7$
   - These match the *proof* of Proposition 5.4 and the *ledger* of Theorem 5.5, but contradict the *statement* of Proposition 5.4 (which says $O_1 = -7$ and $O_2 = -8$).

4. **Triangular and Fibonacci identities:**
   - $T_5 + T_3 = 15 + 6 = 21$ ✓
   - $F_7 + F_6 = 13 + 8 = 21$ ✓
   - These are correct arithmetic; the identities $T_5 = 15$ and $F_7 = 13$ are standard.

5. **Period-formula consistency:** The paper claims to use $\mathrm{period}(n) = 7 - n$ but the values $\Psi_B(2) = -3$, $\Psi_B(6) = -1$, $\Psi_B(7) = -3$ require $\mathrm{period}(2) = 4$, $\mathrm{period}(6) = 2$, $\mathrm{period}(7) = 4$. The linear formula $7 - n$ gives $5, 1, 0$ respectively — none match. The proof's parenthetical appeal to "the boundary formula [SandersBridgeWP9] Corollary 2.2" implicitly admits that the linear formula is wrong here.

So:
- σ²-orbit decomposition: correct (M5).
- $T + T = 21$ and $F + F = 21$ identities: correct (independent of $\Psi_B$).
- Per-orbit $\Psi_B$ values: I cannot verify without [SandersBridgeWP9].
- Proposition 5.4: internally contradictory (statement vs. proof — see M2).
- Period formula: inconsistently used (M3).

The σ²-orbit structure on the σ-cycle is correct (M5). The $T_5 + T_3 = F_7 + F_6 = 21$ coincidence is striking and worth noting. But the proof structure of the manuscript has unforced internal errors.

---

## 6. Strengths of the manuscript

1. **The triangular-Fibonacci coincidence is striking.** $T_5 + T_3 = F_7 + F_6 = 21$ is a real arithmetic fact, and partitioning the same total along two different decompositions (σ-orbit vs. role) is a nice combinatorial observation. With proper structural setup, this could be developed into a theorem.

2. **The σ-cycle palindrome on $\mathbb{Z}/10$** ($\sigma$: 6-cycle, $\sigma^2$: 2 trefoils, $\sigma^3$: 3 dualities, ...) referenced via the companion is genuine combinatorial content. This is not the present paper's main result but is interesting.

3. **The lens-scope statement (despite my critique in m1) is a sign of mathematical care:** the authors acknowledge that they are not committing to a canonical $\sigma^2$-triadic BHML projection and are presenting only what is invariant under their open choice. This is honest, even if the framework-internal vocabulary is opaque.

---

## 7. What a publishable version would have to contain

For *Algebraic Combinatorics*:

(a) A self-contained definition of $\Psi_B$, the role partition, and the substrate operators $\mathrm{TS}_8, \mathrm{BH}_{10}$ — at least to the level of being checkable from the manuscript alone. The current dependence on [SandersBridgeWP9] is fatal.

(b) A precise definition of "conservation" and "manifestation" as mathematical properties. Currently they are labels.

(c) Correction of the Proposition 5.4 statement-vs-proof inconsistency.

(d) Resolution of the period-formula contradiction (linear formula $7-n$ vs. boundary formula values).

(e) A description of the random-table sampling methodology supporting the "0/200" claim.

(f) A theorem that goes beyond the elementary observation that $\sigma^2$ has order 3 on a 6-cycle. The interesting content (T+T = 21, F+F = 21, both decompositions cross at 21) is real but currently buried under terminology and stated as side-remarks.

A cleaner, self-contained paper focused on the $T_5 + T_3 = F_7 + F_6 = 21$ coincidence and its $\sigma^2$-orbit refinement could be publishable. The current draft is not.

---

## 8. Decision

**Reject** in current form. The mathematical content has substantive problems:
- (M1) The paper depends on an inaccessible companion paper for its central definitions.
- (M2) Proposition 5.4 has a sign-swap error between statement and proof.
- (M3) The period formula is inconsistently invoked.
- (M4) The "conservation/manifestation duality" of the title is undefined.
- (M5) The σ²-triadic decomposition is the standard cycle-structure observation, not a theorem.
- (M6) The canonical-specificity claim relies on an empirical statement without methodology.

Some of these (M2, the typo) are easily fixable; M1 and M4 require either substantial new writing or a pre-existing public companion paper. M3 may require a reformulation of the underlying definitions.

The $T_5 + T_3 = F_7 + F_6 = 21$ coincidence is striking, and a much shorter, self-contained paper focused on that arithmetic-combinatorial identity (with the $\sigma^2$-orbit refinement) could be of interest. But the current manuscript is not in a state to be evaluated.

I recommend the authors withdraw and resubmit after the companion [SandersBridgeWP9] is publicly available with citable arXiv ID, the internal contradictions are resolved, and "conservation/manifestation duality" is given a precise mathematical meaning — or the framing is changed to remove the term.

I am willing to re-review a substantially revised submission.

---

**Referee signature:** Anonymous external referee, fresh-eyes (no prior contact with the framework or its authors).
**Time spent:** ~4 hours (including independent computation of σ² cycle structure and verification of the Proposition 5.4 inconsistency).
**Conflicts of interest:** None.
