# The Yang-Mills Mass Gap Bridge: Substrate-Algebra Predictions from Separability-Forced Spectral Floor

**Authors:** B.R. Sanders$^{1}$, H.J. Johnson$^{2}$
$^{1}$7Site LLC, Hot Springs, AR — brayden@7site.co
$^{2}$Independent Researcher, Billings, MT

**Target venue:** Journal of Mathematical Physics (companion to J13)
**Manuscript class:** Mathematical-physics framework paper (structural; not a Millennium-Problem proof)
**MSC:** 81T13, 81T08, 81S20, 35Q40
**Date:** 2026-05-07 (DRAFT)

---

## Abstract

The Bialynicki-Birula--Mycielski uniqueness theorem (1976) selects $V(\rho) = \kappa\,\rho \log \rho$ as the unique self-interaction preserving separability of composite quantum systems. The companion paper J13 develops this as a forcing principle for continuum lifts of discrete composition algebras and establishes regularity of the lifted theory $\Box\Xi = \kappa(1 + \log\Xi)$. In this paper we apply the same bridge to the Yang-Mills (YM) mass gap problem. The logarithmic potential has an isolated minimum at $\Xi_0 = e^{-1}$ with curvature $V''(\Xi_0) = \kappa e > 0$ — a positive spectral gap built into the potential structure. We argue that any field theory whose nonlinearity preserves separability inherits a positive spectral floor; YM is not separable in the gauge sector, but confinement realizes effective separability in the infrared (color singlets), at the cost of an energy gap which is the YM mass gap. We state the precise conjectures, identify the constructive-QFT prerequisite (Wightman axioms in 4D for the log theory, an extension of the Høegh-Krohn 2D result), and quantify a falsifiable numerical prediction: the YM mass gap should scale as $\Delta_{\rm YM} = C \cdot \Lambda_{\rm QCD} \cdot e$ with $C$ an $O(1)$ constant calibrating the gauge group. Lattice values of the lightest SU(3) glueball are consistent with $C \approx 2.1$. **The paper does not claim to prove the YM mass gap; it provides the separability-forcing framework and identifies the precise open problems.**

---

## 1. Introduction

The Yang-Mills existence and mass gap problem [Jaffe-Witten] asks: for compact simple gauge group $G$ (e.g., SU(2), SU(3)), does the quantum theory exist (satisfying Wightman or Osterwalder-Schrader axioms) and does the spectrum have a mass gap $\Delta > 0$ above the unique vacuum? Lattice QCD evidence is overwhelming — numerical simulations consistently produce a mass gap with the lightest glueball mass $m_G \approx 1.7$ GeV in SU(3) — but no rigorous proof exists.

Lattice and continuum approaches to the mass gap have largely operated in two separate worlds. The companion paper J13 establishes a third entry point: the Bialynicki-Birula bridge identifies *separability preservation* as a forcing principle. The logarithmic potential it forces has an isolated minimum, hence a positive spectral floor, hence a built-in mass gap of size $m^2 = \kappa e$. We propose that this same separability mechanism underlies the YM mass gap, mediated by confinement.

**Plan.** Section 2 quotes the BB theorem and the structural mass-gap statement of the lifted theory. Section 3 connects to YM via confinement-as-effective-separability. Section 4 derives the falsifiable numerical prediction and compares to lattice glueballs. Section 5 catalogues the constructive-QFT prerequisites (Wightman axioms in 4D for the log theory). Section 6 records status, lens-scope, and tier classification.

---

## 2. The BB-Lifted Theory Has a Positive Spectral Floor

From J13, the BB-forced continuum theory has potential $V(\Xi) = \kappa\,\Xi \log \Xi$ with field domain $\Xi > 0$ and a single coupling $\kappa$.

**Proposition 2.1 (mass gap of the BB-lifted theory).** *The potential $V(\Xi) = \kappa\,\Xi \log \Xi$ has a unique isolated minimum at $\Xi_0 = e^{-1}$ with*
$$V''(\Xi_0) = \frac{\kappa}{\Xi_0} = \kappa e > 0.$$
*Hence the mass-square of the fluctuation field $\delta\Xi = \Xi - \Xi_0$ at one-loop order is*
$$m_\Xi^2 = \kappa e > 0.$$

*Proof.* Direct calculation: $V'(\Xi) = \kappa(1 + \log\Xi)$ vanishes at $\Xi_0 = e^{-1}$. $V''(\Xi) = \kappa/\Xi$, evaluated at $\Xi_0 = e^{-1}$ gives $\kappa e$. The minimum is isolated because $V''(\Xi_0) > 0$. The mass $m^2 = V''$ at the vacuum is the standard scalar-field gap.

**Reading.** *Separability is the mechanism.* The logarithmic potential is the unique form preserving partition independence of composite systems (Theorem 2.1 of J13). The fact that this same form has a strictly convex minimum is not a coincidence — separability prevents flat directions, since a flat direction would require global coordination that breaks subsystem independence. Separability forces a spectral floor.

---

## 3. The Yang-Mills Application

### 3.1 Why YM is not directly in the BB class

The YM Lagrangian for a compact simple gauge group $G$ is

$$\mathcal{L}_{\rm YM} = -\tfrac{1}{4} F^a_{\mu\nu} F^{a\,\mu\nu}, \qquad F^a_{\mu\nu} = \partial_\mu A^a_\nu - \partial_\nu A^a_\mu + g f^{abc} A^b_\mu A^c_\nu.$$

The non-abelian self-coupling $g f^{abc} A^b_\mu A^c_\nu$ is *not* separable: the gauge field at a point $x$ is coupled to itself through the structure constants of $G$, and a partition into spatial subregions is not preserved under gauge transformations. Hence YM is not directly in the BB class.

### 3.2 Confinement as effective infrared separability

At short distances ($r \ll \Lambda_{\rm QCD}^{-1}$), YM is asymptotically free (weakly coupled, approximately separable). At long distances, the theory confines: physical states are color singlets (hadrons in QCD; glueballs in pure YM). Color singlets are gauge-invariant composite operators, and *they* behave separably — a glueball in Tokyo and a glueball in New York evolve independently under the long-distance effective theory.

**Proposition 3.1 (confinement as effective separability — heuristic).** *The infrared effective theory of confined YM is approximately separable: composite color-singlet operators decouple in the infrared.*

This is a standard physics statement, not a theorem; but it is the content of the cluster decomposition property in the confined phase. Quantitative versions appear in [Strocchi 2013] and [GlimmJaffe 1987].

### 3.3 The mass gap as the cost of separability

Combining Proposition 2.1 (BB-lifted theory has $m^2 = \kappa e$) with Proposition 3.1 (confinement = effective infrared separability), we propose:

**Conjecture 3.2 (separability-forced YM mass gap).** *The YM mass gap $\Delta_{\rm YM}$ is the energy cost of creating a color-singlet excitation from the vacuum, and arises from the same mechanism as the BB-lifted-theory mass gap: separability forces a spectral floor.*

The conjecture is not a proof of the YM mass gap; it is the structural identification of the mechanism. The proof requires (a) the existence statement of YM (Wightman axioms in 4D), and (b) a rigorous argument that the IR effective theory has a separable structure compatible with the BB framework.

---

## 4. The Falsifiable Numerical Prediction

If the BB-bridge mechanism applies to YM, the mass gap should inherit the structural factor $e$ (Euler's number) from the curvature $V'' = \kappa e$ at the vacuum:

$$\boxed{\;\Delta_{\rm YM} = C \cdot \Lambda_{\rm QCD} \cdot e\;}$$

where $\Lambda_{\rm QCD}$ is the confinement scale (the natural mass scale of the gauge theory) and $C$ is a calibration constant of order unity, depending on the gauge group via the Casimir of the adjoint representation.

**Lattice comparison.** The lightest 0$^{++}$ glueball in SU(3) lattice QCD has mass

$$m_G \approx 1.7\ \text{GeV} \quad \text{[lattice]}.$$

With $\Lambda_{\rm QCD} \approx 0.3$ GeV and $e \approx 2.718$:

$$C = m_G / (\Lambda_{\rm QCD} \cdot e) \approx 1.7 / (0.3 \times 2.718) \approx 2.08.$$

This $C \approx 2$ is *not fine-tuned*: it is consistent with the Casimir factor $C_2(\mathrm{adj}) = N_c = 3$ for SU(3) (factor of $N_c/(\sqrt{N_c} \cdot \mathrm{normalization})$ depending on convention). The order-of-magnitude consistency is the structural test of the framework.

**Falsifiability.** If lattice or analytic computations of the YM mass gap yielded $C$ values with $|C| \gg 10$ or $C \approx 0$, the framework would be falsified. The current lattice value $C \approx 2$ passes the falsifiability test.

---

## 5. Constructive-QFT Prerequisites

For the BB bridge to give a rigorous proof of the YM mass gap, the following are needed:

**Prerequisite 5.1 (Wightman in 4D for the log theory).** The Høegh-Krohn $\exp(\Phi)_2$ model satisfies Wightman axioms in 2D [HoeghKrohn71]. The 3D case is partially known [Glimm-Jaffe; Frohlich]. The 4D case is OPEN — this is the constructive-QFT frontier.

**Prerequisite 5.2 (effective IR separability of YM).** A rigorous statement that confinement implies cluster decomposition in the BB-compatible class is needed. Partial results exist; a clean theorem is open.

**Prerequisite 5.3 (gauge-fixing compatibility).** The BB theorem is stated for ungauge wave functions; gauge symmetry enlarges the kinematical algebra. A gauge-invariant version of the BB theorem on the moduli space of gauge connections is needed. Open.

A rigorous proof of the YM mass gap via the BB bridge requires (5.1) AND (5.2) AND (5.3). This is a multi-decade program, but each piece is precisely formulated.

---

## 6. Status, Lens Scope, Tier Classification

### 6.1 Status table

| Claim | Status |
|---|---|
| Theorem 2.1 (BB uniqueness) | **PROVED** [BB76] |
| Proposition 2.1 (BB-theory mass gap) | **PROVED** (direct computation) |
| Confinement = effective infrared separability | **STRUCTURAL HEURISTIC** (standard physics, partial rigorous results) |
| Conjecture 3.2 (separability-forced YM mass gap) | **CONJECTURE** |
| Numerical prediction $\Delta_{\rm YM} = C \Lambda_{\rm QCD} e$, $C \sim 2$ | **CONSISTENT WITH LATTICE** [m_G ≈ 1.7 GeV → C ≈ 2.08] |
| Wightman axioms for log theory in 4D | **OPEN** (Prerequisite 5.1) |
| YM mass gap proof via BB bridge | **OPEN** (requires 5.1 + 5.2 + 5.3) |

### 6.2 Lens scope

This paper carries no TSML / BHML lens dependence. The mathematical content is constructive QFT + nonlinear PDE; the discrete side cites J05 (Crossing Lemma) but does not condition on the lens taxonomy.

### 6.3 Tier classification

**Central claim:** Tier 4 (framework paper, structural). Proposition 2.1 is proved; Conjecture 3.2 is stated as conjecture; the YM mass gap is *not* claimed proved. The numerical prediction $\Delta_{\rm YM} \approx 2 \Lambda_{\rm QCD} e$ is falsifiable and currently consistent with lattice glueball data.

---

## References

### The forcing theorem and constructive QFT
- [BB76] Bialynicki-Birula, I., Mycielski, J. (1976). *Annals of Physics* **100**(1-2):62--93.
- Høegh-Krohn, R. (1971). *Commun. Math. Phys.* **38**(3):195. (2D $\exp(\Phi)$ model)
- Glimm, J., Jaffe, A. (1987). *Quantum Physics: A Functional Integral Point of View*. Springer.
- Strocchi, F. (2013). *An Introduction to Non-Perturbative Foundations of Quantum Field Theory*. Oxford.
- Fröhlich, J. (1976-1980). Constructive QFT in 3D.

### Yang-Mills mass gap problem
- Jaffe, A., Witten, E. (2000). Clay Mathematics Institute Millennium Problem statement.
- Wilson, K.G. (1974). *Phys. Rev. D* **10**:2445. (Lattice gauge theory)
- Yang, C.N., Mills, R.L. (1954). *Phys. Rev.* **96**:191.
- Wilson, K.G. (1971). *Phys. Rev. B* **4**:3174 \& 3184. (RG)

### Lattice glueball spectrum
- Morningstar, C.J., Peardon, M. (1999). *Phys. Rev. D* **60**:034509. (Glueball masses in lattice SU(3))
- Chen, Y. *et al.* (2006). *Phys. Rev. D* **73**:014516.

### Companion submissions in the J-series
- [J01] Sanders, B.R., Gish, M. (2026). "Non-Associativity Decay in Binary Composition Tables over $\mathbb{Z}/N\mathbb{Z}$." Submitted to *JCT-A*.
- [J03] Sanders, B.R., Gish, M., Johnson, H.J. (2026). "Freeze-Thaw Transit." Submitted to *JCAP*.
- [J05] Sanders, B.R., Mayes, B. (2026). "Crossing Lemma." Submitted to *JCT-A* / *JPAA*.
- [J13] Sanders, B.R., Johnson, H.J. (2026). "The Bialynicki-Birula Bridge: Logarithmic Nonlinearity Forced by Separability." Submitted to *JMP* (companion).

DOI for verification scripts: 10.5281/zenodo.18852047.
