# Why A-Prime Is Now Valid
## The Object-Type Match That P3-BridgeA Lacked

---

## The Asymmetry That Made P3-BridgeA FAIL

P3-BridgeA compared two objects that shared a name ("seam") but differed in almost every structural property.

| Property | Path 1 input (P3-BridgeA) | Path 2 input (P3-BridgeA) |
|---|---|---|
| Generator | Theorem's overlay specification | Union of single-seed disagreements over 20 noisy runs |
| Epistemic class | Designed artifact | Noise-residue accumulation |
| Size | Fixed (8 ordered cells, 4 edges) | Growing with $n^2$ (from 3 edges at $n=14$ to 144 edges at $n=94$) |
| Topology | Tree, one hub, three leaves | Multi-component forest at small $n$, non-forest with growing cycles at large $n$ |
| Role of the attractor | Central (hub at vertex 2, attractor-adjacent) | Noise-averaged; no structural hub persists |
| Scales with carrier? | No | Yes, approximately $n^2$ |

The topology metrics — forest-ness, component count, max degree, low-degree profile — were calibrated to the fixed-size designed artifact. Applied to the growing noise-residue object, they measured something that was not there by construction: a growing union cannot stay forest-like forever, and at large carriers forest-ness becomes structurally impossible regardless of what signal the data might carry.

`OBJECT_TYPE_ATLAS.md` now names these as different object types. The `SPRINT_SELECTOR.md` compatibility matrix marks "graph topology on noise-residue union at large $n$" as ✗, not ✓. The P3-BridgeA verdict attributed this to "inappropriate Path 2 input" at the time; the atlas makes the attribution formal.

---

## The Symmetry That Makes A-Prime Valid

Bridge A-Prime compares two objects of the **same type** as the Path 1 reference:

| Property | Path 1 input (A-Prime) | Path 2 input (A-Prime) |
|---|---|---|
| Generator | $(C_0 + S_\text{planted})$ under noise, recovered by extractor with persistence filter | $(C_0 + S_\text{planted-extended})$ under noise, recovered by extractor with persistence filter |
| Epistemic class | Recovered planted artifact | Recovered planted artifact |
| Size | 8 ordered cells (the theorem's published seam) | 6 to 10 ordered cells per carrier (the extended planted overlay) |
| Topology | Small designed artifact | Small designed artifact |
| Role of the attractor | Central | Central |
| Scales with carrier? | No | No (planted overlay is constant-size by the extension algorithm) |

Both objects are produced by the *same extractor* from *same-noise* generation of a *planted overlay*. The extractor has already been validated on Path 1 (S31-pilot-v2.0 achieved ceiling recovery). Both objects are small designed artifacts recovered under noise. Topology metrics on one are semantically commensurable with topology metrics on the other.

This is the object-type match the atlas and selector were built to enable.

---

## What Changed, Concretely

Three things changed between P3-BridgeA and A-Prime.

**First, the Path 2 generator changed.** In P3-BridgeA the Path 2 seam was extracted from noised-$C_0$ data *without any planted overlay*. The resulting seam is whatever noise-driven disagreement emerges. In A-Prime the Path 2 generator is $C_0 + S_\text{planted-extended}$ — meaning the Path 2 data contains an explicitly planted overlay in addition to noise. The extractor now has a designed artifact to find, rather than having only noise-driven flips to report.

**Second, the extractor workflow changed.** In P3-BridgeA the Path 2 workflow was "union across seeds of per-seed disagreement cells." In A-Prime the workflow is "persistence filter ($\pi = 0.50$) across seeds," matching S31-pilot-v2.0 on Z/10. Persistence filtering produces a seam that closely matches planted ground truth under moderate noise (as validated on Z/10) rather than accumulating random seed-level flips.

**Third, the overlay extension rule is now explicit.** P3-BridgeA used only the prior-free empirical seam. A-Prime defines a specific algorithmic extension of the theorem's overlay — the doubling-chain rule for MAX and the identity-edge rule for ADD, applied to each Path 2 carrier. This is a heuristic extension (not a theorem), declared as such, and the bridge question is whether the extractor recovers it consistently. The heuristic nature is explicit and bounded: we test whether it produces recoverable artifacts with topology similar to the theorem's, not whether the heuristic is itself proven.

---

## The Honest Scope of A-Prime

Bridge A-Prime, like every bridge sprint, produces bridge-level claims only. A PASS earns the sentence:

> Under the specified overlay-extension algorithm, planted-recovery artifacts on Z/14, Z/22, Z/34, ... share topology features (forest-ness, low max degree, hub-and-spokes profile) with the Z/10 theorem seam's planted-recovery artifact at ≥ 2σ above matched-density random graphs.

Four things remain outside the claim even under a strong PASS:

- **That the overlay-extension algorithm is the "correct" extension.** We chose one rule (doubling-chain + identity-edge + attractor-involution) algorithmically. Other rules could be tested separately.
- **That the extended overlays correspond to any "natural" object on non-Z/10 carriers.** They are heuristic constructions recovered by a validated extractor. The recovery proves the tool works; it does not prove the overlays are the "real" seams on those rings.
- **Transport in the stronger theorem sense.** A-Prime is still Path 3 relational. No Path 1 theorem is being extended to non-Z/10.
- **Cell-identity or rule-subtype correspondence across carriers.** Topology-level comparison only.

A FAIL would say that even under matching object types, recovered planted artifacts across the Path 2 family do not share the Z/10 theorem seam's topology signature beyond density. That is a narrower negative than P3-BridgeA's (which failed partly due to object mismatch); it would suggest the overlay extension algorithm itself produces structurally different artifacts per carrier, or that the specific topology metrics chosen do not capture what is similar about the extended artifacts.

---

## Why This Is The Right Next Sprint

Two alternatives exist for the next sprint slot: Bridge A-Prime (this one) and a corridor-closure extension within Path 2 (conservative).

Bridge A-Prime is chosen because:

1. **The atlas makes it newly possible.** Before the atlas, a clean cross-path topology bridge was blocked by object-type mismatch. Now the objects can be matched cleanly.
2. **The extractor is validated.** S31-pilot-v2.0 confirmed that the low-$N$ + persistence extractor recovers planted artifacts at ceiling quality on Z/10. A-Prime is the natural next question given that validation.
3. **The comparison law permits it.** Both objects are Path 1/2 recovered-planted artifacts. Under the law, Test 1 requires a bridge (different paths); Test 2 passes (same generator type — planted recovery); Test 3 passes (topology metrics are meaningful for both small designed artifacts).
4. **It answers a question the program has actually been circling.** Do the theorem's structural features (seam as small tree with attractor hub) persist under algorithmic extension? That is the core "does the grammar transfer" question, asked at one specific level.

The conservative alternative — extending Sprint 25's corridor closure to additional carriers within Path 2 — is also legitimate and would likely produce a positive result. But it would not answer the bridge question. It would extend an already-established Path 2 observation. That is valuable but lateral; A-Prime is forward.

---

## What Happens Depending on Outcome

**PASS.** Bridge A-Prime is the first confirmed Path 3 bridge. The program gains a narrow relational claim: recovered planted artifacts share topology family across Path 1 and the Path 2 family under the specified extension algorithm. A subsequent sprint can test subtype mix (is the MAX/ADD partition preserved?), or extension to different overlay rules, or bridge to Path 3 objects of other kinds.

**FAIL.** The overlay-extension algorithm does not produce recoverable artifacts with Path-1-like topology. This is a narrow negative: either the specific extension rule is wrong for bridging, or the extraction loses topology fidelity on non-Z/10 carriers. A subsequent sprint would try a different extension rule (e.g., shell-native rather than doubling-chain) under a new Path 3 spec.

**UNCLEAR.** Topology metrics pass weakly but null separation is marginal. Report and pause for judgment, as with prior sprints.

Any outcome is informative. The sprint is narrow enough that the result will attribute cleanly.
