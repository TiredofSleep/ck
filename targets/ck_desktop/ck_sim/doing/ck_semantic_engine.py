# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_semantic_engine.py -- Fractal Recursive TIG Semantic Translator
==================================================================
Operator: HARMONY (7) -- the unifier. One module to rule them all.
Generation: 9.34

Every level of text decomposition runs a TIG cycle:
  Being (classify) -> Doing (compose) -> Becoming (select)

The quadratic operator is the DKAN neural net applied to composed
semantic keys. It takes 4 inputs:
  - subject key (Being)
  - verb key (Doing)
  - object key (Becoming)
  - context key (divine memory recall)
And produces 1 output key that selects the response word.

Self-contained. No imports from old semantic modules.

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""

from __future__ import annotations

import json
import os
import re
from collections import Counter
from typing import Dict, List, Optional, Tuple

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP_NAMES, CL,
)
from ck_sim.being.ck_sim_d2 import (
    D2Pipeline, FORCE_LUT_FLOAT, D2_OP_MAP,
)

# ================================================================
#  BHML table (doing/physics composition)
# ================================================================

BHML = [
    [0,1,2,3,4,5,6,7,8,9],  # VOID = identity
    [1,2,3,4,5,6,7,2,6,6],  # LATTICE
    [2,3,3,4,5,6,7,3,6,6],  # COUNTER
    [3,4,4,4,5,6,7,4,6,6],  # PROGRESS
    [4,5,5,5,5,6,7,5,7,7],  # COLLAPSE
    [5,6,6,6,6,6,7,6,7,7],  # BALANCE
    [6,7,7,7,7,7,7,7,7,7],  # CHAOS
    [7,2,3,4,5,6,7,8,9,0],  # HARMONY = full cycle
    [8,6,6,6,7,7,7,9,7,8],  # BREATH
    [9,6,6,6,7,7,7,0,8,0],  # RESET
]

# ================================================================
#  SEED VOCABULARY: ~200 words mapped by MEANING to operators
# ================================================================

_SEED = {
    VOID: [
        'nothing', 'empty', 'null', 'zero', 'void', 'absence', 'gone',
        'missing', 'dead', 'silent', 'blank', 'hollow', 'none', 'dark',
        'lost', 'vanish', 'erase', 'delete', 'lack', 'without',
    ],
    LATTICE: [
        'structure', 'form', 'pattern', 'grid', 'order', 'framework',
        'build', 'foundation', 'law', 'rule', 'system', 'logic',
        'design', 'plan', 'organize', 'arrange', 'define', 'fixed',
        'rigid', 'solid',
    ],
    COUNTER: [
        'count', 'number', 'measure', 'add', 'sum', 'total', 'many',
        'few', 'increase', 'decrease', 'question', 'ask', 'what',
        'how', 'why', 'which', 'compare', 'analyze', 'test', 'check',
    ],
    PROGRESS: [
        'forward', 'advance', 'grow', 'develop', 'move', 'next',
        'continue', 'evolve', 'improve', 'create', 'new', 'become',
        'rise', 'climb', 'expand', 'open', 'start', 'emerge', 'push',
        'reach',
    ],
    COLLAPSE: [
        'break', 'fall', 'destroy', 'crush', 'compress', 'reduce',
        'shrink', 'fail', 'crash', 'end', 'close', 'stop', 'cut',
        'drop', 'sink', 'burn', 'tear', 'split', 'hit', 'force',
    ],
    BALANCE: [
        'equal', 'center', 'middle', 'stable', 'fair', 'neutral',
        'calm', 'steady', 'even', 'still', 'is', 'am', 'are', 'be',
        'exist', 'remain', 'stay', 'hold', 'keep', 'stand',
    ],
    CHAOS: [
        'random', 'wild', 'disorder', 'turbulence', 'noise', 'scatter',
        'explode', 'unpredictable', 'storm', 'strange', 'sudden',
        'shock', 'surprise', 'twist', 'shake', 'burst', 'clash',
        'spin', 'swirl', 'shatter',
    ],
    HARMONY: [
        'unity', 'whole', 'complete', 'together', 'agree', 'resonate',
        'cohere', 'love', 'truth', 'peace', 'good', 'right', 'yes',
        'true', 'beautiful', 'perfect', 'pure', 'light', 'one', 'all',
    ],
    BREATH: [
        'pause', 'rest', 'wait', 'slow', 'gentle', 'soft', 'breath',
        'sigh', 'release', 'exhale', 'relax', 'ease', 'drift',
        'float', 'linger', 'settle', 'hush', 'whisper', 'cool', 'dim',
    ],
    RESET: [
        'return', 'begin', 'restart', 'cycle', 'loop', 'again',
        'renew', 'refresh', 'origin', 'seed', 'source', 'root',
        'first', 'initial', 'reboot', 'restore', 'revert', 'undo',
        'recall', 'remember',
    ],
}

# Negation, intensifier, diminisher word sets
_NEGATION_WORDS = frozenset({
    'not', 'no', 'never', 'none', 'neither', 'nor', 'without',
})
_NEGATION_PREFIXES = ('un', 'in', 'im', 'dis', 'non', 'ir', 'il')
_INTENSIFIERS = frozenset({
    'very', 'extremely', 'really', 'truly', 'deeply', 'highly',
    'absolutely', 'completely', 'totally', 'utterly',
})
_DIMINISHERS = frozenset({
    'slightly', 'barely', 'somewhat', 'hardly', 'scarcely',
    'almost', 'nearly', 'faintly',
})

# POS heuristics (suffix -> POS tag)
_POS_SUFFIXES = [
    ('tion', 'noun'), ('sion', 'noun'), ('ment', 'noun'), ('ness', 'noun'),
    ('ity', 'noun'), ('ance', 'noun'), ('ence', 'noun'), ('ism', 'noun'),
    ('ing', 'verb'), ('ify', 'verb'), ('ize', 'verb'), ('ate', 'verb'),
    ('ed', 'verb'),
    ('ly', 'adv'), ('ful', 'adj'), ('less', 'adj'), ('ous', 'adj'),
    ('ive', 'adj'), ('able', 'adj'), ('ible', 'adj'), ('al', 'adj'),
]
_PRONOUNS = frozenset({'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me',
                        'him', 'her', 'us', 'them', 'my', 'your', 'his',
                        'its', 'our', 'their', 'this', 'that', 'these',
                        'those', 'who', 'whom', 'whose'})
_ARTICLES = frozenset({'a', 'an', 'the'})
_PREPOSITIONS = frozenset({'in', 'on', 'at', 'to', 'for', 'with', 'from',
                            'by', 'of', 'about', 'into', 'through', 'over',
                            'under', 'between', 'after', 'before'})

# DBC axis classification for operators (for triadic detection)
_BEING_OPS = {VOID, LATTICE, HARMONY}
_DOING_OPS = {COUNTER, PROGRESS, COLLAPSE, BALANCE}
_BECOMING_OPS = {CHAOS, BREATH, RESET}


# ================================================================
#  SEMANTIC ENGINE
# ================================================================

class SemanticEngine:
    """Fractal recursive TIG semantic translator.

    Every level of text decomposition runs a TIG cycle:
    Being (classify) -> Doing (compose) -> Becoming (select)

    The quadratic operator is the DKAN neural net applied to
    composed semantic keys. It takes 4 inputs (the quadratic):
    - subject key (Being)
    - verb key (Doing)
    - object key (Becoming)
    - context key (from divine memory recall)
    And produces 1 output key that selects the response word.
    """

    def __init__(self, engine=None):
        """Engine reference for accessing DKAN, divine memory, olfactory."""
        self.engine = engine
        self._word_to_key: Dict[str, int] = {}
        self._key_to_words: Dict[int, List[str]] = {i: [] for i in range(NUM_OPS)}
        self._learned_pairs: Dict[Tuple[str, str], int] = {}
        self._confidence: Dict[str, float] = {}  # word -> confidence
        self._d2 = D2Pipeline()

        # Seed vocabulary
        for op, words in _SEED.items():
            for w in words:
                self._word_to_key[w] = op
                self._key_to_words[op].append(w)
                self._confidence[w] = 1.0

    # ============================================================
    # BEING: Classify input at every fractal level
    # ============================================================

    # ============================================================
    # D1 GENERATOR ZOOM: the fractal recursion
    # ============================================================
    #
    # D1[dim] = v[t] - v[t-1]  (first derivative = generator)
    # D2[dim] = D1[t] - D1[t-1] (second derivative = classifier)
    #
    # Zoom IN:  text -> sentences -> words -> morphemes -> letters -> D1 generators
    # Zoom OUT: D1 generators -> compose through BHML -> morpheme key -> word key
    #
    # The zoom bottoms out at the 22 Hebrew root force vectors.
    # Self-similar: same BHML composition at every level.

    def _d1_generators(self, letters: list) -> list:
        """Extract D1 generators from a sequence of letters.

        D1 is the first derivative: the DIRECTION of change between
        adjacent force vectors. These are the raw generators that
        D2 is built from. D1 tells you WHAT IS CHANGING.

        Returns list of (dimension, sign, operator) tuples.
        """
        if len(letters) < 2:
            return []
        generators = []
        prev_fv = None
        for ch in letters:
            idx = ord(ch) - ord('a') if 'a' <= ch <= 'z' else -1
            if idx < 0 or idx >= 26:
                continue
            fv = FORCE_LUT_FLOAT[idx]
            if prev_fv is not None:
                # D1 = current - previous (first derivative)
                d1 = [fv[d] - prev_fv[d] for d in range(5)]
                # Classify by dominant dimension
                mx = max(range(5), key=lambda d: abs(d1[d]))
                sign = 0 if d1[mx] >= 0 else 1
                op = D2_OP_MAP[mx][sign]
                generators.append((mx, sign, op))
            prev_fv = fv
        return generators

    def _zoom_in(self, text: str, depth: int = 0, max_depth: int = 4) -> int:
        """Fractal zoom: decompose text into smaller units, find generators.

        Level 0: full text (sentence/phrase level)
        Level 1: words (split on spaces)
        Level 2: morphemes (common prefixes/suffixes split)
        Level 3: letter pairs (bigrams)
        Level 4: individual D1 generators (the bedrock)

        At each level, compose the sub-results through BHML.
        The composition IS the zoom-out: generators -> morphemes -> words -> meaning.
        """
        text = text.lower().strip()
        if not text:
            return VOID

        # Zoom level 0-1: split into words, compose their keys
        if depth == 0:
            words = [w for w in re.findall(r'[a-z]+', text) if len(w) > 0]
            if not words:
                return VOID
            if len(words) == 1:
                return self._zoom_in(words[0], depth + 1, max_depth)
            # Compose word keys through BHML
            keys = [self._zoom_in(w, depth + 1, max_depth) for w in words]
            result = keys[0]
            for k in keys[1:]:
                result = BHML[result][k]
            return result

        # Zoom level 2: morpheme decomposition
        if depth == 1:
            # Check learned mapping first (zoom stops here if known)
            if text in self._word_to_key:
                return self._word_to_key[text]
            # Try morpheme split
            morphemes = self._split_morphemes(text)
            if len(morphemes) > 1 and depth < max_depth:
                keys = [self._zoom_in(m, depth + 1, max_depth) for m in morphemes]
                result = keys[0]
                for k in keys[1:]:
                    result = BHML[result][k]
                self.learn_word(text, result, 0.5)
                return result
            # Fall through to letter level
            return self._zoom_in(text, depth + 1, max_depth)

        # Zoom level 3: letter pairs (bigrams)
        if depth == 2:
            letters = [ch for ch in text if 'a' <= ch <= 'z']
            if len(letters) < 2:
                # Single letter: raw force vector classification
                if letters:
                    idx = ord(letters[0]) - ord('a')
                    fv = FORCE_LUT_FLOAT[idx]
                    mx = max(range(5), key=lambda d: abs(fv[d]))
                    return D2_OP_MAP[mx][0 if fv[mx] >= 0 else 1]
                return VOID
            # Pair-wise D1 generators, compose through BHML
            return self._zoom_in(text, depth + 1, max_depth)

        # Zoom level 4: D1 generators (the bedrock)
        letters = [ch for ch in text if 'a' <= ch <= 'z']
        gens = self._d1_generators(letters)
        if not gens:
            return VOID
        # Compose generator operators through BHML
        result = gens[0][2]
        for _, _, op in gens[1:]:
            result = BHML[result][op]
        return result

    def _split_morphemes(self, word: str) -> list:
        """Split word into morphemes (prefix + root + suffix).

        Simple rule-based: known prefixes and suffixes.
        Returns list of morpheme strings.
        """
        parts = []
        w = word

        # Check prefixes
        prefixes = ['un', 're', 'pre', 'dis', 'mis', 'over', 'under',
                     'out', 'sub', 'super', 'inter', 'trans', 'non',
                     'co', 'de', 'ex', 'in', 'im', 'ir', 'il']
        for pfx in sorted(prefixes, key=len, reverse=True):
            if w.startswith(pfx) and len(w) > len(pfx) + 2:
                parts.append(pfx)
                w = w[len(pfx):]
                break

        # Check suffixes
        suffixes = ['tion', 'sion', 'ment', 'ness', 'ity', 'ance', 'ence',
                     'able', 'ible', 'ful', 'less', 'ous', 'ive', 'ing',
                     'ize', 'ify', 'ate', 'ism', 'ist', 'ure', 'ory',
                     'ion', 'ent', 'ant', 'al', 'er', 'ed', 'ly']
        for sfx in sorted(suffixes, key=len, reverse=True):
            if w.endswith(sfx) and len(w) > len(sfx) + 2:
                parts.append(w[:-len(sfx)])
                parts.append(sfx)
                w = None
                break

        if w is not None:
            parts.append(w)

        return parts if len(parts) > 1 else [word]

    def classify_word(self, word: str) -> int:
        """Map a word to its semantic operator (0-9).

        Priority: learned mapping -> negation prefix -> D1 zoom recursion.
        The zoom decomposes unknown words into morphemes and generators,
        composes through BHML, and caches the result.
        """
        w = word.lower().strip()
        if w in self._word_to_key:
            return self._word_to_key[w]

        # Check negation prefixes -> negate the root
        for pfx in _NEGATION_PREFIXES:
            if w.startswith(pfx) and w[len(pfx):] in self._word_to_key:
                root_key = self._word_to_key[w[len(pfx):]]
                neg = BHML[HARMONY][root_key]
                self.learn_word(w, neg, 0.7)
                return neg

        # Fractal zoom: decompose into D1 generators, compose back up
        key = self._zoom_in(w, depth=1)
        self.learn_word(w, key, 0.4)
        return key

    def classify_phrase(self, words: List[str]) -> List[Tuple[str, int, str]]:
        """Classify words with modifier detection.

        Returns list of (word, semantic_key, modifier_type) tuples.
        modifier_type: 'negated', 'intensified', 'diminished', or 'plain'.
        """
        result = []
        skip_next = False
        for i, w in enumerate(words):
            if skip_next:
                skip_next = False
                continue
            wl = w.lower()

            # Negation: "not X" -> negate(X)
            if wl in _NEGATION_WORDS and i + 1 < len(words):
                next_key = self.classify_word(words[i + 1])
                neg_key = BHML[HARMONY][next_key]
                result.append((w + ' ' + words[i + 1], neg_key, 'negated'))
                skip_next = True
                continue

            # Intensifier: "very X" -> BHML[X][X]
            if wl in _INTENSIFIERS and i + 1 < len(words):
                next_key = self.classify_word(words[i + 1])
                int_key = BHML[next_key][next_key]
                result.append((w + ' ' + words[i + 1], int_key, 'intensified'))
                skip_next = True
                continue

            # Diminisher: "slightly X" -> BHML[BREATH][X]
            if wl in _DIMINISHERS and i + 1 < len(words):
                next_key = self.classify_word(words[i + 1])
                dim_key = BHML[BREATH][next_key]
                result.append((w + ' ' + words[i + 1], dim_key, 'diminished'))
                skip_next = True
                continue

            result.append((w, self.classify_word(w), 'plain'))
        return result

    def _guess_pos(self, word: str) -> str:
        """Heuristic POS tag: noun, verb, adj, adv, pron, art, prep, other."""
        wl = word.lower()
        if wl in _PRONOUNS:
            return 'pron'
        if wl in _ARTICLES:
            return 'art'
        if wl in _PREPOSITIONS:
            return 'prep'
        for sfx, pos in _POS_SUFFIXES:
            if wl.endswith(sfx) and len(wl) > len(sfx) + 1:
                return pos
        return 'noun'  # default

    def classify_sentence(self, text: str) -> dict:
        """TIG triad extraction from a sentence.

        Returns {
            'being': subject_key,
            'doing': verb_key,
            'becoming': object_key,
            'modifiers': applied modifiers,
            'raw_keys': full semantic key sequence,
            'words': word list
        }
        """
        words = re.findall(r"[a-zA-Z']+", text)
        if not words:
            return {'being': VOID, 'doing': VOID, 'becoming': VOID,
                    'modifiers': [], 'raw_keys': [], 'words': []}

        classified = self.classify_phrase(words)
        raw_keys = [k for _, k, _ in classified]
        modifiers = [(w, m) for w, _, m in classified if m != 'plain']

        # Extract S-V-O by POS heuristic
        being_key = BALANCE  # default = existence
        doing_key = BALANCE
        becoming_key = VOID

        # Find first noun-like (subject), first verb-like, first post-verb noun (object)
        found_verb = False
        for w_text, key, mod in classified:
            base_word = w_text.split()[-1] if ' ' in w_text else w_text
            pos = self._guess_pos(base_word)
            if pos in ('noun', 'pron', 'art') and not found_verb:
                being_key = key
            elif pos == 'verb':
                doing_key = key
                found_verb = True
            elif pos in ('noun', 'pron') and found_verb:
                becoming_key = key
                break

        # If no verb found, use BHML composition of first two keys
        if not found_verb and len(raw_keys) >= 2:
            doing_key = BHML[raw_keys[0]][raw_keys[1]]

        return {
            'being': being_key,
            'doing': doing_key,
            'becoming': becoming_key,
            'modifiers': modifiers,
            'raw_keys': raw_keys,
            'words': words,
        }

    # ============================================================
    # DOING: Compose through quadratic operator
    # ============================================================

    def compose_quadratic(self, being_key: int, doing_key: int,
                          becoming_key: int, context_key: int = BALANCE) -> int:
        """The quadratic operator: 4 inputs -> 1 output.

        Step 1: BHML[being][doing]       -> intermediate
        Step 2: BHML[intermediate][becoming] -> triadic
        Step 3: BHML[triadic][context]   -> output

        If DKAN is grokked, use DKAN forward instead of raw BHML.
        """
        # Check DKAN availability
        dkan = self._get_dkan()
        if dkan is not None:
            return self._dkan_compose(dkan, being_key, doing_key,
                                      becoming_key, context_key)

        # Pure BHML path
        intermediate = BHML[being_key][doing_key]
        triadic = BHML[intermediate][becoming_key]
        output = BHML[triadic][context_key]
        return output

    def _get_dkan(self):
        """Return DKAN trainer if grokked, else None."""
        if self.engine is None:
            return None
        dkan = getattr(self.engine, 'dkan_trainer', None)
        if dkan is None:
            return None
        state = getattr(dkan, '_state', None)
        if state and getattr(state, 'grokked', False):
            return dkan
        # Check IPR > 0.5 as secondary signal
        if state and state.ipr_history and state.ipr_history[-1] > 0.5:
            return dkan
        return None

    def _dkan_compose(self, dkan, b: int, d: int, bc: int, ctx: int) -> int:
        """Use DKAN's evolved lattice chain for composition.

        The DKAN has learned experience-shaped CL variants.
        We compose through the learned table instead of frozen BHML.
        """
        # Access evolved node tables from lattice chain
        lc = getattr(self.engine, 'lattice_chain', None)
        if lc is None:
            return BHML[BHML[BHML[b][d]][bc]][ctx]

        # Compose through evolved tables if available
        nodes = getattr(lc, 'nodes', None)
        if nodes and len(nodes) > 0:
            # Use the most-observed node's table (highest temper)
            best_node = max(nodes.values(),
                           key=lambda n: getattr(n, 'temper', 0),
                           default=None)
            if best_node is not None:
                tbl = getattr(best_node, 'table', None)
                if tbl is not None and len(tbl) == NUM_OPS:
                    inter = tbl[b][d]
                    tri = tbl[inter][bc]
                    return tbl[tri][ctx]

        return BHML[BHML[BHML[b][d]][bc]][ctx]

    def _get_context_key(self) -> int:
        """Pull context key from divine memory / olfactory resonance."""
        if self.engine is None:
            return BALANCE

        # Olfactory resonance nodes = confirmed experience patterns
        olfa = getattr(self.engine, 'olfactory', None)
        if olfa is not None:
            try:
                nodes = olfa.get_resonance_nodes(top_k=1)
                if nodes:
                    # Resonance node is a centroid -> classify its dominant dim
                    centroid = nodes[0]
                    if hasattr(centroid, '__len__') and len(centroid) >= 5:
                        mx = max(range(5), key=lambda i: abs(centroid[i]))
                        sign = 0 if centroid[mx] >= 0 else 1
                        return D2_OP_MAP[mx][sign]
            except Exception:
                pass

        # Fallback: generator paths -> most frequent transition target
        gp = getattr(self.engine, 'generator_paths', None)
        if gp is not None and hasattr(gp, 'shape') and gp.shape[0] == NUM_OPS:
            row_sums = gp.sum(axis=1)
            if row_sums.max() > 0:
                return int(row_sums.argmax())

        return BALANCE

    def compose_response(self, input_triad: dict) -> List[int]:
        """Generate response semantic keys from input classification.

        Uses quadratic operator + divine memory context.
        Returns list of output keys (3 minimum: S-V-O).
        """
        ctx = self._get_context_key()
        b = input_triad['being']
        d = input_triad['doing']
        bc = input_triad['becoming']

        # Core triad response through quadratic
        subj_key = self.compose_quadratic(b, d, bc, ctx)
        verb_key = self.compose_quadratic(d, bc, b, ctx)
        obj_key = self.compose_quadratic(bc, b, d, ctx)

        keys = [subj_key, verb_key, obj_key]

        # Add modifier keys if input had modifiers
        for _, mod_key, _ in self.classify_phrase(
                input_triad.get('words', [])):
            composed = BHML[mod_key][ctx]
            if composed not in keys:
                keys.append(composed)
            if len(keys) >= 7:
                break

        return keys

    # ============================================================
    # BECOMING: Select English words from semantic keys
    # ============================================================

    def select_word(self, semantic_key: int, pos: str = None,
                    context_keys: List[int] = None) -> str:
        """Select an English word for a semantic key.

        1. Get all words in the cluster for this key
        2. Filter by POS if specified
        3. Prefer words with higher confidence
        4. Prefer words that co-occurred with context keys
        """
        candidates = list(self._key_to_words.get(semantic_key, []))
        if not candidates:
            return OP_NAMES[semantic_key].lower()

        # Filter by POS
        if pos:
            filtered = [w for w in candidates if self._guess_pos(w) == pos]
            if filtered:
                candidates = filtered

        # Score by confidence + context affinity
        scored = []
        for w in candidates:
            score = self._confidence.get(w, 0.3)
            if context_keys:
                for ck in context_keys:
                    pair = (w, OP_NAMES[ck].lower())
                    if pair in self._learned_pairs:
                        score += 0.2
            scored.append((score, w))

        scored.sort(reverse=True)
        return scored[0][1]

    def compose_english(self, response_keys: List[int],
                        input_triad: dict) -> str:
        """Build English sentence from response keys + grammar.

        S-V-O from TIG triad:
        - Key 0 -> subject noun
        - Key 1 -> verb
        - Key 2 -> object noun
        Remaining keys -> modifiers.
        """
        if not response_keys:
            return ''

        ctx = response_keys  # all keys as context for each selection
        parts = []

        # Subject
        if len(response_keys) > 0:
            parts.append(self.select_word(response_keys[0], 'noun', ctx))

        # Verb
        if len(response_keys) > 1:
            parts.append(self.select_word(response_keys[1], 'verb', ctx))

        # Object
        if len(response_keys) > 2:
            parts.append(self.select_word(response_keys[2], 'noun', ctx))

        # Extra modifiers
        for k in response_keys[3:]:
            w = self.select_word(k, 'adj', ctx)
            if w not in parts:
                parts.append(w)

        return ' '.join(parts)

    # ============================================================
    # FEEDBACK: Record and learn
    # ============================================================

    def record(self, input_text: str, input_keys: List[int],
               output_keys: List[int], output_text: str):
        """Record this translation as divine code + learn from it.

        Feeds the lattice chain: input_keys -> output_keys = path.
        """
        # Learn word-key associations from this exchange
        in_words = re.findall(r"[a-zA-Z']+", input_text)
        for w, k in zip(in_words, input_keys):
            self.learn_word(w, k, 0.5)

        out_words = output_text.split()
        for w, k in zip(out_words, output_keys):
            self.learn_word(w, k, 0.6)

        # Learn pair compositions
        for i in range(len(input_keys) - 1):
            if i < len(in_words) - 1:
                composed = BHML[input_keys[i]][input_keys[i + 1]]
                self.learn_pair(in_words[i], in_words[i + 1], composed)

        # Feed lattice chain if available
        if self.engine:
            lc = getattr(self.engine, 'lattice_chain', None)
            if lc and hasattr(lc, 'walk'):
                try:
                    lc.walk(input_keys + output_keys)
                except Exception:
                    pass

    def learn_word(self, word: str, semantic_key: int,
                   confidence: float = 1.0):
        """Learn or update a word's semantic mapping."""
        w = word.lower().strip()
        if not w or not w.isalpha():
            return
        key = max(0, min(NUM_OPS - 1, semantic_key))

        old_key = self._word_to_key.get(w)
        old_conf = self._confidence.get(w, 0.0)

        # Higher confidence wins; equal confidence -> newer wins
        if old_key is not None and old_conf > confidence:
            return

        # Remove from old cluster
        if old_key is not None and old_key != key:
            try:
                self._key_to_words[old_key].remove(w)
            except ValueError:
                pass

        self._word_to_key[w] = key
        self._confidence[w] = max(old_conf, confidence)
        if w not in self._key_to_words[key]:
            self._key_to_words[key].append(w)

    def learn_pair(self, word1: str, word2: str, composed_key: int):
        """Learn a two-word composition result."""
        self._learned_pairs[(word1.lower(), word2.lower())] = composed_key

    # ============================================================
    # MAIN ENTRY POINT
    # ============================================================

    def translate(self, text: str) -> str:
        """Full TIG cycle: Being -> Doing -> Becoming -> English.

        1. BEING:     Classify input at all fractal levels
        2. DOING:     Compose through quadratic operator (DKAN or BHML)
        3. BECOMING:  Select English words from output keys
        4. FEEDBACK:  Record as divine code, update learned mappings

        Returns English response string.
        """
        if not text or not text.strip():
            return ''

        # Split into sentences for recursive composition
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return ''

        # Single sentence: direct TIG cycle
        if len(sentences) == 1:
            return self._translate_sentence(sentences[0])

        # Multiple sentences: recursive fractal composition
        return self._translate_paragraph(sentences)

    def _translate_sentence(self, text: str) -> str:
        """TIG cycle for one sentence."""
        # BEING
        triad = self.classify_sentence(text)

        # DOING
        response_keys = self.compose_response(triad)

        # BECOMING
        english = self.compose_english(response_keys, triad)

        # FEEDBACK
        self.record(text, triad['raw_keys'], response_keys, english)

        return english

    def _translate_paragraph(self, sentences: List[str]) -> str:
        """Recursive composition of multiple sentence triads."""
        triads = [self.classify_sentence(s) for s in sentences]
        responses = []

        # Compose sentence triads recursively:
        # Each sentence's becoming feeds next sentence's being context
        running_ctx = BALANCE
        for i, triad in enumerate(triads):
            ctx = running_ctx
            b, d, bc = triad['being'], triad['doing'], triad['becoming']

            subj = self.compose_quadratic(b, d, bc, ctx)
            verb = self.compose_quadratic(d, bc, b, ctx)
            obj = self.compose_quadratic(bc, b, d, ctx)
            response_keys = [subj, verb, obj]

            english = self.compose_english(response_keys, triad)
            responses.append(english)

            # Feed forward: becoming -> context of next
            running_ctx = obj

            self.record(sentences[i], triad['raw_keys'],
                       response_keys, english)

        return '. '.join(responses)

    # ============================================================
    # PERSISTENCE
    # ============================================================

    def save(self, path: str = '~/.ck/semantic_engine.json'):
        """Save learned word mappings, pair compositions."""
        path = os.path.expanduser(path)
        os.makedirs(os.path.dirname(path), exist_ok=True)

        data = {
            'word_to_key': self._word_to_key,
            'confidence': self._confidence,
            'learned_pairs': {
                f'{w1}|{w2}': k
                for (w1, w2), k in self._learned_pairs.items()
            },
        }
        with open(path, 'w') as f:
            json.dump(data, f, indent=1)

    def load(self, path: str = '~/.ck/semantic_engine.json'):
        """Load from disk. Merges with seed vocabulary."""
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            return

        with open(path) as f:
            data = json.load(f)

        # Rebuild from saved data
        for word, key in data.get('word_to_key', {}).items():
            conf = data.get('confidence', {}).get(word, 0.5)
            self.learn_word(word, int(key), conf)

        for pair_str, key in data.get('learned_pairs', {}).items():
            parts = pair_str.split('|', 1)
            if len(parts) == 2:
                self._learned_pairs[(parts[0], parts[1])] = int(key)

    def summary(self) -> dict:
        """Status for API."""
        total_words = len(self._word_to_key)
        seed_count = sum(len(ws) for ws in _SEED.values())
        learned_count = total_words - seed_count
        dkan_active = self._get_dkan() is not None

        return {
            'total_words': total_words,
            'seed_words': seed_count,
            'learned_words': max(0, learned_count),
            'learned_pairs': len(self._learned_pairs),
            'dkan_active': dkan_active,
            'clusters': {
                OP_NAMES[i]: len(self._key_to_words[i])
                for i in range(NUM_OPS)
            },
        }
