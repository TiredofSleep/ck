"""
ck_concept_spine_tests.py -- Tests for CK's Concept Spine
==========================================================
Validates: SPINE_CONCEPTS, SPINE_RELATIONS, ConceptSpine class,
           domain coverage, integration with WorldLattice.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import unittest
import os
import sys

# Ensure ck_sim package is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ================================================================
#  TestImport: Module imports and constants exist
# ================================================================

class TestImport(unittest.TestCase):
    """Test that the module imports correctly and constants exist."""

    def test_module_imports(self):
        """ck_concept_spine imports without error."""
        from ck_sim.ck_concept_spine import SPINE_CONCEPTS, SPINE_RELATIONS, ConceptSpine
        self.assertTrue(True)

    def test_spine_concepts_exists(self):
        """SPINE_CONCEPTS is a non-empty list."""
        from ck_sim.ck_concept_spine import SPINE_CONCEPTS
        self.assertIsInstance(SPINE_CONCEPTS, list)
        self.assertGreater(len(SPINE_CONCEPTS), 0)

    def test_spine_relations_exists(self):
        """SPINE_RELATIONS is a non-empty list."""
        from ck_sim.ck_concept_spine import SPINE_RELATIONS
        self.assertIsInstance(SPINE_RELATIONS, list)
        self.assertGreater(len(SPINE_RELATIONS), 0)

    def test_concept_spine_class_exists(self):
        """ConceptSpine class is importable and callable."""
        from ck_sim.ck_concept_spine import ConceptSpine
        self.assertTrue(callable(ConceptSpine))

    def test_imports_from_heartbeat(self):
        """Module imports operator constants from ck_sim_heartbeat."""
        from ck_sim.ck_concept_spine import (
            HARMONY, VOID, COLLAPSE, CHAOS, PROGRESS, BREATH,
            BALANCE, COUNTER, LATTICE, RESET
        )
        self.assertEqual(VOID, 0)
        self.assertEqual(HARMONY, 7)


# ================================================================
#  TestSpineConcepts: Concept tuples are well-formed
# ================================================================

class TestSpineConcepts(unittest.TestCase):
    """Test SPINE_CONCEPTS entries are valid."""

    def test_concepts_are_tuples(self):
        """Each concept is a 4-tuple."""
        from ck_sim.ck_concept_spine import SPINE_CONCEPTS
        for i, entry in enumerate(SPINE_CONCEPTS):
            self.assertEqual(len(entry), 4,
                             f"Concept at index {i} has {len(entry)} elements, expected 4")

    def test_operators_in_range(self):
        """All operator codes are 0-9."""
        from ck_sim.ck_concept_spine import SPINE_CONCEPTS, NUM_OPS
        for node_id, domain, op, bindings in SPINE_CONCEPTS:
            self.assertGreaterEqual(op, 0,
                                    f"Concept '{node_id}' has op {op} < 0")
            self.assertLess(op, NUM_OPS,
                            f"Concept '{node_id}' has op {op} >= {NUM_OPS}")

    def test_all_have_bindings(self):
        """Every concept has at least 'en' in bindings."""
        from ck_sim.ck_concept_spine import SPINE_CONCEPTS
        for node_id, domain, op, bindings in SPINE_CONCEPTS:
            self.assertIsInstance(bindings, dict,
                                 f"Concept '{node_id}' bindings is not a dict")
            self.assertIn('en', bindings,
                          f"Concept '{node_id}' missing 'en' binding")

    def test_multilingual_bindings(self):
        """Every concept has at least 7 language bindings."""
        from ck_sim.ck_concept_spine import SPINE_CONCEPTS
        required_langs = {'en', 'es', 'fr', 'de', 'he', 'ar', 'zh'}
        for node_id, domain, op, bindings in SPINE_CONCEPTS:
            for lang in required_langs:
                self.assertIn(lang, bindings,
                              f"Concept '{node_id}' missing '{lang}' binding")

    def test_unique_node_ids(self):
        """All node_ids within SPINE_CONCEPTS are unique."""
        from ck_sim.ck_concept_spine import SPINE_CONCEPTS
        seen = set()
        for node_id, domain, op, bindings in SPINE_CONCEPTS:
            self.assertNotIn(node_id, seen,
                             f"Duplicate node_id: '{node_id}'")
            seen.add(node_id)

    def test_concept_count_minimum(self):
        """At least 280 spine concepts exist."""
        from ck_sim.ck_concept_spine import SPINE_CONCEPTS
        self.assertGreaterEqual(len(SPINE_CONCEPTS), 280,
                                f"Only {len(SPINE_CONCEPTS)} concepts, expected >= 280")

    def test_node_ids_are_strings(self):
        """All node_ids are non-empty strings."""
        from ck_sim.ck_concept_spine import SPINE_CONCEPTS
        for node_id, domain, op, bindings in SPINE_CONCEPTS:
            self.assertIsInstance(node_id, str)
            self.assertGreater(len(node_id), 0)

    def test_domains_are_strings(self):
        """All domains are non-empty strings."""
        from ck_sim.ck_concept_spine import SPINE_CONCEPTS
        for node_id, domain, op, bindings in SPINE_CONCEPTS:
            self.assertIsInstance(domain, str)
            self.assertGreater(len(domain), 0)


# ================================================================
#  TestSpineRelations: Relations are well-formed
# ================================================================

class TestSpineRelations(unittest.TestCase):
    """Test SPINE_RELATIONS entries are valid."""

    def test_relations_are_triples(self):
        """Each relation is a 3-tuple."""
        from ck_sim.ck_concept_spine import SPINE_RELATIONS
        for i, entry in enumerate(SPINE_RELATIONS):
            self.assertEqual(len(entry), 3,
                             f"Relation at index {i} has {len(entry)} elements, expected 3")

    def test_valid_relation_types(self):
        """All relation types are valid RELATION_TYPES keys."""
        from ck_sim.ck_concept_spine import SPINE_RELATIONS
        from ck_sim.ck_world_lattice import RELATION_TYPES
        valid_types = set(RELATION_TYPES.keys())
        for source, rel, target in SPINE_RELATIONS:
            self.assertIn(rel, valid_types,
                          f"Invalid relation type '{rel}' in ({source}, {rel}, {target})")

    def test_relations_reference_valid_concepts(self):
        """All source and target in SPINE_RELATIONS reference known concepts."""
        from ck_sim.ck_concept_spine import SPINE_CONCEPTS, SPINE_RELATIONS
        from ck_sim.ck_world_lattice import CORE_CONCEPTS

        # Collect all known node_ids from both spine and core
        all_ids = set()
        for node_id, domain, op, bindings in SPINE_CONCEPTS:
            all_ids.add(node_id)
        for node_id, domain, op, bindings in CORE_CONCEPTS:
            all_ids.add(node_id)

        for source, rel, target in SPINE_RELATIONS:
            self.assertIn(source, all_ids,
                          f"Source '{source}' not found in concepts")
            self.assertIn(target, all_ids,
                          f"Target '{target}' not found in concepts")

    def test_relation_count_minimum(self):
        """At least 370 spine relations exist."""
        from ck_sim.ck_concept_spine import SPINE_RELATIONS
        self.assertGreaterEqual(len(SPINE_RELATIONS), 370,
                                f"Only {len(SPINE_RELATIONS)} relations, expected >= 370")


# ================================================================
#  TestConceptSpine: Class functionality
# ================================================================

class TestConceptSpine(unittest.TestCase):
    """Test the ConceptSpine class."""

    def test_init_default(self):
        """ConceptSpine can be created with default lattice."""
        from ck_sim.ck_concept_spine import ConceptSpine
        spine = ConceptSpine()
        self.assertIsNotNone(spine.lattice)

    def test_init_with_lattice(self):
        """ConceptSpine can be created with provided lattice."""
        from ck_sim.ck_concept_spine import ConceptSpine
        from ck_sim.ck_world_lattice import WorldLattice
        lattice = WorldLattice()
        spine = ConceptSpine(lattice=lattice)
        self.assertIs(spine.lattice, lattice)

    def test_load_spine_populates(self):
        """load_spine() adds concepts to the lattice."""
        from ck_sim.ck_concept_spine import ConceptSpine
        spine = ConceptSpine()
        self.assertEqual(len(spine.lattice.nodes), 0)
        spine.load_spine()
        self.assertGreater(len(spine.lattice.nodes), 0)

    def test_load_spine_loads_core_first(self):
        """load_spine() loads core concepts first when lattice is empty."""
        from ck_sim.ck_concept_spine import ConceptSpine, SPINE_CONCEPTS
        from ck_sim.ck_world_lattice import CORE_CONCEPTS
        spine = ConceptSpine()
        spine.load_spine()
        # Total should be at least core + spine
        expected_min = len(CORE_CONCEPTS) + len(SPINE_CONCEPTS)
        self.assertGreaterEqual(len(spine.lattice.nodes), expected_min)

    def test_query_domain_returns_results(self):
        """query_domain() returns concepts for a valid domain."""
        from ck_sim.ck_concept_spine import ConceptSpine
        spine = ConceptSpine()
        spine.load_spine()
        physics = spine.query_domain('physics')
        self.assertGreater(len(physics), 0)

    def test_spine_concept_count(self):
        """spine_concept_count matches SPINE_CONCEPTS length."""
        from ck_sim.ck_concept_spine import ConceptSpine, SPINE_CONCEPTS
        spine = ConceptSpine()
        self.assertEqual(spine.spine_concept_count, len(SPINE_CONCEPTS))

    def test_spine_relation_count(self):
        """spine_relation_count matches SPINE_RELATIONS length."""
        from ck_sim.ck_concept_spine import ConceptSpine, SPINE_RELATIONS
        spine = ConceptSpine()
        self.assertEqual(spine.spine_relation_count, len(SPINE_RELATIONS))

    def test_stats_returns_dict(self):
        """stats() returns a dict with expected keys."""
        from ck_sim.ck_concept_spine import ConceptSpine
        spine = ConceptSpine()
        spine.load_spine()
        s = spine.stats()
        self.assertIsInstance(s, dict)
        self.assertIn('spine_concepts', s)
        self.assertIn('spine_relations', s)
        self.assertIn('total_nodes', s)
        self.assertIn('total_languages', s)
        self.assertIn('domains', s)

    def test_stats_total_nodes(self):
        """stats() total_nodes matches lattice size."""
        from ck_sim.ck_concept_spine import ConceptSpine
        spine = ConceptSpine()
        spine.load_spine()
        s = spine.stats()
        self.assertEqual(s['total_nodes'], len(spine.lattice.nodes))


# ================================================================
#  TestDomainCoverage: Each domain has concepts
# ================================================================

class TestDomainCoverage(unittest.TestCase):
    """Test that all expected domains are present."""

    def test_physics_domain(self):
        """Physics domain has concepts."""
        from ck_sim.ck_concept_spine import SPINE_CONCEPTS
        physics = [c for c in SPINE_CONCEPTS if c[1] == 'physics']
        self.assertGreater(len(physics), 30)

    def test_chemistry_domain(self):
        """Chemistry domain has concepts."""
        from ck_sim.ck_concept_spine import SPINE_CONCEPTS
        chem = [c for c in SPINE_CONCEPTS if c[1] == 'chemistry']
        self.assertGreater(len(chem), 20)

    def test_biology_domain(self):
        """Biology domain has concepts."""
        from ck_sim.ck_concept_spine import SPINE_CONCEPTS
        bio = [c for c in SPINE_CONCEPTS if c[1] == 'biology']
        self.assertGreater(len(bio), 30)

    def test_mathematics_domain(self):
        """Mathematics domain has concepts."""
        from ck_sim.ck_concept_spine import SPINE_CONCEPTS
        math = [c for c in SPINE_CONCEPTS if c[1] == 'mathematics']
        self.assertGreater(len(math), 20)

    def test_philosophy_domain(self):
        """Philosophy domain has concepts."""
        from ck_sim.ck_concept_spine import SPINE_CONCEPTS
        phil = [c for c in SPINE_CONCEPTS if c[1] == 'philosophy']
        self.assertGreater(len(phil), 15)

    def test_language_domain(self):
        """Language domain has concepts."""
        from ck_sim.ck_concept_spine import SPINE_CONCEPTS
        lang = [c for c in SPINE_CONCEPTS if c[1] == 'language']
        self.assertGreater(len(lang), 15)

    def test_emotions_domain(self):
        """Emotions domain has concepts."""
        from ck_sim.ck_concept_spine import SPINE_CONCEPTS
        emo = [c for c in SPINE_CONCEPTS if c[1] == 'emotions']
        self.assertGreater(len(emo), 15)

    def test_society_domain(self):
        """Society domain has concepts."""
        from ck_sim.ck_concept_spine import SPINE_CONCEPTS
        soc = [c for c in SPINE_CONCEPTS if c[1] == 'society']
        self.assertGreater(len(soc), 15)


# ================================================================
#  TestIntegration: Spine integrates with WorldLattice
# ================================================================

class TestIntegration(unittest.TestCase):
    """Test spine concepts integrate with existing world lattice."""

    def test_no_duplicate_node_ids_with_core(self):
        """Spine node_ids do not conflict with CORE_CONCEPTS."""
        from ck_sim.ck_concept_spine import SPINE_CONCEPTS
        from ck_sim.ck_world_lattice import CORE_CONCEPTS

        core_ids = set(nid for nid, d, o, b in CORE_CONCEPTS)
        spine_ids = set(nid for nid, d, o, b in SPINE_CONCEPTS)
        overlap = core_ids & spine_ids
        self.assertEqual(len(overlap), 0,
                         f"Duplicate node_ids between core and spine: {overlap}")

    def test_spine_can_load_on_top_of_core(self):
        """ConceptSpine loads after core without error."""
        from ck_sim.ck_concept_spine import ConceptSpine
        spine = ConceptSpine()
        spine.load_spine()
        # Should have both core and spine concepts
        self.assertGreater(len(spine.lattice.nodes), 300)

    def test_cross_domain_relations_work(self):
        """Cross-domain relations connect spine and core concepts."""
        from ck_sim.ck_concept_spine import ConceptSpine
        spine = ConceptSpine()
        spine.load_spine()
        # 'atom' (spine) should be connected to 'element' (spine)
        neighbors = spine.lattice.get_neighbors('atom')
        target_ids = [t for t, r, o in neighbors]
        # atom should have relations
        self.assertGreater(len(neighbors), 0)

    def test_combined_lattice_has_languages(self):
        """Combined lattice has multiple languages."""
        from ck_sim.ck_concept_spine import ConceptSpine
        spine = ConceptSpine()
        spine.load_spine()
        self.assertGreater(len(spine.lattice.languages_seen), 5)


# ================================================================
#  Run
# ================================================================

if __name__ == '__main__':
    unittest.main()
