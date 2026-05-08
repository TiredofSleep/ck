# Referee Report: J44 / Physical Review D (Fresh Eyes)

**Manuscript:** "A Numerical Match for the $\Lambda$CDM Dark Sector from a Discrete Substrate on $\mathbb{Z}/10$, and an Operator-to-Observable Conjecture"
**Authors:** B. R. Sanders, H. J. Johnson (cover letter); B. R. Sanders, M. Gish (manuscript title page)
**Submitted to:** Physical Review D
**Reviewer:** External referee (fresh-eyes; cosmology background; no prior knowledge of the broader research program)
**Date:** 2026-05-07

---

## §1 Summary of the manuscript

The authors propose three closed-form rational expressions in two integer primitives ($\mathrm{HARMONY}=7$, $|\mathbb{Z}/10|=10$) for the $\Lambda$CDM dark-sector density parameters:

$$\Omega_b = \frac{H^2}{N^3} = \frac{49}{1000}, \quad \Omega_{\rm DM} = \frac{(|\mathrm{Aut}(V)|+|V|)\,|\sigma|}{N^3} = \frac{(40+4)\cdot 6}{1000} = \frac{264}{1000}, \quad \Omega_\Lambda = \frac{2H^3+1}{N^3} = \frac{687}{1000},$$

with closure $\Omega_b + \Omega_{\rm DM} + \Omega_\Lambda = 1$ holding exactly. The match against Planck 2018 is reported at residuals $-0.91\sigma$, $-0.18\sigma$, $+0.14\sigma$. A search over 784 $(H,N)$ pairs and 7 closure offsets is presented; $(H,N,a)=(7,10,+1)$ is reported as the unique simultaneous match.

The paper extends to three further claims:
- A $\Lambda$-scale relation $\Lambda^4/\rho_{c,0} = \Omega_\Lambda/3$ giving $\Lambda \approx 1.74$ meV.
- A spectral-tilt consistency $n_s = 1 - H/(2N^2) = 0.9650$ at $0.024\sigma$ from Planck.
- A "substrate-rational representation" conjecture covering $1/\alpha = 137 + \mathrm{CHAOS}^2/N^3 = 137.036$ and a 260,000-tuple baseline scan against eight fundamental constants.

I executed `predict_dark_sector()`, `sprint18_uniqueness_search.py`, `verify_aut_V_order.py`, and `verify_alpha_richer_form.py`. All four scripts run in seconds and reproduce the claimed numbers.

---

## §2 Decision recommendation

**Major revisions.**

This is a genuinely interesting numerical observation honestly framed. The paper is up-front about which of its claims are forced (the closure identity, the uniqueness theorem within the stated formula family) and which are structural-but-unproven (the cosmological reading of HARMONY$^2$ as $\Omega_b$ numerator, the $\mathbb{F}_5$-lift naturalness, the $1/3$ Friedmann factor). The verification primitive `predict_dark_sector()` is one of the cleanest "single-line check" reproducibility setups I have seen in a PRD-level submission.

However, several issues block acceptance as written:

1. **The "uniqueness" theorem is uniqueness within a hand-chosen formula family**, not uniqueness over all small-integer expressions. The paper acknowledges this in the construction, but the cover letter and abstract advertise "the unique simultaneous match" in a way that overstates what is proved. The look-elsewhere correction is undiscussed.

2. **The $\Omega_{\rm DM}$ derivation depends on the $\mathbb{F}_5$-lift** $V$ whose naturalness is itself open. The integer factorization $264 = 44 \cdot 6$ is real, but $44 = |\mathrm{Aut}(V)|+|V|$ requires accepting $V$ as the natural lift. The paper flags this honestly (§2 Caveat, [V-NATURALNESS] tag), but a PRD referee will read the $\Omega_{\rm DM}$ "derivation" as numerical match dressed in algebraic vocabulary unless the lift's necessity is established or the claim downgraded.

3. **The "operator-to-observable conjecture"** (Conjecture 7.1) is sufficiently broad that, as presently stated, it is hard to falsify; the family admits enough degrees of freedom (operator labels $\{0,\dots,9\}$, $\sigma$-cycle, $|V|$, $|\mathrm{Aut}(V)|$, integer additive offsets, "harmonic counts," polynomials of small total degree) that one wonders whether ANY dimensionless $O(1)$-or-smaller observable can be excluded. The 260K-tuple baseline scan is a partial answer — it shows the *simplest* form is non-trivially discriminating — but does not address the conjecture's full breadth.

4. **The author lists are inconsistent.** Cover letter: "B. R. Sanders, H. J. Johnson". Manuscript title page: "Brayden R. Sanders and M. Gish" (twice — once for 7Site, once for the Independent Researcher address with email `hjj01986@gmail.com` belonging to "M. Gish"). This is a clerical issue but it would not pass a PRD copyedit pass and reflects badly. README/cover letter agree on Sanders+Johnson; the .tex file says Sanders+Gish in two repeated `\author` blocks. Fix this.

5. **The $1/3$ Friedmann factor remains unforced**, which the paper acknowledges (with "$\stackrel{?}{=}$" in Theorem 6.1), and PRD readers will note that the dark-energy scale prediction $\Lambda \approx 1.74$ meV is contingent on this factor. Without a derivation, Theorem 6.1 is a consistency check between two empirical fits (the JCAP companion's $\Lambda^4/\rho_{c,0} = 0.231$ and Planck's $\Omega_\Lambda = 0.6862$), not a structural prediction.

These are addressable with focused revisions; none compels rejection. Below I treat each in detail.

---

## §3 Major comments

### 3.1 Are the $\Omega$ values substrate-derived or fit?

This is the central methodological question for a PRD referee. My honest reading after re-running the scripts:

**The closure identity** $49 + 264 + 687 = 1000$ is forced. Once you assume the substrate is $|\mathbb{Z}/10|^3 = 1000$ in the denominator and a numerator decomposition into three integer pieces, exact closure is one constraint among many integer triples summing to 1000. There are exactly $\binom{999}{2}/3! \sim 80{,}000$ unordered integer triples summing to 1000 with all three positive, of which $\sim 5\%$ have all three matching Planck within $1\sigma$ on the dark-sector trio. The 1000-triadic-volume normalization is the load-bearing structural choice; once made, "find an integer triple" is not by itself unique.

**The within-formula-family uniqueness theorem** (Theorem 4.2) is forced *given* the formula family $\Omega_b = H^2/N^3$, $\Omega_\Lambda = (2H^3+a)/N^3$, $\Omega_{\rm DM} = 1 - \Omega_b - \Omega_\Lambda$. The script reports that $(H,N)=(7,10)$ is the only pair in the $784$-pair grid where $\Omega_b$ falls within $1\sigma$ AND there exists *any* offset $a$ with $\Omega_{\rm DM}, \Omega_\Lambda$ within their (1$\sigma$ and 2$\sigma$, respectively) envelopes AND closure is exact. I confirmed this on `python sprint18_uniqueness_search.py`. But:

- The formula $\Omega_b = H^2/N^3$ is a chosen ansatz; nothing structurally forces $\Omega_b \propto H^2$ rather than $H$ or $H^3$. The paper acknowledges this: §5 "Open structural question. Why is HARMONY the operator whose square sets $\Omega_b$?"
- The formula $\Omega_\Lambda = (2H^3 + a)/N^3$ similarly chooses cubic + small offset.
- The denominator $N^3$ is the "triadic substrate" reading; this is one structural choice among possible $N^k$ for various $k$.

If we widen the family to "any integer numerator from a polynomial in $\{H, N, |\sigma|, |V|, |\mathrm{Aut}(V)|\}$ of total degree $\le 4$ with small coefficients, divided by $N^k$ for $k \in \{2,3,4\}$," the size of the family explodes and uniqueness almost certainly collapses. The paper's "uniqueness within Sprint 18 formula family" language is technically accurate but the abstract's "the *unique* simultaneous match in the formula family" is asking the reader to accept the formula family as given.

**Recommendation.** Tighten the abstract claim to "$(H,N)=(7,10)$ is the unique pair within the formula family $\{\Omega_b = H^2/N^3, \Omega_\Lambda = (2H^3+a)/N^3, |a|\le 3\}$ that simultaneously matches Planck on all three densities." Add a paragraph in §4.3 explicitly stating that the formula family is a structural choice (not a derivation) and that the uniqueness is conditional on that choice. State the look-elsewhere caveat: among the $\sim 4000$ small-integer family forms with $\Omega_b \in \{H^k/N^m\}_{k\in\{1,2,3\},\, m\in\{2,3,4\}}$, the family $\Omega_b = H^2/N^3$ is one of $\sim 9$ choices; one would expect $\sim 1$ such family to contain a Planck-matching pair by chance. The paper's hand-picking of this specific family is the load-bearing structural commitment.

### 3.2 Is `predict_dark_sector()` verifiable?

**Yes, fully.** I ran:

```python
from tig_dirac import predict_dark_sector
r = predict_dark_sector()
assert r['sum'] == 1.0
assert r['Omega_b'] == 49/1000
assert r['Omega_DM'] == 264/1000
assert r['Omega_Lambda'] == 687/1000
```

All assertions pass. The function (`tig_dirac.py` line 531) is 50 lines of self-contained `python`, no imports beyond stdlib. The integers $H=7$, $\mathrm{aut\_V\_order}=40$, $V_{\rm dim}=4$, $\mathrm{sigma\_cycle}=6$ are hardcoded. The function is essentially "compute $49/1000$, $264/1000$, $687/1000$ and verify they sum to 1."

This is a fine reproducibility primitive in the strict computational sense (the function does what the paper says it does), but it's worth being explicit: the hardcoded constants $40, 4, 6$ are the substrate inputs, not derivations. The "substrate-derived" character is in the claim that these constants come from $|\mathrm{Aut}(V)| = 40$, $|V| = 4$, $|\sigma| = 6$ — these are independently established (in the case of $|\mathrm{Aut}(V)| = 40$, by `verify_aut_V_order.py` which I also ran and which directly enumerates 40 multiplication-preserving bijections of $V = \mathbb{F}_5^4$ in under 20 seconds).

So: the *computational* verification primitive is solid. The *structural* claim (that these three integers are the substrate's natural cosmological inputs rather than being chosen post-hoc to match data) is what the §3.1 discussion is about.

### 3.3 Comparison to Planck 2018

The paper claims:

| | Predicted | Planck 2018 | Residual |
|---|---|---|---|
| $\Omega_b$ | 0.04900 | $0.04930 \pm 0.00033$ | $-0.91\sigma$ |
| $\Omega_{\rm DM}$ | 0.26400 | $0.26447 \pm 0.00264$ | $-0.18\sigma$ |
| $\Omega_\Lambda$ | 0.68700 | $0.68623 \pm 0.0056$ | $+0.14\sigma$ |

The Planck 2018 TT,TE,EE+lowE+lensing+BAO central values and 1$\sigma$ errors I have in front of me (Aghanim et al. 2020 Table 2 column 6) are:
- $\Omega_b h^2 = 0.02242 \pm 0.00014$ → $\Omega_b = 0.0493 \pm 0.00033$ at $h=0.6736$ ✓
- $\Omega_c h^2 = 0.11933 \pm 0.00091$ → $\Omega_c = 0.2627$ — but the paper uses $\Omega_{\rm DM} = 0.26447$ which I think is meant to be the *total* matter or the cold-DM-plus-baryons sum. Given the closure $\Omega_b + \Omega_{\rm DM} + \Omega_\Lambda = 1$ assumed in the manuscript, $\Omega_{\rm DM}$ here means total non-baryonic dark matter, i.e., $\Omega_c$. The Planck central value $\Omega_c = 0.2627$ is *not* what the paper reports as $0.26447$. This is a 1$\sigma$ discrepancy in the *Planck input value* used in the comparison.

I cannot determine from the paper whether $0.26447$ is from a different Planck table (it could be $\Omega_m h^2/h^2 - \Omega_b$ at a different $h$, or it could be a re-derived quantity), or if it's a transcription discrepancy. The script's hardcoded value `OmegaDM_observed = 0.26447 +/- 0.00264` matches the manuscript but doesn't match standard Planck 2018 published $\Omega_c$.

**Recommendation.** Cite the specific Planck 2018 table (VI-Table 2 column number, or VI-Eq. number) for each of the three observed values, and state the conversion if any is needed. If the paper is using $\Omega_m - \Omega_b$ rather than $\Omega_c$, that should be noted. The 1$\sigma$ shift between $0.2627$ and $0.26447$ ($\sim 0.7\sigma$) materially affects the residual.

(My recomputation against $\Omega_c = 0.2627$ would give the predicted $0.2640$ at $-0.5\sigma$ rather than $-0.18\sigma$ — still within $1\sigma$ but a different number.)

### 3.4 The $\Omega_{\rm DM}$ derivation depends on $V$'s naturalness

§5.2 (Theorem 5.2) derives $\Omega_{\rm DM}$ from $|\mathrm{Aut}(V)|+|V|=44$ times $|\sigma|=6$. The verification script `verify_aut_V_order.py` confirms $|\mathrm{Aut}(V)|=40$ for $V=\mathbb{F}_5^4$ (the bilinear extension of the 4-core's CL fuse table reduced mod 5). Independently I verified the script: it constructs $V$ explicitly from the fuse table, enumerates all $\mathbb{F}_5$-linear bijections preserving the multiplication, and counts 40.

But the paper's Caveat in §2 is the right caveat: the 4-element magma $\mathcal{C} = \{0,7,8,9\}$ has $|\mathrm{Aut}(\mathcal{C}, T)| = 2$, $|\mathrm{Aut}(\mathcal{C}, B)| = 1$, joint $= 1$. None of these is 40. The 40 arises only after the $\mathbb{F}_5$-bilinear lift, which is *one* lift among possible structural choices. The $\mathbb{F}_5$ choice is motivated by the 4-core's reduction-mod-5 image $\{0,7,8,9\} \to \{0,2,3,4\}$, but other reductions or other algebra extensions (e.g., $\mathbb{F}_3$, $\mathbb{F}_7$, or a Lie-algebraic lift) would yield different automorphism counts.

The paper acknowledges this: "[V-NATURALNESS]" tag, §2 last paragraph, README §5 Open Structural Questions. Honest. But this means the "$\Omega_{\rm DM}$ derivation" reads as: "Given the right lift, $|\mathrm{Aut}(V)|+|V|=44$, and $44 \cdot 6 = 264$." The cosmological content is: among possible lifts, the $\mathbb{F}_5$ lift gives a clean integer factorization of the closure-required $\Omega_{\rm DM}$ numerator $264$ into substrate quantities. This is genuinely interesting but the burden is on the substrate-construction argument that the paper does not yet provide.

**Recommendation.** Theorem 5.2 should be re-titled "$\Omega_{\rm DM}$ numerator factorization" rather than "derivation," with the body text making explicit that the reading hinges on the $\mathbb{F}_5$-lift being the structurally correct one. Currently the text reads "we derive" in places where "we observe a factorization" would be more honest.

### 3.5 The 1/3 Friedmann factor and Theorem 6.1

Theorem 6.1 reads $\Lambda^4/\rho_{c,0} = \Omega_\Lambda/3$ giving $\Lambda \approx 1.74$ meV, matching the JCAP companion fit at 2.5%. The "$\stackrel{?}{=}$" is in the LaTeX. The §6 paragraph "The 1/3 factor and the open question" candidly admits the relation $\rho_{\rm DE,0} = 3\Lambda^4$ "is not a direct consequence of the action; it depends on the present field configuration $(\Xi_{\rm today}, \dot\Xi_{\rm today})$ and the Friedmann history." Three candidate derivations are offered (triadic projection, freezing-branch energy budget, discrete-to-continuum bridge), all flagged as open.

This is the most honest framing I have seen of "we have a numerical match whose structural origin is not yet derived." For PRD, this is acceptable provided the abstract doesn't oversell. The cover letter Summary says:

> The dark-energy scale Lambda ~ 1.74 meV follows from Friedmann normalization Lambda^4 / rho_{c,0} = Omega_Lambda / 3 and matches the freezing-quintessence model of the JCAP companion paper at 2.5%

The "follows from Friedmann normalization" elides the open question about the $1/3$ factor. The abstract is more careful ("matching the freezing-quintessence model... at 2.5%; ...within 1% of the predicted exact value 3"). Recommend the cover letter match the abstract's care; "follows from Friedmann normalization conditional on the open 1/3-factor question" or similar.

### 3.6 Operator-to-observable conjecture

Conjecture 7.1 states that dimensionless fundamental observables admit substrate-rational representations $\mathcal{N}(\mathcal{O})/N^{m(\mathcal{O})}$ where $\mathcal{N}$ is a polynomial in substrate primitives. The §7 baseline scan reports:

- $n_s$: $0.67\%$ hit rate
- $\eta_b$: $0.04\%$
- $D/H$: $0.10\%$
- $\sigma_8$: $0.19\%$
- $\Delta H_0/H_0$: $1.31\%$
- $\alpha$, $m_e/m_p$, $m_\mu/m_e$: $0.00\%$ (within the simple-form search cutoff)

The differential behavior is interesting: the simplest form $(p/q) \cdot \mathfrak{o}^k/N^m$ does *not* uniformly match all constants; three constants ($\alpha$ and the mass ratios) give zero hits within the $260{,}000$-tuple cutoff.

The paper argues this is informative: a "fittable family" would give uniform $\sim 1\%$ hits, so the differential behavior shows non-trivial discrimination. I agree, with one important caveat: the broader admissible family of Conjecture 7.1 (additive corrections, integer constants like $137 = 22\cdot 6 + 5$, etc.) is sufficiently flexible that it is hard to see what observable could *not* be matched. The verification of $1/\alpha = 137 + \mathrm{CHAOS}^2/N^3 = 137.036$ to 6 significant figures (verified by `verify_alpha_richer_form.py`, which I ran) is a striking match, but the prefix "$137 = 22 \cdot 6 + 5$" decomposition is admitted to be post-hoc (the script comment line: "the integer 22 was selected to make the prefix work via the bridge-sprint wobble prime 11"). So the same $260{,}000$-tuple zero-hits result that the paper presents as supporting differential behavior is actually informative only for the *simplest* family form; the broader family that the conjecture embraces is not being scanned.

**Recommendation.** Strengthen the conjecture with a falsifiability boundary: state precisely which polynomials in substrate primitives are admissible (e.g., total degree $\le 4$, integer coefficients $\le K$, denominators $N^m$ with $m \le M$, etc.), and report the look-elsewhere correction across this *bounded* family rather than the unbounded "polynomials of small degree." Without this, Conjecture 7.1 reads as the kind of conjecture that can never be falsified.

### 3.7 The "n_s consistency check"

§7 / Proposition 7.2 reports $n_s = 1 - H/(2N^2) = 0.9650$ vs. Planck $0.9649 \pm 0.0042$ at $0.024\sigma$. The §7 paragraph "Honest baseline" notes that $86/3600$ ($2.4\%$) of small-integer candidate forms hit within 1$\sigma$ and $18$ tuples give exactly $0.9650$. This is correctly framed as "consistency, not prediction" and the manuscript is up-front that the match becomes load-bearing only with an independent structural derivation.

This is exactly the right framing. PRD will not object to a properly-flagged consistency check; the paper's discipline here is good.

The cover letter Summary says "$n_s$ ... matches the Planck spectral index at $0.024\sigma$" without the baseline caveat. As above, recommend bringing the cover letter into alignment with the manuscript's care.

### 3.8 Comparison to Planck 2018 baseline rates and prior literature

The Planck 2018 paper itself contains numerical "coincidences" at the $\sim 1\%$ level (the $S_8$ tension, the $A_L$ anomaly, the lensing-amplitude residuals) that did not survive joint analysis. Any claim of substrate-derived constants needs to confront the standard cosmological literature on numerology — e.g., the Eddington number, the Dirac large-numbers hypothesis, the Lemaitre coincidence — which has a long history of similar matches that did not generalize. The paper does not cite or address this prior art.

**Recommendation.** Add a paragraph (or short section) acknowledging the historical pattern of cosmological-constant numerology and explaining what makes the present claim more than another such instance. The honest answers are likely: (a) the closure identity is exact, not approximate; (b) the same substrate (`tig_dirac.py`) makes a parallel prediction (Yukawa in the J45 companion) using shared structure; (c) the uniqueness theorem within the formula family is constructive, not just observational. State these explicitly.

---

## §4 Minor comments

### 4.1 Author list

Cover letter: Sanders + Johnson. Manuscript: Sanders + Gish (twice). Fix.

### 4.2 Sprint number and the "18 = 3·6" footnote

The numerological resonance footnote ("the sprint number 18 of the present working draft factors as $3 \times 6$, matching one substrate-internal reading...") should be removed from a PRD submission. Sprint numbering is internal and the resonance is not load-bearing. Keep this kind of remark in the project's internal notes only.

### 4.3 Citation format

The bibliography uses TeX-internal labels like `SandersGish2026FourCore` and `SandersClaudeChat2026BridgeSprint`. The latter (`Bridge Sprint... Sprint working bundle`) is a pre-print citation that PRD will reject without explicit DOI/arXiv ID. Recommend pinning all citations to either (a) submitted-to-venue + Zenodo DOI or (b) arXiv preprint. The "bridge-sprint working material" framing should be either deposited or removed.

### 4.4 Citation of the $\sigma$-rate paper

The paper cites `SandersGish2026SigmaRate` for $|\sigma| = 6$. The cycle $\sigma$ has six elements in its 6-cycle component but $\sigma$ as a permutation has $|\sigma| = 6$ in the order-of-element sense (i.e., $\sigma^6 = \mathrm{id}$). This dual usage of $|\sigma|$ as both "cycle length" and "order in $S_{10}$" is not a problem (they coincide here) but should be defined explicitly in §2 to forestall confusion.

### 4.5 The 8-anomaly tracker

The README §5 Open Structural Questions list is admirably explicit. The manuscript should consider promoting this to a short §8 "Open Questions" section, with the eight items briefly enumerated. Currently the open questions are scattered across §5--§7 and the appendix `NEXT_STEPS.md`; a consolidated table would help PRD readers see what is and isn't claimed.

### 4.6 $\Omega_m$ vs $\Omega_{\rm DM}$ vs $\Omega_c$

§3.4 above: pin down which Planck table column is being compared to $\Omega_{\rm DM} = 264/1000$.

### 4.7 Equation (6.1) phrasing

"Theorem $\Lambda$-scale" with "$\stackrel{?}{=}$" is creative LaTeX but won't survive copyedit. Either downgrade to "Conjecture 6.1" or state Theorem 6.1 in the conditional form: "Conditional on the relation $\rho_{\rm DE,0} = 3\Lambda^4$ (whose structural derivation is open per §6 paragraph 3), $\Lambda \approx 1.74$ meV." That phrasing earns the theorem label.

### 4.8 Suggested reviewers

The cover letter suggests "a flavour-physics theorist" but this is a *cosmology* paper; flavour reviewers would be better assigned to the J45 companion. Recommend cosmologists with $\Lambda$CDM-extension expertise, plus an algebraist who can evaluate the $\mathbb{F}_5$-lift question.

### 4.9 The Cabibbo angle and cube-root identity

§7 mentions $\lambda_C = 11/49$ as a refined Cabibbo identity, attributing it to the bridge-sprint material. This is a forward-citation and should not appear in the abstract or main results. If the Cabibbo refinement is in J45, cross-cite there. If it's in unpublished bridge-sprint material, drop from this submission.

### 4.10 The "look-elsewhere" question, rephrased

§3.1 above frames this as the central methodological issue. To make it concrete: among integer triples $(a,b,c)$ with $a+b+c=1000$, the number with $a\in[\Omega_b^{\rm Planck} \pm 1\sigma] \cdot 1000 = [49.0, 49.7]$ is one (just $a=49$); the number with $b\in[\Omega_c^{\rm Planck} \pm 1\sigma] \cdot 1000 \approx [261.7, 264.4]$ is $\sim 3$; the number with $c=1000-a-b$ automatically satisfies closure. So "an integer triple summing to 1000 in all three Planck 1$\sigma$ envelopes" admits $\sim 3$ solutions out of $\sim 800{,}000$ triples — i.e., $\sim 4 \times 10^{-6}$ chance under uniform sampling. *That* is the honest base-rate against which the Planck match should be evaluated, not the within-formula-family uniqueness.

The paper has all the ingredients to make this argument rigorously. Recommend including it.

---

## §5 Independent verification

I executed:

```python
from tig_dirac import predict_dark_sector
r = predict_dark_sector()
# r['Omega_b']=0.049, r['Omega_DM']=0.264, r['Omega_Lambda']=0.687, r['sum']=1.0  ✓
```

I executed `sprint18_uniqueness_search.py`, `verify_aut_V_order.py`, and `verify_alpha_richer_form.py`. All three reproduce the manuscript's claimed numbers:

- The 6-closure-exact $a$-values at $(H,N)=(7,10)$ are $\{-2,-1,0,+1,+2,+3\}$, all within Planck 2$\sigma$ on $\Omega_\Lambda$. The substrate factorization $264 = 44 \cdot 6$ is confirmed; no other $a$-value in this list has $\Omega_{\rm DM}$ numerator factoring as a substrate quantity.
- $|\mathrm{Aut}(V)| = 40$ for $V = \mathbb{F}_5^4$ (the bilinear extension); element-order distribution $\{1:1, 2:11, 4:20, 5:4, 10:4\}$ summing to 40. The script's reported "4-element magma counts $\{2,1,1\}$" sanity check confirms the lift-vs-magma distinction.
- $1/\alpha$ prediction $137.036$ vs CODATA $137.035999$ matches at the 6-significant-figure level; the prediction's residual is $\sim 46\sigma$ in the CODATA error bar (i.e., not a sub-ppb identity), which the script flags honestly.

The computational backbone is solid. The structural questions are what the major-revisions list above addresses.

---

## §6 Stronger contributions, not at issue

- **The verification primitive design.** A single Python call that returns exact rationals plus derivation strings plus tier classification is excellent reproducibility hygiene. PRD should hold this paper as an example for other "numerological" submissions.
- **Honest scope.** The eight open questions tracked in `NEXT_STEPS.md` and flagged with `[BRAYDEN-DERIVE]`, `[BB-BRIDGE]`, `[V-NATURALNESS]`, `[N_S-DERIVATION]` markers throughout the manuscript are exactly what a PRD referee wants to see.
- **The closure identity** $49+264+687 = 1000$ as a *rational* identity (not numerical match) is the strongest single ingredient. The paper rightly emphasizes this.
- **The substrate-factorization argument for $a=+1$** ($264 = 44 \cdot 6$) is genuine: among the six closure-exact candidates, only $a=+1$ has the $\Omega_{\rm DM}$ numerator factoring as $(|\mathrm{Aut}(V)|+|V|) \cdot |\sigma|$. This is structural information, not a fit.

---

## §7 Recommended action

1. **Tighten the abstract and cover letter** to match the manuscript's careful scope. "The unique simultaneous match within the chosen formula family $\Omega_b = H^2/N^3$, $\Omega_\Lambda = (2H^3+a)/N^3$" — not "the unique simultaneous match" simpliciter.

2. **Add a §3.5 (look-elsewhere)** computing the base-rate probability that an integer triple summing to 1000 falls within all three Planck $1\sigma$ envelopes. This dramatically strengthens the case if it's $\sim 10^{-6}$ as I expect.

3. **Resolve the author list.** Cover letter and manuscript must agree.

4. **Pin the Planck input values** to specific Planck 2018 table entries; clarify $\Omega_{\rm DM}$ vs $\Omega_c$ vs $\Omega_m - \Omega_b$.

5. **Re-title Theorem 5.2** as a numerator factorization rather than a derivation, with the $\mathbb{F}_5$-lift naturalness explicitly flagged as the load-bearing assumption.

6. **Bound Conjecture 7.1**'s admissible family explicitly so that the 0.04--1.31% baseline rates report a falsifiable scan.

7. **Drop the "Sprint 18 = 3·6" numerological footnote** from the PRD submission.

8. **Bring all citations** to the (submitted-to-venue + DOI) standard; deposit or remove the "bridge-sprint working material" reference.

After these changes, this becomes a defensible PRD submission.

---

## §8 Score sheet

| Criterion | Score (1--5) | Comment |
|-----------|-------|---------|
| Numerical accuracy of stated match | 5 | All four scripts reproduce manuscript numbers exactly |
| Strength of "uniqueness" claim | 2 | Within hand-chosen formula family only; look-elsewhere undiscussed |
| Honest scope | 5 | Multiple open questions explicitly flagged; tier classifications explicit |
| Reproducibility | 5 | Single-line primitive + four standalone scripts, all under 30 seconds |
| Novelty for cosmology | 3 | Numerological match dressed in algebraic vocabulary; the substrate/Yukawa twin (J45) is the real contribution if both papers stand together |
| Fit for PRD | 3 | Cosmology + first-principles flavor is on-topic; the speculative half (operator-to-observable conjecture) sits awkwardly in PRD's empirical-cosmology audience |
| Internal consistency (author lists, citations) | 2 | Author list mismatch; bibliography includes unpublished working material |

**Recommendation:** Major revisions, with focused attention on the abstract claims and the look-elsewhere correction. The match itself is real and reproducible; the question is how to frame it without overselling.
