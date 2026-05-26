"""test_ck_pc_recommend.py -- regression tests for recommendation bridge.

What we test:
  T1 -- empty buffer returns no recommendations
  T2 -- short buffer returns no recommendations (insufficient evidence)
  T3 -- SUSTAINED_HIGH_CPU fires when one process pegged for 35s
  T4 -- MEMORY_PRESSURE fires above 80% sustained
  T5 -- UNBALANCED_LOAD fires on high variance sustained
  T6 -- GREEN_WINDOW fires when all readings green for > 30s
  T7 -- MEMORY_LEAK_HINT fires on monotonic growth
  T8 -- IDLE_CONFIRMED fires on sustained VOID
  T9 -- PROCESS_STORM fires on +50 process jump
  T10 -- priority ordering: ALERT > WARN > NOTICE > INFO
  T11 -- all recommendations carry TIER_RECOMMENDATION_HEURISTIC tag
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))

from ck_pc_recommend import (  # noqa: E402
    ALERT,
    INFO,
    NOTICE,
    TIER_RECOMMENDATION_HEURISTIC,
    WARN,
    recommendations_for,
)
from ck_pc_sense import PCSenseReading  # noqa: E402


def _r(ts: float, op: int = 5, op_name: str = "BALANCE",
        coh: float = 0.6, band: str = "YELLOW",
        cpu: float = 0.10, cpu_var: float = 0.01,
        mem: float = 0.40, mem_gb: float = 16.0,
        n_proc: int = 200,
        top_cpu: list = None, top_mem: list = None) -> PCSenseReading:
    """Build a synthetic PCSenseReading for testing."""
    return PCSenseReading(
        ts=ts,
        cpu_overall=cpu,
        cpu_per_core=[cpu] * 8,
        cpu_variance=cpu_var,
        mem_used=mem,
        mem_available_gb=mem_gb,
        n_processes=n_proc,
        top_cpu_processes=top_cpu or [{"name": "idle", "pct": 0.5, "pid": 0}],
        top_mem_processes=top_mem or [{"name": "system", "pct_gb": 0.5, "pid": 4}],
        op=op,
        op_name=op_name,
        coherence=coh,
        coherence_band=band,
        notes=[],
    )


def test_empty_buffer():
    assert recommendations_for([]) == []
    print("T1 PASS: empty buffer returns no recommendations")


def test_short_buffer():
    buf = [_r(time.time())]
    recs = recommendations_for(buf)
    assert len(recs) == 0, f"short buffer should produce no recs; got {recs}"
    print("T2 PASS: short buffer (1 reading) returns no recommendations")


def test_sustained_high_cpu():
    """Build 40s of one process pegged at 95%."""
    t0 = time.time()
    buf = []
    for i in range(40):
        buf.append(_r(
            ts=t0 + i,
            cpu=0.95,
            cpu_var=0.01,
            top_cpu=[{"name": "runaway.exe", "pct": 95.0, "pid": 9001}],
        ))
    recs = recommendations_for(buf)
    codes = [r.code for r in recs]
    assert any("SUSTAINED_HIGH_CPU" in c for c in codes), (
        f"expected SUSTAINED_HIGH_CPU; got {codes}")
    matching = [r for r in recs if "SUSTAINED_HIGH_CPU" in r.code]
    assert any("runaway.exe" in r.text for r in matching), (
        f"recommendation should name the offending process; got {matching}")
    print(f"T3 PASS: SUSTAINED_HIGH_CPU fires on 40s @ 95% one process "
          f"({len(matching)} rec(s), priority={matching[0].priority})")


def test_memory_pressure():
    """40s of mem_used > 0.85."""
    t0 = time.time()
    buf = []
    for i in range(40):
        buf.append(_r(
            ts=t0 + i,
            mem=0.88, mem_gb=2.0,
            top_mem=[{"name": "hog.exe", "pct_gb": 12.0, "pid": 8888}],
        ))
    recs = recommendations_for(buf)
    codes = [r.code for r in recs]
    assert "MEMORY_PRESSURE" in codes, (
        f"expected MEMORY_PRESSURE; got {codes}")
    mp = [r for r in recs if r.code == "MEMORY_PRESSURE"][0]
    assert "hog.exe" in mp.text, "should name top mem process"
    print(f"T4 PASS: MEMORY_PRESSURE fires at 88% for 40s "
          f"(priority={mp.priority})")


def test_unbalanced_load():
    """40s of high variance."""
    t0 = time.time()
    buf = []
    for i in range(40):
        buf.append(_r(ts=t0 + i, cpu=0.20, cpu_var=0.18))
    recs = recommendations_for(buf)
    codes = [r.code for r in recs]
    assert "UNBALANCED_LOAD" in codes, (
        f"expected UNBALANCED_LOAD; got {codes}")
    print("T5 PASS: UNBALANCED_LOAD fires on sustained high variance")


def test_green_window():
    """40s of all-green readings."""
    t0 = time.time()
    buf = []
    for i in range(40):
        buf.append(_r(ts=t0 + i, coh=0.75, band="GREEN", op=7,
                       op_name="HARMONY"))
    recs = recommendations_for(buf)
    codes = [r.code for r in recs]
    assert "GREEN_WINDOW" in codes, f"expected GREEN_WINDOW; got {codes}"
    print("T6 PASS: GREEN_WINDOW fires on sustained all-green")


def test_memory_leak_hint():
    """One process growing monotonically over 70s."""
    t0 = time.time()
    buf = []
    for i in range(70):
        buf.append(_r(
            ts=t0 + i,
            top_mem=[{"name": "leaky.exe",
                       "pct_gb": 1.0 + (i * 0.05),  # 1.0 GB -> 4.45 GB
                       "pid": 7777}],
        ))
    recs = recommendations_for(buf)
    codes = [r.code for r in recs]
    assert "MEMORY_LEAK_HINT" in codes, (
        f"expected MEMORY_LEAK_HINT; got {codes}")
    ml = [r for r in recs if r.code == "MEMORY_LEAK_HINT"][0]
    assert "leaky.exe" in ml.text
    print(f"T7 PASS: MEMORY_LEAK_HINT fires on monotonic growth "
          f"(+{ml.evidence['growth_gb']:.2f} GB over "
          f"{ml.evidence['duration_sec']:.0f}s)")


def test_idle_confirmed():
    """40s of all VOID readings."""
    t0 = time.time()
    buf = []
    for i in range(40):
        buf.append(_r(ts=t0 + i, cpu=0.01, mem=0.10,
                       op=0, op_name="VOID"))
    recs = recommendations_for(buf)
    codes = [r.code for r in recs]
    assert "IDLE_CONFIRMED" in codes, (
        f"expected IDLE_CONFIRMED; got {codes}")
    print("T8 PASS: IDLE_CONFIRMED fires on sustained VOID")


def test_process_storm():
    """One reading with +60 processes vs previous."""
    t0 = time.time()
    buf = [_r(ts=t0, n_proc=200),
           _r(ts=t0 + 1, n_proc=265)]
    recs = recommendations_for(buf)
    codes = [r.code for r in recs]
    assert "PROCESS_STORM" in codes, (
        f"expected PROCESS_STORM; got {codes}")
    ps = [r for r in recs if r.code == "PROCESS_STORM"][0]
    assert ps.evidence["delta"] == 65
    print("T9 PASS: PROCESS_STORM fires on +65 process jump")


def test_priority_ordering():
    """If we trigger multiple, output should be sorted ALERT > WARN > NOTICE > INFO."""
    t0 = time.time()
    # Build a buffer that triggers MEMORY_PRESSURE (WARN/ALERT) +
    # GREEN_WINDOW (INFO) — wait, those are mutually exclusive (green
    # implies low mem). Use MEMORY_PRESSURE + UNBALANCED_LOAD instead.
    buf = []
    for i in range(40):
        buf.append(_r(
            ts=t0 + i,
            mem=0.88, mem_gb=2.0,
            cpu=0.20, cpu_var=0.18,
            top_mem=[{"name": "ram_hog.exe", "pct_gb": 12.0, "pid": 8}],
        ))
    recs = recommendations_for(buf)
    assert len(recs) >= 2
    priority_order = {ALERT: 0, WARN: 1, NOTICE: 2, INFO: 3}
    pvals = [priority_order[r.priority] for r in recs]
    assert pvals == sorted(pvals), (
        f"recommendations not sorted by priority: {[(r.priority, r.code) for r in recs]}")
    print(f"T10 PASS: priority ordering preserved across "
          f"{len(recs)} recommendations: "
          f"{[r.priority for r in recs]}")


def test_all_carry_heuristic_tier():
    """Every recommendation, regardless of detector, must be tagged HEURISTIC."""
    t0 = time.time()
    buf = []
    for i in range(40):
        buf.append(_r(
            ts=t0 + i,
            mem=0.88, mem_gb=2.0,
            cpu=0.95, cpu_var=0.20,
            top_cpu=[{"name": "all_the_things.exe", "pct": 95.0, "pid": 1}],
            top_mem=[{"name": "ram_hog.exe", "pct_gb": 12.0, "pid": 2}],
        ))
    recs = recommendations_for(buf)
    assert len(recs) >= 1
    for r in recs:
        assert r.tier == TIER_RECOMMENDATION_HEURISTIC, (
            f"recommendation {r.code} has wrong tier: {r.tier}")
    print(f"T11 PASS: all {len(recs)} recommendations carry "
          f"TIER_RECOMMENDATION_HEURISTIC")


def run_all():
    print("=" * 64)
    print("ck_pc_recommend regression tests")
    print("=" * 64)
    print()
    tests = [
        test_empty_buffer,
        test_short_buffer,
        test_sustained_high_cpu,
        test_memory_pressure,
        test_unbalanced_load,
        test_green_window,
        test_memory_leak_hint,
        test_idle_confirmed,
        test_process_storm,
        test_priority_ordering,
        test_all_carry_heuristic_tier,
    ]
    n_pass = 0
    n_fail = 0
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
    print("=" * 64)
    print(f"RESULT: {n_pass}/{len(tests)} tests passed")
    print("=" * 64)
    return n_fail == 0


if __name__ == "__main__":
    ok = run_all()
    sys.exit(0 if ok else 1)
