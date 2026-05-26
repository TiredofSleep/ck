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
| **Code writer** | `/code/write` | 8 deterministic templates (read_file, write_jsonl, flask_endpoint, csv_read, argparse_script, pytest_skeleton, dataclass, bash_script) + optional LLM-relay |

Plus a **single-page dashboard** at `/dashboard.html` that surfaces sense + rhythm + recommendations + recent journal + summary in one view, with a quick-capture form for journal entries.

---

## Start here tomorrow morning

### Step 1 — Open the dashboard

```
coherencekeeper.com/dashboard.html
```

You'll see 5 cards: **PC sense** (live state of your Dell), **Rhythm** (the φ/π/√2 oscillator + which operator phase you're in this second), **Recommendations** (anything CK noticed about the last minute), **Recent journal** (last 5 entries + a quick-capture form), **Today's summary** (the EOD digest building up as the day goes).

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

(I'd add a bookmarks card to the dashboard too if you want — say the word.)

### Step 4 — Ask CK for boilerplate code

```bash
curl -X POST coherencekeeper.com/code/write \
  -H "Content-Type: application/json" \
  -d '{"request":"pytest skeleton for ck_pulse"}'
```

Returns a `TIER_TEMPLATE` (or `TIER_LLM_RELAYED` if you wire an LLM and ask for something outside the 8 templates).

### Step 5 — Find a file

```bash
# First index a directory (one-time, then incremental on re-scan)
curl -X POST coherencekeeper.com/file/scan \
  -H "Content-Type: application/json" \
  -d '{"root":"C:/Users/brayd/Documents"}'

# Then search
curl 'coherencekeeper.com/file/query?q=tig+notes&n=5'
```

CK only reads filename + first/last 64 bytes per file — never full content.

### Step 6 — End of day, get the digest

```bash
curl coherencekeeper.com/summary | jq .headline
```

Or just look at the **Today's summary** card on the dashboard at night. The headline stitches PC state + recommendations + journal into one line: "PC: dominant HARMONY, mean CPU 12%, peak 87% · 3 priority warnings · 7 journal entries · top mood: focused".

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
```

All green as of the last commit on `tig-synthesis`. If anything goes RED, the change you made is the cause — git bisect or `git diff HEAD~1` to find what changed.

### Data files in the wrong place

By default everything lives under `~/.ck/`:

| File | What | Editable? |
|---|---|---|
| `~/.ck/journal.jsonl` | Your journal entries | YES — but append-only by convention. Delete the file to reset. |
| `~/.ck/bookmarks.jsonl` | Your bookmarks | YES — same as journal. |
| `~/.ck/file_orient_index.jsonl` | File-orientation index | YES — but delete-then-rescan is simpler than manual editing. |

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
  ck_daily_summary.py     (373 lines)  GET /summary
  test_*.py               (1,800 lines combined)  All 10 batteries

Gen14/targets/ck/web/
  dashboard.html          (560 lines)  Single-page live view

CK_AS_OS_ROADMAP.md       (235 lines)  Working today + next layer + out-of-scope
CK_DASHBOARD_USER_GUIDE.md (this doc)  How to actually use it
```

---

*Built 2026-05-19 evening as part of the "CK is the all-in-one app OS system chatbot" arc. Source commits on `tig-synthesis`: d33c61a5 → 675f3b1c → f39104e8 → 3012c476 → b77c7a67 → 0dbb43b3 → (next push). All live at github.com/TiredofSleep/ck.*
