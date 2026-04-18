# Path 3 Subtype Bridge Verdict
## P3-Subtype-v1.0 — Final Determination

---

## Verdict: **UNCLEAR**

Two of three null-separation sub-conditions fail, but for structurally different and informative reasons documented below. One of three null-separation sub-conditions passes at +3.80σ. All three primary metric thresholds pass.

---

## One-Paragraph Justification

Under the pre-registered pass criteria of P3-Subtype-v1.0 §4.1, all three primary-metric sub-conditions are met: $\mu_\Delta = 0.083$ (≤ 0.10 threshold), $\mu_\text{ADDrole} = 1.000$ (≥ 0.75 threshold, all 8 carriers match), and $\mu_\text{adj} = 0.955$ (≥ 0.80 threshold). However, two of the three required null separations fail. The $\mu_\Delta$ null separation fails degenerately because the subtype-relabeling null preserves edge counts per carrier, so real and null produce identical $\mu_\Delta$ values and the null has zero variance — the chosen null cannot discriminate on a count-only metric. The $\mu_\text{adj}$ null separation fails at $-0.87\sigma$ because on chain-topology Path 2 graphs, the constraint "one edge labeled ADD on a 6-edge chain" produces adjacency vector (0.80, 0.20, 0.00) regardless of placement, and random internal-chain placements happen to land closer to Path 1's hub-derived (0.50, 0.50, 0.00) than the real external-attachment placement does — a metric-hypothesis mismatch specific to comparing chain artifacts against a hub reference. The single null separation that passes is the decisive one: $\mu_\text{ADDrole}$ at $+3.80\sigma$ above null, corresponding to the structurally invariant property that the identity-edge rule places the ADD edge to attach vertex 1 (the ring's identity element) to the main seam component on all 8 carriers, exactly as Path 1 does. Per anti-tuning rules §5.7, no substitution is made post-hoc. The literal verdict is UNCLEAR — primary metrics met, mixed null support — with one genuinely strong structural finding (role placement transports decisively) and two informative methodological failures (null model too preservative for M1; adjacency metric mismatched to chain-vs-hub shape comparison).

---

## Substantive Reading

This verdict has three distinct components, each with its own status:

### Component A — Role placement transports (strong positive finding)

The hypothesis that ADD-subtype edges occupy a structurally invariant role within the seam — attaching the ring's identity element as an external leaf to the main seam component — holds decisively across all 8 Path 2 carriers. The null rate of random label placement producing this role pattern is only 34.75%, with real matching 100%. Separation is $+3.80\sigma$.

This is the core subtype transport claim, and it is confirmed at the level the spec committed to test.

### Component B — Count transport cannot be tested under this null (methodological)

The subtype-relabeling null was chosen to ask "is the placement of the MAX/ADD labels meaningful given the counts?" It cannot simultaneously test "do the counts themselves transport?" because the null preserves counts by construction. This is a known limitation of the null choice, now visible after execution.

The count data itself *is* consistent with transport — 7 of 8 carriers produce 83.3% MAX (close to Path 1's 75%), and Z/14's 66.7% reflects its shorter chain — but whether these counts are "more similar to Z/10's 75% than random would produce" requires a different null model, which a successor sprint could run.

### Component C — Adjacency metric fails under chain-vs-hub asymmetry (methodological)

The adjacency metric was designed to ask "does the local subtype-pair structure at each vertex match Path 1's?" Path 1's hub topology produces adjacency vector (0.5, 0.5, 0.0). Path 2's chain topology, with any ADD placement, produces an adjacency vector dominated by MAX-MAX counts simply because chains have many MAX-MAX adjacencies along the chain interior. The metric therefore measures "how close is the adjacency vector to (0.5, 0.5, 0.0)," which on chain graphs rewards internal ADD placement (two MAX-ADD adjacencies) over external ADD placement (one MAX-ADD adjacency).

Real placement is external (the correct structural match per M2). The adjacency metric penalizes this by making the adjacency vector less Path-1-like. Random placements, which include internal positions, can produce higher similarity by topology accident — not by structural match.

The metric and the hypothesis are mis-aligned given the known chain-vs-hub asymmetry from P3AP. This mis-alignment was not foreseen at spec-design time, because the hub-vs-chain implications for adjacency computation were not fully worked out before freezing. The UNCLEAR verdict reflects this, and the data preserves the real result for a successor sprint to use.

---

## What UNCLEAR Means For The Program

Per P3-Subtype-v1.0 §7:

> **UNCLEAR.** Counts/placement transport but null separation is marginal on one dimension. Report with flag, pause for judgment.

The spec's UNCLEAR case anticipated "marginal null separation." This result is an UNCLEAR by the frozen rules but with a different shape: two of three nulls fail substantively (one degenerately, one for a metric-hypothesis mismatch), while one null passes decisively. The strong finding — role placement transport — is buried inside a mixed verdict.

Under the frozen rules, no substitution. The UNCLEAR stands. But the substantive reading is: the subtype bridge finds one clean transport result and two instructive methodological issues, each of which a successor sprint can address individually.

---

## Actions Required by the Verdict

1. **Record P3-Subtype-v1.0 as UNCLEAR** in the sprint ledger, with the annotation "1 null separation decisive (ADDrole, +3.80σ); 2 null separations fail structurally (count-null degenerate; adjacency metric mis-aligned with chain topology)."

2. **Do not re-run v1.0.** Anti-tuning rules prohibit it.

3. **Do not claim a subtype-bridge PASS.** The literal verdict is UNCLEAR; that is the record.

4. **Two successor sprint directions become legitimate.** Each would require its own pre-registration:
   - **P3-Subtype-v1.1-count:** test count transport with a different null (e.g., reassign which rule generates each chain position pre-planting, then re-run the extractor). Tests whether the 83.3%/16.7% split on 7 of 8 carriers is more Path-1-like than random rule-assignment would produce.
   - **P3-Subtype-v1.1-placement:** test ADD-role placement more tightly with a stricter null or an expanded role taxonomy (e.g., "does ADD always attach the ring's identity element specifically, rather than just any low-degree external vertex?"). Tests the strong finding from v1.0 at higher resolution.

5. **Do not run hub-extension yet.** The ordering rationale from `WHY_SUBTYPE_COMES_BEFORE_HUB_EXTENSION.md` still applies: subtype is the question being answered. v1.0's UNCLEAR is itself an answer about subtype, not a sign that hub-extension should leapfrog.

6. **Update the object-type atlas and sprint selector** to reflect what was learned: subtype-relabeling null cannot test count-based metrics; adjacency metrics on asymmetric-topology bridges require careful calibration.

---

## What P3-Subtype-v1.0 Establishes Honestly

- **Strong:** ADD-edge role placement transports across paths — identity element attachment pattern is invariant on all 8 Path 2 carriers under the P3AP extension.
- **Inconclusive-but-consistent:** subtype count proportions transport observably, but the spec's null cannot test this.
- **Negative by methodology, not by structure:** adjacency similarity metric is mis-matched to chain-vs-hub asymmetry.

Combined: the subtype bridge has partial evidence of transport at the role-placement level. It does not close the subtype question affirmatively at the *full* resolution the spec attempted. It does not refute subtype transport either.

---

## Program State After P3-Subtype-v1.0

| Sprint | Path | Verdict | Summary |
|---|---|---|---|
| S28-v1.0 | 2 | FAIL | Basin smoothness |
| S29-v1.0 | 2 | FAIL | Anchored curve |
| S30-v1.0 | 2 | PASS vacuous | Empty seams |
| S30b-v1.0 | 2 | FAIL | No seam under uniform noise |
| S31p-v1.0 | cross (undeclared) | FAIL | Convention mismatch |
| S31p-v2.0 | 1 | effective PASS | Ceiling recovery |
| P3-BridgeA-v1.0 | 3 | FAIL | Object-type mismatch |
| P3-BridgeA-Prime-v1.0 | 3 | PASS | First bridge, topology-family |
| **P3-Subtype-v1.0** | **3** | **UNCLEAR** | **Role placement transport confirmed at +3.80σ; count and adjacency nulls inadequate** |

Nine sprints under discipline. Two PASSes on the record. One UNCLEAR with strong substantive content. Six informative negatives. No rescues, no post-hoc parameter tuning.

---

## Integrity Statement

The verdict is recorded honestly at UNCLEAR per the frozen rules. The substantive reading of what the data shows — one strong transport finding, two methodological issues — is also recorded in full. Neither overstates nor understates what v1.0 actually learned. The strong finding (ADD-role placement transport at +3.80σ) is preserved for a successor sprint's careful treatment. The methodological issues are documented so that v1.1's spec design starts from the real problem.
