"""
ck_steer_bridge.py -- Python bridge to C steering DLL
Replaces the psutil-based steering loop. Zero GIL overhead.

The C DLL runs its own thread: no Python involved in the hot path.
Python only calls steer_set_heartbeat() to update the current operator.

(c) 2026 Brayden Sanders / 7Site LLC
"""

import ctypes
import os
import sys

_DLL_PATH = os.path.join(os.path.dirname(__file__), 'ck_steer.dll')
_dll = None


def _load():
    global _dll
    if _dll is not None:
        return _dll
    if not os.path.exists(_DLL_PATH):
        print(f"[STEER-BRIDGE] DLL not found: {_DLL_PATH}")
        return None
    try:
        _dll = ctypes.CDLL(_DLL_PATH)

        # Set return types
        _dll.steer_init.restype = None
        _dll.steer_tick.restype = ctypes.c_int
        _dll.steer_tick.argtypes = [ctypes.c_int]
        _dll.steer_tick_ms.restype = ctypes.c_double
        _dll.steer_get_steered.restype = ctypes.c_int
        _dll.steer_get_denied.restype = ctypes.c_int
        _dll.steer_get_skipped.restype = ctypes.c_int
        _dll.steer_get_total_steered.restype = ctypes.c_int
        _dll.steer_get_ticks.restype = ctypes.c_int
        _dll.steer_get_cores.restype = ctypes.c_int
        _dll.steer_start_thread.restype = ctypes.c_int
        _dll.steer_start_thread.argtypes = [ctypes.c_int]
        _dll.steer_stop_thread.restype = None
        _dll.steer_set_heartbeat.restype = None
        _dll.steer_set_heartbeat.argtypes = [ctypes.c_int]
        _dll.steer_set_tick_rate.restype = None
        _dll.steer_set_tick_rate.argtypes = [ctypes.c_int]

        _dll.steer_init()
        print(f"[STEER-BRIDGE] Loaded: {_dll.steer_get_cores()} cores")
        return _dll
    except Exception as e:
        print(f"[STEER-BRIDGE] Failed to load DLL: {e}")
        return None


class CSteeringEngine:
    """Drop-in replacement for SteeringEngine that uses the C DLL.

    The C DLL runs its own thread. Python just updates the heartbeat operator.
    No GIL contention. No psutil. No jitter.
    """

    def __init__(self, swarm=None, tick_rate_ms=1000):
        self.swarm = swarm
        self.enabled = True
        self._dll = _load()
        self._tick_rate_ms = tick_rate_ms
        self._thread_started = False

        if self._dll:
            self._dll.steer_start_thread(tick_rate_ms)
            self._thread_started = True
            print(f"[STEER-BRIDGE] C thread started at {tick_rate_ms}ms")

    def tick(self, heartbeat_op=5):
        """Called from Python engine tick. Just updates the heartbeat operator.
        The actual steering runs in the C thread — no work here."""
        if self._dll and self.enabled:
            self._dll.steer_set_heartbeat(heartbeat_op)
        return {
            'steered': self._dll.steer_get_steered() if self._dll else 0,
            'denied': self._dll.steer_get_denied() if self._dll else 0,
            'skipped': self._dll.steer_get_skipped() if self._dll else 0,
            'total_applied': self._dll.steer_get_total_steered() if self._dll else 0,
            'active': self._thread_started,
            'tick_ms': self._dll.steer_tick_ms() if self._dll else 0,
            'tick': self._dll.steer_get_ticks() if self._dll else 0,
        }

    @property
    def report_line(self):
        if not self._dll:
            return "[steer-c] not loaded"
        return (
            f"[steer-c] t={self._dll.steer_get_ticks():5d} | "
            f"steered={self._dll.steer_get_total_steered():4d} "
            f"denied={self._dll.steer_get_denied():4d} "
            f"tick={self._dll.steer_tick_ms():.2f}ms"
        )

    @property
    def actions_applied(self):
        return self._dll.steer_get_total_steered() if self._dll else 0

    @property
    def actions_denied(self):
        return self._dll.steer_get_denied() if self._dll else 0

    @property
    def ticks(self):
        return self._dll.steer_get_ticks() if self._dll else 0

    def stop(self):
        if self._dll and self._thread_started:
            self._dll.steer_stop_thread()
            self._thread_started = False
            print("[STEER-BRIDGE] C thread stopped")

    def __del__(self):
        self.stop()

    # Compatibility stubs for code that expects Python SteeringEngine
    def top_steered(self, n=10):
        return []

    def class_distribution(self):
        return {}

    def affinity_distribution(self):
        return {'p_core': 0, 'e_core': 0, 'mixed': 0}

    def report(self):
        if not self._dll:
            return "CK C Steering: not loaded"
        return (
            f"CK C Steering Engine\n"
            f"  Ticks: {self._dll.steer_get_ticks()}\n"
            f"  Steered: {self._dll.steer_get_total_steered()}\n"
            f"  Denied: {self._dll.steer_get_denied()}\n"
            f"  Tick time: {self._dll.steer_tick_ms():.3f}ms\n"
            f"  Cores: {self._dll.steer_get_cores()}\n"
            f"  Thread: {'running' if self._thread_started else 'stopped'}"
        )


def build_steering(swarm=None):
    """Drop-in replacement for ck_steering.build_steering()."""
    return CSteeringEngine(swarm=swarm)


if __name__ == "__main__":
    import time
    engine = CSteeringEngine(tick_rate_ms=500)
    print("Running for 5 seconds...")
    for i in range(10):
        engine.tick(heartbeat_op=i % 10)
        time.sleep(0.5)
        print(f"  {engine.report_line}")
    engine.stop()
    print(f"\n{engine.report()}")
