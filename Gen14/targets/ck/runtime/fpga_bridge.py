# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0 (DOI: 10.5281/zenodo.18852047)
"""
fpga_bridge.py -- the body half of the swarm.

Wraps the existing ck_protocol packet framing with a supervised serial
connection that:

  * opens lazily (so import never blocks boot, even if the board is off),
  * stays connected across ticks (no per-tick open/close thrash),
  * answers ping() with real round-trip latency if alive, else `None`,
  * degrades to "dormant" silently so the swarm can still tick without
    a board attached.

When the FPGA is live, state() returns the most recent PKT_STATE the
board sent us (being/doing/becoming/fuse operators, coherence, tick,
brain_ticks, and optional gait fields).  The swarm supervisor folds
those numbers into the /swarm endpoint alongside brain and RT status.

Honest defaults: no auto-open on import.  Call open() explicitly.  Never
raises on a missing port -- you get `live=False` in status().
"""

from __future__ import annotations

import os
import sys
import time
from dataclasses import dataclass, field
from typing import List, Optional

# Bring in the existing packet protocol so we don't duplicate framing.
_DOG_DIR = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "xiaor_dog"))
if _DOG_DIR not in sys.path:
    sys.path.insert(0, _DOG_DIR)

try:
    from ck_protocol import (  # type: ignore
        make_packet, parse_packet,
        pack_ping, unpack_pong, unpack_state,
        pack_gait, pack_estop,
        PKT_PING, PKT_PONG, PKT_STATE, PKT_GAIT, PKT_ESTOP,
        GAIT_STAND, GAIT_WALK, GAIT_TROT, GAIT_BOUND, GAIT_NAMES,
    )
    _HAS_PROTOCOL = True
except Exception as _e:
    _HAS_PROTOCOL = False
    _PROTOCOL_ERROR = str(_e)

try:
    import serial  # pyserial
    _HAS_SERIAL = True
except Exception as _e:
    _HAS_SERIAL = False
    _SERIAL_ERROR = str(_e)


DEFAULT_PORT = "COM3"
DEFAULT_BAUD = 115200
DEFAULT_TIMEOUT = 0.050   # 50 ms -- bounded read so the tick stays on schedule


@dataclass
class FPGAStatus:
    live: bool
    port: str
    baud: int
    last_state: Optional[dict] = None
    last_ping_ms: Optional[float] = None
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "live": self.live,
            "port": self.port,
            "baud": self.baud,
            "last_state": self.last_state,
            "last_ping_ms": self.last_ping_ms,
            "errors": list(self.errors[-8:]),  # keep last 8 only
        }


class FPGABridge:
    """Supervised UART bridge to the Zynq-7020 CK board.

    Usage:
        bridge = FPGABridge(port="COM3")
        bridge.open()       # no-op if no board / port -> errors[]
        if bridge.live:
            bridge.ping()
            st = bridge.read_state()
            bridge.gait("trot")
    """

    def __init__(self, port: str = DEFAULT_PORT, baud: int = DEFAULT_BAUD,
                 timeout: float = DEFAULT_TIMEOUT) -> None:
        self.port = port
        self.baud = baud
        self.timeout = timeout
        self._ser = None
        self._last_state: Optional[dict] = None
        self._last_ping_ms: Optional[float] = None
        self._errors: List[str] = []

    @property
    def live(self) -> bool:
        return self._ser is not None and self._ser.is_open

    def open(self) -> bool:
        """Attempt to open the serial port.  Returns True on success,
        False on any failure (port not present, permission denied, etc)."""
        if not _HAS_SERIAL:
            self._errors.append(f"pyserial unavailable: {_SERIAL_ERROR}")
            return False
        if not _HAS_PROTOCOL:
            self._errors.append(f"ck_protocol unavailable: {_PROTOCOL_ERROR}")
            return False
        try:
            self._ser = serial.Serial(
                self.port, self.baud, timeout=self.timeout, write_timeout=self.timeout,
            )
            # Brief wait for any boot banner.
            time.sleep(0.05)
            return True
        except Exception as e:
            self._errors.append(f"open({self.port}) failed: {e}")
            self._ser = None
            return False

    def close(self) -> None:
        try:
            if self._ser is not None and self._ser.is_open:
                self._ser.close()
        except Exception:
            pass
        self._ser = None

    # ── I/O primitives ──────────────────────────────────────────────

    def _write(self, pkt: bytes) -> bool:
        if not self.live:
            return False
        try:
            self._ser.write(pkt)
            self._ser.flush()
            return True
        except Exception as e:
            self._errors.append(f"write failed: {e}")
            self.close()
            return False

    def _read_packet(self) -> Optional[tuple]:
        """Best-effort: try to pull one framed CK packet within self.timeout."""
        if not self.live:
            return None
        try:
            # Read a reasonable upper bound; parse_packet tolerates extras.
            buf = self._ser.read(256)
            if not buf:
                return None
            # Find CK sync word.
            idx = buf.find(b"CK")
            if idx < 0:
                return None
            return parse_packet(buf[idx:])
        except Exception as e:
            self._errors.append(f"read failed: {e}")
            return None

    # ── High-level actions ──────────────────────────────────────────

    def ping(self) -> Optional[float]:
        """Send PKT_PING, wait for PKT_PONG.  Returns round-trip ms or None."""
        if not self.live:
            return None
        if not self._write(pack_ping()):
            return None
        result = self._read_packet()
        if not result:
            return None
        pkt_type, payload = result
        if pkt_type != PKT_PONG:
            return None
        info = unpack_pong(payload)
        ms = info.get("latency_ms")
        if ms is not None and ms >= 0:
            self._last_ping_ms = float(ms)
            return self._last_ping_ms
        return None

    def read_state(self) -> Optional[dict]:
        """Pull one PKT_STATE if available."""
        if not self.live:
            return None
        result = self._read_packet()
        if not result:
            return None
        pkt_type, payload = result
        if pkt_type != PKT_STATE:
            return None
        st = unpack_state(payload)
        if st:
            self._last_state = st
        return st

    def gait(self, mode: str, speed: int = 100) -> bool:
        """Set gait by name: 'stand' | 'walk' | 'trot' | 'bound'."""
        if not self.live:
            return False
        mode = mode.lower()
        m = {
            "stand": GAIT_STAND, "walk": GAIT_WALK,
            "trot":  GAIT_TROT,  "bound": GAIT_BOUND,
        }.get(mode)
        if m is None:
            self._errors.append(f"unknown gait: {mode!r}")
            return False
        return self._write(pack_gait(m, speed))

    def estop(self) -> bool:
        """Emergency stop."""
        if not self.live:
            return False
        return self._write(pack_estop())

    # ── Status ──────────────────────────────────────────────────────

    def status(self) -> FPGAStatus:
        return FPGAStatus(
            live=self.live,
            port=self.port,
            baud=self.baud,
            last_state=self._last_state,
            last_ping_ms=self._last_ping_ms,
            errors=list(self._errors),
        )


# ── Self-test ────────────────────────────────────────────────────────

def _smoke() -> None:
    port = os.environ.get("CK_FPGA_PORT", DEFAULT_PORT)
    b = FPGABridge(port=port)
    opened = b.open()
    st = b.status().to_dict()
    print(f"fpga_bridge smoke: opened={opened} port={port}")
    print(f"  status: {st}")
    if opened:
        ms = b.ping()
        print(f"  ping: {ms} ms")
        b.close()
    else:
        print("  (no board; swarm will run with dormant body)")


if __name__ == "__main__":
    _smoke()
