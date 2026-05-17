"""poetry_cell.py -- standalone process for the public-domain poetry
daemon (Whitman, Dickinson, Rumi, Rilke, etc.)."""
from __future__ import annotations
import sys
from pathlib import Path

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))
from _cell_runner import StubEngine, run_cell


def _start(engine: StubEngine):
    from ck_poetry_study import PoetryDaemon  # type: ignore[import-not-found]
    d = PoetryDaemon(engine, interval_sec=0.05, resonance_threshold=0.30)
    d.start()
    return d


def _stop(d) -> None:
    try:
        d.stop(timeout=3.0)
    except Exception:
        pass


if __name__ == "__main__":
    raise SystemExit(run_cell("poetry", _start, _stop))
