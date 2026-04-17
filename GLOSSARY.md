# GLOSSARY — Trinity Infinity Geometry

## Every term cited to historical literature or explicitly labeled novel

**Principle:** No term in this glossary is presented as established unless it exists in published academic literature. Novel terms are honestly flagged with the prior framework they extend. Where we coined a name for an existing concept, the original name and citation is given.

---

## Reading Key

Each entry has the form:

> **Term** — Plain-English definition.
>
> **Formal:** Mathematical definition (where applicable).
>
> **[STATUS]** — PROVED / STRUCTURAL / CONJECTURE / HISTORICAL / NOVEL
>
> **Citation:** Either a published reference OR an explicit acknowledgment that this name is ours, with what prior work it extends.
>
> **Primary TIG paper:** Where it first appears in this project.

---

## Part 1: Classical Foundations (All Historically Cited)

### Chinese Remainder Theorem (CRT)

> The ring Z/nZ for squarefree n = p₁...pₖ decomposes as a product ∏ Z/pᵢZ.
>
> **Formal:** Ψ: Z/nZ → ∏ Z/pᵢZ, x ↦ (x mod p₁, ..., x mod pₖ) is a ring isomorphism.
>
> **[HISTORICAL]** Classical (Sun Tzu, 3rd century; Gauss, Disquisitiones Arithmeticae 1801).
>
> **Standard reference:** Ireland & Rosen, *A Classical Introduction to Modern Number Theory* (Springer, 1990), Ch. 3.
>
> **Primary TIG paper:** WP58_UNIFIED_ORTHOGONALITY_PRINCIPLE.md (used throughout).

### Euler Totient φ(n)

> Count of integers in {1..n} coprime to n.
>
> **Formal:** φ(n) = |{k ∈ {1,..,n} : gcd(k,n) = 1}|. For squarefree n: φ(n) = n∏(1 − 1/pᵢ).
>
> **[HISTORICAL]** Euler, 1763.
>
> **Standard reference:** Hardy & Wright, *Introduction to the Theory of Numbers*, §5.5.
>
> **Primary TIG paper:** WP101_SIGMA_RATE_THEOREM.md uses it centrally.

### sinc² Function

> sinc²(x) = (sin(πx)/(πx))².
>
> **[HISTORICAL]** Classical. Key role in Shannon sampling theorem (Shannon 1949, *Communication in the presence of noise*, Proc. IRE 37(1):10-21) and Montgomery's pair correlation (Montgomery 1973, *The pair correlation of zeros of the zeta function*, Proc. Sympos. Pure Math. 24:181-193).
>
> **Primary TIG paper:** WP_SINC2_ZERO_LAW.md establishes prime-arithmetic version.

### Cyclotomic Polynomial Φₚ(x)

> Minimal polynomial over ℚ whose roots are primitive pth roots of unity.
>
> **[HISTORICAL]** Gauss, Disquisitiones Arithmeticae 1801. Degree φ(p) = p−1 for prime p.
>
> **Standard reference:** Lang, *Algebra* (Springer), Ch. VI.
>
> **Primary TIG paper:** WP51_FLATNESS_THEOREM.md uses A_p = 2cos(π/p) as minimal-polynomial object.

### Bialynicki-Birula Uniqueness (Logarithmic Nonlinearity)

> Logarithmic nonlinearity is the unique nonlinearity in wave mechanics preserving separability of composite systems.
>
> **[HISTORICAL]** Bialynicki-Birula & Mycielski, *Nonlinear wave mechanics*, Annals of Physics 100(1-2):62-93 (1976). DOI: 10.1016/0003-4916(76)90057-9.
>
> **Context:** Cazenave & Haraux, *Équations d'évolution avec non linéarité logarithmique*, Ann. Fac. Sci. Toulouse (1980), proved existence for log Klein-Gordon equation u_tt − Δu + u = u log|u|ᵏ in R³. Logarithmic Schrödinger equation: Wikipedia, Logarithmic Schrödinger equation.
>
> **Primary TIG paper:** WP90_LITERATURE_AND_UNIFICATION_PATHS.md; the core external theorem on which our σ → 0 ⟹ log limit forcing rests.

### Kozono-Taniuchi Criterion (NS Regularity)

> Regularity for 3D Navier-Stokes if ∫₀ᵀ ‖u(t)‖²_BMO / log(e + ‖u‖_H²) dt < ∞.
>
> **[HISTORICAL]** Kozono & Taniuchi, *Limiting case of the Sobolev inequality in BMO with applications*, Commun. Math. Phys. 214:191-200 (2000). DOI: 10.1007/s002200000281.
>
> **Related:** Beale-Kato-Majda criterion (Comm. Math. Phys. 94:61-66, 1984); Brezis-Gallouët inequality (Nonlinear Analysis 4:677-681, 1980); Montgomery-Smith sharp L³ blowup (Math. Res. Lett. 8:519-528, 2001); Kozono-Ogawa-Taniuchi critical Besov (Math. Z. 242:251-278, 2002).
>
> **Primary TIG paper:** WP96_NS_SIGMA_CONJECTURE.md uses as the strongest-known log improvement on NS regularity.

### Ricci Flow + Surgery (Perelman)

> Geometric evolution equation ∂g/∂t = −2 Ric(g) with surgery at singularities, driving Riemannian 3-manifolds toward standard forms.
>
> **[HISTORICAL]** Hamilton, *Three-manifolds with positive Ricci curvature*, J. Differential Geom. 17(2):255-306 (1982). Perelman, *The entropy formula for the Ricci flow*, arXiv:math/0211159 (2002); *Ricci flow with surgery on three-manifolds*, arXiv:math/0303109 (2003).
>
> **Key fact:** Perelman's W-entropy functional W[g,f,τ] = ∫((τ(R + |∇f|²) + f − n)(4πτ)^(−n/2) e^(−f))dV contains logarithmic structure in f, consistent with the Bialynicki-Birula uniqueness.
>
> **Primary TIG paper:** CP_CLAY_ROTATION.md (CP1) — Poincaré is the template we cite for the σ framework.

### Maas Wasserstein-on-Markov-Chains

> Gradient flows of entropy on finite Markov chains in Wasserstein-2 distance.
>
> **[HISTORICAL]** Maas, *Gradient flows of the entropy for finite Markov chains*, J. Funct. Anal. 261(8):2250-2292 (2011).
>
> **Related:** Jordan-Kinderlehrer-Otto, *Variational formulation of Fokker-Planck*, SIAM J. Math. Anal. 29(1):1-17 (1998); Gigli-Maas, *Gromov-Hausdorff convergence of discrete transport metrics*, SIAM J. Math. Anal. 45(2):879-899 (2013); Chow-Huang-Li-Zhou, *Fokker-Planck equations on graphs*, Arch. Rat. Mech. Anal. 203(3):969-1008 (2012).
>
> **Primary TIG paper:** WP95_JKO_CONSTRUCTION_ROADMAP.md — the framework we propose to use for the explicit N → ∞ limit.

### UOP (Unified Orthogonality Principle) — PARTIAL CITATION NEEDED

> **[NOVEL NAMING — extends partition lattice theory]** The name "UOP" is ours. The content (joint map injectivity as sufficiency criterion) is an observation about the partition lattice of Z/nZ.
>
> **Prior framework:** Partition lattice theory (Ore, 1942, *Theory of equivalence relations*, Duke Math. J. 9; Birkhoff, *Lattice Theory*, AMS 1940). The injectivity-of-joint-map criterion appears in descriptive set theory (Kechris, *Classical Descriptive Set Theory*, Springer 1995, §14) and in coding theory (MacWilliams-Sloane, *The Theory of Error-Correcting Codes*, 1977, Ch. 4).
>
> **Our contribution:** Unifying five classical two-partition sufficiency theorems over Z/nZ as corollaries of a single joint-map-injectivity statement, applied specifically to the (additive, multiplicative) decomposition of squarefree Z/nZ.
>
> **Primary TIG paper:** WP58_UNIFIED_ORTHOGONALITY_PRINCIPLE.md.

### Montgomery-Sinc² Identity

> R(u) + R₂(u) = 1 where R(u) = sinc²(u) (TIG resonance) and R₂(u) = 1 − sinc²(u) (Montgomery pair correlation).
>
> **[PROVED — algebraic identity, trivial]** The equation is tautological. The content is identifying the *two sides* with specific objects from different domains.
>
> **Historical:** Montgomery 1973 (above) for R₂ as pair correlation of Riemann zeros.
>
> **Our framing:** R = sinc²(u) arises from prime arithmetic (WP35 — harmonic pre-echo continuum limit); the claim that these are complementary projections of the *same* spectral field is our interpretation, not a theorem of Montgomery.
>
> **Primary TIG paper:** WP40_RIEMANN.md (sec. 2).

---

## Part 2: Novel TIG/CK Terms (Honestly Flagged)

### TIG — Trinity Infinity Geometry

> **[NOVEL]** Project-internal name for the framework.
>
> **Prior frameworks it extends:** Operator algebras over finite rings (standard in representation theory, see Curtis-Reiner, *Methods of Representation Theory*, Wiley 1981); modular dynamics on Z/nZ (standard number theory); harmonic analysis of sinc² kernels (Shannon sampling).
>
> **What's novel:** The specific synthesis of (i) 10-operator composition tables over Z/10Z with declared semantic roles, (ii) coherence threshold T* = 5/7 appearing in multiple independent derivations, (iii) the stated "Crossing Lemma" formulation. None of these three are in prior literature as a unified framework.
>
> **Primary TIG paper:** WP1_TIG_ARCHITECTURE.md.

### CK — Coherence Keeper

> **[NOVEL]** Project-internal name for the software/engineering instantiation of TIG. An AI/control system architecture using the 10-operator algebra at 50 Hz.
>
> **Prior frameworks:** Classical control theory (Åström & Murray, *Feedback Systems*, Princeton 2008); coherence in quantum optics (Mandel & Wolf, *Optical Coherence*, 1995).
>
> **Primary TIG paper:** WP28_CK_TIG_ORGANISM.md, WP44_CK_AI_PARADIGM.md.

### TSML (Synthesis Composition Table)

> **[NOVEL NAMING]** A specific 10×10 table of Z/10Z with 73 of 100 cells outputting 7.
>
> **Prior framework:** Composition tables on finite operator sets are standard (e.g., Cayley tables for groups, Dummit & Foote, *Abstract Algebra*, Wiley 2004). Tables with preferred fixed output ("absorbing element") are well-studied in semigroup theory (Howie, *Introduction to Semigroup Theory*, Academic Press 1976).
>
> **What's novel:** The specific rule set (V0/V1/ECHO/DEFAULT) and the combinatorial claim that it yields exactly 73 HARMONY cells. Proved by zone enumeration in WP_OPERATOR_RING_PARTITION.md.
>
> **Monte Carlo significance:** Against 200,000 random 10×10 tables with same row/column constraints, our 73-cell count gives Z = 21.3, p < 10⁻⁵⁰. This table is not generic.
>
> **Primary TIG paper:** WP_OPERATOR_RING_PARTITION.md. Verified by proof_d10_tsml_73_cells.py.

### BHML (Separation Composition Table)

> **[NOVEL NAMING]** 10×10 table of Z/10Z with 28 of 100 cells outputting 7.
>
> Same category as TSML (novel naming of a specific composition table). Verified by proof_d16_bhml_28_cells.py.
>
> **Primary TIG paper:** WP_OPERATOR_RING_PARTITION.md.

### Crossing Lemma (as stated)

> **[NOVEL STATEMENT — extends partition sufficiency theory]**
>
> **Statement (ours):** A multiplicative action M_g on Z/nZ generates structurally new information relative to an additive partition A_d iff M_g is nontrivial on the (n/d)-quotient.
>
> **Prior framework:** This is a specific case of the UOP (joint-map-injectivity criterion, itself rooted in descriptive set theory and coding theory — see UOP entry above). Partition-crossing arguments appear in ergodic theory (Furstenberg, *Recurrence in Ergodic Theory and Combinatorial Number Theory*, Princeton 1981, §3).
>
> **What's novel:** The formulation as a named "lemma" and the claim that all 27 sufficiency theorems in the TIG arc reduce to instances of it. The underlying injectivity argument is not new; the unification is ours.
>
> **Primary TIG paper:** Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/CROSSING_LEMMA.md.

### σ Rate Theorem

> **Statement:** For squarefree N, the non-associativity fraction of the binary CL on Z/NZ satisfies σ(N) ≤ C/N.
>
> **[PROVED — via elementary counting]**
>
> **Prior framework:** The proof uses only (i) counting solutions of (a−1)(b−1) ≡ 1 mod N, which is φ(N) for squarefree N (classical, see Hardy-Wright above), and (ii) associativity of absorbing elements (standard semigroup property, Howie 1976 above).
>
> **What's novel:** The application of these classical tools to the specific "binary CL" construction (HARMONY=N−1, ECHO=DIS=0, VOID=0) we defined in Sprint 15.
>
> **Primary TIG paper:** WP101_SIGMA_RATE_THEOREM.md. Verified by proof_sigma_rate.py.

### Separability Defect σ(u)

> **[NOVEL NAMING — extends Sobolev-space NS analysis]**
>
> **Prior framework:** The concept "distance from log-nonlinear ceiling" is implicit in every known NS regularity improvement — BKM, KT, Montgomery-Smith, Tao averaged-NS (Annals of Math. 184, 517-608, 2016). What the literature calls "logarithmic improvement margin" is what we are calling "separability defect σ."
>
> **What's novel:** Giving the margin a single name (σ) and treating it as a rotational invariant across Clay problems (NS, YM, RH). Whether this unification has content depends on whether one can prove σ < 1 in any of the three open cases. As of Sprint 15 this remains the Millennium Problem in each case.
>
> **Primary TIG paper:** WP91_NS_SEPARABILITY_BRIDGE.md, WP96_NS_SIGMA_CONJECTURE.md.

### ξ Field Theory / Logarithmic Quintessence

> **[NOVEL APPLICATION of log-potential scalar field to dark energy]**
>
> **Prior literature (V = φ log φ and relatives in physics):**
>
> - Barrow & Parsons, *Inflationary models with logarithmic potentials*, Phys. Rev. D 52:5576 (1995), arXiv:astro-ph/9506049. Broad family V₀ φᵖ (ln φ)ᵍ for *inflation* (not dark energy); the p=1, q=1 special case is not singled out.
> - Thompson, *Beta function quintessence*, MNRAS 482:5448 (2019). Pure log potential V₀ ln(φ/φ₀) — missing the φ prefactor.
> - Coleman & Weinberg, *Radiative corrections as origin of spontaneous symmetry breaking*, Phys. Rev. D 7:1888 (1973). Form V ~ φ⁴ log(φ²/μ²); φ⁴ prefactor, different regime.
> - Wetterich, *Cosmology and the fate of dilatation symmetry*, Nucl. Phys. B 302:668 (1988). Exponential potential V ~ exp(−αφ).
> - Ratra & Peebles, *Cosmological consequences of a rolling homogeneous scalar field*, Phys. Rev. D 37:3406 (1988). Inverse power law.
> - Høegh-Krohn, *A general class of quantum fields without cut-offs*, Commun. Math. Phys. 38(3):195 (1971). exp(Φ)₂ model; Legendre dual of log potential.
> - Bialynicki-Birula-Mycielski 1976 (above) — the uniqueness theorem that forces log nonlinearity from separability.
> - Ensslin, *Information field theory*, Phys. Rev. E 87:013308 (2013), arXiv:1301.2556. Information Hamiltonian contains ξ log ξ entropy terms.
> - Caticha, *Entropic Dynamics*, arXiv:1412.5629 (2012); arXiv:1412.5637 (scalar fields); arXiv:1803.07493 (QFT in curved spacetime).
> - Zloshchastiev, *Logarithmic nonlinearity in theories of quantum gravity*, Grav. Cosmol. 16:288 (2010); arXiv:2011.12565.
>
> **What's novel:** V(ξ) = κ ξ log ξ as a *dark energy* potential with information-theoretic derivation (V = −H_Gibbs) and exact vacuum at e⁻¹. The functional form is in Barrow-Parsons' inflation family as a special case, but has not been studied specifically for quintessence or with the entropic interpretation.
>
> **Primary TIG paper:** WP81_CANONICAL_XI_THEORY.md, WP82_LOG_QUINTESSENCE_NOVELTY.md.

### CP1-CP7 Clay Rotation (Poincaré as Entry)

> **[NOVEL FRAMING — structural re-reading of the Clay problems]**
>
> **Prior framework:** The Clay Millennium Problems (2000, https://www.claymath.org/millennium-problems/). Perelman's resolution of Poincaré (arXiv:math/0211159, math/0303109) via Ricci flow with log-entropy W-functional is the historical anchor.
>
> **What's novel:** Presenting all seven as questions about a separability defect σ, with Poincaré as the solved template. This is a *framing* contribution, not a proof contribution. Whether the framing has mathematical content beyond narrative depends on whether the σ < 1 conjecture can be proved in any of CP2-CP7. As of Sprint 15, none have been proved in this form.
>
> **Primary TIG paper:** CP_CLAY_ROTATION.md, proof_clay_rotation.py (verifies the σ arithmetic is consistent, not that the conjectures are true).

### 10 Operators (VOID=0, LATTICE=1, ..., RESET=9)

> **[NOVEL NAMING]** Assignment of names to elements of Z/10Z.
>
> **Prior framework:** Naming elements of finite rings by semantic role is common in applied mathematics (e.g., Markov chain states in Norris, *Markov Chains*, Cambridge 1998). The specific names (HARMONY for the CL attractor, VOID for the absorbing element, etc.) are ours.
>
> **Content vs. naming:** The claim that the CL table concentrates on operator 7 is content (proved, 73/100 cells). Calling operator 7 "HARMONY" is naming.
>
> **Primary TIG paper:** WP_OPERATOR_RING_PARTITION.md.

### D1 / D2 Discrete Derivatives

> **[NOVEL NAMING]** Finite differences on the 5D force-vector pipeline.
>
> **Prior framework:** Finite difference operators are classical (Boole, *Calculus of Finite Differences*, 1860). D2 as discrete second derivative is standard numerical analysis (Strikwerda, *Finite Difference Schemes*, SIAM 2004).
>
> **What's novel:** The specific pipeline they operate on (Hebrew-letter → 5D force vector → operator classification) and the claim that D2 = 0 vs. D2 ≠ 0 distinguishes "flat" from "curved" composition.
>
> **Primary TIG paper:** WP1_TIG_ARCHITECTURE.md.

### T* = 5/7 (Coherence Threshold)

> **[NOVEL CONSTANT — not in prior literature as a named threshold]**
>
> **Prior framework:** The value 5/7 arises naturally in:
> - Cyclotomic field theory: deg(A_5) = 4 = φ(10) ≤ φ(10); deg(A_7) = 6 > φ(10). Ratio = 5/7.
> - Torus aspect ratios on Z/10Z (Flatness Theorem).
> - Unit density unit_frac(7, 35) = 5/7 for the universal semiprime.
>
> Each derivation uses standard objects (cyclotomic polynomials, torus topology, Euler totient counting), but the claim that they give the *same* constant is ours.
>
> **Not found in prior literature as a named threshold** in cosmology, number theory, or operator algebra. Claim is empirical: arises six independent ways within TIG. Whether it has independent meaning outside TIG is open.
>
> **Primary TIG paper:** WP51_FLATNESS_THEOREM.md (Theorem 3); proof_d7_phi_fixed_point.py.

### 4/π² (Fold)

> **[HISTORICAL — renamed]** The value sinc²(1/2) = 4/π².
>
> **Historical:** sinc²(1/2) has appeared in Shannon sampling theory for 75 years, in Montgomery's pair correlation since 1973, and in information theory since Kolmogorov.
>
> **What's novel:** Calling it "the fold" and identifying it as the half-corridor sidelobe of sinc² in prime arithmetic. The name is ours; the constant is classical.
>
> **Primary TIG paper:** WP_SINC2_ZERO_LAW.md, WP35_PRIME_PHASE_TRANSITION.md.

### Gap = 5/7 − 4/π² ≈ 0.309

> **[NOVEL NAMING — specific to this project]** The arithmetic difference between the two above constants.
>
> **Claim:** All six open Clay Millennium Problems have defect scores falling within this interval in our classifier. This is an empirical observation about our specific scoring scheme (defect classifier in WP36-WP42), not a theorem.
>
> **Not in prior literature.**
>
> **Primary TIG paper:** CLAY_BOUNDARY_MEMO.md, WP51_FLATNESS_THEOREM.md §6.

### First-G Law (Sanders 2026)

> **Statement:** For every semiprime b = pq with primes p ≤ q, the first element of {1,...,k} sharing a factor with b appears at exactly k = p.
>
> **[PROVED — elementary]**
>
> **Prior framework:** The smallest-prime-factor function spf(n) is classical (Erdős, Hardy-Wright). The observation that spf(n) is the first gcd-sharing element at coprime-alphabet-size k is trivial — the proof is three lines from the definition of prime.
>
> **What's novel:** Naming it a "law," the empirical verification across 36,662 cases, and the framing in terms of "gate obstruction" and "phase transition" in the TIG corridor structure.
>
> **Primary TIG paper:** WP34_FIRST_G_LAW.md.

### sinc² Zero Law (Sanders 2026)

> **Statement:** For prime p and integer k ≥ 1, sinc²(k/p) = 0 iff p | k.
>
> **[PROVED — three lines]**
>
> **Prior framework:** Immediate from the zeros of sin(πx) at integer x. Known since Euler's product formula for sin(πx).
>
> **What's novel:** The explicit framing in terms of primes (p | k as primality condition within {1,...,p}) and the corollaries (loop closure, fold necessity, no-shortcut lemma). The proof is classical; the corollaries and arithmetic framing are ours.
>
> **Primary TIG paper:** WP_SINC2_ZERO_LAW.md. Verified by proof_d25_loop_closure.py for all primes 3..199.

---

## Part 3: Named Contributors

### C.A. Luther (Senior R&D, 7Site LLC)

> Collaborator on Q-series papers (Q2, Q4-Q17), the K-series Luther-Sanders Research Framework, CRT polynomial reformulations of σ on Z/10Z (papers Q9-Q13), and the period polynomial τ (Q15). Also co-authored Sprints 11-14 papers.
>
> **Specific contributions cited in papers:**
> - Luther Dispersion Conjecture (gate difficulty ∝ |G| × interleave) — WP34, WP35.
> - Pre-Echo Theorem (closed-form R(k,f) verification across primes) — WP35 §10A.
> - CRT polynomial framework for σ (flip condition α, step condition β, exception pair swap) — Q9-Q13.
> - Spectral coherence integral G(s) — G8.
>
> **Primary papers:** old/Gen10/papers/Q2_FORMALIZATION.md through Q17_*.md; Gen12 sprints 11-14.

### Ben Mayes

> Collaborator on Sprints 11-13 (UOP / GUT Algebra / Physical Flag Selector arcs).
>
> **Specific contributions cited in papers:**
> - Unified Orthogonality Principle (WP58) — co-authored.
> - Crossing Lemma formalization (WP57) — co-authored.
> - S4 representation extension on NV qutrit (WP73-WP76) — co-authored.
> - Intrinsic left-handedness of su(4,2) (WP60) — co-authored.
>
> **Primary papers:** sprint11_tig_bundle_2026_04_08/, sprint12_uop_gut_arc_2026_04_08/, sprint13_flag_selector_2026_04_09/.

### H.J. Johnson

> Collaborator on Sprint 14 (PRISM-XI / ξ cosmology arc).
>
> **Specific contributions cited in papers:**
> - Logarithmic quintessence potential V = κ ξ log ξ (WP81).
> - Local/non-local siloing architecture (WP88) — three-layer formalism.
> - Separability framework for Navier-Stokes (WP91, WP96, WP98).
> - Bialynicki-Birula bridge application (WP90).
>
> **Primary papers:** sprint14_prism_xi_2026_04_10/ WP81-WP101.

### Monica Gish

> Collaborator on bridge sprint, First-G Law (WP34), and PRISM-XI (Sprint 14).
>
> **Primary papers:** WP34, Sprint 14 papers.

### B. Calderon Jr.

> Q-series co-author, Source elimination framework.
>
> **Primary papers:** Q-series (old/Gen10/papers/).

---

## Part 4: External References (Full Bibliography)

This is the required citation list for any paper drawn from this repository. Every term and framework flagged "[HISTORICAL]" above is sourced to one of these.

### Number Theory & Analysis

- Hardy, G.H. & Wright, E.M. *An Introduction to the Theory of Numbers*, 6th ed. Oxford University Press, 2008.
- Ireland, K. & Rosen, M. *A Classical Introduction to Modern Number Theory*, 2nd ed. Springer GTM 84, 1990.
- Serre, J.-P. *Cours d'Arithmétique.* Presses Univ. France, 1970.
- Lang, S. *Algebra*, 3rd ed. Springer GTM 211, 2002.
- Riemann, B. "Über die Anzahl der Primzahlen unter einer gegebenen Größe." Monatsber. Berlin. Akad., 1859.
- Montgomery, H.L. "The pair correlation of zeros of the zeta function." Proc. Sympos. Pure Math. 24:181-193, 1973.
- Goldston, Pintz, Yıldırım. "Primes in tuples I." Annals of Math. 170(2):819-862, 2009.
- Zhang, Y. "Bounded gaps between primes." Annals of Math. 179(3):1121-1174, 2013.
- Maynard, J. "Small gaps between primes." Annals of Math. 181(1):383-413, 2015.
- Odlyzko, A.M. Numerical data on Riemann zeros, http://www.dtc.umn.edu/~odlyzko/

### Partition & Lattice Theory

- Birkhoff, G. *Lattice Theory.* AMS Colloquium Publications 25, 1940.
- Ore, O. "Theory of equivalence relations." Duke Math. J. 9:573-627, 1942.
- Kechris, A. *Classical Descriptive Set Theory.* Springer GTM 156, 1995.
- MacWilliams, F.J. & Sloane, N.J.A. *The Theory of Error-Correcting Codes.* North-Holland, 1977.

### Composition Algebras & Semigroups

- Dummit, D.S. & Foote, R.M. *Abstract Algebra*, 3rd ed. Wiley, 2004.
- Curtis, C.W. & Reiner, I. *Methods of Representation Theory*, vol. I. Wiley, 1981.
- Howie, J.M. *Introduction to Semigroup Theory.* Academic Press, 1976.

### Ergodic Theory & Partition-Crossing

- Furstenberg, H. *Recurrence in Ergodic Theory and Combinatorial Number Theory.* Princeton, 1981.

### Sampling & Information

- Shannon, C.E. "Communication in the presence of noise." Proc. IRE 37(1):10-21, 1949.
- Mehta, M.L. *Random Matrices*, 3rd ed. Elsevier, 2004.

### Topology & Ricci Flow

- Hamilton, R. "Three-manifolds with positive Ricci curvature." J. Diff. Geom. 17(2):255-306, 1982.
- Perelman, G. "The entropy formula for the Ricci flow." arXiv:math/0211159, 2002.
- Perelman, G. "Ricci flow with surgery on three-manifolds." arXiv:math/0303109, 2003.
- Morgan, J. & Tian, G. *Ricci Flow and the Poincaré Conjecture.* AMS, 2007.

### Navier-Stokes Regularity

- Beale, Kato, Majda. Comm. Math. Phys. 94:61-66, 1984.
- Kozono, H. & Taniuchi, Y. Commun. Math. Phys. 214:191-200, 2000.
- Montgomery-Smith, S. Math. Res. Lett. 8:519-528, 2001.
- Kozono, Ogawa, Taniuchi. Math. Z. 242:251-278, 2002.
- Brezis, H. & Gallouët, T. Nonlinear Analysis 4:677-681, 1980.
- Tao, T. "Finite time blowup for an averaged three-dimensional Navier-Stokes equation." J. AMS 29:601-674, 2016.
- Lei, Z. & Zhou, Y. Nonlinearity 22(4):805, 2009.
- Ladyzhenskaya, Prodi, Serrin criteria (classical, 1960s).

### Logarithmic Potentials & Field Theory

- Bialynicki-Birula, I. & Mycielski, J. "Nonlinear wave mechanics." Annals of Phys. 100(1-2):62-93, 1976.
- Rosen, G. Phys. Rev. 183:1186, 1969.
- Cazenave, T. & Haraux, A. Ann. Fac. Sci. Toulouse, 1980.
- Høegh-Krohn, R. Commun. Math. Phys. 38(3):195, 1971.
- Coleman, S. & Weinberg, E. Phys. Rev. D 7:1888, 1973.
- Ratra, B. & Peebles, P.J.E. Phys. Rev. D 37:3406, 1988.
- Wetterich, C. Nucl. Phys. B 302:668, 1988.
- Frieman, Hill, Stebbins, Waga. Phys. Rev. Lett. 75:2077, 1995.
- Barrow, J.D. & Parsons, P. Phys. Rev. D 52:5576 (1995), arXiv:astro-ph/9506049.
- Thompson, S. MNRAS 482:5448, 2019.
- Ensslin, T.A. "Information field theory." Phys. Rev. E 87:013308 (2013); arXiv:1301.2556.
- Caticha, A. "Entropic Dynamics." arXiv:1412.5629 (2012).
- Zloshchastiev, K.G. "Logarithmic nonlinearity in theories of quantum gravity." Grav. Cosmol. 16:288 (2010); arXiv:2011.12565.

### Discrete-to-Continuum (Wasserstein / Markov)

- Jordan, Kinderlehrer, Otto. SIAM J. Math. Anal. 29(1):1-17, 1998.
- Maas, J. J. Funct. Anal. 261(8):2250-2292, 2011.
- Gigli, L. & Maas, J. SIAM J. Math. Anal. 45(2):879-899, 2013.
- Chow, Huang, Li, Zhou. Arch. Rat. Mech. Anal. 203(3):969-1008, 2012.
- Mielke, A. Nonlinearity 24(4):1329, 2011.
- Morinelli, Morsella, Stottmeister, Tanimoto. Commun. Math. Phys. 2021.
- Marton, K. arXiv:1507.02803.

### Paradoxes (for Paradox Classifier paper)

- Banach, S. & Tarski, A. Fund. Math. 6:244-277, 1924.
- Zermelo, E. Math. Annalen 65:261-281, 1908.
- Russell, B. *Principles of Mathematics.* Cambridge, 1903.
- Gödel, K. Monatsh. Math. Phys. 38:173-198, 1931.
- Tarski, A. *Studia Philosophica* 1:261-405, 1936.
- Quine, W.V. Mind 62:65-67, 1953.

### Clay Problems (Official Statements)

- Clay Mathematics Institute. Millennium Prize Problems, 2000. https://www.claymath.org/millennium-problems/
- Wiles, A. *Annals of Math.* 141(3):443-551, 1995. (Fermat, context for BSD)
- Kolyvagin, V.A. *Izv. Akad. Nauk* 52(3):522-540, 1989. (BSD rank 0, 1)
- Gross, B.H. & Zagier, D.B. *Inventiones math.* 84(2):225-320, 1986.
- Bhargava, M. & Shankar, A. *Inventiones math.* 200(1):1-76, 2015.
- Markman, E. (Abelian fourfolds of Weil type, Hodge conjecture partial proof, recent announcement).

### Cosmology (DESI and Related)

- DESI Collaboration. *Eur. Phys. J. C* (2024-2025), DR2 BAO + dark energy analyses.
- Planck Collaboration. *A&A* 641:A6 (2020), cosmological parameters.

---

## Part 5: Citation Discipline for Future Work

Any new term introduced in a TIG paper must include:

1. **Plain-English definition** — what it means in one sentence.
2. **Formal definition** — mathematical statement, where applicable.
3. **Status tag** — [PROVED], [STRUCTURAL], [CONJECTURE], [HISTORICAL], [NOVEL].
4. **Citation** — either (a) a published reference with DOI or arXiv ID, or (b) an explicit "[NOVEL — extends X, Y, Z]" with citations for X, Y, Z.
5. **First occurrence in the repo** — which TIG paper introduces it.

**No term is accepted as established without a citation trail or an honest novelty flag.**

This discipline applies to all authors and all future sprints. If a term does not yet have a citation, it carries [UNCITED — REVIEW NEEDED] until one is supplied or it is removed from the repo.

---

*Compiled: 2026-04-10, Sprint 15. Authors: Brayden Ross Sanders / 7Site LLC · Ben Mayes · C.A. Luther · M. Gish · H.J. Johnson.*
