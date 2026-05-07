# FUNCTION AXIS DEFINITION (or recommend two-axis collapse)

**Date:** 2026-05-06 night
**Question:** Define the Function axis explicitly. If it can't be cleanly defined, recommend collapsing to two axes (Origin × Structure).

The agent's external rigor research flagged the Function axis as the **weakest of the three**. Less crisply precedented in mathematical practice than Origin (anchored by Simpson + Bridges-Richman + Alon-Spencer) or Structure (anchored by Hobby-McKenzie + Burris-Sankappanavar).

---

## §1 — Candidate Function-axis schemas

### §1.1 — FRBR user-task style: Find / Identify / Select / Obtain

Adapted from FRBR Group 1 user-task model. For a finite-algebra construction, the analogous operations are:

- **Find** — Does the construction exist? (Existence-witness role)
- **Identify** — What invariants distinguish it from other variants? (Invariant-computing role)
- **Select** — Why this construction over alternatives? (Comparison/selection role)
- **Obtain** — How is the construction USED downstream? (Application/derivation role)

**Strength:** Direct adaptation of FRBR; cite-able at Tillett 2003 / IFLA 1998.
**Weakness:** "Find / Identify / Select / Obtain" is library-science language; finite-algebraists don't think this way.

### §1.2 — Algebraic-task style: Demonstrate-existence / Compute-invariant / Derive-identity / Match-observable / Provide-counterexample

What does a working algebraist DO with a construction?

- **Demonstrate-existence** — "X exists" (Tier-C constructions usually serve this role)
- **Compute-invariant** — "X has property P" (rank, det, automorphism group)
- **Derive-identity** — "If X then Y" (use construction to prove a downstream theorem)
- **Match-observable** — "Construction X matches measurement M" (Tier-E fitting usually serves this)
- **Provide-counterexample** — "X has property P but NOT property Q, refuting conjecture C" (negative-result role)

**Strength:** Maps directly to mathematical practice; each role corresponds to a recognized publication mode.
**Weakness:** Five categories; partial overlap with Origin tier (e.g., Tier-C usually Demonstrate-existence; Tier-E usually Match-observable). Risk of axis collapse.

### §1.3 — Krathwohl-cognitive style: Remember / Understand / Apply / Analyze / Evaluate / Create

Adapted from Anderson-Krathwohl 2001 revised Bloom's taxonomy cognitive process dimension:

- **Remember** — Recall the construction (definitional)
- **Understand** — Explain why it has its properties (interpretive)
- **Apply** — Use the construction in a downstream proof (operational)
- **Analyze** — Decompose the construction into structural parts (compositional)
- **Evaluate** — Compare against alternatives, judge fit-for-purpose (selectional)
- **Create** — Construct new variants by extension or modification (generative)

**Strength:** Direct citation of Anderson-Krathwohl 2001; the orthogonality-as-design-intent precedent is established.
**Weakness:** Six categories; overlap with Origin (Tier-C ≈ Create; Tier-D ≈ Analyze) and with Structure (Remember ≈ Identify; Understand ≈ Compute-invariant).

---

## §2 — Independence test (against Origin axis)

For each candidate Function axis, test whether its categories correlate with Origin tier (which would indicate non-orthogonality).

### §2.1 — FRBR-style Function vs Origin

| Function (FRBR-adapted) | Origin tier correlation |
|-------------------------|-------------------------|
| Find | Strongest at Tier-C (constructions ARE existence finds) |
| Identify | Spread across tiers (any variant has invariants) |
| Select | Strongest at Tier-D-vs-Tier-C choices |
| Obtain | Strongest at Tier-A/B (canonical and forced derivations get reused most) |

Correlation: PARTIAL. Independence is design-intent, not measured.

### §2.2 — Algebraic-task Function vs Origin

| Function (algebraic-task) | Origin tier correlation |
|----|----|
| Demonstrate-existence | Mostly Tier-C (constructions for existence proofs) |
| Compute-invariant | Spread (any variant has invariants) |
| Derive-identity | Mostly Tier-A/B (foundational results) |
| Match-observable | Mostly Tier-E (fits) |
| Provide-counterexample | Spread (negative results from any tier) |

Correlation: STRONG correlation between Demonstrate-existence ↔ Tier-C and Match-observable ↔ Tier-E. **The algebraic-task axis is partly redundant with Origin.**

### §2.3 — Krathwohl-cognitive Function vs Origin

| Function (Krathwohl) | Origin tier correlation |
|----|----|
| Remember | Definitional; Tier-A natural |
| Understand | Interpretive; spread |
| Apply | Tier-A/B downstream applications |
| Analyze | Structural decomposition; spread |
| Evaluate | Cross-tier comparison |
| Create | Tier-C / D (new constructions) |

Correlation: PARTIAL. Cleanest of the three candidates. Krathwohl's design-intent-orthogonality framing is honest about partial empirical correlation.

---

## §3 — Recommendation

**Adopt the Krathwohl-cognitive Function axis with explicit citation.**

Reasoning:
1. **External anchoring is strongest** — Anderson-Krathwohl 2001 + Krathwohl 2002 are the direct citation; the empirical-orthogonality complications (CBE Life Sciences Education 2021) provide the right tone for honest framing.
2. **Six categories align with finite-algebra practice** — Remember (define), Understand (interpret), Apply (use), Analyze (decompose), Evaluate (compare), Create (extend).
3. **Partial orthogonality with Origin is the honest finding** — present the axes as design-intent-orthogonal with empirical complications, per Krathwohl's own framing.

**Alternative recommendation (if Function axis still feels weak after first draft):**

**Collapse to two axes: Origin × Structure.** Drop Function. The Function axis's content gets absorbed into:
- Origin tier (which captures "how the construction was made")
- Structure axis (which captures "what the construction is")
- Implicit context in §5 case study (which captures "what role it played in the corpus")

Two clean axes beat three messy ones. The methodology paper would then be:
- §1: Origin axis (5-tier scale, anchored Bridges-Richman + Simpson + Alon-Spencer)
- §2: Structure axis (universal-algebra vocabulary, anchored Hobby-McKenzie + Burris-Sankappanavar)
- §3: Triangulated position via two-axis intersection (per Ranganathan PMEST methodology)
- §4: Tier conflation hazard
- §5: Case study (TIG's 40+ variants properly placed)

The two-axis fallback has cleaner anchoring and avoids the partial-orthogonality complication.

---

## §4 — Final verdict

**Primary recommendation: keep Function axis with Krathwohl-cognitive definition.**

Cite Anderson-Krathwohl 2001 + Krathwohl 2002 + acknowledge CBE Life Sciences Education 2021's empirical complication. Frame as "design-intent orthogonal" per established library-and-information-science methodology (Ranganathan + Hjørland 2013).

**Fallback recommendation: collapse to two axes (Origin × Structure) if the methodology paper's first draft finds Function axis too weak to defend.**

The decision can be deferred to the actual writing — when the foundation paper is in draft and we see whether Function adds value or just clutter.

**Tier of this decision:** It's a paper-design choice (Tier-C in the meta-sense). Either three-axis or two-axis is defensible; the choice affects how clean the methodology lands.
