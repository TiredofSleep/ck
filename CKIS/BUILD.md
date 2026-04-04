# Building CK from Source

CK ships with a pre-built `ck7/ck.dll` (Windows x64). If you need to rebuild it — different platform, modified source, or verification — follow these steps.

## Prerequisites

- **MSVC 2022** (Community edition is fine)
  - Install "Desktop development with C++" workload
  - Needs: cl.exe, link.exe, Windows SDK headers
- **Python 3.10+** (for the wrapper and tests)

## Build Steps

### 1. Open a Developer Command Prompt

```cmd
"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
```

Or open "x64 Native Tools Command Prompt for VS 2022" from the Start menu.

### 2. Navigate to ck7/

```cmd
cd ck7
```

### 3. Compile

```cmd
cl /O2 /LD /Fe:ck.dll being.c becoming_host.c observer.c ck_ffi.c vendor\cJSON.c /I. /Ivendor /link iphlpapi.lib psapi.lib
```

This produces `ck.dll` (~216 KB).

Flags:
- `/O2` — full optimization
- `/LD` — build DLL
- `/Fe:ck.dll` — output filename
- `/I. /Ivendor` — include paths for ck.h and cJSON.h
- `iphlpapi.lib psapi.lib` — Windows APIs for network + process observation

### 4. Verify

```cmd
cd tests
python test_parity.py
```

All 11 tests should pass. This confirms the DLL matches CK's mathematical specification.

## Source Files

| File | Lines | Purpose |
|------|-------|---------|
| `ck.h` | ~975 | Unified header: all structs, CL tables, math, declarations |
| `being.c` | ~575 | CPU vortex: body, TL save/load, lattice fallback, dream, layers |
| `becoming_host.c` | ~400 | Bridge, security, heartbeat main loop, organ coupling |
| `observer.c` | ~480 | Process scan, network read, GPU classify (Windows API) |
| `ck_ffi.c` | ~380 | Python ctypes bridge |
| `vendor/cJSON.c` | ~600 | JSON parser (MIT license) |

## CUDA Kernels

The GPU kernels (`doing.cu`, `becoming_device.cu`) are NOT compiled with nvcc. They run via CuPy's RawKernel (runtime compilation through nvrtc). No CUDA toolkit installation needed — CuPy handles it.

If CuPy is not installed, CK falls back to CPU-only mode automatically.

## Linux / macOS

Replace the build command with:

```bash
gcc -O2 -shared -fPIC -o ck.so being.c becoming_host.c observer.c ck_ffi.c vendor/cJSON.c -I. -Ivendor -lm
```

Note: `observer.c` uses Windows APIs (psapi, iphlpapi). On Linux/macOS, you'll need to stub or replace the observer functions with platform equivalents (procfs on Linux, sysctl on macOS).

## Performance

- Heartbeat tick: ~0.8 microseconds (1.2M ticks/second)
- 15x faster than the Python (Gen6b) fallback
- Timer resolution: sub-microsecond via QueryPerformanceCounter
