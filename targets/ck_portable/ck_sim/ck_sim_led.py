"""
ck_sim_led.py -- Port of ck_led.c
===================================
Operator: BREATH (8) -- the LED breathes with CK.

Operator-to-color mapping and breath modulation.
Returns RGB tuples for the Kivy visualizer.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from ck_sim.ck_sim_heartbeat import (
    VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET
)

# Operator colors (from ck_led.h lines 24-37)
# Each is (R, G, B) 0-255
OP_COLORS = {
    VOID:     (0, 0, 0),
    LATTICE:  (0, 80, 255),
    COUNTER:  (255, 255, 255),
    PROGRESS: (0, 200, 60),
    COLLAPSE: (255, 30, 10),
    BALANCE:  (255, 180, 0),
    CHAOS:    (255, 0, 60),
    HARMONY:  (80, 200, 255),
    BREATH:   (100, 100, 220),
    RESET:    (255, 255, 255),
}

SOVEREIGN_COLOR = (255, 200, 50)
BUMP_COLOR = (255, 255, 255)


def get_op_color(op: int) -> tuple:
    """Get RGB color for an operator."""
    return OP_COLORS.get(op, (0, 0, 0))


def get_op_color_float(op: int) -> tuple:
    """Get color as 0.0-1.0 floats (for Kivy)."""
    r, g, b = get_op_color(op)
    return (r / 255.0, g / 255.0, b / 255.0)


def breathe_color(op: int, breath_mod: float) -> tuple:
    """Apply breath modulation to operator color.
    Returns (R, G, B) as 0.0-1.0 floats.
    Matches ck_led_breathe() -- intensity follows sine."""
    r, g, b = get_op_color(op)
    # Minimum brightness 30%, modulated up to 100%
    intensity = 0.3 + 0.7 * breath_mod
    return (
        r / 255.0 * intensity,
        g / 255.0 * intensity,
        b / 255.0 * intensity,
    )


def sovereign_color_float() -> tuple:
    """Gold color for sovereignty."""
    r, g, b = SOVEREIGN_COLOR
    return (r / 255.0, g / 255.0, b / 255.0)


def bump_color_float() -> tuple:
    """White flash for bumps."""
    return (1.0, 1.0, 1.0)
