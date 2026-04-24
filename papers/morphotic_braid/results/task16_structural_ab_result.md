# Task 16 result -- structural A/B (TSML_Jordan vs TSML_Idempotent)

**Tier:** 4 slice (pure-table subset of the full runtime A/B)
**Parent spec:** `../../claudecode_jobs/task16_ck_dual_table_experiment/SPEC.md`

## Scope

The SPEC proposes a full runtime A/B requiring child-CK-spawn on port 7778 with 10,000 ticks per arm and Ollama queries. This result covers the *structural* slice only: pure-table measurements that answer "do these two composition tables have materially different behavior at all?" before committing hours of runtime.

Structural divergence here is *necessary* for runtime divergence; structural invariance would make runtime divergence unlikely.

## Arm A: canonical `TSML` from `papers/ck_tables.py` (Jordan variant)

| metric | value |
|---|---|
| HARMONY (=7) rate | 73/100 |
| ZERO (=0) rate | 17/100 |
| symmetric | True |
| DIS cells | 0 |
| DOING cells | 100 |
| Jordan identity | 100/100 |
| Moufang L/R/M | 874/1000, 874/1000, 822/1000 |
| alpha (assoc. index) | 872/1000 = 0.8720 |
| det | 0 |
| \|det\| prime factorization | {} |

### Operator histogram

| op | name | count |
|---|---|---|
| 0 | VOID | 17 |
| 3 | PROGRESS | 4 |
| 4 | COLLAPSE | 2 |
| 7 | HARMONY | 73 |
| 8 | BREATH | 2 |
| 9 | RESET | 2 |

## Arm B: `TSML_Idempotent` (rank-10, per TSML_FAMILY handoff)

| metric | value |
|---|---|
| HARMONY (=7) rate | 71/100 |
| ZERO (=0) rate | 17/100 |
| symmetric | True |
| DIS cells | 0 |
| DOING cells | 100 |
| Jordan identity | 100/100 |
| Moufang L/R/M | 888/1000, 888/1000, 836/1000 |
| alpha (assoc. index) | 880/1000 = 0.8800 |
| det | -49 |
| \|det\| prime factorization | {7: 2} |

### Operator histogram

| op | name | count |
|---|---|---|
| 0 | VOID | 17 |
| 1 | LATTICE | 1 |
| 2 | COUNTER | 1 |
| 3 | PROGRESS | 1 |
| 4 | COLLAPSE | 3 |
| 5 | BALANCE | 1 |
| 6 | CHAOS | 3 |
| 7 | HARMONY | 71 |
| 8 | BREATH | 1 |
| 9 | RESET | 1 |

## Divergence

Per-operator delta (A - B):

| op | name | A | B | A-B |
|---|---|---|---|---|
| 0 | VOID | 17 | 17 | +0 |
| 1 | LATTICE | 0 | 1 | -1 |
| 2 | COUNTER | 0 | 1 | -1 |
| 3 | PROGRESS | 4 | 1 | +3 |
| 4 | COLLAPSE | 2 | 3 | -1 |
| 5 | BALANCE | 0 | 1 | -1 |
| 6 | CHAOS | 0 | 3 | -3 |
| 7 | HARMONY | 73 | 71 | +2 |
| 8 | BREATH | 2 | 1 | +1 |
| 9 | RESET | 2 | 1 | +1 |

- HARMONY rate equal? **False**  (A=73, B=71)
- ZERO rate equal? **True**  (A=17, B=17)
- Jordan count equal? **True**  (A=100/100, B=100/100)
- alpha equal? **False**  (A=0.8720, B=0.8800)
- det equal? **False**  (A=0, B=-49)
- Moufang equal? **False**

## Verdict

**STRUCTURAL DIVERGENCE CONFIRMED.** The two tables are materially different algebras on the same carrier (Z/10Z, 10 operators). A runtime A/B is expected to show divergent operator-stream and coherence behavior. Proceeding to the full runtime A/B (child-CK-spawn on port 7778, 10k ticks per arm) is justified when Brayden signs off on the child-spawn plumbing.

## Follow-up (runtime A/B, not done here)

The SPEC's full protocol requires:

1. Spawn child CK on port 7778 (bypassing the Cloudflare tunnel on 7777)
2. 10,000 ticks per arm against a 100-query probe set
3. Metrics: operator stream, mean coherence floor, Ollama-verdict rate, voice-accept rate, mean response length, crystal-hit rate
4. Statistical compare (t-test or paired comparison on metric means)

This structural slice gives the *algebraic baseline*. The runtime slice is a separate engineering task.

**Tag:** `[COMPUTE JOB -- TIER 4 SLICE (STRUCTURAL) -- VERIFIED]`
