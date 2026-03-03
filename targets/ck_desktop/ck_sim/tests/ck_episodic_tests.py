"""
ck_episodic_tests.py -- Tests for Episodic Memory
===================================================
Validates: event packing, episode lifecycle, saliency scoring,
boundary detection, recall queries, consolidation, persistence,
narrative arc extraction, and engine integration.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import os
import struct
import tempfile
import unittest

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, COLLAPSE, CHAOS, PROGRESS,
    BREATH, BALANCE, COUNTER, LATTICE, RESET, CL, OP_NAMES
)
from ck_sim.ck_episodic import (
    EventSnapshot, Episode, EpisodicStore, SaliencyEngine,
    build_context_flags,
    MAX_EPISODES, MAX_EVENTS_PER_EPISODE, EVENT_PACK_SIZE,
    BOUNDARY_BAND_CHANGE, BOUNDARY_MODE_CHANGE,
    BOUNDARY_EMOTION_SHIFT, BOUNDARY_MAX_LENGTH,
    BOUNDARY_OBSTACLE, BOUNDARY_MANUAL,
    SALIENCY_THRESHOLD, CONSOLIDATION_AGE,
)


class TestImport(unittest.TestCase):
    """Module imports without error."""

    def test_import(self):
        import ck_sim.ck_episodic
        self.assertTrue(hasattr(ck_sim.ck_episodic, 'EpisodicStore'))
        self.assertTrue(hasattr(ck_sim.ck_episodic, 'EventSnapshot'))
        self.assertTrue(hasattr(ck_sim.ck_episodic, 'Episode'))
        self.assertTrue(hasattr(ck_sim.ck_episodic, 'SaliencyEngine'))


class TestEventSnapshot(unittest.TestCase):
    """EventSnapshot packing and unpacking."""

    def test_pack_size(self):
        """Packed event is exactly 8 bytes."""
        ev = EventSnapshot()
        self.assertEqual(len(ev.pack()), EVENT_PACK_SIZE)

    def test_roundtrip(self):
        """Pack then unpack preserves all fields."""
        ev = EventSnapshot(
            tick_offset=42,
            phase_b=PROGRESS,
            phase_bc=HARMONY,
            coherence=180,
            emotion_id=5,
            band=2,
            breath_phase=1,
            d2_magnitude=128,
            saliency=200,
            action_op=BREATH,
            context_flags=0b10100101,
        )
        data = ev.pack()
        ev2 = EventSnapshot.unpack(data)

        self.assertEqual(ev2.tick_offset, 42)
        self.assertEqual(ev2.phase_b, PROGRESS)
        self.assertEqual(ev2.phase_bc, HARMONY)
        self.assertEqual(ev2.coherence, 180)
        self.assertEqual(ev2.emotion_id, 5)
        self.assertEqual(ev2.band, 2)
        self.assertEqual(ev2.breath_phase, 1)
        self.assertEqual(ev2.d2_magnitude, 128)
        self.assertEqual(ev2.saliency, 200)
        self.assertEqual(ev2.action_op, BREATH)
        self.assertEqual(ev2.context_flags, 0b10100101)

    def test_context_flag_properties(self):
        """Context flag bitfield accessors work."""
        ev = EventSnapshot(context_flags=0xFF)
        self.assertTrue(ev.has_obstacle)
        self.assertTrue(ev.has_voice)
        self.assertTrue(ev.is_bonded)
        self.assertTrue(ev.has_bump)
        self.assertTrue(ev.has_crystal)
        self.assertTrue(ev.has_immune)
        self.assertTrue(ev.is_moving)
        self.assertTrue(ev.is_charging)

        ev2 = EventSnapshot(context_flags=0x00)
        self.assertFalse(ev2.has_obstacle)
        self.assertFalse(ev2.has_voice)

    def test_coherence_float(self):
        """Q0.8 coherence converts to float correctly."""
        ev = EventSnapshot(coherence=255)
        self.assertAlmostEqual(ev.coherence_float, 1.0, places=2)

        ev2 = EventSnapshot(coherence=0)
        self.assertAlmostEqual(ev2.coherence_float, 0.0, places=2)

        ev3 = EventSnapshot(coherence=128)
        self.assertAlmostEqual(ev3.coherence_float, 0.502, places=2)

    def test_operator_triad_packing(self):
        """phase_b and phase_bc pack into single byte correctly."""
        for pb in range(NUM_OPS):
            for pbc in range(NUM_OPS):
                ev = EventSnapshot(phase_b=pb, phase_bc=pbc)
                ev2 = EventSnapshot.unpack(ev.pack())
                self.assertEqual(ev2.phase_b, pb)
                self.assertEqual(ev2.phase_bc, pbc)


class TestBuildContextFlags(unittest.TestCase):
    """Context flag builder helper."""

    def test_empty(self):
        self.assertEqual(build_context_flags(), 0)

    def test_all_set(self):
        flags = build_context_flags(
            obstacle=True, voice=True, bonded=True, bump=True,
            crystal=True, immune=True, moving=True, charging=True
        )
        self.assertEqual(flags, 0xFF)

    def test_individual_bits(self):
        self.assertEqual(build_context_flags(obstacle=True), 0x80)
        self.assertEqual(build_context_flags(voice=True), 0x40)
        self.assertEqual(build_context_flags(bonded=True), 0x20)
        self.assertEqual(build_context_flags(bump=True), 0x10)
        self.assertEqual(build_context_flags(crystal=True), 0x08)
        self.assertEqual(build_context_flags(immune=True), 0x04)
        self.assertEqual(build_context_flags(moving=True), 0x02)
        self.assertEqual(build_context_flags(charging=True), 0x01)


class TestSaliencyEngine(unittest.TestCase):
    """Saliency computation."""

    def setUp(self):
        self.engine = SaliencyEngine()

    def test_returns_float(self):
        """Saliency is a float in [0, 1]."""
        s = self.engine.compute(0.7, HARMONY, 0.5, 0, False, 2.0)
        self.assertIsInstance(s, float)
        self.assertGreaterEqual(s, 0.0)
        self.assertLessEqual(s, 1.0)

    def test_bump_increases_saliency(self):
        """Quantum bump should significantly increase saliency."""
        # Feed some baseline
        for _ in range(5):
            self.engine.compute(0.7, HARMONY, 0.3, 0, False, 2.0)

        s_no_bump = self.engine.compute(0.7, HARMONY, 0.3, 0, False, 2.0)
        # Reset and measure with bump
        engine2 = SaliencyEngine()
        for _ in range(5):
            engine2.compute(0.7, HARMONY, 0.3, 0, False, 2.0)
        s_bump = engine2.compute(0.7, HARMONY, 0.3, 0, True, 2.0)

        self.assertGreater(s_bump, s_no_bump)

    def test_coherence_drop_increases_saliency(self):
        """Sudden coherence drop should be salient."""
        # Build stable history
        for _ in range(10):
            self.engine.compute(0.8, HARMONY, 0.3, 0, False, 2.0)

        # Sudden drop
        s = self.engine.compute(0.2, COLLAPSE, 0.8, 0x80, False, 3.0)
        # This should be relatively high due to coherence derivative + context change
        self.assertGreater(s, 0.1)

    def test_high_emotion_increases_saliency(self):
        """High emotional intensity should increase saliency."""
        # Baseline
        for _ in range(5):
            self.engine.compute(0.7, HARMONY, 0.0, 0, False, 2.0)
        s_low = self.engine.compute(0.7, HARMONY, 0.0, 0, False, 2.0)

        engine2 = SaliencyEngine()
        for _ in range(5):
            engine2.compute(0.7, HARMONY, 0.0, 0, False, 2.0)
        s_high = engine2.compute(0.7, HARMONY, 1.0, 0, False, 2.0)

        self.assertGreater(s_high, s_low)


class TestEpisode(unittest.TestCase):
    """Episode lifecycle and summary statistics."""

    def _make_episode(self, n_events=10, base_op=HARMONY, base_coherence=0.7):
        """Helper: create episode with N events."""
        ep = Episode(episode_id=1, start_tick=1000, boundary_type=BOUNDARY_MANUAL)
        for i in range(n_events):
            ev = EventSnapshot(
                tick_offset=i,
                phase_b=PROGRESS,
                phase_bc=base_op,
                coherence=int(base_coherence * 255),
                emotion_id=0,  # calm
                band=2,  # green
                breath_phase=i % 4,
                d2_magnitude=128,
                saliency=int(0.5 * 255),
                action_op=base_op,
                context_flags=0,
            )
            ep.add_event(ev)
        ep.close()
        return ep

    def test_close_computes_stats(self):
        """Episode.close() fills summary fields."""
        ep = self._make_episode(10, HARMONY, 0.7)
        self.assertEqual(ep.dominant_operator, HARMONY)
        self.assertAlmostEqual(ep.mean_coherence, 0.7, places=1)
        self.assertGreater(ep.peak_saliency, 0.0)
        self.assertEqual(ep.event_count, 10)

    def test_operator_distribution(self):
        """Operator distribution sums to ~1.0."""
        ep = self._make_episode(20, PROGRESS, 0.6)
        dist_sum = sum(ep.operator_distribution)
        self.assertAlmostEqual(dist_sum, 1.0, places=2)
        self.assertEqual(ep.dominant_operator, PROGRESS)

    def test_duration(self):
        """Duration computed from tick offsets."""
        ep = self._make_episode(10)
        self.assertEqual(ep.duration_ticks, 9)  # tick_offset 0..9

    def test_importance_range(self):
        """Importance is in [0, 1]."""
        ep = self._make_episode(10)
        self.assertGreaterEqual(ep.importance, 0.0)
        self.assertLessEqual(ep.importance, 1.0)

    def test_pack_unpack_roundtrip(self):
        """Episode serializes and deserializes correctly."""
        ep = self._make_episode(5, COLLAPSE, 0.3)
        data = ep.pack()

        ep2, consumed = Episode.unpack(data)
        self.assertEqual(ep2.episode_id, ep.episode_id)
        self.assertEqual(ep2.start_tick, ep.start_tick)
        self.assertEqual(ep2.dominant_operator, ep.dominant_operator)
        self.assertEqual(ep2.event_count, ep.event_count)
        self.assertAlmostEqual(ep2.mean_coherence, ep.mean_coherence, places=3)

    def test_empty_episode(self):
        """Empty episode close doesn't crash."""
        ep = Episode()
        ep.close()
        self.assertEqual(ep.event_count, 0)


class TestEpisodicStore(unittest.TestCase):
    """EpisodicStore lifecycle, recording, and recall."""

    def setUp(self):
        self.store = EpisodicStore(max_episodes=16)

    def _record_n_ticks(self, n, start_tick=0, band=2, mode=0,
                         emotion_id=0, operator=HARMONY, coherence=0.7):
        """Helper: record N ticks with consistent state."""
        for i in range(n):
            self.store.record_tick(
                tick=start_tick + i,
                phase_b=PROGRESS,
                phase_bc=operator,
                coherence=coherence,
                emotion_id=emotion_id,
                band=band,
                breath_phase=i % 4,
                d2_magnitude=0.5,
                action_op=operator,
                context_flags=0,
                emotion_intensity=0.3,
                bump=False,
                tl_entropy=2.0,
                mode=mode,
            )

    def test_recording_creates_episode(self):
        """Recording ticks creates at least one episode."""
        self._record_n_ticks(10)
        self.store.close_episode()  # Force close the open episode
        self.assertGreater(self.store.count, 0)

    def test_band_change_creates_boundary(self):
        """Band change triggers new episode."""
        # Record in GREEN band
        self._record_n_ticks(5, start_tick=0, band=2)
        # Switch to RED band
        self._record_n_ticks(5, start_tick=5, band=0)
        self.store.close_episode()

        # Should have at least 2 episodes (boundary at band change)
        self.assertGreaterEqual(self.store.count, 2)

    def test_emotion_change_creates_boundary(self):
        """Emotion change triggers new episode."""
        self._record_n_ticks(5, start_tick=0, emotion_id=0)  # calm
        self._record_n_ticks(5, start_tick=5, emotion_id=2)  # stress
        self.store.close_episode()
        self.assertGreaterEqual(self.store.count, 2)

    def test_mode_change_creates_boundary(self):
        """Brain mode change triggers new episode."""
        self._record_n_ticks(5, start_tick=0, mode=0)  # OBSERVE
        self._record_n_ticks(5, start_tick=5, mode=3)  # SOVEREIGN
        self.store.close_episode()
        self.assertGreaterEqual(self.store.count, 2)

    def test_max_events_creates_boundary(self):
        """Exceeding MAX_EVENTS_PER_EPISODE forces new episode."""
        self._record_n_ticks(MAX_EVENTS_PER_EPISODE + 5)
        self.store.close_episode()
        self.assertGreaterEqual(self.store.count, 2)

    def test_ring_buffer_overwrites(self):
        """Store never exceeds max_episodes."""
        store = EpisodicStore(max_episodes=4)
        for i in range(20):
            store.begin_episode(tick=i * 100, boundary_type=BOUNDARY_MANUAL)
            for j in range(3):
                store.record_tick(
                    tick=i * 100 + j, phase_b=0, phase_bc=HARMONY,
                    coherence=0.7, emotion_id=0, band=2, breath_phase=0,
                    d2_magnitude=0.5, action_op=0, context_flags=0,
                    mode=0,
                )
            store.close_episode()

        valid = sum(1 for ep in store.episodes if ep is not None)
        self.assertLessEqual(valid, 4)

    def test_recall_by_operator(self):
        """Recall episodes dominated by specific operator."""
        # HARMONY episodes
        self._record_n_ticks(10, start_tick=0, operator=HARMONY)
        self.store.close_episode()
        # COLLAPSE episodes
        self._record_n_ticks(10, start_tick=100, operator=COLLAPSE, band=0)
        self.store.close_episode()

        harmony_eps = self.store.recall_by_operator(HARMONY, limit=5)
        self.assertGreater(len(harmony_eps), 0)
        self.assertEqual(harmony_eps[0].dominant_operator, HARMONY)

    def test_recall_by_emotion(self):
        """Recall episodes by dominant emotion."""
        self._record_n_ticks(10, start_tick=0, emotion_id=5)  # joy
        self.store.close_episode()
        self._record_n_ticks(10, start_tick=100, emotion_id=2)  # stress
        self.store.close_episode()

        joy_eps = self.store.recall_by_emotion(5, limit=5)
        self.assertGreater(len(joy_eps), 0)
        self.assertEqual(joy_eps[0].dominant_emotion, 5)

    def test_recall_by_coherence_range(self):
        """Recall episodes by coherence range."""
        self._record_n_ticks(10, start_tick=0, coherence=0.9)
        self.store.close_episode()
        self._record_n_ticks(10, start_tick=100, coherence=0.2, band=0)
        self.store.close_episode()

        high_coh = self.store.recall_by_coherence_range(0.8, 1.0, limit=5)
        self.assertGreater(len(high_coh), 0)
        self.assertGreater(high_coh[0].mean_coherence, 0.7)

    def test_recall_by_pattern(self):
        """Recall by operator distribution similarity."""
        self._record_n_ticks(10, start_tick=0, operator=HARMONY)
        self.store.close_episode()

        # Query with HARMONY-heavy distribution
        query = [0.0] * NUM_OPS
        query[HARMONY] = 1.0
        results = self.store.recall_by_pattern(query, limit=5)
        self.assertGreater(len(results), 0)

    def test_recall_recent(self):
        """Recent recall returns newest episodes first."""
        self._record_n_ticks(5, start_tick=0)
        self.store.close_episode()
        self._record_n_ticks(5, start_tick=1000, band=0)
        self.store.close_episode()

        recent = self.store.recall_recent(limit=5)
        self.assertGreater(len(recent), 0)
        # First result should be the newer episode
        if len(recent) >= 2:
            self.assertGreater(recent[0].start_tick, recent[1].start_tick)

    def test_recall_important(self):
        """Important recall returns highest-importance episodes first."""
        self._record_n_ticks(10, start_tick=0, coherence=0.9)
        self.store.close_episode()

        important = self.store.recall_important(limit=5)
        self.assertGreater(len(important), 0)

    def test_recall_by_context_flags(self):
        """Recall by context flag mask."""
        # Episode with obstacle
        self.store.begin_episode(tick=0, boundary_type=BOUNDARY_MANUAL)
        for i in range(5):
            self.store.record_tick(
                tick=i, phase_b=0, phase_bc=COLLAPSE,
                coherence=0.3, emotion_id=2, band=0, breath_phase=0,
                d2_magnitude=0.8, action_op=COLLAPSE,
                context_flags=build_context_flags(obstacle=True),
                mode=0,
            )
        self.store.close_episode()

        # Episode without obstacle
        self._record_n_ticks(5, start_tick=100)
        self.store.close_episode()

        obstacle_eps = self.store.recall_by_context(0x80, limit=5)
        self.assertGreater(len(obstacle_eps), 0)


class TestConsolidation(unittest.TestCase):
    """Memory consolidation and compression."""

    def setUp(self):
        self.store = EpisodicStore(max_episodes=16)

    def test_consolidation_prunes_events(self):
        """Consolidation removes low-saliency events."""
        self.store.begin_episode(tick=0, boundary_type=BOUNDARY_MANUAL)
        for i in range(20):
            ev = EventSnapshot(
                tick_offset=i, phase_b=0, phase_bc=HARMONY,
                coherence=180, emotion_id=0, band=2, breath_phase=0,
                d2_magnitude=128,
                saliency=10 if i != 10 else 250,  # Only event 10 is salient
                action_op=HARMONY, context_flags=0,
            )
            self.store._current.add_event(ev)
            self.store._event_count_in_current += 1
        self.store.close_episode()

        ep = self.store.episodes[0]
        original_count = ep.event_count

        # Age the episode
        ep.end_tick = 0  # Make it old
        self.store.consolidate(current_tick=CONSOLIDATION_AGE + 100)

        self.assertTrue(ep.consolidated)
        # Should have fewer events after consolidation
        self.assertLess(ep.event_count, original_count)
        # Should still have at least 3 (first, peak, last)
        self.assertGreaterEqual(ep.event_count, 3)

    def test_young_episodes_not_consolidated(self):
        """Episodes younger than CONSOLIDATION_AGE are not touched."""
        self.store.begin_episode(tick=1000, boundary_type=BOUNDARY_MANUAL)
        for i in range(10):
            self.store.record_tick(
                tick=1000 + i, phase_b=0, phase_bc=HARMONY,
                coherence=0.7, emotion_id=0, band=2, breath_phase=0,
                d2_magnitude=0.5, action_op=0, context_flags=0, mode=0,
            )
        self.store.close_episode()

        self.store.consolidate(current_tick=1009 + CONSOLIDATION_AGE - 1)
        ep = self.store.episodes[0]
        self.assertFalse(ep.consolidated)


class TestNarrative(unittest.TestCase):
    """Narrative arc extraction."""

    def test_narrative_arc(self):
        """Narrative arc returns episode summaries in order."""
        store = EpisodicStore(max_episodes=16)

        # Create a few episodes with different states
        for i, (op, band) in enumerate([
            (HARMONY, 2), (COLLAPSE, 0), (PROGRESS, 1), (HARMONY, 2)
        ]):
            store.begin_episode(tick=i * 100, boundary_type=BOUNDARY_BAND_CHANGE)
            for j in range(5):
                store.record_tick(
                    tick=i * 100 + j, phase_b=0, phase_bc=op,
                    coherence=0.3 + band * 0.3, emotion_id=0,
                    band=band, breath_phase=0, d2_magnitude=0.5,
                    action_op=op, context_flags=0, mode=0,
                )
            store.close_episode()

        arc = store.get_narrative_arc(n_episodes=10)
        self.assertGreater(len(arc), 0)
        # Check chronological order
        for i in range(len(arc) - 1):
            self.assertLessEqual(arc[i]['start_tick'], arc[i+1]['start_tick'])

    def test_coherence_trajectory(self):
        """Coherence trajectory returns float list."""
        store = EpisodicStore(max_episodes=16)
        for i in range(5):
            store.begin_episode(tick=i * 50, boundary_type=BOUNDARY_MANUAL)
            for j in range(3):
                store.record_tick(
                    tick=i * 50 + j, phase_b=0, phase_bc=HARMONY,
                    coherence=0.5 + i * 0.1, emotion_id=0,
                    band=2, breath_phase=0, d2_magnitude=0.5,
                    action_op=0, context_flags=0, mode=0,
                )
            store.close_episode()

        traj = store.get_coherence_trajectory(n_episodes=10)
        self.assertGreater(len(traj), 0)
        for val in traj:
            self.assertIsInstance(val, float)
            self.assertGreaterEqual(val, 0.0)
            self.assertLessEqual(val, 1.0)


class TestPersistence(unittest.TestCase):
    """Save/load episodic store."""

    def test_save_load_roundtrip(self):
        """Save and load preserves episodes."""
        store = EpisodicStore(max_episodes=16)

        # Create episodes
        store.begin_episode(tick=0, boundary_type=BOUNDARY_MANUAL)
        for i in range(5):
            store.record_tick(
                tick=i, phase_b=PROGRESS, phase_bc=HARMONY,
                coherence=0.75, emotion_id=0, band=2, breath_phase=i % 4,
                d2_magnitude=0.6, action_op=HARMONY, context_flags=0, mode=0,
            )
        store.close_episode()

        store.begin_episode(tick=100, boundary_type=BOUNDARY_BAND_CHANGE)
        for i in range(3):
            store.record_tick(
                tick=100 + i, phase_b=VOID, phase_bc=COLLAPSE,
                coherence=0.2, emotion_id=2, band=0, breath_phase=0,
                d2_magnitude=0.8, action_op=COLLAPSE,
                context_flags=build_context_flags(obstacle=True), mode=0,
            )
        store.close_episode()

        # Save
        with tempfile.NamedTemporaryFile(suffix='.bin', delete=False) as f:
            tmpfile = f.name
        try:
            store.save(tmpfile)

            # Load into new store
            store2 = EpisodicStore(max_episodes=16)
            ok = store2.load(tmpfile)
            self.assertTrue(ok)
            self.assertEqual(store2.count, store.count)

            # Verify first episode
            ep1 = store2.episodes[0]
            self.assertIsNotNone(ep1)
            self.assertEqual(ep1.event_count, 5)
        finally:
            os.unlink(tmpfile)

    def test_load_nonexistent(self):
        """Loading nonexistent file returns False."""
        store = EpisodicStore()
        ok = store.load('/tmp/nonexistent_ck_episodic.bin')
        self.assertFalse(ok)


class TestStats(unittest.TestCase):
    """Statistics reporting."""

    def test_empty_stats(self):
        """Empty store produces valid stats."""
        store = EpisodicStore()
        s = store.stats()
        self.assertEqual(s['total_episodes'], 0)
        self.assertEqual(s['total_events'], 0)

    def test_nonempty_stats(self):
        """Stats reflect recorded episodes."""
        store = EpisodicStore(max_episodes=16)
        store.begin_episode(tick=0, boundary_type=BOUNDARY_MANUAL)
        for i in range(10):
            store.record_tick(
                tick=i, phase_b=0, phase_bc=HARMONY,
                coherence=0.7, emotion_id=0, band=2, breath_phase=0,
                d2_magnitude=0.5, action_op=0, context_flags=0, mode=0,
            )
        store.close_episode()

        s = store.stats()
        self.assertGreater(s['total_episodes'], 0)
        self.assertGreater(s['total_events'], 0)
        self.assertGreater(s['memory_bytes'], 0)


class TestIntegration(unittest.TestCase):
    """Integration with existing CK subsystems."""

    def test_operators_match_heartbeat(self):
        """Episodic module uses same operator constants as heartbeat."""
        from ck_sim.ck_episodic import NUM_OPS as EP_NUM_OPS
        self.assertEqual(EP_NUM_OPS, NUM_OPS)

    def test_cl_composition_in_episode(self):
        """CL composition works within episode context."""
        from ck_sim.ck_sim_heartbeat import compose
        # Simulate what happens in an episode: Being composes with Doing
        result = compose(PROGRESS, HARMONY)
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
        self.assertLess(result, NUM_OPS)

    def test_full_lifecycle(self):
        """Complete lifecycle: record -> consolidate -> recall -> save -> load."""
        store = EpisodicStore(max_episodes=32)

        # Phase 1: Record a story
        # Act 1: calm exploration (GREEN)
        for i in range(20):
            store.record_tick(
                tick=i, phase_b=PROGRESS, phase_bc=HARMONY,
                coherence=0.8, emotion_id=0, band=2, breath_phase=i % 4,
                d2_magnitude=0.4, action_op=HARMONY,
                context_flags=build_context_flags(moving=True),
                mode=0,
            )

        # Act 2: obstacle! (band drops)
        for i in range(10):
            store.record_tick(
                tick=20 + i, phase_b=VOID, phase_bc=COLLAPSE,
                coherence=0.3, emotion_id=2, band=0, breath_phase=i % 4,
                d2_magnitude=0.9, action_op=COLLAPSE,
                context_flags=build_context_flags(obstacle=True),
                bump=True if i == 0 else False,
                mode=0,
            )

        # Act 3: recovery (back to GREEN)
        for i in range(15):
            store.record_tick(
                tick=30 + i, phase_b=BALANCE, phase_bc=HARMONY,
                coherence=0.6 + i * 0.02, emotion_id=7, band=1, breath_phase=i % 4,
                d2_magnitude=0.5, action_op=HARMONY,
                context_flags=0, mode=1,
            )

        store.close_episode()

        # Phase 2: Verify story structure
        self.assertGreater(store.count, 1)  # Multiple episodes from state changes

        # Phase 3: Recall
        collapse_eps = store.recall_by_operator(COLLAPSE)
        self.assertGreater(len(collapse_eps), 0)

        obstacle_eps = store.recall_by_context(0x80)
        self.assertGreater(len(obstacle_eps), 0)

        # Phase 4: Narrative
        arc = store.get_narrative_arc()
        self.assertGreater(len(arc), 0)

        # Phase 5: Stats
        s = store.stats()
        self.assertGreater(s['total_episodes'], 0)
        self.assertGreater(s['total_events'], 10)

        # Phase 6: Persistence
        with tempfile.NamedTemporaryFile(suffix='.bin', delete=False) as f:
            tmpfile = f.name
        try:
            store.save(tmpfile)
            store2 = EpisodicStore(max_episodes=32)
            ok = store2.load(tmpfile)
            self.assertTrue(ok)
            self.assertEqual(store2.count, store.count)
        finally:
            os.unlink(tmpfile)


if __name__ == '__main__':
    unittest.main()
