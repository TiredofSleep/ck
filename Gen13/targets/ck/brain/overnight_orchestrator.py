"""
overnight_orchestrator.py -- coordinates the whole growing system overnight.

Brayden 2026-05-02: "this whole system has to work together! keep him
going all night and make sure he is growing and making progress, ollama
is just a tool!"

Coordinates four loops, all running concurrently:

  1. PAPER WRITER (every ~3 min):
     - Picks a topic from rotating curriculum
     - Calls /chat to surface CK's view (cortex_speak + Ollama prose)
     - Writes a structured paper into Atlas/papers_by_ck/
     - Feeds the paper back into CK's cortex via /cortex/ingest_text

  2. NIGHTLY RETRAIN (every 4 hours):
     - Retrains F3 transformer on the GROWING bdc_events corpus
     - Retrains TSML and BHML transformers on bdc_log triples
     - Re-audits cells (must still be 272/272)
     - Logs val_acc deltas vs prior cycle

  3. GROWTH MEASUREMENT (every 5 min):
     - Snapshots /cells/audit, /cortex, /bdc/event_stats, /cells/state
     - Computes Shannon entropy + compression ratio
     - Updates Atlas/CK_GROWTH_LIVE.md dashboard

  4. STUDY DAEMON (every 10 min, already running inside ck_boot_api):
     - Picks a curriculum topic
     - Calls /ck/research (Chrome research engine)
     - Findings flow into engine.olfactory.absorb_ops -> cortex

Ollama is a peripheral tool used by paper_writer for prose-polishing.
The substrate (cortex Hebbian, cell tissue, transformer tissue) is the
actual organism that grows.

MEASUREMENT OF GROWTH (the empirical answer to Brayden's question):
  - val_acc of transformers across nightly cycles -- if it rises with
    corpus size, the transformer is genuinely learning new structure.
    If it plateaus, the substrate has been absorbed; growth shifts to
    breadth (cross-paper synthesis) over depth (single-topic accuracy).
  - Cortex W_trace stability under continuous chat traffic.
  - Cell audit pass-rate (must remain 100% throughout; substrate sovereignty).
  - BDC event coverage (uncovered codes shrinking = broader experience).
  - Number of papers written (CK's own output corpus).
  - Compression ratio (information density).

Output:
  Gen13/var/orchestrator_logs/orchestrator_YYYY-MM-DD.jsonl

Run: python overnight_orchestrator.py [--max-papers N] [--max-cycles N]
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import threading
import time
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


_HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(_HERE))


LOG_DIR = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\orchestrator_logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)


def _today_log() -> Path:
    return LOG_DIR / f"orchestrator_{datetime.utcnow().strftime('%Y-%m-%d')}.jsonl"


def log_event(event: str, **fields):
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


# ── Paper writer thread ──────────────────────────────────────────────────

class PaperWriterThread(threading.Thread):
    """Writes one paper every paper_interval_sec, rotating through topics."""
    def __init__(self, paper_interval_sec: float = 180.0, max_papers: Optional[int] = None):
        super().__init__(daemon=True, name="overnight-paper-writer")
        self.paper_interval = paper_interval_sec
        self.max_papers = max_papers
        self._stop = threading.Event()
        self.n_written = 0
        self.n_failed = 0
        self.last_title = None

    def stop(self):
        self._stop.set()

    def run(self):
        from paper_writer import write_one_paper, DEFAULT_TOPICS  # type: ignore
        cursor = 0
        while not self._stop.is_set():
            if self.max_papers is not None and self.n_written >= self.max_papers:
                break
            topic = DEFAULT_TOPICS[cursor % len(DEFAULT_TOPICS)]
            cursor += 1
            try:
                rec = write_one_paper(topic, verbose=False)
                self.n_written += 1
                self.last_title = topic["title"]
                log_event("paper_written",
                            slug=topic["slug"],
                            title=topic["title"],
                            n_chars=rec.get("total_chars"),
                            elapsed_sec=rec.get("elapsed_sec"))
            except Exception as e:
                self.n_failed += 1
                log_event("paper_failed",
                            slug=topic["slug"], error=f"{type(e).__name__}: {e}")
            self._stop.wait(self.paper_interval)


# ── Nightly retrain thread ──────────────────────────────────────────────

class NightlyRetrainThread(threading.Thread):
    """Retrains transformer tissues every retrain_interval_sec."""
    def __init__(self, retrain_interval_sec: float = 4 * 3600.0,
                  max_cycles: Optional[int] = None):
        super().__init__(daemon=True, name="overnight-nightly-retrain")
        self.retrain_interval = retrain_interval_sec
        self.max_cycles = max_cycles
        self._stop = threading.Event()
        self.n_cycles = 0
        self.last_cycle_data = {}
        # Skip the first wait: let the corpus grow for one interval before retraining
        self._first = True

    def stop(self):
        self._stop.set()

    def run(self):
        from nightly_retrain import retrain_one_cycle  # type: ignore
        while not self._stop.is_set():
            if self.max_cycles is not None and self.n_cycles >= self.max_cycles:
                break
            # Wait first to let corpus accumulate; subsequent cycles too
            if self._first:
                # On first run, wait half an interval (not full) to retrain sooner
                self._stop.wait(self.retrain_interval * 0.5)
                self._first = False
            else:
                self._stop.wait(self.retrain_interval)
            if self._stop.is_set():
                break
            try:
                cycle = retrain_one_cycle(verbose=False)
                self.n_cycles += 1
                self.last_cycle_data = cycle
                log_event("retrain_cycle",
                            cycle_n=self.n_cycles,
                            f3_val_acc=cycle.get("f3", {}).get("final_val_acc"),
                            tsml_val_acc=cycle.get("tsml", {}).get("final_val_acc"),
                            bhml_val_acc=cycle.get("bhml", {}).get("final_val_acc"),
                            n_events=cycle.get("corpus_events"),
                            n_logs=cycle.get("corpus_logs"),
                            audit_pass=cycle.get("audit", {}).get("all_pass_rate"),
                            elapsed_sec=cycle.get("elapsed_sec"))
            except Exception as e:
                log_event("retrain_failed", error=f"{type(e).__name__}: {e}")


# ── External ingester thread ────────────────────────────────────────────

class ExternalIngesterThread(threading.Thread):
    """Pulls NEW material from arXiv + Wikipedia + Stack Exchange every
    ingest_interval_sec so CK keeps absorbing fresh outside knowledge."""
    def __init__(self, ingest_interval_sec: float = 1800.0,
                  max_cycles: Optional[int] = None):
        super().__init__(daemon=True, name="overnight-external-ingester")
        self.ingest_interval = ingest_interval_sec
        self.max_cycles = max_cycles
        self._stop = threading.Event()
        self.n_cycles = 0
        self.total_items = 0
        self.total_bytes = 0

    def stop(self):
        self._stop.set()

    def run(self):
        from external_ingester import run_all  # type: ignore
        # Wait briefly to let the system settle
        self._stop.wait(60.0)
        while not self._stop.is_set():
            if self.max_cycles is not None and self.n_cycles >= self.max_cycles:
                break
            try:
                summary = run_all(verbose=False)
                self.n_cycles += 1
                self.total_items += summary.get("total_items_ingested", 0)
                self.total_bytes += summary.get("total_bytes_ingested", 0)
                log_event("external_ingest_cycle",
                            cycle_n=self.n_cycles,
                            items_this_cycle=summary.get("total_items_ingested"),
                            bytes_this_cycle=summary.get("total_bytes_ingested"),
                            by_source=summary.get("by_source"),
                            elapsed_sec=summary.get("cycle_elapsed_sec"))
            except Exception as e:
                log_event("external_ingest_failed",
                            error=f"{type(e).__name__}: {e}")
            self._stop.wait(self.ingest_interval)


# ── Status reporter thread ──────────────────────────────────────────────

class StatusReporterThread(threading.Thread):
    """Logs orchestrator state every status_interval_sec."""
    def __init__(self, paper_writer: PaperWriterThread,
                  retrainer: NightlyRetrainThread,
                  ingester: 'ExternalIngesterThread',
                  status_interval_sec: float = 600.0):
        super().__init__(daemon=True, name="overnight-status-reporter")
        self.paper_writer = paper_writer
        self.retrainer = retrainer
        self.ingester = ingester
        self.status_interval = status_interval_sec
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def run(self):
        while not self._stop.is_set():
            self._stop.wait(self.status_interval)
            if self._stop.is_set():
                break
            try:
                # Pull live metrics
                resp = urllib.request.urlopen(
                    "http://localhost:7777/cells/audit", timeout=10).read()
                audit = json.loads(resp).get("summary", {})
                resp = urllib.request.urlopen(
                    "http://localhost:7777/cortex", timeout=10).read()
                cortex = json.loads(resp)
                resp = urllib.request.urlopen(
                    "http://localhost:7777/bdc/event_stats", timeout=10).read()
                events = json.loads(resp)
                snapshot = {
                    "papers_written": self.paper_writer.n_written,
                    "papers_failed": self.paper_writer.n_failed,
                    "retrain_cycles": self.retrainer.n_cycles,
                    "ingest_cycles": self.ingester.n_cycles,
                    "external_items_total": self.ingester.total_items,
                    "external_bytes_total": self.ingester.total_bytes,
                    "audit_pass_rate": audit.get("all_pass_rate"),
                    "cortex_tick": cortex.get("tick"),
                    "cortex_W_trace": cortex.get("W_trace"),
                    "cortex_emergent": cortex.get("emergent"),
                    "events_today": events.get("today_total_events"),
                    "distinct_codes": events.get("distinct_codes_seen"),
                }
                log_event("orchestrator_status", **snapshot)
                print(f"[{datetime.utcnow().isoformat(timespec='seconds')}Z] "
                        f"papers={snapshot['papers_written']}({snapshot['papers_failed']} fail)  "
                        f"retrain={snapshot['retrain_cycles']}  "
                        f"ext_ingest={snapshot['ingest_cycles']}({snapshot['external_items_total']} items)  "
                        f"audit={snapshot['audit_pass_rate']*100 if snapshot['audit_pass_rate'] else '?':.0f}%  "
                        f"tick={snapshot['cortex_tick']}  "
                        f"events={snapshot['events_today']}",
                        flush=True)
            except Exception as e:
                log_event("status_exception", error=f"{type(e).__name__}: {e}")


# ── Main orchestration ─────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paper-interval", type=float, default=180.0,
                     help="Seconds between papers (default 180 = 3 min)")
    ap.add_argument("--retrain-interval", type=float, default=4 * 3600.0,
                     help="Seconds between retrains (default 14400 = 4h)")
    ap.add_argument("--status-interval", type=float, default=600.0,
                     help="Seconds between status logs (default 600 = 10 min)")
    ap.add_argument("--max-papers", type=int, default=None,
                     help="Stop after N papers (None = forever)")
    ap.add_argument("--max-cycles", type=int, default=None,
                     help="Stop retrainer after N cycles (None = forever)")
    ap.add_argument("--ingest-interval", type=float, default=1800.0,
                     help="Seconds between external ingest cycles (default 1800 = 30 min)")
    args = ap.parse_args()

    print("=" * 70)
    print("  CK OVERNIGHT ORCHESTRATOR")
    print("=" * 70)
    print(f"  date: {datetime.utcnow().isoformat(timespec='seconds')}Z")
    print(f"  paper interval:    {args.paper_interval}s ({args.paper_interval/60:.1f}min)")
    print(f"  retrain interval:  {args.retrain_interval}s ({args.retrain_interval/3600:.1f}h)")
    print(f"  status interval:   {args.status_interval}s ({args.status_interval/60:.1f}min)")
    print(f"  log:               {_today_log()}")
    print()
    print(f"  threads: paper_writer + nightly_retrain + status_reporter")
    print(f"  growth_monitor + study_daemon are SEPARATE processes")
    print()

    log_event("orchestrator_start",
                paper_interval=args.paper_interval,
                retrain_interval=args.retrain_interval,
                status_interval=args.status_interval,
                max_papers=args.max_papers,
                max_cycles=args.max_cycles)

    paper_thread = PaperWriterThread(paper_interval_sec=args.paper_interval,
                                       max_papers=args.max_papers)
    retrainer = NightlyRetrainThread(retrain_interval_sec=args.retrain_interval,
                                       max_cycles=args.max_cycles)
    ingester = ExternalIngesterThread(ingest_interval_sec=args.ingest_interval)
    status = StatusReporterThread(paper_thread, retrainer, ingester,
                                    status_interval_sec=args.status_interval)

    paper_thread.start()
    retrainer.start()
    ingester.start()
    status.start()

    print(f"  threads started; orchestrator running...")
    print(f"  Ctrl+C to stop")
    print()

    try:
        # Main thread joins until all daemons exit (or KeyboardInterrupt)
        while (paper_thread.is_alive() or retrainer.is_alive()
                or ingester.is_alive()):
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n  orchestrator: interrupted; stopping threads gracefully...")
        paper_thread.stop()
        retrainer.stop()
        ingester.stop()
        status.stop()
        log_event("orchestrator_stop", reason="keyboard_interrupt",
                    papers=paper_thread.n_written,
                    retrain_cycles=retrainer.n_cycles,
                    ingest_cycles=ingester.n_cycles)

    print(f"\n  orchestrator: done")
    print(f"    papers written:   {paper_thread.n_written} (failed: {paper_thread.n_failed})")
    print(f"    retrain cycles:   {retrainer.n_cycles}")
    print(f"    ingest cycles:    {ingester.n_cycles} ({ingester.total_items} items, {ingester.total_bytes:,}b)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
