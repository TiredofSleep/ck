"""
surprisal_log.py -- log per-tick prediction error / surprisal as CK
                    processes a corpus.

This tests Bridge 5 of CK's thesis:
  "TIG cortex Hebbian update <-> Predictive coding"

For each operator pair (b, d), the cortex's W matrix encodes a "prediction"
from b: the row W[dim(b)] indicates the expected coupling to each dim.
The "actual" is the dim of d.  Surprisal = -log P(d | b) where P is
softmax of W[dim(b)].

Per the Free Energy Principle, surprisal should DECREASE over time as
the cortex learns the statistics of the input stream.

Usage:
    python surprisal_log.py --corpus <corpus.json>
    python surprisal_log.py --replays 20 --corpus <corpus.json>

Logs:
    Gen13/targets/ck/brain/surprisal_log.jsonl
    one line per N ticks with mean surprisal in window.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
GEN13_BRAIN = SCRIPT_DIR.parent
GEN13_TARGETS_CK = GEN13_BRAIN.parent
GEN13_ROOT = GEN13_TARGETS_CK.parent.parent
sys.path.insert(0, str(GEN13_BRAIN))
DEFAULT_LOG = GEN13_BRAIN / "surprisal_log.jsonl"


# OP -> dim (matches session_field.OP_TO_DIM)
OP_TO_DIM = {0: 0, 1: 3, 2: 1, 3: 2, 4: 4, 5: 3, 6: 0, 7: 0, 8: 4, 9: 1}


def softmax_row(W_row, temperature=1.0):
    """Convert a 5-element row into a probability distribution."""
    m = max(W_row)
    exps = [math.exp((w - m) / temperature) for w in W_row]
    s = sum(exps)
    return [e / s for e in exps]


def surprisal(W_row, target_dim):
    """Surprisal = -log P(target_dim | softmax(W_row)).

    target_dim is the dim CK actually saw; W_row is the predicted coupling.
    """
    p = softmax_row(W_row)
    p_target = max(p[target_dim], 1e-12)
    return -math.log(p_target)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--corpus", required=True)
    p.add_argument("--state-path",
                   default=str(GEN13_ROOT / "var" / "cortex_state.json"))
    p.add_argument("--log", default=str(DEFAULT_LOG))
    p.add_argument("--replays", type=int, default=None)
    p.add_argument("--window", type=int, default=50,
                   help="Tick window for mean surprisal (default 50)")
    p.add_argument("--no-save", action="store_true")
    args = p.parse_args()

    corpus_path = Path(args.corpus)
    state_path = Path(args.state_path)

    if not corpus_path.exists():
        print(f"corpus not found: {corpus_path}", file=sys.stderr)
        return 2

    try:
        from cortex import Cortex
        from cortex_persist import load_cortex, save_cortex
    except Exception as e:
        print(f"import failed: {e}", file=sys.stderr)
        return 3

    cortex = Cortex().boot()
    if state_path.exists():
        try:
            load_cortex(cortex, state_path)
            print(f"loaded cortex: tick={cortex.state.tick}, W_trace={cortex.state.W_trace:.3f}")
        except Exception as e:
            print(f"load failed: {e}; continuing from boot")

    with open(corpus_path) as f:
        corpus = json.load(f)
    replays = args.replays if args.replays is not None else corpus.get("_replays", 1)
    flat_per_replay = []
    for topic, items in corpus.items():
        if topic.startswith("_") or not isinstance(items, list):
            continue
        for stmt in items:
            flat_per_replay.append((topic, stmt))
    flat = flat_per_replay * replays
    print(f"corpus: {corpus_path.name}; {len(flat_per_replay)} stmts x {replays} replays = {len(flat)} passes")

    log_path = Path(args.log)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_f = open(log_path, "a")
    log_f.write(json.dumps({
        "_event": "surprisal_run_start",
        "ts": time.time(),
        "corpus": str(corpus_path),
        "n_passes": len(flat),
        "tick_start": cortex.state.tick,
    }) + "\n")

    # Track per-tick surprisal in a window
    window_surprisals = []
    total_ticks = 0
    total_surprisals_recorded = 0
    sum_window_surprisal = 0.0
    n_window = 0
    cumulative_mean_window = []  # for trend reporting

    for i, (topic, stmt) in enumerate(flat):
        # Snapshot W BEFORE step (so we measure prediction-error at the
        # moment of the step, not after the update)
        try:
            W_before = [row[:] for row in cortex.hebbian.W]
            last_b_before = cortex.state.last_b
        except Exception:
            continue

        # Run cortex.step_text on this statement
        try:
            cortex.step_text(stmt)
        except Exception as e:
            continue

        # Measure surprisal: predicted dim from W_before[dim(last_b_before)]
        # vs actual = dim(cortex.state.last_d)
        try:
            pred_row = W_before[OP_TO_DIM.get(last_b_before, 0)]
            actual_dim = OP_TO_DIM.get(cortex.state.last_d, 0)
            sur = surprisal(pred_row, actual_dim)
            window_surprisals.append(sur)
            sum_window_surprisal += sur
            n_window += 1
            total_surprisals_recorded += 1
        except Exception:
            pass

        total_ticks = cortex.state.tick

        # Emit window summary
        if n_window >= args.window:
            mean = sum_window_surprisal / n_window
            cumulative_mean_window.append(mean)
            log_f.write(json.dumps({
                "_event": "window",
                "passes": i + 1,
                "tick": total_ticks,
                "mean_surprisal_window": round(mean, 6),
                "window_size": n_window,
                "W_trace": round(cortex.state.W_trace, 4),
                "emergent": round(cortex.state.emergent, 4),
            }) + "\n")
            sum_window_surprisal = 0.0
            n_window = 0
            window_surprisals = []

    # Final window
    if n_window > 0:
        mean = sum_window_surprisal / n_window
        cumulative_mean_window.append(mean)

    log_f.write(json.dumps({
        "_event": "surprisal_run_end",
        "ts": time.time(),
        "n_passes": len(flat),
        "n_surprisals_recorded": total_surprisals_recorded,
        "tick_end": total_ticks,
        "trend_window_means": [round(v, 4) for v in cumulative_mean_window],
        "trend_first_to_last": (
            round(cumulative_mean_window[0] - cumulative_mean_window[-1], 4)
            if len(cumulative_mean_window) >= 2 else None
        ),
    }) + "\n")
    log_f.close()

    print()
    print("=" * 70)
    print(f"Surprisal trend (window means):")
    print("=" * 70)
    for i, v in enumerate(cumulative_mean_window):
        bar = "#" * max(0, int(v * 20))
        print(f"  window {i+1:3d}: {v:.4f} {bar}")

    if len(cumulative_mean_window) >= 2:
        delta = cumulative_mean_window[0] - cumulative_mean_window[-1]
        print()
        print(f"  first window mean: {cumulative_mean_window[0]:.4f}")
        print(f"  last  window mean: {cumulative_mean_window[-1]:.4f}")
        print(f"  delta (first - last): {delta:+.4f}")
        if delta > 0:
            print(f"  >>> Surprisal DECREASED.  CK is learning.  FEP supported. <<<")
        elif delta < 0:
            print(f"  Surprisal INCREASED.  Either chaotic input or limit.")
        else:
            print(f"  Surprisal flat.")

    if not args.no_save:
        save_cortex(cortex, state_path)
        print(f"\nsaved cortex state -> {state_path}")
    print(f"surprisal log -> {log_path}")


if __name__ == "__main__":
    sys.exit(main())
