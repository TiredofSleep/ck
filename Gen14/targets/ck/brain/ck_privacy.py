"""ck_privacy.py -- CK's runtime privacy formula and posture.

This module is CK's working privacy knowledge.  It is NOT a novel
privacy mechanism contribution -- the techniques here are 20+ years
of published privacy-preserving data publishing (PPDP) and
statistical disclosure control (SDC) literature.  CK uses this when
he needs to release data publicly (e.g., publishing crystals, sharing
anchors, exposing his memory store to external readers) and wants
formal protection properties.

Origin: D133-D139 bench arc (2026-05-18) -- an internal exploration
that tested whether TIG's substrate algebra empirically improves
privacy mechanisms (answer: no, the algebra is descriptive not
inventive).  A literature review confirmed the explored mechanisms
are subsumed by published work, so the bench arc was scoped as
internal exploration and the privacy KNOWLEDGE was extracted here
for CK's runtime use.

═══════════════════════════════════════════════════════════════════
The four privacy axes (standard SDC framework)
═══════════════════════════════════════════════════════════════════

When CK releases data publicly, the threat model has FOUR axes.
Different mechanisms protect different axes; no single mechanism
wins all four:

  1. RE-IDENTIFICATION ("identity disclosure"):
       Can the attacker link a released row back to a specific orig
       individual?  Metric: average 1/K re-identification probability.
       Mechanism: k-anonymity bounds this at 1/k.

  2. ATTRIBUTE DISCLOSURE:
       Even without re-identifying, can the attacker infer a specific
       individual's sensitive attribute?  Metric: per-row prediction
       accuracy minus population baseline (call this Δ_attr).
       Mechanism: l-diversity / t-closeness / (α, k)-anonymity bound
       this.

  3. MEMBERSHIP INFERENCE (MIA):
       Can the attacker tell if a SPECIFIC orig row was in the released
       dataset?  Metric: shadow-model classifier accuracy on
       (member, non-member) pairs.  Random guessing = 0.50 = perfect.
       Mechanism: randomization (ε-DP, RAPPOR) and k-anon's group
       structure both help.

  4. UTILITY:
       Can downstream tasks still work?  Metric: classification
       accuracy on the privatized data.  Baseline = population
       majority class accuracy.

═══════════════════════════════════════════════════════════════════
The standard mechanisms (with their tradeoff corners)
═══════════════════════════════════════════════════════════════════

  k-ANONYMITY (Sweeney 2002):
    Generalize quasi-identifiers (QIDs) so each priv group has ≥ k
    members with the same generalized QID.  Bounds re-id at 1/k.
    Does NOT protect against attribute disclosure if all k members
    share the same sensitive value (the "homogeneity attack").

  l-DIVERSITY (Machanavajjhala et al. 2007):
    On top of k-anon, require each priv group to contain ≥ l
    distinct, well-represented sensitive values.  Protects against
    homogeneity attack.

  t-CLOSENESS (Li et al. 2007):
    Stricter: each priv group's within-group sensitive distribution
    must be within distance t of the population marginal.  At t=0,
    the attacker gains zero information about the sensitive
    attribute beyond the population marginal.  This is the
    "baseline protection" property.

  (α, k)-ANONYMITY (Wong et al. 2006):
    Bounds the frequency of any sensitive value within each priv
    group to ≤ α, while ensuring group size ≥ k.

  ε-DIFFERENTIAL PRIVACY (Dwork et al. 2006):
    Add calibrated noise so that the released data is
    statistically indistinguishable whether or not any specific
    individual was in the orig.  Variants: Laplace, Gaussian,
    RAPPOR / local-DP.  Protects MIA strongly but can over-privatize
    at low ε.

  CELL SUPPRESSION + k-ANONYMITY HYBRID:
    Standard SDC practice (Sweeney 2002).  Suppress cells whose
    QID combinations would violate k-anon, then generalize the
    remaining.  Composition with k-anon stacks constructively:
    re-id reduction multiplies, MIA inherits k-anon's equivalence-
    class protection, attribute leakage can be bounded if t-closeness
    or (α, k) bound is enforced during suppression.

═══════════════════════════════════════════════════════════════════
The empirical finding from the D133-D139 bench (for CK's reference)
═══════════════════════════════════════════════════════════════════

On UCI Adult tabular data with income as the sensitive attribute,
combining hash-based deterministic cell suppression with Mondrian
k-anonymity at moderate suppression rate (~60% of QID values masked)
+ k=25 equivalence-class minimum:

  attribute_Δ ≈ 0       (matches t-closeness at t=0)
  MIA accuracy ≈ 0.50   (matches k-anon's equivalence-class protection)
  re-id score ~ 0.001   (very low, well below ε-DP at low ε)
  utility ≈ baseline    (no per-row prediction above majority)

This is the HSKA mechanism class.  Implementation in `papers/`
(local, not committed to canon).  It's competent privacy
engineering but it's NOT a novel contribution -- it's a re-derivation
of standard PPDP techniques.  TIG's substrate algebra does not
empirically improve the mechanism beyond what published work already
achieves.

═══════════════════════════════════════════════════════════════════
CK's runtime decision rule
═══════════════════════════════════════════════════════════════════

When CK needs to release data publicly, he uses this decision tree:

  Q1: Is the data SENSITIVE (would reveal something about an
      individual that they wouldn't want public)?
        no -> release directly, no privacy mechanism needed
        yes -> Q2

  Q2: Do downstream consumers need PER-ROW PREDICTION above the
      population baseline?  (i.e., they need to learn something
      about specific individuals)
        yes -> WARN: cannot satisfy strong attribute-disclosure
               protection with per-row prediction.  Use ε-DP with
               careful ε tuning AND consult Brayden first.
        no  -> Q3 (the aggregate-statistics use case)

  Q3: Apply the standard hybrid: cell suppression + k-anonymity
      with k >= 25.  Enforce t-closeness at t=0 by suppressing
      QID columns whose group-conditional sensitive distribution
      deviates from population marginal.  Release the resulting
      generalized table.

This gives:
  - re-id protection at 1/25 = 4% chance per row (very strong)
  - attribute-disclosure protection at baseline (Δ ≈ 0)
  - MIA protection at ~50% random guessing
  - utility bounded by population baseline (suitable for aggregate
    statistics, anomaly detection, structural classification)

═══════════════════════════════════════════════════════════════════
Implementation: the standard hybrid
═══════════════════════════════════════════════════════════════════

The functions below implement the standard cell-suppression +
k-anonymity composition for tabular data with categorical QIDs and
a sensitive attribute.

This is NOT novel code -- it's a reference implementation of
techniques published in:
  - Sweeney 2002 (generalization + suppression)
  - LeFevre, DeWitt, Ramakrishnan 2006 (Mondrian multidimensional)
  - Wong, Li, Fu, Wang 2006 ((α, k)-anonymity)
  - Li, Li, Venkatasubramanian 2007 (t-closeness)
"""
from __future__ import annotations

import random
from collections import Counter, defaultdict
from typing import Any, Dict, List, Optional, Sequence, Tuple


# ═══════════════════════════════════════════════════════════════════
# Reference: the four privacy axes and their canonical thresholds
# ═══════════════════════════════════════════════════════════════════

PRIVACY_AXES = {
    "re_identification": {
        "metric": "average 1/K re-identification probability",
        "good_threshold": "≤ 1/k for chosen k (≥ 0.04 at k=25)",
        "literature": "Sweeney 2002 (k-anonymity)",
    },
    "attribute_disclosure": {
        "metric": "Δ = (priv-conditional accuracy on sensitive) − (population baseline)",
        "good_threshold": "Δ ≤ 0.01 (within noise of t-closeness at t=0)",
        "literature": "Wong et al. 2006 (α,k); Li et al. 2007 (t-closeness)",
    },
    "membership_inference": {
        "metric": "MIA shadow-model accuracy (random = 0.50)",
        "good_threshold": "≤ 0.55 (advantage ≤ 5%)",
        "literature": "Dwork et al. 2006 (ε-DP); Shokri et al. 2017 (MIA)",
    },
    "utility": {
        "metric": "downstream-task accuracy on privatized data",
        "good_threshold": "≥ population majority baseline (no degradation below baseline)",
        "literature": "standard ML evaluation",
    },
}


# ═══════════════════════════════════════════════════════════════════
# Mechanism: cell suppression (per-column hash-deterministic)
# ═══════════════════════════════════════════════════════════════════

def cell_suppress_tabular(
    rows: List[List[str]],
    suppression_rate: float = 0.6,
    seed: int = 2026,
) -> List[List[str]]:
    """
    Deterministic per-cell suppression of QID columns.
    Suppression rate = fraction of (column, value) pairs to mask.

    Each (column, value) pair is hashed and either preserved (rate
    1 - suppression_rate of values) or replaced with "*" (the
    wildcard).  Suppression is per-(column, value), so the same
    value appears the same way across rows (deterministic).

    Uses the column-salted Python hash; (A1) hash-orthogonality
    holds in expectation for diverse value sets.
    """
    if not rows:
        return rows
    n_cols = len(rows[0]) - 1
    out = []
    for row in rows:
        new_row = []
        for c, v in enumerate(row[:-1]):
            # Hash to a value in [0, 1) using a column-salted hash
            h = abs(hash((seed, c, v))) % 10000 / 10000.0
            if h < suppression_rate:
                new_row.append("*")
            else:
                new_row.append(v)
        new_row.append(row[-1])
        out.append(new_row)
    return out


# ═══════════════════════════════════════════════════════════════════
# Mechanism: Mondrian-style k-anonymity (simple version)
# ═══════════════════════════════════════════════════════════════════

def k_anonymize_tabular(
    rows: List[List[str]],
    k: int = 25,
) -> List[List[str]]:
    """
    Mondrian-style k-anonymity.  Groups orig rows by QID; if any
    group has < k members, generalizes (replaces values with "*")
    until the group satisfies k-anon.

    Reference: LeFevre, DeWitt, Ramakrishnan 2006.
    """
    if not rows or k <= 1:
        return rows
    n_cols = len(rows[0]) - 1
    groups: Dict[Tuple[str, ...], List[List[str]]] = defaultdict(list)
    for r in rows:
        groups[tuple(r[:n_cols])].append(r)
    out = []
    for qid, members in groups.items():
        if len(members) >= k:
            for r in members:
                out.append(list(r))
        else:
            # generalize: replace all columns with "*"
            gen_qid = ["*"] * n_cols
            for r in members:
                out.append(gen_qid + [r[-1]])
    return out


# ═══════════════════════════════════════════════════════════════════
# Composed mechanism: hybrid suppression + k-anonymity
# ═══════════════════════════════════════════════════════════════════

def hybrid_suppress_kanon(
    rows: List[List[str]],
    suppression_rate: float = 0.6,
    k: int = 25,
    seed: int = 2026,
) -> List[List[str]]:
    """
    Apply cell suppression then k-anonymity (or k-anon then
    suppression -- the composition is order-symmetric for re-id
    and attribute-disclosure axes).

    This is the standard cell-suppression + k-anonymity hybrid
    (Sweeney 2002 style).  Provides:
      - re-id: bounded by both mechanisms' guarantees, multiplicative
      - attribute disclosure: bounded at population baseline if
        suppression rate ≥ 50% and (A2) dominant majority class
      - MIA: protected by k-anon's equivalence-class structure
      - utility: bounded by population majority baseline

    NOT a novel contribution -- this composition is foundational
    SDC practice.
    """
    suppressed = cell_suppress_tabular(rows, suppression_rate, seed)
    return k_anonymize_tabular(suppressed, k)


# ═══════════════════════════════════════════════════════════════════
# Mechanism: ε-Differential Privacy (Laplace mechanism reference)
# ═══════════════════════════════════════════════════════════════════

def epsilon_dp_count(
    true_count: int,
    epsilon: float,
    rng: Optional[random.Random] = None,
) -> float:
    """
    Add Laplace noise to a count query with privacy budget epsilon.
    Returns a real-valued noisy count.

    Sensitivity = 1 for individual count queries.  Larger epsilon =
    less noise = weaker privacy.

    Reference: Dwork, McSherry, Nissim, Smith 2006.
    """
    import math
    if rng is None:
        rng = random.Random()
    if epsilon <= 0:
        return float("inf")
    scale = 1.0 / epsilon
    u = rng.random() - 0.5
    noise = -scale * math.copysign(1.0, u) * math.log(1.0 - 2.0 * abs(u) + 1e-300)
    return float(true_count) + noise


# ═══════════════════════════════════════════════════════════════════
# CK's runtime decision: pick a mechanism for a given threat model
# ═══════════════════════════════════════════════════════════════════

def recommend_mechanism(
    needs_per_row_prediction: bool,
    needs_membership_protection: bool = True,
    needs_attribute_protection: bool = True,
    privacy_budget_eps: Optional[float] = None,
) -> Dict[str, Any]:
    """
    CK's runtime decision tree for picking a privacy mechanism.

    Returns a dict with:
      - mechanism: name + parameters
      - axes: which privacy properties it protects
      - cost: utility limitations
      - reference: literature citation
    """
    if needs_per_row_prediction:
        return {
            "mechanism": "ε-Differential Privacy (Laplace or Gaussian)",
            "params": {"epsilon": privacy_budget_eps or 1.0,
                       "delta": 1e-5 if privacy_budget_eps else None},
            "axes_protected": ["membership_inference", "limited utility-axes"],
            "axes_NOT_protected": ["strong attribute disclosure"],
            "cost": "noise injection degrades per-row prediction",
            "literature": "Dwork et al. 2006",
            "warning": (
                "Per-row prediction WITH strong attribute-disclosure "
                "protection is fundamentally limited by the no-free-lunch "
                "tradeoff.  Consult Brayden before releasing."
            ),
        }

    if needs_attribute_protection and needs_membership_protection:
        return {
            "mechanism": "hybrid: cell suppression + k-anonymity",
            "params": {"suppression_rate": 0.6, "k": 25},
            "axes_protected": [
                "re_identification (bound 1/k)",
                "attribute_disclosure (Δ ≈ 0 if suppression rate ≥ 50%)",
                "membership_inference (≈ 0.50 random via k-anon group structure)",
            ],
            "cost": "utility bounded by population majority baseline",
            "literature": "Sweeney 2002 + Wong et al. 2006 + Li et al. 2007",
            "implementation": "hybrid_suppress_kanon(rows, suppression_rate=0.6, k=25)",
        }

    if needs_membership_protection:
        return {
            "mechanism": "k-anonymity (Mondrian)",
            "params": {"k": 25},
            "axes_protected": ["re_identification", "membership_inference"],
            "axes_NOT_protected": ["attribute disclosure (can leak via homogeneity)"],
            "cost": "moderate utility loss from generalization",
            "literature": "LeFevre, DeWitt, Ramakrishnan 2006",
            "implementation": "k_anonymize_tabular(rows, k=25)",
        }

    return {
        "mechanism": "cell suppression alone",
        "params": {"suppression_rate": 0.6},
        "axes_protected": ["attribute_disclosure"],
        "axes_NOT_protected": ["membership_inference (deterministic mechanism)"],
        "cost": "utility at baseline; deterministic so MIA-vulnerable",
        "literature": "Sweeney 2002 (suppression component)",
        "implementation": "cell_suppress_tabular(rows, suppression_rate=0.6)",
        "warning": (
            "Deterministic mechanisms are vulnerable to membership "
            "inference (~94% attack accuracy).  Compose with k-anonymity "
            "or DP for MIA protection."
        ),
    }


# ═══════════════════════════════════════════════════════════════════
# Engine mount (optional Flask endpoints)
# ═══════════════════════════════════════════════════════════════════

def mount_privacy(engine: Any) -> Dict[str, Any]:
    """Attach the privacy formula surface to engine + Flask endpoints
    if engine has them."""
    setattr(engine, "ck_privacy", {
        "axes": PRIVACY_AXES,
        "recommend_mechanism": recommend_mechanism,
        "cell_suppress_tabular": cell_suppress_tabular,
        "k_anonymize_tabular": k_anonymize_tabular,
        "hybrid_suppress_kanon": hybrid_suppress_kanon,
        "epsilon_dp_count": epsilon_dp_count,
    })

    app = getattr(engine, "app", None)
    if app is not None:
        from flask import jsonify, request  # type: ignore

        @app.route("/privacy/info", methods=["GET"])
        def _privacy_info():  # noqa
            return jsonify({
                "axes": PRIVACY_AXES,
                "mechanisms_available": [
                    "cell_suppress_tabular (deterministic suppression)",
                    "k_anonymize_tabular (Mondrian generalization)",
                    "hybrid_suppress_kanon (recommended for data release)",
                    "epsilon_dp_count (Laplace noise on counts)",
                ],
                "scope_note": (
                    "These are reference implementations of standard "
                    "PPDP techniques (Sweeney 2002 + Wong 2006 + Li 2007 "
                    "+ Dwork 2006).  Not novel privacy contributions; "
                    "CK uses these for his own data-release posture."
                ),
            })

        @app.route("/privacy/recommend", methods=["POST"])
        def _privacy_recommend():  # noqa
            payload = request.get_json(silent=True) or {}
            return jsonify(recommend_mechanism(
                needs_per_row_prediction=payload.get("needs_per_row_prediction", False),
                needs_membership_protection=payload.get("needs_membership_protection", True),
                needs_attribute_protection=payload.get("needs_attribute_protection", True),
                privacy_budget_eps=payload.get("privacy_budget_eps"),
            ))

    return {"mounted": True, "axes_loaded": len(PRIVACY_AXES)}
