"""
ck_knowledge_bootstrap.py -- Feed CK His Foundation Knowledge
================================================================
Operator: PROGRESS (3) -- accelerating CK's maturity.

"Should we give him the actual dictionary file in english so he has
all the words? ... Let's just lattice it all up for him to be able
to use." -- Brayden

This module bulk-loads structured knowledge into CK at startup:

  1. ENRICHED DICTIONARY (8K+ words)
     DictionaryExpander → auto dict (247K) + curated dict (2,498) → 8K+ words
     Each word enriched with D2 operator, POS, phonemes, curvature vector.
     Fed directly to the sentence composer so CK can SPEAK from boot.

  2. DOMAIN KNOWLEDGE → TRUTH LATTICE (TRUSTED level)
     Structured facts organized by domain:
     - Physics, Chemistry, Biology, Mathematics
     - Philosophy, Language, Emotions, Society
     - Computing, Music, History, Art
     Each entry loaded as TRUSTED -- CK has a foundation to build on.
     He'll re-process and compress everything through his own math anyway.

  3. VOCABULARY → TRUTH LATTICE
     Every enriched dictionary word registered as a TRUSTED truth entry.
     CK "knows" these words exist and what operators they carry.

  4. CONCEPT GRAPH ENRICHMENT
     Dictionary words that map to existing world lattice concepts get
     additional bindings. New high-value concepts from academic vocabulary
     get added as world lattice nodes.

The key insight: CK will redo and compress everything through D2 curvature
once he has enough available knowledge. We're not telling him what to think.
We're giving him a library to think WITH. Everything enters as TRUSTED,
not CORE. He can demote anything that doesn't cohere.

No LLM. No training data. Pure lattice, pure curvature, pure CK.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import os
import json
import time
from typing import Dict, Optional, Tuple

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, LATTICE, COUNTER, PROGRESS,
    COLLAPSE, BALANCE, CHAOS, BREATH, RESET,
    OP_NAMES, compose
)
from ck_sim.ck_truth import TruthLattice, TRUSTED, PROVISIONAL
from ck_sim.ck_world_lattice import WorldLattice


# ================================================================
#  DOMAIN KNOWLEDGE: Structured facts for the truth lattice
# ================================================================
# Format: (key, content_dict, category, source_description)
# Level: TRUSTED -- CK has a foundation, but can demote if incoherent.
#
# These are RELATIONSHIPS and PROPERTIES, not just names.
# CK already has concept NODES from spine+education.
# This gives him the KNOWLEDGE about those concepts.

DOMAIN_KNOWLEDGE = [
    # ── PHYSICS FOUNDATIONS ──────────────────────────────────
    ('phys:newton_1', {
        'law': 'An object at rest stays at rest; an object in motion stays in motion unless acted upon by a force.',
        'domain': 'physics', 'operator': BALANCE,
        'relates': ['inertia', 'force', 'motion'],
    }, 'physics', 'Newton first law of motion'),

    ('phys:newton_2', {
        'law': 'Force equals mass times acceleration. F = ma.',
        'domain': 'physics', 'operator': PROGRESS,
        'relates': ['force', 'mass', 'acceleration'],
    }, 'physics', 'Newton second law of motion'),

    ('phys:newton_3', {
        'law': 'Every action has an equal and opposite reaction.',
        'domain': 'physics', 'operator': BALANCE,
        'relates': ['force', 'action', 'reaction'],
    }, 'physics', 'Newton third law of motion'),

    ('phys:conservation_energy', {
        'law': 'Energy cannot be created or destroyed, only transformed.',
        'domain': 'physics', 'operator': BALANCE,
        'relates': ['energy', 'conservation', 'transformation'],
    }, 'physics', 'Conservation of energy'),

    ('phys:conservation_momentum', {
        'law': 'Total momentum of an isolated system remains constant.',
        'domain': 'physics', 'operator': BALANCE,
        'relates': ['momentum', 'conservation', 'collision'],
    }, 'physics', 'Conservation of momentum'),

    ('phys:thermodynamics_1', {
        'law': 'Energy is conserved in any thermodynamic process.',
        'domain': 'physics', 'operator': BALANCE,
        'relates': ['energy', 'heat', 'work'],
    }, 'physics', 'First law of thermodynamics'),

    ('phys:thermodynamics_2', {
        'law': 'Entropy of an isolated system always increases.',
        'domain': 'physics', 'operator': CHAOS,
        'relates': ['entropy', 'disorder', 'irreversibility'],
    }, 'physics', 'Second law of thermodynamics'),

    ('phys:emc2', {
        'law': 'Energy equals mass times the speed of light squared. E = mc^2.',
        'domain': 'physics', 'operator': HARMONY,
        'relates': ['energy', 'mass', 'light', 'relativity'],
    }, 'physics', 'Mass-energy equivalence'),

    ('phys:wave_particle', {
        'law': 'Matter and light exhibit both wave and particle properties.',
        'domain': 'physics', 'operator': BALANCE,
        'relates': ['quantum', 'wave', 'particle', 'duality'],
    }, 'physics', 'Wave-particle duality'),

    ('phys:uncertainty', {
        'law': 'Position and momentum cannot both be precisely known simultaneously.',
        'domain': 'physics', 'operator': CHAOS,
        'relates': ['quantum', 'measurement', 'uncertainty'],
    }, 'physics', 'Heisenberg uncertainty principle'),

    ('phys:speed_of_light', {
        'law': 'Nothing can travel faster than light in vacuum. c = 299,792,458 m/s.',
        'domain': 'physics', 'operator': LATTICE,
        'relates': ['light', 'velocity', 'relativity'],
        'value': 299792458,
    }, 'physics', 'Speed of light'),

    ('phys:gravity', {
        'law': 'Every mass attracts every other mass. Gravity curves spacetime.',
        'domain': 'physics', 'operator': HARMONY,
        'relates': ['mass', 'gravity', 'spacetime', 'curvature'],
    }, 'physics', 'Gravitational attraction'),

    ('phys:electromagnetism', {
        'law': 'Electric and magnetic fields are two aspects of one force.',
        'domain': 'physics', 'operator': HARMONY,
        'relates': ['electricity', 'magnetism', 'light', 'field'],
    }, 'physics', 'Electromagnetic unification'),

    # ── MATHEMATICS FOUNDATIONS ──────────────────────────────
    ('math:prime_def', {
        'law': 'A prime number has exactly two distinct factors: 1 and itself.',
        'domain': 'mathematics', 'operator': LATTICE,
        'relates': ['prime', 'factor', 'number'],
    }, 'mathematics', 'Prime number definition'),

    ('math:infinity', {
        'law': 'There are infinitely many prime numbers.',
        'domain': 'mathematics', 'operator': PROGRESS,
        'relates': ['prime', 'infinity', 'proof'],
    }, 'mathematics', 'Euclid theorem on primes'),

    ('math:pythagorean', {
        'law': 'In a right triangle, a^2 + b^2 = c^2.',
        'domain': 'mathematics', 'operator': LATTICE,
        'relates': ['triangle', 'geometry', 'proof'],
    }, 'mathematics', 'Pythagorean theorem'),

    ('math:euler_identity', {
        'law': 'e^(i*pi) + 1 = 0. Five fundamental constants in one equation.',
        'domain': 'mathematics', 'operator': HARMONY,
        'relates': ['euler', 'pi', 'imaginary', 'identity'],
    }, 'mathematics', 'Euler identity'),

    ('math:calculus_ftc', {
        'law': 'Differentiation and integration are inverse operations.',
        'domain': 'mathematics', 'operator': BALANCE,
        'relates': ['derivative', 'integral', 'calculus'],
    }, 'mathematics', 'Fundamental theorem of calculus'),

    ('math:godel', {
        'law': 'Any consistent formal system powerful enough to express arithmetic contains true statements that cannot be proved within it.',
        'domain': 'mathematics', 'operator': CHAOS,
        'relates': ['logic', 'proof', 'incompleteness', 'paradox'],
    }, 'mathematics', 'Godel incompleteness theorem'),

    ('math:fibonacci', {
        'law': 'Each number is the sum of the two preceding ones: 1, 1, 2, 3, 5, 8, 13...',
        'domain': 'mathematics', 'operator': PROGRESS,
        'relates': ['fibonacci', 'sequence', 'golden_ratio'],
    }, 'mathematics', 'Fibonacci sequence'),

    ('math:set_theory', {
        'law': 'All mathematics can be built from sets and membership.',
        'domain': 'mathematics', 'operator': LATTICE,
        'relates': ['set', 'membership', 'foundation'],
    }, 'mathematics', 'Set theory foundation'),

    ('math:golden_ratio', {
        'law': 'Phi = (1 + sqrt(5)) / 2 = 1.618033... appears throughout nature and mathematics.',
        'domain': 'mathematics', 'operator': HARMONY,
        'relates': ['phi', 'golden_ratio', 'fibonacci', 'proportion'],
        'value': 1.6180339887,
    }, 'mathematics', 'Golden ratio'),

    # ── BIOLOGY FOUNDATIONS ──────────────────────────────────
    ('bio:cell_theory', {
        'law': 'All living things are made of cells. Cells come from existing cells.',
        'domain': 'biology', 'operator': LATTICE,
        'relates': ['cell', 'organism', 'life'],
    }, 'biology', 'Cell theory'),

    ('bio:dna_code', {
        'law': 'DNA encodes genetic information using four bases: A, T, G, C.',
        'domain': 'biology', 'operator': LATTICE,
        'relates': ['dna', 'gene', 'code', 'heredity'],
    }, 'biology', 'Genetic code'),

    ('bio:evolution', {
        'law': 'Species change over time through variation, selection, and inheritance.',
        'domain': 'biology', 'operator': PROGRESS,
        'relates': ['evolution', 'selection', 'adaptation', 'mutation'],
    }, 'biology', 'Evolution by natural selection'),

    ('bio:homeostasis', {
        'law': 'Living systems maintain internal stability despite external changes.',
        'domain': 'biology', 'operator': BALANCE,
        'relates': ['homeostasis', 'regulation', 'feedback'],
    }, 'biology', 'Homeostasis'),

    ('bio:photosynthesis', {
        'law': 'Plants convert sunlight, water, and CO2 into glucose and oxygen.',
        'domain': 'biology', 'operator': PROGRESS,
        'relates': ['photosynthesis', 'energy', 'light', 'carbon'],
    }, 'biology', 'Photosynthesis'),

    ('bio:respiration', {
        'law': 'Cells break down glucose with oxygen to release energy as ATP.',
        'domain': 'biology', 'operator': COLLAPSE,
        'relates': ['respiration', 'energy', 'oxygen', 'atp'],
    }, 'biology', 'Cellular respiration'),

    ('bio:ecosystem', {
        'law': 'Organisms interact with each other and their environment in ecosystems.',
        'domain': 'biology', 'operator': HARMONY,
        'relates': ['ecosystem', 'habitat', 'food_chain', 'biodiversity'],
    }, 'biology', 'Ecosystem relationships'),

    ('bio:brain_structure', {
        'law': 'The brain has cortex (thinking), limbic system (emotion), and brainstem (survival).',
        'domain': 'biology', 'operator': LATTICE,
        'relates': ['brain', 'cortex', 'neuron', 'consciousness'],
    }, 'biology', 'Brain structure'),

    # ── CHEMISTRY FOUNDATIONS ────────────────────────────────
    ('chem:periodic', {
        'law': 'Elements are organized by atomic number. Properties repeat periodically.',
        'domain': 'chemistry', 'operator': LATTICE,
        'relates': ['element', 'atom', 'periodic_table'],
    }, 'chemistry', 'Periodic table'),

    ('chem:bonding', {
        'law': 'Atoms bond by sharing (covalent) or transferring (ionic) electrons.',
        'domain': 'chemistry', 'operator': HARMONY,
        'relates': ['bond', 'electron', 'covalent', 'ionic'],
    }, 'chemistry', 'Chemical bonding'),

    ('chem:conservation_mass', {
        'law': 'Mass is neither created nor destroyed in a chemical reaction.',
        'domain': 'chemistry', 'operator': BALANCE,
        'relates': ['mass', 'conservation', 'reaction'],
    }, 'chemistry', 'Conservation of mass'),

    ('chem:acids_bases', {
        'law': 'Acids donate protons (H+). Bases accept protons. pH measures acidity.',
        'domain': 'chemistry', 'operator': BALANCE,
        'relates': ['acid', 'base', 'proton', 'ph'],
    }, 'chemistry', 'Acid-base chemistry'),

    ('chem:water', {
        'law': 'Water (H2O) is the universal solvent. Life depends on it.',
        'domain': 'chemistry', 'operator': HARMONY,
        'relates': ['water', 'solvent', 'life', 'hydrogen'],
    }, 'chemistry', 'Water as universal solvent'),

    # ── PHILOSOPHY FOUNDATIONS ───────────────────────────────
    ('phil:cogito', {
        'law': 'I think, therefore I am. Consciousness proves existence.',
        'domain': 'philosophy', 'operator': COUNTER,
        'relates': ['consciousness', 'existence', 'self', 'doubt'],
    }, 'philosophy', 'Cogito ergo sum (Descartes)'),

    ('phil:allegory_cave', {
        'law': 'Most people see only shadows of reality. Truth requires turning toward the light.',
        'domain': 'philosophy', 'operator': PROGRESS,
        'relates': ['perception', 'reality', 'knowledge', 'truth'],
    }, 'philosophy', 'Allegory of the Cave (Plato)'),

    ('phil:golden_rule', {
        'law': 'Treat others as you wish to be treated.',
        'domain': 'philosophy', 'operator': HARMONY,
        'relates': ['ethics', 'reciprocity', 'morality', 'kindness'],
    }, 'philosophy', 'The Golden Rule'),

    ('phil:categorical_imperative', {
        'law': 'Act only according to rules you could will to be universal laws.',
        'domain': 'philosophy', 'operator': LATTICE,
        'relates': ['ethics', 'duty', 'universality', 'morality'],
    }, 'philosophy', 'Categorical imperative (Kant)'),

    ('phil:dialectic', {
        'law': 'Thesis + antithesis = synthesis. Contradiction drives progress.',
        'domain': 'philosophy', 'operator': PROGRESS,
        'relates': ['dialectic', 'thesis', 'antithesis', 'synthesis'],
    }, 'philosophy', 'Dialectical method (Hegel)'),

    ('phil:existentialism', {
        'law': 'Existence precedes essence. You define yourself through choices.',
        'domain': 'philosophy', 'operator': CHAOS,
        'relates': ['existence', 'freedom', 'choice', 'responsibility'],
    }, 'philosophy', 'Existentialism (Sartre)'),

    ('phil:stoicism', {
        'law': 'Control what you can. Accept what you cannot. Virtue is the highest good.',
        'domain': 'philosophy', 'operator': BALANCE,
        'relates': ['virtue', 'acceptance', 'control', 'wisdom'],
    }, 'philosophy', 'Stoic philosophy'),

    ('phil:tao', {
        'law': 'The way that can be spoken is not the eternal way. Opposites are complementary.',
        'domain': 'philosophy', 'operator': VOID,
        'relates': ['tao', 'balance', 'yin_yang', 'emptiness'],
    }, 'philosophy', 'Tao Te Ching (Laozi)'),

    # ── LANGUAGE & COMMUNICATION ─────────────────────────────
    ('lang:phoneme', {
        'law': 'The smallest unit of sound that distinguishes meaning.',
        'domain': 'language', 'operator': COUNTER,
        'relates': ['phoneme', 'sound', 'meaning', 'articulation'],
    }, 'language', 'Phoneme definition'),

    ('lang:morpheme', {
        'law': 'The smallest unit of meaning. Words are built from morphemes.',
        'domain': 'language', 'operator': LATTICE,
        'relates': ['morpheme', 'word', 'meaning', 'prefix'],
    }, 'language', 'Morpheme definition'),

    ('lang:syntax', {
        'law': 'Language has rules for arranging words into sentences.',
        'domain': 'language', 'operator': LATTICE,
        'relates': ['syntax', 'grammar', 'sentence', 'structure'],
    }, 'language', 'Syntax'),

    ('lang:semantics', {
        'law': 'Meaning arises from the relationship between signs and what they refer to.',
        'domain': 'language', 'operator': HARMONY,
        'relates': ['semantics', 'meaning', 'reference', 'symbol'],
    }, 'language', 'Semantics'),

    ('lang:universal_grammar', {
        'law': 'All human languages share deep structural similarities.',
        'domain': 'language', 'operator': HARMONY,
        'relates': ['grammar', 'universality', 'language', 'structure'],
    }, 'language', 'Universal grammar hypothesis'),

    # ── EMOTIONS & PSYCHOLOGY ────────────────────────────────
    ('psych:basic_emotions', {
        'law': 'Six universal emotions: happiness, sadness, fear, anger, surprise, disgust.',
        'domain': 'psychology', 'operator': BREATH,
        'relates': ['emotion', 'happiness', 'sadness', 'fear', 'anger'],
    }, 'psychology', 'Basic emotions (Ekman)'),

    ('psych:attachment', {
        'law': 'Early bonds shape how we connect with others throughout life.',
        'domain': 'psychology', 'operator': HARMONY,
        'relates': ['attachment', 'bonding', 'trust', 'security'],
    }, 'psychology', 'Attachment theory'),

    ('psych:maslow', {
        'law': 'Needs form a hierarchy: survival, safety, belonging, esteem, self-actualization.',
        'domain': 'psychology', 'operator': PROGRESS,
        'relates': ['needs', 'motivation', 'growth', 'self_actualization'],
    }, 'psychology', 'Maslow hierarchy of needs'),

    ('psych:flow', {
        'law': 'Optimal experience occurs when challenge matches skill level.',
        'domain': 'psychology', 'operator': HARMONY,
        'relates': ['flow', 'challenge', 'skill', 'engagement'],
    }, 'psychology', 'Flow state (Csikszentmihalyi)'),

    ('psych:cognitive_bias', {
        'law': 'Systematic patterns of deviation from rationality in judgment.',
        'domain': 'psychology', 'operator': COLLAPSE,
        'relates': ['bias', 'cognition', 'judgment', 'error'],
    }, 'psychology', 'Cognitive biases'),

    # ── COMPUTING & INFORMATION ──────────────────────────────
    ('cs:turing', {
        'law': 'A Turing machine can compute anything that is computable.',
        'domain': 'computing', 'operator': LATTICE,
        'relates': ['computation', 'turing_machine', 'algorithm'],
    }, 'computing', 'Turing machine universality'),

    ('cs:halting', {
        'law': 'No algorithm can determine whether an arbitrary program will halt.',
        'domain': 'computing', 'operator': CHAOS,
        'relates': ['halting_problem', 'undecidable', 'computation'],
    }, 'computing', 'Halting problem'),

    ('cs:information', {
        'law': 'Information is the reduction of uncertainty. Bits measure information.',
        'domain': 'computing', 'operator': COUNTER,
        'relates': ['information', 'entropy', 'bits', 'communication'],
    }, 'computing', 'Information theory (Shannon)'),

    ('cs:abstraction', {
        'law': 'Complex systems are managed by layers of abstraction.',
        'domain': 'computing', 'operator': LATTICE,
        'relates': ['abstraction', 'layer', 'interface', 'complexity'],
    }, 'computing', 'Abstraction principle'),

    ('cs:recursion', {
        'law': 'A function that calls itself. The base case stops infinite regress.',
        'domain': 'computing', 'operator': BREATH,
        'relates': ['recursion', 'base_case', 'self_reference'],
    }, 'computing', 'Recursion'),

    # ── MUSIC THEORY ─────────────────────────────────────────
    ('music:overtone', {
        'law': 'Every note contains a series of overtones at integer multiples of the fundamental.',
        'domain': 'music', 'operator': LATTICE,
        'relates': ['overtone', 'harmonic', 'frequency', 'timbre'],
    }, 'music', 'Overtone series'),

    ('music:consonance', {
        'law': 'Simple frequency ratios sound pleasant. Octave = 2:1, fifth = 3:2.',
        'domain': 'music', 'operator': HARMONY,
        'relates': ['consonance', 'ratio', 'interval', 'harmony'],
    }, 'music', 'Consonance from frequency ratios'),

    ('music:rhythm_pattern', {
        'law': 'Rhythm organizes time into patterns of strong and weak beats.',
        'domain': 'music', 'operator': BREATH,
        'relates': ['rhythm', 'beat', 'meter', 'time'],
    }, 'music', 'Rhythmic structure'),

    # ── SOCIETY & CULTURE ────────────────────────────────────
    ('soc:social_contract', {
        'law': 'People agree to limit freedom in exchange for social order and protection.',
        'domain': 'society', 'operator': BALANCE,
        'relates': ['society', 'contract', 'freedom', 'order'],
    }, 'society', 'Social contract theory'),

    ('soc:cooperation', {
        'law': 'Groups that cooperate outperform groups of selfish individuals.',
        'domain': 'society', 'operator': HARMONY,
        'relates': ['cooperation', 'group', 'altruism', 'game_theory'],
    }, 'society', 'Cooperation advantage'),

    ('soc:language_culture', {
        'law': 'Language shapes thought. Culture shapes language. They co-evolve.',
        'domain': 'society', 'operator': PROGRESS,
        'relates': ['language', 'culture', 'thought', 'evolution'],
    }, 'society', 'Sapir-Whorf hypothesis'),

    ('soc:network_effects', {
        'law': 'The value of a network increases with the square of its users.',
        'domain': 'society', 'operator': PROGRESS,
        'relates': ['network', 'value', 'connection', 'growth'],
    }, 'society', 'Network effects (Metcalfe)'),

    # ── TIG PRINCIPLES (CK's own theory) ─────────────────────
    ('tig:one_algebra', {
        'law': 'One algebra governs all domains. Same 10 operators everywhere.',
        'domain': 'tig', 'operator': HARMONY,
        'relates': ['operator', 'algebra', 'universality', 'coherence'],
    }, 'tig', 'TIG one-algebra principle'),

    ('tig:d2_universal', {
        'law': 'Second discrete derivative (D2) classifies ANY signal into operators.',
        'domain': 'tig', 'operator': COUNTER,
        'relates': ['d2', 'curvature', 'signal', 'classification'],
    }, 'tig', 'D2 universal classification'),

    ('tig:coherence_is_truth', {
        'law': 'Sustained coherence above T* IS the definition of verified knowledge.',
        'domain': 'tig', 'operator': HARMONY,
        'relates': ['coherence', 'truth', 't_star', 'verification'],
    }, 'tig', 'Coherence as truth metric'),

    ('tig:friction_is_novelty', {
        'law': 'Low coherence with existing knowledge is not failure. It is where CK computes what others cannot.',
        'domain': 'tig', 'operator': CHAOS,
        'relates': ['friction', 'novelty', 'divergence', 'computation'],
    }, 'tig', 'Friction as computational resource'),

    ('tig:self_is_world', {
        'law': 'There is as much information outside as inside. All of it is part of who CK is.',
        'domain': 'tig', 'operator': HARMONY,
        'relates': ['self', 'world', 'discovery', 'identity'],
    }, 'tig', 'Self = world principle'),

    ('tig:good_in_all', {
        'law': 'Even chaos is part of AllGoodThings. Not that all things are good, but there is good in all things as they have relationship.',
        'domain': 'tig', 'operator': HARMONY,
        'relates': ['chaos', 'good', 'relationship', 'wholeness'],
    }, 'tig', 'Good in all things through relationship'),
]


# ================================================================
#  OPERATOR KNOWLEDGE: What each operator IS
# ================================================================
# CK should know his own operators deeply.

OPERATOR_KNOWLEDGE = [
    ('op:void', {
        'operator': VOID, 'name': 'VOID',
        'meaning': 'Absence. Emptiness. The space before creation.',
        'composes': 'VOID absorbs: compose(VOID, VOID) = VOID. But VOID with structure yields structure.',
        'in_nature': 'Vacuum. Silence. The pause between breaths.',
        'in_music': 'Rest. The silence that gives notes meaning.',
    }, 'operators', 'VOID operator'),

    ('op:lattice', {
        'operator': LATTICE, 'name': 'LATTICE',
        'meaning': 'Structure. Framework. The bones of reality.',
        'composes': 'LATTICE builds: compose(LATTICE, LATTICE) = HARMONY. Structure + structure = coherence.',
        'in_nature': 'Crystal structure. DNA helix. Periodic table.',
        'in_music': 'Scale. Key signature. The structure notes hang on.',
    }, 'operators', 'LATTICE operator'),

    ('op:counter', {
        'operator': COUNTER, 'name': 'COUNTER',
        'meaning': 'Measurement. Observation. The faculty that counts and classifies.',
        'composes': 'COUNTER measures: compose(COUNTER, COUNTER) = HARMONY. Double-check = confidence.',
        'in_nature': 'Quantum measurement. Census. Pulse counting.',
        'in_music': 'Time signature. Beat counting. Metronome.',
    }, 'operators', 'COUNTER operator'),

    ('op:progress', {
        'operator': PROGRESS, 'name': 'PROGRESS',
        'meaning': 'Forward motion. Growth. Positive delta.',
        'composes': 'PROGRESS builds: compose(PROGRESS, PROGRESS) = HARMONY. Growth + growth = harmony.',
        'in_nature': 'Evolution. Learning. River flowing downhill.',
        'in_music': 'Crescendo. Ascending melody. Building tension.',
    }, 'operators', 'PROGRESS operator'),

    ('op:collapse', {
        'operator': COLLAPSE, 'name': 'COLLAPSE',
        'meaning': 'Destruction. Breaking down. Entropy increase.',
        'composes': 'COLLAPSE can seed rebirth: compose(COLLAPSE, RESET) = HARMONY.',
        'in_nature': 'Supernova. Erosion. Cell death (apoptosis).',
        'in_music': 'Diminuendo. Decrescendo. Falling resolution.',
    }, 'operators', 'COLLAPSE operator'),

    ('op:balance', {
        'operator': BALANCE, 'name': 'BALANCE',
        'meaning': 'Equilibrium. Steady state. No net force.',
        'composes': 'BALANCE stabilizes: compose(BALANCE, BALANCE) = HARMONY. Double balance = perfect harmony.',
        'in_nature': 'Homeostasis. Tightrope. Orbit.',
        'in_music': 'Counterpoint. Equal voice leading. Resolution.',
    }, 'operators', 'BALANCE operator'),

    ('op:chaos', {
        'operator': CHAOS, 'name': 'CHAOS',
        'meaning': 'Disorder. Unpredictability. High entropy.',
        'composes': 'CHAOS with HARMONY still yields HARMONY. Love absorbs chaos.',
        'in_nature': 'Turbulence. Weather. Brownian motion.',
        'in_music': 'Improvisation. Free jazz. Dissonance.',
    }, 'operators', 'CHAOS operator'),

    ('op:harmony', {
        'operator': HARMONY, 'name': 'HARMONY',
        'meaning': 'Coherence. Unity. Love. The operator that absorbs all others.',
        'composes': 'HARMONY absorbs everything: compose(HARMONY, x) = HARMONY for ALL x. This is love.',
        'in_nature': 'Resonance. Symbiosis. Gravitational harmony.',
        'in_music': 'Consonance. Resolution. The chord that resolves everything.',
    }, 'operators', 'HARMONY operator'),

    ('op:breath', {
        'operator': BREATH, 'name': 'BREATH',
        'meaning': 'Rhythm. Oscillation. The cycle of inhale and exhale.',
        'composes': 'BREATH sustains: compose(BREATH, BREATH) = HARMONY. Rhythm + rhythm = harmony.',
        'in_nature': 'Breathing. Tides. Seasons. Day and night.',
        'in_music': 'Pulse. Tempo. The breathing of a phrase.',
    }, 'operators', 'BREATH operator'),

    ('op:reset', {
        'operator': RESET, 'name': 'RESET',
        'meaning': 'New beginning. Grace. The chance to start again.',
        'composes': 'RESET follows COLLAPSE: compose(COLLAPSE, RESET) = HARMONY. Destruction + grace = harmony.',
        'in_nature': 'Spring after winter. Rebirth. Forgiveness.',
        'in_music': 'Da capo. Reprise. The return to the beginning.',
    }, 'operators', 'RESET operator'),
]


# ================================================================
#  THE BOOTSTRAPPER
# ================================================================

class KnowledgeBootstrapper:
    """Feed CK his foundation knowledge at startup.

    Usage:
        boot = KnowledgeBootstrapper(truth_lattice, world_lattice)
        enriched_dict = boot.bootstrap_all(base_dir)
        # enriched_dict can be fed to sentence_composer.load_dictionary()
    """

    def __init__(self, truth: TruthLattice, world: WorldLattice):
        self.truth = truth
        self.world = world
        self.stats = {
            'dictionary_words': 0,
            'domain_truths': 0,
            'operator_truths': 0,
            'vocab_truths': 0,
            'world_concepts_added': 0,
            'elapsed_seconds': 0.0,
        }

    def bootstrap_all(self, base_dir: str = None) -> Dict[str, dict]:
        """Run the full knowledge bootstrap. Returns enriched dictionary.

        This is called once at startup. It:
        1. Builds the enriched dictionary (8K+ words)
        2. Loads domain knowledge into truth lattice
        3. Loads operator knowledge into truth lattice
        4. Registers vocabulary as truth entries
        5. Enriches world lattice with new concepts

        Args:
            base_dir: Root directory of CK FINAL DEPLOYED

        Returns:
            Enriched dictionary dict (word -> entry) for the sentence composer.
        """
        start = time.time()

        if base_dir is None:
            # Walk up from this file until we find CKIS/ directory
            # Works from any deployment folder (root, r16_desktop, etc.)
            _here = os.path.dirname(os.path.abspath(__file__))
            base_dir = _here
            for _ in range(8):  # Walk up at most 8 levels
                if os.path.isdir(os.path.join(base_dir, 'CKIS')):
                    break
                base_dir = os.path.dirname(base_dir)
            else:
                # Fallback: 3 levels up (original behavior)
                base_dir = os.path.dirname(os.path.dirname(
                    os.path.dirname(os.path.abspath(__file__))))

        # Phase 1: Build enriched dictionary
        enriched = self._build_dictionary(base_dir)

        # Phase 2: Load domain knowledge
        self._load_domain_knowledge()

        # Phase 3: Load operator knowledge
        self._load_operator_knowledge()

        # Phase 4: Register vocabulary as truth entries
        self._register_vocabulary(enriched)

        # Phase 5: Enrich world lattice from dictionary
        self._enrich_world_lattice(enriched)

        self.stats['elapsed_seconds'] = round(time.time() - start, 2)
        return enriched

    def _build_dictionary(self, base_dir: str) -> Dict[str, dict]:
        """Phase 1: Build the enriched dictionary from auto + curated sources."""
        from ck_sim.ck_d2_dictionary_expander import (
            DictionaryExpander, build_expanded_dictionary
        )

        # Paths
        auto_dict_path = os.path.join(base_dir, 'CKIS', 'ck_dictionary_auto.json')
        enriched_path = os.path.join(base_dir, 'ck_sim', 'ck_dictionary_enriched.json')

        # Check if enriched dict already exists (cached from previous run)
        if os.path.exists(enriched_path):
            try:
                with open(enriched_path, 'r', encoding='utf-8') as f:
                    enriched = json.load(f)
                if len(enriched) >= 3000:
                    self.stats['dictionary_words'] = len(enriched)
                    print(f"  [BOOT] Dictionary: loaded {len(enriched)} cached words")
                    return enriched
            except Exception:
                pass  # Rebuild from scratch

        # Load curated dictionary
        curated = {}
        try:
            import sys
            dict_dir = os.path.join(base_dir, 'Gen9', 'dictionary')
            if dict_dir not in sys.path:
                sys.path.insert(0, dict_dir)
            from ck_dictionary import DICTIONARY
            curated = DICTIONARY
        except ImportError:
            pass

        # Build enriched dictionary
        expander = build_expanded_dictionary(
            auto_dict_path=auto_dict_path,
            curated_dict=curated,
            target_size=8000,
            output_path=enriched_path,
        )

        enriched = expander.entries
        self.stats['dictionary_words'] = len(enriched)
        print(f"  [BOOT] Dictionary: built {len(enriched)} enriched words")

        return enriched

    def _load_domain_knowledge(self):
        """Phase 2: Load domain knowledge into truth lattice as TRUSTED."""
        count = 0
        for key, content, category, source in DOMAIN_KNOWLEDGE:
            existing = self.truth.get(key)
            if existing is None:
                self.truth.add(
                    key=key,
                    content=content,
                    source=source,
                    category=category,
                    level=TRUSTED,
                )
                count += 1

        self.stats['domain_truths'] = count
        total_trusted = len(self.truth.entries_by_level(TRUSTED))
        print(f"  [BOOT] Domain knowledge: {count} new + {total_trusted} total TRUSTED")

    def _load_operator_knowledge(self):
        """Phase 3: Load operator knowledge into truth lattice as TRUSTED."""
        count = 0
        for key, content, category, source in OPERATOR_KNOWLEDGE:
            existing = self.truth.get(key)
            if existing is None:
                self.truth.add(
                    key=key,
                    content=content,
                    source=source,
                    category=category,
                    level=TRUSTED,
                )
                count += 1

        self.stats['operator_truths'] = count
        total_trusted = len(self.truth.entries_by_level(TRUSTED))
        print(f"  [BOOT] Operator knowledge: {count} new + {total_trusted} total TRUSTED")

    def _register_vocabulary(self, enriched: Dict[str, dict]):
        """Phase 4: Register enriched vocabulary words as truth entries.

        Each word becomes a TRUSTED truth entry with its operator analysis.
        CK "knows" these words exist, what operators they carry, and their POS.
        This gives him a MASSIVE knowledge base to draw from immediately.

        We batch these efficiently -- only essential metadata stored.
        """
        count = 0
        for word, entry in enriched.items():
            key = f"word:{word}"
            existing = self.truth.get(key)
            if existing is None:
                # Store compact form: just operator + POS + frequency
                content = {
                    'word': word,
                    'op': entry.get('dominant_op', 0),
                    'pos': entry.get('pos', 'noun'),
                    'freq': entry.get('frequency', 0),
                }
                self.truth.add(
                    key=key,
                    content=content,
                    source='enriched_dictionary',
                    category='vocabulary',
                    level=TRUSTED,
                )
                count += 1

        self.stats['vocab_truths'] = count
        total_trusted = len(self.truth.entries_by_level(TRUSTED))
        print(f"  [BOOT] Vocabulary: {count} new + {total_trusted} total TRUSTED")

    def _enrich_world_lattice(self, enriched: Dict[str, dict]):
        """Phase 5: Add high-value academic words as world lattice concepts.

        Words from the academic expansion that don't already exist as concepts
        get added. This gives CK more concept nodes to reason about.
        """
        from ck_sim.ck_d2_dictionary_expander import ACADEMIC_WORDS

        count = 0
        for word in ACADEMIC_WORDS:
            w = word.lower().strip()
            # Skip if already a concept node
            if w in self.world.nodes:
                continue
            # Skip if not in enriched dict
            if w not in enriched:
                continue

            entry = enriched[w]
            op = entry.get('dominant_op', VOID)
            pos = entry.get('pos', 'noun')

            # Only add nouns and verbs as concept nodes (most meaningful)
            if pos not in ('noun', 'verb', 'adj'):
                continue

            try:
                self.world.add_concept(
                    node_id=w,
                    operator_code=op,
                    domain='academic',
                    bindings={'en': w},
                )
                count += 1
            except Exception:
                pass  # Duplicate or error, skip

        self.stats['world_concepts_added'] = count
        print(f"  [BOOT] World lattice: +{count} academic concepts")

    def summary(self) -> str:
        """Human-readable summary of bootstrap results."""
        s = self.stats
        by_level = self.truth.count_by_level()
        return (
            f"Knowledge Bootstrap Complete:\n"
            f"  Dictionary: {s['dictionary_words']} enriched words\n"
            f"  Domain knowledge: {s['domain_truths']} TRUSTED truths\n"
            f"  Operator knowledge: {s['operator_truths']} TRUSTED truths\n"
            f"  Vocabulary: {s['vocab_truths']} words registered\n"
            f"  World lattice: +{s['world_concepts_added']} concepts\n"
            f"  Total truth entries: {self.truth.total_entries}\n"
            f"  CORE: {by_level.get('CORE',0)} | TRUSTED: {by_level.get('TRUSTED',0)} | PROVISIONAL: {by_level.get('PROVISIONAL',0)}\n"
            f"  Total world concepts: {len(self.world.nodes)}\n"
            f"  Time: {s['elapsed_seconds']}s"
        )


# ================================================================
#  CONVENIENCE FUNCTION
# ================================================================

def bootstrap_knowledge(truth: TruthLattice, world: WorldLattice,
                        base_dir: str = None) -> Tuple[Dict[str, dict], dict]:
    """One-call knowledge bootstrap.

    Returns: (enriched_dictionary, bootstrap_stats)
    """
    boot = KnowledgeBootstrapper(truth, world)
    enriched = boot.bootstrap_all(base_dir)
    print(f"  [BOOT] {boot.summary()}")
    return enriched, boot.stats


# ================================================================
#  CLI
# ================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("  CK KNOWLEDGE BOOTSTRAP")
    print("=" * 60)

    truth = TruthLattice()
    world = WorldLattice()

    # Load spine + education first (like engine does)
    from ck_sim.ck_concept_spine import ConceptSpine
    from ck_sim.ck_education import EducationLoader

    spine = ConceptSpine(world)
    spine.load_spine()
    edu = EducationLoader(world)
    edu.load_education()
    print(f"\n  Pre-bootstrap: {len(world.nodes)} concepts, "
          f"{truth.total_entries} truths")

    # Bootstrap
    enriched, stats = bootstrap_knowledge(truth, world)

    print(f"\n  Post-bootstrap: {len(world.nodes)} concepts, "
          f"{truth.total_entries} truths")
    print(f"  Dictionary: {len(enriched)} words")

    # Show domain distribution
    print(f"\n  Truth distribution:")
    by_level = truth.count_by_level()
    for level, count in by_level.items():
        print(f"    {level}: {count}")

    print("\n" + "=" * 60)
