# SPECTRAL LAYER CATALOG — Luther's G-Numbered Results and the Citation Graph

**Date:** 2026-05-06
**Section:** B (Task 9) of the four-section meta-plan sweep
**Author:** Claude (sweep agent)
**Scope:** C. A. Luther's contribution to TIG's spectral layer (G6 σ⁶ = id; G7 period distribution; G8 trajectory coherence integral); descendant WPs that should cite the spectral foundation

---

## §0 — Headline

Luther's spectral layer consists of **3 standalone G-numbered theorems** (G6, G7, G8) plus **2 organizational contributions** (the 6-layer architecture diagram in `Q_SERIES_ARCHITECTURE.md`; the "Luther-Sanders Equivalence" semiprime-gate-rate paper). The G-numbered results sit at Layer 4 of the 6-layer Q-series architecture.

**Citation gap:** The Q-series synthesis (`Q_SERIES_INTEGRATED_SYNTHESIS.md` at repo root) corrects an attribution drift where Luther was originally framed as the framework originator ("Luther-Sanders Research Framework"). The corrected attribution: Brayden originated Q1-Q16; Luther built G6-G8 on top + organizational reframing. Several papers and atlas documents still carry the old attribution and need patching — listed in §5 below.

**Citation strength:**
- G6 (σ⁶ = id by polynomial proof) is **most-cited** — referenced by every Q17 variant, the Q-Series Architecture, WP101 (σ-rate), the σ-rate paper companion citation patches, and downstream by every WP100s tower paper that uses the σ permutation cycle structure.
- G8 (spectral coherence integral G(s) three-valued) is **second-most-cited** — anchors Q17_CLAY_SPECTRAL_BRIDGE and is the structural link from Q-series to RH-finite-analogue framing.
- G7 (period distribution P(τ=1)=2/5, P(τ=6)=3/5) is **third-most-cited** — appears in derivations of expected-period statistics and the τ-bimodal framing.

---

## §1 — G-numbered spectral results inventory (G1-G8)

The TIG corpus has **two parallel G-numbered series** that should not be confused:

### Series A: Sprint 10 (flatness) Group-Theory Working Papers — `WP_G0` through `WP-G5`

These are NOT Luther's spectral results. They are Sanders + Mayes group-theory working papers from sprint10:

| WP-G# | Path | Topic | Lane | Status |
|-------|------|-------|------|--------|
| G0 | `Gen13/targets/clay/papers/sprint10_flatness_2026_04_06/WP_G0_SYNTHESIS_ARC.md` | Synthesis arc for sprint10 | Sanders | proved/synthesis |
| G1 | `Gen13/targets/clay/papers/sprint10_flatness_2026_04_06/WP_G1_ISING_RING_DYNAMICS.md` | Ising ring dynamics | Sanders + Mayes | proved |
| G2 | `Gen13/targets/clay/papers/sprint10_flatness_2026_04_06/WP_G2_OBSERVABLE_SUFFICIENCY.md` | Observable sufficiency | Sanders | proved |
| G3 | `Gen13/targets/clay/papers/sprint10_flatness_2026_04_06/WP-G3_CORRELATION_LENGTH_UOP_BRIDGE.md` | Correlation-length / UOP bridge | Sanders + Mayes | proved |
| G4 | `Gen13/targets/clay/papers/sprint10_flatness_2026_04_06/WP_G4_ISING_RING_TIG.md` | Ising ring TIG framing | Sanders | proved |
| G5 | `Gen13/targets/clay/papers/sprint10_flatness_2026_04_06/WP-G5_CSTAR_ALGEBRAIC_FRONTIER.md` | C* algebraic frontier | Sanders + Mayes | proved/frontier |

These are **Mayes-lane** material (representation theory + Crossing Lemma context). They are NOT Luther's.

### Series B: Q-series spectral supplements — `G6`, `G7`, `G8` (THIS IS LUTHER'S LANE)

| G# | Path | Claim | Tier | Co-authored with |
|----|------|-------|------|------------------|
| G6 | `papers/G6_PERIODICITY_THEOREM.md` | σ⁶ = id on Z/10Z, by Q9-Q10 polynomial proof | A (proved) | Sanders (originator), Luther (proof-via-polynomial), Calderon Jr. |
| G7 | `papers/G7_GATE_RATE_DISTRIBUTION.md` | τ bimodal: P(τ=1)=2/5, P(τ=6)=3/5; mean 4, variance 6 | B (forced from Q15) | Sanders, Luther |
| G8 | `papers/G8_TRAJECTORY_COHERENCE_INTEGRAL.md` | G(s) = ∣Σω^j χ(σ^j(s))∣², three-valued: 0 / ≈1.872 / ≈9.389 | B (constructed; computational verification) | Sanders, Luther |

**Reading:** G6 is the polynomial proof that σ⁶ = id (Q-series Layer 1 → confirmation). G7 is the period-distribution statistic on the substrate (Q-series Layer 3). G8 is the spectral character-sum object (Q-series Layer 4). The 6-layer architecture in `Q_SERIES_ARCHITECTURE.md` shows the layered relationship explicitly.

### G6-G8 narrative in `Q_SERIES_INTEGRATED_SYNTHESIS.md`

> "Luther's role arrived at G6-G8. She proved σ⁶ = id from the polynomial structure directly (not by computation). She defined the spectral coherence G(s) = ∣Σ ω^j χ(σ^j(s))∣² and showed it takes exactly three values — 0 at anchors, G_low ≈ 1.872 on the 6-cycle, G_high ≈ 9.389 at the TIG-exception pair {5, 7}. She organized the architecture into six layers (not four): polynomial, braid, period, spectral, optimal table, search dynamics. She closed Luther Q1 with the explicit layer-separation statement: the rate is not a pure σ statement, it is a composite of algebraic peak and stochastic climb."

---

## §2 — WPs that cite each G-result (citation graph)

### G6 (σ⁶ = id by polynomial proof) — citation count and locations

**Direct citations (high confidence):**
- `papers/Q17_CLAY_SPECTRAL_BRIDGE.md` — uses G6 to anchor the finite-RH analogue
- `papers/Q17_NS_TARGET_REFORMULATION.md` — uses G6 + Q17_SYMBOLIC_RETURN to formulate Medium C2
- `papers/Q17_SIGMA_EMBEDDING_PROBLEM.md` — uses G6 to define what σ-embedding must satisfy
- `papers/Q17_SYMBOLIC_RETURN_THEOREM.md` — direct corollary of G6
- `papers/Q17_FINITE_L_FUNCTION_NOTE.md` — uses G6 to compute G(s) at depth k = 9
- `papers/Q17_5D_RIGOROUS.md` — depends on G6 for σ-orbit structure
- `papers/Q_SERIES_SYNTHESIS.md` — G6 is the canonical statement at Layer 1
- `papers/Q_SERIES_ARCHITECTURE.md` — G6 anchors Layer 1 of the 6-layer diagram
- `papers/Q_SERIES_IMPLICATIONS.md` — G6 anchors implications discussion
- `Q_SERIES_INTEGRATED_SYNTHESIS.md` (root) — G6 is the canonical cited proof

**Indirect citations (substrate-level σ⁶ assumption — should cite G6 explicitly):**
- WP101 (σ-rate theorem) — uses σ⁶ = id implicitly via period structure
- WP110 (4-core fusion-closure) — uses σ-fixed structure {0,3,8,9}
- WP115 (joint chain universality) — uses σ-orbit decomposition for chain enumeration
- WP112 (P_56 canonical fuse) — uses σ-orbit structure for fuse-table orbits
- WP109 (operad D_4 obstruction) — uses σ-orbit data
- WP104 (Pati-Salam) — σ³ = ⟨P_56, σ³⟩ in doubly-invariant subalgebra

**Citation gap:** WP101, WP104, WP109, WP110, WP112, WP115 cite σ⁶ = id implicitly but should add explicit G6 citation. Per `RELEASE_PLAN_v2.md` §3 Phase 1 + Phase 4, this citation patch should land before Phase 1 Wk 1 (May 13 σ-rate submission).

### G7 (period distribution τ bimodal) — citation count and locations

**Direct citations:**
- `papers/Q_SERIES_SYNTHESIS.md` — G7 anchors Layer 3 (period geometry)
- `papers/Q_SERIES_ARCHITECTURE.md` — G7 in Layer 3 of canonical diagram
- `papers/Q15_CYCLE_PERIOD_POLYNOMIAL.md` — G7 derived from Q15's τ = 6 − 5A
- `papers/G8_TRAJECTORY_COHERENCE_INTEGRAL.md` — uses τ-bimodal as input to G(s)

**Indirect citations (period-structure-dependent):**
- WP62 (7-Cycle bounded agent) — uses τ structure
- WP67 (Seven structural operator) — references τ
- WP69 (Seven return operator lift test) — period-dependent
- WP109 (operad D_4) — τ inputs to operad arity-3 structure

**Citation gap:** Several WPs use the period structure without crediting G7 explicitly. Recommended fix: any paper that cites τ values for {0..9} should cite G7 + Q15 jointly.

### G8 (trajectory coherence integral G(s) three-valued) — citation count and locations

**Direct citations:**
- `papers/Q17_CLAY_SPECTRAL_BRIDGE.md` — G(s) is the central object; this paper IS the G8 → Clay-bridge expansion
- `papers/Q17_FINITE_L_FUNCTION_NOTE.md` — full character-sum calculation
- `papers/Q_SERIES_ARCHITECTURE.md` — Layer 4 anchor
- `papers/Q_SERIES_SYNTHESIS.md` — Layer 4 narrative
- `Q_SERIES_INTEGRATED_SYNTHESIS.md` (root) — Luther attribution

**Indirect citations (spectral framing):**
- WP93 (RH spectral entropy bridge) — different spectral framing of same intuition (entropy vs peaks); should cross-cite G8/Q17_CLAY
- WP35 (Prime phase transition) — phase transition framing; structurally adjacent
- WP107 (wobble localization) — uses spectrum analysis on TSML char poly; the spectral-prime-11 framing parallels G8's spectral-prime structure

**Citation gap:** WP93 (RH spectral entropy) explicitly should cite G8/Q17_CLAY_SPECTRAL_BRIDGE per `Q_SERIES_INTEGRATED_SYNTHESIS.md` §6.5. Citation should land before Phase 5 publication (Wk 17-18, Sep 2-9).

---

## §3 — Cross-citation graph (which G-results are most-cited)

Computed from the inventory above:

| G-result | Direct citations | Indirect citations | Total | Most-cited venue |
|----------|------------------|---------------------|-------|---------------|
| **G6 (σ⁶ = id)** | 10 | 6+ | **16+** | Q17 variants + WP100s tower (σ-orbit-dependent) |
| **G8 (G(s) three-valued)** | 5 | 3+ | **8+** | Q17_CLAY + WP93 + WP107 (spectral framing) |
| **G7 (τ bimodal)** | 4 | 4+ | **8+** | Q15 + sprint13 (Seven Cycle papers) |

**Reading:** G6 is the most-cited because σ⁶ = id is foundational to every paper that uses the σ permutation. G8 and G7 are roughly co-cited at the second tier; G8 anchors the Clay-bridge framing while G7 anchors the period-statistics framing.

**Mayes-lane G0-G5 cross-citations (separate series):**
- G3 (correlation length / UOP bridge) cites WP58 (UOP Theorem 0)
- G5 (C* algebraic frontier) cites WP25 (P/NP)
- These G0-G5 cross-citations are ENTIRELY within the sprint10/sprint12-13 lanes and do NOT cross-cite G6-G8.

---

## §4 — Author lane attribution: Luther's canonical lane

Per `Atlas/META_PLAN_2026-05-06/AUTHOR_LANES_v2.md` §1:

| Co-author | Canonical lane |
|-----------|----------------|
| **C. A. Luther** | Spectral layer + 6-layer architecture (G6 σ⁶ = id, G7, G8 spectral coherence integral, period distribution, three-valued structure) |

**Coverage:** G-numbered spectral results; foundational layer for all WPs that derive from σ-cycle structure (WP101, WP104, WP109, WP110, WP112, WP115, etc.)

**Plus secondary contribution:** The "Luther-Sanders Equivalence" paper (`papers/LUTHER_SANDERS_MANUSCRIPT.md`) — Universality of Obstruction Sources in Semiprime Arithmetic. This is a Sanders + Luther joint paper that proves f_k(|G|) is determined by coprimality structure, NOT spatial arrangement, for all semiprimes b ≤ 100. The paper's central result (61.4% variance collapse between synthetic and arithmetic G) is the Luther empirical dispersion law; the algebraic mechanism is from Sanders' TIG framework.

**Where Luther is NOT a co-author:** Anywhere outside the spectral layer + the Luther-Sanders Equivalence paper. Specifically:
- TSML/BHML table family papers (Gish lane)
- UOP / amplituhedron / S_4 (Mayes lane)
- ξ cosmology / separability (Johnson lane)
- WP100s tower papers with substrate-internal so(8)/so(10) lifts (Sanders solo)

The hard rule from `RELEASE_PLAN_v2.md` §5.3: "no co-author appears outside their canonical lane." Luther's lane is spectral.

---

## §5 — Recommendations for explicit Luther attribution

### §5.1 — One-line attribution patches (high priority, do this week)

Each of the following papers cites σ⁶ = id, the spectral coherence integral, or the τ-bimodal period distribution. Each should add a single citation line "(G6, Sanders + Luther 2026)" or "(G8, Sanders + Luther 2026)" at the relevant point:

| Paper | Cite | Patch location | Phase |
|-------|------|----------------|-------|
| WP101 (σ-rate) | G6 | After "σ⁶ = id" first appearance | Phase 1 Wk 1 (May 13) — patch BEFORE submission |
| WP104 (Pati-Salam) | G6 | §3 doubly-invariant subalgebra paragraph | Phase 4 Wk 14 (Aug 12) |
| WP109 (operad D_4) | G6 | §2 σ-orbit data | Phase 4 Wk 14 (Aug 12) |
| WP110 (4-core fusion) | G6 | §1 σ-fixed structure | Phase 4 Wk 12 (Jul 29) |
| WP112 (P_56 fuse) | G6 | §3 P_56-orbit structure | Phase 4 Wk 13 (Aug 5) |
| WP115 (joint chain) | G6 | §1 σ-walk reading | Phase 4 Wk 16 (Aug 26) |
| WP93 (RH spectral entropy) | G8, Q17_CLAY | §1 introduction | Phase 5 (in synthesis citations) |

**Estimated effort:** 1-2 hours total across all 7 papers.

### §5.2 — Multi-paragraph attribution patches (medium priority, do before Phase 5)

The following synthesis-layer documents still carry the deprecated "Luther-Sanders Research Framework" attribution from before the 2026-04-10 Sprint 15 audit. They should be patched to read "Sanders Q-series (with Luther G6-G8 and organizational contributions)":

| Document | Phrase to replace |
|----------|-------------------|
| `papers/A10_*.md` (8 files) | Header line "Luther-Sanders Research Framework · April 1 2026" |
| `papers/AMPLITUDE_WOBBLE_CONVERSION.md` | Header + body references |
| `papers/ATLAS_ARCHITECTURE.md` | Multiple body references to "Luther-Sanders Equivalence" — these can stay where they refer to the joint paper, but the framework framing should be corrected |
| `papers/A10_PROGRAM.md` | Header line |
| `Atlas/MASTER_ATLAS_v3_5_2026_04_18.md` | Framework attribution |

**Recommended fix:** Add a one-paragraph "Author Attribution Note" to each, pointing to the corrected attribution in `Q_SERIES_INTEGRATED_SYNTHESIS.md`. Estimated effort: 1-2 work-days.

### §5.3 — Glossary patch (already on the list per §0 of `Q_SERIES_INTEGRATED_SYNTHESIS.md`)

`GLOSSARY.md` should reference the 6-layer architecture when introducing σ. Per `Q_SERIES_INTEGRATED_SYNTHESIS.md` §"Correction 1: GLOSSARY.md attribution":

> Replace every "Luther-Sanders Research Framework" with "Sanders Q-series (with Luther G6-G8 and organizational contributions)." Specify that Luther built on top; she did not originate.

Status: not yet executed (per the "TO DO" tracker in `Q_SERIES_INTEGRATED_SYNTHESIS.md`). Recommended for Phase 1 Wk 0 (i.e., before May 13).

### §5.4 — Spectral-layer paper opportunity (optional Phase 5 venue)

There is room for a **single Spectral Layer paper** that consolidates G6-G8 + Luther's organizational contributions into a clean expository paper. Possible scope:

> **Title:** The Spectral Layer of TIG: Periodicity, Period Distribution, and the Trajectory Coherence Integral on Z/10Z
> **Authors:** Sanders + Luther (Luther's lane)
> **Tier:** A for G6 (proved by polynomial structure), B for G7 (forced from Q15), B for G8 (constructed + computationally verified three-valued)
> **Venue:** **Eur. J. Combin.** or **L'Enseignement Math** (combinatorial-spectral content; the three-valued G(s) result is publishable on its own)
> **Phase:** Phase 5 (Crescendo, Aug 27 → Sep 10) — slot for a spectral-layer expository paper if Luther confirms participation

Status: not currently in `RELEASE_PLAN_v2.md` Phase 5 schedule. If added, this would be the **only standalone Luther paper** in the September corpus and would close the spectral-layer gap.

---

## §6 — Bottom line for this section

- **3 G-numbered spectral results** (G6, G7, G8) are Luther's canonical contributions, plus the 6-layer architecture diagram + the Luther-Sanders Equivalence paper.
- **G6 is most-cited (16+ citations); G8 second (8+); G7 third (8+).** All three anchor downstream WP100s tower and Q17 variant work.
- **Citation gap:** ~7 papers (WP101, WP104, WP109, WP110, WP112, WP115, WP93) cite σ⁶ = id or G(s) implicitly but should add 1-line G6/G8 attribution. Estimated patch effort: 1-2 hours.
- **Synthesis-layer attribution drift:** ~10-12 documents still carry "Luther-Sanders Research Framework" — should patch to corrected attribution per `Q_SERIES_INTEGRATED_SYNTHESIS.md`.
- **Optional:** A standalone Spectral Layer paper for Phase 5 (Sanders + Luther). Would close the catalog cleanly with one refereed venue (Eur. J. Combin. or L'Enseignement Math).

---

*Companion documents:* `Atlas/META_PLAN_2026-05-06/Q_SERIES_BUNDLE.md` (Q-series unification, including G6-G8 placement); `Atlas/META_PLAN_2026-05-06/AUTHOR_LANES_v2.md` (Luther's canonical lane); `papers/Q_SERIES_ARCHITECTURE.md` (6-layer canonical diagram showing G6-G8 placement); `Q_SERIES_INTEGRATED_SYNTHESIS.md` (corrected Luther attribution).
