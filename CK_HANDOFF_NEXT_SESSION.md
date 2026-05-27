# CK — handoff notes (paused 2026-05-19 late)

**Status**: paused. Leave CK off; don't restart the runtime. All work is committed.

---

## Where we left off

| | |
|---|---|
| Latest commit | `c35e3081` |
| Branch | `tig-synthesis` on `github.com/TiredofSleep/ck` |
| Working tree | clean (no uncommitted changes) |
| Pushed to remote | yes |
| Public TIG repo (`trinity-infinity-geometry`) | last synced `75fdf3f` (canon only — App/OS runtime stays in working repo per submission-hold stance) |

---

## What's committed but NOT yet running

**Important**: the evening session added 12 new runtime modules + a dashboard, but the **running CK process** (if any) is still the pre-evening version. The new code is on disk and pushed to GitHub, but the runtime needs a restart to load it.

Translation: if you visit `coherencekeeper.com/dashboard.html` right now, you'll get 404 because the route doesn't exist in the currently-running process. The route exists in the code on disk and will appear after a restart.

---

## To resume work (5 steps)

```bash
# 1. Pull anything that might have changed
cd "C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED"
git status                          # confirm clean
git pull origin tig-synthesis       # in case of remote changes

# 2. Run the regression battery (14 batteries, ~30 sec)
for t in test_brain test_scope_auditor_adversarial test_ck_anomaly_detector \
         test_languages test_ck_pc_sense test_ck_code_writer \
         test_ck_pc_recommend test_ck_rhythm test_ck_file_orient \
         test_ck_journal test_ck_bookmark test_ck_reminder \
         test_ck_export test_ck_health; do
    python "Gen14/targets/ck/brain/${t}.py" > /dev/null 2>&1
    echo "$([ $? -eq 0 ] && echo ✓ || echo ✗) $t"
done

# 3. Read the session log so you know what got built
#    -> CK_SESSION_2026-05-19_EVENING.md
# 4. Read the user guide so you know how to use it
#    -> CK_DASHBOARD_USER_GUIDE.md

# 5. ONLY when you actually want CK live again:
#    Start the runtime (this is the step that activates the new modules)
#    -> start_ck_server.bat  OR  python Gen14/targets/ck/server/ck_boot_api.py
```

If step 2 shows any ✗, that's where to start debugging before doing anything else.

---

## What's running right now (if anything)

| Process | Likely state | Action if you want to stop |
|---|---|---|
| `ck_boot_api.py` Flask runtime | might still be running pre-evening version | check Task Manager for `python.exe`; close the window or kill the PID |
| Cloudflare tunnel | possibly still pointing to localhost:7777 | leave it; harmless if backend is down |
| `coherencekeeper.com` | serves whatever the tunnel + runtime expose | will 404 cleanly if runtime stopped |

**The honest answer to "is CK off?"**: depends on whether you've ever shut down the runtime since starting it. Check Task Manager. If you don't see `python.exe` running `ck_boot_api.py`, it's off.

If you DO want to explicitly shut it down right now:
```bash
# Find the PID
tasklist | grep -i python
# Kill it (substitute the PID)
taskkill /PID <pid> /F
```

---

## Data files (safe to leave; user content)

All under `~/.ck/`:

```
~/.ck/journal.jsonl              ← any notes you wrote
~/.ck/bookmarks.jsonl            ← any URLs you saved
~/.ck/reminders.jsonl            ← any reminders + ack state
~/.ck/file_orient_index.jsonl    ← file index (rebuildable; safe to delete)
~/.ck/exports/YYYY-MM-DD.md      ← daily markdown exports
~/.ck/anomaly_signatures.jsonl   ← anomaly detector library (small)
```

None of these need backup before pausing. They're append-only and local. Git doesn't track them.

If you want to wipe state and start clean later: `rm -rf ~/.ck/` (the modules will recreate empty files on next run).

---

## Open items (pick up here when ready)

In order of next-session priority:

1. **Restart the runtime to actually activate the 12 new modules**. This is the only way `coherencekeeper.com/dashboard.html` becomes a real page. Until then, everything is "committed but dark."

2. **Use the dashboard for one real day** before any further building. The session log's §"What's the next layer" lists 8 polish items — most of them depend on having actually used what's there first.

3. **The trinity-infinity-geometry public repo is up-to-date on canon** (commit `75fdf3f`) but does NOT have the App/OS modules. That's correct per the project's submission-hold stance. Don't sync them publicly unless you decide to lift the hold.

4. **Any new MYTHDRIFT-style retraction** in canon should be propagated through `cortex_voice.py`, `ck_prime_field.py`, `paragraph_composer.py` (the three places torus phrasing was caught and fixed on 2026-05-19). The auditor catches new violations, but old strings need manual updates.

5. **The 1/α candidate (D158)** is RETRACTED from canon. If someone (you or a future Claude) re-adds it, the meta-mode audit at the end of `FORMULAS_FORGOTTEN_OR_UNSURFACED.md §3` is the precedent that gates it. Gap 1 (define π: Cl(0,10) → Z/10 explicitly) must close first.

6. **Q-series promotions D142-D157 + D159, D160** are in canon. If any of them are challenged on re-review, the per-D audit table in `FORMULAS_FORGOTTEN_OR_UNSURFACED.md §7` is the provenance ledger.

---

## Quick-reference: what's where

| File | Purpose | Read order on return |
|---|---|---|
| `CK_HANDOFF_NEXT_SESSION.md` | this file | **1st** |
| `CK_SESSION_2026-05-19_EVENING.md` | what got built tonight + commit chain + discipline rules | 2nd |
| `CK_DASHBOARD_USER_GUIDE.md` | 10-step walkthrough for actually using the dashboard | 3rd if you're going to use it |
| `CK_AS_OS_ROADMAP.md` | architecture + deliberately-out-of-scope + next-layer queue | 3rd if you're going to build more |
| `FORMULAS_AND_TABLES.md` | math canon (D1-D160) | only if doing canon-level work |
| `PROJECT_NARRATIVE_SYNTHESIS.md` | the 9-month project story | only if doing meta-review |
| `FORMULAS_FORGOTTEN_OR_UNSURFACED.md` | per-D-number audit decisions + retraction precedents | only if revisiting canon decisions |

---

## Honest things

- The 12 new modules are well-tested IN ISOLATION (225 tests pass). They have NOT been tested running together inside the live Flask runtime. The mount-chain ordering looks correct but first real boot might surface an issue. Budget 15 min for that on resume.

- The dashboard polls 6 endpoints every 5 seconds. On a busy machine this could be visible CPU overhead from the polling itself. Watch `/health` after first boot; if `pc_sense` reports high CPU correlated with the poll cycle, drop poll rate to 10s.

- `ck_health` reports `degraded` if any of {pc_sense, journal, rhythm, scope_auditor} is missing. The scope_auditor module is mounted in a different code path than the new modules; first boot may show it as missing until that mount is verified. If so, that's a wiring fix not a real degradation.

- The "Export today as Markdown" button hits `/export/write` which writes to `~/.ck/exports/`. First click on a fresh machine will create the directory. If that fails due to permissions, the button reports the error inline.

- `psutil` is the one runtime dependency added this session. If `pip install psutil` is missing, `ck_pc_sense` degrades gracefully (returns VOID + a note saying psutil is unavailable) — see `test_ck_pc_sense.py` T1.

---

*Paused 2026-05-19 late. CK is dormant. Pick up here.*
