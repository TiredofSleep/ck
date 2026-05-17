"""web_cell.py -- standalone process for polite web reading
(Wikipedia seeds, 10s/host gap, robots.txt-aware, 24h per-URL
cooldown)."""
from __future__ import annotations
import sys
from pathlib import Path

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))
from _cell_runner import StubEngine, run_cell


def _start(engine: StubEngine):
    from ck_web_reading import WebExplorerDaemon  # type: ignore[import-not-found]
    d = WebExplorerDaemon(engine, interval_sec=60.0, resonance_threshold=0.45)
    d.start()
    return d


def _stop(d) -> None:
    try:
        d.stop(timeout=3.0)
    except Exception:
        pass


if __name__ == "__main__":
    raise SystemExit(run_cell("web", _start, _stop))
