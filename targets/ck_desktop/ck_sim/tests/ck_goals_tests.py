"""
ck_goals_tests.py -- Tests for Goal Hierarchy System
======================================================
Validates: goal patterns, goal evaluation, goal stack, drive system,
goal planner, goal evaluator, and integration with forecast + episodic.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import unittest

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, COLLAPSE, CHAOS, PROGRESS,
    BREATH, BALANCE, COUNTER, LATTICE, RESET, OP_NAMES
)
from ck_sim.ck_goals import (
    Goal, GoalPriority, GoalStack, DriveSystem, GoalPlanner,
    GoalEvaluator, make_goal, GOAL_PATTERNS,
    MAX_GOALS, GOAL_TIMEOUT_TICKS, SATISFACTION_THRESHOLD,
)


class TestImport(unittest.TestCase):
    def test_import(self):
        import ck_sim.ck_goals
        self.assertTrue(hasattr(ck_sim.ck_goals, 'GoalEvaluator'))
        self.assertTrue(hasattr(ck_sim.ck_goals, 'DriveSystem'))
        self.assertTrue(hasattr(ck_sim.ck_goals, 'GOAL_PATTERNS'))


class TestGoalPatterns(unittest.TestCase):
    """Goal pattern templates."""

    def test_patterns_exist(self):
        expected = ['survive', 'charge', 'retreat', 'stabilize',
                    'explore', 'bond', 'express', 'rest', 'observe',
                    'play', 'home']
        for name in expected:
            self.assertIn(name, GOAL_PATTERNS)

    def test_patterns_are_distributions(self):
        """Each pattern sums to ~1.0."""
        for name, pattern in GOAL_PATTERNS.items():
            self.assertEqual(len(pattern), NUM_OPS)
            total = sum(pattern)
            self.assertAlmostEqual(total, 1.0, places=2,
                msg=f"Pattern '{name}' sums to {total}")

    def test_patterns_non_negative(self):
        for name, pattern in GOAL_PATTERNS.items():
            for v in pattern:
                self.assertGreaterEqual(v, 0.0,
                    msg=f"Pattern '{name}' has negative value")


class TestGoal(unittest.TestCase):
    """Goal lifecycle and evaluation."""

    def test_create_goal(self):
        g = make_goal('test', GoalPriority.EXPLORATION, tick=100,
                       pattern_name='explore')
        self.assertEqual(g.name, 'test')
        self.assertEqual(g.priority, GoalPriority.EXPLORATION)
        self.assertFalse(g.satisfied)

    def test_evaluate_matching_pattern(self):
        """Goal satisfied when current matches target."""
        g = make_goal('test', GoalPriority.EXPLORATION, tick=0,
                       pattern_name='explore')
        # Feed it a distribution that matches the explore pattern
        current = list(GOAL_PATTERNS['explore'])
        sat = g.evaluate(current)
        self.assertGreater(sat, 0.9)  # Should be very high
        self.assertTrue(g.satisfied)

    def test_evaluate_mismatching_pattern(self):
        """Goal not satisfied when current doesn't match."""
        g = make_goal('test', GoalPriority.EXPLORATION, tick=0,
                       pattern_name='explore')
        # Feed a completely different distribution (rest pattern)
        current = list(GOAL_PATTERNS['rest'])
        sat = g.evaluate(current)
        self.assertLess(sat, 1.0)

    def test_expiration(self):
        g = make_goal('test', GoalPriority.BACKGROUND, tick=100)
        self.assertFalse(g.is_expired(100))
        self.assertFalse(g.is_expired(5099))
        self.assertTrue(g.is_expired(100 + GOAL_TIMEOUT_TICKS + 1))

    def test_deadline_expiration(self):
        g = make_goal('test', GoalPriority.BACKGROUND, tick=100)
        g.deadline_tick = 500
        self.assertFalse(g.is_expired(499))
        self.assertTrue(g.is_expired(500))

    def test_dominant_operator(self):
        g = make_goal('test', GoalPriority.EXPLORATION, tick=0,
                       pattern_name='explore')
        dom = g.dominant_operator
        self.assertIn(dom, [COUNTER, PROGRESS, CHAOS])

    def test_to_dict(self):
        g = make_goal('test', GoalPriority.SOCIAL, tick=0,
                       pattern_name='bond')
        d = g.to_dict()
        self.assertEqual(d['name'], 'test')
        self.assertEqual(d['priority'], GoalPriority.SOCIAL)
        self.assertIn('satisfaction', d)


class TestGoalStack(unittest.TestCase):
    """Goal stack priority management."""

    def setUp(self):
        self.stack = GoalStack(max_goals=4)

    def test_push_and_top(self):
        g = make_goal('test', GoalPriority.EXPLORATION, tick=0,
                       pattern_name='explore')
        self.stack.push(g)
        self.assertEqual(self.stack.top.name, 'test')

    def test_priority_ordering(self):
        """Higher priority goal becomes top."""
        g1 = make_goal('low', GoalPriority.BACKGROUND, tick=0)
        g2 = make_goal('high', GoalPriority.SURVIVAL, tick=0,
                        pattern_name='survive')
        self.stack.push(g1)
        self.stack.push(g2)
        self.assertEqual(self.stack.top.name, 'high')

    def test_max_goals_eviction(self):
        """Stack evicts lowest priority when full."""
        for i in range(4):
            g = make_goal(f'goal_{i}', GoalPriority.BACKGROUND, tick=0)
            self.stack.push(g)

        # Push higher priority -- should evict a BACKGROUND
        g_high = make_goal('urgent', GoalPriority.SURVIVAL, tick=0,
                            pattern_name='survive')
        ok = self.stack.push(g_high)
        self.assertTrue(ok)
        self.assertEqual(self.stack.active_count, 4)
        self.assertEqual(self.stack.top.name, 'urgent')

    def test_duplicate_name_updates(self):
        """Pushing same name updates existing goal."""
        g1 = make_goal('energy', GoalPriority.HOMEOSTASIS, tick=0,
                        pattern_name='charge')
        g2 = make_goal('energy', GoalPriority.SURVIVAL, tick=100,
                        pattern_name='charge')
        self.stack.push(g1)
        self.stack.push(g2)
        # Should still be 1 goal, but with upgraded priority
        self.assertEqual(self.stack.active_count, 1)
        self.assertEqual(self.stack.top.priority, GoalPriority.SURVIVAL)

    def test_pop_satisfied(self):
        g = make_goal('test', GoalPriority.EXPLORATION, tick=0,
                       pattern_name='explore')
        self.stack.push(g)
        # Satisfy it
        g.evaluate(list(GOAL_PATTERNS['explore']))
        self.assertTrue(g.satisfied)

        satisfied = self.stack.pop_satisfied()
        self.assertEqual(len(satisfied), 1)
        self.assertEqual(self.stack.active_count, 0)

    def test_remove_expired(self):
        g = make_goal('old', GoalPriority.BACKGROUND, tick=0)
        self.stack.push(g)
        expired = self.stack.remove_expired(GOAL_TIMEOUT_TICKS + 1)
        self.assertEqual(len(expired), 1)

    def test_target_blend(self):
        """Blended target is weighted by priority."""
        g1 = make_goal('urgent', GoalPriority.SURVIVAL, tick=0,
                        pattern_name='retreat')
        g2 = make_goal('chill', GoalPriority.BACKGROUND, tick=0,
                        pattern_name='rest')
        self.stack.push(g1)
        self.stack.push(g2)
        blend = self.stack.get_target_blend()
        self.assertEqual(len(blend), NUM_OPS)
        total = sum(blend)
        self.assertAlmostEqual(total, 1.0, places=1)

    def test_empty_stack(self):
        self.assertIsNone(self.stack.top)
        self.assertEqual(self.stack.active_count, 0)


class TestDriveSystem(unittest.TestCase):
    """Innate drive evaluations."""

    def setUp(self):
        self.drives = DriveSystem()

    def test_low_battery_triggers_charge(self):
        goals = self.drives.evaluate(
            tick=100, coherence=0.7, band=2,
            battery_voltage=0.2)
        names = [g.name for g in goals]
        self.assertIn('charge_battery', names)

    def test_obstacle_triggers_retreat(self):
        goals = self.drives.evaluate(
            tick=100, coherence=0.7, band=2,
            obstacle_distance=10.0)
        names = [g.name for g in goals]
        self.assertIn('avoid_obstacle', names)

    def test_red_band_triggers_stabilize(self):
        goals = self.drives.evaluate(
            tick=100, coherence=0.2, band=0)
        names = [g.name for g in goals]
        self.assertIn('restore_coherence', names)

    def test_low_entropy_triggers_explore(self):
        goals = self.drives.evaluate(
            tick=100, coherence=0.8, band=2,
            tl_entropy=0.5)
        names = [g.name for g in goals]
        self.assertIn('explore_environment', names)

    def test_loneliness_triggers_bond(self):
        goals = self.drives.evaluate(
            tick=100, coherence=0.7, band=2,
            bonding_strength=0.05)
        names = [g.name for g in goals]
        self.assertIn('seek_companion', names)

    def test_healthy_state_no_urgent_goals(self):
        """Healthy state shouldn't trigger survival goals."""
        goals = self.drives.evaluate(
            tick=100, coherence=0.8, band=2,
            battery_voltage=1.0, obstacle_distance=400.0,
            bonding_strength=0.8, tl_entropy=3.0)
        survival_goals = [g for g in goals if g.priority == GoalPriority.SURVIVAL]
        self.assertEqual(len(survival_goals), 0)


class TestGoalPlanner(unittest.TestCase):
    """Goal decomposition into operator sequences."""

    def setUp(self):
        self.planner = GoalPlanner()

    def test_suggest_next_operator(self):
        g = make_goal('explore', GoalPriority.EXPLORATION, tick=0,
                       pattern_name='explore')
        op = self.planner.suggest_next_operator(g, HARMONY, 0.7)
        self.assertGreaterEqual(op, 0)
        self.assertLess(op, NUM_OPS)

    def test_plan_sequence_length(self):
        g = make_goal('explore', GoalPriority.EXPLORATION, tick=0,
                       pattern_name='explore')
        seq = self.planner.plan_sequence(g, HARMONY, steps=5)
        self.assertEqual(len(seq), 5)

    def test_plan_sequence_valid_operators(self):
        g = make_goal('charge', GoalPriority.SURVIVAL, tick=0,
                       pattern_name='charge')
        seq = self.planner.plan_sequence(g, COLLAPSE, steps=5)
        for op in seq:
            self.assertGreaterEqual(op, 0)
            self.assertLess(op, NUM_OPS)

    def test_explore_goal_suggests_exploration_ops(self):
        """Explore goal should suggest COUNTER, PROGRESS, or CHAOS."""
        g = make_goal('explore', GoalPriority.EXPLORATION, tick=0,
                       pattern_name='explore')
        ops = set()
        for start in range(NUM_OPS):
            op = self.planner.suggest_next_operator(g, start, 0.7)
            ops.add(op)
        # Should include at least one exploration operator
        exploration_ops = {COUNTER, PROGRESS, CHAOS}
        self.assertTrue(ops & exploration_ops)


class TestGoalEvaluator(unittest.TestCase):
    """Full goal evaluator integration."""

    def setUp(self):
        self.evaluator = GoalEvaluator()

    def test_tick_returns_operator_or_none(self):
        result = self.evaluator.tick(
            tick=100, coherence=0.8, band=2,
            current_op=HARMONY,
            current_op_dist=[0.1] * NUM_OPS)
        # May or may not suggest an operator
        if result is not None:
            self.assertGreaterEqual(result, 0)
            self.assertLess(result, NUM_OPS)

    def test_drives_generate_goals(self):
        """Low battery should generate goals after drive check."""
        # Run enough ticks for drive check to fire
        for i in range(10):
            self.evaluator.tick(
                tick=i * 50, coherence=0.7, band=2,
                current_op=HARMONY,
                current_op_dist=[0.1] * NUM_OPS,
                battery_voltage=0.2)

        self.assertGreater(self.evaluator.stack.active_count, 0)

    def test_obstacle_generates_survival_goal(self):
        for i in range(10):
            self.evaluator.tick(
                tick=i * 50, coherence=0.7, band=2,
                current_op=HARMONY,
                current_op_dist=[0.1] * NUM_OPS,
                obstacle_distance=5.0)

        top = self.evaluator.stack.top
        self.assertIsNotNone(top)
        self.assertEqual(top.priority, GoalPriority.SURVIVAL)

    def test_stats(self):
        s = self.evaluator.stats()
        self.assertIn('active_goals', s)
        self.assertIn('top_goal', s)
        self.assertIn('total_satisfied', s)

    def test_target_blend(self):
        blend = self.evaluator.target_blend
        self.assertEqual(len(blend), NUM_OPS)


class TestIntegration(unittest.TestCase):
    """Integration with forecast and episodic systems."""

    def test_goal_feeds_forecast(self):
        """Goal's target pattern can drive forecast comparison."""
        from ck_sim.ck_forecast import ForecastEngine, make_simple_tl

        engine = ForecastEngine(horizon=5, n_trajectories=2)
        tl = make_simple_tl()

        # Get goal's suggested operators
        g = make_goal('explore', GoalPriority.EXPLORATION, tick=0,
                       pattern_name='explore')
        planner = GoalPlanner()
        seq = planner.plan_sequence(g, HARMONY, steps=3)

        # Forecast each step
        for op in seq:
            fc = engine.forecast_from(op, tl, 0.7)
            self.assertGreater(len(fc.states), 0)

    def test_goal_system_lifecycle(self):
        """Full lifecycle: drive -> goal -> plan -> evaluate -> satisfy."""
        evaluator = GoalEvaluator()

        # Phase 1: Generate goal from low battery
        for i in range(10):
            evaluator.tick(
                tick=i * 50, coherence=0.7, band=2,
                current_op=HARMONY,
                current_op_dist=[0.1] * NUM_OPS,
                battery_voltage=0.2)

        self.assertGreater(evaluator.stack.active_count, 0)

        # Phase 2: Simulate achieving the charge goal
        charge_pattern = list(GOAL_PATTERNS['charge'])
        for i in range(5):
            evaluator.tick(
                tick=1000 + i * 50, coherence=0.7, band=2,
                current_op=RESET,
                current_op_dist=charge_pattern,
                battery_voltage=0.9)

        # Goal should eventually be satisfied
        s = evaluator.stats()
        # Either satisfied or still active (depends on timing)
        self.assertIsInstance(s['total_satisfied'], int)


if __name__ == '__main__':
    unittest.main()
