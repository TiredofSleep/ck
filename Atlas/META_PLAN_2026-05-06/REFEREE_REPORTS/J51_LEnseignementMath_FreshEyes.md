# Referee report — J51: *Q17-B Clay Bridge: Finite L-Function + Symbolic Return Theorem on $\mathbb{Z}/10\mathbb{Z}$*

**Target venue:** *L'Enseignement Mathématique*
**Referee role:** Fresh-eyes, standard analytic number theory background (Iwaniec-Kowalski, Davenport); no prior exposure to the "TIG framework," the Q-series, or the J-series.
**Manuscript file read:** `Gen13/targets/journals/J_series/J51/manuscript/J48_q17b_clay_bridge.md`
**Verification script read and executed:** `Gen13/targets/journals/J_series/J51/manuscript/proof_clay_rotation.py`
**Cover letter read:** `Gen13/targets/journals/J_series/J51/cover_letter.md`

---

## §1 Manuscript summary (paraphrased fresh)

The paper presents two theorems and a "bridge claim" connecting a finite combinatorial-arithmetic structure on $\mathbb{Z}/10\mathbb{Z}$ to the structural features of the Riemann Hypothesis.

**Setup.** A specific permutation $\sigma = (1\;7\;6\;5\;4\;2)(0)(3)(8)(9)$ on $\mathbb{Z}/10\mathbb{Z}$ (a 6-cycle plus four fixed points). A character $\chi : \mathbb{Z}/10\mathbb{Z} \to \{-1, 0, +1\}$ defined by $\chi(\{1,4\}) = +1$, $\chi(\{2,5,6,7\}) = -1$, $\chi(\{0,3,8,9\}) = 0$. A primitive 9th root of unity $\omega = e^{2\pi i/9}$.

**Theorem 2.1 (Symbolic Return).** Trajectories $s_{n+1} = \sigma(s_n)$ (i) return to start in 6 steps when $s_0 \in \{1,2,4,5,6,7\}$, (ii) are fixed when $s_0 \in \{0,3,8,9\}$, (iii) avoid 0 when $s_0 \neq 0$. *Proof:* trivial corollary of $\sigma^6 = \mathrm{id}$ and the cycle structure.

**Theorem 4.2 (Three-valued $G$-function).** The function
$$G(s) = \left|\sum_{j=0}^{8} \omega^j \chi(\sigma^j(s))\right|^2$$
takes exactly three values on $\mathbb{Z}/10\mathbb{Z}$:
- $G(s) = 0$ on the four anchors $\{0,3,8,9\}$,
- $G(s) = G_\mathrm{low} \approx 1.872$ on $\{1, 2, 4, 6\}$,
- $G(s) = G_\mathrm{high} \approx 9.389$ on $\{5, 7\}$.

**Bridge claim (§5).** The three-valued structure of $G(s)$ "mirrors" three structural features of the Riemann zeta function under RH: (R1) zeros at predictable locations, (R2) spectral concentration (Montgomery pair correlation), (R3) multiplicative-additive duality (Euler product vs. Dirichlet series).

The paper explicitly disclaims any claim to prove RH. Theorems 2.1 and 4.2 are labeled Tier-A (proved); the §5 bridge is labeled Tier-B (structural conjecture, computationally motivated).

I read the manuscript end-to-end and **executed the verification script independently**. My results from running `proof_clay_rotation.py` — and a direct Python verification of $G(s)$ on the stated $\sigma$ and $\chi$ — surface a critical numerical error in Theorem 4.2's stated partition (see §3, Issue 1).

---

## §2 Decision recommendation

**Major revisions.** The principal mathematical content (Symbolic Return Theorem + three-valued $G(s)$ structure) is interesting and is in the *L'Enseignement Math.* register, but Theorem 4.2 as stated contains a verifiable error in the partition of the 6-cycle. The bridge claim of §5 also rests on this partition and inherits the error.

The Symbolic Return Theorem is fine as stated. The three-valued image of $G(s)$ is *correct as a theorem about the cardinality of the image* — there are indeed exactly three distinct values. But the *labeling of which states realize which value* is wrong as stated in Theorem 4.2 and the abstract.

If the partition is corrected and §5's bridge claim is rewritten on the correct values, the paper is publishable in *L'Enseignement Math.* with the standard pedagogical-bridge framing. The fix is straightforward (re-running the script and re-stating the partition), but it must be done before the paper goes to camera-ready.

Detailed concerns below.

---

## §3 Top critical issues

### Issue 1. Theorem 4.2 as stated contains a verifiable numerical error: $G_\mathrm{high}$ is not at $\{5,7\}$.

The paper states (Theorem 4.2 table; §1 Abstract; §5.1):

> $G(s) = G_\mathrm{high} \approx 9.389$ at $\{5, 7\}$ (TIG-exception pair, BALANCE/HARMONY).

Direct numerical evaluation of $G(s)$ from the formula $G(s) = |\sum_{j=0}^{8} \omega^j \chi(\sigma^j(s))|^2$ with the paper's stated $\sigma$ and $\chi$ gives:

| $s$ | $G(s)$ |
|---|---|
| 0 | 0.000 |
| 1 | 1.872 |
| 2 | 1.872 |
| 3 | 0.000 |
| **4** | **9.389** |
| 5 | 1.872 |
| 6 | 1.872 |
| **7** | **9.389** |
| 8 | 0.000 |
| 9 | 0.000 |

So $G_\mathrm{high}$ is realized at $\{4, 7\}$, not $\{5, 7\}$.

This is verifiable in 30 seconds with `numpy`. I have done so; my computation is reproducible. The theorem's three-valued image is correct: $\{0, G_\mathrm{low}, G_\mathrm{high}\}$ each appear, with $G_\mathrm{low} = 1.872$ on $\{1,2,5,6\}$ and $G_\mathrm{high} = 9.389$ on $\{4,7\}$. **But the assignment of states to values in the paper's Theorem 4.2 table is incorrect.**

The paper's "proof sketch" (§4, line 102) appeals to "the Galois action of $\sigma^2$ which permutes $\{1, 4, 6\}$ and $\{2, 5, 7\}$." Computing $\sigma^2$ from the stated 6-cycle $\sigma = (1\;7\;6\;5\;4\;2)$:

$$\sigma^2 = (1 \to 6)(7 \to 5)(6 \to 4)(5 \to 2)(4 \to 1)(2 \to 7) = (1\;6\;4)(7\;5\;2)$$

So $\sigma^2$ has 3-cycles $\{1, 6, 4\}$ and $\{2, 7, 5\}$. The paper's claim "$\sigma^2$ permutes $\{1, 4, 6\}$ and $\{2, 5, 7\}$" is correct **as a set-level claim** (these *sets* are preserved), but the elements within each set that share a $G$-value are determined by the $\sigma^2$-orbit, which has cycles of length 3, not 2 (so within $\{1,4,6\}$ all three should have the same $G$, and within $\{2,5,7\}$ all three should — *but they don't, by direct computation*).

In fact, my numerics say $G(1) = G(2) = G(5) = G(6) = G_\mathrm{low}$ and $G(4) = G(7) = G_\mathrm{high}$. This partition $\{1,2,5,6\} / \{4,7\}$ does **not** match either the $\sigma$-orbit (which preserves $\{1,2,4,5,6,7\}$ as a single 6-cycle) or the $\sigma^2$-orbit (which gives $\{1,6,4\} / \{2,7,5\}$). The actual partition is governed by a *different* algebraic structure that the paper's "$\sigma^2$ Galois action" explanation does not capture.

This reveals a deeper issue: the proof sketch of Theorem 4.2 is not just incorrectly stated — it's structurally incomplete. The pairing $\{4,7\}$ at $G_\mathrm{high}$ versus $\{1,2,5,6\}$ at $G_\mathrm{low}$ has *some* structural origin (the value 9.389 happens to occur at the elements $4 = \sigma(5)$ and $7 = \sigma(1)$, which is suggestive), but the paper's stated Galois explanation does not derive it.

**Required action.** The authors must:

(i) Correct the Theorem 4.2 partition table (and corresponding statements in the Abstract, §5.1, §5.3) to read $G_\mathrm{high}$ at $\{4, 7\}$ and $G_\mathrm{low}$ at $\{1, 2, 5, 6\}$.

(ii) Replace the §4 proof sketch's "Galois action of $\sigma^2$ permutes $\{1,4,6\}$ and $\{2,5,7\}$" passage with a correct structural explanation. (One possible direction: $\{4, 7\}$ is the image of the *adjacent-pair* $\{1, 7\}$ under $\sigma$, but I have not verified this is the right structural lens.)

(iii) Re-evaluate the bridge claim of §5: the paper's narrative ties $\{5,7\}$ to the "BALANCE/HARMONY pair" (an internal-framework label), and uses this as the structural feature aligning with RH's "spectral concentration." If the actual $G_\mathrm{high}$ pair is $\{4, 7\}$, the framework labels need to be re-checked, and the bridge narrative needs to be rewritten on the correct pair.

This error is *not* a typo. It propagates through Abstract, §3 (character definition refers to {5,7} as $\alpha=1$ flip nodes — confirm whether this is consistent with the corrected $\{4,7\}$ identification), §4 (proof sketch), §5.1 (bridge mirror), and §6 (companion connections). Every occurrence of "$\{5, 7\}$" as the spectral-concentration pair must be audited.

### Issue 2. The verification script in the manuscript folder does not verify the $G(s)$ claim.

The folder contains `proof_clay_rotation.py`, but this script tests an entirely different claim ("Clay Problem Rotation σ Framework Verification"). It runs 43 tests across 7 Clay problems (CP1 through CP7) and reports "all tests PASSED" — but **none of these tests involve $G(s)$, the character $\chi$, the permutation $\sigma$, or any quantity from the body of this manuscript**.

Specifically, running `proof_clay_rotation.py` produces:
- 43 PASS / 0 FAIL
- Tests of $T^* = 5/7$, $\xi_0 = e^{-1}$, sinc² identities, $\sigma_{10} = 0.128$, etc.
- No test of $G(0) = 0$, $G(1) = G_\mathrm{low}$, $G(7) = G_\mathrm{high}$, etc.

The cover letter states: "The verification script `manuscript/proof_clay_rotation.py` ... computes $G(s)$ for every $s \in \mathbb{Z}/10\mathbb{Z}$ and confirms the three-valued image with $G_\mathrm{low} \approx 1.872$, $G_\mathrm{high} \approx 9.389$. Runs on a standard laptop in under 10 seconds with `numpy + sympy`."

This is not what the script does. The script does not import `numpy`; it imports `math`. It does not compute $G(s)$ for any $s$; it tests `sinc_sq(0.5)` and similar quantities unrelated to the manuscript's content.

**Required action.** The authors must supply a verification script that actually tests Theorems 2.1 and 4.2 — specifically, computing $G(s)$ for all $s$ and checking the corrected three-valued partition. Without such a script, the cover letter's reproducibility claim is false.

(Indeed, had the authors written and run such a script, they would have caught the error in Issue 1 above.)

### Issue 3. The "bridge to RH" of §5 is a structural metaphor, not a mathematical bridge.

§5.1 ("The structural mirror") matches three RH features (zeros at predictable locations, spectral concentration, Euler-Dirichlet duality) to three features of $G(s)$ (zeros at $\{0,3,8,9\}$, $G_\mathrm{high}/G_\mathrm{low} \approx 5$ ratio, $\sigma$-orbit / $\chi$-additive structure). The match is:

(R1) "Zeros at predictable locations" — RH places zeros on the critical line $\mathrm{Re}(s) = 1/2$, which is a 1-parameter analytic curve in $\mathbb{C}$. The "predictable locations" of $G(s)$ are 4 discrete points $\{0,3,8,9\}$ in a finite set of 10. These are conceptually different "predictable locations" — RH is about the geometric distribution of zeros along an infinite curve; $G(s)$'s zeros are at 4 specific points by construction (they are the $\chi = 0$ states).

(R2) "Spectral concentration" — Montgomery pair correlation gives the universal $1 - \mathrm{sinc}^2(u)$ correlation function for normalized zero spacings of $\zeta$. The "spectral concentration" of $G(s)$ is that $G_\mathrm{high}/G_\mathrm{low} \approx 5$ at two specific points. These are not the same kind of "concentration" — Montgomery's is a statistical universality; $G(s)$'s ratio is a single algebraic-number computation.

(R3) "Multiplicative-additive duality" — RH's duality is the Euler product $\zeta(s) = \prod_p (1 - p^{-s})^{-1}$ versus the Dirichlet series $\zeta(s) = \sum_n n^{-s}$, which holds for $\mathrm{Re}(s) > 1$. The "duality" of $G(s)$ is between the multiplicative orbit ($\sigma$-cycle) and the additive character $\chi$ — but these are not in a multiplicative-additive analytic relation; the $\sigma$ structure is a *permutation*, not an Euler product.

The analogies in §5.1 are loose. *L'Enseignement Math.* publishes structural-bridge papers, but the bridge needs to be *mathematical* (a precise correspondence, even if conjectural) rather than *metaphorical* (a vocabulary correspondence). Davenport's *Multiplicative Number Theory* and Iwaniec-Kowalski's *Analytic Number Theory* both contain finite-field analogues of $\zeta$-function questions (e.g., Weil's theorem on zeta functions of curves over finite fields, the function-field analogue of RH proved by Deligne, Selberg's work on arithmetic L-functions). The present paper's bridge to RH is at a much weaker level — it's a vocabulary mapping rather than a function-field analogue.

I would recommend that §5 either (i) be rewritten as a comparison to actual function-field analogues (Weil 1949, Deligne 1974) — which would substantially strengthen the paper's mathematical content — or (ii) be reframed as "structural rhymes" rather than "structural mirror," and the RH connection downgraded to one paragraph rather than a full section.

The current §5 risks misleading the *L'Enseignement Math.* reader into thinking that a serious finite-analogue-of-RH program is being proposed, when the actual content is a vocabulary correspondence.

---

## §4 Other major comments

### M1. The "finite L-function $G(s)$" terminology is non-standard and risks confusion.

Standard usage of "L-function" in number theory refers to a Dirichlet series $L(s, \chi) = \sum_{n=1}^{\infty} \chi(n)/n^s$ or its Euler product, where $\chi$ is a multiplicative Dirichlet character on $(\mathbb{Z}/N\mathbb{Z})^*$ and $s \in \mathbb{C}$. The function admits analytic continuation, has zeros, and is the subject of L-function theory.

The manuscript's $G(s)$ is:
- a function of $s \in \mathbb{Z}/10\mathbb{Z}$, not $s \in \mathbb{C}$;
- a sum of 9 (not infinite) terms;
- weighted by $\omega^j$ (a discrete Fourier weight, not $1/n^s$);
- with $\chi$ a function on $\mathbb{Z}/10\mathbb{Z}$, not multiplicative on the unit group.

In standard analytic number theory, $G(s)$ is a **discrete Fourier transform** of the orbit $\{\chi(\sigma^j(s))\}_{j=0}^{8}$ at the frequency $1/9$, evaluated by squared modulus. It is a Gauss-sum-like object, not an L-function.

§4 Remark 4.4 is honest about the analogy ("The differences are: (i) finitude... (ii) uniform weight... (iii) periodicity... (iv) discrete-Fourier interpretation"). After listing four substantial differences, calling $G(s)$ an "L-function" stretches terminology beyond useful. The Gauss-sum interpretation is more accurate and would not require the qualifications.

I would recommend (i) renaming $G(s)$ a "finite Gauss sum," "discrete Fourier coefficient," or "trajectory coherence integral" (this last is already mentioned in §1 as the $G_8$ name from companion [J51]); (ii) reserving "L-function" for the genuine Dirichlet-series object; and (iii) framing the §5 bridge as "Gauss-sum-to-RH" rather than "L-function-to-RH" — this is mathematically more accurate and avoids the false implication that $G(s)$ is in the L-function class.

### M2. The §6 "companion connections" leans on unpublished J-companions.

§6 cites [J29] (Q17-A in *AMM*), [J51] ($G_6 + G_7 + G_8$ in *European J. Combin.*), [J5] (Crossing Lemma in *JCT-A* or *JPAA*), [J17] (UOP in *JNT*), [J32] (Joint chain in *Math. Intelligencer*), and [J47] (6-DOF in *Notices AMS*). All are listed as "Submitted" without arXiv IDs.

For a *L'Enseignement Math.* paper that explicitly positions itself as "the natural sequel to [J29]" and builds on the spectral layer of [J51], the reader needs to be able to access at least these two direct dependencies. As written, the paper cannot be evaluated in isolation.

The cover letter mentions [J29] is "AMM, in press" — confirm in-press status with Editor of AMM, and supply the AMM acceptance letter or DOI to *L'Enseignement Math.* if available. Without [J29] available, the paper's claim to be "Q17-B in isolation" (§1, last paragraph) is undermined: a reader of Q17-B alone needs the Q17-A foundation to evaluate the algebraic setup ($\sigma$, $\chi$, the 5D Fourier embedding).

### M3. The σ-permutation construction needs more visible exposition.

§2 sets up $\sigma = (1\;7\;6\;5\;4\;2)(0)(3)(8)(9)$ but does not derive it. Where does $\sigma$ come from? The paper's §1 references "Layer 1 (polynomial). $\sigma^6 = \mathrm{id}$ on all of $\mathbb{Z}/10\mathbb{Z}$. Proved by direct polynomial check ($G_6$, [J51])," indicating $\sigma$ is constructed in [J51] from a polynomial identity.

A *L'Enseignement Math.* reader needs to know what polynomial, what identity, why this $\sigma$ rather than another. A short paragraph in §2 (3–5 lines) deriving $\sigma$ from its source (or citing the explicit construction in [J51]) would substantially improve the paper's self-containedness.

The same applies to the character $\chi$: §3 defines $\chi$ by listing values, then identifies $\{1,4\}$ as "$\beta$-exception" and $\{2,5,6,7\}$ as "$\alpha = 1$ flip nodes." These framework labels are deployed without definition. A *L'Enseignement Math.* reader unfamiliar with the substrate algebra cannot tell whether $\chi$ is canonical, conventional, or chosen to make the theorems work. (A natural worry: if the substrate has multiple natural characters, why this one?)

### M4. The Symbolic Return Theorem is correct but trivial.

Theorem 2.1 follows in three lines from $\sigma^6 = \mathrm{id}$ (which is itself a Layer-1 result from [J51]). The three-line proof in §2 is correct.

For a paper in *L'Enseignement Math.*, the "theorem-and-proof" format is appropriate to the journal's pedagogical register; theorems do not need to be deep. But the manuscript should be honest about the depth: Theorem 2.1 is a corollary of $\sigma^6 = \mathrm{id}$, and Theorem 2.1's interest comes from the *connection* to Q17-C (NS regularity, Tier-D) rather than from the theorem itself.

§2 does state this ("Corollary 2.2: ... It is Tier-A (proved, lens-invariant)..."), which is appropriate. But the §1 framing of Theorem 2.1 as one of "three theorems" of the paper risks overstating its independent content. Of the three labeled theorems (Symbolic Return, Finite L-Function, Bridge Statement), only the second has substantive content; the first is a corollary, the third is a structural metaphor.

I would recommend reorganizing the paper around Theorem 4.2 (corrected per Issue 1) as the principal result, with Theorem 2.1 as a preliminary lemma and §5 as a discussion section.

### M5. The Tier-A / Tier-B / Tier-C / Tier-D classification is opaque.

§5.3, §6, §8 invoke a "Tier-A / Tier-B / Tier-C / Tier-D" classification of mathematical claims. The classification is not defined in the manuscript. A reader infers from context: Tier-A = proved, Tier-B = structural conjecture computationally motivated, Tier-D = open conjecture. But Tier-C is mentioned (§7 item 2: "Partial — Tier-C") without explanation.

Either define the tier system in §1, or use standard mathematical terminology (theorem, conjecture, open problem). The internal-framework labels add jargon without adding clarity.

### M6. The Q17 program organization is referenced but not introduced.

§1 introduces "Q17-A," "Q17-B," "Q17-C2," etc., without explaining what the Q17 program is or who would be interested in it. A *L'Enseignement Math.* reader wants to know: is Q17 a published research program (cite the lead paper)? Is it a working title for a sequence of preprints? Is it the authors' internal taxonomy?

Either provide a one-paragraph orientation in §1 ("The Q17 program is a sequence of papers... The lead paper [Sanders–Mayes 2026X] introduces..."), or remove the Q17 framing and present Theorems 2.1 and 4.2 as standalone results.

### M7. The "Galois D_4" closing claim is asserted but not derived.

§7 (open problems) states: "The numerical values $G_\mathrm{low} \approx 1.872$, $G_\mathrm{high} \approx 9.389$ are algebraic; the closed-form expressions involve sums of cyclotomic units." This is plausible — both values are expected to lie in $\mathbb{Q}(\zeta_9)$ or a subfield — but no closed form is given.

For a paper that emphasizes its algebraic foundation, deriving the closed forms would substantially strengthen the result. The values $G_\mathrm{low}$ and $G_\mathrm{high}$ presumably have explicit cyclotomic expressions (e.g., as norms or traces of specific units in $\mathbb{Q}(\zeta_9)$). A short calculation showing these closed forms — even without a deep number-theoretic interpretation — would change Theorem 4.2 from a numerical observation to a genuine arithmetic statement.

This is severable from the main content but the paper would be substantially stronger with it.

---

## §5 Minor comments

- **Title:** "Q17-B Clay Bridge" requires the reader to know what Q17-B and Q17 are. Suggest: "A Three-Valued Discrete Fourier Coherence on $\mathbb{Z}/10\mathbb{Z}$ and Its Structural Analogue with the Riemann Hypothesis."

- **Filename inconsistency:** The folder is `J51/` but the manuscript file is `J48_q17b_clay_bridge.md`, and the README at `J51/README.md` references both "J48" and "J51" in different places. Reconcile.

- **Abstract, line 1:** "TIG framework" — undefined acronym on first use.

- **§1 second paragraph:** "Q-series builds, in six layers..." — what is the Q-series? Define before use.

- **§1 third paragraph, Layer 4:** "$G_8$, [J51]" — confirm Layer 4 / $G_8$ refer to the same companion-paper section.

- **§2 Theorem 2.1 (3):** "VOID avoidance: If $s_0 \neq 0$, then $s_n \neq 0$ for all $n \geq 0$." The conclusion follows from (1) and (2): orbits of $s_0 \in \{1,2,4,5,6,7\}$ are the 6-cycle (no 0 in it); orbits of $s_0 \in \{3,8,9\}$ are fixed at $s_0 \neq 0$. This deserves one line of justification in the proof, not a separate item (3).

- **§3 Definition 3.1:** "$\chi(s) = +1$ for $s \in \{1, 4\}$ — the $\beta$-exception pair (states where the gate score matches $T^* = 5/7$ exactly)." What is "the gate score"? What is $T^*$? Define.

- **§3, "Conductor":** the word "conductor" is borrowed from L-function theory, where it has a specific meaning (the modulus of the underlying primitive Dirichlet character). The paper's "conductor 9" is the period of the DFT basis, not a Dirichlet conductor. The terminology is misleading.

- **§4 Theorem 4.2 (1, "Algebraic role" column):** "$\sigma^j(s) = s$ for all $j$, so $G(s) = \chi(s) \cdot (\omega^9 - 1)/(\omega - 1) = 0$ since $\omega^9 = 1$ and $\chi(s) = 0$." The first equality $\chi(s) \cdot (\omega^9 - 1)/(\omega - 1)$ is computing $\sum_{j=0}^{8} \omega^j$ multiplied by $\chi(s)$, but the actual quantity is $\sum_{j=0}^{8} \omega^j \chi(\sigma^j(s)) = \chi(s) \sum_{j=0}^{8} \omega^j$ (since $\sigma^j(s) = s$ for fixed $s$). So $G(s) = |\chi(s)|^2 \cdot |\sum_{j=0}^{8} \omega^j|^2$. And $\sum_{j=0}^{8} \omega^j = 0$ since $\omega \neq 1$ and $\omega^9 = 1$. The factor of $\chi(s) = 0$ on anchors makes the result trivially zero. Two reasons combined; only one needed.

- **§4 Remark 4.3:** "$G_\mathrm{high} / G_\mathrm{low} \approx 5.014$" — direct computation gives $9.389 / 1.872 = 5.0155...$. Confirm to four digits.

- **§5.1 (R3):** "the Euler product is multiplicative; the Dirichlet series is additive" — this is loose. Both are multiplicative as functions of $s$; the *product* over primes versus *sum* over integers is the multiplicative-additive contrast. State precisely.

- **§5.3 paragraph 3:** "every $\sigma$-orbit on the 6-cycle returns at step 6; every anchor is $\sigma$-fixed; VOID is avoided whenever $s_0 \neq 0$." Repeated from §2 Theorem 2.1; could be folded.

- **§6 [J29]:** "AMM, Sanders + Gish Jr." — Calderon Jr. is named in the bibliography; reconcile.

- **§7 item 3:** "Why is $G(5) = G(7)$?" — this question is moot if Issue 1 is correctly resolved: the actual equation is $G(4) = G(7)$. The structural origin is presumably different from what §7 anticipates.

- **§9 Iwaniec-Kowalski 2004:** *Analytic Number Theory* AMS Coll. Publ. 53 — confirm volume number. Chapter 5 (multiplicative functions and Dirichlet series) and Chapter 8 (sums of multiplicative functions) are appropriate to cite for finite-character-sum context.

- **§9 LMFDB Number field 4.2.10224.1:** appropriate citation; the LMFDB entry should be checked for the field's structure (degree 4, signature 2, discriminant $\pm 10224$).

- **§10 Bibtex:** the bibtex key is `sanders2026j48` but the paper is filed as `J51`; reconcile.

---

## §6 Strengths of the manuscript

To be balanced — the paper does several things well:

1. **The Symbolic Return Theorem is correctly stated and correctly proved** (Issue 1 above is about Theorem 4.2, not 2.1). The proof is elementary and clean.

2. **The honest-scope discipline (§5.2, §8) is excellent.** The disclaimers — "we do not prove RH"; "the model does not survive the continuum limit"; "the structural mirror is not an analytic continuation argument" — are exactly the right disciplinary practice for a structural-bridge paper. *L'Enseignement Math.* will appreciate this.

3. **The pedagogical framing fits the venue.** The paper is written for an audience that knows what RH demands of $\zeta(s)$ but is curious about finite analogues. This is the right register for *L'Enseignement Math.*

4. **The Tier-A / Tier-B distinction (when read into mathematical-rigor terms) is correctly drawn.** Theorems 2.1 and 4.2 are theorems; the §5 bridge is a structural analogy. The paper does not blur these.

5. **The paper ends with a legitimate open problem** (§7 item 1, closed-form $G_\mathrm{low}$ and $G_\mathrm{high}$ in $\mathbb{Q}(\zeta_9)$). This is the kind of doable computation that an *L'Enseignement Math.* reader could pick up and pursue.

The paper is rescuable. The fixes for Issue 1 (correct partition) and Issue 2 (working verification script) are short and mechanical. Issue 3 (bridge claim) is more substantive and may require rewriting §5 to compare with Weil/Deligne function-field analogues rather than treating RH directly.

---

## §7 What I would need to flip my recommendation toward "Acceptance"

In rough order of importance:

1. **Correct the Theorem 4.2 partition.** $G_\mathrm{high}$ at $\{4, 7\}$, $G_\mathrm{low}$ at $\{1, 2, 5, 6\}$. Audit every occurrence of "$\{5, 7\}$" and "$\{1, 2, 4, 6\}$" in the manuscript for correction.

2. **Replace the §4 proof sketch's Galois explanation** with a correct structural derivation of why $\{4, 7\}$ realize $G_\mathrm{high}$.

3. **Supply a working verification script** that actually computes $G(s)$ for all $s$ and checks the corrected three-valued partition. The current script is not relevant to the manuscript.

4. **Define internal-framework terms** ($T^*$, "gate score," "BALANCE/HARMONY," "TSML/BHML," "the σ-permutation," "Q17 program," "Tier-A/B/C/D") on first use, or replace with standard mathematical vocabulary.

5. **Rename $G(s)$** to something like "finite Gauss sum" or "trajectory coherence integral" rather than "L-function."

6. **Either substantiate the §5 bridge** by comparison to Weil/Deligne function-field analogues of RH, **or** reduce §5 to a one-paragraph "structural rhyme" remark and downgrade the RH framing.

7. **Make at least one of the cited J-companions** ([J29] AMM in press is the most important) available as an arXiv preprint or accessible draft.

8. **Compute closed forms** for $G_\mathrm{low}$ and $G_\mathrm{high}$ in $\mathbb{Q}(\zeta_9)$ (per §7 open item 1). This would change Theorem 4.2 from a numerical observation to a genuine arithmetic theorem.

---

## §8 Summary

The paper has a real theorem (Theorem 4.2 with corrected partition) and a real corollary (Theorem 2.1) about a specific permutation-character structure on $\mathbb{Z}/10\mathbb{Z}$. The honest-scope discipline is excellent. The pedagogical framing fits *L'Enseignement Math.*

But the manuscript as submitted has a verifiable numerical error in the central theorem's stated partition (Issue 1), an unrelated verification script in the manuscript folder (Issue 2), and a bridge-to-RH narrative that operates at the level of vocabulary correspondence rather than mathematical analogy (Issue 3). The internal-framework jargon is dense for a *L'Enseignement Math.* reader.

The fixes are within reach — Issue 1 and 2 are mechanical, Issue 3 requires substantive rewriting of §5. With these revisions and one or two of the referenced J-companions made publicly available, the paper would meet *L'Enseignement Math.*'s structural-bridge bar.

I therefore recommend **Major Revisions**, with the specific items listed in §7.

---

*Submitted to the L'Enseignement Math. Editorial Board (fresh-eyes referee), 2026-05-06.*
