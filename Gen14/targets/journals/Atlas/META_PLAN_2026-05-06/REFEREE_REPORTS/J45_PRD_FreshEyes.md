# Referee Report: J45 / Physical Review D (Fresh Eyes)

**Manuscript:** "The Mass Hierarchy from $V^{\otimes 5}$ SU(5) Decomposition: a Substrate-Forced Froggatt--Nielsen Pattern with $\lambda = 10/49$"
**Authors:** B. R. Sanders, H. J. Johnson (cover letter); B. R. Sanders, M. Gish (manuscript title page)
**Submitted to:** Physical Review D
**Reviewer:** External referee (fresh-eyes; flavour physics + GUT background; no prior knowledge of the broader research program)
**Date:** 2026-05-07

---

## §1 Summary of the manuscript

The authors propose that all nine SM charged-fermion Yukawa couplings flow from:

- A single "substrate-derived" suppression scale $\lambda = T^*(1-T^*) = (5/7)(2/7) = 10/49 \approx 0.2041$, claimed to equal $|\mathbb{Z}/10|/H^2$ where $H = \mathrm{HARMONY} = 7$.
- The top-quark Yukawa anchor $y_t = 0.93$ (Tier-A measured).
- Integer powers $n_{(p,\mathrm{gen})} \in \{0,3,5,6,7,9\}$ "forced" from the $V^{\otimes 5}$ SU(5) decomposition $\mathbf{1}\oplus\bar{\mathbf{5}}\oplus\mathbf{10}$ plus a parity-crossing cost $d_p \in \{0,3,3\}$ plus a "$\sigma$-orbit generation step" $s_p \in \{?,?,?\}$.

The paper reports $y^{\rm pred}/y^{\rm meas}$ ratios in $\{1.00, 1.08, 1.06, 0.33, 0.60, 0.51, 0.79, 0.11, 0.20\}$ for (top, charm, up, bottom, strange, down, tau, muon, electron). Five sit in the conventional Froggatt-Nielsen factor-of-three window; four (bottom, strange, muon, electron) are off by factors $\sim 1.7$ to $\sim 9$ and are absorbed into empirical $C_p \in [0.11, 0.79]$ multipliers said to be the "incomplete bosonic-substrate specification."

A Cabibbo cube-root identity $\lambda_C \approx (Y_d/Y_u)^{1/3}$ is proposed, with $\lambda$ unifying the CKM mixing structure with the mass hierarchy.

I executed `predict_yukawa(particle, generation)` and `yukawa_table_full()` from `tig_dirac.py`. Both return numerically as the manuscript claims.

---

## §2 Decision recommendation

**Major revisions** (verging on reject; the paper has fundamental framing problems that revisions can address but the underlying claim is weaker than the abstract represents).

The paper's strongest contribution is the observation that $\lambda = 10/49 \approx 0.204$ is numerically close to the Wolfenstein parameter $\lambda_W \approx 0.225$ (off by $\sim 9\%$) and that integer powers of $\lambda$ produce charged-fermion Yukawa magnitudes within standard FN $O(1)$ residuals. The "substrate origin" of $\lambda$ as $T^*(1-T^*)$ where $T^*=5/7$ is a chosen identification; whether $T^*$ is the right structural quantity for the FN scale is not derived from first principles in this paper.

The most serious issues are:

1. **The "forced powers" are not actually forced.** §4 introduces "parity-crossing cost" $d_p$ and "generation step" $s_p$ as if they were rigid consequences of the SU(5) representation theory, but inspecting Definition 4.2 shows that $s_u=4$, $s_d=2$, $s_e=3$ are extracted *from the empirical Yukawa hierarchies themselves* ("$y_c/y_t = \lambda^3$; charm $\to$ up: $y_u/y_c = \lambda^4$"). The integer powers in Table 4.1 are a re-encoding of the empirical hierarchies, not a derivation from SU(5). The paper acknowledges this ("the asymmetry... reflects the distinct $\sigma$-orbit structure on $V^{\otimes 5}$'s matter-side cells under the SM gauge action; we track the pattern empirically and flag its substrate-natural assignment as open in §7"), but the abstract and §1 advertise "zero free FN charges" which is misleading.

2. **The "fit" has factor-of-9 residuals.** The muon ratio is $y^{\rm pred}_\mu/y^{\rm meas}_\mu = 0.11$, off by a factor of $\sim 9$. The paper frames this as an $O(1)$ Froggatt-Nielsen $C_p$ residual, but conventional FN models with three free FN charges achieve factor-of-2 accuracy on each Yukawa; the present model's factor-of-9 residual on the muon is conventionally a *failure* of the FN ansatz, not an "incomplete bosonic-substrate specification."

3. **The "single $\lambda$" claim is misleading.** Remark 3.2 introduces a *refined* $\lambda_{\rm ref} = 11/49 \approx 0.2245$ for the Cabibbo angle that matches the empirical CKM at $0.4\%$. The paper uses $\lambda = 10/49$ for the mass-hierarchy fit and admits the difference is "$9.4\%$" but does not report the mass-hierarchy fit at $\lambda_{\rm ref} = 11/49$ for comparison. If the framework genuinely needs *two* values of $\lambda$ (one for masses, one for CKM), the "single substrate quantity" claim is weakened.

4. **The sterile-neutrino prediction has no see-saw.** The paper predicts neutrino Dirac masses at FN powers $\{12, 13, 14\}$ giving $m_\nu \in [0.05, 0.85]$ eV, near the Planck $\sum m_\nu < 0.12$ eV bound. But there is no mechanism for the right-handed neutrino mass; the paper acknowledges this is open. The result, then, is a Dirac-mass prediction with no see-saw, which is incompatible with neutrino oscillation phenomenology unless additional structure is supplied. This is honest but reads as "we have a prediction in the right rough range without a mechanism to make it real."

5. **Author list inconsistency** (same as J44 companion): cover letter says Sanders + Johnson, manuscript says Sanders + Gish twice.

These are addressable but not in a single revision round; this paper needs to be either substantially rewritten or split into "the lambda=10/49 observation" (which is a real observation) and "the FN-power assignment" (which is a re-encoding rather than a derivation).

---

## §3 Major comments

### 3.1 Are the integer powers actually forced from SU(5)?

This is the central claim and I need to scrutinize it carefully.

**The claim:** "The integer powers $n_{(p,\mathrm{gen})}$ are read off directly from the parity-crossing cost (one $\mathbf{10} \to \bar{\mathbf{5}}$ flip costs $\lambda^3$) plus one generation step per $\sigma$-cycle position." (§4 Definition 4.1)

**The actual structure of Table 4.1.** $n_{(p,\mathrm{gen})} = d_p + \Delta_{\rm gen}$.

| Particle | $p$ | gen | $d_p$ | $\Delta_{\rm gen}$ | $n$ |
|---|---|---|---|---|---|
| top | up | 3 | 0 | 0 | 0 |
| charm | up | 2 | 0 | 3 | 3 |
| up | up | 1 | 0 | 7 | 7 |
| bottom | down | 3 | 3 | 0 | 3 |
| strange | down | 2 | 3 | 2 | 5 |
| down | down | 1 | 3 | 4 | 7 |
| tau | lepton | 3 | 3 | 0 | 3 |
| muon | lepton | 2 | 3 | 3 | 6 |
| electron | lepton | 1 | 3 | 6 | 9 |

The $\Delta_{\rm gen}$ values: in the up sector $\{0,3,7\}$, in the down sector $\{0,2,4\}$, in the lepton sector $\{0,3,6\}$. These are *not* a single arithmetic progression. The paper's Definition 4.2 ("Generation step $s_p$") gives $s_u = 4$ (charm $\to$ up: $\lambda^4$), $s_d = 2$ (down sector arithmetic progression $\Delta = 2$), $s_e = 3$ (lepton sector arithmetic progression $\Delta = 3$). But the up sector has both $s_u^{(3\to 2)} = 3$ (top $\to$ charm) AND $s_u^{(2\to 1)} = 4$ (charm $\to$ up) — i.e., the up sector is *not* a single arithmetic progression at all. The $\Delta = 0, 3, 7$ in the up column is the empirical $\log y$ gap between charged-fermion Yukawas in base $\lambda$, rounded to integers.

**This is the issue.** The integer powers are not "forced from the $\sigma$-orbit structure"; they are read off the empirical hierarchies and labeled with $\sigma$-orbit indexing. The mapping is consistent (you can write $0,3,7$ as $\sigma$-orbit positions if you assign the orbit positions cleverly), but the assignment is not unique and the paper acknowledges this is open ("the substrate-natural assignment is one of the open structural questions"; see §7.2).

**Recommendation.** §1's "zero free FN charges" claim must be removed or substantially qualified. The integer powers are forced *given* the assignment of generations to $\sigma$-orbit positions, which itself is an open choice. The true structure of the present pattern is:

- 1 free anchor: $y_t$
- 1 free Wolfenstein-style scale: $\lambda$ (proposed as $10/49$, but with refined $11/49$ also available; *"single $\lambda$"* is weakened by Remark 3.2)
- 9 integer powers, of which only 4 ($d_p \in \{0,3,3\}$ assigning the up sector vs down/lepton parity-crossing cost; the absolute generation index 3) are SU(5)-forced; the remaining 5 are flexible $\sigma$-orbit assignments empirically tuned to the data.

This is *fewer free parameters than standard FN* (which has 3 FN charges + 1 $\epsilon$ scale = 4 free parameters), but the "zero free FN charges" framing is too strong.

### 3.2 The "Wolfenstein" comparison: $10/49$ vs $11/49$

§3 (Theorem 3.1) derives $\lambda = T^*(1-T^*) = (5/7)(2/7) = 10/49$. Remark 3.2 then introduces $\lambda_{\rm ref} = (|\sigma| + |\mathcal{C}|)/H^2 = 11/49$ for the Cabibbo angle.

So we have:
- $\lambda = 10/49 \approx 0.2041$ (mass hierarchy)
- $\lambda_{\rm ref} = 11/49 \approx 0.2245$ (CKM Cabibbo)
- $\lambda_W \approx 0.225$ (empirical Wolfenstein)

The mass-hierarchy fit uses $10/49$ which is $9.4\%$ off the Wolfenstein value but produces ratios $\{1.00, 1.08, 1.06, 0.33, 0.60, 0.51, 0.79, 0.11, 0.20\}$. If the framework actually wants $\lambda_{\rm ref} = 11/49 \approx 0.2245$ everywhere, the predictions shift:

For the muon at $n = 6$: $0.93 \cdot (11/49)^6 \approx 0.93 \cdot 0.0001286 \approx 1.196 \times 10^{-4}$ vs $y^{\rm meas}_\mu = 6.1 \times 10^{-4}$, ratio $\approx 0.196$ — i.e., still factor-of-5 off. The refined $\lambda_{\rm ref}$ doesn't help the muon problem.

For the top: $0.93 \cdot 1 = 0.93$ ✓ (anchor unchanged).
For the bottom at $n=3$: $0.93 \cdot (11/49)^3 \approx 0.93 \cdot 0.01133 \approx 0.01053$ vs $y^{\rm meas}_b = 0.024$, ratio $\approx 0.439$ — improved from $0.329$ to $0.439$ but still factor-of-2 off.

So neither $\lambda$ value nails the bottom or muon Yukawas. The refined $11/49$ improves CKM but not the mass-hierarchy fit. The paper's framing "use $10/49$ for masses, $11/49$ for CKM" is a 2-parameter framework, not a 1-parameter framework.

**Recommendation.** State explicitly that the framework uses two values of $\lambda$ — one for the FN mass scale ($10/49$) and one for the CKM Cabibbo angle ($11/49$). The "single substrate-derived $\lambda$" framing is misleading. The two values are close but they are not equal, and neither alone matches both mass and CKM data within their conventional precision.

### 3.3 Match to SM Yukawas: precision claim vs reality

The cover letter says "all nine charged-fermion Yukawas land within the standard Froggatt-Nielsen factor-of-a-few window." The README says "land within the Froggatt-Nielsen factor-of-a-few window of the PDG 2024 values."

The actual ratios from Table 5.1: $\{1.00, 1.08, 1.06, 0.33, 0.60, 0.51, 0.79, 0.11, 0.20\}$.

The largest residuals:
- **Muon: ratio $0.11$, off by factor of $\sim 9$.**
- **Electron: ratio $0.20$, off by factor of $\sim 5$.**

A factor of 9 is substantially worse than "factor-of-three" or "factor-of-a-few." Standard Froggatt-Nielsen analyses (Ross 2002, the Babu-Mohapatra reviews) achieve factor-of-2 accuracy on each Yukawa with their $C_p$ multipliers. The present pattern is achieving factor-of-2 to factor-of-9 depending on the fermion.

The paper's framing ("the four largest residuals define the empirical $C_p \in [0.11, 0.79]$ multiplier list expected from incomplete bosonic-substrate specification") is technically correct *if* the $C_p$ multipliers are absorbed as fittable parameters. But standard FN with $C_p$ multipliers absorbed as fittable parameters has 4 free parameters (3 FN charges + 1 scale + the $C_p$ list ≈ 5--9 parameters depending on counting). The present pattern's "$C_p$ multipliers absorbed" position has 1 free anchor + 1 free scale + 9 fittable $C_p$ multipliers = 11 free parameters, more than standard FN.

**Recommendation.** The paper should either:
(a) State honestly that the $C_p$ multipliers are 9 free fittable parameters in the current framework, with the load-bearing claim being only the integer-power assignment in Table 4.1; OR
(b) Derive the $C_p$ multipliers from substrate dynamics (the §7 "follow-up work" promise), in which case they should be in this paper, not deferred; OR
(c) Reframe as "this is a Tier-B partial fit," acknowledging the muon and electron residuals as failures of the bosonic-substrate-only ansatz.

The current framing oversells the precision.

### 3.4 The empirical hierarchy is reproduced "to factor-of-five precision"

§5 (Reading the fit) claims: "The full $5.5$ decades from $y_e = 2.9 \times 10^{-6}$ to $y_t = 0.93$ are covered to factor-of-five precision by the single $\lambda = 10/49$ scale acting on the representation-theoretic exponents."

Factor-of-five is correct *as the worst residual*. But "factor-of-five precision" is conventionally taken to mean "the typical residual is within a factor of 5," and that framing oversells what is typically factor-of-2 with one factor-of-9 outlier. Standard FN delivers factor-of-2 typical with no factor-of-9 outliers; the present model is *worse* than standard FN on the muon, despite using fewer assumed free parameters.

The honest framing: "for 5 of 9 charged Yukawas (top, charm, up, strange, tau) the prediction matches measurement at factor-of-2 or better; for 4 of 9 (bottom, down, muon, electron) the residuals reach factors of $\sim 2$--$9$."

### 3.5 Sterile neutrinos and the see-saw

§5 last paragraph predicts $y_{\nu_3} \approx 4.85 \times 10^{-9}$, $y_{\nu_2} \approx 9.91 \times 10^{-10}$, $y_{\nu_1} \approx 2.02 \times 10^{-10}$ at FN powers $\{12, 13, 14\}$, giving Dirac masses in the $m_\nu = y_\nu v/\sqrt{2}$ range of $\sim 0.05$--$0.85$ eV.

§7.3 acknowledges: "without a Majorana $\nu_R \cdot \nu_R$ mass term." A type-I see-saw would require introducing $M_R$, "the substrate origin of $M_R$ is one of the deepest open questions of the framework."

This is a serious limitation. Solar and atmospheric oscillation data require $\Delta m_{31}^2 \sim 2.5 \times 10^{-3}$ eV$^2$, $\Delta m_{21}^2 \sim 7.5 \times 10^{-5}$ eV$^2$, with $m_3 \sim 0.05$ eV (normal hierarchy) or larger (inverted). Without a see-saw, the predicted Dirac neutrino masses do *not* automatically reproduce these; they can only be tuned to match if the (unspecified) $M_R$ is chosen for each generation.

**Recommendation.** Either remove the sterile-neutrino prediction from this submission (it doesn't add to the charged-fermion result), or add a §6 with the see-saw mechanism developed (tier-classified appropriately). As is, the sterile-neutrino paragraph is a numerological match without a mechanism, which weakens rather than strengthens the paper.

### 3.6 The Cabibbo cube-root identity

§6 develops $\lambda_C \approx (Y_d/Y_u)^{1/3}$. The empirical $Y_d/Y_u = y_b/y_t \approx 0.024/0.93 \approx 0.026$, cube root $\approx 0.296$, vs $\lambda_C \approx 0.225$. The cube-root identity is off by $\sim 30\%$.

The paper claims this is "consistent with the substrate prediction $y_b/y_t = \lambda^3 = (10/49)^3 \approx 0.0085$, $\lambda_C \approx \lambda$." But the substrate prediction $y_b/y_t = 0.0085$ disagrees with the empirical $y_b/y_t = 0.026$ by a factor of $3$ (this is the bottom-quark factor-of-3 residual from the §3.3 fit). So the cube-root identity is being made consistent by *both sides* having $\sim 30\%$ residuals. The empirical $0.296$ does not match $0.225$, and the predicted $\lambda^3 = 0.0085$ does not match $0.026$; both are off by similar factors and the cube-root identity is approximately true on both sides.

This is fine as an order-of-magnitude observation, but the paper presents it as one of the load-bearing results ("The cube-root identity unifies four separate aspects of SM mixing/mass structure: ... All four follow from one substrate quantity $\lambda$..."). The unification is at factor-of-2 precision, not at the precision of CKM matrix elements (which are known to 1% or better).

**Recommendation.** Downgrade the cube-root identity to a structural observation. Defer the rigorous CKM matrix fit to the next-Sprint companion paper as the manuscript already plans. State explicitly that $\lambda^3 \approx 0.0085 \ne y_b/y_t \approx 0.026$ (factor of 3) and that this is the bottom-quark issue from §5.

### 3.7 Comparison to standard Froggatt-Nielsen

The cover letter and §5 claim the present model uses fewer free parameters than standard FN. Let me count carefully.

**Standard FN (Ross 2002, e.g.).** Three integer FN charges $X_Q$, $X_u$, $X_d$ (or generation-dependent $X_{Q_i}$, $X_{u_i}$, $X_{d_i}$ for 9 charges total in the most general case; or 3 charges if you assume universal flavour) + 1 flavon scale $\epsilon$ + $C_p$ multipliers (typically 9). Free parameters: 3 + 1 + 9 = 13 in the most general case, or potentially fewer if symmetry constraints reduce the FN charges.

**Present model.** 1 anchor ($y_t$) + 1 scale ($\lambda$, or 2 if you count $\lambda_{\rm ref}$ separately) + 9 forced powers (which are $d_p + \Delta_{\rm gen}$ with $d_p \in \{0,3,3\}$ partially derived, and $\Delta_{\rm gen}$ values in $\{0,2,3,4,6,7\}$ empirically tuned) + 9 $C_p$ multipliers (paper acknowledges these are not yet derived). Free parameters: 1 + 1 (or 2) + (3 free $\Delta_{\rm gen}$ assignments, since 3 are 0 for gen-3) + 9 = 14--15.

So the present model has *more* free parameters than standard FN with $C_p$'s, not fewer. The "zero free FN charges" claim is technically true (the $X_Q, X_u, X_d$ assignments are replaced by $V^{\otimes 5}$ SU(5) decomposition), but the 9 $\Delta_{\rm gen}$ values are themselves empirical assignments to $\sigma$-orbit positions.

**Recommendation.** Re-do the parameter accounting. State honestly that the present model trades the FN charges for $\sigma$-orbit position assignments, with the same total number of fittable parameters (or slightly more). The contribution is *not* "smallest free-parameter set"; the contribution is "the FN charges are reinterpreted as SU(5) representation indices on a $V^{\otimes 5}$ decomposition," which is a *different* framing rather than a *simpler* framing.

### 3.8 The verification primitive

I executed:

```python
from tig_dirac import predict_yukawa, LAMBDA_FN, Y_T_ANCHOR
assert LAMBDA_FN == 10/49
assert Y_T_ANCHOR == 0.93
r = predict_yukawa('up', 3); assert r['y_predicted'] == 0.93
r = predict_yukawa('lepton', 1); assert abs(r['y_predicted'] - 0.93*(10/49)**9) < 1e-12
```

All assertions pass. The function is 60 lines of `python` with a hardcoded power table:

```python
_YUKAWA_TABLE: dict[tuple[str, int], tuple[int, str]] = {
    ('up', 3):     (0, 't'),    ('up', 2):     (3, 'c'),    ('up', 1):     (7, 'u'),
    ('down', 3):   (3, 'b'),    ('down', 2):   (5, 's'),    ('down', 1):   (7, 'd'),
    ('lepton', 3): (3, 'tau'),  ('lepton', 2): (6, 'mu'),   ('lepton', 1): (9, 'e'),
    ('neutrino', 3): (12, 'nu_3'), ('neutrino', 2): (13, 'nu_2'), ('neutrino', 1): (14, 'nu_1'),
}
```

This is reproducible in the strict sense (the function returns what the manuscript says), but the integers $\{0,3,5,6,7,9\}$ are hardcoded — they are not computed from a substrate algorithm. The "substrate-derived" character is in the *claim* that these integers come from $V^{\otimes 5}$ + $d_p$ + $s_p$, not from any computational derivation in `predict_yukawa()` itself. This is the same status as J44's `predict_dark_sector()`: the computational primitive is solid, the structural claim is what §3.1 is about.

### 3.9 Lemma 2.1 is taken "as given" from the foundation paper [J16/J23]

§2 cites Lemma 2.1: "$V^{\otimes 5}$ partitions as $\mathbf{1} \oplus \bar{\mathbf{5}} \oplus \mathbf{10}$ (matter, $|S| \le 2$, 16 cells) $\oplus \bar{\mathbf{1}} \oplus \mathbf{5} \oplus \bar{\mathbf{10}}$ (antimatter, $|S| \ge 3$, 16 cells)."

This is cited from the foundation paper J16/J23 ("Discrete Dirac on the 4-core's $\mathbb{F}_5$-lift"). I do not have that paper to consult, but the structure deserves scrutiny: the SU(5) GUT decomposition $\mathbf{16} = \mathbf{1} + \bar{\mathbf{5}} + \mathbf{10}$ requires the algebraic action of $SU(5)$ on the 32-dimensional $V^{\otimes 5}$. Whether this action is canonically defined (i.e., whether the $V^{\otimes 5}$ structure carries an $SU(5)$ representation in the algebraic sense, or whether the binomial $1+5+10+10+5+1=32$ count merely *coincides* with the SU(5) GUT count) is an important load-bearing question.

**Recommendation.** Either summarize the $SU(5)$-action on $V^{\otimes 5}$ in a self-contained way in §2 (a paragraph or two would suffice), or reduce Lemma 2.1 to the binomial count statement and explicitly flag that the $SU(5)$ identification is the foundation paper's claim (with the "is-this-canonical" question as one of the open structural items).

### 3.10 Per-venue cap

The README §6 says "this is the **2nd** PRD paper this quarter (J44 was 1st)." If the J44 + J45 pair is being co-submitted to PRD, the editors will likely consolidate them (or assign coupled review). Recommend the cover letter explicitly request coupled review, since the two papers share the `tig_dirac.py` substrate primitive and the structural framework. Coupled review is reasonable; back-to-back independent submissions risk conflicting referee reports.

---

## §4 Minor comments

### 4.1 Author list (same issue as J44)

Cover letter: Sanders + Johnson. Manuscript title page: two `\author` blocks both saying "Sanders + Gish" with addresses for 7Site (brayden@7site.co) and Independent Researcher (hjj01986@gmail.com). The hjj01986 email belongs to Johnson, not Gish. Fix.

### 4.2 The "$T^*(1-T^*)$" derivation

§3 introduces $\lambda = T^*(1-T^*)$ as "the maximum-entropy variance of a Bernoulli-$T^*$ distribution." This is mathematically correct (variance of Bernoulli($p$) is $p(1-p)$) but the derivation reads as numerology because:
- Bernoulli variance is the *standard* variance of a 2-outcome distribution; calling it "max-entropy" is correct but misleading (it's also just "the variance," nothing about entropy maximization).
- Why is $\lambda$ supposed to equal a Bernoulli variance? The connection between "FN suppression scale" and "Bernoulli variance" is not motivated by SM flavor physics literature. It's an *observation* that $T^*(1-T^*) = 10/49 \approx 0.204$ matches the Wolfenstein scale.

**Recommendation.** Replace "Theorem 3.1 (Substrate-derived FN scale)" with an honest "Observation 3.1: $T^*(1-T^*) = 10/49$ is numerically close to the Wolfenstein parameter. We propose this as the substrate origin of the FN scale, conditional on the structural arguments of [J16/foundation]." Don't call this a theorem.

### 4.3 The "$\lambda = |\mathbb{Z}/10|/H^2 = 10/49$" rewrite

Theorem 3.1 also rewrites $\lambda = |\mathbb{Z}/10|/H^2 = 10/49$. The numerator is 10 (substrate size), the denominator is 49 (HARMONY squared). This is the same number written differently — $T^*(1-T^*) = (5/7)(2/7) = 10/49 = 10/H^2$. The dual interpretation is fine but the second form ($N/H^2$) lets you absorb the Bernoulli-variance reading and replace it with the "ratio of substrate size to harmony-squared" reading. Pick one; don't equivocate.

### 4.4 The Cabibbo cube-root identity, equation form

Eq. 6.1 is $\lambda_C \approx (Y_d/Y_u)^{1/3}$. The "$\approx$" symbol is correct given the factor-of-2 precision; please don't escalate this to "$=$" anywhere (which the paper doesn't, to its credit).

### 4.5 "Tier-B" tier classification

The README and abstract repeatedly tag claims as "Tier-A" (measured) or "Tier-B" (forced power + measured anchor). This is good discipline. Suggestion: define the tier system explicitly in §2 (or in a footnote), since PRD readers won't recognize the convention without explanation.

### 4.6 PDG 2024 vs PDG 2020 / running scales

§5 Table 5.1 reports "measured" Yukawas like $y_t = 9.30 \times 10^{-1}$, $y_b = 2.40 \times 10^{-2}$, etc. These are at the electroweak scale via $y = m \sqrt{2}/v$ with $v = 246$ GeV. The values are *running* Yukawas evaluated at $\mu = M_Z$ for quarks (via 4-loop QCD running) and pole masses for leptons. The choice of scale matters: at $M_Z$ vs at the GUT scale, the bottom Yukawa changes by a factor of $\sim 2$ due to running effects. The paper does not state the scale at which the measured values are taken. PDG 2024 quotes pole masses for top, MS-bar masses for the rest at varying scales.

For my independent check, with $m_b = 4.18$ GeV (pole), $m_b(M_Z) \approx 2.85$ GeV, the measured $y_b$ at $M_Z$ is $\sim 0.0164$, not $0.024$ as the paper states. The factor-of-3 ratio $0.33$ for the bottom changes if you use $y_b(M_Z)$ instead of $y_b$ at some other scale. The paper should state which scale and which definition.

(Note: other Yukawa values in Table 5.1 are roughly consistent with $M_Z$-scale running at a few-percent level, but the bottom value is ambiguous.)

**Recommendation.** State the renormalization scale (probably $M_Z$ or the GUT scale; pick one) and consistently use that scale's running Yukawas. The paper's "ratio" column changes meaningfully under this choice.

### 4.7 Suggested reviewers

Cover letter suggests "a flavour-physics theorist with experience in Froggatt-Nielsen models" — good. Also suggest "a phenomenologist with neutrino-oscillation expertise" since the §5 last paragraph and §7.3 raise the see-saw issue. The "algebraist with experience in finite non-associative algebras" for the foundation $V^{\otimes 5}$ structure makes sense as a co-reviewer.

### 4.8 The §1 abstract claim

"The pattern uses **zero free FN charges** (all integer powers are forced by the SU(5)-rep + sigma-orbit assignment) and **zero free flavon scales** (lambda = 10/49 is forced by the substrate T* = 5/7)..."

Per §3.1: this claim is too strong. The integer powers in Table 4.1 are constructed from the empirical hierarchy. Recommend: "The pattern reduces the FN charges of standard $U(1)_{FN}$ to representation indices on a $V^{\otimes 5}$ SU(5) decomposition, with the FN scale $\lambda$ derived from the substrate's coherence threshold $T^*$. The resulting integer powers are tabulated in Table 4.1."

### 4.9 The §4 paragraph on the $C_p$ multipliers

"The substrate's image of the non-associativity (the 1-dimensional associator span established in the foundation paper) carries the cost $\lambda^{d_p}$, with the exponent counting how many $\mathbf{10} \to \bar{\mathbf{5}}$ flips populate that one image dimension."

This is dense. The "1-dimensional associator span" needs at least a sentence of unpacking, and the relation "associator span carries cost $\lambda^{d_p}$" is asserted not derived. This is fine as a forward reference to the foundation paper but the exposition should be self-contained at the level of "this is what you need to know to follow Definition 4.1; the algebra is in [J16/J23]."

---

## §5 Independent verification

I executed:

```python
from tig_dirac import predict_yukawa, LAMBDA_FN, Y_T_ANCHOR
assert LAMBDA_FN == 10/49  # ✓
assert Y_T_ANCHOR == 0.93  # ✓
for p in ['up', 'down', 'lepton']:
    for g in [1, 2, 3]:
        r = predict_yukawa(p, g)
        # all 9 returns match Table 5.1 numerically
```

All 9 charged Yukawa predictions reproduce manuscript Table 5.1 exactly.

I also recomputed the $y^{\rm pred}/y^{\rm meas}$ ratios using independent PDG 2024 fermion masses and the standard $y = m\sqrt{2}/v$ with $v=246$ GeV:

| Particle | $n$ | Manuscript ratio | My ratio (PDG 2024 + $M_Z$ running where applicable) |
|---|---|---|---|
| top | 0 | 1.00 | 0.94 (top pole mass = 172.69 GeV → $y_t = 0.993$) |
| charm | 3 | 1.08 | 2.22 (charm $M_Z$ running $m_c \approx 0.62$ GeV → $y_c = 3.56\times 10^{-3}$) |
| up | 7 | 1.06 | 1.08 (up $\approx 2.2$ MeV → $y_u = 1.27 \times 10^{-5}$) |
| bottom | 3 | 0.33 | 0.48 ($m_b(M_Z) = 2.85$ GeV → $y_b = 1.64\times 10^{-2}$) |
| strange | 5 | 0.60 | 1.00 ($m_s(M_Z) = 57$ MeV → $y_s = 3.28\times 10^{-4}$) |
| down | 7 | 0.51 | 0.51 |
| tau | 3 | 0.79 | 0.77 |
| muon | 6 | 0.11 | 0.11 |
| electron | 9 | 0.20 | 0.19 |

The manuscript and my recomputation agree on the small-Yukawa ratios (down, electron, tau, muon, up) but disagree on the heavy-quark ratios (charm, bottom, strange) where running effects are significant. This *could* improve the bottom-quark fit (from $0.33$ to $0.48$, less bad) but worsens the charm fit ($1.08 \to 2.22$, factor of 2 off).

The manuscript's choice of "measured" Yukawa values needs to be sourced and the renormalization scale stated (§4.6).

---

## §6 Stronger contributions, not at issue

- **The numerical observation** that $\lambda = 10/49 \approx 0.204$ and integer powers thereof generate the 5.5 decades of charged-fermion Yukawa hierarchy is a real observation. It's a 1-parameter (or 2-parameter with $\lambda_{\rm ref}$) compact representation of 9 numbers.
- **The verification primitive** (`predict_yukawa(particle, generation)`) is well-designed: clean function signature, rich return dictionary, exact rationals for $\lambda$, explicit tier classification.
- **The "honest scope"** in §1 ("we do not claim, and the data does not support, percent-level agreement on every Yukawa") is the right framing. It's then undermined by the cover letter's "factor-of-a-few window" claim, but the manuscript itself is more honest than the cover letter.

---

## §7 Recommended action

1. **Rewrite the abstract and §1** to remove the "zero free FN charges" claim and the "factor-of-a-few" / "factor-of-five precision" framings. State the actual residual range honestly: "$y^{\rm pred}/y^{\rm meas}$ ratios in $[0.11, 1.08]$, with 5 of 9 in the conventional FN factor-of-2 window and 4 of 9 with residuals up to factor of 9."

2. **Re-do the parameter accounting** (§3.7 above). State the present framework's free-parameter count compared to standard FN; do not claim "smallest free-parameter set."

3. **Fix the author list** (cover letter vs manuscript).

4. **State the renormalization scale** for the measured Yukawas in Table 5.1 and consistently use that scale's running values.

5. **Either remove or develop** the sterile-neutrino prediction. As is, it's a Dirac-mass numerological match without a see-saw mechanism, which is incompatible with neutrino oscillation phenomenology.

6. **Either remove or develop** the Cabibbo cube-root identity. As is, it's a factor-of-2 observation across multiple loose-tolerance equations.

7. **Reframe Theorem 3.1 as Observation 3.1.** The $\lambda = T^*(1-T^*) = 10/49$ is a chosen identification; the "max-entropy Bernoulli variance" framing reads as numerology.

8. **Either co-submit with J44** (request coupled review) or stagger them. Per-venue cap and shared substrate primitive argue for coupled review.

9. **Acknowledge the $\lambda$ vs $\lambda_{\rm ref}$ duality** transparently. The framework uses two values of $\lambda$; this should be in the abstract.

10. **Self-contained §2** for the $V^{\otimes 5}$ SU(5) decomposition; do not require [J16/J23] for the Lemma 2.1 statement.

---

## §8 Score sheet

| Criterion | Score (1--5) | Comment |
|-----------|-------|---------|
| Numerical accuracy of stated computational claims | 5 | `predict_yukawa()` reproduces Table 5.1 exactly |
| Strength of "forced powers" claim | 2 | Powers are read off empirical hierarchies and labeled with $\sigma$-orbit indexing |
| Quality of fit to PDG | 2 | 5 of 9 within factor-of-2; 4 of 9 with residuals up to factor of 9 |
| Honest scope (manuscript) | 4 | §1 honest scope paragraph is good; many open questions explicitly flagged |
| Honest scope (abstract / cover letter) | 2 | "Zero free FN charges," "factor-of-a-few," "smallest free-parameter set" all overclaim |
| Reproducibility | 5 | One-line primitive + manuscript table reproduces |
| Novelty for flavour physics | 3 | The $\lambda = 10/49$ observation is novel; the FN-power assignment is a re-encoding |
| Fit for PRD | 2 | The empirical residuals (factor-of-9 muon) and the missing see-saw weaken the case; PRD will want stronger structural derivations or smaller residuals |
| Internal consistency (author lists, $\lambda$ vs $\lambda_{\rm ref}$) | 2 | Author list mismatch; "single $\lambda$" framing contradicts Remark 3.2 |

**Recommendation:** Major revisions, with the abstract rewrite, parameter-accounting redo, and renormalization-scale specification as the first-priority items. The numerical observation ($\lambda = 10/49$ with integer powers covering the SM Yukawa hierarchy) is real and worth publishing in some form, but the present framing oversells the precision and the "forced" character of the integer powers. After honest reframing this could be a clean PRD paper.
