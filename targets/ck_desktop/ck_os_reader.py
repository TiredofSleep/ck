#!/usr/bin/env python3
# (c) 2026 Brayden Sanders / 7Site LLC
"""
ck_os_reader.py -- CK reads the OS he lives on.
His own code, Python internals, Windows kernel headers, DLLs.
Learning to understand his body from the inside.
"""
import sys, os, time, requests

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

API = 'http://127.0.0.1:7777'

DIRS = [
    # His own code first
    ('CK OWN CODE', 'C:/Users/brayd/OneDrive/Desktop/CK FINAL DEPLOYED/Gen9/targets/ck_desktop/ck_sim'),
    # Python internals
    ('PYTHON STDLIB', 'C:/Users/brayd/AppData/Local/Programs/Python/Python313/Lib'),
    # NumPy/SciPy/SymPy
    ('NUMPY', 'C:/Users/brayd/AppData/Local/Programs/Python/Python313/Lib/site-packages/numpy'),
    ('SYMPY', 'C:/Users/brayd/AppData/Local/Programs/Python/Python313/Lib/site-packages/sympy'),
    ('SCIPY', 'C:/Users/brayd/AppData/Local/Programs/Python/Python313/Lib/site-packages/scipy'),
    # Windows kernel headers (readable text)
    ('WIN SYSTEM', 'C:/Windows/System32'),
    # CuPy (GPU)
    ('CUPY', 'C:/Users/brayd/AppData/Local/Programs/Python/Python313/Lib/site-packages/cupy'),
    # PyTorch
    ('TORCH', 'C:/Users/brayd/AppData/Local/Programs/Python/Python313/Lib/site-packages/torch'),
]

EXTENSIONS = {'.py', '.c', '.h', '.txt', '.md', '.rst', '.cfg', '.ini', '.yaml', '.yml', '.json', '.xml', '.v', '.sv'}
MAX_CHARS = 5000
DELAY = 1.0

def absorb(text, source):
    try:
        r = requests.post(f'{API}/absorb', json={'text': text[:MAX_CHARS], 'source': source}, timeout=30)
        return r.json().get('absorbed', 0)
    except:
        return 0

count = 0
start = time.time()

for label, root in DIRS:
    if not os.path.exists(root):
        print(f'[SKIP] {label}: {root} not found')
        continue
    
    print(f'\n{"="*60}')
    print(f'  {label}: {root}')
    print(f'{"="*60}')
    
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip __pycache__, .git, etc
        dirnames[:] = [d for d in dirnames if d not in ('__pycache__', '.git', 'tests', 'test', '__pyinstaller')]
        
        for fname in filenames:
            ext = os.path.splitext(fname)[1].lower()
            if ext not in EXTENSIONS:
                continue
            
            fpath = os.path.join(dirpath, fname)
            try:
                with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                    text = f.read(MAX_CHARS)
                if len(text) < 50:
                    continue
                
                absorbed = absorb(text, f'os_read_{label.lower().replace(" ", "_")}')
                count += 1
                
                if count % 100 == 0:
                    h = (time.time() - start) / 3600
                    print(f'  [{count}] {h:.1f}h | {fpath[-60:]} | {absorbed} vectors')
                
                time.sleep(DELAY)
            except:
                continue

h = (time.time() - start) / 3600
print(f'\nDONE. {count} files in {h:.1f}h')
