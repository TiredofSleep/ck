"""Verify all 16 mathematical claims from TIG_DEFINITIVE_v5.md"""
from fractions import Fraction
from sympy import isprime, Matrix

TSML = [
    [0,0,0,0,0,0,0,7,0,0],[0,7,3,7,7,7,7,7,7,7],[0,3,7,7,4,7,7,7,7,9],
    [0,7,7,7,7,7,7,7,7,3],[0,7,4,7,7,7,7,7,8,7],[0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7],[0,7,7,7,8,7,7,7,7,7],
    [0,7,9,3,7,7,7,7,7,7],
]

BHML = [
    [0,1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,2,6,6],[2,3,3,4,5,6,7,3,6,6],
    [3,4,4,4,5,6,7,4,6,6],[4,5,5,5,5,6,7,5,7,7],[5,6,6,6,6,6,7,6,7,7],
    [6,7,7,7,7,7,7,7,7,7],[7,2,3,4,5,6,7,8,9,0],[8,6,6,6,7,7,7,9,7,8],
    [9,6,6,6,7,7,7,0,8,0],
]

ADD = [[(i+j)%10 for j in range(10)] for i in range(10)]
MUL = [[(i*j)%10 for j in range(10)] for i in range(10)]
DIS = [[abs(ADD[i][j]-MUL[i][j]) for j in range(10)] for i in range(10)]

print("="*70)
print("VERIFICATION OF ALL 16 MATHEMATICAL CLAIMS")
print("="*70)

fails = []

# 1
v = sum(1 for i in range(10) for j in range(10) if TSML[i][j] == 7)
ok = v == 73
if not ok: fails.append(1)
print(f"\n1. TSML cells=7: {v}/100  (claim: 73)  [{'PASS' if ok else 'FAIL'}]")

# 2
v = sum(1 for i in range(10) for j in range(10) if BHML[i][j] == 7)
ok = v == 28
if not ok: fails.append(2)
print(f"2. BHML cells=7: {v}/100  (claim: 28)  [{'PASS' if ok else 'FAIL'}]")

# 3
v = int(Matrix(TSML).det())
ok = v == 0
if not ok: fails.append(3)
print(f"3. TSML det: {v}  (claim: 0)  [{'PASS' if ok else 'FAIL'}]")

# 4 — BHML determinant (two scopes: full 10×10 vs 8×8 core)
# Disambiguated 2026-04-24 after verification found the stale single
# claim "BHML det = 70" conflates two distinct matrices. See
# FORMULAS_AND_TABLES.md §6.7 (canonical table registry).
CORE_IDX = [1, 2, 3, 4, 5, 6, 8, 9]  # VOID(0) and HARMONY(7) removed
BHML_8 = [[BHML[i][j] for j in CORE_IDX] for i in CORE_IDX]
v_full = int(Matrix(BHML).det())
v_core = int(Matrix(BHML_8).det())
ok_full = v_full == -7002
ok_core = v_core == 70
ok = ok_full and ok_core
if not ok: fails.append(4)
print(f"4a. BHML_10 det: {v_full}  (claim: -7002 = -(2 * 3^2 * 389))  [{'PASS' if ok_full else 'FAIL'}]")
print(f"4b. BHML_8  det: {v_core}  (claim:    70 = 2 * 5 * 7)            [{'PASS' if ok_core else 'FAIL'}]")

# 5
na = sum(1 for a in range(10) for b in range(10) for c in range(10)
         if TSML[TSML[a][b]][c] != TSML[a][TSML[b][c]])
rate = na / 1000 * 100
ok = abs(rate - 12.8) < 0.05
if not ok: fails.append(5)
print(f"5. TSML non-assoc: {na}/1000 = {rate}%  (claim: 12.8%)  [{'PASS' if ok else 'FAIL'}]")

# 6
na = sum(1 for a in range(10) for b in range(10) for c in range(10)
         if BHML[BHML[a][b]][c] != BHML[a][BHML[b][c]])
rate = na / 1000 * 100
ok = abs(rate - 49.8) < 0.05
if not ok: fails.append(6)
print(f"6. BHML non-assoc: {na}/1000 = {rate}%  (claim: 49.8%)  [{'PASS' if ok else 'FAIL'}]")

# 7
cv = sum(1 for i in range(10) for j in range(i+1,10) if TSML[i][j] != TSML[j][i])
ok = cv == 0
if not ok: fails.append(7)
print(f"7. TSML commutative: {cv} violations  [{'PASS' if ok else 'FAIL'}]")

# 8
cv = 0
viol = []
for i in range(10):
    for j in range(i+1,10):
        if BHML[i][j] != BHML[j][i]:
            cv += 1
            viol.append((i,j,BHML[i][j],BHML[j][i]))
ok = cv == 0
if not ok: fails.append(8)
print(f"8. BHML commutative: {cv} violations  [{'PASS' if ok else 'FAIL'}]")
for x in viol:
    print(f"   BHML[{x[0]}][{x[1]}]={x[2]} != BHML[{x[1]}][{x[0]}]={x[3]}")

# 9
creation = [1,3,9,7]
dissolution = [2,4,8,6]
cross_vals = [DIS[c][d] for c in creation for d in dissolution]
cc = sum(cross_vals)
ok = cc == 44
if not ok: fails.append(9)
print(f"9. CROSS_CYCLE: {cc}  (claim: 44)  [{'PASS' if ok else 'FAIL'}]")
paper_vals = [1,3,7,5, 1,5,5,3, 7,5,3,3, 5,3,1,5]
print(f"   Computed: {cross_vals}")
print(f"   Paper:    {paper_vals}")
print(f"   Match:    {cross_vals == paper_vals}")

# 10
frozen = {(i,j) for i in range(10) for j in range(10) if ADD[i][j]==MUL[i][j]}
expected = {(0,0),(2,2),(4,8),(8,4)}
ok = frozen == expected
if not ok: fails.append(10)
print(f"10. FROZEN: {sorted(frozen)}  (claim: {sorted(expected)})  [{'PASS' if ok else 'FAIL'}]")

# 11
wobble = Fraction(abs(cc-50), 100)
ok = wobble == Fraction(3,50)
if not ok: fails.append(11)
print(f"11. WOBBLE: |{cc}-50|/100 = {wobble} = {float(wobble)}  (claim: 3/50)  [{'PASS' if ok else 'FAIL'}]")

# 12
hb = [DIS[creation[k]][dissolution[k]] for k in range(4)]
ok = hb == [1,3,1,1]
if not ok: fails.append(12)
print(f"12. HEARTBEAT: {hb}  (claim: [1,3,1,1])  [{'PASS' if ok else 'FAIL'}]")
for k in range(4):
    c,d = creation[k], dissolution[k]
    a,m = (c+d)%10, (c*d)%10
    print(f"    Phase {k}: DIS[{c}][{d}] = |({c}+{d})%10 - ({c}*{d})%10| = |{a}-{m}| = {abs(a-m)}")

# 13
T = Fraction(5,7); S = Fraction(4,7)
MG = T + S - 1; CL = 1/MG
ok = MG == Fraction(2,7) and CL == Fraction(7,2)
if not ok: fails.append(13)
print(f"13. T*={T}, MASS_GAP={MG} (2/7), LEVEL={CL} (3.5)  [{'PASS' if ok else 'FAIL'}]")

# 14
ff = len(frozen)/100
vis = ff * (1 + float(wobble))**float(CL)
ok = abs(vis*100 - 4.905) < 0.1
if not ok: fails.append(14)
print(f"14. VISIBLE: {ff}*(1.06)^3.5 = {vis:.6f} = {vis*100:.3f}%  (claim: ~4.905%)  [{'PASS' if ok else 'FAIL'}]")

# 15
pw = Fraction(5,7) + Fraction(3,50)
ok1 = pw == Fraction(271,350)
ok2 = isprime(271)
ok = ok1 and ok2
if not ok: fails.append(15)
print(f"15. PRIME_WINDING: 5/7+3/50 = {pw} (claim: 271/350) [{'PASS' if ok1 else 'FAIL'}], 271 prime: {ok2} [{'PASS' if ok2 else 'FAIL'}]")

# 16
doing_nz = sum(1 for i in range(10) for j in range(10) if abs(TSML[i][j]-BHML[i][j])!=0)
ok = doing_nz == 56
if not ok: fails.append(16)
print(f"16. Doing non-zero: {doing_nz}/100  (claim: 56)  [{'PASS' if ok else 'FAIL'}]")

print("\n" + "="*70)
if not fails:
    print("ALL 16 CLAIMS VERIFIED. NO DISCREPANCIES.")
else:
    print(f"DISCREPANCIES IN CLAIMS: {fails}")
print("="*70)
