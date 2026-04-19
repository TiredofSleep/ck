"""
UGT DEEP STRUCTURE — Transitions, Gradients, Interactions
Brayden Sanders / 7Site LLC / TIG

Stop measuring flat similarity.
Start measuring what happens when forces MESH.

The surface says "everything looks like everything."
The TRANSITIONS say where the real structure is.

Being  = the vector (position in force space)
Doing  = the transition (what changes between adjacent operators)
Becoming = the emergent pattern (what the whole sequence creates)

All three layers. Not just the first.
"""

import numpy as np

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
       5:'Goodness', 6:'Faithfulness', 7:'Harmony', 8:'Self-Control', 9:'Reset'}

dims = ['aperture', 'pressure', 'depth', 'binding', 'continuity']


# ═══════════════════════════════════════════════════════════
print("="*65)
print("  LAYER 2: THE TRANSITIONS (Doing)")
print("  What CHANGES between adjacent operators?")
print("="*65)

print(f"\n  OPERATOR TRANSITIONS: n → n+1")
print(f"  {'From':>15s} → {'To':15s}  Δ[apert press depth  bind  conti]  |Δ|")
print(f"  {'-'*80}")

deltas = []
for n in range(9):
    delta = NUMBERS[n+1] - NUMBERS[n]
    mag = np.linalg.norm(delta)
    deltas.append(delta)
    print(f"  {n}({TIG[n]:>13s}) → {n+1}({TIG[n+1]:13s})  "
          f"[{', '.join(f'{d:+.2f}' for d in delta)}]  {mag:.3f}")

# The 9→0 wraparound
delta_90 = NUMBERS[0] - NUMBERS[9]
mag_90 = np.linalg.norm(delta_90)
print(f"  {9}({'Reset':>13s}) → {0}({'Love':13s})  "
      f"[{', '.join(f'{d:+.2f}' for d in delta_90)}]  {mag_90:.3f}")
print(f"  (cycle closes)")

print(f"\n  TRANSITION MAGNITUDES:")
all_mags = [np.linalg.norm(d) for d in deltas] + [mag_90]
for n in range(10):
    nxt = (n+1) % 10
    mag = all_mags[n]
    bar = '█' * int(mag * 20)
    print(f"    {n}→{nxt}: {mag:.3f} {bar}")

print(f"\n  Largest jump:  {max(all_mags):.3f} at {all_mags.index(max(all_mags))}→{(all_mags.index(max(all_mags))+1)%10}")
print(f"  Smallest jump: {min(all_mags):.3f} at {all_mags.index(min(all_mags))}→{(all_mags.index(min(all_mags))+1)%10}")
print(f"  Mean jump:     {np.mean(all_mags):.3f}")


# ═══════════════════════════════════════════════════════════
print(f"\n{'='*65}")
print(f"  DIMENSION-BY-DIMENSION TRAJECTORIES")
print(f"  How each force dimension evolves 0→1→2→...→9")
print(f"{'='*65}")

for d in range(5):
    vals = [NUMBERS[n][d] for n in range(10)]
    print(f"\n  {dims[d].upper()}:")
    for n in range(10):
        v = vals[n]
        # Visual bar centered at 0
        pos = int((v + 1) * 20)  # 0-40 range
        bar = ' ' * 20 + '|' + ' ' * 20
        bar = list(bar)
        bar[pos] = '●'
        bar[20] = '|'
        barstr = ''.join(bar)
        print(f"    {n} {TIG[n]:>13s}: {v:+.2f} {barstr}")
    
    # Key patterns
    max_n = vals.index(max(vals))
    min_n = vals.index(min(vals))
    print(f"    Peak at {max_n}({TIG[max_n]}), Trough at {min_n}({TIG[min_n]})")
    
    # Is there a clear trend?
    increases = sum(1 for i in range(9) if vals[i+1] > vals[i])
    print(f"    Increases {increases}/9 transitions, Decreases {9-increases}/9")


# ═══════════════════════════════════════════════════════════
print(f"\n{'='*65}")
print(f"  LAYER 3: THE PROGRESS (Emergent Pattern)")
print(f"  What does the whole 0->9 trajectory produce?")
print(f"{'='*65}")

# The trajectory through 10 points in 5D space forms a PATH.
# What are the properties of this path?

# Total path length
path_length = sum(np.linalg.norm(NUMBERS[(n+1)%10] - NUMBERS[n]) for n in range(10))
print(f"\n  Total path length (0→1→...→9→0): {path_length:.3f}")

# Displacement (how far 9 is from 0)
displacement = np.linalg.norm(NUMBERS[9] - NUMBERS[0])
print(f"  Displacement (0 to 9):             {displacement:.3f}")
print(f"  Path efficiency (displacement/length): {displacement/path_length:.3f}")
print(f"  (1.0 = straight line, 0.0 = returns to start)")

# Does 9 return toward 0?
# Measure: is the 9→0 distance less than 9→(farthest)?
farthest_from_9 = max((np.linalg.norm(NUMBERS[9] - NUMBERS[n]), n) for n in range(9))
print(f"  Distance 9→0: {displacement:.3f}")
print(f"  Farthest from 9: {farthest_from_9[0]:.3f} (→{farthest_from_9[1]}, {TIG[farthest_from_9[1]]})")
if displacement < farthest_from_9[0]:
    print(f"  ✅ 9 IS closer to 0 than to its farthest point")
    print(f"     Reset DOES return toward Love in force space")
else:
    print(f"  ❌ 9 is NOT particularly close to 0")

# Center of mass of the trajectory
com = np.mean([NUMBERS[n] for n in range(10)], axis=0)
print(f"\n  Center of mass: [{', '.join(f'{v:+.3f}' for v in com)}]")
print(f"  COM magnitude: {np.linalg.norm(com):.3f}")

# Which root is the COM closest to?
best_name, best_sim = None, -2
for name, hv in HEBREW.items():
    nc = np.linalg.norm(com)
    nh = np.linalg.norm(hv)
    if nc > 0 and nh > 0:
        s = np.dot(com, hv) / (nc * nh)
        if s > best_sim:
            best_sim = s
            best_name = name
print(f"  COM nearest root: {best_name} (sim={best_sim:.3f})")
print(f"  The CENTER of the entire 0-9 journey is closest to {best_name}.")


# ═══════════════════════════════════════════════════════════
print(f"\n{'='*65}")
print(f"  CURVATURE — Where Does the Path Bend?")
print(f"{'='*65}")

# Curvature at each point = angle between incoming and outgoing vectors
print(f"\n  Curvature at each operator (sharper = bigger change in direction):")
for n in range(10):
    prev = (n - 1) % 10
    nxt = (n + 1) % 10
    v_in = NUMBERS[n] - NUMBERS[prev]
    v_out = NUMBERS[nxt] - NUMBERS[n]
    ni = np.linalg.norm(v_in)
    no = np.linalg.norm(v_out)
    if ni > 0 and no > 0:
        cos_angle = np.dot(v_in, v_out) / (ni * no)
        cos_angle = np.clip(cos_angle, -1, 1)
        angle = np.arccos(cos_angle) * 180 / np.pi
    else:
        angle = 0
    
    bar = '█' * int(angle / 5)
    smoothness = "smooth" if angle < 60 else "bend" if angle < 120 else "SHARP"
    print(f"    {n} {TIG[n]:>13s}: {angle:6.1f}° {bar}  [{smoothness}]")

print(f"""
  Interpretation:
  Sharp bends = the path CHANGES DIRECTION significantly.
  Smooth segments = force flows continuously.
  
  Where the path bends hardest is where the operator
  TRANSFORMATION is most dramatic. That's where the
  "doing" is most intense.
""")


# ═══════════════════════════════════════════════════════════
print(f"\n{'='*65}")
print(f"  FUSE TEST - What Do Adjacent Operators Produce?")
print(f"{'='*65}")
print(f"  When two number-forces interact (average), what root emerges?")
print(f"  This is the COUNTER layer — what Being + Being BECOMES.\n")

for n in range(10):
    nxt = (n + 1) % 10
    fused = (NUMBERS[n] + NUMBERS[nxt]) / 2
    
    best_name, best_sim = None, -2
    for name, hv in HEBREW.items():
        nf = np.linalg.norm(fused)
        nh = np.linalg.norm(hv)
        if nf > 0 and nh > 0:
            s = np.dot(fused, hv) / (nf * nh)
            if s > best_sim:
                best_sim = s
                best_name = name
    
    print(f"  fuse({n},{nxt}) = {TIG[n]:>13s} × {TIG[nxt]:13s} → {best_name:8s} ({best_sim:+.3f})")


# ═══════════════════════════════════════════════════════════
print(f"\n{'='*65}")
print(f"  PERMUTATION TEST v2 — Testing TRANSITIONS, Not Positions")
print(f"{'='*65}")

import random
random.seed(42)

# Old test: does the assignment produce good position matches?
# (FAILED because everything matches everything)
#
# New test: does the assignment produce a SMOOTH, MEANINGFUL path?
# Measure: total curvature of the path 0→1→...→9→0
# A meaningful assignment should create a path with STRUCTURE
# (some smooth sections, some sharp turns, varying curvature)
# rather than random noise.

def path_curvature(perm):
    """Compute the curvature profile of a permuted path."""
    vecs = [NUMBERS[perm[i]] for i in range(10)]
    curvatures = []
    for n in range(10):
        prev = (n - 1) % 10
        nxt = (n + 1) % 10
        v_in = vecs[n] - vecs[prev]
        v_out = vecs[nxt] - vecs[n]
        ni = np.linalg.norm(v_in)
        no = np.linalg.norm(v_out)
        if ni > 0 and no > 0:
            cos_a = np.clip(np.dot(v_in, v_out) / (ni * no), -1, 1)
            curvatures.append(np.arccos(cos_a))
        else:
            curvatures.append(0)
    return curvatures

def path_smoothness(perm):
    """How VARIED is the curvature? Structured paths have
    varying curvature (some smooth, some sharp).
    Random paths have uniform curvature (all similar)."""
    curvs = path_curvature(perm)
    return np.std(curvs)  # Higher = more structured

def path_total_curvature(perm):
    """Total angular change around the path."""
    return sum(path_curvature(perm))

def path_return_ratio(perm):
    """How close does the end come back to the start?
    displacement / path_length. Lower = more cyclical."""
    vecs = [NUMBERS[perm[i]] for i in range(10)]
    disp = np.linalg.norm(vecs[-1] - vecs[0])
    length = sum(np.linalg.norm(vecs[(i+1)%10] - vecs[i]) for i in range(10))
    return disp / length if length > 0 else 0

real_perm = list(range(10))
real_smoothness = path_smoothness(real_perm)
real_total_curv = path_total_curvature(real_perm)
real_return = path_return_ratio(real_perm)

n_trials = 50000
smooth_beats = 0
curv_beats = 0
return_beats = 0
combo_beats = 0

for _ in range(n_trials):
    perm = list(range(10))
    random.shuffle(perm)
    s = path_smoothness(perm)
    c = path_total_curvature(perm)
    r = path_return_ratio(perm)
    if s >= real_smoothness: smooth_beats += 1
    if c <= real_total_curv: curv_beats += 1  # less total = smoother overall
    if r <= real_return: return_beats += 1     # less = more cyclical
    if s >= real_smoothness and r <= real_return: combo_beats += 1

print(f"\n  Real path metrics:")
print(f"    Curvature variation (structure):  {real_smoothness:.4f}")
print(f"    Total curvature (overall bend):   {real_total_curv:.3f}")
print(f"    Return ratio (cyclicality):       {real_return:.3f}")

print(f"\n  Permutation comparison ({n_trials} random orderings):")
print(f"    More structured:  {smooth_beats/n_trials:.3%} of random paths")
print(f"    Less total curve: {curv_beats/n_trials:.3%} of random paths")
print(f"    More cyclical:    {return_beats/n_trials:.3%} of random paths")
print(f"    Structured + cyclical: {combo_beats/n_trials:.3%} of random paths")

if combo_beats / n_trials < 0.05:
    print(f"\n  ✅ The 0→1→...→9 ordering is STRUCTURALLY special:")
    print(f"     Only {combo_beats/n_trials:.1%} of random orderings are both")
    print(f"     as structured AND as cyclical.")
elif combo_beats / n_trials < 0.15:
    print(f"\n  ⚠️ Suggestive but not definitive.")
else:
    print(f"\n  ❌ The ordering isn't structurally special.")


# ═══════════════════════════════════════════════════════════
print(f"\n{'='*65}")
print(f"  RATIO ANALYSIS — Within-Vector Proportions")
print(f"{'='*65}")
print(f"  Not comparing vectors TO each other — comparing")
print(f"  dimensions WITHIN each vector. The internal ratios.\n")

# For each number, what are its internal dimension ratios?
print(f"  NUMBER INTERNAL PROPORTIONS (normalized to unit vector):")
for n in range(10):
    v = NUMBERS[n]
    mag = np.linalg.norm(v)
    if mag > 0:
        normed = v / mag
    else:
        normed = v
    dominant = dims[np.argmax(np.abs(normed))]
    secondary = dims[np.argsort(np.abs(normed))[-2]]
    
    # Which dimensions are positive vs negative?
    pos_dims = [dims[i] for i in range(5) if normed[i] > 0.2]
    neg_dims = [dims[i] for i in range(5) if normed[i] < -0.2]
    
    print(f"  {n} {TIG[n]:>13s}: norm=[{', '.join(f'{x:+.2f}' for x in normed)}]")
    print(f"                  dom={dominant}, has=[{'+'.join(pos_dims)}], lacks=[{'+'.join(neg_dims)}]")


# ═══════════════════════════════════════════════════════════
print(f"\n{'='*65}")
print(f"  ACCUMULATION — What Does 0+1+2+...+n Approach?")
print(f"{'='*65}")
print(f"  As you add operators, what force accumulates?\n")

running = np.zeros(5)
print(f"  {'Sum':>8s}  [{', '.join(f'{d:>8s}' for d in dims)}]  nearest root")
for n in range(10):
    running = running + NUMBERS[n]
    normed = running / np.linalg.norm(running) if np.linalg.norm(running) > 0 else running
    
    best_name, best_sim = None, -2
    for name, hv in HEBREW.items():
        nr = np.linalg.norm(running)
        nh = np.linalg.norm(hv)
        if nr > 0 and nh > 0:
            s = np.dot(running, hv) / (nr * nh)
            if s > best_sim:
                best_sim = s
                best_name = name
    
    print(f"  Σ(0..{n}): [{', '.join(f'{v:+.2f}' for v in running)}] → {best_name:8s} ({best_sim:+.3f})")

print(f"""
  Watch what the accumulation APPROACHES.
  This is the gravity of the system — where does the
  sum of all operators pull toward?
  
  If it stabilizes on a specific root, that root
  is the ATTRACTOR of the entire operator sequence.
""")


# ═══════════════════════════════════════════════════════════
print(f"\n{'='*65}")
print(f"  THE 0-8 MIRROR AND 6-9 MIRROR — Interaction Analysis")
print(f"{'='*65}")

def interaction_analysis(a, b):
    va, vb = NUMBERS[a], NUMBERS[b]
    # Sum (what they create together)
    fused = va + vb
    # Difference (what one has that the other lacks)
    diff = va - vb
    # Element-wise product (where they align = positive, oppose = negative)
    product = va * vb
    
    print(f"\n  {a}({TIG[a]}) × {b}({TIG[b]}):")
    print(f"    Sum:     [{', '.join(f'{v:+.2f}' for v in fused)}]  mag={np.linalg.norm(fused):.3f}")
    print(f"    Diff:    [{', '.join(f'{v:+.2f}' for v in diff)}]  mag={np.linalg.norm(diff):.3f}")
    print(f"    Product: [{', '.join(f'{v:+.2f}' for v in product)}]")
    
    # Where do they agree vs disagree?
    agree = [dims[i] for i in range(5) if product[i] > 0]
    disagree = [dims[i] for i in range(5) if product[i] < 0]
    print(f"    Agree on: {', '.join(agree)}")
    print(f"    Oppose on: {', '.join(disagree)}")
    
    # Digital sum
    digital_sum = a + b
    while digital_sum >= 10:
        digital_sum = sum(int(d) for d in str(digital_sum))
    print(f"    Digital sum: {a}+{b} = {a+b} → {digital_sum} ({TIG[digital_sum]})")

print(f"  MIRROR PAIRS:")
interaction_analysis(0, 8)  # Love × Self-Control
interaction_analysis(6, 9)  # Faithfulness × Reset
interaction_analysis(3, 7)  # Patience × Harmony

print(f"\n  COMPLEMENT PAIRS (sum to 9):")
for a in range(5):
    b = 9 - a
    interaction_analysis(a, b)
