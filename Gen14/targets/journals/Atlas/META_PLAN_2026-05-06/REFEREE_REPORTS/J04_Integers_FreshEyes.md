# Referee report — J04: *The Sinc² Zero Law for Squarefree Moduli*

**Target venue:** *Integers — Electronic Journal of Combinatorial Number Theory*
**Referee role:** Fresh-eyes, standard number-theory literature only.
**Manuscript file read:** `Gen13/targets/journals/J_series/J04/manuscript/sinc2_zero_law.tex`
**Verification script read:** `Gen13/targets/journals/J_series/J04/manuscript/proof_d25_loop_closure.py`

---

## §1 Manuscript summary (paraphrased fresh)

The paper studies the squared sinc function `sinc²(x) = (sin(πx)/(πx))²` evaluated at rational arguments `k/b` with squarefree denominator `b > 1`. Section 1 records what the authors call the "basic divisibility biconditional":

> **Lemma 1.** For `b > 1` and `k ≥ 1`, `sinc²(k/b) = 0 ⟺ b ∣ k`.

The proof is a one-line observation: `sin(πk/b) = 0 ⟺ k/b ∈ ℤ ⟺ b ∣ k`.

Section 2 then poses the following question for squarefree `b = p₁p₂…pᵣ`: what is the smallest `k ≥ 1` such that `sinc²(k/d) = 0` for at least one non-trivial divisor `d ∣ b`? Theorem 2 ("Squarefree sinc² Zero Law") answers `k = p₁ = spf(b)`. The proof is two short paragraphs; the heart is `gcd(k, b) = 1` for `k < p₁` because every prime divisor of `b` is `≥ p₁`.

Sections 3–4 list three corollaries (a "loop closure" inclusion-monotonicity statement, a "prime-indexed amplitude transitions" statement, a "stability window" of width `p₁ − 1`) and record the boundary value `sinc²(1/2) = 4/π²`. Section 5 states the result as an `sinc²` shadow of the "First-G Event Localization Theorem" of a companion paper. Section 6 reports a Python verification over primes `3 ≤ p ≤ 199`. Section 7 disclaims overreach (no claim about RH, distribution of primes, etc.).

---

## §2 Decision recommendation

**Reject.** (With encouragement to consider a 1-page expository note for *Math. Mag.* or similar pedagogical venue if the authors wish to publish.)

This recommendation is reluctant — the paper is honest, well-written, and self-aware — but the substance is below the threshold for *Integers*. Details below.

---

## §3 Top 3 critical issues

### Issue 1. The main theorem is a one-line corollary of a one-line lemma; the squarefree hypothesis is decorative.

Theorem 2 says: the smallest `k ≥ 1` for which some non-trivial divisor `d ∣ b` divides `k` is `k = p₁`. After Lemma 1, this reduces to a fact every undergraduate proves on day one of a number-theory course:

> The smallest `k ≥ 1` with `gcd(k, b) > 1` is the smallest prime factor of `b`.

This is true for **every** `b > 1`, squarefree or not — `gcd(k, b) > 1` requires `k` to share a prime with `b`, and the smallest such prime is `spf(b)` regardless of multiplicities. The author's Remark after Theorem 2 acknowledges that the squarefree hypothesis is needed only "to ensure that the ladder of prime divisors of `b` has a clean smallest-element structure (every prime power `pᵃ ∣ b` collapses to its prime base)" — i.e., the hypothesis is not used at all. The argument goes through verbatim for any `b > 1` because the smallest prime in the radical and the smallest prime of `b` coincide.

So Theorem 2 reduces to `spf(b) = spf(b)`. The `sinc²` window dressing does not change this.

### Issue 2. The corollaries restate Theorem 2 in three different vocabularies without adding content.

- **Corollary 1 (loop closure):** "as `k` runs from 1 to `b`, `Z_k(b)` grows with `k` and equals all of `Div(b) ∖ {1}` at `k = b`." This is just `gcd(k, b)` is monotone (in the divisibility order) along multiples and `gcd(b, b) = b`. Standard.
- **Corollary 2 (prime-indexed transitions):** restates `sinc²(k/p_j) = 0 ⟺ p_j ∣ k`, applied separately to each `p_j ∣ b`. This is Lemma 1 applied to the primes dividing `b`.
- **Corollary 3 (stability window):** "no zeros for `k < p₁`." This is part (i) of Theorem 2.

None of these introduces new combinatorial data, generating function, asymptotic, or sieve-theoretic structure.

### Issue 3. The "real machinery" (Fejér / sin² identity, continuum limit) promised in the README and §5 is absent from the paper itself.

The cover letter and §5's "harmonic pre-echo function `R(k,b) → sinc²(k/b)` as `b → ∞`" suggest a discrete-Fejér / spectral connection. But the manuscript proves nothing about this limit — equation (5) of §5 is stated without proof and not used elsewhere. Theorem 2 is proved without `sinc²` ever appearing in a nontrivial role: the entire content lies in the divisibility lemma, and `sinc²(k/d) = 0` is a stand-in for `d ∣ k`.

If the authors mean to claim a Fejér-kernel / Tauberian / pair-correlation result, that would be a different paper. The present paper does not contain one.

---

## §4 Other major comments

**M1. Self-overlap with the cited companion (J04, "First-G Event").** Section 5 explicitly states Theorem 2 is "the `sinc²` image" of a theorem in a companion paper, with verification shared. This is not in itself disqualifying — `Integers` does publish elementary notes — but the per-quarter cap and the cover letter wording ("second submission to `Integers` this quarter") together suggest two separate elementary notes are being submitted whose mathematical content is identical modulo the substitution `sinc²(k/d) = 0 ↔ d ∣ k`. This is a problem for editorial workflow regardless of mathematical merit.

**M2. The Montgomery pair-correlation reference (§4) is a non-sequitur.** Montgomery's pair-correlation conjecture concerns the spacing of nontrivial zeros of `ζ(s)` and the function `1 − sinc²(u)` where `u` is a normalized spacing. Citing this in a section computing `sinc²(1/2) = 4/π²` is window-dressing — there is no link beyond the function `sinc²` appearing in both contexts.

**M3. The verification script's "fold" content is irrelevant and confused.** `proof_d25_loop_closure.py` computes the location where `sinc²(x) = 1/2` via bisection between `3/7` and `4/7`, and asserts properties of that location. This computation does not appear in the manuscript proper, but the script (which the cover letter promises is supplementary material) treats it as central. The "fold" has no theorem about it in the paper. Either include a theorem about the fold or remove this content from the script.

**M4. The script's strict-decreasing assertion is wrong outside `(0, 1)`.** Lines 106–110 assert `sinc²(k/p)` is non-increasing for `k = 1, 2, …, 7` at `p = 7`, but `sinc²` is *not* monotone past `x = 1` — it has further sidelobe peaks. For `k ≥ p` the assertion happens to hold because `sinc²(k/p) = 0` at `k = p` and rises again afterwards. The script passes only because the assertion is `v ≤ prev + 1e-10` and `sinc²` happens to dip below the prior values numerically in this range. The proof tactic ("strictly decreasing on (0,1)") is a red herring for the corridor structure and should be removed or restated correctly.

**M5. "pairwise sinc² across distinct divisors" is the only place a squarefree hypothesis could matter, and the paper does not use it.** Suppose `b = 12 = 2² · 3`. The first `k` with `Z_k(b) ≠ ∅` is still `k = 2`; the smallest prime factor argument is unchanged. The theorem holds verbatim for non-squarefree `b` with `spf(b) = 2`. The remark on page 4 admits as much. So there is no genuine restriction to squarefree.

---

## §5 Minor comments

- Title is misleading: "Sinc² Zero Law" sounds like a statement about the analytic structure of `sinc²` (Fourier transform, harmonic measure, equidistribution). The actual statement is about divisibility.
- Two `\author` blocks with identical text but different addresses (lines 48–54 of the .tex). Compilation will produce a duplicate name in the masthead. Probably intended as a single author block with two affiliations.
- §5 calls equation (5) the "harmonic pre-echo function" — undefined term, no source, no proof of the limit. Either drop or substantiate.
- §1 cites Shannon (1949) and Montgomery (1973) as motivation, but the paper neither uses sampling theorems nor pair-correlation. These belong in a related-work paragraph in a longer paper, not as motivation in a 4-page note that does not engage with either.
- Bibliography has 4 entries; a *Integers* note with this little engagement with prior work should make do with the standard textbook citations rather than papers it does not actually use.
- The remark on `b = 15, k = 6` (lines 197–198) is meant to motivate why the squarefree hypothesis is needed but is incoherent: at `b = 15`, both `b` and `rad(b)` are squarefree. The remark accidentally argues the hypothesis is vacuous.

---

## §6 Literature missed

The "smallest prime factor of `b` is the first `k ≥ 1` with `gcd(k, b) > 1`" fact is so elementary it does not have a single canonical citation, but if the authors want one, they should consult:

- **Apostol**, *Introduction to Analytic Number Theory* (1976), §2.3. Standard treatment of the divisor / coprime structure of finite cyclic groups.
- **Tenenbaum**, *Introduction to Analytic and Probabilistic Number Theory* (3rd ed., 2015), §III.5 (sieve methods, inclusion-exclusion on divisors).
- **Iwaniec & Kowalski**, *Analytic Number Theory*, AMS Colloquium 53 (2004), §6 (Selberg's sieve uses essentially this fact).

The paper claims novelty in the `sinc²` formulation, but this exact reading appears in:

- **Pomerance**, "On the distribution of pseudoprimes," *Math. Comp.* 37 (1981), 587–593, and in the more pedagogical:
- **Erdős & Pomerance**, "On the largest prime factor of `n!`," *Acta Arithmetica* 1959–1990s — where ratios `k/p` and their integer character appear in elementary form.

The authors should also know:

- The closed-form value `sinc²(1/2) = 4/π²` is recorded as the first sidelobe amplitude of a rectangular window in **Oppenheim & Schafer**, *Discrete-Time Signal Processing* (any edition); this is not folklore worthy of a "boundary value" section in a mathematics paper.
- The `sinc²(x) = 1 − R₂(x)` relation cited via Montgomery is more standard in **Mehta**, *Random Matrices* (3rd ed., 2004), Chapter 6, but again: Montgomery's theorem is a quantitative correlation statement not invoked in this paper.

There is no overlap with Erdős 1959 or Pomerance 1984 in any deep sense — these papers concern entirely different sieve and arithmetic-function questions. The triviality concern raised here is independent of the literature; it is internal to the manuscript.

---

## §7 Estimated revision effort

There is no clear path to a publishable-in-*Integers* paper from this manuscript without genuine new content. Options the authors might pursue:

1. **Drop the squarefree note and write the discrete-Fejér / continuum-limit paper.** If equation (5) of §5 is a real theorem (uniform-in-`b` rate of convergence of `R(k, b)` to `sinc²(k/b)` along primes), state and prove it. This would be a different paper.
2. **Drop the standalone publication and merge with the cited "First-G companion."** If the two papers prove the same theorem, the appropriate venue is one paper, not two. The submitting authors can keep the `sinc²` viewpoint as a remark.
3. **Recast as a 1-page expository note for *Math. Mag.* or *Coll. Math. J.*.** The fact that "the first `k` with `sinc²(k/d) = 0` for some `d ∣ b` is `k = spf(b)`" is a nice exercise for a sophomore-level number-theory course. *Integers*, however, expects more.

Effort: option 1 is a major rewrite (months); option 2 is administrative; option 3 is straightforward (days).

---

## §8 Verdict — meets *Integers* bar?

**No.** *Integers* publishes short notes, but the bar is "novel, finite, elementary number-theoretic content with a runnable witness." This paper's central theorem reduces to "the smallest prime factor of `b` is the smallest `k ≥ 1` sharing a prime with `b`" — a fact that does not require a manuscript. The `sinc²` framing is decorative; the squarefree hypothesis is decorative; the verification script overlaps with the companion paper's script and tests properties (the "fold") not stated in the theorems.

The manuscript reads like an honest preprint expanded from a lecture note. With the clarity and self-disclaiming style intact, it would make a fine pedagogical note. As a research note for *Integers* it does not clear the bar.

**Recommend reject, with the suggestion that the authors either (a) develop the discrete-Fejér limit into a real theorem and resubmit, or (b) merge with the First-G companion paper.**
