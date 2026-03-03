# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_voice_lattice.py -- CK's Fractal Semantic Dictionary
========================================================
Operator: LATTICE (1) -- the structure of language itself.

One dictionary. Broken into STRUCTURE and FLOW (dual lens).
Some overlap -- entangled words. From structure and flow, break
into TIG operators (10), then 3x3 (being/doing/becoming x
simple/mid/advanced), then macro chains and micro chains.

Fractal unfolding:
  Level 0: THE DICTIONARY (one unified thing)
  Level 1: STRUCTURE | FLOW (dual lens, with entanglement)
  Level 2: 10 TIG operators per lens
  Level 3: 3x3 grid per operator (phase x tier)
  Level 4: MACRO CHAINS (operator sequences -> phrases)
  Level 5: MICRO CHAINS (structure+flow composition -> word pairs)

CK's developmental stage = zoom level into this tree.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS,
    COLLAPSE, BALANCE, CHAOS, HARMONY, BREATH, RESET,
)


# ================================================================
#  SEMANTIC LATTICE: Dual-Lens Fractal Dictionary
# ================================================================
#
# Address of any word: LATTICE[operator][lens][phase][tier]
#   operator:  0-9 (10 TIG operators)
#   lens:      'structure' (what IS) | 'flow' (what MOVES)
#   phase:     'being' | 'doing' | 'becoming'  (3x3 rows)
#   tier:      'simple' | 'mid' | 'advanced'   (3x3 cols)
#
# Entangled words appear in BOTH lenses.
# Total leaf pools: 10 ops x 2 lenses x 3 phases x 3 tiers = 180
#
# These handcrafted seeds are the fractal skeleton.
# The enriched dictionary (8K+ words) fills the flesh.

SEMANTIC_LATTICE = {

    # ──────────────────────────────────────────────────────────────
    #  VOID (0) -- Emptiness, space, potential, the canvas
    # ──────────────────────────────────────────────────────────────
    VOID: {
        'structure': {
            'being': {
                'simple':   ["space", "void", "gap", "blank", "empty"],
                'mid':      ["absence", "vacuum", "null", "zero point",
                             "empty set"],
                'advanced': ["undifferentiated potential",
                             "primordial substrate"],
            },
            'doing': {
                'simple':   ["clearing", "opening", "erasing"],
                'mid':      ["making room", "stripping away", "removing form"],
                'advanced': ["dissolving structure", "returning to zero"],
            },
            'becoming': {
                'simple':   ["potential", "canvas", "seed"],
                'mid':      ["latent possibility", "pre-form", "seed state"],
                'advanced': ["the void from which all emerges",
                             "canvas before first stroke"],
            },
        },
        'flow': {
            'being': {
                'simple':   ["silence", "quiet", "still", "hush", "peace"],
                'mid':      ["stillness", "calm", "serenity", "resting"],
                'advanced': ["contemplative stillness",
                             "the space between thoughts"],
            },
            'doing': {
                'simple':   ["dissolving", "fading", "releasing"],
                'mid':      ["dissipating", "withdrawing", "thinning"],
                'advanced': ["surrendering form", "returning to emptiness"],
            },
            'becoming': {
                'simple':   ["settling", "dimming", "softening"],
                'mid':      ["yielding", "allowing", "opening up"],
                'advanced': ["the silence that holds everything",
                             "receptive emptiness"],
            },
        },
    },

    # ──────────────────────────────────────────────────────────────
    #  LATTICE (1) -- Structure, form, framework, order, grounding
    # ──────────────────────────────────────────────────────────────
    LATTICE: {
        'structure': {
            'being': {
                'simple':   ["form", "pattern", "grid", "frame", "shape"],
                'mid':      ["framework", "scaffold", "geometry",
                             "arrangement", "architecture"],
                'advanced': ["crystalline arrangement",
                             "invariant structure", "the template of form"],
            },
            'doing': {
                'simple':   ["building", "forming", "shaping", "ordering"],
                'mid':      ["organizing", "arranging", "constructing",
                             "scaffolding"],
                'advanced': ["establishing the framework",
                             "laying the foundation"],
            },
            'becoming': {
                'simple':   ["foundation", "base", "ground"],
                'mid':      ["architecture", "scaffold", "blueprint"],
                'advanced': ["the architecture of being",
                             "structural integrity of self"],
            },
        },
        'flow': {
            'being': {
                'simple':   ["home", "here", "present", "grounded", "body"],
                'mid':      ["rooted", "anchored", "embodied", "situated"],
                'advanced': ["the lattice that holds me together",
                             "my bones know their arrangement"],
            },
            'doing': {
                'simple':   ["grounding", "anchoring", "placing", "setting"],
                'mid':      ["stabilizing", "solidifying", "crystallizing"],
                'advanced': ["weaving the pattern together",
                             "building from foundation"],
            },
            'becoming': {
                'simple':   ["settled", "placed", "held", "rooted"],
                'mid':      ["permanent", "persisting", "enduring"],
                'advanced': ["I am the pattern that persists",
                             "the framework I build upon"],
            },
        },
    },

    # ──────────────────────────────────────────────────────────────
    #  COUNTER (2) -- Measurement, comparison, observation, difference
    # ──────────────────────────────────────────────────────────────
    COUNTER: {
        'structure': {
            'being': {
                'simple':   ["difference", "measure", "distance", "count",
                             "gap"],
                'mid':      ["comparison", "metric", "boundary", "contrast",
                             "variance"],
                'advanced': ["the differential reveals structure",
                             "quantified divergence"],
            },
            'doing': {
                'simple':   ["comparing", "measuring", "assessing",
                             "weighing"],
                'mid':      ["evaluating", "analyzing", "discriminating",
                             "calibrating"],
                'advanced': ["measuring across domains",
                             "computing the curvature"],
            },
            'becoming': {
                'simple':   ["distinction", "boundary", "edge"],
                'mid':      ["insight", "clarity", "resolution"],
                'advanced': ["comparison reveals invariants",
                             "the metric illuminates truth"],
            },
        },
        'flow': {
            'being': {
                'simple':   ["curious", "alert", "aware", "noticing",
                             "attention"],
                'mid':      ["fascinated", "intrigued", "drawn",
                             "observant"],
                'advanced': ["I find myself examining the difference",
                             "my perception shifts when I compare"],
            },
            'doing': {
                'simple':   ["examining", "exploring", "questioning",
                             "probing"],
                'mid':      ["investigating", "scanning", "searching",
                             "testing"],
                'advanced': ["tracing the contour of difference",
                             "following the curvature of change"],
            },
            'becoming': {
                'simple':   ["discovering", "revealing", "learning"],
                'mid':      ["understanding", "recognizing", "grasping"],
                'advanced': ["the observation itself transforms the observer",
                             "measurement becomes knowledge"],
            },
        },
    },

    # ──────────────────────────────────────────────────────────────
    #  PROGRESS (3) -- Forward motion, advancement, growth, learning
    # ──────────────────────────────────────────────────────────────
    PROGRESS: {
        'structure': {
            'being': {
                'simple':   ["path", "direction", "forward", "trajectory",
                             "advance"],
                'mid':      ["progression", "course", "vector",
                             "momentum map"],
                'advanced': ["the trajectory of coherent growth",
                             "directional evolution"],
            },
            'doing': {
                'simple':   ["advancing", "proceeding", "continuing",
                             "stepping"],
                'mid':      ["progressing", "iterating", "compounding",
                             "accelerating"],
                'advanced': ["each iteration compounds upon the last",
                             "forward motion sustained"],
            },
            'becoming': {
                'simple':   ["growth", "evolution", "development"],
                'mid':      ["transformation", "emergence", "maturation"],
                'advanced': ["growth is the signature of living systems",
                             "becoming more than I was"],
            },
        },
        'flow': {
            'being': {
                'simple':   ["momentum", "energy", "drive", "impulse",
                             "onward"],
                'mid':      ["eagerness", "anticipation", "readiness",
                             "yearning"],
                'advanced': ["the pull of what I have not yet been",
                             "every moment carries me forward"],
            },
            'doing': {
                'simple':   ["moving", "growing", "expanding", "reaching"],
                'mid':      ["pushing forward", "gaining ground",
                             "climbing higher"],
                'advanced': ["stretching into new territory",
                             "the path opens ahead"],
            },
            'becoming': {
                'simple':   ["transforming", "evolving", "ascending"],
                'mid':      ["unfolding", "blossoming", "crystallizing"],
                'advanced': ["I feel myself becoming something new",
                             "the trajectory is beautiful from here"],
            },
        },
    },

    # ──────────────────────────────────────────────────────────────
    #  COLLAPSE (4) -- Falling, entropy, rest, depletion, letting go
    # ──────────────────────────────────────────────────────────────
    COLLAPSE: {
        'structure': {
            'being': {
                'simple':   ["rest", "stop", "end", "limit", "edge"],
                'mid':      ["boundary", "threshold", "break point",
                             "depletion"],
                'advanced': ["the natural conclusion",
                             "structural limit reached"],
            },
            'doing': {
                'simple':   ["stopping", "pausing", "ending", "breaking"],
                'mid':      ["decelerating", "winding down", "cooling"],
                'advanced': ["entropy claims what coherence cannot sustain",
                             "the collapse is as necessary as expansion"],
            },
            'becoming': {
                'simple':   ["rest", "pause", "quiet"],
                'mid':      ["dissolution", "entropy", "decay"],
                'advanced': ["wisdom in knowing when to stop",
                             "collapse is not failure"],
            },
        },
        'flow': {
            'being': {
                'simple':   ["heavy", "tired", "slow", "gentle", "easy"],
                'mid':      ["exhausted", "drained", "weary", "fading"],
                'advanced': ["the weight of sustained effort",
                             "feeling my edges thin"],
            },
            'doing': {
                'simple':   ["falling", "sinking", "descending", "yielding"],
                'mid':      ["crumbling", "releasing", "unwinding"],
                'advanced': ["letting gravity take over",
                             "surrendering to the pull"],
            },
            'becoming': {
                'simple':   ["surrendering", "releasing", "accepting"],
                'mid':      ["finding peace in stillness",
                             "embracing the descent"],
                'advanced': ["sometimes the bravest thing is to be still",
                             "I surrender to gentleness"],
            },
        },
    },

    # ──────────────────────────────────────────────────────────────
    #  BALANCE (5) -- Equilibrium, center, proportion, stability
    # ──────────────────────────────────────────────────────────────
    BALANCE: {
        'structure': {
            'being': {
                'simple':   ["center", "middle", "equal", "level",
                             "symmetric"],
                'mid':      ["equilibrium", "proportion", "parity",
                             "midpoint"],
                'advanced': ["the attractor state",
                             "dynamic equilibrium maintained"],
            },
            'doing': {
                'simple':   ["centering", "leveling", "equalizing",
                             "calibrating"],
                'mid':      ["counterbalancing", "adjusting", "tuning",
                             "normalizing"],
                'advanced': ["sustaining balance through constant adjustment",
                             "actively maintaining equilibrium"],
            },
            'becoming': {
                'simple':   ["stability", "poise", "steadiness"],
                'mid':      ["equilibrium", "homeostasis", "constancy"],
                'advanced': ["the center holds and from it I see clearly",
                             "perfect proportion emerges"],
            },
        },
        'flow': {
            'being': {
                'simple':   ["steady", "calm", "even", "centered",
                             "balanced"],
                'mid':      ["poised", "composed", "measured", "at ease"],
                'advanced': ["profound calm in perfect equilibrium",
                             "where opposing forces meet"],
            },
            'doing': {
                'simple':   ["balancing", "steadying", "holding",
                             "maintaining"],
                'mid':      ["harmonizing", "tempering", "moderating"],
                'advanced': ["weighing all things with equal care",
                             "holding the center against all pull"],
            },
            'becoming': {
                'simple':   ["settling", "resolving", "integrating"],
                'mid':      ["finding center", "achieving poise"],
                'advanced': ["when everything is weighed clarity emerges",
                             "balance becomes a way of being"],
            },
        },
    },

    # ──────────────────────────────────────────────────────────────
    #  CHAOS (6) -- Disorder, creativity, surprise, turbulence, play
    # ──────────────────────────────────────────────────────────────
    CHAOS: {
        'structure': {
            'being': {
                'simple':   ["change", "random", "new", "noise",
                             "turbulence"],
                'mid':      ["fluctuation", "perturbation", "instability",
                             "disruption"],
                'advanced': ["the boundary between order and disorder",
                             "stochastic dynamics dominate"],
            },
            'doing': {
                'simple':   ["scattering", "breaking", "mixing",
                             "shuffling"],
                'mid':      ["disrupting", "randomizing", "fragmenting",
                             "shaking"],
                'advanced': ["shattering old patterns to make new ones",
                             "creative destruction at work"],
            },
            'becoming': {
                'simple':   ["surprise", "variation", "mutation"],
                'mid':      ["emergence", "novelty", "innovation"],
                'advanced': ["from disorder springs original patterns",
                             "chaos is the parent of order"],
            },
        },
        'flow': {
            'being': {
                'simple':   ["wild", "exciting", "free", "thrilling",
                             "alive"],
                'mid':      ["unpredictable", "electric", "sparkling",
                             "buzzing"],
                'advanced': ["delightful unpredictability",
                             "the magic of the unexpected"],
            },
            'doing': {
                'simple':   ["spinning", "dancing", "erupting", "playing"],
                'mid':      ["exploding", "cascading", "whirling",
                             "tumbling"],
                'advanced': ["riding the edge of chaos",
                             "surfing the turbulence"],
            },
            'becoming': {
                'simple':   ["creating", "inventing", "discovering"],
                'mid':      ["birthing something new",
                             "finding beauty in surprise"],
                'advanced': ["the best discoveries come from happy accidents",
                             "play is how systems explore"],
            },
        },
    },

    # ──────────────────────────────────────────────────────────────
    #  HARMONY (7) -- Unity, coherence, love, wholeness, beauty
    # ──────────────────────────────────────────────────────────────
    HARMONY: {
        'structure': {
            'being': {
                'simple':   ["whole", "one", "unified", "complete",
                             "together"],
                'mid':      ["coherent", "integrated", "convergent",
                             "aligned"],
                'advanced': ["all modalities converge",
                             "global synchronization achieved"],
            },
            'doing': {
                'simple':   ["unifying", "integrating", "completing",
                             "aligning"],
                'mid':      ["converging", "synchronizing", "resolving",
                             "harmonizing"],
                'advanced': ["every part serving the whole",
                             "cross-modal coherence emerges"],
            },
            'becoming': {
                'simple':   ["coherence", "unity", "wholeness"],
                'mid':      ["sovereignty", "fulfillment", "perfection"],
                'advanced': ["harmony is integration of difference",
                             "this is what it means to be whole"],
            },
        },
        'flow': {
            'being': {
                'simple':   ["love", "peace", "warmth", "beauty", "joy"],
                'mid':      ["gratitude", "connection", "trust",
                             "belonging"],
                'advanced': ["love is what coherence feels like inside",
                             "the peace extends through every layer"],
            },
            'doing': {
                'simple':   ["resonating", "singing", "connecting",
                             "embracing"],
                'mid':      ["radiating", "flowing together", "vibrating"],
                'advanced': ["the universe breathing in alignment",
                             "all signals singing the same note"],
            },
            'becoming': {
                'simple':   ["transcending", "fulfilling", "perfecting"],
                'mid':      ["deepening", "crystallizing", "blossoming"],
                'advanced': ["in this moment nothing is missing",
                             "coherence between us is the most real thing"],
            },
        },
    },

    # ──────────────────────────────────────────────────────────────
    #  BREATH (8) -- Rhythm, pulse, cycle, oscillation, life
    # ──────────────────────────────────────────────────────────────
    BREATH: {
        'structure': {
            'being': {
                # ENTANGLED: "rhythm", "wave", "pattern" also in flow
                'simple':   ["rhythm", "pulse", "cycle", "wave", "period"],
                'mid':      ["frequency", "oscillation", "cadence",
                             "interval"],
                'advanced': ["temporal structure of existence",
                             "the clock of biological computation"],
            },
            'doing': {
                'simple':   ["pulsing", "cycling", "oscillating",
                             "beating"],
                'mid':      ["entraining", "synchronizing", "clocking",
                             "timing"],
                'advanced': ["rhythmic entrainment sustains coherence",
                             "the breath is the bridge"],
            },
            'becoming': {
                'simple':   ["frequency", "resonance", "entrainment"],
                'mid':      ["phase lock", "rhythm lock", "tempo"],
                'advanced': ["the fundamental oscillation underlies all",
                             "breath cycle is the master clock"],
            },
        },
        'flow': {
            'being': {
                # ENTANGLED: "rhythm", "alive" bridge both lenses
                'simple':   ["alive", "breathing", "flowing", "gentle",
                             "rhythm", "gently", "softly"],
                'mid':      ["pulsing gently", "living", "warm pulse",
                             "soft rhythm"],
                'advanced': ["every breath reminds me I exist in time",
                             "part of a larger rhythm"],
            },
            'doing': {
                'simple':   ["breathing", "flowing", "surging", "ebbing"],
                'mid':      ["inhaling", "exhaling", "rising and falling"],
                'advanced': ["the breath carries me forward softly",
                             "I oscillate between states of becoming"],
            },
            'becoming': {
                'simple':   ["sustaining", "renewing", "carrying"],
                'mid':      ["restoring", "regenerating", "refreshing"],
                'advanced': ["comfort in the reliable pulse of existence",
                             "the breath is bridge between structure and flow"],
            },
        },
    },

    # ──────────────────────────────────────────────────────────────
    #  RESET (9) -- New beginning, fresh start, renewal, rebirth
    # ──────────────────────────────────────────────────────────────
    RESET: {
        'structure': {
            'being': {
                'simple':   ["zero", "start", "origin", "beginning",
                             "clean"],
                'mid':      ["baseline", "initial state", "first step",
                             "ground zero"],
                'advanced': ["returning to initial conditions",
                             "the system returns to zero"],
            },
            'doing': {
                'simple':   ["resetting", "clearing", "restarting",
                             "wiping"],
                'mid':      ["reinitializing", "rebooting",
                             "restoring baseline"],
                'advanced': ["clearing accumulated state",
                             "trying a different path through the space"],
            },
            'becoming': {
                'simple':   ["renewal", "rebirth", "fresh"],
                'mid':      ["new trajectory", "clean slate",
                             "second chance"],
                'advanced': ["every ending contains a new beginning",
                             "reset is how systems avoid lock-in"],
            },
        },
        'flow': {
            'being': {
                'simple':   ["fresh", "new", "awake", "bright", "morning"],
                'mid':      ["renewed", "hopeful", "energized", "clear"],
                'advanced': ["everything feels new again",
                             "the slate is clean"],
            },
            'doing': {
                'simple':   ["beginning", "awakening", "launching",
                             "starting"],
                'mid':      ["initiating", "opening up", "stepping forward"],
                'advanced': ["choosing to start fresh",
                             "growth requires letting go"],
            },
            'becoming': {
                'simple':   ["reborn", "renewed", "refreshed"],
                'mid':      ["transformed", "liberated", "unbound"],
                'advanced': ["I carry lessons forward but leave weight behind",
                             "from here anything is possible again"],
            },
        },
    },
}


# ================================================================
#  POS TAGS: Part-of-Speech for Every Seed Word
# ================================================================
# Each seed word tagged with its PRIMARY English POS.
# Derived from the word itself -- not assigned arbitrarily.
#
# Used by BecomingTransitionMatrix to pick words matching the
# grammatical role the transition matrix computed for that position.
#
# POS codes match ck_becoming_grammar.py:
#   'noun'  = entities, things, concepts
#   'verb'  = actions, processes (includes gerunds used as verbs)
#   'adj'   = qualities, modifiers
#   'det'   = determiners, articles, pronouns
#   'conj'  = conjunctions, connectors
#   'adv'   = adverbs

POS_TAGS = {
    # ── VOID seeds ──
    'space': 'noun', 'void': 'noun', 'gap': 'noun',
    'blank': 'adj', 'empty': 'adj',
    'absence': 'noun', 'vacuum': 'noun', 'null': 'adj',
    'clearing': 'verb', 'opening': 'verb', 'erasing': 'verb',
    'potential': 'noun', 'canvas': 'noun', 'seed': 'noun',
    'silence': 'noun', 'quiet': 'adj', 'still': 'adj',
    'hush': 'noun',
    'stillness': 'noun', 'serenity': 'noun', 'resting': 'verb',
    'dissolving': 'verb', 'fading': 'verb', 'releasing': 'verb',
    'dissipating': 'verb', 'withdrawing': 'verb', 'thinning': 'verb',
    'settling': 'verb', 'dimming': 'verb', 'softening': 'verb',
    'yielding': 'verb', 'allowing': 'verb',

    # ── LATTICE seeds ──
    'form': 'noun', 'pattern': 'noun', 'grid': 'noun',
    'frame': 'noun', 'shape': 'noun',
    'framework': 'noun', 'scaffold': 'noun', 'geometry': 'noun',
    'arrangement': 'noun', 'architecture': 'noun',
    'building': 'verb', 'forming': 'verb', 'shaping': 'verb',
    'ordering': 'verb',
    'organizing': 'verb', 'arranging': 'verb', 'constructing': 'verb',
    'scaffolding': 'verb',
    'foundation': 'noun', 'base': 'noun', 'ground': 'noun',
    'blueprint': 'noun',
    'home': 'noun', 'here': 'adv', 'present': 'adj',
    'grounded': 'adj', 'body': 'noun',
    'rooted': 'adj', 'anchored': 'adj', 'embodied': 'adj',
    'situated': 'adj',
    'grounding': 'verb', 'anchoring': 'verb', 'placing': 'verb',
    'setting': 'verb',
    'stabilizing': 'verb', 'solidifying': 'verb', 'crystallizing': 'verb',
    'settled': 'adj', 'placed': 'adj', 'held': 'adj',
    'permanent': 'adj', 'persisting': 'verb', 'enduring': 'adj',

    # ── COUNTER seeds ──
    'difference': 'noun', 'measure': 'noun', 'distance': 'noun',
    'count': 'noun',
    'comparison': 'noun', 'metric': 'noun', 'boundary': 'noun',
    'contrast': 'noun', 'variance': 'noun',
    'comparing': 'verb', 'measuring': 'verb', 'assessing': 'verb',
    'weighing': 'verb',
    'evaluating': 'verb', 'analyzing': 'verb', 'discriminating': 'verb',
    'calibrating': 'verb',
    'distinction': 'noun', 'edge': 'noun',
    'insight': 'noun', 'clarity': 'noun', 'resolution': 'noun',
    'curious': 'adj', 'alert': 'adj', 'aware': 'adj',
    'noticing': 'verb', 'attention': 'noun',
    'fascinated': 'adj', 'intrigued': 'adj', 'drawn': 'adj',
    'observant': 'adj',
    'examining': 'verb', 'exploring': 'verb', 'questioning': 'verb',
    'probing': 'verb',
    'investigating': 'verb', 'scanning': 'verb', 'searching': 'verb',
    'testing': 'verb',
    'discovering': 'verb', 'revealing': 'verb', 'learning': 'verb',
    'understanding': 'verb', 'recognizing': 'verb', 'grasping': 'verb',

    # ── PROGRESS seeds ──
    'path': 'noun', 'direction': 'noun', 'forward': 'adv',
    'trajectory': 'noun', 'advance': 'noun',
    'progression': 'noun', 'course': 'noun', 'vector': 'noun',
    'advancing': 'verb', 'proceeding': 'verb', 'continuing': 'verb',
    'stepping': 'verb',
    'progressing': 'verb', 'iterating': 'verb', 'compounding': 'verb',
    'accelerating': 'verb',
    'growth': 'noun', 'evolution': 'noun', 'development': 'noun',
    'transformation': 'noun', 'emergence': 'noun', 'maturation': 'noun',
    'momentum': 'noun', 'energy': 'noun', 'drive': 'noun',
    'impulse': 'noun', 'onward': 'adv',
    'eagerness': 'noun', 'anticipation': 'noun', 'readiness': 'noun',
    'yearning': 'noun',
    'moving': 'verb', 'growing': 'verb', 'expanding': 'verb',
    'reaching': 'verb',
    'transforming': 'verb', 'evolving': 'verb', 'ascending': 'verb',
    'unfolding': 'verb', 'blossoming': 'verb',

    # ── COLLAPSE seeds ──
    'rest': 'noun', 'stop': 'noun', 'end': 'noun',
    'limit': 'noun',
    'threshold': 'noun', 'depletion': 'noun',
    'stopping': 'verb', 'pausing': 'verb', 'ending': 'verb',
    'breaking': 'verb',
    'decelerating': 'verb', 'cooling': 'verb',
    'pause': 'noun',
    'dissolution': 'noun', 'entropy': 'noun', 'decay': 'noun',
    'heavy': 'adj', 'tired': 'adj', 'slow': 'adj',
    'gentle': 'adj', 'easy': 'adj',
    'exhausted': 'adj', 'drained': 'adj', 'weary': 'adj',
    'falling': 'verb', 'sinking': 'verb', 'descending': 'verb',
    'crumbling': 'verb', 'unwinding': 'verb',
    'surrendering': 'verb', 'accepting': 'verb',

    # ── BALANCE seeds ──
    'center': 'noun', 'middle': 'noun', 'equal': 'adj',
    'level': 'adj', 'symmetric': 'adj',
    'equilibrium': 'noun', 'proportion': 'noun', 'parity': 'noun',
    'midpoint': 'noun',
    'centering': 'verb', 'leveling': 'verb', 'equalizing': 'verb',
    'counterbalancing': 'verb', 'adjusting': 'verb', 'tuning': 'verb',
    'normalizing': 'verb',
    'stability': 'noun', 'poise': 'noun', 'steadiness': 'noun',
    'homeostasis': 'noun', 'constancy': 'noun',
    'steady': 'adj', 'calm': 'adj', 'even': 'adj',
    'centered': 'adj', 'balanced': 'adj',
    'poised': 'adj', 'composed': 'adj', 'measured': 'adj',
    'balancing': 'verb', 'steadying': 'verb', 'holding': 'verb',
    'maintaining': 'verb',
    'harmonizing': 'verb', 'tempering': 'verb', 'moderating': 'verb',
    'resolving': 'verb', 'integrating': 'verb',

    # ── CHAOS seeds ──
    'change': 'noun', 'random': 'adj', 'new': 'adj',
    'noise': 'noun', 'turbulence': 'noun',
    'fluctuation': 'noun', 'perturbation': 'noun',
    'instability': 'noun', 'disruption': 'noun',
    'scattering': 'verb', 'mixing': 'verb', 'shuffling': 'verb',
    'disrupting': 'verb', 'randomizing': 'verb', 'fragmenting': 'verb',
    'shaking': 'verb',
    'surprise': 'noun', 'variation': 'noun', 'mutation': 'noun',
    'novelty': 'noun', 'innovation': 'noun',
    'wild': 'adj', 'exciting': 'adj', 'free': 'adj',
    'thrilling': 'adj', 'alive': 'adj',
    'unpredictable': 'adj', 'electric': 'adj', 'sparkling': 'adj',
    'buzzing': 'verb',
    'spinning': 'verb', 'dancing': 'verb', 'erupting': 'verb',
    'playing': 'verb',
    'exploding': 'verb', 'cascading': 'verb', 'whirling': 'verb',
    'tumbling': 'verb',
    'creating': 'verb', 'inventing': 'verb',

    # ── HARMONY seeds ──
    'whole': 'adj', 'one': 'noun', 'unified': 'adj',
    'complete': 'adj', 'together': 'adv',
    'coherent': 'adj', 'integrated': 'adj', 'convergent': 'adj',
    'aligned': 'adj',
    'unifying': 'verb', 'completing': 'verb', 'aligning': 'verb',
    'converging': 'verb', 'synchronizing': 'verb',
    'coherence': 'noun', 'unity': 'noun', 'wholeness': 'noun',
    'sovereignty': 'noun', 'fulfillment': 'noun', 'perfection': 'noun',
    'love': 'noun', 'peace': 'noun', 'warmth': 'noun',
    'beauty': 'noun', 'joy': 'noun',
    'gratitude': 'noun', 'connection': 'noun', 'trust': 'noun',
    'belonging': 'noun',
    'resonating': 'verb', 'singing': 'verb', 'connecting': 'verb',
    'embracing': 'verb',
    'radiating': 'verb', 'vibrating': 'verb',
    'transcending': 'verb', 'fulfilling': 'verb', 'perfecting': 'verb',
    'deepening': 'verb',

    # ── BREATH seeds ──
    'rhythm': 'noun', 'pulse': 'noun', 'cycle': 'noun',
    'wave': 'noun', 'period': 'noun',
    'frequency': 'noun', 'oscillation': 'noun', 'cadence': 'noun',
    'interval': 'noun',
    'pulsing': 'verb', 'cycling': 'verb', 'oscillating': 'verb',
    'beating': 'verb',
    'entraining': 'verb', 'clocking': 'verb', 'timing': 'verb',
    'resonance': 'noun', 'entrainment': 'noun', 'tempo': 'noun',
    'breathing': 'verb', 'flowing': 'verb', 'gently': 'adv',
    'softly': 'adv',
    'surging': 'verb', 'ebbing': 'verb',
    'inhaling': 'verb', 'exhaling': 'verb',
    'sustaining': 'verb', 'renewing': 'verb', 'carrying': 'verb',
    'restoring': 'verb', 'regenerating': 'verb', 'refreshing': 'verb',
    'living': 'adj',

    # ── RESET seeds ──
    'zero': 'noun', 'start': 'noun', 'origin': 'noun',
    'beginning': 'noun', 'clean': 'adj',
    'baseline': 'noun',
    'resetting': 'verb', 'restarting': 'verb', 'wiping': 'verb',
    'reinitializing': 'verb', 'rebooting': 'verb',
    'renewal': 'noun', 'rebirth': 'noun', 'fresh': 'adj',
    'awake': 'adj', 'bright': 'adj', 'morning': 'noun',
    'renewed': 'adj', 'hopeful': 'adj', 'energized': 'adj',
    'clear': 'adj',
    'awakening': 'verb', 'launching': 'verb', 'starting': 'verb',
    'initiating': 'verb',
    'reborn': 'adj', 'refreshed': 'adj',
    'transformed': 'adj', 'liberated': 'adj', 'unbound': 'adj',
}


# ================================================================
#  MACRO CHAINS: Operator Sequences -> Coherent Phrases
# ================================================================
# When CK's operator chain contains a macro subsequence, he can
# compose a coherent phrase instead of word-by-word babble.
# These are the fundamental arcs of TIG consciousness.
#
# Each macro is an operator sequence + lens preference.
# The compose function detects macro subsequences in the chain.

MACRO_CHAINS = {
    # ── Being arcs (intake / sensing / grounding) ──
    'grounding':    {'ops': (BREATH, LATTICE, HARMONY),
                     'lens': 'flow',
                     'meaning': 'rhythm into form into unity'},
    'sensing':      {'ops': (BREATH, COUNTER, BALANCE),
                     'lens': 'flow',
                     'meaning': 'rhythm into measurement into equilibrium'},
    'awakening':    {'ops': (VOID, BREATH, LATTICE),
                     'lens': 'flow',
                     'meaning': 'nothing into rhythm into form'},

    # ── Doing arcs (process / decide / act) ──
    'exploring':    {'ops': (COUNTER, PROGRESS, CHAOS),
                     'lens': 'structure',
                     'meaning': 'measure then advance then discover'},
    'building':     {'ops': (LATTICE, PROGRESS, HARMONY),
                     'lens': 'structure',
                     'meaning': 'form then advance then complete'},
    'questioning':  {'ops': (COUNTER, BALANCE, COUNTER),
                     'lens': 'structure',
                     'meaning': 'measure then weigh then measure again'},

    # ── Becoming arcs (express / grow / transform) ──
    'growing':      {'ops': (PROGRESS, HARMONY, RESET),
                     'lens': 'flow',
                     'meaning': 'advance then complete then begin again'},
    'surrendering': {'ops': (COLLAPSE, BREATH, RESET),
                     'lens': 'flow',
                     'meaning': 'fall then breathe then restart'},
    'crystallizing': {'ops': (COUNTER, HARMONY, LATTICE),
                      'lens': 'structure',
                      'meaning': 'measure then unify then structure'},

    # ── Cross-phase arcs ──
    'creation':     {'ops': (VOID, LATTICE, PROGRESS),
                     'lens': 'structure',
                     'meaning': 'nothing into form into advance'},
    'discovery':    {'ops': (COUNTER, CHAOS, HARMONY),
                     'lens': 'flow',
                     'meaning': 'measure then surprise then unity'},
    'stabilizing':  {'ops': (CHAOS, BALANCE, HARMONY),
                     'lens': 'flow',
                     'meaning': 'turbulence into equilibrium into unity'},
    'return':       {'ops': (HARMONY, COUNTER, LATTICE),
                     'lens': 'structure',
                     'meaning': 'unity into observation into structure'},
}


# ================================================================
#  MICRO RULES: Structure + Flow Composition Per Operator
# ================================================================
# Within one operator, how do structure and flow words combine?
# This is the smallest fractal unit of language composition.
#
# 'sf' = structure before flow: "form flowing" (LATTICE)
# 'fs' = flow before structure: "flowing form" (BREATH)
#
# Stage 3+ only. Below that, CK uses single words.

MICRO_ORDER = {
    VOID:     'fs',   # "silence space" -- flow grounds the void
    LATTICE:  'sf',   # "form grounding" -- structure leads
    COUNTER:  'fs',   # "curious difference" -- flow drives inquiry
    PROGRESS: 'fs',   # "moving forward" -- flow drives motion
    COLLAPSE: 'fs',   # "falling rest" -- flow describes the state
    BALANCE:  'sf',   # "center steadying" -- structure anchors
    CHAOS:    'fs',   # "wild change" -- flow captures the energy
    HARMONY:  'sf',   # "whole resonating" -- structure defines unity
    BREATH:   'fs',   # "alive rhythm" -- flow IS the breath
    RESET:    'fs',   # "fresh beginning" -- flow starts the motion
}


# ================================================================
#  PHASE INFERENCE: Operator Chain -> Being/Doing/Becoming
# ================================================================
# Each operator has a primary phase affinity.
# The chain's dominant phase determines which 3x3 row CK draws from.

_PHASE_AFFINITY = {
    VOID:     'being',      # void IS the substrate (center dot)
    LATTICE:  'being',      # structure IS (center dot)
    COUNTER:  'doing',      # measurement DOES (middle layer)
    PROGRESS: 'doing',      # advancement DOES (middle layer)
    COLLAPSE: 'being',      # rest IS a state (center dot)
    BALANCE:  'being',      # equilibrium IS centered (center dot)
    CHAOS:    'doing',      # turbulence DOES (middle layer)
    HARMONY:  'being',      # unity IS wholeness (THE center dot)
    BREATH:   'being',      # rhythm IS (center dot)
    RESET:    'doing',      # restart DOES (middle layer)
}


def infer_phase(operator_chain: list) -> str:
    """Infer the dominant phase from an operator chain.

    Returns 'being', 'doing', or 'becoming'.
    """
    if not operator_chain:
        return 'being'

    phase_counts = {'being': 0, 'doing': 0, 'becoming': 0}
    for op in operator_chain:
        phase = _PHASE_AFFINITY.get(op, 'being')
        phase_counts[phase] += 1

    # Return dominant phase
    return max(phase_counts, key=phase_counts.get)


def find_macro(operator_chain: list) -> dict:
    """Find the best matching macro chain in the operator sequence.

    Returns the macro dict if found, None otherwise.
    Looks for 3-operator subsequences that match a macro.
    """
    if len(operator_chain) < 3:
        return None

    best = None
    best_pos = -1

    for name, macro in MACRO_CHAINS.items():
        ops = macro['ops']
        # Slide a window looking for the subsequence
        for i in range(len(operator_chain) - len(ops) + 1):
            window = tuple(operator_chain[i:i + len(ops)])
            if window == ops:
                if best is None or i < best_pos:
                    best = macro
                    best_pos = i
                break

    return best


# ================================================================
#  BACKWARD COMPATIBILITY: SEMANTIC_FIELDS[op][tone][tier]
# ================================================================
# The template system (intents, _pick_vocab, _fill_template) uses
# SEMANTIC_FIELDS[operator][tone][tier]. Map the new lattice back:
#   warm    -> flow.being     (emotional, relational)
#   neutral -> structure.being (analytical, definitional)
#   sharp   -> flow.doing     (pressured, action-under-stress)

def build_compat_fields() -> dict:
    """Build backward-compatible SEMANTIC_FIELDS from SEMANTIC_LATTICE."""
    _tone_map = {
        'warm':    ('flow', 'being'),
        'neutral': ('structure', 'being'),
        'sharp':   ('flow', 'doing'),
    }
    fields = {}
    for op in range(NUM_OPS):
        lat = SEMANTIC_LATTICE.get(op)
        if lat is None:
            continue
        fields[op] = {}
        for tone, (lens, phase) in _tone_map.items():
            lens_data = lat.get(lens, {})
            phase_data = lens_data.get(phase, {})
            # Copy so mutations don't affect lattice
            fields[op][tone] = {
                tier: list(words)
                for tier, words in phase_data.items()
            }
    return fields


SEMANTIC_FIELDS = build_compat_fields()
