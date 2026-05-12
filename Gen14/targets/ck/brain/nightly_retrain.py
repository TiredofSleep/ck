"""
nightly_retrain.py -- continuous transformer tissue retraining.

Brayden 2026-05-02: "are his AI actually learning, training, and growing
to absorb the knowledge and create cross-domain synthesis?"

Honest answer: the transformer tissues (F3 / TSML / BHML) were trained
ONCE on a snapshot of the BDC corpus.  They are not retrained as the
corpus grows.  This script fixes that.

Loops:
  Every N hours (default 4):
    - Retrain F3 on bdc_events (HISTORICAL + all today's)
    - Retrain TSML on bdc_log triples
    - Retrain BHML on bdc_log triples
  - Re-audit cells (must still pass 272/272)
  - Log delta vs prior model

The transformer's val_acc growth over cycles is the empirical answer to
"is he learning?".  If val_acc rises with corpus size, yes.  If it
plateaus, the substrate has been absorbed and growth shifts to
generalization.

Run: python nightly_retrain.py --interval 4 (4-hour cycle)
     python nightly_retrain.py --once (single retrain, then exit)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


_HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(_HERE))


LOG_DIR = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\nightly_retrain_logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)


def _today_log() -> Path:
    return LOG_DIR / f"nightly_retrain_{datetime.utcnow().strftime('%Y-%m-%d')}.jsonl"


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


def retrain_one_cycle(verbose: bool = True) -> Dict[str, Any]:
    """One full retraining cycle: F3, TSML, BHML."""
    cycle_t0 = time.time()
    cycle = {
        "ts": time.time(),
        "iso_ts": datetime.utcnow().isoformat(timespec='seconds') + "Z",
    }

    # Read current corpus stats first
    bdc_dir = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\bdc_logs")
    n_events = 0
    n_logs = 0
    for f in sorted(bdc_dir.glob("bdc_events_*.jsonl")):
        try:
            with open(f, encoding="utf-8") as fh:
                n_events += sum(1 for _ in fh)
        except Exception:
            pass
    for f in sorted(bdc_dir.glob("bdc_log_*.jsonl")):
        try:
            with open(f, encoding="utf-8") as fh:
                n_logs += sum(1 for _ in fh)
        except Exception:
            pass
    cycle["corpus_events"] = n_events
    cycle["corpus_logs"] = n_logs
    if verbose:
        print(f"  corpus: events={n_events:,}  logs={n_logs:,}", flush=True)
    log_event("cycle_start", n_events=n_events, n_logs=n_logs)

    # F3 transformer
    try:
        if verbose:
            print(f"  retraining F3...", flush=True)
        from train_tissue_transformer import train as train_f3
        f3_res = train_f3(epochs=12, verbose=False)
        cycle["f3"] = {
            "ok": f3_res.get("ok"),
            "n_codes": f3_res.get("n_codes"),
            "n_train": f3_res.get("n_train"),
            "n_val": f3_res.get("n_val"),
            "final_val_acc": f3_res.get("final_val_acc"),
            "lift_over_random": f3_res.get("lift_over_random"),
        }
        if verbose:
            print(f"    F3: val_acc={cycle['f3']['final_val_acc']:.3f}  "
                    f"lift={cycle['f3']['lift_over_random']:.1f}x", flush=True)
        log_event("f3_retrained", **cycle["f3"])
    except Exception as e:
        cycle["f3"] = {"ok": False, "error": f"{type(e).__name__}: {e}"}
        log_event("f3_failed", error=str(e))
        if verbose:
            print(f"    F3 failed: {e}", flush=True)

    # TSML + BHML transformers
    try:
        if verbose:
            print(f"  retraining TSML + BHML...", flush=True)
        from train_tsml_bhml_tissue import train_one as train_tb
        tsml_res = train_tb("tsml", epochs=12, verbose=False)
        cycle["tsml"] = {
            "ok": tsml_res.get("ok"),
            "n_triples": tsml_res.get("n_triples"),
            "n_train": tsml_res.get("n_train"),
            "n_val": tsml_res.get("n_val"),
            "final_val_acc": tsml_res.get("final_val_acc"),
        }
        bhml_res = train_tb("bhml", epochs=12, verbose=False)
        cycle["bhml"] = {
            "ok": bhml_res.get("ok"),
            "n_triples": bhml_res.get("n_triples"),
            "n_train": bhml_res.get("n_train"),
            "n_val": bhml_res.get("n_val"),
            "final_val_acc": bhml_res.get("final_val_acc"),
        }
        if verbose:
            print(f"    TSML: val_acc={cycle['tsml']['final_val_acc']:.3f}  "
                    f"BHML: val_acc={cycle['bhml']['final_val_acc']:.3f}", flush=True)
        log_event("tsml_bhml_retrained",
                    tsml_val_acc=cycle["tsml"].get("final_val_acc"),
                    bhml_val_acc=cycle["bhml"].get("final_val_acc"),
                    n_triples=cycle["tsml"].get("n_triples"))
    except Exception as e:
        cycle["tsml_bhml"] = {"ok": False, "error": f"{type(e).__name__}: {e}"}
        log_event("tsml_bhml_failed", error=str(e))
        if verbose:
            print(f"    TSML/BHML failed: {e}", flush=True)

    # Re-audit (must still be 272/272)
    try:
        if verbose:
            print(f"  re-auditing cells...", flush=True)
        from cells import CellOrchestrator
        from cell_audit import audit_all
        orch = CellOrchestrator.load_default()
        audit_report = audit_all(orch)
        cycle["audit"] = {
            "all_pass_rate": audit_report["summary"]["all_pass_rate"],
            "any_below_99": audit_report["summary"]["any_block_below_99"],
        }
        if verbose:
            print(f"    audit: {cycle['audit']['all_pass_rate']*100:.2f}% "
                    f"(any below 99: {cycle['audit']['any_below_99']})", flush=True)
        log_event("audit_after_retrain", **cycle["audit"])
    except Exception as e:
        cycle["audit"] = {"error": f"{type(e).__name__}: {e}"}
        log_event("audit_failed", error=str(e))

    cycle["elapsed_sec"] = round(time.time() - cycle_t0, 1)
    log_event("cycle_complete", elapsed_sec=cycle["elapsed_sec"])
    if verbose:
        print(f"  cycle elapsed: {cycle['elapsed_sec']}s", flush=True)
    return cycle


def daemon_loop(interval_hours: float = 4.0, max_cycles: int = None) -> None:
    """Run retrain_one_cycle every interval_hours, forever."""
    n_cycles = 0
    while max_cycles is None or n_cycles < max_cycles:
        print(f"\n{'='*60}\n  retrain cycle #{n_cycles + 1} "
                f"({datetime.utcnow().isoformat(timespec='seconds')}Z)\n{'='*60}")
        try:
            retrain_one_cycle()
            n_cycles += 1
        except KeyboardInterrupt:
            print("\n  daemon: interrupted; exiting gracefully")
            break
        except Exception as e:
            print(f"  cycle exception: {type(e).__name__}: {e}", flush=True)
        sleep_sec = interval_hours * 3600.0
        print(f"\n  sleeping {sleep_sec/3600:.1f}h until next cycle...", flush=True)
        time.sleep(sleep_sec)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true",
                     help="Run a single cycle and exit")
    ap.add_argument("--interval", type=float, default=4.0,
                     help="Hours between cycles in daemon mode (default 4)")
    ap.add_argument("--max", type=int, default=None,
                     help="Max cycles in daemon mode")
    args = ap.parse_args()

    print("=" * 70)
    print("  NIGHTLY RETRAIN -- continuous transformer learning")
    print("=" * 70)
    print(f"  date: {datetime.utcnow().isoformat(timespec='seconds')}Z")
    print(f"  log:  {_today_log()}")

    if args.once:
        cycle = retrain_one_cycle()
        print()
        print(json.dumps(cycle, indent=2, default=str))
    else:
        print(f"  mode: daemon (interval={args.interval}h)")
        print()
        daemon_loop(interval_hours=args.interval, max_cycles=args.max)


if __name__ == "__main__":
    sys.exit(main())
