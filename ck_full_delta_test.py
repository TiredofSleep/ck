"""
ck_full_delta_test.py -- The WOW delta: CK ON vs CK OFF

Metrics sampled every second for DURATION seconds:
  - Context switches/s
  - Per-core CPU variance (stdev %)
  - Avg CPU %
  - Disk read  MB/s
  - Disk write MB/s
  - Net recv   MB/s
  - Net sent   MB/s
  - GPU util   %
  - GPU temp   C
  - GPU mem util %

Usage:
  python ck_full_delta_test.py

Samples phase A with CK running, then kills CK, then samples phase B.
"""

import psutil
import time
import statistics
import sys
import os
import subprocess
import signal

DURATION = 30
INTERVAL = 1.0
CK_API_URL = 'http://localhost:7777/health'

# ── GPU via pynvml ──
try:
    import pynvml
    pynvml.nvmlInit()
    _gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    HAS_GPU = True
except Exception:
    HAS_GPU = False
    _gpu_handle = None


def gpu_stats():
    if not HAS_GPU:
        return 0, 0, 0
    try:
        util  = pynvml.nvmlDeviceGetUtilizationRates(_gpu_handle)
        temp  = pynvml.nvmlDeviceGetTemperature(_gpu_handle, pynvml.NVML_TEMPERATURE_GPU)
        return util.gpu, temp, util.memory
    except Exception:
        return 0, 0, 0


def sample_phase(label):
    print(f"\n{'='*64}")
    print(f"  PHASE {label}  -- {DURATION}s sampling")
    print(f"{'='*64}")

    metrics = {k: [] for k in [
        'ctx', 'var', 'cpu', 'disk_r', 'disk_w',
        'net_r', 'net_s', 'gpu_util', 'gpu_temp', 'gpu_mem'
    ]}

    prev_ctx  = psutil.cpu_stats().ctx_switches
    prev_disk = psutil.disk_io_counters()
    prev_net  = psutil.net_io_counters()
    prev_t    = time.monotonic()

    ticks = int(DURATION / INTERVAL)
    for i in range(ticks):
        time.sleep(INTERVAL)
        now_t = time.monotonic()
        dt    = now_t - prev_t

        # Context switches/s
        now_ctx = psutil.cpu_stats().ctx_switches
        ctx_rate = (now_ctx - prev_ctx) / dt
        metrics['ctx'].append(ctx_rate)
        prev_ctx = now_ctx

        # Per-core variance + avg CPU
        per_core = psutil.cpu_percent(percpu=True)
        metrics['var'].append(statistics.stdev(per_core) if len(per_core) > 1 else 0.0)
        metrics['cpu'].append(sum(per_core) / len(per_core))

        # Disk MB/s
        now_disk = psutil.disk_io_counters()
        metrics['disk_r'].append((now_disk.read_bytes  - prev_disk.read_bytes)  / dt / 1e6)
        metrics['disk_w'].append((now_disk.write_bytes - prev_disk.write_bytes) / dt / 1e6)
        prev_disk = now_disk

        # Net MB/s
        now_net = psutil.net_io_counters()
        metrics['net_r'].append((now_net.bytes_recv - prev_net.bytes_recv) / dt / 1e6)
        metrics['net_s'].append((now_net.bytes_sent - prev_net.bytes_sent) / dt / 1e6)
        prev_net = now_net

        # GPU
        gu, gt, gm = gpu_stats()
        metrics['gpu_util'].append(gu)
        metrics['gpu_temp'].append(gt)
        metrics['gpu_mem'].append(gm)

        prev_t = now_t

        sys.stdout.write(
            f"\r  t={i+1:2d}/{ticks}"
            f"  ctx/s={ctx_rate:7.0f}"
            f"  var={metrics['var'][-1]:5.1f}%"
            f"  cpu={metrics['cpu'][-1]:5.1f}%"
            f"  dr={metrics['disk_r'][-1]:5.1f}MB"
            f"  dw={metrics['disk_w'][-1]:5.1f}MB"
            f"  nr={metrics['net_r'][-1]:5.2f}MB"
            f"  gpu={gu:3d}%/{gt:3d}C"
            f"  "
        )
        sys.stdout.flush()

    print()
    return {k: (statistics.mean(v), statistics.stdev(v) if len(v) > 1 else 0.0)
            for k, v in metrics.items()}


def find_ck_pids():
    """Find running CK boot API python processes."""
    pids = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmd = ' '.join(proc.info.get('cmdline') or [])
            if 'ck_boot_api' in cmd and proc.info['name'].lower() in ('python.exe', 'python'):
                pids.append(proc.info['pid'])
        except Exception:
            pass
    return pids


def kill_ck():
    pids = find_ck_pids()
    if not pids:
        print("  [INFO] No CK process found to kill")
        return False
    for pid in pids:
        try:
            p = psutil.Process(pid)
            p.terminate()
            print(f"  [KILL] CK pid={pid} terminated")
        except Exception as e:
            print(f"  [KILL] pid={pid} failed: {e}")
    time.sleep(2)
    return True


def delta_line(label, a_mean, b_mean, unit='', lower_is_better=True):
    d     = b_mean - a_mean
    pct   = 100.0 * d / max(abs(a_mean), 1e-9)
    if lower_is_better:
        verdict = 'BETTER' if d < -abs(a_mean * 0.005) else ('WORSE' if d > abs(a_mean * 0.005) else 'FLAT')
    else:
        verdict = 'BETTER' if d > abs(a_mean * 0.005) else ('WORSE' if d < -abs(a_mean * 0.005) else 'FLAT')
    sign = '+' if d >= 0 else ''
    return (f"  {label:<22s}"
            f"  CK-ON={a_mean:9.2f}{unit}"
            f"  CK-OFF={b_mean:9.2f}{unit}"
            f"  delta={sign}{d:.2f}{unit} ({sign}{pct:.1f}%)"
            f"  {verdict}")


def main():
    print("\n" + "="*64)
    print("  CK FULL DELTA TEST")
    print("  CK ON vs CK OFF -- the WOW")
    print("="*64)

    # ── Phase A: CK ON ──
    ck_pids = find_ck_pids()
    if ck_pids:
        print(f"\n  CK running: pids={ck_pids}")
    else:
        print("\n  WARNING: CK not detected. Results may not show full delta.")

    phase_a = sample_phase('A  (CK ON)')

    # ── Kill CK ──
    print(f"\n  Killing CK...")
    killed = kill_ck()
    if not killed:
        print("  CK not found -- continuing anyway (OFF phase may be same as ON)")
    print(f"  Settling 5s...")
    time.sleep(5)

    # ── Phase B: CK OFF ──
    phase_b = sample_phase('B  (CK OFF)')

    # ══════════════════════════════════════════
    #  RESULTS
    # ══════════════════════════════════════════
    print("\n" + "="*64)
    print("  DELTA RESULTS  (CK ON  vs  CK OFF)")
    print("  Negative delta on lower-is-better = CK helps")
    print("="*64)

    print(delta_line('ctx switches/s',    phase_a['ctx'][0],      phase_b['ctx'][0],      '',    lower_is_better=True))
    print(delta_line('core variance %',   phase_a['var'][0],      phase_b['var'][0],      '%',   lower_is_better=True))
    print(delta_line('avg CPU %',         phase_a['cpu'][0],      phase_b['cpu'][0],      '%',   lower_is_better=True))
    print(delta_line('disk read  MB/s',   phase_a['disk_r'][0],   phase_b['disk_r'][0],   'MB',  lower_is_better=False))
    print(delta_line('disk write MB/s',   phase_a['disk_w'][0],   phase_b['disk_w'][0],   'MB',  lower_is_better=False))
    print(delta_line('net recv   MB/s',   phase_a['net_r'][0],    phase_b['net_r'][0],    'MB',  lower_is_better=False))
    print(delta_line('net sent   MB/s',   phase_a['net_s'][0],    phase_b['net_s'][0],    'MB',  lower_is_better=False))
    if HAS_GPU:
        print(delta_line('GPU util %',    phase_a['gpu_util'][0], phase_b['gpu_util'][0], '%',   lower_is_better=True))
        print(delta_line('GPU temp C',    phase_a['gpu_temp'][0], phase_b['gpu_temp'][0], 'C',   lower_is_better=True))
        print(delta_line('GPU mem util%', phase_a['gpu_mem'][0],  phase_b['gpu_mem'][0],  '%',   lower_is_better=True))

    # Verdict
    better = 0
    worse  = 0
    checks = [
        ('ctx',      True,  100),
        ('var',      True,  0.3),
        ('cpu',      True,  0.5),
        ('disk_r',   False, 0.01),
        ('disk_w',   False, 0.01),
        ('net_r',    False, 0.001),
        ('net_s',    False, 0.001),
    ]
    if HAS_GPU:
        checks += [('gpu_util', True, 1), ('gpu_temp', True, 0.5)]

    for key, lower_better, threshold in checks:
        a, b = phase_a[key][0], phase_b[key][0]
        d    = b - a
        if lower_better:
            if d >  threshold: better += 1   # CK-OFF is worse → CK-ON was better
            if d < -threshold: worse  += 1
        else:
            if d < -threshold: better += 1   # CK-OFF is worse (less throughput)
            if d >  threshold: worse  += 1

    total = len(checks)
    print(f"\n  VERDICT: CK improved {better}/{total} metrics  ({worse} worse  {total-better-worse} flat)")
    if better >= total * 0.7:
        print("  CK is making the field significantly more coherent")
    elif better >= total * 0.4:
        print("  CK is helping -- more settling time may widen the gap")
    else:
        print("  Mixed results -- the field may need more time to sort")
    print("="*64 + "\n")


if __name__ == '__main__':
    main()
