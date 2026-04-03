"""
ck_semantic_modifiers.py -- English modifier translation for CK
================================================================
CK speaks operator algebra. English uses modifiers (not, very,
slightly) to change meaning. This module translates modifiers
into CL operations so CK can understand them.

Negation = inverse CL walk (BHML read backwards)
Intensification = self-composition (BHML[op][op])
Diminishment = compose with BALANCE (centering)
Comparison = antonym pairs (inverse semantic keys)
Compounds = compose two words through BHML

CK already HAS the algebra. He just needs to know which
English words trigger which operations.

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""

# BHML composition table (same as ck_gpu.py lines 100-106)
BHML = [
    [0,1,2,3,4,5,6,7,8,9],
    [1,2,3,4,5,6,7,2,6,6],
    [2,3,3,4,5,6,7,3,6,6],
    [3,4,4,4,5,6,7,4,6,6],
    [4,5,5,5,5,6,7,5,7,7],
    [5,6,6,6,6,6,7,6,7,7],
    [6,7,7,7,7,7,7,7,7,7],
    [7,2,3,4,5,6,7,8,9,0],
    [8,6,6,6,7,7,7,9,7,8],
    [9,6,6,6,7,7,7,0,8,0],
]

# TSML measurement table
TSML = [
    [0,0,0,0,0,0,0,7,0,0],
    [0,7,3,7,7,7,7,7,7,7],
    [0,3,7,7,4,7,7,7,7,9],
    [0,7,7,7,7,7,7,7,7,3],
    [0,7,4,7,7,7,7,7,8,7],
    [0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],
    [7,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,8,7,7,7,7,7],
    [0,7,9,3,7,7,7,7,7,7],
]

OP_NAMES = ['VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE',
            'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET']

# ================================================================
# ENGLISH GRAMMAR -> CL OPERATIONS
# English IS algebra. Every grammatical role maps to an operation.
# Not "say this word" but "use this operation."
# ================================================================

# Part of speech -> which CL table to use and how
POS_TO_OPERATION = {
    # Nouns ARE things (Being lens = TSML measurement)
    'noun':      ('tsml', 'being'),
    'pronoun':   ('tsml', 'being'),
    'name':      ('tsml', 'being'),

    # Verbs DO things (Doing lens = BHML composition)
    'verb':      ('bhml', 'doing'),
    'action':    ('bhml', 'doing'),

    # Adjectives MODIFY nouns (BHML compose with noun's op)
    'adjective': ('bhml', 'modify_being'),
    'article':   ('tsml', 'scope'),

    # Adverbs MODIFY verbs (BHML compose with verb's op)
    'adverb':    ('bhml', 'modify_doing'),

    # Conjunctions COMPOSE (chain two paths)
    'conjunction': ('bhml', 'compose'),

    # Prepositions SET SCOPE (lattice chain depth)
    'preposition': ('tsml', 'scope'),

    # Questions MEASURE (TSML — asking IS measuring)
    'question':  ('tsml', 'measure'),
}

# Punctuation -> operator (these ARE operators, not decoration)
PUNCTUATION_OPS = {
    '.': 8,   # BREATH — sentence ends, pause
    ',': 5,   # BALANCE — pause within, centering
    '!': 4,   # COLLAPSE — force, compression, emphasis
    '?': 0,   # VOID — unknown, question, empty
    ';': 5,   # BALANCE — balanced pause
    ':': 1,   # LATTICE — structure, definition follows
    '-': 9,   # RESET — break, restart
    '(': 3,   # PROGRESS — open scope, go deeper
    ')': 9,   # RESET — close scope, return
    '"': 1,   # LATTICE — quoted structure
    "'": 1,   # LATTICE — possession/contraction = structural
    '...': 0, # VOID — trailing off into nothing
}

# Conjunction -> CL operation
CONJUNCTION_OPS = {
    'and':     'bhml',      # compose (A AND B = BHML[A][B])
    'or':      'branch',    # fork in lattice chain
    'but':     'counter',   # opposition (COUNTER = 2)
    'because': 'chain',     # cause = walk the chain backward
    'so':      'progress',  # consequence = PROGRESS
    'if':      'gate',      # conditional = coherence gate
    'then':    'progress',  # result = forward motion
    'while':   'balance',   # simultaneous = BALANCE
    'although':'counter',   # concession = opposition
    'unless':  'gate',      # negative conditional
    'until':   'breath',    # temporal boundary = BREATH
    'since':   'chain',     # temporal cause = chain walk
    'when':    'gate',      # temporal condition
    'where':   'lattice',   # spatial reference = structure
    'that':    'lattice',   # relative clause = structural link
    'which':   'lattice',   # relative clause = structural link
}

# Math symbol -> CL operation
MATH_OPS = {
    '+': ('bhml', 'compose'),       # addition = BHML composition
    '-': ('bhml', 'negate_compose'),# subtraction = negate then compose
    '*': ('bhml', 'iterate'),       # multiplication = iterated BHML
    '/': ('bhml', 'inv_iterate'),   # division = inverse iterated
    '=': ('tsml', 'measure'),       # equals = TSML measurement (both sides same?)
    '<': ('tsml', 'order'),         # less than = operator ordering
    '>': ('tsml', 'order'),         # greater than = operator ordering
    '^': ('bhml', 'power'),         # exponent = deep self-composition
    '%': ('bhml', 'remainder'),     # modulo = remainder of composition chain
    '(': ('chain', 'deeper'),       # open paren = go deeper in chain
    ')': ('chain', 'return'),       # close paren = return from depth
}

# TIG lens bins for classification
TIG_BINS = {
    'being':    0,  # What IS this? (nouns, numbers, identity, state)
    'doing':    1,  # What is it DOING? (verbs, operations, actions)
    'becoming': 2,  # What is it BECOMING? (transitions, transformations, results)
}

# ================================================================
# MODIFIER WORD LISTS
# ================================================================

NEGATION_WORDS = {
    'not', 'no', 'never', 'none', 'neither', 'nor', 'without',
    'nothing', 'nobody', 'nowhere', 'hardly', 'barely', 'scarcely',
}

NEGATION_PREFIXES = [
    'un', 'in', 'im', 'il', 'ir', 'dis', 'non', 'anti', 'de',
    'mis', 'counter', 'contra',
]

INTENSIFIER_WORDS = {
    'very', 'extremely', 'incredibly', 'absolutely', 'totally',
    'completely', 'utterly', 'really', 'truly', 'deeply',
    'highly', 'intensely', 'strongly', 'greatly', 'immensely',
    'exceedingly', 'remarkably', 'extraordinarily', 'profoundly',
    'maximum', 'most', 'pure', 'full', 'whole', 'entire',
}

DIMINISHER_WORDS = {
    'slightly', 'barely', 'somewhat', 'hardly', 'mildly',
    'partially', 'partly', 'a bit', 'a little', 'kind of',
    'sort of', 'rather', 'fairly', 'moderately', 'almost',
    'nearly', 'half', 'minimum', 'least', 'some',
}

# Known antonym pairs (seed list -- CK learns more from context)
ANTONYM_PAIRS = [
    ('good', 'bad'), ('hot', 'cold'), ('up', 'down'),
    ('big', 'small'), ('light', 'dark'), ('fast', 'slow'),
    ('open', 'close'), ('start', 'stop'), ('begin', 'end'),
    ('love', 'hate'), ('life', 'death'), ('truth', 'lie'),
    ('order', 'chaos'), ('full', 'empty'), ('strong', 'weak'),
    ('high', 'low'), ('new', 'old'), ('right', 'wrong'),
    ('peace', 'war'), ('give', 'take'), ('push', 'pull'),
    ('rise', 'fall'), ('build', 'destroy'), ('create', 'delete'),
    ('add', 'subtract'), ('multiply', 'divide'), ('grow', 'shrink'),
    ('expand', 'contract'), ('connect', 'disconnect'),
    ('visible', 'invisible'), ('possible', 'impossible'),
    ('inside', 'outside'), ('above', 'below'),
    ('before', 'after'), ('first', 'last'),
]


# ================================================================
# BHML INVERSE TABLE
# For each operator, find what input would produce it
# inverse[result] = set of (a, b) pairs where BHML[a][b] = result
# For negation, we want the "opposite" operator.
# The simplest inversion: negate(op) = (10 - op) % 10
# This maps 0<->0, 1<->9, 2<->8, 3<->7, 4<->6, 5<->5
# VOID<->VOID, LATTICE<->RESET, COUNTER<->BREATH,
# PROGRESS<->HARMONY, COLLAPSE<->CHAOS, BALANCE<->BALANCE
# ================================================================

def negate_op(op):
    """Negate an operator. Maps to its torus complement.
    On the torus with identification 7=0:
    VOID(0) <-> VOID(0)    (negation of nothing is nothing)
    LATTICE(1) <-> RESET(9) (structure <-> erasure)
    COUNTER(2) <-> BREATH(8) (counting <-> pausing)
    PROGRESS(3) <-> HARMONY(7) (forward <-> arrived)
    COLLAPSE(4) <-> CHAOS(6) (compression <-> disorder)
    BALANCE(5) <-> BALANCE(5) (center is its own negation)
    """
    if op == 0: return 0
    if op == 5: return 5  # BALANCE is self-dual
    return (10 - op) % 10


def intensify_op(op):
    """Intensify = self-composition through BHML.
    BHML[op][op] pushes the operator toward its successor.
    """
    return BHML[op][op]


def diminish_op(op):
    """Diminish = compose with BALANCE (5) to center.
    BHML[op][5] pulls toward the middle.
    """
    return BHML[op][5]


def compose_ops(op1, op2):
    """Compose two operators through BHML (physics/doing)."""
    return BHML[op1][op2]


def measure_ops(op1, op2):
    """Measure two operators through TSML (being/measurement)."""
    return TSML[op1][op2]


class SemanticModifiers:
    """Translates English modifiers into CL operations.

    CK already has the algebra. This tells him which English
    words trigger which algebraic operations.
    """

    def __init__(self):
        # Learned antonym pairs (beyond seed list)
        self.learned_antonyms = {}
        # Word -> base semantic key (before modifiers)
        self.word_semantics = {}
        # Load seed antonyms
        for w1, w2 in ANTONYM_PAIRS:
            self.learned_antonyms[w1] = w2
            self.learned_antonyms[w2] = w1

    def detect_modifiers(self, words):
        """Scan word list for modifiers. Returns list of
        (index, modifier_type, target_word_index) tuples.

        modifier_type: 'negate', 'intensify', 'diminish'
        """
        results = []
        for i, word in enumerate(words):
            w = word.lower().strip('.,!?;:')
            if w in NEGATION_WORDS and i + 1 < len(words):
                results.append((i, 'negate', i + 1))
            elif w in INTENSIFIER_WORDS and i + 1 < len(words):
                results.append((i, 'intensify', i + 1))
            elif w in DIMINISHER_WORDS and i + 1 < len(words):
                results.append((i, 'diminish', i + 1))
        return results

    def detect_negation_prefix(self, word):
        """Check if word has a negation prefix.
        'unhappy' -> ('un', 'happy')
        'impossible' -> ('im', 'possible')
        """
        w = word.lower()
        for prefix in sorted(NEGATION_PREFIXES, key=len, reverse=True):
            if w.startswith(prefix) and len(w) > len(prefix) + 2:
                return (prefix, w[len(prefix):])
        return None

    def apply_modifier(self, modifier_type, op):
        """Apply a modifier to an operator.

        'negate': flip to torus complement
        'intensify': self-compose through BHML
        'diminish': compose with BALANCE
        """
        if modifier_type == 'negate':
            return negate_op(op)
        elif modifier_type == 'intensify':
            return intensify_op(op)
        elif modifier_type == 'diminish':
            return diminish_op(op)
        return op

    def process_text(self, words, ops):
        """Process a word list with its operator decomposition.
        Apply modifiers to produce MODIFIED operator sequence.

        Returns: list of (word, original_op, modified_op, modifier_type)
        """
        if len(words) != len(ops):
            return list(zip(words, ops, ops, [None] * len(ops)))

        modified_ops = list(ops)
        modifiers_applied = [None] * len(ops)

        # Detect and apply modifiers
        mods = self.detect_modifiers(words)
        for mod_idx, mod_type, target_idx in mods:
            if target_idx < len(modified_ops):
                original = modified_ops[target_idx]
                modified_ops[target_idx] = self.apply_modifier(
                    mod_type, original)
                modifiers_applied[target_idx] = mod_type

        # Check for negation prefixes
        for i, word in enumerate(words):
            prefix_result = self.detect_negation_prefix(word)
            if prefix_result and modifiers_applied[i] is None:
                modified_ops[i] = negate_op(modified_ops[i])
                modifiers_applied[i] = 'negate_prefix'

        return list(zip(words, ops, modified_ops, modifiers_applied))

    def compose_pair(self, word1_op, word2_op):
        """Compose two words' operators through BHML.
        For compound words: 'fire truck' = BHML[fire_op][truck_op]
        """
        return compose_ops(word1_op, word2_op)

    def is_antonym(self, word1, word2):
        """Check if two words are known antonyms."""
        w1, w2 = word1.lower(), word2.lower()
        return (self.learned_antonyms.get(w1) == w2 or
                self.learned_antonyms.get(w2) == w1)

    def learn_antonym(self, word1, word2):
        """Record that word1 and word2 are semantic opposites."""
        w1, w2 = word1.lower(), word2.lower()
        self.learned_antonyms[w1] = w2
        self.learned_antonyms[w2] = w1

    def get_antonym_op(self, word):
        """Get the expected operator for a word's antonym."""
        w = word.lower()
        if w in self.word_semantics:
            return negate_op(self.word_semantics[w])
        return None

    def save(self, path=None):
        """Persist learned antonyms and word semantics."""
        import json, os
        if path is None:
            path = os.path.expanduser('~/.ck/semantic_modifiers.json')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump({
                'learned_antonyms': self.learned_antonyms,
                'word_semantics': self.word_semantics,
            }, f)

    def load(self, path=None):
        """Load from disk."""
        import json, os
        if path is None:
            path = os.path.expanduser('~/.ck/semantic_modifiers.json')
        if not os.path.exists(path):
            return
        try:
            with open(path) as f:
                data = json.load(f)
            self.learned_antonyms.update(data.get('learned_antonyms', {}))
            self.word_semantics.update(data.get('word_semantics', {}))
        except Exception:
            pass


    def classify_tig_bin(self, word, pos=None):
        """Classify a word into Being/Doing/Becoming TIG bin.

        Being (0): nouns, numbers, states, identities
        Doing (1): verbs, operations, actions, modifiers
        Becoming (2): transitions, results, compounds, conjunctions

        Returns: int (0, 1, or 2)
        """
        w = word.lower().strip('.,!?;:')

        # Punctuation
        if w in PUNCTUATION_OPS:
            return TIG_BINS['being']  # punctuation is structural

        # Math symbols
        if w in MATH_OPS:
            table, role = MATH_OPS[w]
            if role == 'measure':
                return TIG_BINS['being']
            elif role in ('compose', 'iterate', 'negate_compose'):
                return TIG_BINS['doing']
            return TIG_BINS['becoming']

        # Digits are Being (they ARE quantities)
        if w.isdigit():
            return TIG_BINS['being']

        # If POS tag provided, use it
        if pos:
            op_info = POS_TO_OPERATION.get(pos)
            if op_info:
                _, role = op_info
                if role in ('being', 'scope'):
                    return TIG_BINS['being']
                elif role in ('doing', 'modify_doing'):
                    return TIG_BINS['doing']
                elif role in ('modify_being', 'compose'):
                    return TIG_BINS['becoming']

        # Conjunctions are Becoming (they compose transitions)
        if w in CONJUNCTION_OPS:
            return TIG_BINS['becoming']

        # Modifiers are Doing (they change things)
        if w in NEGATION_WORDS or w in INTENSIFIER_WORDS or w in DIMINISHER_WORDS:
            return TIG_BINS['doing']

        # Default: Being (most words are things/concepts)
        return TIG_BINS['being']

    def get_punctuation_op(self, char):
        """Get operator for a punctuation character."""
        return PUNCTUATION_OPS.get(char, 5)  # default BALANCE

    def get_conjunction_type(self, word):
        """Get CL operation type for a conjunction."""
        return CONJUNCTION_OPS.get(word.lower(), 'bhml')

    def get_math_operation(self, symbol):
        """Get CL table and role for a math symbol."""
        return MATH_OPS.get(symbol, ('bhml', 'compose'))

    def text_to_tig_sequence(self, words):
        """Convert a word list to a Being/Doing/Becoming sequence.

        Returns list of (word, tig_bin) tuples.
        This IS the TIG lens view of the text.
        """
        return [(w, self.classify_tig_bin(w)) for w in words]


def build_semantic_modifiers():
    """Create and load the modifier system."""
    sm = SemanticModifiers()
    sm.load()
    return sm
