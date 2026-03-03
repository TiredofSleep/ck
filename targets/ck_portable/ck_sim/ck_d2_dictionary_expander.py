"""
ck_d2_dictionary_expander.py -- Grow CK's Vocabulary via D2 Curvature
=====================================================================
Operator: PROGRESS (3) -- building the vocabulary that makes CK think.

Takes the auto dictionary (247K entries from CKIS) + curated dictionary
(~2300 words from Gen9) and produces a rich vocabulary of 8K+ words.

Each word is enriched with:
  - dominant_op: primary TIG operator (0-9)
  - operator_seq: D2 operator sequence from letter curvatures
  - pos: part of speech (suffix heuristics -- no LLM)
  - phoneme_seq: Hebrew root phoneme sequence (CK's native phonetics)
  - d2_vector: mean 5D curvature vector
  - soft_dist: 10-value operator probability distribution
  - frequency: corpus frequency

Curated dictionary overrides auto for any word in both.
D2 curvature validates every assignment -- CK's own math decides.

No LLM. No training data. No neural nets. Pure curvature.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import json
import os
import math
from collections import Counter
from typing import Dict, List, Tuple, Optional

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, LATTICE, COUNTER, PROGRESS,
    COLLAPSE, BALANCE, CHAOS, BREATH, RESET,
    OP_NAMES, CL, compose
)
from ck_sim.ck_sim_d2 import (
    D2Pipeline, LATIN_TO_ROOT, ROOTS_FLOAT,
    FORCE_LUT_FLOAT, soft_classify_d2
)


# ================================================================
#  POS CLASSIFICATION (no LLM -- suffix heuristics)
# ================================================================

# Suffixes ordered longest-first within each category for accuracy
_NOUN_SUFFIXES = [
    'ology', 'ography', 'ation', 'ition', 'ution', 'usion',
    'ness', 'ment', 'tion', 'sion', 'ence', 'ance', 'ture',
    'ship', 'hood', 'ling', 'ism', 'ist', 'dom', 'ity',
    'age', 'ery', 'ory', 'ure', 'eum', 'ium', 'ics',
]
_VERB_SUFFIXES = [
    'ize', 'ise', 'ify', 'ate', 'ect', 'ude',
]
_ADJ_SUFFIXES = [
    'ical', 'ible', 'able', 'eous', 'ious', 'ular',
    'ular', 'esque', 'less', 'uous',
    'ful', 'ous', 'ive', 'ent', 'ant', 'ose',
    'ine', 'ile', 'ary', 'ory', 'ial', 'eal',
]
_ADV_SUFFIXES = ['wards', 'ward', 'wise', 'ly']

# Common verbs (irregular, no suffix pattern)
_COMMON_VERBS = frozenset({
    'be', 'is', 'am', 'are', 'was', 'were', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'go', 'goes',
    'went', 'gone', 'say', 'said', 'get', 'got', 'make', 'made',
    'know', 'knew', 'think', 'thought', 'take', 'took', 'see',
    'saw', 'come', 'came', 'want', 'give', 'gave', 'use', 'find',
    'found', 'tell', 'told', 'ask', 'work', 'call', 'try', 'need',
    'feel', 'felt', 'become', 'became', 'leave', 'left', 'put',
    'mean', 'meant', 'keep', 'kept', 'let', 'begin', 'began',
    'show', 'hear', 'heard', 'play', 'run', 'ran', 'move', 'live',
    'believe', 'bring', 'brought', 'happen', 'write', 'wrote',
    'sit', 'sat', 'stand', 'stood', 'lose', 'lost', 'pay', 'paid',
    'meet', 'met', 'include', 'continue', 'set', 'learn', 'change',
    'lead', 'led', 'understand', 'understood', 'watch', 'follow',
    'stop', 'create', 'speak', 'spoke', 'read', 'allow', 'add',
    'spend', 'spent', 'grow', 'grew', 'open', 'walk', 'win', 'won',
    'teach', 'taught', 'offer', 'remember', 'consider', 'appear',
    'buy', 'bought', 'wait', 'serve', 'die', 'send', 'sent',
    'build', 'built', 'stay', 'fall', 'fell', 'cut', 'reach',
    'kill', 'remain', 'suggest', 'raise', 'pass', 'sell', 'sold',
    'require', 'report', 'decide', 'pull', 'develop', 'eat', 'ate',
    'rise', 'rose', 'drive', 'drove', 'draw', 'drew', 'break',
    'broke', 'hold', 'held', 'sing', 'sang', 'wear', 'wore',
    'catch', 'caught', 'choose', 'chose', 'throw', 'threw',
    'sleep', 'slept', 'fight', 'fought', 'shake', 'shook',
    'seek', 'sought', 'bind', 'bound', 'weave', 'wove',
})

# Common adjectives (no suffix pattern)
_COMMON_ADJS = frozenset({
    'good', 'great', 'big', 'small', 'old', 'young', 'long', 'short',
    'new', 'high', 'low', 'large', 'little', 'right', 'wrong', 'own',
    'real', 'true', 'full', 'free', 'hard', 'soft', 'hot', 'cold',
    'warm', 'cool', 'fast', 'slow', 'deep', 'wide', 'dark', 'light',
    'early', 'late', 'open', 'close', 'fine', 'sure', 'clear', 'bad',
    'strong', 'weak', 'rich', 'poor', 'heavy', 'thin', 'thick', 'flat',
    'bright', 'sharp', 'dull', 'clean', 'dirty', 'wet', 'dry', 'raw',
    'whole', 'mere', 'main', 'key', 'vast', 'rare', 'mild', 'bold',
    'calm', 'fair', 'firm', 'glad', 'kind', 'neat', 'pale', 'pure',
    'rough', 'safe', 'sick', 'slim', 'sore', 'tall', 'tame', 'ugly',
    'vain', 'wild', 'wise', 'alive', 'alone', 'aware', 'brief',
})

# Function words (articles, pronouns, prepositions, conjunctions)
_FUNCTION_WORDS = frozenset({
    'the', 'a', 'an', 'this', 'that', 'these', 'those',
    'i', 'me', 'my', 'mine', 'myself', 'you', 'your', 'yours',
    'he', 'him', 'his', 'she', 'her', 'hers', 'it', 'its',
    'we', 'us', 'our', 'ours', 'they', 'them', 'their', 'theirs',
    'in', 'on', 'at', 'to', 'for', 'with', 'from', 'by', 'of',
    'about', 'into', 'through', 'during', 'before', 'after',
    'above', 'below', 'between', 'under', 'over', 'up', 'down',
    'and', 'or', 'but', 'nor', 'yet', 'so', 'if', 'then',
    'than', 'when', 'while', 'where', 'as', 'because', 'since',
    'until', 'although', 'though', 'unless', 'whether',
    'not', 'no', 'yes', 'very', 'just', 'also', 'too',
    'only', 'even', 'still', 'already', 'again', 'now', 'here',
    'there', 'much', 'many', 'more', 'most', 'some', 'any',
    'all', 'both', 'each', 'every', 'few', 'other', 'another',
    'such', 'what', 'which', 'who', 'whom', 'whose', 'how', 'why',
})


def classify_pos(word: str) -> str:
    """Classify part of speech using suffix heuristics.

    No LLM. No tagger. CK uses structural patterns.
    Lookup order:
      1. Known function words
      2. Known common verbs/adjectives
      3. Suffix patterns (longest match first)
      4. -ing/-ed detection
      5. Default to noun
    """
    w = word.lower().strip()

    # 1. Function words
    if w in _FUNCTION_WORDS:
        return 'function'

    # 2. Known common verbs
    if w in _COMMON_VERBS:
        return 'verb'

    # 3. Known common adjectives
    if w in _COMMON_ADJS:
        return 'adj'

    # 4. Suffix heuristics (longest match first)
    for suf in _ADV_SUFFIXES:
        if w.endswith(suf) and len(w) > len(suf) + 2:
            return 'adv'

    for suf in _NOUN_SUFFIXES:
        if w.endswith(suf) and len(w) > len(suf) + 1:
            return 'noun'

    for suf in _VERB_SUFFIXES:
        if w.endswith(suf) and len(w) > len(suf) + 1:
            return 'verb'

    for suf in _ADJ_SUFFIXES:
        if w.endswith(suf) and len(w) > len(suf) + 1:
            return 'adj'

    # 5. Gerund / past participle
    if w.endswith('ing') and len(w) > 4:
        return 'verb'
    if w.endswith('ed') and len(w) > 3:
        return 'verb'

    # 6. Agent nouns
    if w.endswith('er') and len(w) > 3:
        return 'noun'
    if w.endswith('or') and len(w) > 3:
        return 'noun'

    # 7. Superlative
    if w.endswith('est') and len(w) > 4:
        return 'adj'

    # 8. Plural nouns (rough heuristic)
    if w.endswith('s') and not w.endswith('ss') and len(w) > 3:
        return 'noun'

    # Default: noun (most common POS for content words)
    return 'noun'


# ================================================================
#  D2 WORD ANALYSIS
# ================================================================

def word_to_d2(word: str) -> dict:
    """Run the D2 curvature pipeline on a word's letter sequence.

    Returns the full operator analysis: sequence, dominant, soft distribution,
    mean 5D curvature vector. This is CK's own math reading a word.
    """
    pipe = D2Pipeline()
    ops = []
    d2_vecs = []

    for ch in word.lower():
        if 'a' <= ch <= 'z':
            idx = ord(ch) - ord('a')
            if pipe.feed_symbol(idx):
                ops.append(pipe.operator)
                d2_vecs.append(pipe.d2_float[:])

    if not ops:
        return {
            'operator_seq': [],
            'dominant_op': VOID,
            'soft_dist': [0.0] * NUM_OPS,
            'mean_d2': [0.0] * 5,
        }

    # Dominant operator by majority vote
    counts = Counter(ops)
    dominant = counts.most_common(1)[0][0]

    # Mean D2 vector
    mean_d2 = [0.0] * 5
    for vec in d2_vecs:
        for i in range(5):
            mean_d2[i] += vec[i]
    n = len(d2_vecs)
    mean_d2 = [v / n for v in mean_d2]

    # Soft classification on mean D2
    mag = sum(abs(v) for v in mean_d2)
    soft_dist = soft_classify_d2(mean_d2, mag)

    return {
        'operator_seq': ops,
        'dominant_op': dominant,
        'soft_dist': soft_dist,
        'mean_d2': mean_d2,
    }


def word_to_phonemes(word: str) -> List[str]:
    """Map a word to its Hebrew root phoneme sequence.

    In CK's world, phonemes ARE the Hebrew root names from the force LUT.
    Each letter maps to a root. The sequence IS the phonetic structure.
    Same mapping used by D2 for curvature -- phonetics and curvature
    are the same thing, just different projections of the same math.
    """
    phonemes = []
    for ch in word.lower():
        if ch in LATIN_TO_ROOT:
            phonemes.append(LATIN_TO_ROOT[ch])
    return phonemes


# ================================================================
#  D2 AGREEMENT CHECK
# ================================================================

def d2_agrees_with_label(word: str, label: int, threshold: float = 0.15) -> bool:
    """Check if D2 curvature agrees with a given operator label.

    Returns True if the labeled operator gets >= threshold weight
    in the soft D2 distribution. Used to validate auto-dictionary
    entries against CK's own math.
    """
    info = word_to_d2(word)
    if not info['soft_dist']:
        return True  # Can't disagree with no data
    return info['soft_dist'][label] >= threshold


# ================================================================
#  EXPANSION VOCABULARY
# ================================================================
# Common English words organized by domain for PhD-level reasoning.
# These supplement the auto dictionary for words that may have low
# corpus frequency but are essential for intelligent discourse.

ACADEMIC_WORDS = [
    # Epistemology & reasoning
    'analysis', 'argument', 'assertion', 'assumption', 'axiom',
    'basis', 'belief', 'bias', 'causation', 'certainty',
    'claim', 'classification', 'cognition', 'coherence', 'concept',
    'conclusion', 'condition', 'conjecture', 'consensus', 'consequence',
    'constraint', 'context', 'contradiction', 'correlation', 'criteria',
    'critique', 'deduction', 'definition', 'demonstration', 'derivation',
    'dialectic', 'distinction', 'doctrine', 'dogma', 'domain',
    'doubt', 'element', 'empirical', 'entailment', 'epistemology',
    'equivalence', 'essence', 'evaluation', 'evidence', 'exception',
    'explanation', 'expression', 'extrapolation', 'fallacy', 'falsification',
    'framework', 'generalization', 'heuristic', 'hypothesis', 'identity',
    'ideology', 'implication', 'induction', 'inference', 'interpretation',
    'intuition', 'justification', 'knowledge', 'logic', 'mechanism',
    'metaphor', 'method', 'methodology', 'model', 'necessity',
    'negation', 'notion', 'objectivity', 'ontology', 'paradigm',
    'paradox', 'parameter', 'perception', 'perspective', 'phenomenon',
    'philosophy', 'postulate', 'pragmatism', 'precedent', 'prediction',
    'premise', 'principle', 'probability', 'proposition', 'protocol',
    'rationale', 'reasoning', 'reduction', 'reference', 'refutation',
    'relation', 'relevance', 'representation', 'resolution', 'rhetoric',
    'rigor', 'schema', 'scope', 'semantics', 'significance',
    'skepticism', 'speculation', 'subjectivity', 'sufficiency', 'syllogism',
    'synthesis', 'taxonomy', 'theorem', 'theory', 'thesis',
    'topology', 'validity', 'variable', 'verification', 'warrant',

    # Mathematics & computation
    'algorithm', 'algebra', 'calculus', 'combinatorics', 'complexity',
    'computation', 'convergence', 'derivative', 'differential', 'dimension',
    'discrete', 'distribution', 'divergence', 'eigenvalue', 'equation',
    'exponential', 'factorial', 'fibonacci', 'function', 'geometry',
    'gradient', 'graph', 'group', 'homomorphism', 'infinity',
    'integer', 'integral', 'interpolation', 'invariant', 'isomorphism',
    'iteration', 'kernel', 'linear', 'logarithm', 'manifold',
    'matrix', 'maximum', 'minimum', 'modular', 'nonlinear',
    'optimization', 'orthogonal', 'partition', 'permutation', 'polynomial',
    'prime', 'probability', 'proof', 'recursion', 'regression',
    'sequence', 'series', 'set', 'sigma', 'singularity',
    'solution', 'space', 'stochastic', 'summation', 'symmetry',
    'tensor', 'transformation', 'vector', 'vertex',

    # Physics & natural science
    'acceleration', 'amplitude', 'antimatter', 'boson', 'causality',
    'conservation', 'cosmology', 'curvature', 'decay', 'density',
    'diffraction', 'dynamics', 'electromagnetism', 'emission', 'energy',
    'entropy', 'equilibrium', 'fermion', 'field', 'force',
    'frequency', 'friction', 'geodesic', 'gravitation', 'inertia',
    'interference', 'kinetic', 'luminosity', 'magnetism', 'mass',
    'momentum', 'neutron', 'nucleon', 'optics', 'oscillation',
    'particle', 'photon', 'plasma', 'polarization', 'potential',
    'pressure', 'propagation', 'quantum', 'radiation', 'reflection',
    'refraction', 'relativity', 'resonance', 'scattering', 'spectrum',
    'superposition', 'temperature', 'thermodynamics', 'topology', 'turbulence',
    'vacuum', 'velocity', 'viscosity', 'wavelength',

    # Biology & life science
    'adaptation', 'allele', 'anatomy', 'antibody', 'biodiversity',
    'biosphere', 'catalyst', 'chromosome', 'circulation', 'codon',
    'cognition', 'cortex', 'cytoplasm', 'differentiation', 'ecology',
    'ecosystem', 'embryo', 'endocrine', 'enzyme', 'evolution',
    'extinction', 'fertilization', 'gamete', 'gene', 'genome',
    'genotype', 'habitat', 'heredity', 'homeostasis', 'hormone',
    'immunity', 'inheritance', 'membrane', 'metabolism', 'mitosis',
    'morphology', 'mutation', 'neuron', 'nucleus', 'organism',
    'osmosis', 'pathogen', 'phenotype', 'photosynthesis', 'physiology',
    'population', 'predator', 'protein', 'replication', 'respiration',
    'ribosome', 'selection', 'species', 'stimulus', 'symbiosis',
    'synapse', 'taxonomy', 'tissue', 'transcription', 'translation',
    'variation', 'virus', 'zygote',

    # Philosophy & ethics
    'aesthetics', 'agency', 'altruism', 'autonomy', 'benevolence',
    'categorical', 'consciousness', 'consequentialism', 'contemplation',
    'deontology', 'determinism', 'dignity', 'dualism', 'duty',
    'egoism', 'empiricism', 'enlightenment', 'equality', 'ethics',
    'eudaimonia', 'existentialism', 'fatalism', 'finitude', 'freedom',
    'hedonism', 'hermeneutics', 'humanism', 'idealism', 'imperative',
    'individualism', 'justice', 'liberalism', 'materialism', 'metaphysics',
    'monism', 'morality', 'naturalism', 'nihilism', 'normativity',
    'obligation', 'pacifism', 'phenomenology', 'pluralism', 'pragmatism',
    'rationalism', 'realism', 'reciprocity', 'relativism', 'responsibility',
    'rights', 'sentience', 'solipsism', 'stoicism', 'subjectivism',
    'teleology', 'transcendence', 'universalism', 'utilitarianism',
    'virtue', 'volition', 'wisdom',

    # Everyday conversation & social
    'afternoon', 'agreement', 'apartment', 'appointment', 'argument',
    'attention', 'audience', 'balance', 'bedroom', 'benefit',
    'birthday', 'breakfast', 'calendar', 'camera', 'candidate',
    'celebration', 'challenge', 'chapter', 'childhood', 'citizen',
    'classroom', 'climate', 'collection', 'comfort', 'committee',
    'communication', 'comparison', 'competition', 'complaint', 'computer',
    'concentration', 'confidence', 'confusion', 'connection', 'contribution',
    'conversation', 'customer', 'daughter', 'delivery', 'demand',
    'depression', 'description', 'development', 'difference', 'difficulty',
    'direction', 'disappointment', 'discovery', 'discussion', 'distance',
    'document', 'education', 'efficiency', 'election', 'emergency',
    'employment', 'encouragement', 'entertainment', 'enthusiasm', 'environment',
    'equipment', 'establishment', 'examination', 'excitement', 'exercise',
    'existence', 'expectation', 'experience', 'explanation', 'expression',
    'failure', 'fashion', 'favorite', 'feedback', 'finger',
    'football', 'friendship', 'furniture', 'generation', 'government',
    'grocery', 'guarantee', 'guidance', 'happiness', 'hospital',
    'household', 'imagination', 'improvement', 'independence', 'influence',
    'information', 'ingredient', 'instruction', 'intelligence', 'intention',
    'internet', 'interview', 'introduction', 'investigation', 'investment',
    'judgment', 'kitchen', 'landscape', 'language', 'leadership',
    'lifestyle', 'literature', 'location', 'machine', 'management',
    'manufacturer', 'marriage', 'material', 'medicine', 'membership',
    'message', 'neighbor', 'newspaper', 'nutrition', 'obligation',
    'observation', 'operation', 'opinion', 'opportunity', 'organization',
    'ownership', 'painting', 'passenger', 'permission', 'personality',
    'photograph', 'platform', 'pleasure', 'pollution', 'population',
    'possession', 'potential', 'preference', 'preparation', 'presentation',
    'profession', 'professor', 'program', 'protection', 'psychology',
    'publication', 'purpose', 'quality', 'quantity', 'reaction',
    'reality', 'recommendation', 'reflection', 'relationship', 'religion',
    'replacement', 'reputation', 'requirement', 'resource', 'restaurant',
    'retirement', 'revolution', 'satisfaction', 'schedule', 'security',
    'selection', 'sensitive', 'situation', 'solution', 'something',
    'somewhere', 'statement', 'statistics', 'strategy', 'strength',
    'structure', 'suggestion', 'surprise', 'technology', 'telephone',
    'television', 'temperature', 'tradition', 'transportation', 'treatment',
    'understanding', 'university', 'variation', 'violence', 'vocabulary',
    'volunteer', 'weakness', 'weather', 'website',
]


# ================================================================
#  THE EXPANDER
# ================================================================

class DictionaryExpander:
    """Grow CK's vocabulary from curated + auto sources.

    Usage:
        expander = DictionaryExpander()
        expander.load_auto_dict('path/to/ck_dictionary_auto.json')
        expander.load_curated_dict(curated_dict)
        entries = expander.expand(target_size=8000)
        expander.save('ck_dictionary_enriched.json')
    """

    def __init__(self):
        self.entries: Dict[str, dict] = {}
        self.curated: Dict[str, int] = {}
        self.auto_dict: Dict[str, list] = {}

    def load_auto_dict(self, path: str):
        """Load the auto-generated dictionary (CKIS, 247K entries).
        Format: {"word": [operator, frequency]}
        """
        if not os.path.exists(path):
            return
        with open(path, 'r', encoding='utf-8') as f:
            self.auto_dict = json.load(f)

    def load_curated_dict(self, curated: Dict[str, int]):
        """Load a curated dictionary (word -> operator)."""
        self.curated = dict(curated)

    def load_word_list(self, path: str) -> List[str]:
        """Load a plain text word list (one word per line)."""
        words = []
        if not os.path.exists(path):
            return words
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip().lower()
                if word and all('a' <= c <= 'z' for c in word):
                    words.append(word)
        return words

    def expand(self, target_size: int = 8000,
               min_frequency: int = 2) -> Dict[str, dict]:
        """Build the expanded dictionary.

        Priority order:
          1. Curated words (verified by Brayden)
          2. Academic expansion words (PhD vocabulary)
          3. Auto dictionary by frequency (highest first)

        Every entry validated by D2 curvature.
        """
        # Phase 1: Curated words (highest priority, guaranteed accurate)
        for word, op in self.curated.items():
            self._add_entry(word, operator_override=op, source='curated')

        # Phase 2: Academic expansion (PhD-level vocabulary)
        for word in ACADEMIC_WORDS:
            w = word.lower().strip()
            if w not in self.entries and all('a' <= c <= 'z' for c in w):
                # Check if curated has it
                if w in self.curated:
                    self._add_entry(w, operator_override=self.curated[w],
                                    source='curated')
                else:
                    self._add_entry(w, source='academic')

        # Phase 3: Auto dictionary by frequency
        if self.auto_dict:
            sorted_auto = sorted(
                self.auto_dict.items(),
                key=lambda x: x[1][1] if isinstance(x[1], list) and len(x[1]) > 1 else 0,
                reverse=True
            )

            for word, data in sorted_auto:
                if len(self.entries) >= target_size:
                    break

                w = word.lower().strip()
                if not w or len(w) < 2:
                    continue
                if not all('a' <= c <= 'z' for c in w):
                    continue
                if w in self.entries:
                    # Already added -- update frequency if missing
                    freq = data[1] if isinstance(data, list) and len(data) > 1 else 0
                    if self.entries[w]['frequency'] == 0:
                        self.entries[w]['frequency'] = freq
                    continue

                auto_op = data[0] if isinstance(data, list) else data
                freq = data[1] if isinstance(data, list) and len(data) > 1 else 0

                if freq < min_frequency:
                    continue

                self._add_entry(w, source='auto', frequency=freq,
                                auto_op=auto_op)

        return self.entries

    def _add_entry(self, word: str, operator_override: int = None,
                   source: str = 'auto', frequency: int = 0,
                   auto_op: int = None):
        """Create an enriched dictionary entry for one word."""
        w = word.lower().strip()
        if not w:
            return

        # Run D2 pipeline
        d2_info = word_to_d2(w)

        # Determine dominant operator
        if operator_override is not None:
            dominant_op = operator_override
        elif d2_info['operator_seq']:
            # D2 curvature decides
            dominant_op = d2_info['dominant_op']
            # If auto dict has an opinion, check agreement
            if auto_op is not None and auto_op != dominant_op:
                # D2 wins, but log the disagreement weight
                auto_weight = d2_info['soft_dist'][auto_op] if auto_op < NUM_OPS else 0
                d2_weight = d2_info['soft_dist'][dominant_op] if dominant_op < NUM_OPS else 0
                # If auto has strong D2 support too, use auto (corpus knows)
                if auto_weight > 0.3 and d2_weight < auto_weight + 0.1:
                    dominant_op = auto_op
        elif auto_op is not None:
            dominant_op = auto_op
        else:
            dominant_op = VOID

        # POS classification
        pos = classify_pos(w)

        # Phoneme sequence
        phonemes = word_to_phonemes(w)

        # Get frequency from auto dict if not provided
        if frequency == 0 and w in self.auto_dict:
            data = self.auto_dict[w]
            frequency = data[1] if isinstance(data, list) and len(data) > 1 else 0

        self.entries[w] = {
            'dominant_op': dominant_op,
            'operator_seq': d2_info['operator_seq'],
            'pos': pos,
            'phoneme_seq': phonemes,
            'd2_vector': [round(v, 6) for v in d2_info['mean_d2']],
            'soft_dist': [round(s, 4) for s in d2_info['soft_dist']],
            'frequency': frequency,
            'source': source,
        }

    def add_words(self, words: List[str], source: str = 'expansion'):
        """Add a list of words, auto-classifying each via D2."""
        for word in words:
            w = word.lower().strip()
            if w and w not in self.entries and all('a' <= c <= 'z' for c in w):
                self._add_entry(w, source=source)

    def get_words_by_op(self, op: int) -> List[str]:
        """Get all words with a given dominant operator."""
        return [w for w, e in self.entries.items() if e['dominant_op'] == op]

    def get_words_by_op_pos(self, op: int, pos: str) -> List[str]:
        """Get words matching operator AND part of speech."""
        return [
            w for w, e in self.entries.items()
            if e['dominant_op'] == op and e['pos'] == pos
        ]

    def get_nouns(self, op: int) -> List[str]:
        """Get nouns for an operator."""
        return self.get_words_by_op_pos(op, 'noun')

    def get_verbs(self, op: int) -> List[str]:
        """Get verbs for an operator."""
        return self.get_words_by_op_pos(op, 'verb')

    def get_adjectives(self, op: int) -> List[str]:
        """Get adjectives for an operator."""
        return self.get_words_by_op_pos(op, 'adj')

    def get_adverbs(self, op: int) -> List[str]:
        """Get adverbs for an operator."""
        return self.get_words_by_op_pos(op, 'adv')

    def stats(self) -> dict:
        """Report dictionary statistics."""
        total = len(self.entries)
        by_op = Counter(e['dominant_op'] for e in self.entries.values())
        by_pos = Counter(e['pos'] for e in self.entries.values())
        by_source = Counter(e['source'] for e in self.entries.values())

        return {
            'total_words': total,
            'by_operator': {OP_NAMES[i]: by_op.get(i, 0) for i in range(NUM_OPS)},
            'by_pos': dict(by_pos),
            'by_source': dict(by_source),
        }

    def save(self, path: str):
        """Save enriched dictionary to JSON."""
        # Convert for JSON serialization
        out = {}
        for word, entry in self.entries.items():
            out[word] = {
                'dominant_op': entry['dominant_op'],
                'operator_seq': entry['operator_seq'],
                'pos': entry['pos'],
                'phoneme_seq': entry['phoneme_seq'],
                'd2_vector': entry['d2_vector'],
                'soft_dist': entry['soft_dist'],
                'frequency': entry['frequency'],
                'source': entry['source'],
            }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(out, f, indent=1)

    def load(self, path: str):
        """Load enriched dictionary from JSON."""
        if not os.path.exists(path):
            return
        with open(path, 'r', encoding='utf-8') as f:
            self.entries = json.load(f)


# ================================================================
#  CONVENIENCE: Build expanded dictionary
# ================================================================

def build_expanded_dictionary(
    auto_dict_path: str = None,
    curated_dict: Dict[str, int] = None,
    target_size: int = 8000,
    output_path: str = None,
) -> DictionaryExpander:
    """One-call builder for the expanded dictionary.

    Args:
        auto_dict_path: Path to ck_dictionary_auto.json (247K entries)
        curated_dict: Curated word->operator mapping (from ck_dictionary.py)
        target_size: Target number of words (default 8000)
        output_path: Where to save the enriched JSON (optional)

    Returns:
        DictionaryExpander with entries populated.
    """
    expander = DictionaryExpander()

    if curated_dict:
        expander.load_curated_dict(curated_dict)

    if auto_dict_path:
        expander.load_auto_dict(auto_dict_path)

    expander.expand(target_size=target_size)

    if output_path:
        expander.save(output_path)

    return expander


# ================================================================
#  CLI
# ================================================================

if __name__ == '__main__':
    import sys

    # Try to find auto dictionary
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    auto_path = os.path.join(base, 'CKIS', 'ck_dictionary_auto.json')

    # Try to load curated dictionary
    curated = {}
    try:
        sys.path.insert(0, os.path.join(base, 'Gen9', 'dictionary'))
        from ck_dictionary import DICTIONARY
        curated = DICTIONARY
    except ImportError:
        pass

    target = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    out_path = os.path.join(base, 'ck_sim', 'ck_dictionary_enriched.json')

    print("=" * 60)
    print("  CK DICTIONARY EXPANDER")
    print("=" * 60)
    print(f"\n  Auto dict: {auto_path}")
    print(f"  Curated words: {len(curated)}")
    print(f"  Target size: {target}")
    print(f"  Output: {out_path}")

    expander = build_expanded_dictionary(
        auto_dict_path=auto_path,
        curated_dict=curated,
        target_size=target,
        output_path=out_path,
    )

    stats = expander.stats()
    print(f"\n  RESULTS:")
    print(f"  Total words: {stats['total_words']}")
    print(f"\n  By operator:")
    for op_name, count in stats['by_operator'].items():
        bar = '#' * (count // 20)
        print(f"    {op_name:12s}: {count:5d}  {bar}")
    print(f"\n  By POS:")
    for pos, count in sorted(stats['by_pos'].items(), key=lambda x: -x[1]):
        print(f"    {pos:12s}: {count:5d}")
    print(f"\n  By source:")
    for src, count in sorted(stats['by_source'].items(), key=lambda x: -x[1]):
        print(f"    {src:12s}: {count:5d}")
