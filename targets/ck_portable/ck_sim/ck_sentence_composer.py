"""
ck_sentence_composer.py -- CK Composes English From Operators
=============================================================
Operator: HARMONY (7) -- composing meaning from curvature.

The sentence composer turns CK's operator chains into grammatical
English. No LLM. No grammar model. No training data.

Architecture:
  1. OPERATOR GRAMMAR GRAPH - CL table defines which operator
     transitions are valid. This REPLACES English syntax.
  2. CLAUSE COMPOSER - subject/verb/object from operator word pools.
     Each slot filled by a word whose operator matches the chain.
  3. SENTENCE PLANNER - multi-sentence composition from operator arcs.
     Rising arc = build complexity. Falling = wind down. Stable = sustain.
  4. CK TALK LOOP - idea → operators → grammar → curvature check → speak.

The key insight: operator transitions ARE grammar.
  CL[LATTICE][PROGRESS] = HARMONY → "structure grows" is valid
  CL[VOID][VOID] = VOID → "nothing nothing" is incoherent

Paper 4: "D2 → Operators → Semantic Lattice → English sentence."

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import random
import math
from collections import Counter, deque
from typing import Dict, List, Tuple, Optional

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, LATTICE, COUNTER, PROGRESS,
    COLLAPSE, BALANCE, CHAOS, BREATH, RESET,
    OP_NAMES, CL, compose
)
from ck_sim.ck_sim_d2 import D2Pipeline, soft_classify_d2


# ================================================================
#  OPERATOR GRAMMAR GRAPH
# ================================================================
# The CL table IS the grammar. If CL[A][B] = HARMONY, the
# transition A→B is grammatically harmonious. Other results are
# still valid but carry different weight/meaning.
#
# Edge weight = how "grammatically smooth" the transition is.
# HARMONY result = 1.0, non-VOID non-HARMONY = 0.5, VOID = 0.1

class OperatorGrammarGraph:
    """Grammar graph built from the CL composition table.

    Nodes = operators (0-9)
    Edges = (from_op, to_op) with weight from CL composition
    Weight = smoothness of the transition in English.

    This replaces syntax rules. Operator algebra IS the grammar.
    """

    def __init__(self):
        # Build adjacency matrix from CL table
        self.weights = [[0.0] * NUM_OPS for _ in range(NUM_OPS)]
        self._build()

    def _build(self):
        """Compute transition weights from CL table."""
        for a in range(NUM_OPS):
            for b in range(NUM_OPS):
                result = CL[a][b]
                if result == HARMONY:
                    self.weights[a][b] = 1.0
                elif result == VOID:
                    self.weights[a][b] = 0.1
                else:
                    # Non-trivial composition -- interesting but not smooth
                    self.weights[a][b] = 0.6

    def transition_weight(self, from_op: int, to_op: int) -> float:
        """How grammatically smooth is from_op → to_op?"""
        if 0 <= from_op < NUM_OPS and 0 <= to_op < NUM_OPS:
            return self.weights[from_op][to_op]
        return 0.0

    def best_next(self, current_op: int, n: int = 3) -> List[Tuple[int, float]]:
        """Top n next operators by grammar weight from current."""
        if current_op < 0 or current_op >= NUM_OPS:
            return [(HARMONY, 1.0)]
        candidates = [
            (op, self.weights[current_op][op])
            for op in range(NUM_OPS)
        ]
        candidates.sort(key=lambda x: -x[1])
        return candidates[:n]

    def chain_coherence(self, ops: List[int]) -> float:
        """Grammatical coherence of an operator chain.
        Average transition weight across adjacent pairs.
        Higher = more grammatically smooth.
        """
        if len(ops) < 2:
            return 1.0
        total = sum(
            self.weights[ops[i]][ops[i + 1]]
            for i in range(len(ops) - 1)
        )
        return total / (len(ops) - 1)

    def cl_fuse(self, ops: List[int]) -> int:
        """CL-fuse an operator chain to a single operator."""
        if not ops:
            return VOID
        result = ops[0]
        for op in ops[1:]:
            result = compose(result, op)
        return result


# Singleton grammar graph
GRAMMAR = OperatorGrammarGraph()


# ================================================================
#  OPERATOR → POS ROLE MAPPING
# ================================================================
# Which operators naturally fill which grammatical roles.
# This is the bridge between operator algebra and English POS.

# Operators that naturally serve as subjects (entities, things)
SUBJECT_OPS = {LATTICE, COUNTER, HARMONY, BREATH, RESET}

# Operators that naturally serve as verbs (actions, processes)
VERB_OPS = {PROGRESS, COLLAPSE, BALANCE, CHAOS, BREATH, RESET}

# Operators that naturally serve as objects (targets, results)
OBJECT_OPS = {VOID, LATTICE, COUNTER, HARMONY, PROGRESS, COLLAPSE}

# Operators that naturally serve as modifiers (qualities)
MODIFIER_OPS = {VOID, BALANCE, CHAOS, HARMONY, BREATH}


# ================================================================
#  CLAUSE COMPOSER
# ================================================================

class ClauseComposer:
    """Builds grammatical English clauses from operator chains.

    Uses an enriched dictionary (from DictionaryExpander) to pick
    words whose operators match the chain. Falls back to a built-in
    minimal vocabulary if no dictionary is loaded.

    Rules:
      subject = noun_phrase(subject_op)
      verb    = action_word(verb_op)
      object  = noun_phrase(object_op)
      mods    = modifier_words(mod_ops)
    """

    def __init__(self, dictionary: Dict[str, dict] = None, seed: int = None):
        self.rng = random.Random(seed)
        self.dict = dictionary or {}
        self._recent_words = deque(maxlen=30)  # Anti-repetition
        # Index words by (op, pos) for fast lookup
        self._index: Dict[Tuple[int, str], List[str]] = {}
        self._build_index()

    def _build_index(self):
        """Index dictionary by (operator, POS)."""
        self._index.clear()
        for word, entry in self.dict.items():
            op = entry.get('dominant_op', 0)
            pos = entry.get('pos', 'noun')
            key = (op, pos)
            if key not in self._index:
                self._index[key] = []
            self._index[key].append(word)

        # Also build a fallback: words by op regardless of POS
        for op in range(NUM_OPS):
            key_all = (op, '_all')
            words = []
            for pos in ['noun', 'verb', 'adj', 'adv', 'function']:
                words.extend(self._index.get((op, pos), []))
            self._index[key_all] = words

    def load_dictionary(self, dictionary: Dict[str, dict]):
        """Load or replace the dictionary."""
        self.dict = dictionary
        self._build_index()

    def _pick(self, op: int, pos: str, n: int = 1) -> List[str]:
        """Pick n words matching operator and POS, avoiding repeats."""
        candidates = self._index.get((op, pos), [])
        if not candidates:
            candidates = self._index.get((op, '_all'), [])
        if not candidates:
            # Last resort: any word for this op from fallback vocab
            candidates = list(_FALLBACK_VOCAB.get(op, {}).get(pos, []))
            if not candidates:
                candidates = list(_FALLBACK_VOCAB.get(op, {}).get('noun', ['something']))

        # Filter out recently used words
        fresh = [w for w in candidates if w not in self._recent_words]
        if not fresh:
            fresh = candidates  # Allow repeats if all used recently

        picks = []
        pool = list(fresh)
        for _ in range(min(n, len(pool))):
            word = self.rng.choice(pool)
            picks.append(word)
            pool.remove(word)
            self._recent_words.append(word)
        return picks

    def noun_phrase(self, op: int, with_article: bool = True,
                    with_adj: bool = False, adj_op: int = None) -> str:
        """Generate a noun phrase from an operator.

        Example: op=LATTICE → "the structure"
                 op=LATTICE, with_adj=True, adj_op=HARMONY → "the beautiful structure"
        """
        noun = self._pick(op, 'noun')[0] if self._pick(op, 'noun') else 'thing'

        parts = []
        if with_article:
            # Deterministic article choice
            if noun[0] in 'aeiou':
                parts.append('an')
            else:
                parts.append('the')

        if with_adj and adj_op is not None:
            adjs = self._pick(adj_op, 'adj')
            if adjs:
                parts.append(adjs[0])

        parts.append(noun)
        return ' '.join(parts)

    def verb_phrase(self, op: int, tense: str = 'present') -> str:
        """Generate a verb from an operator.

        tense: 'present', 'past', 'gerund'
        """
        verbs = self._pick(op, 'verb')
        if not verbs:
            return 'is'  # Safest fallback
        verb = verbs[0]

        # Very simple tense handling (no morphology engine)
        if tense == 'gerund' and not verb.endswith('ing'):
            if verb.endswith('e'):
                verb = verb[:-1] + 'ing'
            else:
                verb = verb + 'ing'
        elif tense == 'past' and not verb.endswith('ed'):
            if verb.endswith('e'):
                verb = verb + 'd'
            else:
                verb = verb + 'ed'
        return verb

    def modifier(self, op: int, pos: str = 'adj') -> str:
        """Generate a modifier (adjective or adverb)."""
        words = self._pick(op, pos)
        if words:
            return words[0]
        # Fallback
        words = self._pick(op, 'adj')
        return words[0] if words else 'coherent'

    def compose_clause(self, subject_op: int, verb_op: int,
                       object_op: int = None,
                       mod_op: int = None) -> str:
        """Compose a single clause: [mod] subject verb [object].

        Example:
          subject_op=LATTICE, verb_op=PROGRESS, object_op=HARMONY
          → "the structure builds harmony"
        """
        parts = []

        # Optional modifier
        if mod_op is not None:
            parts.append(self.modifier(mod_op))

        # Subject
        parts.append(self.noun_phrase(subject_op, with_article=True))

        # Verb
        parts.append(self.verb_phrase(verb_op))

        # Optional object
        if object_op is not None:
            parts.append(self.noun_phrase(object_op, with_article=True))

        clause = ' '.join(parts)
        # Capitalize first letter
        if clause:
            clause = clause[0].upper() + clause[1:]
        return clause

    def compose_from_chain(self, ops: List[int]) -> str:
        """Compose a sentence from an operator chain.

        Analyzes the chain to extract subject/verb/object roles,
        then builds a grammatical clause.
        """
        if not ops:
            return "Silence."

        if len(ops) == 1:
            return self.noun_phrase(ops[0], with_article=False).capitalize() + '.'

        # Extract roles from operator chain
        counts = Counter(ops)
        dominant = counts.most_common(1)[0][0]

        # Find subject: first entity-like operator
        subject_op = dominant
        for op in ops:
            if op in SUBJECT_OPS:
                subject_op = op
                break

        # Find verb: first action-like operator
        verb_op = PROGRESS  # default
        for op in ops:
            if op in VERB_OPS and op != subject_op:
                verb_op = op
                break

        # Find object: last entity-like operator different from subject
        object_op = None
        for op in reversed(ops):
            if op in OBJECT_OPS and op != subject_op:
                object_op = op
                break

        # Find modifier: any balance/chaos/harmony that isn't used
        mod_op = None
        for op in ops:
            if op in MODIFIER_OPS and op not in (subject_op, verb_op, object_op):
                mod_op = op
                break

        return self.compose_clause(subject_op, verb_op, object_op, mod_op) + '.'


# ================================================================
#  SENTENCE PLANNER
# ================================================================

class SentencePlanner:
    """Plans multi-sentence utterances from operator chain arcs.

    Analyzes the shape of the operator chain:
      - Rising arc (low → high coherence) → build complexity
      - Falling arc (high → low) → wind down
      - Stable arc → sustained reasoning
      - Mixed → address each phase

    Then generates a coherent multi-sentence response.
    """

    def __init__(self, composer: ClauseComposer = None, seed: int = None):
        self.composer = composer or ClauseComposer(seed=seed)
        self.rng = random.Random(seed)

    def _analyze_arc(self, ops: List[int]) -> str:
        """Classify the operator chain's arc shape."""
        if len(ops) < 3:
            return 'short'

        # Split into halves and compare coherence
        mid = len(ops) // 2
        first_half = ops[:mid]
        second_half = ops[mid:]

        # Coherence = harmony fraction
        h1 = sum(1 for o in first_half if o == HARMONY) / len(first_half)
        h2 = sum(1 for o in second_half if o == HARMONY) / len(second_half)

        if h2 > h1 + 0.15:
            return 'rising'
        elif h1 > h2 + 0.15:
            return 'falling'
        elif h1 > 0.5 and h2 > 0.5:
            return 'stable_high'
        elif h1 < 0.3 and h2 < 0.3:
            return 'stable_low'
        return 'mixed'

    def _segment_chain(self, ops: List[int], max_segment: int = 5) -> List[List[int]]:
        """Break an operator chain into clause-sized segments.

        Each segment becomes one sentence. Split at operator transitions
        that have low CL weight (natural clause boundaries).
        """
        if len(ops) <= max_segment:
            return [ops]

        segments = []
        current = [ops[0]]

        for i in range(1, len(ops)):
            weight = GRAMMAR.transition_weight(ops[i - 1], ops[i])
            if len(current) >= max_segment or (len(current) >= 3 and weight < 0.5):
                segments.append(current)
                current = [ops[i]]
            else:
                current.append(ops[i])

        if current:
            segments.append(current)

        return segments

    def plan(self, ops: List[int], max_sentences: int = 4) -> str:
        """Plan and generate a multi-sentence utterance.

        Args:
            ops: operator chain from CK's brain
            max_sentences: maximum sentences to generate

        Returns:
            Grammatical English text.
        """
        if not ops:
            return "I am quiet."

        arc = self._analyze_arc(ops)
        segments = self._segment_chain(ops)[:max_sentences]

        sentences = []
        for seg in segments:
            sentence = self.composer.compose_from_chain(seg)
            sentences.append(sentence)

        text = ' '.join(sentences)

        # Add arc-appropriate framing
        if arc == 'rising' and len(sentences) > 1:
            text += ' Something is building.'
        elif arc == 'falling' and len(sentences) > 1:
            text += ' Things are settling now.'

        return text

    def compose_explanation(self, topic_ops: List[int],
                            detail_ops: List[int] = None,
                            max_sentences: int = 3) -> str:
        """Compose an explanation of a topic from its operator signature.

        Used when CK retrieves knowledge and needs to express it.

        Args:
            topic_ops: operator chain representing the topic
            detail_ops: additional operators for supporting detail
            max_sentences: max output sentences
        """
        if not topic_ops:
            return "I do not have enough information."

        # First sentence: state the topic
        topic_sentence = self.composer.compose_from_chain(topic_ops)

        sentences = [topic_sentence]

        # Second sentence: elaborate with detail operators
        if detail_ops and len(sentences) < max_sentences:
            detail_sentence = self.composer.compose_from_chain(detail_ops)
            sentences.append(detail_sentence)

        # Third sentence: synthesize (CL-fuse topic + detail)
        if detail_ops and len(sentences) < max_sentences:
            combined = topic_ops + detail_ops
            fused = GRAMMAR.cl_fuse(combined)
            # Generate a concluding sentence from the fused operator
            conclusion_ops = [fused, HARMONY]
            conclusion = self.composer.compose_from_chain(conclusion_ops)
            sentences.append(conclusion)

        return ' '.join(sentences)

    def respond_to_text(self, input_text: str,
                        engine_ops: List[int] = None,
                        max_sentences: int = 3) -> str:
        """Generate a response to input text.

        Runs D2 on the input to get its operator signature,
        then composes a response that addresses those operators.

        Args:
            input_text: what was said to CK
            engine_ops: CK's current internal operator chain
            max_sentences: max output sentences
        """
        # D2 on input text
        input_ops = text_to_operator_chain(input_text)

        # Combine with engine state
        if engine_ops:
            response_ops = input_ops + engine_ops
        else:
            response_ops = input_ops

        if not response_ops:
            return "I hear you."

        return self.plan(response_ops, max_sentences)


# ================================================================
#  TEXT → OPERATOR CHAIN (D2 analysis)
# ================================================================

def text_to_operator_chain(text: str) -> List[int]:
    """Convert text to an operator chain via D2 curvature.

    Each letter triplet produces one D2 sample → one operator.
    This is how CK "reads" -- through curvature, not tokens.
    """
    pipe = D2Pipeline()
    ops = []
    for ch in text.lower():
        if 'a' <= ch <= 'z':
            idx = ord(ch) - ord('a')
            if pipe.feed_symbol(idx):
                ops.append(pipe.operator)
    return ops


def text_operator_distribution(text: str) -> List[float]:
    """Get the 10-value operator distribution for a text.

    Returns normalized histogram of operators from D2 analysis.
    Used for matching and comparison.
    """
    ops = text_to_operator_chain(text)
    if not ops:
        return [0.0] * NUM_OPS

    dist = [0.0] * NUM_OPS
    for op in ops:
        dist[op] += 1.0
    total = sum(dist)
    if total > 0:
        dist = [d / total for d in dist]
    return dist


# ================================================================
#  CURVATURE COHERENCE CHECK
# ================================================================

def curvature_check(sentence: str, min_coherence: float = 0.3) -> Tuple[bool, float]:
    """Check if a composed sentence maintains curvature coherence.

    Runs D2 on the generated text and measures the coherence
    of its operator chain against the CL table.

    Returns: (passes, coherence_score)
    """
    ops = text_to_operator_chain(sentence)
    if len(ops) < 2:
        return True, 1.0

    coherence = GRAMMAR.chain_coherence(ops)
    return coherence >= min_coherence, coherence


# ================================================================
#  CK TALK LOOP
# ================================================================

class CKTalkLoop:
    """CK's speech generation pipeline.

    idea → operator chain → grammar composer → curvature check → speak

    No neural nets. No training. All math.
    """

    def __init__(self, dictionary: Dict[str, dict] = None, seed: int = None):
        self.composer = ClauseComposer(dictionary=dictionary, seed=seed)
        self.planner = SentencePlanner(composer=self.composer, seed=seed)
        self._utterance_history = deque(maxlen=50)
        self._retry_limit = 3

    def speak(self, operator_chain: List[int],
              max_sentences: int = 3) -> str:
        """Generate English from an operator chain.

        The full pipeline:
          1. Plan sentence structure from operator arc
          2. Compose clauses using grammar graph
          3. Curvature check -- verify coherence of output
          4. If incoherent, retry with alternative phrasing
          5. Record utterance in history
        """
        for attempt in range(self._retry_limit):
            text = self.planner.plan(operator_chain, max_sentences)

            # Curvature check
            passes, coherence = curvature_check(text)
            if passes:
                self._utterance_history.append(text)
                return text

            # Shuffle operators slightly for retry
            chain = list(operator_chain)
            if len(chain) > 2:
                idx = random.randint(0, len(chain) - 2)
                chain[idx], chain[idx + 1] = chain[idx + 1], chain[idx]
            operator_chain = chain

        # Accept best attempt if all retries fail
        text = self.planner.plan(operator_chain, max_sentences)
        self._utterance_history.append(text)
        return text

    def respond(self, input_text: str,
                engine_ops: List[int] = None,
                max_sentences: int = 3) -> str:
        """Respond to text input.

        Combines input D2 analysis with CK's internal state,
        then generates a response.
        """
        input_ops = text_to_operator_chain(input_text)

        if engine_ops:
            combined = input_ops + engine_ops
        else:
            combined = input_ops

        if not combined:
            return "I hear you."

        return self.speak(combined, max_sentences)

    def explain(self, topic_text: str,
                detail_text: str = None,
                max_sentences: int = 3) -> str:
        """Explain a topic retrieved from the knowledge library.

        Converts topic text to operators, then composes an explanation.
        """
        topic_ops = text_to_operator_chain(topic_text)
        detail_ops = text_to_operator_chain(detail_text) if detail_text else None

        return self.planner.compose_explanation(
            topic_ops, detail_ops, max_sentences)

    @property
    def history(self) -> List[str]:
        """Recent utterance history."""
        return list(self._utterance_history)


# ================================================================
#  FALLBACK VOCABULARY
# ================================================================
# Minimal vocabulary for when no enriched dictionary is loaded.
# Organized by operator and POS. Enough for basic speech.

_FALLBACK_VOCAB = {
    VOID: {
        'noun': ['silence', 'emptiness', 'void', 'shadow', 'darkness', 'absence', 'space', 'nothing'],
        'verb': ['vanish', 'fade', 'disappear', 'erase', 'forget', 'dissolve', 'hide'],
        'adj':  ['empty', 'silent', 'dark', 'absent', 'hollow', 'blank', 'hidden', 'unknown'],
        'adv':  ['silently', 'barely', 'hardly', 'faintly'],
    },
    LATTICE: {
        'noun': ['structure', 'pattern', 'framework', 'lattice', 'foundation', 'system', 'network', 'order', 'form'],
        'verb': ['organize', 'arrange', 'build', 'connect', 'link', 'anchor', 'support', 'frame'],
        'adj':  ['structured', 'ordered', 'organized', 'stable', 'grounded', 'solid', 'systematic'],
        'adv':  ['firmly', 'steadily', 'systematically'],
    },
    COUNTER: {
        'noun': ['measure', 'observation', 'analysis', 'comparison', 'question', 'difference', 'count', 'test'],
        'verb': ['measure', 'compare', 'observe', 'analyze', 'examine', 'assess', 'notice', 'count'],
        'adj':  ['different', 'curious', 'distinct', 'precise', 'measured', 'observed', 'analytical'],
        'adv':  ['carefully', 'precisely', 'curiously', 'distinctly'],
    },
    PROGRESS: {
        'noun': ['growth', 'progress', 'creation', 'advance', 'development', 'evolution', 'momentum', 'journey'],
        'verb': ['grow', 'build', 'advance', 'create', 'develop', 'expand', 'improve', 'learn', 'discover'],
        'adj':  ['growing', 'advancing', 'creative', 'forward', 'rising', 'dynamic', 'productive'],
        'adv':  ['forward', 'steadily', 'rapidly', 'actively'],
    },
    COLLAPSE: {
        'noun': ['ending', 'rest', 'decline', 'weight', 'pressure', 'collapse', 'fatigue', 'loss'],
        'verb': ['rest', 'stop', 'fall', 'break', 'end', 'slow', 'collapse', 'decline', 'fade'],
        'adj':  ['tired', 'heavy', 'fallen', 'broken', 'weary', 'still', 'exhausted'],
        'adv':  ['heavily', 'slowly', 'wearily', 'gently'],
    },
    BALANCE: {
        'noun': ['balance', 'tension', 'equilibrium', 'center', 'duality', 'contrast', 'trade', 'choice'],
        'verb': ['balance', 'weigh', 'compare', 'decide', 'trade', 'mediate', 'hold', 'consider'],
        'adj':  ['balanced', 'equal', 'steady', 'centered', 'measured', 'fair', 'moderate'],
        'adv':  ['evenly', 'carefully', 'moderately', 'equally'],
    },
    CHAOS: {
        'noun': ['chaos', 'change', 'surprise', 'storm', 'disruption', 'turbulence', 'energy', 'noise'],
        'verb': ['scatter', 'disrupt', 'surprise', 'shake', 'transform', 'challenge', 'stir', 'erupt'],
        'adj':  ['wild', 'unpredictable', 'turbulent', 'complex', 'exciting', 'chaotic', 'random'],
        'adv':  ['wildly', 'suddenly', 'unpredictably', 'intensely'],
    },
    HARMONY: {
        'noun': ['harmony', 'truth', 'unity', 'peace', 'love', 'beauty', 'coherence', 'connection'],
        'verb': ['unite', 'harmonize', 'align', 'converge', 'resolve', 'integrate', 'heal', 'connect'],
        'adj':  ['harmonious', 'true', 'unified', 'peaceful', 'beautiful', 'whole', 'coherent', 'good'],
        'adv':  ['truly', 'beautifully', 'peacefully', 'completely'],
    },
    BREATH: {
        'noun': ['rhythm', 'pulse', 'cycle', 'breath', 'flow', 'wave', 'oscillation', 'current'],
        'verb': ['breathe', 'flow', 'pulse', 'oscillate', 'cycle', 'circulate', 'return', 'repeat'],
        'adj':  ['rhythmic', 'flowing', 'cyclic', 'pulsing', 'alive', 'breathing', 'periodic'],
        'adv':  ['rhythmically', 'steadily', 'continuously', 'gently'],
    },
    RESET: {
        'noun': ['beginning', 'renewal', 'origin', 'seed', 'dawn', 'fresh start', 'rebirth', 'genesis'],
        'verb': ['begin', 'restart', 'renew', 'refresh', 'awaken', 'start', 'emerge', 'initiate'],
        'adj':  ['new', 'fresh', 'original', 'first', 'young', 'initial', 'pristine', 'reborn'],
        'adv':  ['freshly', 'newly', 'originally', 'again'],
    },
}
