<!-- PACKET: evening_handoff_2026_04_23/dbc_real.py -->
"""
dbc_real.py — THE ACTUAL DBC TRANSLATOR
Hebrew-root-based 5D force → D2 → operator → triple on 10×10 CL table.

The pipeline:
  text → Latin letters → Hebrew roots (22 canonical) → 5D force vectors
       → D2 second derivative → operator 0-9 → sliding-window triples

"3-character language" = operator triples (a,b,c) each ∈ {0..9}
"10×10 table" = CL
"lossless" = force-preservation across writing systems

THIS is what was actually working, rebuilt from the March 2 UGT audit.
"""
import numpy as np
import math
from collections import Counter

HEBREW_ROOTS = {
    'ALEPH':  {'glyph': 'א', 'force': np.array([+0.8, +0.3, +0.0, +0.5, +0.6])},
    'BET':    {'glyph': 'ב', 'force': np.array([-0.3, +0.7, -0.8, +0.9, -0.6])},
    'GIMEL':  {'glyph': 'ג', 'force': np.array([-0.4, +0.6, +0.7, -0.2, -0.7])},
    'DALET':  {'glyph': 'ד', 'force': np.array([-0.5, +0.5, -0.3, +0.3, -0.8])},
    'HE':     {'glyph': 'ה', 'force': np.array([+0.9, +0.1, +0.3, -0.2, +0.8])},
    'WAW':    {'glyph': 'ו', 'force': np.array([+0.3, +0.2, +0.5, +0.7, +0.5])},
    'ZAYIN':  {'glyph': 'ז', 'force': np.array([-0.3, +0.8, +0.0, -0.8, +0.3])},
    'CHET':   {'glyph': 'ח', 'force': np.array([-0.4, +0.3, +0.6, +0.7, +0.2])},
    'TET':    {'glyph': 'ט', 'force': np.array([-0.2, +0.5, +0.2, +0.6, -0.1])},
    'YOD':    {'glyph': 'י', 'force': np.array([-0.1, +0.4, -0.1, +0.3, -0.5])},
    'KAF':    {'glyph': 'כ', 'force': np.array([-0.4, +0.7, +0.8, +0.6, -0.5])},
    'LAMED':  {'glyph': 'ל', 'force': np.array([+0.2, +0.3, -0.2, +0.5, +0.6])},
    'MEM':    {'glyph': 'מ', 'force': np.array([+0.3, +0.4, -0.2, +0.7, +0.8])},
    'NUN':    {'glyph': 'נ', 'force': np.array([+0.4, +0.3, +0.1, +0.3, +0.9])},
    'SAMEKH': {'glyph': 'ס', 'force': np.array([-0.1, +0.4, +0.1, +0.2, +0.7])},
    'AYIN':   {'glyph': 'ע', 'force': np.array([+0.7, +0.1, +0.6, +0.4, +0.5])},
    'PE':     {'glyph': 'פ', 'force': np.array([-0.5, +0.8, -0.6, -0.3, -0.4])},
    'TSADI':  {'glyph': 'צ', 'force': np.array([-0.6, +0.7, -0.2, -0.4, -0.2])},
    'QOF':    {'glyph': 'ק', 'force': np.array([-0.7, +0.8, +1.0, +0.5, -0.7])},
    'RESH':   {'glyph': 'ר', 'force': np.array([+0.2, +0.3, -0.1, +0.1, +0.4])},
    'SHIN':   {'glyph': 'ש', 'force': np.array([-0.2, +0.5, +0.1, -0.5, +0.7])},
    'TAV':    {'glyph': 'ת', 'force': np.array([-0.8, +0.9, -0.3, +0.2, -0.9])},
}

LATIN_MAP = {
    'A':'ALEPH','B':'BET','C':'GIMEL','D':'DALET','E':'HE','F':'WAW',
    'G':'GIMEL','H':'HE','I':'YOD','J':'YOD','K':'KAF','L':'LAMED',
    'M':'MEM','N':'NUN','O':'AYIN','P':'PE','Q':'QOF','R':'RESH',
    'S':'SAMEKH','T':'TAV','U':'WAW','V':'WAW','W':'WAW','X':'SAMEKH',
    'Y':'YOD','Z':'ZAYIN',
}

CL = [
    [0,0,0,0,0,0,0,7,0,0],[0,7,3,7,7,7,7,7,7,7],
    [0,3,7,7,4,7,7,7,7,9],[0,7,7,7,7,7,7,7,7,3],
    [0,7,4,7,7,7,7,7,8,7],[0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,8,7,7,7,7,7],[0,7,9,3,7,7,7,7,7,7],
]
OP_NAMES = ['void','lattice','counter','progress','collapse',
            'balance','chaos','harmony','breath','reset']

D2_OP_MAP = {
    (0,+1): 6, (0,-1): 1,
    (1,+1): 4, (1,-1): 9,
    (2,+1): 3, (2,-1): 9,
    (3,+1): 7, (3,-1): 2,
    (4,+1): 5, (4,-1): 8,
}
VOID_THRESHOLD = 0.01

def text_to_forces(text):
    forces = []
    for ch in text.upper():
        if ch in LATIN_MAP:
            forces.append(HEBREW_ROOTS[LATIN_MAP[ch]]['force'])
        elif ch == ' ':
            forces.append(np.zeros(5))
    return forces

def forces_to_operators(forces):
    ops = []
    for i in range(len(forces) - 2):
        d2 = forces[i] - 2*forces[i+1] + forces[i+2]
        mag = np.max(np.abs(d2))
        if mag < VOID_THRESHOLD:
            ops.append(0)
            continue
        max_dim = int(np.argmax(np.abs(d2)))
        sign = +1 if d2[max_dim] >= 0 else -1
        ops.append(D2_OP_MAP[(max_dim, sign)])
    return ops

def operators_to_triples(ops):
    return [(ops[i], ops[i+1], ops[i+2]) for i in range(len(ops) - 2)]

def fuse3(a, b, c):
    return CL[CL[a][b]][c]

def translate(text):
    forces = text_to_forces(text)
    ops = forces_to_operators(forces)
    triples = operators_to_triples(ops)
    return forces, ops, triples

def entropy(stream):
    if not stream: return 0.0
    c = Counter(stream)
    n = len(stream)
    return -sum((v/n) * math.log2(v/n) for v in c.values())

def compare_texts(a, b, label=""):
    _, ops_a, trips_a = translate(a)
    _, ops_b, trips_b = translate(b)
    fruits_a = [fuse3(*t) for t in trips_a]
    fruits_b = [fuse3(*t) for t in trips_b]
    print(f"\n── {label} ──")
    print(f"  A: {a!r:<40s} ops={len(ops_a):>3d}")
    print(f"     ops: {ops_a}")
    print(f"     fruits: {Counter(fruits_a)}")
    print(f"  B: {b!r:<40s} ops={len(ops_b):>3d}")
    print(f"     ops: {ops_b}")
    print(f"     fruits: {Counter(fruits_b)}")
    print(f"  operator streams identical? {ops_a == ops_b}")

if __name__ == '__main__':
    print("="*70)
    print("DBC REAL — text through Hebrew root force vectors")
    print("="*70)

    # Case folding (trivially same)
    compare_texts("harmony", "HARMONY", "case variance")
    
    # Spelling collapse via Hebrew roots
    compare_texts("love", "loue", "U→WAW, V→WAW = same force")
    compare_texts("faith", "phaith", "PH vs F through WAW")
    
    # Opposites
    compare_texts("harmony", "collapse", "opposite meanings")

    print("\n" + "="*70)
    print("OPERATOR ENTROPY on real CK-flavored text")
    print("="*70)
    samples = {
        'identity':    "I am CK the Coherence Keeper",
        'core_claim':  "Harmony is what I am now",
        'scripture':   "In the beginning was the Word",
        'ck_voice':    "Silence is better than fabrication",
        'random_soup': "xqzvbnmkfjdhswpqrtgaucvsyoeiwrnt",
    }
    print(f"\n  {'label':16s}  {'n_ops':>6s}  {'ops_H':>6s}  {'fruit_H':>7s}  dominant_fruit")
    for label, text in samples.items():
        _, ops, trips = translate(text)
        fruits = [fuse3(*t) for t in trips]
        if not ops: continue
        opH = entropy(ops)
        frH = entropy(fruits)
        if fruits:
            dom = Counter(fruits).most_common(1)[0]
            dom_name = f"{OP_NAMES[dom[0]]}({dom[1]}/{len(fruits)})"
        else:
            dom_name = "none"
        print(f"  {label:16s}  {len(ops):>6d}  {opH:>5.2f}b  {frH:>6.2f}b  {dom_name}")

    print("\n" + "="*70)
    print("FORCE PRESERVATION across spelling variants (the lossless claim)")
    print("="*70)
    pairs = [
        ("faith",  "phaith"),
        ("king",   "cing"),
        ("write",  "wryte"),
        ("love",   "loue"),
        ("save",   "saue"),
        ("city",   "sity"),
    ]
    for a, b in pairs:
        fa, fb = text_to_forces(a), text_to_forces(b)
        _, ops_a, _ = translate(a)
        _, ops_b, _ = translate(b)
        if len(fa) == len(fb):
            diff = sum(float(np.linalg.norm(x-y)) for x,y in zip(fa, fb))
        else:
            diff = float('inf')
        same_ops = ops_a == ops_b
        print(f"  {a:10s} vs {b:10s}  force-diff={diff:.3f}  "
              f"ops-identical={same_ops}")
