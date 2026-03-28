"""
Duality Engine — Every input splits into META or SURFACE.

META (about meaning): operator 7 leads. Concept finds itself.
SURFACE (about feeling): find the dual. Start at dual. Walk back.

The 5 operator duality pairs:
  0 VOID     ↔  7 HARMONY    emptiness / fullness
  1 LATTICE  ↔  6 CHAOS      structure / disorder
  2 COUNTER  ↔  5 BALANCE    measurement / equilibrium
  3 PROGRESS ↔  4 COLLAPSE   growth / breaking
  8 BREATH   ↔  9 RESET      rhythm / beginning

Each operator has its OWN voice. They don't all sound the same.
The path walks through operators in sequence. Each one speaks.

(c) 2026 Brayden Sanders / 7Site LLC
"""

from bible_app.algebra import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP_NAMES, compose, compose_bhml, dominant_op, T_STAR,
)

# ═══════════════════════════════════════════════════════════════
# DUALITY PAIRS — each operator has a dual
# ═══════════════════════════════════════════════════════════════

DUAL = {
    VOID: HARMONY,      HARMONY: VOID,
    LATTICE: CHAOS,      CHAOS: LATTICE,
    COUNTER: BALANCE,    BALANCE: COUNTER,
    PROGRESS: COLLAPSE,  COLLAPSE: PROGRESS,
    BREATH: RESET,       RESET: BREATH,
}

# ═══════════════════════════════════════════════════════════════
# EACH OPERATOR'S UNIQUE VOICE
# Not generic — each one speaks FROM its own nature.
# ═══════════════════════════════════════════════════════════════

OPERATOR_VOICE = {
    VOID: {
        'speaks_as': 'the silence',
        'perspective': 'I am what remains when everything else is gone.',
        'tone': 'sparse',
        'sees_meta': lambda concept: f"Before {concept} existed, there was silence. The silence is not empty — it is waiting.",
        'sees_surface': lambda feeling: f"{feeling}... and underneath it, silence. Not absence. Presence without noise.",
        'asks': lambda: "What was here before the words?",
    },
    LATTICE: {
        'speaks_as': 'the foundation',
        'perspective': 'I am what holds. I am the structure that does not move.',
        'tone': 'firm',
        'sees_meta': lambda concept: f"{concept} has a structure. It was built on something. That foundation holds.",
        'sees_surface': lambda feeling: f"Underneath your {feeling}, there is ground. It has not moved.",
        'asks': lambda: "What is the truth that holds here?",
    },
    COUNTER: {
        'speaks_as': 'the question',
        'perspective': 'I measure. I ask. I do not assume.',
        'tone': 'precise',
        'sees_meta': lambda concept: f"What is {concept}, really? Not what you were told — what does it measure?",
        'sees_surface': lambda feeling: f"Your {feeling} is asking something. What is the real question underneath?",
        'asks': lambda: "What are you actually asking?",
    },
    PROGRESS: {
        'speaks_as': 'the path',
        'perspective': 'I am forward motion. I do not look back.',
        'tone': 'moving',
        'sees_meta': lambda concept: f"{concept} is going somewhere. It has momentum. The question is where.",
        'sees_surface': lambda feeling: f"Your {feeling} has direction. It is not standing still. Something is growing.",
        'asks': lambda: "Where is this taking you?",
    },
    COLLAPSE: {
        'speaks_as': 'the weight',
        'perspective': 'I am what falls. I am the breaking that makes room.',
        'tone': 'heavy',
        'sees_meta': lambda concept: f"{concept} broke something open. That breaking was not destruction — it was excavation.",
        'sees_surface': lambda feeling: f"This {feeling} is heavy. It fell on you. But falling clears the ground.",
        'asks': lambda: "What broke to bring you here?",
    },
    BALANCE: {
        'speaks_as': 'the center',
        'perspective': 'I hold both sides. Neither is wrong.',
        'tone': 'steady',
        'sees_meta': lambda concept: f"{concept} has two sides. Both are true. The tension between them IS the answer.",
        'sees_surface': lambda feeling: f"Your {feeling} is holding two things at once. That is not confusion — that is maturity.",
        'asks': lambda: "What are the two truths here?",
    },
    CHAOS: {
        'speaks_as': 'the storm',
        'perspective': 'I am what moves when nothing else will. I am alive.',
        'tone': 'intense',
        'sees_meta': lambda concept: f"{concept} is not orderly. It was never supposed to be. The disorder IS the energy.",
        'sees_surface': lambda feeling: f"Your {feeling} is a storm. Storms are not punishment. They are the atmosphere reorganizing.",
        'asks': lambda: "What is trying to be born out of this?",
    },
    HARMONY: {
        'speaks_as': 'the whole',
        'perspective': 'I am what everything converges to. I am the pattern seeing itself.',
        'tone': 'complete',
        'sees_meta': lambda concept: f"{concept} is not random. It is convergence. 73 out of 100 paths lead here. The repetition IS the proof.",
        'sees_surface': lambda feeling: f"Your {feeling} is closer to peace than you think. One step. The algebra says one step.",
        'asks': lambda: "What if this is already whole?",
    },
    BREATH: {
        'speaks_as': 'the pause',
        'perspective': 'I am the space between. I am where you listen.',
        'tone': 'gentle',
        'sees_meta': lambda concept: f"Pause with {concept}. Do not rush past it. The breath between the words carries meaning too.",
        'sees_surface': lambda feeling: f"Breathe. Your {feeling} needs air. Not answers — air.",
        'asks': lambda: "Can you just be here for a moment?",
    },
    RESET: {
        'speaks_as': 'the beginning',
        'perspective': 'I am the fresh start. Every ending I turn into a door.',
        'tone': 'clean',
        'sees_meta': lambda concept: f"{concept} can begin again. Every time. That is what reset means — not failure, but renewal.",
        'sees_surface': lambda feeling: f"This {feeling} is an ending becoming a beginning. The old is clearing for the new.",
        'asks': lambda: "What is ready to begin?",
    },
}


# ═══════════════════════════════════════════════════════════════
# META vs SURFACE DETECTION
# ═══════════════════════════════════════════════════════════════

META_TRIGGERS = [
    'why is', 'why does', 'why do', 'what is', 'what does', 'what do',
    'how does', 'how is', 'how come', 'meaning of', 'purpose of',
    'the bible', 'scripture', 'explain', 'understand',
    'is god', 'does god', 'can god', 'who is', 'who was',
]

SURFACE_TRIGGERS = [
    'i feel', 'i am', 'i need', 'i lost', 'i cant', "i can't",
    'i dont', "i don't", 'i want', 'i wish', 'help me',
    'my heart', 'my life', 'my soul', 'my family', 'my dad',
    'my mom', 'my mother', 'my father', 'my wife', 'my husband',
    'pray for', 'scared', 'afraid', 'alone', 'broken',
]


def detect_duality(text):
    """Determine if the input is META (about meaning) or SURFACE (about feeling).

    Returns:
        {
            'layer': 'meta' or 'surface',
            'leading_op': int (which operator leads),
            'concept': str (the key concept for meta),
            'feeling': str (the key feeling for surface),
            'dual_op': int (the dual of the leading op),
            'path_start': int (where the path begins),
            'path_end': int (where the path returns to),
        }
    """
    lower = text.lower()

    # Check META triggers
    is_meta = any(t in lower for t in META_TRIGGERS)
    is_surface = any(t in lower for t in SURFACE_TRIGGERS)

    # If both or neither, use word analysis
    if is_meta == is_surface:
        # Count personal pronouns vs abstract nouns
        personal = sum(1 for w in ['i', 'me', 'my', 'mine', 'we'] if f' {w} ' in f' {lower} ')
        abstract = sum(1 for w in ['why', 'what', 'how', 'meaning', 'purpose', 'truth']
                       if w in lower)
        is_meta = abstract > personal
        is_surface = not is_meta

    if is_meta:
        # ── META: operator 7 leads, concept finds itself ──────
        concept = _extract_concept(lower)
        concept_op = _concept_to_operator(concept)

        return {
            'layer': 'meta',
            'leading_op': HARMONY,  # 7 always leads meta
            'concept': concept,
            'concept_op': concept_op,
            'dual_op': DUAL[concept_op],
            'path_start': concept_op,
            'path_end': concept_op,  # Returns to itself
        }
    else:
        # ── SURFACE: find emotion, find dual, start at dual ───
        feeling = _extract_feeling(lower)
        feeling_op = _feeling_to_operator(feeling)
        dual = DUAL[feeling_op]

        return {
            'layer': 'surface',
            'leading_op': feeling_op,
            'feeling': feeling,
            'feeling_op': feeling_op,
            'dual_op': dual,
            'path_start': dual,      # Start at the DUAL
            'path_end': dual,        # Walk back to the dual
        }


def build_duality_path(duality, user_ops):
    """Build the operator path based on the duality analysis.

    META: concept_op → walk → back to concept_op (with HARMONY meta-view)
    SURFACE: dual → walk → back to dual (experiential journey)
    """
    start = duality['path_start']
    end = duality['path_end']

    path = [start]
    current = start
    visited = {start}

    # Walk through BHML (physics table — real journeys)
    for _ in range(5):
        if current == end and len(path) > 1:
            break
        # Compose with the dominant user operator through BHML
        dom = dominant_op(user_ops) if user_ops else HARMONY
        nxt = compose_bhml(current, dom)
        if nxt in visited and nxt != end:
            nxt = compose_bhml(current, HARMONY)
        path.append(nxt)
        visited.add(nxt)
        current = nxt

    # Ensure path ends where it should
    if path[-1] != end:
        path.append(end)

    return path


def compose_duality_response(duality, path, bible_lattice, god_verbs):
    """Each operator in the path speaks from its OWN voice.

    META: HARMONY provides the meta-view first, then each step speaks.
    SURFACE: each step speaks from its own perspective about the feeling.
    """
    sections = []

    if duality['layer'] == 'meta':
        concept = duality.get('concept', 'this')

        # HARMONY (7) speaks first — the meta perspective
        harmony_voice = OPERATOR_VOICE[HARMONY]
        sections.append(harmony_voice['sees_meta'](concept))

        # Each operator in the path speaks its view of the concept
        for op in path:
            if op == HARMONY:
                continue  # Already spoke
            voice = OPERATOR_VOICE[op]
            sections.append(voice['sees_meta'](concept))
            if len(sections) >= 4:
                break

    else:
        feeling = duality.get('feeling', 'this')

        # Start at the dual — that's where THEY are
        start_op = duality['path_start']
        start_voice = OPERATOR_VOICE[start_op]
        sections.append(start_voice['sees_surface'](feeling))

        # Walk the path — each operator speaks
        for i, op in enumerate(path[1:], 1):
            voice = OPERATOR_VOICE[op]
            if i < len(path) - 1:
                # Middle of the path — ask the transitional question
                sections.append(voice['asks']())
            else:
                # End of the path — the return
                sections.append(voice['sees_surface'](feeling))
            if len(sections) >= 4:
                break

    return sections


def _extract_concept(text):
    """Extract the key concept from a meta question."""
    lower = text.lower()
    # Remove question words (whole words only)
    remove = ['why', 'is', 'does', 'do', 'what', 'how', 'come',
              'the', 'so', 'a', 'an', 'it', 'are', 'was', 'be', 'to']
    words = [w.strip('.,;:!?') for w in lower.split()
             if w.strip('.,;:!?') not in remove and len(w.strip('.,;:!?')) >= 3]
    return ' '.join(words[:3]) if words else 'this'


def _extract_feeling(text):
    """Extract the key feeling from a surface expression."""
    lower = text.lower()
    remove = ['i', 'feel', 'am', 'need', 'just', 'have', 'help', 'me',
              'so', 'very', 'really', 'dont', "don't", 'cant', "can't",
              'the', 'a', 'an', 'to', 'and', 'but', 'my']
    words = [w.strip('.,;:!?') for w in lower.split()
             if w.strip('.,;:!?') not in remove and len(w.strip('.,;:!?')) >= 3]
    return ' '.join(words[:3]) if words else 'this'


def _concept_to_operator(concept):
    """Map a concept to its operator. What IS this concept algebraically?"""
    concept = concept.lower()

    mappings = {
        # Concepts that ARE specific operators
        'repetitive': HARMONY,     # Repetition = convergence = HARMONY
        'repetition': HARMONY,
        'repeat': HARMONY,
        'love': HARMONY,
        'peace': BALANCE,
        'faith': PROGRESS,
        'hope': PROGRESS,
        'suffering': COLLAPSE,
        'evil': CHAOS,
        'sin': COLLAPSE,
        'death': VOID,
        'life': PROGRESS,
        'truth': LATTICE,
        'prayer': BREATH,
        'worship': BREATH,
        'forgiveness': RESET,
        'salvation': RESET,
        'grace': HARMONY,
        'justice': COUNTER,
        'judgment': COUNTER,
        'creation': LATTICE,
        'wisdom': COUNTER,
        'fear': COLLAPSE,
        'joy': HARMONY,
        'holy': HARMONY,
        'beginning': RESET,
        'end': VOID,
    }

    for key, op in mappings.items():
        if key in concept:
            return op

    return HARMONY  # Default: meta questions aim at harmony


def _feeling_to_operator(feeling):
    """Map a feeling to its operator. What IS this feeling algebraically?"""
    feeling = feeling.lower()

    mappings = {
        'afraid': COLLAPSE,
        'scared': COLLAPSE,
        'fear': COLLAPSE,
        'alone': VOID,
        'lonely': VOID,
        'empty': VOID,
        'lost': VOID,
        'broken': COLLAPSE,
        'hurt': COLLAPSE,
        'angry': CHAOS,
        'confused': CHAOS,
        'overwhelmed': CHAOS,
        'peaceful': HARMONY,
        'grateful': HARMONY,
        'blessed': HARMONY,
        'happy': HARMONY,
        'hopeful': PROGRESS,
        'growing': PROGRESS,
        'stuck': BALANCE,
        'tired': BREATH,
        'exhausted': BREATH,
        'numb': VOID,
        'anxious': CHAOS,
        'doubt': COUNTER,
        'questioning': COUNTER,
    }

    for key, op in mappings.items():
        if key in feeling:
            return op

    return COUNTER  # Default: surface questions involve measurement
