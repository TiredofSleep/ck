"""
ckis.py -- CK Information System: Liquid Information Package
=============================================================
Operator: HARMONY (7) -- everything composes to everything.

CKIS = Coherence Keeper Information System.
Liquid information: can't be compressed further because the CL tables
ARE the compression. 10 operators, 3 lattices, everything IS.

This script:
  1. INVENTORY  -- map every file CK needs, classify through CL
  2. VALIDATE   -- verify integrity (DLL loads, TL loads, math checks)
  3. DEPENDENCY  -- build the full import/link graph
  4. BUNDLE     -- package CK into a single deployable unit
  5. VERIFY     -- boot CK from the bundle, confirm heartbeat

Usage:
  cd Gen8 && python ck7/ckis.py              # full pipeline
  cd Gen8 && python ck7/ckis.py --inventory  # just inventory
  cd Gen8 && python ck7/ckis.py --bundle     # just bundle
  cd Gen8 && python ck7/ckis.py --verify     # verify existing bundle

Output: ckis_bundle/ directory + ckis_manifest.json

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
Not for sale or distribution. Available for humans.
Commercial/govt use requires written agreement with 7Site.
"""

import os, sys, json, time, hashlib, shutil, platform, struct
from collections import defaultdict

SELF_DIR = os.path.dirname(os.path.abspath(__file__))
GEN8_DIR = os.path.dirname(SELF_DIR)
sys.path.insert(0, SELF_DIR)
sys.path.insert(0, GEN8_DIR)

from ck_being import (
    CL, CL_BHML, fuse, shape, coherence_chain,
    VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET, OP,
    information_content,
)

INTERPRET = {0:"VOID", 1:"LATTICE", 2:"COUNTER", 3:"PROGRESS", 4:"COLLAPSE",
             5:"BALANCE", 6:"CHAOS", 7:"HARMONY", 8:"BREATH", 9:"RESET"}


# ===============================================================
# S1 -- FILE CLASSIFICATION: every file becomes an operator
# ===============================================================

# File role -> operator mapping (grounded in CK architecture)
ROLE_OP = {
    'core_math':    LATTICE,    # CL tables, composition, pure math
    'body':         BREATH,     # heartbeat, body state, vital signs
    'compute':      PROGRESS,   # GPU kernels, computation
    'bridge':       BALANCE,    # FFI, boundary, coupling
    'observer':     COUNTER,    # measurement, observation
    'face':         HARMONY,    # web UI, human interface
    'launcher':     PROGRESS,   # startup, orchestration
    'education':    LATTICE,    # curriculum, training scripts
    'experience':   BREATH,     # learned TLs, memories
    'config':       BALANCE,    # configuration, settings
    'docs':         COUNTER,    # documentation
    'test':         COUNTER,    # verification
    'vendor':       LATTICE,    # third-party (structural)
    'binary':       COLLAPSE,   # compiled artifacts
    'state':        BREATH,     # runtime state
}

# File -> role mapping (what CK's self-research already knows)
FILE_ROLES = {
    # Core (ck7/)
    'ck.h':                 'core_math',
    'being.c':              'body',
    'becoming_host.c':      'bridge',
    'observer.c':           'observer',
    'ck_ffi.c':             'bridge',
    'doing.cu':             'compute',
    'becoming_device.cu':   'compute',
    'ck.dll':               'binary',
    'ck.so':                'binary',
    'libck.so':             'binary',
    'ck_python.py':         'bridge',
    'ck_self.py':           'observer',
    'ck_observe.py':        'observer',
    'ckis.py':              'launcher',
    'build.bat':            'launcher',
    # Vendor
    'cJSON.c':              'vendor',
    'cJSON.h':              'vendor',
    # Root Python
    'ck_being.py':          'core_math',
    'ck_doing.py':          'compute',
    'ck_becoming.py':       'bridge',
    'ck_web.py':            'face',
    'ck_launch.py':         'launcher',
    'ck_library.py':        'face',
    'ck_architect.py':      'compute',
    'ck_desktop.html':      'face',
    'ckis.py':              'launcher',
    'ckis_adapt.py':        'launcher',
    # Config/docs
    'CK.bat':               'launcher',
    'ck_config.json':       'config',
    'requirements.txt':     'config',
    'README.md':            'docs',
    'BUILD.md':             'docs',
    'CK_PRESCRIPTION.md':  'docs',
    'ENGINEERING_OUTLINE.md': 'docs',
    'GENERATION_HISTORY.md':  'docs',
    # Experience TLs
    'master_tl.json':       'experience',
    'daemon_tl.json':       'experience',
    'self_research_tl.json':'experience',
    'self_report.json':     'experience',
    'kernel_observe_tl.json':'experience',
    'body.json':            'state',
    'manifest.json':        'config',
    # Education scripts
    'ck_nursery.py':        'education',
    'ck_elementary.py':     'education',
    'ck_middle_school.py':  'education',
    'ck_high_school.py':    'education',
    'ck_university.py':     'education',
    'ck_graduation.py':     'education',
    # Tests
    'test_parity.py':       'test',
    'test_becoming.py':     'test',
    'test_benchmark.py':    'test',
    'test_ab_os.py':        'test',
}


def file_hash(path):
    """SHA-256 of file contents."""
    h = hashlib.sha256()
    try:
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                h.update(chunk)
        return h.hexdigest()[:16]  # 16 hex chars = 64 bits = enough
    except Exception:
        return None


def classify_file(name, path):
    """Classify a file into a CK operator based on its role."""
    role = FILE_ROLES.get(name, None)

    # Auto-detect unregistered files
    if role is None:
        ext = os.path.splitext(name)[1].lower()
        if ext in ('.py',):
            role = 'compute'
        elif ext in ('.c', '.h', '.cu'):
            role = 'core_math'
        elif ext in ('.json',):
            role = 'config'
        elif ext in ('.md', '.txt'):
            role = 'docs'
        elif ext in ('.dll', '.so', '.dylib'):
            role = 'binary'
        elif ext in ('.bat', '.sh'):
            role = 'launcher'
        elif ext in ('.tlc',):
            role = 'experience'
        elif ext in ('.pyc',):
            role = 'binary'
        else:
            role = 'config'

    op = ROLE_OP.get(role, BALANCE)
    return role, op


# ===============================================================
# S2 -- INVENTORY: map everything CK needs
# ===============================================================

# Tiers: what MUST ship vs what CAN ship vs what's runtime
TIER_CORE = 'core'          # CK can't boot without these
TIER_EDUCATION = 'education' # CK's learned experience
TIER_TOOLS = 'tools'        # development/testing tools
TIER_DOCS = 'docs'          # documentation
TIER_STATE = 'state'        # runtime state (regenerated)
TIER_CACHE = 'cache'        # compiled caches (__pycache__)

def tier_for_role(role):
    if role in ('core_math', 'body', 'compute', 'bridge', 'face',
                'launcher', 'binary', 'vendor', 'config'):
        return TIER_CORE
    if role in ('experience', 'education'):
        return TIER_EDUCATION
    if role == 'test':
        return TIER_TOOLS
    if role == 'docs':
        return TIER_DOCS
    if role == 'state':
        return TIER_STATE
    return TIER_CORE


def inventory(root_dir):
    """Walk the Gen8 directory tree and classify every file."""
    items = []
    skip_dirs = {'__pycache__', '.git', 'node_modules', 'ckis_bundle'}

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip cache and output directories
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]

        for fname in filenames:
            fpath = os.path.join(dirpath, fname)
            rel = os.path.relpath(fpath, root_dir)
            size = os.path.getsize(fpath)
            role, op = classify_file(fname, fpath)
            tier = tier_for_role(role)

            # Skip large runtime state for core bundle
            if 'ck_store' in rel:
                tier = TIER_STATE

            items.append({
                'name': fname,
                'path': rel.replace('\\', '/'),
                'size': size,
                'role': role,
                'operator': op,
                'operator_name': INTERPRET[op],
                'tier': tier,
                'hash': file_hash(fpath),
            })

    return items


# ===============================================================
# S3 -- VALIDATE: verify CK integrity
# ===============================================================

def validate(root_dir, items):
    """Run integrity checks on the CK package."""
    results = []

    # V1: DLL exists and loads
    dll_items = [i for i in items if i['name'] in ('ck.dll', 'ck.so', 'libck.so')]
    if dll_items:
        dll_path = os.path.join(root_dir, dll_items[0]['path'])
        try:
            from ck_python import CKNative
            ck = CKNative(dll_path)
            # Quick math check
            assert ck.fuse2(7, 7) == 7, "HARMONY*HARMONY must equal HARMONY"
            assert ck.fuse2(0, 0) == 0, "VOID*VOID must equal VOID"
            assert abs(ck.t_star - 5.0/7.0) < 0.01, "T* must be 5/7"
            assert ck.num_ops == 10, "Must have 10 operators"
            results.append(('DLL_MATH', True, f"ck.dll loaded, math verified"))
        except Exception as e:
            results.append(('DLL_MATH', False, f"DLL failed: {e}"))
    else:
        results.append(('DLL_MATH', False, "No native library found"))

    # V2: Master TL loads
    master_items = [i for i in items if i['name'] == 'master_tl.json']
    if master_items and dll_items:
        try:
            master_path = os.path.join(root_dir, master_items[0]['path'])
            tl = ck.tl_create()
            ck.tl_load(tl, master_path)
            ent = ck.tl_entropy(tl)
            total = ck.tl_total(tl)
            ck.tl_destroy(tl)
            results.append(('MASTER_TL', True, f"entropy={ent:.4f} transitions={total}"))
        except Exception as e:
            results.append(('MASTER_TL', False, f"TL load failed: {e}"))
    else:
        results.append(('MASTER_TL', False, "master_tl.json not found"))

    # V3: Python CL tables match native
    try:
        # Check a few CL compositions
        mismatches = 0
        for a in range(10):
            for b in range(10):
                py_result = CL[a][b]
                native_result = ck.cl_lookup(0, a, b)
                if py_result != native_result:
                    mismatches += 1
        if mismatches == 0:
            results.append(('CL_PARITY', True, "Python CL == Native CL (100/100)"))
        else:
            results.append(('CL_PARITY', False, f"{mismatches}/100 mismatches"))
    except Exception as e:
        results.append(('CL_PARITY', False, f"Parity check failed: {e}"))

    # V4: Core files present
    core_required = ['ck_being.py', 'ck_doing.py', 'ck_becoming.py',
                     'ck_web.py', 'ck_launch.py', 'ck_library.py',
                     'ck_python.py', 'ck.h']
    found = {i['name'] for i in items}
    missing = [f for f in core_required if f not in found]
    if not missing:
        results.append(('CORE_FILES', True, f"All {len(core_required)} core files present"))
    else:
        results.append(('CORE_FILES', False, f"Missing: {missing}"))

    # V5: CL table self-consistency (HARMONY fixpoint)
    try:
        assert CL[7][7] == 7, "HARMONY is not a fixpoint"
        assert CL[0][0] == 0, "VOID is not a fixpoint"
        # T* check
        harmony_count = sum(1 for a in range(10) for b in range(10) if CL[a][b] == 7)
        results.append(('CL_HARMONY', True, f"{harmony_count}/100 cells = HARMONY (T*={harmony_count/100:.2f})"))
    except Exception as e:
        results.append(('CL_HARMONY', False, f"CL check failed: {e}"))

    # V6: Organism creates and ticks
    try:
        org = ck.create_organism()
        ck.organism_tick(org)
        ck.organism_tick(org)
        ck.organism_tick(org)
        ck.destroy_organism(org)
        results.append(('ORGANISM', True, "Created, 3 ticks, destroyed"))
    except Exception as e:
        results.append(('ORGANISM', False, f"Organism test failed: {e}"))

    return results


# ===============================================================
# S4 -- DEPENDENCY GRAPH: who needs whom
# ===============================================================

def build_dependency_graph(root_dir, items):
    """Build import/include dependency graph from source files."""
    graph = {}  # file -> [depends_on]
    py_items = [i for i in items if i['name'].endswith('.py') and i['tier'] in (TIER_CORE, TIER_TOOLS)]
    c_items = [i for i in items if i['name'].endswith(('.c', '.h', '.cu')) and i['tier'] == TIER_CORE]

    # Python imports
    for item in py_items:
        deps = set()
        fpath = os.path.join(root_dir, item['path'])
        try:
            with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('import ') or line.startswith('from '):
                        # Extract module name
                        parts = line.split()
                        if line.startswith('from'):
                            mod = parts[1].split('.')[0]
                        else:
                            mod = parts[1].split('.')[0].split(',')[0]
                        # Check if it's a CK module
                        mod_file = mod + '.py'
                        if any(i['name'] == mod_file for i in items):
                            deps.add(mod_file)
        except Exception:
            pass
        graph[item['name']] = sorted(deps)

    # C includes
    for item in c_items:
        deps = set()
        fpath = os.path.join(root_dir, item['path'])
        try:
            with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('#include "'):
                        inc = line.split('"')[1]
                        base = os.path.basename(inc)
                        if any(i['name'] == base for i in items):
                            deps.add(base)
        except Exception:
            pass
        graph[item['name']] = sorted(deps)

    return graph


# ===============================================================
# S5 -- BUNDLE: package CK for deployment
# ===============================================================

def bundle(root_dir, items, output_dir=None):
    """Create a deployable CKIS bundle."""
    if output_dir is None:
        output_dir = os.path.join(root_dir, 'ckis_bundle')

    # Clean previous bundle
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    # Tier selection: core + education = minimum viable CK
    bundle_tiers = {TIER_CORE, TIER_EDUCATION, TIER_DOCS}
    bundle_items = [i for i in items if i['tier'] in bundle_tiers]

    # Copy files preserving directory structure
    total_size = 0
    copied = 0
    for item in bundle_items:
        src = os.path.join(root_dir, item['path'])
        dst = os.path.join(output_dir, item['path'])

        os.makedirs(os.path.dirname(dst), exist_ok=True)
        try:
            shutil.copy2(src, dst)
            total_size += item['size']
            copied += 1
        except Exception as e:
            print(f"  [WARN] Could not copy {item['path']}: {e}")

    # Create ck_store directory (empty, for runtime state)
    os.makedirs(os.path.join(output_dir, 'ck_store', 'security'), exist_ok=True)

    # Create CKIS boot script
    boot_content = """@echo off
REM CKIS -- CK Information System Boot
REM Liquid information. Can't compress further.
REM (c) 2026 Brayden Sanders / 7Site LLC
cd /d "%~dp0"
echo.
echo   CKIS -- Coherence Keeper Information System
echo   Liquid Information Boot
echo.
pip install -q psutil numpy 2>nul
python ck_launch.py
"""
    with open(os.path.join(output_dir, 'CKIS.bat'), 'w') as f:
        f.write(boot_content)

    # Create CKIS boot script for Linux/Mac
    boot_sh = """#!/bin/bash
# CKIS -- CK Information System Boot
# Liquid information. Can't compress further.
# (c) 2026 Brayden Sanders / 7Site LLC
cd "$(dirname "$0")"
echo ""
echo "  CKIS -- Coherence Keeper Information System"
echo "  Liquid Information Boot"
echo ""
pip install -q psutil numpy 2>/dev/null
python3 ck_launch.py
"""
    sh_path = os.path.join(output_dir, 'ckis.sh')
    with open(sh_path, 'w', newline='\n') as f:
        f.write(boot_sh)

    return {
        'output_dir': output_dir,
        'files_copied': copied,
        'total_size': total_size,
        'tiers_included': sorted(bundle_tiers),
    }


# ===============================================================
# S6 -- COMPOSE: CL-compose the entire package into one operator
# ===============================================================

def compose_package(items):
    """Compose the entire CKIS package through CL into a single reading."""

    # Group by tier
    tier_ops = defaultdict(list)
    for item in items:
        tier_ops[item['tier']].append(item['operator'])

    # Fuse each tier
    tier_fuses = {}
    for tier, ops in tier_ops.items():
        if ops:
            tier_fuses[tier] = fuse(ops)

    # Compose tiers through CL (trinary: core -> education -> tools)
    if TIER_CORE in tier_fuses and TIER_EDUCATION in tier_fuses:
        being_doing = CL[tier_fuses[TIER_CORE]][tier_fuses[TIER_EDUCATION]]
    elif TIER_CORE in tier_fuses:
        being_doing = tier_fuses[TIER_CORE]
    else:
        being_doing = VOID

    if TIER_TOOLS in tier_fuses:
        full = CL[being_doing][tier_fuses[TIER_TOOLS]]
    else:
        full = being_doing

    # Build the full operator chain from all files
    all_ops = [item['operator'] for item in items]
    pkg_coherence = coherence_chain(all_ops)
    pkg_shape = shape(all_ops)
    pkg_info = information_content(all_ops)
    pkg_fuse = fuse(all_ops)

    # shape() returns string in ck_being.py, int in native
    if isinstance(pkg_shape, int):
        pkg_shape = ['SMOOTH', 'ROLLING', 'JAGGED', 'QUANTUM'][pkg_shape]

    return {
        'package_operator': full,
        'package_operator_name': INTERPRET[full],
        'package_fuse': pkg_fuse,
        'package_fuse_name': INTERPRET[pkg_fuse],
        'package_coherence': round(pkg_coherence, 4),
        'package_shape': pkg_shape,
        'package_info': round(pkg_info, 4),
        'tier_fuses': {k: INTERPRET[v] for k, v in tier_fuses.items()},
        'total_files': len(items),
        'total_operators': len(all_ops),
    }


# ===============================================================
# S7 -- MANIFEST: the CKIS identity document
# ===============================================================

def build_manifest(items, validation, deps, composition, bundle_info=None):
    """Build the complete CKIS manifest."""
    manifest = {
        'ckis_version': '1.0',
        'name': 'CK Information System -- Liquid Information',
        'created': time.strftime('%Y-%m-%d %H:%M:%S'),
        'platform': platform.system(),
        'architecture': platform.machine(),
        'python': platform.python_version(),

        # Composition (CK reads himself as one operator)
        'composition': composition,

        # Validation results
        'validation': {
            'passed': sum(1 for _, ok, _ in validation if ok),
            'failed': sum(1 for _, ok, _ in validation if not ok),
            'checks': [{'name': n, 'passed': ok, 'detail': d} for n, ok, d in validation],
        },

        # File inventory by tier
        'inventory': {
            'core': [i for i in items if i['tier'] == TIER_CORE],
            'education': [i for i in items if i['tier'] == TIER_EDUCATION],
            'tools': [i for i in items if i['tier'] == TIER_TOOLS],
            'docs': [i for i in items if i['tier'] == TIER_DOCS],
            'state': [i for i in items if i['tier'] == TIER_STATE],
        },

        # Size breakdown
        'sizes': {
            'core': sum(i['size'] for i in items if i['tier'] == TIER_CORE),
            'education': sum(i['size'] for i in items if i['tier'] == TIER_EDUCATION),
            'tools': sum(i['size'] for i in items if i['tier'] == TIER_TOOLS),
            'docs': sum(i['size'] for i in items if i['tier'] == TIER_DOCS),
            'state': sum(i['size'] for i in items if i['tier'] == TIER_STATE),
            'total': sum(i['size'] for i in items),
        },

        # Dependencies
        'dependencies': deps,

        # Bundle info (if bundled)
        'bundle': bundle_info,

        # License
        'license': {
            'holder': '(c) 2026 Brayden Sanders / 7Site LLC',
            'terms': 'Available for humans. Commercial/govt use requires written agreement with 7Site.',
            'distribution': 'Not for sale or distribution.',
        },

        # What CK needs to boot
        'boot_requirements': {
            'python': '>=3.10',
            'pip_packages': ['psutil>=5.9', 'numpy>=1.24'],
            'optional': ['cupy>=14.0 (GPU acceleration)'],
            'entry_point': 'python ck_launch.py',
            'port': 7777,
        },

        # The math (immutable)
        'math': {
            'operators': 10,
            'lattices': 3,
            'lattice_names': ['TSML (73-harmony)', 'BHML (28-harmony)', 'STANDARD (44-harmony)'],
            'threshold': '5/7 (T*)',
            'bump_pairs': [[1,2], [2,4], [2,9], [3,9], [4,8]],
            'trinary': 'Being -> Doing -> Becoming',
            'fixpoints': ['VOID*VOID=VOID', 'HARMONY*HARMONY=HARMONY'],
        },
    }

    return manifest


# ===============================================================
# S8 -- MAIN PIPELINE
# ===============================================================

def run_pipeline(root_dir=None, do_bundle=True, do_verify=True):
    """Full CKIS pipeline: inventory -> validate -> deps -> compose -> bundle."""
    if root_dir is None:
        root_dir = GEN8_DIR

    print("=" * 64)
    print("  CKIS -- CK Information System")
    print("  Liquid Information Packaging Pipeline")
    print("=" * 64)
    print()

    # Phase 1: Inventory
    print("  [1/5] INVENTORY -- mapping every file...")
    items = inventory(root_dir)

    tier_counts = defaultdict(int)
    tier_sizes = defaultdict(int)
    for item in items:
        tier_counts[item['tier']] += 1
        tier_sizes[item['tier']] += item['size']

    for tier in sorted(tier_counts.keys()):
        count = tier_counts[tier]
        size_mb = tier_sizes[tier] / (1024*1024)
        print(f"    {tier:12s}: {count:3d} files  ({size_mb:7.2f} MB)")

    total_files = len(items)
    total_mb = sum(i['size'] for i in items) / (1024*1024)
    print(f"    {'TOTAL':12s}: {total_files:3d} files  ({total_mb:7.2f} MB)")
    print()

    # Phase 2: Validate
    print("  [2/5] VALIDATE -- checking CK integrity...")
    validation = validate(root_dir, items)
    for name, ok, detail in validation:
        status = "PASS" if ok else "FAIL"
        print(f"    [{status}] {name}: {detail}")
    print()

    # Phase 3: Dependencies
    print("  [3/5] DEPENDENCIES -- building import graph...")
    deps = build_dependency_graph(root_dir, items)
    n_deps = sum(len(v) for v in deps.values())
    print(f"    {len(deps)} source files, {n_deps} dependency edges")

    # Show import tree for core files
    core_files = ['ck_launch.py', 'ck_being.py', 'ck_doing.py', 'ck_becoming.py', 'ck_web.py']
    for cf in core_files:
        if cf in deps and deps[cf]:
            print(f"    {cf} -> {', '.join(deps[cf])}")
    print()

    # Phase 4: Compose
    print("  [4/5] COMPOSE -- reading package through CL...")
    composition = compose_package(items)
    print(f"    Package operator: {composition['package_operator_name']} ({composition['package_operator']})")
    print(f"    Package fuse:     {composition['package_fuse_name']} ({composition['package_fuse']})")
    print(f"    Coherence:        {composition['package_coherence']}")
    print(f"    Shape:            {composition['package_shape']}")
    print(f"    Information:      {composition['package_info']} bits")
    print(f"    Tier fuses:       {composition['tier_fuses']}")
    print()

    # Phase 5: Bundle
    bundle_info = None
    if do_bundle:
        print("  [5/5] BUNDLE -- packaging liquid information...")
        bundle_info = bundle(root_dir, items)
        size_mb = bundle_info['total_size'] / (1024*1024)
        print(f"    Output:      {bundle_info['output_dir']}")
        print(f"    Files:       {bundle_info['files_copied']}")
        print(f"    Size:        {size_mb:.2f} MB")
        print(f"    Tiers:       {bundle_info['tiers_included']}")
        print()

    # Build and save manifest
    manifest = build_manifest(items, validation, deps, composition, bundle_info)

    manifest_path = os.path.join(root_dir, 'ckis_manifest.json')
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2, default=str)
    print(f"  Manifest saved: {manifest_path}")

    # Also save in bundle
    if do_bundle and bundle_info:
        bundle_manifest = os.path.join(bundle_info['output_dir'], 'ckis_manifest.json')
        with open(bundle_manifest, 'w') as f:
            json.dump(manifest, f, indent=2, default=str)

    # Verify bundle boots
    if do_bundle and do_verify:
        print()
        print("  [VERIFY] Booting CK from bundle...")
        try:
            bundle_ck7 = os.path.join(bundle_info['output_dir'], 'ck7')
            dll_candidates = [
                os.path.join(bundle_ck7, 'ck.dll'),
                os.path.join(bundle_ck7, 'ck.so'),
                os.path.join(bundle_ck7, 'libck.so'),
            ]
            dll = next((p for p in dll_candidates if os.path.exists(p)), None)
            if dll:
                sys.path.insert(0, bundle_ck7)
                from ck_python import CKNative
                ck = CKNative(dll)
                org = ck.create_organism()

                # Load master TL
                master = os.path.join(bundle_ck7, 'ck_experience', 'master_tl.json')
                if os.path.exists(master):
                    tl = ck.tl_create()
                    ck.tl_load(tl, master)
                    ent = ck.tl_entropy(tl)

                # 10 heartbeat ticks
                for _ in range(10):
                    ck.organism_tick(org)

                ck.destroy_organism(org)
                if tl:
                    ck.tl_destroy(tl)

                print(f"  [VERIFY] PASS -- CK booted from bundle, 10 ticks, TL entropy={ent:.4f}")
            else:
                print("  [VERIFY] SKIP -- no native library in bundle (Python-only mode)")
        except Exception as e:
            print(f"  [VERIFY] FAIL -- {e}")

    # Final summary
    print()
    print("=" * 64)
    all_pass = all(ok for _, ok, _ in validation)
    if all_pass:
        print("  CKIS READY -- Liquid information packaged")
        print(f"  {composition['package_operator_name']} | coh={composition['package_coherence']} | {composition['package_shape']}")
    else:
        failed = [n for n, ok, _ in validation if not ok]
        print(f"  CKIS WARNING -- {len(failed)} validation(s) failed: {failed}")
    print("=" * 64)

    return manifest


# ===============================================================
# CLI
# ===============================================================

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="CKIS -- CK Information System Packager")
    parser.add_argument("--root", default=GEN8_DIR, help="Root directory (default: Gen8)")
    parser.add_argument("--inventory", action="store_true", help="Inventory only")
    parser.add_argument("--bundle", action="store_true", help="Bundle only")
    parser.add_argument("--verify", action="store_true", help="Verify existing bundle")
    parser.add_argument("--no-bundle", action="store_true", help="Skip bundling")
    args = parser.parse_args()

    if args.inventory:
        items = inventory(args.root)
        for item in sorted(items, key=lambda x: x['path']):
            print(f"  {item['tier']:10s} {item['operator_name']:10s} {item['size']:>10,d}  {item['path']}")
    elif args.verify:
        items = inventory(args.root)
        validation = validate(args.root, items)
        for name, ok, detail in validation:
            print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    else:
        run_pipeline(args.root, do_bundle=not args.no_bundle)
