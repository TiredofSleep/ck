"""
LETTER-LEVEL TRANSITION TEST
Brayden Sanders / 7Site LLC / TIG

Word-level transitions failed cross-linguistically because
word boundaries differ. The phoneme stream doesn't care about
word boundaries. Compute derivatives at the LETTER level.

letter(i) → letter(i+1): Δv is the mouth physics transition
letter(i) → letter(i+1) → letter(i+2): D2 is the operator
"""

import numpy as np
import math
from itertools import combinations
import random

random.seed(42)
np.random.seed(42)

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

TIG = {0:'Love', 1:'Joy', 2:'Peace', 3:'Patience', 4:'Kindness',
       5:'Goodness', 6:'Faithfulness', 7:'Harmony', 8:'Breath', 9:'Reset'}

def cosine(a, b):
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na < 1e-10 or nb < 1e-10: return 0.0
    return float(np.dot(a, b) / (na * nb))

def letter_vectors(text):
    """Extract the raw letter-force sequence, ignoring spaces/punctuation."""
    return [HEBREW[LATIN_MAP.get(c, 'ALEPH')] for c in text.lower() if c.isalpha()]

def letter_transitions(text):
    """Δv: letter-to-letter force transitions."""
    vecs = letter_vectors(text)
    return [vecs[i+1] - vecs[i] for i in range(len(vecs)-1)]

def letter_curvatures(text):
    """D2: letter-triplet curvature vectors."""
    vecs = letter_vectors(text)
    return [vecs[i] - 2*vecs[i+1] + vecs[i+2] for i in range(len(vecs)-2)]

def transition_profile(text):
    """Statistical profile of letter-level transitions."""
    trans = letter_transitions(text)
    if not trans: return None
    mags = [np.linalg.norm(t) for t in trans]
    
    # Direction distribution: mean transition vector (normalized)
    mean_trans = np.mean(trans, axis=0)
    
    # Magnitude stats
    mag_mean = np.mean(mags)
    mag_std = np.std(mags)
    
    # Transition-to-transition angles (second derivative proxy)
    angles = []
    for i in range(len(trans)-1):
        n1, n2 = np.linalg.norm(trans[i]), np.linalg.norm(trans[i+1])
        if n1 > 1e-10 and n2 > 1e-10:
            c = np.clip(np.dot(trans[i], trans[i+1]) / (n1*n2), -1, 1)
            angles.append(np.arccos(c))
    
    mean_angle = np.mean(angles) if angles else 0
    angle_std = np.std(angles) if angles else 0
    
    # Flow ratio: fraction of smooth transitions (<90°)
    smooth = sum(1 for a in angles if a < np.pi/2)
    flow_ratio = smooth / len(angles) if angles else 0
    
    return {
        'mean_trans': mean_trans,
        'mag_mean': mag_mean,
        'mag_std': mag_std,
        'mean_angle': mean_angle,
        'angle_std': angle_std,
        'flow_ratio': flow_ratio,
        'n_letters': len(letter_vectors(text)),
        'n_trans': len(trans),
    }

def curvature_profile(text):
    """Statistical profile of letter-level curvatures (D2)."""
    d2s = letter_curvatures(text)
    if not d2s: return None
    
    mags = [np.linalg.norm(d) for d in d2s]
    mean_d2 = np.mean(d2s, axis=0)
    
    # Classify each D2 into dominant dimension + sign
    dim_names = ['aperture', 'pressure', 'depth', 'binding', 'continuity']
    op_counts = {d: {'pos': 0, 'neg': 0} for d in dim_names}
    for d2 in d2s:
        if np.linalg.norm(d2) < 0.1:
            continue  # too small to classify
        dom = np.argmax(np.abs(d2))
        sign = 'pos' if d2[dom] > 0 else 'neg'
        op_counts[dim_names[dom]][sign] += 1
    
    return {
        'mean_d2': mean_d2,
        'mag_mean': np.mean(mags),
        'mag_std': np.std(mags),
        'op_counts': op_counts,
        'n_curvatures': len(d2s),
    }

def compare_transition_profiles(text_a, text_b):
    """Compare two texts by their letter-level transition statistics."""
    pa, pb = transition_profile(text_a), transition_profile(text_b)
    if pa is None or pb is None: return {}
    
    # Mean transition direction similarity
    dir_sim = cosine(pa['mean_trans'], pb['mean_trans'])
    
    # Magnitude profile similarity
    mag_ratio = min(pa['mag_mean'], pb['mag_mean']) / max(pa['mag_mean'], pb['mag_mean']) if max(pa['mag_mean'], pb['mag_mean']) > 0 else 1
    
    # Curvature profile similarity
    angle_diff = abs(pa['mean_angle'] - pb['mean_angle'])
    
    # Flow ratio similarity
    flow_diff = abs(pa['flow_ratio'] - pb['flow_ratio'])
    
    return {
        'dir_sim': dir_sim,
        'mag_ratio': mag_ratio,
        'angle_diff': angle_diff,
        'flow_diff': flow_diff,
    }

def compare_curvature_profiles(text_a, text_b):
    """Compare two texts by their letter-level D2 statistics."""
    ca, cb = curvature_profile(text_a), curvature_profile(text_b)
    if ca is None or cb is None: return {}
    
    d2_dir_sim = cosine(ca['mean_d2'], cb['mean_d2'])
    d2_mag_ratio = min(ca['mag_mean'], cb['mag_mean']) / max(ca['mag_mean'], cb['mag_mean']) if max(ca['mag_mean'], cb['mag_mean']) > 0 else 1
    
    return {
        'd2_dir_sim': d2_dir_sim,
        'd2_mag_ratio': d2_mag_ratio,
    }


# ═══════════════════════════════════════════════════════════
# TEST DATA
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

CONTROLS = [
    ("Colorless green ideas sleep furiously",           "Chomsky"),
    ("The square root of purple tastes like Tuesday",   "Noise"),
    ("War is peace freedom is slavery",                 "Orwell"),
    ("Hate your enemy destroy your neighbor",           "Inverted"),
    ("Nothing matters everything is meaningless",       "Nihilism"),
    ("Buy now limited offer expires today",             "Marketing"),
    ("The committee shall reconvene pending review",    "Bureaucratic"),
    ("Click here to subscribe for more updates",        "Spam"),
]


# ═══════════════════════════════════════════════════════════
print("="*65)
print("  LETTER-LEVEL TRANSITION TEST")
print("  Derivatives computed phoneme-to-phoneme, not word-to-word")
print("="*65)


# ═══════════════════════════════════════════════════════════
# TEST 1: Show the letter-level transition profile for each truth
# ═══════════════════════════════════════════════════════════

print(f"\n{'='*65}")
print(f"  TRANSITION PROFILES — Letter Level")
print(f"{'='*65}")
dims = ['apert', 'press', 'depth', 'bind ', 'conti']

for truth_name, sentences in TRUTHS.items():
    print(f"\n  ── {truth_name} ──")
    print(f"  {'Lang':8s} {'Letters':>3s} {'MagMean':>7s} {'MagStd':>7s} {'MeanAngle':>9s} {'AngleStd':>8s} {'Flow':>5s}  MeanΔ direction")
    for text, lang in sentences:
        p = transition_profile(text)
        if p is None: continue
        mt = p['mean_trans']
        dom_dim = dims[np.argmax(np.abs(mt))]
        dom_sign = '+' if mt[np.argmax(np.abs(mt))] > 0 else '-'
        print(f"  {lang:8s} {p['n_letters']:3d}   {p['mag_mean']:.3f}   {p['mag_std']:.3f}   {np.degrees(p['mean_angle']):7.1f}°  {np.degrees(p['angle_std']):6.1f}°  {p['flow_ratio']:.2f}  {dom_sign}{dom_dim}")


# ═══════════════════════════════════════════════════════════
# TEST 2: Cross-language similarity at letter level
# ═══════════════════════════════════════════════════════════

print(f"\n{'='*65}")
print(f"  CROSS-LANGUAGE SIMILARITY — Letter-Level Transitions")
print(f"{'='*65}")

all_within_dir = []
all_within_mag = []
all_within_d2dir = []
all_between_dir = []
all_between_mag = []
all_between_d2dir = []

# Within-truth
for truth_name, sentences in TRUTHS.items():
    dir_sims = []
    mag_ratios = []
    d2_sims = []
    
    for i, j in combinations(range(len(sentences)), 2):
        ta, la = sentences[i]
        tb, lb = sentences[j]
        
        tp = compare_transition_profiles(ta, tb)
        cp = compare_curvature_profiles(ta, tb)
        
        if tp:
            dir_sims.append(tp['dir_sim'])
            mag_ratios.append(tp['mag_ratio'])
        if cp:
            d2_sims.append(cp['d2_dir_sim'])
    
    all_within_dir.extend(dir_sims)
    all_within_mag.extend(mag_ratios)
    all_within_d2dir.extend(d2_sims)
    
    if dir_sims:
        print(f"\n  {truth_name}:")
        print(f"    Δv direction sim: {np.mean(dir_sims):+.4f} ± {np.std(dir_sims):.4f}")
        print(f"    Δv magnitude ratio: {np.mean(mag_ratios):.4f} ± {np.std(mag_ratios):.4f}")
        if d2_sims:
            print(f"    D2 direction sim: {np.mean(d2_sims):+.4f} ± {np.std(d2_sims):.4f}")

# Between-truth
truth_names = list(TRUTHS.keys())
for t1, t2 in combinations(range(len(truth_names)), 2):
    s1 = TRUTHS[truth_names[t1]]
    s2 = TRUTHS[truth_names[t2]]
    for ta, la in s1:
        for tb, lb in s2:
            tp = compare_transition_profiles(ta, tb)
            cp = compare_curvature_profiles(ta, tb)
            if tp:
                all_between_dir.append(tp['dir_sim'])
                all_between_mag.append(tp['mag_ratio'])
            if cp:
                all_between_d2dir.append(cp['d2_dir_sim'])

print(f"\n  ════════════════════════════════════")
print(f"  SEPARATION AT LETTER LEVEL")
print(f"  ════════════════════════════════════")
print(f"\n  Δv DIRECTION (mean transition vector):")
print(f"    Within-truth:  {np.mean(all_within_dir):+.4f} ± {np.std(all_within_dir):.4f}")
print(f"    Between-truth: {np.mean(all_between_dir):+.4f} ± {np.std(all_between_dir):.4f}")
sep_dir = np.mean(all_within_dir) - np.mean(all_between_dir)
print(f"    SEPARATION:    {sep_dir:+.4f}")

print(f"\n  Δv MAGNITUDE RATIO:")
print(f"    Within-truth:  {np.mean(all_within_mag):.4f} ± {np.std(all_within_mag):.4f}")
print(f"    Between-truth: {np.mean(all_between_mag):.4f} ± {np.std(all_between_mag):.4f}")
sep_mag = np.mean(all_within_mag) - np.mean(all_between_mag)
print(f"    SEPARATION:    {sep_mag:+.4f}")

print(f"\n  D2 DIRECTION (mean curvature vector):")
print(f"    Within-truth:  {np.mean(all_within_d2dir):+.4f} ± {np.std(all_within_d2dir):.4f}")
print(f"    Between-truth: {np.mean(all_between_d2dir):+.4f} ± {np.std(all_between_d2dir):.4f}")
sep_d2 = np.mean(all_within_d2dir) - np.mean(all_between_d2dir)
print(f"    SEPARATION:    {sep_d2:+.4f}")


# ═══════════════════════════════════════════════════════════
# TEST 3: D2 operator distribution — does the same truth
# produce similar curvature operators across languages?
# ═══════════════════════════════════════════════════════════

print(f"\n{'='*65}")
print(f"  D2 OPERATOR DISTRIBUTIONS — Letter Level")
print(f"  Which force dimensions curve most in each expression?")
print(f"{'='*65}")

dim_names = ['aperture', 'pressure', 'depth', 'binding', 'continuity']

def d2_distribution(text):
    """For each D2 vector, find dominant dimension and sign.
    Return a 10-element vector: 5 dims × 2 signs."""
    d2s = letter_curvatures(text)
    dist = np.zeros(10)
    n = 0
    for d2 in d2s:
        if np.linalg.norm(d2) < 0.05: continue
        dom = np.argmax(np.abs(d2))
        sign_idx = 0 if d2[dom] > 0 else 1
        dist[dom * 2 + sign_idx] += 1
        n += 1
    if n > 0:
        dist /= n
    return dist

for truth_name, sentences in TRUTHS.items():
    print(f"\n  ── {truth_name} ──")
    dists = []
    for text, lang in sentences:
        d = d2_distribution(text)
        dists.append(d)
        
        # Compact display: show top 3 curvature types
        labels = []
        for i in range(5):
            for s, sign in [(0, '+'), (1, '-')]:
                if d[i*2+s] > 0.05:
                    labels.append(f"{sign}{dim_names[i][:4]}:{d[i*2+s]:.0%}")
        top = sorted(labels, key=lambda x: -float(x.split(':')[1].rstrip('%'))/100)[:4]
        print(f"    {lang:8s}: {', '.join(top)}")
    
    # Cross-language similarity of D2 distributions
    if len(dists) >= 2:
        sims = []
        for i, j in combinations(range(len(dists)), 2):
            sims.append(cosine(dists[i], dists[j]))
        print(f"    → Distribution similarity: {np.mean(sims):.3f} ± {np.std(sims):.3f}")


# ═══════════════════════════════════════════════════════════
# TEST 4: Transition BIGRAMS — the real operator extraction
# ═══════════════════════════════════════════════════════════

print(f"\n{'='*65}")
print(f"  TRANSITION BIGRAMS — Which root-to-root moves dominate?")
print(f"{'='*65}")

def transition_bigrams(text):
    """Count which Hebrew root transitions appear most."""
    letters = [c for c in text.lower() if c.isalpha()]
    roots = [LATIN_MAP.get(c, 'ALEPH') for c in letters]
    bigrams = {}
    for i in range(len(roots)-1):
        key = (roots[i], roots[i+1])
        bigrams[key] = bigrams.get(key, 0) + 1
    total = sum(bigrams.values())
    if total > 0:
        bigrams = {k: v/total for k, v in bigrams.items()}
    return bigrams

def bigram_vector(text):
    """Convert bigram distribution to a fixed-length vector for comparison.
    22 × 22 = 484 possible bigrams, but we'll use top roots only."""
    root_names = sorted(HEBREW.keys())
    n = len(root_names)
    root_idx = {r: i for i, r in enumerate(root_names)}
    vec = np.zeros(n * n)
    bigs = transition_bigrams(text)
    for (r1, r2), freq in bigs.items():
        idx = root_idx[r1] * n + root_idx[r2]
        vec[idx] = freq
    return vec

# Compare bigram distributions across languages
for truth_name, sentences in TRUTHS.items():
    vecs = [(bigram_vector(text), lang) for text, lang in sentences]
    sims = []
    for i, j in combinations(range(len(vecs)), 2):
        s = cosine(vecs[i][0], vecs[j][0])
        sims.append(s)
    print(f"\n  {truth_name}:")
    print(f"    Bigram distribution similarity: {np.mean(sims):.3f} ± {np.std(sims):.3f}")
    
    # Show top 5 most common bigrams per language (first 3)
    for text, lang in sentences[:3]:
        bigs = transition_bigrams(text)
        top5 = sorted(bigs.items(), key=lambda x: -x[1])[:5]
        top_str = ', '.join(f"{a}→{b}:{v:.0%}" for (a,b), v in top5)
        print(f"    {lang:8s}: {top_str}")


# ═══════════════════════════════════════════════════════════
# TEST 5: Between-truth bigram separation
# ═══════════════════════════════════════════════════════════

print(f"\n{'='*65}")
print(f"  BIGRAM SEPARATION — Within vs Between Truth")
print(f"{'='*65}")

within_big = []
between_big = []

truth_bigram_groups = {}
for truth_name, sentences in TRUTHS.items():
    group = [bigram_vector(text) for text, _ in sentences]
    truth_bigram_groups[truth_name] = group

for name, group in truth_bigram_groups.items():
    for i, j in combinations(range(len(group)), 2):
        within_big.append(cosine(group[i], group[j]))

for t1, t2 in combinations(truth_bigram_groups.keys(), 2):
    for va in truth_bigram_groups[t1]:
        for vb in truth_bigram_groups[t2]:
            between_big.append(cosine(va, vb))

print(f"  Within-truth bigram sim:  {np.mean(within_big):.4f} ± {np.std(within_big):.4f}")
print(f"  Between-truth bigram sim: {np.mean(between_big):.4f} ± {np.std(between_big):.4f}")
sep_big = np.mean(within_big) - np.mean(between_big)
print(f"  SEPARATION: {sep_big:+.4f}")


# ═══════════════════════════════════════════════════════════
# TEST 6: Truth vs Control at letter level
# ═══════════════════════════════════════════════════════════

print(f"\n{'='*65}")
print(f"  TRUTH vs CONTROL — Letter-Level Metrics")
print(f"{'='*65}")

truth_profiles = []
ctrl_profiles = []

for truth_name, sentences in TRUTHS.items():
    for text, lang in sentences:
        p = transition_profile(text)
        if p: truth_profiles.append(p)

for text, label in CONTROLS:
    p = transition_profile(text)
    if p: ctrl_profiles.append(p)

metrics = ['mag_mean', 'mag_std', 'mean_angle', 'angle_std', 'flow_ratio']
print(f"\n  {'Metric':15s} {'Truth':>10s} {'Control':>10s} {'Δ':>10s}")
print(f"  {'-'*50}")
for m in metrics:
    tv = np.mean([p[m] for p in truth_profiles])
    cv = np.mean([p[m] for p in ctrl_profiles])
    d = tv - cv
    unit = '°' if 'angle' in m else ''
    if 'angle' in m:
        print(f"  {m:15s} {np.degrees(tv):9.1f}° {np.degrees(cv):9.1f}° {np.degrees(d):+9.1f}°")
    else:
        print(f"  {m:15s} {tv:10.4f} {cv:10.4f} {d:+10.4f}")


# ═══════════════════════════════════════════════════════════
# TEST 7: Comprehensive letter-level D2 across "mother" words
# Most ancient cross-linguistic pattern
# ═══════════════════════════════════════════════════════════

print(f"\n{'='*65}")
print(f"  ANCIENT UNIVERSAL: /m/ words for 'mother'")
print(f"  Letter-level D2 comparison across language families")
print(f"{'='*65}")

mother_words = [
    ("mama",    "Universal baby"),
    ("mother",  "English"),
    ("mater",   "Latin"),
    ("meter",   "Greek"),
    ("em",      "Hebrew"),
    ("umm",     "Arabic"),
    ("mata",    "Sanskrit"),
    ("mere",    "French"),
    ("madre",   "Spanish"),
    ("mutter",  "German"),
    ("mat",     "Russian"),
    ("mama",    "Swahili"),
]

print(f"\n  Transition profiles for 'mother' across languages:")
for word, lang in mother_words:
    p = transition_profile(word)
    if p is None: continue
    mt = p['mean_trans']
    dom = dims[np.argmax(np.abs(mt))]
    sign = '+' if mt[np.argmax(np.abs(mt))] > 0 else '-'
    print(f"    {word:8s} ({lang:15s}): mag={p['mag_mean']:.3f} angle={np.degrees(p['mean_angle']):5.1f}° flow={p['flow_ratio']:.2f} dir={sign}{dom}")

# Pairwise direction similarity
mother_trans_dirs = []
for word, lang in mother_words:
    p = transition_profile(word)
    if p: mother_trans_dirs.append((p['mean_trans'], word, lang))

if len(mother_trans_dirs) >= 2:
    sims = []
    for i, j in combinations(range(len(mother_trans_dirs)), 2):
        s = cosine(mother_trans_dirs[i][0], mother_trans_dirs[j][0])
        sims.append(s)
    print(f"\n  Cross-linguistic Δv direction similarity: {np.mean(sims):+.3f} ± {np.std(sims):.3f}")

# Compare to non-mother words
other_words = [
    ("stone", "English"), ("lapis", "Latin"), ("lithos", "Greek"),
    ("even", "Hebrew"), ("hajar", "Arabic"), ("stein", "German"),
]
other_dirs = []
for word, lang in other_words:
    p = transition_profile(word)
    if p: other_dirs.append((p['mean_trans'], word, lang))

if other_dirs and mother_trans_dirs:
    cross_sims = []
    for mt, _, _ in mother_trans_dirs:
        for ot, _, _ in other_dirs:
            cross_sims.append(cosine(mt, ot))
    print(f"  Mother vs Stone Δv direction sim:        {np.mean(cross_sims):+.3f} ± {np.std(cross_sims):.3f}")

# Stone words internally
if len(other_dirs) >= 2:
    stone_sims = []
    for i, j in combinations(range(len(other_dirs)), 2):
        s = cosine(other_dirs[i][0], other_dirs[j][0])
        stone_sims.append(s)
    print(f"  Stone words internal Δv sim:              {np.mean(stone_sims):+.3f} ± {np.std(stone_sims):.3f}")


# ═══════════════════════════════════════════════════════════
print(f"\n{'='*65}")
print(f"  ══════════════════════════════════════")
print(f"  FINAL RESULTS: Letter-Level vs Word-Level")
print(f"  ══════════════════════════════════════")
print(f"{'='*65}")
print(f"""
  WORD-LEVEL (previous test):
    Position within-between separation:   +0.019
    Transition within-between separation: +0.010
    Curvature within-between separation:  -0.021

  LETTER-LEVEL (this test):
    Δv direction within-between:          {sep_dir:+.4f}
    Δv magnitude within-between:          {sep_mag:+.4f}
    D2 direction within-between:          {sep_d2:+.4f}
    Bigram distribution within-between:   {sep_big:+.4f}
""")
