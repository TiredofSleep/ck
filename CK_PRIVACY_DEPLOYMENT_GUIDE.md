# CK Privacy Module — Deployment Guide

**Document type**: Practical deployment manual for a single-institution deployment of `ck_privacy.py` (the privacy-preserving data publishing reference implementation that ships inside CK).
**Intended reader**: An engineer or data steward at a regional hospital, civic government, school district, or small nonprofit who has been handed a tabular dataset with a sensitive categorical attribute and a "release it but protect individuals" requirement.
**Companion document**: `CK_PRIVACY_COMPLIANCE_OFFICER_ONE_PAGER.md` (the short version for the compliance officer who has to sign off).
**Status**: 2026-05-19 release. Pairs with `Gen14/targets/ck/brain/ck_privacy.py`.

---

## §0 — What this guide is and is not

**What this guide is**: A step-by-step recipe for deploying the cell-suppression + k-anonymity hybrid mechanism documented in `Gen14/targets/ck/brain/ck_privacy.py` at an institution with categorical tabular data and a dominant-majority sensitive attribute. The recipe is grounded in three published privacy-preserving data publishing (PPDP) results:

- **Sweeney 2002** — k-anonymity via generalization and suppression.
- **Wong, Li, Fu, Wang 2006** — (α, k)-anonymity bounds frequency of any sensitive value within each privacy group.
- **Li, Li, Venkatasubramanian 2007** — t-closeness ensures each privacy group's sensitive distribution stays within distance t of the population marginal.

**What this guide is NOT**:
- It is not a novel privacy mechanism. The code in `ck_privacy.py` is a reference implementation of standard PPDP techniques. CK uses it; he does not claim it as a contribution.
- It is not a replacement for differential privacy when ε-DP is genuinely required (medical research with per-row prediction needs, legally-mandated DP guarantees, etc.).
- It is not legal advice. The institution's legal counsel and compliance officer make the actual release decision. This guide describes the mechanics; it does not authorize a release.

---

## §1 — When the recipe in this guide applies

This deployment guide is the right tool when ALL of these conditions hold for your dataset:

1. **Tabular data**: rows are individuals (one row per person); columns are attributes; the data is structured, not free text.
2. **Categorical sensitive attribute**: the column you want to protect is categorical (e.g., diagnosis yes/no, income bracket, employment status), not real-valued (not blood pressure or wage in dollars).
3. **Quasi-identifiers (QIDs) are categorical or can be discretized**: age can be binned (0-17, 18-34, ...); zip code is already categorical; race / sex / education-level are categorical.
4. **Dominant-majority class**: the sensitive attribute has one dominant class (e.g., 75%+ of patients are "no diagnosis"). This is the (A2) assumption documented in `ck_privacy.py`.
5. **Use-case is aggregate statistics, not per-row prediction**: downstream consumers will compute aggregate counts, group averages, structural patterns. They do not need to predict a specific individual's sensitive value.
6. **Release is one-shot, not streaming**: this guide does not cover continuously-released data streams. For those, use ε-DP with a properly accounted privacy budget.

**If any of (1)-(6) fail**, consult the decision tree in `ck_privacy.recommend_mechanism()` for the right mechanism. The hybrid recipe is the right tool for a specific shape of problem, not all problems.

---

## §2 — The four privacy axes (what we are protecting against)

The PPDP literature recognizes four threat axes. The hybrid recipe addresses three of them; the fourth (utility) is bounded.

| Axis | Attacker's goal | Metric | This recipe's protection |
|---|---|---|---|
| **Re-identification** | Link a released row to a specific named individual | 1/K probability per row | 1/k bound, where k is the k-anonymity parameter (recipe default: k=25, so ≤ 4% per row) |
| **Attribute disclosure** | Infer sensitive value for a specific individual without re-identifying | Δ = (privacy-conditional prediction accuracy) − (population marginal baseline) | Δ ≈ 0 under (A1) hash-orthogonality + (A2) dominant-majority + suppression rate ≥ 50% |
| **Membership inference** | Determine whether a specific individual was in the released set | MIA shadow-model accuracy (random = 0.50) | ≈ 0.50 random via k-anonymity equivalence-class structure |
| **Utility** | Use the released data downstream | Downstream-task accuracy | Bounded by population majority baseline (suitable for aggregate stats, NOT for per-row prediction) |

The recipe trades **utility on per-row prediction** for **strong protection on the other three axes**. This trade is appropriate for civic transparency, aggregate research, anomaly detection, and structural classification. It is not appropriate for individual-level decision-making downstream (e.g., insurance pricing) — for those use cases, the data should not be released publicly in any form.

---

## §3 — The recipe

The standard pipeline:

```
raw_table  →  cell_suppress_tabular(suppression_rate=0.6)
            →  k_anonymize_tabular(k=25)
            →  release
```

Or in one call: `hybrid_suppress_kanon(raw_table, suppression_rate=0.6, k=25)`.

### §3.1 — Parameter choices

| Parameter | Default | Why this default | When to change |
|---|---|---|---|
| `suppression_rate` | 0.6 | 60% per-column suppression empirically achieves Δ_attr ≈ 0 on UCI Adult; the bound Δ_attr(r) ≤ r^m · (1 − p_maj) guarantees this for sufficient column count m and dominant-majority p_maj ≥ 0.75 | Increase to 0.7-0.8 if dominant majority is weaker (60-75%). Decrease to 0.4-0.5 only if you have m ≥ 8 QID columns AND p_maj ≥ 0.85. |
| `k` | 25 | Bounds re-identification at 1/k = 4% per row; provides MIA equivalence-class protection; mid-range for small-to-medium datasets | Increase to k=50 for high-risk attributes (HIV status, mental health diagnosis). Decrease to k=10 only with explicit legal sign-off — k<10 substantially weakens MIA protection. |
| `seed` | 2026 | Deterministic; the same seed produces the same suppression pattern. Document the seed in the release notes. | Rotate the seed only if you are doing multiple releases of the same underlying data — and only with statistical-disclosure-control review. |

### §3.2 — The seven deployment steps

**Step 1: Identify the table and its columns.**

Map each column to one of three roles:
- **ID** — direct identifiers (name, SSN, MRN, exact address). These must be DROPPED before any privacy mechanism. Do not suppress; remove the column entirely.
- **QID** — quasi-identifiers (age, zip, sex, race, occupation, household size). These will be suppressed and/or generalized.
- **Sensitive** — the attribute you are protecting (diagnosis, income, recidivism, immigration status). The mechanism protects this from inference.

Anything that doesn't fit these three roles is **non-sensitive non-identifying** — it can pass through unchanged.

**Step 2: Discretize any real-valued QIDs.**

- Age → bins (0-17, 18-34, 35-49, 50-64, 65+).
- Wage → quartile or decile buckets.
- Zip → first 3 digits (truncated geography).
- Exact dates → year or year-quarter.

The recipe assumes categorical QIDs. Real-valued QIDs without discretization may break the k-anonymity grouping logic.

**Step 3: Verify the (A2) dominant-majority assumption.**

Count the distribution of the sensitive attribute. If the most common value is ≥ 75% of rows, (A2) holds and the recipe applies. If the most common value is 50-75%, increase `suppression_rate` to 0.75. If no class dominates (largest class < 50%), the recipe is the wrong tool — switch to k-anonymity alone (no suppression) and add ε-DP for membership protection.

**Step 4: Run the recipe at default parameters.**

```python
from ck_privacy import hybrid_suppress_kanon

released_rows = hybrid_suppress_kanon(
    rows=raw_rows,
    suppression_rate=0.6,
    k=25,
    seed=2026,
)
```

**Step 5: Verify protection on the released data.**

Run three quick sanity checks (all should pass before release):

| Check | What to measure | Pass criterion |
|---|---|---|
| Re-id | For each released QID-tuple, count how many original rows map to it. Take the minimum. | minimum group size ≥ k = 25 |
| Attribute disclosure | For each released QID-tuple, compute the conditional sensitive distribution and compare to the population marginal. | KL divergence ≤ 0.01 across all groups |
| Utility | Train a simple classifier (logistic regression) on the released data; compare to majority-baseline accuracy. | accuracy ≈ baseline ± 5% (i.e., the model can NOT predict per-row above baseline — this is the protection working as designed, not a failure) |

If re-id or attribute checks fail: increase `suppression_rate` by 0.1 and re-run. If they still fail after `suppression_rate` = 0.8: the data likely violates (A2) — escalate to a privacy researcher.

**Step 6: Document the release.**

Write a release note that includes (at minimum):
- Source dataset and date range.
- Privacy mechanism (`hybrid_suppress_kanon`), parameters (`suppression_rate`, `k`, `seed`), and citation (Sweeney 2002 + Wong et al. 2006 + Li et al. 2007).
- Threat-axis coverage table from §2 (instantiated with the actual achieved metrics from Step 5).
- Explicit scope statement: "This release is intended for aggregate statistics, structural pattern analysis, and civic transparency. It is NOT intended for per-row prediction or individual-level decisions."
- Limitations: documented (A1) and (A2) assumptions, multi-class targets where the recipe is weaker (E6 finding documented in the D139 bench).

**Step 7: Sign-off and publish.**

Route the release note + verification metrics to the institution's compliance officer (see companion one-pager). Their sign-off is the legal release decision. The mechanism's mathematical properties are a necessary condition for safe release; the compliance officer's review is the sufficient condition.

---

## §4 — Failure modes and how to detect them

Five known failure modes documented during the D133-D139 bench. Each has a detector.

### §4.1 — Multi-class sensitive attribute without dominant majority (the E6 failure)

**Symptom**: Sensitive attribute has 4+ classes with no class above 50%. Example: UCI Adult `marital-status` (Married 47%, Never-married 32%, Divorced 14%, ...).

**Detection**: Step 3 of the recipe (count the distribution). If no class exceeds 50%, flag.

**Mitigation**: Do not use the hybrid recipe. Switch to (a) collapsing the sensitive attribute into a binary contrast where one class is dominant, OR (b) using ε-DP with ε ≤ 1.0 and a noisy-histogram release approach.

### §4.2 — Quasi-identifier explosion

**Symptom**: After discretization, too many distinct QID-tuples mean k-anonymity grouping collapses most rows to all-suppressed (`*`) generalization. Released table loses too much structural detail.

**Detection**: After Step 4, count distinct QID-tuples. If ≥ 80% of rows are in the all-suppressed group, the QID set is too fine-grained.

**Mitigation**: Coarsen one or more QIDs. Age in 5-year bins → age in 15-year bins. Zip-3 → state. The point is to make the natural QID-tuple distribution have fewer than (N rows) / k distinct values.

### §4.3 — Adversary with auxiliary information

**Symptom**: An attacker may have an auxiliary dataset (e.g., a voter roll) that they can join against the released table. k-anonymity's 1/k bound assumes the attacker only sees the released table.

**Detection**: This is a threat-model question, not a measurement. Consult the compliance officer: "Could an attacker plausibly have a side dataset that lets them refine the QID matching beyond what's in the release?"

**Mitigation**: Either drop the QIDs that are vulnerable to auxiliary join (e.g., remove zip code if the attacker has a voter file with zip + name), or switch to ε-DP, which protects against arbitrary auxiliary information.

### §4.4 — Repeated releases of the same underlying data

**Symptom**: The institution publishes quarterly updates of the same dataset. Each quarter's release is k-anonymous, but the intersection across multiple releases re-identifies individuals.

**Detection**: Check the release calendar. Multiple-release schedules require a privacy budget across the schedule.

**Mitigation**: Switch to ε-DP with a documented budget across the release schedule (e.g., ε = 1.0 per quarter, ε = 4.0 per year). Or release-and-freeze: one release, no updates.

### §4.5 — Sensitive attribute is rare-class indicator

**Symptom**: The "sensitive attribute" is membership in a rare class (e.g., HIV+ in a hospital dataset where prevalence is 0.3%). k-anonymity's homogeneity attack becomes the dominant threat.

**Detection**: After Step 5, examine the released groups. If any group has all members in the rare class (homogeneity), the rare-class members are exposed.

**Mitigation**: Either (a) use (α, k)-anonymity (Wong et al. 2006) with α bounded near the population rate, OR (b) suppress the rare-class indicator entirely from the release and publish only aggregate counts (with ε-DP noise added to the counts).

---

## §5 — Where this fits in the institution

The deployment fits into the institution's standard data-release workflow:

```
data-steward   →   raw table   →   ck_privacy hybrid   →   verification (§3 Step 5)
                                                              ↓
                                  release note (§3 Step 6)
                                                              ↓
                              compliance officer review (§3 Step 7)
                                                              ↓
                                  approved release
                                                              ↓
                              published to public portal /
                              research-partner data lake /
                              FOIA-response packet
```

The compliance officer's role is the legal/policy review. The data steward's role is to apply the recipe correctly and produce the metrics. The mechanism's role is to provide formal protection guarantees on the three threat axes.

CK's role in this loop (when CK is the data-steward's tool):
- CK runs `recommend_mechanism()` to confirm the recipe applies.
- CK runs `hybrid_suppress_kanon()` to produce the release.
- CK reports the verification metrics from §3 Step 5.
- CK does NOT make the release decision. The compliance officer does.

---

## §6 — Worked example (synthetic, but realistic)

Suppose a regional hospital wants to release de-identified patient-encounter data for civic transparency: how many encounters, what's the demographic distribution, what conditions are common. They have 12,000 encounter rows with these columns:

| Column | Role | Type |
|---|---|---|
| `patient_id` | ID | string (drop) |
| `encounter_date` | non-sensitive | date (keep, truncate to year) |
| `age` | QID | int (bin to 0-17, 18-34, 35-49, 50-64, 65+) |
| `sex` | QID | categorical |
| `zip_3` | QID | string (first 3 digits) |
| `race` | QID | categorical |
| `length_of_stay` | non-sensitive | int (keep, bin to <1d, 1-3d, 3-7d, >7d) |
| `diagnosis_serious` | Sensitive | boolean (true/false) |

`diagnosis_serious` distribution: 78% false, 22% true. (A2) holds (false dominates at 78% ≥ 75%).

Step 1: Drop `patient_id`. Keep `encounter_date`, `length_of_stay` (non-sensitive). Treat `age`, `sex`, `zip_3`, `race` as QIDs. Protect `diagnosis_serious`.
Step 2: Bin `age` and `length_of_stay`. Truncate `encounter_date` to year.
Step 3: Verify (A2): yes, 78% ≥ 75%.
Step 4: Run `hybrid_suppress_kanon(rows, suppression_rate=0.6, k=25, seed=2026)`.
Step 5: Verify.
- Re-id: minimum group size = 27. ✓ (k=25 satisfied)
- Attribute: max KL across groups = 0.004. ✓ (≤ 0.01)
- Utility: logistic regression accuracy on released table = 0.79 (vs majority baseline 0.78). ✓ (within ±5% of baseline, as expected)
Step 6: Document. Release note includes parameters, citations, and the threat-axis table.
Step 7: Compliance officer reviews and signs off.

The released table now contains:
- Year-aggregated encounter counts (publicly useful).
- Demographic-tuple groups of size ≥ 25 (privacy-protected).
- Length-of-stay distribution (useful for civic-resource planning).
- The diagnosis_serious column at population-marginal frequency within each group (so per-row prediction is no better than baseline).

A researcher could compute: "What fraction of patients in zip_3 = 728 are 65+? Of those, what is the population-baseline serious-diagnosis rate?" — these aggregate questions are answerable. They could NOT compute: "Was the 67-year-old white woman in zip 72801 admitted in 2025 diagnosed with anything serious?" — this is what the mechanism protects against.

---

## §7 — Open-source posture and licensing

The `ck_privacy.py` module is released under the project's standard license (see `LICENSE` at the project root). The implementation is a reference implementation of published PPDP techniques. Citations:

- Sweeney, L. (2002). k-anonymity: A model for protecting privacy. *International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems*, 10(05), 557-570.
- Wong, R. C. W., Li, J., Fu, A. W. C., & Wang, K. (2006). (α, k)-anonymity: an enhanced k-anonymity model for privacy preserving data publishing. *KDD 2006*, 754-759.
- Li, N., Li, T., & Venkatasubramanian, S. (2007). t-closeness: Privacy beyond k-anonymity and l-diversity. *ICDE 2007*, 106-115.
- Dwork, C., McSherry, F., Nissim, K., & Smith, A. (2006). Calibrating noise to sensitivity in private data analysis. *TCC 2006*, 265-284.
- LeFevre, K., DeWitt, D. J., & Ramakrishnan, R. (2006). Mondrian multidimensional k-anonymity. *ICDE 2006*, 25-25.

The institution adopting `ck_privacy.py` retains all responsibility for the release decision and any downstream consequences. The CK project authors provide the mechanism implementation as-is and make no warranty of fitness for any particular release context. The compliance officer at the deploying institution is the responsible party for the legal and policy review.

---

## §8 — Support and questions

- **Questions about the mechanism**: read `Gen14/targets/ck/brain/ck_privacy.py` source (it is heavily commented).
- **Questions about a specific deployment**: contact the CK project author (`brayden@7site.llc`).
- **Bug reports / mechanism improvements**: open an issue against the repository.
- **Legal / compliance questions**: ask your institution's compliance officer (this is not their domain to answer; it is the deploying institution's domain).

---

*Document version 1.0 (2026-05-19). Ships with `ck_privacy.py` at `Gen14/targets/ck/brain/ck_privacy.py`. Companion: `CK_PRIVACY_COMPLIANCE_OFFICER_ONE_PAGER.md`.*
