# PPM-v3.0 — V0 Boundary Checkpoint Pre-Registration (Revised)
## Pair-Primitive Framework Applied to Z/10's V0 Zero-Absorption Region, with Source 3 Sensitivity Branch

---

## Revision Note

**Revision:** the original v3.0 draft froze Source 3 ("attractor-privilege reading") at a single argument direction. Per user direction, Source 3 is now a **sensitivity branch** scored under two frozen readings (S3a and S3b), with a robustness rule governing how the two branches combine into a final verdict.

**Rationale:** see `WHY_SOURCE_3_BECAME_SENSITIVITY_BRANCH.md`. Source 3's argument direction is a vocabulary-level choice inside the pair-primitive framework, not an algebraic fact about Z/10. Sources 1, 2, 4 are algebraically anchored and do not need sensitivity analysis. Source 3 does.

**Everything else unchanged from the original draft** except where noted.

---

## Scope Declaration

**Path:** Local Theorem Chart (Path 1).
**Attractor convention:** $h_\text{thm} = 7$ (Z/10 theorem scope).
**Claim class:** structural-fit claim at the local theorem chart, conditional on the framework's vocabulary applied to V0's boundary behavior.
**Canonical construction source:** Rule (b) of `CANONICAL_TSML_CONSTRUCTION.md`.
**Relation to prior sprints:**
- Operates on Z/10's V0 cells (disjoint from the seam).
- Does NOT re-score any prior PPM or Path 3 verdict.
- Does NOT extend beyond Z/10.
- Tests a **second independent checkpoint** on Z/10, disjoint from the seam subtype-mapping checkpoint.

**Inherited wording clarification (Rule 18 extension):** This sprint evaluates the pair-primitive framework on the V0 region under a specific operational reading; failure refutes this reading of V0, not the framework in all possible readings.

---

**Status:** DRAFT awaiting approval (revised).
**Version:** PPM-v3.0 (V0 boundary, local, Source-3 sensitivity branch).
**Change policy:** once any source is scored, spec cannot be edited. Revisions require v3.0.1+.

---

## 1. Hypothesis Under Test

**Hypothesis (PPM-v3.0-H).** Under the pair-primitive framework's vocabulary applied to Z/10's V0 region via the rubric in §5, exactly one of Map-V0-I or Map-V0-II produces a coherent structural fit across the four data sources at pre-registered cleanness threshold, **and this verdict is robust to the Source 3 argument direction**.

**Null:** (a) neither map reaches the threshold under either S3 direction, (b) both fit comparably without cleanness under either S3 direction, OR (c) the verdict differs between S3a and S3b (sensitivity).

---

## 2. V0 Structure On Z/10

From `CANONICAL_TSML_CONSTRUCTION.md` Rule (b):

$$T(0, x) = T(x, 0) = \begin{cases} h & \text{if } x = h \\ 0 & \text{otherwise} \end{cases}$$

On Z/10 with $h = 7$:
- **V0 cells:** 19 cells where at least one operand is 0. $(0, y)$ for $y \in \{0,\ldots,9\}$ plus $(y, 0)$ for $y \in \{1,\ldots,9\}$.
- **V0_Z (zero-output):** 17 cells, all V0 EXCEPT $(0, 7)$ and $(7, 0)$.
- **V0_H (HARMONY-output):** 2 cells, $(0, 7)$ and $(7, 0)$.
- **Split:** 17 / 2.

As unordered-edge set: $\{(0,y) : y \in \{1,\ldots,9\}\}$ — 9 edges, star topology at vertex 0. Edge $(0, 7)$ is distinguished (HARMONY output).

---

## 3. Candidate Mappings — V0-Specific

- **Map-V0-I:** V0_Z = persistent-side, V0_H = excluded-side.
- **Map-V0-II:** V0_H = persistent-side, V0_Z = excluded-side.

V0-specific labels to preserve independence from the seam checkpoint.

---

## 4. Operational Interpretation (FROZEN)

**Core reading:** persistent-side = structural backbone; excluded-side = localized departure.

**V0-adapted reading:**
- **Persistent-side** = subtype constituting V0's default structural behavior (the rule V0 imposes by construction).
- **Excluded-side** = subtype constituting a localized departure from V0's default (the exception overriding the default rule).

**Key structural facts:**
- V0 is the additive-identity absorption region.
- V0 is governed by Rule (b): zero-absorption *except* at $h$.
- The HARMONY exception is a localized override affecting 2 of 19 cells at the distinguished vertex $h = 7$.
- Framework's hold/gap/flow vocabulary reads onto V0: zero-absorption as "gap," HARMONY exception as "hold" at boundary.

---

## 5. Scoring Rubric (FROZEN)

### 5.1 Sources 1, 2, 4 — Fixed (Algebraically Anchored)

Each scores in $\{-1, 0, +1\}$ per map. Unchanged from original draft.

#### Source 1 — V0 rule-majority / default-behavior backbone

**Criterion:** backbone requires (a) majority (≥ 50%) of V0 cells AND (b) alignment with V0's constructed default (zero-absorption is the default; HARMONY is the override).

**Evaluation:** V0_Z meets both (89% + default); V0_H meets neither (11% + override).

**Scoring:**
- Map-V0-I (persistent = V0_Z): **+1**.
- Map-V0-II (persistent = V0_H): **−1**.

#### Source 2 — Exception-structure reading

**Criterion:** excluded-side is the localized exception iff (a) minority count AND (b) default-rule override AND (c) restricted to a distinguished element.

**Evaluation:** V0_H meets all three; V0_Z meets none.

**Scoring:**
- Map-V0-I (excluded = V0_H): **+1**.
- Map-V0-II (excluded = V0_Z): **−1**.

#### Source 4 — Pair-object symmetry

**Criterion:** excluded-side matches pair-object signature iff it has exactly 2 cells forming a swap-symmetric pair.

**Evaluation:** V0_H = {(0,7), (7,0)} matches; V0_Z (17 cells) does not.

**Scoring:**
- Map-V0-I (excluded = V0_H): **+1**.
- Map-V0-II (excluded = V0_Z): **−1**.

### 5.2 Source 3 — Attractor-Privilege Reading (Sensitivity Branch, FROZEN)

**Background.** The framework's treatment of $h$ (per `ATTRACTOR_RECONCILIATION.md`) gives $h$ a privileged structural role. At V0, this manifests as: $h$ is the only element whose cells resist zero-absorption.

**Two frozen readings, both scored:**

#### S3a — Attractor privilege as "hold at boundary" → excluded-side

**Criterion (S3a):** if $h$'s V0-privilege manifests as a surviving distinction at a boundary that otherwise collapses to nothingness, this is "hold" content — a localized, distinguished feature → **excluded-side** role under the framework's vocabulary.

**Scoring under S3a:**
- Map-V0-I (excluded = V0_H): attractor privilege at excluded-side = "hold at boundary." Coheres. **+1**.
- Map-V0-II (persistent = V0_H): attractor privilege at persistent-side contradicts Rule (b)'s override framing. **−1**.

#### S3b — Attractor privilege as "structural gravity well" → persistent-side

**Criterion (S3b):** if $h$ is "where structure gathers" (gravity well), then structure associated with $h$ is at its most persistent — the content that survives collapse toward the attractor. V0_H cells preserve $h$ at the boundary, carrying the attractor's persistent signature. "Persistent at attractor" → **persistent-side** role.

**Scoring under S3b:**
- Map-V0-I (persistent = V0_Z): persistent-side does NOT contain attractor-privilege content. **−1**.
- Map-V0-II (persistent = V0_H): persistent-side DOES contain attractor-privilege content. **+1**.

### 5.3 The Sensitivity

S3a and S3b score Source 3 with **opposite signs** on both maps. S3a favors Map-V0-I; S3b favors Map-V0-II. This is the structural fragility the revision addresses.

Neither reading is picked pre-sprint. Both are scored; §7 robustness rule decides final verdict.

**No third reading permitted** (per §8). S3a and S3b are the two frozen readings. Alternative readings require a new pre-reg version.

---

## 6. Aggregation Per Sensitivity Branch

For each branch (S3a, S3b):

$$S_\text{Map, branch} = S_1 + S_2 + S_{3\text{-branch}} + S_4$$

Each aggregate in $[-4, +4]$. Two aggregates per map (one per branch).

Per-branch cleanness gap: $|S_\text{Map-V0-I, branch} - S_\text{Map-V0-II, branch}|$.

---

## 7. Per-Branch Verdict and Robustness Rule (FROZEN)

### 7.1 Per-branch verdict

For each of S3a and S3b, apply v1.0 threshold style:

- **Branch PASS-V0-I** if Map-V0-I ≥ +3 AND Map-V0-II ≤ +1 AND gap ≥ 2.
- **Branch PASS-V0-II** if Map-V0-II ≥ +3 AND Map-V0-I ≤ +1 AND gap ≥ 2.
- **Branch FAIL** if neither map reaches +3.
- **Branch UNCLEAR** if one map ≥ +3 but gap < 2, OR both in {+2, +3} with gap < 2.

### 7.2 Final verdict — robustness rule

Five possible final outcomes:

**Robust PASS-V0-I:** Branch PASS-V0-I under BOTH S3a AND S3b.

**Robust PASS-V0-II:** Branch PASS-V0-II under BOTH S3a AND S3b.

**Robust FAIL:** Branch FAIL under BOTH S3a AND S3b.

**Robust UNCLEAR:** Branch UNCLEAR under BOTH S3a AND S3b.

**UNCLEAR by Sensitivity:** ANY other combination where branches disagree in verdict.

Examples of UNCLEAR by Sensitivity:
- PASS-V0-I under S3a, FAIL under S3b.
- PASS-V0-I under S3a, PASS-V0-II under S3b.
- PASS-V0-I under S3a, UNCLEAR under S3b.
- FAIL under S3a, UNCLEAR under S3b.

---

## 8. Anti-Tuning Rules

1. Rubric in §5 frozen before scoring.
2. Operational interpretation in §4 frozen.
3. V0 cell data (§2) is sole structural input.
4. Per-branch thresholds (§7.1) frozen.
5. Robustness rule (§7.2) frozen.
6. No post-hoc rubric adjustment.
7. Scoring proceeds source-by-source; per-branch aggregates computed independently.
8. **No substitute criteria for any source.** No third S3 reading permitted. Sources 1, 2, 4 criteria are frozen verbatim.
9. **No merging of v3.0 with prior PPM verdicts** (Rule 19 continues).
10. On any UNCLEAR outcome (sensitivity or robust), no re-run with adjusted rubric; successor requires v3.0.1+.

---

## 9. Verdict Sentences (Frozen)

| Outcome | Sentence |
|---|---|
| Robust PASS-V0-I | Under the pair-primitive framework's vocabulary applied to Z/10's V0 region with the §4 operational interpretation, Map-V0-I (V0_Z = persistent, V0_H = excluded) produces a coherent structural fit across the four pre-registered data sources at cleanness gap ≥ 2 **under both frozen readings of Source 3**. The checkpoint is robust to the attractor-privilege argument direction. |
| Robust PASS-V0-II | Under the same framework and rubric, Map-V0-II (V0_H = persistent, V0_Z = excluded) produces a coherent structural fit at cleanness gap ≥ 2 under both frozen readings of Source 3. The checkpoint is robust to the attractor-privilege argument direction. |
| Robust FAIL | Under the same framework and rubric, neither map reaches the pre-registered aggregate-score threshold under either frozen reading of Source 3. The framework's vocabulary does not cash out decisively on V0 boundary behavior, and this non-result is robust to the attractor-privilege argument direction. |
| Robust UNCLEAR | Under the same framework and rubric, both S3 branches produce ambiguous aggregate scores. The ambiguity is not due to Source 3 direction sensitivity; it is a property of the rubric under either reading. |
| UNCLEAR by Sensitivity | Under the same framework and rubric, the verdict depends on the frozen reading of Source 3: [specific S3a verdict] under S3a and [specific S3b verdict] under S3b. The checkpoint's discriminating content on V0 is not robust to the attractor-privilege argument direction. |

---

## 10. Scope Boundaries

**Tests:** whether the pair-primitive framework has a coherent mapping on V0's 19 cells under §4 interpretation, robust to S3 direction.

**Does NOT test:**
- BHML, unit cyclic structure, or any other Z/10 feature.
- V0 on rings other than Z/10.
- Additive/multiplicative operationalization axis (V0 has no seam-style AND/MAX choice).
- The seam subtype checkpoint.
- SAH or shape-admissibility claims.
- The "correct" Source 3 reading (explicitly not picked).

**Rule 19 reminder:** v3.0 verdict is a separate sentence. No composite claim with prior PPM verdicts.

---

## 11. Honest Prediction (Rule 21)

### Fixed sources (same across branches)

| Source | Map-V0-I | Map-V0-II |
|---|---:|---:|
| 1. Rule-majority backbone | +1 | −1 |
| 2. Exception-structure | +1 | −1 |
| 4. Pair-object symmetry | +1 | −1 |
| **Fixed subtotal** | **+3** | **−3** |

### Source 3 branches

| Branch | Map-V0-I | Map-V0-II |
|---|---:|---:|
| S3a (hold at boundary → excluded) | +1 | −1 |
| S3b (gravity well → persistent) | −1 | +1 |

### Combined aggregates per branch

**Under S3a:** Map-V0-I = +3 + (+1) = **+4**, Map-V0-II = −3 + (−1) = **−4**. Gap = 8. Map-V0-I clears +3, Map-V0-II ≤ +1, gap ≥ 2. Branch verdict: **PASS-V0-I**.

**Under S3b:** Map-V0-I = +3 + (−1) = **+2**, Map-V0-II = −3 + (+1) = **−2**. Gap = 4. Neither map reaches +3. Branch verdict: **FAIL**.

### Predicted final verdict

S3a → PASS-V0-I; S3b → FAIL. Branches differ → per §7.2: **UNCLEAR by Sensitivity**.

### What this prediction tells us

If the prediction holds, the sprint returns UNCLEAR by Sensitivity — a diagnostic finding specifying that V0's discriminating content depends on the attractor-privilege argument direction. This is different from the original draft's predicted PASS-V0-I because the revision converts a predicted fragile PASS into a predicted diagnostic UNCLEAR.

Both predictions are honest. The revised prediction is more informative: it names the specific vocabulary-level argument the framework has not settled.

### Diagnostic possibilities

1. **Source 1 default-vs-override reading.** A scorer could argue Rule (b) has two equally primary clauses rather than default+override. §5.1 frozen criterion rules this out.
2. **Source 4 pair-object ambiguity.** 17 zero-cells could be argued as "generalized pair." §5.4 frozen criterion requires "exactly 2 cells."
3. **S3a/S3b under-specification.** Each argument has internal ambiguity. §5.2 fixes both criteria.

Prediction does not modify thresholds. Rubric decides.

### What each possible outcome authorizes

- **Robust PASS-V0-I:** second independent Z/10 checkpoint earned. V0 transport or BHML/unit-structure checkpoints next.
- **Robust PASS-V0-II:** same as above with opposite map.
- **Robust FAIL:** framework's scope on Z/10 is seam-specific; foundation work to understand why.
- **Robust UNCLEAR:** rubric doesn't discriminate on V0; diagnosis required.
- **UNCLEAR by Sensitivity:** foundation work needed on attractor-privilege argument before re-running V0.

Prediction expects the last. If the prediction holds, the program gets a specific diagnostic target rather than a verdict.

---

## 12. Integrity Check Against Comparison Law

- **Test 1 — path/convention coherence:** Path 1, $h_\text{thm} = 7$. ✓
- **Test 2 — generator type commensurability:** V0 data from Rule (b). ✓
- **Test 3 — metric-object match:** four rubric sources on V0 cell features; per-branch aggregation follows frozen rule. ✓

---

## 13. Deliverables (Post-Execution, If Approved)

Written to `/home/claude/foundation_sprint/ppm_v30/`:

- `PPM_V30_V0_RESULTS.md` — 16 scores (4 sources × 2 branches × 2 maps), per-branch aggregates, robustness determination.
- `PPM_V30_V0_VERDICT.md` — one-paragraph determination per §9.
- `PPM_V30_V0_REPRO.md` — reproducibility notes.

---

## 14. Awaiting Approval

Frozen choices for review (revised):

1. V0 as v3.0 target — **approved previously**.
2. V0-specific map labels — **approved previously**.
3. Inherited threshold style (winner ≥+3, loser ≤+1, gap ≥2, applied per branch) — **approved previously**.
4. Operational interpretation (§4) — unchanged from original.
5. Sources 1, 2, 4 (§5.1) — unchanged from original.
6. **Source 3 as sensitivity branch (§5.2)** — new: S3a and S3b both scored, criteria frozen.
7. **Robustness rule (§7.2)** — new: five final outcome categories including Robust PASS / FAIL / UNCLEAR and UNCLEAR by Sensitivity.
8. Prohibited substitutions (§8) — **approved previously**, extended: no third S3 reading.

If approved: freeze as PPM-v3.0 (revised) and execute.

---

## 15. Note on Source 4

Per user direction: "if needed after the revision, flag whether Source 4 should remain scored or move to diagnostic-only, but do not change it yet unless the revised draft still looks loaded."

**My read after revision:** Source 4 is algebraically anchored on the "exactly 2 cells forming a swap-symmetric pair" predicate. This is a cardinality-plus-symmetry check decidable by inspection, not a vocabulary argument.

However: the source interprets "exactly 2 cells swap-symmetric" as **matching the pair-primitive framework's signature**. A skeptic could argue the match itself is a framework-assumption — why should the pair primitive manifest as exactly 2 cells?

**Recommendation:** leave Source 4 scored in this revision. Its score is determined by the algebraic predicate, not by vocabulary choice. Moving to diagnostic-only would reduce the aggregate range from $[-4, +4]$ to $[-3, +3]$, which would (under the predicted scoring) give fixed-source subtotal of $+2 / −2$ (S1+S2 only for fixed) — not enough for Map-V0-I to reach +3 under either S3 branch, forcing FAIL under both branches. That would produce a Robust FAIL by mechanical thresholding rather than by actual V0-structural insufficiency.

**If Source 4 looks loaded after you read the revised draft:** flag it and we redesign, potentially with one additional algebraic source to maintain aggregate range. But the recommendation is to keep it scored as-is.

Flagging the tension for transparency.
