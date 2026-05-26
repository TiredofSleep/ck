"""ck_export.py -- export today's journal+bookmarks+reminders+PC as Markdown.

CK Gen14 module — closes the loop on the daily primitives.  Everything
else CAPTURES (journal, bookmarks, reminders, PC sensing); this module
EXPORTS the day as a single human-readable Markdown file.

═══════════════════════════════════════════════════════════════════
What this module DOES
═══════════════════════════════════════════════════════════════════

`render_day_markdown(engine, target_date=None)` returns a string with:

  # CK day report — YYYY-MM-DD

  ## Headline
  PC: dominant HARMONY, mean CPU 12% · 3 journal entries · top mood: focused

  ## PC summary
  - readings: 234
  - mean CPU: 12% · peak 87%
  - mean memory: 41% · peak 52%
  - time in band: GREEN 1.2h / YELLOW 4.5h / RED 1.0h
  - dominant operator: HARMONY

  ## Recommendations (3)
  - [WARN] MEMORY_PRESSURE — Memory at 88%...
  - [NOTICE] SUSTAINED_HIGH_CPU — chrome.exe pegged...
  - [INFO] GREEN_WINDOW — All-green for 12 min...

  ## Journal (5 entries)
  ### 09:14 · HARMONY · focused · #ck #dev
  > started CK summary work
  ...

  ## Reminders (2 acknowledged, 3 pending)
  - [ACK] check the dryer (was due 14:32)
  - [DUE] call back the customer (due 16:00)
  ...

  ## Bookmarks (1 saved today)
  - [arxiv.org] Huang-Lehtonen 2022 — tags: math, paper

`write_day_file(engine, target_date=None, dest=None)` writes the
markdown to a file (default: `~/.ck/exports/YYYY-MM-DD.md`).

═══════════════════════════════════════════════════════════════════
What this module DOES NOT DO
═══════════════════════════════════════════════════════════════════

  - Never auto-emails / auto-syncs to cloud (user keeps the file).
  - Never includes content from outside today's window.
  - Never re-renders past days unless explicitly requested.

═══════════════════════════════════════════════════════════════════
Honest scope
═══════════════════════════════════════════════════════════════════

Pure formatter.  Reads the same data the daily summary endpoint
reads, but renders it as Markdown for human review / sharing.
The intended use case: end-of-day review, weekly journaling
recap (run for each day of the past week), or sharing one day's
state with a collaborator.
"""
from __future__ import annotations

from datetime import date as _date, datetime, time as _time
from pathlib import Path
from typing import Any, List, Optional


def _start_of_day(d: _date) -> float:
    return datetime.combine(d, _time.min).timestamp()


def _end_of_day(d: _date) -> float:
    return datetime.combine(d, _time.max).timestamp()


def _fmt_pct(x: float) -> str:
    return f"{x*100:.0f}%"


def _fmt_duration(sec: float) -> str:
    if sec < 60: return f"{sec:.0f}s"
    if sec < 3600: return f"{sec/60:.0f}m"
    if sec < 86400: return f"{sec/3600:.1f}h"
    return f"{sec/86400:.1f}d"


def render_day_markdown(engine: Any,
                          target_date: Optional[_date] = None) -> str:
    """Render the entire day's CK data as a single Markdown string."""
    td = target_date or _date.today()
    start = _start_of_day(td)
    end = _end_of_day(td)
    lines: List[str] = []

    lines.append(f"# CK day report — {td.isoformat()}")
    lines.append("")
    lines.append(f"*generated {datetime.now().isoformat(timespec='seconds')}*")
    lines.append("")

    # Headline (from daily_summary if available)
    headline = None
    summary_api = getattr(engine, "ck_daily_summary", None)
    if summary_api and summary_api.get("build_summary"):
        try:
            s = summary_api["build_summary"](engine, td)
            headline = s.get("headline")
        except Exception:
            pass
    if headline:
        lines.append("## Headline")
        lines.append("")
        lines.append(f"> {headline}")
        lines.append("")

    # PC summary
    pc_api = getattr(engine, "ck_pc_sense", None)
    if pc_api and pc_api.get("daemon"):
        try:
            full_history = pc_api["daemon"].history()
            history = [r for r in full_history if start <= r.ts <= end]
            if history:
                lines.append(f"## PC summary ({len(history)} readings)")
                lines.append("")
                cpus = [r.cpu_overall for r in history]
                mems = [r.mem_used for r in history]
                from collections import Counter
                bands = Counter(r.coherence_band for r in history)
                ops = Counter(r.op_name for r in history)
                span = history[-1].ts - history[0].ts if len(history) > 1 else 1
                per = span / max(1, len(history) - 1)
                lines.append(f"- mean CPU: {_fmt_pct(sum(cpus)/len(cpus))} · peak {_fmt_pct(max(cpus))}")
                lines.append(f"- mean memory: {_fmt_pct(sum(mems)/len(mems))} · peak {_fmt_pct(max(mems))}")
                lines.append(f"- time in band: "
                              f"GREEN {_fmt_duration(bands.get('GREEN',0)*per)} "
                              f"/ YELLOW {_fmt_duration(bands.get('YELLOW',0)*per)} "
                              f"/ RED {_fmt_duration(bands.get('RED',0)*per)}")
                lines.append(f"- dominant operator: **{ops.most_common(1)[0][0]}**")
                lines.append("")
        except Exception as e:
            lines.append(f"## PC summary")
            lines.append(f"")
            lines.append(f"_(error reading PC sense: {e})_")
            lines.append("")

    # Recommendations
    rec_api = getattr(engine, "ck_pc_recommend", None)
    if rec_api and pc_api and pc_api.get("daemon"):
        try:
            full = pc_api["daemon"].history()
            in_window = [r for r in full if start <= r.ts <= end]
            recs = rec_api["recommendations_for"](in_window) if in_window else []
            # dedupe by code
            seen = set()
            unique = []
            for r in recs:
                if r.code in seen: continue
                seen.add(r.code)
                unique.append(r)
            if unique:
                lines.append(f"## Recommendations ({len(unique)})")
                lines.append("")
                for r in unique:
                    lines.append(f"- **[{r.priority}]** {r.code} — {r.text}")
                lines.append("")
        except Exception as e:
            pass

    # Journal
    journal_api = getattr(engine, "ck_journal", None)
    if journal_api and journal_api.get("journal"):
        try:
            entries = [e for e in journal_api["journal"]._entries
                        if start <= e.ts <= end]
            if entries:
                lines.append(f"## Journal ({len(entries)} entries)")
                lines.append("")
                for e in entries:
                    when = datetime.fromtimestamp(e.ts).strftime("%H:%M")
                    mood = f" · {e.mood}" if e.mood else ""
                    tags = (" · " + " ".join(f"#{t}" for t in e.tags)
                             if e.tags else "")
                    lines.append(f"### {when} · {e.dominant_op_name}{mood}{tags}")
                    lines.append("")
                    for ln in e.text.splitlines():
                        lines.append(f"> {ln}")
                    lines.append("")
        except Exception as e:
            pass

    # Reminders
    rem_api = getattr(engine, "ck_reminder", None)
    if rem_api and rem_api.get("store"):
        try:
            store = rem_api["store"]
            # Reminders due/created today (covers both ack'd and pending)
            today_rems = [r for r in store._items
                           if (start <= r.created_ts <= end
                               or start <= r.due_ts <= end)]
            if today_rems:
                ack_count = sum(1 for r in today_rems if r.acknowledged)
                active_count = sum(1 for r in today_rems if not r.acknowledged)
                lines.append(f"## Reminders ({ack_count} acknowledged, {active_count} active)")
                lines.append("")
                # Sort: due first, then pending, then ack'd
                import time as _t
                now = _t.time()
                def order(r):
                    if r.acknowledged: return (2, r.due_ts)
                    if r.due_ts <= now: return (0, r.due_ts)
                    return (1, r.due_ts)
                for r in sorted(today_rems, key=order):
                    if r.acknowledged:
                        lines.append(f"- ✓ [ACK] {r.text} (was due {datetime.fromtimestamp(r.due_ts).strftime('%H:%M')})")
                    elif r.due_ts <= now:
                        lines.append(f"- ⚠ [DUE] {r.text} (due {datetime.fromtimestamp(r.due_ts).strftime('%H:%M')})")
                    else:
                        lines.append(f"- [PENDING] {r.text} (due {datetime.fromtimestamp(r.due_ts).strftime('%H:%M')})")
                lines.append("")
        except Exception as e:
            pass

    # Bookmarks
    bm_api = getattr(engine, "ck_bookmark", None)
    if bm_api and bm_api.get("store"):
        try:
            items = [b for b in bm_api["store"]._items
                      if start <= b.ts <= end]
            if items:
                lines.append(f"## Bookmarks ({len(items)} saved today)")
                lines.append("")
                for b in items:
                    title = b.title or b.url
                    tags = (" — tags: " + ", ".join(b.tags)) if b.tags else ""
                    lines.append(f"- **[{b.domain}]** [{title}]({b.url}){tags}")
                lines.append("")
        except Exception as e:
            pass

    # Footer
    lines.append("---")
    lines.append("")
    lines.append("*generated by ck_export.py · CK reports / user acts*")

    return "\n".join(lines)


def write_day_file(engine: Any,
                     target_date: Optional[_date] = None,
                     dest: Optional[Path] = None) -> Path:
    """Write today's Markdown to disk.  Returns the path written."""
    td = target_date or _date.today()
    if dest is None:
        dest = Path.home() / ".ck" / "exports" / f"{td.isoformat()}.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    md = render_day_markdown(engine, td)
    dest.write_text(md, encoding="utf-8")
    return dest


# ─── Engine mount ─────────────────────────────────────────────────

def mount_export(engine: Any) -> bool:
    """Attach the export module + register Flask endpoints.

    Endpoints:
      GET /export/md[?date=YYYY-MM-DD] — render markdown (text response)
      POST /export/write — body: {"date"?, "dest"?} — write to disk
      GET /export/info — module philosophy
    """
    engine.ck_export = {
        "render_day_markdown": render_day_markdown,
        "write_day_file": write_day_file,
    }

    api = getattr(engine, "web_api", None) or getattr(engine, "api", None)
    if api is not None:
        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify, request, Response  # type: ignore

                def _md():
                    date_str = request.args.get("date")
                    td = None
                    if date_str:
                        try:
                            td = datetime.strptime(date_str, "%Y-%m-%d").date()
                        except ValueError:
                            return jsonify({"ok": False,
                                              "error": f"invalid date: {date_str}"}), 400
                    md = render_day_markdown(engine, td)
                    return Response(md, mimetype="text/markdown")

                def _write():
                    payload = request.get_json(silent=True) or {}
                    td = None
                    if payload.get("date"):
                        try:
                            td = datetime.strptime(payload["date"], "%Y-%m-%d").date()
                        except ValueError:
                            return jsonify({"ok": False,
                                              "error": "invalid date"}), 400
                    dest = Path(payload["dest"]) if payload.get("dest") else None
                    try:
                        path = write_day_file(engine, td, dest)
                    except Exception as e:
                        return jsonify({"ok": False, "error": str(e)}), 500
                    return jsonify({"ok": True, "path": str(path),
                                      "size_bytes": path.stat().st_size})

                def _info():
                    return jsonify({
                        "module": "ck_export",
                        "philosophy": ("export today as one markdown file. "
                                        "Pure formatter; reads existing "
                                        "modules' data; never auto-syncs."),
                        "default_path": str(Path.home() / ".ck" / "exports" /
                                              "{date}.md"),
                        "endpoints": [
                            "GET /export/md[?date=YYYY-MM-DD]",
                            "POST /export/write",
                            "GET /export/info",
                        ],
                    })

                existing = {r.rule for r in app.url_map.iter_rules()}
                for rule, ep, fn, methods in (
                    ("/export/md",    "exp_md",    _md,    ["GET"]),
                    ("/export/write", "exp_write", _write, ["POST"]),
                    ("/export/info",  "exp_info",  _info,  ["GET"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
            except Exception as e:
                print(f"[CK Gen14] mount_export: routes failed: {e}")

    print(f"[CK Gen14] mount_export: GET /export/md + POST /export/write ready")
    return True


# ─── CLI smoke ────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    import tempfile

    sys.path.insert(0, str(Path(__file__).parent))
    from ck_pc_sense import PCSenseDaemon
    from ck_pc_recommend import recommendations_for
    from ck_journal import Journal
    from ck_bookmark import Bookmarks
    from ck_reminder import Reminders
    from ck_daily_summary import build_summary
    import time

    print("ck_export smoke test")
    print("=" * 60)
    print()

    class FakeEngine: pass
    eng = FakeEngine()

    # Wire up the four primitives
    pc = PCSenseDaemon(poll_hz=2.0, buffer_size=20)
    pc.start()
    eng.ck_pc_sense = {"daemon": pc}
    eng.ck_pc_recommend = {"recommendations_for": recommendations_for}
    eng.ck_daily_summary = {"build_summary": build_summary}

    tmp_j = Path(tempfile.gettempdir()) / "ck_exp_j.jsonl"
    if tmp_j.exists(): tmp_j.unlink()
    j = Journal(path=tmp_j)
    j.note("started the CK export module", tags=["dev"], mood="focused")
    j.note("tests passing across all primitives", tags=["dev"], mood="satisfied")
    eng.ck_journal = {"journal": j}

    tmp_b = Path(tempfile.gettempdir()) / "ck_exp_b.jsonl"
    if tmp_b.exists(): tmp_b.unlink()
    b = Bookmarks(path=tmp_b)
    b.add("https://github.com/TiredofSleep/ck", title="CK repo")
    eng.ck_bookmark = {"store": b}

    tmp_r = Path(tempfile.gettempdir()) / "ck_exp_r.jsonl"
    if tmp_r.exists(): tmp_r.unlink()
    r = Reminders(path=tmp_r)
    r.add("check the dryer", "5m", tags=["drycleaners"])
    r.add("done thing", time.time() - 100)
    r.acknowledge(r._items[-1].id)
    eng.ck_reminder = {"store": r}

    print("Waiting 4s for PC daemon...")
    time.sleep(4.0)
    pc.stop()

    print()
    print("=" * 60)
    print("RENDERED MARKDOWN")
    print("=" * 60)
    print(render_day_markdown(eng))

    # Cleanup
    j.clear(); b.clear(); r.clear()
