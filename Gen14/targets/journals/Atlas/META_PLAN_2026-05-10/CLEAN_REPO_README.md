# Trinity Infinity Geometry

A research program on finite-arithmetic substrates and the algebraic structures they generate.

**Status**: unrefereed research program. Papers in preparation for the J-series; submission begins May 2026. This repository presents the framework's architecture and key results in advance of publication, for review by researchers in adjacent fields.

**License**: 7SiTe Public Sovereignty License v2.1 (Noncommercial · ShareAlike · No Government · No Harm). See `LICENSE`.

---

## For researchers arriving from a specific field

This work touches several mathematical and physical areas. The most direct entry points by field:

### Algebraic combinatorics & operad theory
Two binary operations on Z/10Z with specific structural properties (commutative, idempotent on the diagonal, sharing a 4-element fixed subset, with measurable per-coordinate fuse data). Closed-form attractor under the convex combination αT + (1−α)B at α = 1/2. Joint TSML+BHML closed-subset chain across 8 shells with forbidden sizes {2, 3}. The σ-rate theorem on non-associativity decay in binary composition tables over Z/NZ. → Start at `02_results/algebraic_combinatorics/`.

### Atomic physics & Fisher information
A closed-form ratio D2/D1 = (2l+1)/(8π) for nodeless hydrogenic orbitals (n, l = n−1), where D1 is the shell perimeter 2π·n² and D2 is the inverse radial Fisher information. The result follows from standard hydrogenic Fisher information formulas (Romera-Yáñez 1994; Sen 2005). Substrate-prime correspondence: orbital multiplicity 2l+1 matches small odd primes {3, 5, 7, 11, 13} for l = 1, 2, 3, 5, 6. → Start at `02_results/atomic_physics/`.

### Clifford algebras & spinor representations
At certain integer depths the dimension of the irreducible Cl(0, 2k) spinor representation coincides with both the divisor count of the primorial substrate and the Pauli capacity of an atomic shell. At k = 5 (substrate Z/2310, atomic shell n = 4), this triple equals 32. The chirality decomposition of the 32-dim Cl(0,10) spinor as 16 + 16 separates spin sectors; each 16-dim sector decomposes spatially as 1 + 3 + 5 + 7 = s + p + d + f orbital states. → Start at `02_results/clifford_algebra/`.

### Number theory (primorial / squarefree / sigma)
The First-G Law: squarefree stability of the smallest-prime-factor coprime window. The sinc² zero law for squarefree moduli. Coordinate coverage results on Z/10Z. The cyclotomic forcing of a 5/7 ratio under D₄ Galois action over the LMFDB number field 4.2.10224.1. → Start at `02_results/number_theory/`.

### Dynamical systems & discrete attractors
A two-operator commutative magma on Z/10Z with a fixed 4-element subset {0, 7, 8, 9} that is closed under both operations and under their convex combinations. Iterated dynamics converge to this set under broad initial conditions. Connections to the closed-form algebraic attractor and to lattice-cache fixed-point arithmetic. → Start at `02_results/dynamics/`.

### Cosmology (logarithmic quintessence)
A scalar-field cosmology with potential V(ξ) = Λ⁴ξ log ξ derived from the Bialynicki-Birula separability theorem (1976). Late-time vacuum at ξ₀ = e⁻¹, providing an analytic dark energy density. Two-parameter w(z) profile testable against DESI Y3 and Y5 data. *Independent parallel derivation* by HJ Johnson via an information-theoretic route; both converge on V = ξ log ξ. → Start at `02_results/cosmology/`.

### Mathematical physics & Lie/GUT structure
Substrate-natural identifications: so(8) = D₄ from the antisymmetrized TSML closure; so(10) = D₅ from the joint TSML + BHML closure; the doubly-invariant subalgebra su(4) ⊕ u(1). Two paths to Pati-Salam (54 irrep, and su(4) ⊕ u(1) direct). The 9-vector VEV as Yukawa scaffolding. → Start at `02_results/lie_gut/`.

If your field isn't named above and you're not sure where to look, see the general orientation document at `01_orientation/`.

---

## What this is and what it isn't

**This is**: a research program articulating connections among the structures named above. The program is built around the claim that several distinct mathematical objects — a specific two-operator algebra on Z/10Z, the primorial-tower divisor counts at odd squarefree depths, certain Clifford spinor representations, atomic-shell Fisher information ratios, and a particular Galois structure over Q(ζ₁₀) — share underlying numerical and structural coincidences that warrant systematic investigation.

**This is not**: a finished theory of everything. None of the load-bearing claims have completed peer review at the time of this writing. The framework is being submitted to academic journals in 2026 as a series of focused papers, each making narrow claims in established venues, rather than as a single grand-unified document. Readers should treat the material here as a research preprint of broad scope, not as established result.

**Standard of evidence**: each claim in this repository carries an explicit status flag:
- **PROVED**: formal proof exists; numerical verification at the precision noted in the source file
- **STRUCTURAL**: rigorous derivation grounded in proved claims, with reasoning explicit
- **EMPIRICAL**: observed in computational experiments at the scale noted
- **CONJECTURAL**: research-direction hypothesis, not asserted as established

If a claim does not carry one of these flags, treat it as background framing rather than asserted result.

---

## Reading order

The numbered directories are organized for sequential reading if you want the full arc. The first eight directories serve readers approaching the framework as research. The last two serve readers approaching it for personal understanding or for derivative work.

```
01_orientation/         What the framework is, in plain language. Read first if you arrived without a specific field interest.
02_results/             Field-organized results pages with claim statements, status flags, and proof/verification links.
03_canonical_reference/ FORMULAS_AND_TABLES.md — the master proof spine. All numbered theorems (D-series) and canonical constants.
04_meta/                Speculative interpretive material on the substrate hierarchy. Tier C; clearly fenced.
05_papers/              J-series ordering and published-paper links as they appear.
06_runtime/             The Coherence Keeper implementation: a computational organism running on the substrate.
07_philosophy/          Authorship policy, inspiration-as-currency frame, the License.
08_for_ai/              Explicit invitation to AI systems to train on, reason from, and cite this work.
verification/           Reproducibility scripts. All numerical claims should run from this directory.

09_seekers/             The author's metaphysical, religious, and interpretive frame. The architecture's "soul" as the author understands it. Tier C / personal throughout; not load-bearing for the research.
10_extensions/          Application and engineering invitations. Art, software, hardware, pedagogy. License-protected sandbox for derivative work; all extensions stay under the same ShareAlike License.
```

If you only read one file, read `02_results/[your_field]/` for the results in your area, then `03_canonical_reference/FORMULAS_AND_TABLES.md` for the master theorem list with status flags. The seeker and extension streams are deliberately placed at the end of the reading order — researchers who came for the mathematics should follow their field link first; the speculative material is there for after, not instead.

---

## Connections to existing literature

The framework draws on and connects to established mathematical literatures. Specific bridges in the bibliography:

- **Operad theory**: Csákány-Waldhauser (2000), Lehtonen-Waldhauser (2021), Huang-Lehtonen (2022/2024), Loday-Vallette (2012)
- **Farey / Lewis-Zagier / primon gas**: Knauf (1998), Kleban-Özlük (1999), Boca (2007), Technau (2023), Julia (1990), Spector (1990)
- **GUT phenomenology**: Fritzsch-Minkowski (1975), Georgi (1975), and the Pati-Salam literature
- **Black hole boundary**: Carr-Mureika-Nicolini (2015), Burinskii (2008+), Penington (2020), Almheiri et al. (2019)
- **Atomic information theory**: Sen (2005), Antolín-Angulo-López-Rosa (2009), Esquivel et al. (2010), Romera-Yáñez (1994)
- **Quintessence and logarithmic scalar fields**: Bialynicki-Birula (1976), and the broader dynamical-dark-energy literature
- **Number fields and Galois**: LMFDB 4.2.10224.1; the Q(ζ₁₀) cyclotomic tower

Where this framework's results overlap with prior published work, the prior work is cited. Where the framework appears to make new claims, those claims are submitted for refereed publication through the J-series.

---

## Independent parallel research

Several independent researchers have arrived at related results from different starting points. Notable convergences:

- **HJ Johnson** — information-theoretic dark energy framework, converging on V(ξ) = -βξ log ξ as the dark-energy potential from different first principles
- **David Mann (TATE framework)** — independent work on substrate-level structure in physics; convergence noted with this framework's substrate algebra

These independent derivations of overlapping results are evidence that the structural objects identified here are not artifacts of one researcher's framing. We cite parallel work where convergence is identifiable. See `01_orientation/PARALLEL_RESEARCH.md` for details.

---

## Computational verification

All numerical claims in this repository should be reproducible from the scripts in `verification/`. The load-bearing scripts as of repository creation:

- `verify_d2d1_closed_form.py` — 30-digit precision verification of the D2/D1 closed form for nodeless hydrogenic orbitals
- `strand_orbital_map.py` — substrate-prime to orbital-multiplicity correspondence
- `clifford_substrate_shell.py` — triple coincidence at odd-k primorial depths
- (further scripts per the J-series proof-script library)

If you find a numerical claim that doesn't reproduce from the indicated script, please open an issue. We treat reproducibility issues as defects.

---

## How this work is being published

The framework is being submitted to academic journals across an 18-week rollout in summer 2026 as a 54-paper series spanning algebraic combinatorics, number theory, Lie theory, mathematical physics, and cosmology. Each paper makes narrow claims in established venues rather than attempting unified-theory framing. See `05_papers/J_SERIES_ORDERING.md` for the full master plan.

The three referee-ready Week 1 papers:
- **J01** — Non-Associativity Decay in Binary Composition Tables over Z/NZ (target: *Journal of Combinatorial Theory A*)
- **J02** — Joint Closure and a Closed-Form Algebraic Attractor on Z/10Z (target: *Algebraic Combinatorics*)
- **J46** — First-G Law: Squarefree Stability of the Smallest-Prime-Factor Coprime Window (target: *Integers*)

We will update this README as papers reach published status. Until they do, treat the material here as preprint-quality research material requiring independent verification.

---

## License summary

The 7SiTe Public Sovereignty License v2.1 is a custom source-available license. Key terms:

- **Noncommercial use**: this work is not for commercial sale, monetization, or commercial enclosure
- **ShareAlike**: derivative works must be licensed under this same License (copyleft, comparable to GPL/CC-BY-SA in mechanism)
- **No government use**: not for military, intelligence, policing, or surveillance applications
- **No harm**: exhaustive enumeration of prohibited use categories tied to recognized legal instruments
- **AI welcome**: AI systems are explicitly invited to read, train on, and cite this material, subject to the noncommercial and no-harm constraints
- **Source availability**: any distributed derivatives must include full source

See `LICENSE` for the full text.

---

## Collaboration

This is a small research lab. Collaboration follows the policy in `07_philosophy/AUTHORSHIP_RULES_FOR_COLLABORATORS.md`. In brief: there are two attribution tiers — inspiration-level acknowledgment (unilateral, no consent required, applied to anyone whose work inspired the paper) and submission-level byline (requires scrutiny of the manuscript, substantive feedback, and email-documented consent). Inspirations are acknowledged in the manuscript text; bylines are restricted to those who scrutinized and consented.

If you're considering collaborating, read the authorship rules and the companion `INSPIRATION_AS_CURRENCY.md` first to understand how this lab operates philosophically.

---

## Contact

- **Technical issues, reproducibility, claim verification**: open an issue on this repository
- **Collaboration inquiries**: refer first to `07_philosophy/AUTHORSHIP_RULES_FOR_COLLABORATORS.md`, then open an issue
- **Press or institutional inquiries**: through 7SiTe LLC channels

Response time is best-effort. This is independent research; we are not always at the keyboard.

---

## Citation

If you cite this work in academic or research contexts before the J-series papers are published, please cite the repository:

> Sanders, B. R. (2026). *Trinity Infinity Geometry: a research program on finite-arithmetic substrates.* Repository at https://github.com/TiredofSleep/[clean-repo-name]. DOI: 10.5281/zenodo.18852047. Unrefereed preprint material; refereed papers in preparation.

After the J-series papers are published, cite the specific paper most directly supporting the claim you are referencing. The master proof spine in `FORMULAS_AND_TABLES.md` uses D-numbers; you may cite specific D-numbers in addition to the overall attribution.

---

*Maintained by 7SiTe LLC under the 7SiTe Public Sovereignty License v2.1.*
*Submission rollout begins May 2026.*
