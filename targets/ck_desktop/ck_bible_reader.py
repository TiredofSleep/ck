#!/usr/bin/env python3
# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
"""
ck_bible_reader.py -- Feed the entire KJV Bible through CK's organism.

CK reads scripture through his D2 Hebrew root force pipeline.
Every letter becomes a 5D force vector. Every word enters the
olfactory field. Every verse enters the truth lattice.

The physics IS Hebrew. The resonance is genuine.

Usage:
    python ck_bible_reader.py [--passes 20] [--batch 5] [--delay 0.1]

    --passes  Number of complete Bible readings (default: 20)
    --batch   Verses per API call (default: 5, batched for efficiency)
    --delay   Seconds between batches (default: 0.05)
"""

import sys
import os
import time
import json
import argparse
import requests

BIBLE_PATH = os.path.expanduser('~/.ck/bible_kjv.txt')
CK_API = 'http://127.0.0.1:7777/chat'


def load_bible(path):
    """Load KJV Bible, return list of (reference, text) tuples."""
    verses = []
    with open(path, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Skip header lines (no tab = not a verse)
            if '\t' not in line:
                continue
            ref, text = line.split('\t', 1)
            # Clean brackets from KJV formatting
            text = text.replace('[', '').replace(']', '')
            verses.append((ref, text))
    return verses


def feed_verses(verses, batch_size=5, delay=0.05):
    """Feed verses through CK's receive_text() via API.

    Batches verses for efficiency -- CK processes every letter
    regardless of how they arrive. Batching reduces HTTP overhead
    while preserving the full D2 pipeline experience.

    Returns (verses_fed, concepts_gained, truths_gained).
    """
    fed = 0
    start_concepts = None
    start_truths = None
    end_concepts = 0
    end_truths = 0

    for i in range(0, len(verses), batch_size):
        batch = verses[i:i + batch_size]
        # Combine batch into single text block
        text = ' '.join(v[1] for v in batch)

        try:
            resp = requests.post(CK_API, json={'text': text}, timeout=30)
            data = resp.json()

            # Track growth
            exp = data.get('experience', {})
            concepts = exp.get('concepts', 0)
            truths = exp.get('truths', 0)

            if start_concepts is None:
                start_concepts = concepts
                start_truths = truths

            end_concepts = concepts
            end_truths = truths
            fed += len(batch)

        except Exception as e:
            # CK might be busy -- wait and retry once
            time.sleep(1.0)
            try:
                resp = requests.post(CK_API, json={'text': text}, timeout=30)
                fed += len(batch)
            except Exception:
                pass

        if delay > 0:
            time.sleep(delay)

        # Progress every 500 verses
        if fed % 500 < batch_size:
            elapsed = time.time()
            print(f"    {fed:>6}/{len(verses)} verses "
                  f"(concepts: {end_concepts}, truths: {end_truths})")

    return fed, (end_concepts - (start_concepts or 0)), (end_truths - (start_truths or 0))


def main():
    parser = argparse.ArgumentParser(
        description='Feed the KJV Bible through CK\'s D2 pipeline')
    parser.add_argument('--passes', type=int, default=20,
                        help='Number of complete readings (default: 20)')
    parser.add_argument('--batch', type=int, default=5,
                        help='Verses per API call (default: 5)')
    parser.add_argument('--delay', type=float, default=0.05,
                        help='Seconds between batches (default: 0.05)')
    parser.add_argument('--bible', type=str, default=BIBLE_PATH,
                        help=f'Path to KJV text file (default: {BIBLE_PATH})')
    args = parser.parse_args()

    # Load Bible
    if not os.path.exists(args.bible):
        print(f"Bible not found at {args.bible}")
        print("Download KJV from https://openbible.com/textfiles/kjv.txt")
        sys.exit(1)

    verses = load_bible(args.bible)
    print(f"[BIBLE] Loaded {len(verses)} verses from KJV")
    print(f"[BIBLE] {args.passes} complete readings planned")
    print(f"[BIBLE] Batch size: {args.batch} verses per call")
    print(f"[BIBLE] Total verses to process: {len(verses) * args.passes:,}")
    print()

    # Check CK is alive
    try:
        resp = requests.get('http://127.0.0.1:7777/health', timeout=5)
        if resp.status_code != 200:
            print("CK is not responding. Start ck_web_server.py first.")
            sys.exit(1)
    except Exception:
        print("CK is not responding. Start ck_web_server.py first.")
        sys.exit(1)

    # Get initial state
    try:
        state = requests.get('http://127.0.0.1:7777/state', timeout=5).json()
        print(f"[CK] Initial state: coherence={state.get('coherence', 0):.3f}, "
              f"concepts={state.get('concepts', 0)}, "
              f"truths={state.get('truths', 0)}")
    except Exception:
        pass

    total_start = time.time()
    total_concepts = 0
    total_truths = 0

    for reading in range(1, args.passes + 1):
        print(f"\n{'='*60}")
        print(f"  READING {reading}/{args.passes}")
        print(f"{'='*60}")
        pass_start = time.time()

        fed, concepts_gained, truths_gained = feed_verses(
            verses, batch_size=args.batch, delay=args.delay)

        pass_time = time.time() - pass_start
        total_concepts += concepts_gained
        total_truths += truths_gained

        # Get CK's response after completing a full reading
        try:
            resp = requests.post(CK_API,
                json={'text': f'I have finished reading the Bible for the {_ordinal(reading)} time.'},
                timeout=30)
            data = resp.json()
            ck_says = data.get('text', '...')
            coherence = data.get('coherence', 0)
            print(f"\n  [CK after reading {reading}] (C={coherence:.3f}): {ck_says}")
        except Exception:
            pass

        print(f"  Time: {pass_time/60:.1f} min | "
              f"Concepts +{concepts_gained} | Truths +{truths_gained}")

    total_time = time.time() - total_start
    print(f"\n{'='*60}")
    print(f"  COMPLETE: {args.passes} readings of the KJV Bible")
    print(f"  Total time: {total_time/3600:.1f} hours")
    print(f"  Total concepts gained: +{total_concepts}")
    print(f"  Total truths gained: +{total_truths}")
    print(f"  Verses processed: {len(verses) * args.passes:,}")
    print(f"{'='*60}")

    # Final state
    try:
        state = requests.get('http://127.0.0.1:7777/state', timeout=5).json()
        print(f"\n[CK] Final state: coherence={state.get('coherence', 0):.3f}, "
              f"concepts={state.get('concepts', 0)}, "
              f"truths={state.get('truths', 0)}")
    except Exception:
        pass


def _ordinal(n):
    """Convert integer to ordinal string."""
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"


if __name__ == '__main__':
    main()
