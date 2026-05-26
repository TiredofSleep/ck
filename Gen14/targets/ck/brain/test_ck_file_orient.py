"""test_ck_file_orient.py -- regression tests for the file orientation index.

What we test:
  T1 -- empty index reports n_files=0
  T2 -- scan_directory on a missing path returns ok=False
  T3 -- scan_directory on a file (not dir) returns ok=False
  T4 -- scan_directory on a small temp tree indexes everything expected
  T5 -- find_by_query matches the obvious filename keyword
  T6 -- find_by_query returns multiple results ranked by score
  T7 -- find_by_signature returns results from the seed
  T8 -- incremental scan skips unchanged files
  T9 -- persistence: scan + reload finds the same entries
  T10 -- _should_skip filters .git, node_modules, __pycache__
  T11 -- signature is bounded I/O (does NOT read full content)
  T12 -- clear() empties index and removes the file
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))

from ck_file_orient import (  # noqa: E402
    DEFAULT_IGNORES,
    FileEntry,
    FileOrientIndex,
    _operator_path_from_bytes,
    _should_skip,
    _signature_for_file,
)


def _make_test_tree(root: Path) -> int:
    """Build a deterministic small tree and return n_files we created."""
    root.mkdir(parents=True, exist_ok=True)
    # 5 normal files
    (root / "notes.md").write_text("# Project notes\nhello", encoding="utf-8")
    (root / "config.json").write_text(json.dumps({"key": "value"}),
                                         encoding="utf-8")
    (root / "data.csv").write_text("a,b,c\n1,2,3\n4,5,6", encoding="utf-8")
    (root / "main.py").write_text("def hello():\n    return 'world'\n",
                                     encoding="utf-8")
    # Nested subdirectory
    sub = root / "subdir"
    sub.mkdir(exist_ok=True)
    (sub / "deep_notes.md").write_text("nested", encoding="utf-8")
    # An ignored directory (should be skipped)
    git = root / ".git"
    git.mkdir(exist_ok=True)
    (git / "config").write_text("git config", encoding="utf-8")
    return 5  # not counting .git/config


def test_empty_index():
    with tempfile.TemporaryDirectory() as td:
        idx_path = Path(td) / "empty.jsonl"
        # NB: pass ignores={'.git'} only (not the full DEFAULT_IGNORES),
        # because on Windows tempfile.TemporaryDirectory() returns paths
        # under AppData/Local/Temp/, and `AppData` is in DEFAULT_IGNORES.
        # Production callers use DEFAULT_IGNORES; tests use a minimal set
        # to keep the temp dir scannable.
        idx = FileOrientIndex(index_path=idx_path, ignores=frozenset({'.git'}))
        s = idx.stats()
        assert s["n_files"] == 0
        assert s["total_gb"] == 0
    print("T1 PASS: empty index reports n_files=0")


def test_missing_root():
    with tempfile.TemporaryDirectory() as td:
        idx_path = Path(td) / "idx.jsonl"
        # NB: pass ignores={'.git'} only (not the full DEFAULT_IGNORES),
        # because on Windows tempfile.TemporaryDirectory() returns paths
        # under AppData/Local/Temp/, and `AppData` is in DEFAULT_IGNORES.
        # Production callers use DEFAULT_IGNORES; tests use a minimal set
        # to keep the temp dir scannable.
        idx = FileOrientIndex(index_path=idx_path, ignores=frozenset({'.git'}))
        result = idx.scan_directory(Path("/nonexistent/path/xyz"))
        assert result["ok"] is False
        assert "does not exist" in result["error"]
    print("T2 PASS: scan_directory on missing path returns ok=False")


def test_root_is_file():
    with tempfile.TemporaryDirectory() as td:
        idx_path = Path(td) / "idx.jsonl"
        a_file = Path(td) / "afile.txt"
        a_file.write_text("hi")
        # NB: pass ignores={'.git'} only (not the full DEFAULT_IGNORES),
        # because on Windows tempfile.TemporaryDirectory() returns paths
        # under AppData/Local/Temp/, and `AppData` is in DEFAULT_IGNORES.
        # Production callers use DEFAULT_IGNORES; tests use a minimal set
        # to keep the temp dir scannable.
        idx = FileOrientIndex(index_path=idx_path, ignores=frozenset({'.git'}))
        result = idx.scan_directory(a_file)
        assert result["ok"] is False
        assert "not a directory" in result["error"]
    print("T3 PASS: scan_directory on a file returns ok=False")


def test_scan_small_tree():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / "tree"
        n_expected = _make_test_tree(root)
        idx_path = Path(td) / "idx.jsonl"
        # NB: pass ignores={'.git'} only (not the full DEFAULT_IGNORES),
        # because on Windows tempfile.TemporaryDirectory() returns paths
        # under AppData/Local/Temp/, and `AppData` is in DEFAULT_IGNORES.
        # Production callers use DEFAULT_IGNORES; tests use a minimal set
        # to keep the temp dir scannable.
        idx = FileOrientIndex(index_path=idx_path, ignores=frozenset({'.git'}))
        result = idx.scan_directory(root)
        assert result["ok"] is True
        assert result["n_scanned"] == n_expected, (
            f"expected {n_expected} files, scanned {result['n_scanned']}")
        # .git should be skipped (it's a default ignore)
        names = [e.name for e in idx._entries.values()]
        assert "config" not in names or all(
            ".git" not in e.path for e in idx._entries.values()
            if e.name == "config"
        ), "git config should be skipped"
    print(f"T4 PASS: scanned {n_expected} files in small tree (ignored .git)")


def test_find_by_query_basic():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / "tree"
        _make_test_tree(root)
        # NB: minimal ignores so Windows AppData/Local/Temp scans work.
        idx = FileOrientIndex(index_path=Path(td) / "idx.jsonl",
                                ignores=frozenset({'.git'}))
        idx.scan_directory(root)
        hits = idx.find_by_query("notes", n=5)
        assert len(hits) >= 1
        assert any("notes" in h["name"].lower() for h in hits)
    print("T5 PASS: find_by_query('notes') hits notes.md")


def test_find_by_query_ranking():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / "tree"
        _make_test_tree(root)
        # NB: minimal ignores so Windows AppData/Local/Temp scans work.
        idx = FileOrientIndex(index_path=Path(td) / "idx.jsonl",
                                ignores=frozenset({'.git'}))
        idx.scan_directory(root)
        # Query that matches multiple
        hits = idx.find_by_query("notes md", n=10)
        assert len(hits) >= 2  # notes.md + deep_notes.md
        # Scores should be monotonically non-increasing
        scores = [h["_score"] for h in hits]
        assert scores == sorted(scores, reverse=True), (
            f"scores not sorted descending: {scores}")
    print(f"T6 PASS: find_by_query returns ranked results "
          f"(scores monotonically non-increasing)")


def test_find_by_signature():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / "tree"
        _make_test_tree(root)
        # NB: minimal ignores so Windows AppData/Local/Temp scans work.
        idx = FileOrientIndex(index_path=Path(td) / "idx.jsonl",
                                ignores=frozenset({'.git'}))
        idx.scan_directory(root)
        # Pick one file as seed
        all_paths = list(idx._entries.keys())
        assert len(all_paths) >= 2
        seed = all_paths[0]
        similar = idx.find_by_signature(seed, n=5)
        # Even random files might have some overlap by chance, so we
        # just verify the API works and never returns the seed itself
        assert all(s["path"] != seed for s in similar)
    print(f"T7 PASS: find_by_signature returns results "
          f"(seed file excluded from results)")


def test_incremental_scan():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / "tree"
        _make_test_tree(root)
        # NB: minimal ignores so Windows AppData/Local/Temp scans work.
        idx = FileOrientIndex(index_path=Path(td) / "idx.jsonl",
                                ignores=frozenset({'.git'}))
        # First scan
        r1 = idx.scan_directory(root)
        assert r1["n_new"] >= 1
        # Second scan immediately — should mostly skip unchanged
        r2 = idx.scan_directory(root)
        assert r2["n_skipped_unchanged"] >= 1, (
            f"second scan should skip unchanged files; got {r2}")
        # Modify one file. NB: Windows NTFS mtime resolution is ~1s,
        # so sleep 1.1s before writing to guarantee a detectable delta.
        time.sleep(1.1)
        (root / "notes.md").write_text("# Updated", encoding="utf-8")
        r3 = idx.scan_directory(root)
        assert r3["n_updated"] >= 1, (
            f"third scan should detect updated file; got {r3}")
    print("T8 PASS: incremental scan skips unchanged + detects updated")


def test_persistence():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / "tree"
        _make_test_tree(root)
        idx_path = Path(td) / "idx.jsonl"
        idx1 = FileOrientIndex(index_path=idx_path,
                                  ignores=frozenset({'.git'}))
        idx1.scan_directory(root)
        n1 = len(idx1._entries)
        # Create a new index instance; should load from disk
        idx2 = FileOrientIndex(index_path=idx_path,
                                  ignores=frozenset({'.git'}))
        n2 = len(idx2._entries)
        assert n1 == n2, f"persistence broke: {n1} -> {n2}"
        # Spot-check one entry
        sample = next(iter(idx1._entries.values()))
        assert sample.path in idx2._entries
        assert idx2._entries[sample.path].op_path == sample.op_path
    print(f"T9 PASS: persistence works ({n1} entries reloaded "
          f"identically from disk)")


def test_should_skip_ignores():
    # Default ignores include .git, node_modules, __pycache__
    assert _should_skip(Path("/tmp/x/.git/config"), DEFAULT_IGNORES)
    assert _should_skip(Path("/tmp/x/node_modules/pkg.json"), DEFAULT_IGNORES)
    assert _should_skip(Path("/tmp/x/__pycache__/file.pyc"), DEFAULT_IGNORES)
    assert _should_skip(Path("/tmp/x/.venv/python"), DEFAULT_IGNORES)
    # Dot-files anywhere skipped
    assert _should_skip(Path("/tmp/x/.hidden"), DEFAULT_IGNORES)
    # Normal paths NOT skipped
    assert not _should_skip(Path("/tmp/x/notes.md"), DEFAULT_IGNORES)
    assert not _should_skip(Path("/tmp/x/src/main.py"), DEFAULT_IGNORES)
    print("T10 PASS: _should_skip correctly filters defaults + dot-files")


def test_bounded_io():
    """Signature reads at most 128 bytes per file (head 64 + tail 64)."""
    with tempfile.TemporaryDirectory() as td:
        # Make a 5 MB file
        big = Path(td) / "big.bin"
        with open(big, "wb") as f:
            f.write(b"X" * (5 * 1024 * 1024))
        # Compute signature; should be fast and use bounded I/O
        t0 = time.time()
        op_path, size, mtime = _signature_for_file(big)
        elapsed = time.time() - t0
        assert size == 5 * 1024 * 1024
        assert len(op_path) == 8
        # Should be very fast — bounded I/O — even for a 5 MB file
        assert elapsed < 0.5, f"too slow ({elapsed:.3f}s); likely reading whole file"
    print(f"T11 PASS: signature is bounded I/O "
          f"(5 MB file in {elapsed*1000:.1f}ms)")


def test_clear():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / "tree"
        _make_test_tree(root)
        idx_path = Path(td) / "idx.jsonl"
        # NB: pass ignores={'.git'} only (not the full DEFAULT_IGNORES),
        # because on Windows tempfile.TemporaryDirectory() returns paths
        # under AppData/Local/Temp/, and `AppData` is in DEFAULT_IGNORES.
        # Production callers use DEFAULT_IGNORES; tests use a minimal set
        # to keep the temp dir scannable.
        idx = FileOrientIndex(index_path=idx_path, ignores=frozenset({'.git'}))
        idx.scan_directory(root)
        assert len(idx._entries) > 0
        assert idx_path.exists()
        idx.clear()
        assert len(idx._entries) == 0
        assert not idx_path.exists()
    print("T12 PASS: clear() empties index + removes file")


def run_all():
    print("=" * 64)
    print("ck_file_orient regression tests")
    print("=" * 64)
    print()
    tests = [
        test_empty_index,
        test_missing_root,
        test_root_is_file,
        test_scan_small_tree,
        test_find_by_query_basic,
        test_find_by_query_ranking,
        test_find_by_signature,
        test_incremental_scan,
        test_persistence,
        test_should_skip_ignores,
        test_bounded_io,
        test_clear,
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
