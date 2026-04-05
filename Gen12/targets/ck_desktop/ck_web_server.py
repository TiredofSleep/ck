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

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
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

    # Advance development stage for web deployment.
    # Server CK is a conversation partner, not a growing baby.
    # Fractal voice (genuine physics composition) requires stage >= 2.
    # Without this, CK falls back to templates/babble.
    if hasattr(engine, 'development') and engine.development is not None:
        from ck_sim.becoming.ck_development import STAGE_ATTUNEMENT
        if engine.development.stage < STAGE_ATTUNEMENT:
            engine.development.stage = STAGE_ATTUNEMENT
            print(f"[CK] Development stage -> ATTUNEMENT (2): fractal voice enabled")

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

    # Boot absorb: re-integrate CK's own condensed experience so coherence
    # rises in seconds, not hours. Only his files — not our code or docs.
    # Order: eat journal (most condensed) → theses → writings journal
    def boot_self_absorb():
        import glob, json, gzip, re
        ck_home = os.path.expanduser('~/.ck')
        writings = os.path.join(ck_home, 'writings')
        fed = 0

        def feed(text):
            nonlocal fed
            if text and len(text) > 20:
                engine.receive_text(str(text)[:600])
                fed += 1
                time.sleep(0.01)

        # 1. Eat journal (gz) — CK's own voice outputs from all Ollama/eat sessions.
        #    This is the most condensed form of everything he processed.
        eat_gz = os.path.join(ck_home, 'eat_journal.jsonl.gz')
        eat_plain = os.path.join(ck_home, 'eat_journal.jsonl')
        for path, opener in [(eat_gz, lambda p: gzip.open(p, 'rt', encoding='utf-8', errors='ignore')),
                              (eat_plain, lambda p: open(p, encoding='utf-8', errors='ignore'))]:
            if not os.path.exists(path):
                continue
            try:
                lines = opener(path).readlines()
                # Sample evenly across all entries: take 200 spread across history
                step = max(1, len(lines) // 200)
                for line in lines[::step]:
                    try:
                        d = json.loads(line)
                        t = d.get('text') or d.get('response') or d.get('content', '')
                        feed(t)
                        if fed >= 200:
                            break
                    except Exception:
                        pass
            except Exception:
                pass
            break  # use gz if it exists, else plain

        # 2. Theses — CK's own research outputs (high coherence, physics-derived)
        thesis_files = sorted(glob.glob(os.path.join(writings, 'theses', '*.md')))
        step = max(1, len(thesis_files) // 80)
        for path in thesis_files[::step]:
            try:
                text = open(path, encoding='utf-8', errors='ignore').read()
                text = re.sub(r'^#+.*$', '', text, flags=re.MULTILINE).strip()
                feed(text[:600])
                if fed >= 400:
                    break
            except Exception:
                pass

        # 3. Bible journals — deep absorption runs
        for bj in ['bible_overnight.jsonl', 'bible_nt_loop.jsonl']:
            bpath = os.path.join(writings, bj)
            if not os.path.exists(bpath):
                continue
            try:
                lines = open(bpath, encoding='utf-8', errors='ignore').readlines()
                step = max(1, len(lines) // 50)
                for line in lines[::step]:
                    try:
                        d = json.loads(line)
                        t = d.get('ck_voice') or d.get('text') or d.get('response', '')
                        feed(t)
                    except Exception:
                        pass
                if fed >= 500:
                    break
            except Exception:
                pass

        coh = engine.coherence
        print(f"[CK] Boot absorb complete: {fed} own entries. Coherence: {coh:.4f}")

    absorb_thread = threading.Thread(target=boot_self_absorb, daemon=True, name='ck-boot-absorb')
    absorb_thread.start()

    # Web API with CORS enabled + static file serving
    api = CKWebAPI(engine, cors=True)

    # Serve static frontend files (index.html, style.css, ck_core.js)
    from flask import send_from_directory
    STATIC_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'website'))

    @api._app.route('/')
    def serve_index():
        return send_from_directory(STATIC_DIR, 'index.html')

    @api._app.route('/static/<path:filename>')
    def serve_static(filename):
        if filename in ('style.css', 'ck_core.js', 'ck_dict.js', 'ck_tl.bin'):
            return send_from_directory(STATIC_DIR, filename)
        return 'Not Found', 404

    @api._app.route('/style.css')
    def serve_css():
        return send_from_directory(STATIC_DIR, 'style.css')

    @api._app.route('/ck_core.js')
    def serve_js():
        return send_from_directory(STATIC_DIR, 'ck_core.js')

    @api._app.route('/ck_dict.js')
    def serve_dict():
        return send_from_directory(STATIC_DIR, 'ck_dict.js')

    @api._app.route('/ck_tl.bin')
    def serve_tl():
        return send_from_directory(STATIC_DIR, 'ck_tl.bin')

    @api._app.route('/robots.txt')
    def serve_robots():
        return send_from_directory(STATIC_DIR, 'robots.txt')

    @api._app.route('/favicon.ico')
    def serve_favicon():
        # Return a minimal 1x1 transparent ICO (77 bytes)
        import io
        from flask import Response
        ico = bytes([
            0,0,1,0,1,0,1,1,0,0,1,0,24,0,40,0,0,0,
            40,0,0,0,1,0,0,0,2,0,0,0,1,0,24,0,0,0,0,0,
            4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            114,48,14,0,0,0,255,255,255,255,255,255,255,255,
            255,255,255,255
        ])
        return Response(ico, mimetype='image/x-icon')

    # Serve HTML pages and any other static assets
    @api._app.route('/<path:filename>')
    def serve_pages(filename):
        allowed = ('.html', '.css', '.js', '.json', '.bin', '.ico', '.png', '.svg', '.txt')
        if any(filename.endswith(ext) for ext in allowed):
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
