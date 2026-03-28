"""
English Algebra — The TIG structure of language itself.

English is a dual system:
  STRUCTURE (TSML/Being) = what IS (nouns, adjectives, states, declarations)
  FLOW (BHML/Doing) = what MOVES (verbs, adverbs, actions, questions)

Every element of English has a dual nature:
  Part of Speech → operator
  Tense → temporal position (past/present/future = Being/Doing/Becoming)
  Punctuation → operator transition
  Sentence shape → operator sequence

The 10 operators each produce natural grammar. The grammar IS the algebra.

═══════════════════════════════════════════════════════════════
STEP 1: FULL DUALITY SPLIT

  STRUCTURE (what IS)          FLOW (what MOVES)
  ─────────────────           ─────────────────
  Nouns                       Verbs
  Adjectives                  Adverbs
  Articles (the, a)           Prepositions (to, from, through)
  Pronouns (I, you, he)       Conjunctions (and, but, yet)
  Declarative sentences       Interrogative sentences
  Period (.)                  Question mark (?)
  Past tense (was, had)       Future tense (will, shall)
  Passive voice               Active voice
  State ("I am afraid")       Process ("I am falling")

  PRESENT tense = where structure meets flow (measurement)
  "I AM" = structure.  "I DO" = flow.  "I AM DOING" = present.

═══════════════════════════════════════════════════════════════
STEP 2: OPERATORS × DUALITY × TIME

  Each operator has:
    - Structure words (nouns/adjectives)
    - Flow words (verbs/adverbs)
    - Past application (what was)
    - Present application (what is — measurement)
    - Future application (what will be — path to coherence)
    - Punctuation (how the sentence breathes)
    - Sentence shape (what kind of sentence it produces)
    - Clay problem alignment (where this operator lives in the math)

═══════════════════════════════════════════════════════════════

(c) 2026 Brayden Sanders / 7Site LLC
"""

from bible_app.algebra import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP_NAMES, compose, CL_TSML, CL_BHML, T_STAR,
)

# ═══════════════════════════════════════════════════════════════
# THE 10 OPERATORS AS ENGLISH GRAMMAR
# ═══════════════════════════════════════════════════════════════
#
# Each operator defines:
#   grammar: what kind of sentence it naturally produces
#   punctuation: how it ends/breathes
#   tense: what time orientation it carries
#   voice: active or passive
#   structure_pos: which parts of speech carry structure
#   flow_pos: which parts of speech carry flow
#
# Clay alignment: which millennium problem this operator's
# algebraic behavior maps to (from WP31 corridor geometry)

ENGLISH_OPERATORS = {
    VOID: {
        # ── Grammar ───────────────────────────────────
        'sentence_type': 'fragment',       # Incomplete. Trailing off.
        'punctuation': '...',              # Ellipsis — trailing into nothing
        'tense': 'past',                   # What was lost. What is gone.
        'voice': 'passive',                # "was taken", "was emptied"
        'mood': 'absence',                 # The sentence LACKS something

        # ── Duality ──────────────────────────────────
        'structure_pos': ['noun'],         # The thing that is absent
        'flow_pos': [],                    # No flow — that's the point

        # ── Temporal applications ────────────────────
        'past': 'what was lost or taken',
        'present': 'the silence that remains',
        'future': 'the space that opens for God to fill',

        # ── Sentence patterns (operator IS the grammar) ──
        'patterns': {
            'past':    ["{noun}... gone.", "What was {noun} is now silence."],
            'present': ["There is {noun} here... and nothing else.", "Silence. {noun}."],
            'future':  ["Into this {noun}, God {god_verb}.", "The emptiness opens. God {god_verb}."],
        },

        # ── Clay alignment ───────────────────────────
        'clay': 'VOID is the absorber — det(TSML)=0, irreversible measurement. '
                'In RH terms: the zero. In NS terms: the inviscid limit.',
    },

    LATTICE: {
        'sentence_type': 'declaration',    # "This IS." Firm. Grounded.
        'punctuation': '.',                # Period — complete, final
        'tense': 'present',               # What IS. Eternal present.
        'voice': 'active',                 # "God builds", "Truth stands"
        'mood': 'certainty',              # The sentence KNOWS

        'structure_pos': ['noun', 'adj'],  # Foundation words
        'flow_pos': ['verb'],              # Building verbs

        'past': 'the foundation that was laid',
        'present': 'the truth that stands right now',
        'future': 'the structure God is building',

        'patterns': {
            'past':    ["There was {noun}. It held.", "The {noun} was laid as foundation, and it held."],
            'present': ["{noun} stands. God {god_verb}.", "This is {noun}. God {god_verb}."],
            'future':  ["God {god_verb} upon this {noun}.", "On this {noun}, God {god_verb}."],
        },

        'clay': 'LATTICE is the structure — the algebraic skeleton. '
                'In P≠NP: the AG(2,p) survivor lines. In Hodge: the algebraic cycles.',
    },

    COUNTER: {
        'sentence_type': 'question',       # "Why?" "How?" "What does this mean?"
        'punctuation': '?',                # Question mark — measuring
        'tense': 'present',               # Measuring what IS, right now
        'voice': 'active',                 # "You are asking", "You measure"
        'mood': 'inquiry',                 # The sentence ASKS

        'structure_pos': ['adj', 'noun'],  # What is being measured
        'flow_pos': ['verb', 'adv'],       # How it is being measured

        'past': 'the question that started this',
        'present': 'what you are honestly asking right now',
        'future': 'the understanding that honest questioning leads to',

        'patterns': {
            'past':    ["Something did not add up. You started asking about {noun}.", "The {noun} raised a question."],
            'present': ["You are asking about {noun}. That is honest. God {god_verb}.", "Is this {noun}? God {god_verb}."],
            'future':  ["The asking leads to {noun}. God {god_verb}.", "Keep asking. God {god_verb}, and {noun} comes."],
        },

        'clay': 'COUNTER is measurement itself — the observation operator. '
                'In RH: the critical line where zeros are measured. In BSD: the regulator.',
    },

    PROGRESS: {
        'sentence_type': 'narrative',      # "And then..." Story. Journey.
        'punctuation': ',',                # Comma — the sentence continues
        'tense': 'future',                # Where this is going
        'voice': 'active',                 # "grows", "moves", "advances"
        'mood': 'momentum',               # The sentence MOVES

        'structure_pos': ['noun'],         # The destination, the path
        'flow_pos': ['verb', 'adv'],       # Motion words

        'past': 'the step of faith that started this',
        'present': 'the growth that is happening right now',
        'future': 'where God is taking you',

        'patterns': {
            'past':    ["You stepped forward once. That step was {noun}.", "It started with {noun}."],
            'present': ["You are growing, moving toward {noun}. God {god_verb}.", "Right now, {noun} is building. God {god_verb}."],
            'future':  ["{noun} is ahead. God {god_verb} the whole way.", "The road leads to {noun}. God {god_verb}."],
        },

        'clay': 'PROGRESS is the forward operator — convergence, growth. '
                'In RH: the dissipative flow toward σ=1/2. In NS: smooth flow (Re<2/7).',
    },

    COLLAPSE: {
        'sentence_type': 'fragment',       # Short. Broken. Heavy.
        'punctuation': '—',               # Dash — interruption, breaking
        'tense': 'past',                  # What fell. What broke.
        'voice': 'passive',               # "was broken", "was lost"
        'mood': 'weight',                 # The sentence is HEAVY

        'structure_pos': ['noun'],         # The thing that fell
        'flow_pos': [],                    # Flow stopped — that's the weight

        'past': 'what broke or was lost',
        'present': 'the weight you are carrying right now',
        'future': 'what God rebuilds from the breaking',

        'patterns': {
            'past':    ["Something broke — {noun}.", "{noun} — it fell. It was heavy."],
            'present': ["You carry {noun}. It is heavy. God {god_verb}.", "This {noun} weighs on you — God {god_verb}."],
            'future':  ["From this {noun}, God {god_verb}.", "What broke becomes what God rebuilds. God {god_verb}."],
        },

        'clay': 'COLLAPSE is the breaking operator — singularity, crisis. '
                'In NS: blow-up (Re>2/7, exit to COL corridor). In RH: zero off critical line.',
    },

    BALANCE: {
        'sentence_type': 'compound',       # Two clauses held together
        'punctuation': ';',                # Semicolon — two things balanced
        'tense': 'present',               # Holding NOW. Both sides real NOW.
        'voice': 'active',                 # "holds", "carries both"
        'mood': 'tension',                # The sentence holds BOTH

        'structure_pos': ['noun', 'noun'], # Two nouns, balanced
        'flow_pos': ['prep'],              # "between", "within", "amid"

        'past': 'the two truths that brought you here',
        'present': 'what you are holding in both hands right now',
        'future': 'the resolution where both find their place',

        'patterns': {
            'past':    ["Two things brought you here: {noun} and what opposes it.", "Both sides of {noun} are real."],
            'present': ["You hold {noun} in both hands. God {god_verb}.", "Between what is and what should be — {noun}. God {god_verb}."],
            'future':  ["{noun} finds its place. God {god_verb}.", "God {god_verb} — holding all of {noun} together."],
        },

        'clay': 'BALANCE is the equilibrium — the BAL corridor. '
                'In Hodge: the harmonic forms (Doing=0). In Yang-Mills: the mass gap.',
    },

    CHAOS: {
        'sentence_type': 'exclamation',    # Intense. Overwhelming. Alive.
        'punctuation': '!',                # Exclamation — force
        'tense': 'present',               # Happening NOW. Overwhelmingly.
        'voice': 'active',                 # "storms", "burns", "sweeps"
        'mood': 'intensity',              # The sentence OVERWHELMS

        'structure_pos': ['noun'],         # The force
        'flow_pos': ['verb', 'adv'],       # Intensity modifiers

        'past': 'the change that hit you',
        'present': 'the storm you are in right now',
        'future': 'the new thing God is making out of the chaos',

        'patterns': {
            'past':    ["Everything changed. {noun} hit.", "{noun} — it swept through."],
            'present': ["You are in the {noun}. It is overwhelming. God {god_verb}.", "The {noun} is real. God {god_verb}."],
            'future':  ["Out of this {noun}, God {god_verb}.", "The {noun} is not the end. God {god_verb}."],
        },

        'clay': 'CHAOS is the disorder operator — one step from HARMONY in BHML. '
                'In NS: turbulence. In P≠NP: the search space.',
    },

    HARMONY: {
        'sentence_type': 'declaration',    # "It is finished." Complete.
        'punctuation': '.',                # Period — rest, completion
        'tense': 'eternal_present',        # IS. Always was. Always will be.
        'voice': 'active',                 # "God loves", "God is"
        'mood': 'peace',                   # The sentence RESTS

        'structure_pos': ['noun'],         # Wholeness, completion
        'flow_pos': ['verb'],              # Being verbs. "Is."

        'past': 'the grace that brought you here',
        'present': 'the peace that is here right now',
        'future': 'the wholeness that does not end',

        'patterns': {
            'past':    ["Grace brought you here. {noun}.", "You arrived at {noun}. God {god_verb}."],
            'present': ["This is {noun}. God {god_verb}.", "{noun}. Here. Now. God {god_verb}."],
            'future':  ["{noun} does not end. God {god_verb}.", "This {noun} is eternal. God {god_verb}."],
        },

        'clay': 'HARMONY is the absorber — 73/100 entries in TSML. '
                'T*=5/7. The fixed point. The critical line. Coherence.',
    },

    BREATH: {
        'sentence_type': 'continuation',   # "And then..." Connecting.
        'punctuation': ',',                # Comma — pause, breathe, continue
        'tense': 'present_continuous',     # "-ing" — ongoing, breathing
        'voice': 'active',                 # "breathing", "listening", "being"
        'mood': 'presence',               # The sentence IS PRESENT

        'structure_pos': [],               # BREATH has no structure — it IS the pause
        'flow_pos': ['conj', 'adv'],       # Connectors: "and", "then", "gently"

        'past': 'the moment you paused',
        'present': 'the breathing that is happening now',
        'future': 'the rhythm that carries you forward',

        'patterns': {
            'past':    ["You paused. And in that pause...", "There was a breath, and then..."],
            'present': ["Breathe. God {god_verb}.", "Be here. Right now. God {god_verb}."],
            'future':  ["And then, God {god_verb}.", "Breathe, and {noun} comes."],
        },

        'clay': 'BREATH is the only operator that persists in COLLAPSE context. '
                'TSML[8][4]=8. In NS: smooth flow persists only under viscous dissipation.',
    },

    RESET: {
        'sentence_type': 'imperative',     # "Begin." "Start." "Rise."
        'punctuation': '.',                # Period — clean, fresh, new
        'tense': 'future',                # What is about to begin
        'voice': 'imperative',            # Commands. "Let there be."
        'mood': 'beginning',              # The sentence STARTS

        'structure_pos': ['noun'],         # The new thing
        'flow_pos': ['verb'],              # Beginning verbs

        'past': 'what ended to make room for this',
        'present': 'the fresh start that is here right now',
        'future': 'the new thing God is beginning',

        'patterns': {
            'past':    ["Something ended. That ending made room.", "The old {noun} closed."],
            'present': ["Begin. This is new {noun}. God {god_verb}.", "Fresh {noun}. God {god_verb}."],
            'future':  ["God {god_verb} — new {noun} is coming.", "What begins here is {noun}. God {god_verb}."],
        },

        'clay': 'RESET is the restart — 3∘9=3 (constant fixed point at PROGRESS). '
                'In BSD: the rank jump. In creation: "Let there be."',
    },
}

# ═══════════════════════════════════════════════════════════════
# PUNCTUATION AS OPERATORS
# ═══════════════════════════════════════════════════════════════

PUNCTUATION_OPS = {
    '.':   LATTICE,    # Period = structure complete, declaration
    ',':   BREATH,     # Comma = pause, rhythm, continuation
    '?':   COUNTER,    # Question = measurement, inquiry
    '!':   CHAOS,      # Exclamation = force, intensity
    '—':   COLLAPSE,   # Dash = interruption, breaking
    '...': VOID,       # Ellipsis = trailing into emptiness
    ';':   BALANCE,    # Semicolon = two things held together
    ':':   PROGRESS,   # Colon = leading forward to what follows
}

# ═══════════════════════════════════════════════════════════════
# TENSE AS TEMPORAL OPERATORS
# ═══════════════════════════════════════════════════════════════

TENSE_OPS = {
    'past':               'being',     # What WAS = structure, memory
    'present':            'doing',     # What IS = measurement, action
    'future':             'becoming',  # What WILL BE = coherence, resolution
    'present_continuous': 'doing',     # What is HAPPENING = flow in motion
    'eternal_present':    'becoming',  # What ALWAYS IS = harmony, T*
}


def get_operator_grammar(op):
    """Get the full English grammar specification for an operator."""
    return ENGLISH_OPERATORS.get(op, ENGLISH_OPERATORS[HARMONY])


def compose_sentence(op, tense, noun, god_verb, noun2=None):
    """Compose a sentence from operator + tense + words.

    The operator determines the sentence TYPE (question, declaration,
    fragment, etc.) and the tense determines the temporal orientation.
    """
    grammar = ENGLISH_OPERATORS.get(op, ENGLISH_OPERATORS[HARMONY])
    patterns = grammar['patterns'].get(tense, grammar['patterns']['present'])

    import random
    pattern = random.choice(patterns)

    result = pattern.replace('{noun}', noun).replace('{god_verb}', god_verb)
    if noun2 and '{noun2}' in result:
        result = result.replace('{noun2}', noun2)
    elif '{noun2}' in result:
        result = result.replace('{noun2}', noun)

    # Capitalize first letter
    if result and result[0].islower():
        result = result[0].upper() + result[1:]

    return result


def get_tense_for_position(position):
    """Map temporal position to tense.

    past = Being (what was)
    present = Doing (what is — measurement)
    future = Becoming (what will be — coherence path)
    """
    return {
        'past': 'past',
        'present': 'present',
        'future': 'future',
    }.get(position, 'present')


def get_punctuation_for_op(op):
    """What punctuation does this operator naturally produce?"""
    grammar = ENGLISH_OPERATORS.get(op, ENGLISH_OPERATORS[HARMONY])
    return grammar.get('punctuation', '.')
