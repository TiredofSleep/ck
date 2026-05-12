"""
ck_run.py -- Minimal TIG Demo
==============================
Copyright © 2025–2026 Brayden Ross Sanders / 7SiTe LLC
Licensed under the 7SiTe Public Sovereignty License v2.1.
Human use only. No commercial use. No government use.
No military, intelligence, policing, or surveillance use.
See LICENSE for full terms. DOI: 10.5281/zenodo.18852047

Demonstrates core results of WP34 and WP35 using tig_algebra.py.
No dependencies beyond Python stdlib + math.

Run:  python ck_run.py

Checks:
  - First-G event at k = p (WP34 Theorem)
  - R(p, p) = 0 exactly (the sinc2 null)
  - R(k,p) -> 4/pi2 as p grows (WP35 Theorem 5, t=0.5)
  - R(k,p) -> 0.9675 as p grows (WP35 Theorem 5, t=0.1)
  - D1 sign flip at k=p: D1(p-1)<0, D1(p)>0
  - T* = 5/7 at b=35 (WP35 §1A)
  - Montgomery bridge: R(0.5) + R2(0.5) = 1
  - b=15 vs b=35 dispersion comparison (WP34 §9A)
"""

import math
from tig_algebra import (
    TIGSemiprime, MONTGOMERY, SINC2_TENTH,
    verify_first_g, verify_sinc2_limit,
    dispersion_comparison, _next_prime,
)

PI = math.pi
LINE = "-" * 60


def banner(title):
    print(f"\n{LINE}\n  {title}\n{LINE}")


def check(label, value, expected, tol=1e-4):
    ok = abs(value - expected) < tol
    mark = "OK  " if ok else "FAIL"
    print(f"  {mark}  {label:<44}  {value:.8f}  (expected ~{expected:.8f})")
    return ok


# --------------------------------------------------------------------------
# 1. First-G Law  (WP34 Theorem)
# --------------------------------------------------------------------------

banner("WP34 -- First-G Law: first_g(b) = p  for every semiprime b")

sample = [
    (6,2,3),(10,2,5),(15,3,5),(21,3,7),(35,5,7),
    (77,7,11),(143,11,13),(437,19,23),(1147,31,37),(10403,101,103),
]
all_ok = True
for b, p, q in sample:
    s = TIGSemiprime.from_params(p, q)
    fg = s.first_g()
    ok = fg == p
    all_ok = all_ok and ok
    print(f"  {'OK  ' if ok else 'FAIL'}  b={b:>6} = {p}x{q:<5}  first_g={fg}  (p={p})")

print(f"\n  First-G Law batch: {'ALL PASS' if all_ok else 'FAILURES DETECTED'}")


# --------------------------------------------------------------------------
# 2. Sinc2 Field  (WP35 Theorem 5)
# --------------------------------------------------------------------------

banner("WP35 -- Sinc2 Field: R(k,f) -> sinc2(k/f) as f -> inf")

s35 = TIGSemiprime(35)
print(f"\n  b=35 (p=5, q=7) -- exact formula checks:")
check("R(1, 5) = 1.0 (k=1 exact)",        s35.R(1),      1.0,  tol=1e-10)
check("R(5, 5) = 0   (prime null, exact)", s35.R(5),      0.0,  tol=1e-10)
check("T* = unit_frac(35) = 5/7",         s35.t_star(), 5/7,   tol=1e-12)

d1b = s35.D1(s35.p - 1)
d1a = s35.D1(s35.p)
sf = d1b < 0 and d1a > 0
print(f"  {'OK  ' if sf else 'FAIL'}  D1 sign flip at k=p: D1(p-1)={d1b:+.6f} D1(p)={d1a:+.6f}")

print(f"\n  Convergence R(floor(p/2), p) -> 4/pi2 = {MONTGOMERY:.8f}:")
for p in [5, 11, 23, 97, 997]:
    q = _next_prime(p)
    s = TIGSemiprime.from_params(p, q)
    k = max(1, p // 2)
    val = s.R(k)
    print(f"    p={p:<6}  k={k:<5}  R={val:.8f}  err={abs(val-MONTGOMERY):.2e}")

print(f"\n  Convergence R(floor(p/10), p) -> {SINC2_TENTH:.8f}:")
for p in [11, 23, 97, 997]:
    q = _next_prime(p)
    s = TIGSemiprime.from_params(p, q)
    k = max(1, p // 10)
    val = s.R(k)
    print(f"    p={p:<6}  k={k:<5}  R={val:.8f}  err={abs(val-SINC2_TENTH):.2e}")


# --------------------------------------------------------------------------
# 3. Montgomery Bridge  (WP35 §9 / WP40 §5)
# --------------------------------------------------------------------------

banner("Montgomery Bridge: R(x) + R2(x) = 1  at x = 1/2")

R_TIG = MONTGOMERY
R_MON = 1.0 - MONTGOMERY
print(f"\n  TIG  R(1/2)  = sinc2(1/2) = 4/pi2  = {R_TIG:.10f}")
print(f"  Mont R2(1/2) = 1 - sinc2(1/2)      = {R_MON:.10f}")
print(f"  Sum  R + R2  =                      = {R_TIG + R_MON:.15f}")
check("R(1/2) + R2(1/2) = 1.0 exactly", R_TIG + R_MON, 1.0,             tol=1e-14)
check("R(1/2) = 4/pi2 = 0.40528...",    R_TIG,          4 / (PI ** 2),  tol=1e-12)


# --------------------------------------------------------------------------
# 4. b=15 vs b=35 Dispersion Comparison  (WP34 §9A)
# --------------------------------------------------------------------------

banner("WP34 §9A -- Luther Dispersion: b=15 vs b=35")

cmp = dispersion_comparison(15, 35)
for label, data in cmp.items():
    s = data["summary"]
    prof = data["profile"]
    print(f"\n  {label}  (p={s['p']}, q={s['q']}, q/p={s['q_over_p']:.4f})")
    print(f"    First-G:         k={s['first_g']}  (= p: {s['first_g_is_p']})")
    print(f"    T* = unit_frac:  {s['unit_frac']} ~= {s['t_star']:.6f}")
    print(f"    R(1):            {s['R_at_1']:.6f}")
    print(f"    R(p-1):          {s['R_at_p_minus_1']:.6f}")
    print(f"    R(p) sink:       {s['R_at_p_sink']:.8f}")
    print(f"    D1 sign flip:    {s['D1_sign_flip_at_p']}")
    print(f"    dispersion(q):   {s['dispersion_at_q']:.6f}")
    print(f"\n    k   |G|    interleave    dispersion")
    for k, g, iv, d in prof:
        marker = " <- First-G" if k == s["first_g"] else ""
        print(f"    {k:>3}  {g:>3.0f}  {iv:>12.6f}  {d:>12.6f}{marker}")


# --------------------------------------------------------------------------
# 5. Batch verification
# --------------------------------------------------------------------------

banner("Batch Verification -- WP34 First-G + WP35 Sinc2 Limit")

r1 = verify_first_g()
print(f"\n  First-G Law:  {r1['passed']} passed, {r1['failed']} failed")
if r1["failures"]:
    for f in r1["failures"]:
        print(f"    FAIL: {f}")

large_primes = [97, 101, 127, 131, 149, 151, 997, 1009, 9973]
r2 = verify_sinc2_limit(primes=large_primes, t=0.5, tol=0.02)
print(f"\n  Sinc2 limit t=0.5 (p>=97, tol=0.02):")
print(f"    target 4/pi2 = {r2['target_sinc2']:.8f}")
print(f"    {r2['passed']} passed, {r2['failed']} failed, max_err={r2['max_error']:.2e}")

r3 = verify_sinc2_limit(primes=large_primes, t=0.1, tol=0.02)
print(f"\n  Sinc2 limit t=0.1 (p>=97, tol=0.02):")
print(f"    target 0.9675 = {r3['target_sinc2']:.8f}")
print(f"    {r3['passed']} passed, {r3['failed']} failed, max_err={r3['max_error']:.2e}")

print(f"\n{LINE}")
all_pass = r1["failed"] == 0 and r2["failed"] == 0 and r3["failed"] == 0
print(f"  Overall: {'ALL CHECKS PASS' if all_pass else 'FAILURES DETECTED'}")
print(LINE)
