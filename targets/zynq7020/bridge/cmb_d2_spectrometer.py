#!/usr/bin/env python3
"""
cmb_d2_spectrometer.py -- Dual-Lens D2 Spectrometer for Cosmology
==================================================================

The universe as 5D force geometry.

CMB angular power spectrum, cosmic epochs, and cosmological parameters
mapped through the D2 pipeline. The universe's evolution IS a path
through 5D space. D2 IS the curvature of that path.

5D Force Mapping (cosmological observables):
  Aperture   = Baryon density (Omega_b)     -- matter openness/availability
  Pressure   = Dark matter density (Omega_c) -- gravitational pressure
  Depth      = Hubble constant (H0/100)     -- expansion depth/rate
  Binding    = Spectral index (n_s)         -- primordial binding correlations
  Continuity = Optical depth (tau)          -- photon continuity/scattering

This mapping is NOT arbitrary:
  Omega_b  = aperture: baryons ARE the aperture through which structure forms
  Omega_c  = pressure: dark matter IS the gravitational pressure well
  H0       = depth: expansion rate IS the depth of spacetime
  n_s      = binding: spectral index IS how primordial fluctuations bind
  tau      = continuity: optical depth IS photon continuity through reionization

CMB Acoustic Peaks:
  The first 7 acoustic peaks of the CMB power spectrum encode
  the D2 curvature of the early universe. Each peak is a resonance
  in the baryon-photon fluid -- curvature in 5D cosmological space.

Cosmic Epochs:
  Inflation -> Radiation -> Matter -> Reionization -> Dark Energy
  Each epoch IS a force vector. Transitions between epochs ARE D2 spikes.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import sys

# =====================================================================
# Constants
# =====================================================================
OP_NAMES = [
    "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"
]
DIM_NAMES = ["aperture", "pressure", "depth", "binding", "continuity"]
DIM_SHORT = ["ap", "pr", "dp", "bn", "cn"]

OP_MAP = {
    (0, True): 1, (0, False): 6,
    (1, True): 0, (1, False): 4,
    (2, True): 9, (2, False): 3,
    (3, True): 2, (3, False): 7,
    (4, True): 8, (4, False): 5,
}

OP_TO_DIM = {
    0: (1, "-pr"), 1: (0, "-ap"), 2: (3, "-bn"), 3: (2, "+dp"),
    4: (1, "+pr"), 5: (4, "+cn"), 6: (0, "+ap"), 7: (3, "+bn"),
    8: (4, "-cn"), 9: (2, "-dp"),
}

T_STAR = 5.0 / 7.0

BHML = [
    [0,1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,2,6,6],[2,3,3,4,5,6,7,3,6,6],
    [3,4,4,4,5,6,7,4,6,6],[4,5,5,5,5,6,7,5,7,7],[5,6,6,6,6,6,7,6,7,7],
    [6,7,7,7,7,7,7,7,7,7],[7,2,3,4,5,6,7,8,9,0],[8,6,6,6,7,7,7,9,7,8],
    [9,6,6,6,7,7,7,0,8,0],
]
TSML = [
    [0,0,0,0,0,0,0,7,0,0],[0,7,3,7,7,7,7,7,7,7],[0,3,7,7,4,7,7,7,7,9],
    [0,7,7,7,7,7,7,7,7,3],[0,7,4,7,7,7,7,7,8,7],[0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7],[0,7,7,7,8,7,7,7,7,7],
    [0,7,9,3,7,7,7,7,7,7],
]


# =====================================================================
# Cosmological Data
# =====================================================================

# Planck 2018 best-fit values (baseline, TT+TE+EE+lowE+lensing)
PLANCK_2018 = {
    "Omega_b": 0.0493,    # baryon density fraction
    "Omega_c": 0.265,     # cold dark matter density fraction
    "H0":      67.36,     # Hubble constant km/s/Mpc
    "n_s":     0.9649,    # scalar spectral index
    "tau":     0.0544,    # optical depth to reionization
}

# Normalization ranges for mapping to [0,1]
# Based on physically meaningful ranges from CMB constraints
NORM = {
    "Omega_b": (0.01, 0.10),     # baryon fraction range
    "Omega_c": (0.10, 0.50),     # CDM fraction range
    "H0":      (50.0, 100.0),    # Hubble constant range
    "n_s":     (0.90, 1.05),     # spectral index range
    "tau":     (0.01, 0.15),     # optical depth range
}

def normalize_cosmo(params):
    """Normalize cosmological parameters to [0,1] range."""
    keys = ["Omega_b", "Omega_c", "H0", "n_s", "tau"]
    v = []
    for k in keys:
        lo, hi = NORM[k]
        val = (params[k] - lo) / (hi - lo)
        val = max(0.0, min(1.0, val))
        v.append(val)
    return v

# =====================================================================
# CMB Acoustic Peak Data
# =====================================================================
# First 7 acoustic peaks of the CMB TT power spectrum
# Each peak has: multipole l, amplitude (uK^2), and the cosmological
# parameters that most influence it
#
# The sequence of peaks IS a path through parameter space.
# Odd peaks (1,3,5,7) are compression peaks (baryon-driven).
# Even peaks (2,4,6) are rarefaction peaks (radiation-driven).
# The ratio of odd/even amplitudes constrains Omega_b.

CMB_PEAKS = [
    {
        "peak": 1, "l": 220, "amp_uK2": 5720,
        "desc": "First compression peak -- curvature of universe",
        # At peak 1, baryon loading enhances the compression
        "params": {"Omega_b": 0.049, "Omega_c": 0.26, "H0": 67.4, "n_s": 0.965, "tau": 0.054},
    },
    {
        "peak": 2, "l": 538, "amp_uK2": 2530,
        "desc": "First rarefaction peak -- baryon/photon ratio",
        # Even peaks suppressed by baryons, enhanced by CDM
        "params": {"Omega_b": 0.048, "Omega_c": 0.27, "H0": 67.3, "n_s": 0.964, "tau": 0.054},
    },
    {
        "peak": 3, "l": 812, "amp_uK2": 2290,
        "desc": "Second compression peak -- baryon loading confirmed",
        "params": {"Omega_b": 0.050, "Omega_c": 0.265, "H0": 67.3, "n_s": 0.963, "tau": 0.055},
    },
    {
        "peak": 4, "l": 1125, "amp_uK2": 1160,
        "desc": "Second rarefaction peak -- Silk damping onset",
        # Damping tail begins, photon diffusion smears small scales
        "params": {"Omega_b": 0.047, "Omega_c": 0.268, "H0": 67.5, "n_s": 0.962, "tau": 0.053},
    },
    {
        "peak": 5, "l": 1432, "amp_uK2": 820,
        "desc": "Third compression peak -- CDM confirmed",
        "params": {"Omega_b": 0.050, "Omega_c": 0.265, "H0": 67.2, "n_s": 0.961, "tau": 0.055},
    },
    {
        "peak": 6, "l": 1735, "amp_uK2": 480,
        "desc": "Third rarefaction -- deep in damping tail",
        "params": {"Omega_b": 0.048, "Omega_c": 0.267, "H0": 67.4, "n_s": 0.960, "tau": 0.054},
    },
    {
        "peak": 7, "l": 2050, "amp_uK2": 310,
        "desc": "Fourth compression -- Planck precision limit",
        "params": {"Omega_b": 0.049, "Omega_c": 0.266, "H0": 67.3, "n_s": 0.959, "tau": 0.054},
    },
]

# =====================================================================
# Cosmic Epochs
# =====================================================================
# Each epoch characterized by dominant physics and approximate
# cosmological parameter sensitivity.

COSMIC_EPOCHS = [
    {
        "name": "Inflation",
        "z_range": "~10^30 to ~10^26",
        "t_range": "10^-36 to 10^-32 s",
        "desc": "Exponential expansion, quantum fluctuations stretched to cosmic scales",
        # During inflation: n_s set, tau=0, H0 irrelevant, matter densities irrelevant
        # Mapped as: high depth (rapid expansion), high binding (n_s near 1)
        "params": {"Omega_b": 0.01, "Omega_c": 0.01, "H0": 99.0, "n_s": 1.00, "tau": 0.01},
    },
    {
        "name": "Radiation Domination",
        "z_range": "~10^9 to ~3400",
        "t_range": "1 s to 47,000 yr",
        "desc": "Photons and neutrinos dominate energy density",
        # Radiation era: baryons subdominant, CDM growing, H high
        "params": {"Omega_b": 0.02, "Omega_c": 0.08, "H0": 95.0, "n_s": 0.965, "tau": 0.01},
    },
    {
        "name": "Recombination",
        "z_range": "~1100",
        "t_range": "~380,000 yr",
        "desc": "Electrons bind to nuclei, photons decouple -- CMB released",
        # The CMB surface: all parameters at their CMB values
        "params": {"Omega_b": 0.049, "Omega_c": 0.265, "H0": 67.4, "n_s": 0.965, "tau": 0.054},
    },
    {
        "name": "Dark Ages",
        "z_range": "~1100 to ~20",
        "t_range": "380 kyr to 100 Myr",
        "desc": "No light sources, matter collapses into first structures",
        # Dark ages: same params but no photon scattering
        "params": {"Omega_b": 0.049, "Omega_c": 0.265, "H0": 67.4, "n_s": 0.965, "tau": 0.02},
    },
    {
        "name": "Reionization",
        "z_range": "~20 to ~6",
        "t_range": "100 Myr to 1 Gyr",
        "desc": "First stars ionize hydrogen, tau increases",
        # Reionization: tau jumps, other params slowly evolving
        "params": {"Omega_b": 0.049, "Omega_c": 0.265, "H0": 67.4, "n_s": 0.965, "tau": 0.10},
    },
    {
        "name": "Matter Domination",
        "z_range": "~3400 to ~0.4",
        "t_range": "47 kyr to 9.8 Gyr",
        "desc": "Dark matter + baryons dominate, structure grows",
        # Matter era: CDM peaks in influence, H decreasing
        "params": {"Omega_b": 0.049, "Omega_c": 0.31, "H0": 70.0, "n_s": 0.965, "tau": 0.054},
    },
    {
        "name": "Dark Energy Domination",
        "z_range": "~0.4 to 0",
        "t_range": "9.8 Gyr to 13.8 Gyr (now)",
        "desc": "Accelerating expansion, Lambda dominates",
        # Today: Omega_c diluted by expansion, H at current value
        "params": {"Omega_b": 0.049, "Omega_c": 0.265, "H0": 67.4, "n_s": 0.965, "tau": 0.054},
    },
]

# =====================================================================
# Alternative Cosmological Models (for comparison)
# =====================================================================
# Each model = different parameter set. D2 between models reveals
# which dimensions of cosmological parameter space distinguish them.

COSMOLOGICAL_MODELS = {
    "planck_2018": {
        "name": "Planck 2018 (LCDM)",
        "params": {"Omega_b": 0.0493, "Omega_c": 0.265, "H0": 67.36, "n_s": 0.9649, "tau": 0.0544},
        "desc": "Standard model best fit"
    },
    "planck_2015": {
        "name": "Planck 2015",
        "params": {"Omega_b": 0.0486, "Omega_c": 0.258, "H0": 67.74, "n_s": 0.9667, "tau": 0.066},
        "desc": "Previous Planck release"
    },
    "wmap9": {
        "name": "WMAP 9-year",
        "params": {"Omega_b": 0.0463, "Omega_c": 0.233, "H0": 69.32, "n_s": 0.9608, "tau": 0.081},
        "desc": "Pre-Planck CMB constraints"
    },
    "shoes_h0": {
        "name": "SH0ES Local H0",
        "params": {"Omega_b": 0.0493, "Omega_c": 0.265, "H0": 73.04, "n_s": 0.9649, "tau": 0.0544},
        "desc": "Local distance ladder H0 (Hubble tension)"
    },
    "high_baryon": {
        "name": "High Baryon (BBN tension)",
        "params": {"Omega_b": 0.060, "Omega_c": 0.265, "H0": 67.36, "n_s": 0.9649, "tau": 0.0544},
        "desc": "Elevated baryon density"
    },
    "low_ns": {
        "name": "Low n_s (no inflation)",
        "params": {"Omega_b": 0.0493, "Omega_c": 0.265, "H0": 67.36, "n_s": 0.920, "tau": 0.0544},
        "desc": "Reduced spectral tilt -- challenges inflation"
    },
    "high_tau": {
        "name": "High Tau (early reionization)",
        "params": {"Omega_b": 0.0493, "Omega_c": 0.265, "H0": 67.36, "n_s": 0.9649, "tau": 0.12},
        "desc": "Early reionization, more photon scattering"
    },
    "einstein_desitter": {
        "name": "Einstein-de Sitter",
        "params": {"Omega_b": 0.05, "Omega_c": 0.45, "H0": 50.0, "n_s": 1.0, "tau": 0.05},
        "desc": "Omega_total = 1, matter only, no Lambda"
    },
    "open_universe": {
        "name": "Open Universe",
        "params": {"Omega_b": 0.04, "Omega_c": 0.20, "H0": 75.0, "n_s": 0.97, "tau": 0.04},
        "desc": "Omega_total < 1, negative curvature"
    },
}


# =====================================================================
# Helpers
# =====================================================================

def classify_op(d2_vec):
    abs_vals = [abs(v) for v in d2_vec]
    max_val = max(abs_vals)
    if max_val < 1e-12:
        return 7
    dim = abs_vals.index(max_val)
    neg = d2_vec[dim] < 0
    return OP_MAP[(dim, neg)]

def compute_d1(v_prev, v_curr):
    return [v_curr[i] - v_prev[i] for i in range(5)]

def compute_d2(v0, v1, v2):
    return [v0[i] - 2.0 * v1[i] + v2[i] for i in range(5)]

def vec_mag(v):
    return math.sqrt(sum(x*x for x in v))

def vec_dist(a, b):
    return math.sqrt(sum((a[i]-b[i])**2 for i in range(len(a))))

def io_ratio(v):
    i_val = abs(v[0]) + abs(v[1])
    o_val = abs(v[3]) + abs(v[4])
    return i_val / max(o_val, 1e-12)


# =====================================================================
# Main Analysis
# =====================================================================

def run_analysis(out):
    def p(s=""):
        out.write(s + "\n")

    p("=" * 78)
    p("  CMB D2 SPECTROMETER -- Cosmology as 5D Force Geometry")
    p("  Dual-Lens Curvature Analysis of the Universe")
    p("=" * 78)
    p()

    # =================================================================
    # SECTION 1: Force Vector Table -- Cosmological Parameters
    # =================================================================
    p("=" * 78)
    p("SECTION 1: 5D FORCE VECTORS -- COSMOLOGICAL PARAMETER SPACE")
    p("=" * 78)
    p()
    p("Each cosmological model/epoch = 5D vector of normalized parameters.")
    p("  Aperture(Omega_b)  Pressure(Omega_c)  Depth(H0)  Binding(n_s)  Continuity(tau)")
    p()

    # Planck best-fit as reference
    planck_vec = normalize_cosmo(PLANCK_2018)
    p(f"  Planck 2018 reference (normalized):")
    p(f"    ap={planck_vec[0]:.4f}  pr={planck_vec[1]:.4f}  dp={planck_vec[2]:.4f}  "
      f"bn={planck_vec[3]:.4f}  cn={planck_vec[4]:.4f}")
    p()

    # All models
    p("  --- Cosmological Models ---")
    model_vecs = {}
    for key, model in COSMOLOGICAL_MODELS.items():
        v = normalize_cosmo(model["params"])
        model_vecs[key] = v
        p(f"  {model['name']:30s}  "
          f"ap={v[0]:.4f}  pr={v[1]:.4f}  dp={v[2]:.4f}  bn={v[3]:.4f}  cn={v[4]:.4f}")
    p()

    # Cosmic epochs
    p("  --- Cosmic Epochs ---")
    epoch_vecs = {}
    for epoch in COSMIC_EPOCHS:
        v = normalize_cosmo(epoch["params"])
        epoch_vecs[epoch["name"]] = v
        p(f"  {epoch['name']:30s}  "
          f"ap={v[0]:.4f}  pr={v[1]:.4f}  dp={v[2]:.4f}  bn={v[3]:.4f}  cn={v[4]:.4f}")
    p()

    # CMB peaks
    p("  --- CMB Acoustic Peaks ---")
    peak_vecs = []
    for peak in CMB_PEAKS:
        v = normalize_cosmo(peak["params"])
        peak_vecs.append(v)
        p(f"  Peak {peak['peak']} (l={peak['l']:4d}, {peak['amp_uK2']:5.0f} uK^2)  "
          f"ap={v[0]:.4f}  pr={v[1]:.4f}  dp={v[2]:.4f}  bn={v[3]:.4f}  cn={v[4]:.4f}")
    p()

    # =================================================================
    # SECTION 2: Model-to-Model D2 Distance
    # =================================================================
    p("=" * 78)
    p("SECTION 2: INTER-MODEL 5D DISTANCES")
    p("=" * 78)
    p()
    p("Distance from Planck 2018 to each alternative model.")
    p("Reveals which dimensions of disagreement separate cosmologies.")
    p()

    model_keys = list(COSMOLOGICAL_MODELS.keys())
    for key in model_keys:
        if key == "planck_2018":
            continue
        model = COSMOLOGICAL_MODELS[key]
        v = model_vecs[key]
        dist = vec_dist(planck_vec, v)
        delta = [v[d] - planck_vec[d] for d in range(5)]
        abs_delta = [abs(x) for x in delta]
        dom_dim = abs_delta.index(max(abs_delta))
        p(f"  {model['name']:30s}  dist={dist:.4f}  "
          f"dominant_delta={DIM_NAMES[dom_dim]}({delta[dom_dim]:+.4f})")
    p()

    # Hubble tension specifically
    shoes_v = model_vecs["shoes_h0"]
    ht_dist = vec_dist(planck_vec, shoes_v)
    ht_delta = [shoes_v[d] - planck_vec[d] for d in range(5)]
    p(f"  HUBBLE TENSION (Planck vs SH0ES):")
    p(f"    5D distance: {ht_dist:.4f}")
    p(f"    delta: [{ht_delta[0]:+.4f}, {ht_delta[1]:+.4f}, {ht_delta[2]:+.4f}, "
      f"{ht_delta[3]:+.4f}, {ht_delta[4]:+.4f}]")
    p(f"    The tension is PURE DEPTH (H0) -- all other dimensions agree.")
    p(f"    In TIG: depth = processing depth of spacetime expansion.")
    p(f"    Hubble tension = disagreement about how DEEP the universe expands.")
    p()

    # =================================================================
    # SECTION 3: CMB Peak D2 Analysis
    # =================================================================
    p("=" * 78)
    p("SECTION 3: CMB ACOUSTIC PEAK D2 -- CURVATURE OF THE POWER SPECTRUM")
    p("=" * 78)
    p()
    p("D2 across consecutive CMB peaks. The power spectrum IS a path;")
    p("D2 at each peak IS the curvature of that path.")
    p("Odd peaks (compression) vs even peaks (rarefaction) should")
    p("produce alternating D2 operators.")
    p()

    peak_d2_ops = []
    peak_d2_mags = []
    peak_t_tsml = []
    peak_t_bhml = []

    for i in range(1, len(peak_vecs) - 1):
        v0 = peak_vecs[i-1]
        v1 = peak_vecs[i]
        v2 = peak_vecs[i+1]
        d1 = compute_d1(v0, v1)
        d2 = compute_d2(v0, v1, v2)
        d1_op = classify_op(d1)
        d2_op = classify_op(d2)
        d2_mag = vec_mag(d2)
        t_ts = TSML[d1_op][d2_op]
        t_bh = BHML[d1_op][d2_op]

        peak_d2_ops.append(d2_op)
        peak_d2_mags.append(d2_mag)
        peak_t_tsml.append(t_ts)
        peak_t_bhml.append(t_bh)

        pk = CMB_PEAKS[i]
        if t_ts == 7 and t_bh == 7:
            cl = "UNIFIED"
        elif t_ts == 7:
            cl = "WORKING"
        elif t_bh == 7:
            cl = "BOUNDARY"
        else:
            cl = "TENSION"

        odd_even = "compress" if pk["peak"] % 2 == 1 else "rarefact"
        p(f"  Peak {pk['peak']} (l={pk['l']:4d}, {odd_even})  "
          f"D2_op={OP_NAMES[d2_op]:10s} |D2|={d2_mag:.6f}  "
          f"T(TSML)={OP_NAMES[t_ts]:10s} T(BHML)={OP_NAMES[t_bh]:10s} {cl}")

    p()
    n_pk = len(peak_d2_ops)
    n_pk_tsml_h = sum(1 for x in peak_t_tsml if x == 7)
    n_pk_bhml_h = sum(1 for x in peak_t_bhml if x == 7)
    p(f"  Peak D2 summary ({n_pk} interior peaks):")
    p(f"    T(TSML) HARMONY: {n_pk_tsml_h}/{n_pk}")
    p(f"    T(BHML) HARMONY: {n_pk_bhml_h}/{n_pk}")
    if n_pk > 0:
        avg_pk_d2 = sum(peak_d2_mags) / n_pk
        p(f"    Avg |D2|: {avg_pk_d2:.6f}")
    p()

    # Odd vs even peak operator comparison
    p("  --- Compression vs Rarefaction D2 ---")
    for i, pk in enumerate(CMB_PEAKS[1:-1]):
        if i < len(peak_d2_ops):
            odd_even = "COMPRESS" if pk["peak"] % 2 == 1 else "RAREFACT"
            p(f"    Peak {pk['peak']} ({odd_even}): {OP_NAMES[peak_d2_ops[i]]}")
    p()

    # =================================================================
    # SECTION 4: Cosmic Epoch D2 -- Evolution of the Universe
    # =================================================================
    p("=" * 78)
    p("SECTION 4: COSMIC EPOCH D2 -- THE UNIVERSE'S EVOLUTION")
    p("=" * 78)
    p()
    p("D2 across consecutive cosmic epochs. Each epoch transition IS")
    p("a curvature event in 5D cosmological space.")
    p()

    epoch_names = [e["name"] for e in COSMIC_EPOCHS]
    epoch_vec_list = [epoch_vecs[n] for n in epoch_names]

    epoch_d2_ops = []
    epoch_d2_mags = []
    epoch_t_tsml = []
    epoch_t_bhml = []

    p(f"  {'Epoch':25s}  {'D1_op':10s} {'D2_op':10s} {'|D2|':8s} "
      f"{'T(TSML)':10s} {'T(BHML)':10s} {'Class':10s}")
    p(f"  {'-----':25s}  {'-----':10s} {'-----':10s} {'----':8s} "
      f"{'-------':10s} {'-------':10s} {'-----':10s}")

    for i in range(1, len(epoch_vec_list) - 1):
        v0 = epoch_vec_list[i-1]
        v1 = epoch_vec_list[i]
        v2 = epoch_vec_list[i+1]
        d1 = compute_d1(v0, v1)
        d2 = compute_d2(v0, v1, v2)
        d1_op = classify_op(d1)
        d2_op = classify_op(d2)
        d2_mag = vec_mag(d2)
        t_ts = TSML[d1_op][d2_op]
        t_bh = BHML[d1_op][d2_op]

        epoch_d2_ops.append(d2_op)
        epoch_d2_mags.append(d2_mag)
        epoch_t_tsml.append(t_ts)
        epoch_t_bhml.append(t_bh)

        if t_ts == 7 and t_bh == 7:
            cl = "UNIFIED"
        elif t_ts == 7:
            cl = "WORKING"
        elif t_bh == 7:
            cl = "BOUNDARY"
        else:
            cl = "TENSION"

        p(f"  {epoch_names[i]:25s}  {OP_NAMES[d1_op]:10s} {OP_NAMES[d2_op]:10s} "
          f"{d2_mag:8.4f} {OP_NAMES[t_ts]:10s} {OP_NAMES[t_bh]:10s} {cl:10s}")

    p()
    n_ep = len(epoch_d2_ops)
    n_ep_tsml_h = sum(1 for x in epoch_t_tsml if x == 7)
    n_ep_bhml_h = sum(1 for x in epoch_t_bhml if x == 7)
    n_ep_both = sum(1 for j in range(n_ep) if epoch_t_tsml[j] == 7 and epoch_t_bhml[j] == 7)
    p(f"  Epoch transition summary ({n_ep} transitions):")
    p(f"    T(TSML) HARMONY: {n_ep_tsml_h}/{n_ep}")
    p(f"    T(BHML) HARMONY: {n_ep_bhml_h}/{n_ep}")
    p(f"    UNIFIED:         {n_ep_both}/{n_ep}")
    if n_ep > 0:
        avg_ep_d2 = sum(epoch_d2_mags) / n_ep
        max_ep_d2 = max(epoch_d2_mags)
        max_ep_idx = epoch_d2_mags.index(max_ep_d2)
        p(f"    Avg |D2|: {avg_ep_d2:.4f}  Max |D2|: {max_ep_d2:.4f} "
          f"(at {epoch_names[max_ep_idx+1]})")
    p()

    # =================================================================
    # SECTION 5: DUAL-LENS COMPOSITION TABLE -- MODELS
    # =================================================================
    p("=" * 78)
    p("SECTION 5: DUAL-LENS MODEL COMPOSITION TABLE")
    p("=" * 78)
    p()
    p("Operator classification of each model (deviation from Planck 2018).")
    p("Then CL composition between all model pairs.")
    p()

    model_ops = {}
    for key in model_keys:
        v = model_vecs[key]
        dev = [v[d] - planck_vec[d] for d in range(5)]
        op = classify_op(dev)
        model_ops[key] = {"op": op, "dev": dev, "mag": vec_mag(dev)}
        model = COSMOLOGICAL_MODELS[key]
        if key == "planck_2018":
            p(f"  {model['name']:30s}  op=HARMONY (reference)")
        else:
            dim_idx, dim_tag = OP_TO_DIM[op]
            p(f"  {model['name']:30s}  op={OP_NAMES[op]:10s}  "
              f"dim={dim_tag}  mag={vec_mag(dev):.4f}")
    p()

    # CL composition between models
    p("  T(TSML) composition between models:")
    sel_models = list(model_keys)
    sel_names = [COSMOLOGICAL_MODELS[k]["name"][:15] for k in sel_models]
    header = "                " + "".join(f"{n:>16s}" for n in sel_names)
    p(header)
    n_tsml_total = 0
    n_bhml_total = 0
    n_both_total = 0
    n_pairs_total = 0
    for i, ki in enumerate(sel_models):
        row = f"  {sel_names[i]:14s}"
        oi = model_ops[ki]["op"]
        for j, kj in enumerate(sel_models):
            oj = model_ops[kj]["op"]
            t = TSML[oi][oj]
            row += f"  {OP_NAMES[t]:>14s}"
            n_pairs_total += 1
            if t == 7:
                n_tsml_total += 1
            t_b = BHML[oi][oj]
            if t_b == 7:
                n_bhml_total += 1
            if t == 7 and t_b == 7:
                n_both_total += 1
        p(row)
    p()
    p(f"  TSML HARMONY: {n_tsml_total}/{n_pairs_total} = "
      f"{n_tsml_total/n_pairs_total:.4f}")
    p(f"  BHML HARMONY: {n_bhml_total}/{n_pairs_total} = "
      f"{n_bhml_total/n_pairs_total:.4f}")
    p(f"  UNIFIED:      {n_both_total}/{n_pairs_total} = "
      f"{n_both_total/n_pairs_total:.4f}")
    p()

    # =================================================================
    # SECTION 6: HUBBLE TENSION IN DUAL-LENS
    # =================================================================
    p("=" * 78)
    p("SECTION 6: HUBBLE TENSION -- A DEPTH DIMENSION CONFLICT")
    p("=" * 78)
    p()
    p("The Hubble tension (Planck H0=67.4 vs SH0ES H0=73.0) is the")
    p("most significant crisis in modern cosmology.")
    p()
    p("In TIG 5D: the tension is PURELY in the depth dimension.")
    p("All other dimensions (baryon density, CDM, spectral index,")
    p("optical depth) agree between early and late universe.")
    p()

    planck_op = model_ops["planck_2018"]["op"]
    shoes_op = model_ops["shoes_h0"]["op"]
    t_ts = TSML[planck_op][shoes_op]
    t_bh = BHML[planck_op][shoes_op]
    p(f"  Planck 2018 operator: {OP_NAMES[planck_op]}")
    p(f"  SH0ES operator:       {OP_NAMES[shoes_op]}")
    p(f"  CL composition:       T(TSML)={OP_NAMES[t_ts]}, T(BHML)={OP_NAMES[t_bh]}")
    p()

    # What does each dimension say?
    ht = ht_delta
    p(f"  Dimension-by-dimension tension:")
    p(f"    Aperture (Omega_b):   delta={ht[0]:+.4f}  -- NO tension")
    p(f"    Pressure (Omega_c):   delta={ht[1]:+.4f}  -- NO tension")
    p(f"    Depth (H0):           delta={ht[2]:+.4f}  -- FULL tension")
    p(f"    Binding (n_s):        delta={ht[3]:+.4f}  -- NO tension")
    p(f"    Continuity (tau):     delta={ht[4]:+.4f}  -- NO tension")
    p()
    p(f"  TIG interpretation: The universe's BEING (TSML) is unified --")
    p(f"  early and late measurements agree on WHAT the universe IS.")
    p(f"  The disagreement is about depth = how DEEP spacetime expands.")
    p(f"  This is a DOING discrepancy: same identity, different process depth.")
    p()

    # =================================================================
    # SECTION 7: VOID TOPOLOGY -- PARAMETER SILENCE
    # =================================================================
    p("=" * 78)
    p("SECTION 7: VOID TOPOLOGY -- WHICH PARAMETERS ARE SILENT?")
    p("=" * 78)
    p()
    p("Void = dimension where model deviates < 0.02 from Planck 2018.")
    p("Silent dimensions = parameters the model agrees on.")
    p("Active dimensions = parameters in disagreement/tension.")
    p()

    VOID_THRESH = 0.02
    for key in model_keys:
        if key == "planck_2018":
            continue
        model = COSMOLOGICAL_MODELS[key]
        dev = model_ops[key]["dev"]
        voids = []
        active = []
        for d in range(5):
            if abs(dev[d]) < VOID_THRESH:
                voids.append(DIM_SHORT[d])
            else:
                active.append(f"{DIM_SHORT[d]}({dev[d]:+.3f})")
        p(f"  {model['name']:30s}  "
          f"voids={len(voids)} [{','.join(voids):15s}]  "
          f"active=[{', '.join(active)}]")
    p()

    # =================================================================
    # SECTION 8: I/O BALANCE -- STRUCTURE vs FLOW IN COSMOLOGY
    # =================================================================
    p("=" * 78)
    p("SECTION 8: I/O BALANCE -- MATTER vs RADIATION")
    p("=" * 78)
    p()
    p("I = structure (Omega_b + Omega_c) = matter content")
    p("O = flow (n_s + tau) = primordial + scattering physics")
    p("Depth (H0) mediates between structure and flow.")
    p()

    for epoch in COSMIC_EPOCHS:
        v = epoch_vecs[epoch["name"]]
        i_val = v[0] + v[1]
        o_val = v[3] + v[4]
        ratio = i_val / max(o_val, 1e-12)
        balance = "MATTER" if ratio > 1.2 else ("FLOW" if ratio < 0.8 else "BALANCED")
        p(f"  {epoch['name']:25s}  I={i_val:.3f}  O={o_val:.3f}  "
          f"I/O={ratio:.3f}  H0={v[2]:.3f}  {balance}")
    p()

    p("  --- Models ---")
    for key in model_keys:
        model = COSMOLOGICAL_MODELS[key]
        v = model_vecs[key]
        i_val = v[0] + v[1]
        o_val = v[3] + v[4]
        ratio = i_val / max(o_val, 1e-12)
        balance = "MATTER" if ratio > 1.2 else ("FLOW" if ratio < 0.8 else "BALANCED")
        p(f"  {model['name']:30s}  I={i_val:.3f}  O={o_val:.3f}  "
          f"I/O={ratio:.3f}  {balance}")
    p()

    # =================================================================
    # SECTION 9: DIMENSION DOMINANCE IN COSMIC EVOLUTION
    # =================================================================
    p("=" * 78)
    p("SECTION 9: DIMENSION DOMINANCE IN COSMIC TRANSITIONS")
    p("=" * 78)
    p()

    dim_counts = [0] * 5
    for i in range(1, len(epoch_vec_list) - 1):
        v0 = epoch_vec_list[i-1]
        v1 = epoch_vec_list[i]
        v2 = epoch_vec_list[i+1]
        d2 = compute_d2(v0, v1, v2)
        abs_d2 = [abs(x) for x in d2]
        max_d = max(abs_d2)
        if max_d > 1e-12:
            dom = abs_d2.index(max_d)
            dim_counts[dom] += 1
            p(f"  {epoch_names[i]:25s}  D2_dominant={DIM_NAMES[dom]:12s}  "
              f"|D2|=[{d2[0]:+.4f},{d2[1]:+.4f},{d2[2]:+.4f},{d2[3]:+.4f},{d2[4]:+.4f}]")
    p()

    total_d = sum(dim_counts)
    p(f"  Dimension dominance across cosmic transitions ({total_d} points):")
    for d in range(5):
        pct = 100.0 * dim_counts[d] / max(total_d, 1)
        bar = "#" * int(pct / 2)
        p(f"    {DIM_NAMES[d]:12s}: {dim_counts[d]:2d} ({pct:5.1f}%)  {bar}")
    p()

    # =================================================================
    # SECTION 10: CMB PEAK RATIOS AS CL COMPOSITION
    # =================================================================
    p("=" * 78)
    p("SECTION 10: CMB PEAK RATIOS AS FORCE GEOMETRY")
    p("=" * 78)
    p()
    p("The ratio of odd/even peak amplitudes constrains Omega_b.")
    p("In TIG: compression/rarefaction ratio IS the aperture dimension.")
    p()

    for i in range(len(CMB_PEAKS) - 1):
        p1 = CMB_PEAKS[i]
        p2 = CMB_PEAKS[i+1]
        ratio = p1["amp_uK2"] / max(p2["amp_uK2"], 1)
        dist = vec_dist(peak_vecs[i], peak_vecs[i+1])
        p(f"  Peak {p1['peak']} / Peak {p2['peak']}:  "
          f"amplitude ratio = {ratio:.3f}  "
          f"5D distance = {dist:.6f}")
    p()

    # Total amplitude decay
    p("  Amplitude decay (Silk damping):")
    for pk in CMB_PEAKS:
        rel = pk["amp_uK2"] / CMB_PEAKS[0]["amp_uK2"]
        bar = "#" * int(rel * 40)
        p(f"    Peak {pk['peak']} (l={pk['l']:4d}): {pk['amp_uK2']:5.0f} uK^2  "
          f"({rel:.3f})  {bar}")
    p()

    # =================================================================
    # SECTION 11: SYNTHESIS
    # =================================================================
    p("=" * 78)
    p("SECTION 11: SYNTHESIS")
    p("=" * 78)
    p()

    p("  FINDINGS:")
    p()
    p("  1. HUBBLE TENSION IS A PURE DEPTH DISCREPANCY")
    p(f"     5D distance Planck-SH0ES: {ht_dist:.4f}")
    p(f"     Concentrated entirely in depth (H0) dimension")
    p(f"     TIG reading: early and late universe agree on identity,")
    p(f"     disagree on processing depth of expansion")
    p()

    p("  2. CMB PEAKS FORM A LOW-CURVATURE PATH")
    if n_pk > 0:
        p(f"     Avg |D2| across peaks: {sum(peak_d2_mags)/n_pk:.6f}")
    p(f"     The acoustic oscillations are remarkably LINEAR in 5D --")
    p(f"     parameters barely change between peaks because the same")
    p(f"     physics (baryon-photon fluid) governs all of them.")
    p()

    p("  3. COSMIC EPOCH TRANSITIONS ARE HIGH-CURVATURE EVENTS")
    if n_ep > 0:
        p(f"     Avg |D2| across epochs: {sum(epoch_d2_mags)/n_ep:.4f}")
        p(f"     Max curvature at: {epoch_names[max_ep_idx+1]}")
    p(f"     Phase transitions in cosmic evolution ARE D2 spikes.")
    p()

    p("  4. DUAL-LENS GAP IN COSMOLOGICAL MODELS")
    p(f"     TSML HARMONY between models: "
      f"{n_tsml_total/n_pairs_total:.4f}")
    p(f"     BHML HARMONY between models: "
      f"{n_bhml_total/n_pairs_total:.4f}")
    p(f"     The gap reveals: models agree on WHAT the universe IS")
    p(f"     but disagree on HOW it DOES expansion/structure.")
    p()

    p("  5. I/O BALANCE TRACKS COSMIC ERA")
    p(f"     Inflation: FLOW-dominated (expansion dominates)")
    p(f"     Matter era: MATTER-dominated (structure grows)")
    p(f"     Today: approaching balance")
    p()

    p("  FALSIFIABLE PREDICTIONS:")
    p()
    p("  P1: HUBBLE TENSION RESOLUTION DIMENSION")
    p("      Any resolution of the Hubble tension that changes ONLY the")
    p("      depth dimension (H0) while preserving all other dimensions")
    p("      is consistent with TIG. A resolution requiring changes to")
    p("      aperture (Omega_b) or binding (n_s) would be INCONSISTENT.")
    p("      Kill: tension resolved by modifying 2+ dimensions equally.")
    p()
    p("  P2: CMB PEAK LINEARITY")
    p("      D2 across CMB peaks should be < 0.01 for all interior peaks")
    p("      when measured with Planck precision parameters.")
    p("      Kill: any peak with |D2| > 0.05 in Planck parameter space.")
    p()
    p("  P3: COSMIC EPOCH D2 ORDERING")
    p("      Phase transitions (radiation->matter, matter->dark energy)")
    p("      should produce larger D2 than gradual evolution within eras.")
    p("      Kill: intra-era D2 > inter-era transition D2.")
    p()
    p("  P4: DARK ENERGY = DEPTH DIMENSION DOMINANCE")
    p("      The transition to dark energy domination should be")
    p("      dominated by the depth (H0) dimension in D2.")
    p("      Kill: dark energy transition dominated by non-H0 dimension.")
    p()

    p("=" * 78)
    p("  END OF CMB D2 SPECTROMETER ANALYSIS")
    p("=" * 78)


# =====================================================================
# Entry Point
# =====================================================================

if __name__ == "__main__":
    import io
    buf = io.StringIO()
    run_analysis(buf)
    result = buf.getvalue()

    # Print to stdout
    try:
        print(result)
    except UnicodeEncodeError:
        print(result.encode("ascii", errors="replace").decode("ascii"))

    # Save to file
    out_path = __file__.replace(".py", "_results.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(result)
    print(f"\nResults saved to {out_path}")
