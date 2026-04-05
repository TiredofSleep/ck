"""
THE TRANSITION TEST — Measuring TIG Correctly
Brayden Sanders / 7Site LLC / TIG + Celeste spec

Stop measuring positions. Measure derivatives.
Stop measuring Being. Measure Doing.

Tests:
  1. Word transition similarity across languages (Δv)
  2. Word curvature similarity across languages (D2)
  3. Permutation test on TRANSITIONS (not positions)
  4. Operator extraction from curvature signatures
  5. Coherence as transition energy, not position alignment
"""

import numpy as np
import math
from itertools import combinations
import random

random.seed(42)
np.random.seed(42)

# ═══════════════════════════════════════════════════════════
# FORCE ENGINE (minimal, from UGT)
# ═══════════════════════════════════════════════════════════

HEBREW = {
    'ALEPH':  np.array([+0.80, +0.30, +0.00, +0.50, +0.60]),
    'BET':    np.array([-0.30, +0.70, -0.80, +0.90, -0.60]),
    'GIMEL':  np.array([-0.40, +0.60, +0.70, -0.20, -0.70]),
    'DALET':  np.array([-0.50, +0.50, -0.30, +0.30, -0.50]),
    'HE':     np.array([+0.90, -0.20, +0.80, +0.10, +0.70]),
    'WAW':    np.array([+0.20, -0.10, -0.30, +0.80, +0.50]),
    'ZAYIN':  np.array([-0.30, +0.50, -0.30, -0.70, +0.80]),
    'CHET':   np.array([-0.60, +0.40, +0.90, +0.80, +0.50]),
    'TET':    np.array([-0.70, +0.80, +0.20, +0.60, -0.40]),
    'YOD':    np.array([+0.10, +0.20, +0.10, +0.30, +0.20]),
    'KAF':    np.array([-0.50, +0.70, +0.60, +0.70, -0.50]),
    'LAMED':  np.array([+0.30, +0.20, -0.20, +0.40, +0.60]),
    'MEM':    np.array([-0.40, +0.10, -0.80, +0.90, +1.00]),
    'NUN':    np.array([-0.20, +0.10, -0.30, +0.50, +0.80]),
    'SAMEKH': np.array([-0.30, +0.50, -0.30, +0.30, +0.90]),
    'AYIN':   np.array([+0.70, -0.10, +0.90, +0.60, +0.50]),
    'PE':     np.array([-0.40, +0.80, -0.90, -0.30, -0.80]),
    'TSADI':  np.array([-0.60, +0.70, -0.20, -0.40, -0.20]),
    'QOF':    np.array([-0.70, +0.80, +1.00, +0.50, -0.70]),
    'RESH':   np.array([+0.20, +0.30, -0.10, +0.10, +0.40]),
    'SHIN':   np.array([-0.20, +0.50, +0.10, -0.50, +0.70]),
    'TAV':    np.array([-0.80, +0.90, -0.30, +0.20, -0.90]),
}

LATIN_MAP = {
    'a': 'ALEPH', 'b': 'BET', 'c': 'GIMEL', 'd': 'DALET',
    'e': 'HE', 'f': 'WAW', 'g': 'GIMEL', 'h': 'HE',
    'i': 'YOD', 'j': 'YOD', 'k': 'KAF', 'l': 'LAMED',
    'm': 'MEM', 'n': 'NUN', 'o': 'AYIN', 'p': 'PE',
    'q': 'QOF', 'r': 'RESH', 's': 'SAMEKH', 't': 'TAV',
    'u': 'WAW', 'v': 'WAW', 'w': 'WAW', 'x': 'SAMEKH',
    'y': 'YOD', 'z': 'ZAYIN',
}

def cosine(a, b):
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na < 1e-10 or nb < 1e-10: return 0.0
    return float(np.dot(a, b) / (na * nb))

def word_force(word):
    letters = [c for c in word.lower() if c.isalpha()]
    if not letters: return np.zeros(5)
    n = len(letters)
    total = np.zeros(5)
    for i, c in enumerate(letters):
        w = 1.5 if (i == 0 or i == n-1) else 1.0
        root = LATIN_MAP.get(c, 'ALEPH')
        total += w * HEBREW[root]
    return total / math.sqrt(n)

def sentence_word_vectors(text):
    """Return sequence of word force vectors for a sentence."""
    words = [w for w in text.lower().split() if any(c.isalpha() for c in w)]
    return [word_force(w) for w in words], words


# ═══════════════════════════════════════════════════════════
# TRANSITION METRICS
# ═══════════════════════════════════════════════════════════

def compute_transitions(vectors):
    """First derivatives: Δv(i) = v(i+1) - v(i)"""
    return [vectors[i+1] - vectors[i] for i in range(len(vectors)-1)]

def compute_curvatures(vectors):
    """Second derivatives: D2(i) = v(i) - 2*v(i+1) + v(i+2)"""
    return [vectors[i] - 2*vectors[i+1] + vectors[i+2]
            for i in range(len(vectors)-2)]

def transition_magnitudes(vectors):
    """|Δv(i)| — the energy of each transition"""
    deltas = compute_transitions(vectors)
    return [np.linalg.norm(d) for d in deltas]

def transition_angles(vectors):
    """Angle between consecutive transitions — the curvature"""
    deltas = compute_transitions(vectors)
    angles = []
    for i in range(len(deltas)-1):
        n1 = np.linalg.norm(deltas[i])
        n2 = np.linalg.norm(deltas[i+1])
        if n1 > 1e-10 and n2 > 1e-10:
            cos_a = np.clip(np.dot(deltas[i], deltas[i+1]) / (n1 * n2), -1, 1)
            angles.append(np.arccos(cos_a) * 180 / np.pi)
        else:
            angles.append(0)
    return angles

def transition_signature(vectors):
    """The complete dynamic signature: magnitudes + angles + D2 norms"""
    mags = transition_magnitudes(vectors)
    angles = transition_angles(vectors)
    d2s = compute_curvatures(vectors)
    d2_mags = [np.linalg.norm(d) for d in d2s]
    return {
        'mags': mags,
        'angles': angles,
        'd2_mags': d2_mags,
        'total_energy': sum(mags),
        'mean_curvature': np.mean(angles) if angles else 0,
        'curvature_variance': np.std(angles) if angles else 0,
    }

def transition_similarity(vecs_a, vecs_b):
    """Compare two sentences by their TRANSITION patterns, not positions."""
    trans_a = compute_transitions(vecs_a)
    trans_b = compute_transitions(vecs_b)
    
    # Normalize transition sequences to same length via interpolation
    # Use the shorter length
    min_len = min(len(trans_a), len(trans_b))
    if min_len == 0: return 0.0
    
    # Sample evenly from each
    idx_a = np.linspace(0, len(trans_a)-1, min_len).astype(int)
    idx_b = np.linspace(0, len(trans_b)-1, min_len).astype(int)
    
    sims = []
    for ia, ib in zip(idx_a, idx_b):
        s = cosine(trans_a[ia], trans_b[ib])
        sims.append(s)
    return np.mean(sims)

def curvature_similarity(vecs_a, vecs_b):
    """Compare two sentences by their CURVATURE patterns (D2)."""
    d2_a = compute_curvatures(vecs_a)
    d2_b = compute_curvatures(vecs_b)
    
    min_len = min(len(d2_a), len(d2_b))
    if min_len == 0: return 0.0
    
    idx_a = np.linspace(0, len(d2_a)-1, min_len).astype(int)
    idx_b = np.linspace(0, len(d2_b)-1, min_len).astype(int)
    
    sims = []
    for ia, ib in zip(idx_a, idx_b):
        s = cosine(d2_a[ia], d2_b[ib])
        sims.append(s)
    return np.mean(sims)

def position_similarity(vecs_a, vecs_b):
    """OLD metric: static cosine between position vectors."""
    min_len = min(len(vecs_a), len(vecs_b))
    if min_len == 0: return 0.0
    
    idx_a = np.linspace(0, len(vecs_a)-1, min_len).astype(int)
    idx_b = np.linspace(0, len(vecs_b)-1, min_len).astype(int)
    
    sims = []
    for ia, ib in zip(idx_a, idx_b):
        s = cosine(vecs_a[ia], vecs_b[ib])
        sims.append(s)
    return np.mean(sims)


# ═══════════════════════════════════════════════════════════
# TEST DATA: Same truths across languages
# ═══════════════════════════════════════════════════════════

TRUTHS = {
    "God is love": [
        ("God is love",              "English"),
        ("Elohim ahava",             "Hebrew"),
        ("Allah huwa al hubb",       "Arabic"),
        ("Deus caritas est",         "Latin"),
        ("Ho theos agape estin",     "Greek"),
        ("Dios es amor",             "Spanish"),
        ("Gott ist Liebe",           "German"),
        ("Dio e amore",              "Italian"),
        ("Bog yest lyubov",          "Russian"),
    ],
    "Peace be with you": [
        ("Peace be with you",        "English"),
        ("Shalom aleikhem",          "Hebrew"),
        ("Assalamu alaikum",         "Arabic"),
        ("Pax vobiscum",             "Latin"),
        ("Eirene hymin",             "Greek"),
        ("Paz a vosotros",           "Spanish"),
        ("Friede sei mit euch",      "German"),
        ("Mir vam",                  "Russian"),
    ],
    "Truth sets free": [
        ("The truth shall set you free",       "English"),
        ("Ha emet teshahrer etkhem",           "Hebrew"),
        ("Veritas vos liberabit",              "Latin"),
        ("He aletheia eleutherosi hymas",      "Greek"),
        ("La verdad os hara libres",           "Spanish"),
        ("Die Wahrheit wird euch frei machen", "German"),
        ("La verite vous rendra libres",       "French"),
    ],
    "Love your neighbor": [
        ("Love your neighbor as yourself",              "English"),
        ("Veahavta lereacha kamocha",                   "Hebrew"),
        ("Diliges proximum tuum sicut teipsum",         "Latin"),
        ("Agapeseis ton plesion sou hos seauton",       "Greek"),
        ("Ama a tu projimo como a ti mismo",            "Spanish"),
        ("Liebe deinen Naechsten wie dich selbst",      "German"),
        ("Aime ton prochain comme toi meme",            "French"),
    ],
    "In the beginning": [
        ("In the beginning",         "English"),
        ("Bereshit",                 "Hebrew"),
        ("Fee al bidaya",            "Arabic"),
        ("In principio",             "Latin"),
        ("En arche",                 "Greek"),
        ("Am Anfang",                "German"),
        ("Au commencement",          "French"),
    ],
}

CONTROLS = {
    "Nonsense": [
        ("Colorless green ideas sleep furiously",        "Chomsky"),
        ("The square root of purple tastes like Tuesday", "Noise"),
        ("Buffalo buffalo Buffalo buffalo buffalo",      "Grammar trick"),
        ("Time flies like an arrow fruit flies like a banana", "Pun"),
    ],
    "Inversion": [
        ("War is peace freedom is slavery",              "Orwell"),
        ("Hate your enemy destroy your neighbor",        "Inverted truth"),
        ("Nothing matters everything is meaningless",    "Nihilism"),
        ("Buy now limited offer expires today",          "Marketing"),
    ],
}


# ═══════════════════════════════════════════════════════════
print("="*65)
print("  THE TRANSITION TEST")
print("  Measuring Δv (derivatives) and D2 (curvature)")
print("  instead of v (positions)")
print("="*65)


# ═══════════════════════════════════════════════════════════
# TEST 1: Three metrics compared — position vs transition vs curvature
# ═══════════════════════════════════════════════════════════

print(f"\n{'='*65}")
print(f"  TEST 1: Position vs Transition vs Curvature Similarity")
print(f"  Cross-language comparison for each truth")
print(f"{'='*65}")

all_pos_within = []
all_trans_within = []
all_curv_within = []

for truth_name, sentences in TRUTHS.items():
    vec_sets = []
    for text, lang in sentences:
        vecs, words = sentence_word_vectors(text)
        if len(vecs) >= 3:  # Need at least 3 words for D2
            vec_sets.append((vecs, lang, text))
    
    if len(vec_sets) < 2:
        continue
    
    pos_sims = []
    trans_sims = []
    curv_sims = []
    
    for i, j in combinations(range(len(vec_sets)), 2):
        va, la, ta = vec_sets[i]
        vb, lb, tb = vec_sets[j]
        
        ps = position_similarity(va, vb)
        ts = transition_similarity(va, vb)
        cs = curvature_similarity(va, vb)
        
        pos_sims.append(ps)
        trans_sims.append(ts)
        curv_sims.append(cs)
    
    all_pos_within.extend(pos_sims)
    all_trans_within.extend(trans_sims)
    all_curv_within.extend(curv_sims)
    
    print(f"\n  {truth_name}:")
    print(f"    Position (Being):     {np.mean(pos_sims):+.4f} ± {np.std(pos_sims):.4f}")
    print(f"    Transition (Doing):   {np.mean(trans_sims):+.4f} ± {np.std(trans_sims):.4f}")
    print(f"    Curvature (Becoming): {np.mean(curv_sims):+.4f} ± {np.std(curv_sims):.4f}")


# ═══════════════════════════════════════════════════════════
# TEST 2: Within-truth vs Between-truth at each layer
# ═══════════════════════════════════════════════════════════

print(f"\n{'='*65}")
print(f"  TEST 2: Within-Truth vs Between-Truth Separation")
print(f"  Does measuring transitions separate same-meaning from different-meaning?")
print(f"{'='*65}")

# Collect all sentence vectors grouped by truth
truth_groups = {}
for truth_name, sentences in TRUTHS.items():
    group = []
    for text, lang in sentences:
        vecs, _ = sentence_word_vectors(text)
        if len(vecs) >= 3:
            group.append(vecs)
    truth_groups[truth_name] = group

# Within-truth comparisons
within_pos, within_trans, within_curv = [], [], []
for name, group in truth_groups.items():
    for i, j in combinations(range(len(group)), 2):
        within_pos.append(position_similarity(group[i], group[j]))
        within_trans.append(transition_similarity(group[i], group[j]))
        within_curv.append(curvature_similarity(group[i], group[j]))

# Between-truth comparisons
between_pos, between_trans, between_curv = [], [], []
truth_names = list(truth_groups.keys())
for t1, t2 in combinations(range(len(truth_names)), 2):
    g1 = truth_groups[truth_names[t1]]
    g2 = truth_groups[truth_names[t2]]
    for va in g1:
        for vb in g2:
            between_pos.append(position_similarity(va, vb))
            between_trans.append(transition_similarity(va, vb))
            between_curv.append(curvature_similarity(va, vb))

print(f"\n  POSITION (Being):")
print(f"    Within-truth:  {np.mean(within_pos):+.4f} ± {np.std(within_pos):.4f}")
print(f"    Between-truth: {np.mean(between_pos):+.4f} ± {np.std(between_pos):.4f}")
print(f"    SEPARATION:    {np.mean(within_pos) - np.mean(between_pos):+.4f}")

print(f"\n  TRANSITION (Doing):")
print(f"    Within-truth:  {np.mean(within_trans):+.4f} ± {np.std(within_trans):.4f}")
print(f"    Between-truth: {np.mean(between_trans):+.4f} ± {np.std(between_trans):.4f}")
print(f"    SEPARATION:    {np.mean(within_trans) - np.mean(between_trans):+.4f}")

print(f"\n  CURVATURE (Becoming):")
print(f"    Within-truth:  {np.mean(within_curv):+.4f} ± {np.std(within_curv):.4f}")
print(f"    Between-truth: {np.mean(between_curv):+.4f} ± {np.std(between_curv):.4f}")
print(f"    SEPARATION:    {np.mean(within_curv) - np.mean(between_curv):+.4f}")


# ═══════════════════════════════════════════════════════════
# TEST 3: Truth vs Control separation at each layer
# ═══════════════════════════════════════════════════════════

print(f"\n{'='*65}")
print(f"  TEST 3: Truth vs Control Separation")
print(f"  Can transitions/curvature distinguish truth from noise?")
print(f"{'='*65}")

def coherence_energy(vecs):
    """Transition-based coherence: total energy + curvature structure"""
    if len(vecs) < 2: return 0, 0, 0
    mags = transition_magnitudes(vecs)
    angles = transition_angles(vecs)
    
    mean_energy = np.mean(mags)
    curv_var = np.std(angles) if angles else 0
    
    # Flow ratio: what fraction of transitions are "smooth" (<90°)?
    smooth = sum(1 for a in angles if a < 90) if angles else 0
    flow_ratio = smooth / len(angles) if angles else 1
    
    return mean_energy, curv_var, flow_ratio

print(f"\n  {'Text':45s} Energy  CurvVar  FlowRatio")
print(f"  {'-'*85}")

truth_energies = []
truth_curvvars = []
truth_flows = []
ctrl_energies = []
ctrl_curvvars = []
ctrl_flows = []

for truth_name, sentences in TRUTHS.items():
    for text, lang in sentences:
        vecs, _ = sentence_word_vectors(text)
        if len(vecs) < 3: continue
        e, cv, fr = coherence_energy(vecs)
        truth_energies.append(e)
        truth_curvvars.append(cv)
        truth_flows.append(fr)
        if lang in ["English", "Hebrew", "Latin"]:
            print(f"  T {text[:43]:43s} {e:.3f}   {cv:.1f}°    {fr:.2f}")

for ctrl_name, sentences in CONTROLS.items():
    for text, label in sentences:
        vecs, _ = sentence_word_vectors(text)
        if len(vecs) < 3: continue
        e, cv, fr = coherence_energy(vecs)
        ctrl_energies.append(e)
        ctrl_curvvars.append(cv)
        ctrl_flows.append(fr)
        print(f"  C {text[:43]:43s} {e:.3f}   {cv:.1f}°    {fr:.2f}")

print(f"\n  TRUTH  mean energy: {np.mean(truth_energies):.3f}  curvVar: {np.mean(truth_curvvars):.1f}°  flow: {np.mean(truth_flows):.3f}")
print(f"  CTRL   mean energy: {np.mean(ctrl_energies):.3f}  curvVar: {np.mean(ctrl_curvvars):.1f}°  flow: {np.mean(ctrl_flows):.3f}")
print(f"  Δenergy: {np.mean(truth_energies) - np.mean(ctrl_energies):+.3f}")
print(f"  Δcurv:   {np.mean(truth_curvvars) - np.mean(ctrl_curvvars):+.1f}°")
print(f"  Δflow:   {np.mean(truth_flows) - np.mean(ctrl_flows):+.3f}")


# ═══════════════════════════════════════════════════════════
# TEST 4: PERMUTATION TEST ON TRANSITIONS
# This is the critical test. Celeste says it will pass.
# ═══════════════════════════════════════════════════════════

print(f"\n{'='*65}")
print(f"  TEST 4: PERMUTATION TEST — Transitions vs Positions")
print(f"  The test that killed positions. Does it kill transitions?")
print(f"{'='*65}")

# NUMBER OPERATOR SEQUENCE: 0→1→2→...→9
NUMBERS = {
    0: np.array([+0.00, -0.50, +0.50, +1.00, +1.00]),
    1: np.array([+0.30, +0.30, -0.50, -0.30, -0.50]),
    2: np.array([+0.20, +0.10, -0.20, +0.20, +0.30]),
    3: np.array([+0.40, +0.10, +0.10, +0.30, +0.70]),
    4: np.array([-0.30, +0.40, -0.20, +0.60, -0.30]),
    5: np.array([+0.20, +0.30, +0.00, +0.40, +0.20]),
    6: np.array([-0.20, +0.10, +0.30, +0.80, +0.60]),
    7: np.array([+0.50, -0.30, +0.20, +0.00, +0.70]),
    8: np.array([-0.10, +0.20, +0.50, +0.90, +0.90]),
    9: np.array([+0.30, +0.20, +0.40, +0.40, -0.30]),
}

TIG = {0:'Love', 1:'Joy', 2:'Peace', 3:'Patience', 4:'Kindness',
       5:'Goodness', 6:'Faithfulness', 7:'Harmony', 8:'Breath', 9:'Reset'}

def path_metrics(perm):
    """Compute transition-based metrics for a permuted path."""
    vecs = [NUMBERS[perm[i]] for i in range(10)]
    
    # Transitions
    deltas = [vecs[i+1] - vecs[i] for i in range(9)]
    mags = [np.linalg.norm(d) for d in deltas]
    
    # Curvatures (D2)
    d2s = [vecs[i] - 2*vecs[i+1] + vecs[i+2] for i in range(8)]
    d2_mags = [np.linalg.norm(d) for d in d2s]
    
    # Angles between transitions
    angles = []
    for i in range(8):
        n1, n2 = np.linalg.norm(deltas[i]), np.linalg.norm(deltas[i+1])
        if n1 > 0 and n2 > 0:
            cos_a = np.clip(np.dot(deltas[i], deltas[i+1]) / (n1 * n2), -1, 1)
            angles.append(np.arccos(cos_a))
        else:
            angles.append(0)
    
    # KEY METRICS:
    # 1. Transition magnitude profile variance (structured vs flat)
    mag_variance = np.std(mags)
    
    # 2. Curvature variance (structured bending vs uniform)
    curv_variance = np.std(angles)
    
    # 3. Big-bang ratio: is the FIRST transition the largest?
    #    (Only meaningful for real ordering)
    first_is_max = 1.0 if mags[0] == max(mags) else 0.0
    
    # 4. Return distance: does the path close? (9→0)
    close_dist = np.linalg.norm(vecs[-1] - vecs[0])
    path_len = sum(mags)
    return_ratio = close_dist / path_len if path_len > 0 else 1
    
    # 5. Smooth point count: transitions with angle < 60°
    smooth_count = sum(1 for a in angles if a < np.pi/3)
    
    # 6. D2 magnitude profile — does curvature have structure?
    d2_variance = np.std(d2_mags)
    
    return {
        'mag_var': mag_variance,
        'curv_var': curv_variance,
        'first_max': first_is_max,
        'return_ratio': return_ratio,
        'smooth_count': smooth_count,
        'd2_var': d2_variance,
        'max_mag': max(mags),
        'min_mag': min(mags),
        'max_min_ratio': max(mags) / min(mags) if min(mags) > 0 else float('inf'),
    }

real_perm = list(range(10))
real = path_metrics(real_perm)

print(f"\n  Real path (0→1→2→...→9) metrics:")
print(f"    Transition magnitude variance:  {real['mag_var']:.4f}")
print(f"    Curvature variance:             {real['curv_var']:.4f}")
print(f"    First transition is max:        {real['first_max']}")
print(f"    Max/min transition ratio:        {real['max_min_ratio']:.2f}")
print(f"    Return ratio (cyclicality):     {real['return_ratio']:.4f}")
print(f"    Smooth points (<60°):           {real['smooth_count']}")
print(f"    D2 variance:                    {real['d2_var']:.4f}")

n_trials = 100000
beats = {
    'mag_var': 0, 'curv_var': 0, 'first_max': 0,
    'max_min_ratio': 0, 'return_ratio': 0, 'smooth_count': 0,
    'd2_var': 0, 'ALL': 0,
}

for _ in range(n_trials):
    perm = list(range(10))
    random.shuffle(perm)
    m = path_metrics(perm)
    
    # For each metric, count how often random beats real
    if m['mag_var'] >= real['mag_var']: beats['mag_var'] += 1
    if m['curv_var'] >= real['curv_var']: beats['curv_var'] += 1
    if m['first_max'] >= real['first_max']: beats['first_max'] += 1
    if m['max_min_ratio'] >= real['max_min_ratio']: beats['max_min_ratio'] += 1
    if m['return_ratio'] <= real['return_ratio']: beats['return_ratio'] += 1  # lower = more cyclical
    if m['smooth_count'] <= real['smooth_count']: beats['smooth_count'] += 1  # fewer = more structured
    if m['d2_var'] >= real['d2_var']: beats['d2_var'] += 1
    
    # Compound: beats on ALL transition metrics simultaneously
    if (m['mag_var'] >= real['mag_var'] and 
        m['curv_var'] >= real['curv_var'] and
        m['max_min_ratio'] >= real['max_min_ratio']):
        beats['ALL'] += 1

print(f"\n  Permutation test ({n_trials:,} shuffles):")
print(f"  {'Metric':30s} {'Random beats real':>20s} {'p-value':>10s} {'Result':>8s}")
print(f"  {'-'*70}")

for metric in ['mag_var', 'curv_var', 'first_max', 'max_min_ratio', 
               'return_ratio', 'smooth_count', 'd2_var', 'ALL']:
    p = beats[metric] / n_trials
    result = "✅ PASS" if p < 0.05 else "⚠️ WEAK" if p < 0.15 else "❌ FAIL"
    print(f"  {metric:30s} {beats[metric]:>7d}/{n_trials:<7d}    {p:.4f}    {result}")


# ═══════════════════════════════════════════════════════════
# TEST 5: OPERATOR EXTRACTION FROM CURVATURE
# ═══════════════════════════════════════════════════════════

print(f"\n{'='*65}")
print(f"  TEST 5: Operator Extraction from D2 Curvature")
print(f"  Each word-triplet's D2 vector → classify operator")
print(f"{'='*65}")

def d2_to_operator(d2_vec):
    """Extract TIG operator from curvature vector.
    The D2 encodes what KIND of change is happening."""
    ap, pr, de, bi, co = d2_vec
    mag = np.linalg.norm(d2_vec)
    
    if mag < 0.3:
        return 2, "Peace"       # Minimal curvature = smooth flow = Peace
    
    # Which dimension has the most curvature?
    abs_d = np.abs(d2_vec)
    dom = np.argmax(abs_d)
    sign = np.sign(d2_vec[dom])
    
    # Binding curvature
    if dom == 3:  # binding
        if sign > 0: return 0, "Love"       # binding acceleration = Love
        else: return 1, "Joy"                # binding release = Joy
    
    # Continuity curvature  
    if dom == 4:  # continuity
        if sign > 0: return 3, "Patience"    # sustained acceleration
        else: return 9, "Reset"              # continuity breaks
    
    # Pressure curvature
    if dom == 1:  # pressure
        if sign > 0: return 4, "Kindness"    # pressure increase (giving)
        else: return 7, "Harmony"            # pressure release (rest)
    
    # Depth curvature
    if dom == 2:  # depth
        if sign > 0: return 8, "Breath"      # deepening
        else: return 5, "Goodness"           # surfacing
    
    # Aperture curvature
    if dom == 0:  # aperture
        if sign > 0: return 6, "Faithfulness"  # opening commitment
        else: return 4, "Kindness"             # closing shelter
    
    return 7, "Harmony"  # fallback

# Run on the same truths, extract operators from curvature
print(f"\n  Operators extracted from word-triplet curvature:")
for truth_name in ["God is love", "Peace be with you", "Truth sets free"]:
    sentences = TRUTHS[truth_name]
    print(f"\n  === {truth_name} ===")
    for text, lang in sentences[:4]:  # First 4 languages
        vecs, words = sentence_word_vectors(text)
        if len(vecs) < 3:
            print(f"    [{lang}] {text} — too short for D2")
            continue
        d2s = compute_curvatures(vecs)
        ops = [d2_to_operator(d)[1] for d in d2s]
        print(f"    [{lang:8s}] {text[:40]:40s} → D2 ops: {ops}")


# ═══════════════════════════════════════════════════════════
print(f"\n{'='*65}")
print(f"  ══════════════════════════════════════")
print(f"  FINAL VERDICT: Three Layers of Measurement")
print(f"  ══════════════════════════════════════")
print(f"{'='*65}")
print(f"""
  POSITION (Being) — cosine(v, v'):
    Within-truth:  {np.mean(within_pos):+.4f}
    Between-truth: {np.mean(between_pos):+.4f}
    Separation:    {np.mean(within_pos) - np.mean(between_pos):+.4f}
    
  TRANSITION (Doing) — cosine(Δv, Δv'):
    Within-truth:  {np.mean(within_trans):+.4f}
    Between-truth: {np.mean(between_trans):+.4f}
    Separation:    {np.mean(within_trans) - np.mean(between_trans):+.4f}

  CURVATURE (Becoming) — cosine(D2, D2'):
    Within-truth:  {np.mean(within_curv):+.4f}
    Between-truth: {np.mean(between_curv):+.4f}
    Separation:    {np.mean(within_curv) - np.mean(between_curv):+.4f}
""")
