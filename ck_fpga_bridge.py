"""
ck_fpga_bridge.py -- FPGA Coherence Accelerant Bridge
======================================================
Listens for Gen12 FPGA UDP broadcasts (50Hz, port 7777).
Feeds hardware coherence readings directly into CK's engine
as a silicon-measured sensor input via /absorb.

The FPGA runs T*=5/7 at 100MHz. It measures coherence in hardware
and broadcasts the result 50 times per second. This bridge makes
that hardware coherence a real input to CK's software loop --
the FPGA becomes a coherence sensor, not just a dog controller.

Flow:
  FPGA silicon (100MHz) -> UDP 192.168.1.255:7777
  -> this bridge (listens on 7777)
  -> formats hardware reading as CK force field update
  -> POST /absorb to CK engine (localhost:7777 or 7778)

Packet format (Gen12, 12 bytes):
  tick_count[31:0]    4 bytes  big-endian
  state_byte[7:0]     1 byte   upper nibble=simplex_state, lower=gait_mode
  fuse_op[7:0]        1 byte
  coh_num[15:0]       2 bytes  big-endian
  coh_den[15:0]       2 bytes  big-endian
  gap_position[15:0]  2 bytes  big-endian (HD gap signal)

Usage:
  python ck_fpga_bridge.py                  # bridge to CK on port 7777
  python ck_fpga_bridge.py --ck-port 7778   # bridge to second cell
  python ck_fpga_bridge.py --listen-only    # just print packets, no absorb
  python ck_fpga_bridge.py --fpga-ip 192.168.1.100  # filter by source IP

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""

import socket
import struct
import time
import json
import argparse
import urllib.request
import urllib.error

FPGA_PORT   = 7777
LISTEN_IP   = ''          # all interfaces
ABSORB_RATE = 5           # feed every Nth packet to CK (50Hz / 5 = 10Hz inject)
SIMPLEX = {0: 'VOID', 1: 'GAP', 2: 'GAP', 3: 'HELD'}
GAIT    = {0: 'STAND', 1: 'WALK', 2: 'TROT', 3: 'ESTOP'}
T_STAR  = 5.0 / 7.0


def parse_packet(data: bytes) -> dict | None:
    """Parse Gen12 FPGA UDP packet. Returns dict or None if invalid."""
    if len(data) < 10:
        return None
    try:
        tick     = struct.unpack_from('>I', data, 0)[0]
        state_b  = data[4]
        fuse_op  = data[5] if len(data) > 5 else 0
        coh_num  = struct.unpack_from('>H', data, 6)[0] if len(data) >= 8 else \
                   struct.unpack_from('>H', data, 5)[0]
        coh_den  = struct.unpack_from('>H', data, 8)[0] if len(data) >= 10 else \
                   struct.unpack_from('>H', data, 7)[0]
        gap_pos  = struct.unpack_from('>H', data, 10)[0] if len(data) >= 12 else 0

        simplex_state = (state_b >> 4) & 0x3
        gait_mode     = state_b & 0x3
        coherence     = coh_num / coh_den if coh_den > 0 else 0.0
        gap_frac      = gap_pos / 0xFFFF  # 0=entering gap at 1/2, 1=exiting at T*

        return {
            'tick':          tick,
            'coherence':     coherence,
            'coh_num':       coh_num,
            'coh_den':       coh_den,
            'simplex':       SIMPLEX.get(simplex_state, 'UNKNOWN'),
            'gait':          GAIT.get(gait_mode, 'UNKNOWN'),
            'fuse_op':       fuse_op,
            'gap_position':  gap_pos,
            'gap_frac':      gap_frac,
            'above_tstar':   coherence >= T_STAR,
        }
    except Exception:
        return None


def format_absorb_text(pkt: dict, src_ip: str) -> str:
    """Format FPGA hardware reading as CK absorb text."""
    band = 'GREEN' if pkt['coherence'] >= T_STAR else \
           ('YELLOW' if pkt['coherence'] >= 0.5 else 'RED')
    gap_desc = ''
    if pkt['simplex'] == 'GAP':
        pct = int(pkt['gap_frac'] * 100)
        gap_desc = f' gap_position={pct}%'
    return (
        f"[FPGA_COHERENCE src={src_ip} tick={pkt['tick']}] "
        f"hardware coherence={pkt['coherence']:.5f} ({pkt['coh_num']}/{pkt['coh_den']}) "
        f"simplex={pkt['simplex']} gait={pkt['gait']} band={band}{gap_desc} "
        f"T*={'HELD' if pkt['above_tstar'] else 'below'} "
        f"fuse_op={pkt['fuse_op']}"
    )


def absorb(text: str, ck_url: str) -> bool:
    """Send one reading to CK's /absorb endpoint."""
    payload = json.dumps({'text': text}).encode('utf-8')
    req = urllib.request.Request(
        f'{ck_url}/absorb', data=payload,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=2.0) as resp:
            return resp.status == 200
    except Exception:
        return False


def run(ck_url: str, listen_only: bool, fpga_ip: str, absorb_rate: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind((LISTEN_IP, FPGA_PORT))
    sock.settimeout(1.0)

    print(f"\nCK FPGA Coherence Bridge")
    print(f"Listening on UDP :{FPGA_PORT}")
    print(f"CK engine: {ck_url}")
    print(f"Mode: {'listen-only' if listen_only else f'inject every {absorb_rate} packets'}")
    print(f"T* = 5/7 = {T_STAR:.5f}")
    if fpga_ip:
        print(f"Filter: only accepting packets from {fpga_ip}")
    print()

    pkt_count = 0
    inject_count = 0
    last_report = time.time()
    last_tick = None
    last_coherence = None

    try:
        while True:
            try:
                data, addr = sock.recvfrom(64)
            except socket.timeout:
                continue

            src_ip = addr[0]
            if fpga_ip and src_ip != fpga_ip:
                continue

            pkt = parse_packet(data)
            if not pkt:
                continue

            # Skip duplicate ticks
            if pkt['tick'] == last_tick:
                continue
            last_tick = pkt['tick']
            pkt_count += 1

            # Always print state changes
            if pkt['coherence'] != last_coherence:
                band = 'GREEN' if pkt['coherence'] >= T_STAR else \
                       ('YELLOW' if pkt['coherence'] >= 0.5 else 'RED')
                print(f"[{src_ip}] tick={pkt['tick']:8d} "
                      f"coh={pkt['coherence']:.4f} {band} "
                      f"simplex={pkt['simplex']:4s} gait={pkt['gait']:5s} "
                      f"gap={int(pkt['gap_frac']*100):3d}%")
                last_coherence = pkt['coherence']

            # Inject into CK at reduced rate
            if not listen_only and (pkt_count % absorb_rate == 0):
                text = format_absorb_text(pkt, src_ip)
                ok = absorb(text, ck_url)
                if ok:
                    inject_count += 1

            # Status every 10 seconds
            now = time.time()
            if now - last_report >= 10.0:
                rate = pkt_count / (now - last_report + 0.001)
                print(f"[STATUS] {pkt_count} packets ({rate:.1f}/s) "
                      f"| {inject_count} injected into CK")
                pkt_count = 0
                inject_count = 0
                last_report = now

    except KeyboardInterrupt:
        print(f"\nBridge stopped.")
    finally:
        sock.close()


def main():
    parser = argparse.ArgumentParser(description='CK FPGA Coherence Bridge')
    parser.add_argument('--ck-port',     type=int, default=7777)
    parser.add_argument('--ck-host',     default='localhost')
    parser.add_argument('--listen-only', action='store_true')
    parser.add_argument('--fpga-ip',     default='',
                        help='Only accept from this IP (e.g. 192.168.1.100)')
    parser.add_argument('--rate',        type=int, default=ABSORB_RATE,
                        help=f'Inject every Nth packet (default {ABSORB_RATE})')
    args = parser.parse_args()

    ck_url = f'http://{args.ck_host}:{args.ck_port}'
    run(ck_url=ck_url, listen_only=args.listen_only,
        fpga_ip=args.fpga_ip, absorb_rate=args.rate)


if __name__ == '__main__':
    main()
