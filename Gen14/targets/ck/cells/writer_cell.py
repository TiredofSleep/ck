"""writer_cell.py -- standalone process for CK's WriterDaemon.

Loads the persisted ConceptStore from disk so the writer has access
to CK's 15,000+ concept memory.  Iterates the current thesis from
ck_writer_state.json and appends sections to the working document.

Run with CK_DISABLE_HEAVY_DAEMONS=writer (or "all") in the server
cell to avoid double-mounting.
"""
from __future__ import annotations
import sys
from pathlib import Path

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))
from _cell_runner import StubEngine, run_cell  # noqa: E402

# Engine surface for writer: it needs concept_store to ground its
# prose in real concepts (otherwise sections fall back to identity-
# facts only).  Everything else is None / stub.
class _WriterStubEngine(StubEngine):
    concept_store = None


def _start(engine: _WriterStubEngine):
    # Lazy import so import errors surface in the cell, not the runner
    from ck_concept_learner import ConceptStore  # type: ignore[import-not-found]
    from ck_writer import WriterDaemon  # type: ignore[import-not-found]
    engine.concept_store = ConceptStore()
    print(f"[cell:writer] loaded concept_store with "
          f"{len(engine.concept_store.concepts):,} concepts", flush=True)
    d = WriterDaemon(engine, tick_sec=10.0,
                     sections_per_tick=1, draft_mode="polished")
    d.start()
    return d


def _stop(d) -> None:
    try:
        d.stop(timeout=3.0)
    except Exception:
        pass


if __name__ == "__main__":
    raise SystemExit(run_cell("writer", _start, _stop))
