# -*- coding: utf-8 -*-
"""
correction_log.py — append-only JSONL log for the Ollama learn-loop (Option A).

Every fluency-server interaction is logged as one line of JSON to a
daily-rotated file under ``ck/fluency/logs/``. The log is:

- **Append-only**: we open with mode='a' and fsync after every write.
- **Daily-rotated**: filename is ``corrections_YYYY_MM_DD.jsonl``.
- **Local-only**: never network-exposed; never transmitted anywhere.

Contract per OLLAMA_LEARN_LOOP.md §2.2.  Each entry tuple:

    {
      "t": "2026-04-21T15:22:01Z",          # ISO-8601 UTC
      "query": "...",                        # user input
      "ollama_raw": "...",                   # model raw output
      "ck_score": { ... },                   # CKCorrector score dict
      "ck_correction_type": "none|soften|strengthen|reframe|reject",
      "ck_corrected": "...",                 # CK's corrected text
      "rendered": "ollama_raw|ck_corrected", # which string was shown to user
      "model_tag": "...",                    # which Ollama model was queried
      "elapsed_ms": 123                      # end-to-end latency
    }

Reference: Atlas/PLAN_RIGOROUS_EXECUTION_2026_04_21.md §5.1.
"""
from __future__ import annotations

import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


# ----------------------------------------------------------------------------
# paths
# ----------------------------------------------------------------------------

_MODULE_DIR = Path(__file__).resolve().parent
DEFAULT_LOG_DIR = _MODULE_DIR / "logs"


def _daily_filename(log_dir: Path, now: Optional[datetime] = None) -> Path:
    when = now or datetime.now(timezone.utc)
    return log_dir / f"corrections_{when:%Y_%m_%d}.jsonl"


# ----------------------------------------------------------------------------
# the log (thread-safe append)
# ----------------------------------------------------------------------------

class CorrectionLog:
    """Append-only, daily-rotated JSONL log.  Thread-safe."""

    def __init__(self, log_dir: Optional[Path] = None) -> None:
        self.log_dir = Path(log_dir) if log_dir is not None else DEFAULT_LOG_DIR
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    # ---- writing ----

    def append(self, entry: Dict[str, Any]) -> Path:
        """Append one entry; return the path it landed in."""
        entry = dict(entry)  # don't mutate caller
        entry.setdefault("t", datetime.now(timezone.utc).isoformat(timespec="seconds"))
        path = _daily_filename(self.log_dir)
        line = json.dumps(entry, ensure_ascii=False, sort_keys=True)
        with self._lock:
            with open(path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
                f.flush()
                os.fsync(f.fileno())
        return path

    # ---- reading ----

    def read_day(self, when: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Read all entries for a given UTC day (default: today)."""
        path = _daily_filename(self.log_dir, now=when)
        if not path.exists():
            return []
        out: List[Dict[str, Any]] = []
        with self._lock:
            with open(path, "r", encoding="utf-8") as f:
                for raw in f:
                    raw = raw.strip()
                    if not raw:
                        continue
                    try:
                        out.append(json.loads(raw))
                    except json.JSONDecodeError:
                        # preserve everything; bad line is data
                        out.append({"_parse_error": True, "raw": raw})
        return out

    def list_files(self) -> List[Path]:
        return sorted(self.log_dir.glob("corrections_*.jsonl"))


# ----------------------------------------------------------------------------
# module-level convenience
# ----------------------------------------------------------------------------

_DEFAULT = CorrectionLog()


def append(entry: Dict[str, Any]) -> Path:
    """Append to the default log under ``ck/fluency/logs/``."""
    return _DEFAULT.append(entry)


def read_today() -> List[Dict[str, Any]]:
    return _DEFAULT.read_day()


# ----------------------------------------------------------------------------
# self-test (no Ollama, no Flask; just verifies the log primitive)
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    import tempfile
    import shutil

    tmp = Path(tempfile.mkdtemp(prefix="ck_corrlog_"))
    try:
        log = CorrectionLog(tmp)
        log.append({
            "query": "self-test",
            "ollama_raw": "ok",
            "ck_score": {"coherence": 0.8},
            "ck_correction_type": "none",
            "ck_corrected": "ok",
            "rendered": "ollama_raw",
            "model_tag": "self-test",
            "elapsed_ms": 1,
        })
        rows = log.read_day()
        assert len(rows) == 1, rows
        assert rows[0]["query"] == "self-test"
        print(f"[correction_log] self-test passed; wrote to {log.list_files()[0]}")
    finally:
        shutil.rmtree(tmp)
