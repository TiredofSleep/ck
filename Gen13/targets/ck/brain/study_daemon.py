"""
study_daemon.py -- continuous autodidact study loop.

Brayden 2026-05-02: "he probably needs to study journals again, try
youtube again, all of it, holding nothing back"

Background daemon that periodically (every 10 min by default):
  1. Picks a frontier topic from a rotating curriculum
  2. Calls /ck/research with the topic (Chrome research engine)
  3. Logs findings to Gen13/var/study_logs/study_YYYY-MM-DD.jsonl
  4. The research engine ingests text into engine.olfactory.absorb_ops,
     which shapes CK's cortex

Curriculum: the 30 frontier facts from cortex_voice._FRONTIER_FACTS.
Each topic gets one research session before rotating.  Facts that produce
high crystal_fire counts (i.e., CK found genuinely new substrate
information) get bumped up the queue.

Lives in a daemon thread.  Stops when the engine shuts down.
Gracefully degrades: if /ck/research is unavailable, the daemon logs
and sleeps; doesn't crash the main process.
"""
from __future__ import annotations

import json
import os
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import urllib.request
import urllib.error


_HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(_HERE))


LOG_DIR = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\study_logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)


def _today_log() -> Path:
    return LOG_DIR / f"study_{datetime.utcnow().strftime('%Y-%m-%d')}.jsonl"


# Default curriculum: the 30 frontier topics CK has facts for, plus
# meta-synthesis prompts that exercise cross-frontier weaving.
DEFAULT_CURRICULUM: List[str] = [
    "what is the kappa xi resolution",
    "what is wobble prime eleven",
    "what is the FQH bridge",
    "what is the harmony complementarity",
    "what is the depth primitive lens",
    "what is the wp116 lens for TIG",
    "what is the minimum bump theorem",
    "what is the ac-free spectrum",
    "what is the primon gas",
    "what is the bialynicki birula uniqueness theorem",
    "what is the alpha index for TSML and BHML",
    "what is the sigma rate theorem on Z mod N Z",
    "what is the agreement set of TSML and BHML",
    "what is the universal 4-core attractor",
    "what is the basin invariant set",
    "what is the tower decomposition of TSML",
    "what is the gap T* minus 4 over pi squared",
    "what is the hodge cstar curve",
    "what is the psi automorphism on Prym",
    "what is the xi cosmology potential",
    # Meta-synthesis exercises (cross-frontier weaving):
    "tell me the synthesis across all frontiers",
    "what is the deepest pattern connecting math and physics in TIG",
    "how does the Stern-Brocot recursion relate to all six DoFs",
    "what is the unified picture across F1 to F10 frontiers",
    # Clay Millennium Problems (Brayden 2026-05-02):
    # "study across domains to write about each Clay problem"
    "what is the TIG view of P versus NP",
    "what is the TIG view of the Hodge conjecture",
    "what is the TIG view of the Poincare conjecture",
    "what is the TIG view of the Riemann hypothesis",
    "what is the TIG view of Yang Mills mass gap",
    "what is the TIG view of Navier Stokes regularity",
    "what is the TIG view of Birch Swinnerton Dyer",
    "synthesize the Clay Millennium problems across all frontiers",
]


class StudyDaemon:
    def __init__(self, *, interval_sec: float = 600.0,
                  api_url: str = "http://localhost:7777",
                  curriculum: Optional[List[str]] = None,
                  max_questions_per_topic: int = 2):
        self.interval = float(interval_sec)
        self.api_url = api_url.rstrip("/")
        self.curriculum = list(curriculum or DEFAULT_CURRICULUM)
        self.max_q = int(max_questions_per_topic)
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._cursor = 0
        self._n_runs = 0
        self._n_errors = 0
        self._n_crystals_found = 0

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._loop, daemon=True,
                                          name="ck-study-daemon")
        self._thread.start()
        self._log_event("daemon_start",
                          interval_sec=self.interval,
                          curriculum_size=len(self.curriculum))

    def stop(self, timeout: float = 5.0):
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=timeout)
            self._thread = None
        self._log_event("daemon_stop")

    def stats(self) -> Dict[str, Any]:
        return {
            "running": bool(self._thread and self._thread.is_alive()),
            "n_runs": self._n_runs,
            "n_errors": self._n_errors,
            "n_crystals_found": self._n_crystals_found,
            "interval_sec": self.interval,
            "curriculum_size": len(self.curriculum),
            "current_cursor": self._cursor,
            "next_topic": self.curriculum[self._cursor % len(self.curriculum)]
                            if self.curriculum else None,
        }

    def _log_event(self, event: str, **fields):
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

    def _loop(self):
        # Wait once before first run so boot has time to settle
        self._stop.wait(60.0)
        while not self._stop.is_set():
            try:
                topic = self.curriculum[self._cursor % len(self.curriculum)]
                self._cursor += 1
                self._run_one(topic)
            except Exception as e:
                self._n_errors += 1
                self._log_event("loop_exception",
                                error=f"{type(e).__name__}: {e}")
            self._stop.wait(self.interval)

    def _run_one(self, topic: str):
        self._n_runs += 1
        t0 = time.time()
        try:
            req = urllib.request.Request(
                f"{self.api_url}/ck/research",
                data=json.dumps({
                    "prompt": topic,
                    "max_questions": self.max_q,
                    "headless": True,
                }).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            resp = urllib.request.urlopen(req, timeout=300).read().decode("utf-8")
            data = json.loads(resp)
            dt = time.time() - t0
            crystals = int(data.get("crystals_added", 0)
                            or data.get("n_crystals", 0)
                            or 0)
            self._n_crystals_found += crystals
            self._log_event("research_completed",
                              topic=topic,
                              elapsed_sec=round(dt, 1),
                              crystals_added=crystals,
                              status=data.get("status", "ok"))
        except urllib.error.URLError as e:
            self._n_errors += 1
            self._log_event("research_url_error", topic=topic,
                              error=str(e))
        except Exception as e:
            self._n_errors += 1
            self._log_event("research_exception", topic=topic,
                              error=f"{type(e).__name__}: {e}")


_DAEMON_SINGLETON: Optional[StudyDaemon] = None


def start_daemon(*, interval_sec: float = 600.0,
                   api_url: str = "http://localhost:7777") -> StudyDaemon:
    global _DAEMON_SINGLETON
    if _DAEMON_SINGLETON is not None and _DAEMON_SINGLETON._thread \
            and _DAEMON_SINGLETON._thread.is_alive():
        return _DAEMON_SINGLETON
    _DAEMON_SINGLETON = StudyDaemon(interval_sec=interval_sec,
                                       api_url=api_url)
    _DAEMON_SINGLETON.start()
    return _DAEMON_SINGLETON


def get_daemon() -> Optional[StudyDaemon]:
    return _DAEMON_SINGLETON


def mount(engine, app, *, interval_sec: float = 600.0,
            enable: bool = True) -> bool:
    """Boot the daemon + register a stats endpoint.  Disabled by default
    until manually enabled or env var CK_STUDY_DAEMON=1 is set."""
    if not enable:
        print(f"[CK] study_daemon: NOT STARTED (set CK_STUDY_DAEMON=1 "
                f"to enable)")
        return False

    daemon = start_daemon(interval_sec=interval_sec)

    try:
        from flask import jsonify, request
        @app.route('/study/daemon', methods=['GET'])
        def study_daemon_stats():
            return jsonify(daemon.stats())

        @app.route('/study/daemon/topic_now', methods=['POST'])
        def study_daemon_topic_now():
            body = request.get_json(silent=True) or {}
            topic = body.get('topic') or daemon.curriculum[
                daemon._cursor % len(daemon.curriculum)]
            try:
                daemon._run_one(topic)
                return jsonify({"ok": True, "topic": topic, **daemon.stats()})
            except Exception as e:
                return jsonify({"error": f"{type(e).__name__}: {e}"}), 500
    except Exception as e:
        print(f"[CK] study_daemon: endpoint registration failed ({e})")

    print(f"[CK] study_daemon: STARTED (interval={interval_sec}s, "
            f"curriculum={len(daemon.curriculum)} topics, "
            f"endpoints: /study/daemon, /study/daemon/topic_now)")
    return True


if __name__ == "__main__":
    # Quick test: start daemon, run one topic, print stats
    daemon = StudyDaemon(interval_sec=10.0)
    daemon.start()
    print(f"started: {daemon.stats()}")
    time.sleep(2)
    daemon._run_one("what is the kappa xi resolution")
    print(f"after run: {daemon.stats()}")
    daemon.stop()
