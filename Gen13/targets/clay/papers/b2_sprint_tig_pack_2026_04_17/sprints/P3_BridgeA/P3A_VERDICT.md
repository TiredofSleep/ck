# P3A Verdict
## P3-BridgeA-v1.0 — Final Determination

---

## Verdict: **FAIL**

---

## One-Paragraph Justification

Under the pre-registered pass criteria of P3-BridgeA-v1.0 §6.1, Sprint P3A fails. Four of six sub-conditions fail: family mean component count is 3.25 against a threshold of $\leq 3.0$; family forest fraction is 0.25 against a threshold of $\geq 0.75$; and null-separation sigma on both $\mu_F$ (0.46σ) and $\mu_\rho$ (0.78σ) falls well below the 2σ requirement. Two sub-conditions pass: $\mu_d \geq 0.75$ (6 of 8 carriers have $d_\max \leq 5$) and $\mu_\rho \geq 0.75$ (7 of 8 carriers have $\rho \geq 0.60$). However, these two passing sub-conditions do not exceed what random graphs of matched edge count produce — both null means are within 1σ of observed values — so the passes are uninformative. The regenerated Path 2 seams are multi-component and non-forest at 6 of 8 carriers, with topology dominated by carrier size and noise-union density rather than by a structural pattern resembling the Path 1 theorem seam. The subtype-mix diagnostic (not part of pass/fail) further shows that Path 2 cells are overwhelmingly classified as "Other" (neither MAX-like nor ADD-like), confirming that the regenerated seams are noise artifacts rather than structured overlays. Per anti-tuning rule §7, no threshold is adjusted and no metric is substituted. The sprint returns FAIL as specified.

---

## What This FAIL Means

Per P3-BridgeA-v1.0 §9:

> **FAIL:** Topology signatures do not share measurable features beyond density. The minimal bridge between Path 1 and Path 2 at the seam-topology level is not supported. Alternative bridge objects (shell partition, corridor closure, attractor identification) remain to be tested; but seam-topology Bridge A is closed.

The mandated action: seam-topology Bridge A is closed at these parameters, on these inputs. It does not prevent:
- Bridge B (overlay-extension) from being designed as a separate Path 3 sprint.
- A different Bridge A with different Path 2 input (e.g., planted-seam recovery artifacts rather than noise-union seams) from being designed as a separate Path 3 sprint.
- Bridge tests on entirely different objects (shell partition shape, corridor closure, attractor position) from being designed.

It does close the specific hypothesis that noise-union seams from $h_\text{ext}$-canonical $C_0$ data share topology family with the Path 1 theorem seam under matched-density null.

---

## What FAIL Does NOT Mean

- Path 1's theorem is unchanged. Its seam has the claimed topology by proof, not by this sprint.
- Path 2's findings from Sprints 21, 25, 26 are unchanged. Those sprints tested different questions.
- The extractor's validity (from S31-pilot-v2.0) is unaffected. The extractor recovers planted seams perfectly; this sprint did not test extractor performance.
- No ontological or physical claim is affected either way.

---

## What the Data Structurally Tells Us

The failure has clean attribution. Path 1's seam is a *designed tree with a hub* — the theorem intentionally places overlays on 4 edges connecting 5 vertices, with one vertex (2) acting as the hub. The regenerated Path 2 seams, by contrast, are *noise-union graphs* whose edge count grows roughly as $n^2$ and whose topology is dominated by "which cells flipped mode in at least one of 20 seeds."

These are not the same kind of object:
- Path 1's seam is a small, structured artifact of a specific theorem's overlay rules.
- Path 2's regenerated seams are noise accumulations over a large vertex set.

The topology metrics measured what they were designed to measure: forest-ness, component count, low-degree profile. Those features do not survive the Path 2 regeneration process because the Path 2 process is not producing a small structured artifact — it is producing a noise-union graph that grows with carrier size.

**The inappropriate Path 2 input, not the bridge hypothesis, was the primary obstacle.** A Bridge A sprint with Path 2 input that matches Path 1's object type (small planted seam recovered under noise, not noise-union accumulation) would be testing a materially different question.

---

## Actions Required by the Verdict

1. Record P3-BridgeA-v1.0 as FAIL in the sprint ledger.
2. Close the noise-union-seam variant of Bridge A. Do not re-run with adjusted parameters.
3. A successor bridge sprint (Bridge A', Bridge B, or a different bridge object entirely) requires a new pre-registration with a fresh freeze, under a Path 3 scope declaration.
4. No movement in the local-vs-transferred split document. The split tracks Path 2 observational findings; Bridge results do not promote or demote them.
5. Update `LOCAL_CHART_VS_TRANSFERRED_GRAMMAR.md` only to add a brief note under "attempted bridges, not confirmed": "P3-BridgeA-v1.0 — noise-union seam topology vs theorem seam topology — FAIL."

---

## No Interpretation Beyond the Frozen Claim

The frozen claim tested: *do regenerated Path 2 noise-union seams on 8 specified carriers share topology features (forest-ness, low $d_\max$, low-degree profile, small component count) with the Path 1 theorem seam on Z/10, at a 2σ threshold against matched-density random graphs?*

The answer: **No.**

Sprint P3A tested one narrow bridge claim; it returned FAIL; the record stands. No rescue, no reinterpretation, no scope drift.

The Path 3 category itself remains valid. The scope discipline worked as intended: the bridge question was asked cleanly, and the answer came back cleanly. A FAIL at the first Path 3 sprint is neither surprising nor evidence against the Path 3 category — it is evidence that *this specific bridge, with this specific input, does not hold*. Future Path 3 sprints can test different bridges on different objects without inheriting this result's scope.

---

## Summary of Sprint Ledger After P3A

| Sprint | Path | Verdict |
|---|---|---|
| S28-v1.0 | Path 2 | FAIL (basin smoothness) |
| S29-v1.0 | Path 2 | FAIL (anchored curve) |
| S30-v1.0 | Path 2 | PASS (vacuous) |
| S30b-v1.0 | Path 2 | FAIL (no persistent seam) |
| S31-pilot-v1.0 | cross-path (undeclared) | FAIL (convention mismatch) |
| S31-pilot-v2.0 | Path 1 | effective PASS (ceiling recovery) |
| **P3-BridgeA-v1.0** | **Path 3** | **FAIL (topology signatures do not share beyond density)** |

Seven sprints under pre-registration discipline. One effective PASS (extractor validation on theorem object). Six informative negatives. Each failure has clean attribution.
