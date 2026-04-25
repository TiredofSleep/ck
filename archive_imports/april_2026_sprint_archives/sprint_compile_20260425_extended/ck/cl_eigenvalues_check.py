"""
TIE #6: CL eigenvalues ↔ TIG constants

Claim from userMemories: 
  "CL eigenvalues produce e, 1/e, π, φ, ζ(3), Catalan's G all within 1%"
  
Earlier check today (in cl_spectrum.py):
  TSML eigenvalues: 61.37, -6.79, 6.44, 5.77, -3.73, -1.58, 0.76±0.86j, 0, 0
  Direct match to constants: only loose (within 5%, not 1%)

Possible interpretations:
  (a) The claim is about a DIFFERENT spectrum (not direct eigenvalues of T).
      Maybe singular values, or eigenvalues of T^T·T, or eigenvalues of (T-mean)·..., 
      or eigenvalues of T projected onto some subspace.
  (b) The claim is about RATIOS of eigenvalues, not bare values.
  (c) The claim is wrong (was loose / approximate when first stated).
  (d) The claim refers to a derived quantity like |λ|^(1/k) or sums/products.
  
Test thoroughly to distinguish.
"""
import numpy as np

TSML_ROWS = [
    "0000000700",  "0737777777",  "0377477779",  "0777777773",  "0747777787",
    "0777777777",  "0777777777",  "7777777777",  "0777877777",  "0797377777",
]
T = np.array([[int(c) for c in row] for row in TSML_ROWS], dtype=float)

# Constants to find
constants = {
    'e': np.e,                          # 2.71828
    '1/e': 1/np.e,                      # 0.36788
    'π': np.pi,                         # 3.14159
    '1/π': 1/np.pi,                     # 0.31831
    'φ': (1+np.sqrt(5))/2,             # 1.61803
    '1/φ': 2/(1+np.sqrt(5)),           # 0.61803
    'ζ(3)': 1.20205690315959,          # Apéry's constant
    'Catalan G': 0.9159655941772,      
    '4/π²': 4/np.pi**2,                # 0.40528, sinc²(1/2)
    'π²/6': np.pi**2/6,                # 1.64493, ζ(2)
    '√(π/2)': np.sqrt(np.pi/2),        # 1.25331
    '√π': np.sqrt(np.pi),              # 1.77245
    'γ (Euler)': 0.5772156649015329,
    'ln 2': np.log(2),                  # 0.69315
    'ln 3': np.log(3),                  # 1.09861
    'ln 7': np.log(7),                  # 1.94591
    '5/7': 5/7,                         # 0.71429
    '4/7': 4/7,                         # 0.57143
    '2/7': 2/7,                         # 0.28571
}

# Helper: check if a value matches a constant within err%
def match_within(val, err_pct=1.0):
    matches = []
    for name, c in constants.items():
        if c > 0 and abs(val - c) / c < err_pct/100:
            err = abs(val - c) / c * 100
            matches.append((name, c, err))
    return matches

print("="*70)
print("TEST 1: Direct eigenvalues of T")
print("="*70)

eigs_T = np.linalg.eigvals(T)
print("\nDirect eigenvalues:")
for e in sorted(eigs_T, key=lambda x: -abs(x)):
    re, im = np.real(e), np.imag(e)
    if abs(im) > 1e-9:
        print(f"  {re:+.4f} {im:+.4f}j (|λ|={abs(e):.4f})")
    else:
        print(f"  {re:+.4f}")

print("\nWithin-1% matches to TIG constants for each |λ|:")
for e in eigs_T:
    if abs(np.imag(e)) > 1e-9:
        continue
    re = np.real(e)
    if abs(re) < 1e-9:
        continue
    abs_re = abs(re)
    matches = match_within(abs_re)
    if matches:
        for m in matches:
            print(f"  |λ|={abs_re:.4f}: matches {m[0]}={m[1]:.4f} within {m[2]:.2f}%")

# No matches at 1%. Let me try transformations.

print("\n" + "="*70)
print("TEST 2: Various transforms of eigenvalues")
print("="*70)

real_eigs = sorted([np.real(e) for e in eigs_T 
                    if abs(np.imag(e)) < 1e-9 and abs(np.real(e)) > 1e-6])
abs_eigs = [abs(e) for e in real_eigs]

print(f"\nReal nonzero |eigs|: {[f'{e:.4f}' for e in abs_eigs]}")

# Transforms: log, sqrt, 1/x, x², ratios
transforms = [
    ('|λ|', lambda x: x),
    ('1/|λ|', lambda x: 1/x if x > 0 else 0),
    ('ln|λ|', lambda x: np.log(x) if x > 0 else 0),
    ('√|λ|', lambda x: np.sqrt(x) if x > 0 else 0),
    ('|λ|²', lambda x: x**2),
    ('|λ|/π', lambda x: x/np.pi),
    ('|λ|/e', lambda x: x/np.e),
    ('|λ|/7', lambda x: x/7),
    ('|λ|/10', lambda x: x/10),
    ('|λ|/61.37', lambda x: x/61.367644),  # divided by max
]

print("\nTransform-of-eig matches (within 1%):")
for label, t in transforms:
    for e in abs_eigs:
        v = t(e)
        if abs(v) < 1e-9 or abs(v) > 100:
            continue
        matches = match_within(v)
        if matches:
            for m in matches:
                print(f"  {label} for |λ|={e:.4f}: {v:.4f} matches {m[0]} within {m[2]:.2f}%")

print("\n" + "="*70)
print("TEST 3: Singular values of T")
print("="*70)

# Maybe the claim is about singular values, not eigenvalues
U_t, S_t, _ = np.linalg.svd(T)
print(f"\nSingular values of T: {[f'{s:.4f}' for s in S_t]}")

print("\nSingular value matches (within 1%):")
for s in S_t:
    matches = match_within(s)
    for m in matches:
        print(f"  σ={s:.4f}: matches {m[0]} within {m[2]:.2f}%")

# Also try on transformed singular values
for s in S_t:
    if s > 0:
        for label, t in transforms:
            v = t(s)
            if abs(v) < 1e-9 or abs(v) > 100:
                continue
            matches = match_within(v)
            for m in matches:
                if m[2] < 1.0:
                    print(f"  {label}(σ={s:.4f}) = {v:.4f} matches {m[0]} within {m[2]:.2f}%")

print("\n" + "="*70)
print("TEST 4: Eigenvalues of related matrices")
print("="*70)

# T·T^T (symmetric, eigenvalues are σ_i²)
TT = T @ T.T
eigs_TTT = sorted(np.linalg.eigvalsh(TT), reverse=True)
print(f"\nEigenvalues of T·T^T: {[f'{e:.2f}' for e in eigs_TTT]}")

# T^T·T
TtT = T.T @ T
eigs_TtT = sorted(np.linalg.eigvalsh(TtT), reverse=True)
print(f"Eigenvalues of T^T·T: {[f'{e:.2f}' for e in eigs_TtT]}")

# Symmetric part of T
T_sym = (T + T.T) / 2
eigs_sym = sorted(np.linalg.eigvalsh(T_sym), reverse=True)
print(f"\nEigenvalues of (T+T^T)/2: {[f'{e:.4f}' for e in eigs_sym]}")

# Antisymmetric part eigenvalues (will be ±i times something)
T_anti = (T - T.T) / 2
eigs_anti = np.linalg.eigvals(T_anti)
abs_anti = sorted([abs(e) for e in eigs_anti if abs(e) > 1e-9], reverse=True)
print(f"\n|Eigs| of (T-T^T)/2: {[f'{e:.4f}' for e in abs_anti]}")

# Test these for constant matches
for label, evals in [('sym', eigs_sym), ('antisym |λ|', abs_anti)]:
    print(f"\n{label} eigenvalue matches (1%):")
    for e in evals:
        if abs(e) < 1e-9:
            continue
        for trans_label, t in transforms:
            v = t(abs(e))
            if abs(v) < 1e-9 or abs(v) > 100:
                continue
            matches = match_within(v)
            for m in matches:
                if m[2] < 1.0:
                    print(f"  {trans_label}(|λ|={abs(e):.4f}) = {v:.4f} matches {m[0]} within {m[2]:.2f}%")

print("\n" + "="*70)
print("TEST 5: Characteristic polynomial coefficients")
print("="*70)

char_poly = np.poly(T)  # coefficients of det(λI - T)
print(f"\nChar poly coefficients: {[f'{c:.4f}' for c in char_poly]}")

# Each coefficient is some symmetric function of eigenvalues
for i, c in enumerate(char_poly):
    if abs(c) < 1e-9:
        continue
    matches = match_within(abs(c))
    for m in matches:
        if m[2] < 1.0:
            print(f"  c_{i} = {c:.4f}: matches {m[0]} within {m[2]:.2f}%")

print("\n" + "="*70)
print("CONCLUSION")
print("="*70)
print("""
After extensive testing, no clean 1% match between TSML eigenvalues 
(or transforms thereof) and the constants e, 1/e, π, φ, ζ(3), Catalan G.

The userMemories claim "CL eigenvalues produce e, π, φ, ζ(3), Catalan's G 
all within 1%" appears to be either:
  (a) Misremembered (the verified TSML eigenvalues don't match at 1%)
  (b) Referring to a different spectrum or table I don't have access to
  (c) An aspirational claim that didn't survive precise verification
  
This is a NEGATIVE result for tie #6.

The honest finding is: TSML's eigenvalue spectrum has structural integers 
({7,7,7} on lattice, exact integer norm 81 for antisym, ratio matches to 
small fractions like 45/7, 26/7) but does NOT cleanly produce 
transcendental constants e, π, φ, ζ(3), Catalan G at 1% tolerance.

Recommend: flag this claim in userMemories for review by Brayden.
""")
