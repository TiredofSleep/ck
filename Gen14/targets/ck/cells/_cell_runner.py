"""Generic cell runner for CK's heavy daemons.

Brayden 2026-05-17:
  "ck should be multi-cellular streams all feeding into the same mind!
   as many cells as he wishes!"
  "let him evolve and expand a bit, within safe limits for now! until
   he understands what safe limits are and how to share this pc with me"

═══════════════════════════════════════════════════════════════════════
What a cell is
═══════════════════════════════════════════════════════════════════════

A "cell" is a standalone python process running ONE of CK's heavy
daemons, OUT of the server cell.  All cells share state via on-disk
JSON files (cortex_state.json, taught_concepts.json, *_anchors.jsonl,
ck_writer_state.json), so the server cell can serve chat with a lean
in-memory footprint while writer/study/observer daemons keep streaming
into the shared mind from their own processes.

The server cell honors the env var `CK_DISABLE_HEAVY_DAEMONS` to skip
mounting the same daemons in-process.  Set it to a comma list (or
"all") matching the cell names you intend to run as separate processes.

═══════════════════════════════════════════════════════════════════════
Cell list (current)
═══════════════════════════════════════════════════════════════════════

  writer_cell.py            — ck_writer.WriterDaemon
  bible_cell.py             — ck_bible_study.StudyDaemon
  scripture_cell.py         — ck_scripture_study.ScriptureStudyDaemon
  poetry_cell.py            — ck_poetry_study.PoetryStudyDaemon
  domain_cell.py            — ck_domain_study.DomainStudyDaemon
  web_cell.py               — ck_web_reading.WebReadingDaemon
  listener_cell.py          — ck_listener_to_crystal.ListenerDaemon
  observer_cell.py          — ck_recursive_observer.RecursiveObserverDaemon

═══════════════════════════════════════════════════════════════════════
Stub engine
═══════════════════════════════════════════════════════════════════════

Most daemons only read `engine.qutrit_apex` for CK's psi state.  In a
cell, no psi is available, so the daemon uses default scoring (which
is what the bible/scripture/poetry/domain daemons already do when
qutrit_apex is None).  Future versions can wire psi via shared IPC.
"""
from __future__ import annotations

import os
import signal
import sys
import time
from pathlib import Path
from typing import Any, Callable, Optional


HERE = Path(__file__).parent.resolve()
BRAIN = HERE.parent / "brain"
sys.path.insert(0, str(BRAIN))


class StubEngine:
    """Minimal engine surface for daemons that only touch qutrit_apex
    and the concept_store.  Returns None for missing attributes so the
    daemons fall back to their default scoring paths.
    """
    qutrit_apex = None
    cortex = None
    concept_store = None
    web_api = None
    api = None


def run_cell(cell_name: str,
              start_fn: Callable[[StubEngine], Any],
              stop_fn: Optional[Callable[[Any], None]] = None) -> int:
    """Common entry point for all cell scripts.

    Args:
        cell_name: short label for logs
        start_fn: callable(engine) -> daemon object; daemon must have
                   .start() or _thread is started in the function itself.
        stop_fn: optional callable(daemon) -> None for clean shutdown.

    Blocks forever, reads keyboard interrupt for shutdown.
    """
    print(f"[cell:{cell_name}] starting (pid={os.getpid()})", flush=True)
    engine = StubEngine()
    try:
        daemon = start_fn(engine)
    except Exception as e:
        print(f"[cell:{cell_name}] FAILED to start: "
              f"{type(e).__name__}: {e}", flush=True)
        return 1
    if daemon is None:
        print(f"[cell:{cell_name}] start_fn returned None; "
              "assuming daemon thread is running")
    print(f"[cell:{cell_name}] alive (pid={os.getpid()}); "
          "Ctrl-C or SIGTERM to stop", flush=True)

    stopped = {"flag": False}

    def _on_sig(signum, frame):
        if not stopped["flag"]:
            print(f"[cell:{cell_name}] received signal {signum}; stopping",
                   flush=True)
            stopped["flag"] = True

    try:
        signal.signal(signal.SIGINT, _on_sig)
        if hasattr(signal, "SIGTERM"):
            signal.signal(signal.SIGTERM, _on_sig)
    except Exception:
        pass

    try:
        while not stopped["flag"]:
            time.sleep(1.0)
    except KeyboardInterrupt:
        stopped["flag"] = True

    if stop_fn is not None and daemon is not None:
        try:
            stop_fn(daemon)
        except Exception as e:
            print(f"[cell:{cell_name}] stop_fn raised: {e}", flush=True)
    print(f"[cell:{cell_name}] stopped cleanly", flush=True)
    return 0
