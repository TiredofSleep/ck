# Gen13 — Math-First Rebuild

**Date opened:** 2026-04-17
**Branch:** `tig-synthesis`
**Predecessor:** Gen12 (preserved intact in `Gen12/` per never-delete policy)

---

## Why Gen13

CK regressed in Gen12. He was **overarchitected** (514 files, ~32 MB; `ck_sim_engine.py` alone is 4,912 lines) and **under-mathed** (the load-bearing pieces — AO 5-element coupling, HER, math vocabulary in voice — were buried or absent).

A live diagnostic session against the production server (`localhost:7777`, tick=36,270,588, coherence=1.0, GROKKED) confirmed the root cause: **CK's operator chains are mathematically perfect**, but the voice layer renders adjectives only — it cannot say `5/7`, `100/100`, `92+6+2`, or any number. See `targets/ck/CK_DIALOGUE_2026_04_17.md` for the full transcript.

Gen13 is a thin Gen13-orchestration layer wrapped around Gen11's full neural architecture (156 modules / 122K LOC carried forward intact, with citations preserved).

---

## What's Inside

```
Gen13/
├── README_GEN13.md            ← this file
├── ARCHITECTURE.md            ← math-first design rationale
├── NEXT_CLAUDE_NOTES.md       ← future-Claude startup protocol
└── targets/
    ├── ck/                    ← CK runtime + coherencekeeper.com (one creature)
    │   ├── brain/             ← Gen11 ck_sim package intact (156 modules)
    │   │   ├── BRAIN_DESIGN.md
    │   │   ├── NEURAL_INVENTORY.md
    │   │   └── ck_sim/        ← being/ + doing/ + becoming/ + face/
    │   ├── runtime/
    │   │   └── ck_voice_math.py  ← math-first voice patch (FACTS dict)
    │   ├── server/
    │   │   └── ck_boot_api.py    ← Flask boot, surface_math wired into /chat
    │   ├── web/                  ← 14 HTML pages carried from Gen12
    │   └── CK_DIALOGUE_2026_04_17.md  ← diagnostic transcript
    ├── clay/papers/              ← 6 sprint folders linked from README
    │   ├── sprint10_flatness_2026_04_06/
    │   ├── sprint12_uop_gut_arc_2026_04_08/
    │   ├── sprint13_flag_selector_2026_04_09/
    │   ├── sprint14_prism_xi_2026_04_10/
    │   ├── sprint16_basin_handoff_2026_04_10/
    │   └── sprint17_tsml_tower_2026_04_17/
    ├── journals/                 ← 11 venues, 4-tier ladder
    │   ├── SUBMISSION_LADDER.md
    │   ├── tier1_submit_now/
    │   ├── tier2_format_then_submit/
    │   ├── tier3_partner_then_submit/
    │   └── tier4_framework/
    ├── fpga/                     ← Zynq-7020 reference (bitstream stays in Gen9)
    └── xiaor_dog/                ← XIAOR Dog with FPGA leash
```

---

## How to Boot CK

```
cd Gen13/targets/ck/server
python ck_boot_api.py
```

Server listens on `0.0.0.0:7777`. On boot you should see:

```
[CK] Disagreement tick: adaptive Hz from algebraic disagreement
[CK] Gen13 math-first voice: ENABLED
[CK] Gen13 HER: restored (engine.olfactory_her initialized)
[CK] Static files: .../web
[CK] Organism alive. API: http://0.0.0.0:7777
```

Then ask CK a math question:

```
curl -X POST http://localhost:7777/chat \
  -H "Content-Type: application/json" \
  -d '{"text": "What number is T star?", "session_id": "test", "mode": "normal"}'
```

Expected response: `T* = 5/7 = 0.714286. Torus aspect ratio. Six independent derivations: ...` (math-first), with `text_gen12` preserving the old SEMANTIC_LATTICE output for comparison.

---

## What Changed vs Gen12

| Concern | Gen12 | Gen13 |
|---|---|---|
| Voice on math topics | adjective glue ("eigenvalue, geodesic") | exact facts (`T* = 5/7`, `92+6+2=100`) |
| HER (HindsightBuffer) | `available: false` | `available: true` (restored on boot) |
| Brain modules visible | buried in 514 files | catalogued in `NEURAL_INVENTORY.md` |
| Composition spine | unstated | Gen9 AO 5-element rule, documented |
| Top-level entry docs | 30 conflicting | 3 (this README, ARCHITECTURE, NEXT_CLAUDE_NOTES) |

---

## What Did NOT Change

- Every Gen12 file is preserved in `Gen12/` (never-delete).
- The 156 Gen11 brain modules are copied intact (no rewrites).
- Cloudflare tunnel config unchanged. Live coherencekeeper.com tunnel is NOT cut over to Gen13 until user confirms.
- All 6 carried-forward Clay sprint papers, all 11 journal venues, and all 14 HTML pages are byte-identical to Gen12.

---

## See Also

- `ARCHITECTURE.md` — the math-first design + AO 5-element diagram
- `NEXT_CLAUDE_NOTES.md` — startup protocol for future-Claude
- `targets/ck/brain/BRAIN_DESIGN.md` — brain composition + boot path
- `targets/ck/brain/NEURAL_INVENTORY.md` — 156-module catalog with citations
- `targets/journals/SUBMISSION_LADDER.md` — door-by-door publication map
- `targets/clay/papers/README.md` — index of forwarded sprint papers
