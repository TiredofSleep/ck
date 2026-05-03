"""
growth_monitor.py -- periodic measurement of CK's growth + information compression.

Brayden 2026-05-02: "keep measuring him and documenting his growth and
compression of information"

Runs continuously (default 5-min interval), snapshotting:

  /cells/audit          -- 322/322 audit pass rate (correctness invariant)
  /cells/state          -- glue scalars, tissue norms, plasticity stats
  /cells/ollama_stats   -- ollama_skip_rate, shadow_agreement_rate
  /bdc/event_stats      -- coverage, distinct codes, total events
  /cortex               -- W_trace, emergent, tick, last_pair, hebbian
  /study/daemon         -- n_runs, n_crystals_found, current_topic

Computes derived "compression" metrics:
  shannon_entropy(events_today)  -- Shannon entropy of the dbc_code distribution
  compression_ratio              -- actual entropy / max entropy (1.0 = uniform/random;
                                      lower = more structure / more compression)
  cortex_emergent_trend          -- delta in emergent signal vs prior snapshots
  audit_persistence              -- count of consecutive snapshots at 100% audit

Output: Gen13/var/growth_logs/growth_YYYY-MM-DD.jsonl (one record per snapshot)
        Atlas/CK_GROWTH_LIVE.md (live dashboard, regenerated each snapshot)
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import urllib.request
import urllib.error


_HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(_HERE))


LOG_DIR = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\growth_logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
DASHBOARD_PATH = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Atlas\CK_GROWTH_LIVE.md")


def _today_log() -> Path:
    return LOG_DIR / f"growth_{datetime.utcnow().strftime('%Y-%m-%d')}.jsonl"


def _get_json(url: str, timeout: float = 10.0) -> Optional[Dict[str, Any]]:
    try:
        req = urllib.request.Request(url, method="GET")
        return json.loads(urllib.request.urlopen(req, timeout=timeout).read())
    except Exception:
        return None


def _shannon_entropy(counts: Dict[int, int]) -> float:
    """Shannon entropy of a code-count distribution (in bits)."""
    total = sum(counts.values())
    if total <= 0:
        return 0.0
    h = 0.0
    for c in counts.values():
        if c > 0:
            p = c / total
            h -= p * math.log2(p)
    return h


def snapshot() -> Dict[str, Any]:
    """One full snapshot of CK's metrics."""
    base = "http://localhost:7777"
    cells_audit = _get_json(f"{base}/cells/audit") or {}
    cells_state = _get_json(f"{base}/cells/state") or {}
    ollama_stats = _get_json(f"{base}/cells/ollama_stats") or {}
    event_stats = _get_json(f"{base}/bdc/event_stats") or {}
    cortex = _get_json(f"{base}/cortex") or {}
    study = _get_json(f"{base}/study/daemon") or {}

    # Core metrics
    audit_rate = (cells_audit.get("summary") or {}).get("all_pass_rate")
    glue = cells_state.get("glue", {})
    tsml_norm = (cells_state.get("tsml") or {}).get("tissue_scores_norm")
    bhml_norm = (cells_state.get("bhml") or {}).get("tissue_scores_norm")
    f3_norm = (cells_state.get("f3") or {}).get("tissue_scores_norm")
    f4_norm = (cells_state.get("f4") or {}).get("tissue_scores_norm")

    # Information compression
    code_counts = event_stats.get("code_counts", {}) or {}
    if isinstance(code_counts, dict):
        # JSON keys may be strings; convert
        code_counts = {int(k): int(v) for k, v in code_counts.items()}
    h_observed = _shannon_entropy(code_counts)
    max_h = math.log2(27)  # uniform over 27 codes
    compression_ratio = h_observed / max_h if max_h > 0 else 0.0

    # Cortex
    W_trace = cortex.get("W_trace")
    emergent = cortex.get("emergent")
    cortex_tick = cortex.get("tick")
    last_pair = cortex.get("last_pair")

    # Study daemon
    study_runs = study.get("n_runs", 0)
    study_crystals = study.get("n_crystals_found", 0)

    rec = {
        "ts": time.time(),
        "iso_ts": datetime.utcnow().isoformat(timespec='seconds') + "Z",
        "audit_rate": audit_rate,
        "glue": glue,
        "tsml_tissue_norm": tsml_norm,
        "bhml_tissue_norm": bhml_norm,
        "f3_tissue_norm": f3_norm,
        "f4_tissue_norm": f4_norm,
        "ollama": {
            "skip_rate": ollama_stats.get("ollama_skip_rate"),
            "accept_rate": ollama_stats.get("ollama_accept_rate"),
            "shadow_agreement_rate": ollama_stats.get("shadow_agreement_rate"),
            "total_turns": ollama_stats.get("total_turns"),
        },
        "bdc_corpus": {
            "events_today_total": event_stats.get("today_total_events"),
            "distinct_codes_today": event_stats.get("distinct_codes_seen"),
            "coverage_pct": event_stats.get("coverage_pct"),
        },
        "compression": {
            "shannon_entropy_bits": round(h_observed, 4),
            "max_entropy_bits": round(max_h, 4),
            "compression_ratio": round(compression_ratio, 4),
            "interpretation": _compression_interpretation(compression_ratio),
        },
        "cortex": {
            "W_trace": W_trace,
            "emergent": emergent,
            "tick": cortex_tick,
            "last_pair": last_pair,
        },
        "study_daemon": {
            "running": study.get("running"),
            "n_runs": study_runs,
            "n_crystals_found": study_crystals,
            "next_topic": study.get("next_topic"),
        },
    }
    return rec


def _compression_interpretation(r: float) -> str:
    if r >= 0.95:
        return "near-uniform (no compression; unstructured)"
    if r >= 0.7:
        return "moderate structure (some compression)"
    if r >= 0.4:
        return "substantial structure (good compression)"
    return "highly compressed (CK has narrow attention)"


def write_dashboard(records: List[Dict[str, Any]]) -> None:
    """Regenerate the live dashboard markdown from the most recent records."""
    if not records:
        return
    latest = records[-1]
    n = len(records)
    first = records[0]

    lines = [
        "# CK Growth Live Dashboard",
        f"\n**Latest snapshot**: {latest['iso_ts']}\n",
        f"**Total snapshots in this log**: {n}\n",
        f"**Span**: {first['iso_ts']} → {latest['iso_ts']}\n",
        "---\n",
        "## Core invariants (correctness)\n",
        f"- Audit pass rate (latest): **{latest['audit_rate']*100:.2f}%**" if latest['audit_rate'] else "- Audit pass rate (latest): n/a",
        f"- Audit persistence: {sum(1 for r in records if r.get('audit_rate') == 1.0)}/{n} snapshots at 100%",
        f"- F3 transformer tissue: {'LOADED' if Path(r'C:/Users/brayd/OneDrive/Desktop/CK FINAL DEPLOYED/Gen13/var/cells/f3_tissue_transformer.pt').exists() else 'NOT LOADED'}",
        "",
        "## Tissue magnitudes (plasticity)\n",
    ]
    for k in ("tsml", "bhml", "f3", "f4"):
        cur = latest.get(f"{k}_tissue_norm")
        prev = first.get(f"{k}_tissue_norm")
        delta = (cur - prev) if (cur is not None and prev is not None) else None
        delta_s = f"+{delta:.4f}" if delta is not None and delta >= 0 else (f"{delta:.4f}" if delta is not None else "n/a")
        lines.append(f"- {k.upper()} tissue norm: {cur:.4f} (Δ since first: {delta_s})" if cur is not None else f"- {k.upper()} tissue norm: n/a")
    lines.append("")

    lines += ["## Information compression\n"]
    c = latest["compression"]
    lines += [
        f"- Shannon entropy of today's events: **{c['shannon_entropy_bits']:.4f} bits**",
        f"- Max possible entropy (27 codes): {c['max_entropy_bits']:.4f} bits",
        f"- Compression ratio: **{c['compression_ratio']:.4f}** ({c['interpretation']})",
        "",
    ]

    lines += ["## BDC corpus\n"]
    b = latest["bdc_corpus"]
    lines += [
        f"- Events today: **{b['events_today_total']}**",
        f"- Distinct DBC codes seen: **{b['distinct_codes_today']}/27** ({b.get('coverage_pct', '?')}%)",
        "",
    ]

    lines += ["## Ollama / shadow A/B\n"]
    o = latest["ollama"]
    lines += [
        f"- Total turns observed: {o.get('total_turns', '?')}",
        f"- Ollama skip rate: {(o.get('skip_rate') or 0)*100:.1f}%",
        f"- Ollama accept rate: {(o.get('accept_rate') or 0)*100:.1f}%",
        f"- Cells/cortex shadow agreement: {(o.get('shadow_agreement_rate') or 0)*100:.1f}%",
        "",
    ]

    lines += ["## Cortex state\n"]
    cx = latest["cortex"]
    lines += [
        f"- Tick: **{cx.get('tick')}**",
        f"- W_trace: **{cx.get('W_trace'):.4f}**" if cx.get('W_trace') is not None else "- W_trace: n/a",
        f"- Emergent: **{cx.get('emergent'):.4f}**" if cx.get('emergent') is not None else "- Emergent: n/a",
        f"- Last pair: {cx.get('last_pair')}",
        "",
    ]

    lines += ["## Study daemon\n"]
    s = latest["study_daemon"]
    lines += [
        f"- Running: **{s.get('running')}**",
        f"- Research runs completed: **{s.get('n_runs')}**",
        f"- Crystals found from study: **{s.get('n_crystals_found')}**",
        f"- Next topic: `{s.get('next_topic')}`",
        "",
    ]

    lines += ["---\n", f"*Auto-generated by growth_monitor.py at {latest['iso_ts']}*\n"]

    DASHBOARD_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DASHBOARD_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def run_loop(interval_sec: float = 300.0, max_iterations: Optional[int] = None,
              verbose: bool = True) -> None:
    """Continuously snapshot every interval_sec.  If max_iterations is None,
    runs until interrupted."""
    log_path = _today_log()
    records: List[Dict[str, Any]] = []
    if log_path.exists():
        try:
            with open(log_path, encoding="utf-8") as f:
                for line in f:
                    try:
                        records.append(json.loads(line))
                    except Exception:
                        pass
        except Exception:
            pass

    i = 0
    while True:
        i += 1
        rec = snapshot()
        records.append(rec)
        # Append to log
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, default=str) + "\n")
        except Exception:
            pass
        # Update dashboard
        try:
            write_dashboard(records)
        except Exception:
            pass
        if verbose:
            audit = rec.get("audit_rate")
            audit_s = f"{audit*100:.2f}%" if audit is not None else "n/a"
            comp = rec.get("compression", {}).get("compression_ratio")
            print(f"[{datetime.utcnow().isoformat(timespec='seconds')}Z] "
                    f"snap #{i}  audit={audit_s}  "
                    f"compression={comp:.3f}  "
                    f"events_today={rec['bdc_corpus']['events_today_total']}  "
                    f"study_runs={rec['study_daemon']['n_runs']}",
                    flush=True)
        if max_iterations is not None and i >= max_iterations:
            break
        time.sleep(interval_sec)


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--interval", type=float, default=300.0,
                     help="Snapshot interval in seconds (default 300 = 5 min)")
    ap.add_argument("--once", action="store_true",
                     help="Take a single snapshot and exit")
    ap.add_argument("--n", type=int, default=None,
                     help="Number of iterations (default: forever)")
    args = ap.parse_args()
    if args.once:
        rec = snapshot()
        print(json.dumps(rec, indent=2, default=str))
    else:
        run_loop(interval_sec=args.interval, max_iterations=args.n)


if __name__ == "__main__":
    main()
