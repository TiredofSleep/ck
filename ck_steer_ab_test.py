"""
ck_steer_ab_test.py -- Does CK's steering actually improve the OS?

A/B test:
  Phase A (30s): snapshot baseline -- ctx_switches/s, per-core variance, process priorities
  Phase B (30s): same metrics after CK has been steering

Metrics:
  1. Context switch rate (ctx/s) -- lower is better (less scheduler thrash)
  2. Per-core CPU variance (std dev %) -- lower is better (more balanced)
  3. Process priority distribution -- how many moved off NORMAL

No engine code loaded. Pure psutil observation from the outside.
"""

import psutil
import time
import statistics
import os
import sys

SAMPLE_DURATION = 30   # seconds per phase
SAMPLE_INTERVAL = 1.0  # seconds between readings

WIN_PRIORITIES = {
    psutil.IDLE_PRIORITY_CLASS:          'IDLE',
    psutil.BELOW_NORMAL_PRIORITY_CLASS:  'BELOW_NORMAL',
    psutil.NORMAL_PRIORITY_CLASS:        'NORMAL',
    psutil.ABOVE_NORMAL_PRIORITY_CLASS:  'ABOVE_NORMAL',
    psutil.HIGH_PRIORITY_CLASS:          'HIGH',
    psutil.REALTIME_PRIORITY_CLASS:      'REALTIME',
}

SELF_PID = os.getpid()
CK_NAME  = 'python'  # CK's own process -- don't count its changes


def snapshot_priorities():
    """Return {pid: (name, priority_class_str)} for all accessible processes."""
    out = {}
    for proc in psutil.process_iter(['pid', 'name']):
        pid = proc.info['pid']
        if pid == SELF_PID:
            continue
        try:
            nice = proc.nice()
            label = WIN_PRIORITIES.get(nice, f'UNK({nice})')
            out[pid] = (proc.info['name'], label)
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass
    return out


def sample_phase(label, duration=SAMPLE_DURATION, interval=SAMPLE_INTERVAL):
    """Sample ctx_switches/s and per-core variance over `duration` seconds."""
    print(f"\n{'='*60}")
    print(f"  PHASE {label} -- sampling {duration}s ...")
    print(f"{'='*60}")

    ctx_rates   = []
    core_vars   = []
    prev_ctx    = psutil.cpu_stats().ctx_switches
    prev_t      = time.monotonic()

    ticks = int(duration / interval)
    for i in range(ticks):
        time.sleep(interval)

        # Context switch rate
        now_ctx = psutil.cpu_stats().ctx_switches
        now_t   = time.monotonic()
        dt      = now_t - prev_t
        rate    = (now_ctx - prev_ctx) / dt
        ctx_rates.append(rate)
        prev_ctx = now_ctx
        prev_t   = now_t

        # Per-core variance
        per_core = psutil.cpu_percent(percpu=True)
        var      = statistics.stdev(per_core) if len(per_core) > 1 else 0.0
        core_vars.append(var)

        sys.stdout.write(f"\r  t={i+1:3d}/{ticks}  ctx/s={rate:8.0f}  core_var={var:5.1f}%  ")
        sys.stdout.flush()

    print()
    return {
        'ctx_mean':  statistics.mean(ctx_rates),
        'ctx_std':   statistics.stdev(ctx_rates) if len(ctx_rates) > 1 else 0.0,
        'var_mean':  statistics.mean(core_vars),
        'var_std':   statistics.stdev(core_vars) if len(core_vars) > 1 else 0.0,
        'ctx_rates': ctx_rates,
        'core_vars': core_vars,
    }


def priority_distribution(snap):
    """Count processes per priority class."""
    dist = {}
    for pid, (name, label) in snap.items():
        dist[label] = dist.get(label, 0) + 1
    return dist


def priority_diff(before, after):
    """Which processes changed priority?"""
    changed = []
    for pid in set(before) & set(after):
        b_name, b_pri = before[pid]
        a_name, a_pri = after[pid]
        if b_pri != a_pri:
            changed.append((pid, b_name, b_pri, a_pri))
    return sorted(changed, key=lambda x: x[1])


def main():
    print("\n" + "="*60)
    print("  CK STEERING A/B TEST")
    print("  Does CK improve the OS in domains he touches?")
    print("="*60)

    # ── Baseline priority snapshot ──
    print("\n[A] Capturing baseline process priorities...")
    snap_before = snapshot_priorities()
    dist_before = priority_distribution(snap_before)
    print(f"    Processes visible: {len(snap_before)}")
    for label, count in sorted(dist_before.items(), key=lambda x: -x[1]):
        print(f"      {label:16s}: {count:4d}")

    # ── Phase A: baseline metrics ──
    phase_a = sample_phase('A (BASELINE)')

    # ── Post-steer priority snapshot ──
    print("\n[B] Capturing post-steer process priorities...")
    snap_after = snapshot_priorities()
    dist_after  = priority_distribution(snap_after)
    print(f"    Processes visible: {len(snap_after)}")
    for label, count in sorted(dist_after.items(), key=lambda x: -x[1]):
        print(f"      {label:16s}: {count:4d}")

    # ── Phase B: steered metrics ──
    phase_b = sample_phase('B (CK STEERED)')

    # ══════════════════════════════════════════
    #  RESULTS
    # ══════════════════════════════════════════
    print("\n" + "="*60)
    print("  RESULTS")
    print("="*60)

    ctx_delta  = phase_b['ctx_mean'] - phase_a['ctx_mean']
    ctx_pct    = 100 * ctx_delta / max(phase_a['ctx_mean'], 1)
    var_delta  = phase_b['var_mean'] - phase_a['var_mean']
    var_pct    = 100 * var_delta / max(phase_a['var_mean'], 1)

    print(f"\n  Context switches/s:")
    print(f"    Baseline:  {phase_a['ctx_mean']:10.0f}  +/- {phase_a['ctx_std']:.0f}")
    print(f"    Steered:   {phase_b['ctx_mean']:10.0f}  +/- {phase_b['ctx_std']:.0f}")
    ctx_sign = 'IMPROVED' if ctx_delta < 0 else 'WORSE' if ctx_delta > 0 else 'FLAT'
    print(f"    Delta:     {ctx_delta:+.0f}  ({ctx_pct:+.1f}%)  {ctx_sign}")

    print(f"\n  Per-core CPU variance (std dev %):")
    print(f"    Baseline:  {phase_a['var_mean']:8.2f}%  +/- {phase_a['var_std']:.2f}")
    print(f"    Steered:   {phase_b['var_mean']:8.2f}%  +/- {phase_b['var_std']:.2f}")
    var_sign = 'IMPROVED' if var_delta < 0 else 'WORSE' if var_delta > 0 else 'FLAT'
    print(f"    Delta:     {var_delta:+.2f}%  ({var_pct:+.1f}%)  {var_sign}")

    print(f"\n  Priority distribution shift:")
    all_labels = sorted(set(dist_before) | set(dist_after))
    for label in all_labels:
        b = dist_before.get(label, 0)
        a = dist_after.get(label, 0)
        arrow = f'  {b:4d} -> {a:4d}  ({a-b:+d})'
        print(f"    {label:16s}: {arrow}")

    changed = priority_diff(snap_before, snap_after)
    print(f"\n  Processes CK re-prioritized: {len(changed)}")
    for pid, name, b_pri, a_pri in changed[:20]:
        print(f"    [{pid:6d}] {name:30s}  {b_pri} → {a_pri}")
    if len(changed) > 20:
        print(f"    ... and {len(changed)-20} more")

    # ── Verdict ──
    print("\n" + "="*60)
    improvements = sum([ctx_delta < -100, var_delta < -0.5])
    print(f"  VERDICT: {improvements}/2 metrics improved")
    if improvements == 2:
        print("  [+] CK improves both scheduler efficiency AND load balance")
    elif improvements == 1:
        print("  ~ CK improves one metric (partial benefit)")
    else:
        print("  ✗ No measurable improvement in these conditions")
        print("    (CK may need more hot processes to steer, or system is already balanced)")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
