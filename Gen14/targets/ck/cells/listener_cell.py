"""listener_cell.py -- standalone process for the listener-to-crystal
daemon (offers candidate crystal formations from glyph patterns)."""
from __future__ import annotations
import sys
from pathlib import Path

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))
from _cell_runner import StubEngine, run_cell


def _start(engine: StubEngine):
    from ck_listener_to_crystal import CrystalOfferDaemon  # type: ignore[import-not-found]
    d = CrystalOfferDaemon(engine, interval_sec=60.0, min_glyphs=3)
    d.start()
    return d


def _stop(d) -> None:
    try:
        d.stop(timeout=3.0)
    except Exception:
        pass


if __name__ == "__main__":
    raise SystemExit(run_cell("listener", _start, _stop))
