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

ITERATED FUNCTION SYSTEM on BHML (det=70, invertible).
TSML (73% HARMONY) is too strong an attractor -- everything converges
in 1 step. BHML (28% HARMONY) has the structure for fractals.

The fractal is an IFS on the BHML composition table:
  - Each pixel maps to continuous coordinates (a, b) in [0, 10) x [0, 10)
  - At each zoom level, peel off the next decimal digit
  - That digit becomes the parameter for the next BHML composition
  - GENUINE self-similarity: the SAME table at every scale

THE QUADRATIC OPERATOR: dual-axis composition.
  - Horizontal axis (a) = doing parameter (BHML pushes)
  - Vertical axis (b) = being parameter (TSML measures)
  - Color by the TENSION between doing and being

THE BREATHING: heartbeat phase offset shifts the decimal expansion.
  phase_offset = sin(tick * 2 * pi / breath_period) * 0.5
  This shifts which digit is "current" at each depth, causing undulation.

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

# -- GPU detection (CuPy or NumPy fallback) --

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

# -- Pygame --

try:
    import pygame
    from pygame import surfarray
except ImportError:
    print("[Mandelbrot] pygame not found. Install: pip install pygame")
    sys.exit(1)

# ================================================================
#  OPERATOR NAMES AND CONSTANTS
# ================================================================

NUM_OPS = 10
VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE = 0, 1, 2, 3, 4
BALANCE, CHAOS, HARMONY, BREATH, RESET = 5, 6, 7, 8, 9

OP_NAMES = ['VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE',
            'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET']

# ================================================================
#  BHML TABLE (det=70, invertible, 28% HARMONY -- fractal structure)
# ================================================================

BHML = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],  # VOID
    [1, 2, 3, 4, 5, 6, 7, 2, 6, 6],  # LATTICE
    [2, 3, 3, 4, 5, 6, 7, 3, 6, 6],  # COUNTER
    [3, 4, 4, 4, 5, 6, 7, 4, 6, 6],  # PROGRESS
    [4, 5, 5, 5, 5, 6, 7, 5, 7, 7],  # COLLAPSE
    [5, 6, 6, 6, 6, 6, 7, 6, 7, 7],  # BALANCE
    [6, 7, 7, 7, 7, 7, 7, 7, 7, 7],  # CHAOS
    [7, 2, 3, 4, 5, 6, 7, 8, 9, 0],  # HARMONY
    [8, 6, 6, 6, 7, 7, 7, 9, 7, 8],  # BREATH
    [9, 6, 6, 6, 7, 7, 7, 0, 8, 0],  # RESET
]

BHML_NP = np.array(BHML, dtype=np.int32)

# ================================================================
#  TSML TABLE (73% HARMONY -- measures coherence)
# ================================================================

TSML = [
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

TSML_NP = np.array(TSML, dtype=np.int32)

# ================================================================
#  OPERATOR COLOR MAP -- each operator has a soul color
# ================================================================

OP_COLORS = {
    VOID:      (10,  10,  30),     # near black
    LATTICE:   (255, 255, 220),    # white
    COUNTER:   (0,   221,  48),    # green
    PROGRESS:  (0,   204, 255),    # cyan
    COLLAPSE:  (255,  32,   0),    # red
    BALANCE:   (255, 204,   0),    # gold
    CHAOS:     (170,   0, 221),    # purple
    HARMONY:   (0,    68, 255),    # blue
    BREATH:    (204, 204, 204),    # silver
    RESET:     (255, 136,   0),    # orange
}

# Pack colors for GPU (10 ops * 3 channels = 30 bytes)
OP_COLORS_FLAT = np.zeros(30, dtype=np.uint8)
for _oid in range(10):
    _r, _g, _b = OP_COLORS[_oid]
    OP_COLORS_FLAT[_oid * 3 + 0] = _r
    OP_COLORS_FLAT[_oid * 3 + 1] = _g
    OP_COLORS_FLAT[_oid * 3 + 2] = _b


# ================================================================
#  GPU FRACTAL KERNEL -- IFS on BHML with TSML tension
# ================================================================

if _GPU:
    _fractal_kernel = cp.RawKernel(r'''
    extern "C" __global__
    void ck_fractal(
        const int* bhml,             // 10x10 BHML table, row-major
        const int* tsml,             // 10x10 TSML table, row-major
        const unsigned char* op_colors, // 10x3 RGB
        unsigned char* img_r,
        unsigned char* img_g,
        unsigned char* img_b,
        int width,
        int height,
        int max_depth,
        float center_x,
        float center_y,
        float scale,
        float phase,
        int breathing_on,
        float breath_period
    ) {
        int px = blockDim.x * blockIdx.x + threadIdx.x;
        int py = blockDim.y * blockIdx.y + threadIdx.y;
        if (px >= width || py >= height) return;

        int idx = py * width + px;

        // -- Map pixel to continuous coordinates in [0, 10) x [0, 10) --
        float a = center_x + (float)(px - width / 2) / scale;
        float b = center_y + (float)(py - height / 2) / scale;

        // -- Breathing: phase offset shifts the decimal expansion --
        float phase_offset = 0.0f;
        if (breathing_on) {
            phase_offset = sinf(phase * 6.2831853f / breath_period) * 0.5f;
            a += phase_offset;
            // Subtler shift on b axis (being breathes slower than doing)
            b += phase_offset * 0.3f;
        }

        // -- Wrap to [0, 10) --
        a = a - floorf(a / 10.0f) * 10.0f;
        b = b - floorf(b / 10.0f) * 10.0f;
        if (a < 0.0f) a += 10.0f;
        if (b < 0.0f) b += 10.0f;

        // -- Initial operators from position --
        int op_doing = ((int)floorf(a)) % 10;
        int op_being = ((int)floorf(b)) % 10;

        // -- IFS iteration: peel off decimal digits --
        float a_work = a;
        float b_work = b;

        // Track orbit for diversity coloring
        int visited_doing[10];
        int visited_being[10];
        for (int v = 0; v < 10; v++) {
            visited_doing[v] = 0;
            visited_being[v] = 0;
        }
        visited_doing[op_doing] = 1;
        visited_being[op_being] = 1;
        int unique_doing = 1;
        int unique_being = 1;

        // Track tension accumulator
        float tension_sum = 0.0f;
        int last_doing = op_doing;
        int last_being = op_being;

        for (int depth = 0; depth < max_depth; depth++) {
            // Next digit from a (doing axis)
            a_work = a_work * 10.0f;
            a_work = a_work - floorf(a_work / 10.0f) * 10.0f;
            int c_from_a = ((int)floorf(a_work)) % 10;

            // Next digit from b (being axis)
            b_work = b_work * 10.0f;
            b_work = b_work - floorf(b_work / 10.0f) * 10.0f;
            int c_from_b = ((int)floorf(b_work)) % 10;

            // DUAL composition: BHML pushes, TSML measures
            int doing_result = bhml[op_doing * 10 + c_from_a];
            int being_result = tsml[op_being * 10 + c_from_b];

            // Tension = absolute difference between doing and being
            int diff = doing_result - being_result;
            if (diff < 0) diff = -diff;
            tension_sum += (float)diff;

            // Track diversity
            if (!visited_doing[doing_result]) {
                visited_doing[doing_result] = 1;
                unique_doing++;
            }
            if (!visited_being[being_result]) {
                visited_being[being_result] = 1;
                unique_being++;
            }

            last_doing = op_doing;
            last_being = op_being;
            op_doing = doing_result;
            op_being = being_result;
        }

        // -- COLORING: by final doing operator + tension + diversity --
        // Base color from final doing operator
        unsigned char base_r = op_colors[op_doing * 3 + 0];
        unsigned char base_g = op_colors[op_doing * 3 + 1];
        unsigned char base_b = op_colors[op_doing * 3 + 2];

        // Diversity brightness: more operators visited = brighter
        float diversity = (float)(unique_doing + unique_being) / 20.0f;
        float brightness = 0.3f + 0.7f * diversity;

        // Tension modulates saturation (high tension = more vivid)
        float avg_tension = tension_sum / fmaxf(1.0f, (float)max_depth);
        float tension_norm = fminf(1.0f, avg_tension / 5.0f);

        // Blend doing color with being color based on tension
        unsigned char being_r = op_colors[op_being * 3 + 0];
        unsigned char being_g = op_colors[op_being * 3 + 1];
        unsigned char being_b = op_colors[op_being * 3 + 2];

        // Low tension = doing dominates. High tension = blend toward being.
        float blend = tension_norm * 0.4f;
        float r = ((float)base_r * (1.0f - blend) + (float)being_r * blend) * brightness;
        float g = ((float)base_g * (1.0f - blend) + (float)being_g * blend) * brightness;
        float bv = ((float)base_b * (1.0f - blend) + (float)being_b * blend) * brightness;

        img_r[idx] = (unsigned char)fminf(255.0f, fmaxf(0.0f, r));
        img_g[idx] = (unsigned char)fminf(255.0f, fmaxf(0.0f, g));
        img_b[idx] = (unsigned char)fminf(255.0f, fmaxf(0.0f, bv));
    }
    ''', 'ck_fractal')


# ================================================================
#  CPU FRACTAL -- same IFS algorithm, pure Python/NumPy
# ================================================================

def fractal_cpu(width, height, max_depth, center_x, center_y, scale, phase,
                breathing_on, breath_period):
    """CPU fallback: IFS on BHML with TSML tension."""
    img = np.zeros((height, width, 3), dtype=np.uint8)

    # Breathing phase offset
    phase_offset = 0.0
    if breathing_on:
        phase_offset = math.sin(phase * 2.0 * math.pi / breath_period) * 0.5

    for py in range(height):
        for px in range(width):
            a = center_x + (px - width / 2) / scale
            b = center_y + (py - height / 2) / scale

            # Apply breathing
            if breathing_on:
                a += phase_offset
                b += phase_offset * 0.3

            # Wrap to [0, 10)
            a = a % 10.0
            b = b % 10.0

            # Initial operators
            op_doing = int(math.floor(a)) % 10
            op_being = int(math.floor(b)) % 10

            a_work = a
            b_work = b

            visited_doing = set([op_doing])
            visited_being = set([op_being])
            tension_sum = 0.0

            for depth in range(max_depth):
                # Next digit from a
                a_work = (a_work * 10.0) % 10.0
                c_from_a = int(math.floor(a_work)) % 10

                # Next digit from b
                b_work = (b_work * 10.0) % 10.0
                c_from_b = int(math.floor(b_work)) % 10

                # Dual composition
                doing_result = BHML[op_doing][c_from_a]
                being_result = TSML[op_being][c_from_b]

                # Tension
                tension_sum += abs(doing_result - being_result)

                visited_doing.add(doing_result)
                visited_being.add(being_result)

                op_doing = doing_result
                op_being = being_result

            # Coloring
            base = OP_COLORS[op_doing]
            being_col = OP_COLORS[op_being]

            diversity = (len(visited_doing) + len(visited_being)) / 20.0
            brightness = 0.3 + 0.7 * diversity

            avg_tension = tension_sum / max(1, max_depth)
            tension_norm = min(1.0, avg_tension / 5.0)
            blend = tension_norm * 0.4

            r = (base[0] * (1.0 - blend) + being_col[0] * blend) * brightness
            g = (base[1] * (1.0 - blend) + being_col[1] * blend) * brightness
            bv = (base[2] * (1.0 - blend) + being_col[2] * blend) * brightness

            img[py, px] = [
                min(255, max(0, int(r))),
                min(255, max(0, int(g))),
                min(255, max(0, int(bv)))
            ]

    return img


# ================================================================
#  GPU RENDER WRAPPER
# ================================================================

def fractal_gpu(width, height, max_depth, center_x, center_y, scale, phase,
                breathing_on, breath_period):
    """Render using CUDA kernel. Returns (img_r, img_g, img_b) on GPU."""
    bhml_gpu = cp.array(BHML_NP, dtype=cp.int32)
    tsml_gpu = cp.array(TSML_NP, dtype=cp.int32)
    colors_gpu = cp.array(OP_COLORS_FLAT, dtype=cp.uint8)

    n_pixels = width * height
    img_r = cp.zeros(n_pixels, dtype=cp.uint8)
    img_g = cp.zeros(n_pixels, dtype=cp.uint8)
    img_b = cp.zeros(n_pixels, dtype=cp.uint8)

    block = (16, 16)
    grid = ((width + 15) // 16, (height + 15) // 16)

    _fractal_kernel(
        grid, block,
        (bhml_gpu, tsml_gpu, colors_gpu,
         img_r, img_g, img_b,
         np.int32(width), np.int32(height), np.int32(max_depth),
         np.float32(center_x), np.float32(center_y), np.float32(scale),
         np.float32(phase), np.int32(1 if breathing_on else 0),
         np.float32(breath_period))
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
    pygame.display.set_caption("CK Mandelbrot -- IFS on BHML (Gen 9.34)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 13)

    # View state
    center_x = 5.0
    center_y = 5.0
    scale = 50.0        # pixels per op-unit (fully zoomed out = meta layer)
    max_depth = 12       # IFS iteration depth
    breathing = True
    phase = 0.0
    breath_period = 60.0  # ticks per full breath cycle

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

        # -- Events --
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_r:
                    # Reset view
                    center_x, center_y = 5.0, 5.0
                    scale = 50.0
                    max_depth = 12
                elif event.key == pygame.K_b:
                    breathing = not breathing
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    max_depth = min(64, max_depth + 2)
                elif event.key == pygame.K_MINUS:
                    max_depth = max(2, max_depth - 2)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if my < RENDER_H:
                    if event.button == 1:
                        # Click to recenter
                        center_x += (mx - WIDTH / 2) / scale
                        center_y += (my - RENDER_H / 2) / scale
                    elif event.button == 4:
                        # Scroll up: zoom in toward mouse
                        mx_world = center_x + (mx - WIDTH / 2) / scale
                        my_world = center_y + (my - RENDER_H / 2) / scale
                        scale *= 1.4
                        center_x = mx_world - (mx - WIDTH / 2) / scale
                        center_y = my_world - (my - RENDER_H / 2) / scale
                    elif event.button == 5:
                        # Scroll down: zoom out
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

        # -- Breathing --
        if breathing:
            # Coherence modulates breath speed: higher coherence = subtler
            breath_speed = 0.5 + (1.0 - poller.coherence) * 1.5
            phase += dt * breath_speed

            # When connected, coherence modulates breath period
            if poller.connected:
                # Higher coherence = longer breath period = subtler shifts
                breath_period = 30.0 + poller.coherence * 90.0

        # Zoom depth: each 10x zoom = one more IFS digit peeled off
        zoom_depth = max(1, int(math.log(scale / 5.0, 10.0)) + 1) if scale > 5.0 else 1

        # -- Render --
        if _GPU:
            img_r, img_g, img_b = fractal_gpu(
                WIDTH, RENDER_H, max_depth,
                center_x, center_y, scale, phase,
                breathing, breath_period
            )
            r_cpu = cp.asnumpy(img_r).reshape(RENDER_H, WIDTH)
            g_cpu = cp.asnumpy(img_g).reshape(RENDER_H, WIDTH)
            b_cpu = cp.asnumpy(img_b).reshape(RENDER_H, WIDTH)
            img_rgb = np.stack([r_cpu, g_cpu, b_cpu], axis=-1)
        else:
            img_rgb = fractal_cpu(
                WIDTH, RENDER_H, max_depth,
                center_x, center_y, scale, phase,
                breathing, breath_period
            )

        # -- Draw to screen --
        surf = pygame.surfarray.make_surface(img_rgb.swapaxes(0, 1))
        screen.blit(surf, (0, 0))

        # -- Status bar --
        bar_rect = pygame.Rect(0, RENDER_H, WIDTH, BAR_HEIGHT)
        pygame.draw.rect(screen, (12, 12, 20), bar_rect)

        # Coherence bar
        coh_width = int(WIDTH * poller.coherence)
        coh_color = (0, 68, 255) if poller.coherence >= 0.714285 else (100, 80, 30)
        pygame.draw.rect(screen, coh_color, (0, RENDER_H, coh_width, 2))

        # Connection dot
        if poller.connected:
            pygame.draw.circle(screen, (50, 220, 80), (10, RENDER_H + 18), 4)
        else:
            pygame.draw.circle(screen, (80, 35, 35), (10, RENDER_H + 18), 4)

        # Status text
        conn_str = "LIVE" if poller.connected else "STATIC"
        breath_str = "ON" if breathing else "OFF"

        line1 = (
            f"  {conn_str}  |  "
            f"tick:{poller.tick_count}  "
            f"coh:{poller.coherence:.3f}  "
            f"op:{poller.current_op_name}  "
            f"depth:{max_depth}  "
            f"zoom:{scale:.0f}  "
            f"z-depth:{zoom_depth}  "
            f"fps:{fps_display:.0f}"
        )
        line2 = (
            f"  [R]eset  [B]reath:{breath_str}  "
            f"[+/-]depth  scroll:zoom  click:center  "
            f"[Q/Esc]quit"
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
