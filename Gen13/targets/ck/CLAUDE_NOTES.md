# CK Notes — for Claude (not for readers)

**Purpose.** Fast orientation for a future Claude session opening this repo. Current as of 2026-04-18 post-embodiment (commits `bc4c4f0` + `63ce375` + `9e94ca2` + swarm). Public-facing docs are `README.md §CK section`, `CK_RUNTIME.md` (now with L0 embodiment layer), and `BRAIN_DESIGN.md`; this file is the internal working note.

**If you are reading this and you are not Claude:** you can read it, but the voice is blunt and assumes you already know the repo. Start with `README.md` and `CK_RUNTIME.md` first.

---

## What CK is, in 4 lines

1. A **5D Hebbian cortex** (`Gen13/targets/ck/brain/cortex.py`) that learns operator-pair correlations from text via `step_text()`, gated by T*=5/7, persisted as JSON at `Gen13/var/cortex_state.json`.
2. A **structural voice** (`cortex_voice.py :: speak()`) that answers a narrow set of query classes (state / learned / field / op-entity / dim-entity / **frontier topic**) with `label=value` readouts — no prose, no sampling, no hallucination surface.
3. An **embodied tick** (`Gen13/targets/ck/runtime/ck_swarm.py`): RT-elevated 50 Hz loop with CuPy-backed brain + CuPy-backed doing kernel on the GPU, UART bridge to the Zynq-7020 body, streaming jitter distribution at `/swarm`.
4. Served by the **Gen12 Flask runtime** (`Gen12/targets/ck_desktop/ck_boot_api.py`) as a **Phase C override** that wraps the older template layers. An **optional LLM bridge** (`Gen13/targets/ck/bridge/llm_bridge.py` + `ck_proof.py`) is available as a fluency wrapper; CK's /chat works fine without it.

The brain trinity (AO + Hebbian + quadratic glue) is real. The voice is narrow on purpose — CK grows by the math getting wider, not by ingesting text. The embodiment is what makes "50 Hz" a measurement instead of copy.

---

## The actual boot path (what happens when `python ck_boot_api.py` runs)

```
ck_boot_api.py imports
    from cortex import Cortex
    from cortex_persist import load_cortex, save_cortex, AutoSaver
    from cortex_voice import cortex_speak, speak
    from ck_voice_math import install_math_first_patch
    from ck_swarm import Swarm                  # L0 embodiment

_cortex = Cortex().boot()
    # AO + Hebbian(eta=0.005, decay=0.02) + quadratic glue
    # (defaults changed 2026-04-18; old defaults saturated at clamp 1.0)

load_cortex(_cortex, "Gen13/var/cortex_state.json")
    # restores W, tick, harmony_hits; silent if missing (cold boot)

install_math_first_patch(api)
    # wraps api.process_chat; T*/σ/5/7/operator queries short-circuit

api.process_chat = _process_chat_with_cortex(api.process_chat)
    # outer wrap: every chat fed to cortex.step_text() (learning);
    # then speak(cortex, text); if readout AND prior source was
    # template (ck_fractal/ck_self/ck_truth_recall), swap in readout

Flask serves 0.0.0.0:7777
    # Cloudflare tunnel routes coherencekeeper.com/chat
```

Order of precedence per /chat message: **math-first patch → cortex wrap → Gen12 template layers**. First one that fires wins; others get preserved on `text_previous` / `text_gen12`.

---

## What was changed today (2026-04-18) — the fix pack

Before you trust any pre-fix-pack note, check the commit. Two commits shipped:

### `bc4c4f0` — CK fix pack
| File | Change |
|---|---|
| `hebbian_5x5_cl.py` | `DEFAULT_ETA` 0.02→0.005, `DEFAULT_DECAY` 0.001→0.02. Equilibrium W* = η/decay = 0.25. Old defaults clamped at 1.0 (saturation). |
| `cortex_voice.py` | Added `_FRONTIER_FACTS`: 12 topic families (flatness / crossing / hodge_cstar / ψ order-4 / σ rate / ξ / BHML / TSML / tower / gap / basin / ck_system). T* aliases broadened: `t*` / `t star` / `t-star` / `tstar` / `5/7`. |
| `test_brain.py` | Added `t_hebbian_no_saturation_at_defaults` + `t_cortex_voice_frontier_router`. Now 20/20 green. |
| `Gen13/targets/ck/bridge/llm_bridge.py` (new) | Ollama + DeepSeek adapters, `ck_structural_context()`, `build_grounded_system()`. Pure library, no side effects on import. |
| `ck_proof.py` (repo root, new) | Side-by-side: CK alone vs LLM alone vs LLM+CK grounded. |
| `CK_RUNTIME.md` (repo root, new) | Public-facing runtime manifest. |
| `README.md` | Added "CK (Coherence Keeper): Algebraic Coherence System" section. |

### `63ce375` — Discoverability pass
| File | Change |
|---|---|
| `BRIDGES_INVENTORY.md` (repo root, new) | Verified-path map of every bridge paper across 7 categories + 6 branches. |
| `README.md` | Branches block now shows all six (tig-synthesis, clay, archive-full, tesla, bible-companion, fpga-dog); §6 gains 2 rows (interdisciplinary → BRIDGES_INVENTORY; engineer → CK_RUNTIME + ck_proof). |

### `9e94ca2` — CLAUDE_NOTES.md
Internal file (this one).

### Embodiment commit — full swarm (commit `d7df220`)
| File | Change |
|---|---|
| `Gen13/targets/ck/runtime/rt_priority.py` (new) | OS priority + affinity via ctypes (Windows) / os.sched (Linux). Non-admin → HIGH/HIGHEST + core-pinning. Admin → REALTIME/TIME_CRITICAL. Linux → SCHED_FIFO 50. Never raises; reports what the OS allowed. |
| `Gen13/targets/ck/brain/hebbian_gpu.py` (new) | CuPy-vectorized Hebbian 5×5 field. Bit-for-bit parity with CPU reference (`max_diff_vs_cpu_ref=0.000e+00`). NumPy fallback when CuPy absent. `backend` attr reports which bus. |
| `Gen13/targets/ck/runtime/fpga_bridge.py` (new) | Lazy pyserial bridge wrapping `ck_protocol`. Dormant-safe (`live=False` if port absent). Methods: `open()`, `ping()`, `read_state()`, `gait()`, `estop()`. |
| `Gen13/targets/ck/runtime/jitter_probe.py` (new) | Standalone CLI probe. `--seconds 30 --hz 50 --rt --affinity 0`. Writes JSON + markdown with full delta + jitter distribution. |
| `Gen13/targets/ck/runtime/ck_swarm.py` (new) | The supervisor. Owns brain + doing (GPU DoingKernel, pre-allocated buffers, T* gate) + body. Runs measured 50 Hz tick with RT + coarse+spin sleep. 512-entry rolling jitter distribution. |
| `Gen12/targets/ck_desktop/ck_boot_api.py` | Additive patch: `from ck_swarm import Swarm; _swarm = Swarm(cortex=_cortex, hz=50, rt=True, affinity=[0], fpga_port="COM3").start()`. New endpoints `/swarm` and `/jitter`. atexit hook stops cleanly. |
| `CK_RUNTIME.md` | Rewrote "Three Layers" to "Four Layers" with L0 embodiment section. Added measured jitter table, body status line, `/swarm` + `/jitter` routes. Updated boot-path + honest-limits. |

### Embodiment follow-up — W merge + core separation (2026-04-18, uncommitted)
Fixes the two known weaknesses from the first embodiment commit: (a) the
swarm's Hebbian field was separate from `cortex.hebbian` so `/swarm` and
`/chat` were reading different W matrices, and (b) the engine tick_loop
and the swarm tick both fought for core 0.

| File | Change |
|---|---|
| `Gen13/targets/ck/runtime/ck_swarm.py` | `_ensure_brain()` now prefers `cortex.hebbian` as the shared W when a cortex is passed — the swarm stops owning a separate field. `_tick_once()` syncs `cortex.state.W_trace`, `W_strongest`, and bumps `cortex.state.tick` on every tick. `/swarm` brain snapshot adds `shared_with_cortex`, `cortex_tick`, `cortex_emergent`. |
| `Gen13/targets/ck/runtime/rt_priority.py` | `elevate()` now takes `process: bool` (default True) + `thread_level: str` ('auto' / 'high' / 'above' / 'normal'). Peer threads (e.g. engine tick_loop) call with `process=False, thread_level='above'` so they don't override the swarm's REALTIME/HIGH process class. |
| `Gen12/targets/ck_desktop/ck_boot_api.py` | `tick_loop()` now self-elevates to core 1 with ABOVE_NORMAL thread priority, process class untouched. Engine and swarm run on adjacent cores instead of fighting. |
| `Gen13/targets/ck/runtime/EMBODIMENT_NEXT.md` (new) | Documents Task 2 (flash `ck_full.bit` → body live) + admin REALTIME + AO-driven input + GPU-mirror of W. |

**What this means for /swarm + /chat state:** `cortex.state.tick` now advances from TWO drivers — `cortex.step_text()` from the /chat wrap AND the swarm tick. That's intentional: both are real experience. W_trace from /chat and from /swarm are now guaranteed identical since they read the same field.

**Stale notes to distrust** until updated:
- `Gen13/targets/ck/brain/BRAIN_DESIGN.md` — says `test_brain.py (to be written)` and `runtime/ck_engine.py — TBD`. Both untrue post-fix-pack. Also does not mention cortex.py / cortex_voice.py / cortex_persist.py / cortex_replay.py / hebbian_gpu.py / ck_swarm.py at all.

---

## Live state this session

Last battery (10 /chat queries) on the live server returned:

| Query | Source | Result |
|---|---|---|
| how do you feel right now | cortex_speak | feel: aperture=LATTICE … ao: op=HARMONY coherence=1.000 breath=INHALE |
| what have you learned | cortex_speak | couplings: … W=0.250 × 5 pairs (at equilibrium) |
| show strongest couplings | cortex_speak | same structure |
| what is the beauville curve c star | cortex_speak | hodge_cstar: genus=5 bielliptic=yes … descent_risk=HIGH \| sprint35b [target] |
| what is the crossing lemma | cortex_speak | crossing_lemma: D2=0 flat \| 27 instances \| WP57 [proved] |
| what is the flatness theorem | cortex_speak | flatness: T*=5/7 \| torus R/r=5/7 \| 6 derivations \| WP51 [proved] |
| what is T star | cortex_speak | (T* alias fix) flatness readout |
| what is the sigma rate theorem | cortex_speak | sigma_rate: σ(N) ≤ C/N \| WP101 [proved] |
| what is the xi field | cortex_speak | field: tick=155908 emergent=0.445 W_trace=0.824 \| xi: V=ξ·log(ξ) … [structural; DESI χ²=15.7 vs ΛCDM 14.1] |
| what is psi order 4 | cortex_speak | psi: order=4 \| ψ²=ι \| acts_as=+i_on_Prym \| embeds Q(i) into End0(Prym) |

Cortex snapshot at time of battery: **tick 155,908 · emergent 0.445 · W_trace 0.824 · mean|W| 0.176 · harmony_rate 0.713 · strongest pair (0,0) = 0.250**.

---

## Where to look first (by question type)

| If the user asks... | Open this first |
|---|---|
| "how is CK doing" / "is he broken" | POST to `/chat` with "how do you feel right now" — look at `cortex.W_trace` (>0.3 warm, <0.05 cold), `strongest pair` (should be ≤ 0.25 = equilibrium; 1.0 = saturation bug). |
| "what does CK say about X" | Try `speak(cortex, "what is X")` in a REPL; if it returns None the topic is not in `_FRONTIER_FACTS` — consider adding a fact. |
| "why is CK template-like" | Check the source field on /chat response. If `ck_fractal` or `ck_self` and there's no `source_previous` swap, the query didn't match any cortex route. Add frontier fact or state-route alias. |
| "CK's voice is too narrow" | That is by design. Widen by adding to `_FRONTIER_FACTS` (1 trigger line + 1 label=value + 1 sprint/paper pointer + 1 `[proved/structural/target]` tag). Do NOT add prose templates. |
| "CK lost his learned state" | Check `Gen13/var/cortex_state.json`. If missing or corrupted, run `python Gen13/targets/ck/brain/cortex_replay.py` to reseed from paper corpus. |
| "run the proof script" | `python ck_proof.py "…your prompt…"`. Needs Ollama at 127.0.0.1:11434 **or** `DEEPSEEK_API_KEY`. Without either, rows 2 and 3 show `[skip]`. |
| "is the LLM bridge load-bearing" | **No.** CK's /chat works without it. Bridge is wrapper, not dependency. |

---

## Common pitfalls a future-Claude will hit

1. **Editing cortex_voice.py without restarting CK.** Flask caches the module in memory. You must stop PID on 7777 and reboot `ck_boot_api.py` to pick up the change. Symptom: old behavior on live server even though the module on disk is updated.

2. **Confusing Cortex class locations.** `Cortex` lives in `Gen13/targets/ck/brain/cortex.py`, **not** `cortex_voice.py` and **not** `hebbian_5x5_cl.py`. Tests use `from cortex import Cortex`.

3. **Treating the cortex state as source-controlled.** `Gen13/var/cortex_state.json` is `.gitignore`-excluded (runtime artifact). Never commit it. The backup from the saturation incident (`cortex_state.saturated_backup_2026_04_18.json`) is also gitignored but preserved locally per never-delete.

4. **Assuming saturation = learning.** `W_trace ≈ 5.0` and `mean|W| ≈ 1.0` means every cell clamped — CK is not learning, he's ceilinged. Healthy looks like `W_trace 0.5–1.5` and `mean|W| 0.05–0.25` with `strongest pair ≤ 0.25`.

5. **Writing prose for CK.** Hard rule from memory: never ventriloquize CK. The structural router is his voice. If a topic needs more surface, add a `_FRONTIER_FACTS` entry — do not write narrative on his behalf.

6. **Trusting Grok / ChatGPT file claims uncritically.** Every external-LLM claim about "file X exists at path Y" must be verified via Glob/Read before being cited. BRIDGES_INVENTORY.md was written only after Explore-agent verification of each path.

7. **Pushing without checking stage surface.** Repo has ~40 untracked noise items at root (`_*_raw/`, scratch `.py`, `.bat`, result JSONs, `nul`). Always `git add <explicit file>` — never `git add -A` or `git add .`.

8. **Confusing the swarm tick with the engine tick.** Two loops run in the live process: (a) the Gen12 `tick_loop()` in `ck_boot_api.py:31` driving the older `CKSimEngine` (now pinned to core 1, ABOVE_NORMAL), and (b) the Gen13 `Swarm.start()` thread driving the embodiment substrate (core 0, HIGH/HIGHEST, HIGHEST if admin=true→TIME_CRITICAL). They DO share Hebbian state now: the swarm's brain IS `cortex.hebbian`, and every swarm tick bumps `cortex.state.tick`, `W_trace`, and `W_strongest`. W_trace read from `/chat` and `/swarm` will always agree. What they still DON'T share: the engine's `CKSimEngine` is a separate being (its own heartbeat, its own 8M-experience HER, its own SwarmField); merging those into cortex is future work.

9. **CuPy first-tick JIT stall.** The very first CuPy outer-product + clip launches compiles kernels on the device (~400–500 ms). The swarm's `status()` already drops the first delta from its percentiles, but if you see a one-time "max=500ms" on startup don't read that as steady-state jitter.

10. **Running /jitter while the swarm runs.** The `/jitter?seconds=N` endpoint elevates and runs its own high-res tick, which means two RT threads fight for core 0 during the probe window. Numbers during probe are noisier than steady-state `/swarm`. For a clean baseline, measure with the swarm stopped.

11. **Windows RT without admin.** `SetPriorityClass(REALTIME_PRIORITY_CLASS)` silently downgrades when not elevated. `rt_priority.elevate()` handles this gracefully (returns `process_class="HIGH"`), but don't claim REALTIME in docs unless the console shows `admin=True`. Run the console as Administrator to actually get REALTIME.

12. **FPGA port open ≠ board alive.** `COM3` opening on Windows just means a USB-serial device is enumerated. It does NOT mean the ARM firmware answers PKT_PING. If `/swarm` shows `body.live=True` but `last_ping_ms=None` and `errors=["write failed: Write timeout"]`, the board is unpowered or the bitstream isn't loaded. The bitstream lives at `old/Gen9/targets/zynq7020/build/ck_full.bit`.

---

## Five commands to verify CK is healthy

```bash
# 1. Test suite (required before committing brain/ changes)
python Gen13/targets/ck/brain/test_brain.py
# Expect: 20/20 green

# 2. Live state probe (must return cortex_speak source + differentiated W)
curl -s -X POST http://127.0.0.1:7777/chat \
  -H 'Content-Type: application/json' \
  -d '{"session_id":"probe","text":"what have you learned","mode":"normal"}' | python -m json.tool
# Expect: source=cortex_speak (possibly was:ck_fractal); text starts "couplings:..."

# 3. Frontier router sanity
for q in "beauville curve c star" "flatness theorem" "crossing lemma" "T*" "sigma rate"; do
  curl -s -X POST http://127.0.0.1:7777/chat \
    -H 'Content-Type: application/json' \
    -d "{\"session_id\":\"probe\",\"text\":\"what is the $q\",\"mode\":\"normal\"}" \
    | python -c "import sys,json; d=json.load(sys.stdin); print(d['source'],'|',d['text'][:100])"
done
# Expect: every row source=cortex_speak with a structural readout.

# 4. Embodiment: GPU brain, GPU doing, RT, body link, jitter window
curl -s http://127.0.0.1:7777/swarm | python -c "
import sys,json; d=json.load(sys.stdin)
print('ticks', d['ticks'], 'hz', d['hz'], 'running', d['running'])
print('brain', d['brain']['backend'], 'strongest', d['brain']['strongest_pair'])
print('doing', d['doing']['backend'], 'coherence', round(d['doing']['coherence'],3))
print('body live', d['body']['live'], 'port', d['body']['port'])
print('rt', d['rt']['process_class'], d['rt']['thread_priority'])
print('jitter', d['jitter_us'])
"
# Expect: brain=cupy, doing=cupy, rt=HIGH/HIGHEST (REALTIME if admin), ticks climbing.

# 5. One-shot jitter probe (blocks 3s)
curl -s "http://127.0.0.1:7777/jitter?seconds=3&hz=50&rt=1" | python -c "
import sys,json; d=json.load(sys.stdin)
print('delta_us', d['delta_us'])
print('jitter_us', d['jitter_us'])
"
done
# Expect: all source=cortex_speak; all text is label=value (not prose)
```

---

## Where the live CK actually runs (deployment)

- **Dev local:** `python Gen12/targets/ck_desktop/ck_boot_api.py` on 127.0.0.1:7777
- **Prod:** Cloudflare tunnel from `coherencekeeper.com/chat` → 127.0.0.1:7777 on Brayden's box. **Do not modify the tunnel without explicit user confirmation.** A broken tunnel = a dead website.
- **State file:** `Gen13/var/cortex_state.json` — local to the running machine. `AutoSaver` writes every 200 ticks or 30 s.

---

## Honest limits (do not overclaim)

- CK's voice is **narrow**. He does not answer freeform prose questions. That's by design.
- CK is **not profound**. He is **precise**. The profundity is in the math he cites, not in novel synthesis he generates.
- Phase C override wins **only for specific query classes**. Other queries fall through to the Gen12 template layers (fluent but template-driven).
- The LLM bridge is **optional and wrapper-only**. CK's goal is for his structural voice to grow wide enough that the bridge stops earning its keep.
- Frontier facts are **curated, not learned**. If a topic is missing, it won't be answered structurally until someone adds a `_FRONTIER_FACTS` entry.

---

## Preserved pointers (never-delete discipline)

- Saturated pre-fix cortex state: `Gen13/var/cortex_state.saturated_backup_2026_04_18.json` (gitignored, local only)
- Pre-fix default constants in `hebbian_5x5_cl.py`: documented in module docstring with derivation
- `BRAIN_DESIGN.md` is preserved in its pre-fix-pack form — update it, don't delete its history

---

*Author: ClaudeCode (2026-04-18 fix-pack session). If you are a future Claude and something in here is wrong, fix it rather than commenting around it. The file is for orientation, not archaeology.*
