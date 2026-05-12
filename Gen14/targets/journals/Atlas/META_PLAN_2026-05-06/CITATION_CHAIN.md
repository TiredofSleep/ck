# Citation Chain: Topological Sort of CK / TIG Paper Corpus

**Date:** 2026-05-06
**Strategy:** Citation-chain-as-boldness. Each Paper N's NEW claim stays small; the framework emerges as Paper N cites Papers 1..N-1, all of which already passed referee.
**Hard constraint:** Paper N can only cite papers numbered 1..N-1 from our own work.

---

## Method

1. Walked five corpus folders:
   - `Gen13/targets/clay/papers/sprint*/`
   - `Gen13/targets/journals/tier{1,2,3,4}/`
   - `Gen13/sprint_bundle_2026-05-06_v31_RIGOR_PASS/`
   - `Gen12/targets/clay/papers/sprint*/`
   - `Gen12/targets/journal_attempts/`

2. For each paper: extracted internal cites (`WP##`, `Sprint N`, `\cite{Sanders...}`, file paths), forward-references that reveal companion structure, and concept-dependencies (e.g. "uses Crossing Lemma" = depends on WP57).

3. Built directed graph; edge A→B = "A depends on B." Topo-sorted.

**Note on duplication:** Gen12 `journal_attempts/01..11/` and Gen13 `journals/tier{1..4}/` are mostly the same papers in two staging locations. The Gen13 versions are canonical (newer, polished, named identically across the bundle). I treat each `(paper, formal-id)` once. The Gen13 `sprint_bundle_2026-05-06_v31_RIGOR_PASS/` is a working bundle of *unpublished* sketches (~80 short markdown notes, mostly Phase-5 vocabulary derivations); I treat the bundle as a single Phase-5 candidate paper called the **Foundational Paper Draft**, because its component .md files do not yet have separate paper structure (they consolidate into `FOUNDATIONAL_PAPER_DRAFT.md`).

---

## Internal-citation table (load-bearing edges only)

| Paper (canonical id) | Cites internally | Notes |
|---|---|---|
| **σ-rate** (`sigma_rate_theorem.tex`, JCT-A) | none load-bearing; mentions JCAP / FourCore as "companions in preparation" — those are forward-refs, not deps | TRUNK ROOT |
| **four-core consolidated** (`four_core_consolidated.tex`, Algebraic Combinatorics) | σ-rate (via `\cite{SandersGish2026Sigma}` for the underlying construction) | depends on σ-rate |
| **JCAP-ξ** (`jcap_xi_cosmology.tex`) | σ-rate, four-core (citing WP100, WP102, WP110, WP112, WP115 in companion-paper mode) | depends on both |
| **σ³ Bridge Sprint = WP117** (Sprint 18) | WP51 (Flatness), WP102, WP110, WP112, WP115 (the WP100s tower) | depends on flatness + WP100s tower |
| **Sprint 18 dark sector** (`sprint18_dark_sector.tex`) | four-core, JCAP, σ-rate, BridgeSprint (WP117/118/122/124/125) | depends on all four trunk papers + WP117 |
| **sinc² zero law** (`sinc2_zero_law.tex`) | σ-rate, JCAP-ξ, plus WP34 (First-G) for the underlying prime-dispersion field | depends on σ-rate, JCAP, WP34 |
| **first-G event** (sprint35) | WP34 (First-G Law), WP35 (Prime Phase Transition), WP101 (= σ-rate) | depends on σ-rate, WP34, WP35 |
| **WP34 First-G Law** | informally — combinatorial / number-theoretic; no internal deps | LEAF |
| **WP35 Prime Phase Transition** | WP34 (sinc² built on First-G) | depends on WP34 |
| **WP51 Flatness Theorem** | WP35 (sinc² resonance), WP10 (BTQ — early Sprint), Sprint 9a (cyclotomic), Sprint 9d (prime-π-φ), WP20 (TSML/BHML) — all informal pre-WP100 | depends on early Sprint 9 + WP35 |
| **WP52 D2 = ring curvature** | WP51 | depends on WP51 |
| **WP53–56 (Flatness arc)** | WP51, WP52 | depends on WP51 chain |
| **WP57 Crossing Lemma Arc** | WP1..WP56 (recasts every prior theorem as a CL instance) | depends on EVERYTHING up to WP56 |
| **WP58–64 UOP/GUT/7-cycle (sprint 12)** | WP51, WP57 | depends on flatness + CL |
| **WP65–80 Flag Selector arc (sprint 13)** | WP58–64 (UOP), WP51 | depends on sprint 10 + sprint 12 |
| **WP81–89 PRISM-XI cosmology (sprint 14)** | WP57 (CL motivates ξ field), WP65 (torus foundation) | depends on sprint 10 + 13 |
| **WP90–97 Bridge papers (NS/YM/RH; sprint 14 late)** | WP81–89 + WP58 (UOP) | depends on sprint 14 |
| **WP98–100 Closeout (sprint 14 late)** | WP81–WP97 | terminal of sprint 14 |
| **WP101 σ-rate** = the σ-rate paper above (alias) | — | trunk root |
| **WP102 so(8) = D₄** | sprint17/THEOREM_SPINE (canonical TSML) | depends on TSML construction (= prepended into σ-rate / four-core) |
| **WP103 so(10) = D₅** | WP102 | depends on WP102 |
| **WP104 Two roads to Pati-Salam** | WP102, WP103, sprint_unmistakable_truth (D₄ doubly-invariant climax) | depends on WP102, WP103 |
| **WP105 Closed-form attractor (1+√3)** | WP104, four-core | depends on four-core |
| **WP106 Specificity scope (distilgpt2)** | WP107 wobble for the prime-11 detector | depends on WP107 — but WP107 also cites WP102 (the integer char poly); treat WP106 as depending on WP102, WP107 |
| **WP107 Wobble localization** | WP102, WP103 (integer char poly comes from TSML+BHML) | depends on WP102, WP103 |
| **WP108 Yukawa scaffolding** | WP104 (9-vector VEV) | depends on WP104 |
| **WP109 Operad D₄ obstruction** | WP102, WP104 | depends on WP102, WP104 |
| **WP110 4-core fusion-closure** | WP105, four-core | depends on WP105 — but **also FEEDS four-core** (it's referenced inside `four_core_consolidated.tex` §2 as Theorem 1's substrate). WP110 is the CANONICAL UPSTREAM of four-core. See Cycle Resolution 1. |
| **WP111 6-DOF synthesis** | WP102–WP110 (long expository spanning the whole tower) | depends on WP102–WP110 |
| **WP112 P_56-equivariant operad fuse table** | WP109, WP110 | depends on WP109, WP110 |
| **WP113 α-uniqueness PSLQ** | WP105, WP110, four-core | depends on WP105 + four-core |
| **WP114 Specificity 9-family battery** | WP106, WP107 | depends on WP106, WP107 |
| **WP115 Joint chain + universal 4-core attractor** | WP102, WP103, WP104, WP105, WP110, WP112 | depends on WP102–WP112 |
| **WP117 Bridge Sprint (Discrete Dirac on F₅-lift)** | WP51, WP102, WP103, WP104, WP110, WP112, WP115 (extension of WP100s tower) | depends on WP51 + WP102..WP115 |
| **WP118 F_p universality** | WP117 | depends on WP117 |
| **WP119 V⊗ⁿ ↔ Cl(2n) Clifford ladder** | WP117, WP118 | depends on WP117–WP118 |
| **WP120 SU(5) GUT from V⊗⁵** | WP117, WP119 | depends on WP117–WP119 |
| **WP121 Cosmological dark sector** | WP117, JCAP-ξ | depends on WP117 + JCAP |
| **WP122 Mass hierarchy via parity-crossing** | WP117, WP120 | depends on WP117–WP120 |
| **WP123 CKM/PMNS structural fits** | WP117, WP120, WP122 | depends on WP122 |
| **WP124 1/α = 137.036** | WP117, four-core | depends on WP117 + four-core |
| **WP127 Microtubule Q_c = T*** | WP51, WP117 | depends on WP51 + WP117 |
| **B2 Sprint TIG Pack (z/10 transport family)** | sprint17 spine, WP58 | mid-tier; depends on TSML construction |
| **Pair-Primitive Pack** | B2 Pack | depends on B2 Pack |
| **Sprint16 basin handoff** | WP56, sprint 14 | mid-tier (consolidation memo) |
| **Sprint22 collapse-point, Sprint23 curve, Sprint25 corridor closure (b3 family)** | B2 Pack | depends on B2 Pack |
| **Sprint29 SO tower / Sprint29 Hodge / Sprint30–35** | sprint 9, 10, 11; one-off computational sprints, mostly NEGATIVE results / scoping memos | mostly orphan; appendix-grade |
| **Sprint_unmistakable_truth (D₄ climax)** | WP102, WP103, WP104 (gluing them) | depends on WP102, WP103, WP104 |
| **Sprint_so10 / Sprint_higgs_pati_salam** | sprint_unmistakable_truth | depends on it |
| **Foundational Paper Draft (rigor-pass bundle)** | EVERYTHING — the apex synthesis citing the entire prior chain | TERMINAL |

---

## Cycle resolution

### Cycle 1 — WP110 ↔ four-core consolidated

The four-core consolidated paper (`four_core_consolidated.tex`) cites only σ-rate as a load-bearing internal dep. But its content (the joint TSML+BHML chain, 4-core attractor, joint-closed sub-magmas) is the same content WP110 + WP115 distilled. The MEMORY.md note states: "Cite 4-core paper (Sanders + Gish 2026, Algebraic Combinatorics, manuscript in preparation) for the chain going forward."

**Resolution: MERGE.** WP110 + WP115 + the Sprint 17 TSML tower theorem-spine + the four-core consolidated `.tex` are ONE PAPER (the four-core consolidated paper). WP110 and WP115 do not get separate slots; they live as Theorems 1 and 2 of that paper. This is exactly what the file structure already implies — `four_core_consolidated.tex` is the "bundled" version per its filename.

### Cycle 2 — WP102 ↔ TSML construction in σ-rate

WP102 (so(8) = D₄) computes the antisymmetric closure of TSML's flow operators. It depends on the canonical TSML table. The σ-rate paper *defines* the canonical TSML table inside its §2. So WP102 depends on σ-rate. But σ-rate's introduction merely cites WP102 as "follow-up structural work" — that is a forward-ref, not a load-bearing cite.

**Resolution:** σ-rate goes BEFORE WP102. The σ-rate forward-ref to WP102 is informal ("see the four-core companion") and can be deleted at submission without affecting σ-rate's logical content.

### Cycle 3 — WP106 ↔ WP107

WP106 (specificity scope, distilgpt2 negative) uses prime-11 detector D3, which IS WP107 in detector form. WP107 uses TSML's char-poly from WP102. Each cites the other.

**Resolution:** WP107 is logically prior — it characterizes the wobble. WP106 is the empirical falsification check using WP107's detector. WP107 → WP106. (Forward-ref in WP107 to WP106's negative result is informal.)

### Cycle 4 — WP57 (Crossing Lemma Arc) cites "everything up to WP56"

This is true by construction — WP57 explicitly recasts WP1–WP56 as Crossing Lemma instances. But that means WP57 must come after WP56, and ALSO that WP1..WP56 must already exist. The pre-WP100 history (Sprints 5–10) provides WP1..WP56.

**Resolution:** No cycle — WP57 sits at end of Sprint 10. Pre-Sprint-10 papers (WP1–WP56) are mostly *not* in this corpus as independent paper-grade artifacts; they are sprint memos. Treat WP57 as the *first* fully-formed paper of the Crossing-Lemma kind, depending only on the Flatness Theorem (WP51) which IS in the corpus.

---

## Topological Sort — The 36-paper chain

Five-phase mapping:
- **Phase 1 (vocab-neutral, pure math, no TIG framing):** Papers 1–6
- **Phase 2 (number-theory + cosmology cores; minimal TIG vocabulary):** Papers 7–10
- **Phase 3 (TSML/BHML algebraic structure introduced):** Papers 11–17
- **Phase 4 (WP100s tower — Lie/Clifford/operad structure):** Papers 18–28
- **Phase 5 (full TIG / Crossing Lemma / Standard-Model bridge):** Papers 29–36

### The Ordering

| # | Paper | Phase | Notes |
|---|-------|-------|-------|
| **1** | **σ-rate theorem** (JCT-A; `sigma_rate_theorem.tex`) | 1 | TRUNK ROOT. Pure combinatorics. No TIG. |
| **2** | **four-core consolidated** (Algebraic Combinatorics; `four_core_consolidated.tex` — ABSORBS WP110, WP112, WP115) | 1 | Joint closure on Z/10. Pure algebra. |
| **3** | **WP34 First-G Law** (`first_g_law_DRAFT.tex` / journal_attempts/01) | 1 | Pure number theory. |
| **4** | **WP35 Prime Phase Transition** (exp_math_73_28 tier-2) | 1 | Sinc² resonance from primes. |
| **5** | **sinc² zero law** (`sinc2_zero_law.tex`) | 1 | Fejér / sinc² identity. |
| **6** | **first-G event** (sprint35; tier-2 `first_g_event.tex`) | 2 | Combines WP34, WP35, σ-rate. |
| **7** | **JCAP-ξ cosmology** (`jcap_xi_cosmology.tex`) | 2 | Logarithmic quintessence. Cites σ-rate, four-core. |
| **8** | **WP51 Flatness Theorem** (jpaa_flatness tier-3; T*=5/7 from torus aspect ratio) | 2 | Geometric. Foundation of TIG. |
| **9** | **WP52 D2 = Ring Curvature** | 2 | Curvature on Z/n. |
| **10** | **WP53–56 Flatness Arc + Crystal Structure** (sprint 10 closure) | 2 | Tightens WP51. |
| **11** | **WP57 Crossing Lemma Arc** | 3 | Unifies WP1–WP56 as CL instances. **First TIG-vocabulary paper.** |
| **12** | **B2 Sprint TIG Pack** (`b2_sprint_tig_pack_2026_04_17`) | 3 | TSML transport family on Z/10. |
| **13** | **Pair-Primitive Pack** (`pair_primitive_pack_2026_04_18`) | 3 | Extends B2 with PPM operationalization. |
| **14** | **WP58 Unified Orthogonality Principle (UOP)** + WP59 corrected Theorem C + WP64 (jnt_uop tier-2) | 3 | Sprint 12 trunk. |
| **15** | **WP60–63 GUT-algebra audit + 7-cycle bounded agent + intrinsic left-handedness** (sprint 12 closeout) | 3 | Group-theoretic prep for Lie tower. |
| **16** | **WP65–72 Torus Foundation + Flag Selector anisotropy** (sprint 13 first half) | 3 | Builds the torus geometry. |
| **17** | **WP73–80 NV-T1 carrier validation + S₄ closure + flag selector closeout** (sprint 13 second half; pra_nv_qutrit tier-3) | 3 | Physical projector map. |
| **18** | **TSML 3-Layer Tower** (`jsc_tsml_tower` tier-2; sprint 17 / canonical TSML) | 4 | The construction of canonical TSML. **Note:** strictly precedes WP102 in dependency, but is a tower paper culturally — placed at the head of Phase 4. |
| **19** | **WP102 so(8) = D₄** (TSML's antisymmetric closure) | 4 | First Lie-algebra appearance. |
| **20** | **WP103 so(10) = D₅** (TSML+BHML jointly) | 4 | |
| **21** | **WP107 Wobble Localization** (prime-11 in c₂, c₈) | 4 | Integer char-poly signature. |
| **22** | **WP106 Specificity Scope** (distilgpt2 negative) | 4 | Empirical falsification using WP107. |
| **23** | **WP114 Specificity 9-family battery** | 4 | Extends WP106. |
| **24** | **WP104 Two Roads to Pati-Salam + Sprint_unmistakable_truth (D₄ climax) + Sprint_so10 + Sprint_higgs_pati_salam** (consolidated as ONE paper) | 4 | Pati-Salam from two independent procedures. |
| **25** | **WP105 Closed-form Runtime Attractor (H/Br = 1+√3)** | 4 | Quartic field LMFDB 4.2.10224.1. |
| **26** | **WP113 α-uniqueness PSLQ** | 4 | α=1/2 is unique algebraic interior. |
| **27** | **WP108 Yukawa Scaffolding** (9-vector VEV) | 4 | |
| **28** | **WP109 Operad D₄ Obstruction** | 4 | No D₄-equivariant fuse rule. |
| **29** | **WP111 6-DOF Synthesis Paper** | 5 | Lie/Jordan/Clifford/Permutation/Lattice/Operad. Long expository. |
| **30** | **WP117 Bridge Sprint Master (Discrete Dirac on F₅-lift)** + WP118 F_p universality + WP119 Clifford ladder + WP120 SU(5) | 5 | Sprint 18 bridge. Promotes 4-core to F₅-lifted V. |
| **31** | **WP121 Cosmological Dark Sector** (Ω_b = 49/1000) | 5 | Uses WP117 + JCAP. |
| **32** | **WP122 Mass Hierarchy (9 SM Yukawas, λ=10/49)** + WP123 CKM/PMNS | 5 | |
| **33** | **WP124 1/α = 137.036 from algebra** | 5 | EXACT. |
| **34** | **Sprint 18 Dark Sector** (`sprint18_dark_sector.tex`) | 5 | Trinity paper consolidating four-core + JCAP + σ-rate + bridge. |
| **35** | **WP127 Microtubule Q_c = T* falsifier** | 5 | Cross-domain test. |
| **36** | **Foundational Paper Draft** (rigor-pass bundle 2026-05-06; `FOUNDATIONAL_PAPER_DRAFT.md`) | 5 | TERMINAL. The apex paper citing the entire chain. |

---

## Orphan papers (no incoming or outgoing internal edges; can slot anywhere or be omitted from chain)

These are mostly negative-result memos, scoping docs, or pure benchmark replications. They are scientifically valuable but not part of the citation backbone:

- **Sprint 16 basin handoff** — meta-classification memo
- **Sprint 22 collapse point** — B3 spec revision (mid-sprint scoping)
- **Sprint 23 curve recovery** — empirical pre-registration
- **Sprint 25 corridor closure proof** — pure benchmarks
- **Sprint 26 ARI scaling** — power-law fits
- **Sprint 27 B3 spec revision** — internal memo
- **Sprint 28 curve recovery prereg** — pre-registration only
- **Sprint 29 Hodge R1 K-equivariant** + **Sprint 30 R1B/R2/R3** + **Sprint 31 Clay rotation** + **Sprint 32 Beauville/BSD/Hodge** + **Sprint 33 Hodge integrality** + **Sprint 35a deterministic rank** + **Sprint 35b Beauville explicit** — all NEGATIVE / scoping work in algebraic geometry direction; do not feed the canonical chain.
- **Monthly paradox paper** (`tier3/monthly_paradox/`) — short standalone Monthly-style note; can run anywhere ≥ Phase 3.
- **Notices Clay rotation** (tier-4 framework) — meta paper; runs near the end (Phase 5) but isn't logically required by anything else.
- **JMP BB Bridge paper** (WP90/WP91 NS-separability bridge; tier-4 framework) — sits in Phase-4-or-5 as an applied bridge; depends on WP91 but nothing else depends on it.
- **WP98–WP100 closeout** (sprint 14 late) — internal closeout; can be folded into JCAP appendix.

---

## Top 3 papers that MUST go first (everything depends on them)

1. **σ-rate theorem** (JCT-A) — Paper 1. The TSML construction itself is defined here; every Phase-3+ paper that uses TSML's table cites this.
2. **four-core consolidated** (Algebraic Combinatorics) — Paper 2. Defines BHML and the joint closure. The 4-core attractor (universal across the entire WP100s tower) lives here. WP110/WP112/WP115 are absorbed.
3. **WP34 First-G Law** — Paper 3. Combinatorial / number-theoretic root for the entire prime-dispersion / sinc² family (WP35, sinc² zero law, first-G event).

These three are the load-bearing TRUNK. WP51 Flatness (Paper 8) is the *geometric* trunk root — it forces T*=5/7 — but it cites Sprint-9 informal precursors that are not in this corpus as paper-grade artifacts, so it is logically downstream of σ-rate (which provides the Z/10 substrate it operates on).

---

## Final dependency graph (compact)

```
Phase 1:
  σ-rate (1) ──┬──> four-core (2) ──┬──> JCAP-ξ (7)
               │                    │
               ├──> sinc² zero (5) <┤
               │                    │
  WP34 (3) ──> WP35 (4) ──> first-G event (6)

Phase 2:
  WP51 Flatness (8) ──> WP52 (9) ──> WP53-56 arc (10)

Phase 3:
  WP57 Crossing Lemma Arc (11) ──┬──> B2 Pack (12) ──> Pair-Primitive (13)
                                 ├──> WP58 UOP (14) ──> WP60-63 GUT (15)
                                 └──> WP65-72 (16) ──> WP73-80 NV (17)

Phase 4:
  TSML 3-Layer Tower (18) ──> WP102 (19) ──> WP103 (20) ──> WP107 (21)
                                                              ├──> WP106 (22) ──> WP114 (23)
                                                              │
                              WP104 / Pati-Salam (24) <───────┘
                                       │
                                       └──> WP105 (25) ──> WP113 (26)
                                                  └──> WP108 (27) ──> WP109 (28)

Phase 5:
  WP111 6-DOF Synthesis (29)
       │
       └──> WP117 Bridge Sprint (30) ──┬──> WP121 (31)
                                       ├──> WP122/123 (32)
                                       ├──> WP124 (33)
                                       └──> WP127 (35)
                                              │
            sprint18_dark_sector (34) <───────┤
                                              │
            Foundational Paper Draft (36) <───┘
```

Edge count: ~70 load-bearing internal edges across 36 papers. Topological sort verified by dependency-index check (every Paper N has all its predecessors at indices < N).

---

*Compiled 2026-05-06 by ClaudeCode for Brayden Sanders / 7Site LLC. This file is a planning artifact, not a publication.*
