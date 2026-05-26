"""test_ck_journal.py -- regression tests for the journal module."""
from __future__ import annotations

import json
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))

from ck_journal import (  # noqa: E402
    OP_NAMES,
    Journal,
    JournalEntry,
    _compute_signature,
)


def _fresh_journal() -> Journal:
    tmp = Path(tempfile.gettempdir()) / f"ck_j_test_{id(object())}.jsonl"
    if tmp.exists():
        tmp.unlink()
    return Journal(path=tmp)


def test_empty_journal_stats():
    j = _fresh_journal()
    try:
        s = j.stats()
        assert s["n_entries"] == 0
    finally:
        j.clear()
    print("T1 PASS: empty journal stats correct")


def test_note_writes_entry():
    j = _fresh_journal()
    try:
        e = j.note("hello world", tags=["smoke"], mood="curious")
        assert isinstance(e, JournalEntry)
        assert e.text == "hello world"
        assert e.tags == ["smoke"]
        assert e.mood == "curious"
        assert 0 <= e.dominant_op <= 9
        assert e.dominant_op_name in OP_NAMES
        assert e.operator_path  # non-empty
        assert e.signature_hash  # non-empty hex
    finally:
        j.clear()
    print("T2 PASS: note() returns properly populated JournalEntry")


def test_empty_text_rejected():
    j = _fresh_journal()
    try:
        try:
            j.note("")
            assert False, "should have raised"
        except ValueError:
            pass
        try:
            j.note("   ")
            assert False, "should have raised on whitespace-only"
        except ValueError:
            pass
    finally:
        j.clear()
    print("T3 PASS: empty/whitespace text rejected with ValueError")


def test_persistence():
    tmp = Path(tempfile.gettempdir()) / f"ck_j_persist_{id(object())}.jsonl"
    if tmp.exists():
        tmp.unlink()
    try:
        j1 = Journal(path=tmp)
        j1.note("first note", tags=["a"], mood="ok")
        j1.note("second note", tags=["b"])
        n1 = len(j1._entries)
        # reload
        j2 = Journal(path=tmp)
        assert len(j2._entries) == n1
        assert j2._entries[0].text == "first note"
        assert j2._entries[1].text == "second note"
    finally:
        if tmp.exists():
            tmp.unlink()
    print(f"T4 PASS: persistence works ({n1} entries reloaded)")


def test_recent_chronological():
    j = _fresh_journal()
    try:
        j.note("a")
        time.sleep(0.01)
        j.note("b")
        time.sleep(0.01)
        j.note("c")
        recent = j.recent(2)
        assert len(recent) == 2
        # Reverse-chronological: c, b
        assert recent[0].text == "c"
        assert recent[1].text == "b"
    finally:
        j.clear()
    print("T5 PASS: recent(n) returns reverse-chronological top-N")


def test_today_filter():
    j = _fresh_journal()
    try:
        j.note("today note")
        today_entries = j.today()
        assert len(today_entries) >= 1
        assert all(e.text == "today note" or True for e in today_entries)
        # Inject a synthetic past entry by direct buffer manipulation
        # (NB: bypasses _append, only for testing)
        past = JournalEntry(
            ts=time.time() - (3 * 86400),  # 3 days ago
            iso="2026-05-16T00:00:00",
            text="three days ago",
            operator_path=[1, 2, 3], dominant_op=1, dominant_op_name="LATTICE",
            signature_hash="abc",
        )
        j._entries.insert(0, past)
        today_entries_2 = j.today()
        # The past entry should NOT appear in today's list
        assert all(e.text != "three days ago" for e in today_entries_2)
    finally:
        j.clear()
    print("T6 PASS: today() filters to today only")


def test_by_dominant_op():
    j = _fresh_journal()
    try:
        # Build entries with known dominant ops by content
        for i in range(5):
            j.note(f"entry {i}")
        # Pick the dominant op of the first entry
        target_op = j._entries[0].dominant_op
        hits = j.by_dominant_op(target_op)
        assert len(hits) >= 1
        for h in hits:
            assert h.dominant_op == target_op
        # Out-of-range op returns empty
        assert j.by_dominant_op(99) == []
        assert j.by_dominant_op(-1) == []
    finally:
        j.clear()
    print("T7 PASS: by_dominant_op filters correctly")


def test_search_text():
    j = _fresh_journal()
    try:
        j.note("learning Python today", tags=["learning"], mood="curious")
        j.note("teaching Python to a friend", tags=["teaching"])
        j.note("watching the rain", tags=["personal"], mood="calm")
        hits = j.search("python", n=5)
        assert len(hits) >= 2
        # All hits should contain 'python' in text or tags
        for h in hits:
            assert "python" in h["text"].lower() or \
                    any("python" in t.lower() for t in h["tags"])
        # Score sorted
        scores = [h["_score"] for h in hits]
        assert scores == sorted(scores, reverse=True)
    finally:
        j.clear()
    print("T8 PASS: search by text returns ranked hits")


def test_search_mood():
    j = _fresh_journal()
    try:
        j.note("a", mood="frustrated")
        j.note("b", mood="happy")
        j.note("c", mood="frustrated")
        hits = j.search("frustrated", n=5)
        assert len(hits) >= 2
        for h in hits:
            assert h["mood"] == "frustrated"
    finally:
        j.clear()
    print("T9 PASS: search by mood works")


def test_stats_full():
    j = _fresh_journal()
    try:
        j.note("a long note about coding", tags=["dev"], mood="focused")
        j.note("a short note", tags=["dev"], mood="quick")
        j.note("personal stuff", tags=["personal"])
        s = j.stats()
        assert s["n_entries"] == 3
        assert "total_chars" in s
        assert s["total_chars"] > 0
        assert "dominant_op_distribution" in s
        assert "top_moods" in s
        assert "top_tags" in s
        assert s["top_tags"].get("dev", 0) == 2
    finally:
        j.clear()
    print("T10 PASS: stats has correct counts and distributions")


def test_signature_deterministic():
    a = _compute_signature("hello world")
    b = _compute_signature("hello world")
    assert a == b, "signature must be deterministic"
    c = _compute_signature("HELLO WORLD")
    assert a != c, "signature should be case-sensitive (byte-mod-10)"
    print("T11 PASS: _compute_signature is deterministic + case-sensitive")


def test_signature_empty_text():
    s = _compute_signature("")
    assert s["operator_path"] == []
    assert s["dominant_op"] == 0
    assert s["dominant_op_name"] == "VOID"
    print("T12 PASS: empty text -> empty signature (VOID)")


def run_all():
    print("=" * 64)
    print("ck_journal regression tests")
    print("=" * 64)
    print()
    tests = [
        test_empty_journal_stats,
        test_note_writes_entry,
        test_empty_text_rejected,
        test_persistence,
        test_recent_chronological,
        test_today_filter,
        test_by_dominant_op,
        test_search_text,
        test_search_mood,
        test_stats_full,
        test_signature_deterministic,
        test_signature_empty_text,
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
