"""
Tests for Clay SDV determinism -- same seed MUST produce identical results.
"""

import json
import os
import tempfile
import unittest

from ck_sim.doing.ck_clay_protocol import ProbeConfig, ClayProbe, ClayProtocol
from ck_sim.being.ck_tig_bundle import CLAY_PROBLEMS
from ck_sim.becoming.ck_clay_journal import (
    probe_result_to_dict, save_json, save_csv, generate_report, ClayJournal,
)


class TestDeterminism(unittest.TestCase):

    def test_same_seed_same_hash(self):
        """Same seed + same config = identical final hash."""
        cfg = ProbeConfig(problem_id='navier_stokes', test_case='lamb_oseen',
                          seed=42, n_levels=6)
        r1 = ClayProbe(cfg).run()

        cfg2 = ProbeConfig(problem_id='navier_stokes', test_case='lamb_oseen',
                           seed=42, n_levels=6)
        r2 = ClayProbe(cfg2).run()

        self.assertEqual(r1.final_hash, r2.final_hash)

    def test_same_seed_same_operators(self):
        """Same seed produces identical operator sequences."""
        cfg = ProbeConfig(seed=42, n_levels=8)
        r1 = ClayProbe(cfg).run()
        r2 = ClayProbe(ProbeConfig(seed=42, n_levels=8)).run()

        ops1 = [s.operator for s in r1.steps]
        ops2 = [s.operator for s in r2.steps]
        self.assertEqual(ops1, ops2)

    def test_same_seed_same_defects(self):
        """Same seed produces identical defect trajectories."""
        cfg = ProbeConfig(seed=42, n_levels=6)
        r1 = ClayProbe(cfg).run()
        r2 = ClayProbe(ProbeConfig(seed=42, n_levels=6)).run()

        for d1, d2 in zip(r1.defect_trajectory, r2.defect_trajectory):
            self.assertAlmostEqual(d1, d2, places=10)

    def test_different_seed_different_hash(self):
        """Different seeds produce different hashes."""
        r1 = ClayProbe(ProbeConfig(seed=42, n_levels=6)).run()
        r2 = ClayProbe(ProbeConfig(seed=123, n_levels=6)).run()
        self.assertNotEqual(r1.final_hash, r2.final_hash)

    def test_all_problems_deterministic(self):
        """Every problem is deterministic with the same seed."""
        for pid in CLAY_PROBLEMS:
            with self.subTest(problem=pid):
                cfg = ProbeConfig(problem_id=pid, seed=42, n_levels=4)
                r1 = ClayProbe(cfg).run()
                r2 = ClayProbe(ProbeConfig(problem_id=pid, seed=42, n_levels=4)).run()
                self.assertEqual(r1.final_hash, r2.final_hash)

    def test_step_hashes_deterministic(self):
        """Per-step hashes are also deterministic."""
        cfg = ProbeConfig(seed=42, n_levels=6)
        r1 = ClayProbe(cfg).run()
        r2 = ClayProbe(ProbeConfig(seed=42, n_levels=6)).run()

        for s1, s2 in zip(r1.steps, r2.steps):
            self.assertEqual(s1.step_hash, s2.step_hash)


class TestJournal(unittest.TestCase):

    def setUp(self):
        self.result = ClayProbe(ProbeConfig(seed=42, n_levels=4)).run()

    def test_to_dict(self):
        """ProbeResult serializes to dict without error."""
        d = probe_result_to_dict(self.result)
        self.assertEqual(d['problem_id'], 'navier_stokes')
        self.assertEqual(d['seed'], 42)
        self.assertEqual(len(d['steps']), 4)

    def test_json_roundtrip(self):
        """JSON output is valid and contains expected fields."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                          delete=False) as f:
            path = f.name
        try:
            save_json(self.result, path)
            with open(path) as f:
                data = json.load(f)
            self.assertEqual(data['problem_id'], 'navier_stokes')
            self.assertIn('_timestamp', data)
            self.assertIn('_version', data)
        finally:
            os.unlink(path)

    def test_csv_output(self):
        """CSV output has correct header and row count."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv',
                                          delete=False) as f:
            path = f.name
        try:
            save_csv(self.result, path)
            with open(path) as f:
                lines = f.readlines()
            # Header + 4 data rows
            self.assertEqual(len(lines), 5)
            self.assertIn('level', lines[0])
            self.assertIn('operator', lines[0])
        finally:
            os.unlink(path)

    def test_markdown_report(self):
        """Markdown report contains key sections."""
        report = generate_report(self.result)
        self.assertIn('# SDV Probe Report', report)
        self.assertIn('Measurement Verdict', report)
        self.assertIn('Operator Distribution', report)
        self.assertIn('3-6-9 Spine', report)
        self.assertIn('SCA Loop', report)
        self.assertIn('Per-Level Data', report)

    def test_journal_class(self):
        """ClayJournal creates output directory and files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            journal = ClayJournal(tmpdir)
            base = journal.record(self.result)
            self.assertTrue(os.path.exists(f'{base}.json'))
            self.assertTrue(os.path.exists(f'{base}.csv'))
            self.assertTrue(os.path.exists(f'{base}.md'))

    def test_journal_record_all(self):
        """ClayJournal records all results + cross-problem report."""
        protocol = ClayProtocol(seed=42, n_levels=4)
        results = protocol.run_all()
        summary = protocol.cross_problem_summary(results)

        with tempfile.TemporaryDirectory() as tmpdir:
            journal = ClayJournal(tmpdir)
            journal.record_all(results, summary)
            self.assertTrue(os.path.exists(
                os.path.join(tmpdir, 'all_results.json')))
            self.assertTrue(os.path.exists(
                os.path.join(tmpdir, 'cross_problem_report.md')))


if __name__ == '__main__':
    unittest.main()
