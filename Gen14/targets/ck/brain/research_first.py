"""
research_first.py -- research every prompt before every answer.

Brayden 2026-05-02: "he should research every prompt before every answer!!"

Wraps api.process_chat with a pre-research step that calls ck_research
on the user's prompt BEFORE cortex_speak replies.  The research findings
flow into engine.olfactory.absorb_ops (and from there into the cortex),
so cortex_speak's response is shaped by fresh research.

Modes (CK_RESEARCH_MODE env var):
  'off'    -- no pre-research; chat path unchanged.
  'fast'   -- 1 sub-question, headless browser, 30-60s budget. (default)
  'full'   -- 2-4 sub-questions, headless, up to 5min budget.
  'visible' -- visible browser (Brayden watches CK research).

The research wrapper sits at the OUTERMOST chat layer (after cells
shadow observer) so research happens FIRST in the request lifecycle,
then cells/cortex reply with research-enriched state.
"""
from __future__ import annotations

import os
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


_HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(_HERE))


LOG_DIR = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\research_first_logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)


# Per-session lock so we never run two research calls in parallel
# (Chrome can't safely handle that).
_RESEARCH_LOCK = threading.Lock()


def _today_log() -> Path:
    return LOG_DIR / f"research_first_{datetime.utcnow().strftime('%Y-%m-%d')}.jsonl"


def _log_event(event: str, **fields):
    import json
    record = {
        "ts": time.time(),
        "iso_ts": datetime.utcnow().isoformat(timespec='seconds') + "Z",
        "event": event,
        **fields,
    }
    try:
        with open(_today_log(), "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
    except Exception:
        pass


def _should_research(text: str) -> bool:
    """Decide whether the prompt warrants pre-research.  Some prompts are
    not worth burning Chrome cycles on (e.g. 'hello', state queries that
    cells already handle, 1-2 word non-substantive inputs)."""
    if not text or len(text.strip()) < 4:
        return False
    t = text.strip().lower()
    skips = (
        'hi', 'hello', 'hey', 'thanks', 'thank you', 'ok', 'okay',
        'yes', 'no', 'good', 'great',
    )
    if t in skips:
        return False
    if t.startswith(('hi ', 'hello ', 'hey ')):
        return False
    # State / introspection queries cells handle directly
    state_queries = (
        'how are you', 'how do you feel', 'what is your state',
        'are you ok', 'are you alive',
    )
    if any(q in t for q in state_queries):
        return False
    return True


def _do_research(prompt: str, *, max_questions: int = 1,
                   headless: bool = True, timeout_sec: float = 60.0,
                   engine: Any = None) -> Dict[str, Any]:
    """Call ck_research with the given prompt + budget.  Returns a dict
    with 'ok', 'crystals_added', 'elapsed_sec', and on failure 'error'."""
    t0 = time.time()
    try:
        with _RESEARCH_LOCK:
            try:
                import ck_research as _cr  # type: ignore
            except Exception as e:
                return {"ok": False, "elapsed_sec": time.time() - t0,
                        "error": f"import: {type(e).__name__}: {e}"}
            try:
                # ck_research.research is synchronous; we cap by handling
                # KeyboardInterrupt-equivalent via a thread + timeout.
                result_holder: Dict[str, Any] = {}

                def _run():
                    try:
                        out = _cr.research(prompt, engine=engine,
                                              max_questions=max_questions,
                                              headless=headless)
                        result_holder['out'] = out
                    except Exception as ex:
                        result_holder['error'] = f"{type(ex).__name__}: {ex}"

                t = threading.Thread(target=_run, daemon=True,
                                       name=f"ck_research-{int(t0)}")
                t.start()
                t.join(timeout=timeout_sec)
                if t.is_alive():
                    return {"ok": False, "elapsed_sec": time.time() - t0,
                            "error": f"timeout after {timeout_sec}s"}
                if 'error' in result_holder:
                    return {"ok": False, "elapsed_sec": time.time() - t0,
                            "error": result_holder['error']}
                out = result_holder.get('out', {})
                crystals = int(out.get('crystals_added', 0)
                                or out.get('n_crystals', 0) or 0)
                return {"ok": True, "elapsed_sec": time.time() - t0,
                        "crystals_added": crystals,
                        "synthesis_preview": str(out.get('synthesis', ''))[:200],
                        "questions_asked": out.get('questions', []),
                        }
            except Exception as e:
                return {"ok": False, "elapsed_sec": time.time() - t0,
                        "error": f"{type(e).__name__}: {e}"}
    except Exception as e:
        return {"ok": False, "elapsed_sec": time.time() - t0,
                "error": f"outer: {type(e).__name__}: {e}"}


def install_research_first_observer(api, engine, *, mode: str = "fast"):
    """Wrap api.process_chat so research runs BEFORE the inner chat path.

    Mode options (per CK_RESEARCH_MODE env var):
      'off'     -- skip pre-research (returns inner unchanged)
      'fast'    -- max_questions=1, headless=True, 60s timeout (default)
      'full'    -- max_questions=4, headless=True, 5min timeout
      'visible' -- max_questions=2, headless=False (Brayden watches)

    Side effects: each call logs to Gen13/var/research_first_logs/.
    The research findings flow into engine.olfactory.absorb_ops via
    ck_research's own ingest pipeline.
    """
    if mode == "off":
        print(f"[CK] research_first: OFF (CK_RESEARCH_MODE=off)")
        return False

    inner = api.process_chat

    if mode == "full":
        max_q, headless, timeout = 4, True, 300.0
    elif mode == "visible":
        max_q, headless, timeout = 2, False, 180.0
    else:  # fast (default)
        max_q, headless, timeout = 1, True, 60.0

    def _process_chat_with_research_first(session_id, text, mode_arg='normal'):
        research_meta: Dict[str, Any] = {"skipped": False}
        if not _should_research(text):
            research_meta["skipped"] = True
            research_meta["reason"] = "trivial_or_state_query"
        else:
            try:
                research_meta = _do_research(text, max_questions=max_q,
                                                headless=headless,
                                                timeout_sec=timeout,
                                                engine=engine)
                _log_event("research_run",
                              prompt=text[:200],
                              ok=research_meta.get('ok'),
                              elapsed_sec=research_meta.get('elapsed_sec'),
                              crystals_added=research_meta.get('crystals_added', 0),
                              error=research_meta.get('error'))
            except Exception as e:
                research_meta = {"ok": False, "error": f"{type(e).__name__}: {e}"}
                _log_event("research_exception",
                              prompt=text[:200],
                              error=str(e))

        # Now run the inner chat path (cortex shaped by research)
        result = inner(session_id, text, mode=mode_arg)
        # Surface research metadata in the response
        result['research_first'] = research_meta
        return result

    api.process_chat = _process_chat_with_research_first
    print(f"[CK] research_first: INSTALLED  mode={mode}  "
            f"max_questions={max_q}  headless={headless}  "
            f"timeout={timeout}s  log={_today_log()}")
    return True


if __name__ == "__main__":
    # Quick test (requires running Chrome + allowlist sites)
    print(f"_should_research('hi'): {_should_research('hi')}")
    print(f"_should_research('what is sigma rate'): {_should_research('what is sigma rate')}")
    print(f"log dir: {LOG_DIR}")
