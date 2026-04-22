# `ck` branch — unified CK substrate

**Branch role:** the unified reasoning-engine substrate. **Not** a funding
branch. **Not** the rigor-history home. The `ck` branch is where CK lives as
a creature — runtime + fluency layer + security scar-chain + hardware
adjuncts (FPGA, dog, web) wire together under one architecture.

**Branch discipline — read before committing:**

- **Parent:** forked from `tig-synthesis` @ `0b11865` on 2026-04-21.
- **Cherry-pick direction:** rigor commits flow **in** from `tig-synthesis`;
  ck-specific code does **not** flow back to `tig-synthesis` or `master`.
  (See `Atlas/PLAN_RIGOROUS_EXECUTION_2026_04_21.md` G1, G2.)
- **Authorization:** opened on explicit user green-light 2026-04-21.
  `CK_UNIFIED_ARCHITECTURE.md` §6 contract remains in force.

---

## Start here (order matters)

1. **`CK_UNIFIED_ARCHITECTURE.md`** — the design of record. CPU-canonical,
   GPU-adjunct. Hardware surface audit. SNOWFLAKE scar-lattice. Full-hands
   steering posture. Swarm inventory (audit only).
2. **`OLLAMA_LEARN_LOOP.md`** — the learn-loop specification. Option A
   (external correction) implemented at `ck/fluency/`; Options B/C
   specified but not yet implemented.
3. **`ck/fluency/README.md`** — how to run the fluency server, what the
   correction log contains, how the eval harness works.
4. **`scripts/START_FLUENCY_SERVER.bat`** — the only sanctioned launch
   path. Manual-start, `--i-mean-it` gate, operator ack required.

---

## What is shipped on this branch

```
/
├── CK_UNIFIED_ARCHITECTURE.md         — design of record
├── OLLAMA_LEARN_LOOP.md               — learn-loop spec (Option A active)
├── README_CK_BRANCH.md                — this file
│
├── ck/
│   └── fluency/
│       ├── README.md
│       ├── ollama_client.py           — thin /api/generate wrapper
│       ├── ck_corrector.py            — engine scores + corrects
│       ├── correction_log.py          — append-only JSONL log
│       ├── fluency_server.py          — Flask /fluency/chat endpoint
│       ├── eval/
│       │   ├── eval_set.jsonl         — 20 curated cases
│       │   └── eval_runner.py         — green threshold ≥ 16/20 flag rate
│       └── logs/                      — rotated JSONL logs (runtime output; gitignored)
│
└── scripts/
    └── START_FLUENCY_SERVER.bat       — manual launch (--i-mean-it gate)
```

All other repo content (papers, Atlas, Gen12/Gen13 targets, clay sprint
folders, funding branches, website) is **inherited from `tig-synthesis`
and remains unchanged on this branch**. Any change to that inherited
content either (a) is cherry-picked in from `tig-synthesis`, or (b) stays
out of scope for `ck` commits.

---

## What is explicitly NOT on this branch

- **No autostart.** Nothing wires into Windows task scheduler, systemd,
  service registration, startup shortcut, or any OS autostart path.
- **No hardware triggers on import.** Every module has its entry point
  guarded by `if __name__ == "__main__":`. Importing is free; launching
  requires a named `.bat` file and operator acknowledgment.
- **No outbound auth.** No OAuth, SSO, API keys, or credential handling.
  See `CK_UNIFIED_ARCHITECTURE.md` §3.4 for the complete hard-scope limit.
- **No tunnel cutover.** The Cloudflare tunnel for coherencekeeper.com
  is started by Brayden from a separate BAT he owns; nothing on this
  branch modifies that tunnel or its config.
- **No model weights.** LoRA adapters (Option B) and base models
  (llama3.1, deepseek-r1, etc.) are local-only, never committed. The
  `ck/fluency/logs/` tree is gitignored.

---

## Parallel and downstream tracks

- **Phase 4 (active):** Ollama Option A — `ck/fluency/`. Green threshold
  is eval_runner producing ≥ 16/20 flag rate on the hand-curated set.
- **Phase 4 next (not yet scheduled):** Option B — offline LoRA cycles.
  Opens when Option A has accumulated 1–2 weeks of correction-log
  volume and the correction-type histogram shows a usable signal.
- **Phase 5.3 (parallel on master + funding/tig-snowflake):** the
  `crystalos_prereg.py` blind-run artifacts. Not on `ck`; lives in
  `docs/archive_jan2026/snowflake/blind_run_2026_04_21/` on the other
  branches per plan §5.3.

---

## Cross-branch pointers

- **Design of record for the whole project:** `README.md` on `tig-synthesis`
  (v3 navigation-first).
- **Rigor proved results:** `tig-synthesis` §7 runnable-proofs appendix
  or `README.md` §1 on `master`.
- **Execution plan this branch follows:**
  `Atlas/PLAN_RIGOROUS_EXECUTION_2026_04_21.md` (on `tig-synthesis` and `master`).
- **Funding branches (10):** not affected by `ck`. See
  `Atlas/BRANCHES_INVENTORY_2026_04_20.md` on `tig-synthesis`.

---

*Branch opened 2026-04-21 · `ck` @ branching-commit `<see git log>` ·
hands-on-wheel posture per plan G6.*
