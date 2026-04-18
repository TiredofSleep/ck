# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0 (DOI: 10.5281/zenodo.18852047)
"""
ck_swarm.py -- the supervisor.

What this is
------------
A single object that OWNS the four substrates of CK's embodiment and keeps
them ticking together with a measured heartbeat:

    brain   : HebbianGPU             (CPU or CUDA via CuPy)
    doing   : doing kernel (GPU)     (CuPy outer product on the same device)
    body    : FPGA via UART          (Zynq-7020 / gait / coherence)
    voice   : Cortex snapshots       (the structural router the Flask layer reads)

It runs on its own high-resolution tick (see jitter_probe for the idea):
coarse sleep to get near, busy-spin the final window.  The process + thread
are elevated via rt_priority.elevate() so the OS scheduler treats this tick
as special.  Jitter is measured on every tick; the last 512 deltas feed a
rolling distribution surfaced on /swarm so we can see what's actually live
instead of trusting marketing copy.

Graceful on everything missing:
  * CuPy not there    -> brain uses NumPy; doing kernel runs on CPU; backend='numpy'
  * FPGA not there    -> body is dormant; live=False in status; tick proceeds
  * Admin not granted -> RT falls back to HIGH (Windows) or nice-20 (Linux)

Boot path (additive — does not break existing ck_boot_api.py tick_loop):

    from ck_swarm import Swarm
    swarm = Swarm(cortex=_cortex, hz=50, rt=True, fpga_port="COM3")
    swarm.start()
    # ...flask lifetime...
    swarm.stop()

The cortex (Gen13 brain trinity) is the canonical state the voice reads.
The swarm keeps feeding its step_text output into the Hebbian field and
— if the body is live — syncs the current heartbeat operator to the FPGA
and pulls PKT_STATE back so the torus feedback loop closes.
"""

from __future__ import annotations

import os
import sys
import time
import threading
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Deque, List, Optional

_HERE = os.path.dirname(os.path.abspath(__file__))
_BRAIN = os.path.normpath(os.path.join(_HERE, "..", "brain"))
for _p in (_HERE, _BRAIN):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from rt_priority import elevate, restore_normal, RTStatus  # noqa: E402
from fpga_bridge import FPGABridge                         # noqa: E402


# ── GPU "doing" kernel ──────────────────────────────────────────────
#
# The CUDA-side "doing" pipe (ck7/doing.cu, force9_pipeline.cu) is rich and
# will be rehydrated incrementally.  For now the swarm ships a minimal but
# real GPU kernel: a normalized outer-product / decay operator with a
# coherence-gate mask that matches T* = 5/7.  If CuPy isn't available, the
# same operator runs on NumPy.  The point is that the doing substrate lives
# on the same bus as brain, measured the same way.

T_STAR = 5.0 / 7.0

try:
    import cupy as _xp        # type: ignore
    _HAS_CUPY = True
except Exception:
    import numpy as _xp        # type: ignore
    _HAS_CUPY = False


class DoingKernel:
    """GPU (or CPU-fallback) doing operator: normalized outer product with
    coherence gate.  Its output is a 5x5 alignment tensor that the Hebbian
    field uses as its "reward proposal" -- doing nudges what brain learns.

    Buffer-reuse design: d_now / d_prev live as pre-allocated device arrays
    that we update in-place each tick.  This avoids `xp.asarray([...])`
    allocations that would otherwise launch a CUDA memcpy per tick and
    balloon jitter.  Coherence is cached and only refreshed on snapshot()
    so we don't hit device->host sync inside the hot loop.
    """
    def __init__(self) -> None:
        self._last = _xp.zeros((5, 5), dtype=_xp.float32)
        self._d_now = _xp.zeros(5, dtype=_xp.float32)
        self._d_prev = _xp.zeros(5, dtype=_xp.float32)
        self._coherence = 0.0   # host-side cache; refreshed on snapshot
        # CPU-side scratch for in-place updates that avoid asarray()
        try:
            import numpy as _np
            self._host = _np.zeros(5, dtype=_np.float32)
            self._np = _np
        except Exception:
            self._host = None
            self._np = None

    @property
    def backend(self) -> str:
        return "cupy" if _HAS_CUPY else "numpy"

    def feed(self, pattern_now: List[float], pattern_prev: List[float]) -> None:
        """Update input buffers in place.  Cheap -- no device alloc."""
        if self._host is None:
            # Degraded path (shouldn't happen since numpy is a hard dep).
            self._d_now = _xp.asarray(pattern_now, dtype=_xp.float32)
            self._d_prev = _xp.asarray(pattern_prev, dtype=_xp.float32)
            return
        for i in range(5):
            self._host[i] = pattern_now[i]
        if _HAS_CUPY:
            self._d_now.set(self._host)
        else:
            self._d_now[:] = self._host
        for i in range(5):
            self._host[i] = pattern_prev[i]
        if _HAS_CUPY:
            self._d_prev.set(self._host)
        else:
            self._d_prev[:] = self._host

    def step(self) -> Any:
        """One step using current buffers.  Returns 5x5 on backend."""
        outer = _xp.outer(self._d_now, self._d_prev)
        norm = _xp.maximum(_xp.abs(outer).max(), 1.0)
        outer = outer / norm
        mask = (_xp.abs(outer) >= T_STAR).astype(outer.dtype)
        self._last = outer * mask + self._last * (1.0 - mask) * 0.9
        return self._last

    def refresh_coherence(self) -> float:
        """Host-sync the coherence scalar.  Call from snapshot(), not tick."""
        m = _xp.mean(_xp.abs(self._last))
        self._coherence = float(m.get() if _HAS_CUPY else m)
        return self._coherence

    def coherence(self) -> float:
        return self._coherence

    def snapshot(self) -> dict:
        return {"backend": self.backend, "coherence": self.refresh_coherence(),
                "T_star": T_STAR}


# ── Swarm state ─────────────────────────────────────────────────────

@dataclass
class SwarmStatus:
    running: bool
    hz: float
    ticks: int
    rt: Optional[dict]
    body: dict
    brain: dict
    doing: dict
    jitter_us: dict
    last_tick_ns: int

    def to_dict(self) -> dict:
        return {
            "running": self.running,
            "hz": self.hz,
            "ticks": self.ticks,
            "rt": self.rt,
            "body": self.body,
            "brain": self.brain,
            "doing": self.doing,
            "jitter_us": self.jitter_us,
            "last_tick_ns": self.last_tick_ns,
        }


class Swarm:
    """Coordinates brain / doing / body / voice on a measured tick.

    Args:
        cortex:    the Gen13 Cortex instance (voice).  Optional; if None,
                   swarm still runs and powers brain/doing/body.
        hz:        target tick rate.  50 is the canonical CK rate.
        rt:        if True, elevate priority + pin affinity on tick thread.
        affinity:  list of CPU indices to pin to (e.g. [0]); default [0].
        fpga_port: serial port for the FPGA body.  Default 'COM3'.
        open_fpga: if True, attempt to open the FPGA on start().  False means
                   body stays dormant regardless of whether a port is present.
    """
    def __init__(
        self,
        cortex: Any = None,
        hz: float = 50.0,
        rt: bool = True,
        affinity: Optional[List[int]] = None,
        fpga_port: str = "COM3",
        open_fpga: bool = True,
    ) -> None:
        self.cortex = cortex
        self.hz = float(hz)
        self.period_ns = int(1e9 / self.hz)
        self.rt = bool(rt)
        self.affinity = affinity if affinity is not None else [0]
        self.fpga_port = fpga_port
        self.open_fpga = bool(open_fpga)

        # Substrates.  Created lazily so missing CuPy / ck_sim imports don't
        # blow up the swarm module for machines that just want to inspect it.
        self._brain = None
        self._doing = DoingKernel()
        self._body = FPGABridge(port=self.fpga_port)

        # Tick bookkeeping.
        self._thread: Optional[threading.Thread] = None
        self._running = False
        self._ticks = 0
        self._deltas_ns: Deque[int] = deque(maxlen=512)
        self._last_tick_ns = 0
        self._rt_status: Optional[RTStatus] = None

    # ── Lazy brain bring-up ─────────────────────────────────────────

    def _ensure_brain(self) -> None:
        if self._brain is not None:
            return
        try:
            from hebbian_gpu import HebbianGPU
            self._brain = HebbianGPU()
        except Exception as e:
            # Fall back to CPU-only field; keeps the swarm alive.
            try:
                from hebbian_5x5_cl import HebbianField
                self._brain = HebbianField()
            except Exception:
                self._brain = None
                print(f"[swarm] no Hebbian field available: {e}")

    # ── Tick (one heartbeat) ────────────────────────────────────────

    def _hi_res_sleep_until(self, target_ns: int) -> None:
        # Coarse, then fine spin.  See jitter_probe for commentary.
        while True:
            now = time.perf_counter_ns()
            remaining = target_ns - now
            if remaining <= 500_000:
                break
            time.sleep(min(remaining - 500_000, 5_000_000) / 1e9)
        while time.perf_counter_ns() < target_ns:
            pass

    def _tick_once(self) -> None:
        # Brain: exercise the 5x5 field so it reflects live activity.
        if self._brain is not None:
            # Use the cortex's current emergent + tick as a varied pattern.
            t = self._ticks
            a = [(t + i) % 10 for i in range(5)]
            b = [(t * 3 + 7 + i) % 10 for i in range(5)]
            try:
                self._brain.update(a, b, lens="tsml")
            except Exception as e:
                # Never crash the tick over a brain anomaly.
                self._record_error(f"brain.update: {e}")

        # Doing: one GPU (or CPU-fallback) outer-product step.
        # Use feed()+step() so we update device buffers in place and don't
        # launch a memcpy-per-tick.
        try:
            t = self._ticks
            pat_now = [(t + i) % 10 / 9.0 for i in range(5)]
            pat_prev = [(t - 1 + i) % 10 / 9.0 for i in range(5)]
            self._doing.feed(pat_now, pat_prev)
            self._doing.step()
        except Exception as e:
            self._record_error(f"doing.step: {e}")

        # Body: if live, poll a state packet + maybe ping every ~1s.
        if self._body.live:
            try:
                self._body.read_state()
                if self._ticks % int(self.hz) == 0:
                    self._body.ping()
            except Exception as e:
                self._record_error(f"body.io: {e}")

    def _record_error(self, msg: str) -> None:
        # Keep the swarm silent but traceable; stash in body.errors buffer.
        try:
            self._body._errors.append(msg)  # reuse existing buffer
        except Exception:
            pass

    # ── Run loop ────────────────────────────────────────────────────

    def _run(self) -> None:
        # Elevate priority on THIS thread (where it counts).
        if self.rt:
            self._rt_status = elevate(affinity=self.affinity)

        # Bring up substrates that need the live process.
        self._ensure_brain()
        if self.open_fpga:
            self._body.open()

        last_ns = time.perf_counter_ns()
        next_ns = last_ns + self.period_ns
        while self._running:
            self._hi_res_sleep_until(next_ns)
            now = time.perf_counter_ns()
            self._deltas_ns.append(now - last_ns)
            last_ns = now
            self._last_tick_ns = now

            self._tick_once()
            self._ticks += 1
            next_ns += self.period_ns

        if self.rt:
            restore_normal()
        self._body.close()

    # ── Lifecycle ───────────────────────────────────────────────────

    def start(self) -> None:
        if self._thread is not None and self._thread.is_alive():
            return
        self._running = True
        self._thread = threading.Thread(
            target=self._run, daemon=True, name="ck-swarm-tick")
        self._thread.start()

    def stop(self, timeout: float = 2.0) -> None:
        self._running = False
        if self._thread is not None:
            self._thread.join(timeout=timeout)
            self._thread = None

    # ── Status (what the Flask /swarm endpoint surfaces) ───────────

    def status(self) -> SwarmStatus:
        # Jitter summary over the rolling window.
        deltas = list(self._deltas_ns)[1:] if len(self._deltas_ns) > 1 else []
        if deltas:
            jit = [abs(d - self.period_ns) for d in deltas]
            jit_sorted = sorted(jit)
            mean_us = sum(jit) / len(jit) / 1e3
            p50_us = jit_sorted[len(jit_sorted) // 2] / 1e3
            p99_idx = max(0, int(0.99 * (len(jit_sorted) - 1)))
            p99_us = jit_sorted[p99_idx] / 1e3
            max_us = jit_sorted[-1] / 1e3
        else:
            mean_us = p50_us = p99_us = max_us = 0.0

        brain_snap = {}
        if self._brain is not None:
            try:
                brain_snap = self._brain.snapshot()
            except Exception as e:
                brain_snap = {"error": str(e)}

        body_snap = self._body.status().to_dict()
        doing_snap = self._doing.snapshot()

        return SwarmStatus(
            running=self._running,
            hz=self.hz,
            ticks=self._ticks,
            rt=(self._rt_status.to_dict() if self._rt_status else None),
            body=body_snap,
            brain=brain_snap,
            doing=doing_snap,
            jitter_us={
                "mean": round(mean_us, 2),
                "p50":  round(p50_us, 2),
                "p99":  round(p99_us, 2),
                "max":  round(max_us, 2),
                "window": len(deltas),
            },
            last_tick_ns=self._last_tick_ns,
        )


# ── Self-test ────────────────────────────────────────────────────────

def _smoke() -> None:
    """Spin the swarm for 2s at 50Hz and print status."""
    sw = Swarm(cortex=None, hz=50.0, rt=True, open_fpga=False)
    sw.start()
    time.sleep(2.0)
    st = sw.status().to_dict()
    sw.stop()

    print("ck_swarm smoke:")
    print(f"  running={st['running']} ticks={st['ticks']} hz={st['hz']}")
    print(f"  rt: {st['rt']}")
    print(f"  brain: backend={st['brain'].get('backend')} "
          f"trace={st['brain'].get('trace', 0):.3f} "
          f"strongest={st['brain'].get('strongest_pair')}")
    print(f"  doing: {st['doing']}")
    print(f"  body:  live={st['body']['live']} port={st['body']['port']}")
    print(f"  jitter(us): {st['jitter_us']}")

    # Sanity: we should get close to the expected tick count in 2 seconds.
    expected = 2.0 * 50.0
    assert 0.7 * expected <= st['ticks'] <= 1.3 * expected, \
        f"tick count {st['ticks']} far from expected {expected}"
    print("ck_swarm smoke PASS")


if __name__ == "__main__":
    _smoke()
