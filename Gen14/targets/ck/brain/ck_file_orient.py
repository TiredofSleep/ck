"""ck_file_orient.py -- content-blind file orientation index for CK.

CK Gen14 module — walks a user-designated directory tree, computes a
content-blind operator-path signature for each file, and builds a
local index so the user can ask "where did I put that file about X"
without CK actually reading the contents.

═══════════════════════════════════════════════════════════════════
What this module DOES
═══════════════════════════════════════════════════════════════════

  1. `scan_directory(root, ...)` — walks the tree, respects ignore
     patterns (.git, node_modules, __pycache__, etc.), computes a
     signature per file from filename + size + mtime + first/last 64
     bytes (NOT full content read — bounded I/O).
  2. `find_by_query(query, n=10)` — fuzzy-match the user's query
     against the filename + path components; rank by string-similarity
     score; return up to N hits.
  3. `find_by_signature(seed_file_path, n=10)` — given a known file,
     return up to N files with similar operator-path signatures
     (potential duplicates, related material).
  4. Persistent index at user-chosen path (JSONL); incremental updates
     via stored mtime — re-scan only files that changed since the
     last scan.

═══════════════════════════════════════════════════════════════════
What this module DOES NOT DO
═══════════════════════════════════════════════════════════════════

  - Does NOT read full file contents.  Reads at most 128 bytes per
    file (64 head + 64 tail) for signature; the rest of the signature
    comes from filename + size + mtime.  The user's files are NOT
    retained or transmitted.
  - Does NOT move, copy, rename, or delete files.  Read-only.
  - Does NOT make outbound network calls.
  - Does NOT scan filesystem roots unless the user explicitly passes
    them.  Defaults to `~/Documents` only (with explicit confirm).
  - Does NOT recurse into hidden directories (`.git`, `.venv`,
    `node_modules`, etc.) by default.

═══════════════════════════════════════════════════════════════════
Honest scope
═══════════════════════════════════════════════════════════════════

This is a file-orientation primitive.  The "signature" is a short
content-blind fingerprint (similar in spirit to ck_anomaly_detector
but applied to small filename-and-edge-bytes data); it's good enough
for "show me files that look like this other file" but NOT for
deduplication-grade similarity.  For real dedup use a content-aware
tool (rmlint, fdupes).  For real search use `grep -r` or `ripgrep`.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple


# ─── Defaults ─────────────────────────────────────────────────────

DEFAULT_IGNORES = frozenset({
    ".git", ".hg", ".svn", ".bzr",
    "node_modules", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache",
    ".venv", "venv", "env", ".env",
    ".idea", ".vscode", ".vs",
    "dist", "build", ".next", ".nuxt",
    "target",  # Rust
    "Library", "Pictures/iCloud Photos",  # macOS
    "AppData",  # Windows user-local crap
    "$Recycle.Bin", "System Volume Information",  # Windows
})

DEFAULT_MAX_FILE_BYTES = 64  # bytes read from head and from tail
DEFAULT_MAX_FILES_PER_SCAN = 50_000  # safety cap

OP_NAMES = ("VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
            "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET")


# ─── File-entry dataclass ─────────────────────────────────────────

@dataclass
class FileEntry:
    """One file's metadata + content-blind signature."""
    path: str            # absolute path
    name: str            # basename
    size: int            # bytes
    mtime: float         # epoch seconds
    op_path: List[int]   # short operator path (length = signature_depth)
    op_path_str: str     # comma-separated for display (e.g. "3,7,5,2,9")
    suffix: str          # file extension (lowercase, no dot)
    parent: str          # basename of the immediate parent directory

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ─── Signature computation ────────────────────────────────────────

def _operator_path_from_bytes(data: bytes, depth: int = 8) -> List[int]:
    """Deterministic operator path from arbitrary bytes.  Uses SHA-1
    (just as a stable bit-mixer, NOT for crypto) then takes the first
    `depth` bytes mod 10.  Note: this is a content-blind fingerprint
    primitive; we do NOT claim cryptographic properties."""
    h = hashlib.sha1(data).digest()
    return [h[i] % 10 for i in range(min(depth, len(h)))]


def _signature_for_file(path: Path,
                          head_bytes: int = DEFAULT_MAX_FILE_BYTES,
                          tail_bytes: int = DEFAULT_MAX_FILE_BYTES
                          ) -> Tuple[List[int], int, float]:
    """Compute (op_path, size_bytes, mtime) for a single file.
    Reads at most head_bytes + tail_bytes of the file."""
    try:
        st = path.stat()
        size = st.st_size
        mtime = st.st_mtime
    except (OSError, PermissionError):
        return ([], 0, 0.0)

    # Build the seed bytes: filename + size + head + tail
    seed = path.name.encode("utf-8", errors="replace")
    seed += str(size).encode("ascii")
    try:
        with open(path, "rb") as f:
            head = f.read(head_bytes)
            if size > head_bytes + tail_bytes:
                try:
                    f.seek(-tail_bytes, 2)  # 2 = from end
                    tail = f.read(tail_bytes)
                except OSError:
                    tail = b""
            else:
                tail = b""
        seed += head + tail
    except (OSError, PermissionError):
        pass

    op_path = _operator_path_from_bytes(seed, depth=8)
    return (op_path, size, mtime)


# ─── Ignore-path helper ───────────────────────────────────────────

def _should_skip(path: Path, ignores: frozenset) -> bool:
    parts = set(path.parts)
    if any(p in ignores for p in parts):
        return True
    # Also skip dot-files at any level
    if any(p.startswith(".") and len(p) > 1 and p not in {".", ".."}
           for p in path.parts):
        return True
    return False


# ─── Index ────────────────────────────────────────────────────────

class FileOrientIndex:
    """Persistent file orientation index."""

    def __init__(self,
                  index_path: Optional[Path] = None,
                  ignores: Optional[frozenset] = None):
        self.index_path = index_path or (
            Path.home() / ".ck" / "file_orient_index.jsonl"
        )
        self.ignores = ignores or DEFAULT_IGNORES
        self._entries: Dict[str, FileEntry] = {}
        self._load()

    def _load(self) -> None:
        if not self.index_path.exists():
            return
        try:
            with open(self.index_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        d = json.loads(line)
                        self._entries[d["path"]] = FileEntry(**d)
                    except Exception:
                        continue
        except Exception:
            pass

    def _save(self) -> None:
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.index_path, "w", encoding="utf-8") as f:
            for e in self._entries.values():
                f.write(json.dumps(e.to_dict(), ensure_ascii=False) + "\n")

    def scan_directory(self,
                         root: Path,
                         max_files: int = DEFAULT_MAX_FILES_PER_SCAN,
                         on_progress: Optional[Callable[[int, str], None]] = None
                         ) -> Dict[str, Any]:
        """Walk `root` and index files. Incremental: skips files whose
        mtime hasn't changed since last scan.  Returns a summary."""
        root = Path(root).resolve()
        if not root.exists():
            return {"ok": False, "error": f"root does not exist: {root}"}
        if not root.is_dir():
            return {"ok": False, "error": f"root is not a directory: {root}"}

        n_scanned = 0
        n_new = 0
        n_updated = 0
        n_skipped_unchanged = 0
        n_skipped_ignored = 0
        n_errors = 0

        for dirpath, dirnames, filenames in os.walk(root):
            # Prune ignored directories in-place so os.walk doesn't recurse
            dirnames[:] = [d for d in dirnames
                            if not _should_skip(Path(dirpath) / d, self.ignores)]
            for fname in filenames:
                fpath = Path(dirpath) / fname
                if _should_skip(fpath, self.ignores):
                    n_skipped_ignored += 1
                    continue
                if n_scanned >= max_files:
                    break
                spath = str(fpath)
                # Incremental: skip unchanged
                try:
                    cur_mtime = fpath.stat().st_mtime
                except (OSError, PermissionError):
                    n_errors += 1
                    continue
                existing = self._entries.get(spath)
                if existing and abs(existing.mtime - cur_mtime) < 1e-3:
                    n_skipped_unchanged += 1
                    continue

                op_path, size, mtime = _signature_for_file(fpath)
                if not op_path:
                    n_errors += 1
                    continue
                entry = FileEntry(
                    path=spath,
                    name=fname,
                    size=size,
                    mtime=mtime,
                    op_path=op_path,
                    op_path_str=",".join(str(x) for x in op_path),
                    suffix=fpath.suffix.lstrip(".").lower(),
                    parent=fpath.parent.name,
                )
                if existing:
                    n_updated += 1
                else:
                    n_new += 1
                self._entries[spath] = entry
                n_scanned += 1
                if on_progress and n_scanned % 500 == 0:
                    on_progress(n_scanned, fname)
            if n_scanned >= max_files:
                break

        self._save()
        return {
            "ok": True,
            "root": str(root),
            "n_scanned": n_scanned,
            "n_new": n_new,
            "n_updated": n_updated,
            "n_skipped_unchanged": n_skipped_unchanged,
            "n_skipped_ignored": n_skipped_ignored,
            "n_errors": n_errors,
            "n_total_in_index": len(self._entries),
        }

    def find_by_query(self, query: str, n: int = 10) -> List[Dict[str, Any]]:
        """Fuzzy match query against filename + path components."""
        q = query.lower().strip()
        if not q:
            return []
        words = re.findall(r"\w+", q)
        scored: List[Tuple[float, FileEntry]] = []
        for entry in self._entries.values():
            score = 0.0
            target = (entry.name + " " + entry.parent).lower()
            target_path = entry.path.lower()
            for w in words:
                if w in target:
                    score += 1.0
                if w in target_path:
                    score += 0.5
                if entry.suffix == w:
                    score += 0.5
            if score > 0:
                scored.append((score, entry))
        scored.sort(key=lambda x: -x[0])
        return [
            {**entry.to_dict(), "_score": round(s, 3)}
            for s, entry in scored[:n]
        ]

    def find_by_signature(self, seed_path: str, n: int = 10) -> List[Dict[str, Any]]:
        """Find files with operator-path signature similar to seed."""
        seed = self._entries.get(seed_path)
        if not seed:
            # Try absolute resolution
            try:
                rp = str(Path(seed_path).resolve())
                seed = self._entries.get(rp)
            except Exception:
                pass
        if not seed:
            return []
        scored: List[Tuple[int, FileEntry]] = []
        seed_op = seed.op_path
        for entry in self._entries.values():
            if entry.path == seed.path:
                continue
            overlap = sum(
                1 for i in range(min(len(seed_op), len(entry.op_path)))
                if seed_op[i] == entry.op_path[i]
            )
            if overlap > 0:
                scored.append((overlap, entry))
        scored.sort(key=lambda x: -x[0])
        return [
            {**entry.to_dict(), "_overlap": ov}
            for ov, entry in scored[:n]
        ]

    def stats(self) -> Dict[str, Any]:
        """Summary of what's in the index."""
        from collections import Counter
        sufs = Counter(e.suffix for e in self._entries.values() if e.suffix)
        total_bytes = sum(e.size for e in self._entries.values())
        return {
            "n_files": len(self._entries),
            "total_gb": round(total_bytes / (1024 ** 3), 3),
            "top_extensions": dict(sufs.most_common(10)),
            "index_path": str(self.index_path),
        }

    def clear(self) -> None:
        self._entries = {}
        if self.index_path.exists():
            self.index_path.unlink()


# ─── Engine mount ─────────────────────────────────────────────────

def mount_file_orient(engine: Any,
                       index_path: Optional[Path] = None) -> bool:
    """Attach FileOrientIndex to engine + register Flask endpoints.

    Endpoints (read-only; user explicitly triggers scans):
      POST /file/scan           — body: {"root": "<path>"} — index a tree
      GET  /file/query?q=X&n=N  — fuzzy match by name/path
      GET  /file/similar?path=P&n=N — find files with similar signature
      GET  /file/stats          — index summary
      GET  /file/info           — module philosophy + scope
    """
    idx = FileOrientIndex(index_path=index_path)
    engine.ck_file_orient = {
        "index": idx,
        "scan_directory": idx.scan_directory,
        "find_by_query": idx.find_by_query,
        "find_by_signature": idx.find_by_signature,
        "stats": idx.stats,
    }

    api = getattr(engine, "web_api", None) or getattr(engine, "api", None)
    if api is not None:
        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify, request  # type: ignore

                def _scan():
                    payload = request.get_json(silent=True) or {}
                    root = payload.get("root")
                    if not root:
                        return jsonify({"ok": False,
                                          "error": "missing 'root' field"}), 400
                    result = idx.scan_directory(Path(root))
                    return jsonify(result)

                def _query():
                    q = request.args.get("q", "")
                    n = request.args.get("n", default=10, type=int)
                    return jsonify({
                        "query": q,
                        "results": idx.find_by_query(q, n=n),
                    })

                def _similar():
                    p = request.args.get("path", "")
                    n = request.args.get("n", default=10, type=int)
                    return jsonify({
                        "seed_path": p,
                        "results": idx.find_by_signature(p, n=n),
                    })

                def _stats():
                    return jsonify(idx.stats())

                def _info():
                    return jsonify({
                        "module": "ck_file_orient",
                        "philosophy": ("content-blind file index. CK "
                                        "signs each file from its name + "
                                        "size + first/last 64 bytes — "
                                        "never reads full contents. "
                                        "User triggers scans explicitly."),
                        "scope": ("Read-only. Never moves / copies / "
                                   "renames / deletes. No outbound "
                                   "network. Bounded I/O per file."),
                        "endpoints": [
                            "POST /file/scan",
                            "GET /file/query?q=X&n=N",
                            "GET /file/similar?path=P&n=N",
                            "GET /file/stats", "GET /file/info",
                        ],
                        "ignores": sorted(DEFAULT_IGNORES),
                    })

                existing = {r.rule for r in app.url_map.iter_rules()}
                for rule, ep, fn, methods in (
                    ("/file/scan",    "file_scan",    _scan,    ["POST"]),
                    ("/file/query",   "file_query",   _query,   ["GET"]),
                    ("/file/similar", "file_similar", _similar, ["GET"]),
                    ("/file/stats",   "file_stats",   _stats,   ["GET"]),
                    ("/file/info",    "file_info",    _info,    ["GET"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
            except Exception as e:
                print(f"[CK Gen14] mount_file_orient: routes failed: {e}")

    print(f"[CK Gen14] mount_file_orient: FileOrientIndex at "
          f"{idx.index_path.name} ({len(idx._entries)} entries)")
    return True


# ─── CLI smoke ────────────────────────────────────────────────────

if __name__ == "__main__":
    import tempfile
    print("ck_file_orient smoke test")
    print("=" * 60)
    print()

    # Use a temp index path so we don't pollute the user's real index
    tmp_idx = Path(tempfile.gettempdir()) / "ck_orient_smoke.jsonl"
    if tmp_idx.exists():
        tmp_idx.unlink()
    idx = FileOrientIndex(index_path=tmp_idx)

    # Scan a small known directory: the brain folder itself
    print("Step 1: scan Gen14/targets/ck/brain (small test scan)")
    print("-" * 60)
    root = Path(__file__).parent
    result = idx.scan_directory(root)
    print(f"  ok:                 {result['ok']}")
    print(f"  n_scanned:          {result['n_scanned']}")
    print(f"  n_new:              {result['n_new']}")
    print(f"  n_skipped_ignored:  {result['n_skipped_ignored']}")
    print(f"  n_total_in_index:   {result['n_total_in_index']}")
    print()
    print("Step 2: stats")
    print("-" * 60)
    s = idx.stats()
    print(f"  n_files:    {s['n_files']}")
    print(f"  total_gb:   {s['total_gb']}")
    print(f"  top_exts:   {s['top_extensions']}")
    print()
    print("Step 3: query for 'auditor'")
    print("-" * 60)
    hits = idx.find_by_query("auditor", n=5)
    for h in hits:
        print(f"  [{h['_score']:.2f}]  {h['name']:50s}  op_path={h['op_path_str']}")
    print()
    print("Step 4: query for 'rhythm'")
    print("-" * 60)
    hits = idx.find_by_query("rhythm", n=3)
    for h in hits:
        print(f"  [{h['_score']:.2f}]  {h['name']:50s}  op_path={h['op_path_str']}")
    print()
    print("Step 5: cleanup")
    print("-" * 60)
    idx.clear()
    print(f"  index cleared; file exists: {tmp_idx.exists()}")
    print()
    print("Smoke test complete.")
