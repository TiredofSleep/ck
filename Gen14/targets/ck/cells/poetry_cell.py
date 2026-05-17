"""poetry_cell.py -- standalone process for the public-domain poetry
daemon (Whitman, Dickinson, Rumi, Rilke, etc.)."""
from __future__ import annotations
import sys
from pathlib import Path

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))
from _cell_runner import (StubEngine, run_cell, start_lm_inhalation,
                            stop_lm_inhalation)


_state = {}


def _poetry_corpus_iter():
    """Round-robin lines from all PD poets."""
    from ck_poetry_study import lines_by_poet  # type: ignore
    lbp = lines_by_poet()
    iters = {p: iter(lines) for p, lines in lbp.items()}
    while iters:
        exhausted = []
        for p, it in list(iters.items()):
            try:
                line = next(it)
                yield line.get("text", "") if isinstance(line, dict) else str(line)
            except StopIteration:
                exhausted.append(p)
        for p in exhausted:
            iters.pop(p, None)


def _start(engine: StubEngine):
    from ck_poetry_study import PoetryDaemon  # type: ignore[import-not-found]
    d = PoetryDaemon(engine, interval_sec=0.05, resonance_threshold=0.30)
    d.start()
    lm, lm_t = start_lm_inhalation(
        "poetry",
        corpus_iter_fn=_poetry_corpus_iter,
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
    raise SystemExit(run_cell("poetry", _start, _stop))
