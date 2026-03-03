"""
ck_game_sense_tests.py -- Tests for Digital Environment Perception
==================================================================
Validates: GameStateCodec, ScreenVisionCodec, GameActionDomain,
GameRewardSignal, GameEnvironmentAdapter, GameSession.

66 tests. Zero external dependencies beyond ck_sim.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import unittest
import math
import os
import sys

# Ensure ck_sim package is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ================================================================
#  GAME STATE CODEC TESTS
# ================================================================

class TestGameStateCodec(unittest.TestCase):
    """Test game telemetry → 5D force vector → operator pipeline."""

    def test_import(self):
        """GameStateCodec imports cleanly."""
        from ck_sim.ck_game_sense import GameStateCodec
        codec = GameStateCodec()
        self.assertIsNotNone(codec)

    def test_name(self):
        """Codec name is 'game_state'."""
        from ck_sim.ck_game_sense import GameStateCodec
        codec = GameStateCodec()
        self.assertEqual(codec.name, 'game_state')

    def test_team_assignment(self):
        """Team 0 = blue, team 1 = orange."""
        from ck_sim.ck_game_sense import GameStateCodec, GOAL_ORANGE, GOAL_BLUE
        blue = GameStateCodec(team=0)
        orange = GameStateCodec(team=1)
        self.assertEqual(blue._target_goal, GOAL_ORANGE)
        self.assertEqual(orange._target_goal, GOAL_BLUE)

    def test_force_vector_dimensions(self):
        """map_to_force_vector returns 5 floats."""
        from ck_sim.ck_game_sense import GameStateCodec
        codec = GameStateCodec()
        vec = codec.map_to_force_vector({
            'car_x': 0, 'car_y': 0, 'car_z': 17,
            'car_vx': 500, 'car_vy': 0, 'car_vz': 0,
            'ball_x': 1000, 'ball_y': 0, 'ball_z': 93,
            'boost_amount': 50,
        })
        self.assertEqual(len(vec), 5)

    def test_force_vector_range(self):
        """All force vector components in [0, 1]."""
        from ck_sim.ck_game_sense import GameStateCodec
        codec = GameStateCodec()
        # Various positions
        for cx in [-5000, 0, 5000]:
            for cy in [-4000, 0, 4000]:
                vec = codec.map_to_force_vector({
                    'car_x': cx, 'car_y': cy, 'car_z': 17,
                    'car_vx': 1000, 'car_vy': 200, 'car_vz': 0,
                    'ball_x': 0, 'ball_y': 0, 'ball_z': 93,
                    'boost_amount': 50,
                })
                for i, v in enumerate(vec):
                    self.assertGreaterEqual(v, 0.0,
                        f"Component {i} = {v} < 0 at ({cx}, {cy})")
                    self.assertLessEqual(v, 1.0,
                        f"Component {i} = {v} > 1 at ({cx}, {cy})")

    def test_center_field_high_aperture(self):
        """Car at center of field → high aperture (field awareness)."""
        from ck_sim.ck_game_sense import GameStateCodec
        codec = GameStateCodec()
        vec = codec.map_to_force_vector({
            'car_x': 0, 'car_y': 0, 'car_z': 17,
            'car_vx': 0, 'car_vy': 0, 'car_vz': 0,
            'ball_x': 0, 'ball_y': 0, 'ball_z': 93,
            'boost_amount': 50,
        })
        self.assertGreater(vec[0], 0.5)  # aperture should be high at center

    def test_high_speed_high_pressure(self):
        """High car speed → high pressure."""
        from ck_sim.ck_game_sense import GameStateCodec
        codec = GameStateCodec()
        vec = codec.map_to_force_vector({
            'car_x': 0, 'car_y': 0, 'car_z': 17,
            'car_vx': 2200, 'car_vy': 0, 'car_vz': 0,
            'ball_x': 0, 'ball_y': 0, 'ball_z': 93,
            'boost_amount': 50,
        })
        self.assertGreater(vec[1], 0.4)  # pressure from speed

    def test_low_boost_high_pressure(self):
        """Low boost → pressure increases (resource scarcity)."""
        from ck_sim.ck_game_sense import GameStateCodec
        codec = GameStateCodec()
        vec_low = codec.map_to_force_vector({
            'car_x': 0, 'car_y': 0, 'car_z': 17,
            'car_vx': 500, 'car_vy': 0, 'car_vz': 0,
            'ball_x': 0, 'ball_y': 0, 'ball_z': 93,
            'boost_amount': 5,
        })
        codec2 = GameStateCodec()
        vec_high = codec2.map_to_force_vector({
            'car_x': 0, 'car_y': 0, 'car_z': 17,
            'car_vx': 500, 'car_vy': 0, 'car_vz': 0,
            'ball_x': 0, 'ball_y': 0, 'ball_z': 93,
            'boost_amount': 100,
        })
        self.assertGreater(vec_low[1], vec_high[1])

    def test_ball_close_high_binding(self):
        """Ball close to car → high binding."""
        from ck_sim.ck_game_sense import GameStateCodec
        codec = GameStateCodec()
        vec = codec.map_to_force_vector({
            'car_x': 0, 'car_y': 0, 'car_z': 17,
            'car_vx': 0, 'car_vy': 0, 'car_vz': 0,
            'ball_x': 100, 'ball_y': 0, 'ball_z': 93,
            'boost_amount': 50,
        })
        self.assertGreater(vec[3], 0.8)  # binding high when ball is close

    def test_ball_far_low_binding(self):
        """Ball far from car → low binding."""
        from ck_sim.ck_game_sense import GameStateCodec
        codec = GameStateCodec()
        vec = codec.map_to_force_vector({
            'car_x': -5000, 'car_y': -4000, 'car_z': 17,
            'car_vx': 0, 'car_vy': 0, 'car_vz': 0,
            'ball_x': 5000, 'ball_y': 4000, 'ball_z': 93,
            'boost_amount': 50,
        })
        self.assertLess(vec[3], 0.3)  # binding low when ball is far

    def test_feed_returns_valid_operator(self):
        """feed() returns operator in [0, 9]."""
        from ck_sim.ck_game_sense import GameStateCodec
        from ck_sim.ck_sim_heartbeat import NUM_OPS
        codec = GameStateCodec()
        import random
        random.seed(42)
        for _ in range(10):
            reading = {
                'car_x': random.gauss(0, 2000),
                'car_y': random.gauss(0, 1000),
                'car_z': 17,
                'car_vx': random.gauss(500, 200),
                'car_vy': random.gauss(0, 100),
                'car_vz': 0,
                'ball_x': random.gauss(1000, 500),
                'ball_y': random.gauss(0, 500),
                'ball_z': 93,
                'boost_amount': random.uniform(0, 100),
            }
            op = codec.feed(reading)
        self.assertTrue(0 <= op < NUM_OPS)

    def test_coherence_in_range(self):
        """coherence() returns [0, 1] after some ticks."""
        from ck_sim.ck_game_sense import GameStateCodec
        codec = GameStateCodec()
        import random
        random.seed(42)
        for _ in range(20):
            codec.feed({
                'car_x': random.gauss(0, 2000),
                'car_y': random.gauss(0, 1000),
                'car_z': 17,
                'car_vx': random.gauss(500, 200),
                'car_vy': 0, 'car_vz': 0,
                'ball_x': 1000, 'ball_y': 0, 'ball_z': 93,
                'boost_amount': 50,
            })
        coh = codec.coherence()
        self.assertGreaterEqual(coh, 0.0)
        self.assertLessEqual(coh, 1.0)

    def test_stats_keys(self):
        """stats() returns expected keys."""
        from ck_sim.ck_game_sense import GameStateCodec
        codec = GameStateCodec()
        codec.feed({'car_x': 0, 'car_y': 0, 'car_z': 17,
                     'car_vx': 0, 'car_vy': 0, 'car_vz': 0,
                     'ball_x': 0, 'ball_y': 0, 'ball_z': 93,
                     'boost_amount': 50})
        s = codec.stats()
        self.assertIn('name', s)
        self.assertIn('ticks', s)
        self.assertIn('coherence', s)
        self.assertEqual(s['name'], 'game_state')


# ================================================================
#  SCREEN VISION CODEC TESTS
# ================================================================

class TestScreenVisionCodec(unittest.TestCase):
    """Test screen capture statistics → operator pipeline."""

    def test_import(self):
        from ck_sim.ck_game_sense import ScreenVisionCodec
        codec = ScreenVisionCodec()
        self.assertIsNotNone(codec)

    def test_name(self):
        from ck_sim.ck_game_sense import ScreenVisionCodec
        codec = ScreenVisionCodec()
        self.assertEqual(codec.name, 'screen_vision')

    def test_force_vector_dimensions(self):
        from ck_sim.ck_game_sense import ScreenVisionCodec
        codec = ScreenVisionCodec()
        vec = codec.map_to_force_vector({
            'field_motion': 0.3, 'field_brightness': 0.6,
            'field_edges': 0.4, 'boost_meter': 0.5,
            'score_delta': 0.0, 'minimap_density': 0.3,
        })
        self.assertEqual(len(vec), 5)

    def test_force_vector_range(self):
        """All components in [0, 1]."""
        from ck_sim.ck_game_sense import ScreenVisionCodec
        codec = ScreenVisionCodec()
        import random
        random.seed(42)
        for _ in range(20):
            vec = codec.map_to_force_vector({
                'field_motion': random.random(),
                'field_brightness': random.random(),
                'field_edges': random.random(),
                'boost_meter': random.random(),
                'score_delta': random.uniform(-1, 1),
                'minimap_density': random.random(),
            })
            for i, v in enumerate(vec):
                self.assertGreaterEqual(v, 0.0)
                self.assertLessEqual(v, 1.0)

    def test_high_motion_high_pressure(self):
        """High field motion → high pressure."""
        from ck_sim.ck_game_sense import ScreenVisionCodec
        codec = ScreenVisionCodec()
        vec = codec.map_to_force_vector({
            'field_motion': 0.9, 'field_brightness': 0.5,
            'field_edges': 0.3, 'boost_meter': 0.5,
            'score_delta': 0.0, 'minimap_density': 0.2,
        })
        self.assertGreater(vec[1], 0.8)

    def test_score_delta_affects_depth(self):
        """Score tension affects depth."""
        from ck_sim.ck_game_sense import ScreenVisionCodec
        codec1 = ScreenVisionCodec()
        vec_calm = codec1.map_to_force_vector({
            'field_motion': 0.3, 'field_brightness': 0.5,
            'field_edges': 0.3, 'boost_meter': 0.5,
            'score_delta': 0.0, 'minimap_density': 0.2,
        })
        codec2 = ScreenVisionCodec()
        vec_tense = codec2.map_to_force_vector({
            'field_motion': 0.3, 'field_brightness': 0.5,
            'field_edges': 0.3, 'boost_meter': 0.5,
            'score_delta': -1.0, 'minimap_density': 0.2,
        })
        self.assertGreater(vec_tense[2], vec_calm[2])

    def test_feed_returns_operator(self):
        from ck_sim.ck_game_sense import ScreenVisionCodec
        from ck_sim.ck_sim_heartbeat import NUM_OPS
        codec = ScreenVisionCodec()
        import random
        random.seed(42)
        for _ in range(10):
            op = codec.feed({
                'field_motion': random.random(),
                'field_brightness': random.random(),
                'field_edges': random.random(),
                'boost_meter': random.random(),
                'score_delta': 0.0,
                'minimap_density': random.random(),
            })
        self.assertTrue(0 <= op < NUM_OPS)


# ================================================================
#  GAME ACTION DOMAIN TESTS
# ================================================================

class TestGameActionDomain(unittest.TestCase):
    """Test BTQ decision domain for game actions."""

    def test_import(self):
        from ck_sim.ck_game_sense import GameActionDomain
        domain = GameActionDomain()
        self.assertIsNotNone(domain)

    def test_name(self):
        from ck_sim.ck_game_sense import GameActionDomain
        domain = GameActionDomain()
        self.assertEqual(domain.name, 'game_action')

    def test_t_generate_candidates(self):
        """t_generate produces the requested number of candidates."""
        from ck_sim.ck_game_sense import GameActionDomain
        domain = GameActionDomain(seed=42)
        candidates = domain.t_generate({}, {}, 32)
        self.assertEqual(len(candidates), 32)

    def test_t_generate_has_templates(self):
        """Generated candidates include template actions."""
        from ck_sim.ck_game_sense import GameActionDomain
        domain = GameActionDomain(seed=42)
        candidates = domain.t_generate({}, {}, 32)
        sources = [c.source for c in candidates]
        self.assertTrue(any('template_' in s for s in sources))

    def test_t_generate_has_perturbations(self):
        """Generated candidates include Lévy-perturbed actions."""
        from ck_sim.ck_game_sense import GameActionDomain
        domain = GameActionDomain(seed=42)
        candidates = domain.t_generate({}, {}, 32)
        sources = [c.source for c in candidates]
        self.assertTrue(any('levy_' in s for s in sources))

    def test_b_check_passes_normal(self):
        """Normal action with boost available passes b_check."""
        from ck_sim.ck_game_sense import GameActionDomain, GameAction
        from ck_sim.ck_btq import Candidate
        domain = GameActionDomain()
        cand = Candidate(
            domain='game_action',
            payload=GameAction(throttle=1.0, boost=True, action_name='boost_fwd'),
        )
        passed, reason = domain.b_check(cand, {
            'boost_amount': 50, 'is_on_ground': True, 'has_flip': True
        })
        self.assertTrue(passed)

    def test_b_check_rejects_no_boost(self):
        """Boosting with empty tank is rejected."""
        from ck_sim.ck_game_sense import GameActionDomain, GameAction
        from ck_sim.ck_btq import Candidate
        domain = GameActionDomain()
        cand = Candidate(
            domain='game_action',
            payload=GameAction(throttle=1.0, boost=True, action_name='boost_fwd'),
        )
        passed, reason = domain.b_check(cand, {
            'boost_amount': 0, 'is_on_ground': True, 'has_flip': True
        })
        self.assertFalse(passed)
        self.assertEqual(reason, 'no_boost')

    def test_b_check_rejects_no_flip(self):
        """Jumping without ground or flip is rejected."""
        from ck_sim.ck_game_sense import GameActionDomain, GameAction
        from ck_sim.ck_btq import Candidate
        domain = GameActionDomain()
        cand = Candidate(
            domain='game_action',
            payload=GameAction(throttle=0.5, jump=True, action_name='jump'),
        )
        passed, reason = domain.b_check(cand, {
            'boost_amount': 50, 'is_on_ground': False, 'has_flip': False
        })
        self.assertFalse(passed)
        self.assertEqual(reason, 'no_flip')

    def test_b_check_allows_ground_jump(self):
        """Jumping from ground is allowed even without flip."""
        from ck_sim.ck_game_sense import GameActionDomain, GameAction
        from ck_sim.ck_btq import Candidate
        domain = GameActionDomain()
        cand = Candidate(
            domain='game_action',
            payload=GameAction(throttle=0.5, jump=True, action_name='jump'),
        )
        passed, _ = domain.b_check(cand, {
            'boost_amount': 50, 'is_on_ground': True, 'has_flip': False
        })
        self.assertTrue(passed)

    def test_einstein_score_range(self):
        """Einstein score in [0, 1]."""
        from ck_sim.ck_game_sense import GameActionDomain, GameAction
        from ck_sim.ck_btq import Candidate
        domain = GameActionDomain()
        cand = Candidate(
            domain='game_action',
            payload=GameAction(throttle=1.0, boost=True, action_name='boost_fwd'),
        )
        env = {
            'car_x': 0, 'car_y': 0, 'ball_x': 1000, 'ball_y': 0,
            'boost_amount': 50, 'team': 0, 'score_self': 0, 'score_opponent': 0,
        }
        score, details = domain.einstein_score(cand, env)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
        self.assertIn('pursuit_cost', details)

    def test_tesla_score_range(self):
        """Tesla score in [0, 1]."""
        from ck_sim.ck_game_sense import GameActionDomain, GameAction
        from ck_sim.ck_btq import Candidate
        domain = GameActionDomain()
        cand = Candidate(
            domain='game_action',
            payload=GameAction(throttle=0.5, steer=0.3, boost=False, action_name='turn'),
        )
        score, details = domain.tesla_score(cand)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
        self.assertIn('smoothness_cost', details)

    def test_simple_action_lower_tesla(self):
        """Simple action (one input) has lower Tesla score than complex."""
        from ck_sim.ck_game_sense import GameActionDomain, GameAction
        from ck_sim.ck_btq import Candidate
        domain = GameActionDomain()
        simple = Candidate(
            domain='game_action',
            payload=GameAction(throttle=0.3, action_name='gentle'),
        )
        complex_a = Candidate(
            domain='game_action',
            payload=GameAction(throttle=1.0, steer=1.0, boost=True, jump=True, action_name='crazy'),
        )
        s_simple, _ = domain.tesla_score(simple)
        s_complex, _ = domain.tesla_score(complex_a)
        self.assertLess(s_simple, s_complex)


# ================================================================
#  GAME REWARD SIGNAL TESTS
# ================================================================

class TestGameRewardSignal(unittest.TestCase):
    """Test game event → operator feedback system."""

    def test_import(self):
        from ck_sim.ck_game_sense import GameRewardSignal
        reward = GameRewardSignal()
        self.assertIsNotNone(reward)

    def test_goal_scored_is_harmony(self):
        """Scoring a goal produces HARMONY operator."""
        from ck_sim.ck_game_sense import GameRewardSignal
        from ck_sim.ck_sim_heartbeat import HARMONY
        reward = GameRewardSignal()
        op = reward.signal('goal_scored')
        self.assertEqual(op, HARMONY)

    def test_goal_conceded_is_collapse(self):
        """Conceding a goal produces COLLAPSE operator."""
        from ck_sim.ck_game_sense import GameRewardSignal
        from ck_sim.ck_sim_heartbeat import COLLAPSE
        reward = GameRewardSignal()
        op = reward.signal('goal_conceded')
        self.assertEqual(op, COLLAPSE)

    def test_unknown_event_is_void(self):
        """Unknown event produces VOID."""
        from ck_sim.ck_game_sense import GameRewardSignal
        from ck_sim.ck_sim_heartbeat import VOID
        reward = GameRewardSignal()
        op = reward.signal('unknown_event')
        self.assertEqual(op, VOID)

    def test_event_counts(self):
        """Event counts track correctly."""
        from ck_sim.ck_game_sense import GameRewardSignal
        reward = GameRewardSignal()
        reward.signal('goal_scored')
        reward.signal('goal_scored')
        reward.signal('save')
        self.assertEqual(reward._event_counts['goal_scored'], 2)
        self.assertEqual(reward._event_counts['save'], 1)

    def test_fuse_recent(self):
        """fuse_recent() composes recent reward operators via CL."""
        from ck_sim.ck_game_sense import GameRewardSignal
        from ck_sim.ck_sim_heartbeat import HARMONY, compose
        reward = GameRewardSignal()
        reward.signal('goal_scored')   # HARMONY
        reward.signal('goal_scored')   # HARMONY
        fuse = reward.fuse_recent(2)
        # compose(HARMONY, HARMONY) = HARMONY
        self.assertEqual(fuse, compose(HARMONY, HARMONY))

    def test_coherence_after_goals(self):
        """Coherence is 1.0 when all events are HARMONY."""
        from ck_sim.ck_game_sense import GameRewardSignal
        reward = GameRewardSignal()
        for _ in range(10):
            reward.signal('goal_scored')
        self.assertAlmostEqual(reward.coherence(), 1.0)

    def test_coherence_mixed_events(self):
        """Coherence < 1.0 with mixed events."""
        from ck_sim.ck_game_sense import GameRewardSignal
        reward = GameRewardSignal()
        reward.signal('goal_scored')    # HARMONY
        reward.signal('goal_conceded')  # COLLAPSE
        reward.signal('save')           # BALANCE
        coh = reward.coherence()
        self.assertLess(coh, 1.0)

    def test_stats_keys(self):
        from ck_sim.ck_game_sense import GameRewardSignal
        reward = GameRewardSignal()
        reward.signal('ball_touch')
        s = reward.stats()
        self.assertIn('reward_operator', s)
        self.assertIn('coherence', s)
        self.assertIn('event_counts', s)
        self.assertIn('total_events', s)

    def test_all_events_have_operators(self):
        """Every event in GAME_EVENT_TO_OPERATOR produces a valid operator."""
        from ck_sim.ck_game_sense import GameRewardSignal, GAME_EVENT_TO_OPERATOR
        from ck_sim.ck_sim_heartbeat import NUM_OPS
        reward = GameRewardSignal()
        for event_name in GAME_EVENT_TO_OPERATOR:
            op = reward.signal(event_name)
            self.assertTrue(0 <= op < NUM_OPS, f"Event '{event_name}' → op={op}")


# ================================================================
#  GAME ENVIRONMENT ADAPTER TESTS
# ================================================================

class TestGameEnvironmentAdapter(unittest.TestCase):
    """Test CK operator → game input bridge."""

    def test_import(self):
        from ck_sim.ck_game_sense import GameEnvironmentAdapter
        adapter = GameEnvironmentAdapter()
        self.assertIsNotNone(adapter)

    def test_update_from_operator(self):
        """update_from_operator returns a valid action dict."""
        from ck_sim.ck_game_sense import GameEnvironmentAdapter
        from ck_sim.ck_sim_heartbeat import HARMONY
        adapter = GameEnvironmentAdapter()
        action = adapter.update_from_operator(HARMONY)
        self.assertIn('action', action)
        self.assertIn('throttle', action)
        self.assertIn('steer', action)
        self.assertIn('boost', action)

    def test_void_is_idle(self):
        """VOID operator → idle action."""
        from ck_sim.ck_game_sense import GameEnvironmentAdapter
        from ck_sim.ck_sim_heartbeat import VOID
        adapter = GameEnvironmentAdapter()
        action = adapter.update_from_operator(VOID)
        self.assertEqual(action['action'], 'idle')

    def test_progress_is_advance(self):
        """PROGRESS operator → advance action with boost."""
        from ck_sim.ck_game_sense import GameEnvironmentAdapter
        from ck_sim.ck_sim_heartbeat import PROGRESS
        adapter = GameEnvironmentAdapter()
        action = adapter.update_from_operator(PROGRESS)
        self.assertEqual(action['action'], 'advance')
        self.assertTrue(action['boost'])

    def test_collapse_is_retreat(self):
        """COLLAPSE operator → retreat action."""
        from ck_sim.ck_game_sense import GameEnvironmentAdapter
        from ck_sim.ck_sim_heartbeat import COLLAPSE
        adapter = GameEnvironmentAdapter()
        action = adapter.update_from_operator(COLLAPSE)
        self.assertEqual(action['action'], 'retreat')
        self.assertLess(action['throttle'], 0)

    def test_smoothing_applied(self):
        """Smoothing produces intermediate values."""
        from ck_sim.ck_game_sense import GameEnvironmentAdapter
        from ck_sim.ck_sim_heartbeat import VOID, PROGRESS
        adapter = GameEnvironmentAdapter()
        adapter.update_from_operator(VOID)     # throttle=0
        action = adapter.update_from_operator(PROGRESS)  # throttle=1.0
        # With smoothing, throttle_smooth should be < 1.0
        self.assertLess(action['throttle_smooth'], 1.0)
        self.assertGreater(action['throttle_smooth'], 0.0)

    def test_game_tick_holds_action(self):
        """game_tick returns held action between CK updates."""
        from ck_sim.ck_game_sense import GameEnvironmentAdapter
        from ck_sim.ck_sim_heartbeat import HARMONY
        adapter = GameEnvironmentAdapter()
        adapter.update_from_operator(HARMONY)
        held = adapter.game_tick()
        self.assertEqual(held['action'], 'flow')

    def test_update_from_btq(self):
        """update_from_btq accepts a GameAction."""
        from ck_sim.ck_game_sense import GameEnvironmentAdapter, GameAction
        adapter = GameEnvironmentAdapter()
        ga = GameAction(throttle=0.8, steer=-0.3, boost=True,
                        action_name='custom')
        action = adapter.update_from_btq(ga)
        self.assertEqual(action['action'], 'custom')
        self.assertEqual(action['source'], 'btq')

    def test_stats_keys(self):
        from ck_sim.ck_game_sense import GameEnvironmentAdapter
        adapter = GameEnvironmentAdapter()
        s = adapter.stats()
        self.assertIn('current_action', s)
        self.assertIn('smooth_throttle', s)
        self.assertIn('smooth_steer', s)


# ================================================================
#  OPERATOR → GAME ACTION MAPPING TESTS
# ================================================================

class TestOperatorToGameAction(unittest.TestCase):
    """Test the operator → action mapping table."""

    def test_all_operators_mapped(self):
        """Every operator 0-9 has a game action mapping."""
        from ck_sim.ck_game_sense import OPERATOR_TO_GAME_ACTION
        from ck_sim.ck_sim_heartbeat import NUM_OPS
        for op in range(NUM_OPS):
            self.assertIn(op, OPERATOR_TO_GAME_ACTION,
                          f"Operator {op} missing from OPERATOR_TO_GAME_ACTION")

    def test_all_actions_have_required_keys(self):
        """Every action has throttle, steer, boost, jump."""
        from ck_sim.ck_game_sense import OPERATOR_TO_GAME_ACTION
        for op, action in OPERATOR_TO_GAME_ACTION.items():
            self.assertIn('action', action)
            self.assertIn('throttle', action)
            self.assertIn('steer', action)
            self.assertIn('boost', action)
            self.assertIn('jump', action)

    def test_throttle_range(self):
        """Throttle values in [-1, 1]."""
        from ck_sim.ck_game_sense import OPERATOR_TO_GAME_ACTION
        for op, action in OPERATOR_TO_GAME_ACTION.items():
            self.assertGreaterEqual(action['throttle'], -1.0)
            self.assertLessEqual(action['throttle'], 1.0)


# ================================================================
#  GAME SESSION TESTS
# ================================================================

class TestGameSession(unittest.TestCase):
    """Test the top-level game session orchestrator."""

    def test_import(self):
        from ck_sim.ck_game_sense import GameSession
        session = GameSession()
        self.assertIsNotNone(session)

    def test_feed_state_returns_operator(self):
        """feed_state returns a valid operator."""
        from ck_sim.ck_game_sense import GameSession
        from ck_sim.ck_sim_heartbeat import NUM_OPS
        session = GameSession(team=0)
        op = session.feed_state({
            'car_x': 0, 'car_y': 0, 'car_z': 17,
            'car_vx': 500, 'car_vy': 0, 'car_vz': 0,
            'ball_x': 1000, 'ball_y': 0, 'ball_z': 93,
            'boost_amount': 50,
        })
        self.assertTrue(0 <= op < NUM_OPS)

    def test_feed_screen_returns_operator(self):
        from ck_sim.ck_game_sense import GameSession
        from ck_sim.ck_sim_heartbeat import NUM_OPS
        session = GameSession()
        op = session.feed_screen({
            'field_motion': 0.3, 'field_brightness': 0.5,
            'field_edges': 0.4, 'boost_meter': 0.5,
            'score_delta': 0.0, 'minimap_density': 0.3,
        })
        self.assertTrue(0 <= op < NUM_OPS)

    def test_fused_operator_composes(self):
        """Fused operator is CL composition of state and screen."""
        from ck_sim.ck_game_sense import GameSession
        from ck_sim.ck_sim_heartbeat import compose
        session = GameSession()
        # Feed enough to get valid operators
        for _ in range(5):
            session.feed_state({
                'car_x': 0, 'car_y': 0, 'car_z': 17,
                'car_vx': 500, 'car_vy': 0, 'car_vz': 0,
                'ball_x': 1000, 'ball_y': 0, 'ball_z': 93,
                'boost_amount': 50,
            })
            session.feed_screen({
                'field_motion': 0.3, 'field_brightness': 0.5,
                'field_edges': 0.4, 'boost_meter': 0.5,
                'score_delta': 0.0, 'minimap_density': 0.3,
            })
        expected = compose(session._state_operator, session._screen_operator)
        self.assertEqual(session.fused_operator, expected)

    def test_on_event_returns_operator(self):
        from ck_sim.ck_game_sense import GameSession
        from ck_sim.ck_sim_heartbeat import HARMONY
        session = GameSession()
        op = session.on_event('goal_scored')
        self.assertEqual(op, HARMONY)

    def test_get_action_reflex(self):
        """get_action without BTQ returns a valid action dict."""
        from ck_sim.ck_game_sense import GameSession
        session = GameSession()
        session.feed_state({
            'car_x': 0, 'car_y': 0, 'car_z': 17,
            'car_vx': 0, 'car_vy': 0, 'car_vz': 0,
            'ball_x': 0, 'ball_y': 0, 'ball_z': 93,
            'boost_amount': 50,
        })
        action = session.get_action()
        self.assertIn('action', action)

    def test_get_action_btq(self):
        """get_action with BTQ returns a valid action dict."""
        from ck_sim.ck_game_sense import GameSession
        session = GameSession()
        env = {
            'car_x': 0, 'car_y': 0, 'ball_x': 1000, 'ball_y': 0,
            'boost_amount': 50, 'is_on_ground': True, 'has_flip': True,
            'team': 0, 'score_self': 0, 'score_opponent': 0,
        }
        action = session.get_action(use_btq=True, env_state=env)
        self.assertIn('action', action)

    def test_coherence_in_range(self):
        from ck_sim.ck_game_sense import GameSession
        session = GameSession()
        import random
        random.seed(42)
        for _ in range(20):
            session.feed_state({
                'car_x': random.gauss(0, 2000),
                'car_y': random.gauss(0, 1000),
                'car_z': 17,
                'car_vx': random.gauss(500, 200),
                'car_vy': 0, 'car_vz': 0,
                'ball_x': 1000, 'ball_y': 0, 'ball_z': 93,
                'boost_amount': 50,
            })
        coh = session.coherence()
        self.assertGreaterEqual(coh, 0.0)
        self.assertLessEqual(coh, 1.0)

    def test_stats_complete(self):
        """stats() returns all expected keys."""
        from ck_sim.ck_game_sense import GameSession
        session = GameSession()
        session.feed_state({
            'car_x': 0, 'car_y': 0, 'car_z': 17,
            'car_vx': 0, 'car_vy': 0, 'car_vz': 0,
            'ball_x': 0, 'ball_y': 0, 'ball_z': 93,
            'boost_amount': 50,
        })
        session.on_event('kickoff')
        s = session.stats()
        self.assertIn('tick', s)
        self.assertIn('fused_operator', s)
        self.assertIn('coherence', s)
        self.assertIn('reward', s)
        self.assertIn('adapter', s)
        self.assertIn('state_codec', s)
        self.assertIn('screen_codec', s)

    def test_multi_tick_simulation(self):
        """Run 50 ticks without error."""
        from ck_sim.ck_game_sense import GameSession
        import random
        random.seed(42)
        session = GameSession(team=0, seed=42)
        for tick in range(50):
            session.feed_state({
                'car_x': random.gauss(0, 2000),
                'car_y': random.gauss(0, 1000),
                'car_z': 17,
                'car_vx': random.gauss(500, 200),
                'car_vy': random.gauss(0, 100),
                'car_vz': 0,
                'ball_x': random.gauss(1000, 500),
                'ball_y': random.gauss(0, 500),
                'ball_z': 93,
                'boost_amount': random.uniform(0, 100),
                'team': 0,
            })
            session.feed_screen({
                'field_motion': random.uniform(0.1, 0.6),
                'field_brightness': random.uniform(0.3, 0.8),
                'field_edges': random.uniform(0.2, 0.7),
                'boost_meter': random.uniform(0.0, 1.0),
                'score_delta': 0.0,
                'minimap_density': random.uniform(0.1, 0.5),
            })
            if tick == 25:
                session.on_event('ball_touch')
            if tick == 40:
                session.on_event('shot_on_goal')
        # Should complete without error
        stats = session.stats()
        self.assertEqual(stats['tick'], 50)
        self.assertGreater(stats['reward']['total_events'], 0)


# ================================================================
#  GAME CODEC REGISTRY TESTS
# ================================================================

class TestGameCodecRegistry(unittest.TestCase):
    """Test that game codecs register properly."""

    def test_registry_entries(self):
        from ck_sim.ck_game_sense import GAME_CODEC_REGISTRY
        self.assertIn('game_state', GAME_CODEC_REGISTRY)
        self.assertIn('screen_vision', GAME_CODEC_REGISTRY)

    def test_registry_creates_instances(self):
        from ck_sim.ck_game_sense import GAME_CODEC_REGISTRY
        for name, cls in GAME_CODEC_REGISTRY.items():
            instance = cls()
            self.assertEqual(instance.name, name)


# ================================================================
#  CONSTANTS TESTS
# ================================================================

class TestConstants(unittest.TestCase):
    """Validate game constants against Rocket League specs."""

    def test_field_dimensions_positive(self):
        from ck_sim.ck_game_sense import FIELD_LENGTH, FIELD_WIDTH, FIELD_HEIGHT
        self.assertGreater(FIELD_LENGTH, 0)
        self.assertGreater(FIELD_WIDTH, 0)
        self.assertGreater(FIELD_HEIGHT, 0)

    def test_car_max_speed(self):
        from ck_sim.ck_game_sense import CAR_MAX_SPEED, CAR_SUPERSONIC
        self.assertEqual(CAR_MAX_SPEED, 2300)
        self.assertLess(CAR_SUPERSONIC, CAR_MAX_SPEED)

    def test_goal_positions_symmetric(self):
        """Blue and orange goals are symmetric about origin."""
        from ck_sim.ck_game_sense import GOAL_BLUE, GOAL_ORANGE
        self.assertAlmostEqual(GOAL_BLUE[0], -GOAL_ORANGE[0])
        self.assertEqual(GOAL_BLUE[1], GOAL_ORANGE[1])

    def test_tick_rates(self):
        from ck_sim.ck_game_sense import GAME_TICK_RATE, CK_TICK_RATE, TICKS_PER_CK
        self.assertEqual(GAME_TICK_RATE, 120)
        self.assertEqual(CK_TICK_RATE, 50)
        self.assertEqual(TICKS_PER_CK, GAME_TICK_RATE // CK_TICK_RATE)

    def test_all_game_events_defined(self):
        """All game events map to valid operators."""
        from ck_sim.ck_game_sense import GAME_EVENT_TO_OPERATOR
        from ck_sim.ck_sim_heartbeat import NUM_OPS
        self.assertGreater(len(GAME_EVENT_TO_OPERATOR), 10)
        for event, op in GAME_EVENT_TO_OPERATOR.items():
            self.assertTrue(0 <= op < NUM_OPS,
                            f"Event '{event}' maps to invalid op={op}")


# ================================================================
#  RUN
# ================================================================

if __name__ == '__main__':
    unittest.main()
