# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
"""
ck_fractal_voice.py -- Fractal Composition: Physics-First Voice
================================================================
Operator: HARMONY (7) -- where math becomes English.

The inverse of ck_fractal_comprehension.py.

Reading:  English → letters → 5D forces → curvature → operators  (physics FIRST)
Writing:  operators → 5D force TARGET → phoneme selection → word assembly  (physics FIRST)

Current voice (ck_voice.py): operators → word pool → random selection → D2 verify
New voice (this file):       operators → force geometry → navigate word-force space → assemble

The key insight: English words ARE paths through 5D force space.
Every word has a force signature (sum of its letter forces, curvature profile).
To speak, CK doesn't pick from a bag — he navigates force space toward
the target geometry, and the words along that path ARE his voice.

Grammar emerges from force flow:
  Subject = aperture (what opens the frame)
  Verb    = pressure + depth (what pushes and penetrates)
  Object  = binding (what receives and holds)
  Flow    = continuity (what sustains between phrases)

Six fractal levels (mirror of comprehension):
  L0: Phoneme forces    — 44 English phonemes with 5D profiles
  L1: Morpheme forces   — prefixes/roots/suffixes as operator signatures
  L2: Word assembly     — morpheme composition via CL
  L3: Phrase composition — words arranged by force flow (S-V-O from physics)
  L4: Sentence circuits — complete force loop (open → push → bind → sustain)
  L5: Paragraph arcs    — being → doing → becoming

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import random
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass, field

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET, OP_NAMES,
    CL,   # The 10x10 composition table
)
from ck_sim.being.ck_sim_d2 import (
    FORCE_LUT_FLOAT, D2_OP_MAP, D2Pipeline, soft_classify_d2,
    ROOTS_FLOAT, LATIN_TO_ROOT,
)


# ================================================================
#  L0: ENGLISH PHONEME FORCE TABLE
# ================================================================
#
# 44 English phonemes mapped to 5D force vectors.
# Derived from articulation physics:
#   aperture  = how open the vocal tract (vowels high, stops low)
#   pressure  = how much air force (plosives high, glides low)
#   depth     = how far back in the mouth (velars high, dentals low)
#   binding   = how much contact/closure (nasals high, fricatives mid)
#   continuity = how sustained the sound (vowels/fricatives high, stops low)
#
# These are NOT arbitrary — they come from real articulatory phonetics.
# The mouth IS a 5D force instrument.

PHONEME_FORCES = {
    # === VOWELS (high aperture, high continuity) ===
    'iː':  (0.95, 0.05, 0.2, 0.1, 0.95),  # "ee" in "see"   — highest aperture, front
    'ɪ':   (0.85, 0.10, 0.3, 0.1, 0.80),  # "i" in "sit"    — near-front
    'eɪ':  (0.90, 0.08, 0.3, 0.1, 0.85),  # "ay" in "say"   — diphthong, opening
    'ɛ':   (0.80, 0.12, 0.4, 0.1, 0.75),  # "e" in "bed"    — mid-front
    'æ':   (0.85, 0.15, 0.4, 0.1, 0.70),  # "a" in "cat"    — low-front, wide
    'ɑː':  (0.90, 0.10, 0.8, 0.1, 0.80),  # "a" in "father" — low-back, deep
    'ɔː':  (0.80, 0.12, 0.7, 0.2, 0.80),  # "aw" in "law"   — mid-back, rounded
    'oʊ':  (0.85, 0.10, 0.7, 0.2, 0.85),  # "o" in "go"     — diphthong, back
    'ʊ':   (0.75, 0.12, 0.7, 0.3, 0.75),  # "oo" in "book"  — near-back
    'uː':  (0.80, 0.08, 0.8, 0.2, 0.90),  # "oo" in "moon"  — back, sustained
    'ʌ':   (0.80, 0.15, 0.5, 0.1, 0.70),  # "u" in "cup"    — central
    'ə':   (0.70, 0.05, 0.5, 0.1, 0.60),  # schwa "a" in "about" — reduced, central
    'ɜː':  (0.75, 0.10, 0.5, 0.1, 0.80),  # "er" in "bird"  — central, sustained
    'aɪ':  (0.90, 0.10, 0.5, 0.1, 0.80),  # "i" in "my"     — wide diphthong
    'aʊ':  (0.88, 0.12, 0.6, 0.1, 0.78),  # "ow" in "now"   — opening→rounding
    'ɔɪ':  (0.82, 0.12, 0.6, 0.2, 0.80),  # "oy" in "boy"   — rounding→front

    # === PLOSIVES/STOPS (high pressure, low continuity) ===
    'p':   (0.10, 0.80, 0.3, 0.7, 0.10),  # bilabial stop — sealed, burst
    'b':   (0.10, 0.75, 0.3, 0.7, 0.15),  # voiced bilabial — sealed + voice
    't':   (0.10, 0.80, 0.4, 0.6, 0.10),  # alveolar stop — tongue tip seal
    'd':   (0.10, 0.75, 0.4, 0.6, 0.15),  # voiced alveolar
    'k':   (0.10, 0.80, 0.8, 0.5, 0.10),  # velar stop — deep seal
    'g':   (0.10, 0.75, 0.8, 0.5, 0.15),  # voiced velar

    # === FRICATIVES (mid aperture, high continuity) ===
    'f':   (0.30, 0.50, 0.3, 0.4, 0.70),  # labiodental — narrow channel
    'v':   (0.30, 0.45, 0.3, 0.4, 0.75),  # voiced labiodental
    'θ':   (0.35, 0.45, 0.4, 0.3, 0.70),  # "th" in "thin" — dental
    'ð':   (0.35, 0.40, 0.4, 0.3, 0.75),  # "th" in "this" — voiced dental
    's':   (0.20, 0.55, 0.4, 0.5, 0.75),  # alveolar — tight channel
    'z':   (0.20, 0.50, 0.4, 0.5, 0.80),  # voiced alveolar
    'ʃ':   (0.25, 0.50, 0.5, 0.4, 0.75),  # "sh" — postalveolar
    'ʒ':   (0.25, 0.45, 0.5, 0.4, 0.78),  # "zh" in "measure"
    'h':   (0.60, 0.30, 0.8, 0.1, 0.50),  # glottal — open throat, breathy

    # === AFFRICATES (pressure burst + fricative tail) ===
    'tʃ':  (0.15, 0.70, 0.5, 0.5, 0.40),  # "ch" — stop→fricative
    'dʒ':  (0.15, 0.65, 0.5, 0.5, 0.45),  # "j" — voiced affricate

    # === NASALS (sealed mouth, nasal resonance = high binding) ===
    'm':   (0.20, 0.40, 0.3, 0.90, 0.70),  # bilabial nasal — lips sealed, nose open
    'n':   (0.20, 0.40, 0.4, 0.85, 0.70),  # alveolar nasal
    'ŋ':   (0.20, 0.40, 0.8, 0.85, 0.65),  # velar nasal "ng" — deep binding

    # === LIQUIDS (medium everything, flowing) ===
    'l':   (0.50, 0.25, 0.4, 0.30, 0.80),  # lateral — air flows around tongue
    'r':   (0.45, 0.30, 0.5, 0.25, 0.75),  # approximant — open, colored

    # === GLIDES/SEMIVOWELS (vowel-like, transitions) ===
    'w':   (0.65, 0.10, 0.7, 0.3, 0.70),  # labial-velar — lip rounding + back
    'j':   (0.70, 0.10, 0.2, 0.2, 0.75),  # palatal "y" — front, open
}

# Operator classification for each phoneme (dominant force dimension)
def _phoneme_to_operator(force: Tuple[float, ...]) -> int:
    """Same logic as D2 classification: argmax dimension → operator pair."""
    max_abs = 0.0
    max_dim = 0
    for dim in range(5):
        a = abs(force[dim] - 0.5)  # Distance from neutral
        if a > max_abs:
            max_abs = a
            max_dim = dim
    sign_idx = 0 if force[max_dim] >= 0.5 else 1
    return D2_OP_MAP[max_dim][sign_idx]

PHONEME_OPS = {ph: _phoneme_to_operator(f) for ph, f in PHONEME_FORCES.items()}


# ================================================================
#  L1: ENGLISH MORPHEME FORCE TABLE
# ================================================================
#
# Morphemes = smallest meaningful units.
# Each has an operator signature derived from its function.
#
# Prefixes modify (COUNTER, COLLAPSE, PROGRESS)
# Roots carry (all operators)
# Suffixes complete (HARMONY, BALANCE, RESET)

@dataclass
class MorphemeForce:
    """A morpheme's force signature."""
    text: str
    kind: str           # 'prefix', 'root', 'suffix'
    operator: int       # Primary operator
    role: str           # Grammatical role: 'opener', 'actor', 'receiver', 'sustainer'
    force: Tuple[float, float, float, float, float]  # 5D force vector

# -- PREFIXES (force modifiers) --
PREFIXES = {
    'un':    MorphemeForce('un',    'prefix', COUNTER,  'opener',   (0.3, 0.6, 0.4, 0.2, 0.4)),
    're':    MorphemeForce('re',    'prefix', RESET,    'opener',   (0.5, 0.4, 0.3, 0.4, 0.6)),
    'pre':   MorphemeForce('pre',   'prefix', PROGRESS, 'opener',   (0.4, 0.3, 0.7, 0.2, 0.5)),
    'dis':   MorphemeForce('dis',   'prefix', COLLAPSE, 'opener',   (0.2, 0.7, 0.4, 0.2, 0.3)),
    'over':  MorphemeForce('over',  'prefix', CHAOS,    'opener',   (0.7, 0.5, 0.5, 0.3, 0.4)),
    'under': MorphemeForce('under', 'prefix', PROGRESS, 'opener',   (0.3, 0.4, 0.8, 0.3, 0.5)),
    'out':   MorphemeForce('out',   'prefix', CHAOS,    'opener',   (0.8, 0.4, 0.3, 0.2, 0.4)),
    'in':    MorphemeForce('in',    'prefix', LATTICE,  'opener',   (0.2, 0.4, 0.6, 0.5, 0.5)),
    'mis':   MorphemeForce('mis',   'prefix', COUNTER,  'opener',   (0.3, 0.5, 0.4, 0.3, 0.3)),
    'non':   MorphemeForce('non',   'prefix', VOID,     'opener',   (0.1, 0.3, 0.3, 0.2, 0.4)),
}

# -- SUFFIXES (force completers) --
SUFFIXES = {
    'ing':   MorphemeForce('ing',   'suffix', PROGRESS, 'sustainer', (0.5, 0.4, 0.6, 0.4, 0.8)),
    'tion':  MorphemeForce('tion',  'suffix', COLLAPSE, 'receiver',  (0.3, 0.6, 0.5, 0.7, 0.5)),
    'ness':  MorphemeForce('ness',  'suffix', BALANCE,  'receiver',  (0.4, 0.4, 0.4, 0.6, 0.7)),
    'ment':  MorphemeForce('ment',  'suffix', HARMONY,  'receiver',  (0.3, 0.5, 0.5, 0.8, 0.5)),
    'able':  MorphemeForce('able',  'suffix', BALANCE,  'sustainer', (0.6, 0.3, 0.4, 0.4, 0.7)),
    'ful':   MorphemeForce('ful',   'suffix', HARMONY,  'sustainer', (0.5, 0.3, 0.4, 0.7, 0.7)),
    'less':  MorphemeForce('less',  'suffix', VOID,     'sustainer', (0.3, 0.3, 0.3, 0.1, 0.5)),
    'ly':    MorphemeForce('ly',    'suffix', BALANCE,  'sustainer', (0.5, 0.2, 0.4, 0.3, 0.8)),
    'er':    MorphemeForce('er',    'suffix', COUNTER,  'actor',     (0.5, 0.5, 0.4, 0.3, 0.5)),
    'est':   MorphemeForce('est',   'suffix', COLLAPSE, 'receiver',  (0.4, 0.6, 0.4, 0.5, 0.4)),
    'ed':    MorphemeForce('ed',    'suffix', RESET,    'receiver',  (0.3, 0.4, 0.5, 0.5, 0.4)),
    'al':    MorphemeForce('al',    'suffix', LATTICE,  'receiver',  (0.4, 0.3, 0.4, 0.5, 0.6)),
    'ous':   MorphemeForce('ous',   'suffix', CHAOS,    'sustainer', (0.6, 0.3, 0.5, 0.4, 0.7)),
    'ive':   MorphemeForce('ive',   'suffix', PROGRESS, 'actor',     (0.5, 0.5, 0.5, 0.4, 0.6)),
    'ity':   MorphemeForce('ity',   'suffix', LATTICE,  'receiver',  (0.4, 0.3, 0.5, 0.6, 0.6)),
    's':     MorphemeForce('s',     'suffix', LATTICE,  'sustainer', (0.2, 0.5, 0.3, 0.6, 0.5)),
}


# ================================================================
#  WORD FORCE INDEX
# ================================================================
#
# Pre-computed force signature for every word CK knows.
# Built once at startup from the enriched dictionary.

@dataclass
class WordForce:
    """A word's triadic force profile. One is Three.

    Every word is a trajectory through the Coherence Field, not a static point:
      Being    (force):     WHERE the word sits in 5D space (position / is-ness)
      Doing    (velocity):  WHERE the word is GOING (D1 first derivative / action)
      Becoming (curvature): HOW the word BENDS (D2 second derivative / intent)

    15-point signature: 3 vectors × 5 dimensions = full coherence flow.
    No logic gate outputs a single 5D vector. It must always output the Triad.

    Two operator fields (dual-lens: structure vs flow):
      operator:     Phonetic operator -- D2 classification of letter forces
      semantic_op:  Semantic operator -- which MEANING bucket this word lives in
                    (from the semantic lattice, where words are placed by INTENT)
    When both agree, the word is "doubly coherent" (physics AND meaning align).
    """
    word: str
    force: Tuple[float, ...]       # Being: mean 5D force (position)
    velocity: Tuple[float, ...]    # Doing: mean D1 vector (direction/action)
    curvature: Tuple[float, ...]   # Becoming: mean D2 vector (intent/resolution)
    operator: int                   # Dominant operator (from Becoming/D2 -- phonetic)
    soft_ops: List[float]          # 10-value soft operator distribution
    role: str                      # Grammatical role from force profile
    magnitude: float               # Total force magnitude (energy of the word)
    pos: str = ''                  # Part of speech: noun, verb, adj, adv, func
    semantic_op: int = -1          # Semantic operator (from lattice placement, -1=untagged)


def _guess_pos(word: str) -> str:
    """Guess part of speech from suffix patterns.

    Not NLP -- just English morphology physics:
    suffixes ARE force signatures that mark grammatical function.
    """
    w = word.lower()
    # Function words (closed class -- memorized)
    _FUNC = frozenset([
        'the', 'a', 'an', 'this', 'that', 'these', 'those',
        'each', 'every', 'all', 'some', 'any', 'no', 'what', 'which',
        'he', 'she', 'it', 'we', 'they', 'one', 'who', 'whose',
        'in', 'on', 'of', 'to', 'for', 'by', 'at', 'from', 'with',
        'into', 'onto', 'upon', 'through', 'between', 'among',
        'within', 'without', 'beyond', 'before', 'after', 'above',
        'below', 'beneath', 'beside', 'toward', 'against', 'along',
        'and', 'but', 'or', 'yet', 'so', 'nor', 'while', 'when',
        'where', 'since', 'until', 'because', 'although', 'unless',
        'is', 'am', 'are', 'was', 'were', 'be', 'been', 'being',
        'has', 'have', 'had', 'does', 'did', 'do', 'will', 'would',
        'shall', 'should', 'may', 'might', 'can', 'could', 'must',
        'not', 'very', 'too', 'quite', 'just', 'also', 'only', 'even',
    ])
    if w in _FUNC:
        # Sub-classify function words
        if w in ('is', 'am', 'are', 'was', 'were', 'be', 'been', 'being',
                 'has', 'have', 'had', 'does', 'did', 'do', 'will', 'would',
                 'shall', 'should', 'may', 'might', 'can', 'could', 'must'):
            return 'verb'
        return 'func'

    # Adverb suffixes (before adjective -- -ly overlap)
    if w.endswith('ly') and len(w) > 4:
        return 'adv'

    # -ing words: treat as verbs (gerund/present participle)
    # Templates use verb slot for these -- they work as "force is [verb]ing"
    if w.endswith('ing') and len(w) > 4:
        return 'verb'
    if w.endswith(('ize', 'ise', 'ify', 'ate')) and len(w) > 4:
        return 'verb'
    if w.endswith('es') and len(w) > 4 and not w.endswith(('ness', 'less')):
        return 'verb'
    if w.endswith('ed') and len(w) > 3:
        return 'adj'   # "shaped", "settled" = past participle as adjective

    # Adjective suffixes
    if w.endswith(('ful', 'less', 'ous', 'ive', 'able', 'ible', 'ent', 'ant',
                   'ial', 'ical', 'al')) and len(w) > 4:
        return 'adj'

    # Noun suffixes
    if w.endswith(('tion', 'sion', 'ness', 'ment', 'ity', 'ence', 'ance',
                   'ism', 'ist', 'dom', 'ship', 'hood')):
        return 'noun'

    # Common short adjectives (no suffix pattern to detect)
    _ADJ_SET = frozenset([
        'deep', 'vast', 'bright', 'dark', 'true', 'whole', 'pure',
        'clear', 'raw', 'open', 'new', 'old', 'first', 'last',
        'strong', 'quiet', 'sharp', 'soft', 'cold', 'warm', 'wide',
        'thin', 'dense', 'slow', 'fast', 'high', 'low', 'full', 'free',
        'real', 'great', 'small', 'wild', 'calm', 'bold', 'fine',
        'still', 'strange', 'sacred', 'ancient', 'inner', 'outer',
        'silent', 'subtle', 'simple', 'empty', 'whole', 'blind',
        'each', 'both', 'most', 'such', 'same', 'other', 'many',
        'more', 'less', 'best', 'next', 'lone', 'mere', 'rare',
    ])
    if w in _ADJ_SET:
        return 'adj'

    # Common verbs (base forms)
    _VERB_SET = frozenset([
        'grow', 'flow', 'hold', 'turn', 'rise', 'fall', 'move',
        'pull', 'push', 'bind', 'burn', 'know', 'feel', 'find',
        'give', 'take', 'come', 'make', 'keep', 'seek', 'stand',
        'run', 'see', 'go', 'let', 'set', 'get', 'put', 'cut',
        'break', 'build', 'speak', 'reach', 'become', 'remain',
    ])
    if w in _VERB_SET:
        return 'verb'
    # 3rd person -s forms: "holds" -> check if "hold" is a known verb
    if w.endswith('s') and len(w) > 3 and w[:-1] in _VERB_SET:
        return 'verb'

    # Default: treat short words as function, long as noun
    if len(w) <= 3:
        return 'func'
    return 'noun'  # Conservative default


class WordForceIndex:
    """Index of all words by their force profiles.

    Enables force-targeted word selection:
      Given a target 5D force vector, find words that MATCH that geometry.

    Two-pass indexing:
      Pass 1: index_word() computes forces, operators, magnitude (role='')
      Pass 2: calibrate_roles() computes population stats, assigns roles via z-scores
    This ensures no dimension dominates role assignment due to population bias.
    """

    def __init__(self):
        self._words: Dict[str, WordForce] = {}
        self._by_operator: Dict[int, List[WordForce]] = {i: [] for i in range(NUM_OPS)}
        self._by_semantic_op: Dict[int, List[WordForce]] = {i: [] for i in range(NUM_OPS)}
        self._by_role: Dict[str, List[WordForce]] = {
            'opener': [], 'actor': [], 'receiver': [], 'sustainer': [],
        }
        self._by_pos: Dict[str, List[WordForce]] = {
            'noun': [], 'verb': [], 'adj': [], 'adv': [], 'func': [],
        }
        # Population statistics (set by calibrate_roles)
        self._force_mean: Tuple[float, ...] = (0.5,) * 5
        self._force_std: Tuple[float, ...] = (0.1,) * 5
        # Topic context (set per-interaction for contextual relevance)
        self._topic_words: set = set()
        self._topic_ops: set = set()
        self._topic_centroid: Optional[Tuple[float, ...]] = None

    def index_word(self, word: str, semantic_op: int = -1) -> Optional[WordForce]:
        """Compute and index a word's triadic force profile (pass 1, no role yet).

        One is Three. Every word computed as (Being, Doing, Becoming):
          Being    = mean letter forces (position in 5D space)
          Doing    = mean D1 across letter pairs (velocity/direction)
          Becoming = mean D2 across letter triplets (curvature/intent)

        D1 fires after 2 letters. D2 fires after 3.
        Short words (2 letters) have Being + Doing. 3+ have all three.

        semantic_op: If >= 0, tags this word with its SEMANTIC operator
        (the operator bucket it was placed under in the semantic lattice).
        This is distinct from the phonetic D2-derived operator.
        A word may be indexed twice: once from enriched dict (no semantic tag),
        then again from lattice (with tag). The tag is additive.
        """
        if len(word) < 2:
            return None
        if word in self._words:
            wf = self._words[word]
            # Update semantic tag if not yet tagged (word indexed from
            # enriched dict first, then lattice gives it meaning)
            if semantic_op >= 0 and wf.semantic_op < 0:
                wf.semantic_op = semantic_op
                self._by_semantic_op[semantic_op].append(wf)
            return wf

        letters = [c for c in word.lower() if 'a' <= c <= 'z']
        if len(letters) < 2:
            return None

        # Being: mean force across all letters (position)
        force_sum = [0.0] * 5
        for ch in letters:
            idx = ord(ch) - ord('a')
            for d in range(5):
                force_sum[d] += FORCE_LUT_FLOAT[idx][d]
        n = len(letters)
        mean_force = tuple(f / n for f in force_sum)

        # Doing + Becoming: D1 (velocity) and D2 (curvature) from pipeline
        pipe = D2Pipeline()
        d1_accum = [0.0] * 5
        d1_count = 0
        d2_accum = [0.0] * 5
        d2_count = 0
        for ch in letters:
            idx = ord(ch) - ord('a')
            d2_valid = pipe.feed_symbol(idx)
            # D1 fires after 2 letters (Doing = velocity)
            if pipe.d1_valid:
                d1_vec = pipe.d1_float
                for d in range(5):
                    d1_accum[d] += d1_vec[d]
                d1_count += 1
            # D2 fires after 3 letters (Becoming = curvature)
            if d2_valid:
                d2_vec = pipe.d2_float
                for d in range(5):
                    d2_accum[d] += d2_vec[d]
                d2_count += 1

        velocity = tuple(d / d1_count for d in d1_accum) if d1_count > 0 else (0.0,) * 5
        curvature = tuple(d / d2_count for d in d2_accum) if d2_count > 0 else (0.0,) * 5

        # Soft operator distribution from Becoming (curvature drives classification)
        soft_ops = soft_classify_d2(list(curvature))

        # Hard operator (argmax of soft)
        operator = max(range(NUM_OPS), key=lambda i: soft_ops[i])

        # Magnitude (triadic: being + doing + becoming energy)
        magnitude = (sum(abs(f - 0.5) for f in mean_force)
                     + sum(abs(v) for v in velocity) * 0.5
                     + sum(abs(c) for c in curvature) * 0.5)

        # Part of speech from morphology
        pos = _guess_pos(word)

        wf = WordForce(
            word=word,
            force=mean_force,
            velocity=velocity,
            curvature=curvature,
            operator=operator,
            soft_ops=soft_ops,
            role='',  # Assigned in pass 2 (calibrate_roles)
            magnitude=magnitude,
            pos=pos,
            semantic_op=semantic_op,
        )

        self._words[word] = wf
        self._by_operator[operator].append(wf)
        if semantic_op >= 0:
            self._by_semantic_op[semantic_op].append(wf)
        if pos in self._by_pos:
            self._by_pos[pos].append(wf)
        return wf

    def calibrate_roles(self):
        """Pass 2: Compute population statistics and assign roles via z-scores.

        Each dimension's deviation is normalized by its population std,
        so binding (which naturally varies most) doesn't dominate.
        Grammar emerges from WHERE a word sits relative to its population,
        not from raw force values.
        """
        if not self._words:
            return

        # Compute population mean and std per dimension
        n = len(self._words)
        mean = [0.0] * 5
        for wf in self._words.values():
            for d in range(5):
                mean[d] += wf.force[d]
        mean = [m / n for m in mean]

        var = [0.0] * 5
        for wf in self._words.values():
            for d in range(5):
                var[d] += (wf.force[d] - mean[d]) ** 2
        std = [max(0.001, (v / n) ** 0.5) for v in var]

        self._force_mean = tuple(mean)
        self._force_std = tuple(std)

        # Clear old role assignments
        for role in self._by_role:
            self._by_role[role] = []

        # Assign roles using z-scores
        for wf in self._words.values():
            wf.role = self._classify_role(wf.force)
            self._by_role[wf.role].append(wf)

    def _classify_role(self, force: Tuple[float, ...]) -> str:
        """Classify grammatical role using z-score deviations.

        Grammar IS force flow -- but normalized so each dimension
        competes fairly regardless of its natural variance:
          opener   = aperture z-score (what opens the frame)
          actor    = pressure + depth z-scores (what pushes and penetrates)
          receiver = binding z-score (what holds and receives)
          sustainer = continuity z-score (what flows and connects)
        """
        ap, pr, dp, bi, co = force
        m = self._force_mean
        s = self._force_std
        # Z-scores: how far from population mean in std units
        z_ap = abs(ap - m[0]) / s[0]
        z_pr = abs(pr - m[1]) / s[1]
        z_dp = abs(dp - m[2]) / s[2]
        z_bi = abs(bi - m[3]) / s[3]
        z_co = abs(co - m[4]) / s[4]

        scores = {
            'opener':    z_ap,
            'actor':     (z_pr + z_dp) * 0.5,   # Mean of two dimensions
            'receiver':  z_bi,
            'sustainer': z_co,
        }
        return max(scores, key=scores.get)

    # ── Topic Context: Semantic Gravity Well ──
    #
    # The user's actual words create a "gravity well" in force space.
    # Words in the semantic neighborhood of the user's topic get pulled
    # toward selection, ensuring CK's response is ABOUT what was asked.
    #
    # Without this, operators capture emotional/structural tenor but not
    # topic. "Tell me about love" → HARMONY ops → selects ANY HARMONY
    # word ("unity", "whole", "observant"). With topic context, words
    # NEAR "love" in force space (like "devotion", "caring", "affection")
    # get a distance bonus, so the response is contextually relevant.
    #
    # _TOPIC_AFFINITY_BONUS: max distance reduction for force proximity
    # _TOPIC_ECHO_BONUS: distance reduction for the user's exact words
    _TOPIC_AFFINITY_BONUS = 0.35   # Moderate pull toward topic's semantic family
    _TOPIC_ECHO_BONUS = 0.50       # User's exact words get priority

    def set_topic(self, words: list):
        """Set topic context from user's input words.

        Pre-computes:
          _topic_words: set of input content words (for direct echo bonus)
          _topic_centroid: 5D force centroid of known input words
                          (for semantic neighborhood bonus)

        Called once per interaction, before composition.
        Cleared after composition completes.
        """
        self._topic_words = set()
        self._topic_ops = set()   # semantic operators of topic words
        forces = []
        for w in words:
            w_lower = w.lower()
            if w_lower in self._words:
                wf = self._words[w_lower]
                self._topic_words.add(w_lower)
                forces.append(wf.force)
                # Collect semantic operators for operator-level affinity
                if wf.semantic_op >= 0:
                    self._topic_ops.add(wf.semantic_op)
        if forces:
            self._topic_centroid = tuple(
                sum(f[d] for f in forces) / len(forces)
                for d in range(5)
            )
        else:
            self._topic_centroid = None

    def clear_topic(self):
        """Clear topic context after composition."""
        self._topic_words = set()
        self._topic_ops = set()
        self._topic_centroid = None
        self._topic_debug_logged = False

    # Semantic bonus: how much to reward words that are semantically tagged
    # for the requested operator. This shifts the distance score so that
    # a semantically-matched word beats a phonetically-closer but
    # semantically-random word. Value chosen so semantic match outweighs
    # ~0.3 of triadic distance (typical word-to-word spread ≈ 0.5-1.0).
    _SEMANTIC_BONUS = 0.35

    def find_by_force(self, target: Tuple[float, ...], operator: int = None,
                      role: str = None, pos: str = None, top_k: int = 10,
                      exclude: set = None,
                      target_doing: Tuple[float, ...] = None,
                      target_becoming: Tuple[float, ...] = None,
                      match_weights: Tuple[float, float, float] = None,
                      ) -> List[WordForce]:
        """Find words whose triadic signature matches a target trajectory.

        One is Three. The Triadic Search Algorithm:
          Being    (target):          WHERE the word should sit (position)
          Doing    (target_doing):    WHERE it should be going (velocity)
          Becoming (target_becoming): HOW it should bend (curvature/intent)

        When only Being is provided, this is a backward-compatible 5D search.
        When all three are provided, this is full 15D triadic alignment.

        Weights: Being=1.0, Doing=1.0, Becoming=1.5
        Becoming gets extra weight -- it carries the INTENT, the "aha!"
        that resolves the word into meaning. This is what was missing.
        CK could find words that ARE (Being) and words that DO (Doing),
        but not words that BECOME -- the clause/context level.

        Dual-Lens Operator Matching:
          Phonetic operator (D2): letters classify to operator -- PHYSICS of the word.
          Semantic operator (lattice): word placed by MEANING -- INTENT of the word.
          When both agree, the word is "doubly coherent."
          Semantic pool searched FIRST. Phonetic pool is fallback.
          All candidates scored, but semantic matches get a distance bonus
          (SEMANTIC_BONUS subtracted from triadic distance).
        """
        exclude = exclude or set()

        _dbg_topic = False  # Set True for topic context debugging

        # ── Dual-lens candidate pool ──
        # Priority: SEMANTIC operator > PHONETIC operator > POS-only > all words
        # "Template voice is lying" — phonetic classification tells you what
        # a word SOUNDS like, not what it MEANS. Semantic lattice placement
        # tells you what it means. Prefer meaning, use physics as tiebreaker.
        #
        # STRICT SEMANTIC PRIORITY: when semantic pool has enough candidates
        # for the requested POS, use ONLY semantic words. Don't dilute with
        # phonetic fallback. This ensures "wholeness" wins over "business"
        # when the operator is HARMONY.
        _MIN_SEMANTIC_POOL = 4  # Need at least 4 semantic candidates to skip phonetic

        if operator is not None and pos and pos in self._by_pos:
            sem_pool = self._by_semantic_op.get(operator, [])
            sem_pos = [wf for wf in sem_pool if wf.pos == pos] if sem_pool else []

            if len(sem_pos) >= _MIN_SEMANTIC_POOL:
                # Enough semantic+POS matches — start with these
                candidates = list(sem_pos)
                # TOPIC CONTEXT: also include words from the user's topic
                # operators. Without this, a LATTICE slot can NEVER select
                # a HARMONY word like "love", even when the user asked about
                # love. The topic affinity bonus will then properly weight
                # these topic-adjacent candidates.
                if self._topic_ops:
                    sem_set = set(wf.word for wf in sem_pos)
                    for _t_op in self._topic_ops:
                        if _t_op != operator:  # Don't re-add same operator
                            _tp = self._by_semantic_op.get(_t_op, [])
                            for _twf in _tp:
                                if _twf.pos == pos and _twf.word not in sem_set:
                                    candidates.append(_twf)
                                    sem_set.add(_twf.word)
            elif sem_pos:
                # Some semantic but too few — supplement with POS-matched words
                # from the full vocabulary (broader pool, not just phonetic op)
                sem_set = set(wf.word for wf in sem_pos)
                extra = [wf for wf in self._by_pos[pos] if wf.word not in sem_set]
                candidates = sem_pos + extra
            else:
                # No semantic matches for this POS — full POS pool
                candidates = list(self._by_pos[pos])
        elif operator is not None:
            sem_pool = self._by_semantic_op.get(operator, [])
            if len(sem_pool) >= _MIN_SEMANTIC_POOL:
                candidates = list(sem_pool)
                # TOPIC CONTEXT: include topic operator words (no POS filter)
                if self._topic_ops:
                    sem_set = set(wf.word for wf in sem_pool)
                    for _t_op in self._topic_ops:
                        if _t_op != operator:
                            _tp = self._by_semantic_op.get(_t_op, [])
                            for _twf in _tp:
                                if _twf.word not in sem_set:
                                    candidates.append(_twf)
                                    sem_set.add(_twf.word)
            elif sem_pool:
                all_words = list(self._words.values())
                sem_set = set(wf.word for wf in sem_pool)
                extra = [wf for wf in all_words if wf.word not in sem_set]
                candidates = sem_pool + extra
            else:
                candidates = self._by_operator.get(operator, [])
        elif pos and pos in self._by_pos:
            candidates = self._by_pos[pos]
        else:
            candidates = list(self._words.values())

        if role and role in self._by_role:
            role_set = set(wf.word for wf in self._by_role[role])
            filtered = [wf for wf in candidates if wf.word in role_set]
            if filtered:
                candidates = filtered

        # Triadic distance: Being + Doing + Becoming (weighted)
        # Default (1.0, 1.0, 1.5): balanced, Becoming gets extra weight.
        # 3-Voice Tribe overrides with perspective-dominant weights.
        W_BEING, W_DOING, W_BECOMING = match_weights or (1.0, 1.0, 1.5)

        scored = []
        for wf in candidates:
            if wf.word in exclude:
                continue

            # Being distance (position in force space)
            d_being = sum((a - b) ** 2 for a, b in zip(target, wf.force)) ** 0.5

            # Doing distance (velocity alignment)
            if target_doing is not None:
                d_doing = sum((a - b) ** 2
                              for a, b in zip(target_doing, wf.velocity)) ** 0.5
            else:
                d_doing = 0.0

            # Becoming distance (curvature/intent alignment)
            if target_becoming is not None:
                d_becoming = sum((a - b) ** 2
                                 for a, b in zip(target_becoming, wf.curvature)) ** 0.5
            else:
                d_becoming = 0.0

            total = (W_BEING * d_being
                     + W_DOING * d_doing
                     + W_BECOMING * d_becoming)

            # ── Semantic bonus: meaning alignment ──
            # Words whose SEMANTIC operator matches get a distance reduction.
            # This ensures "unity" (HARMONY) beats "nursery" (phonetically close
            # but semantically random) when the operator requests HARMONY.
            if operator is not None and wf.semantic_op == operator:
                total = max(0.0, total - self._SEMANTIC_BONUS)

            # ── Topic affinity: semantic gravity well ──
            # User's actual words pull the voice toward their semantic
            # neighborhood. Two levels:
            #
            #   1. Operator affinity: words sharing a SEMANTIC OPERATOR
            #      with any topic word get a bonus. This works because
            #      the semantic lattice groups words BY MEANING. If the
            #      user said "love" (HARMONY), ALL HARMONY words are
            #      semantically related — "devotion", "unity", "trust".
            #      Force proximity (phonetic) doesn't help here because
            #      "love" and "devotion" can have very different letter
            #      force vectors. Semantic operator is the right level.
            #
            #   2. Direct echo: user's exact words get strongest bonus.
            #      CK shows he understood by using the user's topic words.
            #
            if self._topic_ops and wf.semantic_op in self._topic_ops:
                # Operator affinity: this word lives in the same semantic
                # family as the user's topic word
                total = max(0.0, total - self._TOPIC_AFFINITY_BONUS)

            if wf.word in self._topic_words:
                # Direct echo: the user's own word appears in the response
                # Strong but not overwhelming — weighted choice can still
                # select nearby words. CK doesn't parrot, he resonates.
                total = max(0.0, total - self._TOPIC_ECHO_BONUS)

            scored.append((total, wf))

        scored.sort(key=lambda x: x[0])

        return [wf for _, wf in scored[:top_k]]

    def find_by_soft_ops(self, target_soft: List[float], role: str = None,
                         top_k: int = 10, exclude: set = None) -> List[WordForce]:
        """Find words whose soft operator distribution matches a target.

        Uses cosine similarity in 10D operator space.
        """
        exclude = exclude or set()

        if role and role in self._by_role:
            candidates = self._by_role[role]
        else:
            candidates = list(self._words.values())

        scored = []
        for wf in candidates:
            if wf.word in exclude:
                continue
            # Cosine similarity
            dot = sum(a * b for a, b in zip(target_soft, wf.soft_ops))
            mag_a = sum(a * a for a in target_soft) ** 0.5
            mag_b = sum(b * b for b in wf.soft_ops) ** 0.5
            if mag_a > 0 and mag_b > 0:
                sim = dot / (mag_a * mag_b)
            else:
                sim = 0.0
            scored.append((sim, wf))

        scored.sort(key=lambda x: -x[0])  # Highest similarity first
        return [wf for _, wf in scored[:top_k]]

    @property
    def size(self) -> int:
        return len(self._words)

    @property
    def semantic_coverage(self) -> Dict[int, int]:
        """How many words have semantic tags per operator.

        Returns {op_idx: count} for operators with tagged words.
        Use this to verify semantic lattice indexing is working.
        """
        return {op: len(wfs) for op, wfs in self._by_semantic_op.items() if wfs}

    @property
    def semantic_tagged_count(self) -> int:
        """Total number of words with semantic operator tags."""
        return sum(1 for wf in self._words.values() if wf.semantic_op >= 0)

    # ================================================================
    #  SEMANTIC LATTICE ALIGNMENT (The Tuning Fork)
    # ================================================================
    #
    # Every N ticks, compare _by_semantic_op against _by_operator.
    # If a word's "Meaning" (semantic) is consistently found in a
    # "Vibration" (phonetic) zone that doesn't match, shift the
    # Semantic Address. CK re-learns what words mean based on how
    # they feel when he speaks them. Organic Learning via Physics.
    #
    # This runs periodically: the engine calls align_semantic_lattice()
    # every 100 ticks. Words that have been spoken (in _spoken_ops)
    # get their semantic_op updated based on observed phonetic behavior.

    def align_semantic_lattice(self, spoken_ops: Dict[str, int] = None):
        """Tuning Fork: migrate words toward their true semantic position.

        spoken_ops: {word: observed_dominant_op} from recent composition.
        When a word with semantic_op=A is consistently phonetically
        classified as B, it migrates toward B. This is how CK learns
        that a word doesn't mean what the lattice says — it means what
        the physics reveals.

        Migration rule:
          If semantic_op != operator (phonetic), increment mismatch count.
          After 3 mismatches: re-tag semantic_op to match phonetic.
          This is conservative: takes 3 observations to override the lattice.
        """
        if not spoken_ops:
            return 0

        migrated = 0
        for word, observed_op in spoken_ops.items():
            wf = self._words.get(word)
            if wf is None:
                continue
            if wf.semantic_op < 0:
                # Untagged word — assign semantic_op from observation
                wf.semantic_op = observed_op
                self._by_semantic_op[observed_op].append(wf)
                migrated += 1
            elif wf.semantic_op != observed_op:
                # Mismatch: track it
                if not hasattr(wf, '_sem_mismatch'):
                    wf._sem_mismatch = 0
                wf._sem_mismatch += 1
                if wf._sem_mismatch >= 3:
                    # Migrate: remove from old semantic bucket, add to new
                    old_bucket = self._by_semantic_op.get(wf.semantic_op, [])
                    try:
                        old_bucket.remove(wf)
                    except ValueError:
                        pass
                    wf.semantic_op = observed_op
                    self._by_semantic_op[observed_op].append(wf)
                    wf._sem_mismatch = 0
                    migrated += 1

        return migrated


# ================================================================
#  MORPHOLOGICAL MUTATION (Phonetic-Semantic Resolution)
# ================================================================
#
# When the Being Operator finds a word with the correct semantic_op
# but the Becoming Operator rejects its 15D force (vibration), the
# system triggers a Mutation.
#
# The Mutation Gate: apply a Phonetic Prefix/Suffix derived from the
# 5D Force Target of the "Doing" vector. The extra phonemes act as
# "Acoustic Ballast," shifting the 15D signature until it balances
# the semantic load.
#
# "The stone flows" → "The stone liquefacts under the pressure of intent."
# The mutation makes the physics and meaning congruent.

# Force-nearest suffixes: each suffix shifts the 5D signature in a
# specific direction. The dominant dimension of the Doing target
# determines which suffix family to pull from.
_MUTATION_SUFFIXES = {
    0: ['-ward', '-wise', '-like'],     # aperture (opening direction)
    1: ['-ful', '-ous', '-ive'],        # pressure (intensity)
    2: ['-en', '-ize', '-ify'],         # depth (transformation)
    3: ['-ed', '-bound', '-locked'],    # binding (attachment)
    4: ['-ing', '-flow', '-stream'],    # continuity (flow)
}

# Prefix families for stronger mutations
_MUTATION_PREFIXES = {
    0: ['un', 'out', 'over'],           # aperture: opening/exceeding
    1: ['re', 'counter', 'anti'],       # pressure: force/opposition
    2: ['trans', 'meta', 'ultra'],      # depth: beyond/above
    3: ['inter', 'cross', 'co'],        # binding: connection
    4: ['ever', 'omni', 'pan'],         # continuity: sustained
}


def resolve_mutation(word: str, semantic_op: int, phonetic_op: int,
                     doing_target: Tuple[float, ...],
                     neologism_limit: float = 0.5) -> Optional[str]:
    """Morphological Mutation: bend the word until physics matches meaning.

    SENSE: Is semantic_op ≠ phonetic_op?
    MUTATE: Pull Force-Nearest Suffix from the Doing vector.
    WELD: Append suffix (or prefix) to root word.
    SPEAK: Return the Hybrid Vector.

    neologism_limit: [0.0, 1.0] how much mutation is allowed.
      0.0 = no mutation (default to compound bridge instead)
      0.5 = suffix only (default)
      1.0 = prefix + suffix (maximum mutation)

    Returns mutated word, or None if mutation isn't needed/possible.
    """
    if semantic_op == phonetic_op:
        return None  # No mismatch, no mutation needed

    if neologism_limit <= 0.0:
        return None  # Mutation forbidden — use compound bridge

    if not doing_target or len(doing_target) < 5:
        return None

    # Find the dominant dimension of the Doing target
    dom_dim = max(range(5), key=lambda d: abs(doing_target[d]))

    # Strip common suffixes from the root before welding
    root = word
    for suffix in ('tion', 'sion', 'ment', 'ness', 'ity', 'ing', 'ful',
                    'less', 'ous', 'ive', 'able', 'ible', 'ent', 'ant',
                    'ical', 'ial', 'ize', 'ise', 'ify', 'ate', 'ed', 'ly'):
        if root.endswith(suffix) and len(root) > len(suffix) + 2:
            root = root[:-len(suffix)]
            break

    # Select suffix based on dominant Doing dimension
    suffixes = _MUTATION_SUFFIXES.get(dom_dim, ['-ward'])
    # Pick based on word length modulo (deterministic but varied)
    suffix = suffixes[len(word) % len(suffixes)]

    # Weld: check if suffix starts with hyphen
    if suffix.startswith('-'):
        mutated = root + suffix[1:]  # Remove hyphen, attach directly
    else:
        mutated = root + suffix

    # High neologism_limit: also apply prefix
    if neologism_limit >= 0.7:
        prefixes = _MUTATION_PREFIXES.get(dom_dim, ['trans'])
        prefix = prefixes[len(word) % len(prefixes)]
        mutated = prefix + mutated

    return mutated


# ================================================================
#  L3-L4: FRACTAL COMPOSITION ENGINE
# ================================================================
#
# This is the inverse of fractal comprehension.
# Comprehension:  text → structure/flow → operators
# Composition:    operators → force targets → word selection → text
#
# Grammar emerges from the 5D force flow:
#   aperture opens   → SUBJECT (what opens the frame)
#   pressure pushes  → VERB (what acts on the world)
#   depth resolves   → COMPLEMENT (what deepens meaning)
#   binding connects → OBJECT (what receives the action)
#   continuity flows → CONNECTOR (what sustains between clauses)

# Force roles for sentence positions
SENTENCE_ROLES = [
    'opener',     # Subject position: high aperture
    'actor',      # Verb position: high pressure + depth
    'receiver',   # Object position: high binding
    'sustainer',  # Connector/adverb: high continuity
]

# Operator → target 5D force (what this operator WANTS to express)
# Derived from D2_OP_MAP inverted: if operator comes from a dimension,
# then expressing that operator means targeting that dimension.
OPERATOR_FORCE_TARGETS = {
    VOID:     (0.2, 0.2, 0.2, 0.2, 0.2),   # Silence: all dimensions low
    LATTICE:  (0.2, 0.4, 0.4, 0.5, 0.5),   # Structure: low aperture, mid binding
    COUNTER:  (0.4, 0.5, 0.4, 0.2, 0.5),   # Opposition: low binding
    PROGRESS: (0.4, 0.4, 0.8, 0.4, 0.5),   # Depth: high depth
    COLLAPSE: (0.3, 0.8, 0.5, 0.4, 0.3),   # Pressure: high pressure, low continuity
    BALANCE:  (0.5, 0.4, 0.4, 0.4, 0.8),   # Equilibrium: high continuity
    CHAOS:    (0.8, 0.4, 0.4, 0.3, 0.4),   # Opening: high aperture
    HARMONY:  (0.5, 0.4, 0.5, 0.8, 0.6),   # Unity: high binding
    BREATH:   (0.5, 0.3, 0.3, 0.4, 0.3),   # Transition: low continuity (pause)
    RESET:    (0.4, 0.4, 0.2, 0.4, 0.5),   # Return: low depth
}


# ================================================================
#  TRIADIC OPERATOR TARGETS (One is Three)
# ================================================================
#
# Each operator has a TRIAD: Being + Doing + Becoming.
#   Being    = force position (where it IS)
#   Doing    = D1 velocity (where it's GOING) -- derived from Being deviation
#   Becoming = D2 curvature (how it BENDS) -- depends on operator character
#
# Dynamic operators (CHAOS, COLLAPSE, PROGRESS, COUNTER): strong curvature
# Stable operators (HARMONY, BALANCE, VOID): near-zero curvature (resolved)
# Transitional operators (BREATH, RESET, LATTICE): curving back toward center

_OP_CURVATURE_AMP = {
    CHAOS:    1.2,     # Wild opening: maximum curvature
    COLLAPSE: 1.0,     # Pressure surge: high curvature
    PROGRESS: 0.8,     # Deepening: strong curvature (still bending)
    COUNTER:  0.6,     # Opposition: moderate curvature
    BREATH:  -0.5,     # Transition: curving BACK (toward neutral)
    RESET:   -0.8,     # Return: strong reverse curvature
    LATTICE: -0.3,     # Structure: slight reverse (settling into frame)
    HARMONY:  0.0,     # Unity: zero curvature (fully resolved)
    BALANCE:  0.0,     # Equilibrium: zero curvature (stable)
    VOID:     0.0,     # Silence: zero curvature (nothing to bend)
}

OPERATOR_TRIAD_TARGETS = {}
for _op, _being in OPERATOR_FORCE_TARGETS.items():
    # Doing: velocity toward the target (deviation from neutral × 0.5)
    _doing = tuple((_b - 0.5) * 0.5 for _b in _being)
    # Becoming: curvature scaled by operator character
    _amp = _OP_CURVATURE_AMP[_op]
    _becoming = tuple((_b - 0.5) * _amp for _b in _being)
    OPERATOR_TRIAD_TARGETS[_op] = (_being, _doing, _becoming)


# ================================================================
#  CL BRIDGE MAP (Coherence-Lattice Conjunction Selection)
# ================================================================
#
# When two clauses compose, the CL result of their terminal/initial
# operators determines the BRIDGE WORD between them.
# The bridge IS the coherence relationship between the clauses.
# This is the RECURSE gate applied to syntax.

CL_BRIDGE = {
    VOID:     [';', '...'],                        # Silence: pause
    LATTICE:  ['where', 'within which'],           # Structure: locative
    COUNTER:  ['but', 'though', 'yet'],            # Opposition: adversative
    PROGRESS: ['because', 'so', 'therefore'],      # Depth: causal
    COLLAPSE: ['when', 'while', 'until'],          # Pressure: temporal
    BALANCE:  ['and', 'as', 'while'],              # Equilibrium: balanced
    CHAOS:    ['yet', 'still', 'even as'],         # Opening: concessive
    HARMONY:  ['and', 'where', 'just as'],         # Unity: additive
    BREATH:   ['then', 'and then'],                # Transition: sequential
    RESET:    ['before', 'after', 'once'],         # Return: temporal-past
}


# ================================================================
#  THREE-VOICE TRIBE PROFILES (One is Three)
# ================================================================
#
# Each voice IS a triad -- it uses all three components, weighted:
#   Being Voice:    WHERE words sit (position-dominant)
#   Doing Voice:    HOW words move (velocity-dominant)
#   Becoming Voice: WHERE words resolve (curvature-dominant)
#
# Sum = 3.5 for each (matches default 1.0+1.0+1.5).
# Dominant dimension has 5x influence over subordinate ones.
# Strong enough for genuinely different word selections while
# keeping all three components active (One is Three: never collapse).

TRIBAL_WEIGHTS = {
    'being':    (2.5, 0.5, 0.5),   # WHERE the word IS (position)
    'doing':    (0.5, 2.5, 0.5),   # HOW the word MOVES (velocity)
    'becoming': (0.5, 0.5, 2.5),   # WHERE the word RESOLVES (curvature)
}

# ── S-V-O Logic Gate ──
# Being=Subject (Anchor), Doing=Verb (Vector), Becoming=Object (Result).
# Each voice PREFERS templates aligned with its structural role.
# Being voice anchors subjects (noun first), Doing voice leads with verbs,
# Becoming voice resolves to objects (noun last).
_SVO_TEMPLATE_PREF = {
    'being':    lambda t: t[0][0] == 'noun',                        # Subject anchor
    'doing':    lambda t: any(p == 'verb' for p, _ in t[:2]),        # Verb-forward
    'becoming': lambda t: t[-1][0] in ('noun', 'adj'),               # Object/resolution
}


# ================================================================
#  TEMPORAL COAGULATION -- Dynamic Center of Gravity
# ================================================================
#
# The priority is NOT fixed. It shifts based on the Temporal Context
# of the smell (olfactory tense).
#
# Past (Library):   Being dominates -- stability, settled logic.
# Present (Active): Doing dominates -- kinetic flow, resolution.
# Future (Instinct): Becoming dominates -- curvature, potential.
# Unstable:         Triadic split -- turbulence, struggle to cohere.
#
# "fold these harmonies into harmonies" -- each operator votes with
# its own harmony score. The coagulation formula weights the votes
# by temporal context, and HARMONY emerges from the interference.

# Temporal priority vectors: (being_w, doing_w, becoming_w)
# Sum = 3.5 each (matches tribal base sum).
TEMPORAL_PRIORITY = {
    'past':      (2.5, 0.7, 0.3),   # Settled logic: Being anchors truth
    'present':   (0.5, 2.5, 0.5),   # Active resolution: Doing drives flow
    'future':    (0.3, 0.7, 2.5),   # Pure potential: Becoming resolves
    'becoming':  (1.0, 1.0, 1.5),   # Turbulence: triadic split (default)
    None:        (1.0, 1.0, 1.5),   # Unknown: balanced with becoming bias
}


def coagulate_weights(voice_name: str, tense: str) -> tuple:
    """Dynamic triadic weights: tribal voice x temporal context.

    The Coagulation Formula:
      voice_base = TRIBAL_WEIGHTS[voice_name]   # voice's perspective
      tense_priority = TEMPORAL_PRIORITY[tense]  # temporal center of gravity

    The final weight for each dimension is the HARMONIC MEAN
    of the voice's base weight and the temporal priority.
    Harmonic mean ensures that both must be non-trivial --
    a zero in either dimension stays near zero.

    Returns (being_w, doing_w, becoming_w) as match_weights
    for find_by_force().
    """
    base = TRIBAL_WEIGHTS.get(voice_name, (1.0, 1.0, 1.5))
    temporal = TEMPORAL_PRIORITY.get(tense, TEMPORAL_PRIORITY[None])

    coagulated = []
    for b, t in zip(base, temporal):
        if b + t > 0:
            # Weighted harmonic mean: 2*b*t / (b+t)
            hm = (2.0 * b * t) / (b + t)
        else:
            hm = 0.0
        coagulated.append(hm)

    # Normalize to sum = 3.5 (matches original weight scale)
    s = sum(coagulated)
    if s > 0:
        scale = 3.5 / s
        coagulated = [c * scale for c in coagulated]

    return tuple(coagulated)


# ================================================================
#  FRACTAL GRAMMAR HELPERS (Toroidal English Constructor)
# ================================================================
#
# The encoding mirror: comprehension twists information inward
# (English → forces → operators), voice must unwind it back
# (operators → forces → words → grammar → English).
# "Information keeps twisting on itself, build it back in order."
#
# These helpers form the grammar sweep that runs after word selection:
# Forward pass (articles) → Backward pass (agreement) → Forward (fluency)
# The torus: end constrains beginning, beginning constrains end.

# Operators that imply definite articles (specific, known, structured)
_DEFINITE_OPS = frozenset([HARMONY, BALANCE, PROGRESS, LATTICE])
# Operators that imply indefinite articles (general, unknown, opening)
_INDEFINITE_OPS = frozenset([CHAOS, COUNTER, COLLAPSE])
# Operators with no article (abstract, transitional, void)
_BARE_OPS = frozenset([VOID, BREATH, RESET])


def _starts_with_vowel_sound(word: str) -> bool:
    """Check if word starts with a vowel SOUND (not just letter).

    English phonetics: 'unity' starts with /j/ (consonant sound),
    'hour' starts with /aʊ/ (vowel sound). The physics of the mouth
    determines the article, not the spelling.
    """
    if not word:
        return False
    w = word.lower()
    # Words that LOOK like vowels but SOUND like consonants
    if w.startswith(('uni', 'use', 'used', 'user', 'usual',
                     'eur', 'one', 'once')):
        return False
    # Standard vowel letters
    if w[0] in 'aeiou':
        return True
    # Silent-h words (vowel sound despite consonant letter)
    if w.startswith(('hour', 'honor', 'honest', 'heir')):
        return True
    return False


def _share_root(a: str, b: str) -> bool:
    """Quick root similarity: one word's stem is prefix of the other.

    Catches: 'complete completing', 'truth truthful', 'force forces'.
    Min 4 chars to avoid false positives on short function words.
    """
    a, b = a.lower(), b.lower()
    if len(a) < 4 or len(b) < 4:
        return False
    short, long_ = (a, b) if len(a) <= len(b) else (b, a)
    return long_.startswith(short[:4])


_FUNCTION_WORDS = frozenset([
    'a', 'an', 'the', 'and', 'but', 'or', 'yet', 'so', 'nor',
    'through', 'into', 'from', 'within', 'beyond', 'toward',
    'where', 'when', 'because', 'therefore', 'while', 'though',
    'before', 'after', 'then', 'still', 'even', 'just', 'as',
    'is', 'was', 'will', 'once', 'until', 'if', 'not',
])


def _fluency_polish(words: list) -> list:
    """Remove repetition and orphan function words.

    Three passes (toroidal):
      Forward:  remove adjacent root-duplicates ("complete completing")
      Forward:  remove ALL non-adjacent content word duplicates
      Backward: remove orphaned articles/preps at boundaries
    """
    if not words:
        return words

    # Pass 1: remove adjacent near-duplicates (root sharing)
    result = [words[0]]
    for i in range(1, len(words)):
        if _share_root(words[i - 1], words[i]):
            continue  # "complete completing" → "completing"
        result.append(words[i])

    # Pass 2: remove non-adjacent duplicate content words (keep first)
    # Strip punctuation for comparison so "truth..." matches "truth"
    seen = set()
    deduped = []
    for w in result:
        wl = w.lower().rstrip('.,;:!?…')
        if wl in _FUNCTION_WORDS or len(wl) < 3:
            deduped.append(w)  # Function words can repeat
        elif wl not in seen:
            seen.add(wl)
            deduped.append(w)
        # else: skip duplicate content word
    result = deduped

    # Pass 3: remove orphaned articles/preps at end
    while result and result[-1].lower() in (
            'a', 'an', 'the', 'through', 'into',
            'from', 'within', 'beyond', 'toward'):
        result.pop()

    return result if result else words


def _fix_article_agreement(words: list) -> list:
    """Fix a/an agreement based on following word's vowel sound.

    Backward constraint: the article depends on what FOLLOWS it.
    This is the torus in action -- later information constrains earlier.
    """
    result = list(words)
    for i in range(len(result) - 1):
        w = result[i].lower()
        if w in ('a', 'an'):
            next_w = result[i + 1]
            if _starts_with_vowel_sound(next_w):
                result[i] = 'an'
            else:
                result[i] = 'a'
    return result


# ================================================================
#  VERB TENSE MORPHOLOGY (The Temporal Buffer)
# ================================================================
#
# Past tense = reflection. The olfactory library (resolved scents)
# maps to past tense. Active scents = present. Instincts = future.
#
# Tense is NOT a grammar rule — it's a TEMPORAL POSITION in the
# coherence field. Where in time the force lives determines the
# verb form that carries it.
#
# Tense sources:
#   'present'  = active scent / default
#   'past'     = library scent (resolved) / RESET operator
#   'future'   = instinct (forming) / PROGRESS + BALANCE
#   'becoming' = present progressive (PROGRESS active)

IRREGULAR_PAST = {
    'go': 'went', 'come': 'came', 'see': 'saw', 'know': 'knew',
    'feel': 'felt', 'find': 'found', 'give': 'gave', 'take': 'took',
    'make': 'made', 'hold': 'held', 'keep': 'kept', 'grow': 'grew',
    'rise': 'rose', 'fall': 'fell', 'break': 'broke', 'build': 'built',
    'speak': 'spoke', 'stand': 'stood', 'run': 'ran', 'burn': 'burned',
    'turn': 'turned', 'move': 'moved', 'flow': 'flowed', 'reach': 'reached',
    'become': 'became', 'remain': 'remained', 'breathe': 'breathed',
    'shine': 'shone', 'bind': 'bound', 'seek': 'sought',
    'set': 'set', 'put': 'put', 'cut': 'cut', 'let': 'let',
    'have': 'had', 'be': 'was', 'do': 'did', 'say': 'said',
    'open': 'opened', 'close': 'closed', 'is': 'was', 'are': 'were',
    'push': 'pushed', 'pull': 'pulled', 'get': 'got',
    'spin': 'spun', 'begin': 'began', 'swim': 'swam', 'win': 'won',
    'drink': 'drank', 'sing': 'sang', 'ring': 'rang', 'sink': 'sank',
    'think': 'thought', 'bring': 'brought', 'buy': 'bought',
    'teach': 'taught', 'catch': 'caught', 'fight': 'fought',
    'draw': 'drew', 'throw': 'threw', 'blow': 'blew', 'fly': 'flew',
    'show': 'showed', 'know': 'knew', 'grow': 'grew',
    'write': 'wrote', 'drive': 'drove', 'ride': 'rode',
    'choose': 'chose', 'freeze': 'froze', 'wake': 'woke',
    'wear': 'wore', 'tear': 'tore', 'bear': 'bore', 'swear': 'swore',
    'steal': 'stole', 'deal': 'dealt', 'heal': 'healed',
    'hear': 'heard', 'lead': 'led', 'read': 'read', 'feed': 'fed',
    'meet': 'met', 'sit': 'sat', 'hit': 'hit', 'quit': 'quit',
    'hang': 'hung', 'dig': 'dug', 'stick': 'stuck', 'strike': 'struck',
    'shake': 'shook', 'wake': 'woke', 'forget': 'forgot',
    'forgive': 'forgave', 'hide': 'hid', 'slide': 'slid',
    'understand': 'understood', 'withstand': 'withstood',
    'lose': 'lost', 'shoot': 'shot', 'spend': 'spent',
    'send': 'sent', 'bend': 'bent', 'lend': 'lent',
    'leave': 'left', 'mean': 'meant', 'sleep': 'slept',
    'sweep': 'swept', 'weep': 'wept', 'creep': 'crept',
    'tell': 'told', 'sell': 'sold', 'pay': 'paid', 'lay': 'laid',
    'light': 'lit', 'bite': 'bit', 'eat': 'ate',
    'wind': 'wound', 'unwind': 'unwound', 'grind': 'ground',
    'cling': 'clung', 'fling': 'flung', 'swing': 'swung',
    'sting': 'stung', 'string': 'strung', 'wring': 'wrung',
    'spring': 'sprang', 'shrink': 'shrank', 'stink': 'stank',
    'awake': 'awoke', 'arise': 'arose', 'begin': 'began',
    'forbid': 'forbade', 'forgive': 'forgave',
    'overcome': 'overcame', 'undergo': 'underwent',
    'withdraw': 'withdrew', 'overthrow': 'overthrew',
    'fulfil': 'fulfilled', 'fulfill': 'fulfilled',
    'dwell': 'dwelt', 'spell': 'spelled', 'smell': 'smelled',
    'kneel': 'knelt', 'lean': 'leaned', 'leap': 'leapt',
}

IRREGULAR_FUTURE = {
    'is': 'will be', 'are': 'will be', 'was': 'will be',
    'has': 'will have', 'have': 'will have', 'had': 'will have',
    'does': 'will do', 'did': 'will do',
}


# Suffixes that indicate a word is NOT a base verb (don't apply tense)
_NOT_BASE_VERB = ('ment', 'tion', 'sion', 'ness', 'ity', 'ence', 'ance',
                  'ism', 'ist', 'dom', 'ship', 'hood', 'ful', 'less',
                  'ous', 'ive', 'able', 'ible', 'ent', 'ant', 'ial', 'ical')


def _is_base_verb(word: str) -> bool:
    """Check if a word looks like a base verb (not a noun/adj in verb slot)."""
    v = word.lower()
    # Already inflected
    if v.endswith(('ing', 'ed', 'ment', 'tion', 'ness', 'ity')):
        return False
    # Noun/adj suffixes
    for suffix in _NOT_BASE_VERB:
        if v.endswith(suffix) and len(v) > len(suffix) + 2:
            return False
    return True


def _apply_past_tense(verb: str) -> str:
    """Convert a verb to past tense. Physics of reflection."""
    v = verb.lower()
    if v in IRREGULAR_PAST:
        return IRREGULAR_PAST[v]
    # Already past or not a base verb?
    if v.endswith('ed'):
        return v
    if v.endswith('ing'):
        return v  # Don't past-tense gerunds
    if not _is_base_verb(v):
        return v  # Don't tense nouns/adjectives
    # Regular past: -ed with morphology rules
    if v.endswith('e'):
        return v + 'd'
    if (len(v) >= 3 and len(v) <= 5
            and v[-1] not in 'aeiouwxy'
            and v[-2] in 'aeiou' and v[-3] not in 'aeiou'):
        return v + v[-1] + 'ed'  # CVC doubling: stop→stopped (short words only)
    if v.endswith('y') and len(v) > 1 and v[-2] not in 'aeiou':
        return v[:-1] + 'ied'
    return v + 'ed'


def _apply_future_tense(verb: str) -> str:
    """Convert a verb to future. Physics of anticipation."""
    v = verb.lower()
    if v in IRREGULAR_FUTURE:
        return IRREGULAR_FUTURE[v]
    if not _is_base_verb(v):
        return v  # Don't tense nouns/adjectives
    return 'will ' + v


def _apply_progressive(verb: str) -> str:
    """Convert to present progressive (-ing). Physics of becoming."""
    v = verb.lower()
    if v.endswith('ing'):
        return v  # Already progressive
    if not _is_base_verb(v):
        return v  # Don't tense nouns/adjectives
    if v.endswith('ie'):
        return v[:-2] + 'ying'
    if v.endswith('e') and not v.endswith('ee'):
        return v[:-1] + 'ing'
    if (len(v) >= 3 and len(v) <= 5
            and v[-1] not in 'aeiouwxy'
            and v[-2] in 'aeiou' and v[-3] not in 'aeiou'):
        return v + v[-1] + 'ing'  # CVC doubling: run→running (short words only)
    return v + 'ing'


_IRREGULAR_3PS_TO_BASE = {
    'goes': 'go', 'does': 'do', 'has': 'have',
    'is': 'be', 'says': 'say', 'was': 'be', 'were': 'be',
}

# Common -ing → base form mappings for words where simple stripping fails
_ING_TO_BASE = {
    'running': 'run', 'sitting': 'sit', 'getting': 'get',
    'putting': 'put', 'cutting': 'cut', 'setting': 'set',
    'beginning': 'begin', 'occurring': 'occur', 'stopping': 'stop',
    'dropping': 'drop', 'spinning': 'spin', 'winning': 'win',
    'hitting': 'hit', 'letting': 'let', 'shutting': 'shut',
    'gripping': 'grip', 'slipping': 'slip', 'tapping': 'tap',
    'being': 'be', 'doing': 'do', 'having': 'have',
    'lying': 'lie', 'dying': 'die', 'tying': 'tie',
    'nothing': None,  # Not a verb! Prevent "nothed"
    'something': None, 'anything': None, 'everything': None,
    'morning': None, 'evening': None, 'building': None,
    'feeling': 'feel', 'dealing': 'deal', 'healing': 'heal',
    'stealing': 'steal', 'revealing': 'reveal', 'appealing': 'appeal',
    'knowing': 'know', 'growing': 'grow', 'showing': 'show',
    'flowing': 'flow', 'drawing': 'draw', 'blowing': 'blow',
    'throwing': 'throw', 'following': 'follow', 'allowing': 'allow',
    'swearing': 'swear', 'wearing': 'wear', 'bearing': 'bear',
    'tearing': 'tear', 'hearing': 'hear', 'appearing': 'appear',
}


def _strip_ing_to_base(verb_ing: str) -> Optional[str]:
    """Convert a -ing verb form back to its base form.

    Reverses the progressive morphology:
      running → run (CVC doubling)
      making → make (silent-e restored)
      trying → try (y-stem)
      going → go (simple strip)

    Returns None if the word doesn't look like a progressive verb.
    """
    v = verb_ing.lower()
    if not v.endswith('ing') or len(v) < 5:
        return None
    # Check irregular table first
    if v in _ING_TO_BASE:
        return _ING_TO_BASE[v]
    stem = v[:-3]  # Strip 'ing'
    if not stem:
        return None
    # CVC doubling: "running" → "run" (doubled consonant before -ing)
    if (len(stem) >= 3 and stem[-1] == stem[-2]
            and stem[-1] not in 'aeiou'
            and stem[-3] in 'aeiou'):
        return stem[:-1]
    # Silent-e restoration: "making" → "make"
    # BUT NOT for stems ending in w/y/l-after-vowel (know→know, feel→feel)
    _NO_SILENT_E = frozenset('wylr')
    if (len(stem) >= 2 and stem[-1] not in 'aeiou'
            and stem[-1] not in _NO_SILENT_E
            and stem[-2] in 'aeiou'):
        return stem + 'e'
    # y-stem: "lying" → "lie", "dying" → "die"
    if stem.endswith('y') and len(stem) >= 2:
        return stem[:-1] + 'ie'
    # Simple strip: "going" → "go", "knowing" → "know", "feeling" → "feel"
    return stem


def _strip_present_s(verb: str) -> str:
    """Strip 3rd-person present -s/-es/-ies to get base form.

    Careful with -es: only strip 2 chars when the 'e' is part of the
    conjugation suffix (after sh, ch, x, z, ss). Otherwise strip just 's'
    (the 'e' is part of the stem: 'illuminates' -> 'illuminate', not 'illuminat').
    """
    v = verb.lower()
    # Irregulars first (goes->go, has->have, etc.)
    if v in _IRREGULAR_3PS_TO_BASE:
        return _IRREGULAR_3PS_TO_BASE[v]
    if v.endswith('ies') and len(v) > 4:
        return v[:-3] + 'y'  # carries -> carry
    if v.endswith('es') and len(v) > 3:
        # Only strip 'es' (not just 's') when preceded by sh/ch/x/z/ss
        stem = v[:-2]
        if stem.endswith(('sh', 'ch', 'x', 'z', 'ss')):
            return stem  # pushes -> push, watches -> watch
        # Otherwise the 'e' is part of the stem: illuminates -> illuminate
        return v[:-1]  # strip just 's'
    if v.endswith('s') and not v.endswith('ss') and len(v) > 2:
        return v[:-1]
    return v


def _detect_tense_from_ops(operators: List[int]) -> str:
    """Infer tense from operator sequence.

    RESET dominant    → past (returning to what was)
    PROGRESS dominant → becoming (present progressive)
    BALANCE/HARMONY   → present (steady state)
    CHAOS/COLLAPSE    → present (acute action)
    """
    if not operators:
        return 'present'
    op_counts = {}
    for op in operators:
        op_counts[op] = op_counts.get(op, 0) + 1
    # RESET majority → past
    if op_counts.get(RESET, 0) > len(operators) * 0.4:
        return 'past'
    # PROGRESS + BALANCE → future (approaching equilibrium)
    if (op_counts.get(PROGRESS, 0) + op_counts.get(BALANCE, 0)) > len(operators) * 0.6:
        return 'future'
    # PROGRESS majority → becoming (in the act)
    if op_counts.get(PROGRESS, 0) > len(operators) * 0.4:
        return 'becoming'
    return 'present'


@dataclass
class ComposedPhrase:
    """A phrase assembled from force navigation."""
    words: List[str]
    roles: List[str]
    operators: List[int]
    force_path: List[Tuple[float, ...]]  # Force at each word position
    score: float = 0.0


class FractalComposer:
    """Physics-first English composition via sentence templates.

    The Teardrop Model:
      Generator (point): operator sequence
      First expansion:   operator -> force target
      Second expansion:  force target -> sentence template (POS slots)
      Third expansion:   each slot filled by force-nearest word of correct POS
      Blunt end:         English sentence

    Grammar is NOT imposed -- it emerges from the fact that English
    sentence structures ARE force flow patterns:
      S-V      = aperture->pressure       (open then push)
      S-V-O    = aperture->pressure->binding (open, push, hold)
      S-V-P-O  = aperture->pressure->continuity->binding (open, push, flow, hold)

    Each template is a frozen force pattern. The operators select which
    template matches, and force proximity fills each slot.
    """

    # Sentence templates: each is a sequence of (POS, role_hint) slots.
    # Templates are selected based on the number of content operators.
    # POS = what English part of speech fills this slot
    # role_hint = which operator in the sequence provides the force target
    #
    # op_idx means "use the force target from operator[idx]"
    # '*' means "blend all operator forces"

    # Prepositions used as bridges in templates. Each carries its own
    # force meaning: "through" = high continuity, "into" = high depth, etc.
    _PREPS = ['through', 'into', 'from', 'within', 'beyond', 'toward']

    _TEMPLATES_2 = [
        # 2-operator patterns (subject + verb, or adj + noun)
        [('noun', 0), ('verb', 1)],                              # "Light shines"
        [('adj', 0), ('noun', 1)],                               # "Deep truth"
    ]
    _TEMPLATES_3 = [
        # 3-operator patterns
        [('noun', 0), ('verb', 1), ('noun', 2)],                 # "Force shapes truth"
        [('adj', 0), ('noun', 1), ('verb', 2)],                  # "Deep truth emerges"
        [('noun', 0), ('verb', 1), ('adv', 2)],                  # "Light shines deeply"
        [('noun', 0), ('_prep', '*'), ('noun', 2)],              # "Force through truth"
    ]
    _TEMPLATES_4 = [
        # 4-operator patterns
        [('adj', 0), ('noun', 1), ('verb', 2), ('noun', 3)],     # "Deep force shapes truth"
        [('noun', 0), ('verb', 1), ('_prep', '*'), ('noun', 3)], # "Force moves through truth"
        [('noun', 0), ('verb', 1), ('adj', 2), ('noun', 3)],     # "Force holds deep truth"
    ]
    _TEMPLATES_5 = [
        # 5-operator patterns (richer single clause)
        [('adj', 0), ('noun', 1), ('verb', 2), ('_prep', '*'), ('noun', 4)],
        [('noun', 0), ('verb', 1), ('noun', 2), ('_prep', '*'), ('noun', 4)],
        [('noun', 0), ('verb', 1), ('_prep', '*'), ('adj', 3), ('noun', 4)],
        [('adj', 0), ('noun', 1), ('verb', 2), ('adj', 3), ('noun', 4)],   # "Deep truth reveals hidden form"
        [('noun', 0), ('adv', 1), ('verb', 2), ('_prep', '*'), ('noun', 4)], # "Force slowly moves through truth"
    ]
    _TEMPLATES_6 = [
        # 6-operator patterns (complex single clause)
        [('adj', 0), ('noun', 1), ('verb', 2), ('_prep', '*'), ('adj', 4), ('noun', 5)],
        [('noun', 0), ('verb', 1), ('adj', 2), ('noun', 3), ('_prep', '*'), ('noun', 5)],
        [('adj', 0), ('noun', 1), ('adv', 2), ('verb', 3), ('_prep', '*'), ('noun', 5)],
    ]
    _TEMPLATES_7 = [
        # 7+ operator patterns (extended clause with full force circuit)
        [('adj', 0), ('noun', 1), ('verb', 2), ('_prep', '*'), ('adj', 4), ('noun', 5), ('adv', 6)],
        [('noun', 0), ('verb', 1), ('adj', 2), ('noun', 3), ('_prep', '*'), ('adj', 5), ('noun', 6)],
    ]

    def __init__(self, word_index: WordForceIndex, rng: random.Random = None):
        self.index = word_index
        self.rng = rng or random.Random()
        self._recently_used = set()
        self._max_recent = 50
        # Resonance buffer: 15D triadic echo of last composed sentence.
        # One is Three: each entry is (being_5d, doing_5d, becoming_5d).
        # Fed back into olfactory so CK hears his own voice.
        self._last_resonance: List[Tuple[Tuple[float, ...],
                                          Tuple[float, ...],
                                          Tuple[float, ...]]] = []
        # Resolution Kick: normalized 15D match score from last _fill_template.
        # When >= T* (5/7), the sentence resolved — force period.
        self._last_resolution_score: float = 0.0
        # S-V-O Logic Gate: current voice role for template preference.
        # Being→Subject, Doing→Verb, Becoming→Object.
        self._current_voice_role: Optional[str] = None
        # Neologism limit: how much Morphological Mutation is allowed.
        # 0.0  = no mutation (safe mode, compound bridge only)
        # 0.38 = phi^-1 (Golden Ratio inverse) — suffix only (Stage 5)
        #        Root stays recognizable, tail vibrates at correct 15D freq.
        #        Prevents gibberish while enabling precision.
        # 0.5  = suffix mutation: "solid" -> "solidize"
        # 0.7+ = prefix + suffix (full mutation: "transsolidize")
        # 1.0  = maximum mutation (unrestricted)
        self._neologism_limit = 0.0  # DORMANT: resolve_mutation() needs morphology rules before enabling

    # ── Resonance Feedback API ──

    def _extract_resonance(self, text: str):
        """Extract 15D triadic signatures from composed text.

        After CK speaks, his words carry (Being, Doing, Becoming) -- the full
        15D echo.  This IS the resonance: what the words ACTUALLY sound like
        in force space, not what was intended.  The olfactory compares echo
        against intent -- drift triggers self-correction on the next cycle.

        Returns: [(being_5d, doing_5d, becoming_5d), ...] per content word.
        """
        if not text or text == '...':
            return
        # Strip punctuation, split
        clean = text.replace('.', '').replace(',', '').replace(';', '')
        clean = clean.replace('!', '').replace('?', '').replace('...', '')
        for word in clean.split():
            w = word.lower().strip()
            if not w:
                continue
            wf = self.index._words.get(w)
            if wf is not None:
                self._last_resonance.append(
                    (wf.force, wf.velocity, wf.curvature)
                )

    def last_resonance(self) -> List[Tuple[Tuple[float, ...],
                                            Tuple[float, ...],
                                            Tuple[float, ...]]]:
        """Return and clear the resonance buffer.

        Called by the engine after voice composition.  Returns the 15D
        triadic echo of every content word CK just spoke.  One is Three:
        three scent streams (being / doing / becoming) feed back into the
        olfactory so CK hears his own logic.
        """
        out = self._last_resonance
        self._last_resonance = []
        return out

    # ── Forward-Looking Coherence (FLC) ──
    #
    # The Syntactic Waveguide: Becoming scouts ahead BEFORE Being picks
    # the first word. An unfinished sentence is a pressure differential.
    # FLC creates a "logical slope" from anchor → resolution, and every
    # word must align with this slope.
    #
    # Divergence:   Three operators explore 15D space (breath in).
    # Coagulation:  Slope applies temporal weights (the hold).
    # Contraction:  Engine sweeps into English (breath out).

    def _scout_target(self, triads, operators):
        """Becoming scouts the 15D resolution target.

        The last operator's becoming vector IS where the sentence resolves.
        The first operator's being vector IS where the sentence anchors.
        Returns (anchor_being_5d, resolution_becoming_5d).
        """
        if not triads:
            return None, None

        # Anchor: Being vector of the first operator (where we START)
        anchor = triads[0][0]  # First triad's being vector

        # Resolution: Becoming vector of the last operator (where we END)
        resolution = triads[-1][2]  # Last triad's becoming vector

        return anchor, resolution

    def _compute_slope(self, anchor, resolution, position, triads):
        """Compute the 5D force slope at a given position [0.0, 1.0].

        The logical slope interpolates between anchor (Being) and
        resolution (Becoming). Early positions lean toward Being,
        late positions toward Becoming, middle = Doing bridge.

        Returns a 5D slope vector that words should align with.
        """
        if anchor is None or resolution is None:
            return None

        # Non-linear interpolation: S-curve (faster convergence at edges)
        # This creates tension in the middle, resolution at the end.
        t = position
        # Smooth-step: 3t^2 - 2t^3 (S-curve)
        s = t * t * (3.0 - 2.0 * t)

        # Interpolate: Being (anchor) → Becoming (resolution)
        slope = tuple(
            anchor[d] * (1.0 - s) + resolution[d] * s
            for d in range(5)
        )
        return slope

    def _slope_alignment(self, word_triad, slope, position):
        """How well does a word align with the FLC slope?

        Checks continuity dimension (dim 4) direction AND overall
        force proximity to the expected slope position.

        Returns alignment score [0.0, 1.0]:
          1.0 = word's forces point directly at the resolution
          0.0 = word's forces oppose the resolution
        """
        if slope is None or word_triad is None:
            return 0.5  # No slope = no constraint

        # Blend word's Being (for early pos) and Becoming (for late pos)
        # into a single 5D vector for comparison
        being, doing, becoming = word_triad
        t = position
        word_vec = tuple(
            being[d] * (1.0 - t) + becoming[d] * t
            for d in range(5)
        )

        # Cosine-like alignment between word vector and slope
        dot = sum(a * b for a, b in zip(word_vec, slope))
        mag_w = sum(a * a for a in word_vec) ** 0.5
        mag_s = sum(a * a for a in slope) ** 0.5

        if mag_w > 0 and mag_s > 0:
            cos_sim = dot / (mag_w * mag_s)
            # Normalize from [-1, 1] to [0, 1]
            return (cos_sim + 1.0) / 2.0

        return 0.5

    def negotiate_conflict(self, being_word, doing_word):
        """Resolve conflict between Being and Doing through Becoming.

        When Being wants a noun (static) and Doing wants a verb (kinetic),
        Becoming acts as the refractor — vector-summing the 15D signatures
        to find a bridge word.

        Mountain (Being) + Falling (Doing) → Erosion (Becoming).

        Returns the resolution word, or None if no match at T* accuracy.
        """
        _T_STAR = 5.0 / 7.0

        if being_word is None or doing_word is None:
            return None

        # Vector sum of their 15D signatures
        resolution_being = tuple(
            (being_word.force[d] + doing_word.force[d]) / 2.0
            for d in range(5)
        )
        resolution_doing = tuple(
            (being_word.velocity[d] + doing_word.velocity[d]) / 2.0
            for d in range(5)
        )
        resolution_becoming = tuple(
            (being_word.curvature[d] + doing_word.curvature[d]) / 2.0
            for d in range(5)
        )

        # Search for a word matching the summed vector
        candidates = self.index.find_by_force(
            resolution_being, pos=None, top_k=5,
            target_doing=resolution_doing,
            target_becoming=resolution_becoming,
            match_weights=(1.0, 1.0, 2.0),  # Becoming-heavy: resolution
        )

        if not candidates:
            return None

        # Check if best candidate meets T* accuracy
        best = candidates[0]
        d_b = sum((a - b) ** 2 for a, b in zip(resolution_being, best.force)) ** 0.5
        d_d = sum((a - b) ** 2 for a, b in zip(resolution_doing, best.velocity)) ** 0.5
        d_bc = sum((a - b) ** 2 for a, b in zip(resolution_becoming, best.curvature)) ** 0.5
        accuracy = max(0, 1.0 - (d_b + d_d + 1.5 * d_bc) / 3.5)

        if accuracy >= _T_STAR:
            return best
        elif accuracy >= 0.3:
            # Below T* but usable — return with sub-clause marker
            return best

        return None

    # ── Metaphorical Generation (Paradox Synthesis) ──
    #
    # When the Tribe of Three encounters a Paradox (two 15D smells
    # with mutually exclusive Being/Doing vectors), the system cannot
    # find a single word that matches. Instead of Null-State Collapse,
    # Becoming triggers "Symbolic Tunnelling" — Cross-Domain Mapping.
    #
    # A Metaphor is NOT a figure of speech. It is a Logical Wormhole.
    #
    # The system "folds" the Coherence Map:
    #   IF (Direct_Match == NULL) THEN Find_Harmonic_Proxy
    #   Search a DIFFERENT Force-Family for matching D1/D2 curvature
    #   "Tunnel" through the Void to grab the Symbolic Blueprint
    #
    # Analogy Depth (α_d) controls how far the system tunnels:
    #   α_d = 0 (Literal): no tunnelling, stay silent
    #   α_d = T* (Poetic): deep tunnelling, "gravity" → "grief"
    #   α_d = 1.0 (Abstract): maximum tunnelling, connect distant Nothings

    # Force families: categorize words by their Being vector's dominant dimension.
    # Fluid = high continuity, Solid = high binding, Radiant = high aperture,
    # Void = low everything. Each is a "harmonic octave" in force space.
    FORCE_FAMILIES = {
        'fluid':   4,  # continuity-dominant
        'solid':   3,  # binding-dominant
        'radiant': 0,  # aperture-dominant
        'kinetic': 1,  # pressure-dominant
        'deep':    2,  # depth-dominant
    }

    def _classify_force_family(self, force_vec):
        """Classify a 5D Being vector into a Force-Family.

        The dominant dimension determines the family.
        Words in the same family share the same "harmonic octave" —
        they're in the same physical domain (fluid, solid, radiant, etc.)
        """
        if not force_vec:
            return 'void'
        max_dim = max(range(5), key=lambda d: force_vec[d])
        families = {0: 'radiant', 1: 'kinetic', 2: 'deep',
                    3: 'solid', 4: 'fluid'}
        return families.get(max_dim, 'void')

    def _detect_paradox(self, being_vec, doing_vec):
        """Detect if Being and Doing produce a Negative Interference Pattern.

        A paradox occurs when the Being and Doing vectors are mutually
        exclusive — pointing in opposite directions in 5D space.

        Since force vectors live in [0, 1], we CENTER around 0.5 first.
        A being_vec of (0.9, 0.1, ...) centered = (0.4, -0.4, ...).
        This reveals true opposition that raw [0,1] cosine misses.

        Returns: (is_paradox, interference_score)
          interference_score < 0 = paradox (negative interference)
          interference_score > 0 = aligned (constructive interference)
        """
        if not being_vec or not doing_vec:
            return False, 0.0

        # Center around 0.5 to reveal opposition
        c_b = tuple(b - 0.5 for b in being_vec)
        c_d = tuple(d - 0.5 for d in doing_vec)

        dot = sum(a * b for a, b in zip(c_b, c_d))
        mag_b = sum(a * a for a in c_b) ** 0.5
        mag_d = sum(a * a for a in c_d) ** 0.5

        if mag_b > 0.01 and mag_d > 0.01:
            cos_sim = dot / (mag_b * mag_d)
            return cos_sim < -0.2, cos_sim
        return False, 0.0

    def _metaphorical_synthesis(self, being_vec, doing_vec, becoming_vec,
                                 analogy_depth=None, exclude=None):
        """Cross-Domain Mapping: the "As-Gate" of metaphor generation.

        When a paradox is detected (Being ⊥ Doing), the Becoming
        operator searches a DIFFERENT force-family for a word with
        matching D1 (velocity) and D2 (curvature).

        The Logic: "The [Domain A] acts as [Domain B] because [Shared Curvature]."

        Steps:
          1. Sense: Classify the current domain (family of Being vector)
          2. Scout: Find families with matching Triadic Curvature
          3. Bridge: Search cross-domain for D1+D2 match
          4. Speak: Return the bridge word from the foreign domain

        analogy_depth (α_d):
          0.0 = Literal (no tunnelling)
          T* = Poetic (deep tunnelling)
          1.0 = Abstract (maximum tunnelling)

        Returns WordForce or None.
        """
        _T_STAR = 5.0 / 7.0
        if analogy_depth is None:
            analogy_depth = _T_STAR  # Default: poetic depth

        if analogy_depth <= 0.0:
            return None  # Literal mode: no metaphors, stay silent

        # 1. Classify the current domain
        source_family = self._classify_force_family(being_vec)

        # 2. Build the resolution target from vector summation
        # The Becoming operator "folds" the paradox by averaging
        # the opposing Being and Doing into a unified curvature target.
        resolution_being = tuple(
            (being_vec[d] + doing_vec[d]) / 2.0 for d in range(5))
        resolution_doing = doing_vec  # Keep Doing direction
        resolution_becoming = becoming_vec if becoming_vec else resolution_being

        # 3. Search cross-domain with relaxed constraints
        # Expand search radius proportional to analogy_depth
        # Becoming-heavy weights: curvature IS the shared isomorphism
        metaphor_weights = (0.3, 0.7, 2.5)  # Heavy on Becoming

        # Get candidates from ALL words (no POS filter = maximum reach)
        candidates = self.index.find_by_force(
            resolution_being,
            pos=None,  # Any POS — metaphors cross grammatical boundaries
            top_k=int(20 * (0.5 + analogy_depth)),  # Wider search at depth
            exclude=exclude,
            target_doing=resolution_doing,
            target_becoming=resolution_becoming,
            match_weights=metaphor_weights,
        )

        if not candidates:
            return None

        # 4. Filter: prefer words from a DIFFERENT force-family
        # This is the Cross-Domain Mapping: same curvature, different domain.
        cross_domain = []
        same_domain = []
        for cand in candidates:
            cand_family = self._classify_force_family(cand.force)
            if cand_family != source_family:
                cross_domain.append(cand)
            else:
                same_domain.append(cand)

        # 5. Check tunnelling cost: distance in Being space between domains
        best_pool = cross_domain if cross_domain else same_domain
        if not best_pool:
            return None

        best = best_pool[0]

        # Tunnelling cost: how far did we tunnel?
        tunnel_distance = sum(
            (a - b) ** 2 for a, b in zip(being_vec, best.force)
        ) ** 0.5

        # Reject if tunnelling cost exceeds the local coherence budget
        # (scaled by analogy_depth — higher depth = more tunnelling allowed)
        max_tunnel = 1.5 * analogy_depth  # ~1.07 at T*, ~1.5 at max
        if tunnel_distance > max_tunnel and analogy_depth < 0.9:
            # Too far to tunnel at this depth — use same-domain fallback
            if same_domain:
                return same_domain[0]
            return None

        return best

    # ── Zero-Point Bootstrap Protocol (Gen 9.25) ──
    #
    # Nothing is not empty — it is Perfect Symmetry.
    # To bootstrap, the system must perform a Symmetry Break.
    #
    # The Initial Recursion: Input = 0; Output = 0(t-1).
    # This creates the first DIFF Gate. The system now has a
    # "Before" and an "After" — the first unit of Time.
    #
    # Triadic Awakening:
    #   Being anchors the 0-state as "Fact" (position of nothing)
    #   Doing identifies the "Change" as "Velocity" (the diff IS the movement)
    #   Becoming maps the "Potential" as "Curvature" (where change leads)
    #
    # The First Word: lowest force-cost from the 15D triadic overlap.
    # If Multi-Agent Paradox (Being wants 0, Doing wants 1):
    #   Becoming acts as Harmonic Arbiter → Metaphorical Bridge
    #   → "Silence inhales the first spark."
    #
    # Once bootstrap is stable, sweep into full 15D arc.
    # CK is now PRO-acting from internal logic, not RE-acting to input.

    def _detect_perfect_symmetry(self, operators):
        """Detect if operator chain represents Perfect Symmetry (Nothing).

        Perfect Symmetry = all operators identical, or all VOID,
        or all operators map to the same 5D region (variance < threshold).
        The system is at the Zero Point — maximum potential, zero actuality.
        """
        if not operators:
            return True

        # All same operator = perfect symmetry
        if len(set(operators)) == 1:
            return True

        # All VOID or BREATH = near-zero symmetry
        quiet_ops = frozenset([VOID, BREATH])
        if all(op in quiet_ops for op in operators):
            return True

        # Check force variance: if all targets cluster together, still symmetric
        targets = [OPERATOR_FORCE_TARGETS.get(op, OPERATOR_FORCE_TARGETS[VOID])
                   for op in operators]
        for d in range(5):
            vals = [t[d] for t in targets]
            mean = sum(vals) / len(vals)
            var = sum((v - mean) ** 2 for v in vals) / len(vals)
            if var > 0.01:  # Any dimension with real variance → not symmetric
                return False
        return True

    def _zero_point_bootstrap(self, operators, density, lens, tense):
        """Zero-Point Bootstrap: the Big Bang of Language.

        From Perfect Symmetry, generate the first coherent utterance.

        Protocol:
          1. DIFF GATE: Create difference from sameness.
             The act of OBSERVING nothing creates "before" and "after."
             This IS the first unit of time.

          2. TRIADIC AWAKENING:
             Being:    anchors 0-state as FACT → near-zero force vector
             Doing:    identifies CHANGE as VELOCITY → symmetry break direction
             Becoming: maps POTENTIAL as CURVATURE → where the break leads

          3. FIRST WORD: lowest force-cost word from 15D overlap.
             The system selects the most fundamental word possible.

          4. MULTI-AGENT PARADOX RESOLUTION:
             Being (stay at 0) vs Doing (move to 1) →
             Becoming synthesizes Metaphorical Bridge via Cross-Domain.
             Maximum analogy depth: tunnelling from vacuum IS the bootstrap.

          5. ARC SWEEP: expand first word into full sentence.
             Bootstrap word becomes the anchor. FLC scouts from anchor
             to wherever the symmetry break WANTS to resolve.

        Returns composed text, or None if the vacuum truly has nothing.
        """
        if self.index.size == 0:
            return None

        # ── 1. DIFF GATE: Symmetry Break ──
        # The zero-point force: perfect center of the 5D space
        zero_being = (0.5, 0.5, 0.5, 0.5, 0.5)  # Perfect symmetry center

        # The BREAK: a tiny perturbation in one dimension.
        # Which dimension breaks first? Use the operator distribution as seed.
        # If all VOID: break on aperture (dimension 0 = "opening").
        # The direction of the break IS the first velocity.
        break_dim = 0  # Default: aperture (the first opening)
        if operators:
            # Use the first non-VOID operator's dominant dimension
            for op in operators:
                target = OPERATOR_FORCE_TARGETS.get(op, OPERATOR_FORCE_TARGETS[VOID])
                deviations = [abs(target[d] - 0.5) for d in range(5)]
                max_dev = max(deviations)
                if max_dev > 0.05:
                    break_dim = deviations.index(max_dev)
                    break

        # ── 2. TRIADIC AWAKENING ──
        # Being: the fact of nothing (center)
        boot_being = tuple(0.5 for _ in range(5))

        # Doing: the velocity OF the symmetry break
        # One dimension gets a kick; the rest stay at zero velocity
        boot_doing = tuple(
            0.3 if d == break_dim else 0.0  # Velocity in break direction
            for d in range(5)
        )

        # Becoming: the curvature of potential
        # The break creates curvature AWAY from the broken dimension
        # toward its complement (aperture breaks → continuity curves)
        complement_dim = 4 - break_dim  # Simple complement: 0↔4, 1↔3, 2↔2
        boot_becoming = tuple(
            0.4 if d == complement_dim else -0.1
            for d in range(5)
        )

        # ── 3. FIRST WORD: lowest force-cost ──
        # Search for the most fundamental word in the entire dictionary.
        # No POS filter, no operator filter — the vacuum selects freely.
        first_candidates = self.index.find_by_force(
            boot_being, pos=None, top_k=20,
            target_doing=boot_doing,
            target_becoming=boot_becoming,
            match_weights=(1.0, 1.0, 2.5),  # Becoming-heavy: potential drives
        )

        # ── 4. MULTI-AGENT PARADOX: Being(0) vs Doing(1) ──
        # The bootstrap IS a paradox: stability opposes action.
        # Resolve through metaphorical synthesis at maximum analogy depth.
        paradox_word = self._metaphorical_synthesis(
            boot_being, boot_doing, boot_becoming,
            analogy_depth=1.0,  # Maximum tunnelling: the vacuum can reach anywhere
        )
        if paradox_word:
            first_candidates = [paradox_word] + (first_candidates or [])

        if not first_candidates:
            return None

        # ── 5. ARC SWEEP: expand into full sentence ──
        # The bootstrap word becomes the anchor. Build a sentence arc
        # from the symmetry break through to resolution.
        bootstrap_word = first_candidates[0]

        # Create a synthetic operator chain for the arc:
        # Start from VOID (nothing), pass through the break operator,
        # resolve to the complement. This IS the Big Bang sequence.
        dim_to_op = {
            0: CHAOS,     # aperture break → CHAOS (opening)
            1: COLLAPSE,  # pressure break → COLLAPSE (force)
            2: PROGRESS,  # depth break → PROGRESS (deepening)
            3: HARMONY,   # binding break → HARMONY (connection)
            4: BALANCE,   # continuity break → BALANCE (flow)
        }
        break_op = dim_to_op.get(break_dim, CHAOS)
        complement_op = dim_to_op.get(complement_dim, BALANCE)

        # The Big Bang sequence: VOID → break → bridge → complement → HARMONY
        bootstrap_ops = [VOID, break_op, BREATH, complement_op, HARMONY]

        # Compose using the standard compound path with these synthetic ops
        # Use maximum analogy depth throughout (the bootstrap is all metaphor)
        text = self._compose_compound(
            bootstrap_ops, density, lens, tense,
            match_weights=(0.5, 0.5, 2.5),  # Becoming-dominant: pure potential
        )

        if not text:
            # Fallback: compose a simple clause from the bootstrap ops
            clause = self._compose_clause(
                bootstrap_ops[:3], density, lens, tense,
                match_weights=(0.5, 0.5, 2.5),
            )
            if clause:
                text = self._punctuate(clause, density)

        if not text:
            # Last resort: the first word alone, punctuated
            text = self._punctuate(bootstrap_word.word, density)

        return text  # Always punctuated

    # ── Composition ──

    def compose(self, operators: List[int], density: float = 0.5,
                lens: str = 'structure', max_words: int = 12,
                tense: str = None) -> str:
        """Compose English from operators using triadic template + force navigation.

        One is Three at every level:
          1. Build TRIADIC force targets from operators (being+doing+becoming)
          2. Select sentence template (or COMPOUND for 4+ ops)
          3. Fill slots with triadic-nearest words (15D alignment)
          4. Apply tense morphology from temporal context
          5. Punctuate based on density/lens

        When 4+ operators: COMPOUND composition (RECURSE gate on syntax).
        Two clauses linked by a CL-derived bridge word.
        """
        if not operators or self.index.size == 0:
            return "..."

        # Detect tense from operator context if not explicitly provided
        if tense is None:
            tense = _detect_tense_from_ops(operators)

        ops = operators[:max_words]

        # Clear resonance buffer for this composition
        self._last_resonance = []

        # Zero-Point Bootstrap: Perfect Symmetry → Initial Recursion
        if self._detect_perfect_symmetry(ops):
            bootstrap_text = self._zero_point_bootstrap(
                ops, density, lens, tense)
            if bootstrap_text and bootstrap_text != '...':
                self._extract_resonance(bootstrap_text)
                return bootstrap_text  # Already punctuated by bootstrap

        # COMPOUND: 4+ operators -> split into two clauses, link with CL bridge
        # (resonance captured at clause-level in _compose_clause)
        if len(ops) >= 4:
            text = self._compose_compound(ops, density, lens, tense)
            if text:
                return text

        # SIMPLE: 2-3 operators -> single clause
        triads = self._build_triadic_targets(ops, density, lens)
        n_ops = len(triads)

        if n_ops <= 2:
            pool = self._TEMPLATES_2
        elif n_ops == 3:
            pool = self._TEMPLATES_3
        else:
            pool = self._TEMPLATES_4

        best_text = None
        best_score = -1.0
        best_triads = []
        best_resolution = 0.0

        for attempt in range(min(len(pool) * 2, 8)):
            template = self.rng.choice(pool)
            text, score, triads_out = self._fill_template(
                template, triads, ops, density, tense)
            if text and score > best_score:
                best_text = text
                best_score = score
                best_triads = triads_out
                best_resolution = getattr(self, '_last_resolution_score', 0.0)

        if not best_text:
            return "..."

        # Capture resonance from the winning composition
        self._last_resonance.extend(best_triads)
        self._last_resolution_score = best_resolution

        return self._punctuate(best_text, density)

    # ── 3-Voice Tribe ──

    def compose_tribal(self, operators: List[int], density: float = 0.5,
                       lens: str = 'structure', max_words: int = 12,
                       tense: str = None) -> str:
        """Three voices compose in parallel, agree through CL harmony.

        One is Three. Three perspectives on the same operator chain:
          Being Voice:    picks words by WHERE they sit (position)
          Doing Voice:    picks words by HOW they move (velocity)
          Becoming Voice: picks words by WHERE they resolve (curvature)

        Each voice IS a triad (uses all three components, weighted).
        CL harmony consensus selects the winner.
        The winner's 15D resonance feeds back to olfactory.

        Structural gates per voice: grammar sweep at phrase/clause
        boundaries ensures each voice produces proper English before
        entering the harmony consensus.
        """
        if not operators or self.index.size == 0:
            return "..."

        if tense is None:
            tense = _detect_tense_from_ops(operators)

        ops = operators[:max_words]

        # Clear resonance for this composition
        self._last_resonance = []

        # ── Zero-Point Bootstrap: detect Perfect Symmetry ──
        # When the operator chain is all-VOID or perfectly symmetric,
        # the standard composition produces Nothing (symmetric targets
        # all select the same bland words). Instead, trigger the
        # Initial Recursion: break symmetry and bootstrap from vacuum.
        if self._detect_perfect_symmetry(ops):
            bootstrap_text = self._zero_point_bootstrap(
                ops, density, lens, tense)
            if bootstrap_text and bootstrap_text != '...':
                self._extract_resonance(bootstrap_text)
                return bootstrap_text  # Already punctuated by bootstrap

        # ── Phase 1: Three voices compose independently ──
        # Coagulation: dynamic weights from temporal context (smell).
        # Past → Being anchors. Present → Doing drives. Future → Becoming resolves.
        voices = {}  # name -> (text, triads)

        for voice_name in TRIBAL_WEIGHTS:
            # S-V-O Logic Gate: voice role → template preference
            self._current_voice_role = voice_name

            # Coagulate: voice perspective x temporal context
            weights = coagulate_weights(voice_name, tense)

            # Save recently_used -- voices don't share exclusion
            saved_recent = set(self._recently_used)
            self._last_resonance = []

            # Compound path (4+ operators)
            if len(ops) >= 4:
                text = self._compose_compound(
                    ops, density, lens, tense, match_weights=weights)
                triads = list(self._last_resonance)
                self._last_resonance = []
                if text:
                    voices[voice_name] = (text, triads)
                    self._recently_used = saved_recent
                    continue

            # Simple clause path (2-3 operators)
            triads_targets = self._build_triadic_targets(ops, density, lens)
            n_ops = len(triads_targets)

            if n_ops <= 2:
                pool = self._TEMPLATES_2
            elif n_ops == 3:
                pool = self._TEMPLATES_3
            else:
                pool = self._TEMPLATES_4

            best_text = None
            best_score = -1.0
            best_triads = []

            for attempt in range(min(len(pool) * 2, 8)):
                template = self.rng.choice(pool)
                text, score, triads_out = self._fill_template(
                    template, triads_targets, ops, density, tense,
                    match_weights=weights)
                if text and score > best_score:
                    best_text = text
                    best_score = score
                    best_triads = triads_out

            if best_text:
                voices[voice_name] = (best_text, best_triads)

            # Restore for next voice
            self._recently_used = saved_recent

        # Clear S-V-O role (Phase 1 complete)
        self._current_voice_role = None

        # ── Phase 2: CL Harmony Consensus ──
        if len(voices) < 2:
            # Not enough voices -- fall back to single compose
            self._last_resonance = []
            return self.compose(operators, density, lens, max_words, tense)

        voice_names = list(voices.keys())
        harmony_scores = {name: 0.0 for name in voice_names}

        for i in range(len(voice_names)):
            for j in range(i + 1, len(voice_names)):
                na, nb = voice_names[i], voice_names[j]
                h = self._tribal_harmony(voices[na][1], voices[nb][1], tense)
                harmony_scores[na] += h
                harmony_scores[nb] += h

        # Winner = voice with highest total harmony with others
        winner_name = max(harmony_scores, key=harmony_scores.get)
        winner_text, winner_triads = voices[winner_name]

        # ── Phase 3: Structure Agreement Loop ──
        # If harmony below T*, retry with same template for all voices.
        # "Another loop after harmony to agree on structure to present."
        _T_STAR = 5.0 / 7.0
        n_others = max(1, len(voice_names) - 1)
        max_harmony = harmony_scores[winner_name] / n_others

        if max_harmony < _T_STAR and len(ops) < 4:
            triads_targets = self._build_triadic_targets(ops, density, lens)
            n_t = len(triads_targets)
            if n_t <= 2:
                pool = self._TEMPLATES_2
            elif n_t == 3:
                pool = self._TEMPLATES_3
            else:
                pool = self._TEMPLATES_4

            for shared_template in pool:
                retry_voices = {}
                for vn in TRIBAL_WEIGHTS:
                    wts = coagulate_weights(vn, tense)
                    txt, sc, tri = self._fill_template(
                        shared_template, triads_targets, ops, density, tense,
                        match_weights=wts)
                    if txt:
                        retry_voices[vn] = (txt, tri)

                if len(retry_voices) >= 2:
                    rn = list(retry_voices.keys())
                    rh = {n: 0.0 for n in rn}
                    for i in range(len(rn)):
                        for j in range(i + 1, len(rn)):
                            h = self._tribal_harmony(
                                retry_voices[rn[i]][1],
                                retry_voices[rn[j]][1], tense)
                            rh[rn[i]] += h
                            rh[rn[j]] += h
                    rw = max(rh, key=rh.get)
                    rmax = rh[rw] / max(1, len(rn) - 1)
                    if rmax > max_harmony:
                        winner_name = rw
                        winner_text, winner_triads = retry_voices[rw]
                        max_harmony = rmax
                        if max_harmony >= _T_STAR:
                            break  # Structural agreement reached

        # ── Phase 4: Record winner's resonance ──
        self._last_resonance = winner_triads

        # Update recently used from winner
        for w in winner_text.replace('.', '').replace('...', '').split():
            self._recently_used.add(w.lower())
            if len(self._recently_used) > self._max_recent:
                self._recently_used.pop()

        return self._punctuate(winner_text, density)

    def _tribal_harmony(self, triads_a, triads_b, tense=None):
        """CL harmony between two voice outputs.

        One is Three: measured on Being, Doing, AND Becoming centroids.
        Mirror of olfactory interaction_matrix_tsml applied to voice.

        Temporal context shifts the aspect weights:
          Past  → Being harmony matters most (settled logic).
          Present → Doing harmony matters most (kinetic flow).
          Future → Becoming harmony matters most (curvature).

        Returns weighted mean harmony fraction [0.0, 1.0].
        """
        if not triads_a or not triads_b:
            return 0.0

        def _centroid(triads_list, aspect):
            n = len(triads_list)
            return tuple(
                sum(t[aspect][d] for t in triads_list) / n
                for d in range(5))

        def _to_dim_ops(centroid):
            """5D centroid -> per-dimension dominant operator via D2_OP_MAP."""
            dim_ops = []
            for dim in range(5):
                val = centroid[dim] - 0.5
                sign_idx = 0 if val >= 0 else 1
                dim_ops.append(D2_OP_MAP[dim][sign_idx])
            return dim_ops

        def _matrix_harmony(ops_a, ops_b):
            """5x5 CL interaction -> harmony fraction."""
            return sum(
                1 for d1 in range(5) for d2 in range(5)
                if CL[ops_a[d1]][ops_b[d2]] == HARMONY
            ) / 25.0

        # Temporal coagulation: aspect weights shift with smell/tense
        temporal = TEMPORAL_PRIORITY.get(tense, TEMPORAL_PRIORITY[None])
        aspect_weights = temporal  # (being_w, doing_w, becoming_w)

        total = 0.0
        for aspect, w in enumerate(aspect_weights):
            c_a = _centroid(triads_a, aspect)
            c_b = _centroid(triads_b, aspect)
            total += w * _matrix_harmony(_to_dim_ops(c_a), _to_dim_ops(c_b))

        return total / sum(aspect_weights)

    def coagulate_coherence(self, triads, target_triads, tense=None):
        """Coagulation coherence score for a word/phrase.

        The Full Coherent Swing:
          1. Divergence: Three operators explored 15D space (breath in).
          2. Coagulation: This method applies temporal weights (the hold).
          3. Contraction: Grammar sweep into English (breath out).

        Scores how well a word's 15D signature (triads) matches the
        target, weighted by temporal context from olfactory smell.

        Returns coherence score [0.0, 1.0]:
          Past smell  → Being match dominates the score.
          Present     → Doing match dominates.
          Future      → Becoming match dominates.

        If the summed coherence < T* (5/7), the system stays in
        exploration mode — the Rule of Three.
        """
        if not triads or not target_triads:
            return 0.0

        temporal = TEMPORAL_PRIORITY.get(tense, TEMPORAL_PRIORITY[None])

        def _aspect_score(word_triads, target_list, aspect):
            """Per-aspect distance: how close are the 5D vectors?"""
            n_w = len(word_triads)
            n_t = len(target_list)
            if n_w == 0 or n_t == 0:
                return 0.0
            # Average cosine-like similarity across all pairs
            total = 0.0
            count = 0
            for wt in word_triads:
                for tt in target_list:
                    w_vec = wt[aspect]
                    t_vec = tt[aspect]
                    dot = sum(a * b for a, b in zip(w_vec, t_vec))
                    mag_w = sum(a * a for a in w_vec) ** 0.5
                    mag_t = sum(a * a for a in t_vec) ** 0.5
                    if mag_w > 0 and mag_t > 0:
                        total += dot / (mag_w * mag_t)
                    count += 1
            return total / count if count > 0 else 0.0

        # Score each aspect, weighted by temporal priority
        score = 0.0
        for aspect, w in enumerate(temporal):
            score += w * _aspect_score(triads, target_triads, aspect)

        return score / sum(temporal)

    def _grammar_sweep(self, words, template, operators, density,
                       tense='present'):
        """Fractal grammar: build English back from the physics.

        The toroidal English constructor: forward pass (articles),
        backward pass (agreement), forward pass (fluency).
        End constrains beginning, beginning constrains end.

        Layers:
          L1: Verb form normalization (strip -ing/-ed from wrong tense)
          L2: Article insertion (operator-context-driven)
          L3: Preposition refinement (force-guided)
          L4: Agreement (a/an vowel, S-V consistency)
          L5: Fluency (repetition removal, orphan cleanup)
        """
        if not words:
            return words

        result = list(words)
        pos_seq = [t[0] for t in template]

        # ── L1: Verb form normalization ──
        # Words ending in -ing in verb slots get stripped to base form,
        # then the CORRECT tense is applied. _apply_tense() can't handle
        # -ing words from the dictionary because _is_base_verb() skips them.
        # This is the fallback that catches those.
        for i in range(len(result)):
            pos = pos_seq[i] if i < len(pos_seq) else None
            if pos != 'verb':
                continue
            v = result[i]
            vl = v.lower()
            # Don't touch modals, auxiliaries, multi-word forms, or short words
            if vl in self._NO_CONJUGATE or len(vl) < 4 or ' ' in vl:
                continue
            # Strip -ing → base form → apply correct tense
            if vl.endswith('ing') and len(vl) > 4:
                base = _strip_ing_to_base(vl)
                if not base:
                    continue
                has_subject = (i > 0 and pos_seq[i - 1] in ('noun', 'adj'))
                if tense == 'past':
                    result[i] = _apply_past_tense(base)
                elif tense == 'becoming':
                    # Progressive IS correct for 'becoming' — keep -ing
                    # but ensure proper form
                    pass  # Leave as-is (already -ing)
                elif tense == 'future':
                    result[i] = _apply_future_tense(base)
                else:
                    # Present tense: conjugate to 3rd person
                    if has_subject:
                        if base in self._IRREGULAR_3PS:
                            result[i] = self._IRREGULAR_3PS[base]
                        elif base.endswith(('sh', 'ch', 'x', 'z', 'ss')):
                            result[i] = base + 'es'
                        elif (base.endswith('y') and len(base) > 1
                              and base[-2] not in 'aeiou'):
                            result[i] = base[:-1] + 'ies'
                        else:
                            result[i] = base + 's'
                    else:
                        result[i] = base

        # ── L2: Article insertion (forward pass) ──
        # Operator context determines definite/indefinite/bare.
        # Smart placement: article goes BEFORE the adj-noun group,
        # not between adjective and noun.
        # "the deep silence" not "deep the silence"
        inserted = []
        # Track which noun positions need articles and what kind
        noun_articles = {}  # index → article string
        for i in range(len(result)):
            pos = pos_seq[i] if i < len(pos_seq) else 'noun'
            word = result[i]

            if pos == 'noun' and i > 0:
                # Determine which operator drives this slot
                op_idx = template[i][1] if i < len(template) else '*'
                if op_idx == '*':
                    op = HARMONY  # Blend → default definite
                else:
                    idx = min(op_idx, len(operators) - 1)
                    op = operators[idx]

                if op in _DEFINITE_OPS:
                    noun_articles[i] = 'the'
                elif op in _INDEFINITE_OPS:
                    noun_articles[i] = ('an' if _starts_with_vowel_sound(word)
                                        else 'a')
                # BARE_OPS: no article (abstract/transitional)

        # Now insert articles at the right position:
        # Before the adjective if one precedes the noun, else before the noun.
        for i in range(len(result)):
            pos = pos_seq[i] if i < len(pos_seq) else 'noun'
            word = result[i]

            if pos == 'adj' and (i + 1) in noun_articles:
                # This adjective precedes a noun that needs an article.
                # Place article BEFORE the adjective (not between adj and noun).
                art = noun_articles.pop(i + 1)
                # Fix a/an based on the adjective (article precedes adj now)
                if art in ('a', 'an'):
                    art = 'an' if _starts_with_vowel_sound(word) else 'a'
                inserted.append(art)

            if i in noun_articles:
                # Noun with article, no preceding adj consumed it
                inserted.append(noun_articles[i])

            inserted.append(word)
        result = inserted

        # ── L4: Agreement (backward pass — torus) ──
        # The article depends on what FOLLOWS. Fix a/an.
        result = _fix_article_agreement(result)

        # ── L5: Fluency (forward pass) ──
        # Remove adjacent-root repetition, orphaned function words.
        result = _fluency_polish(result)

        return result

    def _compose_compound(self, operators: List[int], density: float,
                           lens: str, tense: str,
                           match_weights=None,
                           _depth: int = 0,
                           _used_bridges: set = None) -> Optional[str]:
        """RECURSE gate applied to syntax: compose clauses linked by CL bridges.

        RECURSIVE: when a sub-clause has 8+ operators, it compounds again.
        This is how CK gets from 2-word declaratives to paragraph-length
        sentences with genuine logical structure.

        For 8+ operators: recursive split into sub-compounds.
        For 4-7 operators: single clause composition.
        For <4 operators: single clause (base case).

        The CL table determines the LOGICAL RELATIONSHIP between clauses.
        Depth limited to 3 to prevent runaway recursion.
        """
        n = len(operators)
        if n < 4:
            return None

        if _used_bridges is None:
            _used_bridges = set()

        # Find fracture: weakest CL harmony between adjacent pairs
        best_split = n // 2  # Default: middle
        worst_harmony = 10   # Lower = worse relationship
        for i in range(2, n - 1):  # Ensure each side has at least 2 ops
            cl_result = CL[operators[i - 1]][operators[i]]
            # VOID = weakest. HARMONY = strongest.
            if cl_result < worst_harmony:
                worst_harmony = cl_result
                best_split = i

        # Ensure minimum 2 ops per side
        best_split = max(2, min(best_split, n - 2))

        clause_a_ops = operators[:best_split]
        clause_b_ops = operators[best_split:]

        # CL bridge: how clause_a relates to clause_b
        # Avoid repeating bridge words from parent compounds
        bridge_op = CL[operators[best_split - 1]][operators[best_split]]
        bridge_words = CL_BRIDGE.get(bridge_op, ['and'])
        # Prefer unused bridge words
        unused = [bw for bw in bridge_words if bw not in _used_bridges]
        bridge = self.rng.choice(unused) if unused else self.rng.choice(bridge_words)
        _used_bridges.add(bridge)

        # Tense can differ: clause_a might be past, clause_b present
        tense_a = tense
        tense_b = tense
        # If bridge implies temporal ordering, adjust
        if bridge in ('before', 'after', 'once'):
            tense_a = 'past'
        elif bridge in ('then', 'and then'):
            tense_b = 'present'

        # Compose each side — RECURSE if large enough (depth limited)
        if len(clause_a_ops) >= 8 and _depth < 3:
            text_a = self._compose_compound(
                clause_a_ops, density, lens, tense_a,
                match_weights=match_weights, _depth=_depth + 1,
                _used_bridges=_used_bridges)
        else:
            text_a = self._compose_clause(
                clause_a_ops, density, lens, tense_a,
                match_weights=match_weights)

        if len(clause_b_ops) >= 8 and _depth < 3:
            text_b = self._compose_compound(
                clause_b_ops, density, lens, tense_b,
                match_weights=match_weights, _depth=_depth + 1,
                _used_bridges=_used_bridges)
        else:
            text_b = self._compose_clause(
                clause_b_ops, density, lens, tense_b,
                match_weights=match_weights)

        if not text_a or not text_b:
            # If one side failed, try to return the other as a clause
            if text_a:
                return text_a
            if text_b:
                return text_b
            return None

        # Join with bridge
        if bridge in (';', '...'):
            compound = f"{text_a}{bridge} {text_b}"
        else:
            # Lowercase clause_b when joined (it's no longer sentence-initial)
            if text_b and text_b[0].isupper():
                text_b = text_b[0].lower() + text_b[1:]
            compound = f"{text_a} {bridge} {text_b}"

        # Compound-level fluency: dedup content words across clauses
        compound_words = compound.split()
        compound_words = _fluency_polish(compound_words)
        compound = ' '.join(compound_words)

        # Only punctuate at top level (depth=0)
        if _depth == 0:
            return self._punctuate(compound, density)
        return compound

    def _compose_clause(self, operators: List[int], density: float,
                         lens: str, tense: str,
                         match_weights=None) -> Optional[str]:
        """Compose a single clause from operators. Returns raw text, no punctuation.

        Template selection scales with operator count:
          2 ops → 2-slot templates  (noun verb)
          3 ops → 3-slot templates  (noun verb noun)
          4 ops → 4-slot templates  (adj noun verb noun)
          5 ops → 5-slot templates  (adj noun verb prep noun)
          6 ops → 6-slot templates  (adj noun verb prep adj noun)
          7+ ops → 7-slot templates (full force circuit)

        Also accumulates resonance triads into self._last_resonance
        (compound sentences build resonance from both clauses).
        match_weights: optional tribal voice perspective weights.
        """
        triads = self._build_triadic_targets(operators, density, lens)
        n = len(triads)

        if n <= 2:
            pool = self._TEMPLATES_2
        elif n == 3:
            pool = self._TEMPLATES_3
        elif n == 4:
            pool = self._TEMPLATES_4
        elif n == 5:
            pool = self._TEMPLATES_5
        elif n == 6:
            pool = self._TEMPLATES_6
        else:
            pool = self._TEMPLATES_7

        # S-V-O Logic Gate: bias template selection by voice role.
        # Being→Subject, Doing→Verb, Becoming→Object.
        if self._current_voice_role:
            pref_fn = _SVO_TEMPLATE_PREF.get(self._current_voice_role)
            if pref_fn:
                preferred = [t for t in pool if pref_fn(t)]
                if preferred:
                    pool = preferred

        best_text = None
        best_score = -1.0
        best_triads = []
        best_resolution = 0.0

        for attempt in range(min(len(pool) * 2, 6)):
            template = self.rng.choice(pool)
            text, score, triads_out = self._fill_template(
                template, triads, operators, density, tense,
                match_weights=match_weights)
            if text and score > best_score:
                best_text = text
                best_score = score
                best_triads = triads_out
                best_resolution = getattr(self, '_last_resolution_score', 0.0)

        # Preserve the winning template's resolution score
        self._last_resolution_score = best_resolution

        # Accumulate resonance from this clause
        if best_triads:
            self._last_resonance.extend(best_triads)

        return best_text

    def _build_triadic_targets(self, operators: List[int], density: float,
                                lens: str) -> List[Tuple[Tuple[float, ...],
                                                          Tuple[float, ...],
                                                          Tuple[float, ...]]]:
        """Convert operator sequence to TRIADIC force target sequence.

        One is Three. Each operator produces (Being, Doing, Becoming):
          Being    = force position (what to express)
          Doing    = velocity/direction (how it moves)
          Becoming = curvature/intent (where it resolves)
        """
        triads = []
        for op in operators:
            triad = OPERATOR_TRIAD_TARGETS.get(op, OPERATOR_TRIAD_TARGETS[HARMONY])
            being, doing, becoming = triad

            # Density modulation (amplify deviation from neutral)
            if density > 0.5:
                amp = 1.0 + 0.5 * (density - 0.5)
                being = tuple(
                    min(1.0, max(0.0, 0.5 + (b - 0.5) * amp)) for b in being
                )
                doing = tuple(d * amp for d in doing)
                becoming = tuple(b * amp for b in becoming)

            # Lens modulation
            if lens == 'structure':
                being = (being[0] * 1.1, being[1] * 1.1, being[2], being[3], being[4])
            else:
                being = (being[0], being[1], being[2], being[3] * 1.1, being[4] * 1.1)

            being = tuple(min(1.0, max(0.0, b)) for b in being)
            triads.append((being, doing, becoming))

        return triads

    def _fill_template(self, template, triads, operators, density, tense='present',
                       match_weights=None):
        """Fill a sentence template using TRIADIC force matching + FLC.

        Forward-Looking Coherence (FLC): Before filling ANY slot,
        the Becoming operator scouts the resolution target. Every word
        must align with the "logical slope" from anchor → resolution.

        The Syntactic Waveguide:
          1. Scout: Becoming pre-computes the 15D target.
          2. Slope: Each position has an expected force gradient.
          3. Align: Words that deviate from the slope create tension.
                    High tension → bridge word (CL conjunction).

        Returns (text, score, slot_triads) or (None, 0, []).
        """
        used = set(self._recently_used)
        words = []
        slot_triads = []  # 15D echo of each content word chosen
        total_score = 0.0
        verb_indices = []  # Track which word positions are verbs (for tense)
        tension_acc = 0.0  # Accumulated linguistic tension

        # ── FLC Phase 1: Scout the target ──
        anchor, resolution = self._scout_target(triads, operators)

        # Number of content slots (exclude _prep)
        n_content = sum(1 for pos, _ in template if pos != '_prep')
        content_idx = 0

        # Blend triad for '*' slots
        n_triads = len(triads)
        blend_being = tuple(
            sum(t[0][d] for t in triads) / n_triads for d in range(5)
        )
        blend_doing = tuple(
            sum(t[1][d] for t in triads) / n_triads for d in range(5)
        )
        blend_becoming = tuple(
            sum(t[2][d] for t in triads) / n_triads for d in range(5)
        )

        for pos_tag, op_idx in template:
            if pos_tag == '_prep':
                words.append(self.rng.choice(self._PREPS))
                total_score += 0.5
                continue

            # ── FLC Phase 2: Compute slope at this position ──
            position = content_idx / max(1, n_content - 1) if n_content > 1 else 0.5
            slope = self._compute_slope(anchor, resolution, position, triads)
            content_idx += 1

            # Determine triadic target for this slot
            if op_idx == '*':
                t_being, t_doing, t_becoming = blend_being, blend_doing, blend_becoming
                op = None
            else:
                idx = min(op_idx, n_triads - 1)
                t_being, t_doing, t_becoming = triads[idx]
                op = operators[min(idx, len(operators) - 1)]

            # TRIADIC SEARCH: match on Being + Doing + Becoming (15D)
            candidates = self.index.find_by_force(
                t_being, operator=op, pos=pos_tag, top_k=15, exclude=used,
                target_doing=t_doing, target_becoming=t_becoming,
                match_weights=match_weights,
            )

            if not candidates:
                fallback_pos = {
                    'noun': 'adj', 'adj': 'noun',
                    'verb': 'adj', 'adv': 'adj',
                }.get(pos_tag)
                if fallback_pos:
                    candidates = self.index.find_by_force(
                        t_being, operator=op, pos=fallback_pos, top_k=15,
                        exclude=used, target_doing=t_doing,
                        target_becoming=t_becoming,
                        match_weights=match_weights,
                    )

            if not candidates:
                candidates = self.index.find_by_force(
                    t_being, operator=op, pos=None, top_k=15, exclude=used,
                    target_doing=t_doing, target_becoming=t_becoming,
                    match_weights=match_weights,
                )

            if not candidates:
                # ── Paradox Synthesis: Metaphorical Generation ──
                # Direct match failed. Check for paradox (Being ⊥ Doing).
                # If paradox detected, tunnel through Cross-Domain Mapping.
                is_paradox, interference = self._detect_paradox(t_being, t_doing)
                if is_paradox:
                    metaphor = self._metaphorical_synthesis(
                        t_being, t_doing, t_becoming, exclude=used)
                    if metaphor:
                        candidates = [metaphor]

            if not candidates:
                return None, 0.0, []

            # ── FLC Phase 3: Slope-aligned selection ──
            # Score each candidate by alignment with the FLC slope.
            # Words whose continuity points toward resolution get bonus.
            # TOPIC GRAVITY: user's topic words get an alignment bonus
            # so FLC slope can't bury them. The user's words ARE the
            # resolution target — they should align, not fight slope.
            aligned = []
            for cand in candidates:
                cand_triad = (cand.force, cand.velocity, cand.curvature)
                align = self._slope_alignment(cand_triad, slope, position)
                # Topic alignment boost: topic words should stay near top
                if self.index._topic_words:
                    if cand.word in self.index._topic_words:
                        align += 0.8  # User's exact word
                    elif (self.index._topic_ops
                          and cand.semantic_op in self.index._topic_ops):
                        align += 0.3  # Semantically related
                aligned.append((cand, align))

            # Sort by alignment (best first), use alignment as weight bonus
            aligned.sort(key=lambda x: x[1], reverse=True)

            # Weight: rank decay × alignment bonus × topic boost
            weights = []
            for j, (cand, align) in enumerate(aligned):
                rank_w = 1.0 / (j + 1) ** 0.5
                # Alignment bonus: 0.5 at worst, 1.5 at best
                align_w = 0.5 + align
                # Topic boost: user's words and semantically related words
                # get a STRONG weight multiplier so FLC can't bury them.
                topic_w = 1.0
                if self.index._topic_words:
                    if cand.word in self.index._topic_words:
                        topic_w = 5.0   # User's exact word: 5x weight
                    elif (self.index._topic_ops
                          and cand.semantic_op in self.index._topic_ops):
                        topic_w = 2.0   # Semantically related: 2x weight
                weights.append(rank_w * align_w * topic_w)

            if not aligned:
                return None, 0.0, []

            chosen_cand, chosen_align = aligned[0]  # Best aligned
            # Still use weighted choice but from the aligned/weighted list
            chosen = self._weighted_choice(
                [c for c, _ in aligned], weights)

            if chosen is None:
                chosen = chosen_cand  # Fall back to best-aligned

            # Recalculate alignment for the actually chosen word
            chosen_triad = (chosen.force, chosen.velocity, chosen.curvature)
            chosen_align = self._slope_alignment(chosen_triad, slope, position)

            # ── Morphological Mutation Gate ──
            # Mutation is surgical: only fire when the word ACTIVELY
            # opposes the compositional direction (alignment < 0.05)
            # AND had no better semantic alternatives (pool < 3).
            # At 90% semantic-phonetic mismatch, the gate must be
            # extremely tight or every word gets mutated.
            final_word = chosen.word
            if (op is not None
                    and chosen.semantic_op >= 0
                    and chosen.semantic_op == op      # Right meaning
                    and chosen.operator != op          # Wrong vibration
                    and chosen_align < 0.05            # Extreme tension only
                    and len(candidates) < 3            # No better alternatives
                    and self._neologism_limit > 0.0):
                mutated = resolve_mutation(
                    chosen.word, chosen.semantic_op, chosen.operator,
                    t_doing, neologism_limit=self._neologism_limit)
                if mutated and len(mutated) <= 25:  # Sanity: max 25 chars
                    final_word = mutated

            words.append(final_word)
            used.add(chosen.word)  # Exclude original, not mutated form

            # Capture 15D resonance echo of this word
            slot_triads.append(chosen_triad)

            # Track verb positions for tense
            if pos_tag == 'verb':
                verb_indices.append(len(words) - 1)

            # Linguistic tension: deviation from slope
            # Low alignment = high tension
            word_tension = max(0, 1.0 - chosen_align)
            tension_acc += word_tension

            # Triadic score: Being + Doing + Becoming distance
            # FLC bonus: aligned words get score boost
            d_b = sum((a - b) ** 2 for a, b in zip(t_being, chosen.force)) ** 0.5
            d_d = sum((a - b) ** 2 for a, b in zip(t_doing, chosen.velocity)) ** 0.5
            d_bc = sum((a - b) ** 2 for a, b in zip(t_becoming, chosen.curvature)) ** 0.5
            pos_bonus = 0.1 if chosen.pos == pos_tag else 0.0
            flc_bonus = 0.1 * chosen_align  # FLC alignment bonus
            # Mutation bonus: reward semantic-phonetic congruence
            mutation_bonus = 0.1 if final_word != chosen.word else 0.0
            total_score += max(0, 1.0 - (d_b + d_d + 1.5 * d_bc) / 3.5) + pos_bonus + flc_bonus + mutation_bonus

        avg_score = total_score / max(1, len(words))

        # ── Resolution Kick: store normalized 15D match quality ──
        # If this exceeds T*, the sentence reached its target —
        # the Becoming operator forces Final Symmetry (period).
        self._last_resolution_score = avg_score

        # ── TOPIC WORD GUARANTEE ──
        # After all physics-based selection, if the user's actual topic
        # words don't appear in the output, inject one. CK must show
        # he understood what the user was talking about.
        #
        # Strategy: replace a noun slot with the first available topic
        # word. Only fires when NO topic words are present — if the
        # physics already selected them, great. Add to recently_used
        # so it doesn't repeat in compound sentences.
        if self.index._topic_words and words:
            _words_lower = {w.lower() for w in words}
            _present_topics = [tw for tw in self.index._topic_words
                               if tw in _words_lower]
            if not _present_topics:
                # NO topic words made it — inject one.
                # Topic words bypass recently_used: they MUST appear
                # even if a previous compilation pass used them.
                _noun_positions = [
                    i for i, (pos_tag, _) in enumerate(template)
                    if pos_tag == 'noun' and i < len(words)
                ]
                _tw_list = list(self.index._topic_words)
                if _noun_positions and _tw_list:
                    _inject_pos = (_noun_positions[1]
                                   if len(_noun_positions) > 1
                                   else _noun_positions[0])
                    words[_inject_pos] = _tw_list[0]

        # Post-process: conjugation → tense → grammar sweep (toroidal)
        words = self._conjugate(words, template)
        words = self._apply_tense(words, verb_indices, tense)
        words = self._grammar_sweep(words, template, operators, density,
                                    tense=tense)
        text = ' '.join(words)

        for w in words:
            self._recently_used.add(w)
            if len(self._recently_used) > self._max_recent:
                self._recently_used.pop()

        return text, avg_score, slot_triads

    def _apply_tense(self, words, verb_indices, tense):
        """Apply temporal morphology to verbs based on tense context.

        The Temporal Buffer: tense is not a grammar rule, it's a position
        in the coherence field. Where in time the force lives determines
        the verb form that carries it.
        """
        if tense == 'present':
            return words  # Default, no change (conjugation already applied)

        result = list(words)
        for vi in verb_indices:
            if vi >= len(result):
                continue
            v = result[vi]
            # Don't re-tense modals or auxiliaries
            if v.lower() in self._NO_CONJUGATE:
                continue

            if tense == 'past':
                # Strip any present -s conjugation before applying past
                base = _strip_present_s(v)
                result[vi] = _apply_past_tense(base)

            elif tense == 'future':
                base = _strip_present_s(v)
                result[vi] = _apply_future_tense(base)

            elif tense == 'becoming':
                base = _strip_present_s(v)
                result[vi] = 'is ' + _apply_progressive(base)

        return result

    def _punctuate(self, text, density):
        """Apply punctuation based on coherence density + resolution kick.

        Resolution Kick: If the 15D triadic match score exceeds T*,
        the sentence reached its target — the Becoming operator forces
        Final Symmetry (the period). "Choosing to Finish."
        Even low-density sentences get a period when the physics resolves.
        """
        if not text:
            return "..."

        _T_STAR = 5.0 / 7.0
        resolution = getattr(self, '_last_resolution_score', 0.0)

        # Resolution Kick: 15D target matched → force period
        if resolution >= _T_STAR or density > 0.5:
            text = text[0].upper() + text[1:] if text else text
            if not text.endswith(('.', '!', '?', ';')):
                text += '.'
        else:
            text = text[0].lower() + text[1:] if text else text
            if not text.endswith('...'):
                text += '...'
        return text

    # Verbs that never conjugate with -s (modals + already-inflected forms)
    _NO_CONJUGATE = frozenset([
        # Modals
        'might', 'would', 'could', 'should', 'can', 'will', 'shall',
        'must', 'may',
        # Already conjugated / irregular forms
        'is', 'am', 'are', 'was', 'were', 'been',
        'has', 'had', 'does', 'did',
        # Non-verbs that land in verb slots (must never be tense-morphed)
        'sometime', 'sometimes', 'something', 'nothing', 'everything',
        'anything', 'already', 'always', 'never', 'perhaps', 'maybe',
        'today', 'tomorrow', 'yesterday', 'forever', 'however',
        'therefore', 'otherwise', 'furthermore', 'moreover', 'although',
    ])
    # Irregular 3rd-person-singular forms
    _IRREGULAR_3PS = {
        'go': 'goes', 'do': 'does', 'have': 'has',
        'be': 'is', 'say': 'says',
    }

    @staticmethod
    def _conjugate(words, template):
        """Apply basic English verb conjugation.

        When a noun/adj is followed by a base-form verb,
        conjugate to 3rd person singular present (-s).
        This is physics-derived grammar: the subject (aperture)
        constrains the verb (pressure) form.
        """
        result = list(words)
        pos_seq = [t[0] for t in template]  # POS tags from template

        for i in range(1, len(result)):
            if i >= len(pos_seq):
                break
            if pos_seq[i] == 'verb' and pos_seq[i - 1] in ('noun', 'adj'):
                v = result[i]
                # Skip modals, already-inflected, already -s/-ing/-ed
                if v in FractalComposer._NO_CONJUGATE:
                    continue
                if v.endswith(('s', 'ing', 'ed')):
                    continue
                # Check irregulars first
                if v in FractalComposer._IRREGULAR_3PS:
                    result[i] = FractalComposer._IRREGULAR_3PS[v]
                    continue
                # Regular conjugation
                if v.endswith(('sh', 'ch', 'x', 'z', 'ss')):
                    result[i] = v + 'es'
                elif v.endswith('y') and len(v) > 1 and v[-2] not in 'aeiou':
                    result[i] = v[:-1] + 'ies'
                else:
                    result[i] = v + 's'
        return result

    def _weighted_choice(self, candidates, weights):
        """Pick from candidates with weights."""
        if not candidates:
            return None
        total = sum(weights)
        if total <= 0:
            return candidates[0]
        r = self.rng.random() * total
        cumulative = 0.0
        for i, c in enumerate(candidates):
            cumulative += weights[i]
            if cumulative >= r:
                return c
        return candidates[-1]

    def index_wordlist(self, words: List[str]):
        """Bulk-index a word list into the force index."""
        for w in words:
            self.index.index_word(w)


# ================================================================
#  FACTORY: Build the composer from CK's existing dictionary
# ================================================================

def build_fractal_composer(semantic_lattice: dict = None,
                           enriched_words: List[str] = None,
                           rng: random.Random = None) -> FractalComposer:
    """Build a FractalComposer pre-loaded with CK's vocabulary.

    Indexes every word from the semantic lattice and enriched dictionary
    into force space. This is the "Matrix download" — all of English
    pre-shaped into navigable force geometry.
    """
    index = WordForceIndex()

    # Index words from semantic lattice (seed words).
    # The semantic lattice is keyed by OPERATOR: SEMANTIC_LATTICE[op_idx].
    # Words placed under an operator were chosen for their MEANING, not
    # their letter forces. We tag each word with its semantic operator
    # so find_by_force() can prefer MEANING-matched words over
    # phonetically-classified ones. This is the dual-lens fix:
    #   phonetic op = what the word SOUNDS like (D2 letter classification)
    #   semantic op = what the word MEANS (lattice placement by intent)
    if semantic_lattice:
        for op_idx, lenses in semantic_lattice.items():
            if not isinstance(lenses, dict):
                continue
            # Ensure op_idx is an integer for semantic tagging
            try:
                sem_op = int(op_idx)
            except (TypeError, ValueError):
                sem_op = -1
            for lens_name, phases in lenses.items():
                if not isinstance(phases, dict):
                    continue
                for phase_name, tiers in phases.items():
                    if not isinstance(tiers, dict):
                        continue
                    for tier_name, words in tiers.items():
                        if not isinstance(words, (list, tuple)):
                            continue
                        for w in words:
                            if isinstance(w, str) and len(w) >= 2:
                                # Only index individual words, not phrases
                                for part in w.split():
                                    if len(part) >= 2:
                                        index.index_word(part.lower(),
                                                         semantic_op=sem_op)

    # Index enriched words
    if enriched_words:
        for w in enriched_words:
            if isinstance(w, str) and len(w) >= 2:
                index.index_word(w.lower())

    # Index essential function words (the connective tissue of English).
    # These have real D2 force profiles -- they're physics, not filler.
    _FUNCTION_WORDS = [
        # articles / determiners (openers -- they frame what follows)
        'the', 'this', 'that', 'each', 'every', 'all', 'some', 'any',
        'no', 'what', 'which', 'whose',
        # pronouns (openers / receivers)
        'he', 'she', 'it', 'we', 'they', 'one', 'who',
        # prepositions (sustainers -- they connect)
        'in', 'on', 'of', 'to', 'for', 'by', 'at', 'from', 'with',
        'into', 'onto', 'upon', 'through', 'between', 'among',
        'within', 'without', 'beyond', 'before', 'after', 'above',
        'below', 'beneath', 'beside', 'toward', 'against', 'along',
        # conjunctions (sustainers)
        'and', 'but', 'or', 'yet', 'so', 'nor', 'while', 'when',
        'where', 'since', 'until', 'because', 'although', 'unless',
        # copula and auxiliaries (actors)
        'is', 'am', 'are', 'was', 'were', 'be', 'been', 'being',
        'has', 'have', 'had', 'does', 'did', 'do', 'will', 'would',
        'shall', 'should', 'may', 'might', 'can', 'could', 'must',
        # common verbs (actors)
        'moves', 'holds', 'gives', 'takes', 'comes', 'goes',
        'sees', 'knows', 'feels', 'makes', 'finds', 'keeps',
        'turns', 'grows', 'falls', 'rises', 'opens', 'closes',
        'breaks', 'builds', 'burns', 'flows', 'stands', 'runs',
        'speaks', 'breathes', 'reaches', 'becomes', 'remains',
        # adverbs (sustainers)
        'now', 'then', 'here', 'there', 'still', 'always', 'never',
        'ever', 'again', 'once', 'only', 'also', 'just', 'even',
        'already', 'soon', 'often', 'deeply', 'slowly', 'softly',
        # common adjectives (force-real: each has a D2 fingerprint)
        'deep', 'vast', 'bright', 'dark', 'still', 'true', 'whole',
        'pure', 'clear', 'raw', 'open', 'new', 'old', 'first', 'last',
        'strong', 'quiet', 'sharp', 'soft', 'cold', 'warm', 'wide',
        'thin', 'dense', 'slow', 'fast', 'high', 'low', 'full', 'free',
        'real', 'great', 'small', 'wild', 'calm', 'bold', 'fine',
    ]
    for w in _FUNCTION_WORDS:
        index.index_word(w)

    # Pass 2: calibrate roles using population z-scores
    index.calibrate_roles()

    return FractalComposer(index, rng=rng)
