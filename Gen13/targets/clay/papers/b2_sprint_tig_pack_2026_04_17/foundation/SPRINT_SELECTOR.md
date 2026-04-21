# Sprint Selector
## What Kind of Sprint Is Legitimate for Each Object Type

---

## Purpose

For each object type in `OBJECT_TYPE_ATLAS.md`, this document specifies: what sprints can be run on it, what metrics belong to those sprints, what nulls are legitimate, and what claims are allowed. Intended as a design-time lookup before freezing any new spec.

If a proposed sprint does not match any entry in this document, it requires either a new entry or a re-examination of the sprint's design.

---

## Sprint Template Categories

Four categories of sprint exist under the current program structure:

- **R (Recovery):** does the extractor find a known planted object under noise?
- **O (Observation):** does an invariant hold across a family under pre-registered metrics?
- **T (Transport):** does a property of one object reappear in another object of the same path?
- **B (Bridge):** does a relational claim hold between objects in different paths?

These categories are not mutually exclusive — a Bridge sprint contains a Transport-like comparison wrapped in a bridging rule. But they give enough structure to select appropriate metrics and nulls per object.

---

## Selector By Object Type

### 1. Published TSML theorem operator (Path 1, theorem)

**Sprint categories allowed:** R only.

**Metrics:** Jaccard, recall, precision, type agreement on planted overlays.

**Nulls:** not required for recovery on a known construction; use NONE-control against spurious detection.

**Allowed claims:** "extractor correctly recovers $S_\text{planted}$ under these noise conditions."

**Forbidden claims:** any claim about transport, bridges, or non-Z/10 carriers.

**Reference sprint:** S31-pilot-v2.0.

---

### 2. Canonical $C_0$ under $h_\text{thm}=7$ (Path 1, theorem)

**Sprint categories allowed:** R (as ground truth for recovery).

**Metrics:** equality to published TSML on non-overlay cells (should be 92/100 by construction).

**Nulls:** none — deterministic construction.

**Allowed claims:** "canonical reconstruction matches theorem."

**Forbidden claims:** anything about other carriers or other conventions.

---

### 3. Canonical $C_0$ under $h_\text{ext}$ (Path 2, observed)

**Sprint categories allowed:** O, T.

**Metrics:** corridor closure across carriers; shell-partition recovery on the output histogram; basin-ratio distribution (with the caveat that basin-ratio *as a transport variable* has been closed by S28/S29).

**Nulls:** category-preserving scrambles (e.g., random unit-valued attractor, random permutation-of-shell-labels).

**Allowed claims:** "property $X$ holds under $h_\text{ext}$-canonical $C_0$ across the tested carrier family" (observation-level within Path 2).

**Forbidden claims:** theorem-level statements about $C_0$ under $h_\text{ext}$; physics claims; direct claims about Path 1 objects.

**Reference sprints:** Sprint 25 (corridor closure), Sprint 26 (shell shape).

---

### 4. Path 1 planted theorem seam (Path 1, designed artifact)

**Sprint categories allowed:** R.

**Metrics:** recovery metrics against the known cells: Jaccard, recall, precision, type agreement.

**Nulls:** NONE control (empty generator) to confirm absence of spurious detection.

**Allowed claims:** "the published seam is recoverable by the extractor under specified noise."

**Forbidden claims:** transport; bridges to noise-union Path 2 objects without explicit bridging spec; category-level claims.

**Reference sprint:** S31-pilot-v2.0.

---

### 5. Path 2 prior-free discovered seam (historical artifact) / regenerated union seam (Path 2, noise-residue)

**Sprint categories allowed:** O — but with a tightly scoped question. The noise-residue nature of the union seam means many metrics normally applied to designed artifacts (tree-ness, specific hub topology) are not semantically meaningful.

**Appropriate metrics:** cell set cardinality; dependence of cardinality on $N$ and $p$; cell set coverage relative to ring structure (fraction of cells in V0, in core, etc.); rate of convergence to stable union as $K \to \infty$.

**Inappropriate metrics:** detailed topology (tree-ness, max degree, branch profile) at large carriers where the union grows beyond a threshold.

**Nulls:** random cell sets of matching cardinality on the same carrier.

**Allowed claims:** "union seam has cardinality / coverage property $X$ under specified noise regime on tested carriers."

**Forbidden claims:** that the union seam has a specific "structure" in the designed-artifact sense; that it transports to or resembles Path 1 objects at the topology level (this was P3-BridgeA's FAIL).

**Reference sprint:** P3-BridgeA (as a cautionary failure).

---

### 6. Path 2 persistent seam under low-$N$ + persistence filter (Path 2, noise-residue filtered)

**Sprint categories allowed:** R (when planting is applied, as in S31-pilot-v2.0 extended to other carriers); O (when the question is detectability on the bare canonical).

**Metrics:** for R, recovery metrics against planted ground truth. For O, $\mu_\text{non-empty}$, $\mu_J$ (cross-seed Jaccard), $\mu_\text{canonical-tie}$.

**Nulls:** for R, NONE control. For O, scrambles that preserve category (e.g., unit-valued random attractor).

**Allowed claims for R:** "extractor recovers planted seam on this carrier under specified noise."

**Allowed claims for O:** "bare canonical $C_0$ under uniform noise has / does not have detectable seam-prone cells at these parameters."

**Forbidden claims:** that the persistent seam is a structural invariant of the canonical object independent of sampling; that cross-carrier persistent seams should topologically resemble the theorem seam (object-type mismatch).

**Reference sprints:** S30b (O, detectability FAIL on bare $C_0$), S31-pilot-v2.0 (R, ceiling recovery on Z/10 with planting).

---

### 7. Basin ratio $\beta(R_n)$ (Path 2, observed scalar)

**Sprint categories allowed:** O (distributional questions); T is closed.

**Appropriate metrics:** distribution of $\beta$ across carriers; moments of that distribution; correlation with carrier-structural features (prime factorization, $|U|$, etc.) at the *distributional* level, not at the *curve* level.

**Inappropriate metrics:** point-wise smoothness across carrier index; monotone trend with depth coordinate. Both were closed by S28/S29.

**Nulls:** category-preserving scrambles of shell partition or attractor.

**Allowed claims:** "distribution of $\beta$ across the compatibility family has property $X$" (distributional observation).

**Forbidden claims:** that $\beta$ is a transport variable; that it organizes into a curve under any tested coordinate.

**Reference sprints:** S28 (FAIL), S29 (FAIL). Future $\beta$ sprints should operate at the distributional level only.

---

### 8. Corridor closure (Path 2, transported observation)

**Sprint categories allowed:** O, T.

**Metrics:** closure under direct enumeration (is the corridor's rule set $\{MAX, MIN\}$ or $\{MAX, MIN, ADD\}$ or something else); tightness of closure (any rules almost in the closure).

**Nulls:** random rule-sets on the corridor; rule-sets with a single canonical backbone.

**Allowed claims:** "pure $C_0$ under $h_\text{ext}$ has corridor closure $\{MAX, MIN\}$ on tested carriers $X$" (observation-level, Path 2).

**Forbidden claims:** that the closure corresponds to any specific Path 1 object (would require bridge); that the closure is a theorem rather than an observation (Path 2 results are not theorems until explicitly promoted).

**Reference sprint:** Sprint 25.

---

### 9. Shell partition shape (Path 2, asymptotic observation)

**Sprint categories allowed:** O, T.

**Metrics:** ARI between extracted partition and canonical; scaling of ARI with $n$; per-carrier stability under seed variation.

**Nulls:** random partitions of units into two classes of matching sizes.

**Allowed claims:** "shell partition shape is recoverable from output histograms with ARI $\to 1$ as $n \to \infty$ on tested carriers."

**Forbidden claims:** that shell labeling (which specific units go in which shell) is recoverable without dynamics; that partition shape transports to Path 1 theorem objects (would require bridge).

**Reference sprint:** Sprint 26.

---

### 10. Attractor position $h_\text{ext}(R_n)$ (Path 2, observed)

**Sprint categories allowed:** O.

**Metrics:** concordance of extracted attractor with structural rule (max odd unit); stability across seeds.

**Nulls:** random element of ring; random unit; random odd unit (tests whether "max" adds signal over "odd unit").

**Allowed claims:** "prior-free extraction identifies max odd unit as attractor with concordance rate $X$ on tested carriers."

**Forbidden claims:** that $h_\text{ext}$ equals $h_\text{thm}$ (it does not on Z/10, as `ATTRACTOR_RECONCILIATION.md` establishes); that attractor transports in a stronger sense than its identification rule.

---

### 11. Path 3 bridge topology comparison object (Path 3, bridge)

**Sprint categories allowed:** B.

**Mandatory structure:** the bridge must specify exactly two paths being bridged, the bridging rule, the commensurability transform, and the claim permitted under PASS.

**Appropriate metrics:** topology invariants (component count, forest-ness, degree profile) on small designed artifacts; subtype-mix on properly-classified seams; structural pattern matching via pre-specified templates.

**Nulls:** preserve one aspect (vertex set, edge count, degree sequence) and scramble another.

**Allowed claims under PASS:** "these two specific objects, under the specified bridging rule, share structural feature $X$ at significance $\sigma$."

**Forbidden claims:** transport in the cross-path sense; equivalence of objects; that one path "contains" or "completes" the other; that PASS constitutes a theorem.

**Reference sprint:** P3-BridgeA (FAIL; cautionary example of object-type mismatch within a bridge).

---

## Metric-Object Compatibility Matrix

A quick lookup: which metric types are semantically meaningful for which object types.

| Metric type → / ↓ Object type | Scalar summary | Cell set cardinality | Cell set coverage | Graph topology | Partition similarity | Recovery |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Theorem operator | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Theorem-designed seam | ✓ | ✓ | ✓ | ✓ | — | ✓ |
| Small recovered seam | ✓ | ✓ | ✓ | ✓ | — | ✓ |
| Noise-residue per-seed | ✓ | ✓ | ✓ | ⚠ (unstable) | — | — |
| Noise-residue union (large $n$) | ✓ | ✓ | ✓ | ✗ | — | — |
| Noise-residue persistence-filtered | ✓ | ✓ | ✓ | ⚠ (small samples) | — | ✓ (if planted) |
| Scalar $\beta(R_n)$ | ✓ | — | — | — | — | — |
| Shell partition | — | — | — | — | ✓ | ✓ |
| Closure/rule set | — | ✓ | — | — | — | ✓ |

Key: ✓ meaningful; ⚠ meaningful with caveats; ✗ not meaningful (object does not support the metric); — not applicable.

The matrix captures why P3-BridgeA was in trouble: "Graph topology" applied to "noise-residue union (large $n$)" has ✗, not ✓. The sprint was asking a question the object cannot answer.

---

## Sprint-Design Workflow

Before freezing any new spec:

1. Identify the object type(s) involved. Locate in atlas.
2. Look up allowed sprint categories for each object type.
3. Look up appropriate metrics.
4. Look up appropriate nulls.
5. Verify metric-object compatibility via the matrix.
6. If cross-path: run the three Comparison Law tests.
7. Write spec with scope declaration per scope tag template.
8. Freeze.

Any spec that cannot be matched cleanly to an entry in this document is either (a) proposing a new kind of sprint, which requires adding an entry here, or (b) structurally problematic, which requires redesign.

---

## Maintenance

This document is updated when:

- A new object type enters the atlas.
- A new sprint category is proven useful (a fifth category beyond R/O/T/B might emerge).
- A metric is shown to be meaningful or unmeaningful on an object type via accumulated evidence.

Updates are explicit; prior sprints are not retroactively reclassified.
