"""test_ck_reminder.py -- regression tests for the reminder module."""
from __future__ import annotations

import sys
import tempfile
import time
from datetime import datetime, timedelta
from pathlib import Path

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))

from ck_reminder import Reminder, Reminders, parse_when  # noqa: E402


def _fresh() -> Reminders:
    tmp = Path(tempfile.gettempdir()) / f"ck_rem_test_{id(object())}.jsonl"
    if tmp.exists(): tmp.unlink()
    return Reminders(path=tmp)


def test_parse_when_epoch():
    assert parse_when(1779820800.0) == 1779820800.0
    assert parse_when(1779820800) == 1779820800.0
    print("T1 PASS: parse_when accepts epoch float/int")


def test_parse_when_iso():
    ts = parse_when("2026-05-19T14:30:00")
    dt = datetime.fromtimestamp(ts)
    assert dt.year == 2026
    assert dt.month == 5
    assert dt.day == 19
    assert dt.hour == 14
    assert dt.minute == 30
    print("T2 PASS: parse_when handles ISO datetime")


def test_parse_when_relative():
    now = time.time()
    # 30m -> +1800s
    t = parse_when("30m", now=now)
    assert abs((t - now) - 1800) < 1
    # 2h -> +7200s
    t = parse_when("2h", now=now)
    assert abs((t - now) - 7200) < 1
    # 1h30m -> 5400s
    t = parse_when("1h30m", now=now)
    assert abs((t - now) - 5400) < 1
    # 45s -> 45s
    t = parse_when("45s", now=now)
    assert abs((t - now) - 45) < 1
    # 1d4h -> 100800s
    t = parse_when("1d4h", now=now)
    assert abs((t - now) - 100800) < 1
    print("T3 PASS: parse_when handles 30m / 2h / 1h30m / 45s / 1d4h")


def test_parse_when_natural():
    # "tomorrow at 9am"
    ts = parse_when("tomorrow at 9am")
    dt = datetime.fromtimestamp(ts)
    expected = datetime.now() + timedelta(days=1)
    assert dt.day == expected.day
    assert dt.hour == 9
    assert dt.minute == 0
    # "tonight at 8pm"
    ts = parse_when("tonight at 8pm")
    dt = datetime.fromtimestamp(ts)
    assert dt.hour == 20
    # "today at 5pm"
    ts = parse_when("today at 5pm")
    dt = datetime.fromtimestamp(ts)
    assert dt.hour == 17
    print("T4 PASS: parse_when handles 'tomorrow/tonight/today at H[am|pm]'")


def test_parse_when_garbage_raises():
    for w in ("", "   ", "not a time", "0m", None):
        try:
            parse_when(w)
            raise AssertionError(f"should have raised for {w!r}")
        except (ValueError, TypeError):
            pass
    print("T5 PASS: parse_when raises on empty/garbage/None")


def test_add_basic():
    r = _fresh()
    try:
        rem = r.add("check the dryer", "5m", tags=["drycleaners"])
        assert isinstance(rem, Reminder)
        assert rem.text == "check the dryer"
        assert rem.tags == ["drycleaners"]
        assert not rem.acknowledged
        # due in roughly 5 min
        assert 290 <= (rem.due_ts - time.time()) <= 310
        # has an id
        assert rem.id and len(rem.id) == 12
    finally:
        r.clear()
    print("T6 PASS: add() returns properly populated Reminder")


def test_add_empty_text_raises():
    r = _fresh()
    try:
        for txt in ("", "   ", None):
            try:
                r.add(txt, "5m")
                raise AssertionError("should have raised")
            except (ValueError, TypeError):
                pass
    finally:
        r.clear()
    print("T7 PASS: empty/None text rejected")


def test_due_pending_split():
    r = _fresh()
    try:
        # one already in the past, one future
        r.add("past one", time.time() - 100)
        r.add("future one", "30m")
        due = r.due()
        pending = r.pending()
        assert len(due) == 1
        assert due[0].text == "past one"
        assert len(pending) == 1
        assert pending[0].text == "future one"
    finally:
        r.clear()
    print("T8 PASS: due() vs pending() split by due_ts")


def test_acknowledge():
    r = _fresh()
    try:
        rem = r.add("ack me", time.time() - 10)  # already due
        assert len(r.due()) == 1
        result = r.acknowledge(rem.id)
        assert result is not None
        assert result.acknowledged
        assert result.ack_ts is not None
        # now no longer in due()
        assert len(r.due()) == 0
        assert len(r.all_active()) == 0
        # invalid id returns None
        assert r.acknowledge("nonexistent_id") is None
    finally:
        r.clear()
    print("T9 PASS: acknowledge() removes from due(); invalid id returns None")


def test_persistence():
    tmp = Path(tempfile.gettempdir()) / "ck_rem_persist.jsonl"
    if tmp.exists(): tmp.unlink()
    try:
        r1 = Reminders(path=tmp)
        rem = r1.add("persist me", "1h", tags=["test"])
        n1 = len(r1._items)
        r2 = Reminders(path=tmp)
        assert len(r2._items) == n1
        assert r2._items[0].text == "persist me"
        # Acknowledge in r1, verify state propagates on r3 reload
        r1.acknowledge(rem.id)
        r3 = Reminders(path=tmp)
        assert any(x.acknowledged for x in r3._items)
    finally:
        if tmp.exists(): tmp.unlink()
    print("T10 PASS: persistence + ack state survives reload")


def test_recent_chronological():
    r = _fresh()
    try:
        for i in range(5):
            r.add(f"note {i}", f"{i+10}m")
            time.sleep(0.01)
        recent = r.recent(3)
        assert len(recent) == 3
        # Most recent first by created_ts (last added)
        assert recent[0].text == "note 4"
        assert recent[1].text == "note 3"
        assert recent[2].text == "note 2"
    finally:
        r.clear()
    print("T11 PASS: recent(n) returns by created_ts reverse-chronologically")


def test_stats():
    r = _fresh()
    try:
        r.add("past", time.time() - 100)
        r.add("future a", "10m")
        r.add("future b", "20m")
        s = r.stats()
        assert s["n_total"] == 3
        assert s["n_active"] == 3
        assert s["n_due_now"] == 1
        assert s["n_pending"] == 2
        assert s["n_acknowledged"] == 0
    finally:
        r.clear()
    print("T12 PASS: stats reports correct counts")


def run_all():
    print("=" * 64)
    print("ck_reminder regression tests")
    print("=" * 64)
    print()
    tests = [test_parse_when_epoch, test_parse_when_iso,
              test_parse_when_relative, test_parse_when_natural,
              test_parse_when_garbage_raises, test_add_basic,
              test_add_empty_text_raises, test_due_pending_split,
              test_acknowledge, test_persistence,
              test_recent_chronological, test_stats]
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
