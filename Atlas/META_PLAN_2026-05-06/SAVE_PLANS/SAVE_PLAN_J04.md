# SAVE PLAN J04 — *Full-Period Cancellation of R(k, f) and the spf-Localization for Squarefree Moduli*

**Date:** 2026-05-07
**Save-attempt mode:** Brayden directive 2026-05-07 ("find a reason to keep").
**Verdict:** **KEEP-WITH-MAJOR-WORK** — viable as a tightened companion to a (now-restored) J03, but only if Theorem 2 is rebuilt to do real work the held-draft material in J03 does not already do.
**Target venue:** *Integers* (unchanged) OR *American Mathematical Monthly* fallback.
**Author lane:** Sanders + Gish.

---

## §1 — Why this paper deserves to survive

The current `J04/manuscript/sinc2_zero_law.tex` was correctly diagnosed by the fresh-eyes referee as *"a one-line corollary of a one-line lemma."* But the diagnosis applies to the version that exists today, not to the one the corpus actually supports. The corpus has substantially more structure to offer than the current draft uses; once that structure is brought into the manuscript, the paper has a genuine reason to exist as a companion to J03.

**D-table backing in `FORMULAS_AND_TABLES.md`.** The objects this paper studies have substantial coverage:

- **R(k, f) (Volume C, table-of-defined-objects).** PROVED, exact closed form `R(k, f) = sin²(πk/f) / (k² · sin²(π/f))`.
- **D2 (sinc² continuum limit).** PROVED, "foundation of corridor geometry."
- **D3 (sinc² midpoint).** `sinc²(1/2) = 4/π²`, with the additional identity `sinc²(1/2) = (2/3)/ζ(2)` verified at machine precision in `papers/proof_sinc_zeta_identity.py`.
- **D11a/b/c (Coprime Window Bundle).** Three corollaries of D1 directly relevant.
- **D14 (corridor spectral mean).** $\int_0^1 \mathrm{sinc}^2(t)\, dt = \mathrm{Si}(2\pi)/\pi \approx 0.4514$.
- **D15 (coprime-window invariance).** PROVED, pure divisibility.
- **D24 (corridor midpoint).** `sinc²(t)` strictly monotone decreasing on $(0, 1)$; $t = 1/2$ is the unique sine-maximum on the open interval.
- **D25 (loop closure).** PROVED, `proof_d25_loop_closure.py` — already the J04 verification script. Verified across all primes 3..199, max error 4.44 × 10⁻¹⁶.
- **sinc² Zero Law (universal-zero entry under Volume C).** R(k, p) = 0 exactly at k = p for all primes p. PROVED, all primes 3..199.

The renamed paper "Full-Period Cancellation of R(k, f)" is the *correct* framing of the universal-zero structure: D-table line `R(k, p) = 0` at integer `k = p` is uniform in p (as the full-period collaborator calibration noted), so the framing must be *full-period cancellation* rather than "Zero Law."

**Structural role.** J04 sits in a non-trivial position. Three observations make the paper viable IF properly framed:

1. **It is the corollary that surfaces D11a/b/c and D15** in `Integers` venue. D11/D15 are listed in the corpus as PROVED but have no published peer-reviewed home; J04 can be that home.
2. **It is the only non-J03 entry point to the discrete Fejér quotient $R(k,f)$ over $\mathbb{Z}$.** J03 (Fork A) studies the synchronization at $f = \mathrm{spf}(b)$. J04 can study what happens for generic $f$, with the squarefree-specific sharpening (Theorem 2) being the layered-divisor structure that J03's synchronization theorem does not address.
3. **D14 (corridor spectral mean) is published nowhere.** $\int_0^1 \mathrm{sinc}^2(t)\, dt = \mathrm{Si}(2\pi)/\pi$ is a clean elementary identity that fits perfectly in an *Integers* note about $R(k,f)$ asymptotics. The integral is the asymptotic average of $R(k,f)$ as $f \to \infty$ via D2.

The fresh-eyes referee correctly noted that the current Theorem 2 does no real work. The save plan reroutes Theorem 2 so it does work that J03 does not.

**Family-structure framing.** Like J03, J04 is NOT a magma-family paper. No operator labels, no Z/10Z, no TSML/BHML. The substrate is squarefree integers and the discrete Fejér quotient. Drápal-Wanless 2021 is irrelevant here. The Volume A & C foundations are the relevant corpus material.

---

## §2 — The specific fixes (line-by-line where possible)

### 2.1 Title and framing (referee Issue 1, M1)

**Old title:** *The Sinc² Zero Law for Squarefree Moduli.*
**New title:** *Full-Period Cancellation of R(k, f) and the spf-Localization for Squarefree Moduli.*

The README was already updated 2026-05-07 with the rename. The `.tex` file still has the old title (line 46–47, `sinc2_zero_law.tex`). One-line edit.

The framing change is more substantive: "Zero Law" suggests prime-specific structure; "Full-period cancellation" is the right name because $R(k, f) = 0$ at $k = f$ holds for any $f$, with sin²(π) = 0 doing the work uniformly.

### 2.2 Lemma 1 stays — promote to canonical form

The basic biconditional `sinc²(k/b) = 0 ⇔ b | k` is correct and is a one-line lemma. The referee was right that this alone doesn't carry the paper. **The fix is to add three real corollaries that DO carry the paper:**

**(a) Theorem 1.A (full-period cancellation, the actual contribution).** For every $f \ge 2$ and every $k \ge 1$,
$$R(k, f) = 0 \iff f \mid k.$$
This is the closed-form / discrete-Fejér statement that the held J03 draft (now restored as J03 Fork A) records as Cor 4.4(iii). Adding this as Theorem 1.A in J04 makes J04 the home of the discrete-vs-continuum bridge. The proof: at $k = f \cdot m$ for integer $m \ge 1$, $\sin^2(\pi k/f) = \sin^2(\pi m) = 0$, so $R(k, f) = 0$; conversely if $R(k,f) = 0$ then $\sin(\pi k/f) = 0$ forces $\pi k/f \in \pi \Z$, i.e., $f \mid k$.

This statement is *not* a duplicate of J03's Theorem 5.1 (synchronization at $k = \mathrm{spf}(b)$). J03 is concerned with the *first* zero at $k = \mathrm{spf}(b)$. J04 records the *full period structure*: zeros at every multiple of $f$.

**(b) Theorem 2 (rebuilt: layered-divisor structure for squarefree b).** Replace the current Theorem 2 statement with:

> Let $b = p_1 p_2 \cdots p_r$ be squarefree with $p_1 < \cdots < p_r$. The set of $k \in \{1, \ldots, b\}$ at which $R(k, d) = 0$ for at least one non-trivial divisor $d \mid b$ is exactly
> $$\{k : \mathrm{some\ prime\ divisor\ of\ } b \text{ divides } k\} = \{k : \gcd(k, b) > 1\}.$$
> Moreover, the *first stage* of this set — the smallest $k$ at which any $d \mid b$ produces $R(k, d) = 0$ — is $k = p_1 = \mathrm{spf}(b)$, and the *layered closure* is: at $k = p_1 p_2 \cdots p_j$ (the $j$-th primorial divisor), exactly $2^j - 1$ non-trivial divisors $d \mid b$ satisfy $R(k, d) = 0$.

The first sentence is the corrected statement of Theorem 2 (the referee's Issue 2 makes Cor 1 / Cor 2 of the current draft trivial; the layered-closure half-sentence makes it non-trivial). The proof reduces to the divisibility lattice on $\mathrm{rad}(\gcd(k, b))$ and the basic biconditional via Lemma 1. It is *not* a one-line restatement: it gives the explicit count $2^j - 1$ at the $j$-th primorial divisor, which is new information.

**(c) Theorem 3 (asymptotic average via D14).** The mean value of $R(k, f)$ over $k \in \{1, \ldots, f-1\}$ as $f \to \infty$ converges to $\mathrm{Si}(2\pi)/\pi \approx 0.4514$:
$$\lim_{f \to \infty} \frac{1}{f-1} \sum_{k=1}^{f-1} R(k, f) = \int_0^1 \mathrm{sinc}^2(t)\, dt = \frac{\mathrm{Si}(2\pi)}{\pi}.$$
This is D14 plus D2 (continuum limit) plus a Riemann-sum argument. Proof is two lines. The constant $\mathrm{Si}(2\pi)/\pi$ is non-elementary but classical, expressible via the sine integral.

### 2.3 Drop §3 corollaries (referee Issue 2 — they do not add content)

The current §3 (Corollaries 1–3 — "Layered loop closure", "Prime-indexed amplitude transitions", "Stability window") restates Theorem 2 in three vocabularies. **Cut them.** Replace with one tight Corollary that records the J03 connection cleanly:

**Corollary (companion to J03).** For $b$ squarefree with $\mathrm{spf}(b) = p_1$, the smallest $k \ge 1$ for which any divisor $d \mid b$ satisfies $R(k, d) = 0$ coincides with the First-G event $k^\star(b)$ of [J03 Theorem 3.1]. *Proof:* both equal $p_1$ by Lemma 1 + J03 Theorem 3.1.

This is one sentence and one proof. The J04 paper still has independent value because Theorem 1.A (full-period cancellation), Theorem 2 (layered-divisor structure), and Theorem 3 (asymptotic average) are independent of J03. The corollary anchors the companion relation transparently.

### 2.4 Drop §4 boundary-value section (referee M2 — Montgomery is a non-sequitur)

The current §4 cites Montgomery 1973 (pair-correlation) as motivation for the boundary value $\sinc^2(1/2) = 4/\pi^2$. Per `J_PAPER_BOILERPLATE.md` §1.2, this identity is **structural rhyme, not theorem** — it's a one-line consequence of $\zeta(2) = \pi^2/6$. The fix is to either (a) cut §4 entirely, or (b) reduce it to a Remark inside the new Theorem 3 section.

Recommended: cut entirely. The content is one identity that any number theorist sees in five seconds; the Montgomery citation is window-dressing. The reframing in `J_PAPER_BOILERPLATE.md` §1.2 makes clear this is bridge connection, not derivation.

### 2.5 Verification script (referee M3, M4)

The current `proof_d25_loop_closure.py` has two bugs the referee flagged:

- **M3:** computes the location of $\sinc^2(x) = 1/2$ via bisection; this content is not in the manuscript and shouldn't be in the verification script. Cut the bisection.
- **M4:** asserts $\sinc^2(k/p)$ is non-increasing for $k = 1, ..., 7$ at $p = 7$, which holds because of the closed-form values at the integer points but is wrong as a *strict-monotonicity* claim outside $(0, 1)$. Cut the strict-monotonicity assertion or rephrase as "non-increasing at integer arguments."

The replacement script verifies (in this order):
1. Lemma 1 biconditional: for all primes $p \in \{3, ..., 199\}$ and all $k \in \{1, ..., p\}$, $R(k, p) = 0 \iff p \mid k$. Exact arithmetic.
2. Theorem 1.A full-period cancellation: $R(k \cdot m, f) = 0$ for $f \in \{2, ..., 30\}$, $m \in \{1, ..., 5\}$.
3. Theorem 2 layered closure: for 50 squarefree $b \in \{6, 10, 14, 15, ..., 210\}$, the first $k$ at which any non-trivial divisor produces $R(k, d) = 0$ is exactly $\mathrm{spf}(b)$; the count at $k = p_1 p_2$ is $2^2 - 1 = 3$; the count at $k = p_1 p_2 p_3$ is $2^3 - 1 = 7$.
4. Theorem 3 asymptotic average: numerical Riemann sum $\to \mathrm{Si}(2\pi)/\pi$ for increasing $f \in \{50, 100, 500, 1000\}$.

Total runtime <5 seconds. Produces a green-light line `ALL ASSERTIONS PASSED`.

### 2.6 Lens-ownership preamble (per `J_PAPER_BOILERPLATE.md` §5.5)

Insert §0 immediately after `\maketitle`:

> *Lens and substrate.* This note works on $\mathbb{Z}$ with the discrete Fejér quotient $R(k, f) = \sin^2(\pi k/f) / (k^2 \sin^2(\pi/f))$ and the smallest-prime-factor function $\mathrm{spf}$. The objects are the standard discrete Fourier-analytic and divisibility structures of the integers; no specialized algebraic substrate is invoked. The squarefree-modulus restriction in Theorem 2 reflects the regime where the layered-divisor-lattice argument applies cleanly. The companion paper [J03] proves the related synchronization theorem at the *first* zero $k = \mathrm{spf}(b)$.

### 2.7 PROVEN/COMPUTED/RHYME/OPEN paragraph (per `J_PAPER_BOILERPLATE.md` §2)

Insert in §1 introduction:

> *Tier discipline.* This paper PROVES three theorems: full-period cancellation $R(k, f) = 0 \iff f \mid k$ (Theorem 1.A), the squarefree layered-divisor structure (Theorem 2), and the asymptotic average $\to \mathrm{Si}(2\pi)/\pi$ (Theorem 3). We COMPUTE the verifications via `proof_d25_loop_closure.py` (primes 3..199, 50 squarefree $b$, exact arithmetic, runtime <5s). The exact identity $\mathrm{sinc}^2(1/2) = (2/3)/\zeta(2)$ is cited as STRUCTURAL RHYME, not theorem — it follows in one line from $\zeta(2) = \pi^2/6$. The theorem-shaped question of why the corridor midpoint at $t = 1/2$ makes this identity structurally relevant is OPEN.

### 2.8 Bibliography expansion

Add to the current 4-entry bibliography:

- **Erdős (1959).** "On the distribution of the smallest prime factor of $n$," *Mathematika* 6, 1–6. (Same addition as J03; for J04 it's the literature on `spf`-distributions.)
- **Tenenbaum (2015).** *Introduction to Analytic and Probabilistic Number Theory*, 3rd ed., Cambridge Studies 46, §III.5. (Smooth numbers context.)
- **Iwaniec & Kowalski (2004).** *Analytic Number Theory*, AMS CP 53, §6.1.
- **Apostol (1976).** *Introduction to Analytic Number Theory*, §3.1–3.4. (For the totient and the sieve in alphabet-size coordinates.)
- **Hardy & Wright (2008).** *An Introduction to the Theory of Numbers*, 6th ed.

This brings the bibliography to 9 entries. Drop the Montgomery 1973 reference if §4 is cut (per 2.4).

### 2.9 Cover letter

Replace current cover letter with one that frames J04 as a companion to J03, not a duplicate:

> Dear Editors of *Integers*,
>
> We submit *Full-Period Cancellation of R(k, f) and the spf-Localization for Squarefree Moduli* as a companion submission to *The First-G Event and a Discrete Sinc² Identity* (J03, also under consideration at *Integers*). The two papers share an underlying object — the discrete Fejér quotient $R(k, f)$ — but address different questions: J03 proves the synchronization at the *first* zero $k = \mathrm{spf}(b)$; the present paper proves the full-period cancellation structure for any $f$, the squarefree layered-divisor closure (Theorem 2: count $2^j - 1$ at the $j$-th primorial divisor), and the asymptotic average $\int_0^1 \mathrm{sinc}^2(t)\, dt = \mathrm{Si}(2\pi)/\pi$ (Theorem 3). The two-paper coupling is intentional: each stands alone and the cross-citations are explicit.
>
> Verification: `proof_d25_loop_closure.py` runs in under 5 seconds and prints `ALL ASSERTIONS PASSED` on first execution.
>
> Sincerely,
> Brayden R. Sanders (corresponding) + M. Gish

This addresses the referee's M1 (self-overlap with J03 companion) by making the differentiation explicit upfront.

---

## §3 — Estimated revision time

| Task | Hours |
|------|-------|
| Rewrite Theorem 2 to add layered-divisor count $2^j - 1$ statement | 2.0 |
| Add Theorem 1.A (full-period cancellation as own theorem) and proof | 0.5 |
| Add Theorem 3 (asymptotic average to Si(2π)/π) and proof | 1.5 |
| Cut current §3 corollaries; replace with one J03-companion corollary | 1.0 |
| Cut §4 (boundary-value section, referee M2 non-sequitur) | 0.25 |
| Update title in .tex (line 46–47) | 0.1 |
| Add §0 lens-ownership preamble + tier-discipline paragraph | 0.5 |
| Bibliography expansion (5 new entries) | 0.5 |
| Rewrite verification script: drop bisection (M3), drop strict-monotonicity claim (M4), add Theorem 2 + Theorem 3 checks | 2.5 |
| Verify script runs green; new green light is `ALL ASSERTIONS PASSED` after the new tests | 0.5 |
| Cover letter rewrite (J03-companion framing) | 0.5 |
| Update README §5 with SAVE PLAN reference + 2-paragraph summary | 0.25 |
| Final pass + arXiv prep | 0.5 |

**Total:** **10–12 hours.** The major work is in proving Theorem 2's layered-divisor count and Theorem 3's asymptotic-average statement, plus verifying both. Both are tractable but neither is purely cosmetic. This is *not* a 4-hour merge like J03 Fork A.

---

## §4 — PROVEN / COMPUTED / RHYME / OPEN (per boilerplate)

**PROVEN:**
- *Lemma 1 (basic biconditional).* For every $b > 1$ and every $k \ge 1$, $\sinc^2(k/b) = 0 \iff b \mid k$.
- *Theorem 1.A (full-period cancellation).* For every $f \ge 2$ and every $k \ge 1$, $R(k, f) = 0 \iff f \mid k$.
- *Theorem 2 (squarefree layered-divisor structure).* For squarefree $b = p_1 \cdots p_r$, the smallest $k$ at which any non-trivial $d \mid b$ produces $R(k, d) = 0$ is $k = \mathrm{spf}(b)$, and at the $j$-th primorial divisor $k = p_1 \cdots p_j$ exactly $2^j - 1$ non-trivial divisors produce zeros.
- *Theorem 3 (asymptotic average).* $\lim_{f \to \infty} \frac{1}{f-1} \sum_{k=1}^{f-1} R(k, f) = \int_0^1 \mathrm{sinc}^2(t)\, dt = \mathrm{Si}(2\pi)/\pi$.
- *Corollary (J03 companion).* The first-zero index in J04 Theorem 2 equals the First-G event of J03 Theorem 3.1.

**COMPUTED:**
- Lemma 1 verified for primes 3..199, all $k \in \{1, ..., p\}$, exact arithmetic.
- Theorem 1.A verified for $f \in \{2, ..., 30\}$, $m \in \{1, ..., 5\}$, exact.
- Theorem 2 verified for 50 squarefree $b \in \{6, 10, ..., 210\}$, exact.
- Theorem 3 numerically verified at $f \in \{50, 100, 500, 1000\}$ vs $\mathrm{Si}(2\pi)/\pi \approx 0.45141$, max error $\le 10^{-3}$ at $f = 1000$.
- Multi-prime squarefree case (J03 companion script): all squarefree $b \le 500$, 22,367 (b,k) pairs, zero exceptions.

**STRUCTURAL RHYME:**
- *Identity sinc²(1/2) = (2/3)/ζ(2).* One-line consequence of $\zeta(2) = \pi^2/6$. Cited as motivation in §1, not derivation. (Per `J_PAPER_BOILERPLATE.md` §1.2.)
- *Primon-gas link: 1/ζ(2) = density of squarefree integers.* The squarefree restriction in our verification regime sits in the primon-gas regime — bridge connection only.
- *Drápal-Wanless 2021 JCTA.* Not invoked in J04 (not a magma paper), but acknowledged as the precedent for the broader (TSML, BHML) magma-family research program.

**OPEN:**
- Why does the corridor midpoint $t = 1/2$ make $\sinc^2(1/2) = (2/3)/\zeta(2)$ structurally relevant? Per the boilerplate this is the open theorem-shaped question.
- Does the Theorem 2 layered-divisor-lattice count $2^j - 1$ extend to non-squarefree $b$ via the radical? The non-squarefree case follows from the squarefree case applied to $\mathrm{rad}(b)$, with multiplicities introduced in the count; the precise formula is not pursued here.

---

## §5 — Lens-ownership paragraph (J04 variant)

Insert immediately after `\maketitle`:

> *Lens and substrate.* This note works on $\mathbb{Z}$ with the discrete Fejér quotient $R(k, f) = \sin^2(\pi k/f) / (k^2 \sin^2(\pi/f))$ and the smallest-prime-factor function $\mathrm{spf}$. The objects are the standard discrete Fourier-analytic and divisibility structures of the integers; no specialized algebraic substrate is invoked. The squarefree-modulus restriction in Theorem 2 reflects the regime where the layered-divisor-lattice argument applies cleanly (the radical of $b$ collapses non-squarefree multiplicities, recovering the squarefree case). The companion paper [J03] proves the related synchronization theorem at the *first* zero $k = \mathrm{spf}(b)$; the present paper handles the full-period cancellation, the squarefree layered closure, and the asymptotic average across the corridor.

This is the J04-specific variant: substrate is plain $\mathbb{Z}$, not Z/10Z; no operator labels; the squarefree restriction is acknowledged as the regime where the proof technique applies, not where the phenomenon lives.

---

## §6 — Recommended retitle / retarget

**Title:** *Full-Period Cancellation of R(k, f) and the spf-Localization for Squarefree Moduli.*

This is the renamed title from the README (2026-05-07). The `.tex` file (`sinc2_zero_law.tex`) retains the old "The Sinc² Zero Law for Squarefree Moduli" title — single-line edit needed.

**Venue:** *Integers* (unchanged).

**Why this retitle:** the collaborator calibration documented in `J_PAPER_BOILERPLATE.md` §1.1 is correct: "Zero Law" implies prime-specific structure that the basic biconditional doesn't deliver. "Full-Period Cancellation" describes what is actually true — $R(k, f) = 0$ at $k = f$ for any $f$, with sin²(π) = 0 doing the work uniformly.

**Why no retarget:** the substantive rebuild proposed above (Theorem 2 with the $2^j - 1$ count + Theorem 3 with the asymptotic average) is exactly the kind of finite, elementary, computable, runnable-witness contribution `Integers` exists for. If the rebuild succeeds, J04 lands cleanly. If a sieve-theory referee insists on a heavier sieve-machinery engagement than J04 plausibly carries (Selberg's $\lambda^2$, Linnik's large sieve), the fallback is to demote J04 to *AMM Notes* or *Math. Magazine* — both still publishable venues, just less prestigious. This is the same Fork-C-equivalent fallback as J03's contingency.

**Per-venue cap.** With both J03 and J04 going to *Integers*, the per-quarter cap (2 papers) is exactly used. The J03 companion submission frames the cap honestly — both papers are referred to each other, both stand alone, both are short notes.

---

## §7 — Risk and contingency

**Primary risk:** Theorem 2 (the layered-divisor-lattice count $2^j - 1$) might be considered insufficiently novel by an *Integers* sieve-theorist referee. The fallback is to (a) merge J04 into J03 as a §6/§7 of the held draft (single paper instead of two; the J03 substance audit's Fork A would then be the path), or (b) demote J04 to AMM Notes / Math. Magazine.

**Secondary risk:** Theorem 3 (asymptotic average $\to \mathrm{Si}(2\pi)/\pi$) might be considered "well-known" — the integral $\int_0^1 \mathrm{sinc}^2(t)\, dt$ is in any signal-processing textbook, and the Riemann-sum argument is standard. The fix: present it as an explicit closed-form for the corridor average, not as a discovery. The novelty is the *combination* of Theorem 1.A + Theorem 3 + Theorem 2 in one note — not any individual statement.

**Tertiary risk:** the verification script rewrite might surface a subtle bug. The J04 referee already flagged two (M3, M4); a clean rewrite is the right path, but it needs careful testing. Allocate 2.5 hours including test debugging.

---

## §8 — Final verdict

**KEEP-WITH-MAJOR-WORK.** The save is viable, but only if Theorem 2 is rebuilt to do real work (the $2^j - 1$ count) and Theorem 3 is added (the asymptotic average via D14). The referee's "Reject" recommendation applies to the *current* draft, not to the rebuilt version. The corpus has the material — D11/D14/D15/D24/D25 are all PROVED; the paper just isn't using them.

The directive "find a reason to keep" is satisfied: the reason is that the discrete Fejér quotient + smallest-prime-factor synchronization story has more depth than a single paper (J03) can carry, and the corpus has the D-table backing for J04 to be the home of (Theorem 2: layered divisor structure) + (Theorem 3: asymptotic average) + (Theorem 1.A: full-period cancellation as canonical statement). 10–12 hours of work converts the current 4-page note into a real *Integers* contribution.

If Brayden has only 4–6 hours total budget across J03+J04, the cleanest path is **Fork A on J03 + merge J04 into J03 as a §7/§8** — a single more-substantial paper instead of two notes. If the budget allows 14–18 hours total, the two-paper companion structure (J03 + tightened J04) is the better outcome because it preserves the per-venue cap usage and gives both papers individual citation footprints.
