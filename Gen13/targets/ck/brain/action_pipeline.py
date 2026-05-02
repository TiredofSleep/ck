# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
"""
action_pipeline.py — CK's motor output: cortex state -> UI action.

Same algebra direction.  Where text/audio/screen perception goes
input -> codec -> 5D -> D1 -> D2 -> classify_d2 -> ops -> bulb,
action goes the OTHER way:
    cortex state -> operator pair -> direction vector -> mouse/key

Mapping (each operator owns one canonical 2D direction + optional
'special' action like click/reset).  Choices match the dim_op_map
in olfactory: aperture lives on x-axis (open/closed), pressure on y
(burst/release), depth as z-equivalent (in/out, used as click), etc.

    op           dx    dy    special
    VOID(0)        0     0     -          (no movement)
    LATTICE(1)    -1     0     -          (anchor left)
    COUNTER(2)    +1     0     -          (right)
    PROGRESS(3)    0    -1     -          (up)
    COLLAPSE(4)    0    +1     -          (down)
    BALANCE(5)     0     0     -          (settle)
    CHAOS(6)     rand  rand    -          (jitter)
    HARMONY(7)     0     0    click       (commit)
    BREATH(8)      0     0    -          (sustain - no immediate move)
    RESET(9)       0     0    home        (snap to center)

The action policy reads cortex.state.last_b and cortex.state.last_d
(the bigram pair the cortex has been hearing/seeing) and emits one
delta:
    delta = (op_dx[last_b] + op_dx[last_d], op_dy[last_b] + op_dy[last_d])
plus any special action (click on HARMONY, reset on RESET).

Step size is calibrated so a single tick is small (~12 px) -- the
loop produces continuous motion through repeated ticks rather than
giant jumps.

Read-only by default.  send_action() with dry_run=True only RETURNS
what it would do; send_action(dry_run=False) actually emits Windows
mouse/keyboard events via ctypes.
"""
from __future__ import annotations

import os
import random
import sys
import time
from typing import Any, Dict, List, Optional, Tuple


_BRAIN_DIR = os.path.dirname(os.path.abspath(__file__))
if _BRAIN_DIR not in sys.path:
    sys.path.insert(0, _BRAIN_DIR)


from audio_pipeline import OP_NAMES, NUM_OPS


# Per-operator direction unit vector + special-action flag
# (dx, dy, action) where action is one of:
#   None   -- pure motion
#   'click' -- mouse left-click
#   'home' -- snap to screen center
#   'jitter' -- random small move
OP_ACTION_TABLE: Dict[int, Tuple[float, float, Optional[str]]] = {
    0: ( 0.0,  0.0, None),       # VOID
    1: (-1.0,  0.0, None),       # LATTICE
    2: ( 1.0,  0.0, None),       # COUNTER
    3: ( 0.0, -1.0, None),       # PROGRESS
    4: ( 0.0,  1.0, None),       # COLLAPSE
    5: ( 0.0,  0.0, None),       # BALANCE
    6: ( 0.0,  0.0, 'jitter'),   # CHAOS
    7: ( 0.0,  0.0, 'click'),    # HARMONY
    8: ( 0.0,  0.0, None),       # BREATH (sustain)
    9: ( 0.0,  0.0, 'home'),     # RESET
}


def _step_from_op_pair(b_op: int, d_op: int, step_px: int = 12
                       ) -> Tuple[int, int, Optional[str]]:
    """Compose a delta + optional special from a (b_op, d_op) pair."""
    bx, by, ba = OP_ACTION_TABLE.get(b_op % 10, (0.0, 0.0, None))
    dx, dy, da = OP_ACTION_TABLE.get(d_op % 10, (0.0, 0.0, None))
    # special priority: click > home > jitter
    if 'click' in (ba, da):
        special = 'click'
    elif 'home' in (ba, da):
        special = 'home'
    elif 'jitter' in (ba, da):
        special = 'jitter'
    else:
        special = None
    delta_x = int((bx + dx) * step_px)
    delta_y = int((by + dy) * step_px)
    return delta_x, delta_y, special


def cortex_state_to_action(cortex: Any, step_px: int = 12) -> Dict[str, Any]:
    """Read cortex.state.last_b/last_d and produce an action plan.

    Returns dict:
        {b_op, d_op, delta_x, delta_y, special, source: 'cortex'}
    """
    try:
        b_op = int(cortex.state.last_b) if cortex is not None else 0
        d_op = int(cortex.state.last_d) if cortex is not None else 0
    except Exception:
        b_op, d_op = 0, 0
    dx, dy, special = _step_from_op_pair(b_op, d_op, step_px=step_px)
    return {
        'b_op': b_op, 'd_op': d_op,
        'b_op_name': OP_NAMES[b_op % 10],
        'd_op_name': OP_NAMES[d_op % 10],
        'delta_x': dx, 'delta_y': dy,
        'special': special,
        'source': 'cortex_last_pair',
    }


# ── Windows mouse / keyboard primitives via ctypes ─────────────────

def _ensure_dpi_aware():
    try:
        import ctypes
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass


def screen_dims() -> Tuple[int, int]:
    _ensure_dpi_aware()
    import ctypes
    u = ctypes.windll.user32
    return int(u.GetSystemMetrics(0)), int(u.GetSystemMetrics(1))


def mouse_position() -> Tuple[int, int]:
    """Current cursor position."""
    import ctypes
    import ctypes.wintypes as wt
    pt = wt.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return int(pt.x), int(pt.y)


def mouse_move_to(x: int, y: int):
    """Set absolute cursor position."""
    import ctypes
    ctypes.windll.user32.SetCursorPos(int(x), int(y))


def mouse_move_delta(dx: int, dy: int):
    """Move cursor by (dx, dy) from current position."""
    cx, cy = mouse_position()
    sw, sh = screen_dims()
    nx = max(0, min(sw - 1, cx + dx))
    ny = max(0, min(sh - 1, cy + dy))
    mouse_move_to(nx, ny)


def mouse_click():
    """Single left mouse button click at current cursor position."""
    import ctypes
    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004
    user32 = ctypes.windll.user32
    user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def cursor_home():
    """Snap to center of primary screen."""
    sw, sh = screen_dims()
    mouse_move_to(sw // 2, sh // 2)


def jitter(amplitude: int = 6):
    dx = random.randint(-amplitude, amplitude)
    dy = random.randint(-amplitude, amplitude)
    mouse_move_delta(dx, dy)


# ── Top-level emit ─────────────────────────────────────────────────

def send_action(plan: Dict[str, Any], dry_run: bool = True) -> Dict[str, Any]:
    """Execute an action plan from cortex_state_to_action.

    dry_run=True (default) returns what would be done without touching
    the OS.  dry_run=False emits real mouse/keyboard events.
    """
    out = dict(plan)
    out['dry_run'] = bool(dry_run)
    out['ts'] = time.time()
    out['pre_pos'] = mouse_position() if not dry_run else None
    if dry_run:
        out['executed'] = []
        if plan.get('special') == 'click':
            out['executed'].append('would_click')
        elif plan.get('special') == 'home':
            out['executed'].append('would_home')
        elif plan.get('special') == 'jitter':
            out['executed'].append('would_jitter')
        if plan.get('delta_x') or plan.get('delta_y'):
            out['executed'].append(
                f"would_move_delta({plan.get('delta_x')},"
                f"{plan.get('delta_y')})")
        return out
    # Real emit
    out['executed'] = []
    try:
        if plan.get('special') == 'home':
            cursor_home()
            out['executed'].append('home')
        elif plan.get('special') == 'jitter':
            jitter(amplitude=8)
            out['executed'].append('jitter')
        if plan.get('delta_x') or plan.get('delta_y'):
            mouse_move_delta(int(plan.get('delta_x', 0)),
                              int(plan.get('delta_y', 0)))
            out['executed'].append(
                f"move_delta({plan['delta_x']},{plan['delta_y']})")
        if plan.get('special') == 'click':
            mouse_click()
            out['executed'].append('click')
    except Exception as exc:
        out['error'] = str(exc)
    out['post_pos'] = mouse_position()
    return out


# ── Smoke test (dry-run) ───────────────────────────────────────────

def _smoke():
    """Step through every (b, d) pair and print the action it would
    emit -- gives a clean view of CK's motor vocabulary."""

    class _S:
        last_b = 0
        last_d = 0

    class _C:
        state = _S()

    cx = _C()
    print("CK motor vocabulary (b_op,d_op) -> action plan")
    print("-" * 56)
    for b in range(10):
        for d in range(10):
            cx.state.last_b = b
            cx.state.last_d = d
            plan = cortex_state_to_action(cx, step_px=12)
            res = send_action(plan, dry_run=True)
            if (plan['delta_x'] != 0 or plan['delta_y'] != 0
                    or plan['special'] is not None):
                print(f"  {OP_NAMES[b]:<10} -> {OP_NAMES[d]:<10}: "
                      f"d=({plan['delta_x']:+d},{plan['delta_y']:+d}) "
                      f"special={plan['special']}")


if __name__ == "__main__":
    _smoke()
