# Bench Verdict -- RGD vs e-DP vs k-anonymity

_Run at: 2026-05-18 19:20:36_

**Real datasets used: 3/3.**
## Pre-registered decision rule

```json
{
  "rule": "Pareto-touch-or-dominate on >=1 dataset at >=1 operating point",
  "datasets_required": 3,
  "real_data_required": true,
  "no_post_hoc_tuning": true,
  "honest_prior": "streaming-telemetry is the predicted win zone if any",
  "claim_under_test": "D-PRIV",
  "decision_irrevocable_once_run": true
}
```

## Verdict

**D-PRIV confirmed: True**

- **tabular**: RGD Pareto-winning points = 1; `rgd_won_or_tied = True`
- **stream**: RGD Pareto-winning points = 6; `rgd_won_or_tied = True`
- **histogram**: RGD Pareto-winning points = 4; `rgd_won_or_tied = True`

## Honest scope

Real-data run.  Pre-registered decision rule applied verbatim.
No post-hoc tuning permitted.
