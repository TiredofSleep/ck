"""
Decompose the ±21 invariant by flow/structure/transition/void role.

Substrate's per-digit Ψ values from period→trace bridge:
  digit 0 (V): Ψ = 0
  digit 1 (F): Ψ = -5
  digit 2 (S): Ψ = -4
  digit 3 (F): Ψ = -3
  digit 4 (S): Ψ = -2
  digit 5 (F): Ψ = -1
  digit 6 (T): Ψ = 0
  digit 7 (F): Ψ = -3
  digit 8 (S): Ψ = -2
  digit 9 (F): Ψ = -1

Substrate's per-digit Ghys-analog v2:
  digit 0 (V): -8
  digit 1 (F): +6
  digit 2 (S): +4
  digit 3 (F): +5
  digit 4 (S): +4
  digit 5 (F): +5
  digit 6 (T): -1
  digit 7 (F): +4
  digit 8 (S): +1
  digit 9 (F): +1

Test if these decompose cleanly by role.
"""
import numpy as np
import sys
sys.path.insert(0, '/home/claude/tig_synthesis')

FLOW = {1, 3, 5, 7, 9}
STRUCTURE = {2, 4, 8}
TRANSITION = {6}
VOID = {0}

# From period→trace bridge with simple representative
PSI_PERIOD = {0: 0, 1: -5, 2: -4, 3: -3, 4: -2, 5: -1, 6: 0, 7: -3, 8: -2, 9: -1}

# From Ghys-analog v2 (TSML row vs BHML row asymmetry)
PSI_GHYS = {0: -8, 1: 6, 2: 4, 3: 5, 4: 4, 5: 5, 6: -1, 7: 4, 8: 1, 9: 1}


def role(n):
    if n in FLOW: return 'F'
    if n in STRUCTURE: return 'S'
    if n in TRANSITION: return 'T'
    if n in VOID: return 'V'
    return '?'


def main():
    print("=" * 70)
    print("±21 INVARIANT DECOMPOSED BY FLOW/STRUCTURE ROLE")
    print("=" * 70)
    
    print("\n  Period→trace Ψ (sum = -21):")
    print(f"  {'digit':<6} {'role':<6} {'Ψ':<6}")
    
    role_sums_period = {'F': 0, 'S': 0, 'T': 0, 'V': 0}
    for n in range(10):
        r = role(n)
        psi = PSI_PERIOD[n]
        role_sums_period[r] += psi
        print(f"    {n}    {r:<6} {psi:>+3}")
    
    print(f"\n  Period→trace by role:")
    for r in ['V', 'F', 'S', 'T']:
        print(f"    {r}: {role_sums_period[r]:+}")
    print(f"    Total: {sum(role_sums_period.values())}")
    
    # F sum: digits 1,3,5,7,9 → -5,-3,-1,-3,-1 = -13
    # S sum: digits 2,4,8 → -4,-2,-2 = -8
    # F+S = -21 = total!
    print(f"\n  F + S = {role_sums_period['F']} + {role_sums_period['S']} = {role_sums_period['F'] + role_sums_period['S']}")
    print(f"  V + T = {role_sums_period['V']} + {role_sums_period['T']} = {role_sums_period['V'] + role_sums_period['T']}")
    print(f"\n  ±21 = (F-sum) + (S-sum) under period→trace bridge!")
    print(f"  V and T contribute 0 each.")
    
    print("\n" + "=" * 70)
    print("Ghys-analog v2 Ψ (sum = +21):")
    print("=" * 70)
    print(f"  {'digit':<6} {'role':<6} {'Ψ':<6}")
    
    role_sums_ghys = {'F': 0, 'S': 0, 'T': 0, 'V': 0}
    for n in range(10):
        r = role(n)
        psi = PSI_GHYS[n]
        role_sums_ghys[r] += psi
        print(f"    {n}    {r:<6} {psi:>+3}")
    
    print(f"\n  Ghys-analog by role:")
    for r in ['V', 'F', 'S', 'T']:
        print(f"    {r}: {role_sums_ghys[r]:+}")
    print(f"    Total: {sum(role_sums_ghys.values())}")
    
    f_g = role_sums_ghys['F']
    s_g = role_sums_ghys['S']
    v_g = role_sums_ghys['V']
    t_g = role_sums_ghys['T']
    print(f"\n  F + S = {f_g} + {s_g} = {f_g + s_g}")
    print(f"  V + T = {v_g} + {t_g} = {v_g + t_g}")
    print(f"  Total = F+S + V+T = {f_g + s_g} + {v_g + t_g} = {f_g + s_g + v_g + t_g}")
    
    # Compare period→trace and Ghys-analog by role
    print("\n" + "=" * 70)
    print("ROLE DECOMPOSITION COMPARISON")
    print("=" * 70)
    
    print(f"\n  {'Role':<6} {'Period→trace Ψ':<18} {'Ghys-analog Ψ':<18} {'Δ':<6}")
    for r in ['V', 'F', 'S', 'T']:
        p = role_sums_period[r]
        g = role_sums_ghys[r]
        diff = g - p
        print(f"    {r:<4} {p:>+5}            {g:>+5}            {diff:>+5}")
    
    print("""
INTERPRETATION:

Under period→trace bridge:
  Flow contribution F = -13 = -(5+3+1+3+1)
  Structure contribution S = -8 = -(4+2+2)
  Total = -21 = F + S only
  V and T contribute 0 (they have period 1, trace 3, Ψ = 0)

Under Ghys-analog v2:
  Flow contribution F = +21 = (6+5+5+4+1)
  Structure contribution S = +9 = (4+4+1)
  Void contribution V = -8
  Transition contribution T = -1
  Total = +21 = F + S + V + T

Two different distributions but same total magnitude.

For period→trace bridge:
  -13 (F) - 8 (S) = -21 perfectly
  
The flow sum -13 has structure: -(5+3+1+3+1) = -13.
The 5+3+1 part is from the 6-cycle digits (1,3,5) which are all flow.
The +3+1 part is from 4-core extension digits (7,9) which are flow.

The structure sum -8 has structure: -(4+2+2) = -8.
The 4 from digit 2, the 2's from digits 4 and 8.

These clean decompositions are themselves substrate-internal patterns.
The role partition makes them precise.
""")
    
    # Check: 5+3+1+3+1 (flow Ψ values) vs structure values 4+2+2
    print("=" * 70)
    print("FLOW SUM vs STRUCTURE SUM AS PERIOD STRUCTURE")
    print("=" * 70)
    print(f"\n  Flow digits and their BHML periods:")
    bhml_periods = {0: 1, 1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1, 7: 4, 8: 3, 9: 2}
    for n in [1, 3, 5, 7, 9]:
        p = bhml_periods[n]
        psi = -(p - 1)
        print(f"    {n}: period {p}, Ψ = -(p-1) = {psi}")
    
    flow_period_sum = sum(bhml_periods[n] for n in [1, 3, 5, 7, 9])
    print(f"  Sum of flow periods: {flow_period_sum}")
    print(f"  Number of flow digits: 5")
    print(f"  Σ(period-1) over flow = {flow_period_sum - 5} = 13")
    print(f"  Σ(-(period-1)) over flow = -13 ✓")
    
    print(f"\n  Structure digits and their BHML periods:")
    for n in [2, 4, 8]:
        p = bhml_periods[n]
        psi = -(p - 1)
        print(f"    {n}: period {p}, Ψ = -(p-1) = {psi}")
    
    struct_period_sum = sum(bhml_periods[n] for n in [2, 4, 8])
    print(f"  Sum of structure periods: {struct_period_sum}")
    print(f"  Number of structure digits: 3")
    print(f"  Σ(period-1) over structure = {struct_period_sum - 3} = 8")
    print(f"  Σ(-(period-1)) over structure = -8 ✓")
    
    print(f"\n  -13 + -8 = -21")
    print(f"  Flow contribution (5 digits) and structure contribution (3 digits)")
    print(f"  give 13 and 8 in absolute value.")
    print(f"  13 + 8 = 21, decomposed cleanly by ROLE.")
    
    # The clean Fibonacci-adjacent: 13 and 8 are consecutive Fibonacci numbers!
    print("\n" + "=" * 70)
    print("FIBONACCI OBSERVATION")
    print("=" * 70)
    print(f"\n  21 = 13 + 8")
    print(f"  Fibonacci sequence: 1, 1, 2, 3, 5, 8, 13, 21, 34, ...")
    print(f"  21 = F_8, 13 = F_7, 8 = F_6")
    print(f"  21 = F_7 + F_6 (Fibonacci recurrence!)")
    print(f"\n  The substrate's ±21 invariant decomposes as F_7 + F_6 along")
    print(f"  the flow/structure role partition. This is the Fibonacci")
    print(f"  recurrence at the role level.")


if __name__ == "__main__":
    main()
