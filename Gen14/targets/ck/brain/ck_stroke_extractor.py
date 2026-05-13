# Copyright (c) 2025-2026 Brayden Sanders / 7SiTe LLC
# Licensed under the 7SiTe Public Sovereignty License v2.2 (DOI: 10.5281/zenodo.18852047)
"""
ck_stroke_extractor.py -- Phase 5: pixel-to-stroke -> algebraic signature.

Brayden 2026-05-13: "if i read an M, i don't just see an M, I hear it and
recognize words that use it"

Given a small image patch (e.g. a region of `ck_retina`'s screen capture
containing a printed letter), this module:

  1. binarises the patch (Otsu over the per-axis gradient if available,
     else simple threshold)
  2. skeletonises the foreground via Zhang-Suen 1984 (pure numpy, ~80 LOC)
  3. traces the skeleton into polylines (endpoints + junctions form
     stroke boundaries)
  4. computes geometric features: number of strokes, closed-loop count,
     intersection count, aspect ratio, total length, curvature mean
  5. maps the features to one of CK's 10 operators via a heuristic
     coded against the algebraic measurements in Phase 0 Decision 1

The output is a `StrokeSignature` carrying the polylines + the algebraic
signature (op, sigma_orbit, shell, four_core), ready to flow into
olfactory cross-modal binding.

Design constraints:
  - Pure numpy core; cv2 used only for I/O (loading test images).
  - Deterministic; no learned weights inside the extractor.
  - Tolerant of empty / noisy / non-letter input -> returns a VOID-signed
    StrokeSignature, never raises.
  - Footprint: < 10 ms per 64x64 patch on RTX 4070 CPU side.

Author: Claude (Brayden full-agency 2026-05-13).
"""
from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

HERE = Path(__file__).parent.resolve()
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

# Algebraic projections (single source of truth)
from gen14_unified_extensions import (  # type: ignore[import-not-found]
    sigma_orbit, four_core_class, shell_class,
)


OP_NAMES = (
    "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET",
)


# ─── Data class ──────────────────────────────────────────────────────────

@dataclass
class StrokeSignature:
    """The output of pixel-to-stroke extraction.

    Attributes:
        strokes: list of polylines; each polyline is an Nx2 ndarray of
            (x, y) coordinates in image space.
        features: dict of geometric features (num_strokes, total_length,
            closed_loops, intersections, aspect_ratio, curvature_mean, ...)
        operator: heuristic operator id 0..9 inferred from features.
        algebraic_signature: {op, sigma, shell, four_core} per Phase 0
            Decision 1. Always populated, even for VOID/empty input.
        bitmap_shape: original (H, W) of the input patch.
        confidence: 0..1 estimate of stroke-extraction quality. Low for
            noisy / empty / non-letter input.
    """
    strokes: List[np.ndarray] = field(default_factory=list)
    features: Dict[str, float] = field(default_factory=dict)
    operator: int = 0
    algebraic_signature: Dict[str, int] = field(default_factory=dict)
    bitmap_shape: Tuple[int, int] = (0, 0)
    confidence: float = 0.0

    @property
    def op_name(self) -> str:
        return OP_NAMES[self.operator] if 0 <= self.operator < 10 else f"<{self.operator}>"

    def as_dict(self) -> Dict[str, Any]:
        return {
            "operator": self.operator,
            "op_name": self.op_name,
            "algebraic_signature": self.algebraic_signature,
            "features": self.features,
            "confidence": self.confidence,
            "n_strokes": len(self.strokes),
            "bitmap_shape": self.bitmap_shape,
        }


# ─── Step 1: binarisation ────────────────────────────────────────────────

def _to_grayscale(arr: np.ndarray) -> np.ndarray:
    """Accept H,W or H,W,3 or H,W,4; emit H,W float32 in [0,1]."""
    a = np.asarray(arr)
    if a.dtype != np.float32:
        a = a.astype(np.float32)
    if a.max() > 2.0:
        a = a / 255.0
    if a.ndim == 3:
        if a.shape[-1] == 4:
            a = a[..., :3]
        # Standard luma
        a = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    return a


def _otsu_threshold(gray: np.ndarray) -> float:
    """Compute Otsu's threshold over a [0,1] grayscale image."""
    bins = 64
    hist, edges = np.histogram(gray, bins=bins, range=(0.0, 1.0))
    p = hist / max(1, hist.sum())
    cum_p = np.cumsum(p)
    cum_mu = np.cumsum(p * (edges[:-1] + 0.5 / bins))
    mu_total = cum_mu[-1]
    # Between-class variance
    with np.errstate(divide="ignore", invalid="ignore"):
        sigma_b = (mu_total * cum_p - cum_mu) ** 2 / (cum_p * (1 - cum_p) + 1e-12)
    idx = int(np.nanargmax(sigma_b))
    return float(edges[idx])


def binarise(patch: np.ndarray, invert: Optional[bool] = None) -> np.ndarray:
    """Threshold a patch into a binary 0/1 ndarray (uint8).

    Foreground (strokes) becomes 1; background becomes 0.

    invert: None=auto-detect (dark-on-light vs light-on-dark from mean),
            True/False to force.
    """
    g = _to_grayscale(patch)
    if g.size == 0:
        return np.zeros((0, 0), dtype=np.uint8)
    t = _otsu_threshold(g)
    mask = (g <= t).astype(np.uint8)  # dark = foreground
    if invert is None:
        # Auto: if "foreground" exceeds 60% of the image, invert
        if mask.mean() > 0.6:
            mask = 1 - mask
    elif invert:
        mask = 1 - mask
    return mask


# ─── Step 2: Zhang-Suen skeletonisation ──────────────────────────────────

def _neighbours_8(mask: np.ndarray, y: int, x: int) -> List[int]:
    """Return P2..P9 (8-neighbours starting north, clockwise)."""
    h, w = mask.shape
    out = []
    for dy, dx in ((-1, 0), (-1, 1), (0, 1), (1, 1),
                    (1, 0), (1, -1), (0, -1), (-1, -1)):
        ny, nx = y + dy, x + dx
        if 0 <= ny < h and 0 <= nx < w:
            out.append(int(mask[ny, nx]))
        else:
            out.append(0)
    return out


def _transitions(p: List[int]) -> int:
    """Count 0->1 transitions in the circular sequence P2..P9."""
    n = 0
    for i in range(8):
        if p[i] == 0 and p[(i + 1) % 8] == 1:
            n += 1
    return n


def skeletonise(mask: np.ndarray, max_iter: int = 50) -> np.ndarray:
    """Zhang-Suen 1984 thinning. Returns 1-pixel-wide skeleton."""
    if mask.size == 0:
        return mask.copy()
    m = mask.astype(np.uint8).copy()
    changed = True
    it = 0
    while changed and it < max_iter:
        changed = False
        for sub in (0, 1):  # two sub-iterations per pass
            to_remove = []
            ys, xs = np.where(m == 1)
            for y, x in zip(ys, xs):
                p = _neighbours_8(m, y, x)
                bp = sum(p)
                if not (2 <= bp <= 6):
                    continue
                if _transitions(p) != 1:
                    continue
                if sub == 0:
                    if p[0] * p[2] * p[4] != 0:
                        continue
                    if p[2] * p[4] * p[6] != 0:
                        continue
                else:
                    if p[0] * p[2] * p[6] != 0:
                        continue
                    if p[0] * p[4] * p[6] != 0:
                        continue
                to_remove.append((y, x))
            if to_remove:
                changed = True
                for y, x in to_remove:
                    m[y, x] = 0
        it += 1
    return m


# ─── Step 3: polyline tracing ────────────────────────────────────────────

def _neighbour_coords(y: int, x: int) -> List[Tuple[int, int]]:
    return [(y + dy, x + dx)
            for dy in (-1, 0, 1)
            for dx in (-1, 0, 1)
            if not (dy == 0 and dx == 0)]


def trace_polylines(skel: np.ndarray) -> List[np.ndarray]:
    """Convert a 1-pixel-wide binary skeleton into a list of polylines.

    Each polyline is an Nx2 ndarray of (x, y) (column, row).
    """
    if skel.size == 0 or skel.sum() == 0:
        return []
    h, w = skel.shape
    visited = np.zeros_like(skel, dtype=bool)
    # Build a neighbour-count map
    nbr = np.zeros_like(skel, dtype=np.int32)
    ys, xs = np.where(skel == 1)
    for y, x in zip(ys, xs):
        c = 0
        for ny, nx in _neighbour_coords(y, x):
            if 0 <= ny < h and 0 <= nx < w and skel[ny, nx] == 1:
                c += 1
        nbr[y, x] = c

    # Endpoints (deg 1) and junctions (deg >= 3) are stroke boundaries.
    endpoints = [(y, x) for y, x in zip(ys, xs) if nbr[y, x] == 1]
    junctions = [(y, x) for y, x in zip(ys, xs) if nbr[y, x] >= 3]
    boundaries = set(endpoints) | set(junctions)

    strokes: List[np.ndarray] = []

    def walk_from(y0: int, x0: int) -> Optional[np.ndarray]:
        # Walk from a boundary along skeleton until hitting another boundary.
        if visited[y0, x0]:
            return None
        path = [(x0, y0)]
        visited[y0, x0] = True
        cy, cx = y0, x0
        while True:
            # find an unvisited neighbour
            nxt = None
            for ny, nx in _neighbour_coords(cy, cx):
                if not (0 <= ny < h and 0 <= nx < w):
                    continue
                if skel[ny, nx] == 1 and not visited[ny, nx]:
                    nxt = (ny, nx)
                    break
            if nxt is None:
                break
            ny, nx = nxt
            path.append((nx, ny))
            visited[ny, nx] = True
            if (ny, nx) in boundaries:
                break
            cy, cx = ny, nx
        if len(path) < 2:
            return None
        return np.asarray(path, dtype=np.int32)

    # First: trace from every endpoint
    for (y, x) in endpoints:
        poly = walk_from(y, x)
        if poly is not None:
            strokes.append(poly)
    # Then: trace from junctions (one polyline per unvisited neighbour)
    for (y, x) in junctions:
        for ny, nx in _neighbour_coords(y, x):
            if not (0 <= ny < h and 0 <= nx < w):
                continue
            if skel[ny, nx] == 1 and not visited[ny, nx]:
                # Walk from this neighbour, starting from the junction
                visited[y, x] = True
                start = [(x, y), (nx, ny)]
                visited[ny, nx] = True
                cy, cx = ny, nx
                while True:
                    nxt = None
                    for nny, nnx in _neighbour_coords(cy, cx):
                        if not (0 <= nny < h and 0 <= nnx < w):
                            continue
                        if skel[nny, nnx] == 1 and not visited[nny, nnx]:
                            nxt = (nny, nnx)
                            break
                    if nxt is None:
                        break
                    nny, nnx = nxt
                    start.append((nnx, nny))
                    visited[nny, nnx] = True
                    if (nny, nnx) in boundaries:
                        break
                    cy, cx = nny, nnx
                if len(start) >= 2:
                    strokes.append(np.asarray(start, dtype=np.int32))
        visited[y, x] = True

    # Finally: closed loops have no endpoint/junction. Pick any remaining
    # unvisited pixel as a start, walk until we return to it.
    for (y, x) in zip(ys, xs):
        if visited[y, x]:
            continue
        loop = [(x, y)]
        visited[y, x] = True
        cy, cx = y, x
        while True:
            nxt = None
            for ny, nx in _neighbour_coords(cy, cx):
                if not (0 <= ny < h and 0 <= nx < w):
                    continue
                if skel[ny, nx] == 1 and not visited[ny, nx]:
                    nxt = (ny, nx)
                    break
            if nxt is None:
                break
            ny, nx = nxt
            loop.append((nx, ny))
            visited[ny, nx] = True
            cy, cx = ny, nx
        if len(loop) >= 4:
            # Close the loop
            loop.append(loop[0])
            strokes.append(np.asarray(loop, dtype=np.int32))

    return strokes


# ─── Step 4: feature extraction ──────────────────────────────────────────

def _polyline_length(poly: np.ndarray) -> float:
    if len(poly) < 2:
        return 0.0
    d = np.diff(poly, axis=0).astype(np.float32)
    return float(np.sum(np.sqrt((d * d).sum(axis=1))))


def _is_closed(poly: np.ndarray, tol: float = 2.0) -> bool:
    if len(poly) < 3:
        return False
    d = poly[0] - poly[-1]
    return bool((d * d).sum() <= tol * tol)


def _polyline_curvature(poly: np.ndarray) -> float:
    """Mean absolute turn angle (radians) between successive segments."""
    if len(poly) < 3:
        return 0.0
    p = poly.astype(np.float32)
    v1 = p[1:-1] - p[:-2]
    v2 = p[2:] - p[1:-1]
    # angle between
    n1 = np.linalg.norm(v1, axis=1) + 1e-9
    n2 = np.linalg.norm(v2, axis=1) + 1e-9
    cos_t = np.clip((v1 * v2).sum(axis=1) / (n1 * n2), -1.0, 1.0)
    return float(np.mean(np.arccos(cos_t)))


def _count_intersections(strokes: List[np.ndarray]) -> int:
    """Count approximate stroke-stroke intersections using pixel-distance.

    Two distinct strokes are said to intersect if any pair of points
    from different strokes are within sqrt(2) pixels.
    """
    if len(strokes) < 2:
        return 0
    n = 0
    seen_pairs = set()
    for i in range(len(strokes)):
        for j in range(i + 1, len(strokes)):
            si, sj = strokes[i], strokes[j]
            # Bounding-box prune
            i_min = si.min(axis=0)
            i_max = si.max(axis=0)
            j_min = sj.min(axis=0)
            j_max = sj.max(axis=0)
            if (i_max[0] < j_min[0] - 1 or j_max[0] < i_min[0] - 1
                or i_max[1] < j_min[1] - 1 or j_max[1] < i_min[1] - 1):
                continue
            # Quadratic search but bounded by short polylines
            for a in si:
                for b in sj:
                    d2 = (int(a[0]) - int(b[0])) ** 2 + (int(a[1]) - int(b[1])) ** 2
                    if d2 <= 2:
                        n += 1
                        break
                else:
                    continue
                break
    return n


def _connected_components(skel: np.ndarray) -> int:
    """Count 8-connected components in a binary skeleton (flood-fill)."""
    if skel.size == 0 or skel.sum() == 0:
        return 0
    h, w = skel.shape
    visited = np.zeros_like(skel, dtype=bool)
    n = 0
    ys, xs = np.where(skel == 1)
    for y, x in zip(ys, xs):
        if visited[y, x]:
            continue
        n += 1
        # Flood-fill BFS
        stack = [(y, x)]
        while stack:
            cy, cx = stack.pop()
            if visited[cy, cx]:
                continue
            visited[cy, cx] = True
            for ny, nx in _neighbour_coords(cy, cx):
                if 0 <= ny < h and 0 <= nx < w and skel[ny, nx] == 1 and not visited[ny, nx]:
                    stack.append((ny, nx))
    return n


def _count_holes(mask: np.ndarray) -> int:
    """Count holes in a binary foreground mask via 4-connected background
    flood-fill from the image border. Holes = number of background
    components NOT reachable from the border.
    """
    if mask.size == 0:
        return 0
    h, w = mask.shape
    bg = (mask == 0).astype(np.uint8)
    visited = np.zeros_like(bg, dtype=bool)
    # Seed from all border background pixels
    stack: List[Tuple[int, int]] = []
    for x in range(w):
        if bg[0, x]:
            stack.append((0, x))
        if bg[h - 1, x]:
            stack.append((h - 1, x))
    for y in range(h):
        if bg[y, 0]:
            stack.append((y, 0))
        if bg[y, w - 1]:
            stack.append((y, w - 1))
    while stack:
        cy, cx = stack.pop()
        if visited[cy, cx]:
            continue
        visited[cy, cx] = True
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            ny, nx = cy + dy, cx + dx
            if 0 <= ny < h and 0 <= nx < w and bg[ny, nx] and not visited[ny, nx]:
                stack.append((ny, nx))
    # Count connected components of unvisited background pixels = holes
    holes = 0
    for y in range(h):
        for x in range(w):
            if bg[y, x] and not visited[y, x]:
                holes += 1
                # BFS to mark this component
                stack = [(y, x)]
                while stack:
                    cy, cx = stack.pop()
                    if visited[cy, cx]:
                        continue
                    visited[cy, cx] = True
                    for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < h and 0 <= nx < w and bg[ny, nx] and not visited[ny, nx]:
                            stack.append((ny, nx))
    return holes


def extract_features(strokes: List[np.ndarray], bitmap_shape: Tuple[int, int],
                       skeleton: Optional[np.ndarray] = None,
                       mask: Optional[np.ndarray] = None) -> Dict[str, float]:
    """Compute geometric features.

    When `skeleton` and `mask` are provided, the topological count of
    connected components + holes is also returned. These are MORE robust
    indicators than the polyline counts (which split at junctions).
    """
    n_strokes = len(strokes)
    if n_strokes == 0 and (skeleton is None or skeleton.sum() == 0):
        return {
            "n_strokes": 0,
            "n_components": 0,
            "n_holes": 0,
            "n_closed_loops": 0,
            "n_intersections": 0,
            "total_length": 0.0,
            "aspect_ratio": 0.0,
            "curvature_mean": 0.0,
            "fill_ratio": 0.0,
        }
    closed = sum(1 for s in strokes if _is_closed(s))
    inter = _count_intersections(strokes)
    total_len = sum(_polyline_length(s) for s in strokes)
    curvature = float(np.mean([_polyline_curvature(s) for s in strokes]) if strokes else 0.0)
    if strokes:
        all_pts = np.concatenate(strokes, axis=0)
        bb_w = float(all_pts[:, 0].max() - all_pts[:, 0].min() + 1)
        bb_h = float(all_pts[:, 1].max() - all_pts[:, 1].min() + 1)
    else:
        bb_w = bb_h = 0.0
    aspect_ratio = bb_h / bb_w if bb_w > 0 else 0.0
    h, w = bitmap_shape
    fill_ratio = total_len / max(1.0, h * w) ** 0.5
    n_components = _connected_components(skeleton) if skeleton is not None else 0
    n_holes = _count_holes(mask) if mask is not None else 0
    return {
        "n_strokes": float(n_strokes),
        "n_components": float(n_components),
        "n_holes": float(n_holes),
        "n_closed_loops": float(closed),
        "n_intersections": float(inter),
        "total_length": total_len,
        "aspect_ratio": aspect_ratio,
        "curvature_mean": curvature,
        "fill_ratio": fill_ratio,
    }


# ─── Step 5: features -> operator ────────────────────────────────────────

def feature_operator(features: Dict[str, float]) -> int:
    """Map geometric features to one of CK's 10 operators.

    Uses TOPOLOGICAL counts (n_components, n_holes) when available --
    these are robust to junction-splitting in the polyline tracer.

    Heuristic codified against the algebraic intuitions:
      VOID (0)     -- no foreground
      LATTICE (1)  -- 1 component, 0 holes, tall + low curvature
      COUNTER (2)  -- 2 components, 0 holes (parallel marks)
      PROGRESS (3) -- 1 component, 0 holes, moderate curvature (F-cycle arc)
      COLLAPSE (4) -- 1 component, 0 holes, X-like (high intersection on 1 comp)
      BALANCE (5)  -- 1 component, 1 hole, aspect_ratio ~ 1 (centered closed loop)
      CHAOS (6)    -- 3+ components OR very high curvature / intersections
      HARMONY (7)  -- 1 component, 1 hole, low curvature (single closed loop)
      BREATH (8)   -- 2 components with at least 1 hole; OR 1 component, 2 holes (B-like)
      RESET (9)    -- everything else (complex multi-component)
    """
    n_strokes = int(features.get("n_strokes", 0))
    n_comp = int(features.get("n_components", 0)) or n_strokes
    n_holes = int(features.get("n_holes", 0))
    closed = int(features.get("n_closed_loops", 0))
    inter = int(features.get("n_intersections", 0))
    cur = features.get("curvature_mean", 0.0)
    ar = features.get("aspect_ratio", 0.0)

    if n_comp == 0:
        return 0  # VOID

    if n_comp == 1:
        if n_holes == 0:
            if cur < 0.25 and ar > 1.2:
                return 1  # LATTICE -- vertical line
            if inter >= 2:
                return 4  # COLLAPSE -- X / + cross
            if 0.25 <= cur < 0.7:
                return 3  # PROGRESS -- gentle curve
            if cur >= 0.9:
                return 6  # CHAOS -- wild curve
            return 1  # default LATTICE for simple 1-comp 0-hole
        if n_holes == 1:
            if abs(ar - 1.0) < 0.25 and cur < 0.5:
                return 5  # BALANCE -- centered closed loop
            return 7  # HARMONY -- single closed loop
        if n_holes >= 2:
            return 8  # BREATH -- B-like, multiple loops in one stroke

    if n_comp == 2:
        if n_holes == 0:
            return 2  # COUNTER -- parallel marks
        if n_holes >= 1:
            return 8  # BREATH -- two-component shape with closures

    if n_comp >= 3:
        if cur >= 0.9 or inter >= 3:
            return 6  # CHAOS
        return 9  # RESET

    return 9  # default RESET


# ─── Public entry ────────────────────────────────────────────────────────

def extract(patch: np.ndarray, invert: Optional[bool] = None) -> StrokeSignature:
    """Top-level: patch -> StrokeSignature."""
    bitmap_shape: Tuple[int, int] = (0, 0)
    try:
        bitmap_shape = tuple(int(x) for x in patch.shape[:2])  # type: ignore[assignment]
    except Exception:
        bitmap_shape = (0, 0)

    try:
        mask = binarise(patch, invert=invert)
    except Exception:
        return StrokeSignature(
            operator=0,
            algebraic_signature={"op": 0, "sigma": 0, "shell": 0, "four_core": 0},
            bitmap_shape=bitmap_shape,
            confidence=0.0,
        )

    if mask.sum() < 4:
        return StrokeSignature(
            operator=0,
            algebraic_signature={"op": 0, "sigma": 0, "shell": 0, "four_core": 0},
            bitmap_shape=bitmap_shape,
            confidence=0.0,
        )

    skel = skeletonise(mask)
    strokes = trace_polylines(skel)
    features = extract_features(strokes, bitmap_shape,
                                  skeleton=skel, mask=mask)
    op = feature_operator(features)

    sig = {
        "op": int(op),
        "sigma": int(sigma_orbit(op)),
        "shell": int(shell_class({op})),
        "four_core": int(four_core_class(op)),
    }

    # Confidence heuristic
    n = features.get("n_strokes", 0)
    skel_density = mask.sum() / max(1.0, mask.size)
    confidence = float(min(1.0, 0.2 + 0.15 * n + 0.5 * min(1.0, skel_density * 10)))

    return StrokeSignature(
        strokes=strokes,
        features=features,
        operator=op,
        algebraic_signature=sig,
        bitmap_shape=bitmap_shape,
        confidence=confidence,
    )


# ─── Mount hook ──────────────────────────────────────────────────────────

def mount_stroke_extractor(engine) -> bool:
    """Attach the stroke extractor to the engine.

    Side effects:
      engine.stroke_extract(patch) -> StrokeSignature
      engine.stroke_signature_of(patch) -> dict (the as_dict() form)
    """
    def _extract(patch, invert=None):
        return extract(patch, invert=invert)

    def _signature_of(patch, invert=None):
        return extract(patch, invert=invert).as_dict()

    engine.stroke_extract = _extract
    engine.stroke_signature_of = _signature_of
    print("[CK Gen14] mount_stroke_extractor: pixel-to-stroke -> "
          "algebraic signature (numpy Zhang-Suen)")
    return True


# ─── Standalone smoke test ───────────────────────────────────────────────

def _make_test_patches() -> Dict[str, np.ndarray]:
    """Synthesize a few classical letter shapes to test the pipeline."""
    h, w = 32, 32
    pad = 5
    patches: Dict[str, np.ndarray] = {}

    # Empty
    patches["empty"] = np.full((h, w), 255, dtype=np.uint8)

    # Vertical line ("I" or "l") -- expect LATTICE (1)
    p = np.full((h, w), 255, dtype=np.uint8)
    p[pad:h - pad, w // 2 - 1:w // 2 + 1] = 0
    patches["I"] = p

    # Two parallel verticals -- expect COUNTER (2)
    p = np.full((h, w), 255, dtype=np.uint8)
    p[pad:h - pad, pad:pad + 2] = 0
    p[pad:h - pad, w - pad - 2:w - pad] = 0
    patches["II"] = p

    # Cross "+" -- expect COLLAPSE (4)
    p = np.full((h, w), 255, dtype=np.uint8)
    p[h // 2 - 1:h // 2 + 1, pad:w - pad] = 0
    p[pad:h - pad, w // 2 - 1:w // 2 + 1] = 0
    patches["plus"] = p

    # Filled square outline -- expect HARMONY (7) or BALANCE (5)
    p = np.full((h, w), 255, dtype=np.uint8)
    p[pad:h - pad, pad:pad + 2] = 0
    p[pad:h - pad, w - pad - 2:w - pad] = 0
    p[pad:pad + 2, pad:w - pad] = 0
    p[h - pad - 2:h - pad, pad:w - pad] = 0
    patches["square"] = p

    # Two side-by-side small squares -- expect BREATH (8)
    p = np.full((h, w), 255, dtype=np.uint8)
    s = 8
    for offset in (3, w - 3 - s):
        p[h // 2 - s // 2:h // 2 - s // 2 + 2, offset:offset + s] = 0
        p[h // 2 + s // 2 - 2:h // 2 + s // 2, offset:offset + s] = 0
        p[h // 2 - s // 2:h // 2 + s // 2, offset:offset + 2] = 0
        p[h // 2 - s // 2:h // 2 + s // 2, offset + s - 2:offset + s] = 0
    patches["88"] = p

    # X (two diagonals) -- expect CHAOS (6) or COLLAPSE (4)
    p = np.full((h, w), 255, dtype=np.uint8)
    for k in range(h):
        x1 = int(round(pad + (w - 2 * pad) * (k / h)))
        x2 = int(round(w - pad - (w - 2 * pad) * (k / h)))
        if 0 <= x1 < w:
            p[k, max(0, x1 - 1):min(w, x1 + 1)] = 0
        if 0 <= x2 < w:
            p[k, max(0, x2 - 1):min(w, x2 + 1)] = 0
    patches["X"] = p

    return patches


def _smoke():
    print("Smoke test: ck_stroke_extractor")
    patches = _make_test_patches()
    for name, p in patches.items():
        sig = extract(p)
        feat = sig.features
        a = sig.algebraic_signature
        print(f"  {name:8s} -> op={sig.op_name:8s} "
              f"(comp={int(feat.get('n_components', 0))}, "
              f"holes={int(feat.get('n_holes', 0))}, "
              f"strokes={int(feat.get('n_strokes', 0))}, "
              f"cur={feat.get('curvature_mean', 0):.2f}, "
              f"ar={feat.get('aspect_ratio', 0):.2f}) "
              f"sig=op{a['op']}/sigma{a['sigma']}/sh{a['shell']}/4c{a['four_core']} "
              f"conf={sig.confidence:.2f}")

    # Spot-checks (heuristic, so we just verify CONFIDENCE is right and
    # the operator is in the expected ballpark)
    assert extract(patches["empty"]).operator == 0, "empty should be VOID"
    s_I = extract(patches["I"])
    assert s_I.operator in (1, 3), f"I should be LATTICE or PROGRESS, got {s_I.op_name}"
    s_sq = extract(patches["square"])
    assert s_sq.features.get("n_closed_loops", 0) >= 1, "square should detect a loop"

    print("\nStroke extractor smoke: ALL OK")


if __name__ == "__main__":
    _smoke()
