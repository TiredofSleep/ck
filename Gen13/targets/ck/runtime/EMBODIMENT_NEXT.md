# Embodiment next — what's left after Tasks 1 + 3

**State as of commit `d7df220` + the shared-brain + core-1 follow-up:**
CK runs as a full swarm on the desktop. Brain + doing are live on the RTX
4070 via CuPy; the engine tick_loop and the Gen13 swarm tick now run on
different cores (engine core 1 ABOVE_NORMAL, swarm core 0 HIGH/HIGHEST);
the swarm's Hebbian field is merged into `cortex.hebbian` so `/chat` and
`/swarm` read from the same W. Body (FPGA) software path opens COM3 and
is dormant-safe.

---

## What's still open — do this next

### Task 2 (deferred — flash `ck_full.bit` and bring body live)

**File:** `old/Gen9/targets/zynq7020/build/ck_full.bit` (existing, carried
forward from Gen9).

**Board:** Zybo Z7-20 (Zynq-7020). Reachable at **COM3** / **115200**
per `Gen13/targets/xiaor_dog/HARDWARE_SETUP.md`.

**What "live" looks like on `/swarm`:**
```json
"body": {
  "live": true,
  "port": "COM3",
  "last_ping_ms": <small, say < 10>,
  "last_state": {...PKT_STATE fields...}
}
```
Currently we see `"live": false, "errors": ["write failed: Write timeout"]`
because the board is unpowered / unflashed.

**Bring-up sequence (one-time per power cycle):**
1. Power the Zybo board, confirm FTDI shows up as COM3 in Device Manager.
2. Flash bitstream via Vivado hw_server or xsct:
   ```
   xsct -eval "connect; fpga -file old/Gen9/targets/zynq7020/build/ck_full.bit; exit"
   ```
   (or load from SD card if the board is configured for that boot mode.)
3. `python Gen13/targets/ck/runtime/fpga_bridge.py --port COM3` — expect
   ping round-trip ≤ 10 ms and a PKT_STATE response.
4. Restart `ck_boot_api.py` — `/swarm` should now report body live.

**If ping times out after flashing:** check that the bitstream is
running the CK UART protocol (SYNC `CK` + TYPE + LEN + PAYLOAD + CRC8
maxim poly 0x31, per `Gen13/targets/xiaor_dog/ck_protocol.py`). If the
bitstream is a stock blink demo, it won't speak the protocol.

**What this unlocks:** the `body_to_brain` loop closes. The FPGA reports
its local coherence, gait phase, and heartbeat; the swarm feeds that
into the Hebbian field alongside the software inputs. CK's hands come
online.

---

## Why Tasks 1 + 3 landed first, not Task 2

- Tasks 1 + 3 are pure software — they run on the desktop, no hardware
  prerequisite. Jitter and state-merge are verifiable immediately.
- Task 2 depends on physical access to the Zybo (power + Vivado + USB),
  which isn't a refactor; it's a bring-up. Easier to do standalone once
  the board is on the bench.

## After Task 2 — further embodiment

- **admin REALTIME path:** rerun `ck_boot_api.py` from an elevated shell
  — Windows will grant `REALTIME_PRIORITY_CLASS` to the process and
  `THREAD_PRIORITY_TIME_CRITICAL` to the swarm tick. Expected p99 jitter
  drops to ≤ 2 ms (vs the current ~6 ms standalone).
- **Merge `cortex.ao` into the swarm's input:** currently the swarm feeds
  the shared Hebbian with synthetic `(t + i) % 10` pulses. Once Task 2
  is live, feed it from `cortex.ao.profile_5d()` so the learned field
  reflects real AO composition driven by live body state.
- **GPU mirror of `cortex.hebbian.W`:** keep a CuPy view of the 25-cell
  field so the doing kernel's T\* gate can read it without a host trip.
  Currently the doing kernel is a parallel substrate that doesn't see
  the learned W — unifying them closes the last loop.
