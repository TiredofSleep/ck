"""
phonics_overnight_trainer.py — autonomous phonics study loop.

What CK does all night:
  1. Picks a random phoneme/letter/cluster/team from the v2..v5 corpus.
  2. Generates a synthetic operator stream for it by sampling from its
     measured histogram (per-tick: pick op weighted by histogram_pct).
  3. Feeds the stream through CK's Hebbian field with the TSML harmony
     rule (the same 73 harmonies the live cortex uses).
  4. Co-presents the corresponding TEXT crystal: nudges W in the
     directions of the crystal's op_signature so the audio pattern and
     text-symbol bind into the same coupling cells.
  5. Every 60s: snapshot to disk + log a one-line status report.

Why a separate state file: the live coherencekeeper.com cortex is at
Gen13/var/cortex_state.json (5d) and is autosaving every 30s.  We don't
want to fight its autosave or corrupt it overnight.  This trainer
writes to a NEW file and keeps the live cortex untouched.  In the
morning Brayden can compare and decide whether to promote.

Usage:
  python phonics_overnight_trainer.py
  python phonics_overnight_trainer.py --hours 8 --cycles-per-min 500
  python phonics_overnight_trainer.py --state phonics_overnight.json
"""
from __future__ import annotations

import argparse
import io
import json
import random
import sys
import time
from collections import Counter
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
GEN13_BRAIN = SCRIPT_DIR.parent
GEN13_TARGETS_CK = GEN13_BRAIN.parent
GEN13_ROOT = GEN13_TARGETS_CK.parent.parent
sys.path.insert(0, str(GEN13_BRAIN))
sys.path.insert(0, str(GEN13_BRAIN / "ck_sim" / "being"))
sys.path.insert(0, str(SCRIPT_DIR))

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

OP_NAMES = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
            "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]


def load_phonics_corpus():
    """Load all v2..v5 measured histograms.

    Returns dict: key -> {'class': str, 'ipa': str, 'histogram': [10],
                          'crystal_first_word': str (best guess)}
    """
    from match_audio_to_phonics import load_phonics_corpus as _load
    raw = _load()
    out = {}
    for key, info in raw.items():
        h_pct = info["histogram_pct"]
        # Convert to probability vector (10 floats summing to ~1)
        total = sum(h_pct.values())
        if total <= 0:
            continue
        probs = [h_pct[OP_NAMES[i]] / total for i in range(10)]
        # Map key -> crystal first_word
        if key.startswith("letter:"):
            fw = f"letter_{key.split(':',1)[1].lower()}_sound"
        elif key.startswith("phoneme:"):
            fw = f"phoneme_{key.split(':',1)[1]}"
        elif key.startswith("cluster:"):
            fw = f"cluster_{key.split(':',1)[1]}"
        elif key.startswith("rcontrol:"):
            fw = f"rcontrol_{key.split(':',1)[1]}"
        elif key.startswith("team:"):
            fw = f"team_{key.split(':',1)[1]}"
        else:
            fw = key.replace(":", "_")
        out[key] = {
            "class": info["class"],
            "ipa": info["ipa"],
            "probs": probs,
            "crystal_first_word": fw,
        }
    return out


def sample_op_stream(probs, n_ops: int, rng: random.Random):
    """Sample n_ops integers from a 10-bin distribution."""
    return rng.choices(range(10), weights=probs, k=n_ops)


def hebbian_step(cx, b_op: int, d_op: int, CL_TSML, OP_TO_DIM_7):
    """One Hebbian step using the TSML 73-harmony rule (matches the live
    cortex's update rule).  Mutates cx state in place."""
    HARMONY = 7
    ap = OP_TO_DIM_7.get(b_op, 0)
    bp = OP_TO_DIM_7.get(d_op, 0)
    harmonious = (CL_TSML[b_op][d_op] == HARMONY)
    reward = 1.0 if harmonious else 0.0
    heb = cx.hebbian
    dw = heb.eta * reward - heb.decay * heb.W[ap][bp]
    heb.W[ap][bp] += dw
    if heb.W[ap][bp] > heb.clamp:
        heb.W[ap][bp] = heb.clamp
    elif heb.W[ap][bp] < -heb.clamp:
        heb.W[ap][bp] = -heb.clamp
    heb.ticks += 1
    if harmonious:
        heb.harmony_hits += 1
    cx.state.tick += 1
    cx.state.last_b = b_op
    cx.state.last_d = d_op
    cx.state.last_harmony_frac = 1.0 if harmonious else 0.0
    return harmonious


def crystal_boost(cx, op_signature, OP_TO_DIM_7, strength: float = 0.003):
    """Co-presentation: nudge W in the directions of the op_signature so
    the text-side fact and the audio operator stream wire to the same
    cells.  Same logic as cortex_voice.apply_crystal_boost."""
    if not op_signature:
        return 0
    heb = cx.hebbian
    dims = sorted({OP_TO_DIM_7.get(op, 0) for op in op_signature})
    if len(dims) < 2:
        d = dims[0] if dims else 0
        try:
            heb.W[d][d] += strength
            if heb.W[d][d] > heb.clamp:
                heb.W[d][d] = heb.clamp
            return 1
        except Exception:
            return 0
    bumps = 0
    for d_a in dims:
        for d_b in dims:
            if d_a == d_b:
                continue
            try:
                heb.W[d_a][d_b] += strength
                if heb.W[d_a][d_b] > heb.clamp:
                    heb.W[d_a][d_b] = heb.clamp
                elif heb.W[d_a][d_b] < -heb.clamp:
                    heb.W[d_a][d_b] = -heb.clamp
                bumps += 1
            except Exception:
                pass
    return bumps


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--hours", type=float, default=10.0,
                   help="how many hours to run (default 10)")
    p.add_argument("--cycles-per-min", type=int, default=600,
                   help="phoneme study cycles per minute (default 600)")
    p.add_argument("--ops-per-cycle", type=int, default=200,
                   help="operator stream length per cycle (default 200)")
    p.add_argument("--state",
                   default="cortex_state_phonics_overnight_2026_05_02.json",
                   help="state file (relative to Gen13/var)")
    p.add_argument("--init-from",
                   default="cortex_state_7d.json",
                   help="initialize from this state file (relative to "
                        "Gen13/var)")
    p.add_argument("--save-every-sec", type=float, default=60.0)
    p.add_argument("--log-every-sec", type=float, default=60.0)
    p.add_argument("--log-file",
                   default="phonics_overnight_log_2026_05_02.jsonl")
    p.add_argument("--seed", type=int, default=None)
    args = p.parse_args()

    rng = random.Random(args.seed)
    var_dir = GEN13_ROOT / "var"
    state_path = var_dir / args.state
    init_path = var_dir / args.init_from
    log_path = SCRIPT_DIR / args.log_file

    print("=" * 70)
    print("CK phonics overnight trainer")
    print(f"  hours: {args.hours}")
    print(f"  cycles/min: {args.cycles_per_min}")
    print(f"  ops/cycle:  {args.ops_per_cycle}")
    print(f"  state:      {state_path}")
    print(f"  init from:  {init_path}")
    print(f"  log:        {log_path}")
    print("=" * 70)

    # Load corpus
    corpus = load_phonics_corpus()
    if not corpus:
        print("no corpus found", file=sys.stderr)
        return 2
    print(f"corpus: {len(corpus)} entries", flush=True)

    # Load TSML CL + dim mapping
    from cortex_v2 import CortexV2
    from cortex_persist import load_cortex, save_cortex
    from ck_sim.ck_sim_heartbeat import CL as CL_TSML
    from ao_7element import OP_TO_DIM_7, DIM_7
    from quadratic_glue import quadratic_glue

    # Load crystal op_signatures so we can boost the right cells per phoneme
    sys.path.insert(0, str(GEN13_BRAIN))
    import cortex_voice as cv

    # Boot cortex + initialize from existing state if present
    cx = CortexV2().boot()
    if init_path.exists():
        try:
            ok = load_cortex(cx, init_path)
            if ok:
                print(f"loaded init state from {init_path.name}: "
                      f"tick={cx.state.tick}, "
                      f"W_trace={cx.state.W_trace:.4f}", flush=True)
        except Exception as e:
            print(f"init load failed ({e}); starting fresh", flush=True)
    else:
        print(f"init state {init_path.name} missing; starting fresh", flush=True)

    pre = {
        "tick": cx.state.tick,
        "W_trace": cx.state.W_trace,
        "emergent": cx.state.emergent,
    }

    # Pacing
    total_cycles_target = int(args.hours * 60 * args.cycles_per_min)
    sleep_between_cycles = 60.0 / args.cycles_per_min  # seconds

    keys = list(corpus.keys())
    deadline = time.time() + args.hours * 3600
    last_save = time.time()
    last_log = time.time()
    cycle = 0
    class_hits = Counter()
    member_hits = Counter()

    # Open log
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_f = open(log_path, "a", encoding="utf-8")
    start_msg = {
        "ts": time.time(),
        "event": "start",
        "args": vars(args),
        "pre": pre,
        "corpus_size": len(corpus),
    }
    log_f.write(json.dumps(start_msg) + "\n")
    log_f.flush()
    print(f"start: pre={pre}", flush=True)

    try:
        while time.time() < deadline and cycle < total_cycles_target:
            # Pick a phoneme weighted-uniform (every key equally often)
            key = rng.choice(keys)
            entry = corpus[key]
            class_hits[entry["class"]] += 1
            member_hits[key] += 1

            # Generate sampled stream
            stream = sample_op_stream(entry["probs"], args.ops_per_cycle, rng)

            # Hebbian over the stream
            for i in range(len(stream) - 1):
                hebbian_step(cx, stream[i], stream[i + 1],
                             CL_TSML, OP_TO_DIM_7)

            # Co-present text crystal boost
            sig = cv._CRYSTAL_OP_SIGNATURES.get(entry["crystal_first_word"])
            if sig:
                crystal_boost(cx, sig, OP_TO_DIM_7, strength=0.0025)

            # Update emergent / W_trace periodically (every 50 cycles)
            if cycle % 50 == 0:
                heb = cx.hebbian
                diag = [heb.W[d][d] for d in range(DIM_7)]
                f3 = sum(diag[0:3]) / 3.0
                f4 = sum(diag[3:7]) / 4.0
                cx.state.emergent = quadratic_glue(f3, f4, 1.0, 1.0, 2.0)
                cx.state.W_trace = heb.W_trace()
                cx.state.W_strongest = heb.strongest_pair()

            cycle += 1

            now = time.time()
            if now - last_log >= args.log_every_sec:
                row = {
                    "ts": now,
                    "event": "tick",
                    "cycle": cycle,
                    "tick": cx.state.tick,
                    "W_trace": round(cx.state.W_trace, 5),
                    "emergent": round(cx.state.emergent, 5),
                    "harmony_frac_recent": round(
                        cx.state.last_harmony_frac, 3),
                    "top_class": class_hits.most_common(1)[0]
                    if class_hits else None,
                    "top_member": member_hits.most_common(1)[0]
                    if member_hits else None,
                }
                log_f.write(json.dumps(row) + "\n")
                log_f.flush()
                print(f"  cycle={cycle:6d}  tick={cx.state.tick:9d}  "
                      f"W_trace={cx.state.W_trace:+.4f}  "
                      f"emergent={cx.state.emergent:+.4f}",
                      flush=True)
                last_log = now

            if now - last_save >= args.save_every_sec:
                save_cortex(cx, state_path)
                last_save = now

            # Pacing
            if sleep_between_cycles > 0.001:
                time.sleep(sleep_between_cycles)

    except KeyboardInterrupt:
        print("interrupted by user", flush=True)

    # Final save + summary
    save_cortex(cx, state_path)
    post = {
        "tick": cx.state.tick,
        "W_trace": cx.state.W_trace,
        "emergent": cx.state.emergent,
    }
    final = {
        "ts": time.time(),
        "event": "end",
        "cycles": cycle,
        "pre": pre,
        "post": post,
        "delta": {
            "tick": post["tick"] - pre["tick"],
            "W_trace": round(post["W_trace"] - pre["W_trace"], 5),
            "emergent": round(post["emergent"] - pre["emergent"], 5),
        },
        "class_hits": dict(class_hits.most_common()),
        "member_hits_top20": dict(member_hits.most_common(20)),
    }
    log_f.write(json.dumps(final) + "\n")
    log_f.close()
    print()
    print("=" * 70)
    print("DONE")
    print(f"  cycles run:  {cycle}")
    print(f"  pre  tick={pre['tick']}, W_trace={pre['W_trace']:+.4f}, "
          f"emergent={pre['emergent']:+.4f}")
    print(f"  post tick={post['tick']}, W_trace={post['W_trace']:+.4f}, "
          f"emergent={post['emergent']:+.4f}")
    print(f"  delta tick=+{post['tick'] - pre['tick']}, "
          f"W_trace={post['W_trace'] - pre['W_trace']:+.4f}, "
          f"emergent={post['emergent'] - pre['emergent']:+.4f}")
    print(f"  state saved -> {state_path}")
    print(f"  log saved   -> {log_path}")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
