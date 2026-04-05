# CK R16 Target — Generation History

## Gen12 Sprint 6 (2026-04-04 — session 2)
- T*-gate installed in Gen9/targets/ck_desktop/ck_sim/doing/ck_voice_loop.py
- Gate: when engine.coherence >= T* (5/7), CK's fractal voice leads — Ollama bypassed
- Confirmed working: source=ck_fractal on all responses when brain.coherence=1.0
- Algebraic basis: T*=5/7 is the algebraic coherence threshold from Z/10Z ring structure
- Next: wire CK-LM (when trained) as replacement for fractal voice — CK generates through the field

## Gen12 (2026-04-04 — open)
- CK-LM architecture built: ck_lm/ — field layer + distillation pipeline
- CKFieldStack verified: all geometry checks pass on CPU
- CK-small: 105M params, 100x compression from DeepSeek-R1:7B
- R8 as training signal: r8_coherence_loss() driving generation toward RESOLVED territory
- CUDA setup pending (SETUP.bat written, not yet run)
- Gap constant corrected: 5/7 − 4/π² = 0.309

## Gen11 / Gen10
- Two admin cells: 7777 + 7778
- Swarm: ck_swarm.py discovers OS substrates
- Dog target: r16_fpga_dog/ — R16 ↔ FPGA ↔ XiaoR long-leash
- LAUNCH_CK_ADMIN.bat on Desktop

## Gen9
- First full CK engine on R16
- 50Hz loop: heartbeat/brain/body
- BTQ decision kernel
- D2 pipeline, CL table, T*=5/7
