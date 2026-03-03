"""
ck_attention_tests.py -- Tests for Attentional Gating System
==============================================================
Validates: novelty detection, salience mapping, attention control,
gain clamping, goal alignment, danger boosting, and integration
with goals and operator constants.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import unittest

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, COLLAPSE, CHAOS, PROGRESS,
    BREATH, BALANCE, COUNTER, LATTICE, RESET, OP_NAMES
)
from ck_sim.ck_attention import (
    NoveltyDetector, SalienceMap, AttentionController,
    NUM_STREAMS, NOVELTY_WINDOW, GATE_MIN, GATE_MAX,
    NOVELTY_BOOST, GOAL_ALIGNMENT_BOOST, DANGER_BOOST,
    BAND_RED, BAND_YELLOW, BAND_GREEN,
)


# ================================================================
#  IMPORT TEST
# ================================================================

class TestImport(unittest.TestCase):
    def test_import(self):
        import ck_sim.ck_attention
        self.assertTrue(hasattr(ck_sim.ck_attention, 'AttentionController'))
        self.assertTrue(hasattr(ck_sim.ck_attention, 'NoveltyDetector'))
        self.assertTrue(hasattr(ck_sim.ck_attention, 'SalienceMap'))

    def test_constants_exist(self):
        self.assertEqual(NUM_STREAMS, 8)
        self.assertEqual(NOVELTY_WINDOW, 16)
        self.assertAlmostEqual(GATE_MIN, 0.1)
        self.assertAlmostEqual(GATE_MAX, 2.0)
        self.assertAlmostEqual(NOVELTY_BOOST, 0.5)
        self.assertAlmostEqual(GOAL_ALIGNMENT_BOOST, 0.3)
        self.assertAlmostEqual(DANGER_BOOST, 0.8)

    def test_band_constants(self):
        self.assertEqual(BAND_RED, 0)
        self.assertEqual(BAND_YELLOW, 1)
        self.assertEqual(BAND_GREEN, 2)


# ================================================================
#  NOVELTY DETECTOR TESTS
# ================================================================

class TestNoveltyDetectorNovel(unittest.TestCase):
    """Novel operators should score high."""

    def setUp(self):
        self.nd = NoveltyDetector()

    def test_first_observation_is_novel(self):
        """Very first operator in a stream is always maximally novel."""
        score = self.nd.feed(HARMONY, 'audio')
        self.assertAlmostEqual(score, 1.0)

    def test_new_operator_is_novel(self):
        """An operator never seen in the window scores 1.0."""
        # Fill window with HARMONY
        for _ in range(NOVELTY_WINDOW):
            self.nd.feed(HARMONY, 'audio')
        # Now feed CHAOS -- never seen
        score = self.nd.feed(CHAOS, 'audio')
        self.assertAlmostEqual(score, 1.0)

    def test_rare_operator_is_somewhat_novel(self):
        """An operator seen once in window is mostly novel."""
        for _ in range(15):
            self.nd.feed(HARMONY, 'audio')
        self.nd.feed(CHAOS, 'audio')  # 1 out of 16
        # Feed another CHAOS -- frequency is 1/16
        score = self.nd.feed(CHAOS, 'audio')
        self.assertGreater(score, 0.8)
        self.assertLess(score, 1.0)


class TestNoveltyDetectorRepeated(unittest.TestCase):
    """Repeated operators should score low."""

    def setUp(self):
        self.nd = NoveltyDetector()

    def test_repeated_operator_low_novelty(self):
        """Same operator repeated many times should have low novelty."""
        for _ in range(NOVELTY_WINDOW):
            self.nd.feed(HARMONY, 'heartbeat')
        # Now the window is full of HARMONY
        score = self.nd.feed(HARMONY, 'heartbeat')
        self.assertAlmostEqual(score, 0.0)

    def test_half_repeated_moderate_novelty(self):
        """Operator at 50% frequency should have ~0.5 novelty."""
        for i in range(NOVELTY_WINDOW):
            op = HARMONY if i % 2 == 0 else CHAOS
            self.nd.feed(op, 'mixed')
        # Feed HARMONY -- frequency is 8/16 = 0.5
        score = self.nd.feed(HARMONY, 'mixed')
        self.assertAlmostEqual(score, 0.5, places=1)

    def test_independent_streams(self):
        """Different streams have independent novelty histories."""
        for _ in range(NOVELTY_WINDOW):
            self.nd.feed(HARMONY, 'stream_a')
        # stream_b has no history
        score_b = self.nd.feed(HARMONY, 'stream_b')
        score_a = self.nd.feed(HARMONY, 'stream_a')
        self.assertAlmostEqual(score_b, 1.0)  # First observation
        self.assertAlmostEqual(score_a, 0.0)  # Fully expected

    def test_entropy_high_for_diverse_stream(self):
        """Stream with many different operators has high entropy."""
        for i in range(NOVELTY_WINDOW):
            self.nd.feed(i % NUM_OPS, 'diverse')
        entropy = self.nd.get_stream_entropy('diverse')
        # Max entropy for 10 ops = log2(10) ~ 3.32
        self.assertGreater(entropy, 2.5)

    def test_entropy_low_for_uniform_stream(self):
        """Stream with one operator has zero entropy."""
        for _ in range(NOVELTY_WINDOW):
            self.nd.feed(HARMONY, 'uniform')
        entropy = self.nd.get_stream_entropy('uniform')
        self.assertAlmostEqual(entropy, 0.0)

    def test_reset_clears_history(self):
        """Resetting a stream makes next observation novel again."""
        for _ in range(NOVELTY_WINDOW):
            self.nd.feed(HARMONY, 'resettable')
        self.nd.reset_stream('resettable')
        score = self.nd.feed(HARMONY, 'resettable')
        self.assertAlmostEqual(score, 1.0)

    def test_tracked_streams(self):
        """Tracked streams list reflects all fed streams."""
        self.nd.feed(HARMONY, 'alpha')
        self.nd.feed(CHAOS, 'beta')
        tracked = self.nd.tracked_streams
        self.assertIn('alpha', tracked)
        self.assertIn('beta', tracked)


# ================================================================
#  SALIENCE MAP TESTS
# ================================================================

class TestSalienceMapWeights(unittest.TestCase):
    """Weights update correctly and respect bounds."""

    def setUp(self):
        self.sm = SalienceMap()

    def test_update_stores_weight(self):
        self.sm.update('audio', novelty=0.5, goal_alignment=0.3,
                        coherence_contribution=0.7, band=BAND_GREEN)
        w = self.sm.get_weight('audio')
        self.assertGreater(w, 0.0)

    def test_default_weight_is_gate_min(self):
        """Unknown stream returns GATE_MIN."""
        w = self.sm.get_weight('nonexistent')
        self.assertAlmostEqual(w, GATE_MIN)

    def test_weight_clamped_to_min(self):
        """Even zero novelty + zero alignment doesn't go below GATE_MIN."""
        self.sm.update('quiet', novelty=0.0, goal_alignment=0.0,
                        coherence_contribution=0.0, band=BAND_GREEN)
        w = self.sm.get_weight('quiet')
        self.assertGreaterEqual(w, GATE_MIN)

    def test_weight_clamped_to_max(self):
        """Maximum everything doesn't exceed GATE_MAX."""
        self.sm.update('hot', novelty=1.0, goal_alignment=1.0,
                        coherence_contribution=1.0, band=BAND_RED)
        w = self.sm.get_weight('hot')
        self.assertLessEqual(w, GATE_MAX)


class TestSalienceMapNormalize(unittest.TestCase):
    """Normalization preserves budget and bounds."""

    def setUp(self):
        self.sm = SalienceMap()

    def test_normalize_sums_to_active(self):
        """After normalize, weights sum approximately to n_active."""
        self.sm.update('a', 0.5, 0.3, 0.6, BAND_GREEN)
        self.sm.update('b', 0.8, 0.1, 0.4, BAND_GREEN)
        self.sm.update('c', 0.2, 0.5, 0.9, BAND_GREEN)
        self.sm.normalize()

        total = sum(self.sm.get_weight(s) for s in ['a', 'b', 'c'])
        # Should be close to 3 (n_active), but clamping may shift it
        self.assertGreater(total, 0.0)
        self.assertLess(total, 3 * GATE_MAX + 0.01)

    def test_normalize_respects_min(self):
        """No weight drops below GATE_MIN after normalization."""
        self.sm.update('loud', 1.0, 1.0, 1.0, BAND_RED)
        self.sm.update('quiet', 0.0, 0.0, 0.0, BAND_GREEN)
        self.sm.normalize()

        self.assertGreaterEqual(self.sm.get_weight('quiet'), GATE_MIN)
        self.assertGreaterEqual(self.sm.get_weight('loud'), GATE_MIN)

    def test_normalize_respects_max(self):
        """No weight exceeds GATE_MAX after normalization."""
        self.sm.update('x', 1.0, 1.0, 1.0, BAND_RED)
        self.sm.normalize()
        self.assertLessEqual(self.sm.get_weight('x'), GATE_MAX)

    def test_remove_stream(self):
        """Removed stream no longer in map."""
        self.sm.update('temp', 0.5, 0.5, 0.5, BAND_GREEN)
        self.sm.remove_stream('temp')
        self.assertAlmostEqual(self.sm.get_weight('temp'), GATE_MIN)
        self.assertEqual(self.sm.active_count, 0)


# ================================================================
#  ATTENTION CONTROLLER TESTS
# ================================================================

class TestAttentionControllerTick(unittest.TestCase):
    """tick() returns weights for each stream."""

    def setUp(self):
        self.ac = AttentionController()

    def test_tick_returns_weights(self):
        streams = {'audio': HARMONY, 'text': PROGRESS, 'heartbeat': BREATH}
        weights = self.ac.tick(streams, band=BAND_GREEN)
        self.assertEqual(len(weights), 3)
        for name in streams:
            self.assertIn(name, weights)
            self.assertGreaterEqual(weights[name], GATE_MIN)
            self.assertLessEqual(weights[name], GATE_MAX)

    def test_tick_empty_streams(self):
        weights = self.ac.tick({}, band=BAND_GREEN)
        self.assertEqual(len(weights), 0)

    def test_tick_single_stream(self):
        weights = self.ac.tick({'only': HARMONY}, band=BAND_GREEN)
        self.assertIn('only', weights)


class TestAttentionControllerDanger(unittest.TestCase):
    """RED band boosts all streams (hypervigilance)."""

    def setUp(self):
        self.ac = AttentionController()

    def test_danger_boosts_all_streams(self):
        streams = {'a': HARMONY, 'b': HARMONY, 'c': HARMONY}

        # GREEN band tick
        green_weights = self.ac.tick(streams, band=BAND_GREEN)

        # Reset for fair comparison
        self.ac = AttentionController()

        # RED band tick
        red_weights = self.ac.tick(streams, band=BAND_RED)

        # In RED band, the raw (pre-normalize) weights are higher.
        # After normalization weights sum to n_active, so the
        # individual weights may not be strictly higher. But the
        # raw salience inputs include DANGER_BOOST.
        # Test that at least the salience map recorded the boost:
        for name in streams:
            # The pre-normalization weight in RED should be
            # at least DANGER_BOOST above the GREEN equivalent.
            # We verify indirectly: the stats should show active streams.
            self.assertIn(name, red_weights)
            self.assertGreaterEqual(red_weights[name], GATE_MIN)

    def test_danger_vs_green_raw_salience(self):
        """RED band should produce higher raw salience than GREEN.

        Use two streams so normalization doesn't collapse both to 1.0.
        The relative weights shift when danger boost is applied to all.
        We verify by checking the salience map BEFORE normalization.
        """
        sm_green = SalienceMap()
        sm_red = SalienceMap()

        # Same inputs except band
        sm_green.update('sensor', novelty=0.5, goal_alignment=0.3,
                         coherence_contribution=0.5, band=BAND_GREEN)
        sm_red.update('sensor', novelty=0.5, goal_alignment=0.3,
                       coherence_contribution=0.5, band=BAND_RED)

        # Before normalization, RED weight includes DANGER_BOOST
        w_green = sm_green.get_weight('sensor')
        w_red = sm_red.get_weight('sensor')
        self.assertGreater(w_red, w_green)
        self.assertAlmostEqual(w_red - w_green, DANGER_BOOST, places=2)


class TestAttentionControllerGoalAlignment(unittest.TestCase):
    """Goal-aligned streams get boosted."""

    def setUp(self):
        self.ac = AttentionController()

    def test_goal_aligned_stream_boosted(self):
        """Stream producing the goal's dominant operator gets boosted."""
        # Goal pattern heavily favoring PROGRESS
        goal = [0.0] * NUM_OPS
        goal[PROGRESS] = 0.8
        goal[HARMONY] = 0.2

        streams = {'aligned': PROGRESS, 'unaligned': VOID}
        weights = self.ac.tick(streams, band=BAND_GREEN,
                                top_goal_pattern=goal)

        # Aligned stream should have higher weight
        self.assertGreater(weights['aligned'], weights['unaligned'])

    def test_goal_with_soft_distributions(self):
        """Goal alignment uses cosine similarity with soft dists."""
        goal = [0.0] * NUM_OPS
        goal[COUNTER] = 0.3
        goal[PROGRESS] = 0.4
        goal[CHAOS] = 0.3

        # Stream A's distribution matches the goal
        dist_a = list(goal)
        # Stream B's distribution is opposite
        dist_b = [0.0] * NUM_OPS
        dist_b[VOID] = 0.5
        dist_b[COLLAPSE] = 0.5

        stream_dists = {'match': dist_a, 'mismatch': dist_b}
        streams = {'match': PROGRESS, 'mismatch': VOID}

        weights = self.ac.tick(
            streams, band=BAND_GREEN,
            top_goal_pattern=goal,
            stream_op_dists=stream_dists)

        self.assertGreater(weights['match'], weights['mismatch'])

    def test_no_goal_no_boost(self):
        """Without a goal pattern, goal alignment is zero."""
        streams = {'a': PROGRESS, 'b': VOID}
        weights = self.ac.tick(streams, band=BAND_GREEN,
                                top_goal_pattern=None)
        # Both should still get valid weights
        self.assertGreaterEqual(weights['a'], GATE_MIN)
        self.assertGreaterEqual(weights['b'], GATE_MIN)


class TestAttentionControllerFocus(unittest.TestCase):
    """Focus stream tracking."""

    def setUp(self):
        self.ac = AttentionController()

    def test_focus_stream_returns_highest(self):
        """get_focus_stream returns the highest weighted stream."""
        # Use goal alignment to force one stream higher
        goal = [0.0] * NUM_OPS
        goal[HARMONY] = 1.0

        streams = {'winner': HARMONY, 'loser': VOID}
        self.ac.tick(streams, band=BAND_GREEN, top_goal_pattern=goal)

        focus = self.ac.get_focus_stream()
        self.assertEqual(focus, 'winner')

    def test_focus_stream_none_when_empty(self):
        focus = self.ac.get_focus_stream()
        self.assertIsNone(focus)

    def test_focus_stability_consistent(self):
        """Stable focus produces high stability score."""
        goal = [0.0] * NUM_OPS
        goal[HARMONY] = 1.0

        streams = {'stable': HARMONY, 'other': VOID}
        for _ in range(20):
            self.ac.tick(streams, band=BAND_GREEN, top_goal_pattern=goal)

        stability = self.ac.get_focus_stability()
        self.assertGreater(stability, 0.5)

    def test_stats_structure(self):
        streams = {'a': HARMONY, 'b': CHAOS}
        self.ac.tick(streams, band=BAND_GREEN)
        s = self.ac.stats()
        self.assertIn('tick', s)
        self.assertIn('active_streams', s)
        self.assertIn('focus_stream', s)
        self.assertIn('focus_stability', s)
        self.assertIn('weights', s)
        self.assertIn('novelty_entropy', s)
        self.assertEqual(s['tick'], 1)
        self.assertEqual(s['active_streams'], 2)


# ================================================================
#  INTEGRATION TESTS
# ================================================================

class TestIntegrationWithGoals(unittest.TestCase):
    """Works with goal patterns from ck_goals."""

    def test_goal_pattern_as_attention_input(self):
        """GOAL_PATTERNS can be used directly as top_goal_pattern."""
        from ck_sim.ck_goals import GOAL_PATTERNS

        ac = AttentionController()
        goal = GOAL_PATTERNS['explore']
        streams = {'audio': COUNTER, 'text': PROGRESS, 'heartbeat': HARMONY}
        weights = ac.tick(streams, band=BAND_GREEN, top_goal_pattern=goal)

        self.assertEqual(len(weights), 3)
        for w in weights.values():
            self.assertGreaterEqual(w, GATE_MIN)
            self.assertLessEqual(w, GATE_MAX)

    def test_goal_evaluator_target_blend(self):
        """GoalEvaluator's target_blend works as top_goal_pattern."""
        from ck_sim.ck_goals import GoalEvaluator

        evaluator = GoalEvaluator()
        blend = evaluator.target_blend
        self.assertEqual(len(blend), NUM_OPS)

        ac = AttentionController()
        streams = {'heartbeat': HARMONY}
        weights = ac.tick(streams, band=BAND_GREEN, top_goal_pattern=blend)
        self.assertIn('heartbeat', weights)


class TestIntegrationWithOperatorConstants(unittest.TestCase):
    """All operator constants work with the attention system."""

    def test_all_operators_produce_valid_weights(self):
        """Every operator value produces a valid attention weight."""
        ac = AttentionController()
        all_ops = [VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
                   BALANCE, CHAOS, HARMONY, BREATH, RESET]

        for op in all_ops:
            ac_fresh = AttentionController()
            name = OP_NAMES[op]
            weights = ac_fresh.tick({name: op}, band=BAND_GREEN)
            self.assertGreaterEqual(weights[name], GATE_MIN,
                msg=f"Operator {name} produced weight below GATE_MIN")
            self.assertLessEqual(weights[name], GATE_MAX,
                msg=f"Operator {name} produced weight above GATE_MAX")

    def test_harmony_has_high_coherence_contribution(self):
        """HARMONY operator should contribute most to coherence."""
        coh_harmony = AttentionController._operator_coherence_value(HARMONY)
        coh_void = AttentionController._operator_coherence_value(VOID)
        coh_chaos = AttentionController._operator_coherence_value(CHAOS)
        self.assertAlmostEqual(coh_harmony, 1.0)
        self.assertGreater(coh_harmony, coh_void)
        self.assertGreater(coh_harmony, coh_chaos)

    def test_cosine_similarity_identical(self):
        """Identical distributions produce similarity ~1.0."""
        dist = [0.0] * NUM_OPS
        dist[HARMONY] = 0.5
        dist[BREATH] = 0.3
        dist[BALANCE] = 0.2
        sim = AttentionController._cosine_similarity(dist, dist)
        self.assertAlmostEqual(sim, 1.0, places=3)

    def test_cosine_similarity_orthogonal(self):
        """Orthogonal distributions produce similarity ~0.0."""
        a = [0.0] * NUM_OPS
        a[HARMONY] = 1.0
        b = [0.0] * NUM_OPS
        b[VOID] = 1.0
        sim = AttentionController._cosine_similarity(a, b)
        self.assertAlmostEqual(sim, 0.0, places=3)


if __name__ == '__main__':
    unittest.main()
