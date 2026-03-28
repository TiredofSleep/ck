# CK Generation History — Gen 10

## Gen 10.00 — 2026-03-27 — Separation from Gen 9

**What this generation is:**
Gen 10 is the first generation where all parts close into one organism.
Gen 9 built every layer. Gen 10 wires them together and proves the math beneath.

**Core changes from Gen 9:**

1. **Voice fallback closed** — `_fallback_ck_voice()` cascades through CK's own physics:
   Level C: Fractal voice (15D triadic, compose_tribal)
   Level D: Sentence composer (CKTalkLoop, SVO from CL graph)
   Level E: CAEL grammar (BecomingTransitionMatrix)
   Level F: Babble (raw operator→word lattice)
   No more canned strings. CK always speaks his own physics.

2. **Coherence loop fully closed** — CK hears his own voice, absorbs it via olfactory,
   and that absorption shapes what he says next tick. The loop is real, not stubbed.

3. **Constant taxonomy locked** — d_COL (1/18, geometry), W_BHML (3/50, statistics),
   inner_shell (2/9, shell boundary), MASS_GAP (2/7, dynamics) are now distinct constants
   with separate physical meanings. The conflation from Gen 9 docs is corrected.

4. **Product-gap proved for all k≥1** — Previously verified by script for k=1..4.
   Now proved by induction on the 4×4 corner sub-table. Valid for arbitrary tensor depth.

5. **TIG formal ledger** — WP24 audit classifies all claims into PROVED / STRUCTURAL /
   EMPIRICAL / OPEN. No overclaiming. Yang-Mills quantitative 2/7 explicitly falsified.

**Inherited from Gen 9 (unchanged):**
- 50Hz main loop: heartbeat/brain/body
- BTQ decision kernel (T generates, B filters, Q scores)
- D2 pipeline: 5D force vectors from Hebrew roots
- CL table: TSML 73-harmony composition
- TIG 3-phase pipeline: Being → Gate1 → Doing → Gate2 → Becoming → Gate3
- Olfactory + gustatory + lattice chain + reverse voice
- Fractal voice v2 (15D triadic, 3-voice tribe)
- Experience-to-voice bridge (olfactory centroids → voice context)
- L-CODEC v1 (text → 5D force vectors)

**Papers baseline:** WP1–WP27 + 2 sprint packages (2026-03-27 morning + afternoon)

---

## Gen 10.02–10.07 — 2026-03-27 — GPU-First DOING Architecture

**Core principle implemented:**
DOING = GPU (CuPy/Taichi). BEING = CPU. Any computation CK runs per-tick
lives on the RTX 4070. Memory (olfactory library, crystals, experience) stays on CPU.

**Changes:**

1. **EarsEngine** (`ck_sim_ears.py`) — 8-frame rolling CuPy buffer, rfft per frame.
   Falls back to numpy when cufft DLL is unavailable.

2. **Taichi chain walker wired** (`ck_sim_engine.py`, `ck_taichi_chains.py`) —
   `build_taichi_bridge()` now instantiated and wired into engine at startup.
   Both lattice chain walk sites (heartbeat + text-eat) use GPU parallel walks.
   Olfactory `_enforce_cl_field()` uses `taichi_bridge.olfactory_interaction()`.

3. **WP29 λ-Voice Theorem** (`ck_sim_engine.py`) — `engine.voice_lambda` property:
   `λ_ck = (stage/5) × coherence`. Corridor threshold gates BRT/CHA/BAL/COL/CTR.

4. **WP30 Re_local criterion** (`ck_olfactory.py`, `ck_lattice_chain.py`) —
   `stall_count = len(active)` (enstrophy Ω). `mean_depth` rolling 100-walk average (L).
   `engine.olfactory_re_local = stall × depth² / coherence ≤ 2/7 (MASS_GAP)`.

5. **WP31 Corridor geometry** (`ck_voice_loop.py`) — `VoiceLoopResult.corridor` field.
   Every voice response labelled: Pre-leak / BRT / CHA / BAL / COL / CTR.

6. **GPU word search** (`ck_fractal_voice.py`) — `WordForceIndex._build_gpu_arrays()`:
   (N,15) CuPy float32 triadic matrix. `batch_distance()` replaces Python 15D loop.
   `find_by_force()` now uses GPU batch distance + CPU bonus post-processing.

7. **GPU TeslaWaveField** (`ck_vortex_physics.py`) — CuPy batch Ψ sum.
   Ψ = Σ A_c·exp(i·(k_c·|r−r_c| − ω_c·t + φ_c)) runs per 50Hz tick on GPU.
   Parameter cache (N,5)/(N,) arrays rebuilt when concept count changes.

8. **GPU visual encoder** (`ck_visual_encoder.py`) — `_xp = cupy` replaces numpy.
   sRGB→CIELab→TIG 27-bit shell packing all via CuPy array ops on GPU.

9. **OS stats loop closed** (`ck_power_sense.py`, `ck_sim_engine.py`) —
   `gpu.tick()` now runs before `power_sense.tick()`. Real NVML readings
   (gpu_power_w, gpu_util_pct, gpu_temp_c) injected into sensors dict.
   CK feels his own GPU activity as D2 physics via the power stream.

10. **GPU NS spectral solver** (`ck_clay_generators.py`) — NavierStokes time-stepping
    loop uses CuPy fft2/ifft2 when cufft DLL is available, scipy fallback otherwise.

**GPU status (RTX 4070, 12GB VRAM):**
- CuPy array ops: ACTIVE (distance, wave fields, word search, visual encoding)
- Taichi CUDA kernels: ACTIVE (chain walks, olfactory CL field, CA lattice tick)
- cuFFT: UNAVAILABLE (CUDA toolkit DLL missing — FFT falls back to numpy/scipy)
- CUDA lattice_tick + cell_tick kernels: ACTIVE (compiled from `ck_gpu.py`)

---

## Gen 10.09 — 2026-03-27 — Import Alias Fix + Voice Fallback Wiring

**Changes:**

1. **EarsEngine import alias fixed** (`ck_sim/__init__.py`) —
   `'ck_sim.ck_sim_ears'` was pointing to stale `ck_sim.face.ck_sim_ears`.
   Corrected to `ck_sim.being.ck_sim_ears`. Sensorium can now resolve
   `from ck_sim.ck_sim_ears import EarsEngine` correctly.

2. **Voice fallback cascade wired** (`ck_voice_loop.py`) —
   `_fallback_ck_voice()` rewritten to cascade through CK's own physics:
   Level C: Fractal voice (compose_from_operators, 15D triadic, compose_tribal)
   Level D: Sentence composer (CKTalkLoop, SVO from CL graph)
   Level E+F: CAEL grammar / babble (compose_from_operators at dev_stage=0)
   No more canned strings when Ollama is down. CK always speaks his own math.
   `user_text` passed through to composer.respond() for contextual replies.
   BECOMING phase extended: own-voice results crystallize + feed lattice learning.

---

## Gen 10.10 — 2026-03-27 — EarsEngine GPU Rewrite

**Changes:**

1. **EarsEngine full GPU rewrite** (`ck_sim_ears.py`, 467 lines) —
   All audio feature extraction runs on the GPU as a single vectorised batch
   pass over an 8-frame rolling buffer:
   - `_RollingBuffer((8, 441) CuPy array)`: circular write; `extract_features()`
     computes RMS / spectral centroid / spectral spread / ZCR across all 8
     rows simultaneously via `cupy.fft.rfft(buf, axis=1)` — no Python frame loop.
   - Temporal smoothing is free: all 8-frame results are averaged in the same pass.
   - `EarsEngine._audio_callback()`: flatten → push → silence gate (raw numpy RMS)
     → GPU batch extract → smoothness (RMS delta) → 5D force vector →
     `CurvatureEngine` → operator. No Python loops.
   - 5D mapping: aperture=spectral_spread, pressure=rms, depth=spectral_centroid,
     binding=1−zcr, continuity=smoothness.
   - cufft probe preserved: `_GPU=False` if cufft DLL absent; identical numpy fallback.

---

## Gen 10.11 — 2026-03-27 — Boot Hardening + GPU/Game Coexistence

**What broke, what we found, what we fixed:**

1. **Taichi load_experience() triple loop** (`ck_taichi_chains.py`) —
   `load_experience()` used a Python triple loop (N×10×10 = 1.05M assignments)
   to push experience tables to GPU. On 10528 nodes this hung for minutes.
   Fixed: `experience_tables.from_numpy(padded)` — one DMA bulk transfer.

2. **Double sync on boot** (`ck_taichi_chains.py`, `ck_sim_engine.py`) —
   `build_taichi_bridge()` already calls `sync(force=True)` internally.
   Engine was calling it again → second full load. Removed redundant engine sync.
   `detect_grokking()` was also calling `self.sync()` unconditionally →
   changed to `maybe_sync()` (only syncs when new nodes exist).

3. **Taichi→olfactory wiring order bug** (`ck_sim_engine.py`) —
   Wire code at line 774 checked `self.olfactory` before olfactory was
   initialized (olfactory init is at line 799). AttributeError on first tick.
   Fixed: moved wiring to immediately after olfactory init.

4. **`ck_sim.ck_tig` missing from Gen10** (`ck_sim/__init__.py`,
   `ck_sim/being/ck_tig.py`) — Engine tick() lazy-imports
   `compose, disagreement, is_frozen, heartbeat_phase, GENERATORS,
   CREATION_CYCLE, DISSOLUTION_CYCLE` from `ck_sim.ck_tig`. Module existed in
   Gen9 but wasn't carried to Gen10. Copied to `being/`, added alias.
   Without this fix: first tick() crashed, engine never ticked.

5. **Power sense thresholds** (`ck_power_sense.py`) —
   Calibrated for desktop RTX 4070 system:
   MAX_POWER_W 65→280W, THERMAL_LIMIT 75→85°C, YELLOW threshold 75°C/75% max.
   Previously b_check() always returned False (CK stuck at "quick" reasoning).

6. **Taichi GPU throttle + game coexistence** (`ck_sim_engine.py`) —
   Both Taichi `walk_parallel()` call sites now gate on power band AND tick rate:
   - GREEN + tick%50==0: GPU walk (~15Hz)
   - YELLOW or RED: CPU chain walk (no GPU contention)
   At 1138Hz tick rate, un-gated Taichi caused 700+ CUDA kernel launches/sec
   which hitched Rocket League frame pacing (165fps→140fps).
   Now CK backs off GPU naturally when he senses gaming load via NVML.

**Boot time after fixes:** 21–24 seconds (was: infinite hang)
**Tick rate:** 1138 Hz (DisagreementTick adaptive)
**Chat source:** ck_fractal (Ollama not needed — CK speaks own physics)
**GPU coexistence:** Taichi at ~15Hz, Rocket League at full frames

---

## Gen 10.12 — 2026-03-27 — Full OS Stats + Sensor Pipeline

**What broke, what we found, what we fixed:**

1. **HER + Chain Compressor endpoints wrong attribute names** (`ck_boot_api.py`) —
   `/her/status` checked `engine.olfactory_her` (wrong) → `engine.hindsight_replay`.
   `/compression/status` checked `engine.chain_compressor` (wrong) → `engine.chain_compression`.
   Both now return live data. HER shows 8.8M recorded, 1.1M replayed, 92.6% tempered.

2. **`power_sense.tick()` never called — BREATH-gated sensing** (`ck_sim_engine.py`) —
   `power_sense.tick()` lived inside `_tool_sense()` which only fires when
   `op == BREATH (8)` or on bump pairs. With CK often in VOID, sensors never updated.
   Fixed: added unconditional power+OS sense block every 66 ticks (~20Hz) in main `tick()`.
   Reads `platform_body._sensors` (OS thread data) + `gpu.state` directly — no kernel launch.

3. **`self.gpu.stats` called without `()`** (`ck_sim_engine.py`) —
   `_gs = self.gpu.stats` returned the bound method object (truthy but not a dict).
   `_gs.get(...)` raised AttributeError → outer try/except swallowed it silently.
   Fixed: `self.gpu.stats()` (method call).

4. **Full OS stats pipeline** (`ck_body_interface.py`, `ck_power_sense.py`) —
   `SimBody` now runs a 2Hz background psutil poller thread writing to `_sensors`:
   - cpu_pct (avg), cpu_per_core (32-element list), cpu_freq_mhz
   - ram_used_mb, ram_total_mb, ram_pct, swap_pct
   - disk_read_bps, disk_write_bps (delta rates)
   - net_sent_bps, net_recv_bps (delta rates)
   - proc_ram_mb, proc_threads, proc_cpu_pct (CK self-stats)
   `PowerState` extended with 13 new fields for all OS dimensions.
   `smooth_power` now blends GPU watts (60%) + CPU% (20%) + RAM% (10%) + I/O (10%)
   so ALL subsystem load shapes D2 physics, not just GPU watts.

5. **All 6 GPU fields forwarded to sensors** (`ck_sim_engine.py`) —
   Previously only 3 GPU fields (util, power, temp) injected into sensors.
   Now all 8: + mem_used_mb, clock_graphics_mhz, clock_memory_mhz, fan_pct, mem_util_pct.

6. **`/sensors` endpoint** (`ck_boot_api.py`) —
   New endpoint exposing full live sensor stream: power, cpu, ram, disk, net, gpu, process.
   All 24 sensor channels visible and verified flowing.

**Verified sensor readings (RTX 4070, R16 system at idle):**
- CPU: 17.4% avg, 32 cores, 2400MHz
- RAM: 20092MB / 32485MB (61.9%)
- GPU: 6% util, 42W, 50°C, 2475MHz clock, 2732MB VRAM
- Disk: 0.25MB/s read, 24.78MB/s write
- Net: 0.006MB/s recv, 0.076MB/s sent
- CK process: 1176MB RAM, 102 threads
- Composite power scalar: 59.69W → D2 physics

---

*See papers/ for full formal status.*
*(c) 2026 Brayden Sanders / 7Site LLC*
