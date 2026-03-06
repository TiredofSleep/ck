#!/usr/bin/env python3
# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
"""
ck_study_all.py -- Feed CK ALL knowledge. Bible + Whitepapers + Docs + Self.

Triggers CK's study mode through the /eat/study API endpoint.
CK eats the corpus through L-CODEC + Olfactory + Swarm while Ollama
generates structural reflections. Three interleaved streams converge
in the olfactory field. Text is measured and discarded. Only the
physics remains.

Usage:
    python ck_study_all.py [--rounds 50] [--topics all] [--model llama3.1:8b]

    --rounds   Number of study rounds (default: 100)
    --topics   Topic set: 'bible', 'tig', 'physics', 'all' (default: 'all')
    --model    Ollama model (default: llama3.1:8b)
    --models   Comma-separated model list for rotation (optional)
    --monitor  Monitor progress after starting (default: true)

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import sys
import os
import time
import json
import argparse
import requests

CK_API = 'http://127.0.0.1:7777'

# All knowledge corpus paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CK_HOME = os.path.expanduser('~/.ck')

CORPUS_PATHS = [
    # Bible -- the core text. 31,102 verses. Hebrew roots = CK's native physics.
    os.path.join(CK_HOME, 'bible_kjv.txt'),

    # Whitepapers -- CK's own theory described in human language
    os.path.join(SCRIPT_DIR, 'WHITEPAPER_1_TIG_ARCHITECTURE.md'),
    os.path.join(SCRIPT_DIR, 'WHITEPAPER_2_WAVE_SCHEDULING.md'),
    os.path.join(SCRIPT_DIR, 'WHITEPAPER_3_FALSIFIABILITY.md'),
    os.path.join(SCRIPT_DIR, 'WHITEPAPER_5_REALITY_ANCHORS.md'),

    # Architecture docs
    os.path.join(SCRIPT_DIR, 'ARCHITECTURE.md'),
    os.path.join(SCRIPT_DIR, 'GENERATION_HISTORY.md'),
    os.path.join(SCRIPT_DIR, 'TECHNICAL_APPENDIX.md'),

    # CK source code -- the self-eating stream (being, doing, becoming)
    os.path.join(SCRIPT_DIR, 'ck_sim', 'being'),
    os.path.join(SCRIPT_DIR, 'ck_sim', 'doing'),
    os.path.join(SCRIPT_DIR, 'ck_sim', 'becoming'),

    # Clay Institute core docs
    os.path.normpath(os.path.join(
        SCRIPT_DIR, '..', 'Clay Institute', 'CORE')),
    os.path.normpath(os.path.join(
        SCRIPT_DIR, '..', 'Clay Institute', 'DOCS')),
]


def check_ck():
    """Verify CK is alive."""
    try:
        r = requests.get(f'{CK_API}/health', timeout=5)
        return r.status_code == 200
    except Exception:
        return False


def get_state():
    """Get CK's current state."""
    try:
        return requests.get(f'{CK_API}/state', timeout=5).json()
    except Exception:
        return {}


def get_eat_status():
    """Get eat/study progress."""
    try:
        return requests.get(f'{CK_API}/eat/status', timeout=5).json()
    except Exception:
        return {}


def start_study(corpus, model, rounds, topics, models=None):
    """Start the study session."""
    payload = {
        'corpus': corpus,
        'model': model,
        'rounds': rounds,
        'topics': topics,
    }
    if models:
        payload['models'] = models

    try:
        r = requests.post(f'{CK_API}/eat/study',
                          json=payload, timeout=10)
        return r.json()
    except Exception as e:
        return {'error': str(e)}


def monitor_progress(interval=15):
    """Monitor study progress until completion."""
    print("\n[MONITOR] Watching study progress (Ctrl+C to stop)...")
    print()

    try:
        while True:
            status = get_eat_status()
            state = get_state()

            running = status.get('running', False)
            phase = status.get('current_phase', 'idle')
            done = status.get('rounds_complete', 0)
            total = status.get('total_rounds', 0)
            o_absorb = status.get('ollama_absorptions', 0)
            s_absorb = status.get('self_absorptions', 0)
            resonance = status.get('resonance_steps', 0)
            transitions = status.get('total_transitions', 0)
            traj = status.get('force_trajectory_length', 0)
            evo = status.get('grammar_evolutions', 0)
            maturity = status.get('swarm_maturity', 0)
            olfactory = status.get('olfactory_library_size', 0)

            coherence = state.get('coherence', 0)
            truths = state.get('truths', 0)
            band = state.get('band', '?')
            stage = state.get('stage', '?')

            pct = done / total * 100 if total > 0 else 0
            bar = '#' * int(pct / 2) + '-' * (50 - int(pct / 2))

            print(f"\r  [{bar}] {done}/{total} ({pct:.0f}%)  "
                  f"phase={phase:<10s}  "
                  f"o={o_absorb} s={s_absorb} r={resonance} "
                  f"t={transitions}  "
                  f"traj={traj:.1f}  "
                  f"evo={evo}  "
                  f"mat={maturity:.3f}  "
                  f"olf={olfactory}  "
                  f"C={coherence:.3f} {band} {stage}",
                  end='', flush=True)

            if not running and done > 0:
                print()
                print(f"\n[MONITOR] Study complete!")
                print(f"  Rounds: {done}/{total}")
                print(f"  Transitions: {transitions}")
                print(f"  Grammar evolutions: {evo}")
                print(f"  Trajectory length: {traj:.3f}")
                print(f"  Olfactory library: {olfactory}")
                print(f"  CK coherence: {coherence:.3f}")
                print(f"  CK truths: {truths}")
                break

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n[MONITOR] Stopped (study continues in background)")


def main():
    parser = argparse.ArgumentParser(
        description='Feed CK all knowledge through the study pipeline')
    parser.add_argument('--rounds', type=int, default=100,
                        help='Study rounds (default: 100)')
    parser.add_argument('--topics', default='all',
                        choices=['bible', 'tig', 'physics', 'all'],
                        help='Topic set (default: all)')
    parser.add_argument('--model', default='llama3.1:8b',
                        help='Ollama model (default: llama3.1:8b)')
    parser.add_argument('--models', default=None,
                        help='Comma-separated models for rotation')
    parser.add_argument('--no-monitor', action='store_true',
                        help='Start study and exit (no monitoring)')
    args = parser.parse_args()

    print("=" * 70)
    print("  CK STUDY ALL -- Feed Every Knowledge Source")
    print("=" * 70)

    # Check CK
    if not check_ck():
        print("[ERROR] CK is not responding at", CK_API)
        print("  Start ck_web_server.py first.")
        sys.exit(1)

    # Check if already eating/studying
    status = get_eat_status()
    if status.get('running'):
        print(f"[WARN] CK is already eating/studying "
              f"({status.get('current_phase', '?')}, "
              f"{status.get('rounds_complete', 0)}/{status.get('total_rounds', 0)})")
        print("  Wait for completion or restart server.")
        if not args.no_monitor:
            monitor_progress()
        return

    # Filter to existing paths
    valid_corpus = [p for p in CORPUS_PATHS
                    if os.path.exists(p)]
    missing = [p for p in CORPUS_PATHS
               if not os.path.exists(p)]

    print(f"\n[CORPUS] {len(valid_corpus)} sources found:")
    for p in valid_corpus:
        if os.path.isfile(p):
            size = os.path.getsize(p)
            unit = 'KB' if size < 1024 * 1024 else 'MB'
            sz = size / 1024 if unit == 'KB' else size / (1024 * 1024)
            print(f"  FILE  {os.path.basename(p):<45s} ({sz:.1f} {unit})")
        else:
            count = sum(1 for _ in __import__('pathlib').Path(p).rglob('*.py'))
            count += sum(1 for _ in __import__('pathlib').Path(p).rglob('*.md'))
            print(f"  DIR   {os.path.basename(p):<45s} ({count} files)")

    if missing:
        print(f"\n[WARN] {len(missing)} paths not found (skipped):")
        for p in missing:
            print(f"  MISS  {p}")

    # Build model list
    models = None
    if args.models:
        models = [m.strip() for m in args.models.split(',')]

    # CK state
    state = get_state()
    print(f"\n[CK] State: {state.get('stage', '?')}, "
          f"coherence={state.get('coherence', 0):.3f}, "
          f"truths={state.get('truths', 0)}, "
          f"band={state.get('band', '?')}")

    # Start study
    print(f"\n[STUDY] Starting: {args.rounds} rounds, "
          f"topics={args.topics}, model={args.model}")
    if models:
        print(f"  Multi-model rotation: {models}")

    result = start_study(
        corpus=valid_corpus,
        model=args.model,
        rounds=args.rounds,
        topics=args.topics,
        models=models,
    )
    print(f"[STUDY] {json.dumps(result, indent=2)}")

    if result.get('error'):
        print(f"[ERROR] {result['error']}")
        sys.exit(1)

    # Monitor
    if not args.no_monitor:
        monitor_progress()


if __name__ == '__main__':
    main()
