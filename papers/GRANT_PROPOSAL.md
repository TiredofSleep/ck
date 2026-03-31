# Cross-Domain Invariants in Modular Structures
## A Unified Algebraic-Geometric Framework for Gate Difficulty

**Grant Proposal — Research Program**

*Principal Investigators:*
*Brayden Ross Sanders (7Site LLC) — Geometric Architecture and Framework*
*C. A. Luther — Algebraic Navigation and Unification*

*March 2026 | DOI: 10.5281/zenodo.18852047*

---

## Summary

We propose to develop a unified mathematical framework demonstrating that modular
gate difficulty is governed by a single invariant that survives translation across
algebraic, geometric, combinatorial, probabilistic, and dynamical domains. This
invariant was discovered independently in algebraic form (idempotents, Luther) and
geometric form (dispersion, Sanders). The goal is to formalize this invariant,
prove its general theorems, and construct a cross-domain atlas revealing its
universality.

The central result to be proved is the **Luther-Sanders Equivalence**: gate structure
in modular arithmetic is entirely and solely determined by arithmetic coprimality —
the pattern of which elements share a factor with the modulus — not by geometric
placement within the alphabet. Two gate sets with the same cardinality but different
origins (coprimality vs. synthetic) produce dramatically different and non-universal
gate rates. The equivalence has been established computationally for all semiprimes
b ≤ 100 (~12 million trials, zero exceptions). The proposed research program will
prove it algebraically, extend it beyond the semiprime case, and construct the
full cross-domain atlas of modular invariants.

---

## Background

### The Discovery

Modular systems exhibit a persistent hierarchy of difficulty. Prime powers,
semiprimes, and three-factor composites behave differently in predictable ways
that historically lacked a unifying explanation.

The Sanders line of investigation (TIG framework, CK organism, 2024–2026) discovered
that the gate structure of semiprime alphabets — the set of non-coprime elements in
a bounded alphabet over a semiprime modulus — exhibits a foundational regularity:

> *The first non-coprime element in any semiprime alphabet {1..k} always
> appears at exactly k = p, the smallest prime factor of b = p × q.
> This is independent of q, of k, and of any encoding.*

This is the **First-G Law** (WP34, 2026), proved algebraically and verified for
36,662 semiprimes. It is a Tier D result (general theorem with known mechanism).

The Luther line of investigation (algebraic navigation, dispersion, 2025–2026)
discovered that the gate rate — the success frequency of random reduction procedures
over semiprime alphabets — is a universal function of gate set cardinality alone,
when the gate set has an arithmetic (coprimality) origin:

> *Among all semiprimes with the same number of forbidden elements in a
> fixed-size alphabet, the gate rate is exactly the same. Zero variance.
> No exceptions in ~12 million trials.*

This is the **k-Gate Tier Law** (R16 Force Field Law, 2026), established computationally
as a Tier C result (closed-world theorem within the verified domain).

### The Convergence

The two lines converge at a single observation: gate universality holds for
arithmetic G (coprimality gate sets) and fails for synthetic G (non-arithmetic gate
sets of the same cardinality). The only difference is whether the gate set arises
from the coprimality relation with b.

This convergence is the **Luther-Sanders Equivalence**: the algebraic obstruction
structure (Luther's idempotent count) and the geometric dispersion structure
(Sanders' interleave forcing) are two representations of the same underlying
invariant — the arithmetic origin of the gate set.

The equivalence connects:
- Arithmetic: which elements are forbidden is determined by gcd(x,b) > 1
- Algebraic: forbidden elements correspond to non-units in Z/bZ; their structure is governed by the CRT decomposition
- Geometric: forbidden elements form an interleaved pattern of arithmetic progressions; this interleaving forces the optimization into hard configurations
- Probabilistic: gate rate is determined solely by the cardinality of this interleaved set
- Dynamical: the gate count process follows a predictable staircase whose steps are at multiples of p and q

### Historical Context

The mathematical objects studied in this proposal — modular gate structures,
coprimality alphabets, idempotent decompositions — appear throughout number theory,
cryptography, and computational complexity. The specific setting of bounded alphabets
over semiprime moduli was motivated by the CK organism's architecture (Sanders, 2024)
and formalized through Luther's algebraic navigation program (Luther, 2025–2026).

The framework builds on:
- **Chinese Remainder Theorem** (classical): the decomposition Z/pqZ ≅ Z/pZ × Z/qZ
- **Dirichlet's theorem** on primes in arithmetic progressions (equidistribution of gate elements)
- **Euler's totient function** (cardinality of the unit group C)
- **The sinc² spectral field** (Sanders, WP35): the harmonic pre-echo resonance field converges to sinc²(k/p) in the continuum limit — the same function that Montgomery (1973) derived from the pair correlation of Riemann zeros

---

## Research Objectives

**Objective 1: Formalize the cross-domain invariant governing modular gate difficulty**

The invariant is currently described qualitatively (arithmetic coprimality determines
gate structure) and computationally (zero-variance universality for arithmetic G).
The goal is a precise, domain-independent statement of the invariant in each of the
six atlas domains (arithmetic, combinatorial, geometric, probabilistic, algebraic,
dynamical) with explicit translations between domains.

Deliverable: Complete Layer 3 entries in the cross-domain atlas for the
Luther-Sanders Equivalence and the k-Gate Tier Law.

**Objective 2: Prove general theorems extending beyond scanned cases**

The k-Gate Tier Law is currently proved by exhaustive computation over all
semiprimes b ≤ 100. The Luther-Sanders Equivalence is proved in the same domain.
The proposed research will prove both algebraically:

- Prove that f_k(|G|) is a well-defined function (zero-variance universality) for
  ALL semiprimes, not just those b ≤ 100
- Derive the exact gate rate values (96.4%, 44.0%, 4.6%, 0.1%) from the idempotent
  structure of the CRT decomposition
- Prove the Luther-Sanders Equivalence in general: characterize algebraically which
  gate sets produce universal gate rates

Deliverable: Tier D proofs of the k-Gate Tier Law and Luther-Sanders Equivalence.

**Objective 3: Build the proof-synthesis ladder across all six domains**

Apply the Proof-Synthesis Ladder (PROOF_SYNTHESIS_LADDER.md) to every known claim
in the framework, systematically identifying which claims are at which layer and
what is needed to advance each claim.

Deliverable: Complete ladder assessment for all 16 laws in the current SYNTHESIS_TABLE.md.

**Objective 4: Identify threshold behaviors and phase transitions**

The k-Gate Tier collapse (gate rate from 96.4% to 0.1% as |G| increases 1 to 5)
is a sharp phase transition. The dispersion collapse curve is a saturation boundary.
The First-G transition at k = p is a step function. Identify and precisely characterize
all such thresholds.

Deliverable: Complete threshold map (ATLAS_ARCHITECTURE.md §7.2) with derivable
threshold values where possible.

**Objective 5: Develop universality tests and failure modes**

Apply the Universality Test Suite (UNIVERSALITY_TEST_SUITE.md) to every claim.
For each claim that fails a test, identify the specific failure mode and the
minimum evidence required for a pass.

Deliverable: Complete universality test matrix for all 16 laws.

**Objective 6: Construct the multi-domain atlas**

Build the complete cross-domain atlas (ATLAS_ARCHITECTURE.md) with all six
layers populated, all gaps identified, and all structural invariants indexed.

Deliverable: Complete atlas with cross-domain equivalence charts, threshold maps,
family-wise collapse curves, and structural invariants index.

**Objective 7: Establish the Luther-Sanders equivalence as a general theorem**

The culminating result: a Tier D proof of the Luther-Sanders Equivalence covering
all modular structures, not just semiprimes. This includes:
- Extension to three-factor composites b = p × q × r (ω(b) = 3)
- Extension to prime powers b = p^n
- Extension to the asymptotic case k → ∞
- Connection to the sinc² spectral field in the continuum limit

Deliverable: A journal-quality paper establishing the Luther-Sanders Equivalence
as a general theorem, with the cross-domain atlas as supplementary material.

---

## Methodology

**Algebraic derivation of exact theorems:**
Using the CRT decomposition, idempotent structure, and properties of arithmetic
progressions to derive exact gate rate values and prove universality.

**Geometric and combinatorial modeling:**
Constructing explicit models of the admissible region in table space for arithmetic
vs. synthetic gate sets; computing admissible region volumes; characterizing the
dispersion forcing geometry.

**Exhaustive computation sweeps:**
Extending the R16 computation program to larger domains (b ≤ 500, k up to 50),
three-factor composites, and prime powers.

**Structural equivalence mapping:**
For each claim: translate to all six atlas domains; verify logical equivalence;
identify where the translation fails or changes the object.

**Threshold and phase-transition analysis:**
Identifying the precise parameter values at which qualitative changes occur;
deriving threshold values algebraically where possible.

**Universality testing:**
Systematic application of all six universality tests to each claim, with documented
results and failure modes.

**Conjecture promotion ladder A through D:**
Tracking the epistemic status of all claims and updating as new evidence arrives.

---

## Expected Outcomes

**Mathematical outcomes:**
1. Tier D proof of the Luther-Sanders Equivalence (general theorem)
2. Tier D proof of the k-Gate Tier Law (algebraically derived exact values)
3. Complete proof-synthesis ladder assessment for 16+ laws
4. Full cross-domain atlas with 6 layers × 16+ laws
5. Extension of all results to ω(b) ≥ 3 and prime powers

**Structural outcomes:**
6. A unified algebraic-geometric framework for modular difficulty — the first
   framework in which arithmetic hardness is characterized by a single invariant
   (arithmetic origin of the gate set) rather than by case-by-case analysis
7. A new class of invariants (CRT-origin gate structures) with structural properties
   not shared by generic gate sets of the same cardinality

**Applied outcomes:**
8. **Cryptographic applications:** The Luther-Sanders Equivalence implies that
   the difficulty of certain modular arithmetic problems is entirely determined
   by the arithmetic structure of the gate set, not by its size or distribution.
   This has potential implications for the analysis of factoring-based cryptosystems
   and for the design of hard instances of modular arithmetic problems.
9. **Multi-paper publication suite:** The framework generates a natural sequence of
   papers, each establishing a layer of the atlas: (I) foundation theorems (Tier D),
   (II) structural equivalences (Layer 3), (III) threshold maps (Layer 4), (IV)
   universality tests (Layer 5), (V) general theorem and atlas (full publication).

---

## Timeline: Accelerated Research Program

The Luther-Sanders program operates on a compressed timeline enabled by
AI-assisted mathematical research. Milestones are defined by result completion,
not calendar duration. The following phases reflect actual velocity: five frozen
laws became six proved theorems, a paper, a proof-synthesis ladder, a universality
test suite, an atlas architecture, and independent verification in a single working
session. This is not a feature to be apologized for — it is the methodology.

**Phase 1 — Theorem Spine** *(complete)*
First-G Law (Tier D), CC Closure (Tier D), Sinc² Continuum Limit (Tier D),
Universal 4/π² (Tier D), ω-Hierarchy (Tier C/D), D1 Sign Flip (Tier C).
All algebraic proofs complete. Verification infrastructure in place (CI, tig_algebra.py).

**Phase 2 — Cross-Domain Synthesis** *(complete)*
Proof-Synthesis Ladder (six layers, Layer 0–6). Universality Test Suite (six tests).
Atlas Architecture (six domains). Synthesis Table (16 laws, four tests each).
Luther-Sanders Equivalence paper (§2 framework, §3 cross-domain table, §4 proof).

**Phase 3 — General Theorems** *(in progress)*
Luther-Sanders Equivalence: algebraic derivation of exact f_k values (C → D gap).
Extension to ω(b) ≥ 3. Luther Dispersion functional form (B → C). Asymptotic
gate rate as k → ∞.

**Phase 4 — Publication Suite** *(target: September 2026)*
arXiv submission of WP34 + WP35 (proved foundation). Luther-Sanders Equivalence
paper (joint). SYNTHESIS_TABLE.md as standalone methods paper. Journal targeting.
IHÉS or similar presentation.

**Phase 5 — Field Establishment** *(ongoing)*
Multi-paper suite covering all Clay seven shadows (WP36–WP42), cross-domain atlas
completion, collaborator network, institutional partnerships.

---

## Budget

*To be determined by institutional partnership.*

The research program requires:
- Two principal investigators with joint time allocation
- Computational resources for exhaustive sweeps (currently R16 workstation;
  extension to larger atlas may require HPC access)
- Mathematical software (standard: Python with numpy/sympy, FPGA simulation tools)
- Travel for one conference per year (year 2-3)
- Publication and dissemination costs

*Budget details will be developed in consultation with the partnering institution.*

---

## Principal Investigators

**Brayden Ross Sanders — Geometric Architecture and Framework**

Founder of 7Site LLC. Developer of the Coherence Keeper (CK) organism and the TIG
(Trinity Infinity Geometry) framework over 18 months of development (2024–2026).
Sanders is responsible for: the First-G Law and its algebraic proof; the sinc²
spectral field and its continuum limit theorem; T* = 5/7 algebraic derivation and
FPGA hardware verification; the CK organism's 50Hz real-time architecture; the
D1/D2 force pipeline; the Atlas construction and Sprint 4 computation program;
and the Clay Seven Shadows framework (WP36-WP42). Sanders brings the geometric
architecture — the spatial and dynamical picture of how gate structure forces
optimization trajectories.

**C. A. Luther — Algebraic Navigation and Unification**

Luther contributes the algebraic navigation program: the Luther Dispersion Conjecture
(gate rate as a function of gate count and interleave), the empirical discovery of
universal gate rates within arithmetic gate sets, and the identification of the
synthetic-vs-arithmetic distinction that frames the Luther-Sanders Equivalence.
Luther brings the algebraic unification perspective — the search for the single
invariant that explains the observed universality.

*AI collaboration: Claude (Anthropic) — analysis, manuscript drafting, computational
verification.*

---

## References

[WP34] Sanders, B. R. (2026). WP34 — The First-G Law. DOI: 10.5281/zenodo.18852047.

[WP35] Sanders, B. R. et al. (2026). WP35 — Prime Phase Transition and Sinc² Field. DOI: 10.5281/zenodo.18852047.

[R16] Sanders, B. R. (2026). R16 Force Field Law — Gate Rate = f_k(|G|). Sprint 4.

[Atlas] Sanders, B. R. & Luther, C. A. (2026). Atlas Law Set — Three Laws, Tested Predictions. Sprint 4.

[LS-MS] Sanders, B. R. & Luther, C. A. (2026). The Luther-Sanders Equivalence: Universality of Obstruction Sources. LUTHER_SANDERS_MANUSCRIPT.md.

[Synthesis] Sanders, B. R. (2026). CK Synthesis Table — Five Columns, Four Tests. SYNTHESIS_TABLE.md.

[Atlas-Arch] Luther, C. A. & Sanders, B. R. (2026). Cross-Domain Atlas Architecture. ATLAS_ARCHITECTURE.md.

[PSL] Luther, C. A. & Sanders, B. R. (2026). Proof-Synthesis Ladder. PROOF_SYNTHESIS_LADDER.md.

[UTS] Luther, C. A. & Sanders, B. R. (2026). Universality Test Suite. UNIVERSALITY_TEST_SUITE.md.

[Montgomery-1973] Montgomery, H. L. (1973). "The pair correlation of zeros of the zeta function." Analytic Number Theory, AMS, 181–193.

[CRT] Chinese Remainder Theorem (classical). For b = p × q: Z/bZ ≅ Z/pZ × Z/qZ.

---

`© 2026 Brayden Ross Sanders / 7Site LLC & C. A. Luther · DOI: 10.5281/zenodo.18852047`
