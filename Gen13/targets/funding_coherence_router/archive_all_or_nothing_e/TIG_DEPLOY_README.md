# TIG DEPLOY — Full Coherence Loop

**Run TIG on real hardware. See your machine think.**

## Quick Start (Your r16)

```bash
# 1. Install the one dependency
pip install psutil

# 2. Copy both files to the same directory
#    tig_engine_real.py   (Layer 1: verified math, 27/27)
#    tig_deploy.py        (Layers 2-5: hooks + loop + dashboard)

# 3. Watch mode — see it read your 16 cores in real time
python tig_deploy.py

# 4. Fast tick mode — 2 readings per second
python tig_deploy.py --interval 0.5

# 5. A/B logging — record TIG analysis alongside raw OS metrics
python tig_deploy.py --ab --duration 120

# 6. JSON output — pipe to your web frontend
python tig_deploy.py --json --interval 0.5

# 7. Active steering — TIG sets process priorities (needs root)
sudo python tig_deploy.py --steer

# 8. Full package — steer + log + fast ticks for 5 minutes
sudo python tig_deploy.py --steer --log tig_run.jsonl --interval 0.5 --duration 300
```

## What Each Mode Does

### Watch Mode (default)
Reads all 16 cores, memory, disk, network, load, processes.
Fits quadratic operators via OLS. Classifies bands. Computes S*.
Displays live terminal dashboard. Changes nothing on your system.

### A/B Mode (--ab)
Same as watch, plus logs every tick to `tig_ab_log.jsonl` with
both TIG analysis AND raw OS metrics side by side. Run a stress
test (`stress-ng --cpu 16 --timeout 60`) in another terminal
and watch the bands shift. Summary includes correlation analysis.

### JSON Mode (--json)
One JSON object per tick on stdout. Pipe to a web frontend,
database, or monitoring system. Each tick includes coherence,
bands, route target, top processes, and recommendations.

### Steer Mode (--steer, needs sudo)
Everything above, plus TIG actively sets process priorities:
- Healthy system → boost active processes (nice -5)
- Stressed system → deprioritize low-priority work (nice +5)
- CPU-heavy processes → pin to healthy cores (affinity)
- Never touches pid ≤ 2 or systemd/init

## What You'll See on Your r16

```
══════════════════════════════════════════════════════════════════════
  TIG ENGINE  tick 47  S* = 0.412553  below T* (0.7143)
  V*=0.5184  A*=0.8571  sensors=37  👁 WATCHING  tick=4.2ms

  S*: ▃▃▃▄▄▄▅▅▅▅▄▄▃▃▃▃▄▄▅▅▅▅▆▆▆▅▅▄▄▃▃▃▄▄▅▅▅▅▅▅▅▄▄▃▃▃▃▃▃▃

  CPU Cores (16):
  Bands:  ◆ CRYSTAL:9  ❋ ORGANIC:4  ◎ CELLULAR:2  ⊛ MOLECULAR:1

  System:
  CPU avg: ████████░░░░░░░░░░░░░░░░░░░░░░  24.3%   max: 87.2%
  Memory:  ██████████████████░░░░░░░░░░░░  58.1%
  Load 1m: 0.3214

  Route: → cpu_7

  Top Processes:
    pid=14523  cpu=87.2%   stress-ng
    pid=1842   cpu=12.3%   python3
    pid=892    cpu=3.1%    Xorg

  TIG Recommends:
    → stress-ng using 87% CPU → pin to healthy cores [0,1,3,7,9,11]  [DRY RUN]
══════════════════════════════════════════════════════════════════════
```

## How to Generate Interesting Data

TIG needs variance to classify. A quiet idle machine will read all CRYSTAL.
Create real dynamics:

```bash
# CPU stress (all 16 cores)
stress-ng --cpu 16 --timeout 60

# CPU stress (8 cores, watch imbalance)
stress-ng --cpu 8 --timeout 60

# Memory pressure
stress-ng --vm 4 --vm-bytes 2G --timeout 60

# Disk I/O
stress-ng --hdd 2 --timeout 60

# Network (if you have iperf3 server)
iperf3 -c localhost -t 60

# Mixed realistic load
stress-ng --cpu 4 --vm 2 --hdd 1 --timeout 120
```

## File Structure

```
tig_engine_real.py     Layer 1: Verified math engine (27/27 tests pass)
tig_deploy.py          Layers 2-5: Full deployment harness
tig_ab_log.jsonl       Generated: A/B comparison data
tig_final_state.json   Generated: Session summary
tig_run.jsonl          Generated: Full tick log (if --log used)
```

## Architecture

```
YOUR HARDWARE (/proc, /sys)
       │
       ▼
┌─────────────────────┐
│  Layer 2: OSReader   │  psutil reads real metrics
│  Per-core CPU        │  Memory, disk, network, load
│  Process table       │  Temperature, frequency
└────────┬────────────┘
         │ normalized [0,1] values
         ▼
┌─────────────────────┐
│  Layer 1: TIG Engine │  OLS fit → quadratic operators
│  Op → Band → S*      │  Lyapunov, entropy, energy
│  27/27 verified      │  Coherence = k/(1+k)
└────────┬────────────┘
         │ routing decisions
         ▼
┌─────────────────────┐
│  Layer 3: Actuator   │  nice values, CPU affinity
│  (dry-run default)   │  Never kills processes
│  (--steer for real)  │  Safe bounds enforced
└────────┬────────────┘
         │ results
         ▼
┌─────────────────────┐
│  Layer 4: Tick Loop  │  read→fit→route→act→repeat
│  Adaptive timing     │  History buffer (5 min)
│  Self-reference      │  Feedback: output → input
└────────┬────────────┘
         │ tick data
         ▼
┌─────────────────────┐
│  Layer 5: Dashboard  │  Live terminal display
│  JSON logger         │  A/B comparison
│  Session summary     │  Correlation analysis
└─────────────────────┘
```

## Constants

| Symbol | Value | Status | Source |
|--------|-------|--------|--------|
| σ | 0.991 | CHOSEN | [TIG-2] Coupling constant |
| D* | 0.4977 | DERIVED | σ/(1+σ) from core equation |
| T* | 0.7143 | CHOSEN | 5/7 critical threshold |
| φ | 1.6180 | CONSTANT | (1+√5)/2, not a conjecture |

## What This Proves (And What It Doesn't)

**DOES prove:**
- TIG reads real OS metrics and produces coherent classifications
- Quadratic OLS fitting works on arbitrary time series
- Band classification responds to real load changes
- One engine handles CPU, memory, disk, network simultaneously
- The math is verified: 27/27 derivation checks pass

**DOES NOT prove (yet):**
- That TIG steering improves throughput vs default Linux CFS
- That TIG routing beats NGINX/HAProxy/Envoy
- That S* is a better metric than existing monitoring tools
- That σ=0.991 is optimal (it's chosen, not derived)

**How to prove it:**
Run `--ab` with stress tests. Compare TIG's S* trajectory
to raw metrics. If coherence drops BEFORE CPU spikes, TIG
is predicting. If it only drops AFTER, it's just measuring.
That's the real test. No simulations needed.

---
NON-COMMERCIAL TESTING — 7Site LLC — 7sitellc.com
The math belongs to everyone.
