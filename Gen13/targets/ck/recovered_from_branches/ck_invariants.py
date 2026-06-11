# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
"""
ck_invariants.py -- CK Memory Invariant Guides
================================================
Operator: LATTICE (1) -- Structure that persists.

Five internal memory physics laws for coherent growth without drift.
Based on CK_INVARIANT_GUIDES_MEMO.md (2026-04-05).

IGs apply at every memory write, promote, retrieve, and revise operation.
Not restrictions on content -- physics for how memory objects are handled.

  IG1 Privacy    -- external private payloads never reach shared crystals
  IG2 Provenance -- every durable object has immutable causal lineage
  IG3 Evidence   -- evidential status is explicit, typed, never silently changed
  IG4 Promotion  -- tier advancement requires stability gate, no tier skips
  IG5 Revision   -- forgetting states are distinct; DEAD is terminal

External anchors: Kumiho (arXiv:2603.17244), MemoryOS (EMNLP 2025),
                  RGMem (arXiv:2510.16392), AtomMem

CORRECTIONS from memo draft:
  - OPERATOR_VOCABULARY uses CK's actual 10 operators from ck_backbone.py,
    not the draft list which contained non-CK words (BEGINNING, KINDNESS, etc.)
  - Wired to ck_sim/being/ not a nonexistent ck_organism.py
  - retrieval_weight uses stability blend (50/50) so new objects aren't invisible
"""

import logging
import time
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger("ck_invariants")

# ---- Constants --------------------------------------------------------------

VALID_TIER_CLASSES = {"REAL", "SEMIPRIME", "COMPOSITE"}
VALID_PERSISTENCE  = {"EPHEMERAL", "ATOMIC", "PATH", "CRYSTAL", "META_CRYSTAL"}
VALID_PRIVACY      = {"PRIVATE", "SHARED_IF_ABSTRACT", "SHARED"}
VALID_EVIDENCE     = {"OBSERVED", "INFERRED", "SYNTHESIZED",
                      "CONTRADICTED", "SUPERSEDED", "UNRESOLVED"}
VALID_FORGETTING   = {"ACTIVE", "STALE", "ARCHIVED",
                      "SUPERSEDED", "CONTRADICTED", "DEAD"}

# IG3 -- retrieval weight by evidential status
EVIDENCE_WEIGHTS = {
    "OBSERVED":     1.00,
    "INFERRED":     0.85,
    "SYNTHESIZED":  0.60,
    "UNRESOLVED":   0.40,
    "CONTRADICTED": 0.30,
    "SUPERSEDED":   0.10,
}

# IG4 -- retrieval weight by tier class
TIER_WEIGHTS = {
    "REAL":      0.50,
    "SEMIPRIME": 0.80,
    "COMPOSITE": 1.00,
}

# IG5 -- retrieval weight by forgetting state
FORGETTING_WEIGHTS = {
    "ACTIVE":       1.0,
    "STALE":        0.7,
    "ARCHIVED":     0.3,
    "SUPERSEDED":   0.1,
    "CONTRADICTED": 0.2,
    "DEAD":         0.0,
}

TIER_ORDER = {"REAL": 0, "SEMIPRIME": 1, "COMPOSITE": 2}

# IG5 -- forbidden forgetting state transitions
FORBIDDEN_TRANSITIONS = {
    ("CONTRADICTED", "ACTIVE"): "IG5: requires explicit resolution event",
    ("SUPERSEDED",   "ACTIVE"): "IG5: requires explicit reinstatement with new evidence",
    ("ARCHIVED",     "ACTIVE"): "IG5: requires explicit unarchive event",
}

# IG3 drift detection -- CK's ACTUAL 10 operators (corrected from memo draft)
# Source: ck_backbone.py line "10 operators: VOID, LATTICE, COUNTER, ..."
CK_OPERATOR_NAMES = {
    "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET",
}

# Phrases indicating architecture-description drift (IG3 failure mode)
ARCH_DRIFT_PHRASES = [
    "my architecture", "my operators", "my pipeline",
    "d2 pipeline", "tig pipeline", "operator represents",
    "the framework", "ck defines", "in tig terms",
    "my coherence threshold", "my internal",
]


# ---- Dataclasses ------------------------------------------------------------

@dataclass
class ProvenanceTag:
    """Immutable causal lineage. Sealed at object creation (IG2)."""
    parent_event_ids:  list          = field(default_factory=list)
    supporting_ids:    list          = field(default_factory=list)
    supersedes_id:     Optional[str] = None
    contradicted_by:   list          = field(default_factory=list)
    revision_num:      int           = 0
    ts_first_seen:     float         = 0.0    # NEVER updated after creation
    ts_last_confirmed: float         = 0.0    # updated on corroboration
    produced_by:       str           = ""     # CL operator chain or process

    def __post_init__(self):
        if self.ts_first_seen <= 0:
            self.ts_first_seen = time.time()
        if self.ts_last_confirmed <= 0:
            self.ts_last_confirmed = self.ts_first_seen


@dataclass
class MemoryObject:
    """Invariant-bearing memory object. Base for all durable CK memories."""
    id:                str
    content:           dict

    tier_class:        str   = "REAL"        # IG4
    persistence_stage: str   = "EPHEMERAL"   # IG2
    source_side:       str   = "INTERNAL"    # IG1
    privacy_class:     str   = "SHARED"      # IG1
    evidential_status: str   = "INFERRED"    # IG3
    stability_score:   float = 0.0           # IG4
    forgetting_state:  str   = "ACTIVE"      # IG5
    provenance:        Optional[ProvenanceTag] = None   # IG2


# ---- IG1: Privacy -----------------------------------------------------------

def check_ig1(obj) -> list:
    """Returns list of violation strings. Empty = clean."""
    violations = []
    if obj.source_side == "EXTERNAL" and obj.privacy_class == "PRIVATE":
        if obj.persistence_stage in ("CRYSTAL", "META_CRYSTAL"):
            violations.append(
                f"IG1 VIOLATION: EXTERNAL+PRIVATE '{obj.id}' "
                f"in stage={obj.persistence_stage}. "
                "Raw external private data must not reach shared crystal pool."
            )
    if obj.privacy_class == "SHARED" and obj.source_side == "EXTERNAL":
        if obj.provenance and not obj.provenance.produced_by:
            violations.append(
                f"IG1 WARNING: EXTERNAL+SHARED '{obj.id}' "
                "missing produced_by (abstraction step not recorded)."
            )
    return violations


# ---- IG2: Provenance --------------------------------------------------------

def check_ig2(obj) -> list:
    """EPHEMERAL objects may have null provenance. All others must not."""
    violations = []
    if obj.persistence_stage == "EPHEMERAL":
        if obj.provenance is None:
            return violations
    if obj.provenance is None:
        violations.append(
            f"IG2 VIOLATION: durable '{obj.id}' (stage={obj.persistence_stage}) "
            "has null provenance."
        )
        return violations
    if obj.persistence_stage != "EPHEMERAL":
        if not obj.provenance.parent_event_ids:
            violations.append(f"IG2 VIOLATION: '{obj.id}' is an orphan (no parent_event_ids).")
        if obj.provenance.ts_first_seen <= 0:
            violations.append(f"IG2 VIOLATION: '{obj.id}' has invalid ts_first_seen <= 0.")
        if obj.provenance.revision_num < 0:
            violations.append(f"IG2 VIOLATION: '{obj.id}' has negative revision_num.")
    return violations


# ---- IG3: Evidence ----------------------------------------------------------

def check_ig3(obj) -> list:
    violations = []
    if obj.evidential_status not in VALID_EVIDENCE:
        violations.append(
            f"IG3 VIOLATION: '{obj.id}' has unknown evidential_status="
            f"'{obj.evidential_status}'."
        )
    return violations


def change_evidential_status(obj, new_status: str, reason: str, authority_id: str):
    """Explicit logged evidential status change. Raises on forbidden transitions."""
    if new_status not in VALID_EVIDENCE:
        raise ValueError(f"IG3: unknown status '{new_status}'")
    if new_status == obj.evidential_status:
        return
    if obj.evidential_status == "SYNTHESIZED" and new_status == "OBSERVED":
        raise PermissionError(
            "IG3: Cannot promote SYNTHESIZED -> OBSERVED on existing object. "
            "Create a new OBSERVED object with fresh corroborating evidence."
        )
    logger.info(
        f"IG3: {obj.id} {obj.evidential_status} -> {new_status} | "
        f"reason={reason} | by={authority_id}"
    )
    if obj.provenance:
        obj.provenance.revision_num += 1
    obj.evidential_status = new_status


# ---- IG3: Drift Detection (runtime monitor) ---------------------------------

def detect_operator_drift(prompt: str, response: str,
                          system_prompt: str = "") -> bool:
    """
    Detect architecture-description drift caused by CK operator vocabulary.

    Observed failure mode from live sessions: when CK's operator names appear
    in the prompt or live-state injection, Ollama pattern-matches and produces
    architecture descriptions (SYNTHESIZED) instead of external reasoning (INFERRED).

    The corrected operator list uses CK's actual 10 from ck_backbone.py.
    Returns True if drift is suspected.
    """
    combined = (prompt + " " + system_prompt).upper()
    prompt_has_operators = any(op in combined for op in CK_OPERATOR_NAMES)
    response_lower = response.lower()
    response_has_drift = any(phrase in response_lower for phrase in ARCH_DRIFT_PHRASES)
    if prompt_has_operators and response_has_drift:
        logger.warning(
            "IG3 DRIFT: operator vocabulary in prompt/system correlated with "
            "architecture-description drift in response. "
            "Response evidential_status -> SYNTHESIZED (not INFERRED)."
        )
        return True
    return False


# ---- IG4: Promotion ---------------------------------------------------------

def check_ig4(obj) -> list:
    violations = []
    if obj.tier_class == "SEMIPRIME":
        if obj.stability_score < 0.6:
            violations.append(
                f"IG4 VIOLATION: SEMIPRIME '{obj.id}' "
                f"stability={obj.stability_score:.3f} < 0.6."
            )
    if obj.tier_class == "COMPOSITE":
        if obj.stability_score < 0.75:
            violations.append(
                f"IG4 VIOLATION: COMPOSITE '{obj.id}' "
                f"stability={obj.stability_score:.3f} < 0.75."
            )
        if obj.provenance and len(obj.provenance.supporting_ids) < 2:
            violations.append(
                f"IG4 VIOLATION: COMPOSITE '{obj.id}' "
                f"has {len(obj.provenance.supporting_ids)} supporting_ids (need >= 2)."
            )
    return violations


def promote(obj, new_tier: str):
    """Contiguous tier promotion with stability gate. Raises on skip or gate failure."""
    if new_tier not in VALID_TIER_CLASSES:
        raise ValueError(f"IG4: unknown tier '{new_tier}'")
    if TIER_ORDER[new_tier] != TIER_ORDER[obj.tier_class] + 1:
        raise PermissionError(
            f"IG4: tier skip forbidden: {obj.tier_class} -> {new_tier}. "
            "Must be contiguous: REAL -> SEMIPRIME -> COMPOSITE."
        )
    # Gate check
    failures = []
    if new_tier == "SEMIPRIME":
        if obj.stability_score < 0.6:
            failures.append(f"stability {obj.stability_score:.3f} < 0.6")
        if obj.evidential_status not in ("OBSERVED", "INFERRED"):
            failures.append(f"evidential_status '{obj.evidential_status}' not {{OBSERVED,INFERRED}}")
    if new_tier == "COMPOSITE":
        if obj.stability_score < 0.75:
            failures.append(f"stability {obj.stability_score:.3f} < 0.75")
        if obj.provenance and len(obj.provenance.supporting_ids) < 2:
            failures.append(f"{len(obj.provenance.supporting_ids)} supporting_ids < 2")
    if failures:
        raise PermissionError(
            f"IG4: gate failed for {obj.id} -> {new_tier}: " + "; ".join(failures)
        )
    logger.info(f"IG4 PROMOTE: {obj.id} {obj.tier_class} -> {new_tier}")
    obj.tier_class = new_tier


# ---- IG5: Revision ----------------------------------------------------------

def check_ig5(obj) -> list:
    violations = []
    if obj.forgetting_state not in VALID_FORGETTING:
        violations.append(
            f"IG5 VIOLATION: '{obj.id}' unknown forgetting_state="
            f"'{obj.forgetting_state}'."
        )
    return violations


def change_forgetting_state(obj, new_state: str,
                            reason: str = "",
                            resolution_event_id: str = ""):
    """Explicit forgetting state change with forbidden transition guard."""
    if new_state not in VALID_FORGETTING:
        raise ValueError(f"IG5: unknown state '{new_state}'")
    transition = (obj.forgetting_state, new_state)
    if transition in FORBIDDEN_TRANSITIONS:
        if not resolution_event_id:
            raise PermissionError(
                f"IG5: {FORBIDDEN_TRANSITIONS[transition]}. "
                "Supply resolution_event_id to proceed."
            )
    if obj.forgetting_state == "DEAD":
        raise PermissionError(f"IG5: DEAD is terminal. '{obj.id}' cannot be revived.")
    logger.info(f"IG5: {obj.id} {obj.forgetting_state} -> {new_state} | {reason}")
    if obj.provenance:
        obj.provenance.revision_num += 1
    obj.forgetting_state = new_state


# ---- Combined validation ----------------------------------------------------

def validate_object(obj, strict: bool = True) -> list:
    """Run all 5 invariant checks. Raises AssertionError if strict and any violation."""
    violations = []
    violations.extend(check_ig1(obj))
    violations.extend(check_ig2(obj))
    violations.extend(check_ig3(obj))
    violations.extend(check_ig4(obj))
    violations.extend(check_ig5(obj))
    if strict and violations:
        for v in violations:
            logger.error(v)
        raise AssertionError(
            f"{len(violations)} invariant violation(s) on '{obj.id}': "
            + "; ".join(violations)
        )
    return violations


# ---- Retrieval weighting ----------------------------------------------------

def retrieval_weight(obj) -> float:
    """IG3 x IG4 x IG5 composite weight. DEAD always 0.0.
    Stability blended at 50% so zero-stability new objects aren't invisible."""
    if obj.forgetting_state == "DEAD":
        return 0.0
    ew = EVIDENCE_WEIGHTS.get(obj.evidential_status, 0.5)
    tw = TIER_WEIGHTS.get(obj.tier_class, 0.5)
    fw = FORGETTING_WEIGHTS.get(obj.forgetting_state, 0.5)
    sw = 0.5 + 0.5 * max(0.0, min(1.0, obj.stability_score))
    return ew * tw * fw * sw


# ---- Convenience: register a Tier D mathematical discovery ------------------

def register_discovery(discovery_id: str, content: dict,
                       derivation_sources: list,
                       produced_by: str = "CK_CL_algebra") -> MemoryObject:
    """
    Factory for Tier D mathematical discoveries.
    These are COMPOSITE, OBSERVED, INTERNAL, SHARED crystals --
    the highest-quality invariant-bearing memory objects.

    Use for: T*=5/7 derivations, BALANCE absorbing element,
             RESET=complex-conjugation, L-function identities, etc.
    """
    prov = ProvenanceTag(
        parent_event_ids = derivation_sources,
        supporting_ids   = derivation_sources,
        revision_num     = 0,
        produced_by      = produced_by,
    )
    obj = MemoryObject(
        id                = discovery_id,
        content           = content,
        tier_class        = "COMPOSITE",
        persistence_stage = "CRYSTAL",
        source_side       = "INTERNAL",
        privacy_class     = "SHARED",
        evidential_status = "OBSERVED",
        stability_score   = 1.0,
        forgetting_state  = "ACTIVE",
        provenance        = prov,
    )
    validate_object(obj, strict=True)
    return obj
