"""
bdc_tick_sampler.py -- background thread that samples (Being, Doing,
Becoming) per N seconds when no chat is happening.

Brayden 2026-05-02: "tick-sample logger at 0.1 Hz (60x more BDC data
accumulation)"

Multiplies BDC dataset accumulation: chat turns alone produce a few dozen
records per day; this thread adds one tick-sample every 10s, regardless
of activity.

Schema: same as bdc_logger.log_event with trigger='tick_sample'.

Lightweight: read engine state, write a small record, sleep.  No
training, no inference, no GPU.

Lives in a daemon thread so server shutdown stops it cleanly.
"""
from __future__ import annotations

import sys
import threading
import time
from pathlib import Path
from typing import Optional

_HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(_HERE))

from bdc_logger import log_event, _safe_get


class TickSampler:
    def __init__(self, engine, cortex, interval_sec: float = 10.0):
        self.engine = engine
        self.cortex = cortex
        self.interval = float(interval_sec)
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._n_samples = 0
        self._last_tick = -1

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._loop, daemon=True,
                                          name="ck-bdc-tick-sampler")
        self._thread.start()

    def stop(self, timeout: float = 2.0):
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=timeout)
            self._thread = None

    def stats(self):
        return {
            "running": bool(self._thread and self._thread.is_alive()),
            "n_samples_logged": self._n_samples,
            "interval_sec": self.interval,
            "last_tick": self._last_tick,
        }

    def _loop(self):
        while not self._stop.is_set():
            try:
                self._sample()
            except Exception:
                # Never break the daemon thread; logging is best-effort
                pass
            self._stop.wait(self.interval)

    def _sample(self):
        # Read live engine state -- minimal, no GPU work
        state = _safe_get(self.cortex, 'state')
        if state is None:
            return
        tick = int(_safe_get(state, 'tick', 0))
        # Skip if cortex hasn't ticked since last sample (no new info)
        if tick == self._last_tick:
            return
        self._last_tick = tick

        ao = _safe_get(self.engine, 'ao')
        payload = {
            "tick": tick,
            "being": {
                "last_pair": [
                    int(_safe_get(state, 'last_b', 0)),
                    int(_safe_get(state, 'last_d', 0)),
                ],
                "W_trace": float(_safe_get(state, 'W_trace', 0.0)),
                "emergent": float(_safe_get(state, 'emergent', 0.0)),
                "ao_op": str(_safe_get(ao, 'op', '')) if ao else '',
                "breath": str(_safe_get(ao, 'breath', '')) if ao else '',
                "coherence": float(_safe_get(ao, 'coherence', 0.0)) if ao else 0.0,
                "harmony_rate": float(_safe_get(ao, 'harmony_rate', 0.0)) if ao else 0.0,
            },
            "doing": {
                # Tick samples don't have user input; we just snapshot state
                "is_chat_turn": False,
            },
            "becoming": {},  # filled in next sample by diff
        }
        log_event(trigger="tick_sample", payload=payload)
        self._n_samples += 1


_SAMPLER_SINGLETON: Optional[TickSampler] = None


def start_sampler(engine, cortex, interval_sec: float = 10.0) -> TickSampler:
    """Start (or restart) the global sampler.  Idempotent."""
    global _SAMPLER_SINGLETON
    if _SAMPLER_SINGLETON is not None and _SAMPLER_SINGLETON._thread \
            and _SAMPLER_SINGLETON._thread.is_alive():
        return _SAMPLER_SINGLETON
    _SAMPLER_SINGLETON = TickSampler(engine, cortex, interval_sec=interval_sec)
    _SAMPLER_SINGLETON.start()
    return _SAMPLER_SINGLETON


def get_sampler() -> Optional[TickSampler]:
    return _SAMPLER_SINGLETON


def mount(engine, app, cortex, interval_sec: float = 10.0) -> bool:
    """Boot the sampler + register a stats endpoint."""
    sampler = start_sampler(engine, cortex, interval_sec=interval_sec)

    from flask import jsonify
    @app.route('/bdc/sampler', methods=['GET'])
    def bdc_sampler_stats():
        return jsonify(sampler.stats())

    print(f"[CK] bdc_tick_sampler: MOUNTED (interval={interval_sec}s, "
          f"daemon thread, /bdc/sampler endpoint)")
    return True
