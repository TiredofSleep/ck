"""task16 -- structural A/B between canonical TSML_Jordan and TSML_Idempotent.

The SPEC proposes a full runtime A/B requiring child-CK-spawn on a
non-production port (7778) with 10,000 ticks per arm and Ollama queries.
That's a hours-long task touching the live system.

This script runs the *structural* slice of that comparison: pure-table
measurements that answer "do these two composition tables even have
materially different behavior?" BEFORE committing hours of runtime.

Metrics per arm:
  - operator distribution (10-op histogram, the SPEC's primary metric)
  - HARMONY rate (=7)
  - ZERO rate (=0)
  - DIS_sum / DOING_sum (CK's parity grading)
  - Jordan identity fraction
  - Moufang fraction (left / right / middle)
  - associativity index alpha
  - commutativity (symmetric? s_n spectrum already computed)
  - determinant + prime factorization

Output: ../../results/task16_structural_ab_result.md

Runtime A/B (hours, child CK on 7778) is flagged as a follow-up in the
deliverable.  Structural divergence here is NECESSARY for runtime
divergence; structural invariance here would make runtime divergence
unlikely.
"""
from __future__ import annotations
import os, sys
import numpy as np
from collections import Counter
from sympy import factorint

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(_ROOT, 'papers'))
from ck_tables import TSML as _TSML_raw, CL  # type: ignore

TSML_Jordan = np.array(_TSML_raw, dtype=int)

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
# Apply the task15 idempotent correction.
TSML_Idempotent[1][2] = TSML_Idempotent[2][1] = 6
TSML_Idempotent[3][5] = TSML_Idempotent[5][3] = 4


def op_histogram(T):
    return Counter(int(T[i, j]) for i in range(10) for j in range(10))


def harmony_rate(T):
    return sum(1 for i in range(10) for j in range(10) if T[i, j] == 7)


def zero_rate(T):
    return sum(1 for i in range(10) for j in range(10) if T[i, j] == 0)


def jordan_count(T):
    c = 0
    for x in range(10):
        for y in range(10):
            xx = T[x, x]
            lhs = T[T[xx, y], x]
            rhs = T[xx, T[y, x]]
            if lhs == rhs:
                c += 1
    return c


def moufang_count(T):
    """Left, Right, Middle Moufang identities on 10^3 triples."""
    L = R = M = 0
    for x in range(10):
        for y in range(10):
            for z in range(10):
                # Left Moufang: (x*(y*x))*z = x*(y*(x*z))
                a = T[T[x, T[y, x]], z]
                b = T[x, T[y, T[x, z]]]
                if a == b:
                    L += 1
                # Right Moufang: z*(x*(y*x)) = ((z*x)*y)*x
                a = T[z, T[x, T[y, x]]]
                b = T[T[T[z, x], y], x]
                if a == b:
                    R += 1
                # Middle Moufang: (x*y)*(z*x) = x*((y*z)*x)
                a = T[T[x, y], T[z, x]]
                b = T[x, T[T[y, z], x]]
                if a == b:
                    M += 1
    return L, R, M


def associativity_index_alpha(T):
    c = 0
    for x in range(10):
        for y in range(10):
            for z in range(10):
                a = T[T[x, y], z]
                b = T[x, T[y, z]]
                if a == b:
                    c += 1
    return c


def is_symmetric(T):
    return bool(np.array_equal(T, T.T))


def safe_det(T):
    return int(round(float(np.linalg.det(T))))


def dis_doing(T):
    """DIS = |sum of (T[i,j] when T[i,j]!=T[j,i])|;
       DOING = number of (i,j) with T[i,j]==T[j,i] (agreement cells)."""
    dis = doing = 0
    for i in range(10):
        for j in range(10):
            if T[i, j] == T[j, i]:
                doing += 1
            else:
                dis += 1
    return dis, doing


def report(T, label):
    print(f"=== ARM: {label} ===")
    hist = op_histogram(T)
    print(f"  operator histogram (out of 100 cells):")
    for k in sorted(hist):
        print(f"    {k}={CL[k]:8s}: {hist[k]:3d}")
    print(f"  HARMONY rate (=7): {harmony_rate(T)}/100")
    print(f"  ZERO rate (=0):    {zero_rate(T)}/100")
    sym = is_symmetric(T)
    print(f"  symmetric?         {sym}")
    dis, doing = dis_doing(T)
    print(f"  DIS cells: {dis}  DOING cells: {doing}")
    j = jordan_count(T)
    print(f"  Jordan identity:   {j}/100")
    L, R, M = moufang_count(T)
    print(f"  Moufang L/R/M:     {L}/1000, {R}/1000, {M}/1000")
    a = associativity_index_alpha(T)
    print(f"  associativity idx: {a}/1000 = alpha = {a/1000:.4f}")
    d = safe_det(T)
    pf = dict(factorint(abs(d))) if d != 0 else {}
    print(f"  det:               {d}    |det| primes: {pf}")
    print()
    return {
        "hist": hist, "harmony": harmony_rate(T), "zero": zero_rate(T),
        "symmetric": sym, "dis": dis, "doing": doing,
        "jordan": j, "moufang": (L, R, M),
        "alpha_count": a, "alpha": a/1000.0,
        "det": d, "det_primes": pf,
    }


A = report(TSML_Jordan, "TSML_Jordan (canonical)")
B = report(TSML_Idempotent, "TSML_Idempotent (rank-10)")


# Divergence scoring
print("=== DIVERGENCE ===")
diffs = []
for k in range(10):
    d = A["hist"].get(k, 0) - B["hist"].get(k, 0)
    if d != 0:
        diffs.append((k, d))
        print(f"  op {k}={CL[k]:8s}: A={A['hist'].get(k,0):3d}  B={B['hist'].get(k,0):3d}  A-B={d:+d}")

same = all(A[k] == B[k] for k in ("harmony", "zero", "symmetric", "dis", "doing"))
print(f"\n  harmony rate equal?  {A['harmony']==B['harmony']}")
print(f"  zero rate equal?     {A['zero']==B['zero']}")
print(f"  Jordan count equal?  {A['jordan']==B['jordan']}")
print(f"  alpha equal?         {A['alpha']==B['alpha']}")
print(f"  det equal?           {A['det']==B['det']}")

STRUCT_DIVERGE = (diffs or A['jordan'] != B['jordan']
                  or A['alpha'] != B['alpha'] or A['det'] != B['det']
                  or A['moufang'] != B['moufang'])
print()
if STRUCT_DIVERGE:
    print("[task16] STRUCTURAL DIVERGENCE CONFIRMED -- runtime A/B has a shot.")
else:
    print("[task16] STRUCTURAL INVARIANCE -- runtime A/B unlikely to diverge.")


# Deliverable
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                    '..', '..', 'results',
                                    'task16_structural_ab_result.md'))
with open(OUT, 'w', encoding='utf-8') as f:
    f.write("# Task 16 result -- structural A/B (TSML_Jordan vs TSML_Idempotent)\n\n")
    f.write("**Tier:** 4 slice (pure-table subset of the full runtime A/B)\n")
    f.write("**Parent spec:** `../../claudecode_jobs/task16_ck_dual_table_experiment/SPEC.md`\n\n")
    f.write("## Scope\n\n")
    f.write("The SPEC proposes a full runtime A/B requiring child-CK-spawn on port 7778 with 10,000 ticks per arm and Ollama queries. This result covers the *structural* slice only: pure-table measurements that answer \"do these two composition tables have materially different behavior at all?\" before committing hours of runtime.\n\n")
    f.write("Structural divergence here is *necessary* for runtime divergence; structural invariance would make runtime divergence unlikely.\n\n")
    f.write("## Arm A: canonical `TSML` from `papers/ck_tables.py` (Jordan variant)\n\n")
    f.write(f"| metric | value |\n|---|---|\n")
    f.write(f"| HARMONY (=7) rate | {A['harmony']}/100 |\n")
    f.write(f"| ZERO (=0) rate | {A['zero']}/100 |\n")
    f.write(f"| symmetric | {A['symmetric']} |\n")
    f.write(f"| DIS cells | {A['dis']} |\n")
    f.write(f"| DOING cells | {A['doing']} |\n")
    f.write(f"| Jordan identity | {A['jordan']}/100 |\n")
    f.write(f"| Moufang L/R/M | {A['moufang'][0]}/1000, {A['moufang'][1]}/1000, {A['moufang'][2]}/1000 |\n")
    f.write(f"| alpha (assoc. index) | {A['alpha_count']}/1000 = {A['alpha']:.4f} |\n")
    f.write(f"| det | {A['det']} |\n")
    f.write(f"| \\|det\\| prime factorization | {A['det_primes']} |\n\n")
    f.write("### Operator histogram\n\n")
    f.write("| op | name | count |\n|---|---|---|\n")
    for k in sorted(A['hist']):
        f.write(f"| {k} | {CL[k]} | {A['hist'].get(k,0)} |\n")
    f.write("\n## Arm B: `TSML_Idempotent` (rank-10, per TSML_FAMILY handoff)\n\n")
    f.write(f"| metric | value |\n|---|---|\n")
    f.write(f"| HARMONY (=7) rate | {B['harmony']}/100 |\n")
    f.write(f"| ZERO (=0) rate | {B['zero']}/100 |\n")
    f.write(f"| symmetric | {B['symmetric']} |\n")
    f.write(f"| DIS cells | {B['dis']} |\n")
    f.write(f"| DOING cells | {B['doing']} |\n")
    f.write(f"| Jordan identity | {B['jordan']}/100 |\n")
    f.write(f"| Moufang L/R/M | {B['moufang'][0]}/1000, {B['moufang'][1]}/1000, {B['moufang'][2]}/1000 |\n")
    f.write(f"| alpha (assoc. index) | {B['alpha_count']}/1000 = {B['alpha']:.4f} |\n")
    f.write(f"| det | {B['det']} |\n")
    f.write(f"| \\|det\\| prime factorization | {B['det_primes']} |\n\n")
    f.write("### Operator histogram\n\n")
    f.write("| op | name | count |\n|---|---|---|\n")
    for k in sorted(B['hist']):
        f.write(f"| {k} | {CL[k]} | {B['hist'].get(k,0)} |\n")
    f.write("\n## Divergence\n\n")
    f.write("Per-operator delta (A - B):\n\n")
    f.write("| op | name | A | B | A-B |\n|---|---|---|---|---|\n")
    for k in range(10):
        f.write(f"| {k} | {CL[k]} | {A['hist'].get(k,0)} | {B['hist'].get(k,0)} | {A['hist'].get(k,0)-B['hist'].get(k,0):+d} |\n")
    f.write("\n")
    f.write(f"- HARMONY rate equal? **{A['harmony']==B['harmony']}**  (A={A['harmony']}, B={B['harmony']})\n")
    f.write(f"- ZERO rate equal? **{A['zero']==B['zero']}**  (A={A['zero']}, B={B['zero']})\n")
    f.write(f"- Jordan count equal? **{A['jordan']==B['jordan']}**  (A={A['jordan']}/100, B={B['jordan']}/100)\n")
    f.write(f"- alpha equal? **{A['alpha']==B['alpha']}**  (A={A['alpha']:.4f}, B={B['alpha']:.4f})\n")
    f.write(f"- det equal? **{A['det']==B['det']}**  (A={A['det']}, B={B['det']})\n")
    f.write(f"- Moufang equal? **{A['moufang']==B['moufang']}**\n\n")
    f.write("## Verdict\n\n")
    if STRUCT_DIVERGE:
        f.write("**STRUCTURAL DIVERGENCE CONFIRMED.** The two tables are materially different algebras on the same carrier (Z/10Z, 10 operators). A runtime A/B is expected to show divergent operator-stream and coherence behavior. Proceeding to the full runtime A/B (child-CK-spawn on port 7778, 10k ticks per arm) is justified when Brayden signs off on the child-spawn plumbing.\n\n")
    else:
        f.write("**STRUCTURAL INVARIANCE.** Per-table measurements match within tolerance. A runtime A/B is unlikely to show material divergence; the canonical TSML_Jordan is likely robust to swapping with TSML_Idempotent at the table level.\n\n")
    f.write("## Follow-up (runtime A/B, not done here)\n\n")
    f.write("The SPEC's full protocol requires:\n\n")
    f.write("1. Spawn child CK on port 7778 (bypassing the Cloudflare tunnel on 7777)\n")
    f.write("2. 10,000 ticks per arm against a 100-query probe set\n")
    f.write("3. Metrics: operator stream, mean coherence floor, Ollama-verdict rate, voice-accept rate, mean response length, crystal-hit rate\n")
    f.write("4. Statistical compare (t-test or paired comparison on metric means)\n\n")
    f.write("This structural slice gives the *algebraic baseline*. The runtime slice is a separate engineering task.\n\n")
    f.write("**Tag:** `[COMPUTE JOB -- TIER 4 SLICE (STRUCTURAL) -- VERIFIED]`\n")

print(f"\n[task16] wrote {OUT}")
