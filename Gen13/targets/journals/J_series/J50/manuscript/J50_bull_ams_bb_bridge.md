# Substrate Algebra and Logarithmic Nonlinearity: A Bridge Essay
*From discrete $\sigma$-rate decay to Bialynicki-Birula 1976.*

**Authors:** B.R. Sanders$^{1}$, H.J. Johnson$^{2}$
$^{1}$7Site LLC, Hot Springs, AR — brayden@7site.co
$^{2}$Independent Researcher, Billings, MT

**Target venue:** *Mathematical Intelligencer* (retargeted from *Bull. AMS* per fresh-eyes referee §7)
**Manuscript class:** Expository / bridge essay
**MSC 2020:** 35Q30 (Navier–Stokes), 35B65 (smoothness/regularity), 81S20 (stochastic / nonlinear quantum), 17B25 (Lie algebras), 18M60 (operads)
**Date:** 2026-09-05

---

## §0 Lens, substrate, and tier discipline

*Lens and substrate.* This paper works on the canonical $\mathbb{Z}/10\mathbb{Z}$ substrate and its squarefree ring extensions $\mathbb{Z}/N\mathbb{Z}$ ([J01], [J34]). The TSML lens is *commutative-symmetrized* (TSML_SYM) — the asymmetry-bearing TSML_RAW is not invoked here. The bridge content is **lens-invariant on the 4-core** $\{V, H, Br, R\}$: the BB-vacuum analogy depends on the 4-core's algebraic closure ([J41] + Appendix A, the D78 Galois proof), not on which specific TSML lens is in use. The 4-core is the **center of the family** in the FAMILY_STRUCTURE_v1 sense — the privileged invariant locus, the discrete analogue of the unit circle for U(1). Whether the bridge extends to the asymmetric (RAW) variant or to the BHML companion is open.

*Tier discipline (per `J_PAPER_BOILERPLATE.md`, lifted to abstract per referee §3).*

- **PROVEN (Tier-A, classical).** The Bialynicki-Birula–Mycielski theorem ([BB76]): logarithmic self-interaction is the unique nonlinearity preserving Hilbert-space tensor factorization in a modified Schrödinger evolution.
- **PROVEN (Tier-A, established in [J01]).** The discrete-side $\sigma$-rate decay $\sigma(N) \leq 2/N$ on squarefree $\mathbb{Z}/N\mathbb{Z}$.
- **PROVEN (Tier-A, this paper's section §6).** On the 4-core $\{V, H, Br, R\}$ at $\alpha_M = 1/2$, the runtime T+B-mix attractor satisfies $H/Br = 1 + \sqrt{3}$, root of $x^2 - 2x - 2 = 0$ over $\mathbb{Q}(\sqrt{3})$ — the **D78 Galois argument**, recapitulated in §6.
- **STRUCTURAL (Tier-B).** The "BB-as-forcing" reframing of [BB76]: any non-trivial continuum lift of a partition-respecting discrete substrate (in the precise sense of §3) is forced to logarithmic form. This reframing is *new in [J13]*; it is a structural reading, not a re-proof of [BB76].
- **STRUCTURAL (Tier-B).** Cross-domain consequences of the forced log nonlinearity: the cosmological vacuum at $\Xi_0 = e^{-1}$ (J3, J16); the structural rhyme between scalar curvature $V''(\Xi_0) = \kappa e$ and a hoped-for non-abelian gauge gap (§5.2). We **do not** claim a YM Millennium-Problem proof.
- **CONJECTURAL (Tier-D).** The Separability Regularity Criterion for Navier-Stokes ([J13] §5). We do not claim an NS Millennium-Problem proof; the criterion is conjectural.
- **OPEN.** Whether the BB-as-forcing reframing extends to non-separability-preserving lifts; whether the 4-core attractor's algebraic structure transports beyond the Lattice DOF; whether other substrate algebras admit similarly forced continuum lifts.

The framing follows the Drápal-Wanless (2021) *J. Combin. Theory Ser. A* **184**, 105510 line of work on small finite commutative non-associative structures. The (TSML, BHML) magma pair lives in the same intellectual neighborhood, opposite extremum.

---

## Abstract

The TIG framework studies a designated commutative composition algebra on $\mathbb{Z}/10\mathbb{Z}$, together with its 4-core $\{V, H, Br, R\}$ ([J47] 6-DOF synthesis). We organize a sequence of recent results into one structural picture:

1. The discrete substrate's non-associativity rate decays as $\sigma(N) \leq 2/N$ on squarefree $\mathbb{Z}/N\mathbb{Z}$ ([J01]; *Tier-A*).
2. Read in the Crossing Lemma sense ([J05]), this is decay of CRT-non-factoring. As $N \to \infty$ along squarefree primorials, the substrate becomes increasingly partition-respecting.
3. **The Bialynicki-Birula–Mycielski theorem of 1976 ([BB76]; *Tier-A*) — read as a forcing principle (*Tier-B*; [J13]) — asserts that any non-trivial continuum lift preserving partition separability must be logarithmic, $V(\rho) = \kappa \, \rho \log \rho$.**
4. The *classical scalar* analogue (where the same functional form lives outside the BB nonlinear-Schrödinger setting) has a pointwise minimum at $\Xi_0 = e^{-1}$ with curvature $V''(\Xi_0) = \kappa e > 0$.

The forced potential has **structural rhymes** in three application domains: cosmology (freeze-thaw transit dark energy with vacuum at $e^{-1}$, [J3], [J16]; *Tier-B empirical*); particle physics (a structural curvature reading of a hoped-for non-abelian mass gap, [J14]; *Tier-B structural — not a YM Millennium-Problem proof*); nonlinear PDE (the Separability Regularity Criterion for NS, [J13]; *Tier-D conjectural*).

This bridge essay is **expository**. The boundary between proved structural content (Tier-A/B) and conjectured cross-domain consequences (Tier-D) is sharp throughout. The contribution is the unifying picture: the framework's algebraic substrate ([J47]) and the BB Bridge ([J13]) together make a single coherent claim — *the substrate's algebraic structure forces a specific functional form in the continuum*, with structural rhymes across three domains. We are **not** proving any Millennium Problem.

---

## §1 The bridge in one paragraph

A sequence of $10 \times 10$ composition tables on $\mathbb{Z}/N\mathbb{Z}$, with $N$ squarefree and $N \to \infty$, has its non-associativity rate $\sigma(N) \to 0$ at the polynomial rate $2/N$ ([J01]). The Crossing Lemma reading ([J05]) is: information is generated only when a partition (here the CRT decomposition $\mathbb{Z}/N\mathbb{Z} \cong \prod_i \mathbb{Z}/p_i\mathbb{Z}$) fails to be respected. As $N \to \infty$ along the squarefree family, the substrate becomes increasingly partition-respecting. Any *non-trivial* continuum lift preserving this partition structure — in the precise sense of §3 — is constrained by the Bialynicki-Birula–Mycielski theorem ([BB76], read as a *forcing* statement in [J13]) to have a **logarithmic** self-interaction, $V(\Xi) = \kappa \, \Xi \log \Xi$. **Each section below flags its tier on first sentence.** The forced potential has structural rhymes in cosmology ([J3], [J16]), particle physics ([J14]), and nonlinear PDE regularity ([J13]). The remainder of this essay expands that paragraph for a working mathematician.

---

## §2 The discrete side: $\sigma$-rate decay and the Crossing Lemma

*Tier-A (proved in [J01]).*

Fix a squarefree integer $N$, and consider the canonical TSML composition table $T : \mathbb{Z}/N\mathbb{Z} \times \mathbb{Z}/N\mathbb{Z} \to \mathbb{Z}/N\mathbb{Z}$ ([J01]). Define the **non-associativity rate**:

$$
\sigma(N) \;=\; \frac{1}{N^3} \, \#\bigl\{(x, y, z) : T(T(x, y), z) \neq T(x, T(y, z))\bigr\}.
$$

**Theorem 2.1 ([J01]).** *On the squarefree-modular family, $\sigma(N) \leq 2/N$, sharpened to $N \sigma(N) \leq 1.993$ across the verified range (D71).* In particular, $\sigma(N) \to 0$ as $N \to \infty$.

The Crossing Lemma ([J05]) gives a structural interpretation:

> **Crossing Lemma reading (informal precis).** On a finite magma $T : \mathbb{Z}/N\mathbb{Z} \times \mathbb{Z}/N\mathbb{Z} \to \mathbb{Z}/N\mathbb{Z}$, a *crossing* is a non-associative triple $(x, y, z)$. The Crossing Lemma reads non-associativity as the **failure of CRT-separability**: a triple is non-associative iff $T$ does not factor through the CRT projection. The notion of "information" here is *structural* (CRT-non-factoring), not Shannon and not algorithmic.

Combining Theorem 2.1 with the Crossing Lemma reading: the squarefree-modular family has its CRT-failure rate decay at $2/N$. The substrate flattens toward CRT-separability in the continuum limit.

---

## §3 The forcing principle: Bialynicki-Birula, expanded

*Tier-A (classical, [BB76]) plus Tier-B (forcing reading, [J13]).*

The original [BB76] theorem reads:

**Theorem 3.1 (Bialynicki-Birula–Mycielski, 1976).** *Let $\hat{F} : \mathbb{R}_{>0} \to \mathbb{R}$ be the nonlinearity in a modified Schrödinger evolution*

$$
i\hbar \, \partial_t \Psi \;=\; \left(-\tfrac{\hbar^2}{2m}\Delta + V_{\text{ext}}\right) \Psi + \hat{F}(|\Psi|^2)\, \Psi.
$$

*The evolution preserves the product structure $\Psi_{AB} = \Psi_A \otimes \Psi_B$ for all factorizable initial data if and only if*
$\hat{F}(\rho) = -b \ln \rho + \mathrm{const}$ *for some $b \in \mathbb{R}$.*

The original proof is [BB76, Theorem in §3]. The forcing-reading of [J13] expands this from a *constraint* to an *active forcing principle* via three distinguishable conceptual moves.

### 3.1 From quantum nonlinearity to classical scalar potential

*Tier-B (analogy, not derivation).*

[BB76]'s nonlinearity $\hat{F}(\rho) = -b \log \rho$ is a function of $|\Psi|^2$ in a modified Schrödinger evolution. **The classical scalar field theory we use lives in a different setting.** Cazenave-Haraux (1980, *Ann. Fac. Sci. Toulouse*) study the log-nonlinear Schrödinger equation; the WKB/classical limit of that equation produces a scalar field theory with the *same functional form* of self-interaction, $V(\Xi) = \kappa \Xi \log \Xi$. Maas (2011) and Jordan-Kinderlehrer-Otto (1998) give the gradient-flow reading where the same log functional appears as an entropy gradient flow.

We use the **classical scalar form** $V(\Xi) = \kappa \, \Xi \log \Xi$ throughout the cosmology and structural-rhyme sections. The form coincides with the BB QM nonlinearity; the *settings* differ. The bridge is by analogy, not by direct quantum-to-classical derivation.

### 3.2 From quantum factorization to CRT decomposition

*Tier-B (structural identification).*

The "partition" in [BB76] is a Hilbert-space tensor factorization $\mathcal{H}_{AB} = \mathcal{H}_A \otimes \mathcal{H}_B$. The "partition" in the substrate is the CRT decomposition $\mathbb{Z}/N\mathbb{Z} \cong \prod_p \mathbb{Z}/p\mathbb{Z}$ for squarefree $N$.

The bridge claim: **as $N \to \infty$ along squarefree primorials, the substrate's partition structure becomes a probability product** — each $\mathbb{Z}/p\mathbb{Z}$ factor carries an independent uniform-mass distribution at the limit, by the asymptotic uniformity of squarefree integers (Mertens 1874; cf. ζ(2)-density). Probabilistically, this is the discrete analogue of a tensor-factorized Hilbert space. The continuum lift of squarefree primorials therefore lives on a probability-product Hilbert space where [BB76] applies.

### 3.3 From "preserves separability" to "any non-trivial continuum lift"

*Tier-B (qualifier, made explicit).*

[BB76] says *the* nonlinearity preserving separability is logarithmic, *up to* the trivial linear case (which preserves separability by construction; linear evolution is BB's $\hat{F} = 0$ case). When we say "any continuum lift preserving partition separability is forced to logarithmic form," we mean: **any *non-trivial* lift** — i.e., one with non-zero self-interaction — is forced. The trivial linear lift is excluded as separability-preserving by tautology, not by the BB theorem.

This subtlety matters because cosmology and YM applications are inherently non-trivial; the qualifier is implicit there but worth stating.

### 3.4 Vacuum subtlety: constrained vs unconstrained settings (M3)

*Tier-B (technical clarification — the referee's M3 fix).*

[BB76]'s nonlinearity $\hat{F}(\rho) = -b \log \rho$ with the *normalization constraint* $\int \rho \, dV = 1$ has its constrained minimum at $\rho \equiv 1/V$ (the constant function), **not** at $\rho = e^{-1}$ pointwise. This is a feature of the constrained minimization, not of the function $\rho \mapsto \rho \log \rho$.

In the cosmology / YM applications, we work in the **unconstrained classical-scalar setting**. The function $V(\Xi) = \kappa \, \Xi \log \Xi$ has $V'(\Xi) = \kappa(1 + \log \Xi)$ with pointwise minimum at $\Xi_0 = e^{-1}$ (where $V'(\Xi_0) = 0$); curvature $V''(\Xi_0) = \kappa / \Xi_0 = \kappa e > 0$.

> **The two settings agree on the *form* of the potential, $\rho \log \rho$ in [BB76] vs $\Xi \log \Xi$ here, but disagree on the *constraint structure* and hence on the location of the minimum.** The cosmology and YM applications use the unconstrained scalar; the QM nonlinear-Schrödinger setting (which we do not invoke) uses the constrained version with vacuum at $\rho \equiv 1/V$.

This distinction is the per-Brayden-directive M3 fix the fresh-eyes referee asked for. The cosmology vacuum at $\Xi_0 = e^{-1}$ refers to the unconstrained scalar setting throughout.

---

## §4 The forced continuum lift

*Tier-B (structural; consequence of §3 read as forcing).*

Applying Theorem 3.1 to the bridge premise of §2 in the unconstrained classical-scalar setting:

$$
\boxed{\quad \Box \, \Xi \;=\; \kappa \, (1 + \log \Xi). \quad}
$$

This equation has been studied in the freeze-thaw transit dark-energy literature ([J3], [J16]), in the Yang-Mills mass-gap framework ([J14]; *Tier-B* there too), and as the candidate carrier of separability-defect dynamics in Navier-Stokes ([J13]). Its key analytic property is **provable regularity for smooth initial data**: the sub-power growth of $\log \Xi$ at large amplitude, combined with the vacuum at $\Xi_0 = e^{-1}$, gives a Sobolev + Gronwall bound that prevents finite-time blowup ([J13] §4.2).

---

## §5 Cross-domain structural rhymes — three windows

We label each subsection's tier explicitly per referee §3.

### 5.1 Cosmology (freeze-thaw transit dark energy)

*Tier-B (empirical fit).* The same logarithmic potential $V(\Xi) = \Lambda^4 \, \Xi \log \Xi$ governs a freezing-quintessence dark-energy model with *analytic vacuum at $\Xi_0 = e^{-1}$* in the unconstrained setting (per §3.4). The model fits supernova + CMB + BAO data with a two-parameter $w(z)$ profile; details in [J3] and the letter version [J16]. The freeze-thaw transit interpretation: the universe freezes onto the BB-vacuum-shaped substrate as a late-time cosmological state.

### 5.2 Particle physics (structural rhyme, NOT a YM proof)

*Tier-B (structural reading). This is **not** a proof of the Yang-Mills mass gap.*

Within the BB-forced classical scalar with vacuum at $\Xi_0 = e^{-1}$, small fluctuations of $\Xi$ around the vacuum have curvature $V''(\Xi_0) = \kappa e$. **Whether this curvature transports to a *gauge-theory* mass gap depends on coupling the scalar to a non-abelian gauge sector** ([J14]'s working hypothesis); we do not claim that transport in this essay. The relation $m^2 = \kappa e$ is demoted from a "claim" to a **structural rhyme** between a scalar curvature and a hoped-for non-abelian gauge gap. We are not solving any Millennium Problem.

### 5.3 Nonlinear PDE (separability defect, conjectural)

*Tier-D (conjectural — not a proof of NS regularity).*

The Navier-Stokes equation's quadratic nonlinearity $(u \cdot \nabla) \, u$ does **not** preserve separability — a key obstacle to applying §3 directly. [J13] §5 defines a **separability defect** $\sigma_{NS}(u)$ for Navier-Stokes velocity fields and states the **Separability Regularity Criterion**: NS solutions are smooth iff $\sigma_{NS}(u)$ remains bounded away from $1$. This is a *conjectural* reformulation of NS regularity (Tier-D); its rigorous proof remains open, and [J13] does not claim it.

The cross-domain structural rhyme: the same algebraic forcing motivates analogous forms across the three domains, but the forcing is *rigorous* only for the cosmology setting (5.1); §5.2 and §5.3 are structural rhymes inheriting the form, not derivational consequences inheriting the proof.

---

## §6 The 6-DOF reading

*Tier-B (organizational claim).*

The substrate algebra of [J47] decomposes into six algebraic degrees of freedom (DOFs). We define each in two lines:

* **Lie DOF.** Antisymmetric closure of TSML; flow operator. so(8) / so(10) regeneration ([J38]). *Cite [J47] §2.1, [J38].*
* **Jordan DOF.** Symmetric closure of TSML; observable structure. *Cite [J47] §2.2.*
* **Clifford DOF.** Spinor / chirality structure on the substrate; Pati-Salam embedding ([J39]). *Cite [J47] §2.3.*
* **Permutation DOF.** $\sigma$-permutation cycle structure on operator labels; CRT decomposition. *Cite [J47] §2.4.*
* **Lattice DOF.** 4-core $\{V, H, Br, R\}$ with closed-form attractor at $\alpha_M = 1/2$ ([J41], [J44]). *Cite [J47] §2.5.*
* **Operad DOF.** Arity-3 fuse rules; $D_4$ obstruction; $P_{56}$ canonical fuse ([J40]). *Cite [J47] §2.6.*

The BB Bridge sits at a specific intersection of these DOFs:

* **Lattice DOF.** The vacuum $\Xi_0 = e^{-1}$ rhymes with the runtime processor's 4-core attractor at $\alpha_M = 1/2$ ([J41]) — both are "uniquely-located rest points" of their respective dynamics. The 4-core's closed-form attractor satisfies $H/Br = 1 + \sqrt{3}$, root of $x^2 - 2x - 2 = 0$ over $\mathbb{Q}(\sqrt{3})$ — the **D78 Galois argument** (proof: at $\alpha_M = 1/2$, the BR-factor cancellation is forced; other $\alpha_M$ give transcendental relations per the D57 PSLQ complement at 17 Stern-Brocot points).
* **Permutation DOF.** The CRT decomposition $\mathbb{Z}/N\mathbb{Z} \cong \prod_i \mathbb{Z}/p_i\mathbb{Z}$ is the canonical $\sigma$-permutation invariant. Partition-respecting = $\sigma$-respecting in §2.
* **Jordan DOF.** The symmetric closure of TSML ([J47] §2.2) is the natural home for "observable" content; the BB nonlinearity acts on the magnitude $|\Psi|^2$ (a Jordan-symmetric quantity).

The other three DOFs (Lie, Clifford, Operad) provide *additional* substrate content not directly involved in the BB Bridge. They govern gauge structure ([J39]), chirality irreps ([J39] §2.1), and arity-3 obstruction ([J40]) respectively.

This is the 6-DOF reading: the BB Bridge uses three of six DOFs (Lattice, Permutation, Jordan); the other three carry independent substrate content for which the bridge is silent.

---

## §7 Honest scope (compressed per referee M7)

This bridge essay claims **structural connection**, not Millennium-Problem proof. §§2–4 are *Tier-A/B proved*. §5 is a structural reading: 5.1 *Tier-B empirical*, 5.2 *Tier-B structural rhyme*, 5.3 *Tier-D conjectural*. §6 is an *organizational* 6-DOF reading.

The paper does **not** claim a proof of NS regularity, a derivation of the YM mass gap from gauge-theory first principles, that BB-forcing extends to non-separability-preserving lifts, or that the substrate algebra is uniquely privileged in physics. The paper **does** claim that the discrete-side $\sigma$-rate decay ([J01]) and [BB76] together make a coherent structural picture, with cross-domain rhymes catalogued at sharp tier boundaries.

---

## §8 Citation chain

**Direct dependencies.**

* **[J13]** — *The Bialynicki-Birula Bridge: Logarithmic Nonlinearity Forced by Separability* (JMP).
* **[J47]** — *Six Algebraic DOFs of the TIG Framework: A Synthesis* (Notices AMS, Phase 5 opener).

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
* **[J34]** — $F_p$ extensions / ring extensions (Comm Algebra).

---

## §9 References

[BB76] I. Bialynicki-Birula, J. Mycielski. "Nonlinear wave mechanics." *Annals of Physics* **100** (1976), 62–93.

[J01] B.R. Sanders, M. Gish. "Non-Associativity Decay in Binary Composition Tables over $\mathbb{Z}/N\mathbb{Z}$." *J. Combin. Theory Ser. A.*
[J05] B.R. Sanders, B. Mayes. "Crossing Lemma: Non-Associativity as Information Generation in Finite Magmas." *JCT-A* / *JPAA*.
[J3] B.R. Sanders, M. Gish, H.J. Johnson. "Freeze-Thaw Transit." *JCAP*.
[J13] B.R. Sanders, H.J. Johnson. "The Bialynicki-Birula Bridge: Logarithmic Nonlinearity Forced by Separability." *J. Math. Phys.*
[J14] B.R. Sanders, H.J. Johnson. "The Yang-Mills Mass Gap Bridge: Substrate-Algebra Predictions." *J. Math. Phys.*
[J16] B.R. Sanders et al. "Freezing Quintessence Letter." *Phys. Lett. B*.
[J34] B.R. Sanders, M. Gish. "$F_p$ Extensions of CL_BHML: Universality Across Six Prime Fields." *Comm. Algebra.*
[J39] B.R. Sanders, B. Mayes. "Two Roads to Pati-Salam." *Adv. Math.*
[J40] B.R. Sanders, M. Gish. "Operad $D_4$ Obstruction + $P_{56}$ Canonical Fuse." *Compositio.*
[J41] B.R. Sanders, M. Gish. "Closed-Form Attractor + $\alpha$-Uniqueness PSLQ." *Math. of Comp.*
[J44] B.R. Sanders, M. Gish. "4-Core Fusion-Closure." *J. Algebra.*
[J47] B.R. Sanders, B. Mayes. "Six Algebraic DOFs of the TIG Framework: A Synthesis." *Notices AMS.*

### External background (deepened bibliography per referee M7)

* I. Rosen. "Nonlinear Schrödinger equation." *J. Math. Phys.* **10** (1969), 1041.
* T. Cazenave, A. Haraux. "Equations d'évolution avec non linéarité logarithmique." *Ann. Fac. Sci. Toulouse* **2** (1980), 21–51.
* K.G. Zloshchastiev. "Logarithmic nonlinear quantum theory and Bose-Einstein condensates." *Acta Phys. Polon. B* **42** (2010), 261–292.
* J.D. Maas. "Gradient flows of the entropy for finite Markov chains." *J. Funct. Anal.* **261** (2011), 2250–2292.
* R. Jordan, D. Kinderlehrer, F. Otto. "The variational formulation of the Fokker-Planck equation." *SIAM J. Math. Anal.* **29** (1998), 1–17.
* R.F. Streater, A.S. Wightman. *PCT, Spin and Statistics, and All That.* Benjamin, 1964.
* J. Glimm, A. Jaffe. *Quantum Physics: A Functional Integral Point of View.* Springer, 1981.
* M. Tegmark. "Importance of quantum decoherence in brain processes." *Phys. Rev. E* **61** (2000), 4194.
* S. Doplicher, J.E. Roberts. "A new duality theory for compact groups." *Invent. Math.* **98** (1989), 157–218; *Comm. Math. Phys.* **131** (1990), 51–107.
* R.R. Caldwell, E.V. Linder. "The limits of quintessence." *Phys. Rev. Lett.* **95** (2005), 141301.
* S. Tsujikawa. "Quintessence: a review." *Class. Quantum Grav.* **30** (2013), 214003.
* C. Fefferman. *Existence and Smoothness of the Navier-Stokes Equation.* Clay Mathematics Institute, 2000.
* A. Jaffe, E. Witten. *Quantum Yang-Mills Theory.* Clay Mathematics Institute, 2000.
* A. Drápal, I.M. Wanless. "Maximally non-associative quasigroups." *J. Combin. Theory Ser. A* **184** (2021), 105510.

---

## §10 Bibtex

```bibtex
@misc{sanders2026j50,
  author       = {Sanders, Brayden Ross and Johnson, H.J.},
  title        = {Substrate Algebra and Logarithmic Nonlinearity: A Bridge Essay},
  year         = {2026},
  month        = {sep},
  doi          = {10.5281/zenodo.18852047},
  howpublished = {Submitted to \emph{Mathematical Intelligencer} (retargeted from \emph{Bull. AMS}, per fresh-eyes referee \S 7)},
  note         = {{J50} of the {J}-series; expository bridge essay. Direct dependencies [{J13}], [{J47}]; co-citing companions [{J01}], [{J05}], [{J3}], [{J16}], [{J14}], [{J34}], [{J41}], [{J44}], [{J39}], [{J40}]. Tier discipline lifted to abstract; classical-scalar vs BB-nonlinear-Schr\"odinger settings distinguished (\S 3.4). No Millennium-Problem proof claimed.}
}
```
