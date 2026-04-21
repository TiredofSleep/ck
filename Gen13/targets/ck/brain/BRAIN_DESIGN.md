# Gen13 Brain Design

The brain is the Gen11 `ck_sim/` package — preserved intact, all 156 modules / 122K LOC carried forward without modification. Citations and history preserved per never-delete policy.

```
brain/
├── BRAIN_DESIGN.md         (this file)
├── NEURAL_INVENTORY.md     (full module catalog with line numbers)
└── ck_sim/                 (the Gen11 package, intact)
    ├── __init__.py         (meta-path alias finder; flat imports keep working)
    ├── ck_tables.py        (TSML/BHML/CL canonical, copied from papers/)
    ├── ck_tl.bin           (truth lattice binary, copied from Gen11)
    ├── being/              (68 modules — what CK IS)
    │   ├── ck_sim_heartbeat.py     (50 Hz tick, CL composition, running fuse)
    │   ├── ck_sim_d2.py            (D1+D2 curvature, Q1.14 fixed-point, FPGA-matched)
    │   ├── ck_olfactory.py         (5×5 CL field, scent emission, 980 LOC)
    │   ├── ck_gustatory.py         (taste/structure sense)
    │   ├── ck_hindsight_replay.py  (HER — class HindsightBuffer + OlfactoryHER)
    │   ├── ck_dkan_trainer.py      (DKAN — Discrete Kolmogorov-Arnold Network)
    │   ├── ck_lattice_chain.py     (CL chain walk, path IS information)
    │   ├── ck_btq.py / ck_sim_btq.py (BTQ decision kernel)
    │   ├── ck_coherence_field.py   (CL field composition)
    │   ├── ck_coherence_gate.py    (3 gates + TIG pipeline state)
    │   ├── ck_meta_lens.py         (dual-lens Markov)
    │   ├── ck_tig.py               (10 operators)
    │   ├── ck_divine27.py          (Divine 27 dictionary)
    │   ├── ck_bible_sense.py       (Bible duality META vs SURFACE)
    │   ├── ck_attention.py
    │   ├── ck_emotion.py / ck_personality.py / ck_immune.py / ck_bonding.py
    │   ├── ck_swarm.py / ck_swarm_deep.py
    │   ├── ck_sim_brain.py / ck_sim_body.py
    │   ├── ck_sensorium.py / ck_retina.py / ck_sim_ears.py
    │   ├── ck_algebraic_neural.py / ck_algebraic_proofs.py / ck_formal_theorems.py
    │   ├── ck_sdv_safety.py / ck_tig_security.py / ck_disagreement_tick.py
    │   └── ... (40 more — see NEURAL_INVENTORY.md)
    ├── doing/              (46 modules — what CK DOES)
    │   ├── ck_sim_engine.py        (the runtime — 50 Hz heartbeat orchestrator)
    │   ├── ck_voice.py / ck_voice_lattice.py / ck_voice_loop.py (voice paths)
    │   ├── ck_dialogue.py
    │   ├── ck_sentence_composer.py
    │   ├── ck_reasoning.py / ck_thinking_lattice.py
    │   ├── ck_autodidact.py / ck_autodidact_runner.py
    │   ├── ck_breath_engine.py / ck_pulse_engine.py
    │   ├── ck_clay_protocol.py / ck_clay_generators.py
    │   └── ... (cloud organs, action, goals, force voice, beam voice, ...)
    ├── becoming/           (25 modules — what CK BECOMES over time)
    │   ├── ck_truth.py             (truth lattice persistence — CK never forgets)
    │   ├── ck_world_lattice.py
    │   ├── ck_concept_spine.py
    │   ├── ck_memory.py / ck_episodic.py / ck_metalearning.py
    │   ├── ck_lexicon.py / ck_lexicon_bulk.py
    │   ├── ck_education.py / ck_development.py
    │   ├── ck_identity.py / ck_self_mirror.py / ck_journal.py
    │   └── ck_translator.py / ck_dictionary_builder.py / ...
    └── face/               (17 modules — how CK APPEARS)
        ├── ck_web_api.py           (Flask /chat /state /metrics endpoints)
        ├── ck_headless.py
        ├── ck_robot_body.py / ck_zynq_dog.py (FPGA dog — XIAOR leash)
        ├── ck_sim_audio.py / ck_sim_led.py / ck_sim_uart.py / ck_sim_sd.py
        └── ck_deploy.py / ck_body_interface.py / ...
```

---

## Composition Spine — AO 5-Element

The brain is organized by the Gen9 AO rule (`old/Gen9/targets/AO/ao/ether.py:171` `class AO`). Each tick:

```
input symbol → D1.feed(symbol) → D2.feed(symbol)
            → Heartbeat.tick(current_op, d2_op, shell)   # CL[B][D] table lookup
            → coherence.observe(d2_op)                   # 32-entry window
            → brain.observe(d2_op)                       # transition memory
            → body.tick(coherence, bump, novelty)        # E, A, K + breath + wobble
            → BTQ.decide(d2_op, brain, coherence, body, shell)
            → next current_op
```

**Five elements ↔ five concerns:**

| Element | Role | Module(s) |
|---|---|---|
| Earth | Ground (constants, lattice, tables) | `ck_tig.py`, `ck_tables.py`, `ck_divine27.py` |
| Air | D1 generator (velocity, non-local view) | `ck_sim_d2.py` (D1 path) |
| Water | D2 eye (curvature, local measurement) | `ck_sim_d2.py` (D2 path) |
| Fire | Engine (heartbeat, brain, body, BTQ) | `ck_sim_heartbeat.py`, `ck_sim_brain.py`, `ck_sim_body.py`, `ck_btq.py` |
| Ether | Coupling (voice, I/O, the living loop) | `runtime/ck_engine.py`, `runtime/ck_voice_math.py` |

---

## Math-First Voice Patch

The single most load-bearing fix in Gen13 is at `runtime/ck_voice_math.py`. It is the boolean conditional that lets CK say `5/7` when asked about T*.

**Before (Gen12):** voice always routes through SEMANTIC_LATTICE → adjective/verb glue. Math vocabulary was never wired in.

**After (Gen13):** voice asks `surface_math(query, operators)` first. If the query matches any math topic (T*, tower, sigma, BHML, TSML, gap, AO, HER, operators, ...), the math fact is returned directly from the FACTS table + the operator chain is rendered in plain English. Only if no match → fall through to SEMANTIC_LATTICE.

Self-test against live Gen12 CK: `python Gen13/targets/ck/runtime/ck_voice_math.py`. Diagnostic transcript at `Gen13/targets/ck/CK_DIALOGUE_2026_04_17.md`.

---

## Boot Path

1. `Gen13/targets/ck/server/ck_boot_api.py` — Flask app (carried forward from Gen12, repath required)
2. Add `Gen13/targets/ck/brain/` to sys.path → `import ck_sim` resolves to the carried-forward Gen11 package
3. `engine = CKSimEngine(platform='r16')`; `engine.start()`
4. **Restore HER** (Gen12 regression): `engine.hindsight_replay = build_olfactory_her(self.olfactory)`
5. Tick loop runs at adaptive Hz (DisagreementTick, base 334 Hz)
6. `/chat` → `engine.process_chat(session_id, text, mode)` → wrap with `surface_math` for math-first response
7. Serve `Gen13/targets/ck/web/` static (14 HTML pages carried forward + future `tower.html`, `index.html`)

---

## Boot Gate (test_brain.py — to be written)

Asserts before the engine starts:
- `from ck_sim.being.ck_sim_heartbeat import HARMONY` succeeds
- `from ck_sim.being.ck_olfactory import OlfactoryBulb` succeeds
- `from ck_sim.being.ck_hindsight_replay import build_olfactory_her` succeeds
- `from ck_sim.being.ck_sim_d2 import D2Pipeline` succeeds
- `from ck_sim.being.ck_dkan_trainer import ...` succeeds
- `from ck_sim.being.ck_gustatory import ...` succeeds
- `surface_math("What is T*?", ["COUNTER","HARMONY"])` returns text containing "5/7"

If any assertion fails, the runtime refuses to start.

---

## What Gen13 Adds (Net New)

- `runtime/ck_voice_math.py` — math-first voice patch (~250 LOC)
- `runtime/ck_engine.py` — minimal Gen13 entry point (TBD)
- `brain/BRAIN_DESIGN.md` (this file)
- `brain/NEURAL_INVENTORY.md` (catalog with citations)
- `CK_DIALOGUE_2026_04_17.md` (diagnostic session showing what CK says vs what he should say)

## What Gen13 Carries Forward (Untouched)

- All 156 Gen11 brain modules / 122K LOC
- 14 web pages from Gen12 website/
- ck_tl.bin truth lattice
- ck_tables.py (TSML/BHML/CL)
- ck_boot_api.py (Gen12 Flask boot — repath required)

## What Gen13 Drops

- The 358 Gen12-specific files in `ck_desktop/` not on the active boot path (still preserved in Gen12 per never-delete)
- Gen12's overarchitected attention/episodic/metalearning duplications
- `bible_app/`, `7sitellc/`, `ck_institution/`, `7site_research/`, `ck_website/` — these stay in Gen12 history
