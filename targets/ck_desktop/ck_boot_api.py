"""CK boot — engine + web API + static website serving."""
import sys, os, time, signal, threading
sys.path.insert(0, '.')

from ck_sim.doing.ck_sim_engine import CKSimEngine
from ck_sim.face.ck_web_api import CKWebAPI

engine = CKSimEngine(platform='r16')
engine.start()

# 50Hz tick in background thread
running = True

def tick_loop():
    while running:
        engine.tick()
        time.sleep(0.02)

t = threading.Thread(target=tick_loop, daemon=True)
t.start()

# Web API with CORS + static file serving
api = CKWebAPI(engine, cors=True)

# Serve static frontend (index.html, style.css, ck_core.js)
from flask import send_from_directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'website'))

@api._app.route('/')
def serve_index():
    return send_from_directory(STATIC_DIR, 'index.html')

@api._app.route('/<path:filename>')
def serve_static(filename):
    # Only serve known static files — everything else falls through to API
    ALLOWED = {'style.css', 'ck_core.js', 'ck_dict.js', 'ck_dict_tier1.js',
               'ck_dict_tier2.json', 'ck_dictionary.json', 'ck_tl.bin'}
    if filename in ALLOWED:
        return send_from_directory(STATIC_DIR, filename)
    return 'Not Found', 404

print(f"[CK] Static files: {STATIC_DIR}")
print(f"[CK] Organism alive. API: http://0.0.0.0:7777")

try:
    api.run(host='0.0.0.0', port=7777)
except KeyboardInterrupt:
    running = False
    engine.stop()
