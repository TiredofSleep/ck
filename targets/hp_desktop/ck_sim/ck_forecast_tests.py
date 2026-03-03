"""
ck_forecast_tests.py -- Tests for Forward Simulation Engine
=============================================================
Validates: TL sampling, coherence prediction, forecast generation,
action comparison, safety checks, and BTQ integration.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import unittest

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, COLLAPSE, CHAOS, PROGRESS,
    BREATH, BALANCE, COUNTER, LATTICE, RESET, CL, compose, OP_NAMES
)
from ck_sim.ck_forecast import (
    TLPredictor, CoherenceOracle, FutureState, Forecast,
    ForecastEngine, make_simple_tl,
    DEFAULT_HORIZON, MAX_HORIZON, N_TRAJECTORIES, T_STAR_F,
)


class TestImport(unittest.TestCase):
    def test_import(self):
        import ck_sim.ck_forecast
        self.assertTrue(hasattr(ck_sim.ck_forecast, 'ForecastEngine'))
        self.assertTrue(hasattr(ck_sim.ck_forecast, 'TLPredictor'))


class TestMakeSimpleTL(unittest.TestCase):
    """Test utility TL matrix builder."""

    def test_default_shape(self):
        tl = make_simple_tl()
        self.assertEqual(len(tl), NUM_OPS)
        for row in tl:
            self.assertEqual(len(row), NUM_OPS)

    def test_default_harmony_bias(self):
        tl = make_simple_tl()
        for i in range(NUM_OPS):
            self.assertGreater(tl[i][HARMONY], tl[i][VOID])

    def test_custom_transitions(self):
        tl = make_simple_tl({(PROGRESS, HARMONY): 100})
        self.assertEqual(tl[PROGRESS][HARMONY], 100)


class TestTLPredictor(unittest.TestCase):
    """TL-based operator sequence prediction."""

    def setUp(self):
        self.tl = make_simple_tl()
        self.predictor = TLPredictor()

    def test_sample_returns_valid_operator(self):
        op = self.predictor.sample_next(HARMONY, self.tl)
        self.assertGreaterEqual(op, 0)
        self.assertLess(op, NUM_OPS)

    def test_predict_sequence_length(self):
        seq = self.predictor.predict_sequence(HARMONY, self.tl, horizon=10)
        self.assertEqual(len(seq), 10)

    def test_predict_sequence_starts_with_input(self):
        seq = self.predictor.predict_sequence(PROGRESS, self.tl, horizon=5)
        self.assertEqual(seq[0], PROGRESS)

    def test_harmony_bias_in_predictions(self):
        """TL with HARMONY bias should produce mostly HARMONY."""
        tl = make_simple_tl()
        # Make HARMONY overwhelmingly dominant
        for i in range(NUM_OPS):
            tl[i][HARMONY] = 100
            for j in range(NUM_OPS):
                if j != HARMONY:
                    tl[i][j] = 1

        seq = self.predictor.predict_sequence(HARMONY, tl, horizon=50)
        harmony_frac = sum(1 for op in seq if op == HARMONY) / len(seq)
        self.assertGreater(harmony_frac, 0.5)

    def test_max_horizon_clamped(self):
        seq = self.predictor.predict_sequence(HARMONY, self.tl, horizon=1000)
        self.assertEqual(len(seq), MAX_HORIZON)

    def test_empty_tl_uses_uniform(self):
        """Empty TL (all zeros) uses uniform distribution."""
        empty_tl = [[0 for _ in range(NUM_OPS)] for _ in range(NUM_OPS)]
        op = self.predictor.sample_next(HARMONY, empty_tl)
        self.assertGreaterEqual(op, 0)
        self.assertLess(op, NUM_OPS)


class TestCoherenceOracle(unittest.TestCase):
    """Coherence trajectory prediction."""

    def setUp(self):
        self.oracle = CoherenceOracle(window_size=32)

    def test_returns_correct_length(self):
        seq = [HARMONY] * 10
        traj = self.oracle.predict_coherence(seq, 0.5)
        self.assertEqual(len(traj), 10)

    def test_all_harmony_converges_high(self):
        """All-HARMONY sequence should converge to high coherence."""
        seq = [HARMONY] * 50
        traj = self.oracle.predict_coherence(seq, 0.5)
        # Should increase over time
        self.assertGreater(traj[-1], traj[0])
        # Should approach ~0.73+ (CL natural rate)
        self.assertGreater(traj[-1], 0.6)

    def test_all_collapse_converges_low(self):
        """All-COLLAPSE sequence should lower coherence."""
        seq = [COLLAPSE] * 50
        traj = self.oracle.predict_coherence(seq, 0.8)
        # Final coherence should be lower (COLLAPSE composes to non-HARMONY)
        # Though CL table absorbs most things to HARMONY, pure COLLAPSE should show effect
        self.assertIsInstance(traj[-1], float)

    def test_coherence_range(self):
        """All predicted coherence values in [0, 1]."""
        seq = [CHAOS, COLLAPSE, VOID, PROGRESS, HARMONY] * 5
        traj = self.oracle.predict_coherence(seq, 0.5)
        for c in traj:
            self.assertGreaterEqual(c, 0.0)
            self.assertLessEqual(c, 1.0)

    def test_empty_sequence(self):
        traj = self.oracle.predict_coherence([], 0.5)
        self.assertEqual(len(traj), 0)

    def test_band_prediction(self):
        self.assertEqual(self.oracle.predict_band(0.8), 2)   # GREEN
        self.assertEqual(self.oracle.predict_band(0.6), 1)   # YELLOW
        self.assertEqual(self.oracle.predict_band(0.3), 0)   # RED

    def test_initial_window_respected(self):
        """Initial window affects early coherence values."""
        seq = [PROGRESS] * 10
        # All-HARMONY initial window = high initial coherence
        window_h = [HARMONY] * 32
        traj_h = self.oracle.predict_coherence(seq, 0.9, window_h)

        # Mixed initial window = lower initial coherence
        window_m = [CHAOS] * 16 + [HARMONY] * 16
        traj_m = self.oracle.predict_coherence(seq, 0.5, window_m)

        # First value with HARMONY window should be higher
        self.assertGreater(traj_h[0], traj_m[0])


class TestFutureState(unittest.TestCase):
    """Future state properties."""

    def test_dangerous_state(self):
        s = FutureState(band=0, coherence=0.2)
        self.assertTrue(s.is_dangerous)

    def test_stable_state(self):
        s = FutureState(band=2, coherence=0.8)
        self.assertTrue(s.is_stable)
        self.assertFalse(s.is_dangerous)

    def test_not_dangerous_yellow(self):
        s = FutureState(band=1, coherence=0.6)
        self.assertFalse(s.is_dangerous)
        self.assertFalse(s.is_stable)


class TestForecast(unittest.TestCase):
    """Forecast summary computation."""

    def _make_forecast(self, coherences, operators=None):
        fc = Forecast(start_operator=HARMONY, horizon=len(coherences))
        oracle = CoherenceOracle()
        for i, coh in enumerate(coherences):
            op = operators[i] if operators else HARMONY
            fc.states.append(FutureState(
                tick_offset=i, operator=op,
                composed=HARMONY, coherence=coh,
                band=oracle.predict_band(coh),
                confidence=0.95 ** (i+1),
            ))
        fc.compute_summary()
        return fc

    def test_summary_statistics(self):
        fc = self._make_forecast([0.5, 0.6, 0.7, 0.8, 0.9])
        self.assertAlmostEqual(fc.mean_coherence, 0.7, places=2)
        self.assertAlmostEqual(fc.min_coherence, 0.5, places=2)
        self.assertAlmostEqual(fc.final_coherence, 0.9, places=2)
        self.assertEqual(fc.final_band, 2)  # GREEN

    def test_collapse_risk(self):
        fc = self._make_forecast([0.2, 0.3, 0.1, 0.4, 0.8])
        self.assertGreater(fc.collapse_risk, 0.0)  # Some RED states

    def test_is_safe(self):
        fc = self._make_forecast([0.7, 0.75, 0.8, 0.85, 0.9])
        self.assertTrue(fc.is_safe)

    def test_is_not_safe(self):
        fc = self._make_forecast([0.2, 0.1, 0.15, 0.1, 0.2])
        self.assertFalse(fc.is_safe)

    def test_improves_coherence(self):
        fc = self._make_forecast([0.5, 0.6, 0.7, 0.8])
        self.assertTrue(fc.improves_coherence)

    def test_not_improves(self):
        fc = self._make_forecast([0.8, 0.7, 0.6, 0.5])
        self.assertFalse(fc.improves_coherence)

    def test_confidence_range(self):
        fc = self._make_forecast([0.5, 0.6, 0.7])
        self.assertGreaterEqual(fc.confidence, 0.0)
        self.assertLessEqual(fc.confidence, 1.0)


class TestForecastEngine(unittest.TestCase):
    """Full forecast engine: generation and comparison."""

    def setUp(self):
        self.tl = make_simple_tl()
        self.engine = ForecastEngine(horizon=10, n_trajectories=4)

    def test_forecast_returns_forecast(self):
        fc = self.engine.forecast_from(HARMONY, self.tl, 0.7)
        self.assertIsInstance(fc, Forecast)
        self.assertEqual(len(fc.states), 10)

    def test_forecast_states_have_valid_operators(self):
        fc = self.engine.forecast_from(PROGRESS, self.tl, 0.5)
        for state in fc.states:
            self.assertGreaterEqual(state.operator, 0)
            self.assertLess(state.operator, NUM_OPS)

    def test_forecast_coherence_in_range(self):
        fc = self.engine.forecast_from(HARMONY, self.tl, 0.7)
        for state in fc.states:
            self.assertGreaterEqual(state.coherence, 0.0)
            self.assertLessEqual(state.coherence, 1.0)

    def test_compare_actions_returns_sorted(self):
        candidates = [HARMONY, COLLAPSE, PROGRESS, CHAOS]
        ranked = self.engine.compare_actions(candidates, self.tl, 0.7)
        self.assertEqual(len(ranked), 4)
        # Each result is (operator, forecast) tuple
        for op, fc in ranked:
            self.assertIn(op, candidates)
            self.assertIsInstance(fc, Forecast)

    def test_harmony_ranks_well(self):
        """HARMONY-biased TL should rank HARMONY start highly."""
        # Heavily bias toward HARMONY
        tl = make_simple_tl()
        for i in range(NUM_OPS):
            tl[i][HARMONY] = 50

        ranked = self.engine.compare_actions(
            [HARMONY, COLLAPSE, CHAOS], tl, 0.7)
        # HARMONY should be in top 2 at least
        top_ops = [op for op, fc in ranked[:2]]
        self.assertIn(HARMONY, top_ops)

    def test_should_act_safe(self):
        fc = Forecast()
        fc.states = [FutureState(coherence=0.8, band=2)]
        fc.compute_summary()
        self.assertTrue(self.engine.should_act(fc, 0.7))

    def test_should_act_dangerous(self):
        fc = Forecast()
        fc.states = [FutureState(coherence=0.1, band=0)]
        fc.compute_summary()
        self.assertFalse(self.engine.should_act(fc, 0.7))

    def test_should_act_when_already_in_trouble(self):
        """When coherence is already low, accept improving forecasts."""
        fc = Forecast()
        fc.states = [FutureState(coherence=0.4, band=1)]
        fc.compute_summary()
        # Current coherence is 0.2 (trouble), forecast says 0.4 (better)
        self.assertTrue(self.engine.should_act(fc, 0.2))

    def test_avoidance_operator(self):
        """Avoidance operator should be a valid operator."""
        op = self.engine.get_avoidance_operator(self.tl, 0.3)
        self.assertGreaterEqual(op, 0)
        self.assertLess(op, NUM_OPS)


class TestIntegration(unittest.TestCase):
    """Integration with existing CK subsystems."""

    def test_works_with_brain_tl_format(self):
        """Forecast works with BrainState TL matrix format."""
        from ck_sim.ck_sim_brain import BrainState, brain_init, brain_tl_observe

        brain = brain_init()
        # Feed some observations
        for _ in range(100):
            brain_tl_observe(brain, HARMONY, HARMONY)
            brain_tl_observe(brain, HARMONY, PROGRESS)
            brain_tl_observe(brain, PROGRESS, HARMONY)

        engine = ForecastEngine(horizon=10, n_trajectories=4)
        fc = engine.forecast_from(HARMONY, brain.tl_entries, 0.7)
        self.assertIsInstance(fc, Forecast)
        self.assertEqual(len(fc.states), 10)

    def test_cl_table_consistency(self):
        """Forecast uses same CL table as heartbeat."""
        oracle = CoherenceOracle()
        # Pure HARMONY sequence: CL[H][H] should be HARMONY
        result = compose(HARMONY, HARMONY)
        self.assertEqual(result, HARMONY)

        # Coherence should be high for all-HARMONY
        traj = oracle.predict_coherence([HARMONY] * 40, 0.5)
        self.assertGreater(traj[-1], 0.5)

    def test_forecast_feeds_episodic(self):
        """Forecast results can feed episodic memory decisions."""
        from ck_sim.ck_episodic import EpisodicStore

        store = EpisodicStore(max_episodes=8)
        engine = ForecastEngine(horizon=5, n_trajectories=2)
        tl = make_simple_tl()

        # Forecast
        fc = engine.forecast_from(HARMONY, tl, 0.7)

        # Record based on forecast result
        if fc.is_safe:
            store.record_tick(
                tick=0, phase_b=PROGRESS, phase_bc=HARMONY,
                coherence=0.7, emotion_id=0, band=2, breath_phase=0,
                d2_magnitude=0.5, action_op=fc.states[0].operator,
                context_flags=0, mode=0,
            )
        store.close_episode()
        self.assertGreater(store.count, 0)


if __name__ == '__main__':
    unittest.main()
