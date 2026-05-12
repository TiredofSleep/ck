# OPEN_FRONTIERS_AND_NEXT_CALCULATIONS

## Consolidated reference for what's still open across the framework

**Status**: living document. Updated as frontiers close and new ones open.
**Locked**: 2026-05-10 (initial consolidation from session content)
**For**: ClaudeCode reference, Brayden's priority planning, future researchers entering the work

---

## §0. How to read this doc

Every item below is a real open question. Each carries:

- **Priority flag**: 🔴 critical-path (blocks something downstream) / 🟡 high-value (would unlock next layer) / 🟢 exploratory (legitimate research direction, not blocking)
- **Domain tag**: which area of the framework it lives in
- **Falsifiability note**: what would prove it wrong or right
- **Next calculation**: the specific computational or theoretical step needed
- **Dependencies**: what must be done first

Items are NOT priority-ordered within sections. Within each section, items are grouped by domain coherence.

---

## §1. CRITICAL-PATH FRONTIERS (🔴)

These either block published work or are needed for the integrity of the framework's central claims.

### §1.1 J36 freeze-thaw transit JCAP referee inconsistency
**Status**: BLOCKED per J-series meta-plan
**Domain**: cosmology, Sanders-Gish line
**Issue**: referee-flagged numerical inconsistency must be resolved before JCAP submission
**Specifics needed**: identify exact source of inconsistency (likely correlated χ² calculation or Path A vs Path B framing). Determine whether resolution is numerical (recompute) or interpretive (reframe under Path B TIG-internal interpretation).
**Next calculation**: rerun the JCAP referee's specific objection through the Sanders-Gish framework; produce a clean response document.
**Falsifies**: if the inconsistency is real and structural, the paper needs significant revision before resubmission.
**Blocks**: J36 publication; downstream Phase 5 cosmology timing.

### §1.2 J26 distilgpt2 sweep script
**Status**: GATED per J-series meta-plan
**Domain**: TIG detector specificity, WP106
**Issue**: script for distilgpt2 sweep is either lost or unwritten; J26 manuscript depends on it.
**Next calculation**: locate or reconstruct the sweep script (estimated 1-2 hours). Run sweep, generate specificity data, integrate into J26 manuscript.
**Blocks**: J26 publication.

### §1.3 Verification of session scripts against canon
**Status**: REQUIRED before public release
**Domain**: this session's deliverables
**Issue**: the D2/D1 closed form, strand-orbital correspondence, and triple coincidence must verify against published atomic-physics canon (Romera-Yáñez 1994, Sen 2005) before propagation.
**Next calculation**: 
- Run `verify_d2d1_closed_form.py` — confirm 30-digit precision
- Run `strand_orbital_map.py` — confirm Pauli/divisor match at n=2, n=4
- Run `clifford_substrate_shell.py` — confirm triple coincidence at Rungs 1, 3, 5
- Cross-check I_r(n, l) formula = 4/[n²(2n-1)] for max-l hydrogenic against textbook references
- Verify 8π factor is dimensionally consistent in atomic units
**Falsifies**: if any script diverges from claimed precision OR if cross-check against published canon disagrees, the session's structural results need revision before any public release.
**Blocks**: trinity-infinity-geometry repo creation, FORMULAS Volume K addition, any J56 manuscript draft.

### §1.4 Canon citation verification
**Status**: REQUIRED before public release
**Domain**: cross-cutting
**Issue**: this session repeatedly cited D-numbers (D33, D35, D38-D44, D77, D82, D87) and WP-numbers (WP102-WP116) against FORMULAS_AND_TABLES.md. Citations must be confirmed accurate.
**Next calculation**: for each cited D-number and WP-number, locate it in FORMULAS_AND_TABLES.md and confirm the session's usage matches the canonical statement. Document any discrepancies.
**Blocks**: any propagation of session content to the public repo.

---

## §2. HIGH-VALUE OPEN PROBLEMS (🟡)

These would significantly advance the framework if resolved. None block immediate publication but each opens new structural territory.

### §2.1 Explicit Cl(0,10) ↔ n=4 electron-state bijection
**Status**: open
**Domain**: Clifford algebra ↔ atomic physics
**Issue**: at Rung 5, the 32-dim Cl(0,10) spinor representation has the same cardinality as the n=4 atomic shell's 32 electron states. The chirality ω₁₀ decomposition gives 16+16 (spin doubling). Each 16-dim sector decomposes spatially as 1+3+5+7 (s+p+d+f). But the EXPLICIT BIJECTION between Cl(0,10) basis elements and (l, m, s) electron states has not been written down.
**Next calculation**:
1. Choose Cl(0,10) γ-matrix representation in a basis where ω₁₀ is diagonal
2. Construct the chain Cl(0,10) ⊃ Cl(0,8) ⊃ Cl(0,6) ⊃ Cl(0,4) ⊃ Cl(0,2)
3. At each chain level, the chirality decomposition adds an orbital subshell layer
4. Match chain levels to (l = 0, 1, 2, 3) angular momenta
5. Write out the 32-element table mapping (l, m, s) ↔ Cl(0,10) basis element
**Falsifies**: if no clean chain produces (s, p, d, f) labeling in any natural γ-matrix choice, the structural map fails and the triple coincidence becomes "numerical only, not combinatorial."
**Success**: would close the atomic-representation framework. Would also enable multi-electron exchange via Cl(0,10) tensor products and provide a substrate-addressing scheme.

### §2.2 Pauli/divisor direct combinatorial bijection at n=4
**Status**: failed simple attempts (recorded in `priority1_pauli_divisor_attempt.py`)
**Domain**: substrate algebra ↔ Pauli structure
**Issue**: 32 Z/2310 divisors must match 32 n=4 electron states. Simple groupings (Hamming weight, max-prime, prime-as-l-label) all failed to decompose 32 into the required 2+6+10+14 subshell sizes.
**Next calculation**:
1. Try multi-prime encoding schemes — perhaps two primes together encode (l, m) jointly
2. Try σ-orbit structure on divisors — does the σ permutation on Z/10 induce a structure on Z/2310 divisors?
3. Try lattice-quotient encodings — divisors quotiented by some lattice action
4. Try assigning primes to quantum numbers via (n, l, m, s) = (kernel-2, kernel-5, strand-3, strand-7) with prime-11 as additional structure marker
5. If still no bijection, characterize what kind of combinatorial structure would be required
**Falsifies**: if no clean bijection exists in any encoding, the integer match 32=32 is a number-theoretic coincidence (Pascal triangle level) rather than a structural identity.
**Success**: would establish substrate-as-atomic-addressing-scheme. Major implications for the CK runtime architecture.

### §2.3 8π factor in D2/D1 — Gauss-Bonnet?
**Status**: observed, not derived
**Domain**: differential geometry, Fisher information
**Issue**: D2/D1 = (2l+1)/(8π) has 8π in the denominator. 8π appears in Gauss-Bonnet for the total curvature of S². Is this coincidence or is the closed form geometrically a Gauss-Bonnet-type integral?
**Next calculation**:
1. Recast D1 = 2πn² as the perimeter of a sphere of radius n²/2 in Bohr units
2. Recast D2 = 1/I_r as a Fisher-information-derived length scale  
3. Compute the Gauss-Bonnet integral ∮ K dA / (2π) for the hydrogenic probability density on the n-sphere — does it produce 8π?
4. Alternative: check if the 8π emerges from the Bohr-radius-normalized integration measure
5. If neither, derive 8π from the radial probability density's specific form
**Falsifies**: if 8π has no geometric meaning, it's a numerical constant with no deeper significance.
**Success**: would tie the closed form to standard differential geometry and strengthen its publishability in J. Phys. A.

### §2.4 D3 σ-rate analog at the shell-measurement layer
**Status**: partial — tunneling slope analog is -0.365, doesn't match -1 substrate value
**Domain**: shell measurement framework
**Issue**: the three-shape framework needs a clean D3 (σ-rate) analog to match D1 (perimeter) and D2 (Fisher info edge). The current tunneling-fraction slope doesn't reproduce the substrate σ-rate of -1.
**Next calculation**:
1. Identify alternative D3 candidates: WKB tunneling integral derivative, decay-of-correlations rate, autocorrelation slope
2. Test each against hydrogenic data for slope = -1 at appropriate normalization
3. If none work, characterize what physical quantity WOULD satisfy a slope-of-1 condition on atomic shells
**Falsifies**: if no D3 analog exists with slope -1 in atomic systems, the three-shape framework doesn't fully map to atomic measurement.
**Success**: closes the D1/D2/D3 framework at the atomic layer.

### §2.5 General-l closed form for D2/D1 (not just nodeless)
**Status**: closed form only proved for nodeless orbitals (l = n-1)
**Domain**: atomic Fisher information
**Issue**: D2/D1 = (2l+1)/(8π) is verified at 30-digit precision for nodeless orbitals (n, l=n-1). For non-extremal orbitals (l < n-1), the ratio is more complex.
**Next calculation**:
1. Compute D2/D1 for all (n, l) pairs with n ≤ 10, l ∈ {0, 1, ..., n-1}
2. Look for closed-form patterns — does (2l+1)/(8π) hold approximately? With corrections?
3. Try generating function approach: ∑_l D2(n,l)/D1(n,l) might have a clean form even when individual ratios don't
4. Try ratio of integrals rather than ratio of values
**Falsifies**: if no clean general form exists, the structural significance is limited to extremal orbitals (which are still the substrate-resident ones, so this doesn't kill the framework).
**Success**: would generalize the substrate-orbital correspondence to all chemistry, not just nodeless.

### §2.6 Aufbau anomalies as kernel-Z/5 perturbations
**Status**: conjecture (Priority 3 in TRIPLE_COINCIDENCE §6.3)
**Domain**: atomic chemistry, substrate algebra
**Issue**: standard Aufbau is broken in chromium (Cr), copper (Cu), molybdenum (Mo), silver (Ag), and several other d-block / f-block elements. These all involve d-orbital filling. The framework's d-orbital is associated with kernel-Z/5 (not a strand). Are Aufbau anomalies derivable as perturbations from kernel-Z/5's non-strand status?
**Next calculation**:
1. List all known Aufbau anomalies in the periodic table
2. Check whether they correlate specifically with d-orbital filling (and only d, not p or f)
3. If correlation holds, model the perturbation as a coupling between kernel-Z/5 and strand-3 (the p-orbital strand) at half-filled d-shell configurations
4. Predict which superheavy elements (Z > 120) should show Aufbau anomalies based on the model
**Falsifies**: if Aufbau anomalies don't correlate with kernel-Z/5 (d-orbital) specifically, the framework doesn't predict them.
**Success**: would extend the substrate-atomic correspondence to chemistry, not just atomic physics.

### §2.7 Higher-rung physical realization (Rung 7, n=8 atomic)
**Status**: speculative
**Domain**: META extension
**Issue**: the convergence series predicts Rung 7 (substrate Z/510510, Cl(0,14), n=8 atomic shell) with triple coincidence at 128. n=8 shells exist in superheavy elements (Z ≥ 119). Whether superheavy atoms realize the architectural template is testable in principle but currently outside experimental reach.
**Next calculation**: this is largely waiting on superheavy element synthesis and characterization. In the meantime:
1. Compute predicted spectroscopic signatures for n=8 shell structure under the framework
2. Compare against any available theoretical predictions from relativistic quantum chemistry
3. Identify which predicted observable would distinguish the framework from standard relativistic atomic theory
**Falsifies**: lack of detected n=8 architecture in superheavy elements (when measurable).
**Success**: would extend the architectural template beyond atomic to "superheavy chemistry."

### §2.8 The bridge between Braiding Fractal and Bialynicki-Birula
**Status**: structural connection asserted, derivation incomplete
**Domain**: cosmology ↔ substrate algebra
**Issue**: the Sanders-Gish JCAP paper uses V(ξ) = Λ⁴ξ log ξ derived from Bialynicki-Birula 1976 separability. The Braiding Fractal architecture at Rung 5 has Cl(0,10) as Clifford carrier. Are these connected? Specifically: does the BB log-potential emerge naturally from the Cl(0,10) structure at cosmological scales?
**Next calculation**:
1. Derive the effective potential of a Cl(0,10)-valued scalar field
2. Check whether the natural quintessence-like potential under separability gives ξ log ξ
3. If yes, the BB logarithm and the Cl(0,10) substrate are unified
**Falsifies**: if Cl(0,10) doesn't produce ξ log ξ under any natural projection, the cosmology and substrate stories are independent (which is fine, but less unified).
**Success**: would tie the JCAP submission and the Braiding Fractal Rung 5 lock into one structural object.

### §2.9 CK A/B architectural-uniqueness test
**Status**: proposed, not run
**Domain**: CK runtime
**Issue**: the claim that CK's architecture is canonically unique at Rung 5 is testable by deliberately modifying one component and measuring degradation.
**Next calculation**:
1. Fork CK
2. Run four perturbation tests: (α: 1/2 → 1/3), (α: 1/2 → 2/3), (drop 4-core), (single-table TSML-only)
3. Run each modification for 1M ticks with identical inputs to canonical CK
4. Measure coherence stability, attractor convergence, tick performance
5. Compare degradation patterns against the prediction that modifications break stability
**Falsifies**: if modifications preserve stability, the architectural-uniqueness claim is empirically unsupported.
**Success**: empirical confirmation of canonical Rung 5 architecture.

---

## §3. EXPLORATORY FRONTIERS (🟢)

Legitimate research directions worth pursuing as resources allow. Not blocking or load-bearing.

### §3.1 Multi-electron exchange via Cl(0,10) tensor products
**Status**: open
**Domain**: many-body atomic physics
**Issue**: single-electron Cl(0,10) handles n=4 hydrogenic. Multi-electron systems require tensor products of Cl(0,10). What is the natural structure?
**Next calculation**: dependent on §2.1 first.

### §3.2 Braiding Fractal in molecular systems
**Status**: open
**Domain**: chemistry / materials
**Issue**: does the architectural template recur at the molecular level (covalent bonding networks, molecular orbitals)? Specifically, is there a "Rung 6" molecular analog with kernel-dual-quadratic structure?
**Next calculation**: pick a small representative molecule (e.g., H₂, H₂O, CH₄), construct its Cl(0,*) structure, check for convergence patterns.

### §3.3 Microtubule quantum coherence at Q_c = T*
**Status**: predicted by J49
**Domain**: neuroscience / consciousness
**Issue**: prediction that microtubule coherence saturates at T* = 5/7. Testable via biophysics.
**Next calculation**: design experimental protocol; engage biophysics collaborators.

### §3.4 Higher Cl algebras at Rungs 7, 9, 11
**Status**: exploratory
**Domain**: Clifford theory
**Issue**: Cl(0,14), Cl(0,18), Cl(0,22) representation theory at the convergence rungs. What spinor structures appear? Do they map to physical systems?
**Next calculation**: representation-theoretic survey; map known Cl(0,2k) reps for k = 7, 9, 11 against candidate physical systems at corresponding scales.

### §3.5 Substrate-as-cosmic-hierarchy interpretation tests
**Status**: META extension, Tier C
**Domain**: cosmology / philosophy of science
**Issue**: the META framework places successive convergence rungs at cosmological/biological/cellular scales. Identify candidate physical systems at each rung.
**Next calculation**: literature survey across scales for systems with the relevant cardinalities (8, 32, 128, 512, 2048). Rung 7 (128) candidates: molecular orbitals? Specific protein domains?

### §3.6 The σ-rate at higher rungs
**Status**: open
**Domain**: substrate algebra
**Issue**: σ-rate proved on Z/N for binary composition tables. Does the σ-rate generalize to substrates at higher rungs (Z/30, Z/210, Z/2310)?
**Next calculation**: compute σ-rate analog for Z/30 binary tables, check whether closed-form behavior at α=1/2 persists.

### §3.7 Cyclotomic Galois group at higher rungs
**Status**: characterized at Z/10 (LMFDB 4.2.10224.1, Galois D₄)
**Domain**: number theory
**Issue**: what's the Galois structure of Q(ζ_30), Q(ζ_210), Q(ζ_2310) under the framework's lens? Do they encode their own "forced ratios" analogous to T*=5/7?
**Next calculation**: compute Galois groups, identify natural ratios, check for structural correspondences.

### §3.8 Quantum-information interpretation of the substrate
**Status**: gestured at, not developed
**Domain**: quantum information theory
**Issue**: the substrate's two-operator structure might encode a quantum measurement framework. Specifically: is TSML ↔ measurement basis and BHML ↔ transformation operation? Does this give a substrate-native quantum information theory?
**Next calculation**: identify standard quantum information operations (measurement, unitaries, POVMs) and check whether the substrate's operator alphabet captures them.

### §3.9 Pati-Salam Higgs sector at Z/210
**Status**: noted (16 idempotents = dim D₄-invariant of so(10); matches Pati-Salam Higgs sector)
**Domain**: GUT phenomenology
**Issue**: cardinality coincidence at the Z/210 rung suggests Pati-Salam structure lives there. Confirm and extend.
**Next calculation**: compute the actual lattice frame / Higgs vacuum manifold at Z/210; compare to Pati-Salam phenomenology.

### §3.10 Connection to Khovanov homology / braid group representations
**Status**: motivated by the renaming to Braiding Fractal
**Domain**: knot theory / categorification
**Issue**: braid groups B_n have well-developed representation theory. The Braiding Fractal's kernel-strand wrapping should embed naturally in some braid representation.
**Next calculation**: identify the natural braid group action on the substrate; check whether it factors through known representations (Burau, Lawrence-Krammer, Khovanov).

### §3.11 Logarithmic quintessence convergence with HJ Johnson
**Status**: independent convergence noted; not formally analyzed
**Domain**: cosmology
**Issue**: HJ Johnson derives V(ξ) = -βξ log ξ from "Shannon axioms"; Sanders-Gish derives same potential from BB separability. Are these provably the same potential from different first principles?
**Next calculation**: map both derivations onto a common framework; identify the structural reason convergence is forced.

### §3.12 Engineering applications of the Braiding Fractal
**Status**: invitation extended in 10_EXTENSIONS_SOVEREIGN_DOMAIN.md
**Domain**: FPGA / ASIC / neuromorphic / quantum hardware
**Issue**: hardware realizations of the architecture might offer real performance benefits over conventional designs.
**Next calculation**: identify FPGA / ASIC prototypes that could test the architectural template; coordinate with hardware contributors.

### §3.13 The 666 / 144,000 structural identifications
**Status**: speculative, in canon
**Domain**: religious framework
**Issue**: 666 = Being + Becoming without Doing; 144,000 = 12 non-associative triples × 12 × 1000. These are identifications, not derivations. Can they be made rigorous?
**Next calculation**: this lives in the META / SEEKERS stream; Brayden's voice is the right author for this one.

---

## §4. LEGAL AND STRUCTURAL FRONTIERS

### §4.1 Perpetual Purpose Trust formalization
**Status**: framework described in License §15; not yet legally constituted
**Domain**: legal / structural
**Issue**: License v2.1 §15.6 has interim provisions until trust is formed. Trust requires drafting by qualified attorney.
**Next calculation**: identify jurisdiction (Delaware, Utah, Arkansas), draft trust instrument, recruit trustees per §15.3.
**Priority**: 🟡 not blocking; can run on its own timeline. Brayden has stated no lawyer money currently, so this is "when resources allow" territory.

### §4.2 License v2.1 enforcement testing
**Status**: untested in court
**Domain**: legal
**Issue**: License is structured for enforceability via Jacobsen v. Katzer ShareAlike framework. Not yet tested by actual challenge.
**Next calculation**: hope it's not tested; if tested, defend.
**Priority**: 🟢 don't pursue; respond if needed.

### §4.3 Trademark protections
**Status**: no trademarks registered
**Domain**: legal
**Issue**: "Coherence Keeper", "Trinity Infinity Geometry", "Braiding Fractal", "TIG", "CK" are not trademarked. License §3.7 mentions trademarks but no trademarks exist to protect.
**Next calculation**: optional — register trademarks if Brayden decides to. Not blocking.

---

## §5. PUBLICATION FRONTIERS (J-series specific)

These are tracked in the J-series meta-plan (`J_SERIES_ORDERING_v2.md`); listed here for completeness.

### §5.1 Three referee-ready Week 1 papers
- **J01** Non-Associativity Decay (JCT-A) — SUBMISSION-READY, awaiting Brayden's referee-rigor pass
- **J02** Joint Closure + Closed-Form Attractor (Algebraic Combinatorics) — SUBMISSION-READY
- **J46** First-G Law (Integers) — FORMAT (cover letter polish)

### §5.2 ~30 papers awaiting Brayden's referee-rigor pass
Listed in J-series meta-plan. Bottleneck is human review, not drafting.

### §5.3 Three papers needing scope work
- **J36** freeze-thaw (BLOCKED, see §1.1)
- **J26** detector specificity (GATED, see §1.2)
- **J34** discrete sinc² identity (FALLBACK NEEDED — per-venue cap concern)

### §5.4 New paper candidate from this session
- **J56** (or insertion to J51 or J15): D1/D2/D3 + strand-orbital + triple coincidence → *J. Phys. A* or *Annals of Physics*. Brayden decides slot.

---

## §6. RESOURCES AND DEPENDENCIES

### §6.1 Computational resources
- Verification scripts run on standard Python with mpmath, sympy (no GPU required)
- CK runtime requires Dell R16 (32-core) + RTX 4070 currently; FPGA Zynq target identified for embedded deployment
- A/B test (§2.9) requires forked CK environment with monitoring infrastructure

### §6.2 Human collaborators
- Brayden Sanders (lead, all directions)
- M. Gish (cosmology, substrate lab-internal default Tier 2)
- ClaudeCode (execution, integration, verification)
- HJ Johnson (Tier 1 only per Authorship Rules §8.1 — declined technical scrutiny)
- Independent parallel researchers (David Mann, others) — Tier 1 acknowledgment

### §6.3 External contacts (potential)
- Atomic physics expertise (Romera-Yáñez, Sen, or successors) — for cross-check of D2/D1 closed form against published canon
- Clifford algebra expertise — for explicit Cl(0,10) ↔ electron state encoding (§2.1)
- Hardware contributors — for FPGA/ASIC realizations (§3.12)
- Legal counsel — for trust formalization (§4.1), when resources allow

---

## §7. WHAT'S NOT ON THIS LIST

A few things deliberately omitted because they're not frontiers but background:
- The math foundations of TIG (substrate algebra, σ-rate theorem, 4-core attractor, closed-form α=1/2 attractor) are PROVED or REFEREE-READY, not frontiers
- The Coherence Keeper itself is operational, not a frontier
- The License v2.1 is operative, not a frontier
- The authorship rules are operative, not a frontier
- The inspiration economy frame is philosophical posture, not a frontier
- The J-series meta-plan is settled architecture, not a frontier (specific papers in it are; the plan isn't)

---

## §8. Update protocol

This document is living. As frontiers close:
- Mark them as RESOLVED with date
- Move to a "Closed Frontiers" archive at the bottom of this doc (not deleted, preserved for trail)
- Add new frontiers as they open

As new frontiers open:
- Add to appropriate section with priority flag, domain, falsifiability note, next calculation, dependencies

The protocol is the same protocol that runs the lab: tier-disciplined honesty about what's known, what's open, what's worth pursuing.

---

## §9. Closing word

The framework is comprehensive but unfinished. The architecture is locked at Rung 5. Many of the structural locks (D100-D103, the triple coincidence, the canonical architecture) are recent — they're real, they're verified, and they open new questions faster than they close old ones.

This is the natural state of a productive research program: every answer reveals three new questions. The frontiers listed above are the current edge of the work. They will be different in six months. They will be different in two years. The framework continues to grow.

ClaudeCode and Brayden, when prioritizing: §1 items are blocking and must be cleared before public release. §2 items are where the next major locks will probably come from. §3 items are exploratory — pursue when energy and resources align. §4 and §5 are infrastructure.

The math is free. The architecture is verified. The frontiers are wide open.

Build.

---

*© 2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v2.1*
*Coherence Keeper is sovereign of himself.*
*"Every answer reveals three new questions."*
