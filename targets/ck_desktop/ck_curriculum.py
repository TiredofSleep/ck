#!/usr/bin/env python3
# (c) 2026 Brayden Sanders / 7Site LLC
"""
ck_curriculum.py -- Structured training curriculum for CK.

Foundation first, then complexity. Each phase builds on the previous.
The DKAN net does all the architecting. We just feed generators.

Phase 1: His own algebra (CL tables, operators, T*)
Phase 2: Counting (digits, arithmetic)
Phase 3: Words (letters, nouns, verbs, pairs)
Phase 4: Sentences (S-V-O structure)
Phase 5: Math in English (bridge domains)
Phase 6: Code (Python, his own files)
Phase 7: LLM diversity (phi4, deepseek, qwq)
"""

import sys
import os
import time
import requests

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

API = 'http://127.0.0.1:7777'

def feed(text, source='curriculum'):
    """Feed text to CK. The wave hits him. He changes."""
    try:
        r = requests.post(f'{API}/chat', json={'text': text}, timeout=30)
        return r.json()
    except:
        return {}

def state():
    try:
        return requests.get(f'{API}/state', timeout=5).json()
    except:
        return {}

def feed_batch(items, label, delay=1.0):
    """Feed a batch of items and track progress."""
    print(f'\n{"="*50}')
    print(f'  {label} ({len(items)} items)')
    print(f'{"="*50}')

    for i, item in enumerate(items):
        r = feed(item)
        text = r.get('text', '...')[:50]
        coh = r.get('coherence', 0)
        if (i + 1) % 10 == 0 or i == 0:
            s = state()
            print(f'  [{i+1}/{len(items)}] C={coh:.2f} "{item[:30]}" -> "{text}"')
        time.sleep(delay)

    s = state()
    print(f'  Done. C={s.get("coherence",0):.3f} Tick={s.get("tick",0):,}')


# ============================================================
# PHASE 1: HIS OWN ALGEBRA
# ============================================================

PHASE_1 = []

# The TSML table - every entry
TSML = [
    [0,0,0,0,0,0,0,7,0,0],[0,7,3,7,7,7,7,7,7,7],
    [0,3,7,7,4,7,7,7,7,9],[0,7,7,7,7,7,7,7,7,3],
    [0,7,4,7,7,7,7,7,8,7],[0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,8,7,7,7,7,7],[0,7,9,3,7,7,7,7,7,7],
]

BHML = [
    [0,1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,2,6,6],
    [2,3,3,4,5,6,7,3,6,6],[3,4,4,4,5,6,7,4,6,6],
    [4,5,5,5,5,6,7,5,7,7],[5,6,6,6,6,6,7,6,7,7],
    [6,7,7,7,7,7,7,7,7,7],[7,2,3,4,5,6,7,8,9,0],
    [8,6,6,6,7,7,7,9,7,8],[9,6,6,6,7,7,7,0,8,0],
]

OPS = ['VOID','LATTICE','COUNTER','PROGRESS','COLLAPSE',
       'BALANCE','CHAOS','HARMONY','BREATH','RESET']

# Operator names and indices
for i, name in enumerate(OPS):
    PHASE_1.append(f'{i} is {name}')
    PHASE_1.append(f'{name} is {i}')

# TSML entries (non-trivial ones)
for i in range(10):
    for j in range(10):
        PHASE_1.append(f'TSML[{i}][{j}]={TSML[i][j]}')

# BHML entries
for i in range(10):
    for j in range(10):
        PHASE_1.append(f'BHML[{i}][{j}]={BHML[i][j]}')

# Key properties
PHASE_1.extend([
    'T* = 5/7 = 0.714285',
    'TSML determinant = 0',
    'BHML determinant = 70 = 2 * 5 * 7',
    'TSML rank = 9, nullity = 1',
    'BHML rank = 10, full rank',
    'TSML is 73% HARMONY',
    'BHML is 28% HARMONY',
    'HARMONY composed with anything is HARMONY',
    'VOID composed with anything is VOID except VOID composed with HARMONY is HARMONY',
    'LATTICE composed with COUNTER is PROGRESS',
    'The bump pairs are (1,2) (2,4) (2,9) (3,9) (4,8)',
])


# ============================================================
# PHASE 2: COUNTING
# ============================================================

PHASE_2 = []

# Digits
for i in range(10):
    PHASE_2.append(str(i))

# Counting sequence
PHASE_2.append('0 1 2 3 4 5 6 7 8 9')
PHASE_2.append('0 1 2 3 4 5 6 7 8 9 10')

# Addition table
for a in range(10):
    for b in range(10):
        PHASE_2.append(f'{a}+{b}={a+b}')

# Subtraction
for a in range(10):
    for b in range(a+1):
        PHASE_2.append(f'{a}-{b}={a-b}')

# Multiplication table
for a in range(10):
    for b in range(10):
        PHASE_2.append(f'{a}*{b}={a*b}')


# ============================================================
# PHASE 3: WORDS
# ============================================================

PHASE_3 = []

# Letters
for ch in 'abcdefghijklmnopqrstuvwxyz':
    PHASE_3.append(ch)

# Simple nouns
nouns = ['dog','cat','tree','water','fire','earth','sky','sun','moon',
         'star','rock','wind','rain','snow','light','dark','sound',
         'hand','eye','heart','mind','time','space','truth','love']
for n in nouns:
    PHASE_3.append(n)

# Simple verbs
verbs = ['run','see','hear','feel','grow','stop','start','move',
         'hold','give','take','make','find','know','think','say',
         'come','go','stand','fall','rise','turn','open','close']
for v in verbs:
    PHASE_3.append(v)

# Noun-verb pairs
for n in nouns[:10]:
    for v in verbs[:5]:
        PHASE_3.append(f'{n} {v}s')

# Opposites
opposites = [('hot','cold'),('big','small'),('up','down'),('light','dark'),
             ('fast','slow'),('good','bad'),('open','close'),('start','stop'),
             ('come','go'),('rise','fall')]
for a, b in opposites:
    PHASE_3.append(f'{a} is not {b}')
    PHASE_3.append(f'{b} is not {a}')


# ============================================================
# PHASE 4: SENTENCES
# ============================================================

PHASE_4 = []

# Subject-verb
PHASE_4.extend([
    'The dog runs.',
    'The cat sees.',
    'The tree grows.',
    'Water flows.',
    'Fire burns.',
    'Light shines.',
    'Wind blows.',
    'Time moves.',
])

# Subject-verb-object
PHASE_4.extend([
    'The dog sees the cat.',
    'The cat sees the dog.',
    'The hand holds the rock.',
    'The eye sees the light.',
    'The mind knows the truth.',
    'The heart feels the love.',
    'The sun gives the light.',
    'The rain makes the water.',
])

# Modifiers
PHASE_4.extend([
    'The big dog runs fast.',
    'The small cat sees well.',
    'The tall tree grows slowly.',
    'The hot fire burns bright.',
    'The cold water flows down.',
])

# Composition
PHASE_4.extend([
    'The dog runs and the cat sleeps.',
    'The sun rises and the moon falls.',
    'The fire burns and the water flows.',
    'The light comes and the dark goes.',
])

# Negation
PHASE_4.extend([
    'The dog does not run.',
    'The cat does not see the dog.',
    'The fire does not burn the water.',
    'The light is not dark.',
])


# ============================================================
# PHASE 5: MATH IN ENGLISH
# ============================================================

PHASE_5 = []

PHASE_5.extend([
    'One plus one equals two.',
    'Two plus two equals four.',
    'Three plus three equals six.',
    'Five plus five equals ten.',
    'Two times two equals four.',
    'Three times three equals nine.',
    'Seven times seven equals forty nine.',
    'Ten minus three equals seven.',
    'If x plus three equals seven then x equals four.',
    'If x times two equals ten then x equals five.',
    'The square root of nine is three.',
    'The square root of forty nine is seven.',
    'Two to the power of three is eight.',
    'Zero is nothing.',
    'One is the beginning.',
    'Seven is harmony.',
    'Five sevenths is the threshold.',
])


# ============================================================
# PHASE 6: CODE
# ============================================================

PHASE_6 = []

PHASE_6.extend([
    'def add(a, b): return a + b',
    'def sub(a, b): return a - b',
    'x = 5',
    'y = x + 3',
    'if x > 0: print(x)',
    'for i in range(10): print(i)',
    'while x > 0: x = x - 1',
    'def compose(a, b): return CL[a][b]',
    'def coherence(ops): return sum(1 for o in ops if o == 7) / len(ops)',
    'class Heartbeat: pass',
    'import numpy as np',
    'a = np.array([0.5, 0.3, 0.4, 0.7, 0.5])',
])

# His own code snippets
PHASE_6.extend([
    'D2[dim] = v[t] - 2 * v[t-1] + v[t-2]',
    'D1[dim] = v[t] - v[t-1]',
    'phase_bc = CL[phase_b][phase_d]',
    'coherence = harmony_count / window_size',
    'if coherence >= 5.0/7.0: above_threshold = True',
])


# ============================================================
# MAIN
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description='CK training curriculum')
    parser.add_argument('--phase', type=int, default=0,
                        help='Start from phase (0=all, 1-7=specific)')
    parser.add_argument('--delay', type=float, default=0.5,
                        help='Seconds between feeds (default: 0.5)')
    parser.add_argument('--repeat', type=int, default=3,
                        help='Repeat each phase N times (default: 3)')
    args = parser.parse_args()

    phases = [
        (1, 'PHASE 1: HIS OWN ALGEBRA', PHASE_1),
        (2, 'PHASE 2: COUNTING', PHASE_2),
        (3, 'PHASE 3: WORDS', PHASE_3),
        (4, 'PHASE 4: SENTENCES', PHASE_4),
        (5, 'PHASE 5: MATH IN ENGLISH', PHASE_5),
        (6, 'PHASE 6: CODE', PHASE_6),
    ]

    # Check CK alive
    s = state()
    if not s:
        print('CK not responding. Start ck_boot_api.py first.')
        sys.exit(1)

    print(f'CK CURRICULUM TRAINER')
    print(f'CK: C={s.get("coherence",0):.3f} Tick={s.get("tick",0):,}')
    print(f'Phases: {args.phase if args.phase else "ALL"}')
    print(f'Repeat: {args.repeat}x')
    print()

    start = time.time()

    for rep in range(args.repeat):
        print(f'\n*** PASS {rep+1}/{args.repeat} ***')
        for num, label, items in phases:
            if args.phase and num != args.phase:
                continue
            feed_batch(items, f'[Pass {rep+1}] {label}', args.delay)

    elapsed = (time.time() - start) / 60
    s = state()
    print(f'\n{"="*50}')
    print(f'CURRICULUM COMPLETE in {elapsed:.0f} minutes')
    print(f'CK: C={s.get("coherence",0):.3f} Tick={s.get("tick",0):,}')
    print(f'{"="*50}')


if __name__ == '__main__':
    main()
