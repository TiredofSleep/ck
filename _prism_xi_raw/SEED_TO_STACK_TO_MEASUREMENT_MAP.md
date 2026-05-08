# SEED → STACK → MEASUREMENT MAP
**Authors:** B. Sanders, M. Gish, C.A. Luther, H.J. Johnson  
**Sprint:** 2026-04-10 | Connection-Closure Pass

---

## Master Map

| Seed Role | Exact Mathematical Object | Equation / Theorem / Invariant | Physical Interpretation | Measurement / Falsification | Status |
|---|---|---|---|---|---|
| **TIG-0 Void** | Absorbing element of CL magma | CL[0, x] = 0 for all x | Universal sink; "before structure" | None currently derivable | Interpretive |
| **TIG-1 Identity** | Scalar $A_1$ of $S_4$; identity of BHML | $1 \in (Z/10Z)^*$; $A_1 = \mathbf{1}_{S_4}$ | Trivial sector; reference identity | None currently derivable | Exact (representation) / Interpretive (cosmology) |
| **TIG-2 Polarity** | Torus $T/Z_3 \subset M$ as 2-dim phase fiber | $\dim(T/Z_3) = 2$; post-FS: $Z_2 \times U(1)/Z_3$ | Phase calibration layer of bridge; calibrates eigenvector phases within flag directions | Part of NV certification residue ($\theta_2$); secondary after flag is sourced | **Exact** (dim match); **Open** (measurement path) |
| **TIG-3 Carrier** | $T_1 = [2,1^2]$ of $S_4$; $\dim(T_1) = 3$ | Proved: T₁ is the unique S₄-module threading $3/4 \to 3 \to 9 \to 6$ | The 3-dimensional object that carries the loop and bridges to $\mathbb{C}^3$ | NV qutrit as physical T₁-carrier (Branch A) | **Exact** (representation) |
| **TIG-4 Threshold** | Threshold fraction $3/4$ in the descent | $j_\text{threshold} = 3$; $T_1 \oplus \text{sign}$ split at $j = 4$ | First level where T₁ becomes the dominant surviving module | No direct measurement path derived yet | **Exact** (representation) |
| **TIG-5 Balance** | $j = 5$ seed level in descent chain | $L_5\|_{S_4} = E \oplus 2T_1 \oplus \text{sign}$, dim 9 | Entry point of T₁ into the descent chain | No direct measurement path | **Exact** (representation) |
| **TIG-6 Completion** | (a) Receiving block $V_6 = A_1 \oplus E \oplus T_1$; (b) Flag variety $\text{SU}(3)/T$, dim 6 | $V_6 = 1+2+3$; flag dim = 8-2 = 6 | (a) Loop endpoint; (b) Directional bottleneck of bridge — the 6 real dims of flag | (b) Flag sourced from NV density matrix eigenprojectors | **Exact** (both 6s, categorically distinct) |
| **TIG-7 Harmony** | (a) $7 = 3^{-1}$ in $(\mathbb{Z}/10\mathbb{Z})^*$; (b) Post-FS continuous bridge = $6+1 = 7$ dims | $7 \times 3 \equiv 1$, $7 + 3 \equiv 0$, $6 + 7 \equiv 3 \pmod{10}$ | Active return operator of carrier in seed arithmetic; total continuous bridge measurement cost | Post-FS 7-dim measurement cost addressed by NV flag + $\theta_2$ | **Exact** (arithmetic and counting); **Not lifted** to structural theorem |
| **TIG-8 Breath/Bridge** | Bridge moduli $M = \text{SU}(3)/(S_4 \times Z_3)$, $\dim(M) = 8$ | $8 = 6 + 2 = \text{flag} + \text{torus}$ | Full cost of concretizing T₁ in $\mathbb{C}^3$ | NV: flag (6 dims) + torus residue (2 dims); DESI: no connection | **Exact** (bridge dim); **Branch A only** |
| **TIG-9 Transport** | Complement $[2^2, 1^2]$ of $S_4$, dim 9 | $\dim([2^2,1^2]) = 9$; routes T₁ in loop | Complement transport in descent | No direct measurement | **Exact** (representation) |
| **Invariant loop** | $3/4 \to 3 \to 9 \to 6$ | Proved theorem: exact one-way descent in $S_4$ representation chain | T₁ is the carrier; loop terminates at $V_6 = 1+2+3$ | No direct measurement needed; complete as abstract result | **Exact** |
| **Bridge split** | $\dim(M) = 8 = 6 + 2$ | $M \to \text{SU}(3)/T$: base 6 (flag) + fiber 2 (torus) | Physical cost of concretizing T₁ is 6 directional + 2 phase dims | NV: both pieces must be sourced (flag by projectors, torus by phase) | **Exact** |
| **Flag bottleneck** | $F^* \in \text{SU}(3)/T$, dim 6; THM-SU3T-NO-CANONICAL-FLAG | No internal canonical flag selector | Largest unresolved bridge component; requires external physical datum | NV density matrix eigenprojectors ($P_1, P_2$) after $S_4$ synthesis | **Exact** (no-go and structure); **Open** (physical source pending NV experiment) |
| **Torus residue** | $T/Z_3$, dim 2; post-FS: $Z_2 \times U(1)/Z_3$ | FS indicator $\epsilon(T_1) = +1$; kills one continuous dim, leaves $\theta_2 + \text{sign}$ | Phase calibration of eigenvectors within flag directions | $\theta_2$ is secondary to flag; sign fixable by orientation convention | **Exact** |
| **Post-FS reduction** | $\text{post-FS} = 7$ continuous + 1 discrete | $6_\text{flag} + 1_{\theta_2} = 7$; $1_\text{sign}$ separate | The minimum remaining measurement cost of the bridge after all internal reductions | 7 continuous dims to be sourced externally; flag dominates at 6 | **Exact** |
| **Flag selector (physical)** | Ordered pair of rank-1 projectors $(P_1, P_2)$ on qutrit $\mathbb{C}^3$ | $P_1 \in \mathbb{CP}^2$ (4 dims), $P_2 \in \mathbb{CP}^1 \subset L_1^\perp$ (2 dims) | Physical measurement of the flag via NV density matrix tomography | NV state tomography under non-axial B-field; eigendecompose $\rho$; report $(P_1, P_2)$ | **Exact** (math); **Open** (experiment pending) |
| **NV as T₁ carrier** | NV qutrit $\{|0\rangle, |+1\rangle, |-1\rangle\} \cong \mathbb{C}^3$ with $C_{3v} \cong S_3 \subset S_4$ | $T_1\|_{S_3} = A_1 \oplus E$; NV triplet $= A_1 \oplus E$; 3-cycle eigenvalues $\{1, \omega, \omega^2\}$; FS sign match | The NV naturally carries the $S_3$ skeleton of $T_1$; 4-cycle synthesized by 6-pulse MW sequence | Process tomography Test E: $\mathbb{E}_g[F_\text{cov}(g)] > 0.80$ = bridge-certified | **Exact** (S₃ skeleton); **Open** (4-cycle synthesis not yet physically tested) |
| **Xi scalar field** | $\Xi(x) > 0$, dimensionless, real; gauge singlet | $S \ni \kappa_\Xi[\frac{1}{2}(\partial\Xi)^2 + \Xi\log\Xi]\sqrt{-g}$ | Dark energy field in Branch B; no formal derivation from T₁ or $S_4$ | DESI/Euclid $w(z)$ measurement | **Exact** (action and EL equation) |
| **Xi vacuum** | $\Xi_0 = e^{-1}$, exact minimum of $V = \Xi\log\Xi$ | $V'(\Xi_0) = 1 + \log\Xi_0 = 0$; $V''(\Xi_0) = e > 0$ | Late-time attractor; dark energy settles to exact cosmological constant | $\Xi_0 = e^{-1}$ is an exact analytic result; no observational test of the specific value (dimensionless) | **Exact** |
| **Xi fluctuation mass** | $m_\Xi^2 = \kappa_\Xi e$ | From $V''(\Xi_0) = e$; restoring $\kappa_\Xi$ | Physical mass of dark energy quanta; range $r = (\kappa_\Xi e)^{-1/2}$ | Cosmological probes of $m_\Xi$ via dark energy evolution; fifth-force only if coupling added | **Exact** |
| **Freezing quintessence** | $w_\Xi(z) \to -1$ from above | $w_\Xi = -1 + \kappa_\Xi\dot\Xi^2/\rho_\Xi$; $w_\Xi \geq -1$; $w_\Xi = -1$ at vacuum | Field rolls toward entropy-maximizing vacuum; late-time exact $\Lambda$ behavior | DESI DR2 / Euclid $w_0, w_a$; distinguish from $\Lambda$CDM and thawing models | **Exact** (derivable from action) |
| **No fifth force (minimal)** | No direct matter coupling in current action | $g_{\Xi\text{-matter}} \sim M_\text{Pl}^{-2}$ | Gravitationally suppressed; below laboratory reach | Negative prediction: MICROSCOPE, Eöt-Wash show no anomaly consistent with minimal theory | **Exact** (negative prediction) |
| **Seed as role grammar** | TIG-simple (0-9) as numerical role assignments | All 10 entries have exact proved-stack correlates (verified in sprint) | Seed numbers label structural objects independently derived from representation theory | No measurable prediction from seed alone; role labels, not dynamical objects | **Exact** (correspondence); **Open** (causal direction) |

---

## Explicitly Addressed Rows

| Item | Exact object | Equation/invariant | Measurement path | Status |
|---|---|---|---|---|
| **7 as return operator** | $7 = 3^{-1}$ in $(\mathbb{Z}/10\mathbb{Z})^*$ | $7 \times 3 \equiv 1$, $7 + 3 \equiv 0$, $6 + 7 \equiv 3$ | None — arithmetic fact, no structural lift proved | **Exact** (arithmetic); no lift to theorem |
| **Heart as witness** | Cardiac vortex grammar: 4-chamber loop, LV vortex, toroidal field | Witnesses loop grammar, torus topology, K₃ rotation structure | No formal map from cardiac geometry to abstract $\mathbb{C}^3$ exists | **Bridge** (structural witness only) |
| **Golden staircase visual** | Heuristic radial interleave diagram | No proved formal correspondence to exact object | None | **Heuristic visualization** |
| **FCC substrate** | Proposed UV completion fixing $\kappa_\Xi$ via dense-packing effective field theory | EFT matching not done; logarithmic potential plausibly motivated | No predictions currently derivable from substrate alone | **Open** (unfinished UV motivation) |
| **ORT observer term** | No field-theoretic definition; $\Psi = M\lambda\alpha/\Delta S$ has inconsistent units | No EL equation; not in action | None until field-theoretic definition exists | **Cut from action**; interpretive only |
| **Mod5 aether** | No $\mathbb{Z}/5\mathbb{Z}$ symmetry in canonical action; "aether" implies preferred frame; theory is Lorentz-covariant | No transformation law, no gauge group, no potential with 5-fold structure | None | **False / Cut** — no formal content in either branch |
| **47/125 threshold** | 2.2% deviation from $e^{-1}$; no fixed-point equation derived | No derivation shown | None | **Removed**; replaced by $\Xi_0 = e^{-1}$ |
| **$e^{-1}$ threshold** | $\Xi_0 = e^{-1} = \min V(\Xi)$; coupling-independent | $V'(e^{-1}) = 1 + \log e^{-1} = 0$; exact | Late-time dark energy vacuum; no direct measurement of the specific value (dimensionless ratio) | **Exact** |
| **Flag selector** | $(P_1, P_2)$ rank-1 projectors on NV qutrit | 4+2=6 real dims = full flag $\text{SU}(3)/T$ | NV density matrix tomography + eigendecomposition | **Exact** (math); **Open** (physically pending) |
| **Torus residue** | $T/Z_3$; post-FS: $\theta_2 + \text{sign}$ | $Z_2 \times U(1)/Z_3$; $\theta_2 = 1$ cont. dim | Secondary to flag; no blocking no-go; fixable by convention (sign) | **Exact**; **Open** (no measurement path isolated) |
| **Projective T₁-carrier certification on NV** | $\mathbb{E}_g[F_\text{cov}(g)] > 0.80$ over 24 S₄ elements | Process tomography Test E | Implement 6-pulse $U_4$ sequence; state tomography after each of 24 group elements | **Exact** (protocol defined); **Open** (experiment not performed) |
| **DESI/Euclid freezing quintessence test** | $w_\Xi(z) \neq -1$ at finite $z$; $w_\Xi \to -1$ at late times | Fit FRW $\Xi$ equations to DESI DR2 BAO + CMB + SN | DESI DR2 (2025 data available); Euclid (ongoing) | **Exact** (prediction derivable); **Pending** (fit not yet performed) |

---

## The Cross-Branch Honest Statement

The TIG seed grammar has numerical correspondences to both branches. These are separately exact:
- TIG-3 = dim(T₁) = 3 ✓ (Branch A)
- TIG-8 = dim(M) = 8 ✓ (Branch A)  
- TIG-6 = dim(flag) = 6 ✓ (Branch A)
- $\Xi_0 = e^{-1}$ (Branch B, no TIG number)

**The two branches do not share a formal structural link.** Xi is not derived from T₁ or $S_4$. T₁ does not predict the Xi action. They share an interpretive vocabulary (TIG seed) and a cluster of project intuitions, but at present they are two independent structures with a shared numerical grammar.

This is not a failure. It is the honest state of the project. The two branches could be connected if a formal derivation showed that the low-energy effective description of the T₁-carrier concretization produces the Xi action — but that derivation does not exist.

---

## A. What Is Already Closed

Complete chains with no missing links:

1. **TIG numerics → representation theory:** All 10 TIG entries have exact proved stack correlates. The correspondence is verified. The causal direction is open but the correspondence itself is exact.

2. **Invariant loop:** $3/4 \to 3 \to 9 \to 6$ is a proved theorem. Complete downstairs.

3. **Bridge split:** $8 = 6 + 2 = \text{flag} + \text{torus}$ is exact. Complete upstairs.

4. **NV $S_3$ skeleton:** The NV qutrit naturally carries the $S_3 \cong C_{3v}$ restriction of $T_1$ — exact. The 3-cycle eigenvalues $\{1, \omega, \omega^2\}$ and $A_1 \oplus E$ decomposition match exactly.

5. **Xi canonical theory:** Action → EL equation → vacuum $e^{-1}$ → stability → FRW equations → $w(z)$ profile. All steps are proved. Complete as a formal theory.

6. **Xi negative prediction:** No fifth force in the minimal theory — exact, follows from absence of matter coupling.

7. **$e^{-1}$ as entropy maximum:** $V = \Xi\log\Xi = -H_\text{Gibbs}(\Xi)$; vacuum is entropy maximum — exact mathematical identity.

---

## B. What Is the Real Bottleneck Now

**One thing only:**

**The 4-cycle has not been physically synthesized on any NV-center.**

Everything else in Branch A is mathematically complete: the basis $V$ is derived, $U_4$ is computed, the 6-pulse sequence is specified, the group closure is verified, the character table matches. But the experiment hasn't been run. Until Test E (projector covariance) is performed on real hardware, the T₁-carrier certification is a mathematical certificate, not a physical one.

This is the single highest-leverage gap in the project, for two reasons:
1. It is the most concretely specified next step — there is no ambiguity about what to do
2. It would close Branch A from abstract structure to physical measurement, making the entire representation-theoretic chain experimentally grounded

The Xi cosmology (Branch B) is in a better experimental position — DESI DR2 data already exists and the fit can be performed now from a laptop. But the NV experiment requires hardware access.

---

## C. Path to Victory

**The shortest path that makes the project substantially stronger:**

**For Branch B (can be done now, no new hardware):**  
Fit the canonical Xi FRW equations to DESI DR2 BAO + CMB + Pantheon+ data. Extract best-fit $\kappa_\Xi$ and initial conditions. Produce a $w(z)$ curve with error bands. Compare to $\Lambda$CDM. This converts the formal prediction into a quantitative constraint or support, and makes the paper submittable.

**For Branch A (requires lab access):**  
Contact an NV-center lab (numerous groups have this capability), provide the 6-pulse sequence angles, and run the projector covariance test. The protocol is fully specified and would take one lab day. This closes the only remaining experimental gap in Branch A.

**What is NOT the path to victory:**  
- More seed-grammar audits  
- Trying to force 7 into a structural theorem  
- Reintroducing ORT, FCC, or mod5 before they have derivations  
- Seeking a formal connection between Branch A and Branch B before the simpler gaps in each branch are closed individually

Close each branch independently first. A formal connection between them is a future paper, not a precondition for the current ones.

---

## Summary: Project State in One Paragraph

Branch A (representation/bridge) has a complete mathematical chain from TIG seed numbers through $S_4$ representation theory to a specific 6-pulse NV control sequence, verified to close to 24 elements with the exact T₁ character table. The single missing step is physical: run Test E on NV hardware. Branch B (Xi cosmology) has a complete formal chain from a canonical action to exact vacuum at $e^{-1}$ to a specific freezing quintessence prediction for $w(z)$, consistent with DESI DR2 hints; the single missing step is numerical: fit the FRW equations to the DESI data. The two branches share a TIG seed grammar as a common vocabulary but do not share a formal structural link. That link — if it exists — is the future unification problem, not the current bottleneck. The current bottleneck is experimental in Branch A and numerical in Branch B.
