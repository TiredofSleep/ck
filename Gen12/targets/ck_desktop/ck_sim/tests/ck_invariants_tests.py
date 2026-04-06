"""
ck_invariants_tests.py -- Tests for CK Memory Invariant Guides (IG1-IG5)
=========================================================================
Validates all five invariant physics laws from CK_INVARIANT_GUIDES_MEMO.md.

Acceptance criteria from CLAUDECODE_INVARIANTS_HANDOFF.md:
  - All 5 checks pass on a fresh MemoryObject with valid fields
  - IG1 violation throws AssertionError on EXTERNAL+PRIVATE+CRYSTAL
  - IG3 SYNTHESIZED->OBSERVED raises PermissionError
  - IG4 tier skip raises PermissionError
  - IG5 DEAD->any raises PermissionError
  - retrieval_weight(DEAD) == 0.0
  - retrieval_weight(OBSERVED+COMPOSITE+ACTIVE+stability=1.0) is maximum

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""

import time
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ck_sim.being.ck_invariants import (
    ProvenanceTag, MemoryObject,
    check_ig1, check_ig2, check_ig3, check_ig4, check_ig5,
    validate_object,
    change_evidential_status,
    promote,
    change_forgetting_state,
    retrieval_weight,
    detect_operator_drift,
    register_discovery,
    EVIDENCE_WEIGHTS, TIER_WEIGHTS, FORGETTING_WEIGHTS,
)


# ─── HELPERS ─────────────────────────────────────────────────────────────────

def make_prov(**kwargs):
    defaults = dict(
        parent_event_ids=['evt_001'],
        supporting_ids=[],
        revision_num=0,
        ts_first_seen=time.time(),
        produced_by='test_suite',
    )
    defaults.update(kwargs)
    return ProvenanceTag(**defaults)


def make_obj(**kwargs):
    """Build a fully valid MemoryObject with sensible defaults."""
    defaults = dict(
        id='test_obj',
        content={'value': 42},
        tier_class='REAL',
        persistence_stage='ATOMIC',
        source_side='INTERNAL',
        privacy_class='PRIVATE',
        evidential_status='OBSERVED',
        stability_score=0.5,
        forgetting_state='ACTIVE',
        provenance=make_prov(),
    )
    defaults.update(kwargs)
    return MemoryObject(**defaults)


# ─── IG1: PRIVACY ────────────────────────────────────────────────────────────

class TestIG1Privacy(unittest.TestCase):

    def test_ig1_clean_internal_private(self):
        obj = make_obj(source_side='INTERNAL', privacy_class='PRIVATE',
                       persistence_stage='CRYSTAL')
        self.assertEqual(check_ig1(obj), [])

    def test_ig1_clean_external_shared_with_abstraction(self):
        prov = make_prov(produced_by='abstraction_layer')
        obj = make_obj(source_side='EXTERNAL', privacy_class='SHARED',
                       persistence_stage='CRYSTAL', provenance=prov)
        self.assertEqual(check_ig1(obj), [])

    def test_ig1_violation_external_private_crystal(self):
        obj = make_obj(source_side='EXTERNAL', privacy_class='PRIVATE',
                       persistence_stage='CRYSTAL')
        violations = check_ig1(obj)
        self.assertTrue(len(violations) > 0)
        self.assertIn('IG1 VIOLATION', violations[0])

    def test_ig1_violation_external_private_meta_crystal(self):
        obj = make_obj(source_side='EXTERNAL', privacy_class='PRIVATE',
                       persistence_stage='META_CRYSTAL')
        violations = check_ig1(obj)
        self.assertTrue(len(violations) > 0)

    def test_ig1_external_private_atomic_is_ok(self):
        obj = make_obj(source_side='EXTERNAL', privacy_class='PRIVATE',
                       persistence_stage='ATOMIC')
        self.assertEqual(check_ig1(obj), [])

    def test_ig1_warning_external_shared_no_abstraction(self):
        prov = make_prov(produced_by='')  # no abstraction step recorded
        obj = make_obj(source_side='EXTERNAL', privacy_class='SHARED',
                       persistence_stage='CRYSTAL', provenance=prov)
        violations = check_ig1(obj)
        self.assertTrue(len(violations) > 0)
        self.assertIn('IG1 WARNING', violations[0])

    def test_ig1_raises_on_validate_strict(self):
        obj = make_obj(source_side='EXTERNAL', privacy_class='PRIVATE',
                       persistence_stage='CRYSTAL')
        with self.assertRaises(AssertionError):
            validate_object(obj, strict=True)


# ─── IG2: PROVENANCE ─────────────────────────────────────────────────────────

class TestIG2Provenance(unittest.TestCase):

    def test_ig2_clean_atomic_with_provenance(self):
        obj = make_obj(persistence_stage='ATOMIC', provenance=make_prov())
        self.assertEqual(check_ig2(obj), [])

    def test_ig2_ephemeral_no_provenance_is_ok(self):
        obj = make_obj(persistence_stage='EPHEMERAL', provenance=None)
        self.assertEqual(check_ig2(obj), [])

    def test_ig2_violation_durable_null_provenance(self):
        obj = make_obj(persistence_stage='ATOMIC', provenance=None)
        violations = check_ig2(obj)
        self.assertTrue(len(violations) > 0)
        self.assertIn('IG2 VIOLATION', violations[0])

    def test_ig2_violation_orphan_no_parent_events(self):
        prov = make_prov(parent_event_ids=[])
        obj = make_obj(persistence_stage='CRYSTAL', provenance=prov)
        violations = check_ig2(obj)
        self.assertTrue(any('orphan' in v for v in violations))

    def test_ig2_violation_invalid_ts_first_seen(self):
        prov = make_prov()
        prov.ts_first_seen = -1.0  # bypass __post_init__ by setting after creation
        obj = make_obj(persistence_stage='ATOMIC', provenance=prov)
        violations = check_ig2(obj)
        self.assertTrue(any('ts_first_seen' in v for v in violations))

    def test_ig2_violation_negative_revision_num(self):
        prov = make_prov(revision_num=-1)
        obj = make_obj(persistence_stage='ATOMIC', provenance=prov)
        violations = check_ig2(obj)
        self.assertTrue(any('revision_num' in v for v in violations))


# ─── IG3: EVIDENCE ───────────────────────────────────────────────────────────

class TestIG3Evidence(unittest.TestCase):

    def test_ig3_all_valid_statuses(self):
        for status in ['OBSERVED', 'INFERRED', 'SYNTHESIZED',
                       'CONTRADICTED', 'SUPERSEDED', 'UNRESOLVED']:
            obj = make_obj(evidential_status=status)
            self.assertEqual(check_ig3(obj), [],
                             f"Expected clean for evidential_status={status}")

    def test_ig3_violation_unknown_status(self):
        obj = make_obj(evidential_status='MAGICAL')
        violations = check_ig3(obj)
        self.assertTrue(len(violations) > 0)

    def test_ig3_change_allowed_inferred_to_synthesized(self):
        obj = make_obj(evidential_status='INFERRED')
        change_evidential_status(obj, 'SYNTHESIZED', reason='test', authority_id='test')
        self.assertEqual(obj.evidential_status, 'SYNTHESIZED')

    def test_ig3_change_allowed_observed_to_contradicted(self):
        obj = make_obj(evidential_status='OBSERVED')
        change_evidential_status(obj, 'CONTRADICTED', reason='conflict', authority_id='test')
        self.assertEqual(obj.evidential_status, 'CONTRADICTED')

    def test_ig3_synthesized_to_observed_raises(self):
        obj = make_obj(evidential_status='SYNTHESIZED')
        with self.assertRaises(PermissionError):
            change_evidential_status(obj, 'OBSERVED', reason='test', authority_id='test')

    def test_ig3_no_op_same_status(self):
        obj = make_obj(evidential_status='INFERRED')
        original_rev = obj.provenance.revision_num
        change_evidential_status(obj, 'INFERRED', reason='no-op', authority_id='test')
        self.assertEqual(obj.provenance.revision_num, original_rev)

    def test_ig3_change_increments_revision(self):
        obj = make_obj(evidential_status='OBSERVED')
        original_rev = obj.provenance.revision_num
        change_evidential_status(obj, 'INFERRED', reason='test', authority_id='test')
        self.assertEqual(obj.provenance.revision_num, original_rev + 1)

    def test_ig3_unknown_new_status_raises(self):
        obj = make_obj(evidential_status='OBSERVED')
        with self.assertRaises(ValueError):
            change_evidential_status(obj, 'MADE_UP', reason='test', authority_id='test')


# ─── IG4: PROMOTION ──────────────────────────────────────────────────────────

class TestIG4Promotion(unittest.TestCase):

    def test_ig4_clean_real(self):
        obj = make_obj(tier_class='REAL', stability_score=0.0)
        self.assertEqual(check_ig4(obj), [])

    def test_ig4_clean_semiprime_above_gate(self):
        obj = make_obj(tier_class='SEMIPRIME', stability_score=0.7)
        self.assertEqual(check_ig4(obj), [])

    def test_ig4_violation_semiprime_below_stability(self):
        obj = make_obj(tier_class='SEMIPRIME', stability_score=0.4)
        violations = check_ig4(obj)
        self.assertTrue(len(violations) > 0)

    def test_ig4_clean_composite_with_supports(self):
        prov = make_prov(supporting_ids=['obj_a', 'obj_b'])
        obj = make_obj(tier_class='COMPOSITE', stability_score=0.8, provenance=prov)
        self.assertEqual(check_ig4(obj), [])

    def test_ig4_violation_composite_below_stability(self):
        prov = make_prov(supporting_ids=['obj_a', 'obj_b'])
        obj = make_obj(tier_class='COMPOSITE', stability_score=0.5, provenance=prov)
        violations = check_ig4(obj)
        self.assertTrue(any('COMPOSITE' in v for v in violations))

    def test_ig4_violation_composite_insufficient_supports(self):
        prov = make_prov(supporting_ids=['only_one'])
        obj = make_obj(tier_class='COMPOSITE', stability_score=0.9, provenance=prov)
        violations = check_ig4(obj)
        self.assertTrue(any('supporting' in v for v in violations))

    def test_ig4_promote_real_to_semiprime_succeeds(self):
        obj = make_obj(tier_class='REAL', stability_score=0.65,
                       evidential_status='OBSERVED')
        promote(obj, 'SEMIPRIME')
        self.assertEqual(obj.tier_class, 'SEMIPRIME')

    def test_ig4_promote_tier_skip_raises(self):
        obj = make_obj(tier_class='REAL', stability_score=0.9,
                       evidential_status='OBSERVED')
        with self.assertRaises(PermissionError):
            promote(obj, 'COMPOSITE')

    def test_ig4_promote_below_stability_raises(self):
        obj = make_obj(tier_class='REAL', stability_score=0.3,
                       evidential_status='OBSERVED')
        with self.assertRaises(PermissionError):
            promote(obj, 'SEMIPRIME')

    def test_ig4_promote_synthesized_to_semiprime_raises(self):
        obj = make_obj(tier_class='REAL', stability_score=0.9,
                       evidential_status='SYNTHESIZED')
        with self.assertRaises(PermissionError):
            promote(obj, 'SEMIPRIME')


# ─── IG5: REVISION ───────────────────────────────────────────────────────────

class TestIG5Revision(unittest.TestCase):

    def test_ig5_clean_active(self):
        obj = make_obj(forgetting_state='ACTIVE')
        self.assertEqual(check_ig5(obj), [])

    def test_ig5_all_valid_states(self):
        for state in ['ACTIVE', 'STALE', 'ARCHIVED', 'SUPERSEDED', 'CONTRADICTED', 'DEAD']:
            obj = make_obj(forgetting_state=state)
            self.assertEqual(check_ig5(obj), [],
                             f"Expected clean for forgetting_state={state}")

    def test_ig5_violation_unknown_state(self):
        obj = make_obj(forgetting_state='LIMBO')
        violations = check_ig5(obj)
        self.assertTrue(len(violations) > 0)

    def test_ig5_dead_is_terminal(self):
        obj = make_obj(forgetting_state='DEAD')
        with self.assertRaises(PermissionError):
            change_forgetting_state(obj, 'ACTIVE')

    def test_ig5_dead_to_dead_also_raises(self):
        obj = make_obj(forgetting_state='DEAD')
        with self.assertRaises(PermissionError):
            change_forgetting_state(obj, 'STALE')

    def test_ig5_contradicted_to_active_without_resolution_raises(self):
        obj = make_obj(forgetting_state='CONTRADICTED')
        with self.assertRaises(PermissionError):
            change_forgetting_state(obj, 'ACTIVE')

    def test_ig5_contradicted_to_active_with_resolution_succeeds(self):
        obj = make_obj(forgetting_state='CONTRADICTED')
        change_forgetting_state(obj, 'ACTIVE',
                                reason='resolved by new derivation',
                                resolution_event_id='evt_resolution_42')
        self.assertEqual(obj.forgetting_state, 'ACTIVE')

    def test_ig5_active_to_stale_succeeds(self):
        obj = make_obj(forgetting_state='ACTIVE')
        change_forgetting_state(obj, 'STALE', reason='aged out')
        self.assertEqual(obj.forgetting_state, 'STALE')

    def test_ig5_change_increments_revision(self):
        obj = make_obj(forgetting_state='ACTIVE')
        original_rev = obj.provenance.revision_num
        change_forgetting_state(obj, 'STALE', reason='test')
        self.assertEqual(obj.provenance.revision_num, original_rev + 1)


# ─── RETRIEVAL WEIGHT ────────────────────────────────────────────────────────

class TestRetrievalWeight(unittest.TestCase):

    def test_weight_dead_is_zero(self):
        obj = make_obj(forgetting_state='DEAD')
        self.assertEqual(retrieval_weight(obj), 0.0)

    def test_weight_max_for_best_object(self):
        # OBSERVED + COMPOSITE + ACTIVE + stability=1.0
        # retrieval_weight uses 50/50 blend: sw = 0.5 + 0.5*1.0 = 1.0
        prov = make_prov(supporting_ids=['s1', 's2'])
        obj = make_obj(tier_class='COMPOSITE', evidential_status='OBSERVED',
                       forgetting_state='ACTIVE', stability_score=1.0, provenance=prov)
        w = retrieval_weight(obj)
        expected = EVIDENCE_WEIGHTS['OBSERVED'] * TIER_WEIGHTS['COMPOSITE'] * 1.0 * 1.0
        self.assertAlmostEqual(w, expected, places=6)

    def test_weight_synthesized_lower_than_observed(self):
        obj_obs = make_obj(evidential_status='OBSERVED', stability_score=0.8)
        obj_syn = make_obj(evidential_status='SYNTHESIZED', stability_score=0.8)
        self.assertGreater(retrieval_weight(obj_obs), retrieval_weight(obj_syn))

    def test_weight_stale_lower_than_active(self):
        obj_active = make_obj(forgetting_state='ACTIVE', stability_score=0.5)
        obj_stale = make_obj(forgetting_state='STALE', stability_score=0.5)
        self.assertGreater(retrieval_weight(obj_active), retrieval_weight(obj_stale))

    def test_weight_positive_for_valid_object(self):
        obj = make_obj()
        self.assertGreater(retrieval_weight(obj), 0.0)

    def test_new_object_zero_stability_not_invisible(self):
        # stability_score=0.0 should still produce positive weight (50/50 blend)
        obj = make_obj(stability_score=0.0, evidential_status='OBSERVED')
        self.assertGreater(retrieval_weight(obj), 0.0)


# ─── DRIFT DETECTION ─────────────────────────────────────────────────────────

class TestDriftDetection(unittest.TestCase):

    def test_drift_detected_operator_in_prompt(self):
        prompt = "Explain the BALANCE operator and what BREATH means in TIG."
        response = "In my architecture, BALANCE represents the equilibrium state in the TIG pipeline."
        self.assertTrue(detect_operator_drift(prompt, response))

    def test_no_drift_clean_math_response(self):
        prompt = "What is the absorbing element of Z/10Z?"
        response = "The absorbing idempotent of Z/10Z is 5, since 5 squared equals 5 mod 10."
        self.assertFalse(detect_operator_drift(prompt, response))

    def test_no_drift_no_operators_in_prompt(self):
        prompt = "Tell me about prime numbers."
        response = "My architecture processes primes through the framework."
        # Drift phrases in response but no CK operators in prompt — should not trigger
        self.assertFalse(detect_operator_drift(prompt, response))

    def test_drift_case_insensitive_prompt(self):
        prompt = "what does balance do?"
        response = "In my architecture, balance defines the threshold."
        self.assertTrue(detect_operator_drift(prompt, response))


# ─── REGISTER DISCOVERY ──────────────────────────────────────────────────────

class TestRegisterDiscovery(unittest.TestCase):

    def test_register_tstar_derivation(self):
        obj = register_discovery(
            discovery_id='tstar_ring_absorption',
            content={
                'claim': 'T* = 5/7 forced by Z/10Z ring absorption',
                'alpha': 5, 'beta': 7, 'ratio': '5/7',
            },
            derivation_sources=['session_2026_04_05_sprint8', 'ck_sim_heartbeat'],
            produced_by='CK_CL_algebra',
        )
        self.assertEqual(obj.tier_class, 'COMPOSITE')
        self.assertEqual(obj.evidential_status, 'OBSERVED')
        self.assertEqual(obj.forgetting_state, 'ACTIVE')
        self.assertGreater(retrieval_weight(obj), 0.0)

    def test_register_validates_on_creation(self):
        # Should not raise — 2 sources satisfies COMPOSITE supporting_ids >= 2 gate
        obj = register_discovery(
            discovery_id='balance_absorbing',
            content={'claim': '5*k ≡ 5 (mod 10) for all odd k'},
            derivation_sources=['session_2026_04_04', 'sprint8_ring_audit'],
        )
        violations = validate_object(obj, strict=False)
        self.assertEqual(violations, [])


# ─── COMBINED VALIDATE ───────────────────────────────────────────────────────

class TestValidateObject(unittest.TestCase):

    def test_validate_clean_object_passes(self):
        obj = make_obj()
        violations = validate_object(obj, strict=False)
        self.assertEqual(violations, [])

    def test_validate_strict_raises_on_ig1(self):
        obj = make_obj(source_side='EXTERNAL', privacy_class='PRIVATE',
                       persistence_stage='CRYSTAL')
        with self.assertRaises(AssertionError):
            validate_object(obj, strict=True)

    def test_validate_non_strict_returns_list(self):
        obj = make_obj(evidential_status='UNKNOWN_STATUS')
        violations = validate_object(obj, strict=False)
        self.assertTrue(len(violations) > 0)

    def test_validate_multiple_violations_collected(self):
        obj = make_obj(
            source_side='EXTERNAL',
            privacy_class='PRIVATE',
            persistence_stage='CRYSTAL',
            evidential_status='UNKNOWN_STATUS',
        )
        violations = validate_object(obj, strict=False)
        self.assertGreaterEqual(len(violations), 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
