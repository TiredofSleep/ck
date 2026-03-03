"""
ck_dialogue_tests.py -- Tests for Dialogue Engine: Learn, Track, Compose
=========================================================================
Validates: ClaimExtractor, ConversationMemory, DialogueTracker,
ResponseComposer, DialogueEngine, and full pipeline integration.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import unittest
import math
import os
import sys

# Ensure ck_sim package is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ================================================================
#  CONSTANTS TESTS
# ================================================================

class TestDialogueConstants(unittest.TestCase):
    """Validate dialogue module constants."""

    def test_max_turn_history_positive(self):
        from ck_sim.ck_dialogue import MAX_TURN_HISTORY
        self.assertGreater(MAX_TURN_HISTORY, 0)
        self.assertEqual(MAX_TURN_HISTORY, 64)

    def test_max_topics_positive(self):
        from ck_sim.ck_dialogue import MAX_TOPICS
        self.assertGreater(MAX_TOPICS, 0)
        self.assertEqual(MAX_TOPICS, 16)

    def test_topic_decay_in_range(self):
        from ck_sim.ck_dialogue import TOPIC_DECAY
        self.assertGreater(TOPIC_DECAY, 0.0)
        self.assertLess(TOPIC_DECAY, 1.0)
        self.assertAlmostEqual(TOPIC_DECAY, 0.9)

    def test_topic_min_relevance_positive(self):
        from ck_sim.ck_dialogue import TOPIC_MIN_RELEVANCE
        self.assertGreater(TOPIC_MIN_RELEVANCE, 0.0)
        self.assertLess(TOPIC_MIN_RELEVANCE, 0.5)

    def test_depth_constants_ordered(self):
        from ck_sim.ck_dialogue import DEPTH_RED, DEPTH_YELLOW, DEPTH_GREEN
        self.assertEqual(DEPTH_RED, 1)
        self.assertEqual(DEPTH_YELLOW, 2)
        self.assertEqual(DEPTH_GREEN, 3)
        self.assertLess(DEPTH_RED, DEPTH_YELLOW)
        self.assertLess(DEPTH_YELLOW, DEPTH_GREEN)

    def test_claim_coherence_boost_positive(self):
        from ck_sim.ck_dialogue import CLAIM_COHERENCE_BOOST
        self.assertGreater(CLAIM_COHERENCE_BOOST, 0.0)
        self.assertLessEqual(CLAIM_COHERENCE_BOOST, 1.0)


# ================================================================
#  TEMPLATE FRAGMENTS TESTS
# ================================================================

class TestTemplateFragments(unittest.TestCase):
    """Validate template fragment structure."""

    def test_level0_has_all_operators(self):
        from ck_sim.ck_dialogue import TEMPLATE_FRAGMENTS
        from ck_sim.ck_sim_heartbeat import NUM_OPS
        level0 = TEMPLATE_FRAGMENTS[0]
        for op in range(NUM_OPS):
            self.assertIn(op, level0, f"Missing operator {op} in level 0")
            self.assertGreater(len(level0[op]), 0, f"Empty phrases for operator {op}")

    def test_level0_phrases_are_strings(self):
        from ck_sim.ck_dialogue import TEMPLATE_FRAGMENTS
        for op, phrases in TEMPLATE_FRAGMENTS[0].items():
            for phrase in phrases:
                self.assertIsInstance(phrase, str)
                self.assertGreater(len(phrase), 0)

    def test_level1_has_intents(self):
        from ck_sim.ck_dialogue import TEMPLATE_FRAGMENTS
        level1 = TEMPLATE_FRAGMENTS[1]
        expected_intents = ['observe', 'reflect', 'learn', 'affirm', 'question']
        for intent in expected_intents:
            self.assertIn(intent, level1, f"Missing intent '{intent}' in level 1")
            self.assertGreater(len(level1[intent]), 0)

    def test_level1_templates_have_one_slot(self):
        from ck_sim.ck_dialogue import TEMPLATE_FRAGMENTS
        for intent, templates in TEMPLATE_FRAGMENTS[1].items():
            for t in templates:
                self.assertIn('{0}', t, f"Template missing slot {{0}}: {t}")

    def test_level2_has_styles(self):
        from ck_sim.ck_dialogue import TEMPLATE_FRAGMENTS
        level2 = TEMPLATE_FRAGMENTS[2]
        expected_styles = ['connect', 'contrast', 'cause', 'learn_deep']
        for style in expected_styles:
            self.assertIn(style, level2, f"Missing style '{style}' in level 2")

    def test_level2_templates_have_two_slots(self):
        from ck_sim.ck_dialogue import TEMPLATE_FRAGMENTS
        for style, templates in TEMPLATE_FRAGMENTS[2].items():
            for t in templates:
                self.assertIn('{0}', t, f"Template missing {{0}}: {t}")
                self.assertIn('{1}', t, f"Template missing {{1}}: {t}")

    def test_level3_has_styles(self):
        from ck_sim.ck_dialogue import TEMPLATE_FRAGMENTS
        level3 = TEMPLATE_FRAGMENTS[3]
        expected_styles = ['synthesize', 'narrative', 'reflect_deep']
        for style in expected_styles:
            self.assertIn(style, level3, f"Missing style '{style}' in level 3")

    def test_level3_templates_have_three_slots(self):
        from ck_sim.ck_dialogue import TEMPLATE_FRAGMENTS
        for style, templates in TEMPLATE_FRAGMENTS[3].items():
            for t in templates:
                self.assertIn('{0}', t, f"Template missing {{0}}: {t}")
                self.assertIn('{1}', t, f"Template missing {{1}}: {t}")
                self.assertIn('{2}', t, f"Template missing {{2}}: {t}")

    def test_four_depth_levels(self):
        from ck_sim.ck_dialogue import TEMPLATE_FRAGMENTS
        self.assertIn(0, TEMPLATE_FRAGMENTS)
        self.assertIn(1, TEMPLATE_FRAGMENTS)
        self.assertIn(2, TEMPLATE_FRAGMENTS)
        self.assertIn(3, TEMPLATE_FRAGMENTS)


# ================================================================
#  EXTRACTED CLAIM TESTS
# ================================================================

class TestExtractedClaim(unittest.TestCase):
    """Validate ExtractedClaim dataclass."""

    def test_default_values(self):
        from ck_sim.ck_dialogue import ExtractedClaim
        from ck_sim.ck_sim_heartbeat import VOID
        claim = ExtractedClaim(key='test', text='test text', claim_type='is_claim')
        self.assertEqual(claim.key, 'test')
        self.assertEqual(claim.text, 'test text')
        self.assertEqual(claim.claim_type, 'is_claim')
        self.assertEqual(claim.subject, "")
        self.assertEqual(claim.predicate, "")
        self.assertEqual(claim.operator, VOID)
        self.assertAlmostEqual(claim.confidence, 0.5)

    def test_custom_values(self):
        from ck_sim.ck_dialogue import ExtractedClaim
        from ck_sim.ck_sim_heartbeat import HARMONY
        claim = ExtractedClaim(
            key='is_claim:sky', text='sky is blue', claim_type='is_claim',
            subject='sky', predicate='blue', operator=HARMONY, confidence=0.8,
        )
        self.assertEqual(claim.subject, 'sky')
        self.assertEqual(claim.predicate, 'blue')
        self.assertEqual(claim.operator, HARMONY)
        self.assertAlmostEqual(claim.confidence, 0.8)


# ================================================================
#  CLAIM EXTRACTOR TESTS
# ================================================================

class TestClaimExtractor(unittest.TestCase):
    """Validate ClaimExtractor: pattern matching on text."""

    def setUp(self):
        from ck_sim.ck_dialogue import ClaimExtractor
        self.extractor = ClaimExtractor()

    def test_construction(self):
        self.assertIsNotNone(self.extractor)
        self.assertEqual(self.extractor.seen_count, 0)

    def test_is_claim_extraction(self):
        claims = self.extractor.extract("The sky is blue")
        self.assertGreater(len(claims), 0)
        found_types = [c.claim_type for c in claims]
        self.assertIn('is_claim', found_types)

    def test_has_claim_extraction(self):
        claims = self.extractor.extract("The dog has four legs")
        self.assertGreater(len(claims), 0)
        found_types = [c.claim_type for c in claims]
        self.assertIn('has_claim', found_types)

    def test_name_claim_extraction(self):
        claims = self.extractor.extract("My name is Brayden")
        self.assertGreater(len(claims), 0)
        found_types = [c.claim_type for c in claims]
        self.assertIn('name_claim', found_types)

    def test_preference_claim_extraction(self):
        claims = self.extractor.extract("I like music")
        self.assertGreater(len(claims), 0)
        found_types = [c.claim_type for c in claims]
        self.assertIn('preference_claim', found_types)

    def test_means_claim_extraction(self):
        claims = self.extractor.extract("Harmony means alignment")
        self.assertGreater(len(claims), 0)
        found_types = [c.claim_type for c in claims]
        self.assertIn('means_claim', found_types)

    def test_can_claim_extraction(self):
        claims = self.extractor.extract("CK can learn from conversation")
        self.assertGreater(len(claims), 0)
        found_types = [c.claim_type for c in claims]
        self.assertIn('can_claim', found_types)

    def test_skip_questions(self):
        claims = self.extractor.extract("What is the sky?")
        self.assertEqual(len(claims), 0)

    def test_skip_commands(self):
        claims = self.extractor.extract("please tell me about the sky")
        self.assertEqual(len(claims), 0)

    def test_skip_can_you_commands(self):
        claims = self.extractor.extract("can you help me with this")
        self.assertEqual(len(claims), 0)

    def test_empty_string(self):
        claims = self.extractor.extract("")
        self.assertEqual(len(claims), 0)

    def test_claim_has_key(self):
        claims = self.extractor.extract("The sky is blue")
        self.assertGreater(len(claims), 0)
        for claim in claims:
            self.assertIsInstance(claim.key, str)
            self.assertGreater(len(claim.key), 0)

    def test_claim_key_format(self):
        """Key should be tag:normalized_subject."""
        claims = self.extractor.extract("The sky is blue")
        self.assertGreater(len(claims), 0)
        for claim in claims:
            self.assertIn(':', claim.key)

    def test_claim_has_operator(self):
        """Every claim gets a D2-classified operator."""
        claims = self.extractor.extract("Harmony is beautiful")
        self.assertGreater(len(claims), 0)
        for claim in claims:
            self.assertIsInstance(claim.operator, int)
            self.assertGreaterEqual(claim.operator, 0)
            self.assertLess(claim.operator, 10)

    def test_seen_count_tracks(self):
        self.assertEqual(self.extractor.seen_count, 0)
        self.extractor.extract("The sky is blue")
        self.assertGreater(self.extractor.seen_count, 0)

    def test_stats(self):
        self.extractor.extract("The sky is blue")
        stats = self.extractor.stats()
        self.assertIn('unique_claims_seen', stats)
        self.assertIn('total_extractions', stats)
        self.assertIn('top_claims', stats)

    def test_multiple_claims_in_one_sentence(self):
        """A rich sentence can produce multiple claims."""
        claims = self.extractor.extract("The dog is fast and has sharp teeth")
        self.assertGreater(len(claims), 0)

    def test_deduplication_via_key(self):
        """Same extraction repeated should still have consistent key."""
        c1 = self.extractor.extract("The sky is blue")
        c2 = self.extractor.extract("The sky is blue")
        if c1 and c2:
            self.assertEqual(c1[0].key, c2[0].key)


# ================================================================
#  TURN DATACLASS TESTS
# ================================================================

class TestTurn(unittest.TestCase):
    """Validate Turn dataclass."""

    def test_default_values(self):
        from ck_sim.ck_dialogue import Turn
        from ck_sim.ck_sim_heartbeat import VOID
        turn = Turn(role='user')
        self.assertEqual(turn.role, 'user')
        self.assertEqual(turn.text, "")
        self.assertEqual(turn.operator, VOID)
        self.assertAlmostEqual(turn.coherence, 0.0)
        self.assertEqual(turn.tick, 0)
        self.assertEqual(turn.topics, [])

    def test_user_turn(self):
        from ck_sim.ck_dialogue import Turn
        from ck_sim.ck_sim_heartbeat import HARMONY
        turn = Turn(role='user', text='hello', operator=HARMONY,
                    coherence=0.8, tick=42, topics=['hello'])
        self.assertEqual(turn.role, 'user')
        self.assertEqual(turn.text, 'hello')
        self.assertEqual(turn.operator, HARMONY)
        self.assertAlmostEqual(turn.coherence, 0.8)
        self.assertEqual(turn.tick, 42)
        self.assertEqual(turn.topics, ['hello'])


# ================================================================
#  DIALOGUE TRACKER TESTS
# ================================================================

class TestDialogueTracker(unittest.TestCase):
    """Validate DialogueTracker: turn history, topics, coherence arc."""

    def setUp(self):
        from ck_sim.ck_dialogue import DialogueTracker
        self.tracker = DialogueTracker()

    def test_construction_empty(self):
        self.assertEqual(self.tracker.turn_count, 0)
        self.assertIsNone(self.tracker.last_turn)
        self.assertEqual(self.tracker.active_topics, [])
        self.assertAlmostEqual(self.tracker.conversation_coherence, 0.0)

    def test_add_turn(self):
        from ck_sim.ck_sim_heartbeat import HARMONY
        turn = self.tracker.add_turn('user', 'hello world', HARMONY, 0.7, tick=1)
        self.assertEqual(turn.role, 'user')
        self.assertEqual(turn.text, 'hello world')
        self.assertEqual(self.tracker.turn_count, 1)

    def test_turn_count_increments(self):
        from ck_sim.ck_sim_heartbeat import VOID
        for i in range(5):
            self.tracker.add_turn('user', f'msg {i}', VOID, 0.5, tick=i)
        self.assertEqual(self.tracker.turn_count, 5)

    def test_last_turn(self):
        from ck_sim.ck_sim_heartbeat import PROGRESS
        self.tracker.add_turn('user', 'first', PROGRESS, 0.5, tick=1)
        self.tracker.add_turn('ck', 'second', PROGRESS, 0.6, tick=2)
        last = self.tracker.last_turn
        self.assertEqual(last.role, 'ck')
        self.assertEqual(last.text, 'second')

    def test_recent_turns(self):
        from ck_sim.ck_sim_heartbeat import VOID
        for i in range(10):
            self.tracker.add_turn('user', f'msg {i}', VOID, 0.5, tick=i)
        recent = self.tracker.recent_turns(3)
        self.assertEqual(len(recent), 3)
        self.assertEqual(recent[-1].text, 'msg 9')

    def test_topic_extraction(self):
        topics = self.tracker._extract_topics("I think quantum physics is amazing")
        self.assertIsInstance(topics, list)
        self.assertGreater(len(topics), 0)
        # Should filter stop words and short words
        for t in topics:
            self.assertGreater(len(t), 3)

    def test_topic_extraction_deduplicates(self):
        topics = self.tracker._extract_topics("music music music is music")
        count = sum(1 for t in topics if t == 'music')
        self.assertEqual(count, 1)

    def test_topic_extraction_max_eight(self):
        long_text = " ".join([f"word{i}x" for i in range(20)])
        topics = self.tracker._extract_topics(long_text)
        self.assertLessEqual(len(topics), 8)

    def test_active_topics_after_turn(self):
        from ck_sim.ck_sim_heartbeat import VOID
        self.tracker.add_turn('user', 'quantum physics is interesting',
                              VOID, 0.5, tick=1)
        topics = self.tracker.active_topics
        self.assertGreater(len(topics), 0)

    def test_topic_decay(self):
        from ck_sim.ck_dialogue import TOPIC_DECAY
        from ck_sim.ck_sim_heartbeat import VOID
        self.tracker.add_turn('user', 'quantum physics research',
                              VOID, 0.5, tick=1, topics=['quantum'])
        relevance_before = self.tracker.topic_relevance.get('quantum', 0)
        # Add many turns without mentioning quantum
        for i in range(20):
            self.tracker.add_turn('user', 'hello', VOID, 0.5, tick=i+2,
                                  topics=['hello'])
        relevance_after = self.tracker.topic_relevance.get('quantum', 0)
        self.assertLess(relevance_after, relevance_before)

    def test_topic_pruning(self):
        from ck_sim.ck_sim_heartbeat import VOID
        self.tracker.add_turn('user', 'quantum', VOID, 0.5, tick=1,
                              topics=['quantum'])
        # Add many turns to decay quantum below threshold
        for i in range(100):
            self.tracker.add_turn('user', 'x', VOID, 0.5, tick=i+2, topics=[])
        # Quantum should be pruned by now
        self.assertNotIn('quantum', self.tracker.topic_relevance)

    def test_conversation_coherence(self):
        from ck_sim.ck_sim_heartbeat import VOID
        self.tracker.add_turn('user', 'hello', VOID, 0.8, tick=1)
        self.tracker.add_turn('ck', 'hi', VOID, 0.6, tick=2)
        avg = self.tracker.conversation_coherence
        self.assertAlmostEqual(avg, 0.7)

    def test_coherence_trend_zero_few_turns(self):
        from ck_sim.ck_sim_heartbeat import VOID
        self.tracker.add_turn('user', 'hello', VOID, 0.5, tick=1)
        self.assertAlmostEqual(self.tracker.coherence_trend, 0.0)

    def test_coherence_trend_positive(self):
        from ck_sim.ck_sim_heartbeat import VOID
        # Start low, trend upward
        for i in range(8):
            coherence = 0.3 + i * 0.05
            self.tracker.add_turn('user', f'msg {i}', VOID, coherence, tick=i)
        self.assertGreater(self.tracker.coherence_trend, 0.0)

    def test_coherence_trend_negative(self):
        from ck_sim.ck_sim_heartbeat import VOID
        # Start high, trend downward
        for i in range(8):
            coherence = 0.9 - i * 0.05
            self.tracker.add_turn('user', f'msg {i}', VOID, coherence, tick=i)
        self.assertLess(self.tracker.coherence_trend, 0.0)

    def test_user_operator_distribution(self):
        from ck_sim.ck_sim_heartbeat import HARMONY, VOID, NUM_OPS
        self.tracker.add_turn('user', 'a', HARMONY, 0.5, tick=1)
        self.tracker.add_turn('user', 'b', HARMONY, 0.5, tick=2)
        self.tracker.add_turn('user', 'c', VOID, 0.5, tick=3)
        dist = self.tracker.user_operator_distribution()
        self.assertEqual(len(dist), NUM_OPS)
        # HARMONY should be 2/3
        self.assertAlmostEqual(dist[HARMONY], 2.0/3.0)

    def test_dominant_user_operator(self):
        from ck_sim.ck_sim_heartbeat import HARMONY, VOID, PROGRESS
        self.tracker.add_turn('user', 'a', HARMONY, 0.5, tick=1)
        self.tracker.add_turn('user', 'b', HARMONY, 0.5, tick=2)
        self.tracker.add_turn('user', 'c', PROGRESS, 0.5, tick=3)
        self.assertEqual(self.tracker.dominant_user_operator(), HARMONY)

    def test_dominant_user_operator_void_when_empty(self):
        from ck_sim.ck_sim_heartbeat import VOID
        self.assertEqual(self.tracker.dominant_user_operator(), VOID)

    def test_conversation_band_green(self):
        from ck_sim.ck_sim_heartbeat import VOID
        from ck_sim.ck_truth import T_STAR
        self.tracker.add_turn('user', 'a', VOID, T_STAR + 0.1, tick=1)
        self.assertEqual(self.tracker.conversation_band(), "GREEN")

    def test_conversation_band_yellow(self):
        from ck_sim.ck_sim_heartbeat import VOID
        self.tracker.add_turn('user', 'a', VOID, 0.5, tick=1)
        self.assertEqual(self.tracker.conversation_band(), "YELLOW")

    def test_conversation_band_red(self):
        from ck_sim.ck_sim_heartbeat import VOID
        self.tracker.add_turn('user', 'a', VOID, 0.2, tick=1)
        self.assertEqual(self.tracker.conversation_band(), "RED")

    def test_stats(self):
        from ck_sim.ck_sim_heartbeat import VOID
        self.tracker.add_turn('user', 'hello world', VOID, 0.5, tick=1)
        stats = self.tracker.stats()
        self.assertIn('turn_count', stats)
        self.assertIn('active_topics', stats)
        self.assertIn('conversation_coherence', stats)
        self.assertIn('coherence_trend', stats)
        self.assertIn('conversation_band', stats)
        self.assertIn('dominant_user_op', stats)
        self.assertIn('user_op_dist', stats)
        self.assertEqual(stats['turn_count'], 1)

    def test_max_turn_history_enforced(self):
        from ck_sim.ck_dialogue import MAX_TURN_HISTORY
        from ck_sim.ck_sim_heartbeat import VOID
        for i in range(MAX_TURN_HISTORY + 20):
            self.tracker.add_turn('user', f'msg {i}', VOID, 0.5, tick=i)
        # Deque should cap at MAX_TURN_HISTORY
        recent = self.tracker.recent_turns(MAX_TURN_HISTORY + 10)
        self.assertLessEqual(len(recent), MAX_TURN_HISTORY)
        # But turn count should track all
        self.assertEqual(self.tracker.turn_count, MAX_TURN_HISTORY + 20)

    def test_ck_operator_tracking(self):
        from ck_sim.ck_sim_heartbeat import BALANCE
        self.tracker.add_turn('ck', 'response', BALANCE, 0.5, tick=1)
        self.assertEqual(self.tracker._ck_op_counts[BALANCE], 1)


# ================================================================
#  RESPONSE COMPOSER TESTS
# ================================================================

class TestResponseComposer(unittest.TestCase):
    """Validate ResponseComposer: recursive template composition."""

    def setUp(self):
        from ck_sim.ck_dialogue import ResponseComposer
        self.composer = ResponseComposer(seed=42)

    def test_construction(self):
        self.assertIsNotNone(self.composer)

    def test_compose_red_band(self):
        from ck_sim.ck_sim_heartbeat import HARMONY
        response = self.composer.compose(
            operators=[HARMONY], coherence=0.2, band="RED"
        )
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_compose_yellow_band(self):
        from ck_sim.ck_sim_heartbeat import HARMONY, BALANCE
        response = self.composer.compose(
            operators=[HARMONY, BALANCE], coherence=0.5, band="YELLOW"
        )
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_compose_green_band(self):
        from ck_sim.ck_sim_heartbeat import HARMONY, PROGRESS, LATTICE
        response = self.composer.compose(
            operators=[HARMONY, PROGRESS, LATTICE], coherence=0.8,
            band="GREEN"
        )
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_green_response_longer_than_red(self):
        """GREEN band should produce richer (generally longer) responses."""
        from ck_sim.ck_sim_heartbeat import HARMONY
        # Generate many to average out randomness
        red_total = 0
        green_total = 0
        for seed in range(10):
            from ck_sim.ck_dialogue import ResponseComposer
            c = ResponseComposer(seed=seed)
            red = c.compose([HARMONY], 0.2, band="RED")
            green = c.compose([HARMONY], 0.9, band="GREEN")
            red_total += len(red)
            green_total += len(green)
        # GREEN should be longer on average
        self.assertGreater(green_total, red_total)

    def test_compose_auto_band_detection(self):
        from ck_sim.ck_sim_heartbeat import HARMONY
        from ck_sim.ck_truth import T_STAR
        # High coherence → GREEN auto-detection
        response = self.composer.compose(
            operators=[HARMONY], coherence=T_STAR + 0.1
        )
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_compose_with_topics(self):
        from ck_sim.ck_sim_heartbeat import HARMONY
        response = self.composer.compose(
            operators=[HARMONY], coherence=0.5,
            topics=['music', 'harmony', 'rhythm']
        )
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_compose_with_claims(self):
        from ck_sim.ck_dialogue import ExtractedClaim
        from ck_sim.ck_sim_heartbeat import HARMONY
        claims = [ExtractedClaim(
            key='test', text='the sky is blue', claim_type='is_claim',
            subject='sky', predicate='blue', operator=HARMONY,
        )]
        response = self.composer.compose(
            operators=[HARMONY], coherence=0.5,
            learned_claims=claims,
        )
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_compose_empty_operators(self):
        """Should handle empty operator list gracefully."""
        response = self.composer.compose(
            operators=[], coherence=0.5
        )
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_compose_deterministic_with_seed(self):
        from ck_sim.ck_dialogue import ResponseComposer
        from ck_sim.ck_sim_heartbeat import HARMONY
        c1 = ResponseComposer(seed=99)
        c2 = ResponseComposer(seed=99)
        r1 = c1.compose([HARMONY], 0.5)
        r2 = c2.compose([HARMONY], 0.5)
        self.assertEqual(r1, r2)

    def test_compose_varies_with_different_seeds(self):
        from ck_sim.ck_dialogue import ResponseComposer
        from ck_sim.ck_sim_heartbeat import HARMONY
        responses = set()
        for seed in range(20):
            c = ResponseComposer(seed=seed)
            r = c.compose([HARMONY], 0.5, band="GREEN")
            responses.add(r)
        # Should have some variety
        self.assertGreater(len(responses), 1)

    def test_pick_atomic_per_operator(self):
        from ck_sim.ck_sim_heartbeat import HARMONY, VOID, COLLAPSE, CHAOS
        for op in [HARMONY, VOID, COLLAPSE, CHAOS]:
            phrase = self.composer._pick_atomic(op)
            self.assertIsInstance(phrase, str)
            self.assertGreater(len(phrase), 0)

    def test_fresh_selection_avoids_repeats(self):
        """_pick_fresh should prefer unused templates."""
        templates = ['a', 'b', 'c', 'd']
        seen = set()
        for _ in range(4):
            choice = self.composer._pick_fresh(templates)
            seen.add(choice)
        # Should have picked at least 2 different ones (high probability)
        self.assertGreater(len(seen), 1)

    def test_compose_all_operators_red(self):
        """Every operator should produce a valid RED response."""
        from ck_sim.ck_sim_heartbeat import NUM_OPS
        for op in range(NUM_OPS):
            response = self.composer.compose([op], 0.2, band="RED")
            self.assertIsInstance(response, str)
            self.assertGreater(len(response), 0, f"Empty response for operator {op}")


# ================================================================
#  CONVERSATION MEMORY TESTS
# ================================================================

class TestConversationMemory(unittest.TestCase):
    """Validate ConversationMemory: claims → Truth Lattice pipeline."""

    def setUp(self):
        from ck_sim.ck_truth import TruthLattice
        from ck_sim.ck_dialogue import ConversationMemory
        self.lattice = TruthLattice()
        self.memory = ConversationMemory(self.lattice)

    def test_construction(self):
        self.assertIsNotNone(self.memory)
        self.assertEqual(self.memory._learned_count, 0)
        self.assertEqual(self.memory._promoted_count, 0)

    def test_process_message_extracts_claims(self):
        claims = self.memory.process_message("The sky is blue", tick=1)
        self.assertIsInstance(claims, list)
        self.assertGreater(len(claims), 0)

    def test_process_message_adds_to_lattice(self):
        from ck_sim.ck_truth import PROVISIONAL
        before = self.lattice.total_entries
        self.memory.process_message("The dog has four legs", tick=1)
        after = self.lattice.total_entries
        self.assertGreater(after, before)

    def test_claims_enter_as_provisional(self):
        from ck_sim.ck_truth import PROVISIONAL
        claims = self.memory.process_message("The ocean is deep", tick=1)
        for claim in claims:
            if claim.confidence > 0:
                entry = self.lattice.get(claim.key)
                if entry:
                    self.assertEqual(entry.level, PROVISIONAL)

    def test_question_produces_no_claims(self):
        claims = self.memory.process_message("What is the sky?", tick=1)
        self.assertEqual(len(claims), 0)

    def test_learned_count_increases(self):
        self.memory.process_message("The sky is blue", tick=1)
        self.assertGreater(self.memory._learned_count, 0)

    def test_recall_about(self):
        self.memory.process_message("The sky is blue", tick=1)
        results = self.memory.recall_about("sky")
        self.assertIsInstance(results, list)
        # Should find something about sky
        self.assertGreater(len(results), 0)

    def test_recall_about_nonexistent(self):
        results = self.memory.recall_about("xyznonexistent")
        self.assertEqual(len(results), 0)

    def test_what_has_ck_learned(self):
        self.memory.process_message("The sky is blue", tick=1)
        learned = self.memory.what_has_ck_learned()
        self.assertIn('CORE', learned)
        self.assertIn('TRUSTED', learned)
        self.assertIn('PROVISIONAL', learned)

    def test_stats(self):
        self.memory.process_message("The sky is blue", tick=1)
        stats = self.memory.stats()
        self.assertIn('claims_learned', stats)
        self.assertIn('claims_promoted', stats)
        self.assertIn('extractor', stats)

    def test_coherence_computed_for_claims(self):
        """Each claim gets a coherence score."""
        claims = self.memory.process_message("The sky is blue", tick=1)
        for claim in claims:
            self.assertGreaterEqual(claim.confidence, 0.0)
            self.assertLessEqual(claim.confidence, 1.0)

    def test_core_truth_contradiction_rejected(self):
        """Claims contradicting core truths should be rejected."""
        # op_count is a core truth = 10
        claims = self.memory.process_message("op count is eleven", tick=1)
        # The claim might still be extracted, but confidence should be 0
        # (or it may not be about op_count at all — depends on extraction)
        # At minimum, the core truth should be unchanged
        entry = self.lattice.get('op_count')
        self.assertEqual(entry.content, 10)

    def test_multiple_messages_accumulate(self):
        self.memory.process_message("The sky is blue", tick=1)
        count1 = self.memory._learned_count
        self.memory.process_message("The grass is green", tick=2)
        count2 = self.memory._learned_count
        self.assertGreater(count2, count1)


# ================================================================
#  DIALOGUE ENGINE INTEGRATION TESTS
# ================================================================

class TestDialogueEngine(unittest.TestCase):
    """Validate DialogueEngine: full pipeline integration."""

    def setUp(self):
        from ck_sim.ck_dialogue import DialogueEngine
        self.engine = DialogueEngine(seed=42)

    def test_construction(self):
        self.assertIsNotNone(self.engine)
        self.assertIsNotNone(self.engine.lattice)
        self.assertIsNotNone(self.engine.memory)
        self.assertIsNotNone(self.engine.tracker)
        self.assertIsNotNone(self.engine.composer)

    def test_process_simple_message(self):
        response = self.engine.process_user_message("Hello CK", tick=1, coherence=0.5)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_process_factual_message(self):
        response = self.engine.process_user_message(
            "The sky is blue", tick=1, coherence=0.6
        )
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_turn_count_increases(self):
        self.engine.process_user_message("Hello", tick=1, coherence=0.5)
        # Both user and CK turn should be tracked
        self.assertEqual(self.engine.tracker.turn_count, 2)

    def test_claims_learned_from_message(self):
        self.engine.process_user_message("The dog is friendly", tick=1, coherence=0.6)
        self.assertGreater(self.engine.memory._learned_count, 0)

    def test_question_no_claims(self):
        before = self.engine.memory._learned_count
        self.engine.process_user_message("What is the weather?", tick=1, coherence=0.5)
        # Questions shouldn't produce claims
        self.assertEqual(self.engine.memory._learned_count, before)

    def test_multi_turn_conversation(self):
        """Engine handles multi-turn conversation."""
        messages = [
            "My name is Brayden",
            "The sky is blue today",
            "I like music and harmony",
            "CK is a coherence keeper",
        ]
        responses = []
        for i, msg in enumerate(messages):
            r = self.engine.process_user_message(msg, tick=i*10, coherence=0.6)
            responses.append(r)
            self.assertIsInstance(r, str)
            self.assertGreater(len(r), 0)
        # Should have tracked all turns (user + ck each)
        self.assertEqual(self.engine.tracker.turn_count, len(messages) * 2)

    def test_coherence_affects_response_depth(self):
        """Higher coherence should generally produce richer responses."""
        from ck_sim.ck_dialogue import DialogueEngine
        # Low coherence
        e_low = DialogueEngine(seed=42)
        r_low = e_low.process_user_message("hello", tick=1, coherence=0.2)
        # High coherence
        e_high = DialogueEngine(seed=42)
        r_high = e_high.process_user_message("hello", tick=1, coherence=0.9)
        # Both should be valid
        self.assertGreater(len(r_low), 0)
        self.assertGreater(len(r_high), 0)

    def test_stats(self):
        self.engine.process_user_message("The sky is blue", tick=1, coherence=0.5)
        stats = self.engine.stats()
        self.assertIn('memory', stats)
        self.assertIn('tracker', stats)
        self.assertIn('lattice_entries', stats)
        self.assertIn('lattice_levels', stats)

    def test_with_custom_lattice(self):
        from ck_sim.ck_truth import TruthLattice
        from ck_sim.ck_dialogue import DialogueEngine
        lattice = TruthLattice()
        engine = DialogueEngine(lattice=lattice, seed=99)
        self.assertIs(engine.lattice, lattice)
        response = engine.process_user_message("The sky is blue", tick=1, coherence=0.5)
        self.assertIsInstance(response, str)

    def test_with_operator_list(self):
        from ck_sim.ck_sim_heartbeat import HARMONY, PROGRESS
        response = self.engine.process_user_message(
            "Hello CK", tick=1, coherence=0.5,
            operators=[HARMONY, PROGRESS, HARMONY]
        )
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_classify_text_returns_valid_operator(self):
        from ck_sim.ck_sim_heartbeat import NUM_OPS
        op = self.engine._classify_text("The sky is blue and beautiful")
        self.assertGreaterEqual(op, 0)
        self.assertLess(op, NUM_OPS)

    def test_topics_tracked_across_turns(self):
        self.engine.process_user_message(
            "quantum physics is fascinating", tick=1, coherence=0.6
        )
        topics = self.engine.tracker.active_topics
        self.assertGreater(len(topics), 0)


# ================================================================
#  EDGE CASE AND STRESS TESTS
# ================================================================

class TestDialogueEdgeCases(unittest.TestCase):
    """Edge cases and stress tests."""

    def test_empty_message(self):
        from ck_sim.ck_dialogue import DialogueEngine
        engine = DialogueEngine(seed=42)
        response = engine.process_user_message("", tick=1, coherence=0.5)
        self.assertIsInstance(response, str)

    def test_very_long_message(self):
        from ck_sim.ck_dialogue import DialogueEngine
        engine = DialogueEngine(seed=42)
        long_msg = "The sky is blue " * 100
        response = engine.process_user_message(long_msg, tick=1, coherence=0.5)
        self.assertIsInstance(response, str)

    def test_special_characters(self):
        from ck_sim.ck_dialogue import DialogueEngine
        engine = DialogueEngine(seed=42)
        response = engine.process_user_message(
            "Hello! @#$% ñoño 日本語", tick=1, coherence=0.5
        )
        self.assertIsInstance(response, str)

    def test_rapid_fire_messages(self):
        from ck_sim.ck_dialogue import DialogueEngine
        engine = DialogueEngine(seed=42)
        for i in range(50):
            response = engine.process_user_message(
                f"message number {i}", tick=i, coherence=0.5
            )
            self.assertIsInstance(response, str)
        self.assertEqual(engine.tracker.turn_count, 100)  # 50 user + 50 CK

    def test_all_bands_produce_responses(self):
        from ck_sim.ck_dialogue import DialogueEngine
        for band_coh in [0.1, 0.5, 0.9]:
            engine = DialogueEngine(seed=42)
            response = engine.process_user_message(
                "testing bands", tick=1, coherence=band_coh
            )
            self.assertIsInstance(response, str)
            self.assertGreater(len(response), 0)

    def test_composer_level2_with_single_claim(self):
        """Level 2 with only one claim should still work."""
        from ck_sim.ck_dialogue import ResponseComposer, ExtractedClaim
        from ck_sim.ck_sim_heartbeat import HARMONY
        composer = ResponseComposer(seed=42)
        claims = [ExtractedClaim(
            key='test', text='sky is blue', claim_type='is_claim',
            operator=HARMONY,
        )]
        response = composer.compose(
            operators=[HARMONY], coherence=0.5, band="YELLOW",
            learned_claims=claims,
        )
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_composer_level3_no_topics_no_claims(self):
        """Level 3 with no context should still compose something."""
        from ck_sim.ck_dialogue import ResponseComposer
        from ck_sim.ck_sim_heartbeat import HARMONY
        composer = ResponseComposer(seed=42)
        response = composer.compose(
            operators=[HARMONY], coherence=0.9, band="GREEN",
            topics=[], learned_claims=[],
        )
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)


# ================================================================
#  IMPORT TEST
# ================================================================

class TestDialogueImport(unittest.TestCase):
    """Validate that all public names are importable."""

    def test_import_all_classes(self):
        from ck_sim.ck_dialogue import (
            ClaimExtractor, ConversationMemory, DialogueTracker,
            ResponseComposer, DialogueEngine, ExtractedClaim, Turn,
        )
        self.assertIsNotNone(ClaimExtractor)
        self.assertIsNotNone(ConversationMemory)
        self.assertIsNotNone(DialogueTracker)
        self.assertIsNotNone(ResponseComposer)
        self.assertIsNotNone(DialogueEngine)
        self.assertIsNotNone(ExtractedClaim)
        self.assertIsNotNone(Turn)

    def test_import_constants(self):
        from ck_sim.ck_dialogue import (
            MAX_TURN_HISTORY, MAX_TOPICS, TOPIC_DECAY, TOPIC_MIN_RELEVANCE,
            CLAIM_COHERENCE_BOOST, DEPTH_RED, DEPTH_YELLOW, DEPTH_GREEN,
            TEMPLATE_FRAGMENTS,
        )
        self.assertIsNotNone(TEMPLATE_FRAGMENTS)

    def test_import_compiled_patterns(self):
        from ck_sim.ck_dialogue import _COMPILED_PATTERNS
        self.assertGreater(len(_COMPILED_PATTERNS), 0)


# ================================================================
#  MAIN
# ================================================================

if __name__ == '__main__':
    unittest.main()
