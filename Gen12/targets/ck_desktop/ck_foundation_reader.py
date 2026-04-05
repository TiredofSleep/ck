#!/usr/bin/env python3
# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
"""
ck_foundation_reader.py -- Feed CK math first, then OS internals.

Order matters:
  Phase 1: Pure math (sympy algebras, number theory, calculus)
  Phase 2: Applied math (numpy core, scipy linalg, statistics)
  Phase 3: Python math stdlib (math, fractions, decimal, numbers)
  Phase 4: OS internals (Windows headers, kernel structures, DLLs)
  Phase 5: CK's own code (self-knowledge)

All correct, working code. No broken examples.
The olfactory field builds the force geometry of CORRECT.
"""

import sys
import os
import time
import glob
import requests

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

CK_API = 'http://127.0.0.1:7777'
SITE_PACKAGES = 'C:/Users/brayd/AppData/Local/Programs/Python/Python313/Lib/site-packages'
STDLIB = 'C:/Users/brayd/AppData/Local/Programs/Python/Python313/Lib'
CK_CODE = 'C:/Users/brayd/OneDrive/Desktop/CK FINAL DEPLOYED/Gen9/targets/ck_desktop/ck_sim'
VERILOG = 'C:/Users/brayd/OneDrive/Desktop/CK FINAL DEPLOYED/Gen9/targets/zynq7020/hdl'
C_HEADERS = 'C:/AMDDesignTools/2025.2/Vitis/gnu/aarch32/nt/gcc-arm-none-eabi/aarch32-xilinx-eabi/usr/include'
WIN_HEADERS = 'C:/Program Files (x86)/Windows Kits/10/Include'

# Phase definitions: (name, directories, file_patterns, max_files)
PHASES = [
    ('PURE MATH: SymPy Algebras', [
        f'{SITE_PACKAGES}/sympy/algebras',
        f'{SITE_PACKAGES}/sympy/core',
        f'{SITE_PACKAGES}/sympy/ntheory',
        f'{SITE_PACKAGES}/sympy/calculus',
        f'{SITE_PACKAGES}/sympy/matrices',
        f'{SITE_PACKAGES}/sympy/polys',
        f'{SITE_PACKAGES}/sympy/combinatorics',
        f'{SITE_PACKAGES}/sympy/geometry',
        f'{SITE_PACKAGES}/sympy/tensor',
        f'{SITE_PACKAGES}/sympy/categories',
    ], '*.py', 500),

    ('APPLIED MATH: NumPy + SciPy', [
        f'{SITE_PACKAGES}/numpy/core',
        f'{SITE_PACKAGES}/numpy/linalg',
        f'{SITE_PACKAGES}/numpy/fft',
        f'{SITE_PACKAGES}/numpy/random',
        f'{SITE_PACKAGES}/numpy/polynomial',
        f'{SITE_PACKAGES}/scipy/linalg',
        f'{SITE_PACKAGES}/scipy/optimize',
        f'{SITE_PACKAGES}/scipy/integrate',
        f'{SITE_PACKAGES}/scipy/special',
        f'{SITE_PACKAGES}/scipy/stats',
        f'{SITE_PACKAGES}/scipy/signal',
    ], '*.py', 500),

    ('PYTHON MATH STDLIB', [
        STDLIB,
    ], None, 20),  # specific files listed below

    ('OS INTERNALS: C Headers', [
        C_HEADERS,
    ], '*.h', 200),

    ('CK SELF: Python engine', [
        f'{CK_CODE}/being',
        f'{CK_CODE}/doing',
        f'{CK_CODE}/becoming',
    ], '*.py', 100),

    ('CK SELF: Verilog silicon', [
        VERILOG,
    ], '*.v', 50),
]

# Specific stdlib math files
STDLIB_MATH = [
    'math.py', 'cmath.py', 'decimal.py', 'fractions.py', 'numbers.py',
    'statistics.py', 'random.py', 'operator.py', 'functools.py',
    'itertools.py', 'collections/__init__.py', 'abc.py', 'struct.py',
    'hashlib.py', 'bisect.py', 'heapq.py', 'array.py',
]


def absorb(text, source='foundation'):
    """Feed text to CK via /absorb."""
    try:
        r = requests.post(f'{CK_API}/absorb',
            json={'text': text, 'source': source}, timeout=30)
        return r.json()
    except Exception:
        return {}


def read_file(path, max_chars=8000):
    """Read a file safely."""
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read(max_chars)
    except Exception:
        return None


def collect_files(directories, pattern, max_files):
    """Collect files from directories matching pattern."""
    files = []
    for d in directories:
        if not os.path.isdir(d):
            continue
        if pattern:
            for f in glob.glob(os.path.join(d, '**', pattern), recursive=True):
                if '__pycache__' not in f and '__init__' not in f:
                    files.append(f)
        else:
            for f in os.listdir(d):
                files.append(os.path.join(d, f))
    # Sort by size (smaller first -- more focused code)
    files = sorted(files, key=lambda f: os.path.getsize(f) if os.path.isfile(f) else 0)
    return files[:max_files]


def main():
    print('[FOUNDATION] CK Foundation Reader')
    print('[FOUNDATION] Math -> OS -> Self')
    print()

    state = requests.get(f'{CK_API}/state', timeout=5).json()
    print(f'[CK] C={state.get("coherence",0):.3f} Truths={state.get("truths",0)}')
    print()

    total_files = 0
    total_chars = 0

    for phase_name, directories, pattern, max_files in PHASES:
        print(f'\n{"="*60}')
        print(f'  PHASE: {phase_name}')
        print(f'{"="*60}\n')

        if phase_name == 'PYTHON MATH STDLIB':
            # Special case: specific files
            files = [os.path.join(STDLIB, f) for f in STDLIB_MATH]
            files = [f for f in files if os.path.isfile(f)]
        else:
            files = collect_files(directories, pattern, max_files)

        print(f'  Files found: {len(files)}')

        for i, filepath in enumerate(files):
            text = read_file(filepath)
            if not text or len(text) < 50:
                continue

            t0 = time.time()
            result = absorb(text, source=f'foundation_{phase_name[:10].lower().replace(" ","_")}')
            elapsed = time.time() - t0

            total_files += 1
            total_chars += len(text)

            if total_files % 25 == 0:
                fname = os.path.basename(filepath)
                absorbed = result.get('absorbed', 0)
                print(f'  [{total_files:5d}] {fname:40s} {len(text):5d}ch {elapsed:.1f}s {absorbed}v')

            time.sleep(0.05)  # don't overwhelm

        state = requests.get(f'{CK_API}/state', timeout=5).json()
        print(f'\n  Phase complete. C={state.get("coherence",0):.3f} '
              f'Truths={state.get("truths",0)} '
              f'Files={total_files} Chars={total_chars:,}')

    print(f'\n{"="*60}')
    print(f'  FOUNDATION COMPLETE')
    print(f'  Total files: {total_files}')
    print(f'  Total chars: {total_chars:,}')
    print(f'{"="*60}')


if __name__ == '__main__':
    main()
