# S31 Z/10 Pilot — Frozen Recovery Spec
## Known-Chart Seam Recovery, Recovery Sprint Only

---

**Status:** FROZEN pending user approval.
**Version:** S31-pilot-v1.0.
**Change policy:** once any datum is scored against this spec, the spec cannot be edited. Amendments require S31-pilot-v1.1+ and a fresh run against the new spec.
**Relation to prior sprints:** S31-pilot tests recovery on Z/10 only. It does NOT test transport. It does NOT test overlay extension to other carriers. S30b's FAIL stands independently; this pilot uses the same extractor architecture at the same core parameters in a different generative setting.

---

## 1. Explicit Scope Statement

This is a **recovery pilot**, not a transport sprint.

The sprint answers exactly one question: **does the low-$N$ mode-extractor with persistence filter recover a known planted seam on Z/10 across four overlay conditions and three noise levels?**

The sprint does not answer:
- Whether seams transport across carriers.
- Whether the overlay-extension algorithm (doubling-chain + identity-edge) is meaningful on carriers other than Z/10.
- Whether any invariant should move between columns in `LOCAL_CHART_VS_TRANSFERRED_GRAMMAR.md`.
- Whether the Z/10 TSML theorem has implications for physical systems.

A PASS validates the extractor for known-chart recovery at low $N$. It earns the right to run a subsequent sprint testing overlay extension on other carriers. It does not promote any invariant. It is a tool-validation result.

A FAIL blocks all downstream sprints using this extractor and triggers diagnostic work.

---

## 2. Carrier

**Carrier:** $R_{10} = \mathbb{Z}/10\mathbb{Z}$ only.

$|U(10)| = 4$. Attractor $h = 9$. Shell partition $\sigma(u) = v_2(3u+1)$ gives shells $\{1, 9\}$ (shell 0) and $\{3, 7\}$ (shell 1). Canonical core $= U(10) \setminus \{1\} = \{3, 7, 9\}$.

On Z/10 the planted overlays reproduce the published TSML theorem exactly (for MAX + ADD). This gives us a bit-exact ground truth against which the extractor is measured.

---

## 3. Overlays (Frozen, Four Conditions)

### 3.1 Overlay MAX

Ordered pairs:
$$S_\text{MAX} = \{(2,4), (4,2), (4,8), (8,4), (2,9), (9,2)\}$$

Six ordered cells. Matches the published TSML MAX seam exactly.

Rule: $T_\text{gen}(x, y) = \max(x, y)$ on these pairs.

### 3.2 Overlay ADD

Ordered pairs:
$$S_\text{ADD} = \{(1,2), (2,1)\}$$

Two ordered cells. Matches the published TSML ADD seam exactly.

Rule: $T_\text{gen}(x, y) = (x + y) \bmod 10 = 3$ on these two cells.

### 3.3 Overlay MAX+ADD

Union of $S_\text{MAX}$ and $S_\text{ADD}$. Eight ordered cells. Reproduces the full published TSML seam exactly.

Each overlay rule is applied on its own domain.

### 3.4 Overlay NONE

No overlay. $T_\text{gen} = C_0$.

The NONE condition is the in-sprint control. Under the same extractor, same parameters, same scoring environment, we expect empty persistent seams — consistent with the S30b result, in a cleaner single-carrier setting.

---

## 4. Generator (Frozen)

For each (overlay, noise, seed):

1. Compute canonical $C_0(R_{10}, h = 9, \sigma)$ with the shell partition above and core $\{3, 7, 9\}$.
2. Apply the overlay (NONE, MAX, ADD, or MAX+ADD) to produce $T_\text{gen}$.
3. Generate $N = 10 \cdot n^2 = 1{,}000$ samples. Each sample:
   - $(x, y)$ uniform in $\{0, 1, \ldots, 9\}^2$.
   - $u$ uniform in $[0, 1)$.
   - If $u < p$: $z$ uniform in $\{0, 1, \ldots, 9\}$.
   - Else: $z = T_\text{gen}(x, y)$.
4. Compute mode $T^\text{emp}(x, y) = \arg\max_z c_{xy}(z)$, tie-break by smallest $z$.
5. Extract per-run seam against $C_0$:
$$S_r = \{(x, y) : T^\text{emp}(x, y) \neq C_0(x, y)\}$$

---

## 5. Extractor Parameters (Frozen)

| Parameter | Value |
|---|---|
| Carrier | Z/10 only |
| $N$ per run | 1,000 |
| Noise levels | $\{0.02, 0.10, 0.20\}$ |
| Overlays | MAX, ADD, MAX+ADD, NONE |
| Seeds per (overlay, noise) | 10 |
| Persistence threshold $\pi$ | 0.50 |
| Mode tie-break | smallest $z$ |
| Data seed base | 31,000 |
| Per-run seed | $31000 + 10000 \cdot \text{overlay\_idx} + 100 \cdot \text{noise\_idx} + r$ |

Overlay index map (frozen): NONE = 0, MAX = 1, ADD = 2, MAX+ADD = 3.
Noise index map (frozen): 0.02 = 0, 0.10 = 1, 0.20 = 2.

Total extractions: $4 \times 3 \times 10 = 120$ per-run extractions.

---

## 6. Persistence Filter (Frozen)

For each (overlay, noise) condition:
- Collect the 10 per-run seam sets.
- For each ordered pair $(x, y)$, count how many of the 10 runs contain it.
- Persistent seam: pairs appearing in $\geq \lceil \pi K \rceil = \lceil 5 \rceil = 5$ runs.

---

## 7. Recovery Metrics (Frozen)

Each metric computed per (overlay, noise) condition. Aggregated across overlays at each noise level.

### 7.1 M1 — Jaccard recovery

$$J = \frac{|S_\text{persistent} \cap S_\text{planted}|}{|S_\text{persistent} \cup S_\text{planted}|}$$

Defined as $1.0$ if both are empty (the NONE-clean case). Defined as $0.0$ if exactly one is empty.

### 7.2 M2 — Recall

$$R = \frac{|S_\text{persistent} \cap S_\text{planted}|}{|S_\text{planted}|} \text{ if } |S_\text{planted}| > 0, \text{ else undefined.}$$

### 7.3 M3 — Precision

$$P = \frac{|S_\text{persistent} \cap S_\text{planted}|}{|S_\text{persistent}|} \text{ if } |S_\text{persistent}| > 0, \text{ else } 1.0.$$

### 7.4 M4 — Type agreement

For each recovered pair $(x, y) \in S_\text{persistent} \cap S_\text{planted}$:
- If the pair is in $S_\text{MAX}$ domain: check $T^\text{emp}(x, y) = \max(x, y)$. Use modal $T^\text{emp}$ value across the 10 runs (seed-level mode, with $\pi K$ threshold).
- If the pair is in $S_\text{ADD}$ domain: check $T^\text{emp}(x, y) = (x+y) \bmod 10$.

For this, "modal $T^\text{emp}$ value across runs" means: at each (x,y) pair, take the value that appeared as the mode output in the majority of the K runs.

Type agreement rate $A = $ fraction of recovered seam cells with matching predicted value.

Undefined if the recovered intersection is empty.

---

## 8. Pass / Fail Criteria (Frozen)

### 8.1 Clean-regime recovery ($p = 0.02$)

For each non-NONE overlay (MAX, ADD, MAX+ADD) at $p = 0.02$:
- Jaccard $\geq 0.90$.
- Recall $\geq 0.95$.
- Precision $\geq 0.90$.
- Type agreement $\geq 0.90$.

The NONE overlay at $p = 0.02$: $|S_\text{persistent}| = 0$ required.

### 8.2 Reference regime ($p = 0.10$)

For each non-NONE overlay:
- Jaccard $\geq 0.70$.
- Type agreement $\geq 0.80$.

The NONE overlay at $p = 0.10$: $|S_\text{persistent}| = 0$ required.

### 8.3 Stress regime ($p = 0.20$)

For each non-NONE overlay:
- Jaccard $\geq 0.30$.

No threshold on type agreement at $p = 0.20$; reported but not enforced. NONE at $p = 0.20$: any non-empty persistent seam is reported but does not auto-fail (under aggressive noise, spurious persistent cells may appear; this is diagnostic rather than failure).

### 8.4 Overall pass

The pilot **passes** if all sub-conditions in 8.1, 8.2, and 8.3 (except the non-enforced parts) are met. Specifically:

1. All three non-NONE overlays meet 8.1 (four sub-thresholds each).
2. All three non-NONE overlays meet 8.2 (two sub-thresholds each).
3. All three non-NONE overlays meet 8.3 (Jaccard $\geq 0.30$).
4. NONE produces empty persistent seam at $p \in \{0.02, 0.10\}$.

### 8.5 Fail triggers

Any sub-threshold in 8.1–8.3 violated. Or NONE produces non-empty persistent seam at $p \in \{0.02, 0.10\}$.

### 8.6 Unclear

All thresholds met, but at least one is within 10% of its threshold (e.g., clean-regime Jaccard is 0.905–0.99, reference-regime Jaccard is 0.705–0.77). Report and flag the marginal sub-condition.

---

## 9. Anti-Tuning Rules

1. Carrier frozen (Z/10).
2. Overlay definitions frozen (§3).
3. Generator frozen (§4).
4. Extractor parameters frozen (§5).
5. Persistence threshold frozen ($\pi = 0.50$).
6. Metric definitions frozen (§7).
7. Thresholds frozen (§8).
8. Data seeds deterministic (§5).
9. No alternative metric may be substituted if results are unclear.
10. No parameter sweep within the pilot.

---

## 10. Deliverables

Written to `/home/claude/sprint31_pilot/`:

- `S31P_PER_SEED.csv` — per (overlay, noise, seed): seam size, seam edges.
- `S31P_PERSISTENT.json` — per (overlay, noise): planted seam, persistent seam, intersection, metrics.
- `S31P_SCORES.json` — aggregated metrics, thresholds, sub-conditions, verdict.
- `S31P_RESULTS.md` — per-condition table + summary.
- `S31P_VERDICT.md` — one-paragraph determination.
- `S31P_REPRO.md` — reproducibility notes.

---

## 11. Three-Way Outcome Interpretation

**PASS.** Extractor recovers planted seams on Z/10 at low $N$ across three overlay types and three noise levels, while correctly reporting empty seams under NONE control. The extractor is validated for Z/10 recovery. This earns the right to design a separate sprint testing overlay extension to Z/22 and Z/58. No invariant is promoted by this verdict.

**FAIL.** Extractor does not reliably recover planted seams on Z/10 at low $N$. This blocks all downstream sprints using this extractor architecture. Diagnostic required: the failure points to either (a) low-$N$ sampling variance is too large at $N = 1{,}000$ for Z/10 planted recovery — raise $N$ or raise $K$; (b) persistence threshold $\pi = 0.50$ is too strict — lower to 0.40 or 0.30; (c) the mode tie-breaking interacts with specific planted values — audit specific cells. No successor sprint until the diagnostic is complete.

**UNCLEAR.** Primary thresholds met but at least one sub-condition is marginal. Report finding. User decides whether to proceed to overlay-extension sprint with the caveat or to tighten the extractor before proceeding.

---

## 12. Status Effects on Outcomes

- **PASS:** extractor validated for Z/10 low-$N$ recovery. Right to design next sprint earned.
- **FAIL:** extractor architecture blocked. No sprint using this extractor until diagnosis.
- **UNCLEAR:** provisional use of the extractor permitted, with the marginal condition flagged in any downstream sprint.

---

## 13. What PASS Cannot Establish

Even under a strong PASS:
- No claim about other carriers.
- No claim about seam transport.
- No claim about physical interpretation.
- No claim that the overlay-extension algorithm will produce recoverable seams on Z/22, Z/58, or any other carrier.

The verified Z/10 seam is reproduced by the overlays by construction. A PASS confirms the extractor finds what was explicitly planted. That is a tool-validation statement. Any broader claim requires a separate sprint.

---

## 14. What FAIL Would Establish

A FAIL here is significant. It would mean the extractor architecture, even on Z/10 with a known ground truth, does not recover planted seams at low $N$ under uniform noise. The instrument would need to be reconsidered before any downstream use. Unlike the S28/S29 failures (which ruled out specific transport hypotheses), a FAIL here would rule out the current extractor's viability as a detection tool for anything at low $N$ on this family.

---

## 15. Integrity Commitment

The pilot runs once. One frozen spec, one deterministic run, one verdict. No parameter sweeps within the pilot. No adjustment of thresholds based on observed data. The verdict is whatever the metrics produce against the frozen thresholds.

This pilot earns or blocks future sprints. It does not answer any open invariant question. It answers one question about the tool: does the tool work on its home ground? That is the only question within scope.
