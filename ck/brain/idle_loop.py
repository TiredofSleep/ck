# -*- coding: utf-8 -*-
"""
idle_loop.py - the closing loop between fluency log and brain trinity.

MATH_IN_CK.md Sec 9.2 promised this module: read the append-only JSONL
log of Ollama turns, decompose each entry's operator profile onto the
AO 5-element basis, and strengthen the 5x5 Hebbian tensor links that
co-fired.  That is how Ollama's output teaches CK's brain without ever
touching the model's weights.

Design constraints (G6 hands-on-wheel):
- On-demand CLI ONLY.  No cron, no service, no autostart.
- Stateless between invocations EXCEPT via the persistent tensor file
  (ck/brain/hebbian_5x5.json) and the offset log
  (ck/brain/hebbian_5x5.offsets.json).
- Idempotent: running it twice on the same log does NOT double-count.
  The offset log records (log_file, last_line_index) per file.

Per-entry update recipe:
    1. Read entry i and entry i-1 from the daily JSONL file.
    2. Extract each profile dict from entry.ck_score.operator_profile.
    3. Project each 10-profile to AO 5-vector via ao_basis.project_10_to_5.
    4. Call tensor.update(d_now, d_prev).
    5. The very first entry of the whole history uses d_prev = d_now
       (self-outer; no history yet).

CLI:
    python -m ck.brain.idle_loop              (defaults)
    python -m ck.brain.idle_loop --dry-run    (report, do not write)
    python -m ck.brain.idle_loop --reset      (start offsets from zero)
    python -m ck.brain.idle_loop --log-dir X  (override log dir)
    python -m ck.brain.idle_loop --tensor PATH
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .ao_basis import project_10_to_5, AO_NAMES, NUM_AO
from .hebbian_5x5 import HebbianTensor5x5, DEFAULT_TENSOR_PATH


# ---------------------------------------------------------------------------
# paths
# ---------------------------------------------------------------------------

_MODULE_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _MODULE_DIR.parent.parent        # ck/brain -> ck -> repo root
DEFAULT_LOG_DIR = _REPO_ROOT / "ck" / "fluency" / "logs"
DEFAULT_OFFSETS_PATH = _MODULE_DIR / "hebbian_5x5.offsets.json"


# ---------------------------------------------------------------------------
# offset log: how far we've processed each daily file
# ---------------------------------------------------------------------------


def load_offsets(path: Path) -> Dict[str, int]:
    """Return {filename: next_line_index_to_process}.  Missing -> {}."""
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return {}
        return {str(k): int(v) for k, v in data.items()}
    except (json.JSONDecodeError, ValueError, OSError):
        return {}


def save_offsets(path: Path, offsets: Dict[str, int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(offsets, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.flush()
    tmp.replace(path)


# ---------------------------------------------------------------------------
# the sweep
# ---------------------------------------------------------------------------


def extract_profile(entry: Dict[str, Any]) -> Optional[List[float]]:
    """Return AO-5 vector for this log entry, or None if entry is unscored.

    ``ollama-error`` entries (where Ollama was offline) have empty
    ck_score and are skipped -- no math event to learn from.
    """
    ck_score = entry.get("ck_score") or {}
    profile = ck_score.get("operator_profile")
    if not profile:
        return None
    try:
        return project_10_to_5(profile)
    except (TypeError, ValueError):
        return None


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    """Read one daily jsonl file.  Skips blank and malformed lines."""
    rows: List[Dict[str, Any]] = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for raw in f:
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    rows.append(json.loads(raw))
                except json.JSONDecodeError:
                    # preserve marker; don't crash on a bad line
                    rows.append({"_parse_error": True, "raw": raw})
    except OSError:
        return []
    return rows


def sweep(
    tensor: HebbianTensor5x5,
    log_dir: Path,
    offsets: Dict[str, int],
    max_entries: Optional[int] = None,
) -> Tuple[int, int, Optional[List[float]]]:
    """Consume new log entries and apply updates in place.

    Returns ``(files_touched, updates_applied, last_d_vector)``.

    ``max_entries``, if given, caps how many new entries are processed
    across all files this call.  Useful for --dry-run or for bounded
    incremental work.

    The "previous d" is threaded across entries in chronological order
    within this sweep, but at the very start of the sweep we have no
    in-memory prior because the tensor's own state is what carries
    history.  For the FIRST entry of the sweep we use d_prev = d_now
    (self-outer), which is the Hebbian "prior matches present" update.
    Subsequent entries in the sweep pair with the last-processed d.
    """
    files = sorted(log_dir.glob("corrections_*.jsonl"))
    if not files:
        return 0, 0, None

    files_touched = 0
    updates = 0
    d_prev: Optional[List[float]] = None

    for fpath in files:
        fname = fpath.name
        start_at = int(offsets.get(fname, 0))
        rows = read_jsonl(fpath)
        if start_at >= len(rows):
            # already caught up on this file
            continue
        files_touched += 1

        for idx in range(start_at, len(rows)):
            if max_entries is not None and updates >= max_entries:
                offsets[fname] = idx
                return files_touched, updates, d_prev
            entry = rows[idx]
            d_now = extract_profile(entry)
            if d_now is None:
                # skip unscored / error entries, but still advance offset
                continue
            use_prev = d_prev if d_prev is not None else d_now
            tensor.update(d_now, use_prev)
            d_prev = d_now
            updates += 1

        offsets[fname] = len(rows)

    return files_touched, updates, d_prev


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="CK brain idle loop: feed fluency log into Hebbian 5x5 tensor.",
    )
    ap.add_argument("--log-dir", default=str(DEFAULT_LOG_DIR),
                    help="where the corrections_YYYY_MM_DD.jsonl files live")
    ap.add_argument("--tensor", default=str(DEFAULT_TENSOR_PATH),
                    help="path to the persistent Hebbian 5x5 JSON file")
    ap.add_argument("--offsets", default=str(DEFAULT_OFFSETS_PATH),
                    help="path to the per-file offset tracker")
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would happen; do not write tensor or offsets")
    ap.add_argument("--reset", action="store_true",
                    help="start offsets from zero (re-process everything)")
    ap.add_argument("--max-entries", type=int, default=None,
                    help="cap on entries processed this call")
    ap.add_argument("--verbose", "-v", action="store_true",
                    help="print per-entry diagnostic")
    return ap.parse_args(argv)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def main(argv: Optional[List[str]] = None) -> int:
    args = _parse_args(argv)
    log_dir = Path(args.log_dir)
    tensor_path = Path(args.tensor)
    offsets_path = Path(args.offsets)

    if not log_dir.exists():
        print(f"[idle_loop] log dir not found: {log_dir}", file=sys.stderr)
        return 2

    # load
    tensor = HebbianTensor5x5.load(tensor_path)
    offsets = {} if args.reset else load_offsets(offsets_path)

    norm_before = tensor.norm()
    print(f"[idle_loop] {_now_iso()}")
    print(f"[idle_loop]   log dir: {log_dir}")
    print(f"[idle_loop]   tensor:  {tensor_path} (norm={norm_before:.4f}, "
          f"n_updates={tensor.n_updates})")
    print(f"[idle_loop]   offsets: {offsets_path} ({len(offsets)} files)")

    # sweep
    files_touched, updates, d_last = sweep(
        tensor=tensor,
        log_dir=log_dir,
        offsets=offsets,
        max_entries=args.max_entries,
    )

    norm_after = tensor.norm()

    if args.verbose and d_last is not None:
        print(f"[idle_loop]   last d: " + ", ".join(
            f"{AO_NAMES[i]}={d_last[i]:.3f}" for i in range(NUM_AO)
        ))

    # report
    print(f"[idle_loop] files_touched={files_touched} updates={updates} "
          f"norm_before={norm_before:.4f} norm_after={norm_after:.4f}")
    top = tensor.top_links(3, off_diagonal_only=True)
    if top:
        print(f"[idle_loop] top off-diagonal links:")
        for (a, b, w) in top:
            print(f"[idle_loop]   {a}-{b}: {w:+.4f}")

    if args.dry_run:
        print("[idle_loop] --dry-run: NOT persisting tensor or offsets.")
        return 0

    # record sweep provenance into tensor.meta
    tensor.meta["last_sweep_at"] = _now_iso()
    tensor.meta["last_sweep_files_touched"] = files_touched
    tensor.meta["last_sweep_updates"] = updates
    tensor.save(tensor_path)
    save_offsets(offsets_path, offsets)
    print(f"[idle_loop] wrote tensor -> {tensor_path}")
    print(f"[idle_loop] wrote offsets -> {offsets_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
