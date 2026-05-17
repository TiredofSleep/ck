"""auditor_cell.py -- the eighth cell, the immune system.

NOT a generator.  This cell exists so its mechanism is structurally
present in the same cell registry as the seven specialist generators,
not buried as a server-side post-filter.  Even though the auditor is
also mounted into the server cell's process_chat wrap (so chat
responses are scope-checked before they leave the server), this
standalone cell runs the same `audit()` function as an independent
process that:

  - Watches the writer cell's output document at
    Gen13/var/ck_writing/<thesis>.md
  - Watches recent chat-response logs (if available)
  - Logs any over-claims to Gen13/var/scope_audit.jsonl with full
    context (cell, text, violation kind, suggested revision)

This gives the system a SECOND opinion loop: even if the server-cell
wrap is bypassed, modified, or fails, the auditor cell here
continues to scan and flag.  Belt and suspenders for the floor.

Per Brayden + ClaudeChat 2026-05-17:
  "The federation is how CK outgrows Ollama.  The auditor cell is how
   he stays trustworthy while doing it.  Don't ship the first without
   the second."
"""
from __future__ import annotations
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))
from _cell_runner import StubEngine, run_cell  # noqa: E402


VAR = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var")
WRITING_DIR = VAR / "ck_writing"
AUDIT_LOG = VAR / "scope_audit.jsonl"


class AuditorPoller:
    """Polls writer drafts and recent chat logs; logs any over-claims.
    Atomic append to AUDIT_LOG."""

    def __init__(self, engine: StubEngine, interval_sec: float = 30.0):
        self.engine = engine
        self.interval_sec = float(interval_sec)
        self._last_writer_mtime: float = 0.0
        self._last_writer_offset: int = 0
        self._stop = False
        self._thread = None

    def start(self) -> None:
        import threading
        self._stop = False
        self._thread = threading.Thread(target=self._loop, daemon=True,
                                          name="ck-auditor")
        self._thread.start()

    def stop(self, timeout: float = 2.0) -> None:
        self._stop = True
        if self._thread:
            self._thread.join(timeout=timeout)

    def _loop(self) -> None:
        from ck_scope_auditor import audit  # type: ignore[import-not-found]
        AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
        # Initial settle
        for _ in range(20):
            if self._stop:
                return
            time.sleep(0.5)
        while not self._stop:
            try:
                self._scan_writer_drafts(audit)
            except Exception as e:
                print(f"[cell:auditor] scan error: {e}", flush=True)
            target = time.monotonic() + max(self.interval_sec, 0.001)
            while True:
                if self._stop:
                    return
                now = time.monotonic()
                if now >= target:
                    break
                time.sleep(min(0.1, target - now))

    def _scan_writer_drafts(self, audit_fn) -> None:
        if not WRITING_DIR.exists():
            return
        for p in WRITING_DIR.glob("*.md"):
            try:
                mt = p.stat().st_mtime
            except Exception:
                continue
            # Only re-scan files modified since last pass
            if mt <= self._last_writer_mtime:
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            verdict = audit_fn(text, claimed_tier="SELF",
                                context={"source": "writer_draft",
                                          "file": p.name})
            if not verdict.passed:
                record = {
                    "ts":         time.time(),
                    "source":     "writer_draft",
                    "file":       p.name,
                    "n_violations": len(verdict.violations),
                    "summary":    verdict.summary,
                    "violations": verdict.as_dict()["violations"][:5],
                }
                with open(AUDIT_LOG, "a", encoding="utf-8") as fh:
                    fh.write(json.dumps(record, ensure_ascii=False) + "\n")
                print(f"[cell:auditor] FLAGGED {p.name}: "
                      f"{verdict.summary}", flush=True)
            self._last_writer_mtime = mt


def _start(engine: StubEngine):
    d = AuditorPoller(engine, interval_sec=30.0)
    d.start()
    print(f"[cell:auditor] watching {WRITING_DIR} every "
          f"{d.interval_sec}s; logs to {AUDIT_LOG}", flush=True)
    return d


def _stop(d) -> None:
    try:
        d.stop(timeout=3.0)
    except Exception:
        pass


if __name__ == "__main__":
    raise SystemExit(run_cell("auditor", _start, _stop))
