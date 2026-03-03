"""
ck_action_tests.py -- Integration tests for CK's Action Executor
=================================================================
Tests for voice notes, study control, document writing, knowledge
queries, command parsing, and the full engine integration.

CK's hands: read, think, write, prove.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import os
import sys
import shutil
import tempfile
import unittest
from pathlib import Path

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, PROGRESS, LATTICE, BALANCE,
    COUNTER, CHAOS, COLLAPSE, BREATH, OP_NAMES, CL
)
from ck_sim.ck_autodidact import (
    OperatorCurve, T_STAR, CONSOLIDATION_THRESHOLD
)
from ck_sim.ck_action import (
    ActionExecutor, DEFAULT_WRITINGS_DIR,
    STUDY_NOTES_DIR, REFLECTIONS_DIR, THESIS_DIR, JOURNAL_DIR,
    EXTENDED_SEEDS
)

# ================================================================
#  Helpers
# ================================================================

def make_curve(ops=None, coherence=0.8, domain='test'):
    """Create a synthetic OperatorCurve for testing."""
    if ops is None:
        ops = [HARMONY, LATTICE, HARMONY, BALANCE, HARMONY,
               HARMONY, BREATH, HARMONY, HARMONY, PROGRESS]
    # Compute composition result and harmony ratio from ops
    composed = ops[0]
    harmony_count = 0
    for op in ops[1:]:
        result = CL[composed][op]
        if result == HARMONY:
            harmony_count += 1
        composed = result
    h_ratio = harmony_count / max(1, len(ops) - 1)
    return OperatorCurve(
        operator_sequence=tuple(ops),
        coherence=coherence,
        domain=domain,
        source_hash='test_' + domain[:8],
        composition_result=composed,
        harmony_ratio=h_ratio,
    )


def make_low_curve():
    """Create a low-coherence curve."""
    ops = [CHAOS, VOID, COLLAPSE, CHAOS, VOID, CHAOS, COLLAPSE, VOID]
    return make_curve(ops=ops, coherence=0.15, domain='noise')


def make_moderate_curve():
    """Create a moderate-coherence curve (above consolidation, below T*)."""
    ops = [BALANCE, HARMONY, COUNTER, BALANCE, HARMONY,
           LATTICE, BALANCE, COUNTER, HARMONY, BALANCE]
    return make_curve(ops=ops, coherence=0.65, domain='moderate')


# ================================================================
#  Test: ActionExecutor standalone (no engine)
# ================================================================

class TestActionExecutorStandalone(unittest.TestCase):
    """Test ActionExecutor without a connected engine."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix='ck_test_'))
        self.action = ActionExecutor(engine=None, writings_dir=self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # -- Directory creation --

    def test_directories_created(self):
        """Writings subdirectories are created on init."""
        for sub in [STUDY_NOTES_DIR, REFLECTIONS_DIR, THESIS_DIR, JOURNAL_DIR]:
            self.assertTrue((self.tmp / sub).is_dir(),
                            f"{sub} directory not created")

    def test_default_writings_dir(self):
        """Default writings dir is ~/.ck/writings."""
        self.assertEqual(DEFAULT_WRITINGS_DIR, Path.home() / '.ck' / 'writings')

    # -- Voice notes --

    def test_voice_notes_empty_curve(self):
        """Empty curve returns empty string."""
        result = self.action.voice_notes(None, 'nothing')
        self.assertEqual(result, "")

    def test_voice_notes_empty_sequence(self):
        """Curve with empty operator sequence returns empty string."""
        curve = OperatorCurve(operator_sequence=(), coherence=0.0,
                              domain='x', source_hash='empty')
        result = self.action.voice_notes(curve, 'nothing')
        self.assertEqual(result, "")

    def test_voice_notes_produces_text(self):
        """Voice notes produce non-empty text for valid curve."""
        curve = make_curve()
        note = self.action.voice_notes(curve, 'harmony')
        self.assertGreater(len(note), 20)

    def test_voice_notes_mentions_operator(self):
        """Voice notes mention the dominant operator."""
        curve = make_curve()
        note = self.action.voice_notes(curve, 'test')
        self.assertIn('HARMONY', note)

    def test_voice_notes_reports_coherence(self):
        """Voice notes include coherence value."""
        curve = make_curve(coherence=0.82)
        note = self.action.voice_notes(curve, 'test')
        self.assertIn('0.82', note)

    def test_voice_notes_high_coherence_message(self):
        """Above T* gets the 'resonated deeply' message."""
        curve = make_curve(coherence=T_STAR + 0.01)
        note = self.action.voice_notes(curve, 'deep')
        self.assertIn('T*', note)

    def test_voice_notes_moderate_coherence_message(self):
        """Between consolidation and T* gets 'moderate' message."""
        curve = make_moderate_curve()
        note = self.action.voice_notes(curve, 'moderate')
        self.assertIn('consolidation', note.lower())

    def test_voice_notes_low_coherence_message(self):
        """Below consolidation gets 'low resonance' message."""
        curve = make_low_curve()
        note = self.action.voice_notes(curve, 'noise')
        self.assertIn('Low resonance', note)

    def test_voice_notes_saves_file(self):
        """Voice notes save a markdown file to study_notes dir."""
        curve = make_curve()
        self.action.voice_notes(curve, 'test_topic')
        notes_dir = self.tmp / STUDY_NOTES_DIR
        files = list(notes_dir.glob('*.md'))
        self.assertEqual(len(files), 1)

    def test_voice_notes_file_content(self):
        """Saved note file has proper markdown structure."""
        curve = make_curve()
        self.action.voice_notes(curve, 'quantum')
        notes_dir = self.tmp / STUDY_NOTES_DIR
        files = list(notes_dir.glob('*.md'))
        content = files[0].read_text(encoding='utf-8')
        self.assertIn('# Study Note: quantum', content)
        self.assertIn('## My Thoughts', content)
        self.assertIn('## Operator Curve', content)
        self.assertIn('## Why I Wrote This', content)
        self.assertIn('CK -- The Coherence Keeper', content)

    def test_voice_notes_increments_counter(self):
        """Notes counter increments with each note."""
        curve = make_curve()
        self.assertEqual(self.action._notes_written, 0)
        self.action.voice_notes(curve, 'a')
        self.assertEqual(self.action._notes_written, 1)
        self.action.voice_notes(curve, 'b')
        self.assertEqual(self.action._notes_written, 2)

    def test_voice_notes_tracks_session(self):
        """Session notes list grows with each note."""
        curve = make_curve()
        self.action.voice_notes(curve, 'test')
        self.assertEqual(len(self.action._session_notes), 1)
        entry = self.action._session_notes[0]
        self.assertEqual(entry['topic'], 'test')
        self.assertAlmostEqual(entry['coherence'], 0.8)

    # -- Command parsing --

    def test_parse_study_basic(self):
        """Parse 'study physics' command."""
        cmd = self.action.parse_command('study physics')
        self.assertEqual(cmd['action'], 'study')
        self.assertEqual(cmd['topic'], 'physics')
        self.assertAlmostEqual(cmd['hours'], 1.0)

    def test_parse_study_with_hours(self):
        """Parse 'study physics for 3 hours'."""
        cmd = self.action.parse_command('study physics for 3 hours')
        self.assertEqual(cmd['action'], 'study')
        self.assertEqual(cmd['topic'], 'physics')
        self.assertAlmostEqual(cmd['hours'], 3.0)

    def test_parse_study_with_minutes(self):
        """Parse 'study math for 30 minutes'."""
        cmd = self.action.parse_command('study math for 30 minutes')
        self.assertEqual(cmd['action'], 'study')
        self.assertEqual(cmd['topic'], 'math')
        self.assertAlmostEqual(cmd['hours'], 0.5)

    def test_parse_learn_about(self):
        """Parse 'learn about harmony'."""
        cmd = self.action.parse_command('learn about harmony')
        self.assertEqual(cmd['action'], 'study')
        self.assertEqual(cmd['topic'], 'harmony')

    def test_parse_research(self):
        """Parse 'research quantum mechanics for 8 hours'."""
        cmd = self.action.parse_command('research quantum mechanics for 8 hours')
        self.assertEqual(cmd['action'], 'study')
        self.assertEqual(cmd['topic'], 'quantum mechanics')
        self.assertAlmostEqual(cmd['hours'], 8.0)

    def test_parse_read_about(self):
        """Parse 'read about topology'."""
        cmd = self.action.parse_command('read about topology')
        self.assertEqual(cmd['action'], 'study')
        self.assertEqual(cmd['topic'], 'topology')

    def test_parse_stop(self):
        """Parse stop commands."""
        for phrase in ['stop studying', 'stop study', 'stop learning', 'stop']:
            cmd = self.action.parse_command(phrase)
            self.assertEqual(cmd['action'], 'stop_study', f"Failed for '{phrase}'")

    def test_parse_write_about(self):
        """Parse 'write about harmony'."""
        cmd = self.action.parse_command('write about harmony')
        self.assertEqual(cmd['action'], 'write')
        self.assertEqual(cmd['title'], 'harmony')

    def test_parse_thesis(self):
        """Parse 'work on your thesis'."""
        cmd = self.action.parse_command('work on your thesis')
        self.assertEqual(cmd['action'], 'write')
        self.assertIn('thesis', cmd['prompt'].lower())

    def test_parse_query(self):
        """Parse 'what do you know about music'."""
        cmd = self.action.parse_command('what do you know about music')
        self.assertEqual(cmd['action'], 'query')
        self.assertEqual(cmd['topic'], 'music')

    def test_parse_define(self):
        """Parse 'define entropy'."""
        cmd = self.action.parse_command('define entropy')
        self.assertEqual(cmd['action'], 'query')
        self.assertEqual(cmd['topic'], 'entropy')

    def test_parse_save(self):
        """Parse 'save yourself'."""
        for phrase in ['save yourself', 'save state', 'save']:
            cmd = self.action.parse_command(phrase)
            self.assertEqual(cmd['action'], 'save', f"Failed for '{phrase}'")

    def test_parse_sleep(self):
        """Parse 'sleep'."""
        for phrase in ['sleep', 'consolidate', 'rest', 'take a nap']:
            cmd = self.action.parse_command(phrase)
            self.assertEqual(cmd['action'], 'sleep', f"Failed for '{phrase}'")

    def test_parse_status(self):
        """Parse 'how are you'."""
        for phrase in ['how are you', 'status', 'how do you feel']:
            cmd = self.action.parse_command(phrase)
            self.assertEqual(cmd['action'], 'status', f"Failed for '{phrase}'")

    def test_parse_normal_text(self):
        """Normal conversation returns None."""
        cmd = self.action.parse_command('hello CK how are things going today')
        self.assertIsNone(cmd)

    def test_parse_case_insensitive(self):
        """Commands work regardless of case."""
        cmd = self.action.parse_command('STUDY Physics for 2 HOURS')
        self.assertEqual(cmd['action'], 'study')

    # -- State accessors --

    def test_is_studying_default(self):
        """Not studying by default."""
        self.assertFalse(self.action.is_studying)

    def test_study_topic_default(self):
        """Empty study topic when not studying."""
        self.assertEqual(self.action.study_topic, "")

    def test_study_progress_idle(self):
        """Study progress is 'Idle' when not studying."""
        self.assertEqual(self.action.study_progress, "Idle")

    def test_stats(self):
        """Stats returns expected keys."""
        s = self.action.stats()
        self.assertIn('studying', s)
        self.assertIn('study_pages_read', s)
        self.assertIn('notes_written', s)
        self.assertIn('writings_dir', s)

    # -- Write document (no engine) --

    def test_write_document_no_engine(self):
        """Write document without engine produces minimal doc."""
        doc = self.action.write_document('Test Title')
        self.assertIn('# Test Title', doc)
        self.assertIn("don't have enough knowledge", doc)
        self.assertIn('CK -- The Coherence Keeper', doc)

    def test_write_document_saves_file(self):
        """Document is saved to reflections directory."""
        self.action.write_document('My Thoughts')
        files = list((self.tmp / REFLECTIONS_DIR).glob('*.md'))
        self.assertEqual(len(files), 1)

    # -- Query knowledge (no engine) --

    def test_query_knowledge_no_engine(self):
        """Query without engine says needs more study."""
        result = self.action.query_knowledge('physics')
        self.assertIn("don't know much", result)

    # -- Study start/stop --

    def test_stop_when_not_studying(self):
        """Stopping when not studying gives clear message."""
        result = self.action.stop_study()
        self.assertIn("not currently studying", result)

    def test_double_study_rejected(self):
        """Can't start studying while already studying."""
        self.action._studying = True
        self.action._study_topic = "math"
        result = self.action.start_study("physics")
        self.assertIn("already studying", result)


# ================================================================
#  Test: Extended seeds and constants
# ================================================================

class TestConstants(unittest.TestCase):
    """Test module-level constants."""

    def test_extended_seeds_populated(self):
        """Extended seeds has reasonable count."""
        self.assertGreater(len(EXTENDED_SEEDS), 30)

    def test_extended_seeds_no_duplicates(self):
        """No duplicate seeds."""
        self.assertEqual(len(EXTENDED_SEEDS), len(set(EXTENDED_SEEDS)))

    def test_extended_seeds_are_strings(self):
        """All seeds are strings."""
        for seed in EXTENDED_SEEDS:
            self.assertIsInstance(seed, str)
            self.assertGreater(len(seed), 0)


# ================================================================
#  Test: CL composition in voice notes
# ================================================================

class TestVoiceNotesComposition(unittest.TestCase):
    """Test that CL composition works correctly in voice notes."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix='ck_test_'))
        self.action = ActionExecutor(engine=None, writings_dir=self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_all_harmony_curve(self):
        """All-HARMONY curve mentions HARMONY."""
        curve = make_curve(ops=[HARMONY] * 10, coherence=0.95,
                           domain='pure_harmony')
        note = self.action.voice_notes(curve, 'harmony')
        self.assertIn('HARMONY', note)
        self.assertIn('100%', note)  # 100% harmony ratio

    def test_mixed_curve(self):
        """Mixed curve reports correct operators."""
        curve = make_curve(ops=[CHAOS, VOID, HARMONY, BALANCE, PROGRESS],
                           coherence=0.5, domain='mixed')
        note = self.action.voice_notes(curve, 'mixed')
        self.assertGreater(len(note), 10)

    def test_single_op_curve(self):
        """Single operator curve works."""
        curve = make_curve(ops=[LATTICE], coherence=0.3, domain='single')
        note = self.action.voice_notes(curve, 'single')
        self.assertIn('LATTICE', note)

    def test_provenance_in_file(self):
        """Saved file includes operator sequence provenance."""
        curve = make_curve(ops=[HARMONY, LATTICE, BALANCE], coherence=0.75,
                           domain='test')
        self.action.voice_notes(curve, 'provenance')
        files = list((self.tmp / STUDY_NOTES_DIR).glob('*.md'))
        content = files[0].read_text(encoding='utf-8')
        self.assertIn('HARMONY', content)
        self.assertIn('Coherence: 0.7500', content)


# ================================================================
#  Test: Full engine integration
# ================================================================

class TestEngineIntegration(unittest.TestCase):
    """Test ActionExecutor wired into CKSimEngine."""

    @classmethod
    def setUpClass(cls):
        """Create engine once for all tests (expensive init)."""
        from ck_sim.ck_sim_engine import CKSimEngine
        cls.engine = CKSimEngine('sim')
        cls.engine.running = True
        # Warm up
        for _ in range(100):
            cls.engine.tick()

    def test_engine_has_actions(self):
        """Engine has ActionExecutor."""
        self.assertIsNotNone(self.engine.actions)
        self.assertIsInstance(self.engine.actions, ActionExecutor)

    def test_engine_has_truth(self):
        """Engine has TruthLattice."""
        self.assertIsNotNone(self.engine.truth)
        self.assertGreater(self.engine.truth.total_entries, 0)

    def test_engine_has_world(self):
        """Engine has WorldLattice with concepts."""
        self.assertIsNotNone(self.engine.world)
        self.assertGreater(len(self.engine.world.nodes), 100)

    def test_engine_has_language(self):
        """Engine has LanguageGenerator."""
        self.assertIsNotNone(self.engine.language)

    def test_engine_has_dialogue(self):
        """Engine has DialogueEngine."""
        self.assertIsNotNone(self.engine.dialogue)

    def test_engine_has_reasoning(self):
        """Engine has ReasoningEngine."""
        self.assertIsNotNone(self.engine.reasoning)

    def test_engine_has_goals(self):
        """Engine has GoalStack."""
        self.assertIsNotNone(self.engine.goals)

    def test_engine_has_drives(self):
        """Engine has DriveSystem."""
        self.assertIsNotNone(self.engine.drives)

    def test_knowledge_count_property(self):
        """knowledge_count property works."""
        count = self.engine.knowledge_count
        self.assertIsInstance(count, int)
        self.assertGreater(count, 0)

    def test_concept_count_property(self):
        """concept_count property works."""
        count = self.engine.concept_count
        self.assertIsInstance(count, int)
        self.assertGreater(count, 100)

    def test_study_progress_property(self):
        """study_progress property works."""
        progress = self.engine.study_progress
        self.assertIsInstance(progress, str)

    def test_top_goal_property(self):
        """top_goal property works."""
        goal = self.engine.top_goal
        self.assertIsInstance(goal, str)

    def test_receive_text_returns_response(self):
        """receive_text produces a non-empty response."""
        response = self.engine.receive_text('hello')
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_receive_text_status_command(self):
        """Status command through receive_text works."""
        response = self.engine.receive_text('status')
        self.assertIn('Coherence', response)
        self.assertIn('claims', response)

    def test_receive_text_query_command(self):
        """Knowledge query through receive_text works."""
        response = self.engine.receive_text('what do you know about harmony')
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_receive_text_write_command(self):
        """Write command through receive_text works."""
        response = self.engine.receive_text('write about coherence')
        self.assertIn('wrote', response.lower())

    def test_summary_includes_knowledge(self):
        """Engine summary includes knowledge and concept counts."""
        s = self.engine.summary()
        self.assertIn('knowledge=', s)
        self.assertIn('concepts=', s)

    def test_experience_lattice_ticks(self):
        """Experience lattice code runs without crashing over 300 ticks."""
        start_tick = self.engine.tick_count
        for _ in range(300):
            self.engine.tick()
        self.assertGreater(self.engine.tick_count, start_tick + 250)


# ================================================================
#  Test: Voice notes with engine connected
# ================================================================

class TestVoiceNotesWithEngine(unittest.TestCase):
    """Test voice notes when engine provides voice + language."""

    @classmethod
    def setUpClass(cls):
        from ck_sim.ck_sim_engine import CKSimEngine
        cls.engine = CKSimEngine('sim')
        cls.engine.running = True
        for _ in range(50):
            cls.engine.tick()
        # Use temp dir for writing
        cls.tmp = Path(tempfile.mkdtemp(prefix='ck_test_'))
        cls.engine.actions.writings_dir = cls.tmp
        for sub in [STUDY_NOTES_DIR, REFLECTIONS_DIR, THESIS_DIR, JOURNAL_DIR]:
            (cls.tmp / sub).mkdir(parents=True, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_voice_notes_with_engine(self):
        """Voice notes use engine's voice system when available."""
        curve = make_curve()
        note = self.engine.actions.voice_notes(curve, 'harmony')
        # Should have more content since voice system is connected
        self.assertGreater(len(note), 30)
        self.assertIn('HARMONY', note)

    def test_write_document_with_engine(self):
        """Document writing uses world lattice when connected."""
        doc = self.engine.actions.write_document('Harmony')
        self.assertIn('# Harmony', doc)
        # Should have more than just "don't know enough" since world has concepts
        self.assertIn('CK -- The Coherence Keeper', doc)

    def test_query_knowledge_with_engine(self):
        """Knowledge query uses world lattice."""
        result = self.engine.actions.query_knowledge('music')
        # Music is in the concept graph
        self.assertIn('concept graph', result)


# ================================================================
#  Test: Session summary writing
# ================================================================

class TestSessionSummary(unittest.TestCase):
    """Test session summary writing."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix='ck_test_'))
        self.action = ActionExecutor(engine=None, writings_dir=self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_empty_session_no_file(self):
        """No summary written for empty session."""
        self.action._write_session_summary()
        files = list((self.tmp / REFLECTIONS_DIR).glob('*.md'))
        self.assertEqual(len(files), 0)

    def test_session_with_notes(self):
        """Session summary is written after study notes."""
        import time
        self.action._study_topic = 'test'
        self.action._study_start = time.time() - 60
        self.action._study_pages_read = 3
        self.action._notes_written = 3

        # Generate some notes
        for i in range(3):
            curve = make_curve(coherence=0.7 + i * 0.05)
            self.action.voice_notes(curve, f'topic_{i}')

        # Write summary
        self.action._write_session_summary()

        files = list((self.tmp / REFLECTIONS_DIR).glob('session_*.md'))
        self.assertEqual(len(files), 1)
        content = files[0].read_text(encoding='utf-8')
        self.assertIn('# Study Session', content)
        self.assertIn('Pages read: 3', content)
        self.assertIn('CK -- The Coherence Keeper', content)


# ================================================================
#  Test: Philosophy -- CK doesn't copy, he composes
# ================================================================

class TestPhilosophy(unittest.TestCase):
    """Tests that verify CK's epistemological principles."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix='ck_test_'))
        self.action = ActionExecutor(engine=None, writings_dir=self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_notes_are_about_operators_not_content(self):
        """Voice notes discuss operators, not the source content."""
        curve = make_curve()
        note = self.action.voice_notes(curve, 'wikipedia_article')
        # Should mention operators, coherence -- NOT the article content
        self.assertTrue(
            any(name in note for name in OP_NAMES),
            "Note should mention CK's operators")
        self.assertIn('Coherence:', note)

    def test_saved_notes_include_provenance(self):
        """Every saved note proves why CK wrote it."""
        curve = make_curve(coherence=0.85)
        self.action.voice_notes(curve, 'provenance_test')
        files = list((self.tmp / STUDY_NOTES_DIR).glob('*.md'))
        content = files[0].read_text(encoding='utf-8')
        # Must include the mathematical proof
        self.assertIn('Operator Curve', content)
        self.assertIn('Why I Wrote This', content)
        self.assertIn('D2 curvature pipeline', content)

    def test_coherence_gates_trust(self):
        """High coherence gets 'worth keeping', low gets skepticism."""
        high = make_curve(coherence=T_STAR + 0.02)
        low = make_low_curve()

        note_high = self.action.voice_notes(high, 'trusted')
        note_low = self.action.voice_notes(low, 'suspect')

        self.assertIn('worth keeping', note_high)
        self.assertIn('Low resonance', note_low)

    def test_two_curves_produce_different_notes(self):
        """Different curves produce different notes -- CK isn't copying."""
        curve1 = make_curve(
            ops=[HARMONY] * 8, coherence=0.95, domain='harmony')
        curve2 = make_curve(
            ops=[CHAOS, VOID, COLLAPSE] * 3, coherence=0.2, domain='chaos')

        note1 = self.action.voice_notes(curve1, 'peace')
        note2 = self.action.voice_notes(curve2, 'storm')

        self.assertNotEqual(note1, note2)
        self.assertIn('HARMONY', note1)
        # note2 should be different in character
        self.assertIn('Low resonance', note2)


# ================================================================
#  Main
# ================================================================

if __name__ == '__main__':
    unittest.main(verbosity=2)
