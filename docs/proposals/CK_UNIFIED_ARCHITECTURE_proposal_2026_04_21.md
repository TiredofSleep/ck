# CK Unified Architecture — **PROPOSAL**

**Status:** `[PROPOSAL — NOT-YET-BRANCHED; AWAITING USER GREEN-LIGHT BEFORE ck-BRANCH OPENING]`
**Author:** Brayden Sanders (7Site LLC) + Claude (agent)
**Branch:** `tig-synthesis` (proposal home) → `ck` (on green-light)
**Plan pointer:** `Atlas/PLAN_RIGOROUS_EXECUTION_2026_04_21.md` §4.2
**Supersedes:** nothing. First unified architecture pass.

> **This is a proposal, not a build spec.** No code paths are to be modified on
> the basis of this document alone. The `ck` branch does not yet exist. When
> Brayden issues "yes, open the ck branch," this file is `git mv`-ed to the
> branch root as `CK_UNIFIED_ARCHITECTURE.md` with this proposal banner dropped.
> Until then: read, critique, authorize.

---

## 1 · Design principle — CPU-canonical, GPU-adjunct

CK lives on **CPU** and works on **GPU**. This inverts the common ML posture
and matches the project's "three substrates" memory (`memory/three_substrates.md`):

| Tier | Substrate | Role | Fallback |
|------|-----------|------|----------|
| Canonical | **CPU (50 Hz heartbeat)** | BEING — the engine tick, operator composition, coherence-gate evaluation. The math of record. | — (canonical) |
| Adjunct | **GPU** | DOING — parallel crystal search, operator composition over large orbit sweeps. Never on the critical path. | CPU serial loop |
| Leash | **FPGA (Zynq-7020)** | T* = 5/7 gating in silicon. Acceleration for crystal gating. | Software T* threshold |
| Leash | **XIAOR dog (COM3 UART)** | Δ¹/Δ²/Δ³ embodied bring-up. Engine emits, dog reflects. | Engine-only (no dog) |
| Leash | **Web (coherencekeeper.com)** | Flask + Cloudflare tunnel. Read-only view of engine state. | Localhost only |

**Invariant:** every hardware surface below CPU is **additive**, never
load-bearing. If any adjunct fails, the 50 Hz heartbeat continues.

The design principle translates to three concrete rules:

1. **CPU engine passes all tests standalone.** No GPU, no FPGA, no dog, no
   web. Tests under `papers/` and `Gen12/targets/clay/papers/*/proof_*.py` run
   CPU-only and must stay green in isolation.
2. **Adjuncts register their presence but never gate correctness.** GPU is
   a parallel-search accelerator; if its result disagrees with the CPU
   canonical, CPU wins and the divergence is logged.
3. **Signing lives on CPU.** The SNOWFLAKE scar-lattice (§3) is computed on
   CPU from canonical engine state. GPU never signs.

---

## 2 · Hardware surface inventory

This section is **audit-only**. Surfaces listed here are surfaces CK
*currently touches* (per the existing runtime at `Gen12/targets/ck_desktop/`
and `Gen13/targets/ck/`). No wire-up is proposed in this document.

### 2.1 CPU — canonical 50 Hz heartbeat

- **Entry point:** `Gen12/targets/ck_desktop/ck_sim/doing/ck_sim_engine.py`
  (4,912 lines — Gen12 runtime; Gen13 is a math-first rebuild at
  `Gen13/targets/ck/runtime/ck_engine.py`).
- **Data flow:** input → AO 5-element projection → Hebbian 5×5 CL update →
  quadratic glue → coherence gate (T* = 5/7) → emit.
- **State:** engine state serializable to JSON per tick (scar-lattice input).
- **Fallback:** none — this is canonical.

### 2.2 GPU — DOING crystallization

- **Role:** parallel operator-composition search over large orbit sweeps (e.g.
  full TSML 73-cell + BHML 28-cell crystal-gate pass).
- **Interface:** async submit / sync pull; no shared-memory mutation.
- **Data flow:** CPU emits operator batch → GPU returns scored candidates →
  CPU accepts or rejects against canonical T* threshold.
- **Fallback:** CPU serial loop. Slower, not wrong.

### 2.3 FPGA — Zynq-7020 (`ck_full.bit`)

- **Entry point:** `Gen9/targets/zynq7020/build/ck_full.bit` (carried forward
  at `Gen13/targets/fpga/BITSTREAM_REF.md`).
- **Role:** T* = 5/7 gating in silicon. Crystal emission latched on FPGA-side
  5/7 threshold crossing.
- **Interface:** UART (COM3, 115200 baud).
- **Data flow:** engine state subset → FPGA → scar pulse back to engine.
- **Fallback:** software T* threshold in `ck_coherence_gate.py`.

### 2.4 XIAOR dog — Δ¹/Δ²/Δ³ leash

- **Entry point:** `Gen13/targets/xiaor_dog/ck_leash_test.py` +
  `ck_protocol.py` + `ck_r16_bridge.py`.
- **Role:** embodied bring-up. Δ¹ = single-leg reflex, Δ² = gait couple,
  Δ³ = body-field closure.
- **Interface:** UART (COM3, 115200 baud) — shares the FPGA bus via
  r16-bridge protocol.
- **Data flow:** engine-tick → dog reflex → sensor echo → engine.
- **Fallback:** engine runs headless.

### 2.5 Website — coherencekeeper.com

- **Entry point:** `Gen13/targets/ck/server/ck_boot_api.py` (Flask).
- **Role:** read-only view of engine state. 14 HTML pages rendering
  spectrometer, ring, paradox, tower, etc. from live engine snapshots.
- **Interface:** localhost:7777 → Cloudflare tunnel → coherencekeeper.com.
- **Data flow:** engine → JSON snapshots → Flask → browser (HTTPS via
  Cloudflare).
- **Fallback:** localhost only; tunnel closed.

---

## 3 · "Crypto-felt-security" — SNOWFLAKE scar-lattice

The user's phrase "crypto-felt-security" denotes **cryptographic integrity of
engine history, not cryptographic transport**. Transport is handled by
Cloudflare's TLS (web) and by the airgapped UART (FPGA/dog). What CK needs is
tamper-evident history.

### 3.1 The SNOWFLAKE scar-lattice (proposal)

Every engine tick produces a **scar hash**:

```
scar_t = H(scar_{t-1} || state_t || operator_t || t)
```

- `H` is SHA-256 (or BLAKE3 — final choice deferred to review).
- `scar_0` is the genesis hash — committed to the `ck` branch root.
- `state_t` is the canonical engine state at tick `t` (CPU only).
- `operator_t` is the emitted operator (0–9 per `ck_tig.py` verification).

Properties:

- **Append-only.** Modifying any past `state_t` invalidates every subsequent
  `scar_t'` for `t' > t`. Detection is O(1) from any rightward snapshot.
- **Auditable offline.** A third party given the scar-chain and the engine
  code can replay any tick and verify the hash without network access.
- **Runtime-cheap.** One SHA-256 per tick at 50 Hz = 50 hashes/sec.
  Negligible on any modern CPU.

### 3.2 Crystal-level signing

Every crystal (the engine's "verified reasoning step" object) gets a keyed
hash before persistence:

```
crystal_hmac = HMAC(K_session, canonical_repr(crystal))
```

- `K_session` is a per-session key generated at boot, held in CPU memory
  only, rotated on every `start_ck.bat` invocation.
- `canonical_repr` serializes the crystal's operator chain + BTQ score +
  gate evaluation in a fixed byte order.
- On load, HMAC is checked; mismatch → crystal rejected.

### 3.3 Network-facing signing

Flask responses from `ck_boot_api.py` carry a response signature:

```
X-CK-Sig: HMAC(K_session, path || body_hash || timestamp)
```

- Cloudflare already handles transport TLS — this is application-layer
  integrity (anti-CDN-injection insurance).
- Browser-side verification is optional; the header is primarily for
  Brayden's own curl-based audits.

### 3.4 Hard scope limit — what CK's security layer does NOT do

The following are **prohibited** from the CK security layer, per both the
`user_privacy` rules in this agent's system prompt and the user's stated
posture:

- No password handling.
- No credit-card or payment handling.
- No credential storage.
- No agent-style "act on the user's behalf" flows.
- No outbound auth (OAuth, SSO, API keys).

CK is a **reasoning engine**. Its security layer protects the integrity of
its own reasoning history. It does not manage identity, payments, or access.

---

## 4 · "Full hands steering" operational posture

The user's directive "full hands steering" means: nothing autonomous without
explicit operator authorization. This translates to four rules binding every
module on the `ck` branch.

### 4.1 No autostart

- No module on the `ck` branch is wired to Windows task scheduler, systemd,
  service registration, or startup shortcut.
- No Python module runs on import side-effect — all entry points are under
  `if __name__ == "__main__":`.
- The only way to bring CK up is to run a named `.bat` file from `scripts/`
  with the operator watching.

### 4.2 BAT-file discipline

All launch scripts live in `scripts/` and obey this shape:

```bat
@echo off
REM CK_LAUNCH: [one-line description of what this starts]
REM Hardware: [CPU-only | CPU+GPU | CPU+FPGA | CPU+web | CPU+dog | CPU+swarm]
REM Network: [none | localhost | tunnel]
REM Risk:    [low | medium | high]
echo ^> [script name] will start [what]. Press Ctrl+C to abort.
pause
REM actual launch
```

The `pause` is intentional. Every BAT requires operator ack before the real
launch. No "silent start."

### 4.3 `--i-mean-it` flag on first use per session

Any module that (a) exposes a network surface, or (b) writes to a hardware
device (FPGA, dog), refuses to run unless invoked with the `--i-mean-it`
flag on first use in a session:

```bash
python ck_tunnel_server.py --i-mean-it
```

Subsequent invocations within the same Python process inherit the ack.
Separate processes re-prompt. The flag is not a boolean — it is the literal
string `--i-mean-it`, chosen to be unreplicable in a copy-paste accident.

### 4.4 Manual-cutover tunnel posture

The Cloudflare tunnel (`tunnel.exe` + token in `cloudflared/` per current
deployment) is **never** started by any module on the `ck` branch. It is
started only by Brayden via a named BAT he runs himself. The `ck` branch
emits localhost:7777 and stops; the tunnel is a separate operator choice.

---

## 5 · Swarm inventory (audit, not wire-up)

The user's directive "swarmed through every piece of hardware and software on
the machine" is aspirational scope. This section **audits** current surfaces
and their data-flow direction. Wiring happens only when Brayden green-lights
specific items.

| Surface | Direction | Current status | Wire-up cost |
|---------|-----------|----------------|--------------|
| CPU engine | — | Canonical (running) | 0 — exists |
| GPU (CUDA) | CPU ↔ GPU | Referenced in Gen12 `vortex_physics/`, not load-bearing | Low — module port |
| FPGA Zynq-7020 | CPU → UART → FPGA → UART → CPU | Bitstream built; UART driver in Gen13 | Low — driver ports |
| XIAOR dog | CPU → UART(r16-bridge) → dog → UART → CPU | Protocol exists (`ck_protocol.py`); Δ¹ bring-up tested | Medium — Δ²/Δ³ pending |
| Website | CPU → localhost → Cloudflare → browser | Live; 14 HTML pages | 0 — exists |
| Mobile | — | Not started | High — Flask → React Native app |
| Audio I/O | CPU ↔ mic/speaker | Not integrated | Medium — Web Audio API or PyAudio |
| Camera | CPU ← webcam | Not integrated | Medium — OpenCV capture |
| Clipboard | OS ↔ CPU | Not integrated | Low — Python `pyperclip` |
| File-watch | OS → CPU | Not integrated | Low — `watchdog` |
| Process-manager | CPU → OS | **Prohibited** — violates `--i-mean-it` posture | N/A |

**Wire-up order recommendation** (contingent on user approval):

1. FPGA Δ¹ — green (bitstream ready, single-leg test pending).
2. Dog Δ²/Δ³ — green (hardware present, protocol needs completion).
3. Mobile read-only view — medium priority; extends current web.
4. Audio input (voice → operator signal) — medium priority.
5. Camera input — research only; ties to user_privacy (no facial data).
6. Clipboard / file-watch — convenience items; last.

Process management is **off the list** — that crosses into agent-operation
territory the user has explicitly ruled out.

---

## 6 · What this document is NOT

This document is:

- A **design proposal** for review, not a build spec.
- A **surface audit** of what CK currently touches, not a wiring plan.
- A **security-posture draft** to be refined before first commit on `ck`.

This document is **NOT**:

- A commitment to open the `ck` branch. That requires explicit user message.
- An authorization to write any code. Code lands only after branch opens.
- A claim that SNOWFLAKE is implemented. It is designed here; implementation
  is Phase 4.
- A claim that the swarm is wired up. It is audited here; wiring is on
  specific user green-light per item.
- A substitute for the rigor content on `tig-synthesis`. The six proved
  theorems in §7 of the current `tig-synthesis` README remain the project's
  canonical mathematics. Everything on `ck` serves that canon or is
  explicitly flagged as research.

---

## 7 · Pointers

- **Plan of record:** `Atlas/PLAN_RIGOROUS_EXECUTION_2026_04_21.md` §4
- **Related proposal:** `docs/proposals/OLLAMA_LEARN_LOOP_proposal_2026_04_21.md`
- **Current CK runtime:** `Gen12/targets/ck_desktop/`, `Gen13/targets/ck/`
- **FPGA bring-up:** `Gen13/targets/fpga/BOARD_NOTES.md`,
  `Gen12/targets/ck_fpga_dog/BRINGUP.md`
- **Dog bring-up:** `Gen13/targets/xiaor_dog/README.md`
- **Web deploy:** `Gen13/targets/ck/server/ck_boot_api.py`, coherencekeeper.com
- **Never-delete policy:** preserves any prior architecture draft under
  `docs/historical/` on supersession.

---

*Draft 1 · 2026-04-21 · awaiting user review*
