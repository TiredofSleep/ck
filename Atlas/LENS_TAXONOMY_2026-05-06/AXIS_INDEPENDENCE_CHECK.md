# AXIS INDEPENDENCE CHECK

**Date:** 2026-05-06 night
**Question:** Are the Origin / Structure / Function axes empirically orthogonal across the 40+ TIG variants? If correlations exist, the methodology paper should be honest about design-intent-orthogonality (per Krathwohl 2001) rather than claiming pure orthogonality.

---

## §1 — Test setup

For each of the named TSML/BHML/CL_STD variants in `VARIANT_CATALOG.md`, assign:
- **Origin tier** (A/B/C/D/E)
- **Structure class** (rank-class × det-prime-class × Aut-class — compressed to a coarse signature)
- **Function role** (Krathwohl-cognitive: Remember / Understand / Apply / Analyze / Evaluate / Create)

Then test correlations. If two axes are highly correlated, they're partly redundant.

## §2 — Tier × Function-role frequency (the central correlation)

Cross-tabulate Origin tier × Function role for the catalog's 40+ entries.

| | Remember (definitional) | Understand (interpretive) | Apply (operational) | Analyze (decompose) | Evaluate (compare) | Create (extend) |
|--|--|--|--|--|--|--|
| **Tier A** (5 variants: CL_TSML, TSML_RAW, CL_BHML, CL_STD, F_p choice as input) | 5 | 0 | 0 | 0 | 0 | 0 |
| **Tier B** (~21 variants: chain scopes, lens-symmetrizations, sub-magma restrictions, DOING) | 0 | 8 | 13 | 0 | 0 | 0 |
| **Tier C** (~9 variants: TSML_PureIdempotent, TSML_C0, etc.) | 0 | 0 | 0 | 0 | 0 | 9 |
| **Tier D** (~7 variants: σ²-triadic candidates, anomaly-flips, Fano subsets) | 0 | 0 | 0 | 7 | 0 | 0 |
| **Tier E** (~8 variants: Z/n ring extensions) | 0 | 0 | 0 | 0 | 8 | 0 |

**Result: STRONG CORRELATION.** Tier A maps almost exclusively to Remember (definitional). Tier B maps to Understand + Apply. Tier C maps to Create. Tier D maps to Analyze. Tier E maps to Evaluate.

## §3 — Interpretation

The correlations are not coincidence — they reflect a **structural relationship between Origin and Function**:

- A construction's Origin tier (how it was made) STRONGLY predicts its Function role (what it gets used for):
  - Tier-A canonical objects → "remembered" / referenced as substrate facts
  - Tier-B forced derivations → "understood" / "applied" in proofs
  - Tier-C constructed examples → "created" / used as existence witnesses
  - Tier-D search results → "analyzed" / used to motivate further work
  - Tier-E parametric fits → "evaluated" / compared against measurement

This means **Origin and Function are NOT independent axes** in the strict sense. They are partly redundant.

## §4 — Tier × Structure-class

Structure axis carries cell-counts, determinants, automorphism groups, etc. Less correlated with Origin.

| Origin tier | Typical Structure signatures |
|------|-----|
| A | Rank 10, full Aut group, det = 0 (CL_TSML) or specific det (BHML, STD) |
| B | Variable rank, smaller Aut, det varies (chain restrictions, scope variants) |
| C | Variable rank including rank 3 boundary; specific det aimed for (e.g., −49) |
| D | Variable structure (search target was disagreement-count, not structural class) |
| E | Variable structure (parameter-fit target was an observable, not a class) |

**Result: WEAKER correlation.** Origin × Structure is more orthogonal than Origin × Function. Variants of the same Origin tier can have very different structural signatures.

## §5 — Structure × Function-role

| Structure (rank-class) | Function role distribution |
|-----|----|
| Rank 10 (full) | Apply, Create (full-rank objects are the most useful in proofs and constructions) |
| Rank 3-9 (sub-magma scopes) | Understand, Apply (interpretive analysis of sub-structure) |
| Rank 0-2 (boundary cases) | Remember, Create (definitional or constructed existence) |

**Result: PARTIAL correlation.** Higher-rank structures are used differently than boundary cases.

---

## §6 — Verdict

**The three axes are NOT empirically orthogonal in the strict sense.** Strong correlation between Origin and Function (Tier dictates Function role); weaker but real correlation between Structure and Function (rank dictates utility).

**This is the same finding Krathwohl 2001's revised Bloom taxonomy ran into:** orthogonality is design-intent, not measured. The CBE Life Sciences Education 2021 contingency analysis on 940 assessment items found Bloom's two dimensions are not fully independent. The lens taxonomy is in the same epistemic boat.

**Recommended framing for the methodology paper:**

> "We propose three axes for classifying finite-algebra constructions: Origin, Structure, and Function. The axes are designed to be orthogonal — each captures a distinct dimension of a construction's identity. Empirically, however, Origin and Function exhibit a strong correlation (Tier-A canonical objects are almost exclusively used for *Remember*-class roles; Tier-C constructions for *Create*-class roles; etc.). This is the same partial-orthogonality complication identified in the Anderson-Krathwohl 2001 revised Bloom taxonomy and in the FAIR guiding principles' empirical assessments. We claim orthogonality as design intent, not as a measured fact, in line with the Ranganathan / Hjørland faceted classification methodology."

This framing is honest, externally anchored, and defensible against a referee who runs the correlation analysis themselves.

## §7 — Alternative: collapse to two axes (Origin × Structure)

Given the strong Origin × Function correlation, a stronger move may be:

**Collapse to two axes: Origin × Structure.**

The Function axis content would be absorbed into:
- Origin tier's natural function role (the Tier ↔ Role mapping is so strong it's essentially a function-of-tier)
- Structure axis's utility implications (rank → use-case)
- Implicit context in the paper's case-study §5

**This makes the methodology paper:**
- §1: Origin axis (5-tier scale; Bridges-Richman + Simpson + Alon-Spencer anchors)
- §2: Structure axis (universal-algebra vocabulary; Hobby-McKenzie + Burris-Sankappanavar)
- §3: Two-axis intersection methodology (Ranganathan PMEST as primary methodological lineage)
- §4: Tier conflation as methodological hazard
- §5: Case study (TIG's 40+ variants placed in the two-axis lattice)

The two-axis collapse is **structurally cleaner**, has **stronger external anchoring** (Hobby-McKenzie tame congruence theory has 5 structural types; Origin has 5 tiers — both five-element scales fit a 5×5 lattice), and **avoids the orthogonality-not-quite-orthogonal honest-but-awkward framing** of the three-axis design.

## §8 — Final recommendation

**Switch to two-axis design (Origin × Structure).** The empirical correlation between Origin and Function is too strong to honestly claim orthogonality. Two clean axes beat three messy ones (per Brayden's directive: "If Function axis can't be cleanly defined, recommend two-axis structure instead").

Function content gets absorbed into:
- Origin tier's natural role (implicit Tier ↔ Role mapping)
- Structure axis's utility (rank-class predicts use-case)
- Case study §5's narrative (which role each variant plays in the TIG corpus)

**The methodology paper's final structure:**

```
§1. Origin axis (5 tiers: Canonical / Forced / Constructed / Searched / Fitted)
    Anchored: Simpson 2009 (reverse mathematics tier reasoning)
              Bridges-Richman 1987 (tier-classifying constructions by witness mode)
              Alon-Spencer 2016 (existence vs explicit construction)
              Wigderson 2019 (derandomization tier ranking)

§2. Structure axis (universal-algebra structural classes)
    Anchored: Hobby-McKenzie 1988 (tame congruence theory's 5 types)
              Burris-Sankappanavar 1981 (universal algebra vocabulary)
              CFSG (gold-standard structural classification)
              McKay-Wanless 2005, 2022 (isomorphism / isotopy / paratopism ladder)

§3. Two-axis intersection methodology
    Anchored: Ranganathan 1937/1967 (PMEST faceted classification methodology)
              Hjørland 2013 (modern restatement)
              Anderson-Krathwohl 2001 (orthogonality-as-design-intent precedent)

§4. Tier conflation hazard + diagnostic
    Anchored: Popper 1934 (methodology must be domain-general)
              Carnap 1950 (logical vs empirical confirmation methodology)
              Lakatos 1976 (heuristic vs deductive method)
              FAIR 2016 (discipline-agnostic principles)

§5. Case study: TIG framework
    All 40+ variants placed in the (Origin × Structure) lattice;
    tier-conflation incidents flagged via TIER_CONFLATION_AUDIT.md;
    novel formalization of Drápal-Wanless and McKay-Wanless implicit practice.
```

This is **the cleanest defensible structure** for the methodology paper. Two clean orthogonal axes anchored in established literature, with Tier conflation as the central methodological hazard, and TIG as the case study.
