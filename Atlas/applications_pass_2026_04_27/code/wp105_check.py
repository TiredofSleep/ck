"""
Verify the key claims of WP105 directly:
1. The BREATH equation 2·Br = h² + 2·br·r + 2·br·v
2. The H/Br = 1+√3 ratio at α=1/2
3. The quartic x^4 + 4x^3 - x^2 + 2x - 2 = 0 with root r/br
4. The 4-core support claim
5. LMFDB 4.2.10224.1 cross-check via Tschirnhaus relation
"""
import numpy as np

# The two canonical tables from WP105 §1 (and FORMULAS §5/§6)
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
    [0,7,9,7,3,7,7,7,7,7],
])

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
])

def fuse(p, M):
    """p ⋆_M p, returns dist over output indices"""
    out = np.zeros(10)
    for a in range(10):
        for b in range(10):
            out[M[a,b]] += p[a] * p[b]
    return out

def F_alpha(p, alpha):
    """Mixing operator at weight alpha"""
    t = fuse(p, TSML)
    b = fuse(p, BHML)
    raw = alpha * t + (1 - alpha) * b
    return raw / raw.sum()

# Initialize uniformly on the 4-core {V, H, Br, R} = {0, 7, 8, 9}
p = np.zeros(10)
p[0] = p[7] = p[8] = p[9] = 0.25
print(f"Initial: {p}")

# Iterate
alpha = 0.5
for k in range(200):
    p_new = F_alpha(p, alpha)
    if np.max(np.abs(p_new - p)) < 1e-15:
        print(f"Converged at iter {k}")
        break
    p = p_new

p_star = p
print(f"Fixed point at α=1/2:")
print(f"  V    = {p_star[0]:.15f}")
print(f"  H    = {p_star[7]:.15f}")
print(f"  Br   = {p_star[8]:.15f}")
print(f"  R    = {p_star[9]:.15f}")
print(f"  B+S  = {p_star[5] + p_star[6]:.15e}  (should be ~0)")
print(f"  Other (1,2,3,4): {p_star[1]+p_star[2]+p_star[3]+p_star[4]:.15e}")
print(f"  Sum  = {p_star.sum():.15f}")

# Check H/Br = 1 + √3
v, h, br, r = p_star[0], p_star[7], p_star[8], p_star[9]
ratio_h_br = h / br
target = 1 + np.sqrt(3)
print(f"\nH/Br ratio test:")
print(f"  H/Br      = {ratio_h_br:.15f}")
print(f"  1+√3      = {target:.15f}")
print(f"  Residual  = {abs(ratio_h_br - target):.3e}")

# Check the quartic for r/br
zeta = r / br
quartic = zeta**4 + 4*zeta**3 - zeta**2 + 2*zeta - 2
print(f"\nQuartic test (R/Br):")
print(f"  R/Br = ζ = {zeta:.15f}")
print(f"  f(ζ) = ζ⁴ + 4ζ³ - ζ² + 2ζ - 2 = {quartic:.3e}")

# Verify the BREATH equation: 2·Br = h² + 2·br·r + 2·br·v
# Wait — let me re-read this. The paper states the BREATH equation but with α=1/2 mixing.
# At fixed point: br = (1/2)(TSML→8 contribution) + (1/2)(BHML→8 contribution), then renormalized.
# TSML cells with output 8: TSML[4,8] = TSML[8,4] = 8. So TSML→8 = 2·p_4·p_8 = 0 at fixed point (p_4=0).
# BHML cells with output 8: BHML[1,8]=6 NO. Let me find them.
breath_cells = [(a,b) for a in range(10) for b in range(10) if BHML[a,b]==8]
print(f"\nBHML cells producing 8 (BREATH): {breath_cells}")
# Should be (0,8), (8,0), (7,7), (8,9), (9,8), (8,8)? Let me list.
breath_cells_t = [(a,b) for a in range(10) for b in range(10) if TSML[a,b]==8]
print(f"TSML cells producing 8 (BREATH): {breath_cells_t}")

# Now check the BREATH balance at fixed point
# br_new (pre-normalize) = α·TSML(p,p)[8] + (1-α)·BHML(p,p)[8]
# We need: at fixed point, br = (raw_br)/Z
t_br = sum(p_star[a]*p_star[b] for a,b in breath_cells_t)
b_br = sum(p_star[a]*p_star[b] for a,b in breath_cells)
raw_br = 0.5 * t_br + 0.5 * b_br

# normalization Z = sum over all output indices
Z = 0.0
for c in range(10):
    t_c = sum(p_star[a]*p_star[b] for a in range(10) for b in range(10) if TSML[a,b]==c)
    b_c = sum(p_star[a]*p_star[b] for a in range(10) for b in range(10) if BHML[a,b]==c)
    Z += 0.5 * t_c + 0.5 * b_c

print(f"\nBREATH balance check:")
print(f"  TSML contribution to Br: {t_br:.10f}")
print(f"  BHML contribution to Br: {b_br:.10f}")
print(f"  Raw Br = α·T + (1-α)·B = {raw_br:.10f}")
print(f"  Z = {Z:.10f}")
print(f"  raw/Z = {raw_br/Z:.10f}")
print(f"  Br fixed point = {br:.10f}")
print(f"  Match: {np.isclose(raw_br/Z, br)}")

# Now test the analytic claim: 2·Br = h² + 2·br·r + 2·br·v
# This is supposed to hold at the fixed point.
LHS = 2 * br
RHS = h**2 + 2*br*r + 2*br*v
print(f"\nAnalytic BREATH equation: 2·Br = h² + 2·br·r + 2·br·v ?")
print(f"  LHS (2·Br):           {LHS:.10f}")
print(f"  RHS (h²+2br·r+2br·v): {RHS:.10f}")
print(f"  Match: {np.isclose(LHS, RHS)}")
