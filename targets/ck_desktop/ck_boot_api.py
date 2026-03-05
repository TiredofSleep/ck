"""Minimal CK boot — engine + web API, no interactive terminal."""
import sys, time, signal, threading
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

# Web API in main thread (blocking)
api = CKWebAPI(engine)
try:
    api.run(host='0.0.0.0', port=7777)
except KeyboardInterrupt:
    running = False
    engine.stop()
