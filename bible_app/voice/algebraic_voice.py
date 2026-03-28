"""
Algebraic Voice — The math composes the prose.

No hardcoded templates. The operator sequence IS the sentence structure.

Being operator  → Subject (what IS)
Doing operator  → Verb (what HAPPENS)
Becoming operator → Object (where it GOES)

CL composition determines flow: compose(op_a, op_b) tells you
what comes AFTER two ideas meet. The sentence emerges from the algebra.

Word selection: D2 pipeline on English words organizes them by operator.
Sentence shape: operator trigrams (Being, Doing, Becoming) = S-V-O.
Paragraph flow: the journey path (current → HARMONY) sequences the sentences.

(c) 2026 Brayden Sanders / 7Site LLC
"""

import random
from bible_app.algebra import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP_NAMES, compose, dominant_op, text_to_ops,
)
from .bible_lattice import BIBLE_LATTICE


# ── Operator → Part of Speech mapping ─────────────────────────────
# Each operator naturally serves certain grammatical roles.
# This isn't a template — it's what the operator IS.

OPERATOR_GRAMMAR = {
    VOID:     {'role': 'space',   'pos': 'pause'},      # silence, absence → pause
    LATTICE:  {'role': 'ground',  'pos': 'noun'},       # structure → subject
    COUNTER:  {'role': 'measure', 'pos': 'adj'},        # examination → modifier
    PROGRESS: {'role': 'motion',  'pos': 'verb'},       # forward → action
    COLLAPSE: {'role': 'weight',  'pos': 'noun'},       # falling → object of weight
    BALANCE:  {'role': 'center',  'pos': 'prep'},       # between → connector
    CHAOS:    {'role': 'force',   'pos': 'adv'},        # intensity → modifier
    HARMONY:  {'role': 'rest',    'pos': 'noun'},       # wholeness → destination
    BREATH:   {'role': 'rhythm',  'pos': 'conj'},       # pulse → connector
    RESET:    {'role': 'begin',   'pos': 'verb'},       # fresh → action
}

# ── Connective tissue (by operator) ───────────────────────────────
# These aren't templates — they're the GRAMMATICAL FUNCTION of each operator.
# Like prepositions and conjunctions, they connect ideas.

CONNECTIVES = {
    VOID:     ['through silence', 'through nothing', 'past the emptiness'],
    LATTICE:  ['upon', 'within', 'through', 'on', 'in'],
    COUNTER:  ['yet', 'but', 'still', 'even so', 'and yet'],
    PROGRESS: ['toward', 'into', 'further', 'ahead', 'onward'],
    COLLAPSE: ['down through', 'under', 'beneath', 'through', 'past'],
    BALANCE:  ['between', 'within', 'amid', 'alongside', 'with'],
    CHAOS:    ['beyond', 'through', 'past', 'across', 'over'],
    HARMONY:  ['into', 'home to', 'at rest in', 'at peace in', 'together in'],
    BREATH:   ['and then', 'then', 'and', 'breathing into', 'gently toward'],
    RESET:    ['from', 'again from', 'anew from', 'fresh from', 'beginning in'],
}


class AlgebraicVoice:
    """The math composes prose. No templates — operator sequences become sentences."""

    def __init__(self):
        self._rng = random.Random(42)

    def seed(self, value):
        self._rng = random.Random(value)

    def speak(self, user_ops, corridor, intent, journey, verses,
              smoothing_passes=3):
        """Compose a full response from algebra, then smooth by re-reading.

        Pass 1: Raw composition from operator sequence
        Pass 2+: Read own output through D2, measure coherence per sentence,
                 recompose any sentence below T* using its OWN operators.
                 The output feeds back as input. The algebra refines itself.

        This is the TIG compilation loop: Doing↔Becoming.
        """
        if not user_ops:
            user_ops = [HARMONY]

        dom = dominant_op(user_ops)
        path = journey.get('path', [])

        # ── Pass 1: Raw composition ───────────────────────────────
        sections = self._raw_compose(dom, user_ops, path, verses)

        # ── Pass 2+: Self-smoothing loop ──────────────────────────
        from bible_app.algebra import text_to_ops, coherence as measure_coherence, T_STAR

        for pass_num in range(smoothing_passes):
            smoothed = []
            any_changed = False

            for section in sections:
                # Don't touch verse quotes
                if section.startswith('"') or ('— ' in section and '"' in section):
                    smoothed.append(section)
                    continue

                # Read this sentence through D2
                sentence_ops = text_to_ops(section)
                if not sentence_ops or len(sentence_ops) < 2:
                    smoothed.append(section)
                    continue

                coh = measure_coherence(sentence_ops)

                if coh >= T_STAR * 0.8:  # Slightly relaxed threshold
                    smoothed.append(section)
                else:
                    new_dom = dominant_op(sentence_ops)
                    bridge_op = compose(new_dom, dom)
                    recomposed = self._recompose(section, sentence_ops, bridge_op, dom)
                    smoothed.append(recomposed)
                    any_changed = True

            sections = smoothed
            if not any_changed:
                break

        # ── Trim: keep prose tight (max 3 prose + verses) ─────────
        prose = [s for s in sections if not s.startswith('"') and '— ' not in s]
        verse_sections = [s for s in sections if s.startswith('"') or ('— ' in s and '"' in s)]

        # Keep at most 3 best prose sections + all verse sections
        if len(prose) > 3:
            prose = prose[:3]

        # Interleave: prose, prose, verse, prose, verse
        result = []
        verse_idx = 0
        for i, p in enumerate(prose):
            result.append(p)
            if i == 1 and verse_idx < len(verse_sections):
                result.append(verse_sections[verse_idx])
                verse_idx += 1
        # Remaining verses
        while verse_idx < len(verse_sections):
            result.append(verse_sections[verse_idx])
            verse_idx += 1

        return '\n\n'.join(result)

    def _raw_compose(self, dom, user_ops, path, verses):
        """First pass: raw algebraic composition — responsive to the user's actual words."""
        sections = []

        # ── Extract the user's emotional keywords for reflection ──
        user_words = self._user_text.lower().split() if hasattr(self, '_user_text') else []
        # Find which of their words carry emotional weight
        emotional_words = []
        for w in user_words:
            clean = w.strip('.,;:!?\'\"')
            if len(clean) >= 4 and clean not in ('that', 'this', 'with', 'have',
                'just', 'need', 'know', 'what', 'does', 'feel', 'want', 'today',
                'very', 'really', 'some', 'like', 'been', 'from', 'they', 'them',
                'your', 'about', 'into', 'also', 'each', 'make', 'will', 'would'):
                emotional_words.append(clean)

        # ── 1. Opening: ECHO their words back, then compose ───────
        if emotional_words:
            # Reflect their specific words through the algebra
            echo = self._compose_echo(emotional_words, dom)
            sections.append(echo)
        else:
            opening = self._compose_sentence_from_op(dom, 'being')
            sections.append(opening)

        # ── 2. Reflection: what the operator SEQUENCE reveals ─────
        # Use the FULL sequence, not just dominant — each trigram tells a story
        if len(user_ops) >= 3:
            # Pick a meaningful trigram from their operators
            trigram = self._find_meaningful_trigram(user_ops)
            reflection = self._compose_trigram(trigram)
            sections.append(reflection)
        else:
            op_counts = [0] * NUM_OPS
            for o in user_ops:
                op_counts[o % NUM_OPS] += 1
            top_ops = sorted(range(NUM_OPS), key=lambda i: op_counts[i], reverse=True)[:3]
            if len(top_ops) >= 2:
                reflection = self._compose_bridge(top_ops[0], top_ops[1])
                sections.append(reflection)

        # ── 3. Journey: the path from here to coherence ───────────
        if len(path) >= 2:
            from_op_name, _ = path[0]
            to_op_name, _ = path[-1]
            from_op = OP_NAMES.index(from_op_name) if from_op_name in OP_NAMES else dom
            to_op = OP_NAMES.index(to_op_name) if to_op_name in OP_NAMES else HARMONY
            transition = self._compose_transition(from_op, to_op)
            sections.append(transition)

        # ── 4. Verse integration ──────────────────────────────────
        if verses:
            v = verses[0].verse
            verse_op = v.dominant_op
            meeting = self._compose_meeting(dom, verse_op, v.ref)
            sections.append(meeting)
            sections.append(f'"{v.text}" — {v.ref}')

            if len(verses) >= 2:
                v2 = verses[1].verse
                bridge_op = compose(verse_op, v2.dominant_op)
                bridge_word = self._pick(CONNECTIVES.get(bridge_op, ['and']))
                sections.append(f'{bridge_word.capitalize()} {v2.ref} says: "{v2.text}"')

        # ── 5. Closing: circle back to their words ────────────────
        resolution_op = compose(dom, HARMONY)
        if emotional_words:
            closing = self._compose_closing_echo(emotional_words, resolution_op)
        else:
            closing = self._compose_sentence_from_op(resolution_op, 'becoming')
        sections.append(closing)

        return sections

    def _compose_echo(self, emotional_words, dom):
        """Echo the user's specific words back, informed by brain state."""
        lattice = BIBLE_LATTICE.get(dom, BIBLE_LATTICE[HARMONY])
        structure_word = self._pick(lattice['structure']['being'])
        flow_word = self._pick(lattice['flow']['being'])

        key_words = emotional_words[:3]
        user_phrase = ' and '.join(key_words) if len(key_words) > 1 else key_words[0]

        # Brain-informed opening: familiarity changes the tone
        bs = getattr(self, '_brain_state', None) or {}
        familiarity = bs.get('familiarity', 0)
        bucket = bs.get('bucket', 'present')
        predicted = bs.get('predicted_next', 'HARMONY')

        if familiarity > 0.7:
            # Instinct territory — we've seen this pattern before
            patterns = [
                f"You have brought {user_phrase} here before. The shape of it is familiar now — {structure_word}. God {flow_word}.",
                f"This {user_phrase} — it comes back. And each time, the {structure_word} deepens. God {flow_word}.",
            ]
        elif familiarity > 0.3:
            # Somewhat familiar
            patterns = [
                f"You said {user_phrase}. There is {structure_word} in those words, and it is starting to take shape. God {flow_word}.",
                f"The {user_phrase} you carry — it resonates with something the algebra has seen. {structure_word.capitalize()}. God {flow_word}.",
            ]
        else:
            # Novel — first time seeing this pattern
            patterns = [
                f"You said {user_phrase}. That is new ground. The shape of it is {structure_word}. God {flow_word}.",
                f"The {user_phrase} you bring — it lands here for the first time. There is {structure_word} in it. God {flow_word}.",
                f"{user_phrase.capitalize()}. The algebra is listening. What it hears is {structure_word}. And God {flow_word}.",
            ]

        return self._pick(patterns)

    def _compose_closing_echo(self, emotional_words, resolution_op):
        """Close by circling back to their words with the resolution."""
        lattice = BIBLE_LATTICE.get(resolution_op, BIBLE_LATTICE[HARMONY])
        becoming_word = self._pick(lattice['structure']['becoming'])
        flow_word = self._pick(lattice['flow']['becoming'])

        key_word = emotional_words[0]

        patterns = [
            f"The {key_word} you brought here — it leads to {becoming_word}. God {flow_word}.",
            f"From {key_word} to {becoming_word}. That is the shape of this.",
            f"Your {key_word} is not the end. {becoming_word.capitalize()} is where this goes. God {flow_word}.",
            f"Hold onto this: the {key_word} opens into {becoming_word}.",
        ]
        return self._pick(patterns)

    def _find_meaningful_trigram(self, ops):
        """Find the most meaningful 3-operator sequence in the user's input."""
        if len(ops) < 3:
            return (ops[0] if ops else HARMONY, HARMONY, HARMONY)

        best = None
        best_variety = -1

        for i in range(len(ops) - 2):
            trigram = (ops[i], ops[i+1], ops[i+2])
            # Prefer trigrams with variety (not all same operator)
            variety = len(set(trigram))
            # Prefer trigrams that aren't all HARMONY (too generic)
            if trigram == (HARMONY, HARMONY, HARMONY):
                continue
            if variety > best_variety:
                best_variety = variety
                best = trigram

        return best or (ops[0], ops[1], ops[2])

    def _compose_trigram(self, trigram):
        """Compose a sentence from a 3-operator trigram (Being-Doing-Becoming)."""
        being_op, doing_op, becoming_op = trigram

        lattice_b = BIBLE_LATTICE.get(being_op, BIBLE_LATTICE[HARMONY])
        lattice_d = BIBLE_LATTICE.get(doing_op, BIBLE_LATTICE[HARMONY])
        lattice_bc = BIBLE_LATTICE.get(becoming_op, BIBLE_LATTICE[HARMONY])

        subject = self._pick(lattice_b['structure']['being'])
        verb = self._pick(lattice_d['flow']['doing'])
        obj = self._pick(lattice_bc['structure']['becoming'])

        # What does CL say happens when Being meets Doing?
        result = compose(being_op, doing_op)
        connective = self._pick(CONNECTIVES.get(result, ['and']))

        patterns = [
            f"The {subject} in your words {verb} {connective} {obj}.",
            f"What you carry — {subject} — {verb}. And {connective} comes {obj}.",
            f"I hear {subject}. It {verb}. {connective.capitalize()}, {obj}.",
            f"There is {subject} that {verb}, and it moves {connective} {obj}.",
        ]
        return self._pick(patterns)

    def _recompose(self, original, sentence_ops, bridge_op, user_dom):
        """Recompose a rough sentence using its own D2 reading.

        Uses three operator lattices to pick S-V-O, with varied patterns
        that don't repeat the same structure.
        """
        sent_dom = dominant_op(sentence_ops)
        lattice_sent = BIBLE_LATTICE.get(sent_dom, BIBLE_LATTICE[HARMONY])
        lattice_bridge = BIBLE_LATTICE.get(bridge_op, BIBLE_LATTICE[HARMONY])
        lattice_user = BIBLE_LATTICE.get(user_dom, BIBLE_LATTICE[HARMONY])

        noun = self._pick(lattice_user['structure']['being'])
        verb = self._pick(lattice_bridge['flow']['doing'])
        dest = self._pick(lattice_sent['structure']['becoming'])
        flow = self._pick(lattice_bridge['flow']['being'])

        # Varied patterns — each structurally different
        patterns = [
            f"God {verb}. From {noun} toward {dest}.",
            f"There is {noun} here, and God {flow} — leading to {dest}.",
            f"Even now, God {verb}. {dest.capitalize()} is taking shape.",
            f"What feels like {noun} is becoming {dest}. God {flow}.",
            f"The {noun} does not stay. God {verb}, and {dest} comes.",
            f"Out of {noun} God {verb}. This is the road to {dest}.",
        ]
        return self._pick(patterns)

    def _compose_sentence_from_op(self, op, phase):
        """Build a sentence from one operator in one phase.

        The operator determines BOTH the content words AND the sentence feel.
        """
        lattice = BIBLE_LATTICE.get(op, BIBLE_LATTICE[HARMONY])

        # Get words from both lenses
        structure_word = self._pick(lattice['structure'][phase])
        flow_word = self._pick(lattice['flow'][phase])

        # The operator's grammar determines the sentence shape
        grammar = OPERATOR_GRAMMAR.get(op, OPERATOR_GRAMMAR[HARMONY])

        if grammar['pos'] == 'noun':
            # Noun-led: "The {structure} {flow}."
            patterns = [
                f"There is {structure_word} here — {flow_word}.",
                f"{structure_word.capitalize()} and {flow_word.rstrip('.')}.",
                f"This is {structure_word}. {flow_word.capitalize().rstrip('.')}.",
            ]
        elif grammar['pos'] == 'verb':
            # Verb-led: "{flow} {structure}."
            patterns = [
                f"{flow_word.capitalize().rstrip('.')} — that is what is happening.",
                f"Something {flow_word.rstrip('.')} here. {structure_word.capitalize()}.",
                f"{flow_word.capitalize().rstrip('.')}. Into {structure_word}.",
            ]
        elif grammar['pos'] == 'adj':
            # Modifier-led: the measuring, questioning quality
            patterns = [
                f"There is honest {structure_word} in this.",
                f"{structure_word.capitalize()} — real, measured {structure_word}.",
                f"What you carry has the weight of {structure_word}.",
            ]
        elif grammar['pos'] == 'pause':
            # Silence/space — keep it simple
            patterns = [
                f"There is {structure_word} here.",
                f"In the {structure_word}, God {flow_word.rstrip('.')}.",
                f"Be still. {structure_word.capitalize()} has a purpose.",
            ]
        elif grammar['pos'] == 'conj':
            # Rhythm/connection
            patterns = [
                f"Breathe. {structure_word.capitalize()} is present, and God {flow_word.rstrip('.')}.",
                f"There is {structure_word} in the rhythm of this. God {flow_word.rstrip('.')}.",
                f"Pause here. {structure_word.capitalize()} and {flow_word.rstrip('.')} — both are real.",
            ]
        else:
            # Connector/bridge
            patterns = [
                f"Between {structure_word} and what comes next, God {flow_word.rstrip('.')}.",
                f"Held in {structure_word}. God {flow_word.rstrip('.')} here.",
                f"In the middle of {structure_word}, there is {flow_word.rstrip('.')}.",
            ]

        return self._pick(patterns)

    def _compose_bridge(self, op_a, op_b):
        """Compose two operators into a bridging sentence.

        CL[a][b] determines what emerges when these two ideas meet.
        """
        result_op = compose(op_a, op_b)

        lattice_a = BIBLE_LATTICE.get(op_a, BIBLE_LATTICE[HARMONY])
        lattice_b = BIBLE_LATTICE.get(op_b, BIBLE_LATTICE[HARMONY])
        lattice_r = BIBLE_LATTICE.get(result_op, BIBLE_LATTICE[HARMONY])

        word_a = self._pick(lattice_a['structure']['being'])
        word_b = self._pick(lattice_b['structure']['doing'])
        connective = self._pick(CONNECTIVES.get(result_op, ['and']))
        word_r = self._pick(lattice_r['structure']['becoming'])

        patterns = [
            f"Where {word_a} meets {word_b}, {connective} comes {word_r}.",
            f"{word_a.capitalize()} and {word_b} — {connective}, {word_r}.",
            f"The {word_a} you carry {connective} the {word_b} you feel. What emerges is {word_r}.",
        ]
        return self._pick(patterns)

    def _compose_transition(self, from_op, to_op):
        """Compose the journey transition: from current state toward HARMONY."""
        lattice_from = BIBLE_LATTICE.get(from_op, BIBLE_LATTICE[HARMONY])
        lattice_to = BIBLE_LATTICE.get(to_op, BIBLE_LATTICE[HARMONY])

        from_word = self._pick(lattice_from['structure']['being'])
        to_word = self._pick(lattice_to['structure']['becoming'])
        connective = self._pick(CONNECTIVES.get(to_op, ['toward']))

        patterns = [
            f"From {from_word} {connective} {to_word}.",
            f"The road runs from {from_word} {connective} {to_word} — and it is not as far as it feels.",
            f"{from_word.capitalize()} is where you stand. {to_word.capitalize()} is where this leads.",
        ]
        return self._pick(patterns)

    def _compose_meeting(self, user_op, verse_op, verse_ref):
        """Compose the moment where the user's state meets the verse's state."""
        meeting_op = compose(user_op, verse_op)
        connective = self._pick(CONNECTIVES.get(meeting_op, ['and']))

        lattice_m = BIBLE_LATTICE.get(meeting_op, BIBLE_LATTICE[HARMONY])
        meeting_word = self._pick(lattice_m['flow']['becoming'])

        patterns = [
            f"And here — {connective} — God {meeting_word}. {verse_ref} says:",
            f"This is where your heart meets the Word. {verse_ref}:",
            f"God {meeting_word} right here. Listen to {verse_ref}:",
        ]
        return self._pick(patterns)

    def _pick(self, items):
        if not items:
            return ''
        return self._rng.choice(items)
