# What v1.1 Proved, and What Count Transport Would Add
## Short Note

---

## What v1.1 Proved

P3-Subtype-v1.1 returned PASS at $+6.06\sigma$ on one narrow, algebraically-meaningful question:

> Under the P3AP overlay-extension algorithm, recovered ADD-subtype edges on the tested Path 2 family attach the ring's multiplicative identity element (vertex 1) at a rate significantly exceeding a subtype-label-scrambling null on the same recovered seam graphs.

Concretely: all 8 Path 2 carriers produce recovered ADD edge = (1, 2). Random label placement achieves this identity-touching pattern only ~19.6% of the time across 100 replicates. Real 100%; null ~20%; separation +6σ.

The claim v1.1 supports is about the *role* ADD edges play: they are anchored to a specific algebraic object (the ring's identity element). Not to "some low-degree vertex," and not to a carrier-specific graph-theoretic position. To the identity element.

---

## What v1.1 Did Not Prove

**Count transport remains untested.**

v1.0 observed that 7 of 8 Path 2 carriers have 83.3% MAX / 16.7% ADD, and Z/14 has 66.7% MAX / 33.3% ADD. Mean absolute deviation from Path 1's 75% MAX is 0.083, below v1.0's 0.10 threshold. But v1.0's null (subtype-label scrambling) preserved counts by construction, so count-based metrics had zero variance in the null, and v1.0 could not test whether the observed count pattern was significant.

The open question is: **if the overlay-extension algorithm had made different pre-planting decisions about which edges to label ADD vs MAX, would the observed count proportions still cluster near Path 1's?**

A PASS on that question would upgrade v1.1's algebraic claim. Currently, v1.1 says "identity-element attachment is the structural role." A count-transport PASS would add "and that role is not an isolated feature — the MAX/ADD count balance around the identity-anchored object also transports."

A FAIL on count would narrow v1.1's claim. It would say "identity-element attachment is specifically what transports; count proportions are incidental and could vary freely under different extension rules without changing the identity-edge result."

Either outcome sharpens the picture.

---

## What Count Transport Would Add, Concretely

Consider two possible worlds consistent with v1.1's PASS but distinguished by count transport:

**World A — Count transports.**
Recovered seams consistently have ~1 ADD edge per ~5 MAX edges, centered on the identity-to-chain-start edge. This ratio is stable across carriers and is not reproducible by random rule-reassignment. The MAX/ADD partition has a specific *size* signature — "small ADD minority anchored to the identity" — that is itself a transportable feature.

**World B — Count is incidental, identity-edge transport is everything.**
Recovered seams could have arbitrary MAX/ADD proportions under different extension rules. The 83.3%/16.7% split on P3AP happens because the P3AP algorithm happens to produce 6 edges with exactly 1 ADD. Under alternative rules (e.g., multiple ADD seeds rooted at different small elements), the count ratio would shift freely, but identity-edge attachment would still hold.

v1.1 alone cannot distinguish A from B. Count v1.2 can.

---

## Why This Is Not Just Bigger Numbers

A common trap in multi-sprint programs is to test the same hypothesis with progressively more stringent thresholds and call each pass an "upgrade." That is not what count v1.2 does. It tests a *different* hypothesis on a different null model:

- v1.1 null: subtype-label scrambling on fixed graphs. Fixes structure, varies labels.
- v1.2 null: pre-planting rule reassignment. Varies which edges are eligible-to-be-ADD before generation, re-runs recovery, measures counts.

The two nulls answer different questions. v1.1 asks "given the recovered graph, is the observed labeling special?" v1.2 asks "given the generator family, are the recovered counts special?"

Count v1.2 is upstream of v1.1 at the generator level. It tests whether the extension algorithm's specific rule-assignment produces counts that match Path 1's, or whether any rule-assignment-consistent-with-the-algorithm's-structure would produce similar counts.

---

## What Count Will Not Add

**It will not establish theorem transport.** That remains outside the program's current scope. Path 2 planted-recovery artifacts are heuristic objects; the Path 1 theorem is a proven construction on Z/10. A bridge PASS at the count level says structural features match across paths; it does not upgrade Path 2 artifacts to theorem status.

**It will not address the hub-vs-chain question.** The overlay extension still produces chains on Path 2. A count PASS would confirm count transport on chain topology; whether it would also hold on hub topology (under a different extension) is a separate question for a separate sprint.

**It will not test exact-cell identity.** Specific edge identities across carriers — which cells correspond to which — are not in Path 3 bridge scope, ever.

**It will not test adjacency.** Deferred to a later sprint once count is settled.

---

## The Narrow Delta

v1.1 established that the *identity element is the ADD anchor*. Count v1.2 tests whether the *count ratio around that anchor is also invariant*. Together, a PASS on both would support the claim:

> Under the P3AP overlay-extension, recovered Path 2 seams share with the Z/10 theorem seam both an algebraically-specific anchor (the identity element as ADD attachment) and a count-proportion signature (small ADD minority) at generator-level significance.

Together, a PASS on v1.1 and FAIL on count would support the narrower claim:

> Under the P3AP overlay-extension, recovered Path 2 seams share the identity-anchor feature with Path 1, but the count proportion is not a transportable feature at generator level — it is an artifact of the specific extension rule.

Each outcome is a clean, attributable addition to the program's body of findings.

---

## Scope Discipline Reminder

One sprint, one question, one null, one verdict. Count v1.2 tests count transport under a generator-level null. It does not test adjacency, does not run hub-extension, does not re-open v1.0's bundle, does not rescue anything. If it passes, it adds a specific finding to the ledger. If it fails, it narrows the v1.1 claim by one specific dimension. Either way, the program continues its pattern of accumulating narrow results rather than asserting broad ones.
