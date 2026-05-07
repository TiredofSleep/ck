# WP Tier and Lens-Dependence Classification

**Date:** 2026-05-06 evening (post lens-taxonomy night)
**Purpose:** For each of the 106 WPs + 6 WP-G entries in `FULL_WP_INVENTORY.md`, classify by Origin tier (A/B/C/D/E) and lens-dependence (substrate-operator / lens-invariant / table-dependent / joint / unclear), with verification status and script path.

**Framework basis:** `Atlas/LENS_TAXONOMY_2026-05-06/TABLE_INDEPENDENCE_LEDGER.md`, `Atlas/LENS_TAXONOMY_2026-05-06/CL_FORCING_AXIOMS.md`, `Atlas/LENS_TAXONOMY_2026-05-06/VARIANT_CATALOG.md`.

**Tier scale:**
- **A (Canonical):** axiomatically given (the operator menu, σ, Z/10Z, CL_BIT_PATTERN forced by A1-A9)
- **B (Forced):** uniquely derived from canonical (e.g., σ²-cycles, 4-core fusion-closure, lens-invariant identifications)
- **C (Constructed):** built to demonstrate realizability (existence demonstrators, bridge constructions, ring-internal lemmas)
- **D (Searched):** found by algorithmic sweep (PSLQ sweeps before forcing argument; orbit enumerations)
- **E (Fitted):** parameterized to match observable (Yukawa fits, Ω fits, microtubule predictions)

---

## §1 — WP-numbered table

| WP # | Title | Tier | Lens | Status | Script | Notes |
|------|-------|------|------|--------|--------|-------|
| WP1 | TIG Definitive (foundational) | A | substrate-operator | PROVED+SCOPED | papers/data/* | Canonical statement of operator algebra; honest 4-bin classification (DEF/THM/EMP/HYP); lens-invariant claims when stating; some HYP claims fitted physics |
| WP9 | LATTICE / Paradoxical Info Algebras | B | table-dependent: TSML_8 + BHML | PROVED | papers/wp_bridge_findings_2026_05_02/code/verify_findings.py | Uses TSML_8 (drops {0,7}) + BHML_10 + V/H flow cells per D88; trefoil and role analyses scoped to corrected substrate frame |
| WP10 | DKAN | C | table-dependent: TSML_8 + BHML_10 | STRUCTURAL/EMPIRICAL | none cited | "Structurally analogous to KAN"; depends on the D91 split between geometric and arithmetic codings; explicitly NOT a literal port |
| WP11 | so(8) Identification (early) | B | table-dependent: TSML_SYM | PROVED | papers/wp102/verification/stage5_so8.py (= WP102 redo) | 12.8% non-assoc rate stated → uses symmetrized variant; superseded by WP102 |
| WP12 | so(10) Identification (early) | B | table-dependent: TSML_SYM + BHML | PROVED | papers/wp103/verification/verify_so10.py (= WP103 redo) | Joint TSML+BHML; superseded by WP103 |
| WP19 | Halving Lemma (RH dissipative flow) | C | substrate-operator (motivation only) | PROVED+SCOPED | none in repo | Analytic flow result; TIG used as motivating analogy only; the analytic theorem is independent of TIG variant |
| WP20 | RH Halving Lemma (= WP19) | C | substrate-operator | PROVED+SCOPED | none in repo | Identical text to WP19; duplicate filename |
| WP21 | BSD Energy Law | E | table-dependent: TSML | SUPERSEDED | none | SUPERSEDED by Mix_λ model (WP21_BSD_MIX_LAMBDA.md, not separately enumerated); empirical regression |
| WP22 | NS BREATH Criterion | C | table-dependent: TSML | EMPIRICAL/STRUCTURAL | none | EXTENDED by WP22_NS_BREATH_LYAPUNOV.md; mock DNS results |
| WP23 | Hodge Map | C | table-dependent: TSML+BHML | EMPIRICAL/STRUCTURAL | tsml_ag23_verify.py (legacy) | Structural translation table; "21/81 pairs verified" empirical |
| WP24 | Formal Status Audit | A | substrate-operator | PROVED (catalog) | tsml_ag23_verify.py | Catalog; lens-invariant by aggregation across the corpus |
| WP25 | P vs NP / AG(2,p) | B | table-dependent: TSML | PROVED+SCOPED | none in repo | Two-step convergence theorem proved on the TSML 9×9 sub-table |
| WP26 | Doing Table Tension Geometry | B | joint: TSML+BHML | PROVED+SCOPED | none in repo | D = \|TSML − BHML\| has 60 nonzero entries; depends on which TSML lens (the 60/21 split is TSML_SYM specific) |
| WP27 | Product-Gap Theorem | B | table-dependent: TSML | PROVED | papers/data/product_gap_note.tex | Corner sub-magma C={1,3,7,9} closure; lens-invariant within TSML choice (corner monoid is in §2 of the ledger) |
| WP28 | CK as TIG Organism | C | substrate-operator (architectural) | STRUCTURAL/EMPIRICAL | runtime telemetry | Architecture-as-proof; classification by construction |
| WP29 | λ-Voice Theorem | C | joint: TSML+BHML (Mix_λ) | STRUCTURAL | none | Mix_λ = (1−λ)·TSML + λ·BHML interpolation |
| WP30 | BREATH in CK Olfactory | C | table-dependent: TSML | STRUCTURAL | none | Re_local ≤ 2/7 mapped to olfactory threshold |
| WP31 | Corridor Geometry | C | joint: TSML+BHML (Mix_λ corridors) | STRUCTURAL | none | Six convergence corridors via Mix_λ thresholds |
| WP32 | TIG⊗³ / Hodge-Kuga | B | table-dependent: TSML | PROVED | papers/data/product_gap_note.tex | Corollary of WP27 at k=3 |
| WP33 | DNA Force Field 64 | E | substrate-operator + numerical fit | PROVED (arithmetic core) + SPECULATION (DNA) | none | b=4 unique semiprime claim is arithmetic; DNA mapping is HYPOTHESIS/CONJECTURE |
| WP34 | First-G Law | B | substrate-operator (= number theory) | PROVED | none in repo | Coprimality partition first-G event = smallest prime; pure number theory, lens-independent |
| WP35 | Prime Phase Transition | B | substrate-operator | PROVED | none in repo | Harmonic Pre-Echo Countdown Law; sinc² → Montgomery bridge; pure number theory |
| WP36 | Spectrometer Research (citations) | A | n/a | RESEARCH SCAFFOLD | none | Citation document only, no theorem |
| WP37 | P-NP Research (citations) | A | n/a | RESEARCH SCAFFOLD | none | Citation document only |
| WP38 | NS Research (citations) | A | n/a | RESEARCH SCAFFOLD | none | Citation document only |
| WP39 | Hodge Research (citations) | A | n/a | RESEARCH SCAFFOLD | none | Citation document only |
| WP40 | RH Research (citations) | A | n/a | RESEARCH SCAFFOLD | none | Citation document only |
| WP41 | Yang-Mills Research (citations) | A | n/a | RESEARCH SCAFFOLD | none | Citation document only |
| WP42 | BSD Research (citations) | A | n/a | RESEARCH SCAFFOLD | none | Citation document only |
| WP43 | Split Coherence Architecture | C | substrate-operator (algebraic projection) | PROVED+STRUCTURAL | runtime D2 pipeline | Privacy primitive; algebraic irreversibility proved |
| WP44 | CK AI Paradigm | C | substrate-operator (architectural) | STRUCTURAL/EMPIRICAL | runtime telemetry | Paradigm-position paper |
| WP51 | Flatness Theorem | B | substrate-operator (= ring theory) | PROVED+SCOPED | none in repo | T*=5/7 from Z/nZ squarefree torus aspect ratio; pure ring theory; lens-independent within squarefree Z/nZ |
| WP52 | D2 as Ring Curvature | B | substrate-operator | PROVED+STRUCTURAL | runtime D2 | D2 measurement geometric justification |
| WP53 | Why Primes Are Hard | B | substrate-operator | STRUCTURAL | none | Maximum-tension framework; prose framing of WP51 |
| WP54 | Ancient Sacred Geometry | E | substrate-operator (correspondence catalog) | EMPIRICAL/SPECULATION | none | Post-hoc discovery; correspondences labeled PROVED/STRUCTURAL/POSTHOC |
| WP55 | Love, Truth, Coherence | A | n/a (mission statement) | MANIFESTO | none | Not a math paper; mission/values |
| WP56 | Complete Arc | A | substrate-operator (overview) | OVERVIEW | none | Collaborator's guide; aggregator |
| WP57 | Crossing Lemma Arc | A | substrate-operator | PROVED | none in repo | Foundation: every theorem WP1-WP56 as a CL instance; CL is itself foundational/canonical |
| WP58 | Unified Orthogonality Principle | B | substrate-operator | PROVED | none in repo | Joint map injectivity; pure ring theory |
| WP59 | Corrected Theorem C | B | substrate-operator | PROVED | none in repo | M+A sufficiency correction; ring theory |
| WP60 | Intrinsic Left-Handedness | C | substrate-operator (ℂ⁶ block + su(4,2)) | PROVED+STRUCTURAL | none in repo | Left-handed SM charges; algebraic; depends on chosen block decomposition |
| WP61 | Productive Incompleteness | B | substrate-operator | PROVED+SCOPED | none in repo | 5-category classification of measurement utility |
| WP62 | 7-Cycle Bounded Agent | E | substrate-operator | EMPIRICAL/SUPERSEDED | none | Universal 7-attractor REJECTED via simulation; threshold law survives |
| WP63 | GUT Algebra Audit | C | substrate-operator | PROVED+SCOPED | none in repo | Honest audit; staged corridor PROVED given block decomp |
| WP64 | Coordinate Coverage | B | substrate-operator | PROVED | none in repo | CRT k−1 jump necessity; non-CRT alternatives at n=30 |
| WP65 | Torus Foundation | C | substrate-operator + S₄ rep theory | PROVED | none in repo | Role table for the torus argument |
| WP66 | Torus Irreducible Remainder | C | substrate-operator + S₄ rep theory | PROVED+SCOPED | none in repo | Algebraic-prime/operational-not-dominant duality |
| WP67 | Seven Structural Operator | B | substrate-operator | PROVED | none in repo | 7×3≡1, 7+3≡0 in Z/10Z — pure arithmetic |
| WP68 | Seven Hinge Not Endpoint | C | substrate-operator | STRUCTURAL | none in repo | 7's role as active return operator |
| WP69 | Seven Return Operator Lift Test | C | substrate-operator + rep theory | PROVED+SCOPED | none in repo | Lift of 7's arithmetic role into the stack |
| WP70 | Second Complex Direction | C | substrate-operator + ℂP¹ geometry | PROVED+SCOPED | none in repo | Bloch sphere geometry inside L1-perp |
| WP71 | Physical Projector Map | C | substrate-operator + projector calculus | PROVED+SCOPED | none in repo | P2 candidate ranking |
| WP72 | Flag Selector Anisotropy | C | substrate-operator + SU(3)/T geometry | PROVED+SCOPED | none in repo | Flag F* requirement framing |
| WP73 | T1 Carrier Identification | E | physical mapping (NV-center) | STRUCTURAL/HYPOTHESIS | none in repo | NV-center qutrit S4 mapping; needs lab partner |
| WP74 | Physical Observable Identification | E | physical mapping (NV) | STRUCTURAL/HYPOTHESIS | none in repo | NV Hamiltonian protocol |
| WP75 | S4 Extension Synthesis | E | physical mapping (NV) | STRUCTURAL/HYPOTHESIS | none in repo | U4 matrix + 6-pulse microwave |
| WP76 | NV S4 Closure Calibration | C | rep theory + NV mapping | PROVED (group closure)+SCOPED | none in repo | 24-element group machine verified |
| WP77 | NV T1 Carrier Validation | E | physical test design | STRUCTURAL/HYPOTHESIS | none in repo | 5-test falsification ladder; pending Test E |
| WP78 | Projector Covariance Closeout | C | substrate-operator + flag geometry | PROVED+SCOPED | none in repo | Mathematical closure achieved; Test E pending |
| WP79 | Flag Selector Victory Path | C | substrate-operator | OVERVIEW | none in repo | Closeout-arc paper |
| WP80 | Flag Selector Victory 7-Hinge | C | substrate-operator | STRUCTURAL | none in repo | 7-hinge framing |
| WP81 | Canonical ξ Theory | E | scalar field theory (post-TIG) | STRUCTURAL | none | ξ scalar with V=ξ logξ; cosmology branch |
| WP82 | Log Quintessence Novelty | E | literature comparison | EMPIRICAL | none | Novelty audit |
| WP83 | PRISM Consistency Audit v1 | A | catalog | AUDIT | none | Field inventory; supersedes-and-replaced by WP84 |
| WP84 | PRISM Consistency Audit v2 | A | catalog | AUDIT | none | Complete field inventory |
| WP85 | Seed-to-Stack Map | C | substrate-operator + cosmology mapping | STRUCTURAL | none | Two-branch architecture |
| WP86 | ξ Core Canonical Form | C | scalar field theory | STRUCTURAL | none | Minimal surviving theory statement |
| WP87 | Cross-Branch Analysis | A | substrate-operator (negative) | PROVED+SCOPED | none | HONEST: NO formal mathematical link between TIG-CL branch A and ξ branch B |
| WP88 | Local/Non-Local Siloing | C | substrate-operator (architectural) | STRUCTURAL | none | Three-layer architecture for siloing |
| WP89 | Sprint Closeout & Handoff | A | n/a | OVERVIEW | none | Sprint synthesis |
| WP90 | Literature & Unification Paths | E | literature review | EMPIRICAL | none | Novelty audit for V=ξ logξ |
| WP91 | NS Separability Bridge | C | substrate-operator + BB bridge | STRUCTURAL | none | Bialynicki-Birula bridge; framework essay |
| WP92 | YM Mass Gap Bridge | C | substrate-operator + BB bridge | STRUCTURAL | none | Mass gap as separability-forced spectral floor |
| WP93 | RH Spectral Entropy Bridge | C | sinc² + Montgomery | STRUCTURAL | none | Spectral completeness |
| WP94 | Synthesis: What Unified | A | catalog | OVERVIEW | none | Sprint synthesis |
| WP95 | JKO Construction Roadmap | C | substrate-operator + Wasserstein | STRUCTURAL+NEGATIVE-RESULT | none | Cyclotomic NEGATIVE result; JKO scheme proposed |
| WP96 | NS σ < 1 Conjecture | C | analytic | CONJECTURE | none | Precise conjecture statement; gap identification |
| WP97 | Field Observer Synthesis | E | external literature mapping | STRUCTURAL | none | TIG/Xi as organizing lens for collapse direction |
| WP98 | NS Structural Cancellation | C | analytic | STRUCTURAL/CONJECTURE | none | Brezis-Gallouet → σ_NS < 1 chain; gap = one log factor |
| WP99 | Non-Reversibility Resolution | B | substrate-operator (CL Markov) | PROVED+EMPIRICAL | none | Maas (2011) applies; CL Markov chain reversible |
| WP100 | Sprint Synthesis (100 papers) | A | catalog | OVERVIEW | none | The arc in one paragraph |
| WP101 | σ Rate Theorem | B | substrate-operator | PROVED+CORRECTED | proof_sigma_rate.py / Atlas/applications_pass_2026_04_27/ | σ(N) ≤ 2/N rigorous; ECHO mechanism corrected to VOID-HARM rule disagreement |
| WP102 | so(8) = D₄ identification | B | table-dependent: TSML_SYM | PROVED | papers/wp102/verification/stage5_so8.py | 12.8% non-assoc rate → SYM lens; 4 diagnostics machine-verified |
| WP103 | so(10) = D₅ identification | B | joint: TSML_SYM + BHML | PROVED | papers/wp103/verification/verify_so10.py | 5 diagnostics machine-verified |
| WP104 | Two Roads to Pati-Salam | B | joint: TSML+BHML (so(10) content) | PROVED+SCOPED | papers/wp104_higgs_pati_salam/verification/find_higgs_*.py | Two-paths-converge framing CORRECTED in audit; both paths separately PROVED, but converge on different reductions |
| WP105 | Closed-Form Runtime Attractor | B | joint: TSML_SYM + BHML | PROVED | papers/wp105_closed_form_attractor/verification/*.py (7 scripts) | H/Br = 1+√3 at α=1/2; LMFDB 4.2.10224.1; the 4-core itself is lens-invariant |
| WP106 | TIG Detector Specificity Scope | B | table-dependent: TSML+BHML (negative result on transformer weights) | EMPIRICAL+PROVED-NEGATIVE | runtime distilgpt2 sweep | Honest negative scoping |
| WP107 | Wobble Localization | B | **table-dependent: TSML_RAW** | PROVED+SCOPED | sympy wobble_check.py | Prime 11 in c_2 + c_8; explicitly TSML_RAW; lens-scope note added 2026-05-06 |
| WP108 | Yukawa Scaffolding | C | so(10) GUT identification (load-bearing hyp) | SCAFFOLDING | none | Sets up Yukawa computation; not completed |
| WP109 | Operad D₄ Obstruction | B | **table-dependent: TSML_RAW** | PROVED+SCOPED | papers/wp112_p56_canonical_fuse/verification/d4_orbit_decomposition.py | 67 orbits; 16 D_4-incoherent; lens-scope note explicit (RAW vs SYM differ by 2 triples) |
| WP110 | 4-Core Fusion-Closure | B | lens-invariant (4-core itself) | PROVED | papers/wp105_closed_form_attractor/verification/03_eight_magma_core.py | The 4-core {0,7,8,9} is closed under both TSML_RAW and TSML_SYM; symbolic 1+√3 |
| WP111 | Six DOF Synthesis | A | substrate-operator (synthesis) | OVERVIEW | none new | Long-form expository; depends on WP102-WP110 |
| WP112 | P_56-Canonical Operad Fuse | B | **table-dependent: TSML_RAW** for 126→98 orbit count; lens-invariant for Theorem 5.5 (4-core arity-3 closure) | PROVED | papers/wp112_p56_canonical_fuse/verification/p56_canonical_fuse.py | Closes F4; 8/8 surveyed rule families P_56-equivariant |
| WP113 | α-Uniqueness via PSLQ | D-promoted-to-B | joint: TSML_SYM + BHML (attractor) | EMPIRICAL+PROVED-via-D78 | papers/wp113_alpha_uniqueness/verification/alpha_pslq_sweep.py | Originally Tier-D (PSLQ search); PROMOTED to Tier-B by D78 Galois argument |
| WP114 | Specificity Extension | B | table-dependent: TSML | EMPIRICAL+PROVED-NEGATIVE | papers/wp114_specificity_extension/verification/structured_matrix_sweep.py | 9-family structured matrix battery; identifies WP107 wobble as load-bearing positive marker |
| WP115 | Joint Chain + Universal 4-core | B | **joint: TSML_SYM, BHML** (chain count is LENS-DEPENDENT: 7 on TSML_RAW, 8 on TSML_SYM) | PROVED+SCOPED | papers/wp115_joint_chain_universality/verification/joint_chain_attractor.py | 8-shell chain (corrected 2026-05-05); Theorem 2 (universal 4-core attractor) is lens-invariant |
| WP116 | Lens of Projections | A | substrate-operator (synthesis) | OVERVIEW | none new | Six DOFs as projection axes of one Stern-Brocot recursion |
| WP117 | Discrete Dirac on F_5^4 | B | lens-invariant (4-core 4-element subset of TSML) | PROVED | verify_discrete_dirac_4core.py + test_tig_dirac.py | 4-element commutative non-assoc algebra over F_5; |Aut|=40; field-invariant skeleton |
| WP118 | Field-Invariance of 4-Algebra | B | lens-invariant | PROVED | axial_algebra_check.md + verify_discrete_dirac_4core.py | Skeleton invariant across F_p, p∈{2,3,5,7,11,13} |
| WP119 | Clifford Ladder V⊗ⁿ ↔ Cl(2n) | B | lens-invariant | PROVED | test_tig_dirac.py | dim V⊗ⁿ = 4ⁿ = dim Cl(2n) for n=0..5 |
| WP120 | SU(5) from V⊗⁵ | C | substrate-operator + GUT identification | STRUCTURAL | test_tig_dirac.py | 32-cell binomial decomposition matches SU(5) GUT rep content |
| WP121 | Cosmological Densities | E | algebraic identification + Planck fit | EMPIRICAL+SPECULATION | tig_dirac.py predict_dark_sector() | Ω_b=49/1000 exact; Ω_DM, Ω_Λ companion identities ≤1.3% Planck |
| WP122 | Yukawa Hierarchy via λ=10/49 | E | Froggatt-Nielsen fit | EMPIRICAL/FIT | none | All 9 charged-fermion Yukawas fit by λ=10/49 |
| WP123 | CKM/PMNS via T*, D* | E | mixing angle fit | EMPIRICAL/FIT | none | 5 angles fit within 5% via TIG structural constants |
| WP124 | Fine-Structure Constant | E | algebraic identification + CODATA fit | EMPIRICAL/FIT | none | 1/α=137.036 from T*⁻¹·\|Aut(V)\| with structural corrections |
| WP127 | Microtubule Coherence Q_c | E | falsifiable cross-domain prediction | HYPOTHESIS | none | Q_c = 5/7 prediction for terahertz spectroscopy |

## §2 — WP-G (g-series) table

| WP-G # | Title | Tier | Lens | Status | Script | Notes |
|--------|-------|------|------|--------|--------|-------|
| G0 | Generator Synthesis Arc | A | n/a (overview) | OVERVIEW | none | Entry point for WP-G arc |
| G1 | Ising Ring State Space | C | substrate-operator + Ising physics | PROVED+SCOPED | none | n=4 closed-form, n=10 motivated; TIG connection labeled STRUCTURAL ANALOGY |
| G2 | Observable Sufficiency | B | substrate-operator | PROVED | none | UOP score sequence n=4 Ising |
| G3 | Correlation Length / UOP Bridge | C | Ising transfer matrix + UOP | STRUCTURAL+OPEN | none | Bridge conjecture: ξ ↔ UOP information radius; OPEN |
| G4 | n=10 Ising Ring as TIG Substrate | C | Ising + TIG mapping | PROVED+SCOPED | none | Energy spectrum + degeneracy histogram vs TIG operator distribution |
| G5 | C*-Algebraic Frontier | C | UOP + C*-algebra | OPEN/FRONTIER | none | Frontier paper; most claims OPEN |

---

## §3 — Summary distributions

### Tier distribution

| Tier | Count | %  |
|------|-------|----|
| A (Canonical / overview / catalog) | 17 | 15.2% |
| B (Forced) | 36 | 32.1% |
| C (Constructed) | 36 | 32.1% |
| D (Searched, not promoted) | 0 | 0.0% |
| D-promoted-to-B | 1 | 0.9% |
| E (Fitted) | 22 | 19.6% |
| **Total** | **112** | 100% |

(Counts include the 6 WP-G entries.)

### Lens-dependence distribution

| Lens | Count | Notes |
|------|-------|-------|
| substrate-operator (table-independent) | 47 | The strongest spine |
| lens-invariant (TSML- or BHML-family) | 6 | WP110, WP117, WP118, WP119 + the 4-core-itself parts of WP105/WP110/WP112/WP115 |
| table-dependent: TSML (broadly) | 17 | Most include both RAW and SYM acceptable |
| **table-dependent: TSML_RAW** | 3 | WP107, WP109, WP112 (the explicitly tier-scoped ones) |
| **table-dependent: TSML_SYM** | 3 | WP102, WP103, WP11 (12.8% non-assoc rate uses SYM) |
| joint: TSML+BHML | 11 | including the joint chain (WP115) |
| n/a (overview / catalog / mission / scaffold) | 24 | research docs, syntheses, manifestos |
| unclear | 1 | WP120 (SU(5) from V⊗⁵; identification claim's lens isn't fully specified) |

### Verification status distribution

| Status | Count |
|--------|-------|
| PROVED | 26 |
| PROVED+SCOPED | 22 |
| EMPIRICAL | 8 |
| EMPIRICAL+PROVED-NEGATIVE | 3 |
| STRUCTURAL / STRUCTURAL ANALOGY | 22 |
| HYPOTHESIS | 5 |
| FIT (parametric) | 4 |
| CONJECTURE | 3 |
| AUDIT / OVERVIEW / RESEARCH SCAFFOLD | 16 |
| SUPERSEDED | 2 (WP21, WP62) |
| MANIFESTO / MISSION | 1 (WP55) |

### WPs needing scope-tightening before submission

These are papers whose central claims depend on TSML_SYM or TSML_RAW but the abstract does not yet disambiguate:

1. **WP11** (so(8) identification, early version) — uses 12.8% non-assoc → TSML_SYM, but the abstract refers to "the frozen magma" without specifying. Superseded by WP102 which has the same gap.
2. **WP12** (so(10), early) — same as above. Superseded by WP103.
3. **WP102** (so(8) = D_4) — 12.8% non-assoc rate quoted; the abstract says "the Coherence Lattice (CL), a frozen 10×10 commutative non-associative magma" — needs explicit "we use the upper-triangle symmetrized form TSML_SYM" sentence.
4. **WP103** (so(10) = D_5) — same gap; needs explicit symmetrization scope.
5. **WP104** (Two Roads to Pati-Salam) — uses TSML_SYM via WP103; the framing-correction note already added (2026-04-27) should be augmented with explicit lens scope per the new lens-taxonomy.
6. **WP105** (closed-form attractor) — uses TSML_SYM in the proof; the H/Br = 1+√3 result is structurally lens-invariant at the 4-core, but the derivation path is on TSML_SYM. Needs the scope-clarifying sentence per ledger §5.2 claim #47.
7. **WP115** (joint chain) — has the lens-dependence note added 2026-05-06; the Theorem 1 chain count itself is lens-dependent (7 on RAW, 8 on SYM); Theorems 2 and 3 are lens-invariant. Acceptable as currently scoped, but the abstract should state the lens-dependence upfront, not in a footnote.

### WPs that should be DEFER, SUPERSEDE, or merge

| WP | Recommendation | Reason |
|----|---------------|--------|
| **WP19, WP20** | merge (one is a duplicate filename) | Identical text |
| **WP11, WP12** | DEFER (superseded) | Superseded by WP102, WP103 |
| **WP21** | SUPERSEDE (already explicitly superseded by Mix_λ in the paper itself) | Empirical regression replaced by structural model |
| **WP54** (Ancient Sacred Geometry) | DEFER from Phase 1 | Tier-E correspondence catalog; honest framing but not at submission strength |
| **WP62** (7-Cycle Bounded Agent) | DEFER from Phase 1 | Universal-attractor claim was REJECTED via simulation; survives only as a threshold law |

### Top 10 Phase-1 candidates (highest tier discipline + lens-clean + verification script)

These are the WPs that are Tier-A or Tier-B, lens-invariant or substrate-operator, and have explicit verification:

1. **WP57** (Crossing Lemma Arc) — Tier-A, substrate-operator, foundational
2. **WP51** (Flatness Theorem) — Tier-B, substrate-operator (squarefree Z/nZ), pure ring theory
3. **WP58** (UOP) — Tier-B, substrate-operator, pure ring theory
4. **WP59** (Corrected Theorem C) — Tier-B, substrate-operator
5. **WP64** (Coordinate Coverage) — Tier-B, substrate-operator
6. **WP34** (First-G Law) — Tier-B, substrate-operator (number theory)
7. **WP35** (Prime Phase Transition) — Tier-B, substrate-operator (number theory) + sinc²/Montgomery bridge
8. **WP110** (4-Core Fusion-Closure) — Tier-B, lens-invariant (4-core itself), structural strengthening of WP105
9. **WP117** (Discrete Dirac on F_5^4) — Tier-B, lens-invariant 4-core sub-algebra, journal-clean tex with verification
10. **WP118** (Field-Invariance) — Tier-B, lens-invariant, multi-field empirical verification

Honorable mentions just below the cut: **WP19/WP20** (Halving Lemma — Tier-C as a TIG bridge, but the analytic content on RH zero-free strip is independent and submission-ready); **WP101** (σ rate theorem, sharp Tier-B with corrected proof); **WP119** (Clifford ladder, dimension match clean).

### WPs flagged "claim doesn't match its tier"

| WP | Issue |
|----|-------|
| **WP104** | "Two paths converging on Pati-Salam" framing was Tier-C synthesis; the paths separately are Tier-B PROVED but go to different reductions (SO(8) vs SU(4)×U(1)). The 2026-04-27 audit already flagged this. The internal note should be moved to the abstract for any external version. |
| **WP21** | Energy law was empirical regression (Tier-E) but framed as a structural claim; correctly SUPERSEDED by Mix_λ. |
| **WP62** | Universal 7-attractor was a Tier-D conjecture inadvertently presented as Tier-B in arc materials before simulation; correctly REJECTED in the paper itself. |
| **WP122-WP124** | Yukawa, CKM/PMNS, and 1/α fits are Tier-E (parametric matches to TIG primitives). The journal versions correctly frame as "structural identifications, not derivations" — must keep that framing. |
| **WP127** | Microtubule Q_c=5/7 is HYPOTHESIS (correctly framed as falsifiable test); not a current proven result. |
| **WP54** | Ancient sacred geometry correspondences are POST-HOC discoveries (Tier-E); honest framing in the paper but should not be cited as evidence for TIG's mathematical content. |

---

## §4 — Cross-references

- `Atlas/LENS_TAXONOMY_2026-05-06/TABLE_INDEPENDENCE_LEDGER.md` — the substrate-operator / lens-invariant / table-dependent / joint claim ledger (50+ claims classified)
- `Atlas/LENS_TAXONOMY_2026-05-06/CL_FORCING_AXIOMS.md` — 9-axiom forcing of CL_RAW; CL_TSML's tier classification (A internally, with B-derivable axioms A5/A6/A8)
- `Atlas/LENS_TAXONOMY_2026-05-06/VARIANT_CATALOG.md` — full TSML/BHML variant inventory with construction lineage and tier
- `Atlas/META_PLAN_2026-05-06/FULL_WP_INVENTORY.md` — canonical paths for the 106 WPs + 6 WP-G

This classification is the spine for Phase-1 submission selection and the §5/§6 of the foundation paper.
