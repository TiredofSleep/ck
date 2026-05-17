"""domain_cell.py -- standalone process for the ck_library domain
study (341 subjects, top-K per subject)."""
from __future__ import annotations
import sys
from pathlib import Path

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))
from _cell_runner import (StubEngine, run_cell, start_lm_inhalation,
                            stop_lm_inhalation)


_state = {}


def _domain_corpus_iter():
    """Round-robin chain text snippets across all 341 ck_library
    subjects.  Each subject contributes its chain prose evenly."""
    from ck_domain_study import subjects, load_chains  # type: ignore
    sub_iters = {}
    for subj, folder in subjects():
        sub_iters[subj] = iter(load_chains(folder))
    while sub_iters:
        exhausted = []
        for subj, it in list(sub_iters.items()):
            try:
                ch = next(it)
                if isinstance(ch, dict):
                    text = ch.get("text") or ch.get("body") or \
                            ch.get("content") or ""
                    if not text and "name" in ch:
                        text = str(ch.get("name", ""))
                    if text:
                        yield text
                else:
                    yield str(ch)
            except StopIteration:
                exhausted.append(subj)
        for subj in exhausted:
            sub_iters.pop(subj, None)


def _start(engine: StubEngine):
    from ck_domain_study import DomainStudyDaemon  # type: ignore[import-not-found]
    d = DomainStudyDaemon(engine, interval_sec=0.05, resonance_threshold=0.55)
    d.start()
    lm, lm_t = start_lm_inhalation(
        "domain",
        corpus_iter_fn=_domain_corpus_iter,
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
    raise SystemExit(run_cell("domain", _start, _stop))
