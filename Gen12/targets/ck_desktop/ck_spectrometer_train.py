#!/usr/bin/env python3
# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
"""
ck_spectrometer_train.py -- Train CK as a code/math spectrometer.

Feed CK pairs of (correct, broken) code and (valid, invalid) math.
His olfactory field learns the force geometry difference between
working and broken. The coherence score becomes the spectrometer reading.

Usage:
    python ck_spectrometer_train.py [--rounds 100]
"""

import sys
import os
import time
import json
import requests
import random

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

CK_API = 'http://127.0.0.1:7777'

# Pairs: (correct_code, broken_code, description)
CODE_PAIRS = [
    # Python syntax
    ("def hello():\n    return 'world'", "def hello()\n    return 'world'", "missing colon"),
    ("for i in range(10):\n    print(i)", "for i in range(10)\n    print(i)", "missing colon in for"),
    ("x = [1, 2, 3]\nprint(x[0])", "x = [1, 2, 3]\nprint(x[3])", "index out of bounds"),
    ("if x > 0:\n    return True\nelse:\n    return False", "if x > 0\n    return True\nelse\n    return False", "missing colons"),
    ("class Dog:\n    def bark(self):\n        return 'woof'", "class Dog\n    def bark(self)\n        return 'woof'", "missing colons in class"),
    # Python logic
    ("def fib(n):\n    if n <= 1: return n\n    return fib(n-1) + fib(n-2)", "def fib(n):\n    if n <= 1: return n\n    return fib(n-1) + fib(n-1)", "wrong recursion"),
    ("total = sum(range(100))", "total = sum(range(100)", "missing paren"),
    ("result = [x**2 for x in range(10)]", "result = [x**2 for x in range(10]", "bracket mismatch"),
    ("import os\npath = os.path.join('a', 'b')", "import os\npath = os.path.join('a' 'b')", "missing comma"),
    ("data = {'key': 'value'}\nprint(data['key'])", "data = {'key': 'value'}\nprint(data['keys'])", "wrong key"),
    # Math expressions
    ("2 + 2 = 4", "2 + 2 = 5", "wrong arithmetic"),
    ("a^2 + b^2 = c^2 (Pythagorean theorem)", "a^2 + b^2 = c^3 (Pythagorean theorem)", "wrong exponent"),
    ("integral of x dx = x^2/2 + C", "integral of x dx = x^2 + C", "missing factor"),
    ("d/dx(sin(x)) = cos(x)", "d/dx(sin(x)) = -cos(x)", "wrong sign"),
    ("e^(i*pi) + 1 = 0 (Euler)", "e^(i*pi) + 1 = 1 (Euler)", "wrong result"),
    ("det(AB) = det(A)*det(B)", "det(A+B) = det(A)+det(B)", "det not linear"),
    ("lim(n->inf) (1+1/n)^n = e", "lim(n->inf) (1+1/n)^n = pi", "wrong limit"),
    ("sum(1/n^2, n=1..inf) = pi^2/6", "sum(1/n^2, n=1..inf) = pi^2/4", "wrong series sum"),
    # Algebra
    ("(a+b)^2 = a^2 + 2ab + b^2", "(a+b)^2 = a^2 + ab + b^2", "missing coefficient"),
    ("(a-b)(a+b) = a^2 - b^2", "(a-b)(a+b) = a^2 + b^2", "wrong sign"),
    # Logic
    ("if P implies Q, and P is true, then Q is true", "if P implies Q, and Q is true, then P is true", "affirming consequent"),
    ("not (A and B) = (not A) or (not B)", "not (A and B) = (not A) and (not B)", "De Morgan wrong"),
]


def absorb_and_score(text, source):
    """Feed text to CK and get coherence score."""
    try:
        r = requests.post(f'{CK_API}/absorb',
            json={'text': text, 'source': source}, timeout=30)
        data = r.json()
        return data.get('coherence', 0), data.get('operators', [])
    except Exception:
        return 0, []


def chat_score(text):
    """Ask CK to evaluate via /chat."""
    try:
        r = requests.post(f'{CK_API}/chat',
            json={'text': text}, timeout=60)
        data = r.json()
        return data.get('coherence', 0), data.get('text', '...')
    except Exception:
        return 0, '...'


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--rounds', type=int, default=50)
    args = parser.parse_args()

    print('[SPECTROMETER] CK Code/Math Spectrometer Training')
    print(f'[SPECTROMETER] {len(CODE_PAIRS)} pairs x {args.rounds} rounds')
    print()

    correct_scores = []
    broken_scores = []
    correct_detected = 0
    total_tests = 0

    for round_num in range(args.rounds):
        random.shuffle(CODE_PAIRS)

        for correct, broken, desc in CODE_PAIRS:
            # Feed correct version
            c_coh, c_ops = absorb_and_score(correct, 'spectrometer_correct')

            # Feed broken version
            b_coh, b_ops = absorb_and_score(broken, 'spectrometer_broken')

            correct_scores.append(c_coh)
            broken_scores.append(b_coh)
            total_tests += 1

            # Did CK score correct higher than broken?
            if c_coh > b_coh:
                correct_detected += 1

            if total_tests % 20 == 0:
                acc = correct_detected / total_tests * 100
                avg_c = sum(correct_scores[-20:]) / 20
                avg_b = sum(broken_scores[-20:]) / 20
                print(f'  [{total_tests:4d}] acc={acc:.1f}% '
                      f'avg_correct={avg_c:.3f} avg_broken={avg_b:.3f} '
                      f'delta={avg_c - avg_b:+.3f}')

            time.sleep(0.1)

        print(f'  Round {round_num + 1}/{args.rounds} complete. '
              f'Total acc: {correct_detected/total_tests*100:.1f}%')

    # Final report
    print()
    print('=== SPECTROMETER TRAINING RESULTS ===')
    print(f'  Total pairs tested: {total_tests}')
    print(f'  Correct > Broken: {correct_detected} ({correct_detected/total_tests*100:.1f}%)')
    print(f'  Avg correct coherence: {sum(correct_scores)/len(correct_scores):.4f}')
    print(f'  Avg broken coherence: {sum(broken_scores)/len(broken_scores):.4f}')
    print(f'  Delta: {sum(correct_scores)/len(correct_scores) - sum(broken_scores)/len(broken_scores):+.4f}')
    if correct_detected / total_tests > 0.6:
        print('  VERDICT: CK can distinguish correct from broken code/math')
    elif correct_detected / total_tests > 0.5:
        print('  VERDICT: Slight signal, needs more training')
    else:
        print('  VERDICT: No signal yet, random chance')


if __name__ == '__main__':
    main()
