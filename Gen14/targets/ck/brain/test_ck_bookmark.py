"""test_ck_bookmark.py -- regression tests for the bookmark module."""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))

from ck_bookmark import Bookmark, Bookmarks, _extract_domain, _is_url  # noqa: E402


def _fresh() -> Bookmarks:
    tmp = Path(tempfile.gettempdir()) / f"ck_bm_test_{id(object())}.jsonl"
    if tmp.exists(): tmp.unlink()
    return Bookmarks(path=tmp)


def test_empty_stats():
    b = _fresh()
    try:
        s = b.stats()
        assert s["n_items"] == 0
    finally:
        b.clear()
    print("T1 PASS: empty bookmarks stats")


def test_add_full_url():
    b = _fresh()
    try:
        bm = b.add("https://github.com/TiredofSleep/ck",
                     title="CK repo", tags=["code"], note="main")
        assert isinstance(bm, Bookmark)
        assert bm.domain == "github.com"
        assert bm.title == "CK repo"
        assert bm.tags == ["code"]
        assert bm.note == "main"
        assert 0 <= bm.dominant_op <= 9
    finally:
        b.clear()
    print("T2 PASS: add(full https URL) populates all fields")


def test_add_bare_domain():
    b = _fresh()
    try:
        bm = b.add("arxiv.org/abs/2202.11826", title="paper")
        assert bm.url.startswith("arxiv.org")
        # _extract_domain handles bare domains via path-split fallback
        assert "arxiv" in bm.domain
    finally:
        b.clear()
    print("T3 PASS: add(bare-domain) accepted")


def test_reject_empty_url():
    b = _fresh()
    try:
        try:
            b.add("")
            assert False, "should have raised"
        except ValueError: pass
        try:
            b.add("   ")
            assert False, "should have raised"
        except ValueError: pass
    finally:
        b.clear()
    print("T4 PASS: empty/whitespace URL rejected")


def test_reject_garbage():
    b = _fresh()
    try:
        try:
            b.add("not a url at all")
            assert False, "should have raised"
        except ValueError: pass
    finally:
        b.clear()
    print("T5 PASS: garbage non-URL rejected")


def test_recent_chronological():
    b = _fresh()
    try:
        b.add("a.com")
        b.add("b.com")
        b.add("c.com")
        recent = b.recent(2)
        assert len(recent) == 2
        assert recent[0].url == "c.com"
        assert recent[1].url == "b.com"
    finally:
        b.clear()
    print("T6 PASS: recent(n) is reverse-chronological")


def test_search_by_url_title_tag():
    b = _fresh()
    try:
        b.add("https://github.com/A/ck", title="CK repo", tags=["code"])
        b.add("https://github.com/B/tig", title="TIG repo", tags=["math"])
        b.add("https://python.org/", title="Python", tags=["lang"])
        # Search "github" should hit two
        hits = b.search("github")
        assert len(hits) == 2
        # Search "math" should hit one (tag match)
        hits = b.search("math")
        assert len(hits) == 1
        # Search "lang" hits one
        hits = b.search("lang")
        assert len(hits) == 1
    finally:
        b.clear()
    print("T7 PASS: search matches url + title + tags")


def test_by_domain():
    b = _fresh()
    try:
        b.add("https://github.com/A/x")
        b.add("https://github.com/B/y")
        b.add("https://python.org/z")
        hits = b.by_domain("github.com")
        assert len(hits) == 2
        hits = b.by_domain("python.org")
        assert len(hits) == 1
        # www. prefix tolerated
        hits = b.by_domain("www.github.com")
        assert len(hits) == 2
    finally:
        b.clear()
    print("T8 PASS: by_domain filters + tolerates www.")


def test_persistence():
    tmp = Path(tempfile.gettempdir()) / "ck_bm_persist.jsonl"
    if tmp.exists(): tmp.unlink()
    try:
        b1 = Bookmarks(path=tmp)
        b1.add("https://example.com/a", title="A")
        b1.add("https://example.com/b", title="B")
        n1 = len(b1._items)
        b2 = Bookmarks(path=tmp)
        assert len(b2._items) == n1
        assert b2._items[0].url == "https://example.com/a"
    finally:
        if tmp.exists(): tmp.unlink()
    print(f"T9 PASS: persistence works ({n1} items reloaded)")


def test_extract_domain_helpers():
    assert _extract_domain("https://github.com/x") == "github.com"
    assert _extract_domain("https://www.github.com/x") == "github.com"
    assert _extract_domain("http://example.com:8080/y") == "example.com:8080"
    assert _extract_domain("arxiv.org/abs/123") == "arxiv.org"
    assert _extract_domain("") == ""
    print("T10 PASS: _extract_domain handles common URL shapes + bare domains")


def test_is_url_helper():
    assert _is_url("https://github.com/x")
    assert _is_url("http://example.com")
    assert _is_url("ftp://files.example.com/")
    assert _is_url("example.com/foo")
    assert not _is_url("")
    assert not _is_url("just some words")
    assert not _is_url("/local/path/no/domain")
    print("T11 PASS: _is_url permissive but rejects garbage")


def test_stats_full():
    b = _fresh()
    try:
        b.add("https://github.com/A", tags=["code"])
        b.add("https://github.com/B", tags=["code"])
        b.add("https://python.org/", tags=["lang"])
        s = b.stats()
        assert s["n_items"] == 3
        assert s["top_domains"].get("github.com") == 2
        assert s["top_tags"].get("code") == 2
    finally:
        b.clear()
    print("T12 PASS: stats reports domains + tags + ops correctly")


def run_all():
    print("=" * 64)
    print("ck_bookmark regression tests")
    print("=" * 64)
    print()
    tests = [test_empty_stats, test_add_full_url, test_add_bare_domain,
              test_reject_empty_url, test_reject_garbage, test_recent_chronological,
              test_search_by_url_title_tag, test_by_domain, test_persistence,
              test_extract_domain_helpers, test_is_url_helper, test_stats_full]
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
