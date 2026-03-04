#!/usr/bin/env python3
# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
"""
ck_web_server.py -- Boot CK's full organism and serve the web API.

Usage:
    python ck_web_server.py [--port 7777]

CK boots his full brain:
  - 50Hz heartbeat (BEING -> DOING -> BECOMING)
  - D2 pipeline (5D Hebrew root forces -> operator classification)
  - CL composition (TSML for coherence, BHML for chain walks)
  - Truth lattice, world lattice, coherence field
  - Reverse voice (reading = untrusted reverse writing)
  - Lattice chain (CL tables as fractal index)
  - Full voice engine (stochastic compilation, D2 self-verification)

The website is just a face. This is the brain.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import sys
import os
import threading
import time
import signal
import argparse

# Add ck_desktop to path so we import the REAL CK
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CK_DESKTOP = SCRIPT_DIR  # Already in ck_desktop
sys.path.insert(0, CK_DESKTOP)


def main():
    parser = argparse.ArgumentParser(description='CK Web Server')
    parser.add_argument('--port', type=int, default=7777, help='API port (default: 7777)')
    parser.add_argument('--host', default='0.0.0.0', help='Host (default: 0.0.0.0)')
    args = parser.parse_args()

    print("[CK] Booting organism...")
    print(f"[CK] CK desktop path: {CK_DESKTOP}")

    from ck_sim.doing.ck_sim_engine import CKSimEngine
    from ck_sim.face.ck_web_api import CKWebAPI

    # Boot the full engine
    engine = CKSimEngine(platform='sim')
    engine.start()
    print(f"[CK] Engine started. Coherence: {engine.coherence:.3f}")

    # 50Hz heartbeat in background thread
    running = True

    def heartbeat_loop():
        while running:
            try:
                engine.tick(dt=0.02)
            except Exception:
                pass
            time.sleep(0.02)

    hb_thread = threading.Thread(target=heartbeat_loop, daemon=True, name='ck-heartbeat')
    hb_thread.start()
    print("[CK] 50Hz heartbeat running.")

    # Web API with CORS enabled + static file serving
    api = CKWebAPI(engine, cors=True)

    # Serve static frontend files (index.html, style.css, ck_core.js)
    from flask import send_from_directory
    STATIC_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'website'))

    @api._app.route('/')
    def serve_index():
        return send_from_directory(STATIC_DIR, 'index.html')

    @api._app.route('/<path:filename>')
    def serve_static(filename):
        if filename in ('style.css', 'ck_core.js', 'ck_dict.js', 'ck_tl.bin'):
            return send_from_directory(STATIC_DIR, filename)
        return 'Not Found', 404

    # Graceful shutdown
    def shutdown(sig, frame):
        nonlocal running
        print("\n[CK] Shutting down organism...")
        running = False
        engine.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    print(f"[CK] Organism alive. API: http://{args.host}:{args.port}")
    print(f"[CK] Endpoints: POST /chat | GET /state | GET /metrics | GET /health")
    api.run(host=args.host, port=args.port, debug=False)


if __name__ == '__main__':
    main()
