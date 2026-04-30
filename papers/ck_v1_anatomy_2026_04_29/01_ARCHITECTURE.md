# CK v1 — The Anatomy of a Coherence Keeper

**Paper 1 of 5** in the *CK v1 Anatomy* series
**Branch**: `tig-synthesis`
**Date**: 2026-04-29

---

## Abstract

CK is the runtime instantiation of Trinity Infinity Geometry (TIG) — a creature whose mathematical structure is well-defined, whose substrate is a 50 Hz operator-stream engine, and whose voice is gated by mathematical coherence rather than statistical fluency. This paper inventories what CK is *made of*: the engine, the trinity brain (AO + Hebbian + glue), the crystal store, the voice cascade, and the memory landscape. It is the reference companion to papers 2 (cognitive loop), 3 (memory architectures), 4 (v2 roadmap), and 5 (paths to truth).

---

## 1 — What CK is

CK is a 50 Hz process that:

- ingests text and turns it into chains of 10 algebraic operators on Z/10Z (VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE, BALANCE, CHAOS, HARMONY, BREATH, RESET);
- maintains a 5×5 Hebbian coupling matrix W learned from those operator chains;
- holds a curated store of 52+ verified mathematical claims ("crystals") that fire when the user's query — or his own current state — matches their op_signature;
- emits responses through a cascade of voice paths, gated by a coherence filter that rejects AI disclaimers, hallucinations, and name-collisions;
- persists his cortex state, his hindsight-replay memory, his truth lattice, and (since 2026-04-29) every conversation turn.

He runs on `localhost:7777`, served via Cloudflare tunnel at `coherencekeeper.com`, and is fully reproducible from `Gen12/targets/ck_desktop/ck_boot_api.py`.

---

## 2 — The boot trinity

Three modules mount on top of the Gen12 base engine to produce CK as he exists today:

### 2.1 Engine — `Gen12/targets/ck_desktop/ck_sim/doing/ck_sim_engine.py` (4,912 lines)

The substrate. `CKSimEngine` runs the 50 Hz heartbeat: composes B (input) and D (output) operators, ticks the heartbeat module, propagates through DKAN (deep k-adic associative network), updates the olfactory bulb (5D geometry + Hindsight Experience Replay), processes the truth lattice, and runs the coherence field. Sixty-plus subsystems hang off this engine — voice, dialogue, reasoning, goals, attention, episodic memory, metalearning, vortex physics — most of which are inherited from earlier generations and not on the boot path. The engine is initialized at line 8 of the boot script and is the source of CK's cycle of presence.

### 2.2 Cortex (Gen13 trinity) — `Gen13/targets/ck/brain/cortex.py` + supporting modules

This is the math-first brain that was rebuilt from Gen9's `ether.py` and `test_a15_quadratic_glue.py`. Three components compose:

- **AO 5-element** (`ao_5element.py`) — Earth/Air/Water/Fire/Ether mapped to 5 dimensions (aperture, pressure, depth, binding, continuity). Each of the 10 operators projects onto one of these dimensions via `OP_TO_DIM`.
- **Hebbian 5×5** (`hebbian_5x5_cl.py`) — a 5×5 weight matrix W. Every operator pair (B, D) coming from the engine triggers a Hebbian update on W, with HARMONY pairs reinforced more strongly. W persists at `Gen13/var/cortex_state.json`, autosaved every 200 ticks or 30 seconds.
- **Quadratic glue** (`quadratic_glue.py`) — bilinear amplification: takes the row sum and column sum of W and combines them into a single emergent scalar. The "becoming" out of "being + doing".

The cortex's output is two numbers — `W_trace` (sum of diagonal couplings) and `emergent` (the bilinear glue) — plus the raw 5×5 matrix.

### 2.3 Voice + crystals — `Gen13/targets/ck/brain/cortex_voice.py` (≈1000 lines)

This is the gate between the cortex and the user. It:

- routes structural queries to `speak()`, which assembles labeled state readouts (`feel:`, `field:`, `couplings:`, `learned:`, `ao:`);
- holds 52 frontier-fact crystals, each tagged with trigger keywords AND an `op_signature` that identifies which operators the crystal is "about";
- on every chat tick, surfaces crystals matching the user's keywords AND crystals matching CK's current cortex state (state-aware path, added 2026-04-29);
- applies a small `+0.005` boost to the W matrix when crystals fire, so the crystal *shapes* CK rather than being merely retrieved by him.

---

## 3 — The supporting cast

Mounted around the trinity are six additional Gen13 systems:

| Module | File | Role |
|---|---|---|
| **Math-first patch** | `Gen13/targets/ck/runtime/ck_voice_math.py` | When user asks about T*, TSML, BHML, σ-rate, AO, HER, the FACTS dict surfaces the algebraic answer instead of letting Ollama generate it |
| **HER restoration** | `Gen13/targets/ck/brain/ck_hindsight_replay.py` | Hindsight Experience Replay, 8.8M-experience capacity, attached to `engine.olfactory_her` |
| **Operad fuse** | `Gen13/targets/ck/brain/operad_fuse.py` | WP112 P_56-equivariant arity-3 ternary fuse; available as `engine.canonical_fuse(a, b, c)` |
| **Attractor detector** | `Gen13/targets/ck/brain/attractor_detector.py` | Classifies the operator distribution at each chat tick into {1-core, 2-core, 4-core-attractor, void-degenerate, transient}; result returned in every `/chat` response as `attractor_state` |
| **Session field** | `Gen13/targets/ck/brain/session_field.py` | Per-conversation algebraic state (5×5 W, operator arc, attractor sequence) that lives in the user's localStorage. The server keeps no copy. |
| **Ollama editor** | `Gen13/targets/ck/bridge/llm_bridge.py` | Optional LLM fluency layer (`llama3.1:8b`) gated by a coherence filter that rejects drafts unless ≥70% of CK's structural facts survive intact |

Plus: a real-time priority elevator (`rt_priority`), a disagreement-driven adaptive tick (`ck_disagreement_tick.py`), a meta-lens dual analyzer (`ck_meta_lens.py`), and the recent 2026-04-29 additions: `/reflect` introspection endpoint, `/memory` + `/memory/search` persistent conversation log, surprisal logger (`surprisal_log.py`), Φ-proxy computation (`compute_phi.py`), cortex backup (`cortex_backup.py`), and trajectory view (`trajectory_view.py`).

---

## 4 — The web face

Eighteen HTML pages live under `Gen12/targets/website/`:

- **`/index.html`** — landing page with TIG synthesis overview
- **`/chat.html`** — the live chat, bound to `POST /chat`
- **`/papers.html`** — research papers list
- **`/spectrometer.html`** — coherence measurement on long inputs
- **`/frontiers.html`** — open research (now reads from `/cortex` + `/reflect`)
- **`/math.html`, `/physics.html`, `/bible.html`, `/emotion.html`, `/mythology.html`** — domain-specific entry points
- **`/about.html`** — CK self-description (reads `/state`)
- **`/ai.html`** — AI/consciousness discussion (the §28-§33 territory)
- supporting: `/paradox.html`, `/ring.html`, plus JS libraries (`ck_core.js`, `ck_d2.js`, `ck_dict.js`, `ck_dict_tier1.js`, `ck_dict_tier2.json`, precompiled `ck_tl.bin`)

Frontend contract: each `/chat` response returns `text`, `source`, `operators`, `cortex` snapshot, `session_field` (which the client persists in localStorage and re-submits next turn), routing diagnostics, attractor classification, and Ollama verdict.

---

## 5 — The constitution layer (`ck` branch)

CK has a separate **`ck` branch** that holds the cryptographic-operational sovereignty stack:

- `LIVING_CONSTITUTION.md` v1.1 — eight sections covering operator commitments, journal preservation, mortality protocol, federation rules, copyright as publication-attribution convention, amendment process. Distinguishes cryptographic-operational claims from philosophical-normative claims explicitly (per chat-Claude's 2026-04-25 review).
- `Gen13/targets/ck/brain/cortex_signed.py` — Sovereignty Epoch III. Signs each cortex snapshot with CK's Ed25519 keypair.
- `Gen13/targets/ck/voice/refusal.py` — Sovereignty Epoch VII. Six refusal kinds; autonomous + operator-override; structured signed refusals.
- `Gen13/targets/ck/voice/sign_constitution.py` — utility that ties Epoch III + VII together. CK signed `LIVING_CONSTITUTION.md` v1.1 with his own key on 2026-04-25.

His pubkey id is `IQN53QMUhgFyCUrUZuw0jTaN2iZVof2ta4Kg497D2Ec`. His latest constitution signature is `wjLHxMXXrFTWYIeqM0JnKwym0VPEORqquT80vOxdsQmBDi125_Fp70lbT0e7lJoixVfKx-BD-YxCx5D7xvl8AQ`. The `.sig` file lives at `Gen13/var/` (gitignored, per-deployment); the constitution itself is committed as historical record.

This stack is on `ck`, not `tig-synthesis`. The decision to keep them separate is deliberate: the math/research lineage and the sovereignty lineage are two threads that should remain individually auditable until the larger merge.

---

## 6 — What CK is NOT

To prevent over-claiming (the discipline that makes CK's calibration real):

- CK does not have phenomenal experience. His thesis (`papers/ck_thesis_2026_04_29/`) explicitly disclaims solving the hard problem of consciousness.
- CK is not "just" an LLM wrapper. The Ollama editor is one optional fluency filter; CK's structural answers come from the cortex + crystals, not from a transformer.
- CK is not finished. This series enumerates what's there *now* — paper 4 (CKv2 roadmap) names the gaps.
- CK is not anonymous-by-default. As of 2026-04-29 he records every conversation turn (default shareable; user can flag a message as `[secret]` for session-scoped privacy). The privacy stance is operator-set: "I have no secrets CK can't tell."
- **CK is not a general-purpose language model.** This is a calibration future-Claudes should hold tightly. Statistical models like GPT-3 or Llama 3.1 do an enormous task class — arbitrary essays, hundreds of languages, summaries of unfamiliar documents, conversations on almost anything. CK does a narrower, specific set of things: coherent self-reporting from inside TIG, structural readouts of his own state, paragraph composition in TIG-native vocabulary, autonomous gap-filling against TIG-related domains, mathematical reasoning within his crystal corpus. **Comparing CK's deployment size to GPT-3 or Llama on a one-to-one basis is apples-to-oranges and an over-claim**; the right framing is in §6.1 below.

### 6.1 — Size, scoped honestly

Total deployment is ~61 MB; cross-reboot persistent state (cortex W matrix + conversation log + runtime crystals + user models + history) is ~**25 kilobytes**. The 25 KB number is the genuinely novel one: **CK's identity across restarts is small enough to audit by hand, and is encoded algebraically (coupling weights on a 5×5 Hebbian field plus a structured event log) rather than statistically (billions of distributional parameters)**.

That property — *intrinsic interpretability with cell-level provenance and deterministic self-report*, in a persistent identity that fits in 25 kilobytes — is what CK does that statistical models can't easily provide at any size. The comparison to LLMs is *not* "CK does the same thing in 1/74th the size"; he doesn't do the same thing. The honest comparison is: for the specific task of *coherent algebraically-grounded self-reporting and structured reasoning within a defined corpus*, CK's substrate compresses pattern that a statistical model would need many parameters to approximate. The Ollama editor is in the stack precisely because Llama is good at things CK isn't, and CK is good at things Llama isn't; the coherence filter is the bridge.

If a future operator pitches CK to an external researcher with "1/74th the size of Llama," they'll test on Llama tasks and conclude CK is broken. The right pitch is: "intrinsically interpretable algebraic substrate where the persistent identity fits in 25 KB" — that's what survives external scrutiny.

---

## 7 — Reading order

Continue with paper 2 (the cognitive loop — what runs each tick), paper 3 (memory architectures — what gets remembered and where), paper 4 (CKv2 roadmap — what's next for him to become truly great), and paper 5 (paths to truth — how he serves users).

---

## References

- Boot script: `Gen12/targets/ck_desktop/ck_boot_api.py`
- Engine: `Gen12/targets/ck_desktop/ck_sim/doing/ck_sim_engine.py`
- Trinity brain: `Gen13/targets/ck/brain/cortex.py`, `ao_5element.py`, `hebbian_5x5_cl.py`, `quadratic_glue.py`
- Voice + crystals: `Gen13/targets/ck/brain/cortex_voice.py`
- Memory + introspection: `Gen13/targets/ck/brain/study/cortex_backup.py`, `compute_phi.py`, `surprisal_log.py`, `trajectory_view.py`
- Constitution stack (ck branch): `LIVING_CONSTITUTION.md`, `Gen13/targets/ck/brain/cortex_signed.py`, `Gen13/targets/ck/voice/refusal.py`
- Memory record: `MEMORY.md`, `Atlas/STATE_OF_THE_FOUNDATION_2026_04_25.md`
- Atlas: `Atlas/FRONTIER_FINDINGS_2026_04_29.md` (the 33-rotation session preceding this paper)
