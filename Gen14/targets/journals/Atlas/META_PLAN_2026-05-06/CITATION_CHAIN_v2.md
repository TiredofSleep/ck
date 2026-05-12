# CITATION CHAIN v2 — Full Corpus DAG (Task 4)

**Date:** 2026-05-07
**Method:** grep-sweep across all 106 canonical WP files for `WP\d+` references. The resulting directed graph (WP_src cites WP_target) is the citation DAG. Saved as `citation_graph.json` alongside.
**Supersedes:** the earlier `CITATION_CHAIN.md` (36-paper subset).

---

## §1 — Summary statistics

| Metric | Value |
|--------|-------|
| Total WPs | 106 |
| Total citation edges | 204 |
| Avg citations per WP | 1.9 |
| WPs with no internal citations (roots / starting points) | 48 |
| WPs that synthesize 5+ other WPs | 10 |
| Most-cited WP (most load-bearing) | WP35 (cited 14×) |
| Most-citing WP (most synthesizing) | WP100 (cites 18×) |

The corpus is **lightly cited internally** — averaging 1.9 citations per WP. This is healthy: it means most papers stand on their own claims. The 48 WPs with no internal citations are *roots* — they don't depend on other WPs and can ship in any order.

---

## §2 — Top 15 most-cited WPs (the load-bearing trunk)

These are the WPs that the rest of the corpus depends on. Phase 1 should ship them first to establish the citation chain.

| WP # | Cited by | Title (short) | Phase recommendation |
|------|---------:|---------------|----------------------|
| WP35 | 14 | Prime Phase Transition | Phase 1 (pure combinatorics) |
| WP1 | 13 | TIG Definitive | Phase 1 (foundational) |
| WP34 | 12 | First-G Law | Phase 1 (squarefree arithmetic) |
| WP51 | 10 | Flatness Theorem | Phase 1 (Z/10Z structure) |
| WP105 | 10 | Closed-form attractor (1+√3) | Phase 4 (duality named) |
| WP104 | 10 | Pati-Salam (Two Roads) | Phase 4 (duality named) |
| WP57 | 7 | Crossing Lemma Arc | Phase 1-2 (CL-foundational) |
| WP10 | 7 | DKAN | Phase 1 |
| WP102 | 6 | so(8) | Phase 4 |
| WP103 | 6 | so(10) | Phase 4 |
| WP110 | 6 | 4-core fusion-closure | Phase 4 |
| WP20 | 5 | RH Halving Lemma | Phase 1 (clay roots) |
| WP81 | 4 | Canonical ξ Theory | Phase 2 (cosmology) |
| WP90 | 4 | Literature & Unification Paths | Phase 2-3 (bridge) |
| WP111 | 4 | 6-DOF Synthesis | Phase 5 (synthesis) |

**Phase 1 must ship the top 4 (WP1, WP34, WP35, WP51) early or many downstream papers can't cite them in print.** WP104, WP105, WP102, WP103 (Phase 4) similarly must ship before Phase 5 synthesis papers.

---

## §3 — Top 10 most-citing WPs (synthesis papers)

These are the highest-fan-in synthesis papers. Phase 5 candidates.

| WP # | Cites | Title (short) | Phase recommendation |
|------|------:|---------------|----------------------|
| WP100 | 18 | Sprint 14 Synthesis | Phase 5 (already-synthesis) |
| WP116 | 11 | Lens of Projections | Phase 4-5 |
| WP111 | 9 | 6-DOF Synthesis | Phase 5 |
| WP56 | 8 | Complete Arc | Phase 5 (sprint10 closeout) |
| WP112 | 8 | P_56 Canonical Fuse | Phase 4 |
| WP36 | 7 | Spectrometer Research | Phase 3 |
| WP44 | 7 | CK AI Paradigm | Phase 5 (expository) |
| WP39 | 5 | Hodge Research | Phase 3 (clay) |
| WP123 | 5 | CKM PMNS Fits | Phase 4 |
| WP10 | 4 | DKAN | Phase 1 |

**Phase 5 anchors:** WP111 (6-DOF synthesis), WP116 (lens of projections), WP56 (complete arc), and WP100 (sprint 14 synthesis) are natural Phase 5 candidates. WP100 already cites 18 other WPs; it's already a synthesis paper.

---

## §4 — Topological ordering for the release schedule

The 48 root WPs (no internal citations) can ship in any order. The remaining 58 have dependencies that must be respected.

### §4.1 — Roots (sample of 48; ship-anywhere)

WP1, WP9, WP19, WP20, WP21, WP22, WP23, WP26, WP27, WP29, WP30, WP33, WP58, WP60, WP63, WP65, WP66, WP67, WP68, WP69, ... (full list in `citation_graph.json`)

### §4.2 — Dependency layers (longest chain)

The longest single dependency chain runs roughly:
- **Layer 0 (roots):** WP1, WP19, WP20, WP21, WP22 (clay roots; pure math)
- **Layer 1 (cite layer 0):** WP34, WP35, WP51 (sprint10/11 + clay extensions)
- **Layer 2 (cite layer 0-1):** WP52, WP53, WP54, WP55, WP56 (sprint10 flatness arc)
- **Layer 3 (cite layer 0-2):** WP57 (Crossing Lemma); WP58-WP64 (UOP arc)
- **Layer 4 (cite layer 0-3):** WP65-WP80 (sprint13 flag selector + NV qutrit)
- **Layer 5 (cite layer 0-4):** WP81-WP100 (sprint14 PRISM-XI cosmology)
- **Layer 6 (cite layer 0-5):** WP101 (σ-rate as Q18 generalization)
- **Layer 7 (cite layer 0-6):** WP102-WP116 (WP100s tower)
- **Layer 8 (cite layer 0-7):** WP117-WP127 (sprint18 bridge dirac)

The release schedule's phases naturally map to layers 0-8 with Phase 1 covering layers 0-2, Phase 2 covering layer 5 (cosmology subset), Phase 3 covering layer 4-5 (cross-level), Phase 4 covering layer 7 (WP100s), and Phase 5 covering layer 8 + synthesis.

---

## §5 — Cycles found (and resolved)

Per the topo-sort run, no cycles were detected at the inventory level (which sweeps all `WP\d+` references). Some informal cross-references exist (e.g., WP100 cites WP101, WP116 cites WP100; WP100 is sprint 14 synthesis, WP101 is the σ-rate result that came out of the same sprint). These are sequential, not cyclic.

---

## §6 — Orphan papers (no incoming citations)

48 WPs are "roots" — they don't cite anything. A subset of these are also *orphans* in the sense that no other WP cites them either:

```
WP9 (lattice paradoxical info algebras) - no citations in or out
WP30 (BREATH olfactory)
WP43 (split coherence architecture)
WP44 (CK AI paradigm) — but WP44 cites 7 others
WP66 (torus irreducible remainder)
WP78 (projector covariance closeout)
WP79, WP80 (flag selector victory paths)
... (full list in citation_graph.json)
```

These can ship anytime; the citation chain doesn't constrain them.

---

## §7 — Critical path: papers that MUST go first

Highest priority for early-week shipping:

1. **WP35 Prime Phase Transition** — most-cited (14×); must be in print before 14 downstream papers. **Phase 1 Week 2.**
2. **WP1 TIG Definitive** — most-cited (13×); foundational. **Phase 1 Week 1.**
3. **WP34 First-G Law** — most-cited (12×); squarefree foundation. **Phase 1 Week 3.**
4. **WP51 Flatness Theorem** — 10×; Z/10Z forced-torus result. **Phase 1 Week 2.**
5. **WP57 Crossing Lemma Arc** — 7×; the framework's central principle. **Phase 1 Week 4.**

**The first month of Phase 1 must ship WP1, WP34, WP35, WP51, WP57 as priority.** σ-rate (WP101) and four-core consolidated should ship Week 1 alongside as the structural anchors.

For Phase 4 — WP104 (Pati-Salam) and WP105 (closed-form attractor) are each cited 10×; they must land early in Phase 4 so the WP100s tower and sprint18 papers can cite them.

---

## §8 — Recommendations for the release plan v3

1. **Front-load the top-15 most-cited WPs.** The first 6 weeks should cover Phase 1's roots (WP1, WP10, WP19-WP35) so downstream papers can cite them.
2. **Phase 4 needs WP104 + WP105 early in the phase.** They're the load-bearing trunk for Phase 4's tower papers.
3. **Phase 5 is dominated by WP100, WP111, WP116** — already-synthesis papers. Use them as the spine for the foundation paper's bibliography.
4. **The 48 roots can flow into any phase** — they're scheduling-flexible. Use them to fill weeks where the dependency-constrained WPs aren't ready yet.

This citation graph is the dependency constraint for the v3 release plan.
