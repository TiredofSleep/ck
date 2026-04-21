# Current State Summary
## TIG/TSML Sprint Archive — Snapshot

---

## 1. What Is Exact

**Z/10 TSML 3-Layer Tower Theorem** — proven on $R = \mathbb{Z}/10\mathbb{Z}$ with $h_\text{thm} = 7$.

- Canonical construction $C_0$ reconstructs 92/100 entries of the published Z/10 TSML.
- The 8-entry seam residue decomposes as 6 MAX cells + 2 ADD cells:
  - MAX cells: $\{(2,4), (4,2), (4,8), (8,4), (2,9), (9,2)\}$.
  - ADD cells: $\{(1,2), (2,1)\}$.
- Combined with $C_0$ via the tower operator, these reproduce the published TSML bit-exactly.

Reference: `theorem_local_chart/THEOREM_SPINE.md`, `theorem_local_chart/CANONICAL_TSML_CONSTRUCTION.md`.

Scope: Path 1 (Local Theorem).

---

## 2. What Is Operationally Validated

**Low-$N$ mode extractor with persistence filter.**

- Validated at ceiling on the Z/10 theorem object in S31-pilot-v2.0 under $h_\text{thm} = 7$.
- Parameters: $N = 10n^2$ samples per seed, $K = 10$ seeds, $\pi = 0.50$ persistence threshold, tie-break on smallest $z$.
- Performance: Jaccard = recall = precision = type-agreement = 1.000 on every condition at noise levels $p \in \{0.02, 0.10, 0.20\}$.
- Verdict: effective PASS (literal UNCLEAR due to one-sided rule not applied to ceiling recovery; documented as spec-rule artifact).

Reference: `sprints/S31_pilot_v2.0_local_theorem/`.

Scope: Path 1 (Local Theorem).

---

## 3. What Is Bridge-Confirmed

Three independent Path 3 bridge-level findings, each under its own pre-registered metric and null.

### 3a. Topology-family resemblance (P3-BridgeA-Prime-v1.0)

> Under the P3AP overlay-extension algorithm, planted-recovery artifacts on $\{14, 22, 34, 42, 46, 58, 74, 94\}$ share topology-family features (forest-ness, single connected component, low max degree, low-degree-vertex dominance) with the Z/10 theorem seam's planted-recovery artifact, at $+12.56\sigma$ above matched-density random-graph baseline on mean component count.

Reference: `sprints/P3_BridgeA_Prime/`.

### 3b. Identity-element attachment (P3-Subtype-v1.1)

> On the Path 2 carrier family under the P3AP overlay-extension, recovered ADD-subtype edges attach the ring's multiplicative identity element (vertex 1) at $+6.06\sigma$ above a subtype-label-scrambling null on the same recovered seam graphs.

Reference: `sprints/P3_Subtype_v1.1_identity_edge/`.

### 3c. Leaf-edge placement (P3-Subtype-v1.2-adj)

> On the Path 2 carrier family under the P3AP overlay-extension, recovered ADD-subtype edges are consistently leaf edges of the recovered seam graph (at least one degree-1 endpoint) at $+3.73\sigma$ above a subtype-label-scrambling null on the same recovered seam graphs.

Reference: `sprints/P3_Subtype_v1.2_adj_leaf_edge/`.

Each of these three findings stands alone. No composite claim is produced by combining them. Scope on all three: Path 3 (Bridge Test).

---

## 4. What Lanes Are Closed

Lane closures are attributed to specific verdicts; they do not represent negative theorems.

### 4a. Basin-ratio smoothness transport
Closed by S28-v1.0 (FAIL, null inverted at 3.35σ wrong direction).

### 4b. Basin-ratio anchored curve transport
Closed by S29-v1.0 (FAIL, Kendall τ = 0.063 below threshold 0.35; R² = 0.00005 below 0.40).

### 4c. Noise-only persistent seam on pure $C_0$
Closed by S30b-v1.0 (FAIL, no persistent seam under uniform noise at tested parameters).

### 4d. Noise-union seam topology bridge
Closed by P3-BridgeA-v1.0 (FAIL, object-type mismatch between designed theorem artifact and noise-union accumulation).

### 4e. Raw adjacency ratio bridge (v1.0-style)
Closed by P3-Subtype-v1.0 UNCLEAR verdict — adjacency-ratio metric is shape-entangled under chain-vs-hub asymmetry. Replaced by role-based metrics in v1.1 and v1.2-adj.

### 4f. Count transport under P3AP generator family
Closed by generator-structural argument — $n_\text{ADD}$ is structurally fixed at 1 per carrier after audit, so within-family nulls are degenerate on count. Reference: `open_questions/COUNT_TRANSPORT_CLOSED_UNDER_P3AP.md`. Future generator families may revisit this question.

---

## 5. What Remains Open

Open questions are documented but not authorized for sprinting. Each would require its own pre-registration under the scope-tag discipline.

### 5a. Hub-extension overlay rules
An alternative overlay-extension algorithm that produces hub-and-spokes structure on Path 2 carriers (rather than chains) has not been designed or tested. Reference: `open_questions/HUB_EXTENSION_DEFERRED.md`. All current Path 3 bridge findings are conditional on the P3AP extension specifically.

### 5b. Identity-element attachment under alternative extensions
v1.1's $+6.06\sigma$ finding is specific to the P3AP extension. Whether the identity-element anchoring transports under a different overlay-generation rule is untested.

### 5c. Leaf-edge placement under alternative extensions
v1.2-adj's $+3.73\sigma$ finding is similarly specific to the P3AP extension.

### 5d. Subtype transport for carrier-families outside the tested set
All Path 3 results are on the 8-carrier family $\{14, 22, 34, 42, 46, 58, 74, 94\}$. Extension to additional carriers within the compatibility family is untested.

### 5e. Count transport under richer generator families
Closed under P3AP; would be re-opened by defining a parameterized extension family where $n_\text{ADD}$ is stochastic.

### 5f. Corridor closure extension (Path 2 observation, not bridge)
Sprint 25's observation of $\{\text{MAX}, \text{MIN}\}$ corridor closure on 23 carriers has not been extended to additional carriers in the compatibility family. Pure Path 2 observation sprint; would not cross into Path 3 bridge territory.

### 5g. Shell-partition shape recovery extension
Sprint 26's observation of asymptotic ARI → 1 on 12/32 carriers (at the time) has not been updated with newer data or extended to the 35-member family.

---

## Summary Counts

- **Proven (Path 1):** 1 theorem (Z/10 TSML).
- **Validated (Path 1 tool):** 1 extractor architecture.
- **Bridge-confirmed (Path 3):** 3 independent narrow findings.
- **Closed lanes:** 6 specific closures with attribution.
- **Open questions:** 7 noted, none authorized for sprinting without new pre-reg.

- **Total sprints on record:** 11.
- **PASSes:** 4 (one effective, three substantive).
- **UNCLEAR:** 1 (P3-Subtype-v1.0, with documented residual).
- **FAILs:** 6 (informative, each with specific cause).
- **Vacuous PASSes:** 1 (S30 — empty seams under tested noise-immunity).

---

## Scope Boundaries

This summary respects the program's scope discipline. Nothing here is upgraded to theorem status beyond Z/10 TSML. Nothing is promoted across paths. No physical, ontological, or real-world claims. The three bridge findings earn their specific sentences only — no composite, no generalization, no extrapolation.

Changes to this summary require user approval per `PACKING_RULES.md` §17.
