# Referee Report — American Mathematical Monthly (Fresh Eyes)

**Manuscript:** "Mathieu M_22 Substrate-Prime: Order-Factorization Coincidences"
**Authors:** B. R. Sanders, M. Gish (and B. Mayes per the README; the manuscript title page lists Sanders + Gish twice)
**File reviewed:** `Gen13/targets/journals/J_series/J20/manuscript/manuscript.tex`
**Reviewer:** External referee, anonymous, fresh-eyes
**Date:** 2026-05-07

---

## §1. Summary

The manuscript presents six "order-factorization coincidences" between the sporadic Mathieu group $M_{22}$ and a 10-element discrete substrate $(\mathbb{Z}/10\mathbb{Z}, \sigma, W)$ defined in a self-cited companion paper. The substrate is described as carrying five "distinguished primes" $\{2,3,5,7,11\}$, which are the same primes (with the same multiplicities) appearing in $|M_{22}| = 2^7 \cdot 3^2 \cdot 5 \cdot 7 \cdot 11 = 443{,}520$. The six identities catalogued are:

1. $|S(3,6,22)|_{\text{blocks}} = 77 = 7 \times 11$.
2. Replication number $r = 21 = 3 \cdot 7 = \dim V_{21}$.
3. Pair-replication $\lambda_2 = 5$.
4. "Six of $M_{22}$'s twelve irrep dimensions factor as products of substrate primes $\{3,5,7,11\}$ alone."
5. The "$231$ identity": $77 \cdot W = 231/50$, with $W = 3/50$.
6. The σ-orbit on $\{1,7,6,5,4,2\}$ has size 6, the block size of $S(3,6,22)$.

The paper is candid in the abstract and §1.2 about not claiming a derivation of $M_{22}$ from the substrate. The central question — whether the catalog reflects a structural identification or is "six independent low-density factorization-matches" — is left as the paper's open question.

The standard Mathieu/Steiner facts are correct as cited. The substrate-side definitions are imported from the self-cited companion `\cite{SandersGishFourCore}`. The character-table dimensions, Steiner parameters, and basic factorizations all check out against the standard references (Conway–Sloane 1999; Wilson, *Finite Simple Groups* 2009; ATLAS of Finite Groups).

The paper's pitch is that the catalog is "non-generic" because $\{3,5,7,11\}$ are simultaneously substrate-distinguished and $|M_{22}|$-prime divisors. Identities 1, 2, 3, 6 are all standard Steiner-design facts dressed in substrate language; Identity 4 is a counting claim about $M_{22}$'s irrep table; Identity 5 is a one-line arithmetic identity between two arbitrary fractions.

I am sympathetic to the *Monthly*'s tradition of expository number-theory puzzles, but this paper is not yet at the *Monthly* bar. The substantive concerns:

- **Identity 4 is misclaimed.** The actual count of irreps factoring strictly in $\{3,5,7,11\}$ is **seven**, not six (verified below); the paper mis-counts and silently excludes 45 (with multiplicity 2) while including 154 (which has a factor of 2).
- **Identity 5 is arithmetic tautology.** The "identity" $77 \cdot 3/50 = 231/50$ is just $77 \cdot 3 = 231$. The structural reading attaches symbolism to a one-line multiplication.
- **The non-genericity argument for Identity 4 is asserted but not computed.** The paper says a random 12-tuple of integers ≤ 385 would have a "much smaller fraction" factoring in the substrate primes. Computation: 67 of the 385 integers in [1, 385] factor in $\{2,3,5,7,11\}$ with at most one factor of 2 (density 17.4%); the irrep set has 9 such (density 75%). The 75 vs 17.4% comparison is genuinely non-generic, but the paper does not perform it.
- **Identities 1, 2, 3, 6 are standard Steiner-design parameters in substrate-flavored language.** "$77 = 7 \times 11$" and "$r = 21$" are textbook. The substrate-side reading does not add expository content beyond renaming.

The paper is honest about its open question. But I do not see, even within the *Monthly*'s relaxed standards, that the catalog rises above what Conway–Sloane (1999, Ch. 11) and the ATLAS already provide.

---

## §2. Decision recommendation

**Major revision.**

To meet the *Monthly* bar, the manuscript needs:

(i) **Identity 4 corrected.** The "six of twelve" claim is wrong; the correct counts (with derivation) need to appear, and the substrate-prime characterization needs to be revised to whatever statement is actually true (see M1 below).
(ii) **A non-genericity computation, not an assertion.** The 17% vs 75% density comparison (or its corrected version) needs to be in the paper, with a clean test against a null model.
(iii) **A real coincidence kept, decorative ones cut.** Identity 5 should be removed; Identities 1–3 and 6 should be presented as substrate-flavored renamings of textbook Steiner facts, not as separate "coincidences."
(iv) **Self-containment.** The substrate-prime distinction is the load-bearing definition, and it is delegated to the companion. A reader of the *Monthly* should not need to read another paper to understand what the "five substrate primes" are.

If these are addressed, the resulting paper would be a 4–6 page expository note suitable for the *Monthly* — with a tighter, sharper claim than the present six-item catalog. As it stands, the paper does not yet say what is true and does not yet defend why the *Monthly* should publish it.

---

## §3. Major comments

### M1. Identity 4 is misclaimed (CRITICAL)

**Location.** §4.4 (Theorem 4.4 "Substrate-prime irreps"); abstract.

**Claim.** "Six of $M_{22}$'s twelve irrep dimensions factor as products of substrate primes $\{3,5,7,11\}$ alone: $21, 55, 99, 154, 231, 385$. The dimension 154 has a single factor of 2; counting 154 as 'substrate-prime up to one factor of 2' is consistent with..."

**Issue.** The claim conflates two non-equivalent counts and silently drops representations.

The full $M_{22}$ irrep dimension list (Conway–Sloane 1999; ATLAS) is:
$$
\{1,\, 21,\, 45,\, 45,\, 55,\, 99,\, 154,\, 210,\, 231,\, 280,\, 280,\, 385\}.
$$

Direct factorization (verified below):

| dim | factorization | strict $\{3,5,7,11\}$? | with one factor of 2? |
|---:|:---|:---:|:---:|
| 1 | trivial | yes (vacuously) | yes |
| 21 | $3 \cdot 7$ | yes | yes |
| 45 | $3^2 \cdot 5$ | **yes** | yes |
| 45 | $3^2 \cdot 5$ | **yes** | yes |
| 55 | $5 \cdot 11$ | yes | yes |
| 99 | $3^2 \cdot 11$ | yes | yes |
| 154 | $2 \cdot 7 \cdot 11$ | no (has 2) | yes |
| 210 | $2 \cdot 3 \cdot 5 \cdot 7$ | no | yes |
| 231 | $3 \cdot 7 \cdot 11$ | yes | yes |
| 280 | $2^3 \cdot 5 \cdot 7$ | no | no (three 2's) |
| 280 | $2^3 \cdot 5 \cdot 7$ | no | no (three 2's) |
| 385 | $5 \cdot 7 \cdot 11$ | yes | yes |

**Correct counts.**

- *Strict* $\{3,5,7,11\}$ (no factor of 2): **seven** dimensions (excluding the trivial 1: 21, 45, 45, 55, 99, 231, 385). The paper's list (21, 55, 99, 154, 231, 385) **omits 45 (twice)** and **incorrectly includes 154**.
- *With at most one factor of 2*: **nine** dimensions (the seven above plus 154 plus 210). The paper's "six" is missing 45×2, 210, and (depending on reading) the trivial.

**Severity.** Critical for two reasons. First, the abstract and §4.4 state a numerical fact that is wrong; this is the kind of error the *Monthly* will not tolerate. Second, the silent exclusion of 45 is the more serious problem: the dimension 45 appears with multiplicity 2 and is structurally as substrate-prime as 21 or 99. A reader checking the claim will conclude either that the authors did not check, or that they cherry-picked the list to land at "six." Both readings are bad.

**Fix.** State the correct count. Likely the paper wants something like:

> Among $M_{22}$'s 12 irrep dimensions, **seven** (excluding the trivial 1) have all prime factors in $\{3,5,7,11\}$: namely 21, 45 (with multiplicity 2), 55, 99, 231, and 385. Two further dimensions (154, 210) factor entirely in $\{2,3,5,7,11\}$ with at most one factor of 2. Of the 12 total, **9** factor in $\{2,3,5,7,11\}$ with at most one factor of 2; only the two copies of 280 (with $2^3$) and the trivial 1 lie outside this band.

The corrected statement is just as suggestive as the wrong one, but it is correct.

### M2. Non-genericity is asserted, not computed (MAJOR)

**Location.** §4.4 Remark.

**Claim.** "Six of twelve $M_{22}$ irreps have dimensions in the substrate's prime monoid. This is a 50% density that is not generic: a random 12-tuple of integers ≤ 385 would have a much smaller fraction factoring entirely in $\{3,5,7,11\}$ (with at most one factor of 2)."

**Issue.** The "much smaller fraction" is asserted without computation. The actual computation (verified below):

- Integers in $[1, 385]$ factoring in $\{3,5,7,11\}$ with at most one factor of 2: **67** out of **385** (density **17.4%**).
- Of $M_{22}$'s 12 irrep dimensions, **9** satisfy this (density **75%**).

The 75% vs 17.4% comparison is a meaningful non-genericity statement, and it is exactly the test the paper is asserting without performing.

**Fix.** Add a one-paragraph explicit non-genericity computation. Use the corrected count from M1. State the null-model density and the observed density, and report a $p$-value or Bayes factor. For example:

> Under a null model where the 12 dimensions are i.i.d. uniform on $[1, 385]$, the probability that 9 or more of them factor in $\{2,3,5,7,11\}$ with at most one factor of 2 is $\binom{12}{9}(0.174)^9 (0.826)^3 + \cdots \approx [\text{computed value}]$. The observed concentration is therefore non-generic at level $p \approx [\text{value}]$.

This computation lifts the catalog from "we noticed something" to "we have a quantitative statement."

### M3. Identity 5 is arithmetic tautology (MAJOR)

**Location.** §4.5 (Theorem 4.5 "The 231 identity").

**Claim.** $77 \cdot W = 77 \cdot \tfrac{3}{50} = \tfrac{231}{50}$, with the substrate-side reading that the numerator 231 matches the unique $M_{22}$-irrep dimension factoring as $3 \cdot 7 \cdot 11$.

**Issue.** The identity is a one-line multiplication: $77 \cdot 3 = 231$. The factorizations $77 = 7 \cdot 11$ and $231 = 3 \cdot 7 \cdot 11$ make the multiplication's primes line up, but this is the same observation as Identity 1 (the hexad count is $7 \cdot 11$) plus the substrate's wobble numerator (3) being the "missing prime." The "identity" is the equation $77 \cdot 3 = 231$, with both sides factored by hand.

The substrate-side reading "Among the 12 $M_{22}$-irrep dimensions, 231 is the unique one whose factorization is exactly the product of three distinct substrate primes" is correct (231 is the only one in $\{3,5,7,11\}$ whose factorization is squarefree with exactly three distinct primes), but the *arithmetic identity* is not what makes 231 special; the *factorization pattern* is. The two are conflated.

**Fix.** Either (a) drop Identity 5 entirely and absorb the "231 is the unique squarefree-three-prime irrep" observation into Identity 4, or (b) reframe Identity 5 as the *factorization-pattern uniqueness* of 231, with a clean statement (e.g., "$231 \in \{\dim V_i\}_{i=1}^{12}$ is the unique irrep dimension whose prime factorization is a squarefree product of exactly three substrate primes"), without the cosmetic $77 \cdot W$ multiplication. The latter adds nothing.

### M4. Identities 1, 2, 3, 6 are standard Steiner-design facts (MAJOR)

**Location.** §4.1–4.3 and §4.6.

The four "identities":

- $b = 77 = 7 \cdot 11$ (Identity 1).
- $r = 21 = 3 \cdot 7$ (Identity 2).
- $\lambda_2 = 5$ (Identity 3).
- Block size $k = 6$ (Identity 6).

are textbook Steiner-system parameters for $S(3, 6, 22)$ (Conway–Sloane 1999, Ch. 11; Cameron, *Permutation Groups* 1999, Ch. 6; Wilson, *Finite Simple Groups* 2009, Ch. 5). Their factorizations into small primes are also textbook. The "substrate reading" for each is a one-line renaming (e.g., "$T^* = 5/7$ has numerator 5"; "the σ-cycle has length 6").

For a *Monthly* paper, the bar is that the expository value should exceed the textbook treatment. The present paper renames the textbook quantities; the renaming is the substrate side. A reader without the substrate companion has no way to evaluate whether the renaming is non-trivial.

**Fix.** Rather than presenting each as a separate "Theorem," consolidate Identities 1, 2, 3, 6 into a single short table headed "Standard Steiner-system parameters for $S(3,6,22)$, with substrate-prime decomposition." This is honest scholarship: textbook + a column of substrate-side primes. The expository value of the paper is then concentrated in the (corrected) Identity 4 and the non-genericity computation (see M2).

### M5. Self-containment failure (MAJOR)

**Location.** Throughout, especially §3 (the substrate).

The "five substrate primes" claim — the central conceit of the paper — depends on the companion `\cite{SandersGishFourCore}` for the substrate's definition. In the manuscript the substrate is described in §3 in three short paragraphs, with claims like:

- "$3$: the order of $\sigma^2$ on the $\sigma$-cycle (the trinitarian / triadic structure)." But $\sigma^2$ on a 6-cycle has order 3 — this is correct. (Verified: $\sigma$ a 6-cycle, $\sigma^2$ has order 3.)
- "$11$: the wobble denominator $W = 3/50$ scales out, but 11 appears in the substrate's $\Psi_B$-period contributions and in the $M_{22}$ irrep dimensions $V_{55}, V_{99}, V_{154}, V_{231}, V_{385}$."

The second bullet is where it gets uncomfortable. "$W = 3/50$ scales out" — what does this mean? The denominator of $W$ is 50, not 11. The claim that 11 is a substrate prime *because* of "$\Psi_B$-period contributions" is not defended in this paper; the *Monthly* reader has no way to evaluate it.

For the catalog to land, the substrate needs to define its primes from its own internal data, in this paper. As written, the reader is asked to take it on faith that $\{2,3,5,7,11\}$ are the substrate's distinguished primes; the structural defense is in the companion.

**Fix.** Inline the substrate's prime distinction in §3 with at least one sentence per prime explaining how it arises *from the substrate's own data*. If 11 cannot be defended without the $\Psi_B$ machinery, then either (a) inline $\Psi_B$, or (b) demote 11 to "appears in $|M_{22}|$, conjecturally substrate-distinguished" and tell the reader honestly.

Without this, the paper cannot stand alone, and a *Monthly* reader will close it without confidence in the central claim.

### M6. Identity 6 (block-size match) is weak (MAJOR)

**Location.** §4.6.

**Claim.** The σ-orbit on $\{1,7,6,5,4,2\}$ has size 6, the block size of $S(3,6,22)$.

**Issue.** Two integers — the cycle length of an involution's largest orbit, and the block size of a Steiner system — are both 6. The substrate-side reading is a one-line factorization with no prime; the Steiner-side fact is textbook. The identity is "6 = 6."

The remark following the theorem acknowledges this: "$S(3,6,22)$ is unique up to isomorphism, so any 6-element set is a hexad in some isomorphism class; whether the substrate selects a specific isomorphism class is a substantive representation-theoretic question (Section 6)."

**Fix.** Either (a) cut Identity 6 entirely (it is the weakest of the six, and the remark already concedes there is nothing to it without a representation-theoretic embedding theorem), or (b) state the embedding question as the actual content of the paper and prove (or fail to prove) the embedding. In the latter case, this becomes the paper's main result; the catalog becomes setup. I would not advise (b) without substantial new computation.

---

## §4. Specific technical issues

### S1. Author list mismatch

The README lists "Sanders + Gish" as the author lane and `WP_PARADOX_CLASSIFIER.md` is mentioned in the manuscript folder as a separate planned paper. The cover letter says "B. Mayes, Independent Researcher." The manuscript .tex lists "Brayden R. Sanders \and M. Gish" twice (which appears to be a duplicate of the same author block). Reconcile.

### S2. Wobble decomposition (§3.2)

"The wobble fraction $W = 3/50$ admits the decomposition $W = K + G \cdot 0$, $K = 3/50$, $G = 22/50$, $K + G = 1/2$."

This is mathematically incoherent as written. $W = K + G \cdot 0 = K = 3/50$, and the equation $K + G = 1/2$ is just $3/50 + 22/50 = 25/50 = 1/2$ — but this has nothing to do with the wobble decomposition. The "$G \cdot 0$" is presumably a typo or compressed notation from the companion.

**Fix.** Rewrite the wobble decomposition with proper notation. If the intended statement is that the wobble fraction $W = 3/50$ and a separate "gentleness" fraction $G = 22/50$ sum to $1/2$, say so cleanly without the spurious "$\cdot 0$".

### S3. The "$22$ matches $|\Omega_{22}|$" suggestion (§3.2)

"The gentleness numerator 22 matches $|\Omega_{22}|$."

This is a coincidence between two integers labeled 22, where one is a hand-defined fraction's numerator and the other is the size of $M_{22}$'s natural action. Without an underlying structural map, this is purely cosmetic.

**Fix.** Either build a map between the substrate and $\Omega_{22}$ that sends gentleness to the action set (this would be an *enormous* result, well beyond a *Monthly* note), or remove the claim. The current placement, in §3, primes the reader to expect a substantive identification that is not delivered.

### S4. Computational verification scripts (§5)

Three scripts named (`m22_verification.py`, `steiner_sigma_hexad.py`, `m22_decomposition.py`) are referenced. The `m22_verification.py` is described as verifying "the $M_{22}$-equivariant projections $P_1$ and $P_{21}$ commute with 1000 random $S_{22}$ permutations." But there is no $M_{22}$-equivariant content in the body of the paper — the body is about prime factorizations of irrep dimensions, not about projections.

**Fix.** Either (a) describe the scripts honestly as "verifies the listed Steiner-system parameters and the listed irrep-dimension factorizations" (which is what they should do for the present paper), or (b) bring in the $P_1, P_{21}$ projection content from the verification script into the body of the paper, where it would be a substantive new contribution.

### S5. Forward citation discipline

The companion `\cite{SandersGishFourCore}` is cited as "submitted to *Algebraic Combinatorics*, 2026 (J02)." For *Monthly* submission, "submitted" is fine, but the present paper depends on it for the substrate definition (M5). At minimum, the *status* of the companion needs to be known to the editor at the *Monthly* — if the companion is under revision, in press, or not yet refereed, the present paper's foundational dependency is a risk.

---

## §5. Minor comments

- **Title.** "Substrate-Prime: Order-Factorization Coincidences" is honest. The paper delivers what the title promises (a catalog of factorizations); whether it merits *Monthly* publication is the question.
- **Abstract.** The abstract states the catalog truthfully and disclaims a derivation. The "six identities" needs to be corrected to whatever count is actually true after M1–M6.
- **§2.** The introduction is clean. The Mathieu / Steiner facts are stated correctly with proper attribution.
- **§3.2.** "$0$ at size 1" — this is from a different paper's chain enumeration and does not belong here.
- **§4.4 proof.** "Direct factorization of each dimension; the dimensions are taken from the standard $M_{22}$ character table." This is correct as a method but does not establish the *count* of "six." See M1.
- **§5.** "All scripts run in <5 seconds with `numpy` and `sympy` as the only external dependencies." Good. But the URL for the deposited scripts is a long path inside a sprint bundle; consider depositing the verification scripts at a stable, citable location (Zenodo, with a DOI), which is the *Monthly*'s preference.
- **§6 open question 5.** "Other sporadic groups… $M_{11}, M_{12}, M_{23}, M_{24}$." The paper would be substantially stronger if it answered this question for at least $M_{12}$ (whose irreps are tabulated and small). The *Monthly* reader would benefit from a comparison row in a table.

---

## §6. Comparison to literature

### Conway–Sloane 1999, *Sphere Packings, Lattices and Groups* (3rd ed.).
Chapters 10–11 give the standard exposition of the Mathieu groups, Steiner systems $S(5,6,12)$ and $S(5,8,24)$, and the Leech lattice. The factorizations $|M_{11}| = 7920$, $|M_{12}| = 95040$, $|M_{22}| = 443520$, etc., and their decompositions into small primes, are textbook. The character tables are tabulated.

The present paper's "six coincidences" do not improve on Conway–Sloane's exposition; they re-present the standard parameters with substrate-side renamings.

### ATLAS of Finite Groups (Conway, Curtis, Norton, Parker, Wilson 1985).
The standard reference for character tables and conjugacy-class data of all sporadic groups. The $M_{22}$ irrep dimensions are tabulated and their factorizations are immediate.

### Mathieu moonshine (Eguchi–Ooguri–Tachikawa 2011 and the subsequent line).
The paper cites this as "open question 4." Mathieu moonshine for $M_{24}$ links the elliptic genus of K3 surfaces to the character table of $M_{24}$ via a generating function. This is a *substantive* coincidence: not just primes lining up, but generating-function coefficients matching irrep multiplicities.

The present paper's catalog has no analogue of this. The "coincidences" are arithmetic (primes match), not analytic (generating functions match) and not algebraic ($M_{22}$ does not act on the substrate).

### Diaconis 1988, *Group Representations in Probability and Statistics*.
For an exposition of finite Fourier analysis and group representations at the *Monthly* level, Diaconis (Ch. 1–2) sets the bar. Diaconis's hand is light: he motivates each definition, computes small examples, and connects to combinatorial identities. The present paper's substrate-side exposition (§3) is much terser and more reliant on external companions. To meet the Diaconis bar, §3 needs at least 2x its current length.

---

## §7. Constructive suggestions for resubmission

**Path A (single-coincidence note).** Cut the catalog to the one corrected, computed coincidence: the *non-generic concentration* of $M_{22}$-irrep dimensions in the substrate-prime monoid. This is a quantitative claim with a clean null-model test. Length: 4–6 pages. This is *Monthly*-appropriate.

**Path B (representation-theoretic embedding).** Develop Identity 6 (the σ-orbit as a candidate hexad) into a representation-theoretic embedding of the substrate into the $M_{22}$ action on $\Omega_{22}$. If such an embedding exists and is canonical, this is a substantive paper, plausibly for *J. Algebraic Combinatorics* rather than *Monthly*. Length: 12–20 pages. Significant new computation needed.

**Path C (catalog rewrite).** Keep the catalog but make every identity into a *theorem-statement-with-uniqueness*. E.g., "The 4-dim group $\mathbb{Z}/2 \times \mathbb{Z}/5$ is the unique abelian group of order 10 with prime decomposition matching $|M_{22}|$ at the squarefree level." Stretch each "coincidence" into a uniqueness statement. Length: 8–12 pages. This works only if the uniqueness statements are non-trivial.

I recommend Path A. The present paper has the seed of a good *Monthly* note — the non-generic concentration of $M_{22}$ irreps in the substrate-prime band — but the catalog framing dilutes it into "six coincidences," several of which are not coincidences at all.

---

## §8. Decision

**Major revision.**

The mathematical content is mostly correct (the Mathieu/Steiner facts are textbook-accurate), but the paper's central numerical claim (Identity 4) is wrong, and the catalog framing conflates textbook quantities with non-trivial coincidences. With the corrections in M1–M6, a single substantive observation — the non-generic concentration of $M_{22}$ irrep dimensions in the substrate-prime monoid — can be lifted into a clean *Monthly* note.

The paper's open question (whether the catalog is structural or coincidental) is honest and well-framed, but the paper is not yet at the bar where the question can be answered.

I encourage the authors to revise along Path A above and resubmit. The corrected version would, in my view, be publishable at the *Monthly*.

Reviewer's confidence: high on the M1 numerical error (verified by direct computation); medium on the M2 non-genericity assessment (depends on choice of null model); high on M3, M4, M6 (each is a structural observation about the manuscript's framing).

— Anonymous Referee, AMM, 2026-05-07
