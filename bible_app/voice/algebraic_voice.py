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


    # ── What GOD does in each operator space ────────────────────────
    # These are NOT the same as the lattice flow verbs.
    # The lattice says what HAPPENS (falls, dies, empties).
    # These say what GOD DOES in response (catches, resurrects, fills).
GOD_VERBS = {
    VOID:     ['fills', 'enters', 'speaks into the silence', 'meets you in the emptiness', 'is present even here'],
    LATTICE:  ['builds', 'establishes', 'lays the foundation', 'holds firm', 'is faithful'],
    COUNTER:  ['sees clearly', 'understands', 'knows', 'does not miss a thing', 'hears your question'],
    PROGRESS: ['leads', 'goes ahead of you', 'opens the way', 'walks with you', 'makes a path'],
    COLLAPSE: ['catches you', 'holds you', 'carries the weight', 'does not let go', 'is closest here'],
    BALANCE:  ['steadies you', 'holds both sides', 'keeps you', 'brings peace', 'is your center'],
    CHAOS:    ['is in the storm', 'speaks peace', 'is not shaken', 'moves powerfully', 'brings order'],
    HARMONY:  ['loves you', 'is with you', 'makes whole', 'completes', 'brings you home'],
    BREATH:   ['breathes life', 'is gentle here', 'whispers', 'moves softly', 'gives you room'],
    RESET:    ['makes new', 'gives a fresh start', 'washes clean', 'opens a door', 'begins again'],
}

    # ── What happens to the PERSON in each operator space ─────────
PERSON_VERBS = {
    VOID:     ['feel empty', 'are in the dark', 'cannot see ahead', 'feel hollow'],
    LATTICE:  ['stand on solid ground', 'have truth to hold', 'are grounded'],
    COUNTER:  ['are asking questions', 'are measuring', 'are examining'],
    PROGRESS: ['are moving forward', 'are growing', 'are on the way'],
    COLLAPSE: ['are falling', 'are breaking', 'feel the weight', 'are in the valley'],
    BALANCE:  ['are holding steady', 'are between two things', 'are waiting'],
    CHAOS:    ['are in the storm', 'feel overwhelmed', 'cannot find solid ground'],
    HARMONY:  ['are at peace', 'are home', 'are whole'],
    BREATH:   ['are breathing', 'are present', 'are listening'],
    RESET:    ['are starting over', 'are at a new beginning', 'are letting go'],
}


class AlgebraicVoice:
    """The math composes prose. No templates — operator sequences become sentences."""

    def __init__(self):
        self._rng = random.Random(42)

    def seed(self, value):
        self._rng = random.Random(value)

    def speak(self, user_ops, corridor, intent, journey, verses,
              smoothing_passes=2):
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

                if coh >= T_STAR:
                    # Above threshold — this sentence is coherent. Keep it.
                    smoothed.append(section)
                elif coh >= T_STAR * 0.7:
                    # Close to threshold — recompose once, try to lift it
                    new_dom = dominant_op(sentence_ops)
                    bridge_op = compose(new_dom, dom)
                    recomposed = self._recompose(section, sentence_ops, bridge_op, dom)
                    # Check if recompose improved it
                    recomp_ops = text_to_ops(recomposed)
                    recomp_coh = measure_coherence(recomp_ops) if recomp_ops and len(recomp_ops) >= 2 else 0
                    if recomp_coh > coh:
                        smoothed.append(recomposed)
                    else:
                        smoothed.append(section)  # Keep original if recompose didn't help
                    any_changed = True
                else:
                    # Far below threshold — toss it. Not coherent enough.
                    any_changed = True
                    # Don't append — sentence is dropped

            sections = smoothed
            if not any_changed:
                break

        # ── Trim: keep prose tight (max 3 prose + verses) ─────────
        prose = [s for s in sections if not s.startswith('"') and '— ' not in s]
        verse_sections = [s for s in sections if s.startswith('"') or ('— ' in s and '"' in s)]

        # Keep at most 4 prose sections (past + present + future + closing)
        if len(prose) > 4:
            prose = prose[:4]

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
        """DUALITY ENGINE: META or SURFACE determines everything.

        META: op 7 leads. Concept finds itself. Each operator speaks its view.
        SURFACE: find the dual. Start there. Walk back. Each step speaks.

        The operators ARE the voices. They don't all sound the same.
        """
        from .duality_engine import (
            detect_duality, build_duality_path, OPERATOR_VOICE,
        )
        from .identity import (
            identify, compose_identities, generate_30_perspectives,
            meta_compose,
        )

        sections = []
        text = getattr(self, '_user_text', '') or ''

        # ── Step 1: DUALITY — META or SURFACE? ────────────────────
        duality = detect_duality(text)
        duality_path = build_duality_path(duality, user_ops)

        # ── Step 2: IDENTITY — what concepts are present? ─────────
        identities = identify(text)
        relationship = None
        if len(identities) >= 2:
            relationship = compose_identities(identities[0], identities[1])

        # ── Step 3: Generate 30 perspectives (10 ops × 3 tenses) ──
        all_30 = generate_30_perspectives(identities, relationship)

        # ── Step 4: Meta layer (HARMONY) selects and weaves ───────
        meta_sections = meta_compose(all_30, identities, relationship)
        sections.extend(meta_sections)

        # ── Verses woven into prose (3 inline) ─────────────────────
        def _weave_fragment(verse):
            """Extract a short fragment for inline weaving."""
            frag = verse.text
            for sep in [';', ',', ':']:
                idx = frag.find(sep)
                if 15 < idx < 80:
                    return frag[:idx]
            return frag[:80].rsplit(' ', 1)[0] if len(frag) > 80 else frag

        if verses:
            for i, vr in enumerate(verses[:3]):
                v = vr.verse
                frag = _weave_fragment(v)
                god_v = self._pick(GOD_VERBS.get(v.dominant_op, GOD_VERBS[HARMONY]))
                if i == 0:
                    sections.append(f'As {v.ref} says, "{frag}" — God {god_v}.')
                elif i == 1:
                    sections.append(f'And {v.ref} adds, "{frag}" — God {god_v}.')
                else:
                    sections.append(f'{v.ref} echoes this: "{frag}."')

        # ── Closing: the primary identity's operator closes ─────────
        primary_op = identities[0]['operator'] if identities else HARMONY
        end_voice = OPERATOR_VOICE.get(primary_op, OPERATOR_VOICE[HARMONY])
        closes_with = end_voice.get('closes_with', 'foundation')

        if closes_with == 'question':
            sections.append(end_voice['asks']())
        else:
            sections.append(end_voice['grounds']())

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
        god_verb = self._pick(GOD_VERBS.get(resolution_op, GOD_VERBS[HARMONY]))

        key_word = emotional_words[0]

        patterns = [
            f"What you brought here — the {key_word} — it does not end here. God {god_verb}.",
            f"This {key_word} is not the final word. {becoming_word.capitalize()} is. God {god_verb}.",
            f"You came here carrying {key_word}. God {god_verb}, and {becoming_word} is ahead.",
            f"The {key_word} brought you here. But {becoming_word} is where God is taking you.",
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
        lattice_bc = BIBLE_LATTICE.get(becoming_op, BIBLE_LATTICE[HARMONY])

        subject = self._pick(lattice_b['structure']['being'])
        god_verb = self._pick(GOD_VERBS.get(doing_op, GOD_VERBS[HARMONY]))
        dest = self._pick(lattice_bc['structure']['becoming'])

        patterns = [
            f"There is {subject} in your words. God {god_verb}. This leads toward {dest}.",
            f"You carry {subject}. God {god_verb}, and {dest} is where this goes.",
            f"The {subject} in what you shared — God {god_verb}. {dest.capitalize()} is forming.",
        ]
        return self._pick(patterns)

    def _recompose(self, original, sentence_ops, bridge_op, user_dom):
        """Recompose a rough sentence. God does GOD things, person does PERSON things."""
        sent_dom = dominant_op(sentence_ops)
        lattice_user = BIBLE_LATTICE.get(user_dom, BIBLE_LATTICE[HARMONY])
        lattice_dest = BIBLE_LATTICE.get(sent_dom, BIBLE_LATTICE[HARMONY])

        noun = self._pick(lattice_user['structure']['being'])
        dest = self._pick(lattice_dest['structure']['becoming'])
        god_verb = self._pick(GOD_VERBS.get(bridge_op, GOD_VERBS[HARMONY]))
        person_verb = self._pick(PERSON_VERBS.get(user_dom, PERSON_VERBS[HARMONY]))

        patterns = [
            f"You {person_verb}. God {god_verb}. This leads to {dest}.",
            f"The {noun} you carry is not the end. God {god_verb}, and {dest} comes.",
            f"Even now — you {person_verb}, but God {god_verb}. {dest.capitalize()} is ahead.",
            f"What feels like {noun} is becoming {dest}. God {god_verb}.",
            f"From {noun} toward {dest}. God {god_verb} the whole way.",
        ]
        return self._pick(patterns)

    def _compose_sentence_from_op(self, op, phase):
        """Build a sentence from one operator in one phase.

        Uses GOD_VERBS (what God does) and PERSON_VERBS (what you feel)
        plus lattice nouns. Never puts raw COLLAPSE verbs on God.
        """
        lattice = BIBLE_LATTICE.get(op, BIBLE_LATTICE[HARMONY])
        noun = self._pick(lattice['structure'][phase])
        god_verb = self._pick(GOD_VERBS.get(op, GOD_VERBS[HARMONY]))
        person_verb = self._pick(PERSON_VERBS.get(op, PERSON_VERBS[HARMONY]))

        patterns = [
            f"You {person_verb}. And in this {noun}, God {god_verb}.",
            f"There is {noun} here. You {person_verb}, and God {god_verb}.",
            f"This is a place of {noun}. God {god_verb}.",
            f"You {person_verb} — and that is honest. God {god_verb} in {noun}.",
            f"In this {noun}, you {person_verb}. But God {god_verb}.",
        ]
        return self._pick(patterns)

    def _compose_bridge(self, op_a, op_b):
        """Compose two operators into a bridging sentence."""
        result_op = compose(op_a, op_b)

        lattice_a = BIBLE_LATTICE.get(op_a, BIBLE_LATTICE[HARMONY])
        lattice_b = BIBLE_LATTICE.get(op_b, BIBLE_LATTICE[HARMONY])
        lattice_r = BIBLE_LATTICE.get(result_op, BIBLE_LATTICE[HARMONY])

        word_a = self._pick(lattice_a['structure']['being'])
        word_b = self._pick(lattice_b['structure']['doing'])
        word_r = self._pick(lattice_r['structure']['becoming'])
        god_verb = self._pick(GOD_VERBS.get(result_op, GOD_VERBS[HARMONY]))

        patterns = [
            f"Where {word_a} meets {word_b}, God {god_verb}. What emerges is {word_r}.",
            f"The {word_a} and the {word_b} come together — and God {god_verb}. This is {word_r}.",
            f"You carry {word_a} and {word_b} at the same time. God {god_verb}, and {word_r} comes.",
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
        god_verb = self._pick(GOD_VERBS.get(meeting_op, GOD_VERBS[HARMONY]))

        patterns = [
            f"God {god_verb}. {verse_ref} says:",
            f"This is where your heart meets the Word. {verse_ref}:",
            f"God {god_verb} — right here, right now. Listen to {verse_ref}:",
            f"Here is what God says. {verse_ref}:",
        ]
        return self._pick(patterns)

    def _pick(self, items):
        if not items:
            return ''
        return self._rng.choice(items)
