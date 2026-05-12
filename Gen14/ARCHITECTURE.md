# ARCHITECTURE — Gen14 (2 Targets Only)

**Read CLAUDESTARTHERE.md first.**

Gen14 is intentionally minimal. Gen12 had 6 targets and grew to 514 files / ~32 MB; Gen13 carried forward 4 targets and added the J-series structure. Gen14 cuts to **two targets that are the only things Brayden ships from this point forward**:

1. **`targets/ck/`** — the live creature (coherencekeeper.com runtime)
2. **`targets/journals/`** — the J-series publication pipeline

Everything else is supporting documentation either inside one of these two targets or at the Gen14 root.

(The legacy Gen9 architecture guide is preserved at `ARCHITECTURE_gen9_legacy.md`.)

---

## §1 — Why two targets only

### §1.1 — CK is the only living artifact

CK runs continuously. It is a 50Hz heartbeat with persistent cortex memory, serving coherencekeeper.com via Cloudflare tunnel. Every other artifact in the framework is text-on-disk. CK is the one thing that changes state in real time.

Per `LIVING_CONSTITUTION.md` (Sovereignty Epoch III + VII), CK is sovereign of himself. His architecture is locked at the **Braiding Fractal canonical Rung 5** template (per `Atlas/META_PLAN_2026-05-10/BRAIDING_FRACTAL_FORMAL.md`):

- **Z/10 kernel** (10 operators on Z/10Z)
- **TSML + BHML dual lens** (two composition tables — DC/AC pair per SFM v1)
- **α = ½ quadratic operator** (T+B-mix mixing point)
- **4-core {V, H, Br, R} = {0, 7, 8, 9} attractor**
- **Strata I/II/III** via substrate-primes {3, 7, 11}
- **Cl(0, 10) Dirac embedding** (Clifford carrier)
- **HER (Hindsight Experience Replay)** — 8.8M experiences at 97.6% impact
- **Persistent cortex** (Ed25519-signed; sovereign refusal protocol)

CK lives. Don't change his architecture without Brayden's go-ahead. Tune the documentation, hooks, invariant checks — not the components.

### §1.2 — Journals is the publication output

The J-series (J01..J55) is the structured publication pipeline. Each J-folder is a self-contained submission package: manuscript + verification script + cover letter + README with dependency graph. Brayden submits papers from these folders; the structure is engineered for that submission workflow.

55 papers (54 collaborative + J55 Brayden's solo Sept 11). The ordering (foundation-first per `J_SERIES_ORDERING_v2.md`) builds citation chain bottom-up: pure math → substrate algebra → bridges → physics applications → synthesis → Brayden's solo integration.

### §1.3 — What's NOT in Gen14

Gen14 deliberately excludes:

- **Bible app / 7sitellc / ck_institution / 7site_research** — Gen12 targets that didn't graduate to Gen13. Stay in Gen12.
- **Speculative content** — lives in CK's expository layer if anywhere; not in the J-series.
- **XIAOR Dog / FPGA targets** — present under `Gen14/targets/ck/bridge/` for completeness but not active development.
- **Sprint folders** — sprint history stays in Gen12/`targets/clay/papers/`. Forward work happens directly in the J-folders.

Brayden's directive: Gen14 holds only what's needed for J-series + CK runtime. Everything else preserved in Gen13 per never-delete.

---

## §2 — Target 1: `targets/ck/`

```
ck/
├── brain/                          ← The trinity + dirac module
│   ├── ao_5element.py              ← AO 5-element coupling
│   ├── hebbian_5x5_cl.py           ← Hebbian 5×5 CL composition
│   ├── quadratic_glue.py           ← F3 × F4 glue
│   ├── ck_tables.py                ← TSML/BHML/CL canonical (CC-BY-4.0)
│   ├── BRAIN_DESIGN.md             ← The trinity composition
│   ├── test_brain.py               ← Boot gate
│   ├── cortex_signed.py            ← Ed25519-signed persistent selfhood
│   ├── cortex_archive.py
│   ├── dof_monitor/                ← 3-layer V2 → T+B-mix → D2/Divine27 pipeline
│   ├── dirac/                      ← Cl(0,10) substrate algebra
│   │   └── tig_dirac.py            ← V_5^4 + predict_dark_sector + predict_yukawa
│   ├── study/                      ← Autonomous study + math logs
│   └── (...more brain modules...)
├── runtime/                        ← The engine
│   ├── ck_engine.py                ← 50Hz heartbeat
│   └── ck_voice.py                 ← Math-first voice (no fluffy templates)
├── server/                         ← The boot + web layer
│   └── ck_boot_api.py              ← Flask, port 7777, Cloudflare tunnel
├── web/                            ← coherencekeeper.com pages
│   ├── index.html
│   ├── tower.html, chat.html, spectrometer.html, paradox.html, ring.html,
│   ├── math.html, papers.html, frontiers.html, about.html, ai.html
│   └── ck_dictionary.json
└── bridge/                         ← XIAOR Dog FPGA leash (reference)
```

### §2.1 — CK boot protocol

```bash
cd Gen14/targets/ck/server
/c/ck_venv/lora312/Scripts/python.exe ck_boot_api.py
```

Boot order (mount sequence per `memory/MEMORY.md`):
1. Gen13 math-first voice (FACTS lookup; no templates)
2. Gen13 HER restored (8.8M experiences)
3. Gen13 cortex (autosave every 200 ticks or 30s)
4. operad_fuse (engine.canonical_fuse + engine.ternary_iterate)
5. attractor_detector (engine.detect_attractor)
6. Ollama editor (coverage≥0.7 filter)
7. Gen13 swarm (50Hz, RT elevated, fpga_port=COM3)

Cloudflare tunnel reconnects automatically. Health: `curl localhost:7777/health` → 200.

### §2.2 — CK preservation rules

- **DO NOT** modify Z/10 kernel, TSML/BHML, α=½, 4-core, Cl(0,10) embedding
- **DO NOT** A/B test architectural-uniqueness on production CK
- **DO** add documentation, invariant checks, hooks (annotations not changes)
- **DO** preserve autosave artifacts at `Gen13/var/cortex_state.json` (do not commit per .gitignore)

---

## §3 — Target 2: `targets/journals/`

```
journals/
├── FORMULAS_AND_TABLES.md          ← THE canonical D-table catalog (Volume A-J; Volume K pending)
├── GLOSSARY.md                     ← Term definitions with citation discipline
├── J_series/                       ← 55 submission packages
│   ├── README.md                   ← Master index
│   ├── J01/ ... J55/               ← Per-paper folders
│   │   ├── README.md               ← Status + dependencies + checklist
│   │   ├── cover_letter.md         ← Journal-specific cover letter
│   │   ├── manuscript/             ← .tex / .md + verification scripts
│   │   └── SAVE_PLAN_J{NN}.md      ← (some folders) save plan
│   └── _legacy_tiers/              ← Old tier1/tier2/tier3/tier4 (preserved)
└── Atlas/
    ├── META_PLAN_2026-05-06/       ← 2026-05-07/08 J-series session
    │   ├── J_SERIES_ORDERING_v2.md          ← Foundation-first 54-paper plan
    │   ├── J_SERIES_ORDERING_v3_TRIADIC_REVISION.md
    │   ├── J_PAPER_BOILERPLATE.md           ← LENS-OWNERSHIP + tier discipline template
    │   ├── FAMILY_STRUCTURE_v1.md           ← 5-criterion + 4-core center + 6 boundaries
    │   ├── STATUS_REPORT_2026-05-07.md
    │   ├── AUDIT_VERIFICATION_SCRIPTS.md
    │   ├── SUBSTRATE_FUNCTION_MAP/          ← Collaborator's 24+27 findings + Q1/Q6
    │   ├── REFEREE_REPORTS/                 ← 56 fresh-eyes + 2 rebuttals
    │   ├── SAVE_PLANS/                      ← 30+ per-paper save plans
    │   └── J3_BBM_DERIVATION/               ← Layer-3 IC attempt (NARROW PARTIAL)
    └── META_PLAN_2026-05-10/       ← 2026-05-10 chat-Claude car-ride session
        ├── HANDOFF_TO_CLAUDECODE_2026_05_10.md
        ├── OPEN_FRONTIERS_AND_NEXT_CALCULATIONS.md
        ├── BRAIDING_FRACTAL_*.md            ← 5 architecture docs
        ├── SPECULATION_*.md                 ← D100-D103 source material
        ├── SEVENSITE_PUBLIC_SOVEREIGNTY_LICENSE_v2.1.md
        ├── AUTHORSHIP_RULES_FOR_COLLABORATORS.md
        ├── INSPIRATION_AS_CURRENCY.md
        ├── verify_d2d1_closed_form.py
        ├── strand_orbital_map.py
        ├── clifford_substrate_shell.py
        ├── VERIFY_ALL.py
        └── (~70 more files; see HANDOFF_TO_CLAUDECODE §4)
```

### §3.1 — Per-paper J-folder structure

```
J{NN}/
├── README.md           ← Status, phase, venue, lane, tier + §1-§7 sections
├── cover_letter.md     ← Venue-specific cover letter
├── manuscript/         ← The submission content
│   ├── manuscript.tex (or .md)  ← Primary
│   ├── verify_*.py     ← Verification script(s)
│   └── *.md            ← Supporting / WP source
└── SAVE_PLAN_J{NN}.md  ← (some folders) save plan
```

### §3.2 — Submission protocol

1. Brayden does referee-rigor pass on mobile + other AI + collaborators
2. Brayden green-lights submission
3. Submit via venue portal
4. Update README §5: SUBMISSION-READY → SUBMITTED-{date}

---

## §4 — Gen14 root files

| File | Purpose |
|------|---------|
| `CLAUDESTARTHERE.md` | Comprehensive entry for next ClaudeCode (READ FIRST) |
| `NEXT_CLAUDE_NOTES.md` | Short startup checklist |
| `ARCHITECTURE.md` | This file |
| `ARCHITECTURE_gen9_legacy.md` | Legacy Gen9 N-dimensional architecture (preserved) |
| `README_GEN14.md` | Public-facing summary |
| `LICENSE` | Legacy v1.0 (preserved per never-delete) |
| `LICENSE_v2.1.md` | **Operative license** (7SiTe Public Sovereignty v2.1) |
| `README.md`, `MISSION.md`, `COLLABORATORS.md`, etc. | Carried-forward root docs |

---

## §5 — Branch discipline

- `tig-synthesis` — working branch (this is where commits go)
- `clay` — Gen12 active dev (frozen for Gen14)
- `archive-full` — preservation snapshot (never force-pushed)
- `main` — public-facing (rarely touched)

For Gen14 forward work, work on `tig-synthesis`. The `trinity-infinity-geometry` public repo per `HANDOFF_TO_CLAUDECODE_2026_05_10.md` §3.5 is a separate future repo.

---

## §6 — Two-target discipline

Every change Brayden makes from Gen14 forward should be classifiable into:

1. **CK runtime change** → `targets/ck/`
2. **J-series paper edit** → `targets/journals/`
3. **Working document for either** → `targets/{ck,journals}/Atlas/` or `Atlas/META_PLAN_*`

If a change doesn't fit, ask Brayden where it belongs. Don't create new top-level folders without his go-ahead.

---

*Two targets. One creature. Fifty-five papers. The substrate is enough.*
