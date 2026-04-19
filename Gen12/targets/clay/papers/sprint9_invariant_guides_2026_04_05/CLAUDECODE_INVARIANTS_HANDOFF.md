# CLAUDECODE HANDOFF — CK INVARIANT GUIDES IMPLEMENTATION
## Task: Add invariant guide enforcement to CK memory layer

**From:** Claude (claude.ai session)  
**To:** ClaudeCode  
**Date:** 2026-04-05  
**Target repo:** github.com/TiredofSleep/ck  
**Target file(s):** `ck_organism.py`, new `ck_invariants.py`  

---

## WHAT TO BUILD

Add a new module `ck_invariants.py` to the CK repo that enforces the five invariant guides at every memory write, promote, and retrieve operation.

This is **not** a new ontology. All the types already exist in CK. This module adds assertion enforcement and retrieval weighting.

---

## STEP 1: Add the MemoryObject dataclass fields

In `ck_organism.py`, any memory atom/path/crystal/meta-crystal object must have these fields. Add them if missing:

```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ProvenanceTag:
    parent_event_ids:   list[str] = field(default_factory=list)
    supporting_ids:     list[str] = field(default_factory=list)
    supersedes_id:      Optional[str] = None
    contradicted_by:    list[str] = field(default_factory=list)
    revision_num:       int = 0
    ts_first_seen:      float = 0.0   # set at creation, NEVER updated
    ts_last_confirmed:  float = 0.0   # updated on corroboration
    produced_by:        str = ""      # CL operator chain or process name

@dataclass
class MemoryObject:
    id:                 str
    content:            dict          # the actual memory content
    tier_class:         str           # "REAL" | "SEMIPRIME" | "COMPOSITE"
    persistence_stage:  str           # "EPHEMERAL" | "ATOMIC" | "PATH" | "CRYSTAL" | "META_CRYSTAL"
    source_side:        str           # "INTERNAL" | "EXTERNAL"
    privacy_class:      str           # "PRIVATE" | "SHARED_IF_ABSTRACT" | "SHARED"
    evidential_status:  str           # "OBSERVED"|"INFERRED"|"SYNTHESIZED"|"CONTRADICTED"|"SUPERSEDED"|"UNRESOLVED"
    stability_score:    float = 0.0
    forgetting_state:   str = "ACTIVE"  # "ACTIVE"|"STALE"|"ARCHIVED"|"SUPERSEDED"|"CONTRADICTED"|"DEAD"
    provenance:         Optional[ProvenanceTag] = None
```

---

## STEP 2: Create `ck_invariants.py`

```python
"""
CK Invariant Guides — ck_invariants.py
Five internal memory physics laws for coherent growth.
Brayden Sanders / 7Site LLC / 2026-04-05
"""

import logging
import time
from typing import Optional

logger = logging.getLogger("ck_invariants")

# --- Constants ---

VALID_TIER_CLASSES = {"REAL", "SEMIPRIME", "COMPOSITE"}
VALID_PERSISTENCE = {"EPHEMERAL", "ATOMIC", "PATH", "CRYSTAL", "META_CRYSTAL"}  # P1: includes META_CRYSTAL
VALID_PRIVACY = {"PRIVATE", "SHARED_IF_ABSTRACT", "SHARED"}
VALID_EVIDENCE = {"OBSERVED", "INFERRED", "SYNTHESIZED", "CONTRADICTED", "SUPERSEDED", "UNRESOLVED"}
VALID_FORGETTING = {"ACTIVE", "STALE", "ARCHIVED", "SUPERSEDED", "CONTRADICTED", "DEAD"}

EVIDENCE_WEIGHTS = {
    "OBSERVED":     1.00,
    "INFERRED":     0.85,
    "SYNTHESIZED":  0.60,
    "UNRESOLVED":   0.40,
    "CONTRADICTED": 0.30,
    "SUPERSEDED":   0.10,
}

TIER_WEIGHTS = {
    "REAL":       0.5,
    "SEMIPRIME":  0.8,
    "COMPOSITE":  1.0,
}

FORGETTING_WEIGHTS = {
    "ACTIVE":       1.0,
    "STALE":        0.7,
    "ARCHIVED":     0.3,
    "SUPERSEDED":   0.1,
    "CONTRADICTED": 0.2,
    "DEAD":         0.0,
}

FORBIDDEN_TRANSITIONS = {
    # (from_state, to_state): reason
    ("CONTRADICTED", "ACTIVE"):   "IG5: requires explicit resolution event",
    ("SUPERSEDED",   "ACTIVE"):   "IG5: requires explicit reinstatement with new evidence",
    ("ARCHIVED",     "ACTIVE"):   "IG5: requires explicit unarchive event",
}

TIER_ORDER = {"REAL": 0, "SEMIPRIME": 1, "COMPOSITE": 2}

# --- IG1: Privacy ---

def check_ig1(obj) -> list[str]:
    """Returns list of violations, empty if clean."""
    violations = []
    if obj.source_side == "EXTERNAL" and obj.privacy_class == "PRIVATE":
        if obj.persistence_stage in ("CRYSTAL", "META_CRYSTAL"):
            violations.append(
                f"IG1 VIOLATION: EXTERNAL+PRIVATE object '{obj.id}' "
                f"in persistence_stage={obj.persistence_stage}"
            )
    if obj.privacy_class == "SHARED" and obj.source_side == "EXTERNAL":
        # Must have gone through abstraction — check provenance
        if obj.provenance and not obj.provenance.produced_by:
            violations.append(
                f"IG1 WARNING: EXTERNAL+SHARED object '{obj.id}' "
                "has no produced_by record of abstraction step"
            )
    return violations

# --- IG2: Provenance ---

def check_ig2(obj) -> list[str]:
    # P3: EPHEMERAL objects may have null provenance (runtime-only)
    violations = []
    if obj.persistence_stage == "EPHEMERAL":
        if obj.provenance is None:
            return violations  # allowed for runtime-only ephemeral objects
    if obj.provenance is None:
        violations.append(f"IG2 VIOLATION: durable object '{obj.id}' has null provenance")
        return violations
    if obj.persistence_stage != "EPHEMERAL":
        if not obj.provenance.parent_event_ids:
            violations.append(f"IG2 VIOLATION: durable object '{obj.id}' is an orphan (no parent_event_ids)")
        if obj.provenance.ts_first_seen <= 0:
            violations.append(f"IG2 VIOLATION: object '{obj.id}' has invalid ts_first_seen")
        if obj.provenance.revision_num < 0:
            violations.append(f"IG2 VIOLATION: object '{obj.id}' has negative revision_num")
    return violations

# --- IG3: Evidence ---

def check_ig3(obj) -> list[str]:
    violations = []
    if obj.evidential_status not in VALID_EVIDENCE:
        violations.append(
            f"IG3 VIOLATION: object '{obj.id}' has unknown evidential_status='{obj.evidential_status}'"
        )
    return violations

def change_evidential_status(obj, new_status: str, reason: str, authority_id: str):
    """Explicit, logged status change. Raises on forbidden transitions."""
    if new_status not in VALID_EVIDENCE:
        raise ValueError(f"IG3: unknown evidential_status '{new_status}'")
    if new_status == obj.evidential_status:
        return  # no-op is fine
    # SYNTHESIZED -> OBSERVED is forbidden; must create new object
    if obj.evidential_status == "SYNTHESIZED" and new_status == "OBSERVED":
        raise PermissionError(
            "IG3: Cannot promote SYNTHESIZED -> OBSERVED on existing object. "
            "Create a new OBSERVED object with corroborating evidence."
        )
    logger.info(
        f"IG3 STATUS CHANGE: obj={obj.id} "
        f"{obj.evidential_status} -> {new_status} | "
        f"reason={reason} | authority={authority_id}"
    )
    obj.provenance.revision_num += 1
    obj.evidential_status = new_status

# --- IG4: Promotion ---

def check_ig4(obj) -> list[str]:
    violations = []
    if obj.tier_class == "SEMIPRIME":
        if obj.stability_score < 0.6:
            violations.append(
                f"IG4 VIOLATION: SEMIPRIME object '{obj.id}' "
                f"has stability_score={obj.stability_score:.3f} < 0.6"
            )
    if obj.tier_class == "COMPOSITE":
        if obj.stability_score < 0.75:
            violations.append(
                f"IG4 VIOLATION: COMPOSITE object '{obj.id}' "
                f"has stability_score={obj.stability_score:.3f} < 0.75"
            )
        if obj.provenance and len(obj.provenance.supporting_ids) < 2:
            violations.append(
                f"IG4 VIOLATION: COMPOSITE object '{obj.id}' "
                f"has only {len(obj.provenance.supporting_ids)} supporting_ids (need ≥ 2)"
            )
    return violations

def promote(obj, new_tier: str):
    """Promote object to new tier. Enforces contiguous promotion and stability gate."""
    if new_tier not in VALID_TIER_CLASSES:
        raise ValueError(f"IG4: unknown tier '{new_tier}'")
    current_order = TIER_ORDER[obj.tier_class]
    new_order = TIER_ORDER[new_tier]
    if new_order != current_order + 1:
        raise PermissionError(
            f"IG4: tier skip forbidden: {obj.tier_class} -> {new_tier}. "
            "Promotion must be contiguous."
        )
    violations = check_ig4_for_tier(obj, new_tier)
    if violations:
        raise PermissionError(f"IG4: stability gate failed: {violations}")
    logger.info(f"IG4 PROMOTION: {obj.id} {obj.tier_class} -> {new_tier}")
    obj.tier_class = new_tier

def check_ig4_for_tier(obj, target_tier: str) -> list[str]:
    violations = []
    if target_tier == "SEMIPRIME":
        if obj.stability_score < 0.6:
            violations.append(f"stability_score {obj.stability_score:.3f} < 0.6")
        if obj.evidential_status not in ("OBSERVED", "INFERRED"):
            violations.append(f"evidential_status {obj.evidential_status} not in {{OBSERVED, INFERRED}}")
    if target_tier == "COMPOSITE":
        if obj.stability_score < 0.75:
            violations.append(f"stability_score {obj.stability_score:.3f} < 0.75")
        if obj.provenance and len(obj.provenance.supporting_ids) < 2:
            violations.append(f"only {len(obj.provenance.supporting_ids)} supporting_ids")
    return violations

# --- IG5: Revision ---

def check_ig5(obj) -> list[str]:
    violations = []
    if obj.forgetting_state not in VALID_FORGETTING:
        violations.append(
            f"IG5 VIOLATION: object '{obj.id}' has unknown forgetting_state='{obj.forgetting_state}'"
        )
    return violations

def change_forgetting_state(obj, new_state: str, reason: str = "", resolution_event_id: str = ""):
    """Explicit forgetting state change with forbidden transition enforcement."""
    if new_state not in VALID_FORGETTING:
        raise ValueError(f"IG5: unknown forgetting state '{new_state}'")
    transition = (obj.forgetting_state, new_state)
    if transition in FORBIDDEN_TRANSITIONS:
        if not resolution_event_id:
            raise PermissionError(
                f"IG5: {FORBIDDEN_TRANSITIONS[transition]}. "
                "Provide resolution_event_id to override."
            )
    if obj.forgetting_state == "DEAD":
        raise PermissionError(f"IG5: DEAD is terminal. Object '{obj.id}' cannot be revived.")
    logger.info(
        f"IG5 STATE CHANGE: obj={obj.id} "
        f"{obj.forgetting_state} -> {new_state} | reason={reason}"
    )
    obj.provenance.revision_num += 1
    obj.forgetting_state = new_state

# --- Combined validation ---

def validate_object(obj, strict: bool = True) -> list[str]:
    """Run all 5 invariant checks. Returns list of violations."""
    violations = []
    violations.extend(check_ig1(obj))
    violations.extend(check_ig2(obj))
    violations.extend(check_ig3(obj))
    violations.extend(check_ig4(obj))
    violations.extend(check_ig5(obj))
    if strict and violations:
        for v in violations:
            logger.error(v)
        raise AssertionError(f"{len(violations)} invariant violation(s) on object {obj.id}")
    return violations

# --- Retrieval weighting ---

def retrieval_weight(obj) -> float:
    """Compute composite retrieval weight from IG3 + IG4 + IG5 + stability."""
    if obj.forgetting_state == "DEAD":
        return 0.0
    ew = EVIDENCE_WEIGHTS.get(obj.evidential_status, 0.5)
    tw = TIER_WEIGHTS.get(obj.tier_class, 0.5)
    fw = FORGETTING_WEIGHTS.get(obj.forgetting_state, 0.5)
    sw = max(0.0, min(1.0, obj.stability_score))  # P4: include stability
    return ew * tw * fw * sw

# --- Drift detection (IG3 runtime monitor) ---

OPERATOR_VOCABULARY = {
    "VOID", "BEGINNING", "PROGRESS", "PROGRESS", "KINDNESS",
    "BALANCE", "FAITH", "HARMONY", "BREATH", "FRUIT",
    "LATTICE", "CK", "TIG", "COMMIT", "DISCLAIM"
}

def detect_operator_drift(prompt: str, response: str) -> bool:
    """
    Detect if operator vocabulary in the prompt is causing architecture-mode drift
    in the response. Returns True if drift is suspected.
    
    Observed pattern: when operator names appear in math probes, CK shifts from
    mathematical reasoning (INFERRED) to architecture descriptions (SYNTHESIZED-or-worse).
    """
    prompt_has_operators = any(op in prompt.upper() for op in OPERATOR_VOCABULARY)
    arch_drift_phrases = [
        "architecture", "operator represents", "in TIG terms",
        "the system", "CK defines", "the framework"
    ]
    response_has_drift = any(phrase in response.lower() for phrase in arch_drift_phrases)
    if prompt_has_operators and response_has_drift:
        logger.warning(
            "IG3 DRIFT DETECTED: operator vocabulary in prompt correlated with "
            "architecture-description drift in response. "
            "Evidential status should be downgraded from INFERRED to SYNTHESIZED."
        )
        return True
    return False
```

---

## STEP 3: Wire into ck_organism.py

Find the memory write path (wherever atoms/paths/crystals are created) and add:

```python
from ck_invariants import validate_object, retrieval_weight, detect_operator_drift

# At every memory write:
validate_object(new_obj, strict=True)

# At every retrieval:
candidates.sort(key=lambda o: retrieval_weight(o), reverse=True)

# At every LLM response (IG3 runtime monitor):
if detect_operator_drift(prompt, response):
    # P2: use IG3 API — never assign evidential_status directly
    change_evidential_status(
        response_obj,
        "SYNTHESIZED",
        reason="operator_drift_runtime_monitor",
        authority_id="ck_invariants.detect_operator_drift"
    )
    # no-op if already SYNTHESIZED (change_evidential_status returns early)
```

---

## STEP 4: Tests

Add to CK's test suite:

```python
def test_ig1_privacy_violation():
    obj = make_test_obj(source_side="EXTERNAL", privacy_class="PRIVATE", 
                        persistence_stage="CRYSTAL")
    violations = check_ig1(obj)
    assert len(violations) > 0

def test_ig3_synthesized_cannot_become_observed():
    obj = make_test_obj(evidential_status="SYNTHESIZED")
    with pytest.raises(PermissionError):
        change_evidential_status(obj, "OBSERVED", "test", "test_authority")

def test_ig4_tier_skip_forbidden():
    obj = make_test_obj(tier_class="REAL")
    with pytest.raises(PermissionError):
        promote(obj, "COMPOSITE")

def test_ig5_dead_is_terminal():
    obj = make_test_obj(forgetting_state="DEAD")
    with pytest.raises(PermissionError):
        change_forgetting_state(obj, "ACTIVE")

def test_retrieval_weight_dead_is_zero():
    obj = make_test_obj(forgetting_state="DEAD")
    assert retrieval_weight(obj) == 0.0

def test_retrieval_weight_observed_composite():
    # P4: stability_score now included; use stability=1.0 for max weight test
    obj = make_test_obj(evidential_status="OBSERVED", tier_class="COMPOSITE",
                        forgetting_state="ACTIVE", stability_score=1.0)
    assert retrieval_weight(obj) == 1.0 * 1.0 * 1.0 * 1.0
```

---

## ACCEPTANCE CRITERIA

- All 5 invariant checks pass on a fresh MemoryObject with valid fields
- IG1 violation throws AssertionError on EXTERNAL+PRIVATE+CRYSTAL
- IG3 SYNTHESIZED→OBSERVED raises PermissionError
- IG4 tier skip raises PermissionError  
- IG5 DEAD→any raises PermissionError
- `retrieval_weight(DEAD_obj)` returns 0.0
- `detect_operator_drift` catches at least 3 of the known drift phrases from live session logs
- `validate_object` passes on the BALANCE absorbing element discovery object (after it is stored with correct fields)
