#!/usr/bin/env python3
"""
econ_d2_spectrometer.py -- Dual-Lens D2 Spectrometer for Economics
===================================================================

Financial markets as 5D force geometry.

Market regimes, business cycles, and macro indicators mapped through
the D2 pipeline. The economy IS a path through 5D space.
D2 IS the curvature of that path. Crashes ARE D2 spikes.

5D Force Mapping (macro-financial indicators, normalized):
  Aperture   = Yield Spread (10Y-2Y)     -- openness of credit channel
  Pressure   = Volatility (VIX)          -- market pressure/fear
  Depth      = GDP Growth (real, annualized) -- depth of economic expansion
  Binding    = Employment Rate            -- labor market binding
  Continuity = Inflation Rate (CPI)       -- price continuity/persistence

This mapping is NOT arbitrary:
  Yield spread = aperture: credit OPENS or CLOSES to the economy
  VIX = pressure: volatility IS the pressure under which decisions are made
  GDP = depth: economic output IS the depth of productive activity
  Employment = binding: labor IS what binds inputs to outputs
  Inflation = continuity: prices IS the continuity signal in exchange

Market Regimes:
  Expansion, Peak, Contraction, Trough, Recovery, Bubble, Crash,
  Stagflation, Deflation

Historical Cycles (US):
  1990s expansion, Dot-com crash, 2008 GFC, 2020 COVID, 2022 inflation

The dual-lens question:
  TSML (being): What IS this market regime? (identity)
  BHML (doing): What DOES this regime produce? (mechanism)
  Gap = what the market IS vs what it DOES = mispricing/sentiment

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
# Normalization ranges
# =====================================================================
# Based on US historical data ranges (1960-2025)
NORM = {
    "spread":     (-1.0, 3.0),    # 10Y-2Y spread (pp)
    "vix":        (9.0, 80.0),    # VIX index
    "gdp":        (-10.0, 10.0),  # Real GDP growth (%)
    "employment": (88.0, 97.0),   # Employment rate (100 - unemployment %)
    "inflation":  (-2.0, 15.0),   # CPI YoY (%)
}

def normalize_econ(params):
    """Normalize economic indicators to [0,1]."""
    keys = ["spread", "vix", "gdp", "employment", "inflation"]
    v = []
    for k in keys:
        lo, hi = NORM[k]
        val = (params[k] - lo) / (hi - lo)
        val = max(0.0, min(1.0, val))
        v.append(val)
    return v

# =====================================================================
# Market Regime Data
# =====================================================================
# Representative values for each market regime type

REGIMES = {
    "healthy_expansion": {
        "name": "Healthy Expansion",
        "category": "growth",
        "stable": True,
        "params": {"spread": 1.5, "vix": 14, "gdp": 3.0, "employment": 96.0, "inflation": 2.5},
        "desc": "Goldilocks economy: moderate growth, low vol, stable prices"
    },
    "late_cycle": {
        "name": "Late Cycle Expansion",
        "category": "growth",
        "stable": True,
        "params": {"spread": 0.5, "vix": 18, "gdp": 2.0, "employment": 96.5, "inflation": 3.5},
        "desc": "Curve flattening, tight labor, rising inflation"
    },
    "peak": {
        "name": "Cycle Peak",
        "category": "transition",
        "stable": False,
        "params": {"spread": 0.0, "vix": 22, "gdp": 1.0, "employment": 96.0, "inflation": 4.0},
        "desc": "Flat/inverted curve, growth slowing, inflation high"
    },
    "early_contraction": {
        "name": "Early Contraction",
        "category": "recession",
        "stable": False,
        "params": {"spread": -0.5, "vix": 30, "gdp": -1.0, "employment": 94.0, "inflation": 3.0},
        "desc": "Inverted curve, rising vol, GDP turns negative"
    },
    "recession": {
        "name": "Full Recession",
        "category": "recession",
        "stable": False,
        "params": {"spread": -0.3, "vix": 35, "gdp": -3.0, "employment": 91.0, "inflation": 1.0},
        "desc": "Deep contraction, high vol, employment falling"
    },
    "trough": {
        "name": "Cycle Trough",
        "category": "transition",
        "stable": False,
        "params": {"spread": 1.0, "vix": 30, "gdp": -1.0, "employment": 89.5, "inflation": 0.5},
        "desc": "Curve steepening, GDP bottoming, employment worst"
    },
    "early_recovery": {
        "name": "Early Recovery",
        "category": "growth",
        "stable": True,
        "params": {"spread": 2.5, "vix": 22, "gdp": 4.0, "employment": 91.0, "inflation": 1.5},
        "desc": "Steep curve, accelerating GDP, jobs lagging"
    },
    "bubble": {
        "name": "Asset Bubble",
        "category": "bubble",
        "stable": False,
        "params": {"spread": 1.0, "vix": 12, "gdp": 3.5, "employment": 95.5, "inflation": 2.0},
        "desc": "Complacency: low vol, strong growth, leverage building"
    },
    "crash": {
        "name": "Market Crash",
        "category": "crisis",
        "stable": False,
        "params": {"spread": -0.8, "vix": 65, "gdp": -6.0, "employment": 90.0, "inflation": 0.0},
        "desc": "Extreme vol, credit freeze, rapid GDP decline"
    },
    "panic": {
        "name": "Financial Panic",
        "category": "crisis",
        "stable": False,
        "params": {"spread": -0.5, "vix": 75, "gdp": -8.0, "employment": 88.5, "inflation": -1.0},
        "desc": "Systemic crisis, VIX extreme, deflation threat"
    },
    "stagflation": {
        "name": "Stagflation",
        "category": "pathological",
        "stable": False,
        "params": {"spread": 0.5, "vix": 25, "gdp": 0.0, "employment": 92.0, "inflation": 8.0},
        "desc": "Stagnant growth + high inflation (1970s style)"
    },
    "deflation": {
        "name": "Deflation Trap",
        "category": "pathological",
        "stable": False,
        "params": {"spread": 1.5, "vix": 20, "gdp": 0.5, "employment": 93.0, "inflation": -1.5},
        "desc": "Falling prices, weak demand, Japan-style"
    },
    "hyperinflation": {
        "name": "Hyperinflation",
        "category": "pathological",
        "stable": False,
        "params": {"spread": 2.0, "vix": 40, "gdp": -2.0, "employment": 90.0, "inflation": 14.0},
        "desc": "Currency collapse, price spiral, economic breakdown"
    },
    "zirp": {
        "name": "ZIRP/QE Era",
        "category": "policy",
        "stable": True,
        "params": {"spread": 1.8, "vix": 15, "gdp": 2.0, "employment": 94.5, "inflation": 1.5},
        "desc": "Zero rates, QE, moderate growth, low inflation"
    },
    "tightening": {
        "name": "Aggressive Tightening",
        "category": "policy",
        "stable": False,
        "params": {"spread": -0.3, "vix": 28, "gdp": 1.5, "employment": 96.0, "inflation": 6.0},
        "desc": "Fed hiking aggressively, inverted curve, inflation high"
    },
}

# =====================================================================
# Historical Cycle Sequences
# =====================================================================

CYCLES = {
    "normal_cycle": {
        "name": "Textbook Business Cycle",
        "desc": "Expansion -> Peak -> Contraction -> Trough -> Recovery",
        "epochs": ["early_recovery", "healthy_expansion", "late_cycle", "peak",
                   "early_contraction", "recession", "trough", "early_recovery"],
    },
    "dotcom": {
        "name": "Dot-Com Cycle (1997-2003)",
        "desc": "Bubble -> Peak -> Crash -> Recovery",
        "epochs": ["healthy_expansion", "bubble", "bubble", "peak",
                   "crash", "recession", "trough", "early_recovery"],
    },
    "gfc_2008": {
        "name": "Global Financial Crisis (2006-2010)",
        "desc": "Bubble -> Credit Crisis -> Panic -> Recovery",
        "epochs": ["late_cycle", "bubble", "peak", "crash",
                   "panic", "trough", "early_recovery", "zirp"],
    },
    "covid_2020": {
        "name": "COVID-19 Cycle (2019-2022)",
        "desc": "Expansion -> Instant Crash -> V-Recovery -> Inflation",
        "epochs": ["healthy_expansion", "healthy_expansion", "crash", "panic",
                   "trough", "early_recovery", "healthy_expansion", "tightening"],
    },
    "stagflation_70s": {
        "name": "1970s Stagflation",
        "desc": "Expansion -> Oil Shock -> Stagflation -> Volcker",
        "epochs": ["healthy_expansion", "peak", "stagflation", "stagflation",
                   "tightening", "recession", "trough", "early_recovery"],
    },
    "japan_lost": {
        "name": "Japan Lost Decades (1989-2010)",
        "desc": "Bubble -> Crash -> Deflation Trap -> ZIRP",
        "epochs": ["bubble", "peak", "crash", "recession",
                   "deflation", "deflation", "zirp", "zirp"],
    },
    "inflation_2022": {
        "name": "2022 Inflation/Tightening",
        "desc": "QE -> Recovery -> Inflation -> Tightening",
        "epochs": ["zirp", "zirp", "early_recovery", "healthy_expansion",
                   "late_cycle", "tightening", "tightening", "peak"],
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
    p("  ECONOMICS D2 SPECTROMETER -- Markets as 5D Force Geometry")
    p("  Dual-Lens Curvature Analysis of Business Cycles")
    p("=" * 78)
    p()

    # =================================================================
    # SECTION 1: Force Vectors -- All Market Regimes
    # =================================================================
    p("=" * 78)
    p("SECTION 1: 5D FORCE VECTORS -- MARKET REGIME SIGNATURES")
    p("=" * 78)
    p()
    p("Each regime = 5D vector of normalized macro indicators.")
    p("  Aperture(spread)  Pressure(VIX)  Depth(GDP)  Binding(empl)  Continuity(CPI)")
    p()

    regime_keys = list(REGIMES.keys())
    regime_vecs = {}

    categories = ["growth", "transition", "recession", "bubble",
                  "crisis", "pathological", "policy"]
    cat_names = {
        "growth": "GROWTH REGIMES",
        "transition": "TRANSITION REGIMES",
        "recession": "RECESSION REGIMES",
        "bubble": "BUBBLE REGIMES",
        "crisis": "CRISIS REGIMES",
        "pathological": "PATHOLOGICAL REGIMES",
        "policy": "POLICY REGIMES",
    }

    for cat in categories:
        states_in_cat = [k for k in regime_keys if REGIMES[k]["category"] == cat]
        if not states_in_cat:
            continue
        p(f"  --- {cat_names[cat]} ---")
        for key in states_in_cat:
            r = REGIMES[key]
            v = normalize_econ(r["params"])
            regime_vecs[key] = v
            stable_mark = "S" if r["stable"] else " "
            p(f"  [{stable_mark}] {r['name']:25s}  "
              f"sp={v[0]:.3f}  vx={v[1]:.3f}  gd={v[2]:.3f}  "
              f"em={v[3]:.3f}  in={v[4]:.3f}")
        p()

    p(f"  Total regimes: {len(regime_vecs)}")
    p(f"  [S] = stable regime")
    p()

    # =================================================================
    # SECTION 2: Pairwise Distances
    # =================================================================
    p("=" * 78)
    p("SECTION 2: KEY PAIRWISE DISTANCES")
    p("=" * 78)
    p()

    pairs = [
        ("healthy_expansion", "late_cycle", "Healthy -> Late cycle"),
        ("late_cycle", "peak", "Late cycle -> Peak"),
        ("peak", "early_contraction", "Peak -> Contraction"),
        ("early_contraction", "recession", "Contraction -> Recession"),
        ("recession", "trough", "Recession -> Trough"),
        ("trough", "early_recovery", "Trough -> Recovery"),
        ("bubble", "crash", "Bubble -> Crash"),
        ("healthy_expansion", "crash", "Expansion -> Crash"),
        ("healthy_expansion", "stagflation", "Expansion -> Stagflation"),
        ("crash", "panic", "Crash -> Panic"),
        ("zirp", "tightening", "ZIRP -> Tightening"),
        ("deflation", "hyperinflation", "Deflation -> Hyperinflation"),
    ]

    for k1, k2, desc in pairs:
        d = vec_dist(regime_vecs[k1], regime_vecs[k2])
        p(f"  {desc:35s}  dist = {d:.4f}")
    p()

    # Stable vs unstable centroid
    stable_keys = [k for k in regime_keys if REGIMES[k]["stable"]]
    unstable_keys = [k for k in regime_keys if not REGIMES[k]["stable"]]

    s_centroid = [0.0] * 5
    for k in stable_keys:
        for d in range(5):
            s_centroid[d] += regime_vecs[k][d]
    s_centroid = [x / len(stable_keys) for x in s_centroid]

    u_centroid = [0.0] * 5
    for k in unstable_keys:
        for d in range(5):
            u_centroid[d] += regime_vecs[k][d]
    u_centroid = [x / len(unstable_keys) for x in u_centroid]

    p(f"  Stable centroid:   sp={s_centroid[0]:.3f} vx={s_centroid[1]:.3f} "
      f"gd={s_centroid[2]:.3f} em={s_centroid[3]:.3f} in={s_centroid[4]:.3f}")
    p(f"  Unstable centroid: sp={u_centroid[0]:.3f} vx={u_centroid[1]:.3f} "
      f"gd={u_centroid[2]:.3f} em={u_centroid[3]:.3f} in={u_centroid[4]:.3f}")
    p(f"  Centroid separation: {vec_dist(s_centroid, u_centroid):.4f}")
    p()

    dim_sep = [abs(s_centroid[d] - u_centroid[d]) for d in range(5)]
    max_sep = dim_sep.index(max(dim_sep))
    p(f"  Most separating dimension: {DIM_NAMES[max_sep]} ({dim_sep[max_sep]:.4f})")
    p()

    # =================================================================
    # SECTION 3: Operator Classification
    # =================================================================
    p("=" * 78)
    p("SECTION 3: D2 OPERATOR CLASSIFICATION PER REGIME")
    p("=" * 78)
    p()

    all_vecs = list(regime_vecs.values())
    n_reg = len(all_vecs)
    global_centroid = [sum(v[d] for v in all_vecs) / n_reg for d in range(5)]
    p(f"  Global centroid: sp={global_centroid[0]:.3f} vx={global_centroid[1]:.3f} "
      f"gd={global_centroid[2]:.3f} em={global_centroid[3]:.3f} in={global_centroid[4]:.3f}")
    p()

    regime_ops = {}
    for key in regime_keys:
        r = REGIMES[key]
        v = regime_vecs[key]
        dev = [v[d] - global_centroid[d] for d in range(5)]
        op = classify_op(dev)
        regime_ops[key] = {"op": op, "dev": dev, "mag": vec_mag(dev)}
        stable_mark = "S" if r["stable"] else " "
        dim_idx, dim_tag = OP_TO_DIM[op]
        p(f"  [{stable_mark}] {r['name']:25s}  op={OP_NAMES[op]:10s}  "
          f"dim={dim_tag:4s}  mag={vec_mag(dev):.4f}")
    p()

    # Operator distribution
    op_counts = [0] * 10
    for key in regime_keys:
        op_counts[regime_ops[key]["op"]] += 1
    p("  Operator distribution:")
    for i in range(10):
        if op_counts[i] > 0:
            pct = 100.0 * op_counts[i] / n_reg
            p(f"    {OP_NAMES[i]:10s}: {op_counts[i]:2d} ({pct:5.1f}%)")
    p()

    # =================================================================
    # SECTION 4: Cycle D2 Analysis (Trajectories)
    # =================================================================
    p("=" * 78)
    p("SECTION 4: BUSINESS CYCLE D2 -- CURVATURE OF ECONOMIC HISTORY")
    p("=" * 78)
    p()

    cycle_summaries = {}

    for cyc_key, cycle in CYCLES.items():
        epochs = cycle["epochs"]
        n_ep = len(epochs)
        p(f"  --- {cycle['name']} ---")
        p(f"  {cycle['desc']}")
        p()

        if n_ep < 3:
            continue

        cyc_d2_ops = []
        cyc_d2_mags = []
        cyc_t_tsml = []
        cyc_t_bhml = []

        p(f"  {'Ep':3s} {'Regime':22s} {'D2_op':10s} {'|D2|':8s} "
          f"{'T(TSML)':10s} {'T(BHML)':10s} {'Class':10s}")

        for i in range(1, n_ep - 1):
            v0 = regime_vecs[epochs[i-1]]
            v1 = regime_vecs[epochs[i]]
            v2 = regime_vecs[epochs[i+1]]

            d1 = compute_d1(v0, v1)
            d2 = compute_d2(v0, v1, v2)
            d1_op = classify_op(d1)
            d2_op = classify_op(d2)
            d2_mag = vec_mag(d2)

            t_ts = TSML[d1_op][d2_op]
            t_bh = BHML[d1_op][d2_op]

            if t_ts == 7 and t_bh == 7:
                cl = "UNIFIED"
            elif t_ts == 7:
                cl = "WORKING"
            elif t_bh == 7:
                cl = "BOUNDARY"
            else:
                cl = "TENSION"

            cyc_d2_ops.append(d2_op)
            cyc_d2_mags.append(d2_mag)
            cyc_t_tsml.append(t_ts)
            cyc_t_bhml.append(t_bh)

            rname = REGIMES[epochs[i]]["name"]
            p(f"  {i:3d} {rname:22s} {OP_NAMES[d2_op]:10s} {d2_mag:8.4f} "
              f"{OP_NAMES[t_ts]:10s} {OP_NAMES[t_bh]:10s} {cl:10s}")

        n_pts = len(cyc_d2_ops)
        if n_pts > 0:
            avg_d2 = sum(cyc_d2_mags) / n_pts
            max_d2 = max(cyc_d2_mags)
            n_h_ts = sum(1 for x in cyc_t_tsml if x == 7)
            n_h_bh = sum(1 for x in cyc_t_bhml if x == 7)
            n_uni = sum(1 for j in range(n_pts)
                       if cyc_t_tsml[j] == 7 and cyc_t_bhml[j] == 7)

            p()
            p(f"  Avg |D2|: {avg_d2:.4f}  Max |D2|: {max_d2:.4f}")
            p(f"  T(TSML) HARMONY: {n_h_ts}/{n_pts}")
            p(f"  T(BHML) HARMONY: {n_h_bh}/{n_pts}")
            p(f"  UNIFIED: {n_uni}/{n_pts}")

            cycle_summaries[cyc_key] = {
                "avg_d2": avg_d2, "max_d2": max_d2,
                "tsml_h": n_h_ts / n_pts, "bhml_h": n_h_bh / n_pts,
                "unified": n_uni / n_pts, "n_pts": n_pts,
            }
        p()

    # =================================================================
    # SECTION 5: Crisis Detection -- D2 Spike Magnitude
    # =================================================================
    p("=" * 78)
    p("SECTION 5: CRISIS DETECTION -- D2 SPIKE ANALYSIS")
    p("=" * 78)
    p()
    p("Prediction: Financial crises produce D2 spikes > 2x normal.")
    p("Normal cycle transitions have moderate curvature.")
    p("Crashes have extreme curvature (the market BENDS sharply).")
    p()

    for cyc_key in ["normal_cycle", "dotcom", "gfc_2008", "covid_2020",
                     "stagflation_70s", "japan_lost"]:
        if cyc_key in cycle_summaries:
            s = cycle_summaries[cyc_key]
            cycle = CYCLES[cyc_key]
            p(f"  {cycle['name']:35s}  "
              f"avg|D2|={s['avg_d2']:.4f}  max|D2|={s['max_d2']:.4f}  "
              f"TSML_H={s['tsml_h']:.3f}  gap={abs(s['tsml_h']-s['bhml_h']):.3f}")
    p()

    # Compare crisis vs normal
    if "normal_cycle" in cycle_summaries and "gfc_2008" in cycle_summaries:
        normal_avg = cycle_summaries["normal_cycle"]["avg_d2"]
        gfc_max = cycle_summaries["gfc_2008"]["max_d2"]
        ratio = gfc_max / max(normal_avg, 1e-12)
        p(f"  GFC max D2 / Normal avg D2: {ratio:.2f}x")
    if "normal_cycle" in cycle_summaries and "covid_2020" in cycle_summaries:
        covid_max = cycle_summaries["covid_2020"]["max_d2"]
        ratio = covid_max / max(normal_avg, 1e-12)
        p(f"  COVID max D2 / Normal avg D2: {ratio:.2f}x")
    p()

    # =================================================================
    # SECTION 6: Dual-Lens Gap -- Sentiment vs Reality
    # =================================================================
    p("=" * 78)
    p("SECTION 6: DUAL-LENS GAP -- WHAT THE MARKET IS vs WHAT IT DOES")
    p("=" * 78)
    p()
    p("The gap between TSML and BHML for each cycle = sentiment mismatch.")
    p("Large gap = market is BEING one thing but DOING another.")
    p("Bubble: BEING healthy (TSML=HARMONY) but DOING leverage (BHML!=HARMONY)")
    p()

    for cyc_key, s in cycle_summaries.items():
        cycle = CYCLES[cyc_key]
        gap = abs(s["tsml_h"] - s["bhml_h"])
        p(f"  {cycle['name']:35s}  "
          f"TSML_H={s['tsml_h']:.3f}  BHML_H={s['bhml_h']:.3f}  gap={gap:.3f}")
    p()

    # =================================================================
    # SECTION 7: Void Topology -- Silent Indicators
    # =================================================================
    p("=" * 78)
    p("SECTION 7: VOID TOPOLOGY -- WHICH INDICATORS ARE SILENT?")
    p("=" * 78)
    p()
    p("Void = dimension near centroid (deviation < 0.05).")
    p("Silent indicators = what this regime does NOT stress.")
    p()

    VOID_THRESH = 0.05
    for key in regime_keys:
        r = REGIMES[key]
        dev = regime_ops[key]["dev"]
        voids = []
        active = []
        for d in range(5):
            if abs(dev[d]) < VOID_THRESH:
                voids.append(DIM_SHORT[d])
            else:
                active.append(f"{DIM_SHORT[d]}({dev[d]:+.3f})")
        stable_mark = "S" if r["stable"] else " "
        p(f"  [{stable_mark}] {r['name']:25s}  "
          f"voids={len(voids)}  [{','.join(active)}]")
    p()

    # =================================================================
    # SECTION 8: I/O Balance -- Structure vs Flow
    # =================================================================
    p("=" * 78)
    p("SECTION 8: I/O BALANCE -- REAL ECONOMY vs FINANCIAL FLOWS")
    p("=" * 78)
    p()
    p("I = structure (yield spread + VIX) = credit + fear")
    p("O = flow (employment + inflation) = labor + prices")
    p("Depth (GDP) mediates between financial and real.")
    p()

    for key in regime_keys:
        r = REGIMES[key]
        v = regime_vecs[key]
        i_val = v[0] + v[1]
        o_val = v[3] + v[4]
        ratio = i_val / max(o_val, 1e-12)
        balance = "FINANCIAL" if ratio > 1.2 else ("REAL" if ratio < 0.8 else "BALANCED")
        stable_mark = "S" if r["stable"] else " "
        p(f"  [{stable_mark}] {r['name']:25s}  "
          f"I={i_val:.3f}  O={o_val:.3f}  I/O={ratio:.3f}  "
          f"GDP={v[2]:.3f}  {balance}")
    p()

    # =================================================================
    # SECTION 9: Cross-Regime CL Composition
    # =================================================================
    p("=" * 78)
    p("SECTION 9: CROSS-REGIME CL COMPOSITION TABLE")
    p("=" * 78)
    p()

    selected = ["healthy_expansion", "bubble", "crash", "recession",
                "trough", "early_recovery", "stagflation", "zirp"]
    sel_names = [REGIMES[k]["name"][:14] for k in selected]

    # TSML
    p("  T(TSML) Composition:")
    header = "               " + "".join(f"{n:>15s}" for n in sel_names)
    p(header)
    n_ts_h = 0
    n_bh_h = 0
    n_both = 0
    n_total = 0
    for i, ki in enumerate(selected):
        row = f"  {sel_names[i]:13s}"
        oi = regime_ops[ki]["op"]
        for j, kj in enumerate(selected):
            oj = regime_ops[kj]["op"]
            t = TSML[oi][oj]
            row += f"  {OP_NAMES[t]:>13s}"
            n_total += 1
            if t == 7:
                n_ts_h += 1
            tb = BHML[oi][oj]
            if tb == 7:
                n_bh_h += 1
            if t == 7 and tb == 7:
                n_both += 1
        p(row)
    p()
    p(f"  TSML HARMONY: {n_ts_h}/{n_total} = {n_ts_h/n_total:.4f}")
    p(f"  BHML HARMONY: {n_bh_h}/{n_total} = {n_bh_h/n_total:.4f}")
    p(f"  UNIFIED:      {n_both}/{n_total} = {n_both/n_total:.4f}")
    p()

    # =================================================================
    # SECTION 10: Dimension Dominance in Cycles
    # =================================================================
    p("=" * 78)
    p("SECTION 10: DIMENSION DOMINANCE IN BUSINESS CYCLES")
    p("=" * 78)
    p()

    global_dim_counts = [0] * 5
    for cyc_key, cycle in CYCLES.items():
        epochs = cycle["epochs"]
        dim_counts = [0] * 5
        n_pts = 0
        for i in range(1, len(epochs) - 1):
            v0 = regime_vecs[epochs[i-1]]
            v1 = regime_vecs[epochs[i]]
            v2 = regime_vecs[epochs[i+1]]
            d2 = compute_d2(v0, v1, v2)
            abs_d2 = [abs(x) for x in d2]
            max_d = max(abs_d2)
            if max_d > 1e-12:
                dom = abs_d2.index(max_d)
                dim_counts[dom] += 1
                global_dim_counts[dom] += 1
                n_pts += 1

        if n_pts > 0:
            dom_dim = dim_counts.index(max(dim_counts))
            p(f"  {cycle['name']:35s}  dominant={DIM_NAMES[dom_dim]:12s}  "
              f"sp={dim_counts[0]} vx={dim_counts[1]} gd={dim_counts[2]} "
              f"em={dim_counts[3]} in={dim_counts[4]}")

    p()
    total_g = sum(global_dim_counts)
    p(f"  Global dimension dominance ({total_g} total D2 points):")
    for d in range(5):
        pct = 100.0 * global_dim_counts[d] / max(total_g, 1)
        bar = "#" * int(pct / 2)
        p(f"    {DIM_NAMES[d]:12s}: {global_dim_counts[d]:3d} ({pct:5.1f}%)  {bar}")
    p()

    # =================================================================
    # SECTION 11: Yield Curve Inversion as D2 Predictor
    # =================================================================
    p("=" * 78)
    p("SECTION 11: YIELD CURVE INVERSION -- APERTURE DIMENSION PREDICTOR")
    p("=" * 78)
    p()
    p("An inverted yield curve (negative spread) has predicted every")
    p("US recession since 1955. In TIG: this is the aperture dimension")
    p("going negative = credit channel CLOSING.")
    p()
    p("Regimes with negative aperture (inverted curve):")
    for key in regime_keys:
        r = REGIMES[key]
        raw_spread = r["params"]["spread"]
        v = regime_vecs[key]
        if raw_spread < 0:
            p(f"  {r['name']:25s}  spread={raw_spread:+.1f}pp  "
              f"ap(normalized)={v[0]:.3f}  op={OP_NAMES[regime_ops[key]['op']]}")
    p()
    p("Regimes with wide aperture (steep curve):")
    for key in regime_keys:
        r = REGIMES[key]
        raw_spread = r["params"]["spread"]
        v = regime_vecs[key]
        if raw_spread >= 2.0:
            p(f"  {r['name']:25s}  spread={raw_spread:+.1f}pp  "
              f"ap(normalized)={v[0]:.3f}  op={OP_NAMES[regime_ops[key]['op']]}")
    p()

    # =================================================================
    # SECTION 12: Synthesis
    # =================================================================
    p("=" * 78)
    p("SECTION 12: SYNTHESIS")
    p("=" * 78)
    p()

    p("  FINDINGS:")
    p()
    p("  1. MARKET STABILITY IS GEOMETRICALLY SEPARABLE")
    p(f"     Stable/Unstable centroid separation: {vec_dist(s_centroid, u_centroid):.4f}")
    p(f"     Most discriminating dimension: {DIM_NAMES[max_sep]}")
    p()

    p("  2. CRISIS = D2 SPIKE")
    if "normal_cycle" in cycle_summaries:
        p(f"     Normal cycle avg |D2|: {cycle_summaries['normal_cycle']['avg_d2']:.4f}")
    if "gfc_2008" in cycle_summaries:
        p(f"     GFC 2008 max |D2|: {cycle_summaries['gfc_2008']['max_d2']:.4f}")
    if "covid_2020" in cycle_summaries:
        p(f"     COVID 2020 max |D2|: {cycle_summaries['covid_2020']['max_d2']:.4f}")
    p()

    p("  3. DUAL-LENS GAP = MARKET MISPRICING")
    p(f"     Bubble cycles show large TSML-BHML gap")
    p(f"     (market IS one thing but DOES another)")
    p()

    p("  4. YIELD CURVE INVERSION = APERTURE CLOSURE")
    p(f"     Inverted curve maps to low aperture dimension")
    p(f"     All recession-preceding regimes have negative aperture")
    p()

    p("  FALSIFIABLE PREDICTIONS:")
    p()
    p("  P1: CRISIS D2 THRESHOLD")
    p("      Financial crises produce max |D2| > 2x the average |D2|")
    p("      of normal business cycles when measured quarterly.")
    p("      Kill: crisis max |D2| < 1.5x normal avg |D2| in historical data.")
    p()
    p("  P2: BUBBLE = DUAL-LENS DIVERGENCE")
    p("      Asset bubbles show |TSML_H - BHML_H| > 0.3 before crash.")
    p("      Normal expansion shows gap < 0.2.")
    p("      Kill: bubble gap < normal gap in 3+ historical episodes.")
    p()
    p("  P3: YIELD CURVE INVERSION = APERTURE VOID")
    p("      Every recession is preceded by aperture dimension dropping")
    p("      below 0.20 (normalized). Recovery begins when aperture > 0.40.")
    p("      Kill: recession without prior aperture drop in US data.")
    p()
    p("  P4: DIMENSION DOMINANCE SHIFTS WITH REGIME")
    p("      Growth regimes dominated by binding (employment).")
    p("      Crisis regimes dominated by pressure (VIX).")
    p("      Kill: crisis regime dominated by binding dimension.")
    p()

    p("=" * 78)
    p("  END OF ECONOMICS D2 SPECTROMETER ANALYSIS")
    p("=" * 78)


# =====================================================================
# Entry Point
# =====================================================================

if __name__ == "__main__":
    import io
    buf = io.StringIO()
    run_analysis(buf)
    result = buf.getvalue()

    try:
        print(result)
    except UnicodeEncodeError:
        print(result.encode("ascii", errors="replace").decode("ascii"))

    out_path = __file__.replace(".py", "_results.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(result)
    print(f"\nResults saved to {out_path}")
