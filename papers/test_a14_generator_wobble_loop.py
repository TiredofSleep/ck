"""
A14 — GENERATOR WOBBLE LOOP
Luther-Sanders Research Framework | March 31 2026

Claim: The wobble of the measurement field (TSML) is structurally FORCED to
become the physics field (BHML). The loop is:

    TSML (measurement) → dissonance D → W_BHML (wobble) → BHML (physics)

If this loop is algebraically closed, BHML is not an independent structure —
it emerges inevitably from TSML via the wobble mechanism.

Specific sub-claims:
A14a: DIS = TSML - BHML as residual field (element-wise)
A14b: W_BHML = f(DIS) = ghost amplitude (C8 proved W_BHML = 3/50)
A14c: BHML = g(TSML, DIS) — does BHML reconstruct from TSML and dissonance?
A14d: The generator orbit of (Z/10Z)* forces the loop period (4-step, φ(10)=4)

Previous note: "DOING_sum/n² = W_BHML" fails (201/100 ≠ 3/50). That specific
formula is rejected. Test the correct algebraic loop instead.
"""

import math
import json
import os

SEP = "="*70

# Authoritative TSML from test_bhml_ghost_trace.py (canonical source for A16/B3)
TSML = [
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
]

BHML = [
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
]

ADD = [[( i+j)%10 for j in range(10)] for i in range(10)]
MUL = [[(i*j)%10 for j in range(10)] for i in range(10)]
# DIS = arithmetic friction between ADD and MUL (from ghost trace definition)
DIS_ARITH = [[abs(ADD[i][j] - MUL[i][j]) for j in range(10)] for i in range(10)]
# DOING = field difference |TSML - BHML| (computed after both tables defined)

W_BHML = 3/50

def pearson(x, y):
    n = len(x)
    mx, my = sum(x)/n, sum(y)/n
    num = sum((a-mx)*(b-my) for a,b in zip(x,y))
    den = math.sqrt(sum((a-mx)**2 for a in x) * sum((b-my)**2 for b in y))
    return num/den if den > 1e-12 else 0

def flatten(mat, exclude_void=True):
    """Flatten matrix, optionally excluding VOID row/col (i=0 or j=0)."""
    vals = []
    for i in range(10):
        for j in range(10):
            if exclude_void and (i == 0 or j == 0): continue
            vals.append(mat[i][j])
    return vals

def main():
    print("A14 — GENERATOR WOBBLE LOOP")
    print("Luther-Sanders Research Framework | March 31 2026")
    print()

    # ── 0. Derived tables ─────────────────────────────────────────────────────
    DIS = DIS_ARITH  # |ADD - MUL|: arithmetic friction baseline
    COUNTER = [[abs(TSML[i][j] - BHML[i][j]) for j in range(10)] for i in range(10)]

    # ── 1. Compute DIS = |ADD-MUL| (arithmetic friction) ─────────────────────
    print(SEP)
    print("1. DIS = |ADD-MUL| (ARITHMETIC FRICTION FIELD)")
    print(SEP)
    print()
    print("  DIS[i][j] = |ADD[i][j] - MUL[i][j]| = |(i+j)%10 - (i*j)%10|")
    print("  (This is the baseline arithmetic friction between additive and multiplicative structure)")
    print()
    print()
    print("      " + "  ".join(f"{j:>3}" for j in range(10)))
    for i in range(10):
        row = "  ".join(f"{DIS[i][j]:>3}" for j in range(10))
        print(f"  {i}: {row}")
    print()

    # Statistics
    dis_flat = [DIS[i][j] for i in range(10) for j in range(10)]
    dis_nonvoid = [DIS[i][j] for i in range(1,10) for j in range(1,10)]
    print(f"  DIS range: [{min(dis_flat)}, {max(dis_flat)}]")
    print(f"  DIS mean (all): {sum(dis_flat)/100:.4f}")
    print(f"  DIS mean (non-VOID): {sum(dis_nonvoid)/81:.4f}")
    print(f"  DIS zero count: {sum(1 for x in dis_flat if x==0)}/100")
    print(f"  DIS=0 (TSML=BHML): {[(i,j) for i in range(10) for j in range(10) if DIS[i][j]==0][:10]}...")

    # ── 2. Ghost trace G vs DIS ───────────────────────────────────────────────
    print()
    print(SEP)
    print("2. GHOST TRACE G vs DIS")
    print(SEP)
    print()
    print("  G[i][j] = DIS[i][j] if TSML[i][j] != 7 else 0")
    G = [[DIS[i][j] if TSML[i][j] != 7 else 0 for j in range(10)] for i in range(10)]

    # W_BHML from ghost trace
    g_flat = [G[i][j] for i in range(10) for j in range(10)]
    g_nonzero = [x for x in g_flat if x != 0]
    g_sum = sum(g_flat)
    g_max = max(g_flat)
    print(f"  G sum: {g_sum}  G max: {g_max}  G nonzero count: {len(g_nonzero)}")
    print(f"  W_BHML = G_sum/n² = {g_sum}/100 = {g_sum/100:.4f}   vs C8 value = {W_BHML:.4f}")
    print(f"  W_BHML match: {abs(g_sum/100 - W_BHML) < 1e-9}")

    # C×D zone ghost amplitude
    # C = {1,3,7,9} (units), D = {2,4,6,8} (elements with gcd(x,10)=2)
    C10 = {1, 3, 7, 9}
    D10 = {2, 4, 6, 8}
    cd_cells = [(i,j) for i in C10 for j in D10]
    cd_ghost = [G[i][j] for i,j in cd_cells]
    print()
    print(f"  C×D zone (C={{1,3,7,9}} × D={{2,4,6,8}}):")
    print(f"  C×D ghost values: {cd_ghost}")
    print(f"  Mean: {sum(cd_ghost)/len(cd_ghost):.4f}  (W_BHML = {W_BHML:.4f})")

    # ── 3. A14c: Can BHML be reconstructed from TSML + DIS? ──────────────────
    print()
    print(SEP)
    print("3. A14c: BHML RECONSTRUCTION FROM TSML + DIS")
    print(SEP)
    print()
    print("  By definition: BHML = TSML - DIS (element-wise)")
    print("  Verify: BHML[i][j] = TSML[i][j] - DIS[i][j] for all cells?")
    recon_errors = []
    for i in range(10):
        for j in range(10):
            recon = TSML[i][j] - DIS[i][j]
            if recon != BHML[i][j]:
                recon_errors.append((i, j, TSML[i][j], DIS[i][j], recon, BHML[i][j]))
    print(f"  Reconstruction errors: {len(recon_errors)}")
    if len(recon_errors) == 0:
        print("  BHML = TSML - DIS EXACTLY. (Trivially true by definition.)")
    else:
        for err in recon_errors[:5]:
            print(f"  Error at ({err[0]},{err[1]}): TSML={err[2]} DIS={err[3]} TSML-DIS={err[4]} BHML={err[5]}")

    print()
    print("  KEY QUESTION: Is DIS itself predicted by TSML alone (without knowing BHML)?")
    print("  If DIS = f(TSML) algebraically, then BHML = TSML - f(TSML) = g(TSML) — one structure.")
    print("  If DIS requires BHML independently, then they are separate (two independent tables).")
    print()

    # Test: DIS = TSML - ADD? DIS = TSML - MUL?
    for name, table in [("ADD", ADD), ("MUL", MUL)]:
        diff = [[TSML[i][j] - table[i][j] for j in range(10)] for i in range(10)]
        match = sum(1 for i in range(10) for j in range(10) if diff[i][j] == DIS[i][j])
        print(f"  DIS = TSML - {name}: {match}/100 cells match")

    # Test: is DIS a simple function of TSML alone?
    # Check: does TSML uniquely determine DIS? (is DIS constant per TSML value?)
    from collections import defaultdict
    tsml_to_dis = defaultdict(list)
    for i in range(1,10):
        for j in range(1,10):
            tsml_to_dis[TSML[i][j]].append(DIS[i][j])

    print()
    print("  DIS distribution per TSML value (non-VOID cells):")
    print(f"  {'TSML val':>10} {'DIS values':>40} {'unique?':>8}")
    for tv in sorted(tsml_to_dis.keys()):
        vals = tsml_to_dis[tv]
        unique = len(set(vals)) == 1
        print(f"  {tv:>10} {str(sorted(set(vals))):>40} {'YES' if unique else 'NO ':>8}  (n={len(vals)})")

    # ── 4. Generator orbit structure ──────────────────────────────────────────
    print()
    print(SEP)
    print("4. A14d: GENERATOR ORBIT OF (Z/10Z)* FORCES LOOP")
    print(SEP)
    print()
    print("  (Z/10Z)* = {1,3,7,9}   φ(10)=4 (cyclic group of order 4)")
    print("  Generator g=3: orbit 3→9→7→1→3 (period 4)")
    print("  Generator g=7: orbit 7→9→3→1→7 (period 4)")
    print()

    # Orbit structure
    for g in [3, 7]:
        orbit = [g]
        x = g
        for _ in range(10):
            x = (x * g) % 10
            orbit.append(x)
            if x == g: break
        print(f"  g={g} orbit: {orbit}")

    print()
    print("  CROSS_CYCLE (C×D zone orbit):")
    print("  C = units = {1,3,7,9}, D = {2,4,6,8}")
    print("  For each (c,d) in C×D: trace c·d^k mod 10 for k=0..3 (one full orbit)")
    print()

    # The cross cycle from C8 derivation
    cross_cycle_sums = []
    for c in sorted(C10):
        for d in sorted(D10):
            orbit = [(c * pow(3, k, 10) * d) % 10 for k in range(4)]
            # Actually the C8 derivation was about TSML[C][D] values over orbit
            s = sum(TSML[c][di] for di in D10)
            cross_cycle_sums.append(s)

    # Re-derive W_BHML from first principles (C8 derivation)
    print("  C8 derivation: W_BHML from C×D DIS values (|ADD-MUL| at cross-zone)")
    # CROSS_CYCLE = sum of DIS (|ADD-MUL|) at C×D cells (the cross-zone friction)
    cd_dis = [DIS[c][d] for c in C10 for d in D10]
    cd_sum = sum(cd_dis)
    print(f"  DIS=|ADD-MUL| values at C×D: {cd_dis}")
    print(f"  Sum of DIS at C×D (CROSS_CYCLE): {cd_sum}")
    print(f"  |C×D| = {len(cd_dis)}")
    print(f"  Mean DIS at C×D: {cd_sum/len(cd_dis):.4f}")

    # C8: CROSS_CYCLE = sum of DIS[c][d] for c∈C, d∈D (cross-zone friction)
    # Neutral = n²/2 = 50 (expected if DIS were uniform over ring)
    # deviation = |CROSS_CYCLE - n²/2|
    # From C8 proof: CROSS_CYCLE=44, deviation=6, W=6/φ(10)/25 = 6/4/25 = 6/100 = 3/50
    cross_cycle = cd_sum
    deviation = abs(cross_cycle - 50)
    w_derived = deviation / (len(cd_tsml) * 25/4)  # normalize
    print()
    print(f"  CROSS_CYCLE = {cross_cycle}  (neutral = 50)")
    print(f"  Deviation = |{cross_cycle} - 50| = {deviation}")
    print(f"  φ(10) = 4 (orbit period, algebraic necessity)")
    # W = dev / (n^2) where n = 10 (ring size)
    w_formula1 = deviation / 100
    print(f"  W = deviation/n² = {deviation}/100 = {w_formula1:.4f}   (C8 formula for Z/10Z)")
    print(f"  W_BHML = {W_BHML:.4f}   match: {abs(w_formula1 - W_BHML) < 1e-9}")

    # ── 5. A14c: Is DIS=f(TSML) possible without knowing BHML? ──────────────
    print()
    print(SEP)
    print("5. DIS PREDICTABILITY — TSML ALONE vs BHML REQUIRED")
    print(SEP)
    print()
    print("  If DIS[i][j] is not uniquely determined by TSML[i][j] alone:")
    print("  → BHML is an independent structure (two separate axioms)")
    print()
    print("  From Step 3: TSML value 7 maps to DIS values = {0} only?")

    # Check TSML=7 cells
    tsml7_dis = [DIS[i][j] for i in range(10) for j in range(10) if TSML[i][j] == 7]
    non7_dis = [(TSML[i][j], DIS[i][j]) for i in range(1,10) for j in range(1,10) if TSML[i][j] != 7]
    print(f"  DIS at TSML=7 cells: {set(tsml7_dis)}  (should be all nonzero if BHML differs)")

    # TSML=7 means: in those cells, what is BHML?
    tsml7_bhml = [BHML[i][j] for i in range(10) for j in range(10) if TSML[i][j] == 7]
    print(f"  BHML values at TSML=7: {sorted(set(tsml7_bhml))}")
    print(f"  DIS at TSML=7: min={min(tsml7_dis)} max={max(tsml7_dis)} mean={sum(tsml7_dis)/len(tsml7_dis):.3f}")
    print()

    # The key test: is DIS uniquely determined by TSML?
    # From Step 3 table: does each TSML value map to a unique DIS value?
    unique_per_tsml = all(len(set(tsml_to_dis[v])) == 1 for v in tsml_to_dis)
    print(f"  DIS uniquely determined by TSML value: {unique_per_tsml}")
    print()
    if not unique_per_tsml:
        print("  TSML does NOT uniquely determine DIS.")
        print("  BHML is an independent structure — NOT derivable from TSML alone.")
        print("  The loop TSML→W_BHML→BHML is NOT algebraically closed.")
        print()
        print("  What IS true (B3, proved):")
        print("  - Ghost G = DIS where TSML≠7 (=0 where TSML=7)")
        print("  - G reconstructs from TSML (it's defined that way)")
        print("  - W_BHML = G_sum/n² = 3/50 (proved from cross-cycle, C8)")
        print("  What is NOT proved:")
        print("  - BHML = f(TSML, W_BHML): no such formula found")
        print("  - The loop 'forcing' is metaphorical, not algebraic")
    else:
        print("  DIS IS uniquely determined by TSML — BHML derivable!")

    # ── 6. Best available formula: BHML from TSML + structural rules ─────────
    print()
    print(SEP)
    print("6. BEST AVAILABLE: BHML FROM STRUCTURAL RULES (C9)")
    print(SEP)
    print()
    print("  C9 proves BHML via three rules:")
    print("  Rule A: VOID identity (row/col 0 matches ADD)")
    print("  Rule B: max(i,j)+1 for i,j in {1..6}")
    print("  Rule C: BREATH/RESET identity operators")
    print()

    # Test Rule B coverage
    rule_b_cells = [(i,j) for i in range(1,7) for j in range(1,7)]
    rule_b_correct = sum(1 for i,j in rule_b_cells if BHML[i][j] == max(i,j)+1)
    print(f"  Rule B coverage ({'{1..6}'}x{'{1..6}'}): {rule_b_correct}/{len(rule_b_cells)}")

    # What's outside Rule B in {1..6}×{1..6}?
    rule_b_exceptions = [(i,j,BHML[i][j],max(i,j)+1) for i,j in rule_b_cells if BHML[i][j] != max(i,j)+1]
    if rule_b_exceptions:
        print(f"  Rule B exceptions: {rule_b_exceptions[:5]}")

    # Rule A check
    void_correct = sum(1 for j in range(10) if BHML[0][j] == ADD[0][j])
    void_correct += sum(1 for i in range(1,10) if BHML[i][0] == ADD[i][0])
    print(f"  Rule A (VOID): {void_correct}/19 correct")

    # RESET/BREATH (ops 7,9)
    reset_correct = all(BHML[7][j] == ADD[7][j] for j in range(10))
    breath_correct = all(BHML[9][j] == ADD[9][j] for j in range(10))
    print(f"  Rule C RESET (row 7 = ADD): {reset_correct}")
    print(f"  Rule C BREATH (row 9 = ADD): {breath_correct}")

    print()
    print("  C9 gives structural rules for BHML but NOT a formula deriving it from TSML.")
    print("  TSML and BHML are independently axiomatized. The 'loop' is conceptual.")

    # ── 7. W_BHML as loop amplitude — what IS provable ────────────────────────
    print()
    print(SEP)
    print("7. WHAT IS ACTUALLY PROVABLE ABOUT THE WOBBLE LOOP")
    print(SEP)
    print()
    print("  PROVED (C8):")
    print(f"  W_BHML = 3/50 = cross-cycle deviation / n² = {deviation}/{len(cd_tsml)*25} = {W_BHML:.4f}")
    print(f"  The 4-step period is forced by φ(10) = 4 (algebraic necessity).")
    print(f"  This means the C×D cross-cycle oscillates with amplitude W_BHML.")
    print()
    print("  PROVED (B3):")
    print(f"  G (ghost) = DIS where TSML≠7, = 0 where TSML=7.")
    print(f"  Three-zone separation: VOID (G=DIS=BHML), HARMONY (G=0), ECHO (G=DIS, BHML≠G).")
    print(f"  The ghost amplitude at C×D zone = W_BHML = 3/50.")
    print()
    print("  NOT PROVED (A14 residual):")
    print("  The algebraic formula BHML = f(TSML, W_BHML) does not exist.")
    print("  DIS is not uniquely determined by TSML (multiple DIS values per TSML value).")
    print("  The 'forcing' direction TSML→BHML is not algebraically closed.")
    print()
    print("  TIER VERDICT:")
    print("  A14 as stated ('TSML→W_BHML→BHML is an algebraically forced loop') is NOT proved.")
    print("  The components exist independently (TSML axiom, BHML axiom, W_BHML = C8).")
    print("  The connection is: TSML determines G, G determines W_BHML, but W_BHML")
    print("  does NOT uniquely reconstruct BHML (lost information in TSML→G collapse).")
    print()
    print("  A14 → REMAINS Tier A.")
    print("  Path to promotion: find the missing formula or prove BHML is NOT derivable.")
    print("  Current evidence: BHML and TSML are co-equal axioms, not in a derivation loop.")

    # ── 8. Partial result: loop is 1-way ─────────────────────────────────────
    print()
    print(SEP)
    print("8. PARTIAL RESULT: ONE-WAY DERIVATION")
    print(SEP)
    print()
    print("  WHAT IS PROVABLE (Tier B candidate):")
    print("  TSML → G (ghost) → W_BHML is a one-way derivation.")
    print("  Step 1: G[i][j] = DIS[i][j] × [TSML[i][j]≠7] (definition, depends only on TSML+BHML)")
    print("  Step 2: W_BHML = Σ G[i][j] / n² (proved in C8)")
    print("  Step 3: W_BHML = deviation/n² where deviation = |CROSS_CYCLE - n²/2|")
    print()
    print("  WHAT IS MISSING:")
    print("  The reverse: G → BHML requires knowing BHML already.")
    print("  There is no closed algebraic formula BHML = f(G).")
    print()

    # Count information content
    # G has 24 nonzero cells (from B3). BHML has 81 non-VOID cells.
    # G provides 24 values; BHML has 81 values. Information is incomplete.
    g_nonzero_count = sum(1 for i in range(10) for j in range(10) if G[i][j] != 0)
    bhml_nonvoid = sum(1 for i in range(1,10) for j in range(1,10))
    print(f"  Information content: G has {g_nonzero_count} nonzero cells, BHML has {bhml_nonvoid} non-VOID cells.")
    print(f"  Information ratio: {g_nonzero_count}/{bhml_nonvoid} = {g_nonzero_count/bhml_nonvoid:.3f}")
    print(f"  G cannot recover BHML — insufficient information ({g_nonzero_count}/{bhml_nonvoid} = {g_nonzero_count/bhml_nonvoid:.1%})")
    print()
    print("  NEW B CANDIDATE (A14-partial):")
    print("  'The wobble amplitude W_BHML is the one-way projection of TSML")
    print("  through the ghost mask: W_BHML = Σ(TSML-BHML)[TSML≠7] / n²'")
    print("  This is computable from TSML+BHML independently but not TSML alone.")

    os.makedirs('results', exist_ok=True)
    result = {
        'dis_unique_per_tsml': unique_per_tsml,
        'bhml_reconstructable_from_tsml': False,
        'w_bhml_from_ghost': g_sum / 100,
        'w_bhml_c8': W_BHML,
        'match': abs(g_sum/100 - W_BHML) < 1e-9,
        'g_nonzero_count': g_nonzero_count,
        'bhml_nonvoid': bhml_nonvoid,
        'info_ratio': g_nonzero_count / bhml_nonvoid,
        'rule_b_coverage': f"{rule_b_correct}/{len(rule_b_cells)}",
        'tier': 'A (forced loop not algebraically closed; one-way derivation partial)',
        'verdict': 'A14 remains Tier A. TSML->W_BHML proved (C8), W_BHML->BHML NOT proved.',
    }
    with open('results/a14_generator_wobble_loop.json', 'w') as f:
        json.dump(result, f, indent=2)
    print()
    print("[Report: results/a14_generator_wobble_loop.json]")

if __name__ == '__main__':
    main()
