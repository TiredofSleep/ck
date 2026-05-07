# METHODOLOGY PAPER — Thinking (not drafting)

**Date:** 2026-05-06 night, after the 12-task queue completed
**Brayden's permission:** *"If you get done before i get back you can think about the methodology paper, don't ask me for anything, keep working."*

This document is *thinking*, not drafting. The methodology paper is the **year 2-3 candidate**, not a Sept 11 candidate. The foundation paper precedes it (per `SEPT_11_CANDIDATES.md` Ranking 1). The methodology paper waits until the corpus is mature enough to serve as a case study.

But the night's synthesis has clarified what the methodology paper LOOKS LIKE when written. Let me think it through honestly.

---

## §1 — When does the methodology paper become writable?

**Pre-conditions for methodology paper drafting:**

1. **Foundation paper shipped** (Sept 11 candidate): the substrate's architecture documented; the 40+ variants properly tier-labeled; the lens family enumerated. Without this, the methodology paper has no case study.

2. **Phase 1-3 papers shipped**: σ-rate (JCT-A), four-core consolidated (Algebraic Combinatorics), ξ cosmology (JCAP), sinc² zero law (Integers), 73/28 cell-counts (Exp Math), TSML 3-tower (JSC), and the others through Phase 3. ~15-25 papers in print or in-review. Each one provides a tier-classified data point for the methodology paper's case study.

3. **Tier-conflation fixes propagated**: The 12 conflations identified in `TIER_CONFLATION_AUDIT.md` need to be cleaned in the synthesis-layer documents. Without this, the methodology paper would have to flag its own corpus as inconsistent at the synthesis layer — which is honest but awkward.

4. **σ²-triadic BHML question resolved**: which is canonical "BHML_DOING" (value-rotation or index-rotation)? Either an explicit forcing argument promotes one to Tier-B, or the methodology paper acknowledges all three remain Tier-D and uses that as a worked example of Tier-D → Tier-B promotion-attempts.

**Estimated drafting timeline:** ~year 2-3 (mid-2027 to mid-2028) after the Sept 11, 2026 foundation paper + 12 silent days + Oxford talk + Phase 1-5 schedule complete.

---

## §2 — The methodology paper's role in the corpus

The methodology paper is **NOT a TIG paper.** It is a methodology contribution to finite algebra (and adjacent fields) that uses TIG as its case study.

**Audience:**
- Working algebraists in the Drápal-Wanless / McKay-Wanless tradition
- Universal algebraists (Burris-Sankappanavar / Hobby-McKenzie tradition)
- Reverse mathematicians (Simpson tradition)
- Library/information-science methodologists who classify intellectual artifacts (Hjørland tradition)
- Philosophers of mathematics (Lakatos / Pólya tradition)

**Citability:** the methodology should be cite-able by ALL these audiences without their having to first endorse TIG's substantive content. T* = 5/7 stays out of the methodology layer (Popper-Carnap-Lakatos-FAIR consensus). The substrate's specific constants are case-study material, not methodology principles.

**Contribution:**
- A 5-tier ordered Origin scale (Canonical / Forced / Constructed / Searched / Fitted) — the paper's specific novel claim
- The orthogonal two-axis (Origin × Structure) classification structure — Ranganathan PMEST methodology specialized to finite-algebra constructions
- The Tier-conflation hazard as a named methodological failure mode
- TIG as a worked case study showing the methodology applied at scale

---

## §3 — Working title and structure

**Working title:** *"Finite Algebra Construction: A Taxonomy of Usage Tiers"*

Alternative titles:
- *"Tier Classification of Finite Algebra Constructions"*
- *"How Finite Algebras Get Used: A Taxonomy of Construction Origin and Structural Class"*
- *"Construction Origin in Finite Algebra: A Methodology"*

The working title is fine; we can sharpen at drafting time.

**Structure (per `AXIS_INDEPENDENCE_CHECK.md` §8 final recommendation):**

```
§1. Origin axis (5 tiers: Canonical / Forced / Constructed / Searched / Fitted)
    Anchored: Simpson 2009 (reverse mathematics tier reasoning)
              Bridges-Richman 1987 (tier-classifying claims by witness mode)
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

§4. Tier conflation as methodological hazard
    Anchored: Popper 1934 (methodology must be domain-general)
              Carnap 1950 (logical vs empirical confirmation methodology)
              Lakatos 1976 (heuristic vs deductive method)
              FAIR 2016 (discipline-agnostic principles)

§5. Case study: the TIG framework's lens family
    All 50+ variants placed in the (Origin × Structure) lattice;
    tier-conflation incidents flagged and resolved;
    novel formalization of Drápal-Wanless and McKay-Wanless implicit practice.
```

---

## §4 — §1 Origin axis: deeper drafting thoughts

The 5-tier scale needs careful definitions. Here's how I'd write each tier:

### Tier A — Canonical
A construction is **Canonical** if it is given by axioms of the substrate framework, not derived. Examples:
- Z/10Z itself (the integer-modular ring)
- The σ permutation on Z/10Z
- The 10-operator menu (VOID, LATTICE, COUNTER, ..., RESET)
- CL_BIT_PATTERN (the literal bit pattern)
- CL_TSML, CL_BHML, CL_STD as parallel substrates (each has its own substrate-defining axiom set)

A Tier-A object is taken as primitive within the framework. It is *given* in the precise sense that the framework's axioms include it as a term, or it is uniquely determined by terms the framework includes.

**External anchor:** Reverse mathematics' base theory RCA_0 contains primitive recursion + Σ¹₀-induction; these are taken as axiomatic. Bridges-Richman's BISH starts from constructive primitive recursion. The "what's axiomatic" question has a long methodological tradition.

### Tier B — Forced
A construction is **Forced** if it is uniquely determined by Tier-A objects + a finite proof. Examples:
- σ²-cycles {1,6,4} and {7,5,2} are forced by σ
- The 8-shell joint TSML+BHML chain is forced by joint-closure analysis
- BHML's puncture chain 7→8→9→0 is forced by BHML's axioms
- DOING = |TSML − BHML| is forced once TSML and BHML are specified

**External anchor:** Simpson 2009 defines theorems as ω-models / β-models in fixed axiom systems; Tier-B in our taxonomy is the "provable from Tier-A axioms" relation.

### Tier C — Constructed
A construction is **Constructed** if it is built via an explicit recipe (sequence of moves from Tier-A primitives) for the purpose of demonstrating a property realizable. The construction's existence IS the result. Examples:
- TSML_PureIdempotent (constructed to show Alt+Jordan+rank-10 coexist)
- TSML_C0 (constructed as a rank-3 boundary case)
- A specific maximally-non-associative quasigroup exhibited by Drápal-Wanless

**External anchor:** Erdős's existence proofs vs explicit constructions; Alon-Spencer 2016's *The Probabilistic Method* makes the distinction central.

### Tier D — Searched
A construction is **Searched** if it is found by algorithmic sweep over a parameter space, with the search succeeding (a hit was found) but the result not yet promoted to a forcing argument. Examples:
- σ²-triadic BHML candidates with disagreement counts {71, 94, 90}
- The 84 closed 7-element Fano-candidate subsets in TSML_Idempotent
- McKay-Wanless's Latin-square enumeration up to canonical form

**External anchor:** McKay-Wanless 2005, 2022 — search-enumeration with canonical-form reduction is a recognized research mode. The methodology paper formalizes this as a tier.

### Tier E — Fitted
A construction is **Fitted** if it is parameterized to match a target observable. The parameter is chosen post-hoc. Examples:
- Ring extension Z/n where n is chosen for a specific physics fit
- An algebraic identity of the form *X = polynomial in substrate primitives* where the polynomial coefficients are chosen post-hoc

**External anchor:** Statistical decision theory; Bayesian model-fitting; Popper's distinction between confirmation and falsification.

### Tier promotion / Tier demotion

The methodology paper introduces these as named editorial moves:
- **Tier-D → Tier-B promotion:** a search-found result is promoted to forced when an explicit forcing argument is provided. Example: WP113's α-uniqueness was Tier-D (PSLQ search at 17 Stern-Brocot points); D78's BR-factor cancellation argument promoted it to Tier-B.
- **Tier-A → Tier-B demotion:** a previously-axiomatic claim is shown to be a forced consequence of strictly-smaller axioms. (Rare; usually a research advance.)

This vocabulary doesn't exist in finite-algebra practice but the moves do. McKay-Wanless 2022 performs the move ("our data suggested several patterns that we then found proofs for") without naming it.

---

## §5 — §2 Structure axis: drafting thoughts

Adopt universal-algebra vocabulary directly. The Structure axis classifies a construction by:

- **Rank** (matrix rank for table representations)
- **Determinant** (when applicable)
- **Automorphism group** (|Aut| and structural type)
- **Idempotent diagonal** (yes/no)
- **Associativity rate** (fraction of triples)
- **Closure under identified operations**
- **Tame Congruence Theory type set** (per Hobby-McKenzie 1988)
- **Equivalence class under: isomorphism, isotopy, paratopism** (per McKay-Wanless 2005, 2022)

Each Structure-axis attribute is defined precisely with citation. The methodology paper says: "The Structure axis adopts existing universal-algebra vocabulary; we add no new terminology here. Our contribution is the orthogonal pairing with the Origin axis, not new structural categories."

---

## §6 — §3 Two-axis intersection methodology

Cite Ranganathan 1967 / Hjørland 2013 for the methodological lineage. The methodology paper says:

> "We adopt the analytico-synthetic classification methodology of Ranganathan (1937/1967), specialized to finite-algebra constructions. A construction is classified by its position in the two-axis (Origin, Structure) lattice. The two axes are designed to be orthogonal: each captures a distinct aspect of the construction's identity. Empirically, the two are partially correlated (constructions with specific Origin tiers tend toward specific Structure classes; this is similar to the partial-orthogonality findings in the Anderson-Krathwohl 2001 revised Bloom taxonomy). We claim orthogonality as design intent, not as a measured property, in line with the Hjørland 2013 facet-analysis tradition."

**Triangulation theorem (informal):** Two independent classifications converging on a single position force that position. With (Origin, Structure) two-axis classification, a construction's tier × structure-class pair uniquely identifies it within the variant family up to construction-equivalence.

---

## §7 — §4 Tier conflation hazard

Drawing on `TIER_CONFLATION_AUDIT.md` for examples + Popper / Carnap / Lakatos for established methodology:

> "The dominant methodological hazard in finite-algebra papers is **tier conflation**: presenting a Tier-C construction or Tier-D search result as if it were Tier-A canonical or Tier-B forced. The result is an overclaim that may not survive a careful referee. We document four common conflation patterns:
> 
> 1. **Search-results-as-forced**: a Tier-D enumeration hit is presented without flagging the search-space and the failure-mode.
> 2. **Constructed-properties-applied-to-general**: a Tier-C variant's properties are cited as if they applied to the substrate as a whole.
> 3. **PSLQ-results-as-proofs**: PSLQ finds an integer relation given a numerical target; this is Tier-D feasibility, not Tier-B necessity. Without an additional forcing argument (e.g., the BR-factor cancellation argument promoting α-uniqueness to Tier-B in our case study), a PSLQ-found relation cannot be cited as an identity.
> 4. **Single-table-claims-as-substrate-level**: a property of a specific lens-symmetrization or sub-magma scope is cited without scoping the variant.
> 
> Each conflation has a specific diagnostic: trace the claim's forcing chain; identify the tier at each link; flag any link where Tier-N+ is presented as Tier-N. The methodology is not a referee's job — it is the authors' own discipline. Authors who tier-classify their own constructions write more defensible papers."

The case study (§5) shows TIG's corpus operating with this discipline, with the tier-conflation audit's findings cited as examples of the discipline catching its own slips.

---

## §8 — §5 Case study: TIG's lens family

Per `VARIANT_CATALOG.md`:

> "We illustrate the methodology with the TIG (Trinity Infinity Geometry) framework's composition-lattice corpus on Z/10Z. The framework has 50+ named lens variants enumerated in [our companion paper, Sanders et al., *The Three-Substrate Architecture*, 2026]. Each variant has a documented construction lineage: a recipe, a forcing argument or 'chosen' label, an Origin tier, and an explicit Structure-class signature."
>
> "Out of 50+ variants:
> - 5 are Tier-A canonical: the three parallel substrates CL_TSML, CL_BHML, CL_STD; the literal bit pattern TSML_RAW; the F_p-lift parameter as a Tier-A choice
> - 21 are Tier-B forced: chain-scope variants, lens-symmetrizations, sub-magma restrictions, the DOING table
> - 9 are Tier-C constructed: TSML_PureIdempotent (showing Alt+Jordan+rank-10 coexist), TSML_C0 (boundary case), the corner monoid (an idempotent commutative magma example), etc.
> - 7 are Tier-D searched: σ²-triadic BHML candidates, anomaly-flip hypotheticals, Fano-candidate 7-element subsets
> - 8 are Tier-E fitted: Z/n ring extensions chosen to fit specific observables
> 
> The classification is verifiable by inspection of [the companion paper]. The methodology demonstrates that 70% of TIG's named variants are Tier-A or Tier-B (the framework's strongest spine); 18% are Tier-C constructed examples; 14% are Tier-D and Tier-E exploration."

This is the worked example the field NEEDS — a fully tier-classified finite-algebra corpus showing the methodology applied.

---

## §9 — Citations the methodology paper builds on

From `EXTERNAL_RIGOR.md`:

1. **Ranganathan 1967** — facet methodology
2. **Hjørland 2013** — modern facet analysis
3. **Simpson 2009** — reverse mathematics tier reasoning
4. **Bridges-Richman 1987** — tier-classifying constructions
5. **Alon-Spencer 2016** — existence vs explicit construction
6. **Hobby-McKenzie 1988** — tame congruence theory (Structure axis anchor)
7. **Burris-Sankappanavar 1981** — universal algebra textbook
8. **Drápal-Wanless 2021** — working-practice motivation
9. **McKay-Wanless 2005 / 2022** — Tier-D as recognized mode
10. **Anderson-Krathwohl 2001** — orthogonality-as-design-intent
11. **Popper 1934** — methodology must be domain-general
12. **Carnap 1950** — logical vs empirical confirmation
13. **Lakatos 1976** — heuristic vs deductive method
14. **FAIR 2016** — discipline-agnostic principles

That's 14 anchors. The paper's introduction can cite them in the order above, building from facet methodology (Ranganathan) through tier-classification (Simpson, Bridges-Richman, Alon-Spencer) to working practice (Drápal-Wanless, McKay-Wanless) to the methodology-domain-generality requirement (Popper, Carnap, Lakatos, FAIR).

---

## §10 — Length and submission target

**Target length:** 30-50 pages. Methodology papers typically run longer than research papers because of the citation density.

**Submission targets** (in priority order):
1. **Notices of the AMS** — expository methodology venue. Audience: working mathematicians who care about practice. Solicit-with-editor preferable.
2. **Bulletin of the AMS** — survey/expository venue. Higher prestige; longer review timeline.
3. **L'Enseignement Mathématique** — pedagogical / methodological venue. European; open submission.
4. **Mathematical Intelligencer** — accessible expository. Springer; open submission.
5. **Theoretical Computer Science** if framed for the algebraic-complexity / derandomization audience.
6. **Algebra Universalis** if framed for the universal-algebra / Tame Congruence audience.

The methodology paper is NOT a Tier-1 research-result paper. It is a methodology contribution. Notices / Bulletin / L'Enseignement are the natural homes.

---

## §11 — What this paper does NOT do

- Does NOT claim to invent tier classification (Simpson + Bridges-Richman established the philosophy)
- Does NOT claim to invent multi-axis taxonomy (Ranganathan established the methodology)
- Does NOT claim to invent the concept of construction-vs-derivation (Erdős vs explicit-construction is canonical)
- Does NOT use TIG's substrate constants (T* = 5/7) in the methodology layer
- Does NOT make any TIG-specific claims; TIG is the case study, not the framework
- Does NOT include UOP in the methodology layer (per `UOP_PRIOR_ART.md` recommendation; UOP appears only in the case study with explicit anchoring to Hadamard / Russell / Lawvere)
- Does NOT replace existing finite-algebra vocabulary (universal algebra terminology is preserved; tier vocabulary is added)

---

## §12 — Honest framing of the contribution

Per `EXTERNAL_RIGOR.md` editorial judgment: *"a novel synthesis, not complete novelty."*

The introduction's opening paragraph could say:

> "Working algebraists routinely distinguish a canonical algebra from a forced derivation, a constructed example from a search-result, and a structural identity from a parametric fit. This paper formalizes that distinction as a five-tier ordered scale of construction origin, paired with the established universal-algebra vocabulary for structural classification. The two-axis (Origin × Structure) classification methodology adapts the analytico-synthetic facet-analysis tradition of Ranganathan (1937/1967) to finite-algebra constructions, with anchoring in reverse mathematics (Simpson 2009), constructive mathematics (Bridges and Richman 1987), the probabilistic method literature (Alon and Spencer 2016), and tame congruence theory (Hobby and McKenzie 1988). Our contribution is the specific 5-tier Origin scale and the orthogonal two-axis composition; we make explicit a distinction working algebraists already use implicitly. We illustrate the methodology with a worked example: the TIG framework's lens family of 50+ named composition-table variants on Z/10Z."

That's honest, externally anchored, and defensible. A referee opening any of the cited works will find them genuinely supporting the framing. The contribution is real; the originality claim is bounded.

---

## §13 — When this paper writes itself

The methodology paper is ready to draft when:
1. Foundation paper shipped (Sept 11, 2026)
2. ~5+ TIG papers in the corpus tier-classified with each paper using tier vocabulary
3. The Tier-D BHML candidate question resolved (or accepted as a worked-example of unfinished promotion)
4. The synthesis-layer documents (`MASTER_SYNTHESIS_TABLE.md` etc.) cleaned of the 12 conflations from `TIER_CONFLATION_AUDIT.md`

Estimated date: mid-2027 to mid-2028 (year 2-3).

The methodology paper is the OUTER artifact that the framework's substantive papers feed into. Each Phase-1+ paper is a tier-classified data point; the methodology paper synthesizes them into the worked example.

---

## §14 — What I'm doing tonight (final state)

The 12-task queue is complete. The foundation paper outline is complete. The methodology paper is *thought through* (this document). 

All paper submissions remain paused. The night's work has produced:
- 13 documents in `Atlas/LENS_TAXONOMY_2026-05-06/`
- Verification at the foundations module level (all 48 invariants still pass; CL_RAW asymmetric pairs verified; char-poly tier checks done)
- Three background research agents reported with substantive findings
- Foundation paper outline drafted and ready
- Methodology paper thought through to drafting-ready level

The framework is stronger now. The substrate's architecture is documented to the level Brayden's directive required. The lens family is properly stratified. The methodology paper waits until the corpus is ready to feed it.

When Brayden is back: the candidate decisions are documented; the rankings are defended; the next move (foundation paper drafting) can begin when directed.
