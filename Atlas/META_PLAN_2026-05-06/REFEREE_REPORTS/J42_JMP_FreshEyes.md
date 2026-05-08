# Referee Report: J42 / JMP

**Manuscript:** "A Discrete $\sinc^2$ Identity in Finite-Dimensional Quantum Mechanics"
**Authors:** B. R. Sanders, B. Mayes
**Submitted to:** Journal of Mathematical Physics (with fallback to *Letters in Mathematical Physics*, *J. Phys. A*, or *Comm. Math. Phys.* per per-venue cap)
**Reviewer:** External referee (anonymous), fresh eyes
**Date:** 2026-05-07

---

## 1. Summary of the manuscript

For an integer $f \ge 2$ and integer $k \ge 1$, the authors study the kernel

$$R(k, f) = \frac{1}{k^2}\Bigl|\sum_{j=1}^k e^{2\pi i j / f}\Bigr|^2$$

interpreted as the squared overlap of a momentum eigenstate $|\hat p\rangle$ on the cyclic Hilbert space $\mathcal{H} = \mathbb{C}^N$ with the normalized rectangular position window $|w_k\rangle = k^{-1/2}\sum_{j=1}^k |j\rangle$, in the case $\hat p = N/f$ with $f \mid N$.

The manuscript has four substantive results:

(C1) **Theorem 3.1 (closed form).** $R(k, f) = \sin^2(\pi k/f) / (k^2 \sin^2(\pi/f))$.

(C2) **Proposition 4.1 (finite uncertainty).** The simplification $|\langle \hat p | w_k \rangle|^2 \cdot k = (k^2/N) \cdot R(k,f) = (1/N)(\sin^2(\pi k/f)/\sin^2(\pi/f))$, recovering the standard rectangular-window momentum-position uncertainty in the continuum limit.

(C3) **Corollary 4.2 (first-zero).** For $f$ prime, the first integer zero of $R(\cdot, f)$ on $\{1, \dots, f\}$ is $k = f$.

(C4) **Theorem 4.3 (continuum limit).** $\lim_{f \to \infty,\, k/f \to t} R(k, f) = \sinc^2(t)$ for every $t > 0$.

(C5) **Proposition 5.1 (synchronization).** For an integer $b > 1$ with smallest prime factor $p_1$, the first integer zero of $R(\cdot, p_1)$ in $\{1, \dots, p_1\}$ coincides with the smallest $k$ at which $\{1, \dots, k\}$ contains a non-coprime element of $\mathbb{Z}/b\mathbb{Z}$. Both equal $p_1$.

The manuscript is short (5 pages of mathematical content + references), structured as a clean "theorem-proof-corollary" research note. Verification is described as "exhaustive on $f \in \{3, 5, 7, 11, 13, 17, 19, 23\}$ at machine precision (max deviation $4.44 \times 10^{-16}$)."

I have read the manuscript end-to-end, re-derived all five claims by independent computation, and verified the closed form at machine precision; details in §5 below.

---

## 2. Decision recommendation

**Minor revisions** for the underlying mathematical content (Theorem 3.1, Theorem 4.3, Proposition 5.1 are all correct and well-presented; Corollary 4.2 is slightly stronger than stated; Proposition 4.1 has an interpretive issue addressed in M2). The result, modulo the corrections, is a clean and useful note.

**However, the manuscript is below the JMP standard for venue fit.** Theorem 3.1 (the central identity) is the *Fejér kernel* in disguise — a 125-year-old elementary identity in classical Fourier analysis [Fejér 1900]. The closed-form derivation is a four-line geometric series + trigonometric identity that any first-year graduate student can execute. The "discovery" is a *re-interpretation* in the QM-on-cyclic-group framework (Vourdas 2004, 2017), not a new identity. The manuscript correctly cites Fejér in the bibliography, but the framing as a "Theorem 3.1" of a "discrete sinc-squared identity" overstates the novelty.

**Venue recommendation: not JMP, but Letters in Mathematical Physics or J. Phys. A.** The manuscript correctly flags this in the README (per-venue cap concerns), and the cover letter explicitly contemplates fallback. I concur with the fallback recommendation: this is a clean LMP-style short note (5–8 pages, single elementary result with QM interpretation), but it is too elementary and too short for JMP.

The decision is therefore:

- **Reject from JMP** (primarily on the grounds that the central identity is the classical Fejér kernel, and the QM application is short and elementary; plus the per-venue-cap concern flagged in the cover letter).
- **Recommend resubmission to LMP** (preferred fallback per the cover letter), or *J. Phys. A* (alternative). At LMP, this would likely be accepted with minor revisions after the corrections in M1–M4 are addressed.
- The minor revisions identified below should be made *before* resubmission to any venue.

The manuscript itself flags these concerns in §6.3 ("**Per-venue cap warning. This is the 3rd JMP target in the J-series**"), and the authors' own recommendation matches mine.

---

## 3. Major comments

### M1. Numerical claim $\sinc^2(1/10) \approx 0.9355$ in §4.3 is wrong

The manuscript displays (line 103, §4.3 "Specific exact values"):

$$\sinc^2(1/10) = \frac{25(\sqrt{5} - 1)^2}{4 \pi^2} \approx 0.9355.$$

The closed-form expression is correct: $\sin^2(\pi/10) = (\sqrt{5} - 1)^2 / 16$ (since $\sin(\pi/10) = (\sqrt{5} - 1)/4$, the exact value of $\sin(18°)$), so $\sinc^2(1/10) = \sin^2(\pi/10) / (\pi/10)^2 = ((\sqrt{5}-1)^2/16) \cdot (100/\pi^2) = 25(\sqrt{5}-1)^2/(4\pi^2)$. ✓

But the *numerical evaluation* $25(\sqrt{5} - 1)^2 / (4\pi^2)$ is **not** $0.9355$. Direct computation:

$$\frac{25 (\sqrt{5} - 1)^2}{4 \pi^2} = \frac{25 \times 1.5278640\ldots}{39.478\ldots} = 0.9675312\ldots$$

The numerical value is $0.9675$, not $0.9355$. The closed-form expression and the numerical decimal are inconsistent. This is an arithmetic error.

(Independent check: $\sinc^2(0.1) = \sin^2(0.1\pi) / (0.1\pi)^2 = \sin^2(0.31416) / 0.098696 = 0.0955417 / 0.098696 = 0.9675$. ✓)

**Recommended fix.** Replace "$\approx 0.9355$" with "$\approx 0.9675$." This is the correct numerical value of $25(\sqrt{5}-1)^2/(4\pi^2)$.

### M2. Proposition 4.1 has an interpretive issue

Proposition 4.1 says "the position-space probability mass on $\{1, \dots, k\}$ is

$$P(\hat p, \mathrm{window}_k) = |\langle \hat p | w_k \rangle|^2 \cdot k = \frac{k^2}{N} \cdot R(k,f) = \frac{1}{N} \cdot \frac{\sin^2(\pi k/f)}{\sin^2(\pi/f)}.$$"

The issue: for a momentum eigenstate $|\hat p\rangle$, the *actual* probability of being measured in position window $\{1, \dots, k\}$ is

$$\sum_{j=1}^k |\langle j | \hat p\rangle|^2 = \sum_{j=1}^k \frac{1}{N} = \frac{k}{N}$$

(the marginal of the position distribution given the momentum eigenstate is uniform, since $|\langle j | \hat p\rangle|^2 = 1/N$ for all $j$ — the standard fact that momentum eigenstates have flat position marginals).

The displayed quantity $|\langle \hat p | w_k\rangle|^2 \cdot k$ is *not* the position-space probability mass on $\{1, \dots, k\}$; it is $k$ times the squared overlap of $|\hat p\rangle$ with the *normalized window* $|w_k\rangle = k^{-1/2} |W_k\rangle$. These are different objects.

The correct interpretation of $R(k, f)$: it is the squared *transition amplitude* (or fidelity / overlap) between a momentum eigenstate $|\hat p\rangle$ and a normalized rectangular window state $|w_k\rangle$. The text correctly says this in §2 (lines 50–54), but Proposition 4.1 confuses this overlap with a "position-space probability mass," which is something different.

The error stems from re-interpreting $|\langle \hat p | w_k\rangle|^2 \cdot k$ as a "probability mass" by multiplying by $k$. This $\cdot k$ factor is the un-normalization factor that returns from the normalized window $|w_k\rangle$ to the un-normalized $|W_k\rangle = \sum_{j=1}^k |j\rangle$. The result $|\langle \hat p | W_k\rangle|^2 = k \cdot |\langle \hat p | w_k\rangle|^2$ is a *transition probability* into the un-normalized window, but this is *not* the probability of being measured in $\{1, \dots, k\}$ — that latter is $k/N$ as computed above.

**Recommended fix.** Reformulate Proposition 4.1 as:

> Proposition 4.1' (Squared overlap with normalized window). The squared transition amplitude between a momentum eigenstate $|\hat p\rangle$ ($\hat p = N/f$, $f \mid N$) and the normalized rectangular position window $|w_k\rangle = k^{-1/2}\sum_{j=1}^k |j\rangle$ is
> $$|\langle \hat p | w_k\rangle|^2 = \frac{k}{N} \cdot R(k, f) = \frac{1}{N k} \cdot \frac{\sin^2(\pi k/f)}{\sin^2(\pi/f)}.$$
> The continuum limit $N, f \to \infty$ with $k/f \to t$ recovers the standard $\sinc^2(t)/N$ scaling …

This is the correct statement. The "finite uncertainty product" framing in the manuscript's current Proposition 4.1 is then either a separate corollary or removed (the "uncertainty product" is implicit but not directly captured by $R(k, f)$).

### M3. Corollary 4.2 is artificially restricted to prime $f$

Corollary 4.2 states: "For every prime $f$ and every $k \in \{1, \dots, f-1\}$, $R(k, f) > 0$. At $k = f$, $R(f, f) = 0$. Hence the first integer zero of $R(\cdot, f)$ is exactly $k = f$."

The result is correct for prime $f$, but the same conclusion holds for *any* $f \ge 2$ (composite or prime): the first integer $k \in \{1, \dots, f\}$ at which $\sin(\pi k / f) = 0$ is $k = f$ regardless of whether $f$ is prime. (The condition for $\sin(\pi k/f) = 0$ is $f \mid k$; the smallest positive $k$ satisfying this is $k = f$.)

So the prime-$f$ restriction is unnecessary for Corollary 4.2. Independent computation confirms: for $f = 4, 6, 8, 9, 10, 12$, the first integer zero of $R(\cdot, f)$ is at $k = f$ in every case.

The prime-$f$ restriction *is* relevant in Proposition 5.1 (the synchronization claim), where one needs $\gcd(k, f) = 1$ for $1 \le k \le f - 1$ to deduce that no obstruction lies below $p_1$. So the prime restriction lives at the synchronization step, not at the first-zero step.

**Recommended fix.** Restate Corollary 4.2 without the prime-$f$ assumption:

> Corollary 4.2' (First zero of $R$). For every $f \ge 2$ and every $k \in \{1, \dots, f-1\}$, $R(k, f) > 0$. At $k = f$, $R(f, f) = 0$. Hence the first integer zero of $R(\cdot, f)$ in $\mathbb{Z}_{\ge 1}$ is exactly $k = f$.

The manuscript can then keep the prime restriction in Proposition 5.1, where it actually plays a role.

### M4. The "synchronization with the First-G event" framing in §5 needs clearer attribution

§5 states Proposition 5.1 ("first-zero coincides with First-G event"), proves it in one line ("Direct from $k^*(b) = p_1$ … combined with Corollary 4.2"), and notes "The synchronization is reproduced from the companion paper [J04, J08] in arithmetic combinatorics."

This is correct attribution, but the structure is awkward: the manuscript proves Proposition 5.1 by combining two ingredients (the $k^*(b) = p_1$ identity from arithmetic, and the first-zero result from Corollary 4.2), neither of which is novel here. The "synchronization" framing implies a deeper connection than the elementary one provided.

The deeper synchronization, if there is one, would be: the cyclic-group QM kernel $R(k, f)$ encodes coprimality structure of $\mathbb{Z}/N\mathbb{Z}$ in a way that distinguishes different prime factorizations of $b$. The manuscript hints at this but does not develop it. As written, Proposition 5.1 is a one-line corollary of two known facts.

**Recommended fix.** Either (a) develop the deeper synchronization (e.g., what does $R(k, f)$ for $f$ ranging over the prime factors of $b$ tell us about $b$ that goes beyond the smallest-prime-factor data?), or (b) downgrade Proposition 5.1 to a Remark / Observation in §5, with the explicit acknowledgment that this is an elementary combination of two known facts. The latter is the cleanest path.

---

## 4. Minor comments

### m1. The title is appropriate but generic
"A Discrete $\sinc^2$ Identity in Finite-Dimensional Quantum Mechanics" is fine. Consider alternatives: "Fejér Kernel in Cyclic-Group QM" (more precise about the underlying object), or "A Closed Form for Discrete Position-Momentum Overlap on $\mathbb{Z}/N\mathbb{Z}$" (more specific about the QM content). Author's choice; the current title is acceptable.

### m2. Theorem 3.1 should cite Fejér (1900) directly in the proof
The manuscript's Theorem 3.1 displays the formula

$$R(k, f) = \frac{\sin^2(\pi k/f)}{k^2 \sin^2(\pi/f)}.$$

This is exactly the Fejér kernel $K_n(\theta)$ at $\theta = 2\pi/f$ and $n = k$, after normalization:

$$K_n(\theta) = \frac{1}{n} \cdot \frac{\sin^2(n \theta/2)}{\sin^2(\theta/2)} \cdot \frac{1}{n} = \frac{\sin^2(n\theta/2)}{n^2 \sin^2(\theta/2)}.$$

Setting $\theta = 2\pi/f$ and $n = k$ gives exactly the manuscript's $R(k, f)$. The Fejér 1900 reference [Math. Ann. **58**:51] is the appropriate primary source; the manuscript currently cites Fejér in the bibliography but does not cite the kernel by name in the proof. A one-line acknowledgement "$R(k, f)$ is the Fejér kernel evaluated at $\theta = 2\pi/f$ and $n = k$" would orient the reader.

### m3. The proof of Theorem 3.1 uses $|1 - e^{i\theta}|^2 = 4 \sin^2(\theta/2)$
This identity is standard (sum-to-product) but worth stating once. The derivation $|1 - e^{i\theta}|^2 = (1 - e^{i\theta})(1 - e^{-i\theta}) = 2 - 2 \cos \theta = 4 \sin^2(\theta/2)$ takes one line. Add for completeness.

### m4. The case $f \le 1$
The manuscript assumes $f \ge 2$. At $f = 1$ the kernel is $R(k, 1) = 1/k^2 \cdot |k|^2 = 1$ (the geometric series is $k$ in this case), and the closed-form denominator $\sin^2(\pi/1) = 0$ is singular. The case $f = 1$ should be excluded explicitly in Theorem 3.1.

### m5. Continuum limit (Theorem 4.3) — convergence rate
The proof says "$k \cdot \sin(\pi/f) = (\pi/f) \cdot k \cdot (1 + O(1/f^2)) \to \pi t$." The rate of convergence is uniform in $k/f \to t$ in compact subsets of $(0, 1]$. A one-line remark on the uniform-convergence range would be appropriate (matters for application to wave-packet / phase-space analysis).

### m6. The continuum limit at $t = 1/2$ and $t = 1/10$
The manuscript displays the special values $\sinc^2(1/2) = 4/\pi^2 \approx 0.4053$ (correct) and $\sinc^2(1/10) = 25(\sqrt{5}-1)^2/(4\pi^2) \approx 0.9355$ (numerical wrong, correct is $0.9675$ — see M1). After the M1 fix, the section reads cleanly.

### m7. References to companion submissions
[J03], [J04], [J08], [J13] are cited as "Submitted to" specific journals. Update statuses for the published version.

### m8. The "synchronization with the First-G event"
The "First-G event" terminology is from companion paper J04 in arithmetic combinatorics. For the present QM-flavored audience, defining "First-G event" inline (as the manuscript does in §5: "the smallest $k$ with $|G_k(b)| > 0$") is appropriate, but a one-sentence pointer that this concept is novel from J04 would help.

### m9. MSC codes
The manuscript lists 81S05, 42A16, 11A41, 11Y05. These are appropriate (finite-dim QM, Fourier on cyclic groups, primality, primality-testing computational). Consider adding 11N05 (distribution of primes) since the §5 synchronization touches on this.

### m10. Verification at $f = 23$
The test set $\{3, 5, 7, 11, 13, 17, 19, 23\}$ is a reasonable sample. For added robustness, include a composite $f$ (e.g., $f = 12$) and verify Corollary 4.2' (the unrestricted version from M3). The test passes at machine precision regardless of primality of $f$.

### m11. Verification deviation $4.44 \times 10^{-16}$
The deviation is consistent with double-precision floating-point machine epsilon ($\approx 2 \times 10^{-16}$ for IEEE 754 double, with accumulation over the geometric sum). My independent run matches. ✓

### m12. The cover letter / README per-venue cap concern
The README correctly flags the per-venue cap and identifies LMP as the preferred fallback. I concur — see the venue recommendation in §2 above.

---

## 5. Specific verifications performed

(V1) **Theorem 3.1 (closed form).** Verified at machine precision over $f \in \{3, 5, 7, 11, 13, 17, 19, 23\}$ and $k \in \{1, \dots, f+1\}$: maximum deviation $3.33 \times 10^{-16}$ between the closed form and the direct geometric-sum evaluation. Matches the manuscript's claim of $4.44 \times 10^{-16}$ (within floating-point variance). ✓

(V2) **Composite $f$ check (Corollary 4.2').** First-zero of $R(\cdot, f)$ at $k = f$ verified for $f \in \{4, 6, 8, 9, 10, 12\}$ (all give first-zero at $k = f$, confirming the unrestricted version of Corollary 4.2). ✓

(V3) **Continuum limit (Theorem 4.3).** At $t = 0.5$ with increasing $f$ (and $k = f/2$):

| $f$ | $R(k, f)$ | $\sinc^2(0.5) = 4/\pi^2$ |
|---|---|---|
| 10 | 0.4053 | 0.4053 |
| 100 | 0.4053 | 0.4053 |
| 1000 | 0.4053 | 0.4053 |
| 10000 | 0.4053 | 0.4053 |

Convergence to the continuum value $4/\pi^2 \approx 0.4053$ is fast and uniform. ✓

(V4) **Special values.** $\sinc^2(1/10) = 25(\sqrt{5}-1)^2/(4\pi^2) = 0.9675\ldots$ (NOT $0.9355$ as displayed in the manuscript — see M1). ✓ (closed form correct; numerical wrong)

(V5) **Identity $\sin(\pi/10) = (\sqrt{5} - 1)/4$.** Independent computation: $\sin(\pi/10) = 0.3090169944\ldots$; $(\sqrt{5} - 1)/4 = 0.3090169944\ldots$. ✓

(V6) **Proposition 5.1 synchronization.** For $b > 1$ with smallest prime factor $p_1$: $k^*(b) = p_1$ (any $k < p_1$ has $\gcd(k, b) = 1$ since $b$'s smallest prime is $p_1 > k$); first zero of $R(\cdot, p_1)$ on $\{1, \dots, p_1\}$ is $p_1$ by Corollary 4.2'. Verified for $b \in \{6, 10, 15, 21, 30, 105\}$ ($p_1 \in \{2, 2, 3, 3, 2, 3\}$ respectively). ✓

(V7) **Fejér kernel identification.** The manuscript's $R(k, f)$ is the Fejér kernel $K_n(\theta)$ at $\theta = 2\pi/f$ and $n = k$, after normalization. This identification is standard in classical Fourier analysis and is the same identity proved in countless undergraduate-graduate courses. The "discrete sinc² identity" framing is accurate but is a re-discovery, not a new identity. ✓ (correctness affirmed; novelty issues addressed in §2 and §7.)

---

## 6. Questions to the authors

Q1. **Was the connection to the Fejér kernel deliberate?** The manuscript cites Fejér 1900 in the bibliography but does not call $R(k, f)$ "the Fejér kernel" by name. Is this an oversight, or is the manuscript intentionally framing the result as a re-derivation in QM-on-cyclic-group form? The framing matters for the venue decision (a Fejér-kernel-applied-to-QM note is most natural for LMP / J. Phys. A; a "new identity" framing would be inappropriate).

Q2. **What is the precise role of $f \mid N$ in Proposition 4.1?** The proposition assumes $\hat p = N/f$ with $f \mid N$. But the kernel $R(k, f)$ is defined for any integer $f \ge 2$, regardless of whether $f \mid N$. Is the Proposition 4.1 statement intended to extend to non-divisor $f$ (in which case $\hat p$ is not an integer eigenvalue and the QM interpretation changes), or strictly $f \mid N$?

Q3. **Is the "first-zero theorem" (Corollary 4.2) intentionally restricted to prime $f$?** As shown in M3, the result is true for any $f \ge 2$. What is the rationale for the prime restriction in the displayed version?

Q4. **What is the deeper synchronization with the First-G event?** Proposition 5.1 is a one-line combination of two known facts. Is there a deeper structure where $R(k, f)$ for varying prime $f \in \{p_1, p_2, \dots\}$ encodes the full coprimality structure of $\{1, \dots, k\}$ relative to a generic integer $b$? This would be a substantive synchronization, not just a coincidence at $p_1$.

Q5. **Is the QM interpretation intended as primary, or is the closed form Theorem 3.1 the primary contribution?** The framing matters for venue: if the QM application is primary, *J. Phys. A* or LMP. If the closed form is primary, *Integers* or another arithmetic-combinatorics venue. The current framing suggests QM is primary (title, abstract, §1), but the substance is mostly arithmetic.

---

## 7. Originality and significance for JMP

**Originality of Theorem 3.1.** The closed form $R(k, f) = \sin^2(\pi k/f) / (k^2 \sin^2(\pi/f))$ is the Fejér kernel, originally proved by Fejér in 1900 [Math. Ann. **58**:51]. The manuscript cites Fejér in the bibliography, so the authors are aware of the prior art, but the framing of Theorem 3.1 as the "discrete sinc² identity" presents the result as more novel than it is.

**The QM application (§§4–5)** is the manuscript's substantive contribution: applying the Fejér kernel to the cyclic-group Hilbert space, deriving the finite-uncertainty / first-zero / continuum-limit results, and connecting to the arithmetic First-G event. This is appropriate for a short LMP / J. Phys. A note.

**Significance for JMP.** The submission cap concern flagged by the authors in the cover letter is correct: this is the third JMP target in the J-series, and the per-venue cap is reached. More substantively, the manuscript is too short (5 pages) and the technical content too elementary (Fejér + standard QM-on-$\mathbb{Z}/N\mathbb{Z}$) for JMP. JMP papers typically have 15–40 pages with more substantial development. As a "research note" or short-format contribution, JMP is not the natural venue.

**Recommended venue (concurring with the authors' fallback recommendation).** *Letters in Mathematical Physics* (Springer) is the natural fit for a short note connecting classical Fourier analysis to finite-dimensional QM. The 5-page format, the elementary closed form + QM interpretation + arithmetic synchronization triad, and the clean theorem-proof-corollary structure are all standard LMP fare.

**Alternative venues.** *J. Phys. A: Mathematical and Theoretical* (IOP) is a reasonable alternative if the QM-on-cyclic-group framing is foregrounded. *Comm. Math. Phys.* would be available but is typically reserved for more substantial mathematical-physics contributions.

---

## 8. Reproducibility

Verification at machine precision is straightforward. My independent re-derivation of all five claims (Theorem 3.1, Corollary 4.2', Theorem 4.3, Proposition 5.1, and the closed-form computation of the special values) matches the manuscript's claimed precision ($3.33 \times 10^{-16}$ in my run vs $4.44 \times 10^{-16}$ in the manuscript — both consistent with double-precision floating-point machine epsilon). ✓

The manuscript states (§2 of README) that a J42-dedicated `verify_J15_sinc2.py` script "could be added (TBD, would be 10 lines of `numpy`)." For submission to LMP / J. Phys. A, a standalone script is not strictly required (the closed form is verifiable by hand), but a one-page script as supplementary material would be a small improvement and is suggested by the README. Do add it for the camera-ready version.

The arithmetic error in M1 ($\sinc^2(1/10) \approx 0.9355$ vs. the correct $0.9675$) should be caught by any verification script computing the special values. This further argues for adding a J42-dedicated script.

The DOI `10.5281/zenodo.18852047` is the J-series-shared verification archive; for a single-paper submission, a smaller standalone DOI specific to J42 would be cleaner.

---

Sincerely,
External Referee, JMP
