# Referee Report: J13 / Acta Arithmetica (Fresh Eyes)

**Manuscript:** "The Forced 5/7 Torus Aspect Ratio: Cyclotomic Forcing on $\mathbb{Z}/10\mathbb{Z}$"
**Authors:** B. R. Sanders, M. Gish
**Submitted to:** Acta Arithmetica
**Reviewer:** External referee (anonymous, fresh eyes; no prior exposure to the authors' research program)
**Date:** 2026-05-07

---

## §1. Summary of the manuscript

The authors consider four algebraic structures on $\mathbb{Z}/10\mathbb{Z}$ — additive divisor lattice, multiplicative orbit lattice, additive translation flow, multiplicative root flow — and assert (citing a companion *Flatness Theorem*) that the minimal smooth $2$-manifold simultaneously hosting these structures is a torus $T^{2} = S^{1}_{R} \times S^{1}_{r}$. The present paper claims to determine the aspect ratio $R/r$ from cyclotomic data.

The main result (Theorem 1.1) asserts:
$$
T^{*} := R/r = 5/7,
$$
where $R$ is forced proportional to the smallest prime $p \mid 10$ at which $A_{p} := 2\cos(\pi/p)$ has algebraic degree $\le 2$ over $\mathbb{Q}$ (namely $p = 5$, with $A_{5} = \varphi$), and $r$ is forced proportional to the smallest prime at which $A_{p}$ has algebraic degree $\ge 3$ over $\mathbb{Q}$ (namely $p = 7$).

The technical core is the irreducibility of a cubic minimal polynomial of $A_{7}$ (Lemma 4.2, stated as $8x^{3} - 4x^{2} - 4x + 1$), verified by the rational root test. Section 6 catalogs five additional "independent derivations" of $5/7$ from the authors' research program. Section 7 conjectures a generalization for arbitrary squarefree $n$.

I have verified each numerical claim independently in `sympy`. The verifications produced **two technical errors** and **multiple unsupported structural claims**, detailed in §3 below.

---

## §2. Decision recommendation

**Reject.** The paper cannot be salvaged into an Acta Arithmetica submission in its current form. The mathematical content reduces to standard textbook facts about cyclotomic minimal polynomials (Niven, Lehmer 1933, Washington Ch. 2) embedded in a framework that depends entirely on an unverified companion paper.

The reasons are layered:

1. **The central technical claim is misstated.** The polynomial $8x^{3} - 4x^{2} - 4x + 1$ in Lemma 4.2 is the minimal polynomial of $\cos(\pi/7)$, not of $A_{7} = 2\cos(\pi/7)$. The actual minimal polynomial of $A_{7}$ is $x^{3} - x^{2} - 2x + 1$. Both are degree-3 irreducible over $\mathbb{Q}$, so the structural conclusion ("$A_{7}$ has degree 3") is preserved, but the paper proves irreducibility of the wrong polynomial.

2. **An arithmetic error appears in the rational-root-test proof.** The paper's evaluation $f(-1/2) = 3$ (line 172) is incorrect; the correct value (for the polynomial as written) is $f(-1/2) = 1$. The error sources from $8 \cdot (-1/2)^{3} = -1$, but the paper writes $8 \cdot (1/8) = 1$, dropping the cube's sign.

3. **The "forcing" argument is heuristic, not rigorous.** Sections 3 and 4 motivate the assignment $R \propto 5$, $r \propto 7$ via cyclotomic closure / obstruction language, but never establish that the torus aspect ratio is determined by these primes rather than (e.g.) being a free parameter in the *Flatness Theorem* construction. The crucial step "the proportionality constant cancels" (line 132) is unjustified.

4. **The "five companion derivations" of §6 are vague allusions.** Each of Derivations 1–5 is a one-paragraph sketch citing the authors' own program; none has a self-contained statement, and Derivation 4 admits an asymptotic-only fit to $73/101 \approx 0.7228 \neq 5/7 = 0.7143$ that the paper presents as exact.

5. **Heavy dependence on an unsubmitted companion.** Theorem 2.2 (Flatness obstruction), the structural input from which the torus topology is taken as given, is cited as Sanders–Gish "Flatness Theorem" submitted to *J. Pure Appl. Algebra*. A referee cannot assess whether the present paper has content without seeing that companion.

A revised manuscript could potentially be a short note in *Integers* or *American Mathematical Monthly* if the authors (i) restate the central claim correctly, (ii) provide a self-contained derivation of why the torus aspect ratio is determined by these primes (not assumed), and (iii) drop the "five companion derivations" framing. But Acta Arithmetica is not the right venue.

---

## §3. Major issues

### M1. The minimal polynomial of $A_{7} = 2\cos(\pi/7)$ is misidentified.

The paper repeatedly asserts (abstract, Remark 1.2 page 2, statement of Theorem 1.1, Lemma 4.2 line 168, etc.) that the minimal polynomial of $A_{7} = 2\cos(\pi/7)$ over $\mathbb{Q}$ is $8x^{3} - 4x^{2} - 4x + 1$. This is incorrect.

Direct computation:
$$
A_{7} = 2\cos(\pi/7) \approx 1.8019, \qquad 8(1.8019)^{3} - 4(1.8019)^{2} - 4(1.8019) + 1 \approx 27.6 \neq 0.
$$
By contrast, the minimal polynomial of $\cos(\pi/7)$ (with $\cos(\pi/7) \approx 0.9009$) is $8x^{3} - 4x^{2} - 4x + 1$. The relation is the substitution $x \mapsto x/2$: if $u = \cos(\pi/7)$ satisfies $8u^{3} - 4u^{2} - 4u + 1 = 0$, then $A_{7} = 2u$ satisfies $w^{3} - w^{2} - 2w + 1 = 0$ (where $w = 2u$).

A `sympy` confirmation:
```
>>> minimal_polynomial(2*cos(pi/7), x)
x**3 - x**2 - 2*x + 1
>>> minimal_polynomial(cos(pi/7), x)
8*x**3 - 4*x**2 - 4*x + 1
```

Effect on the paper:
- The structural claim "$A_{7}$ has degree 3 over $\mathbb{Q}$" remains true (since $x^{3} - x^{2} - 2x + 1$ is irreducible over $\mathbb{Q}$ — rational roots $\pm 1$ give $-1, 1$ respectively, neither zero).
- Lemma 4.2 as written is a true statement about a different number ($\cos(\pi/7)$, not $A_{7}$). The proof of irreducibility (rational root test) carries through for the true minimal polynomial $x^{3} - x^{2} - 2x + 1$ in one line: $g(1) = -1 \neq 0$, $g(-1) = 1 \neq 0$, so no rational roots, so irreducible.
- All structural conclusions (degree-3 obstruction at $p = 7$) are preserved, but the paper as it stands does not prove the result it claims to prove.

The Lehmer (1933) reference cited in the proof of Lemma 4.2 actually uses $2\cos(2\pi/n)$, not $2\cos(\pi/n)$, and gives a different polynomial again (degree $\varphi(n)/2$). The author should consult Lehmer carefully and verify the formula.

**Recommended action:** Replace the polynomial $8x^{3} - 4x^{2} - 4x + 1$ with the correct $x^{3} - x^{2} - 2x + 1$ throughout (abstract, statement, proof). This requires re-verifying the rational root test (trivial: $g(\pm 1) \in \{-1, 1\}$). Or, alternatively, redefine $A_{p} := \cos(\pi/p)$ (without the factor of 2), in which case the cited polynomial is correct but every other formula in the paper changes by powers of $2$.

### M2. Arithmetic error in the rational root test.

Page 7 lines 172–173 evaluate the polynomial $f(x) = 8x^{3} - 4x^{2} - 4x + 1$ at $x = -1/2$:
> "$f(-1/2) = 0 + 1 - (-2) + 1 = 1 - 1 + 2 + 1 = 3$ (recompute: $8(1/8) - 4(1/4) - 4(-1/2) + 1 = 1 - 1 + 2 + 1 = 3 \neq 0$)"

This is incorrect. The correct evaluation is:
$$
f(-1/2) = 8 \cdot (-1/2)^{3} - 4 \cdot (-1/2)^{2} - 4 \cdot (-1/2) + 1 = -1 - 1 + 2 + 1 = 1 \neq 0.
$$
The error is in computing $8 \cdot (-1/2)^{3}$: this equals $-1$, not $+1$. The authors appear to have computed $8 \cdot |(-1/2)^{3}|$ instead.

The conclusion (no rational root at $x = -1/2$) is correct under either evaluation, since both $1$ and $3$ are nonzero. But the proof as written is wrong, and a referee would catch this.

**Recommended action:** Correct line 172. (Note: this issue is moot if M1 is addressed — for the correct polynomial $g(x) = x^{3} - x^{2} - 2x + 1$, the only rational candidates are $\pm 1$ and the test is one line.)

### M3. The "forcing" of $R \propto 5$ and $r \propto 7$ is asserted but not proved.

Theorems 3.1 and 4.1 assert that the major and minor radii $R, r$ are *forced* by cyclotomic structure to particular primes. The proofs proceed by language ("the closure condition", "the obstruction") that I cannot translate into a precise mathematical argument.

In particular:

(a) The proof of Theorem 3.1 (line 121–133) embeds $\mathbb{Z}/n\mathbb{Z}$ into $S^{1}$ via $\Phi(x) = e^{2\pi i x/n}$ and computes the trace of multiplication by $\zeta_{n}$. The identification $R \propto p$ then comes from "the closure condition: the $A$-flow on the $p_{i}$-component encodes a closed circle iff $A_{p_{i}}$ admits a finite-degree algebraic relation over $\mathbb{Q}$ that factors through a quadratic extension." But every algebraic number admits a finite-degree algebraic relation over $\mathbb{Q}$ — this is the definition of algebraic. The "factors through a quadratic extension" condition is the condition $\deg_{\mathbb{Q}}(A_{p}) \le 2$, which is what the paper says it derives. The argument is circular: the prime is selected by the condition the paper imposes.

(b) Theorem 4.1 (lines 145–164) says the $M$-flow's "continuum closure" requires $\mathbb{Q}(A_{p})$ to be at most quadratic, and the obstruction at $p = 7$ forces $r \propto 7$. But the obstruction prime $p = 7$ does not divide $n = 10$. The paper acknowledges this in line 162: "the obstruction prime is determined globally by the cyclotomic structure of $\mathbb{Q}$, not by the specific primes dividing $n$." This is a strong claim — that $r$ is determined by a number-theoretic fact about $\mathbb{Q}$, *not* about the specific ring $\mathbb{Z}/10\mathbb{Z}$ — and it is asserted without proof. Why does the global cyclotomic structure determine the minor radius of a torus *associated to a particular finite ring*? The paper does not say.

(c) The "proportionality constant cancels" (line 132) sweeps a critical issue under the rug. The major and minor radii of an embedded torus have units of length; the ratio $R/r$ is a dimensionless number that depends on the choice of embedding. The paper does not specify the embedding, so the ratio is not well-defined without further input.

**Recommended action:** Either (i) reduce the paper's claims to "if we calibrate the radii to the cyclotomic embedding by the prescription [explicit formula], then $R/r = 5/7$", or (ii) provide a derivation from the *Flatness Theorem* (companion paper) that pins down the embedding. As stated, the "forcing" argument is not a proof.

### M4. The "five companion derivations" (§6) do not constitute independent derivations.

Section 6 catalogs five additional derivations of $5/7$, presented as supporting the central result by independent agreement.

(a) **Derivation 1 (sinc² first-G law):** the sketch "the smallest-prime-factor coprime window $W_{p} = (p-1)/p$ stabilizes at $p = 5$ with $W_{5} = 4/5$, and the cyclotomic complement $1 - 1/7 = 6/7$ enters as the multiplicative companion. The two together give the first-G stability constant $5/7$." The authors do not explain how $4/5$ and $6/7$ "give" $5/7$: $(4/5) \cdot (6/7) = 24/35 \neq 5/7$, $(4/5) + (6/7) - 1 = 13/35$ (not $5/7$), nor any obvious arithmetic combination.

(b) **Derivation 2 (BTQ operator balance):** the sketch refers to "the trace of the joint operator $T_{g} \circ M_{d}$ for $g$ a primitive root mod 5 and $d$ a multiplier mod 2", saying the balance point is $5/7$. No definition of "balance point" is given, and a primitive root mod 5 has order 4 while $\mathbb{Z}/2\mathbb{Z}$ has multipliers of order 1 or 2 — the joint operator's trace would naturally be a sum of cyclotomic values, not a rational.

(c) **Derivation 3 (cyclotomic reduction gap):** the paper states this is "essentially the same forcing as Theorem 1.1 stated at the level of cyclotomic fields rather than torus radii". So this is not an independent derivation; it is the same derivation in different language.

(d) **Derivation 4 (TSML/BHML harmony cell ratio):** the sketch claims the harmony cell counts $73$ and $28$ give the ratio "$73/(28+73) = 73/101$, approximately $5/7$". But $73/101 = 0.7228$, while $5/7 = 0.7143$ — the relative difference is about 1%, and approximate agreement of two distinct rationals at the 1% level is not a derivation. The paper qualifies this with "more precisely, the structural identity $73 + 28 = 101$ together with the prime structure of $101$ enforces the $5/7$ ratio at the asymptotic limit of the table" — this is unverifiable speculation.

(e) **Derivation 5 (prime-π-φ bridge):** the sketch is "$5/7 = (\sin(\pi/5) \cdot \sin(\pi/7))^{?}$ via the cyclotomic identities for the golden ratio $\varphi$ and the cubic $A_{7}$". The "$^{?}$" symbol explicitly marks the formula as undefined, and the rest is hand-waving.

The convergence of multiple derivations on a common value is a classical heuristic in mathematics (e.g., the various derivations of $\zeta(2) = \pi^{2}/6$). For such convergence to be evidence of structural significance, each derivation must (i) be self-contained, (ii) yield the value as an output rather than imposing it as a target, and (iii) be verifiable by an independent reader. None of the five derivations meets these criteria; they read as five different ways of asserting the same conclusion rather than five independent paths to it.

**Recommended action:** Either remove §6 entirely (recommended), or replace each one-paragraph sketch with a self-contained derivation in an appendix. As written, §6 weakens rather than strengthens the paper.

### M5. The companion *Flatness Theorem* is not available for review.

The entire framework of the paper rests on Theorem 2.2 (cited as Sanders–Gish 2026, *Flatness Theorem*, submitted to *J. Pure Appl. Algebra*). I have not seen this companion paper. The present manuscript does not reproduce or sketch the Flatness Theorem, and a referee cannot verify the topological claim from which the entire torus-radius analysis proceeds.

A referee's working assumption is that companion papers are accessible (preprint server, supplementary materials, or sufficient detail in the present paper's introduction). Without access to the *Flatness Theorem*, I cannot determine:
- Whether the four-structure embedding into a torus is unique up to isotopy.
- Whether the major and minor circle assignments are canonical (as the paper assumes) or a choice.
- Whether the "proportionality constants" (§3 line 132) are intrinsic to the embedding.

**Recommended action:** Either submit the *Flatness Theorem* simultaneously and reference its preprint, or include a self-contained §1.5 sketching the topological argument and the canonical $S^{1}_{R}, S^{1}_{r}$ assignment.

### M6. Conjecture 7.1 has internal inconsistencies.

The generalization conjecture (line 220–225) states:
$$
T^{*}(\mathbb{Z}/n\mathbb{Z}) = p_{\text{closed}} / p_{\text{obstr}},
$$
where $p_{\text{closed}}$ is the smallest prime $p \mid n$ with $\deg_{\mathbb{Q}}(A_{p}) \le 2$, and $p_{\text{obstr}}$ is the smallest prime (not necessarily $\mid n$) with $\deg_{\mathbb{Q}}(A_{p}) \ge 3$.

The paper itself notes (line 228) that for $n = 14 = 2 \cdot 7$, "$p_{\text{closed}} = 7$ (since at $p = 7$, $A_{7}$ has degree $3 \ge 3$, but the closure threshold is degree $\le 2$ — so $p_{\text{closed}}$ would not exist)". This admits the conjecture is ill-posed for $n = 14$. The paper says "the conjecture requires care for $n$ containing 7" — but this is a substantive failure, not a care-issue: the conjecture's domain excludes any $n$ for which no prime divisor has $A_{p}$ of degree $\le 2$, which includes $n = 7, 14, 21, 35, 49, \ldots$ and most $n$ with large prime factors.

For $n = 6 = 2 \cdot 3$, the conjecture predicts $p_{\text{closed}} = 3$, $p_{\text{obstr}} = 7$, ratio $3/7 \approx 0.4286$. The authors offer no evidence (numerical or structural) that this ratio actually arises from the $\mathbb{Z}/6\mathbb{Z}$ structure.

**Recommended action:** Either restrict the conjecture's scope explicitly (e.g., "$n$ squarefree with at least one prime divisor $p \in \{3, 5\}$"), or provide computational evidence for at least one $n$ beyond $10$ that the conjectured ratio matches.

---

## §4. Minor issues

### m1. Two duplicate \author blocks (lines 35–40).

The .tex source has two `\author{Brayden R. Sanders \and M. Gish}` blocks back-to-back, with conflicting addresses (`7Site LLC` and `Independent Researcher`). One of these is presumably the M. Gish address. AmSart will process this in a confused way; please use a single `\author` per author with proper `\address` linking.

### m2. Citation [SandersMayes-CL] inconsistency.

In §2 line 102, the paper cites "Sanders–Mayes, UOP companion, Lemma 4.1" for the pairwise incompatibility of CRT factor partitions. The bibliography entry [SandersMayes-UOP] (item 9 of references) is "submitted to J. Number Theory, 2026". A standard requirement at Acta Arithmetica is that cited unpublished companions are available for the referee. If [SandersMayes-UOP] is also under review, it should be available; if not yet submitted, the present paper should not cite it as an established source.

### m3. Remark on "narrow-major" torus (Cor. 5.1, line 187).

The remark "The standard $\mathbb{R}^{3}$ embedding of a torus with $r > R$ is the spindle torus, which self-intersects but in the algebraic setting we always work with the abstract torus" is a presentational issue. If $R$ is the major radius (distance from torus axis to tube center) and $r$ is the minor radius (tube radius), then $r > R$ means $T^{*} = R/r < 1$ — but the standard torus convention has $R > r$ (so that the tube does not self-intersect). The authors' calibration $R = 5, r = 7$ is therefore the *opposite* of the standard torus convention. This should be stated up front rather than as a corollary remark, since it affects how the reader visualizes the geometry throughout.

### m4. The phrase "not jointly orderable" (abstract).

The abstract says the four structures are "not jointly orderable". This is a striking phrase but undefined. The body of the paper instead notes that the additive divisor lattice is totally ordered while the multiplicative orbit lattice is not — that's a less dramatic statement. Please use precise language in the abstract.

### m5. Section 5's statement of the main result.

§5 (lines 179–184) gives a 2-line "Proof of Theorem 1.1" that is essentially: "By Theorems 3.1 and 4.1, $R \propto 5$ and $r \propto 7$, so $R/r = 5/7$." This is fine in form, but Theorems 3.1 and 4.1 themselves do the heavy lifting and they are not solid (M3). Please integrate the proof flow rather than presenting Theorem 1.1 as a corollary of two unproved theorems.

### m6. "The torus of $\mathbb{Z}/10\mathbb{Z}$ is a 'narrow-major' torus" — undefined term.

"Narrow-major" is not a standard term in differential or algebraic geometry. Either define it (footnote, remark) or use standard language ("ring torus" vs "spindle torus" if appropriate).

### m7. Open question (b) — "structural 7 zeros" (line 236).

The open question references "the structural '7 zeros' arising from the multiplicative cyclotomic obstruction at $p = 7$". This is unclear: the standard torus Gaussian curvature has zero set on a circle (where $\cos\theta_{M} = 0$), not a discrete set of 7 zeros. The "structural 7 zeros" appears to be a concept from the authors' research program that has no place in an Acta Arithmetica submission without definition.

### m8. Bibliography quality.

The bibliography contains both classical references (Niven, Lehmer, Washington, Hardy–Wright, Ireland–Rosen, Lang) and four self-cites to companion submissions. The companion submissions are appropriate, but the classical references are over-broad — six general textbooks on number theory for a result that uses only the irreducibility of one cubic. A focused bibliography (Lehmer 1933 + Washington Ch. 6 §6.1 on $2\cos(2\pi/n)$ + Niven Ch. 6) would be more appropriate.

---

## §5. Comments on the "$5/7$ value"

The numerical value $5/7$ is striking only relative to the authors' independent research program. From a fresh-eyes perspective:
- It is the ratio of two consecutive odd primes ($5$ and $7$).
- It has algebraic-degree partition exactly at this boundary: $A_{5}$ is degree 2, $A_{7}$ is degree 3.
- The boundary itself is well-known in cyclotomic theory: degree of $\mathbb{Q}(2\cos(2\pi/p))$ over $\mathbb{Q}$ is $(p-1)/2$, transitioning from $\le 2$ to $\ge 3$ between $p = 5$ and $p = 7$.

So the specific value $5/7$ is the natural ratio at the cyclotomic threshold. The paper's claim is that this ratio is the *forced* aspect ratio of the $\mathbb{Z}/10\mathbb{Z}$ torus. The referee's concern is whether the forcing is mathematical or rhetorical. As described in M3, the forcing is rhetorical: the paper selects the closure prime ("smallest $p$ with degree $\le 2$") and obstruction prime ("smallest $p$ with degree $\ge 3$") and presents their ratio as forced, but does not prove that the torus actually has these radii.

A genuinely interesting result would be: prove that the *Flatness Theorem* embedding of $\mathbb{Z}/10\mathbb{Z}$ into a torus determines the aspect ratio in a way that depends only on the cyclotomic data, and that this dependence yields $5/7$. The present paper announces this conclusion without proving it.

---

## §6. Summary of recommended changes (in priority order)

If the authors wish to revise for resubmission (to a different journal, since Acta Arithmetica should reject):

1. **(M1)** Correct the minimal polynomial of $A_{7}$. Use $x^{3} - x^{2} - 2x + 1$ throughout, or redefine $A_{p} := \cos(\pi/p)$.
2. **(M3)** Provide a rigorous derivation of why $R/r$ is determined by these primes, not assumed. This may require including the *Flatness Theorem* construction in detail.
3. **(M4)** Either remove §6 or rewrite it to give self-contained derivations.
4. **(M5)** Make the *Flatness Theorem* companion available to the referee.
5. **(M2)** Correct the arithmetic error at line 172.
6. **(M6)** Restrict the scope of Conjecture 7.1 or provide computational evidence beyond $n = 10$.
7. **(m1–m8)** Address the minor exposition issues.

---

## §7. Recommendation summary

**Reject.** The paper as submitted has a misidentified central polynomial (M1), an arithmetic error (M2), an unproved "forcing" argument (M3), unsupported "companion derivations" (M4), and depends on an inaccessible companion paper (M5). The conjectural generalization (M6) is internally inconsistent.

The mathematical content reduces to: "$A_{5}$ has degree 2 over $\mathbb{Q}$; $A_{7}$ has degree 3 over $\mathbb{Q}$" — both known to Lehmer (1933). Wrapping these in a "torus aspect ratio is forced to $5/7$" framework is creative but, as written, not mathematically substantiated.

The paper might be appropriate for *Mathematical Intelligencer* or *American Mathematical Monthly* as an essay on cyclotomic boundaries between degree 2 and degree 3, or might fold into the *Flatness Theorem* companion as Section 5 of that paper. Acta Arithmetica is not the right venue.

---

## §8. Reviewer disclosures

I am a number-theoretic referee with experience in cyclotomic field theory and rational forcing arguments. I have no prior contact with the authors and no knowledge of the broader research program ("TIG", "CK", "TSML/BHML") referenced in the manuscript. I evaluated the paper purely on its standalone mathematical content as visible to a reader new to the framework.

Verifications were performed in `sympy` with a 50-digit precision context. All counterexamples (M1 polynomial misidentification, M2 arithmetic error, M4(a) non-derivation of $5/7$ from $4/5$ and $6/7$) are reproducible from the supplied .tex source.

— External Referee, 2026-05-07
