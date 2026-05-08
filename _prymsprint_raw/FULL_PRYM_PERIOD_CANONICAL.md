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

## §10. Update 2026-04-19 — attempted det(Y) via local mpmath build

### §10.1 Sage path: closed

Sage `RiemannSurface.period_matrix` was attempted on Google Colab with this curve.

- Initial run: 10+ hours, hung with zero output, killed.
- Armored retry A at `prec=200` (watchdog, unbuffered stdout, `stdbuf -oL`): hung 20 min at `period_matrix`, watchdog killed.
- Retry B at `prec=53` (changed `PREC = 200` → `PREC = 53`, grep confirmed): still no output after 60 s at `period_matrix`.

**Diagnosis:** the hang is topology-dominated, not precision-dominated. Sage's `RiemannSurface` (intended primarily for $y^2 = f$) stalls on the specific superelliptic ramification of $y^4 = x(x-1)(x-\sqrt 2)^3(x-\sqrt 3)^2(x-\sqrt 5)^2$ (gcd pattern 1,1,3,2,2,3 at the six branch points). Abandoned.

### §10.2 Local mpmath attempt: `prym_compute.py`

Written from scratch (300 LOC) at `mp.dps = 60`. Strategy:

- 4 Prym forms (odd-j): $\omega_0 = dx/y$, $\omega_1 = x\,dx/y$, $\omega_2 = (x-\lambda)^2(x-\mu)(x-\nu)\,dx/y^3$, $\omega_3 = x(x-\lambda)^2(x-\mu)(x-\nu)\,dx/y^3$.
- 4 $\alpha$-cycles: doubled real intervals $[0,1], [1,\sqrt 2], [\sqrt 2, \sqrt 3], [\sqrt 3, \sqrt 5]$ (factor 2 from sheet-0 + sheet-2 reverse).
- 4 $\beta$-cycles: doubled UHP box contours at height $H=4$, between $\iota$-fixed branch-point pairs $(0, \sqrt 2)$, $(0, \sqrt 3)$, $(1, \sqrt 3)$, $(1, \sqrt 5)$.

**Numerical caveat (fixed):** initial `EPS = 1e-50` caused tanh-sinh endpoint evaluation to produce $|f|^{-1/4} \sim 10^{12}$, poisoning the first 2 digits of alpha periods (got $-9688 + 1022i$ vs baseline's $-8375 + 948i$). After `EPS = 1e-5`, alpha-matrix matches `extended_heavy.py` exactly: $\det A = -8375.337\ldots + 948.056\ldots\,i$.

### §10.3 Result — non-symplectic basis, as baseline §3 predicted

With the corrected alpha matrix and the 4 UHP beta contours:

- $\det A$ nonzero ✓ (alpha sub-matrix is a valid rank-4 basis)
- $\max |\tau - \tau^T| = 2.139$ — **structurally asymmetric**, not a rounding issue
- $\text{Im}\,\tau$ has signature $(2, 2)$ — **not positive-definite**, Riemann bilinear positivity fails
- $\det(\text{Im}\,\tau) = 0.01297$ — ratio to target $7238.26$ is $1.79 \times 10^{-6}$, not a clean factor
- PSLQ against $\{1, \sqrt 6, \sqrt{10}, \sqrt{15}\}$ and $\{1, \sqrt 2, \sqrt 3, \sqrt 5, \sqrt 6, \sqrt{10}, \sqrt{15}, \sqrt{30}\}$: no integer relation.

**Interpretation.** The 8 cycles I chose are topologically closed on the Prym (each is $\gamma_0 - \gamma_2$ between branch-point endpoints, which automatically closes because sheets 0 and 2 merge at ramified points) and linearly independent ($\det A \neq 0$), but they do not form a **symplectic basis** for $H_1(P, \mathbb{Z})$ with respect to the intersection form. Under a non-symplectic integer basis, $A^{-1}B$ is not the canonical $\tau$ — it is some other matrix related to $\tau$ by a non-symplectic $\text{GL}(8, \mathbb{Z})$ transformation, which in general destroys both symmetry and the positivity of the imaginary part.

This is **exactly the failure mode baseline §3 predicted**: *"Rolling my own and trusting the output at 50-digit precision is unrealistic in a session of this length — a single cycle-basis bug would poison the entire downstream diagnostic."*

### §10.4 Methodological options

To get the canonical $\det(Y)$, we need one of:

1. **Symplectic normalization from Riemann bilinear constraints.** Given our (non-symplectic) $\Pi = (A \mid B)$, write the constraint $\Pi \cdot E \cdot \Pi^T = 0$ as a linear system on the $8 \times 8$ skew-symmetric integer intersection form $E$ (28 unknowns, 20 real constraints → 8-dim affine family); intersect with the integer lattice via LLL; select the principal-polarization element (minimal det $E$); find $M \in \text{GL}(8, \mathbb{Z})$ with $M^T E M = J$; $\tau_{\text{canon}} = (\Pi M)_B \, (\Pi M)_A^{-1}$. Estimated effort: 300–500 LOC, half a day careful.

2. **Tretkoff–Tretkoff (1984) or Molin–Neurohr (2017) constructive symplectic basis** for superelliptic covers. Either algorithm gives a combinatorial cycle diagram, then explicit integer intersection matrix, then Pi in the correct basis by construction. Estimated effort: 400–700 LOC, full day.

3. **`abelfunctions` Python package** (Swierczewski, UW). Handles the Molin–Neurohr step natively. Not currently installed (`pip install abelfunctions` may or may not succeed on current Python — historically Python 2.7 only, some forks exist). Worth trying first before hand-rolling.

4. **MAGMA `AnalyticJacobian`** — cleanest tool for this specific curve shape, but paid license, not available in current environment.

5. **Parameter-perturbation proxy** — if the target $\det(Y) = 2086 + 462\sqrt{15} + 498\sqrt{10} + 730\sqrt 6$ is a Hodge-field-carrier invariant, nearby triples $(\sqrt 2 + \varepsilon_1, \sqrt 3 + \varepsilon_2, \sqrt 5 + \varepsilon_3)$ with varying $\varepsilon_i$ should give continuously varying $\det(Y)$. Evaluating WITHOUT a symplectic basis still gives *some* matrix invariant; checking whether that invariant is continuous across the Hodge locus could give indirect evidence. Not a proof, but a triage.

### §10.5 Written artifacts from this attempt

- `prym_compute.py` — the 300 LOC local pipeline (complete, deterministic, EPS-corrected)
- `prym_compute_out.txt` — first run (EPS=1e-50, alpha periods off by 8%)
- `prym_compute_out_v2.txt` — corrected run (alpha matches baseline, tau non-symmetric confirmed)
- `diagnose_asym.py` + stdout — entrywise asymmetry + Im-tau eigenvalue signature

### §10.6 Pending methodological decision

The user's directive was *"keep going don't stop unless you need help"*. This is the point where help is genuinely needed: the cycle-basis problem is the **same** one baseline §3 flagged, and solving it requires a substantive algorithm (options 1–5 above) rather than another quick numerical pass. The quick paths (Sage, EPS fix) have been exhausted.

**Atlas status unchanged.** Canonical remains *"live candidate"* at foundation register; the $\det(Y)$ atlas-promotion criterion remains pending a proper symplectic basis.

### §10.7 Option 1 (LLL symplectic normalization) — exhausted

**User directive (carried from prior session):** *"3 1 2 5 and then we can pay for something if we really need to only!"*
(Method waterfall: 3=`abelfunctions`, 1=LLL-Riemann, 2=Tretkoff–Tretkoff, 5=parameter perturbation, last resort=MAGMA.)

Option 3 was ruled out upstream (`abelfunctions` installation failure on current Python). This section documents the exhaustive attempt at Option 1.

#### 10.7.1 Setup

At `mp.dps = 60`, the 12 × 28 real constraint matrix $C$ (six index pairs $p<q$ in $\{0,1,2,3\}$, each giving one real + one imaginary row) was built directly from the high-precision $\Pi$ in `prym_compute_out_v2.txt`:

$$C_{pq,(i,j)} \;=\; \Pi_{p,i}\,\Pi_{q,j} - \Pi_{p,j}\,\Pi_{q,i}, \qquad (i,j) \in \binom{\{0,\ldots,7\}}{2}.$$

Singular values of $C$ (sanity check):

| $\sigma_0$ | $\sigma_5$ | $\sigma_{11}$ |
|---|---|---|
| $1.451\times10^{3}$ | $\sim 1.5\times10^{2}$ | $12.53$ |

All 12 singular values are $\mathcal O(1)$ — **$C$ is well-conditioned**, so the null space is geometric, not a precision artifact.

#### 10.7.2 Three escalating LLL runs

Each run built a lattice $B$ whose short vectors are integer $e \in \mathbb Z^{28}$ (or $D \in \mathbb Z^{16}$ for the cross-block) with $S \cdot C \cdot e$ small. A genuine integer intersection form would produce $C \cdot e = 0$ exactly, so $\|S \cdot C \cdot e\| \ll \|e\|$ for all $S$.

| Run | Form | Unknowns | Scale $S$ | LLL $\delta$ | Min $\|e\|$ / $\|D\|$ |
|---|---|---|---|---|---|
| A | full 28-dim skew | 28 | $10^{12}$ (double prec) | $3/4$ | $\sim 10^{6}$ |
| B | full 28-dim skew | 28 | $10^{20}$ (mpmath 60) | $3/4$ | $\sim 2.4 \times 10^{9}$ |
| C | cross-block $E=\begin{pmatrix}0&D\\-D^T&0\end{pmatrix}$ | 16 | $10^{30}$ | $3/4$ | $\sim 3.8 \times 10^{23}$ |
| D | cross-block | 16 | $10^{50}$ | $99/100$ | $\sim 4.0 \times 10^{38}$ |

In every run the "residual" part $S\cdot C\cdot e$ stayed at the $S$-scaled noise floor ($\sim 10^{-11}$ in scaled units), and the integer part grew **in lockstep with $S$**. This is the unmistakable LLL signature of **no short integer null vector existing in the chosen basis** — the algorithm is not stuck; it is correctly reporting that the minimum-norm integer $e$ with $C \cdot e = 0$ has entries of order at least $10^{9}$.

Run D even with $\delta = 99/100$ (maximal-quality LLL, much slower, essentially BKZ-competitive for this dimension) confirms the same scaling.

#### 10.7.3 Geometric interpretation

The 8 cycles chosen in §10.2 (4 real intervals $[0,1], [1,\sqrt2], [\sqrt2,\sqrt3], [\sqrt3,\sqrt5]$ as $\alpha$'s; 4 doubled UHP contours between $\iota$-fixed pairs as $\beta$'s) span an **extremely high-index sublattice** of $H_1(P, \mathbb Z)$. The integer intersection form $E$ expressing the true topological intersections in *this* basis has entries $\gtrsim 10^{9}$. LLL cannot recover such vectors from 12-row constraints at any reasonable scale — its success region in 28 dimensions is $\|e\| \lesssim 2^{28/4} \approx 128$, and with only $28 - 12 = 16$ null directions, it is nowhere near the needed magnitude.

**Option 1 is conclusively dead.**

#### 10.7.4 Pivot to Option 2 (Tretkoff–Tretkoff)

Per the waterfall, Option 2 is the next free path. The prerequisite monodromy data for $y^4 = x(x-1)(x-\sqrt2)^3(x-\sqrt3)^2(x-\sqrt5)^2$ was established in-session:

- Branch points $\{0, 1, \sqrt2, \sqrt3, \sqrt5, \infty\}$.
- Local monodromy $\sigma_i \in \mathbb Z/4$: multiplicities at each root $\in \{1, 1, 3, 2, 2\}$ give $\sigma \in \{1, 1, 3, 2, 2\}$ at the finite points; $\sigma_\infty = 3$ (from $\deg f = 9 \equiv 1 \pmod 4$, so $\sigma_\infty \equiv -1 \equiv 3$).
- Sum: $1 + 1 + 3 + 2 + 2 + 3 = 12 \equiv 0 \pmod 4$ ✓ (monodromy closes, required for a $\mathbb Z/4$ cover to exist).
- Riemann–Hurwitz: $2g - 2 = 4 \cdot (-2) + \sum (4 - \gcd(\sigma_i, 4)) = -8 + (3+3+3+2+2+3) \cdot 16 \cdot …$ (checked separately) gives $g = 5$ ✓.
- $\iota$ fixed points: 8 (including $x=\infty$), consistent with bielliptic quotient of genus 1.

Tretkoff–Tretkoff's algorithm will:
1. triangulate $\mathbb{CP}^1 \setminus \{\text{branch points}\}$ with a base point,
2. lift each edge to the 4-sheeted cover according to $\sigma_i$,
3. produce a combinatorial cycle diagram with **explicit integer intersection numbers** $\pm 1$ by construction,
4. yield a Smith-normal-form reduction to a $J = \begin{pmatrix}0 & I_5 \\ -I_5 & 0\end{pmatrix}$ symplectic basis on $H_1(X, \mathbb Z)$, restricted to the Prym via the $-1$ eigenspace of $\iota_*$.

Estimated effort: 400–700 LOC, full day of careful implementation.

#### 10.7.5 Option 5 as parallel triage

While Option 2 is being built, Option 5 (parameter perturbation) remains cheap and informative:
- Evaluate $\det(Y_{\text{mine}})$ at $(\sqrt2 + \varepsilon, \sqrt3, \sqrt5)$, $(\sqrt2, \sqrt3 + \varepsilon, \sqrt5)$, $(\sqrt2, \sqrt3, \sqrt5 + \varepsilon)$ for $\varepsilon \in \{10^{-3}, 10^{-2}, 10^{-1}\}$.
- If $\det(Y_{\text{mine}})$ varies *continuously* but not *smoothly* in the predicted target direction, that is indirect evidence the target formula describes a *different* invariant (on a symplectic basis) than the one our non-symplectic basis computes.
- Cost: one perturbed run of `prym_compute.py` per point, $\sim 2$ min each.

#### 10.7.6 Artifacts from Option 1 exhaustion

- `lll_intersection.py` — Run A, double-precision 28-dim LLL
- `lll_intersection_highprec.py` — Run B, mpmath-60 28-dim LLL
- `lll_crossblock.py` — Runs C/D, cross-block 16-dim LLL (Python-int Laplace determinant replacing int64 reshape)
- `lll_hp_out_S20.txt` — captured stdout of Run B (28 reduced vectors, all $\|e\|\sim 10^{9\text{–}10}$)

**Atlas status unchanged.** Canonical remains *"live candidate"*; Option 2 is the next free attempt; MAGMA stays the last-resort paid path.

### §10.8 Option 5 (parameter perturbation triage) — results

`perturb_det_Y.py` at `mp.dps = 40`, same non-symplectic basis as §10.2, seven evaluations.

| Point | $\det(A)$ | $\det(Y)$ | $\mathrm{diag}(Y)$ signs |
|---|---|---|---|
| baseline $(\sqrt 2, \sqrt 3, \sqrt 5)$ | $-8375.34 + 948.06\,i$ | $+0.01297$ | $[-1, +1, -1, +1]$ |
| $\lambda + 10^{-2}$ | $-8447.98 + 946.44\,i$ | $+0.04660$ | $[-1, -1, -1, +1]$ |
| $\lambda + 10^{-1}$ | $-9353.24 + 914.42\,i$ | $+0.08642$ | $[-1, -1, -1, +1]$ |
| $\mu + 10^{-2}$ | $-8259.67 + 973.93\,i$ | $+0.51276$ | $[+1, -1, -1, +1]$ |
| $\mu + 10^{-1}$ | $-7422.59 + 1172.07\,i$ | $+0.07951$ | $[-1, -1, -1, +1]$ |
| $\nu + 10^{-2}$ | $-8237.81 + 918.39\,i$ | $+0.05579$ | $[-1, -1, -1, +1]$ |
| $\nu + 10^{-1}$ | $-7155.61 + 697.23\,i$ | $-0.16820$ | $[-1, -1, -1, +1]$ |

Observations:

1. **The diagonal-sign pattern flips at every single perturbation.** The baseline $(-, +, -, +)$ is a signature-$(2,2)$ pattern; $\lambda+10^{-2}$ and $\mu+10^{-1}$ and both $\nu$ perturbations land on $(-, -, -, +)$ (signature $(1,3)$); $\mu+10^{-2}$ lands on $(+, -, -, +)$ (a third signature). A properly Prym-normalized $\operatorname{Im}\tau$ is positive-definite by Riemann bilinear positivity, so ALL diagonal entries must be positive. None of our points (including baseline) have that property.

2. **$\det(Y)$ goes negative at $\nu + 10^{-1}$.** In a true principal polarization $\det(\operatorname{Im}\tau) > 0$; our non-symplectic basis does not preserve even the sign of the invariant.

3. **The rate of change is wildly non-uniform.** $d\det(Y)/d\mu \approx 50$ at $\varepsilon = 10^{-2}$ but drops to $0.67$ at $\varepsilon = 10^{-1}$, indicating a **near-singularity** in the basis at the canonical point — consistent with an eigenvalue of $\operatorname{Im}\tau_{\text{sym}}$ crossing zero.

4. **$\det(Y)$ at baseline, $0.01297$, does NOT lie on a smooth curve connecting it to the target value $7238.26$.** Perturbations $10^{-2}$ to $10^{-1}$ away span the range $[-0.17, +0.51]$ — four orders of magnitude below target, with no sign of trending upward. The target is not recoverable from our basis by small perturbation.

**Conclusion.** The cycle basis chosen in §10.2 is topologically well-defined (cycles are closed) but **numerically unstable at the canonical point**. The signature flips and near-singular derivative confirm that the $\mathrm{GL}(8, \mathbb Z)$ transformation connecting our basis to a symplectic basis is itself discontinuous as $(\lambda, \mu, \nu)$ varies, i.e. we are *crossing a wall* in the moduli space of bielliptic genus-5 curves where the intersection form changes its Smith-normal-form shape. No amount of quadrature precision fixes this — we need the cycles themselves reconstructed from ramification data.

Option 5 is therefore *not* a proxy for the target — it is a diagnostic, and the diagnostic says: **build Option 2**.

### §10.9 Option 2 — Tretkoff–Tretkoff implementation plan

Full implementation plan written to `_prymsprint_raw/TRETKOFF_PLAN.md`. Summary:

1. Cell-decompose $\mathbb{CP}^1$: base point $P_0$ + 6 radial edges to branch points; obtain Tretkoff cyclic ordering.
2. Lift each edge to the 4-sheeted cover ($4 \times 6 = 24$ lifted edges).
3. Enumerate the $8g = 40$ Tretkoff cycles; their $\pm 1$ intersection numbers come **by construction** (no LLL, no integer recovery).
4. Smith normal form of the $40 \times 40$ skew integer matrix → polarization type $(d_1, \ldots, d_5)$; unimodular $M$ takes cycles to a symplectic basis.
5. Integrate the 4 Prym differentials along the new basis using existing quadrature infrastructure from `prym_compute.py`.
6. Project onto the $\iota$-antiinvariant subspace (Prym): $\pi_- = (1 - \iota_*)/2$ with $\iota_* : k \mapsto k+2 \pmod 4$ on sheets.
7. Normalize $\tau_P = A_P^{-1} B_P$ (now genuinely symmetric + positive-definite by construction).
8. $\det(\operatorname{Im}\tau_P)$ → PSLQ against $\{1, \sqrt 6, \sqrt{10}, \sqrt{15}\}$ → compare to target.

Estimated LOC: 400–700. Estimated time: one focused session.

**Atlas status.** Canonical still *"live candidate"*. Promotion criterion: Option 2 produces $\det(\operatorname{Im}\tau_P) = 2086 + 462\sqrt{15} + 498\sqrt{10} + 730\sqrt 6$ to $\geq 30$ digits via PSLQ, or falsifies it.

### §10.10 Tooling survey — what exists as of 2026-04

A dedicated research pass (sub-agent, 112 s, 21 tool calls) mapped the open-source landscape:

| Tool | Status on this Windows machine |
|---|---|
| `abelfunctions` (Swierczewski, github.com/abelfunctions/abelfunctions) | **fails to install** — Cython/MSVC compile failures (GitHub issues #137, #142, unresolved since Python 3 transition) |
| `passagemath` (pip-installable SageMath fork) | ships the same `RiemannSurface` class that already hung on us — no improvement |
| `cypari2` (PARI/GP binding) | **fails to install** — Cython compile failure |
| `python-flint 0.8.0` | **installed successfully** via pre-built wheel — provides Arb primitives (`acb`, `acb_mat`, `fmpz_mat`, Smith normal form, polynomial root-finding); does NOT include Riemann-surface algorithms |
| `nbruin/RiemannTheta` | evaluates $\vartheta(z, \tau)$ given $\tau$; does not *compute* $\tau$. Irrelevant here |
| PARI/GP 2.17 `hyperellPeriods` | implements **m=2 only**; not m=4 |
| **`hcperiods`** (Molin, github.com/pascalmolin/hcperiods) | **the recommended tool** — C + Arb, general $y^m = f(x)$, Tretkoff-84 internally, thousands-of-digits precision, produces symplectic basis by construction. Requires Arb ≥ 2.12. Build needs MinGW / MSVC + Arb+FLINT+MPFR install — **~2 hours of Windows build-env work** OR WSL/Linux (~10 min) |
| MAGMA `AnalyticJacobian(f, 4)` | paid license — not currently available |

### §10.11 Correct reading of Molin–Neurohr 2017 — no Prym shortcut exists

**Retraction of the §6 Prym-shortcut claim.** A first research pass suggested that §6 of Molin–Neurohr contains a direct Prym block decomposition. Direct reading of the paper text (extracted to `molin_neurohr.txt`, 2862 lines) shows this is **false**:

- §6 is titled "Numerical integration" and contains only the double-exponential change of variables (Theorem 6.3) and Gauss–Chebychev integration for hyperelliptic curves (Theorem 6.6). No Prym-specific machinery.
- The $\mathbb{Z}/m$ representation decomposition of $H^{1,0}(C)$ is standard and **not** used as a shortcut in the paper; the paper gives a single uniform algorithm for all $y^m = f(x)$ via the integer lattice $\Gamma$ and the symplectic base change $S$ with $S^T K_\Gamma S = J$ (see §4.4).

**The actual algorithm (applicable to our curve).** §3.3 Theorem 3.6 + §4.1 Theorem 4.1 + §4.4 SNF + §5 Theorem 5.1 (intersection numbers) give a uniform construction of the full period matrix $\Omega_\Gamma$, followed by symplectic reduction to $(\Omega_A \mid \Omega_B)$. The Prym must then be extracted by a separate $\iota_*$-antiinvariant projection on the resulting $5 \times 10$ period matrix.

**Caveat: non-simple roots.** Our $f(x) = x(x-1)(x-\sqrt 2)^3(x-\sqrt 3)^2(x-\sqrt 5)^2$ is **not** separable — Molin–Neurohr assume $f$ separable (Def. 3.1). The paper's formulas for the analytic branches $\tilde y_{a,b}(u)$ (eq. 5) and the constant $C_{a,b}$ (eq. 7) must be generalized to accommodate multiplicities $e_k$ at each branch point, via

$$\tilde y_{a,b}(u) = \prod_{k: \text{Re}(u_k) \leq 0} (u - u_k)^{e_k/m} \prod_{k: \text{Re}(u_k) > 0} (u_k - u)^{e_k/m}$$

with corresponding adjustment of the exponents $e_a/m$, $e_b/m$ at the endpoint factors $(1 \pm u)$. The local monodromy $\sigma_k = e_k \bmod m$ replaces the paper's implicit $\sigma_k = 1$.

**Estimated LOC.** Full port with non-simple-roots extension: **600–900 LOC** Python + `python-flint` / `mpmath`. The "Prym shortcut" estimate of 300–500 LOC was incorrect because it presumed machinery that doesn't exist in the paper.

### §10.12 Decision point

The four open-source free paths are now mapped:

1. ❌ `abelfunctions` — Cython-MSVC blocker, no Windows fork exists.
2. ❌ LLL on Riemann-bilinear constraint — min integer null norm $\gtrsim 10^9$, exhausted.
3. ❌ Perturbation triage — confirms basis discontinuity at canonical point.
4. **⚠ Build hcperiods / port full Molin–Neurohr algorithm (§3–§5 + §6.1) to Python** — the remaining free path. WSL is blocked (no admin+reboot available). Python port is self-contained but larger than first estimated (600–900 LOC), and must extend the paper to handle our non-separable $f$.

Paid last resort: MAGMA.

**Recommendation for next session:** port the full Molin–Neurohr algorithm (Theorems 3.6 + 4.1 + 4.4 SNF + 5.1 + §6.1 double-exp) to Python with `mpmath` and `python-flint`, handling non-simple roots by generalizing the analytic branch formula (eq. 5) to $\tilde y_{a,b}(u) = \prod_k(u - u_k)^{e_k/m}$. Extract the Prym by post-hoc $\iota_*$-antiinvariant projection.

**Atlas status.** Canonical still *"live candidate"*. Promotion via either path (a) or (b) above.

### §10.13 Artifacts from this session

All in `_prymsprint_raw/`:

| File | Role |
|---|---|
| `prym_compute.py` | 300 LOC non-symplectic-basis pipeline, EPS-corrected (still used for diagnostic Pi in LLL scripts) |
| `prym_compute_out_v2.txt` | high-precision Pi output (dps 60) |
| `lll_intersection.py`, `lll_intersection_highprec.py`, `lll_crossblock.py` | Option 1 escalation ladder (all dead) |
| `lll_hp_out_S20.txt` | captured LLL output demonstrating min integer null $\sim 10^9$ |
| `perturb_det_Y.py`, `perturb_det_Y_out.txt` | Option 5 triage (basis discontinuity confirmed) |
| `TRETKOFF_PLAN.md` | 8-step implementation blueprint for Option 2 |
| `FULL_PRYM_PERIOD_CANONICAL.md` (this file) | narrative log §1–§10 |

### §10.14 Molin–Neurohr port — empirical result and blocker isolation

`mn_port.py` (~787 LOC) implements Steps A–F of the paper: branch-point/monodromy setup, spanning tree, branch matching via `_branch_match_case` (paper eq. 5 + generalized for $e_k \neq 1$), cycle generation (Theorem 3.6), and intersection matrix $K_\Gamma$ (Theorem 5.1).

Three diagnostic tests were written to isolate where the port breaks:

| Test | Curve | Expected $2g$ | Expected rank $K_\Gamma$ | Observed rank | Status |
|---|---|---|---|---|---|
| `test_sqfree.py` | $y^4 = x(x{-}1)(x{-}2)(x{-}3)(x{-}4)$ | 12 | 12 (full, unimodular) | **12**, $\det = 1$ | ✅ |
| `test_nonsqfree_mini.py` | $y^4 = x(x{-}1)^2$ | 2 | 2 (one edge, 3 gens, nullity 1) | **2**, nullity 1 | ✅ |
| `test_nonsqfree_two_edges.py` | $y^4 = x(x{-}1)(x{-}2)^2$ | 2 | 2 (two edges, 6 gens, nullity 4) | **6** (full), nullity 0 | ❌ |

**Blocker isolation.** The port is correct for:

1. **All-simple-roots curves** (separable $f$, paper's original scope) — reproduces Theorem 5.1 exactly, giving the unimodular lattice $\Gamma$ predicted by Remark 3.7.
2. **Single-edge non-squarefree curves** — the generalized branch formula $\tilde y_{a,b}(u) = \prod_k (u-u_k)^{e_k/m}$ and the adjusted cycle definition produce the right rank (2 = $2g$) with the topological nullity (= 1 here, reflecting the one linear relation among the 3 generators of a single edge).

It fails *only* when:

3. **Two tree edges meet at a shared branch point with local monodromy $\sigma \geq 2$** — the cross-edge entries of $K_\Gamma$ (paper's Theorem 5.1 cases iii and iv) are wrong. The 6-generator matrix comes out full-rank instead of rank 2; no algebraic relation among the 6 generators is detected.

Diagnostic interpretation: Theorem 5.1's cross-edge formula $s_x = (1/2\pi)(\rho + m \cdot \arg(\cdot))$ is derived under Def. 3.1's separability assumption, specifically via the bisectrix argument in Lemma 5.3 (paper lines 1099+). That argument uses $\sigma_{\text{shared}} = 1$ (each lifted edge meets each other's lifts at exactly one point in the fiber over the shared vertex); for $\sigma_{\text{shared}} \geq 2$, multiple pairs of lifted edges meet at the same fiber point and the $(\rho, \arg)$ reconstruction undercounts.

The paper's §10.2 explicitly flags the non-separable extension as future work and does **not** provide the corrected cross-edge formula. Reverse-engineering it requires either (a) redoing Lemma 5.3 under general $e_k$, or (b) abandoning the Molin–Neurohr cycle basis entirely in favor of a construction where cross-edge intersections are combinatorial rather than analytic.

**Decision.** Option (b) — the Tretkoff–Tretkoff 1984 construction — is exactly `TRETKOFF_PLAN.md` Steps 1–4: the cyclic-order cell decomposition and lifted-edge graph yield $\pm 1$ intersections *by construction*, independent of the multiplicity of the shared branch point. The Molin–Neurohr port graduates to a **verified subroutine for squarefree segments** but is not the whole pipeline.

**Updated decision vs §10.12.**

1. ❌ `abelfunctions` — Cython-MSVC blocker.
2. ❌ LLL on Riemann bilinear — exhausted.
3. ❌ Perturbation triage — basis discontinuity confirmed.
4. ⚠→✂ Molin–Neurohr Python port — **blocked at Theorem 5.1 cross-edge formula for $\sigma \geq 2$**; works for squarefree and single-edge non-squarefree, not for our two-adjacent-branch-multiplicity curve. Not the free path to det(Y).
5. **→ Tretkoff–Tretkoff port per `TRETKOFF_PLAN.md`** — intersections combinatorial (±1 by cyclic order), genus-5 case = 40 cycles, SNF → symplectic basis, then Prym projection + period integrals. Estimated 400–700 LOC. *This is the next session's work.*

Paid last resort: MAGMA.

### §10.15 Artifacts from this sub-session

Added to `_prymsprint_raw/`:

| File | Role |
|---|---|
| `mn_port.py` | 787 LOC Molin–Neurohr Steps A–F port, squarefree-verified |
| `test_sqfree.py` | passes: rank 12, $\det K = 1$ (Remark 3.7) |
| `test_nonsqfree_mini.py` | passes: rank 2, nullity 1, $2g = 2$ |
| `test_nonsqfree_two_edges.py` | **fails**: rank 6, nullity 0 where rank 2 expected — isolates the Theorem 5.1 cross-edge blocker |
| `tretkoff.py` | Step 1–4 skeleton of Tretkoff–Tretkoff construction (~340 LOC) |

### §10.16 Tretkoff skeleton attempt — partial result

`tretkoff.py` implements Steps 1–4 of `TRETKOFF_PLAN.md`:

1. **Cell decomposition**: base point $P_0$ chosen at $(\bar x, 4i)$, $\bar x$ = mean of real branch-point $x$-values; finite branch points + $P_\infty$ (with ray direction $+i$) form the vertex list.
2. **Cyclic ordering** by $\arg(P_i - P_0)$: for the canonical curve, order is $[x_0, x_1, \sqrt 2, \sqrt 3, \sqrt 5, \infty]$ with $\sigma$-values $[1, 1, 3, 2, 2, 3]$.
3. **Lifted radial edges**: each radial edge has $m = 4$ sheet lifts, with monodromy $k \mapsto k + \sigma_i \pmod m$.
4. **Closed walk enumeration**: enumerate walks visiting CONSECUTIVE positions in the cyclic order, length $L$ with $\sum_{j < L} \sigma_{i_{p+j}} \equiv 0 \pmod m$. For the canonical curve: 60 such walks (12 at each of lengths 2, 4, 8 + 24 at length 6).

**Intersection rule attempt**: corners-at-$P_0$ chord-crossing — for cycles $A, B$, sum over matching-sheet corner pairs the signed interleavings of edges in the Tretkoff cyclic order. This is the "chord diagram" rule.

**Empirical result** (same three test curves):

| Test | Expected $2g$ | MN rank | Tretkoff (this skeleton) rank |
|---|---|---|---|
| squarefree | 12 | 12 ✅ | **8** ❌ |
| 1-edge non-sqf | 2 | 2 ✅ | **0** ❌ |
| 2-edge non-sqf | 2 | 6 ❌ | **0** ❌ |
| canonical $g = 5$ | 10 | (blocked by 2-edge) | **8** ❌ |

**Diagnosis.** The "consecutive-cyclic-position walk" enumeration produces cycles whose corners at $P_0$ are all between *adjacent* edges in the cyclic order — these chord pairs never interleave (an arc between adjacent positions is on the boundary of the cyclic disc, not a proper chord across it). So the rule returns $0$ for all length-$\leq 2$ cycles and undercounts for longer ones. The generating set is topologically incomplete: Tretkoff's full construction requires walks visiting *any subset* of branch points in *any order* (word-length enumeration in $F_r$), whose chord diagrams then have the interior-crossing pattern the rule detects.

Scope of the remaining work to get rank right:

- Enumerate words in $\alpha_1, \ldots, \alpha_r$ of bounded length that close under the monodromy representation $\rho(\alpha_i) = \sigma_i \in \mathbb{Z}/m$. For $r = 6, m = 4$, word-length $\leq 8$ gives on the order of $r^8 / m = 100k$ candidates, prunable to a generating subset by incremental rank checks.
- Refine the chord-diagram sign rule (the naïve "in-B between in-A and out-A" convention sometimes misses the second crossing at nested corners; standard reference: Tretkoff–Tretkoff 1984 §3, Van Wamelen 2006 §2.3).
- Handle infinity separately (base point $P_0$ must be finite; ray to $\infty$ bends the cyclic disc; needs compactification).

Honest estimate on remaining Tretkoff LOC: 300–500 more (enumerate + intersection refinement + closure verifier + Step 5 SNF) beyond the skeleton.

### §10.17 Decision point (revised)

The four methods in the user's waterfall ("3 1 2 5 and then we can pay for something if we really need to only!"):

| # | Method | Status after this session |
|---|---|---|
| 3 | `abelfunctions` | ❌ Cython/MSVC, no Windows fork |
| 1 | LLL on Riemann bilinear | ❌ min integer null $\sim 10^9$ |
| 2 | Tretkoff–Tretkoff port | ⚠ skeleton in place (`tretkoff.py`, 340 LOC); intersection rule incomplete; full port estimate now $700$–$1200$ LOC total including MN cross-edge fix OR full word-enumeration replacement |
| 5 | perturbation triage | ❌ basis discontinuity at canonical point |

Paid last resort: **MAGMA `AnalyticJacobian(f, 4)`** — one-line computation. Commercial license, typically accessed via institutional affiliation or the online MAGMA Calculator (time-limited).

**Recommendation for next session.** The free-path effort has revealed that implementing a rigorous Tretkoff construction for a degree-4 cover with non-separable $f$ is a research-level task (order of 1000 LOC, requires careful combinatorial verification against published test cases). Before committing another session to that port, consider:

(a) **WSL unblock + hcperiods build** — if WSL can be enabled (admin + reboot), this is ~10 min of build time vs. 10+ hours of porting. Primary blocker has been the inability to reboot during active sessions.
(b) **MAGMA Calculator web interface** — single-query, ~$0, time-limited but may complete within the 120 s server limit for $g = 5$.
(c) **Continue Tretkoff port** — with explicit word-enumeration + Van Wamelen 2006 §2.3 as combinatorial reference for the intersection rule.

### §10.18 Artifacts from this session (final)

All in `_prymsprint_raw/`:

| File | Role | LOC |
|---|---|---|
| `mn_port.py` | Molin–Neurohr Steps A–F port; squarefree-verified, breaks at 2-edge non-sqf | 787 |
| `test_sqfree.py`, `test_nonsqfree_mini.py`, `test_nonsqfree_two_edges.py` | Three-tier validation isolating the Theorem 5.1 cross-edge blocker | ~150 |
| `tretkoff.py` | Tretkoff–Tretkoff skeleton (Steps 1–4, incomplete intersection rule) | 340 |
| `FULL_PRYM_PERIOD_CANONICAL.md` (this file) | narrative log §1–§10.18 | 509 |

**Atlas status.** Canonical still *"live candidate"*. Promotion gated on either (a) WSL + hcperiods, (b) MAGMA, or (c) a finished Tretkoff port with verified rank matches on all four test curves.

---

*Proceeds to `BASELINE_VS_CANONICAL_COMPARISON.md`.*
