# SAVE_PLAN_J13 — Forced 5/7 Torus / Cyclotomic Forcing (Acta Arithmetica)

**Date:** 2026-05-07
**Status:** SAVE — by polynomial correction, arithmetic correction, calibration retreat, and §6/§7 honesty pass. Paper survives, but with a retitled scope ("Forced 5/7 Torus Aspect Ratio (Up to a Calibration Choice)") and with Acta Arithmetica likely still the wrong target — Integers / Math Intelligencer / a short-note venue is more likely the appropriate landing.
**Referee:** `Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J13_ActaArith_FreshEyes.md` (Reject; M1, M2 hard errors; M3-M6 structural).
**Companion:** J07 (Flatness Theorem) — see `SAVE_PLAN_J07.md`.

---

## §1 — The two hard errors and the fixes (with verification)

### Error 1 — Misidentified minimal polynomial of $A_7 = 2\cos(\pi/7)$

**The claim in the original manuscript** (abstract, Remark 1.2, statement of Theorem 1.1, Lemma 4.2): the minimal polynomial of $A_7 = 2\cos(\pi/7)$ over $\mathbb{Q}$ is
$$
8x^3 - 4x^2 - 4x + 1.
$$
**This is wrong.** That polynomial is the minimal polynomial of $\cos(\pi/7)$, not of $2\cos(\pi/7)$. The two are related by the substitution $x \mapsto x/2$ (then clearing denominators), so they have the same Galois structure but different roots.

**Verification (sympy, 50-digit precision):**
```
>>> minimal_polynomial(2*cos(pi/7), x)
x**3 - x**2 - 2*x + 1            # CORRECT MP of A_7
>>> minimal_polynomial(cos(pi/7), x)
8*x**3 - 4*x**2 - 4*x + 1        # MP of cos(pi/7), what the paper cited
>>> simplify(g(2*cos(pi/7)))     # g(x) = x^3 - x^2 - 2x + 1
0                                 # confirmed root
>>> N(8*A7**3 - 4*A7**2 - 4*A7 + 1, 50)
27.611171244527927273866494740212599713040257738336    # paper's polynomial NOT zero at A_7
```

**Fix applied to manuscript:** the polynomial $8x^3 - 4x^2 - 4x + 1$ is replaced throughout by $x^3 - x^2 - 2x + 1$ (abstract, Remark in §1, Theorem 4.1, Lemma 4.2). The Lehmer 1933 / Watkins–Zeitlin 1993 reference is now cited correctly: the minimal polynomial of $2\cos(\pi/p)$ over $\mathbb{Q}$ has degree $\varphi(2p)/2 = (p-1)/2$ for $p$ odd prime, which gives the correct polynomial. The remark in §1 explicitly notes the cause of the original confusion (the substitution $x \mapsto x/2$).

### Error 2 — Arithmetic mistake in Lemma 4.2 evaluation $f(-1/2)$

**The claim in the original manuscript** (line 172): for $f(x) = 8x^3 - 4x^2 - 4x + 1$,
$$
f(-1/2) = 8(1/8) - 4(1/4) - 4(-1/2) + 1 = 1 - 1 + 2 + 1 = 3.
$$
**This is wrong twice over.** The cube $(-1/2)^3 = -1/8$, not $1/8$; so $8 \cdot (-1/2)^3 = -1$, not $+1$. The correct evaluation:
$$
f(-1/2) = -1 - 1 + 2 + 1 = 1.
$$

**Verification (sympy):**
```
>>> f.subs(x, Rational(-1,2))
1
```

**Fix applied to manuscript:** the Lemma 4.2 proof has been rewritten using the correct polynomial $g(x) = x^3 - x^2 - 2x + 1$. The rational root test for $g$ is much shorter — the only candidates are $\pm 1$ (since $g$ is monic with constant term $\pm 1$), and $g(1) = -1$, $g(-1) = 1$, neither zero. The arithmetic is now trivial and verifiable by inspection. The discriminant $\disc(g) = 49 = 7^2$ is recorded in a remark, identifying the Galois group as $A_3 = \mathbb{Z}/3\mathbb{Z}$.

---

## §2 — What survives

The structural skeleton of the paper survives both errors:

1. **Cyclotomic threshold.** The fact that $\deg_{\mathbb{Q}}(A_p) = (p-1)/2$ for odd prime $p$, hence $\deg_{\mathbb{Q}}(A_5) = 2$ and $\deg_{\mathbb{Q}}(A_7) = 3$, is correct (Lehmer 1933). The transition from quadratic closure (at $p = 5$) to cubic obstruction (at $p = 7$) is real and is the structural content of the paper. It does not depend on which specific polynomial is cited as the minimal polynomial of $A_7$; it depends only on the *degree*.

2. **The deg-2 / deg-3 obstruction.** With the corrected polynomial $g(x) = x^3 - x^2 - 2x + 1$, irreducibility over $\mathbb{Q}$ follows from a one-line rational root test, and $A_7$ is genuinely a degree-$3$ algebraic number over $\mathbb{Q}$. The "first cubic obstruction at $p = 7$" claim is preserved. The Galois group $A_3$ is now identified explicitly.

3. **The cyclotomic-embedding calibration.** Once the calibration is fixed (Definition 2.4 in the revised manuscript), the ratio $5/7$ is forced by the cyclotomic threshold above. The forcing is conditional on the calibration, but the conditional statement is a clean, verifiable theorem with no number-theoretic gaps after the polynomial correction.

In short: **the polynomial correction does not affect the structural conclusion.** The paper proves what it claims it proves, once the right polynomial is named.

---

## §3 — Other revisions needed (per referee)

### M3 — "Forcing" argument is heuristic — **CALIBRATION RETREAT**
The original proof asserted "the proportionality constant cancels" and presented $R/r = 5/7$ as unconditional. The revised manuscript:
- Adds **Definition 2.4 (cyclotomic-embedding calibration)** that explicitly fixes the embedding scale so a prime-$p$ closed circle has circumference $p$.
- Adds **Remark 2.5** that the theorem is forced *relative to this calibration* and is conditional on it. A self-contained derivation of the calibration is left as future work (open question (b) in §8).
- **Retitles the paper:** "The Forced 5/7 Torus Aspect Ratio (Up to a Calibration Choice)". The "(Up to a Calibration Choice)" is honest about the dependency.

### M4 — Five companion derivations don't hold up — **HONEST PASS**
The original §6 listed five "derivations" of $5/7$ as independent confirmations. After honest review:
- **Reformulation 1** (cyclotomic reduction gap) — relabeled as a reformulation, not an independent derivation. Same theorem in different language.
- **Reformulation 2** (prime-π-φ field bridge) — similarly a Galois-lattice reformulation, not independent.
- **Independent appearance 1** (First-G coprime window): the original sketch claimed $4/5$ and $6/7$ "give" $5/7$; checked arithmetically, neither $(4/5)\cdot(6/7) = 24/35$ nor $(4/5) + (6/7) - 1 = 13/35$ equals $5/7$. The connection is *not* a direct arithmetic identity but a common cyclotomic threshold; this is restated honestly.
- **Independent appearance 2** (TSML/BHML harmony cell ratio $73/101$): the original claimed $73/101 \approx 5/7$ as if it were derived. **Checked: $73/101 = 0.7227\ldots \neq 5/7 = 0.7143\ldots$ (relative gap $\approx 1.2\%$, NOT exact).** The revised manuscript records this honestly as a numerical observation, retracts the earlier claim of exact agreement, and demotes the question to an open problem (whether the discrepancy is asymptotic or genuine).
- **Two original "derivations" deleted entirely:** the BTQ operator-balance sketch and the $5/7 = (\sin(\pi/5)\sin(\pi/7))^?$ bridge. Both lacked self-contained mathematical content (the latter literally has a $^?$ in the formula).

### M5 — Companion (Flatness Theorem) inaccessible to referee — **CITE PREPRINT + SKETCH**
The Flatness Theorem (J07) is a parallel paper in submission. The cyclotomic-embedding calibration of Definition 2.4 in the revised manuscript provides enough self-contained detail that the present paper can be read independently of J07; the dependency is now stated explicitly as "the calibration is imported from J07" rather than as an unstated assumption.

### M6 — Conjecture A.2 contradicted by $n = 14$ — **RESTRICT SCOPE**
The original Conjecture 7.1 stated the formula for all squarefree $n$, but $n = 14$ has $7 \mid n$ and no prime divisor with $\deg_{\mathbb{Q}}(A_p) \le 2$ irrational, so $p_{\mathrm{closed}}$ is undefined. The revised manuscript:
- States the conjecture under the explicit hypothesis that some prime divisor $p_i \mid n$ has $A_{p_i}$ irrational and $\deg_{\mathbb{Q}}(A_{p_i}) \le 2$.
- Includes **Proposition 7.2** identifying the domain: this hypothesis is satisfied iff $5 \mid n$ (since $p = 5$ is the only prime with $A_p$ irrational of degree $\le 2$).
- Lists worked examples: $n = 10, 15, 35$ in the domain; $n = 6, 14, 21$ silent (conjecture does not apply).

### m1 — Duplicate `\author` blocks — **FIXED**
Replaced the duplicate `\author{Brayden R. Sanders \and M. Gish}` blocks with separate `\author` entries: Sanders at 7Site, Gish as Independent Researcher.

### m3 — "Narrow-major" terminology — **REPLACED**
The non-standard "narrow-major torus" label is replaced by an explicit corollary stating that under the chosen labelling convention (additive flow on $S^1_R$, multiplicative on $S^1_r$) the ratio is $5/7 < 1$, with a remark explaining the relation to the standard $\mathbb{R}^3$ ring-torus convention $R > r$.

### m4 — "Not jointly orderable" undefined — **MOVED TO BODY**
The abstract uses precise language: the additive structure is totally ordered by divisor refinement; the multiplicative structure has pairwise-incompatible CRT-factor partitions (cite Sanders–Mayes UOP Lemma 4.1). The phrase "not jointly orderable" is no longer used as a primitive notion.

### m7 — "Structural 7 zeros" undefined — **DELETED**
Open question (b) is rewritten without the "7 zeros" reference (which was a proprietary CK-program concept with no place in an Acta Arithmetica submission). The new (b) asks whether the cyclotomic data at $p = 7$ contributes a structural curvature term in the algebraic torus.

### Two new open questions added
- **(b) Calibration-free derivation.** Explicitly states what would make Theorem 1.1 unconditional (a derivation of the canonical calibration from $\mathbb{Z}/n\mathbb{Z}$ alone).
- **(e) The 73/101 near-agreement.** Records the observed $1\%$ discrepancy as an open problem rather than swept under the rug.

---

## §4 — Updated PROVEN / COMPUTED / RHYME / OPEN

- **PROVEN (with the polynomial correction):**
  - Theorem 1.1 (Cyclotomic-calibrated $5/7$ aspect ratio): conditional on the cyclotomic-embedding calibration of Definition 2.4, $T^* = R/r = 5/7$ for $n = 10$.
  - Theorem 3.1 (Major-radius selection): $R = 5$ under the calibration.
  - Theorem 4.1 (Minor-radius selection): $r = 7$ under the calibration.
  - Lemma 4.2: $g(x) = x^3 - x^2 - 2x + 1$ is the minimal polynomial of $A_7 = 2\cos(\pi/7)$ over $\mathbb{Q}$, and is irreducible. (Corrected from the original $8x^3 - 4x^2 - 4x + 1$, which was the MP of $\cos(\pi/7)$.)
  - Proposition 7.2: $p_{\mathrm{closed}}(n)$ is well-defined iff $5 \mid n$.
- **COMPUTED:**
  - $\deg_{\mathbb{Q}}(A_p) = (p-1)/2$ for $p$ odd prime, verified via Lehmer / Watkins–Zeitlin.
  - $\disc(g) = 49 = 7^2$ confirmed via sympy; Galois group $A_3$.
  - $73/101 - 5/7 = 6/707 \approx 0.0085$ (1.2% relative gap), recorded as a numerical observation.
- **STRUCTURAL RHYME:**
  - Convergence of the cyclotomic threshold prime $7$ across multiple appearances (Theorem 4.1, the $\sinc^2$ resonance window of J03/First-G law, the discriminant of $g$).
  - The choice of major/minor labelling for the additive vs. multiplicative flow (a convention from J07 Flatness Theorem, not derived in the present paper).
- **OPEN:**
  - Generalize to $n = 15, 35$ (next cases in the conjecture's domain).
  - Calibration-free derivation (would make $T^* = 5/7$ unconditional).
  - $73/101$ vs. $5/7$ discrepancy: asymptotic correction or genuinely independent?
  - Connection to modular curves $X(N)$ at the cusps.

---

## §5 — Estimated revision time

- **Polynomial correction (M1, M2):** done in this pass — ~30 minutes.
- **Calibration retreat (M3):** done in this pass — ~45 minutes.
- **§6 honesty pass (M4):** done in this pass — ~45 minutes.
- **Conjecture scope restriction (M6):** done in this pass — ~30 minutes.
- **Minor exposition (m1–m8):** done in this pass — ~30 minutes.
- **Total revision time already invested:** ~3 hours; manuscript is in revised state in `manuscript/manuscript.tex`.
- **Remaining work to bring to submission-ready:**
  - Brayden's referee-rigor pass (~30 minutes).
  - Cover letter update reflecting calibration-conditional framing (~15 minutes).
  - Bibliography cull (per m8) — keep Lehmer, Washington, drop the broad textbook citations not actually used (~15 minutes).
  - **Total:** ~1 hour to submission-ready after this save plan.

---

## §6 — Recommended retitle/retarget

**Retitle (already applied to manuscript):**
"The Forced 5/7 Torus Aspect Ratio (Up to a Calibration Choice): Cyclotomic Forcing on $\mathbb{Z}/10\mathbb{Z}$"

The qualifier "(Up to a Calibration Choice)" is the honest description after the M3 fix. The paper proves a calibration-conditional theorem; this is what the title now says.

**Retarget recommendation:**
- **Acta Arithmetica is likely still the wrong venue,** even after corrections. The mathematical content reduces to one cyclotomic threshold theorem plus its application to a torus aspect ratio (calibration-dependent). Acta Arithmetica typically wants either deeper number-theoretic content or a cleaner unconditional result.
- **Better targets:**
  1. **Integers** (open access, open to short notes; the cyclotomic threshold + calibration framework + open-problem section is natural for Integers' style).
  2. **Mathematical Intelligencer** as an essay on cyclotomic boundaries between degree 2 and degree 3 (per the referee's own suggestion).
  3. **American Mathematical Monthly** as an exposition of the deg-2/deg-3 transition with the torus interpretation.
  4. **As a section of the J07 Flatness Theorem retarget** (per `SAVE_PLAN_J07.md`); this is the most economical route — fold the cyclotomic threshold into J07's structural appendix rather than carrying it as a standalone paper.
- **If standalone retargeting:** Integers is the recommendation. A short note (~6 pages) with the corrected polynomial, the calibration-conditional theorem, the scope-restricted conjecture, and the honest §6 will fit Integers' format.

**Decision recommended:** retarget to **Integers** as a standalone short note, OR fold into J07 (companion). Brayden's call.

---

## §7 — Checklist of fixes applied to `manuscript/manuscript.tex`

- [x] Corrected polynomial $8x^3 - 4x^2 - 4x + 1 \to x^3 - x^2 - 2x + 1$ throughout (abstract, §1 remark, §4 Theorem and Lemma 4.2).
- [x] Fixed Lemma 4.2 arithmetic (rewritten using corrected polynomial; trivial rational root test).
- [x] Added Definition 2.4 (cyclotomic-embedding calibration) and Remark 2.5 (conditional nature).
- [x] Added Remark 4.3 (Galois group $A_3$, discriminant $49$).
- [x] Reframed Theorems 1.1, 3.1, 4.1 as conditional on the calibration.
- [x] Replaced "narrow-major" terminology with explicit corollary + remark.
- [x] §6 honest pass: relabeled reformulations vs. independent appearances; retracted the $73/101 = 5/7$ claim.
- [x] §7 conjecture scope restricted to squarefree multiples of $5$; Proposition 7.2 added.
- [x] §8 open questions: dropped "structural 7 zeros"; added calibration-free derivation and 73/101 discrepancy.
- [x] Fixed duplicate `\author` blocks.
- [x] Added `\newtheorem{conjecture}` for the conjecture environment.
- [x] LaTeX environment balance verified (30 begin / 30 end, all matched).

---

## §8 — Sympy verification log (reproducible)

```python
import sympy
from sympy import symbols, cos, pi, Rational, minimal_polynomial, factor, N, discriminant

x = symbols('x')
A7 = 2 * cos(pi/7)

# Error 1: the polynomial
print('MP of 2*cos(pi/7):', minimal_polynomial(A7, x))
# -> x**3 - x**2 - 2*x + 1                 (CORRECT)
print('MP of cos(pi/7):',   minimal_polynomial(cos(pi/7), x))
# -> 8*x**3 - 4*x**2 - 4*x + 1             (what paper cited; wrong number)

# Confirm the paper's polynomial doesn't vanish at A_7
f_paper = 8*x**3 - 4*x**2 - 4*x + 1
print('f_paper(A_7) =', N(f_paper.subs(x, A7), 50))
# -> 27.611...  (NOT zero)

# Confirm correct polynomial DOES vanish at A_7
g = x**3 - x**2 - 2*x + 1
print('g(A_7) =', N(g.subs(x, A7), 50))
# -> 0E-159     (zero at machine precision)

# Error 2: arithmetic
print('f_paper(-1/2) =', f_paper.subs(x, Rational(-1, 2)))
# -> 1          (paper claimed 3)

# Irreducibility of g
print('g(1)  =', g.subs(x, 1))    # -> -1
print('g(-1) =', g.subs(x, -1))   # -> 1
# Monic cubic, only rational candidates ±1 by rational root theorem;
# neither is a root, so g is irreducible over Q.

# Discriminant -> Galois group
print('disc(g) =', discriminant(g, x))   # -> 49 = 7^2 -> A_3 = Z/3Z

# 73/101 vs 5/7
print('73/101 - 5/7 =', Rational(73, 101) - Rational(5, 7))
# -> 6/707 (about 1.2% of 5/7, NOT exact)
```

---

**Save status:** ACHIEVED. Paper fixed, retitled, retargeted (Integers recommended), and ready for Brayden's pass.
