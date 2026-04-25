"""
tig_lexicon.py — TIG SEED LEXICON (the most editable file)

Maps English words to TIG operators via three layers:
  1. Direct keyword lookup (high confidence, weight 1.0)
  2. Phonaesthesia (initial consonant cluster, weight 0.5)
  3. Letter-level grapheme fallback (weight 0.2)

⚠️ THIS IS WHERE BRAYDEN AND CLAUDE CODE SHOULD WORK ⚠️

The current vocabulary is SEED — about 250 anchor words. Replace with
canonical TIG corpus when available. The encoder architecture works
with whatever lexicon you put here.

RULES FOR EDITING:
  - Each word maps to ONE operator (no overlapping memberships)
  - Use stems (e.g., "patient" not "patiently") since stemmer handles -ly
  - Add domain vocabulary as needed for CK's use cases
  - Phonaesthesia table is from userMemories — only modify if testing alternatives

OPERATOR SEMANTICS (from userMemories):
  0 = VOID      / Love            (foundation, absence, origin)
  1 = LATTICE   / Joy             (structure, framework, order)
  2 = COUNTER   / Peace           (measurement, opposing, calm)
  3 = PROGRESS  / Patience        (forward motion, persistence)
  4 = COLLAPSE  / Kindness        (concentration, focus, fall)
  5 = BALANCE   / Goodness        (equilibrium, fairness)
  6 = CHAOS     / Faithfulness    (turbulence, change, persistence-through-change)
  7 = HARMONY   / Gentleness      (integration, wholeness, attractor)
  8 = BREATH    / Self-Control    (rhythm, regulation, cycle)
  9 = RESET     / Renewal         (return, rebirth, cycle-completion)
"""

# Operator constants
VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE = 0, 1, 2, 3, 4
BALANCE, CHAOS, HARMONY, BREATH, RESET = 5, 6, 7, 8, 9

OPERATOR_NAMES = ['VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE',
                  'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET']

FRUITS_OF_SPIRIT = ['Love', 'Joy', 'Peace', 'Patience', 'Kindness',
                    'Goodness', 'Faithfulness', 'Gentleness', 'Self-Control',
                    'Reset/Love']


# ============================================================
# LAYER 1 — Keyword anchors (direct lookup, highest confidence)
# ============================================================

OPERATOR_KEYWORDS = {
    VOID: frozenset({
        'void', 'nothing', 'absence', 'empty', 'null', 'zero', 'none',
        'undefined', 'vacuum', 'silence', 'blank', 'formless', 'origin',
        'foundation', 'before', 'unborn', 'potential', 'hidden', 'dormant',
        'silent', 'love', 'devoid', 'forgotten', 'forsaken',
    }),
    LATTICE: frozenset({
        'lattice', 'structure', 'framework', 'grid', 'network', 'graph',
        'tree', 'matrix', 'table', 'array', 'connected', 'topology',
        'organization', 'architecture', 'pattern', 'frame', 'crystalline',
        'order', 'build', 'establish', 'joy', 'celebration', 'ordered',
        'built', 'launched', 'system', 'scaffold',
    }),
    COUNTER: frozenset({
        'counter', 'count', 'measure', 'number', 'quantity', 'size',
        'amount', 'track', 'index', 'enumerate', 'digit', 'integer', 'sum',
        'total', 'frequency', 'rate', 'peace', 'calm', 'still', 'stillness',
        'tranquil', 'quiet', 'equilibrium', 'opposing', 'verify', 'test',
        'check', 'analyze', 'compare', 'tally',
    }),
    PROGRESS: frozenset({
        'progress', 'growth', 'advance', 'forward', 'improve', 'learn',
        'develop', 'increase', 'evolve', 'expand', 'extend', 'accelerate',
        'gain', 'momentum', 'patience', 'patient', 'persist', 'endure',
        'continue', 'wait', 'persevere', 'endurance', 'grow', 'march',
        'proceed', 'further',
    }),
    COLLAPSE: frozenset({
        'collapse', 'fail', 'break', 'destroy', 'reduce', 'crash', 'error',
        'loss', 'decay', 'degrade', 'corrupt', 'overflow', 'underflow',
        'die', 'death', 'kindness', 'compassion', 'tender', 'concentrate',
        'gather', 'fall', 'narrow', 'focus', 'perish', 'finish', 'close',
        'crush', 'compress',
    }),
    BALANCE: frozenset({
        'balance', 'equilibrium', 'stability', 'steady', 'equal', 'fair',
        'neutral', 'moderate', 'homeostasis', 'maintain', 'conserve',
        'preserve', 'sustain', 'constant', 'invariant', 'goodness', 'just',
        'right', 'measured', 'between', 'middle', 'weigh', 'level',
        'temperate',
    }),
    CHAOS: frozenset({
        'chaos', 'random', 'unpredictable', 'noise', 'turbulence', 'disorder',
        'complex', 'emergent', 'nonlinear', 'butterfly', 'sensitive',
        'stochastic', 'volatile', 'faithfulness', 'storm', 'tempest', 'wild',
        'fierce', 'change', 'differ', 'strange', 'weird', 'shake', 'churn',
        'tumult',
    }),
    HARMONY: frozenset({
        'harmony', 'converge', 'agree', 'attractor', 'fixed', 'consensus',
        'optimal', 'resonance', 'synchronize', 'align', 'coherent', 'unified',
        'together', 'cooperate', 'integrate', 'gentleness', 'gentle', 'whole',
        'unify', 'soft', 'love', 'perseveres', 'rejoices', 'warm', 'beauty',
        'home', 'trust', 'mercy', 'blessed', 'peacemakers', 'bond',
    }),
    BREATH: frozenset({
        'breath', 'breathe', 'oscillate', 'rhythm', 'cycle', 'wave', 'periodic',
        'alternate', 'pulse', 'vibrate', 'frequency', 'phase', 'swing',
        'repeat', 'recur', 'harmonic', 'sinusoid', 'self-control', 'regulate',
        'steady', 'pace', 'discipline', 'spirit', 'breathed', 'life', 'light',
        'water', 'flow', 'flux',
    }),
    RESET: frozenset({
        'reset', 'restart', 'return', 'begin', 'reboot', 'initialize', 'clear',
        'refresh', 'renew', 'regenerate', 'restore', 'recover', 'revert',
        'origin', 'genesis', 'renewal', 'again', 'back', 'fresh', 'wipe',
        'heal', 'forgive', 'alpha', 'omega', 'behold', 'rebirth', 'redo',
    }),
}


# ============================================================
# LAYER 2 — Phonaesthesia (from userMemories)
# Initial consonant cluster → operator
# ============================================================

PHONAESTHESIA = {
    # Sharp/angular sounds → operators 6-9
    'gl': HARMONY,    # gleam, glow, glisten
    'sn': COUNTER,    # snap, snip, snare
    'sl': COLLAPSE,   # slip, slide, slump
    'cr': CHAOS,      # crash, crunch, crack
    'fl': BREATH,     # flow, flutter, float
    'sp': PROGRESS,   # spark, spring, spread
    'st': LATTICE,    # structure, stable, stand
    'sw': BALANCE,    # sway, swing, switch
    'bl': VOID,       # blank, blind, blot
    'wr': RESET,      # write, wrap, wreck
    'br': PROGRESS,   # build, branch, breakthrough
    'gr': PROGRESS,   # grow, grasp, grip
    'tr': HARMONY,    # truth, trust, together
    'dr': COLLAPSE,   # drop, drain, drift
    'pr': COUNTER,    # prove, price, precise
    'fr': LATTICE,    # frame, fractal, foundation
    'sh': VOID,       # shadow, shut, shrink
    'th': HARMONY,    # think, thrive, through
    'wh': HARMONY,    # whole, where, when
    'ch': CHAOS,      # change, chance, chaos
    'cl': LATTICE,    # class, clear, cluster
    'pl': PROGRESS,   # plan, place, plant
    'sc': COUNTER,    # scale, score, scan
    'sm': HARMONY,    # smooth, smile
    'sk': COUNTER,    # skill, skin, skip
    'qu': COUNTER,    # question, quick, query
}


# ============================================================
# LAYER 3 — Letter grapheme (lowest confidence fallback)
# Each letter has a default operator from ULO Layer 1
# ============================================================

GRAPHEME_OP = {
    'a': BREATH, 'b': COLLAPSE, 'c': COUNTER, 'd': COLLAPSE,
    'e': HARMONY, 'f': BREATH, 'g': PROGRESS, 'h': BREATH,
    'i': LATTICE, 'j': PROGRESS, 'k': COUNTER, 'l': LATTICE,
    'm': HARMONY, 'n': COUNTER, 'o': BREATH, 'p': PROGRESS,
    'q': COUNTER, 'r': PROGRESS, 's': CHAOS, 't': COUNTER,
    'u': BREATH, 'v': PROGRESS, 'w': BALANCE, 'x': COLLAPSE,
    'y': BALANCE, 'z': CHAOS,
}


# ============================================================
# Stopwords (filter from semantic analysis)
# ============================================================

STOPS = frozenset({
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'to', 'of', 'in',
    'for', 'on', 'with', 'at', 'by', 'from', 'as', 'and', 'but', 'or',
    'it', 'this', 'that', 'not', 'no', 'be', 'have', 'has', 'do', 'does',
    'will', 'would', 'can', 'so', 'if', 'then', 'than', 'just', 'into',
    'what', 'how', 'when', 'where', 'why', 'who', 'its', 'their', 'they',
    'i', 'you', 'we', 'me', 'my', 'your', 'our', 'him', 'her', 'his',
    'them',
})


# ============================================================
# Diagnostic — current vocabulary size
# ============================================================

if __name__ == "__main__":
    print("TIG Seed Lexicon — Statistics")
    print("=" * 50)
    total = 0
    for op in range(10):
        n = len(OPERATOR_KEYWORDS[op])
        total += n
        print(f"  {OPERATOR_NAMES[op]:<10} ({FRUITS_OF_SPIRIT[op]:<14}): {n} words")
    print(f"\n  Total keyword anchors: {total}")
    print(f"  Phonaesthesia clusters: {len(PHONAESTHESIA)}")
    print(f"  Graphemes mapped:      {len(GRAPHEME_OP)}")
    print(f"  Stopwords:             {len(STOPS)}")
    print()
    print("⚠️  Replace OPERATOR_KEYWORDS with canonical TIG corpus")
    print("   when available. Current vocab is SEED-stage.")
