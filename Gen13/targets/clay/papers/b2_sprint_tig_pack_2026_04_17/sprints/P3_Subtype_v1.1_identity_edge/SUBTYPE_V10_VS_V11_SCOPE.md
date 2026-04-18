# What v1.0 Actually Established, and What v1.1 Isolates
## Short Note

---

## What v1.0 Established

v1.0 ran three parallel tests on the same P3AP-recovered seams:

- **Count proportion (M1):** Path 2 carriers produced 83.3% MAX / 16.7% ADD on 7 of 8 carriers, 66.7%/33.3% on Z/14. Mean absolute deviation from Path 1's 75% MAX was 0.083, within the 0.10 threshold. Null was structurally degenerate (label-scrambling preserves counts), so no null separation possible.

- **Role placement (M2):** On all 8 Path 2 carriers, the ADD edge attached a degree-1 external vertex to the main connected component. Null separation $+3.80\sigma$ above a label-scrambling null — decisive.

- **Adjacency similarity (M3):** Mean Bhattacharyya similarity to Path 1's adjacency vector was 0.9551, above the 0.80 threshold. Null mean was 0.9713 (higher than real) because random label placements at chain-interior positions happened to produce adjacency vectors closer to Path 1's hub-derived (0.5, 0.5, 0.0) than the real external-attachment placement did. Separation was $-0.87\sigma$.

**Verdict:** UNCLEAR, per the frozen spec.

**What is firmly established by v1.0:**

The role-placement result is the one v1.0 actually settled. It says that under the P3AP extension algorithm, the ADD subtype edge in recovered seams consistently attaches a degree-1 vertex (external to the main seam body) to the main connected component, across 8 Path 2 carriers, and this pattern is not reproducible by random label assignments on the same graphs at a rate significantly above chance.

**What is *not* established by v1.0:**

- Count transport at any level of significance (null inadequate).
- Adjacency-pattern transport (metric mis-aligned with chain topology).
- Whether the "degree-1 external vertex" is specifically the ring's identity element, or merely happens to be vertex 1 because the identity-edge rule puts it there.
- Anything about what would transport under a different extension algorithm.

v1.0's strong finding is real but structurally under-specified. The v1.0 spec's adapted role rule was chosen to be forgiving — it accepted any external low-degree vertex attachment — because the chain-vs-hub asymmetry discovered in P3AP made stricter rules inapplicable without further analysis.

---

## What v1.1 Isolates

v1.1 asks one question:

> **Does the ADD edge on recovered Path 2 seams touch the identity element (vertex 1) of the ring at a rate significantly exceeding label-scrambling null?**

That is the tighter, algebraically-meaningful form of v1.0's loose M2. "Attaches a degree-1 external vertex" is graph-theoretic. "Attaches the identity element of the ring" is algebraic. The identity element is a distinguished position determined by ring structure, not by graph shape.

If v1.1 passes, v1.0's strong finding upgrades: the transporting feature is not just "external-vertex attachment" (which could happen by chance with any low-degree vertex choice), but specifically "identity-element attachment" (which reflects the ring's algebraic structure).

If v1.1 fails, v1.0's role-placement result was a graph-shape artifact rather than an algebraic transport. The ADD edge happens to attach vertex 1 on all 8 carriers because the identity-edge rule puts it there, but that attachment is not significantly more frequent than random label scrambling would produce on the same graphs.

Either outcome narrows the claim.

---

## Specifically What Changes From v1.0 to v1.1

| Aspect | v1.0 | v1.1 |
|---|---|---|
| Object class | P3AP recovered seams | Same |
| Generator | None (reuses P3AP) | Same |
| Primary metrics | M1 count, M2 role, M3 adjacency | M4 identity-edge attachment only |
| Number of hypotheses | 3 (bundled) | 1 |
| Adapted rule | Graph-role (degree-1 external) | Algebraic (vertex = identity element) |
| Null | Subtype-label scrambling | Same |
| Number of null separations required | 3 (degenerate, pass, fail) | 1 |
| Possible verdicts | UNCLEAR given the chosen metric/null combinations | Clean PASS / FAIL / UNCLEAR |
| What PASS permits claiming | Bundled, hard to isolate | "Identity-element attachment transports at $N\sigma$" |

---

## The Claim Structure Each Sprint Supports Under PASS

**v1.0 under a full PASS would have supported** (had it occurred):

> MAX/ADD count proportions, role placements, and adjacency patterns from the Z/10 theorem seam are each reproducible on the Path 2 family under the specified extension algorithm, at significance exceeding the label-scrambling null.

That sentence has three clauses. v1.0's actual mixed result makes it unavailable.

**v1.1 under a clean PASS will support:**

> On Path 2 carriers under the specified extension algorithm, the ADD-subtype edge attaches the identity element (vertex 1) of the ring at a rate significantly exceeding the label-scrambling null on the same graphs.

One clause. One metric. One null. One number.

The narrower claim is more informative because it is tied to an algebraic feature of the ring (the multiplicative identity), not merely a graph-theoretic feature (low-degree external vertex).

---

## Honest Disclosure About Prediction

v1.1 is expected to pass. The reason: all 8 P3AP carriers already show ADD-edge attachment to vertex 1, which is the identity element. v1.0's $+3.80\sigma$ on M2 was measuring a looser condition than identity-element-touch; the tighter condition is visibly met.

Null separation is the less-certain part. Under label-scrambling on small graphs (3-6 edges), random label placement touches vertex 1 with probability proportional to vertex 1's degree relative to total degree. If vertex 1 has degree 1 in all 8 carriers (which is what P3AP produced), random labeling places the ADD label on the vertex-1-incident edge with probability $2/|E|$ (two half-edges incident to vertex 1 out of $2|E|$ total half-edges). For $|E| = 6$, that's $1/3$. For $|E| = 3$, that's $2/3$. Across 8 carriers, random expected match rate is somewhere around 0.4–0.5 — well below the real 1.0.

Predicted null separation: strong, likely $> 3\sigma$. Prediction does not modify thresholds.

---

## What This Note Does Not Say

- Nothing about whether v1.2-count or v1.2-adjacency will later succeed. Those are open questions.
- Nothing about hub-extension or alternative overlay rules.
- Nothing about theorem-level claims.
- Nothing about physical, ontological, or real-world structures.

v1.1 is a narrow sprint with a precise target. This note clarifies what that target is relative to v1.0, and nothing more.
