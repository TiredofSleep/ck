# PPM-v2.1 Additive Transport — Reproducibility
## How to Rerun

---

## Scope Reference

**Path:** Path 3 Bridge Test.
**Operationalization:** Additive, carrier-adapted for Source 1 under strict AND.
**Spec:** `PPM_V21_ADDITIVE_TRANSPORT_PREREG.md` (frozen as PPM-v2.1).
**Verdict:** FAIL (Uniform sub-pattern).

---

## Execution Character

Deterministic application of frozen rubric to frozen P3AP audit data. Script `ppm_v21_score.py` reads P3AP records and applies each source's rubric predicate per carrier. No RNG, no sampling, no tuning.

---

## Input Data (Static)

Same P3AP audit records used by PPM-v2.0:

1. `/home/claude/path3_bridgeAprime/P3AP_OVERLAY_AUDIT.json` — per-carrier overlay rules and cells_removed_by_audit.
2. Per-carrier seams inferred by subtracting audit-removed cells from raw MAX / ADD cell sets.

The 8 Path 2 carriers are fixed: {14, 22, 34, 42, 46, 58, 74, 94}. None changes on rerun.

---

## Rubric (Frozen in PPM-v2.1 §5)

- **Source 1 (carrier-adapted, strict AND):** persistent-side = additive backbone iff (majority of unordered seam edges ≥ 50%) AND (native additive-flow alignment). Neither subtype meets both conditions on any Path 2 carrier.
- **Source 2 (inherited from v1.1):** coherence of "ADD at vertex 1" reading under additive §3 — vertex 1 is additive generator, not additive identity; no clean parallel to v1.0's multiplicative argument; substitute arguments prohibited per §5.2; scores 0/0.
- **Source 3 (inherited, topology-neutral):** ADD at leaf → Map A −1, Map B +1.
- **Source 4 (inherited, topology-neutral):** MAX carries majority topology features → Map A −1, Map B +1.

---

## Expected Reproduction Results

| Carrier | S1 A | S1 B | S2 A | S2 B | S3 A | S3 B | S4 A | S4 B | A agg | B agg | Gap | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|
| Z/14 | 0 | 0 | 0 | 0 | −1 | +1 | −1 | +1 | −2 | +2 | 4 | INDECISIVE |
| Z/22 | 0 | 0 | 0 | 0 | −1 | +1 | −1 | +1 | −2 | +2 | 4 | INDECISIVE |
| Z/34 | 0 | 0 | 0 | 0 | −1 | +1 | −1 | +1 | −2 | +2 | 4 | INDECISIVE |
| Z/42 | 0 | 0 | 0 | 0 | −1 | +1 | −1 | +1 | −2 | +2 | 4 | INDECISIVE |
| Z/46 | 0 | 0 | 0 | 0 | −1 | +1 | −1 | +1 | −2 | +2 | 4 | INDECISIVE |
| Z/58 | 0 | 0 | 0 | 0 | −1 | +1 | −1 | +1 | −2 | +2 | 4 | INDECISIVE |
| Z/74 | 0 | 0 | 0 | 0 | −1 | +1 | −1 | +1 | −2 | +2 | 4 | INDECISIVE |
| Z/94 | 0 | 0 | 0 | 0 | −1 | +1 | −1 | +1 | −2 | +2 | 4 | INDECISIVE |

**Family aggregation:** $N_B = 0$, $N_A = 0$, $N_I = 8$. **Verdict: FAIL. Sub-pattern: Uniform FAIL.**

**Secondary summary:** mean gap across all carriers = 4.00.

---

## Verification Hooks

Any reproducing scorer should verify:

Per-carrier structural facts (from P3AP audit):
- [ ] Every carrier has |E_ADD| = 1 (minority under additive reading).
- [ ] Every carrier's ADD edge is (1, 2).
- [ ] Every carrier has ADD NOT touching vertex 0 (additive identity outside seam).
- [ ] Every carrier has ADD touching vertex 1 (additive generator, not identity).
- [ ] Every carrier's MAX is majority (67–83%), non-additive, connected.

Per-source predicate checks:
- [ ] Source 1 strict AND: no subtype meets majority + native-additive-alignment. Score 0/0 on every carrier.
- [ ] Source 2 key criterion: vertex 1 is additive generator, not additive identity. No clean parallel; substitute arguments prohibited. Score 0/0 on every carrier.
- [ ] Source 3: ADD has degree-1 endpoint on every carrier. ADD at leaf → −1/+1.
- [ ] Source 4: MAX has edge-count majority + connected on every carrier. Majority → −1/+1.

Per-carrier verdict:
- [ ] Every carrier's Map A aggregate is −2.
- [ ] Every carrier's Map B aggregate is +2.
- [ ] Every carrier's cleanness gap is 4.
- [ ] Every carrier classifies as INDECISIVE (no map reaches +3).

Family-level:
- [ ] $N_B = 0$, $N_A = 0$, $N_I = 8$.
- [ ] Neither PASS threshold met.
- [ ] Verdict = FAIL, sub-pattern = Uniform FAIL per §9.2.

---

## Command to Rerun

```bash
cd /home/claude/foundation_sprint/ppm_v21
python3 ppm_v21_score.py
```

Expected runtime: < 1 second. Produces `PPM_V21_PER_CARRIER_SCORES.json`.

---

## Potential Sources of Reproduction Divergence

### Divergence point 1 — Source 1 strict AND vs relaxed OR

The pre-reg §5.1 specifies strict AND (majority AND native-additive-alignment). A scorer might relax to "majority OR native-alignment," which would give:
- ADD: native-additive alignment alone ✓. Map A +1, Map B −1.
- MAX: majority alone ✓. Map A −1, Map B +1.

Both maps would then get points on Source 1, producing different aggregates.

**Anti-divergence rule:** §16 item 8 explicitly prohibits rubric relaxation. Strict AND is frozen; relaxation requires a new sprint version (v2.1.1 or later).

### Divergence point 2 — Source 2 substitute argument

A scorer might introduce "ADD at additive-generator = excluded at flow origin" as a substitute for v1.0's multiplicative-trivialization argument. This would score Map B +1 on every carrier, producing aggregate B = +3 and potentially reaching the +3 winner threshold.

**Anti-divergence rule:** §5.2 explicitly prohibits substitute arguments. Introducing a new structural argument requires its own pre-registration. Under the frozen v2.1 rubric, Source 2 scores 0/0.

### Divergence point 3 — Source 3 and 4 topology-neutral interpretation

Sources 3 and 4 are inherited verbatim from v1.0 and v2.0. Any scorer interpreting them differently is disputing the v1.0 rubric, not just v2.1.

**Anti-divergence rule:** the topology-neutral sources have been consistent across v1.0, v1.1, v2.0, v2.1. Reinterpreting them requires a new v1.0 version, not a v2.1 deviation.

### Divergence point 4 — Sub-pattern classification

A scorer might argue that $N_B = N_A = 0$ with $N_I = 8$ should count as "Below-threshold" because the uniform indecisive pattern has per-carrier Map B leading by 2. The observed pattern has discriminating signal per-carrier (gap 4) but no carrier reaches the winner threshold.

**Anti-divergence rule:** §9.2 defines Uniform FAIL as $N_B = N_A = 0$, which is a strict definition. The observed configuration satisfies it. The pre-reg's definitions are authoritative per anti-tuning rule §11. The Below-threshold label in §12's prose was a pre-reg authoring inconsistency; the frozen §9.2 definitions win.

---

## Cross-Sprint Position

| # | Spec | Path | Operationalization | Verdict | Key result |
|---|---|---|---|---|---|
| 12 | PPM-v1.0 | 1 | Multiplicative | PASS (Map B) | +4/−4, gap 8 |
| 13 | PPM-v1.1 | 1 | Additive | FAIL | +2/−2, gap 4, winner sub-threshold |
| 14 | PPM-v2.0 | 3 | Multiplicative | PASS (uniform) | $N_B = 8/8$, gap 8 |
| 15 | **PPM-v2.1** | **3** | **Additive** | **FAIL (Uniform)** | **$N_B = N_A = 0$, gap 4 uniform** |

Fifteen sprints under discipline. The 2×2 design space (local/transport × multiplicative/additive) is now complete for the subtype-mapping checkpoint.

---

## If Rerun Gives a Different Verdict

All inputs are static P3AP audit records. The rubric is specified in frozen prose. Divergence must come from:

1. Modified P3AP audit JSON (check against B2 pack).
2. Rubric relaxation (prohibited per §16 item 8).
3. Substitute Source 2 argument (prohibited per §5.2).
4. Sub-pattern misclassification (strict §9.2 definitions apply).

The FAIL with Uniform sub-pattern, $N_B = N_A = 0$, $N_I = 8$ is the deterministic output of the frozen spec. Any correct reimplementation reproduces this result.

---

## Integrity

- No external inputs beyond the frozen pre-reg and P3AP audit records.
- All 32 per-carrier-per-source scores traceable to specific rubric clauses.
- Prohibited substitutions honored (§16 item 8).
- Pilot prediction mismatch at sub-pattern layer documented transparently; frozen pre-reg's definitions take precedence.
- No post-hoc rubric adjustment.
- v1.0, v1.1, v2.0 verdicts unaffected.
- SAH at foundation register unaffected; this FAIL neither validates nor refutes SAH.
- Rule 19 enforced: no composite claim merging v2.0 and v2.1.
