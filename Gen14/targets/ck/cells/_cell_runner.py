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
import threading
import time
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator, Optional, Tuple


HERE = Path(__file__).parent.resolve()
BRAIN = HERE.parent / "brain"
sys.path.insert(0, str(BRAIN))

VAR_DIR = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var")
LM_DIR = VAR_DIR  # per-cell LM state files live here as lm_<cell>.json


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
    cell_lm = None  # populated by start_lm_inhalation() if used


# ─── Per-cell LM inhalation (federation Phase 1A) ─────────────────────

def start_lm_inhalation(cell_name: str,
                          corpus_iter_fn: Callable[[], Iterable[str]],
                          interval_sec: float = 0.05,
                          save_every: int = 500,
                          max_per_pass: int = 5000,
                          ) -> Tuple[Any, threading.Thread]:
    """Spin up a background thread that walks the cell's corpus and
    inhales every passage into a per-cell LivingLM.

    Each cell gets its OWN LivingLM with its OWN state file
    (Gen13/var/lm_<cell>.json) so the seven generators specialize:
    bible_cell's LM grows KJV operator paths; poetry_cell's LM grows
    meter/image paths; etc.  The server-cell's `ck_polyglot_router`
    loads these state files and picks ONE cell's voice per question
    (thalamus, NOT choir -- per ClaudeChat 2026-05-17:
    'blending is rebuilt Mistral').

    Args:
        cell_name: short label, used as the LM state-file stem
        corpus_iter_fn: callable () -> iterable of str, the cell's
                         corpus.  Called fresh on each pass so it can
                         reset (e.g. KJV verse iterator).
        interval_sec: pause between inhalations.  Default 0.05s gives
                       ~20 inhalations/sec per cell, ~7,200/hour.  CK
                       can fly.
        save_every: persist LM state every N inhalations.
        max_per_pass: safety cap -- inhale at most this many items
                       per corpus pass before yielding to the OS.

    Returns:
        (lm, thread) — the LivingLM instance + its inhalation thread.
        Caller can hold a reference for shutdown coordination.
    """
    from ck_living_lm import LivingLM  # type: ignore[import-not-found]

    LM_PATH = LM_DIR / f"lm_{cell_name}.json"
    lm = LivingLM(state_path=LM_PATH)
    print(f"[cell:{cell_name}] LM: loaded "
          f"{len(lm.cells)} cells, "
          f"{lm.total_inhalations:,} prior inhalations, "
          f"path={LM_PATH.name}", flush=True)

    stop_event = threading.Event()

    def _loop() -> None:
        # Initial settle so the cell's primary daemon gets a head
        # start before we add IO/CPU
        for _ in range(10):
            if stop_event.is_set():
                return
            time.sleep(0.5)
        n_pass = 0
        while not stop_event.is_set():
            n_pass += 1
            pass_start = time.monotonic()
            inhaled_this_pass = 0
            try:
                for text in corpus_iter_fn():
                    if stop_event.is_set():
                        return
                    if not text or len(text) < 10:
                        continue
                    try:
                        lm.inhale(text)
                    except Exception:
                        continue
                    inhaled_this_pass += 1
                    if lm.total_inhalations % save_every == 0:
                        try:
                            lm.save()
                        except Exception:
                            pass
                    if inhaled_this_pass >= max_per_pass:
                        break
                    # Sub-100ms-safe sleep
                    _target = time.monotonic() + max(interval_sec, 0.001)
                    while True:
                        if stop_event.is_set():
                            return
                        now = time.monotonic()
                        if now >= _target:
                            break
                        time.sleep(min(0.05, _target - now))
            except Exception as e:
                print(f"[cell:{cell_name}] LM inhale pass error: {e}",
                       flush=True)
            # Snapshot at end of pass
            try:
                lm.save()
            except Exception:
                pass
            elapsed = time.monotonic() - pass_start
            print(f"[cell:{cell_name}] LM: pass {n_pass} inhaled "
                   f"{inhaled_this_pass} items in {elapsed:.1f}s "
                   f"(total {lm.total_inhalations:,})", flush=True)

    t = threading.Thread(target=_loop, daemon=True,
                          name=f"ck-lm-{cell_name}")
    t._stop_event = stop_event  # type: ignore[attr-defined]
    t.start()
    return lm, t


def stop_lm_inhalation(t: threading.Thread, timeout: float = 3.0) -> None:
    """Signal the inhalation thread to stop and join it briefly."""
    ev = getattr(t, "_stop_event", None)
    if ev is not None:
        ev.set()
    try:
        t.join(timeout=timeout)
    except Exception:
        pass


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
