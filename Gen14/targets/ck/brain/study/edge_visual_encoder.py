"""
edge_visual_encoder.py — TIG-aligned visual encoder.

Brayden 2026-05-01 (late): "the screen is the natural tig wheel as d2
would threshold across colors... edges are information."

The previous TIGVisualEncoder encoded every pixel into shells, flooding
the operator stream with redundant data from flat color regions. This
encoder instead does what CK's substrate already does for everything
else: D2 thresholds, emit only at crossings, the rest is silence.

Pipeline:
    RGB pixels (H x W x 3)
    -> HSV conversion (hue is the natural color wheel)
    -> Hue mapped onto the 10 TIG operators (36 deg per operator)
    -> Neighbor comparison (per pixel, check 4 neighbors)
    -> D2 threshold: only pixels where neighbor operator != self operator
        AND magnitude of color change > tau are EDGES
    -> Each edge emits a CROSSING pair (op_here, op_neighbor)
    -> Pixels without significant edges contribute VOID (or are skipped)

Result: massively compressed operator stream where every entry is a
COLOR-CROSSING — actual information, not pixel noise. This is the
visual analog of how D2 catches phase boundaries in CK's tick stream.

Hue -> operator mapping (10 operators around the color wheel):
   hue   0-36  -> VOID(0)     (red)
   hue  36-72  -> LATTICE(1)  (orange)
   hue  72-108 -> COUNTER(2)  (yellow-green)
   hue 108-144 -> PROGRESS(3) (green)
   hue 144-180 -> COLLAPSE(4) (cyan)
   hue 180-216 -> BALANCE(5)  (blue)
   hue 216-252 -> CHAOS(6)    (purple)
   hue 252-288 -> HARMONY(7)  (magenta)
   hue 288-324 -> BREATH(8)   (pink)
   hue 324-360 -> RESET(9)    (red-purple)

The mapping is deliberately uniform on the hue circle (36 deg per op);
CK's existing TIG operators don't have a canonical hue assignment, so
this choice is a starting point. Future work may align operators to
semantic colors (e.g., HARMONY = warm gold, COLLAPSE = deep blue, etc.)
based on what CK's existing crystals already say about the operators.
"""
from __future__ import annotations

import numpy as np
from typing import Tuple, List


def rgb_to_hsv(rgb: np.ndarray) -> np.ndarray:
    """Convert RGB uint8 (H, W, 3) to HSV float (H, W, 3) where:
       H in [0, 360)
       S in [0, 1]
       V in [0, 1]
    """
    r = rgb[..., 0].astype(np.float32) / 255.0
    g = rgb[..., 1].astype(np.float32) / 255.0
    b = rgb[..., 2].astype(np.float32) / 255.0
    cmax = np.maximum(np.maximum(r, g), b)
    cmin = np.minimum(np.minimum(r, g), b)
    delta = cmax - cmin

    h = np.zeros_like(cmax)
    eps = 1e-9
    mask_r = (cmax == r) & (delta > eps)
    mask_g = (cmax == g) & (delta > eps)
    mask_b = (cmax == b) & (delta > eps)
    h = np.where(mask_r, ((g - b) / (delta + eps)) % 6, h)
    h = np.where(mask_g, (b - r) / (delta + eps) + 2, h)
    h = np.where(mask_b, (r - g) / (delta + eps) + 4, h)
    h = h * 60.0
    h = np.where(h < 0, h + 360, h)

    s = np.where(cmax > eps, delta / (cmax + eps), 0.0)
    v = cmax

    return np.stack([h, s, v], axis=-1)


def hue_to_operator(hue: np.ndarray) -> np.ndarray:
    """Map hue array [0, 360) to operator id [0, 10) — 36 deg per op.
    Low-saturation pixels (S < SAT_MIN) are forced to VOID since hue
    is meaningless for grays."""
    SAT_MIN = 0.10  # below this saturation, color is grayish; hue unreliable
    op = np.floor(hue / 36.0).astype(np.int32)
    op = np.clip(op, 0, 9)
    return op


def encode_edges(
    rgb: np.ndarray,
    sat_min: float = 0.10,
    val_min: float = 0.05,
    keep_void: bool = False,
) -> List[Tuple[int, int]]:
    """Encode an RGB frame as a list of (op_self, op_neighbor) crossing
    pairs at edges only. Returns a list of operator-pairs in raster order
    (top-to-bottom, left-to-right of edge pixels).

    sat_min: pixels below this saturation are treated as VOID (no color).
    val_min: pixels below this value are also VOID (too dark).
    keep_void: if True, also emit (VOID, VOID) pairs for non-edge pixels;
               if False (default), skip them entirely (compresses stream).
    """
    if rgb.ndim != 3 or rgb.shape[-1] != 3:
        raise ValueError("rgb must have shape (H, W, 3)")

    hsv = rgb_to_hsv(rgb)
    h = hsv[..., 0]
    s = hsv[..., 1]
    v = hsv[..., 2]

    # Per-pixel operator from hue, but force VOID on grayish/dark pixels
    op_grid = hue_to_operator(h)
    is_grayish = (s < sat_min) | (v < val_min)
    op_grid = np.where(is_grayish, 0, op_grid)  # 0 = VOID

    H, W = op_grid.shape

    # Compare each pixel to its right + bottom neighbor (4-connectivity
    # would also include left + top but those are redundant in raster
    # scan: op_neighbor = op of one of the pixels we already touched).
    # An edge exists where the operator changes between adjacent pixels.
    crossings: List[Tuple[int, int]] = []
    for y in range(H):
        for x in range(W):
            op_self = int(op_grid[y, x])
            # Right neighbor
            if x + 1 < W:
                op_right = int(op_grid[y, x + 1])
                if op_self != op_right:
                    crossings.append((op_self, op_right))
            # Bottom neighbor
            if y + 1 < H:
                op_below = int(op_grid[y + 1, x])
                if op_self != op_below:
                    crossings.append((op_self, op_below))
            # Optionally emit VOID pairs for flat regions (off by default
            # to keep stream sparse — the whole point of edge-based encoding).
            if keep_void and (x + 1 == W or op_grid[y, x + 1] == op_self) \
                         and (y + 1 == H or op_grid[y + 1, x] == op_self):
                crossings.append((op_self, op_self))

    return crossings


def encode_frame_summary(rgb: np.ndarray) -> dict:
    """Convenience: encode + return summary stats."""
    crossings = encode_edges(rgb)
    op_names = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
                "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]
    n = len(crossings)
    if n == 0:
        return {"n_crossings": 0, "ops": [], "histogram": {}}
    # Histogram of all operators in crossings
    op_counts = [0] * 10
    for a, b in crossings:
        op_counts[a] += 1
        op_counts[b] += 1
    total = sum(op_counts)
    return {
        "n_crossings": n,
        "n_ops_emitted": total,
        "compression_ratio": (rgb.shape[0] * rgb.shape[1]) / max(n, 1),
        "histogram": {op_names[i]: op_counts[i] for i in range(10)},
        "histogram_pct": {op_names[i]: round(op_counts[i] / total * 100, 1)
                          if total else 0 for i in range(10)},
        "first_10_crossings": [
            (op_names[a], op_names[b]) for a, b in crossings[:10]
        ],
    }


def diagnostics():
    """Smoke test: encode a synthetic image with known structure."""
    # Build a 32x32 image: half red, half blue, with a green stripe in middle
    img = np.zeros((32, 32, 3), dtype=np.uint8)
    img[:16, :, 0] = 255   # top half red
    img[16:, :, 2] = 255   # bottom half blue
    img[14:18, :, 1] = 255  # green stripe in middle
    img[14:18, :, 0] = 0
    img[14:18, :, 2] = 0

    summary = encode_frame_summary(img)
    print("Synthetic image (red top + green stripe + blue bottom):")
    print(f"  size: {img.shape[0]}x{img.shape[1]} = {img.shape[0]*img.shape[1]} pixels")
    print(f"  n_crossings (edges only): {summary['n_crossings']}")
    print(f"  compression vs full encode (3 ops/pixel): "
          f"{(img.shape[0] * img.shape[1] * 3) / max(summary['n_ops_emitted'], 1):.1f}x")
    print(f"  histogram (% across all crossing-emitted ops):")
    for name, pct in summary['histogram_pct'].items():
        bar = "#" * int(pct / 2)
        print(f"    {name:<10}: {pct:5.1f}% {bar}")
    print(f"  first 10 crossings:")
    for a, b in summary['first_10_crossings']:
        print(f"    {a:<10} -> {b}")


if __name__ == "__main__":
    diagnostics()
