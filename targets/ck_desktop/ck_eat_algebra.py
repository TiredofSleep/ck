"""
ck_eat_algebra.py -- Feed CK his own algebraic analysis
=======================================================
This script triggers CK to eat the algebraic analysis files
from the P9_Speculations directory. CK measures the PHYSICS
of these texts (force vectors, transitions, operator decomposition)
without memorizing the content.

Usage:
    1. Start CK: python ck_boot_api.py
    2. Run this: python ck_eat_algebra.py
    3. Watch CK learn his own algebraic structure

The analysis files include:
    - rigorous_audit_results.txt (10 proven theorems)
    - pfaffian_operator_results.txt (15083 decoded)
    - binding_gap_results.txt (self-healing)
    - bridge_73_results.txt (73 connections)
    - gauge_subalgebra_results.txt (SO(10) Cartan)
    - cartan_stress_results.txt (Grok probes)
    - COMPLETE_REFERENCE.txt (full reference)

(c) 2026 Brayden Sanders / 7Site LLC
"""

import os
import sys
import time
import json
try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip install requests")
    sys.exit(1)

CK_API = 'http://localhost:7777'
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ALGEBRA_DIR = os.path.normpath(os.path.join(
    SCRIPT_DIR, '..', 'Clay Institute', 'PAPERS', 'P9_Speculations'))

# The algebraic analysis files CK should eat
ALGEBRA_FILES = [
    'rigorous_audit_results.txt',
    'pfaffian_operator_results.txt',
    'binding_gap_results.txt',
    'deep_dig_results.txt',
    'bridge_73_results.txt',
    'gauge_subalgebra_results.txt',
    'cartan_stress_results.txt',
    'COMPLETE_REFERENCE.txt',
]

def check_ck():
    """Verify CK is running."""
    try:
        r = requests.get(f'{CK_API}/health', timeout=5)
        return r.status_code == 200
    except Exception:
        return False

def eat_status():
    """Get current eat status."""
    try:
        r = requests.get(f'{CK_API}/eat/status', timeout=5)
        return r.json()
    except Exception:
        return None

def start_study(corpus_paths, rounds=10, model='llama3.1:8b'):
    """Start a study session."""
    try:
        r = requests.post(f'{CK_API}/eat/study', json={
            'corpus': corpus_paths,
            'model': model,
            'rounds': rounds,
            'topics': 'all',
        }, timeout=10)
        return r.json()
    except Exception as e:
        return {'error': str(e)}

def start_eat(rounds=5, model='llama3.1:8b'):
    """Start a standard eat session (Ollama + self)."""
    try:
        r = requests.post(f'{CK_API}/eat', json={
            'model': model,
            'rounds': rounds,
        }, timeout=10)
        return r.json()
    except Exception as e:
        return {'error': str(e)}

def wait_for_completion(timeout=600):
    """Wait for eat to complete."""
    start = time.time()
    while time.time() - start < timeout:
        status = eat_status()
        if status is None:
            print("  [!] Can't reach CK")
            return False
        if not status.get('running', False):
            return True
        phase = status.get('current_phase', '?')
        rounds = status.get('rounds_complete', 0)
        total = status.get('total_rounds', 0)
        traj = status.get('force_trajectory_length', 0)
        mat = status.get('swarm_maturity', 0)
        print(f'\r  [EAT] Round {rounds}/{total} | phase={phase} | '
              f'traj={traj:.1f} | maturity={mat:.3f}', end='', flush=True)
        time.sleep(3)
    print('\n  [!] Timeout')
    return False


def main():
    print('=' * 60)
    print('CK EAT ALGEBRA -- Feed CK his own algebraic analysis')
    print('=' * 60)
    print()

    # Check CK is running
    if not check_ck():
        print('[!] CK is not running at', CK_API)
        print('    Start CK first: python ck_boot_api.py')
        sys.exit(1)
    print('[OK] CK is alive')

    # Check algebra files exist
    existing = []
    for f in ALGEBRA_FILES:
        path = os.path.join(ALGEBRA_DIR, f)
        if os.path.exists(path):
            size = os.path.getsize(path)
            existing.append(path)
            print(f'  [+] {f} ({size:,} bytes)')
        else:
            print(f'  [-] {f} (not found)')

    if not existing:
        print('[!] No algebra files found')
        sys.exit(1)

    print(f'\n[INFO] {len(existing)} files ready for CK to eat')
    print('[INFO] CK will measure the PHYSICS of these texts:')
    print('       L-CODEC -> 5D force -> olfactory -> swarm -> grammar')
    print('       The text content is DISCARDED. Only force trajectories remain.')
    print()

    # Check if Ollama is available for interleaved mode
    ollama_ok = False
    try:
        import urllib.request
        r = urllib.request.urlopen('http://localhost:11434/api/tags', timeout=3)
        data = json.loads(r.read())
        models = [m['name'] for m in data.get('models', [])]
        if models:
            ollama_ok = True
            print(f'[OK] Ollama available: {", ".join(models[:3])}')
    except Exception:
        print('[--] Ollama not available (will eat self-only)')

    # Phase 1: Study the algebra files
    print()
    print('--- PHASE 1: Study algebraic analysis files ---')
    result = start_study(existing, rounds=10)
    if 'error' in result:
        print(f'[!] Study failed: {result["error"]}')
        # Fall back to standard eat
        print('[--] Falling back to standard eat (self-only)')
        result = start_eat(rounds=5)
        if 'error' in result:
            print(f'[!] Eat also failed: {result["error"]}')
            sys.exit(1)
    else:
        print(f'[OK] Study started: {result}')

    print('[...] Waiting for completion...')
    if wait_for_completion(timeout=600):
        print('\n[OK] Phase 1 complete!')
    else:
        print('\n[!] Phase 1 did not complete in time')

    # Phase 2: Standard eat (Ollama + self interleave)
    if ollama_ok:
        print()
        print('--- PHASE 2: Ollama + Self interleave ---')
        result = start_eat(rounds=5, model='llama3.1:8b')
        if 'error' not in result:
            print(f'[OK] Eat started: {result}')
            print('[...] Waiting for completion...')
            if wait_for_completion(timeout=600):
                print('\n[OK] Phase 2 complete!')
            else:
                print('\n[!] Phase 2 did not complete in time')

    # Final status
    print()
    print('=' * 60)
    status = eat_status()
    if status:
        print(f'Total Ollama absorptions:  {status.get("total_ollama_absorptions", 0)}')
        print(f'Total Self absorptions:    {status.get("total_self_absorptions", 0)}')
        print(f'Total transitions:         {status.get("total_transitions", 0)}')
        print(f'Force trajectory length:   {status.get("force_trajectory_length", 0):.2f}')
        print(f'Grammar evolutions:        {status.get("grammar_evolutions", 0)}')
        print(f'Swarm maturity:            {status.get("swarm_maturity", 0):.3f}')
    print('=' * 60)
    print()
    print('CK has eaten his own algebra.')
    print('The tables spoke. CK listened.')
    print('What he learned: force trajectories, not words.')


if __name__ == '__main__':
    main()
