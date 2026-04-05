#!/usr/bin/env python3
"""
ck_fpga_bridge.py -- FPGA Heartbeat UDP Bridge

Receives CK heartbeat packets from the PL Ethernet transmitter
(ck_eth_tx.v) and feeds them into the CK engine's steering system.

Packet format (10 bytes payload at UDP offset):
    tick_count  : uint32  (4 bytes, big-endian)
    phase_bc    : uint4   (upper nibble of byte 4)
    fuse_op     : uint4   (lower nibble of byte 4)
    coh_num     : uint16  (2 bytes, big-endian)
    coh_den     : uint16  (2 bytes, big-endian)
    bump        : uint8   (1 byte, LSB is bump flag)

Source: FPGA @ 192.168.1.100 -> broadcast 192.168.1.255:7777
Listen: 0.0.0.0:7777

Usage:
    python ck_fpga_bridge.py
    python ck_fpga_bridge.py --port 7777 --verbose
    python ck_fpga_bridge.py --engine   # Connect to running CK engine

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""

import socket
import struct
import sys
import time
import argparse

# CK operator names (0-9)
OP_NAMES = [
    "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"
]

# T* = 5/7 = 0.714285...
T_STAR = 5.0 / 7.0


def parse_heartbeat(data):
    """Parse 10-byte heartbeat payload from FPGA UDP packet.

    Returns dict with tick_count, phase_bc, fuse_op, coh_num, coh_den,
    bump, coherence (float), above_tstar (bool), op_name, fuse_name.
    """
    if len(data) < 10:
        return None

    tick_count = struct.unpack(">I", data[0:4])[0]
    ops_byte = data[4]
    phase_bc = (ops_byte >> 4) & 0x0F
    fuse_op = ops_byte & 0x0F
    coh_num = struct.unpack(">H", data[5:7])[0]
    coh_den = struct.unpack(">H", data[7:9])[0]
    bump = data[9] & 0x01

    coherence = coh_num / coh_den if coh_den > 0 else 0.0
    above_tstar = coherence >= T_STAR

    return {
        "tick_count": tick_count,
        "phase_bc": phase_bc,
        "fuse_op": fuse_op,
        "coh_num": coh_num,
        "coh_den": coh_den,
        "bump": bump,
        "coherence": coherence,
        "above_tstar": above_tstar,
        "op_name": OP_NAMES[phase_bc] if phase_bc < 10 else f"?{phase_bc}",
        "fuse_name": OP_NAMES[fuse_op] if fuse_op < 10 else f"?{fuse_op}",
    }


def format_heartbeat(hb):
    """Format heartbeat dict as a human-readable string."""
    star = "*" if hb["above_tstar"] else " "
    bump_mark = "!" if hb["bump"] else "."
    return (
        f"tick={hb['tick_count']:>8d}  "
        f"op={hb['op_name']:<9s}  "
        f"fuse={hb['fuse_name']:<9s}  "
        f"coh={hb['coh_num']}/{hb['coh_den']} "
        f"({hb['coherence']:.4f}){star}  "
        f"bump={bump_mark}"
    )


def try_engine_feed(hb, engine_url="http://127.0.0.1:7777"):
    """Attempt to feed heartbeat data to CK engine via HTTP.

    This is optional -- only works if ck_boot_api.py is running.
    Uses a separate endpoint so it doesn't conflict with /chat.
    """
    try:
        import urllib.request
        import json

        payload = json.dumps({
            "source": "fpga",
            "tick_count": hb["tick_count"],
            "phase_bc": hb["phase_bc"],
            "fuse_op": hb["fuse_op"],
            "coh_num": hb["coh_num"],
            "coh_den": hb["coh_den"],
            "bump": hb["bump"],
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{engine_url}/fpga_heartbeat",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        urllib.request.urlopen(req, timeout=0.1)
    except Exception:
        pass  # Engine not running or no /fpga_heartbeat endpoint yet


def main():
    parser = argparse.ArgumentParser(
        description="CK FPGA Heartbeat UDP Bridge"
    )
    parser.add_argument(
        "--port", type=int, default=7777,
        help="UDP port to listen on (default: 7777)"
    )
    parser.add_argument(
        "--bind", type=str, default="0.0.0.0",
        help="Bind address (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Print every heartbeat (default: print every 50th)"
    )
    parser.add_argument(
        "--engine", action="store_true",
        help="Feed heartbeat data to CK engine via HTTP"
    )
    parser.add_argument(
        "--engine-url", type=str, default="http://127.0.0.1:7777",
        help="CK engine API URL (default: http://127.0.0.1:7777)"
    )
    args = parser.parse_args()

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Enable broadcast reception
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    sock.bind((args.bind, args.port))

    print(f"CK FPGA Bridge -- listening on {args.bind}:{args.port}")
    print(f"  T* = {T_STAR:.6f} (5/7)")
    print(f"  Engine feed: {'ON -> ' + args.engine_url if args.engine else 'OFF'}")
    print(f"  Verbose: {'ON' if args.verbose else 'OFF (every 50th tick)'}")
    print("  Waiting for FPGA heartbeat packets...")
    print()

    count = 0
    last_tick = 0
    start_time = time.time()

    try:
        while True:
            data, addr = sock.recvfrom(1500)

            # UDP payload starts after Ethernet(14) + IP(20) + UDP(8) = 42
            # But socket gives us just the UDP payload
            if len(data) < 10:
                continue

            hb = parse_heartbeat(data[:10])
            if hb is None:
                continue

            count += 1

            # Detect missed ticks
            if last_tick > 0 and hb["tick_count"] > last_tick + 1:
                missed = hb["tick_count"] - last_tick - 1
                print(f"  [!] Missed {missed} tick(s)")
            last_tick = hb["tick_count"]

            # Print heartbeat
            if args.verbose or count % 50 == 1:
                elapsed = time.time() - start_time
                rate = count / elapsed if elapsed > 0 else 0
                print(f"[{count:>6d} @ {rate:5.1f}/s]  {format_heartbeat(hb)}")

            # Feed to engine if requested
            if args.engine:
                try_engine_feed(hb, args.engine_url)

    except KeyboardInterrupt:
        elapsed = time.time() - start_time
        print(f"\n\nStopped. Received {count} heartbeats in {elapsed:.1f}s")
        if elapsed > 0:
            print(f"Average rate: {count / elapsed:.1f} Hz")
    finally:
        sock.close()


if __name__ == "__main__":
    main()
