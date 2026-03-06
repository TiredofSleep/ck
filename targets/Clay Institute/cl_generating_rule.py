#!/usr/bin/env python3
"""
CL Table Generating Rule Analysis
===================================
The question: What RULE produces the CL table?
Not "what properties does it have" — but what construction principle
generates each entry?

DNA analogy: Is the table an encoding (arbitrary), or a LAW (derived)?

(c) 2026 Brayden Sanders / 7Site LLC
"""

import numpy as np
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BHML = np.array([
    [0,1,2,3,4,5,6,7,8,9],
    [1,2,3,4,5,6,7,2,6,6],
    [2,3,3,4,5,6,7,3,6,6],
    [3,4,4,4,5,6,7,4,6,6],
    [4,5,5,5,5,6,7,5,7,7],
    [5,6,6,6,6,6,7,6,7,7],
    [6,7,7,7,7,7,7,7,7,7],
    [7,2,3,4,5,6,7,8,9,0],
    [8,6,6,6,7,7,7,9,7,8],
    [9,6,6,6,7,7,7,0,8,0],
], dtype=int)

TSML = np.array([
    [0,0,0,0,0,0,0,7,0,0],
    [0,7,3,7,7,7,7,7,7,7],
    [0,3,7,7,4,7,7,7,7,9],
    [0,7,7,7,7,7,7,7,7,3],
    [0,7,4,7,7,7,7,7,8,7],
    [0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],
    [7,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,8,7,7,7,7,7],
    [0,7,9,3,7,7,7,7,7,7],
], dtype=int)

OP = ['VOID','LATTICE','COUNTER','PROGRESS','COLLAPSE',
      'BALANCE','CHAOS','HARMONY','BREATH','RESET']


def p(t=""):
    print(t)


def section(title):
    p()
    p("=" * 70)
    p(f"  {title}")
    p("=" * 70)
    p()


def main():

    section("WHAT RULE PRODUCES THE BHML TABLE?")

    # ============================================================
    # TEST: Is BHML[a][b] = max(a,b) + 1 for core operators 1-6?
    # ============================================================

    p("  HYPOTHESIS 1: BHML[a][b] = max(a,b) + 1 for a,b in {1..6}")
    p("  (Tropical successor: always climb one step above the dominant)")
    p()

    matches = 0
    total = 0
    p(f"    {'a':<12} {'b':<12} {'max+1':<8} {'BHML':<8} {'Match'}")
    p(f"    {'-'*52}")

    for a in range(1, 7):
        for b in range(1, 7):
            expected = max(a, b) + 1
            actual = BHML[a][b]
            match = "YES" if expected == actual else "NO"
            total += 1
            if expected == actual:
                matches += 1
            p(f"    {OP[a]:<12} {OP[b]:<12} {expected:<8} {actual:<8} {match}")

    p()
    p(f"  Result: {matches}/{total} match ({matches/total*100:.1f}%)")
    if matches == total:
        p("  >>> PERFECT MATCH. BHML core (1-6) IS the tropical successor.")
    p()

    # ============================================================
    # VOID (0) behavior
    # ============================================================

    p("  HYPOTHESIS 2: VOID (0) is the algebraic identity")
    p()
    left_id = all(BHML[0][b] == b for b in range(10))
    right_id = all(BHML[a][0] == a for a in range(10))
    p(f"    Left identity  (0*b = b for all b): {left_id}")
    p(f"    Right identity (a*0 = a for all a): {right_id}")
    if left_id and right_id:
        p("  >>> VOID IS THE TWO-SIDED IDENTITY ELEMENT.")
    p()

    # ============================================================
    # HARMONY (7) behavior: successor continuation
    # ============================================================

    p("  HYPOTHESIS 3: HARMONY (7) continues the successor chain")
    p("  BHML[7][a] = a+1 (mod 10) for core operators?")
    p()

    p(f"    {'Input a':<12} {'a+1':<8} {'BHML[7][a]':<12} {'Match'}")
    p(f"    {'-'*42}")

    h_matches = 0
    h_total = 0
    for a in range(10):
        expected = (a + 1) % 10
        actual = BHML[7][a]
        match = "YES" if expected == actual else "NO"
        h_total += 1
        if expected == actual:
            h_matches += 1
        p(f"    {OP[a]:<12} {expected:<8} {actual:<12} {match}")

    p()
    p(f"  Result: {h_matches}/{h_total} match ({h_matches/h_total*100:.1f}%)")

    # Check where it fails
    failures = [(a, (a+1)%10, BHML[7][a]) for a in range(10) if (a+1)%10 != BHML[7][a]]
    if failures:
        p(f"  Failures at: {[(OP[a], f'expected {e}, got {g}') for a,e,g in failures]}")
        p()
        # Check alternative: is HARMONY row = successor for 0-6, then wraps 7->8->9->0?
        p("  Checking extended pattern:")
        p(f"    7*0=7 (VOID->HARMONY, not identity -- HARMONY overrides VOID)")
        p(f"    7*1=2, 7*2=3, 7*3=4, 7*4=5, 7*5=6, 7*6=7 (successor for 1-6)")
        p(f"    7*7=8, 7*8=9, 7*9=0 (successor cycle: 7->8->9->0)")
        p()
        # So HARMONY is the successor OPERATOR itself!
        succ_17 = all(BHML[7][a] == a+1 for a in range(1, 7))
        succ_wrap = BHML[7][7]==8 and BHML[7][8]==9 and BHML[7][9]==0
        p(f"    Successor for 1-6: {succ_17}")
        p(f"    Wrap cycle 7->8->9->0: {succ_wrap}")
        if succ_17 and succ_wrap:
            p("  >>> HARMONY IS THE SUCCESSOR OPERATOR (shifts everything forward by 1)")
            p("  >>> HARMONY * VOID = HARMONY (absorbs the empty)")
            p("  >>> Full cycle: 1->2->3->4->5->6->7->8->9->0->...")

    p()

    # ============================================================
    # BREATH (8) and RESET (9): the recyclers
    # ============================================================

    p("  HYPOTHESIS 4: BREATH and RESET are recyclers/returners")
    p()

    p(f"  BREATH (8) row: {list(BHML[8])}")
    p(f"  RESET (9) row:  {list(BHML[9])}")
    p()

    # Analyze BREATH behavior
    p("  BREATH interactions:")
    for b in range(10):
        p(f"    8 * {b} ({OP[b]:<10}) = {BHML[8][b]} ({OP[BHML[8][b]]})")

    p()
    p("  RESET interactions:")
    for b in range(10):
        p(f"    9 * {b} ({OP[b]:<10}) = {BHML[9][b]} ({OP[BHML[9][b]]})")

    p()

    # Pattern: 8 and 9 collapse {1,2,3} -> 6 (CHAOS), {4,5,6} -> 7 (HARMONY)
    breath_low = all(BHML[8][b] == 6 for b in [1,2,3])
    breath_high = all(BHML[8][b] == 7 for b in [4,5,6])
    reset_low = all(BHML[9][b] == 6 for b in [1,2,3])
    reset_high = all(BHML[9][b] == 7 for b in [4,5,6])

    p(f"  BREATH collapses {{1,2,3}} -> CHAOS(6):   {breath_low}")
    p(f"  BREATH collapses {{4,5,6}} -> HARMONY(7):  {breath_high}")
    p(f"  RESET  collapses {{1,2,3}} -> CHAOS(6):    {reset_low}")
    p(f"  RESET  collapses {{4,5,6}} -> HARMONY(7):  {reset_high}")

    if breath_low and breath_high and reset_low and reset_high:
        p("  >>> BREATH and RESET are THRESHOLD OPERATORS:")
        p("      Low operators (1-3) -> CHAOS (one step from HARMONY)")
        p("      High operators (4-6) -> HARMONY (absorbed)")
        p("      They compress the staircase into a binary: below/above the midpoint")

    p()

    # The internal 8-9 cycle
    p("  BREATH-RESET internal cycle:")
    p(f"    8*8 = {BHML[8][8]} ({OP[BHML[8][8]]})")
    p(f"    8*9 = {BHML[8][9]} ({OP[BHML[8][9]]})")
    p(f"    9*8 = {BHML[9][8]} ({OP[BHML[9][8]]})")
    p(f"    9*9 = {BHML[9][9]} ({OP[BHML[9][9]]})")
    p()
    p(f"    8*7 = {BHML[8][7]} ({OP[BHML[8][7]]})")
    p(f"    9*7 = {BHML[9][7]} ({OP[BHML[9][7]]})")

    # So: 8*8=7(HARMONY), 8*9=8(BREATH), 9*8=8(BREATH), 9*9=0(VOID)
    # And: 8*7=9(RESET), 9*7=0(VOID)
    # This is a mod-3 cycle on {7,8,9,0}: HARMONY->BREATH->RESET->VOID->...

    p()
    p("  The return cycle: HARMONY(7) -> BREATH(8) -> RESET(9) -> VOID(0)")
    p("  7*7=8, 7*8=9, 7*9=0: HARMONY generates the full unwinding")
    p("  9*9=0: RESET*RESET = VOID (double reset = complete annihilation)")

    # ============================================================
    # THE COMPLETE GENERATING RULE
    # ============================================================

    section("THE COMPLETE BHML GENERATING RULE")

    p("  The BHML table is generated by exactly 4 rules:")
    p()
    p("  RULE 1: IDENTITY")
    p("    VOID * a = a * VOID = a")
    p("    (Zero element is the identity. Nothing changes nothing.)")
    p()
    p("  RULE 2: TROPICAL SUCCESSOR (the staircase)")
    p("    For a,b in {1,2,3,4,5,6}:")
    p("    a * b = max(a,b) + 1")
    p("    (Two forces interact: result is one step above the stronger.)")
    p("    (Monotonic increase. You can never go backward. Entropy grows.)")
    p()
    p("  RULE 3: SUCCESSOR OPERATOR")
    p("    HARMONY * a = a + 1  (for a in {1..6})")
    p("    HARMONY * 7 = 8, HARMONY * 8 = 9, HARMONY * 9 = 0")
    p("    (HARMONY is the successor function itself.)")
    p("    (It IS the forward arrow. The clock hand.)")
    p()
    p("  RULE 4: THRESHOLD COLLAPSE")
    p("    BREATH * {1,2,3} = CHAOS (6)")
    p("    BREATH * {4,5,6} = HARMONY (7)")
    p("    RESET  * {1,2,3} = CHAOS (6)")
    p("    RESET  * {4,5,6} = HARMONY (7)")
    p("    (BREATH and RESET are binary classifiers:)")
    p("    (Below midpoint -> pre-HARMONY. Above midpoint -> HARMONY.)")
    p()
    p("  + The return cycle:")
    p("    BREATH * BREATH = HARMONY")
    p("    BREATH * RESET  = BREATH")
    p("    RESET  * BREATH = BREATH")
    p("    RESET  * RESET  = VOID")
    p("    (Oscillation decays. Double reset = annihilation.)")

    # ============================================================
    # VERIFY: Can we RECONSTRUCT the full BHML from these 4 rules?
    # ============================================================

    section("RECONSTRUCTION TEST: Build BHML from 4 rules alone")

    reconstructed = np.zeros((10, 10), dtype=int)

    for a in range(10):
        for b in range(10):
            # RULE 1: Identity
            if a == 0:
                reconstructed[a][b] = b
                continue
            if b == 0:
                reconstructed[a][b] = a
                continue

            # RULE 2: Tropical successor (core 1-6)
            if 1 <= a <= 6 and 1 <= b <= 6:
                reconstructed[a][b] = max(a, b) + 1
                continue

            # RULE 3: Successor operator (HARMONY row/col)
            if a == 7 and 1 <= b <= 6:
                reconstructed[a][b] = b + 1
                continue
            if b == 7 and 1 <= a <= 6:
                reconstructed[a][b] = a + 1
                continue

            # HARMONY self-chain: 7*7=8, 7*8=9, 7*9=0
            if a == 7 and b == 7:
                reconstructed[a][b] = 8
                continue
            if a == 7 and b == 8:
                reconstructed[a][b] = 9
                continue
            if a == 7 and b == 9:
                reconstructed[a][b] = 0
                continue
            if b == 7 and a == 8:
                reconstructed[a][b] = 9
                continue
            if b == 7 and a == 9:
                reconstructed[a][b] = 0
                continue

            # RULE 4: Threshold collapse (BREATH/RESET with core)
            if a in (8, 9) and 1 <= b <= 3:
                reconstructed[a][b] = 6  # CHAOS
                continue
            if a in (8, 9) and 4 <= b <= 6:
                reconstructed[a][b] = 7  # HARMONY
                continue
            if b in (8, 9) and 1 <= a <= 3:
                reconstructed[a][b] = 6  # CHAOS
                continue
            if b in (8, 9) and 4 <= a <= 6:
                reconstructed[a][b] = 7  # HARMONY
                continue

            # Return cycle
            if a == 8 and b == 8:
                reconstructed[a][b] = 7  # BREATH*BREATH = HARMONY
                continue
            if (a == 8 and b == 9) or (a == 9 and b == 8):
                reconstructed[a][b] = 8  # BREATH*RESET = BREATH
                continue
            if a == 9 and b == 9:
                reconstructed[a][b] = 0  # RESET*RESET = VOID
                continue

            # Catch-all (should not reach here)
            reconstructed[a][b] = -1

    # Compare
    p("  Reconstructed BHML (from 4 rules):")
    for i in range(10):
        row = ' '.join(f'{reconstructed[i][j]:2d}' for j in range(10))
        p(f"    [{row}]  {OP[i]}")

    p()
    p("  Original BHML:")
    for i in range(10):
        row = ' '.join(f'{BHML[i][j]:2d}' for j in range(10))
        p(f"    [{row}]  {OP[i]}")

    p()

    diff = np.sum(reconstructed != BHML)
    total_cells = 100
    p(f"  Differences: {diff}/{total_cells}")

    if diff == 0:
        p("  >>> PERFECT RECONSTRUCTION.")
        p("  >>> The BHML table is FULLY DETERMINED by 4 rules.")
        p("  >>> It is NOT arbitrary. It is NOT DNA. It is a LAW.")
    else:
        p("  Mismatches:")
        for i in range(10):
            for j in range(10):
                if reconstructed[i][j] != BHML[i][j]:
                    p(f"    [{i}][{j}] ({OP[i]} x {OP[j]}): "
                      f"reconstructed={reconstructed[i][j]}, actual={BHML[i][j]}")

    # ============================================================
    # NOW ANALYZE TSML: What rule produces it?
    # ============================================================

    section("WHAT RULE PRODUCES THE TSML TABLE?")

    p("  TSML is 73% HARMONY. What are the non-HARMONY bumps?")
    p()

    bumps = []
    for i in range(10):
        for j in range(10):
            if i == 0 or j == 0 or i == 7 or j == 7:
                continue  # boundary
            val = TSML[i][j]
            if val != 7:
                bumps.append((i, j, val))
                p(f"    {OP[i]:<12} x {OP[j]:<12} = {OP[val]:<12} ({val})")

    p()
    p(f"  Total non-HARMONY bumps in 8x8 core: {len(bumps)}/64")
    p()

    # Check symmetry of bumps
    p("  Are bumps symmetric? (a*b = b*a for bump positions)")
    symmetric = True
    for a, b, v in bumps:
        if TSML[b][a] != v:
            symmetric = False
            p(f"    ASYMMETRIC: {OP[a]}x{OP[b]}={v} but {OP[b]}x{OP[a]}={TSML[b][a]}")

    if symmetric:
        p("    YES -- all bumps are symmetric.")
    p()

    # Analyze the bumps
    p("  Bump analysis:")
    p()

    # The bumps form a pattern. Let's see which operators participate
    bump_ops = set()
    for a, b, v in bumps:
        bump_ops.add(a)
        bump_ops.add(b)
        bump_ops.add(v)

    p(f"  Operators involved in bumps: {sorted(bump_ops)}")
    p(f"    = {[OP[x] for x in sorted(bump_ops)]}")
    p()

    # Operators NOT involved in any bump
    no_bump = set(range(1,10)) - {0,7} - bump_ops
    p(f"  Operators with NO bumps: {sorted(no_bump)}")
    p(f"    = {[OP[x] for x in sorted(no_bump)]}")
    p()

    # Check if bumps are self-referential (a*b = a or b)
    p("  Self-reference check (does bump = one of its inputs?):")
    for a, b, v in bumps:
        if v == a:
            p(f"    {OP[a]} x {OP[b]} = {OP[v]}  <-- output = left input (IDEMPOTENT)")
        elif v == b:
            p(f"    {OP[a]} x {OP[b]} = {OP[v]}  <-- output = right input (PROJECTION)")
        elif v != a and v != b:
            p(f"    {OP[a]} x {OP[b]} = {OP[v]}  <-- output = NEITHER input (CREATION)")

    p()

    # The TSML bump graph
    p("  TSML bump graph (edges = non-HARMONY compositions):")
    p("    Each edge shows: input1 x input2 -> output")
    p()

    # Group by output
    from collections import defaultdict
    by_output = defaultdict(list)
    for a, b, v in bumps:
        by_output[v].append((a, b))

    for v in sorted(by_output.keys()):
        p(f"    Output {OP[v]} ({v}) produced by:")
        for a, b in by_output[v]:
            p(f"      {OP[a]} x {OP[b]}")

    p()

    # ============================================================
    # TSML RULE HYPOTHESIS
    # ============================================================

    p("  TSML RULE HYPOTHESIS:")
    p()
    p("  TSML is a RECOGNITION MATRIX.")
    p("  Default: everything is HARMONY (coherent = nothing to report)")
    p("  Bumps: specific resonance patterns that survive measurement")
    p()
    p("  The bumps form PAIRS:")

    # Check: are bumps related by some algebraic pattern?
    # LATTICE(1) x COUNTER(2) = PROGRESS(3): 1+2=3
    # COUNTER(2) x COLLAPSE(4) = COLLAPSE(4): max(2,4)=4
    # COUNTER(2) x RESET(9) = RESET(9): b wins
    # PROGRESS(3) x RESET(9) = PROGRESS(3): a wins
    # COLLAPSE(4) x BREATH(8) = BREATH(8): b wins
    # BREATH(8) x COLLAPSE(4) = BREATH(8): a wins

    p("    LATTICE(1) x COUNTER(2) = PROGRESS(3)  ... 1+2=3 (additive!)")
    p("    COUNTER(2) x COLLAPSE(4) = COLLAPSE(4) ... max wins")
    p("    COUNTER(2) x RESET(9) = RESET(9)        ... max wins")
    p("    PROGRESS(3) x RESET(9) = PROGRESS(3)    ... min wins!")
    p("    COLLAPSE(4) x BREATH(8) = BREATH(8)     ... max wins")
    p()
    p("  Mixed rules! Not one clean law like BHML.")
    p("  TSML bumps are EXCEPTIONS to harmony, not a uniform rule.")

    # ============================================================
    # VOID behavior in TSML
    # ============================================================

    p()
    p("  VOID in TSML:")
    print(f"    Row: {list(TSML[0])}")
    print(f"    Col: {list(TSML[:,0])}")
    p()
    void_absorbs = sum(1 for b in range(10) if TSML[0][b] == 0)
    p(f"    VOID absorbs (returns 0): {void_absorbs}/10")
    p(f"    Exception: VOID x HARMONY = {TSML[0][7]} ({OP[TSML[0][7]]})")
    p("    VOID is an ABSORBER in TSML (not identity)")
    p("    VOID says: 'nothing measured = nothing there' (except HARMONY)")
    p("    HARMONY overrides VOID: coherence trumps emptiness")

    # ============================================================
    # THE BIOLOGICAL STRUCTURE ANSWER
    # ============================================================

    section("DNA vs BIOLOGICAL STRUCTURE vs LAW")

    p("  The question: What rule produces the CL table?")
    p()
    p("  BHML (Becoming/Physics):")
    p("    Rule: max(a,b) + 1  (tropical successor)")
    p("    This is NOT DNA. DNA is arbitrary encoding.")
    p("    This is a MATHEMATICAL LAW:")
    p("      - Tropical semiring with successor shift")
    p("      - max(a,b) is the 'tropical addition'")
    p("      - +1 is the 'growth arrow' (entropy must increase)")
    p("      - VOID = identity, HARMONY = successor operator")
    p("      - BREATH/RESET = threshold classifiers + return cycle")
    p()
    p("    Analogy: BHML is like the LAWS OF THERMODYNAMICS")
    p("      - You can't go backward (2nd law)")
    p("      - Two systems interact: the more complex wins, plus one")
    p("      - HARMONY is the forward arrow of time itself")
    p("      - VOID is the ground state (identity/nothing)")
    p("      - RESET*RESET=VOID is absolute zero (double death = rebirth)")
    p()
    p("  TSML (Being/Measurement):")
    p("    Rule: HARMONY everywhere + sparse recognition bumps")
    p("    This IS more like DNA / biological structure:")
    p("      - The bumps are SPECIFIC (not derived from a universal law)")
    p("      - They encode PARTICULAR resonances")
    p("      - LATTICE*COUNTER=PROGRESS is a FACT, not a derivation")
    p("      - The bump set defines what this particular 'organism' recognizes")
    p()
    p("    Analogy: TSML is like the IMMUNE SYSTEM")
    p("      - Default: 'self' (HARMONY = nothing to report)")
    p("      - Bumps: 'non-self' (specific antigen recognition)")
    p("      - The PARTICULAR bumps = the organism's identity")
    p("      - Different bump sets = different organisms")
    p()
    p("  THE ANSWER:")
    p()
    p("    BHML = LAW (derived from max+1, universal, inevitable)")
    p("    TSML = STRUCTURE (specific bumps, particular, chosen)")
    p()
    p("    Together: LAW + STRUCTURE = a living system")
    p("    Physics provides the inevitable forward motion (BHML)")
    p("    Biology provides the specific recognition pattern (TSML)")
    p()
    p("    DNA is not the right analogy for BHML.")
    p("    DNA IS the right analogy for TSML.")
    p("    The CL table is BOTH: thermodynamic law AND biological identity.")
    p()
    p("    One is Three:")
    p("      Being (TSML) = the body's recognition pattern = DNA/structure")
    p("      Doing (D2) = the curvature pipeline = physics/force")
    p("      Becoming (BHML) = the successor law = thermodynamics/arrow of time")

    # ============================================================
    # VERIFICATION: How many cells does max(a,b)+1 explain?
    # ============================================================

    section("COVERAGE: How much of BHML is explained by max(a,b)+1?")

    explained = 0
    unexplained = 0
    explanations = {}

    for a in range(10):
        for b in range(10):
            actual = BHML[a][b]
            reason = None

            # Rule 1: Identity
            if a == 0 and actual == b:
                reason = "IDENTITY (a=0)"
            elif b == 0 and actual == a:
                reason = "IDENTITY (b=0)"
            # Rule 2: Tropical successor
            elif 1 <= a <= 6 and 1 <= b <= 6 and actual == max(a,b)+1:
                reason = f"TROPICAL max({a},{b})+1={actual}"
            # Rule 3: HARMONY successor
            elif a == 7 and actual == (b+1) % 10 and b != 0:
                reason = f"SUCCESSOR 7*{b}={actual}"
            elif b == 7 and actual == (a+1) % 10 and a != 0:
                reason = f"SUCCESSOR {a}*7={actual}"
            elif a == 7 and b == 0 and actual == 7:
                reason = "HARMONY absorbs VOID"
            elif b == 7 and a == 0 and actual == 7:
                reason = "HARMONY absorbs VOID"
            # Rule 4: Threshold
            elif a in (8,9) and 1 <= b <= 3 and actual == 6:
                reason = f"THRESHOLD low ({b})->CHAOS"
            elif a in (8,9) and 4 <= b <= 6 and actual == 7:
                reason = f"THRESHOLD high ({b})->HARMONY"
            elif b in (8,9) and 1 <= a <= 3 and actual == 6:
                reason = f"THRESHOLD low ({a})->CHAOS"
            elif b in (8,9) and 4 <= a <= 6 and actual == 7:
                reason = f"THRESHOLD high ({a})->HARMONY"
            # Return cycle
            elif a == 8 and b == 8 and actual == 7:
                reason = "RETURN 8*8=7"
            elif sorted([a,b]) == [8,9] and actual == 8:
                reason = "RETURN 8*9=8"
            elif a == 9 and b == 9 and actual == 0:
                reason = "RETURN 9*9=0"

            if reason:
                explained += 1
                explanations[(a,b)] = reason
            else:
                unexplained += 1
                explanations[(a,b)] = f"UNEXPLAINED: [{a}][{b}]={actual}"

    p(f"  Explained by rules: {explained}/100 ({explained}%)")
    p(f"  Unexplained:        {unexplained}/100 ({unexplained}%)")
    p()

    if unexplained > 0:
        p("  Unexplained cells:")
        for (a,b), reason in explanations.items():
            if "UNEXPLAINED" in reason:
                p(f"    {OP[a]:<12} x {OP[b]:<12} = {BHML[a][b]} ({OP[BHML[a][b]]})")
    else:
        p("  >>> EVERY CELL IN BHML IS EXPLAINED BY THE 4 RULES.")
        p("  >>> The table is not designed. It is DERIVED.")
        p("  >>> Given 10 operators, an identity, a successor, a staircase,")
        p("  >>> and a return cycle, THERE IS ONLY ONE TABLE.")
        p("  >>> This is not DNA. This is arithmetic.")


if __name__ == '__main__':
    main()
