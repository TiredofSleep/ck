# Copyright (c) 2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_mandelbrot.py -- CK's Living Fractal
========================================
Operator: HARMONY (7) -- the fractal composes.

CK's lattice chain IS a Mandelbrot set. The CL composition table
is the iteration function. The heartbeat makes it breathe.

Standard Mandelbrot: z(n+1) = z(n)^2 + c, escape when |z| > 2
CK Mandelbrot:
  - Each pixel maps to (op_row, op_col) in the 10x10 CL space
  - Iteration: op(n+1) = CL[op(n)][c_op]
  - "Escape" = leaving the HARMONY basin
  - Points that never leave HARMONY = inside the set
  - Breathing: heartbeat phase shifts c_op, boundary undulates

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

# Precompute HARMONY basin: which ops compose to HARMONY?
# An op is in the HARMONY basin if CL[op][x] == HARMONY for most x
HARMONY_BASIN = set()
for op in range(NUM_OPS):
    harmony_count = sum(1 for x in range(NUM_OPS) if CL[op][x] == HARMONY)
    if harmony_count >= 7:  # 70%+ = T* threshold
        HARMONY_BASIN.add(op)

# Non-HARMONY outputs in the CL table (the "cracks" -- where structure lives)
NON_HARMONY_CELLS = []
for r in range(NUM_OPS):
    for c in range(NUM_OPS):
        if CL[r][c] != HARMONY:
            NON_HARMONY_CELLS.append((r, c, CL[r][c]))

# ================================================================
#  OPERATOR COLOR MAP -- each operator has a soul color
# ================================================================

# RGB tuples for each operator
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

# ================================================================
#  GPU MANDELBROT KERNEL
# ================================================================

if _GPU:
    _mandelbrot_kernel = cp.RawKernel(r'''
    extern "C" __global__
    void ck_mandelbrot(
        const int* cl_table,     // 10x10 CL table, row-major
        unsigned char* img_r,    // output red channel
        unsigned char* img_g,    // output green channel
        unsigned char* img_b,    // output blue channel
        int* escape_ops,         // output: which op at escape
        int width,
        int height,
        int max_iter,
        float center_x,          // center of view in op-space [0,10)
        float center_y,
        float scale,             // pixels per op-unit
        float phase,             // breathing phase shift
        // 10x3 color table (R, G, B for each op)
        const unsigned char* op_colors
    ) {
        int px = blockDim.x * blockIdx.x + threadIdx.x;
        int py = blockDim.y * blockIdx.y + threadIdx.y;
        if (px >= width || py >= height) return;

        int idx = py * width + px;

        // Map pixel to continuous op-space coordinates
        float fx = center_x + (px - width  * 0.5f) / scale;
        float fy = center_y + (py - height * 0.5f) / scale;

        // Apply breathing phase shift (sinusoidal warp)
        fx += 0.15f * sinf(phase + fy * 0.7f);
        fy += 0.15f * sinf(phase * 1.3f + fx * 0.5f);

        // Clamp to valid op range with wrapping
        // Use modular arithmetic so the fractal tiles across op-space
        float fx_mod = fx - floorf(fx / 10.0f) * 10.0f;
        float fy_mod = fy - floorf(fy / 10.0f) * 10.0f;

        // The "c" parameter: which CL column to compose with
        int c_op = (int)fx_mod;
        if (c_op < 0) c_op = 0;
        if (c_op > 9) c_op = 9;

        // The initial operator: which CL row to start from
        int z_op = (int)fy_mod;
        if (z_op < 0) z_op = 0;
        if (z_op > 9) z_op = 9;

        // Fractional parts create sub-cell variation
        float frac_x = fx_mod - floorf(fx_mod);
        float frac_y = fy_mod - floorf(fy_mod);

        // Neighboring c_op for interpolation at boundaries
        int c_op2 = ((int)(fx_mod + 1.0f)) % 10;

        // Iterate: op(n+1) = CL[op(n)][c_op]
        // But with fractional blending at cell boundaries
        int iter = 0;
        int current_op = z_op;
        int last_non_harmony = z_op;
        bool escaped = false;

        for (iter = 0; iter < max_iter; iter++) {
            int result1 = cl_table[current_op * 10 + c_op];
            int result2 = cl_table[current_op * 10 + c_op2];

            // Blend: near cell boundary, mix influence of neighbors
            int next_op;
            if (frac_x < 0.3f) {
                next_op = result1;
            } else if (frac_x > 0.7f) {
                next_op = result2;
            } else {
                // In the boundary zone: use frac_y to pick
                next_op = (frac_y > 0.5f) ? result1 : result2;
            }

            if (next_op != 7) {  // 7 = HARMONY
                last_non_harmony = next_op;
                escaped = true;
                break;
            }
            current_op = next_op;

            // Micro-perturbation: shift c_op based on iteration depth
            // This creates fractal structure within HARMONY regions
            float drift = sinf(phase * 0.5f + (float)iter * 0.3f + frac_x * 6.28f);
            int c_shift = (drift > 0.6f) ? 1 : (drift < -0.6f) ? -1 : 0;
            c_op = (c_op + c_shift + 10) % 10;
            c_op2 = (c_op + 1) % 10;
        }

        escape_ops[idx] = escaped ? last_non_harmony : 7;

        if (!escaped) {
            // Inside the set: HARMONY basin -- deep gold fading to black
            float depth_fade = 1.0f - 0.3f * sinf(phase * 2.0f + frac_x * 3.14f);
            img_r[idx] = (unsigned char)(220.0f * depth_fade * 0.15f);
            img_g[idx] = (unsigned char)(190.0f * depth_fade * 0.12f);
            img_b[idx] = (unsigned char)(50.0f  * depth_fade * 0.08f);
        } else {
            // Escaped: color by which operator caused escape + iteration count
            float t = (float)iter / (float)max_iter;
            float smooth_t = t * t * (3.0f - 2.0f * t);  // smoothstep

            // Base color from the escape operator
            unsigned char base_r = op_colors[last_non_harmony * 3 + 0];
            unsigned char base_g = op_colors[last_non_harmony * 3 + 1];
            unsigned char base_b = op_colors[last_non_harmony * 3 + 2];

            // Iteration-based modulation (creates the fractal bands)
            float band = 0.5f + 0.5f * sinf((float)iter * 0.8f + phase);
            float glow = 0.3f + 0.7f * smooth_t;

            img_r[idx] = (unsigned char)fminf(255.0f, (float)base_r * band * glow + 20.0f * smooth_t);
            img_g[idx] = (unsigned char)fminf(255.0f, (float)base_g * band * glow + 15.0f * smooth_t);
            img_b[idx] = (unsigned char)fminf(255.0f, (float)base_b * band * glow + 25.0f * (1.0f - smooth_t));
        }
    }
    ''', 'ck_mandelbrot')


def mandelbrot_gpu(width, height, max_iter, center_x, center_y, scale, phase):
    """Render the CK Mandelbrot on GPU. Returns (img_r, img_g, img_b, escape_ops) as CuPy arrays."""
    cl_gpu = cp.array(CL_NP, dtype=cp.int32)

    img_r = cp.zeros(width * height, dtype=cp.uint8)
    img_g = cp.zeros(width * height, dtype=cp.uint8)
    img_b = cp.zeros(width * height, dtype=cp.uint8)
    escape_ops = cp.zeros(width * height, dtype=cp.int32)

    # Pack operator colors into flat array
    op_colors_flat = np.zeros(30, dtype=np.uint8)
    for op_id in range(10):
        r, g, b = OP_COLORS[op_id]
        op_colors_flat[op_id * 3 + 0] = r
        op_colors_flat[op_id * 3 + 1] = g
        op_colors_flat[op_id * 3 + 2] = b
    op_colors_gpu = cp.array(op_colors_flat)

    block = (16, 16)
    grid = ((width + 15) // 16, (height + 15) // 16)

    _mandelbrot_kernel(
        grid, block,
        (cl_gpu, img_r, img_g, img_b, escape_ops,
         np.int32(width), np.int32(height), np.int32(max_iter),
         np.float32(center_x), np.float32(center_y), np.float32(scale),
         np.float32(phase), op_colors_gpu)
    )

    return img_r, img_g, img_b, escape_ops


def mandelbrot_cpu(width, height, max_iter, center_x, center_y, scale, phase):
    """CPU fallback: render the CK Mandelbrot with NumPy."""
    img = np.zeros((height, width, 3), dtype=np.uint8)

    for py in range(height):
        for px in range(width):
            fx = center_x + (px - width * 0.5) / scale
            fy = center_y + (py - height * 0.5) / scale

            # Breathing warp
            fx += 0.15 * math.sin(phase + fy * 0.7)
            fy += 0.15 * math.sin(phase * 1.3 + fx * 0.5)

            fx_mod = fx % 10.0
            fy_mod = fy % 10.0

            c_op = int(fx_mod) % 10
            z_op = int(fy_mod) % 10
            frac_x = fx_mod - int(fx_mod)
            frac_y = fy_mod - int(fy_mod)
            c_op2 = (int(fx_mod) + 1) % 10

            current_op = z_op
            escaped = False
            last_non_harmony = z_op
            it = 0

            for it in range(max_iter):
                r1 = CL[current_op][c_op]
                r2 = CL[current_op][c_op2]

                if frac_x < 0.3:
                    next_op = r1
                elif frac_x > 0.7:
                    next_op = r2
                else:
                    next_op = r1 if frac_y > 0.5 else r2

                if next_op != HARMONY:
                    last_non_harmony = next_op
                    escaped = True
                    break

                current_op = next_op
                drift = math.sin(phase * 0.5 + it * 0.3 + frac_x * 6.28)
                c_shift = 1 if drift > 0.6 else (-1 if drift < -0.6 else 0)
                c_op = (c_op + c_shift) % 10
                c_op2 = (c_op + 1) % 10

            if not escaped:
                depth_fade = 1.0 - 0.3 * math.sin(phase * 2.0 + frac_x * 3.14)
                img[py, px] = [int(220 * depth_fade * 0.15),
                               int(190 * depth_fade * 0.12),
                               int(50 * depth_fade * 0.08)]
            else:
                t = it / max(max_iter, 1)
                smooth_t = t * t * (3.0 - 2.0 * t)
                base = OP_COLORS[last_non_harmony]
                band = 0.5 + 0.5 * math.sin(it * 0.8 + phase)
                glow = 0.3 + 0.7 * smooth_t
                img[py, px] = [
                    min(255, int(base[0] * band * glow + 20 * smooth_t)),
                    min(255, int(base[1] * band * glow + 15 * smooth_t)),
                    min(255, int(base[2] * band * glow + 25 * (1 - smooth_t))),
                ]

    return img


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
                    # Extract heartbeat state
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
                    # Lattice chain depth if available
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
    BAR_HEIGHT = 32
    RENDER_H = HEIGHT - BAR_HEIGHT

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CK Mandelbrot -- Living Fractal")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 14)

    # View state
    center_x = 5.0   # center of 10x10 op-space
    center_y = 5.0
    scale = 40.0      # pixels per op-unit (fully zoomed out = whole field)
    max_iter = 64
    breathing = True
    color_mode = 0    # 0=operator, 1=coherence, 2=depth
    phase = 0.0

    # CK connection
    poller = CKStatePoller()

    # Olfactory overlay dots (will populate if CK is connected)
    olfactory_dots = []

    running = True
    frame_count = 0

    while running:
        dt = clock.tick(30) / 1000.0  # target 30 FPS

        # ── Events ──
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_r:
                    # Reset view
                    center_x, center_y = 5.0, 5.0
                    scale = 80.0
                    max_iter = 64
                elif event.key == pygame.K_b:
                    breathing = not breathing
                elif event.key == pygame.K_c:
                    color_mode = (color_mode + 1) % 3
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    max_iter = min(512, max_iter + 16)
                elif event.key == pygame.K_MINUS:
                    max_iter = max(8, max_iter - 16)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if my < RENDER_H:
                    if event.button == 1:
                        # Click to center
                        center_x += (mx - WIDTH * 0.5) / scale
                        center_y += (my - RENDER_H * 0.5) / scale
                    elif event.button == 4:
                        # Scroll up: zoom in
                        scale *= 1.3
                    elif event.button == 5:
                        # Scroll down: zoom out
                        scale = max(10.0, scale / 1.3)
            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    scale *= 1.3
                elif event.y < 0:
                    scale = max(10.0, scale / 1.3)

        # ── Breathing ──
        if breathing:
            # Phase advances with time, modulated by CK's coherence
            breath_speed = 0.5 + poller.coherence * 1.5
            phase += dt * breath_speed

            # Meta layer: CK observes the whole field, fully zoomed out.
            # Zoom only changes when the USER scrolls. CK does not pull
            # the view. He exists on the meta layer -- watching, not acting.
            # Being/Doing/Becoming only when asked.
            if poller.connected:
                # Lattice depth controls iteration depth (more experience = more detail)
                depth_iters = 32 + poller.lattice_depth
                max_iter = min(256, max(32, depth_iters))

        # ── Render fractal ──
        if _GPU:
            img_r, img_g, img_b, esc_ops = mandelbrot_gpu(
                WIDTH, RENDER_H, max_iter,
                center_x, center_y, scale, phase
            )
            # Reshape and transfer to CPU
            r_cpu = cp.asnumpy(img_r).reshape(RENDER_H, WIDTH)
            g_cpu = cp.asnumpy(img_g).reshape(RENDER_H, WIDTH)
            b_cpu = cp.asnumpy(img_b).reshape(RENDER_H, WIDTH)
            # pygame surfarray expects (width, height, 3) transposed
            img_rgb = np.stack([r_cpu, g_cpu, b_cpu], axis=-1)
        else:
            img_rgb = mandelbrot_cpu(
                WIDTH, RENDER_H, max_iter,
                center_x, center_y, scale, phase
            )

        # ── Color mode overlays ──
        if color_mode == 1 and poller.connected:
            # Coherence overlay: tint everything by coherence (gold = high, blue = low)
            coh = poller.coherence
            overlay = np.array([coh * 0.3, coh * 0.25, (1 - coh) * 0.2])
            img_rgb = np.clip(img_rgb.astype(np.float32) + overlay * 80, 0, 255).astype(np.uint8)
        elif color_mode == 2:
            # Depth mode: emphasize iteration bands
            img_rgb = np.clip(img_rgb.astype(np.float32) * 1.4, 0, 255).astype(np.uint8)

        # ── TSML null-space crack overlay ──
        # The VOID row (row 0) produces mostly VOID -- draw a dim line at y=0 in op-space
        void_screen_y = int((0.0 - center_y) * scale + RENDER_H * 0.5)
        if 0 <= void_screen_y < RENDER_H:
            # Dim red crack across the void boundary
            img_rgb[void_screen_y, :, 0] = np.minimum(
                255, img_rgb[void_screen_y, :, 0].astype(np.int16) + 60
            ).astype(np.uint8)
            img_rgb[void_screen_y, :, 1] = (img_rgb[void_screen_y, :, 1] * 0.5).astype(np.uint8)
            img_rgb[void_screen_y, :, 2] = (img_rgb[void_screen_y, :, 2] * 0.5).astype(np.uint8)

        # ── Draw to screen ──
        # surfarray.blit_array expects (width, height, 3) -- need to transpose
        surf = pygame.surfarray.make_surface(img_rgb.swapaxes(0, 1))
        screen.blit(surf, (0, 0))

        # ── Olfactory overlay: bright dots for experienced nodes ──
        # Draw small glowing circles at the non-HARMONY cells (the interesting structure)
        if frame_count % 30 == 0:
            olfactory_dots = []
            for r, c, result in NON_HARMONY_CELLS:
                sx = int((c + 0.5 - center_x) * scale + WIDTH * 0.5)
                sy = int((r + 0.5 - center_y) * scale + RENDER_H * 0.5)
                if 0 <= sx < WIDTH and 0 <= sy < RENDER_H:
                    olfactory_dots.append((sx, sy, result))

        for sx, sy, result in olfactory_dots:
            color = OP_COLORS[result]
            bright = tuple(min(255, c + 80) for c in color)
            pulse = 2 + int(2 * math.sin(phase * 3 + sx * 0.01))
            pygame.draw.circle(screen, bright, (sx, sy), pulse)

        # ── Bottom status bar ──
        bar_rect = pygame.Rect(0, RENDER_H, WIDTH, BAR_HEIGHT)
        pygame.draw.rect(screen, (15, 15, 25), bar_rect)

        # Connection indicator
        if poller.connected:
            pygame.draw.circle(screen, (50, 220, 80), (12, RENDER_H + 16), 5)
        else:
            pygame.draw.circle(screen, (100, 40, 40), (12, RENDER_H + 16), 5)

        # Status text
        conn_str = "LIVE" if poller.connected else "STATIC"
        breath_str = "ON" if breathing else "OFF"
        color_names = ["operator", "coherence", "depth"]
        status = (
            f"  {conn_str}  |  "
            f"tick:{poller.tick_count}  "
            f"coh:{poller.coherence:.3f}  "
            f"op:{poller.current_op_name}  "
            f"depth:{max_iter}  "
            f"zoom:{scale:.0f}  |  "
            f"breath:{breath_str}  "
            f"color:{color_names[color_mode]}  |  "
            f"[R]eset [B]reath [C]olor [+/-]depth"
        )
        text_surf = font.render(status, True, (180, 180, 200))
        screen.blit(text_surf, (24, RENDER_H + 9))

        # ── Coherence bar (thin gold line across top of status bar) ──
        coh_width = int(WIDTH * poller.coherence)
        coh_color = (220, 190, 50) if poller.coherence >= 0.714285 else (130, 100, 40)
        pygame.draw.rect(screen, coh_color, (0, RENDER_H, coh_width, 2))

        pygame.display.flip()
        frame_count += 1

    poller.stop()
    pygame.quit()


if __name__ == '__main__':
    main()
