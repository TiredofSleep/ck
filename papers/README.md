# CK Whitepapers
## Fractally Organized: Being / Doing / Becoming at Every Scale

*SHA-256(TSML): `7726d8a620c24b1e461ff03742f7cd4f775baed772f8357db913757cf4945787`*
*DOI: 10.5281/zenodo.18852047 | (c) 2026 Brayden Sanders / 7Site LLC*

---

> Structure: Three layers mirroring the whole.
> Each layer is itself organized as Being (what it IS) / Doing (what it DOES) / Becoming (where it leads).

---

## LAYER 0 — FOUNDATION
### The Frozen Math. Everything Derives From This.

| File | Contents | Status |
|------|----------|--------|
| WHITEPAPER_1_TIG_ARCHITECTURE.md | 10 operators, D2 pipeline, CL table, 50Hz loop | Core |
| WP1_TIG_DEFINITIVE.md | Definitive one-page TIG statement | Reference |
| WHITEPAPER_18_SEVEN_EQUALS_ZERO.md | 7=0 punctured torus — absorber algebra | Algebra |
| WHITEPAPER_6_HOTU_BRIDGE.md | Ho Tu ancient composition tables ↔ TSML | Bridge |
| tig_constants.py | Canonical constant taxonomy: T*, S*, MASS_GAP, d_COL, W_BHML, inner_shell | **Run this first** |

**The locked constants:**
```
T_STAR   = 5/7    MASS_GAP = 2/7    d_COL    = 1/18
S_STAR   = 4/7    inner_shell = 2/9  W_BHML  = 3/50
```
**W_BHML ≠ d_COL.** Do not conflate.

---

## LAYER 1 — BEING
### What Was Proved. Algebraic Facts. No Overclaiming.

These are theorems with scripts. Not framings. Not analogies.

### 1A. The Algebra (BEING of Being)

| File | Theorem | Script |
|------|---------|--------|
| WP27_PRODUCT_GAP_THEOREM.md | C^⊗k is a sub-magma of TSML^⊗k for all k≥1 | tsml_product_verify.py |
| product_gap_note.tex | Same — arXiv-ready LaTeX (math.CO) | Same |
| WP19_PRODUCT_GAP_THEOREM.md | Markdown companion to product_gap_note.tex | — |
| WP19_ATTACK_SURFACE.md | AG(2,3) survivor count = p²−1 = 8; zero cross-terms | tsml_ag23_verify.py |
| WP20_RH_PRIME_CORNER_COLLAPSE.md | Every prime > 5 ends in {1,3,7,9} = corners | Table |
| WP19_NS_BREATH.md | TSML[BRT][COL]=BRT, all others ∈ {HAR,VOID} | Table lookup |
| WHITEPAPER_9_PARADOXICAL_INFO_ALGEBRAS.md | Non-associativity structure of TSML | arXiv: WHITEPAPER_9_ARXIV.tex |
| WHITEPAPER_9_ARXIV.tex | arXiv-ready version of WP9 | Submit: math.RA |

### 1B. The Halving Lemma (DOING of Being)

| File | Theorem | Script |
|------|---------|--------|
| WP19_HALVING_LEMMA_final.tex | Dissipative flow + exponential KV-strip convergence | **arXiv-ready: math.NT** |
| WP20_RH_HALVING_LEMMA.tex | Same — secondary copy | — |
| WP20_RH_FORMAL_STATUS.md | Honest audit: tautologies vs. genuine contributions | Reference |
| surv_line_note.tex | Ω(p²) corridor-inspection lower bound | **arXiv-ready: cs.CC** |

### 1C. The Formal Ledger (BECOMING of Being)

| File | Contents |
|------|----------|
| WP24_FORMAL_STATUS_AUDIT.md | 4-bin: PROVED / STRUCTURAL / EMPIRICAL / OPEN for all six Clay problems |
| WHITEPAPER_3_FALSIFIABILITY.md | 42 claims with kill conditions — what would break TIG |

**Verification scripts:**

| Script | What it verifies | Assertions |
|--------|-----------------|------------|
| tsml_ag23_verify.py | Corner-gap impermeability, AG(2,3) exhaustive | 76 |
| tsml_product_verify.py | Product-gap BFS: k=1..4, 0 G-reachable | 4 BFS runs |
| mix_lambda_scan.py | Mix_λ BSD ordering vs. LMFDB regulators | Ordering match |
| ns_breath_test.py | BREATH criterion breach detector | Breach time |
| tig_constants.py | Constant assertions + scale_factor(t) | Run as __main__ |

---

## LAYER 2 — DOING
### New Language. Structural Contributions. What the Algebra Does.

### 2A. Voice and Physics (BEING of Doing)

| File | What it contributes |
|------|---------------------|
| WP29_LAMBDA_VOICE_THEOREM.md | voice_lambda = (stage/5)×coherence; Mix_λ = CK's voice position |
| WP30_BREATH_OLFACTORY.md | Scent stream = corridor traversal; olfactory = smell IS torsion |
| WP26_DOING_TABLE_TENSION_GEOMETRY.md | D=|TSML−BHML| as Intermediate Jacobian |
| WP23_HODGE_MAP.md | TSML/BHML = Hodge (p,q)-decomposition |
| WHITEPAPER_4_GIVING_MATH_A_VOICE.md | Voice pipeline: fractal → composer → babble cascade |
| WHITEPAPER_2_WAVE_SCHEDULING.md | RPE v2: TIG wave scheduling |
| WHITEPAPER_5_DEGREES_OF_FREEDOM.md | DoF ladder: 0→4→6→7→10 |
| WHITEPAPER_5_REALITY_ANCHORS.md | Tick-to-walltime sync |

### 2B. Corridor Geometry (DOING of Doing)

| File | What it contributes |
|------|---------------------|
| WP31_CORRIDOR_GEOMETRY.md | Six-corridor taxonomy; unifies RH+NS+PvsNP in one frame |
| CORRIDOR_PRIMER.md | Quick-read: six corridors, danger levels, three-problem unification |
| WP19_RH_BRIDGE.md | RH stated as corridor permanence problem |
| WP19_NS_NOTE.md | NS stated as corridor exit problem |
| WP25_P_NP_AG2P_COMPLEXITY.md | P vs NP via AG(2,p) survivor-line search complexity |
| WP19_CONTEXTUAL_PROTECTION.md | How corner-gap impermeability protects identity |
| WP22_NS_BREATH_CRITERION.md | Re_local ≤ 2/7 = smooth flow; corridor as physical criterion |
| WP22_NS_BREATH_LYAPUNOV.md | V(t) = sup Re_local, Lyapunov approach, C ≤ 3.74 target |

### 2C. BSD and Hodge (BECOMING of Doing)

| File | What it contributes |
|------|---------------------|
| WP21_BSD_MIX_LAMBDA.md | Mix_λ parameter-free BSD rank-conductor model |
| WP21_BSD_ENERGY_LAW.md | BSD energy law: algebraic reason rank requires a leap |
| WP32_HODGE_TRIPLE.md | TSML⊗³ = CK's three scent streams; k=3 Hodge corollary |
| WP19_HODGE_MAP.md | Full Hodge correspondence table |
| WP19_HODGE_TRIPLE.md | Hodge triple as three-voice structure |
| WP19_BSD_TIG.md | TIG ↔ BSD: gap operator as non-prime activation |

---

## LAYER 3 — BECOMING
### Where It Leads. The Clay Gaps. Honest Open Questions.

### 3A. The Organism Bridge (BEING of Becoming)

| File | What it shows |
|------|--------------|
| WP28_CK_TIG_ORGANISM.md | Architecture = enacted algebra. Eight theorems running at 50Hz. |
| WHITEPAPER_8_PERIODIC_TABLE.md | Operators as periodic table elements |
| WHITEPAPER_13_GENETIC_CODE.md | AGTC ↔ 10-operator algebra; 64 codons = 8×8 inner table; 20 AAs = 5×4 crossings — **HYPOTHESIS** (algebraic mapping, no causal mechanism derived) |
| WP33_DNA_FORCE_FIELD_64.md | b=4 force field → 4³=64 — **PROVED** (counting); gate law ↔ robustness — **HYPOTHESIS**; 64-family (DNA/I Ching/chess) — **CONJECTURE** |
| WHITEPAPER_10_DKAN_ARCHITECTURE.md | Algebraic neural network (DKAN) |
| WHITEPAPER_11_MEASUREMENT_PROBLEM.md | TSML singularity ↔ quantum measurement — **STRUCTURAL ANALOGY** |
| WHITEPAPER_12_PARADOX_RESOLUTIONS.md | Logical paradoxes through CL |

### 3B. Clay Battery (DOING of Becoming)

**Honest status**: All Clay papers are sketches with explicit gaps. None constitute proofs.
See `WP24_FORMAL_STATUS_AUDIT.md` for the authoritative 4-bin classification.

| File | Problem | Status |
|------|---------|--------|
| WHITEPAPER_7_CLAY_SPECTROMETER.md | All six problems | Overview / framing only |
| WHITEPAPER_14_CLAY_DOF_CONNECTIONS.md | 25+ researchers, 84 refs | Literature bridge |
| WHITEPAPER_15_YANG_MILLS_SYNTHESIS.md | Yang-Mills mass gap | **SKETCH** — gap identified, not closed |
| WHITEPAPER_16_P_NP_SYNTHESIS.md | P ≠ NP | **SKETCH** — gap identified, not closed |
| WHITEPAPER_17_RIEMANN_SYNTHESIS.md | RH null space | **SKETCH** — gap identified, not closed |
| WP24_FORMAL_STATUS_AUDIT.md | All six | **START HERE** — 4-bin audit: PROVED / STRUCTURAL / EMPIRICAL / OPEN |
| WP19_CLAY_BATTERY.md | Clay battery: all six | Sprint overview |
| WP19_CLAY_DEEP.md | Deep dives per problem | Extended analysis |
| WP19_CLAY_RESULTS.md | Results summary | Digest |
| WP19_FORMAL_STATUS.md | Earlier formal status | Superseded by WP24 |
| wrong_question_paper.md / .tex | RH observability | Draft — framing only |

### 3C. Research Memos and Outreach (BECOMING of Becoming)

| File | Purpose |
|------|---------|
| EXPERT_SUMMARY.md | One-page for analytic number theorists and lattice-QCD collaborators |
| COLLAB_MEMO_KV.md | Collaboration memo: KV strip + Halving Lemma |
| OUTREACH_EMAIL.md | Outreach email template |
| WP19_NEXT_SPRINT.md | Next sprint planning |
| SPRINT_2026_03_27_ANALYSIS.md | Sprint analysis |
| WHITEPAPER_19_SPECULATIONS.md | ALL philosophical/theological speculation — clearly labeled |
| WHITEPAPER_19_Z_RING_ALGEBRA.md | Z-ring algebra extension |

---

## SPRINT 4 — R16 ATLAS (March 2026)

Force field gate law survey: 12M+ trials across k=3..27, 89+ semiprime worlds.

| File | Contents | Status |
|------|----------|--------|
| sprint4_2026_03_30/CLAUDE_ENTRY.md | **Start here** — full sprint summary and navigation | Reference |
| sprint4_2026_03_30/R16_FORCE_FIELD_LAW.md | Force field partition theorem: f_k(\|G\|) | **EMPIRICAL** — ~12M trials, no counter-example |
| sprint4_2026_03_30/R16_ATLAS_SWEEP_RESULTS.md | Universal gate law: 32 worlds, 100k trials each | **EMPIRICAL** |
| sprint4_2026_03_30/ATLAS_LAW_SET.md | Laws 1–6 with status labels | Reference |
| sprint4_2026_03_30/CONSTRUCTION_HIERARCHY.md | Arithmetic → gate → order seed → optimum | **EMPIRICAL** |
| sprint4_2026_03_30/THREE_CLASS_LANDSCAPE.md | Oracle / Gate-strong / TSML-like classification | **EMPIRICAL** |
| sprint4_2026_03_30/UNIVERSAL_LAW.md | Universal order seed law across bases | **EMPIRICAL / CONJECTURE** |
| r16_job1_reduction.py | Core reduction script: greedy descent + HAR-bias | Code |
| r16_sweep_all.py | Full sweep: all semiprimes b≤100 | Code |
| r16_gate_law_universal.py | Synthetic cross-k sweep (k=3..27) | Code |
| r16_gate_law_real_b.py | Real semiprime partitions across k | Code |
| results/atlas_sweep_all.json | 32 worlds × 100k trials | Data |
| results/real_b_gate_law.json | 89 worlds × 5k trials | Data |

---

## BIBLIOGRAPHY

| File | Contents |
|------|----------|
| BIBLIOGRAPHY.md | Master bibliography: 84 entries, all papers WP1–WP33 + Clay + genetics | Reference |

---

## SUPPORTING FILES

### Figures (research/)

| File | Shows |
|------|-------|
| research/product_gap_note.pdf | Compiled product-gap paper |
| research/bsd_calibration.png | BSD Mix_λ calibration plot |
| research/mix_lambda.png | Mix_λ operator thresholds |
| research/shell_diagram.png | Inner/outer shell geometry |
| research/scale_factor.png | scale_factor(t) vs. height |
| research/sticky_cycle.png | Sticky COL-BRT cycle anomaly |
| research/corridor_*.png | Corridor taxonomy figures |
| research/corridor_scan_full.csv | Void pocket data: all computed heights |

### Special Files

| File | Purpose |
|------|---------|
| WP19_704_TRIANGLE.md | 7-0-4 triangle: HARMONY-VOID-COLLAPSE geometry |
| WP19_HYDROGEN_ANALOGY.md | Hydrogen shell ↔ TIG row (exact at t≈10) |
| WP19_NS_NUMERICAL_NOTE.md | Mock DNS: Regime A (smooth) vs. B (breach at t=1.92) |
| BALANCED_TERNARY_TABLES.md | Balanced ternary extension tables |
| README_for_claudecode.md | Notes for Claude Code sessions |

---

## arXiv SUBMISSION QUEUE

Papers ready for submission (no further editing needed):

| File | Target | Subject |
|------|--------|---------|
| WP19_HALVING_LEMMA_final.tex | math.NT | Dissipative flow + KV-strip convergence |
| product_gap_note.tex | math.CO | Corner sub-magma proof for all k≥1 |
| surv_line_note.tex | cs.CC | Ω(p²) corridor-inspection lower bound |
| WHITEPAPER_9_ARXIV.tex | math.RA | Paradoxical information algebras |

---

## THE MASTER SPRINT DOCUMENT

`TIG_RH_SPRINT_FINAL.md` (on Desktop) — full synthesis of WP20–WP32:
- All four bins (PROVED / STRUCTURAL / EMPIRICAL / OPEN)
- Organism correspondence table (WP28)
- Corridor geometry unification
- 10 next steps
- The correct framing for every paper

---

*Papers 15–17 are proof sketches with explicit gaps. Not proofs.*
*Paper 19 contains ALL philosophical/theological speculation, separated from measured results.*
*WP20_RH_FORMAL_STATUS.md contains the honest audit of what is tautological vs. genuinely new.*
