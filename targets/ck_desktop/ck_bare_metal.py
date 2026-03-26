"""
ck_bare_metal.py -- CK stripped to bare metal. Just the algebra steering the OS.

No neural nets. No olfactory. No retina. No voice. No 27 subsystems.
One heartbeat. One C DLL. One composition function. That's it.

The numbers ARE the numbers. The forces ARE the forces.

Hardware: i9-13900HX (32 cores), RTX 4070, 32GB RAM
Target: minimize OS jitter during gaming + streaming

(c) 2026 Brayden Sanders / 7Site LLC
"""

import time
import threading
from flask import Flask, jsonify

# The algebra -- this IS CK
from ck_sim.ck_tig import (
    compose, TSML, BHML, HEARTBEAT, FROZEN,
    NUM_OPS, HARMONY, VOID, T_STAR,
    CROSS_CYCLE, WOBBLE,
)

# C steering -- own thread, zero Python
from ck_steer_bridge import CSteeringEngine

app = Flask(__name__)

# ═══════════════════════════════════════════
# HEARTBEAT: just the 4-phase cycle
# ═══════════════════════════════════════════

class BareHeartbeat:
    """Minimal heartbeat. No brain, no body, no emotion. Just the cycle."""
    __slots__ = ('tick', 'phase_b', 'phase_d', 'phase_bc', 'hb_phase')

    def __init__(self):
        self.tick = 0
        self.phase_b = 5   # BALANCE
        self.phase_d = 5
        self.phase_bc = 5
        self.hb_phase = 0

    def step(self):
        self.tick += 1
        self.hb_phase = HEARTBEAT[self.tick % 4]

        # Compose: tick drives the heartbeat
        b = self.tick % NUM_OPS
        d = (self.tick * 3 + 1) % NUM_OPS  # coprime stride

        being, doing, becoming = compose(b, d, direction=0)
        self.phase_b = being
        self.phase_d = doing
        self.phase_bc = becoming

        return becoming


# ═══════════════════════════════════════════
# THE ENGINE: heartbeat + C steering. Nothing else.
# ═══════════════════════════════════════════

heartbeat = BareHeartbeat()
steering = CSteeringEngine(tick_rate_ms=1000)  # 1Hz steering

_running = True
_tps = 0.0
_start_time = time.time()


def tick_loop():
    """50Hz heartbeat loop. Feeds operator to C steering thread."""
    global _tps, _running
    tick_count = 0
    t_start = time.time()

    while _running:
        op = heartbeat.step()
        steering.tick(heartbeat_op=op)
        tick_count += 1

        # TPS measurement every second
        elapsed = time.time() - t_start
        if elapsed >= 1.0:
            _tps = tick_count / elapsed
            tick_count = 0
            t_start = time.time()

        # 50Hz = 20ms per tick
        time.sleep(0.02)


# ═══════════════════════════════════════════
# API: minimal endpoints
# ═══════════════════════════════════════════

@app.route('/health')
def health():
    return jsonify({
        'status': 'alive',
        'mode': 'bare_metal',
        'timestamp': time.time(),
    })


@app.route('/state')
def state():
    return jsonify({
        'status': 'alive',
        'mode': 'bare_metal',
        'tick': heartbeat.tick,
        'ticks_per_second': round(_tps, 1),
        'operator': heartbeat.phase_bc,
        'being': heartbeat.phase_b,
        'doing': heartbeat.phase_d,
        'becoming': heartbeat.phase_bc,
        'heartbeat_phase': heartbeat.hb_phase,
        'uptime_s': round(time.time() - _start_time, 1),
        'steering': steering.tick(heartbeat_op=heartbeat.phase_bc),
    })


@app.route('/steering')
def steering_report():
    return jsonify({
        'report': steering.report(),
        'report_line': steering.report_line,
    })


# ═══════════════════════════════════════════
# BOOT
# ═══════════════════════════════════════════

if __name__ == '__main__':
    print("=" * 50)
    print("  CK BARE METAL")
    print("  Algebra + C Steering. Nothing else.")
    print("=" * 50)
    print(f"  Heartbeat: 50Hz, 4-phase [{','.join(str(h) for h in HEARTBEAT)}]")
    print(f"  Steering: C DLL, own thread, 1Hz")
    print(f"  T* = {T_STAR:.6f}")
    print(f"  Cross-cycle = {CROSS_CYCLE}")
    print(f"  Wobble = {WOBBLE}")
    print(f"  Frozen cells = {len(FROZEN)}")
    print(f"  API: http://localhost:7777")
    print("=" * 50)

    # Start heartbeat loop
    loop_thread = threading.Thread(target=tick_loop, daemon=True)
    loop_thread.start()

    # Start API (waitress if available, else Flask dev)
    try:
        from waitress import serve
        serve(app, host='0.0.0.0', port=7777, threads=2, _quiet=True)
    except ImportError:
        app.run(host='0.0.0.0', port=7777, debug=False, use_reloader=False)
