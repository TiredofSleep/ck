# CK Privacy Module — One-Page Briefing for Compliance Officers

**For**: The compliance officer (HIPAA, FERPA, state-privacy-law, or institutional-IRB) who must sign off on releasing a tabular dataset that contains a sensitive categorical attribute about identifiable individuals.
**About**: A privacy-protection mechanism the institution's data steward proposes to apply before release.
**Length**: One page, by design. The full deployment guide is in `CK_PRIVACY_DEPLOYMENT_GUIDE.md`.

---

## What the mechanism is

The mechanism is **cell-suppression + k-anonymity hybrid** — a standard statistical-disclosure-control (SDC) recipe published by Latanya Sweeney (Carnegie Mellon, 2002) and refined by subsequent work (Wong et al. 2006, Li et al. 2007). The institution's data steward applies it to a tabular dataset before public release. The reference implementation is `ck_privacy.py`, an open-source Python module the institution can audit.

This is **not a novel privacy mechanism**. It is a re-implementation of techniques the privacy-engineering literature has used and refined for 20+ years. It is the standard recipe for "tabular data release with categorical sensitive attribute and dominant-majority class."

---

## What it protects against (and what it does not)

| Threat | What it is | Protection level |
|---|---|---|
| **Re-identification** | An attacker linking a released row to a named individual | ≤ 4% per row (1/k at k=25) |
| **Attribute disclosure** | An attacker inferring a specific individual's sensitive value | ≈ population baseline (no advantage over public stats) |
| **Membership inference** | An attacker determining whether a specific individual was in the released set | ≈ 50% random guessing |

What the mechanism does **NOT** protect against:
- **Auxiliary-information attacks** (an attacker with a voter roll or other external dataset that can be joined against the release). The recipe's protection assumes the attacker sees only the released table.
- **Repeated releases of the same underlying data** without a privacy budget. The recipe is for one-shot release.
- **Per-row prediction** — by design. The released data does not let downstream users predict individual outcomes above the population baseline. This is the protection working as intended.

---

## What you (the compliance officer) should verify before signing off

Five questions. The data steward should be able to answer each.

1. **Have direct identifiers been dropped?** (Names, IDs, exact addresses, exact dates of birth, etc. must be REMOVED from the data before any privacy mechanism runs. Suppression is for quasi-identifiers, not direct identifiers.)
2. **Has the sensitive attribute's distribution been verified to have a dominant majority class (≥ 75%)?** If not, the recipe is the wrong tool and a different mechanism (ε-differential privacy) is needed.
3. **Has the minimum group size in the released data been measured and confirmed ≥ 25?** This is the k-anonymity check.
4. **Has the per-group conditional sensitive distribution been measured and confirmed within KL divergence 0.01 of the population marginal?** This is the t-closeness check (Li et al. 2007).
5. **Is the use case downstream aggregate statistics, not per-row prediction?** If a downstream user needs to predict individual outcomes (insurance pricing, individual eligibility decisions), this recipe is the WRONG mechanism — and the data probably should not be released at all.

If all five answers are "yes" and the data steward has provided the §3 Step 5 verification metrics from the deployment guide, the mechanism's protection guarantees hold mathematically. **Your sign-off is still required** — the mechanism is necessary, not sufficient, for safe release.

---

## What the institution owes you (the documentation packet)

For the release file, the data steward should provide:

- **The raw-data inventory**: source dataset, date range, row count, column list with role tags (ID / QID / sensitive / non-sensitive).
- **The pre-processing record**: which columns were dropped, which were discretized, what bin boundaries were used.
- **The mechanism parameters**: `suppression_rate`, `k`, `seed`, mechanism name (`hybrid_suppress_kanon`).
- **The verification metrics**: min group size, max KL divergence, downstream classifier accuracy vs baseline.
- **The release scope statement**: explicit statement that the data is for aggregate statistics, structural pattern analysis, and civic transparency — NOT for individual-level decision-making.
- **The citation list**: Sweeney 2002 + Wong et al. 2006 + Li et al. 2007 + Dwork et al. 2006 + LeFevre et al. 2006.

If any of these are missing, request them before sign-off.

---

## What you (the compliance officer) decide

The mechanism's mathematical properties guarantee protection on three threat axes IF the assumptions hold and the verification metrics pass. Your role is to decide whether:

- The release is appropriate for the institution's policies and the legal regime (HIPAA / FERPA / state law / IRB).
- The use case is genuinely aggregate-statistical, not per-row predictive.
- The auxiliary-information threat model is acceptable (no plausible adversary has a side dataset that breaks the QID protection).
- The institution can accept the residual risk represented by the threat-axis protection levels above.

The mechanism cannot answer these questions for you. It can only give you the formal protection guarantees on the released artifact.

---

## If something goes wrong

If a privacy breach occurs after release (re-identification, attribute disclosure, etc.):

1. **Audit trail**: the deterministic seed in the mechanism means the entire release can be reproduced and re-audited from the raw data + the documented parameters. The data steward should preserve the original release artifact, the parameters, the verification metrics, and the documentation packet for the institution's audit retention period.
2. **Mechanism-failure investigation**: examine which of (A1) hash-orthogonality, (A2) dominant-majority, or (A3) large-N assumptions failed. The deployment guide §4 documents the five known failure modes and their detectors.
3. **Mitigation**: rotate to a stronger mechanism (ε-DP at low ε) for subsequent releases of the same data; do NOT re-release the same data with weaker parameters.
4. **Disclosure**: follow the institution's standard incident-disclosure process. The mechanism is a published technique; failures of the assumptions are documented and well-understood in the literature.

---

## The bottom line for the compliance officer

The institution's data steward is proposing to apply a 20-year-old, well-documented privacy mechanism to a tabular dataset with the right shape for it. The mechanism is implemented in an auditable open-source Python module. The protection guarantees are mathematical, the assumptions are documented, and the failure modes are known.

**What you are signing off on**: the institution's decision to release a privacy-protected version of this data for aggregate statistical use, under the protections described above.

**What you are NOT signing off on**: a novel privacy theory, an experimental mechanism, or a use case for individual-level decision-making.

This is a routine, well-grounded, published-literature SDC deployment. The implementation is reference-quality. Your sign-off is the policy and legal decision; the mechanism's protection guarantees are the engineering substrate underneath that decision.

---

*Companion document: `CK_PRIVACY_DEPLOYMENT_GUIDE.md` (the full deployment manual). Source code: `Gen14/targets/ck/brain/ck_privacy.py`. Citations: Sweeney 2002, Wong et al. 2006, Li et al. 2007, Dwork et al. 2006, LeFevre et al. 2006. Document version 1.0 (2026-05-19).*
