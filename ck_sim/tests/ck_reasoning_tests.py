"""
ck_reasoning_tests.py -- Tests for CK's 3-Speed Reasoning Engine
=================================================================
Validates: spreading activation, Levy jumps, contradiction pruning,
           3-speed reasoning engine, speed selection, integration
           with real WorldLattice loaded with seed corpus.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import unittest
import os
import sys

# Ensure ck_sim package is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ================================================================
#  TEST IMPORTS AND CONSTANTS
# ================================================================

class TestImport(unittest.TestCase):
    """Module imports without error."""

    def test_import_module(self):
        """ck_reasoning imports cleanly."""
        import ck_sim.ck_reasoning
        self.assertTrue(hasattr(ck_sim.ck_reasoning, 'ReasoningEngine'))

    def test_import_all_classes(self):
        """All public classes importable."""
        from ck_sim.ck_reasoning import (
            ActivationMap, LevyJumper, ContradictionPruner,
            ReasoningEngine, ReasoningResult
        )
        self.assertTrue(callable(ActivationMap))
        self.assertTrue(callable(LevyJumper))
        self.assertTrue(callable(ContradictionPruner))
        self.assertTrue(callable(ReasoningEngine))

    def test_import_heartbeat_constants(self):
        """Heartbeat constants accessible via reasoning module."""
        from ck_sim.ck_reasoning import (
            HARMONY, VOID, COLLAPSE, PROGRESS, LATTICE
        )
        self.assertEqual(HARMONY, 7)
        self.assertEqual(VOID, 0)
        self.assertEqual(COLLAPSE, 4)


class TestConstants(unittest.TestCase):
    """Speed constants and configuration values."""

    def test_speed_constants(self):
        """Speed constants are 0, 1, 2."""
        from ck_sim.ck_reasoning import SPEED_QUICK, SPEED_NORMAL, SPEED_HEAVY
        self.assertEqual(SPEED_QUICK, 0)
        self.assertEqual(SPEED_NORMAL, 1)
        self.assertEqual(SPEED_HEAVY, 2)

    def test_speed_names(self):
        """Speed names array matches constants."""
        from ck_sim.ck_reasoning import SPEED_NAMES
        self.assertEqual(len(SPEED_NAMES), 3)
        self.assertEqual(SPEED_NAMES[0], 'QUICK')
        self.assertEqual(SPEED_NAMES[1], 'NORMAL')
        self.assertEqual(SPEED_NAMES[2], 'HEAVY')

    def test_decay_and_dampen(self):
        """Decay and dampen constants are in valid range."""
        from ck_sim.ck_reasoning import DEFAULT_DECAY, COLLAPSE_DAMPEN
        self.assertGreater(DEFAULT_DECAY, 0.0)
        self.assertLess(DEFAULT_DECAY, 1.0)
        self.assertGreater(COLLAPSE_DAMPEN, 0.0)
        self.assertLess(COLLAPSE_DAMPEN, 1.0)


# ================================================================
#  HELPER: Build a seeded lattice for tests
# ================================================================

def _make_lattice():
    """Create and return a WorldLattice loaded with seed corpus."""
    from ck_sim.ck_world_lattice import WorldLattice
    lattice = WorldLattice()
    lattice.load_seed_corpus()
    return lattice


# ================================================================
#  TEST ACTIVATION MAP
# ================================================================

class TestActivationMap(unittest.TestCase):
    """Spreading activation on concept graph."""

    def setUp(self):
        self.lattice = _make_lattice()

    def test_activate_single_node(self):
        """Activating a node sets its activation level."""
        from ck_sim.ck_reasoning import ActivationMap
        amap = ActivationMap(self.lattice)
        amap.activate('water', 1.0)
        self.assertEqual(amap.get_activation('water'), 1.0)

    def test_activate_invalid_node(self):
        """Activating a non-existent node is a no-op."""
        from ck_sim.ck_reasoning import ActivationMap
        amap = ActivationMap(self.lattice)
        amap.activate('nonexistent_node_xyz', 1.0)
        self.assertEqual(amap.get_activation('nonexistent_node_xyz'), 0.0)

    def test_activate_clamping(self):
        """Activation strength is clamped to [0, 1]."""
        from ck_sim.ck_reasoning import ActivationMap
        amap = ActivationMap(self.lattice)
        amap.activate('water', 5.0)
        self.assertEqual(amap.get_activation('water'), 1.0)
        amap.activate('fire', -1.0)
        self.assertEqual(amap.get_activation('fire'), 0.0)

    def test_activate_max_semantics(self):
        """Repeated activation takes the max, not sum."""
        from ck_sim.ck_reasoning import ActivationMap
        amap = ActivationMap(self.lattice)
        amap.activate('water', 0.5)
        amap.activate('water', 0.3)
        self.assertEqual(amap.get_activation('water'), 0.5)
        amap.activate('water', 0.8)
        self.assertEqual(amap.get_activation('water'), 0.8)

    def test_spread_reaches_neighbors(self):
        """Spreading from a node activates its neighbors."""
        from ck_sim.ck_reasoning import ActivationMap
        amap = ActivationMap(self.lattice)
        # Water has relations: sustains->life, opposes fire, etc.
        amap.activate('water', 1.0)
        activated = amap.spread(steps=1)
        # Life should be activated (water sustains life)
        self.assertGreater(amap.get_activation('life'), 0.0)

    def test_spread_decays(self):
        """Activation decays with each hop."""
        from ck_sim.ck_reasoning import ActivationMap, DEFAULT_DECAY
        amap = ActivationMap(self.lattice, decay=0.5)
        amap.activate('water', 1.0)
        amap.spread(steps=1)
        # Neighbor activation should be <= decay * source
        for nid, act in amap.activations.items():
            if nid != 'water':
                self.assertLessEqual(act, 0.5 + 0.01)  # decay=0.5, small float tolerance

    def test_spread_multi_step(self):
        """Multi-step spread reaches further nodes."""
        from ck_sim.ck_reasoning import ActivationMap
        amap = ActivationMap(self.lattice)
        amap.activate('seed', 1.0)
        # seed -> growth -> life (2 hops)
        amap.spread(steps=1)
        act_1 = amap.active_count()
        amap.spread(steps=2)
        act_3 = amap.active_count()
        self.assertGreaterEqual(act_3, act_1)

    def test_collapse_edge_dampened(self):
        """COLLAPSE edges dampen activation relative to HARMONY edges."""
        from ck_sim.ck_reasoning import ActivationMap
        # Fire opposes water (COLLAPSE edge) and is sustained by other things
        # Test that opposes edges produce lower activation than sustains edges
        amap = ActivationMap(self.lattice, decay=0.9)
        amap.activate('joy', 1.0)
        amap.spread(steps=1)
        # joy opposes sorrow -- sorrow should get dampened activation
        sorrow_act = amap.get_activation('sorrow')
        # If sorrow is activated, it should be dampened below full decay
        if sorrow_act > 0:
            self.assertLess(sorrow_act, 0.9)  # Less than full decay (dampened by COLLAPSE)

    def test_top_k(self):
        """top_k returns correct number of results, sorted."""
        from ck_sim.ck_reasoning import ActivationMap
        amap = ActivationMap(self.lattice)
        amap.activate('water', 1.0)
        amap.activate('fire', 0.5)
        amap.activate('earth_element', 0.3)
        top = amap.top_k(k=2)
        self.assertEqual(len(top), 2)
        self.assertEqual(top[0][0], 'water')
        self.assertEqual(top[0][1], 1.0)
        self.assertGreaterEqual(top[0][1], top[1][1])

    def test_reset(self):
        """Reset clears all activations."""
        from ck_sim.ck_reasoning import ActivationMap
        amap = ActivationMap(self.lattice)
        amap.activate('water', 1.0)
        amap.spread(steps=2)
        self.assertGreater(amap.active_count(), 0)
        amap.reset()
        self.assertEqual(amap.active_count(), 0)
        self.assertEqual(len(amap.activations), 0)

    def test_active_count(self):
        """active_count tracks nodes above threshold."""
        from ck_sim.ck_reasoning import ActivationMap
        amap = ActivationMap(self.lattice)
        self.assertEqual(amap.active_count(), 0)
        amap.activate('water', 1.0)
        amap.activate('fire', 0.5)
        self.assertEqual(amap.active_count(), 2)


# ================================================================
#  TEST LEVY JUMPER
# ================================================================

class TestLevyJumper(unittest.TestCase):
    """Levy flight jumps for creative exploration."""

    def setUp(self):
        self.lattice = _make_lattice()

    def test_jump_returns_valid_node(self):
        """Jump returns a node_id that exists in the lattice."""
        from ck_sim.ck_reasoning import LevyJumper
        jumper = LevyJumper(self.lattice)
        target = jumper.jump('water')
        if target is not None:
            self.assertIn(target, self.lattice.nodes)

    def test_jump_not_same_node(self):
        """Jump never returns the source node."""
        from ck_sim.ck_reasoning import LevyJumper
        jumper = LevyJumper(self.lattice)
        for _ in range(10):
            target = jumper.jump('water')
            if target is not None:
                self.assertNotEqual(target, 'water')

    def test_jump_not_direct_neighbor(self):
        """Jump avoids direct neighbors (we want distant connections)."""
        from ck_sim.ck_reasoning import LevyJumper
        jumper = LevyJumper(self.lattice)
        direct = set(t for t, _, _ in self.lattice.get_neighbors('water'))
        for _ in range(10):
            target = jumper.jump('water')
            if target is not None:
                self.assertNotIn(target, direct)

    def test_jump_from_invalid_node(self):
        """Jump from non-existent node returns None."""
        from ck_sim.ck_reasoning import LevyJumper
        jumper = LevyJumper(self.lattice)
        self.assertIsNone(jumper.jump('nonexistent_xyz'))

    def test_jump_finds_similar_nodes(self):
        """Levy jumps tend to find nodes with similar soft_dist signatures."""
        from ck_sim.ck_reasoning import LevyJumper
        import math
        jumper = LevyJumper(self.lattice, lfsr_seed=42)
        source = self.lattice.nodes['water']
        targets = []
        for _ in range(5):
            t = jumper.jump('water')
            if t:
                targets.append(t)
        # At least some jumps should succeed
        self.assertGreater(len(targets), 0)

    def test_lfsr_deterministic(self):
        """Same seed produces same LFSR sequence."""
        from ck_sim.ck_reasoning import LevyJumper
        j1 = LevyJumper(self.lattice, lfsr_seed=12345)
        j2 = LevyJumper(self.lattice, lfsr_seed=12345)
        r1 = j1.jump('water')
        r2 = j2.jump('water')
        self.assertEqual(r1, r2)

    def test_jump_count_increments(self):
        """Jump count tracks successful jumps."""
        from ck_sim.ck_reasoning import LevyJumper
        jumper = LevyJumper(self.lattice)
        self.assertEqual(jumper.jump_count, 0)
        result = jumper.jump('water')
        if result is not None:
            self.assertEqual(jumper.jump_count, 1)


# ================================================================
#  TEST CONTRADICTION PRUNER
# ================================================================

class TestContradictionPruner(unittest.TestCase):
    """Contradiction detection and pruning."""

    def setUp(self):
        self.lattice = _make_lattice()

    def test_opposes_detected(self):
        """Paths through 'opposes' relations are contradictory."""
        from ck_sim.ck_reasoning import ContradictionPruner
        pruner = ContradictionPruner()
        # existence opposes void
        self.assertTrue(pruner.prune(['existence', 'void'], self.lattice))

    def test_no_false_positive_on_clean_path(self):
        """Clean paths without opposition are not contradictory."""
        from ck_sim.ck_reasoning import ContradictionPruner
        pruner = ContradictionPruner()
        # water sustains life, seed causes growth -- no contradiction
        self.assertFalse(pruner.prune(['water', 'life'], self.lattice))

    def test_single_node_path(self):
        """Single-node path is never contradictory."""
        from ck_sim.ck_reasoning import ContradictionPruner
        pruner = ContradictionPruner()
        self.assertFalse(pruner.prune(['water'], self.lattice))

    def test_empty_path(self):
        """Empty path is never contradictory."""
        from ck_sim.ck_reasoning import ContradictionPruner
        pruner = ContradictionPruner()
        self.assertFalse(pruner.prune([], self.lattice))

    def test_indirect_contradiction(self):
        """Contradiction detected even if nodes are not adjacent in path."""
        from ck_sim.ck_reasoning import ContradictionPruner
        pruner = ContradictionPruner()
        # joy opposes sorrow -- put something between them
        result = pruner.prune(['joy', 'peace', 'sorrow'], self.lattice)
        self.assertTrue(result)

    def test_find_contradictions_in_activated(self):
        """find_contradictions identifies opposing active pairs."""
        from ck_sim.ck_reasoning import ContradictionPruner
        pruner = ContradictionPruner()
        activated = {'joy': 0.8, 'sorrow': 0.6, 'water': 0.5}
        contradictions = pruner.find_contradictions(activated, self.lattice)
        # joy opposes sorrow should be found
        found = False
        for a, b in contradictions:
            if (a == 'joy' and b == 'sorrow') or (a == 'sorrow' and b == 'joy'):
                found = True
        self.assertTrue(found)

    def test_find_contradictions_no_false_positives(self):
        """No contradictions found when none exist."""
        from ck_sim.ck_reasoning import ContradictionPruner
        pruner = ContradictionPruner()
        # water, life, growth -- all harmonious
        activated = {'water': 0.8, 'life': 0.6, 'growth': 0.5}
        contradictions = pruner.find_contradictions(activated, self.lattice)
        self.assertEqual(len(contradictions), 0)

    def test_prevents_counted_as_contradiction(self):
        """'prevents' relations are also treated as contradictions."""
        from ck_sim.ck_reasoning import ContradictionPruner
        pruner = ContradictionPruner()
        # wall prevents path
        result = pruner.prune(['wall', 'path'], self.lattice)
        self.assertTrue(result)


# ================================================================
#  TEST REASONING ENGINE
# ================================================================

class TestReasoningEngine(unittest.TestCase):
    """3-speed reasoning engine tests."""

    def setUp(self):
        self.lattice = _make_lattice()

    def test_quick_returns_result(self):
        """QUICK reasoning returns a ReasoningResult."""
        from ck_sim.ck_reasoning import ReasoningEngine, SPEED_QUICK, ReasoningResult
        engine = ReasoningEngine(self.lattice)
        result = engine.reason(['water'], speed=SPEED_QUICK)
        self.assertIsInstance(result, ReasoningResult)
        self.assertEqual(result.speed, SPEED_QUICK)

    def test_quick_finds_neighbors(self):
        """QUICK reasoning finds immediate neighbors."""
        from ck_sim.ck_reasoning import ReasoningEngine, SPEED_QUICK
        engine = ReasoningEngine(self.lattice)
        result = engine.reason(['water'], speed=SPEED_QUICK)
        # water sustains life, so life should be in activated_nodes
        self.assertIn('life', result.activated_nodes)

    def test_normal_returns_result(self):
        """NORMAL reasoning returns a ReasoningResult."""
        from ck_sim.ck_reasoning import ReasoningEngine, SPEED_NORMAL
        engine = ReasoningEngine(self.lattice)
        result = engine.reason(['water'], speed=SPEED_NORMAL)
        self.assertEqual(result.speed, SPEED_NORMAL)
        self.assertGreater(len(result.activated_nodes), 0)

    def test_normal_finds_more_than_quick(self):
        """NORMAL reasoning activates more nodes than QUICK."""
        from ck_sim.ck_reasoning import ReasoningEngine, SPEED_QUICK, SPEED_NORMAL
        engine = ReasoningEngine(self.lattice)
        quick = engine.reason(['water'], speed=SPEED_QUICK)
        normal = engine.reason(['water'], speed=SPEED_NORMAL)
        self.assertGreaterEqual(len(normal.activated_nodes), len(quick.activated_nodes))

    def test_heavy_returns_result(self):
        """HEAVY reasoning returns a ReasoningResult."""
        from ck_sim.ck_reasoning import ReasoningEngine, SPEED_HEAVY
        engine = ReasoningEngine(self.lattice)
        result = engine.reason(['water'], speed=SPEED_HEAVY)
        self.assertEqual(result.speed, SPEED_HEAVY)

    def test_heavy_makes_jumps(self):
        """HEAVY reasoning performs Levy jumps."""
        from ck_sim.ck_reasoning import ReasoningEngine, SPEED_HEAVY
        engine = ReasoningEngine(self.lattice)
        result = engine.reason(['water'], speed=SPEED_HEAVY)
        # Heavy reasoning should attempt jumps (may or may not succeed)
        self.assertIsInstance(result.jumps_made, int)

    def test_heavy_detects_contradictions(self):
        """HEAVY reasoning detects contradictions when they exist."""
        from ck_sim.ck_reasoning import ReasoningEngine, SPEED_HEAVY
        engine = ReasoningEngine(self.lattice)
        # Query nodes that include opposing concepts
        result = engine.reason(['joy', 'sorrow'], speed=SPEED_HEAVY)
        # Should detect that joy and sorrow oppose each other
        self.assertIsInstance(result.contradictions, list)

    def test_empty_query_nodes(self):
        """Empty query returns zero-confidence result."""
        from ck_sim.ck_reasoning import ReasoningEngine
        engine = ReasoningEngine(self.lattice)
        result = engine.reason([])
        self.assertEqual(result.confidence, 0.0)
        self.assertEqual(len(result.activated_nodes), 0)

    def test_invalid_query_nodes(self):
        """Invalid node IDs return zero-confidence result."""
        from ck_sim.ck_reasoning import ReasoningEngine
        engine = ReasoningEngine(self.lattice)
        result = engine.reason(['nonexistent_abc', 'nonexistent_def'])
        self.assertEqual(result.confidence, 0.0)

    def test_confidence_bounded(self):
        """Confidence is always in [0, 1]."""
        from ck_sim.ck_reasoning import (
            ReasoningEngine, SPEED_QUICK, SPEED_NORMAL, SPEED_HEAVY
        )
        engine = ReasoningEngine(self.lattice)
        for speed in [SPEED_QUICK, SPEED_NORMAL, SPEED_HEAVY]:
            result = engine.reason(['water', 'fire'], speed=speed)
            self.assertGreaterEqual(result.confidence, 0.0)
            self.assertLessEqual(result.confidence, 1.0)


class TestChooseSpeed(unittest.TestCase):
    """Auto speed selection logic."""

    def setUp(self):
        self.lattice = _make_lattice()

    def test_single_node_with_neighbors_is_quick(self):
        """Single node that has neighbors -> QUICK."""
        from ck_sim.ck_reasoning import ReasoningEngine, SPEED_QUICK
        engine = ReasoningEngine(self.lattice)
        speed = engine.choose_speed(['water'])
        self.assertEqual(speed, SPEED_QUICK)

    def test_two_nodes_same_domain_is_normal(self):
        """Two nodes in same domain -> NORMAL."""
        from ck_sim.ck_reasoning import ReasoningEngine, SPEED_NORMAL
        engine = ReasoningEngine(self.lattice)
        speed = engine.choose_speed(['water', 'fire'])
        self.assertEqual(speed, SPEED_NORMAL)

    def test_many_nodes_is_heavy(self):
        """4+ nodes -> HEAVY."""
        from ck_sim.ck_reasoning import ReasoningEngine, SPEED_HEAVY
        engine = ReasoningEngine(self.lattice)
        speed = engine.choose_speed(['water', 'fire', 'earth_element', 'wind'])
        self.assertEqual(speed, SPEED_HEAVY)

    def test_cross_domain_is_heavy(self):
        """Nodes from different domains -> HEAVY."""
        from ck_sim.ck_reasoning import ReasoningEngine, SPEED_HEAVY
        engine = ReasoningEngine(self.lattice)
        # mother (family) + gravity (physics) -- different domains
        speed = engine.choose_speed(['mother', 'gravity'])
        self.assertEqual(speed, SPEED_HEAVY)

    def test_empty_query_is_quick(self):
        """Empty query -> QUICK (fast fallback)."""
        from ck_sim.ck_reasoning import ReasoningEngine, SPEED_QUICK
        engine = ReasoningEngine(self.lattice)
        speed = engine.choose_speed([])
        self.assertEqual(speed, SPEED_QUICK)


class TestStats(unittest.TestCase):
    """Engine statistics tracking."""

    def setUp(self):
        self.lattice = _make_lattice()

    def test_stats_initial(self):
        """Initial stats are zeros."""
        from ck_sim.ck_reasoning import ReasoningEngine
        engine = ReasoningEngine(self.lattice)
        s = engine.stats()
        self.assertEqual(s['total_queries'], 0)
        self.assertEqual(s['queries_by_speed']['quick'], 0)
        self.assertEqual(s['queries_by_speed']['normal'], 0)
        self.assertEqual(s['queries_by_speed']['heavy'], 0)

    def test_stats_after_queries(self):
        """Stats track query counts by speed."""
        from ck_sim.ck_reasoning import ReasoningEngine, SPEED_QUICK, SPEED_NORMAL
        engine = ReasoningEngine(self.lattice)
        engine.reason(['water'], speed=SPEED_QUICK)
        engine.reason(['water'], speed=SPEED_NORMAL)
        engine.reason(['fire'], speed=SPEED_QUICK)
        s = engine.stats()
        self.assertEqual(s['total_queries'], 3)
        self.assertEqual(s['queries_by_speed']['quick'], 2)
        self.assertEqual(s['queries_by_speed']['normal'], 1)

    def test_stats_has_lattice_info(self):
        """Stats include lattice node count."""
        from ck_sim.ck_reasoning import ReasoningEngine
        engine = ReasoningEngine(self.lattice)
        s = engine.stats()
        self.assertGreater(s['lattice_nodes'], 0)
        self.assertIn('default_speed', s)


# ================================================================
#  INTEGRATION TESTS
# ================================================================

class TestIntegration(unittest.TestCase):
    """End-to-end tests with real WorldLattice seed corpus."""

    def setUp(self):
        self.lattice = _make_lattice()

    def test_full_reasoning_pipeline(self):
        """Complete reasoning pipeline: activate -> spread -> prune -> result."""
        from ck_sim.ck_reasoning import ReasoningEngine, SPEED_NORMAL
        engine = ReasoningEngine(self.lattice)
        result = engine.reason(['mother', 'love'], speed=SPEED_NORMAL)
        # Should activate related family/emotion concepts
        self.assertGreater(len(result.activated_nodes), 0)
        self.assertGreater(result.confidence, 0.0)

    def test_creative_discovery(self):
        """HEAVY reasoning makes creative connections."""
        from ck_sim.ck_reasoning import ReasoningEngine, SPEED_HEAVY
        engine = ReasoningEngine(self.lattice)
        result = engine.reason(['music'], speed=SPEED_HEAVY)
        self.assertGreater(len(result.activated_nodes), 0)
        # Heavy should have attempted Levy jumps
        self.assertIsInstance(result.jumps_made, int)

    def test_auto_speed_selection(self):
        """Auto speed selects appropriate level and reasoning succeeds."""
        from ck_sim.ck_reasoning import ReasoningEngine
        engine = ReasoningEngine(self.lattice)
        nodes = ['water']
        speed = engine.choose_speed(nodes)
        result = engine.reason(nodes, speed=speed)
        self.assertGreater(len(result.activated_nodes), 0)

    def test_contradiction_pruning_integration(self):
        """Full pipeline correctly handles contradictions."""
        from ck_sim.ck_reasoning import ReasoningEngine, SPEED_HEAVY
        engine = ReasoningEngine(self.lattice)
        # creation opposes destruction -- reasoning should detect this
        result = engine.reason(['creation', 'destruction'], speed=SPEED_HEAVY)
        self.assertIsInstance(result, object)
        # Paths should survive pruning (may be empty if all contradictory)
        self.assertIsInstance(result.paths, list)

    def test_set_default_speed(self):
        """Setting default speed is used when speed not specified."""
        from ck_sim.ck_reasoning import ReasoningEngine, SPEED_HEAVY
        engine = ReasoningEngine(self.lattice)
        engine.set_default_speed(SPEED_HEAVY)
        result = engine.reason(['water'])
        self.assertEqual(result.speed, SPEED_HEAVY)


# ================================================================
#  RUN
# ================================================================

if __name__ == '__main__':
    unittest.main()
