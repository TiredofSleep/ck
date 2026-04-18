# PPM-v3.0 V0 Boundary Checkpoint — Reproducibility
## How to Rerun

---

## Scope Reference

**Path:** Path 1 (Local Theorem Chart), $h_\text{thm} = 7$.
**Operationalization:** V0-adapted persistent/excluded reading with Source 3 sensitivity branch.
**Spec:** `PPM_V30_V0_PREREG_DRAFT.md` (frozen as PPM-v3.0 revised).
**Verdict:** UNCLEAR by Sensitivity.

---

## Execution Character

Deterministic application of frozen rubric to frozen V0 data, with two Source 3 branches scored independently and combined via §7.2 robustness rule. Script `ppm_v30_score.py` verifies structural facts, computes 16 source-map-branch scores, aggregates per branch, and applies the robustness rule. No RNG, no sampling.

---

## Input Data (Static)

All inputs are on-record:

1. **Rule (b) of `CANONICAL_TSML_CONSTRUCTION.md`** (B2 pack, `theorem_local_chart/`):
   $$T(0, x) = T(x, 0) = \begin{cases} h & \text{if } x = h \\ 0 & \text{otherwise} \end{cases}$$
2. **Z/10 with $h = 7$**: fixes the 19 V0 cells and the 17/2 split into V0_Z (zero-output) and V0_H (HARMONY-output).

None changes on rerun.

---

## Rubric (Frozen in PPM-v3.0 §5)

### Fixed sources (same under both S3 branches)

- **Source 1:** backbone iff majority (≥50%) AND aligns with Rule (b) default. V0_Z meets both; V0_H meets neither.
- **Source 2:** localized exception iff minority AND is default-rule override AND restricted to distinguished element. V0_H meets all three; V0_Z meets none.
- **Source 4:** pair-object signature iff exactly 2 cells forming swap-symmetric pair. V0_H matches; V0_Z does not.

### Source 3 sensitivity branch

- **S3a (hold at boundary → excluded):** attractor-privilege cells at excluded-side = "hold at boundary" reading = coheres with Map-V0-I.
- **S3b (gravity well → persistent):** attractor-privilege cells at persistent-side = "where structure gathers" reading = coheres with Map-V0-II.

---

## Expected Reproduction Results

### Per-source scores

| Source | Map-V0-I | Map-V0-II |
|---|---:|---:|
| S1 (rule-majority backbone) | +1 | −1 |
| S2 (exception-structure) | +1 | −1 |
| S3a (→ excluded) | +1 | −1 |
| S3b (→ persistent) | −1 | +1 |
| S4 (pair-object symmetry) | +1 | −1 |

### Per-branch aggregates

| | Map-V0-I | Map-V0-II | Gap |
|---|---:|---:|---:|
| Fixed subtotal (S1+S2+S4) | +3 | −3 | 6 |
| Under S3a | +4 | −4 | 8 |
| Under S3b | +2 | −2 | 4 |

### Per-branch verdicts

- **S3a:** PASS-V0-I (Map-V0-I ≥ +3, Map-V0-II ≤ +1, gap ≥ 2).
- **S3b:** FAIL (neither map reaches +3).

### Final verdict

**UNCLEAR by Sensitivity** (branches disagree).

---

## Verification Hooks

Any reproducing scorer should verify:

V0 structural facts:
- [ ] |V0| = 19 cells.
- [ ] |V0_Z| = 17 cells (all V0 cells except (0,7) and (7,0)).
- [ ] |V0_H| = 2 cells = {(0,7), (7,0)}.
- [ ] V0_H cells are swap-symmetric: (0,7) ↔ (7,0).

Per-source predicate checks:
- [ ] Source 1: V0_Z is 89% majority + aligns with Rule (b) default.
- [ ] Source 2: V0_H is minority + override + restricted to h=7.
- [ ] Source 4: V0_H is exactly 2 swap-symmetric cells.
- [ ] Source 3a scores Map-V0-I +1, Map-V0-II −1.
- [ ] Source 3b scores Map-V0-I −1, Map-V0-II +1.

Per-branch aggregates:
- [ ] Fixed subtotal = +3/−3.
- [ ] S3a aggregate = +4/−4, gap 8.
- [ ] S3b aggregate = +2/−2, gap 4.

Branch verdicts:
- [ ] S3a → PASS-V0-I.
- [ ] S3b → FAIL.

Final verdict:
- [ ] Branches disagree → UNCLEAR by Sensitivity.

---

## Command to Rerun

```bash
cd /home/claude/foundation_sprint/ppm_v30
python3 ppm_v30_score.py
```

Expected runtime: < 1 second. Produces `PPM_V30_V0_SCORES.json`.

---

## Potential Sources of Reproduction Divergence

### Divergence point 1 — Introducing a third Source 3 reading

A scorer might propose an alternative attractor-privilege argument direction beyond S3a and S3b.

**Anti-divergence rule:** §8 item 8 explicitly prohibits third Source 3 readings in this sprint. Any alternative argument requires pre-registration of v3.0.1+.

### Divergence point 2 — Relaxing a fixed source criterion

A scorer could argue that Source 1's "default vs override" distinction is not forced by Rule (b) (both clauses are part of the rule), or Source 2's "restricted to distinguished element" criterion is over-specific, or Source 4's "exactly 2 cells" is too strict.

**Anti-divergence rule:** §8 prohibits substitutions on any source. The fixed sources' criteria are frozen verbatim.

### Divergence point 3 — Source 4 demotion mid-run

A scorer could argue Source 4 is framework-loaded and should be moved to diagnostic-only.

**Anti-divergence rule:** user discipline explicitly prohibits Source 4 demotion mid-run. Source 4 remains scored for this sprint version.

### Divergence point 4 — Robustness rule reinterpretation

A scorer could argue the S3b FAIL is "close" to passing (Map-V0-I = +2, just one point below threshold) and should be treated as a soft PASS.

**Anti-divergence rule:** §7.1 per-branch threshold is exactly +3. +2 is below threshold, not close to it. §7.2 robustness rule triggers UNCLEAR by Sensitivity on any branch disagreement — no soft-verdict option exists.

### Divergence point 5 — Reframing UNCLEAR by Sensitivity

A scorer could describe the result as "near-pass" or "50% PASS" or similar soft framings.

**Anti-divergence rule:** user discipline explicitly prohibits these framings. UNCLEAR by Sensitivity is the earned diagnostic verdict category, not a position on the PASS/FAIL spectrum.

---

## Cross-Sprint Position

| # | Spec | Path | Operationalization | Verdict | Key result |
|---|---|---|---|---|---|
| 12 | PPM-v1.0 | 1 | Multiplicative | PASS (Map B) | +4/−4, gap 8 |
| 13 | PPM-v1.1 | 1 | Additive | FAIL | +2/−2, gap 4, sub-threshold |
| 14 | PPM-v2.0 | 3 | Multiplicative | PASS (uniform) | $N_B = 8/8$, gap 8 |
| 15 | PPM-v2.1 | 3 | Additive | FAIL (Uniform) | $N_B = N_A = 0$, gap 4 uniform |
| 16 | **PPM-v3.0** | **1 (V0)** | **V0-adapted, S3 sensitivity** | **UNCLEAR by Sensitivity** | **S3a PASS-V0-I, S3b FAIL; first sensitivity-branch outcome** |

Sixteen sprints under discipline. The pair-primitive framework has five PPM checkpoints: four at the seam subtype-mapping checkpoint (v1.0–v2.1, complete 2×2) and one at the V0 boundary (v3.0, sensitivity-diagnostic).

---

## If Rerun Gives a Different Verdict

All inputs are static. The rubric is prose-specified and deterministic. Divergence must come from:

1. Introducing a third S3 reading (prohibited per §8).
2. Relaxing or substituting fixed-source criteria (prohibited per §8).
3. Demoting Source 4 mid-run (prohibited per user discipline).
4. Reinterpreting the robustness rule (§7.2 definitions are strict).
5. Inflating UNCLEAR by Sensitivity into a soft verdict (prohibited per user discipline).

The UNCLEAR by Sensitivity verdict with S3a → PASS-V0-I, S3b → FAIL, aggregates +4/−4 (gap 8) and +2/−2 (gap 4) respectively, is the deterministic output of the frozen spec. Any correct reimplementation reproduces this result.

---

## Integrity

- No external inputs beyond the frozen pre-reg and `CANONICAL_TSML_CONSTRUCTION.md` Rule (b).
- All 16 per-source-per-branch-per-map scores traceable to specific rubric clauses.
- Prohibited substitutions honored (§8).
- Source 4 remained scored throughout (user discipline).
- Robustness rule applied strictly (§7.2).
- UNCLEAR by Sensitivity recorded as earned diagnostic, not as soft verdict.
- Pilot prediction matched rubric-scored result at every level.
- No post-hoc rubric adjustment.
- v1.0, v1.1, v2.0, v2.1 verdicts unaffected.
- B2-pack sprint verdicts unaffected.
- SAH at foundation register unaffected.
- Rule 19 enforced: no composite claim merging v3.0 with prior PPM verdicts.
