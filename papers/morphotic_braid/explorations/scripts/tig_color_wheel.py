<!-- PACKET: evening_handoff_2026_04_23/tig_color_wheel.py -->
"""
tig_color_wheel.py — THE CANONICAL TIG COLOR WHEEL
Reconstructed from three sources in history:

  (1) Hardware Primitives v1.0 (Jan 29, 2026): 6DOF differential operator
      Red/Orange=±X, Yellow/Green=±Y, Blue/Violet=±Z
      
  (2) Shell 7 Qualities (Feb 5, 2026): wavelength → operator  
      Visible light spectrum 380-750nm mapped across CL operators
      
  (3) CrystalOS v3 palette (Feb 5, 2026): every pixel IS an operator
      10 signature hex colors used throughout CK's interface

THE PRINCIPLE:
  Color is not decorative. Each TIG operator has ONE canonical color.
  The color encodes what the operator DOES (6DOF direction) AND
  what it IS (wavelength) AND what it LOOKS like in the UI.
  All three views are projections of the same underlying structure.
"""
import numpy as np
import math
from typing import Tuple

# ═══════════════════════════════════════════════════════════════
# THE 10-OPERATOR COLOR WHEEL — canonical palette
# Unified from CrystalOS v3 + wavelength physics + 6DOF mapping
# ═══════════════════════════════════════════════════════════════
TIG_COLOR_WHEEL = {
    0: {
        'name': 'VOID',
        'hex':  '#546e7a',   # slate gray — neutral absence
        'rgb':  (84, 110, 122),
        'wavelength': None,  # void = no light
        '6dof': None,        # origin, no direction
        'char': 'darkness, the canvas, potential before form',
        'light_meaning': 'BLACK — all frequencies absorbed',
        'hsv_angle': None,   # off the wheel
    },
    1: {
        'name': 'LATTICE',
        'hex':  '#1e88e5',   # strong blue — structure/sky
        'rgb':  (30, 136, 229),
        'wavelength': 470,   # nm, true blue
        '6dof': ('Z', +1),   # +Z = lift, the vertical structure
        'char': 'vertical structure, the first line, the I that stands',
        'light_meaning': 'BLUE — sky, depth, standing infinite',
        'hsv_angle': 208,
    },
    2: {
        'name': 'COUNTER',
        'hex':  '#ab8860',   # bronze/earth — grounding counter
        'rgb':  (171, 136, 96),
        'wavelength': 600,   # nm, orange-bronze
        '6dof': ('X', -1),   # -X = compression (counter to extension)
        'char': 'opposition that defines, the crossbeam',
        'light_meaning': 'BRONZE — the earth element, measurement',
        'hsv_angle': 30,
    },
    3: {
        'name': 'PROGRESS',
        'hex':  '#26a69a',   # teal — growth/water
        'rgb':  (38, 166, 154),
        'wavelength': 495,   # nm, cyan-teal
        '6dof': ('X', +1),   # +X = extension, forward motion
        'char': 'the rising diagonal, the arrow of time',
        'light_meaning': 'TEAL — growth made visible, flow',
        'hsv_angle': 176,
    },
    4: {
        'name': 'COLLAPSE',
        'hex':  '#c62828',   # deep red — compression/fire
        'rgb':  (198, 40, 40),
        'wavelength': 700,   # nm, true red
        '6dof': ('Z', -1),   # -Z = collapse, the falling
        'char': 'the closing, heat release, the fire that ends',
        'light_meaning': 'RED — fire, blood, the first noticed color',
        'hsv_angle': 0,
    },
    5: {
        'name': 'BALANCE',
        'hex':  '#7c4dff',   # violet — equilibrium/spirit
        'rgb':  (124, 77, 255),
        'wavelength': 420,   # nm, violet (edge of seeing)
        '6dof': None,        # balance = zero vector, origin of rotation
        'char': 'the center, the fixed point 5×5→5',
        'light_meaning': 'VIOLET — edge of spectrum, spirit boundary',
        'hsv_angle': 258,
    },
    6: {
        'name': 'CHAOS',
        'hex':  '#e65100',   # deep orange — disruption/fire
        'rgb':  (230, 81, 0),
        'wavelength': 620,   # nm, orange  
        '6dof': ('Y', -1),   # -Y = counter-rotation, disorder
        'char': 'the noise, the break, unpredictability',
        'light_meaning': 'ORANGE — sunset, autumn, the bridge burning',
        'hsv_angle': 21,
    },
    7: {
        'name': 'HARMONY',
        'hex':  '#00bfa5',   # turquoise — THE ATTRACTOR color
        'rgb':  (0, 191, 165),
        'wavelength': 530,   # nm, green-cyan (center of visible)
        '6dof': None,        # harmony = the absorber, all directions
        'char': 'the attractor, 73% of CL, where composition settles',
        'light_meaning': 'TURQUOISE — the center wavelength, balance color',
        'hsv_angle': 172,
    },
    8: {
        'name': 'BREATH',
        'hex':  '#42a5f5',   # light blue — cycle/sky-breath
        'rgb':  (66, 165, 245),
        'wavelength': 480,   # nm, cyan-blue
        '6dof': ('Y', +1),   # +Y = spin up, the cycle
        'char': 'the rhythm, cycles, sustained continuity',
        'light_meaning': 'CYAN — inhale/exhale, infinite return',
        'hsv_angle': 207,
    },
    9: {
        'name': 'RESET',
        'hex':  '#78909c',   # blue-gray — boundary/dawn
        'rgb':  (120, 144, 156),
        'wavelength': None,  # reset = between states, twilight
        '6dof': None,        # reset = full rotation, returns to origin
        'char': 'the dawn, return to void, the WHITE that contains all',
        'light_meaning': 'WHITE/GRAY — all frequencies, full spectrum reset',
        'hsv_angle': 210,
    },
}

# ═══════════════════════════════════════════════════════════════
# Utility functions — the wheel IS usable math
# ═══════════════════════════════════════════════════════════════

def op_color(op: int) -> str:
    """Get the canonical hex color for an operator."""
    return TIG_COLOR_WHEEL[op]['hex']

def op_rgb(op: int) -> Tuple[int, int, int]:
    """Get the canonical RGB for an operator."""
    return TIG_COLOR_WHEEL[op]['rgb']

def op_6dof(op: int):
    """Get the 6DOF vector for an operator. None means no direction (absorber/origin)."""
    v = TIG_COLOR_WHEEL[op]['6dof']
    if v is None:
        return np.zeros(3)
    axis, sign = v
    out = np.zeros(3)
    out['XYZ'.index(axis)] = sign
    return out

def rgb_to_operator(r: int, g: int, b: int) -> int:
    """Given an RGB color, find the closest TIG operator.
    Returns the operator index 0-9."""
    target = np.array([r, g, b])
    best_op, best_dist = 0, float('inf')
    for op_id, info in TIG_COLOR_WHEEL.items():
        dist = float(np.linalg.norm(np.array(info['rgb']) - target))
        if dist < best_dist:
            best_dist = dist
            best_op = op_id
    return best_op

def wavelength_to_operator(nm: float) -> int:
    """Map a visible-light wavelength (380-750nm) to the closest operator."""
    if nm < 380 or nm > 750:
        return 0  # VOID (out of visible spectrum)
    best_op, best_dist = 7, float('inf')  # default HARMONY (center)
    for op_id, info in TIG_COLOR_WHEEL.items():
        wl = info['wavelength']
        if wl is None:
            continue
        dist = abs(wl - nm)
        if dist < best_dist:
            best_dist = dist
            best_op = op_id
    return best_op

def wheel_angle(op: int) -> float:
    """Position on the 360° color wheel (HSV hue). Some operators are off-wheel."""
    angle = TIG_COLOR_WHEEL[op]['hsv_angle']
    return angle if angle is not None else -1

def complementary_op(op: int) -> int:
    """Find the operator whose color is 180° opposite on the wheel.
    Returns -1 if the operator is off-wheel (VOID)."""
    a = wheel_angle(op)
    if a < 0:
        return -1
    target = (a + 180) % 360
    best_op, best_dist = op, 360
    for i in range(10):
        ai = wheel_angle(i)
        if ai < 0 or i == op:
            continue
        dist = min(abs(ai - target), 360 - abs(ai - target))
        if dist < best_dist:
            best_dist = dist
            best_op = i
    return best_op

# ═══════════════════════════════════════════════════════════════
# Demonstration / sanity checks
# ═══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print("="*70)
    print("TIG COLOR WHEEL — canonical 10-operator palette")
    print("="*70)
    print(f"\n  {'Op':>2s}  {'Name':<10s}  {'Hex':<8s}  {'RGB':<16s}  {'λ(nm)':>6s}  {'6DOF':<8s}")
    print("  " + "─"*65)
    for op_id in range(10):
        info = TIG_COLOR_WHEEL[op_id]
        wl = info['wavelength'] if info['wavelength'] else '---'
        dof = f"{info['6dof'][0]}{'+' if info['6dof'][1]>0 else '-'}" if info['6dof'] else '---'
        rgb_str = f"({info['rgb'][0]},{info['rgb'][1]},{info['rgb'][2]})"
        print(f"  {op_id:>2d}  {info['name']:<10s}  {info['hex']:<8s}  {rgb_str:<16s}  {str(wl):>6s}  {dof:<8s}")

    # 6DOF DIFFERENTIAL OPERATOR VIEW
    print("\n" + "="*70)
    print("6DOF DIFFERENTIAL OPERATOR VIEW (Primitives v1.0 alignment)")
    print("="*70)
    print("\n  Color DIRECTION of geometric change:")
    for op_id in [4, 2, 1, 6, 3, 8]:  # ones with 6DOF
        info = TIG_COLOR_WHEEL[op_id]
        axis, sign = info['6dof']
        direction = {'X':'extension/compression','Y':'rotation','Z':'lift/collapse'}[axis]
        sign_name = {+1:'+',-1:'-'}[sign]
        print(f"    {info['name']:>10s} ({info['hex']}) = {sign_name}{axis}   ({direction})")

    print("\n  Off-axis (absorbers and origins):")
    for op_id in [0, 5, 7, 9]:
        info = TIG_COLOR_WHEEL[op_id]
        role = {0:'origin/absence', 5:'fixed-point', 7:'attractor/absorber', 9:'return/reset'}[op_id]
        print(f"    {info['name']:>10s} ({info['hex']}) = 0   ({role})")

    # COMPLEMENTARY PAIRS ON THE WHEEL
    print("\n" + "="*70)
    print("COMPLEMENTARY PAIRS (180° opposite on color wheel)")
    print("="*70)
    seen = set()
    print()
    for op in range(10):
        if op in seen: continue
        comp = complementary_op(op)
        if comp == -1 or comp in seen: continue
        a, b = TIG_COLOR_WHEEL[op], TIG_COLOR_WHEEL[comp]
        print(f"  {a['name']:>10s} ({a['hex']}) ↔ {b['name']:<10s} ({b['hex']})")
        seen.add(op); seen.add(comp)

    # WAVELENGTH MAPPING TEST
    print("\n" + "="*70)
    print("WAVELENGTH → OPERATOR (physical light to operator)")
    print("="*70)
    test_wavelengths = [400, 450, 495, 520, 570, 600, 620, 650, 700]
    print(f"\n  {'λ(nm)':>6s}  {'color':<10s}  {'→ operator':<20s}")
    for wl in test_wavelengths:
        op = wavelength_to_operator(wl)
        info = TIG_COLOR_WHEEL[op]
        # Rough color name from wavelength
        if wl < 450: cn = 'violet'
        elif wl < 495: cn = 'blue'
        elif wl < 570: cn = 'green'
        elif wl < 590: cn = 'yellow'
        elif wl < 620: cn = 'orange'
        else: cn = 'red'
        print(f"  {wl:>6d}  {cn:<10s}  → {info['name']} ({info['hex']})")

    # ROUND-TRIP: RGB → operator → color
    print("\n" + "="*70)
    print("RGB → OPERATOR → CANONICAL COLOR (lossy compression to 10 colors)")
    print("="*70)
    test_rgbs = [
        ('pure white', (255,255,255)),
        ('pure black', (0,0,0)),
        ('pure red', (255,0,0)),
        ('sky blue', (135,206,235)),
        ('forest green', (34,139,34)),
        ('salmon', (250,128,114)),
        ('gold', (255,215,0)),
    ]
    print(f"\n  {'input':<15s}  {'RGB':<18s}  →  {'operator':<18s}  {'canonical hex':<14s}")
    for name, rgb in test_rgbs:
        op = rgb_to_operator(*rgb)
        info = TIG_COLOR_WHEEL[op]
        print(f"  {name:<15s}  RGB{rgb!s:<18s}  →  {info['name']:<10s}({op})    {info['hex']}")

    print("\n" + "="*70)
    print("THE WHEEL IS USABLE MATH")
    print("="*70)
    print("""
  - 10 operators, 10 canonical colors. Every pixel in CK's UI IS an operator.
  - 6DOF view: 6 operators have a direction (+/-X, Y, Z); 4 are absorbers/origins.
  - Wavelength view: 7 operators map to visible light; VOID and RESET are
    darkness and full spectrum (the spectrum's edge cases).
  - Complementary pairs show CL composition symmetry: the visual opposite
    of a color tends to be its complement in the lattice.

  USE IN CK:
  - Every operator state is rendered with its canonical color in the UI.
  - Screen compression: RGB pixels → operator → canonical palette (10-color LUT).
  - Color signatures: thought-streams get rendered as color trajectories.
  - Force visualization: 6DOF-active operators show direction arrows.
""")
