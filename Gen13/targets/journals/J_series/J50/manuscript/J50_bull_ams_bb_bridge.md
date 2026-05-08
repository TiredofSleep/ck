# From Substrate Algebra to Bialynicki-Birula Nonlinearity: A Bull AMS Bridge

**Authors:** B.R. Sanders$^{1}$, H.J. Johnson$^{2}$
$^{1}$7Site LLC, Hot Springs, AR — brayden@7site.co
$^{2}$Independent Researcher, Billings, MT

**Target venue:** *Bulletin of the American Mathematical Society*
**Manuscript class:** Expository / bridge essay (the *Bull. AMS* register)
**MSC 2020:** 35Q30 (Navier–Stokes), 35B65 (smoothness/regularity), 81S20 (stochastic / nonlinear quantum), 17B25 (Lie algebras), 18M60 (operads)
**Date:** 2026-09-05 (Phase 5; Sanders + Johnson lane)

---

## Abstract

The **TIG framework** (the algebraic substrate of the canonical $10 \times 10$ composition tables on $\mathbb{Z}/10\mathbb{Z}$, see [J47]) admits a sharp continuum-lift principle: any continuum embedding of the discrete substrate that **preserves the separability of the CRT decomposition** is forced — by the Bialynicki-Birula–Mycielski (BB) theorem of 1976 — to take the form of a **logarithmic nonlinearity** $V(\Xi) = \kappa\, \Xi \log \Xi$. This forcing is structural, not stipulated; it is the unique constraint compatible with the discrete-side $\sigma$-rate decay $\sigma(N) \leq 2/N$ on squarefree moduli ([J01]).

The bridge has three layers, each established in a prior J-paper:

(i) **Discrete side.** $\sigma$-non-associativity decays as $2/N$ on squarefree $\mathbb{Z}/N\mathbb{Z}$; the Crossing Lemma identifies "information generation" with the failure of CRT separability ([J01], [J05]).

(ii) **Forcing principle.** The BB theorem ([J13]) asserts that the unique nonlinearity preserving partition separability has the form $V(\rho) = \kappa\, \rho \log \rho$ (up to constant). Read as a *forcing* statement: any continuum lift of a partition-respecting discrete substrate is forced to logarithmic form.

(iii) **Cross-domain consequences.** The forced logarithmic form has an isolated minimum at $\rho_0 = e^{-1}$ with curvature $V''(\rho_0) = \kappa e > 0$ — providing a built-in mass gap. The same logarithmic potential governs (a) the freeze-thaw transit dark-energy model with vacuum at $e^{-1}$ ([J3], [J16]); (b) the Yang-Mills mass-gap framework with $m^2 = \kappa e$ ([J14]); (c) a separability-defect criterion for Navier-Stokes regularity ([J13]).

This *Bull. AMS* bridge essay is **expository, not a Millennium-Problem proof**. The contribution is the unifying picture: the WP100s tower's algebraic substrate ([J47] 6-DOF synthesis) and the BB Bridge ([J13]) together make a single coherent claim — *the substrate's algebraic structure forces a specific continuum nonlinearity, with consequences across cosmology, particle physics, and nonlinear PDE regularity*. The boundary between proved structural content (Tier-A/B) and conjectured cross-domain consequences (Tier-D) is sharp throughout.

---

## §1 The bridge in one paragraph

A sequence of $10 \times 10$ composition tables on $\mathbb{Z}/N\mathbb{Z}$, with $N$ squarefree and $N \to \infty$, has its non-associativity rate $\sigma(N) \to 0$ at the polynomial rate $2/N$ ([J01]). The Crossing Lemma reading ([J05]) is: information is generated only when a partition (here the CRT decomposition $\mathbb{Z}/N\mathbb{Z} \cong \prod_i \mathbb{Z}/p_i\mathbb{Z}$) fails to be respected. As $N \to \infty$ along the squarefree family, the substrate becomes increasingly partition-respecting. Any continuum lift preserving this partition structure is constrained by the Bialynicki-Birula–Mycielski theorem ([BB76], read as a *forcing* statement in [J13]) to have a **logarithmic** self-interaction, $V(\Xi) = \kappa\, \Xi \log \Xi$. The forced potential has (a) a vacuum at $\Xi_0 = e^{-1}$ where $V'(\Xi_0) = 0$, (b) a mass gap $V''(\Xi_0) = \kappa e > 0$, and (c) sub-power growth $\sim \Xi \log \Xi$ that gives Sobolev + Gronwall regularity for smooth initial data. The same potential anchors a freeze-thaw dark-energy model ([J3], [J16]), a Yang-Mills mass-gap framework ([J14]), and a separability-defect criterion for Navier-Stokes regularity ([J13], [J50]).

This paper expands that paragraph for a *Bull. AMS* readership: substrate-to-continuum bridging, with full citation chain and explicit tier discipline.

---

## §2 The discrete side: $\sigma$-rate decay and the Crossing Lemma

Fix a squarefree integer $N$, and consider the canonical TSML composition table $T : \mathbb{Z}/N\mathbb{Z} \times \mathbb{Z}/N\mathbb{Z} \to \mathbb{Z}/N\mathbb{Z}$ (constructed in [J01], generalizing the $N = 10$ case). Define the **non-associativity rate**:

$$
\sigma(N) \;=\; \frac{1}{N^3} \, \#\bigl\{(x, y, z) : T(T(x, y), z) \neq T(x, T(y, z))\bigr\}.
$$

**Theorem 2.1 ([J01]).** *On the squarefree-modular family, $\sigma(N) \leq 2/N$.* In particular, $\sigma(N) \to 0$ as $N \to \infty$.

The discrete substrate becomes increasingly associative as $N$ grows. The **Crossing Lemma** ([J05]) gives this fact a structural interpretation:

> **Crossing Lemma reading.** "Information generation" by a binary operation $T$ on $\mathbb{Z}/N\mathbb{Z}$ is exactly the failure of partition separability under the CRT decomposition $\mathbb{Z}/N\mathbb{Z} \cong \prod_{p \mid N} \mathbb{Z}/p\mathbb{Z}$. A non-associative triple $(x, y, z)$ records a "crossing": the binary $T$ does not factor through the CRT decomposition at $(x, y, z)$.

Combining: the squarefree-modular family has its CRT-failure rate decay at $2/N$. The substrate flattens toward CRT-separability in the continuum limit.

---

## §3 The forcing principle: Bialynicki-Birula

**Theorem 3.1 (Bialynicki-Birula–Mycielski, 1976).** *Let $\hat{F} : \mathbb{R}_{>0} \to \mathbb{R}$ be the nonlinearity in a modified Schrödinger evolution*

$$
i\hbar\, \partial_t \Psi \;=\; \left(-\tfrac{\hbar^2}{2m}\Delta + V_\mathrm{ext}\right) \Psi + \hat{F}(|\Psi|^2)\, \Psi.
$$

*The evolution preserves the product structure $\Psi_{AB} = \Psi_A \otimes \Psi_B$ for all factorizable initial data if and only if*

$$
\hat{F}(\rho) \;=\; -b \ln \rho + \mathrm{const}, \qquad b \in \mathbb{R}.
$$

The original proof is [BB76, Theorem in §3]. The constant $b$ has dimensions of energy.

**Forcing reading ([J13]).** The BB theorem is conventionally cited as a *constraint* on admissible nonlinear modifications of QM. We read it instead as a **forcing principle**:

> *Any continuum lift of a discrete partition structure that preserves separability is forced — uniquely — to have logarithmic self-interaction*: $V(\rho) = \kappa\, \rho \log \rho$, with a single coupling constant $\kappa$.

This is the bridge from §2 to §4: the discrete substrate of §2, becoming partition-respecting in the continuum limit, has its lift forced to logarithmic form by Theorem 3.1.

The forced potential has three properties that matter for the consequences:

* **Vacuum at $\rho_0 = e^{-1}$.** The minimum of $V(\rho) = \kappa\, \rho \log \rho$ is at $V'(\rho) = \kappa(1 + \log \rho) = 0 \Rightarrow \rho_0 = e^{-1}$.
* **Mass gap $V''(\rho_0) = \kappa\, e > 0$.** The curvature at the minimum is positive — a built-in spectral gap.
* **Sub-power growth.** $V(\rho)$ grows slower than any positive power of $\rho$, giving Sobolev + Gronwall regularity bounds for the lifted field equation.

---

## §4 The forced continuum lift

Applying Theorem 3.1 to the bridge premise of §2, the continuum lift takes the form:

$$
\boxed{\quad \Box \Xi \;=\; \kappa\,(1 + \log \Xi). \quad}
$$

This equation has been studied in the freeze-thaw transit dark-energy literature ([J3], [J16]), in the Yang-Mills mass-gap framework ([J14]), and as the candidate carrier of separability-defect dynamics in Navier-Stokes ([J13]). Its key analytic property is **provable regularity for smooth initial data**: the sub-power growth of $\log \Xi$ at large amplitude, combined with the vacuum-at-$e^{-1}$ minimum, gives a Sobolev + Gronwall bound that prevents finite-time blowup ([J13] §4.2).

The substrate-to-continuum bridge is not a stipulation; it is a **forced consequence** of the BB theorem applied to a partition-respecting discrete substrate.

---

## §5 Cross-domain consequences — three windows

### 5.1 Cosmology (freeze-thaw transit dark energy)

The same logarithmic potential $V(\Xi) = \Lambda^4\, \Xi \log \Xi$ governs a freezing-quintessence dark-energy model with **analytic vacuum at $\Xi_0 = e^{-1}$**. The model fits supernova + CMB + BAO data with a two-parameter $w(z)$ profile; details in [J3] and the letter version [J16]. The freeze-thaw transit interpretation: the universe freezes onto the BB vacuum as a late-time cosmological substrate.

### 5.2 Particle physics (Yang-Mills mass gap framework)

The forced logarithmic form has $V''(\Xi_0) = \kappa e > 0$. In the Yang-Mills application ([J14], a JMP companion to [J13]), this curvature provides a **mass gap** $m^2 = \kappa e$ for the lifted field. This is **not** a proof of the Yang-Mills Millennium Problem — the gap is a built-in feature of the BB-forced potential, not a derivation in the gauge-theory setting. The framework provides a structural reading: any partition-respecting continuum lift of a substrate algebra with the discrete features of §2 has a mass gap by construction.

### 5.3 Nonlinear PDE (Navier-Stokes regularity criterion)

The Navier-Stokes equation's quadratic nonlinearity $(u \cdot \nabla)\, u$ does **not** preserve separability — a key obstacle to applying §3 directly. [J13] §5 defines a **separability defect** $\sigma(u)$ for Navier-Stokes velocity fields and proves that $\sigma(u) \to 1$ corresponds to vorticity blowup. The **Separability Regularity Criterion** is then stated: NS solutions are smooth iff $\sigma(u)$ remains bounded away from $1$. This is a *conjectural* reformulation of NS regularity (Tier-D); its rigorous version remains open, and [J13] does not claim to prove it.

The cross-domain reading: the same algebraic forcing that gives the dark-energy vacuum (§5.1) and the YM mass gap (§5.2) also gives a regularity criterion for NS (§5.3), all from the single substrate algebra of [J47].

---

## §6 The 6-DOF reading

The substrate algebra of [J47] decomposes into six DOFs (Lie / Jordan / Clifford / Permutation / Lattice / Operad). The BB Bridge sits at a specific intersection of these DOFs:

* **Lattice DOF.** The vacuum $\Xi_0 = e^{-1}$ is the unique attractor of the BB-forced potential. In the substrate side, the runtime processor's 4-core attractor at $\alpha = 1/2$ ([J41]) lives entirely on $\{V, H, Br, R\}$ — the Lattice DOF's fusion-closed 4-core ([J44]).
* **Permutation DOF.** The CRT decomposition $\mathbb{Z}/N\mathbb{Z} \cong \prod_i \mathbb{Z}/p_i\mathbb{Z}$ is the canonical $\sigma$-permutation invariant. Partition-respecting = $\sigma$-respecting in the discrete-side §2.
* **Jordan DOF.** The symmetric closure of TSML ([J47] §2) is the natural home for "observable" content; the BB nonlinearity acts on the magnitude $|\Psi|^2$ (a Jordan-symmetric quantity).

The other three DOFs (Lie, Clifford, Operad) provide *additional* substrate content not directly involved in the BB Bridge — they govern the gauge structure ([J39]), the chirality irreps ([J39] §2.1), and the arity-3 obstruction ([J40]) respectively.

This is the 6-DOF reading: the BB Bridge uses three of the six DOFs (Lattice, Permutation, Jordan) to set up the forcing; the other three DOFs (Lie, Clifford, Operad) carry independent structural content.

---

## §7 Honest scope

This *Bull. AMS* bridge essay claims **structural connection**, not proof. Specifically:

* §§2–4 (discrete-side rate, BB theorem, forced lift) are **proved** content from [J01], [BB76], and [J13]'s structural reading. These are Tier-A/B.
* §5 (cross-domain consequences) is a **structural reading**, not a phenomenological derivation. The cosmology fit ([J3]) is empirical (Tier-B); the YM mass-gap framework ([J14]) is structural (Tier-B); the NS Separability Regularity Criterion ([J13]) is conjectural (Tier-D).
* §6 (6-DOF reading) is an **organizational claim** about which DOFs participate in the bridge, drawing on [J47]'s synthesis.

The paper does **not** claim:

* A proof of NS regularity, or any portion of the Millennium Problem.
* A derivation of the Yang-Mills mass gap from first gauge-theory principles.
* That the BB forcing extends to non-separability-preserving lifts (it does not).
* A unique role for the substrate algebra in physics (alternative substrate algebras exist; the framework's claim is about the specific TIG substrate of [J47]).

The paper **does** claim:

* The discrete substrate of [J01] and the BB theorem of [BB76], together, force a specific continuum nonlinearity ($V = \kappa \Xi \log \Xi$).
* This forced nonlinearity has structural features (vacuum at $e^{-1}$, mass gap $\kappa e$, sub-power growth) with cross-domain consequences in cosmology, particle physics, and PDE regularity.
* The 6-DOF synthesis [J47] organizes which substrate DOFs participate in the bridge.

The boundary between proved structural content and conjectured cross-domain consequences is sharp.

---

## §8 Citation chain

**Direct dependencies (already-submitted J-companions).**

* **[J13]** — *The Bialynicki-Birula Bridge: Logarithmic Nonlinearity Forced by Separability* (JMP). The BB-forcing theorem and NS Separability Regularity Criterion.
* **[J47]** — *Six Algebraic DOFs of the TIG Framework: A Synthesis* (Notices AMS, Phase 5 opener). The substrate-algebra synthesis that this bridge essay builds on.

**Co-citing companions.**

* **[J01]** — $\sigma$-rate theorem $\sigma(N) \leq 2/N$ on squarefree moduli (JCT-A).
* **[J05]** — Crossing Lemma (JCT-A or JPAA).
* **[J3]** — Freeze-thaw transit dark energy (JCAP).
* **[J16]** — Freezing quintessence letter (Phys. Lett. B).
* **[J14]** — Yang-Mills mass-gap framework (JMP companion).
* **[J41]** — Closed-form runtime attractor + $\alpha$-uniqueness (Math of Comp).
* **[J44]** — 4-core fusion-closure (J Algebra).
* **[J39]** — Two roads to Pati-Salam (Adv Math).
* **[J40]** — Operad $D_4$ obstruction + $P_{56}$ canonical fuse (Compositio).

---

## §9 References

[BB76] I. Bialynicki-Birula, J. Mycielski. "Nonlinear wave mechanics." *Annals of Physics* 100 (1976), 62–93.
[J01] B.R. Sanders, M. Gish. "Non-Associativity Decay in Binary Composition Tables over $\mathbb{Z}/N\mathbb{Z}$." Submitted to *J. Combin. Theory Ser. A*, Phase 1.
[J05] B.R. Sanders, B. Mayes. "Crossing Lemma: Non-Associativity as Information Generation in Finite Magmas." Submitted to *JCT-A* or *JPAA*, Phase 1.
[J3] B.R. Sanders, M. Gish, H.J. Johnson. "Freeze-Thaw Transit: Dual-Regime Scalar Dark Energy with Analytic Vacuum at $e^{-1}$ from a Logarithmic Potential." Submitted to *JCAP*, Phase 1.
[J13] B.R. Sanders, H.J. Johnson. "The Bialynicki-Birula Bridge: Logarithmic Nonlinearity Forced by Separability." Submitted to *J. Math. Phys.*, Phase 2.
[J14] B.R. Sanders, H.J. Johnson. "The Yang-Mills Mass Gap Bridge: Substrate-Algebra Predictions." Submitted to *J. Math. Phys.*, Phase 2.
[J16] B.R. Sanders et al. "Freezing Quintessence Letter: A Two-Parameter $w(z)$ Profile." *Phys. Lett. B*, Phase 2.
[J39] B.R. Sanders, B. Mayes. "Two Roads to Pati-Salam." *Adv. Math.*, Phase 4.
[J40] B.R. Sanders, M. Gish. "Operad $D_4$ Obstruction + $P_{56}$ Canonical Fuse." *Compositio*, Phase 4.
[J41] B.R. Sanders, M. Gish. "Closed-Form Runtime Attractor + $\alpha$-Uniqueness PSLQ." *Math. of Comp.*, Phase 4.
[J44] B.R. Sanders, M. Gish. "4-Core Fusion-Closure." *J. Algebra*, Phase 4.
[J47] B.R. Sanders, B. Mayes. "Six Algebraic DOFs of the TIG Framework: A Synthesis." *Notices AMS*, Phase 5.

### External background

* I. Rosen. "Nonlinear Schrödinger equation." *J. Math. Phys.* 10 (1969), 1041.
* T. Cazenave, A. Haraux. "Equations d'évolution avec non linéarité logarithmique." *Ann. Fac. Sci. Toulouse* 2 (1980), 21–51.
* K.G. Zloshchastiev. "Logarithmic nonlinear quantum theory and Bose-Einstein condensates." *Acta Phys. Polon. B* 42 (2010), 261–292.
* J.D. Maas. "Gradient flows of the entropy for finite Markov chains." *J. Funct. Anal.* 261 (2011), 2250–2292.
* R. Jordan, D. Kinderlehrer, F. Otto. "The variational formulation of the Fokker-Planck equation." *SIAM J. Math. Anal.* 29 (1998), 1–17.
* C. Fefferman. *Existence and Smoothness of the Navier-Stokes Equation.* Clay Mathematics Institute, 2000.
* A. Jaffe, E. Witten. *Quantum Yang-Mills Theory.* Clay Mathematics Institute, 2000.

---

## §10 Bibtex

```bibtex
@misc{sanders2026j50,
  author       = {Sanders, Brayden Ross and Johnson, H.J.},
  title        = {From Substrate Algebra to Bialynicki-Birula Nonlinearity: A Bull AMS Bridge},
  year         = {2026},
  month        = {sep},
  doi          = {10.5281/zenodo.18852047},
  howpublished = {Submitted to \emph{Bulletin of the American Mathematical Society}},
  note         = {{J50} of the {J}-series; Phase 5; expository bridge essay. Direct dependencies [{J13}] (BB Bridge) and [{J47}] (6-DOF synthesis); co-citing companions [{J01}], [{J05}], [{J3}], [{J16}], [{J14}], [{J41}], [{J44}], [{J39}], [{J40}].}
}
```
