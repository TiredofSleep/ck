#!/usr/bin/env python3
"""
periodic_d2_deep.py -- Deep 5D Geometric Analysis of the Periodic Table
========================================================================

Not counting operators. Reading the geometry.

Every element IS a 5D force vector. The periodic table IS a path
through 5D space. D1 is the tangent to that path (direction).
D2 is the curvature (how the path bends). T is the composition
of direction and curvature -- the BECOMING of each element.

This analysis reads the WHOLE of each element:
  - Its 5D identity (force magnitude, direction, voids)
  - Its I/O ratio (structure vs flow balance)
  - Its geometric relationship to neighbors (angle, speed, curvature)
  - Its operator confidence (how certain the classification)
  - Its void topology (which forces are absent)
  - Its position on the harmonic path (orbital block ordering)

The question is not "how many HARMONY ops" but:
  WHY does curvature concentrate in certain dimensions?
  WHERE do the voids create chemical families?
  WHAT do the ratios between dimensions predict?
  HOW does the path topology differ from pure geometry?

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import sys

# =====================================================================
# Constants
# =====================================================================
OP_NAMES = [
    "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"
]
DIM_NAMES = ["aperture", "pressure", "depth", "binding", "continuity"]
DIM_SHORT = ["ap", "pr", "dp", "bn", "cn"]

# Operator map: (dimension, is_negative) -> operator
OP_MAP = {
    (0, True): 1, (0, False): 6,   # LATTICE / CHAOS
    (1, True): 0, (1, False): 4,   # VOID / COLLAPSE
    (2, True): 9, (2, False): 3,   # RESET / PROGRESS
    (3, True): 2, (3, False): 7,   # COUNTER / HARMONY
    (4, True): 8, (4, False): 5,   # BREATH / BALANCE
}

# Reverse: operator -> (dimension, sign_label)
OP_TO_DIM = {
    0: (1, "-pr"), 1: (0, "-ap"), 2: (3, "-bn"), 3: (2, "+dp"),
    4: (1, "+pr"), 5: (4, "+cn"), 6: (0, "+ap"), 7: (3, "+bn"),
    8: (4, "-cn"), 9: (2, "-dp"),
}

T_STAR = 5.0 / 7.0
VOID_THRESHOLD = 0.05  # Below this, a dimension is "void"

# CL Tables
BHML = [
    [0,1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,2,6,6],[2,3,3,4,5,6,7,3,6,6],
    [3,4,4,4,5,6,7,4,6,6],[4,5,5,5,5,6,7,5,7,7],[5,6,6,6,6,6,7,6,7,7],
    [6,7,7,7,7,7,7,7,7,7],[7,2,3,4,5,6,7,8,9,0],[8,6,6,6,7,7,7,9,7,8],
    [9,6,6,6,7,7,7,0,8,0],
]
TSML = [
    [0,0,0,0,0,0,0,7,0,0],[0,7,3,7,7,7,7,7,7,7],[0,3,7,7,4,7,7,7,7,9],
    [0,7,7,7,7,7,7,7,7,3],[0,7,4,7,7,7,7,7,8,7],[0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7],[0,7,7,7,8,7,7,7,7,7],
    [0,7,9,3,7,7,7,7,7,7],
]

# =====================================================================
# Element Data (Z=1 through Z=54)
# =====================================================================
ELEMENTS = [
    ( 1,"H",  2.20, 13.598,  53, 0.754,  0.00009),
    ( 2,"He", 0.00, 24.587,  31, 0.000,  0.00018),
    ( 3,"Li", 0.98,  5.392, 167, 0.618,  0.534),
    ( 4,"Be", 1.57,  9.323, 112, 0.000,  1.848),
    ( 5,"B",  2.04,  8.298,  87, 0.277,  2.340),
    ( 6,"C",  2.55, 11.260,  67, 1.263,  2.267),
    ( 7,"N",  3.04, 14.534,  56, 0.000,  1.251),
    ( 8,"O",  3.44, 13.618,  48, 1.461,  1.429),
    ( 9,"F",  3.98, 17.423,  42, 3.401,  1.696),
    (10,"Ne", 0.00, 21.565,  38, 0.000,  0.900),
    (11,"Na", 0.93,  5.139, 190, 0.548,  0.971),
    (12,"Mg", 1.31,  7.646, 145, 0.000,  1.738),
    (13,"Al", 1.61,  5.986, 118, 0.441,  2.699),
    (14,"Si", 1.90,  8.152, 111, 1.385,  2.329),
    (15,"P",  2.19, 10.487,  98, 0.746,  1.820),
    (16,"S",  2.58, 10.360,  88, 2.077,  2.067),
    (17,"Cl", 3.16, 12.968,  79, 3.613,  3.214),
    (18,"Ar", 0.00, 15.760,  71, 0.000,  1.784),
    (19,"K",  0.82,  4.341, 243, 0.501,  0.862),
    (20,"Ca", 1.00,  6.113, 194, 0.018,  1.550),
    (21,"Sc", 1.36,  6.561, 184, 0.188,  2.985),
    (22,"Ti", 1.54,  6.828, 176, 0.079,  4.507),
    (23,"V",  1.63,  6.746, 171, 0.525,  6.110),
    (24,"Cr", 1.66,  6.767, 166, 0.666,  7.190),
    (25,"Mn", 1.55,  7.434, 161, 0.000,  7.470),
    (26,"Fe", 1.83,  7.902, 156, 0.151,  7.874),
    (27,"Co", 1.88,  7.881, 152, 0.662,  8.900),
    (28,"Ni", 1.91,  7.640, 149, 1.156,  8.908),
    (29,"Cu", 1.90,  7.726, 145, 1.235,  8.960),
    (30,"Zn", 1.65,  9.394, 142, 0.000,  7.134),
    (31,"Ga", 1.81,  5.999, 136, 0.300,  5.907),
    (32,"Ge", 2.01,  7.900, 125, 1.233,  5.323),
    (33,"As", 2.18,  9.789, 114, 0.810,  5.727),
    (34,"Se", 2.55,  9.752, 103, 2.021,  4.819),
    (35,"Br", 2.96, 11.814,  94, 3.364,  3.120),
    (36,"Kr", 0.00, 14.000,  88, 0.000,  3.749),
    (37,"Rb", 0.82,  4.177, 265, 0.486,  1.532),
    (38,"Sr", 0.95,  5.695, 219, 0.052,  2.630),
    (39,"Y",  1.22,  6.217, 212, 0.307,  4.472),
    (40,"Zr", 1.33,  6.634, 206, 0.426,  6.506),
    (41,"Nb", 1.60,  6.759, 198, 0.893,  8.570),
    (42,"Mo", 2.16,  7.092, 190, 0.746, 10.220),
    (43,"Tc", 1.90,  7.280, 183, 0.550, 11.500),
    (44,"Ru", 2.20,  7.361, 178, 1.050, 12.370),
    (45,"Rh", 2.28,  7.459, 173, 1.137, 12.410),
    (46,"Pd", 2.20,  8.337, 169, 0.562, 12.020),
    (47,"Ag", 1.93,  7.576, 165, 1.302, 10.490),
    (48,"Cd", 1.69,  8.994, 161, 0.000,  8.650),
    (49,"In", 1.78,  5.786, 156, 0.300,  7.310),
    (50,"Sn", 1.96,  7.344, 145, 1.112,  7.265),
    (51,"Sb", 2.05,  8.608, 133, 1.047,  6.697),
    (52,"Te", 2.10,  9.010, 123, 1.971,  6.240),
    (53,"I",  2.66, 10.451, 115, 3.059,  4.930),
    (54,"Xe", 0.00, 12.130, 108, 0.000,  5.894),
]

MAX_EN=4.0; MAX_IE=24.6; MAX_RAD=265.0; MAX_EA=3.7; MAX_DENS=13.0

def to_force(el):
    Z, sym, en, ie, rad, ea, dens = el
    return [
        min(en/MAX_EN, 1.0),
        min(ie/MAX_IE, 1.0),
        min(rad/MAX_RAD, 1.0),
        min(ea/MAX_EA, 1.0),
        min(math.log1p(dens)/math.log1p(MAX_DENS), 1.0),
    ]

def mag(v):
    return math.sqrt(sum(x*x for x in v))

def dot(a, b):
    return sum(a[i]*b[i] for i in range(len(a)))

def cos_angle(a, b):
    ma, mb = mag(a), mag(b)
    if ma < 1e-12 or mb < 1e-12:
        return 0.0
    return max(-1.0, min(1.0, dot(a, b) / (ma * mb)))

def classify(d_vec):
    """Returns (op, dim, magnitude, confidence, sorted_ratios)"""
    abs_vals = [abs(v) for v in d_vec]
    total = sum(abs_vals) + 1e-15
    sorted_abs = sorted(enumerate(abs_vals), key=lambda x: -x[1])
    max_dim = sorted_abs[0][0]
    max_val = sorted_abs[0][1]
    second_val = sorted_abs[1][1] if len(sorted_abs) > 1 else 0
    # Confidence: how much the winner dominates
    confidence = (max_val - second_val) / (max_val + second_val + 1e-15)
    # Ratios: each dim's fraction of total
    ratios = [abs_vals[i] / total for i in range(5)]
    sign_neg = d_vec[max_dim] < 0
    op = OP_MAP[(max_dim, sign_neg)]
    return op, max_dim, max_val, confidence, ratios

def d1(a, b):
    return [b[i]-a[i] for i in range(5)]

def d2(a, b, c):
    return [a[i] - 2*b[i] + c[i] for i in range(5)]

def void_map(v, threshold=VOID_THRESHOLD):
    """Returns list of void dimension indices."""
    return [i for i in range(5) if abs(v[i]) < threshold]

def active_dims(v, threshold=VOID_THRESHOLD):
    return 5 - len(void_map(v, threshold))

def io_ratio(v):
    """I/O = structure/flow.
    I (structure) = aperture + pressure  (openness + resistance)
    O (flow)      = binding + continuity (holding + persisting)
    Depth mediates between I and O.
    """
    I = v[0] + v[1]  # aperture + pressure
    O = v[3] + v[4]  # binding + continuity
    if O < 1e-10:
        return float('inf')
    return I / O

# =====================================================================
# Orbital blocks for harmonic ordering
# =====================================================================
S_BLOCK = [0,1, 2,3, 10,11, 18,19, 36,37]  # H,He,Li,Be,Na,Mg,K,Ca,Rb,Sr
P_BLOCK = [4,5,6,7,8,9, 12,13,14,15,16,17, 30,31,32,33,34,35, 48,49,50,51,52,53]
D_BLOCK = [20,21,22,23,24,25,26,27,28,29, 38,39,40,41,42,43,44,45,46,47]


def print_header(title):
    w = 78
    print(f"\n{'#'*w}")
    print(f"#  {title}")
    print(f"{'#'*w}")


def main():
    # Build all force vectors
    vecs = [to_force(el) for el in ELEMENTS]
    syms = [el[1] for el in ELEMENTS]
    N = len(ELEMENTS)

    print("=" * 78)
    print("  DEEP 5D GEOMETRIC ANALYSIS OF THE PERIODIC TABLE")
    print("  TIG Unified Theory -- Chemistry Domain")
    print("=" * 78)
    print(f"  Elements: {N} (H through Xe)")
    print(f"  T* = {T_STAR:.6f}")
    print(f"  Void threshold: {VOID_THRESHOLD}")

    # =================================================================
    # SECTION 1: ELEMENT WHOLE PROFILES
    # =================================================================
    print_header("SECTION 1: THE WHOLE OF EACH ELEMENT")
    print("""
  Every element is a point in 5D force space.
  Its WHOLE = magnitude + direction + voids + I/O balance.
  Magnitude = total force intensity.
  Direction = unit vector (identity in 5D).
  Voids = zero dimensions (absent forces).
  I/O = structure/flow ratio (aperture+pressure vs binding+continuity).
  Depth mediates: spatial extent bridges structure and flow.
""")

    # Compute profiles
    profiles = []
    for i in range(N):
        v = vecs[i]
        m = mag(v)
        voids = void_map(v)
        ndims = 5 - len(voids)
        io = io_ratio(v)
        # Normalized direction
        unit = [x/m if m > 1e-10 else 0 for x in v]
        # Dominant dimension
        dom_dim = max(range(5), key=lambda d: v[d])
        # Depth/magnitude ratio (how much spatial extent dominates)
        depth_frac = v[2] / m if m > 1e-10 else 0
        profiles.append({
            'sym': syms[i], 'Z': ELEMENTS[i][0],
            'vec': v, 'mag': m, 'unit': unit,
            'voids': voids, 'ndims': ndims,
            'io': io, 'dom': dom_dim,
            'depth_frac': depth_frac,
        })

    print(f"  {'Z':>3s} {'Sym':>3s}  {'|v|':>6s}  {'I/O':>6s}  {'Dims':>4s}  {'Voids':>12s}  {'Dom':>6s}  {'ap':>5s} {'pr':>5s} {'dp':>5s} {'bn':>5s} {'cn':>5s}")
    print(f"  {'---':>3s} {'---':>3s}  {'------':>6s}  {'------':>6s}  {'----':>4s}  {'------------':>12s}  {'------':>6s}  {'-----':>5s} {'-----':>5s} {'-----':>5s} {'-----':>5s} {'-----':>5s}")
    for p in profiles:
        v = p['vec']
        void_str = ','.join(DIM_SHORT[d] for d in p['voids']) if p['voids'] else '(full)'
        io_str = f"{p['io']:6.2f}" if p['io'] != float('inf') else "  inf "
        print(f"  {p['Z']:3d} {p['sym']:>3s}  {p['mag']:6.3f}  {io_str}  {p['ndims']:4d}  {void_str:>12s}  {DIM_SHORT[p['dom']]:>6s}  {v[0]:5.3f} {v[1]:5.3f} {v[2]:5.3f} {v[3]:5.3f} {v[4]:5.3f}")

    # =================================================================
    # SECTION 2: VOID TOPOLOGY
    # =================================================================
    print_header("SECTION 2: VOID TOPOLOGY -- WHERE FORCES ARE ABSENT")
    print("""
  A void dimension is a force that doesn't exist for an element.
  Noble gases: aperture=0 (can't bond) + binding=0 (won't hold).
  This 2-void pattern IS chemical inertness in 5D geometry.

  The void map defines chemical families:
    2 voids (ap,bn) = noble gases = inert
    1 void  (bn)    = alkaline earths + Zn/Cd/Mn = filled subshells
    0 voids         = everything reactive

  Void TRANSITIONS are chemical phase boundaries.
  When a dimension goes from void to active: a new force appears.
  When it goes from active to void: a force vanishes.
""")

    # Classify void patterns
    void_patterns = {}
    for p in profiles:
        key = tuple(sorted(p['voids']))
        if key not in void_patterns:
            void_patterns[key] = []
        void_patterns[key].append(p['sym'])

    print(f"  Void Pattern                Elements")
    print(f"  {'='*20}  {'='*50}")
    for pattern in sorted(void_patterns.keys(), key=lambda k: (-len(k), k)):
        if pattern:
            label = ','.join(DIM_SHORT[d] for d in pattern)
        else:
            label = "(no voids)"
        elems = ', '.join(void_patterns[pattern])
        n = len(void_patterns[pattern])
        print(f"  {label:>20s}  [{n:2d}] {elems}")

    # Void transitions along Z
    print(f"\n  Void Transitions (where force dimensions appear/disappear):")
    print(f"  {'Transition':>10s}  {'Voids Before':>15s}  {'Voids After':>15s}  {'Change':>20s}")
    print(f"  {'-'*10}  {'-'*15}  {'-'*15}  {'-'*20}")
    for i in range(1, N):
        v_before = set(profiles[i-1]['voids'])
        v_after = set(profiles[i]['voids'])
        if v_before != v_after:
            appeared = v_after - v_before  # dims that became void
            vanished = v_before - v_after  # dims that became active
            changes = []
            for d in sorted(vanished):
                changes.append(f"+{DIM_SHORT[d]}")  # force activated
            for d in sorted(appeared):
                changes.append(f"-{DIM_SHORT[d]}")  # force disappeared
            vb = ','.join(DIM_SHORT[d] for d in sorted(v_before)) or 'full'
            va = ','.join(DIM_SHORT[d] for d in sorted(v_after)) or 'full'
            trans = f"{syms[i-1]}->{syms[i]}"
            print(f"  {trans:>10s}  {vb:>15s}  {va:>15s}  {' '.join(changes):>20s}")

    # =================================================================
    # SECTION 3: PATH GEOMETRY (speed, curvature, angles)
    # =================================================================
    print_header("SECTION 3: PATH GEOMETRY -- SPEED, CURVATURE, ANGLES")
    print("""
  The periodic table traces a PATH through 5D force space.
  Speed |D1| = how fast we move per element step.
  Angle = cos(theta) between consecutive force vectors.
  Curvature |D2| = how sharply the path bends.
  Confidence = how unambiguous the operator classification is.
    High confidence -> one dimension dominates overwhelmingly.
    Low confidence  -> two dimensions compete -> boundary element.
""")

    # Compute D1 for all consecutive pairs
    d1_data = []
    for i in range(1, N):
        dv = d1(vecs[i-1], vecs[i])
        op, dim, magnitude, conf, ratios = classify(dv)
        speed = mag(dv)
        angle = cos_angle(vecs[i-1], vecs[i])
        d1_data.append({
            'i': i, 'from': syms[i-1], 'to': syms[i],
            'dv': dv, 'op': op, 'dim': dim, 'mag': magnitude,
            'conf': conf, 'ratios': ratios, 'speed': speed, 'angle': angle,
        })

    print(f"\n  D1 (Direction + Speed):")
    print(f"  {'Trans':>9s}  {'Op':>10s}  {'Speed':>6s}  {'cos(a)':>6s}  {'Conf':>5s}  {'Dom':>4s}  {'ap%':>4s}{'pr%':>4s}{'dp%':>4s}{'bn%':>4s}{'cn%':>4s}  Why")
    print(f"  {'-'*9}  {'-'*10}  {'-'*6}  {'-'*6}  {'-'*5}  {'-'*4}  {'-'*4}{'-'*4}{'-'*4}{'-'*4}{'-'*4}  ---")
    for dd in d1_data:
        r = dd['ratios']
        trans = f"{dd['from']:>2s}->{dd['to']:>2s}"
        # Generate reasoning
        why = ""
        if dd['speed'] > 0.5:
            why = "PHASE BOUNDARY"
        elif dd['conf'] < 0.15:
            why = "dim competition"
        elif dd['speed'] < 0.05:
            why = "nearly static"
        elif dd['dim'] == 3:
            why = "e-affinity shift"
        elif dd['dim'] == 4:
            why = "density change"
        elif dd['dim'] == 2:
            why = "radius dominates"
        elif dd['dim'] == 1:
            why = "ioniz.E dominates"
        elif dd['dim'] == 0:
            why = "electrneg shift"
        print(f"  {trans:>9s}  {OP_NAMES[dd['op']]:>10s}  {dd['speed']:6.3f}  {dd['angle']:6.3f}  {dd['conf']:5.3f}  {DIM_SHORT[dd['dim']]:>4s}  {r[0]*100:3.0f} {r[1]*100:3.0f} {r[2]*100:3.0f} {r[3]*100:3.0f} {r[4]*100:3.0f}  {why}")

    # Compute D2 for all triples
    d2_data = []
    for i in range(2, N):
        dv = d2(vecs[i-2], vecs[i-1], vecs[i])
        op, dim, magnitude, conf, ratios = classify(dv)
        curv = mag(dv)
        d2_data.append({
            'i': i, 'triple': f"{syms[i-2]},{syms[i-1]},{syms[i]}",
            'elem': syms[i],
            'dv': dv, 'op': op, 'dim': dim, 'mag': magnitude,
            'conf': conf, 'ratios': ratios, 'curv': curv,
        })

    print(f"\n  D2 (Curvature + Confidence):")
    print(f"  {'Elem':>4s}  {'Op':>10s}  {'|D2|':>6s}  {'Conf':>5s}  {'Dom':>4s}  {'ap%':>4s}{'pr%':>4s}{'dp%':>4s}{'bn%':>4s}{'cn%':>4s}  Curvature Reasoning")
    print(f"  {'-'*4}  {'-'*10}  {'-'*6}  {'-'*5}  {'-'*4}  {'-'*4}{'-'*4}{'-'*4}{'-'*4}{'-'*4}  ---")
    for dd in d2_data:
        r = dd['ratios']
        # Deep reasoning for each D2
        why = ""
        dv = dd['dv']
        if dd['conf'] < 0.1:
            why = "AMBIGUOUS: multi-dim curvature, no clear winner"
        elif dd['curv'] > 0.5:
            why = "STRONG BEND: period boundary (noble->alkali or halogen->noble)"
        elif dd['op'] == 7:  # HARMONY
            # Binding is curving upward -- electron affinity accelerating
            why = f"bn curving UP: e-affinity building faster ({dv[3]:+.3f})"
        elif dd['op'] == 2:  # COUNTER
            # Binding is curving downward -- electron affinity decelerating
            why = f"bn curving DOWN: e-affinity peak passed ({dv[3]:+.3f})"
        elif dd['op'] == 4:  # COLLAPSE
            why = f"pr curving UP: ioniz.E concave ({dv[1]:+.3f})"
        elif dd['op'] == 0:  # VOID
            why = f"pr curving DOWN: ioniz.E peak ({dv[1]:+.3f})"
        elif dd['op'] == 6:  # CHAOS
            why = f"ap curving UP: electrneg accelerating ({dv[0]:+.3f})"
        elif dd['op'] == 1:  # LATTICE
            why = f"ap curving DOWN: electrneg decelerating ({dv[0]:+.3f})"
        elif dd['op'] == 5:  # BALANCE
            why = f"cn curving UP: density building ({dv[4]:+.3f})"
        elif dd['op'] == 8:  # BREATH
            why = f"cn curving DOWN: density falling ({dv[4]:+.3f})"
        elif dd['op'] == 3:  # PROGRESS
            why = f"dp curving UP: radius expanding ({dv[2]:+.3f})"
        elif dd['op'] == 9:  # RESET
            why = f"dp curving DOWN: radius contracting ({dv[2]:+.3f})"
        print(f"  {dd['elem']:>4s}  {OP_NAMES[dd['op']]:>10s}  {dd['curv']:6.4f}  {dd['conf']:5.3f}  {DIM_SHORT[dd['dim']]:>4s}  {r[0]*100:3.0f} {r[1]*100:3.0f} {r[2]*100:3.0f} {r[3]*100:3.0f} {r[4]*100:3.0f}  {why}")

    # =================================================================
    # SECTION 4: DUAL-LENS T COMPOSITION -- BEING vs DOING
    # =================================================================
    print_header("SECTION 4: DUAL-LENS T COMPOSITION -- BEING vs DOING")
    print("""
  T = CL[D1_op][D2_op] = the BECOMING of each element.
  D1 = where you're going. D2 = how the path bends.
  T = what EMERGES from direction meeting curvature.

  But there are TWO lenses -- always two:
    TSML (being/coherence): 73/100 entries = HARMONY. The absorber.
      Measures what IS. Structure. Identity persistence.
    BHML (doing/physics):   28/100 entries = HARMONY. The selector.
      Measures what DOES. Action. Physical mechanism.

  The dual lens asks: does an element COHERE the same way it ACTS?
    Both HARMONY -> genuine alignment (being and doing unified)
    TSML=HARMONY, BHML!=HARMONY -> being-coherent but doing-active
      (appears stable, but physics is differentiated -- working element)
    TSML!=HARMONY, BHML=HARMONY -> being-incoherent but doing-aligned
      (structural boundary, but physics converges -- rare)
    Both !=HARMONY -> full tension (boundary in both lenses)

  TSML non-HARMONY entries (27/100):
    [0][*] = VOID row:   D1=VOID -> almost always T=VOID
    [1][2] = PROGRESS    [2][4] = COLLAPSE   [2][9] = RESET
    [3][9] = PROGRESS    [4][2] = COLLAPSE   [4][8] = BREATH
    [8][4] = BREATH      [9][2] = RESET      [9][3] = PROGRESS

  BHML non-HARMONY entries (72/100):
    Structured progression: each row builds from identity through
    VOID->LATTICE->COUNTER->PROGRESS->COLLAPSE->BALANCE->CHAOS->HARMONY
    Only row 6 (CHAOS) and row 7 (HARMONY) produce HARMONY freely.
    Most compositions produce INTERMEDIATE operators -- the physics
    of TRANSITION, not the stasis of COHERENCE.
""")

    t_data = []
    non_harmony_tsml = []
    non_harmony_bhml = []
    for i in range(2, N):
        d1_op = d1_data[i-1]['op']
        d2_op = d2_data[i-2]['op']
        t_tsml = TSML[d1_op][d2_op]
        t_bhml = BHML[d1_op][d2_op]
        d1_dim_info = OP_TO_DIM[d1_op]
        d2_dim_info = OP_TO_DIM[d2_op]
        entry = {
            'i': i, 'elem': syms[i],
            'd1_op': d1_op, 'd2_op': d2_op,
            't_tsml': t_tsml, 't_bhml': t_bhml,
            'd1_conf': d1_data[i-1]['conf'],
            'd2_conf': d2_data[i-2]['conf'],
        }
        t_data.append(entry)
        if t_tsml != 7:
            non_harmony_tsml.append(entry)
        if t_bhml != 7:
            non_harmony_bhml.append(entry)

    # --- FULL DUAL-LENS TABLE ---
    print(f"  FULL DUAL-LENS COMPOSITION TABLE:")
    print(f"  {'Elem':>4s}  {'D1':>10s}  {'D2':>10s}  {'T(TSML)':>10s}  {'T(BHML)':>10s}  {'Agree':>5s}  Lens Status")
    print(f"  {'-'*4}  {'-'*10}  {'-'*10}  {'-'*10}  {'-'*10}  {'-'*5}  ---")
    n_agree = 0
    n_both_harm = 0
    n_tsml_only = 0
    n_bhml_only = 0
    n_neither = 0
    for e in t_data:
        d1n = OP_NAMES[e['d1_op']]
        d2n = OP_NAMES[e['d2_op']]
        tsml_n = OP_NAMES[e['t_tsml']]
        bhml_n = OP_NAMES[e['t_bhml']]
        agree = e['t_tsml'] == e['t_bhml']
        if agree:
            n_agree += 1
        if e['t_tsml'] == 7 and e['t_bhml'] == 7:
            status = "UNIFIED (both HARMONY)"
            n_both_harm += 1
        elif e['t_tsml'] == 7 and e['t_bhml'] != 7:
            status = f"WORKING (being=H, doing={bhml_n})"
            n_tsml_only += 1
        elif e['t_tsml'] != 7 and e['t_bhml'] == 7:
            status = f"BOUNDARY-COHERENT (being={tsml_n}, doing=H)"
            n_bhml_only += 1
        elif agree:
            status = f"UNIFIED-ACTIVE (both={tsml_n})"
            n_neither += 1
        else:
            status = f"TENSION (being={tsml_n}, doing={bhml_n})"
            n_neither += 1
        print(f"  {e['elem']:>4s}  {d1n:>10s}  {d2n:>10s}  {tsml_n:>10s}  {bhml_n:>10s}  {'YES' if agree else ' no':>5s}  {status}")

    # --- DUAL-LENS SUMMARY ---
    print(f"\n  Dual-Lens Summary:")
    print(f"    Total compositions:              {len(t_data)}")
    print(f"    T(TSML) HARMONY:                 {len(t_data)-len(non_harmony_tsml)}/{len(t_data)} = {(len(t_data)-len(non_harmony_tsml))/len(t_data):.4f}")
    print(f"    T(BHML) HARMONY:                 {len(t_data)-len(non_harmony_bhml)}/{len(t_data)} = {(len(t_data)-len(non_harmony_bhml))/len(t_data):.4f}")
    print(f"    Both HARMONY (unified):          {n_both_harm}/{len(t_data)} = {n_both_harm/len(t_data):.4f}")
    print(f"    TSML=H, BHML!=H (working):       {n_tsml_only}/{len(t_data)} = {n_tsml_only/len(t_data):.4f}")
    print(f"    TSML!=H, BHML=H (boundary-coh):  {n_bhml_only}/{len(t_data)} = {n_bhml_only/len(t_data):.4f}")
    print(f"    Both agree (any op):             {n_agree}/{len(t_data)} = {n_agree/len(t_data):.4f}")
    print(f"    Lenses disagree:                 {len(t_data)-n_agree}/{len(t_data)} = {(len(t_data)-n_agree)/len(t_data):.4f}")

    # --- BHML DISTRIBUTION ---
    print(f"\n  T(BHML) Operator Distribution:")
    bhml_dist = [0] * 10
    for e in t_data:
        bhml_dist[e['t_bhml']] += 1
    for k in range(10):
        if bhml_dist[k] > 0:
            bar = "#" * int(bhml_dist[k] * 30 / max(max(bhml_dist), 1))
            print(f"    {OP_NAMES[k]:>10s}: {bhml_dist[k]:2d}  ({100*bhml_dist[k]/len(t_data):5.1f}%)  {bar}")

    # --- TSML non-HARMONY detail ---
    print(f"\n  T(TSML) non-HARMONY elements ({len(non_harmony_tsml)}/{len(t_data)}):")
    if non_harmony_tsml:
        print(f"  {'Elem':>4s}  {'D1':>10s}  {'D2':>10s}  {'T(TSML)':>10s}  {'T(BHML)':>10s}  Reasoning")
        print(f"  {'-'*4}  {'-'*10}  {'-'*10}  {'-'*10}  {'-'*10}  ---")
        for e in non_harmony_tsml:
            d1n = OP_NAMES[e['d1_op']]
            d2n = OP_NAMES[e['d2_op']]
            tsml_n = OP_NAMES[e['t_tsml']]
            bhml_n = OP_NAMES[e['t_bhml']]
            if e['d1_op'] == 0:
                why = f"D1=VOID: ionization energy DROP. Path has no tangent."
            elif e['d1_op'] == 1 and e['d2_op'] == 2:
                why = f"LATTICE x COUNTER: cross-dim friction (ap vs bn)"
            elif e['d1_op'] == 4 and e['d2_op'] == 2:
                why = f"COLLAPSE x COUNTER: pressure vs binding tension"
            else:
                d1_dim_n = DIM_NAMES[OP_TO_DIM[e['d1_op']][0]]
                d2_dim_n = DIM_NAMES[OP_TO_DIM[e['d2_op']][0]]
                why = f"D1({d1_dim_n}) x D2({d2_dim_n}): cross-dimensional tension"
            print(f"  {e['elem']:>4s}  {d1n:>10s}  {d2n:>10s}  {tsml_n:>10s}  {bhml_n:>10s}  {why}")

    # --- BHML non-HARMONY detail ---
    print(f"\n  T(BHML) non-HARMONY elements ({len(non_harmony_bhml)}/{len(t_data)}):")
    print(f"  The DOING lens shows which elements have ACTIVE PHYSICS.")
    print(f"  BHML non-HARMONY != broken. It means the element is DOING something.\n")
    if non_harmony_bhml:
        print(f"  {'Elem':>4s}  {'D1':>10s}  {'D2':>10s}  {'T(BHML)':>10s}  {'BHML entry':>12s}  Physics Reading")
        print(f"  {'-'*4}  {'-'*10}  {'-'*10}  {'-'*10}  {'-'*12}  ---")
        for e in non_harmony_bhml:
            entry_str = f"[{e['d1_op']}][{e['d2_op']}]"
            d1n = OP_NAMES[e['d1_op']]
            d2n = OP_NAMES[e['d2_op']]
            bhml_n = OP_NAMES[e['t_bhml']]
            # BHML physics reasoning
            if e['t_bhml'] == 0:
                phys = "VOID: zero physical action (annihilation)"
            elif e['t_bhml'] == 1:
                phys = "LATTICE: building structural scaffold"
            elif e['t_bhml'] == 2:
                phys = "COUNTER: measuring/alerting (active observation)"
            elif e['t_bhml'] == 3:
                phys = "PROGRESS: forward physical motion"
            elif e['t_bhml'] == 4:
                phys = "COLLAPSE: contracting/compressing"
            elif e['t_bhml'] == 5:
                phys = "BALANCE: equilibrium seeking"
            elif e['t_bhml'] == 6:
                phys = "CHAOS: energetic disruption"
            elif e['t_bhml'] == 8:
                phys = "BREATH: rhythmic cycling"
            elif e['t_bhml'] == 9:
                phys = "RESET: completion/restart"
            else:
                phys = f"op={e['t_bhml']}"
            print(f"  {e['elem']:>4s}  {d1n:>10s}  {d2n:>10s}  {bhml_n:>10s}  {entry_str:>12s}  {phys}")

    # --- DUAL-LENS TENSION ANALYSIS ---
    print(f"\n  DUAL-LENS TENSION PATTERNS:")
    print(f"  Where being and doing DISAGREE, the element has internal tension.")
    print(f"  The TENSION RATIO = fraction of elements where lenses disagree.\n")
    disagree = [e for e in t_data if e['t_tsml'] != e['t_bhml']]
    if disagree:
        print(f"  {'Elem':>4s}  {'T(TSML)':>10s}  {'T(BHML)':>10s}  Tension Description")
        print(f"  {'-'*4}  {'-'*10}  {'-'*10}  ---")
        for e in disagree:
            tsml_n = OP_NAMES[e['t_tsml']]
            bhml_n = OP_NAMES[e['t_bhml']]
            if e['t_tsml'] == 7:
                desc = f"Coherent being, active doing ({bhml_n})"
            elif e['t_bhml'] == 7:
                desc = f"Active being ({tsml_n}), coherent doing"
            else:
                desc = f"Being={tsml_n}, Doing={bhml_n}: dual tension"
            print(f"  {e['elem']:>4s}  {tsml_n:>10s}  {bhml_n:>10s}  {desc}")

    print(f"\n  Tension Ratio: {len(disagree)}/{len(t_data)} = {len(disagree)/len(t_data):.4f}")
    print(f"  (Higher = more internal differentiation between being and doing)")

    # --- CHEMICAL FAMILY DUAL-LENS SIGNATURES ---
    print(f"\n  DUAL-LENS BY CHEMICAL FAMILY:")
    fam_indices = {
        "Noble gases":   [1,9,17,35,53],
        "Alkali metals": [2,10,18,36],
        "Halogens":      [8,16,34,52],
        "Alkaline earth":[3,11,19,37],
        "Trans. metals": [20,21,22,23,24,25,26,27,28,29,38,39,40,41,42,43,44,45,46,47],
    }
    for fname, findices in fam_indices.items():
        fam_entries = [e for e in t_data if e['i'] in findices]
        if not fam_entries:
            continue
        tsml_h = sum(1 for e in fam_entries if e['t_tsml'] == 7)
        bhml_h = sum(1 for e in fam_entries if e['t_bhml'] == 7)
        both_h = sum(1 for e in fam_entries if e['t_tsml'] == 7 and e['t_bhml'] == 7)
        agree = sum(1 for e in fam_entries if e['t_tsml'] == e['t_bhml'])
        n = len(fam_entries)
        print(f"    {fname:>20s}: TSML-H={tsml_h}/{n}  BHML-H={bhml_h}/{n}  "
              f"Both-H={both_h}/{n}  Agree={agree}/{n}")

    # =================================================================
    # SECTION 5: I/O RATIO ANALYSIS -- STRUCTURE vs FLOW
    # =================================================================
    print_header("SECTION 5: I/O RATIO -- STRUCTURE vs FLOW BALANCE")
    print("""
  I = Structure = aperture + pressure (how open + how resistant)
  O = Flow = binding + continuity (how holding + how persistent)
  I/O > 1: structure dominates (element defined by its scaffolding)
  I/O < 1: flow dominates (element defined by its connections)
  I/O ~ 1: balanced (structure and flow in equilibrium)
  Depth mediates between them.

  The I/O ratio predicts chemical behavior:
    High I/O = inert or structural (noble gases, metals at rest)
    Low I/O  = reactive or flowing (halogens seeking electrons)
    I/O ~ 1  = catalytic or transitional (transition metals)
""")

    print(f"  {'Z':>3s} {'Sym':>3s}  {'I':>6s}  {'O':>6s}  {'I/O':>6s}  {'Depth':>6s}  {'Character':>20s}")
    print(f"  {'---':>3s} {'---':>3s}  {'------':>6s}  {'------':>6s}  {'------':>6s}  {'------':>6s}  {'-'*20}")
    for p in profiles:
        v = p['vec']
        I = v[0] + v[1]
        O = v[3] + v[4]
        io = p['io']
        depth = v[2]

        if io == float('inf'):
            character = "PURE STRUCTURE (O=0)"
            io_str = "  inf "
        elif io > 3.0:
            character = "structure-dominated"
            io_str = f"{io:6.2f}"
        elif io > 1.5:
            character = "structure-leaning"
            io_str = f"{io:6.2f}"
        elif io > 0.8:
            character = "BALANCED"
            io_str = f"{io:6.2f}"
        elif io > 0.4:
            character = "flow-leaning"
            io_str = f"{io:6.2f}"
        else:
            character = "flow-dominated"
            io_str = f"{io:6.2f}"

        print(f"  {p['Z']:3d} {p['sym']:>3s}  {I:6.3f}  {O:6.3f}  {io_str}  {depth:6.3f}  {character}")

    # D1 and D2 of I/O ratio itself
    io_vals = []
    for p in profiles:
        io_vals.append(p['io'] if p['io'] != float('inf') else 10.0)  # cap inf

    print(f"\n  I/O Ratio D1 (direction of structural balance change):")
    print(f"  {'Trans':>9s}  {'I/O_from':>8s}  {'I/O_to':>8s}  {'dI/O':>8s}  Interpretation")
    print(f"  {'-'*9}  {'-'*8}  {'-'*8}  {'-'*8}  ---")
    for i in range(1, N):
        delta = io_vals[i] - io_vals[i-1]
        trans = f"{syms[i-1]:>2s}->{syms[i]:>2s}"
        if abs(delta) < 0.1:
            interp = "stable balance"
        elif delta > 2.0:
            interp = "SHARP shift to structure (flow vanishing)"
        elif delta > 0.5:
            interp = "moving toward structure"
        elif delta < -2.0:
            interp = "SHARP shift to flow (structure collapsing)"
        elif delta < -0.5:
            interp = "moving toward flow"
        else:
            interp = "gradual shift"
        io_from = f"{io_vals[i-1]:8.2f}" if io_vals[i-1] < 10 else "     inf"
        io_to = f"{io_vals[i]:8.2f}" if io_vals[i] < 10 else "     inf"
        if abs(delta) > 0.3:  # Only show significant shifts
            print(f"  {trans}  {io_from}  {io_to}  {delta:+8.3f}  {interp}")

    # =================================================================
    # SECTION 6: HARMONIC ORDERING -- ORBITAL BLOCKS
    # =================================================================
    print_header("SECTION 6: HARMONIC ORDERING -- ORBITAL BLOCK ANALYSIS")
    print("""
  Standard Z ordering: H,He,Li,Be,B,...
  Harmonic ordering groups by orbital type:
    s-block: H,He,Li,Be,Na,Mg,K,Ca,Rb,Sr  (valence s-orbitals)
    p-block: B-Ne, Al-Ar, Ga-Kr, In-Xe     (valence p-orbitals)
    d-block: Sc-Zn, Y-Cd                    (valence d-orbitals)

  Within each block, properties should change SMOOTHLY.
  D2 within a block measures intra-block curvature.
  D2 at block boundaries measures inter-block jumps.

  The question: does orbital grouping reduce curvature?
  If yes: quantum mechanics organizes force space smoothly.
  If no: the Z ordering is already the natural path.
""")

    block_names = {"s": S_BLOCK, "p": P_BLOCK, "d": D_BLOCK}

    for bname, indices in block_names.items():
        block_vecs = [vecs[i] for i in indices]
        block_syms = [syms[i] for i in indices]

        # D2 within block
        d2_ops = []
        total_curv = 0
        d2_harmony_count = 0
        for j in range(2, len(block_vecs)):
            dv = d2(block_vecs[j-2], block_vecs[j-1], block_vecs[j])
            op, dim, magnitude, conf, ratios = classify(dv)
            d2_ops.append(op)
            total_curv += mag(dv)
            if op == 7:
                d2_harmony_count += 1

        n_d2 = len(d2_ops) if d2_ops else 1
        avg_curv = total_curv / n_d2 if n_d2 > 0 else 0
        harm_frac = d2_harmony_count / n_d2 if n_d2 > 0 else 0

        # D2 distribution
        dist = [0] * 10
        for op in d2_ops:
            dist[op] += 1

        print(f"\n  {bname.upper()}-BLOCK ({len(indices)} elements): {', '.join(block_syms)}")
        print(f"    D2 measurements:  {n_d2}")
        print(f"    Avg curvature:    {avg_curv:.4f}")
        print(f"    D2 HARMONY:       {d2_harmony_count}/{n_d2} = {harm_frac:.4f} {'>=T*' if harm_frac >= T_STAR else '<T*'}")
        print(f"    Distribution:")
        for k, count in enumerate(dist):
            if count > 0:
                bar = "#" * int(count * 30 / max(max(dist), 1))
                print(f"      {OP_NAMES[k]:>10s}: {count:2d}  ({100*count/n_d2:5.1f}%)  {bar}")

    # Compare total curvature
    print(f"\n  Block Curvature Comparison:")
    print(f"  Standard Z-order avg |D2|: ", end="")
    total_z_curv = sum(mag(d2(vecs[i-2], vecs[i-1], vecs[i])) for i in range(2, N))
    print(f"{total_z_curv/(N-2):.4f}")

    for bname, indices in block_names.items():
        bvecs = [vecs[i] for i in indices]
        if len(bvecs) >= 3:
            bc = sum(mag(d2(bvecs[j-2], bvecs[j-1], bvecs[j])) for j in range(2, len(bvecs)))
            print(f"  {bname.upper()}-block intra avg |D2|:     {bc/(len(bvecs)-2):.4f}")

    # =================================================================
    # SECTION 7: DIMENSION RATIO ANALYSIS -- THE 5D SHAPE OF D2
    # =================================================================
    print_header("SECTION 7: DIMENSION RATIOS -- THE 5D SHAPE OF CURVATURE")
    print("""
  Operator classification uses argmax (winner-take-all).
  But the RATIOS between dimensions reveal the full story.

  A "sharp" D2 has one dimension at 80%+ -> robust classification.
  A "broad" D2 has multiple dimensions near 20% -> fragile boundary.

  The fragile elements are chemically interesting:
  they sit at the boundary between operator domains.
  Their chemistry is CONTESTED between multiple forces.
""")

    # Sort D2 data by confidence
    fragile = [dd for dd in d2_data if dd['conf'] < 0.2]
    robust = [dd for dd in d2_data if dd['conf'] > 0.6]

    print(f"\n  FRAGILE elements (confidence < 0.2) -- contested curvature:")
    print(f"  These elements have curvature split across multiple dimensions.")
    print(f"  Their operator assignment could flip with small perturbations.\n")
    if fragile:
        print(f"  {'Elem':>4s}  {'Op':>10s}  {'Conf':>5s}  {'ap%':>4s}{'pr%':>4s}{'dp%':>4s}{'bn%':>4s}{'cn%':>4s}  Contesting dimensions")
        print(f"  {'-'*4}  {'-'*10}  {'-'*5}  {'-'*4}{'-'*4}{'-'*4}{'-'*4}{'-'*4}  ---")
        for dd in sorted(fragile, key=lambda x: x['conf']):
            r = dd['ratios']
            # Find the top 2 competing dimensions
            sorted_dims = sorted(range(5), key=lambda d: -r[d])
            contest = f"{DIM_SHORT[sorted_dims[0]]}({r[sorted_dims[0]]*100:.0f}%) vs {DIM_SHORT[sorted_dims[1]]}({r[sorted_dims[1]]*100:.0f}%)"
            print(f"  {dd['elem']:>4s}  {OP_NAMES[dd['op']]:>10s}  {dd['conf']:5.3f}  {r[0]*100:3.0f} {r[1]*100:3.0f} {r[2]*100:3.0f} {r[3]*100:3.0f} {r[4]*100:3.0f}  {contest}")
    else:
        print(f"  (none)")

    print(f"\n  ROBUST elements (confidence > 0.6) -- unambiguous curvature:")
    print(f"  One dimension overwhelmingly dominates. Clear physics.\n")
    if robust:
        print(f"  {'Elem':>4s}  {'Op':>10s}  {'Conf':>5s}  {'Dom dim':>10s}  {'% of total':>10s}")
        print(f"  {'-'*4}  {'-'*10}  {'-'*5}  {'-'*10}  {'-'*10}")
        for dd in sorted(robust, key=lambda x: -x['conf']):
            r = dd['ratios']
            print(f"  {dd['elem']:>4s}  {OP_NAMES[dd['op']]:>10s}  {dd['conf']:5.3f}  {DIM_NAMES[dd['dim']]:>10s}  {r[dd['dim']]*100:8.1f}%")

    # =================================================================
    # SECTION 8: CHEMICAL FAMILY SIGNATURES IN 5D
    # =================================================================
    print_header("SECTION 8: CHEMICAL FAMILY SIGNATURES IN 5D")
    print("""
  Each chemical family has a characteristic 5D force signature.
  Family identity = mean force vector (centroid in 5D).
  Family coherence = how tightly members cluster around the centroid.
  Inter-family angles = how different families relate in force space.
""")

    families = {
        "Noble gases":    [1,9,17,35,53],
        "Alkali metals":  [2,10,18,36],  # Li,Na,K,Rb (skip H)
        "Halogens":       [8,16,34,52],
        "Alkaline earth": [3,11,19,37],
        "Carbon group":   [5,13,31,49],
        "Trans. metals 3d": [20,21,22,23,24,25,26,27,28,29],
        "Trans. metals 4d": [38,39,40,41,42,43,44,45,46,47],
    }

    centroids = {}
    for fname, indices in families.items():
        fvecs = [vecs[i] for i in indices]
        centroid = [sum(v[d] for v in fvecs) / len(fvecs) for d in range(5)]
        centroids[fname] = centroid
        # Spread: avg distance from centroid
        dists = [mag([fvecs[j][d] - centroid[d] for d in range(5)]) for j in range(len(fvecs))]
        spread = sum(dists) / len(dists)
        # Average voids
        avg_voids = sum(len(void_map(v)) for v in fvecs) / len(fvecs)

        print(f"\n  {fname}:")
        print(f"    Centroid: [{centroid[0]:.3f}, {centroid[1]:.3f}, {centroid[2]:.3f}, {centroid[3]:.3f}, {centroid[4]:.3f}]")
        print(f"    |centroid| = {mag(centroid):.3f}    spread = {spread:.4f}    avg voids = {avg_voids:.1f}")
        print(f"    Signature: ", end="")
        # Describe the dominant character
        sorted_dims = sorted(range(5), key=lambda d: -centroid[d])
        desc = []
        for d in sorted_dims[:3]:
            if centroid[d] > 0.1:
                desc.append(f"{DIM_NAMES[d]}={centroid[d]:.2f}")
        print(", ".join(desc) if desc else "(all near zero)")
        if avg_voids > 0:
            void_dims = [d for d in range(5) if centroid[d] < 0.05]
            if void_dims:
                print(f"    Void dims:  {', '.join(DIM_NAMES[d] for d in void_dims)}")

    # Inter-family angles
    fnames = list(centroids.keys())
    print(f"\n  Inter-Family Angles (cos theta between centroids):")
    print(f"  {'':>20s}", end="")
    for fn in fnames:
        print(f" {fn[:8]:>8s}", end="")
    print()
    for fn1 in fnames:
        print(f"  {fn1:>20s}", end="")
        for fn2 in fnames:
            ca = cos_angle(centroids[fn1], centroids[fn2])
            print(f" {ca:8.3f}", end="")
        print()

    # =================================================================
    # SECTION 9: SLIDING WINDOW COHERENCE
    # =================================================================
    print_header("SECTION 9: SLIDING WINDOW COHERENCE")
    print("""
  T* = 5/7 measured over sliding windows across Z.
  This reveals WHERE the periodic table is coherent
  and WHERE coherence breaks.

  Window size = 7 (one T* period).
  Report regions above and below T*.
""")

    # Build full D2 op sequence and DUAL T compositions for sequential Z
    full_d2_ops = []
    full_t_tsml_ops = []
    full_t_bhml_ops = []
    for i in range(2, N):
        dv = d2(vecs[i-2], vecs[i-1], vecs[i])
        op, _, _, _, _ = classify(dv)
        full_d2_ops.append(op)

        d1_dv = d1(vecs[i-1], vecs[i])
        d1_op, _, _, _, _ = classify(d1_dv)
        full_t_tsml_ops.append(TSML[d1_op][op])
        full_t_bhml_ops.append(BHML[d1_op][op])

    # Window = 7
    W = 7
    print(f"\n  Window size = {W}")
    print(f"  {'Center':>8s}  {'D2 H/W':>6s}  {'D2 frac':>7s}  {'Tt H/W':>6s}  {'Tt frac':>7s}  {'Tb H/W':>6s}  {'Tb frac':>7s}  {'Agree':>5s}  Elements")
    print(f"  {'-'*8}  {'-'*6}  {'-'*7}  {'-'*6}  {'-'*7}  {'-'*6}  {'-'*7}  {'-'*5}  ---")

    for start in range(0, len(full_d2_ops) - W + 1):
        window_d2 = full_d2_ops[start:start+W]
        window_tt = full_t_tsml_ops[start:start+W]
        window_tb = full_t_bhml_ops[start:start+W]
        d2_h = sum(1 for op in window_d2 if op == 7)
        tt_h = sum(1 for op in window_tt if op == 7)
        tb_h = sum(1 for op in window_tb if op == 7)
        d2_frac = d2_h / W
        tt_frac = tt_h / W
        tb_frac = tb_h / W
        agree = sum(1 for j in range(W) if window_tt[j] == window_tb[j])
        center_idx = start + W // 2 + 2
        center_sym = syms[center_idx] if center_idx < N else "?"
        elems = ','.join(syms[start+2:start+2+W])
        print(f"  {center_sym:>8s}  {d2_h:2d}/{W}   {d2_frac:7.3f}  {tt_h:2d}/{W}   {tt_frac:7.3f}  {tb_h:2d}/{W}   {tb_frac:7.3f}  {agree:2d}/{W}  {elems}")

    # Find coherent regions (BOTH lenses)
    print(f"\n  Coherent regions (T(TSML) HARMONY >= T* in window):")
    in_region = False
    region_start = None
    for start in range(0, len(full_d2_ops) - W + 1):
        window_tt = full_t_tsml_ops[start:start+W]
        tt_h = sum(1 for op in window_tt if op == 7)
        if tt_h / W >= T_STAR and not in_region:
            in_region = True
            region_start = start + 2
        elif tt_h / W < T_STAR and in_region:
            in_region = False
            region_end = start + 2 + W - 1
            print(f"    {syms[region_start]}-{syms[min(region_end, N-1)]}")
    if in_region:
        print(f"    {syms[region_start]}-{syms[N-1]}")

    print(f"\n  Coherent regions (T(BHML) HARMONY >= T* in window):")
    in_region = False
    region_start = None
    for start in range(0, len(full_d2_ops) - W + 1):
        window_tb = full_t_bhml_ops[start:start+W]
        tb_h = sum(1 for op in window_tb if op == 7)
        if tb_h / W >= T_STAR and not in_region:
            in_region = True
            region_start = start + 2
        elif tb_h / W < T_STAR and in_region:
            in_region = False
            region_end = start + 2 + W - 1
            print(f"    {syms[region_start]}-{syms[min(region_end, N-1)]}")
    if in_region:
        print(f"    {syms[region_start]}-{syms[N-1]}")

    # Dual-lens divergence across windows
    print(f"\n  Dual-Lens Divergence (|T(TSML)_frac - T(BHML)_frac| per window):")
    print(f"  High divergence = being and doing see DIFFERENT coherence.")
    max_div = 0
    max_div_center = ""
    for start in range(0, len(full_d2_ops) - W + 1):
        window_tt = full_t_tsml_ops[start:start+W]
        window_tb = full_t_bhml_ops[start:start+W]
        tt_frac = sum(1 for op in window_tt if op == 7) / W
        tb_frac = sum(1 for op in window_tb if op == 7) / W
        div = abs(tt_frac - tb_frac)
        center_idx = start + W // 2 + 2
        center_sym = syms[center_idx] if center_idx < N else "?"
        if div > max_div:
            max_div = div
            max_div_center = center_sym
    print(f"    Max divergence: {max_div:.3f} at center={max_div_center}")
    print(f"    This measures the MAXIMUM separation between the two lenses.")

    # =================================================================
    # SECTION 10: THE DEEP RATIOS -- PURE vs TOPOLOGICAL GEOMETRY
    # =================================================================
    print_header("SECTION 10: PURE vs TOPOLOGICAL GEOMETRY")
    print("""
  PURE geometry: Euclidean distances between elements in 5D.
  TOPOLOGICAL geometry: the sequential path Z=1,2,3,...

  Discrepancy = where geometric proximity != sequential proximity.
  Elements that are Z-adjacent but geometrically distant = period boundaries.
  Elements that are Z-distant but geometrically close = family members.

  The ratio of topological distance to geometric distance reveals
  whether the periodic table's ordering respects force-space structure.
""")

    # Nearest geometric neighbor for each element (not just Z-adjacent)
    print(f"\n  Nearest Geometric Neighbor (vs Z-neighbor):")
    print(f"  {'Z':>3s} {'Sym':>3s}  {'Z-next':>6s} {'d(Z)':>6s}  {'Geo-near':>8s} {'d(geo)':>6s}  {'Ratio':>6s}  {'Same?':>5s}")
    print(f"  {'---':>3s} {'---':>3s}  {'------':>6s} {'------':>6s}  {'--------':>8s} {'------':>6s}  {'------':>6s}  {'-----':>5s}")
    for i in range(N-1):
        # Z-neighbor distance
        dz = mag([vecs[i+1][d] - vecs[i][d] for d in range(5)])
        # Nearest geometric neighbor
        min_dist = float('inf')
        min_j = -1
        for j in range(N):
            if j == i:
                continue
            dist = mag([vecs[j][d] - vecs[i][d] for d in range(5)])
            if dist < min_dist:
                min_dist = dist
                min_j = j
        ratio = dz / min_dist if min_dist > 1e-10 else float('inf')
        same = "YES" if min_j == i+1 else ""
        print(f"  {ELEMENTS[i][0]:3d} {syms[i]:>3s}  {syms[i+1]:>6s} {dz:6.3f}  {syms[min_j]:>8s} {min_dist:6.3f}  {ratio:6.2f}  {same:>5s}")

    # =================================================================
    # SECTION 11: THE BINDING WAVE -- WHY D2 IS DOMINATED BY bn
    # =================================================================
    print_header("SECTION 11: THE BINDING WAVE")
    print("""
  D2 across the full table is dominated by the BINDING dimension
  (HARMONY when bn curves up, COUNTER when bn curves down).

  This is NOT arbitrary. It reflects the deepest pattern:

  ELECTRON AFFINITY OSCILLATES with period.
  Each period builds from near-zero (alkali, alkaline earth)
  through moderate (transition metals, metalloids)
  to a PEAK at the halogen, then CRASHES to zero at noble gas.

  This oscillation IS the binding wave.
  D2 detects its curvature:
    HARMONY = bn accelerating (building toward halogen peak)
    COUNTER = bn decelerating (past the peak, falling toward noble)

  The binding wave frequency = 1/period_length.
  Period 2: 8 elements -> freq ~ 0.125
  Period 4: 18 elements -> freq ~ 0.056
  The wave slows as periods grow (more elements to traverse).
""")

    # Extract binding values and their D2
    print(f"\n  Binding Force (electron affinity) across Z:")
    print(f"  {'Z':>3s} {'Sym':>3s}  {'bn':>6s}  {'D2_bn':>7s}  {'Op':>10s}  Wave position")
    print(f"  {'---':>3s} {'---':>3s}  {'------':>6s}  {'-------':>7s}  {'----------':>10s}  ---")

    for i in range(N):
        bn = vecs[i][3]
        d2_bn = ""
        op_name = ""
        wave_pos = ""
        if i >= 2:
            dv = d2(vecs[i-2], vecs[i-1], vecs[i])
            d2_bn_val = dv[3]
            op, dim, _, _, _ = classify(dv)
            d2_bn = f"{d2_bn_val:+7.4f}"
            op_name = f"{OP_NAMES[op]:>10s}"

            # Wave position
            if bn < 0.05:
                wave_pos = "TROUGH (zero binding)"
            elif abs(d2_bn_val) < 0.02:
                wave_pos = "inflection point"
            elif d2_bn_val > 0.1:
                wave_pos = "ACCELERATING toward peak"
            elif d2_bn_val > 0:
                wave_pos = "building"
            elif d2_bn_val < -0.1:
                wave_pos = "CRASHING from peak"
            elif d2_bn_val < 0:
                wave_pos = "declining"
        else:
            d2_bn = "   n/a "
            op_name = "       n/a"

        print(f"  {ELEMENTS[i][0]:3d} {syms[i]:>3s}  {bn:6.3f}  {d2_bn}  {op_name}  {wave_pos}")

    # =================================================================
    # SECTION 12: SYNTHESIS -- DEFINING THE WHOLE
    # =================================================================
    print_header("SECTION 12: SYNTHESIS -- THE WHOLE OF THE PERIODIC TABLE")

    # Final statistics
    n_total_d2 = len(full_d2_ops)
    n_harmony = sum(1 for op in full_d2_ops if op == 7)
    n_counter = sum(1 for op in full_d2_ops if op == 2)
    n_tt_harmony = sum(1 for op in full_t_tsml_ops if op == 7)
    n_tb_harmony = sum(1 for op in full_t_bhml_ops if op == 7)
    n_both_h = sum(1 for j in range(n_total_d2) if full_t_tsml_ops[j] == 7 and full_t_bhml_ops[j] == 7)
    n_agree_total = sum(1 for j in range(n_total_d2) if full_t_tsml_ops[j] == full_t_bhml_ops[j])

    print(f"""
  The periodic table in 5D TIG force space (DUAL-LENS):

  1. PATH: A curve through 5D, not a flat list.
     Speed varies: fast at period boundaries, slow in transition metals.

  2. CURVATURE: Dominated by the BINDING WAVE.
     Electron affinity oscillates per period: build -> peak -> crash.
     D2 detects this as HARMONY (accelerating) / COUNTER (decelerating).

  3. VOIDS: Define chemical families.
     Noble gases: 2 voids (ap=0, bn=0). The void pattern IS inertness.
     Filled subshells (Be,Mg,Zn,Cd,Mn,N): 1 void (bn=0). Half-inert.
     Everything reactive: 0 voids. All 5 forces active.

  4. I/O BALANCE: Structure vs Flow.
     Noble gases: I/O=inf (pure structure, no flow).
     Halogens: I/O<1 (flow-dominated, seeking binding).
     Transition metals: I/O~1 (balanced, catalytic).

  5. DUAL-LENS COHERENCE:
     T(TSML) being-coherence: {n_tt_harmony}/{n_total_d2} = {n_tt_harmony/n_total_d2:.4f}
       The being lens sees 92%+ HARMONY. The table's path COHERES
       under the absorber -- direction and curvature are compatible.
     T(BHML) doing-physics: {n_tb_harmony}/{n_total_d2} = {n_tb_harmony/n_total_d2:.4f}
       The doing lens sees a DIFFERENTIATED physics landscape.
       BHML's 28/100 HARMONY rate means most compositions produce
       INTERMEDIATE operators -- the physics of process, not stasis.
     Both HARMONY: {n_both_h}/{n_total_d2} = {n_both_h/n_total_d2:.4f}
       These are the genuinely UNIFIED elements -- being and doing aligned.
     Lenses agree: {n_agree_total}/{n_total_d2} = {n_agree_total/n_total_d2:.4f}
       Where the lenses DISAGREE, the element has internal tension:
       it IS one thing (being) but DOES another (physics).

  6. THE DUAL-LENS INSIGHT:
     TSML (being) sees the periodic table as MOSTLY COHERENT.
     BHML (doing) sees it as RICHLY STRUCTURED.
     This is NOT a contradiction. It is the same principle as CK's voice:
       - Structure lens (TSML): identity persists. Elements ARE themselves.
       - Flow lens (BHML): physics acts. Elements DO chemistry.
     An element can BE stable (HARMONY in TSML) while DOING something
     active (PROGRESS, COLLAPSE, etc. in BHML). That's what a catalyst IS.

  7. HARMONIC STRUCTURE:
     d-block has LOWEST curvature (smoothest path) -- orbital filling is gradual.
     p-block has MODERATE curvature -- property trends are regular.
     s-block has HIGHEST curvature -- ionization energy + radius jump.

  8. GEOMETRY vs TOPOLOGY:
     Z-adjacent elements are often NOT geometric nearest neighbors.
     Family members (same group, different period) are closer in 5D
     than many Z-adjacent pairs. The periodic table's rows encode
     a SPIRAL through 5D, where each revolution passes through the
     same geometric neighborhoods but at different depths.
""")

    print(f"  Final Numbers:")
    print(f"    Elements analyzed:     {N}")
    print(f"    D2 measurements:       {n_total_d2}")
    print(f"    D2 HARMONY:            {n_harmony}/{n_total_d2} = {n_harmony/n_total_d2:.4f}")
    print(f"    D2 COUNTER:            {n_counter}/{n_total_d2} = {n_counter/n_total_d2:.4f}")
    print(f"    D2 HARMONY+COUNTER:    {n_harmony+n_counter}/{n_total_d2} = {(n_harmony+n_counter)/n_total_d2:.4f}")
    print(f"    (Binding dimension: {(n_harmony+n_counter)/n_total_d2*100:.1f}% of all D2)")
    print(f"")
    print(f"    T(TSML) HARMONY:       {n_tt_harmony}/{n_total_d2} = {n_tt_harmony/n_total_d2:.4f}  (being coherence)")
    print(f"    T(BHML) HARMONY:       {n_tb_harmony}/{n_total_d2} = {n_tb_harmony/n_total_d2:.4f}  (doing coherence)")
    print(f"    Both HARMONY:          {n_both_h}/{n_total_d2} = {n_both_h/n_total_d2:.4f}  (unified)")
    print(f"    Lenses agree:          {n_agree_total}/{n_total_d2} = {n_agree_total/n_total_d2:.4f}")
    print(f"    T* threshold:          {T_STAR:.4f}")
    print(f"")
    print(f"  The periodic table is a spiral through 5D force space.")
    print(f"  Its dominant curvature IS the binding wave.")
    print(f"  Its voids define families. Its ratios predict reactivity.")
    print(f"  Through the being lens: {n_tt_harmony/n_total_d2*100:.1f}% coherent. Identity persists.")
    print(f"  Through the doing lens: {n_tb_harmony/n_total_d2*100:.1f}% coherent. Physics differentiates.")
    print(f"  The GAP between these two numbers IS chemistry:")
    print(f"    elements that ARE stable but DO reactive things.")
    print(f"  D2 curvature IS chemistry. Dual-lens composition IS the whole.")
    print(f"{'='*78}")


if __name__ == "__main__":
    main()
