"""web_cell.py -- standalone process for polite web reading
(Wikipedia seeds, 10s/host gap, robots.txt-aware, 24h per-URL
cooldown)."""
from __future__ import annotations
import sys
from pathlib import Path

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))
from _cell_runner import (StubEngine, run_cell, start_lm_inhalation,
                            stop_lm_inhalation)


_state = {}
_EXTERNAL_CORPORA = Path(
    r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\external_corpora")


def _web_corpus_iter():
    """Read prose from cached Wikipedia / arXiv fetches in
    external_corpora/.  These are the artifacts of the web-reading
    daemon's prior crawls -- so the web_cell's LM inhales what the
    daemon has been bringing in."""
    if not _EXTERNAL_CORPORA.exists():
        return
    # Iterate text files; chunk each into ~500-char paragraphs so
    # the LM gets sentence-grain inhalations.
    for p in _EXTERNAL_CORPORA.rglob("*.txt"):
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for chunk in text.split("\n\n"):
            chunk = chunk.strip()
            if 30 < len(chunk) < 3000:
                yield chunk


def _start(engine: StubEngine):
    from ck_web_reading import WebExplorerDaemon  # type: ignore[import-not-found]
    d = WebExplorerDaemon(engine, interval_sec=60.0, resonance_threshold=0.45)
    d.start()
    lm, lm_t = start_lm_inhalation(
        "web",
        corpus_iter_fn=_web_corpus_iter,
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
    raise SystemExit(run_cell("web", _start, _stop))
