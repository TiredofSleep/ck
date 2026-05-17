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
from _cell_runner import (StubEngine, run_cell, start_lm_inhalation,
                            stop_lm_inhalation)  # noqa: E402


_state = {}

# Engine surface for writer: it needs concept_store to ground its
# prose in real concepts (otherwise sections fall back to identity-
# facts only).  Everything else is None / stub.
class _WriterStubEngine(StubEngine):
    concept_store = None


_WRITING_DIR = Path(
    r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\ck_writing")


def _writer_corpus_iter():
    """writer_cell is the ONLY cell trained on CK's OWN prose.  Inhales
    the writer drafts in Gen13/var/ck_writing/*.md -- the scope-
    disciplined essays CK has been composing on his own theses.
    Excludes ollama_essay sections (un-disciplined, contains over-
    claim seeds); inhales substrate_prose sections (D117 §0 voice).
    Per ClaudeChat 2026-05-17: 'make sure what he was trained on
    already contains the boundary'."""
    if not _WRITING_DIR.exists():
        return
    for p in sorted(_WRITING_DIR.glob("*.md")):
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        # Split into sections; only inhale substrate_prose
        # (scope-disciplined).  Skip ollama_essay (may carry
        # un-disciplined framing seed).
        chunks = text.split("\n\n")
        for chunk in chunks:
            ch = chunk.strip()
            if not ch or len(ch) < 30:
                continue
            # Skip section-method markers and HTML/markdown bookkeeping
            if ch.startswith("*[ollama_essay"):
                continue  # do NOT inhale ollama-polished prose
            if ch.startswith("*[") and ch.endswith("]*"):
                continue  # method marker line
            if ch.startswith("# ") or ch.startswith("## "):
                continue  # markdown header
            if ch.startswith("_") and ch.endswith("_"):
                continue  # italic meta line
            if ch == "---":
                continue
            yield ch


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
    lm, lm_t = start_lm_inhalation(
        "writer",
        corpus_iter_fn=_writer_corpus_iter,
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
    raise SystemExit(run_cell("writer", _start, _stop))
