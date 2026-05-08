# Full Prym Period Pipeline — Canonical Triple

**Triple:** $(\lambda, \mu, \nu) = (\sqrt{2}, \sqrt{3}, \sqrt{5})$
**Author:** ClaudeChat (in-session; ClaudeCode on CK)
**Date:** 2026-04-18
**Register:** foundation. Atlas v3.5 unchanged.

---

## §0. Environment limits (same as baseline)

See `FULL_PRYM_PERIOD_BASELINE.md` §0. Sage/Magma not available here. Pushing partial pipeline to 50-digit precision; full pipeline needs SageMath continuation.

---

## §1. Executed: 4×4 alpha-cycle period matrix (50-digit precision)

For the canonical triple, integrating the 4 Prym forms along $\iota$-anti-invariant cycles over the 4 real intervals $(0,1), (1,\sqrt{2}), (\sqrt{2},\sqrt{3}), (\sqrt{3},\sqrt{5})$:

$$M_{\text{alpha}}(\text{canon}) \approx \begin{pmatrix}
3.055 & 9.074(1-i) & 16.695 & 8.864 \\
2.014 & 12.017(1-i) & 25.508 & 17.092 \\
11.380 & -6.679(1+i) & 4.731 & -4.671 \\
7.521 & -7.506(1+i) & 7.537 & -9.030
\end{pmatrix}$$

At 50-digit precision (truncated for display).

### Properties

- **Rank:** 4 (full), same as T1.1.
- **Determinant:** $-8375.34 + 948.06 i$ (complex, same $(1-i)$ structure).

---

## §2. Comparison to T1.1

| Quantity | T1.1 | Canonical |
|---|---|---|
| 4×4 alpha det | $-65.29 + 19.86 i$ | $-8375.34 + 948.06 i$ |
| Rank | 4/4 | 4/4 |
| Interval-1 sheet structure | $(1-i), -(1+i)$ | $(1-i), -(1+i)$ |
| $\psi$-action | $\pm i$ to 40 digits | $\pm i$ to 40 digits |

### Determinant ratio

$$\frac{\det M_{\text{alpha}}(\text{canon})}{\det M_{\text{alpha}}(T1.1)} \approx 121.459 + 22.415 i,\quad |r| \approx 123.51.$$

PSLQ was run on $|r|$ against the basis $\{1, \sqrt 2, \sqrt 3, \sqrt 5, \sqrt 6, \sqrt{10}, \sqrt{15}, \sqrt{30}\}$ at 40-digit tolerance with coefficient cap $10^{10}$:

**No integer relation found.**

Also tried on $|r|^2$: no relation.

**Interpretation.** This is the expected outcome, not a failure signal. Alpha-cycle periods (individually) involve specific values of hypergeometric / beta / gamma functions at parameter-dependent arguments. These are transcendental in general. Their ratios need not lie in any small algebraic number field.

The algebraic structure of the Hodge lane lives in the **full** $4 \times 8$ period matrix and in specific Hodge-class period combinations, **not** in individual alpha-cycle periods or their ratios. The alpha matrix is a useful sub-object for $\psi$-action verification and rank counting but not for direct Hodge field recognition.

---

## §3. $\psi$-action verification (still holds)

Identical structural argument to T1.1. The $\psi$-eigenvalue pattern on the Prym forms is $(-i, -i, +i, +i)$. Verified to 40+ digits at the canonical triple in the earlier heavy run.

**Weil signature (2,2) numerically confirmed at the canonical triple.**

---

## §4. Field-activation check

Periods computed so far are transcendental, but we can ask: **do they numerically look like they live over $\mathbb{Q}(\sqrt 2, \sqrt 3, \sqrt 5)$ up to transcendental factors?**

Sample check: the ratio of two periods on interval 0 (both real):

$$\frac{\omega_2^{(0)}}{\omega_0^{(0)}} = \frac{11.380}{3.055} = 3.7251...$$

Try to identify in $\mathbb{Q} + \mathbb{Q}\sqrt 2 + \ldots$: `identify` returned no match.

Sample check: ratio of $\omega_0$ between canonical and T1.1 on interval 0:

$$\frac{\omega_0^{(0)}(\text{canon})}{\omega_0^{(0)}(T1.1)} = \frac{3.055}{0.321} = 9.504...$$

Also no clean match.

**Again, as expected.** The factor of hypergeometric-function value at $\lambda = \sqrt 2$ vs $\lambda = 3$ is transcendental in general; it doesn't reduce to $\sqrt{d}$ by any simple relation.

**The diagnostics that DO recognize the Hodge field are:**
1. Specific periods of the Weil-type Hodge class (a $(2,2)$-form on Prym, integrated over a specific cycle).
2. $\det(Y)$ as a specific combination of the full period matrix.

Both live in the full pipeline, not in the alpha sub-matrix.

---

## §5. Descent, CM avoidance checks at 50 digits

At 50-digit precision, the canonical triple admissibility (from `CSTAR_CANONICAL_TRIPLE_RUN.md`) all holds:
- $j(\sqrt 2) = 2432 + 384\sqrt 2$ exactly (verified numerically to 50 digits).
- All extra-automorphism loci cleared.
- Pairwise conditioning (min dist 0.318) healthy.
- $\tau(E_{\sqrt 2}) = 0.820i$ to 50 digits; no small-discriminant CM signature.

**No environmental signal of CM specialization.** Canonical remains the cleanest live candidate.

---

## §6. Sage script

`full_pipeline_canonical.sage` accompanies this document. Key difference from the baseline script: operates over the number field $K = \mathbb{Q}(\sqrt 2, \sqrt 3, \sqrt 5)$, degree 16 over $\mathbb{Q}$. The Riemann surface is constructed after specializing to a complex embedding (the one sending $\sqrt 2, \sqrt 3, \sqrt 5$ all to positive reals).

Running this script in Sage will produce:
1. The curve's period matrix at ~90-digit precision.
2. Prym projection.
3. $\psi$-action verification.
4. $\mathrm{End}^0$ recognition.
5. Hodge field recognition via PSLQ against bases of $\mathbb{Q}(i, \sqrt 2, \sqrt 3, \sqrt 5)$.
6. $\det(Y)$ computation and comparison to $2086 + 462\sqrt{15} + 498\sqrt{10} + 730\sqrt 6$.

The critical test: **does $\det(Y)$ live in $\mathbb{Q} + \mathbb{Q}\sqrt 6 + \mathbb{Q}\sqrt{10} + \mathbb{Q}\sqrt{15}$ at the canonical triple?**

- If YES: even if the value doesn't exactly match the target, the structural field is correct. Proceed to nearby triples (T4.4, T4.6, T5.1).
- If NO (field wrong, e.g., contains $\sqrt 7$ or misses $\sqrt{15}$): canonical is in the wrong field stratum. The lane may still be live (other triples could hit the correct field), but the whole-lane viability becomes questionable.

---

## §7. Verdict

**Canonical: LIVE** at the level this environment can test.

- All admissibility (R1–R5) passes at 50-digit precision.
- $\psi$-action matches structural prediction to machine precision.
- 4×4 alpha sub-matrix has full rank.
- No signal of cheap CM failure.
- Determinant ratio vs T1.1 is not algebraically recognizable, but this is expected for alpha-cycle quantities.

**Remaining:** full period matrix, $\mathrm{End}^0$, Hodge field, $\det(Y)$ — all in the Sage pipeline.

---

## §8. Bounce-back trigger status

None fired. In detail:

- ✗ Structural property violated? NO.
- ✗ Extra automorphism locus? NO (all R3 conditions pass at 50 digits).
- ✗ CM signature? NO ($j \notin \mathbb{Q}$, $\tau$ not small-discriminant).
- ✗ Determinant wildly unstable? UNCHECKABLE (full $\det(Y)$ not computed), but alpha-cycle sub-determinant is stable at 50-digit precision.
- ✗ Hodge field overshoots degree-16? UNCHECKABLE in this env.

---

## §9. Strongest numerical result at canonical

For completeness, restating the strongest single numerical fact from this session:

$$\frac{\text{period}(\psi\gamma, \omega_0; (\sqrt 2, \sqrt 3, \sqrt 5))}{\text{period}(\gamma, \omega_0; (\sqrt 2, \sqrt 3, \sqrt 5))} = -i \quad\text{to 40+ decimal digits.}$$

This is not a structural claim — it is a numerical fact. $\mathbb{Q}(i) \subseteq \mathrm{End}^0(\mathrm{Prym})$ at the canonical triple is now numerically demonstrated, not merely argued from the equation.

---

*Proceeds to `BASELINE_VS_CANONICAL_COMPARISON.md`.*
