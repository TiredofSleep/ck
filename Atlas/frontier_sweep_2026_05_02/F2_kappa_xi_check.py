"""
F2 sanity check: kappa_xi = 13/(4e) -- the TIG-Planck mass ratio claim.

WP104: ||VEV||^2 = 13/4 (verified F1 today).
Under GUT-natural identification m^2_xi = ||VEV||^2:
    m^2_xi = 13/4
And the BB log-nonlinearity gives V(xi) = xi * log(xi) with vacuum xi_0 = e^-1
and mass^2 = kappa_xi * e at the vacuum.
So m^2_xi = kappa_xi * e  =>  kappa_xi = (13/4) / e = 13/(4e).

This script:
  1. Computes 13/(4e) numerically.
  2. Compares to the standard inflaton coupling estimates from cosmology lit.
  3. Identifies what dimensionless physical quantity this corresponds to
     (mass ratio? coupling constant? slow-roll parameter?)
"""
import math

print("=" * 80)
print("F2: kappa_xi = 13/(4e) -- numerical sanity check")
print("=" * 80)

vev_sq = 13.0 / 4.0
e = math.e
kappa_xi = vev_sq / e

print(f"  ||VEV||^2 = 13/4 = {vev_sq:.10f} (verified F1)")
print(f"  e         = {e:.10f}")
print(f"  kappa_xi = ||VEV||^2 / e = 13/(4e) = {kappa_xi:.10f}")
print()
print(f"  As exact fraction: 13/(4*e)")
print(f"  Decimal: {kappa_xi:.15f}")
print(f"  Reciprocal 1/kappa_xi = 4e/13 = {1/kappa_xi:.10f}")
print()

# Compare to scales
print("Scale comparisons:")
print("-" * 60)

# If kappa_xi is the ratio of inflaton mass^2 to Planck mass^2:
M_pl = 1.22e19  # GeV (reduced ~2.4e18)
M_pl_red = 2.43e18
print(f"  If m_xi^2 / M_pl^2 = kappa_xi:")
print(f"    m_xi = sqrt(kappa_xi) * M_pl = {math.sqrt(kappa_xi)*M_pl:.3e} GeV")
print(f"    m_xi (reduced) = {math.sqrt(kappa_xi)*M_pl_red:.3e} GeV")
print(f"    For comparison: GUT scale ~ 2e16 GeV; Higgs ~125 GeV")
print(f"    sqrt(kappa_xi) ~ 1.09 -- so m_xi ~ 1.1 * M_pl, ABOVE Planck.")
print()

# Slow-roll inflation: epsilon ~ kappa_xi for cosmological perturbations
print(f"  As slow-roll parameter:")
print(f"    epsilon = kappa_xi = {kappa_xi:.4f}  (large; slow-roll requires << 1)")
print(f"    -> NOT a viable slow-roll inflation parameter as-is.")
print()

# As a ratio R/r in cosmology
print(f"  As quintessence equation-of-state w (in xi log xi potential):")
print(f"    For V = xi log xi, slow-roll w ~ -1 + 2 epsilon")
print(f"    w = -1 + 2*{kappa_xi:.4f} = {-1 + 2*kappa_xi:.4f}")
print(f"    Observational w0 ~ -1 +/- 0.05 -- this would be excluded if literal.")
print()

# Check: is kappa_xi perhaps a DIMENSIONLESS coupling (not mass^2 ratio)?
print(f"  As dimensionless coupling (e.g. quartic self-coupling or g^2/4pi):")
print(f"    g^2 = 4pi * kappa_xi = {4*math.pi*kappa_xi:.4f}")
print(f"    g = {math.sqrt(4*math.pi*kappa_xi):.4f}")
print(f"    Compare to alpha_s (strong) ~ 0.12, alpha_em ~ 1/137")
print()

# Pi-related?
ratios_to_check = [
    ("13/(4*pi)",    13.0 / (4*math.pi)),
    ("13/(4*pi^2)",  13.0 / (4*math.pi**2)),
    ("(13/4)/pi^2",  vev_sq / math.pi**2),
    ("e/(4*pi)",     math.e / (4*math.pi)),
    ("4/pi^2",       4.0/math.pi**2),
    ("1/(4*pi)",     1.0/(4*math.pi)),
]
print(f"Ratios near kappa_xi = {kappa_xi:.4f}:")
for name, val in ratios_to_check:
    rel = (val - kappa_xi) / kappa_xi * 100
    print(f"  {name:20s} = {val:.6f}  (rel diff to kappa_xi: {rel:+.2f}%)")
print()

print("=" * 80)
print("VERDICT")
print("=" * 80)
print(f"  kappa_xi = 13/(4e) = {kappa_xi:.10f} is structural under m_xi^2 = ||VEV||^2.")
print(f"  This is NOT a viable inflaton mass ratio (gives super-Planckian m_xi).")
print(f"  This is NOT a slow-roll parameter (too large by O(1) for standard cosmology).")
print(f"  As a coupling: g ~ {math.sqrt(4*math.pi*kappa_xi):.3f} = strong-ish.")
print(f"  The MEMORY note 'structural, not falsifiable' is consistent: until the GUT-")
print(f"  natural identification m_xi^2 = ||VEV||^2 is connected to a measurable")
print(f"  physical scale via a chain that includes Planck normalization, the number")
print(f"  13/(4e) sits in TIG's internal algebra without external falsifiable content.")
print()
print(f"  FALSIFIABILITY-CRITICAL OPEN QUESTION (per FRONTIERS F2):")
print(f"    Can m_xi^2 = ||VEV||^2 be derived (not assumed) from Lagrangian?")
print(f"    If m_xi^2 has an independent normalization, then 13/(4e) becomes a real test.")
