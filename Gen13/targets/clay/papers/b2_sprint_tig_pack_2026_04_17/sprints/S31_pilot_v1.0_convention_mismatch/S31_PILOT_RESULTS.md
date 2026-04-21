# S31 Pilot Results — Z/10 Recovery Data
## S31-pilot-v1.0, Deterministic Execution

---

## Canonical Setup

- Carrier: Z/10.
- Attractor $h = 9$ (max odd unit of $U(10) = \{1, 3, 7, 9\}$).
- Shell partition $\sigma(u) = v_2(3u+1)$: $\{1 \to 2, 3 \to 1, 7 \to 1, 9 \to 2\}$.
- Canonical core: $\{3, 7, 9\}$ (units minus identity).
- Canonical $C_0$: computed from §4 of pilot spec.

## Per-Condition Table

Each row shows one (overlay, noise) condition, with planted seam size $|S_p|$, persistent seam size $|S_\text{per}|$, intersection size $|\cap|$, and metrics J (Jaccard), R (recall), P (precision), A (type agreement).

| Overlay | $p$ | $\|S_p\|$ | $\|S_\text{per}\|$ | $\|\cap\|$ | J | R | P | A |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| NONE | 0.02 | 0 | 0 | 0 | 1.0000 | — | 1.0000 | — |
| NONE | 0.10 | 0 | 0 | 0 | 1.0000 | — | 1.0000 | — |
| NONE | 0.20 | 0 | 0 | 0 | 1.0000 | — | 1.0000 | — |
| MAX | 0.02 | 6 | 4 | 4 | 0.6667 | 0.6667 | 1.0000 | 1.0000 |
| MAX | 0.10 | 6 | 4 | 4 | 0.6667 | 0.6667 | 1.0000 | 1.0000 |
| MAX | 0.20 | 6 | 4 | 4 | 0.6667 | 0.6667 | 1.0000 | 1.0000 |
| ADD | 0.02 | 2 | 2 | 2 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| ADD | 0.10 | 2 | 2 | 2 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| ADD | 0.20 | 2 | 2 | 2 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| MAX+ADD | 0.02 | 8 | 6 | 6 | 0.7500 | 0.7500 | 1.0000 | 1.0000 |
| MAX+ADD | 0.10 | 8 | 6 | 6 | 0.7500 | 0.7500 | 1.0000 | 1.0000 |
| MAX+ADD | 0.20 | 8 | 6 | 6 | 0.7500 | 0.7500 | 1.0000 | 1.0000 |

---

## Observations Drawn Directly From Data

### Recovery pattern

- **ADD overlay:** perfect recovery at every noise level. Both planted cells $(1,2)$ and $(2,1)$ are recovered in all 10 seeds at all three noise levels. Jaccard = 1.0, recall = 1.0, precision = 1.0.
- **MAX overlay:** exactly 4 of 6 planted cells are recovered. Jaccard = 4/6 = 0.6667, recall = 4/6. Precision = 1.0 (no false positives). The two unrecovered cells are $(2,9)$ and $(9,2)$ — at every noise level.
- **MAX+ADD overlay:** 6 of 8 cells recovered (both ADD cells, plus 4 of 6 MAX cells — the same 4). Jaccard = 6/8 = 0.75.
- **NONE:** empty persistent seam at all noise levels. Control condition passes.

### Noise-invariance of the failure

The failure to recover $(2,9)$ and $(9,2)$ is identical at $p = 0.02, 0.10, 0.20$. This is not a noise-degradation issue. Even at the near-clean regime $p = 0.02$, those two cells are never recovered.

### Which cells are the two unrecovered cells?

$(2,9)$ and $(9,2)$. Both involve the attractor position $h = 9$.

---

## Direct Per-Seed Check

Looking at per-seed data for cells $(2, 9)$ and $(9, 2)$: these cells never appeared in any of the 10 seeds at any noise level under any overlay. Not a persistence filter issue — the extractor never flagged these cells as disagreeing with $C_0$ in any single run.

---

## Diagnostic (Structural, Read-Only)

The cells $(2,9)$ and $(9,2)$ have canonical $C_0$ value = 9 (because $h = 9$ and the default rule applies — neither $x$ nor $y$ is in the core shell-stability domain when one is 2). The MAX overlay rule also assigns these cells the value 9 (since $\max(2,9) = 9$). So the planted value equals the canonical value.

The extractor's definition of a seam cell is "empirical mode ≠ canonical $C_0$ value." When the planted overlay value coincides with the canonical value, there is nothing to detect: the empirical mode agrees with both $C_0$ and the overlay, so the cell does not register as a seam edge.

This is a **spec-design artifact**, not a tool failure. The extractor found every planted cell where the planted value differed from $C_0$. It did not find planted cells where the planted value equalled $C_0$ — because by the extractor's definition, those cells are not in the seam.

---

## Relation to the Published TSML Theorem

The published Z/10 TSML theorem uses $h = 7$, not $h = 9$. Under $h = 7$:
- $C_0(2, 9) = 7$ (default).
- MAX overlay value = 9.
- So $T_\text{gen}(2,9) = 9 \neq 7 = C_0(2,9)$, and the cell is detectable.

The pilot spec fixed the attractor rule as "max odd unit of $U(n)$", which for Z/10 is 9. That rule was inherited from Sprint 21's prior-free discovery (where it correctly identifies the largest odd unit across a family). However, the published TSML theorem uses $h = 7$ as a deliberate choice (matching the $v_2(3u+1)$ maximum-shell element in a specific framing).

**Two different attractor conventions coexist in the program:**
- Sprint 21 discovery: $h = \max$ odd unit → on Z/10, $h = 9$.
- Published TSML theorem: $h = 7$ (specific theorem-choice).

The pilot used the first convention. The planted overlays (published TSML seam) were defined under the assumption of the second convention. They are not fully compatible on cells involving $h$.

---

## What the Data Shows, Stated Narrowly

Under S31-pilot-v1.0's frozen spec:
- ADD recovery is perfect at all noise levels.
- MAX recovery stalls at 4 of 6 cells, at every noise level, due to canonical/overlay coincidence on 2 cells involving the attractor.
- MAX+ADD recovery is 6 of 8 cells, same pattern.
- NONE control behaves as expected.

All metrics sit at exactly the ratios implied by "detect cells where empirical ≠ $C_0$, and coincident cells are by definition not in that set." There is no noise-driven degradation within the tested range; the extractor works cleanly on the cells it can see.

---

## What This Data Cannot Say

- Whether the pilot would pass under a different canonical $h$ convention (e.g., $h = 7$). That is a different spec.
- Whether the extractor would recover planted seams on carriers other than Z/10.
- Any transport claim whatsoever.

Verdict follows in `S31_PILOT_VERDICT.md`.
