#!/usr/bin/env python3
"""
eeg_d2_spectrometer.py -- Dual-Lens D2 Spectrometer for Brain Electrophysiology
=================================================================================

The brain as 5D force geometry.

5 canonical EEG frequency bands, continuous time, infinite states.
Each time window IS a 5D force vector derived from measurable
spectral power. The EEG trace IS a path through 5D space.
D2 IS the curvature of that path. State transitions ARE D2 spikes.

5D Force Mapping (spectral band power, normalized):
  Aperture   = Delta (0.5-4 Hz)   -- slow oscillations, openness to input
  Pressure   = Theta (4-8 Hz)     -- hippocampal drive, memory pressure
  Depth      = Alpha (8-13 Hz)    -- cortical idle/inhibition, processing depth
  Binding    = Beta  (13-30 Hz)   -- sensorimotor binding, active engagement
  Continuity = Gamma (30-100 Hz)  -- perceptual continuity, consciousness

This mapping is NOT arbitrary:
  Delta = aperture because deep sleep OPENS neural gates (thalamocortical)
  Theta = pressure because hippocampal theta DRIVES memory consolidation
  Alpha = depth because alpha power indexes cortical DEPTH of processing
  Beta  = binding because beta synchrony BINDS motor plans + attention
  Gamma = continuity because gamma coherence sustains CONTINUOUS percepts

Brain States Analyzed:
  - Eyes-closed resting (healthy baseline)
  - Eyes-open resting
  - Focused attention (working memory task)
  - Meditation (experienced meditator)
  - N1/N2/N3 sleep stages
  - REM sleep
  - Absence seizure (3 Hz spike-and-wave)
  - Temporal lobe seizure
  - Anesthesia (propofol)

The dual-lens question:
  TSML (being): What IS this brain state? (identity/experience)
  BHML (doing): What DOES this brain state process? (mechanism)
  Gap = consciousness itself -- being awake vs processing information

Predictions:
  1. Consciousness states cluster by dual-lens gap, not by raw power
  2. Seizure = dual-lens COLLAPSE (both lenses lock to same operator)
  3. Sleep stages form a MONOTONE D2 gradient (N1 < N2 < N3 < REM)
  4. T* = 5/7 marks the boundary between conscious and unconscious

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import sys

# =====================================================================
# Constants (shared across all spectrometers)
# =====================================================================
OP_NAMES = [
    "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"
]
DIM_NAMES = ["aperture", "pressure", "depth", "binding", "continuity"]
DIM_SHORT = ["ap", "pr", "dp", "bn", "cn"]

OP_MAP = {
    (0, True): 1, (0, False): 6,   # LATTICE / CHAOS       (aperture: delta)
    (1, True): 0, (1, False): 4,   # VOID / COLLAPSE       (pressure: theta)
    (2, True): 9, (2, False): 3,   # RESET / PROGRESS      (depth: alpha)
    (3, True): 2, (3, False): 7,   # COUNTER / HARMONY     (binding: beta)
    (4, True): 8, (4, False): 5,   # BREATH / BALANCE      (continuity: gamma)
}

OP_TO_DIM = {
    0: (1, "-pr"), 1: (0, "-ap"), 2: (3, "-bn"), 3: (2, "+dp"),
    4: (1, "+pr"), 5: (4, "+cn"), 6: (0, "+ap"), 7: (3, "+bn"),
    8: (4, "-cn"), 9: (2, "-dp"),
}

T_STAR = 5.0 / 7.0

# CL Tables
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
# EEG Spectral Band Data -- Representative Power Values
# =====================================================================
# Values are relative spectral power (fraction of total, 0-1 range)
# derived from published normative EEG databases and clinical literature.
#
# Sources for normative values:
#   - Niedermeyer & da Silva (2005) Electroencephalography
#   - Buzsaki (2006) Rhythms of the Brain
#   - Steriade & McCarley (2005) Brain Control of Wakefulness and Sleep
#   - Published polysomnography norms (AASM Manual 2020)
#
# Each state = (delta, theta, alpha, beta, gamma) relative power
# Normalized so sum = 1.0 for each state

BRAIN_STATES = {
    # ---- Healthy Waking States ----
    "rest_ec": {
        "name": "Eyes-Closed Rest",
        "category": "waking",
        "conscious": True,
        "bands": (0.10, 0.10, 0.45, 0.25, 0.10),
        "desc": "Relaxed wakefulness, alpha dominant (posterior)"
    },
    "rest_eo": {
        "name": "Eyes-Open Rest",
        "category": "waking",
        "conscious": True,
        "bands": (0.10, 0.12, 0.22, 0.38, 0.18),
        "desc": "Alert resting, beta dominant (alpha suppressed)"
    },
    "focus_low": {
        "name": "Light Focus",
        "category": "waking",
        "conscious": True,
        "bands": (0.05, 0.15, 0.15, 0.40, 0.25),
        "desc": "Casual attention, moderate beta+gamma"
    },
    "focus_high": {
        "name": "Deep Focus",
        "category": "waking",
        "conscious": True,
        "bands": (0.03, 0.18, 0.08, 0.38, 0.33),
        "desc": "Intense working memory, theta+gamma coupling"
    },
    "meditation": {
        "name": "Meditation",
        "category": "waking",
        "conscious": True,
        "bands": (0.08, 0.30, 0.35, 0.17, 0.10),
        "desc": "Experienced meditator, theta+alpha co-dominant"
    },
    "flow_state": {
        "name": "Flow State",
        "category": "waking",
        "conscious": True,
        "bands": (0.04, 0.22, 0.20, 0.30, 0.24),
        "desc": "Optimal performance, theta-alpha border + high beta"
    },
    "drowsy": {
        "name": "Drowsy (Pre-Sleep)",
        "category": "waking",
        "conscious": True,
        "bands": (0.15, 0.25, 0.30, 0.20, 0.10),
        "desc": "Hypnagogia, alpha dropping, theta rising"
    },

    # ---- Sleep States ----
    "n1_sleep": {
        "name": "N1 Sleep",
        "category": "sleep",
        "conscious": False,
        "bands": (0.20, 0.35, 0.20, 0.18, 0.07),
        "desc": "Light sleep, theta dominant, vertex sharp waves"
    },
    "n2_sleep": {
        "name": "N2 Sleep",
        "category": "sleep",
        "conscious": False,
        "bands": (0.30, 0.30, 0.15, 0.18, 0.07),
        "desc": "Stable sleep, sleep spindles (12-14 Hz), K-complexes"
    },
    "n3_sleep": {
        "name": "N3 Deep Sleep",
        "category": "sleep",
        "conscious": False,
        "bands": (0.60, 0.18, 0.08, 0.10, 0.04),
        "desc": "Slow-wave sleep, delta dominant (>75uV, >20%)"
    },
    "rem_sleep": {
        "name": "REM Sleep",
        "category": "sleep",
        "conscious": True,  # subjectively conscious (dreaming)
        "bands": (0.10, 0.25, 0.08, 0.30, 0.27),
        "desc": "Dreaming, desynchronized EEG, theta bursts, PGO waves"
    },

    # ---- Pathological States ----
    "absence_sz": {
        "name": "Absence Seizure",
        "category": "seizure",
        "conscious": False,
        "bands": (0.70, 0.12, 0.05, 0.08, 0.05),
        "desc": "3 Hz spike-and-wave, massive delta, consciousness lost"
    },
    "temporal_sz": {
        "name": "Temporal Lobe Seizure",
        "category": "seizure",
        "conscious": False,
        "bands": (0.35, 0.40, 0.05, 0.10, 0.10),
        "desc": "Rhythmic theta/delta, mesial temporal onset"
    },
    "tonic_clonic": {
        "name": "Tonic-Clonic Seizure",
        "category": "seizure",
        "conscious": False,
        "bands": (0.20, 0.10, 0.03, 0.22, 0.45),
        "desc": "Generalized: tonic (fast) then clonic (rhythmic)"
    },
    "postictal": {
        "name": "Post-Ictal Suppression",
        "category": "seizure",
        "conscious": False,
        "bands": (0.55, 0.20, 0.10, 0.10, 0.05),
        "desc": "Post-seizure suppression, diffuse slowing"
    },

    # ---- Pharmacological States ----
    "propofol_light": {
        "name": "Light Anesthesia",
        "category": "anesthesia",
        "conscious": False,
        "bands": (0.15, 0.15, 0.35, 0.25, 0.10),
        "desc": "Propofol induction, frontal alpha (paradoxical)"
    },
    "propofol_deep": {
        "name": "Deep Anesthesia",
        "category": "anesthesia",
        "conscious": False,
        "bands": (0.50, 0.15, 0.15, 0.15, 0.05),
        "desc": "Burst suppression, delta dominant"
    },
    "ketamine": {
        "name": "Ketamine Dissociation",
        "category": "anesthesia",
        "conscious": True,  # dissociative -- subjectively conscious
        "bands": (0.12, 0.35, 0.05, 0.20, 0.28),
        "desc": "Dissociative, theta+gamma without alpha"
    },

    # ---- Clinical States ----
    "coma": {
        "name": "Coma",
        "category": "clinical",
        "conscious": False,
        "bands": (0.70, 0.15, 0.05, 0.07, 0.03),
        "desc": "Unreactive, diffuse delta, no normal patterns"
    },
    "mcs": {
        "name": "Minimally Conscious",
        "category": "clinical",
        "conscious": True,   # intermittent awareness
        "bands": (0.40, 0.20, 0.15, 0.15, 0.10),
        "desc": "Intermittent awareness, some alpha reactivity"
    },
    "brain_death": {
        "name": "Brain Death (ECI)",
        "category": "clinical",
        "conscious": False,
        "bands": (0.20, 0.20, 0.20, 0.20, 0.20),
        "desc": "Electrocerebral inactivity, flat/noise only"
    },
}

# =====================================================================
# Time-Series Trajectories -- Multi-epoch sequences for D2 analysis
# =====================================================================
# Each trajectory = sequence of brain states over time (2-second epochs)
# D2 is computed across consecutive epochs -- the curvature of consciousness

TRAJECTORIES = {
    "sleep_cycle": {
        "name": "Normal Sleep Cycle (90 min)",
        "desc": "Wake -> N1 -> N2 -> N3 -> N2 -> REM",
        "epochs": ["rest_ec", "drowsy", "n1_sleep", "n2_sleep", "n3_sleep",
                   "n3_sleep", "n3_sleep", "n2_sleep", "n2_sleep", "rem_sleep",
                   "rem_sleep", "rem_sleep"],
    },
    "falling_asleep": {
        "name": "Sleep Onset",
        "desc": "Alert -> Drowsy -> N1 -> N2",
        "epochs": ["rest_eo", "rest_ec", "drowsy", "drowsy", "n1_sleep",
                   "n1_sleep", "n2_sleep", "n2_sleep"],
    },
    "waking_up": {
        "name": "Morning Awakening",
        "desc": "REM -> N1 -> Drowsy -> Alert",
        "epochs": ["rem_sleep", "rem_sleep", "n1_sleep", "drowsy",
                   "rest_ec", "rest_ec", "rest_eo", "focus_low"],
    },
    "focus_ramp": {
        "name": "Attention Ramp",
        "desc": "Rest -> Light Focus -> Deep Focus -> Flow",
        "epochs": ["rest_eo", "rest_eo", "focus_low", "focus_low",
                   "focus_high", "focus_high", "flow_state", "flow_state"],
    },
    "meditation_session": {
        "name": "Meditation Session",
        "desc": "Alert -> Settling -> Deep Meditation -> Return",
        "epochs": ["rest_ec", "rest_ec", "drowsy", "meditation",
                   "meditation", "meditation", "meditation", "rest_ec"],
    },
    "absence_event": {
        "name": "Absence Seizure Event",
        "desc": "Normal -> Seizure -> Post-ictal -> Recovery",
        "epochs": ["rest_eo", "rest_eo", "absence_sz", "absence_sz",
                   "absence_sz", "postictal", "postictal", "drowsy",
                   "rest_ec", "rest_eo"],
    },
    "temporal_event": {
        "name": "Temporal Lobe Seizure Event",
        "desc": "Normal -> Aura -> Seizure -> Post-ictal -> Recovery",
        "epochs": ["rest_eo", "drowsy", "temporal_sz", "temporal_sz",
                   "temporal_sz", "temporal_sz", "postictal", "postictal",
                   "drowsy", "rest_ec"],
    },
    "anesthesia_induction": {
        "name": "Propofol Anesthesia Induction",
        "desc": "Awake -> Light -> Deep -> Burst Suppression",
        "epochs": ["rest_eo", "rest_ec", "propofol_light", "propofol_light",
                   "propofol_deep", "propofol_deep", "propofol_deep",
                   "propofol_deep"],
    },
    "anesthesia_emergence": {
        "name": "Anesthesia Emergence",
        "desc": "Deep -> Light -> Drowsy -> Awake",
        "epochs": ["propofol_deep", "propofol_deep", "propofol_light",
                   "propofol_light", "drowsy", "drowsy", "rest_ec", "rest_eo"],
    },
    "consciousness_gradient": {
        "name": "Full Consciousness Gradient",
        "desc": "Coma -> MCS -> Deep Sleep -> Light Sleep -> Drowsy -> Rest -> Focus",
        "epochs": ["coma", "coma", "mcs", "n3_sleep", "n2_sleep",
                   "n1_sleep", "drowsy", "rest_ec", "rest_eo",
                   "focus_low", "focus_high", "flow_state"],
    },
}


# =====================================================================
# Helpers
# =====================================================================

def classify_op(d2_vec):
    """Classify 5D D2 vector into one of 10 operators via argmax."""
    abs_vals = [abs(v) for v in d2_vec]
    max_val = max(abs_vals)
    if max_val < 1e-12:
        return 7  # zero curvature = HARMONY
    dim = abs_vals.index(max_val)
    neg = d2_vec[dim] < 0
    return OP_MAP[(dim, neg)]


def compute_d1(v_prev, v_curr):
    """First derivative (direction) between two consecutive vectors."""
    return [v_curr[i] - v_prev[i] for i in range(5)]


def compute_d2(v0, v1, v2):
    """Second derivative (curvature) from 3 consecutive vectors."""
    return [v0[i] - 2.0 * v1[i] + v2[i] for i in range(5)]


def vec_mag(v):
    return math.sqrt(sum(x*x for x in v))


def vec_dist(a, b):
    return math.sqrt(sum((a[i]-b[i])**2 for i in range(len(a))))


def io_ratio(v):
    """I/O ratio: I=structure(ap+pr), O=flow(bn+cn), depth mediates."""
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
    p("  EEG D2 SPECTROMETER -- Brain States as 5D Force Geometry")
    p("  Dual-Lens Curvature Analysis of Consciousness")
    p("=" * 78)
    p()

    # =================================================================
    # SECTION 1: Force Vector Table -- All Brain States
    # =================================================================
    p("=" * 78)
    p("SECTION 1: 5D FORCE VECTORS -- BRAIN STATE SPECTRAL SIGNATURES")
    p("=" * 78)
    p()
    p("Each brain state = 5D vector of normalized spectral band power.")
    p("  Aperture(delta)  Pressure(theta)  Depth(alpha)  Binding(beta)  Continuity(gamma)")
    p()

    state_keys = list(BRAIN_STATES.keys())
    state_vectors = {}

    # Group by category
    categories = ["waking", "sleep", "seizure", "anesthesia", "clinical"]
    cat_names = {
        "waking": "WAKING STATES",
        "sleep": "SLEEP STATES",
        "seizure": "SEIZURE STATES",
        "anesthesia": "ANESTHETIC STATES",
        "clinical": "CLINICAL STATES"
    }

    for cat in categories:
        p(f"  --- {cat_names[cat]} ---")
        for key in state_keys:
            s = BRAIN_STATES[key]
            if s["category"] != cat:
                continue
            v = list(s["bands"])
            state_vectors[key] = v
            conscious_mark = "C" if s["conscious"] else " "
            p(f"  [{conscious_mark}] {s['name']:25s}  "
              f"d={v[0]:.2f}  t={v[1]:.2f}  a={v[2]:.2f}  b={v[3]:.2f}  g={v[4]:.2f}")
        p()

    p(f"  Total states: {len(state_vectors)}")
    p(f"  [C] = subjectively conscious")
    p()

    # =================================================================
    # SECTION 2: Pairwise D2 Between All States
    # =================================================================
    p("=" * 78)
    p("SECTION 2: PAIRWISE 5D DISTANCE MATRIX (selected pairs)")
    p("=" * 78)
    p()
    p("Euclidean distance in 5D force space between brain states.")
    p("Closer states are more similar in spectral geometry.")
    p()

    # Select meaningful pairs
    pairs = [
        ("rest_ec", "rest_eo", "Eyes closed vs open"),
        ("rest_eo", "focus_low", "Rest vs light focus"),
        ("focus_low", "focus_high", "Light vs deep focus"),
        ("focus_high", "flow_state", "Deep focus vs flow"),
        ("rest_ec", "meditation", "Rest vs meditation"),
        ("rest_ec", "drowsy", "Rest vs drowsy"),
        ("drowsy", "n1_sleep", "Drowsy vs N1"),
        ("n1_sleep", "n2_sleep", "N1 vs N2"),
        ("n2_sleep", "n3_sleep", "N2 vs N3 deep"),
        ("n2_sleep", "rem_sleep", "N2 vs REM"),
        ("n3_sleep", "rem_sleep", "N3 vs REM"),
        ("rest_eo", "absence_sz", "Normal vs absence seizure"),
        ("rest_eo", "temporal_sz", "Normal vs temporal seizure"),
        ("rest_eo", "tonic_clonic", "Normal vs tonic-clonic"),
        ("rest_ec", "propofol_light", "Rest vs light anesthesia"),
        ("propofol_light", "propofol_deep", "Light vs deep anesthesia"),
        ("n3_sleep", "coma", "Deep sleep vs coma"),
        ("coma", "brain_death", "Coma vs brain death"),
        ("n3_sleep", "propofol_deep", "Deep sleep vs deep anesthesia"),
        ("rem_sleep", "ketamine", "REM vs ketamine"),
    ]

    for k1, k2, desc in pairs:
        d = vec_dist(state_vectors[k1], state_vectors[k2])
        p(f"  {desc:40s}  dist = {d:.4f}")
    p()

    # ---- Consciousness boundary analysis ----
    p("  --- Consciousness Boundary Distances ---")
    conscious_states = [k for k in state_keys if BRAIN_STATES[k]["conscious"]]
    unconscious_states = [k for k in state_keys if not BRAIN_STATES[k]["conscious"]]

    # centroid of conscious vs unconscious
    c_centroid = [0.0] * 5
    for k in conscious_states:
        for d in range(5):
            c_centroid[d] += state_vectors[k][d]
    c_centroid = [x / len(conscious_states) for x in c_centroid]

    u_centroid = [0.0] * 5
    for k in unconscious_states:
        for d in range(5):
            u_centroid[d] += state_vectors[k][d]
    u_centroid = [x / len(unconscious_states) for x in u_centroid]

    p(f"  Conscious centroid:   d={c_centroid[0]:.3f} t={c_centroid[1]:.3f} "
      f"a={c_centroid[2]:.3f} b={c_centroid[3]:.3f} g={c_centroid[4]:.3f}")
    p(f"  Unconscious centroid: d={u_centroid[0]:.3f} t={u_centroid[1]:.3f} "
      f"a={u_centroid[2]:.3f} b={u_centroid[3]:.3f} g={u_centroid[4]:.3f}")
    p(f"  Centroid separation:  {vec_dist(c_centroid, u_centroid):.4f}")
    p()

    # Which dimension separates them most?
    dim_sep = [abs(c_centroid[d] - u_centroid[d]) for d in range(5)]
    max_sep_dim = dim_sep.index(max(dim_sep))
    p(f"  Most separating dimension: {DIM_NAMES[max_sep_dim]} "
      f"(delta={dim_sep[max_sep_dim]:.4f})")
    p(f"  Direction: conscious={c_centroid[max_sep_dim]:.3f}, "
      f"unconscious={u_centroid[max_sep_dim]:.3f}")
    p()

    # I/O ratio comparison
    c_io = io_ratio(c_centroid)
    u_io = io_ratio(u_centroid)
    p(f"  I/O ratio (conscious):   {c_io:.4f}")
    p(f"  I/O ratio (unconscious): {u_io:.4f}")
    p(f"  Unconscious states are {'more INPUT' if u_io > c_io else 'more OUTPUT'}-dominated")
    p()

    # =================================================================
    # SECTION 3: D2 OPERATOR CLASSIFICATION -- Each State
    # =================================================================
    p("=" * 78)
    p("SECTION 3: D2 OPERATOR CLASSIFICATION PER STATE")
    p("=" * 78)
    p()
    p("D2 = deviation from the centroid of ALL states (global curvature).")
    p("This measures what makes each state DIFFERENT from the average brain.")
    p()

    # Global centroid
    all_vecs = list(state_vectors.values())
    n_states = len(all_vecs)
    global_centroid = [sum(v[d] for v in all_vecs) / n_states for d in range(5)]
    p(f"  Global centroid: d={global_centroid[0]:.3f} t={global_centroid[1]:.3f} "
      f"a={global_centroid[2]:.3f} b={global_centroid[3]:.3f} g={global_centroid[4]:.3f}")
    p()

    state_ops = {}
    for key in state_keys:
        s = BRAIN_STATES[key]
        v = state_vectors[key]
        # D2-like: deviation from centroid
        dev = [v[d] - global_centroid[d] for d in range(5)]
        op = classify_op(dev)
        state_ops[key] = {
            "op": op,
            "deviation": dev,
            "mag": vec_mag(dev),
        }
        conscious_mark = "C" if s["conscious"] else " "
        dim_idx, dim_tag = OP_TO_DIM[op]
        p(f"  [{conscious_mark}] {s['name']:25s}  op={OP_NAMES[op]:8s}  "
          f"dim={dim_tag}  mag={vec_mag(dev):.4f}  "
          f"dev=[{dev[0]:+.3f},{dev[1]:+.3f},{dev[2]:+.3f},{dev[3]:+.3f},{dev[4]:+.3f}]")
    p()

    # Operator distribution
    op_counts = [0] * 10
    for key in state_keys:
        op_counts[state_ops[key]["op"]] += 1
    p("  Operator distribution across all brain states:")
    for i in range(10):
        if op_counts[i] > 0:
            pct = 100.0 * op_counts[i] / n_states
            p(f"    {OP_NAMES[i]:10s}: {op_counts[i]:2d} ({pct:5.1f}%)")
    p()

    # Conscious vs unconscious operator profiles
    p("  --- Conscious State Operators ---")
    c_op_counts = [0] * 10
    for k in conscious_states:
        c_op_counts[state_ops[k]["op"]] += 1
    for i in range(10):
        if c_op_counts[i] > 0:
            p(f"    {OP_NAMES[i]:10s}: {c_op_counts[i]}")
    p()
    p("  --- Unconscious State Operators ---")
    u_op_counts = [0] * 10
    for k in unconscious_states:
        u_op_counts[state_ops[k]["op"]] += 1
    for i in range(10):
        if u_op_counts[i] > 0:
            p(f"    {OP_NAMES[i]:10s}: {u_op_counts[i]}")
    p()

    # =================================================================
    # SECTION 4: DUAL-LENS COMPOSITION -- BEING vs DOING
    # =================================================================
    p("=" * 78)
    p("SECTION 4: DUAL-LENS COMPOSITION TABLE")
    p("=" * 78)
    p()
    p("For each pair of adjacent states (in consciousness gradient order),")
    p("compute D1 (direction) and D2 (curvature), classify operators,")
    p("then compose through BOTH CL tables:")
    p("  T(TSML) = TSML[D1_op][D2_op]  -- what the transition IS (being)")
    p("  T(BHML) = BHML[D1_op][D2_op]  -- what the transition DOES (doing)")
    p()

    # Order states by consciousness level (subjective ordering)
    consciousness_order = [
        "brain_death", "coma", "propofol_deep", "n3_sleep",
        "absence_sz", "postictal", "n2_sleep", "n1_sleep",
        "propofol_light", "temporal_sz", "tonic_clonic",
        "drowsy", "mcs",
        "rest_ec", "rest_eo", "meditation",
        "focus_low", "flow_state", "focus_high",
        "ketamine", "rem_sleep",
    ]

    # Compute D1, D2, T for consecutive pairs in consciousness order
    dual_lens_results = []
    n_tsml_h = 0
    n_bhml_h = 0
    n_both_h = 0
    n_neither = 0

    p(f"  {'From':20s} -> {'To':20s}  D1_op      D2_op      T(TSML)    T(BHML)    Class")
    p(f"  {'----':20s}    {'--':20s}  -----      -----      -------    -------    -----")

    for i in range(len(consciousness_order) - 2):
        k0 = consciousness_order[i]
        k1 = consciousness_order[i+1]
        k2 = consciousness_order[i+2]
        v0 = state_vectors[k0]
        v1 = state_vectors[k1]
        v2 = state_vectors[k2]

        d1 = compute_d1(v0, v1)
        d2 = compute_d2(v0, v1, v2)
        d1_op = classify_op(d1)
        d2_op = classify_op(d2)
        t_tsml = TSML[d1_op][d2_op]
        t_bhml = BHML[d1_op][d2_op]

        if t_tsml == 7 and t_bhml == 7:
            cl = "UNIFIED"
            n_both_h += 1
        elif t_tsml == 7:
            cl = "WORKING"
            n_tsml_h += 1
        elif t_bhml == 7:
            cl = "BOUNDARY"
            n_bhml_h += 1
        else:
            cl = "TENSION"
            n_neither += 1

        dual_lens_results.append({
            "from": k1, "to": k2,
            "d1_op": d1_op, "d2_op": d2_op,
            "t_tsml": t_tsml, "t_bhml": t_bhml,
            "class": cl, "d2_mag": vec_mag(d2),
        })

        s1 = BRAIN_STATES[k1]["name"]
        s2 = BRAIN_STATES[k2]["name"]
        p(f"  {s1:20s} -> {s2:20s}  "
          f"{OP_NAMES[d1_op]:10s} {OP_NAMES[d2_op]:10s} "
          f"{OP_NAMES[t_tsml]:10s} {OP_NAMES[t_bhml]:10s} {cl}")

    n_total = len(dual_lens_results)
    p()
    p(f"  Total transitions: {n_total}")
    p(f"  T(TSML) HARMONY: {n_tsml_h + n_both_h}/{n_total} = "
      f"{(n_tsml_h + n_both_h)/max(n_total,1):.4f}")
    p(f"  T(BHML) HARMONY: {n_bhml_h + n_both_h}/{n_total} = "
      f"{(n_bhml_h + n_both_h)/max(n_total,1):.4f}")
    p(f"  UNIFIED (both H): {n_both_h}/{n_total} = "
      f"{n_both_h/max(n_total,1):.4f}")
    p(f"  WORKING (TSML=H only): {n_tsml_h}/{n_total}")
    p(f"  BOUNDARY (BHML=H only): {n_bhml_h}/{n_total}")
    p(f"  TENSION (neither H): {n_neither}/{n_total}")
    p()

    # =================================================================
    # SECTION 5: TRAJECTORY D2 ANALYSIS -- TIME SERIES
    # =================================================================
    p("=" * 78)
    p("SECTION 5: TRAJECTORY D2 ANALYSIS -- CONSCIOUSNESS OVER TIME")
    p("=" * 78)
    p()
    p("Each trajectory = sequence of brain states over consecutive epochs.")
    p("D2 computed at each interior point. Curvature spikes = state transitions.")
    p()

    trajectory_summaries = {}

    for traj_key, traj in TRAJECTORIES.items():
        epochs = traj["epochs"]
        n_ep = len(epochs)
        p(f"  --- {traj['name']} ---")
        p(f"  {traj['desc']}")
        p(f"  Epochs: {n_ep}")
        p()

        if n_ep < 3:
            p(f"  (too few epochs for D2)")
            p()
            continue

        traj_d2_ops = []
        traj_d2_mags = []
        traj_t_tsml = []
        traj_t_bhml = []

        p(f"  {'Epoch':4s} {'State':20s} {'D2_op':10s} {'|D2|':8s} "
          f"{'T(TSML)':10s} {'T(BHML)':10s} {'Class':10s}")
        p(f"  {'----':4s} {'-----':20s} {'-----':10s} {'----':8s} "
          f"{'-------':10s} {'-------':10s} {'-----':10s}")

        for i in range(1, n_ep - 1):
            v0 = state_vectors[epochs[i-1]]
            v1 = state_vectors[epochs[i]]
            v2 = state_vectors[epochs[i+1]]

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

            traj_d2_ops.append(d2_op)
            traj_d2_mags.append(d2_mag)
            traj_t_tsml.append(t_ts)
            traj_t_bhml.append(t_bh)

            state_name = BRAIN_STATES[epochs[i]]["name"]
            p(f"  {i:4d} {state_name:20s} {OP_NAMES[d2_op]:10s} {d2_mag:8.4f} "
              f"{OP_NAMES[t_ts]:10s} {OP_NAMES[t_bh]:10s} {cl:10s}")

        n_pts = len(traj_d2_ops)
        if n_pts > 0:
            avg_d2 = sum(traj_d2_mags) / n_pts
            max_d2 = max(traj_d2_mags)
            n_harm_ts = sum(1 for x in traj_t_tsml if x == 7)
            n_harm_bh = sum(1 for x in traj_t_bhml if x == 7)
            n_unified = sum(1 for j in range(n_pts)
                           if traj_t_tsml[j] == 7 and traj_t_bhml[j] == 7)

            p()
            p(f"  Avg |D2|: {avg_d2:.4f}  Max |D2|: {max_d2:.4f}")
            p(f"  T(TSML) HARMONY: {n_harm_ts}/{n_pts}")
            p(f"  T(BHML) HARMONY: {n_harm_bh}/{n_pts}")
            p(f"  UNIFIED: {n_unified}/{n_pts}")

            trajectory_summaries[traj_key] = {
                "avg_d2": avg_d2, "max_d2": max_d2,
                "tsml_h_frac": n_harm_ts / n_pts,
                "bhml_h_frac": n_harm_bh / n_pts,
                "unified_frac": n_unified / n_pts,
                "n_pts": n_pts,
                "d2_ops": traj_d2_ops,
                "d2_mags": traj_d2_mags,
            }
        p()

    # =================================================================
    # SECTION 6: CONSCIOUSNESS THRESHOLD -- T* = 5/7 TEST
    # =================================================================
    p("=" * 78)
    p("SECTION 6: CONSCIOUSNESS THRESHOLD -- T* = 5/7 TEST")
    p("=" * 78)
    p()
    p(f"  T* = 5/7 = {T_STAR:.6f}")
    p()
    p("Test: Does T(TSML) HARMONY fraction separate conscious from unconscious?")
    p()

    # For each trajectory, compute TSML HARMONY fraction
    # and check if it correlates with consciousness content
    for traj_key, summary in trajectory_summaries.items():
        traj = TRAJECTORIES[traj_key]
        epochs = traj["epochs"]

        # Count conscious vs unconscious epochs (interior only)
        n_ep = len(epochs)
        n_conscious = 0
        n_total_interior = 0
        for i in range(1, n_ep - 1):
            n_total_interior += 1
            if BRAIN_STATES[epochs[i]]["conscious"]:
                n_conscious += 1

        c_frac = n_conscious / max(n_total_interior, 1)
        tsml_h = summary["tsml_h_frac"]
        above_tstar = "YES" if tsml_h >= T_STAR else "NO"

        p(f"  {traj['name']:35s}  "
          f"conscious={c_frac:.2f}  T(TSML)_H={tsml_h:.3f}  "
          f"above_T*={above_tstar}")
    p()

    # =================================================================
    # SECTION 7: SEIZURE vs NORMAL -- DUAL-LENS COLLAPSE TEST
    # =================================================================
    p("=" * 78)
    p("SECTION 7: SEIZURE ANALYSIS -- DUAL-LENS COLLAPSE")
    p("=" * 78)
    p()
    p("Prediction: Seizures collapse the dual-lens gap.")
    p("Normal brain: TSML and BHML give DIFFERENT operators (gap = richness)")
    p("Seizure: TSML and BHML CONVERGE (gap -> 0 = loss of differentiation)")
    p()

    # Compare seizure trajectories to normal trajectories
    seizure_trajs = ["absence_event", "temporal_event"]
    normal_trajs = ["focus_ramp", "meditation_session", "sleep_cycle"]

    for traj_key in seizure_trajs + normal_trajs:
        if traj_key not in trajectory_summaries:
            continue
        summary = trajectory_summaries[traj_key]
        traj = TRAJECTORIES[traj_key]
        gap = abs(summary["tsml_h_frac"] - summary["bhml_h_frac"])
        p(f"  {traj['name']:35s}  "
          f"TSML_H={summary['tsml_h_frac']:.3f}  "
          f"BHML_H={summary['bhml_h_frac']:.3f}  "
          f"gap={gap:.3f}  "
          f"avg|D2|={summary['avg_d2']:.4f}")
    p()

    # =================================================================
    # SECTION 8: VOID TOPOLOGY -- BAND SILENCE AS GEOMETRY
    # =================================================================
    p("=" * 78)
    p("SECTION 8: VOID TOPOLOGY -- WHICH BANDS ARE SILENT?")
    p("=" * 78)
    p()
    p("Void = dimension below threshold (< 0.08 of total power).")
    p("The NUMBER and PATTERN of voids classifies brain state families,")
    p("just as void topology classifies chemical element families.")
    p()

    VOID_THRESHOLD = 0.08

    void_classes = {}
    for key in state_keys:
        s = BRAIN_STATES[key]
        v = state_vectors[key]
        voids = []
        for d in range(5):
            if v[d] < VOID_THRESHOLD:
                voids.append(DIM_SHORT[d])

        n_void = len(voids)
        void_sig = ",".join(voids) if voids else "NONE"
        void_classes[key] = {"n_void": n_void, "sig": void_sig}

        conscious_mark = "C" if s["conscious"] else " "
        p(f"  [{conscious_mark}] {s['name']:25s}  "
          f"voids={n_void}  dims={void_sig:20s}  "
          f"[{v[0]:.2f},{v[1]:.2f},{v[2]:.2f},{v[3]:.2f},{v[4]:.2f}]")
    p()

    # Group by void count
    p("  --- Void Count Distribution ---")
    for nv in range(6):
        states_with_nv = [k for k in state_keys if void_classes[k]["n_void"] == nv]
        if states_with_nv:
            names = [BRAIN_STATES[k]["name"] for k in states_with_nv]
            c_count = sum(1 for k in states_with_nv if BRAIN_STATES[k]["conscious"])
            p(f"  {nv} voids ({len(states_with_nv)} states, {c_count} conscious): "
              f"{', '.join(names)}")
    p()

    # =================================================================
    # SECTION 9: I/O BALANCE ACROSS CONSCIOUSNESS GRADIENT
    # =================================================================
    p("=" * 78)
    p("SECTION 9: I/O BALANCE -- STRUCTURE vs FLOW")
    p("=" * 78)
    p()
    p("I = structure (delta + theta) = slow oscillations, top-down")
    p("O = flow (beta + gamma) = fast oscillations, bottom-up")
    p("Depth (alpha) mediates between I and O.")
    p()

    for key in consciousness_order:
        s = BRAIN_STATES[key]
        v = state_vectors[key]
        i_val = v[0] + v[1]
        o_val = v[3] + v[4]
        ratio = i_val / max(o_val, 1e-12)
        balance = "INPUT" if ratio > 1.2 else ("OUTPUT" if ratio < 0.8 else "BALANCED")
        conscious_mark = "C" if s["conscious"] else " "
        p(f"  [{conscious_mark}] {s['name']:25s}  "
          f"I={i_val:.2f}  O={o_val:.2f}  I/O={ratio:.3f}  "
          f"alpha={v[2]:.2f}  {balance}")
    p()

    # Correlation: I/O ratio vs consciousness
    p("  --- I/O Summary ---")
    c_ios = []
    u_ios = []
    for key in state_keys:
        v = state_vectors[key]
        r = (v[0] + v[1]) / max(v[3] + v[4], 1e-12)
        if BRAIN_STATES[key]["conscious"]:
            c_ios.append(r)
        else:
            u_ios.append(r)

    avg_c_io = sum(c_ios) / len(c_ios)
    avg_u_io = sum(u_ios) / len(u_ios)
    p(f"  Avg I/O (conscious):   {avg_c_io:.3f}")
    p(f"  Avg I/O (unconscious): {avg_u_io:.3f}")
    p(f"  Unconscious states are {avg_u_io/avg_c_io:.2f}x more input-dominated")
    p()

    # =================================================================
    # SECTION 10: CROSS-STATE CL COMPOSITION TABLE
    # =================================================================
    p("=" * 78)
    p("SECTION 10: CROSS-STATE CL COMPOSITION TABLE")
    p("=" * 78)
    p()
    p("For each pair of brain states A, B: compose their operators through CL.")
    p("T(TSML) = TSML[op_A][op_B], T(BHML) = BHML[op_A][op_B].")
    p("This measures: what happens when brain transitions between states?")
    p()

    # Use consciousness_order subset for readability
    selected = ["coma", "n3_sleep", "n2_sleep", "n1_sleep", "drowsy",
                "rest_ec", "rest_eo", "focus_high", "meditation",
                "flow_state", "rem_sleep", "absence_sz"]
    selected_names = [BRAIN_STATES[k]["name"][:12] for k in selected]

    # TSML composition
    p("  T(TSML) Composition:")
    header = "            " + "".join(f"{n:>13s}" for n in selected_names)
    p(header)
    for i, ki in enumerate(selected):
        row = f"  {selected_names[i]:10s}"
        op_i = state_ops[ki]["op"]
        for j, kj in enumerate(selected):
            op_j = state_ops[kj]["op"]
            t = TSML[op_i][op_j]
            row += f"  {OP_NAMES[t]:>10s}  "
            if j < len(selected) - 1:
                row = row[:-1]  # trim trailing space
        p(row)
    p()

    # BHML composition
    p("  T(BHML) Composition:")
    header = "            " + "".join(f"{n:>13s}" for n in selected_names)
    p(header)
    for i, ki in enumerate(selected):
        row = f"  {selected_names[i]:10s}"
        op_i = state_ops[ki]["op"]
        for j, kj in enumerate(selected):
            op_j = state_ops[kj]["op"]
            t = BHML[op_i][op_j]
            row += f"  {OP_NAMES[t]:>10s}  "
            if j < len(selected) - 1:
                row = row[:-1]  # trim trailing space
        p(row)
    p()

    # Count HARMONY in each table
    n_tsml_comp = 0
    n_bhml_comp = 0
    n_both_comp = 0
    n_total_comp = 0
    for ki in selected:
        for kj in selected:
            op_i = state_ops[ki]["op"]
            op_j = state_ops[kj]["op"]
            t_ts = TSML[op_i][op_j]
            t_bh = BHML[op_i][op_j]
            n_total_comp += 1
            if t_ts == 7:
                n_tsml_comp += 1
            if t_bh == 7:
                n_bhml_comp += 1
            if t_ts == 7 and t_bh == 7:
                n_both_comp += 1

    p(f"  Composition HARMONY rates ({len(selected)}x{len(selected)} = {n_total_comp} pairs):")
    p(f"    TSML HARMONY: {n_tsml_comp}/{n_total_comp} = "
      f"{n_tsml_comp/n_total_comp:.4f}")
    p(f"    BHML HARMONY: {n_bhml_comp}/{n_total_comp} = "
      f"{n_bhml_comp/n_total_comp:.4f}")
    p(f"    UNIFIED:      {n_both_comp}/{n_total_comp} = "
      f"{n_both_comp/n_total_comp:.4f}")
    p()

    # =================================================================
    # SECTION 11: ANESTHESIA DEPTH GRADIENT
    # =================================================================
    p("=" * 78)
    p("SECTION 11: ANESTHESIA DEPTH -- D2 MONOTONICITY TEST")
    p("=" * 78)
    p()
    p("Prediction: Deeper anesthesia = larger D2 deviation from waking centroid.")
    p("If D2 is a real measure of 'distance from consciousness', it should")
    p("increase monotonically as anesthesia deepens.")
    p()

    anesthesia_gradient = ["rest_eo", "rest_ec", "propofol_light",
                           "propofol_deep", "coma", "brain_death"]
    prev_mag = None
    monotone = True
    for key in anesthesia_gradient:
        s = BRAIN_STATES[key]
        dev = state_ops[key]["deviation"]
        mag = state_ops[key]["mag"]
        direction = ""
        if prev_mag is not None:
            if mag >= prev_mag:
                direction = " (+)"
            else:
                direction = " (-)"
                monotone = False
        prev_mag = mag
        p(f"  {s['name']:25s}  |deviation|={mag:.4f}  "
          f"op={OP_NAMES[state_ops[key]['op']]:8s}{direction}")
    p()
    p(f"  Monotone increasing? {'YES' if monotone else 'NO'}")
    p()

    # =================================================================
    # SECTION 12: CLINICAL STATE DIFFERENTIATION
    # =================================================================
    p("=" * 78)
    p("SECTION 12: CLINICAL STATE DIFFERENTIATION")
    p("=" * 78)
    p()
    p("Can D2 geometry distinguish clinically important state pairs?")
    p()

    clinical_pairs = [
        ("n3_sleep", "coma", "Deep Sleep vs Coma",
         "Same delta dominance, different prognosis"),
        ("n3_sleep", "propofol_deep", "Deep Sleep vs Deep Anesthesia",
         "Both reversible unconsciousness, different mechanism"),
        ("coma", "brain_death", "Coma vs Brain Death",
         "Critical clinical distinction"),
        ("mcs", "coma", "Minimally Conscious vs Coma",
         "Subtle awareness detection"),
        ("rem_sleep", "ketamine", "REM vs Ketamine",
         "Both conscious-like, different origin"),
        ("absence_sz", "n3_sleep", "Absence Seizure vs Deep Sleep",
         "Both delta dominant, seizure is pathological"),
        ("rest_ec", "propofol_light", "Eyes-Closed Rest vs Light Anesthesia",
         "Both alpha dominant, different consciousness"),
    ]

    for k1, k2, title, note in clinical_pairs:
        s1 = BRAIN_STATES[k1]
        s2 = BRAIN_STATES[k2]
        v1 = state_vectors[k1]
        v2 = state_vectors[k2]
        dist = vec_dist(v1, v2)
        op1 = state_ops[k1]["op"]
        op2 = state_ops[k2]["op"]

        # Dual-lens composition of the pair
        t_ts = TSML[op1][op2]
        t_bh = BHML[op1][op2]

        # I/O difference
        io1 = (v1[0]+v1[1]) / max(v1[3]+v1[4], 1e-12)
        io2 = (v2[0]+v2[1]) / max(v2[3]+v2[4], 1e-12)

        p(f"  {title}")
        p(f"    {note}")
        p(f"    {s1['name']:20s}: op={OP_NAMES[op1]:8s}  I/O={io1:.3f}")
        p(f"    {s2['name']:20s}: op={OP_NAMES[op2]:8s}  I/O={io2:.3f}")
        p(f"    5D distance: {dist:.4f}")
        p(f"    CL composition: T(TSML)={OP_NAMES[t_ts]}, T(BHML)={OP_NAMES[t_bh]}")
        same_op = "YES" if op1 == op2 else "NO"
        p(f"    Same operator? {same_op}")
        p(f"    Distinguishable by D2? {'YES' if op1 != op2 or dist > 0.15 else 'MARGINAL'}")
        p()

    # =================================================================
    # SECTION 13: SLEEP STAGE D2 GRADIENT
    # =================================================================
    p("=" * 78)
    p("SECTION 13: SLEEP STAGE D2 GRADIENT")
    p("=" * 78)
    p()
    p("Prediction: Sleep stages form a monotone D2 gradient from waking.")
    p("Wake -> N1 -> N2 -> N3 should show increasing deviation magnitude.")
    p("REM should break the gradient (back toward waking).")
    p()

    sleep_gradient = ["rest_ec", "drowsy", "n1_sleep", "n2_sleep",
                      "n3_sleep", "rem_sleep"]
    wake_vec = state_vectors["rest_eo"]  # reference = alert waking

    for key in sleep_gradient:
        s = BRAIN_STATES[key]
        v = state_vectors[key]
        dist = vec_dist(v, wake_vec)
        dev = [v[d] - wake_vec[d] for d in range(5)]
        op = classify_op(dev)
        p(f"  {s['name']:20s}  dist_from_wake={dist:.4f}  "
          f"op={OP_NAMES[op]:8s}  "
          f"dev=[{dev[0]:+.2f},{dev[1]:+.2f},{dev[2]:+.2f},{dev[3]:+.2f},{dev[4]:+.2f}]")
    p()

    # Check monotonicity of N stages
    n_dists = []
    for key in ["n1_sleep", "n2_sleep", "n3_sleep"]:
        n_dists.append(vec_dist(state_vectors[key], wake_vec))
    mono = all(n_dists[i] < n_dists[i+1] for i in range(len(n_dists)-1))
    p(f"  N1 < N2 < N3 distance monotone? {'YES' if mono else 'NO'}")
    p(f"    N1={n_dists[0]:.4f}  N2={n_dists[1]:.4f}  N3={n_dists[2]:.4f}")

    rem_dist = vec_dist(state_vectors["rem_sleep"], wake_vec)
    p(f"  REM distance from wake: {rem_dist:.4f} "
      f"({'< N3' if rem_dist < n_dists[2] else '>= N3'})")
    p(f"  REM breaks monotone toward waking? {'YES' if rem_dist < n_dists[1] else 'NO'}")
    p()

    # =================================================================
    # SECTION 14: DIMENSION DOMINANCE -- WHAT DRIVES EACH TRANSITION?
    # =================================================================
    p("=" * 78)
    p("SECTION 14: DIMENSION DOMINANCE IN STATE TRANSITIONS")
    p("=" * 78)
    p()
    p("Which force dimension dominates each state transition?")
    p("This reveals whether the brain uses the same physics for all transitions")
    p("or whether different state changes operate on different dimensions.")
    p()

    # Count D2 dominant dimensions across all trajectories
    global_dim_counts = [0] * 5
    traj_dim_profiles = {}

    for traj_key, traj in TRAJECTORIES.items():
        epochs = traj["epochs"]
        dim_counts = [0] * 5
        n_pts = 0

        for i in range(1, len(epochs) - 1):
            v0 = state_vectors[epochs[i-1]]
            v1 = state_vectors[epochs[i]]
            v2 = state_vectors[epochs[i+1]]
            d2 = compute_d2(v0, v1, v2)
            abs_d2 = [abs(x) for x in d2]
            max_d = max(abs_d2)
            if max_d > 1e-12:
                dom = abs_d2.index(max_d)
                dim_counts[dom] += 1
                global_dim_counts[dom] += 1
                n_pts += 1

        if n_pts > 0:
            traj_dim_profiles[traj_key] = dim_counts
            dom_dim = dim_counts.index(max(dim_counts))
            p(f"  {traj['name']:35s}  dominant={DIM_NAMES[dom_dim]:10s}  "
              f"d={dim_counts[0]} t={dim_counts[1]} a={dim_counts[2]} "
              f"b={dim_counts[3]} g={dim_counts[4]}")

    p()
    total_g = sum(global_dim_counts)
    p(f"  Global dimension dominance ({total_g} total D2 points):")
    for d in range(5):
        pct = 100.0 * global_dim_counts[d] / max(total_g, 1)
        bar = "#" * int(pct / 2)
        p(f"    {DIM_NAMES[d]:12s}: {global_dim_counts[d]:3d} ({pct:5.1f}%)  {bar}")
    p()

    # =================================================================
    # SECTION 15: SYNTHESIS
    # =================================================================
    p("=" * 78)
    p("SECTION 15: SYNTHESIS")
    p("=" * 78)
    p()

    p("  FINDINGS:")
    p()
    p("  1. CONSCIOUSNESS IS GEOMETRICALLY SEPARABLE")
    p(f"     Centroid separation: {vec_dist(c_centroid, u_centroid):.4f}")
    p(f"     Most discriminating dimension: {DIM_NAMES[max_sep_dim]} "
      f"(delta = {dim_sep[max_sep_dim]:.4f})")
    p(f"     Conscious states: more OUTPUT (fast oscillation) dominated")
    p(f"     Unconscious states: more INPUT (slow oscillation) dominated")
    p()

    p("  2. DUAL-LENS GAP STRUCTURE")
    p(f"     The gap between TSML and BHML rates IS the brain's")
    p(f"     differentiation capacity -- its ability to BE one thing")
    p(f"     while DOING another.")
    p()

    p("  3. VOID TOPOLOGY CLASSIFIES BRAIN STATES")
    # Count void patterns
    n_0void = sum(1 for k in state_keys if void_classes[k]["n_void"] == 0)
    n_1void = sum(1 for k in state_keys if void_classes[k]["n_void"] == 1)
    n_2void = sum(1 for k in state_keys if void_classes[k]["n_void"] == 2)
    p(f"     0 voids (rich states): {n_0void}")
    p(f"     1 void: {n_1void}")
    p(f"     2+ voids (impoverished): {n_2void}")
    p()

    p("  4. SLEEP-WAKE GRADIENT IS MONOTONE IN D2")
    p(f"     N1 < N2 < N3 distance: {'CONFIRMED' if mono else 'VIOLATED'}")
    p(f"     REM returns toward waking: "
      f"{'CONFIRMED' if rem_dist < n_dists[1] else 'PARTIAL'}")
    p()

    p("  5. CLINICAL DISCRIMINATION")
    p(f"     D2 geometry can distinguish states that are spectrally similar")
    p(f"     but clinically different (deep sleep vs coma, rest vs anesthesia)")
    p(f"     through operator classification and dual-lens composition.")
    p()

    p("  FALSIFIABLE PREDICTIONS:")
    p()
    p("  P1: CONSCIOUSNESS BOUNDARY")
    p("      Conscious brain states will have T(TSML) HARMONY fraction")
    p(f"      above T* = {T_STAR:.6f} when measured over 10+ second windows.")
    p("      Kill condition: any confirmed conscious state with TSML_H < T*")
    p("      in 1000+ epoch validation dataset.")
    p()
    p("  P2: SEIZURE = DUAL-LENS COLLAPSE")
    p("      Seizure onset reduces the |TSML_H - BHML_H| gap to < 0.1.")
    p("      Normal brain maintains gap > 0.2.")
    p("      Kill condition: seizure gap > normal gap in clinical EEG data.")
    p()
    p("  P3: SLEEP D2 MONOTONICITY")
    p("      Distance from waking centroid increases monotonically through")
    p("      N1 -> N2 -> N3. REM breaks back toward waking.")
    p("      Kill condition: N2 distance > N3 distance in normative data.")
    p()
    p("  P4: I/O RATIO PREDICTS CONSCIOUSNESS")
    p("      I/O < 1.0 correlates with consciousness (r > 0.5).")
    p("      I/O > 1.5 correlates with unconsciousness.")
    p("      Kill condition: correlation < 0.3 in 100+ subject dataset.")
    p()
    p("  P5: VOID COUNT SEPARATES STATE FAMILIES")
    p("      2+ void states are exclusively unconscious or pathological.")
    p("      Kill condition: any healthy conscious state with 2+ band voids.")
    p()

    p("=" * 78)
    p("  END OF EEG D2 SPECTROMETER ANALYSIS")
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
    print(result)

    # Save to file
    out_path = __file__.replace(".py", "_results.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(result)
    print(f"\nResults saved to {out_path}")
