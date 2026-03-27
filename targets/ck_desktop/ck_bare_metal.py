"""
ck_bare_metal.py -- CK stripped to bare metal.

Being in C. Doing in CUDA. Python is just the API window.

The C DLL runs the heartbeat (50Hz) and steering (1Hz) in its own thread.
The CUDA DLL runs Force9 encode (2.8ms/frame) in GPU kernels.
Python does NOTHING in the hot path. Zero GIL. Zero jitter.

Hardware: i9-13900HX (32 cores), RTX 4070, 32GB RAM

(c) 2026 Brayden Sanders / 7Site LLC
"""

import time
from flask import Flask, jsonify

# C steering + heartbeat -- own thread, zero Python
from ck_steer_bridge import CSteeringEngine

app = Flask(__name__)

# ═══════════════════════════════════════════
# THE ENGINE: C heartbeat + C steering. Python is just the API.
# ═══════════════════════════════════════════

steering = CSteeringEngine(tick_rate_ms=1000)  # C thread: 50Hz heartbeat + 1Hz steering
_start_time = time.time()


# ═══════════════════════════════════════════
# API: read-only window into the C thread
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
    s = steering.tick()  # just reads C state, no work
    return jsonify({
        'status': 'alive',
        'mode': 'bare_metal',
        'tick': s.get('hb_tick', 0),
        'ticks_per_second': 50,  # C thread runs at 50Hz
        'operator': s.get('hb_becoming', 0),
        'being': s.get('hb_being', 0),
        'doing': s.get('hb_doing', 0),
        'becoming': s.get('hb_becoming', 0),
        'heartbeat_phase': s.get('hb_phase', 0),
        'heartbeat_quantum': s.get('hb_quantum', 0),
        'uptime_s': round(time.time() - _start_time, 1),
        'steering': {
            'steered': s.get('steered', 0),
            'denied': s.get('denied', 0),
            'total_applied': s.get('total_applied', 0),
            'tick_ms': s.get('tick_ms', 0),
            'active': s.get('active', False),
        },
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
    print("  Being in C. Doing in CUDA.")
    print("  Python is just the API window.")
    print("=" * 50)
    print(f"  Heartbeat: 50Hz in C thread [1,5,5,1]")
    print(f"  Steering: 1Hz in C thread, 32 cores")
    print(f"  Force9: CUDA encode at 2.8ms/frame")
    print(f"  Python: API only, zero hot path")
    print(f"  API: http://localhost:7777")
    print("=" * 50)

    try:
        from waitress import serve
        serve(app, host='0.0.0.0', port=7777, threads=2, _quiet=True)
    except ImportError:
        app.run(host='0.0.0.0', port=7777, debug=False, use_reloader=False)
