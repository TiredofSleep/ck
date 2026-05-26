"""ck_daily_summary.py -- end-of-day digest combining sense + recommend + journal.

CK Gen14 bridge module — pulls together the day's PC-sense readings,
recommendations, journal entries, and rhythm into a single
end-of-day digest the user can read at a glance.

═══════════════════════════════════════════════════════════════════
What this module DOES
═══════════════════════════════════════════════════════════════════

`build_summary(date=None)` returns a structured dict with:

  - period: which day (defaults to today)
  - pc_summary:
      mean_cpu, peak_cpu, mean_mem, peak_mem
      total_readings, time_in_each_band (sec)
      dominant_operator over the day
  - recommendations:
      list of UNIQUE recommendations triggered today (dedup by code)
      with timestamps + priorities
  - journal:
      n_entries, mood_distribution, top_tags
      first_entry text + last_entry text
  - rhythm:
      n_distinct_phases_visited (out of 10)
      time_in_each_phase
  - headline: one-line plain-English summary of the day

═══════════════════════════════════════════════════════════════════
What this module DOES NOT DO
═══════════════════════════════════════════════════════════════════

  - No LLM-generated narrative (the "headline" is template-driven
    from quantitative observations).
  - No auto-emailing / Slack-posting / file-writing.  Returns a dict
    the caller renders however they want (dashboard, REST endpoint,
    CLI tool).
  - No predictions about tomorrow.

═══════════════════════════════════════════════════════════════════
Honest scope
═══════════════════════════════════════════════════════════════════

A pure aggregation primitive.  Given pc_sense_daemon + journal +
recommend functions on the engine, it produces a digest.  The
"headline" is a one-line stitched-together quantitative observation —
NOT an interpretation of meaning.
"""
from __future__ import annotations

import time
from collections import Counter
from datetime import date as _date, datetime, time as _time
from typing import Any, Dict, List, Optional


def _start_of_day(d: Optional[_date] = None) -> float:
    """Epoch seconds for 00:00:00 of given date (defaults to today)."""
    d = d or _date.today()
    return datetime.combine(d, _time.min).timestamp()


def _end_of_day(d: Optional[_date] = None) -> float:
    """Epoch seconds for 23:59:59.999999 of given date."""
    d = d or _date.today()
    return datetime.combine(d, _time.max).timestamp()


def _summarize_pc(pc_history: List[Any]) -> Dict[str, Any]:
    """Aggregate a list of PCSenseReading dataclasses."""
    if not pc_history:
        return {
            "n_readings": 0,
            "mean_cpu": 0.0,
            "peak_cpu": 0.0,
            "mean_mem": 0.0,
            "peak_mem": 0.0,
            "time_in_band": {"GREEN": 0, "YELLOW": 0, "RED": 0},
            "dominant_operator": None,
        }
    n = len(pc_history)
    cpus = [r.cpu_overall for r in pc_history]
    mems = [r.mem_used for r in pc_history]
    bands = Counter(r.coherence_band for r in pc_history)
    ops = Counter(r.op_name for r in pc_history)
    # Approximate seconds in each band (assumes ~uniform polling)
    if n >= 2:
        span = pc_history[-1].ts - pc_history[0].ts
        per_reading = span / max(1, n - 1)
    else:
        per_reading = 1.0
    return {
        "n_readings": n,
        "mean_cpu": round(sum(cpus) / n, 4),
        "peak_cpu": round(max(cpus), 4),
        "mean_mem": round(sum(mems) / n, 4),
        "peak_mem": round(max(mems), 4),
        "time_in_band_sec": {
            "GREEN": round(bands.get("GREEN", 0) * per_reading, 1),
            "YELLOW": round(bands.get("YELLOW", 0) * per_reading, 1),
            "RED": round(bands.get("RED", 0) * per_reading, 1),
        },
        "dominant_operator": ops.most_common(1)[0][0] if ops else None,
        "operator_distribution": dict(ops.most_common(5)),
    }


def _summarize_recommendations(recs: List[Any]) -> Dict[str, Any]:
    """Dedup recommendations by code, count priorities."""
    if not recs:
        return {"n_unique": 0, "by_priority": {}, "unique_codes": []}
    by_code: Dict[str, Any] = {}
    for r in recs:
        code = r.code if hasattr(r, 'code') else r.get('code', 'UNKNOWN')
        if code not in by_code:
            by_code[code] = r
    priorities = Counter(
        (r.priority if hasattr(r, 'priority') else r.get('priority', 'INFO'))
        for r in by_code.values()
    )
    return {
        "n_unique": len(by_code),
        "by_priority": dict(priorities.most_common()),
        "unique_codes": list(by_code.keys()),
    }


def _summarize_journal(entries: List[Any]) -> Dict[str, Any]:
    """Mood / tag / first-last summary."""
    if not entries:
        return {
            "n_entries": 0,
            "mood_distribution": {},
            "top_tags": {},
            "first_entry_text": None,
            "last_entry_text": None,
            "dominant_op_in_journal": None,
        }
    moods = Counter(e.mood for e in entries if e.mood)
    tag_counts: Counter = Counter()
    for e in entries:
        for t in e.tags:
            tag_counts[t] += 1
    ops = Counter(e.dominant_op_name for e in entries)
    return {
        "n_entries": len(entries),
        "mood_distribution": dict(moods.most_common(5)),
        "top_tags": dict(tag_counts.most_common(10)),
        "first_entry_text": entries[0].text[:200],
        "last_entry_text": entries[-1].text[:200],
        "dominant_op_in_journal": ops.most_common(1)[0][0] if ops else None,
    }


def _stitch_headline(pc_summary: Dict[str, Any],
                       rec_summary: Dict[str, Any],
                       journal_summary: Dict[str, Any]) -> str:
    """One-line quantitative observation. No interpretation."""
    parts: List[str] = []
    # PC fragment
    if pc_summary["n_readings"] > 0:
        parts.append(
            f"PC: dominant {pc_summary.get('dominant_operator', '?')}, "
            f"mean CPU {pc_summary['mean_cpu']*100:.0f}%, "
            f"peak {pc_summary['peak_cpu']*100:.0f}%"
        )
    # Recommendations fragment
    if rec_summary["n_unique"] > 0:
        priorities = rec_summary["by_priority"]
        n_alert = priorities.get("ALERT", 0)
        n_warn = priorities.get("WARN", 0)
        if n_alert or n_warn:
            parts.append(f"{n_alert + n_warn} priority warnings")
        else:
            parts.append(f"{rec_summary['n_unique']} info-level observations")
    # Journal fragment
    if journal_summary["n_entries"] > 0:
        parts.append(f"{journal_summary['n_entries']} journal entries")
        if journal_summary["mood_distribution"]:
            top_mood = next(iter(journal_summary["mood_distribution"]))
            parts.append(f"top mood: {top_mood}")
    if not parts:
        return "Quiet day. No PC readings, no recommendations, no journal entries."
    return " · ".join(parts)


# ─── Public API ────────────────────────────────────────────────────

def build_summary(engine: Any,
                    target_date: Optional[_date] = None) -> Dict[str, Any]:
    """Build the end-of-day digest dict.  Reads from engine.ck_pc_sense
    + engine.ck_journal + engine.ck_pc_recommend (mounted modules).

    Returns a dict suitable for JSON serialization.  Missing modules
    are reported as `null` in their section without erroring.
    """
    td = target_date or _date.today()
    start = _start_of_day(td)
    end = _end_of_day(td)
    is_today = td == _date.today()

    summary: Dict[str, Any] = {
        "period": {
            "date": td.isoformat(),
            "start_ts": start,
            "end_ts": end,
            "is_today": is_today,
            "as_of": datetime.now().isoformat(timespec="seconds"),
        },
        "pc_summary": None,
        "recommendations": None,
        "journal": None,
        "headline": None,
    }

    # PC sense
    pc_sense = getattr(engine, "ck_pc_sense", None)
    if pc_sense and pc_sense.get("daemon"):
        # daemon.history() returns the buffer; filter to target date
        all_history = pc_sense["daemon"].history()
        in_window = [r for r in all_history
                      if start <= r.ts <= end]
        summary["pc_summary"] = _summarize_pc(in_window)

    # Recommendations
    pc_recommend = getattr(engine, "ck_pc_recommend", None)
    if pc_recommend and pc_sense and pc_sense.get("daemon"):
        recs_fn = pc_recommend["recommendations_for"]
        buf = pc_sense["daemon"].history()
        in_window = [r for r in buf if start <= r.ts <= end]
        recs = recs_fn(in_window) if in_window else []
        summary["recommendations"] = _summarize_recommendations(recs)

    # Journal
    journal_api = getattr(engine, "ck_journal", None)
    if journal_api and journal_api.get("journal"):
        all_entries = journal_api["journal"]._entries
        in_window = [e for e in all_entries
                      if start <= e.ts <= end]
        summary["journal"] = _summarize_journal(in_window)

    # Headline
    summary["headline"] = _stitch_headline(
        summary.get("pc_summary") or {"n_readings": 0,
                                        "mean_cpu": 0, "peak_cpu": 0,
                                        "dominant_operator": None},
        summary.get("recommendations") or {"n_unique": 0, "by_priority": {}},
        summary.get("journal") or {"n_entries": 0, "mood_distribution": {}},
    )

    return summary


# ─── Engine mount ─────────────────────────────────────────────────

def mount_daily_summary(engine: Any) -> bool:
    """Attach summary builder + register Flask endpoint.

    Endpoints (read-only):
      GET /summary           — today's summary
      GET /summary?date=YYYY-MM-DD — specific date's summary
      GET /summary/info      — module philosophy
    """
    engine.ck_daily_summary = {
        "build_summary": build_summary,
    }

    api = getattr(engine, "web_api", None) or getattr(engine, "api", None)
    if api is not None:
        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify, request  # type: ignore

                def _summary():
                    date_str = request.args.get("date")
                    target_date = None
                    if date_str:
                        try:
                            target_date = datetime.strptime(
                                date_str, "%Y-%m-%d").date()
                        except ValueError:
                            return jsonify({
                                "ok": False,
                                "error": f"invalid date format: {date_str}; "
                                          f"use YYYY-MM-DD"
                            }), 400
                    return jsonify(build_summary(engine, target_date))

                def _info():
                    return jsonify({
                        "module": "ck_daily_summary",
                        "philosophy": ("end-of-day digest stitched from "
                                        "pc_sense + pc_recommend + journal. "
                                        "Quantitative aggregation, no LLM "
                                        "narrative."),
                        "endpoints": [
                            "GET /summary",
                            "GET /summary?date=YYYY-MM-DD",
                            "GET /summary/info",
                        ],
                    })

                existing = {r.rule for r in app.url_map.iter_rules()}
                for rule, ep, fn, methods in (
                    ("/summary",      "summary",      _summary, ["GET"]),
                    ("/summary/info", "summary_info", _info,    ["GET"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
            except Exception as e:
                print(f"[CK Gen14] mount_daily_summary: routes failed: {e}")

    print("[CK Gen14] mount_daily_summary: GET /summary endpoint ready")
    return True


# ─── CLI smoke ────────────────────────────────────────────────────

if __name__ == "__main__":
    """Smoke test using a synthetic 'engine' with the three mounted
    modules.  Verifies build_summary stitches a coherent output."""
    import sys
    import tempfile
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent))
    from ck_pc_sense import PCSenseDaemon
    from ck_pc_recommend import recommendations_for
    from ck_journal import Journal

    print("ck_daily_summary smoke test")
    print("=" * 60)
    print()

    class FakeEngine:
        pass

    eng = FakeEngine()

    # Mount fakes
    pc_daemon = PCSenseDaemon(poll_hz=2.0, buffer_size=20)
    pc_daemon.start()
    eng.ck_pc_sense = {"daemon": pc_daemon}
    eng.ck_pc_recommend = {"recommendations_for": recommendations_for}

    tmp_j = Path(tempfile.gettempdir()) / "ck_summary_smoke.jsonl"
    if tmp_j.exists():
        tmp_j.unlink()
    j = Journal(path=tmp_j)
    j.note("morning: started CK summary module", tags=["dev"], mood="focused")
    j.note("ran tests, all green", tags=["dev"], mood="satisfied")
    eng.ck_journal = {"journal": j}

    # Let sense daemon warm up
    print("Warming up sense daemon for 4 seconds...")
    time.sleep(4.0)
    pc_daemon.stop()

    # Build summary
    print()
    print("Building today's summary...")
    print("-" * 60)
    summary = build_summary(eng)
    import json as _json
    print(_json.dumps(summary, indent=2, default=str)[:2500])
    print()
    print("Headline:")
    print(f"  {summary['headline']}")
    print()
    j.clear()
    print("Smoke test complete.")
