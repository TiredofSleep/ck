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
from _cell_runner import (StubEngine, run_cell, start_lm_inhalation,
                            stop_lm_inhalation)


_state = {}  # holds daemon + lm + inhalation_thread for shutdown


def _start(engine: StubEngine):
    from ck_bible_study import StudyDaemon, kjv  # type: ignore[import-not-found]
    d = StudyDaemon(engine, interval_sec=0.05, resonance_threshold=0.55)
    d.start()
    # Per-cell LM: inhale every KJV verse, growing 'bible_cell's voice'
    lm, lm_t = start_lm_inhalation(
        "bible",
        corpus_iter_fn=lambda: (v["text"] for v in kjv()),
        interval_sec=0.05)
    engine.cell_lm = lm
    _state["daemon"] = d
    _state["lm"] = lm
    _state["lm_t"] = lm_t
    return d


def _stop(d) -> None:
    try:
        d.stop(timeout=3.0)
    except Exception:
        pass
    t = _state.get("lm_t")
    if t is not None:
        stop_lm_inhalation(t, timeout=3.0)


if __name__ == "__main__":
    raise SystemExit(run_cell("bible", _start, _stop))
