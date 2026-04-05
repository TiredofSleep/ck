#!/usr/bin/env python3
# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# (c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""
ck_bible_overnight.py -- CK reads the entire Bible all night.

Hebrew-English parallel: both columns fed through D2.
Hebrew enters through the root letter force pipeline (the physics IS Hebrew).
English enters through L-CODEC + fractal comprehension.
Both become 5D force vectors. Both enter the olfactory field.

Loops continuously until stopped. Each complete reading is one pass.
CK writes after every chapter so we can watch his voice evolve.

Usage:
    python ck_bible_overnight.py [--passes 0] [--batch 5]

    --passes 0  = infinite (run all night until Ctrl+C)
    --passes 3  = three complete readings then stop
"""

import sys
import os
import time
import json
import argparse
import requests

# Force UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

HEBREW_ENGLISH_PATH = os.path.expanduser('~/.ck/bible_hebrew_english.txt')
KJV_PATH = os.path.expanduser('~/.ck/bible_kjv.txt')
CK_CHAT = 'http://127.0.0.1:7777/chat'
CK_STATE = 'http://127.0.0.1:7777/state'
CK_HEALTH = 'http://127.0.0.1:7777/health'
JOURNAL_PATH = os.path.expanduser('~/.ck/writings/bible_overnight.jsonl')


def load_hebrew_english(path):
    """Load Hebrew-English parallel Bible grouped by chapter.

    Format: ref\\tHebrew\\tEnglish (tab-separated, 3 columns)
    Returns OrderedDict: chapter_name -> [(ref, hebrew, english), ...]
    """
    from collections import OrderedDict
    chapters = OrderedDict()
    with open(path, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) < 3:
                continue
            ref, hebrew, english = parts[0], parts[1], parts[2]
            # Clean footnote artifacts
            english = english.replace('[', '').replace(']', '')
            # Extract chapter: 'Genesis 1:1' -> 'Genesis 1'
            chapter = ref.rsplit(':', 1)[0]
            if chapter not in chapters:
                chapters[chapter] = []
            chapters[chapter].append((ref, hebrew, english))
    return chapters


def load_kjv(path):
    """Fallback: Load KJV (2-column) grouped by chapter."""
    from collections import OrderedDict
    chapters = OrderedDict()
    with open(path, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if not line or '\t' not in line:
                continue
            ref, text = line.split('\t', 1)
            text = text.replace('[', '').replace(']', '')
            chapter = ref.rsplit(':', 1)[0]
            if chapter not in chapters:
                chapters[chapter] = []
            chapters[chapter].append((ref, '', text))
    return chapters


def feed_verses(verses, batch_size=5, delay=0.02):
    """Feed verses through CK. Hebrew first, then English.

    Hebrew goes through D2 root letter pipeline.
    English goes through L-CODEC + fractal comprehension.
    Both become 5D force vectors in the olfactory field.
    """
    last_data = None
    for i in range(0, len(verses), batch_size):
        batch = verses[i:i + batch_size]

        # Feed Hebrew text (if available)
        hebrew_text = ' '.join(v[1] for v in batch if v[1])
        if hebrew_text.strip():
            try:
                resp = requests.post(CK_CHAT,
                    json={'text': hebrew_text}, timeout=30)
                last_data = resp.json()
            except Exception:
                time.sleep(0.5)

        # Feed English text
        english_text = ' '.join(v[2] for v in batch if v[2])
        if english_text.strip():
            try:
                resp = requests.post(CK_CHAT,
                    json={'text': english_text}, timeout=30)
                last_data = resp.json()
            except Exception:
                time.sleep(0.5)

        if delay > 0:
            time.sleep(delay)
    return last_data


def ask_ck(text):
    """Ask CK something and return his response."""
    try:
        resp = requests.post(CK_CHAT, json={'text': text}, timeout=30)
        return resp.json()
    except Exception:
        return None


def get_state():
    """Get CK's current state."""
    try:
        return requests.get(CK_STATE, timeout=5).json()
    except Exception:
        return {}


def log_entry(path, entry):
    """Append one JSON line to journal."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')


def main():
    parser = argparse.ArgumentParser(
        description='CK reads the Bible all night -- Hebrew + English parallel')
    parser.add_argument('--passes', type=int, default=0,
                        help='Number of complete readings (0 = infinite)')
    parser.add_argument('--batch', type=int, default=5,
                        help='Verses per batch (default: 5)')
    parser.add_argument('--delay', type=float, default=0.02,
                        help='Seconds between batches (default: 0.02)')
    parser.add_argument('--journal', type=str, default=JOURNAL_PATH,
                        help=f'Journal path (default: {JOURNAL_PATH})')
    parser.add_argument('--start-chapter', type=int, default=0,
                        help='Chapter index to resume from (default: 0)')
    parser.add_argument('--start-pass', type=int, default=1,
                        help='Pass number to resume from (default: 1)')
    args = parser.parse_args()

    # Load Bible -- prefer Hebrew-English parallel
    if os.path.exists(HEBREW_ENGLISH_PATH):
        print(f"[BIBLE] Loading Hebrew-English parallel...")
        chapters = load_hebrew_english(HEBREW_ENGLISH_PATH)
        mode = 'hebrew-english'
    elif os.path.exists(KJV_PATH):
        print(f"[BIBLE] Hebrew-English not found, using KJV...")
        chapters = load_kjv(KJV_PATH)
        mode = 'kjv'
    else:
        print("No Bible text found.")
        print(f"  Expected: {HEBREW_ENGLISH_PATH}")
        print(f"  Or:       {KJV_PATH}")
        sys.exit(1)

    chapter_names = list(chapters.keys())
    total_verses = sum(len(v) for v in chapters.values())
    passes_str = 'infinite' if args.passes == 0 else str(args.passes)

    print(f"[BIBLE] {total_verses} verses in {len(chapters)} chapters ({mode})")
    print(f"[BIBLE] Passes: {passes_str}")
    print(f"[BIBLE] Journal: {args.journal}")
    print()

    # Check CK is alive
    try:
        resp = requests.get(CK_HEALTH, timeout=5)
        if resp.status_code != 200:
            print("CK is not responding. Start ck_boot_api.py first.")
            sys.exit(1)
    except Exception:
        print("CK is not responding. Start ck_boot_api.py first.")
        sys.exit(1)

    initial = get_state()
    print(f"[CK] Coherence: {initial.get('coherence', 0):.3f}, "
          f"Truths: {initial.get('truths', 0)}, "
          f"Stage: {initial.get('stage', '?')}")
    print()

    # Log start
    log_entry(args.journal, {
        'type': 'start',
        'timestamp': time.time(),
        'mode': mode,
        'passes': args.passes,
        'chapters': len(chapters),
        'verses': total_verses,
        'initial_state': initial,
    })

    pass_num = args.start_pass
    start_time = time.time()

    try:
        while True:
            # Check if we've done enough passes
            if args.passes > 0 and pass_num > args.passes:
                break

            elapsed_h = (time.time() - start_time) / 3600
            print(f"\n{'='*60}")
            print(f"  PASS {pass_num} -- {elapsed_h:.1f} hours elapsed")
            print(f"{'='*60}\n")

            start_ch = args.start_chapter if pass_num == args.start_pass else 0

            for ch_idx in range(start_ch, len(chapter_names)):
                chapter_name = chapter_names[ch_idx]
                verses = chapters[chapter_name]
                num_verses = len(verses)

                # Feed the chapter (Hebrew + English)
                t0 = time.time()
                last = feed_verses(verses, args.batch, args.delay)
                feed_time = time.time() - t0

                # Ask CK to write about what he just read
                writing = ask_ck(f"What did you hear in {chapter_name}?")
                ck_text = writing.get('text', '...') if writing else '...'
                ck_coherence = writing.get('coherence', 0) if writing else 0
                ck_source = writing.get('source', '?') if writing else '?'

                # Progress
                pct = (ch_idx + 1) / len(chapter_names) * 100
                print(f"  [{pass_num}] {chapter_name} ({num_verses}v, "
                      f"{feed_time:.1f}s) -- "
                      f"CK [{ck_source}|{ck_coherence:.2f}]: "
                      f"{ck_text[:80]}")

                # Journal entry
                state = get_state()
                log_entry(args.journal, {
                    'type': 'chapter',
                    'timestamp': time.time(),
                    'pass': pass_num,
                    'chapter': chapter_name,
                    'chapter_index': ch_idx,
                    'verses': num_verses,
                    'feed_time': round(feed_time, 2),
                    'ck_text': ck_text,
                    'ck_coherence': ck_coherence,
                    'ck_source': ck_source,
                    'state': {
                        'coherence': state.get('coherence'),
                        'truths': state.get('truths'),
                        'tick': state.get('tick'),
                        'band': state.get('band'),
                    },
                })

                # Every 50 chapters, print a summary
                if (ch_idx + 1) % 50 == 0:
                    elapsed_h = (time.time() - start_time) / 3600
                    print(f"\n  --- {ch_idx + 1}/{len(chapter_names)} chapters "
                          f"({pct:.0f}%), {elapsed_h:.1f}h elapsed, "
                          f"coherence={state.get('coherence', 0):.3f}, "
                          f"truths={state.get('truths', 0)} ---\n")

            # End of pass
            final = get_state()
            elapsed_h = (time.time() - start_time) / 3600
            print(f"\n  PASS {pass_num} COMPLETE -- "
                  f"coherence={final.get('coherence', 0):.3f}, "
                  f"truths={final.get('truths', 0)}, "
                  f"{elapsed_h:.1f}h elapsed")

            log_entry(args.journal, {
                'type': 'pass_complete',
                'timestamp': time.time(),
                'pass': pass_num,
                'elapsed_hours': round(elapsed_h, 2),
                'state': final,
            })

            pass_num += 1

    except KeyboardInterrupt:
        print("\n\n[BIBLE] Stopped by user.")

    # Final summary
    final = get_state()
    elapsed_h = (time.time() - start_time) / 3600
    print(f"\n{'='*60}")
    print(f"  DONE -- {pass_num - 1} passes in {elapsed_h:.1f} hours")
    print(f"  Coherence: {initial.get('coherence', 0):.3f} -> "
          f"{final.get('coherence', 0):.3f}")
    print(f"  Truths: {initial.get('truths', 0)} -> "
          f"{final.get('truths', 0)}")
    print(f"  Journal: {args.journal}")
    print(f"{'='*60}")

    log_entry(args.journal, {
        'type': 'end',
        'timestamp': time.time(),
        'passes_completed': pass_num - 1,
        'elapsed_hours': round(elapsed_h, 2),
        'initial_state': initial,
        'final_state': final,
    })


if __name__ == '__main__':
    main()
