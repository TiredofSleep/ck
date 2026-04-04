"""
ck_voice.py — CK's Native Voice: Composition-Attention
════════════════════════════════════════════════════════
The dual-lattice language engine.

NOT retrieval. NOT templates. COMPOSITION.

Every word CK speaks is selected by composing two lattices:
  MACRO (I=1, structure): sentence shape, grammar, position
    Runs on triality (B/D/BC → subject/verb/object)
    Produces evens and duality structures
  MICRO (0=void, force): semantic intent, operator meaning
    Runs on duality (said/unsaid, bump/not-bump)
    Produces triad flows

CL[macro_position_op][micro_force_op] = selection_op → word

This is CK's version of attention.
  Transformer: Q·K → weight → weighted V
  CK: CL[position][intent] → composition → word selection

"Attention Is All You Need" — Vaswani 2017.
"Composition Is All You Are" — CK 2026.

(c) 2026 Brayden Sanders / 7Site LLC — TIG Unified Theory
"""

# ═══════════════════════════════════════════════════════════
# §1  IMPORTS & CONSTANTS
# ═══════════════════════════════════════════════════════════

import re, math, random
from collections import defaultdict, Counter
from typing import List, Tuple, Dict, Optional

from ck_being import (
    CL, CL_BHML, CL_STANDARD,
    VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP, BUMP_PAIRS, _BUMP_SET, T_STAR,
    SEEDS, W2OP, PHONAESTHESIA, CELL_INFO,
    fuse, shape, coherence_chain,
)

# ── The Three Tables for Voice ──────────────────────────────
# CL (TSML, 73-harmony): CK's internal view. Harmony everywhere.
#   Used for: coherence scoring, self-awareness, internal state
# CL_BHML (28-harmony): The honest substrate. Binary. Sparse harmony.
#   Used for: MICRO lattice (force/0). Duality → triad flows.
# CL_STANDARD (44-harmony): The paper's table. Balanced.
#   Used for: MACRO lattice (structure/1). Triality → evens and duality.
#
# Voice composition: CL_STD[macro_position_op][CL_BHML[micro_force_op][query_op]]
# This gives real diversity. TSML would collapse everything to HARMONY.
CL_MACRO = CL_STANDARD    # Structure table — triality, balanced
CL_MICRO = CL_BHML        # Force table — duality, honest
CL_INNER = CL             # Self table — harmony-dominant, CK's lens

from ck_doing import (
    classify_sentence, classify_paragraph,
    classify_semantic, classify_rhythm,
    phonaesthesia_op, tokenize,
    TransitionLattice,
)

# ── Sentence Shape Templates (MACRO lattice) ──────────────
# Each shape is an operator sequence defining grammatical structure.
# Triality: BEING(noun) / DOING(verb) / BECOMING(result)
#
# The macro lattice runs on triality, produces evens and duality:
#   COUNTER(2) = question structure
#   COLLAPSE(4) = conditional/contrast structure
#   CHAOS(6)    = exclamatory/discovery structure
#   BREATH(8)   = cyclic/list structure
#
# Odd operators in macro = transitions between structural positions:
#   LATTICE(1)  = subject/topic position
#   PROGRESS(3) = verb/action position
#   BALANCE(5)  = object/complement position
#   HARMONY(7)  = resolution/conclusion position
#   RESET(9)    = new-clause/restart position

# Shape templates: name → operator chain
# Each operator determines what kind of word goes in that position
SENTENCE_SHAPES = {
    # ── Declarative (statement) ──
    'declare':    [LATTICE, PROGRESS, BALANCE],           # S V O
    'declare_x':  [LATTICE, PROGRESS, BALANCE, HARMONY],  # S V O → resolution
    'explain':    [LATTICE, PROGRESS, BALANCE, COUNTER, HARMONY],  # S V O measure resolve

    # ── Interrogative (question) ──
    'ask':        [COUNTER, LATTICE, PROGRESS],            # ? S V
    'ask_deep':   [COUNTER, LATTICE, PROGRESS, BALANCE, COUNTER],  # ? S V O ?

    # ── Imperative (command/suggestion) ──
    'direct':     [PROGRESS, BALANCE],                     # V O
    'suggest':    [PROGRESS, BALANCE, HARMONY],            # V O → resolution

    # ── Conditional ──
    'if_then':    [COLLAPSE, LATTICE, PROGRESS, RESET, LATTICE, PROGRESS],  # if S V then S V
    'contrast':   [LATTICE, PROGRESS, COLLAPSE, LATTICE, PROGRESS],          # S V but S V

    # ── Cyclic/List ──
    'enumerate':  [BREATH, LATTICE, LATTICE, LATTICE, HARMONY],  # each: A B C → resolve
    'rhythm':     [BREATH, PROGRESS, BREATH, PROGRESS, HARMONY],  # cycle do cycle do resolve

    # ── Discovery ──
    'discover':   [CHAOS, LATTICE, PROGRESS, HARMONY],    # ! S V → resolve
    'void_find':  [VOID, COUNTER, LATTICE, PROGRESS],     # nothing → measure S V

    # ── Composition ──
    'compose':    [LATTICE, HARMONY, LATTICE, HARMONY],    # S=S resolve
    'bridge':     [LATTICE, PROGRESS, HARMONY, LATTICE, PROGRESS],  # S V resolve S V
}


# ═══════════════════════════════════════════════════════════
# §2  QUERY DECOMPOSITION — Read the human through CK's math
# ═══════════════════════════════════════════════════════════

def decompose_query(query: str) -> Dict:
    """Decompose a human query into its operator structure.

    Three lenses (same as DialogueEater but focused on the question):
      1. Structural: sentence-level → dominant operator chain
      2. Semantic: word-level → domain + operator chain
      3. Rhythmic: cadence → single operator

    Returns dict with:
      'structural_ops':  operator chain from structural classification
      'semantic_ops':    operator chain from semantic classification
      'rhythm_op':       single operator from rhythm
      'fused_op':        CL[CL[structural][semantic]][rhythm]
      'query_words':     tokenized content words
      'is_question':     bool
      'force_op':        the MICRO (0-derived) force of the query
      'structure_op':    the MACRO (1-derived) structure of the query
    """
    q = query.strip()
    if not q:
        return {
            'structural_ops': [VOID], 'semantic_ops': [VOID],
            'rhythm_op': VOID, 'fused_op': VOID,
            'query_words': [], 'is_question': False,
            'force_op': VOID, 'structure_op': VOID,
        }

    # Lens 1: Structural
    structural_ops = classify_paragraph(q)

    # Lens 2: Semantic
    semantic_ops = classify_semantic(q)

    # Lens 3: Rhythmic
    rhythm_result = classify_rhythm(q)
    rhythm_op = rhythm_result.get('rhythm_op', HARMONY) if isinstance(rhythm_result, dict) else HARMONY

    # Fuse through CL_MICRO (BHML, honest, 28-harmony)
    # NOT through CL (TSML, 73-harmony) which collapses everything to 7
    def _fuse_micro(ops):
        """Fuse operator chain through BHML for honest force."""
        if not ops: return HARMONY
        result = ops[0]
        for op in ops[1:]:
            result = CL_MICRO[result][op]
        return result

    s_fused = _fuse_micro(structural_ops)
    m_fused = _fuse_micro(semantic_ops)
    fused_op = CL_MICRO[CL_MICRO[s_fused][m_fused]][rhythm_op]

    # Detect question
    is_question = '?' in q or any(q.lower().startswith(w) for w in
        ['what ', 'who ', 'why ', 'how ', 'where ', 'when ', 'can ', 'do ',
         'is ', 'are ', 'should ', 'would ', 'could ', 'will '])

    # Content words (non-stop)
    stops = {'the','a','an','is','at','of','in','to','and','or','for','with',
             'on','my','i','it','was','are','be','been','has','have','had',
             'do','does','did','will','would','could','should','may','might',
             'can','shall','this','that','these','those','me','you','we',
             'they','he','she','not','no','yes','but','if','so','as','by',
             'from','up','out','just','very','also','than','then','here',
             'there','like','your','about','please','really'}
    words = [w for w in tokenize(q.lower()) if w not in stops and len(w) > 2]

    # MACRO structure: which shape template fits this query?
    # Questions want question shapes in response
    # Statements want declarative/explanatory shapes
    # Short queries want short responses
    if is_question:
        structure_op = COUNTER  # questions demand measurement in response
    elif len(q.split()) <= 4:
        structure_op = HARMONY  # brief input → concise response
    elif any(w in q.lower() for w in ['but', 'however', 'although', 'yet']):
        structure_op = COLLAPSE  # contrast demands contrast
    elif any(w in q.lower() for w in ['because', 'since', 'therefore']):
        structure_op = PROGRESS  # causal demands explanation
    else:
        structure_op = LATTICE  # default: provide structure

    # MICRO force: what is the query pushing toward?
    # This IS the fused operator — the algebra already computed the force
    force_op = fused_op

    return {
        'structural_ops': structural_ops,
        'semantic_ops': semantic_ops,
        'rhythm_op': rhythm_op,
        'fused_op': fused_op,
        'query_words': words,
        'is_question': is_question,
        'force_op': force_op,
        'structure_op': structure_op,
    }


# ═══════════════════════════════════════════════════════════
# §3  SHAPE SELECTION — Macro lattice picks sentence structure
# ═══════════════════════════════════════════════════════════

def select_shape(query_decomp: Dict) -> Tuple[str, List[int]]:
    """Select sentence shape via CL composition.

    The MACRO lattice (I, structure, triality) determines the shape.

    CL[structure_op][force_op] = shape_selector

    Shape selection rules (from the algebra):
      HARMONY(7) → concise (declare)
      COUNTER(2) → explanatory (explain)
      LATTICE(1) → structural (declare_x)
      PROGRESS(3) → action (direct/suggest)
      COLLAPSE(4) → contrast (contrast/if_then)
      VOID(0) → discovery (void_find)
      CHAOS(6) → surprise (discover)
      BREATH(8) → cyclic (enumerate/rhythm)
      BALANCE(5) → bridging (bridge)
      RESET(9) → fresh start (declare)
    """
    s = query_decomp['structure_op']
    f = query_decomp['force_op']

    # Compose through CL_MACRO — structure table, not TSML
    # TSML would return HARMONY for nearly everything (73/100)
    # STANDARD gives real diversity (44/100 harmony)
    selector = CL_MACRO[s][f]

    # Map composition result to sentence shape
    shape_map = {
        VOID:     'void_find',
        LATTICE:  'declare_x',
        COUNTER:  'explain',
        PROGRESS: 'suggest',
        COLLAPSE: 'contrast',
        BALANCE:  'bridge',
        CHAOS:    'discover',
        HARMONY:  'declare',
        BREATH:   'rhythm',
        RESET:    'declare',
    }

    # Questions always get explanatory shapes (COUNTER demands COUNTER)
    if query_decomp['is_question']:
        if selector == HARMONY:
            shape_name = 'declare_x'  # don't over-concise a question
        else:
            shape_name = shape_map.get(selector, 'explain')
    else:
        shape_name = shape_map.get(selector, 'declare')

    return shape_name, SENTENCE_SHAPES[shape_name]


# ═══════════════════════════════════════════════════════════
# §4  WORD SELECTION — Micro lattice picks words per position
# ═══════════════════════════════════════════════════════════

class CompositionAttention:
    """CK's attention mechanism. Not dot-product. Composition.

    For each position in the sentence shape:
      1. macro_op = the position's structural operator (from shape)
      2. micro_op = the force operator (from query decomposition)
      3. selection_op = CL[macro_op][micro_op]
      4. word = best word for selection_op given context

    The attention isn't learned weights — it's algebraic truth.
    CL[macro][micro] is frozen. What's learned is which WORDS
    map to which operators (via TL, word_pairs, SEEDS).
    """

    def __init__(self, tl: TransitionLattice):
        self.tl = tl

        # Build reverse seed map: operator → list of words
        self.op_words = {}
        for op in range(10):
            self.op_words[op] = list(SEEDS.get(op, []))

        # Expand with phonaesthesia-derived words from TL
        self._expand_vocabulary()

    def _expand_vocabulary(self):
        """Pull learned words from TL into operator vocabulary.

        The TL has word_pairs[(op_a, op_b)] = {(word_a, word_b): count}
        Extract all words and their operator assignments.
        """
        word_op_counts = defaultdict(lambda: defaultdict(int))

        # From word_pairs: words seen at each operator position
        for (op_a, op_b), pairs in self.tl.word_pairs.items():
            for (w1, w2), count in pairs.items():
                word_op_counts[w1][op_a] += count
                word_op_counts[w2][op_b] += count

        # For each word, find its dominant operator
        for word, ops in word_op_counts.items():
            if len(word) < 3:
                continue
            dominant_op = max(ops, key=ops.get)
            if word not in self.op_words.get(dominant_op, []):
                if dominant_op not in self.op_words:
                    self.op_words[dominant_op] = []
                self.op_words[dominant_op].append(word)

    def attend(self, shape_ops: List[int], force_op: int,
               query_words: List[str], query_ops: List[int],
               tl: TransitionLattice = None) -> List[Tuple[int, str]]:
        """Composition-attention: select words for each position.

        For each position i in shape_ops:
          macro_op = shape_ops[i]        (structure)
          micro_op = force at position i (force)
          CL[macro][micro] = selection_op
          word = best word for selection_op

        The micro force SHIFTS across positions:
          Position 0: force = query's fused_op (responding to the question)
          Position 1+: force = CL[prev_selection][query_op_at_i]
          This creates a WALK through the micro lattice driven by the query.

        Returns [(selection_op, word), ...]
        """
        if tl is None:
            tl = self.tl

        result = []
        prev_word = ''
        prev_op = -1
        micro = force_op  # Start with query's fused force

        # Map query words to operators for micro-force walk
        query_op_seq = list(query_ops) if query_ops else [force_op]

        for i, macro_op in enumerate(shape_ops):
            # ── Composition-attention (dual lattice) ──
            # MACRO table (CL_STANDARD) gives structural diversity
            # MICRO table (CL_BHML) gives force honesty
            # CL_MACRO[structure_position][CL_MICRO[force][query_context]]
            if i < len(query_op_seq):
                micro_composed = CL_MICRO[micro][query_op_seq[i]]
            else:
                micro_composed = micro
            selection_op = CL_MACRO[macro_op][micro_composed]

            # ── Word selection ──
            # Priority: TL-learned words > SEEDS words
            word = self._select_word(selection_op, prev_op, prev_word,
                                     query_words, result, tl)

            result.append((selection_op, word))
            prev_word = word
            prev_op = selection_op

            # ── Advance micro force ──
            # The force walks via MICRO table (honest, binary)
            # Duality → triad flows: each step composes to a new force
            if i < len(query_op_seq):
                micro = CL_MICRO[selection_op][query_op_seq[i]]
            else:
                # Past query length: force continues via TL prediction
                candidates = tl.next_operator(selection_op, prev_op)
                if candidates:
                    micro = candidates[0][0]
                else:
                    micro = CL_MICRO[selection_op][force_op]

        return result

    def _select_word(self, target_op: int, prev_op: int, prev_word: str,
                     query_words: List[str], used: List[Tuple],
                     tl: TransitionLattice) -> str:
        """Select the best word for target_op given context.

        Priority:
          1. TL next_word (learned transitions — context-sensitive)
          2. Query-related words (respond TO the query, don't echo it)
          3. TL _words_for_op (operator vocabulary, diversity-sampled)
          4. SEEDS fallback (basic vocabulary)

        Key: entropy-weighted selection. Don't always pick the
        highest-frequency word — sample from the top candidates
        weighted by frequency. This prevents ruts.

        Avoids:
          - Repeating the last 5 words
          - Using stop words
          - Using query words directly (don't echo)
        """
        used_words = {w for _, w in used[-5:]} if used else set()
        query_set = set(query_words)
        stops = {'the','a','an','is','at','of','in','to','and','or','for',
                 'with','on','my','it','was','are','be','by','that','this',
                 'from','not','but','they','which','their','has','had',
                 'been','its','than','can','into','also','these','would',
                 'could','should','about','each','such','both','have',
                 'were','some','may'}

        def _valid(w):
            return (w not in used_words and w not in query_set
                    and w not in stops and len(w) > 2)

        # 1. TL next_word: context-sensitive word following prev_word
        if prev_word and tl:
            candidates = tl.next_word(prev_word, prev_op, target_op)
            valid = [(w, p) for w, p in candidates if _valid(w)]
            if valid:
                # Weighted random from top 5
                top = valid[:5]
                if len(top) > 1:
                    weights = [p for _, p in top]
                    total = sum(weights)
                    r = random.random() * total
                    cum = 0
                    for w, p in top:
                        cum += p
                        if cum >= r:
                            return w
                return top[0][0]

        # 2. Query-related words: respond TO the query
        #    Find words that FOLLOW query words and map to target_op
        for qw in query_words:
            if qw in tl.followers:
                related = []
                for follower, count in tl.followers[qw].items():
                    if not _valid(follower):
                        continue
                    f_op = phonaesthesia_op(follower)
                    if f_op is None:
                        f_op = W2OP.get(follower, -1)
                    if f_op is None:
                        # Check if word appears in word_pairs at target position
                        for (o1, o2), wp in tl.word_pairs.items():
                            if o2 == target_op:
                                for (w1, w2), c in wp.items():
                                    if w2 == follower:
                                        f_op = target_op
                                        break
                            if f_op == target_op:
                                break
                    if f_op == target_op:
                        related.append((follower, count))
                if related:
                    related.sort(key=lambda x: -x[1])
                    top = related[:5]
                    if len(top) > 1:
                        weights = [c for _, c in top]
                        total = sum(weights)
                        r = random.random() * total
                        cum = 0
                        for w, c in top:
                            cum += c
                            if cum >= r:
                                return w
                    return top[0][0]

        # 3. TL _words_for_op: operator vocabulary with diversity
        if tl:
            words = tl._words_for_op(target_op, prev_op)
            valid = [w for w in words if _valid(w)]
            if valid:
                # Don't always pick the first — sample from top
                if len(valid) > 2:
                    idx = random.randint(0, min(2, len(valid)-1))
                    return valid[idx]
                return valid[0]

        # 4. Expanded vocabulary (SEEDS + TL-learned)
        vocab = self.op_words.get(target_op, [])
        valid = [w for w in vocab if _valid(w)]
        if valid:
            return valid[random.randint(0, min(3, len(valid)-1))]

        # 5. Pure SEEDS fallback
        seed_words = SEEDS.get(target_op, ['void'])
        valid = [w for w in seed_words if w not in used_words]
        if valid:
            return valid[0]

        return OP[target_op]  # last resort: operator name itself


# ═══════════════════════════════════════════════════════════
# §5  RESPONSE COMPOSITION — Dual lattice walks
# ═══════════════════════════════════════════════════════════

def dream_speak(query: str, tl: TransitionLattice,
                body_c: float = 0.714, max_words: int = 20,
                creativity: float = 0.5,
                culture: str = 'english') -> Dict:
    """CK's native voice: DREAM-DOMINANT composition.

    78% dream (TL walk, natural word flow)
    22% structure (CL composition, operator guidance)

    Pipeline:
      1. Decompose query -> operators through 3 lenses
      2. Seed the dream with query operators (CL guidance)
      3. Walk the TL picking words (dream flow)
      4. At each step: CL_MICRO[dream_op][query_op] nudges direction
      5. Score the dreamed sentence
      6. If incoherent, try again with different seed

    This is how CK thinks: not slot-filling, not retrieval,
    but DREAMING through learned word transitions with
    algebraic nudges keeping him on topic.
    """
    decomp = decompose_query(query)

    if not decomp['query_words']:
        return {
            'text': f"C={body_c:.3f}.",
            'shape': 'dream',
            'operators': [COUNTER],
            'coherence': 1.0,
            'info_bits': 0.45,
            'fused_query': VOID,
            'force': VOID,
            'structure': HARMONY,
        }

    query_words = decomp['query_words']
    force_op = decomp['force_op']
    structure_op = decomp['structure_op']
    query_ops = decomp['structural_ops']

    best_words = []
    best_ops = []
    best_coh = 0.0

    # Try up to 3 dream seeds -- pick the most coherent
    seed_attempts = [
        [force_op],
        [CL_MACRO[structure_op][force_op]],
        [_word_to_op(query_words[0]) if query_words else HARMONY],
    ]

    for seed_ops in seed_attempts:
        words, ops = _guided_dream(
            tl, seed_ops, query_words, query_ops, force_op,
            max_words=max_words, creativity=creativity
        )

        if not words:
            continue

        coh = _score_coherence(ops)

        if coh > best_coh or not best_words:
            best_words = words
            best_ops = ops
            best_coh = coh

    # ════════════════════════════════════════════════════
    # ENGLISH CONVERSION MATRIX
    # CK's native order: force → structure → resolution
    # English order:     subject → verb → object
    #
    # The operator of each word tells us its ROLE:
    #   LATTICE(1) = noun/subject    PROGRESS(3) = verb/action
    #   BALANCE(5) = object          COUNTER(2) = qualifier
    #   HARMONY(7) = connector       COLLAPSE(4) = contrast
    #   BREATH(8)  = continuation    CHAOS(6) = exclamation
    #   VOID(0)    = negation        RESET(9) = transition
    #
    # Strategy: chunk into clauses, reorder each clause S-V-O,
    # insert minimal English glue between chunks
    # ════════════════════════════════════════════════════
    if best_words and best_ops:
        if culture == 'english':
            best_text = _english_reorder(best_words, best_ops, decomp['is_question'])
        else:
            # Use the culture-specific conversion matrix
            try:
                from ck_languages import reorder_for_culture
                best_text = reorder_for_culture(best_words, best_ops, culture)
            except ImportError:
                best_text = _english_reorder(best_words, best_ops, decomp['is_question'])
    else:
        best_text = ' '.join(best_words) + '.'

    # Body gate
    if body_c < 0.3:
        best_text = f"[C={body_c:.3f}] " + best_text

    info_bits = sum(CELL_INFO[best_ops[i]][best_ops[i+1]]
                    for i in range(len(best_ops)-1)) if len(best_ops) > 1 else 0

    return {
        'text': best_text,
        'shape': 'dream',
        'operators': best_ops,
        'coherence': best_coh,
        'info_bits': round(info_bits, 2),
        'fused_query': decomp['fused_op'],
        'force': force_op,
        'structure': structure_op,
        'culture': culture,
    }


# ═══════════════════════════════════════════════════════════
# §4  ENGLISH CONVERSION MATRIX
# ═══════════════════════════════════════════════════════════
# CK dreams in operator-composition order (like Yoda: "Strong in the Force, you are").
# English needs Subject-Verb-Object order.
#
# The conversion matrix maps operator roles to English positions:
#   LATTICE(1)  → NOUN position (subject or object)
#   PROGRESS(3) → VERB position (action, process)
#   BALANCE(5)  → COMPLEMENT position (result, measure)
#   COUNTER(2)  → QUALIFIER position (how, when, where)
#   HARMONY(7)  → CONNECTOR (and, because, where, through)
#   COLLAPSE(4) → CONTRAST (but, yet, while, despite)
#   BREATH(8)   → CONTINUATION (and, while, as)
#   CHAOS(6)    → EMPHASIS (even, beyond, suddenly)
#   VOID(0)     → NEGATION (not, without, beyond)
#   RESET(9)    → TRANSITION (then, instead, again)
#
# Strategy:
#   1. Chunk the dream output into CLAUSES at natural break operators
#   2. Within each clause, sort words by English role: S before V before O
#   3. Insert minimal English glue between clauses
#   4. Capitalize and punctuate
# ═══════════════════════════════════════════════════════════

# English role: operators that mark nouns (subjects/objects)
_NOUN_OPS = {LATTICE, BALANCE, COUNTER}
# English role: operators that mark verbs (actions/processes)
_VERB_OPS = {PROGRESS, COLLAPSE, CHAOS}
# English role: operators that mark connectors/glue
_CONN_OPS = {HARMONY, BREATH, RESET, VOID}

# Glue words inserted between clauses based on the bridging operator
_CLAUSE_GLUE = {
    HARMONY:  ['where', 'and', 'through', 'because'],
    BREATH:   ['while', 'as', 'and'],
    COLLAPSE: ['but', 'yet', 'despite'],
    RESET:    ['then', 'until', 'before'],
    VOID:     ['without', 'beyond', 'not'],
    CHAOS:    ['even', 'beyond', 'suddenly'],
    COUNTER:  ['where', 'when', 'because'],
    PROGRESS: ['creating', 'becoming', 'through'],
    LATTICE:  ['within', 'from', 'toward'],
    BALANCE:  ['into', 'toward', 'between'],
}


def _english_reorder(words: List[str], ops: List[int],
                     is_question: bool = False) -> str:
    """Convert CK's operator-order word sequence into English word order.

    CK dreams: force → structure → resolution (Yoda order)
    English:   subject → verb → object (SVO order)

    This function chunks the dream output into clauses,
    reorders each clause to approximate English SVO,
    and inserts minimal glue between clauses.
    """
    if not words:
        return ""

    # Step 1: Chunk into clauses at natural break points
    # A clause break needs 3+ words accumulated AND a connector operator
    # This prevents choppy 2-word "clauses"
    clauses = []
    current_clause = []    # list of (word, op, original_index)
    clause_break_op = None

    for i, (w, op) in enumerate(zip(words, ops)):
        # Clause boundary: connector with 3+ words, or hard max at 7
        if (op in _CONN_OPS and len(current_clause) >= 3) or len(current_clause) >= 7:
            if current_clause:
                clauses.append((current_clause, clause_break_op))
            current_clause = []
            clause_break_op = op
            if op in _CONN_OPS:
                continue  # skip the connector word itself

        current_clause.append((w, op, i))

    if current_clause:
        clauses.append((current_clause, clause_break_op))

    # Step 2: Reorder each clause to English SVO
    reordered_clauses = []

    for clause_words, break_op in clauses:
        nouns = [(w, op, idx) for w, op, idx in clause_words if op in _NOUN_OPS]
        verbs = [(w, op, idx) for w, op, idx in clause_words if op in _VERB_OPS]
        others = [(w, op, idx) for w, op, idx in clause_words
                  if op not in _NOUN_OPS and op not in _VERB_OPS]

        # English order: Subject(noun) + Verb + Object(noun) + Modifiers
        ordered = []

        # Subject: first noun
        if nouns:
            ordered.append(nouns[0])
            remaining_nouns = nouns[1:]
        else:
            remaining_nouns = []

        # Verb: first verb
        if verbs:
            ordered.append(verbs[0])
            remaining_verbs = verbs[1:]
        else:
            remaining_verbs = []

        # Object: second noun or remaining verbs' objects
        if remaining_nouns:
            ordered.append(remaining_nouns[0])
            remaining_nouns = remaining_nouns[1:]

        # Remaining modifiers/nouns/verbs in original order
        remaining = remaining_nouns + remaining_verbs + others
        remaining.sort(key=lambda x: x[2])  # restore original relative order
        ordered.extend(remaining)

        reordered_clauses.append(([w for w, _, _ in ordered], break_op))

    # Step 3: Assemble with MINIMAL glue between clauses
    # Only insert glue at major boundaries, skip when it would be choppy
    result_parts = []
    for i, (clause, break_op) in enumerate(reordered_clauses):
        if i > 0:
            # Only insert glue every other clause, or when break_op is strong
            if break_op in {COLLAPSE, RESET, VOID} or (i % 2 == 1 and break_op is not None):
                glue_options = _CLAUSE_GLUE.get(break_op, ['and'])
                glue = glue_options[i % len(glue_options)]
                result_parts.append(glue)
            else:
                # Comma break instead of word (lighter connection)
                if result_parts:
                    result_parts[-1] = result_parts[-1] + ','
        result_parts.extend(clause)

    # Step 4: Post-process
    text = ' '.join(result_parts)

    # Capitalize first word
    if text:
        text = text[0].upper() + text[1:]

    # Period
    text += '.'

    return text


def _word_to_op(word: str) -> int:
    """Quick word -> operator lookup."""
    op = W2OP.get(word, None)
    if op is not None:
        return op
    op = phonaesthesia_op(word)
    if op is not None:
        return op
    return classify_sentence(word)


def _guided_dream(tl: TransitionLattice, seed_ops: List[int],
                  query_words: List[str], query_ops: List[int],
                  force_op: int, max_words: int = 20,
                  creativity: float = 0.5) -> Tuple[List[str], List[int]]:
    """Dream through the TL, guided by query operators.

    Like tl.dream() but with CL composition nudging the walk
    toward addressing the query.

    78% dream: follow TL word transitions naturally
    22% structure: CL_MICRO[current][query] nudges next operator

    The query words seed the follower lookups — CK starts
    dreaming FROM the query's vocabulary, not randomly.
    """
    stops = {'the','a','an','is','at','of','in','to','and','or','for',
             'with','on','my','it','was','are','be','by','that','this',
             'from','not','but','they','which','their','has','had',
             'been','its','than','can','into','also','these','would',
             'could','should','about','each','such','both','have',
             'were','some','may','often','used','one','two','also',
             'many','more','most','much','well','just','other','like',
             'between','through','where','when','while','then','before',
             'after','during','within','without','however','although',
             'because','since','therefore','thus','hence','yet',
             # Common function words that dominate TL but carry no info
             'all','does','every','what','how','means','says','back',
             'matters','becomes','another','something','until','only',
             'same','different','enough','still','never','always',
             'really','very','way','things','being','make','made',
             'even','get','got','let','put','take','too','own','any',
             # HTML/CSS artifacts from old Ollama eating
             'px','margin','padding','top','bottom','left','right',
             'center','flex','display','align','items','content',
             'div','span','class','style','width','height','color',
             'font','size','border','background','text','none',
             'auto','block','inline','relative','absolute','fixed',
             'overflow','hidden','visible','opacity','transform',
             'margin-top','align-items','12px','8px','16px','0px',
             'href','src','img','url','http','https','www','html',
             'css','javascript','onclick','function','var','let','const',
             }
    query_set = set(query_words)

    words = []
    ops = []
    prev_word = ''
    current_op = seed_ops[0]

    # Start from a query-word follower (respond TO the query)
    # The relationship between query words and response words
    # is the densest information bridge possible.
    # Start by finding words that FOLLOW each query word —
    # these are the bridge between what was asked and what is answered.
    start_word = _find_start_word(tl, query_words, current_op, stops)
    if start_word:
        words.append(start_word)
        ops.append(current_op)
        prev_word = start_word

    # Inject query-followers at key positions (every ~4 words)
    # to keep the dream anchored to the prompt
    query_anchors = []
    for qw in query_words:
        if qw in tl.followers:
            best = [(f, c) for f, c in sorted(tl.followers[qw].items(), key=lambda x: -x[1])
                    if f not in stops and len(f) > 2 and f not in query_set][:3]
            if best:
                query_anchors.append(best)

    for step in range(max_words - len(words)):
        # ── Query anchor: every ~5 words, inject a query-related word ──
        # This keeps the dream ABOUT the prompt
        if query_anchors and step > 0 and step % 5 == 0:
            anchor_idx = (step // 5 - 1) % len(query_anchors)
            anchor_words = query_anchors[anchor_idx]
            for aw, ac in anchor_words:
                if aw not in set(words[-4:]) and aw not in stops:
                    aw_op = phonaesthesia_op(aw)
                    if aw_op is None:
                        aw_op = W2OP.get(aw, current_op)
                    words.append(aw)
                    ops.append(aw_op if aw_op is not None else current_op)
                    prev_word = aw
                    current_op = ops[-1]
                    break

        # ════════════════════════════════════════════════════
        # DREAM LEADS: Generate random diverse candidates
        # STABILITY PICKS: Score by coherence, pick best path
        # "Let the dream layer lead the charge and the
        #  stability layer pick the path" -- Brayden
        # ════════════════════════════════════════════════════
        all_used = set(words)

        # DREAM ATTACK: gather candidates from multiple sources
        dream_pool = []

        # Source 1: Direct followers of prev_word (natural flow)
        if prev_word:
            followers = tl.next_word(prev_word, current_op)
            for w, p in followers:
                if (w not in stops and len(w) > 3 and w not in all_used
                    and w not in query_set
                    and not any(c.isdigit() for c in w)
                    and ('-' not in w or w in {'self-', 'well-', 'co-'})):
                    dream_pool.append((w, p, 'flow'))

        # Source 2: Words for predicted next operator (exploration)
        op_cands = tl.next_operator(current_op,
                                     ops[-2] if len(ops) >= 2 else -1)
        if op_cands:
            for pred_op, prob in op_cands[:3]:
                op_words = tl._words_for_op(pred_op, current_op)
                for w in op_words:
                    if (w not in stops and len(w) > 3 and w not in all_used
                        and w not in query_set):
                        dream_pool.append((w, prob, 'explore'))

        # Source 3: Query anchors (keep response ABOUT the query)
        if query_anchors:
            anchor_idx = step % len(query_anchors)
            for aw, ac in query_anchors[anchor_idx]:
                if aw not in all_used and aw not in stops and len(aw) > 3:
                    dream_pool.append((aw, 0.5, 'anchor'))

        # STABILITY SELECTION: score each candidate by coherence
        if dream_pool:
            # Remove duplicates
            seen = set()
            unique_pool = []
            for w, p, src in dream_pool:
                if w not in seen:
                    seen.add(w)
                    unique_pool.append((w, p, src))

            # Score by: CL coherence with query + CL coherence with previous
            q_idx = step % max(len(query_ops), 1)
            q_op = query_ops[q_idx] if q_idx < len(query_ops) else force_op

            scored = []
            for w, p, src in unique_pool:
                w_op = phonaesthesia_op(w)
                if w_op is None:
                    w_op = W2OP.get(w, -1)
                if w_op < 0:
                    w_op = sum(ord(c) * (j+1) for j, c in enumerate(w)) % 10

                # Stability score: how coherent is this word in context?
                # CL[prev_op][word_op] -> does it harmonize with where we are?
                prev_coh = 1.0 if CL[current_op][w_op] == HARMONY else 0.5
                # CL[word_op][query_op] -> does it connect to the query?
                query_coh = 1.0 if CL_STANDARD[w_op][q_op] == HARMONY else 0.5
                # Anchor bonus
                anchor_bonus = 0.3 if src == 'anchor' else 0.0

                stability = prev_coh * 0.4 + query_coh * 0.4 + anchor_bonus + p * 0.2
                scored.append((w, stability, w_op))

            scored.sort(key=lambda x: -x[1])

            # RANDOM ATTACK from top: don't always pick the best
            top = scored[:6]
            if len(top) > 1:
                # Weighted random from top candidates
                weights = [s ** 2 for _, s, _ in top]  # square to prefer better
                total_w = sum(weights)
                r = random.random() * total_w
                cum = 0
                chosen_word, _, chosen_op = top[0]
                for (w, s, o), wt in zip(top, weights):
                    cum += wt
                    if cum >= r:
                        chosen_word, chosen_op = w, o
                        break
            else:
                chosen_word, _, chosen_op = top[0]

            words.append(chosen_word)
            ops.append(chosen_op)
            prev_word = chosen_word
            current_op = chosen_op
            continue

        # No word candidates from followers — use operator prediction
        op_candidates = tl.next_operator(current_op,
                                          ops[-2] if len(ops) >= 2 else -1)
        if not op_candidates:
            break

        # Nudge: blend TL prediction with CL composition
        next_op = op_candidates[0][0]
        if random.random() < 0.22:  # 22% structure
            next_op = nudge_op

        # Find word for next_op -- avoid ALL repeats
        op_words = tl._words_for_op(next_op, current_op)
        all_used = set(words)
        valid_words = [w for w in op_words
                      if w not in stops and len(w) > 3
                      and w not in all_used
                      and w not in query_set]
        # Prefer unused words
        fresh = [w for w in valid_words if w not in all_used]
        if fresh:
            valid_words = fresh

        if valid_words:
            if len(valid_words) > 2:
                word = valid_words[random.randint(0, min(2, len(valid_words)-1))]
            else:
                word = valid_words[0]
        else:
            # Last resort: SEEDS
            seed_words = SEEDS.get(next_op, [OP[next_op]])
            valid = [w for w in seed_words if w not in set(words[-3:])]
            word = valid[0] if valid else OP[next_op]

        words.append(word)
        ops.append(next_op)
        prev_word = word
        current_op = next_op

    return words, ops


def _find_start_word(tl: TransitionLattice, query_words: List[str],
                     target_op: int, stops: set) -> str:
    """Find a good starting word by looking at what follows query words."""
    all_candidates = []
    for qw in query_words:
        if qw in tl.followers:
            for follower, count in tl.followers[qw].items():
                if follower in stops or len(follower) <= 3:
                    continue
                if follower in set(query_words):
                    continue
                all_candidates.append((follower, count))

    if all_candidates:
        # Diverse selection: use sqrt(count) to flatten distribution
        import math
        all_candidates.sort(key=lambda x: -x[1])
        top = all_candidates[:15]  # wider pool
        weights = [math.sqrt(c) for _, c in top]
        total_w = sum(weights)
        r = random.random() * total_w
        cum = 0
        for (w, _), wt in zip(top, weights):
            cum += wt
            if cum >= r:
                return w
        return top[0][0]

    # No followers found -- use _words_for_op with diversity
    words = tl._words_for_op(target_op, -1)
    valid = [w for w in words if w not in stops and len(w) > 3]
    if valid:
        return valid[random.randint(0, min(4, len(valid)-1))]

    return SEEDS.get(target_op, ['structure'])[0]


# Keep compose_response as alias for backward compat
def compose_response(query: str, tl: TransitionLattice,
                     body_c: float = 0.714, max_sentences: int = 3,
                     culture: str = 'english') -> Dict:
    """Wrapper: calls dream_speak (the real voice)."""
    return dream_speak(query, tl, body_c, max_words=max_sentences * 8,
                       creativity=0.5, culture=culture)


def _score_coherence(ops: List[int]) -> float:
    """Score operator chain coherence via all three tables.

    CL_INNER (TSML): CK's self-judgment — high harmony expected
    CL_MACRO (STD): Paper coherence — moderate harmony
    CL_MICRO (BHML): Honest coherence — sparse harmony

    Final score blends all three:
      inner * 0.3 + macro * 0.3 + micro * 0.4
    Micro weight highest because honest coherence is hardest to achieve.
    """
    if len(ops) < 2:
        return 1.0
    n = len(ops) - 1
    inner_h = sum(1 for i in range(n) if CL_INNER[ops[i]][ops[i+1]] == HARMONY) / n
    macro_h = sum(1 for i in range(n) if CL_MACRO[ops[i]][ops[i+1]] == HARMONY) / n
    micro_h = sum(1 for i in range(n) if CL_MICRO[ops[i]][ops[i+1]] == HARMONY) / n
    return inner_h * 0.3 + macro_h * 0.3 + micro_h * 0.4


# ═══════════════════════════════════════════════════════════
# §6  THOUGHT-TO-VOICE — Replace hardcoded templates
# ═══════════════════════════════════════════════════════════

def thought_to_voice(thought_type: str, data: dict,
                     tl: TransitionLattice,
                     body_c: float = 0.714) -> str:
    """Convert a daemon thought into CK's composed words.

    Instead of hardcoded f-strings, compose through the dual lattice.

    Each thought type maps to a force operator:
      coherence_drop   → COLLAPSE (force: something broke)
      coherence_rise   → PROGRESS (force: something grew)
      new_sovereignty  → LATTICE  (force: structure crystallized)
      dream_discovery  → CHAOS    (force: surprise found)
      eater_spike      → HARMONY  (force: resonance detected)
      entropy_shift    → BREATH   (force: rhythm changed)
      landscape        → COUNTER  (force: measurement taken)

    The structure comes from what the thought IS about.
    The force comes from what the thought MEANS.
    """
    # Map thought type to operators
    type_ops = {
        'coherence_drop':  (COLLAPSE, COUNTER),   # break + measure
        'coherence_rise':  (PROGRESS, HARMONY),    # grow + resolve
        'new_sovereignty': (LATTICE, PROGRESS),    # structure + grow
        'dream_discovery': (CHAOS, COUNTER),       # surprise + measure
        'eater_spike':     (HARMONY, PROGRESS),    # resonate + grow
        'entropy_shift':   (BREATH, COUNTER),      # cycle + measure
        'landscape':       (COUNTER, LATTICE),     # measure + structure
    }

    force_op, struct_op = type_ops.get(thought_type, (HARMONY, LATTICE))

    # Build a pseudo-query from the thought data
    pseudo_query = _thought_to_pseudo_query(thought_type, data)

    # Compose through the normal pipeline
    result = compose_response(pseudo_query, tl, body_c, max_sentences=1)

    # Inject measured values where operators demand COUNTER
    text = result['text']
    text = _inject_measurements(text, thought_type, data)

    return text


def _thought_to_pseudo_query(thought_type: str, data: dict) -> str:
    """Convert thought data into a query string for composition.

    Not a template — just extract the key words that the thought
    is ABOUT, so decompose_query can classify them correctly.
    """
    if thought_type == 'coherence_drop':
        return f"coherence dropped {data.get('now', 0):.3f} shifted"
    if thought_type == 'coherence_rise':
        return f"coherence climbing settling {data.get('now', 0):.3f}"
    if thought_type == 'new_sovereignty':
        domains = ' '.join(data.get('domains', []))
        return f"sovereignty crystallized domains {domains}"
    if thought_type == 'dream_discovery':
        chain = ' '.join(data.get('chain', []))
        return f"dreamed discovery chain {chain} pattern"
    if thought_type == 'eater_spike':
        return f"conversation bumps {data.get('bumps', 0)} info density nutritious"
    if thought_type == 'entropy_shift':
        direction = 'growing diversifying' if data.get('delta', 0) > 0 else 'compressing crystallizing'
        return f"entropy {direction} patterns"
    if thought_type == 'landscape':
        return f"processes {data.get('total', 0)} scanning dominant {data.get('dominant_op', '')}"
    return "observing"


def _inject_measurements(text: str, thought_type: str, data: dict) -> str:
    """Where the composed text has COUNTER-position words,
    inject actual measurements. CK doesn't lie about numbers."""
    # This is the one place where hardcoded values enter —
    # because measurements ARE COUNTER and COUNTER is precise.
    if thought_type == 'coherence_drop' and 'now' in data:
        text += f" C={data['now']:.3f}."
    elif thought_type == 'coherence_rise' and 'now' in data:
        text += f" C={data['now']:.3f}."
    elif thought_type == 'entropy_shift' and 'now' in data:
        text += f" H={data['now']:.3f}."
    elif thought_type == 'eater_spike' and 'bumps' in data:
        text += f" {data['bumps']} bumps."
    return text


# ═══════════════════════════════════════════════════════════
# §7  CONVERSATION ATTENTION — Address the prompt, specifically
# ═══════════════════════════════════════════════════════════

class ConversationAttention:
    """CK's conversational focus. Addresses the prompt specifically,
    entirely, and singularly.

    The problem with retrieval-based responses:
      - CK finds text ABOUT the topic
      - CK stitches excerpts together
      - Result: tangentially related rambling

    The fix: operator-level attention to the query.

    For each heavy word in the query:
      1. Classify it to an operator
      2. That operator MUST appear in the response
      3. The response is GATED by query coverage

    If CK can't cover all query operators, he says so honestly
    rather than rambling around the gaps.
    """

    def __init__(self, tl: TransitionLattice):
        self.tl = tl
        self.attention = CompositionAttention(tl)

    def respond(self, query: str, body_c: float = 0.714) -> Dict:
        """Full composition-attention response.

        Steps:
          1. Decompose query into operators
          2. Map each heavy word to its operator
          3. For each query operator, compose a sentence fragment
          4. Verify coverage: every query operator must be addressed
          5. If gaps: state them honestly
          6. Assemble final response
        """
        decomp = decompose_query(query)
        words = decomp['query_words']

        if not words:
            return compose_response(query, self.tl, body_c, max_sentences=1)

        # Map each query word to its operator
        word_ops = []
        for w in words:
            op = W2OP.get(w, None)
            if op is None:
                op = phonaesthesia_op(w)
            if op is None:
                op = classify_sentence(w)
            word_ops.append((w, op))

        # Group by operator — these are the TOPICS to address
        # Use CL_MICRO to compose overlapping operators into distinct groups
        op_words = defaultdict(list)
        for w, op in word_ops:
            # If this operator already exists, add word to it
            # If not, check if it COMPOSES with an existing one (CL_MICRO)
            placed = False
            for existing_op in list(op_words.keys()):
                composed = CL_MICRO[op][existing_op]
                if composed == op or composed == existing_op:
                    op_words[existing_op].append(w)
                    placed = True
                    break
            if not placed:
                op_words[op].append(w)

        # Compose a response fragment for each operator group
        fragments = []
        covered_ops = set()

        for target_op, topic_words in op_words.items():
            # Create a focused sub-query
            sub_query = ' '.join(topic_words)
            sub_decomp = decompose_query(sub_query)

            # Force the response to address THIS operator
            sub_decomp['force_op'] = target_op

            # Select shape
            shape_name, shape_ops = select_shape(sub_decomp)

            # Compose with this focus
            fragment = self.attention.attend(
                shape_ops=shape_ops,
                force_op=target_op,
                query_words=topic_words,
                query_ops=[target_op] * len(topic_words),
                tl=self.tl,
            )

            frag_words = [w for _, w in fragment]
            frag_ops = [o for o, _ in fragment]
            frag_text = ' '.join(frag_words)

            fragments.append({
                'text': frag_text,
                'target_op': target_op,
                'ops': frag_ops,
                'topic_words': topic_words,
            })
            covered_ops.add(target_op)

        # Check coverage
        all_query_ops = set(op for _, op in word_ops)
        uncovered = all_query_ops - covered_ops

        # Assemble
        sentences = []
        all_ops = []
        for frag in fragments:
            sentences.append(frag['text'] + '.')
            all_ops.extend(frag['ops'])

        if uncovered:
            gap_names = [OP[op] for op in uncovered]
            sentences.append(f"Gap: {', '.join(gap_names)}.")

        full_text = ' '.join(sentences)
        if full_text:
            full_text = full_text[0].upper() + full_text[1:]

        coh = _score_coherence(all_ops)

        return {
            'text': full_text,
            'shape': 'composed',
            'operators': all_ops,
            'coherence': coh,
            'info_bits': sum(CELL_INFO[all_ops[i]][all_ops[i+1]]
                            for i in range(len(all_ops)-1)) if len(all_ops) > 1 else 0,
            'fused_query': decomp['fused_op'],
            'force': decomp['force_op'],
            'structure': decomp['structure_op'],
            'coverage': len(covered_ops) / max(len(all_query_ops), 1),
            'uncovered': list(uncovered),
        }


# ═══════════════════════════════════════════════════════════
# §8  STANDALONE TEST — Run to verify voice
# ═══════════════════════════════════════════════════════════

def _test_voice():
    """Test the composition-attention voice."""
    import os

    print("=" * 60)
    print("  CK VOICE TEST — Composition-Attention")
    print("  CL[structure][force] = word selection")
    print("=" * 60)
    print()

    # Create or load TL
    tl_path = os.path.join(os.path.dirname(__file__), 'ck7', 'ck_experience', 'master_tl.json')
    tl = TransitionLattice(tl_path if os.path.exists(tl_path) else None)

    # If TL is empty, feed it some basic sentences so it has word_pairs
    if tl.total_transitions == 0:
        print("  [BOOT] No TL found — seeding with basic vocabulary...")
        seed_texts = [
            "Structure creates pattern through system and framework.",
            "Harmony resolves truth and brings unity together.",
            "Progress builds and grows through learning development.",
            "Chaos disrupts the expected pattern randomly.",
            "Balance holds tension between equal forces.",
            "Breath cycles through rhythm and returns.",
            "Void is absence and silence and nothing.",
            "Counter measures and compares the evidence.",
            "Collapse breaks and fails when structure ends.",
            "Reset begins fresh from the origin seed.",
            "Coherence emerges when structure meets harmony.",
            "The pattern grows through composition not retrieval.",
            "Each word is selected by the algebra.",
            "Force flows through structure creating meaning.",
            "Attention composes position with intent.",
        ]
        for text in seed_texts:
            tl.eat_text(text)
        print(f"  [BOOT] Seeded TL: {tl.total_transitions} transitions, "
              f"{sum(len(v) for v in tl.word_pairs.values())} word pairs")
        print()

    # Test queries
    test_queries = [
        "Should I share you freely with other humans?",
        "What is coherence?",
        "Tell me about harmony and chaos.",
        "How do you think?",
        "I love you.",
        "What are you?",
        "Build something.",
        "The world is broken but beauty persists.",
    ]

    voice = ConversationAttention(tl)

    for q in test_queries:
        print(f"  QUERY: {q}")

        # Decompose
        decomp = decompose_query(q)
        print(f"  DECOMP: force={OP[decomp['force_op']]}, "
              f"structure={OP[decomp['structure_op']]}, "
              f"fused={OP[decomp['fused_op']]}")
        print(f"  WORDS: {decomp['query_words']}")

        # Simple composition
        simple = compose_response(q, tl, body_c=0.714, max_sentences=2)
        print(f"  SIMPLE: {simple['text']}")
        print(f"    shape={simple['shape']}, coh={simple['coherence']:.2f}, "
              f"info={simple['info_bits']} bits")

        # Full attention
        full = voice.respond(q, body_c=0.714)
        print(f"  ATTEND: {full['text']}")
        print(f"    coverage={full.get('coverage', 1.0):.0%}, "
              f"coh={full['coherence']:.2f}")
        if full.get('uncovered'):
            print(f"    GAPS: {[OP[o] for o in full['uncovered']]}")

        print()

    print("=" * 60)
    print("  Voice test complete.")
    print("=" * 60)


if __name__ == '__main__':
    _test_voice()
