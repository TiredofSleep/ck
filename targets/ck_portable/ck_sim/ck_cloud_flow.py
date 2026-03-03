"""
ck_cloud_flow.py -- Cloud Optical Flow Extraction
===================================================
Operator: PROGRESS (3) -- motion is forward delta.

Physics-first optical flow from image frame pairs.
Turns cloud formation video into dense velocity fields.

Pipeline:
  1. Frame pair → spatial/temporal gradients (Ix, Iy, It)
  2. Horn-Schunck iterative solver → dense flow field (u, v)
  3. Patch decomposition → per-tile flow statistics
  4. Tile stats → 5D force vectors (same dimensions as D2)

No deep nets. No OpenCV. Pure NumPy + classical physics.

Frame format: 2D numpy arrays, float32 [0.0, 1.0] grayscale.
Flow output: (u, v) arrays same shape as input = pixel displacements.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from collections import deque
from typing import List, Optional, Tuple

import numpy as np

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, LATTICE, COUNTER, PROGRESS,
    COLLAPSE, BALANCE, CHAOS, BREATH, RESET, OP_NAMES,
)


# ================================================================
#  CONSTANTS
# ================================================================

DEFAULT_PATCH_SIZE = 8          # 8x8 tiles for operator mapping
HS_ITERATIONS = 50              # Horn-Schunck iterations
HS_ALPHA = 1.0                  # Horn-Schunck smoothness weight
MIN_FRAME_SIZE = 16             # Minimum frame dimension
MAX_FRAME_SIZE = 4096           # Maximum frame dimension
FLOW_CLIP = 50.0                # Clip extreme flow values


# ================================================================
#  HORN-SCHUNCK OPTICAL FLOW
# ================================================================

def compute_gradients(frame1: np.ndarray, frame2: np.ndarray
                      ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Compute spatial and temporal image gradients.

    Uses central differences for Ix, Iy and forward difference for It.

    Args:
        frame1: grayscale frame t   (H, W) float32
        frame2: grayscale frame t+1 (H, W) float32

    Returns:
        (Ix, Iy, It) gradient arrays, same shape as input.
    """
    # Average of both frames for spatial gradient stability
    avg = (frame1 + frame2) * 0.5

    # Spatial gradients via central differences (padded at boundaries)
    Ix = np.zeros_like(avg)
    Iy = np.zeros_like(avg)

    # X gradient (horizontal)
    Ix[:, 1:-1] = (avg[:, 2:] - avg[:, :-2]) * 0.5
    Ix[:, 0] = avg[:, 1] - avg[:, 0]
    Ix[:, -1] = avg[:, -1] - avg[:, -2]

    # Y gradient (vertical)
    Iy[1:-1, :] = (avg[2:, :] - avg[:-2, :]) * 0.5
    Iy[0, :] = avg[1, :] - avg[0, :]
    Iy[-1, :] = avg[-1, :] - avg[-2, :]

    # Temporal gradient
    It = frame2 - frame1

    return Ix, Iy, It


def horn_schunck(frame1: np.ndarray, frame2: np.ndarray,
                 alpha: float = HS_ALPHA,
                 iterations: int = HS_ITERATIONS
                 ) -> Tuple[np.ndarray, np.ndarray]:
    """Dense optical flow via Horn-Schunck method.

    Classical variational method. Minimizes:
        E = ∫∫ (Ix·u + Iy·v + It)² + α²(|∇u|² + |∇v|²) dxdy

    No neural nets. No black boxes. Just calculus of variations.

    Args:
        frame1: grayscale frame at time t   (H, W) float32
        frame2: grayscale frame at time t+1 (H, W) float32
        alpha:  smoothness weight (higher = smoother flow)
        iterations: Gauss-Seidel iterations

    Returns:
        (u, v) flow fields, same shape as input.
        u = horizontal displacement, v = vertical displacement.
    """
    Ix, Iy, It = compute_gradients(frame1, frame2)

    u = np.zeros_like(frame1)
    v = np.zeros_like(frame1)

    # Precompute denominator terms
    Ix2 = Ix * Ix
    Iy2 = Iy * Iy
    IxIy = Ix * Iy
    IxIt = Ix * It
    IyIt = Iy * It

    alpha2 = alpha * alpha

    # Laplacian kernel weights for averaging neighbors
    # Using the standard 4-connectivity average
    for _ in range(iterations):
        # Local average of flow (Laplacian approximation)
        u_avg = np.zeros_like(u)
        v_avg = np.zeros_like(v)

        # Interior
        u_avg[1:-1, 1:-1] = (
            u[:-2, 1:-1] + u[2:, 1:-1] +
            u[1:-1, :-2] + u[1:-1, 2:]
        ) * 0.25

        v_avg[1:-1, 1:-1] = (
            v[:-2, 1:-1] + v[2:, 1:-1] +
            v[1:-1, :-2] + v[1:-1, 2:]
        ) * 0.25

        # Update (Horn-Schunck Gauss-Seidel step)
        denom = alpha2 + Ix2 + Iy2
        denom = np.maximum(denom, 1e-8)  # Prevent division by zero

        P = IxIt + Ix * u_avg + Iy * v_avg + IyIt
        # Corrected: only temporal + spatial coupling
        common = (Ix * u_avg + Iy * v_avg + It) / denom

        u = u_avg - Ix * common
        v = v_avg - Iy * common

    # Clip extreme values
    u = np.clip(u, -FLOW_CLIP, FLOW_CLIP)
    v = np.clip(v, -FLOW_CLIP, FLOW_CLIP)

    return u, v


# ================================================================
#  PATCH DECOMPOSITION
# ================================================================

class FlowPatch:
    """Statistics for one tile of the flow field.

    Each patch maps to a 5D force vector for D2 processing.

    Dimensions:
        aperture   = speed magnitude (how fast)
        pressure   = vorticity (rotational tendency)
        depth      = divergence (expanding/contracting)
        binding    = spatial coherence (how uniform)
        continuity = temporal persistence (from multi-frame)
    """

    __slots__ = [
        'row', 'col', 'speed', 'direction',
        'vorticity', 'divergence', 'coherence', 'persistence',
        'force_vector',
    ]

    def __init__(self, row: int, col: int, u_patch: np.ndarray,
                 v_patch: np.ndarray, prev_speed: float = 0.0):
        self.row = row
        self.col = col

        # Speed and direction
        mag = np.sqrt(u_patch ** 2 + v_patch ** 2)
        self.speed = float(np.mean(mag))
        angles = np.arctan2(v_patch, u_patch)
        self.direction = float(_circular_mean(angles))

        # Vorticity: curl of (u, v) = dv/dx - du/dy
        self.vorticity = float(_compute_vorticity(u_patch, v_patch))

        # Divergence: du/dx + dv/dy
        self.divergence = float(_compute_divergence(u_patch, v_patch))

        # Spatial coherence: how uniform the flow direction is
        if self.speed > 1e-6:
            # Resultant length of unit direction vectors
            cos_sum = float(np.mean(np.cos(angles)))
            sin_sum = float(np.mean(np.sin(angles)))
            self.coherence = math.sqrt(cos_sum ** 2 + sin_sum ** 2)
        else:
            self.coherence = 1.0  # No motion = perfectly "coherent" stillness

        # Temporal persistence (delta from previous speed)
        self.persistence = max(0.0, 1.0 - abs(self.speed - prev_speed) * 2.0)

        # Build 5D force vector
        self.force_vector = self._to_force_vector()

    def _to_force_vector(self) -> Tuple[float, float, float, float, float]:
        """Map patch stats to 5D force: (aperture, pressure, depth, binding, continuity).

        All dimensions normalized to [-1, 1] range.
        """
        # Aperture = speed (scaled, positive)
        aperture = min(self.speed * 2.0, 1.0)

        # Pressure = vorticity (signed: positive = CCW, negative = CW)
        pressure = max(-1.0, min(1.0, self.vorticity * 5.0))

        # Depth = divergence (positive = expanding, negative = contracting)
        depth = max(-1.0, min(1.0, self.divergence * 5.0))

        # Binding = spatial coherence (0 to 1 → -1 to 1)
        binding = self.coherence * 2.0 - 1.0

        # Continuity = temporal persistence
        continuity = self.persistence * 2.0 - 1.0

        return (aperture, pressure, depth, binding, continuity)


def _compute_vorticity(u: np.ndarray, v: np.ndarray) -> float:
    """Curl of 2D vector field: dv/dx - du/dy."""
    if u.shape[0] < 2 or u.shape[1] < 2:
        return 0.0
    dvdx = np.mean(np.diff(v, axis=1))
    dudy = np.mean(np.diff(u, axis=0))
    return dvdx - dudy


def _compute_divergence(u: np.ndarray, v: np.ndarray) -> float:
    """Divergence of 2D vector field: du/dx + dv/dy."""
    if u.shape[0] < 2 or u.shape[1] < 2:
        return 0.0
    dudx = np.mean(np.diff(u, axis=1))
    dvdy = np.mean(np.diff(v, axis=0))
    return dudx + dvdy


def _circular_mean(angles: np.ndarray) -> float:
    """Mean direction of angles (handles wraparound)."""
    return float(np.arctan2(np.mean(np.sin(angles)), np.mean(np.cos(angles))))


def decompose_flow(u: np.ndarray, v: np.ndarray,
                   patch_size: int = DEFAULT_PATCH_SIZE,
                   prev_speeds: Optional[np.ndarray] = None
                   ) -> List[FlowPatch]:
    """Decompose flow field into patches with 5D force vectors.

    Args:
        u: horizontal flow (H, W)
        v: vertical flow (H, W)
        patch_size: tile size (default 8)
        prev_speeds: previous frame's speed grid for persistence (optional)

    Returns:
        List of FlowPatch objects, row-major order.
    """
    H, W = u.shape
    rows = H // patch_size
    cols = W // patch_size
    patches = []

    for r in range(rows):
        for c in range(cols):
            y0 = r * patch_size
            x0 = c * patch_size
            u_tile = u[y0:y0 + patch_size, x0:x0 + patch_size]
            v_tile = v[y0:y0 + patch_size, x0:x0 + patch_size]

            prev_spd = 0.0
            if prev_speeds is not None and r < prev_speeds.shape[0] and c < prev_speeds.shape[1]:
                prev_spd = float(prev_speeds[r, c])

            patches.append(FlowPatch(r, c, u_tile, v_tile, prev_spd))

    return patches


# ================================================================
#  FLOW TRACKER (stateful, multi-frame)
# ================================================================

class FlowTracker:
    """Stateful flow processor across multiple frames.

    Maintains frame history for temporal persistence tracking.

    Usage:
        tracker = FlowTracker(patch_size=8)
        for frame in video_frames:
            patches = tracker.feed(frame)
            # patches is a list of FlowPatch with 5D force vectors
    """

    def __init__(self, patch_size: int = DEFAULT_PATCH_SIZE,
                 alpha: float = HS_ALPHA,
                 iterations: int = HS_ITERATIONS):
        self.patch_size = patch_size
        self.alpha = alpha
        self.iterations = iterations
        self._prev_frame = None
        self._prev_speeds = None
        self._frame_count = 0

    def feed(self, frame: np.ndarray) -> Optional[List[FlowPatch]]:
        """Feed one frame. Returns patches if flow computed (needs 2+ frames).

        Args:
            frame: (H, W) grayscale float32 [0.0, 1.0]

        Returns:
            List of FlowPatch objects, or None if first frame.
        """
        frame = np.asarray(frame, dtype=np.float32)

        if self._prev_frame is None:
            self._prev_frame = frame
            self._frame_count = 1
            return None

        # Compute flow
        u, v = horn_schunck(self._prev_frame, frame,
                            alpha=self.alpha,
                            iterations=self.iterations)

        # Decompose into patches
        patches = decompose_flow(u, v, self.patch_size, self._prev_speeds)

        # Save speed grid for next frame's persistence
        H, W = u.shape
        rows = H // self.patch_size
        cols = W // self.patch_size
        speed_grid = np.zeros((rows, cols), dtype=np.float32)
        for p in patches:
            if p.row < rows and p.col < cols:
                speed_grid[p.row, p.col] = p.speed

        self._prev_speeds = speed_grid
        self._prev_frame = frame
        self._frame_count += 1

        return patches

    @property
    def frame_count(self) -> int:
        return self._frame_count

    def reset(self):
        """Clear state for new video."""
        self._prev_frame = None
        self._prev_speeds = None
        self._frame_count = 0


# ================================================================
#  SYNTHETIC CLOUD GENERATORS (for testing)
# ================================================================

def generate_uniform_flow(H: int, W: int, dx: float, dy: float
                          ) -> Tuple[np.ndarray, np.ndarray]:
    """Pure translation flow field. Stable clouds drifting."""
    u = np.full((H, W), dx, dtype=np.float32)
    v = np.full((H, W), dy, dtype=np.float32)
    return u, v


def generate_vortex_flow(H: int, W: int, strength: float = 1.0
                         ) -> Tuple[np.ndarray, np.ndarray]:
    """Rotational flow centered on frame. Cloud vortex."""
    cy, cx = H / 2.0, W / 2.0
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    dx = x - cx
    dy = y - cy
    r = np.sqrt(dx ** 2 + dy ** 2) + 1e-6
    u = -strength * dy / r
    v = strength * dx / r
    return u.astype(np.float32), v.astype(np.float32)


def generate_expanding_flow(H: int, W: int, rate: float = 0.5
                            ) -> Tuple[np.ndarray, np.ndarray]:
    """Expanding/diverging flow. Cloud dissipation."""
    cy, cx = H / 2.0, W / 2.0
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    u = rate * (x - cx) / max(W, 1)
    v = rate * (y - cy) / max(H, 1)
    return u.astype(np.float32), v.astype(np.float32)


def generate_turbulent_flow(H: int, W: int, scale: float = 1.0,
                            seed: int = 42
                            ) -> Tuple[np.ndarray, np.ndarray]:
    """Random turbulent flow. Chaotic cloud formations."""
    rng = np.random.RandomState(seed)
    u = rng.randn(H, W).astype(np.float32) * scale
    v = rng.randn(H, W).astype(np.float32) * scale
    return u, v


def generate_cloud_frame_pair(H: int, W: int, flow_type: str = 'uniform',
                               strength: float = 0.5, seed: int = 42
                               ) -> Tuple[np.ndarray, np.ndarray]:
    """Generate a synthetic frame pair with known flow.

    Creates frame1 as random cloud texture, then warps it by the
    specified flow to create frame2.

    Args:
        H, W: frame dimensions
        flow_type: 'uniform', 'vortex', 'expanding', 'turbulent'
        strength: flow magnitude
        seed: random seed for reproducibility

    Returns:
        (frame1, frame2) grayscale float32 [0.0, 1.0]
    """
    rng = np.random.RandomState(seed)

    # Cloud-like texture: low-frequency Gaussian noise
    # Simple approach: smooth random field
    raw = rng.randn(H, W).astype(np.float32)
    # Box-filter smooth (simple, no scipy dependency)
    kernel_size = max(3, min(H, W) // 8)
    frame1 = _box_filter(raw, kernel_size)
    # Normalize to [0, 1]
    fmin, fmax = frame1.min(), frame1.max()
    if fmax > fmin:
        frame1 = (frame1 - fmin) / (fmax - fmin)
    else:
        frame1 = np.full_like(frame1, 0.5)

    # Generate flow
    if flow_type == 'vortex':
        u, v = generate_vortex_flow(H, W, strength)
    elif flow_type == 'expanding':
        u, v = generate_expanding_flow(H, W, strength)
    elif flow_type == 'turbulent':
        u, v = generate_turbulent_flow(H, W, strength, seed)
    else:
        u, v = generate_uniform_flow(H, W, strength * 2.0, strength)

    # Warp frame1 by flow to create frame2
    frame2 = _warp_frame(frame1, u, v)

    return frame1, frame2


def _box_filter(img: np.ndarray, k: int) -> np.ndarray:
    """Simple box filter for smoothing. No external deps."""
    if k < 2:
        return img.copy()
    result = img.copy()
    # Horizontal pass
    cumsum = np.cumsum(result, axis=1)
    result[:, k:] = cumsum[:, k:] - cumsum[:, :-k]
    result[:, k:] /= k
    result[:, :k] = np.cumsum(result[:, :k], axis=1) / np.arange(1, k + 1)
    # Vertical pass
    cumsum = np.cumsum(result, axis=0)
    result[k:, :] = cumsum[k:, :] - cumsum[:-k, :]
    result[k:, :] /= k
    result[:k, :] = np.cumsum(result[:k, :], axis=0) / np.arange(1, k + 1).reshape(-1, 1)
    return result


def _warp_frame(frame: np.ndarray, u: np.ndarray, v: np.ndarray
                ) -> np.ndarray:
    """Warp frame by flow field using bilinear interpolation."""
    H, W = frame.shape
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)

    # Source coordinates
    sx = x - u
    sy = y - v

    # Clamp to frame bounds
    sx = np.clip(sx, 0, W - 1.001)
    sy = np.clip(sy, 0, H - 1.001)

    # Bilinear interpolation
    x0 = np.floor(sx).astype(np.int32)
    y0 = np.floor(sy).astype(np.int32)
    x1 = np.minimum(x0 + 1, W - 1)
    y1 = np.minimum(y0 + 1, H - 1)

    wx = sx - x0
    wy = sy - y0

    result = (frame[y0, x0] * (1 - wx) * (1 - wy) +
              frame[y0, x1] * wx * (1 - wy) +
              frame[y1, x0] * (1 - wx) * wy +
              frame[y1, x1] * wx * wy)

    return result.astype(np.float32)


# ================================================================
#  CLI: Demo
# ================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("CK CLOUD FLOW -- Optical Flow Extraction")
    print("=" * 60)

    H, W = 64, 64

    for flow_type in ['uniform', 'vortex', 'expanding', 'turbulent']:
        f1, f2 = generate_cloud_frame_pair(H, W, flow_type, strength=0.5)
        u, v = horn_schunck(f1, f2, iterations=30)
        patches = decompose_flow(u, v, patch_size=8)

        speeds = [p.speed for p in patches]
        avg_speed = sum(speeds) / len(speeds) if speeds else 0.0
        vorts = [abs(p.vorticity) for p in patches]
        avg_vort = sum(vorts) / len(vorts) if vorts else 0.0

        print(f"\n  {flow_type:12s}: {len(patches)} patches, "
              f"avg_speed={avg_speed:.4f}, avg_vort={avg_vort:.4f}")

        # Show first patch force vector
        if patches:
            p = patches[0]
            fv = p.force_vector
            print(f"    patch[0,0] force: "
                  f"({fv[0]:.3f}, {fv[1]:.3f}, {fv[2]:.3f}, "
                  f"{fv[3]:.3f}, {fv[4]:.3f})")

    # Multi-frame test
    tracker = FlowTracker(patch_size=8)
    for i in range(5):
        f, _ = generate_cloud_frame_pair(H, W, 'vortex', strength=0.3 + i * 0.1, seed=i)
        result = tracker.feed(f)
        if result:
            print(f"\n  Frame {i}: {len(result)} patches computed")

    print(f"\n{'=' * 60}")
    print("  Cloud flow extraction ready. Pure NumPy, zero CV deps.")
    print(f"{'=' * 60}")
