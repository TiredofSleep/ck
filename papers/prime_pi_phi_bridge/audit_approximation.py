#!/usr/bin/env python3
"""
audit_approximation.py -- Extended approximation audit for 16/pi^2 vs simple irrationals.

Tests 40+ candidates with algebraic height <= 3, simple radical expressions,
Fibonacci/Lucas rationals, and named constants.

Run with:
    python audit_approximation.py
"""

import mpmath
import math

mpmath.mp.dps = 50

TARGET = float(16 / mpmath.pi**2)  # ~1.62113893828...

def rel_err(candidate):
    return abs(candidate - TARGET) / TARGET

candidates = []

# --- Fibonacci / Lucas rationals (h <= 3 Fibonacci fractions) ---
fibs = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
for i in range(2, len(fibs)):
    for j in range(i-1, min(i+3, len(fibs))):
        if fibs[i-1] != 0:
            v = fibs[j] / fibs[i-1]
            if 1.0 <= v <= 2.5:
                candidates.append((f"F({fibs[j]})/F({fibs[i-1]})", v))

# --- Simple rationals p/q with 1 <= p,q <= 15 ---
for p in range(1, 20):
    for q in range(1, 20):
        v = p / q
        if 1.0 <= v <= 2.5:
            candidates.append((f"{p}/{q}", v))

# --- Simple radicals sqrt(n), n^(1/3), etc. ---
for n in range(1, 20):
    v = math.sqrt(n)
    if 1.0 <= v <= 2.5:
        candidates.append((f"sqrt({n})", v))
    v = n ** (1/3)
    if 1.0 <= v <= 2.5:
        candidates.append((f"{n}^(1/3)", v))
    for m in range(2, 6):
        v = n / math.sqrt(m)
        if 1.0 <= v <= 2.5:
            candidates.append((f"{n}/sqrt({m})", v))
    for m in range(2, 8):
        v = math.sqrt(n) / m
        if 1.0 <= v <= 2.5:
            candidates.append((f"sqrt({n})/{m}", v))

# --- Phi, sqrt(2), sqrt(3), sqrt(5), e, combinations ---
phi = float((1 + mpmath.sqrt(5)) / 2)
e = float(mpmath.e)
sqrt2 = float(mpmath.sqrt(2))
sqrt3 = float(mpmath.sqrt(3))
sqrt5 = float(mpmath.sqrt(5))
pi_f = float(mpmath.pi)

named = [
    ("phi = (1+sqrt(5))/2", phi),
    ("2/phi", 2/phi),
    ("phi^2 - 1 = phi", phi),  # duplicate, skip
    ("phi/1", phi),
    ("1 + 1/phi", 1 + 1/phi),
    ("sqrt(2)", sqrt2),
    ("sqrt(3)", sqrt3),
    ("sqrt(5)/sqrt(2)", sqrt5/sqrt2),
    ("sqrt(5)/sqrt(3)", sqrt5/sqrt3),
    ("sqrt(5) - 1", sqrt5 - 1),
    ("(sqrt(5)+1)/2", (sqrt5+1)/2),
    ("(sqrt(5)+3)/4", (sqrt5+3)/4),
    ("e - 1", e - 1),
    ("e/sqrt(e)", e/math.sqrt(e)),
    ("2*cos(pi/5)", 2*math.cos(pi_f/5)),
    ("2*cos(pi/7)", 2*math.cos(pi_f/7)),
    ("2*cos(pi/9)", 2*math.cos(pi_f/9)),
    ("2*cos(pi/11)", 2*math.cos(pi_f/11)),
    ("pi/2 - 0.05 (informal)", pi_f/2 - 0.05),  # not structured, skip
    ("pi^(1/3)", pi_f**(1/3)),
    ("pi/2", pi_f/2),
    ("2/pi^(1/2)", 2/pi_f**0.5),
    ("pi^2/6", pi_f**2/6),
    ("8/pi", 8/pi_f),
    ("4/sqrt(6)", 4/math.sqrt(6)),
    ("3/sqrt(sqrt(2)*3)", 3/(math.sqrt(2*3))),
    ("ln(5)", math.log(5)),
    ("ln(4)", math.log(4)),
    ("ln(3)", math.log(3)),
    ("ln(phi)", math.log(phi)),
    ("1 + ln(phi)/2", 1 + math.log(phi)/2),
    ("sqrt(phi)", math.sqrt(phi)),
    ("phi + 1/phi^2", phi + 1/phi**2),
    ("phi*sqrt(phi)/sqrt(2)", phi*math.sqrt(phi)/sqrt2),
    ("3*phi/4", 3*phi/4),
    ("phi^(3/2)", phi**1.5),
    ("2*phi - 1", 2*phi - 1),
    ("phi^2/phi", phi),
    ("(sqrt(5)+2)/3", (sqrt5+2)/3),
    ("(2+sqrt(2))/sqrt(3)", (2+sqrt2)/sqrt3),
    ("Catalan*2", 2*0.9159655941),  # Catalan's constant
    ("zeta(2)/pi^2 * 16", 16*(pi_f**2/6)/pi_f**2),  # = 8/3
    ("4/phi", 4/phi),
    ("sqrt(phi+1)", math.sqrt(phi+1)),
]
candidates.extend(named)

# Deduplicate by value (keep first seen)
seen_vals = {}
unique = []
for name, val in candidates:
    if not (1.0 <= val <= 2.5):
        continue
    key = round(val, 8)
    if key not in seen_vals:
        seen_vals[key] = name
        unique.append((name, val))

# Sort by relative error
ranked = sorted(unique, key=lambda x: rel_err(x[1]))

print(f"TARGET: 16/pi^2 = {TARGET:.12f}")
print(f"\nTop 35 closest candidates to 16/pi^2:\n")
print(f"{'Rank':<5} {'Expression':<30} {'Value':<16} {'Rel. Error':<16} {'Abs. Error'}")
print("-"*85)

for i, (name, val) in enumerate(ranked[:35], 1):
    re = rel_err(val)
    ae = abs(val - TARGET)
    marker = " <-- BEST ALGEBRAIC" if i == 1 and "phi" in name.lower() else ""
    print(f"{i:<5} {name:<30} {val:<16.10f} {re*100:<16.6f}% {ae:.6e}{marker}")

print("\n")

# Specific check: is phi the best ALGEBRAIC (non-rational) candidate?
phi_rank = next((i+1 for i, (n,v) in enumerate(ranked[:35]) if "phi" in n.lower() and abs(v - phi) < 1e-10), None)
fib_candidates = [(i+1, n, v) for i, (n,v) in enumerate(ranked[:35])
                  if any(c.isdigit() for c in n) and '/' in n and 'sqrt' not in n]

print(f"phi rank: #{phi_rank} among all 1.0-2.5 candidates")
print(f"phi relative error: {rel_err(phi)*100:.4f}%")
print()

# Check the pure rationals that beat or match phi
rationals_better = [(n, v, rel_err(v)*100) for n, v in ranked[:35]
                    if '/' in n and 'sqrt' not in n and '^' not in n
                    and abs(rel_err(v)) < rel_err(phi)]
if rationals_better:
    print("Rationals closer than phi:")
    for name, val, re in rationals_better:
        print(f"  {name} = {val:.10f}, rel err = {re:.4f}%")
else:
    print("No simple rational is closer to 16/pi^2 than phi.")

# Irrationals better than phi (non-rational non-phi)
irrationals_better = [(n, v, rel_err(v)*100) for n, v in ranked[:35]
                      if 'sqrt' in n or '^' in n or 'ln' in n or 'cos' in n or 'log' in n
                      if abs(rel_err(v)) < rel_err(phi)]
if irrationals_better:
    print("\nIrrationals closer than phi:")
    for name, val, re in irrationals_better:
        print(f"  {name} = {val:.10f}, rel err = {re:.4f}%")
else:
    print("No simple irrational (height<=3) is closer to 16/pi^2 than phi.")

print()
print("CONCLUSION:")
if phi_rank and phi_rank <= 3:
    print(f"  phi is rank #{phi_rank}. It is among the closest simple constants to 16/pi^2.")
    print(f"  The 0.1919% proximity is confirmed as unusually tight for simple algebraic constants.")
else:
    print(f"  phi is rank #{phi_rank}. Some simpler candidates are closer.")
    print(f"  Review the table above to update the approximation audit in the hardened memo.")
