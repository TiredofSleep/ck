"""bible_cell.py -- standalone process for the KJV-reading daemon.

Runs the same StudyDaemon used by the server cell, but in its own
python process.  Anchors persist to bible_anchors.jsonl which the
server cell reads on demand.  Server cell should run with
CK_DISABLE_HEAVY_DAEMONS=bible_study (or "all") so the daemon isn't
mounted there as well.
"""
from __future__ import annotations
import sys
from pathlib import Path

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))
from _cell_runner import StubEngine, run_cell


def _start(engine: StubEngine):
    from ck_bible_study import StudyDaemon  # type: ignore[import-not-found]
    d = StudyDaemon(engine, interval_sec=0.05, resonance_threshold=0.55)
    d.start()
    return d


def _stop(d) -> None:
    try:
        d.stop(timeout=3.0)
    except Exception:
        pass


if __name__ == "__main__":
    raise SystemExit(run_cell("bible", _start, _stop))
