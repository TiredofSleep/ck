"""
ck_english_tests.py -- Validation Tests for CK Education Pipeline
=================================================================
Operator: COUNTER (2) -- measuring everything.

Tests for:
  1. Dictionary Expander (vocabulary layer)
  2. Sentence Composer (grammar layer)
  3. Retrieval Engine (knowledge layer)
  4. Self Mirror (improvement layer)
  5. Integration (full pipeline)

Run: python -m ck_sim.ck_english_tests

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import unittest
import json
import os
import tempfile

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, LATTICE, COUNTER, PROGRESS,
    COLLAPSE, BALANCE, CHAOS, BREATH, RESET, OP_NAMES, CL, compose
)
from ck_sim.ck_sim_d2 import D2Pipeline


# ================================================================
#  1. DICTIONARY EXPANDER TESTS
# ================================================================

class TestDictionaryExpander(unittest.TestCase):
    """Tests for ck_d2_dictionary_expander.py"""

    def test_import(self):
        """Module imports without error."""
        from ck_sim.ck_d2_dictionary_expander import (
            DictionaryExpander, classify_pos, word_to_d2,
            word_to_phonemes, d2_agrees_with_label,
            build_expanded_dictionary
        )

    def test_pos_classification(self):
        """POS heuristics assign correct categories."""
        from ck_sim.ck_d2_dictionary_expander import classify_pos

        # Suffix-based
        self.assertEqual(classify_pos('happiness'), 'noun')
        self.assertEqual(classify_pos('movement'), 'noun')
        self.assertEqual(classify_pos('creation'), 'noun')
        self.assertEqual(classify_pos('quickly'), 'adv')
        self.assertEqual(classify_pos('organize'), 'verb')
        self.assertEqual(classify_pos('beautiful'), 'adj')
        self.assertEqual(classify_pos('dangerous'), 'adj')
        self.assertEqual(classify_pos('running'), 'verb')
        self.assertEqual(classify_pos('walked'), 'verb')

        # Known words
        self.assertEqual(classify_pos('the'), 'function')
        self.assertEqual(classify_pos('run'), 'verb')
        self.assertEqual(classify_pos('good'), 'adj')

    def test_word_to_d2(self):
        """D2 analysis produces valid operator data."""
        from ck_sim.ck_d2_dictionary_expander import word_to_d2

        result = word_to_d2('harmony')
        self.assertIn('operator_seq', result)
        self.assertIn('dominant_op', result)
        self.assertIn('soft_dist', result)
        self.assertIn('mean_d2', result)

        # Operator sequence should have entries (word has 7 letters, needs 3+ for D2)
        self.assertTrue(len(result['operator_seq']) > 0)
        # Dominant op should be 0-9
        self.assertIn(result['dominant_op'], range(NUM_OPS))
        # Soft dist should sum to ~1.0
        self.assertAlmostEqual(sum(result['soft_dist']), 1.0, places=2)
        # Mean D2 should have 5 dimensions
        self.assertEqual(len(result['mean_d2']), 5)

    def test_word_to_d2_short_word(self):
        """Short words still produce valid (possibly empty) results."""
        from ck_sim.ck_d2_dictionary_expander import word_to_d2

        result = word_to_d2('ab')  # Only 2 letters, no D2 possible
        self.assertEqual(result['dominant_op'], VOID)

    def test_word_to_phonemes(self):
        """Phoneme mapping produces Hebrew root sequences."""
        from ck_sim.ck_d2_dictionary_expander import word_to_phonemes

        phonemes = word_to_phonemes('cat')
        self.assertEqual(len(phonemes), 3)
        # c → GIMEL, a → ALEPH, t → TAV
        self.assertEqual(phonemes[0], 'GIMEL')
        self.assertEqual(phonemes[1], 'ALEPH')
        self.assertEqual(phonemes[2], 'TAV')

    def test_d2_agreement(self):
        """D2 agreement check works."""
        from ck_sim.ck_d2_dictionary_expander import d2_agrees_with_label

        # Very low threshold should always agree
        self.assertTrue(d2_agrees_with_label('harmony', HARMONY, threshold=0.0))

    def test_expander_basic(self):
        """Expander creates entries with enriched format."""
        from ck_sim.ck_d2_dictionary_expander import DictionaryExpander

        exp = DictionaryExpander()
        exp.load_curated_dict({'truth': 7, 'chaos': 6, 'growth': 3})
        exp.expand(target_size=10)

        self.assertIn('truth', exp.entries)
        entry = exp.entries['truth']
        self.assertEqual(entry['dominant_op'], 7)
        self.assertIn('pos', entry)
        self.assertIn('phoneme_seq', entry)
        self.assertIn('operator_seq', entry)

    def test_expander_add_words(self):
        """Expander can add arbitrary word lists."""
        from ck_sim.ck_d2_dictionary_expander import DictionaryExpander

        exp = DictionaryExpander()
        exp.add_words(['hello', 'world', 'python', 'coherence'])
        self.assertEqual(len(exp.entries), 4)

    def test_expander_by_op_pos(self):
        """Can query words by operator and POS."""
        from ck_sim.ck_d2_dictionary_expander import DictionaryExpander

        exp = DictionaryExpander()
        exp.load_curated_dict({
            'build': 3, 'grow': 3, 'create': 3,
            'pattern': 1, 'structure': 1,
        })
        exp.expand(target_size=10)

        nouns = exp.get_nouns(1)  # LATTICE nouns
        # 'pattern' and 'structure' should be there
        self.assertTrue(len(nouns) > 0)

    def test_expander_save_load(self):
        """Save and load round-trip."""
        from ck_sim.ck_d2_dictionary_expander import DictionaryExpander

        exp = DictionaryExpander()
        exp.add_words(['alpha', 'beta', 'gamma'])

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            path = f.name

        try:
            exp.save(path)
            exp2 = DictionaryExpander()
            exp2.load(path)
            self.assertEqual(len(exp2.entries), 3)
            self.assertIn('alpha', exp2.entries)
        finally:
            os.unlink(path)

    def test_expander_stats(self):
        """Stats report is complete."""
        from ck_sim.ck_d2_dictionary_expander import DictionaryExpander

        exp = DictionaryExpander()
        exp.add_words(['test', 'word', 'hello'])
        stats = exp.stats()
        self.assertIn('total_words', stats)
        self.assertIn('by_operator', stats)
        self.assertIn('by_pos', stats)
        self.assertEqual(stats['total_words'], 3)


# ================================================================
#  2. SENTENCE COMPOSER TESTS
# ================================================================

class TestSentenceComposer(unittest.TestCase):
    """Tests for ck_sentence_composer.py"""

    def test_import(self):
        """Module imports without error."""
        from ck_sim.ck_sentence_composer import (
            OperatorGrammarGraph, ClauseComposer, SentencePlanner,
            CKTalkLoop, text_to_operator_chain, curvature_check, GRAMMAR
        )

    def test_grammar_graph(self):
        """Grammar graph has correct properties."""
        from ck_sim.ck_sentence_composer import GRAMMAR

        # HARMONY→HARMONY should be high weight (CL[7][7] = 7 = HARMONY)
        self.assertEqual(GRAMMAR.transition_weight(HARMONY, HARMONY), 1.0)
        # VOID→VOID should be low weight (CL[0][0] = 0 = VOID)
        self.assertEqual(GRAMMAR.transition_weight(VOID, VOID), 0.1)

    def test_chain_coherence(self):
        """Chain coherence computed correctly."""
        from ck_sim.ck_sentence_composer import GRAMMAR

        # All-HARMONY chain should be perfectly coherent
        coh = GRAMMAR.chain_coherence([HARMONY, HARMONY, HARMONY])
        self.assertEqual(coh, 1.0)

        # Single op chain
        coh = GRAMMAR.chain_coherence([HARMONY])
        self.assertEqual(coh, 1.0)

    def test_cl_fuse(self):
        """CL fuse matches compose()."""
        from ck_sim.ck_sentence_composer import GRAMMAR

        fused = GRAMMAR.cl_fuse([HARMONY, PROGRESS])
        self.assertEqual(fused, compose(HARMONY, PROGRESS))

    def test_clause_composer_basic(self):
        """Clause composer generates non-empty text."""
        from ck_sim.ck_sentence_composer import ClauseComposer

        comp = ClauseComposer(seed=42)
        clause = comp.compose_clause(LATTICE, PROGRESS, HARMONY)
        self.assertTrue(len(clause) > 0)
        # Should contain actual words
        self.assertTrue(any(c.isalpha() for c in clause))

    def test_compose_from_chain(self):
        """Compose from operator chain produces text."""
        from ck_sim.ck_sentence_composer import ClauseComposer

        comp = ClauseComposer(seed=42)
        text = comp.compose_from_chain([LATTICE, PROGRESS, HARMONY])
        self.assertTrue(len(text) > 5)
        self.assertTrue(text.endswith('.'))

    def test_sentence_planner(self):
        """Sentence planner produces multi-sentence text."""
        from ck_sim.ck_sentence_composer import SentencePlanner

        planner = SentencePlanner(seed=42)
        text = planner.plan([LATTICE, PROGRESS, HARMONY, BREATH, RESET])
        self.assertTrue(len(text) > 10)

    def test_text_to_operator_chain(self):
        """Text → operator chain via D2."""
        from ck_sim.ck_sentence_composer import text_to_operator_chain

        ops = text_to_operator_chain("the truth will set you free")
        self.assertTrue(len(ops) > 0)
        self.assertTrue(all(0 <= o < NUM_OPS for o in ops))

    def test_curvature_check(self):
        """Curvature check returns valid results."""
        from ck_sim.ck_sentence_composer import curvature_check

        passes, score = curvature_check("harmony and peace unite the world")
        self.assertIsInstance(passes, bool)
        self.assertIsInstance(score, float)
        self.assertTrue(0.0 <= score <= 1.0)

    def test_talk_loop_speak(self):
        """CK talk loop generates speech from operators."""
        from ck_sim.ck_sentence_composer import CKTalkLoop

        loop = CKTalkLoop(seed=42)
        text = loop.speak([HARMONY, PROGRESS, LATTICE])
        self.assertTrue(len(text) > 5)

    def test_talk_loop_respond(self):
        """CK talk loop responds to text input."""
        from ck_sim.ck_sentence_composer import CKTalkLoop

        loop = CKTalkLoop(seed=42)
        text = loop.respond("hello, how are you?")
        self.assertTrue(len(text) > 3)

    def test_talk_loop_explain(self):
        """CK talk loop explains topics."""
        from ck_sim.ck_sentence_composer import CKTalkLoop

        loop = CKTalkLoop(seed=42)
        text = loop.explain("the structure of coherence in living systems")
        self.assertTrue(len(text) > 10)

    def test_talk_loop_with_dictionary(self):
        """Talk loop uses enriched dictionary when provided."""
        from ck_sim.ck_sentence_composer import CKTalkLoop

        # Minimal test dictionary
        test_dict = {
            'harmony': {'dominant_op': 7, 'pos': 'noun', 'phoneme_seq': [], 'operator_seq': [], 'd2_vector': [0]*5, 'soft_dist': [0]*10, 'frequency': 100, 'source': 'test'},
            'grow': {'dominant_op': 3, 'pos': 'verb', 'phoneme_seq': [], 'operator_seq': [], 'd2_vector': [0]*5, 'soft_dist': [0]*10, 'frequency': 100, 'source': 'test'},
            'structure': {'dominant_op': 1, 'pos': 'noun', 'phoneme_seq': [], 'operator_seq': [], 'd2_vector': [0]*5, 'soft_dist': [0]*10, 'frequency': 100, 'source': 'test'},
        }
        loop = CKTalkLoop(dictionary=test_dict, seed=42)
        text = loop.speak([LATTICE, PROGRESS, HARMONY])
        self.assertTrue(len(text) > 5)


# ================================================================
#  3. RETRIEVAL ENGINE TESTS
# ================================================================

class TestRetrievalEngine(unittest.TestCase):
    """Tests for ck_retrieval_engine.py"""

    def test_import(self):
        """Module imports without error."""
        from ck_sim.ck_retrieval_engine import (
            RetrievalEngine, ChunkStore, TextChunk,
            text_to_operator_dist, text_to_mean_d2,
            kl_divergence, symmetric_kl, d2_cosine_similarity,
            combined_similarity
        )

    def test_text_to_operator_dist(self):
        """Text → operator distribution."""
        from ck_sim.ck_retrieval_engine import text_to_operator_dist

        dist = text_to_operator_dist("the truth will set you free")
        self.assertEqual(len(dist), NUM_OPS)
        self.assertAlmostEqual(sum(dist), 1.0, places=2)

    def test_text_to_mean_d2(self):
        """Text → mean 5D D2 vector."""
        from ck_sim.ck_retrieval_engine import text_to_mean_d2

        d2 = text_to_mean_d2("coherence is beautiful")
        self.assertEqual(len(d2), 5)

    def test_kl_divergence(self):
        """KL divergence basic properties."""
        from ck_sim.ck_retrieval_engine import kl_divergence

        # Same distribution → KL ≈ 0
        p = [0.1] * 10
        kl = kl_divergence(p, p)
        self.assertAlmostEqual(kl, 0.0, places=5)

        # Different distributions → KL > 0
        q = [0.5] + [0.5 / 9] * 9
        kl = kl_divergence(p, q)
        self.assertGreater(kl, 0.0)

    def test_symmetric_kl(self):
        """Symmetric KL is symmetric."""
        from ck_sim.ck_retrieval_engine import symmetric_kl

        p = [0.3, 0.2, 0.1, 0.1, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
        q = [0.1, 0.1, 0.3, 0.2, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
        self.assertAlmostEqual(symmetric_kl(p, q), symmetric_kl(q, p), places=10)

    def test_cosine_similarity(self):
        """D2 cosine similarity basic properties."""
        from ck_sim.ck_retrieval_engine import d2_cosine_similarity

        a = [1.0, 0.0, 0.0, 0.0, 0.0]
        # Same vector → cosine = 1.0
        self.assertAlmostEqual(d2_cosine_similarity(a, a), 1.0, places=5)
        # Opposite → cosine = -1.0
        b = [-1.0, 0.0, 0.0, 0.0, 0.0]
        self.assertAlmostEqual(d2_cosine_similarity(a, b), -1.0, places=5)

    def test_chunk_store_add_query(self):
        """ChunkStore can add and query text."""
        from ck_sim.ck_retrieval_engine import ChunkStore

        store = ChunkStore()
        store.add_text(
            "Photosynthesis is the process by which plants convert "
            "sunlight into energy. This biological process is fundamental "
            "to life on Earth and involves complex chemical reactions.",
            source='biology'
        )
        store.add_text(
            "The structure of DNA is a double helix consisting of "
            "nucleotide base pairs. This molecular structure was "
            "discovered by Watson and Crick in nineteen fifty three.",
            source='genetics'
        )

        self.assertTrue(len(store.chunks) > 0)

        # Query should return results
        results = store.query("plants convert sunlight energy")
        self.assertTrue(len(results) > 0)

    def test_retrieval_engine_basic(self):
        """RetrievalEngine end-to-end."""
        from ck_sim.ck_retrieval_engine import RetrievalEngine

        engine = RetrievalEngine()
        # Use a large enough text block to produce at least one chunk (>500 chars)
        engine.ingest_text(
            "Coherence is the measure of how aligned the operator "
            "distributions are across multiple modalities. When "
            "coherence is high, the system is sovereign. The CL table "
            "defines how operators compose. Each pair of operators "
            "produces a result through the composition table. The "
            "heartbeat ticks at fifty hertz and the running fuse "
            "accumulates toward harmony. Sovereignty is reached when "
            "the coherence stays above the threshold of five sevenths "
            "for at least fifty consecutive ticks. The brain module "
            "tracks transitions in a ten by ten matrix and crystallizes "
            "patterns that appear with sufficient frequency.",
            source='ck_theory'
        )

        self.assertTrue(len(engine.store.chunks) > 0,
                         f"Expected chunks but got {len(engine.store.chunks)}")
        results = engine.retrieve("What is coherence?")
        self.assertTrue(len(results) > 0)
        text, score = results[0]
        # Retrieval should return text from the source
        self.assertTrue(len(text) > 20)
        self.assertIsInstance(score, float)
        self.assertGreater(score, 0.0)

    def test_chunk_store_save_load(self):
        """ChunkStore save/load round-trip."""
        from ck_sim.ck_retrieval_engine import ChunkStore

        store = ChunkStore()
        store.add_text("Test text for saving and loading.", source='test')

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            path = f.name

        try:
            store.save_signatures(path)
            store2 = ChunkStore()
            store2.load_signatures(path)
            self.assertEqual(len(store2.chunks), len(store.chunks))
        finally:
            os.unlink(path)

    def test_query_by_operator(self):
        """Query by operator returns relevant chunks."""
        from ck_sim.ck_retrieval_engine import ChunkStore

        store = ChunkStore()
        store.add_text("Growth and progress and building new things ahead forward", source='growth')
        store.add_text("Destruction and collapse and ruin and failure and decay", source='collapse')

        # PROGRESS-dominant chunks should rank higher for PROGRESS query
        results = store.query_by_operator(PROGRESS)
        self.assertTrue(len(results) > 0)


# ================================================================
#  4. SELF MIRROR TESTS
# ================================================================

class TestSelfMirror(unittest.TestCase):
    """Tests for ck_self_mirror.py"""

    def test_import(self):
        """Module imports without error."""
        from ck_sim.ck_self_mirror import (
            CKMirror, mirror_score, coherence_score, d2_variance_score,
            repetition_score, complexity_score, pfe_text_score,
            suggest_corrections, drift_operator_chain
        )

    def test_coherence_score(self):
        """Coherence score range is [0, 1]."""
        from ck_sim.ck_self_mirror import coherence_score

        # All-HARMONY ops → high coherence
        ops = [HARMONY, HARMONY, HARMONY, HARMONY]
        score = coherence_score(ops)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)

    def test_d2_variance_score(self):
        """D2 variance score is in [0, 1]."""
        from ck_sim.ck_self_mirror import d2_variance_score

        # Constant vectors → low variance → high score
        vecs = [[0.1, 0.1, 0.1, 0.1, 0.1]] * 5
        score = d2_variance_score(vecs)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)

    def test_repetition_score(self):
        """Repetition detection works."""
        from ck_sim.ck_self_mirror import repetition_score

        # Highly repetitive text
        score_rep = repetition_score("the the the the the the the the")
        # Non-repetitive text
        score_unique = repetition_score("coherence is the measure of alignment in systems")
        # Unique should score higher (less repetitive)
        self.assertGreater(score_unique, score_rep)

    def test_complexity_score(self):
        """Complexity score range and behavior."""
        from ck_sim.ck_self_mirror import complexity_score

        # Monotone → low complexity
        score_mono = complexity_score([HARMONY, HARMONY, HARMONY, HARMONY])
        # Diverse → higher complexity
        score_diverse = complexity_score([LATTICE, COUNTER, PROGRESS, HARMONY, BREATH])
        self.assertGreater(score_diverse, score_mono)

    def test_mirror_score_composite(self):
        """Mirror score returns valid composite."""
        from ck_sim.ck_self_mirror import mirror_score

        score, breakdown = mirror_score("The structure grows toward harmony and truth.")
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
        self.assertIn('coherence', breakdown)
        self.assertIn('total', breakdown)

    def test_suggest_corrections(self):
        """Suggestions generated for low scores."""
        from ck_sim.ck_self_mirror import suggest_corrections

        # Low coherence → should suggest improvement
        breakdown = {'coherence': 0.2, 'd2_variance': 0.5,
                     'repetition': 0.8, 'complexity': 0.6, 'pfe': 0.5}
        suggestions = suggest_corrections("test", 0.3, breakdown)
        self.assertIn('increase_harmony', suggestions)

    def test_drift_operator_chain(self):
        """Drift produces modified chain."""
        from ck_sim.ck_self_mirror import drift_operator_chain

        original = [COLLAPSE, VOID, COLLAPSE, VOID]
        corrected = drift_operator_chain(original, ['improve_valence'])
        # Should have replaced at least one COLLAPSE with PROGRESS
        self.assertTrue(any(o == PROGRESS for o in corrected))

    def test_ck_mirror_class(self):
        """CKMirror class evaluate/suggest/correct cycle."""
        from ck_sim.ck_self_mirror import CKMirror

        mirror = CKMirror(threshold=0.4)
        score, breakdown = mirror.evaluate("The harmony of truth aligns with beauty.")
        self.assertIsInstance(score, float)

        if not mirror.is_acceptable(score):
            suggestions = mirror.suggest(breakdown)
            self.assertIsInstance(suggestions, list)

    def test_mirror_trend(self):
        """Mirror trend detection with sufficient data."""
        from ck_sim.ck_self_mirror import CKMirror

        mirror = CKMirror()
        # Not enough data
        self.assertEqual(mirror.trend(), 'insufficient_data')

        # Add data
        for _ in range(10):
            mirror.evaluate("The harmony of truth and beauty connects everything.")
        trend = mirror.trend()
        self.assertIn(trend, ['improving', 'stable', 'declining', 'insufficient_data'])


# ================================================================
#  5. INTEGRATION TESTS
# ================================================================

class TestIntegration(unittest.TestCase):
    """Integration tests across modules."""

    def test_dictionary_to_composer(self):
        """Dictionary feeds into sentence composer."""
        from ck_sim.ck_d2_dictionary_expander import DictionaryExpander
        from ck_sim.ck_sentence_composer import CKTalkLoop

        exp = DictionaryExpander()
        exp.load_curated_dict({
            'harmony': 7, 'truth': 7, 'love': 7,
            'grow': 3, 'build': 3, 'create': 3,
            'structure': 1, 'pattern': 1, 'framework': 1,
            'measure': 2, 'observe': 2, 'analyze': 2,
            'chaos': 6, 'wild': 6, 'storm': 6,
            'rest': 4, 'stop': 4, 'fall': 4,
            'balance': 5, 'equal': 5, 'center': 5,
            'breathe': 8, 'rhythm': 8, 'pulse': 8,
            'begin': 9, 'fresh': 9, 'new': 9,
            'nothing': 0, 'empty': 0, 'void': 0,
        })
        exp.expand(target_size=100)

        loop = CKTalkLoop(dictionary=exp.entries, seed=42)
        text = loop.speak([LATTICE, PROGRESS, HARMONY])
        self.assertTrue(len(text) > 5)

    def test_retrieval_to_composer(self):
        """Retrieved knowledge feeds into speech."""
        from ck_sim.ck_retrieval_engine import RetrievalEngine
        from ck_sim.ck_sentence_composer import CKTalkLoop

        engine = RetrievalEngine()
        engine.ingest_text(
            "The coherence field measures alignment across modalities. "
            "High coherence means the system is functioning well.",
            source='theory'
        )

        results = engine.retrieve("coherence field")
        self.assertTrue(len(results) > 0)

        loop = CKTalkLoop(seed=42)
        text = loop.explain(results[0][0])
        self.assertTrue(len(text) > 10)

    def test_mirror_on_composed_text(self):
        """Mirror evaluates composed sentences."""
        from ck_sim.ck_sentence_composer import CKTalkLoop
        from ck_sim.ck_self_mirror import CKMirror

        loop = CKTalkLoop(seed=42)
        mirror = CKMirror(threshold=0.3)

        text = loop.speak([HARMONY, PROGRESS, BREATH, HARMONY])
        score, breakdown = mirror.evaluate(text)
        self.assertIsInstance(score, float)
        self.assertTrue(0.0 <= score <= 1.0)

    def test_full_speak_evaluate_correct_cycle(self):
        """Full cycle: speak → evaluate → correct → re-speak."""
        from ck_sim.ck_sentence_composer import CKTalkLoop, text_to_operator_chain
        from ck_sim.ck_self_mirror import CKMirror

        loop = CKTalkLoop(seed=42)
        mirror = CKMirror(threshold=0.3)

        # Speak
        ops = [COLLAPSE, VOID, CHAOS, COLLAPSE]
        text = loop.speak(ops)
        self.assertTrue(len(text) > 0)

        # Evaluate
        score, breakdown = mirror.evaluate(text)

        # Correct if needed
        if not mirror.is_acceptable(score):
            suggestions = mirror.suggest(breakdown)
            corrected_ops = mirror.correct(ops, suggestions)
            new_text = loop.speak(corrected_ops)
            self.assertTrue(len(new_text) > 0)

    def test_stage_0_bootstrap(self):
        """Pipeline Stage 0 passes."""
        from ck_sim.ck_english_build import CKEducationPipeline

        pipeline = CKEducationPipeline()
        pipeline.stage_0_bootstrap()
        self.assertTrue(pipeline.stages_complete[0])


# ================================================================
#  MAIN
# ================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("  CK EDUCATION PIPELINE -- VALIDATION TESTS")
    print("=" * 60)
    unittest.main(verbosity=2)
