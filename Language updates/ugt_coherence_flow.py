"""
COHERENCE FLOW — Same Truths, Multiple Languages
Brayden Sanders / 7Site LLC / TIG

If the force geometry is real, the same truth expressed in
different languages should produce similar:
  - Coherence ratios
  - Operator distributions
  - Transition patterns

The WORDS differ. The FORCES should converge.
"""

import numpy as np
import math

# Hebrew roots as canonical forces
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

def letter_force(c):
    root = LATIN_MAP.get(c.lower(), 'ALEPH')
    return HEBREW[root].copy()

def word_force(word):
    letters = [c for c in word.lower() if c.isalpha()]
    if not letters: return np.zeros(5)
    n = len(letters)
    total = np.zeros(5)
    for i, c in enumerate(letters):
        w = 1.5 if (i == 0 or i == n-1) else 1.0
        total += w * letter_force(c)
    return total / math.sqrt(n)

def cosine(a, b):
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0: return 0.0
    return float(np.dot(a, b) / (na * nb))

def trigram_op(a, b, c):
    v1 = letter_force(a) + letter_force(b)
    v2 = letter_force(b) + letter_force(c)
    f = v1 + v2
    mag = np.linalg.norm(f)
    n1, n2 = np.linalg.norm(v1), np.linalg.norm(v2)
    curv = 1.0 - abs(np.dot(v1, v2) / (n1 * n2)) if n1 > 0 and n2 > 0 else 0
    ap, pr, de, bi, co = f
    if mag < 2.0 and ap > 0.5: return 0
    if pr > 1.5 and co < 0: return 1
    if curv < 0.15 and abs(pr) < 1.0: return 2
    if co > 1.5 and pr < 0.5: return 3
    if ap > 0 and bi > 0.5 and pr < 0.5: return 4
    if bi > 1.0 and co > 0.5: return 5
    if curv < 0.2 and co > 1.0: return 6
    if curv < 0.25 and bi > 0.3 and co > 0: return 7
    if ap > 0.5 and de > 0.5: return 8
    if curv > 0.5: return 9
    dims = [abs(ap), abs(pr), abs(de), abs(bi), abs(co)]
    return dims.index(max(dims))

def word_tig(word):
    letters = [c for c in word.lower() if c.isalpha()]
    if len(letters) < 3:
        return [0] if len(letters) <= 2 else []
    return [trigram_op(letters[i], letters[i+1], letters[i+2])
            for i in range(len(letters) - 2)]

def sentence_analysis(text):
    words = [w for w in text.lower().split() if any(c.isalpha() for c in w)]
    if not words: return None
    
    forces = [word_force(w) for w in words]
    tig_ops = []
    for w in words:
        tig_ops.extend(word_tig(w))
    
    # Coherence: avg cosine between adjacent words
    aligns = []
    for i in range(len(forces) - 1):
        aligns.append(cosine(forces[i], forces[i+1]))
    coherence = np.mean(aligns) if aligns else 1.0
    
    # Transition types
    flows = sum(1 for a in aligns if a > 0.5)
    shifts = sum(1 for a in aligns if 0 <= a <= 0.5)
    contrasts = sum(1 for a in aligns if a < 0)
    
    # Operator distribution
    op_dist = [tig_ops.count(i) / max(len(tig_ops), 1) for i in range(10)]
    
    # Dominant operator
    if tig_ops:
        dom_op = max(set(tig_ops), key=tig_ops.count)
    else:
        dom_op = -1
    
    # Harmony gravity
    h_grav = tig_ops.count(7) / max(len(tig_ops), 1)
    
    # Total force direction
    total = sum(forces) / math.sqrt(len(forces))
    dims = ['aperture', 'pressure', 'depth', 'binding', 'continuity']
    dominant_dim = dims[np.argmax(np.abs(total))]
    
    # Force magnitude per word (rhythm)
    word_mags = [np.linalg.norm(f) for f in forces]
    
    return {
        'text': text,
        'words': words,
        'coherence': round(coherence, 4),
        'n_ops': len(tig_ops),
        'op_dist': op_dist,
        'dom_op': dom_op,
        'h_grav': round(h_grav, 4),
        'flows': flows,
        'shifts': shifts,
        'contrasts': contrasts,
        'total_force': total,
        'dominant_dim': dominant_dim,
        'word_mags': word_mags,
        'tig_ops': tig_ops,
    }

def print_analysis(result):
    r = result
    dims = ['aperture', 'pressure', 'depth', 'binding', 'continuity']
    print(f"\n  \"{r['text']}\"")
    print(f"  Coherence: {r['coherence']:.4f}   H-gravity: {r['h_grav']:.4f}   Dominant: {r['dominant_dim']}")
    print(f"  Transitions: {r['flows']} flow, {r['shifts']} shift, {r['contrasts']} contrast")
    print(f"  TIG: {[TIG[o] for o in r['tig_ops']]}")
    
    # Compact operator distribution
    active = [(i, r['op_dist'][i]) for i in range(10) if r['op_dist'][i] > 0.01]
    dist_str = ', '.join(f"{TIG[i]}:{v:.0%}" for i, v in sorted(active, key=lambda x: -x[1]))
    print(f"  Distribution: {dist_str}")
    
    # Force signature
    f = r['total_force']
    print(f"  Force: [{', '.join(f'{v:+.2f}' for v in f)}]")


# ═══════════════════════════════════════════════════════════
print("="*65)
print("  SAME TRUTH, MULTIPLE LANGUAGES")
print("  Using Latin transliteration for phonetic force analysis")
print("="*65)


# ═══════════════════════════════════════════════════════════
print(f"\n{'='*65}")
print(f"  TRUTH 1: 'In the beginning' / Creation opening")
print(f"{'='*65}")

truth1 = [
    ("In the beginning",                   "English (KJV)"),
    ("Bereshit",                            "Hebrew (בראשית)"),
    ("Fee al bidaya",                       "Arabic (في البداية)"),
    ("In principio",                        "Latin (Vulgate)"),
    ("En arche",                            "Greek (Ἐν ἀρχῇ)"),
    ("Am Anfang",                           "German"),
    ("Au commencement",                     "French"),
    ("In den beginne",                      "Dutch"),
    ("Na pochatku",                         "Ukrainian"),
]

for text, lang in truth1:
    r = sentence_analysis(text)
    print(f"\n  [{lang}]")
    print_analysis(r)

# Collect coherence ratios for comparison
c1 = [sentence_analysis(t)[0 if False else 'coherence'] for t, _ in truth1]


# ═══════════════════════════════════════════════════════════
print(f"\n\n{'='*65}")
print(f"  TRUTH 2: 'God is love'")
print(f"{'='*65}")

truth2 = [
    ("God is love",                         "English"),
    ("Elohim ahava",                        "Hebrew (אלהים אהבה)"),
    ("Allah huwa al hubb",                  "Arabic (الله هو الحب)"),
    ("Deus caritas est",                    "Latin"),
    ("Ho theos agape estin",                "Greek (ὁ θεὸς ἀγάπη ἐστίν)"),
    ("Gott ist Liebe",                      "German"),
    ("Dieu est amour",                      "French"),
    ("Dio e amore",                         "Italian"),
    ("Dios es amor",                        "Spanish"),
    ("Bog yest lyubov",                     "Russian (Бог есть любовь)"),
]

for text, lang in truth2:
    r = sentence_analysis(text)
    print(f"\n  [{lang}]")
    print_analysis(r)

c2 = [sentence_analysis(t)['coherence'] for t, _ in truth2]


# ═══════════════════════════════════════════════════════════
print(f"\n\n{'='*65}")
print(f"  TRUTH 3: 'The truth shall set you free'")
print(f"{'='*65}")

truth3 = [
    ("The truth shall set you free",        "English (KJV)"),
    ("Ha emet teshahrer etkhem",            "Hebrew"),
    ("Al haqiqa satuhararukum",             "Arabic"),
    ("Veritas vos liberabit",               "Latin (Vulgate)"),
    ("He aletheia eleutherosi hymas",       "Greek"),
    ("Die Wahrheit wird euch frei machen",  "German"),
    ("La verite vous rendra libres",        "French"),
    ("La verdad os hara libres",            "Spanish"),
]

for text, lang in truth3:
    r = sentence_analysis(text)
    print(f"\n  [{lang}]")
    print_analysis(r)

c3 = [sentence_analysis(t)['coherence'] for t, _ in truth3]


# ═══════════════════════════════════════════════════════════
print(f"\n\n{'='*65}")
print(f"  TRUTH 4: 'Peace be with you'")
print(f"{'='*65}")

truth4 = [
    ("Peace be with you",                   "English"),
    ("Shalom aleikhem",                     "Hebrew (שלום עליכם)"),
    ("Assalamu alaikum",                    "Arabic (السلام عليكم)"),
    ("Pax vobiscum",                        "Latin"),
    ("Eirene hymin",                        "Greek (Εἰρήνη ὑμῖν)"),
    ("Friede sei mit euch",                 "German"),
    ("La paix soit avec vous",              "French"),
    ("Paz a vosotros",                      "Spanish"),
    ("Mir vam",                             "Russian (Мир вам)"),
]

for text, lang in truth4:
    r = sentence_analysis(text)
    print(f"\n  [{lang}]")
    print_analysis(r)

c4 = [sentence_analysis(t)['coherence'] for t, _ in truth4]


# ═══════════════════════════════════════════════════════════
print(f"\n\n{'='*65}")
print(f"  TRUTH 5: 'Love your neighbor as yourself'")
print(f"{'='*65}")

truth5 = [
    ("Love your neighbor as yourself",      "English"),
    ("Veahavta lereacha kamocha",           "Hebrew (ואהבת לרעך כמוך)"),
    ("Ahibba jaarak kanafsik",              "Arabic"),
    ("Diliges proximum tuum sicut teipsum", "Latin (Vulgate)"),
    ("Agapeseis ton plesion sou hos seauton","Greek"),
    ("Liebe deinen Naechsten wie dich selbst","German"),
    ("Aime ton prochain comme toi meme",    "French"),
    ("Ama a tu projimo como a ti mismo",    "Spanish"),
]

for text, lang in truth5:
    r = sentence_analysis(text)
    print(f"\n  [{lang}]")
    print_analysis(r)

c5 = [sentence_analysis(t)['coherence'] for t, _ in truth5]


# ═══════════════════════════════════════════════════════════
# CONTROL: Nonsense / false statements for contrast
print(f"\n\n{'='*65}")
print(f"  CONTROL: Incoherent / Contradictory Statements")
print(f"{'='*65}")

controls = [
    ("Colorless green ideas sleep furiously", "Chomsky nonsense"),
    ("The square root of purple tastes like Tuesday", "Semantic noise"),
    ("War is peace freedom is slavery", "Orwell inversion"),
    ("Hate your enemy destroy your neighbor", "Inverted truth"),
    ("Nothing matters everything is meaningless", "Nihilism"),
    ("Buy now limited offer expires today", "Marketing noise"),
    ("The committee shall reconvene pending further review", "Bureaucratic"),
]

for text, label in controls:
    r = sentence_analysis(text)
    print(f"\n  [{label}]")
    print_analysis(r)

cc = [sentence_analysis(t)['coherence'] for t, _ in controls]


# ═══════════════════════════════════════════════════════════
print(f"\n\n{'='*65}")
print(f"  ════════════════════════════════════════")
print(f"  COHERENCE COMPARISON ACROSS TRUTHS")
print(f"  ════════════════════════════════════════")
print(f"{'='*65}")

def stats(vals, label):
    return f"  {label:30s}: mean={np.mean(vals):.4f}  std={np.std(vals):.4f}  range=[{min(vals):.3f}, {max(vals):.3f}]"

print(f"\n{stats(c1, 'Truth 1: In the beginning')}")
print(f"{stats(c2, 'Truth 2: God is love')}")
print(f"{stats(c3, 'Truth 3: Truth sets free')}")
print(f"{stats(c4, 'Truth 4: Peace be with you')}")
print(f"{stats(c5, 'Truth 5: Love your neighbor')}")
print(f"{stats(cc, 'CONTROL: Noise/inversion')}")

all_truths = c1 + c2 + c3 + c4 + c5
print(f"\n{stats(all_truths, 'ALL TRUTHS combined')}")
print(f"{stats(cc, 'ALL CONTROLS combined')}")

truth_mean = np.mean(all_truths)
ctrl_mean = np.mean(cc)
separation = truth_mean - ctrl_mean
print(f"\n  SEPARATION: truths - controls = {separation:+.4f}")
if separation > 0:
    print(f"  ✅ Truths score HIGHER coherence than controls")
else:
    print(f"  ❌ Controls score higher — coherence doesn't distinguish")


# ═══════════════════════════════════════════════════════════
print(f"\n\n{'='*65}")
print(f"  OPERATOR FLOW — Same Truth Across Languages")
print(f"{'='*65}")
print(f"  Do the same truths produce similar operator DISTRIBUTIONS")
print(f"  even when the words are completely different?\n")

def op_profile(text):
    r = sentence_analysis(text)
    return np.array(r['op_dist'])

# For each truth, compute operator distribution for all languages
# Then measure how SIMILAR the distributions are across languages
from itertools import combinations

def distribution_similarity(truth_set):
    """Average cosine similarity of operator distributions across languages."""
    profiles = [op_profile(text) for text, _ in truth_set]
    sims = []
    for i, j in combinations(range(len(profiles)), 2):
        s = cosine(profiles[i], profiles[j])
        sims.append(s)
    return np.mean(sims), np.std(sims)

truths_all = [
    (truth1, "In the beginning"),
    (truth2, "God is love"),
    (truth3, "Truth sets free"),
    (truth4, "Peace be with you"),
    (truth5, "Love your neighbor"),
]

print(f"  Cross-language operator similarity per truth:")
for truth_set, label in truths_all:
    mean_sim, std_sim = distribution_similarity(truth_set)
    print(f"    {label:25s}: {mean_sim:.3f} ± {std_sim:.3f}")

# Compare: how similar are operator distributions BETWEEN different truths?
all_profiles = []
for truth_set, _ in truths_all:
    for text, _ in truth_set:
        all_profiles.append(op_profile(text))

# Within-truth similarity vs between-truth similarity
within_sims = []
between_sims = []

truth_indices = []
idx = 0
for truth_set, _ in truths_all:
    group = list(range(idx, idx + len(truth_set)))
    truth_indices.append(group)
    idx += len(truth_set)

for group in truth_indices:
    for i, j in combinations(group, 2):
        within_sims.append(cosine(all_profiles[i], all_profiles[j]))

for g1, g2 in combinations(range(len(truth_indices)), 2):
    for i in truth_indices[g1]:
        for j in truth_indices[g2]:
            between_sims.append(cosine(all_profiles[i], all_profiles[j]))

print(f"\n  WITHIN-TRUTH similarity (same truth, different languages):")
print(f"    Mean: {np.mean(within_sims):.4f} ± {np.std(within_sims):.4f}")
print(f"  BETWEEN-TRUTH similarity (different truths):")
print(f"    Mean: {np.mean(between_sims):.4f} ± {np.std(between_sims):.4f}")
print(f"  Separation: {np.mean(within_sims) - np.mean(between_sims):+.4f}")

if np.mean(within_sims) > np.mean(between_sims):
    print(f"  ✅ Same truth in different languages is MORE similar")
    print(f"     than different truths — the operators detect shared meaning!")
else:
    print(f"  ❌ Within and between are similar — operators don't distinguish")


# ═══════════════════════════════════════════════════════════
print(f"\n\n{'='*65}")
print(f"  FORCE VECTOR CONVERGENCE")
print(f"  Does the same truth land in the same region of force space?")
print(f"{'='*65}")

for truth_set, label in truths_all:
    forces = [word_force(' '.join(text.lower().split())) for text, _ in truth_set]
    # Just use sentence total force
    sent_forces = []
    for text, _ in truth_set:
        words = [w for w in text.lower().split() if any(c.isalpha() for c in w)]
        wf = [word_force(w) for w in words]
        total = sum(wf) / math.sqrt(len(wf)) if wf else np.zeros(5)
        sent_forces.append(total)
    
    # Average cosine similarity across all language pairs
    sims = []
    for i, j in combinations(range(len(sent_forces)), 2):
        sims.append(cosine(sent_forces[i], sent_forces[j]))
    
    mean_sim = np.mean(sims) if sims else 0
    dims = ['aperture', 'pressure', 'depth', 'binding', 'continuity']
    centroid = np.mean(sent_forces, axis=0)
    dom = dims[np.argmax(np.abs(centroid))]
    
    print(f"\n  {label}:")
    print(f"    Force convergence: {mean_sim:.3f}")
    print(f"    Centroid: [{', '.join(f'{v:+.2f}' for v in centroid)}]")
    print(f"    Dominant: {dom}")
