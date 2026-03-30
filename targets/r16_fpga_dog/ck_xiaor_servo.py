"""
ck_xiaor_servo.py -- XiaoR GEEK LewanSoul Servo Protocol
=========================================================
Operator: BREATH (8) -- the legs that move the body.

Python driver for the XiaoR GEEK quadruped's LewanSoul LX series
bus servos. This provides a DIRECT Python -> servo path for:
  - Debugging / manual joint moves without FPGA
  - Verifying servo IDs and ranges before running FPGA gait
  - Reading current joint positions back to R16

In the live system, servo commands flow:
  FPGA gait_vortex -> servo_commander.v -> servo_uart_tx.v -> JM2 PMOD -> XiaoR bus

This file provides the PYTHON fallback path (R16 -> USB-serial -> XiaoR):
  R16 Python -> ck_xiaor_servo.py -> USB-serial -> XiaoR servo bus

Both paths use the same LewanSoul binary packet protocol.

LewanSoul Packet Format:
  [0x55] [0x55] [ID] [LEN] [CMD] [PARAMS...] [CHECKSUM]
  CHECKSUM = ~(ID + LEN + CMD + SUM(PARAMS)) & 0xFF

XiaoR GEEK Servo ID Map (standard XiaoR layout):
  Leg 0 (Front-Right):  Hip=1  Knee=2
  Leg 1 (Front-Left):   Hip=3  Knee=4
  Leg 2 (Rear-Right):   Hip=5  Knee=6
  Leg 3 (Rear-Left):    Hip=7  Knee=8

Servo positions: 0-1000 (LewanSoul units), center=500
  Hip center   = 500 (pointing straight down)
  Knee center  = 500 (90 degree bend)
  Position to microseconds: pos * 1000 / 500 + 500 (approx)

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""

import serial
import time
import struct
from typing import List, Optional, Tuple

# ── LewanSoul protocol constants ───────────────────────────────────────────

LEWAN_SYNC      = 0x55
SERVO_BROADCAST = 0xFE   # Broadcast ID (all servos respond)

# Commands
CMD_MOVE_TIME_WRITE   = 1    # Move to position in time
CMD_MOVE_TIME_READ    = 2    # Read target position + time
CMD_MOVE_TIME_WAIT    = 7    # Queue move (waits for CMD_MOVE_START)
CMD_MOVE_START        = 11   # Execute queued move
CMD_MOVE_STOP         = 12   # Stop motor (hold position)
CMD_ID_WRITE          = 13   # Set servo ID
CMD_ANGLE_OFFSET_ADJ  = 17   # Set angle offset
CMD_ANGLE_LIMIT_WRITE = 20   # Set angle limits [min, max]
CMD_ANGLE_LIMIT_READ  = 21   # Read angle limits
CMD_VIN_LIMIT_WRITE   = 22   # Set voltage limits
CMD_TEMP_MAX_WRITE    = 24   # Set max temperature
CMD_TEMP_READ         = 26   # Read temperature
CMD_VIN_READ          = 27   # Read input voltage
CMD_POS_READ          = 28   # Read current position
CMD_SERVO_OR_MOTOR    = 29   # Switch servo/motor mode
CMD_LOAD_UNLOAD       = 31   # Enable/disable torque

# ── Physical layout ────────────────────────────────────────────────────────

# Servo ID assignments (XiaoR GEEK standard layout)
# leg_idx: 0=FR  1=FL  2=RR  3=RL
SERVO_IDS = {
    # (leg, joint) -> servo_id
    (0, 'hip'):  1,   (0, 'knee'): 2,
    (1, 'hip'):  3,   (1, 'knee'): 4,
    (2, 'hip'):  5,   (2, 'knee'): 6,
    (3, 'hip'):  7,   (3, 'knee'): 8,
}
ALL_SERVO_IDS = list(range(1, 9))   # IDs 1-8

# Position limits (LewanSoul units 0-1000)
POS_CENTER  = 500
POS_MIN     = 0
POS_MAX     = 1000
POS_RANGE   = 200    # +/- from center for safe motion

# Safe positions for standing (all legs extended, balanced)
STAND_POSITIONS = {
    1: 500, 2: 400,   # FR hip, knee
    3: 500, 4: 600,   # FL hip, knee (mirrored)
    5: 500, 6: 400,   # RR hip, knee
    7: 500, 8: 600,   # RL hip, knee (mirrored)
}

# TIG operator -> position offset from center (hip joints)
# Matching servo_commander.v operator-to-angle mapping
OP_HIP_OFFSET = {
    0: 0,     # VOID    -> center (no motion)
    1: -60,   # LATTICE -> slight extension
    2: -120,  # COUNTER -> moderate extension
    3: -60,   # PROGRESS -> step forward
    4: 80,    # COLLAPSE -> flex in
    5: 0,     # BALANCE -> center
    6: 40,    # CHAOS   -> slight flex
    7: 0,     # HARMONY -> center (absorbing state)
    8: -30,   # BREATH  -> oscillate (handled externally)
    9: 100,   # RESET   -> full flex (end of stride)
}

OP_KNEE_OFFSET = {
    0: 0,     1: 20,    2: 40,    3: 20,
    4: -60,   5: 0,     6: -20,   7: 0,
    8: -15,   9: -80,
}


def _checksum(data: bytes) -> int:
    """LewanSoul checksum: ~(sum of ID+LEN+CMD+PARAMS) & 0xFF."""
    return (~sum(data)) & 0xFF


def make_move_packet(servo_id: int, position: int,
                     time_ms: int = 200) -> bytes:
    """
    Build MOVE_TIME_WRITE packet.
    position: 0-1000 (LewanSoul units, 500=center)
    time_ms:  move duration in ms (100-30000)
    """
    position = max(POS_MIN, min(POS_MAX, position))
    time_ms  = max(0, min(30000, time_ms))
    pos_lo  = position & 0xFF
    pos_hi  = (position >> 8) & 0xFF
    t_lo    = time_ms & 0xFF
    t_hi    = (time_ms >> 8) & 0xFF
    body    = bytes([servo_id, 7, CMD_MOVE_TIME_WRITE,
                     pos_lo, pos_hi, t_lo, t_hi])
    return bytes([LEWAN_SYNC, LEWAN_SYNC]) + body + bytes([_checksum(body)])


def make_pos_read_packet(servo_id: int) -> bytes:
    """Build POS_READ request packet."""
    body = bytes([servo_id, 3, CMD_POS_READ])
    return bytes([LEWAN_SYNC, LEWAN_SYNC]) + body + bytes([_checksum(body)])


def make_load_packet(servo_id: int, enable: bool) -> bytes:
    """Enable (True) or disable (False) servo torque."""
    body = bytes([servo_id, 4, CMD_LOAD_UNLOAD, 1 if enable else 0])
    return bytes([LEWAN_SYNC, LEWAN_SYNC]) + body + bytes([_checksum(body)])


def make_stop_packet(servo_id: int) -> bytes:
    """Stop servo motor (hold current position)."""
    body = bytes([servo_id, 3, CMD_MOVE_STOP])
    return bytes([LEWAN_SYNC, LEWAN_SYNC]) + body + bytes([_checksum(body)])


def parse_pos_response(data: bytes) -> Optional[int]:
    """
    Parse POS_READ response.
    Returns position (0-1000) or None on parse error.
    """
    if len(data) < 8:
        return None
    if data[0] != LEWAN_SYNC or data[1] != LEWAN_SYNC:
        return None
    servo_id = data[2]
    length   = data[3]
    cmd      = data[4]
    if cmd != CMD_POS_READ or length < 5:
        return None
    body = data[2:2 + length]
    if _checksum(body[:-1]) != body[-1]:
        return None  # CRC mismatch
    pos = data[5] | (data[6] << 8)
    return pos


def op_to_position(op: int, leg: int, joint: str,
                   base: Optional[int] = None) -> int:
    """
    Convert TIG operator to servo position.
    Mirrors the logic in servo_commander.v.

    leg:   0=FR 1=FL 2=RR 3=RL
    joint: 'hip' or 'knee'
    base:  override center (uses STAND_POSITIONS if None)
    """
    sid  = SERVO_IDS.get((leg, joint), 1)
    center = base if base is not None else STAND_POSITIONS.get(sid, POS_CENTER)

    if joint == 'hip':
        offset = OP_HIP_OFFSET.get(op, 0)
    else:
        offset = OP_KNEE_OFFSET.get(op, 0)

    # Mirror left legs (1, 3 = FL, RL)
    if leg in (1, 3):
        offset = -offset

    return max(POS_MIN, min(POS_MAX, center + offset))


class XiaoRServo:
    """
    Python driver for XiaoR GEEK LewanSoul servo bus.
    One serial port drives all 8 servos (half-duplex bus).

    Typical usage:
        dog = XiaoRServo('COM5')
        dog.open()
        dog.stand()           # Move all to stand position
        dog.move(1, 600, 300) # Servo 1 to pos 600 in 300ms
        dog.read_positions()  # Dict of {servo_id: position}
        dog.close()
    """

    HALF_DUPLEX_DELAY = 0.001   # 1ms between TX and RX on same bus

    def __init__(self, port: str, baud: int = 115200):
        self.port = port
        self.baud = baud
        self._ser  = None
        self._positions = {sid: POS_CENTER for sid in ALL_SERVO_IDS}

    def open(self):
        """Open serial port to servo bus."""
        self._ser = serial.Serial(
            self.port, self.baud,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=0.05,
        )
        print(f"[SERVO] XiaoR bus: {self.port} @ {self.baud}")

    def close(self):
        """Close serial port."""
        if self._ser:
            self._ser.close()
            self._ser = None

    def move(self, servo_id: int, position: int, time_ms: int = 200):
        """Move single servo to position in time_ms."""
        pkt = make_move_packet(servo_id, position, time_ms)
        self._ser.write(pkt)

    def move_all(self, positions: dict, time_ms: int = 300):
        """
        Move multiple servos simultaneously.
        positions: {servo_id: position, ...}
        """
        for sid, pos in positions.items():
            pkt = make_move_packet(sid, pos, time_ms)
            self._ser.write(pkt)
            time.sleep(0.002)   # Small gap between packets on shared bus

    def stand(self, time_ms: int = 500):
        """Move all servos to balanced stand position."""
        print("[SERVO] Standing up...")
        self.move_all(STAND_POSITIONS, time_ms)
        time.sleep(time_ms / 1000.0 + 0.1)

    def center(self, time_ms: int = 500):
        """Center all servos (500). Safe position for powerup/powerdown."""
        print("[SERVO] Centering all servos...")
        positions = {sid: POS_CENTER for sid in ALL_SERVO_IDS}
        self.move_all(positions, time_ms)
        time.sleep(time_ms / 1000.0 + 0.1)

    def torque(self, enable: bool):
        """Enable or disable torque on all servos."""
        state = "ON" if enable else "OFF"
        print(f"[SERVO] Torque {state}")
        for sid in ALL_SERVO_IDS:
            self._ser.write(make_load_packet(sid, enable))
            time.sleep(0.002)

    def apply_operators(self, leg_ops: list, time_ms: int = 200):
        """
        Apply TIG operators to all 4 legs.
        leg_ops: list of 4 operators [leg0, leg1, leg2, leg3]
        Uses op_to_position() mapping (matches servo_commander.v).
        """
        positions = {}
        for leg_idx, op in enumerate(leg_ops[:4]):
            for joint in ('hip', 'knee'):
                sid = SERVO_IDS.get((leg_idx, joint))
                if sid is not None:
                    positions[sid] = op_to_position(op, leg_idx, joint)
        self.move_all(positions, time_ms)
        self._positions.update(positions)

    def read_positions(self, timeout: float = 0.1) -> dict:
        """
        Read current positions from all 8 servos.
        Returns {servo_id: position} dict.
        Note: half-duplex bus -- must flush TX first.
        """
        if not self._ser:
            return {}
        positions = {}
        for sid in ALL_SERVO_IDS:
            self._ser.write(make_pos_read_packet(sid))
            time.sleep(self.HALF_DUPLEX_DELAY)
            deadline = time.monotonic() + timeout
            buf = bytearray()
            while time.monotonic() < deadline:
                raw = self._ser.read(self._ser.in_waiting or 1)
                if raw:
                    buf.extend(raw)
                    if len(buf) >= 8:
                        break
                time.sleep(0.005)
            pos = parse_pos_response(bytes(buf))
            if pos is not None:
                positions[sid] = pos
                self._positions[sid] = pos
        return positions

    def scan_servos(self) -> List[int]:
        """
        Scan for responding servo IDs (1-15).
        Returns list of found IDs.
        """
        found = []
        print("[SERVO] Scanning servo IDs...")
        for sid in range(1, 16):
            self._ser.write(make_pos_read_packet(sid))
            time.sleep(0.02)
            raw = self._ser.read(self._ser.in_waiting or 1)
            if raw and len(raw) >= 8:
                pos = parse_pos_response(bytes(raw))
                if pos is not None:
                    found.append(sid)
                    print(f"  ID {sid}: pos={pos}")
        print(f"[SERVO] Found: {found}")
        return found

    @property
    def positions(self) -> dict:
        """Last known positions (cached from last read_positions call)."""
        return dict(self._positions)

    def __repr__(self) -> str:
        return f"XiaoRServo({self.port} servos={ALL_SERVO_IDS})"


# ── CLI entry point ─────────────────────────────────────────────────────────

if __name__ == '__main__':
    """
    Manual servo test tool.

    Usage:
        python ck_xiaor_servo.py COM5 scan
        python ck_xiaor_servo.py COM5 stand
        python ck_xiaor_servo.py COM5 center
        python ck_xiaor_servo.py COM5 read
        python ck_xiaor_servo.py COM5 move 1 600 300  (id pos time_ms)
    """
    import argparse
    ap = argparse.ArgumentParser(description='XiaoR servo test')
    ap.add_argument('port', help='Serial port to servo bus')
    ap.add_argument('cmd',  choices=['scan','stand','center','read','move'],
                    help='Command')
    ap.add_argument('args', nargs='*')
    args = ap.parse_args()

    dog = XiaoRServo(args.port)
    dog.open()

    if args.cmd == 'scan':
        dog.scan_servos()

    elif args.cmd == 'stand':
        dog.stand()
        print("Standing.")

    elif args.cmd == 'center':
        dog.center()
        print("Centered.")

    elif args.cmd == 'read':
        pos = dog.read_positions()
        print("Servo positions:")
        for sid, p in sorted(pos.items()):
            leg = (sid - 1) // 2
            joint = 'hip' if (sid - 1) % 2 == 0 else 'knee'
            names = ['FR', 'FL', 'RR', 'RL']
            print(f"  ID {sid} ({names[leg]}-{joint}): {p}")

    elif args.cmd == 'move':
        if len(args.args) >= 2:
            sid  = int(args.args[0])
            pos  = int(args.args[1])
            t_ms = int(args.args[2]) if len(args.args) >= 3 else 300
            dog.move(sid, pos, t_ms)
            print(f"Moved servo {sid} to {pos} in {t_ms}ms")
        else:
            print("Usage: move <servo_id> <position> [time_ms]")

    dog.close()
