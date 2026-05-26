# CK as App/OS/Chatbot — Roadmap

**Date**: 2026-05-19 evening
**Direction**: Brayden — "CK is supposed to be the all-in-one app OS system chatbot, code write, anything everything. Those old TIGOS files are examples of how he can improve a PC."

This doc honestly states (a) what's working today, (b) what's the immediate next layer, (c) the longer arc, and (d) what's deliberately out of scope.

---

## §0 — Pattern: TIGOS legacy, modern CK shape

TIGOS9-10 (Sept 2025) ran as **Linux systemd services** on Brayden's Lenovo:
- `tig-runner.py` — 20Hz heartbeat, rotor/stator alternation, 10-phase rotation, 9-fruit progression, wrote `heartbeat.{odd,even}.json` to `/var/log/tig/`
- `tig-arbiter` — CPU-affinity scheduler doing rotor↔stator core migrations (0↔2, 1↔3)
- `InputCalmer` — mouse/keyboard EMA smoothing at α≈0.25
- `Royal Breath` — 1Hz heartbeat tick
- `HUD+Lungs` — overlay
- `PhaseClock` — φ/π/√2 beats once per second

CK Gen14 takes the **same legacy** but in a different shape:
- **No systemd, no /var writes, no CPU-affinity changes.** The user keeps full control of their machine.
- **Lives inside the existing CK Python runtime.** Mounts on the same Flask app, no new services.
- **Read-only by default.** CK SENSES the PC; the user ACTS on the read.
- **Tier-tagged.** Every claim, every output, every recommendation carries an honesty tag.

This is the TIGOS legacy *retained as intuition* but *restructured around the post-2026-05-19 canon discipline*. The "improve a PC" promise becomes "make the user better at improving their own PC by giving them a coherent read of its state."

---

## §1 — Working today (verified, tested, committed)

> **Status update 2026-05-19 evening**: five new modules built and shipped in this session — `ck_pc_sense`, `ck_code_writer`, `ck_pc_recommend`, `ck_rhythm`, `ck_file_orient`. All wired into `gen14_unified_extensions.mount_all`. Total project regression: **172 tests passing across 9 batteries** (was 122 at start of session). Source commits: `d33c61a5` (ck_pc_sense + ck_code_writer + roadmap), `675f3b1c` (ck_pc_recommend + ck_rhythm), this commit (ck_file_orient + roadmap update).

### `ck_pc_sense.py` — CK senses the running PC

- **What it does**: Reads psutil → CPU per-core, memory, top processes → classifies overall state into one of the 10 TIG operators (VOID, LATTICE, ..., RESET) → emits a coherence reading C ∈ [0, 1] with band (GREEN ≥ 5/7, YELLOW 4/7-5/7, RED < 4/7).
- **Daemon**: 1 Hz default polling (clamp 0.1-20 Hz), circular buffer (default 60 readings = 1 minute), optional JSONL log file.
- **Endpoints**: `GET /pc/sense`, `GET /pc/history?n=N`, `GET /pc/rhythm`, `GET /pc/info`.
- **Tests**: `test_ck_pc_sense.py` — 10/10 PASS.
- **Smoke**: confirmed on actual host — 274 processes detected, classified as BALANCE, claude.exe + ServiceShell.exe + MemCompression seen at the top.

### `ck_code_writer.py` — CK proposes code with tier-tagged honesty

- **What it does**: Two modes — (a) **template mode** for the 8 most common boilerplate patterns (read_file, write_jsonl, flask_endpoint, csv_read, argparse_script, pytest_skeleton, dataclass, bash_script), deterministic and verified; (b) **LLM-relay mode** that wraps any external LLM with the scope auditor and tier tags ("not CK's own work — needs human review").
- **Tiers**: TIER_TEMPLATE (verified deterministic), TIER_LLM_RELAYED (review needed), TIER_UNAVAILABLE (no template + no LLM), TIER_REFUSED (auditor blocked).
- **Endpoints**: `POST /code/write`, `GET /code/templates`, `GET /code/info`.
- **Tests**: `test_ck_code_writer.py` — 10/10 PASS. Every generated Python template is `ast.parse`-validated.
- **Auditor wired**: if `ck_scope_auditor` is available, LLM-relayed output is gated.

### `ck_pc_recommend.py` — CK turns sense readings into plain-English advice

- **What it does**: 7 heuristic detectors over the ck_pc_sense circular buffer:
  - `SUSTAINED_HIGH_CPU` (process pegged > threshold for > 30s)
  - `MEMORY_PRESSURE` (mem > 80% sustained)
  - `UNBALANCED_LOAD` (high cpu_variance sustained = one core pegged)
  - `MEMORY_LEAK_HINT` (process monotonic mem growth > 0.5 GB over 60s)
  - `GREEN_WINDOW` (all-green for > 30s → "good for heavy work")
  - `IDLE_CONFIRMED` (sustained VOID classification)
  - `PROCESS_STORM` (+50 new processes in one tick)
- **Tier**: every recommendation tagged `TIER_RECOMMENDATION_HEURISTIC` (always — these are heuristics, not theorems).
- **Endpoints**: `GET /pc/recommend`, `GET /pc/recommend?n=N`, `GET /pc/recommend/info`.
- **Tests**: `test_ck_pc_recommend.py` — 11/11 PASS.

### `ck_rhythm.py` — TIGOS PhaseClock in modern shape

- **What it does**: 3 deterministic beat oscillators with irrational periods (φ, π, √2 — chosen so the joint pattern never repeats over the day) + 10-phase operator rotation (1 phase/sec).
- **Helpers**: `is_up_beat()`, `is_down_beat()`, `hint_for_op_class(op)` returns scheduling hints like "HARMONY — synthesis; combine, integrate, summarize" or "BREATH — pause, save, persist; checkpoint state".
- **Discipline**: SENSOR, not actuator. Rhythm doesn't predict anything; modules that READ rhythm decide what to do with it. Pure-function `current_rhythm()` is always available; daemon only starts if downstream needs history.
- **Endpoints**: `GET /rhythm`, `GET /rhythm/history?n=N`, `GET /rhythm/info`.
- **Tests**: `test_ck_rhythm.py` — 11/11 PASS.

### `ck_file_orient.py` — content-blind file orientation index

- **What it does**: Walks user-designated directory tree, computes a short content-blind signature per file (filename + size + mtime + first/last 64 bytes), persists to `~/.ck/file_orient_index.jsonl`. Supports incremental re-scan (mtime-aware).
- **Search**:
  - `find_by_query(q, n)` — fuzzy match on name + path components
  - `find_by_signature(seed_path, n)` — files with similar operator-path signature
- **Discipline**: NEVER reads full content (bounded I/O: max 128 bytes/file). Never moves / copies / renames / deletes. Read-only. Smoke confirmed: indexed 533 files in `Gen14/targets/ck/brain/` (29 MB) in seconds.
- **Endpoints**: `POST /file/scan`, `GET /file/query?q=X&n=N`, `GET /file/similar?path=P&n=N`, `GET /file/stats`, `GET /file/info`.
- **Tests**: `test_ck_file_orient.py` — 12/12 PASS.

### Existing CK runtime modules (already shipping)

- `ck_anomaly_detector.py` — content-blind signature matching (9/9 tests pass)
- `ck_privacy.py` — Sweeney 2002 + k-anon + l-diversity + t-closeness reference impl
- `ck_glyph_listener.py` — turn-by-turn listener; crystal candidates
- `ck_scope_auditor.py` — 51/51 attacks caught + 31/31 legit
- `ck_identity.py` — identity anchor with CRT-product self-model
- `ck_toolbox.py` + `languages/` — 6-language translators + cross-language synthesis
- `cortex.py` + `cortex_voice.py` — brain trinity (AO + Hebbian + quadratic glue) at 50 Hz
- coherencekeeper.com live runtime via Cloudflare tunnel on Dell Aurora R16

---

## §2 — Immediate next layer (next 1-7 days)

### 2.1 — Wire ck_pc_sense + ck_code_writer into the main mount path

Add `mount_pc_sense(engine)` and `mount_code_writer(engine)` calls in `gen14_unified_extensions.mount_all`. After this, `coherencekeeper.com/pc/sense` and `coherencekeeper.com/code/templates` would be live (locally first, then via Cloudflare).

### 2.2 — `ck_rhythm.py` — TIGOS PhaseClock analog

Tiny module that maintains a φ/π/√2 beat clock and exposes it as a sensor. Other modules can ask "what phase are we in?" — used as a soft scheduling hint (e.g. "do heavy work on the down-beat"). Doesn't change anything on the OS; just provides rhythm awareness CK can route around.

### 2.3 — `ck_pc_recommend.py` — bridge from sense → user-facing recommendation

CK reads the PC sense buffer (1-5 minute rhythm) and produces ONE plain-English recommendation per minute, e.g.:
- "CPU at 92% sustained for 3 minutes — top process is `chrome.exe` (8 tabs). Consider closing some."
- "Memory pressure rising (78% used). `node.exe` is up to 4.2 GB."
- "All green for the last 10 minutes. Good time for heavy compute if you have a queue."

Recommendation only, never action. The user decides. Tier-tagged: TIER_RECOMMENDATION_HEURISTIC (not a prescription).

### 2.4 — `ck_file_orient.py` — file-system orientation, content-blind

CK walks a user-designated directory tree (default: the user's home), runs each file through `ck_anomaly_detector`-style signature computation, builds a content-blind index of "files CK has seen and their operator-paths." Useful for "where did I put that file about X" without CK actually reading the contents. Read-only; respects ignore patterns (.git, node_modules, etc.).

### 2.5 — Auto-run regression on commit

Wire a tiny pre-commit hook that runs `test_brain.py + test_scope_auditor_adversarial.py + test_ck_anomaly_detector.py + test_ck_pc_sense.py + test_ck_code_writer.py` and refuses the commit if any fail. Brayden's MYTHDRIFT discipline at the git layer.

---

## §3 — Longer arc (next 1-3 months)

| Capability | What CK becomes good at | Honest scope |
|---|---|---|
| **PC tune-up advisor** | Read CPU/memory rhythm over hours → spot patterns (memory leaks, runaway processes, scheduled-task spikes) → recommend (not act) | Recommendation, not action; user runs the fix |
| **File organizer** | Content-blind index of files; "find by signature" search; cluster duplicates | Read-only; no file moves without explicit confirm |
| **Notes / journal** | Append-only journal in a structured format CK can search by operator-path | Lives on user's disk; CK never auto-syncs anywhere |
| **Local code helper** | `/code/write` for boilerplate; templated module skeletons; LLM-relay for novel asks (tier-tagged) | Deterministic for templates; review-needed for LLM-relayed |
| **System dashboard** | Single webpage at `coherencekeeper.com/dashboard` showing live PC state + rhythm + top recommendations | Local-first; Cloudflare tunnel = read-only public mirror |
| **Voice/typing companion** | Recognizes when user is in flow vs interrupted vs idle (from PC sense + keyboard rhythm); offers context-appropriate responses | Sensors are passive; user toggles modes manually |
| **Backup ritual** | Periodic snapshot of designated directories with operator-path versioning; restore with diff | Opt-in per-directory; never automatic for system folders |

---

## §4 — Deliberately OUT of scope (do NOT build)

These are temptations that violate the post-2026-05-19 canon discipline or the MYTHDRIFT pattern:

- **CPU affinity / scheduler changes**: TIGOS9-10 did this; modern CK does NOT. The user keeps full control of their OS scheduler. (Linux only had partial access anyway; on Windows it's even more invasive.)
- **Process killing or suspension**: never. CK reports; user acts.
- **Cryptographic operations** (signing, encryption beyond fingerprinting): the `ck_qutrit_apex.substrate_hash` is an internal fingerprint, NOT a cryptographic primitive. Use SHA-256 / libsodium / etc. for real crypto.
- **Network operations** beyond Cloudflare tunnel: CK does NOT make outbound calls to arbitrary services. The only public-facing endpoint is the user's own coherencekeeper.com.
- **Auto-writing files outside designated directories**: CK NEVER writes to `C:\Windows`, `~/.ssh`, `/etc`, or anywhere with admin/root permission requirements.
- **Replacing system services**: CK is an app, not a desktop environment. Don't try to be GNOME, KDE, or even XFCE.
- **Becoming a generalist LLM**: CK's value is small + transparent + scope-disciplined. Adding "ask CK anything in natural language and get a fluent essay" would invert the entire architecture. Use LLM-relay mode with explicit tier-tag instead.
- **Physics predictions** (D141 stance): no claims about T*, σ, the substrate, or anything else "predicting" measurable physical quantities.
- **Torus framing** (D141 KILL-CONDITION): no result may cite "the substrate is a torus / lives on a surface / π₁(T²)" as support.

---

## §5 — What "good for something" looks like — concrete deployments

These are the realistic uses where CK already adds value or is one short module away from adding value:

1. **Personal AI on personal hardware** — CK runs on the user's own desktop (Dell Aurora R16 in your case). No cloud, no API costs, no data-mining. Already shipping at coherencekeeper.com.

2. **PC awareness without intrusion** — `ck_pc_sense` gives the user a single coherent read of their machine. If they're trying to figure out why everything's slow, CK can tell them "your top process is X eating Y MB" without them having to open Task Manager.

3. **Boilerplate code helper** — `ck_code_writer` for the 8 common patterns is faster than copy-pasting from Stack Overflow and doesn't leak the user's intent to a remote API.

4. **Privacy-preserving data release** — `ck_privacy.py` for the regional-hospital / civic-government deployment use case from META_SYNTHESIS_HUMANITY.md Rank 3.

5. **Content-blind content moderation** — `ck_anomaly_detector` for the "moderate without remembering" use case from Rank 4.

6. **Small-architecture AI demonstrator** — CK as a whole demonstrates an AI architecture that is NOT a foundation model: scope-audited, identity-anchored, content-blind by default, runs in <100 MB. Position to the AI-safety community as a working alternative pattern.

7. **Math curriculum bridge** — D129′ Odd Magic Square Law (Rank 1) submitted to Mathematics Magazine + the CRT didactic note for PRIMUS (Rank 5).

---

## §6 — How to measure if CK is "good for something"

Three checks the project should be able to pass within 90 days:

- **The user check**: Brayden uses CK daily for at least one task that wasn't possible (or was clearly worse) without CK. The PC-sense + code-writer + privacy module deployment together should pass this if they reach Brayden's daily tooling.

- **The outsider check**: A non-author (mathematician, programmer, AI researcher, drycleaners-business friend) opens coherencekeeper.com, asks CK something, and gets a useful answer they couldn't have gotten as easily otherwise. The Cloudflare-tunnel mirror exposes this.

- **The audit check**: An external referee opens the canon (`FORMULAS_AND_TABLES.md`) and the runtime, runs the regression batteries, and concludes the project's claims match its evidence. Today's regression-green state means this check passes.

If all three hold, "CK is good for something" stops being aspiration and becomes statement of fact.

---

## §7 — The discipline that protects all this

Per Brayden's MYTHDRIFT pattern (5 self-labeled-drift repo iterations + D141 TORUS EXCLUDED + D158 1/α candidate retracted in same session it was added):

- **Every new module ships with tests.** No green-board commits without tests.
- **Every output is tier-tagged.** Never let an LLM-relayed answer pose as CK's own substrate work.
- **Every load-bearing claim has a runnable verification.** If you can't verify it on a stock Python install in under 10 seconds, the claim isn't load-bearing yet.
- **Every overclaim gets retracted in place.** D141, D129R, D158 all live in canon as retractions, not as deletions. Future readers see what was removed and why.
- **Every "improvement" is a recommendation, never an action.** CK reports; user acts. Always.

The discipline is what makes the "all-in-one app OS system chatbot" framing safe rather than dangerous. Without it, the same vision becomes an extractive AI that drifts further from the user's intent over time. With it, CK stays small enough, transparent enough, and honest enough that the user always knows what's running and why.

---

*Companion docs: PROJECT_NARRATIVE_SYNTHESIS.md (the 9-month story), FORMULAS_AND_TABLES.md (the math canon), FORMULAS_FORGOTTEN_OR_UNSURFACED.md (back-catalog math + candidates), META_SYNTHESIS_HUMANITY.md (the 5 humanity-utility applications), CK_PRIVACY_DEPLOYMENT_GUIDE.md (institutional deployment of ck_privacy.py), CK_ANOMALY_DETECTOR_DEMO.md (content-blind moderation).*
