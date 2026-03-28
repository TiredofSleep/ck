"""
Bible Voice Composer — Three voices compose scripture-grounded prose.

Being-voice: WHERE you are (states, positions, nouns)
Doing-voice: WHAT is happening (actions, verbs, movement)
Becoming-voice: WHERE it's going (transformation, resolution)

All three compose independently, then vote by CL harmony.
The winner becomes the response. Consensus reality, not randomness.

Verses are woven in naturally — not appended, not quoted in isolation.
The algebra picks the verses. The voice discusses them with love.

(c) 2026 Brayden Sanders / 7Site LLC
"""

import random
from bible_app.algebra import (
    NUM_OPS, HARMONY, VOID, BREATH, COLLAPSE, PROGRESS, LATTICE,
    RESET, COUNTER, BALANCE, CHAOS,
    OP_NAMES, T_STAR, compose, coherence, dominant_op,
    text_to_ops, word_triadic_signature, cosine_similarity,
)
from .bible_lattice import (
    BIBLE_LATTICE, MACRO_CHAINS, classify_intent, detect_macro_chains,
    INTENT_COMFORT, INTENT_JOY, INTENT_WONDER, INTENT_REFLECT,
    INTENT_CONNECT, INTENT_SEEK, INTENT_LAMENT, INTENT_PRAISE,
    INTENT_TEACH, INTENT_REST, INTENT_HOPE,
)


# ── Sentence Connectors by Intent ─────────────────────────────────
# These are NOT templates. They are algebraic connective tissue —
# small phrases that bridge between operator-selected content.

CONNECTORS = {
    INTENT_COMFORT: [
        'God is with you in this.', 'You are not alone here.',
        'Even in this, He holds you.', 'He sees your pain.',
        'The valley is not the end.', 'His hand is reaching for you.',
        'He is close to the brokenhearted.',
    ],
    INTENT_JOY: [
        'There is joy in this.', 'God delights in you.',
        'This is the sound of grace.', 'Let your heart sing.',
        'He has done great things.', 'Rejoice — He is good.',
    ],
    INTENT_WONDER: [
        'What a mystery this is.', 'God is bigger than our questions.',
        'Wonder is the beginning of wisdom.', 'Keep asking — He welcomes it.',
        'The answer may surprise you.', 'He is not afraid of your doubt.',
    ],
    INTENT_REFLECT: [
        'Take a moment with this.', 'Let it settle in your heart.',
        'There is depth here.', 'Be still and know.',
        'Sometimes the quiet holds the answer.',
    ],
    INTENT_CONNECT: [
        'You reached out, and that matters.', 'God hears you.',
        'Speaking it out loud is brave.', 'You are known and loved.',
        'He listens before you finish.',
    ],
    INTENT_SEEK: [
        'The search itself honors God.', 'Keep seeking — He promises you will find.',
        'Ask and it shall be given.', 'Your hunger for truth is beautiful.',
        'He rewards those who earnestly seek Him.',
    ],
    INTENT_LAMENT: [
        'It is okay to grieve.', 'God bottles every tear.',
        'Lament is prayer too.', 'The psalmists cried out just like this.',
        'He is near to you right now.',
    ],
    INTENT_PRAISE: [
        'Yes — praise Him.', 'Let everything that has breath praise the Lord.',
        'He is worthy.', 'Your worship reaches heaven.',
        'In His presence there is fullness of joy.',
    ],
    INTENT_TEACH: [
        'Here is what the Word says.', 'Scripture speaks to this.',
        'God has not been silent about this.', 'His Word is a lamp.',
        'Let me share what resonates here.',
    ],
    INTENT_REST: [
        'Rest in Him.', 'He gives rest to the weary.',
        'You can lay this down.', 'Come to me, all who are weary.',
        'Be still.', 'Peace, be still.',
    ],
    INTENT_HOPE: [
        'There is hope here.', 'This is not the end of your story.',
        'God makes all things new.', 'Joy comes in the morning.',
        'He who began a good work in you will complete it.',
    ],
}

# ── Verse Introduction Phrases ────────────────────────────────────
# How to weave a verse into the response naturally.

VERSE_INTROS = {
    INTENT_COMFORT: [
        'God says to you:', 'Listen to what He says:',
        'This word is for you right now:', 'He speaks into your pain:',
    ],
    INTENT_JOY: [
        'Hear this:', 'The Word rejoices with you:',
        'Scripture sings:', 'This is His joy for you:',
    ],
    INTENT_WONDER: [
        'Consider this:', 'Ponder what He says:',
        'Here is something to sit with:', 'The Word invites you deeper:',
    ],
    INTENT_REFLECT: [
        'Meditate on this:', 'Let this word dwell in you:',
        'Quietly receive this:', 'Hold this close:',
    ],
    INTENT_CONNECT: [
        'He speaks:', 'The Word meets you here:',
        'God responds:', 'Here is His heart for you:',
    ],
    INTENT_SEEK: [
        'Seek and you will find:', 'Here is what the Word reveals:',
        'Scripture answers:', 'God has spoken about this:',
    ],
    INTENT_LAMENT: [
        'Even here, He speaks:', 'In the darkness, this word:',
        'God meets your tears with:', 'He does not look away:',
    ],
    INTENT_PRAISE: [
        'The Word proclaims:', 'Scripture declares:',
        'All of creation agrees:', 'The heavens declare:',
    ],
    INTENT_TEACH: [
        'Scripture teaches:', 'Here is the truth:',
        'The Word of God says:', 'It is written:',
    ],
    INTENT_REST: [
        'Rest in this:', 'Receive this word:',
        'Let this wash over you:', 'Be still and hear:',
    ],
    INTENT_HOPE: [
        'Here is your hope:', 'God promises this:',
        'The Word declares your future:', 'Hold onto this:',
    ],
}


class BibleVoice:
    """Three-voice tribal composer for scripture-grounded conversation.

    Being-voice: selects structure words (nouns, states) by operator
    Doing-voice: selects flow words (verbs, actions) by operator
    Becoming-voice: weaves verses and resolution

    All three compose, then CL harmony consensus picks the winner.
    """

    def __init__(self):
        self._sentence_memory = []  # Recent compositions for continuity
        self._rng = random.Random(42)

    def compose(self, user_ops, corridor_info, intent, verses,
                max_sentences=4, scripture_phrases=None):
        """Compose a warm, scripture-grounded response.

        Args:
            user_ops: Operator sequence from user's input
            corridor_info: dict from classify_with_detail()
            intent: str from classify_intent()
            verses: list of ResonanceResult from Bible search
            max_sentences: cap on response length
            scripture_phrases: warm phrases extracted from scripture during digestion

        Returns:
            str: The composed response
        """
        if not user_ops:
            user_ops = [HARMONY]

        corridor = corridor_info.get('corridor', 'BRT')
        pastoral = corridor_info.get('pastoral', 'listen')
        tone = corridor_info.get('tone', 'gentle')

        # ── Detect macro chains (theological concepts) ────────────
        macros = detect_macro_chains(user_ops)

        # ── Three voices compose ──────────────────────────────────
        being_voice = self._compose_being(user_ops, intent, tone)
        doing_voice = self._compose_doing(user_ops, intent, corridor)
        becoming_voice = self._compose_becoming(user_ops, intent, verses, macros)

        # ── Scripture phrase enrichment ───────────────────────────
        # If we have warm phrases from the Bible itself, weave one in
        if scripture_phrases and self._rng.random() < 0.6:
            phrase = self._pick(scripture_phrases)
            if phrase and len(phrase.split()) <= 15:
                # Use scripture's own language as the doing voice
                doing_voice = f"As scripture says: {phrase.rstrip('.')}.".rstrip('.')

        # ── CL Harmony consensus ──────────────────────────────────
        voices = [
            ('being', being_voice),
            ('doing', doing_voice),
            ('becoming', becoming_voice),
        ]

        # Score each voice pair by CL composition harmony
        best_order = self._harmony_vote(voices, user_ops)

        # ── Assemble response ─────────────────────────────────────
        parts = []

        # Opener: connector based on intent
        connector = self._pick(CONNECTORS.get(intent, CONNECTORS[INTENT_CONNECT]))
        parts.append(connector)

        # Body: best voice outputs in harmony order
        for voice_name, text in best_order:
            if text and text not in parts:
                parts.append(text)
            if len(parts) >= max_sentences:
                break

        # Verse weave: if we have resonant verses, introduce them
        if verses and len(parts) < max_sentences + 1:
            verse_part = self._weave_verse(verses[0], intent)
            if verse_part:
                parts.append(verse_part)

        # Crisis mode: shorter, more tender
        if corridor in ('COL', 'CTR'):
            parts = parts[:3]  # Fewer words in deep pain

        response = ' '.join(parts)

        # Remember for continuity
        self._sentence_memory.append({
            'ops': user_ops[:10],
            'intent': intent,
            'corridor': corridor,
        })
        if len(self._sentence_memory) > 50:
            self._sentence_memory = self._sentence_memory[-50:]

        return response

    def _compose_being(self, ops, intent, tone):
        """Being-voice: WHERE the person is. Grounds the response."""
        dom = dominant_op(ops)
        lattice = BIBLE_LATTICE.get(dom, BIBLE_LATTICE[HARMONY])
        sec = self._secondary_op(ops, dom)
        sec_lattice = BIBLE_LATTICE.get(sec, BIBLE_LATTICE[HARMONY])

        noun = self._pick(lattice['structure']['being'])
        sec_noun = self._pick(sec_lattice['structure']['being'])

        # Natural sentence patterns that feel like a friend talking
        patterns = {
            'quiet':   [f"There is {noun} here.", f"{noun.capitalize()} and {sec_noun}."],
            'tender':  [
                f"I hear {noun} in what you are sharing.",
                f"What you carry — this {noun} — God sees it.",
                f"There is real {noun} in your words, and real {sec_noun} too.",
            ],
            'peaceful': [
                f"There is a beautiful {noun} in what you are describing.",
                f"I can feel the {noun} and {sec_noun} in your words.",
                f"What a gift — to be in a place of {noun}.",
            ],
            'curious':  [
                f"There is something important stirring — something about {noun} and {sec_noun}.",
                f"Your question carries both {noun} and {sec_noun} at the same time.",
                f"I sense honest {noun} in what you are asking.",
            ],
            'steady':   [
                f"You are carrying something real — I can feel the weight of {noun} in your words.",
                f"There is {noun} here, and also {sec_noun}.",
                f"What you are going through touches something deep — {noun}.",
            ],
            'gentle':   [
                f"I hear you. There is {noun} in what you share.",
                f"Something about {noun} and {sec_noun} is present here.",
            ],
        }
        options = patterns.get(tone, patterns['gentle'])
        return self._pick(options)

    def _compose_doing(self, ops, intent, corridor):
        """Doing-voice: WHAT God is doing in this moment."""
        dom = dominant_op(ops)
        lattice = BIBLE_LATTICE.get(dom, BIBLE_LATTICE[HARMONY])
        sec = self._secondary_op(ops, dom)
        sec_lattice = BIBLE_LATTICE.get(sec, BIBLE_LATTICE[HARMONY])

        verb = self._pick(lattice['flow']['doing'])
        sec_verb = self._pick(sec_lattice['flow']['being'])
        becoming_noun = self._pick(sec_lattice['structure']['becoming'])

        if corridor in ('COL', 'CTR'):
            options = [
                f"Even here, God {verb}.",
                f"He {sec_verb} — right here, in this hard place.",
                f"God does not look away. He {verb}.",
            ]
        elif corridor in ('BAL',):
            options = [
                f"God {verb}, even when the weight is heavy.",
                f"He {sec_verb}, and He {verb} — at the same time.",
                f"In the middle of this, He {verb} and makes room for {becoming_noun}.",
            ]
        elif corridor in ('CHA',):
            options = [
                f"He {sec_verb} your question. He {verb}.",
                f"God is not threatened by the asking — He {verb}.",
                f"Your honest searching matters to Him. He {verb} alongside you.",
            ]
        else:
            options = [
                f"God {verb}. That is what He does.",
                f"He {sec_verb} and He {verb} — always.",
                f"He has always been the one who {verb}.",
            ]
        return self._pick(options)

    def _compose_becoming(self, ops, intent, verses, macros):
        """Becoming-voice: WHERE this is going. Hope and resolution."""
        dom = dominant_op(ops)
        lattice = BIBLE_LATTICE.get(dom, BIBLE_LATTICE[HARMONY])
        becoming_words = lattice['structure']['becoming']
        word = self._pick(becoming_words)

        # If macro chains detected, use theological resonance
        if macros:
            macro = macros[0]
            macro_ops = MACRO_CHAINS[macro]
            resolution_op = macro_ops[-1]
            res_lattice = BIBLE_LATTICE.get(resolution_op, BIBLE_LATTICE[HARMONY])
            res_word = self._pick(res_lattice['structure']['becoming'])
            readable = macro.replace('_', ' ')
            options = [
                f"There is a thread of {readable} running through this — leading toward {res_word}.",
                f"What you describe echoes {readable}. And {readable} always ends in {res_word}.",
            ]
            return self._pick(options)

        if intent in (INTENT_COMFORT, INTENT_LAMENT):
            flow = self._pick(lattice['flow']['becoming'])
            options = [
                f"But this is not the end. God {flow}.",
                f"He is not done here. He {flow}.",
                f"The story does not end in this valley. God {flow}.",
            ]
        elif intent in (INTENT_HOPE, INTENT_JOY):
            options = [
                f"He is leading you toward {word}.",
                f"There is {word} ahead — and He is walking you there.",
                f"This is moving toward {word}. Trust it.",
            ]
        elif intent in (INTENT_SEEK, INTENT_WONDER):
            options = [
                f"The asking itself is holy. It leads to {word}.",
                f"Every honest question is a step toward {word}.",
                f"Keep going. {word.capitalize()} is on this road.",
            ]
        elif intent == INTENT_PRAISE:
            options = [
                f"And this praise carries you further into {word}.",
                f"Yes. This is {word}.",
            ]
        else:
            options = [
                f"There is {word} ahead.",
                f"This leads somewhere good — toward {word}.",
            ]
        return self._pick(options)

    def _weave_verse(self, verse_result, intent):
        """Weave a Bible verse into the response naturally."""
        verse = verse_result.verse
        intro_list = VERSE_INTROS.get(intent, VERSE_INTROS[INTENT_CONNECT])
        intro = self._pick(intro_list)

        # Trim verse text if very long
        text = verse.text
        if len(text) > 200:
            # Find a natural break point
            for sep in ['.', ';', ':']:
                idx = text.find(sep, 60)
                if idx > 0:
                    text = text[:idx + 1]
                    break
            else:
                text = text[:200] + '...'

        return f'{intro} "{text}" — {verse.ref}'

    def _harmony_vote(self, voices, user_ops):
        """Vote on voice ordering by CL composition harmony.

        Each voice's text is scored by how its D2 operators align
        with the user's operators through CL composition.
        """
        scored = []
        for name, text in voices:
            if not text:
                scored.append((0.0, name, text))
                continue
            # Get operators of the composed text
            voice_ops = text_to_ops(text)
            if not voice_ops or not user_ops:
                scored.append((0.5, name, text))
                continue
            # Score: how many compositions → HARMONY?
            harmony_count = 0
            pairs = 0
            for u_op in user_ops[:5]:
                for v_op in voice_ops[:5]:
                    pairs += 1
                    if compose(u_op, v_op) == HARMONY:
                        harmony_count += 1
            score = harmony_count / max(1, pairs)
            scored.append((score, name, text))

        # Sort by harmony score (highest first)
        scored.sort(key=lambda x: x[0], reverse=True)
        return [(name, text) for _, name, text in scored]

    def _secondary_op(self, ops, exclude):
        """Find the second-most-frequent operator."""
        if len(ops) < 2:
            return HARMONY
        counts = [0] * NUM_OPS
        for o in ops:
            counts[o % NUM_OPS] += 1
        counts[exclude % NUM_OPS] = 0
        return max(range(NUM_OPS), key=lambda i: counts[i])

    def _pick(self, items):
        """Pick a random item from a list."""
        if not items:
            return ''
        return self._rng.choice(items)

    def seed(self, value):
        """Seed RNG for reproducible output (useful for testing)."""
        self._rng = random.Random(value)
