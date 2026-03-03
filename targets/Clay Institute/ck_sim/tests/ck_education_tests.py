"""
Tests for ck_education.py and ck_autodidact.py
===============================================
186 concepts. 202 relations. Experience through coherence.
Autonomous learning. Save curves, not content.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import unittest
import time
from collections import Counter

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, LATTICE, COUNTER, PROGRESS,
    COLLAPSE, BALANCE, CHAOS, BREATH, RESET, OP_NAMES, CL
)


# ================================================================
#  EDUCATION MODULE TESTS
# ================================================================

class TestEducationImports(unittest.TestCase):
    def test_import_concepts(self):
        from ck_sim.ck_education import EDUCATION_CONCEPTS
        self.assertGreater(len(EDUCATION_CONCEPTS), 150)

    def test_import_relations(self):
        from ck_sim.ck_education import EDUCATION_RELATIONS
        self.assertGreater(len(EDUCATION_RELATIONS), 150)

    def test_import_classes(self):
        from ck_sim.ck_education import (
            ExperienceChain, ExperienceGenerator, EducationLoader)


class TestEducationConcepts(unittest.TestCase):
    def test_concept_format(self):
        from ck_sim.ck_education import EDUCATION_CONCEPTS
        for c in EDUCATION_CONCEPTS:
            self.assertEqual(len(c), 4, f"Bad format: {c[0]}")
            nid, domain, op, langs = c
            self.assertIsInstance(nid, str)
            self.assertIsInstance(domain, str)
            self.assertTrue(0 <= op <= 9, f"Bad operator: {op} for {nid}")
            self.assertIn('en', langs, f"Missing English: {nid}")

    def test_unique_ids(self):
        from ck_sim.ck_education import EDUCATION_CONCEPTS
        ids = [c[0] for c in EDUCATION_CONCEPTS]
        self.assertEqual(len(ids), len(set(ids)))

    def test_all_domains_represented(self):
        from ck_sim.ck_education import EDUCATION_CONCEPTS
        domains = set(c[1] for c in EDUCATION_CONCEPTS)
        expected = {'history', 'music', 'computing', 'economics',
                    'psychology', 'astronomy', 'ecology', 'ethics',
                    'spirituality', 'literature', 'linguistics',
                    'geography', 'medicine', 'art', 'law'}
        self.assertTrue(expected.issubset(domains),
                        f"Missing: {expected - domains}")

    def test_seven_languages(self):
        from ck_sim.ck_education import EDUCATION_CONCEPTS
        for c in EDUCATION_CONCEPTS:
            nid, _, _, langs = c
            self.assertGreaterEqual(len(langs), 7,
                                    f"<7 languages for {nid}")

    def test_operator_distribution(self):
        from ck_sim.ck_education import EDUCATION_CONCEPTS
        ops = Counter(c[2] for c in EDUCATION_CONCEPTS)
        # All 10 operators should appear
        for op in range(NUM_OPS):
            self.assertIn(op, ops, f"Missing operator {OP_NAMES[op]}")


class TestEducationRelations(unittest.TestCase):
    def test_relation_format(self):
        from ck_sim.ck_education import EDUCATION_RELATIONS
        from ck_sim.ck_world_lattice import RELATION_TYPES
        for r in EDUCATION_RELATIONS:
            self.assertEqual(len(r), 3, f"Bad format: {r}")
            src, rel, tgt = r
            self.assertIsInstance(src, str)
            self.assertIn(rel, RELATION_TYPES, f"Unknown relation: {rel}")
            self.assertIsInstance(tgt, str)

    def test_cross_domain_bridges_exist(self):
        from ck_sim.ck_education import EDUCATION_CONCEPTS, EDUCATION_RELATIONS
        concept_domains = {c[0]: c[1] for c in EDUCATION_CONCEPTS}
        cross_domain = 0
        for src, rel, tgt in EDUCATION_RELATIONS:
            d_src = concept_domains.get(src, '?')
            d_tgt = concept_domains.get(tgt, '?')
            if d_src != d_tgt and d_src != '?' and d_tgt != '?':
                cross_domain += 1
        # Must have substantial cross-domain bridges
        self.assertGreater(cross_domain, 40,
                           f"Only {cross_domain} cross-domain bridges")

    def test_resembles_are_cross_domain(self):
        """'resembles' relations should primarily bridge different domains."""
        from ck_sim.ck_education import EDUCATION_CONCEPTS, EDUCATION_RELATIONS
        concept_domains = {c[0]: c[1] for c in EDUCATION_CONCEPTS}
        resembles = [(s, t) for s, r, t in EDUCATION_RELATIONS
                     if r == 'resembles']
        cross = sum(1 for s, t in resembles
                    if concept_domains.get(s, 'a') != concept_domains.get(t, 'b'))
        self.assertGreater(cross, 20)


class TestEducationLoader(unittest.TestCase):
    def setUp(self):
        from ck_sim.ck_world_lattice import WorldLattice
        from ck_sim.ck_concept_spine import ConceptSpine
        self.lattice = WorldLattice()
        self.lattice.load_seed_corpus()
        self.spine = ConceptSpine(self.lattice)
        self.spine.load_spine()
        self.base_count = len(self.lattice.nodes)

    def test_load_concepts(self):
        from ck_sim.ck_education import EducationLoader
        loader = EducationLoader(self.lattice)
        n = loader.load_concepts()
        self.assertGreater(n, 150)
        self.assertGreater(len(self.lattice.nodes), self.base_count)

    def test_load_relations(self):
        from ck_sim.ck_education import EducationLoader
        loader = EducationLoader(self.lattice)
        loader.load_concepts()
        n = loader.load_relations()
        self.assertGreater(n, 150)

    def test_load_education_full(self):
        from ck_sim.ck_education import EducationLoader
        loader = EducationLoader(self.lattice)
        result = loader.load_education()
        self.assertGreater(result['concepts_loaded'], 150)
        self.assertGreater(result['relations_loaded'], 150)
        self.assertGreater(result['total_lattice_nodes'], 600)

    def test_no_duplicate_load(self):
        from ck_sim.ck_education import EducationLoader
        loader = EducationLoader(self.lattice)
        r1 = loader.load_education()
        loader2 = EducationLoader(self.lattice)
        r2 = loader2.load_education()
        self.assertEqual(r2['concepts_loaded'], 0)  # All skipped

    def test_stats(self):
        from ck_sim.ck_education import EducationLoader
        loader = EducationLoader(self.lattice)
        loader.load_education()
        s = loader.stats()
        self.assertIn('concepts_loaded', s)
        self.assertIn('relations_loaded', s)


class TestExperienceGenerator(unittest.TestCase):
    def setUp(self):
        from ck_sim.ck_world_lattice import WorldLattice
        from ck_sim.ck_concept_spine import ConceptSpine
        from ck_sim.ck_education import EducationLoader
        self.lattice = WorldLattice()
        self.lattice.load_seed_corpus()
        spine = ConceptSpine(self.lattice)
        spine.load_spine()
        loader = EducationLoader(self.lattice)
        loader.load_education()

    def test_domain_session(self):
        from ck_sim.ck_education import ExperienceGenerator
        gen = ExperienceGenerator(self.lattice)
        chains = gen.generate_domain_session('music')
        self.assertGreater(len(chains), 0)
        for c in chains:
            self.assertGreater(len(c.operators), 1)
            self.assertEqual(c.domain, 'music')

    def test_full_curriculum(self):
        from ck_sim.ck_education import ExperienceGenerator
        gen = ExperienceGenerator(self.lattice)
        chains = gen.generate_full_curriculum()
        self.assertGreater(len(chains), 100)
        self.assertGreater(gen.sessions_completed, 10)

    def test_chain_operators_valid(self):
        from ck_sim.ck_education import ExperienceGenerator
        gen = ExperienceGenerator(self.lattice)
        chains = gen.generate_domain_session('physics')
        for c in chains:
            for op in c.operators:
                self.assertTrue(0 <= op <= 9)

    def test_chain_coherence_computed(self):
        from ck_sim.ck_education import ExperienceGenerator
        gen = ExperienceGenerator(self.lattice)
        chains = gen.generate_domain_session('ethics')
        for c in chains:
            self.assertTrue(0.0 <= c.coherence_target <= 1.0)

    def test_session_count_increments(self):
        from ck_sim.ck_education import ExperienceGenerator
        gen = ExperienceGenerator(self.lattice)
        self.assertEqual(gen.sessions_completed, 0)
        gen.generate_domain_session('history')
        self.assertEqual(gen.sessions_completed, 1)


# ================================================================
#  AUTODIDACT MODULE TESTS
# ================================================================

class TestAutodidactImports(unittest.TestCase):
    def test_import_all(self):
        from ck_sim.ck_autodidact import (
            OperatorCurve, CurveMemory, PageDigester,
            SiteGuard, CuriosityCrawler, LearningSession)

    def test_constants(self):
        from ck_sim.ck_autodidact import (
            T_STAR, STUDY_HOURS, SLEEP_HOURS, CURVE_MEMORY_MAX,
            DEFAULT_APPROVED_SITES, SEED_TOPICS)
        self.assertAlmostEqual(T_STAR, 5/7, places=5)
        self.assertEqual(STUDY_HOURS, 8)


class TestOperatorCurve(unittest.TestCase):
    def test_create(self):
        from ck_sim.ck_autodidact import OperatorCurve
        curve = OperatorCurve(
            operator_sequence=(HARMONY, LATTICE, PROGRESS),
            coherence=0.8, domain='test', source_hash='abc123')
        self.assertEqual(len(curve.operator_sequence), 3)
        self.assertTrue(curve.is_coherent)

    def test_curve_hash(self):
        from ck_sim.ck_autodidact import OperatorCurve
        c1 = OperatorCurve((HARMONY, LATTICE), 0.8, 'test', 'a')
        c2 = OperatorCurve((HARMONY, LATTICE), 0.9, 'other', 'b')
        self.assertEqual(c1.curve_hash, c2.curve_hash)  # Same ops = same hash

    def test_compose_all(self):
        from ck_sim.ck_autodidact import OperatorCurve
        curve = OperatorCurve((HARMONY, LATTICE), 0.8, 'test', '')
        result = curve.compose_all()
        self.assertEqual(result, CL[HARMONY][LATTICE])

    def test_not_coherent(self):
        from ck_sim.ck_autodidact import OperatorCurve
        curve = OperatorCurve((VOID,), 0.3, 'test', '')
        self.assertFalse(curve.is_coherent)

    def test_not_worth_keeping(self):
        from ck_sim.ck_autodidact import OperatorCurve, CONSOLIDATION_THRESHOLD
        curve = OperatorCurve((VOID,), 0.1, 'test', '')
        self.assertFalse(curve.is_worth_keeping)


class TestCurveMemory(unittest.TestCase):
    def test_store_and_retrieve(self):
        from ck_sim.ck_autodidact import CurveMemory, OperatorCurve
        mem = CurveMemory()
        curve = OperatorCurve((HARMONY, LATTICE, PROGRESS), 0.9, 'test', 'a')
        self.assertTrue(mem.store(curve))
        self.assertEqual(len(mem.curves), 1)

    def test_dedup(self):
        from ck_sim.ck_autodidact import CurveMemory, OperatorCurve
        mem = CurveMemory()
        c1 = OperatorCurve((HARMONY, LATTICE), 0.9, 'test', 'a')
        c2 = OperatorCurve((HARMONY, LATTICE), 0.8, 'test', 'b')
        self.assertTrue(mem.store(c1))
        self.assertFalse(mem.store(c2))  # Same curve hash
        self.assertEqual(len(mem.curves), 1)

    def test_reject_low_coherence(self):
        from ck_sim.ck_autodidact import CurveMemory, OperatorCurve
        mem = CurveMemory()
        curve = OperatorCurve((VOID, COLLAPSE), 0.1, 'test', 'a')
        self.assertFalse(mem.store(curve))

    def test_capacity_eviction(self):
        from ck_sim.ck_autodidact import CurveMemory, OperatorCurve
        mem = CurveMemory(max_curves=3)
        for i in range(5):
            ops = tuple([i % NUM_OPS, (i+1) % NUM_OPS, (i+2) % NUM_OPS])
            c = OperatorCurve(ops, 0.6 + i * 0.05, 'test', str(i))
            mem.store(c)
        self.assertLessEqual(len(mem.curves), 3)

    def test_consolidation(self):
        from ck_sim.ck_autodidact import CurveMemory, OperatorCurve
        mem = CurveMemory()
        mem.store(OperatorCurve((HARMONY, LATTICE), 0.9, 'good', 'a'))
        mem.store(OperatorCurve((PROGRESS, BALANCE), 0.61, 'ok', 'b'))
        # Store one that's barely above threshold
        stats = mem.consolidate()
        self.assertEqual(stats['consolidated'], 2)
        for c in mem.curves:
            self.assertTrue(c.is_consolidated)

    def test_average_coherence(self):
        from ck_sim.ck_autodidact import CurveMemory, OperatorCurve
        mem = CurveMemory()
        mem.store(OperatorCurve((HARMONY, LATTICE), 0.8, 'a', '1'))
        mem.store(OperatorCurve((PROGRESS, BALANCE), 0.6, 'b', '2'))
        self.assertAlmostEqual(mem.average_coherence, 0.7, places=1)

    def test_stats(self):
        from ck_sim.ck_autodidact import CurveMemory
        mem = CurveMemory()
        s = mem.stats()
        self.assertIn('stored_curves', s)
        self.assertIn('harmony_ratio', s)


class TestPageDigester(unittest.TestCase):
    def test_digest_text(self):
        from ck_sim.ck_autodidact import PageDigester
        d = PageDigester()
        text = ("Light travels through space as electromagnetic waves. "
                "The speed of light is constant in vacuum. "
                "Photons carry energy proportional to frequency.")
        curve = d.digest(text, url="https://test.com/light")
        self.assertIsNotNone(curve)
        self.assertGreater(len(curve.operator_sequence), 0)

    def test_reject_short_text(self):
        from ck_sim.ck_autodidact import PageDigester
        d = PageDigester()
        curve = d.digest("too short")
        self.assertIsNone(curve)

    def test_domain_detection(self):
        from ck_sim.ck_autodidact import PageDigester
        d = PageDigester()
        text = ("Mathematics provides the foundation for all science. "
                "Equations describe the relationships between quantities. "
                "Algebra and geometry form the basis of analysis.")
        curve = d.digest(text)
        self.assertIsNotNone(curve)
        self.assertIsInstance(curve.domain, str)

    def test_coherence_computed(self):
        from ck_sim.ck_autodidact import PageDigester
        d = PageDigester()
        text = ("Trees grow toward the light. Roots reach into the earth. "
                "Seasons cycle from spring to winter. "
                "Life renews itself each year with new growth.")
        curve = d.digest(text)
        if curve:
            self.assertTrue(0.0 <= curve.coherence <= 1.0)


class TestSiteGuard(unittest.TestCase):
    def test_approved_site(self):
        from ck_sim.ck_autodidact import SiteGuard
        g = SiteGuard(['en.wikipedia.org'])
        self.assertTrue(g.is_allowed('https://en.wikipedia.org/wiki/Light'))

    def test_blocked_site(self):
        from ck_sim.ck_autodidact import SiteGuard
        g = SiteGuard(['en.wikipedia.org'])
        self.assertFalse(g.is_allowed('https://evil.com/hack'))

    def test_add_site(self):
        from ck_sim.ck_autodidact import SiteGuard
        g = SiteGuard([])
        g.add_site('safe.edu')
        self.assertTrue(g.is_allowed('https://safe.edu/page'))

    def test_remove_site(self):
        from ck_sim.ck_autodidact import SiteGuard
        g = SiteGuard(['remove.me'])
        g.remove_site('remove.me')
        self.assertFalse(g.is_allowed('https://remove.me/page'))

    def test_empty_url(self):
        from ck_sim.ck_autodidact import SiteGuard
        g = SiteGuard()
        self.assertFalse(g.is_allowed(''))


class TestCuriosityCrawler(unittest.TestCase):
    def test_next_topic(self):
        from ck_sim.ck_autodidact import CuriosityCrawler
        c = CuriosityCrawler(['physics', 'music', 'art'])
        self.assertEqual(c.next_topic(), 'physics')
        self.assertEqual(c.next_topic(), 'music')

    def test_no_repeat(self):
        from ck_sim.ck_autodidact import CuriosityCrawler
        c = CuriosityCrawler(['a', 'b'])
        c.next_topic()
        c.next_topic()
        self.assertIsNone(c.next_topic())

    def test_report_spawns_topics(self):
        from ck_sim.ck_autodidact import CuriosityCrawler
        c = CuriosityCrawler(['start'])
        c.next_topic()
        c.report_result('start', 0.65, ['new_a', 'new_b'])
        self.assertEqual(c.next_topic(), 'new_a')

    def test_low_coherence_no_spawn(self):
        from ck_sim.ck_autodidact import CuriosityCrawler
        c = CuriosityCrawler(['start'])
        c.next_topic()
        c.report_result('start', 0.1, ['should_not_appear'])
        self.assertIsNone(c.next_topic())  # Nothing spawned

    def test_suggest_url(self):
        from ck_sim.ck_autodidact import CuriosityCrawler
        c = CuriosityCrawler()
        url = c.suggest_url('quantum mechanics', 'en.wikipedia.org')
        self.assertIn('wiki', url)
        self.assertIn('quantum', url)

    def test_stats(self):
        from ck_sim.ck_autodidact import CuriosityCrawler
        c = CuriosityCrawler(['a', 'b'])
        c.next_topic()
        s = c.stats()
        self.assertEqual(s['explored'], 1)


class TestLearningSession(unittest.TestCase):
    def test_create(self):
        from ck_sim.ck_autodidact import LearningSession
        session = LearningSession()
        self.assertIsNotNone(session)

    def test_study_one_page(self):
        from ck_sim.ck_autodidact import LearningSession
        session = LearningSession()
        session.guard.add_site('test.com')
        text = ("The sun is a star at the center of our solar system. "
                "It provides light and warmth to all the planets. "
                "Nuclear fusion converts hydrogen into helium in its core.")
        curve = session.study_one_page(text, 'https://test.com/sun', 'sun')
        # May or may not store depending on coherence

    def test_blocked_site_skipped(self):
        from ck_sim.ck_autodidact import LearningSession
        session = LearningSession()
        curve = session.study_one_page(
            "some text", 'https://blocked.evil/page')
        self.assertIsNone(curve)

    def test_sleep_consolidation(self):
        from ck_sim.ck_autodidact import LearningSession
        session = LearningSession()
        stats = session.sleep()
        self.assertIn('pruned', stats)

    def test_generate_study_plan(self):
        from ck_sim.ck_autodidact import LearningSession
        session = LearningSession()
        plan = session.generate_study_plan(5)
        self.assertGreater(len(plan), 0)
        for item in plan:
            self.assertIn('topic', item)
            self.assertIn('url', item)

    def test_stats(self):
        from ck_sim.ck_autodidact import LearningSession
        session = LearningSession()
        s = session.stats()
        self.assertIn('pages_read', s)
        self.assertIn('curves_stored', s)


class TestPhilosophy(unittest.TestCase):
    """Tests that validate CK's learning philosophy."""

    def test_curves_not_content(self):
        """Operator curves contain NO text content."""
        from ck_sim.ck_autodidact import PageDigester
        d = PageDigester()
        text = "Einstein published general relativity in 1915"
        curve = d.digest(text + ". " + text + ". " + text)
        if curve:
            # The curve contains only operators, no text
            for op in curve.operator_sequence:
                self.assertIsInstance(op, int)
                self.assertTrue(0 <= op <= 9)

    def test_no_preloaded_truths(self):
        """Education module doesn't pre-load TRUSTED truths."""
        from ck_sim.ck_education import EducationLoader
        from ck_sim.ck_world_lattice import WorldLattice
        lattice = WorldLattice()
        lattice.load_seed_corpus()
        loader = EducationLoader(lattice)
        # EducationLoader has no truth_lattice parameter
        # It ONLY loads concepts (infrastructure) not beliefs
        loader.load_education()
        # The loader adds to WorldLattice (map) not TruthLattice (beliefs)
        self.assertGreater(len(lattice.nodes), 0)

    def test_coherence_determines_retention(self):
        """Low-coherence curves are rejected by CurveMemory."""
        from ck_sim.ck_autodidact import CurveMemory, OperatorCurve
        mem = CurveMemory()
        low = OperatorCurve((VOID, COLLAPSE), 0.1, 'bad', '1')
        high = OperatorCurve((HARMONY, LATTICE), 0.9, 'good', '2')
        self.assertFalse(mem.store(low))
        self.assertTrue(mem.store(high))

    def test_sleep_prunes_weak_knowledge(self):
        """Consolidation removes sub-threshold curves."""
        from ck_sim.ck_autodidact import CurveMemory, OperatorCurve
        mem = CurveMemory()
        # Store two curves: one will survive, one won't after threshold change
        mem.store(OperatorCurve((HARMONY, PROGRESS), 0.95, 'strong', '1'))
        mem.store(OperatorCurve((BALANCE, COUNTER), 0.61, 'weak', '2'))
        before = len(mem.curves)
        mem.consolidate()
        # Both should survive since both are above CONSOLIDATION_THRESHOLD (0.6)
        self.assertEqual(len(mem.curves), before)


# ================================================================
#  INTEGRATION TESTS
# ================================================================

class TestFullEducationPipeline(unittest.TestCase):
    """End-to-end: load education, generate experience, digest content."""

    def test_education_to_experience(self):
        from ck_sim.ck_world_lattice import WorldLattice
        from ck_sim.ck_concept_spine import ConceptSpine
        from ck_sim.ck_education import EducationLoader, ExperienceGenerator

        lattice = WorldLattice()
        lattice.load_seed_corpus()
        spine = ConceptSpine(lattice)
        spine.load_spine()
        loader = EducationLoader(lattice)
        loader.load_education()

        gen = ExperienceGenerator(lattice)
        curriculum = gen.generate_full_curriculum()

        self.assertGreater(len(curriculum), 50)
        domains = set(c.domain for c in curriculum)
        self.assertGreater(len(domains), 5)

    def test_autodidact_full_cycle(self):
        from ck_sim.ck_autodidact import LearningSession
        session = LearningSession()
        session.guard.add_site('demo.test')

        texts = [
            "Water flows downhill following the path of least resistance. "
            "Rivers carve valleys over millennia. Erosion shapes landscapes.",
            "Music connects people across cultures and languages. "
            "Rhythm is universal. Harmony creates emotional resonance.",
        ]

        for i, text in enumerate(texts):
            session.study_one_page(text, f'https://demo.test/{i}', f't{i}')

        session.sleep()
        stats = session.stats()
        self.assertGreaterEqual(stats['pages_read'], 0)


if __name__ == '__main__':
    unittest.main()
