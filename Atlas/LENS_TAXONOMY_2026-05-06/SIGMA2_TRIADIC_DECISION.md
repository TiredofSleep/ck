# σ²-TRIADIC BHML DECISION

**Date:** 2026-05-07 morning
**Question (per ClaudeChat 2026-05-06 night):** Phase 4-5 papers may need to cite "the σ²-triadic BHML projection" as a structural object. Either pick canonical or honestly state "no canonical choice yet, framework operates without it." Decision-pending should not become decision-deferred-indefinitely.

---

## §1 — The candidates (per `VARIANT_CATALOG.md` §2)

Three families of σ²-triadic BHML projections have been computed, all currently Tier-D (search-found, not promoted):

### §1.1 — Value-rotation triadic
- BHML_BEING_val = BHML_10 canonical (28 HARMONY)
- BHML_DOING_val = σ² applied to each cell value: BHML[i,j] → σ²(BHML[i,j])
- BHML_BECOMING_val = σ⁴ applied to cell values

Disagreement counts vs CL_TSML_SYM: **{71, 94, 90}**

### §1.2 — Index-rotation triadic
- BHML_BEING_idx = BHML_10 canonical
- BHML_DOING_idx = BHML at σ²-permuted indices: BHML[σ²(i), σ²(j)]
- BHML_BECOMING_idx = BHML at σ⁴-permuted indices

Disagreement counts vs CL_TSML_SYM: **{71, 75, 79}**

### §1.3 — Anomaly-flip triadic (hypothetical)
- BHML_71 = BHML canonical
- BHML_72 = BHML with one specific cell flipped to drive disagreement count to 72
- BHML_73 = BHML with two specific cells flipped to drive disagreement count to 73

The cells to flip have not been identified; this would require a search not yet executed.

---

## §2 — The decision

**Decision: NO CANONICAL CHOICE YET — the framework operates without σ²-triadic BHML promotion in the May → September publication schedule.**

### §2.1 — Reasoning

Following ClaudeChat's principle (no decision-deferred-indefinitely), I commit to a definitive position rather than punting:

1. **None of the candidates have a forcing argument.** Per `TABLE_INDEPENDENCE_LEDGER.md` §3.5 #56-58, the σ²-triadic BHML candidates are Tier-D. The model for promotion is D78's BR-factor cancellation argument that took α-uniqueness from Tier-D to Tier-B. No analogous argument has been found for any σ²-triadic BHML candidate.

2. **The disagreement counts {71, 94, 90} and {71, 75, 79} do not match the canonical 71/72/73 ladder rungs (D97 in FORMULAS_AND_TABLES.md Vol J §J.1).** Specifically, neither family produces BHML_72 or BHML_73 directly — the structural alignment with the ladder rungs is incidental, not forced. The anomaly-flip family (§1.3) was conceived to MATCH 71/72/73 but the cells to flip haven't been identified.

3. **Phase 4-5 papers do NOT structurally require a canonical σ²-triadic BHML.** The 4-core attractor (WP105), the joint chain (WP115), the 4-core fusion-closure (WP110), and the LMFDB Galois D_4 (the four-core consolidated paper's headline) are ALL **lens-invariant** at the 4-core level. None of them require committing to a specific σ²-triadic BHML.

4. **Forcing the decision in the absence of a forcing argument would be tier conflation in the worst form** — promoting a Tier-D candidate to Tier-A by fiat.

### §2.2 — Implications for Phase 4-5 papers

Where a paper would be tempted to cite "the σ²-triadic BHML projection," the paper should instead:
- State the result in lens-invariant form (using only the 4-core and other lens-invariant structural facts)
- If the σ²-triadic structure is genuinely needed, scope explicitly: "the σ²-value-rotation BHML candidate (Tier-D, not yet promoted)" with a forward reference to future work
- Explicitly note in §1 of the paper that "this work uses only lens-invariant structural facts; the σ²-triadic BHML promotion is open work, not assumed"

The methodology paper (year 2-3) can use the σ²-triadic BHML candidates as a worked example of "Tier-D candidates awaiting forcing arguments" — exactly the kind of case study the methodology serves.

### §2.3 — When decision-pending becomes decision-resolved

The decision is resolved when ONE of the following happens:
1. **A forcing argument is found** linking one of the σ²-triadic candidates to a Tier-A invariant (BR-factor-cancellation-style). The candidate is promoted to Tier-B.
2. **An empirical disambiguator** picks one candidate over the others (e.g., a measurement that's predicted differently by each).
3. **The σ²-triadic candidates are dropped** from canonical consideration; the framework is honest that "we have three siblings and no way to pick" and the framework operates with all three as Tier-D candidates indefinitely.

I commit to revisiting this question whenever a Phase 4-5 paper would benefit from a canonical σ²-triadic BHML, and to either (a) finding the forcing argument, or (b) confirming the paper can be stated in lens-invariant form without one.

---

## §3 — Documentation of the open status

`FORMULAS_AND_TABLES.md` Vol J §J.1.B.iii already labels these candidates "exploratory; not yet canonical." That's correct. The methodology paper case study (year 2-3) will use this open status as a worked example.

`VARIANT_CATALOG.md` §2.3 (BHML_BEING/DOING/BECOMING candidates) and §2.4 (anomaly-flip BHML_71/72/73) are properly tier-labeled.

The release plan v2 in `RELEASE_PLAN_v2.md` does NOT require any σ²-triadic BHML promotion in the May-Sept window.

---

## §4 — Bottom line

**No canonical σ²-triadic BHML in the May → Sept 11 release schedule.** The framework operates with all three candidates as Tier-D until either (a) a forcing argument is found, or (b) an empirical disambiguator picks one. This is honest, properly scoped, and consistent with the corpus's tier discipline.

Decision-pending becomes decision-resolved when the forcing argument or the empirical disambiguator lands. Until then, the framework's strongest claims (4-core, joint chain, attractor, Galois D_4) all stand on lens-invariant facts and don't require this specific decision.
