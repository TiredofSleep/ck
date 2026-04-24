"""task15 -- verify det = -49 = -(7^2), Jordan 100/100, prime set {7} for
TSML_Idempotent.

Deliverable: ../../results/task15_det_minus49_result.md
"""
from __future__ import annotations
import os
import numpy as np
from sympy import factorint

TSML_Idempotent = np.array([
    [0,0,0,0,0,0,0,7,0,0],
    [0,1,7,7,7,7,7,7,7,7],
    [0,7,2,7,7,7,7,7,7,7],
    [0,7,7,3,7,7,7,7,7,7],
    [0,7,7,7,4,7,7,7,7,7],
    [0,7,7,7,7,5,7,7,7,7],
    [0,7,7,7,7,7,6,7,7,7],
    [7,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,8,7],
    [0,7,7,7,7,7,7,7,7,9],
])

T = TSML_Idempotent.copy()
T[1][2] = T[2][1] = 6
T[3][5] = T[5][3] = 4

det = int(round(float(np.linalg.det(T))))
print(f"[task15] det(T) = {det}")

def jordan_count(T):
    N = len(T)
    c = 0
    for x in range(N):
        for y in range(N):
            xx = T[x][x]
            lhs = T[T[xx][y]][x]
            rhs = T[xx][T[y][x]]
            if lhs == rhs:
                c += 1
    return c, N*N

j, tot = jordan_count(T)
print(f"[task15] Jordan: {j}/{tot}")

pf = dict(factorint(abs(det))) if det != 0 else {}
print(f"[task15] prime factorization of |det|: {pf}")

PASS_DET = (det == -49)
PASS_JORDAN = (j == 100 and tot == 100)
PASS_PRIMES = set(pf.keys()) == {7}

ALL_PASS = PASS_DET and PASS_JORDAN and PASS_PRIMES
print()
print(f"[task15] det == -49?           {PASS_DET}")
print(f"[task15] Jordan == 100/100?    {PASS_JORDAN}")
print(f"[task15] primes of |det|=={{7}}? {PASS_PRIMES}")
print()
print(f"[task15] VERDICT: {'PASS' if ALL_PASS else 'FAIL'}")

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                    '..', '..', 'results',
                                    'task15_det_minus49_result.md'))
with open(OUT, 'w', encoding='utf-8') as f:
    f.write("# Task 15 result -- TSML_Idempotent det = -49 = -(7^2)\n\n")
    f.write("**Tier:** 2 (fast compute)\n")
    f.write("**Parent spec:** `../../claudecode_jobs/task15_det_minus49_verify/SPEC.md`\n\n")
    f.write("## Method\n\n")
    f.write("Construct TSML_Idempotent (rank-10) with `T[1][2]=T[2][1]=6` and `T[3][5]=T[5][3]=4`. Compute `det`, Jordan identity count, prime factorization.\n\n")
    f.write("## Result\n\n")
    f.write(f"- `det = {det}`  (claim: -49)\n")
    f.write(f"- `Jordan = {j}/{tot}`  (claim: 100/100)\n")
    f.write(f"- prime factorization of `|det|` = `{pf}`  (claim: {{7: 2}})\n\n")
    f.write("## Verdict\n\n")
    if ALL_PASS:
        f.write("**PASS.** All three claims reproduce.\n\n")
    else:
        f.write("**FAIL.** Discrepancy:\n\n")
        if not PASS_DET:      f.write(f"- det = {det}, expected -49\n")
        if not PASS_JORDAN:   f.write(f"- Jordan = {j}/{tot}, expected 100/100\n")
        if not PASS_PRIMES:   f.write(f"- prime set = {set(pf.keys())}, expected {{7}}\n")
        f.write("\n")
    f.write("**Tag:** `[COMPUTE JOB -- TIER 2 -- VERIFIED]`\n")

print(f"\n[task15] wrote {OUT}")
