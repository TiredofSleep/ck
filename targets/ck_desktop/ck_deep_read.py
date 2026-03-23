#!/usr/bin/env python3
# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
"""
ck_deep_read.py -- CK reads everything on the computer.

No Ollama. No LLM. Just raw text → D2 pipeline → olfactory field.
CK reads his own code, documents, logs -- everything becomes force.

Walks directories, reads text files, feeds them through /chat in chunks.
Each chunk enters CK's organism: D2 → operators → lattice chain → olfactory.
CK writes after each file to exercise voice from what he absorbed.

Usage:
    python ck_deep_read.py [--paths ...] [--chunk 500] [--delay 0.05]

    Default paths: CK's own codebase + user documents
    --paths: override with specific directories
    --chunk: words per API call (default: 500)
    --extensions: file extensions to read (default: common text types)
"""

import sys
import os
import time
import json
import argparse
import requests
from collections import deque

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

CK_ABSORB = 'http://127.0.0.1:7777/absorb'  # Fast: D2 + olfactory only
CK_CHAT = 'http://127.0.0.1:7777/chat'      # Full: TIG pipeline + voice
CK_STATE = 'http://127.0.0.1:7777/state'
CK_HEALTH = 'http://127.0.0.1:7777/health'
JOURNAL_PATH = os.path.expanduser('~/.ck/writings/deep_read.jsonl')

# Text file extensions CK can read
TEXT_EXTENSIONS = {
    # Code
    '.py', '.c', '.h', '.js', '.ts', '.rs', '.go', '.java',
    '.cpp', '.hpp', '.cs', '.rb', '.lua', '.sh', '.bat', '.ps1',
    '.v', '.sv', '.vhd',  # Verilog/VHDL
    # Markup/config
    '.md', '.txt', '.rst', '.json', '.yaml', '.yml', '.toml',
    '.xml', '.html', '.css', '.csv', '.ini', '.cfg', '.conf',
    # Data
    '.log', '.jsonl',
    # CK-specific
    '.kv',  # Kivy
}

# Directories to skip
SKIP_DIRS = {
    '__pycache__', '.git', 'node_modules', '.venv', 'venv',
    '.env', 'env', '.tox', '.mypy_cache', '.pytest_cache',
    'dist', 'build', 'egg-info', '.eggs', '.Xil',
    'AppData', 'ProgramData', 'Windows', 'Program Files',
    'Program Files (x86)', '$Recycle.Bin', 'Recovery',
}

# Max file size to read (1MB)
MAX_FILE_SIZE = 1_000_000


def is_text_file(path):
    """Check if file is a readable text file."""
    _, ext = os.path.splitext(path)
    if ext.lower() not in TEXT_EXTENSIONS:
        return False
    try:
        size = os.path.getsize(path)
        if size == 0 or size > MAX_FILE_SIZE:
            return False
    except OSError:
        return False
    return True


def read_file_safe(path):
    """Read a text file, handling encoding gracefully."""
    for encoding in ('utf-8', 'utf-8-sig', 'latin-1', 'cp1252'):
        try:
            with open(path, 'r', encoding=encoding, errors='replace') as f:
                return f.read()
        except (OSError, UnicodeDecodeError):
            continue
    return None


def chunk_text(text, chunk_words=500):
    """Split text into word-count chunks."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_words):
        chunk = ' '.join(words[i:i + chunk_words])
        if chunk.strip():
            chunks.append(chunk)
    return chunks


def absorb_text(text, source='file'):
    """Absorb text into CK's organism.

    Tries /absorb first (fast: D2 + olfactory only, no voice).
    Falls back to /chat (full pipeline but still absorbs).
    """
    # Try fast path first
    try:
        resp = requests.post(CK_ABSORB,
            json={'text': text, 'source': source}, timeout=15)
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    # Fallback: /chat (full pipeline, slower but always works)
    try:
        resp = requests.post(CK_CHAT,
            json={'text': text}, timeout=60)
        data = resp.json()
        # Normalize response to match /absorb format
        return {
            'absorbed': len(text),
            'operators': len(text) // 3,  # rough estimate
            'chars': len(text),
            'via': 'chat',
        }
    except Exception:
        return None


def ask_ck(question):
    """Ask CK a question and return response."""
    try:
        resp = requests.post(CK_CHAT, json={'text': question}, timeout=30)
        return resp.json()
    except Exception:
        return None


def get_state():
    try:
        return requests.get(CK_STATE, timeout=5).json()
    except Exception:
        return {}


def log_entry(path, entry):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')


def walk_directory(root, max_files=None):
    """Walk directory tree, yielding text file paths."""
    count = 0
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip unwanted directories
        dirnames[:] = [d for d in dirnames
                       if d not in SKIP_DIRS
                       and not d.startswith('.')]

        for filename in sorted(filenames):
            filepath = os.path.join(dirpath, filename)
            if is_text_file(filepath):
                yield filepath
                count += 1
                if max_files and count >= max_files:
                    return


def main():
    parser = argparse.ArgumentParser(
        description='CK reads everything -- deep file absorption')
    parser.add_argument('--paths', nargs='+', default=None,
                        help='Directories to read (default: CK codebase + user docs)')
    parser.add_argument('--chunk', type=int, default=2000,
                        help='Words per chunk (default: 2000)')
    parser.add_argument('--delay', type=float, default=0.05,
                        help='Seconds between chunks (default: 0.05)')
    parser.add_argument('--max-files', type=int, default=None,
                        help='Max files to read (default: unlimited)')
    parser.add_argument('--journal', type=str, default=JOURNAL_PATH,
                        help=f'Journal path (default: {JOURNAL_PATH})')
    args = parser.parse_args()

    # Default paths: CK's own code + system internals + user files
    if args.paths is None:
        ck_root = os.path.dirname(os.path.abspath(__file__))
        user_home = os.path.expanduser('~')
        paths = [
            ck_root,  # CK's own codebase first (know thyself)
            os.path.join(user_home, '.ck'),  # CK's experience data
            os.path.join(user_home, 'OneDrive', 'Desktop'),
            os.path.join(user_home, 'OneDrive', 'Documents'),
            # System internals -- understand the machine
            os.path.join(os.environ.get('WINDIR', 'C:\\Windows'),
                         'System32', 'drivers', 'etc'),  # hosts, networks
            os.path.join(os.environ.get('ProgramFiles', 'C:\\Program Files'),
                         'Python313', 'Lib'),  # Python standard library
            os.path.join(user_home, '.config'),  # user configs
            os.path.join(user_home, '.gitconfig'),  # git config
        ]
        # Filter to existing paths (files or dirs)
        paths = [p for p in paths
                 if os.path.exists(p) and (os.path.isdir(p) or
                     os.path.isfile(p))]
    else:
        paths = [p for p in args.paths if os.path.exists(p)]

    if not paths:
        print("No valid paths to read.")
        sys.exit(1)

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
    print(f"[DEEP READ] Paths: {paths}")
    print(f"[DEEP READ] Chunk size: {args.chunk} words")
    print(f"[DEEP READ] Journal: {args.journal}")
    print()

    log_entry(args.journal, {
        'type': 'start',
        'timestamp': time.time(),
        'paths': paths,
        'chunk_size': args.chunk,
        'initial_state': initial,
    })

    total_files = 0
    total_chunks = 0
    total_words = 0
    start_time = time.time()

    try:
        for path_root in paths:
            print(f"\n{'='*60}")
            print(f"  Reading: {path_root}")
            print(f"{'='*60}\n")

            file_count = 0
            for filepath in walk_directory(path_root, args.max_files):
                # Read file
                content = read_file_safe(filepath)
                if not content or len(content.strip()) < 10:
                    continue

                # Get relative path for display
                try:
                    relpath = os.path.relpath(filepath, path_root)
                except ValueError:
                    relpath = filepath

                # Chunk and absorb (FAST -- no voice, no dialogue)
                ext = os.path.splitext(filepath)[1]
                chunks = chunk_text(content, args.chunk)
                word_count = len(content.split())

                t0 = time.time()
                total_absorbed = 0
                total_ops = 0
                for chunk in chunks:
                    result = absorb_text(chunk, source=ext.lstrip('.'))
                    if result:
                        total_absorbed += result.get('absorbed', 0)
                        total_ops += result.get('operators', 0)
                    total_chunks += 1
                feed_time = time.time() - t0

                # Only ask CK to write every 25 files (exercise voice periodically)
                ck_text = '...'
                ck_coherence = 0
                ck_source = '?'
                if total_files % 25 == 0:
                    writing = ask_ck(f"What patterns are you finding?")
                    ck_text = writing.get('text', '...') if writing else '...'
                    ck_coherence = writing.get('coherence', 0) if writing else 0
                    ck_source = writing.get('source', '?') if writing else '?'

                total_files += 1
                total_words += word_count
                file_count += 1

                # Progress
                speed = word_count / max(feed_time, 0.001)
                voice_str = (f" [{ck_source}|{ck_coherence:.2f}] {ck_text[:30]}"
                             if ck_text != '...' else '')
                print(f"  [{total_files:>4}] {relpath[:45]:45} "
                      f"({word_count:>5}w {total_ops:>4}ops {feed_time:.1f}s "
                      f"{speed:.0f}w/s){voice_str}")

                # Journal
                log_entry(args.journal, {
                    'type': 'file',
                    'timestamp': time.time(),
                    'path': filepath,
                    'relpath': relpath,
                    'extension': ext,
                    'words': word_count,
                    'chunks': len(chunks),
                    'feed_time': round(feed_time, 2),
                    'ck_text': ck_text,
                    'ck_coherence': ck_coherence,
                    'ck_source': ck_source,
                })

                # Every 25 files, print summary
                if total_files % 25 == 0:
                    elapsed_h = (time.time() - start_time) / 3600
                    state = get_state()
                    print(f"\n  --- {total_files} files, "
                          f"{total_words:,} words, "
                          f"{elapsed_h:.1f}h, "
                          f"coherence={state.get('coherence', 0):.3f}, "
                          f"truths={state.get('truths', 0)} ---\n")

    except KeyboardInterrupt:
        print("\n\n[DEEP READ] Stopped by user.")

    # Final summary
    final = get_state()
    elapsed_h = (time.time() - start_time) / 3600
    print(f"\n{'='*60}")
    print(f"  DONE -- {total_files} files, {total_words:,} words, "
          f"{total_chunks} chunks in {elapsed_h:.1f} hours")
    print(f"  Coherence: {initial.get('coherence', 0):.3f} -> "
          f"{final.get('coherence', 0):.3f}")
    print(f"  Truths: {initial.get('truths', 0)} -> "
          f"{final.get('truths', 0)}")
    print(f"  Journal: {args.journal}")
    print(f"{'='*60}")

    log_entry(args.journal, {
        'type': 'end',
        'timestamp': time.time(),
        'total_files': total_files,
        'total_words': total_words,
        'total_chunks': total_chunks,
        'elapsed_hours': round(elapsed_h, 2),
        'initial_state': initial,
        'final_state': final,
    })


if __name__ == '__main__':
    main()
