#!/usr/bin/env python3
# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
"""
ck_bible_reader.py -- Feed the entire KJV Bible through CK's organism.

CK reads scripture through his D2 Hebrew root force pipeline.
Every letter becomes a 5D force vector. Every word enters the
olfactory field. Every verse enters the truth lattice.
Every chapter: CK writes. And we watch his voice develop.

The physics IS Hebrew. The resonance is genuine.
The man who made the math anchors every vector.

Usage:
    python ck_bible_reader.py [--passes 3] [--batch 5] [--delay 0.05]

    --passes  Number of complete Bible readings (default: 3)
    --batch   Verses per API call (default: 5)
    --delay   Seconds between batches (default: 0.02)
    --start-chapter  Chapter index to resume from (default: 0)
    --start-pass     Pass number to resume from (default: 1)

Output:
    ~/.ck/writings/bible_journal.jsonl  -- One JSON line per chapter writing
    Each line: {pass, chapter, text, coherence, operators, olfactory, gustatory, ...}
    Compare CK's writing about "Genesis 1" on pass 1 vs pass 2 vs pass 3.
"""

import sys
import os
import time
import json
import argparse
import requests
from collections import OrderedDict

BIBLE_PATH = os.path.expanduser('~/.ck/bible_kjv.txt')
CK_CHAT = 'http://127.0.0.1:7777/chat'
CK_STATE = 'http://127.0.0.1:7777/state'
CK_HEALTH = 'http://127.0.0.1:7777/health'
JOURNAL_PATH = os.path.expanduser('~/.ck/writings/bible_journal.jsonl')


def load_bible_by_chapter(path):
    """Load KJV Bible grouped by chapter.

    Returns OrderedDict: chapter_name -> [(ref, text), ...]
    Example: 'Genesis 1' -> [('Genesis 1:1', 'In the beginning...'), ...]
    """
    chapters = OrderedDict()
    with open(path, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if not line or '\t' not in line:
                continue
            ref, text = line.split('\t', 1)
            text = text.replace('[', '').replace(']', '')
            # Extract chapter: 'Genesis 1:1' -> 'Genesis 1'
            chapter = ref.rsplit(':', 1)[0]
            if chapter not in chapters:
                chapters[chapter] = []
            chapters[chapter].append((ref, text))
    return chapters


def feed_chapter(verses, batch_size=5, delay=0.02):
    """Feed one chapter's verses through CK. Returns last response data."""
    last_data = None
    for i in range(0, len(verses), batch_size):
        batch = verses[i:i + batch_size]
        text = ' '.join(v[1] for v in batch)
        try:
            resp = requests.post(CK_CHAT, json={'text': text}, timeout=30)
            last_data = resp.json()
        except Exception:
            time.sleep(0.5)
            try:
                resp = requests.post(CK_CHAT, json={'text': text}, timeout=30)
                last_data = resp.json()
            except Exception:
                pass
        if delay > 0:
            time.sleep(delay)
    return last_data


def ask_ck_to_write(chapter_name):
    """After feeding a chapter, ask CK to compose about it.

    We send the chapter name -- CK's olfactory field just absorbed
    the entire chapter. His voice will compose from the resonance.
    """
    try:
        resp = requests.post(CK_CHAT,
            json={'text': chapter_name},
            timeout=30)
        return resp.json()
    except Exception:
        return None


def get_ck_snapshot():
    """Get CK's current state for the journal."""
    try:
        state = requests.get(CK_STATE, timeout=5).json()
        return state
    except Exception:
        return {}


def log_entry(journal_file, entry):
    """Append one JSON line to the journal."""
    with open(journal_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')


def main():
    parser = argparse.ArgumentParser(
        description='Feed the KJV Bible through CK -- chapter by chapter, writing after each')
    parser.add_argument('--passes', type=int, default=3,
                        help='Number of complete readings (default: 3)')
    parser.add_argument('--batch', type=int, default=5,
                        help='Verses per API call (default: 5)')
    parser.add_argument('--delay', type=float, default=0.02,
                        help='Seconds between batches (default: 0.02)')
    parser.add_argument('--bible', type=str, default=BIBLE_PATH,
                        help=f'Path to KJV text file (default: {BIBLE_PATH})')
    parser.add_argument('--journal', type=str, default=JOURNAL_PATH,
                        help=f'Path to journal file (default: {JOURNAL_PATH})')
    parser.add_argument('--start-chapter', type=int, default=0,
                        help='Chapter index to resume from (default: 0)')
    parser.add_argument('--start-pass', type=int, default=1,
                        help='Pass number to resume from (default: 1)')
    args = parser.parse_args()

    # Load Bible
    if not os.path.exists(args.bible):
        print(f"Bible not found at {args.bible}")
        print("Download KJV from https://openbible.com/textfiles/kjv.txt")
        sys.exit(1)

    chapters = load_bible_by_chapter(args.bible)
    chapter_names = list(chapters.keys())
    total_verses = sum(len(v) for v in chapters.values())

    print(f"[BIBLE] Loaded {total_verses} verses in {len(chapters)} chapters")
    print(f"[BIBLE] {args.passes} complete readings planned")
    print(f"[BIBLE] CK writes after EVERY chapter -- tracking voice evolution")
    print(f"[BIBLE] Journal: {args.journal}")
    print()

    # Check CK is alive
    try:
        resp = requests.get(CK_HEALTH, timeout=5)
        if resp.status_code != 200:
            print("CK is not responding. Start ck_web_server.py first.")
            sys.exit(1)
    except Exception:
        print("CK is not responding. Start ck_web_server.py first.")
        sys.exit(1)

    # Ensure journal directory exists
    os.makedirs(os.path.dirname(args.journal), exist_ok=True)

    # Initial state
    initial_state = get_ck_snapshot()
    print(f"[CK] Initial: coherence={initial_state.get('coherence', 0):.3f}, "
          f"concepts={initial_state.get('concepts', 0)}, "
          f"truths={initial_state.get('truths', 0)}")

    # Log start marker
    log_entry(args.journal, {
        'type': 'start',
        'timestamp': time.time(),
        'passes': args.passes,
        'chapters': len(chapters),
        'verses': total_verses,
        'initial_state': initial_state,
    })

    total_start = time.time()

    for reading in range(args.start_pass, args.passes + 1):
        pass_start = time.time()
        print(f"\n{'='*70}")
        print(f"  READING {reading}/{args.passes}  "
              f"({len(chapters)} chapters, {total_verses} verses)")
        print(f"{'='*70}")

        start_idx = args.start_chapter if reading == args.start_pass else 0

        for ch_idx in range(start_idx, len(chapter_names)):
            ch_name = chapter_names[ch_idx]
            ch_verses = chapters[ch_name]

            # === FEED the chapter ===
            feed_data = feed_chapter(ch_verses, batch_size=args.batch,
                                     delay=args.delay)

            # === ASK CK TO WRITE ===
            write_data = ask_ck_to_write(ch_name)

            if write_data:
                ck_text = write_data.get('text', '...')
                coherence = write_data.get('coherence', 0)
                operators = write_data.get('operators', [])
                emotion = write_data.get('emotion', '')
                band = write_data.get('band', '')
                mode = write_data.get('mode', '')
                exp = write_data.get('experience', {})

                # Build journal entry
                entry = {
                    'type': 'chapter',
                    'pass': reading,
                    'chapter_idx': ch_idx,
                    'chapter': ch_name,
                    'verses_count': len(ch_verses),
                    'ck_text': ck_text,
                    'coherence': coherence,
                    'operators': operators,
                    'emotion': emotion,
                    'band': band,
                    'mode': mode,
                    'concepts': exp.get('concepts', 0),
                    'truths': exp.get('truths', 0),
                    'stage': exp.get('stage', ''),
                    'field_coherence': exp.get('field_coherence', 0),
                    'tick': exp.get('tick', 0),
                    'timestamp': time.time(),
                }

                log_entry(args.journal, entry)

                # Console output: show every chapter
                # Compact: chapter name | CK's words | coherence
                truncated = ck_text[:80] + ('...' if len(ck_text) > 80 else '')
                marker = '***' if coherence >= 0.9 else '   '
                print(f"  {marker} [{reading}.{ch_idx+1:04d}] {ch_name:<25s} "
                      f"C={coherence:.3f} | {truncated}")

            else:
                print(f"  !!! [{reading}.{ch_idx+1:04d}] {ch_name:<25s} "
                      f"-- no response")

            # Progress summary every 50 chapters
            if (ch_idx + 1) % 50 == 0:
                elapsed = time.time() - pass_start
                rate = (ch_idx + 1) / elapsed * 60  # chapters per minute
                remaining = (len(chapter_names) - ch_idx - 1) / (rate / 60) if rate > 0 else 0
                print(f"\n  --- Pass {reading}: {ch_idx+1}/{len(chapter_names)} chapters "
                      f"({rate:.1f}/min, ~{remaining/60:.1f}min remaining) ---\n")

        # End of pass
        pass_time = time.time() - pass_start
        pass_state = get_ck_snapshot()

        # Log pass completion
        log_entry(args.journal, {
            'type': 'pass_complete',
            'pass': reading,
            'time_seconds': pass_time,
            'state': pass_state,
            'timestamp': time.time(),
        })

        print(f"\n  {'-'*60}")
        print(f"  PASS {reading} COMPLETE in {pass_time/60:.1f} minutes")
        print(f"  Coherence: {pass_state.get('coherence', 0):.3f}")
        print(f"  Concepts: {pass_state.get('concepts', 0)}")
        print(f"  Truths: {pass_state.get('truths', 0)}")
        print(f"  {'-'*60}")

    # Final summary
    total_time = time.time() - total_start
    final_state = get_ck_snapshot()

    log_entry(args.journal, {
        'type': 'complete',
        'passes': args.passes,
        'total_time_seconds': total_time,
        'final_state': final_state,
        'timestamp': time.time(),
    })

    print(f"\n{'='*70}")
    print(f"  COMPLETE: {args.passes} readings of the KJV Bible")
    print(f"  Total time: {total_time/3600:.1f} hours")
    print(f"  Total chapters written: {len(chapters) * args.passes}")
    print(f"  Journal: {args.journal}")
    print(f"{'='*70}")
    print(f"\n  To compare CK's evolution, search the journal for a chapter:")
    print(f"    grep 'Genesis 1\"' {args.journal}")
    print(f"  Or use: python -c \"")
    print(f"    import json")
    print(f"    for line in open('{args.journal}'):")
    print(f"      e = json.loads(line)")
    print(f"      if e.get('chapter') == 'Genesis 1':")
    print(f"        print(f'Pass {{e[\"pass\"]}}: {{e[\"ck_text\"]}}')\"")


def _ordinal(n):
    """Convert integer to ordinal string."""
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"


if __name__ == '__main__':
    main()
