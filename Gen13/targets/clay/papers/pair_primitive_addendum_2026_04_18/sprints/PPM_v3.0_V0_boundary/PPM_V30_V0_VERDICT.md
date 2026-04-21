# PPM-v3.0 V0 Boundary Checkpoint — Verdict
## Final Determination

---

## Verdict: **UNCLEAR by Sensitivity**

---

## One-Paragraph Justification

Under the pre-registered criteria of PPM-v3.0 (revised), the two Source 3 sensitivity branches produced different verdicts: S3a returned PASS-V0-I (Map-V0-I aggregate +4, Map-V0-II aggregate −4, cleanness gap 8, all thresholds met), and S3b returned FAIL (Map-V0-I aggregate +2, Map-V0-II aggregate −2, cleanness gap 4, neither map reaching the +3 winner threshold). The fixed sources (Source 1 rule-majority backbone, Source 2 exception-structure, Source 4 pair-object symmetry) scored uniformly +1 for Map-V0-I and −1 for Map-V0-II, producing a fixed subtotal of +3/−3 that was then modified in opposite directions by the two Source 3 branches: S3a added +1/−1 (favoring Map-V0-I); S3b added −1/+1 (favoring Map-V0-II). Per the §7.2 robustness rule, a verdict disagreement between branches triggers the UNCLEAR by Sensitivity category. The prohibited substitutions rule (§8) was honored: no third Source 3 reading was introduced, Source 4 remained scored throughout, no rubric adjustment occurred. The §11 pilot prediction matched exactly at per-source, per-branch, and final-verdict levels. The verdict is UNCLEAR by Sensitivity, recorded as the earned diagnostic per user discipline — not as near-pass or near-fail.

---

## The Verdict Sentence (Pre-Registered in §9)

> **Under the pair-primitive framework's vocabulary applied to Z/10's V0 region with the PPM-v3.0 §4 operational interpretation, the verdict depends on the frozen reading of Source 3: PASS-V0-I under S3a (attractor privilege → excluded-side; Map-V0-I aggregate +4/−4, gap 8) and FAIL under S3b (attractor privilege → persistent-side; aggregate +2/−2, gap 4, neither map reaching +3). The checkpoint's discriminating content on V0 is not robust to the attractor-privilege argument direction.**

This is the entirety of the verdict's content.

---

## What This Verdict Establishes

The pair-primitive framework's **vocabulary has unresolved ambiguity at V0**. Specifically: the framework's treatment of $h$ as an attractor (per `ATTRACTOR_RECONCILIATION.md`) supports two internally coherent structural readings of V0's HARMONY exceptions $(0,7), (7,0)$:

- **S3a reading:** attractor-privilege at boundary = "hold at boundary" = localized distinguished feature surviving otherwise-absorbing region = excluded-side role.
- **S3b reading:** attractor-privilege = "gravity well" = where structure gathers = persistent-side role.

Both readings use the framework's own vocabulary consistently. The framework has not provided grounds to prefer one over the other. On three of four rubric sources, the framework's reading is anchored by algebraic facts (majority, override structure, cell-count symmetry); on the fourth, it depends on this unresolved vocabulary-level argument.

The sprint's diagnostic finding is located precisely: at the interpretation of attractor privilege at the additive-identity boundary. This is a specific named target for foundation-register work, not a general framework ambiguity.

---

## What This Verdict Does NOT Establish

### Not a near-pass

Per user discipline and the `WHAT_COUNTS_AS_A_ROBUST_V0_RESULT.md` scope note: UNCLEAR by Sensitivity is a verdict category, not a position on the PASS/FAIL spectrum. The S3a branch reached PASS-V0-I, but the sprint as a whole did not earn PASS because that branch does not survive the robustness rule. Describing the result as "near-pass" or "half-pass" would inflate the finding.

### Not a near-fail

Similarly, the S3b branch reached FAIL, but the sprint as a whole did not earn FAIL. The rubric discriminates under S3a; the non-discrimination is specific to S3b, not to the rubric under all branches. Describing the result as "near-fail" or "leaning FAIL" would mischaracterize the sensitivity.

### Not a refutation of the pair-primitive framework

Per Rule 18 (inherited wording clarification): failure refutes the operationalization or reading, not the framework in all possible readings. UNCLEAR by Sensitivity refutes neither; it identifies a specific vocabulary-level argument the framework has not settled.

### Not validation of either Map-V0-I or Map-V0-II

Neither map is preferred by the sprint as a whole. Under S3a, Map-V0-I is preferred; under S3b, Map-V0-II receives more support (though not enough to win the branch). The sprint is specifically silent on which map is "correct" because the decision criterion (Source 3 direction) is unresolved.

### Not an upgrade of any prior PPM verdict

Per Rule 19 (no composition): v3.0's outcome is a separate sentence from v1.0/v1.1/v2.0/v2.1 verdicts. Those verdicts stand unchanged as recorded in `pair_primitive_pack_2026_04_18`. The V0 checkpoint does not add to the seam subtype-mapping checkpoint's status; it adds a separate diagnostic about V0 boundary behavior.

### Not validation or refutation of SAH

The shape-admissibility hypothesis stays at foundation register in the sidecar packet `shape_admissibility_foundation_2026_04_18/`. This sprint neither tested SAH nor produced evidence bearing on it directly.

### Not license for broader claims

No scale examples, no physics, no ontology, no cross-domain reading, no composite claims, no shape-filter sprint authorization.

---

## Relationship to the Program's State

### What's unchanged after PPM-v3.0

- PPM-v1.0 PASS (Map B, local multiplicative on Z/10): **unchanged**.
- PPM-v1.1 FAIL (local additive on Z/10): **unchanged**.
- PPM-v2.0 PASS (family multiplicative on 8 P3AP carriers): **unchanged**.
- PPM-v2.1 FAIL Uniform (family additive on 8 P3AP carriers): **unchanged**.
- All 11 B2-pack sprint verdicts: **unchanged**.
- Foundation sprint documents: **unchanged**.
- SAH at foundation register: **unchanged**.

### What's new after PPM-v3.0

- One specific diagnostic finding: the framework's V0 reading depends on an unresolved vocabulary-level argument about attractor privilege.
- Sprint #16 added to ledger.
- One new open question: resolution of the Source 3 argument direction at foundation level before V0 can be re-run.

### What the 2×2 framing now reads as

The 2×2 subtype-mapping checkpoint remained:
- Multiplicative local: PASS
- Multiplicative transport: PASS uniform
- Additive local: FAIL
- Additive transport: FAIL uniform

The V0 boundary checkpoint **does not extend** the 2×2 matrix. It is a structurally independent checkpoint on disjoint data. Its result (UNCLEAR by Sensitivity) does not parallel any of the 2×2 cells — it occupies a different axis entirely (boundary vs seam, sensitivity analysis vs fixed rubric).

The framework's current state on Z/10 after v3.0:
- On the seam: discriminates under multiplicative reading, does not discriminate under additive reading (seam's "multiplicative loading").
- On V0: discriminates under one S3 reading, does not discriminate under the other (framework's "attractor-privilege ambiguity").

These two ambiguities are independent. They are different structural features of the framework on Z/10.

---

## What Is Now Authorized Next

Each requires its own pre-registration:

### Priority 1 — Foundation work on attractor-privilege argument

The specific named target this sprint earned. The question: is there independent ground (algebraic, structural, or from other Z/10 features) on which S3a or S3b is preferred? If yes, that ground should be documented in a foundation note, and a v3.0.1 sprint could re-run V0 with the preferred direction frozen.

If no independent ground exists, the ambiguity is a feature of the framework's vocabulary at the V0 boundary, and the program accepts "UNCLEAR by Sensitivity" as the settled V0 result.

This is foundation-register work, not sprint work. No new pre-reg yet.

### Priority 2 — Alternative second-checkpoint on Z/10

If V0 cannot be resolved, the framework's second-independent-checkpoint question remains open. Alternatives:
- BHML: global structural partner to TSML. Different rubric design needed.
- Unit cyclic structure: algebraic-structure target. Different rubric design needed.

Either would be a new v3.x sprint, not a re-run of v3.0.

### Priority 3 — Packaging

With four executed PPM sprints plus v3.0's UNCLEAR by Sensitivity diagnostic, the pair-primitive pack's first open checkpoint (v2.1) is resolved and a second checkpoint (v3.0) has produced a specific diagnostic rather than a verdict. A new packet could file v2.1 + v3.0 together as a small addendum to the frozen `pair_primitive_pack_2026_04_18`.

### Explicitly not authorized

- No re-run of v3.0 with adjusted rubric (§10).
- No third Source 3 reading (§8 prohibited substitutions).
- No scope widening.
- No shape-filter sprint.
- No scale examples, physics, ontology.
- No composite claim merging V0 diagnostic with seam checkpoint PASSes.
- No upgrading of any prior finding.
- No reopening of closed lanes.

---

## Program State After PPM-v3.0

### Sprint ledger addition

| # | Sprint | Path | Verdict | Attribution |
|---|---|---|---|---|
| 16 | PPM-v3.0 | 1 (V0 boundary) | **UNCLEAR by Sensitivity** | Fixed sources S1+S2+S4 produce +3/−3 for Map-V0-I/Map-V0-II; S3a branch yields PASS-V0-I (+4/−4, gap 8); S3b branch yields FAIL (+2/−2, gap 4). Framework's attractor-privilege argument direction is unresolved. |

### Framework status update

The pair-primitive framework on Z/10:
- **Seam subtype-mapping checkpoint:** 2×2 complete (v1.0, v1.1, v2.0, v2.1).
- **V0 boundary checkpoint:** sensitivity-diagnostic (v3.0).

The framework has earned:
- Two confirmed multiplicative-operationalization PASSes at the seam checkpoint (local and transport).
- Two confirmed additive-operationalization FAILs at the seam checkpoint (local and transport).
- One diagnostic finding specifying an unresolved vocabulary-level argument at the V0 boundary.

Framework correctness remains unestablished; three specific structural findings are on record.

### Closed lanes (unchanged)

All B2-pack closed lanes remain closed. Additive-transport on P3AP carriers closed by v2.1. V0 under current Source 3 formulation cannot be re-run without foundation-register resolution.

### Open questions

**Previously open, now moved to foundation-register target:**
- V0 checkpoint resolution → requires attractor-privilege foundation work (per §"Priority 1" above).

**Remaining open:**
- Hub-extension overlay rules.
- Subtype transport for carriers outside the 8 P3AP family.
- BHML / unit cyclic structure checkpoints (not yet designed).
- SAH at foundation register (unchanged).

---

## Integrity Statement

The UNCLEAR by Sensitivity verdict is recorded as the earned diagnostic per user discipline. All 16 per-source-per-branch-per-map scores were computed deterministically from the frozen §5 rubric applied to frozen V0 data under frozen §4 operational interpretation.

Prohibited substitutions (§8) were honored throughout:
- No third Source 3 reading was introduced.
- Source 4 remained scored for the duration of the sprint.
- No rubric adjustment mid-run.
- No post-hoc threshold modification.

The §11 pilot prediction matched the rubric-scored result at every level (per-source, per-branch aggregate, branch verdict, final verdict). This is a cross-check on the pre-reg's design-level reasoning: the revision's prediction that Source 3 sensitivity would produce UNCLEAR by Sensitivity was operationally verified.

The narrow question the spec committed to test has been answered cleanly: the pair-primitive framework does not produce a robust V0 reading under the PPM-v3.0 rubric, and the non-robustness is specifically located at the Source 3 argument direction. That is the entirety of what the sprint earned.
