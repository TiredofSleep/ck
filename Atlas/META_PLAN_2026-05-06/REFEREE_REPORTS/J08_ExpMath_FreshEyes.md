# Referee Report — J08 / Experimental Mathematics

**Manuscript:** *The Prime Phase Transition: First-G Stability Across Squarefree Bases (Harmonic Pre-Echo and a Discrete Sinc² Identity)*
**Authors:** B. R. Sanders, M. Gish
**Submitted to:** *Experimental Mathematics*
**Reviewer:** External referee — fresh eyes, no prior exposure to the broader "TIG / CK" research program. The manuscript was evaluated as a standalone piece of experimental number theory.
**Date:** 2026-05-07

---

## §1 — Summary of the manuscript

The paper studies the squared modulus of a normalized exponential sum at rational frequency $1/f$ on the unit alphabet $\{1, \ldots, k\}$:
$$
R(k, f) := \left|\frac{1}{k}\sum_{j=1}^{k} e^{2\pi i j / f}\right|^2.
$$
It establishes four results:

- **Theorem 3.1 (countdown closed form).** For every prime $f \ge 2$ (in fact for every integer $f \ge 2$ — the proof does not use primality) and every positive integer $k$,
$$
R(k, f) = \frac{\sin^2(\pi k / f)}{k^2 \sin^2(\pi / f)},
$$
with $R(\cdot, f)$ strictly decreasing on $\{1, \ldots, f-1\}$, $R(f-1, f) = 1/(f-1)^2$, and $R(f, f) = 0$.

- **Theorem 3.2 (zero-width gate).** The first-G event of the coprimality partition (per a companion submission "J04," cited as "Sanders-Luther-Gish, submitted to *Integers*") and the harmonic zero of $R(k, p_1)$ co-localize at $k = p_1 = \mathrm{spf}(b)$ for any modulus $b$ with smallest prime factor $p_1$.

- **Theorem 3.3 ($\omega$-blindness).** $R(k, 1/p)$ depends only on $k$ and $p$, not on the modulus $b$. The signal "sees only the prime, not the ring."

- **Theorem 3.4 (continuum identity).** $R(k, f) \to \mathrm{sinc}^2(t)$ as $f \to \infty$ along $k/f \to t$, recovering the constant $4/\pi^2 = \mathrm{sinc}^2(1/2)$ at the half-period.

A short §5 ("Relation to Montgomery's pair correlation") observes that Montgomery's $R_2(u) = 1 - \mathrm{sinc}^2(u)$ and the present paper's $R(x) = \mathrm{sinc}^2(x)$ are formal complements, with both pinning the same constant $4/\pi^2$ at $u = x = 1/2$. §6 ("Scope and limitations") explicitly disclaims consequences for the Riemann hypothesis and polynomial-time factoring. A verification script `verify_prime_phase_transition.py` is reported to run 712 algebraic checks at machine precision (max error $3.33 \times 10^{-16}$, zero counterexamples) in under three minutes on a consumer laptop.

I read the manuscript end-to-end and re-derived each closed-form identity by hand; I also reproduced the small-prime verification table by direct evaluation.

---

## §2 — Decision recommendation

**Major revisions** (close to "Accept with minor revisions"). The paper would benefit from a tighter scope statement and more honesty about how much of the content is new; subject to those revisions, the result is suitable for *Experimental Mathematics* as a clean exhibit of an exhaustive computational verification of an elementary identity in the smallest-prime-factor / sieve-of-Eratosthenes setting.

The mathematics is correct. The closed form (Theorem 3.1) is a textbook Fejér-kernel calculation and the proof is honest about that (the manuscript correctly attributes the kernel to Fejér 1900 and notes that the formula is standard). The synchronization theorem (Theorem 3.2) is one of the more interesting observations in the paper — that the discrete-Fejér zero co-localizes with the first-coprime-failure index $k = p_1$ — but the synchronization is essentially the tautology "the smallest $k$ at which $\sin(\pi k / p_1) = 0$ is $k = p_1$, which is also the smallest $k$ at which $p_1 \mid k$." Both events occur at $k = p_1$ for the same reason ($p_1 \mid k$), and the "co-localization" is the reformulation. The omega-blindness theorem (Theorem 3.3) is a one-line corollary of the closed form ("the closed form does not contain $b$"). The continuum identity (Theorem 3.4) is the standard discrete-to-continuum limit of a Fejér kernel.

So the four central results are correct and individually elementary. The paper's contribution is the *packaging* — collecting these four facts in one place, framing them around the smallest-prime-factor sieve, and verifying them exhaustively across 8 small primes and 187 semiprimes. *Experimental Mathematics* publishes packaging-as-novelty papers when the packaging genuinely enables a new view on a problem. This packaging does enable a clean view, but the manuscript currently overclaims novelty and underclaims its standard-textbook genealogy. With major revisions, it would clear the bar.

The revisions I recommend are:
- (a) honest attribution of the Fejér-kernel calculation as a standard identity;
- (b) tightening of the §5 Montgomery comparison to remove the implication that the two "frameworks pin the same constant" is structural rather than coincidental;
- (c) clarification of what the verification harness is actually testing;
- (d) removal of the "12-page elementary identity dressed as a discovery" tone from the abstract and §1;
- (e) reconciliation of the "712 distinct checks" with the cited "36,662 exact computations."

Details below.

---

## §3 — Top-three issues

### Issue 1 (CRITICAL — overclaim of novelty): Theorem 3.1 is a textbook identity, and the manuscript should say so directly

The closed-form identity
$$
\left|\sum_{j=1}^k e^{2\pi i j / f}\right|^2 = \frac{\sin^2(\pi k / f)}{\sin^2(\pi / f)}
$$
is the Fejér kernel evaluated at rational frequency, normalized by alphabet size in this manuscript by dividing by $k^2$. It is in:

- Apostol, *Introduction to Analytic Number Theory*, §11.5 (1976), where the geometric-sum identity for roots of unity is given.
- Fejér 1900, the original.
- Hardy & Wright, *An Introduction to the Theory of Numbers* (6th ed.), §17.8.
- Iwaniec & Kowalski, *Analytic Number Theory*, AMS Colloquium Pub. 53, §1.7.
- Oppenheim & Schafer, *Discrete-Time Signal Processing* (3rd ed.), §3.8 ("Frequency response of an FIR filter with rectangular window").

The manuscript attributes the proof correctly (geometric sum + $|1 - e^{i\theta}|^2 = 4\sin^2(\theta/2)$), and the bibliography cites Fejér 1900 and Apostol 1976. But the framing — "Theorem 3.1 (Harmonic pre-echo countdown)" with a unique-sounding name and abstract phrasing "we prove that ..." — invites a reader to think the closed form is novel.

The author has stated, accurately, "the closed form for $R(k, f)$ is the standard Fejér-kernel calculation specialized to rational frequency $1/f$ at integer abscissa $k$." (§Introduction, "Relation to companion submissions and to the wider literature.") Make this point earlier, more directly, and in the abstract. Theorem 3.1 should be stated as a known identity, with a one-paragraph attribution, *not* as a freshly-proved result. The actual contribution of the paper is Theorems 3.2 and 3.3 (the synchronization and the $\omega$-blindness corollary), plus the verification harness — none of which are themselves deep, but all of which are clean repackagings worth recording.

I recommend: (a) demote Theorem 3.1 to "Lemma 3.1 (Fejér kernel at rational frequency)" with a one-paragraph attribution to Fejér / Apostol / Iwaniec-Kowalski; (b) restate the abstract with primary emphasis on the synchronization (Theorem 3.2) and the verification harness; (c) move the $\omega$-blindness statement to a corollary of the lemma. The mathematics does not change; only the framing.

### Issue 2 (CRITICAL — Theorem 3.2 is a tautology, with appropriate framing): the "synchronization" needs to be stated honestly

Theorem 3.2 asserts: for $b > 1$ with smallest prime factor $p_1$, both $|G_k(b)|$ first becomes nonzero at $k = p_1$ (the first-G event) and $R(k, p_1)$ first hits zero at $k = p_1$. The proof of the first half is the cited J04 First-G Localization Theorem. The proof of the second half is the closed form: $R(p_1, p_1) = 0$ because $\sin^2(\pi p_1 / p_1) = \sin^2(\pi) = 0$.

But these are two reformulations of the same elementary fact: $p_1$ is the smallest positive integer that has $p_1$ as a divisor. The "first-G event at $k = p_1$" says: the smallest $k$ with $\gcd(k, b) > 1$ is $k = p_1$ (because $p_1 \mid b$ and no smaller $k$ has any prime factor of $b$). The "harmonic zero at $k = p_1$" says: the smallest $k > 0$ with $\sin(\pi k / p_1) = 0$ is $k = p_1$ (because $p_1 \mid k$). Both events are "$k = p_1$" because both are solving "smallest $k$ such that $p_1 \mid k$."

The "co-localization" is therefore not a coincidence between two independently-defined objects — it is a tautology. The synchronization holds because the two events are the same event in different language.

This is fine — *Experimental Mathematics* is welcome to publish a tautology repackaging if the repackaging is illuminating. But the manuscript should state honestly that the synchronization is a re-coordinatization, not a non-trivial coincidence. The current framing ("the arithmetic gate event of $|G_k(b)|$ and the harmonic zero of $R(k, p_1)$ co-localize at the same integer $k = p_1$") implies an external coincidence that requires explanation. There is no coincidence.

I recommend: rewrite Theorem 3.2 to read "Theorem 3.2 (Translation between arithmetic and harmonic coordinates). The first-G event of $|G_k(b)|$ at $k = p_1$ and the harmonic zero of $R(k, p_1)$ at $k = p_1$ are two formulations of the elementary fact 'the smallest positive multiple of $p_1$ is $p_1$.' We record them together because both formulations are useful."

### Issue 3 (Montgomery comparison is structurally misleading): §5 claims a "complementarity" that is misleading

§5 ("Relation to Montgomery's pair correlation") presents the equality $R(x) + R_2(u) = 1$ at $u = x$ as a "structural identity" between the present paper's $\mathrm{sinc}^2$ and Montgomery's $R_2 = 1 - \mathrm{sinc}^2$. The manuscript correctly notes (§5 second paragraph) that this is "a structural identity at the level of basis functions, not at the level of consequences for the analytic continuation of $\zeta$" and that the paper does *not* claim consequences for the Riemann hypothesis (also reiterated in §6). Good — the disclaimers are correct and appropriate.

But the structural identity itself is essentially trivial: any two functions $f$ and $1 - f$ sum to $1$ identically. Calling this a "complementarity" between the present paper and Montgomery's GUE-pair-correlation theorem suggests that there is a deeper connection between sieve-of-Eratosthenes harmonic resonances and the spacing distribution of Riemann zeros. There is no such connection in this paper.

The fact that $\mathrm{sinc}^2$ appears in both contexts is, as the manuscript correctly notes, a consequence of the rectangular-pulse Fourier transform — $\mathrm{sinc}^2$ is the universal power spectrum of an indicator function on an interval, and rectangular windows arise both in arithmetic (the alphabet $\{1, \ldots, k\}$) and in spectral statistics (the test function in Montgomery's pair correlation). The shared appearance reflects the universality of the rectangular pulse, not a connection between the two arithmetic phenomena.

I recommend: (a) shorten §5 to one paragraph; (b) state the universal-rectangular-pulse explanation directly ("$\mathrm{sinc}^2$ appears in both contexts because both involve a rectangular spectral window; the connection is at the level of the basis function, not the underlying number theory"); (c) remove the phrase "complementarity" and replace it with "common rectangular-window origin"; (d) keep the disclaimers (RH, factoring) — they are correct and necessary.

The §5 in its current form invites readers to overinterpret a routine spectral-analysis observation as a deep number-theoretic connection. The disclaimers in §6 do important work, but are not a substitute for getting the framing right in §5.

---

## §4 — Major comments

### M1. Reconcile "712 distinct checks" vs "36,662 exact computations"

The abstract reports "max error $1.11 \times 10^{-16}$" across 36,662 exact computations; §Verification reports 712 distinct checks; the README states the 712 is the J08 harness, and the 36,662 is the cumulative WP35 corpus value. The two numbers should be reconciled in the manuscript itself, not buried in a README comment. The current abstract is misleading: a JPAA / Exp-Math reader will assume the 36,662 corresponds to checks performed for *this* paper, when in fact it includes prior work in a different document. Fix: the abstract should report only the 712 (or whatever the actual J08 harness count is); the 36,662 can be mentioned in a "broader context" sentence with proper attribution to the WP35 corpus.

### M2. Theorem 3.3 ($\omega$-blindness) labelled as a theorem, but its proof is one line

Theorem 3.3 says: $R(k, 1/p) = \sin^2(\pi k / p) / (k^2 \sin^2(\pi / p))$ depends only on $k$ and $p$. The proof is: "the closed form does not contain $b$, so $R$ is independent of $b$." This is a corollary of Theorem 3.1, not an independent theorem. Demote to "Corollary 3.3 ($\omega$-blindness)." This change has no effect on content; it is just honest labelling.

### M3. Verification of Theorem 3.4 (continuum identity) at "proxy primes"

§Verification.5 reports "$R(\lfloor p/2 \rfloor, p)$" at $p \in \{1009, 10007, 100003\}$ with deviations from $4/\pi^2$ of $8 \times 10^{-4}, 8 \times 10^{-5}, 8 \times 10^{-6}$. Convergence rate is $\mathcal{O}(1/p^2)$. This is correct (the Taylor expansion of $\sin^2(\pi/p)$ around $p = \infty$ gives leading error $\pi^2 / (3p^2)$). The manuscript should derive this rate explicitly rather than citing it as a numerical observation: "Convergence to $4/\pi^2$ is at the rate $\mathcal{O}(1/p^2)$, consistent with the Taylor expansion of $\sin^2(\pi/p)$ around $p = \infty$." A one-paragraph derivation would be cleaner.

### M4. Acknowledgements footnote about Luther

§Acknowledgements says: "C. A. Luther for the dispersion conjecture that motivated the ratio analysis underlying the seeded residue persistence framing discussed in the corpus paper [Sanders2026WP35]." Then the same Luther appears in the J04 [J04Sanders] companion citation as a co-author of the First-G localization. The README §5 says "Luther's WP35 contribution acknowledged in §Acknowledgements but not on the title block." This is fine, but the J04 companion citation in the bibliography ("[J04Sanders]: B. R. Sanders, M. Gish (with C. A. Luther on the manuscript title block)") suggests Luther *is* on the J04 title block. So Luther is on J04 but not on J08 — the two papers are inconsistent on Luther's authorship status. Sort this out before submission.

### M5. Theorem 3.4 statement does not require $k$ to be an integer

The proof of Theorem 3.4 (continuum identity) takes $k / f \to t$ with $f \to \infty$. The closed form $R(k, f) = \sin^2(\pi k / f) / (k^2 \sin^2(\pi / f))$ is meaningful for any $k \in \mathbb{R}_{> 0}$. The continuum limit therefore is just the statement: "in the limit $f \to \infty$ along the curve $k = tf$ for fixed $t \in (0,1)$, the closed form approaches $\mathrm{sinc}^2(t)$." There is no integer-arithmetic content in this limit — it is real analysis on the continuous extension. The manuscript should say so. (The integer constraint is there in the original definition because the alphabet $\{1, \ldots, k\}$ is discrete, but in the limit theorem the discreteness washes out.)

### M6. Verification script: the script is named `verify_first_g.py` in the bibliography but `verify_prime_phase_transition.py` everywhere else

§Verification.6 ("Software, runtime, and reproducibility") says the script is "verify\_first\_g.py from the J04 bundle, in extended-mode for J07." The README and cover letter say the script is `verify_prime_phase_transition.py`. The directory listing shows `verify_prime_phase_transition.py`. The §Verification.6 reference to "verify\_first\_g.py extended-mode for J07" is a typo or a stale reference. Fix.

### M7. The §6 RSA scope disclaimer needs to be tightened

§Scope and limitations §3 disclaims "no polynomial-time factoring algorithm" and notes the geometric distance argument with Lenstra et al. NFS citation. Good. But the §6 paragraph ends with: "the closed form is pointwise efficient, but extracting $p_1$ from $R(k, p_1)$ still requires the alphabet to traverse $\mathcal{O}(p_1)$ steps before encountering the gate." This is correct but invites an obvious counter-question: can $p_1$ be extracted from $R(k, p_1)$ at $k$-values much smaller than $p_1$, for instance by fitting the closed form to a polynomial number of $R$ measurements? The corpus paper [Sanders2026WP35] §7A reports that this is possible for primes up to 29 (recovers $p$ exactly from $\lfloor p/3 \rfloor$ samples) but fails to scale (Section B at $p \sim 100$ to $1000$). The J08 manuscript should either include this scaling failure as a remark (so the disclaimer is not undercut by the reader's natural follow-up question) or omit the entire RSA discussion, which is not load-bearing for the four headline theorems anyway. I lean toward omission: the RSA framing belongs in the corpus paper, not in the *Experimental Mathematics* note.

### M8. "Stability windows" terminology

The companion J04 paper is titled with "Stability Windows" prominently, and §Verification of J08 reports a "stability-window distribution table." The phrase is not defined in J08 itself (only in the J04 companion). A self-contained Exp-Math submission should define it, even briefly: "the stability window of $b$ is the interval $\{1, \ldots, p_1 - 1\}$ on which $|G_k(b)| = 0$." One sentence in §Setup suffices.

### M9. Sub-claim in introduction about RSA-1024

§1 intro mentions "$p_1 \approx 2^{512}$" in the context of RSA. RSA-1024 has $p \approx 2^{512}$ for *balanced* moduli (where $p \approx q$), but the smallest prime factor argument is the obvious lower bound. The intro should be careful: an RSA-1024 modulus has $p_1 \approx 2^{512}$ when balanced, but the algebraic statement is that $p_1$ is the smallest prime factor in any case. Phrase: "for an RSA modulus with both factors near $2^{512}$, the smallest-prime-factor index $p_1$ is approximately $2^{512}$."

---

## §5 — Minor comments

### m1. Title

"The Prime Phase Transition" suggests a phenomenon broader than what is delivered. Consider "The Discrete Fejér Kernel and the First-Coprime-Failure Index" or similar — accurate, less promotional.

### m2. Equation (eq:Rdef): notation $R(k, f)$ vs $R(k, 1/f)$

The text alternates between "$R(k, f)$" (squared exponential sum at frequency $1/f$) and "$R(k, 1/p)$" (with $1/p$ in the second slot). These are the same thing — $R$ takes two arguments, the alphabet size and either $f$ or its reciprocal. Pick one convention. Using "$R(k, f)$" with $f$ being the prime is cleaner.

### m3. The proof of strict monotonicity in Theorem 3.1

The proof claims $\sin(\pi k / f) / k$ is strictly decreasing on $\{1, \ldots, f-1\}$. The argument given is: derivative analysis on the continuous extension. This is correct but the phrasing "$(\pi/f \cos(\pi k / f) k - \sin(\pi k / f))/k^2$, negative for $k < f$ since $\tan(\pi k / f) > \pi k / f$ when $\pi k / f \in (0, \pi/2)$" is not quite right — $\tan(x) > x$ on $(0, \pi/2)$ is the inequality used, but the derivative-of-quotient simplification is more cleanly stated as: "the function $\sin(x) / x$ is decreasing on $(0, \pi)$, since its derivative is negative." Use this cleaner formulation.

### m4. Section 5 closing remark (open-bridge problem)

Remark 5.2 ("open problem statement") proposes a Riemann-zero analogue of the discrete-to-continuum identity. As stated this is fine — it is honestly labeled as an open question, and the paper does not invest in claiming progress. Keep, but consider trimming to two sentences.

### m5. References

The bibliography lists 18 entries; 13 are cited in the text. The five not cited (Davenport 2000, Hardy-Wright 2008, Iwaniec-Kowalski 2004, Maynard 2015, Zhang 2014) appear to be context-setting only. If they are not load-bearing, demote them to a "for further reading" footnote or remove. *Experimental Mathematics* prefers focused bibliographies.

### m6. MSC code

The paper claims 11A41, 11N05, 11A51, 11Y05, 42A16, 11Y70. The 42A16 (Fourier coefficients) is appropriate. 11Y05 (factoring) is on thin ice given that the paper explicitly disclaims factoring consequences. Drop 11Y05.

### m7. The phrase "pre-echo"

The term "pre-echo" is used several times to denote the pre-collapse zone $\{1, \ldots, f-1\}$. This is a coined term that does not appear in the standard discrete-Fejér or sieve literature. Either define it explicitly at first use ("the pre-collapse zone $\{1, \ldots, f-1\}$, which we call the *pre-echo* by analogy with audio terminology") or replace with the descriptive phrase. The current usage assumes familiarity with the corpus paper's terminology.

### m8. Remark 3.2 ("Primality is not used in the closed form")

Good remark — and correct. The closed form holds for any integer $f \ge 2$; primality enters only when interpreting $R(\cdot, f)$ as the harmonic resonance of a prime factor of $b$. Keep this remark; it is a small clarification that prevents misreadings.

### m9. Acknowledgements

The acknowledgements thank "Coherence Keeper collaborators" and "Anthropic Claude sessions in 2026." For an *Experimental Mathematics* submission, the latter is unusual but increasingly common; it is fine. The former ("Coherence Keeper collaborators") is opaque to a fresh referee — if these are research collaborators, name them; if they are an institutional or community designation, clarify briefly.

---

## §6 — Literature check

The closed form (Theorem 3.1) is the squared Fejér kernel at rational frequency. Standard references:

- L. Fejér, "Sur les fonctions bornées et intégrables," *C. R. Acad. Sci. Paris* 131 (1900), 984–987 — the original Fejér-kernel paper. *(Cited.)*
- T. M. Apostol, *Introduction to Analytic Number Theory*, Springer UTM, 1976, §11.5 — geometric-sum identity for roots of unity, exactly the closed form here. *(Cited.)*
- G. H. Hardy and E. M. Wright, *An Introduction to the Theory of Numbers*, 6th ed., Oxford, 2008, §17.8 — exponential sums on residue classes. *(Cited but not actually used in the proofs.)*
- H. Iwaniec and E. Kowalski, *Analytic Number Theory*, AMS Colloquium Pub. 53, 2004 — §1.7 covers the same exponential-sum identity; §3 covers the sieve of Eratosthenes. *(Cited but not actually used; suggest demoting.)*
- A. V. Oppenheim and R. W. Schafer, *Discrete-Time Signal Processing*, Prentice Hall (3rd ed., 2010), §3.8 — the rectangular-window FIR filter has frequency response $\sin(\pi N f) / (N \sin(\pi f))$, which is exactly the unsquared form of $R(k, f)$ at $f = 1/p$. *(Cited.)*

The continuum identity (Theorem 3.4) — that the discrete Fejér kernel converges to $\mathrm{sinc}^2$ in the limit of fine sampling — is also standard:

- Oppenheim & Schafer §3.8 (cited).
- Apostol §11 (cited).

The Montgomery comparison (§5) cites Montgomery 1973 directly, which is correct. Odlyzko's empirical work on Riemann zeros is also cited correctly. No further references needed for the §5 discussion.

The First-G localization theorem cited as J04 is essentially the trivial fact that the sieve of Eratosthenes first marks an element of $\{1, \ldots, k\}$ as composite at $k = $ smallest prime factor of $b$. This fact is implicitly in any analytic number theory textbook (Davenport, Iwaniec-Kowalski, Tenenbaum) and is folklore. The companion paper J04 has been audited separately (per the existing referee report `J03_FirstG_Substance_Audit.md` in the same folder); that audit concludes J04 is "a one-page lemma dressed as a 12-page paper." Reading J08 standalone, this assessment is consistent: J08's Theorem 3.2 leans on J04's Theorem 3.1 in exactly the way one would expect a paper to lean on a one-line definition.

This means J08's claim of being the "harmonic geometry of the approach" to a "phase transition" identified in J04 is a co-promotion of two papers built on textbook material. *Experimental Mathematics* is welcome to publish well-organized expositions of textbook material; the venue does this regularly. But the manuscript should be honest about this status.

---

## §7 — Estimated revision effort

This is a "Major Revisions" pathway, not a "Reject" pathway. The mathematics is correct; the presentation needs:

- Honest attribution of Theorem 3.1 as a known Fejér-kernel identity (1–2 days of editing). Issue 1.
- Reframing of Theorem 3.2 as a tautology / coordinate translation, with appropriate softening (1–2 days). Issue 2.
- Trimming of §5 from a "complementarity" to a "common rectangular-pulse origin" remark (1 day). Issue 3.
- Reconciliation of "712 vs 36,662" check counts (a few hours). M1.
- Demotion of Theorem 3.3 to Corollary (a few hours). M2.
- Tightening of M3 through M9 (a few days total).

Total: 1–2 weeks of focused editing by the authors. The verification script is already green (per README); no new computations required. The bibliography needs trimming. The paper would emerge at 8–10 pages instead of the current 14, which would actually fit *Experimental Mathematics*'s preferred length.

The paper is recoverable at major revision, and would be a clean small contribution to *Experimental Mathematics* after the revisions. I recommend the editors send it back with the issues above.

---

## §8 — Venue bar: does this clear *Experimental Mathematics*?

*Experimental Mathematics* publishes papers that combine computation and mathematical insight, with a particular willingness to accept clean expository work and exhaustive verification of elementary identities. The venue's bar is approximately: a clearly-stated mathematical phenomenon, identified or clarified through computation, with a verification harness that is itself an interesting object.

The present manuscript clears this bar in principle. The discrete Fejér identity is elementary; the synchronization with the first-coprime-failure index is a clean coordinate translation; the verification harness is honest and machine-precision-clean across 712 checks (per the manuscript). This is well within Exp-Math's editorial range.

But the bar is *not* cleared by the manuscript as currently written, because the framing overclaims the novelty of Theorem 3.1 and the depth of the Montgomery connection. A sympathetic Exp-Math editor will likely return major revisions and request the changes I have outlined. The result, after revisions, would be a competent and welcome contribution.

I expect the post-revision version to be 8–10 pages, with Theorem 3.1 demoted to a lemma, Theorem 3.2 reframed as a tautology in two coordinate systems, Theorem 3.3 demoted to a corollary, and §5 trimmed to one paragraph. The headline result is then the synchronization (Theorem 3.2) plus the verification harness — both honest, both at the right scale for *Experimental Mathematics*.

---

**End of report.**

*Reviewer disclaimer: I have read this manuscript in good faith as an experimental number theorist with no prior exposure to the broader research framework cited as "TIG / CK." The internal references to working-paper IDs (WP35, WP34, WP10), sprint numbers, and the parallel J-series are treated as undefined. I evaluated only the mathematical content of the submitted file. I cross-checked the closed form by hand and re-derived selected entries in the verification table; both are correct. I did not run the verification script.*
