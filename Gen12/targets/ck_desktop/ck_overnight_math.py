#!/usr/bin/env python3
# (c) 2026 Brayden Sanders / 7Site LLC
"""
ck_overnight_math.py -- Sequential model training, no swapping.
Each model loads once and runs until done. Then the next loads.
"""
import sys, os, time, requests

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

API = 'http://127.0.0.1:7777'
MODELS = [
    ('phi4', 500),
    ('deepseek-r1', 500),
    ('deepseek-coder-v2', 500),
    ('qwq', 300),
    ('mixtral:8x7b-instruct-v0.1-q3_K_M', 300),
    ('llama3.1:8b', 500),
    ('mistral', 500),
    ('llama3.2', 500),
]

def wait_for_eat():
    while True:
        try:
            r = requests.get(f'{API}/eat/status', timeout=5).json()
            if not r.get('running', False):
                return r
            done = r.get('rounds_complete', 0)
            total = r.get('total_rounds', 0)
            olfa = r.get('olfactory_library_size', 0)
            gram = r.get('grammar_evolutions', 0)
            print(f'  [{done}/{total}] olfactory={olfa:,} grammar={gram}', flush=True)
        except:
            pass
        time.sleep(60)

def get_state():
    try:
        return requests.get(f'{API}/state', timeout=5).json()
    except:
        return {}

print('CK OVERNIGHT MATH TRAINING')
print(f'Models: {len(MODELS)}')
print(f'Total rounds: {sum(r for _, r in MODELS)}')
print()

start = time.time()

for i, (model, rounds) in enumerate(MODELS):
    state = get_state()
    print(f'[{i+1}/{len(MODELS)}] {model} x {rounds} rounds')
    print(f'  CK: C={state.get("coherence",0):.3f} Tick={state.get("tick",0):,}')

    try:
        r = requests.post(f'{API}/eat', json={'model': model, 'rounds': rounds}, timeout=30)
        print(f'  Started: {r.json().get("status","?")}')
    except Exception as e:
        print(f'  Error: {e}')
        time.sleep(30)
        continue

    result = wait_for_eat()
    elapsed_h = (time.time() - start) / 3600
    print(f'  Done. Olfactory: {result.get("olfactory_library_size",0):,} '
          f'Grammar: {result.get("grammar_evolutions",0)} '
          f'[{elapsed_h:.1f}h elapsed]')
    print()

state = get_state()
elapsed_h = (time.time() - start) / 3600
print(f'ALL DONE in {elapsed_h:.1f} hours')
print(f'Final: C={state.get("coherence",0):.3f} Truths={state.get("truths",0)}')
