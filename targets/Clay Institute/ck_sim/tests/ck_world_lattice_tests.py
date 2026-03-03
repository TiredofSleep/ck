"""
ck_world_lattice_tests.py -- Tests for CK's World Lattice
==========================================================
Validates: transliteration, D2 cross-language, concept graph,
           relations, MDL compression, snapshot, multilingual bindings.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import unittest
import os
import json
import tempfile
import sys

# Ensure ck_sim package is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestTransliteration(unittest.TestCase):
    """Test non-Latin script transliteration to Latin letters."""

    def test_import(self):
        """Module imports without error."""
        from ck_sim.ck_world_lattice import transliterate
        self.assertTrue(callable(transliterate))

    def test_latin_passthrough(self):
        """Latin letters pass through unchanged."""
        from ck_sim.ck_world_lattice import transliterate
        self.assertEqual(transliterate('hello'), 'hello')
        self.assertEqual(transliterate('Mother'), 'mother')

    def test_cyrillic(self):
        """Cyrillic transliterates to Latin."""
        from ck_sim.ck_world_lattice import transliterate
        result = transliterate('мать')  # mat' (mother)
        self.assertTrue(len(result) > 0)
        self.assertTrue(all('a' <= c <= 'z' for c in result))

    def test_hebrew(self):
        """Hebrew transliterates to Latin."""
        from ck_sim.ck_world_lattice import transliterate
        result = transliterate('שלום')  # shalom (peace)
        self.assertTrue(len(result) > 0)
        self.assertTrue(all('a' <= c <= 'z' for c in result))

    def test_arabic(self):
        """Arabic transliterates to Latin."""
        from ck_sim.ck_world_lattice import transliterate
        result = transliterate('سلام')  # salaam (peace)
        self.assertTrue(len(result) > 0)
        self.assertTrue(all('a' <= c <= 'z' for c in result))

    def test_greek(self):
        """Greek transliterates to Latin."""
        from ck_sim.ck_world_lattice import transliterate
        result = transliterate('αληθεια')  # aletheia (truth)
        self.assertTrue(len(result) > 0)
        self.assertTrue(all('a' <= c <= 'z' for c in result))

    def test_hiragana(self):
        """Japanese hiragana transliterates to Latin."""
        from ck_sim.ck_world_lattice import transliterate
        result = transliterate('こころ')  # kokoro (heart/mind)
        self.assertTrue(len(result) > 0)

    def test_mixed_scripts(self):
        """Mixed scripts transliterate without error."""
        from ck_sim.ck_world_lattice import transliterate
        result = transliterate('hello мир world')
        self.assertTrue(len(result) > 0)
        self.assertTrue(all('a' <= c <= 'z' for c in result))

    def test_empty_and_unknown(self):
        """Empty and unknown characters handled gracefully."""
        from ck_sim.ck_world_lattice import transliterate
        self.assertEqual(transliterate(''), '')
        # Punctuation and numbers are dropped
        result = transliterate('123!@#')
        self.assertEqual(result, '')


class TestD2CrossLanguage(unittest.TestCase):
    """Test D2 curvature analysis across languages."""

    def test_word_to_d2_basic(self):
        """word_to_d2 returns valid tuple."""
        from ck_sim.ck_world_lattice import word_to_d2
        op, ops, vec, soft = word_to_d2('mother')
        self.assertIsInstance(op, int)
        self.assertTrue(0 <= op <= 9)
        self.assertIsInstance(ops, list)
        self.assertEqual(len(vec), 5)
        self.assertEqual(len(soft), 10)

    def test_word_to_d2_nonlatin(self):
        """word_to_d2 works on non-Latin words."""
        from ck_sim.ck_world_lattice import word_to_d2
        op, ops, vec, soft = word_to_d2('мать')  # Russian: mother
        self.assertIsInstance(op, int)
        self.assertEqual(len(vec), 5)

    def test_d2_agreement_self(self):
        """D2 agreement of a word with itself is ~1.0."""
        from ck_sim.ck_world_lattice import d2_agreement
        score = d2_agreement('mother', 'mother')
        self.assertAlmostEqual(score, 1.0, places=3)

    def test_d2_agreement_cross_language(self):
        """D2 agreement between translations is measurable."""
        from ck_sim.ck_world_lattice import d2_agreement
        # These may or may not be high, but they should be computable
        score = d2_agreement('mother', 'madre')
        self.assertIsInstance(score, float)
        self.assertTrue(0.0 <= score <= 1.0)

    def test_d2_agreement_short_words(self):
        """Very short words produce valid (possibly low) agreement."""
        from ck_sim.ck_world_lattice import d2_agreement
        score = d2_agreement('ai', 'ai')  # Japanese/Chinese: love
        self.assertIsInstance(score, float)


class TestWorldNode(unittest.TestCase):
    """Test WorldNode creation and serialization."""

    def test_create_node(self):
        """WorldNode created with all fields."""
        from ck_sim.ck_world_lattice import WorldNode, HARMONY
        node = WorldNode('test', HARMONY, [0.1, 0.2, 0.3, 0.4, 0.5])
        self.assertEqual(node.node_id, 'test')
        self.assertEqual(node.operator_code, HARMONY)
        self.assertEqual(len(node.d2_signature), 5)

    def test_bind_word(self):
        """Words bind to nodes correctly."""
        from ck_sim.ck_world_lattice import WorldNode, HARMONY
        node = WorldNode('test', HARMONY)
        node.bind_word('en', 'truth')
        node.bind_word('es', 'verdad')
        self.assertEqual(node.bindings['en'], 'truth')
        self.assertEqual(node.bindings['es'], 'verdad')

    def test_add_relation(self):
        """Relations added correctly."""
        from ck_sim.ck_world_lattice import WorldNode, HARMONY, PROGRESS
        node = WorldNode('source', HARMONY)
        node.add_relation('causes', 'target', PROGRESS)
        self.assertIn('causes', node.relations)
        self.assertEqual(len(node.relations['causes']), 1)
        self.assertEqual(node.relations['causes'][0], ('target', PROGRESS))

    def test_serialization_roundtrip(self):
        """WorldNode serializes and deserializes correctly."""
        from ck_sim.ck_world_lattice import WorldNode, HARMONY, PROGRESS
        node = WorldNode('test', HARMONY, [0.1, 0.2, 0.3, 0.4, 0.5])
        node.bind_word('en', 'truth')
        node.add_relation('causes', 'other', PROGRESS)
        d = node.to_dict()
        restored = WorldNode.from_dict(d)
        self.assertEqual(restored.node_id, 'test')
        self.assertEqual(restored.operator_code, HARMONY)
        self.assertEqual(restored.bindings['en'], 'truth')
        self.assertIn('causes', restored.relations)


class TestWorldLattice(unittest.TestCase):
    """Test the world lattice graph."""

    def _make_lattice(self):
        from ck_sim.ck_world_lattice import build_world_lattice
        return build_world_lattice()

    def test_build_lattice(self):
        """Lattice builds from seed corpus."""
        lattice = self._make_lattice()
        self.assertTrue(len(lattice.nodes) > 50)

    def test_concept_count(self):
        """All seed concepts loaded."""
        from ck_sim.ck_world_lattice import CORE_CONCEPTS
        lattice = self._make_lattice()
        self.assertEqual(len(lattice.nodes), len(CORE_CONCEPTS))

    def test_relation_count(self):
        """Relations loaded."""
        lattice = self._make_lattice()
        total_edges = sum(
            sum(len(t) for t in n.relations.values())
            for n in lattice.nodes.values()
        )
        self.assertTrue(total_edges > 50)

    def test_multilingual_bindings(self):
        """Multiple languages present."""
        lattice = self._make_lattice()
        self.assertTrue(len(lattice.languages_seen) >= 10)
        self.assertIn('en', lattice.languages_seen)
        self.assertIn('es', lattice.languages_seen)
        self.assertIn('fr', lattice.languages_seen)
        self.assertIn('he', lattice.languages_seen)
        self.assertIn('ar', lattice.languages_seen)
        self.assertIn('zh', lattice.languages_seen)
        self.assertIn('ja', lattice.languages_seen)

    def test_lookup_english(self):
        """Lookup word in English."""
        lattice = self._make_lattice()
        node = lattice.lookup_word('mother', 'en')
        self.assertIsNotNone(node)
        self.assertEqual(node.node_id, 'mother')

    def test_lookup_spanish(self):
        """Lookup word in Spanish."""
        lattice = self._make_lattice()
        node = lattice.lookup_word('madre', 'es')
        self.assertIsNotNone(node)
        self.assertEqual(node.node_id, 'mother')

    def test_lookup_cross_language(self):
        """Same concept found from different languages."""
        lattice = self._make_lattice()
        en = lattice.lookup_word('water', 'en')
        es = lattice.lookup_word('agua', 'es')
        fr = lattice.lookup_word('eau', 'fr')
        self.assertIsNotNone(en)
        self.assertIsNotNone(es)
        self.assertIsNotNone(fr)
        self.assertEqual(en.node_id, es.node_id)
        self.assertEqual(es.node_id, fr.node_id)

    def test_lookup_any_language(self):
        """Lookup without specifying language."""
        lattice = self._make_lattice()
        node = lattice.lookup_word('agua')
        self.assertIsNotNone(node)
        self.assertEqual(node.node_id, 'water')

    def test_query_by_operator(self):
        """Query concepts by operator."""
        from ck_sim.ck_world_lattice import HARMONY
        lattice = self._make_lattice()
        harmony_nodes = lattice.query_by_operator(HARMONY)
        self.assertTrue(len(harmony_nodes) > 5)
        for node in harmony_nodes:
            self.assertEqual(node.operator_code, HARMONY)

    def test_query_by_domain(self):
        """Query concepts by domain."""
        lattice = self._make_lattice()
        physics = lattice.query_by_domain('physics')
        self.assertTrue(len(physics) > 3)
        for node in physics:
            self.assertEqual(node.domain, 'physics')

    def test_get_neighbors(self):
        """Get neighbors of a node."""
        lattice = self._make_lattice()
        neighbors = lattice.get_neighbors('water')
        self.assertTrue(len(neighbors) > 0)

    def test_coherence_path(self):
        """Find a path between concepts."""
        lattice = self._make_lattice()
        path = lattice.coherence_path('water', 'life')
        # water sustains life, so direct path should exist
        self.assertIsNotNone(path)
        self.assertEqual(path[0], 'water')
        self.assertEqual(path[-1], 'life')

    def test_bind_new_word_explicit(self):
        """Bind a new word to a specific node."""
        lattice = self._make_lattice()
        result = lattice.bind_new_word('woda', 'pl', 'water')  # Polish: water
        self.assertEqual(result, 'water')
        node = lattice.lookup_word('woda', 'pl')
        self.assertIsNotNone(node)
        self.assertEqual(node.node_id, 'water')

    def test_bind_new_word_auto(self):
        """Bind a new word via D2 auto-matching."""
        lattice = self._make_lattice()
        # This may or may not find a match above threshold
        result = lattice.bind_new_word('acqua', 'it_alt')
        # Just verify it doesn't crash
        self.assertIsInstance(result, (str, type(None)))


class TestMDLCompression(unittest.TestCase):
    """Test Minimum Description Length computation and compression."""

    def _make_lattice(self):
        from ck_sim.ck_world_lattice import build_world_lattice
        return build_world_lattice()

    def test_description_length(self):
        """MDL computation returns valid dict."""
        lattice = self._make_lattice()
        mdl = lattice.description_length()
        self.assertIn('total_mdl', mdl)
        self.assertIn('n_nodes', mdl)
        self.assertIn('n_edges', mdl)
        self.assertIn('n_bindings', mdl)
        self.assertTrue(mdl['total_mdl'] > 0)
        self.assertTrue(mdl['n_nodes'] > 50)
        self.assertTrue(mdl['n_bindings'] > 100)

    def test_compress_no_crash(self):
        """Compression runs without error."""
        lattice = self._make_lattice()
        result = lattice.compress()
        self.assertIn('nodes_merged', result)
        self.assertIn('mdl_before', result)
        self.assertIn('mdl_after', result)
        # MDL should not increase after compression
        self.assertTrue(result['mdl_after'] <= result['mdl_before'])

    def test_compress_preserves_invariants(self):
        """Compression preserves node integrity."""
        lattice = self._make_lattice()
        n_before = len(lattice.nodes)
        lattice.compress()
        n_after = len(lattice.nodes)
        # Should have same or fewer nodes
        self.assertTrue(n_after <= n_before)
        # Every remaining node should be valid
        for nid, node in lattice.nodes.items():
            self.assertEqual(node.node_id, nid)
            self.assertTrue(0 <= node.operator_code <= 9)


class TestSnapshotIO(unittest.TestCase):
    """Test snapshot save/load."""

    def _make_lattice(self):
        from ck_sim.ck_world_lattice import build_world_lattice
        return build_world_lattice()

    def test_snapshot(self):
        """Snapshot produces valid dict."""
        lattice = self._make_lattice()
        snap = lattice.snapshot()
        self.assertIn('version', snap)
        self.assertIn('core_math', snap)
        self.assertIn('lattice', snap)
        self.assertIn('mdl', snap)
        self.assertEqual(snap['core_math']['num_operators'], 10)

    def test_save_load_roundtrip(self):
        """Save and load produces equivalent lattice."""
        from ck_sim.ck_world_lattice import WorldLattice
        lattice = self._make_lattice()
        n_original = len(lattice.nodes)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                         delete=False) as f:
            path = f.name
        try:
            lattice.save(path)
            # Verify file exists and has content
            self.assertTrue(os.path.exists(path))
            self.assertTrue(os.path.getsize(path) > 1000)

            # Load into fresh lattice
            loaded = WorldLattice()
            loaded.load(path)
            self.assertEqual(len(loaded.nodes), n_original)

            # Check a specific node survived
            mother = loaded.nodes.get('mother')
            self.assertIsNotNone(mother)
            self.assertIn('en', mother.bindings)
            self.assertEqual(mother.bindings['en'], 'mother')
        finally:
            os.unlink(path)


class TestCrossLanguageReport(unittest.TestCase):
    """Test D2 cross-language agreement reporting."""

    def test_report_generation(self):
        """Cross-language report generates without error."""
        from ck_sim.ck_world_lattice import build_world_lattice
        lattice = build_world_lattice()
        report = lattice.d2_cross_language_report()
        self.assertIsInstance(report, list)
        self.assertTrue(len(report) > 10)

    def test_report_structure(self):
        """Report entries have correct structure."""
        from ck_sim.ck_world_lattice import build_world_lattice
        lattice = build_world_lattice()
        report = lattice.d2_cross_language_report()
        entry = report[0]
        self.assertIn('concept', entry)
        self.assertIn('operator', entry)
        self.assertIn('n_languages', entry)
        self.assertIn('avg_agreement', entry)
        self.assertIn('pairs', entry)
        self.assertTrue(0.0 <= entry['avg_agreement'] <= 1.0)


class TestStats(unittest.TestCase):
    """Test lattice statistics."""

    def test_stats_complete(self):
        """Stats dict has all expected fields."""
        from ck_sim.ck_world_lattice import build_world_lattice
        lattice = build_world_lattice()
        stats = lattice.stats()
        self.assertIn('n_nodes', stats)
        self.assertIn('n_edges', stats)
        self.assertIn('n_bindings', stats)
        self.assertIn('n_languages', stats)
        self.assertIn('languages', stats)
        self.assertIn('domains', stats)
        self.assertIn('operator_distribution', stats)
        self.assertIn('mdl', stats)


class TestIntegrationWithExisting(unittest.TestCase):
    """Test that world lattice integrates with existing CK modules."""

    def test_operators_match(self):
        """World lattice uses the same operator constants as heartbeat."""
        from ck_sim.ck_world_lattice import (
            HARMONY, VOID, LATTICE, COUNTER, PROGRESS,
            COLLAPSE, BALANCE, CHAOS, BREATH, RESET
        )
        from ck_sim.ck_sim_heartbeat import (
            HARMONY as HB_HARMONY, VOID as HB_VOID
        )
        self.assertEqual(HARMONY, HB_HARMONY)
        self.assertEqual(VOID, HB_VOID)

    def test_compose_in_lattice(self):
        """CL composition works within lattice context."""
        from ck_sim.ck_world_lattice import compose, HARMONY, LATTICE
        result = compose(LATTICE, LATTICE)
        self.assertEqual(result, HARMONY)

    def test_d2_pipeline_in_lattice(self):
        """D2 pipeline works within lattice context."""
        from ck_sim.ck_world_lattice import word_to_d2
        op, ops, vec, soft = word_to_d2('coherence')
        self.assertIsInstance(op, int)
        self.assertTrue(len(ops) > 0)

    def test_lattice_feeds_composer(self):
        """World lattice concepts can feed the sentence composer."""
        from ck_sim.ck_world_lattice import build_world_lattice
        lattice = build_world_lattice()
        # Get operator chain from a concept path
        path = lattice.coherence_path('water', 'life')
        if path:
            ops = [lattice.nodes[nid].operator_code for nid in path]
            self.assertTrue(len(ops) >= 2)
            # Try composing through CL
            from ck_sim.ck_sim_heartbeat import compose
            fuse = ops[0]
            for i in range(1, len(ops)):
                fuse = compose(fuse, ops[i])
            self.assertTrue(0 <= fuse <= 9)


# ================================================================
#  MAIN
# ================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("  CK WORLD LATTICE -- VALIDATION TESTS")
    print("=" * 60)

    unittest.main(verbosity=2)
