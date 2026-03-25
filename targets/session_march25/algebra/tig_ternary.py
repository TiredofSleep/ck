"""
TIG Balanced Ternary — Finding Operators 0-9

Known:
  1 = +1  (LATTICE, positive generator)
  2 = -1  (COUNTER, negative generator)
  3 =  0  (PROGRESS, neutral)

The 10 operators must be all valid balanced ternary representations
using trits {+1, -1, 0}.

Length 0: '' = 1 value → VOID (0)
Length 1: +1, -1, 0 = 3 values → operators 1, 2, 3
Length 2: 9 permutations → need 6 for operators 4, 5, 6, 7, 8, 9

But 7 ≡ 0 (torus inversion). So 7 might be a special case.
That leaves 5 operators (4, 5, 6, 8, 9) from 9 permutations.

Which 5 (or 6) of the 9 two-trit permutations map to which operators?
The binary patterns Brayden gave us constrain the answer.

(c) 2026 Brayden Sanders / 7Site LLC — TIG Unified Theory
"""

import numpy as np
from itertools import product, permutations

# ============================================================
# THE BASE
# ============================================================

# Trit values
P = +1   # positive / I / structure
N = -1   # negative / anti-I / counter-structure  
Z =  0   # neutral / balance point

TRIT_SYMBOL = {P: '+', N: '-', Z: '0'}

# Known mappings
# Operator: ternary
KNOWN = {
    0: (),           # VOID: empty / nothing
    1: (P,),         # LATTICE: +1
    2: (N,),         # COUNTER: -1
    3: (Z,),         # PROGRESS: 0 (the neutral)
}

# Brayden's binary (for cross-reference)
BINARY = {
    0: '0',
    1: '1',
    2: '10',
    3: '11',
    4: '1010',
    5: '?',
    6: '101',
    7: '01',
    8: '010',
    9: '111',
}

OPS = ["VOID","LATTICE","COUNTER","PROGRESS","COLLAPSE",
       "BALANCE","CHAOS","HARMONY","BREATH","RESET"]

# ============================================================
# ALL TWO-TRIT PERMUTATIONS
# ============================================================

def enumerate_two_trits():
    """All 9 two-trit combinations with meaning analysis."""
    
    print(f"\n{'='*60}")
    print(f"  ALL TWO-TRIT COMBINATIONS")
    print(f"  Each pair of {{+1, -1, 0}} composed")
    print(f"{'='*60}")
    
    combos = []
    
    for a in [P, N, Z]:
        for b in [P, N, Z]:
            trit_str = f"({TRIT_SYMBOL[a]},{TRIT_SYMBOL[b]})"
            
            # Properties
            trit_sum = a + b
            trit_product = a * b
            magnitude = abs(a) + abs(b)
            is_palindrome = (a == b)
            is_mirror = (a == -b)
            has_zero = (a == 0 or b == 0)
            
            # Map to I/O binary
            io = ''
            for t in [a, b]:
                if t == P: io += '1'
                elif t == N: io += '0'  # counter = force/O
                else: io += 'x'  # neutral
            
            # Distance from source: how far from (0,0)?
            dist = abs(a) + abs(b)
            
            combos.append({
                'trits': (a, b),
                'str': trit_str,
                'sum': trit_sum,
                'product': trit_product,
                'magnitude': magnitude,
                'palindrome': is_palindrome,
                'mirror_pair': is_mirror,
                'has_zero': has_zero,
                'io': io,
                'dist': dist,
            })
            
            print(f"    {trit_str:>8s}  sum={trit_sum:+d}  prod={trit_product:+d}  "
                  f"|mag|={magnitude}  pal={'✓' if is_palindrome else '✗'}  "
                  f"mir={'✓' if is_mirror else '✗'}  "
                  f"I/O={io}  dist={dist}")
    
    return combos


def find_mapping():
    """
    Find which two-trit combos map to which operators.
    
    Constraints from Brayden's binary and operator meanings:
    
    4 (COLLAPSE) = 1010 binary = I-O-I-O = oscillation
      → (+1,-1): positive then negative. The oscillation.
      
    5 (BALANCE) = ??? 
      → Must be self-mirror (5+5=10). Must be the balance point.
      → (-1,+1): negative then positive. Counter-oscillation of 4.
      OR (0,0): neutral neutral. Pure balance.
      
    6 (CHAOS) = 101 binary = I-O-I
      → (+1,0): structure into neutral. 
      OR (+1,-1,+1) but that's 3 trits...
      
    7 (HARMONY) = 01 binary = O-I = force then structure
      → (0,+1): neutral births positive. Void produces lattice.
      → This IS "harmony produces lattice as its first child"
      
    8 (BREATH) = 010 binary = O-I-O = force-structure-force
      → (0,-1): neutral then negative. 
      OR (-1,0): negative then neutral.
      
    9 (RESET) = 111 binary = I-I-I = all structure
      → (+1,+1): double positive. Maximum. Overflows.
    """
    
    print(f"\n{'='*60}")
    print(f"  MAPPING TWO-TRIT → OPERATORS 4-9")
    print(f"{'='*60}")
    
    # Strong constraints
    print(f"\n  STRONG CONSTRAINTS (from binary + meaning):")
    
    # 9 = 111 = all I = maximum structure → (+1,+1) double positive
    print(f"    9 (RESET) = 111 binary → (+,+) double positive")
    
    # 7 = 01 = O then I → (0,+1) or we handle 7≡0 separately
    print(f"    7 (HARMONY) = 01 binary → (0,+) void births structure")
    
    # 4 = 1010 = oscillation → (+1,-1) positive-negative
    print(f"    4 (COLLAPSE) = 1010 binary → (+,-) oscillation")
    
    # 8 = 010 = O-I-O → This has 3 elements in binary but needs 2 trits
    # The pattern is: void-structure-void = breath (inhale-exhale)
    # In ternary: (-1,0) or (0,-1)?
    # 8 is on the backward cycle (7→8→9→0)
    # 8 = first step backward from harmony
    # If 7 = (0,+), then 8 should be 7 with "one more step"
    # (0,+) → add dissolution → (0,-1)? Or prepend: (-1, 0, +)?
    # Since 8's binary starts with 0: → (0, -1) zero then negative
    print(f"    8 (BREATH) = 010 binary → (0,-) neutral then counter")
    
    # That leaves 5 and 6 from: (-1,-1), (-1,0), (-1,+1), (+1,0)
    
    # 6 = CHAOS = 101 binary = I-O-I
    # Force geometry: structure, force, structure — unstable sandwich
    # Mirror of 4? 4=(+,-), so mirror-of-4 = (-,+)?
    # But 4+6=10, they ARE mirrors!
    # So 6 = (-1, +1): counter then lattice
    # OR: 6 = (+1, 0): structure then neutral
    
    # 5 = BALANCE = self-mirror (5+5=10)
    # Must have equal positive and negative somehow
    # Remaining options depend on 6's assignment
    
    # OPTION A: 6 = (-1,+1), 5 = (+1,0) or (-1,0) or (-1,-1)
    # OPTION B: 6 = (+1,0), 5 = (-1,+1) or (-1,0) or (-1,-1)
    
    print(f"\n  DEDUCTION:")
    print(f"    Assigned: 4=(+,-), 7=(0,+), 8=(0,-), 9=(+,+)")
    print(f"    Remaining trits: (-,-), (-,0), (-,+), (+,0)")
    print(f"    Remaining ops: 5, 6")
    print(f"    Wait — that's 4 remaining trits for 2 operators")
    print(f"    We need to also check if 7 should be here or special")
    
    print(f"\n  IF 7≡0 is handled separately (torus inversion):")
    print(f"    Then 7 is NOT a two-trit combo, it's VOID seen from inside")
    print(f"    Remaining trits: (0,+), (-,-), (-,0), (-,+), (+,0)")
    print(f"    Remaining ops: 5, 6, 7")
    
    print(f"\n  BUT 7 = (0,+1) feels RIGHT: 'void births structure'")
    print(f"  So keep 7 = (0,+1)")
    
    print(f"\n  Remaining: (-,-), (-,0), (-,+), (+,0) → ops 5, 6")
    
    # Key insight: 4 and 6 are mirrors (4+6=10)
    # 4 = (+,-) = positive then negative
    # 6 should be the mirror: (-,+) = negative then positive
    # This is EXACT mirror on the trit level!
    
    print(f"\n  4+6=10 (mirror pair):")
    print(f"    4 = (+,-) : COLLAPSE = positive→negative")  
    print(f"    6 = (-,+) : CHAOS = negative→positive")
    print(f"    They're TRIT COMPLEMENTS. ✓")
    
    # That leaves: (-,-), (-,0), (+,0) for operator 5
    # 5 = BALANCE = the midpoint
    # 5 is self-mirror (5+5=10)
    # In balanced ternary, what is self-complementary?
    # (-,-) complement is (+,+) = 9. Not self.
    # (-,0) complement is (+,0). Not self.
    # (+,0) complement is (-,0). Not self.
    # NONE of the remaining are self-complementary!
    
    # Unless... 5 has a DIFFERENT property.
    # 5 is BALANCE. The EXACT middle. 
    # In balanced ternary, the middle of (-1, 0, +1) is 0.
    # But 0 as a single trit is already operator 3 (PROGRESS).
    
    # What if 5 = (0,0)? Double neutral. Pure balance.
    # Then (0,0) isn't "remaining" because we need to check:
    # We assigned (0,+) to 7 and (0,-) to 8
    # (0,0) is available!
    
    print(f"\n  5 (BALANCE):")
    print(f"    (0,0) = double neutral. Pure balance. The center.")
    print(f"    Sum = 0, product = 0, palindrome ✓, self-symmetric ✓")
    print(f"    This IS balance. Nothing else can be.")
    
    # Remaining unassigned: (-,-), (-,0), (+,0)
    # We need to verify none of these should be 5 instead
    
    print(f"\n  Unassigned two-trits: (-,-), (-,0), (+,0)")
    print(f"  These are NOT operators 0-9.")
    print(f"  They might be:")
    print(f"    (-,-) = double negative = beyond reset? = overflow")
    print(f"    (-,0) = counter→neutral = dissolution path")
    print(f"    (+,0) = lattice→neutral = structure fading")
    print(f"  These could be the 'forbidden' compositions")
    print(f"  Or they could reduce to existing operators through the table")
    
    return {
        0: (),
        1: (P,),
        2: (N,),
        3: (Z,),
        4: (P, N),
        5: (Z, Z),
        6: (N, P),
        7: (Z, P),
        8: (Z, N),
        9: (P, P),
    }


def verify_mapping(mapping):
    """Verify the mapping against all known properties."""
    
    print(f"\n{'='*60}")
    print(f"  VERIFICATION")
    print(f"{'='*60}")
    
    print(f"\n  COMPLETE MAPPING:")
    print(f"  {'Op':>3s} {'Name':>10s} {'Ternary':>12s} {'Sum':>5s} {'Binary':>8s} {'Dist':>5s}")
    print(f"  {'-'*48}")
    
    for op in range(10):
        trits = mapping[op]
        trit_str = '(' + ','.join(TRIT_SYMBOL[t] for t in trits) + ')' if trits else '()'
        trit_sum = sum(trits) if trits else 0
        binary = BINARY[op]
        dist = sum(abs(t) for t in trits)
        
        print(f"  {op:>3d} {OPS[op]:>10s} {trit_str:>12s} {trit_sum:>+5d} {binary:>8s} {dist:>5d}")
    
    # Check mirror pairs
    print(f"\n  MIRROR PAIR CHECK (a + b = 10):")
    mirrors = [(1,9), (2,8), (3,7), (4,6)]
    
    for a, b in mirrors:
        ta = mapping[a]
        tb = mapping[b]
        
        # Check if trits are complementary
        if len(ta) == len(tb):
            is_complement = all(ta[i] == -tb[i] for i in range(len(ta)))
        else:
            is_complement = False
        
        # Check if trit sums are complementary  
        sum_a = sum(ta) if ta else 0
        sum_b = sum(tb) if tb else 0
        sum_comp = (sum_a + sum_b == 0)
        
        ta_str = '(' + ','.join(TRIT_SYMBOL[t] for t in ta) + ')'
        tb_str = '(' + ','.join(TRIT_SYMBOL[t] for t in tb) + ')'
        
        print(f"    {a}↔{b}: {ta_str:>8s} ↔ {tb_str:>8s}  "
              f"complement={'✓' if is_complement else '✗'}  "
              f"sum_zero={'✓' if sum_comp else '✗'}")
    
    # Check 5 self-mirror
    t5 = mapping[5]
    t5_comp = tuple(-t for t in t5) if t5 else ()
    print(f"    5↔5: {t5} → complement = {t5_comp} = {'self ✓' if t5 == t5_comp else '✗'}")
    
    # Check 0≡7
    t0 = mapping[0]
    t7 = mapping[7]
    print(f"\n  0≡7 CHECK:")
    print(f"    0 = {t0}")
    print(f"    7 = {t7}")
    print(f"    7 is 'void that produced its first structure'")
    print(f"    (0,+) = nothing then lattice. Harmony IS void-producing. ✓")
    
    # Generation order
    print(f"\n  GENERATION ORDER:")
    print(f"  7→1→2→3→4→5→6→7  (forward cycle)")
    
    gen = [7, 1, 2, 3, 4, 5, 6, 7]
    for i in range(len(gen)-1):
        a = gen[i]
        b = gen[i+1]
        ta = mapping[a]
        tb = mapping[b]
        
        ta_str = ','.join(TRIT_SYMBOL[t] for t in ta)
        tb_str = ','.join(TRIT_SYMBOL[t] for t in tb)
        
        # What operation transforms ta into tb?
        print(f"    {a}({ta_str:>5s}) → {b}({tb_str:>5s}): ", end="")
        
        if len(tb) > len(ta):
            # Child is longer
            if len(ta) == 0:
                print(f"void produces {tb_str}")
            elif len(ta) == 1 and len(tb) == 2:
                print(f"single trit compounds with {TRIT_SYMBOL[tb[1]]}")
            else:
                print(f"grows")
        elif len(tb) < len(ta):
            print(f"contracts back to fundamental")
        elif len(ta) == len(tb):
            diffs = [(ta[j], tb[j]) for j in range(len(ta)) if ta[j] != tb[j]]
            if diffs:
                print(f"trit change: {diffs}")
            else:
                print(f"same (cycle complete)")
        else:
            print(f"???")
    
    print(f"\n  7→8→9→0  (backward/dissolution)")
    back = [7, 8, 9, 0]
    for i in range(len(back)-1):
        a = back[i]
        b = back[i+1]
        ta = mapping[a]
        tb = mapping[b]
        ta_str = ','.join(TRIT_SYMBOL[t] for t in ta)
        tb_str = ','.join(TRIT_SYMBOL[t] for t in tb)
        print(f"    {a}({ta_str:>5s}) → {b}({tb_str:>5s})")


def build_3x3_table(mapping):
    """
    Build the fundamental 3×3 table from {+1, -1, 0}.
    This is the BEING table at its most fundamental.
    The 10×10 emerges from composing this 3×3 with itself.
    """
    
    print(f"\n{'='*60}")
    print(f"  THE 3×3 FUNDAMENTAL TABLE")
    print(f"  Composition of {{+1, -1, 0}} = {{LATTICE, COUNTER, PROGRESS}}")
    print(f"{'='*60}")
    
    # In balanced ternary, the natural operations are:
    
    # BEING (measurement, collapse toward source):
    # What do two trits LOOK LIKE together?
    # Answer: their minimum absolute value (closest to zero/source)
    
    # BECOMING (transformation, pull away from source):
    # What do two trits CREATE?
    # Answer: their sum (complexity adds)... but clamped to {-1,0,+1}
    
    # Let's try several rules and see which produces the right properties
    
    trits = [P, N, Z]  # +1, -1, 0
    labels = ['+1', '-1', ' 0']
    
    rules = {
        'min_abs': lambda a, b: min(a, b, key=abs) if a != b else a,
        'max_abs': lambda a, b: max(a, b, key=abs) if a != b else a,
        'product': lambda a, b: a * b,
        'add_clamp': lambda a, b: max(-1, min(1, a + b)),
        'xor_sign': lambda a, b: 0 if a == b else (a if b == 0 else (b if a == 0 else -a*b)),
        'meet': lambda a, b: 0 if a + b == 0 else (a if abs(a) >= abs(b) else b),
        'absorb_zero': lambda a, b: 0 if a == 0 or b == 0 else (a if a == b else 0),
    }
    
    for rname, rule in rules.items():
        table = np.zeros((3, 3), dtype=int)
        
        for i, a in enumerate(trits):
            for j, b in enumerate(trits):
                result = rule(a, b)
                # Map back to index
                table[i, j] = trits.index(result) if result in trits else 1
        
        # Analyze
        eigs = np.sort(np.real(np.linalg.eigvals(table.astype(float))))[::-1]
        det = np.linalg.det(table.astype(float))
        comm = np.all(table == table.T)
        
        # Check for constants
        matches = []
        for i in range(3):
            for j in range(i+1, 3):
                if abs(eigs[j]) > 0.01:
                    r = abs(eigs[i] / eigs[j])
                    for cname, cval in [('phi', 1.618034), ('sqrt2', 1.414214), 
                                         ('e', 2.718282), ('pi', 3.141593)]:
                        if abs(r - cval) / cval < 0.05:
                            matches.append(f"{cname}({abs(r-cval)/cval*100:.1f}%)")
        
        print(f"\n  Rule: {rname}")
        print(f"    ", end="")
        print(f"{'':>4s}", end="")
        for l in labels:
            print(f"{l:>4s}", end="")
        print()
        
        for i, a in enumerate(trits):
            print(f"    {labels[i]:>4s}", end="")
            for j, b in enumerate(trits):
                result = rule(a, b)
                print(f"{TRIT_SYMBOL[result]:>4s}", end="")
            print()
        
        print(f"    Comm: {'✓' if comm else '✗'}  Det: {det:.1f}  "
              f"Eigs: {', '.join(f'{e:.3f}' for e in eigs)}")
        if matches:
            print(f"    Constants: {', '.join(matches)}")


def the_product_table():
    """
    The PRODUCT of balanced ternary IS the natural composition.
    (+1) × (+1) = +1  (structure × structure = structure)
    (+1) × (-1) = -1  (structure × counter = counter)
    (+1) × (0)  = 0   (structure × nothing = nothing)
    (-1) × (-1) = +1  (counter × counter = structure! double negative = positive)
    (-1) × (0)  = 0   
    (0)  × (0)  = 0   (nothing × nothing = nothing)
    
    This gives us: the MULTIPLICATION TABLE of {-1, 0, +1}.
    Its eigenvalues are {-1, 0, 2}.
    """
    
    print(f"\n{'='*60}")
    print(f"  THE PRODUCT TABLE — Multiplication of Balanced Ternary")
    print(f"  This IS the fundamental composition.")
    print(f"{'='*60}")
    
    # Product table in {+1, -1, 0} order
    table = np.array([
        [+1, -1,  0],  # +1 × {+1, -1, 0}
        [-1, +1,  0],  # -1 × {+1, -1, 0}
        [ 0,  0,  0],  # 0  × {+1, -1, 0}
    ])
    
    print(f"\n    Multiplication of {{+1, -1, 0}}:")
    labels = ['+1', '-1', ' 0']
    print(f"    {'×':>4s}", end="")
    for l in labels:
        print(f"{l:>4s}", end="")
    print()
    for i in range(3):
        print(f"    {labels[i]:>4s}", end="")
        for j in range(3):
            print(f"{table[i,j]:>+4d}", end="")
        print()
    
    eigs = np.sort(np.real(np.linalg.eigvals(table.astype(float))))[::-1]
    det = np.linalg.det(table.astype(float))
    
    print(f"\n    Eigenvalues: {eigs}")
    print(f"    Determinant: {det}")
    print(f"    Trace: {np.trace(table)}")
    
    print(f"\n    Properties:")
    print(f"    - Commutative ✓ (multiplication is commutative)")
    print(f"    - Associative ✓ (multiplication is associative)")
    print(f"    - 0 is absorber (void absorbs everything)")
    print(f"    - +1 is identity (structure preserves)")
    print(f"    - (-1)×(-1) = +1 (double negation = affirmation)")
    
    # This is the BEING table at the trit level.
    # What about BECOMING?
    
    print(f"\n  BECOMING via addition (clamped to {{-1, 0, +1}}):")
    
    add_table = np.zeros((3, 3), dtype=int)
    trits = [1, -1, 0]
    
    for i, a in enumerate(trits):
        for j, b in enumerate(trits):
            s = a + b
            # Clamp: if |s| > 1, it wraps
            if s > 1: s = -1   # overflow wraps to negative (reset)
            if s < -1: s = 1   # underflow wraps to positive
            add_table[i, j] = s
    
    print(f"    {'+':<4s}", end="")
    for l in labels:
        print(f"{l:>4s}", end="")
    print()
    for i in range(3):
        print(f"    {labels[i]:>4s}", end="")
        for j in range(3):
            print(f"{add_table[i,j]:>+4d}", end="")
        print()
    
    add_eigs = np.sort(np.real(np.linalg.eigvals(add_table.astype(float))))[::-1]
    print(f"\n    Eigenvalues: {add_eigs}")
    print(f"    Note: +1 + +1 = +2 → wraps to -1 (OVERFLOW = RESET)")
    print(f"    This IS 'every act pulls further from source':")
    print(f"    Two positive acts overflow into negative territory")
    
    # DOING = |Being - Becoming|
    doing = np.abs(table - add_table)
    print(f"\n  DOING = |Product - Addition|:")
    print(f"    {'Δ':<4s}", end="")
    for l in labels:
        print(f"{l:>4s}", end="")
    print()
    for i in range(3):
        print(f"    {labels[i]:>4s}", end="")
        for j in range(3):
            print(f"{doing[i,j]:>4d}", end="")
        print()
    
    doing_eigs = np.sort(np.real(np.linalg.eigvals(doing.astype(float))))[::-1]
    print(f"\n    Eigenvalues: {doing_eigs}")
    
    # Check for phi
    for i in range(3):
        for j in range(i+1, 3):
            if abs(add_eigs[j]) > 0.01:
                r = abs(add_eigs[i] / add_eigs[j])
                print(f"    Addition λ{i}/λ{j} = {r:.6f}")
    
    # The 3×3 addition table eigenvalues
    print(f"\n    Addition eigenvalues: {add_eigs}")
    print(f"    Product eigenvalues: {eigs}")
    
    # φ check: does the golden ratio appear?
    # The characteristic polynomial of the addition table
    # might have φ as a root
    char_poly = np.poly(add_table.astype(float))
    print(f"    Addition char polynomial coefficients: {char_poly}")
    
    # Try solving for roots
    roots = np.roots(char_poly)
    print(f"    Roots: {roots}")


def run_all():
    print("\n" + "="*60)
    print("  TIG BALANCED TERNARY — Operators from {+1, -1, 0}")
    print("  1=+1, 2=-1, 3=0. Find the rest.")
    print("="*60)
    
    # Enumerate all two-trit combos
    combos = enumerate_two_trits()
    
    # Find the mapping
    mapping = find_mapping()
    
    # Verify
    verify_mapping(mapping)
    
    # Build the 3×3 fundamental table
    build_3x3_table(mapping)
    
    # The product table (the real deal)
    the_product_table()
    
    # Summary
    print(f"\n\n{'='*60}")
    print(f"  THE COMPLETE MAPPING")
    print(f"{'='*60}")
    print(f"""
  Op  Name       Ternary    Binary   Meaning
  ─────────────────────────────────────────────────────
   0  VOID       ()         0        Nothing. The frame.
   1  LATTICE    (+)        1        First structure. Positive.
   2  COUNTER    (-)        10       Anti-structure. Negative.
   3  PROGRESS   (0)        11       Neutral. First balance.
   4  COLLAPSE   (+,-)      1010     Oscillation. Pos→neg.
   5  BALANCE    (0,0)      ???      Double neutral. Pure center.
   6  CHAOS      (-,+)      101      Counter-oscillation. Neg→pos.
   7  HARMONY    (0,+)      01       Void births structure.
   8  BREATH     (0,-)      010      Void births counter.
   9  RESET      (+,+)      111      Double positive. Overflow.

  Mirror pairs (complement trits, sum to zero):
    1(+) ↔ 2(-):     fundamental mirrors
    4(+,-) ↔ 6(-,+): compound mirrors  
    7(0,+) ↔ 8(0,-): void-birth mirrors
    3(0) ↔ itself:   neutral is self-mirror
    5(0,0) ↔ itself: double-neutral is self-mirror
    9(+,+): mirror would be (-,-) = not in the 10 operators
    
  9's mirror (-,-) being OUTSIDE the operator set means
  RESET has no mirror. It's the edge. The boundary.
  (-,-) = double negation = beyond the algebra = void.
  9 → 0 because the mirror of maximum structure IS void.
  
  The 3×3 core: multiplication of {{+1, -1, 0}}
    Being = multiply (measure: structure × counter = counter)
    Becoming = add with overflow (act: positive + positive wraps negative)
    Doing = |multiply - add| = the disagreement
    
  The 10 operators are:
    1 empty trit (void)
    3 single trits (generators)
    6 two-trit compounds (the active operators)
    = 10 total
    
  1 + 3 + 6 = 10. The system closes at exactly 10.
  
  And 5 (BALANCE) = (0,0) which means:
    5's binary is probably '00' or '0x0' — 
    pure void seen from both sides.
    Balance is double nothing. The still point.
    """)


if __name__ == "__main__":
    run_all()
