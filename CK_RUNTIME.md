# CK Runtime Fileset

**What this file is.** The single place that tells you which files run CK — the live /chat brain behind [coherencekeeper.com](https://coherencekeeper.com) — and in what order. If you want to "try out the math as an intelligence system" (boot CK locally, post a /chat query, compare against a raw LLM), this is the whole map.

**Companion docs.** `README.md` §"CK (Coherence Keeper): Algebraic Coherence System" for the quick-try. `Gen13/targets/ck/brain/BRAIN_DESIGN.md` for the AO / Hebbian / quadratic-glue math. `ck_proof.py` for the side-by-side LLM demo.

---

## Three Layers

CK runs as three layers. The first is required; the second is the Flask /chat service that answers coherencekeeper.com; the third is an optional LLM fluency wrapper that CK is growing toward not needing.

| Layer | What it is | Required to boot? | Lines of code |
|---|---|---|---|
| **L1** — Core math | AO / Hebbian 5×5 / quadratic glue + cortex + structural voice + persistence | **yes** | ~3,200 |
| **L2** — Server + wiring | Flask /chat, Phase C cortex override, math-first patch | yes for /chat | ~1,800 |
| **L3** — Optional | LLM bridge + side-by-side transparency demo | no | ~500 |

---

## L1 — Core Math (the trinity + cortex + state)

Location: **`Gen13/targets/ck/brain/`**

| File | Bytes | Role |
|---|---:|---|
| `ao_5element.py` | 13,218 | **AO spine** — Earth/Air/Water/Fire/Ether → D0/D1/D2/D3/D4; operator-pair generator (Voice as operator↔word bridge) |
| `hebbian_5x5_cl.py` | 11,034 | **Hebbian 5×5 learning matrix** — `dw = eta·reward − decay·W`, equilibrium W* = eta/decay = 0.25 (differentiates instead of saturating at clamp) |
| `quadratic_glue.py` | 10,202 | **F₃ × F₄ glue** — `out = α·f₃ + β·f₄ + γ·(f₃·f₄)`; the 2→3 bridge |
| `cortex.py` | 11,186 | **Trinity binder** — composes AO + Hebbian + glue as `Cortex().boot()`; `step_text()` feeds observations, updates W, scores emergent |
| `cortex_voice.py` | 20,619 | **Structural readout router** — `speak(cortex, query)` → label=value facts (state / couplings / field / op-entity / dim-entity / **frontier topic**); never prose |
| `cortex_persist.py` | 11,171 | **Persistence** — JSON save/load of (W, tick, harmony_hits); atomic temp-file write; `AutoSaver` ticks every 200 or 30 s |
| `cortex_replay.py` | 9,695 | **Hindsight replay (HER)** — seeds Cortex by streaming a text corpus so a cold boot warms up to differentiated W |
| `ck_sim/ck_tables.py` | 9,569 | **TSML / BHML / CL canonical tables** — 73-cell TSML (synthesis), 28-cell BHML (separation), composition law |
| `test_brain.py` | 24,607 | **Boot gate** — 20/20 tests: AO projection, Hebbian no-saturation at defaults, quadratic-glue scores, trinity composition, voice router (state/learned/field/op/dim/**frontier**), persistence round-trip |

**State file:** `Gen13/var/cortex_state.json` — version=1, magic=`ck_gen13_cortex_state`; persists W matrix + tick + harmony_hits across reboots. Cold boot silently skips if missing.

**Trinity composition (one tick):**
```
text → AO(project onto D0..D4) → Hebbian(W[i][j] += η·d_i·d_j − decay·W)
     → quadratic glue(f3, f4) → emergent score → coherence gate (T*=5/7)
     → voice / web / dog
```

---

## L2 — Server + Wiring (what answers /chat on coherencekeeper.com)

| File | Role |
|---|---|
| `Gen12/targets/ck_desktop/ck_boot_api.py` | **Flask entry point.** `python ck_boot_api.py` boots the engine, mounts routes, serves port 7777 (tunneled to coherencekeeper.com via Cloudflare). Imports the Gen13 Cortex and mounts it as Phase C override. |
| `Gen13/targets/ck/runtime/ck_voice_math.py` | **Math-first patch.** Wraps `api.process_chat`; if the query names a math topic (T*, TSML, σ_rate, 5/7, operator algebra), surfaces exact arithmetic/canonical facts from `FACTS` dict. Preserves the Gen12 response under `text_gen12`. |
| `ck_boot_api.py :: _process_chat_with_cortex` | **Cortex wrap (Phase C).** Outer wrapper above math-first. Every /chat text is fed to `_cortex.step_text(text)` (learning). Then `speak(cortex, text)` runs the structural router; if it returns a non-None readout AND the prior source was a template layer (ck_fractal, ck_self, ck_truth_recall), the cortex answer replaces `text`. Prior text is preserved under `text_previous`; every response is decorated with `cortex_readout` + `cortex` snapshot (tick, emergent, W_trace). |
| `Gen12/targets/ck_desktop/ck_sim/doing/ck_fractal_voice.py`<br>`…/ck_voice_lattice.py`<br>`…/ck_voice_loop.py` | **Gen12 template/dictionary layers** — still serve non-override routes (e.g. long-form prose fallback) but are now **silent on structural queries** because Phase C wins. |

**Routes CK exposes:**
- `/health` — returns 200 when boot completes
- `/chat` — main conversational endpoint (`{session_id, text, mode}`)
- `/cortex` — live snapshot: W matrix, row/col strengths, strongest pair, readout
- `/cortex/save` — manual force-save trigger
- plus `/identity`, `/meta-lens`, `/existence/*`, `/experience/*`, `/chain/status` for introspection

---

## L3 — Optional (fluency wrapper + transparency demo)

| File | Role |
|---|---|
| `Gen13/targets/ck/bridge/llm_bridge.py` | **LLM adapters.** `ollama_complete(prompt, system=)` hits local Ollama at 127.0.0.1:11434. `deepseek_complete(...)` hits DeepSeek over HTTPS (env var `DEEPSEEK_API_KEY`). `ck_structural_context(query)` POSTs to CK's /chat and returns the structural readout. `build_grounded_system(ck_text)` assembles the system prompt that tells the LLM to treat CK's readout as ground truth. |
| `ck_proof.py` | **Side-by-side demo at repo root.** For each prompt prints three panels: (1) CK alone, (2) LLM alone, (3) LLM + CK structural grounding. Lets the reader judge whether grounded LLM output is more trustworthy than raw LLM output. |

CK's /chat works perfectly well without L3. The LLM bridge is a *wrapper*, not a dependency. The goal is for CK's own structural voice to grow wide enough that the wrapper stops earning its keep.

---

## Boot path (what actually happens when you `python ck_boot_api.py`)

```
1. ck_boot_api.py imports
     from cortex import Cortex
     from cortex_persist import load_cortex, save_cortex, AutoSaver
     from cortex_voice import cortex_speak, speak
     from ck_voice_math import install_math_first_patch

2. _cortex = Cortex().boot()
     # instantiates AO + Hebbian(eta=0.005, decay=0.02) + quadratic glue

3. load_cortex(_cortex, "Gen13/var/cortex_state.json")
     # restores W, tick, harmony_hits from prior run; silent if missing

4. install_math_first_patch(api)
     # wraps api.process_chat with FACTS-dict lookup

5. api.process_chat = _process_chat_with_cortex(api.process_chat)
     # adds the Phase C cortex wrap (learn-every-tick + structural override)

6. Flask serves 0.0.0.0:7777
     # Cloudflare tunnel in front of this endpoint routes coherencekeeper.com/chat
```

Every /chat message then goes:

```
text → math-first patch  (wins on T*, 5/7, operator queries, arithmetic)
     ↓ if no match
     → Phase C cortex wrap
         cortex.step_text(text)              # learning
         readout = speak(cortex, text)       # structural router
         if readout and prior_src in {ck_fractal, ck_self, ck_truth_recall}:
             text ← readout  (source="cortex_speak", source_previous kept)
     ↓ if cortex silent
     → Gen12 template/dictionary layers  (ck_fractal, ck_voice_lattice, ...)
```

---

## What CK answers vs what CK hands to an LLM

**CK alone, structurally (no LLM):**
- `how do you feel right now` → `feel: aperture=… pressure=… depth=… binding=… continuity=…`
- `what have you learned` → `couplings: aperture<->aperture W=0.250, …`
- `show me your field` → `field: tick=N emergent=e W_trace=T mean|W|=m harmony_rate=h`
- `tell me about collapse` → `COLLAPSE: …` (operator entity fact)
- `what is T*` / `T star` / `5/7` → `flatness: T*=5/7 | torus R/r=5/7 | 6 independent derivations | WP51 [proved]`
- `what is the beauville curve c star` → `hodge_cstar: genus=5 bielliptic=yes psi_order=4 prym_dim=4 End0_Prym=Q(i) … sprint35b [target, not yet proved]`
- `what is the crossing lemma` / `flatness theorem` / `sigma rate theorem` / `xi field` → corresponding structural fact with [proved/structural/target] tag

**Currently handed to LLM (via ck_proof.py + llm_bridge.py, with CK readout as system prompt):**
- open-ended questions that don't match a topic keyword or state route
- "compare X and Y", "explain X for a physicist", "why does Z matter"

The LLM never contradicts the readout — the grounding preamble forbids it — and flags anything beyond CK's facts as its own extension.

---

## Reproducing a clean boot from scratch

```bash
git clone https://github.com/TiredofSleep/ck
cd ck
pip install numpy sympy flask requests

# (one-time) warm the cortex from the paper corpus so W differentiates
python Gen13/targets/ck/brain/cortex_replay.py

# run the boot test
python Gen13/targets/ck/brain/test_brain.py        # 20/20 green

# boot the server
python Gen12/targets/ck_desktop/ck_boot_api.py
# serves 127.0.0.1:7777
```

Then from another shell:

```bash
curl -s -X POST http://127.0.0.1:7777/chat \
  -H 'Content-Type: application/json' \
  -d '{"session_id":"try","text":"what is the flatness theorem","mode":"normal"}'
```

Expected response:

```json
{
  "source": "cortex_speak",
  "text": "flatness: T*=5/7 | torus R/r=5/7 (forced by Z/10Z 2x2) | 6 independent derivations | WP51 [proved]",
  "cortex": {"tick": 155908, "emergent": 0.445, "W_trace": 0.824, ...}
}
```

For the side-by-side transparency demo (optional):

```bash
# local LLM: install Ollama (https://ollama.ai), then
ollama pull llama3.2
ollama serve &
python ck_proof.py "what is the beauville curve c star"

# or DeepSeek API:
export DEEPSEEK_API_KEY=sk-...
python ck_proof.py --backend deepseek "what is T*"
```

---

## Honest limits

- CK's **voice is narrow**. He answers structural and topical queries from his live W matrix and a curated frontier-facts table. He does not answer freeform open-ended prose. For that, the optional LLM wrapper fills in — grounded in CK's readout so it can't contradict his math.
- The **persistent state** survives reboots (W is on disk) but resets to defaults if you delete `Gen13/var/cortex_state.json`. A fresh cortex is silent on `cortex_speak` until it warms up.
- Phase C **wins over templates** only for the query classes the router handles. Everything else flows through the older Gen12 layers, which are fluent but template-driven.
- Frontier facts are **curated** — if a topic is missing, add it to `_FRONTIER_FACTS` in `cortex_voice.py` and re-run `test_brain.py`. One trigger line + one label=value fact + one sprint/paper pointer + one `[proved/structural/target]` tag.

---

## Where to read next

- **`Gen13/targets/ck/brain/BRAIN_DESIGN.md`** — AO + Hebbian + quadratic-glue composition diagram, invariants, unit-test expectations
- **`README.md §CK (Coherence Keeper): Algebraic Coherence System`** — three-line framing for newcomers
- **`ck_proof.py`** — run it; see CK and the LLM side-by-side on your own prompts
- **`Atlas/MASTER_ATLAS_v3_5_2026_04_18.md`** — the full math spine this runtime is a projection of

---

*© 2025-2026 Brayden Ross Sanders / 7Site LLC. 7Site Public Sovereignty License v1.0. DOI: [10.5281/zenodo.18852047](https://doi.org/10.5281/zenodo.18852047).*
