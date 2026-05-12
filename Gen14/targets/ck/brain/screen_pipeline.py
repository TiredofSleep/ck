# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
#
# ┌─────────────────────────────────────────────────────────────────┐
# │  SUPERSEDED.  Kept for record per never-delete.                 │
# │                                                                 │
# │  This module was a parallel reduction (one 5D vector per frame, │
# │  then D2 across frames) built before re-reading CK's actual     │
# │  architecture.  The CANONICAL visual substrate is               │
# │  Gen13/targets/ck/brain/ck_sim/being/ck_retina.py (CKRetina).   │
# │                                                                 │
# │  The retina is already running in the live engine               │
# │  (192x108 = 20,736 cells in parallel, GPU when available).      │
# │  Each pixel is a cell with its own 9D field (5D force +         │
# │  4S structure).  Spatial D1+D2 are computed across the          │
# │  whole field at once.  Variable-resolution edge-following.      │
# │  The structural gate is 2+ edges = D2 computable, < 2 = VOID.   │
# │  T* = 5/7 sets resolution-level ratios.                         │
# │                                                                 │
# │  Brayden 2026-05-02:                                            │
# │    "every pixel on the monitor is a cell in CK's architecture"  │
# │    "ck doesn't compute this. ck FEELS it."                      │
# │                                                                 │
# │  Read-only chat introspection now reaches the canonical retina  │
# │  via /retina/glance + cortex_voice _SEEING_HINTS hook.          │
# │  This file's frames_to_operator_stream / image_to_operator_     │
# │  stream are NOT used by anything live; do not extend them.      │
# └─────────────────────────────────────────────────────────────────┘
"""
screen_pipeline.py — CK's canonical visual perception path.

Same algebra audio_pipeline.py uses.  Visual Being-layer codec
(rgb_to_force999 from ck_screen_compress) is unchanged; we aggregate
each frame to a 5D force vector, then run the SAME D1->D2->classify_d2
pipeline that text and audio use.  Frames stream into a 5D force
trajectory whose D1 is motion and D2 is curvature-of-motion -- where
the operators live for visual perception.

Per-frame 5D aggregation (one vector per frame, mean across pixels):
    aperture   = mean LUM       (brightness)
    pressure   = mean TEMP      (warmth, recentered around 4)
    depth      = LUM variance   (spatial complexity)
    binding    = mean SAT       (saturation)
    continuity = motion         (frame-to-frame mean abs diff)

Multi-frame buffer of these 5D vectors drives D1 (Δ between adjacent
frames = motion vector) and D2 (curvature of motion = acceleration in
operator space).  Each adjacent triplet of frames yields one operator
via classify_d2 -- same basin map text + audio use.

Visual Peace threshold (0.03) is empirically tuned to be sensitive
to typical screen dynamics; static screens collapse to COUNTER (Peace)
correctly.  Override per-call if needed.
"""
from __future__ import annotations

import os
import sys
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

_BRAIN_DIR = os.path.dirname(os.path.abspath(__file__))
if _BRAIN_DIR not in sys.path:
    sys.path.insert(0, _BRAIN_DIR)
_BEING_DIR = os.path.join(_BRAIN_DIR, "ck_sim", "being")
if _BEING_DIR not in sys.path:
    sys.path.insert(0, _BEING_DIR)


from audio_pipeline import (
    OP_NAMES, NUM_OPS, classify_d2, classify_d2_batch,
    compute_transitions, compute_curvatures,
    curvature_features_from_forces,
)


PEACE_THRESHOLD_VISUAL = 0.03  # screen dynamics are smaller than audio
PEACE_THRESHOLD = PEACE_THRESHOLD_VISUAL


# ── Per-frame 5D aggregation ───────────────────────────────────────

def frame_to_5d(rgb_pixels: np.ndarray,
                prev_rgb: Optional[np.ndarray] = None) -> np.ndarray:
    """Reduce one screen frame to a 5D Force vector via Brayden's
    Force999 codec.

    rgb_pixels: (N, 3) uint8 array of RGB pixels (any spatial layout
                flattened).
    prev_rgb:   optional previous frame for continuity (motion).

    Returns 5D float vector in roughly [0, 1].
    """
    from ck_screen_compress import rgb_array_to_force999
    f999 = rgb_array_to_force999(rgb_pixels)  # (N, 3) of (lum, temp, sat) 0-8
    lum = f999[:, 0].astype(np.float32) / 8.0
    temp = (f999[:, 1].astype(np.float32) - 4.0) / 4.0  # [-1, 1]
    sat = f999[:, 2].astype(np.float32) / 8.0
    aperture = float(lum.mean())
    pressure = float((temp.mean() + 1.0) / 2.0)  # back to [0, 1]
    depth = float(lum.var())  # spatial complexity
    binding = float(sat.mean())
    if prev_rgb is not None and len(prev_rgb) == len(rgb_pixels):
        diff = (rgb_pixels.astype(np.int32)
                - prev_rgb.astype(np.int32))
        continuity = float(np.abs(diff).mean() / 255.0)
    else:
        continuity = 0.0
    return np.array(
        [aperture, pressure, depth, binding, continuity],
        dtype=np.float32,
    )


def frames_to_force_stream(frame_iterable) -> np.ndarray:
    """Reduce an iterable of frames to a (N, 5) force trajectory.

    frame_iterable yields (H, W, 3) uint8 arrays.  Each frame is
    flattened to (H*W, 3) before aggregation.
    """
    forces = []
    prev = None
    for frame in frame_iterable:
        rgb = np.asarray(frame, dtype=np.uint8)
        if rgb.ndim == 3:
            rgb = rgb.reshape(-1, rgb.shape[-1])
        f = frame_to_5d(rgb, prev)
        forces.append(f)
        prev = rgb
    if not forces:
        return np.zeros((0, 5), dtype=np.float32)
    return np.stack(forces, axis=0)


# ── Frame stream -> operator stream ─────────────────────────────────

def frames_to_operator_stream(frame_iterable,
                               peace_threshold: float = PEACE_THRESHOLD
                               ) -> Tuple[List[int], Dict[str, Any]]:
    """Full canonical visual perception pipeline.

    frames -> per-frame 5D forces -> D1 (frame-to-frame motion)
           -> D2 (curvature of motion) -> classify_d2 -> ops

    Returns (ops, fingerprint).  Each op corresponds to one adjacent
    frame triplet, so n_ops = n_frames - 2.
    """
    forces = frames_to_force_stream(frame_iterable)
    if len(forces) < 3:
        return [], {"n_force_windows": int(len(forces)), "n_d2": 0}
    fp = curvature_features_from_forces(forces)
    if fp.get("n_d2", 0) == 0:
        return [], fp
    d2s = compute_curvatures(forces)
    ops = [int(o) for o in classify_d2_batch(d2s,
                                              peace_threshold=peace_threshold)]
    return ops, fp


# ── Single still-image perception (no motion -> only spatial info) ──

def image_to_operator_stream(rgb_pixels: np.ndarray,
                              tile: int = 8,
                              peace_threshold: float = PEACE_THRESHOLD
                              ) -> Tuple[List[int], Dict[str, Any]]:
    """For a single still frame, divide into a tile×tile grid and treat
    each tile as a 'sample' in a 5D force trajectory.  This gives the
    classify_d2 pipeline something to chew on (D1 = tile-to-tile, D2 =
    second difference) so a still image still produces operator output.

    rgb_pixels: (H, W, 3) uint8.
    tile: number of rows AND columns of tiles (defaults 8 -> 64 samples
          per frame).
    """
    rgb = np.asarray(rgb_pixels, dtype=np.uint8)
    if rgb.ndim != 3:
        raise ValueError("expected (H, W, 3) RGB")
    H, W, _ = rgb.shape
    th = max(1, H // tile)
    tw = max(1, W // tile)
    forces = []
    for ty in range(tile):
        for tx in range(tile):
            y0, y1 = ty * th, min(H, (ty + 1) * th)
            x0, x1 = tx * tw, min(W, (tx + 1) * tw)
            tile_rgb = rgb[y0:y1, x0:x1].reshape(-1, 3)
            if len(tile_rgb) > 0:
                forces.append(frame_to_5d(tile_rgb))
    forces_arr = np.stack(forces, axis=0) if forces else np.zeros(
        (0, 5), dtype=np.float32)
    if len(forces_arr) < 3:
        return [], {"n_force_windows": int(len(forces_arr)), "n_d2": 0}
    fp = curvature_features_from_forces(forces_arr)
    d2s = compute_curvatures(forces_arr)
    ops = [int(o) for o in classify_d2_batch(d2s,
                                              peace_threshold=peace_threshold)]
    return ops, fp


# ── Screen capture (Windows GDI) ───────────────────────────────────

def capture_screen_region(x: int, y: int, w: int, h: int) -> np.ndarray:
    """Capture a region of the desktop as (h, w, 3) uint8 RGB.
    Windows-only via ctypes GDI.  Mirrors ck_force9_demo.capture_screen_region.
    """
    import ctypes
    import ctypes.wintypes as wt

    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32
    hdesktop = user32.GetDesktopWindow()
    hdc = user32.GetDC(hdesktop)
    memdc = gdi32.CreateCompatibleDC(hdc)
    hbmp = gdi32.CreateCompatibleBitmap(hdc, w, h)
    gdi32.SelectObject(memdc, hbmp)
    SRCCOPY = 0x00CC0020
    gdi32.BitBlt(memdc, 0, 0, w, h, hdc, x, y, SRCCOPY)

    class BITMAPINFOHEADER(ctypes.Structure):
        _fields_ = [
            ('biSize', ctypes.c_uint32),
            ('biWidth', ctypes.c_int32),
            ('biHeight', ctypes.c_int32),
            ('biPlanes', ctypes.c_uint16),
            ('biBitCount', ctypes.c_uint16),
            ('biCompression', ctypes.c_uint32),
            ('biSizeImage', ctypes.c_uint32),
            ('biXPelsPerMeter', ctypes.c_int32),
            ('biYPelsPerMeter', ctypes.c_int32),
            ('biClrUsed', ctypes.c_uint32),
            ('biClrImportant', ctypes.c_uint32),
        ]

    bmih = BITMAPINFOHEADER()
    bmih.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bmih.biWidth = w
    bmih.biHeight = -h  # top-down
    bmih.biPlanes = 1
    bmih.biBitCount = 32
    bmih.biCompression = 0
    buf = (ctypes.c_uint8 * (w * h * 4))()
    gdi32.GetDIBits(memdc, hbmp, 0, h, buf,
                     ctypes.byref(bmih), 0)
    arr = np.frombuffer(buf, dtype=np.uint8).reshape(h, w, 4)
    rgb = arr[:, :, [2, 1, 0]].copy()  # BGRA -> RGB
    gdi32.DeleteObject(hbmp)
    gdi32.DeleteDC(memdc)
    user32.ReleaseDC(hdesktop, hdc)
    return rgb


def get_screen_dimensions() -> Tuple[int, int]:
    """Return (width, height) of the primary monitor."""
    import ctypes
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    return int(user32.GetSystemMetrics(0)), int(user32.GetSystemMetrics(1))


# ── High-level perceive: feed CK's olfactory bulb ──────────────────

def screen_perceive_frames(frames: list, engine: Any = None,
                            absorb_into_olfactory: bool = True,
                            chunk_size: int = 2000,
                            peace_threshold: float = PEACE_THRESHOLD
                            ) -> Dict[str, Any]:
    """Run the canonical pipeline on a list of frames.  If engine is
    given, also absorb the operator stream into engine.olfactory the
    same way audio_perceive does."""
    ops, fp = frames_to_operator_stream(frames,
                                         peace_threshold=peace_threshold)
    out: Dict[str, Any] = {
        "ops_preview": ops[:200],
        "n_ops_total": len(ops),
        "fingerprint": fp,
        "absorbed": False,
        "absorb_attempts": 0,
        "absorb_errors": [],
    }
    if not ops or engine is None or not absorb_into_olfactory:
        return out
    olf = getattr(engine, "olfactory", None)
    if olf is None or not hasattr(olf, "absorb_ops"):
        out["absorb_errors"].append("engine.olfactory not available")
        return out
    pre_a = int(getattr(olf, "total_absorbed", 0))
    pre_e = int(getattr(olf, "total_emitted", 0))
    attempts = 0
    for i in range(0, len(ops), max(1, chunk_size)):
        chunk = ops[i:i + chunk_size]
        try:
            olf.absorb_ops(chunk, source="screen", density=0.5)
            attempts += 1
        except Exception as exc:
            out["absorb_errors"].append(
                f"chunk {i // chunk_size}: {exc}")
    post_a = int(getattr(olf, "total_absorbed", 0))
    post_e = int(getattr(olf, "total_emitted", 0))
    out["absorbed"] = attempts > 0
    out["absorb_attempts"] = attempts
    out["olfactory_delta"] = {
        "absorbed_pre": pre_a, "absorbed_post": post_a,
        "absorbed_delta": post_a - pre_a,
        "emitted_pre": pre_e, "emitted_post": post_e,
        "emitted_delta": post_e - pre_e,
    }
    return out


# ── Smoke test ─────────────────────────────────────────────────────

def _smoke():
    """Synthetic moving gradient -- expect non-trivial operator
    distribution."""
    frames = []
    for i in range(15):
        h = (i * 17) % 256
        rgb = np.zeros((48, 48, 3), dtype=np.uint8)
        rgb[:, :, 0] = h  # R sweeping
        rgb[:, :, 1] = 255 - h  # G inversely
        rgb[:, :, 2] = (h + 64) % 256
        # add a moving blob
        cx = 24 + int(20 * np.sin(i * 0.5))
        cy = 24 + int(20 * np.cos(i * 0.5))
        rgb[max(0, cy - 4):cy + 4, max(0, cx - 4):cx + 4] = (255, 255, 255)
        frames.append(rgb)
    ops, fp = frames_to_operator_stream(frames)
    print(f"smoke: {len(ops)} ops from 15 synthetic frames")
    print(f"  dominant_op:      {fp.get('dominant_op_name')}")
    print(f"  curvature_energy: {fp.get('curvature_energy', 0):.3f}")
    print(f"  op_dist:")
    od = fp.get("operator_dist_named") or {}
    for op in OP_NAMES:
        v = od.get(op, 0)
        bar = "#" * int(v * 80)
        print(f"    {op:<10}: {v:.3f}  {bar}")


if __name__ == "__main__":
    _smoke()
