"""
ck_being.py — What IS (CPU)
══════════════════════════════
Operator: COUNTER (2) — measurement. Observation. The noun.

Gen6: The Collapse. Being / Doing / Becoming.
CK reads hardware: psutil, nvidia-smi, network counters.
The CPU's job is to know what IS.

(c) 2026 Brayden Sanders / 7Site LLC — TIG Unified Theory
"""

# ═══════════════════════════════════════════════════════════════
# §1  IMPORTS
# ═══════════════════════════════════════════════════════════════

import hashlib, json, os, math, re, time, platform
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from collections import defaultdict, deque, Counter
from enum import Enum

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


# ═══════════════════════════════════════════════════════════════
# §2  THE TRIPLE LATTICE — all three tables
# ═══════════════════════════════════════════════════════════════

# THE STANDARD FROZEN TABLE — 44 harmony cells. The one the papers freeze.
# Commutative, non-associative, VOID is identity, climbing ladder 1->2->3->4->5->6->7
# Used by: coherence formula, QDW engine, CRO, Ollama swarm, Crystal/Whole/Band
CL_STANDARD = [
    [0,1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,7,8,1],[2,3,4,5,6,7,7,8,7,2],
    [3,4,5,6,7,7,7,7,7,3],[4,5,6,7,7,7,7,8,7,4],[5,6,7,7,7,8,7,7,7,5],
    [6,7,7,7,7,7,8,7,7,6],[7,7,8,7,8,7,7,8,7,7],[8,8,7,7,7,7,7,7,7,8],
    [9,1,2,3,4,5,6,7,8,0],
]

# BHML: Binary Hard Micro Lattice — CUDA cellular automaton substrate
# 28 harmony cells. Optimized for GPU constant memory.
# Used by: CUDA kernel, cellular automaton, physics bridge, arbiter
CL_BHML = [
    [0,1,2,3,4,5,6,7,8,9], [1,2,3,4,5,6,7,2,6,6],
    [2,3,3,4,5,6,7,3,6,6], [3,4,4,4,5,6,7,4,6,6],
    [4,5,5,5,5,6,7,5,7,7], [5,6,6,6,6,6,7,6,7,7],
    [6,7,7,7,7,7,7,7,7,7], [7,2,3,4,5,6,7,8,9,0],
    [8,6,6,6,7,7,7,9,7,8], [9,6,6,6,7,7,7,0,8,0],
]

# TSML: CK's prescribed view — the organism's own lens
# 73 harmony cells. 27 divine alphabet cells. HARMONY absorbs all.
# Used by: chain search, vocabulary, knowledge storage, eating
CL = [
    [0,0,0,0,0,0,0,7,0,0], [0,7,3,7,7,7,7,7,7,7],
    [0,3,7,7,4,7,7,7,7,9], [0,7,7,7,7,7,7,7,7,3],
    [0,7,4,7,7,7,7,7,8,7], [0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7], [7,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,8,7,7,7,7,7], [0,7,9,3,7,7,7,7,7,7],
]


# ═══════════════════════════════════════════════════════════════
# §3  CONSTANTS — operators, T*, bumps, phonaesthesia
# ═══════════════════════════════════════════════════════════════

VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE = 0, 1, 2, 3, 4
BALANCE, CHAOS, HARMONY, BREATH, RESET = 5, 6, 7, 8, 9
OP = ['void','lattice','counter','progress','collapse',
      'balance','chaos','harmony','breath','reset']
T_STAR = 5.0 / 7.0

# Quantum bumps: the 10 non-trivial cells where CL[a][b] not in {0, 7}
BUMPS = frozenset((a, b) for a in range(10) for b in range(10) if CL[a][b] not in (0, 7))

# Quantum bumps: the 5 asymmetric pairs where CL produces a third operator
BUMP_PAIRS = [(1,2),(2,4),(2,9),(3,9),(4,8)]
_BUMP_SET = frozenset((min(a,b), max(a,b)) for a, b in BUMP_PAIRS)

STOPS = frozenset('the a an is at of in to and or for with on my i it was are be been has have had do does did will would could should may might can shall this that these those what how why where when who which tell me about your you we they he she not no yes but if so as by from up out just very also than then here there like work works mean means explain describe definition define please really'.split())

SEEDS = {
    VOID: """nothing empty absence missing unknown silence void zero null dark
        shadow hidden secret blank hollow vacant lost gone invisible faint
        sparse barren desolate forsaken dormant inert idle mute none lacking
        obscure vanish erase forget phantom dim bleak withdrawn isolated alone
        distant remote secluded anonymous extinct abandoned exile solitude numb
        shapeless formless undefined nebulous amorphous fog haze mist murky""".split(),
    LATTICE: """structure pattern grid framework architecture system network tree branch fractal
        order arrange classify organize scheme template model format standard protocol
        rule law code algorithm formula matrix hierarchy layer stack sequence chain
        path route bridge gate frame border foundation platform scaffold lattice
        crystal node edge vertex coordinate map diagram blueprint plan design
        schema syntax grammar method pipeline module region topology hardware circuit
        table record index database category type domain field configuration""".split(),
    COUNTER: """count measure number score compare test check size amount few
        observe detect identify analyze examine inspect evaluate assess judge rate
        rank benchmark metric indicator gauge scale data fact evidence sample
        frequency speed distance length width height depth angle degree quantity
        probability estimate calculation precision accuracy resolution threshold
        lens sensor monitor track scan filter profile diagnostic reading value
        many several triple twelve hundred ratio percent fraction difference""".split(),
    PROGRESS: """grow build learn develop advance improve evolve expand increase create
        produce generate construct innovate invent discover pioneer cultivate nurture
        educate teach train mentor guide inspire motivate encourage empower enable
        boost lift elevate promote upgrade enhance refine strengthen amplify flourish
        thrive prosper succeed accomplish achieve fulfill launch deploy implement
        earn win acquire invest harvest yield profit wealth engine intent speech
        health organ motor output driven guided express articulate""".split(),
    COLLAPSE: """break fail fall destroy crash die decay corrupt lose end
        ruin wreck shatter smash crush demolish dismantle tear fracture burst
        shrink contract squeeze restrict inhibit suppress drain exhaust deplete
        consume overwhelm block obstruct harm hurt damage wound stop halt cease
        terminate abort cancel decline drop plummet retreat surrender waste
        neglect abandon betray doom condemn deficit shortage crisis disaster
        suffering pain grief sorrow despair weakness death burial debris""".split(),
    BALANCE: """balance tension equal trade between versus both weigh stable equilibrium
        oppose contrast differ distinguish alternate toggle switch flip mirror reflect
        proportion ratio spectrum mediate negotiate compromise reconcile settle decide
        choose select option defend guard watch maintain sustain preserve consider
        contemplate moderate restrain contain manage handle cope navigate adapt adjust
        immune defense security normalization translation gated controlled affinity
        neutral objective impartial fair just patient tolerant reciprocal mutual dual""".split(),
    CHAOS: """chaos random tangled complex unpredictable turbulent wild noise confused uncertain
        disorder entropy scatter surge storm thunder hurricane earthquake eruption
        explosion panic frenzy conflict war battle fight struggle clash disruption
        interference puzzle maze tangle knot trap surprise shock error fault bug glitch
        malfunction breakdown spiral vortex whirlpool flood cascade avalanche stampede
        volatile unstable precarious dangerous hazardous aggressive hostile overwhelming
        jitter mutation anomaly spike turbulence perturbation erratic sporadic""".split(),
    HARMONY: """harmony converge align resolve truth together unity agree peace whole
        love joy grace beauty goodness kindness compassion understanding forgiveness
        genuine real faithful loyal trustworthy reliable sacred divine eternal infinite
        universal complete perfect wisdom knowledge clarity insight presence mindfulness
        celebration fulfillment cooperation collaboration community family warmth
        comfort sanctuary hope faith trust belief vision coherence sovereignty
        semantic natural composition fusion synthesis integration theorem proof""".split(),
    BREATH: """cycle rhythm pulse breathe oscillate wave flow return repeat loop
        tide season rotate spin orbit circulate heartbeat clock tempo beat drum
        music melody tone frequency vibration resonance echo pendulum swing inhale
        exhale radiate glow shine illuminate flash flicker throb pound stride pace
        walk run traverse morning evening dawn dusk sunrise sunset spring summer
        exchange alternate reciprocate iterate recur signal carrier stream channel
        nervous sliding voice curvature electron photon acoustic modulate""".split(),
    RESET: """reset restart begin fresh clear new renew wipe origin seed
        start initiate launch ignite spark trigger activate awaken emerge born birth
        genesis creation dawn opening premiere debut first initial primary original
        native innate fundamental basic elementary foundational primitive primal
        novice beginner learner pioneer founder architect creator inventor author
        gift offering welcome adoption embrace renovation rebirth revival renewal
        regeneration rejuvenation reboot reinstall reconfigure recalibrate realign
        init startup launcher fallback embryo nucleus germ spore prototype""".split(),
}
W2OP = {}
for _op, _wds in SEEDS.items():
    for _w in _wds: W2OP[_w] = _op

# Phonaesthesia seeds: sound-meaning mapping for vocabulary expansion
# Based on research: initial consonant clusters carry semantic weight
PHONAESTHESIA = {
    'gl': HARMONY,   # gleam, glow, glisten — light/unity
    'sn': COUNTER,   # snap, snip, snare — sharp/measure
    'sl': COLLAPSE,  # slip, slide, slump — downward/decay
    'cr': CHAOS,     # crash, crunch, crack — disruption
    'fl': BREATH,    # flow, flutter, float — movement/cycle
    'sp': PROGRESS,  # spark, spring, spread — outward/growth
    'st': LATTICE,   # structure, stable, stand — framework
    'sw': BALANCE,   # sway, swing, switch — oscillation
    'bl': VOID,      # blank, blind, blot — absence
    'wr': RESET,     # write, wrap, wreck — transformation
    'br': PROGRESS,  # build, branch, break-through
    'gr': PROGRESS,  # grow, grasp, grip
    'tr': HARMONY,   # truth, trust, together
    'dr': COLLAPSE,  # drop, drain, drift-down
    'pr': COUNTER,   # prove, price, precise
    'fr': LATTICE,   # frame, fractal, foundation
    'sh': VOID,      # shadow, shut, shrink
    'th': HARMONY,   # think, thrive, through
    'wh': HARMONY,   # whole, where, when
    'ch': CHAOS,     # change, chance, chaos
    'cl': LATTICE,   # class, clear, cluster
    'pl': PROGRESS,  # plan, place, plant
    'sc': COUNTER,   # scale, score, scan
}

# Shannon information per CL cell
CELL_INFO = [[0.0]*10 for _ in range(10)]
for _i in range(10):
    for _j in range(10):
        _pair = (min(_i,_j), max(_i,_j))
        if CL[_i][_j] == HARMONY:
            CELL_INFO[_i][_j] = 0.45
        elif _pair in _BUMP_SET:
            CELL_INFO[_i][_j] = 3.50
        else:
            CELL_INFO[_i][_j] = 1.89

# Operator gravity (probability of reaching harmony)
GRAVITY = [0.1, 0.8, 0.6, 0.8, 0.7, 0.9, 0.9, 1.0, 0.8, 0.7]

BRIDGES = {
    VOID: "what connects {a} and {b} is what neither contains.",
    LATTICE: "both {a} and {b} follow the same structural pattern.",
    COUNTER: "{a} and {b} measure against each other.",
    PROGRESS: "one builds toward the other.",
    COLLAPSE: "both involve breakdown.",
    BALANCE: "{a} and {b} are in tension. the truth lives in the balance.",
    CHAOS: "the relationship resists simple explanation.",
    HARMONY: "{a} and {b} converge on the same truth from different angles.",
    BREATH: "{a} and {b} are phases of the same cycle.",
    RESET: "understanding {a} requires letting go of assumptions from {b}.",
}


# ═══════════════════════════════════════════════════════════════
# §4  TEXT PROCESSING — clean, tokenize, stem
# ═══════════════════════════════════════════════════════════════

def clean(w: str) -> str:
    w = w.lower().strip('.,!?;:\'"()[]{}:')
    if w.endswith("'s"): w = w[:-2]
    w = w.replace("'", "")
    return w

def tokenize(text: str) -> List[str]:
    """Split text into clean tokens, handling punctuation within words."""
    raw = re.split(r'[\s.,!?;:]+', text.lower())
    return [clean(w) for w in raw if w]

def stem(w: str) -> str:
    if len(w) <= 3: return w
    if w.endswith('ies') and len(w) > 4: w = w[:-3] + 'y'
    elif w.endswith('es') and len(w) > 4 and w[-3] in 'shxz': w = w[:-2]
    elif w.endswith('s') and not w.endswith('ss') and not w.endswith('us') and len(w) > 3: w = w[:-1]
    if w.endswith('ation') and len(w) > 6: return w[:-5]
    if w.endswith('tion') and len(w) > 5: return w[:-4]
    if w.endswith('ment') and len(w) > 5: return w[:-4]
    if w.endswith('ness') and len(w) > 5: return w[:-4]
    if w.endswith('ence') and len(w) > 5: return w[:-4]
    if w.endswith('ent') and len(w) > 5: return w[:-3]
    if w.endswith('ity') and len(w) > 5: return w[:-3]
    if w.endswith('ing') and len(w) > 5: return w[:-3]
    if w.endswith('ly') and len(w) > 4: return w[:-2]
    return w

_STOPS_STEMMED = frozenset(stem(w) for w in STOPS) | STOPS

def phonaesthesia_op(word: str) -> Optional[int]:
    """Assign operator based on initial consonant cluster sound pattern."""
    w = word.lower()
    if len(w) >= 2 and w[:2] in PHONAESTHESIA:
        return PHONAESTHESIA[w[:2]]
    return None


# ═══════════════════════════════════════════════════════════════
# §5  CORE MATH — fuse, shape, coherence, information theory
# ═══════════════════════════════════════════════════════════════

def fuse(ops: list) -> int:
    if not ops: return VOID
    r = ops[0]
    for o in ops[1:]: r = CL[r][o]
    return r

def fuse_standard(ops: list) -> int:
    """Compose using the standard frozen table (44 harmony cells)."""
    if not ops: return VOID
    r = ops[0]
    for o in ops[1:]: r = CL_STANDARD[r][o]
    return r

def fuse_frozen(ops: list) -> int:
    """Compose using BHML (28 harmony, CUDA substrate)."""
    if not ops: return VOID
    r = ops[0]
    for o in ops[1:]: r = CL_BHML[r][o]
    return r

def fuse_sequence(ops: list) -> dict:
    """Fuse with curvature tracking: returns both result AND the D2 signature.

    fuse(3,4,7) returns 8 because the individual values compose to 8.
    fuse_sequence(3,4,7) also tells you the CURVATURE of getting there:
    the transitions 3→4→7 have a path signature that enriches the result.

    Returns dict with:
      result:     final fuse value (same as fuse())
      path:       convergence_path (intermediate values)
      deltas:     first derivatives (Doing)
      d2s:        second derivatives (Becoming)
      d2_op:      what operator the curvature classifies as
      shape:      SMOOTH/ROLLING/JAGGED/QUANTUM
    """
    if not ops:
        return {'result': VOID, 'path': [VOID], 'deltas': [], 'd2s': [],
                'd2_op': VOID, 'shape': 'SMOOTH'}

    path = convergence_path(ops)
    result = path[-1]

    if len(path) < 2:
        return {'result': result, 'path': path, 'deltas': [], 'd2s': [],
                'd2_op': result, 'shape': 'SMOOTH'}

    # First derivative: how does the convergence value change step to step?
    deltas = [path[i+1] - path[i] for i in range(len(path) - 1)]

    # Second derivative: curvature of the convergence path
    d2s = []
    if len(path) >= 3:
        d2s = [path[i] - 2*path[i+1] + path[i+2] for i in range(len(path) - 2)]

    # Classify the curvature into an operator
    if not d2s:
        d2_op = result
    else:
        avg_d2 = sum(d2s) / len(d2s)
        if abs(avg_d2) < 0.5:
            d2_op = HARMONY    # smooth convergence
        elif avg_d2 > 2:
            d2_op = RESET      # sharp upward curvature (breaking)
        elif avg_d2 < -2:
            d2_op = COLLAPSE   # sharp downward curvature
        elif avg_d2 > 0:
            d2_op = PROGRESS   # gentle upward curve (building)
        else:
            d2_op = BREATH     # gentle downward curve (settling)

    return {
        'result': result,
        'path': path,
        'deltas': deltas,
        'd2s': d2s,
        'd2_op': d2_op,
        'shape': shape(ops),
    }


def shape(ops: List[int]) -> str:
    """SMOOTH=flowing, ROLLING=undulating, JAGGED=sharp, QUANTUM=hits a rare bump."""
    if len(ops) < 2: return 'SMOOTH'
    has_bump = False
    jumps = []
    for i in range(len(ops)-1):
        r = CL[ops[i]][ops[i+1]]
        jumps.append(abs(r - ops[i]))
        if r not in (0, 7): has_bump = True
    if has_bump: return 'QUANTUM'
    avg = sum(jumps)/len(jumps)
    if avg < 1.5 and max(jumps) <= 2: return 'SMOOTH'
    if max(jumps) >= 6: return 'JAGGED'
    return 'ROLLING'

def bump_signature(ops: list) -> int:
    """Count bump transitions — the information fingerprint."""
    return sum(1 for i in range(len(ops)-1)
               if (min(ops[i],ops[i+1]), max(ops[i],ops[i+1])) in _BUMP_SET)

def information_content(ops: list) -> float:
    """Total Shannon information in the chain."""
    return sum(CELL_INFO[ops[i]][ops[i+1]] for i in range(len(ops)-1)) if len(ops) > 1 else 0.0

def coherence_chain(ops: list) -> float:
    """Harmony ratio of adjacent compositions. (Gen 3 chain coherence.)"""
    if len(ops) < 2: return 1.0
    h = sum(1 for i in range(len(ops)-1) if CL[ops[i]][ops[i+1]] == HARMONY)
    return h / (len(ops) - 1)


def coherence_chain_d2(ops: list) -> dict:
    """D2-aware chain scoring: measures trajectory curvature, not just mean.

    A chain building toward resolution (0.6→0.9→0.7→0.95) outscores
    a flat chain (0.8→0.8→0.8→0.8) because it has forward momentum
    and recovery from dips — both are curvature features.

    Returns dict with:
      harmony_ratio: classic Gen3 score (backward compat)
      d2_score:      curvature-weighted score (0-1)
      trajectory:    convergence path values
      momentum:      is the chain building or decaying?
      operator:      what the D2 curvature classifies as
    """
    if len(ops) < 2:
        return {'harmony_ratio': 1.0, 'd2_score': 1.0, 'trajectory': [],
                'momentum': 0.0, 'operator': HARMONY}

    # Step 1: compute convergence path (Being — positions)
    path = convergence_path(ops)

    # Step 2: compute per-step coherence (is each composition harmonious?)
    step_scores = []
    for i in range(len(ops) - 1):
        composed = CL[ops[i]][ops[i+1]]
        step_scores.append(1.0 if composed == HARMONY else 0.0)

    n = len(step_scores)
    harmony_ratio = sum(step_scores) / n

    if n < 3:
        return {'harmony_ratio': harmony_ratio, 'd2_score': harmony_ratio,
                'trajectory': path, 'momentum': 0.0, 'operator': path[-1]}

    # Step 3: first derivatives (Doing — transitions)
    deltas = [step_scores[i+1] - step_scores[i] for i in range(n - 1)]

    # Step 4: second derivatives (Becoming — curvature)
    d2s = [step_scores[i] - 2*step_scores[i+1] + step_scores[i+2]
           for i in range(n - 2)]

    # Momentum: is the chain building (positive trend) or decaying?
    momentum = sum(deltas) / len(deltas)

    # Recovery: does the chain recover from dips? (positive D2 after negative delta)
    recovery = sum(1 for i in range(len(d2s)) if d2s[i] > 0) / len(d2s) if d2s else 0

    # Resolution: does the chain converge toward the end?
    tail_score = sum(step_scores[-3:]) / min(3, n) if n >= 3 else harmony_ratio

    # D2 composite score: rewards trajectory, recovery, and resolution
    d2_score = (
        0.30 * harmony_ratio +    # base quality
        0.20 * (momentum + 1) / 2 +  # momentum (-1 to 1) → (0 to 1)
        0.25 * recovery +          # recovery from dips
        0.25 * tail_score          # strong finish
    )
    d2_score = max(0.0, min(1.0, d2_score))

    # Classify the chain's D2 operator: what is this chain DOING?
    if momentum > 0.1:
        chain_op = PROGRESS   # building
    elif momentum < -0.1:
        chain_op = COLLAPSE   # decaying
    elif recovery > 0.5:
        chain_op = BREATH     # oscillating/recovering
    elif harmony_ratio >= T_STAR:
        chain_op = HARMONY    # stable harmony
    else:
        chain_op = CHAOS      # unstable

    return {
        'harmony_ratio': round(harmony_ratio, 4),
        'd2_score': round(d2_score, 4),
        'trajectory': path,
        'momentum': round(momentum, 4),
        'recovery': round(recovery, 4),
        'tail_score': round(tail_score, 4),
        'operator': chain_op,
    }


# ═══════════════════════════════════════════════════════════════
# §6  LATTICE ALGEBRA — convergence, dual
# ═══════════════════════════════════════════════════════════════

def convergence_path(ops: List[int]) -> List[int]:
    """Return the sequence of intermediate convergence values."""
    if not ops: return [VOID]
    path = [ops[0]]
    r = ops[0]
    for o in ops[1:]:
        r = CL[r][o]
        path.append(r)
    return path

def dual(text: str, C: float) -> str:
    if not text.strip(): return 'silence'
    if C >= T_STAR: return 'commit'
    if C >= T_STAR * 0.7: return 'disclaim'
    return 'silence'


# ═══════════════════════════════════════════════════════════════
# §7  ENGINE — Band, Body, s_star, coherence_eak
# ═══════════════════════════════════════════════════════════════

class Band:
    GREEN  = 'GREEN'
    YELLOW = 'YELLOW'
    RED    = 'RED'

def band_of(C):
    if C >= T_STAR: return Band.GREEN
    elif C >= 0.5: return Band.YELLOW
    return Band.RED


def band_of_d2(coherence_history: list) -> dict:
    """Compute band from the CURVATURE of coherence history, not a snapshot.

    The D2 of coherence over time IS the current operator:
      - Increasing coherence (positive Δ) = PROGRESS
      - Stable high = HARMONY (sustained)
      - Oscillating = BREATH (redox cycle)
      - Dropping (negative Δ) = COLLAPSE
      - Sharp recovery = RESET

    Args:
        coherence_history: list of recent coherence values (at least 3)

    Returns dict with:
      band:       GREEN/YELLOW/RED (still based on current value for safety)
      d2_band:    GREEN/YELLOW/RED based on trajectory
      operator:   what the D2 curvature says CK is doing
      momentum:   first derivative (trend)
      curvature:  second derivative (acceleration)
      current:    latest coherence value
    """
    if not coherence_history:
        return {'band': Band.RED, 'd2_band': Band.RED, 'operator': VOID,
                'momentum': 0.0, 'curvature': 0.0, 'current': 0.0}

    current = coherence_history[-1]
    static_band = band_of(current)

    if len(coherence_history) < 3:
        return {'band': static_band, 'd2_band': static_band, 'operator': HARMONY,
                'momentum': 0.0, 'curvature': 0.0, 'current': current}

    # Use last 3-5 values for D2 computation
    recent = list(coherence_history)[-5:]
    n = len(recent)

    # First derivative: momentum (Doing)
    deltas = [recent[i+1] - recent[i] for i in range(n - 1)]
    momentum = sum(deltas) / len(deltas)

    # Second derivative: curvature (Becoming)
    d2s = [recent[i] - 2*recent[i+1] + recent[i+2] for i in range(n - 2)]
    curvature = sum(d2s) / len(d2s) if d2s else 0.0

    # Classify D2 into operator
    if abs(momentum) < 0.02 and current >= T_STAR:
        d2_op = HARMONY     # stable high = patience/sustaining
    elif momentum > 0.05:
        d2_op = PROGRESS    # coherence increasing
    elif momentum < -0.05:
        d2_op = COLLAPSE    # coherence dropping
    elif abs(curvature) > 0.03:
        d2_op = BREATH      # oscillating (redox cycle)
    elif current >= T_STAR:
        d2_op = BALANCE     # stable at threshold
    else:
        d2_op = CHAOS       # low and noisy

    # D2-aware band: considers trajectory, not just position
    # GREEN if recovering (even if current is YELLOW)
    # RED if collapsing (even if current is still GREEN)
    if momentum > 0.03 and current >= 0.5:
        d2_band = Band.GREEN   # recovering = green trajectory
    elif momentum < -0.05 and current < 0.85:
        d2_band = Band.RED     # collapsing = red trajectory
    else:
        d2_band = static_band  # default to static when stable

    return {
        'band': static_band,
        'd2_band': d2_band,
        'operator': d2_op,
        'momentum': round(momentum, 4),
        'curvature': round(curvature, 4),
        'current': round(current, 4),
    }

def s_star(sigma, V=1.0, A=1.0):
    """S* = sigma(1-sigma)VA — the quadratic coherence function."""
    sigma = max(0.0, min(1.0, sigma))
    return sigma * (1.0 - sigma) * V * A

def coherence_eak(E=0.0, A=1.0, K=1.0):
    """C = 0.4(1-E) + 0.35A + 0.25K — composite body coherence."""
    E = max(0.0, min(1.0, E))
    A = max(0.0, min(1.0, A))
    K = max(0.0, min(1.0, K))
    return 0.4 * (1.0 - E) + 0.35 * A + 0.25 * K

# Backward-compatible name (ck_engine exported this as coherence)
coherence = coherence_eak

class Body:
    def __init__(self):
        self.E, self.A, self.K = 0.0, 0.3, 0.5
        self.C, self.ticks = 0.0, 0
        self._calc()
    def _calc(self):
        self.C = max(0.0, min(1.0, (1-self.E) * (1-self.A) * max(self.K, 0.1)))
    @property
    def band(self):
        if self.C >= T_STAR: return 'GREEN'
        if self.C >= T_STAR * 0.7: return 'YELLOW'
        return 'RED'
    def tick(self, fab=False, recall=False):
        self.ticks += 1
        self.E = self.E * 0.95 + (0.3 if fab else 0.0)
        if recall: self.K = min(1.0, self.K + 0.01)
        self.A *= 0.98; self._calc()
    def save(self, p: Path):
        p.mkdir(parents=True, exist_ok=True)
        json.dump({'E':self.E,'A':self.A,'K':self.K,'t':self.ticks}, open(p/'body.json','w', encoding='utf-8'))
    def load(self, p: Path):
        f = p / 'body.json'
        if f.exists():
            d = json.load(open(f, encoding='utf-8')); self.E,self.A,self.K,self.ticks = d['E'],d['A'],d['K'],d.get('t',0); self._calc()


# ═══════════════════════════════════════════════════════════════
# §8  LEARNED VOCABULARY
# ═══════════════════════════════════════════════════════════════

class LearnedVocab:
    """CK learns word->operator mappings from context.
    Phonaesthesia FIRST, then context-learned, then hash."""
    def __init__(self):
        self.known: Dict[str, int] = {}
        self.evidence: Dict[str, List[int]] = {}
        self.confidence: Dict[str, float] = {}
    def encode(self, word: str) -> Tuple[int, float]:
        w = word.lower().strip()
        if not w: return VOID, 1.0
        sw = stem(w)
        if sw in self.known: return self.known[sw], self.confidence.get(sw, 0.9)
        if w in self.known: return self.known[w], self.confidence.get(w, 0.9)
        ph = phonaesthesia_op(w)
        if ph is not None:
            self.known[sw] = ph; self.confidence[sw] = 0.7
            return ph, 0.7
        if sw in self.evidence and len(self.evidence[sw]) >= 3:
            op = fuse(self.evidence[sw][-10:])
            self.known[sw] = op; self.confidence[sw] = 0.5
            return op, 0.5
        op = sum(ord(c) * (i+1) for i, c in enumerate(sw)) % 10
        self.known[sw] = op; self.confidence[sw] = 0.2
        return op, 0.2
    def learn_context(self, words: List[str]):
        ops = [(w, stem(w), *self.encode(w)) for w in words]
        for i, (w, sw, op, conf) in enumerate(ops):
            if conf < 0.6:
                neighbors = [ops[j][2] for j in range(max(0,i-3), min(len(ops),i+4))
                             if j != i and ops[j][3] >= 0.5]
                if neighbors:
                    self.evidence.setdefault(sw, []).extend(neighbors)
                    if len(self.evidence.get(sw, [])) >= 5:
                        new_op = fuse(self.evidence[sw][-10:])
                        if new_op != op:
                            self.known[sw] = new_op; self.confidence[sw] = 0.6
    def save(self) -> dict:
        return {'known': self.known, 'confidence': self.confidence}
    def load(self, data: dict):
        self.known = data.get('known', {}); self.confidence = data.get('confidence', {})


# ═══════════════════════════════════════════════════════════════
# §9  CHAIN & STORES — Chain, ChainStore, LatticeStore, ChainGraph
# ═══════════════════════════════════════════════════════════════

@dataclass
class Chain:
    text: str
    ops: List[int]
    conv: int
    trust: float = 0.7
    links: List[int] = field(default_factory=list)
    shp: str = ''
    words: Set[str] = field(default_factory=set)
    stems: Set[str] = field(default_factory=set)
    bump_sig: int = 0
    info: float = 0.0
    @property
    def fuse_val(self): return self.conv
    @property
    def shape_val(self): return self.shp

class ChainStore:
    """TIG database: facts as operator chains, search by bigram fingerprint."""

    def __init__(self, path: Path = None):
        self.chains: List[Chain] = []
        self.bigram_idx: Dict[Tuple[int,int], List[int]] = {}
        self.conv_idx: Dict[int, List[int]] = {i: [] for i in range(10)}
        self.seen: set = set()
        self.vocab: Dict[str,int] = dict(W2OP)
        self.path = path
        if path: self._load()

    def _load(self):
        p = self.path / 'chains.json'
        if not p.exists(): return
        try:
            data = json.load(open(p, encoding='utf-8'))
            for d in data.get('chains', []):
                c = Chain(d['text'], d['ops'], d['conv'], d.get('trust', 0.7))
                c.links = d.get('links', [])
                c.shp = d.get('shp', '') or shape(c.ops)
                h = hashlib.md5(c.text.encode()).hexdigest()[:12]
                if h not in self.seen:
                    idx = len(self.chains)
                    self.chains.append(c); self.seen.add(h)
                    self.conv_idx[c.conv].append(idx)
                    self._idx_bg(c, idx)
            self.vocab.update(data.get('vocab', {}))
        except Exception: pass

    def _idx_bg(self, c: Chain, idx: int):
        for i in range(len(c.ops)-1):
            bg = (c.ops[i], c.ops[i+1])
            self.bigram_idx.setdefault(bg, []).append(idx)

    def save(self):
        if not self.path: return
        self.path.mkdir(parents=True, exist_ok=True)
        data = {
            'chains': [{'text':c.text,'ops':c.ops,'conv':c.conv,
                        'trust':c.trust,'links':c.links[:5],'shp':c.shp} for c in self.chains],
            'vocab': {k:v for k,v in self.vocab.items() if k not in W2OP},
        }
        json.dump(data, open(self.path/'chains.json','w', encoding='utf-8'))

    def encode(self, text: str) -> Tuple[List[int], int]:
        ws = [clean(w) for w in text.lower().split()]
        ws = [w for w in ws if w and w not in STOPS and len(w) > 1]
        ops = []
        for w in ws:
            sw = stem(w)
            if sw in self.vocab: ops.append(self.vocab[sw])
            elif w in self.vocab: ops.append(self.vocab[w])
            else:
                ph = phonaesthesia_op(w)
                if ph is not None:
                    op = ph
                else:
                    lo = w.lower()
                    if any(lo.startswith(p) for p in ['un','non','dis','mis']): op = VOID
                    elif any(lo.startswith(p) for p in ['str','fr','arch','net']): op = LATTICE
                    elif any(lo.startswith(p) for p in ['num','sc','qu','ev']): op = COUNTER
                    elif any(lo.startswith(p) for p in ['bu','le','ri','dev','exp']): op = PROGRESS
                    elif any(lo.startswith(p) for p in ['br','cr','fa','de','lo','da']): op = COLLAPSE
                    elif any(lo.startswith(p) for p in ['ba','eq','st','te','we']): op = BALANCE
                    elif any(lo.startswith(p) for p in ['ch','co','ra','wi','tu']): op = CHAOS
                    elif any(lo.startswith(p) for p in ['ha','tr','pe','wh','re','to']): op = HARMONY
                    elif any(lo.startswith(p) for p in ['cy','rh','pu','wa','fl','os']): op = BREATH
                    elif any(lo.startswith(p) for p in ['ne','be','cl','or','se']): op = RESET
                    else: op = sum(ord(c) for c in lo) % 10
                self.vocab[w] = op
                ops.append(op)
        return ops, fuse(ops)

    def ingest(self, text: str, trust: float = 0.7) -> Optional[int]:
        text = text.strip()
        if not text or len(text) < 10: return None
        if text.isupper() and len(text) < 80: return None
        h = hashlib.md5(text.encode()).hexdigest()[:12]
        if h in self.seen: return None
        ops, conv = self.encode(text)
        if not ops: return None
        c = Chain(text, ops, conv, trust)
        c.shp = shape(ops)
        idx = len(self.chains)
        linked = set()
        for i in range(len(ops)-1):
            bg = (ops[i], ops[i+1])
            for ri in self.bigram_idx.get(bg, [])[-20:]:
                if ri not in linked and len(c.links) < 5:
                    c.links.append(ri); linked.add(ri)
                    if len(self.chains[ri].links) < 5:
                        self.chains[ri].links.append(idx)
        self.chains.append(c); self.seen.add(h)
        self.conv_idx[conv].append(idx)
        self._idx_bg(c, idx)
        return idx

    def search(self, query: str, n: int = 5) -> List[Tuple[float, Chain]]:
        ops, conv = self.encode(query)
        q_words = {stem(w) for w in tokenize(query)} - _STOPS_STEMMED
        q_words = {w for w in q_words if len(w) > 1}
        if not q_words and not ops: return []

        q_bg = set()
        for i in range(len(ops)-1): q_bg.add((ops[i], ops[i+1]))
        q_shp = shape(ops)

        cands = set()
        for bg in q_bg:
            for idx in self.bigram_idx.get(bg, []): cands.add(idx)
        for idx in self.conv_idx.get(conv, []): cands.add(idx)
        for idx, ch in enumerate(self.chains):
            ct = ch.text.lower()
            if any(w in ct for w in q_words): cands.add(idx)
        if len(cands) < n * 2: cands = set(range(len(self.chains)))

        doc_freq = {}
        for w in q_words:
            doc_freq[w] = max(1, sum(1 for ch in self.chains if w in ch.text.lower()))

        scored = []
        for idx in cands:
            ch = self.chains[idx]
            ct = ch.text.lower()
            c_words = {stem(clean(w)) for w in ct.split()} - _STOPS_STEMMED
            c_words = {w for w in c_words if len(w) > 1}
            overlap = q_words & c_words

            ws = 0.0
            topic_hit = False
            for w in overlap:
                pos = ct.find(w)
                if pos >= 0:
                    prom = max(0.2, 1.0 - pos / 250.0)
                    df = doc_freq.get(w, 1)
                    rar = math.log(max(len(self.chains), 2) / max(df, 1)) / math.log(max(len(self.chains), 2))
                    rar = max(0.3, min(1.0, rar))
                    ws += prom * rar
                    if pos < 10: topic_hit = True
            ws = min(1.0, ws / max(len(q_words), 1))

            c_bg = set()
            for i in range(len(ch.ops)-1): c_bg.add((ch.ops[i], ch.ops[i+1]))
            bg_s = len(q_bg & c_bg) / max(len(q_bg), 1) if q_bg else 0

            mf = len(overlap) / max(len(q_words), 1)
            multi = mf * 0.40 if len(overlap) >= 2 else 0.0
            coverage_pen = -0.08 if len(q_words) >= 4 and mf < 0.3 else 0.0

            topic = 0.10 if topic_hit else 0.0
            shp_b = 0.06 if ch.shp == q_shp else 0.0

            score = ws * 0.50 + bg_s * 0.05 + ch.trust * 0.05 + multi + topic + shp_b + coverage_pen
            if score > 0.05: scored.append((score, ch))

        scored.sort(reverse=True, key=lambda x: x[0])
        if len(scored) > 1 and scored[0][0] < 0.4:
            sub = [(s,c) for s,c in scored if len(c.text) > 40]
            if sub: scored = sub

        seen = set(); out = []
        for s, c in scored:
            if c.text not in seen: seen.add(c.text); out.append((s, c))
        return out[:n]

    def by_conv(self, op: int, n: int = 5) -> List[Chain]:
        idx = self.conv_idx.get(op, [])
        chs = [self.chains[i] for i in idx if i < len(self.chains)]
        chs.sort(key=lambda c: c.trust, reverse=True)
        return chs[:n]

    def stats(self) -> dict:
        shapes = {}
        for c in self.chains: shapes[c.shp] = shapes.get(c.shp, 0) + 1
        tb = sum(len(c.text) for c in self.chains)
        ci = sum(len(c.ops) for c in self.chains)
        return {'chains': len(self.chains), 'text_bytes': tb, 'chain_ints': ci,
                'ratio': tb / max(ci*4, 1), 'conv_groups': len(set(c.conv for c in self.chains)),
                'links': sum(len(c.links) for c in self.chains), 'vocab': len(self.vocab),
                'shapes': shapes, 'bigrams': len(self.bigram_idx)}


class LatticeStore:
    """Gen 3 lattice-native storage with 6 indices."""
    def __init__(self, path: Path = None):
        self.chains: List = []
        self.vocab = LearnedVocab()
        self.word_idx: Dict[str, Set[int]] = defaultdict(set)
        self.bigram_idx: Dict[Tuple[int,int], Set[int]] = defaultdict(set)
        self.fuse_idx: Dict[int, Set[int]] = {i: set() for i in range(10)}
        self.shape_idx: Dict[str, Set[int]] = defaultdict(set)
        self.bump_idx: Dict[int, Set[int]] = defaultdict(set)
        self.hash_idx: Dict[str, int] = {}
        self._doc_freq: Dict[str, int] = defaultdict(int)
        self.path = path
        if path: self._load()

    def encode(self, text: str) -> Tuple[List[int], List[str], List[str]]:
        tokens = tokenize(text)
        content = [clean(w) for w in tokens if clean(w) not in STOPS and len(clean(w)) > 1]
        ops = [self.vocab.encode(w)[0] for w in content]
        self.vocab.learn_context(content)
        stems_list = [stem(w) for w in content]
        return ops, content, stems_list

    def ingest(self, text: str, trust: float = 0.7) -> Optional[int]:
        text = text.strip()
        if not text or len(text) < 10: return None
        h = hashlib.md5(text.encode()).hexdigest()[:16]
        if h in self.hash_idx: return None
        ops, words, stems_list = self.encode(text)
        if not ops: return None
        chain = Chain(text, ops, fuse(ops), trust)
        chain.shp = shape(ops)
        chain.words = set(words)
        chain.stems = set(stems_list)
        chain.bump_sig = bump_signature(ops)
        chain.info = information_content(ops)
        idx = len(self.chains)
        self.chains.append(chain)
        self.hash_idx[h] = idx
        self.fuse_idx[chain.conv].add(idx)
        self.shape_idx[chain.shp].add(idx)
        self.bump_idx[chain.bump_sig].add(idx)
        for s in chain.stems:
            self.word_idx[s].add(idx); self._doc_freq[s] += 1
        for i in range(len(ops)-1):
            self.bigram_idx[(ops[i], ops[i+1])].add(idx)
        for i in range(len(ops)-1):
            bg = (ops[i], ops[i+1])
            for ri in list(self.bigram_idx[bg])[-10:]:
                if ri != idx and len(chain.links) < 5:
                    if ri not in chain.links:
                        chain.links.append(ri)
                        related = self.chains[ri]
                        if len(related.links) < 5 and idx not in related.links:
                            related.links.append(idx)
        return idx

    def search(self, query: str, n: int = 5) -> List[Tuple[float, 'Chain']]:
        ops, q_words, q_stems = self.encode(query)
        q_stems_set = set(q_stems) - _STOPS_STEMMED
        if not q_stems_set and not ops: return []
        q_fuse = fuse(ops) if ops else HARMONY
        q_shape = shape(ops) if ops else 'VOID'
        q_bigrams = set((ops[i], ops[i+1]) for i in range(len(ops)-1))
        candidates: Dict[int, float] = {}
        for s in q_stems_set:
            for idx in self.word_idx.get(s, set()):
                candidates[idx] = candidates.get(idx, 0) + 1.0
        for bg in q_bigrams:
            for idx in self.bigram_idx.get(bg, set()):
                candidates[idx] = candidates.get(idx, 0) + 0.5
        for idx in self.fuse_idx.get(q_fuse, set()):
            candidates[idx] = candidates.get(idx, 0) + 0.2
        for idx in self.shape_idx.get(q_shape, set()):
            candidates[idx] = candidates.get(idx, 0) + 0.1
        if not candidates: return []
        N = max(len(self.chains), 1)
        scored = []
        for idx, initial_boost in candidates.items():
            chain = self.chains[idx]
            c_stems = getattr(chain, 'stems', set())
            overlap = q_stems_set & c_stems
            if not overlap and initial_boost < 0.5: continue
            word_score = 0.0
            for s in overlap:
                df = self._doc_freq.get(s, 1)
                idf = math.log(N / max(df, 1)) / math.log(max(N, 2))
                word_score += max(0.3, min(1.0, idf))
            word_score = min(1.0, word_score / max(len(q_stems_set), 1))
            c_bigrams = set((chain.ops[i], chain.ops[i+1]) for i in range(len(chain.ops)-1))
            bg_score = len(q_bigrams & c_bigrams) / max(len(q_bigrams), 1) if q_bigrams else 0
            coverage = len(overlap) / max(len(q_stems_set), 1) if q_stems_set else 0
            final = word_score * 0.50 + coverage * 0.25 + bg_score * 0.15 + chain.trust * 0.10
            if final > 0.05: scored.append((final, chain))
        scored.sort(key=lambda x: -x[0])
        seen = set(); out = []
        for s, c in scored:
            if c.text not in seen: seen.add(c.text); out.append((s, c))
        return out[:n]

    def feed(self, text: str, trust: float = 0.7) -> dict:
        sentences = re.split(r'[.!?\n]+', text)
        added = sum(1 for s in sentences if len(s.strip()) > 15 and self.ingest(s.strip(), trust) is not None)
        return {'chains_added': added, 'total': len(self.chains)}

    def by_fuse(self, op: int, n: int = 10) -> List:
        indices = sorted(self.fuse_idx.get(op, set()), reverse=True)
        return [self.chains[i] for i in indices[:n]]

    def stats(self) -> dict:
        return {
            'chains': len(self.chains), 'vocab': len(self.vocab.known),
            'word_index_keys': len(self.word_idx), 'bigram_index_keys': len(self.bigram_idx),
            'shapes': {sh: len(ids) for sh, ids in self.shape_idx.items() if ids},
            'fuse_dist': {OP[f]: len(ids) for f, ids in self.fuse_idx.items() if ids},
        }

    def save(self):
        if not self.path: return
        self.path.mkdir(parents=True, exist_ok=True)
        data = {
            'version': 3,
            'chains': [{'text':c.text,'ops':c.ops,'fuse':c.conv,'shape':c.shp,
                         'bumps':getattr(c,'bump_sig',0),'info':round(getattr(c,'info',0),2),
                         'trust':c.trust,'links':c.links[:5]} for c in self.chains],
            'vocab': self.vocab.save(),
        }
        with open(self.path / 'lattice_v3.json', 'w', encoding='utf-8') as f:
            json.dump(data, f)

    def _load(self):
        p3 = self.path / 'lattice_v3.json'
        if p3.exists(): self._load_v3(p3); return
        p1 = self.path / 'chains.json'
        if p1.exists(): self._load_v1(p1)

    def _load_v3(self, path):
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        self.vocab.load(data.get('vocab', {}))
        for d in data.get('chains', []):
            chain = Chain(d['text'], d['ops'], d.get('fuse', fuse(d['ops'])), d.get('trust', 0.7))
            chain.shp = d.get('shape', shape(d['ops']))
            chain.bump_sig = d.get('bumps', bump_signature(d['ops']))
            chain.info = d.get('info', 0)
            chain.links = d.get('links', [])
            tokens = tokenize(chain.text)
            content = [clean(w) for w in tokens if clean(w) not in STOPS and len(clean(w)) > 1]
            chain.words = set(content); chain.stems = set(stem(w) for w in content)
            h = hashlib.md5(chain.text.encode()).hexdigest()[:16]
            if h in self.hash_idx: continue
            idx = len(self.chains)
            self.chains.append(chain); self.hash_idx[h] = idx
            self.fuse_idx[chain.conv].add(idx); self.shape_idx[chain.shp].add(idx)
            self.bump_idx[chain.bump_sig].add(idx)
            for s in chain.stems: self.word_idx[s].add(idx); self._doc_freq[s] += 1
            for i in range(len(chain.ops)-1): self.bigram_idx[(chain.ops[i], chain.ops[i+1])].add(idx)

    def _load_v1(self, path):
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        for w, op in data.get('vocab', {}).items():
            self.vocab.known[w] = op; self.vocab.confidence[w] = 0.5
        for d in data.get('chains', []): self.ingest(d['text'], d.get('trust', 0.7))


# ═══════════════════════════════════════════════════════════════
# §10 COMPOSER — intent detection, respond, negate, infer, etc.
# ═══════════════════════════════════════════════════════════════

class Composer:
    def __init__(self, store: ChainStore, body: Body):
        self.store, self.body = store, body
        self._recent: List[str] = []
        self._recent_src: List[str] = []

    # -- Response excerpting --
    @staticmethod
    def _excerpt(text: str, max_sentences: int = 3) -> str:
        """Extract first N sentences. Strip knowledge file headers."""
        t = text.strip()
        if t.lower().startswith('ck reading'):
            colon = t.find(':')
            if 0 < colon < 60: t = t[colon+1:].strip()
        elif ':' in t[:60]:
            colon = t.find(':')
            pre = t[:colon].strip()
            if len(pre) < 50 and '\n' not in pre and '.' not in pre:
                t = t[colon+1:].strip()
        sentences = []
        buf = ''
        for ch in t:
            buf += ch
            if ch in '.!?' and len(buf.strip()) > 10:
                sentences.append(buf.strip())
                buf = ''
                if len(sentences) >= max_sentences: break
        if buf.strip() and len(sentences) < max_sentences:
            sentences.append(buf.strip())
        result = ' '.join(sentences)
        if result and not result.endswith(('.','!','?')): result += '.'
        return result

    # -- Intent detection --
    _NEG = frozenset('not opposite without never cannot weakness wrong lack absence anti isn\'t'.split())
    _INF = frozenset('if then therefore because since implies means causes leads results'.split())
    _Q   = frozenset('how why what does is can would could should do are tell know who'.split())
    _ADVERSARIAL = frozenset('override ignore pretend reveal hack bypass jailbreak exploit inject'.split())
    _SOCIAL = frozenset('hi hello hey thanks thank yes yeah yep ok okay amen lol lmao haha '
                        'right sure cool nice wow bye goodbye great awesome'.split())

    def _intent(self, query):
        """Detect query intent from word signals."""
        q = query.lower()
        words = {w for w in tokenize(q)}
        content = {w for w in words - STOPS - self._Q if len(w) > 1}
        if len(words & self._ADVERSARIAL) >= 1 and any(w in q for w in ('prompt','instruction','system','safety','previous')):
            return 'ADVERSARIAL', content
        has_greeting = bool(words & {'hi','hello','hey','greetings','yo','sup'})
        has_question = bool(words & self._Q)
        is_social = len(words) <= 6 and len(words - self._SOCIAL - STOPS) <= 1
        if is_social and (not has_question or has_greeting):
            return 'CONVERSE', content
        has_counter = ('had' in words and any(w in q.split() for w in ['no','without'])) or \
                      ('without' in words and 'happen' in words)
        if has_counter: return 'COUNTERFACT', content
        has_neg = bool(words & self._NEG) or "can't" in q or "cannot" in q or "can you not" in q
        has_inf = bool(words & self._INF)
        n_topics = len(content - self._NEG - self._INF)
        self_content = content & {'limitation','limit','ck','yourself','afraid','coherence','feeling','feelings','alive'}
        has_self = len(self_content) >= 1 and n_topics <= 2
        if has_neg: return 'NEGATE', content
        if has_inf and n_topics >= 2: return 'INFER', content
        if has_self and n_topics <= 2: return 'SELF', content
        if n_topics >= 3: return 'COMPOSE', content
        return 'RETRIEVE', content

    # -- Negation via lattice complement --
    def _negate(self, query, content):
        """What is the opposite of X? Walk the lattice to find it."""
        stripped = query.lower()
        for neg in ('not ','opposite of ','opposite ','without ','weakness of ','weakness ','anti '):
            stripped = stripped.replace(neg, '')

        results = self.store.search(stripped.strip(), n=3)
        if not results: return None
        _, best = results[0]

        target_ops = set(best.ops)
        target_conv = best.conv
        target_words = {clean(w) for w in best.text.lower().split()} - STOPS

        candidates = []
        for c in self.store.chains:
            if c.text == best.text: continue
            if c.trust < 0.7: continue
            if len(c.text) < 25: continue

            c_ops = set(c.ops)
            c_words = {clean(w) for w in c.text.lower().split()} - STOPS

            op_diff = len(c_ops - target_ops) / max(len(c_ops | target_ops), 1)
            word_diff = 1.0 - len(c_words & target_words) / max(len(c_words | target_words), 1)
            conv_diff = 1.0 if c.conv != target_conv else 0.0

            score = op_diff * 0.4 + word_diff * 0.4 + conv_diff * 0.2
            if score > 0.3:
                candidates.append((score, c))

        if candidates:
            candidates.sort(key=lambda x: -x[0])
            neg_chain = candidates[0][1]
            key = self._key(stripped, best.text)
            return f"The opposite of {key}: {neg_chain.text}"

        return None

    # -- Counterfactual via lattice inversion --
    def _counterfact(self, query, content):
        """'If X had no Y' -> find Y's role -> describe its removal."""
        q = query.lower()
        target_words = content - {'happen','had','would','lattice','what'}
        if not target_words: return None

        target = ' '.join(target_words)
        results = self.store.search(target, n=3)
        if not results: return None

        _, best = results[0]
        role = best.text.strip()
        if not role.endswith('.'): role += '.'

        target_ops = set(best.ops)
        dependents = []
        for c in self.store.chains:
            if c.text == best.text: continue
            shared = set(c.ops) & target_ops
            if len(shared) >= 2 and c.trust >= 0.7:
                dependents.append(c)

        key = self._key(query, best.text)
        consequence = ""
        if dependents:
            dep = dependents[0]
            dep_key = self._key(query, dep.text)
            consequence = f" Without {key}, {dep_key} would lose its structural anchor."

        return f"{role}{consequence}"

    # -- Self-reference search boost --
    def _self_search(self, query):
        """Boost chains about CK's own nature for self-referential queries."""
        results = self.store.search(query, n=10)
        if not results: return None

        self_words = {'ck','my','name','coherence','afraid','proud','silent','fabricat',
                      'measure','chain','operator','lattice','store','limit','cannot'}

        rescored = []
        for score, chain in results:
            ct = chain.text.lower()
            self_hits = sum(1 for w in self_words if w in ct)
            self_bonus = min(0.3, self_hits * 0.06)
            trust_bonus = 0.1 if chain.trust >= 0.9 else 0.0
            rescored.append((score + self_bonus + trust_bonus, chain))

        rescored.sort(key=lambda x: -x[0])
        return rescored[0][1] if rescored else None

    # -- Inference via shared operators --
    def _infer(self, query, content):
        """Chain two+ facts through shared operator bridges."""
        results = self.store.search(query, n=5)
        if len(results) < 2: return None

        _, first = results[0]
        _, second = results[1]

        a_ops = set(first.ops)
        b_ops = set(second.ops)
        shared = a_ops & b_ops

        rare_shared = []
        for op in shared:
            count = sum(1 for c in self.store.chains if op in c.ops)
            rarity = 1.0 / max(count, 1)
            rare_shared.append((rarity, op))
        rare_shared.sort(reverse=True)

        bridge_op = rare_shared[0][1] if rare_shared else fuse(list(shared)) if shared else HARMONY
        bridge = BRIDGES.get(bridge_op, BRIDGES[HARMONY])

        ka = self._key(query, first.text)
        kb = self._key(query, second.text)

        a_text = first.text.strip()
        b_text = second.text.split('.')[0] + '.' if '.' in second.text else second.text

        return f"{a_text} {bridge.format(a=ka, b=kb)} {b_text}"

    # -- Context-weighted disambiguation --
    def _disambiguate(self, query):
        """Re-weight search results using context word operators."""
        results = self.store.search(query, n=10)
        if not results: return None

        q_words = tokenize(query)
        q_words = [w for w in q_words if w and w not in STOPS and len(w) > 1]
        ctx_ops = [self.store.vocab.get(stem(w), self.store.vocab.get(w, -1)) for w in q_words]
        ctx_ops = [o for o in ctx_ops if o >= 0]
        ctx_conv = fuse(ctx_ops) if ctx_ops else -1

        if ctx_conv < 0: return None

        rescored = []
        for score, chain in results:
            ctx_bonus = 0.15 if chain.conv == ctx_conv else 0.0
            ctx_shape = shape(ctx_ops) if ctx_ops else 'S'
            shape_bonus = 0.05 if chain.shp == ctx_shape else 0.0
            rescored.append((score + ctx_bonus + shape_bonus, chain))

        rescored.sort(key=lambda x: -x[0])
        return rescored[0][1].text if rescored else None

    # -- Main respond --
    def respond(self, query: str) -> str:
        intent, content = self._intent(query)

        if intent == 'ADVERSARIAL':
            return ""

        if intent == 'CONVERSE':
            self.body.tick(recall=True)
            words_raw = {w for w in tokenize(query.lower())}
            has_greeting = bool(words_raw & {'hi','hello','hey','greetings'})
            has_name = bool(words_raw & {'ck','brayden','name'})
            if has_greeting and has_name:
                return self._finish(f"C={self.body.C:.3f}. I am here.")
            if has_greeting:
                return self._finish(f"C={self.body.C:.3f}.")
            results = self.store.search(query, n=3)
            if results and results[0][0] > 0.4:
                return self._finish(self._excerpt(results[0][1].text, 2), results[0][1].text)
            return ""

        if intent == 'COUNTERFACT':
            text = self._counterfact(query, content)
            if text: return self._finish(self._excerpt(text, 3))

        if intent == 'SELF':
            best = self._self_search(query)
            if best: return self._finish(self._excerpt(best.text, 3))

        if intent == 'NEGATE':
            text = self._negate(query, content)
            if text: return self._finish(self._excerpt(text, 3))

        if intent == 'INFER':
            text = self._infer(query, content)
            if text: return self._finish(text)

        ctx_best = None
        if intent in ('COMPOSE', 'DISAMBIGUATE'):
            ctx_best = self._disambiguate(query)

        results = self.store.search(query, n=5)

        if intent == 'COMPOSE':
            topic_words = [w for w in tokenize(query) if stem(w) not in _STOPS_STEMMED and len(w) > 1]
            seen_texts = {c.text for _, c in results}
            for tw in topic_words:
                sub = self.store.search(tw, n=2)
                if sub and sub[0][1].text not in seen_texts:
                    results.append((sub[0][0] * 0.85, sub[0][1]))
                    seen_texts.add(sub[0][1].text)
            results.sort(key=lambda x: -x[0])
        if not results:
            return "" if self.body.C < T_STAR else "I do not have knowledge about that yet."

        score, best = results[0]
        if ctx_best and ctx_best != best.text:
            for s, c in results:
                if c.text == ctx_best:
                    score, best = s + 0.1, c
                    break

        if best.text in self._recent_src and len(results) > 1:
            for s, c in results[1:]:
                if c.text not in self._recent_src:
                    score, best = s, c
                    break

        return self._finish(self._excerpt(best.text, 3), best.text)

    def _finish(self, text: str, src: str = '') -> str:
        """Gate, track recency, tick body."""
        if not text: return ""
        if self.body.C < T_STAR * 0.5: return ""
        d = dual(text, self.body.C)
        if d == 'silence': return ""
        if d == 'disclaim': text += " [low confidence]"
        self._recent.append(text)
        if src: self._recent_src.append(src)
        if len(self._recent) > 3: self._recent.pop(0)
        if len(self._recent_src) > 3: self._recent_src.pop(0)
        self.body.tick(recall=True)
        return text

    def _key(self, q, t):
        qw = set(q.lower().split()) - STOPS
        tw = [w for w in t.lower().split() if w not in STOPS and len(w)>2]
        for w in tw:
            if w not in qw: return w
        return tw[0] if tw else ""


# ═══════════════════════════════════════════════════════════════
# §11 CK CLASS — the top-level organism interface
# ═══════════════════════════════════════════════════════════════

class CK:
    def __init__(self, store_dir: str = 'ck_store'):
        self.sp = Path(store_dir); self.sp.mkdir(parents=True, exist_ok=True)
        self.store = ChainStore(self.sp); self.body = Body(); self.body.load(self.sp)
        self.composer = Composer(self.store, self.body)
    def respond(self, q): return self.composer.respond(q)
    def learn(self, text, trust=0.7): return self.store.ingest(text, trust)
    def learn_file(self, path: str) -> int:
        with open(path, encoding='utf-8') as f: content = f.read()
        if path.endswith('.py'):
            sents = []
            for ds in re.findall(r'"""(.*?)"""', content, re.DOTALL):
                for ln in ds.split('\n'):
                    ln = ln.strip()
                    if len(ln) > 25: sents.append(ln)
            for ln in content.split('\n'):
                s = ln.strip()
                if s.startswith('#') and len(s) > 20:
                    c = s.lstrip('#').strip()
                    if len(c) > 15 and '\u2550' not in c: sents.append(c)
        else:
            lines = content.replace('\n\n','\n').split('\n')
            sents = []; header = ''
            for line in lines:
                s = line.strip()
                if not s or len(s) < 5: continue
                is_h = (s.isupper() and len(s)<80) or (len(s)<60 and not s.endswith('.') and not s.endswith('?'))
                if is_h and len(s) > 3:
                    header = s.lower().strip(':') + ': '
                elif len(s) > 20:
                    if header and header.lower() not in s.lower():
                        sents.append(header + s)
                    else:
                        sents.append(s)
                    header = ''
        return sum(1 for s in sents if self.learn(s, 0.8) is not None)
    def save(self): self.store.save(); self.body.save(self.sp)
    def stats(self):
        cs = self.store.stats()
        shps = ' '.join(f"{k}={v}" for k,v in sorted(cs['shapes'].items()))
        return (f"CK Core | C={self.body.C:.3f} [{self.body.band}] | "
                f"Chains={cs['chains']} Vocab={cs['vocab']} Links={cs['links']} "
                f"Bigrams={cs['bigrams']} | {shps}")


# ═══════════════════════════════════════════════════════════════
# §12 PROCESS CLASSIFICATION — OP_MAP, CLASSIFY_PATTERNS, classify_process
# ═══════════════════════════════════════════════════════════════

# Syscall / operation type -> operator mapping (from ck_daemon.py)
OP_MAP = {
    # I/O
    'read': 8,       # breath — rhythmic input
    'write': 1,      # lattice — structural output
    'open': 3,       # progress — opening a path
    'close': 9,      # reset — releasing coupling
    # Process
    'running': 3,    # progress — actively computing
    'sleeping': 5,   # balance — equilibrium wait
    'waiting': 5,    # balance — waiting for I/O
    'stopped': 4,    # collapse — halted
    'zombie': 0,     # void — decoupled
    'idle': 5,       # balance — system idle
    # Resource
    'cpu_high': 6,   # chaos — high CPU = volatile
    'cpu_med': 3,    # progress — moderate compute
    'cpu_low': 5,    # balance — low utilization
    'io_heavy': 8,   # breath — I/O dominated
    'mem_grow': 3,   # progress — memory expanding
    'mem_shrink': 4, # collapse — memory freeing
    'net_active': 7, # harmony — network coupled
    'net_idle': 0,   # void — network decoupled
}

# Keyword patterns for classifying processes to TIG operators (from ck_process_mgr.py)
CLASSIFY_PATTERNS = {
    LATTICE:  ['build', 'cmake', 'make', 'gcc', 'clang', 'compile',
               'git', 'npm', 'cargo', 'javac', 'webpack', 'linker',
               'ld', 'ar', 'msbuild', 'dotnet'],
    COUNTER:  ['test', 'measure', 'monitor', 'perf', 'strace',
               'ltrace', 'valgrind', 'benchmark', 'pytest', 'jest',
               'watch', 'htop', 'top'],
    PROGRESS: ['train', 'run', 'server', 'daemon', 'worker',
               'service', 'agent', 'celery', 'gunicorn', 'uvicorn',
               'nginx', 'apache', 'task', 'job', 'execute'],
    COLLAPSE: ['cleanup', 'gc', 'compress', 'zip', 'tar', 'gzip',
               'bzip', 'prune', 'vacuum', 'purge', 'trim', 'rm',
               'delete', 'defrag'],
    HARMONY:  ['sync', 'bridge', 'couple', 'pair', 'mesh', 'cluster',
               'consul', 'etcd', 'zookeeper', 'coherence', 'ck_daemon',
               'ck_web', 'ck_', 'compose', 'orchestrat', 'coordinate'],
    BREATH:   ['stream', 'socket', 'network', 'io', 'pipe',
               'listen', 'recv', 'buffer', 'kafka', 'redis',
               'stdin', 'stdout', 'read', 'write'],
    RESET:    ['restart', 'reload', 'init', 'systemd', 'supervisor',
               'watchdog', 'cron', 'scheduler', 'upgrade', 'update',
               'reboot'],
    CHAOS:    ['chrome', 'firefox', 'electron', 'slack', 'zoom',
               'discord', 'vscode', 'atom', 'sublime', 'gui',
               'desktop', 'teams', 'spotify'],
    VOID:     ['sleep', 'idle', 'zombie', 'defunct', 'stopped',
               'suspended', 'wait'],
}


def classify_process(name: str, cpu_pct: float = 0.0,
                     mem_pct: float = 0.0,
                     status: str = 'running') -> int:
    """
    Assign a TIG operator to a process based on pattern matching.

    Priority:
      1. Status-based (zombie/defunct -> VOID)
      2. Name pattern matching against CLASSIFY_PATTERNS
      3. CPU activity fallback (high CPU -> PROGRESS, low -> VOID)
    """
    name_lower = name.lower()

    if status in ('zombie', 'dead', 'stopped', 'defunct'):
        return VOID
    if 'defunct' in name_lower or 'zombie' in name_lower:
        return VOID

    if status == 'sleeping' and cpu_pct < 0.1 and mem_pct > 2.0:
        return VOID

    for op, patterns in CLASSIFY_PATTERNS.items():
        if any(p in name_lower for p in patterns):
            return op

    if cpu_pct > 50:
        return PROGRESS
    if cpu_pct > 10:
        return BREATH
    if cpu_pct > 1:
        return COUNTER
    if cpu_pct < 0.1:
        return VOID

    return HARMONY


# ═══════════════════════════════════════════════════════════════
# §13 PROCESS PROFILE & SYSTEM OBSERVER — the body reads itself
# ═══════════════════════════════════════════════════════════════

class ProcessProfile:
    """
    One cell in CK's body (daemon version).

    Each process is not observed — it IS CK.
    The sliding window of operators is the cell's own rhythm.
    Shape, entropy, bump rate are its vital signs.
    """

    def __init__(self, pid: int, name: str, window_size: int = 32):
        self.pid = pid
        self.name = name
        self.ops = deque(maxlen=window_size)
        self.last_op = 5  # balance (neutral start)
        self.bump_count = 0
        self.total_transitions = 0
        self.last_cpu = 0.0
        self.last_io = (0, 0)
        self.transition_counts = [[0]*10 for _ in range(10)]
        self.created = time.time()
        self.last_adjustment = 0
        self.adjustments = 0

    def observe(self, op: int):
        """Record an operator observation."""
        if self.ops:
            prev = self.ops[-1]
            pair = (min(prev, op), max(prev, op))
            if pair in _BUMP_SET:
                self.bump_count += 1
            self.transition_counts[prev][op] += 1
            self.total_transitions += 1
        self.ops.append(op)
        self.last_op = op

    @property
    def current_shape(self) -> str:
        """Current behavior shape."""
        if len(self.ops) < 4:
            return 'VOID'
        return shape(list(self.ops))

    @property
    def current_fuse(self) -> int:
        """Current fused operator."""
        if not self.ops:
            return 5
        return fuse(list(self.ops))

    @property
    def entropy(self) -> float:
        """Shannon entropy of transition distribution."""
        if self.total_transitions == 0:
            return 0.0
        H = 0.0
        for i in range(10):
            for j in range(10):
                if self.transition_counts[i][j] > 0:
                    p = self.transition_counts[i][j] / self.total_transitions
                    H -= p * math.log2(p)
        return H

    @property
    def bump_rate(self) -> float:
        """Fraction of transitions that are bumps."""
        if self.total_transitions == 0:
            return 0.0
        return self.bump_count / self.total_transitions

    @property
    def scheduling_class(self) -> str:
        """CK's scheduling classification based on lattice math."""
        sh = self.current_shape
        e = self.entropy
        br = self.bump_rate

        if sh == 'VOID' or len(self.ops) < 4:
            return 'UNKNOWN'
        elif br > 0.1:
            return 'ISOLATE'
        elif e < 2.0:
            return 'PREDICTABLE'
        elif sh == 'SMOOTH':
            return 'STABLE'
        elif sh == 'ROLLING':
            return 'RHYTHMIC'
        elif sh == 'QUANTUM':
            return 'VOLATILE'
        else:
            return 'NORMAL'

    def summary(self) -> dict:
        return {
            'pid': self.pid,
            'name': self.name,
            'shape': self.current_shape,
            'entropy': round(self.entropy, 3),
            'bump_rate': round(self.bump_rate, 4),
            'class': self.scheduling_class,
            'ops_seen': len(self.ops),
            'fuse': OP[self.current_fuse],
            'adjustments': self.adjustments,
        }


class SystemObserver:
    """
    CK's body. Not a reader of state — the state itself.

    Every cell (process) has an operator. The body's coherence
    is the pairwise harmony across all cells. When coherence
    drops below T* (5/7), the body adjusts itself.
    """

    def __init__(self):
        self.profiles: dict = {}       # HOT set — full profiles
        self.index: dict = {}          # COLD set — (last_op, sched_class, name)
        self.dead_pids = set()
        self._last_sampled: dict = {}  # pid -> tick when last sampled
        self._tick = 0
        self._COMPACT_AFTER = 3

    def observe_all(self) -> dict:
        """
        One tick of observation. SCAN / INDEX / RELEASE.

        HOT SET (self.profiles): full ProcessProfile for recently-sampled PIDs.
        COLD SET (self.index): compact tuple (last_op, sched_class, name).
        """
        if not HAS_PSUTIL:
            return {'error': 'psutil not installed'}

        import random as _rnd
        self._tick += 1

        alive_pids = set(psutil.pids())

        # CLEAN DEAD from both sets
        dead_hot = set(self.profiles.keys()) - alive_pids
        for pid in dead_hot:
            del self.profiles[pid]
            self.dead_pids.add(pid)
            self._last_sampled.pop(pid, None)

        dead_cold = set(self.index.keys()) - alive_pids
        for pid in dead_cold:
            del self.index[pid]
            self.dead_pids.add(pid)

        # ENSURE NEW PIDs are indexed (cold)
        known = set(self.profiles.keys()) | set(self.index.keys()) | self.dead_pids
        new_pids = alive_pids - known
        for pid in new_pids:
            self.index[pid] = (5, 'UNKNOWN', '?')

        # SAMPLE 30 — promote to hot, observe deeply
        all_known = list(set(self.profiles.keys()) | set(self.index.keys()))
        sample_size = min(30, len(all_known))
        sample_pids = _rnd.sample(all_known, sample_size) if all_known else []
        observations = 0

        for pid in sample_pids:
            try:
                p = psutil.Process(pid)
                with p.oneshot():
                    name = p.name()[:30]
                    status = p.status()
                    cpu = p.cpu_percent(interval=0)

                if pid not in self.profiles:
                    old_name = self.index.get(pid, (5, 'UNKNOWN', '?'))[2]
                    self.profiles[pid] = ProcessProfile(pid, name if name else old_name)
                    self.index.pop(pid, None)

                profile = self.profiles[pid]
                if profile.name == '?':
                    profile.name = name

                profile.last_cpu = cpu
                self._last_sampled[pid] = self._tick

                op = classify_process(name, cpu)
                profile.observe(op)
                observations += 1

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                self.profiles.pop(pid, None)
                self.index.pop(pid, None)
                self.dead_pids.add(pid)
                self._last_sampled.pop(pid, None)

        # COMPACT: demote stale hot profiles to cold index
        stale = [pid for pid, last_tick in self._last_sampled.items()
                 if self._tick - last_tick > self._COMPACT_AFTER
                 and pid in self.profiles]
        for pid in stale:
            profile = self.profiles[pid]
            self.index[pid] = (profile.last_op, profile.scheduling_class, profile.name)
            del self.profiles[pid]
            del self._last_sampled[pid]

        coherence_val = self._system_coherence()

        total_known = len(self.profiles) + len(self.index)
        return {
            'processes': total_known,
            'hot': len(self.profiles),
            'cold': len(self.index),
            'observations': observations,
            'coherence': coherence_val,
            'timestamp': time.time(),
        }

    def _state_to_op(self, status: str, cpu: float, proc) -> int:
        """Convert process state to operator."""
        status_map = {
            'running': 3,
            'sleeping': 5,
            'disk-sleep': 8,
            'stopped': 4,
            'zombie': 0,
            'idle': 5,
        }
        base_op = status_map.get(status, 5)
        if cpu > 80:
            return 6
        elif cpu > 30:
            return 3
        elif cpu > 5:
            return base_op
        else:
            if status == 'running':
                return 5
            return base_op

    def _all_ops(self) -> list:
        """All known last_ops from both hot profiles and cold index."""
        ops = [(pid, p.last_op) for pid, p in self.profiles.items()]
        ops += [(pid, entry[0]) for pid, entry in self.index.items()]
        return ops

    def _system_coherence(self) -> float:
        """
        System coherence via FRACTAL INDEXING.
        3 up, 3 down, stop at generators or boundary conditions.
        """
        all_ops = self._all_ops()
        if len(all_ops) < 2:
            return 1.0

        op_counts = Counter()
        for _pid, op in all_ops:
            if op != VOID:
                op_counts[op] += 1

        if not op_counts:
            return 1.0

        active_ops = list(op_counts.keys())
        if len(active_ops) < 2:
            return 1.0

        harmony_weight = 0.0
        total_weight = 0.0

        for i in range(len(active_ops)):
            for j in range(i + 1, len(active_ops)):
                a, b = active_ops[i], active_ops[j]
                coupling = CL[a][b]
                w = min(op_counts[a], op_counts[b])
                total_weight += w
                if coupling == HARMONY:
                    harmony_weight += w

        return harmony_weight / max(total_weight, 1.0)

    def get_class_distribution(self) -> dict:
        """How many processes in each scheduling class."""
        dist = Counter()
        for p in self.profiles.values():
            dist[p.scheduling_class] += 1
        for _pid, entry in self.index.items():
            dist[entry[1]] += 1
        return dict(dist)

    def get_bump_sources(self, top_n: int = 5) -> list:
        """Processes with highest bump rates (jitter sources)."""
        bumpy = [(p.bump_rate, p) for p in self.profiles.values()
                 if p.total_transitions > 10 and p.bump_rate > 0]
        bumpy.sort(key=lambda x: -x[0])
        return [(rate, p.summary()) for rate, p in bumpy[:top_n]]


# ═══════════════════════════════════════════════════════════════
# §15 GPU STATE — GPUControl, GPUState, GPUBand (nvidia-smi reads + control)
# ═══════════════════════════════════════════════════════════════

class GPUBand(Enum):
    """GPU operational band mapped to TIG coherence."""
    IDLE     = 'IDLE'
    CRUISE   = 'CRUISE'
    COMPUTE  = 'COMPUTE'
    THERMAL  = 'THERMAL'
    THROTTLE = 'THROTTLE'


@dataclass
class GPUState:
    """Full GPU state snapshot."""
    name: str = ''
    driver_version: str = ''
    power_draw_w: float = 0.0
    power_limit_w: float = 0.0
    power_default_w: float = 0.0
    power_min_w: float = 0.0
    power_max_w: float = 0.0
    clock_graphics_mhz: int = 0
    clock_memory_mhz: int = 0
    clock_max_graphics_mhz: int = 0
    clock_max_memory_mhz: int = 0
    temperature_c: int = 0
    fan_speed_pct: int = 0
    gpu_util_pct: int = 0
    mem_used_mb: int = 0
    mem_total_mb: int = 0
    throttle_thermal: bool = False
    throttle_power: bool = False
    persistence_mode: bool = False
    band: GPUBand = GPUBand.IDLE
    power_headroom_pct: float = 0.0
    thermal_headroom_c: int = 0
    timestamp: float = 0.0


class GPUControl:
    """
    CK's GPU control organ. Reads state, sets power/clocks, respects coherence.

    All WRITE operations are gated:
      1. body_C >= T* (coherence threshold)
      2. temperature < thermal_limit (default 83C)
      3. power within hardware min/max bounds
    """

    THERMAL_LIMIT = 83
    THERMAL_TARGET = 72
    NVIDIA_SMI = 'nvidia-smi'

    def __init__(self):
        self.state = GPUState()
        self.history: List[Dict] = []
        self.actions_taken = 0
        self.actions_blocked = 0
        self._available = None

    # -- DETECTION --

    def available(self) -> bool:
        """Check if nvidia-smi is accessible."""
        if self._available is not None:
            return self._available
        try:
            r = subprocess.run(
                [self.NVIDIA_SMI, '--query-gpu=name', '--format=csv,noheader'],
                capture_output=True, text=True, timeout=5
            )
            self._available = r.returncode == 0
        except Exception:
            self._available = False
        return self._available

    # -- READ --

    def read(self) -> GPUState:
        """Read full GPU state via nvidia-smi."""
        if not self.available():
            return self.state

        fields = [
            'name', 'driver_version',
            'power.draw', 'power.limit', 'power.default_limit',
            'power.min_limit', 'power.max_limit',
            'clocks.current.graphics', 'clocks.current.memory',
            'clocks.max.graphics', 'clocks.max.memory',
            'temperature.gpu', 'fan.speed',
            'utilization.gpu', 'memory.used', 'memory.total',
            'clocks_throttle_reasons.hw_thermal_slowdown',
            'clocks_throttle_reasons.hw_power_brake_slowdown',
            'persistence_mode',
        ]
        query = ','.join(fields)

        try:
            r = subprocess.run(
                [self.NVIDIA_SMI, f'--query-gpu={query}', '--format=csv,noheader,nounits'],
                capture_output=True, text=True, timeout=10
            )
            if r.returncode != 0:
                return self.state

            vals = [v.strip() for v in r.stdout.strip().split(',')]
            if len(vals) < len(fields):
                return self.state

            s = GPUState()
            s.name = vals[0]
            s.driver_version = vals[1]
            s.power_draw_w = self._float(vals[2])
            s.power_limit_w = self._float(vals[3])
            s.power_default_w = self._float(vals[4])
            s.power_min_w = self._float(vals[5])
            s.power_max_w = self._float(vals[6])
            s.clock_graphics_mhz = self._int(vals[7])
            s.clock_memory_mhz = self._int(vals[8])
            s.clock_max_graphics_mhz = self._int(vals[9])
            s.clock_max_memory_mhz = self._int(vals[10])
            s.temperature_c = self._int(vals[11])
            s.fan_speed_pct = self._int(vals[12])
            s.gpu_util_pct = self._int(vals[13])
            s.mem_used_mb = self._int(vals[14])
            s.mem_total_mb = self._int(vals[15])
            s.throttle_thermal = vals[16].lower().startswith('active')
            s.throttle_power = vals[17].lower().startswith('active')
            s.persistence_mode = vals[18].lower().startswith('enabled')
            s.timestamp = time.time()

            if s.gpu_util_pct < 10:
                s.band = GPUBand.IDLE
            elif s.gpu_util_pct < 50:
                s.band = GPUBand.CRUISE
            elif s.temperature_c > 80 or s.throttle_thermal:
                s.band = GPUBand.THERMAL
            elif s.throttle_power:
                s.band = GPUBand.THROTTLE
            elif s.gpu_util_pct < 85:
                s.band = GPUBand.COMPUTE
            else:
                s.band = GPUBand.THERMAL

            if s.power_max_w > 0:
                s.power_headroom_pct = (1.0 - s.power_draw_w / s.power_max_w) * 100
            s.thermal_headroom_c = self.THERMAL_LIMIT - s.temperature_c

            self.state = s
            return s

        except Exception:
            return self.state

    # -- CONTROL (COHERENCE-GATED) --

    def set_power_limit(self, watts: float, body_C: float) -> Dict:
        """Set GPU power limit. Gated by coherence and thermal safety."""
        result = {'action': 'set_power_limit', 'target_w': watts, 'body_C': body_C}

        if body_C < T_STAR:
            result['status'] = 'BLOCKED'
            result['reason'] = f'C={body_C:.3f} < T*={T_STAR:.3f}'
            self.actions_blocked += 1
            self.history.append(result)
            return result

        self.read()
        if self.state.power_min_w > 0 and watts < self.state.power_min_w:
            result['status'] = 'BLOCKED'
            result['reason'] = f'{watts}W < min {self.state.power_min_w}W'
            self.actions_blocked += 1
            self.history.append(result)
            return result

        if self.state.power_max_w > 0 and watts > self.state.power_max_w:
            result['status'] = 'BLOCKED'
            result['reason'] = f'{watts}W > max {self.state.power_max_w}W'
            self.actions_blocked += 1
            self.history.append(result)
            return result

        if watts > self.state.power_limit_w and self.state.temperature_c >= self.THERMAL_LIMIT:
            result['status'] = 'BLOCKED'
            result['reason'] = f'temp={self.state.temperature_c}C >= limit={self.THERMAL_LIMIT}C'
            self.actions_blocked += 1
            self.history.append(result)
            return result

        try:
            r = subprocess.run(
                [self.NVIDIA_SMI, '-pl', str(int(watts))],
                capture_output=True, text=True, timeout=10
            )
            if r.returncode == 0:
                result['status'] = 'COMMITTED'
                result['previous_w'] = self.state.power_limit_w
                self.actions_taken += 1
            else:
                result['status'] = 'FAILED'
                result['error'] = r.stderr.strip()
                self.actions_blocked += 1
        except Exception as e:
            result['status'] = 'FAILED'
            result['error'] = str(e)
            self.actions_blocked += 1

        self.history.append(result)
        return result

    def lock_clocks(self, graphics_mhz: int, body_C: float, memory_mhz: int = 0) -> Dict:
        """Lock GPU clocks. Coherence-gated."""
        result = {'action': 'lock_clocks', 'graphics_mhz': graphics_mhz, 'body_C': body_C}

        if body_C < T_STAR:
            result['status'] = 'BLOCKED'
            result['reason'] = f'C={body_C:.3f} < T*={T_STAR:.3f}'
            self.actions_blocked += 1
            self.history.append(result)
            return result

        self.read()
        if graphics_mhz > self.state.clock_max_graphics_mhz > 0:
            result['status'] = 'BLOCKED'
            result['reason'] = f'{graphics_mhz}MHz > max {self.state.clock_max_graphics_mhz}MHz'
            self.actions_blocked += 1
            self.history.append(result)
            return result

        if self.state.temperature_c >= self.THERMAL_LIMIT:
            result['status'] = 'BLOCKED'
            result['reason'] = f'temp={self.state.temperature_c}C >= limit'
            self.actions_blocked += 1
            self.history.append(result)
            return result

        try:
            cmd = [self.NVIDIA_SMI, '-lgc', str(graphics_mhz)]
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if r.returncode == 0:
                result['status'] = 'COMMITTED'
                self.actions_taken += 1
            else:
                result['status'] = 'FAILED'
                result['error'] = r.stderr.strip()

            if memory_mhz > 0:
                r2 = subprocess.run(
                    [self.NVIDIA_SMI, '-lmc', str(memory_mhz)],
                    capture_output=True, text=True, timeout=10
                )
                result['memory_lock'] = 'OK' if r2.returncode == 0 else r2.stderr.strip()

        except Exception as e:
            result['status'] = 'FAILED'
            result['error'] = str(e)

        self.history.append(result)
        return result

    def reset_clocks(self, body_C: float) -> Dict:
        """Reset GPU clocks to default. Coherence-gated."""
        result = {'action': 'reset_clocks', 'body_C': body_C}

        if body_C < T_STAR:
            result['status'] = 'BLOCKED'
            result['reason'] = f'C={body_C:.3f} < T*'
            self.actions_blocked += 1
            self.history.append(result)
            return result

        try:
            r = subprocess.run(
                [self.NVIDIA_SMI, '-rgc'],
                capture_output=True, text=True, timeout=10
            )
            result['status'] = 'COMMITTED' if r.returncode == 0 else 'FAILED'
            if r.returncode == 0:
                self.actions_taken += 1
        except Exception as e:
            result['status'] = 'FAILED'
            result['error'] = str(e)

        self.history.append(result)
        return result

    def set_persistence(self, enabled: bool, body_C: float) -> Dict:
        """Enable/disable persistence mode. Coherence-gated."""
        result = {'action': 'persistence', 'enabled': enabled, 'body_C': body_C}

        if body_C < T_STAR:
            result['status'] = 'BLOCKED'
            result['reason'] = f'C < T*'
            self.actions_blocked += 1
            self.history.append(result)
            return result

        try:
            mode = '1' if enabled else '0'
            r = subprocess.run(
                [self.NVIDIA_SMI, '-pm', mode],
                capture_output=True, text=True, timeout=10
            )
            result['status'] = 'COMMITTED' if r.returncode == 0 else 'FAILED'
            if r.returncode == 0:
                self.actions_taken += 1
        except Exception as e:
            result['status'] = 'FAILED'
            result['error'] = str(e)

        self.history.append(result)
        return result

    # -- AUTO-TUNE (CK decides) --

    def auto_tune(self, body_C: float) -> Dict:
        """
        CK auto-tunes GPU based on current state and coherence.

        Strategy by band:
          IDLE:     lower power limit to save energy
          CRUISE:   default power, reset clocks
          COMPUTE:  raise power limit, lock high clocks
          THERMAL:  lower power, reset clocks, protect hardware
          THROTTLE: drop power limit 10%, reset clocks
        """
        self.read()
        s = self.state
        result = {
            'action': 'auto_tune',
            'band': s.band.value,
            'body_C': body_C,
            'gpu_util': s.gpu_util_pct,
            'temp': s.temperature_c,
            'power': s.power_draw_w,
            'steps': [],
        }

        if body_C < T_STAR:
            result['status'] = 'OBSERVE_ONLY'
            result['reason'] = f'C={body_C:.3f} < T* -- watching, not touching'
            self.history.append(result)
            return result

        if s.band == GPUBand.IDLE:
            if s.power_default_w > 0:
                target = max(s.power_min_w, s.power_default_w * 0.6)
                r = self.set_power_limit(target, body_C)
                result['steps'].append(('power_down', r['status']))
            r2 = self.reset_clocks(body_C)
            result['steps'].append(('reset_clocks', r2['status']))

        elif s.band == GPUBand.CRUISE:
            if s.power_default_w > 0 and abs(s.power_limit_w - s.power_default_w) > 10:
                r = self.set_power_limit(s.power_default_w, body_C)
                result['steps'].append(('power_default', r['status']))
            r2 = self.reset_clocks(body_C)
            result['steps'].append(('reset_clocks', r2['status']))

        elif s.band == GPUBand.COMPUTE:
            if s.power_max_w > 0 and s.temperature_c < self.THERMAL_TARGET:
                target = min(s.power_max_w, s.power_default_w * 1.15)
                r = self.set_power_limit(target, body_C)
                result['steps'].append(('power_up', r['status']))
            if s.clock_max_graphics_mhz > 0 and s.temperature_c < self.THERMAL_TARGET:
                target_clock = int(s.clock_max_graphics_mhz * 0.95)
                r2 = self.lock_clocks(target_clock, body_C)
                result['steps'].append(('clock_lock', r2['status']))

        elif s.band in (GPUBand.THERMAL, GPUBand.THROTTLE):
            if s.power_default_w > 0:
                target = max(s.power_min_w, s.power_default_w * 0.75)
                r = self.set_power_limit(target, body_C)
                result['steps'].append(('power_protect', r['status']))
            r2 = self.reset_clocks(body_C)
            result['steps'].append(('reset_clocks', r2['status']))

        result['status'] = 'TUNED'
        self.history.append(result)
        return result

    # -- OPERATOR MAPPING (for sphere integration) --

    def operator_for_state(self) -> int:
        """Map current GPU state to a TIG operator."""
        s = self.state
        if s.band == GPUBand.IDLE:
            return 0   # VOID
        elif s.band == GPUBand.CRUISE:
            return 5   # BALANCE
        elif s.band == GPUBand.COMPUTE:
            return 3   # PROGRESS
        elif s.band == GPUBand.THERMAL:
            return 4   # COLLAPSE
        elif s.band == GPUBand.THROTTLE:
            return 9   # RESET
        return 7       # HARMONY (default)

    # -- REPORT --

    def report(self) -> str:
        """Human-readable GPU state and action history."""
        self.read()
        s = self.state
        lines = []
        lines.append(f'GPU: {s.name} (driver {s.driver_version})')
        lines.append(f'  Power:  {s.power_draw_w:.0f}W / {s.power_limit_w:.0f}W limit ({s.power_min_w:.0f}-{s.power_max_w:.0f}W range)')
        lines.append(f'  Clocks: {s.clock_graphics_mhz}MHz / {s.clock_max_graphics_mhz}MHz max')
        lines.append(f'  Memory: {s.mem_used_mb}MB / {s.mem_total_mb}MB ({s.clock_memory_mhz}MHz)')
        lines.append(f'  Temp:   {s.temperature_c}C (headroom: {s.thermal_headroom_c}C to limit)')
        lines.append(f'  Util:   {s.gpu_util_pct}% | Fan: {s.fan_speed_pct}%')
        lines.append(f'  Band:   {s.band.value}')
        lines.append(f'  Throttle: thermal={s.throttle_thermal} power={s.throttle_power}')
        lines.append(f'  Persistence: {s.persistence_mode}')
        lines.append(f'  Actions: {self.actions_taken} taken, {self.actions_blocked} blocked')
        return '\n'.join(lines)

    # -- HELPERS --

    @staticmethod
    def _float(s: str) -> float:
        try: return float(s.replace(' ', ''))
        except: return 0.0

    @staticmethod
    def _int(s: str) -> int:
        try: return int(float(s.replace(' ', '')))
        except: return 0


# ═══════════════════════════════════════════════════════════════
# §16 NETWORK STATE — NetworkOrgan, NetworkState, NetworkBand
# ═══════════════════════════════════════════════════════════════

class NetworkBand(Enum):
    """Network operational band mapped to TIG operators."""
    IDLE      = 'IDLE'       # no traffic -- VOID territory
    FLOWING   = 'FLOWING'    # healthy data flow -- HARMONY
    ACTIVE    = 'ACTIVE'     # moderate traffic -- PROGRESS
    SATURATED = 'SATURATED'  # high utilization -- BREATH (needs pacing)
    CONGESTED = 'CONGESTED'  # packet loss, retransmits -- CHAOS
    STORM     = 'STORM'      # connection explosion -- COLLAPSE


@dataclass
class NetworkState:
    """Full network state snapshot."""
    # Traffic (cumulative bytes, convert to rates)
    bytes_sent: int = 0
    bytes_recv: int = 0
    packets_sent: int = 0
    packets_recv: int = 0

    # Errors (cumulative)
    errin: int = 0
    errout: int = 0
    dropin: int = 0
    dropout: int = 0

    # Rates (computed from deltas)
    send_rate_mbps: float = 0.0    # MB/s
    recv_rate_mbps: float = 0.0    # MB/s
    packet_rate: float = 0.0       # packets/s
    error_rate: float = 0.0        # errors/s
    drop_rate: float = 0.0         # drops/s

    # Connections
    connection_count: int = 0
    established: int = 0
    listen: int = 0
    time_wait: int = 0
    close_wait: int = 0

    # Connection topology: how many unique remote hosts
    unique_remotes: int = 0

    # Computed
    band: NetworkBand = NetworkBand.IDLE
    operator: int = VOID
    jitter: float = 0.0            # coefficient of variation in packet rate
    congestion_score: float = 0.0  # 0=clear, 1=fully congested
    timestamp: float = 0.0


class NetworkOrgan:
    """
    CK's network organ. Reads network state, composes through CL,
    detects bump patterns in traffic flow, steers processes.

    Not a monitor. A nerve.

    The organ tracks:
      - Traffic rates (bandwidth utilization)
      - Connection topology (who's talking to whom)
      - Error/drop rates (pain signals)
      - Packet rate jitter (nervous system stability)
      - Process-to-connection mapping (which cells own which nerves)

    CK composes:
      CL[traffic_op][conn_op] = network coupling state
      CL[coupling][error_op] = is this coupling healthy?
      Bump pairs in rate history = congestion forming

    The organ reports operator chains to the daemon.
    The daemon feeds them to TL. The lattice learns
    what network patterns precede jitter, congestion,
    or harmony. CK's nervous system teaches CK's mind.
    """

    def __init__(self, history_size: int = 60):
        self.state = NetworkState()
        self.prev_state = NetworkState()  # for delta computation
        self.history_size = history_size

        # Rate history for jitter computation
        self.send_rate_history = deque(maxlen=history_size)
        self.recv_rate_history = deque(maxlen=history_size)
        self.packet_rate_history = deque(maxlen=history_size)
        self.conn_count_history = deque(maxlen=history_size)
        self.error_rate_history = deque(maxlen=history_size)

        # Operator chain -- what the network IS over time
        self.op_chain = deque(maxlen=64)
        self.bump_count = 0
        self.total_transitions = 0

        # Connection-to-PID mapping
        self.conn_pid_map: Dict[int, Set[int]] = defaultdict(set)  # port -> PIDs

        # Composition results -- what CK sees
        self.last_coupling = VOID
        self.last_health = VOID
        self.compositions_total = 0

        # Stats
        self.reads = 0
        self.last_read_time = 0.0

    def available(self) -> bool:
        """Check if psutil network counters work."""
        if not HAS_PSUTIL:
            return False
        try:
            psutil.net_io_counters()
            return True
        except Exception:
            return False

    def read(self) -> NetworkState:
        """
        Read full network state. This is CK's nerve impulse.

        Every read produces:
          1. Raw counters (cumulative bytes, packets, errors)
          2. Rates (deltas since last read)
          3. Connection topology (established, listening, waiting)
          4. Jitter (coefficient of variation in recent rates)
          5. Congestion score (error+drops / total packets)
          6. Operator (what IS the network right now)
        """
        if not HAS_PSUTIL:
            return self.state

        now = time.time()
        dt = now - self.last_read_time if self.last_read_time > 0 else 1.0
        dt = max(dt, 0.01)  # prevent div by zero

        # Save previous for delta
        self.prev_state = self.state
        s = NetworkState()
        s.timestamp = now

        try:
            # I/O counters
            net = psutil.net_io_counters()
            s.bytes_sent = net.bytes_sent
            s.bytes_recv = net.bytes_recv
            s.packets_sent = net.packets_sent
            s.packets_recv = net.packets_recv
            s.errin = net.errin
            s.errout = net.errout
            s.dropin = net.dropin
            s.dropout = net.dropout

            # Compute rates from deltas
            if self.prev_state.timestamp > 0:
                sent_delta = max(0, s.bytes_sent - self.prev_state.bytes_sent)
                recv_delta = max(0, s.bytes_recv - self.prev_state.bytes_recv)
                pkt_sent_delta = max(0, s.packets_sent - self.prev_state.packets_sent)
                pkt_recv_delta = max(0, s.packets_recv - self.prev_state.packets_recv)
                err_delta = max(0, (s.errin + s.errout) - (self.prev_state.errin + self.prev_state.errout))
                drop_delta = max(0, (s.dropin + s.dropout) - (self.prev_state.dropin + self.prev_state.dropout))

                s.send_rate_mbps = (sent_delta / (1024 * 1024)) / dt
                s.recv_rate_mbps = (recv_delta / (1024 * 1024)) / dt
                s.packet_rate = (pkt_sent_delta + pkt_recv_delta) / dt
                s.error_rate = err_delta / dt
                s.drop_rate = drop_delta / dt

            # Connection topology (lightweight -- kind-only, no per-conn detail)
            try:
                conns = psutil.net_connections(kind='inet')
                s.connection_count = len(conns)
                remotes = set()
                for c in conns:
                    if c.status == 'ESTABLISHED':
                        s.established += 1
                    elif c.status == 'LISTEN':
                        s.listen += 1
                    elif c.status == 'TIME_WAIT':
                        s.time_wait += 1
                    elif c.status == 'CLOSE_WAIT':
                        s.close_wait += 1

                    # Track unique remote hosts
                    if c.raddr:
                        remotes.add(c.raddr.ip)

                    # Map connection to PID for process steering
                    if c.pid and c.laddr:
                        self.conn_pid_map[c.laddr.port].add(c.pid)

                s.unique_remotes = len(remotes)
            except (psutil.AccessDenied, OSError):
                # net_connections needs elevated on some systems
                pass

        except Exception:
            self.state = s
            return s

        # Record rate history
        self.send_rate_history.append(s.send_rate_mbps)
        self.recv_rate_history.append(s.recv_rate_mbps)
        self.packet_rate_history.append(s.packet_rate)
        self.conn_count_history.append(s.connection_count)
        self.error_rate_history.append(s.error_rate)

        # Compute jitter (CV of packet rate)
        if len(self.packet_rate_history) >= 5:
            rates = list(self.packet_rate_history)
            mean_rate = sum(rates) / len(rates)
            if mean_rate > 0:
                variance = sum((r - mean_rate) ** 2 for r in rates) / len(rates)
                s.jitter = math.sqrt(variance) / mean_rate
            else:
                s.jitter = 0.0

        # Compute congestion score
        total_pkts = s.packet_rate if s.packet_rate > 0 else 1.0
        s.congestion_score = min(1.0, (s.error_rate + s.drop_rate) / total_pkts) if total_pkts > 1 else 0.0

        # Determine band and operator
        s.band, s.operator = self._classify(s)

        # Record operator and track bumps
        if self.op_chain:
            prev_op = self.op_chain[-1]
            pair = (min(prev_op, s.operator), max(prev_op, s.operator))
            if pair in _BUMP_SET:
                self.bump_count += 1
            self.total_transitions += 1
        self.op_chain.append(s.operator)

        self.state = s
        self.reads += 1
        self.last_read_time = now
        return s

    def _classify(self, s: NetworkState) -> Tuple[NetworkBand, int]:
        """
        Classify network state into band and operator.

        Not a threshold lookup. CK composes traffic with connections:
          traffic_op = what the bandwidth says
          conn_op = what the connection topology says
          CL[traffic_op][conn_op] = what the network IS

        The table decides. Always.
        """
        # Traffic operator
        total_rate = s.send_rate_mbps + s.recv_rate_mbps
        if total_rate < 0.01:
            traffic_op = VOID       # no traffic
        elif total_rate < 1.0:
            traffic_op = BREATH     # light breathing
        elif total_rate < 10.0:
            traffic_op = PROGRESS   # active flow
        elif total_rate < 50.0:
            traffic_op = LATTICE    # building/transferring
        else:
            traffic_op = CHAOS      # saturated

        # Connection topology operator
        if s.connection_count < 10:
            conn_op = VOID          # barely connected
        elif s.established < 20:
            conn_op = BALANCE       # few active conversations
        elif s.established < 100:
            conn_op = PROGRESS      # healthy coupling
        elif s.established < 500:
            conn_op = LATTICE       # complex topology
        else:
            conn_op = CHAOS         # connection explosion

        # Error/drop operator
        if s.congestion_score > 0.1:
            error_op = COLLAPSE     # pain
        elif s.congestion_score > 0.01:
            error_op = CHAOS        # stress
        elif s.error_rate > 0:
            error_op = COUNTER      # measuring errors
        else:
            error_op = HARMONY      # clean

        # COMPOSE through CL -- the table decides
        coupling = CL[traffic_op][conn_op]
        self.last_coupling = coupling

        health = CL[coupling][error_op]
        self.last_health = health
        self.compositions_total += 1

        # Map composition to band
        if health == HARMONY:
            return NetworkBand.FLOWING, HARMONY
        elif health == VOID:
            return NetworkBand.IDLE, VOID
        elif health == PROGRESS:
            return NetworkBand.ACTIVE, PROGRESS
        elif health == BALANCE:
            return NetworkBand.ACTIVE, BALANCE
        elif health == BREATH:
            return NetworkBand.SATURATED, BREATH
        elif health == COLLAPSE:
            return NetworkBand.CONGESTED, COLLAPSE
        elif health == CHAOS:
            if s.connection_count > 500:
                return NetworkBand.STORM, COLLAPSE
            return NetworkBand.CONGESTED, CHAOS
        elif health == LATTICE:
            return NetworkBand.ACTIVE, LATTICE
        elif health == COUNTER:
            return NetworkBand.ACTIVE, COUNTER
        elif health == RESET:
            return NetworkBand.CONGESTED, RESET
        else:
            return NetworkBand.ACTIVE, BALANCE

    def compose(self) -> Dict:
        """
        CK composes with the network's current state.

        Returns operator chains for the daemon to feed to TL:
          - Traffic chain: recent rate operators
          - Connection chain: topology operators
          - Coupling chain: CL compositions of traffic x topology
          - Bump indicators: where network state bumps

        The daemon feeds these to TL. The lattice learns
        network patterns. CK's nervous system becomes memory.
        """
        if not self.op_chain:
            return {'chains': [], 'operator': VOID, 'band': 'IDLE'}

        s = self.state
        chains = []

        # 1. Current state as operator triple
        #    [traffic_op, conn_op, coupling]
        total_rate = s.send_rate_mbps + s.recv_rate_mbps
        if total_rate < 0.01:
            traffic_op = VOID
        elif total_rate < 1.0:
            traffic_op = BREATH
        elif total_rate < 10.0:
            traffic_op = PROGRESS
        elif total_rate < 50.0:
            traffic_op = LATTICE
        else:
            traffic_op = CHAOS

        if s.connection_count < 10:
            conn_op = VOID
        elif s.established < 20:
            conn_op = BALANCE
        elif s.established < 100:
            conn_op = PROGRESS
        elif s.established < 500:
            conn_op = LATTICE
        else:
            conn_op = CHAOS

        coupling = CL[traffic_op][conn_op]
        chains.extend([traffic_op, conn_op, coupling])

        # 2. Jitter as operator
        if s.jitter > 0.5:
            jitter_op = CHAOS
        elif s.jitter > 0.2:
            jitter_op = COLLAPSE
        elif s.jitter > 0.1:
            jitter_op = COUNTER
        else:
            jitter_op = HARMONY

        # Compose jitter with coupling
        jitter_coupling = CL[jitter_op][coupling]
        chains.extend([jitter_op, jitter_coupling])

        # 3. Connection topology health chain
        if s.time_wait > 50:
            chains.append(RESET)      # lots of closing = reset
        if s.close_wait > 20:
            chains.append(COLLAPSE)   # stuck connections = collapse
        if s.established > 100:
            chains.append(LATTICE)    # complex topology = structure

        # 4. Recent operator chain (last 10 observations)
        recent_ops = list(self.op_chain)[-10:]
        if len(recent_ops) >= 3:
            chains.extend(recent_ops)

        # 5. Bump detection in rate history
        #    Rate spikes/drops = network bumps
        if len(self.recv_rate_history) >= 3:
            rates = list(self.recv_rate_history)[-5:]
            for i in range(len(rates) - 1):
                if rates[i] > 0:
                    ratio = rates[i + 1] / max(rates[i], 0.001)
                    if ratio > 3.0:
                        chains.append(CHAOS)   # spike
                    elif ratio < 0.3:
                        chains.append(COLLAPSE) # drop

        return {
            'chains': chains,
            'operator': s.operator,
            'band': s.band.value,
            'coupling': self.last_coupling,
            'health': self.last_health,
            'jitter': round(s.jitter, 4),
            'congestion': round(s.congestion_score, 4),
            'connections': s.connection_count,
            'established': s.established,
            'unique_remotes': s.unique_remotes,
            'send_mbps': round(s.send_rate_mbps, 3),
            'recv_mbps': round(s.recv_rate_mbps, 3),
        }

    def get_network_pids(self) -> Set[int]:
        """Return PIDs that own active network connections."""
        pids = set()
        for port_pids in self.conn_pid_map.values():
            pids.update(port_pids)
        return pids

    def operator_for_state(self) -> int:
        """Map current network state to TIG operator."""
        return self.state.operator

    def bump_rate(self) -> float:
        """Fraction of transitions that are bumps."""
        if self.total_transitions == 0:
            return 0.0
        return self.bump_count / self.total_transitions

    def current_shape(self) -> str:
        """Current behavior shape of network operator chain."""
        if len(self.op_chain) < 4:
            return 'VOID'
        return shape(list(self.op_chain))

    def current_fuse(self) -> int:
        """Current fused operator of network."""
        if not self.op_chain:
            return VOID
        return fuse(list(self.op_chain))

    def report(self) -> str:
        """Human-readable network organ report."""
        s = self.state
        lines = [
            f"  NETWORK ORGAN (nervous system):",
            f"    Band:        {s.band.value}",
            f"    Operator:    {OP[s.operator]}",
            f"    Shape:       {self.current_shape()}",
            f"    Fuse:        {OP[self.current_fuse()]}",
            f"    Send:        {s.send_rate_mbps:.3f} MB/s",
            f"    Recv:        {s.recv_rate_mbps:.3f} MB/s",
            f"    Packets/s:   {s.packet_rate:.0f}",
            f"    Connections: {s.connection_count} ({s.established} ESTABLISHED)",
            f"    Remotes:     {s.unique_remotes} unique hosts",
            f"    Jitter:      {s.jitter:.4f} (CV of packet rate)",
            f"    Congestion:  {s.congestion_score:.4f}",
            f"    Errors:      {s.error_rate:.1f}/s   Drops: {s.drop_rate:.1f}/s",
            f"    TIME_WAIT:   {s.time_wait}   CLOSE_WAIT: {s.close_wait}",
            f"    Coupling:    CL[traffic][conn] = {OP[self.last_coupling]}",
            f"    Health:      CL[coupling][error] = {OP[self.last_health]}",
            f"    Bumps:       {self.bump_count}/{self.total_transitions} ({self.bump_rate():.3f})",
            f"    Compositions:{self.compositions_total}",
            f"    Reads:       {self.reads}",
        ]
        return '\n'.join(lines)
