"""test_ck_health.py -- regression tests for the health aggregator."""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))

from ck_health import (  # noqa: E402
    CORE_MODULES,
    EXPECTED_MODULES,
    build_health,
)


class FakeEngine: pass


def test_empty_engine_minimal():
    eng = FakeEngine()
    h = build_health(eng)
    assert h["status"] in ("degraded", "minimal")
    assert h["counts"]["n_modules_mounted"] == 0
    assert h["counts"]["n_modules_missing"] == len(EXPECTED_MODULES)
    assert set(h["core_missing"]) == set(CORE_MODULES)
    print("T1 PASS: empty engine -> degraded status, all core missing")


def test_has_timestamp_and_epoch():
    eng = FakeEngine()
    h = build_health(eng)
    assert "timestamp" in h
    assert "epoch" in h
    assert isinstance(h["epoch"], (int, float))
    assert h["epoch"] > 1_000_000_000  # plausible epoch
    print("T2 PASS: health has timestamp + epoch fields")


def test_journal_only():
    from ck_journal import Journal
    tmp = Path(tempfile.gettempdir()) / "ck_h_t3.jsonl"
    if tmp.exists(): tmp.unlink()
    j = Journal(path=tmp)
    j.note("test")
    eng = FakeEngine()
    eng.ck_journal = {"journal": j}
    h = build_health(eng)
    assert h["modules"]["journal"]["mounted"] is True
    assert h["modules"]["journal"]["n_entries"] == 1
    assert h["counts"]["n_modules_mounted"] >= 1
    j.clear()
    print("T3 PASS: journal-only -> mounted=true + n_entries reported")


def test_all_simple_modules():
    """Mount the 'simple' modules (no rich status, just is-mounted check)."""
    eng = FakeEngine()
    eng.ck_pc_recommend = {"recommendations_for": lambda x: []}
    eng.ck_daily_summary = {"build_summary": lambda e, td=None: {}}
    eng.ck_search = {"unified_search": lambda q, n=5: {}}
    eng.ck_export = {"render_day_markdown": lambda e, td=None: ""}
    eng.ck_privacy = {"foo": "bar"}
    eng.ck_toolbox = {"foo": "bar"}
    eng.ck_lang = {"foo": "bar"}
    eng.ck_scope_auditor = {"foo": "bar"}
    h = build_health(eng)
    for k in ("pc_recommend", "daily_summary", "search", "export",
               "privacy", "toolbox", "languages", "scope_auditor"):
        assert h["modules"][k]["mounted"] is True, f"{k} should be mounted"
    print("T4 PASS: 8 simple modules detected as mounted")


def test_status_computed_correctly():
    """Verify status field is 'degraded' when core module missing,
    'ok' when all core present."""
    # All core
    eng = FakeEngine()
    eng.ck_pc_sense = {"daemon": None}
    eng.ck_journal = {"journal": None}
    eng.ck_rhythm = {"current_rhythm": None}
    eng.ck_scope_auditor = {"foo": "bar"}
    h = build_health(eng)
    assert len(h["core_missing"]) == 0
    assert h["status"] in ("ok", "minimal")  # not degraded since core full
    # Drop one core
    delattr(eng, "ck_scope_auditor")
    h = build_health(eng)
    assert "scope_auditor" in h["core_missing"]
    assert h["status"] == "degraded"
    print("T5 PASS: status reflects core-missing correctly")


def test_handles_module_errors_gracefully():
    """If a module's stats() call raises, health should report
    the error in that module's section but not crash overall."""
    class BadJournal:
        def stats(self):
            raise RuntimeError("simulated journal failure")
    eng = FakeEngine()
    eng.ck_journal = {"journal": BadJournal()}
    h = build_health(eng)
    assert h["modules"]["journal"]["mounted"] is True
    assert "error" in h["modules"]["journal"]
    assert "RuntimeError" in h["modules"]["journal"]["error"]
    # Overall health still returns; doesn't crash
    assert "status" in h
    print("T6 PASS: per-module errors caught and reported inline")


def test_pc_sense_with_real_data():
    from ck_pc_sense import PCSenseDaemon
    eng = FakeEngine()
    d = PCSenseDaemon(poll_hz=2.0, buffer_size=10)
    d.start()
    import time
    time.sleep(1.5)
    d.stop()
    eng.ck_pc_sense = {"daemon": d}
    h = build_health(eng)
    pc = h["modules"]["pc_sense"]
    assert pc["mounted"] is True
    assert pc["buffer_size"] == 10
    assert pc.get("n_readings", 0) >= 1
    assert pc.get("latest_op") in (
        "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
        "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"
    )
    print(f"T7 PASS: pc_sense reports buffer={pc['buffer_size']}, "
          f"n_readings={pc['n_readings']}, latest_op={pc['latest_op']}")


def test_uptime_tracking():
    """If engine has _started_ts, health reports uptime_seconds."""
    import time
    eng = FakeEngine()
    eng._started_ts = time.time() - 30  # 30 sec ago
    h = build_health(eng)
    assert h["uptime_seconds"] is not None
    assert 25 <= h["uptime_seconds"] <= 35
    # Without _started_ts, uptime is None
    eng2 = FakeEngine()
    h2 = build_health(eng2)
    assert h2["uptime_seconds"] is None
    print("T8 PASS: uptime_seconds tracked when engine._started_ts set")


def test_expected_module_list_complete():
    """EXPECTED_MODULES should include all the major modules we built."""
    must_have = {
        "pc_sense", "journal", "rhythm",
        "code_writer", "file_orient", "bookmark", "reminder",
        "pc_recommend", "daily_summary", "search", "export",
    }
    for m in must_have:
        assert m in EXPECTED_MODULES, f"EXPECTED_MODULES missing {m}"
    print(f"T9 PASS: EXPECTED_MODULES includes all {len(must_have)} primary modules")


def run_all():
    print("=" * 64)
    print("ck_health regression tests")
    print("=" * 64)
    print()
    tests = [test_empty_engine_minimal, test_has_timestamp_and_epoch,
              test_journal_only, test_all_simple_modules,
              test_status_computed_correctly,
              test_handles_module_errors_gracefully,
              test_pc_sense_with_real_data, test_uptime_tracking,
              test_expected_module_list_complete]
    n_pass = n_fail = 0
    for t in tests:
        try:
            t()
            n_pass += 1
        except AssertionError as e:
            print(f"  {t.__name__} FAIL: {e}")
            n_fail += 1
        except Exception as e:
            print(f"  {t.__name__} ERROR: {type(e).__name__}: {e}")
            n_fail += 1
    print()
    print(f"RESULT: {n_pass}/{len(tests)} tests passed")
    return n_fail == 0


if __name__ == "__main__":
    sys.exit(0 if run_all() else 1)
