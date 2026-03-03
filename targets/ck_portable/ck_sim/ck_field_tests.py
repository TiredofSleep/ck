"""
ck_field_tests.py -- N-Dimensional Coherence Field Tests
=========================================================
Operator: COUNTER (2) -- measuring correctness.

Tests for: soft classification, OperatorStream, CoherenceField,
CrossModalCrystal, consensus, UniversalTranslator, backward
compatibility, and performance.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import time
import unittest

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, CHAOS, LATTICE, COUNTER,
    PROGRESS, COLLAPSE, BALANCE, BREATH, RESET,
    compose, OP_NAMES
)
from ck_sim.ck_sim_d2 import (
    D2Pipeline, soft_classify_d2, classify_force_d2
)
from ck_sim.ck_coherence_field import (
    OperatorStream, CoherenceField, CrossModalCrystal
)
from ck_sim.ck_personality import CurvatureMemory
from ck_sim.ck_emotion import PFE
from ck_sim.ck_translator import (
    UniversalTranslator, SpeciesProfile, TranslationResult,
    PROFILE_DOG, PROFILE_CAT, PROFILE_HUMAN, PROFILE_CK,
)


# ================================================================
#  SOFT CLASSIFICATION TESTS
# ================================================================

class TestSoftClassify(unittest.TestCase):
    """Soft D2 classification: 5D vector -> 10-value distribution."""

    def test_distribution_sums_to_one(self):
        """Distribution always sums to 1.0."""
        vecs = [
            [0.5, -0.2, 0.1, 0.3, -0.1],
            [0.0, 0.0, 0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0, 0.0, 0.0],
            [-0.3, 0.7, -0.1, 0.2, 0.4],
        ]
        for vec in vecs:
            dist = soft_classify_d2(vec)
            self.assertAlmostEqual(sum(dist), 1.0, places=6,
                                   msg=f"Distribution doesn't sum to 1.0 for {vec}")

    def test_zero_vector_is_void(self):
        """Zero D2 = VOID."""
        dist = soft_classify_d2([0.0, 0.0, 0.0, 0.0, 0.0])
        self.assertEqual(dist[VOID], 1.0)

    def test_dominant_dimension_wins(self):
        """Largest D2 dimension should produce highest probability."""
        # D2 = [0.9, 0.0, 0.0, 0.0, 0.0] -> aperture dominant -> CHAOS (positive)
        dist = soft_classify_d2([0.9, 0.0, 0.0, 0.0, 0.0])
        max_op = max(range(NUM_OPS), key=lambda i: dist[i])
        self.assertEqual(max_op, CHAOS)  # aperture positive = CHAOS

    def test_negative_dimension(self):
        """Negative D2 -> negative operator from pair."""
        dist = soft_classify_d2([-0.9, 0.0, 0.0, 0.0, 0.0])
        max_op = max(range(NUM_OPS), key=lambda i: dist[i])
        self.assertEqual(max_op, LATTICE)  # aperture negative = LATTICE

    def test_pipeline_soft_classify(self):
        """D2Pipeline.soft_classify() returns valid distribution."""
        pipe = D2Pipeline()
        for ch in "hello":
            pipe.feed_symbol(ord(ch) - ord('a'))
        dist = pipe.soft_classify()
        self.assertEqual(len(dist), NUM_OPS)
        self.assertAlmostEqual(sum(dist), 1.0, places=6)

    def test_pipeline_d2_vector(self):
        """D2Pipeline.d2_vector returns 5D float list."""
        pipe = D2Pipeline()
        for ch in "abc":
            pipe.feed_symbol(ord(ch) - ord('a'))
        vec = pipe.d2_vector
        self.assertEqual(len(vec), 5)
        self.assertTrue(all(isinstance(v, float) for v in vec))

    def test_ten_values(self):
        """Distribution always has exactly 10 values."""
        dist = soft_classify_d2([0.3, -0.1, 0.5, 0.2, -0.4])
        self.assertEqual(len(dist), 10)


# ================================================================
#  OPERATOR STREAM TESTS
# ================================================================

class TestOperatorStream(unittest.TestCase):
    """OperatorStream: per-modality ring buffer with D2 preservation."""

    def test_feed_and_fill(self):
        """Feed operators, check fill count."""
        stream = OperatorStream("test")
        self.assertEqual(stream.fill, 0)
        stream.feed(HARMONY)
        self.assertEqual(stream.fill, 1)
        for i in range(10):
            stream.feed(CHAOS)
        self.assertEqual(stream.fill, 11)

    def test_self_coherence(self):
        """All HARMONY = coherence 1.0."""
        stream = OperatorStream("test")
        for _ in range(20):
            stream.feed(HARMONY)
        self.assertAlmostEqual(stream.self_coherence, 1.0)

    def test_self_coherence_zero(self):
        """No HARMONY = coherence 0.0."""
        stream = OperatorStream("test")
        for _ in range(20):
            stream.feed(CHAOS)
        self.assertAlmostEqual(stream.self_coherence, 0.0)

    def test_self_coherence_mixed(self):
        """Mixed operators = partial coherence."""
        stream = OperatorStream("test")
        for _ in range(10):
            stream.feed(HARMONY)
        for _ in range(10):
            stream.feed(CHAOS)
        coh = stream.self_coherence
        self.assertGreater(coh, 0.0)
        self.assertLess(coh, 1.0)

    def test_ring_buffer_overflow(self):
        """Buffer wraps at 32 entries."""
        stream = OperatorStream("test", buffer_size=32)
        for _ in range(100):
            stream.feed(HARMONY)
        self.assertEqual(stream.fill, 32)

    def test_d2_vector_storage(self):
        """D2 vectors are preserved."""
        stream = OperatorStream("test")
        vec = [0.1, -0.2, 0.3, -0.4, 0.5]
        stream.feed(HARMONY, vec)
        self.assertEqual(stream.current_d2, vec)

    def test_soft_distribution(self):
        """Soft distribution from D2 vector."""
        stream = OperatorStream("test")
        vec = [0.5, -0.2, 0.1, 0.3, -0.1]
        stream.feed(HARMONY, vec)
        dist = stream.distribution
        self.assertEqual(len(dist), NUM_OPS)
        self.assertAlmostEqual(sum(dist), 1.0, places=5)

    def test_current_operator(self):
        """current_operator returns last fed operator."""
        stream = OperatorStream("test")
        self.assertEqual(stream.current_operator, VOID)
        stream.feed(PROGRESS)
        self.assertEqual(stream.current_operator, PROGRESS)

    def test_recent_operators(self):
        """recent_operators returns last N."""
        stream = OperatorStream("test")
        ops = [HARMONY, CHAOS, PROGRESS, BALANCE, VOID]
        for op in ops:
            stream.feed(op)
        recent = stream.recent_operators(3)
        self.assertEqual(recent, [PROGRESS, BALANCE, VOID])


# ================================================================
#  COHERENCE FIELD TESTS
# ================================================================

class TestCoherenceField(unittest.TestCase):
    """CoherenceField: N×N cross-modal coherence matrix."""

    def _make_field(self, n_streams=3):
        """Helper: create field with n streams."""
        field = CoherenceField()
        streams = []
        for i in range(n_streams):
            s = OperatorStream(f"stream_{i}")
            s.active = True
            field.register_stream(s)
            streams.append(s)
        return field, streams

    def test_empty_field(self):
        """Empty field = zero coherence."""
        field = CoherenceField()
        field.tick(0)
        self.assertEqual(field.field_coherence, 0.0)

    def test_matrix_dimensions(self):
        """N streams -> N×N matrix."""
        field, streams = self._make_field(3)
        # Feed some data
        for s in streams:
            for _ in range(5):
                s.feed(HARMONY)
        field.tick(0)
        matrix = field.matrix
        self.assertEqual(len(matrix), 3)
        for row in matrix:
            self.assertEqual(len(row), 3)

    def test_matrix_symmetric(self):
        """Cross-coherence matrix is symmetric."""
        field, streams = self._make_field(3)
        ops = [HARMONY, CHAOS, PROGRESS]
        for i, s in enumerate(streams):
            for _ in range(10):
                s.feed(ops[i % len(ops)])
        field.tick(0)
        matrix = field.matrix
        for i in range(3):
            for j in range(3):
                self.assertAlmostEqual(matrix[i][j], matrix[j][i], places=10)

    def test_diagonal_is_self_coherence(self):
        """Diagonal = each stream's self-coherence."""
        field, streams = self._make_field(2)
        # Stream 0: all HARMONY
        for _ in range(10):
            streams[0].feed(HARMONY)
        # Stream 1: all CHAOS
        for _ in range(10):
            streams[1].feed(CHAOS)
        field.tick(0)
        matrix = field.matrix
        self.assertAlmostEqual(matrix[0][0], streams[0].self_coherence)
        self.assertAlmostEqual(matrix[1][1], streams[1].self_coherence)

    def test_identical_streams_high_coherence(self):
        """Two identical HARMONY streams = high cross-coherence."""
        field, streams = self._make_field(2)
        for _ in range(10):
            streams[0].feed(HARMONY)
            streams[1].feed(HARMONY)
        field.tick(0)
        matrix = field.matrix
        # CL[HARMONY][HARMONY] = HARMONY, so 100% cross-coherence
        self.assertAlmostEqual(matrix[0][1], 1.0)

    def test_field_coherence_range(self):
        """Field coherence is in [0, 1]."""
        field, streams = self._make_field(3)
        for s in streams:
            for _ in range(10):
                s.feed(HARMONY)
        field.tick(0)
        fc = field.field_coherence
        self.assertGreaterEqual(fc, 0.0)
        self.assertLessEqual(fc, 1.0)

    def test_consensus_operator(self):
        """All streams HARMONY -> consensus = HARMONY."""
        field, streams = self._make_field(3)
        for s in streams:
            for _ in range(10):
                s.feed(HARMONY)
        field.tick(0)
        # When all streams just do hard HARMONY with no D2 vector,
        # soft dist = [0]*7 + [1.0] + [0]*2 -> consensus = HARMONY
        self.assertEqual(field.consensus_operator, HARMONY)

    def test_consensus_confidence(self):
        """All-HARMONY streams = high confidence."""
        field, streams = self._make_field(2)
        for s in streams:
            for _ in range(10):
                s.feed(HARMONY)
        field.tick(0)
        self.assertGreater(field.consensus_confidence, 0.5)

    def test_inactive_stream_ignored(self):
        """Inactive stream doesn't affect field."""
        field, streams = self._make_field(2)
        streams[1].active = False
        for _ in range(10):
            streams[0].feed(HARMONY)
        field.tick(0)
        # Only 1 active stream, field = self-coherence of that stream
        self.assertGreater(field.field_coherence, 0.0)

    def test_scalar_coherence_backward_compat(self):
        """scalar_coherence falls back to heartbeat or field."""
        field = CoherenceField()
        hb = OperatorStream("heartbeat")
        hb.active = True
        field.register_stream(hb)
        for _ in range(10):
            hb.feed(HARMONY)
        field.tick(0)
        # Should return heartbeat self-coherence
        self.assertAlmostEqual(field.scalar_coherence, hb.self_coherence)

    def test_crystal_detection(self):
        """High cross-coherence -> crystal formed."""
        field = CoherenceField(crystal_threshold=0.8)
        s1 = OperatorStream("audio")
        s2 = OperatorStream("text")
        s1.active = True
        s2.active = True
        field.register_stream(s1)
        field.register_stream(s2)
        # Feed identical HARMONY sequences
        for _ in range(10):
            s1.feed(HARMONY)
            s2.feed(HARMONY)
        # Tick at tick_number divisible by 8 to trigger crystal detection
        field.tick(8)
        self.assertGreater(len(field.crystals), 0)

    def test_stream_names(self):
        """stream_names returns registered names."""
        field, streams = self._make_field(3)
        names = field.stream_names
        self.assertEqual(names, ["stream_0", "stream_1", "stream_2"])

    def test_summary(self):
        """summary() returns non-empty string."""
        field, streams = self._make_field(2)
        field.tick(0)
        s = field.summary()
        self.assertIn("Field", s)


# ================================================================
#  PERSONALITY 5D BACKWARD COMPAT TESTS
# ================================================================

class TestCMEM5D(unittest.TestCase):
    """CurvatureMemory with 5D vector support."""

    def test_scalar_unchanged(self):
        """Scalar feed still works exactly as before."""
        cmem = CurvatureMemory(n_taps=8)
        for i in range(10):
            out = cmem.feed(0.5)
        self.assertGreater(out, 0.0)

    def test_vector_auto_detect(self):
        """Passing a 5-element list auto-detects as vector."""
        cmem = CurvatureMemory(n_taps=8)
        vec = [0.1, -0.2, 0.3, -0.4, 0.5]
        out = cmem.feed(vec)
        # Should have computed magnitude and filtered
        self.assertGreater(out, 0.0)
        # Vector output should be populated
        vout = cmem.vector_output
        self.assertEqual(len(vout), 5)

    def test_vector_variance(self):
        """vector_variance returns 5 floats."""
        cmem = CurvatureMemory(n_taps=8)
        for _ in range(10):
            cmem.feed([0.1, -0.2, 0.3, -0.4, 0.5])
        vvar = cmem.vector_variance
        self.assertEqual(len(vvar), 5)

    def test_set_style_preserves_vector(self):
        """set_style resizes vector buffer too."""
        cmem = CurvatureMemory(n_taps=16)
        for _ in range(10):
            cmem.feed([0.1, -0.2, 0.3, -0.4, 0.5])
        cmem.set_style(4)
        self.assertEqual(cmem.n_taps, 4)
        # Should still work
        out = cmem.feed([0.2, 0.1, 0.0, -0.1, 0.3])
        self.assertIsInstance(out, float)


# ================================================================
#  EMOTION FIELD INPUT TESTS
# ================================================================

class TestEmotionFieldInputs(unittest.TestCase):
    """PFE with optional field_coherence and consensus_confidence."""

    def test_none_inputs_identical(self):
        """field_coherence=None, consensus_confidence=None = no change."""
        pfe = PFE()
        state = pfe.tick(0.7, 0.05, 1.5, 0.8, 0.6, 0.5)
        self.assertIsNotNone(state.primary)

    def test_field_coherence_affects_valence(self):
        """High field_coherence boosts valence."""
        pfe1 = PFE()
        pfe2 = PFE()
        # Same inputs, but pfe2 gets high field coherence
        for _ in range(20):
            s1 = pfe1.tick(0.5, 0.1, 1.5, 0.6, 0.5, 0.5)
            s2 = pfe2.tick(0.5, 0.1, 1.5, 0.6, 0.5, 0.5,
                           field_coherence=0.9)
        # pfe2 should have higher valence due to field boost
        self.assertGreater(s2.valence, s1.valence)

    def test_consensus_reduces_arousal(self):
        """High consensus_confidence reduces arousal."""
        pfe1 = PFE()
        pfe2 = PFE()
        for _ in range(20):
            s1 = pfe1.tick(0.5, 0.3, 2.0, 0.5, 0.4, 0.5)
            s2 = pfe2.tick(0.5, 0.3, 2.0, 0.5, 0.4, 0.5,
                           consensus_confidence=0.9)
        self.assertLess(s2.arousal, s1.arousal)


# ================================================================
#  UNIVERSAL TRANSLATOR TESTS
# ================================================================

class TestUniversalTranslator(unittest.TestCase):
    """UniversalTranslator: cross-species communication via D2."""

    def test_dog_bark(self):
        """Dog CHAOS+COUNTER = 'Back off!'"""
        tr = UniversalTranslator()
        result = tr.translate([CHAOS, COUNTER], source_species="dog")
        self.assertEqual(result.semantic_meaning, "Back off!")
        self.assertGreater(result.confidence, 0.0)

    def test_dog_play(self):
        """Dog HARMONY+PROGRESS = 'Let's play!'"""
        tr = UniversalTranslator()
        result = tr.translate([HARMONY, PROGRESS], source_species="dog")
        self.assertEqual(result.semantic_meaning, "Let's play!")

    def test_cat_purr(self):
        """Cat HARMONY+HARMONY = 'Trust, purring'"""
        tr = UniversalTranslator()
        result = tr.translate([HARMONY, HARMONY], source_species="cat")
        self.assertEqual(result.semantic_meaning, "Trust, purring")

    def test_cat_hiss(self):
        """Cat CHAOS+CHAOS = 'Hissing, angry'"""
        tr = UniversalTranslator()
        result = tr.translate([CHAOS, CHAOS], source_species="cat")
        self.assertEqual(result.semantic_meaning, "Hissing, angry")

    def test_empty_chain(self):
        """Empty chain = silence."""
        tr = UniversalTranslator()
        result = tr.translate([], source_species="dog")
        self.assertEqual(result.semantic_meaning, "(silence)")
        self.assertEqual(result.confidence, 0.0)

    def test_b_layer_filtering(self):
        """Invalid operators for species get filtered out."""
        tr = UniversalTranslator()
        # LATTICE is not in dog's valid operators
        result = tr.translate([LATTICE, LATTICE], source_species="dog")
        self.assertEqual(len(result.operator_chain), 0)

    def test_cross_species_compose(self):
        """Cross-species CL composition: same ops = high agreement."""
        tr = UniversalTranslator()
        # Both produce HARMONY -> CL[H][H] = H = 100% agreement
        coh = tr.cross_species_compose(
            [HARMONY, HARMONY, HARMONY], "dog",
            [HARMONY, HARMONY, HARMONY], "human")
        self.assertAlmostEqual(coh, 1.0)

    def test_cross_species_compose_mismatch(self):
        """Cross-species: mismatched ops = lower agreement."""
        tr = UniversalTranslator()
        coh = tr.cross_species_compose(
            [CHAOS, CHAOS, CHAOS], "dog",
            [VOID, VOID, VOID], "human")
        self.assertLess(coh, 1.0)

    def test_species_list(self):
        """Default species profiles exist."""
        tr = UniversalTranslator()
        species = tr.species_list
        self.assertIn("dog", species)
        self.assertIn("cat", species)
        self.assertIn("human", species)
        self.assertIn("ck", species)

    def test_self_calibration(self):
        """Translator self-calibrates over time."""
        tr = UniversalTranslator()
        # Feed many translations to build calibration
        for _ in range(50):
            tr.translate([CHAOS, COUNTER], source_species="dog")
        # Calibration should exist
        self.assertIn("dog", tr._calibration)

    def test_confidence_range(self):
        """Confidence always in [0, 1]."""
        tr = UniversalTranslator()
        result = tr.translate([HARMONY, PROGRESS, CHAOS], source_species="dog")
        self.assertGreaterEqual(result.confidence, 0.0)
        self.assertLessEqual(result.confidence, 1.0)

    def test_translation_result_fields(self):
        """TranslationResult has all expected fields."""
        tr = UniversalTranslator()
        result = tr.translate([HARMONY, HARMONY], source_species="dog")
        self.assertEqual(result.source_species, "dog")
        self.assertEqual(result.target_species, "human")
        self.assertIsInstance(result.operator_chain, list)
        self.assertIsInstance(result.chain_names, list)
        self.assertIsInstance(result.semantic_meaning, str)
        self.assertIsInstance(result.confidence, float)
        self.assertIsInstance(result.cross_coherence, float)


# ================================================================
#  PERFORMANCE TESTS
# ================================================================

class TestPerformance(unittest.TestCase):
    """Field operations must be fast enough for 50Hz."""

    def test_field_tick_under_1ms(self):
        """3-stream field tick < 1ms."""
        field = CoherenceField()
        streams = []
        for name in ["heartbeat", "audio", "text"]:
            s = OperatorStream(name)
            s.active = True
            field.register_stream(s)
            streams.append(s)

        # Pre-fill streams
        for s in streams:
            for _ in range(32):
                s.feed(HARMONY)

        # Time 100 ticks
        t0 = time.perf_counter()
        for i in range(100):
            field.tick(i)
        elapsed = time.perf_counter() - t0

        avg_ms = (elapsed / 100) * 1000
        self.assertLess(avg_ms, 1.0,
                        f"Field tick too slow: {avg_ms:.3f}ms (need < 1ms)")

    def test_soft_classify_fast(self):
        """soft_classify_d2 < 0.01ms."""
        vec = [0.3, -0.2, 0.5, 0.1, -0.4]
        t0 = time.perf_counter()
        for _ in range(1000):
            soft_classify_d2(vec)
        elapsed = time.perf_counter() - t0
        avg_us = (elapsed / 1000) * 1e6
        self.assertLess(avg_us, 100,
                        f"soft_classify too slow: {avg_us:.1f}us")


# ================================================================
#  INTEGRATION TEST
# ================================================================

class TestFieldIntegration(unittest.TestCase):
    """End-to-end: D2 pipeline -> streams -> field -> consensus."""

    def test_text_through_field(self):
        """Process text through D2 pipeline into field."""
        pipe = D2Pipeline()
        field = CoherenceField()
        text_stream = OperatorStream("text")
        text_stream.active = True
        field.register_stream(text_stream)

        ops = []
        for ch in "hello world":
            if ch.isalpha():
                idx = ord(ch) - ord('a')
                if pipe.feed_symbol(idx):
                    text_stream.feed(pipe.operator, pipe.d2_vector)
                    ops.append(pipe.operator)

        self.assertGreater(len(ops), 0)
        field.tick(0)
        # Self-coherence >= 0 (may be 0 if no HARMONY in text ops)
        self.assertGreaterEqual(text_stream.self_coherence, 0.0)
        self.assertGreater(text_stream.fill, 0)

    def test_multi_stream_field(self):
        """Multiple streams produce meaningful field coherence."""
        field = CoherenceField()
        hb = OperatorStream("heartbeat")
        audio = OperatorStream("audio")
        hb.active = True
        audio.active = True
        field.register_stream(hb)
        field.register_stream(audio)

        # Both produce same operators -> high field coherence
        for _ in range(20):
            hb.feed(HARMONY)
            audio.feed(HARMONY)

        field.tick(0)
        self.assertGreater(field.field_coherence, 0.5)
        self.assertEqual(field.consensus_operator, HARMONY)


# ================================================================
#  RUN
# ================================================================

def run_field_tests():
    """Run all field tests and return (passed, failed, total)."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromModule(__import__(__name__)))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    passed = result.testsRun - len(result.failures) - len(result.errors)
    failed = len(result.failures) + len(result.errors)
    return passed, failed, result.testsRun


if __name__ == '__main__':
    unittest.main()
