"""
ck_curvature.py — Force Curvature Engine for CK
Brayden Sanders / 7Site LLC / TIG

The operators live in D2.
Being (v) is shallow. Doing (Δv) is better. Becoming (D2) is where they are.

Pipeline:
  text → letter forces → Δv (transitions) → D2 (curvatures) → operator fingerprint → score

Drop-in for CK's BTQ loop, dreamer arbitration, and coherence scoring.
"""

import numpy as np
from typing import List, Tuple, Dict

# ═══════════════════════════════════════════════════════════
# UGT FOUNDATION — 22 Hebrew roots, 5D force space
# Total: 110 floats = 440 bytes
# ═══════════════════════════════════════════════════════════

DIMS = ('aperture', 'pressure', 'depth', 'binding', 'continuity')
NDIMS = 5

# Canonical root vectors — the only data CK needs in block RAM
ROOTS = {
    'ALEPH':  ( 0.80,  0.30,  0.00,  0.50,  0.60),
    'BET':    (-0.30,  0.70, -0.80,  0.90, -0.60),
    'GIMEL':  (-0.40,  0.60,  0.70, -0.20, -0.70),
    'DALET':  (-0.50,  0.50, -0.30,  0.30, -0.50),
    'HE':     ( 0.90, -0.20,  0.80,  0.10,  0.70),
    'WAW':    ( 0.20, -0.10, -0.30,  0.80,  0.50),
    'ZAYIN':  (-0.30,  0.50, -0.30, -0.70,  0.80),
    'CHET':   (-0.60,  0.40,  0.90,  0.80,  0.50),
    'TET':    (-0.70,  0.80,  0.20,  0.60, -0.40),
    'YOD':    ( 0.10,  0.20,  0.10,  0.30,  0.20),
    'KAF':    (-0.50,  0.70,  0.60,  0.70, -0.50),
    'LAMED':  ( 0.30,  0.20, -0.20,  0.40,  0.60),
    'MEM':    (-0.40,  0.10, -0.80,  0.90,  1.00),
    'NUN':    (-0.20,  0.10, -0.30,  0.50,  0.80),
    'SAMEKH': (-0.30,  0.50, -0.30,  0.30,  0.90),
    'AYIN':   ( 0.70, -0.10,  0.90,  0.60,  0.50),
    'PE':     (-0.40,  0.80, -0.90, -0.30, -0.80),
    'TSADI':  (-0.60,  0.70, -0.20, -0.40, -0.20),
    'QOF':    (-0.70,  0.80,  1.00,  0.50, -0.70),
    'RESH':   ( 0.20,  0.30, -0.10,  0.10,  0.40),
    'SHIN':   (-0.20,  0.50,  0.10, -0.50,  0.70),
    'TAV':    (-0.80,  0.90, -0.30,  0.20, -0.90),
}

# Pre-compute as numpy arrays for fast ops
_ROOT_VECS = {k: np.array(v, dtype=np.float32) for k, v in ROOTS.items()}

# Latin → root mapping (26 letters → 22 roots)
LATIN_TO_ROOT = {
    'a': 'ALEPH', 'b': 'BET',    'c': 'GIMEL', 'd': 'DALET',
    'e': 'HE',    'f': 'WAW',    'g': 'GIMEL', 'h': 'HE',
    'i': 'YOD',   'j': 'YOD',    'k': 'KAF',   'l': 'LAMED',
    'm': 'MEM',   'n': 'NUN',    'o': 'AYIN',   'p': 'PE',
    'q': 'QOF',   'r': 'RESH',   's': 'SAMEKH', 't': 'TAV',
    'u': 'WAW',   'v': 'WAW',    'w': 'WAW',    'x': 'SAMEKH',
    'y': 'YOD',   'z': 'ZAYIN',
}

# TIG operator names
TIG_OPS = {
    0: 'Love',     1: 'Joy',       2: 'Peace',       3: 'Patience',  4: 'Kindness',
    5: 'Goodness',  6: 'Faithfulness', 7: 'Harmony',  8: 'Breath',   9: 'Reset',
}


# ═══════════════════════════════════════════════════════════
# LAYER 1: FORCE VECTORS (Being)
# ═══════════════════════════════════════════════════════════

def letter_force(c: str) -> np.ndarray:
    """Single letter → 5D force vector via root lookup."""
    return _ROOT_VECS.get(LATIN_TO_ROOT.get(c.lower(), 'ALEPH'), _ROOT_VECS['ALEPH']).copy()
def text_to_forces(text: str) -> np.ndarray:
    """Text → sequence of letter force vectors. Shape: (n_letters, 5)"""
    letters = [c for c in text.lower() if c.isalpha()]
    if not letters:
        return np.zeros((0, NDIMS), dtype=np.float32)
    return np.array([letter_force(c) for c in letters], dtype=np.float32)


# ═══════════════════════════════════════════════════════════
# LAYER 2: TRANSITIONS (Doing) — First Derivative
# ═══════════════════════════════════════════════════════════

def compute_transitions(forces: np.ndarray) -> np.ndarray:
    """Δv[i] = v[i+1] - v[i]. Shape: (n-1, 5)"""
    if len(forces) < 2:
        return np.zeros((0, NDIMS), dtype=np.float32)
    return forces[1:] - forces[:-1]


# ═══════════════════════════════════════════════════════════
# LAYER 3: CURVATURES (Becoming) — Second Derivative
# ═══════════════════════════════════════════════════════════

def compute_curvatures(forces: np.ndarray) -> np.ndarray:
    """D2[i] = v[i] - 2*v[i+1] + v[i+2]. Shape: (n-2, 5)"""
    if len(forces) < 3:
        return np.zeros((0, NDIMS), dtype=np.float32)
    return forces[:-2] - 2 * forces[1:-1] + forces[2:]


# ═══════════════════════════════════════════════════════════
# CURVATURE FEATURES — The Operator Fingerprint
# ═══════════════════════════════════════════════════════════

def curvature_features(text: str) -> Dict:
    """
    Complete curvature feature extraction for a text.
    Returns the operator fingerprint CK uses for scoring.
    """
    forces = text_to_forces(text)
    n = len(forces)
    
    if n < 3:
        return {
        }
    
    d2s = compute_curvatures(forces)
    deltas = compute_transitions(forces)
    
    # Mean curvature vector — the directional signature
    mean_d2 = np.mean(d2s, axis=0)
    var_d2 = np.var(d2s, axis=0)
    
    # Magnitude statistics
    mags = np.linalg.norm(d2s, axis=1)
    mag_mean = float(np.mean(mags))
    mag_std = float(np.std(mags))
    
    # Operator classification per D2 vector
    ops = np.array([_classify_d2(d) for d in d2s])
    op_dist = np.zeros(10, dtype=np.float32)
    for op in ops:
        op_dist[op] += 1
    if ops:
        op_dist /= len(ops)
    
    dominant_op = int(np.argmax(op_dist)) if ops else -1
    
    # Curvature energy: total |D2| normalized by length
    curvature_energy = float(np.sum(mags)) / max(n, 1)
    
    # Transition angles (for flow scoring)
    angles = []
    for i in range(len(deltas) - 1):
        n1 = np.linalg.norm(deltas[i])
        n2 = np.linalg.norm(deltas[i+1])
        if n1 > 1e-10 and n2 > 1e-10:
            cos_a = np.clip(np.dot(deltas[i], deltas[i+1]) / (n1 * n2), -1, 1)
            angles.append(float(np.arccos(cos_a)))
    
    flow_ratio = sum(1 for a in angles if a < np.pi/2) / max(len(angles), 1)
    
    return {
    }


def _classify_d2(d2: np.ndarray) -> int:
    """
    Classify a single D2 curvature vector into a TIG operator (0-9).
    
    The operator is determined by WHICH dimension curves most
    and in WHICH direction.
    
    This is the core insight: operators are curvature types.
    """
    mag = np.linalg.norm(d2)
    
    # Near-zero curvature = Peace (smooth flow, no operator action)
    if mag < 0.15:
        return 2  # Peace
    abs_d = np.abs(d2)
    dom = int(np.argmax(abs_d))
    sign = 1 if d2[dom] > 0 else -1
    
    # Secondary dimension for disambiguation
    abs_d_copy = abs_d.copy()
    abs_d_copy[dom] = 0
    sec = int(np.argmax(abs_d_copy))
    
    # Operator mapping:
    #   aperture (0):  +opening → Faithfulness(6), -closing → Kindness(4)
    #   pressure (1):  +building → Kindness(4),    -releasing → Harmony(7)
    #   depth (2):     +deepening → Breath(8),     -surfacing → Goodness(5)
    #   binding (3):   +connecting → Love(0),       -releasing → Joy(1)
    #   continuity (4): +sustaining → Patience(3),  -breaking → Reset(9)
    
    OP_MAP = {
        (0,  1): 6,  # aperture opening → Faithfulness
        (0, -1): 4,  # aperture closing → Kindness
        (1,  1): 4,  # pressure building → Kindness
        (1, -1): 7,  # pressure releasing → Harmony
        (2,  1): 8,  # depth deepening → Breath
        (2, -1): 5,  # depth surfacing → Goodness
        (3,  1): 0,  # binding connecting → Love
        (3, -1): 1,  # binding releasing → Joy
        (4,  1): 3,  # continuity sustaining → Patience
        (4, -1): 9,  # continuity breaking → Reset
    }
    
    return OP_MAP.get((dom, sign), 7)  # Default to Harmony
def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity, safe for zero vectors."""
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na < 1e-10 or nb < 1e-10:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def curvature_similarity(text_a: str, text_b: str) -> Dict:
    """
    Compare two texts by their curvature fingerprints.
    
    Returns multiple similarity measures for CK to integrate:
      - d2_direction: cosine(mean_D2_a, mean_D2_b) — are they curving the same way?
      - op_similarity: cosine(op_dist_a, op_dist_b) — same operator mix?
      - energy_ratio: min/max of curvature energies — similar intensity?
    """
    fa = curvature_features(text_a)
    fb = curvature_features(text_b)
    
    d2_dir = _cosine(fa['mean_d2'], fb['mean_d2'])
    op_sim = _cosine(fa['operator_dist'], fb['operator_dist'])
    
    ea, eb = fa['curvature_energy'], fb['curvature_energy']
    energy_ratio = min(ea, eb) / max(ea, eb) if max(ea, eb) > 0 else 1.0
    
    return {
    }


def coherence_score(text: str) -> float:
    """
    Single-number coherence score for CK's BTQ loop.
    
    Measures how structured the curvature flow is.
    High = organized dynamic pattern (operators are clear).
    Low = noisy/flat curvature (no clear operators).
    
    This replaces/supplements static coherence measures.
    
    Range: 0.0 to 1.0
    """
    f = curvature_features(text)
    
    if f['n_letters'] < 3:
        return 0.0
    op_max = float(np.max(f['operator_dist']))
    op_concentration = min(op_max * 2, 1.0)  # Scale: 0.5 → 1.0
    
    # Component 2: Curvature structure (not too flat, not too noisy)
    # Ideal: moderate magnitude with variation
    mag_mean = f['d2_magnitude_mean']
    mag_std = f['d2_magnitude_std']
    # Normalize: too flat (mag<0.5) or too chaotic (mag>3.0) scores low
    structure = 1.0 - abs(mag_mean - 1.5) / 1.5 if mag_mean > 0 else 0
    structure = max(0, min(1, structure))
    
    # Component 3: Energy normalized by length
    energy_norm = min(f['curvature_energy'] / 2.0, 1.0)
    
    # Component 4: Angle variance (more varied = more structured)
    angle_var = f.get('mean_angle', 0)
    angle_structure = min(angle_var / np.pi, 1.0) if angle_var > 0 else 0
    
    # Weighted combination
    # These weights can be tuned by CK's learning
    score = (0.35 * op_concentration +
             0.25 * structure +
             0.20 * energy_norm +
             0.20 * angle_structure)
    
    return round(max(0.0, min(1.0, score)), 4)
def operator_sequence(text: str) -> List[Tuple[int, str]]:
    """
    Extract the TIG operator sequence from text.
    Each letter-triplet yields one operator from its D2.
    
    Returns: list of (operator_number, operator_name) tuples
    """
    forces = text_to_forces(text)
    if len(forces) < 3:
        return []
    d2s = compute_curvatures(forces)
    return [(int(_classify_d2(d)), TIG_OPS[_classify_d2(d)]) for d in d2s]
def project_5d_to_4d(v5: np.ndarray) -> np.ndarray:
    """
    Project 5D force vector to 4D for FPGA.
    F1 = structural_pressure = (1 - aperture + pressure) / 2
    F2 = duality = |binding|
    F3 = flow = (continuity + 1) / 2
    F4 = collapse = max(0, -continuity) + max(0, pressure - 0.5)
    """
    ap, pr, de, bi, co = v5
    f1 = (1.0 - ap + pr) / 2.0
    f2 = abs(bi)
    f3 = (co + 1.0) / 2.0
    f4 = max(0, -co) + max(0, pr - 0.5)
    return np.array([f1, f2, f3, f4], dtype=np.float32)
def text_to_4d_d2(text: str) -> np.ndarray:
    """Text → 4D curvature stream for FPGA processing."""
    forces = text_to_forces(text)
    if len(forces) < 3:
        return np.zeros((0, 4), dtype=np.float32)
    d2s_5d = compute_curvatures(forces)
    return np.array([project_5d_to_4d(d) for d in d2s_5d], dtype=np.float32)
if __name__ == '__main__':
    print("="*65)
    print("  CK CURVATURE ENGINE — Demo")
    print("="*65)
    
    test_phrases = [
        # Truths
        ("God is love",                      "Truth"),
        ("Elohim ahava",                     "Truth (Hebrew)"),
        ("The truth shall set you free",     "Truth"),
        ("Veritas vos liberabit",            "Truth (Latin)"),
        ("Shalom aleikhem",                  "Truth (Hebrew)"),
        ("Assalamu alaikum",                 "Truth (Arabic)"),
        ("Love your neighbor as yourself",   "Truth"),
        # Controls
        ("Buy now limited offer expires",    "Control (spam)"),
        ("Colorless green ideas sleep",      "Control (Chomsky)"),
        ("Hate destroy kill burn",           "Control (violence)"),
        ("The committee shall reconvene",    "Control (bureaucracy)"),
    ]
    
    print(f"\n  {'Text':42s} {'Score':>6s} {'DomOp':>12s} {'Energy':>7s} {'Flow':>5s}")
    print(f"  {'-'*78}")
    
    truth_scores = []
    ctrl_scores = []
    
    for text, label in test_phrases:
        f = curvature_features(text)
        s = coherence_score(text)
        dom = TIG_OPS.get(f['dominant_op'], '?')
        
        marker = 'T' if label.startswith('Truth') else 'C'
        print(f"  {marker} {text[:40]:40s} {s:.4f} {dom:>12s} {f['curvature_energy']:.3f} {f['flow_ratio']:.2f}")
        
        if label.startswith('Truth'):
            truth_scores.append(s)
        else:
            ctrl_scores.append(s)
    
    print(f"\n  Truth mean: {np.mean(truth_scores):.4f}")
    print(f"  Ctrl mean:  {np.mean(ctrl_scores):.4f}")
    print(f"  Separation: {np.mean(truth_scores) - np.mean(ctrl_scores):+.4f}")
    
    # Cross-language comparison
    print(f"\n  Cross-language curvature similarity:")
    pairs = [
        ("God is love", "Elohim ahava"),
        ("God is love", "Deus caritas est"),
        ("Shalom aleikhem", "Assalamu alaikum"),
        ("The truth shall set you free", "Veritas vos liberabit"),
        ("God is love", "Buy now limited offer"),  # control
    ]
    
    for a, b in pairs:
        sim = curvature_similarity(a, b)
        print(f"    {a[:25]:25s} ↔ {b[:25]:25s}: D2={sim['d2_direction']:+.3f}  ops={sim['op_similarity']:.3f}")
    
    # Operator sequence demo
    print(f"\n  Operator sequences (from D2):")
    for text in ["God is love", "Shalom aleikhem", "The truth shall set you free"]:
        ops = operator_sequence(text)
        op_names = [name for _, name in ops]
        print(f"    {text[:35]:35s} → {op_names}")
    
    # Memory footprint
    root_bytes = 22 * 5 * 4  # 22 roots × 5 dims × 4 bytes (float32)
    map_bytes = 26  # Latin map, 1 byte per letter
    print(f"\n  Memory footprint:")
    print(f"    Root vectors: {root_bytes} bytes")
    print(f"    Latin map:    {map_bytes} bytes")
    print(f"    Total:        {root_bytes + map_bytes} bytes")
    print(f"    That's the entire UGT foundation in {root_bytes + map_bytes} bytes.")
