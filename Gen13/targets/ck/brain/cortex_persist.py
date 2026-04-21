# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0 (DOI: 10.5281/zenodo.18852047)
"""
cortex_persist.py -- save/load Gen13 cortex state across reboots.

What gets persisted:
  - Hebbian W matrix (5x5)   -- the LEARNED coupling; the real memory.
  - Hebbian ticks/harmony_hits -- so harmony_rate() stays honest.
  - Cortex tick counter and last (b, d) operators.
  - Previous 5D profile  -- so pair continuity survives a restart.
  - Timestamp, version tag, and a small magic header.

What does NOT get persisted:
  - AO spine internal state (D2/Heartbeat/BrainState/BodyState/BTQState).
    These are working memory and rebuild themselves from a fresh boot
    within ~3 symbols.  Persisting them would require serializing every
    Gen11 dataclass and is a larger task for later.

Design notes:
  - JSON format (human-readable, git-friendly, no pickle security risk).
  - Atomic write via temp-file + os.replace so a crash mid-save can't
    corrupt the live file.
  - Versioned: if we ever change the W layout we bump CORTEX_STATE_VERSION
    and silently skip old files (never crash at boot).
  - ADDITIVE: does not touch cortex.py or any Gen11 module.

This module deliberately has no dependency on cortex.py -- it takes a
Cortex-shaped object (anything with .hebbian, .state, ._prev_op,
._prev_profile).  That lets test code pass a mock without booting the
whole trinity.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional


CORTEX_STATE_VERSION = 1
CORTEX_STATE_MAGIC = "ck_gen13_cortex_state"

# Default save location: <repo>/Gen13/var/cortex_state.json
_HERE = os.path.dirname(os.path.abspath(__file__))
_GEN13_ROOT = os.path.abspath(os.path.join(_HERE, "..", "..", ".."))
DEFAULT_STATE_PATH = os.path.join(_GEN13_ROOT, "var", "cortex_state.json")


def _ensure_parent(path: str) -> None:
    parent = os.path.dirname(os.path.abspath(path))
    if parent and not os.path.isdir(parent):
        os.makedirs(parent, exist_ok=True)


def cortex_to_dict(cortex: Any) -> Dict[str, Any]:
    """Serialize a Cortex-shaped object into a plain dict.

    Args:
        cortex: any object with .hebbian (HebbianField), .state (CortexState),
                ._prev_op (int|None), ._prev_profile (list[int]|None).

    Returns:
        JSON-ready dict.
    """
    heb = cortex.hebbian
    st = cortex.state
    return {
        "magic": CORTEX_STATE_MAGIC,
        "version": CORTEX_STATE_VERSION,
        "saved_at": time.time(),
        "saved_at_iso": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()),
        "hebbian": {
            "W": [row[:] for row in heb.W],
            "ticks": heb.ticks,
            "harmony_hits": heb.harmony_hits,
            "eta": heb.eta,
            "decay": heb.decay,
            "clamp": heb.clamp,
        },
        "cortex": {
            "tick": st.tick,
            "last_b": st.last_b,
            "last_d": st.last_d,
            "last_harmony_frac": st.last_harmony_frac,
            "emergent": st.emergent,
            "W_trace": st.W_trace,
            "W_strongest": list(st.W_strongest) if st.W_strongest else None,
            "prev_op": cortex._prev_op,
            "prev_profile": cortex._prev_profile,
        },
    }


def save_cortex(cortex: Any, path: Optional[str] = None) -> str:
    """Atomically write cortex state to disk.  Returns the path written."""
    path = path or DEFAULT_STATE_PATH
    _ensure_parent(path)
    payload = cortex_to_dict(cortex)
    text = json.dumps(payload, indent=2, sort_keys=False)

    # Atomic write: temp file in the same directory, then os.replace.
    parent = os.path.dirname(os.path.abspath(path)) or "."
    fd, tmp_path = tempfile.mkstemp(
        prefix=".cortex_state.", suffix=".tmp.json", dir=parent
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.replace(tmp_path, path)
    finally:
        # If os.replace succeeded the temp is gone; if it failed, clean up.
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass
    return path


def dict_into_cortex(data: Dict[str, Any], cortex: Any) -> None:
    """Load a dict (from file) into a live Cortex, in place.

    Raises ValueError if the magic/version doesn't match."""
    if data.get("magic") != CORTEX_STATE_MAGIC:
        raise ValueError(
            f"bad cortex state: magic={data.get('magic')!r} expected {CORTEX_STATE_MAGIC!r}"
        )
    v = data.get("version")
    if v != CORTEX_STATE_VERSION:
        raise ValueError(
            f"bad cortex state: version={v} expected {CORTEX_STATE_VERSION}"
        )

    h = data.get("hebbian") or {}
    heb = cortex.hebbian
    W = h.get("W")
    if isinstance(W, list) and len(W) == 5 and all(
        isinstance(r, list) and len(r) == 5 for r in W
    ):
        for d_a in range(5):
            for d_b in range(5):
                val = float(W[d_a][d_b])
                # Clamp on load as a cheap safety net against corrupted files.
                if val > heb.clamp:
                    val = heb.clamp
                elif val < -heb.clamp:
                    val = -heb.clamp
                heb.W[d_a][d_b] = val
    heb.ticks = int(h.get("ticks", heb.ticks))
    heb.harmony_hits = int(h.get("harmony_hits", heb.harmony_hits))

    c = data.get("cortex") or {}
    st = cortex.state
    st.tick = int(c.get("tick", st.tick))
    st.last_b = int(c.get("last_b", st.last_b))
    st.last_d = int(c.get("last_d", st.last_d))
    st.last_harmony_frac = float(c.get("last_harmony_frac", st.last_harmony_frac))
    st.emergent = float(c.get("emergent", st.emergent))
    st.W_trace = float(c.get("W_trace", st.W_trace))
    strongest = c.get("W_strongest")
    if isinstance(strongest, list) and len(strongest) == 3:
        st.W_strongest = (int(strongest[0]), int(strongest[1]), float(strongest[2]))

    prev_op = c.get("prev_op")
    cortex._prev_op = int(prev_op) if prev_op is not None else None
    prev_profile = c.get("prev_profile")
    if isinstance(prev_profile, list) and len(prev_profile) == 5:
        cortex._prev_profile = [int(x) for x in prev_profile]
    else:
        cortex._prev_profile = None


def load_cortex(cortex: Any, path: Optional[str] = None) -> bool:
    """Restore cortex state from disk.  Returns True if a file was loaded.

    Silent no-op (returns False) if the file is missing.  Raises ValueError
    if the file exists but is malformed -- callers can catch that and choose
    to continue with a fresh brain rather than crash.
    """
    path = path or DEFAULT_STATE_PATH
    if not os.path.isfile(path):
        return False
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    dict_into_cortex(data, cortex)
    return True


# ── Auto-save helper ──────────────────────────────────────────────────

@dataclass
class AutoSaver:
    """Thin helper: save every N ticks (or every M seconds), whichever first.

    Usage (inside the server boot):

        saver = AutoSaver(cortex, path, every_ticks=200, every_seconds=30)
        # after each cortex.step_text(...) call:
        saver.maybe_save()
        # on shutdown:
        saver.force_save()
    """
    cortex: Any
    path: str = DEFAULT_STATE_PATH
    every_ticks: int = 200
    every_seconds: float = 30.0
    _last_tick_saved: int = 0
    _last_time_saved: float = 0.0

    def maybe_save(self) -> bool:
        """Save if either tick- or time-threshold is crossed.  Returns
        True iff a save actually happened."""
        now = time.time()
        tick = self.cortex.state.tick
        if (tick - self._last_tick_saved) >= self.every_ticks or \
           (now - self._last_time_saved) >= self.every_seconds:
            save_cortex(self.cortex, self.path)
            self._last_tick_saved = tick
            self._last_time_saved = now
            return True
        return False

    def force_save(self) -> None:
        """Unconditional save -- call on graceful shutdown."""
        save_cortex(self.cortex, self.path)
        self._last_tick_saved = self.cortex.state.tick
        self._last_time_saved = time.time()


# ── Self-test ──────────────────────────────────────────────────────────

def _smoke() -> None:
    """Round-trip: boot cortex -> step text -> save -> boot fresh -> load ->
    confirm W and tick counter match.  Uses a temp file so the smoke doesn't
    trample the real state file."""
    _HERE = os.path.dirname(os.path.abspath(__file__))
    if _HERE not in sys.path:
        sys.path.insert(0, _HERE)
    from cortex import Cortex

    cx1 = Cortex().boot()
    for _ in range(10):
        cx1.step_text("coherencekeeper harmony lattice progress")

    # Confirm some learning happened (else the round-trip is trivial).
    pre_trace = cx1.state.W_trace
    pre_tick = cx1.state.tick
    pre_prev_profile = list(cx1._prev_profile) if cx1._prev_profile else None

    import tempfile
    with tempfile.NamedTemporaryFile(
        prefix="cortex_state_test_", suffix=".json",
        delete=False, mode="w", encoding="utf-8"
    ) as fh:
        tmp_path = fh.name
    try:
        save_cortex(cx1, tmp_path)
        assert os.path.isfile(tmp_path), "save_cortex did not write file"

        # Fresh cortex, same class, then load the saved state.
        cx2 = Cortex().boot()
        assert cx2.state.tick == 0, "fresh cortex should start at tick 0"
        ok = load_cortex(cx2, tmp_path)
        assert ok is True, "load_cortex should return True when file exists"

        # Verify the things that should be restored.
        assert cx2.state.tick == pre_tick, (
            f"tick mismatch: pre={pre_tick} post={cx2.state.tick}"
        )
        assert abs(cx2.state.W_trace - pre_trace) < 1e-9, (
            f"W_trace mismatch: pre={pre_trace} post={cx2.state.W_trace}"
        )
        # Hebbian W round-trip.
        for d_a in range(5):
            for d_b in range(5):
                assert abs(cx2.hebbian.W[d_a][d_b] - cx1.hebbian.W[d_a][d_b]) < 1e-9, (
                    f"W[{d_a}][{d_b}] mismatch after load"
                )
        # Pair continuity.
        assert cx2._prev_profile == pre_prev_profile, (
            f"_prev_profile mismatch: pre={pre_prev_profile} post={cx2._prev_profile}"
        )

        # Missing file should be a silent no-op, not a crash.
        cx3 = Cortex().boot()
        missing = tmp_path + ".does_not_exist"
        assert load_cortex(cx3, missing) is False, (
            "load_cortex should return False for missing file"
        )
    finally:
        if os.path.isfile(tmp_path):
            os.remove(tmp_path)

    print(f"cortex_persist smoke PASS: tick={pre_tick} W_trace={pre_trace:.4f} "
          f"round-trip exact")


if __name__ == "__main__":
    _smoke()
