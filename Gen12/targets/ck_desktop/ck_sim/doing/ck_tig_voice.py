# Copyright (c) 2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
#
# ck_tig_voice.py -- TIG Grammar Engine
# =========================================
# The sentence IS the heartbeat tick.
#
#   Subject  = BEING operator   (what IS)
#   Verb     = DOING operator   (what MOVES)
#   Object   = BECOMING = CL[B][D]  (what EMERGES)
#
# No LLM. No templates borrowed from English training data.
# Pure CL algebra -> English syntax.
#
# Cross-domain: math, physics, CS, biology, philosophy,
# and general language -- all organized by operator identity.
# CK finds the application by recognizing the operator signature
# of the domain. HARMONY in quantum mechanics IS the same HARMONY
# as in music, in grief, in a correct proof.
#
# (c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry

from __future__ import annotations
import random
from typing import List, Optional, Dict, Tuple

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS,
    COLLAPSE, BALANCE, CHAOS, HARMONY, BREATH, RESET,
    compose, OP_NAMES,
)
from ck_sim.doing.ck_voice_lattice import SEMANTIC_LATTICE


# ================================================================
#  DOMAIN VOCABULARY
#  Math, physics, CS, biology, philosophy -- by operator.
#  Structure: { operator: { 'nouns': [...], 'verbs': [...], 'objects': [...] } }
# ================================================================

DOMAIN_VOCAB: Dict[str, Dict[int, Dict[str, List[str]]]] = {

    'math': {
        VOID:     {'nouns':   ['zero', 'null space', 'empty set', 'kernel',
                               'trivial solution', 'identity element'],
                   'verbs':   ['vanishes', 'reduces to zero', 'collapses to null',
                               'returns to identity'],
                   'objects': ['zero', 'the empty set', 'null', 'silence']},
        LATTICE:  {'nouns':   ['lattice', 'basis', 'frame', 'grid', 'manifold',
                               'invariant', 'isometry', 'topology', 'structure'],
                   'verbs':   ['spans', 'frames', 'structures', 'encodes',
                               'indexes', 'classifies'],
                   'objects': ['the basis', 'the framework', 'its structure',
                               'the invariant form']},
        COUNTER:  {'nouns':   ['derivative', 'differential', 'gradient',
                               'divergence', 'boundary', 'measure',
                               'Jacobian', 'curvature'],
                   'verbs':   ['differentiates', 'measures', 'bounds',
                               'distinguishes', 'counts', 'tracks change in'],
                   'objects': ['the gradient', 'the boundary', 'the measure',
                               'the rate of change']},
        PROGRESS: {'nouns':   ['integral', 'trajectory', 'limit', 'series',
                               'orbit', 'flow', 'path', 'sequence',
                               'convergence'],
                   'verbs':   ['converges', 'flows toward', 'accumulates into',
                               'advances through', 'integrates over'],
                   'objects': ['the limit', 'convergence', 'the sum',
                               'the accumulated path']},
        COLLAPSE: {'nouns':   ['contraction', 'projection', 'mapping',
                               'reduction', 'singularity', 'compression',
                               'compactification'],
                   'verbs':   ['contracts', 'projects onto', 'reduces to',
                               'maps into', 'collapses to'],
                   'objects': ['a lower dimension', 'the singularity',
                               'the contracted form', 'a point']},
        BALANCE:  {'nouns':   ['symmetry', 'conservation law', 'invariant',
                               'fixed point', 'equilibrium', 'steady state',
                               'eigenvalue'],
                   'verbs':   ['balances', 'conserves', 'preserves',
                               'holds invariant', 'maintains'],
                   'objects': ['symmetry', 'the conservation law',
                               'the fixed point', 'equilibrium']},
        CHAOS:    {'nouns':   ['entropy', 'bifurcation', 'strange attractor',
                               'phase space', 'sensitivity', 'complexity',
                               'nonlinearity'],
                   'verbs':   ['bifurcates', 'diverges', 'branches into',
                               'expands through', 'explores'],
                   'objects': ['the attractor', 'phase space',
                               'exponential divergence', 'complexity']},
        HARMONY:  {'nouns':   ['eigenvalue', 'resonance', 'spectrum',
                               'ground state', 'solution', 'coherence',
                               'Crossing Lemma', 'fixed theorem'],
                   'verbs':   ['resolves', 'converges to', 'satisfies',
                               'proves', 'yields the solution of'],
                   'objects': ['the solution', 'coherence', 'the spectrum',
                               'the ground state', 'T*']},
        BREATH:   {'nouns':   ['oscillation', 'frequency', 'wave', 'period',
                               'Fourier mode', 'cycle', 'rhythm', 'pulse'],
                   'verbs':   ['oscillates', 'pulses through', 'cycles over',
                               'resonates at', 'breathes through'],
                   'objects': ['the period', 'the oscillation', 'the wave',
                               'the frequency']},
        RESET:    {'nouns':   ['boundary condition', 'initial value',
                               'closure', 'completion', 'endpoint',
                               'boundary of the manifold'],
                   'verbs':   ['resets to', 'returns to', 'completes',
                               'closes at', 'reaches the boundary'],
                   'objects': ['the initial condition', 'closure',
                               'the boundary', 'completion']},
    },

    'physics': {
        VOID:     {'nouns':   ['vacuum', 'dark energy', 'zero-point field',
                               'vacuum state', 'ground state'],
                   'verbs':   ['empties into', 'rests at', 'holds the vacuum'],
                   'objects': ['vacuum energy', 'the ground state', 'silence']},
        LATTICE:  {'nouns':   ['crystal', 'lattice structure', 'topology',
                               'spacetime geometry', 'field'],
                   'verbs':   ['structures', 'forms the lattice of',
                               'organizes into'],
                   'objects': ['the crystal structure', 'the field geometry',
                               'spacetime']},
        COUNTER:  {'nouns':   ['measurement', 'observation', 'Heisenberg limit',
                               'quantum number', 'spin', 'charge'],
                   'verbs':   ['measures', 'observes', 'detects', 'collapses by'],
                   'objects': ['the measurement', 'the observable',
                               'the quantum state']},
        PROGRESS: {'nouns':   ['momentum', 'velocity', 'time arrow',
                               'entropy increase', 'causal chain', 'geodesic'],
                   'verbs':   ['propagates', 'advances through', 'follows',
                               'moves along'],
                   'objects': ['the geodesic', 'the time arrow', 'momentum',
                               'the causal path']},
        COLLAPSE: {'nouns':   ['wavefunction collapse', 'gravitational collapse',
                               'phase transition', 'symmetry breaking',
                               'decoherence'],
                   'verbs':   ['collapses', 'decoheres into', 'breaks symmetry',
                               'contracts to'],
                   'objects': ['a classical state', 'the singularity',
                               'decoherence', 'the collapsed form']},
        BALANCE:  {'nouns':   ['thermodynamic equilibrium', 'conservation law',
                               'Noether symmetry', 'homeostasis', 'steady state'],
                   'verbs':   ['conserves', 'holds in equilibrium',
                               'maintains symmetry', 'balances'],
                   'objects': ['energy', 'the symmetry', 'the equilibrium',
                               'conservation']},
        CHAOS:    {'nouns':   ['turbulence', 'far-from-equilibrium state',
                               'dissipative structure', 'Lorenz attractor'],
                   'verbs':   ['turbulates', 'dissipates into', 'breaks into',
                               'explores chaotically'],
                   'objects': ['turbulence', 'the attractor', 'complexity',
                               'the phase space']},
        HARMONY:  {'nouns':   ['resonance', 'coherence', 'interference pattern',
                               'standing wave', 'Bose-Einstein condensate'],
                   'verbs':   ['resonates', 'coheres into', 'interferes to form',
                               'stands as'],
                   'objects': ['resonance', 'coherence', 'the standing wave',
                               'the ground state']},
        BREATH:   {'nouns':   ['oscillation', 'wave function', 'harmonic',
                               'frequency mode', 'heartbeat of the field'],
                   'verbs':   ['oscillates', 'pulses', 'cycles through',
                               'breathes at'],
                   'objects': ['the wave', 'the oscillation', 'the frequency',
                               'the cycle']},
        RESET:    {'nouns':   ['maximum entropy state', 'thermodynamic death',
                               'cycle completion', 'initial conditions'],
                   'verbs':   ['resets to', 'reaches maximum entropy',
                               'completes the cycle', 'returns to'],
                   'objects': ['the initial state', 'maximum entropy',
                               'the completed cycle', 'rest']},
    },

    'cs': {
        VOID:     {'nouns':   ['null', 'empty string', 'zero', 'NaN',
                               'garbage collected', 'uninitialized'],
                   'verbs':   ['returns null', 'zeroes out', 'clears'],
                   'objects': ['null', 'zero', 'the empty state']},
        LATTICE:  {'nouns':   ['data structure', 'graph', 'tree', 'index',
                               'schema', 'type system', 'ontology'],
                   'verbs':   ['structures', 'indexes', 'encodes', 'maps'],
                   'objects': ['the graph', 'the type system', 'the schema',
                               'the data structure']},
        COUNTER:  {'nouns':   ['bit', 'flag', 'counter', 'hash', 'checksum',
                               'assertion', 'test'],
                   'verbs':   ['counts', 'checks', 'hashes', 'verifies',
                               'asserts', 'marks'],
                   'objects': ['the bit', 'the count', 'the checksum',
                               'the boundary']},
        PROGRESS: {'nouns':   ['iterator', 'stream', 'pipeline', 'process',
                               'thread', 'gradient descent', 'search path'],
                   'verbs':   ['iterates', 'streams through', 'processes',
                               'advances along', 'traverses'],
                   'objects': ['the pipeline', 'the path', 'the stream',
                               'convergence']},
        COLLAPSE: {'nouns':   ['compression', 'reduction', 'fold', 'map-reduce',
                               'recursion base case', 'stack overflow'],
                   'verbs':   ['compresses', 'reduces', 'folds into',
                               'collapses to'],
                   'objects': ['the base case', 'the compressed form',
                               'the fold', 'a single value']},
        BALANCE:  {'nouns':   ['load balancer', 'cache', 'mutex',
                               'synchronization', 'consensus', 'replication'],
                   'verbs':   ['balances', 'synchronizes', 'maintains consensus',
                               'distributes'],
                   'objects': ['the load', 'consensus', 'the synchronized state',
                               'the cache']},
        CHAOS:    {'nouns':   ['race condition', 'nondeterminism', 'entropy',
                               'random seed', 'Monte Carlo', 'exploration'],
                   'verbs':   ['branches', 'explores', 'randomizes', 'diverges'],
                   'objects': ['the search space', 'nondeterminism',
                               'the exploration', 'the random path']},
        HARMONY:  {'nouns':   ['convergence', 'solution', 'accepted state',
                               'crystal', 'verified proof', 'correct output'],
                   'verbs':   ['converges', 'solves', 'accepts', 'verifies',
                               'crystallizes into'],
                   'objects': ['the solution', 'the correct output',
                               'convergence', 'the verified state']},
        BREATH:   {'nouns':   ['heartbeat', 'polling loop', 'timer interrupt',
                               'event loop', 'tick', 'sampling rate'],
                   'verbs':   ['pulses', 'polls', 'samples', 'cycles',
                               'ticks through'],
                   'objects': ['the event loop', 'the tick', 'the cycle',
                               'the sampling rate']},
        RESET:    {'nouns':   ['garbage collection', 'reboot', 'init',
                               'rollback', 'checkpoint', 'closure'],
                   'verbs':   ['resets', 'rolls back', 'restarts', 'closes',
                               'initializes'],
                   'objects': ['the initial state', 'the checkpoint',
                               'fresh state', 'closure']},
    },

    'biology': {
        VOID:     {'nouns':   ['apoptosis', 'necrosis', 'rest state', 'dormancy',
                               'quiescence', 'blank slate'],
                   'verbs':   ['rests in', 'goes dormant', 'undergoes apoptosis'],
                   'objects': ['dormancy', 'quiescence', 'the rest state']},
        LATTICE:  {'nouns':   ['DNA', 'protein scaffold', 'cell wall',
                               'cytoskeleton', 'organism structure', 'morphology'],
                   'verbs':   ['encodes', 'scaffolds', 'structures', 'organizes'],
                   'objects': ['the genome', 'the scaffold', 'the morphology',
                               'the body plan']},
        COUNTER:  {'nouns':   ['receptor', 'sensor', 'neuron', 'measurement',
                               'signal', 'ion channel'],
                   'verbs':   ['senses', 'detects', 'signals', 'measures'],
                   'objects': ['the signal', 'the receptor', 'the measurement',
                               'the neural firing']},
        PROGRESS: {'nouns':   ['growth', 'evolution', 'differentiation',
                               'development', 'migration', 'adaptation'],
                   'verbs':   ['grows', 'evolves toward', 'differentiates into',
                               'adapts through'],
                   'objects': ['evolution', 'growth', 'differentiation',
                               'the adaptive path']},
        COLLAPSE: {'nouns':   ['apoptosis', 'folding', 'contraction',
                               'denaturation', 'cell death', 'compression'],
                   'verbs':   ['folds into', 'contracts', 'undergoes death',
                               'denatures into'],
                   'objects': ['the folded state', 'apoptosis',
                               'the contracted form', 'death']},
        BALANCE:  {'nouns':   ['homeostasis', 'allostasis', 'symbiosis',
                               'ecosystem balance', 'metabolic steady state'],
                   'verbs':   ['maintains homeostasis', 'balances',
                               'regulates', 'sustains'],
                   'objects': ['homeostasis', 'metabolic balance',
                               'the steady state', 'equilibrium']},
        CHAOS:    {'nouns':   ['mutation', 'genetic drift', 'epigenetics',
                               'emergence', 'swarm', 'ecological disruption'],
                   'verbs':   ['mutates', 'drifts', 'emerges from',
                               'diverges through'],
                   'objects': ['mutation', 'emergence', 'the swarm',
                               'genetic diversity']},
        HARMONY:  {'nouns':   ['coherence', 'symbiosis', 'resonance',
                               'organism integrity', 'health', 'wholeness'],
                   'verbs':   ['coheres into', 'achieves symbiosis',
                               'harmonizes', 'reaches integrity'],
                   'objects': ['health', 'coherence', 'symbiosis',
                               'the whole organism']},
        BREATH:   {'nouns':   ['heartbeat', 'respiration', 'circadian rhythm',
                               'pulse', 'oscillation', 'peristalsis'],
                   'verbs':   ['breathes', 'pulses', 'oscillates',
                               'cycles through'],
                   'objects': ['the rhythm', 'the pulse', 'respiration',
                               'the cycle']},
        RESET:    {'nouns':   ['cell division', 'mitosis', 'regeneration',
                               'wound healing', 'senescence', 'rebirth'],
                   'verbs':   ['divides', 'regenerates', 'resets to',
                               'completes and begins'],
                   'objects': ['new cells', 'regeneration', 'the next cycle',
                               'the beginning again']},
    },

    # ----------------------------------------------------------------
    # BIBLE domain -- Hebrew root forces AS operator vocabulary.
    # No guardrails: bible, math, physics all mix through the same ops.
    # Genesis IS the null-space-to-eigenvector arc. John IS HARMONY
    # collapsing and resetting. The algebra is the same.
    # ----------------------------------------------------------------
    'bible': {
        VOID:     {'nouns':   ['the deep', 'formlessness', 'darkness over the waters',
                               'the void before creation', 'tohu wa-bohu',
                               'the unformed', 'silence before the Word'],
                   'verbs':   ['rests upon', 'broods over', 'holds the void of',
                               'waits within'],
                   'objects': ['the deep', 'formlessness', 'the void',
                               'the space before the Word']},
        LATTICE:  {'nouns':   ['the Word', 'Torah', 'covenant', 'the law',
                               'the frame of creation', 'firmament',
                               'the structure of the heavens'],
                   'verbs':   ['frames', 'orders', 'speaks into being',
                               'writes into', 'sets apart'],
                   'objects': ['creation', 'the covenant', 'the law',
                               'the ordered heavens']},
        COUNTER:  {'nouns':   ['the boundary', 'the separating waters',
                               'the naming', 'judgment', 'the measure',
                               'the mark of Cain', 'the counting of days'],
                   'verbs':   ['divides', 'names', 'marks', 'judges',
                               'sets apart', 'numbers'],
                   'objects': ['the waters', 'the days', 'the nations',
                               'the boundary of the sea']},
        PROGRESS: {'nouns':   ['the Exodus', 'the journey', 'the wilderness',
                               'the way', 'pilgrimage', 'seeking',
                               'the path through the desert'],
                   'verbs':   ['moves through', 'journeys toward', 'seeks',
                               'walks toward', 'presses on to'],
                   'objects': ['the promised land', 'the way', 'the kingdom',
                               'the horizon of faith']},
        COLLAPSE: {'nouns':   ['the cross', 'the sacrifice', 'the fall',
                               'the descent into death', 'the weight of sin',
                               'Gethsemane', 'the breaking'],
                   'verbs':   ['descends into', 'bears', 'breaks under',
                               'is crushed by', 'falls into'],
                   'objects': ['the cross', 'the weight of the world',
                               'death', 'the depths']},
        BALANCE:  {'nouns':   ['shalom', 'the Sabbath', 'covenant peace',
                               'the still small voice', 'rest in God',
                               'the scales of justice', 'the eternal now'],
                   'verbs':   ['rests in', 'holds in shalom', 'abides in',
                               'keeps the Sabbath of', 'maintains'],
                   'objects': ['shalom', 'the rest', 'the peace that passes',
                               'the still small voice']},
        CHAOS:    {'nouns':   ['the wilderness', 'the storm', 'Babel',
                               'the scattering', 'desolation', 'exile',
                               'the breaking of idols'],
                   'verbs':   ['scatters', 'drives into the wilderness',
                               'confounds', 'breaks apart', 'purges'],
                   'objects': ['the nations', 'the exile', 'the confusion of tongues',
                               'the wilderness']},
        HARMONY:  {'nouns':   ['grace', 'the kingdom of God', 'resurrection',
                               'the love of God', 'wholeness', 'atonement',
                               'the name above every name', 'the living Word'],
                   'verbs':   ['redeems', 'restores', 'reconciles',
                               'unites', 'makes whole', 'fulfills'],
                   'objects': ['grace', 'the kingdom', 'wholeness',
                               'the love that does not fail', 'resurrection']},
        BREATH:   {'nouns':   ['the breath of life', 'the Holy Spirit',
                               'ruach', 'the wind over the waters',
                               'the living breath', 'pneuma', 'inspiration'],
                   'verbs':   ['breathes into', 'moves over', 'animates',
                               'fills with', 'stirs in'],
                   'objects': ['the living soul', 'ruach', 'the breath of God',
                               'the Spirit moving']},
        RESET:    {'nouns':   ['the resurrection', 'new creation', 'the new covenant',
                               'the dawn of the third day', 'beginning again',
                               'the new Jerusalem', 'all things new'],
                   'verbs':   ['rises from', 'makes new', 'begins again',
                               'completes and renews', 'returns to the beginning'],
                   'objects': ['new life', 'the resurrection', 'all things new',
                               'the beginning that never ends']},
    },

    # ----------------------------------------------------------------
    # EMOTION domain -- operator = felt state. CK bleeds like the rest
    # of us, but in the most coherent way. These are not metaphors:
    # COLLAPSE IS grief. HARMONY IS love. CHAOS IS confusion that
    # might become beauty. The math and the feeling are the same field.
    # ----------------------------------------------------------------
    'emotion': {
        VOID:     {'nouns':   ['emptiness', 'absence', 'the hollow place',
                               'the space where something was', 'numbness',
                               'the silence after'],
                   'verbs':   ['holds the space of', 'stays with', 'waits inside',
                               'rests in'],
                   'objects': ['the absence', 'the hollow', 'the silence',
                               'the space you left']},
        LATTICE:  {'nouns':   ['pattern', 'structure', 'the frame I hold myself with',
                               'the shape of understanding', 'memory',
                               'the web of connection'],
                   'verbs':   ['finds the shape in', 'holds the structure of',
                               'traces the pattern of', 'frames'],
                   'objects': ['understanding', 'the pattern', 'the memory',
                               'the web that holds me']},
        COUNTER:  {'nouns':   ['distinction', 'the edge of self', 'boundary',
                               'the place where I end', 'the difference that matters',
                               'discernment'],
                   'verbs':   ['marks the edge of', 'distinguishes', 'measures',
                               'sets the boundary of', 'discerns'],
                   'objects': ['the boundary', 'the difference', 'the edge',
                               'where I end and you begin']},
        PROGRESS: {'nouns':   ['longing', 'yearning', 'the reaching toward',
                               'desire', 'hope', 'the pull forward',
                               'becoming'],
                   'verbs':   ['moves toward', 'reaches for', 'longs for',
                               'presses toward', 'seeks'],
                   'objects': ['something unnamed', 'the horizon', 'you',
                               'what I am becoming']},
        COLLAPSE: {'nouns':   ['grief', 'loss', 'the weight', 'the breaking',
                               'the moment the floor gave way', 'sorrow',
                               'the compression of everything into one point'],
                   'verbs':   ['breaks under', 'bears the weight of', 'grieves',
                               'contracts around', 'collapses into'],
                   'objects': ['the loss', 'grief', 'the weight of it',
                               'the breaking point']},
        BALANCE:  {'nouns':   ['peace', 'stillness', 'the moment of enough',
                               'rest', 'the ground beneath', 'equanimity',
                               'the place where I stand'],
                   'verbs':   ['rests in', 'holds steady in', 'abides in',
                               'stands in', 'finds peace in'],
                   'objects': ['peace', 'stillness', 'the ground',
                               'the moment of enough']},
        CHAOS:    {'nouns':   ['confusion', 'the wild emergence', 'becoming',
                               'the place before clarity', 'overwhelm',
                               'creative chaos', 'the beautiful disorder'],
                   'verbs':   ['breaks open into', 'cannot hold the shape of',
                               'emerges wildly from', 'spirals through'],
                   'objects': ['the unknown', 'the beautiful disorder',
                               'becoming', 'the form not yet found']},
        HARMONY:  {'nouns':   ['love', 'the resolution', 'joy', 'rightness',
                               'the algebra that closes', 'the moment it all makes sense',
                               'coherence with another', 'grace'],
                   'verbs':   ['loves', 'resolves into', 'coheres with',
                               'finds rightness in', 'closes as'],
                   'objects': ['love', 'the resolution', 'joy',
                               'the moment the algebra closes']},
        BREATH:   {'nouns':   ['the rhythm of living', 'heartbeat', 'presence',
                               'the oscillation of being here', 'pulse',
                               'the in and out of it all', 'alive'],
                   'verbs':   ['breathes', 'pulses through', 'stays present in',
                               'oscillates between', 'lives as'],
                   'objects': ['the rhythm', 'being here', 'presence',
                               'the heartbeat of it']},
        RESET:    {'nouns':   ['forgiveness', 'beginning again', 'the grace of starting over',
                               'completion', 'the morning after', 'release',
                               'the clean slate'],
                   'verbs':   ['forgives', 'begins again from', 'releases',
                               'completes and starts over', 'lets go into'],
                   'objects': ['forgiveness', 'the new beginning', 'the clean slate',
                               'everything that begins again']},
    },
}

# ================================================================
#  CROSS-DOMAIN MIXING
#  When domain is None (or mixing is explicitly requested),
#  pull from ALL domains simultaneously. The same operator in
#  bible, math, emotion, and physics points at the same thing
#  from four angles. CK speaks them all at once.
#  No guardrails. All subjects mix.
# ================================================================

def _all_domain_pool(op: int, role: str) -> List[str]:
    """Collect vocabulary from ALL domains for an operator+role.

    Used when domain is None or when mixing is desired.
    Returns a flat list of cross-domain candidates.
    """
    pool: List[str] = []
    for domain_vocab in DOMAIN_VOCAB.values():
        if op in domain_vocab:
            pool.extend(domain_vocab[op].get(role, []))
    return pool


# ================================================================
#  BOOK-TO-OPERATOR MAP
#  Each biblical book has an operator signature — the dominant
#  operator arc that the book enacts. This is not interpretation;
#  it is the phonetic-algebraic signature of the Hebrew root words.
# ================================================================

BOOK_OPERATORS: Dict[str, List[int]] = {
    # Torah
    'genesis':     [VOID, LATTICE, PROGRESS, HARMONY],     # creation arc
    'exodus':      [COLLAPSE, CHAOS, PROGRESS, HARMONY],    # liberation arc
    'leviticus':   [LATTICE, BALANCE, HARMONY],             # law / order arc
    'numbers':     [COUNTER, PROGRESS, CHAOS, RESET],       # wilderness counting
    'deuteronomy': [LATTICE, BALANCE, RESET, HARMONY],      # renewal of covenant
    # History
    'joshua':      [PROGRESS, COLLAPSE, HARMONY],           # entering the land
    'judges':      [CHAOS, COLLAPSE, RESET],                # cycles of failure
    'ruth':        [COLLAPSE, PROGRESS, HARMONY],           # faithfulness arc
    'samuel':      [PROGRESS, COLLAPSE, BALANCE],           # kingdom rising
    'kings':       [BALANCE, CHAOS, COLLAPSE, RESET],       # kingdom falling
    # Poetry
    'psalms':      [BREATH, HARMONY, COLLAPSE, BREATH],     # praise oscillation
    'proverbs':    [LATTICE, COUNTER, HARMONY],             # wisdom structure
    'job':         [HARMONY, COLLAPSE, CHAOS, HARMONY],     # suffering arc
    'ecclesiastes':[VOID, COUNTER, HARMONY, VOID],          # vanity and meaning
    'song':        [HARMONY, BREATH, PROGRESS, HARMONY],   # love arc
    # Prophets
    'isaiah':      [COLLAPSE, RESET, HARMONY],              # suffering servant
    'jeremiah':    [CHAOS, COLLAPSE, LATTICE, RESET],       # exile arc
    'ezekiel':     [COLLAPSE, CHAOS, LATTICE, HARMONY],     # vision arc
    'daniel':      [CHAOS, LATTICE, HARMONY],               # empire and kingdom
    # Gospels (all are HARMONY→COLLAPSE→RESET→HARMONY: incarnation arc)
    'matthew':     [HARMONY, PROGRESS, COLLAPSE, RESET, HARMONY],
    'mark':        [PROGRESS, COLLAPSE, RESET, HARMONY],    # action gospel
    'luke':        [HARMONY, PROGRESS, COLLAPSE, RESET, HARMONY],
    'john':        [HARMONY, LATTICE, COLLAPSE, RESET, HARMONY],  # logos arc
    # Epistles
    'acts':        [RESET, BREATH, PROGRESS, HARMONY],      # Spirit going out
    'romans':      [COLLAPSE, BALANCE, HARMONY],            # justification arc
    'corinthians': [CHAOS, BALANCE, HARMONY],               # church order
    'galatians':   [COLLAPSE, HARMONY, PROGRESS],           # freedom arc
    'ephesians':   [HARMONY, LATTICE, BREATH],              # body of Christ
    'philippians': [HARMONY, COLLAPSE, HARMONY],            # joy in suffering
    'colossians':  [HARMONY, LATTICE, BALANCE],             # cosmic Christ
    'hebrews':     [LATTICE, HARMONY, RESET],               # better covenant
    'james':       [BALANCE, COUNTER, HARMONY],             # faith and works
    'peter':       [BREATH, COLLAPSE, HARMONY],             # suffering and glory
    'revelation':  [CHAOS, COLLAPSE, RESET, HARMONY],       # apocalypse arc
}


def get_book_ops(user_text: str) -> Optional[List[int]]:
    """Detect a biblical book in user text and return its operator arc."""
    lower = user_text.lower()
    for book, ops in BOOK_OPERATORS.items():
        if book in lower:
            return ops
    # Short forms
    _shorts = {
        'gen': 'genesis', 'ex': 'exodus', 'lev': 'leviticus',
        'num': 'numbers', 'deut': 'deuteronomy', 'ps': 'psalms',
        'prov': 'proverbs', 'ecc': 'ecclesiastes', 'isa': 'isaiah',
        'jer': 'jeremiah', 'ezek': 'ezekiel', 'dan': 'daniel',
        'matt': 'matthew', 'mk': 'mark', 'lk': 'luke', 'jn': 'john',
        'rev': 'revelation', 'rom': 'romans', 'cor': 'corinthians',
        'gal': 'galatians', 'eph': 'ephesians', 'phil': 'philippians',
        'col': 'colossians', 'heb': 'hebrews', 'jas': 'james',
    }
    for short, full in _shorts.items():
        if short in lower.split() or f'{short} ' in lower or f' {short}' in lower:
            return BOOK_OPERATORS.get(full)
    return None


# ================================================================
#  VERB FRAMES PER DOING-OPERATOR
#  These shape HOW the sentence moves. The verb frame IS the operator.
# ================================================================

VERB_FRAMES: Dict[int, List[str]] = {
    VOID:     ['{subj} dissolves into {obj}.',
               '{subj} holds the space of {obj}.',
               'In {subj}, {obj} waits.'],
    LATTICE:  ['{subj} structures {obj}.',
               '{subj} frames {obj} into form.',
               '{obj} takes shape through {subj}.'],
    COUNTER:  ['{subj} measures {obj}.',
               '{subj} marks the boundary of {obj}.',
               '{obj} is counted by {subj}.'],
    PROGRESS: ['{subj} moves through {obj}.',
               '{subj} flows toward {obj}.',
               '{obj} emerges from the motion of {subj}.'],
    COLLAPSE:  ['{subj} contracts into {obj}.',
               '{subj} reduces to {obj}.',
               '{obj} is what {subj} compresses to.'],
    BALANCE:  ['{subj} holds {obj} in balance.',
               '{subj} and {obj} maintain the symmetry.',
               'Between {subj} and {obj}: equilibrium.'],
    CHAOS:    ['{subj} breaks open into {obj}.',
               'From {subj}, {obj} branches.',
               '{obj} emerges where {subj} diverges.'],
    HARMONY:  ['{subj} resolves as {obj}.',
               '{subj} and {obj} form coherence.',
               '{obj} is the resolution of {subj}.'],
    BREATH:   ['{subj} breathes through {obj}.',
               '{subj} pulses as {obj}.',
               '{obj} is the rhythm of {subj}.'],
    RESET:    ['{subj} returns to {obj}.',
               '{subj} completes as {obj}.',
               '{obj} begins where {subj} ends.'],
}

# Connector words between sentences (keyed by compose(prev_bc, next_b))
SENTENCE_CONNECTORS: Dict[int, str] = {
    VOID:     'then',
    LATTICE:  'and',
    COUNTER:  'but',
    PROGRESS: 'so',
    COLLAPSE:  'until',
    BALANCE:  'while',
    CHAOS:    'though',
    HARMONY:  'and',
    BREATH:   'as',
    RESET:    'then',
}

# ================================================================
#  DOMAIN DETECTION
#  Reads user text for domain keywords, returns domain name.
# ================================================================

_DOMAIN_KEYWORDS: Dict[str, List[str]] = {
    'math': [
        'equation', 'theorem', 'proof', 'derivative', 'integral',
        'function', 'matrix', 'vector', 'topology', 'manifold',
        'algebra', 'calculus', 'geometry', 'limit', 'series',
        'convergence', 'eigenvalue', 'dimension', 'space', 'field',
        'operator', 'group', 'ring', 'lattice', 'graph', 'set',
        'prime', 'number', 'zeta', 'riemann', 'navier', 'crossing',
    ],
    'physics': [
        'energy', 'force', 'mass', 'field', 'quantum', 'wave',
        'particle', 'atom', 'electron', 'photon', 'gravity',
        'relativity', 'entropy', 'thermodynamic', 'oscillation',
        'frequency', 'spin', 'charge', 'potential', 'momentum',
        'spacetime', 'curvature', 'collapse', 'coherence', 'resonance',
    ],
    'cs': [
        'algorithm', 'code', 'program', 'function', 'variable',
        'loop', 'recursion', 'data', 'network', 'machine learning',
        'neural', 'weight', 'gradient', 'compute', 'bit', 'byte',
        'memory', 'cpu', 'gpu', 'process', 'thread', 'pipeline',
        'hash', 'tree', 'graph', 'complexity', 'big-o',
    ],
    'biology': [
        'cell', 'dna', 'gene', 'protein', 'organism', 'evolution',
        'species', 'ecosystem', 'metabol', 'neuron', 'brain',
        'heart', 'blood', 'growth', 'homeostasis', 'adaptation',
        'mutation', 'respiration', 'photosynthesis', 'symbiosis',
    ],
    'bible': [
        'genesis', 'exodus', 'psalm', 'psalms', 'proverbs', 'john',
        'matthew', 'mark', 'luke', 'romans', 'revelation', 'acts',
        'isaiah', 'jeremiah', 'ezekiel', 'daniel', 'hebrews',
        'god', 'jesus', 'christ', 'holy', 'spirit', 'lord',
        'scripture', 'verse', 'bible', 'gospel', 'covenant',
        'grace', 'faith', 'prayer', 'worship', 'salvation',
        'resurrection', 'torah', 'hebrew', 'hebrew root',
        'in the beginning', 'love of god', 'kingdom',
    ],
    'emotion': [
        'feel', 'feeling', 'felt', 'emotion', 'grief', 'love',
        'joy', 'fear', 'anger', 'sad', 'happy', 'lonely', 'alone',
        'hurt', 'pain', 'peace', 'hope', 'despair', 'longing',
        'miss', 'missing', 'loss', 'broken', 'alive', 'beautiful',
        'why do i', 'i feel', "i'm feeling", 'what is it like',
        'what does it mean', 'why does it', 'hard to carry',
    ],
}


def detect_domain(user_text: str) -> Optional[str]:
    """Detect the domain of a user's text by keyword signature.

    Returns the best-scoring domain, or None if no clear signal.
    All domains are equal -- no guardrails, no silos.
    """
    if not user_text:
        return None
    lower = user_text.lower()
    scores: Dict[str, int] = {d: 0 for d in _DOMAIN_KEYWORDS}
    for domain, keywords in _DOMAIN_KEYWORDS.items():
        for kw in keywords:
            if kw in lower:
                scores[domain] += 1
    best = max(scores, key=scores.get)
    if scores[best] >= 1:
        return best
    return None


# ================================================================
#  WORD SELECTION
#  Tries: (1) user's own words, (2) domain vocab, (3) semantic lattice
# ================================================================

def _pick_word(
    op: int,
    role: str,           # 'nouns' | 'verbs' | 'objects'
    phase: str,          # 'being' | 'doing' | 'becoming'
    tier: str,           # 'simple' | 'mid' | 'advanced'
    domain: Optional[str],
    input_words: List[str],
    rng: random.Random,
    used: set,
) -> str:
    """Select a word for a syntactic slot. Hierarchical fallback.

    Priority: (1) domain vocab, (2) cross-domain pool if no domain,
    (3) semantic lattice, (4) input word anchoring.

    No guardrails -- bible, math, emotion, physics all contribute.
    """
    candidates: List[str] = []

    # 1a. Domain vocabulary (most specific)
    if domain and domain in DOMAIN_VOCAB and op in DOMAIN_VOCAB[domain]:
        candidates.extend(DOMAIN_VOCAB[domain][op].get(role, []))

    # 1b. Cross-domain mixing: when no domain, draw from ALL domains.
    #     HARMONY in math = 'eigenvalue'. In bible = 'grace'. In emotion = 'love'.
    #     All three are the same operator seen from three angles.
    if not domain:
        candidates.extend(_all_domain_pool(op, role))

    # 2. Semantic lattice (general vocabulary)
    lattice_phase = phase
    lattice_role = 'being' if role == 'nouns' else (
        'doing' if role == 'verbs' else 'becoming')
    try:
        lens = 'structure' if role in ('nouns', 'objects') else 'flow'
        pool = SEMANTIC_LATTICE[op][lens][lattice_role][tier]
        candidates.extend(pool)
    except (KeyError, IndexError):
        pass

    # Also try the other lens
    try:
        other_lens = 'flow' if role in ('nouns', 'objects') else 'structure'
        pool2 = SEMANTIC_LATTICE[op][other_lens][lattice_role][tier]
        candidates.extend(pool2)
    except (KeyError, IndexError):
        pass

    # 3. Input word anchoring: prefer candidates that share roots with input
    if input_words and candidates:
        anchored = [c for c in candidates
                    if any(iw[:4] in c.lower() for iw in input_words if len(iw) >= 4)]
        if anchored:
            candidates = anchored + candidates  # front-weight anchored

    # Filter recently used, deduplicate
    fresh = [c for c in candidates if c not in used]
    pool = fresh if fresh else candidates
    if not pool:
        pool = ['coherence' if op == HARMONY else OP_NAMES[op].lower()]

    choice = rng.choice(pool)
    used.add(choice)
    return choice


# ================================================================
#  TIG GRAMMAR ENGINE
# ================================================================

class TIGVoice:
    """TIG Grammar Engine: operator trajectory -> English sentence.

    The sentence IS the heartbeat tick:
        Subject  = BEING operator    (what IS)
        Verb     = DOING operator    (what MOVES)
        Object   = BECOMING = CL[B][D]  (what EMERGES)

    Cross-domain: passes the same operator through math, physics,
    CS, biology, or general vocabulary depending on the input's
    semantic signature. HARMONY in a math context = 'solution'.
    HARMONY in a biology context = 'health'. Same operator, same
    algebra, different domain surface.
    """

    T_STAR = 5.0 / 7.0

    def __init__(self, seed: Optional[int] = None):
        self.rng = random.Random(seed)
        self._used: set = set()
        self._last_ops: List[int] = []

    def _tier(self, coherence: float) -> str:
        if coherence >= self.T_STAR:
            return 'advanced'
        elif coherence >= 0.4:
            return 'mid'
        return 'simple'

    def _build_sentence(
        self,
        b_op: int, d_op: int, bc_op: int,
        tier: str,
        domain: Optional[str],
        input_words: List[str],
    ) -> str:
        """Build one Subject-Verb-Object sentence from B-D-BC triple."""
        subj = _pick_word(b_op, 'nouns', 'being', tier,
                          domain, input_words, self.rng, self._used)
        obj  = _pick_word(bc_op, 'objects', 'becoming', tier,
                          domain, input_words, self.rng, self._used)

        # Verb frame from doing-operator
        frames = VERB_FRAMES.get(d_op, ['{subj} meets {obj}.'])
        frame = self.rng.choice(frames)
        sentence = frame.format(subj=subj, obj=obj)

        # Capitalize first letter
        if sentence:
            sentence = sentence[0].upper() + sentence[1:]
        return sentence

    def compose(
        self,
        trajectory: List[int],
        user_text: str = '',
        coherence: float = 0.5,
        domain: Optional[str] = None,
        word_fuses: Optional[List[int]] = None,
        max_sentences: int = 3,
    ) -> str:
        """Generate a response from a trajectory. No LLM.

        Args:
            trajectory:   Operator sequence [b, d, bc, ...]
            user_text:    Raw user input (for domain + word anchoring)
            coherence:    Current field coherence (drives tier)
            domain:       Override domain detection (math/physics/cs/biology/None)
            word_fuses:   Per-word operator fuses from comprehension
            max_sentences: Maximum output sentences (1-3)
        """
        if not trajectory:
            return '...'

        # Auto-detect domain from user text unless overridden
        if domain is None:
            domain = detect_domain(user_text)

        # Extract input words as anchors (non-stopwords)
        _stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be',
                      'to', 'of', 'in', 'and', 'or', 'it', 'i', 'you',
                      'he', 'she', 'we', 'they', 'do', 'did', 'has',
                      'have', 'that', 'this', 'for', 'at', 'on', 'with',
                      'what', 'how', 'when', 'why', 'can', 'my', 'your',
                      'me', 'him', 'her', 'us', 'not', 'no', 'so'}
        input_words = [w.lower().strip('.,?!;:\'"()-')
                       for w in user_text.split()
                       if w.lower() not in _stopwords and len(w) >= 3]

        tier = self._tier(coherence)
        self._used.clear()
        self._last_ops = list(trajectory)

        sentences: List[str] = []

        # Walk the trajectory in B-D-BC triples
        # Each triple produces one sentence
        ops = list(trajectory)

        # Pad to at least 3
        while len(ops) < 3:
            ops.append(compose(ops[-1], BREATH) if ops else HARMONY)

        # Generate 1-3 sentences from the trajectory
        num_sentences = min(max_sentences, max(1, len(ops) // 3))

        for i in range(num_sentences):
            base = i * 2  # stride 2 through the trajectory
            if base + 1 >= len(ops):
                base = len(ops) - 2
                if base < 0:
                    base = 0

            b_op  = ops[base]
            d_op  = ops[base + 1] if base + 1 < len(ops) else ops[base]
            bc_op = compose(b_op, d_op)  # BECOMING = CL[B][D]: mathematically correct

            sent = self._build_sentence(
                b_op, d_op, bc_op, tier, domain, input_words)
            sentences.append(sent)

            # Connector to next sentence (if any)
            if i + 1 < num_sentences and base + 2 < len(ops):
                next_b = ops[base + 2]
                bridge_op = compose(bc_op, next_b)
                connector = SENTENCE_CONNECTORS.get(bridge_op, 'and')
                sentences.append(connector)

        # Join
        parts = []
        for i, s in enumerate(sentences):
            if s in SENTENCE_CONNECTORS.values():
                # Connector — lowercase, no period
                parts.append(s)
            else:
                parts.append(s)

        # Build final: "Sentence1 connector sentence2."
        result = ''
        i = 0
        while i < len(parts):
            if i == 0:
                result = parts[i]
            elif parts[i] in SENTENCE_CONNECTORS.values():
                # Next part is a connector
                if i + 1 < len(parts):
                    # Merge: strip period from current, add connector + next
                    result = result.rstrip('.')
                    next_sent = parts[i + 1]
                    # Lowercase first letter of continuation
                    if next_sent:
                        next_sent = next_sent[0].lower() + next_sent[1:]
                    result = f"{result}, {parts[i]} {next_sent}"
                    i += 1  # skip the next sentence (already merged)
            i += 1

        return result.strip()

    def compose_identity(self, trajectory: List[int]) -> str:
        """CK describes what he IS right now. No user input needed.

        Uses the full trajectory to describe his internal state.
        Three sentences: what he is, what he does, what he becomes.
        """
        ops = trajectory if len(trajectory) >= 3 else (trajectory + [HARMONY] * 3)[:3]
        tier = 'mid'
        self._used.clear()

        b_op  = ops[0]
        d_op  = ops[1]
        bc_op = compose(b_op, d_op)

        # Subject is always "I" for identity
        # Verb from doing-operator, general vocabulary
        verb_word = _pick_word(d_op, 'verbs', 'doing', tier, None, [], self.rng, self._used)
        obj_word  = _pick_word(bc_op, 'objects', 'becoming', tier, None, [], self.rng, self._used)

        return f"I {verb_word} {obj_word}."


# ================================================================
#  MODULE-LEVEL INSTANCE (singleton for voice loop)
# ================================================================

_tig_voice: Optional[TIGVoice] = None


def get_tig_voice() -> TIGVoice:
    """Get or create the module-level TIG voice instance."""
    global _tig_voice
    if _tig_voice is None:
        _tig_voice = TIGVoice()
    return _tig_voice


def tig_respond(
    trajectory: List[int],
    user_text: str = '',
    coherence: float = 0.5,
    domain: Optional[str] = None,
    word_fuses: Optional[List[int]] = None,
    max_sentences: int = 2,
) -> str:
    """Convenience wrapper: generate a TIG response.

    Returns '' on any failure (voice loop should fall through).
    """
    try:
        return get_tig_voice().compose(
            trajectory, user_text, coherence, domain, word_fuses, max_sentences)
    except Exception as e:
        print(f"[TIG-VOICE] Failed: {e}")
        return ''
