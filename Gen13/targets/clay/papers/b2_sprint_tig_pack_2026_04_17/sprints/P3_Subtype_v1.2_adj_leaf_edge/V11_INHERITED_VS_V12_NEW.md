# What Is Inherited From v1.1, and What Is Genuinely New in v1.2
## Short Note

---

## Inherited From v1.1 (Not Tested in v1.2)

**v1.1's finding:** under the P3AP overlay-extension on 8 Path 2 carriers, the recovered ADD-subtype edge attaches the ring's multiplicative identity element (vertex 1) at $+6.06\sigma$ above the subtype-label-scrambling null.

This result is on the record. v1.2 does not re-test it, does not re-score it, does not bundle it with new metrics. v1.2's results document will report $I = 1$ on all 8 carriers as *inherited context* from v1.1, but $I$ does not contribute to v1.2's pass/fail logic. Any composite similarity claim between v1.1 and v1.2 belongs to a retrospective synthesis document, not to v1.2's own verdict.

Concretely:

- v1.1 established: the ADD edge's degree-1 endpoint is specifically vertex 1.
- This presupposes the ADD edge *has* a degree-1 endpoint (otherwise the question is vacuous).
- v1.1 took that presupposition for granted because the data plainly satisfied it.

v1.2's question lies under that presupposition.

---

## Genuinely New in v1.2

**v1.2's question:** does the ADD edge's leaf-edge placement — having a degree-1 endpoint at all — transport at significance above label-scrambling?

This is a distinct question because:

- $I$ asks "given a degree-1 endpoint, is it the identity?"
- $L$ asks "is there a degree-1 endpoint?"

Under the null, label-scrambling preserves the recovered graph and reassigns labels. If the scrambled ADD label lands on a chain-interior edge, that edge has no degree-1 endpoint — both endpoints are degree-2 chain interior vertices. In that case $L = 0$, and $I$ would be vacuous or defaulted to 0.

So under the null, there is a substantive probability of $L = 0$ per replicate per carrier. Real always has $L = 1$. The gap is the new signal.

---

## The Pilot Confirms the Separation Is Genuine

A pilot computation on P3AP data shows:

- **$L$ null rate** averaged across 8 carriers: approximately 0.375. (Chain graphs have 2 leaf edges out of $|E|$ total; random placement puts ADD on a leaf edge with probability $2/|E|$.)
- **$L$ real rate** across 8 carriers: 1.000.
- **$I$ null rate** averaged across 8 carriers: approximately 0.188. (This is v1.1's already-tested null.)
- **$I$ real rate:** 1.000.

$L$'s null rate (0.375) is substantially higher than $I$'s (0.188). This is expected: it is easier to satisfy "the ADD edge is a leaf edge" than "the ADD edge's leaf endpoint is the specific identity vertex." $I$ is a stricter condition than $L$.

But $L$'s null rate is still well below its real rate of 1.0. The signal-to-null gap is real, not trivially explained by graph structure alone.

---

## The Claim Each Sprint Earns

**v1.1 earns** (already on record): the ADD edge's leaf endpoint, when one exists, is the ring's identity element.

**v1.2 will earn, if it passes** (pending execution): the ADD edge has a leaf endpoint — it is a leaf edge of the recovered seam graph — at a rate significantly above random label placement.

Together, v1.1 and v1.2 would earn a compound claim only by explicit retrospective synthesis, not by either sprint's own verdict:

> Under the P3AP overlay-extension, the recovered ADD-subtype edge is consistently a leaf edge (v1.2) whose leaf vertex is the ring's multiplicative identity (v1.1). Each of these attributes is independently confirmed at $N\sigma$ above label-scrambling null.

That compound claim is a fair reading of the accumulated evidence. But writing it requires both sprints to have run. v1.2 cannot write it alone. v1.1 cannot write it alone. The composite belongs to a synthesis step separate from either sprint's execution.

---

## What This Means for Reporting

v1.2's results document will include a section called "Inherited Context from v1.1" that reports $I = 1$ across all carriers with a pointer to `PATH3_SUBTYPE_V11_VERDICT.md`. This section is explicitly labeled as inherited, not as new evidence, so that readers cannot confuse v1.1's result with a v1.2 finding.

v1.2's pass/fail depends on $L$ alone. If $L$ passes, v1.2 PASSes. If $L$ fails, v1.2 FAILs, and this failure does not retroactively affect v1.1's identity-edge result (which is measured by a different metric on the same data).

---

## What v1.2 Still Does Not Test

- Count transport (closed under P3AP generator, per `WHY_COUNT_IS_NOT_LIVE_UNDER_P3AP.md`).
- Adjacency ratios in the v1.0 sense (shape-dependent, abandoned).
- Main-component attachment $M$ (structurally redundant on chain topology).
- Hub-extension.
- Any new generator family.
- Cell identity across carriers.
- Theorem transport.
- Physical or ontological invariants.

The narrow scope is preserved. The program's pattern of accumulating one narrow finding per sprint continues.
