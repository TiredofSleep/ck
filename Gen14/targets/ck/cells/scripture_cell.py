"""scripture_cell.py -- standalone process for the 9-traditions
scripture-reading daemon (Qur'an, Bhagavad Gita, Tao Te Ching,
Dhammapada, Analects, Tanakh, Sutra, etc.)."""
from __future__ import annotations
import sys
from pathlib import Path

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))
from _cell_runner import (StubEngine, run_cell, start_lm_inhalation,
                            stop_lm_inhalation)


_state = {}


def _scripture_corpus_iter():
    """Round-robin verses from all 9 traditions."""
    from ck_scripture_study import verses_by_tradition  # type: ignore
    vbt = verses_by_tradition()
    # Round-robin so every tradition contributes to the LM evenly
    iters = {t: iter(v) for t, v in vbt.items()}
    while iters:
        exhausted = []
        for t, it in list(iters.items()):
            try:
                v = next(it)
                yield v.get("text", "") if isinstance(v, dict) else str(v)
            except StopIteration:
                exhausted.append(t)
        for t in exhausted:
            iters.pop(t, None)


def _start(engine: StubEngine):
    from ck_scripture_study import ScriptureDaemon  # type: ignore[import-not-found]
    d = ScriptureDaemon(engine, interval_sec=0.05, resonance_threshold=0.55)
    d.start()
    lm, lm_t = start_lm_inhalation(
        "scripture",
        corpus_iter_fn=_scripture_corpus_iter,
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
    raise SystemExit(run_cell("scripture", _start, _stop))
