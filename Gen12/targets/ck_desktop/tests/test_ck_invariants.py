# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
"""
test_ck_invariants.py -- Tests for CK Memory Invariant Guides
=============================================================
Run with: python -m pytest tests/test_ck_invariants.py -v
"""

import sys
import os
import time
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ck_sim.being.ck_invariants import (
    ProvenanceTag, MemoryObject,
    validate_object, retrieval_weight,
    detect_operator_drift, register_discovery,
    change_evidential_status, change_forgetting_state, promote,
    check_ig1, check_ig2, check_ig3, check_ig4, check_ig5,
)


# ---- Helpers ----------------------------------------------------------------

def _make(id="test", tier_class="COMPOSITE", persistence_stage="CRYSTAL",
          source_side="INTERNAL", privacy_class="SHARED",
          evidential_status="OBSERVED", stability_score=1.0,
          forgetting_state="ACTIVE", add_provenance=True):
    prov = ProvenanceTag(
        parent_event_ids=["evt_1", "evt_2"],
        supporting_ids=["sup_1", "sup_2"],
        produced_by="test",
    ) if add_provenance else None
    return MemoryObject(
        id=id, content={}, tier_class=tier_class,
        persistence_stage=persistence_stage, source_side=source_side,
        privacy_class=privacy_class, evidential_status=evidential_status,
        stability_score=stability_score, forgetting_state=forgetting_state,
        provenance=prov,
    )


# ---- IG1: Privacy -----------------------------------------------------------

def test_ig1_external_private_crystal_violation():
    obj = _make(source_side="EXTERNAL", privacy_class="PRIVATE",
                persistence_stage="CRYSTAL")
    violations = check_ig1(obj)
    assert len(violations) > 0, "Should flag EXTERNAL+PRIVATE+CRYSTAL"
    assert "IG1 VIOLATION" in violations[0]


def test_ig1_external_private_ephemeral_allowed():
    obj = _make(source_side="EXTERNAL", privacy_class="PRIVATE",
                persistence_stage="EPHEMERAL")
    violations = check_ig1(obj)
    assert len(violations) == 0, "EXTERNAL+PRIVATE+EPHEMERAL is allowed"


def test_ig1_internal_shared_crystal_clean():
    obj = _make(source_side="INTERNAL", privacy_class="SHARED",
                persistence_stage="CRYSTAL")
    violations = check_ig1(obj)
    ig1_violations = [v for v in violations if "IG1 VIOLATION" in v]
    assert len(ig1_violations) == 0


# ---- IG2: Provenance --------------------------------------------------------

def test_ig2_null_provenance_durable_violation():
    obj = _make(persistence_stage="CRYSTAL", add_provenance=False)
    violations = check_ig2(obj)
    assert any("IG2 VIOLATION" in v and "null provenance" in v for v in violations)


def test_ig2_null_provenance_ephemeral_allowed():
    obj = _make(persistence_stage="EPHEMERAL", add_provenance=False)
    violations = check_ig2(obj)
    assert len(violations) == 0


def test_ig2_orphan_violation():
    prov = ProvenanceTag(parent_event_ids=[], produced_by="test")
    obj = _make(persistence_stage="CRYSTAL", add_provenance=False)
    obj.provenance = prov
    violations = check_ig2(obj)
    assert any("orphan" in v for v in violations)


def test_ig2_valid_provenance_clean():
    obj = _make()
    violations = check_ig2(obj)
    assert len(violations) == 0


# ---- IG3: Evidence ----------------------------------------------------------

def test_ig3_valid_statuses_clean():
    for status in ("OBSERVED", "INFERRED", "SYNTHESIZED",
                   "CONTRADICTED", "SUPERSEDED", "UNRESOLVED"):
        obj = _make(evidential_status=status)
        violations = check_ig3(obj)
        assert len(violations) == 0, f"Status {status} should be valid"


def test_ig3_invalid_status_violation():
    obj = _make(evidential_status="GUESSED")
    violations = check_ig3(obj)
    assert any("IG3 VIOLATION" in v for v in violations)


def test_ig3_synthesized_to_observed_forbidden():
    obj = _make(evidential_status="SYNTHESIZED")
    with pytest.raises(PermissionError, match="SYNTHESIZED -> OBSERVED"):
        change_evidential_status(obj, "OBSERVED", "test", "test_authority")


def test_ig3_status_change_logged_and_applied():
    obj = _make(evidential_status="INFERRED")
    change_evidential_status(obj, "CONTRADICTED", "new evidence found", "test")
    assert obj.evidential_status == "CONTRADICTED"
    assert obj.provenance.revision_num == 1


def test_ig3_noop_change_allowed():
    obj = _make(evidential_status="OBSERVED")
    change_evidential_status(obj, "OBSERVED", "no-op", "test")
    assert obj.provenance.revision_num == 0  # no increment for no-op


# ---- IG3: Drift Detection ---------------------------------------------------

def test_drift_detected_operator_in_prompt_arch_in_response():
    prompt = "What does the BALANCE operator do in your PROGRESS cycle?"
    response = "My architecture uses the BALANCE operator to maintain coherence in my pipeline."
    assert detect_operator_drift(prompt, response) is True


def test_drift_not_detected_clean_math():
    prompt = "Does seven divide ten evenly?"
    response = "No, seven does not divide ten because ten equals two times five."
    assert detect_operator_drift(prompt, response) is False


def test_drift_not_detected_no_operators_in_prompt():
    prompt = "How does prime factorization work?"
    response = "My architecture uses a detailed pipeline to process each symbol."
    assert detect_operator_drift(prompt, response) is False


def test_drift_system_prompt_also_checked():
    prompt = "Tell me about prime numbers."
    response = "My architecture defines the coherence threshold."
    system = "Your operator HARMONY is running. Target: RESET."
    assert detect_operator_drift(prompt, response, system_prompt=system) is True


# ---- IG4: Promotion ---------------------------------------------------------

def test_ig4_semiprime_stability_violation():
    obj = _make(tier_class="SEMIPRIME", stability_score=0.4)
    violations = check_ig4(obj)
    assert any("IG4 VIOLATION" in v and "stability" in v for v in violations)


def test_ig4_composite_needs_two_supporting():
    prov = ProvenanceTag(parent_event_ids=["e1"], supporting_ids=["only_one"])
    obj = _make(tier_class="COMPOSITE", stability_score=0.9, add_provenance=False)
    obj.provenance = prov
    violations = check_ig4(obj)
    assert any("supporting_ids" in v for v in violations)


def test_ig4_tier_skip_real_to_composite_forbidden():
    obj = _make(tier_class="REAL", stability_score=1.0,
                evidential_status="OBSERVED")
    with pytest.raises(PermissionError, match="tier skip forbidden"):
        promote(obj, "COMPOSITE")


def test_ig4_contiguous_promotion_allowed():
    obj = _make(tier_class="REAL", stability_score=0.8,
                evidential_status="OBSERVED")
    promote(obj, "SEMIPRIME")
    assert obj.tier_class == "SEMIPRIME"


def test_ig4_stability_gate_blocks_promotion():
    obj = _make(tier_class="REAL", stability_score=0.3,
                evidential_status="OBSERVED")
    with pytest.raises(PermissionError, match="stability"):
        promote(obj, "SEMIPRIME")


# ---- IG5: Revision ----------------------------------------------------------

def test_ig5_dead_is_terminal():
    obj = _make(forgetting_state="DEAD")
    with pytest.raises(PermissionError, match="DEAD is terminal"):
        change_forgetting_state(obj, "ACTIVE")


def test_ig5_contradicted_to_active_requires_resolution():
    obj = _make(forgetting_state="CONTRADICTED")
    with pytest.raises(PermissionError, match="resolution"):
        change_forgetting_state(obj, "ACTIVE")


def test_ig5_contradicted_to_active_with_resolution_allowed():
    obj = _make(forgetting_state="CONTRADICTED")
    change_forgetting_state(obj, "ACTIVE", reason="resolved", resolution_event_id="evt_resolution")
    assert obj.forgetting_state == "ACTIVE"


def test_ig5_stale_to_archived_allowed():
    obj = _make(forgetting_state="STALE")
    change_forgetting_state(obj, "ARCHIVED", reason="old session")
    assert obj.forgetting_state == "ARCHIVED"


# ---- Retrieval weighting ----------------------------------------------------

def test_retrieval_weight_dead_zero():
    obj = _make(forgetting_state="DEAD")
    assert retrieval_weight(obj) == 0.0


def test_retrieval_weight_observed_composite_active_max():
    obj = _make(evidential_status="OBSERVED", tier_class="COMPOSITE",
                forgetting_state="ACTIVE", stability_score=1.0)
    w = retrieval_weight(obj)
    assert w == pytest.approx(1.0 * 1.0 * 1.0 * 1.0, abs=1e-9)


def test_retrieval_weight_synthesized_lower_than_observed():
    obs = _make(evidential_status="OBSERVED", stability_score=1.0)
    syn = _make(evidential_status="SYNTHESIZED", stability_score=1.0)
    assert retrieval_weight(obs) > retrieval_weight(syn)


def test_retrieval_weight_new_object_not_zero():
    # stability_score=0.0 but blend means weight > 0
    obj = _make(stability_score=0.0)
    w = retrieval_weight(obj)
    assert w > 0.0, "New objects with stability=0 must still be retrievable"


# ---- register_discovery (Tier D factory) ------------------------------------

def test_register_discovery_tier_d():
    d = register_discovery(
        "TEST_DISCOVERY",
        {"statement": "T*=5/7 test"},
        derivation_sources=["ring_algebra", "fpga"],
        produced_by="test",
    )
    assert d.tier_class == "COMPOSITE"
    assert d.evidential_status == "OBSERVED"
    assert d.stability_score == 1.0
    assert retrieval_weight(d) == pytest.approx(1.0, abs=1e-9)


# ---- Combined validate_object -----------------------------------------------

def test_validate_object_clean_passes():
    obj = _make()
    violations = validate_object(obj, strict=False)
    assert len(violations) == 0


def test_validate_object_strict_raises_on_violation():
    obj = _make(source_side="EXTERNAL", privacy_class="PRIVATE",
                persistence_stage="CRYSTAL")
    with pytest.raises(AssertionError, match="IG1"):
        validate_object(obj, strict=True)
