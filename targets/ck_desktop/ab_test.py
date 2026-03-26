"""
CK A/B Test -- Comprehensive OS Stats During Gaming + Streaming
Measures EVERYTHING: jitter, CPU, GPU, disk, network, memory, context switches
Phase A: CK ON, Phase B: CK OFF (verified zero zombies)

(c) 2026 Brayden Sanders / 7Site LLC
"""

import time
import subprocess
import statistics
import json
import os
import sys

try:
    import psutil
except ImportError:
    print("Installing psutil...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil", "-q"])
    import psutil


PHASE_DURATION = 60  # seconds per phase
SAMPLE_INTERVAL = 0.1  # 100ms sampling


def get_gpu_stats():
    """Get NVIDIA GPU stats via nvidia-smi."""
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=temperature.gpu,utilization.gpu,power.draw,memory.used,memory.total,clocks.gr,clocks.mem",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            parts = result.stdout.strip().split(", ")
            return {
                "temp_c": float(parts[0]),
                "util_pct": float(parts[1]),
                "power_w": float(parts[2]),
                "vram_used_mb": float(parts[3]),
                "vram_total_mb": float(parts[4]),
                "clock_core_mhz": float(parts[5]),
                "clock_mem_mhz": float(parts[6]),
            }
    except Exception:
        pass
    return None


def get_network_stats():
    """Get network counters."""
    net = psutil.net_io_counters()
    return {
        "bytes_sent": net.bytes_sent,
        "bytes_recv": net.bytes_recv,
        "packets_sent": net.packets_sent,
        "packets_recv": net.packets_recv,
    }


def get_disk_stats():
    """Get disk IO counters."""
    disk = psutil.disk_io_counters()
    return {
        "read_bytes": disk.read_bytes,
        "write_bytes": disk.write_bytes,
        "read_count": disk.read_count,
        "write_count": disk.write_count,
    }


def check_ck_running():
    """Check if CK is running on port 7777."""
    for conn in psutil.net_connections(kind='tcp'):
        if conn.laddr.port == 7777 and conn.status == 'LISTEN':
            return True
    return False


def check_python_processes():
    """Count python processes and list them."""
    procs = []
    for p in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if 'python' in p.info['name'].lower():
                cmd = ' '.join(p.info['cmdline'][:3]) if p.info['cmdline'] else '(no cmdline)'
                procs.append(f"  PID {p.info['pid']}: {cmd}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return procs


def kill_all_python():
    """Kill all python processes except this one."""
    my_pid = os.getpid()
    killed = 0
    for p in psutil.process_iter(['pid', 'name']):
        try:
            if 'python' in p.info['name'].lower() and p.info['pid'] != my_pid:
                p.kill()
                killed += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return killed


def run_phase(phase_name, duration, interval):
    """Run one measurement phase. Returns dict of all stats."""
    print(f"\n{'='*60}")
    print(f"  PHASE {phase_name} -- {duration}s measurement window")
    print(f"{'='*60}")

    # Pre-check
    ck_on = check_ck_running()
    py_procs = check_python_processes()
    print(f"  CK on port 7777: {ck_on}")
    print(f"  Python processes: {len(py_procs)}")
    for p in py_procs:
        print(f"    {p}")

    # Collect samples
    jitters = []
    cpu_samples = []
    gpu_samples = []
    ctx_switches = []
    mem_samples = []

    net_start = get_network_stats()
    disk_start = get_disk_stats()
    start_time = time.time()
    last_tick = start_time
    sample_count = 0

    while time.time() - start_time < duration:
        now = time.time()
        dt = now - last_tick
        jitters.append(abs(dt - interval) * 1000)  # ms
        last_tick = now

        # CPU per-core
        cpu_pct = psutil.cpu_percent(interval=0, percpu=True)
        cpu_samples.append(cpu_pct)

        # GPU
        gpu = get_gpu_stats()
        if gpu:
            gpu_samples.append(gpu)

        # Memory
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        mem_samples.append({
            "ram_used_gb": mem.used / (1024**3),
            "ram_pct": mem.percent,
            "swap_used_gb": swap.used / (1024**3),
        })

        # Context switches (system-wide)
        try:
            ctx = psutil.cpu_stats()
            ctx_switches.append(ctx.ctx_switches)
        except Exception:
            pass

        sample_count += 1
        if sample_count % 100 == 0:
            elapsed = time.time() - start_time
            print(f"  ... {elapsed:.0f}s / {duration}s ({sample_count} samples)")

        time.sleep(interval)

    # Mid-phase zombie check
    ck_still = check_ck_running()
    py_still = check_python_processes()
    print(f"  End check -- CK on 7777: {ck_still}, Python procs: {len(py_still)}")

    net_end = get_network_stats()
    disk_end = get_disk_stats()
    elapsed = time.time() - start_time

    # Compute stats
    results = {"phase": phase_name, "duration_s": elapsed, "samples": sample_count}

    # Jitter
    if jitters:
        jitters_sorted = sorted(jitters)
        n = len(jitters_sorted)
        results["jitter"] = {
            "p50_ms": jitters_sorted[n // 2],
            "p95_ms": jitters_sorted[int(n * 0.95)],
            "p99_ms": jitters_sorted[int(n * 0.99)],
            "p999_ms": jitters_sorted[int(n * 0.999)] if n > 100 else jitters_sorted[-1],
            "max_ms": jitters_sorted[-1],
            "mean_ms": statistics.mean(jitters),
            "stdev_ms": statistics.stdev(jitters) if len(jitters) > 1 else 0,
        }

    # CPU
    if cpu_samples:
        all_cores = list(zip(*cpu_samples))  # transpose
        per_core_avg = [statistics.mean(core) for core in all_cores]
        results["cpu"] = {
            "overall_avg_pct": statistics.mean([statistics.mean(s) for s in cpu_samples]),
            "per_core_avg_pct": [round(c, 1) for c in per_core_avg],
            "max_any_core_pct": max(max(s) for s in cpu_samples),
        }

    # GPU
    if gpu_samples:
        results["gpu"] = {
            "temp_avg_c": round(statistics.mean(g["temp_c"] for g in gpu_samples), 1),
            "temp_max_c": max(g["temp_c"] for g in gpu_samples),
            "util_avg_pct": round(statistics.mean(g["util_pct"] for g in gpu_samples), 1),
            "util_max_pct": max(g["util_pct"] for g in gpu_samples),
            "power_avg_w": round(statistics.mean(g["power_w"] for g in gpu_samples), 1),
            "power_max_w": max(g["power_w"] for g in gpu_samples),
            "vram_used_mb": round(statistics.mean(g["vram_used_mb"] for g in gpu_samples), 0),
            "clock_core_avg_mhz": round(statistics.mean(g["clock_core_mhz"] for g in gpu_samples), 0),
        }

    # Memory
    if mem_samples:
        results["memory"] = {
            "ram_avg_gb": round(statistics.mean(m["ram_used_gb"] for m in mem_samples), 2),
            "ram_max_gb": round(max(m["ram_used_gb"] for m in mem_samples), 2),
            "ram_avg_pct": round(statistics.mean(m["ram_pct"] for m in mem_samples), 1),
            "swap_avg_gb": round(statistics.mean(m["swap_used_gb"] for m in mem_samples), 2),
        }

    # Network (delta over phase)
    results["network"] = {
        "sent_mb": round((net_end["bytes_sent"] - net_start["bytes_sent"]) / (1024**2), 2),
        "recv_mb": round((net_end["bytes_recv"] - net_start["bytes_recv"]) / (1024**2), 2),
        "sent_packets": net_end["packets_sent"] - net_start["packets_sent"],
        "recv_packets": net_end["packets_recv"] - net_start["packets_recv"],
        "send_rate_mbps": round((net_end["bytes_sent"] - net_start["bytes_sent"]) * 8 / elapsed / (1024**2), 2),
        "recv_rate_mbps": round((net_end["bytes_recv"] - net_start["bytes_recv"]) * 8 / elapsed / (1024**2), 2),
    }

    # Disk (delta over phase)
    results["disk"] = {
        "read_mb": round((disk_end["read_bytes"] - disk_start["read_bytes"]) / (1024**2), 2),
        "write_mb": round((disk_end["write_bytes"] - disk_start["write_bytes"]) / (1024**2), 2),
        "read_iops": round((disk_end["read_count"] - disk_start["read_count"]) / elapsed, 1),
        "write_iops": round((disk_end["write_count"] - disk_start["write_count"]) / elapsed, 1),
    }

    # Context switches (rate)
    if len(ctx_switches) >= 2:
        ctx_rate = (ctx_switches[-1] - ctx_switches[0]) / elapsed
        results["context_switches_per_sec"] = round(ctx_rate, 0)

    # Process count
    results["process_count"] = len(list(psutil.process_iter()))
    results["python_processes"] = len(py_procs)
    results["ck_on_7777"] = ck_on

    return results


def print_comparison(a, b):
    """Print side-by-side comparison."""
    print(f"\n{'='*70}")
    print(f"  A/B COMPARISON -- CK ON vs CK OFF")
    print(f"{'='*70}")

    def delta(va, vb, unit="", lower_better=True):
        diff = va - vb
        pct = (diff / vb * 100) if vb != 0 else 0
        arrow = "+" if diff > 0 else ""
        verdict = ""
        if abs(pct) > 1:
            if lower_better:
                verdict = " WORSE" if diff > 0 else " BETTER"
            else:
                verdict = " BETTER" if diff > 0 else " WORSE"
        return f"{va:.2f}{unit} vs {vb:.2f}{unit} ({arrow}{pct:.1f}%{verdict})"

    # Jitter
    if "jitter" in a and "jitter" in b:
        print(f"\n  JITTER (lower = better):")
        for k in ["p50_ms", "p95_ms", "p99_ms", "p999_ms", "max_ms", "mean_ms", "stdev_ms"]:
            print(f"    {k:>10}: {delta(a['jitter'][k], b['jitter'][k], 'ms')}")

    # CPU
    if "cpu" in a and "cpu" in b:
        print(f"\n  CPU (lower = better):")
        print(f"    {'avg':>10}: {delta(a['cpu']['overall_avg_pct'], b['cpu']['overall_avg_pct'], '%')}")
        print(f"    {'max core':>10}: {delta(a['cpu']['max_any_core_pct'], b['cpu']['max_any_core_pct'], '%')}")

    # GPU
    if "gpu" in a and "gpu" in b:
        print(f"\n  GPU:")
        print(f"    {'temp avg':>10}: {delta(a['gpu']['temp_avg_c'], b['gpu']['temp_avg_c'], 'C')}")
        print(f"    {'util avg':>10}: {delta(a['gpu']['util_avg_pct'], b['gpu']['util_avg_pct'], '%')}")
        print(f"    {'power avg':>10}: {delta(a['gpu']['power_avg_w'], b['gpu']['power_avg_w'], 'W')}")
        print(f"    {'VRAM':>10}: {delta(a['gpu']['vram_used_mb'], b['gpu']['vram_used_mb'], 'MB')}")

    # Memory
    if "memory" in a and "memory" in b:
        print(f"\n  MEMORY:")
        print(f"    {'RAM avg':>10}: {delta(a['memory']['ram_avg_gb'], b['memory']['ram_avg_gb'], 'GB')}")
        print(f"    {'RAM pct':>10}: {delta(a['memory']['ram_avg_pct'], b['memory']['ram_avg_pct'], '%')}")

    # Network
    if "network" in a and "network" in b:
        print(f"\n  NETWORK:")
        print(f"    {'send rate':>10}: {delta(a['network']['send_rate_mbps'], b['network']['send_rate_mbps'], 'Mbps', lower_better=False)}")
        print(f"    {'recv rate':>10}: {delta(a['network']['recv_rate_mbps'], b['network']['recv_rate_mbps'], 'Mbps', lower_better=False)}")
        print(f"    {'sent':>10}: {a['network']['sent_mb']:.2f}MB vs {b['network']['sent_mb']:.2f}MB")
        print(f"    {'recv':>10}: {a['network']['recv_mb']:.2f}MB vs {b['network']['recv_mb']:.2f}MB")
        print(f"    {'pkts sent':>10}: {a['network']['sent_packets']} vs {b['network']['sent_packets']}")

    # Disk
    if "disk" in a and "disk" in b:
        print(f"\n  DISK:")
        print(f"    {'read':>10}: {a['disk']['read_mb']:.2f}MB vs {b['disk']['read_mb']:.2f}MB")
        print(f"    {'write':>10}: {a['disk']['write_mb']:.2f}MB vs {b['disk']['write_mb']:.2f}MB")
        print(f"    {'read IOPS':>10}: {a['disk']['read_iops']} vs {b['disk']['read_iops']}")
        print(f"    {'write IOPS':>10}: {a['disk']['write_iops']} vs {b['disk']['write_iops']}")

    # Context switches
    if "context_switches_per_sec" in a and "context_switches_per_sec" in b:
        print(f"\n  CONTEXT SWITCHES:")
        print(f"    {'per sec':>10}: {delta(a['context_switches_per_sec'], b['context_switches_per_sec'], '')}")

    # Process count
    print(f"\n  PROCESSES:")
    print(f"    {'total':>10}: {a['process_count']} vs {b['process_count']}")
    print(f"    {'python':>10}: {a['python_processes']} vs {b['python_processes']}")
    print(f"    {'CK alive':>10}: {a['ck_on_7777']} vs {b['ck_on_7777']}")


def main():
    print("=" * 60)
    print("  CK A/B TEST -- Comprehensive OS Stats")
    print("  Gaming + Streaming Measurement")
    print("=" * 60)

    # Phase A: CK ON (whatever state it's in now)
    print("\n>>> PHASE A: Measuring current state (CK ON if running)...")
    phase_a = run_phase("A (CK ON)", PHASE_DURATION, SAMPLE_INTERVAL)

    # Print Phase A results
    print(f"\n  Phase A Results:")
    print(json.dumps(phase_a, indent=2))

    # Kill CK for Phase B
    print("\n>>> Killing all Python processes for Phase B...")
    killed = kill_all_python()
    print(f"  Killed {killed} python processes")
    time.sleep(3)

    # Triple verify
    for check in range(3):
        time.sleep(1)
        procs = check_python_processes()
        port = check_ck_running()
        print(f"  Verify {check+1}/3: Python procs={len(procs)}, Port 7777={port}")
        if procs:
            print("  WARNING: Zombie processes found, killing again...")
            kill_all_python()
            time.sleep(2)

    # Phase B: CK OFF
    print("\n>>> PHASE B: Measuring with CK OFF...")
    phase_b = run_phase("B (CK OFF)", PHASE_DURATION, SAMPLE_INTERVAL)

    # Print Phase B results
    print(f"\n  Phase B Results:")
    print(json.dumps(phase_b, indent=2))

    # Comparison
    print_comparison(phase_a, phase_b)

    # Save results
    results = {"phase_a": phase_a, "phase_b": phase_b, "timestamp": time.time()}
    outpath = os.path.join(os.path.dirname(__file__), "ab_results.json")
    with open(outpath, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  Results saved to: {outpath}")

    print(f"\n{'='*60}")
    print(f"  A/B TEST COMPLETE")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
