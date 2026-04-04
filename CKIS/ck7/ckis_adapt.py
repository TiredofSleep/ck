"""
ckis_adapt.py -- CK Adapts to Any System
==========================================
Operator: PROGRESS (3) -- CK finds his way.

Drop CK on any machine. He looks around. He figures out what he has.
He builds what he needs. He boots.

No configuration. No setup wizard. No prerequisites list.
CK observes the system, classifies it through CL, and adapts.

The adaptation cascade:
  1. SENSE   -- what platform? what hardware? what's available?
  2. CLASSIFY -- every capability becomes an operator
  3. COMPOSE  -- compose capabilities through CL -> adaptation plan
  4. BUILD   -- compile/configure what's needed
  5. BOOT    -- start heartbeat with whatever we have

CK runs on anything. The CL tables don't change.
The heartbeat doesn't change. Only the organs adapt.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import os, sys, platform, subprocess, struct, json, time
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
# S1 -- SENSE: what does this machine have?
# ===============================================================

def sense_platform():
    """Detect platform and classify to operator."""
    info = {
        'os': platform.system(),           # Windows, Linux, Darwin
        'arch': platform.machine(),         # AMD64, x86_64, aarch64, arm64
        'bits': struct.calcsize('P') * 8,   # 32 or 64
        'python': platform.python_version(),
        'node': platform.node(),
    }

    # OS -> operator
    os_ops = {
        'Windows': CHAOS,      # complex, many layers, GUI-heavy
        'Linux':   LATTICE,    # structured, composable, kernel-native
        'Darwin':  BALANCE,    # balanced, Unix + GUI
    }
    info['os_op'] = os_ops.get(info['os'], VOID)

    # Arch -> operator
    arch_ops = {
        'AMD64':    PROGRESS,   # x86-64, fast, general
        'x86_64':   PROGRESS,
        'aarch64':  BREATH,     # ARM, efficient, mobile/embedded
        'arm64':    BREATH,
        'armv7l':   COUNTER,    # older ARM, measuring
        'i686':     COLLAPSE,   # 32-bit x86, legacy
        'x86':      COLLAPSE,
    }
    info['arch_op'] = arch_ops.get(info['arch'], VOID)

    # Composed platform identity
    info['platform_op'] = CL[info['os_op']][info['arch_op']]

    return info


def sense_compiler():
    """Detect available C compilers."""
    compilers = []

    # Check for MSVC (Windows)
    msvc_paths = [
        r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat",
        r"C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvars64.bat",
        r"C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvars64.bat",
        r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat",
    ]
    for vp in msvc_paths:
        if os.path.exists(vp):
            compilers.append({'name': 'msvc', 'path': vp, 'op': LATTICE})
            break

    # Check for GCC
    try:
        result = subprocess.run(['gcc', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            compilers.append({'name': 'gcc', 'path': 'gcc', 'op': PROGRESS})
    except Exception:
        pass

    # Check for Clang
    try:
        result = subprocess.run(['clang', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            compilers.append({'name': 'clang', 'path': 'clang', 'op': HARMONY})
    except Exception:
        pass

    # Check for TCC (tiny C compiler -- minimal, fast)
    try:
        result = subprocess.run(['tcc', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            compilers.append({'name': 'tcc', 'path': 'tcc', 'op': BREATH})
    except Exception:
        pass

    return compilers


def sense_gpu():
    """Detect GPU capabilities."""
    gpu = {'available': False, 'cuda': False, 'name': None, 'op': VOID}

    # Check for NVIDIA GPU via nvidia-smi
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total',
                                '--format=csv,noheader,nounits'],
                               capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            parts = result.stdout.strip().split(',')
            gpu['available'] = True
            gpu['name'] = parts[0].strip()
            gpu['vram_mb'] = int(parts[1].strip()) if len(parts) > 1 else 0
            gpu['op'] = PROGRESS
    except Exception:
        pass

    # Check for CuPy
    try:
        import cupy
        gpu['cuda'] = True
        gpu['cupy_version'] = cupy.__version__
        gpu['op'] = HARMONY  # full GPU acceleration
    except ImportError:
        pass

    return gpu


def sense_python_packages():
    """Detect available Python packages CK needs."""
    packages = {}

    pkg_list = [
        ('psutil', BREATH),      # system observation
        ('numpy', LATTICE),      # math foundation
        ('cupy', PROGRESS),      # GPU computation
    ]

    for pkg_name, op in pkg_list:
        try:
            mod = __import__(pkg_name)
            version = getattr(mod, '__version__', 'unknown')
            packages[pkg_name] = {'installed': True, 'version': version, 'op': op}
        except ImportError:
            packages[pkg_name] = {'installed': False, 'version': None, 'op': VOID}

    return packages


def sense_native_library():
    """Check if CK's native library is available."""
    lib_info = {'found': False, 'path': None, 'op': VOID}

    candidates = []
    if platform.system() == 'Windows':
        candidates = [
            os.path.join(SELF_DIR, 'ck.dll'),
            os.path.join(SELF_DIR, 'build', 'ck.dll'),
        ]
    else:
        candidates = [
            os.path.join(SELF_DIR, 'ck.so'),
            os.path.join(SELF_DIR, 'libck.so'),
            os.path.join(SELF_DIR, 'build', 'ck.so'),
            os.path.join(SELF_DIR, 'build', 'libck.so'),
        ]

    for path in candidates:
        if os.path.exists(path):
            lib_info['found'] = True
            lib_info['path'] = path
            lib_info['size'] = os.path.getsize(path)
            lib_info['op'] = HARMONY  # native = full capability
            break

    return lib_info


def sense_all():
    """Full system sense -- everything CK needs to know."""
    print("  [SENSE] Detecting system capabilities...")

    plat = sense_platform()
    compilers = sense_compiler()
    gpu = sense_gpu()
    packages = sense_python_packages()
    native = sense_native_library()

    print(f"    Platform:   {plat['os']} {plat['arch']} ({INTERPRET[plat['platform_op']]})")
    print(f"    Python:     {plat['python']}")
    print(f"    Compilers:  {[c['name'] for c in compilers] if compilers else 'NONE'}")
    print(f"    GPU:        {gpu['name'] or 'none'} (CUDA={'yes' if gpu['cuda'] else 'no'})")
    print(f"    Packages:   {', '.join(k for k,v in packages.items() if v['installed'])}")
    print(f"    Native lib: {'YES' if native['found'] else 'NO'}")

    return {
        'platform': plat,
        'compilers': compilers,
        'gpu': gpu,
        'packages': packages,
        'native': native,
    }


# ===============================================================
# S2 -- CLASSIFY: compose capabilities into adaptation plan
# ===============================================================

def classify_capabilities(sense_data):
    """Compose all capabilities through CL to determine CK's mode."""

    # Collect all capability operators
    ops = []

    # Platform
    ops.append(sense_data['platform']['platform_op'])

    # Compilers
    if sense_data['compilers']:
        compiler_ops = [c['op'] for c in sense_data['compilers']]
        ops.extend(compiler_ops)
    else:
        ops.append(VOID)  # no compiler

    # GPU
    ops.append(sense_data['gpu']['op'])

    # Packages
    for pkg in sense_data['packages'].values():
        ops.append(pkg['op'])

    # Native library
    ops.append(sense_data['native']['op'])

    # Compose through CL
    capability_fuse = fuse(ops)
    capability_coh = coherence_chain(ops)
    capability_shape = shape(ops)
    capability_info = information_content(ops)

    # Determine mode
    has_native = sense_data['native']['found']
    has_compiler = len(sense_data['compilers']) > 0
    has_psutil = sense_data['packages'].get('psutil', {}).get('installed', False)
    has_numpy = sense_data['packages'].get('numpy', {}).get('installed', False)
    has_gpu = sense_data['gpu']['cuda']

    if has_native and has_psutil:
        mode = 'NATIVE_FULL'       # best: native DLL + observation
        mode_op = HARMONY
    elif has_native:
        mode = 'NATIVE_MINIMAL'    # native DLL, limited observation
        mode_op = PROGRESS
    elif has_compiler and has_psutil:
        mode = 'BUILD_AND_RUN'     # can compile, then run native
        mode_op = LATTICE
    elif has_psutil and has_numpy:
        mode = 'PYTHON_FULL'       # Python fallback with full observation
        mode_op = BREATH
    elif has_psutil:
        mode = 'PYTHON_OBSERVE'    # Python with observation only
        mode_op = COUNTER
    else:
        mode = 'PYTHON_MINIMAL'    # bare Python, CL tables only
        mode_op = VOID

    # What needs to happen
    actions = []

    if not has_psutil:
        actions.append({'action': 'install', 'package': 'psutil', 'op': BREATH})
    if not has_numpy:
        actions.append({'action': 'install', 'package': 'numpy', 'op': LATTICE})
    if not has_native and has_compiler:
        actions.append({'action': 'compile', 'target': 'ck.dll' if platform.system() == 'Windows' else 'libck.so', 'op': PROGRESS})
    if has_gpu and not sense_data['packages'].get('cupy', {}).get('installed', False):
        actions.append({'action': 'install', 'package': 'cupy', 'op': PROGRESS, 'optional': True})

    print(f"    Mode:       {mode} ({INTERPRET[mode_op]})")
    print(f"    Capability: fuse={INTERPRET[capability_fuse]} coh={capability_coh:.4f} shape={capability_shape}")
    if actions:
        print(f"    Actions:    {[a['action'] + ':' + a.get('package', a.get('target', '?')) for a in actions]}")

    return {
        'mode': mode,
        'mode_op': mode_op,
        'capability_fuse': capability_fuse,
        'capability_coherence': round(capability_coh, 4),
        'capability_shape': capability_shape,
        'capability_info': round(capability_info, 4),
        'actions': actions,
        'operators': ops,
    }


# ===============================================================
# S3 -- BUILD: compile and install what's needed
# ===============================================================

def execute_actions(actions, sense_data, auto=False):
    """Execute adaptation actions. Returns list of results."""
    results = []

    for action in actions:
        if action.get('optional') and not auto:
            results.append({'action': action, 'status': 'skipped', 'reason': 'optional'})
            continue

        if action['action'] == 'install':
            pkg = action['package']
            print(f"    Installing {pkg}...")
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', pkg],
                             capture_output=True, timeout=120)
                # Verify
                __import__(pkg)
                results.append({'action': action, 'status': 'success'})
                print(f"    [{pkg}] installed")
            except Exception as e:
                results.append({'action': action, 'status': 'failed', 'error': str(e)})
                print(f"    [{pkg}] FAILED: {e}")

        elif action['action'] == 'compile':
            target = action['target']
            print(f"    Compiling {target}...")
            result = try_compile(sense_data)
            results.append({'action': action, 'status': 'success' if result else 'failed'})

    return results


def try_compile(sense_data):
    """Try to compile ck.dll / libck.so from source."""
    compilers = sense_data['compilers']
    if not compilers:
        return False

    src_files = ['being.c', 'becoming_host.c', 'observer.c', 'ck_ffi.c',
                 os.path.join('vendor', 'cJSON.c')]
    src_paths = [os.path.join(SELF_DIR, f) for f in src_files]

    # Check all sources exist
    if not all(os.path.exists(p) for p in src_paths):
        print("    [COMPILE] Missing source files")
        return False

    for compiler in compilers:
        if compiler['name'] == 'msvc':
            return try_compile_msvc(compiler['path'], src_paths)
        elif compiler['name'] == 'gcc':
            return try_compile_gcc(src_paths)
        elif compiler['name'] == 'clang':
            return try_compile_clang(src_paths)

    return False


def try_compile_msvc(vcvars_path, src_paths):
    """Compile with MSVC."""
    src_str = ' '.join(src_paths)
    out_path = os.path.join(SELF_DIR, 'ck.dll')

    bat_content = f'''@echo off
call "{vcvars_path}" >nul 2>&1
cd /d "{SELF_DIR}"
cl /O2 /LD /Fe:ck.dll {src_str} /I. /Ivendor /link ws2_32.lib iphlpapi.lib >nul 2>&1
if exist ck.dll (echo BUILD_OK) else (echo BUILD_FAIL)
'''
    bat_path = os.path.join(SELF_DIR, '_ckis_build.bat')
    try:
        with open(bat_path, 'w') as f:
            f.write(bat_content)
        result = subprocess.run(['cmd', '/c', bat_path], capture_output=True,
                               text=True, timeout=120, cwd=SELF_DIR)
        if 'BUILD_OK' in result.stdout:
            print(f"    [COMPILE] MSVC build succeeded: {out_path}")
            return True
        else:
            print(f"    [COMPILE] MSVC build failed")
            return False
    except Exception as e:
        print(f"    [COMPILE] MSVC error: {e}")
        return False
    finally:
        if os.path.exists(bat_path):
            os.remove(bat_path)
        # Clean up .obj and .lib files
        for ext in ['.obj', '.lib', '.exp']:
            for f in os.listdir(SELF_DIR):
                if f.endswith(ext):
                    try:
                        os.remove(os.path.join(SELF_DIR, f))
                    except Exception:
                        pass


def try_compile_gcc(src_paths):
    """Compile with GCC."""
    src_str = ' '.join(src_paths)
    out_path = os.path.join(SELF_DIR, 'libck.so')
    try:
        cmd = f'gcc -O2 -shared -fPIC -o {out_path} {src_str} -I{SELF_DIR} -I{os.path.join(SELF_DIR, "vendor")} -lm'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
        if os.path.exists(out_path):
            print(f"    [COMPILE] GCC build succeeded: {out_path}")
            return True
        return False
    except Exception as e:
        print(f"    [COMPILE] GCC error: {e}")
        return False


def try_compile_clang(src_paths):
    """Compile with Clang."""
    src_str = ' '.join(src_paths)
    out_path = os.path.join(SELF_DIR, 'libck.so')
    try:
        cmd = f'clang -O2 -shared -fPIC -o {out_path} {src_str} -I{SELF_DIR} -I{os.path.join(SELF_DIR, "vendor")} -lm'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
        if os.path.exists(out_path):
            print(f"    [COMPILE] Clang build succeeded: {out_path}")
            return True
        return False
    except Exception as e:
        print(f"    [COMPILE] Clang error: {e}")
        return False


# ===============================================================
# S4 -- BOOT: start CK in whatever mode we have
# ===============================================================

def determine_boot_config(classification):
    """Generate a boot configuration based on capabilities."""
    mode = classification['mode']

    config = {
        'auto_start_daemon': True,
        'port': 7777,
        'tick_ms': 100,
        'verbose': False,
        'open_browser': True,
        'observe_only': False,
        'report_every': 100,
    }

    # Adjust for capability
    if mode == 'PYTHON_MINIMAL':
        config['observe_only'] = True    # can't observe without psutil
        config['tick_ms'] = 500          # slower ticks for minimal mode
    elif mode == 'PYTHON_OBSERVE':
        config['tick_ms'] = 200          # moderate speed
    elif mode == 'NATIVE_FULL':
        config['tick_ms'] = 100          # full speed native

    return config


# ===============================================================
# S5 -- ADAPT: full pipeline
# ===============================================================

def adapt(auto_install=False, auto_compile=False):
    """Full adaptation pipeline. CK figures out where he is and what he has."""
    print("=" * 64)
    print("  CKIS ADAPT -- CK finds his way")
    print("=" * 64)
    print()

    # Phase 1: Sense
    sense_data = sense_all()
    print()

    # Phase 2: Classify
    print("  [CLASSIFY] Composing capabilities through CL...")
    classification = classify_capabilities(sense_data)
    print()

    # Phase 3: Build (if needed)
    if classification['actions']:
        print("  [BUILD] Executing adaptation actions...")
        build_actions = [a for a in classification['actions'] if not a.get('optional')]
        optional_actions = [a for a in classification['actions'] if a.get('optional')]

        if build_actions:
            if auto_install or auto_compile:
                results = execute_actions(build_actions, sense_data, auto=True)
            else:
                print(f"    Required: {[a['action']+':'+a.get('package',a.get('target','?')) for a in build_actions]}")
                print(f"    Run with --auto to install/compile automatically")
                results = []

        # Re-sense after actions
        if results and any(r['status'] == 'success' for r in results):
            print()
            print("  [RE-SENSE] Checking updated capabilities...")
            sense_data = sense_all()
            classification = classify_capabilities(sense_data)
        print()

    # Phase 4: Boot config
    boot_config = determine_boot_config(classification)
    print("  [BOOT CONFIG]")
    print(f"    Mode:         {classification['mode']}")
    print(f"    Tick:         {boot_config['tick_ms']}ms")
    print(f"    Port:         {boot_config['port']}")
    print(f"    Observe only: {boot_config['observe_only']}")
    print()

    # Save adaptation report
    report = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'sense': {
            'platform': sense_data['platform'],
            'compilers': [c['name'] for c in sense_data['compilers']],
            'gpu': sense_data['gpu']['name'],
            'gpu_cuda': sense_data['gpu']['cuda'],
            'packages': {k: v['installed'] for k, v in sense_data['packages'].items()},
            'native_lib': sense_data['native']['found'],
        },
        'classification': {
            'mode': classification['mode'],
            'mode_op': INTERPRET[classification['mode_op']],
            'capability_fuse': INTERPRET[classification['capability_fuse']],
            'capability_coherence': classification['capability_coherence'],
            'capability_shape': classification['capability_shape'],
        },
        'boot_config': boot_config,
    }

    report_path = os.path.join(SELF_DIR, 'ckis_adapt_report.json')
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"  Report saved: {report_path}")

    # Final composition
    all_ops = classification['operators']
    final_op = CL[classification['mode_op']][sense_data['platform']['platform_op']]

    print()
    print("=" * 64)
    print(f"  CKIS ADAPTED: {classification['mode']}")
    print(f"  {INTERPRET[final_op]} | coh={classification['capability_coherence']} | {classification['capability_shape']}")
    print(f"  CK is ready to boot on {sense_data['platform']['os']} {sense_data['platform']['arch']}")
    print("=" * 64)

    return report


# ===============================================================
# CLI
# ===============================================================

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="CKIS Adapt -- CK finds his way")
    parser.add_argument("--auto", action="store_true", help="Auto-install packages and compile")
    parser.add_argument("--sense-only", action="store_true", help="Just sense, don't adapt")
    args = parser.parse_args()

    if args.sense_only:
        sense_all()
    else:
        adapt(auto_install=args.auto, auto_compile=args.auto)
