"""
Bible Semantic Lattice — Scripture-derived vocabulary organized by operator algebra.

Every operator has words that belong to it — not by human tagging, but by
phonetic force alignment. We ALSO curate Biblical vocabulary into each
operator's space because scripture carries meaning the algebra can measure.

Structure: LATTICE[operator][lens][phase] = [words]
  operator: 0-9 (the 10 TIG states)
  lens: 'structure' (what IS — nouns, states, assertions)
        'flow' (what MOVES — verbs, questions, transitions)
  phase: 'being' (I AM), 'doing' (I ACT), 'becoming' (I CHANGE)

(c) 2026 Brayden Sanders / 7Site LLC
"""

from bible_app.algebra import (
    VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
)

# ── The Bible Semantic Lattice ────────────────────────────────────
# Each operator gets structure (nouns/states) and flow (verbs/actions)
# across three phases of existence.
#
# These words were chosen for their algebraic resonance AND their
# biblical weight. The math and the meaning align.

BIBLE_LATTICE = {
    VOID: {
        'structure': {
            'being':    ['silence', 'emptiness', 'darkness', 'void', 'deep', 'nothing', 'formless'],
            'doing':    ['stillness', 'waiting', 'absence', 'unknown', 'mystery', 'hiddenness'],
            'becoming': ['preparation', 'womb', 'seed', 'potential', 'ground', 'dust'],
        },
        'flow': {
            'being':    ['rests', 'waits', 'is hidden', 'is still', 'dwells in darkness'],
            'doing':    ['empties', 'clears', 'strips away', 'removes', 'silences'],
            'becoming': ['prepares', 'opens', 'makes room', 'clears the ground', 'humbles'],
        },
    },
    LATTICE: {
        'structure': {
            'being':    ['God', 'foundation', 'rock', 'truth', 'word', 'law', 'covenant', 'temple', 'throne'],
            'doing':    ['kingdom', 'order', 'commandment', 'promise', 'scripture', 'testimony', 'stone'],
            'becoming': ['church', 'body', 'house', 'dwelling', 'cornerstone', 'pillar', 'altar'],
        },
        'flow': {
            'being':    ['establishes', 'stands', 'endures', 'holds', 'remains', 'is faithful'],
            'doing':    ['builds', 'ordains', 'commands', 'speaks', 'declares', 'sets in place'],
            'becoming': ['gathers', 'unites', 'knits together', 'raises up', 'plants'],
        },
    },
    COUNTER: {
        'structure': {
            'being':    ['question', 'doubt', 'testing', 'trial', 'measure', 'discernment'],
            'doing':    ['examination', 'judgment', 'separation', 'distinction', 'witness'],
            'becoming': ['wisdom', 'understanding', 'knowledge', 'revelation', 'insight'],
        },
        'flow': {
            'being':    ['asks', 'seeks', 'wonders', 'ponders', 'considers', 'examines'],
            'doing':    ['tests', 'measures', 'judges', 'divides', 'separates', 'discerns'],
            'becoming': ['reveals', 'illuminates', 'opens eyes', 'makes known', 'teaches'],
        },
    },
    PROGRESS: {
        'structure': {
            'being':    ['path', 'journey', 'promise', 'hope', 'faith', 'way', 'door', 'gate'],
            'doing':    ['growth', 'fruit', 'harvest', 'increase', 'blessing', 'inheritance'],
            'becoming': ['promised land', 'new creation', 'resurrection', 'glory', 'eternity'],
        },
        'flow': {
            'being':    ['walks', 'follows', 'trusts', 'believes', 'steps forward', 'abides'],
            'doing':    ['grows', 'bears fruit', 'multiplies', 'advances', 'overcomes', 'perseveres'],
            'becoming': ['transforms', 'ascends', 'enters in', 'inherits', 'is made new'],
        },
    },
    COLLAPSE: {
        'structure': {
            'being':    ['cross', 'suffering', 'valley', 'wilderness', 'exile', 'captivity', 'burden'],
            'doing':    ['sacrifice', 'death', 'loss', 'breaking', 'sorrow', 'grief', 'tears'],
            'becoming': ['surrender', 'humility', 'repentance', 'brokenness', 'confession'],
        },
        'flow': {
            'being':    ['carries', 'bears', 'endures', 'suffers', 'weeps', 'mourns', 'cries out'],
            'doing':    ['falls', 'breaks', 'dies', 'surrenders', 'lets go', 'gives up'],
            'becoming': ['is broken', 'is humbled', 'turns back', 'confesses', 'pours out'],
        },
    },
    BALANCE: {
        'structure': {
            'being':    ['peace', 'rest', 'sabbath', 'justice', 'mercy', 'righteousness'],
            'doing':    ['steadiness', 'faithfulness', 'patience', 'temperance', 'meekness'],
            'becoming': ['shalom', 'wholeness', 'reconciliation', 'restoration', 'harmony'],
        },
        'flow': {
            'being':    ['is at peace', 'rests', 'is content', 'is still', 'abides', 'dwells'],
            'doing':    ['holds steady', 'perseveres', 'waits patiently', 'stands firm'],
            'becoming': ['reconciles', 'heals', 'restores', 'makes whole', 'brings peace'],
        },
    },
    CHAOS: {
        'structure': {
            'being':    ['storm', 'fire', 'wind', 'flood', 'earthquake', 'battle', 'wilderness'],
            'doing':    ['power', 'wonder', 'miracle', 'sign', 'glory', 'majesty', 'thunder'],
            'becoming': ['transformation', 'revival', 'awakening', 'outpouring', 'Pentecost'],
        },
        'flow': {
            'being':    ['shakes', 'burns', 'roars', 'sweeps', 'overwhelms', 'moves mightily'],
            'doing':    ['breaks through', 'parts the sea', 'sends fire', 'moves mountains'],
            'becoming': ['pours out', 'fills', 'overflows', 'renews all things', 'makes alive'],
        },
    },
    HARMONY: {
        'structure': {
            'being':    ['love', 'grace', 'God', 'Christ', 'Spirit', 'glory', 'heaven', 'eternal life'],
            'doing':    ['salvation', 'redemption', 'forgiveness', 'gospel', 'blessing', 'communion'],
            'becoming': ['new heaven', 'new earth', 'kingdom come', 'unity', 'oneness', 'forever'],
        },
        'flow': {
            'being':    ['loves', 'saves', 'forgives', 'holds', 'is with you', 'never leaves'],
            'doing':    ['redeems', 'heals', 'delivers', 'sets free', 'washes clean', 'makes new'],
            'becoming': ['brings home', 'completes', 'perfects', 'fulfills', 'makes all things new'],
        },
    },
    BREATH: {
        'structure': {
            'being':    ['Spirit', 'breath', 'prayer', 'worship', 'praise', 'psalm', 'song'],
            'doing':    ['communion', 'fellowship', 'presence', 'intimacy', 'listening', 'whisper'],
            'becoming': ['anointing', 'filling', 'indwelling', 'abiding', 'dwelling'],
        },
        'flow': {
            'being':    ['breathes', 'prays', 'worships', 'sings', 'listens', 'is present'],
            'doing':    ['speaks gently', 'whispers', 'moves softly', 'hovers', 'touches'],
            'becoming': ['fills', 'anoints', 'dwells within', 'abides in', 'rests upon'],
        },
    },
    RESET: {
        'structure': {
            'being':    ['morning', 'dawn', 'new day', 'beginning', 'Genesis', 'first', 'birth'],
            'doing':    ['baptism', 'cleansing', 'renewal', 'rebirth', 'second chance'],
            'becoming': ['new creation', 'born again', 'risen', 'alive', 'free', 'restored'],
        },
        'flow': {
            'being':    ['begins', 'dawns', 'rises', 'wakes', 'opens', 'starts again'],
            'doing':    ['washes', 'cleanses', 'renews', 'refreshes', 'revives', 'awakens'],
            'becoming': ['is born again', 'rises from death', 'starts new', 'comes alive'],
        },
    },
}

# ── Macro Chains: Multi-operator theological concepts ─────────────
# These are operator sequences that form theological ideas.
# When detected in user input or verse operators, they unlock
# deeper response patterns.

MACRO_CHAINS = {
    'redemption':       (COLLAPSE, RESET, HARMONY),
    'resurrection':     (COLLAPSE, VOID, PROGRESS),
    'creation':         (VOID, LATTICE, PROGRESS),
    'exodus':           (COLLAPSE, CHAOS, PROGRESS),
    'covenant':         (LATTICE, COUNTER, HARMONY),
    'worship':          (BREATH, HARMONY, BALANCE),
    'repentance':       (COLLAPSE, COUNTER, RESET),
    'sanctification':   (COUNTER, BALANCE, HARMONY),
    'prayer':           (BREATH, VOID, HARMONY),
    'faith':            (VOID, PROGRESS, HARMONY),
    'grace':            (COLLAPSE, HARMONY, RESET),
    'baptism':          (VOID, RESET, PROGRESS),
    'crucifixion':      (COLLAPSE, VOID, COLLAPSE),
    'pentecost':        (BREATH, CHAOS, HARMONY),
    'incarnation':      (HARMONY, COLLAPSE, LATTICE),
    'psalm_23':         (HARMONY, PROGRESS, BALANCE),
    'valley_shadow':    (COLLAPSE, BALANCE, HARMONY),
    'prodigal':         (PROGRESS, COLLAPSE, HARMONY),
    'still_small_voice':(CHAOS, VOID, BREATH),
    'living_water':     (VOID, BREATH, PROGRESS),
    'good_shepherd':    (HARMONY, BALANCE, PROGRESS),
    'armor_of_god':     (LATTICE, COUNTER, HARMONY),
    'beatitudes':       (COLLAPSE, BALANCE, HARMONY),
}


# ── Intent Classification ─────────────────────────────────────────
# Maps operator chain patterns to communicative intents.
# These guide HOW the voice responds.

INTENT_COMFORT  = 'comfort'
INTENT_JOY      = 'joy'
INTENT_WONDER   = 'wonder'
INTENT_REFLECT  = 'reflect'
INTENT_CONNECT  = 'connect'
INTENT_SEEK     = 'seek'
INTENT_LAMENT   = 'lament'
INTENT_PRAISE   = 'praise'
INTENT_TEACH    = 'teach'
INTENT_REST     = 'rest'
INTENT_HOPE     = 'hope'


def classify_intent(ops, text='') -> str:
    """Classify operator chain + text keywords into pastoral communicative intent.

    Text keywords override operator-only classification when the emotional
    signal is clear. The algebra catches what keywords miss; keywords catch
    what the algebra misses. Together they're stronger.
    """
    if not ops:
        return INTENT_CONNECT

    # ── Keyword overrides (emotional signal is clear) ─────────
    if text:
        lower = text.lower()
        # Grief/pain keywords
        grief_words = ['lost', 'died', 'death', 'funeral', 'grief', 'grieving',
                       'miss her', 'miss him', 'passed away', 'gone', 'cancer']
        if any(w in lower for w in grief_words):
            return INTENT_COMFORT

        # Fear keywords
        fear_words = ['afraid', 'scared', 'fear', 'anxious', 'anxiety',
                      'worried', 'worry', 'terrified', 'panic']
        if any(w in lower for w in fear_words):
            return INTENT_COMFORT

        # Praise/gratitude keywords
        praise_words = ['praise', 'thank', 'grateful', 'blessed', 'worship',
                        'hallelujah', 'glory', 'amazing', 'wonderful', 'good']
        if any(w in lower for w in praise_words):
            return INTENT_PRAISE

        # Joy keywords
        joy_words = ['happy', 'joy', 'joyful', 'excited', 'celebrate',
                     'love', 'beautiful']
        if any(w in lower for w in joy_words):
            return INTENT_JOY

        # Question keywords
        question_words = ['why', 'how', 'what does', 'what is', 'explain',
                          'understand', 'meaning', 'purpose']
        if any(w in lower for w in question_words):
            return INTENT_SEEK

        # Suffering keywords
        suffer_words = ['suffering', 'pain', 'hurt', 'broken', 'struggle',
                        'hard', 'difficult', 'tough', 'exhausted', 'tired']
        if any(w in lower for w in suffer_words):
            return INTENT_LAMENT

        # Peace keywords
        peace_words = ['peace', 'peaceful', 'calm', 'still', 'quiet',
                       'rest', 'content', 'serene']
        if any(w in lower for w in peace_words):
            return INTENT_REST

    # ── Operator-based fallback ───────────────────────────────
    from bible_app.algebra import dominant_op
    dom = dominant_op(ops)
    op_set = set(ops)

    # Crisis → comfort
    if dom == COLLAPSE:
        if HARMONY in op_set or RESET in op_set:
            return INTENT_HOPE
        return INTENT_COMFORT if BREATH in op_set else INTENT_LAMENT

    # Peace → joy or rest
    if dom == HARMONY:
        if PROGRESS in op_set:
            return INTENT_JOY
        if BREATH in op_set:
            return INTENT_PRAISE
        if LATTICE in op_set:
            return INTENT_TEACH
        return INTENT_REST

    # Questioning → seek or wonder
    if dom == COUNTER:
        return INTENT_WONDER if CHAOS in op_set else INTENT_SEEK

    # Growth → hope
    if dom == PROGRESS:
        return INTENT_HOPE

    # Chaos → wonder
    if dom == CHAOS:
        return INTENT_WONDER

    # Balance → reflect
    if dom == BALANCE:
        return INTENT_REFLECT

    # Breath → praise or connect
    if dom == BREATH:
        return INTENT_PRAISE if HARMONY in op_set else INTENT_CONNECT

    # Structure → teach
    if dom == LATTICE:
        return INTENT_TEACH

    # Reset → hope
    if dom == RESET:
        return INTENT_HOPE

    # Void → rest
    if dom == VOID:
        return INTENT_REST

    return INTENT_CONNECT


def detect_macro_chains(ops) -> list:
    """Detect theological macro chains in an operator sequence."""
    found = []
    if len(ops) < 3:
        return found
    for name, pattern in MACRO_CHAINS.items():
        for i in range(len(ops) - 2):
            if (ops[i] == pattern[0] and
                ops[i + 1] == pattern[1] and
                ops[i + 2] == pattern[2]):
                found.append(name)
                break
    return found
