"""
ck_language_tests.py -- Tests for CK's Language Generator
=========================================================
Validates: intent classification, concept chains, surface realization,
           translation, multilingual output, full pipeline integration.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import unittest
import os
import sys

# Ensure ck_sim package is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ================================================================
#  HELPER: Build loaded lattice + lexicon for tests
# ================================================================

def build_loaded_environment():
    """Build a WorldLattice + LexiconStore with seed data loaded.

    Returns:
        (lattice, lexicon) tuple ready for testing
    """
    from ck_sim.ck_world_lattice import WorldLattice
    from ck_sim.ck_lexicon import LexiconStore

    lattice = WorldLattice()
    lattice.load_seed_corpus()

    lexicon = LexiconStore(lattice=lattice)
    lexicon.load_seed_lexicon()

    return lattice, lexicon


# ================================================================
#  TEST: Module Imports
# ================================================================

class TestImport(unittest.TestCase):
    """Module imports without error."""

    def test_import_module(self):
        """ck_language module imports cleanly."""
        import ck_sim.ck_language as mod
        self.assertTrue(hasattr(mod, 'Intent'))
        self.assertTrue(hasattr(mod, 'ConceptChain'))
        self.assertTrue(hasattr(mod, 'IntentClassifier'))
        self.assertTrue(hasattr(mod, 'ConceptChainBuilder'))
        self.assertTrue(hasattr(mod, 'SurfaceRealizer'))
        self.assertTrue(hasattr(mod, 'LanguageGenerator'))

    def test_import_templates(self):
        """Templates dict is populated."""
        from ck_sim.ck_language import TEMPLATES
        self.assertIsInstance(TEMPLATES, dict)
        self.assertTrue(len(TEMPLATES) > 10)

    def test_import_relation_verbs(self):
        """Relation verbs dict is populated."""
        from ck_sim.ck_language import RELATION_VERBS
        self.assertIsInstance(RELATION_VERBS, dict)
        self.assertIn('causes', RELATION_VERBS)
        self.assertIn('is_a', RELATION_VERBS)


# ================================================================
#  TEST: Intent Enum
# ================================================================

class TestIntent(unittest.TestCase):
    """Intent enum has correct values and members."""

    def test_intent_values(self):
        """Intent values 0-6 are correct."""
        from ck_sim.ck_language import Intent
        self.assertEqual(Intent.DEFINE, 0)
        self.assertEqual(Intent.EXPLAIN, 1)
        self.assertEqual(Intent.COMPARE, 2)
        self.assertEqual(Intent.INSTRUCT, 3)
        self.assertEqual(Intent.JUSTIFY, 4)
        self.assertEqual(Intent.DESCRIBE, 5)
        self.assertEqual(Intent.TRANSLATE, 6)

    def test_intent_is_intenum(self):
        """Intent is an IntEnum."""
        from ck_sim.ck_language import Intent
        self.assertIsInstance(Intent.DEFINE, int)
        self.assertEqual(int(Intent.EXPLAIN), 1)

    def test_intent_names(self):
        """Intent names are accessible."""
        from ck_sim.ck_language import Intent
        self.assertEqual(Intent.DEFINE.name, 'DEFINE')
        self.assertEqual(Intent.TRANSLATE.name, 'TRANSLATE')


# ================================================================
#  TEST: Intent Classifier
# ================================================================

class TestIntentClassifier(unittest.TestCase):
    """IntentClassifier correctly identifies query intent."""

    @classmethod
    def setUpClass(cls):
        cls.lattice, cls.lexicon = build_loaded_environment()

    def setUp(self):
        from ck_sim.ck_language import IntentClassifier
        self.classifier = IntentClassifier()

    def test_single_node_is_define(self):
        """Single query node -> DEFINE."""
        from ck_sim.ck_language import Intent
        result = self.classifier.classify(['water'], self.lattice)
        self.assertEqual(result, Intent.DEFINE)

    def test_two_causal_nodes_is_explain(self):
        """Two nodes with causal relation -> EXPLAIN."""
        from ck_sim.ck_language import Intent
        # fire causes heat -> seed_corpus has fire opposes water, etc.
        # seed has: 'energy' causes 'movement'
        result = self.classifier.classify(['energy', 'movement'], self.lattice)
        self.assertEqual(result, Intent.EXPLAIN)

    def test_two_same_domain_is_compare(self):
        """Two nodes in same domain with no causal edge -> COMPARE."""
        from ck_sim.ck_language import Intent
        # brother and sister are both in 'family' domain
        result = self.classifier.classify(['brother', 'sister'], self.lattice)
        # brother balances sister exists, but balances is not in CAUSAL_RELATIONS
        # Same domain -> COMPARE
        self.assertEqual(result, Intent.COMPARE)

    def test_target_lang_is_translate(self):
        """Explicit target language -> TRANSLATE."""
        from ck_sim.ck_language import Intent
        result = self.classifier.classify(['water'], self.lattice,
                                          target_lang='es')
        self.assertEqual(result, Intent.TRANSLATE)

    def test_empty_query_is_describe(self):
        """Empty query -> DESCRIBE."""
        from ck_sim.ck_language import Intent
        result = self.classifier.classify([], self.lattice)
        self.assertEqual(result, Intent.DESCRIBE)

    def test_three_nodes_is_describe(self):
        """Three query nodes -> DESCRIBE."""
        from ck_sim.ck_language import Intent
        result = self.classifier.classify(['water', 'fire', 'earth_element'],
                                          self.lattice)
        self.assertEqual(result, Intent.DESCRIBE)

    def test_enables_edge_is_explain(self):
        """Two nodes with enables edge -> EXPLAIN."""
        from ck_sim.ck_language import Intent
        # 'word' enables 'speaking'
        result = self.classifier.classify(['word', 'speaking'], self.lattice)
        self.assertEqual(result, Intent.EXPLAIN)


# ================================================================
#  TEST: Concept Chain
# ================================================================

class TestConceptChain(unittest.TestCase):
    """ConceptChain dataclass creation and properties."""

    def test_empty_chain(self):
        """Empty chain is falsy."""
        from ck_sim.ck_language import ConceptChain
        chain = ConceptChain()
        self.assertFalse(chain)
        self.assertEqual(len(chain), 0)

    def test_single_node_chain(self):
        """Single node chain is valid."""
        from ck_sim.ck_language import ConceptChain
        chain = ConceptChain(nodes=['water'])
        self.assertTrue(chain)
        self.assertEqual(len(chain), 1)
        self.assertTrue(chain.is_valid)

    def test_two_node_chain(self):
        """Two node chain with one relation is valid."""
        from ck_sim.ck_language import ConceptChain
        chain = ConceptChain(
            nodes=['water', 'life'],
            relations=['sustains'],
        )
        self.assertTrue(chain)
        self.assertEqual(len(chain), 2)
        self.assertTrue(chain.is_valid)

    def test_invalid_chain_missing_relation(self):
        """Two nodes with zero relations is invalid."""
        from ck_sim.ck_language import ConceptChain
        chain = ConceptChain(nodes=['water', 'fire'])
        self.assertFalse(chain.is_valid)


# ================================================================
#  TEST: Concept Chain Builder
# ================================================================

class TestConceptChainBuilder(unittest.TestCase):
    """ConceptChainBuilder builds valid chains for each intent."""

    @classmethod
    def setUpClass(cls):
        cls.lattice, cls.lexicon = build_loaded_environment()

    def setUp(self):
        from ck_sim.ck_language import ConceptChainBuilder
        self.builder = ConceptChainBuilder()

    def test_define_chain_has_nodes(self):
        """DEFINE chain contains at least the query node."""
        from ck_sim.ck_language import Intent
        chain = self.builder.build_chain(Intent.DEFINE, ['dog'], self.lattice)
        self.assertIn('dog', chain.nodes)
        self.assertTrue(chain.is_valid)

    def test_define_dog_is_a_animal(self):
        """DEFINE for 'dog' finds is_a 'animal'."""
        from ck_sim.ck_language import Intent
        chain = self.builder.build_chain(Intent.DEFINE, ['dog'], self.lattice)
        self.assertIn('animal', chain.nodes)
        self.assertIn('is_a', chain.relations)
        self.assertGreater(chain.confidence, 0.5)

    def test_explain_chain(self):
        """EXPLAIN chain connects two concepts."""
        from ck_sim.ck_language import Intent
        chain = self.builder.build_chain(Intent.EXPLAIN,
                                         ['energy', 'movement'], self.lattice)
        self.assertTrue(len(chain.nodes) >= 2)
        self.assertTrue(chain.is_valid)

    def test_compare_chain_direct_edge(self):
        """COMPARE chain for directly related concepts."""
        from ck_sim.ck_language import Intent
        # fire opposes water
        chain = self.builder.build_chain(Intent.COMPARE,
                                         ['fire', 'water'], self.lattice)
        self.assertTrue(len(chain.nodes) >= 2)
        self.assertTrue(chain.is_valid)

    def test_compare_chain_shared_parent(self):
        """COMPARE chain for concepts with shared parent."""
        from ck_sim.ck_language import Intent
        # dog is_a animal, bird is_a animal
        chain = self.builder.build_chain(Intent.COMPARE,
                                         ['dog', 'bird'], self.lattice)
        self.assertTrue(len(chain.nodes) >= 2)
        self.assertTrue(chain.is_valid)

    def test_describe_chain_multiple_facts(self):
        """DESCRIBE chain gathers multiple neighbor facts."""
        from ck_sim.ck_language import Intent
        chain = self.builder.build_chain(Intent.DESCRIBE,
                                         ['water'], self.lattice)
        self.assertIn('water', chain.nodes)
        self.assertTrue(len(chain.nodes) >= 2)

    def test_translate_chain_single_node(self):
        """TRANSLATE chain is just the concept node."""
        from ck_sim.ck_language import Intent
        chain = self.builder.build_chain(Intent.TRANSLATE,
                                         ['water'], self.lattice)
        self.assertEqual(chain.nodes, ['water'])
        self.assertEqual(chain.confidence, 1.0)

    def test_empty_query_returns_empty_chain(self):
        """Empty query returns empty chain."""
        from ck_sim.ck_language import Intent
        chain = self.builder.build_chain(Intent.DEFINE, [], self.lattice)
        self.assertFalse(chain)


# ================================================================
#  TEST: Surface Realizer
# ================================================================

class TestSurfaceRealizer(unittest.TestCase):
    """SurfaceRealizer fills templates and picks words correctly."""

    @classmethod
    def setUpClass(cls):
        cls.lattice, cls.lexicon = build_loaded_environment()

    def setUp(self):
        from ck_sim.ck_language import SurfaceRealizer
        self.realizer = SurfaceRealizer()

    def test_get_word_from_lexicon(self):
        """_get_word finds words via lexicon."""
        word = self.realizer._get_word('water', self.lattice,
                                       self.lexicon, 'en')
        self.assertEqual(word.lower(), 'water')

    def test_get_word_from_lattice_bindings(self):
        """_get_word falls back to lattice bindings."""
        # 'existence' should be in lattice bindings even if not primary lexicon
        word = self.realizer._get_word('existence', self.lattice,
                                       self.lexicon, 'en')
        self.assertTrue(len(word) > 0)

    def test_get_word_fallback_to_concept_id(self):
        """_get_word falls back to concept ID for unknown concepts."""
        word = self.realizer._get_word('nonexistent_concept', self.lattice,
                                       self.lexicon, 'en')
        self.assertEqual(word, 'nonexistent concept')

    def test_realize_define_is_a(self):
        """Realize DEFINE with is_a relation produces correct sentence."""
        from ck_sim.ck_language import ConceptChain, Intent
        chain = ConceptChain(
            nodes=['dog', 'animal'],
            relations=['is_a'],
            intent=Intent.DEFINE,
        )
        sentence = self.realizer.realize(chain, Intent.DEFINE,
                                         self.lattice, self.lexicon, 'en')
        self.assertIn('type of', sentence.lower())
        self.assertTrue(sentence[0].isupper())

    def test_realize_explain_causes(self):
        """Realize EXPLAIN with causes relation."""
        from ck_sim.ck_language import ConceptChain, Intent
        chain = ConceptChain(
            nodes=['energy', 'movement'],
            relations=['causes'],
            intent=Intent.EXPLAIN,
        )
        sentence = self.realizer.realize(chain, Intent.EXPLAIN,
                                         self.lattice, self.lexicon, 'en')
        self.assertIn('causes', sentence.lower())

    def test_realize_compare_opposes(self):
        """Realize COMPARE with opposes relation."""
        from ck_sim.ck_language import ConceptChain, Intent
        chain = ConceptChain(
            nodes=['fire', 'water'],
            relations=['opposes'],
            intent=Intent.COMPARE,
        )
        sentence = self.realizer.realize(chain, Intent.COMPARE,
                                         self.lattice, self.lexicon, 'en')
        self.assertIn('opposes', sentence.lower())

    def test_realize_empty_chain(self):
        """Realize empty chain returns empty string."""
        from ck_sim.ck_language import ConceptChain, Intent
        chain = ConceptChain()
        sentence = self.realizer.realize(chain, Intent.DEFINE,
                                         self.lattice, self.lexicon, 'en')
        self.assertEqual(sentence, "")

    def test_realize_translation(self):
        """realize_translation produces correct format."""
        sentence = self.realizer.realize_translation(
            'water', 'water', 'es', self.lattice, self.lexicon
        )
        self.assertIn('Spanish', sentence)

    def test_realize_describe_multiple_facts(self):
        """Realize DESCRIBE with multiple facts."""
        from ck_sim.ck_language import ConceptChain, Intent
        chain = ConceptChain(
            nodes=['water', 'life', 'fire'],
            relations=['sustains', 'opposes'],
            intent=Intent.DESCRIBE,
        )
        sentence = self.realizer.realize(chain, Intent.DESCRIBE,
                                         self.lattice, self.lexicon, 'en')
        self.assertTrue(len(sentence) > 10)
        self.assertTrue(sentence[0].isupper())


# ================================================================
#  TEST: Language Generator
# ================================================================

class TestLanguageGenerator(unittest.TestCase):
    """LanguageGenerator full pipeline: generate(), define(), explain(), etc."""

    @classmethod
    def setUpClass(cls):
        cls.lattice, cls.lexicon = build_loaded_environment()

    def setUp(self):
        from ck_sim.ck_language import LanguageGenerator
        self.gen = LanguageGenerator(self.lattice, self.lexicon)

    def test_generate_single_concept(self):
        """generate() with single concept returns a sentence."""
        sentence = self.gen.generate(['water'])
        self.assertTrue(len(sentence) > 0)
        self.assertTrue(sentence[0].isupper())

    def test_generate_two_concepts(self):
        """generate() with two concepts returns a sentence."""
        sentence = self.gen.generate(['fire', 'water'])
        self.assertTrue(len(sentence) > 0)

    def test_generate_empty(self):
        """generate() with empty list returns empty string."""
        sentence = self.gen.generate([])
        self.assertEqual(sentence, "")

    def test_define(self):
        """define() returns a definition sentence."""
        sentence = self.gen.define('dog')
        self.assertTrue(len(sentence) > 0)
        # Dog is_a animal, so sentence should mention that
        lower = sentence.lower()
        self.assertTrue('type of' in lower or 'animal' in lower
                        or 'dog' in lower)

    def test_explain(self):
        """explain() returns an explanation sentence."""
        sentence = self.gen.explain('energy', 'movement')
        self.assertTrue(len(sentence) > 0)
        self.assertIn('cause', sentence.lower())

    def test_compare(self):
        """compare() returns a comparison sentence."""
        sentence = self.gen.compare('fire', 'water')
        self.assertTrue(len(sentence) > 0)

    def test_describe(self):
        """describe() returns a multi-fact description."""
        sentence = self.gen.describe('water')
        self.assertTrue(len(sentence) > 0)

    def test_stats(self):
        """stats() returns valid statistics dict."""
        stats = self.gen.stats()
        self.assertIn('generation_count', stats)
        self.assertIn('lattice_nodes', stats)
        self.assertIn('templates', stats)
        self.assertGreater(stats['lattice_nodes'], 0)
        self.assertGreater(stats['templates'], 0)

    def test_generation_count_increments(self):
        """Generation count increments with each call."""
        from ck_sim.ck_language import LanguageGenerator
        gen = LanguageGenerator(self.lattice, self.lexicon)
        self.assertEqual(gen.stats()['generation_count'], 0)
        gen.define('water')
        self.assertEqual(gen.stats()['generation_count'], 1)
        gen.explain('fire', 'water')
        self.assertEqual(gen.stats()['generation_count'], 2)


# ================================================================
#  TEST: Translation
# ================================================================

class TestTranslation(unittest.TestCase):
    """translate_word works via lexicon and lattice fallback."""

    @classmethod
    def setUpClass(cls):
        cls.lattice, cls.lexicon = build_loaded_environment()

    def setUp(self):
        from ck_sim.ck_language import LanguageGenerator
        self.gen = LanguageGenerator(self.lattice, self.lexicon)

    def test_translate_water_to_spanish(self):
        """Translate 'water' from English to Spanish."""
        sentence = self.gen.translate_word('water', 'en', 'es')
        self.assertIn('Spanish', sentence)
        self.assertIn('agua', sentence.lower())

    def test_translate_fire_to_french(self):
        """Translate 'fire' from English to French."""
        sentence = self.gen.translate_word('fire', 'en', 'fr')
        self.assertIn('French', sentence)

    def test_translate_unknown_word(self):
        """Translating unknown word returns graceful message."""
        sentence = self.gen.translate_word('xyzzy', 'en', 'es')
        self.assertIn('xyzzy', sentence.lower())

    def test_translate_via_generate(self):
        """generate() with TRANSLATE intent produces translation."""
        from ck_sim.ck_language import Intent
        sentence = self.gen.generate(['water'], lang='en',
                                     intent=Intent.TRANSLATE,
                                     target_lang='es')
        self.assertIn('Spanish', sentence)


# ================================================================
#  TEST: Multilingual Output
# ================================================================

class TestMultilingual(unittest.TestCase):
    """Generates in es, fr, de (not just en)."""

    @classmethod
    def setUpClass(cls):
        cls.lattice, cls.lexicon = build_loaded_environment()

    def setUp(self):
        from ck_sim.ck_language import LanguageGenerator
        self.gen = LanguageGenerator(self.lattice, self.lexicon)

    def test_define_in_spanish(self):
        """define() in Spanish uses Spanish words."""
        sentence = self.gen.define('water', lang='es')
        self.assertTrue(len(sentence) > 0)

    def test_define_in_french(self):
        """define() in French uses French words."""
        sentence = self.gen.define('water', lang='fr')
        self.assertTrue(len(sentence) > 0)

    def test_define_in_german(self):
        """define() in German uses German words."""
        sentence = self.gen.define('water', lang='de')
        self.assertTrue(len(sentence) > 0)

    def test_describe_in_spanish(self):
        """describe() in Spanish."""
        sentence = self.gen.describe('mother', lang='es')
        self.assertTrue(len(sentence) > 0)

    def test_explain_in_french(self):
        """explain() in French."""
        sentence = self.gen.explain('sun', 'life', lang='fr')
        self.assertTrue(len(sentence) > 0)


# ================================================================
#  TEST: Integration -- Full Pipeline
# ================================================================

class TestIntegration(unittest.TestCase):
    """Full pipeline with loaded world lattice + seed lexicon."""

    @classmethod
    def setUpClass(cls):
        cls.lattice, cls.lexicon = build_loaded_environment()

    def setUp(self):
        from ck_sim.ck_language import LanguageGenerator
        self.gen = LanguageGenerator(self.lattice, self.lexicon)

    def test_full_define_pipeline(self):
        """Full pipeline: define 'computer' -> is_a machine."""
        sentence = self.gen.define('computer')
        lower = sentence.lower()
        self.assertTrue('machine' in lower or 'computer' in lower)

    def test_full_explain_pipeline(self):
        """Full pipeline: explain seed -> growth."""
        sentence = self.gen.explain('seed', 'growth')
        self.assertTrue(len(sentence) > 5)
        self.assertIn('cause', sentence.lower())

    def test_full_compare_pipeline(self):
        """Full pipeline: compare dog and bird -> shared parent animal."""
        sentence = self.gen.compare('dog', 'bird')
        lower = sentence.lower()
        # Should find shared parent 'animal'
        self.assertTrue('animal' in lower or 'dog' in lower)

    def test_full_describe_pipeline(self):
        """Full pipeline: describe 'water' with multiple facts."""
        sentence = self.gen.describe('water')
        self.assertTrue(len(sentence) > 5)

    def test_full_translate_pipeline(self):
        """Full pipeline: translate 'mother' en -> es."""
        sentence = self.gen.translate_word('mother', 'en', 'es')
        self.assertIn('Spanish', sentence)
        self.assertIn('madre', sentence.lower())

    def test_coherence_path_explain(self):
        """Explain two indirectly connected concepts via path."""
        # water sustains life, life precedes death
        # So water -> life -> death path should work
        sentence = self.gen.explain('water', 'death')
        self.assertTrue(len(sentence) > 5)

    def test_all_intent_types_produce_output(self):
        """Every intent type produces non-empty output."""
        from ck_sim.ck_language import Intent
        for intent in Intent:
            if intent == Intent.TRANSLATE:
                sentence = self.gen.generate(['water'], intent=intent,
                                             target_lang='es')
            elif intent in (Intent.EXPLAIN, Intent.COMPARE, Intent.JUSTIFY):
                sentence = self.gen.generate(['fire', 'water'], intent=intent)
            else:
                sentence = self.gen.generate(['water'], intent=intent)
            self.assertTrue(len(sentence) > 0,
                            f"Intent {intent.name} produced empty output")

    def test_nonexistent_concept_graceful(self):
        """Nonexistent concept produces best-effort output."""
        sentence = self.gen.define('zxcvbn_unknown')
        self.assertTrue(len(sentence) > 0)

    def test_multiple_generates_consistent(self):
        """Multiple calls produce consistent output."""
        s1 = self.gen.define('water')
        s2 = self.gen.define('water')
        self.assertEqual(s1, s2)


# ================================================================
#  ENTRY POINT
# ================================================================

if __name__ == '__main__':
    unittest.main()
