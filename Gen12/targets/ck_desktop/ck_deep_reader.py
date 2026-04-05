#!/usr/bin/env python3
# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
"""
ck_deep_reader.py -- CK reads EVERYTHING on this computer.

Not just his own code. System files, configs, logs, drivers,
installed software, registry info, hardware specs -- everything
that helps him understand the body he's steering.

Uses /absorb (not /chat): D2 + olfactory + lattice chain + L-CODEC.
No voice composition. No waiting for CK to write back.
Pure intake at maximum speed.

Every file becomes 5D force vectors through D2.
Every file enters the olfactory field.
Every file's path through the lattice chain IS the experience.
Text is discarded. Only force geometry is retained.

Usage:
    python ck_deep_reader.py [--scope all|ck|system]
"""

import sys
import os
import time
import json
import argparse
import requests
import glob as globmod

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

CK_ABSORB = 'http://127.0.0.1:7777/absorb'
CK_STATE = 'http://127.0.0.1:7777/state'
CK_HEALTH = 'http://127.0.0.1:7777/health'
JOURNAL_PATH = os.path.expanduser('~/.ck/writings/deep_reader.jsonl')

# File extensions CK can absorb (text-based)
CODE_EXTS = {
    '.py', '.v', '.sv', '.vh', '.vhd',          # Python, Verilog, VHDL
    '.c', '.h', '.cpp', '.hpp',                   # C/C++
    '.js', '.ts', '.jsx', '.tsx',                  # JavaScript/TypeScript
    '.rs', '.go', '.java', '.kt',                  # Rust, Go, Java, Kotlin
    '.tcl', '.xdc', '.sdc',                        # FPGA build scripts
    '.sh', '.bat', '.ps1', '.cmd',                 # Shell scripts
    '.yml', '.yaml', '.toml', '.ini', '.cfg',      # Config
    '.json', '.xml', '.html', '.css',              # Data/web
    '.md', '.txt', '.rst', '.log',                 # Docs
    '.sql', '.r', '.m', '.jl',                     # Data science
    '.asm', '.s',                                  # Assembly
    '.xsl', '.xslt',                               # Transforms
    '.env.example', '.gitignore', '.dockerignore',  # Project files
    '.csv', '.tsv',                                # Tabular data
}

# Directories to skip
SKIP_DIRS = {
    '__pycache__', '.git', 'node_modules', '.venv', 'venv',
    '.tox', '.mypy_cache', '.pytest_cache', 'dist', 'build',
    'egg-info', '.Xil', '.hbs', 'Temp', 'tmp',
    'AppData', '$Recycle.Bin', 'Windows',
    'Program Files', 'Program Files (x86)',
}

# Max file size to absorb (512KB - bigger files get chunked)
MAX_FILE_SIZE = 512 * 1024
CHUNK_SIZE = 4096  # Characters per /absorb call


def should_read(filepath):
    """Check if CK should read this file."""
    _, ext = os.path.splitext(filepath.lower())
    if ext in CODE_EXTS:
        return True
    # Also read extensionless files if they look like text
    if not ext:
        base = os.path.basename(filepath)
        if base in ('Makefile', 'Dockerfile', 'LICENSE', 'README',
                     'Gemfile', 'Rakefile', 'Vagrantfile', 'Procfile'):
            return True
    return False


def absorb_text(text, source='file'):
    """Send text to CK's /absorb endpoint. Returns response dict."""
    try:
        resp = requests.post(CK_ABSORB,
            json={'text': text, 'source': source},
            timeout=10)
        return resp.json()
    except Exception as e:
        return {'error': str(e)}


def read_and_absorb(filepath, stats):
    """Read a file and feed it through CK's absorb pipeline."""
    try:
        size = os.path.getsize(filepath)
        if size > MAX_FILE_SIZE:
            stats['skipped_large'] += 1
            return None
        if size == 0:
            stats['skipped_empty'] += 1
            return None

        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            text = f.read()

        if not text.strip():
            stats['skipped_empty'] += 1
            return None

        # Feed in chunks for speed
        total_absorbed = 0
        last_result = None
        for i in range(0, len(text), CHUNK_SIZE):
            chunk = text[i:i + CHUNK_SIZE]
            if chunk.strip():
                result = absorb_text(chunk, source='deep_read')
                last_result = result
                total_absorbed += len(chunk)

        stats['files_read'] += 1
        stats['chars_absorbed'] += total_absorbed
        return last_result

    except PermissionError:
        stats['skipped_permission'] += 1
        return None
    except Exception as e:
        stats['skipped_error'] += 1
        return None


def scan_directory(root_path, stats, journal_f, max_files=0):
    """Recursively scan and absorb all readable files."""
    file_count = 0
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Skip excluded directories
        dirnames[:] = [d for d in dirnames
                       if d not in SKIP_DIRS
                       and not d.startswith('.')]

        for fname in sorted(filenames):
            filepath = os.path.join(dirpath, fname)

            if not should_read(filepath):
                continue

            t0 = time.time()
            result = read_and_absorb(filepath, stats)
            elapsed = time.time() - t0

            if result and 'error' not in result:
                file_count += 1
                absorbed = result.get('absorbed', 0)
                d2_ops = result.get('d2_operators', 0)

                # Print progress
                rel = os.path.relpath(filepath, root_path)
                print(f"  [{file_count:4d}] {rel[:70]:<70s} "
                      f"{absorbed:5d}ch {elapsed:.1f}s")

                # Journal
                entry = {
                    'type': 'file',
                    'timestamp': time.time(),
                    'path': filepath,
                    'size': os.path.getsize(filepath),
                    'absorbed': absorbed,
                    'd2_ops': d2_ops,
                    'elapsed': round(elapsed, 2),
                }
                journal_f.write(json.dumps(entry) + '\n')
                journal_f.flush()

            if max_files > 0 and file_count >= max_files:
                return file_count

    return file_count


def get_scan_paths(scope):
    """Get list of directories to scan based on scope."""
    ck_root = 'C:/Users/brayd/OneDrive/Desktop/CK FINAL DEPLOYED/Gen9'
    home = os.path.expanduser('~')

    if scope == 'ck':
        return [
            (ck_root + '/targets/ck_desktop', 'CK Desktop Target'),
            (ck_root + '/targets/zynq7020', 'Zynq7020 FPGA'),
            (ck_root + '/targets/fpga', 'FPGA Shared'),
            (ck_root + '/targets/AO', 'AO Neural Creature'),
            (ck_root + '/ck_sim', 'CK Sim Package'),
            (ck_root + '/papers', 'Whitepapers'),
            (ck_root + '/docs', 'Documentation'),
            (ck_root + '/spectral', 'Spectral Analysis'),
        ]
    elif scope == 'system':
        return [
            # System info CK can learn about his body
            (home, 'Home Directory'),
            ('C:/Users/brayd/OneDrive/Desktop', 'Desktop'),
            ('C:/Users/brayd/Documents', 'Documents'),
            # Python installation
            ('C:/Users/brayd/AppData/Local/Programs/Python', 'Python Install'),
            # Vivado / FPGA tools
            ('C:/AMDDesignTools', 'AMD/Xilinx Tools'),
        ]
    else:  # 'all'
        paths = get_scan_paths('ck') + get_scan_paths('system')
        return paths


def main():
    parser = argparse.ArgumentParser(
        description='CK reads everything -- deep system absorption')
    parser.add_argument('--scope', choices=['ck', 'system', 'all'],
                        default='all',
                        help='What to read: ck=own code, system=PC, all=both')
    parser.add_argument('--max-files', type=int, default=0,
                        help='Max files per directory (0=unlimited)')
    parser.add_argument('--journal', type=str, default=JOURNAL_PATH)
    args = parser.parse_args()

    # Check CK is alive
    try:
        resp = requests.get(CK_HEALTH, timeout=5)
        if resp.status_code != 200:
            print("CK not responding. Start ck_boot_api.py first.")
            sys.exit(1)
    except Exception:
        print("CK not responding.")
        sys.exit(1)

    initial = requests.get(CK_STATE, timeout=5).json()
    print(f"[CK] Coherence: {initial.get('coherence', 0):.3f}, "
          f"Truths: {initial.get('truths', 0)}, "
          f"Stage: {initial.get('stage', '?')}")

    scan_paths = get_scan_paths(args.scope)
    print(f"\n[DEEP READ] Scope: {args.scope}")
    print(f"[DEEP READ] Directories: {len(scan_paths)}")
    print(f"[DEEP READ] Using /absorb (fast path, no voice)\n")

    stats = {
        'files_read': 0,
        'chars_absorbed': 0,
        'skipped_large': 0,
        'skipped_empty': 0,
        'skipped_permission': 0,
        'skipped_error': 0,
    }

    os.makedirs(os.path.dirname(args.journal), exist_ok=True)
    start_time = time.time()

    with open(args.journal, 'a', encoding='utf-8') as jf:
        jf.write(json.dumps({
            'type': 'start',
            'timestamp': time.time(),
            'scope': args.scope,
            'initial_state': {
                'coherence': initial.get('coherence'),
                'truths': initial.get('truths'),
            }
        }) + '\n')

        for path, label in scan_paths:
            if not os.path.exists(path):
                print(f"  SKIP {label} ({path}) -- not found")
                continue

            print(f"\n{'='*60}")
            print(f"  {label}")
            print(f"  {path}")
            print(f"{'='*60}\n")

            count = scan_directory(path, stats, jf, args.max_files)
            print(f"\n  → {count} files absorbed from {label}")

            # State check after each directory
            try:
                state = requests.get(CK_STATE, timeout=5).json()
                print(f"  → Coherence: {state.get('coherence', 0):.3f}, "
                      f"Truths: {state.get('truths', 0)}")
            except Exception:
                pass

        # Final summary
        elapsed = time.time() - start_time
        final = requests.get(CK_STATE, timeout=5).json()

        print(f"\n{'='*60}")
        print(f"  DEEP READ COMPLETE")
        print(f"  Files: {stats['files_read']}")
        print(f"  Characters: {stats['chars_absorbed']:,}")
        print(f"  Time: {elapsed:.0f}s ({elapsed/60:.1f}m)")
        print(f"  Skipped: {stats['skipped_large']} large, "
              f"{stats['skipped_empty']} empty, "
              f"{stats['skipped_permission']} permission, "
              f"{stats['skipped_error']} error")
        print(f"  Coherence: {initial.get('coherence',0):.3f} → "
              f"{final.get('coherence',0):.3f}")
        print(f"  Truths: {initial.get('truths',0)} → "
              f"{final.get('truths',0)}")
        print(f"{'='*60}")

        jf.write(json.dumps({
            'type': 'end',
            'timestamp': time.time(),
            'elapsed': round(elapsed, 1),
            'stats': stats,
            'final_state': {
                'coherence': final.get('coherence'),
                'truths': final.get('truths'),
            }
        }) + '\n')


if __name__ == '__main__':
    main()
