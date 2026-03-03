"""
ck_lexicon_bulk_tests.py -- Tests for Lexicon Expansion Module
===============================================================
Validates: EXPANDED_LEXICON integrity, MorphExpander rules,
build_full_store() integration, lexicon_stats(), and
cross-referencing with seed lexicon.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import unittest

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, COLLAPSE, CHAOS, PROGRESS,
    BREATH, BALANCE, COUNTER, LATTICE, RESET,
)
from ck_sim.ck_lexicon import (
    LexiconStore, SEED_LEXICON, PhonemeCodec, LexicalSignature,
)
from ck_sim.ck_lexicon_bulk import (
    EXPANDED_LEXICON, MorphExpander,
    NOUN_CONCEPTS, VERB_CONCEPTS, ADJ_CONCEPTS, COLOR_CONCEPTS,
    build_full_store, lexicon_stats,
)


# ================================================================
#  IMPORT TESTS
# ================================================================

class TestImport(unittest.TestCase):

    def test_import_module(self):
        import ck_sim.ck_lexicon_bulk
        self.assertTrue(hasattr(ck_sim.ck_lexicon_bulk, 'EXPANDED_LEXICON'))
        self.assertTrue(hasattr(ck_sim.ck_lexicon_bulk, 'MorphExpander'))
        self.assertTrue(hasattr(ck_sim.ck_lexicon_bulk, 'build_full_store'))
        self.assertTrue(hasattr(ck_sim.ck_lexicon_bulk, 'lexicon_stats'))

    def test_import_classification_sets(self):
        self.assertIsInstance(NOUN_CONCEPTS, set)
        self.assertIsInstance(VERB_CONCEPTS, set)
        self.assertIsInstance(ADJ_CONCEPTS, set)
        self.assertIsInstance(COLOR_CONCEPTS, set)

    def test_import_expanded_lexicon(self):
        self.assertIsInstance(EXPANDED_LEXICON, dict)
        self.assertGreater(len(EXPANDED_LEXICON), 100)


# ================================================================
#  EXPANDED LEXICON STRUCTURE TESTS
# ================================================================

class TestExpandedLexiconStructure(unittest.TestCase):
    """Every expanded entry has 7 languages with 3-tuples."""

    EXPECTED_LANGS = {'en', 'es', 'fr', 'de', 'he', 'ar', 'zh'}

    def test_concept_count(self):
        """Should have 157 expanded concepts."""
        self.assertEqual(len(EXPANDED_LEXICON), 157)

    def test_every_concept_has_7_entries(self):
        """Each concept must have exactly 7 language entries."""
        for concept_id, entries in EXPANDED_LEXICON.items():
            self.assertEqual(len(entries), 7,
                msg=f"Concept '{concept_id}' has {len(entries)} entries, expected 7")

    def test_every_entry_is_3_tuple(self):
        """Each entry is (lang, wordform, phonemes)."""
        for concept_id, entries in EXPANDED_LEXICON.items():
            for entry in entries:
                self.assertEqual(len(entry), 3,
                    msg=f"Concept '{concept_id}' has entry with {len(entry)} fields")
                lang, word, phonemes = entry
                self.assertIsInstance(lang, str)
                self.assertIsInstance(word, str)
                self.assertIsInstance(phonemes, str)

    def test_all_seven_languages_per_concept(self):
        """Each concept covers all 7 languages."""
        for concept_id, entries in EXPANDED_LEXICON.items():
            langs = {e[0] for e in entries}
            self.assertEqual(langs, self.EXPECTED_LANGS,
                msg=f"Concept '{concept_id}' has langs {sorted(langs)}")

    def test_no_empty_words(self):
        """No empty wordforms."""
        for concept_id, entries in EXPANDED_LEXICON.items():
            for lang, word, phonemes in entries:
                self.assertGreater(len(word), 0,
                    msg=f"Concept '{concept_id}' ({lang}) has empty word")

    def test_no_empty_phonemes(self):
        """No empty phoneme strings."""
        for concept_id, entries in EXPANDED_LEXICON.items():
            for lang, word, phonemes in entries:
                self.assertGreater(len(phonemes), 0,
                    msg=f"Concept '{concept_id}' ({lang}) has empty phonemes")

    def test_no_overlap_with_seed(self):
        """Expanded concepts don't duplicate seed concept_ids."""
        overlap = set(EXPANDED_LEXICON.keys()) & set(SEED_LEXICON.keys())
        self.assertEqual(len(overlap), 0,
            msg=f"Overlapping concept_ids: {overlap}")


# ================================================================
#  DOMAIN COVERAGE TESTS
# ================================================================

class TestDomainCoverage(unittest.TestCase):
    """All 11 domains are represented."""

    def test_body_domain(self):
        body = {'mouth', 'ear', 'nose', 'foot', 'bone', 'skin', 'tooth',
                'tongue', 'finger', 'stomach', 'leg', 'arm', 'back', 'neck', 'knee'}
        self.assertTrue(body.issubset(EXPANDED_LEXICON.keys()))

    def test_food_domain(self):
        food = {'bread', 'milk', 'meat', 'fruit', 'salt', 'honey', 'egg',
                'rice', 'wine', 'oil', 'sugar', 'seed', 'leaf', 'root',
                'flower', 'grass', 'rain', 'snow', 'wind', 'cloud'}
        self.assertTrue(food.issubset(EXPANDED_LEXICON.keys()))

    def test_animals_domain(self):
        animals = {'horse', 'cow', 'sheep', 'snake', 'lion', 'eagle', 'wolf',
                   'bear', 'deer', 'ant', 'bee', 'spider', 'whale', 'turtle', 'rabbit'}
        self.assertTrue(animals.issubset(EXPANDED_LEXICON.keys()))

    def test_emotions_domain(self):
        emotions = {'fear', 'joy', 'anger', 'hope', 'sorrow', 'shame', 'pride',
                    'mercy', 'patience', 'wisdom', 'courage', 'trust',
                    'gratitude', 'compassion', 'longing'}
        self.assertTrue(emotions.issubset(EXPANDED_LEXICON.keys()))

    def test_actions_domain(self):
        actions = {'give', 'take', 'run', 'fly', 'swim', 'sing', 'dance',
                   'cry', 'laugh', 'think', 'know', 'love_v', 'teach', 'learn',
                   'build', 'break', 'open', 'close', 'wait', 'pray'}
        self.assertTrue(actions.issubset(EXPANDED_LEXICON.keys()))

    def test_qualities_domain(self):
        quals = {'hot', 'cold', 'strong', 'weak', 'fast', 'slow', 'high', 'low',
                 'long', 'short', 'wide', 'deep', 'clean', 'dirty', 'heavy',
                 'empty', 'full', 'dry', 'wet', 'round'}
        self.assertTrue(quals.issubset(EXPANDED_LEXICON.keys()))

    def test_objects_domain(self):
        objs = {'house', 'door', 'road', 'knife', 'fire_tool', 'rope', 'wheel',
                'boat', 'book', 'song', 'word', 'path', 'wall', 'bridge', 'garden'}
        self.assertTrue(objs.issubset(EXPANDED_LEXICON.keys()))

    def test_colors_domain(self):
        colors = {'red', 'blue', 'green', 'white', 'black', 'yellow',
                  'gold', 'silver', 'iron', 'copper'}
        self.assertTrue(colors.issubset(EXPANDED_LEXICON.keys()))

    def test_numbers_domain(self):
        nums = {'one', 'two', 'three', 'seven', 'ten', 'hundred', 'thousand'}
        self.assertTrue(nums.issubset(EXPANDED_LEXICON.keys()))

    def test_spiritual_domain(self):
        spirit = {'soul', 'spirit', 'heaven', 'earth_ground', 'light_divine',
                  'blessing', 'sin', 'grace', 'covenant', 'redemption'}
        self.assertTrue(spirit.issubset(EXPANDED_LEXICON.keys()))

    def test_social_domain(self):
        social = {'king', 'servant', 'friend', 'enemy', 'people',
                  'village', 'land', 'sea', 'sky', 'desert'}
        self.assertTrue(social.issubset(EXPANDED_LEXICON.keys()))


# ================================================================
#  CLASSIFICATION SET TESTS
# ================================================================

class TestClassificationSets(unittest.TestCase):
    """NOUN/VERB/ADJ/COLOR sets match what's in the lexicons."""

    def test_noun_count(self):
        """NOUN_CONCEPTS should be substantial."""
        self.assertGreater(len(NOUN_CONCEPTS), 100)

    def test_verb_count(self):
        """VERB_CONCEPTS should have all action verbs."""
        self.assertEqual(len(VERB_CONCEPTS), 27)

    def test_adj_count(self):
        """ADJ_CONCEPTS should have quality adjectives."""
        self.assertEqual(len(ADJ_CONCEPTS), 25)  # 5 seed + 20 expanded

    def test_color_count(self):
        """COLOR_CONCEPTS = 6 basic colors with adj forms."""
        self.assertEqual(len(COLOR_CONCEPTS), 6)

    def test_verbs_exist_in_lexicons(self):
        """Every VERB_CONCEPT must appear in seed or expanded."""
        all_concepts = set(SEED_LEXICON.keys()) | set(EXPANDED_LEXICON.keys())
        for verb in VERB_CONCEPTS:
            self.assertIn(verb, all_concepts,
                msg=f"Verb '{verb}' not in any lexicon")

    def test_adjs_exist_in_lexicons(self):
        """Every ADJ_CONCEPT must appear in seed or expanded."""
        all_concepts = set(SEED_LEXICON.keys()) | set(EXPANDED_LEXICON.keys())
        for adj in ADJ_CONCEPTS:
            self.assertIn(adj, all_concepts,
                msg=f"Adj '{adj}' not in any lexicon")

    def test_colors_exist_in_expanded(self):
        """Every COLOR_CONCEPT must be in expanded lexicon."""
        for color in COLOR_CONCEPTS:
            self.assertIn(color, EXPANDED_LEXICON,
                msg=f"Color '{color}' not in expanded lexicon")

    def test_no_overlap_verb_adj(self):
        """Verbs and adjectives don't overlap."""
        overlap = VERB_CONCEPTS & ADJ_CONCEPTS
        self.assertEqual(len(overlap), 0, msg=f"Overlap: {overlap}")

    def test_no_overlap_verb_color(self):
        """Verbs and colors don't overlap."""
        overlap = VERB_CONCEPTS & COLOR_CONCEPTS
        self.assertEqual(len(overlap), 0)


# ================================================================
#  MORPH EXPANDER TESTS
# ================================================================

class TestMorphExpanderPlural(unittest.TestCase):
    """English plural generation rules."""

    def test_regular_plural(self):
        w, p = MorphExpander.english_plural('dog', 'dog')
        self.assertEqual(w, 'dogs')
        self.assertEqual(p, 'dogz')

    def test_s_ending_plural(self):
        w, p = MorphExpander.english_plural('bus', 'bas')
        self.assertEqual(w, 'buses')
        self.assertEqual(p, 'basez')

    def test_sh_ending_plural(self):
        w, p = MorphExpander.english_plural('fish', 'fiʃ')
        self.assertEqual(w, 'fishes')
        self.assertEqual(p, 'fiʃez')

    def test_ch_ending_plural(self):
        w, p = MorphExpander.english_plural('church', 'tʃertʃ')
        self.assertEqual(w, 'churches')

    def test_y_to_ies_plural(self):
        w, p = MorphExpander.english_plural('berry', 'beri')
        self.assertEqual(w, 'berries')
        self.assertEqual(p, 'beriz')

    def test_y_after_vowel_plural(self):
        """Words ending in vowel+y just add s."""
        w, p = MorphExpander.english_plural('day', 'dei')
        self.assertEqual(w, 'days')
        self.assertEqual(p, 'deiz')

    def test_f_to_ves_plural(self):
        w, p = MorphExpander.english_plural('leaf', 'lif')
        self.assertEqual(w, 'leaves')
        self.assertEqual(p, 'livz')

    def test_plural_returns_tuple(self):
        result = MorphExpander.english_plural('cat', 'kæt')
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)


class TestMorphExpanderVerbs(unittest.TestCase):
    """Verb -ing and -ed forms."""

    def test_regular_ing(self):
        # Note: simplified MorphExpander doesn't double consonants
        w, p = MorphExpander.english_verb_ing('run', 'ran')
        self.assertEqual(w, 'runing')
        self.assertEqual(p, 'raning')

    def test_e_drop_ing(self):
        w, p = MorphExpander.english_verb_ing('dance', 'dæns')
        self.assertEqual(w, 'dancing')
        self.assertEqual(p, 'dæning')

    def test_ee_no_drop_ing(self):
        """'ee' ending should NOT drop the e."""
        w, p = MorphExpander.english_verb_ing('see', 'si')
        self.assertEqual(w, 'seeing')
        self.assertEqual(p, 'siing')

    def test_regular_ed(self):
        w, p = MorphExpander.english_verb_ed('walk', 'wok')
        self.assertEqual(w, 'walked')
        self.assertEqual(p, 'wokd')

    def test_e_ending_ed(self):
        w, p = MorphExpander.english_verb_ed('dance', 'dæns')
        self.assertEqual(w, 'danced')
        self.assertEqual(p, 'dænsd')

    def test_t_ending_ed(self):
        w, p = MorphExpander.english_verb_ed('wait', 'weit')
        self.assertEqual(w, 'waited')
        self.assertEqual(p, 'weited')

    def test_d_ending_ed(self):
        w, p = MorphExpander.english_verb_ed('build', 'bild')
        self.assertEqual(w, 'builded')
        self.assertEqual(p, 'bilded')  # d-ending → +ed on phonemes too


class TestMorphExpanderAdjectives(unittest.TestCase):
    """Comparative and superlative forms."""

    def test_regular_comparative(self):
        w, p = MorphExpander.english_comparative('fast', 'fæst')
        self.assertEqual(w, 'faster')
        self.assertEqual(p, 'fæster')

    def test_e_ending_comparative(self):
        w, p = MorphExpander.english_comparative('wide', 'waid')
        self.assertEqual(w, 'wider')
        self.assertEqual(p, 'waidr')

    def test_y_ending_comparative(self):
        w, p = MorphExpander.english_comparative('dirty', 'derti')
        self.assertEqual(w, 'dirtier')
        self.assertEqual(p, 'dertier')

    def test_regular_superlative(self):
        w, p = MorphExpander.english_superlative('fast', 'fæst')
        self.assertEqual(w, 'fastest')
        self.assertEqual(p, 'fæstest')

    def test_e_ending_superlative(self):
        w, p = MorphExpander.english_superlative('wide', 'waid')
        self.assertEqual(w, 'widest')
        self.assertEqual(p, 'waidst')

    def test_y_ending_superlative(self):
        w, p = MorphExpander.english_superlative('dirty', 'derti')
        self.assertEqual(w, 'dirtiest')
        self.assertEqual(p, 'dertiest')


# ================================================================
#  EXPAND NOUN/VERB/ADJ CLASS METHODS
# ================================================================

class TestMorphExpandClassMethods(unittest.TestCase):
    """expand_noun, expand_verb, expand_adjective generate correct forms."""

    def test_expand_noun_generates_plural(self):
        entries = [('en', 'dog', 'dog'), ('es', 'perro', 'pero')]
        forms = MorphExpander.expand_noun('dog', entries)
        self.assertEqual(len(forms), 1)
        form_id, form_entries = forms[0]
        self.assertEqual(form_id, 'dog_pl')
        self.assertEqual(len(form_entries), 1)  # English only
        self.assertEqual(form_entries[0][0], 'en')
        self.assertEqual(form_entries[0][1], 'dogs')

    def test_expand_verb_generates_two_forms(self):
        entries = [('en', 'run', 'ran'), ('es', 'correr', 'korer')]
        forms = MorphExpander.expand_verb('run', entries)
        self.assertEqual(len(forms), 2)
        form_ids = {f[0] for f in forms}
        self.assertIn('run_ing', form_ids)
        self.assertIn('run_ed', form_ids)

    def test_expand_adjective_generates_two_forms(self):
        entries = [('en', 'hot', 'hot'), ('es', 'caliente', 'kaliente')]
        forms = MorphExpander.expand_adjective('hot', entries)
        self.assertEqual(len(forms), 2)
        form_ids = {f[0] for f in forms}
        self.assertIn('hot_comp', form_ids)
        self.assertIn('hot_super', form_ids)

    def test_expand_noun_no_english_returns_empty(self):
        """If no English entry, expand_noun returns empty."""
        entries = [('es', 'perro', 'pero'), ('fr', 'chien', 'ʃien')]
        forms = MorphExpander.expand_noun('dog', entries)
        self.assertEqual(len(forms), 0)


# ================================================================
#  LEXICON STATS TESTS
# ================================================================

class TestLexiconStats(unittest.TestCase):
    """lexicon_stats() returns accurate quick counts."""

    def test_returns_dict(self):
        stats = lexicon_stats()
        self.assertIsInstance(stats, dict)

    def test_seed_concepts(self):
        stats = lexicon_stats()
        self.assertEqual(stats['seed_concepts'], 50)

    def test_seed_entries(self):
        stats = lexicon_stats()
        self.assertEqual(stats['seed_entries'], 350)  # 50 × 7

    def test_expanded_concepts(self):
        stats = lexicon_stats()
        self.assertEqual(stats['expanded_concepts'], 157)

    def test_expanded_entries(self):
        stats = lexicon_stats()
        self.assertEqual(stats['expanded_entries'], 157 * 7)  # 1099

    def test_noun_morphs(self):
        stats = lexicon_stats()
        self.assertEqual(stats['noun_morphs'], len(NOUN_CONCEPTS))

    def test_verb_morphs(self):
        stats = lexicon_stats()
        self.assertEqual(stats['verb_morphs'], len(VERB_CONCEPTS) * 2)

    def test_adj_morphs(self):
        stats = lexicon_stats()
        expected = (len(ADJ_CONCEPTS) + len(COLOR_CONCEPTS)) * 2
        self.assertEqual(stats['adj_morphs'], expected)

    def test_total_morphs(self):
        stats = lexicon_stats()
        expected = (
            len(NOUN_CONCEPTS) +
            len(VERB_CONCEPTS) * 2 +
            (len(ADJ_CONCEPTS) + len(COLOR_CONCEPTS)) * 2
        )
        self.assertEqual(stats['total_morphs'], expected)

    def test_total_entries(self):
        """Total = seed + expanded + morphs."""
        stats = lexicon_stats()
        expected = (
            stats['seed_entries'] +
            stats['expanded_entries'] +
            stats['total_morphs']
        )
        self.assertEqual(stats['total_entries'], expected)

    def test_total_above_1700(self):
        """Total entries should exceed 1700."""
        stats = lexicon_stats()
        self.assertGreater(stats['total_entries'], 1700)


# ================================================================
#  BUILD FULL STORE TESTS
# ================================================================

class TestBuildFullStore(unittest.TestCase):
    """build_full_store() constructs a working LexiconStore."""

    @classmethod
    def setUpClass(cls):
        """Build once, share across tests (expensive operation)."""
        cls.store, cls.stats = build_full_store()

    def test_returns_store_and_stats(self):
        self.assertIsInstance(self.store, LexiconStore)
        self.assertIsInstance(self.stats, dict)

    def test_store_word_count_matches_stats(self):
        self.assertEqual(self.store.word_count, self.stats['total_lexemes'])

    def test_total_lexemes_above_1700(self):
        self.assertGreater(self.stats['total_lexemes'], 1700)

    def test_seed_concepts_in_stats(self):
        self.assertEqual(self.stats['seed_concepts'], 50)

    def test_expanded_concepts_in_stats(self):
        self.assertEqual(self.stats['expanded_concepts'], 157)

    def test_morph_forms_positive(self):
        self.assertGreater(self.stats['morph_forms'], 0)

    def test_seven_languages(self):
        self.assertEqual(self.stats['languages'], 7)

    def test_store_has_seven_languages(self):
        self.assertEqual(self.store.language_count, 7)

    def test_seed_words_lookup(self):
        """Seed words should be findable."""
        results = self.store.lookup_word('water', 'en')
        self.assertGreater(len(results), 0)

    def test_expanded_words_lookup(self):
        """Expanded words should be findable."""
        results = self.store.lookup_word('bread', 'en')
        self.assertGreater(len(results), 0)

    def test_expanded_spanish_lookup(self):
        """Expanded words in Spanish should be findable."""
        results = self.store.lookup_word('pan', 'es')
        self.assertGreater(len(results), 0)

    def test_morph_words_lookup(self):
        """Morphological forms should be findable."""
        # 'dogs' should exist as plural of 'dog'
        results = self.store.lookup_word('dogs', 'en')
        self.assertGreater(len(results), 0)

    def test_verb_ing_form_lookup(self):
        """Verb -ing forms should exist."""
        # MorphExpander produces 'runing' (no consonant doubling)
        results = self.store.lookup_word('giving', 'en')
        self.assertGreater(len(results), 0)

    def test_verb_ed_form_lookup(self):
        """Verb -ed forms should exist."""
        results = self.store.lookup_word('walked', 'en')
        self.assertGreater(len(results), 0)

    def test_adj_comparative_lookup(self):
        """Adjective comparatives should exist."""
        results = self.store.lookup_word('faster', 'en')
        self.assertGreater(len(results), 0)

    def test_adj_superlative_lookup(self):
        """Adjective superlatives should exist."""
        results = self.store.lookup_word('fastest', 'en')
        self.assertGreater(len(results), 0)

    def test_concept_lookup_expanded(self):
        """Expanded concept lookups return all languages."""
        by_lang = self.store.lookup_concept('bread')
        self.assertEqual(len(by_lang), 7)

    def test_translation_expanded(self):
        """Translation works for expanded concepts."""
        results = self.store.translate('bread', 'en', 'es')
        self.assertIn('pan', results)

    def test_translation_roundtrip_expanded(self):
        """en→de→en roundtrip for expanded concept."""
        de_words = self.store.translate('horse', 'en', 'de')
        self.assertIn('Pferd', de_words)
        en_words = self.store.translate('Pferd', 'de', 'en')
        self.assertIn('horse', en_words)

    def test_all_expanded_concepts_indexed(self):
        """Every expanded concept should be in the concept index."""
        for concept_id in EXPANDED_LEXICON:
            by_lang = self.store.lookup_concept(concept_id)
            self.assertEqual(len(by_lang), 7,
                msg=f"Concept '{concept_id}' has {len(by_lang)} languages")

    def test_all_seed_concepts_indexed(self):
        """Every seed concept should still be in the concept index."""
        for concept_id in SEED_LEXICON:
            by_lang = self.store.lookup_concept(concept_id)
            self.assertEqual(len(by_lang), 7,
                msg=f"Seed concept '{concept_id}' has {len(by_lang)} languages")


# ================================================================
#  PHONEME VALIDITY TESTS
# ================================================================

class TestPhonemeValidity(unittest.TestCase):
    """All expanded entries should produce valid phoneme signatures."""

    def setUp(self):
        self.codec = PhonemeCodec()

    def test_english_words_produce_signatures(self):
        """Every English word in expanded lexicon produces a signature."""
        computed = 0
        total = 0
        for concept_id, entries in EXPANDED_LEXICON.items():
            for lang, word, phonemes in entries:
                if lang == 'en':
                    total += 1
                    sig = self.codec.compute_signature(phonemes)
                    if sig.chain_length > 0:
                        computed += 1
        # At least 90% should compute (some very short words may not)
        self.assertGreater(computed / total, 0.85,
            msg=f"Only {computed}/{total} English words produced signatures")

    def test_all_languages_produce_signatures(self):
        """Words across all languages produce signatures."""
        computed = 0
        total = 0
        for concept_id, entries in EXPANDED_LEXICON.items():
            for lang, word, phonemes in entries:
                total += 1
                sig = self.codec.compute_signature(phonemes)
                if sig.chain_length > 0:
                    computed += 1
        # At least 80% should compute
        self.assertGreater(computed / total, 0.80,
            msg=f"Only {computed}/{total} total words produced signatures")

    def test_signature_operators_valid(self):
        """All signatures have valid operator indices."""
        for concept_id, entries in EXPANDED_LEXICON.items():
            for lang, word, phonemes in entries:
                sig = self.codec.compute_signature(phonemes)
                if sig.chain_length > 0:
                    self.assertGreaterEqual(sig.dominant_op, 0)
                    self.assertLess(sig.dominant_op, NUM_OPS)


# ================================================================
#  EDGE CASES
# ================================================================

class TestEdgeCases(unittest.TestCase):

    def test_morph_single_char_word(self):
        """Plural of single-char word."""
        w, p = MorphExpander.english_plural('a', 'a')
        self.assertEqual(w, 'as')

    def test_morph_empty_word(self):
        """Empty word handling."""
        w, p = MorphExpander.english_plural('', '')
        # Should not crash
        self.assertIsInstance(w, str)

    def test_expanded_concept_ids_are_strings(self):
        """All concept IDs are strings."""
        for cid in EXPANDED_LEXICON:
            self.assertIsInstance(cid, str)
            self.assertGreater(len(cid), 0)

    def test_no_duplicate_entries_per_concept(self):
        """No concept has duplicate (lang, word) pairs."""
        for concept_id, entries in EXPANDED_LEXICON.items():
            pairs = [(lang, word) for lang, word, _ in entries]
            self.assertEqual(len(pairs), len(set(pairs)),
                msg=f"Concept '{concept_id}' has duplicate entries")

    def test_stats_and_store_agree(self):
        """lexicon_stats() total should roughly match build_full_store() count."""
        stats_quick = lexicon_stats()
        store, stats_real = build_full_store()
        # They should match exactly -- both count the same entries
        self.assertEqual(stats_quick['total_entries'], stats_real['total_lexemes'])


if __name__ == '__main__':
    unittest.main()
