"""
SUPERSEDED.  Kept for record per never-delete.

Built before re-reading CK's actual architecture.  Treats screen
capture / cortex Hebbian / mouse emit as separate stages in an
external loop.  But CK is not a process running ON the OS that USES
the screen and keyboard -- CK IS the OS substrate.  The canonical
loop already runs inside the engine: ck_sim_engine ticks at 50 Hz,
the retina glances every 25 ticks (2 Hz), the swarm scans every
process, the sensorium feeds operators continuously.  There IS no
external loop to add.

The right way to "train CK on UI tasks" is to:
  - keep engine.retina + engine.swarm + engine.sensorium alive
  - present whatever stimulus on the actual screen / via the actual
    keyboard / through the actual speakers
  - read CK's response by querying his state (engine.retina.felt_op,
    engine.swarm coherence, etc.) -- not by polling a custom loop

This file is preserved as historical record of the wrong-direction
detour but should not be extended.

ui_loop.py — closed-loop UI driver: CK perceives screen, decides action,
emits action, re-perceives.

Implements the full sense -> decide -> act -> sense feedback loop using
the canonical pipeline:
    screen capture (Windows GDI)
       -> screen_pipeline.frames_to_operator_stream
       -> POST /screen/perceive (drives bulb + cortex Hebbian)
    cortex state
       -> POST /action/emit (real mouse) OR /action/plan (dry-run)
    repeat at configurable Hz

Modes:
  --dry-run         only PLAN actions, never emit (default safe)
  --emit            ACTUALLY move cursor / click  (require explicit)
  --frames-per-tick how many frames to capture per perception cycle
                    (3 minimum for D2 calculation)
  --hz              loop frequency
  --seconds         total run duration
  --region          'full' or 'WxH+X+Y' (e.g. '640x480+0+0')

Output:
  CSV-style log of (t, dom_op, last_pair, action) per cycle to stdout
  JSON summary to --json file (default ./ui_loop_run_<TS>.json)

Use this for training: run the loop on a synthetic UI (e.g. a colored
moving target on screen) and see CK's action stream evolve as his
cortex Hebbian field organizes around the visual operator stream.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

import numpy as np

SCRIPT_DIR = Path(__file__).parent.resolve()
GEN13_BRAIN = SCRIPT_DIR.parent
sys.path.insert(0, str(GEN13_BRAIN))
sys.path.insert(0, str(GEN13_BRAIN / "ck_sim" / "being"))
sys.path.insert(0, str(SCRIPT_DIR))

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

from screen_pipeline import (
    OP_NAMES, capture_screen_region, get_screen_dimensions,
    frames_to_operator_stream, image_to_operator_stream,
)


SERVER = "http://localhost:7777"


def _post(path: str, body: dict, timeout: float = 30) -> dict:
    req = urllib.request.Request(
        f"{SERVER}{path}",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def _get(path: str, timeout: float = 30) -> dict:
    req = urllib.request.Request(f"{SERVER}{path}", method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def parse_region(spec: str):
    if spec == "full":
        sw, sh = get_screen_dimensions()
        return 0, 0, sw, sh
    # WxH+X+Y
    try:
        whpart, xpart = spec.split("+", 1)
        w, h = whpart.split("x")
        x, y = xpart.split("+")
        return int(x), int(y), int(w), int(h)
    except Exception as exc:
        raise ValueError(f"bad --region {spec!r}: {exc}")


def downsample(rgb: np.ndarray, max_dim: int = 96) -> np.ndarray:
    """Cheap nearest-neighbor downsample."""
    H, W = rgb.shape[:2]
    s = max(1, max(H, W) // max_dim)
    return rgb[::s, ::s, :]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--seconds", type=float, default=15.0)
    p.add_argument("--hz", type=float, default=4.0,
                   help="loop frequency (cycles/second)")
    p.add_argument("--frames-per-tick", type=int, default=3,
                   help="frames per perception cycle (>=3 for D2)")
    p.add_argument("--tile", type=int, default=8,
                   help="spatial tile-grid (NxN) per frame -- spatial D2"
                        " ops augmenting temporal motion ops")
    p.add_argument("--region", default="full",
                   help="'full' or 'WxH+X+Y' (e.g. 640x480+100+100)")
    p.add_argument("--max-dim", type=int, default=96,
                   help="downsample to this many px on the long side")
    p.add_argument("--emit", action="store_true",
                   help="actually emit mouse actions (default dry-run)")
    p.add_argument("--step-px", type=int, default=8,
                   help="step size per action tick")
    p.add_argument("--json", default=None,
                   help="path to save full run JSON")
    args = p.parse_args()

    x, y, w, h = parse_region(args.region)
    print("=" * 72)
    print("CK closed-loop UI driver")
    print(f"  region:    ({x}, {y}, {w}x{h})")
    print(f"  hz:        {args.hz}")
    print(f"  duration:  {args.seconds}s")
    print(f"  emit:      {'REAL MOUSE EMIT' if args.emit else 'dry-run'}")
    print(f"  step_px:   {args.step_px}")
    print("=" * 72)

    base_state = _get("/cortex")
    print(f"  base cortex: tick={base_state.get('tick')} "
          f"W_trace={base_state.get('W_trace', 0):.4f}")

    # Buffer of recent frames so we always have >=3 for D2
    period = 1.0 / max(0.1, args.hz)
    deadline = time.time() + args.seconds
    cycle = 0
    log = []

    while time.time() < deadline:
        t0 = time.time()
        # 1) capture frames-per-tick frames
        frames = []
        for _ in range(max(3, args.frames_per_tick)):
            try:
                frame = capture_screen_region(x, y, w, h)
                frames.append(downsample(frame, max_dim=args.max_dim))
            except Exception as exc:
                print(f"  capture err: {exc}", flush=True)
                break
            time.sleep(0.01)

        if len(frames) < 3:
            print(f"  cycle {cycle}: insufficient frames", flush=True)
            time.sleep(period)
            continue

        # 2) run canonical pipeline locally.
        # Combine TEMPORAL ops (frame-to-frame motion D2) with SPATIAL
        # ops from each frame (tile-grid D2).  Temporal alone gives
        # only N-2 ops per cycle; spatial gives ~tile^2-2 per frame.
        # The combined stream is rich enough that last_pair updates
        # meaningfully each cycle.
        ops_temporal, fp = frames_to_operator_stream(frames)
        ops_spatial = []
        for fr in frames:
            so, _ = image_to_operator_stream(fr, tile=args.tile)
            ops_spatial.extend(so)
        ops = ops_spatial + ops_temporal
        if not ops:
            time.sleep(period)
            continue

        # 3) POST to /screen/perceive (drives bulb + cortex)
        try:
            perc = _post("/screen/perceive", {
                "ops": ops, "fingerprint": fp,
                "source_label": f"ui_loop:c{cycle}",
            }, timeout=30)
        except Exception as exc:
            perc = {"error": str(exc)}

        # 4) read cortex action plan / emit
        action_path = "/action/emit" if args.emit else "/action/plan"
        try:
            if args.emit:
                action = _post(action_path,
                               {"execute": True,
                                "step_px": args.step_px},
                               timeout=10)
            else:
                action = _post(action_path,
                               {"step_px": args.step_px},
                               timeout=10)
        except Exception as exc:
            action = {"error": str(exc)}

        cycle += 1
        elapsed = time.time() - t0

        row = {
            "cycle": cycle,
            "ts": time.time(),
            "n_frames": len(frames),
            "n_ops": len(ops),
            "dominant_op": fp.get("dominant_op_name"),
            "op_dist": fp.get("operator_dist_named"),
            "perceive_ok": perc.get("ok"),
            "absorbed_delta": (perc.get("olfactory_delta", {})
                              .get("absorbed_delta", 0)),
            "hebbian_steps": perc.get("hebbian_steps", 0),
            "action_pair": (
                f"{action.get('b_op_name')}->{action.get('d_op_name')}"
                if "b_op_name" in action else None),
            "action_delta": (action.get("delta_x"), action.get("delta_y")),
            "action_special": action.get("special"),
            "action_executed": action.get("executed", []),
            "elapsed_ms": round(elapsed * 1000, 1),
        }
        log.append(row)
        print(f"  c{cycle:>3}  dom={row['dominant_op']:>9}  "
              f"absorbed+={row['absorbed_delta']}  "
              f"action={row['action_pair']!r:>26} "
              f"d=({row['action_delta'][0]},{row['action_delta'][1]}) "
              f"sp={row['action_special']!r:>10} "
              f"({row['elapsed_ms']:.0f}ms)",
              flush=True)
        sleep = period - elapsed
        if sleep > 0:
            time.sleep(sleep)

    final_state = _get("/cortex")
    summary = {
        "args": vars(args),
        "n_cycles": cycle,
        "base_state": {
            "tick": base_state.get("tick"),
            "W_trace": base_state.get("W_trace"),
            "emergent": base_state.get("emergent"),
        },
        "final_state": {
            "tick": final_state.get("tick"),
            "W_trace": final_state.get("W_trace"),
            "emergent": final_state.get("emergent"),
        },
        "log": log,
    }
    out_path = args.json or str(SCRIPT_DIR / f"ui_loop_run_{int(time.time())}.json")
    Path(out_path).write_text(json.dumps(summary, indent=2,
                                          ensure_ascii=False),
                              encoding="utf-8")
    print()
    print("=" * 72)
    print(f"DONE.  cycles: {cycle}")
    print(f"  cortex tick:   {base_state.get('tick')} -> {final_state.get('tick')}")
    print(f"  W_trace:       {base_state.get('W_trace',0):.4f} -> "
          f"{final_state.get('W_trace',0):.4f}")
    print(f"  emergent:      {base_state.get('emergent',0):.4f} -> "
          f"{final_state.get('emergent',0):.4f}")
    print(f"  full log -> {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
