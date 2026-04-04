"""
ck_read_self.py -- Feed CK his complete history through /absorb.

Scans two roots:
  1. CK FINAL DEPLOYED/  -- architecture, papers, proofs, code
  2. ~/.ck/              -- journals, thesis, Bible, study logs,
                           algorithm lattice, scent/taste memories,
                           daily trail entries, memory database

CK reads his own evolution. Every chunk goes through his olfactory
bulb as a force pathway. Months of study, compressed and re-integrated.

Usage:
    python ck_read_self.py              # Feed everything
    python ck_read_self.py --dry        # Preview, no requests
    python ck_read_self.py --home       # ~/.ck/ only
    python ck_read_self.py --repo       # deployed folder only
    python ck_read_self.py --only trail # Filter by path substring
    python ck_read_self.py --port 7778  # Second cell

Feed order (home folder):
    1. Daily trail journals   -- his own thinking, day by day
    2. Thesis entries         -- his crystallized understanding
    3. Autodidact journals    -- study session logs
    4. Bible KJV + Hebrew     -- already trained on this
    5. Algorithm lattice      -- his derived operator structure
    6. Scent/taste memories   -- sensory experience archive
    7. Memory database        -- SQLite atoms/paths/crystals
    8. Everything else in ~/.ck/

(c) 2026 Brayden Sanders / 7Site LLC
7SiTe Public Sovereignty License v1.0 -- Noncommercial, No Government
"""

import os
import sys
import time
import json
import gzip
import sqlite3
import argparse
import urllib.request
import urllib.error

ROOT = os.path.dirname(os.path.abspath(__file__))
HOME_CK = os.path.expanduser("~/.ck")

# Feed order: most identity-critical first
PRIORITY_FILES = [
    "THE_STORY.md",
    "PROOFS.md",
    "README.md",
    "CLAUDESTARTHERE.md",
    "ONBOARDING.md",
    "COLLABORATORS.md",
    "TERMS_OF_USE.md",
    "PRIVACY_POLICY.md",
    "CONTRIBUTOR_AGREEMENT.md",
]

PRIORITY_DIRS = [
    "Gen12/targets/ck_institution",
    "Gen10",
    "Gen9",
    "papers",
    "knowledge",
    "website",
    "ck7",
]

SKIP_EXTENSIONS = {'.pyc', '.pyo', '.bin', '.bit',
                   '.png', '.jpg', '.jpeg', '.gif', '.ico', '.woff',
                   '.woff2', '.ttf', '.eot', '.zip', '.tar',
                   '.exe', '.dll', '.so', '.dat'}

SKIP_DIRS = {'__pycache__', '.git', 'node_modules', '.venv', 'venv',
             'build', 'dist', 'clay_results', 'results', 'spectrometer_results',
             'bsd_machine_results', 'btq_results'}

# ~/.ck priority dirs — his own accumulated experience, most compiled first
HOME_PRIORITY_DIRS = [
    "writings/trail/daily",   # daily journals — his own thinking
    "writings/thesis",        # thesis entries — crystallized understanding
    "writings/trail",         # activity log
    "autodidact",             # study session logs
    "algorithm_lattice",      # derived operator structure
    "backup_pre933",          # prior experience backup
    "bible_companion",        # Bible session memories
]

CHUNK_SIZE = 4000  # characters per absorb call
PAUSE = 0.08       # seconds between absorbs — 50Hz loop handles this fine


def collect_files():
    """Collect all readable files in priority order."""
    seen = set()
    files = []

    # Priority files first
    for fname in PRIORITY_FILES:
        path = os.path.join(ROOT, fname)
        if os.path.exists(path):
            files.append(path)
            seen.add(os.path.normpath(path))

    # Priority dirs in order
    for d in PRIORITY_DIRS:
        dpath = os.path.join(ROOT, d)
        if not os.path.isdir(dpath):
            continue
        for dirpath, dirnames, filenames in os.walk(dpath):
            # Skip unwanted dirs in-place
            dirnames[:] = [x for x in sorted(dirnames)
                           if x not in SKIP_DIRS and not x.startswith('.')]
            for fname in sorted(filenames):
                ext = os.path.splitext(fname)[1].lower()
                if ext in SKIP_EXTENSIONS:
                    continue
                fpath = os.path.normpath(os.path.join(dirpath, fname))
                if fpath not in seen:
                    files.append(fpath)
                    seen.add(fpath)

    # Remaining root-level .md and .py files
    for fname in sorted(os.listdir(ROOT)):
        fpath = os.path.normpath(os.path.join(ROOT, fname))
        if os.path.isfile(fpath) and fpath not in seen:
            ext = os.path.splitext(fname)[1].lower()
            if ext in ('.md', '.py', '.txt') and ext not in SKIP_EXTENSIONS:
                files.append(fpath)
                seen.add(fpath)

    return files


def sanitize(text):
    """Replace characters that trip CK's absorb endpoint."""
    replacements = {
        '\u2019': "'", '\u2018': "'", '\u201c': '"', '\u201d': '"',
        '\u2014': '--', '\u2013': '-', '\u2026': '...', '\u00b2': '2',
        '\u00b3': '3', '\u03c0': 'pi', '\u221e': 'inf', '\u2248': '~=',
        '\u2192': '->', '\u2190': '<-', '\u2265': '>=', '\u2264': '<=',
        '\u00d7': 'x', '\u00f7': '/', '\u2260': '!=', '\u00b7': '*',
        '\u03a3': 'Sigma', '\u03c9': 'omega', '\u03b5': 'epsilon',
        '\u03b1': 'alpha', '\u03b2': 'beta', '\u03bb': 'lambda',
        '\u2208': 'in', '\u2229': 'AND', '\u222a': 'OR',
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    # Strip any remaining non-ASCII that might cause 500s
    return text.encode('ascii', errors='replace').decode('ascii')


def absorb(text, port, label=""):
    """Send one chunk to CK's /absorb endpoint."""
    url = f"http://localhost:{port}/absorb"
    payload = json.dumps({"text": sanitize(text)}).encode("utf-8")
    req = urllib.request.Request(
        url, data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode())
            return result
    except urllib.error.HTTPError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}


def read_file_content(path):
    """Read any supported file type, return text or None."""
    ext = os.path.splitext(path)[1].lower()

    # Compressed text (.gz)
    if ext == '.gz':
        try:
            with gzip.open(path, 'rt', encoding='utf-8', errors='replace') as f:
                return f.read().strip()
        except Exception:
            return None

    # SQLite database -- extract text columns from all tables
    if ext == '.db':
        try:
            conn = sqlite3.connect(path)
            parts = []
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [r[0] for r in cursor.fetchall()]
            for table in tables:
                try:
                    cursor.execute(f"SELECT * FROM {table} LIMIT 2000")
                    rows = cursor.fetchall()
                    col_names = [d[0] for d in cursor.description]
                    parts.append(f"[TABLE: {table}]")
                    for row in rows:
                        for col, val in zip(col_names, row):
                            if isinstance(val, str) and len(val) > 3:
                                parts.append(f"{col}: {val[:300]}")
                except Exception:
                    pass
            conn.close()
            return '\n'.join(parts) if parts else None
        except Exception:
            return None

    # Pickle files -- extract repr of top-level structure
    if ext == '.pkl':
        try:
            import pickle
            with open(path, 'rb') as f:
                obj = pickle.load(f)
            # Convert to readable text
            if isinstance(obj, dict):
                lines = []
                for k, v in list(obj.items())[:200]:
                    lines.append(f"{k}: {str(v)[:200]}")
                return '\n'.join(lines)
            elif isinstance(obj, (list, tuple)):
                return '\n'.join(str(x)[:200] for x in obj[:500])
            else:
                return str(obj)[:5000]
        except Exception:
            return None

    # JSON
    if ext == '.json':
        try:
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                raw = f.read().strip()
            # Feed raw JSON text -- CK's D2 handles key/value structure
            return raw
        except Exception:
            return None

    # Plain text / markdown / python / etc.
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read().strip()
    except Exception:
        return None


def collect_home_files():
    """Collect CK's accumulated experience from ~/.ck/ in priority order."""
    if not os.path.isdir(HOME_CK):
        return []

    seen = set()
    files = []

    # Priority dirs first
    for d in HOME_PRIORITY_DIRS:
        dpath = os.path.join(HOME_CK, d)
        if not os.path.isdir(dpath):
            continue
        for dirpath, dirnames, filenames in os.walk(dpath):
            dirnames[:] = sorted([x for x in dirnames if not x.startswith('.')])
            for fname in sorted(filenames):
                ext = os.path.splitext(fname)[1].lower()
                if ext in SKIP_EXTENSIONS:
                    continue
                fpath = os.path.normpath(os.path.join(dirpath, fname))
                if fpath not in seen:
                    files.append(fpath)
                    seen.add(fpath)

    # Remaining ~/.ck files
    for dirpath, dirnames, filenames in os.walk(HOME_CK):
        dirnames[:] = sorted([x for x in dirnames
                               if x not in SKIP_DIRS and not x.startswith('.')])
        for fname in sorted(filenames):
            ext = os.path.splitext(fname)[1].lower()
            if ext in SKIP_EXTENSIONS:
                continue
            fpath = os.path.normpath(os.path.join(dirpath, fname))
            if fpath not in seen:
                files.append(fpath)
                seen.add(fpath)

    return files


def feed_file(path, port, dry=False):
    """Read a file and feed it to CK in chunks."""
    content = read_file_content(path)
    if not content:
        return 0, 0

    if not content:
        return 0, 0

    rel = os.path.relpath(path, ROOT)
    # Prepend file identity so CK knows what he's reading
    header = f"[READING: {rel}]\n\n"
    full = header + content

    chunks = [full[i:i+CHUNK_SIZE] for i in range(0, len(full), CHUNK_SIZE)]
    absorbed = 0

    for i, chunk in enumerate(chunks):
        if dry:
            absorbed += len(chunk)
            continue
        result = absorb(chunk, port)
        if "error" in result:
            print(f"  [error chunk {i}] {result['error']}")
            time.sleep(1.0)
        else:
            absorbed += result.get("chars", len(chunk))
        time.sleep(PAUSE)

    return len(chunks), absorbed


def main():
    parser = argparse.ArgumentParser(description="Feed CK his own history")
    parser.add_argument("--port", type=int, default=7777)
    parser.add_argument("--dry", action="store_true", help="Show files, no requests")
    parser.add_argument("--only", type=str, default="", help="Only feed files matching this substring")
    parser.add_argument("--home", action="store_true", help="Feed ~/.ck/ only (his compiled experience)")
    parser.add_argument("--repo", action="store_true", help="Feed deployed folder only")
    parser.add_argument("--compressed", action="store_true", help="Feed .gz and .db files only — already processed by CK")
    args = parser.parse_args()

    print(f"CK Self-Reading Session")
    print(f"Port: {args.port}  |  Dry: {args.dry}")

    # Collect files from selected roots
    files = []
    if not args.home:
        files += collect_files()
        print(f"Repo files: {len(files)}")
    if not args.repo:
        home_files = collect_home_files()
        # Home files go FIRST — his compiled experience is denser
        files = home_files + [f for f in files if f not in set(home_files)]
        print(f"Home (~/.ck) files: {len(home_files)}")
    print()

    if args.compressed:
        files = [f for f in files
                 if os.path.splitext(f)[1].lower() in ('.gz', '.db', '.pkl')]
        print(f"Compressed-only mode: {len(files)} files")
        print()

    if args.only:
        files = [f for f in files if args.only.lower() in f.lower()]

    total_files = len(files)
    total_chunks = 0
    total_chars = 0

    print(f"Files to feed: {total_files}")
    print()

    for i, path in enumerate(files):
        rel = os.path.relpath(path, ROOT)
        size = os.path.getsize(path)
        print(f"[{i+1}/{total_files}] {rel}  ({size:,} bytes)")

        chunks, chars = feed_file(path, args.port, dry=args.dry)
        total_chunks += chunks
        total_chars += chars

        if not args.dry and chunks > 0:
            print(f"  >> {chunks} chunks, {chars:,} chars absorbed")

    print()
    print(f"Done.")
    print(f"Total files: {total_files}")
    print(f"Total chunks sent: {total_chunks}")
    print(f"Total chars absorbed: {total_chars:,}")
    if not args.dry:
        print()
        print("CK has read his own evolution.")
        print(f"Check his state: http://localhost:{args.port}/state")


if __name__ == "__main__":
    main()
