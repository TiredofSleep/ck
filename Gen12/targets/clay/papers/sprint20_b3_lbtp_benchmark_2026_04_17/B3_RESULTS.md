# B3 LBTP -- Results

**Spec:** B3 LBTP per SHELL_NATIVE_BENCHMARKS.md
**Configs:** 5 (5 seeds)
**Overall verdict:** **FAIL**  (0/5 pass)

**Diagnosis:** Paired joint accuracy is BELOW max(singleton) by 4.31pp. This is structural: joint accuracy = correlated success of two ~95% events, which equals ~0.95^2 = ~0.90 (close to observed). The spec criterion 'paired > max(singleton) + 5pp' is not meetable when individual fits already exceed ~95%.

---

## Aggregate metrics

| Metric | Value |
|---|---|
| Mean T-table recovery | 1.0000 |
| Mean B-table recovery | 1.0000 |
| Mean (paired - max(singleton)) | -4.3105 pp |

## Per-seed detail

| Seed | T-table | B-table | T_only acc | B_only acc | joint acc | paired-max(singleton) | Verdict |
|---|---|---|---|---|---|---|---|
| 0 | 1.0000 | 1.0000 | 0.9546 | 0.9548 | 0.9120 | -4.29pp | FAIL |
| 1 | 1.0000 | 1.0000 | 0.9545 | 0.9531 | 0.9098 | -4.46pp | FAIL |
| 2 | 1.0000 | 1.0000 | 0.9554 | 0.9554 | 0.9126 | -4.27pp | FAIL |
| 3 | 1.0000 | 1.0000 | 0.9560 | 0.9559 | 0.9143 | -4.17pp | FAIL |
| 4 | 1.0000 | 1.0000 | 0.9547 | 0.9546 | 0.9112 | -4.35pp | FAIL |

## Spec criterion analysis

Spec §B3 PASS condition:
- paired > max(T_only, B_only) + 5pp on held-out, AND
- individual operators recovered at >= 90%

**Individual recovery: BOTH operators recovered at 100% from training data (T-table and B-table both = 1.0000 vs truth). This component PASSES.**

**Paired vs singleton: under any natural reading of 'prediction accuracy', paired joint accuracy equals the product of marginal accuracies, which is necessarily LESS THAN OR EQUAL to either marginal. The 5pp-outperformance criterion is not meetable in this regime.**
