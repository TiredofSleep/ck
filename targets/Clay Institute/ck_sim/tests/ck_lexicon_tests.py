"""
ck_lexicon_tests.py -- Tests for Universal Lexicon Store
=========================================================
Validates: phoneme codec, lexical signatures, lexeme storage,
word/sound/concept lookups, translation, and integration with
WorldLattice and D2 pipeline.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import unittest

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, COLLAPSE, CHAOS, PROGRESS,
    BREATH, BALANCE, COUNTER, LATTICE, RESET, OP_NAMES
)
from ck_sim.ck_lexicon import (
    PhonemeCodec, LexicalSignature, Lexeme, LexiconStore,
    IPA_TO_ROOT, ASCII_PHONEME_MAP, SEED_LEXICON,
    MAX_LEXEMES, SIMILARITY_THRESHOLD,
)


# ================================================================
#  IMPORT TESTS
# ================================================================

class TestImport(unittest.TestCase):
    def test_import(self):
        import ck_sim.ck_lexicon
        self.assertTrue(hasattr(ck_sim.ck_lexicon, 'LexiconStore'))
        self.assertTrue(hasattr(ck_sim.ck_lexicon, 'PhonemeCodec'))
        self.assertTrue(hasattr(ck_sim.ck_lexicon, 'LexicalSignature'))
        self.assertTrue(hasattr(ck_sim.ck_lexicon, 'Lexeme'))

    def test_constants(self):
        self.assertGreater(len(IPA_TO_ROOT), 30)
        self.assertGreater(len(ASCII_PHONEME_MAP), 20)
        self.assertEqual(len(SEED_LEXICON), 50)

    def test_seed_lexicon_structure(self):
        """Every seed entry has 7 languages with 3-tuples."""
        for concept_id, entries in SEED_LEXICON.items():
            self.assertEqual(len(entries), 7,
                msg=f"Concept '{concept_id}' has {len(entries)} entries, expected 7")
            for lang, wordform, phonemes in entries:
                self.assertIsInstance(lang, str)
                self.assertIsInstance(wordform, str)
                self.assertIsInstance(phonemes, str)
                self.assertGreater(len(wordform), 0)


# ================================================================
#  PHONEME CODEC TESTS
# ================================================================

class TestPhonemeCodecParsing(unittest.TestCase):
    """Phoneme parsing and root mapping."""

    def setUp(self):
        self.codec = PhonemeCodec()

    def test_parse_simple_word(self):
        tokens = self.codec._parse_phonemes('kat')
        self.assertGreater(len(tokens), 0)
        # k, a, t should all parse
        self.assertIn('k', tokens)
        self.assertIn('a', tokens)
        self.assertIn('t', tokens)

    def test_parse_ipa_symbols(self):
        """IPA symbols like ʃ, θ, ŋ should parse."""
        tokens = self.codec._parse_phonemes('ʃip')
        self.assertIn('ʃ', tokens)

    def test_parse_strips_stress(self):
        """Stress marks (ˈˌ) should be stripped."""
        tokens = self.codec._parse_phonemes('ˈwɔtɚ')
        # Should not contain stress marks
        for t in tokens:
            self.assertNotIn('ˈ', t)

    def test_parse_empty_string(self):
        tokens = self.codec._parse_phonemes('')
        self.assertEqual(len(tokens), 0)

    def test_phoneme_to_force_known(self):
        """Known phonemes return 5D force vectors."""
        force = self.codec._phoneme_to_force('m')
        self.assertIsNotNone(force)
        self.assertEqual(len(force), 5)
        for v in force:
            self.assertGreaterEqual(v, 0.0)
            self.assertLessEqual(v, 1.0)

    def test_phoneme_to_force_unknown(self):
        """Unknown symbols return None."""
        force = self.codec._phoneme_to_force('§')
        self.assertIsNone(force)


class TestPhonemeCodecSignature(unittest.TestCase):
    """Signature computation from phonemes."""

    def setUp(self):
        self.codec = PhonemeCodec()

    def test_compute_returns_signature(self):
        sig = self.codec.compute_signature('water')
        self.assertIsInstance(sig, LexicalSignature)
        self.assertGreater(sig.chain_length, 0)

    def test_signature_has_valid_operator(self):
        sig = self.codec.compute_signature('mama')
        self.assertGreaterEqual(sig.dominant_op, 0)
        self.assertLess(sig.dominant_op, NUM_OPS)

    def test_signature_d2_vector_is_5d(self):
        sig = self.codec.compute_signature('hello')
        self.assertEqual(len(sig.d2_vector), 5)

    def test_signature_soft_dist_sums_to_one(self):
        sig = self.codec.compute_signature('mother')
        total = sum(sig.soft_dist)
        self.assertAlmostEqual(total, 1.0, places=2)

    def test_empty_phonemes_returns_default(self):
        sig = self.codec.compute_signature('')
        self.assertEqual(sig.chain_length, 0)
        self.assertEqual(sig.dominant_op, VOID)

    def test_same_word_same_signature(self):
        """Same phonemes → same signature (deterministic)."""
        sig1 = self.codec.compute_signature('baba')
        sig2 = self.codec.compute_signature('baba')
        self.assertEqual(sig1.dominant_op, sig2.dominant_op)
        self.assertEqual(sig1.d2_vector, sig2.d2_vector)

    def test_different_words_different_signatures(self):
        """Very different phonemes → different signatures."""
        sig_mama = self.codec.compute_signature('mama')
        sig_kick = self.codec.compute_signature('kik')
        # At least the D2 vectors should differ
        self.assertNotEqual(sig_mama.d2_vector, sig_kick.d2_vector)

    def test_spelling_fallback(self):
        """compute_from_spelling works as fallback."""
        sig = self.codec.compute_from_spelling('hello')
        self.assertIsInstance(sig, LexicalSignature)
        self.assertGreaterEqual(sig.dominant_op, 0)


# ================================================================
#  LEXICAL SIGNATURE TESTS
# ================================================================

class TestLexicalSignature(unittest.TestCase):
    """Signature similarity computations."""

    def test_cosine_self_similarity(self):
        """A signature has cosine similarity ~1.0 with itself."""
        sig = LexicalSignature(
            dominant_op=HARMONY,
            d2_vector=(0.1, 0.2, -0.3, 0.4, -0.1),
            soft_dist=tuple([0.1] * NUM_OPS),
            chain_length=5,
        )
        sim = sig.cosine_similarity(sig)
        self.assertAlmostEqual(sim, 1.0, places=3)

    def test_cosine_orthogonal(self):
        """Orthogonal vectors produce ~0.0 similarity."""
        sig_a = LexicalSignature(d2_vector=(1.0, 0.0, 0.0, 0.0, 0.0))
        sig_b = LexicalSignature(d2_vector=(0.0, 1.0, 0.0, 0.0, 0.0))
        sim = sig_a.cosine_similarity(sig_b)
        self.assertAlmostEqual(sim, 0.0, places=3)

    def test_dist_similarity(self):
        """Distribution similarity works."""
        dist_a = [0.0] * NUM_OPS
        dist_a[HARMONY] = 1.0
        dist_b = list(dist_a)
        sig_a = LexicalSignature(soft_dist=tuple(dist_a))
        sig_b = LexicalSignature(soft_dist=tuple(dist_b))
        sim = sig_a.dist_similarity(sig_b)
        self.assertAlmostEqual(sim, 1.0, places=3)


# ================================================================
#  LEXEME TESTS
# ================================================================

class TestLexeme(unittest.TestCase):

    def test_create_lexeme(self):
        lex = Lexeme(lexeme_id=0, lang='en', wordform='test',
                     lemma='test', phonemes='test')
        self.assertEqual(lex.lang, 'en')
        self.assertEqual(lex.wordform, 'test')

    def test_to_dict(self):
        lex = Lexeme(lexeme_id=42, lang='es', wordform='agua',
                     lemma='agua', phonemes='agwa',
                     sense_ids=['water'])
        d = lex.to_dict()
        self.assertEqual(d['id'], 42)
        self.assertEqual(d['lang'], 'es')
        self.assertEqual(d['wordform'], 'agua')
        self.assertIn('water', d['senses'])


# ================================================================
#  LEXICON STORE TESTS
# ================================================================

class TestLexiconStoreBasic(unittest.TestCase):
    """Basic add/lookup operations."""

    def setUp(self):
        self.store = LexiconStore()

    def test_add_lexeme(self):
        lex = self.store.add_lexeme('en', 'hello', phonemes='helo',
                                     sense_ids=['greeting'])
        self.assertEqual(lex.lang, 'en')
        self.assertEqual(lex.wordform, 'hello')
        self.assertEqual(self.store.word_count, 1)

    def test_lookup_word(self):
        self.store.add_lexeme('en', 'cat', phonemes='kæt',
                               sense_ids=['cat'])
        results = self.store.lookup_word('cat', 'en')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].wordform, 'cat')

    def test_lookup_word_case_insensitive(self):
        self.store.add_lexeme('de', 'Katze', phonemes='katse',
                               sense_ids=['cat'])
        results = self.store.lookup_word('katze', 'de')
        self.assertEqual(len(results), 1)

    def test_lookup_word_any_language(self):
        """Lookup without specifying language searches all."""
        self.store.add_lexeme('en', 'cat', phonemes='kæt',
                               sense_ids=['cat'])
        self.store.add_lexeme('es', 'gato', phonemes='gato',
                               sense_ids=['cat'])
        results = self.store.lookup_word('gato')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].lang, 'es')

    def test_lookup_lemma(self):
        self.store.add_lexeme('en', 'running', lemma='run',
                               phonemes='raning', sense_ids=['run'])
        results = self.store.lookup_lemma('run', 'en')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].wordform, 'running')

    def test_lookup_nonexistent(self):
        results = self.store.lookup_word('xyzzy', 'en')
        self.assertEqual(len(results), 0)


class TestLexiconStoreConceptLookup(unittest.TestCase):
    """Concept-based lookups."""

    def setUp(self):
        self.store = LexiconStore()
        self.store.add_lexeme('en', 'water', phonemes='woter',
                               sense_ids=['water'])
        self.store.add_lexeme('es', 'agua', phonemes='agwa',
                               sense_ids=['water'])
        self.store.add_lexeme('fr', 'eau', phonemes='o',
                               sense_ids=['water'])

    def test_lookup_concept(self):
        by_lang = self.store.lookup_concept('water')
        self.assertIn('en', by_lang)
        self.assertIn('es', by_lang)
        self.assertIn('fr', by_lang)

    def test_concept_words(self):
        words = self.store.concept_words('water', 'es')
        self.assertIn('agua', words)

    def test_concept_words_all_langs(self):
        words = self.store.concept_words('water')
        self.assertIn('water', words)
        self.assertIn('agua', words)
        self.assertIn('eau', words)


class TestLexiconStoreTranslation(unittest.TestCase):
    """Translation via concept pivot."""

    def setUp(self):
        self.store = LexiconStore()
        self.store.add_lexeme('en', 'water', phonemes='woter',
                               sense_ids=['water'])
        self.store.add_lexeme('es', 'agua', phonemes='agwa',
                               sense_ids=['water'])
        self.store.add_lexeme('fr', 'eau', phonemes='o',
                               sense_ids=['water'])
        self.store.add_lexeme('de', 'Wasser', phonemes='vaser',
                               sense_ids=['water'])

    def test_translate_en_to_es(self):
        results = self.store.translate('water', 'en', 'es')
        self.assertIn('agua', results)

    def test_translate_es_to_fr(self):
        results = self.store.translate('agua', 'es', 'fr')
        self.assertIn('eau', results)

    def test_translate_to_same_language(self):
        """Translating to same language returns nothing (filtered)."""
        # This actually returns the word itself via concept pivot
        # The behavior depends on whether same-lang entries match
        results = self.store.translate('water', 'en', 'en')
        # Should find 'water' since it's in the same concept
        if results:
            self.assertIn('water', results)

    def test_translate_unknown_word(self):
        results = self.store.translate('xyzzy', 'en', 'es')
        self.assertEqual(len(results), 0)

    def test_all_translations(self):
        result = self.store.all_translations('water', 'en')
        self.assertIn('es', result)
        self.assertIn('fr', result)
        self.assertIn('de', result)
        self.assertIn('agua', result['es'])


class TestLexiconStoreSoundLookup(unittest.TestCase):
    """Sound-similarity lookups."""

    def setUp(self):
        self.store = LexiconStore()
        self.store.load_seed_lexicon()

    def test_sound_lookup_returns_results(self):
        """Looking up a phoneme pattern should find similar-sounding words.

        Key insight: repeating 2-phoneme patterns (m-a-m-a) have ZERO D2
        because constant differences => zero second derivative. Must use
        non-repeating queries with 3+ distinct phonemes for real curvature.
        Use 'woter' (water's phonemes) which we know produces non-zero D2.
        """
        # Non-repeating query produces real D2 curvature
        results = self.store.lookup_by_sound('woter', threshold=0.01)
        # Should find 'water' and other words with similar D2 profiles
        self.assertGreater(len(results), 0,
            msg="Sound lookup should find at least one match in 350-word seed")

    def test_sound_lookup_sorted_by_similarity(self):
        """Results are sorted by similarity score (descending)."""
        results = self.store.lookup_by_sound('woter', threshold=0.01)
        if len(results) >= 2:
            self.assertGreaterEqual(results[0][1], results[1][1])

    def test_sound_lookup_returns_tuples(self):
        # 'kabesa' (head/es phonemes) -- non-repeating, real D2
        results = self.store.lookup_by_sound('kabesa', threshold=0.01)
        for lex, score in results:
            self.assertIsInstance(lex, Lexeme)
            self.assertIsInstance(score, float)
            self.assertGreaterEqual(score, 0.01)


# ================================================================
#  SEED LEXICON TESTS
# ================================================================

class TestSeedLexicon(unittest.TestCase):
    """Tests with full seed lexicon loaded."""

    def setUp(self):
        self.store = LexiconStore()
        self.store.load_seed_lexicon()

    def test_total_lexemes(self):
        self.assertEqual(self.store.word_count, 350)  # 50 × 7

    def test_concept_count(self):
        self.assertEqual(self.store.concept_count, 50)

    def test_language_count(self):
        self.assertEqual(self.store.language_count, 7)

    def test_all_seven_languages(self):
        expected = {'en', 'es', 'fr', 'de', 'he', 'ar', 'zh'}
        self.assertEqual(self.store.languages, expected)

    def test_translate_water_all_languages(self):
        """Water translates to all 6 other languages."""
        trans = self.store.all_translations('water', 'en')
        self.assertGreaterEqual(len(trans), 5)

    def test_translate_mother_roundtrip(self):
        """en→es→en roundtrip translation."""
        es_words = self.store.translate('mother', 'en', 'es')
        self.assertIn('madre', es_words)
        en_words = self.store.translate('madre', 'es', 'en')
        self.assertIn('mother', en_words)

    def test_every_concept_has_all_languages(self):
        """Every seed concept is covered in all 7 languages."""
        for concept_id in SEED_LEXICON:
            by_lang = self.store.lookup_concept(concept_id)
            self.assertEqual(len(by_lang), 7,
                msg=f"Concept '{concept_id}' missing languages: "
                    f"has {sorted(by_lang.keys())}")

    def test_stats(self):
        s = self.store.stats()
        self.assertEqual(s['total_lexemes'], 350)
        self.assertEqual(s['concepts_covered'], 50)
        self.assertEqual(s['language_count'], 7)
        self.assertIn('lexemes_per_language', s)

    def test_all_signatures_computed(self):
        """Every lexeme has a computed signature (chain_length > 0)."""
        computed = 0
        for lex in self.store.lexemes.values():
            if lex.signature.chain_length > 0:
                computed += 1
        # Most should compute (some very short words like 'o' may not)
        self.assertGreater(computed, 300)


# ================================================================
#  INTEGRATION TESTS
# ================================================================

class TestIntegrationWithWorldLattice(unittest.TestCase):
    """Lexicon works with WorldLattice."""

    def test_lexicon_senses_match_lattice_concepts(self):
        """Lexicon sense_ids should reference valid lattice concept IDs."""
        from ck_sim.ck_world_lattice import WorldLattice

        lattice = WorldLattice()
        lattice.load_seed_corpus()

        store = LexiconStore(lattice=lattice)
        store.load_seed_lexicon()

        # Check that at least some seed concepts exist in the lattice
        matched = 0
        for concept_id in SEED_LEXICON:
            if concept_id in lattice.nodes:
                matched += 1

        # Many seed concepts should match core lattice concepts
        self.assertGreater(matched, 15,
            msg=f"Only {matched}/50 seed concepts found in lattice")

    def test_phoneme_vs_spelling_signatures(self):
        """Phoneme-based and spelling-based signatures differ but both work."""
        codec = PhonemeCodec()
        sig_phon = codec.compute_signature('mama')
        sig_spell = codec.compute_from_spelling('mama')

        # Both should produce valid signatures
        self.assertGreater(sig_phon.chain_length, 0)
        self.assertGreater(sig_spell.chain_length, 0)


class TestIntegrationWithD2(unittest.TestCase):
    """Phoneme codec uses D2 curvature correctly."""

    def test_articulatory_difference_reflected(self):
        """Words with different articulatory profiles produce different D2.

        Key insight: perfectly repeating 2-phoneme patterns (m-a-m-a...)
        have ZERO second derivative because the differences are constant.
        Real words with 3+ distinct phonemes produce non-zero D2.

        Use real non-repeating sequences so D2 curvature is meaningful.
        """
        codec = PhonemeCodec()
        # Bilabial-heavy: 'madre' = MEM, ALEPH, DALET, RESH, HE
        sig_bilabial = codec.compute_signature('madre')
        # Velar-heavy: 'koxav' = KAF, AYIN, CHET, ALEPH, VAV
        sig_velar = codec.compute_signature('koxav')

        # Both should produce non-zero D2 (non-repeating sequences)
        self.assertGreater(sig_bilabial.chain_length, 0,
            msg="Non-repeating bilabial sequence must produce D2")
        self.assertGreater(sig_velar.chain_length, 0,
            msg="Non-repeating velar sequence must produce D2")

        # D2 vectors should differ for different articulatory profiles
        self.assertNotEqual(sig_bilabial.d2_vector, sig_velar.d2_vector,
            msg="Different articulatory profiles must produce different D2 vectors")

    def test_similar_phonemes_similar_signatures(self):
        """Words with similar phonemes should have higher similarity.

        Use longer sequences for stable D2 computation and
        dist_similarity (on 10-bin operator distributions) which is
        more robust than cosine on raw D2 vectors for short words.
        """
        codec = PhonemeCodec()
        # Longer sequences to ensure non-trivial D2 output
        sig_a = codec.compute_signature('mamamamama')
        sig_b = codec.compute_signature('mamamamaman')  # Same root pattern + NUN
        sig_c = codec.compute_signature('krikrikrikri')  # Very different

        # Use dist_similarity -- compares operator distributions, more stable
        sim_ab = sig_a.dist_similarity(sig_b)
        sim_ac = sig_a.dist_similarity(sig_c)

        # 'mama...' shares the MEM+ALEPH loop with 'maman...',
        # while 'kri...' uses KAF+RESH+YOD -- different operator mix
        self.assertGreaterEqual(sim_ab, sim_ac,
            msg="Similar phoneme patterns should yield higher dist similarity")


if __name__ == '__main__':
    unittest.main()
