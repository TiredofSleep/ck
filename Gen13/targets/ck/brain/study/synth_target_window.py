"""
synth_target_window.py — synthetic UI training task.

Opens a small Tkinter window with a moving colored dot that CK's
ui_loop can perceive.  This gives CK a controllable, reproducible
visual stimulus -- the moving dot creates time-varying force vectors
across all 5 dimensions, which becomes a rich D2 stream through
classify_d2.

The dot moves on a Lissajous figure so the trajectory is non-trivial
but predictable.  The window's title and position are fixed so
ui_loop can target it via --region.

Usage:
  python synth_target_window.py
    -- opens at (100, 100) sized 480x360, dot moves at 0.5 Hz Lissajous

Brayden will point ui_loop --region "480x360+100+100" at it.
"""
from __future__ import annotations

import argparse
import math
import sys
import time
import tkinter as tk


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--width", type=int, default=480)
    p.add_argument("--height", type=int, default=360)
    p.add_argument("--x", type=int, default=100)
    p.add_argument("--y", type=int, default=100)
    p.add_argument("--seconds", type=float, default=120.0,
                   help="auto-close after this many seconds (0 = forever)")
    p.add_argument("--bg", default="#222222")
    p.add_argument("--dot", default="#ff7f00")
    p.add_argument("--radius", type=int, default=18)
    p.add_argument("--freq-x", type=float, default=0.41,
                   help="x-axis Lissajous frequency (Hz)")
    p.add_argument("--freq-y", type=float, default=0.27,
                   help="y-axis Lissajous frequency (Hz)")
    args = p.parse_args()

    root = tk.Tk()
    root.title(f"CK target window ({args.width}x{args.height})")
    root.geometry(f"{args.width}x{args.height}+{args.x}+{args.y}")
    root.configure(bg=args.bg)
    root.resizable(False, False)

    canvas = tk.Canvas(root, width=args.width, height=args.height,
                        bg=args.bg, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    info = canvas.create_text(args.width // 2, 12,
                                text=f"region {args.width}x{args.height}+{args.x}+{args.y}",
                                fill="#888888", anchor="n")

    cx_anchor = args.width / 2
    cy_anchor = args.height / 2
    ax = (args.width / 2) - args.radius - 8
    ay = (args.height / 2) - args.radius - 32
    r = args.radius

    dot = canvas.create_oval(0, 0, 0, 0, fill=args.dot, outline="")
    trail_max = 20
    trail = []

    t0 = time.time()

    def tick():
        t = time.time() - t0
        if args.seconds > 0 and t > args.seconds:
            root.destroy()
            return
        x = cx_anchor + ax * math.sin(2 * math.pi * args.freq_x * t)
        y = cy_anchor + ay * math.sin(2 * math.pi * args.freq_y * t)
        canvas.coords(dot, x - r, y - r, x + r, y + r)
        # short trail
        trail.append((x, y))
        if len(trail) > trail_max:
            trail.pop(0)
        canvas.delete("trail")
        for i, (tx, ty) in enumerate(trail[:-1]):
            f = i / max(len(trail) - 1, 1)
            rr = max(2, int(r * 0.35 * f))
            canvas.create_oval(tx - rr, ty - rr, tx + rr, ty + rr,
                                fill="#444444", outline="",
                                tags=("trail",))
        # ensure dot is on top
        canvas.tag_raise(dot)
        canvas.itemconfig(info, text=f"t={t:5.1f}s  pos=({x:.0f},{y:.0f})")
        root.after(33, tick)  # ~30 Hz

    root.after(33, tick)
    root.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
