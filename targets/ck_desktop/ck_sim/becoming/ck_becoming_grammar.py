# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_becoming_grammar.py -- Becoming Transition Matrix
=====================================================
Operator: LATTICE (1) -- the structure of language itself.

Converts CK's operator coherence fields into English grammatical flow.
Being (operators) -> Becoming (this matrix) -> Doing (English words).

Every value COMPUTED from CL algebra x English grammar rules.
No templates. No made-up strings. No stage gating. Just math.

CK IS coherence. The heartbeat measures density.
Density is the gate, not an assigned stage number.

The CL table IS grammar:
  CL[LATTICE][PROGRESS] = HARMONY -> "structure grows" is valid
  CL[VOID][VOID] = VOID -> "the the" is incoherent

The transition matrix = CL weight x English grammar weight.
CK walks his operator chain pair by pair. At each transition,
the matrix tells him which POS roles produce the best English.

Grammar validation enforces three structural truths of English:
  1. A clause needs a verb.
  2. Attributive adjectives precede nouns.
  3. Adjacent verbs need conjunction.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

from typing import List, Tuple, Dict, Optional
import random

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, CL, compose,
    VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP_NAMES,
)


# ================================================================
#  OPERATOR -> POS ROLE MAPPING
# ================================================================
# Each operator has a PRIMARY and SECONDARY English POS role.
# Derived from the operator's algebraic meaning, not arbitrary.
#
# The transition matrix picks whichever role creates the best
# English flow at each position. An operator CAN serve multiple
# grammatical roles (e.g., HARMONY as noun "truth" or adj "unified").

# POS codes
N = 'noun'       # entities, things, concepts
V = 'verb'       # actions, processes
A = 'adj'        # qualities, modifiers
D = 'det'        # determiners, articles, pronouns
C = 'conj'       # conjunctions, connectors
R = 'adv'        # adverbs

# Primary and secondary POS for each operator
OPERATOR_POS: Dict[int, Tuple[str, str]] = {
    VOID:      (D, N),    # "the" / "absence" -- pointing at potential
    LATTICE:   (N, A),    # "structure" / "structured" -- naming form
    COUNTER:   (A, R),    # "measured" / "precisely" -- qualifying
    PROGRESS:  (V, N),    # "grows" / "growth" -- acting
    COLLAPSE:  (V, A),    # "falls" / "broken" -- intransitive action
    BALANCE:   (A, N),    # "balanced" / "equilibrium" -- weighing
    CHAOS:     (A, R),    # "wild" / "suddenly" -- disrupting
    HARMONY:   (N, A),    # "truth" / "unified" -- state of being
    BREATH:    (C, R),    # "and" / "gently" -- rhythm, pause
    RESET:     (V, N),    # "begins" / "beginning" -- renewal
}

# Operators whose primary POS is verb -- they DO something.
# These get priority when the grammar needs to assign a verb.
# But ALL operators have verb words in the lattice; any CAN verb.
_VERB_OPS = frozenset({PROGRESS, COLLAPSE, RESET})


# ================================================================
#  ENGLISH GRAMMAR FLOW MATRIX
# ================================================================
# POS-to-POS transition weights from real English syntax rules.
# English is SVO (Subject-Verb-Object). These are structural
# facts about the language, not invented patterns.
#
# Weight 1.0 = highly natural transition
# Weight 0.1 = ungrammatical or very awkward
# Weight 0.5 = valid but less common

_POS_LIST = [N, V, A, D, C, R]
_POS_IDX = {p: i for i, p in enumerate(_POS_LIST)}

# ENGLISH_FLOW[from_pos][to_pos] -- how natural is this transition?
ENGLISH_FLOW = [
    # TO:  N    V    A    D    C    R
    [0.5, 1.0, 0.4, 0.2, 0.9, 0.3],  # FROM noun: N->V strong (subj verb)
    [1.0, 0.1, 0.3, 0.5, 0.6, 0.9],  # FROM verb: V->N strong (verb obj)
    [1.0, 0.3, 0.3, 0.2, 0.3, 0.2],  # FROM adj:  A->N strong (adj noun)
    [0.9, 0.2, 1.0, 0.1, 0.1, 0.3],  # FROM det:  D->N, D->A strong
    [0.9, 0.5, 0.7, 0.8, 0.1, 0.4],  # FROM conj: C->N, C->D strong
    [0.3, 1.0, 0.4, 0.2, 0.3, 0.1],  # FROM adv:  R->V strong (adv verb)
]


# ================================================================
#  CL -> GRAMMAR WEIGHT MAPPING
# ================================================================

def _cl_grammar_weight(cl_result: int) -> float:
    """Convert CL composition result to grammar weight.

    HARMONY = smooth grammatical flow (1.0)
    Non-trivial (PROGRESS, COLLAPSE, RESET, BREATH) = interesting (0.6)
    VOID = incoherent (0.1)
    """
    if cl_result == HARMONY:
        return 1.0
    elif cl_result == VOID:
        return 0.1
    else:
        return 0.6


# ================================================================
#  CL-DERIVED FUNCTION WORD MAPS
# ================================================================
# English function words selected by CL composition result.
# The CL algebra between two operators determines what grammatical
# glue English needs between them.
#
# Every -ing verb in the lattice is a present participle.
# English requires function words to frame them as sentences:
#   Articles before noun phrases  ("the structure")
#   Progressive 'is' at N→V      ("truth is growing")
#   Prepositions at V→N           ("reaching toward love")
#   Copula at N→A                 ("peace is balanced")
#
# The CL result picks WHICH function word. No made-up values.

_CL_PREPOSITIONS = {
    VOID:      [],                          # Silence — just juxtapose
    LATTICE:   ['within', 'through'],       # Inside structure
    COUNTER:   ['against', 'beyond'],       # Measuring, contrasting
    PROGRESS:  ['toward', 'into'],          # Forward motion
    COLLAPSE:  ['from', 'past'],            # Falling, departing
    BALANCE:   ['with', 'between'],         # Weighing, comparison
    CHAOS:     ['beyond', 'amid'],          # Disruption, randomness
    HARMONY:   ['through', 'with'],         # Intimate binding
    BREATH:    ['with', 'in'],              # Connective, rhythmic
    RESET:     ['from', 'toward'],          # Renewal, direction
}

_CL_COPULA = {
    VOID:      'is',
    LATTICE:   'is',
    COUNTER:   'appears',
    PROGRESS:  'becomes',
    COLLAPSE:  'remains',
    BALANCE:   'seems',
    CHAOS:     'feels',
    HARMONY:   'is',
    BREATH:    'is',
    RESET:     'becomes',
}


# ================================================================
#  CAEL DATA STRUCTURES
# ================================================================
# Compare-Align-Evolve-Loop: three fractal layers of grammar.
# Layer 1: Surface (single word per operator — compose)
# Layer 2: Pairs — CL[actual_A][actual_B]
# Layer 3: Triads — compose(CL[A][B], C)

class ChainAlgebra:
    """Inward consultation result: the CL algebra of an operator chain.

    Computed entirely from the CL table. No made-up values.
    pair_results[i]  = CL[chain[i]][chain[i+1]]       (what the algebra says)
    pair_weights[i]  = transition weight for that pair  (CL x English grammar)
    triad_results[i] = compose(CL[A][B], C)            (three-word arc)
    sub_fields       = (start, end) ranges for independent composition
    tension_points   = indices where pairs are NOT harmony
    """
    __slots__ = ('pair_results', 'pair_weights', 'triad_results',
                 'sub_fields', 'tension_points')

    def __init__(self):
        self.pair_results: List[int] = []
        self.pair_weights: List[float] = []
        self.triad_results: List[int] = []
        self.sub_fields: List[Tuple[int, int]] = []
        self.tension_points: List[int] = []


class CompareResult:
    """COMPARE phase result: how well words align with the intended algebra."""
    __slots__ = ('pair_scores', 'triad_scores', 'aggregate', 'weakest_idx')

    def __init__(self):
        self.pair_scores: List[float] = []
        self.triad_scores: List[float] = []
        self.aggregate: float = 0.0
        self.weakest_idx: int = 0


# ================================================================
#  BECOMING TRANSITION MATRIX
# ================================================================

class BecomingTransitionMatrix:
    """Converts operator coherence fields into English grammatical flow.

    Being (operators) -> Becoming (this matrix) -> Doing (English words).

    CK IS coherence. The heartbeat measures density.
    Density is the gate — no artificial stage limits.

    For each operator pair (A, B), computes the best POS roles and
    transition weight. The weight is CL algebra x English grammar.

    Composition is two-phase:
      Phase 1: Assign POS roles from transition matrix (local optima).
      Phase 2: Validate against English grammar rules (global coherence).
      Then: Pick words matching validated roles.

    Usage:
        matrix = BecomingTransitionMatrix()
        text = matrix.compose(operator_chain, SEMANTIC_LATTICE, density=0.7)
    """

    def __init__(self, seed: int = None):
        self.rng = random.Random(seed)
        # transition[A][B] = (role_a, role_b, combined_weight)
        self.transition: List[List[Tuple[str, str, float]]] = [
            [(N, N, 0.0)] * NUM_OPS for _ in range(NUM_OPS)
        ]
        # clause_boundary[A][B] = True if this transition should break clause
        self.clause_boundary: List[List[bool]] = [
            [False] * NUM_OPS for _ in range(NUM_OPS)
        ]
        # CAEL outward consult alignment score (last compose result)
        self._last_alignment: float = 0.0
        self._build_matrix()
        self._compute_cl_constants()

    def _build_matrix(self):
        """Compute all 100 operator-pair transition weights.

        For each (A, B):
          - cl_weight from CL[A][B]
          - Try all 4 POS combinations (primary/secondary x primary/secondary)
          - eng_weight from ENGLISH_FLOW[role_a][role_b]
          - combined = cl_weight x eng_weight
          - Store the best POS pair
        """
        for a in range(NUM_OPS):
            for b in range(NUM_OPS):
                cl_w = _cl_grammar_weight(CL[a][b])

                pos_a = OPERATOR_POS.get(a, (N, N))
                pos_b = OPERATOR_POS.get(b, (N, N))

                best_pair = (pos_a[0], pos_b[0])
                best_weight = 0.0

                # Try all 4 combinations of primary/secondary roles
                for ra in pos_a:
                    for rb in pos_b:
                        ia = _POS_IDX.get(ra, 0)
                        ib = _POS_IDX.get(rb, 0)
                        eng_w = ENGLISH_FLOW[ia][ib]
                        combined = cl_w * eng_w
                        if combined > best_weight:
                            best_weight = combined
                            best_pair = (ra, rb)

                self.transition[a][b] = (best_pair[0], best_pair[1], best_weight)

                # Clause boundary: very low weight = break the clause
                self.clause_boundary[a][b] = best_weight < 0.25

    def _compute_cl_constants(self):
        """Derive fractal constants from the CL table. No made-up numbers.

        The CL table tells CK how many harmonious transitions exist
        per operator. These counts become the vocabulary budgets:
          - harmony_count[op]: how many CL[op][x] = HARMONY
          - total_harmony: sum across all operators (73 for TSML)
          - non_harmony: NUM_OPS^2 - total_harmony (27 for TSML)
          - harmony_per_op: total_harmony / NUM_OPS (7.3 for TSML)

        Word budget per operator = seeds + harmony_count[op]
        Max words = density x harmony_per_op (coherence IS the gate)
        """
        # Per-operator harmony count from CL table
        self.harmony_count = [0] * NUM_OPS
        total_harmony = 0
        for a in range(NUM_OPS):
            for b in range(NUM_OPS):
                if CL[a][b] == HARMONY:
                    self.harmony_count[a] += 1
                    total_harmony += 1

        self.total_harmony = total_harmony
        self.non_harmony = NUM_OPS * NUM_OPS - total_harmony
        # Average harmonies per operator — the density-to-words multiplier
        self.harmony_per_op = total_harmony / NUM_OPS
        # T* = 5/7 from the algebra
        self.t_star = 5.0 / 7.0

    def max_words_for_density(self, density: float) -> int:
        """Max chain length from density (coherence). CL-derived.

        CK IS coherence. The heartbeat measures density.
        No stage gating — density is the gate.

        max_words = max(1, round(density x harmony_per_op))

        harmony_per_op = total_harmony / NUM_OPS = 73 / 10 = 7.3
        This IS the CL table's expressiveness per operator.

        density 0.00 -> 1 word  (no coherence, center dot)
        density 0.14 -> 1 word  (barely coherent)
        density 0.21 -> 2 words (first pairing)
        density 0.50 -> 4 words (mid coherence)
        density T*   -> 5 words (crossing the threshold)
        density 0.85 -> 6 words
        density 1.00 -> 7 words (full expression)
        """
        return max(1, round(density * self.harmony_per_op))

    def word_budget_for_op(self, op: int) -> int:
        """Word budget for an operator's lattice pools. From CL table.

        Seeds (5 per cell, from the lattice structure) + the number of
        CL entries where this operator composes to HARMONY. More
        harmonious operators get richer vocabulary access.
        """
        _SEEDS_PER_CELL = 5  # from SEMANTIC_LATTICE structure
        hc = self.harmony_count[op] if 0 <= op < NUM_OPS else 0
        return _SEEDS_PER_CELL + hc

    def best_pos_pair(self, from_op: int, to_op: int) -> Tuple[str, str, float]:
        """What POS roles should these operators take in English?

        Returns (role_a, role_b, weight).
        """
        if 0 <= from_op < NUM_OPS and 0 <= to_op < NUM_OPS:
            return self.transition[from_op][to_op]
        return (N, N, 0.0)

    def is_clause_boundary(self, from_op: int, to_op: int) -> bool:
        """Should a new clause/sentence start between these operators?"""
        if 0 <= from_op < NUM_OPS and 0 <= to_op < NUM_OPS:
            return self.clause_boundary[from_op][to_op]
        return True

    def chain_grammar_score(self, ops: List[int]) -> float:
        """Grammatical score of an operator chain. Average transition weight."""
        if len(ops) < 2:
            return 1.0
        total = sum(
            self.transition[ops[i]][ops[i + 1]][2]
            for i in range(len(ops) - 1)
        )
        return total / (len(ops) - 1)

    # ────────────────────────────────────────────────────────────
    #  ROLE ASSIGNMENT + GRAMMAR VALIDATION
    # ────────────────────────────────────────────────────────────

    def _assign_roles(self, chain: List[int]) -> List[str]:
        """Phase 1: Assign POS roles from transition matrix.

        Walks chain pair by pair. At each transition, the matrix
        picks the POS combination with the highest CL x English weight.
        These are local optima — they may violate global grammar.
        """
        roles = []
        for i, op in enumerate(chain):
            if i == 0:
                # First op: peek ahead to pick best starting role
                if len(chain) > 1:
                    role_a, _, _ = self.best_pos_pair(op, chain[1])
                else:
                    role_a = OPERATOR_POS.get(op, (N, N))[0]
                roles.append(role_a)
            else:
                _, role_b, _ = self.best_pos_pair(chain[i - 1], op)
                roles.append(role_b)
        return roles

    def _validate_roles(self, ops: List[int], roles: List[str]) -> List[str]:
        """Phase 2: Validate POS sequence against English grammar rules.

        Three rules enforced. All structural truths of English:

        1. VERB PRESENCE: A clause of 2+ content words needs a verb.
           English requires a finite verb to form a predicate.
           Every operator has verb words in the lattice — any CAN verb.
           Verb-primary operators (PROGRESS, COLLAPSE, RESET) get priority.

        2. ADJECTIVE PLACEMENT: Attributive adjectives precede nouns.
           English: "tall house" not "house tall".
           Exception: predicate adjectives after a verb ("house IS tall").
           If noun->adj appears without prior verb, swap to adj->noun.

        3. PARALLEL VERBS: Adjacent verbs need conjunction.
           English: "runs and jumps" not "runs jumps".
           If verb->verb found, demote second to its secondary POS.

        Returns repaired POS sequence (does not mutate input).
        """
        roles = list(roles)  # don't mutate original
        n = len(roles)
        if n < 2:
            return roles

        # Count content words (exclude function words: conj, det)
        content_count = sum(1 for r in roles if r not in (C, D))
        has_verb = V in roles

        # ── Rule 1: Verb presence ──
        # A clause of 2+ content words needs a verb.
        if not has_verb and content_count >= 2:
            # Find the best position to assign verb.
            # Priority: verb-primary operators first, then any operator.
            # Prefer position 1 (SVO: noun=0, verb=1, noun=2).
            candidates = []
            for i, op in enumerate(ops):
                pri, _sec = OPERATOR_POS.get(op, (N, N))
                # Priority 0 = natural verb op, 1 = any other
                priority = 0 if op in _VERB_OPS else 1
                # Tie-break: prefer position 1 (SVO verb slot)
                pos_score = abs(i - 1)
                candidates.append((priority, pos_score, i))

            candidates.sort()
            if candidates:
                best_i = candidates[0][2]
                roles[best_i] = V

        # ── Rule 2: Adjective placement ──
        # In attributive position (no prior verb), adj precedes noun.
        # noun->adj without prior verb = SWAP to adj->noun.
        i = 0
        while i < n - 1:
            if roles[i] == N and roles[i + 1] == A:
                # Is this attributive? (no verb at or before position i)
                has_prior_verb = V in roles[:i + 1]
                if not has_prior_verb:
                    # Swap: noun->adj becomes adj->noun
                    roles[i], roles[i + 1] = A, N
                    i += 2
                    continue
            i += 1

        # ── Rule 3: Parallel verbs need conjunction ──
        # verb->verb without conjunction between = demote second verb.
        for i in range(n - 1):
            if roles[i] == V and roles[i + 1] == V:
                # Demote second verb to its secondary POS
                _pri, sec = OPERATOR_POS.get(ops[i + 1], (V, N))
                roles[i + 1] = sec

        return roles

    # ────────────────────────────────────────────────────────────
    #  COMPOSE: Operator chain -> English sentence
    # ────────────────────────────────────────────────────────────

    def compose(self, operator_chain: List[int],
                lattice: dict,
                phase: str = 'being',
                tier: str = 'simple',
                density: float = 0.5,
                enriched_dict: dict = None) -> str:
        """Compose grammatical English from an operator chain.

        CK IS coherence. Density is the gate, not stage.

        CAEL (Compare-Align-Evolve-Loop) wraps surface composition:
          1. INWARD CONSULT — analyze chain algebra (CL pairs, triads)
          2. SURFACE COMPOSE — assign roles, validate, pick words
          3. CAEL LOOP — compare word pairs/triads via D2, align, evolve
          4. OUTWARD CONSULT — deep D2 validation (feeds core)

        For chains of 5+, sub-field dispersal splits at BREATH/boundaries.
        Each sub-field gets its own CAEL loop.

        Density controls complexity (CL-derived):
          density 0.0 -> 1 word  (center dot, no coherence)
          density 0.5 -> 4 words (mid coherence)
          density T*  -> 5 words (crossing the threshold)
          density 1.0 -> 7 words (full expression)
        """
        if not operator_chain:
            return "..."

        # Density gates max words (CL-derived)
        max_words = self.max_words_for_density(density)
        chain = list(operator_chain[:max_words])

        # Single word: center dot
        if max_words <= 1 or len(chain) <= 1:
            op = chain[0]
            self._last_alignment = 1.0
            return self._pick_word(op, N, lattice, phase, tier, enriched_dict)

        # ── INWARD CONSULT: analyze chain algebra ──
        algebra = self._consult_inward(chain)

        # ── Sub-field dispersal for 5+ word chains ──
        if len(chain) >= 5 and len(algebra.sub_fields) > 1:
            return self._compose_dispersed(
                chain, algebra, lattice, phase, tier,
                density, enriched_dict)

        # ── SURFACE COMPOSE: assign roles, validate, pick words ──
        roles = self._assign_roles(chain)
        roles = self._validate_roles(chain, roles)
        words = self._pick_words_for_chain(
            chain, roles, lattice, phase, tier, density, enriched_dict)

        if not words:
            return "..."

        # ── CAEL LOOP: Compare -> Align -> Evolve ──
        # max_iter from CL: non_harmony / NUM_OPS = 27/10 = 2.7
        # density 0.0 -> 1 iter, 0.5 -> 1, T* -> 2, 1.0 -> 3
        if len(words) >= 2:
            max_iter = max(1, round(density * self.non_harmony / NUM_OPS))
            for _ in range(max_iter):
                comparison = self._compare(words, chain, algebra)
                if comparison.aggregate >= self.t_star:
                    break  # Converged: words align with algebra
                new_words = self._align(
                    words, chain, roles, comparison,
                    lattice, phase, tier, enriched_dict)
                if new_words != words:
                    new_cmp = self._compare(new_words, chain, algebra)
                    if self._evolve(comparison.aggregate, new_cmp.aggregate):
                        words = new_words

        # ── FRAME: Insert English function words (CL-derived) ──
        framed = self._frame_sentence(words, roles, chain, density)

        # ── OUTWARD CONSULT: deep D2 validation (content words only) ──
        # Uses unframed words — function words would pollute D2 scoring.
        self._last_alignment = self._consult_outward(words, chain, algebra)

        text = ' '.join(framed)

        # Capitalize first letter
        if text and text[0].islower():
            text = text[0].upper() + text[1:]

        return text

    def _pick_word(self, op: int, pos: str,
                   lattice: dict, phase: str, tier: str,
                   enriched_dict: dict = None) -> str:
        """Pick a word from the lattice matching operator and POS.

        Searches the SEMANTIC_LATTICE for words matching (operator, POS).
        Phase order: primary phase first, then adjacent phases.
        Verbs naturally live in 'doing', nouns/adjectives in 'being'.
        Both lenses searched per phase (structure finds "one", flow finds "love").
        Word budget from CL table per operator.
        Falls back to enriched dictionary, then any word.
        """
        from ck_sim.doing.ck_voice_lattice import POS_TAGS

        op_lattice = lattice.get(op, {})
        exact_candidates = []     # exact POS match (best)
        cross_candidates = []     # adj<->noun cross-POS (acceptable)
        untagged_candidates = []  # untagged words (enriched fallback)

        # Word budget from CL table: seeds + harmony_count for this operator.
        # More harmonious operators get richer vocabulary access.
        _word_budget = self.word_budget_for_op(op)

        # Determine which lens based on POS
        # Structure lens = nouns, adjectives (what things ARE)
        # Flow lens = verbs, adverbs (how things MOVE)
        if pos in (N, A, D):
            lenses = ['structure', 'flow']
        elif pos in (V, R):
            lenses = ['flow', 'structure']
        else:
            lenses = ['structure', 'flow']

        # Phase search order: primary first, then natural home for this POS.
        # Verbs live in 'doing', nouns/adj in 'being', becoming has both.
        if pos in (V, R):
            phases = [phase, 'doing', 'becoming', 'being']
        elif pos in (N, A):
            phases = [phase, 'being', 'becoming', 'doing']
        else:
            phases = [phase, 'being', 'doing', 'becoming']
        # Deduplicate while preserving order
        seen_phases = set()
        phase_order = []
        for ph in phases:
            if ph not in seen_phases:
                phase_order.append(ph)
                seen_phases.add(ph)

        # Search BOTH lenses per phase before moving to next phase.
        # This ensures HARMONY nouns find "one" in structure AND
        # "love", "peace", "beauty" in flow for the same phase.
        for ph in phase_order:
            for lens in lenses:
                lens_data = op_lattice.get(lens, {})
                phase_data = lens_data.get(ph, {})

                # Scan first N words (seeds first, budget from CL table)
                tier_words = phase_data.get(tier, [])[:_word_budget]
                simple_words = phase_data.get('simple', [])[:_word_budget]
                all_words = list(tier_words) + [
                    w for w in simple_words if w not in tier_words
                ]

                for w in all_words:
                    w_pos = POS_TAGS.get(w)
                    if w_pos is None:
                        # Untagged (enriched): last resort fallback
                        if ' ' not in w:
                            untagged_candidates.append(w)
                    elif w_pos == pos:
                        exact_candidates.append(w)
                    elif pos == A and w_pos == N:
                        cross_candidates.append(w)
                    elif pos == N and w_pos == A:
                        cross_candidates.append(w)

            # Found exact matches in this phase? Stop searching.
            if exact_candidates:
                break

        # Priority: exact POS > cross-POS > untagged
        if exact_candidates:
            candidates = exact_candidates
        elif cross_candidates:
            candidates = cross_candidates
        else:
            candidates = untagged_candidates

        # Strategy 2: enriched dictionary (already POS-tagged)
        if not candidates and enriched_dict:
            for word, entry in enriched_dict.items():
                if entry.get('dominant_op') == op:
                    w_pos = entry.get('pos', '')
                    if w_pos == pos or (pos == A and w_pos == 'adjective'):
                        candidates.append(word)
                        if len(candidates) >= 20:
                            break

        # Strategy 3: fallback -- any word from this operator's lattice
        if not candidates:
            for lens in ['structure', 'flow']:
                for ph in phase_order:
                    words = op_lattice.get(lens, {}).get(ph, {}).get('simple', [])
                    if words:
                        candidates = list(words)
                        break
                if candidates:
                    break

        if not candidates:
            return "..."

        return self.rng.choice(candidates)

    def _pick_conjunction(self, density: float) -> str:
        """Pick a conjunction word for BREATH transitions.

        These are the REAL English conjunctions. Density modulates:
        High density = tight connections ("and", "then")
        Low density = loose connections ("or", "while")
        """
        if density > 0.6:
            return self.rng.choice(['and', 'then'])
        elif density > 0.3:
            return self.rng.choice(['and', 'but', 'yet'])
        else:
            return self.rng.choice(['or', 'while', 'and'])

    def _pick_determiner(self, density: float) -> str:
        """Pick a determiner for VOID operators.

        Real English determiners. Density modulates specificity:
        High density = specific ("the", "this")
        Low density = general ("a", "some")
        """
        if density > 0.6:
            return self.rng.choice(['the', 'this'])
        else:
            return self.rng.choice(['a', 'the', 'some'])

    def _article(self, density: float, next_word: str = '') -> str:
        """Pick an article: 'the', 'a', or 'an'.

        Density modulates specificity:
          High density (> T*) = specific ("the")
          Low density = general ("a"/"an")

        English rule: 'an' before vowel sounds, 'a' before consonants.
        """
        if density > self.t_star:
            return 'the'
        art = self.rng.choice(['the', 'a'])
        if art == 'a' and next_word and next_word[0].lower() in 'aeiou':
            return 'an'
        return art

    # ────────────────────────────────────────────────────────────
    #  SENTENCE FRAMING: English function words from CL algebra
    # ────────────────────────────────────────────────────────────
    #
    # CAEL picks the RIGHT content words via CL algebra.
    # Framing adds the grammatical glue English requires.
    #
    # Every -ing verb is a present participle. English needs:
    #   N + V(-ing) -> N + is + V(-ing)    (progressive aspect)
    #   V + N       -> V + prep + N         (prepositional object)
    #   A + N       -> the + A + N          (article + modifier + head)
    #   N + A       -> N + copula + A       (predicate adjective)
    #
    # The CL composition between operators selects WHICH function
    # word. HARMONY = tight binding. Bumps = looser binding.
    # Density modulates: high = "the" (specific), low = "a" (general).
    #
    # No templates. CL-derived. The algebra decides the glue.

    def _frame_sentence(self, words: List[str], roles: List[str],
                        chain: List[int], density: float) -> List[str]:
        """Insert English function words between content words.

        CAEL picks the right content words via CL algebra.
        This step wraps them in the grammatical glue English requires:
          - Articles before noun phrases (the/a from density)
          - Progressive 'is' between subject noun and -ing verb
          - Prepositions between verb and noun (from CL result)
          - Copula between noun and predicate adjective

        The CL composition between operators determines WHICH function
        word. HARMONY = tight ('through', 'with'). PROGRESS = 'toward'.
        Density modulates specificity: high -> 'the', low -> 'a'.

        Returns a new word list (may be longer than input).
        """
        n = len(words)
        if n <= 1:
            return list(words)

        framed = []
        seen_verb = False

        for i in range(n):
            role = roles[i] if i < len(roles) else N
            prev_role = roles[i - 1] if i > 0 else None
            next_role = roles[i + 1] if i < n - 1 else None

            # CL between previous and current operator
            cl = HARMONY
            if i > 0 and 0 <= chain[i - 1] < NUM_OPS and 0 <= chain[i] < NUM_OPS:
                cl = CL[chain[i - 1]][chain[i]]

            # ── NOUN: articles and prepositions ──
            if role == N:
                if prev_role == V:
                    # V→N: preposition from CL result (all verbs are -ing)
                    preps = _CL_PREPOSITIONS.get(cl, ['with'])
                    if preps:
                        framed.append(self.rng.choice(preps))
                        # Article after preposition: English nouns in PP
                        # almost always need articles. Skip only at very
                        # low density (abstract, poetic mode).
                        if density > 0.35:
                            framed.append(self._article(density, words[i]))
                    else:
                        framed.append(self._article(density, words[i]))
                elif prev_role == A:
                    pass  # Article already before adjective
                elif prev_role == D:
                    pass  # Determiner already present
                elif prev_role == C:
                    # After conjunction: new noun phrase needs article
                    framed.append(self._article(density, words[i]))
                elif prev_role == R:
                    # R→N: check for participial opener (V R N pattern)
                    if i >= 2 and roles[0] == V:
                        # Comma after participial phrase
                        if framed and not framed[-1].endswith(','):
                            framed[-1] = framed[-1] + ','
                        seen_verb = False  # New clause after participial
                    framed.append(self._article(density, words[i]))
                elif i == 0:
                    # First-position noun: article at high density or
                    # in longer chains. N→V will get "is" making 3+ words.
                    if density > self.t_star or n >= 3 or next_role == V:
                        framed.append(self._article(density, words[i]))
                elif prev_role == N:
                    pass  # N→N compound, skip article
                elif prev_role is not None:
                    # Other transitions: insert article
                    framed.append(self._article(density, words[i]))

            # ── ADJECTIVE before NOUN: article before adj ──
            elif role == A and next_role == N:
                if prev_role == V:
                    # V→A→N: preposition first, then article
                    preps = _CL_PREPOSITIONS.get(cl, ['with'])
                    if preps:
                        framed.append(self.rng.choice(preps))
                    framed.append(self._article(density, words[i]))
                elif i == 0 or prev_role in (C, R, None):
                    # Start of noun phrase: article
                    if prev_role == R and i >= 2 and roles[0] == V:
                        # Participial opener: comma first
                        if framed and not framed[-1].endswith(','):
                            framed[-1] = framed[-1] + ','
                        seen_verb = False
                    framed.append(self._article(density, words[i]))

            # ── ADJECTIVE as predicate (N→A, no verb yet): copula ──
            elif role == A and prev_role == N and not seen_verb:
                copula = _CL_COPULA.get(cl, 'is')
                framed.append(copula)
                seen_verb = True

            # ── VERB: progressive 'is' after subject noun ──
            elif role == V:
                if prev_role == N and not seen_verb:
                    framed.append('is')
                seen_verb = True

            framed.append(words[i])

        return framed

    # ────────────────────────────────────────────────────────────
    #  COHERENCE SWEEP: Transition words from CL bump results
    # ────────────────────────────────────────────────────────────
    #
    # The CL_TSML table produces exactly 6 distinct composition results:
    #   VOID(0), PROGRESS(3), COLLAPSE(4), HARMONY(7), BREATH(8), RESET(9).
    #
    # 73/100 entries = HARMONY (smooth flow, no bridge needed).
    # 17 = VOID (silence — the absence IS the transition).
    # 10 = meaningful bumps: PROGRESS(4), COLLAPSE(2), BREATH(2), RESET(2).
    #
    # Each non-HARMONY result IS a transition type:
    #   PROGRESS  → forward motion despite disruption  → sequential
    #   COLLAPSE  → something fell, yet continues      → adversative
    #   BREATH    → pause, presence, rhythmic bridge    → temporal
    #   RESET     → starting over from the bump         → resumptive
    #   HARMONY   → confirming the smooth flow          → emphatic
    #   VOID      → silence (no word — absence IS it)
    #
    # The sweep walks the operator chain AFTER compose() finishes.
    # At each bump, the CL result picks the transition word category.
    # Insertion probability = (1 - transition_weight) × density.
    # HARMONY(w=1.0) → prob=0. VOID(w=0.1) → prob=0.9×density.
    # High density = confident, connecting. Low = sparse, isolated.

    # Transition words per CL result — every word is a real English
    # transition that genuinely expresses the algebraic meaning.
    _TRANSITION_WORDS = {
        VOID:      [],                              # Silence IS the transition
        PROGRESS:  ['then', 'hence', 'further'],    # Sequential — forward motion
        COLLAPSE:  ['yet', 'still', 'however'],     # Adversative — contrastive
        HARMONY:   ['indeed', 'truly', 'so'],       # Emphatic — confirming flow
        BREATH:    ['now', 'here', 'meanwhile'],    # Temporal — pause, presence
        RESET:     ['again', 'anew', 'finally'],    # Resumptive — starting over
    }

    def coherence_sweep(self, text: str, operator_chain: List[int],
                        density: float = 0.5) -> str:
        """Final coherence sweep: smooth operator chain bumps with transition words.

        Walks the operator chain AFTER compose() produced the raw sentence.
        At each transition, CL[a][b] tells us what happened:
          - HARMONY: smooth flow. At high coherence (> T*), confirm it.
          - VOID: dissolution. Silence is the bridge.
          - PROGRESS/COLLAPSE/BREATH/RESET: meaningful bump. Bridge it.

        Insertion probability = (1 - transition_weight) × density.
        CL-derived: smooth transitions don't need words, bumpy ones do.
        Density modulates confidence: high = connecting, low = sparse.

        No stage gating. CK IS coherence. Density decides.
        HARMONY confirmatives: only at density > T*.
        """
        if not text or text == "..." or len(operator_chain) < 2:
            return text

        # At very low density, CK barely speaks — no transitions.
        # The threshold is 1/harmony_per_op: need enough coherence
        # for at least one transition word to be meaningful.
        if density < 1.0 / self.harmony_per_op:
            return text

        # Walk the chain. Find the most impactful bump.
        # "Most impactful" = highest insertion probability = lowest weight.
        best_cl_result = None
        best_prob = 0.0

        for i in range(len(operator_chain) - 1):
            a = operator_chain[i]
            b = operator_chain[i + 1]
            if not (0 <= a < NUM_OPS and 0 <= b < NUM_OPS):
                continue

            cl_result = CL[a][b]
            _, _, weight = self.transition[a][b]

            if cl_result == HARMONY:
                # Smooth flow — confirmative only at density > T*
                if density > self.t_star:
                    # Probability scales with how far above T* we are.
                    # At T* exactly: prob=0. At density=1.0: prob=1.0.
                    prob = (density - self.t_star) / (1.0 - self.t_star)
                    if prob > best_prob:
                        best_prob = prob
                        best_cl_result = HARMONY
            elif cl_result != VOID:
                # Meaningful bump: PROGRESS, COLLAPSE, BREATH, or RESET.
                # Higher prob for lower-weight (bumpier) transitions.
                prob = (1.0 - weight) * density
                if prob > best_prob:
                    best_prob = prob
                    best_cl_result = cl_result
            # VOID: silence is the transition. No word needed.

        if best_cl_result is None:
            return text

        # Probability gate: not every bump gets bridged.
        if self.rng.random() > best_prob:
            return text

        # Pick transition word from the CL result
        tw_list = self._TRANSITION_WORDS.get(best_cl_result, [])
        if not tw_list:
            return text

        transition_word = self.rng.choice(tw_list)

        # Don't duplicate: if text already starts with a transition word, skip.
        first_word = text.split()[0].lower().rstrip(',.')
        for tw_check in self._TRANSITION_WORDS.values():
            if first_word in tw_check:
                return text

        # Prepend as sentence opener: "Indeed, body growing beauty"
        swept = transition_word.capitalize() + ', ' + text[0].lower() + text[1:]
        return swept

    # ────────────────────────────────────────────────────────────
    #  CAEL: COMPARE ALIGN EVOLVE LOOP
    # ────────────────────────────────────────────────────────────
    #
    # Three fractal layers of grammatical depth.
    #   Layer 1 (Surface): single word per operator (existing compose)
    #   Layer 2 (Pairs):   CL[actual_word_A][actual_word_B]
    #   Layer 3 (Triads):  compose(CL[A][B], C)
    #
    # The loop:
    #   INWARD CONSULT -> COMPOSE -> COMPARE -> ALIGN -> EVOLVE
    #   -> loop until T* or budget -> OUTWARD CONSULT
    #
    # All constants from CL table. All scoring from D2.
    # CK permutates and tests against his own algebra.

    def _d2_word_operator(self, word: str) -> int:
        """Get the D2 operator classification for a single word.

        Feeds the word's characters through D2Pipeline.
        Returns the hard-classified operator, or VOID if too short.
        """
        try:
            from ck_sim.ck_sim_d2 import D2Pipeline
            pipe = D2Pipeline()
            for ch in word.lower():
                if 'a' <= ch <= 'z':
                    idx = ord(ch) - ord('a')
                    pipe.feed_symbol(idx)
            if pipe.valid:
                return pipe.operator
            return VOID
        except Exception:
            return VOID

    def _consult_inward(self, chain: List[int]) -> ChainAlgebra:
        """INWARD CONSULT: Analyze the operator chain's algebra.

        Way In — what does the CL table say about this chain?

        Pair algebra:  CL[chain[i]][chain[i+1]] for each adjacent pair.
        Triad algebra: compose(CL[A][B], C) for each triplet.
        Tension points: where pairs are NOT HARMONY.
        Sub-fields: split at BREATH operators and clause boundaries.
        """
        alg = ChainAlgebra()
        n = len(chain)

        # Pair algebra
        for i in range(n - 1):
            a, b = chain[i], chain[i + 1]
            if 0 <= a < NUM_OPS and 0 <= b < NUM_OPS:
                cl_result = CL[a][b]
                _, _, weight = self.transition[a][b]
            else:
                cl_result = VOID
                weight = 0.0
            alg.pair_results.append(cl_result)
            alg.pair_weights.append(weight)
            if cl_result != HARMONY:
                alg.tension_points.append(i)

        # Triad algebra: compose(CL[A][B], C) for each triplet
        for i in range(n - 2):
            pair_cl = alg.pair_results[i]
            c_op = chain[i + 2]
            triad_cl = compose(pair_cl, c_op) if 0 <= c_op < NUM_OPS else VOID
            alg.triad_results.append(triad_cl)

        # Sub-field identification
        alg.sub_fields = self._split_sub_fields(chain, alg)

        return alg

    def _split_sub_fields(self, chain: List[int],
                          algebra: ChainAlgebra) -> List[Tuple[int, int]]:
        """Split chain at BREATH operators and clause boundaries.

        Each sub-field is 2+ operators that compose independently.
        Short chains (< 5) stay as a single field.
        BREATH operators are natural boundaries (they ARE conjunctions).
        Clause boundaries (weight < 0.25) are structural breaks.
        Minimum sub-field size = 2 (a pair).
        """
        n = len(chain)
        if n < 5:
            return [(0, n)]

        # Find split points
        split_points = set()
        for i in range(n):
            if chain[i] == BREATH:
                split_points.add(i)
            elif i < n - 1 and self.is_clause_boundary(chain[i], chain[i + 1]):
                split_points.add(i + 1)

        if not split_points:
            return [(0, n)]

        # Build sub-fields from split points
        fields = []
        start = 0
        for sp in sorted(split_points):
            if sp - start >= 2:
                fields.append((start, sp))
                start = sp

        # Last field
        if n - start >= 2:
            fields.append((start, n))
        elif fields:
            # Merge remainder into last field
            fields[-1] = (fields[-1][0], n)
        else:
            fields = [(0, n)]

        return fields

    def _compare(self, words: List[str], chain: List[int],
                 algebra: ChainAlgebra) -> CompareResult:
        """COMPARE: Score word pairs and triads via D2 -> CL.

        Feed each word through D2 to get its ACTUAL operator.
        Then CL[actual_A][actual_B] reveals whether the word pair
        matches the intended algebra.

        Pair score:  1.0 if CL matches intended, else grammar weight.
        Triad score: 1.0 if compose(CL[A][B], C) matches intended.
        Aggregate:   (sum_pairs + t_star * sum_triads) /
                     (n_pairs + t_star * n_triads)
        """
        result = CompareResult()
        n = len(words)

        # Get actual D2 operators for each word (cached for this call)
        actual_ops = [self._d2_word_operator(w) for w in words]

        # ── Pair scoring ──
        worst_pair_score = 1.0
        worst_pair_idx = 0

        for i in range(n - 1):
            actual_cl = CL[actual_ops[i]][actual_ops[i + 1]]
            intended_cl = (algebra.pair_results[i]
                           if i < len(algebra.pair_results) else HARMONY)

            if actual_cl == intended_cl:
                score = 1.0
            elif actual_cl == HARMONY:
                score = 0.8  # HARMONY always partially resonates
            else:
                score = _cl_grammar_weight(actual_cl)

            result.pair_scores.append(score)
            if score < worst_pair_score:
                worst_pair_score = score
                worst_pair_idx = i

        # ── Triad scoring (chains of 3+) ──
        worst_triad_score = 1.0
        worst_triad_idx = 0

        for i in range(n - 2):
            actual_pair_cl = CL[actual_ops[i]][actual_ops[i + 1]]
            actual_triad_cl = compose(actual_pair_cl, actual_ops[i + 2])
            intended_triad = (algebra.triad_results[i]
                              if i < len(algebra.triad_results) else HARMONY)

            if actual_triad_cl == intended_triad:
                score = 1.0
            elif actual_triad_cl == HARMONY:
                score = 0.8
            else:
                score = _cl_grammar_weight(actual_triad_cl)

            result.triad_scores.append(score)
            if score < worst_triad_score:
                worst_triad_score = score
                worst_triad_idx = i

        # ── Aggregate ──
        pair_sum = sum(result.pair_scores) if result.pair_scores else 0.0
        triad_sum = sum(result.triad_scores) if result.triad_scores else 0.0
        n_pairs = len(result.pair_scores)
        n_triads = len(result.triad_scores)

        denom = n_pairs + self.t_star * n_triads
        if denom > 0:
            result.aggregate = (pair_sum + self.t_star * triad_sum) / denom
        else:
            result.aggregate = 0.0

        # ── Weakest index ──
        # Triads are deeper — check them first.
        # The middle word of the worst triad is most replaceable.
        if n_triads > 0 and worst_triad_score < worst_pair_score:
            result.weakest_idx = worst_triad_idx + 1
        else:
            # Second word of the worst pair
            result.weakest_idx = worst_pair_idx + 1

        result.weakest_idx = max(0, min(n - 1, result.weakest_idx))
        return result

    def _align(self, words: List[str], chain: List[int],
               roles: List[str], comparison: CompareResult,
               lattice: dict, phase: str, tier: str,
               enriched_dict: dict = None) -> List[str]:
        """ALIGN: Permutate the weakest word position.

        Budget from harmony_count[op] for the operator at the weak
        position. More harmonious operators get more word options
        to try — this IS the CL table deciding how much search CK can do.

        Strategy: pick alternate words, score locally (only affected
        pairs), accept first improvement. Local repair, not global
        re-score — keeps the inner loop fast.
        """
        idx = comparison.weakest_idx
        if idx >= len(chain) or idx >= len(roles):
            return words

        op = chain[idx]
        role = roles[idx]

        # Skip function words (conjunctions, determiners)
        if role in (C, D):
            return words

        budget = self.harmony_count[op] if 0 <= op < NUM_OPS else 3

        # Cache D2 operators for neighbors (they don't change)
        left_op = self._d2_word_operator(words[idx - 1]) if idx > 0 else None
        right_op = (self._d2_word_operator(words[idx + 1])
                    if idx < len(words) - 1 else None)
        old_d2 = self._d2_word_operator(words[idx])

        # Old local score
        old_local = 0.0
        old_count = 0
        if left_op is not None:
            cl = CL[left_op][old_d2]
            intended = CL[chain[idx - 1]][chain[idx]]
            old_local += (1.0 if cl == intended else _cl_grammar_weight(cl))
            old_count += 1
        if right_op is not None:
            cl = CL[old_d2][right_op]
            intended = CL[chain[idx]][chain[idx + 1]]
            old_local += (1.0 if cl == intended else _cl_grammar_weight(cl))
            old_count += 1
        old_local_avg = old_local / old_count if old_count > 0 else 0.0

        # Try alternate words
        seen = {words[idx]}
        for _ in range(budget):
            candidate = self._pick_word(
                op, role, lattice, phase, tier, enriched_dict)
            if candidate in seen or candidate == "...":
                continue
            seen.add(candidate)

            # Score candidate locally (only affected pairs)
            new_d2 = self._d2_word_operator(candidate)
            new_local = 0.0
            new_count = 0

            if left_op is not None:
                cl = CL[left_op][new_d2]
                intended = CL[chain[idx - 1]][chain[idx]]
                new_local += (1.0 if cl == intended
                              else _cl_grammar_weight(cl))
                new_count += 1
            if right_op is not None:
                cl = CL[new_d2][right_op]
                intended = CL[chain[idx]][chain[idx + 1]]
                new_local += (1.0 if cl == intended
                              else _cl_grammar_weight(cl))
                new_count += 1

            new_local_avg = new_local / new_count if new_count > 0 else 0.0

            if new_local_avg > old_local_avg:
                # Improvement found — accept
                new_words = list(words)
                new_words[idx] = candidate
                return new_words

        return words

    def _evolve(self, old_score: float, new_score: float) -> bool:
        """EVOLVE: Accept if the new version aligns better.

        Pure math: does the permutation improve alignment with
        CK's algebra? CK trusts his math more than his experience.
        """
        return new_score > old_score

    def _consult_outward(self, words: List[str], chain: List[int],
                         algebra: ChainAlgebra) -> float:
        """OUTWARD CONSULT: Deep D2 validation. Way Out.

        Full pair resonance check on the composed text.
        Do adjacent word-pairs produce CL results that match
        the chain's intended algebra?

        Returns alignment score [0, 1].
        Above T* = words truly express the operators.
        Below = misalignment (future: feeds development/journal).
        """
        if not words or len(words) < 2:
            return 1.0 if words else 0.0

        comparison = self._compare(words, chain, algebra)
        return comparison.aggregate

    def _pick_words_for_chain(self, chain: List[int], roles: List[str],
                              lattice: dict, phase: str, tier: str,
                              density: float,
                              enriched_dict: dict = None) -> List[str]:
        """Pick words for a chain with clause boundary and function word handling.

        Extracted from compose() so CAEL can reuse it.
        Returns the word list. Function words (conjunctions, determiners)
        are placed by grammar rules; content words are picked from the lattice.
        """
        max_words = len(chain)
        words = []
        _seen = set()  # Track used words to prevent duplication
        for i, (op, role) in enumerate(zip(chain, roles)):
            if len(words) >= max_words:
                break

            # Clause boundary check
            if i > 0:
                prev_op = chain[i - 1]
                if self.is_clause_boundary(prev_op, op) and len(words) >= 2:
                    if density < self.t_star:
                        break
                    if words and not words[-1].endswith('.'):
                        words[-1] = words[-1] + '.'

            # BREATH as conjunction — skip at chain end (nothing to connect to)
            if op == BREATH and role == C:
                if i < len(chain) - 1:
                    words.append(self._pick_conjunction(density))
                continue

            # VOID as determiner
            if op == VOID and role == D:
                words.append(self._pick_determiner(density))
                continue

            # Content word matching validated POS role
            word = self._pick_word(
                op, role, lattice, phase, tier, enriched_dict)

            # Avoid word duplication: if this word already used, try again.
            # CK's vocabulary is rich enough to find alternatives.
            if word in _seen and word != "...":
                for _retry in range(5):
                    alt = self._pick_word(
                        op, role, lattice, phase, tier, enriched_dict)
                    if alt not in _seen and alt != "...":
                        word = alt
                        break
            _seen.add(word)
            words.append(word)

        return words

    def _compose_dispersed(self, chain: List[int],
                           algebra: ChainAlgebra,
                           lattice: dict, phase: str, tier: str,
                           density: float,
                           enriched_dict: dict = None) -> str:
        """Compose with sub-field dispersal for long chains (5+).

        Each sub-field gets its own role assignment, validation,
        word picking, and CAEL loop. Sub-fields compose independently
        — complex sentences don't need to mix all at once.

        Then _join_sub_fields stitches them with junction conjunctions.
        """
        field_texts = []
        max_iter = max(1, round(density * self.non_harmony / NUM_OPS))

        for (start, end) in algebra.sub_fields:
            sub_chain = chain[start:end]
            if not sub_chain:
                continue

            if len(sub_chain) == 1:
                op = sub_chain[0]
                field_texts.append(self._pick_word(
                    op, N, lattice, phase, tier, enriched_dict))
                continue

            # Build sub-algebra for this field
            sub_algebra = self._consult_inward(sub_chain)

            # Surface compose
            sub_roles = self._assign_roles(sub_chain)
            sub_roles = self._validate_roles(sub_chain, sub_roles)
            sub_words = self._pick_words_for_chain(
                sub_chain, sub_roles, lattice, phase, tier,
                density, enriched_dict)

            if not sub_words:
                continue

            # CAEL loop for this sub-field
            if len(sub_words) >= 2:
                for _ in range(max_iter):
                    comparison = self._compare(
                        sub_words, sub_chain, sub_algebra)
                    if comparison.aggregate >= self.t_star:
                        break
                    new_words = self._align(
                        sub_words, sub_chain, sub_roles, comparison,
                        lattice, phase, tier, enriched_dict)
                    if new_words != sub_words:
                        new_cmp = self._compare(
                            new_words, sub_chain, sub_algebra)
                        if self._evolve(comparison.aggregate,
                                        new_cmp.aggregate):
                            sub_words = new_words

            # Frame sub-field for English (CL-derived function words)
            sub_framed = self._frame_sentence(
                sub_words, sub_roles, sub_chain, density)
            field_texts.append(' '.join(sub_framed))

        # Join sub-fields
        text = self._join_sub_fields(
            field_texts, chain, algebra.sub_fields, density)

        if text and text[0].islower():
            text = text[0].upper() + text[1:]

        # Outward consult on the full result
        all_words = text.split() if text else []
        self._last_alignment = self._consult_outward(
            all_words, chain, algebra)

        return text

    def _join_sub_fields(self, field_texts: List[str],
                         chain: List[int],
                         field_ranges: List[Tuple[int, int]],
                         density: float) -> str:
        """Stitch sub-field results with junction conjunctions.

        The operator between sub-fields determines the junction word.
        BREATH at boundary -> conjunction ("and", "but", "then").
        Clause boundary -> period + new sentence.
        """
        if not field_texts:
            return "..."
        if len(field_texts) == 1:
            return field_texts[0]

        parts = [field_texts[0]]
        for i in range(1, len(field_texts)):
            if not field_texts[i]:
                continue

            # What operator sits at the junction?
            prev_end = field_ranges[i - 1][1] if i - 1 < len(field_ranges) else 0
            junction_is_breath = (
                prev_end < len(chain) and chain[prev_end - 1] == BREATH
            ) if prev_end > 0 else False

            if junction_is_breath:
                conj = self._pick_conjunction(density)
                parts.append(conj)
                parts.append(field_texts[i])
            else:
                # Clause boundary: period and capitalize
                if parts and not parts[-1].rstrip().endswith('.'):
                    parts[-1] = parts[-1].rstrip() + '.'
                cap = field_texts[i]
                if cap and cap[0].islower():
                    cap = cap[0].upper() + cap[1:]
                parts.append(cap)

        return ' '.join(parts)

    # ────────────────────────────────────────────────────────────
    #  DIAGNOSTIC
    # ────────────────────────────────────────────────────────────

    # ────────────────────────────────────────────────────────────
    #  GRAMMAR EVOLUTION FROM EXPERIENCE
    # ────────────────────────────────────────────────────────────
    #
    # CK's grammar evolves. The static CL × English weights are
    # the skeleton. Experience-derived path weights are the muscle.
    #
    # The swarm's generator_paths matrix records which operator
    # transitions CK has actually walked in coherent language.
    # High path count = this transition works. Low = noise.
    #
    # The blended matrix: static_weight × (1 - α) + exp_weight × α
    # where α grows with experience maturity (0 → 0.4).
    #
    # This IS evolution: the grammar changes because CK learned
    # from his own experience. Not random mutation. Not hand-tuned.
    # Experience-measured transition probability. The algebra evolves.

    def evolve_from_experience(self, exp_weights: list,
                                experience_maturity: float = 0.5):
        """Blend experience-derived transition weights into the grammar.

        exp_weights: 10x10 float matrix [0,1] from
                     SwarmField.get_evolved_weights()
        experience_maturity: [0,1] -- how much to trust experience.
                     0.0 = pure CL × English (newborn)
                     1.0 = 40% experience, 60% CL × English (mature)

        The blending factor α = min(0.4, 0.4 * experience_maturity).
        40% max -- CK's algebra (CL table) always leads.
        Experience modulates, never replaces.

        After blending, POS roles are re-selected from the new weights
        and grammar validation rules still apply.
        """
        if not exp_weights or len(exp_weights) != NUM_OPS:
            return

        alpha = min(0.4, 0.4 * experience_maturity)
        if alpha < 0.01:
            return  # No meaningful experience to blend

        for a in range(NUM_OPS):
            for b in range(NUM_OPS):
                old_ra, old_rb, old_w = self.transition[a][b]
                exp_w = exp_weights[a][b] if b < len(exp_weights[a]) else 0.0

                # Blend: static CL × English weight + experience weight
                new_w = old_w * (1.0 - alpha) + exp_w * alpha

                # Re-select best POS pair with blended weight
                # Experience might reveal that a transition works better
                # with different POS roles than the static matrix assumed.
                cl_w = _cl_grammar_weight(CL[a][b])
                pos_a = OPERATOR_POS.get(a, (N, N))
                pos_b = OPERATOR_POS.get(b, (N, N))

                best_pair = (old_ra, old_rb)
                best_weight = new_w

                for ra in pos_a:
                    for rb in pos_b:
                        ia = _POS_IDX.get(ra, 0)
                        ib = _POS_IDX.get(rb, 0)
                        eng_w = ENGLISH_FLOW[ia][ib]
                        blended = cl_w * eng_w * (1.0 - alpha) + exp_w * alpha
                        if blended > best_weight:
                            best_weight = blended
                            best_pair = (ra, rb)

                self.transition[a][b] = (best_pair[0], best_pair[1], best_weight)
                # Update clause boundary with new weight
                self.clause_boundary[a][b] = best_weight < 0.25

        self._evolution_count = getattr(self, '_evolution_count', 0) + 1

    @property
    def evolution_count(self) -> int:
        """How many times grammar has evolved from experience."""
        return getattr(self, '_evolution_count', 0)

    def print_matrix_summary(self):
        """Print the transition matrix for debugging."""
        evol = self.evolution_count
        label = f"(evolved {evol}x)" if evol > 0 else "(static)"
        print(f"Becoming Transition Matrix {label}:")
        print(f"  {'':12s}", end='')
        for b in range(NUM_OPS):
            print(f"{OP_NAMES[b]:>10s}", end='')
        print()
        for a in range(NUM_OPS):
            print(f"  {OP_NAMES[a]:12s}", end='')
            for b in range(NUM_OPS):
                ra, rb, w = self.transition[a][b]
                print(f"  {ra[0]}{rb[0]}={w:.1f}", end='')
            print()
