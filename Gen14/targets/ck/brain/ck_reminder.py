"""ck_reminder.py -- gentle time-based reminders.

CK Gen14 module — append a reminder ("remind me to X at T"); CK keeps
the list, marks them due as time passes; the user reads the due list
from the dashboard / API.  CK does NOT send notifications, alerts, or
any push — pull-only.  User decides when to check.

═══════════════════════════════════════════════════════════════════
What this module DOES
═══════════════════════════════════════════════════════════════════

`add(text, when, tags=None)` — append a reminder.
  - text:  what to remind about
  - when:  an absolute timestamp (epoch), an ISO datetime string,
           OR a relative spec like "30m" / "1h" / "2h30m" / "tomorrow at 9am"
  - tags:  optional list
  Returns a Reminder dataclass with computed due_ts.

`due(now=None)` — reminders whose due_ts <= now.
`pending(now=None)` — reminders not yet due.
`all_active()` — active (not-yet-acknowledged) reminders.
`acknowledge(id_)` — mark a reminder as acknowledged (still in the
  log; just won't show up in due() any more).
`recent(n=20)` — last N reminders (any state).

═══════════════════════════════════════════════════════════════════
What this module DOES NOT DO
═══════════════════════════════════════════════════════════════════

  - Never sends notifications (no email, no Slack, no toast, no
    audible alert).  PULL-ONLY: the user checks the due list.
  - Never auto-deletes reminders (append-only + acknowledge state).
  - Never runs any user-supplied code.
  - No outbound network calls.

═══════════════════════════════════════════════════════════════════
Honest scope
═══════════════════════════════════════════════════════════════════

This is the simplest possible reminder primitive — a JSONL file
with (id, text, due_ts, ack) tuples.  The user pulls the due list
when they remember to look (via the dashboard).  Push notifications
require OS integration (Windows Toast, macOS Notification Center,
Linux libnotify) which violates the "no actuator" discipline; if
push notifications matter, wrap this module's `due()` output with
a separate script the user opts into.
"""
from __future__ import annotations

import json
import re
import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional


DEFAULT_REMINDERS_PATH = Path.home() / ".ck" / "reminders.jsonl"


@dataclass
class Reminder:
    """One reminder entry."""
    id: str                          # uuid4 hex
    text: str
    due_ts: float                    # epoch seconds when reminder is due
    due_iso: str                     # ISO string for display
    created_ts: float
    created_iso: str
    tags: List[str] = field(default_factory=list)
    acknowledged: bool = False
    ack_ts: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ─── Relative-spec parsing ────────────────────────────────────────

_REL_RE = re.compile(r"""
    ^\s*
    (?:(?P<days>\d+)\s*d(?:ay(?:s)?)?)?\s*
    (?:(?P<hours>\d+)\s*h(?:our(?:s)?)?)?\s*
    (?:(?P<minutes>\d+)\s*m(?:in(?:ute(?:s)?)?)?)?\s*
    (?:(?P<seconds>\d+)\s*s(?:ec(?:ond(?:s)?)?)?)?\s*$
""", re.VERBOSE | re.IGNORECASE)


def parse_when(when: Any, now: Optional[float] = None) -> float:
    """Parse a 'when' value into an absolute epoch timestamp.

    Accepts:
      - float / int: epoch seconds (returned as-is)
      - ISO datetime string ("2026-05-19T14:30:00" or "2026-05-19 14:30")
      - relative string: "30m", "1h", "2h30m", "1d4h", "45s", "1h 15m"
      - keywords: "tomorrow at 9am", "tonight at 8pm" (simple)

    Raises ValueError on unparseable input.
    """
    now = now if now is not None else time.time()
    if isinstance(when, (int, float)):
        return float(when)
    if not isinstance(when, str):
        raise ValueError(f"when must be number or string, got {type(when).__name__}")
    w = when.strip()
    if not w:
        raise ValueError("when string is empty")

    # ISO datetime?
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S",
                 "%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"):
        try:
            dt = datetime.strptime(w, fmt)
            return dt.timestamp()
        except ValueError:
            pass

    # "tomorrow at 9am" / "tonight at 8pm" / "today at 5pm"
    m = re.match(r"^(tomorrow|tonight|today)\s+at\s+(\d{1,2})(?:[: ]?(\d{2}))?\s*(am|pm)?\s*$", w, re.I)
    if m:
        day, hr, mn, ampm = m.groups()
        hr = int(hr)
        mn = int(mn) if mn else 0
        if ampm:
            if ampm.lower() == "pm" and hr < 12: hr += 12
            if ampm.lower() == "am" and hr == 12: hr = 0
        elif day.lower() == "tonight" and hr < 12:
            hr += 12
        base = datetime.now()
        if day.lower() in ("tomorrow",):
            base = base + timedelta(days=1)
        target = base.replace(hour=hr, minute=mn, second=0, microsecond=0)
        return target.timestamp()

    # Relative spec
    m = _REL_RE.match(w)
    if m and any(m.group(k) for k in ("days", "hours", "minutes", "seconds")):
        delta = (
            int(m.group("days") or 0) * 86400 +
            int(m.group("hours") or 0) * 3600 +
            int(m.group("minutes") or 0) * 60 +
            int(m.group("seconds") or 0)
        )
        if delta == 0:
            raise ValueError(f"zero-delta relative spec: {w!r}")
        return now + delta

    raise ValueError(
        f"could not parse {w!r} as datetime, "
        f"relative spec ('30m', '2h30m', '1d4h'), "
        f"or natural phrase ('tomorrow at 9am')"
    )


# ─── Reminders class ──────────────────────────────────────────────

class Reminders:
    """Persistent append-only reminders store."""

    def __init__(self, path: Optional[Path] = None):
        self.path = path or DEFAULT_REMINDERS_PATH
        self._items: List[Reminder] = []
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        try:
            with open(self.path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        d = json.loads(line)
                        self._items.append(Reminder(**d))
                    except Exception:
                        continue
        except Exception:
            pass
        # Sort by due_ts ascending
        self._items.sort(key=lambda r: r.due_ts)

    def _append_raw(self, r: Reminder) -> None:
        """Append a fresh reminder to the log."""
        self._items.append(r)
        self._items.sort(key=lambda x: x.due_ts)
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(json.dumps(r.to_dict(), ensure_ascii=False) + "\n")
        except Exception:
            pass

    def _rewrite_log(self) -> None:
        """Rewrite the entire log (used after acknowledge)."""
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self.path.with_suffix(self.path.suffix + ".tmp")
            with open(tmp, "w", encoding="utf-8") as f:
                for r in self._items:
                    f.write(json.dumps(r.to_dict(),
                                        ensure_ascii=False) + "\n")
            tmp.replace(self.path)
        except Exception:
            pass

    def add(self, text: str, when: Any,
              tags: Optional[List[str]] = None) -> Reminder:
        if not text or not str(text).strip():
            raise ValueError("text is required and must be non-empty")
        due_ts = parse_when(when)
        now = time.time()
        r = Reminder(
            id=uuid.uuid4().hex[:12],
            text=str(text).strip(),
            due_ts=due_ts,
            due_iso=datetime.fromtimestamp(due_ts).isoformat(timespec="seconds"),
            created_ts=now,
            created_iso=datetime.fromtimestamp(now).isoformat(timespec="seconds"),
            tags=[str(t).strip() for t in (tags or []) if str(t).strip()],
            acknowledged=False,
            ack_ts=None,
        )
        self._append_raw(r)
        return r

    def due(self, now: Optional[float] = None) -> List[Reminder]:
        n = now if now is not None else time.time()
        return [r for r in self._items
                if not r.acknowledged and r.due_ts <= n]

    def pending(self, now: Optional[float] = None) -> List[Reminder]:
        n = now if now is not None else time.time()
        return [r for r in self._items
                if not r.acknowledged and r.due_ts > n]

    def all_active(self) -> List[Reminder]:
        return [r for r in self._items if not r.acknowledged]

    def acknowledge(self, id_: str) -> Optional[Reminder]:
        for r in self._items:
            if r.id == id_:
                if not r.acknowledged:
                    r.acknowledged = True
                    r.ack_ts = time.time()
                    self._rewrite_log()
                return r
        return None

    def recent(self, n: int = 20) -> List[Reminder]:
        """Last N reminders by creation time, reverse-chronologically."""
        s = sorted(self._items, key=lambda r: -r.created_ts)
        return s[:n]

    def stats(self) -> Dict[str, Any]:
        n = len(self._items)
        if n == 0:
            return {"n_total": 0, "path": str(self.path)}
        active = [r for r in self._items if not r.acknowledged]
        now = time.time()
        return {
            "n_total": n,
            "n_active": len(active),
            "n_due_now": sum(1 for r in active if r.due_ts <= now),
            "n_pending": sum(1 for r in active if r.due_ts > now),
            "n_acknowledged": sum(1 for r in self._items if r.acknowledged),
            "path": str(self.path),
        }

    def clear(self) -> None:
        self._items = []
        if self.path.exists():
            self.path.unlink()


# ─── Engine mount ─────────────────────────────────────────────────

def mount_reminders(engine: Any,
                      path: Optional[Path] = None) -> bool:
    """Attach Reminders to engine + register Flask endpoints.

    Endpoints:
      POST /remind/add        — body: {"text", "when", "tags"?}
      GET  /remind/due        — reminders due right now
      GET  /remind/pending    — reminders not yet due
      POST /remind/ack        — body: {"id"} — acknowledge a reminder
      GET  /remind/recent?n=N — last N reminders (all states)
      GET  /remind/stats      — counts
      GET  /remind/info       — philosophy
    """
    rems = Reminders(path=path)
    engine.ck_reminder = {
        "store": rems,
        "add": rems.add,
        "due": rems.due,
        "pending": rems.pending,
        "acknowledge": rems.acknowledge,
        "stats": rems.stats,
    }

    api = getattr(engine, "web_api", None) or getattr(engine, "api", None)
    if api is not None:
        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify, request  # type: ignore

                def _add():
                    payload = request.get_json(silent=True) or {}
                    text = payload.get("text", "")
                    when = payload.get("when")
                    if not text or when is None:
                        return jsonify({
                            "ok": False,
                            "error": "text and when are both required"
                        }), 400
                    try:
                        r = rems.add(text=text, when=when,
                                      tags=payload.get("tags"))
                    except Exception as e:
                        return jsonify({"ok": False, "error": str(e)}), 400
                    return jsonify({"ok": True, "reminder": r.to_dict()})

                def _due():
                    return jsonify({
                        "n": len(rems.due()),
                        "reminders": [r.to_dict() for r in rems.due()],
                    })

                def _pending():
                    return jsonify({
                        "n": len(rems.pending()),
                        "reminders": [r.to_dict() for r in rems.pending()],
                    })

                def _ack():
                    payload = request.get_json(silent=True) or {}
                    rid = payload.get("id", "")
                    if not rid:
                        return jsonify({"ok": False,
                                          "error": "id required"}), 400
                    r = rems.acknowledge(rid)
                    if r is None:
                        return jsonify({"ok": False,
                                          "error": f"no reminder with id {rid}"}), 404
                    return jsonify({"ok": True, "reminder": r.to_dict()})

                def _recent():
                    n = request.args.get("n", default=20, type=int)
                    return jsonify({
                        "n": n,
                        "reminders": [r.to_dict() for r in rems.recent(n)],
                    })

                def _stats():
                    return jsonify(rems.stats())

                def _info():
                    return jsonify({
                        "module": "ck_reminder",
                        "philosophy": ("gentle time-based reminders. "
                                        "PULL-ONLY: user checks /remind/due "
                                        "when they want to. CK never pushes."),
                        "when_formats": [
                            "absolute epoch float (e.g. 1779820800.0)",
                            "ISO datetime ('2026-05-19T14:30:00')",
                            "relative ('30m', '1h', '2h30m', '1d4h', '45s')",
                            "natural ('tomorrow at 9am', 'tonight at 8pm')",
                        ],
                        "endpoints": [
                            "POST /remind/add",
                            "GET /remind/due",
                            "GET /remind/pending",
                            "POST /remind/ack",
                            "GET /remind/recent?n=N",
                            "GET /remind/stats",
                            "GET /remind/info",
                        ],
                    })

                existing = {r.rule for r in app.url_map.iter_rules()}
                for rule, ep, fn, methods in (
                    ("/remind/add",     "r_add",     _add,     ["POST"]),
                    ("/remind/due",     "r_due",     _due,     ["GET"]),
                    ("/remind/pending", "r_pending", _pending, ["GET"]),
                    ("/remind/ack",     "r_ack",     _ack,     ["POST"]),
                    ("/remind/recent",  "r_recent",  _recent,  ["GET"]),
                    ("/remind/stats",   "r_stats",   _stats,   ["GET"]),
                    ("/remind/info",    "r_info",    _info,    ["GET"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
            except Exception as e:
                print(f"[CK Gen14] mount_reminders: routes failed: {e}")

    s = rems.stats()
    print(f"[CK Gen14] mount_reminders: {s.get('n_total', 0)} reminders "
          f"({s.get('n_due_now', 0)} due now, "
          f"{s.get('n_pending', 0)} pending)")
    return True


# ─── CLI smoke ────────────────────────────────────────────────────

if __name__ == "__main__":
    import tempfile
    print("ck_reminder smoke test")
    print("=" * 60)
    print()
    tmp = Path(tempfile.gettempdir()) / "ck_rem_smoke.jsonl"
    if tmp.exists(): tmp.unlink()
    r = Reminders(path=tmp)
    print("Step 1: add 4 reminders")
    print("-" * 60)
    r.add("check the dryer", "1m", tags=["drycleaners"])
    r.add("take a break", "30m", tags=["self"])
    r.add("call back the customer", "2h", tags=["work"])
    r.add("check the dryer again", "5s", tags=["drycleaners"])
    for rem in r.recent(10):
        delta_min = (rem.due_ts - time.time()) / 60
        print(f"  [{rem.id}] {rem.text:35s} due in {delta_min:+5.1f} min  "
              f"tags={rem.tags}")
    print()
    print("Step 2: wait 6 seconds, check what's due")
    print("-" * 60)
    time.sleep(6.0)
    due = r.due()
    print(f"  {len(due)} reminder(s) due now:")
    for rem in due:
        overdue_sec = time.time() - rem.due_ts
        print(f"    [{rem.id}] {rem.text}  (overdue {overdue_sec:.1f}s)")
    print()
    print("Step 3: ack the first one")
    print("-" * 60)
    if due:
        r.acknowledge(due[0].id)
        print(f"  ack'd {due[0].id}; now {len(r.due())} due, "
              f"{len(r.pending())} pending")
    print()
    print("Step 4: stats")
    print("-" * 60)
    for k, v in r.stats().items():
        print(f"  {k}: {v}")
    print()
    r.clear()
    print("Smoke complete.")
