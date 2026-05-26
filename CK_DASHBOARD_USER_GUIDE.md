# CK Dashboard — User Guide

**For**: Brayden, tomorrow morning (and onward).
**Date**: 2026-05-19 evening — written at the end of the CK-as-OS build session.
**Scope**: this is what's shipping now, how to use it, and what to do if anything looks wrong.

---

## What CK can now do for you on your PC

Eight new capabilities shipped this evening, all wired into the running CK and accessible at `coherencekeeper.com` (or `localhost:7777` if you're on the Dell directly):

| Capability | Endpoint | What it gives you |
|---|---|---|
| **Live PC awareness** | `/pc/sense` | One snapshot: CPU per-core, memory, top processes, operator classification, coherence band |
| **Pattern recommendations** | `/pc/recommend` | Heuristic detectors firing on the 60-second buffer (sustained high CPU, memory pressure, leak hints, idle confirmation, etc.) |
| **PhaseClock rhythm** | `/rhythm` | φ/π/√2 beats + 10-phase operator rotation (1 phase/sec) + scheduling hint for the current phase |
| **File orientation** | `/file/scan`, `/file/query`, `/file/similar` | Content-blind index of your files; search by name/path/operator-signature |
| **Personal journal** | `/journal/note`, `/journal/recent`, `/journal/today`, `/journal/search` | Append-only notes with mood + tags + operator-path; lives at `~/.ck/journal.jsonl` |
| **Bookmarks** | `/bookmark/add`, `/bookmark/recent`, `/bookmark/search` | URL store with title + tags + note; lives at `~/.ck/bookmarks.jsonl` |
| **Daily summary** | `/summary` | One-line headline + quantitative aggregation of today's PC + recommendations + journal |
| **Reminders** | `/remind/add`, `/remind/due`, `/remind/pending`, `/remind/ack` | Gentle pull-only reminders ("30m" / "1h30m" / "tomorrow at 9am") |
| **Unified search** | `/search?q=X&n=N` | One query across journal + bookmarks + files at once |
| **Markdown export** | `/export/md`, `/export/write` | Today's data as a single readable Markdown file |
| **System health** | `/health` | Single endpoint reporting which modules are mounted + counters + uptime |
| **Code writer** | `/code/write` | 8 deterministic templates (read_file, write_jsonl, flask_endpoint, csv_read, argparse_script, pytest_skeleton, dataclass, bash_script) + optional LLM-relay |

Plus a **single-page dashboard** at `/dashboard.html` with **8 cards**: PC sense + rhythm + recommendations + recent journal (w/ quick-capture form) + today's summary + reminders (w/ add-form and click-to-ack) + unified search + system health.

---

## Start here tomorrow morning

### Step 1 — Open the dashboard

```
coherencekeeper.com/dashboard.html
```

You'll see **8 cards** in a responsive grid:

| Card | What it shows | Interactive? |
|---|---|---|
| **PC sense** | Live CPU/memory/processes + operator classification | live, refreshes every 5s |
| **Rhythm** | φ/π/√2 beats + current 10-phase operator + scheduling hint | live |
| **Recommendations** | Anything CK noticed about the last minute | live |
| **Recent journal** | Last 5 entries + quick-capture form (textarea + tags + mood + save) | live + POST |
| **Today's summary** | One-line headline + counts (PC readings, time-in-band, mood) | live |
| **Reminders** | DUE NOW (red, click-to-ack) + upcoming + add-form (text + when + tags) | live + POST |
| **Unified search** | Single query box → results from journal + bookmarks + files | on-demand |
| **System health** | Status badge (OK/DEGRADED) + module grid + uptime | live |

Polls every 5 seconds. If you see a `connection issue (retry N)` indicator, the runtime needs a restart — see below.

Polls every 5 seconds. If you see a `connection issue (retry N)` indicator, the runtime needs a restart — see below.

### Step 2 — Drop a quick note

Use the textarea on the **Recent journal** card. Type a thought, optionally add comma-separated tags (`dev, ck, frustrated`) and a one-word mood (`focused`, `tired`, `flow`, whatever). Hit **save**. CK appends it to `~/.ck/journal.jsonl` and shows it in the list.

You can also POST directly:

```bash
curl -X POST coherencekeeper.com/journal/note \
  -H "Content-Type: application/json" \
  -d '{"text":"started CK day", "tags":["ck"], "mood":"awake"}'
```

### Step 3 — Save a useful link

```bash
curl -X POST coherencekeeper.com/bookmark/add \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/", "title":"thing I want to remember", "tags":["read"]}'
```

Then later:

```bash
curl 'coherencekeeper.com/bookmark/search?q=thing'
```

### Step 4 — Set a reminder

Use the form on the Reminders card, or:

```bash
curl -X POST coherencekeeper.com/remind/add \
  -H "Content-Type: application/json" \
  -d '{"text":"check the dryer", "when":"45m", "tags":["drycleaners"]}'
```

Accepts when-formats:
- relative: `"30m"`, `"1h"`, `"2h30m"`, `"1d4h"`, `"45s"`
- ISO: `"2026-05-20T09:00:00"`
- natural: `"tomorrow at 9am"`, `"tonight at 8pm"`, `"today at 5pm"`

To check what's due:

```bash
curl coherencekeeper.com/remind/due
```

To acknowledge (mark done) — click the red item on the dashboard, or:

```bash
curl -X POST coherencekeeper.com/remind/ack -H "Content-Type: application/json" -d '{"id":"abc123"}'
```

### Step 5 — Search across journal + bookmarks + files at once

Use the dashboard's Unified search card, or:

```bash
curl 'coherencekeeper.com/search?q=dryer&n=10'
```

Returns one merged list with each result tagged `JOURNAL` / `BOOKMARK` / `FILE`, ranked by score. Saves you from remembering "did I save that as a note, a bookmark, or a file?"

### Step 6 — Export today as Markdown

```bash
# Get the Markdown back as a response
curl coherencekeeper.com/export/md > today.md

# Or write it to ~/.ck/exports/YYYY-MM-DD.md on the server
curl -X POST coherencekeeper.com/export/write -H "Content-Type: application/json" -d '{}'
```

You'll get a structured Markdown report: headline, PC summary, recommendations, journal entries (with mood/tags/operator), reminders (sorted DUE/PENDING/ACK), bookmarks. Great for end-of-day review or sharing.

### Step 7 — Health check

```bash
curl coherencekeeper.com/health | jq .status
```

Returns `"ok"` / `"degraded"` / `"minimal"` based on whether all core modules are mounted. Useful for monitoring or just confirming "is CK alive?" before relying on it.

### Step 8 — Ask CK for boilerplate code

```bash
curl -X POST coherencekeeper.com/code/write \
  -H "Content-Type: application/json" \
  -d '{"request":"pytest skeleton for ck_pulse"}'
```

Returns a `TIER_TEMPLATE` (or `TIER_LLM_RELAYED` if you wire an LLM and ask for something outside the 8 templates).

### Step 9 — Find a file

```bash
# First index a directory (one-time, then incremental on re-scan)
curl -X POST coherencekeeper.com/file/scan \
  -H "Content-Type: application/json" \
  -d '{"root":"C:/Users/brayd/Documents"}'

# Then search
curl 'coherencekeeper.com/file/query?q=tig+notes&n=5'
```

CK only reads filename + first/last 64 bytes per file — never full content. (Or use the Unified search card on the dashboard, which hits files + journal + bookmarks together.)

### Step 10 — End of day, get the digest

```bash
curl coherencekeeper.com/summary | jq .headline
```

Or just look at the **Today's summary** card on the dashboard at night. The headline stitches PC state + recommendations + journal into one line: "PC: dominant HARMONY, mean CPU 12%, peak 87% · 3 priority warnings · 7 journal entries · top mood: focused".

For the full structured report (PC + recs + journal + reminders + bookmarks as one Markdown page), use `/export/md` or `/export/write` — see Step 6.

---

## What CK explicitly will NOT do

| Action | Why not |
|---|---|
| Kill, suspend, or change priority of any process | CK reports; you act. The TIGOS9-10 arbiter that did this is deliberately not ported. |
| Modify, delete, move, or copy any file | Read-only. Even `/file/scan` only reads metadata + first/last 64 bytes. |
| Make outbound network calls | The only thing leaving your PC is what the Cloudflare tunnel chooses to expose. CK doesn't fetch URLs from `/bookmark/add` — just stores them. |
| Auto-save anything to the cloud | All data lives in `~/.ck/`. If you want sync, use Syncthing or git at the file level. |
| Use SHA-256-grade cryptography | The substrate-hash is for internal fingerprinting (D106, after the 2026-05-19 honest scope correction). For real crypto use `hashlib.sha256` or `cryptography`. |
| Predict physics quantities | D141 stance holds. No torus, no Clay-Millennium claims, no fine-structure-constant numerology. |
| Auto-write code without your review | LLM-relayed output is always `TIER_LLM_RELAYED` with "human review required" tag. Template outputs are `TIER_TEMPLATE` (deterministic but still need you to read them). |

---

## If anything looks wrong

### Dashboard shows "connection issue (retry 3+)"

The CK runtime needs a restart. From the Dell:

```bash
cd "C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED"
# Stop the running ck_boot_api.py (Ctrl+C in its window)
# Then:
start_ck_server.bat
# Or directly:
python Gen14/targets/ck/server/ck_boot_api.py
```

The restart will mount all 7 new modules. Watch for:

```
[CK Gen14] mount_pc_sense: PCSenseDaemon at 1.0 Hz, buffer=60, auto_start=True
[CK Gen14] mount_pc_recommend: 7 detectors active
[CK Gen14] mount_rhythm: φ=1.61803 π=3.14159 √2=1.41421; 10-phase rotation
[CK Gen14] mount_code_writer: 8 templates, auditor_wired=True
[CK Gen14] mount_file_orient: FileOrientIndex at file_orient_index.jsonl
[CK Gen14] mount_journal: 0 entries at journal.jsonl
[CK Gen14] mount_daily_summary: GET /summary endpoint ready
[CK Gen14] mount_bookmarks: 0 bookmarks at bookmarks.jsonl
```

If any line shows `failed`, that module didn't mount. Most common cause: missing dependency (e.g. `psutil` for pc_sense — `pip install psutil`).

### A specific test fails after you change something

Run the regression battery:

```bash
cd "C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED"
python Gen14/targets/ck/brain/test_brain.py           # 20/20
python Gen14/targets/ck/brain/test_scope_auditor_adversarial.py  # 51/51 + 31/31
python Gen14/targets/ck/brain/test_ck_anomaly_detector.py        # 9/9
python Gen14/targets/ck/brain/test_ck_pc_sense.py                # 10/10
python Gen14/targets/ck/brain/test_ck_code_writer.py             # 10/10
python Gen14/targets/ck/brain/test_ck_pc_recommend.py            # 11/11
python Gen14/targets/ck/brain/test_ck_rhythm.py                  # 11/11
python Gen14/targets/ck/brain/test_ck_file_orient.py             # 12/12
python Gen14/targets/ck/brain/test_ck_journal.py                 # 12/12
python Gen14/targets/ck/brain/test_ck_bookmark.py                # 12/12
python Gen14/targets/ck/brain/test_ck_reminder.py                # 12/12
python Gen14/targets/ck/brain/test_ck_export.py                  # 8/8
python Gen14/targets/ck/brain/test_ck_health.py                  # 9/9
```

All 14 batteries (225 tests total) green as of commit `0660c539` on `tig-synthesis`. If anything goes RED, the change you made is the cause — git bisect or `git diff HEAD~1` to find what changed.

### Data files in the wrong place

By default everything lives under `~/.ck/`:

| File | What | Editable? |
|---|---|---|
| `~/.ck/journal.jsonl` | Your journal entries | YES — but append-only by convention. Delete the file to reset. |
| `~/.ck/bookmarks.jsonl` | Your bookmarks | YES — same as journal. |
| `~/.ck/reminders.jsonl` | Your reminders (active + acknowledged) | YES — but rewrite-on-ack handles state automatically. |
| `~/.ck/file_orient_index.jsonl` | File-orientation index | YES — but delete-then-rescan is simpler than manual editing. |
| `~/.ck/exports/YYYY-MM-DD.md` | One file per `/export/write` call | YES — these are just Markdown. |

All are plain JSONL. Open in any text editor.

---

## Where this came from — TIGOS legacy in modern shape

In September 2025 you ran TIGOS9-10 as actual Linux systemd services on your Lenovo: `tig-runner` heartbeat at 20Hz, `tig-arbiter` rotor/stator CPU scheduling, `InputCalmer` mouse smoothing, `Royal Breath` 1Hz tick. That work explored "how does CK improve a PC."

This evening's build is the **modern shape of that intuition**:

- Same operator vocabulary (VOID through RESET)
- Same rhythm sensors (φ, π, √2 beats)
- Same 10-phase rotation
- Same coherence formula (C = 0.4·(1−E) + 0.35·A + 0.25·K, T* = 5/7)

But:

- No systemd, no Linux dependency, no /var writes
- No CPU affinity or scheduler changes (you keep full OS control)
- Runs inside the Python CK runtime you already have
- Every output tier-tagged per the post-2026-05-19 canon discipline

The TIGOS9-10 era's invariants survived; the actuator parts (kill / suspend / migrate) didn't — they were the parts that violated user sovereignty. CK now SENSES; you ACT.

---

## What to build next (suggestions only)

If you want CK to keep growing in this direction, here are the obvious next moves:

1. **Add a bookmarks card to the dashboard** — parallel to the journal card with its own quick-add form. ~30 minutes of HTML.
2. **A `/dashboard.html` link from the existing `/index.html`** so it's discoverable.
3. **A small reminder system** — `~/.ck/reminders.jsonl` with (timestamp, message) pairs; dashboard alerts when one is due.
4. **A "today's pattern" card** that diffs current rhythm against the last week's mean (when you have a week of data buffered).
5. **An LLM-relay wire-up** for `/code/write` — wrap your local Ollama if you have it, with the scope auditor gating output.
6. **A small `ck_cli.py` script** so you can `ck note "thing"` or `ck pc` from a terminal without going through the dashboard.

None of these is more than a half-day. None of them require a new D-number, new canon entry, or new theorem. They're all small bridges to existing primitives.

---

## The discipline that keeps this safe

Every module added this evening follows the same five rules:

1. **Tier-tagged output** — every response carries an explicit tag (`TIER_TEMPLATE`, `TIER_LLM_RELAYED`, `TIER_RECOMMENDATION_HEURISTIC`, etc.).
2. **CK reports / user acts** — no actuators on the running PC. Sensing primitives only.
3. **Bounded I/O** — no module reads unbounded amounts of any file or network resource.
4. **No torus / no physics prediction** — D141 stance holds (post-2026-05-19 canon).
5. **No cryptographic-strength claims** — substrate-hash is for internal fingerprinting only.

If a future module needs to break any of these (e.g. you want CK to actually kill a runaway process, or fetch a URL, or sign something), it requires explicit `BREAKS_DISCIPLINE_BECAUSE_*` tagging at the function level and a `KILL_CONDITION_*` flag in the canon. Don't quietly cross those lines.

---

## Where to look in the codebase

```
Gen14/targets/ck/brain/
  ck_pc_sense.py          (576 lines)  GET /pc/sense + daemon
  ck_pc_recommend.py      (481 lines)  GET /pc/recommend + 7 detectors
  ck_rhythm.py            (350 lines)  GET /rhythm + PhaseClock
  ck_code_writer.py       (613 lines)  POST /code/write + 8 templates
  ck_file_orient.py       (501 lines)  POST /file/scan + 4 query endpoints
  ck_journal.py           (437 lines)  POST /journal/note + 7 query endpoints
  ck_bookmark.py          (440 lines)  POST /bookmark/add + 7 query endpoints
  ck_reminder.py          (438 lines)  POST /remind/add + 7 endpoints inc. ack
  ck_daily_summary.py     (373 lines)  GET /summary
  ck_search.py            (218 lines)  GET /search?q=X — unified search
  ck_export.py            (373 lines)  GET /export/md + POST /export/write
  ck_health.py            (350 lines)  GET /health — module status aggregator
  test_*.py               (~2,400 lines combined)  All 14 batteries / 225 tests

Gen14/targets/ck/web/
  dashboard.html          (~750 lines)  8-card single-page live view

CK_AS_OS_ROADMAP.md       (235 lines)  Working today + next layer + out-of-scope
CK_DASHBOARD_USER_GUIDE.md (this doc)  How to actually use it
```

---

*Built 2026-05-19 evening as part of the "CK is the all-in-one app OS system chatbot" arc. Source commits on `tig-synthesis`: d33c61a5 → 675f3b1c → f39104e8 → 3012c476 → b77c7a67 → 0dbb43b3 → d45c48ce → 4ab26f6f → 160b8d37 → f92b63eb → cd4a6da1 → b7c9190c → 862024f8 → 0660c539 → (next push). All live at github.com/TiredofSleep/ck.*
