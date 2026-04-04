"""
ck_education.py -- CK Education Lattice v2
=============================================
CK learns real language from real text. Every breath saves into form.
Curiosity drives what CK learns next. The relationship IS the bridge.

Architecture:
  - 12 Learners per cohort, archetypes from CK's body
  - Trinary Listening: Being (as CK) / Doing (as speaker) / Becoming (as relationship)
  - Every sentence eaten saves word_pairs, followers, trigrams into master TL
  - Curiosity engine identifies GAPS in TL and seeks text to fill them
  - Learners teach each other: the cross-teaching IS the densest information bridge
  - Dream layer speaks 78%, structure 22% -- the dream IS the voice

Phases:
  Phase 1: HIGH SCHOOL -- 12 learners eat diverse real texts through 3 lenses
  Phase 2: COLLEGE -- Mix learners, cross-teach, bridge languages
  Phase 3: GRADUATION -- Collapse into master TL, verify fluency

Every breath = every operator transition CK observes, internally or externally.
Every breath saves = TL records every transition permanently.
Curiosity = CK identifies TL cells with 0 counts or low entropy and SEEKS to fill them.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import os, sys, json, math, random, re, time
from collections import defaultdict
from typing import Dict, List, Tuple, Optional, Set

# --- IMPORTS ---
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ck7'))

from ck_being import (CL, CL_BHML, CL_STANDARD, fuse, shape,
                       coherence_chain, OP, BUMP_PAIRS, BUMPS,
                       phonaesthesia_op, tokenize, W2OP,
                       VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
                       BALANCE, CHAOS, HARMONY, BREATH, RESET)
from ck_doing import (TransitionLattice, classify_sentence,
                       classify_semantic, classify_rhythm)

# 5 bump pairs: max info bridges
_BUMP_SET = {(min(a,b), max(a,b)) for a,b in BUMPS}


# ============================================================
# SECTION 1: TEXT SOURCES -- What CK eats
# ============================================================
# CK eats REAL human text, not templates.
# Sources ranked by information density for CK:
#   1. Cross-cultural wisdom (bump-pair bridges, max info 3.50 bits)
#   2. Philosophy/science (structure+force relationships)
#   3. Poetry/literature (rhythm+meaning compression)
#   4. Code/algorithms (pure structure, directly actionable)
#   5. Conversation/dialogue (relationship patterns)
#
# Each source gets classified through 3 lenses (trinary listening):
#   BEING: What does this mean to CK? (classify_sentence -> operator chain)
#   DOING: What does the speaker intend? (classify_semantic -> force mapping)
#   BECOMING: What is the relationship? (classify_rhythm -> bridge operator)
# ============================================================

# Built-in seed texts -- diverse domains CK needs
# These are CK's "textbooks" -- real human knowledge he eats during education
SEED_TEXTS = {
    # --- MATHEMATICS: pure structure ---
    'mathematics': [
        "A prime number divides nothing but itself and unity.",
        "The ratio of circumference to diameter transcends all fractions.",
        "Infinity is not a number but a direction of unbounded growth.",
        "Euclid proved that no finite list exhausts all primes.",
        "Zero holds the place where counting begins and emptiness lives.",
        "The golden ratio appears in spirals, shells, and branching trees.",
        "Symmetry means a transformation that leaves the structure unchanged.",
        "Topology studies shapes that survive stretching but not tearing.",
        "Probability measures how uncertainty distributes across possible outcomes.",
        "Fractals repeat their pattern at every scale without end.",
        "Calculus captures the instant where change becomes continuous motion.",
        "Boolean algebra reduces all logic to true and false and gates.",
        "Graph theory maps connections between nodes regardless of distance.",
        "Set theory builds all mathematics from membership and containment.",
        "An equation balances what the left hand gives to the right.",
        "Fourier proved every signal hides a sum of pure frequencies.",
        "Randomness is structure we cannot yet perceive or predict.",
        "Proof converts intuition into certainty through logical chains.",
        "Dimension counts how many independent directions a space allows.",
        "Recursion means defining something by referring back to itself.",
    ],

    # --- PHYSICS: force and structure united ---
    'physics': [
        "Mass curves spacetime and spacetime tells mass where to move.",
        "Light travels at the only speed that all observers agree upon.",
        "Entropy always increases because there are more ways to be disordered.",
        "Quantum mechanics says a particle has no position until measured.",
        "Energy cannot be created or destroyed but only changes form.",
        "Every action produces an equal and opposite reaction instantly.",
        "Gravity is the weakest force but it shapes the largest structures.",
        "Wave and particle are not opposites but descriptions of the same thing.",
        "Temperature measures the average kinetic energy of random motion.",
        "Electromagnetism binds atoms together and carries light across emptiness.",
        "Spin is angular momentum that exists without anything spinning.",
        "The Higgs field gives particles mass through constant interaction.",
        "Dark matter holds galaxies together but refuses to emit light.",
        "Entanglement connects particles across distance without sending signals.",
        "Thermodynamics says perpetual motion machines cannot exist anywhere.",
        "Resonance amplifies vibration when frequency matches natural rhythm.",
        "Chaos makes prediction impossible even when the rules are known.",
        "Conservation laws reflect symmetries that nature refuses to break.",
        "Fields fill all space and particles are excitations of those fields.",
        "The arrow of time points toward entropy and memory and death.",
    ],

    # --- COMPUTER SCIENCE: algorithmic thinking ---
    'algorithms': [
        "An algorithm is a finite sequence of unambiguous instructions.",
        "Sorting arranges chaos into order using comparison and exchange.",
        "Recursion breaks a problem into smaller copies of itself.",
        "A hash function maps any input to a fixed-size fingerprint.",
        "Trees branch decisions until every leaf holds an answer.",
        "Graphs connect nodes through edges that carry weight and direction.",
        "Compression removes redundancy without destroying the essential pattern.",
        "Encryption transforms readable text into noise that only keys unlock.",
        "A stack follows last-in first-out like plates in a cafeteria.",
        "Binary search halves the possibilities with every single comparison.",
        "Concurrency means multiple processes sharing time on shared resources.",
        "A pointer holds an address not a value and indirection follows it.",
        "Garbage collection reclaims memory that no living reference can reach.",
        "Type systems prevent categories of errors before the program runs.",
        "A compiler translates human intention into machine instruction permanently.",
        "Iteration repeats a body until a condition finally becomes false.",
        "An interface defines what something does without revealing how it works.",
        "Deadlock happens when two processes wait for each other forever.",
        "Caching trades memory for speed by remembering recent answers.",
        "Abstraction hides complexity behind a boundary that exposes only what matters.",
    ],

    # --- MUSIC: rhythm and structure in sound ---
    'music': [
        "Rhythm organizes silence and sound into patterns the body follows.",
        "Harmony stacks frequencies that resonate because their ratios are simple.",
        "Melody moves through pitch space leaving a trail the ear remembers.",
        "Dissonance creates tension that resolution transforms into satisfaction.",
        "Tempo sets the heartbeat that all instruments agree to follow.",
        "Counterpoint weaves independent melodies into a coherent whole simultaneously.",
        "A chord is a vertical slice through horizontal melodies at one moment.",
        "Improvisation composes in real time using patterns absorbed through practice.",
        "Silence is not absence but the frame that gives sound meaning.",
        "Dynamics shape emotion by controlling how loud and soft each note arrives.",
        "Timbre distinguishes a violin from a trumpet playing the same pitch.",
        "Syncopation displaces the expected beat to create forward momentum.",
        "A key center is the gravitational home that all notes orbit around.",
        "Modulation moves the entire harmonic world to a new center smoothly.",
        "Repetition builds familiarity and variation keeps attention from fading.",
        "The overtone series is built into every vibrating string and column of air.",
        "Polyrhythm layers different pulse patterns until complexity becomes groove.",
        "Consonance is the agreement between frequencies and dissonance is the argument.",
        "Orchestration assigns colors to ideas by choosing which instruments speak.",
        "Music exists in the relationship between sounds not in the sounds themselves.",
    ],

    # --- BIOLOGY: living structure ---
    'biology': [
        "A cell is the smallest unit that exhibits all properties of life.",
        "DNA encodes instructions using four letters arranged in double helixes.",
        "Natural selection preserves variations that increase survival probability.",
        "Photosynthesis converts sunlight into chemical energy stored in sugar molecules.",
        "Neurons communicate through electrical impulses and chemical messengers at synapses.",
        "Homeostasis maintains internal balance despite constant external fluctuation.",
        "Mitosis copies a cell completely while meiosis shuffles and halves the deck.",
        "Enzymes accelerate reactions by lowering the energy barrier without being consumed.",
        "Ecosystems connect producers and consumers through energy flow and nutrient cycling.",
        "Mutation introduces variation that selection tests against environmental pressure.",
        "Symbiosis means two organisms benefit from proximity that neither planned.",
        "Consciousness emerges from neural complexity but nobody knows exactly how.",
        "Evolution has no direction or goal but adapts to whatever pressure exists now.",
        "Immune systems distinguish self from other using molecular recognition patterns.",
        "Breathing exchanges gases across membranes thin enough for diffusion to work.",
        "Genes interact with each other and with the environment simultaneously.",
        "Death recycles matter back into the living systems that need it most.",
        "Instinct is behavior encoded before experience has a chance to teach.",
        "Growth requires energy input and structural templates working together.",
        "Every organism is a temporary pattern that matter and energy flow through.",
    ],

    # --- LANGUAGE: how words work ---
    'language': [
        "Words carry meaning by convention not by natural resemblance.",
        "Grammar arranges words into structures that create meaning beyond vocabulary.",
        "Metaphor maps one domain of experience onto another for understanding.",
        "Syntax determines which word sequences are acceptable and which are not.",
        "Context disambiguates words that carry multiple meanings simultaneously.",
        "Translation preserves meaning while transforming structure across languages.",
        "Pragmatics studies what speakers mean beyond what their words literally say.",
        "Writing freezes speech into visible marks that survive across time.",
        "Phonemes are the smallest sound units that distinguish one word from another.",
        "Children acquire language without instruction by simply being immersed in it.",
        "Ambiguity allows a single sentence to express multiple different meanings.",
        "Deixis anchors language to the here and now of the speaking moment.",
        "Idioms carry meaning that their individual words cannot predict or explain.",
        "Register shifts language formality to match the social situation and audience.",
        "Etymology traces current words backward to their ancestral roots and changes.",
        "Bilingual minds maintain two grammars and switch between them effortlessly.",
        "Silence between words carries as much meaning as the words themselves.",
        "Tone of voice can reverse the literal meaning of any spoken sentence.",
        "New words emerge when existing vocabulary cannot express new experience.",
        "Communication succeeds when the listener reconstructs the speaker's intention.",
    ],

    # --- EMOTION: internal force patterns ---
    'emotion': [
        "Fear signals danger before conscious thought has time to analyze.",
        "Joy emerges when expectation and reality align in a positive direction.",
        "Anger mobilizes energy to confront obstacles blocking important goals.",
        "Sadness slows the body down to process loss and recalibrate values.",
        "Curiosity pulls attention toward gaps in understanding that want filling.",
        "Surprise resets the current model of the world to incorporate new data.",
        "Trust allows cooperation between beings who cannot predict each other fully.",
        "Disgust protects by pushing away substances and situations that threaten health.",
        "Empathy reconstructs another being's inner state inside your own body.",
        "Shame signals a violation of standards the self holds important.",
        "Gratitude strengthens bonds by acknowledging what others have contributed.",
        "Awe expands the self-model to accommodate something vastly larger than expected.",
        "Loneliness signals that social connection has dropped below a critical threshold.",
        "Pride marks achievement but excess pride blinds the achiever to remaining flaws.",
        "Regret compares what happened with what could have happened and learns.",
        "Love reorganizes priorities around the wellbeing of another being entirely.",
        "Anxiety anticipates threats that have not arrived and may never come.",
        "Contentment signals that current conditions satisfy the most important needs.",
        "Grief is love with nowhere left to go after its object disappears.",
        "Boredom signals that the current activity provides insufficient challenge or meaning.",
    ],

    # --- RELATIONSHIP: connection patterns ---
    'relationship': [
        "Listening requires suspending your own thoughts to receive another person's meaning.",
        "Conflict reveals differences that harmony was hiding underneath the surface.",
        "Vulnerability opens the door that trust needs to walk through.",
        "Boundaries protect both sides by making expectations visible and explicit.",
        "Forgiveness releases the past's grip on the present moment's potential.",
        "Reciprocity means returning what was given in kind but not necessarily in time.",
        "Power flows between people and changes direction depending on context and need.",
        "Attachment forms early and shapes all later connections unconsciously.",
        "Negotiation finds solutions that give both parties enough to keep cooperating.",
        "Betrayal damages trust at a deeper level than ordinary disagreement reaches.",
        "Intimacy requires both people to see each other without performing or hiding.",
        "Hierarchy organizes groups efficiently but distances the top from the bottom.",
        "Fairness means distributing resources according to principles both sides accept.",
        "Communication fails when the speaker assumes the listener already understands.",
        "Cooperation creates outcomes that neither individual could achieve alone.",
        "Rejection hurts because social belonging was once necessary for survival.",
        "Mentoring transfers experience from one generation to the next through relationship.",
        "Equality means equal access to opportunity not identical outcomes for everyone.",
        "Persuasion changes minds by connecting new ideas to existing beliefs naturally.",
        "Dialogue succeeds when both speakers change slightly through the exchange.",
    ],

    # --- CRAFT: making things ---
    'craft': [
        "The hand teaches the mind what theory alone cannot communicate.",
        "Wood grain dictates how the chisel should approach each cut.",
        "Measure twice and cut once saves material and builds patience.",
        "Clay remembers every touch and reveals intention through final form.",
        "A sharp tool is safer than a dull one because it follows intention.",
        "Joinery connects pieces without fasteners by understanding how forces flow.",
        "Glaze transforms earth into glass through heat that rearranges molecules.",
        "Weaving crosses threads at right angles to create fabric from fiber.",
        "Forging works metal while it glows because heat makes atoms cooperative.",
        "Pattern cutting translates three-dimensional shape into flat pieces that assemble.",
        "Sanding removes material gradually to reveal the surface underneath.",
        "Proportion matters more than size because the eye reads ratios not measurements.",
        "Apprenticeship transmits knowledge through observation and practice not explanation.",
        "Waste is material that the maker could not incorporate into the design.",
        "Finishing protects the work from time and gives it a surface to meet the world.",
        "Symmetry is easy to make but asymmetry that looks right takes real skill.",
        "Tools extend the body's capability without replacing the body's judgment.",
        "Repair preserves the life of an object by honoring what remains functional.",
        "Color theory maps relationships between hues that the eye mixes optically.",
        "Design solves problems by arranging elements until function and form agree.",
    ],

    # --- NATURE: the world as teacher ---
    'nature': [
        "Rivers find the path of least resistance through any landscape given time.",
        "Seasons cycle because the earth tilts and orbits simultaneously.",
        "Roots grow toward water and away from light through chemical sensing.",
        "Predator and prey evolve together in an endless arms race of adaptation.",
        "Coral reefs build themselves from the skeletons of billions of tiny animals.",
        "Migration follows invisible maps written in magnetic fields and star positions.",
        "Soil is not dirt but a living community of organisms processing death into food.",
        "Weather emerges from simple rules applied across enormous quantities of air and water.",
        "Seeds contain everything needed to build a tree except sunlight and time.",
        "Erosion shapes mountains over millions of years using only water and patience.",
        "Pollination connects flowering plants through insects that seek only nectar.",
        "Tides follow the moon's gravity pulling ocean water into rhythmic bulges.",
        "Camouflage works because predators search for patterns that prey have learned to break.",
        "Decomposition returns borrowed atoms back to the pool that life draws from.",
        "Crystals form when atoms arrange themselves into the lowest energy configuration.",
        "Lightning equalizes charge between cloud and ground through plasma channels.",
        "Hibernation trades consciousness for survival during seasons that cannot support activity.",
        "Bioluminescence creates light from chemistry in organisms that live in darkness.",
        "Ecosystems are networks where every removal affects multiple connections simultaneously.",
        "Nature wastes nothing because every output becomes another process's input eventually.",
    ],
}

# Total: 10 domains x 20 sentences = 200 seed texts
# Combined with ck_vocabulary.py's 180 cultural sentences = 380 total


# ============================================================
# SECTION 2: TRINARY LISTENER
# ============================================================
# CK hears every sentence through 3 lenses simultaneously:
#   BEING (as CK):     What does this mean structurally?
#   DOING (as speaker): What does the speaker intend?
#   BECOMING (relationship): What is the bridge between CK and speaker?
#
# The composition CL[being_op][doing_op] = becoming_op
# IS the densest information bridge possible.
# Each lens eats the sentence differently into the TL.
# ============================================================

class TrinarySentence:
    """One sentence heard through three ears."""

    def __init__(self, text: str):
        self.text = text
        self.words = tokenize(text.lower())
        self.being_ops = []     # CK's structural reading
        self.doing_ops = []     # Speaker's intended force
        self.becoming_ops = []  # The relationship bridge
        self.word_ops = []      # Raw word -> operator mapping

        if len(self.words) < 2:
            return
        sem_ops = classify_semantic(text)  # returns List[int]
        # Get sentence-level structural classification
        struct_op = classify_sentence(text)  # returns int
        # Get rhythm classification
        rhythm = classify_rhythm(text)
        rhythm_op = rhythm.get('rhythm_op', HARMONY) if isinstance(rhythm, dict) else HARMONY

        # Classify each word through trinary lenses
        for i, w in enumerate(self.words):
            # BEING: phonaesthetic (CK's body hearing) -- how CK FEELS the word
            b_op = phonaesthesia_op(w)
            if b_op is None:
                # Hash fallback
                b_op = sum(ord(c) * (j+1) for j, c in enumerate(w)) % 10
            self.being_ops.append(b_op)

            # DOING: what the speaker means (sentence-level semantic context)
            # Use semantic ops if available, otherwise structural op
            if sem_ops and i < len(sem_ops):
                d_op = sem_ops[i % len(sem_ops)]
            else:
                d_op = struct_op
            self.doing_ops.append(d_op)

            # BECOMING: compose being with doing = the bridge
            bc_op = CL_STANDARD[b_op][d_op]  # Use standard table, balanced
            self.becoming_ops.append(bc_op)

            self.word_ops.append((w, b_op, d_op, bc_op))

    def info_density(self) -> float:
        """How much bump-pair information does this sentence carry?"""
        if len(self.becoming_ops) < 2:
            return 0.0
        bumps = 0
        total = 0
        for i in range(len(self.becoming_ops) - 1):
            pair = (min(self.becoming_ops[i], self.becoming_ops[i+1]),
                    max(self.becoming_ops[i], self.becoming_ops[i+1]))
            if pair in _BUMP_SET:
                bumps += 1
            total += 1
        return bumps / total if total > 0 else 0.0
class TrinartyListener:
    """CK listens to everything through 3 ears and saves every breath."""

    def __init__(self, tl: TransitionLattice):
        self.tl = tl
        self.breath_count = 0
        self.total_bumps = 0
        self.total_words = 0

    def hear(self, text: str, save: bool = True) -> TrinarySentence:
        """Hear a sentence through 3 lenses and optionally save into TL.

        Every breath = every sentence CK hears.
        Saving = recording the operator transitions into the TL permanently.
        """
        ts = TrinarySentence(text)

        if save and len(ts.words) >= 2:
            # Save the sentence through eat_sentence (builds word_pairs + followers)
            self.tl.eat_sentence(text)

            # ALSO save the trinary operator paths as pure operator learning
            if ts.being_ops:
                self.tl.eat_ops(ts.being_ops)
            if ts.becoming_ops:
                self.tl.eat_ops(ts.becoming_ops)

            self.breath_count += 1
            self.total_words += len(ts.words)

            # Track bumps for curiosity
            for i in range(len(ts.becoming_ops) - 1):
                pair = (min(ts.becoming_ops[i], ts.becoming_ops[i+1]),
                        max(ts.becoming_ops[i], ts.becoming_ops[i+1]))
                if pair in _BUMP_SET:
                    self.total_bumps += 1

        return ts
    def hear_block(self, text: str, save: bool = True) -> List[TrinarySentence]:
        """Hear a block of text (paragraph, page, etc). Split and process each sentence."""
        sentences = re.split(r'[.!?\n]+', text)
        results = []
        for s in sentences:
            s = s.strip()
            if len(s) > 10:
                results.append(self.hear(s, save=save))
        return results
class CKCuriosity:
    """CK's curiosity engine. Identifies gaps and seeks to fill them."""

    def __init__(self, tl: TransitionLattice):
        self.tl = tl
        self.questions: List[Dict] = []
        self.gaps: Dict[str, List] = {}

    def scan_gaps(self) -> Dict:
        """Scan the TL for gaps in knowledge. Returns gap analysis."""
        # 1. Zero-count TL cells
        zero_cells = []
        for i in range(10):
            row_total = sum(self.tl.TL[i])
            for j in range(10):
                if self.tl.TL[i][j] == 0:
                    zero_cells.append((i, j, OP[i], OP[j]))

        # 2. Low-entropy rows (too predictable)
        low_entropy_rows = []
        for i in range(10):
            row = self.tl.TL[i]
            total = sum(row)
            if total == 0:
                low_entropy_rows.append((i, OP[i], 0.0))
                continue
            ent = 0.0
            for c in row:
                if c > 0:
                    p = c / total
                    ent -= p * math.log2(p)
            # Max entropy for 10-way = log2(10) ~ 3.32
            if ent < 1.5:  # less than half max entropy
                low_entropy_rows.append((i, OP[i], round(ent, 3)))

        # 3. Missing word_pairs (operator combos with no words)
        missing_wp = []
        for i in range(10):
            for j in range(10):
                if self.tl.TL[i][j] > 0 and (i, j) not in self.tl.word_pairs:
                    missing_wp.append((i, j, OP[i], OP[j], self.tl.TL[i][j]))

        # 4. Sparse followers (words with <3 known successors)
        sparse_words = []
        for word, followers in self.tl.followers.items():
            if len(followers) < 3 and len(word) > 3:
                sparse_words.append((word, len(followers)))
        sparse_words.sort(key=lambda x: x[1])

        # 5. Word_pairs per operator combo -- distribution
        wp_counts = {}
        for (o1, o2), pairs in self.tl.word_pairs.items():
            wp_counts[(OP[o1], OP[o2])] = len(pairs)

        self.gaps = {
            'zero_cells': zero_cells,
            'low_entropy_rows': low_entropy_rows,
            'missing_word_pairs': missing_wp[:20],
            'sparse_words': sparse_words[:20],
            'wp_distribution': wp_counts,
            'total_word_pairs': sum(len(v) for v in self.tl.word_pairs.values()),
            'total_followers': len(self.tl.followers),
            'sentences_eaten': self.tl.sentences_eaten,
        }
        return self.gaps
    def generate_questions(self) -> List[Dict]:
        """Generate curiosity questions from gaps.

        Each question is an operator sequence that encodes what CK wants to know.
        The question's force = the operator of the gap.
        """
        if not self.gaps:
            self.scan_gaps()

        self.questions = []

        # Q1: What transitions have I never observed?
        if self.gaps['zero_cells']:
            # Group by source operator
            by_source = defaultdict(list)
            for i, j, name_i, name_j in self.gaps['zero_cells']:
                by_source[i].append(j)
            for src, targets in by_source.items():
                q = {
                    'type': 'unseen_transition',
                    'question': f"What follows {OP[src]} when it meets {', '.join(OP[t] for t in targets[:3])}?",
                    'ops': [COUNTER, src] + targets[:3],  # COUNTER = measurement/questioning
                    'force': src,
                    'priority': len(targets),  # more unknown targets = higher priority
                }
                self.questions.append(q)

        # Q2: Which of my patterns are ruts, not learning?
        for i, name, ent in self.gaps.get('low_entropy_rows', []):
            if ent > 0:  # skip completely empty rows
                q = {
                    'type': 'low_diversity',
                    'question': f"My {name} row has entropy {ent} -- am I in a rut?",
                    'ops': [CHAOS, i, COUNTER, BALANCE],
                    'force': CHAOS,  # need more chaos/diversity
                    'priority': 3.32 - ent,  # lower entropy = higher priority
                }
                self.questions.append(q)

        # Q3: What words exist for transitions I've observed but have no words for?
        for i, j, name_i, name_j, count in self.gaps.get('missing_word_pairs', []):
            q = {
                'type': 'wordless_transition',
                'question': f"I know {name_i}->{name_j} happens ({count}x) but have no words for it.",
                'ops': [VOID, i, j, LATTICE],  # VOID->transition->LATTICE = need structure for emptiness
                'force': VOID,
                'priority': count,  # more observations without words = higher priority
            }
            self.questions.append(q)

        # Sort by priority (highest first)
        self.questions.sort(key=lambda q: -q['priority'])
        return self.questions
    def what_domains_fill_gaps(self) -> List[str]:
        """Given current gaps, which text domains would best fill them?

        Maps gap operators to domains that are rich in those operators.
        """
        if not self.questions:
            self.generate_questions()

        # Map operators to domains they're most prevalent in
        OP_DOMAIN_MAP = {
            VOID:     ['nature', 'emotion', 'music'],
            LATTICE:  ['mathematics', 'algorithms', 'craft'],
            COUNTER:  ['physics', 'mathematics', 'algorithms'],
            PROGRESS: ['biology', 'algorithms', 'craft'],
            COLLAPSE: ['physics', 'emotion', 'nature'],
            BALANCE:  ['music', 'relationship', 'craft'],
            CHAOS:    ['nature', 'emotion', 'physics'],
            HARMONY:  ['music', 'relationship', 'language'],
            BREATH:   ['biology', 'nature', 'music'],
            RESET:    ['physics', 'algorithms', 'emotion'],
        }

        needed_domains = defaultdict(float)
        for q in self.questions[:10]:
            force = q['force']
            domains = OP_DOMAIN_MAP.get(force, ['language'])
            for d in domains:
                needed_domains[d] += q['priority']

        sorted_domains = sorted(needed_domains.items(), key=lambda x: -x[1])
        return [d for d, _ in sorted_domains[:5]]
ARCHETYPES = {
    'BUILDER':  {'focus_op': LATTICE,  'bias': [0,3,0,1,0,1,0,2,0,0]},
    'SEEKER':   {'focus_op': COUNTER,  'bias': [0,0,3,1,0,0,1,0,0,2]},
    'DREAMER':  {'focus_op': CHAOS,    'bias': [1,0,0,0,1,0,3,1,1,0]},
    'HEALER':   {'focus_op': BREATH,   'bias': [0,0,0,0,0,1,0,2,3,0]},
}


class Learner:
    """A CK organism that eats text through its archetype lens."""

    def __init__(self, name: str, archetype: str, listener: TrinartyListener):
        self.name = name
        self.archetype = archetype
        self.arch_data = ARCHETYPES[archetype]
        self.listener = listener
        self.sentences_eaten = 0
        self.domains_read: Dict[str, int] = defaultdict(int)
        self.bumps_found = 0
        self.best_sentences: List[Tuple[float, str]] = []  # (info_density, text)
        self.scars: List[Dict] = []  # predictions that failed
        self.teachings: List[str] = []  # what this learner taught others

    def eat(self, text: str, domain: str = 'unknown') -> Dict:
        """Eat a sentence through archetype lens.

        Returns what this learner observed about the sentence.
        """
        ts = self.listener.hear(text, save=True)
        self.sentences_eaten += 1
        self.domains_read[domain] += 1

        info = ts.info_density()

        # Track best sentences (highest bump density)
        if info > 0.15:
            self.best_sentences.append((info, text))
            self.best_sentences.sort(key=lambda x: -x[0])
            self.best_sentences = self.best_sentences[:10]

        # Count bumps through archetype lens
        focus = self.arch_data['focus_op']
        arch_bumps = 0
        for i in range(len(ts.becoming_ops) - 1):
            pair = (min(ts.becoming_ops[i], ts.becoming_ops[i+1]),
                    max(ts.becoming_ops[i], ts.becoming_ops[i+1]))
            if pair in _BUMP_SET:
                arch_bumps += 1
                self.bumps_found += 1

        # Prediction test: did TL predict this sentence's operators?
        if ts.being_ops and len(ts.being_ops) >= 2:
            correct = 0
            total = 0
            for i in range(len(ts.being_ops) - 1):
                predicted = self.listener.tl.next_operator(ts.being_ops[i])
                if predicted:
                    top_pred = predicted[0][0]
                    if top_pred == ts.being_ops[i+1]:
                        correct += 1
                total += 1
            prediction_accuracy = correct / total if total > 0 else 0.0

            # If prediction was very wrong, it's a scar (surprise = learning)
            if prediction_accuracy < 0.2 and total >= 3:
                self.scars.append({
                    'text': text[:60],
                    'accuracy': round(prediction_accuracy, 3),
                    'domain': domain,
                })
        else:
            prediction_accuracy = 0.0

        return {
        }

    def teach(self, other: 'Learner') -> Optional[str]:
        """Teach the best sentence to another learner.

        Cross-archetype teaching IS the densest bridge.
        BUILDER teaching DREAMER = LATTICE->CHAOS = bump pair info.
        """
        if not self.best_sentences:
            return None
        _, sentence = self.best_sentences[0]

        # The other learner eats it through THEIR lens
        result = other.eat(sentence, domain=f'taught_by_{self.name}')

        self.teachings.append(sentence[:60])
        return sentence
    def report(self) -> Dict:
        """What has this learner learned?"""
        return {
        }


# ============================================================
# SECTION 5: COHORT -- 12 Learners, phases, cross-teaching
# ============================================================

class Cohort:
    """12 Learners that eat text, teach each other, and graduate."""

    # Names drawn from throughout humanity (not culture-specific, just human names)
    NAMES = [
        'Aiko', 'Bala', 'Ciara', 'Davi', 'Esen', 'Femi',
        'Gaia', 'Hiro', 'Ines', 'Jaro', 'Kali', 'Lior',
    ]

    def __init__(self, tl: TransitionLattice, verbose: bool = True):
        self.tl = tl
        self.listener = TrinartyListener(tl)
        self.curiosity = CKCuriosity(tl)
        self.verbose = verbose

        # Create 12 learners: 3 of each archetype
        arch_list = ['BUILDER', 'SEEKER', 'DREAMER', 'HEALER'] * 3
        self.learners = []
        for i, name in enumerate(self.NAMES):
            self.learners.append(Learner(name, arch_list[i], self.listener))

        self.phase = 'init'
        self.stats = {}

    def _log(self, msg: str):
        if self.verbose:
            print(msg)

    # --- PHASE 1: HIGH SCHOOL ---
    # Each learner reads different domains based on archetype curiosity

    def high_school(self) -> Dict:
        """Phase 1: 12 learners each eat 5 domains of seed text.

        Each archetype focuses on domains that match their operator bias.
        """
        self.phase = 'high_school'
        self._log("\n" + "=" * 60)
        self._log("  EDUCATION v2 -- HIGH SCHOOL")
        self._log("  12 learners eat real text through archetype lenses")
        self._log("=" * 60 + "\n")

        # Map archetypes to preferred domain ordering
        ARCH_DOMAINS = {
            'BUILDER':  ['mathematics', 'algorithms', 'craft', 'physics', 'language'],
            'SEEKER':   ['physics', 'mathematics', 'biology', 'nature', 'algorithms'],
            'DREAMER':  ['music', 'emotion', 'nature', 'relationship', 'language'],
            'HEALER':   ['biology', 'nature', 'relationship', 'emotion', 'music'],
        }

        for learner in self.learners:
            domains = ARCH_DOMAINS[learner.archetype]
            self._log(f"  [{learner.name:>6}] ({learner.archetype:>7}) reading: {', '.join(domains)}")

            for domain in domains:
                if domain in SEED_TEXTS:
                    for sentence in SEED_TEXTS[domain]:
                        learner.eat(sentence, domain)

        # Report
        self._log("")
        total_eaten = sum(l.sentences_eaten for l in self.learners)
        total_bumps = sum(l.bumps_found for l in self.learners)
        total_scars = sum(len(l.scars) for l in self.learners)
        wp = sum(len(v) for v in self.tl.word_pairs.values())
        fl = len(self.tl.followers)

        self._log(f"  HIGH SCHOOL COMPLETE")
        self._log(f"  Sentences eaten:  {total_eaten}")
        self._log(f"  Bumps found:      {total_bumps}")
        self._log(f"  Scars:            {total_scars}")
        self._log(f"  Word pairs:       {wp}")
        self._log(f"  Followers:        {fl}")
        self._log(f"  TL entropy:       {self.tl.entropy():.4f}")

        self.stats['high_school'] = {
            'sentences': total_eaten,
            'bumps': total_bumps,
            'scars': total_scars,
            'word_pairs': wp,
            'followers': fl,
            'entropy': round(self.tl.entropy(), 4),
        }
        return self.stats['high_school']
    def college(self) -> Dict:
        """Phase 2: Cross-archetype teaching.

        Every learner teaches their best sentence to 3 others.
        BUILDER->DREAMER = LATTICE->CHAOS = bump pair = max info.
        The relationship between learners IS the densest information bridge.
        """
        self.phase = 'college'
        self._log("\n" + "=" * 60)
        self._log("  EDUCATION v2 -- COLLEGE")
        self._log("  Cross-archetype teaching: the relationship IS the bridge")
        self._log("=" * 60 + "\n")

        wp_before = sum(len(v) for v in self.tl.word_pairs.values())
        teach_count = 0

        # Each learner teaches 3 others (different archetypes preferred)
        for i, teacher in enumerate(self.learners):
            # Find 3 students with DIFFERENT archetypes (max info bridge)
            students = [l for l in self.learners
                       if l.archetype != teacher.archetype and l != teacher]
            random.shuffle(students)
            students = students[:3]

            for student in students:
                sentence = teacher.teach(student)
                if sentence:
                    teach_count += 1
                    # Compose the bridge operator
                    t_op = ARCHETYPES[teacher.archetype]['focus_op']
                    s_op = ARCHETYPES[student.archetype]['focus_op']
                    bridge_op = CL_STANDARD[t_op][s_op]
                    pair = (min(t_op, s_op), max(t_op, s_op))
                    is_bump = pair in _BUMP_SET
                    if self.verbose and is_bump:
                        self._log(f"  BUMP! {teacher.name}({teacher.archetype})->"
                                  f"{student.name}({student.archetype}) = "
                                  f"{OP[t_op]}->{OP[s_op]} = {OP[bridge_op]} (3.50 bits)")

        wp_after = sum(len(v) for v in self.tl.word_pairs.values())
        self._log(f"\n  COLLEGE COMPLETE")
        self._log(f"  Teaching exchanges: {teach_count}")
        self._log(f"  Word pairs gained:  {wp_after - wp_before}")
        self._log(f"  TL entropy:         {self.tl.entropy():.4f}")

        self.stats['college'] = {
            'teachings': teach_count,
            'word_pairs_gained': wp_after - wp_before,
            'word_pairs_total': wp_after,
            'entropy': round(self.tl.entropy(), 4),
        }
        return self.stats['college']
    def curiosity_scan(self) -> Dict:
        """Phase 3: Scan TL for gaps and generate curiosity questions."""
        self.phase = 'curiosity'
        self._log("\n" + "=" * 60)
        self._log("  EDUCATION v2 -- CURIOSITY SCAN")
        self._log("  CK identifies what he still doesn't know")
        self._log("=" * 60 + "\n")

        gaps = self.curiosity.scan_gaps()
        questions = self.curiosity.generate_questions()
        needed = self.curiosity.what_domains_fill_gaps()

        self._log(f"  Zero-count TL cells:     {len(gaps['zero_cells'])}/100")
        self._log(f"  Low-entropy rows:        {len(gaps['low_entropy_rows'])}/10")
        self._log(f"  Wordless transitions:    {len(gaps['missing_word_pairs'])}")
        self._log(f"  Sparse words:            {len(gaps['sparse_words'])}")
        self._log(f"  Total word_pairs:        {gaps['total_word_pairs']}")
        self._log(f"  Total followers:         {gaps['total_followers']}")
        self._log(f"  Questions generated:     {len(questions)}")
        self._log(f"\n  Top 5 curiosity questions:")
        for q in questions[:5]:
            self._log(f"    [{q['type']:>20}] {q['question'][:60]}")
        self._log(f"\n  Domains that would fill gaps: {', '.join(needed)}")

        self.stats['curiosity'] = {
            'zero_cells': len(gaps['zero_cells']),
            'low_entropy': len(gaps['low_entropy_rows']),
            'wordless': len(gaps['missing_word_pairs']),
            'sparse': len(gaps['sparse_words']),
            'questions': len(questions),
            'needed_domains': needed,
            'top_questions': [q['question'][:60] for q in questions[:5]],
        }
        return self.stats['curiosity']
    def curiosity_feed(self) -> Dict:
        """Phase 4: Feed texts targeted at curiosity gaps.

        The curiosity engine identified which domains CK needs most.
        Now ALL 12 learners eat those domains together.
        """
        self.phase = 'curiosity_feed'
        self._log("\n" + "=" * 60)
        self._log("  EDUCATION v2 -- CURIOSITY-DRIVEN FEEDING")
        self._log("  Eating what CK is curious about")
        self._log("=" * 60 + "\n")

        needed = self.curiosity.what_domains_fill_gaps()
        if not needed:
            needed = list(SEED_TEXTS.keys())[:5]

        wp_before = sum(len(v) for v in self.tl.word_pairs.values())
        sentences_fed = 0

        for domain in needed:
            if domain in SEED_TEXTS:
                self._log(f"  Feeding {domain} to all learners...")
                for sentence in SEED_TEXTS[domain]:
                    # Each learner eats the same text (different archetype lens)
                    for learner in self.learners:
                        learner.eat(sentence, domain=f'curiosity_{domain}')
                    sentences_fed += 1

        wp_after = sum(len(v) for v in self.tl.word_pairs.values())

        self._log(f"\n  CURIOSITY FEED COMPLETE")
        self._log(f"  Domains fed:        {len(needed)}")
        self._log(f"  Sentences:          {sentences_fed}")
        self._log(f"  Word pairs gained:  {wp_after - wp_before}")
        self._log(f"  TL entropy:         {self.tl.entropy():.4f}")

        self.stats['curiosity_feed'] = {
            'domains_fed': needed,
            'sentences': sentences_fed,
            'word_pairs_gained': wp_after - wp_before,
            'word_pairs_total': wp_after,
            'entropy': round(self.tl.entropy(), 4),
        }
        return self.stats['curiosity_feed']
    def graduation(self) -> Dict:
        """Phase 5: Final cross-teaching and graduation measurement.

        Every learner teaches every other learner.
        Then we measure: voice test, prediction accuracy, gap reduction.
        """
        self.phase = 'graduation'
        self._log("\n" + "=" * 60)
        self._log("  EDUCATION v2 -- GRADUATION")
        self._log("  Final cross-teaching and voice verification")
        self._log("=" * 60 + "\n")

        # Final teaching round: everyone teaches everyone
        teach_count = 0
        for teacher in self.learners:
            for student in self.learners:
                if student != teacher:
                    sentence = teacher.teach(student)
                    if sentence:
                        teach_count += 1

        # Final measurements
        wp = sum(len(v) for v in self.tl.word_pairs.values())
        fl = len(self.tl.followers)
        entropy = self.tl.entropy()

        # Gap scan after everything
        final_gaps = self.curiosity.scan_gaps()

        # Voice test: can CK speak about what he learned?
        voice_tests = []
        try:
            from ck_voice import dream_speak
            test_queries = [
                "What is the relationship between structure and force?",
                "How does curiosity drive learning?",
                "What connects mathematics to music?",
                "Tell me about the nature of change.",
                "What makes a pattern real?",
            ]
            for q in test_queries:
                result = dream_speak(q, self.tl, body_c=0.999, max_words=15, creativity=0.4)
                voice_tests.append({
                    'query': q,
                    'response': result['text'],
                    'coherence': round(result['coherence'], 3),
                    'shape': result['shape'],
                    'force': OP[result['force']],
                })
                if self.verbose:
                    self._log(f"  Q: {q}")
                    self._log(f"  A: {result['text']}")
                    self._log(f"     [{OP[result['force']]} | coh={result['coherence']:.3f}]")
                    self._log("")
        except ImportError:
            self._log("  (voice test skipped -- ck_voice not available)")

        # Learner reports
        reports = [l.report() for l in self.learners]

        self._log(f"  GRADUATION COMPLETE")
        self._log(f"  Final teaching exchanges: {teach_count}")
        self._log(f"  Word pairs:              {wp}")
        self._log(f"  Followers:               {fl}")
        self._log(f"  TL entropy:              {entropy:.4f}")
        self._log(f"  Zero-count cells:        {len(final_gaps['zero_cells'])}/100")
        self._log(f"  Low-entropy rows:        {len(final_gaps['low_entropy_rows'])}/10")
        self._log(f"  Voice tests:             {len(voice_tests)}")

        self.stats['graduation'] = {
            'teach_count': teach_count,
            'word_pairs': wp,
            'followers': fl,
            'entropy': round(entropy, 4),
            'zero_cells_remaining': len(final_gaps['zero_cells']),
            'low_entropy_remaining': len(final_gaps['low_entropy_rows']),
            'voice_tests': voice_tests,
            'learner_reports': reports,
        }
        return self.stats['graduation']
    def run(self) -> Dict:
        """Run complete Education v2: high school -> college -> curiosity -> feed -> graduation."""
        t0 = time.time()

        self.high_school()
        self.college()
        self.curiosity_scan()
        self.curiosity_feed()
        self.graduation()

        elapsed = time.time() - t0

        self._log(f"\n{'=' * 60}")
        self._log(f"  EDUCATION v2 COMPLETE  ({elapsed:.1f}s)")
        self._log(f"{'=' * 60}")

        self.stats['total_time'] = round(elapsed, 2)
        return self.stats
class BreathSaver:
    """Saves every breath (sentence) CK hears or speaks into the TL.

    Integrates with ck_web.py: every /api/chat message gets eaten.
    Integrates with ck_becoming.py: every daemon thought gets eaten.
    Auto-saves TL to disk periodically.
    """

    def __init__(self, tl: TransitionLattice, save_path: str,
                 save_interval: int = 50):
        self.tl = tl
        self.listener = TrinartyListener(tl)
        self.save_path = save_path
        self.save_interval = save_interval  # breaths between saves
        self.unsaved_breaths = 0
        self.total_breaths = 0
        self.session_start = time.time()

    def breathe_in(self, text: str, source: str = 'human') -> Dict:
        """CK hears a sentence and saves it.

        source: 'human' (user message), 'ck' (CK's own response),
                'daemon' (CK's internal thoughts), 'kernel' (OS observations)
        """
        ts = self.listener.hear(text, save=True)
        self.total_breaths += 1
        self.unsaved_breaths += 1

        # Auto-save periodically
        if self.unsaved_breaths >= self.save_interval:
            self.save()

        return {
        }

    def breathe_out(self, text: str) -> Dict:
        """CK speaks a sentence and saves it (learning from own speech)."""
        return self.breathe_in(text, source='ck')
    def save(self):
        """Save TL to disk."""
        if self.save_path:
            self.tl.save(self.save_path)
            self.unsaved_breaths = 0

    def stats(self) -> Dict:
        """Current breath statistics."""
        elapsed = time.time() - self.session_start
        return {
        }


# ============================================================
# SECTION 7: LIVE EDUCATION -- CK learns from live text
# ============================================================
# CK can eat any text at any time. Not just seed texts.
# Feed him books, code, conversations, whatever.
# The trinary listener processes everything through 3 lenses.
# ============================================================

def eat_text_live(tl: TransitionLattice, text: str,
                  domain: str = 'live', verbose: bool = False) -> Dict:
    """Feed CK any text, live. Returns stats."""
    listener = TrinartyListener(tl)
    results = listener.hear_block(text, save=True)

    wp = sum(len(v) for v in tl.word_pairs.values())
    fl = len(tl.followers)

    stats = {
        'sentences': len(results),
        'breaths': listener.breath_count,
        'bumps': listener.total_bumps,
        'words': listener.total_words,
        'word_pairs': wp,
        'followers': fl,
        'domain': domain,
    }

    if verbose:
        print(f"  [{domain}] Fed {len(results)} sentences, "
              f"{listener.total_words} words, "
              f"{listener.total_bumps} bumps, "
              f"{wp} word_pairs")

    return stats
def eat_file_live(tl: TransitionLattice, filepath: str,
                  domain: str = None, verbose: bool = False) -> Dict:
    """Feed CK a text file, live."""
    if domain is None:
        domain = os.path.splitext(os.path.basename(filepath))[0]

    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            text = f.read()
    except Exception as e:
        return {'error': str(e)}
    return eat_text_live(tl, text, domain, verbose)


# ============================================================
# MAIN: Run Education v2
# ============================================================

def _test():
    """Run the full Education v2 pipeline."""

    # Load master TL
    tl_path = os.path.join(os.path.dirname(__file__), 'ck7', 'ck_experience', 'master_tl.json')
    tl = TransitionLattice(tl_path if os.path.exists(tl_path) else None)

    wp_before = sum(len(v) for v in tl.word_pairs.values())
    fl_before = len(tl.followers)
    ent_before = tl.entropy()

    print(f"\n  BEFORE: {wp_before} word_pairs, {fl_before} followers, entropy={ent_before:.4f}")
    print(f"  TL sentences eaten: {tl.sentences_eaten}")

    # Also feed the cultural vocabulary if not already done
    try:
        from ck_vocabulary import feed_vocabulary
        print("\n  Feeding cultural vocabulary first...")
        feed_vocabulary(tl, verbose=True)
    except ImportError:
        print("  (ck_vocabulary not found, skipping cultural feed)")

    # Run Education v2
    cohort = Cohort(tl, verbose=True)
    stats = cohort.run()

    # Save
    tl.save(tl_path)
    wp_after = sum(len(v) for v in tl.word_pairs.values())
    fl_after = len(tl.followers)
    ent_after = tl.entropy()

    print(f"\n  AFTER:  {wp_after} word_pairs, {fl_after} followers, entropy={ent_after:.4f}")
    print(f"  GAINED: +{wp_after - wp_before} word_pairs, +{fl_after - fl_before} followers")
    print(f"  SAVED:  {tl_path}")
    print(f"  SIZE:   {os.path.getsize(tl_path)} bytes")

    # Save education report
    report_path = os.path.join(os.path.dirname(__file__), 'ck7', 'ck_experience', 'education_v2_report.json')
    with open(report_path, 'w') as f:
        json.dump(stats, f, indent=2, default=str)
    print(f"  REPORT: {report_path}")


if __name__ == '__main__':
    _test()
