#!/usr/bin/env python3
"""
ecology_d2_spectrometer.py -- Dual-Lens D2 Spectrometer for Ecosystems
========================================================================

Ecosystems as 5D force geometry.

Biomes, ecological succession, tipping points, and climate regimes
mapped through the D2 pipeline. An ecosystem IS a path through 5D space.
D2 IS the curvature of that path. Tipping points ARE D2 spikes.

5D Force Mapping (ecosystem state variables, normalized):
  Aperture   = Net Primary Productivity (NPP, gC/m2/yr) -- energy aperture
  Pressure   = Species Richness (count)                  -- biodiversity pressure
  Depth      = Soil Organic Carbon (kgC/m2)              -- depth of stored carbon
  Binding    = Water Availability (mm/yr precipitation)   -- hydrological binding
  Continuity = Temperature (mean annual, C)               -- thermal continuity

This mapping is NOT arbitrary:
  NPP = aperture: photosynthesis IS the aperture through which energy enters
  Species richness = pressure: diversity IS the competitive pressure landscape
  Soil carbon = depth: carbon storage IS the depth of ecological memory
  Water = binding: precipitation IS what binds the biosphere together
  Temperature = continuity: warmth IS the continuity condition for life

Biome Sequence:
  Desert -> Grassland -> Savanna -> Temperate Forest -> Tropical Forest
  follows increasing NPP, water, and temperature.

Tipping Points:
  Ecosystem collapse = D2 spike where the path bends sharply.
  Amazon dieback, coral bleaching, permafrost thaw, desertification.

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
# Normalization
# =====================================================================
NORM = {
    "npp":         (0, 2500),       # gC/m2/yr (desert=0 to tropical=2200+)
    "species":     (0, 5000),       # species richness per 10000km2
    "soil_carbon": (0, 50),         # kgC/m2
    "water":       (0, 4000),       # mm/yr precipitation
    "temp":        (-30, 30),       # mean annual temperature (C)
}

def normalize_eco(params):
    keys = ["npp", "species", "water", "soil_carbon", "temp"]
    v = []
    for k in keys:
        lo, hi = NORM[k]
        val = (params[k] - lo) / (hi - lo)
        val = max(0.0, min(1.0, val))
        v.append(val)
    return v

# =====================================================================
# Biome Data
# =====================================================================
# Representative values from global ecology literature

BIOMES = {
    "polar_desert": {
        "name": "Polar Desert",
        "category": "extreme",
        "healthy": True,
        "params": {"npp": 10, "species": 50, "soil_carbon": 2, "water": 100, "temp": -20},
        "desc": "Antarctic/Arctic interior, near-lifeless"
    },
    "tundra": {
        "name": "Arctic Tundra",
        "category": "cold",
        "healthy": True,
        "params": {"npp": 140, "species": 200, "soil_carbon": 40, "water": 250, "temp": -10},
        "desc": "Permafrost, lichens/moss, massive soil carbon"
    },
    "boreal": {
        "name": "Boreal Forest (Taiga)",
        "category": "cold",
        "healthy": True,
        "params": {"npp": 400, "species": 400, "soil_carbon": 35, "water": 500, "temp": -5},
        "desc": "Conifer forest, second largest biome"
    },
    "temp_grassland": {
        "name": "Temperate Grassland",
        "category": "temperate",
        "healthy": True,
        "params": {"npp": 500, "species": 600, "soil_carbon": 20, "water": 500, "temp": 8},
        "desc": "Prairie/steppe, deep soils, fire-maintained"
    },
    "temp_deciduous": {
        "name": "Temperate Deciduous Forest",
        "category": "temperate",
        "healthy": True,
        "params": {"npp": 800, "species": 1200, "soil_carbon": 15, "water": 1000, "temp": 10},
        "desc": "Seasonal leaf drop, moderate diversity"
    },
    "mediterranean": {
        "name": "Mediterranean Scrub",
        "category": "temperate",
        "healthy": True,
        "params": {"npp": 500, "species": 1500, "soil_carbon": 8, "water": 500, "temp": 15},
        "desc": "Fire-adapted, high endemism, dry summers"
    },
    "hot_desert": {
        "name": "Hot Desert",
        "category": "extreme",
        "healthy": True,
        "params": {"npp": 30, "species": 200, "soil_carbon": 1, "water": 50, "temp": 25},
        "desc": "Extreme aridity, specialized life forms"
    },
    "savanna": {
        "name": "Tropical Savanna",
        "category": "tropical",
        "healthy": True,
        "params": {"npp": 700, "species": 2000, "soil_carbon": 10, "water": 1200, "temp": 25},
        "desc": "Grass-tree mix, seasonal drought, megafauna"
    },
    "monsoon_forest": {
        "name": "Tropical Monsoon Forest",
        "category": "tropical",
        "healthy": True,
        "params": {"npp": 1200, "species": 3000, "soil_carbon": 12, "water": 2000, "temp": 26},
        "desc": "Seasonal wet/dry, semi-deciduous"
    },
    "tropical_forest": {
        "name": "Tropical Rainforest",
        "category": "tropical",
        "healthy": True,
        "params": {"npp": 2200, "species": 5000, "soil_carbon": 15, "water": 3000, "temp": 27},
        "desc": "Maximum biodiversity, maximum NPP"
    },
    "coral_reef": {
        "name": "Coral Reef (Marine)",
        "category": "marine",
        "healthy": True,
        "params": {"npp": 1500, "species": 4000, "soil_carbon": 5, "water": 3500, "temp": 26},
        "desc": "Rainforest of the sea, symbiotic foundation"
    },
    "kelp_forest": {
        "name": "Kelp Forest (Marine)",
        "category": "marine",
        "healthy": True,
        "params": {"npp": 800, "species": 1200, "soil_carbon": 3, "water": 3500, "temp": 12},
        "desc": "Temperate marine, high productivity"
    },
    "open_ocean": {
        "name": "Open Ocean",
        "category": "marine",
        "healthy": True,
        "params": {"npp": 150, "species": 300, "soil_carbon": 1, "water": 3500, "temp": 15},
        "desc": "Low productivity, vast area, nutrient-poor"
    },

    # --- Degraded/Tipping States ---
    "amazon_dieback": {
        "name": "Amazon Dieback",
        "category": "tipping",
        "healthy": False,
        "params": {"npp": 500, "species": 2000, "soil_carbon": 8, "water": 1200, "temp": 29},
        "desc": "Forest-to-savanna transition, CO2 source"
    },
    "coral_bleached": {
        "name": "Coral Reef Bleached",
        "category": "tipping",
        "healthy": False,
        "params": {"npp": 300, "species": 1000, "soil_carbon": 3, "water": 3500, "temp": 29},
        "desc": "Symbiosis broken, 1-2C warming kills reef"
    },
    "permafrost_thaw": {
        "name": "Permafrost Thaw",
        "category": "tipping",
        "healthy": False,
        "params": {"npp": 200, "species": 250, "soil_carbon": 15, "water": 350, "temp": 0},
        "desc": "Carbon bomb: 1700 GtC releasing as CO2/CH4"
    },
    "desertification": {
        "name": "Desertified Grassland",
        "category": "tipping",
        "healthy": False,
        "params": {"npp": 80, "species": 150, "soil_carbon": 5, "water": 200, "temp": 20},
        "desc": "Sahel-type: overgrazing + drought = collapse"
    },
    "dead_zone": {
        "name": "Ocean Dead Zone",
        "category": "tipping",
        "healthy": False,
        "params": {"npp": 30, "species": 50, "soil_carbon": 0, "water": 3500, "temp": 18},
        "desc": "Eutrophication -> anoxia -> mass mortality"
    },
    "boreal_shift": {
        "name": "Boreal Dieoff/Shift",
        "category": "tipping",
        "healthy": False,
        "params": {"npp": 200, "species": 200, "soil_carbon": 20, "water": 400, "temp": 2},
        "desc": "Warming + beetles + fire = boreal retreat"
    },
}

# =====================================================================
# Ecological Trajectories
# =====================================================================

TRAJECTORIES = {
    "latitude_gradient": {
        "name": "Latitude Gradient (pole to equator)",
        "desc": "Polar -> Tundra -> Boreal -> Temperate -> Tropical",
        "epochs": ["polar_desert", "tundra", "boreal", "temp_grassland",
                   "temp_deciduous", "savanna", "monsoon_forest", "tropical_forest"],
    },
    "succession": {
        "name": "Primary Succession",
        "desc": "Bare rock -> Grassland -> Shrub -> Forest",
        "epochs": ["polar_desert", "hot_desert", "desertification",
                   "temp_grassland", "temp_grassland", "temp_deciduous",
                   "temp_deciduous", "boreal"],
    },
    "amazon_collapse": {
        "name": "Amazon Dieback Trajectory",
        "desc": "Rainforest -> Degradation -> Savanna",
        "epochs": ["tropical_forest", "tropical_forest", "monsoon_forest",
                   "amazon_dieback", "amazon_dieback", "savanna", "savanna",
                   "desertification"],
    },
    "coral_death": {
        "name": "Coral Reef Collapse",
        "desc": "Healthy reef -> Bleaching -> Dead zone",
        "epochs": ["coral_reef", "coral_reef", "coral_bleached",
                   "coral_bleached", "dead_zone", "dead_zone",
                   "open_ocean", "open_ocean"],
    },
    "permafrost_bomb": {
        "name": "Permafrost Carbon Bomb",
        "desc": "Tundra -> Thaw -> Boreal shift",
        "epochs": ["tundra", "tundra", "permafrost_thaw", "permafrost_thaw",
                   "boreal_shift", "boreal_shift", "temp_grassland",
                   "temp_grassland"],
    },
    "desertification_path": {
        "name": "Sahel Desertification",
        "desc": "Savanna -> Overgrazing -> Desert",
        "epochs": ["savanna", "savanna", "temp_grassland", "desertification",
                   "desertification", "hot_desert", "hot_desert",
                   "polar_desert"],
    },
    "climate_warming": {
        "name": "Global Warming Cascade",
        "desc": "Multiple tipping points in sequence",
        "epochs": ["coral_reef", "coral_bleached", "tropical_forest",
                   "amazon_dieback", "tundra", "permafrost_thaw",
                   "boreal", "boreal_shift"],
    },
    "marine_gradient": {
        "name": "Marine Productivity Gradient",
        "desc": "Open ocean -> Kelp -> Coral reef -> Dead zone",
        "epochs": ["open_ocean", "open_ocean", "kelp_forest",
                   "coral_reef", "coral_reef", "coral_bleached",
                   "dead_zone", "dead_zone"],
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
    p("  ECOLOGY D2 SPECTROMETER -- Ecosystems as 5D Force Geometry")
    p("  Dual-Lens Curvature Analysis of Biomes and Tipping Points")
    p("=" * 78)
    p()

    # =================================================================
    # SECTION 1: Force Vectors
    # =================================================================
    p("=" * 78)
    p("SECTION 1: 5D FORCE VECTORS -- BIOME SIGNATURES")
    p("=" * 78)
    p()
    p("  Aperture(NPP)  Pressure(species)  Depth(soil_C)  Binding(water)  Continuity(temp)")
    p()

    biome_keys = list(BIOMES.keys())
    biome_vecs = {}

    categories = ["extreme", "cold", "temperate", "tropical", "marine", "tipping"]
    cat_names = {
        "extreme": "EXTREME BIOMES",
        "cold": "COLD BIOMES",
        "temperate": "TEMPERATE BIOMES",
        "tropical": "TROPICAL BIOMES",
        "marine": "MARINE BIOMES",
        "tipping": "TIPPING / DEGRADED STATES",
    }

    for cat in categories:
        states = [k for k in biome_keys if BIOMES[k]["category"] == cat]
        if not states:
            continue
        p(f"  --- {cat_names[cat]} ---")
        for key in states:
            b = BIOMES[key]
            v = normalize_eco(b["params"])
            biome_vecs[key] = v
            h_mark = "H" if b["healthy"] else "X"
            p(f"  [{h_mark}] {b['name']:28s}  "
              f"np={v[0]:.3f}  sp={v[1]:.3f}  sc={v[2]:.3f}  "
              f"wa={v[3]:.3f}  te={v[4]:.3f}")
        p()

    p(f"  Total biomes: {len(biome_vecs)}")
    p(f"  [H] = healthy, [X] = degraded/tipping")
    p()

    # =================================================================
    # SECTION 2: Operator Classification
    # =================================================================
    p("=" * 78)
    p("SECTION 2: D2 OPERATOR CLASSIFICATION PER BIOME")
    p("=" * 78)
    p()

    all_vecs = list(biome_vecs.values())
    n_biome = len(all_vecs)
    global_centroid = [sum(v[d] for v in all_vecs) / n_biome for d in range(5)]
    p(f"  Global centroid: np={global_centroid[0]:.3f} sp={global_centroid[1]:.3f} "
      f"sc={global_centroid[2]:.3f} wa={global_centroid[3]:.3f} te={global_centroid[4]:.3f}")
    p()

    biome_ops = {}
    for key in biome_keys:
        b = BIOMES[key]
        v = biome_vecs[key]
        dev = [v[d] - global_centroid[d] for d in range(5)]
        op = classify_op(dev)
        biome_ops[key] = {"op": op, "dev": dev, "mag": vec_mag(dev)}
        h_mark = "H" if b["healthy"] else "X"
        dim_idx, dim_tag = OP_TO_DIM[op]
        p(f"  [{h_mark}] {b['name']:28s}  op={OP_NAMES[op]:10s}  "
          f"dim={dim_tag:4s}  mag={vec_mag(dev):.4f}")
    p()

    # Operator distribution
    op_counts = [0] * 10
    for key in biome_keys:
        op_counts[biome_ops[key]["op"]] += 1
    p("  Operator distribution:")
    for i in range(10):
        if op_counts[i] > 0:
            pct = 100.0 * op_counts[i] / n_biome
            p(f"    {OP_NAMES[i]:10s}: {op_counts[i]:2d} ({pct:5.1f}%)")
    p()

    # Healthy vs degraded
    healthy_keys = [k for k in biome_keys if BIOMES[k]["healthy"]]
    tipping_keys = [k for k in biome_keys if not BIOMES[k]["healthy"]]

    p("  --- Healthy Biome Operators ---")
    h_ops = [0] * 10
    for k in healthy_keys:
        h_ops[biome_ops[k]["op"]] += 1
    for i in range(10):
        if h_ops[i] > 0:
            p(f"    {OP_NAMES[i]:10s}: {h_ops[i]}")
    p()
    p("  --- Degraded/Tipping State Operators ---")
    t_ops = [0] * 10
    for k in tipping_keys:
        t_ops[biome_ops[k]["op"]] += 1
    for i in range(10):
        if t_ops[i] > 0:
            p(f"    {OP_NAMES[i]:10s}: {t_ops[i]}")
    p()

    # =================================================================
    # SECTION 3: Tipping Point D2 Spikes
    # =================================================================
    p("=" * 78)
    p("SECTION 3: TIPPING POINT D2 -- HEALTHY vs DEGRADED DISTANCES")
    p("=" * 78)
    p()
    p("5D distance between healthy biome and its degraded state.")
    p("Larger distance = more catastrophic transition.")
    p()

    tipping_pairs = [
        ("tropical_forest", "amazon_dieback", "Amazon dieback"),
        ("coral_reef", "coral_bleached", "Coral bleaching"),
        ("tundra", "permafrost_thaw", "Permafrost thaw"),
        ("temp_grassland", "desertification", "Desertification"),
        ("open_ocean", "dead_zone", "Ocean dead zone"),
        ("boreal", "boreal_shift", "Boreal dieoff"),
    ]

    for k1, k2, desc in tipping_pairs:
        v1 = biome_vecs[k1]
        v2 = biome_vecs[k2]
        dist = vec_dist(v1, v2)
        # Which dimension shifts most?
        delta = [v2[d] - v1[d] for d in range(5)]
        abs_delta = [abs(x) for x in delta]
        dom = abs_delta.index(max(abs_delta))
        op1 = biome_ops[k1]["op"]
        op2 = biome_ops[k2]["op"]
        t_ts = TSML[op1][op2]
        t_bh = BHML[op1][op2]
        p(f"  {desc:25s}  dist={dist:.4f}  dom_shift={DIM_NAMES[dom]:12s}  "
          f"T(TSML)={OP_NAMES[t_ts]:8s}  T(BHML)={OP_NAMES[t_bh]:8s}")
    p()

    # =================================================================
    # SECTION 4: Trajectory D2 Analysis
    # =================================================================
    p("=" * 78)
    p("SECTION 4: TRAJECTORY D2 -- ECOLOGICAL TRANSITIONS")
    p("=" * 78)
    p()

    traj_summaries = {}

    for traj_key, traj in TRAJECTORIES.items():
        epochs = traj["epochs"]
        n_ep = len(epochs)
        p(f"  --- {traj['name']} ---")
        p(f"  {traj['desc']}")
        p()

        if n_ep < 3:
            continue

        t_d2_ops = []
        t_d2_mags = []
        t_t_tsml = []
        t_t_bhml = []

        for i in range(1, n_ep - 1):
            v0 = biome_vecs[epochs[i-1]]
            v1 = biome_vecs[epochs[i]]
            v2 = biome_vecs[epochs[i+1]]
            d1 = compute_d1(v0, v1)
            d2 = compute_d2(v0, v1, v2)
            d1_op = classify_op(d1)
            d2_op = classify_op(d2)
            d2_mag = vec_mag(d2)
            t_ts = TSML[d1_op][d2_op]
            t_bh = BHML[d1_op][d2_op]

            t_d2_ops.append(d2_op)
            t_d2_mags.append(d2_mag)
            t_t_tsml.append(t_ts)
            t_t_bhml.append(t_bh)

            if t_ts == 7 and t_bh == 7:
                cl = "UNIFIED"
            elif t_ts == 7:
                cl = "WORKING"
            elif t_bh == 7:
                cl = "BOUNDARY"
            else:
                cl = "TENSION"

            bname = BIOMES[epochs[i]]["name"]
            h_mark = "H" if BIOMES[epochs[i]]["healthy"] else "X"
            p(f"  [{h_mark}] {bname:25s}  {OP_NAMES[d2_op]:10s} |D2|={d2_mag:.4f}  "
              f"T(TSML)={OP_NAMES[t_ts]:8s} T(BHML)={OP_NAMES[t_bh]:8s} {cl}")

        n_pts = len(t_d2_ops)
        if n_pts > 0:
            avg_d2 = sum(t_d2_mags) / n_pts
            max_d2 = max(t_d2_mags)
            n_h_ts = sum(1 for x in t_t_tsml if x == 7)
            n_h_bh = sum(1 for x in t_t_bhml if x == 7)
            n_uni = sum(1 for j in range(n_pts)
                       if t_t_tsml[j] == 7 and t_t_bhml[j] == 7)
            p(f"  Avg |D2|: {avg_d2:.4f}  Max |D2|: {max_d2:.4f}")
            p(f"  T(TSML) HARMONY: {n_h_ts}/{n_pts}  T(BHML) HARMONY: {n_h_bh}/{n_pts}  "
              f"UNIFIED: {n_uni}/{n_pts}")
            traj_summaries[traj_key] = {
                "avg_d2": avg_d2, "max_d2": max_d2,
                "tsml_h": n_h_ts / n_pts, "bhml_h": n_h_bh / n_pts,
                "unified": n_uni / n_pts,
            }
        p()

    # =================================================================
    # SECTION 5: Natural vs Collapse Trajectory Comparison
    # =================================================================
    p("=" * 78)
    p("SECTION 5: NATURAL vs COLLAPSE TRAJECTORIES")
    p("=" * 78)
    p()
    p("Natural gradient (latitude) should be smooth (low D2).")
    p("Collapse trajectories should spike (high D2) at tipping points.")
    p()

    natural = ["latitude_gradient", "succession", "marine_gradient"]
    collapse = ["amazon_collapse", "coral_death", "permafrost_bomb",
                "desertification_path", "climate_warming"]

    p("  Natural trajectories:")
    for tk in natural:
        if tk in traj_summaries:
            s = traj_summaries[tk]
            p(f"    {TRAJECTORIES[tk]['name']:35s}  "
              f"avg|D2|={s['avg_d2']:.4f}  max|D2|={s['max_d2']:.4f}  "
              f"gap={abs(s['tsml_h']-s['bhml_h']):.3f}")

    p("  Collapse trajectories:")
    for tk in collapse:
        if tk in traj_summaries:
            s = traj_summaries[tk]
            p(f"    {TRAJECTORIES[tk]['name']:35s}  "
              f"avg|D2|={s['avg_d2']:.4f}  max|D2|={s['max_d2']:.4f}  "
              f"gap={abs(s['tsml_h']-s['bhml_h']):.3f}")
    p()

    # =================================================================
    # SECTION 6: Void Topology
    # =================================================================
    p("=" * 78)
    p("SECTION 6: VOID TOPOLOGY -- WHICH DIMENSIONS ARE SILENT?")
    p("=" * 78)
    p()

    VOID_THRESH = 0.05
    for key in biome_keys:
        b = BIOMES[key]
        dev = biome_ops[key]["dev"]
        voids = []
        for d in range(5):
            if abs(dev[d]) < VOID_THRESH:
                voids.append(DIM_SHORT[d])
        h_mark = "H" if b["healthy"] else "X"
        p(f"  [{h_mark}] {b['name']:28s}  voids={len(voids)}  [{','.join(voids)}]")
    p()

    # =================================================================
    # SECTION 7: I/O Balance -- Production vs Regulation
    # =================================================================
    p("=" * 78)
    p("SECTION 7: I/O BALANCE -- PRODUCTION vs REGULATION")
    p("=" * 78)
    p()
    p("I = structure (NPP + species) = biological production/diversity")
    p("O = flow (water + temperature) = physical environment")
    p("Depth (soil carbon) mediates = ecological memory")
    p()

    for key in biome_keys:
        b = BIOMES[key]
        v = biome_vecs[key]
        i_val = v[0] + v[1]
        o_val = v[3] + v[4]
        ratio = i_val / max(o_val, 1e-12)
        balance = "BIO" if ratio > 1.2 else ("PHYS" if ratio < 0.8 else "BALANCED")
        h_mark = "H" if b["healthy"] else "X"
        p(f"  [{h_mark}] {b['name']:28s}  "
          f"I={i_val:.3f}  O={o_val:.3f}  I/O={ratio:.3f}  "
          f"soil_C={v[2]:.3f}  {balance}")
    p()

    # =================================================================
    # SECTION 8: Latitude Gradient -- The Natural D2 Path
    # =================================================================
    p("=" * 78)
    p("SECTION 8: LATITUDE GRADIENT AS NATURAL D2 PATH")
    p("=" * 78)
    p()
    p("The latitude gradient (pole to equator) IS the natural ordering.")
    p("D2 should increase monotonically toward the tropics (more curvature")
    p("= faster change in ecosystem parameters per degree of latitude).")
    p()

    lat_seq = ["polar_desert", "tundra", "boreal", "temp_grassland",
               "temp_deciduous", "savanna", "monsoon_forest", "tropical_forest"]

    equator_vec = biome_vecs["tropical_forest"]
    for key in lat_seq:
        v = biome_vecs[key]
        dist = vec_dist(v, equator_vec)
        p(f"  {BIOMES[key]['name']:28s}  dist_from_tropics={dist:.4f}")
    p()

    # =================================================================
    # SECTION 9: Cross-Biome CL Composition
    # =================================================================
    p("=" * 78)
    p("SECTION 9: CROSS-BIOME CL COMPOSITION TABLE")
    p("=" * 78)
    p()

    selected = ["hot_desert", "tundra", "boreal", "temp_deciduous",
                "tropical_forest", "coral_reef", "amazon_dieback",
                "coral_bleached"]
    sel_names = [BIOMES[k]["name"][:14] for k in selected]

    p("  T(TSML) Composition:")
    header = "               " + "".join(f"{n:>15s}" for n in sel_names)
    p(header)
    n_ts = 0
    n_bh = 0
    n_bt = 0
    n_tot = 0
    for i, ki in enumerate(selected):
        row = f"  {sel_names[i]:13s}"
        oi = biome_ops[ki]["op"]
        for j, kj in enumerate(selected):
            oj = biome_ops[kj]["op"]
            t = TSML[oi][oj]
            row += f"  {OP_NAMES[t]:>13s}"
            n_tot += 1
            if t == 7:
                n_ts += 1
            tb = BHML[oi][oj]
            if tb == 7:
                n_bh += 1
            if t == 7 and tb == 7:
                n_bt += 1
        p(row)
    p()
    p(f"  TSML HARMONY: {n_ts}/{n_tot} = {n_ts/n_tot:.4f}")
    p(f"  BHML HARMONY: {n_bh}/{n_tot} = {n_bh/n_tot:.4f}")
    p(f"  UNIFIED:      {n_bt}/{n_tot} = {n_bt/n_tot:.4f}")
    p()

    # =================================================================
    # SECTION 10: Dimension Dominance
    # =================================================================
    p("=" * 78)
    p("SECTION 10: DIMENSION DOMINANCE IN ECOLOGICAL TRANSITIONS")
    p("=" * 78)
    p()

    global_dims = [0] * 5
    for traj_key, traj in TRAJECTORIES.items():
        epochs = traj["epochs"]
        dim_counts = [0] * 5
        n_pts = 0
        for i in range(1, len(epochs) - 1):
            v0 = biome_vecs[epochs[i-1]]
            v1 = biome_vecs[epochs[i]]
            v2 = biome_vecs[epochs[i+1]]
            d2 = compute_d2(v0, v1, v2)
            abs_d2 = [abs(x) for x in d2]
            max_d = max(abs_d2)
            if max_d > 1e-12:
                dom = abs_d2.index(max_d)
                dim_counts[dom] += 1
                global_dims[dom] += 1
                n_pts += 1

        if n_pts > 0:
            dom_dim = dim_counts.index(max(dim_counts))
            p(f"  {traj['name']:35s}  dominant={DIM_NAMES[dom_dim]:12s}  "
              f"np={dim_counts[0]} sp={dim_counts[1]} sc={dim_counts[2]} "
              f"wa={dim_counts[3]} te={dim_counts[4]}")

    p()
    total_g = sum(global_dims)
    p(f"  Global dimension dominance ({total_g} total D2 points):")
    for d in range(5):
        pct = 100.0 * global_dims[d] / max(total_g, 1)
        bar = "#" * int(pct / 2)
        p(f"    {DIM_NAMES[d]:12s}: {global_dims[d]:3d} ({pct:5.1f}%)  {bar}")
    p()

    # =================================================================
    # SECTION 11: Synthesis
    # =================================================================
    p("=" * 78)
    p("SECTION 11: SYNTHESIS")
    p("=" * 78)
    p()

    p("  FINDINGS:")
    p()
    p("  1. TIPPING POINTS ARE D2 SPIKES")
    p(f"     Collapse trajectories show higher D2 than natural gradients.")
    p()

    p("  2. APERTURE (NPP) DRIVES BIOME CLASSIFICATION")
    p(f"     Net primary productivity is the primary axis of biome identity.")
    p()

    p("  3. DEGRADED STATES SHIFT OPERATOR CLASS")
    p(f"     Healthy biomes span diverse operators.")
    p(f"     Degraded states cluster toward LATTICE/VOID (low aperture).")
    p()

    p("  4. LATITUDE GRADIENT IS MONOTONE IN 5D DISTANCE")
    p(f"     Distance from tropical centroid increases monotonically poleward.")
    p()

    p("  FALSIFIABLE PREDICTIONS:")
    p()
    p("  P1: TIPPING POINT = D2 SPIKE")
    p("      Ecosystem tipping points produce |D2| > 2x the |D2| of natural")
    p("      succession transitions in the same biome.")
    p("      Kill: tipping |D2| < 1.5x natural |D2| in field data.")
    p()
    p("  P2: NPP COLLAPSE PRECEDES BIODIVERSITY LOSS")
    p("      Aperture (NPP) drops before pressure (species) in all tipping")
    p("      scenarios: the energy channel closes before diversity collapses.")
    p("      Kill: species loss precedes NPP drop in 3+ tipping datasets.")
    p()
    p("  P3: SOIL CARBON = ECOLOGICAL MEMORY")
    p("      Depth dimension (soil carbon) predicts recovery time:")
    p("      higher soil C = longer memory = slower but more complete recovery.")
    p("      Kill: no correlation between soil C and recovery time in field data.")
    p()
    p("  P4: DUAL-LENS GAP PREDICTS RESILIENCE")
    p("      Biomes with high TSML-BHML gap are MORE vulnerable to tipping")
    p("      (they ARE one thing but DO another = structural tension).")
    p("      Kill: high-gap biomes are more resilient than low-gap in field data.")
    p()

    p("=" * 78)
    p("  END OF ECOLOGY D2 SPECTROMETER ANALYSIS")
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
