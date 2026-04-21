# Path 3 Subtype Adjacency v1.2 — Verdict
## P3-Subtype-v1.2-adj — Final Determination

---

## Verdict: **PASS**

---

## One-Paragraph Justification

Under the pre-registered pass criteria of P3-Subtype-v1.2-adj §5.1, both scored sub-conditions are met. The sole scored metric $\mu_L$ equals 1.0000 — all 8 Path 2 carriers in the tested family (Z/14, Z/22, Z/34, Z/42, Z/46, Z/58, Z/74, Z/94) produce recovered ADD edges whose endpoint-degree pair is (1, 2), meaning the ADD edge has at least one degree-1 endpoint (vertex 1) and is therefore a leaf edge of the recovered seam graph. This exceeds the $\geq 0.75$ threshold. Under subtype-label scrambling on the same recovered seam graphs with counts preserved (null seed 33400, 100 replicates), random ADD-label placement produces the leaf-edge attribute at mean rate 0.3588 with standard deviation 0.1720 — close to the theoretical expectation of $2/|E|$ averaged across carriers ($\approx 0.375$). Real $\mu_L$ exceeds null mean by +3.73σ, decisively exceeding the 2σ threshold; the real value of 1.0 lies outside the entire observed null range (max 0.875 across 100 replicates). Both sub-conditions pass unambiguously. The $M$ diagnostic (+2.13σ) is reported but does not contribute to scoring because it is structurally guaranteed on chain topology whenever $L$ holds; the $I$ signal (+6.25σ) is inherited from v1.1 and is not re-scored. Per anti-tuning rule §6, no substitution is made post-hoc. The verdict is PASS as specified.

---

## What This PASS Establishes

The strongest sentence this sprint supports:

> On the Path 2 carrier family {14, 22, 34, 42, 46, 58, 74, 94}, under the P3AP overlay-extension algorithm, recovered ADD-subtype edges are consistently leaf edges of the recovered seam graph (at least one degree-1 endpoint) at +3.73σ above a subtype-label-scrambling null on the same graphs.

This is a new finding, distinct from v1.1's identity-element result. v1.1 established that *given the ADD edge has a degree-1 endpoint, that endpoint is the identity*. v1.2-adj establishes the underlying structural attribute: *the ADD edge has a degree-1 endpoint at all*. That attribute does not follow automatically from $I$; under the null, it fails roughly 64% of the time while $I$ fails 81% of the time. They are related but independently testable.

The transport claim now has two confirmed components at the role-attribute level:

- **Leaf-edge placement** (v1.2-adj, +3.73σ): the ADD edge occupies a boundary position in the seam graph, not an interior position.
- **Identity-element attachment** (v1.1, +6.06σ): the boundary endpoint is specifically the ring's multiplicative identity.

Together, these support a compound claim *via retrospective synthesis*: the ADD edge is consistently placed as a leaf edge whose leaf endpoint is the identity element. But v1.2-adj alone earns only the first clause; the second is v1.1's inheritance.

---

## What This PASS Does NOT Establish

1. **Count-proportion transport remains closed.** The P3AP generator family structurally fixes $n_\text{ADD} = 1$ per carrier, so count transport is not a live question under this generator. Documented in `WHY_COUNT_IS_NOT_LIVE_UNDER_P3AP.md`.

2. **Main-component attachment is not a scored finding.** $M$ was excluded from scoring due to structural redundancy on chain topology. The +2.13σ diagnostic separation is real but happens because the null mean for $M$ (0.68) reflects the high rate at which random label placement lands on a main-component-adjacent edge on these graphs — not because $M$ captures a new structural hypothesis.

3. **Raw adjacency ratios (v1.0 M3-style) are not tested.** That metric was shape-entangled and abandoned.

4. **Hub-and-spokes transport remains open.** Path 2 carriers under the P3AP extension produce chain topology; a different extension algorithm producing hub topology would be a separate object class.

5. **The causal explanation is not established.** Leaf-edge placement transports because the P3AP extension's identity-edge rule plants the ADD cell at $(1, 2)$, which on chain-topology seam graphs places it at a chain endpoint. Whether this reflects a deeper ring-structural invariant or is an artifact of the specific extension rule remains untested.

6. **No theorem-level claim is produced.** The Path 1 theorem remains proven only on Z/10. No extension to non-Z/10 carriers is made.

7. **No physical, ontological, or real-world claim.**

---

## Relationship to v1.1

v1.1's PASS is preserved unchanged. v1.2-adj does not affect v1.1's verdict, does not re-score v1.1's metric, and does not bundle its own scored metric with v1.1's.

The relationship is additive:
- v1.1 verdict: identity-element attachment transports (+6.06σ).
- v1.2-adj verdict: leaf-edge placement transports (+3.73σ).

Each sprint's verdict stands alone. A compound claim combining both requires an explicit synthesis step, not a single-sprint execution.

The v1.2-adj run incidentally re-confirmed v1.1's $I$ signal at +6.25σ on a different seed (33400 vs v1.1's 33300). The consistency of the two estimates (+6.06σ and +6.25σ) is a reproducibility check on the null-sampling methodology, not a promotion of v1.1's result.

---

## What Is Authorized Next

1. **Record P3-Subtype-v1.2-adj as PASS** in the sprint ledger.
2. **Update the object-type atlas** with a new confirmed transportable feature: "leaf-edge placement of ADD edge under P3AP extension."
3. **Update the local-vs-transferred split document** to reflect both v1.1 and v1.2-adj findings as Path 3 bridge-level confirmed features.

### Legitimate successor sprints (not authorized yet; each requires its own pre-reg)

- **Identity-element attachment under alternative extension rules.** Tests whether v1.1's finding is specific to P3AP or generalizes.
- **Leaf-edge placement under alternative extension rules.** Tests whether v1.2-adj's finding is specific to P3AP.
- **Path 3 bridge on a different object entirely.** Shell partition shape, corridor closure, attractor identification.
- **Path 2 observation sprints.** Corridor closure extension to more carriers under pure observation scope, without bridging.

### Explicitly deferred

- **Hub-extension.** Requires a new overlay-extension algorithm and a new scope declaration. Still deferred.
- **Count transport.** Closed under P3AP generator. Requires a new generator family to revisit.
- **Raw adjacency ratios.** Abandoned as shape-entangled.

---

## Program State After v1.2-adj

| Sprint | Path | Verdict | Key result |
|---|---|---|---|
| S28-v1.0 | 2 | FAIL | Basin smoothness (null inverted) |
| S29-v1.0 | 2 | FAIL | Anchored curve |
| S30-v1.0 | 2 | PASS (vacuous) | Empty seams |
| S30b-v1.0 | 2 | FAIL | No seam under uniform noise |
| S31p-v1.0 | cross (undeclared) | FAIL | Convention mismatch |
| S31p-v2.0 | 1 | effective PASS | Ceiling recovery on theorem |
| P3-BridgeA-v1.0 | 3 | FAIL | Object-type mismatch |
| P3-BridgeA-Prime-v1.0 | 3 | PASS | Topology-family (+12.56σ on $\mu_k$) |
| P3-Subtype-v1.0 | 3 | UNCLEAR | ADD role at +3.80σ; count/adj nulls inadequate |
| P3-Subtype-v1.1 | 3 | PASS | Identity-element attachment (+6.06σ) |
| **P3-Subtype-v1.2-adj** | **3** | **PASS** | **Leaf-edge placement (+3.73σ)** |

Eleven sprints under discipline. **Four PASSes now on the record** (one effective on Path 1, three substantive on Path 3). One UNCLEAR with documented residual content. Six informative negatives.

The Path 3 bridge now has three independently confirmed features:
- Topology-family resemblance (P3AP): forest + single component + low-degree profile.
- Algebraic-role resemblance (v1.1): ADD edge anchors the ring's identity element.
- Structural-position resemblance (v1.2-adj): ADD edge is a leaf edge, not an interior edge.

Each of these is a separate narrow finding. Each was confirmed under a separate pre-registered metric and null model. No result depends on any other for its validity.

---

## Integrity Statement

The PASS is recorded honestly with full scope boundaries. $L$ at +3.73σ is a real discriminating finding: null mean (0.359) matches theoretical expectation (0.375), null distribution has meaningful variance (std 0.172, range 0.0 to 0.875), and real (1.0) is outside the entire observed null range. The diagnostic $M$ signal is reported transparently but explicitly not scored. The inherited $I$ signal is reported alongside with explicit inheritance labeling. No double-counting of prior evidence. No ceiling-artifact issues. No post-hoc substitution.

The narrow question the spec committed to test has been answered cleanly: leaf-edge placement transports at pre-registered significance under the P3AP extension on the tested Path 2 family.
