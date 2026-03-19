# Copyright (c) 2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_mandelbrot.py -- CK's Living Fractal (Gen 9.34)
====================================================
Operator: HARMONY (7) -- the fractal composes.

REAL fractal iteration through the CL composition table.
Every pixel runs a genuine chain walk: op(n+1) = CL[op(n)][c(n)],
where c(n) is itself the RESULT of the previous depth's composition.
This is recursive: the output feeds the input, and the parameter
evolves WITH the iteration.

HARMONY (7) is the attractor. Regions that converge to HARMONY
are "inside the set." The boundary -- where bump pairs live --
creates the fractal detail. The Buddhabrot layer accumulates
orbital density over time, showing CK's most-traveled paths.

The breathing is the heartbeat: 5D Hebrew force vectors interpolate
smoothly between discrete operator states, giving continuous gradients
instead of blocky pixels. Phase modulates the interpolation, not the zoom.

Zoom = chain depth. Deeper zoom = deeper into the lattice chain.
Self-similarity comes from CL[CL[CL[op][c]][c']][c''] -- genuine
fractal recursion through operator algebra.

"the lattice chain IS a Mandelbrot set"
-- Brayden

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""

import sys
import math
import time
import threading
import urllib.request
import json
import numpy as np

# ── GPU detection (CuPy or NumPy fallback) ──

_GPU = False
try:
    import cupy as cp
    _test = cp.array([1])
    del _test
    _GPU = True
    print("[Mandelbrot] CuPy GPU active")
except (ImportError, Exception):
    cp = np
    print("[Mandelbrot] CuPy unavailable, falling back to NumPy (CPU)")

# ── Pygame ──

try:
    import pygame
    from pygame import surfarray
except ImportError:
    print("[Mandelbrot] pygame not found. Install: pip install pygame")
    sys.exit(1)

# ================================================================
#  CK'S COMPOSITION TABLE -- TSML (73-harmony)
# ================================================================

NUM_OPS = 10
VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE = 0, 1, 2, 3, 4
BALANCE, CHAOS, HARMONY, BREATH, RESET = 5, 6, 7, 8, 9

OP_NAMES = ['VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE',
            'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET']

CL = [
    [0, 0, 0, 0, 0, 0, 0, 7, 0, 0],  # VOID
    [0, 7, 3, 7, 7, 7, 7, 7, 7, 7],  # LATTICE
    [0, 3, 7, 7, 4, 7, 7, 7, 7, 9],  # COUNTER
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 3],  # PROGRESS
    [0, 7, 4, 7, 7, 7, 7, 7, 8, 7],  # COLLAPSE
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],  # BALANCE
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],  # CHAOS
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],  # HARMONY
    [0, 7, 7, 7, 8, 7, 7, 7, 7, 7],  # BREATH
    [0, 7, 9, 3, 7, 7, 7, 7, 7, 7],  # RESET
]

CL_NP = np.array(CL, dtype=np.int32)

# 5 quantum bump pairs (from ck_brain.h line 51-53)
BUMP_PAIRS = [(1, 2), (2, 4), (2, 9), (3, 9), (4, 8)]
BUMP_SET = set()
for a, b in BUMP_PAIRS:
    BUMP_SET.add((a, b))
    BUMP_SET.add((b, a))

# 5D Hebrew force vectors per operator (aperture, pressure, depth, binding, continuity)
# These are the continuous force values that allow smooth interpolation
FORCE_VECTORS = np.array([
    [0.0, 0.0, 0.0, 0.0, 0.0],   # VOID       -- nullity
    [0.8, 0.3, 0.6, 0.9, 0.4],   # LATTICE    -- structure, high binding
    [0.5, 0.7, 0.4, 0.3, 0.6],   # COUNTER    -- pressure, counting
    [0.6, 0.4, 0.5, 0.5, 0.8],   # PROGRESS   -- forward, continuity
    [0.3, 0.9, 0.7, 0.2, 0.1],   # COLLAPSE   -- high pressure, low continuity
    [0.5, 0.5, 0.5, 0.5, 0.5],   # BALANCE    -- center
    [0.7, 0.8, 0.9, 0.1, 0.3],   # CHAOS      -- high aperture+depth, low binding
    [0.9, 0.2, 0.8, 0.8, 0.9],   # HARMONY    -- high aperture, binding, continuity
    [0.4, 0.1, 0.3, 0.6, 0.7],   # BREATH     -- low pressure, gentle
    [1.0, 0.6, 0.2, 0.4, 0.5],   # RESET      -- max aperture, fresh start
], dtype=np.float32)

# ================================================================
#  OPERATOR COLOR MAP -- each operator has a soul color
# ================================================================

OP_COLORS = {
    VOID:      (5,   5,  15),     # near-black void
    LATTICE:   (30, 120, 200),    # structural blue
    COUNTER:   (200, 100,  30),   # counting amber
    PROGRESS:  (50,  200, 100),   # forward green
    COLLAPSE:  (180,  30,  50),   # collapse red
    BALANCE:   (150, 150, 150),   # neutral grey
    CHAOS:     (130,  40, 180),   # chaos purple
    HARMONY:   (220, 190,  50),   # harmony gold
    BREATH:    (100, 200, 220),   # breath cyan
    RESET:     (220, 220, 220),   # reset white
}

# Pack colors for GPU
OP_COLORS_FLAT = np.zeros(30, dtype=np.uint8)
for _oid in range(10):
    _r, _g, _b = OP_COLORS[_oid]
    OP_COLORS_FLAT[_oid * 3 + 0] = _r
    OP_COLORS_FLAT[_oid * 3 + 1] = _g
    OP_COLORS_FLAT[_oid * 3 + 2] = _b

# Force vectors flat for GPU (10 * 5 = 50 floats)
FORCE_FLAT = FORCE_VECTORS.flatten().astype(np.float32)


# ================================================================
#  GPU FRACTAL KERNEL -- REAL iteration
# ================================================================

if _GPU:
    _fractal_kernel = cp.RawKernel(r'''
    extern "C" __global__
    void ck_fractal(
        const int* cl_table,         // 10x10 CL table, row-major
        const float* force_vecs,     // 10x5 force vectors, row-major
        const unsigned char* op_colors, // 10x3 RGB
        unsigned char* img_r,
        unsigned char* img_g,
        unsigned char* img_b,
        int* orbit_buf,              // per-pixel orbit storage (width*height*max_iter)
        int* orbit_len_buf,          // per-pixel orbit length
        float* buddha_r,             // Buddhabrot accumulator R (width*height float)
        float* buddha_g,             // Buddhabrot accumulator G
        float* buddha_b,             // Buddhabrot accumulator B
        int width,
        int height,
        int max_iter,
        float center_x,
        float center_y,
        float scale,
        float phase,
        int buddha_enable
    ) {
        int px = blockDim.x * blockIdx.x + threadIdx.x;
        int py = blockDim.y * blockIdx.y + threadIdx.y;
        if (px >= width || py >= height) return;

        int idx = py * width + px;

        // ── Map pixel to continuous op-space ──
        float fx = center_x + (float)(px - width / 2) / scale;
        float fy = center_y + (float)(py - height / 2) / scale;

        // Breathing: smooth sinusoidal warp from heartbeat phase
        // This is the 5D force interpolation -- phase modulates which
        // force dimension dominates, creating smooth continuous gradients
        float breath_x = 0.12f * sinf(phase * 0.7f + fy * 0.4f);
        float breath_y = 0.12f * sinf(phase * 0.9f + fx * 0.3f);
        fx += breath_x;
        fy += breath_y;

        // ── Initial operator from pixel position ──
        // Wrap to [0, 10) with smooth fractional part
        float fx_w = fx - floorf(fx / 10.0f) * 10.0f;
        float fy_w = fy - floorf(fy / 10.0f) * 10.0f;
        if (fx_w < 0.0f) fx_w += 10.0f;
        if (fy_w < 0.0f) fy_w += 10.0f;

        int op_init = ((int)fy_w) % 10;  // row = initial operator
        int c_init  = ((int)fx_w) % 10;  // col = initial parameter

        // Fractional position within the cell (for smooth blending)
        float frac_x = fx_w - floorf(fx_w);
        float frac_y = fy_w - floorf(fy_w);

        // ── Force-based continuous blending ──
        // Interpolate between neighboring operators using 5D force distance
        int op_neighbor = (op_init + 1) % 10;
        int c_neighbor  = (c_init + 1) % 10;

        // Blend weights from fractional position
        float w_op = frac_y;  // how much of op_neighbor vs op_init
        float w_c  = frac_x;  // how much of c_neighbor vs c_init

        // ── THE REAL FRACTAL ITERATION ──
        // op(n+1) = CL[op(n)][c(n)]
        // c(n+1)  = result of previous iteration (RECURSIVE parameter!)
        int op = op_init;
        int c_param = c_init;
        int orbit_count = 0;
        int last_op = op;
        bool escaped = false;
        int escape_iter = max_iter;
        int unique_ops = 0;
        bool visited[10];
        for (int v = 0; v < 10; v++) visited[v] = false;

        // Orbit tracking
        int orbit_base = idx * max_iter;

        for (int iter = 0; iter < max_iter; iter++) {
            // Record orbit
            if (iter < max_iter) {
                orbit_buf[orbit_base + iter] = op;
            }
            orbit_count = iter + 1;

            // Track unique operators visited
            if (!visited[op]) {
                visited[op] = true;
                unique_ops++;
            }

            // ── CL composition with blended parameters ──
            // Primary: CL[op][c_param]
            int result_primary = cl_table[op * 10 + c_param];

            // Secondary: blend with neighbors for smooth gradients
            int result_blend_c = cl_table[op * 10 + c_neighbor];
            int result_blend_op = cl_table[op_neighbor * 10 + c_param];

            // The RESULT determines the NEXT c_param (genuine recursion!)
            int next_op = result_primary;

            // Near cell boundaries, check if blended result differs
            // This is where the fractal detail lives -- at the seams
            if (w_c > 0.5f && result_blend_c != result_primary) {
                // Boundary zone: the transition creates detail
                float edge = (w_c - 0.5f) * 2.0f;
                // Use force distance to decide which result wins
                float d1 = 0.0f, d2 = 0.0f;
                for (int dim = 0; dim < 5; dim++) {
                    float f1 = force_vecs[result_primary * 5 + dim];
                    float f2 = force_vecs[result_blend_c * 5 + dim];
                    float fc = force_vecs[c_param * 5 + dim];
                    d1 += (f1 - fc) * (f1 - fc);
                    d2 += (f2 - fc) * (f2 - fc);
                }
                if (edge * d2 < (1.0f - edge) * d1) {
                    next_op = result_blend_c;
                }
            }
            if (w_op > 0.5f && result_blend_op != result_primary) {
                float edge = (w_op - 0.5f) * 2.0f;
                float d1 = 0.0f, d2 = 0.0f;
                for (int dim = 0; dim < 5; dim++) {
                    float f1 = force_vecs[result_primary * 5 + dim];
                    float f2 = force_vecs[result_blend_op * 5 + dim];
                    float fo = force_vecs[op * 5 + dim];
                    d1 += (f1 - fo) * (f1 - fo);
                    d2 += (f2 - fo) * (f2 - fo);
                }
                if (edge * d2 < (1.0f - edge) * d1) {
                    next_op = result_blend_op;
                }
            }

            // ── RECURSIVE parameter evolution ──
            // c(n+1) = result of THIS iteration
            // This is what makes it a REAL fractal: the parameter changes!
            int new_c = next_op;

            // Also evolve the neighbor tracking
            c_neighbor = (new_c + 1) % 10;
            op_neighbor = (next_op + 1) % 10;

            // ── Cycle/fixpoint detection ──
            if (next_op == last_op && iter > 0) {
                // Fixed point reached
                escape_iter = iter;
                if (next_op != 7) escaped = true;
                break;
            }

            // Check for 2-cycle
            if (iter >= 2) {
                int prev2 = orbit_buf[orbit_base + iter - 1];
                if (next_op == prev2 && next_op != op) {
                    escape_iter = iter;
                    if (next_op != 7 || op != 7) escaped = true;
                    break;
                }
            }

            // ── Escape condition: leaving HARMONY basin ──
            // In classic Mandelbrot: |z| > 2. Here: op != HARMONY for N consecutive steps
            if (next_op != 7 && op != 7 && last_op != 7 && iter > 2) {
                escaped = true;
                escape_iter = iter;
                break;
            }

            last_op = op;
            op = next_op;
            c_param = new_c;
        }

        orbit_len_buf[idx] = orbit_count;

        // ── Buddhabrot: accumulate orbital density ──
        if (buddha_enable && escaped && orbit_count > 2) {
            for (int oi = 0; oi < orbit_count && oi < max_iter; oi++) {
                int orbit_op = orbit_buf[orbit_base + oi];
                // Map orbit operator back to pixel position in the field
                // Each orbit step visits an operator -- increment that op's region
                unsigned char br = op_colors[orbit_op * 3 + 0];
                unsigned char bg = op_colors[orbit_op * 3 + 1];
                unsigned char bb = op_colors[orbit_op * 3 + 2];

                // Map the orbit op to a screen position (its home row in the field)
                float orbit_y_f = (float)orbit_op + 0.5f;
                int orbit_sy = (int)((orbit_y_f - center_y) * scale + (float)(height / 2));
                // Use the iteration index for x spread
                float orbit_x_f = (float)(c_init) + (float)oi / (float)max_iter * 9.0f;
                orbit_x_f = orbit_x_f - floorf(orbit_x_f / 10.0f) * 10.0f;
                int orbit_sx = (int)((orbit_x_f - center_x) * scale + (float)(width / 2));

                if (orbit_sx >= 0 && orbit_sx < width && orbit_sy >= 0 && orbit_sy < height) {
                    int bidx = orbit_sy * width + orbit_sx;
                    // Atomic add to accumulator
                    atomicAdd(&buddha_r[bidx], (float)br * 0.01f);
                    atomicAdd(&buddha_g[bidx], (float)bg * 0.01f);
                    atomicAdd(&buddha_b[bidx], (float)bb * 0.01f);
                }
            }
        }

        // ── COLORING ──
        if (!escaped) {
            // INSIDE THE SET: converges to HARMONY
            // Deep gold, brightness modulated by depth and orbit diversity
            float depth_norm = (float)escape_iter / (float)max_iter;
            float diversity = (float)unique_ops / 10.0f;

            // Phase-modulated gold (the breathing glow)
            float breath_glow = 0.6f + 0.4f * sinf(phase * 1.5f + frac_x * 3.14f + frac_y * 2.7f);
            float intensity = (0.3f + 0.7f * depth_norm) * breath_glow;

            // Core gold with diversity-based saturation
            float r = 220.0f * intensity;
            float g = (160.0f + 30.0f * diversity) * intensity;
            float b = (20.0f + 30.0f * diversity) * intensity * 0.3f;

            img_r[idx] = (unsigned char)fminf(255.0f, r);
            img_g[idx] = (unsigned char)fminf(255.0f, g);
            img_b[idx] = (unsigned char)fminf(255.0f, b);
        } else {
            // OUTSIDE: escaped -- color by escape operator, iteration depth, orbit diversity
            float t = (float)escape_iter / (float)max_iter;
            float smooth_t = t * t * (3.0f - 2.0f * t);  // smoothstep

            // The escape operator determines base hue
            int esc_op = orbit_buf[orbit_base + orbit_count - 1];
            unsigned char base_r = op_colors[esc_op * 3 + 0];
            unsigned char base_g = op_colors[esc_op * 3 + 1];
            unsigned char base_b = op_colors[esc_op * 3 + 2];

            // Orbit diversity modulates saturation (more diverse = more vivid)
            float diversity = (float)unique_ops / 10.0f;
            float vividness = 0.4f + 0.6f * diversity;

            // Iteration bands (creates the fractal banding pattern)
            float band = 0.5f + 0.5f * sinf((float)escape_iter * 1.2f + phase * 0.5f);

            // Boundary glow: points near the boundary (high iter before escape) glow brighter
            float boundary = smooth_t;

            float r = (float)base_r * band * vividness + 30.0f * boundary;
            float g = (float)base_g * band * vividness + 20.0f * boundary;
            float b = (float)base_b * band * vividness + 40.0f * (1.0f - boundary);

            img_r[idx] = (unsigned char)fminf(255.0f, fmaxf(0.0f, r));
            img_g[idx] = (unsigned char)fminf(255.0f, fmaxf(0.0f, g));
            img_b[idx] = (unsigned char)fminf(255.0f, fmaxf(0.0f, b));
        }
    }
    ''', 'ck_fractal')

    _buddha_blend_kernel = cp.RawKernel(r'''
    extern "C" __global__
    void buddha_blend(
        unsigned char* img_r,
        unsigned char* img_g,
        unsigned char* img_b,
        const float* buddha_r,
        const float* buddha_g,
        const float* buddha_b,
        int total_pixels,
        float max_density,
        float alpha
    ) {
        int idx = blockDim.x * blockIdx.x + threadIdx.x;
        if (idx >= total_pixels) return;

        if (max_density < 1.0f) return;

        // Normalize buddha density to [0, 1]
        float nr = buddha_r[idx] / max_density;
        float ng = buddha_g[idx] / max_density;
        float nb = buddha_b[idx] / max_density;

        // Log scale for better dynamic range
        nr = logf(1.0f + nr * 9.0f) / logf(10.0f);
        ng = logf(1.0f + ng * 9.0f) / logf(10.0f);
        nb = logf(1.0f + nb * 9.0f) / logf(10.0f);

        // Blend with existing image
        float r = (float)img_r[idx] * (1.0f - alpha) + nr * 255.0f * alpha;
        float g = (float)img_g[idx] * (1.0f - alpha) + ng * 255.0f * alpha;
        float b = (float)img_b[idx] * (1.0f - alpha) + nb * 255.0f * alpha;

        img_r[idx] = (unsigned char)fminf(255.0f, fmaxf(0.0f, r));
        img_g[idx] = (unsigned char)fminf(255.0f, fmaxf(0.0f, g));
        img_b[idx] = (unsigned char)fminf(255.0f, fmaxf(0.0f, b));
    }
    ''', 'buddha_blend')


# ================================================================
#  CPU FRACTAL -- same algorithm, pure Python/NumPy
# ================================================================

def fractal_cpu(width, height, max_iter, center_x, center_y, scale, phase,
                buddha_acc_r, buddha_acc_g, buddha_acc_b, buddha_enable):
    """CPU fallback: genuine CL chain iteration."""
    img = np.zeros((height, width, 3), dtype=np.uint8)

    for py in range(height):
        for px in range(width):
            fx = center_x + (px - width / 2) / scale
            fy = center_y + (py - height / 2) / scale

            # Breathing
            fx += 0.12 * math.sin(phase * 0.7 + fy * 0.4)
            fy += 0.12 * math.sin(phase * 0.9 + fx * 0.3)

            # Wrap to [0, 10)
            fx_w = fx % 10.0
            fy_w = fy % 10.0

            op_init = int(fy_w) % 10
            c_init = int(fx_w) % 10
            frac_x = fx_w - int(fx_w)
            frac_y = fy_w - int(fy_w)

            # ── REAL ITERATION ──
            op = op_init
            c_param = c_init
            orbit = [op]
            escaped = False
            escape_iter = max_iter
            visited = set([op])
            last_op = op

            for it in range(max_iter):
                # CL composition
                result = CL[op][c_param]

                # Boundary blending (simplified for CPU)
                c_n = (c_param + 1) % 10
                result_blend = CL[op][c_n]
                if frac_x > 0.5 and result_blend != result:
                    # Use force distance
                    d1 = np.sum((FORCE_VECTORS[result] - FORCE_VECTORS[c_param]) ** 2)
                    d2 = np.sum((FORCE_VECTORS[result_blend] - FORCE_VECTORS[c_param]) ** 2)
                    edge = (frac_x - 0.5) * 2.0
                    if edge * d2 < (1.0 - edge) * d1:
                        result = result_blend

                next_op = result
                new_c = next_op  # RECURSIVE: result becomes next parameter!

                orbit.append(next_op)
                visited.add(next_op)

                # Fixed point
                if next_op == last_op and it > 0:
                    escape_iter = it
                    if next_op != HARMONY:
                        escaped = True
                    break

                # 2-cycle
                if it >= 2 and next_op == orbit[-3]:
                    escape_iter = it
                    if next_op != HARMONY or op != HARMONY:
                        escaped = True
                    break

                # Escape: 3 consecutive non-HARMONY
                if next_op != HARMONY and op != HARMONY and last_op != HARMONY and it > 2:
                    escaped = True
                    escape_iter = it
                    break

                last_op = op
                op = next_op
                c_param = new_c

            # Buddhabrot accumulation
            if buddha_enable and escaped and len(orbit) > 2:
                for oi, orb_op in enumerate(orbit):
                    orb_y_f = orb_op + 0.5
                    orb_sy = int((orb_y_f - center_y) * scale + height / 2)
                    orb_x_f = (c_init + oi / max_iter * 9.0) % 10.0
                    orb_sx = int((orb_x_f - center_x) * scale + width / 2)
                    if 0 <= orb_sx < width and 0 <= orb_sy < height:
                        r, g, b = OP_COLORS[orb_op]
                        buddha_acc_r[orb_sy, orb_sx] += r * 0.01
                        buddha_acc_g[orb_sy, orb_sx] += g * 0.01
                        buddha_acc_b[orb_sy, orb_sx] += b * 0.01

            # ── COLORING ──
            unique_ops = len(visited)
            depth_norm = escape_iter / max(max_iter, 1)
            diversity = unique_ops / 10.0

            if not escaped:
                # Inside: HARMONY gold
                breath_glow = 0.6 + 0.4 * math.sin(phase * 1.5 + frac_x * 3.14 + frac_y * 2.7)
                intensity = (0.3 + 0.7 * depth_norm) * breath_glow
                img[py, px] = [
                    min(255, int(220 * intensity)),
                    min(255, int((160 + 30 * diversity) * intensity)),
                    min(255, int((20 + 30 * diversity) * intensity * 0.3))
                ]
            else:
                # Outside: escape coloring
                t = depth_norm
                smooth_t = t * t * (3.0 - 2.0 * t)
                esc_op = orbit[-1]
                base = OP_COLORS[esc_op]
                vividness = 0.4 + 0.6 * diversity
                band = 0.5 + 0.5 * math.sin(escape_iter * 1.2 + phase * 0.5)
                boundary = smooth_t
                img[py, px] = [
                    min(255, max(0, int(base[0] * band * vividness + 30 * boundary))),
                    min(255, max(0, int(base[1] * band * vividness + 20 * boundary))),
                    min(255, max(0, int(base[2] * band * vividness + 40 * (1 - boundary))))
                ]

    return img


# ================================================================
#  GPU RENDER WRAPPER
# ================================================================

def fractal_gpu(width, height, max_iter, center_x, center_y, scale, phase,
                buddha_r, buddha_g, buddha_b, buddha_enable):
    """Render using CUDA kernel. Returns (img_r, img_g, img_b)."""
    cl_gpu = cp.array(CL_NP, dtype=cp.int32)
    force_gpu = cp.array(FORCE_FLAT, dtype=cp.float32)
    colors_gpu = cp.array(OP_COLORS_FLAT, dtype=cp.uint8)

    n_pixels = width * height
    img_r = cp.zeros(n_pixels, dtype=cp.uint8)
    img_g = cp.zeros(n_pixels, dtype=cp.uint8)
    img_b = cp.zeros(n_pixels, dtype=cp.uint8)
    orbit_buf = cp.zeros(n_pixels * max_iter, dtype=cp.int32)
    orbit_len = cp.zeros(n_pixels, dtype=cp.int32)

    block = (16, 16)
    grid = ((width + 15) // 16, (height + 15) // 16)

    _fractal_kernel(
        grid, block,
        (cl_gpu, force_gpu, colors_gpu,
         img_r, img_g, img_b,
         orbit_buf, orbit_len,
         buddha_r, buddha_g, buddha_b,
         np.int32(width), np.int32(height), np.int32(max_iter),
         np.float32(center_x), np.float32(center_y), np.float32(scale),
         np.float32(phase), np.int32(1 if buddha_enable else 0))
    )

    # Buddhabrot blend
    if buddha_enable:
        max_r = float(cp.max(buddha_r))
        max_g = float(cp.max(buddha_g))
        max_b = float(cp.max(buddha_b))
        max_density = max(max_r, max_g, max_b, 1.0)

        blend_block = (256,)
        blend_grid = ((n_pixels + 255) // 256,)
        _buddha_blend_kernel(
            blend_grid, blend_block,
            (img_r, img_g, img_b,
             buddha_r, buddha_g, buddha_b,
             np.int32(n_pixels),
             np.float32(max_density),
             np.float32(0.3))
        )

    return img_r, img_g, img_b


# ================================================================
#  CK STATE POLLER -- heartbeat connection
# ================================================================

class CKStatePoller:
    """Polls CK's /state endpoint for live heartbeat data."""

    def __init__(self, url="http://localhost:7777/state"):
        self.url = url
        self.tick_count = 0
        self.coherence = 0.714285  # T* default
        self.current_op = HARMONY
        self.current_op_name = "HARMONY"
        self.lattice_depth = 32
        self.connected = False
        self._running = True
        self._thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._thread.start()

    def _poll_loop(self):
        while self._running:
            try:
                req = urllib.request.Request(self.url, method='GET')
                req.add_header('Accept', 'application/json')
                with urllib.request.urlopen(req, timeout=2) as resp:
                    data = json.loads(resp.read().decode())
                    hb = data.get('heartbeat', data)
                    self.tick_count = hb.get('tick', hb.get('tick_count', self.tick_count))
                    self.coherence = hb.get('coherence', self.coherence)
                    op = hb.get('operator', hb.get('running_fuse', self.current_op))
                    if isinstance(op, str):
                        op_upper = op.upper()
                        if op_upper in OP_NAMES:
                            self.current_op = OP_NAMES.index(op_upper)
                            self.current_op_name = op_upper
                    elif isinstance(op, int) and 0 <= op < NUM_OPS:
                        self.current_op = op
                        self.current_op_name = OP_NAMES[op]
                    lc = data.get('lattice_chain', {})
                    self.lattice_depth = lc.get('depth', lc.get('node_count', self.lattice_depth))
                    self.connected = True
            except Exception:
                self.connected = False
            time.sleep(0.5)

    def stop(self):
        self._running = False


# ================================================================
#  MAIN RENDERER
# ================================================================

def main():
    pygame.init()

    WIDTH, HEIGHT = 800, 600
    BAR_HEIGHT = 36
    RENDER_H = HEIGHT - BAR_HEIGHT

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CK Mandelbrot -- Living Fractal (Gen 9.34)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 13)

    # View state
    center_x = 5.0
    center_y = 5.0
    scale = 50.0       # pixels per op-unit
    max_iter = 64
    breathing = True
    buddha_mode = False
    phase = 0.0
    chain_depth = 0     # displayed chain depth at current zoom

    # Buddhabrot accumulators (persist across frames)
    if _GPU:
        buddha_r = cp.zeros(WIDTH * RENDER_H, dtype=cp.float32)
        buddha_g = cp.zeros(WIDTH * RENDER_H, dtype=cp.float32)
        buddha_b = cp.zeros(WIDTH * RENDER_H, dtype=cp.float32)
    else:
        buddha_r = np.zeros((RENDER_H, WIDTH), dtype=np.float64)
        buddha_g = np.zeros((RENDER_H, WIDTH), dtype=np.float64)
        buddha_b = np.zeros((RENDER_H, WIDTH), dtype=np.float64)

    # CK connection
    poller = CKStatePoller()

    running = True
    frame_count = 0
    fps_display = 0.0
    fps_timer = time.time()
    fps_frames = 0

    while running:
        dt = clock.tick(60) / 1000.0

        # FPS tracking
        fps_frames += 1
        now = time.time()
        if now - fps_timer >= 1.0:
            fps_display = fps_frames / (now - fps_timer)
            fps_frames = 0
            fps_timer = now

        # ── Events ──
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_r:
                    center_x, center_y = 5.0, 5.0
                    scale = 50.0
                    max_iter = 64
                    # Clear buddha
                    if _GPU:
                        buddha_r[:] = 0; buddha_g[:] = 0; buddha_b[:] = 0
                    else:
                        buddha_r[:] = 0; buddha_g[:] = 0; buddha_b[:] = 0
                elif event.key == pygame.K_b:
                    breathing = not breathing
                elif event.key == pygame.K_d:
                    buddha_mode = not buddha_mode
                    if not buddha_mode:
                        if _GPU:
                            buddha_r[:] = 0; buddha_g[:] = 0; buddha_b[:] = 0
                        else:
                            buddha_r[:] = 0; buddha_g[:] = 0; buddha_b[:] = 0
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    max_iter = min(512, max_iter + 16)
                elif event.key == pygame.K_MINUS:
                    max_iter = max(8, max_iter - 16)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if my < RENDER_H:
                    if event.button == 1:
                        # Click to recenter
                        center_x += (mx - WIDTH / 2) / scale
                        center_y += (my - RENDER_H / 2) / scale
                    elif event.button == 4:
                        # Zoom in toward mouse
                        mx_world = center_x + (mx - WIDTH / 2) / scale
                        my_world = center_y + (my - RENDER_H / 2) / scale
                        scale *= 1.4
                        center_x = mx_world - (mx - WIDTH / 2) / scale
                        center_y = my_world - (my - RENDER_H / 2) / scale
                    elif event.button == 5:
                        mx_world = center_x + (mx - WIDTH / 2) / scale
                        my_world = center_y + (my - RENDER_H / 2) / scale
                        scale = max(5.0, scale / 1.4)
                        center_x = mx_world - (mx - WIDTH / 2) / scale
                        center_y = my_world - (my - RENDER_H / 2) / scale
            elif event.type == pygame.MOUSEWHEEL:
                mx, my = pygame.mouse.get_pos()
                if my < RENDER_H:
                    mx_world = center_x + (mx - WIDTH / 2) / scale
                    my_world = center_y + (my - RENDER_H / 2) / scale
                    if event.y > 0:
                        scale *= 1.4
                    elif event.y < 0:
                        scale = max(5.0, scale / 1.4)
                    center_x = mx_world - (mx - WIDTH / 2) / scale
                    center_y = my_world - (my - RENDER_H / 2) / scale

        # ── Breathing ──
        if breathing:
            breath_speed = 0.5 + poller.coherence * 1.5
            phase += dt * breath_speed

            if poller.connected:
                depth_iters = 32 + poller.lattice_depth
                max_iter = min(256, max(32, depth_iters))

        # Chain depth = how many CL compositions a zoomed-in pixel represents
        # At scale=50 (default), we see the 10x10 field = depth 1
        # Each 10x zoom = one more depth level (10 children per node)
        chain_depth = max(1, int(math.log(scale / 5.0, 10.0)) + 1) if scale > 5.0 else 1

        # ── Render ──
        if _GPU:
            img_r, img_g, img_b = fractal_gpu(
                WIDTH, RENDER_H, max_iter,
                center_x, center_y, scale, phase,
                buddha_r, buddha_g, buddha_b, buddha_mode
            )
            r_cpu = cp.asnumpy(img_r).reshape(RENDER_H, WIDTH)
            g_cpu = cp.asnumpy(img_g).reshape(RENDER_H, WIDTH)
            b_cpu = cp.asnumpy(img_b).reshape(RENDER_H, WIDTH)
            img_rgb = np.stack([r_cpu, g_cpu, b_cpu], axis=-1)
        else:
            img_rgb = fractal_cpu(
                WIDTH, RENDER_H, max_iter,
                center_x, center_y, scale, phase,
                buddha_r, buddha_g, buddha_b, buddha_mode
            )

            # CPU buddhabrot blend
            if buddha_mode:
                max_density = max(buddha_r.max(), buddha_g.max(), buddha_b.max(), 1.0)
                if max_density > 1.0:
                    nr = np.log1p(buddha_r / max_density * 9.0) / np.log(10.0)
                    ng = np.log1p(buddha_g / max_density * 9.0) / np.log(10.0)
                    nb = np.log1p(buddha_b / max_density * 9.0) / np.log(10.0)
                    alpha = 0.3
                    img_float = img_rgb.astype(np.float64)
                    img_float[:, :, 0] = img_float[:, :, 0] * (1 - alpha) + nr * 255 * alpha
                    img_float[:, :, 1] = img_float[:, :, 1] * (1 - alpha) + ng * 255 * alpha
                    img_float[:, :, 2] = img_float[:, :, 2] * (1 - alpha) + nb * 255 * alpha
                    img_rgb = np.clip(img_float, 0, 255).astype(np.uint8)

        # ── Bump pair overlay: mark quantum bump boundaries ──
        for (bp_a, bp_b) in BUMP_PAIRS:
            # Draw a subtle glow at the CL cell for each bump pair
            for (r_op, c_op) in [(bp_a, bp_b), (bp_b, bp_a)]:
                sx = int((c_op + 0.5 - center_x) * scale + WIDTH / 2)
                sy = int((r_op + 0.5 - center_y) * scale + RENDER_H / 2)
                # Only draw if on screen
                if 2 <= sx < WIDTH - 2 and 2 <= sy < RENDER_H - 2:
                    pulse = 0.5 + 0.5 * math.sin(phase * 4 + bp_a + bp_b)
                    bright = int(100 + 80 * pulse)
                    # Small cross mark
                    for dd in range(-2, 3):
                        if 0 <= sy + dd < RENDER_H:
                            img_rgb[sy + dd, sx, 0] = min(255, img_rgb[sy + dd, sx, 0] + bright)
                        if 0 <= sx + dd < WIDTH:
                            img_rgb[sy, sx + dd, 0] = min(255, img_rgb[sy, sx + dd, 0] + bright)

        # ── Draw to screen ──
        surf = pygame.surfarray.make_surface(img_rgb.swapaxes(0, 1))
        screen.blit(surf, (0, 0))

        # ── Status bar ──
        bar_rect = pygame.Rect(0, RENDER_H, WIDTH, BAR_HEIGHT)
        pygame.draw.rect(screen, (12, 12, 20), bar_rect)

        # Coherence bar
        coh_width = int(WIDTH * poller.coherence)
        coh_color = (220, 190, 50) if poller.coherence >= 0.714285 else (100, 80, 30)
        pygame.draw.rect(screen, coh_color, (0, RENDER_H, coh_width, 2))

        # Connection dot
        if poller.connected:
            pygame.draw.circle(screen, (50, 220, 80), (10, RENDER_H + 18), 4)
        else:
            pygame.draw.circle(screen, (80, 35, 35), (10, RENDER_H + 18), 4)

        # Status text line 1
        conn_str = "LIVE" if poller.connected else "STATIC"
        buddha_str = "ON" if buddha_mode else "OFF"
        breath_str = "ON" if breathing else "OFF"

        line1 = (
            f"  {conn_str}  |  "
            f"tick:{poller.tick_count}  "
            f"coh:{poller.coherence:.3f}  "
            f"op:{poller.current_op_name}  "
            f"depth:{chain_depth}  "
            f"iter:{max_iter}  "
            f"zoom:{scale:.0f}  "
            f"fps:{fps_display:.0f}"
        )
        line2 = (
            f"  [R]eset  [B]reath:{breath_str}  "
            f"[D]ensity:{buddha_str}  "
            f"[+/-]iter  scroll:zoom  click:center"
        )

        t1 = font.render(line1, True, (180, 180, 200))
        t2 = font.render(line2, True, (130, 130, 150))
        screen.blit(t1, (22, RENDER_H + 4))
        screen.blit(t2, (22, RENDER_H + 20))

        pygame.display.flip()
        frame_count += 1

    poller.stop()
    pygame.quit()


if __name__ == '__main__':
    main()
