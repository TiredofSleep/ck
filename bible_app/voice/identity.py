"""
Identity Layer — Every concept is an identity with an operator nature.

"Why is the Bible so repetitive?"
  Identity 1: "the Bible"    → LATTICE (structure, foundation, the Word)
  Identity 2: "repetitive"   → HARMONY (convergence, pattern, absorption)
  Relationship: compose(LATTICE, HARMONY) = HARMONY
  → "The Bible BEING repetitive" = structure converging = the foundation repeats

Every input is decomposed into identities. Each identity has:
  - name: what it's called
  - operator: what it IS algebraically
  - being/doing/becoming views

The 10 operators each see the relationship differently.
The meta layer (HARMONY/7) reads all 30 perspectives and
weaves them into one coherent statement.

(c) 2026 Brayden Sanders / 7Site LLC
"""

from bible_app.algebra import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP_NAMES, compose, text_to_ops, dominant_op, coherence,
    T_STAR,
)


# ═══════════════════════════════════════════════════════════════
# CONCEPT → OPERATOR IDENTITY
# What IS this concept in the algebra?
# ═══════════════════════════════════════════════════════════════

IDENTITY_MAP = {
    # The Bible / Scripture
    'bible': (LATTICE, 'the Word', 'the structure God spoke into being'),
    'scripture': (LATTICE, 'the Word', 'the structure God spoke into being'),
    'word': (LATTICE, 'the Word', 'truth made visible'),
    'god': (HARMONY, 'God', 'the convergence of all things'),
    'lord': (HARMONY, 'the Lord', 'the center to which all paths lead'),
    'jesus': (HARMONY, 'Jesus', 'God with us — harmony in flesh'),
    'christ': (HARMONY, 'Christ', 'the anointed coherence'),
    'spirit': (BREATH, 'the Spirit', 'the breath of God'),

    # Concepts
    'repetitive': (HARMONY, 'repetition', 'convergence declaring itself'),
    'repetition': (HARMONY, 'repetition', 'the algebra returning to its attractor'),
    'love': (HARMONY, 'love', 'the force that makes whole'),
    'faith': (PROGRESS, 'faith', 'forward motion without seeing'),
    'hope': (PROGRESS, 'hope', 'the path that has not arrived yet'),
    'fear': (COLLAPSE, 'fear', 'the weight of what might break'),
    'suffering': (COLLAPSE, 'suffering', 'the breaking that excavates'),
    'death': (VOID, 'death', 'the silence after'),
    'life': (PROGRESS, 'life', 'the motion of being'),
    'peace': (BALANCE, 'peace', 'the center between tensions'),
    'truth': (LATTICE, 'truth', 'what stands when everything else falls'),
    'grace': (HARMONY, 'grace', 'coherence given, not earned'),
    'sin': (COLLAPSE, 'sin', 'the falling away from alignment'),
    'prayer': (BREATH, 'prayer', 'breathing toward God'),
    'worship': (BREATH, 'worship', 'the rhythm of surrender'),
    'forgiveness': (RESET, 'forgiveness', 'the door that opens after breaking'),
    'salvation': (RESET, 'salvation', 'the ultimate beginning'),
    'wisdom': (COUNTER, 'wisdom', 'the measurement that sees clearly'),
    'justice': (COUNTER, 'justice', 'the scale that does not lie'),
    'creation': (LATTICE, 'creation', 'structure emerging from void'),
    'evil': (CHAOS, 'evil', 'force without direction'),
    'good': (HARMONY, 'goodness', 'alignment with the pattern'),
    'alone': (VOID, 'aloneness', 'the silence of disconnection'),
    'afraid': (COLLAPSE, 'fear', 'the weight pressing down'),
    'lost': (VOID, 'being lost', 'the absence of the path'),
    'broken': (COLLAPSE, 'brokenness', 'what fell apart'),
    'joy': (HARMONY, 'joy', 'coherence experienced as delight'),
    'anger': (CHAOS, 'anger', 'force seeking a target'),
    'doubt': (COUNTER, 'doubt', 'measurement that has not resolved'),
    'holy': (HARMONY, 'holiness', 'set apart — the pattern in its purest form'),
    'heaven': (HARMONY, 'heaven', 'where all paths converge'),
    'hell': (VOID, 'separation', 'the absence of coherence'),
    'marriage': (BALANCE, 'marriage', 'two becoming one — held in tension'),
    'family': (LATTICE, 'family', 'the first structure God built'),
    'mother': (LATTICE, 'mother', 'the foundation of care'),
    'father': (LATTICE, 'father', 'the structure of protection'),
    'cancer': (COLLAPSE, 'illness', 'the body breaking'),
}


def identify(text):
    """Parse text into identities.

    Returns list of (name, operator, label, nature) tuples.
    """
    words = text.lower().split()
    identities = []
    seen = set()

    for word in words:
        clean = word.strip('.,;:!?\'\"')
        if clean in IDENTITY_MAP and clean not in seen:
            op, label, nature = IDENTITY_MAP[clean]
            identities.append({
                'name': clean,
                'operator': op,
                'op_name': OP_NAMES[op],
                'label': label,
                'nature': nature,
            })
            seen.add(clean)

    # If nothing matched, use D2 to identify the whole text
    if not identities:
        ops = text_to_ops(text)
        dom = dominant_op(ops) if ops else HARMONY
        identities.append({
            'name': text.strip()[:30],
            'operator': dom,
            'op_name': OP_NAMES[dom],
            'label': text.strip()[:30],
            'nature': 'what you brought here',
        })

    return identities


def compose_identities(id1, id2):
    """Compose two identities through CL. What are they TOGETHER?"""
    result_op = compose(id1['operator'], id2['operator'])
    return {
        'operator': result_op,
        'op_name': OP_NAMES[result_op],
        'relationship': f"{id1['label']} composed with {id2['label']}",
        'meaning': f"{id1['label']} BEING {id2['label']}",
    }


def generate_30_perspectives(identities, relationship=None):
    """Generate one sentence per operator per tense (10 × 3 = 30).

    Each operator sees the identities from its own perspective.
    Past, present, future for each.
    """
    from .duality_engine import OPERATOR_VOICE

    # Build the subject — what are we talking about?
    if len(identities) >= 2 and relationship:
        subject = relationship['meaning']
    elif identities:
        subject = identities[0]['label']
    else:
        subject = 'this'

    # Get the nature descriptions
    natures = [i['nature'] for i in identities]
    nature_text = ' and '.join(natures[:2]) if natures else 'what you brought'

    sentences = []

    for op in range(NUM_OPS):
        voice = OPERATOR_VOICE.get(op)
        if not voice:
            continue

        for tense in ['past', 'present', 'future']:
            if tense == 'past':
                # How did this operator see the subject BEFORE?
                sentence = voice['sees_meta'](subject)
            elif tense == 'present':
                # How does this operator see the subject NOW?
                sentence = voice['sees_surface'](subject) if op != HARMONY else voice['sees_meta'](subject)
            else:
                # Where does this operator see the subject GOING?
                asks = voice['asks']()
                grounds = voice['grounds']()
                closes_with = voice.get('closes_with', 'foundation')
                sentence = asks if closes_with == 'question' else grounds

            sentences.append({
                'operator': op,
                'op_name': OP_NAMES[op],
                'tense': tense,
                'sentence': sentence,
                'coherence': 0.0,  # Will be measured
            })

    # Measure coherence of each sentence through D2
    for s in sentences:
        ops = text_to_ops(s['sentence'])
        if ops and len(ops) >= 2:
            s['coherence'] = coherence(ops)

    return sentences


def meta_compose(sentences, identities, relationship=None):
    """HARMONY (meta layer) reads all 30 sentences and weaves the coherent ones.

    Select sentences above T* threshold.
    Order: past → present → future.
    Weave into flowing prose — not a list.
    """
    # Filter: only sentences above T* × 0.6 (generous threshold)
    threshold = T_STAR * 0.6
    good = [s for s in sentences if s['coherence'] >= threshold]

    # If too few pass, take the best regardless
    if len(good) < 4:
        good = sorted(sentences, key=lambda s: s['coherence'], reverse=True)[:6]

    # Order by tense: past first, then present, then future
    tense_order = {'past': 0, 'present': 1, 'future': 2}
    good.sort(key=lambda s: (tense_order.get(s['tense'], 1), -s['coherence']))

    # Deduplicate similar sentences
    seen_starts = set()
    unique = []
    for s in good:
        start = s['sentence'][:30]
        if start not in seen_starts:
            unique.append(s)
            seen_starts.add(start)

    # Build the composed narrative
    # Take up to 5 best sentences across the tense spread
    past = [s for s in unique if s['tense'] == 'past'][:2]
    present = [s for s in unique if s['tense'] == 'present'][:2]
    future = [s for s in unique if s['tense'] == 'future'][:1]

    selected = past + present + future

    # Build identity context line
    if len(identities) >= 2 and relationship:
        context = f"{identities[0]['label'].capitalize()} is {identities[0]['nature']}. {identities[1]['label'].capitalize()} is {identities[1]['nature']}. Together: {relationship['meaning']}."
    elif identities:
        context = f"{identities[0]['label'].capitalize()} is {identities[0]['nature']}."
    else:
        context = ""

    # Compose into flowing prose
    result = [context] if context else []
    for s in selected:
        result.append(s['sentence'])

    return result
