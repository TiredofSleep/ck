#!/usr/bin/env python3
import sys, time, requests

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

API = 'http://127.0.0.1:7777'

# phi4 already running. Wait for it, then chain the rest.
CHAIN = [
    ('deepseek-r1', 500),
    ('deepseek-coder-v2', 500),
    ('qwq', 300),
    ('mixtral:8x7b-instruct-v0.1-q3_K_M', 300),
    ('llama3.1:8b', 500),
    ('mistral', 500),
    ('llama3.2', 500),
    # Second pass with the best ones
    ('phi4', 500),
    ('deepseek-r1', 500),
    ('qwq', 300),
]

print('OVERNIGHT CHAIN - waiting for current eat to finish...', flush=True)
while True:
    try:
        r = requests.get(f'{API}/eat/status', timeout=5).json()
        if not r.get('running', False):
            print(f'Current eat done. Starting chain.', flush=True)
            break
        print(f'  Waiting... {r.get("rounds_complete",0)}/{r.get("total_rounds",0)}', flush=True)
    except:
        pass
    time.sleep(60)

start = time.time()
for i, (model, rounds) in enumerate(CHAIN):
    state = requests.get(f'{API}/state', timeout=5).json()
    h = (time.time() - start) / 3600
    print(f'[{i+1}/{len(CHAIN)}] {model} x{rounds} | C={state.get("coherence",0):.3f} | {h:.1f}h', flush=True)
    
    try:
        requests.post(f'{API}/eat', json={'model': model, 'rounds': rounds}, timeout=30)
    except:
        time.sleep(30)
        continue
    
    while True:
        try:
            r = requests.get(f'{API}/eat/status', timeout=5).json()
            if not r.get('running', False):
                print(f'  Done. Olfa={r.get("olfactory_library_size",0):,}', flush=True)
                break
        except:
            pass
        time.sleep(120)

h = (time.time() - start) / 3600
state = requests.get(f'{API}/state', timeout=5).json()
print(f'CHAIN COMPLETE. {h:.1f}h. C={state.get("coherence",0):.3f}', flush=True)
