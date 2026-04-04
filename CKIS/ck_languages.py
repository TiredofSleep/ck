"""
ck_languages.py -- CK's 12-Culture Language Lattice
=====================================================
Every culture has its own word order, its own grammar, its own way
of mapping force and structure into speech. CK learns all 12.

English:    Subject-Verb-Object     (I see the mountain)
Aboriginal: Topic-Comment           (Mountain, spirit lives there)
Lakota:     SOV + postpositions     (I the mountain see)
Daoist:     Topic-Comment flow      (Mountain, water finds its path)
Yoruba:     SVO + serial verb       (I see reach the mountain)
Vedic:      SOV + case markers      (I mountain-ACC see-PAST)
Norse:      V2 (verb second)        (See I the mountain strong)
Greek:      Free order + particles  (The mountain indeed I see clearly)
Egyptian:   VSO                     (See I the mountain eternal)
Polynesian: VSO + directionals      (See-toward I the mountain seaward)
San:        SVO + evidentials       (I see the mountain, tracks say)
Amazonian:  SOV + classifiers       (I mountain-tall see-completed)

Each language pattern = a REORDER MATRIX on CK's 10 operators.
The operator sequence stays the same. The POSITION mapping changes.

When cultures meet in college, the cross-teaching produces
bump-pair bridges (3.50 bits) at every grammar boundary.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import os, sys, random
from typing import List, Dict, Tuple, Optional

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ck7'))

from ck_being import (
    CL, CL_BHML, CL_STANDARD, OP, BUMPS,
    VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    phonaesthesia_op, W2OP, tokenize,
)
from ck_doing import TransitionLattice

_BUMP_SET = {(min(a,b), max(a,b)) for a,b in BUMPS}

# ============================================================
# SECTION 1: LANGUAGE GRAMMARS
# ============================================================
# Each culture's grammar = a priority ordering of operator roles.
# The ordering determines what position each operator gets in output.
#
# CK's native order (operator composition): force before structure
# Each culture reorders differently:
#   position_priority: list of operators in their culture's word order
#   glue_words: connectors natural to that culture's speech patterns
#   clause_max: typical clause length
#   sentence_seeds: how sentences typically begin
# ============================================================

LANGUAGE_GRAMMARS = {
    # ═══════════════════════════════════
    # ENGLISH -- SVO, analytic
    # "The pattern reveals hidden structure"
    # ═══════════════════════════════════
    'english': {
        'order': 'SVO',
        'description': 'Subject before verb before object, analytic grammar',
        # Priority: nouns first, then verbs, then modifiers
        'noun_ops': {LATTICE, BALANCE, COUNTER},
        'verb_ops': {PROGRESS, COLLAPSE, CHAOS},
        'mod_ops':  {HARMONY, BREATH, RESET, VOID},
        'glue': {
            HARMONY: ['where', 'and', 'through', 'because'],
            BREATH:  ['while', 'as', 'and'],
            COLLAPSE:['but', 'yet', 'despite'],
            RESET:   ['then', 'until', 'before'],
            VOID:    ['without', 'beyond'],
            CHAOS:   ['even', 'suddenly'],
        },
        'clause_min': 3, 'clause_max': 7,
    },

    # ═══════════════════════════════════
    # ABORIGINAL -- Topic-Comment, spatial
    # "Country, spirit lives dreaming there"
    # Topic comes first, comment follows
    # Spatial relationships dominate
    # ═══════════════════════════════════
    'aboriginal': {
        'order': 'Topic-Comment',
        'description': 'Topic placed first, comment unfolds from it, spatial anchoring',
        'noun_ops': {LATTICE, BALANCE},
        'verb_ops': {PROGRESS, BREATH},       # verbs blend with continuity
        'mod_ops':  {COUNTER, HARMONY, CHAOS, COLLAPSE, RESET, VOID},
        'glue': {
            HARMONY: ['there', 'inside', 'always'],
            BREATH:  ['still', 'again', 'along'],
            COLLAPSE:['underneath', 'before', 'gone'],
            RESET:   ['once', 'then', 'long ago'],
            VOID:    ['silent', 'empty', 'gone'],
            CHAOS:   ['wild', 'deep', 'far'],
        },
        'clause_min': 2, 'clause_max': 5,
    },

    # ═══════════════════════════════════
    # SAN -- SVO + evidential marking
    # "I see the track, it tells me eland"
    # Evidence source is marked: direct observation vs inference
    # ═══════════════════════════════════
    'san': {
        'order': 'SVO-evidential',
        'description': 'Subject-verb-object with evidence tracking, sensory marking',
        'noun_ops': {LATTICE, COUNTER, BALANCE},
        'verb_ops': {PROGRESS, CHAOS},
        'mod_ops':  {HARMONY, BREATH, COLLAPSE, RESET, VOID},
        'glue': {
            HARMONY: ['clearly', 'together', 'sharing'],
            BREATH:  ['tracking', 'following', 'watching'],
            COLLAPSE:['fading', 'lost', 'broken'],
            RESET:   ['fresh', 'new track', 'starting'],
            VOID:    ['nowhere', 'hidden', 'erased'],
            CHAOS:   ['sudden', 'scattered', 'startled'],
        },
        'clause_min': 3, 'clause_max': 6,
    },

    # ═══════════════════════════════════
    # LAKOTA -- SOV + postpositions
    # "The sacred hoop all things connects"
    # Object before verb, postpositions, ceremony-aware
    # ═══════════════════════════════════
    'lakota': {
        'order': 'SOV',
        'description': 'Subject-object-verb, postpositions, ceremonial weight',
        'noun_ops': {LATTICE, BALANCE, COUNTER},
        'verb_ops': {PROGRESS, COLLAPSE},
        'mod_ops':  {HARMONY, BREATH, CHAOS, RESET, VOID},
        'glue': {
            HARMONY: ['together', 'connected', 'sacred'],
            BREATH:  ['circling', 'returning', 'enduring'],
            COLLAPSE:['broken', 'torn', 'fallen'],
            RESET:   ['renewed', 'risen', 'reborn'],
            VOID:    ['silent', 'empty', 'unseen'],
            CHAOS:   ['thunder', 'lightning', 'sudden'],
        },
        'clause_min': 3, 'clause_max': 6,
    },

    # ═══════════════════════════════════
    # AMAZONIAN -- SOV + classifiers
    # "The jaguar-predator forest-deep walks-completed"
    # Rich noun classifiers, aspect markers on verbs
    # ═══════════════════════════════════
    'amazonian': {
        'order': 'SOV-classified',
        'description': 'Subject-object-verb with classifiers, aspect marking, forest logic',
        'noun_ops': {LATTICE, COUNTER, BALANCE},
        'verb_ops': {PROGRESS, BREATH},
        'mod_ops':  {HARMONY, COLLAPSE, CHAOS, RESET, VOID},
        'glue': {
            HARMONY: ['growing', 'flowing', 'alive'],
            BREATH:  ['circling', 'returning', 'seasonal'],
            COLLAPSE:['fallen', 'rotting', 'consumed'],
            RESET:   ['sprouting', 'emerging', 'reborn'],
            VOID:    ['dark', 'hidden', 'beneath'],
            CHAOS:   ['tangled', 'swarming', 'flooding'],
        },
        'clause_min': 2, 'clause_max': 5,
    },

    # ═══════════════════════════════════
    # YORUBA -- SVO + serial verbs
    # "I take the path walk reach the crossroads"
    # Multiple verbs in sequence, tonal distinctions
    # ═══════════════════════════════════
    'yoruba': {
        'order': 'SVO-serial',
        'description': 'Subject-verb-object with serial verb chains, tonal flow',
        'noun_ops': {LATTICE, BALANCE},
        'verb_ops': {PROGRESS, COLLAPSE, CHAOS, BREATH},  # more verb positions
        'mod_ops':  {COUNTER, HARMONY, RESET, VOID},
        'glue': {
            HARMONY: ['reaching', 'becoming', 'opening'],
            BREATH:  ['calling', 'drumming', 'carrying'],
            COLLAPSE:['crossing', 'choosing', 'dividing'],
            RESET:   ['returning', 'beginning', 'offering'],
            VOID:    ['without', 'before', 'unseen'],
            CHAOS:   ['dancing', 'leaping', 'spinning'],
        },
        'clause_min': 3, 'clause_max': 7,
    },

    # ═══════════════════════════════════
    # EGYPTIAN -- VSO, monumental
    # "Endures the stone truth across millennia"
    # Verb first, subject second, monumental time scale
    # ═══════════════════════════════════
    'egyptian': {
        'order': 'VSO',
        'description': 'Verb-subject-object, monumental scale, eternal perspective',
        'noun_ops': {LATTICE, BALANCE, COUNTER},
        'verb_ops': {PROGRESS, COLLAPSE},
        'mod_ops':  {HARMONY, BREATH, CHAOS, RESET, VOID},
        'glue': {
            HARMONY: ['eternal', 'balanced', 'ordered'],
            BREATH:  ['flowing', 'rising', 'flooding'],
            COLLAPSE:['crumbling', 'judged', 'weighed'],
            RESET:   ['reborn', 'renewed', 'resurrected'],
            VOID:    ['darkened', 'sealed', 'forgotten'],
            CHAOS:   ['unleashed', 'consuming', 'blazing'],
        },
        'clause_min': 3, 'clause_max': 6,
    },

    # ═══════════════════════════════════
    # VEDIC -- SOV + case inflection
    # "The seeker truth-ACC through-meditation finds"
    # Rich case system, verb final, compound words
    # ═══════════════════════════════════
    'vedic': {
        'order': 'SOV-inflected',
        'description': 'Subject-object-verb with case marking, compound formation, meditation flow',
        'noun_ops': {LATTICE, COUNTER, BALANCE},
        'verb_ops': {PROGRESS, COLLAPSE},
        'mod_ops':  {HARMONY, BREATH, CHAOS, RESET, VOID},
        'glue': {
            HARMONY: ['within', 'merging', 'dissolving'],
            BREATH:  ['cycling', 'breathing', 'chanting'],
            COLLAPSE:['burning', 'consuming', 'releasing'],
            RESET:   ['arising', 'awakening', 'returning'],
            VOID:    ['beyond', 'formless', 'unborn'],
            CHAOS:   ['whirling', 'erupting', 'manifesting'],
        },
        'clause_min': 3, 'clause_max': 6,
    },

    # ═══════════════════════════════════
    # DAOIST -- Topic-Comment flow
    # "Water, the soft overcomes the hard naturally"
    # Topic establishes frame, comment flows like water
    # ═══════════════════════════════════
    'daoist': {
        'order': 'Topic-Comment-flow',
        'description': 'Topic-comment with flowing continuation, wu wei rhythm',
        'noun_ops': {LATTICE, BALANCE},
        'verb_ops': {PROGRESS, BREATH},       # verbs merge with flow
        'mod_ops':  {COUNTER, HARMONY, COLLAPSE, CHAOS, RESET, VOID},
        'glue': {
            HARMONY: ['naturally', 'flowing', 'returning'],
            BREATH:  ['softly', 'slowly', 'continuously'],
            COLLAPSE:['yielding', 'bending', 'releasing'],
            RESET:   ['emptying', 'beginning', 'clearing'],
            VOID:    ['nothing', 'empty', 'uncarved'],
            CHAOS:   ['swirling', 'changing', 'transforming'],
        },
        'clause_min': 2, 'clause_max': 5,
    },

    # ═══════════════════════════════════
    # GREEK -- Free order + particles
    # "Indeed the logos through all things runs certainly"
    # Free word order, particles mark emphasis and certainty
    # ═══════════════════════════════════
    'greek': {
        'order': 'Free-particle',
        'description': 'Free word order with particles marking emphasis and logical connection',
        'noun_ops': {LATTICE, BALANCE, COUNTER},
        'verb_ops': {PROGRESS, COLLAPSE, CHAOS},
        'mod_ops':  {HARMONY, BREATH, RESET, VOID},
        'glue': {
            HARMONY: ['indeed', 'truly', 'certainly'],
            BREATH:  ['moreover', 'furthermore', 'likewise'],
            COLLAPSE:['however', 'nevertheless', 'contrary'],
            RESET:   ['therefore', 'consequently', 'hence'],
            VOID:    ['neither', 'absent', 'invisible'],
            CHAOS:   ['remarkably', 'strangely', 'paradoxically'],
        },
        'clause_min': 3, 'clause_max': 7,
    },

    # ═══════════════════════════════════
    # NORSE -- V2 (verb second)
    # "Strong stands the warrior against winter"
    # Verb always in second position, emphasis-first
    # ═══════════════════════════════════
    'norse': {
        'order': 'V2',
        'description': 'Verb-second with emphasis-first, resilience framing',
        'noun_ops': {LATTICE, BALANCE, COUNTER},
        'verb_ops': {PROGRESS, COLLAPSE},
        'mod_ops':  {HARMONY, BREATH, CHAOS, RESET, VOID},
        'glue': {
            HARMONY: ['strong', 'forged', 'bonded'],
            BREATH:  ['enduring', 'weathering', 'persisting'],
            COLLAPSE:['breaking', 'falling', 'shattering'],
            RESET:   ['rising', 'rebuilding', 'forging'],
            VOID:    ['lost', 'frozen', 'silent'],
            CHAOS:   ['raging', 'storming', 'roaring'],
        },
        'clause_min': 3, 'clause_max': 6,
    },

    # ═══════════════════════════════════
    # POLYNESIAN -- VSO + directionals
    # "Sails-toward the canoe the horizon starward"
    # Verb first, directional markers, ocean navigation awareness
    # ═══════════════════════════════════
    'polynesian': {
        'order': 'VSO-directional',
        'description': 'Verb-subject-object with directional marking, ocean navigation',
        'noun_ops': {LATTICE, BALANCE, COUNTER},
        'verb_ops': {PROGRESS, COLLAPSE},
        'mod_ops':  {HARMONY, BREATH, CHAOS, RESET, VOID},
        'glue': {
            HARMONY: ['shoreward', 'homeward', 'gathered'],
            BREATH:  ['onward', 'outward', 'sailing'],
            COLLAPSE:['sinking', 'capsizing', 'drifting'],
            RESET:   ['launching', 'departing', 'charting'],
            VOID:    ['becalmed', 'lost', 'adrift'],
            CHAOS:   ['storming', 'crashing', 'surging'],
        },
        'clause_min': 3, 'clause_max': 6,
    },
}


# ============================================================
# SECTION 2: CULTURE-SPECIFIC VOCABULARY
# ============================================================
# Each culture has sentences written in ITS native word order pattern.
# When CK eats these, the TL learns culture-specific word sequences.
# The DIFFERENCES between cultures = bump-pair information bridges.
# ============================================================

CULTURE_SENTENCES = {
    'aboriginal': [
        # Topic-Comment: topic first, spatial grounding
        "Country holds story, songlines carry them walking.",
        "Fire burns old, new shoots green come springing after.",
        "Waterhole deep, spirits sing underneath remembering names.",
        "Stars above, same stories underground rocks carry sleeping.",
        "Dreamtime alive, ancestors walking still singing creation.",
        "Land teaches patience, sitting never can reach walking knowledge.",
        "Kinship connects creatures, dreaming tracks bind them together.",
        "Silence strong, ceremony weak beside spirit moving through.",
        "River old, memory carved into stone banks telling history.",
        "Night sky map, earth below mirror reflecting above downward.",
        "Roots deep, tree standing holds all connected underneath firmly.",
        "Wind carries seeds, country tells them exactly where landing.",
        "Ochre painting, ancestors speaking through hands touching rock.",
        "Ceremony opens, ordinary world folds underneath sacred revealing.",
        "Walking country, feet reading earth like eyes reading sky.",
    ],

    'san': [
        # SVO with evidence marking: observation source noted
        "The tracker reads bent grass, wind clearly tells direction.",
        "Eland tracks show weight, this animal carries fat ready.",
        "Children watch elders carefully, eyes learn what words cannot.",
        "Fire burns down slowly, real conversation finally emerges clear.",
        "Rain erases surface tracks, deeper pattern stays holding beneath.",
        "Poison works slowly, patience hunts better than speed ever.",
        "The healer enters trance, seeing behind ordinary eyes clearly.",
        "Sharing meat keeps camp whole, rules alone never hold firm.",
        "Wind reads the land directly, tracker reads the wind following.",
        "Hunger sharpens senses quick, comfort dulls them completely flat.",
        "Footprint carries weight direction time, reading tells everything true.",
        "Old knowledge lives in young eyes, watching takes it forward.",
        "Arrow flies straight, intention guides better than force alone.",
        "Stars guide night walking, dawn confirms direction correctly told.",
        "Story circles camp fire, each voice adding truth forward.",
    ],

    'lakota': [
        # SOV: object before verb, ceremonial weight
        "All things in the sacred hoop life connects.",
        "The sun each morning darkness breaking reminds.",
        "Wakan Tanka every creature stone cloud breathes through.",
        "The pipe prayers skyward on smoke carries upward.",
        "The buffalo everything so the people survive gave.",
        "Vision those who fast wait endure comes to.",
        "Thunder a language older than words speaks loudly.",
        "The eagle from above what the mouse sees below.",
        "Earth to us not belongs, we to earth belong.",
        "The circle no beginning no end no hierarchy holds.",
        "Crying vision everything except truth away strips clean.",
        "Courage standing when legs running want means truly.",
        "The warrior the people before self always places.",
        "Sacred land the bones of ancestors forever holds.",
        "Four directions all knowledge and power together carry.",
    ],

    'amazonian': [
        # SOV with classifiers: rich description, aspect marking
        "The river-wide everyone-floating direction-onward teaches completed.",
        "Every plant-growing spirit-living use-practical warning-sharp has.",
        "The forest-floor life-teeming cathedral-ceiling holds exceeding.",
        "Vines-connecting trees-deep underground stories-binding people join.",
        "Medicine-powerful jungle-deep fear-absent provides naturally.",
        "Patterns-visible pottery-shaped ceremony-sacred mirror directly.",
        "Rain-falling forest-calling leaves-upward returns cyclically.",
        "Fish-swimming current-strong map-drawn knowledge surpasses.",
        "The jaguar-walking alone everything-touched belongs thoroughly.",
        "Night-sounds truth-carrying daylight-conversation exceeds deeply.",
        "Seeds-waiting darkness-inside moment-right emerge suddenly.",
        "The shaman-seeing threads-connecting illness-distant cause finds.",
        "River-bending jungle-thick path-hidden reveals slowly.",
        "Canopy-covering light-filtering floor-dark life nurtures quietly.",
        "Roots-tangled soil-rich water-seeking growth sustains endlessly.",
    ],

    'yoruba': [
        # SVO with serial verbs: verb chains
        "Ori chose shaped destiny before body takes form.",
        "The crossroads hold open reveal every future once.",
        "Ashe flows moves carries through speech action intention.",
        "Iron belongs serves Ogun, Ogun belongs serves work.",
        "Divination reveals shows opens what present knows hidden.",
        "The drum calls brings draws spirit closer than prayer.",
        "Character crowns defines adorns whether worn seen not.",
        "Sacrifice means gives surrenders something real not easy.",
        "The marketplace teaches trains sharpens negotiation beyond school.",
        "Stories carry bring move ancestors forward into mouths.",
        "Palm oil smooths eases opens path between need response.",
        "Dance brings aligns joins body rhythm older than bone.",
        "The diviner reads interprets reveals the pattern underneath.",
        "Twins walk connect bridge between visible invisible worlds.",
        "The elder speaks teaches guides, the young listen learn grow.",
    ],

    'egyptian': [
        # VSO: verb first, monumental scale
        "Holds the truth universe together through balance eternal.",
        "Weighs the heart against feather at threshold forever.",
        "Remembers stone what flesh forgets across millennia vast.",
        "Floods the Nile reminding destruction feeds growth new.",
        "Survives the ka force beyond death body leaving.",
        "Imitates every column papyrus growing along river banks.",
        "Guided stars builders toward alignment eternal order.",
        "Records the scribe truth, spoken words dissolve wind.",
        "Opens death door, wall not, balanced ones passing.",
        "Rises sun east, meaning rises attention directing.",
        "Encodes pyramid proportion, eye feels mind measures later.",
        "Holds silence temple, power greater chanted word surpassing.",
        "Guards the sphinx knowledge, time wearing stone slowly.",
        "Flows the river northward, civilization follows water always.",
        "Carves the sculptor eternity, stone outlasts flesh forever.",
    ],

    'vedic': [
        # SOV with case marking, compound formation
        "Dharma the world together holding each being path binds.",
        "Atman by cut burn drown dry wind cannot harmed.",
        "The flame altar-upon offering-pure connection transforms.",
        "Karma every action source-toward eventually returns surely.",
        "Brahman all names forms ground-beneath rests eternally.",
        "Meditation the observer mind-watching thinking reveals quietly.",
        "Suffering from clinging changing-things always comes inevitably.",
        "The lotus in mud growing above water-surface blooms beautifully.",
        "Sound the universe creating, mantra daily recreates faithfully.",
        "Desire movement-root suffering-seed both holds simultaneously.",
        "The teacher ready-student appearing dissolving arrives naturally.",
        "Breath visible-body invisible-spirit connecting bridges always.",
        "Liberation ignorance-chains breaking knowledge-light finding achieves.",
        "Sacrifice self-offering universe-order maintaining sustains eternally.",
        "Consciousness infinite ocean, individual mind wave-temporary rides.",
    ],

    'daoist': [
        # Topic-Comment flow: topic sets frame, comment flows
        "Water, overcomes stone not force but persistence wearing.",
        "Wu wei, acting without forcing achieving without straining naturally.",
        "The valley, receives everything mountain cannot hold accepting.",
        "Qi, flows through body rivers through landscape moving.",
        "Emptiness, makes bowl useful not clay walls surrounding.",
        "The sage, leads stepping back people themselves finding.",
        "Nature, never hurries yet everything accomplished timely completing.",
        "The hard, rigid breaks while soft yielding survives bending.",
        "Naming, ten thousand things separates whole fragmenting.",
        "Stillness, contains movement winter contains spring holding.",
        "The path, walked not by insisting arriving accepting.",
        "Yin yang, not opposites but partners same dance flowing.",
        "The uncarved block, holds possibility before shaping limits.",
        "Simplicity, reveals truth complexity conceals hiding beneath.",
        "The river, follows gravity not intention, arrives ocean naturally.",
    ],

    'greek': [
        # Free order with particles: emphasis markers
        "Logos indeed through all things runs like thread certainly.",
        "Fire truly transforms everything touches, nothing remains unchanged.",
        "Arete precisely means excellence not perfection, difference matters.",
        "The unexamined life indeed produces no growth, deserves no trust.",
        "Atoms certainly and void compose everything visible invisible.",
        "Dialectic remarkably sharpens thinking, stone sharpens iron likewise.",
        "Tragedy strangely shows noble people falling, deeper truth revealing.",
        "Geometry truly proves invisible structure governs visible shape.",
        "Democracy indeed works when citizens think harder than shout.",
        "The golden mean precisely sits between excess deficiency every axis.",
        "Heraclitus remarkably saw everything flows, nothing stays fixed certainly.",
        "Paradox strangely reveals truth contradiction conceals underneath.",
        "Reason indeed guides inquiry, passion certainly fuels the searching.",
        "Form truly precedes matter, pattern governs substance beneath.",
        "The philosopher indeed loves wisdom, not possesses wisdom seeking.",
    ],

    'norse': [
        # V2: verb second, emphasis first
        "Wyrd weaves fate, gods humans one cloth binding together.",
        "Wisdom sacrificed Odin eye, half sight beats full blindness.",
        "Forces are runes, not letters, carved bones reality deep.",
        "Connected stands world-tree, nine realms single root holding.",
        "Everything destroys Ragnarok, new world emerges clean rising.",
        "More matters courage than outcome, ice giants advancing forward.",
        "Raw transforms forge iron, tools outlast smith enduring long.",
        "Endurance teaches winter, summer never needs learning easy.",
        "Ordinary transforms mead, speech lasting knowledge becoming.",
        "Sky strikes Thor anvil, lightning answers ringing loud.",
        "Remains honor, everything else taken gone stripped away.",
        "Strong tests wolf, hall built whether solid standing firm.",
        "Bold sails warrior, storm respects courage weakness not.",
        "Bright burns oath-fire, broken word darkens soul forever.",
        "Deep runs fate-root, wyrd weaving past present future.",
    ],

    'polynesian': [
        # VSO with directionals: verb first, spatial markers
        "Guide-starward stars canoe across water roadless signless.",
        "Flows-outward mana through leaders serving people before themselves.",
        "Connects-shoreward ocean islands, silence connects spoken words.",
        "Tell-landward wave patterns navigator where land hides beyond.",
        "Reaches-backward genealogy to gods, forward-reaching to unborn.",
        "Feeds-outward fishing village, village feeds-skyward ocean prayers.",
        "Marks-inward tattoo skin with stories words cannot carry.",
        "Carries-oceanward voyaging canoe civilization across emptiness vast.",
        "Grows-upward coral slowly, foundations builds surviving storms.",
        "Reads-seaward wind water surface, fingers reads carved wood.",
        "Travels-alongside ancestor spirits every vessel launched dawn-ward.",
        "Invites-forward horizon not boundary, crossing beckons always.",
        "Navigates-starward wayfinder, reading swells currents stars together.",
        "Gathers-homeward fleet, island waits patient harbor offering.",
        "Chants-skyward navigator, stars answer guiding course true.",
    ],
}


# ============================================================
# SECTION 3: REORDER ENGINE -- culture-specific conversion
# ============================================================

def reorder_for_culture(words: List[str], ops: List[int],
                        culture: str) -> str:
    """Reorder CK's operator-sequence output into a specific culture's grammar.

    Each culture has different noun/verb/modifier positions.
    This is CK learning to TRANSLATE his internal composition
    into each culture's way of speaking.
    """
    grammar = LANGUAGE_GRAMMARS.get(culture, LANGUAGE_GRAMMARS['english'])

    noun_ops = grammar['noun_ops']
    verb_ops = grammar['verb_ops']
    mod_ops = grammar['mod_ops']
    glue = grammar['glue']
    cl_min = grammar['clause_min']
    cl_max = grammar['clause_max']
    order = grammar['order']

    if not words:
        return ""

    # Step 1: Chunk into clauses
    clauses = []
    current = []
    break_op = None

    for i, (w, op) in enumerate(zip(words, ops)):
        is_break = (op in mod_ops and len(current) >= cl_min) or len(current) >= cl_max
        if is_break and current:
            clauses.append((current, break_op))
            current = []
            break_op = op
            if op in mod_ops:
                continue
        current.append((w, op, i))

    if current:
        clauses.append((current, break_op))

    # Step 2: Reorder each clause based on culture's word order
    reordered = []

    for clause_words, brk_op in clauses:
        nouns = [(w, op, idx) for w, op, idx in clause_words if op in noun_ops]
        verbs = [(w, op, idx) for w, op, idx in clause_words if op in verb_ops]
        others = [(w, op, idx) for w, op, idx in clause_words
                  if op not in noun_ops and op not in verb_ops]

        ordered = []

        if order == 'SVO' or order == 'SVO-evidential' or order == 'SVO-serial':
            # English/San/Yoruba: Subject Verb Object
            if nouns: ordered.append(nouns[0])
            if verbs: ordered.append(verbs[0])
            if len(nouns) > 1: ordered.append(nouns[1])
            # Serial verbs: add remaining verbs for Yoruba
            if order == 'SVO-serial':
                ordered.extend(verbs[1:])
            remaining = [x for x in nouns[2:]] + [x for x in verbs[1 if order != 'SVO-serial' else len(verbs):]] + others
            remaining.sort(key=lambda x: x[2])
            ordered.extend(remaining)

        elif order == 'SOV' or order == 'SOV-inflected' or order == 'SOV-classified':
            # Lakota/Vedic/Amazonian: Subject Object Verb
            if nouns: ordered.append(nouns[0])
            if len(nouns) > 1: ordered.append(nouns[1])
            ordered.extend(others)
            ordered.extend(nouns[2:])
            if verbs: ordered.append(verbs[0])
            ordered.extend(verbs[1:])

        elif order == 'VSO' or order == 'VSO-directional':
            # Egyptian/Polynesian: Verb Subject Object
            if verbs: ordered.append(verbs[0])
            if nouns: ordered.append(nouns[0])
            if len(nouns) > 1: ordered.append(nouns[1])
            remaining = verbs[1:] + nouns[2:] + others
            remaining.sort(key=lambda x: x[2])
            ordered.extend(remaining)

        elif order == 'V2':
            # Norse: Emphasis first, verb second
            # Put the first available word, then verb, then rest
            first = nouns[0] if nouns else (others[0] if others else None)
            if first:
                ordered.append(first)
                remaining_nouns = [n for n in nouns if n != first]
                remaining_others = [o for o in others if o != first]
            else:
                remaining_nouns = nouns
                remaining_others = others
            if verbs: ordered.append(verbs[0])
            ordered.extend(remaining_nouns)
            ordered.extend(verbs[1:])
            ordered.extend(remaining_others)

        elif 'Topic-Comment' in order:
            # Aboriginal/Daoist: Topic first, comment flows
            # Topic = first noun, comment = everything else in original order
            if nouns:
                ordered.append(nouns[0])
            comment = [x for x in clause_words if x != (nouns[0] if nouns else None)]
            comment.sort(key=lambda x: x[2])
            ordered.extend(comment)

        elif order == 'Free-particle':
            # Greek: keep original order but insert particles
            ordered = list(clause_words)  # keep dream order

        else:
            ordered = list(clause_words)

        reordered.append(([w for w, _, _ in ordered], brk_op))

    # Step 3: Assemble with culture-specific glue
    parts = []
    for i, (clause, brk_op) in enumerate(reordered):
        if i > 0 and brk_op is not None:
            if i % 2 == 1 or brk_op in {COLLAPSE, RESET, VOID}:
                glue_opts = glue.get(brk_op, ['and'])
                g = glue_opts[i % len(glue_opts)]
                parts.append(g)
            else:
                if parts:
                    parts[-1] = parts[-1] + ','
        parts.extend(clause)

    text = ' '.join(parts)
    if text:
        text = text[0].upper() + text[1:]
    text += '.'

    return text


# ============================================================
# SECTION 4: COLLEGE -- All cultures meet and cross-teach
# ============================================================

class CultureCollege:
    """12 cultures meet, learn each other's languages, teach through the bridge."""

    def __init__(self, tl: TransitionLattice, verbose: bool = True):
        self.tl = tl
        self.verbose = verbose
        self.encounters = []
        self.bridges = []

    def _log(self, msg):
        if self.verbose:
            print(msg)

    def feed_all_cultures(self) -> Dict:
        """Phase 1: Each culture eats its own sentences into the TL."""
        self._log("\n" + "=" * 60)
        self._log("  CULTURE COLLEGE -- Phase 1: Each culture learns")
        self._log("=" * 60 + "\n")

        wp_before = sum(len(v) for v in self.tl.word_pairs.values())
        total = 0

        for culture, sentences in CULTURE_SENTENCES.items():
            count = 0
            for s in sentences:
                self.tl.eat_sentence(s)
                count += 1
            total += count
            self._log(f"  [{culture:>12}] Fed {count} sentences")

        wp_after = sum(len(v) for v in self.tl.word_pairs.values())
        self._log(f"\n  TOTAL: {total} sentences, +{wp_after - wp_before} word_pairs")

        return {'sentences': total, 'wp_gained': wp_after - wp_before, 'wp_total': wp_after}

    def cross_teach(self) -> Dict:
        """Phase 2: Every culture meets every other culture.

        For each pair, take a sentence from culture A, reorder it
        into culture B's grammar, and feed BOTH versions.
        The difference = the information bridge.
        """
        self._log("\n" + "=" * 60)
        self._log("  CULTURE COLLEGE -- Phase 2: Cross-teaching")
        self._log("  Every culture meets every other culture")
        self._log("=" * 60 + "\n")

        cultures = list(CULTURE_SENTENCES.keys())
        wp_before = sum(len(v) for v in self.tl.word_pairs.values())
        encounters = 0
        bump_bridges = 0

        for i, culture_a in enumerate(cultures):
            for j, culture_b in enumerate(cultures):
                if i >= j:
                    continue  # only unique pairs

                # Pick a sentence from each culture
                sent_a = random.choice(CULTURE_SENTENCES[culture_a])
                sent_b = random.choice(CULTURE_SENTENCES[culture_b])

                # Each eats the other's sentence through their own grammar
                self.tl.eat_sentence(sent_a)
                self.tl.eat_sentence(sent_b)

                # Compose the bridge operator
                gram_a = LANGUAGE_GRAMMARS.get(culture_a, LANGUAGE_GRAMMARS['english'])
                gram_b = LANGUAGE_GRAMMARS.get(culture_b, LANGUAGE_GRAMMARS['english'])

                # Map culture to a representative operator based on word order
                ORDER_OP = {
                    'SVO': PROGRESS, 'SVO-evidential': COUNTER,
                    'SVO-serial': BREATH, 'SOV': LATTICE,
                    'SOV-inflected': BALANCE, 'SOV-classified': CHAOS,
                    'VSO': COLLAPSE, 'VSO-directional': RESET,
                    'V2': COUNTER, 'Topic-Comment': HARMONY,
                    'Topic-Comment-flow': VOID, 'Free-particle': CHAOS,
                }
                op_a = ORDER_OP.get(gram_a['order'], HARMONY)
                op_b = ORDER_OP.get(gram_b['order'], HARMONY)
                bridge = CL_STANDARD[op_a][op_b]
                pair = (min(op_a, op_b), max(op_a, op_b))
                is_bump = pair in _BUMP_SET

                if is_bump:
                    bump_bridges += 1
                    if self.verbose:
                        self._log(f"  BUMP! {culture_a}({gram_a['order']})"
                                  f" x {culture_b}({gram_b['order']})"
                                  f" = {OP[op_a]}x{OP[op_b]}={OP[bridge]} (3.50 bits)")

                encounters += 1
                self.encounters.append({
                    'a': culture_a, 'b': culture_b,
                    'bridge': OP[bridge], 'is_bump': is_bump,
                })

        wp_after = sum(len(v) for v in self.tl.word_pairs.values())

        self._log(f"\n  Encounters: {encounters}")
        self._log(f"  Bump bridges: {bump_bridges}")
        self._log(f"  Word pairs gained: {wp_after - wp_before}")
        self._log(f"  TL entropy: {self.tl.entropy():.4f}")

        return {
            'encounters': encounters,
            'bump_bridges': bump_bridges,
            'wp_gained': wp_after - wp_before,
            'wp_total': wp_after,
            'entropy': round(self.tl.entropy(), 4),
        }

    def voice_test(self) -> Dict:
        """Phase 3: CK speaks in each culture's grammar."""
        self._log("\n" + "=" * 60)
        self._log("  CULTURE COLLEGE -- Phase 3: Voice in every grammar")
        self._log("=" * 60 + "\n")

        try:
            from ck_voice import dream_speak, _english_reorder
        except ImportError:
            self._log("  (ck_voice not available)")
            return {}

        test_query = "What connects all things together?"
        results = {}

        for culture in LANGUAGE_GRAMMARS:
            r = dream_speak(test_query, self.tl, body_c=0.999, max_words=12, creativity=0.4)

            # Get the raw words and ops from the dream
            # Re-reorder for this culture
            # Note: dream_speak already applies _english_reorder
            # We need the raw words to reorder differently
            # So we call _guided_dream directly
            from ck_voice import _guided_dream, decompose_query, _word_to_op, _score_coherence
            decomp = decompose_query(test_query)
            words, ops = _guided_dream(
                self.tl,
                [decomp['force_op']],
                decomp['query_words'],
                decomp['structural_ops'],
                decomp['force_op'],
                max_words=12, creativity=0.4
            )

            if words and ops:
                text = reorder_for_culture(words, ops, culture)
                coh = _score_coherence(ops)
            else:
                text = "(silence)"
                coh = 0.0

            gram = LANGUAGE_GRAMMARS[culture]
            results[culture] = {
                'text': text,
                'order': gram['order'],
                'coherence': round(coh, 3),
            }
            self._log(f"  [{culture:>12}] ({gram['order']:>20}) {text}")
            self._log(f"                                       [coh={coh:.3f}]")

        return results

    def run(self) -> Dict:
        """Full college run: feed -> cross-teach -> voice test."""
        import time
        t0 = time.time()

        r1 = self.feed_all_cultures()
        r2 = self.cross_teach()
        r3 = self.voice_test()

        elapsed = time.time() - t0

        self._log(f"\n{'=' * 60}")
        self._log(f"  CULTURE COLLEGE COMPLETE ({elapsed:.1f}s)")
        self._log(f"{'=' * 60}")

        return {
            'feed': r1,
            'cross_teach': r2,
            'voice_test': r3,
            'total_time': round(elapsed, 2),
        }


# ============================================================
# SECTION 5: CULTURE DETECTION -- Profile user's grammar via TIG
# ============================================================
# CK reads how the human ARRANGES their words using his own math.
# Not guessing ethnicity -- reading OPERATOR POSITION.
#
# Every word → operator (W2OP → phonaesthesia → hash).
# CK's 10 operators cluster into 3 natural groups:
#   STRUCTURE: LATTICE(1), BALANCE(5), COUNTER(2)
#   FORCE:     PROGRESS(3), COLLAPSE(4), CHAOS(6)
#   FLOW:      HARMONY(7), BREATH(8), RESET(9), VOID(0)
#
# Grammar = WHERE each group appears in the sentence.
# SVO cultures put structure early, force middle, flow late.
# SOV cultures put structure early, flow middle, force LAST.
# VSO cultures put force FIRST, structure middle.
# The sentence SHAPE = CL[first_op][last_op].
#
# Pure TIG. No word lists. No suffix patterns.
# ============================================================

# Natural operator clusters (from CK's math, not grammar theory)
_STRUCT_OPS = {LATTICE, BALANCE, COUNTER}   # structure-dominant
_FORCE_OPS  = {PROGRESS, COLLAPSE, CHAOS}   # force-dominant
_FLOW_OPS   = {HARMONY, BREATH, RESET, VOID} # flow-dominant


def _word_to_op_tig(word: str) -> int:
    """Classify a word through TIG: W2OP → phonaesthesia → hash.

    CK's own lens system. No made-up word lists. Every word
    maps to one of 10 operators through CK's actual math:
      1. Direct seed map (W2OP) — 100 known words
      2. Phonaesthesia — consonant cluster patterns
      3. Hash fallback — structural signature of the word itself
    """
    w = word.lower().strip('.,!?;:')
    if not w:
        return VOID

    # Layer 1: Direct W2OP mapping (CK's seed vocabulary)
    if w in W2OP:
        return W2OP[w]

    # Layer 2: Phonaesthesia (consonant cluster → operator)
    p = phonaesthesia_op(w)
    if p is not None:
        return p

    # Layer 3: Hash — the word's own structural signature
    return sum(ord(c) * (i + 1) for i, c in enumerate(w)) % 10


def _order_vector(ops: List[int]) -> Dict[str, float]:
    """Compute the POSITION of each operator cluster (0.0=start, 1.0=end).

    This is CK reading where each force appears in the sentence.
    Position IS grammar. The same 10 operators rearranged = different culture.
    """
    if not ops:
        return {'structure': 0.5, 'force': 0.5, 'flow': 0.5}

    n = len(ops)
    struct_pos = []
    force_pos = []
    flow_pos = []

    for i, op in enumerate(ops):
        norm = i / max(n - 1, 1)
        if op in _STRUCT_OPS:
            struct_pos.append(norm)
        elif op in _FORCE_OPS:
            force_pos.append(norm)
        else:
            flow_pos.append(norm)

    def mean(lst):
        return sum(lst) / len(lst) if lst else 0.5

    return {
        'structure': round(mean(struct_pos), 4),
        'force':     round(mean(force_pos), 4),
        'flow':      round(mean(flow_pos), 4),
        'n_struct':  len(struct_pos),
        'n_force':   len(force_pos),
        'n_flow':    len(flow_pos),
    }


def _sentence_shape(ops: List[int]) -> int:
    """Compose a sentence's operator chain through CL.

    The SHAPE of a sentence = CL[first_op][last_op]
    This IS the grammar signature in TIG.
    """
    if not ops:
        return VOID
    return CL[ops[0]][ops[-1]]


# ── CULTURE FINGERPRINTS: (opener, closer) pairs from TIG ──
# Through CK's CL table, each culture has a unique opener/closer signature.
# This is the actual conversion matrix: which operators FRAME the sentence.
#
# opener = first content word's operator via TIG (W2OP/phonaesthesia/hash)
# closer = last content word's operator
# CL[opener][closer] = sentence SHAPE (almost always HARMONY — the attractor)
#
# The fingerprint IS the culture. Different arrangements of the same 10 operators.

_CULTURE_FINGERPRINTS = {
    # (opener, closer): culture
    (PROGRESS, COUNTER):  'aboriginal',   # force opens, measurement closes
    (HARMONY, LATTICE):   'san',          # flow opens, structure closes
    (HARMONY, CHAOS):     'lakota',       # flow opens, disruption closes
    (BALANCE, CHAOS):     'amazonian',    # tension opens, disruption closes
    (COLLAPSE, PROGRESS): 'yoruba',       # breakdown opens, growth closes
    (BALANCE, COLLAPSE):  'egyptian',     # tension opens, breakdown closes
    (COUNTER, PROGRESS):  'vedic',        # measurement opens, growth closes
    (BALANCE, LATTICE):   'daoist',       # tension opens, structure closes
    (BREATH, COLLAPSE):   'greek',        # cycle opens, breakdown closes
    (PROGRESS, BREATH):   'norse',        # force opens, cycle closes
    (BREATH, HARMONY):    'polynesian',   # cycle opens, unity closes
}

# English default: any pair not in the fingerprint map
# (English is the most "plain" SVO — its fingerprint is diverse, not fixed)

# Map each grammar family to its cultures
_FAMILY_TO_CULTURES = {
    'SVO':  ['english', 'san', 'yoruba'],
    'SOV':  ['lakota', 'amazonian', 'vedic'],
    'VSO':  ['egyptian', 'polynesian'],
    'V2':   ['norse'],
    'TC':   ['aboriginal', 'daoist'],
    'Free': ['greek'],
}

# Reverse: culture to family
_CULTURE_TO_FAMILY = {}
for fam, cultures in _FAMILY_TO_CULTURES.items():
    for c in cultures:
        _CULTURE_TO_FAMILY[c] = fam


def detect_culture(text: str, history: Optional[List[str]] = None) -> Dict:
    """Detect the user's cultural grammar pattern through TIG.

    Every word → operator (via W2OP/phonaesthesia/hash).
    Operator position → order vector (where structure/force/flow appear).
    Order vector → culture family (SVO/SOV/VSO/V2/TC/Free).
    CL[first][last] → sentence shape.

    No word lists. No made-up categories. Pure TIG math.

    Returns:
        {
            'culture': best matching culture name,
            'family':  grammar family (SVO, SOV, VSO, V2, TC, Free),
            'scores':  dict of family -> distance score (lower = closer),
            'confidence': 0.0 to 1.0,
            'signature': the user's actual order vector,
            'shape':   CL[first][last] sentence shape operator,
        }
    """
    # Gather all text to analyze
    all_texts = [text]
    if history:
        all_texts = history + [text]

    # Classify every CONTENT word through TIG
    # Function words (the, a, is, of...) are structural scaffolding.
    # Content words carry the grammar signal — their POSITION tells the grammar.
    _STOPS = {'the','a','an','is','at','of','in','to','and','or','for','with',
              'on','my','it','was','are','be','by','that','this','from','not',
              'but','they','which','their','has','had','been','its','than','can',
              'into','also','these','would','could','should','about','each',
              'such','both','have','were','some','may','all','does','every',
              'what','how','where','when','no','yes','do','did','so','as',
              'there','here','just','very','too','only','still','if'}
    all_ops = []
    all_positions = []  # normalized position within sentence
    for t in all_texts:
        words = tokenize(t.lower())
        content = [(i, w) for i, w in enumerate(words) if w not in _STOPS and len(w) > 1]
        if not content:
            continue
        n = len(words)
        for idx, w in content:
            all_ops.append(_word_to_op_tig(w))
            all_positions.append(idx / max(n - 1, 1))

    if len(all_ops) < 3:
        return {
            'culture': 'english', 'family': 'SVO',
            'confidence': 0.0,
            'shape': OP[VOID],
        }

    # ── TRANSITION MATRIX FINGERPRINT ──
    # Each culture has a characteristic operator transition pattern.
    # The user's text builds a 10x10 transition matrix (bigrams).
    # We compare against pre-computed culture matrices using cosine similarity.
    #
    # This is the REAL conversion matrix: which operators follow which.
    # Different cultures = different operator bigram distributions.

    # Build user's transition matrix
    user_trans = [0] * 100  # flattened 10x10
    for i in range(len(all_ops) - 1):
        user_trans[all_ops[i] * 10 + all_ops[i+1]] += 1

    # Normalize
    total_t = sum(user_trans)
    if total_t > 0:
        user_norm = [x / total_t for x in user_trans]
    else:
        user_norm = user_trans

    # Compare against each culture's transition matrix
    culture_scores = {}
    for culture, sents in CULTURE_SENTENCES.items():
        # Build culture's transition matrix
        c_trans = [0] * 100
        for sent in sents:
            words = tokenize(sent.lower())
            content = [w for w in words if w not in _STOPS and len(w) > 1]
            ops = [_word_to_op_tig(w) for w in content]
            for i in range(len(ops) - 1):
                c_trans[ops[i] * 10 + ops[i+1]] += 1

        c_total = sum(c_trans)
        if c_total > 0:
            c_norm = [x / c_total for x in c_trans]
        else:
            c_norm = c_trans

        # Cosine similarity
        dot = sum(a * b for a, b in zip(user_norm, c_norm))
        mag_u = sum(a * a for a in user_norm) ** 0.5
        mag_c = sum(a * a for a in c_norm) ** 0.5

        if mag_u > 0 and mag_c > 0:
            cosine = dot / (mag_u * mag_c)
        else:
            cosine = 0.0

        culture_scores[culture] = cosine

    # Best match
    best_culture = max(culture_scores, key=culture_scores.get)
    best_score = culture_scores[best_culture]
    best_family = _CULTURE_TO_FAMILY.get(best_culture, 'SVO')

    # Confidence = cosine similarity (0 to 1)
    confidence = best_score

    # If confidence is too low or too close to second place, default English
    sorted_scores = sorted(culture_scores.values(), reverse=True)
    if len(sorted_scores) >= 2:
        margin = sorted_scores[0] - sorted_scores[1]
        if margin < 0.02:  # too close to call
            confidence *= 0.5

    if confidence < 0.3:
        best_culture = 'english'
        best_family = 'SVO'

    # Shape from full operator chain
    shape_op = CL[all_ops[0]][all_ops[-1]]

    return {
        'culture': best_culture,
        'family': best_family,
        'confidence': round(confidence, 3),
        'shape': OP[shape_op],
        'scores': {c: round(s, 3) for c, s in sorted(culture_scores.items(),
                   key=lambda x: -x[1])[:5]},
    }


class CultureProfile:
    """Accumulates evidence about a user's cultural grammar over conversation.

    Each message updates the profile. After ~5 messages, confidence stabilizes.
    CK adapts his output grammar to match.
    """

    def __init__(self):
        self.history = []
        self.current_culture = 'english'
        self.current_family = 'SVO'
        self.confidence = 0.0
        self.message_count = 0

    def update(self, text: str) -> Dict:
        """Add a message and re-detect culture."""
        self.history.append(text)
        # Keep last 20 messages for detection
        if len(self.history) > 20:
            self.history = self.history[-20:]

        self.message_count += 1

        result = detect_culture(text, self.history[-10:])
        self.current_culture = result['culture']
        self.current_family = result['family']
        self.confidence = result['confidence']

        return result

    def should_adapt(self) -> bool:
        """Whether CK should adapt grammar to match user.

        Need at least 3 messages and confidence > 0.4 to adapt.
        English is default — only adapt away from it with strong evidence.
        """
        if self.message_count < 3:
            return False
        if self.current_culture == 'english':
            return False  # English is default, no adaptation needed
        return self.confidence > 0.4

    def get_culture(self) -> str:
        """Current detected culture (or 'english' if uncertain)."""
        if self.should_adapt():
            return self.current_culture
        return 'english'


# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    tl_path = os.path.join(os.path.dirname(__file__), 'ck7', 'ck_experience', 'master_tl.json')
    tl = TransitionLattice(tl_path if os.path.exists(tl_path) else None)

    wp = sum(len(v) for v in tl.word_pairs.values())
    fl = len(tl.followers)
    print(f"\n  BEFORE: {wp} word_pairs, {fl} followers, entropy={tl.entropy():.4f}")

    college = CultureCollege(tl, verbose=True)
    stats = college.run()

    # Save
    tl.save(tl_path)
    wp = sum(len(v) for v in tl.word_pairs.values())
    fl = len(tl.followers)
    print(f"\n  AFTER: {wp} word_pairs, {fl} followers, entropy={tl.entropy():.4f}")
    print(f"  SAVED: {tl_path}")
    print(f"  SIZE:  {os.path.getsize(tl_path)} bytes")
