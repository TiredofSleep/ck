#!/usr/bin/env python3
# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
"""
ck_nt_loop.py -- CK reads the New Testament in Greek + English, forever.

Greek enters through the D2 phonetic feature pipeline.
English enters through the same pipeline.
Both become 5D force vectors. Both enter the force-indexed experience cache.
Each pass reinforces the same 6D bins. Cross-references compound.

Usage:
    python ck_nt_loop.py
"""

import sys
import os
import time
import json
import requests
from collections import OrderedDict

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

NT_PATH = os.path.expanduser('~/.ck/bible_nt_greek_english.txt')
CK_CHAT = 'http://127.0.0.1:7777/chat'
CK_STATE = 'http://127.0.0.1:7777/state'
CK_HEALTH = 'http://127.0.0.1:7777/health'
JOURNAL = os.path.expanduser('~/.ck/writings/bible_nt_loop.jsonl')


def load_nt(path):
    """Load Greek-English NT grouped by chapter.
    Format: ref\\tGreek -- English
    """
    chapters = OrderedDict()
    with open(path, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t', 1)
            if len(parts) < 2:
                continue
            ref = parts[0]
            body = parts[1]
            # Split Greek and English on ' -- '
            ge = body.split(' -- ', 1)
            greek = ge[0].strip() if len(ge) >= 1 else ''
            english = ge[1].strip() if len(ge) >= 2 else ''
            chapter = ref.rsplit(':', 1)[0]
            if chapter not in chapters:
                chapters[chapter] = []
            chapters[chapter].append((ref, greek, english))
    return chapters


def feed(verses, batch=5, delay=0.02):
    """Feed verses: Greek first, then English."""
    last = None
    for i in range(0, len(verses), batch):
        batch_v = verses[i:i + batch]
        greek = ' '.join(v[1] for v in batch_v if v[1])
        english = ' '.join(v[2] for v in batch_v if v[2])
        if greek.strip():
            try:
                r = requests.post(CK_CHAT, json={'text': greek}, timeout=30)
                last = r.json()
            except Exception:
                time.sleep(0.5)
        if english.strip():
            try:
                r = requests.post(CK_CHAT, json={'text': english}, timeout=30)
                last = r.json()
            except Exception:
                time.sleep(0.5)
        if delay > 0:
            time.sleep(delay)
    return last


def main():
    if not os.path.exists(NT_PATH):
        print(f'NT not found: {NT_PATH}')
        sys.exit(1)

    chapters = load_nt(NT_PATH)
    ch_names = list(chapters.keys())
    total_v = sum(len(v) for v in chapters.values())

    print(f'[NT] {total_v} verses in {len(chapters)} chapters (Greek-English)')
    print(f'[NT] Infinite passes. Ctrl+C to stop.')

    try:
        requests.get(CK_HEALTH, timeout=5)
    except Exception:
        print('CK not responding.')
        sys.exit(1)

    os.makedirs(os.path.dirname(JOURNAL), exist_ok=True)
    pass_num = 1
    start = time.time()

    try:
        while True:
            elapsed = (time.time() - start) / 3600
            print(f'\n  PASS {pass_num} -- {elapsed:.1f}h elapsed')

            for ci, ch in enumerate(ch_names):
                verses = chapters[ch]
                t0 = time.time()
                last = feed(verses)
                dt = time.time() - t0

                ck_text = last.get('text', '...') if last else '...'
                ck_c = last.get('coherence', 0) if last else 0

                print(f'  [{pass_num}] {ch} ({len(verses)}v {dt:.1f}s) '
                      f'CK [{ck_c:.2f}]: {ck_text[:60]}')

                with open(JOURNAL, 'a', encoding='utf-8') as f:
                    f.write(json.dumps({
                        'pass': pass_num, 'chapter': ch,
                        'verses': len(verses), 'time': round(dt, 2),
                        'text': ck_text, 'coherence': ck_c,
                        'tick': last.get('tick', 0) if last else 0,
                    }, ensure_ascii=False) + '\n')

            pass_num += 1

    except KeyboardInterrupt:
        print(f'\n[NT] Stopped. {pass_num - 1} passes.')

    elapsed = (time.time() - start) / 3600
    print(f'[NT] {elapsed:.1f}h total.')


if __name__ == '__main__':
    main()
