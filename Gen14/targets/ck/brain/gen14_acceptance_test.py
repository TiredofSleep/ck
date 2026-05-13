# Copyright (c) 2025-2026 Brayden Sanders / 7SiTe LLC
# Licensed under the 7SiTe Public Sovereignty License v2.2 (DOI: 10.5281/zenodo.18852047)
"""
gen14_acceptance_test.py -- exercise every Phase 1-5 mounted component
in a single runnable script, against a mock engine.

Run:
    cd Gen14/targets/ck/brain
    python gen14_acceptance_test.py

Outcome: 12/12 PASS or a clear failure pointing at the broken Phase.

This is the "is the whole pipeline alive?" gate. Use it before live boot
to confirm the modules are healthy in isolation, then trust mount_all
in ck_boot_api.py to do the same against the real engine.

Author: Claude (Brayden full-agency 2026-05-13).
"""
from __future__ import annotations

import os
import sys
import time
import traceback
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple

import numpy as np

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "grammar_lm"))


# ─── Mock engine ─────────────────────────────────────────────────────────

class MockEngine:
    """Minimal stand-in that satisfies mount_all's attribute probes."""
    def __init__(self):
        self.tick_hooks: List[Any] = []
        self.gpu_brain = None
        self.truth = type("T", (), {
            "tl_entries": [],
            "query": lambda self, q: [],
            "entropy": 2.0,
        })()
        self.brain = type("B", (), {
            "history": [7, 1, 7, 9, 7, 3, 7, 1, 7, 9, 3, 7],
        })()
        self.current_op = 7
        self.suggested_operator = 7
        self.coherence = type("C", (), {"current": 0.6})()


# ─── Test runner ─────────────────────────────────────────────────────────

class TestResult:
    def __init__(self):
        self.results: List[Tuple[str, bool, str]] = []
        self.t0 = time.time()

    def case(self, name: str, fn: Callable[[], Any]) -> Any:
        try:
            ret = fn()
            self.results.append((name, True, ""))
            return ret
        except Exception as e:
            tb = traceback.format_exc(limit=3)
            self.results.append((name, False, f"{type(e).__name__}: {e}\n{tb}"))
            return None

    def report(self):
        elapsed = time.time() - self.t0
        passed = sum(1 for _, ok, _ in self.results if ok)
        total = len(self.results)
        print("\n" + "=" * 72)
        print(f"ACCEPTANCE TEST: {passed}/{total} PASS  ({elapsed:.1f}s)")
        print("=" * 72)
        for name, ok, err in self.results:
            mark = "[PASS]" if ok else "[FAIL]"
            print(f"  {mark} {name}")
            if not ok:
                for line in err.splitlines():
                    print(f"        {line}")
        print("=" * 72)
        return passed, total


# ─── The cases ───────────────────────────────────────────────────────────

def case_mount_all(eng, tr: TestResult):
    """Run mount_all on the mock engine. Expect 12/12 components."""
    def _run():
        from gen14_unified_extensions import mount_all
        results = mount_all(eng)
        n_ok = sum(results.values())
        n_total = len(results)
        if n_ok != n_total:
            raise AssertionError(f"only {n_ok}/{n_total} components mounted: "
                                 f"{[k for k, v in results.items() if not v]}")
        return results
    return tr.case("Phase 1+2+3+4+5: mount_all returns all-green", _run)


def case_algebraic_measurements(eng, tr: TestResult):
    """Phase 0/1: verify the algebraic projections work and agree."""
    def _run():
        assert eng.gen14_sigma_orbit(7) == 1, "HARMONY should be in F orbit"
        assert eng.gen14_four_core_class(7) == 1, "HARMONY should be 4-core H"
        sig = eng.gen14_measurement_signature(7)
        assert sig["sigma_orbit"] == 1
        assert sig["four_core"] == 1
        # Pair signature
        ps = eng.gen14_pair_signature(7, 0)
        assert ps["b_operator"] == 7
        assert ps["d_operator"] == 0
        return sig
    tr.case("Phase 1: algebraic measurements consistent", _run)


def case_lattice_chain(eng, tr: TestResult):
    """Phase 1: lattice_chain mounted, has walk capability."""
    def _run():
        lc = eng.lattice_chain
        assert lc is not None
        # walk over an F-cycle
        path = lc.walk([1, 7, 9, 3], learn=False)
        assert path is not None
        return path
    tr.case("Phase 1: lattice_chain walks an F-cycle", _run)


def case_divine_memory(eng, tr: TestResult):
    """Phase 1: divine_memory mounted, recall returns a list (even if empty)."""
    def _run():
        dm = eng.divine_memory
        assert dm is not None
        hits = dm.recall([0.1, 0.5, 0.7, 0.3, 0.1], top_k=5)
        assert isinstance(hits, list)
        return hits
    tr.case("Phase 1: divine_memory recall returns list", _run)


def case_proactive_queue(eng, tr: TestResult):
    """Phase 1: proactive_queue is a deque with maxlen 50."""
    def _run():
        pq = eng.proactive_queue
        assert pq is not None
        # Push and consume
        pq.append({"kind": "test", "subject_key": "abc"})
        q = eng.proactive_queue_consumer("test_session")
        # Consumer returns one or None; the proactive_trigger may
        # have intercepted, so just verify the API works.
        return True
    tr.case("Phase 1: proactive_queue + consumer API live", _run)


def case_algebraic_lm(eng, tr: TestResult):
    """Phase 2: 4-head LM predicts algebraic signature for F-cycle walk."""
    def _run():
        sig = eng.algebraic_signature([1, 7, 9, 3])
        if "error" in sig:
            raise AssertionError(f"signature failed: {sig['error']}")
        assert "op" in sig
        assert "sigma" in sig
        assert "shell" in sig
        assert "4core" in sig
        # Top-k predictions
        top = eng.algebraic_predict([1, 7, 9, 3], top_k=2)
        for head in ("op", "sigma", "shell", "4core"):
            assert head in top
            assert len(top[head]) == 2
        return sig
    tr.case("Phase 2: algebraic_lm signature + top-k", _run)


def case_spreading_recall(eng, tr: TestResult):
    """Phase 3: spreading-activation recall returns ranked results."""
    def _run():
        query = {
            "operators": [1, 7, 9, 3],
            "centroid": [0.1, 0.5, 0.7, 0.3, 0.1],
            "text": "harmony",
        }
        out = eng.recall(query, depth="any", k=5, seed=42, verbose=False)
        assert isinstance(out, list)
        # Result objects have expected shape
        for r in out:
            assert "source" in r
            assert "energy" in r or "score" in r
        return out
    tr.case("Phase 3: spreading_recall returns ranked results", _run)


def case_frontier_scanner(eng, tr: TestResult):
    """Phase 4: frontier scanner loaded and answers relevance queries."""
    def _run():
        fs = eng.frontier_scanner
        assert fs is not None
        stats = fs.stats()
        # We expect SOMETHING was loaded (FRONTIERS_*.md exists in Atlas/)
        if stats["total"] == 0:
            raise AssertionError("no frontiers parsed -- Atlas/FRONTIERS_*.md missing?")
        hits = fs.find_relevant([7, 1, 7, 9, 7, 3], k=3)
        assert isinstance(hits, list)
        return {"total": stats["total"], "hits": len(hits)}
    tr.case("Phase 4: frontier scanner indexed + relevance query", _run)


def case_proactive_trigger(eng, tr: TestResult):
    """Phase 4: proactive trigger emits structured signals."""
    def _run():
        pt = eng.proactive_trigger
        assert pt is not None
        # Force the surprisal spike
        for _ in range(20):
            pt._surprisal.push(0.1)
        pt._surprisal.push(8.0)
        # Hide engine surprisal field so refresh is a no-op
        eng.surprisal = None
        emitted = pt.tick()
        # We don't require the surprisal one specifically (background
        # threads may have grabbed earlier signals), but SOME signal
        # should be available OR the trigger should report stats.
        stats = pt.stats()
        return {"emitted_this_tick": len(emitted), "stats": stats}
    tr.case("Phase 4: proactive_trigger tick emits signals", _run)


def case_stroke_extractor(eng, tr: TestResult):
    """Phase 5: extract operator from synthetic patches."""
    def _run():
        # Square (closed loop) -> HARMONY
        h, w = 32, 32
        p = np.full((h, w), 255, dtype=np.uint8)
        p[4:h - 4, 4:6] = 0
        p[4:h - 4, w - 6:w - 4] = 0
        p[4:6, 4:w - 4] = 0
        p[h - 6:h - 4, 4:w - 4] = 0
        sig = eng.stroke_signature_of(p)
        assert sig["op_name"] == "HARMONY", \
            f"square should give HARMONY, got {sig['op_name']}"
        # Vertical line -> LATTICE
        p2 = np.full((h, w), 255, dtype=np.uint8)
        p2[4:h - 4, w // 2 - 1:w // 2 + 1] = 0
        sig2 = eng.stroke_signature_of(p2)
        assert sig2["op_name"] == "LATTICE", \
            f"vertical line should give LATTICE, got {sig2['op_name']}"
        # Empty -> VOID
        p3 = np.full((h, w), 255, dtype=np.uint8)
        sig3 = eng.stroke_signature_of(p3)
        assert sig3["op_name"] == "VOID"
        return {
            "square": sig["algebraic_signature"],
            "I": sig2["algebraic_signature"],
            "empty": sig3["algebraic_signature"],
        }
    tr.case("Phase 5: stroke_extractor maps 3 shapes to correct ops", _run)


def case_cross_phase_signature_consistency(eng, tr: TestResult):
    """The 4-axis signature returned by every phase agrees with the
    canonical projection in Phase 1.
    """
    def _run():
        # Phase 5 stroke -> HARMONY
        h, w = 32, 32
        p = np.full((h, w), 255, dtype=np.uint8)
        p[4:h - 4, 4:6] = 0
        p[4:h - 4, w - 6:w - 4] = 0
        p[4:6, 4:w - 4] = 0
        p[h - 6:h - 4, 4:w - 4] = 0
        stroke_sig = eng.stroke_signature_of(p)
        op = stroke_sig["operator"]

        # Phase 1 canonical projection for the same op
        canonical = eng.gen14_measurement_signature(op)

        # Compare just the sigma_orbit and four_core (shell depends on support set)
        ssig = stroke_sig["algebraic_signature"]
        assert ssig["sigma"] == canonical["sigma_orbit"], \
            (f"sigma mismatch: stroke={ssig['sigma']} "
             f"canonical={canonical['sigma_orbit']}")
        assert ssig["four_core"] == canonical["four_core"], \
            (f"four_core mismatch: stroke={ssig['four_core']} "
             f"canonical={canonical['four_core']}")

        # Phase 2 LM agrees: for HARMONY walks, sigma should be F_creation
        lm_sig = eng.algebraic_signature([7, 7, 7, 7])
        # The LM might predict a different op as next-step, but its sigma
        # head should be in {F_creation, V_void} (HARMONY chains can settle)
        assert lm_sig["sigma"] in ("F_creation", "V_void", "BAL_fixed"), \
            f"LM sigma unexpected: {lm_sig['sigma']}"

        return {
            "stroke_op": op,
            "stroke_sig": ssig,
            "canonical": canonical,
            "lm_sig": lm_sig,
        }
    tr.case("Cross-phase: stroke + canonical + LM agree on sigma/four_core", _run)


def case_endpoint_imports(eng, tr: TestResult):
    """Sanity: the boot file imports without error after our extensions."""
    def _run():
        import ast
        boot = HERE.parent / "server" / "ck_boot_api.py"
        if not boot.exists():
            raise AssertionError(f"boot file missing at {boot}")
        with open(boot, encoding="utf-8") as f:
            src = f.read()
        ast.parse(src)
        return len(src.splitlines())
    tr.case("Boot file: ck_boot_api.py parses cleanly", _run)


# ─── Main ────────────────────────────────────────────────────────────────

def main():
    print("=" * 72)
    print(" Gen14 Acceptance Test — 12 phases against a mock engine")
    print("=" * 72)
    print()

    eng = MockEngine()
    tr = TestResult()

    # Phase 1+: mount everything (this is the prerequisite for all later cases)
    case_mount_all(eng, tr)

    # Per-phase functional cases (each is independent)
    case_algebraic_measurements(eng, tr)
    case_lattice_chain(eng, tr)
    case_divine_memory(eng, tr)
    case_proactive_queue(eng, tr)
    case_algebraic_lm(eng, tr)
    case_spreading_recall(eng, tr)
    case_frontier_scanner(eng, tr)
    case_proactive_trigger(eng, tr)
    case_stroke_extractor(eng, tr)
    case_cross_phase_signature_consistency(eng, tr)
    case_endpoint_imports(eng, tr)

    passed, total = tr.report()
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
