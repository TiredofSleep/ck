# S31 Pilot Verdict
## S31-pilot-v1.0 — Final Determination

---

## Verdict: **FAIL**

---

## One-Paragraph Justification

Under the pre-registered pass criteria of S31-pilot-v1.0 §8, the pilot fails. Specifically: the clean-regime ($p = 0.02$) sub-conditions for MAX overlay and MAX+ADD overlay miss the Jaccard and recall thresholds. MAX achieves Jaccard = 0.6667 against a $\geq 0.90$ threshold and recall = 0.6667 against $\geq 0.95$. MAX+ADD achieves Jaccard = 0.75 and recall = 0.75 against the same thresholds. At the reference regime ($p = 0.10$), MAX fails the Jaccard $\geq 0.70$ threshold by a margin of 0.033. Four of the 24 sub-conditions fail; the remaining 20 pass, including all NONE-control conditions, all ADD-overlay conditions at every noise level, all stress-regime Jaccard floors, and all precision and type-agreement thresholds. Per the anti-tuning rules in §9, no threshold is adjusted and the verdict is FAIL as specified. The failure is noise-invariant — the same two cells, $(2,9)$ and $(9,2)$, are unrecovered at every noise level across MAX and MAX+ADD overlays — so the failure is not caused by sampling variance or extractor sensitivity but by a structural property of the spec.

---

## What This FAIL Means

Per S31-pilot-v1.0 §11:

> **FAIL:** the extractor does not reliably recover planted seams on Z/10 at low $N$. This blocks all downstream sprints using this extractor architecture. Diagnostic required.

The mandated action from the user's direction: *"stop and diagnose extractor architecture before any extension."*

Execution honors that rule. No carrier-extension sprint is authorized by this verdict. A diagnostic round is required before any successor sprint proceeds.

---

## Diagnostic Summary (For User Review)

The failure pattern is informative in a specific way. All unrecovered cells are exactly those where the planted overlay value coincides with the canonical $C_0$ value under the pilot's choice of attractor $h = 9$:

- Cell $(2, 9)$: $C_0$ value = 9 (default rule). MAX value = $\max(2,9) = 9$. Planted value equals canonical value.
- Cell $(9, 2)$: same, by symmetry.

The extractor defines the seam as cells where empirical mode ≠ canonical $C_0$. When planted value coincides with $C_0$ value, the empirical mode agrees with both, so the cell is by definition not detectable under this seam definition. The extractor is correctly reporting "no disagreement" on those cells, because no disagreement exists.

The root cause is a mismatch between two attractor conventions that coexist in the program:

- **Pilot spec (inherited from Sprint 21 discovery):** $h = \max$ odd unit → $h = 9$ on Z/10.
- **Published TSML theorem (foundational work):** $h = 7$.

The planted overlays in §3 of the pilot spec reproduce the published TSML seam, which was defined against $h = 7$. Under $h = 9$, the canonical $C_0$ assigns value 9 to many cells that the published theorem's $C_0$ would assign differently. Two of the MAX overlay cells become invisible under the pilot's $h = 9$ convention.

This is not a tool failure. The extractor recovers every detectable overlay cell perfectly: precision = 1.0 everywhere, type agreement = 1.0 on every recovered cell, noise-invariant recovery on ADD (which does not involve the attractor). The failure is that the pilot spec committed to a convention under which 2 of 8 planted cells are structurally undetectable regardless of extractor performance.

---

## What FAIL Does NOT Mean

- The extractor is not broken. It performs perfectly on every cell where detection is possible. ADD recovery is 1.0 at all three noise levels. Precision is 1.0 across the entire grid.
- The noise model is not the problem. Failure is noise-invariant.
- Low $N$ is not the problem. The extractor sees the detectable cells cleanly at $N = 1{,}000$.
- The persistence filter is not the problem. Recovered cells appear in all 10 seeds.

---

## What Must Be Decided Before Any Successor Sprint

Two legitimate paths forward. Neither is authorized by this verdict; both are options for user decision.

**Path A: Align the attractor convention with the published theorem.** Rewrite the successor pilot spec to use $h = 7$ on Z/10, matching the published TSML construction. Under that convention, all 8 planted cells are detectable, and clean-regime recovery should be near-perfect. The tradeoff: this abandons the "max odd unit" rule that emerged from Sprint 21's prior-free discovery, which was a cross-carrier-stable identification. For Z/10, $h = 7$ and $h = \max$ odd unit both make structural sense; on other carriers, "max odd unit" is the rule that extends naturally.

**Path B: Change the seam definition to accommodate coincident cells.** Define the seam as *planted* cells rather than *empirical-vs-canonical* cells. Under a planted-recovery framing, the task is "does the extractor identify the set of cells that were overlaid?" which requires a different detection strategy — for example, comparing the empirical mode against multiple candidate operators and selecting which one fits best per cell. This is a larger change to the extractor architecture.

**Path C (trivial — not recommended):** Change the attractor rule just for Z/10 recovery tests. This would lose the cross-carrier consistency that made Sprint 21's discovery meaningful.

---

## Actions Required by the Verdict

1. Record S31-pilot-v1.0 as FAIL.
2. Block all carrier-extension sprints using this extractor architecture until diagnostic is resolved.
3. No modification to S31-pilot-v1.0 or rerun within this spec.
4. Present Paths A, B, C to user for selection of successor-sprint direction.
5. Any successor pilot must be frozen as a new spec (S31-pilot-v1.1 or later) with explicit resolution of the attractor-convention question.

---

## Honest Assessment

This is a spec-design failure discovered by execution. The pilot spec was written without fully auditing whether the two attractor conventions would produce compatible overlays. S31-pilot-v1.0 correctly executed what was specified and correctly reported that the specified thresholds are not met. The diagnostic above is observation of what happened, not reinterpretation of the verdict.

The verdict is FAIL. The cause is documented. Two of the four sub-conditions that failed would be unaffected by any tool change — they would remain unrecoverable under this spec no matter how the extractor is tuned. The spec itself needs revision before a productive successor pilot can run.
