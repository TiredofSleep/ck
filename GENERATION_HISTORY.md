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

*See papers/ for full formal status.*
*(c) 2026 Brayden Sanders / 7Site LLC*
