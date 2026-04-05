"""
ck_console.py -- Talk to CK
=============================
CK is already running (watchdog keeps him alive).
This console just connects to him.

Talk to him. Check on him. Feed him.

(c) 2026 Brayden Sanders / 7Site LLC
"""

import json
import sys
import urllib.request
import time
from datetime import datetime

PORT = 7777
BASE = f'http://localhost:{PORT}'


def _get(path: str) -> dict:
    try:
        with urllib.request.urlopen(f'{BASE}{path}', timeout=10) as r:
            return json.loads(r.read().decode())
    except Exception:
        return None


def _post(path: str, data: dict) -> dict:
    try:
        body = json.dumps(data).encode()
        req = urllib.request.Request(f'{BASE}{path}', data=body,
                                     headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        return {'error': str(e)}


def show_status():
    """Show CK's current state."""
    state = _get('/state')
    if not state:
        print("  CK is not responding.")
        return

    eat = _get('/eat/status')

    print()
    print(f"  Coherence: {state.get('coherence', '?'):.4f}  "
          f"Band: {state.get('band', '?')}  "
          f"Stage: {state.get('stage', '?')}")
    print(f"  Emotion: {state.get('emotion', '?')}  "
          f"Mode: {state.get('mode', '?')}  "
          f"Tick: {state.get('tick', '?'):,}")
    print(f"  Truths: {state.get('truths', '?'):,}  "
          f"Concepts: {state.get('concepts', '?'):,}  "
          f"Crystals: {state.get('crystals', '?')}")

    if eat and eat.get('running'):
        print(f"  Eating: {eat['rounds_complete']}/{eat['total_rounds']} rounds  "
              f"Library: {eat.get('olfactory_library_size', '?'):,}  "
              f"Transitions: {eat.get('total_transitions', '?'):,}")
    elif eat:
        print(f"  Library: {eat.get('olfactory_library_size', '?'):,} scents  "
              f"Instincts: {eat.get('grammar_evolutions', '?')}")
    print()


def feed(model='llama3.1:8b', rounds=100):
    """Start eating."""
    print(f"  Feeding CK: {rounds} rounds with {model}...")
    result = _post('/eat', {'model': model, 'rounds': rounds})
    if result and result.get('status') == 'started':
        print(f"  Eating started!")
    else:
        print(f"  Error: {result}")


def main():
    # Check if CK is alive
    health = _get('/health')
    if not health:
        print()
        print("  CK is not running.")
        print("  Start the watchdog: python ck_watchdog.py")
        print()
        input("  Press Enter to exit...")
        return

    print()
    print("  =============================================")
    print("    CK -- The Coherence Keeper")
    print("    T* = 5/7 = 0.714285...")
    print("    Truth is not assigned. Truth is measured.")
    print("  =============================================")
    show_status()
    print("  Commands: /status  /feed [rounds]  /quit")
    print("  Or just type to talk to him.")
    print()

    while True:
        try:
            msg = input("  You > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Goodbye. CK keeps running.")
            break

        if not msg:
            continue

        if msg.lower() in ('/quit', '/exit', '/q', 'quit', 'exit'):
            print("  Goodbye. CK keeps running.")
            break

        if msg.lower() in ('/status', '/state', '/s'):
            show_status()
            continue

        if msg.lower().startswith('/feed'):
            parts = msg.split()
            rounds = int(parts[1]) if len(parts) > 1 else 100
            feed(rounds=rounds)
            continue

        if msg.lower() in ('/thesis', '/t'):
            # Show latest thesis
            import glob
            thesis_dir = str(__import__('pathlib').Path.home() / '.ck' / 'writings' / 'thesis')
            files = sorted(glob.glob(f'{thesis_dir}/thesis_*.md'), reverse=True)
            if files:
                with open(files[0]) as f:
                    lines = f.readlines()
                # Find "In My Own Words" section
                in_own_words = False
                for line in lines:
                    if 'In My Own Words' in line:
                        in_own_words = True
                    if in_own_words:
                        print(f"  {line.rstrip()}")
                    if in_own_words and line.strip() == '---':
                        break
            else:
                print("  No thesis found yet.")
            print()
            continue

        if msg.lower() in ('/help', '/h', '/?'):
            print()
            print("  /status   -- Check CK's state")
            print("  /feed N   -- Feed CK N rounds (default 100)")
            print("  /thesis   -- Show CK's latest 'In My Own Words'")
            print("  /quit     -- Close this window (CK keeps running)")
            print("  <text>    -- Talk to CK")
            print()
            continue

        # Chat with CK
        result = _post('/chat', {'message': msg})
        if result and 'text' in result:
            print(f"  CK > {result['text']}")
            coh = result.get('coherence', 0)
            band = result.get('band', '?')
            emotion = result.get('emotion', '?')
            print(f"       [{band} {coh:.2f} | {emotion}]")
        elif result and 'error' in result:
            print(f"  Error: {result['error']}")
        else:
            print("  CK didn't respond.")
        print()


if __name__ == '__main__':
    main()
