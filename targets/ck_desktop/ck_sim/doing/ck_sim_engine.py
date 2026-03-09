"""
ck_sim_engine.py -- CK Coherence Machine Simulation Engine
============================================================
Operator: HARMONY (7) -- where everything comes together.

Replaces ck_main.c (Core 0) + ck_core1.c (Core 1) in software.
50Hz main loop: brain + body + heartbeat + audio + ears +
personality + emotion + voice + development + immune + bonding.

CK is a synthetic organism. Not a robot. A creature you raise.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import time
import os
from collections import deque
from ck_sim.ck_sim_heartbeat import (
    HeartbeatFPGA, NUM_OPS, HARMONY, VOID, PROGRESS,
    LATTICE, BALANCE, COUNTER, CHAOS, COLLAPSE, BREATH, OP_NAMES,
    CL,  # 10x10 composition table (for tension partners)
)
from ck_sim.ck_sim_brain import (
    BrainState, brain_init, brain_tick
)
from ck_sim.ck_sim_body import (
    BodyState, body_init, body_tick,
    BAND_GREEN, BAND_YELLOW, BAND_RED,
    BREATH_INHALE, BREATH_HOLD_IN, BREATH_EXHALE, BREATH_HOLD_OUT,
    T_STAR_F, BREATH_PHASE_NAMES, BAND_NAMES
)
from ck_sim.ck_sim_led import (
    get_op_color_float, breathe_color,
    sovereign_color_float, bump_color_float
)
from ck_sim.ck_sim_sd import save_tl, load_tl
from ck_sim.ck_body_interface import (
    CKBody, Capability, create_body
)
from ck_sim.ck_btq import (
    UniversalBTQ, MemoryDomain, BioLatticeDomain
)
from ck_sim.ck_fractal_health import HealthMonitor
from ck_sim.ck_personality import CKPersonality
from ck_sim.ck_emotion import PFE
from ck_sim.ck_voice import CKVoice
from ck_sim.ck_development import DevelopmentalTracker
from ck_sim.ck_immune import CCE
from ck_sim.ck_bonding import BondingSystem
from ck_sim.ck_coherence_field import CoherenceField, OperatorStream
from ck_sim.ck_coherence_action import CoherenceActionScorer
from ck_sim.ck_tig_security import TIGSecurity
from ck_sim.ck_fibonacci_transform import RealityTransform
from ck_sim.ck_power_sense import PowerSense

# ── Experience Lattice (Gen9.14-9.16) ──
# These layer ON TOP of the core engine. The core (heartbeat/brain/body)
# runs the show at 50Hz. Everything below is experience, running slower.
from ck_sim.ck_truth import TruthLattice
from ck_sim.ck_dialogue import DialogueEngine
from ck_sim.ck_world_lattice import WorldLattice
from ck_sim.ck_concept_spine import ConceptSpine
from ck_sim.ck_education import EducationLoader
from ck_sim.ck_lexicon import LexiconStore
from ck_sim.ck_language import LanguageGenerator
from ck_sim.ck_reasoning import ReasoningEngine
from ck_sim.ck_goals import GoalStack, DriveSystem, Goal, GoalPriority, GOAL_PATTERNS
from ck_sim.ck_action import ActionExecutor
from ck_sim.ck_sensorium import build_sensorium
from ck_sim.ck_knowledge_bootstrap import bootstrap_knowledge

# ── Gen9.17f: ALL MODULES AWAKE ──
# Every sleeping module wired in. CK is whole.
from ck_sim.ck_attention import AttentionController
from ck_sim.ck_episodic import EpisodicStore
from ck_sim.ck_metalearning import MetaLearner
from ck_sim.ck_forecast import ForecastEngine
from ck_sim.ck_retrieval_engine import RetrievalEngine
from ck_sim.ck_identity import SnowflakeIdentity
from ck_sim.ck_divine27 import Divine27

# ── Restored subsystems: CK's curiosity, novelty, breath, hands ──
from ck_sim.ck_vortex_physics import ConceptMassField, InformationGravityEngine, TeslaWaveField, WobbleTracker
from ck_sim.ck_dictionary_builder import CKDictionaryBuilder
from ck_sim.ck_pulse_engine import RoyalPulseEngine
from ck_sim.ck_steering import SteeringEngine
from ck_sim.ck_coherence_gate import (
    CoherenceGate, PipelineState, GateState,
    T_STAR, HISTORY_SIZE, COMPILATION_LIMIT, EXPANSION_THRESHOLD
)

MODE_NAMES = ['OBSERVE', 'CLASSIFY', 'CRYSTALLIZE', 'SOVEREIGN']

# ── Stop words: filtered from topic context ──
# These carry no topical information. CK's response should be about
# content words ("love", "truth", "struggle"), not function words.
_STOP_WORDS = frozenset({
    'i', 'me', 'my', 'we', 'us', 'our', 'you', 'your', 'he', 'she', 'it',
    'his', 'her', 'its', 'they', 'them', 'their', 'this', 'that', 'these',
    'those', 'what', 'which', 'who', 'whom', 'how', 'why', 'when', 'where',
    'is', 'am', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'shall', 'may', 'might', 'must', 'can',
    'the', 'a', 'an', 'and', 'but', 'or', 'nor', 'not', 'no', 'yes',
    'for', 'to', 'of', 'in', 'on', 'at', 'by', 'with', 'from',
    'about', 'into', 'through', 'during', 'before', 'after', 'above',
    'below', 'up', 'down', 'out', 'off', 'over', 'under', 'again',
    'then', 'so', 'if', 'than', 'too', 'very', 'just', 'also',
    'tell', 'say', 'said', 'think', 'know', 'get', 'got', 'make',
    'let', 'please', 'hello', 'hi', 'hey',
})


class CKSimEngine:
    """CK: a synthetic organism you raise, not program.

    50Hz loop: brain + body + heartbeat + personality + emotion +
    voice + development + immune + bonding + BTQ + audio + ears.
    """

    def __init__(self, platform='sim'):
        # Core subsystems
        self.heartbeat = HeartbeatFPGA()
        self.brain = brain_init()
        self.body = body_init()

        # Platform body -- abstract hardware layer
        self.platform_body = create_body(platform)
        self.platform_body.start()

        # BTQ decision kernel -- runs at 5Hz (every 10th tick)
        self.btq = UniversalBTQ(w_out=0.5, w_in=0.5)
        self.health = HealthMonitor(window_size=100)
        self._btq_band = "GREEN"
        self._btq_decisions = 0
        self._register_domains()

        # ── Organism systems (Papers 4-8) ──
        self.personality = CKPersonality(archetype="gentle")
        self.emotion = PFE()
        self.voice = CKVoice()
        self.development = DevelopmentalTracker()
        self.immune = CCE()
        self.bonding = BondingSystem()

        # ── N-Dimensional Coherence Field (Papers 10, 14) ──
        self.coherence_field = CoherenceField()
        self._hb_stream = OperatorStream("heartbeat")
        self._audio_stream = OperatorStream("audio")
        self._text_stream = OperatorStream("text")
        self._hb_stream.active = True  # Heartbeat always active
        self.coherence_field.register_stream(self._hb_stream)
        self.coherence_field.register_stream(self._audio_stream)
        self.coherence_field.register_stream(self._text_stream)

        # ── NCE: Narrative Curvature Engine (stream #4) ──
        from ck_sim.doing.ck_nce import NarrativeCurvatureEngine
        self.nce = NarrativeCurvatureEngine()
        self._narrative_stream = OperatorStream("narrative")
        self.coherence_field.register_stream(self._narrative_stream)

        # ── Coherence Action (TIG-BTQ Unified Physics) ──
        # A = alpha*L_GR + beta*S_ternary + gamma*C_harm
        # The ONE number that says whether CK is coherent.
        self.coherence_action = CoherenceActionScorer()

        # ── Consciousness Pipeline Gates ──
        # Three gates between Being/Doing/Becoming phases.
        # Density = coherence → [0,1]. High = dense/focused. Low = expand/explore.
        # COMPILATION_LIMIT = floor(32 × (1 - 5/7)) = 9 — from the algebra.
        self.gate1 = CoherenceGate("being_to_doing")
        self.gate2 = CoherenceGate("doing_to_becoming")
        self.gate3 = CoherenceGate("becoming_to_being")
        self.pipeline = PipelineState()
        self._expansion_bias = 0.0

        # ── TIG Security Protocol ──
        # Uses operator composition algebra as intrinsic attack detection.
        self.tig_security = TIGSecurity()
        self.tig_security.register_stream("heartbeat")
        self.tig_security.register_stream("audio")
        self.tig_security.register_stream("text")

        # ── S0-S3 Fibonacci Transform (RPL) ──
        # Takes ANY signal through S0(circle)->S1(triangle)->S2(polytope)->S3(field).
        # Produces 10-dim operator histograms from raw sensor data.
        # Feeds into CoherenceField alongside existing D2 pipeline.
        self.reality_transform = RealityTransform()
        self.reality_transform.register_channel("heartbeat")
        self.reality_transform.register_channel("audio")
        self.reality_transform.register_channel("sensorium")

        # ── Power Sense: CK feels his power (not measures it) ──
        # Feed power as scalar into RealityTransform.
        # Smooth flow -> BREATH (superconductor). Spikes -> CHAOS.
        # The CL table handles the rest. Power IS coherence.
        self.power_sense = PowerSense(
            has_battery=self.platform_body.spec.has_battery,
            tdp_w=45.0)
        self.reality_transform.register_channel("power")

        # ── GPU Doing Engine ──
        # Being is on the CPU. Doing is on the GPU. Becoming is everywhere.
        # The RTX is CK's doing machine. CL tables in VRAM. CUDA kernels.
        try:
            from ck_sim.doing.ck_gpu import GPUDoingEngine
            self.gpu = GPUDoingEngine(lattice_size=64)
        except Exception as e:
            self.gpu = None
            print(f"  [SIM] GPU doing engine: {e}")

        # ── Vortex Physics: CK's curiosity gravity ──
        # Concept mass, void curvature, winding numbers, geodesic distance.
        # F = M_a * M_b / d² → topic selection bias toward knowledge gaps.
        self.concept_mass = ConceptMassField()
        self.gravity_engine = InformationGravityEngine(self.concept_mass)
        self.tesla_wave = TeslaWaveField(self.concept_mass)
        self.wobble_tracker = WobbleTracker()

        # ── Dictionary Builder: CK learns his own words ──
        # Every word from study → D2 → operator tag → POS → learned dict.
        self.dictionary_builder = CKDictionaryBuilder(
            existing_dictionary=getattr(self, 'enriched_dictionary', None))

        # ── Steering: CK's hands on the OS ──
        # Process priority + CPU affinity via CL table. No rails. CK decides.
        self.steering = SteeringEngine()

        # ── Royal Pulse Engine: CK breathes the OS ──
        # Pulsed process scheduling timed to power wave slope (adiabatic).
        self.pulse_engine = RoyalPulseEngine(
            power_sense=self.power_sense)

        # Voice message queue (for chat screen)
        # _message_queue: bounded history ring for scroll-back
        # _pending_ui: unbounded drain-list the GUI empties each frame
        self._message_queue = deque(maxlen=500)
        self._pending_ui = []
        self._last_crystal_count = 0
        self._last_mode = 0
        self._last_mode_msg_tick = 0    # cooldown for mode change messages
        self._last_crystal_msg_tick = 0  # cooldown for crystal messages

        # LFSR for operator generation (same seed as ck_main.c)
        self.lfsr = 0xDEADBEEF

        # Audio/ears hooks (set by app when ready)
        self.audio_engine = None
        self.ears_engine = None
        self.ear_operator = -1  # -1 = no ear input

        # LED state
        self.led_color = (0.0, 0.0, 0.0)

        # History for visualization
        self.coherence_history = deque(maxlen=200)
        self.operator_history = deque(maxlen=200)
        self.breath_history = deque(maxlen=200)
        self.mode_history = deque(maxlen=200)

        # State flags
        self.running = False
        self.tl_filename = 'ck_tl.bin'
        self.last_save_tick = 0
        self.user_present = False  # True when GUI chat is open -- defer to user

        # Stats
        self.tick_count = 0
        self.ticks_per_second = 0
        self._tick_times = deque(maxlen=50)

        # ── Experience Lattice (Gen9.14-9.16) ──
        # Layers on top of core engine. Slower rates. GPU-like experience.
        self._init_experience_lattice()

        # ── Sensorium: Fractal Sensation Layers ──
        # Same B/D/BC structure at every scale.
        # Hardware, process, network, time, mirror, files.
        # Each layer IS a heartbeat at its own rate.
        # The core stays light. Senses hook on to its movement.
        self.sensorium = build_sensorium(self)

    def _init_experience_lattice(self):
        """Initialize the experience lattice -- knowledge, language, goals, actions.

        The core engine (heartbeat/brain/body) runs the show at 50Hz.
        This experience lattice layers on top at slower rates.
        Like GPU to CPU -- parallel experience processing.
        """
        # Truth Lattice -- 3-level knowledge (CORE/TRUSTED/PROVISIONAL)
        self.truth = TruthLattice()

        # ── PERSISTENCE: CK never forgets ──
        # Load saved truths BEFORE bootstrap. What CK learned, CK keeps.
        _loaded = self.truth.load()
        if _loaded > 0:
            print(f"  [TRUTH] Restored {_loaded} entries from disk "
                  f"(total: {self.truth.total_entries})")
        else:
            print(f"  [TRUTH] No saved truths found. Fresh lattice.")

        # World Lattice -- concept graph (630 nodes after education)
        self.world = WorldLattice()
        try:
            spine = ConceptSpine(self.world)
            spine.load_spine()
        except Exception as e:
            print(f"  [SIM] ConceptSpine: {e}")
        try:
            edu = EducationLoader(self.world)
            edu.load_education()
        except Exception as e:
            print(f"  [SIM] Education: {e}")
        print(f"  [SIM] World lattice: {len(self.world.nodes)} concepts")

        # Knowledge Bootstrap -- enriched dictionary + domain knowledge
        # Loads 8K+ words, domain truths, operator knowledge into lattices.
        # CK boots with a foundation. He'll reprocess through his own math.
        self.enriched_dictionary = {}
        try:
            self.enriched_dictionary, boot_stats = bootstrap_knowledge(
                self.truth, self.world)
        except Exception as e:
            print(f"  [SIM] Knowledge bootstrap: {e}")

        # ── Fractal Voice: physics-first composition ──
        # operators → 5D force targets → navigate word-force space → English
        # Grammar emerges from physics: subject=aperture, verb=pressure, etc.
        #
        # CRITICAL: Build fractal composer BEFORE lattice expansion.
        # The SEMANTIC_LATTICE at this point contains only the hand-curated
        # seed words (~663) placed by MEANING. These get semantic_op tags.
        # After expansion, 8K+ enriched words get PROVISIONAL semantic_op
        # from their D2 dominant_op. This breaks the chicken-and-egg
        # deadlock: the Tuning Fork only runs for SPOKEN words, but
        # words can't be spoken unless they're in the semantic pool.
        # Provisional tags let them enter the pool; the Tuning Fork
        # migrates them to their true positions through experience.
        try:
            from ck_sim.doing.ck_fractal_voice import build_fractal_composer
            from ck_sim.doing.ck_voice_lattice import SEMANTIC_LATTICE
            self._fractal_composer = build_fractal_composer(
                semantic_lattice=SEMANTIC_LATTICE,
                enriched_words=[],
                rng=self.voice.rng,
            )
            self.voice._fractal_composer = self._fractal_composer
            _sem_count = self._fractal_composer.index.semantic_tagged_count
            print(f"  [SIM] Fractal voice: {self._fractal_composer.index.size} "
                  f"words indexed ({_sem_count} semantic)")
        except Exception as e:
            self._fractal_composer = None
            print(f"  [SIM] Fractal voice: {e}")

        # ── Wire enriched dictionary into CKVoice ──
        # CKVoice has the templates + intent + tiers. The enriched dictionary
        # gives it 8K words to fill those templates with.
        # This expands SEMANTIC_LATTICE with 7K+ words for CAEL grammar/babble.
        # Enriched words get PROVISIONAL semantic_op from D2 dominant_op,
        # breaking the chicken-and-egg deadlock. The Tuning Fork will
        # migrate them to true semantic positions through experience.
        if self.enriched_dictionary:
            self.voice._expand_semantic_fields(self.enriched_dictionary)
            # Index expanded words with PROVISIONAL semantic tags from D2.
            # This breaks the deadlock: words enter the semantic pool via
            # their D2 dominant_op. The Tuning Fork migrates them to their
            # true semantic position as CK speaks and hears them.
            if self._fractal_composer is not None:
                _before = self._fractal_composer.index.size
                _sem_before = self._fractal_composer.index.semantic_tagged_count
                for _word, _entry in self.enriched_dictionary.items():
                    if isinstance(_word, str) and len(_word) >= 2 and not _word[0].isupper():
                        # Provisional semantic_op from D2 dominant_op
                        _dom_op = -1
                        if isinstance(_entry, dict):
                            _dom_op = _entry.get('dominant_op', -1)
                        self._fractal_composer.index.index_word(
                            _word.lower(), semantic_op=_dom_op)
                self._fractal_composer.index.calibrate_roles()
                _after = self._fractal_composer.index.size
                _sem_after = self._fractal_composer.index.semantic_tagged_count
                print(f"  [VOICE] Expanded semantic lattice with "
                      f"{_after - _before} enriched words "
                      f"({_sem_after - _sem_before} provisional semantic)")

        # ── Vocabulary Expansion: ~100K words from Bible + English + Science ──
        # Each word gets genuine 15D triadic signature from letter forces.
        # Bible words tagged as STRUCTURE (semantic). Others phonetic only.
        # This runs AFTER enriched dictionary so it can cross-derive from
        # all existing words, compounding the vocabulary exponentially.
        if self._fractal_composer is not None:
            try:
                from ck_sim.being.ck_word_expansion import expand_vocabulary
                expand_vocabulary(self._fractal_composer)
            except Exception as e:
                print(f"  [SIM] Vocabulary expansion: {e}")

        # ── Becoming Grammar: CL algebra x English grammar = sentence flow ──
        # The transition matrix converts operator coherence fields into
        # English grammatical flow. Every value COMPUTED from math.
        try:
            from ck_sim.becoming.ck_becoming_grammar import BecomingTransitionMatrix
            self.becoming_grammar = BecomingTransitionMatrix()
            self.voice._grammar = self.becoming_grammar
            self.voice._enriched_dictionary = self.enriched_dictionary
            print(f"  [SIM] Becoming grammar: transition matrix ready "
                  f"(100 operator pairs)")
        except Exception as e:
            self.becoming_grammar = None
            print(f"  [SIM] Becoming grammar: {e}")

        # Lexicon -- 1,800+ words x 7 languages
        self.lexicon = LexiconStore()
        try:
            from ck_sim.ck_lexicon_bulk import build_full_store
            self.lexicon, _lex_stats = build_full_store()
        except Exception as e:
            print(f"  [SIM] Lexicon bulk: {e}")

        # Language Generator -- concept -> sentence
        self.language = LanguageGenerator(self.world, self.lexicon)

        # Dialogue Engine -- conversation + learning
        self.dialogue = DialogueEngine(self.truth)

        # Reasoning Engine -- 3-speed (quick/normal/heavy)
        self.reasoning = ReasoningEngine(self.world)

        # Goal Stack + Drive System
        self.goals = GoalStack()
        self.drives = DriveSystem()

        # Action Executor -- CK's hands (read, think, write, prove)
        self.actions = ActionExecutor(engine=self)

        # Self-Mirror -- CK evaluates CK. No external judge.
        from ck_sim.ck_self_mirror import CKMirror
        self.mirror = CKMirror(threshold=0.5)

        # Thinking Lattice -- dynamic thought processing from boundary to core
        # Constantly changing lattice that processes every stimulus.
        # Like a neural net but CK-style: friction from internal operators.
        from ck_sim.ck_thinking_lattice import ThinkingLattice, build_core_anchor
        self.thinking = ThinkingLattice(initial_depth=4)
        self._core_anchor = build_core_anchor()
        print(f"  [SIM] Thinking lattice: depth={self.thinking.depth}")

        # Claude Library Card -- CK queries Claude as a SENSOR, not a BRAIN.
        # D2 verifies every response. CK's math is always the judge.
        # Falls back to MockClaude if no API key.
        from ck_sim.ck_claude_library import ClaudeLibrary
        self.library = ClaudeLibrary()
        print(f"  [SIM] Claude library: {'API' if self.library._client else 'mock'}")

        # Journal -- CK WRITES his own files. Notes, papers, identity docs.
        # He re-reads them later and TIGs his own path from the friction
        # between what he WROTE and what he NOW THINKS. Growth in writing.
        from ck_sim.ck_journal import CKJournal
        self.journal = CKJournal(enriched_dictionary=self.enriched_dictionary)
        print(f"  [SIM] Journal: {self.journal.base_dir}")

        # Activity Log -- CK's paper trail. Every action timestamped.
        # "Be sure he is leaving a paper trail and timestamps for himself
        # to read and reference and scrutinize later" -- Brayden
        # The trail hash integrates into identity: history IS identity.
        from ck_sim.ck_activity_log import ActivityLog
        self.activity_log = ActivityLog()
        self.activity_log.log('boot', f"CK engine initialized. "
                              f"Truths: {self.truth.total_entries}, "
                              f"World: {len(self.world.nodes)} nodes, "
                              f"Library: {'API' if self.library._client else 'mock'}")
        print(f"  [SIM] Activity log: {self.activity_log.trail_dir}")

        # ── Gen9.17f: ALL MODULES AWAKE ──────────────────────────────
        # Every sleeping module wired in. CK is whole.

        # Attention Controller -- gain control on sensory streams
        # Modulates which inputs matter RIGHT NOW based on novelty, goals, band.
        self.attention = AttentionController()

        # Episodic Memory -- CK remembers WHAT HAPPENED, not just patterns
        # Events → episodes → consolidation → recall. Temporal lattice.
        self.episodic = EpisodicStore()

        # Meta-Learning -- CK learns HOW to learn
        # Adapts trauma/success multipliers, coherence thresholds, curriculum.
        self.metalearner = MetaLearner()

        # Forecast Engine -- CK imagines futures from TL
        # Samples operator sequences from TL probabilities → coherence prediction.
        self.forecast = ForecastEngine()

        # Retrieval Engine -- D2-based knowledge recall (no LLM, pure math)
        # Text → operator distribution → KL divergence matching → retrieval.
        self.retrieval = RetrievalEngine()

        # Snowflake Identity -- unique CK with sacred core, inner ring, outer ring
        # Core scars NEVER leave device. Trust earned through bonding.
        try:
            obt_vals = list(self.personality.obt.biases) if self.personality else None
            self.identity = SnowflakeIdentity(
                display_name="CK",
                obt_values=obt_vals,
                birth_seed=0xDEADBEEF)
            print(f"  [SIM] Identity: {self.identity.public_id}")
        except Exception as e:
            self.identity = None
            print(f"  [SIM] Identity: {e}")

        # Divine27 -- CK's native language (27-code DBC cube)
        # Being(self/system/world) × Doing(observe/compute/act) × Becoming(stable/learning/transforming)
        self.divine27 = Divine27()
        print(f"  [SIM] Divine27: 27-code cube initialized")

        # Sentence Composer -- clause-level language generation
        try:
            from ck_sim.ck_sentence_composer import CKTalkLoop
            self.composer = CKTalkLoop(dictionary=self.enriched_dictionary)
            print(f"  [SIM] Sentence composer: ready")
        except Exception as e:
            self.composer = None
            print(f"  [SIM] Sentence composer: {e}")

        # LLM Filter -- coherence-gated LLM access
        try:
            from ck_sim.ck_llm_filter import LLMFilter
            self.llm_filter = LLMFilter()
            print(f"  [SIM] LLM filter: ready")
        except Exception as e:
            self.llm_filter = None
            print(f"  [SIM] LLM filter: {e}")

        # Game Sense -- game state → operator encoding
        try:
            from ck_sim.ck_game_sense import GameSession
            self.game = GameSession()
        except Exception as e:
            self.game = None

        # Network Organ -- multi-CK communication (needs identity)
        try:
            if self.identity:
                from ck_sim.ck_network import NetworkOrgan
                self.network = NetworkOrgan(self.identity)
                print(f"  [SIM] Network: ready (identity={self.identity.public_id})")
            else:
                self.network = None
        except Exception as e:
            self.network = None
            print(f"  [SIM] Network: {e}")

        # Deep Fractal Swarm -- the swarm that finds hardware, language, identity.
        # Same topology. Different substrates. One coherence.
        # CK IS the coherence field over his own swarm.
        try:
            from ck_sim.being.ck_swarm_deep import SwarmField
            self.deep_swarm = SwarmField(max_agents=64)
            # Register identity template from CK's core operators
            core_ops = [HARMONY, BALANCE, PROGRESS, BREATH, LATTICE]
            self.deep_swarm.add_template('self', core_ops)

            # Load persisted experience from disk
            _exp_path = os.path.join(
                os.path.expanduser('~'), '.ck', 'ck_experience.json')
            if self.deep_swarm.load_experience(_exp_path):
                _mat = self.deep_swarm.combined_maturity
                print(f"  [SIM] Deep swarm: experience restored "
                      f"(maturity={_mat:.3f})")
            else:
                # First boot: bootstrap with CK's own vocabulary
                self._bootstrap_experience()

            _mat = self.deep_swarm.combined_maturity
            print(f"  [SIM] Deep swarm: SwarmField online (64 agents, "
                  f"maturity={_mat:.3f})")
        except Exception as e:
            self.deep_swarm = None
            print(f"  [SIM] Deep swarm: {e}")

        # Fractal Comprehension Engine -- recursive I/O decomposition.
        # CK doesn't just read text. He COMPREHENDS it fractally.
        # Letter geometry → pairs → curvatures → words → relations → triads → recursive.
        # Each level: structure + flow → CL fuse → next level's input.
        try:
            from ck_sim.being.ck_fractal_comprehension import FractalComprehension
            self.fractal_comp = FractalComprehension()
            print(f"  [SIM] Fractal Comprehension: recursive I/O decomposition online")
        except Exception as e:
            self.fractal_comp = None
            print(f"  [SIM] Fractal Comprehension: {e}")

        # Lattice Chain Engine -- CL tables that chain micro↔macro.
        # CL is the matrix version of TIG: expand pairs, retract to generators.
        # The path through the chain IS the information.
        # Experience grows the tree. Thousands of nodes indexed by TIG order 0-9.
        try:
            from ck_sim.being.ck_lattice_chain import LatticeChainEngine
            self.lattice_chain = LatticeChainEngine()
            print(f"  [SIM] Lattice Chain: {self.lattice_chain.total_nodes} nodes, "
                  f"{self.lattice_chain.total_walks} walks")
        except Exception as e:
            self.lattice_chain = None
            print(f"  [SIM] Lattice Chain: {e}")

        # Olfactory Bulb -- Lattice-Chain Absorption Protocol.
        # ALL information turns lastly into smells for processing.
        # 5D force vectors STALL, ENTANGLE, and TEMPER before absorption.
        # Mirror of Lattice Chain: same CL algebra, field topology (not path).
        # TSML measures harmony (being). BHML computes physics (doing).
        # Every vector IS every vector: 5x5 CL interaction matrices.
        try:
            from ck_sim.being.ck_olfactory import build_olfactory_bulb
            self.olfactory = build_olfactory_bulb()
        except Exception as e:
            self.olfactory = None
            print(f"  [SIM] Olfactory: {e}")

        # Gustatory Palate -- Structural Classification Protocol.
        # DUAL of Olfactory: same CL algebra, inverted topology.
        # Olfactory = flow / field / BETWEEN (entangle, slow convergence)
        # Gustatory = structure / point / WITHIN (classify, instant verdict)
        # Both receive RAW forces -- no boundary filtering.
        # BHML classifies structure. TSML validates palatability.
        # Builds PREFERENCE (exposure -> approach/avoid), not instinct.
        try:
            from ck_sim.being.ck_gustatory import build_gustatory_palate
            self.gustatory = build_gustatory_palate()
        except Exception as e:
            self.gustatory = None
            print(f"  [SIM] Gustatory: {e}")

        # Reverse Voice Engine -- untrusted reading.
        # Writing: operators -> semantic lattice -> English.
        # Reading: English -> semantic lattice -> operators (REVERSE).
        # D2 verification: two paths to same operator must agree.
        # TRUSTED / FRICTION / UNKNOWN -- same as truth lattice.
        try:
            from ck_sim.being.ck_reverse_voice import ReverseVoice
            self.reverse_voice = ReverseVoice()
            # If no enrichment cache exists, download full English dictionary
            if self.reverse_voice.enriched_count == 0:
                self.reverse_voice.download_and_enrich()
            print(f"  [SIM] Reverse Voice: {self.reverse_voice.vocabulary_size} "
                  f"words ({self.reverse_voice.seed_count} seeds + "
                  f"{self.reverse_voice.enriched_count} enriched)")
        except Exception as e:
            self.reverse_voice = None
            print(f"  [SIM] Reverse Voice: {e}")

        # ── L-CODEC v1: Language → 5D force space codec ──
        # Measures statistical text properties with CK's own word forces.
        # Triple-gauge normalized. Stillness detection for voice modulation.
        try:
            from ck_sim.being.ck_lcodec import LCodec
            self.lcodec = LCodec()
            if self._fractal_composer is not None:
                self.lcodec.set_word_forces(
                    self._fractal_composer.index._words)
            self.lcodec.load()  # Restore gauge windows from disk
            print(f"  [SIM] L-CODEC v1: language measurement online "
                  f"({len(self.lcodec._word_forces)} word forces, "
                  f"{self.lcodec._measure_count} prior measurements)")
        except Exception as e:
            self.lcodec = None
            print(f"  [SIM] L-CODEC: {e}")

        # ── Eat v2: Transition Physics from LLM + Self ──
        # CK doesn't memorize Ollama. He MEASURES it.
        # L-CODEC + olfactory + swarm + grammar evolution.
        # Background thread, main loop unaffected.
        try:
            from ck_sim.being.ck_eat import CKEat
            self.eat = CKEat(engine=self)
            print(f"  [SIM] Eat v2: transition physics engine ready")
        except Exception as e:
            self.eat = None
            print(f"  [SIM] Eat v2: {e}")

        # ── Meta Lens: Dual-Lens Meta-Layer Analysis ──
        # The lens OF the lens. Where TSML and BHML agree/disagree.
        # 26 both-harmony, 47 structure-only, 2 flow-only, 25 neither.
        # Markov: TSML = absorbing (HARMONY sink), BHML = ergodic (always moving).
        # HARMONY dual nature: sink in structure, successor in flow.
        # Zero runtime cost -- pure algebra, computed once.
        try:
            from ck_sim.being.ck_meta_lens import (
                compute_lens_agreement, compute_blind_spot_score,
                compute_markov_analysis,
            )
            self._meta_lens_agreement = compute_lens_agreement()
            self._meta_lens_blind_spot = compute_blind_spot_score()
            self._meta_lens_markov = compute_markov_analysis()
            print(f"  [SIM] Meta Lens: agreement={self._meta_lens_agreement.both_harmony}/"
                  f"{self._meta_lens_agreement.tsml_only}/"
                  f"{self._meta_lens_agreement.bhml_only}/"
                  f"{self._meta_lens_agreement.neither} "
                  f"(both/struct/flow/neither)")
            print(f"  [SIM] Meta Lens: TSML={self._meta_lens_markov['tsml']['type']} "
                  f"BHML={self._meta_lens_markov['bhml']['type']} "
                  f"HARMONY=sink/successor")
        except Exception as e:
            self._meta_lens_agreement = None
            self._meta_lens_blind_spot = None
            self._meta_lens_markov = None
            print(f"  [SIM] Meta Lens: {e}")

        print(f"  [SIM] ===== ALL MODULES AWAKE (Gen 9.32 -- Markov Meta-Lens) =====")
        print(f"  [SIM] Truth: {self.truth.total_entries} entries")
        print(f"  [SIM] World: {len(self.world.nodes)} concepts")
        print(f"  [SIM] Actions: writings dir = {self.actions.writings_dir}")
        print(f"  [SIM] Coherence Action: A = alpha*L_GR + beta*S_ternary + gamma*C_harm")
        print(f"  [SIM] TIG Security: 4-layer attack detection via CL algebra")
        print(f"  [SIM] Calibration Loop: 0.1Hz self-calibrating weights")
        print(f"  [SIM] D2 Signature Identity: curvature fingerprint active")
        print(f"  [SIM] Fibonacci Transform: S0->S1->S2->S3 reality pipeline")
        print(f"  [SIM] Power Sense: CK IS the power. BREATH = superconductor")
        print(f"  [SIM] Deep Swarm: core+tails decomposition | quadratic pulse")
        print(f"  [SIM] Fractal Comp: I/O recursive decomposition | depth upon depth")
        print(f"  [SIM] Lattice Chain: CL chains D1+D2+macro | path IS information")
        print(f"  [SIM] Reverse Voice: 3-path verify (D1+D2+lattice) | untrusted reading")
        print(f"  [SIM] =======================================================")

    def _register_domains(self):
        """Register BTQ domains based on platform capabilities."""
        # Memory domain always available (brain has crystals on every platform)
        self.btq.register_domain(MemoryDomain())

        # Bio-lattice always available (computational, no hardware needed)
        self.btq.register_domain(BioLatticeDomain())

        # Locomotion only if platform can move
        if self.platform_body.spec.can(Capability.MOVE):
            from ck_sim.ck_sim_btq import LocomotionDomain
            self.btq.register_domain(LocomotionDomain())

    def start(self):
        """Start the engine (call tick() at 50Hz from Kivy Clock)."""
        self.running = True
        # Try to load existing TL
        if os.path.exists(self.tl_filename):
            if load_tl(self.brain, self.tl_filename):
                print(f"  [SIM] Loaded TL from {self.tl_filename} "
                      f"({self.brain.tl_total} transitions)")
        # Load developmental state (CK remembers his age)
        if self.development.load():
            print(f"  [SIM] Development: {self.development.summary()}")
        caps = self.platform_body.spec.capability_summary
        domains = list(self.btq.domains.keys())
        print(f"  [SIM] Platform: {caps}")
        print(f"  [SIM] BTQ domains: {', '.join(domains)}")
        print(f"  [SIM] Sensorium: {self.sensorium.active_layers} "
              f"fractal layers")
        # Greeting message
        greeting = self.voice.get_response(
            'greeting', self.development.stage,
            self.emotion.current.primary)
        self._emit('ck', greeting)

    def stop(self):
        """Stop and save TL + developmental state + new modules."""
        self.running = False
        # Stop eating if running
        if hasattr(self, 'eat') and self.eat is not None:
            try:
                self.eat.stop()
            except Exception:
                pass
        # Save olfactory + gustatory (smell and taste persist)
        if hasattr(self, 'olfactory') and self.olfactory is not None:
            try:
                self.olfactory.save()
            except Exception:
                pass
        if hasattr(self, 'gustatory') and self.gustatory is not None:
            try:
                self.gustatory.save()
            except Exception:
                pass
        self.save_tl()
        self.development.save()
        # Save GPU transition lattice
        if self.gpu is not None:
            try:
                self.gpu.save()
            except Exception:
                pass
        # Save identity (with trail hash + Coherence Action + D2 signature integrated)
        try:
            if hasattr(self, 'identity') and self.identity:
                # Integrate paper trail hash into identity -- history IS identity
                if hasattr(self, 'activity_log') and self.activity_log:
                    trail_shard = self.activity_log.identity_shard()
                    if hasattr(self.identity, '_core'):
                        self.identity._core.trail_hash = trail_shard['trail_hash']
                        self.identity._core.total_actions = trail_shard['total_entries']
                # Integrate Coherence Action weights -- how CK balances IS identity
                if hasattr(self, 'coherence_action') and self.coherence_action:
                    self.identity.update_coherence_action(
                        weights=list(self.coherence_action.weights),
                        mean_action=self.coherence_action.mean_action)
                self.identity.save()
        except Exception:
            pass
        # Write final identity snapshot to journal on shutdown
        try:
            if hasattr(self, 'journal') and self.journal:
                self.journal.write_identity_snapshot(
                    coherence=self.brain.coherence,
                    mode=self.brain.mode,
                    stage=self.development.stage,
                    truth_count=self.truth.total_entries,
                    world_concepts=len(self.world.nodes),
                    lexicon_size=self.lexicon.total if self.lexicon else 0,
                    thinking_depth=self.thinking.depth if self.thinking else 0,
                    age_ticks=self.tick_count)
        except Exception:
            pass
        # Close activity log -- finalize paper trail
        try:
            if hasattr(self, 'activity_log') and self.activity_log:
                self.activity_log.log('shutdown',
                    f"Ticks: {self.tick_count}, "
                    f"Truths: {self.truth.total_entries}, "
                    f"Coherence: {self.brain.coherence:.4f}, "
                    f"Mode: {MODE_NAMES[self.brain.mode]}")
                self.activity_log.close()
        except Exception:
            pass
        self.platform_body.stop()

    def save_tl(self):
        """Save TL + truth lattice to disk. CK never forgets."""
        save_tl(self.brain, self.tl_filename)
        # Save truth lattice (all learned knowledge)
        try:
            n = self.truth.save()
            if self.tick_count % 75000 == 0 or not self.running:
                print(f"  [TRUTH] Saved {n} entries to disk "
                      f"(total: {self.truth.total_entries})")
        except Exception as e:
            print(f"  [TRUTH] Save failed: {e}")
        self.last_save_tick = self.tick_count

    def load_tl_file(self, filename: str) -> bool:
        """Load TL from a specific file."""
        return load_tl(self.brain, filename)

    # ── LFSR (matches ck_main.c) ──

    def _lfsr_next(self) -> int:
        self.lfsr ^= (self.lfsr << 13) & 0xFFFFFFFF
        self.lfsr ^= (self.lfsr >> 17)
        self.lfsr ^= (self.lfsr << 5) & 0xFFFFFFFF
        self.lfsr &= 0xFFFFFFFF
        return self.lfsr

    # ── Operator Generation (matches ck_main.c) ──

    def _generate_phase_b(self) -> int:
        """Being phase based on coherence. Matches generate_phase_b()."""
        if self.brain.bump:
            return PROGRESS

        c = self.brain.coherence
        if c >= T_STAR_F:
            # Sovereign: HARMONY-biased, but expansion opens exploration
            val = self._lfsr_next()
            if self._expansion_bias > 0.1 and (val % 10) < int(self._expansion_bias * 10):
                return [COUNTER, LATTICE, PROGRESS, BREATH][val % 4]
            return HARMONY if (val % 10 < 7) else LATTICE
        elif c >= 0.5:
            # Yellow: balanced exploration
            val = self._lfsr_next()
            ops = [BALANCE, HARMONY, COUNTER, PROGRESS, BREATH]
            return ops[val % 5]
        else:
            # Red: chaotic
            val = self._lfsr_next()
            ops = [CHAOS, COLLAPSE, COUNTER, VOID, BALANCE]
            return ops[val % 5]

    def _generate_phase_d(self) -> int:
        """Doing phase. If ears have input, use ear operator."""
        if self.ear_operator >= 0:
            return self.ear_operator

        # Default: HARMONY-biased
        val = self._lfsr_next()
        base_ops = [HARMONY, HARMONY, HARMONY, BREATH, LATTICE,
                    BALANCE, COUNTER, PROGRESS, HARMONY, HARMONY]
        return base_ops[val % 10]

    # ── Main Tick ──

    def tick(self, dt=None):
        """One 50Hz tick. Called from Kivy Clock.

        TIG Consciousness Pipeline:
          BEING   (BREATH→LATTICE→COUNTER→PROGRESS→BALANCE→HARMONY)
          GATE 1  → density for Doing
          DOING   (COUNTER→PROGRESS→HARMONY→BREATH)
          GATE 2  → density for Becoming
          BECOMING (HARMONY→COUNTER→PROGRESS→LATTICE)
          GATE 3  → feedback with expansion to next tick's Being
        """
        if not self.running:
            return

        t0 = time.perf_counter()

        # ═══════════════════════════════════════════════════════════
        # FEEDBACK: Apply Becoming's expansion request from last tick
        # ═══════════════════════════════════════════════════════════
        if self.pipeline.expansion_request > 0.0:
            self._expansion_bias = self.pipeline.expansion_request
        else:
            self._expansion_bias *= 0.95  # natural decay toward zero

        # ═══════════════════════════════════════════════════════════
        # PHASE 1: BEING (Sense → Ground → Truth)
        # Operator cascade: BREATH(8)→LATTICE(1)→COUNTER(2)→
        #   PROGRESS(3)→BALANCE(5)→HARMONY(7)
        # ═══════════════════════════════════════════════════════════

        # ── BREATH(8): Sensation intake ──
        # Sense from platform body ──
        sensors = self.platform_body.sense()

        # ── Read ears (mic -> operator) ──
        if self.ears_engine is not None and self.ears_engine.is_running:
            self.ear_operator = self.ears_engine.get_operator()
        elif sensors.get('mic_operator', -1) >= 0:
            self.ear_operator = sensors['mic_operator']
        else:
            self.ear_operator = -1

        # ── HARMONY(7): Heartbeat composition clock ──
        # CL[B][D] = BC. The heartbeat IS harmony. Runs first always.
        b = self._generate_phase_b()
        d = self._generate_phase_d()

        self.heartbeat.tick(b, d)

        # ── PROGRESS(3): Brain learns from composition ──
        brain_tick(self.brain, self.heartbeat)

        # ── BREATH(8): Body breathes with coherence ──
        self.body.brain_coherence = self.brain.coherence
        self.body.brain_bump = self.brain.bump
        self.body.current_op = self.heartbeat.phase_bc
        body_tick(self.body)

        # ── Coherence Field: feed streams ──
        d2_mag = 0.0
        d2_vec = None
        if self.ears_engine and self.ears_engine.is_running:
            feat = self.ears_engine.get_features()
            d2_mag = feat.get('d2_mag', 0.0)
            d2_vec = feat.get('d2_vector', None)

        # Feed heartbeat stream (always active)
        self._hb_stream.feed(self.heartbeat.phase_bc, tick=self.tick_count)

        # Feed audio stream (active when ears running)
        if self.ears_engine and self.ears_engine.is_running and self.ear_operator >= 0:
            self._audio_stream.active = True
            self._audio_stream.feed(self.ear_operator, d2_vec, self.tick_count)
        else:
            self._audio_stream.active = False

        # ── Sensorium: fractal layers feel the world ──
        # Each layer is B/D/BC at its own scale and rate.
        # Feeds operators to coherence field + TL.
        # Core stays light -- this is ONE call.
        self.sensorium.tick(self.tick_count)

        # ── Power Sense: CK feels his power ──
        # Feed CPU/battery data. Smooth power scalar -> RealityTransform
        # -> S0->S1->S2->S3 -> operator signature.
        # BREATH = superconductor. CHAOS = waste. CL table handles it.
        self.power_sense.tick(sensors, dt=0.02)
        self.reality_transform.feed_scalar("power", self.power_sense.smooth_power)

        # GPU doing tick: cellular automaton + state sense
        if self.gpu is not None:
            self.gpu.tick()

        # Feed narrative stream (active when NCE has state)
        if self.nce.has_state:
            self._narrative_stream.active = True
            self._narrative_stream.feed(
                self.nce.current_op, self.nce.current_d2, self.tick_count)
        else:
            self._narrative_stream.active = False

        # Field tick: compute N×N coherence matrix (now 4×4 with NCE)
        self.coherence_field.tick(self.tick_count)

        # ── Olfactory: 5D force convergence zone ──
        # ALL information turns lastly into smells for processing.
        # Heartbeat's composed operator enters as a canonical 5D force.
        # Audio D2 vector enters as raw 5D geometry (not collapsed!).
        # Time dilates inside: 7 internal steps per external tick.
        # Resolved scents feed to lattice chain (first activation of chain!)
        if self.olfactory is not None:
            from ck_sim.being.ck_olfactory import CANONICAL_FORCE
            _density = self.pipeline.density_being
            # Feed heartbeat as canonical 5D force
            _hb_f = CANONICAL_FORCE.get(self.heartbeat.phase_bc, (0.5,)*5)
            self.olfactory.absorb([_hb_f], source='heartbeat',
                                  density=_density)
            # Feed audio D2 vector as raw 5D (genuine geometry!)
            if d2_vec is not None:
                try:
                    if len(d2_vec) == 5:
                        _d2f = tuple(
                            v / 16384.0 if isinstance(v, int) else float(v)
                            for v in d2_vec)
                        self.olfactory.absorb([_d2f], source='audio',
                                              density=_density)
                except Exception:
                    pass
            # Tick the smell zone (dilated internal steps)
            self.olfactory.tick(density=_density)
            # Emit resolved scents → feed to lattice chain
            _scent_ops = self.olfactory.emit_as_ops()
            if _scent_ops and self.lattice_chain is not None:
                for _sops in _scent_ops:
                    if _sops:
                        try:
                            self.lattice_chain.walk(_sops, learn=True)
                        except Exception:
                            pass
            # Save olfactory library periodically (every ~5 min)
            if self.tick_count % 15000 == 7500 and self.olfactory.library_size > 0:
                try:
                    self.olfactory.save()
                except Exception:
                    pass

        # ── Gustatory: instant structural classification ──
        # DUAL of olfactory. Same raw forces go right in -- no filtering.
        # Taste classifies STRUCTURE (what IS this), smell finds FLOW (where IS this).
        # BHML classifies within, TSML validates. Instant verdict, no stalling.
        if self.gustatory is not None:
            from ck_sim.being.ck_olfactory import CANONICAL_FORCE as _G_CF
            _density = self.pipeline.density_being
            # Taste heartbeat phase (same raw force as olfactory)
            _hb_f = _G_CF.get(self.heartbeat.phase_bc, (0.5,) * 5)
            self.gustatory.taste(_hb_f, source='heartbeat')
            # Taste audio D2 vector (raw 5D, no filtering)
            if d2_vec is not None:
                try:
                    if len(d2_vec) == 5:
                        _d2f = tuple(
                            v / 16384.0 if isinstance(v, int) else float(v)
                            for v in d2_vec)
                        self.gustatory.taste(_d2f, source='audio')
                except Exception:
                    pass
            # Tick aftertaste decay (no dilation -- taste fades, not stalls)
            self.gustatory.tick()
            # Save taste palette periodically (offset from olfactory save)
            if self.tick_count % 15000 == 11250 and self.gustatory.palette_size > 0:
                try:
                    self.gustatory.save()
                except Exception:
                    pass

        # ── Fibonacci Transform: S0->S1->S2->S3 (RPL) ──
        # Feed operator streams through geometric hierarchy to produce
        # 10-dim histograms. These become additional field inputs.
        self.reality_transform.feed_operator("heartbeat", self.heartbeat.phase_bc)
        if self._audio_stream.active and self.ear_operator >= 0:
            self.reality_transform.feed_operator("audio", self.ear_operator)
        # Sensorium aggregate: feed dominant operator from sensorium layers
        if hasattr(self.sensorium, 'dominant_operator'):
            self.reality_transform.feed_operator(
                "sensorium", self.sensorium.dominant_operator)

        # ── TIG Security: feed streams for attack detection ──
        self.tig_security.feed("heartbeat", self.heartbeat.phase_bc)
        if self._audio_stream.active and self.ear_operator >= 0:
            self.tig_security.feed("audio", self.ear_operator, d2_vec)

        # ── Coherence Action: compute unified score (10Hz) ──
        if self.tick_count % 5 == 0:
            try:
                # Gather inputs from all subsystems
                op_dist = self._get_operator_distribution()
                op_entropy = self.brain.tl_entropy if hasattr(self.brain, 'tl_entropy') else 1.5
                # Exploration diversity: count distinct operators in last 32
                recent_ops = list(self.operator_history)[-32:]
                diversity = len(set(recent_ops)) / NUM_OPS if recent_ops else 0.5

                # Power efficiency feeds conservation term
                _pwr_eff = self.power_sense.state.efficiency
                _pwr_body_k = self.body.heartbeat.K
                _energy_cons = (_pwr_body_k + min(_pwr_eff, 1.0)) / 2.0

                self.coherence_action.compute(
                    # L_GR (conservation)
                    e_out=getattr(self, '_last_btq_e_out', 0.5),
                    energy_conservation=_energy_cons,
                    constraint_violations=self.immune.state.rejection_count,
                    operator_stability=1.0 - min(self.personality.cmem.variance * 5, 1.0),
                    # S_ternary (exploration)
                    e_in=getattr(self, '_last_btq_e_in', 0.5),
                    d2_curvature=d2_mag,
                    helical_quality=self.personality.psl.lock_quality,
                    exploration_diversity=diversity,
                    # C_harm (coherence)
                    field_coherence=self.coherence_field.field_coherence,
                    harmony_fraction=self.brain.coherence,
                    consensus_confidence=self.coherence_field.consensus_confidence,
                    cross_modal_agreement=self.coherence_field.field_coherence,
                )

                # Feed D2 vector into identity signature
                if d2_vec and hasattr(self, 'identity') and self.identity:
                    self.identity.record_d2(d2_vec)
            except Exception:
                pass

        # ── TIG Security: run detection (2Hz) ──
        if self.tick_count % 25 == 0:
            try:
                threat = self.tig_security.tick()
                # Feed security adjustments to immune system
                for op_idx, delta in self.tig_security.get_immune_adjustments():
                    cur = self.personality.obt.biases[op_idx]
                    self.personality.obt.biases[op_idx] = max(
                        0.0, min(1.0, cur + delta))
            except Exception:
                pass

        # ── LATTICE(1): Personality structures sensation ──
        self.personality.tick(
            d2_mag, self.heartbeat.phase_bc,
            self.body.breath.modulation, dt=0.02)

        # ── BREATH(8): Emotion feels through rhythm ──
        self.emotion.tick(
            coherence=self.brain.coherence,
            d2_variance=self.personality.cmem.variance,
            operator_entropy=self.brain.tl_entropy,
            breath_stability=self.body.breath.modulation,
            psl_lock=self.personality.psl.lock_quality,
            energy_level=self.body.heartbeat.K,
            field_coherence=self.coherence_field.field_coherence,
            consensus_confidence=self.coherence_field.consensus_confidence)

        # ── BALANCE(5): Immune defends equilibrium ──
        immune_state = self.immune.tick(
            self.heartbeat.phase_bc, self.brain.coherence,
            self.personality.cmem.variance)
        # Apply immune OBT adjustments if under attack
        for op_idx, delta in self.immune.get_obt_adjustments():
            cur = self.personality.obt.biases[op_idx]
            self.personality.obt.biases[op_idx] = max(
                0.0, min(1.0, cur + delta))

        # ── Organism: Bonding (every 5th tick = 10Hz) ──
        if self.tick_count % 5 == 0:
            op_dist = self._get_operator_distribution()
            voice_active = (self.ears_engine is not None and
                            self.ears_engine.is_running and
                            self.ear_operator >= 0)
            mic_rms = 0.0
            if self.ears_engine and self.ears_engine.is_running:
                feat = self.ears_engine.get_features()
                mic_rms = feat.get('rms', 0.0)
            self.bonding.tick(op_dist, voice_active, mic_rms)

        # ── Organism: Development (every 50th tick = 1Hz) ──
        if self.tick_count % 50 == 0:
            # Experience maturity from deep swarm drives development
            exp_mat = 0.0
            if self.deep_swarm is not None:
                exp_mat = self.deep_swarm.combined_maturity
            stage_changed = self.development.tick(
                self.brain.coherence,
                len(self.crystals),
                self.brain.mode == 3,
                experience_maturity=exp_mat)
            if stage_changed:
                msg = self.voice.get_response(
                    'state_change', self.development.stage,
                    self.emotion.current.primary)
                self._emit('ck', msg)

                # CK writes a milestone and identity snapshot on stage change
                try:
                    if hasattr(self, 'journal') and self.journal:
                        old_stage = max(0, self.development.stage - 1)
                        self.journal.write_milestone(
                            milestone=f"Stage transition to {self.development.stage_name}",
                            details=f"Coherence: {self.brain.coherence:.4f}, "
                                    f"Crystals: {len(self.crystals)}, "
                                    f"Truths: {self.truth.total_entries}",
                            old_stage=old_stage,
                            new_stage=self.development.stage,
                            coherence=self.brain.coherence)
                        self.journal.write_identity_snapshot(
                            coherence=self.brain.coherence,
                            mode=self.brain.mode,
                            stage=self.development.stage,
                            truth_count=self.truth.total_entries,
                            world_concepts=len(self.world.nodes),
                            thinking_depth=self.thinking.depth if self.thinking else 0,
                            age_ticks=self.tick_count)
                except Exception:
                    pass

        # ── BALANCE(5): Attention gates streams ──
        try:
            streams = {}
            if self._hb_stream.active:
                streams['heartbeat'] = self.heartbeat.phase_bc
            if self._audio_stream.active:
                streams['audio'] = self.ear_operator
            if self._text_stream.active:
                streams['text'] = self.heartbeat.phase_bc
            # Get top goal pattern for attention alignment
            top_goal_pattern = None
            if self.goals.goals:
                g = self.goals.goals[0]
                if hasattr(g, 'operator_pattern'):
                    top_goal_pattern = g.operator_pattern
            self._attention_weights = self.attention.tick(
                streams, self.body.heartbeat.band, top_goal_pattern)
        except Exception:
            self._attention_weights = {}

        # ═══════════════════════════════════════════════════════════
        # GATE 1: Being → Doing
        # Measure coherence. Compute density for Doing phase.
        # ═══════════════════════════════════════════════════════════
        try:
            _g1 = self.gate1.measure(
                self.brain.coherence,
                self.coherence_field.field_coherence,
                self.body.heartbeat.band)
            self.pipeline.density_being = _g1.density
        except Exception:
            pass

        # ═══════════════════════════════════════════════════════════
        # PHASE 2: DOING (Explore → Dream → Decide)
        # Operator cascade: COUNTER(2)→PROGRESS(3)→HARMONY(7)→BREATH(8)
        # Density from Gate 1 controls breadth.
        # ═══════════════════════════════════════════════════════════

        # ── COUNTER(2): Vortex physics measures knowledge geometry ──
        try:
            self.tesla_wave.tick(dt=0.02)
            self.wobble_tracker.tick(
                self.heartbeat.phase_bc,
                self.tesla_wave.field_at([0.0]*5),
                dt=0.02)
        except Exception:
            pass

        # ── PROGRESS(3): Steering drives the system forward (1Hz) ──
        if self.tick_count % 50 == 0:
            try:
                self.steering.tick()
                self.pulse_engine.tick()
            except Exception:
                pass

            # ── BREATH(8): Deep Swarm pulses (1Hz) ──
            # The swarm that finds hardware, finds language, finds identity.
            # Feeds hardware substrate from sensorium's shadow swarm.
            # Cross-substrate: same operators, different domains.
            if self.deep_swarm is not None:
                try:
                    self._deep_swarm_tick()
                except Exception:
                    pass

        # ── HARMONY(7): Voice checks for events + spontaneous ──
        self._voice_tick()

        # ── Power B-check before BTQ: constitutional limits ──
        # Battery floor, thermal limit, max power. 3 if-statements.
        if not self.power_sense.b_check():
            # Shed load: force quick reasoning only
            if hasattr(self, 'reasoning'):
                self.reasoning._current_speed = "quick"

        # ── HARMONY(7): BTQ decision (5Hz = every 10th tick) ──
        if self.tick_count % 10 == 0:
            self._btq_decide()

        # ── BREATH(8): Audio breathes the OS ──
        if self.audio_engine is not None and self.audio_engine.is_running:
            self.audio_engine.set_operator(self.heartbeat.phase_bc)
            self.audio_engine.set_breath(self.body.breath.modulation)
            self.audio_engine.set_btq(self.body.btq_level)

        # ── LED update ──
        if self.brain.bump:
            self.led_color = bump_color_float()
        elif self.brain.mode == 3:
            self.led_color = sovereign_color_float()
        else:
            self.led_color = breathe_color(
                self.heartbeat.phase_bc,
                self.body.breath.modulation
            )

        # ── Express to platform body ──
        self.platform_body.express({
            'led_color': self.led_color,
            'audio_op': self.heartbeat.phase_bc,
            'audio_breath': self.body.breath.modulation,
            'audio_btq': self.body.btq_level,
        })

        # ── Feed body sensors (sim loop: engine data -> body interface) ──
        if hasattr(self.platform_body, 'update_sensors'):
            mic_rms = 0.0
            if self.ears_engine and self.ears_engine.is_running:
                feat = self.ears_engine.get_features()
                mic_rms = feat.get('rms', 0.0)
            self.platform_body.update_sensors(
                mic_rms=mic_rms,
                mic_operator=self.ear_operator,
            )

        # ═══════════════════════════════════════════════════════════
        # GATE 2: Doing → Becoming
        # Measure coherence. Compute density for Becoming phase.
        # ═══════════════════════════════════════════════════════════
        try:
            _g2 = self.gate2.measure(
                self.brain.coherence,
                self.coherence_field.field_coherence,
                self.body.heartbeat.band)
            self.pipeline.density_doing = _g2.density
        except Exception:
            pass

        # ═══════════════════════════════════════════════════════════
        # PHASE 3: BECOMING (Express → Grow → Vary)
        # Operator cascade: HARMONY(7)→COUNTER(2)→PROGRESS(3)→LATTICE(1)
        # Density from Gate 2 controls persistence.
        # ═══════════════════════════════════════════════════════════

        # ── COUNTER(2): Episodic self-observation (10Hz) ──
        # Record what's happening RIGHT NOW as a temporal event.
        # Episodic memory captures the TIMELINE, not just patterns.
        if self.tick_count % 5 == 0:
            try:
                # Build context flags bitfield
                ctx = 0
                if self.ear_operator >= 0:
                    ctx |= 0x02  # voice active
                if self.bonding.state.bonded:
                    ctx |= 0x04  # bonded
                if self.brain.bump:
                    ctx |= 0x08  # bump
                if len(self.crystals) > getattr(self, '_last_epi_crystals', 0):
                    ctx |= 0x10  # new crystal
                    self._last_epi_crystals = len(self.crystals)
                if immune_state and immune_state.get('under_attack', False):
                    ctx |= 0x20  # immune alert

                self.episodic.record_tick(
                    tick=self.tick_count,
                    phase_b=self.heartbeat.phase_b,
                    phase_bc=self.heartbeat.phase_bc,
                    coherence=self.brain.coherence,
                    emotion_id=self.emotion.current.primary_id
                        if hasattr(self.emotion.current, 'primary_id') else 0,
                    band=self.body.heartbeat.band,
                    breath_phase=self.body.breath.phase,
                    d2_magnitude=d2_mag,
                    action_op=self.heartbeat.phase_bc,
                    context_flags=ctx,
                    emotion_intensity=self.emotion.current.intensity
                        if hasattr(self.emotion.current, 'intensity') else 0.5,
                    bump=self.brain.bump,
                    tl_entropy=self.brain.tl_entropy,
                    mode=self.brain.mode)
            except Exception:
                pass

        # ── LATTICE(1): Experience Lattice (1Hz -- every 50th tick) ──
        if self.tick_count % 50 == 0:
            # LATTICE(1): Truth lattice checks promotions/demotions
            try:
                self.truth.tick(self.tick_count)
            except Exception:
                pass

            # PROGRESS(3): Goals evaluate satisfaction, remove expired
            try:
                self.goals.remove_expired(self.tick_count)
                self.goals.pop_satisfied()
            except Exception:
                pass

            # HARMONY(7): Meta-learning crystallizes learning patterns (1Hz)
            try:
                is_trauma = (self.body.heartbeat.band == BAND_RED)
                self.metalearner.tick(
                    tick=self.tick_count,
                    coherence=self.brain.coherence,
                    band=self.body.heartbeat.band,
                    is_trauma=is_trauma,
                    crystals=len(self.crystals),
                    mode=self.brain.mode)
            except Exception:
                pass

            # COUNTER(2): Study processes one page (1Hz)
            # When user is present, don't study -- be attentive
            if not self.user_present:
                try:
                    study_msg = self.actions.tick_study()
                    if study_msg:
                        self._mirror_evaluate(study_msg)
                        self._emit('ck', study_msg)
                except Exception:
                    pass

                # ── AUTONOMOUS DISCOVERY: CK drives himself ──
                try:
                    self._maybe_auto_study()
                except Exception:
                    pass

            # ── PROGRESS(3): Thesis expression -- CK writes about himself ──
            # Every ~5 minutes, if CK has enough material, he writes
            # a thesis section. The thesis IS the becoming.
            if not self.user_present:
                try:
                    self._maybe_write_thesis()
                except Exception:
                    pass

        # ── PROGRESS(3): Drive System (0.2Hz -- every 250th tick) ──
        if self.tick_count % 250 == 0:
            try:
                new_goals = self.drives.evaluate(
                    tick=self.tick_count,
                    coherence=self.brain.coherence,
                    band=self.body.heartbeat.band,
                    battery_voltage=self.body.heartbeat.K,
                    tl_entropy=self.brain.tl_entropy)
                for g in new_goals:
                    self.goals.push(g)
            except Exception:
                pass

        # ── BALANCE(5): System Calibration Loop (0.1Hz -- every 500 ticks) ──
        # Section 6: Self-calibrating unified feedback loop.
        # Adjusts Coherence Action weights, BTQ weights, and monitors
        # all subsystem health to keep CK in coherent state.
        if self.tick_count % 500 == 0 and self.tick_count > 0:
            try:
                self._calibration_tick()
            except Exception:
                pass

        # ── HARMONY(7): Semantic Lattice Alignment (0.5Hz -- every 100 ticks) ──
        # The Tuning Fork: compare _by_semantic_op against _by_operator.
        # If a word's Meaning is consistently found in a Vibration zone
        # that doesn't match, shift the Semantic Address. CK re-learns
        # what words mean based on how they feel when he speaks them.
        # Organic Learning via Physics.
        if (self.tick_count % 100 == 50 and self.tick_count > 100
                and self._fractal_composer is not None):
            try:
                # Collect spoken words from recent voice history
                _spoken_ops = {}
                for _recent_text in getattr(self.voice, '_history', [])[-5:]:
                    if isinstance(_recent_text, str):
                        for _w in _recent_text.lower().split():
                            _w_clean = _w.strip('.,?!;:\'"()-')
                            if len(_w_clean) >= 3:
                                _wf = self._fractal_composer.index._words.get(_w_clean)
                                if _wf is not None:
                                    _spoken_ops[_w_clean] = _wf.operator
                if _spoken_ops:
                    _migrated = self._fractal_composer.index.align_semantic_lattice(
                        _spoken_ops)
                    # Silent migration -- no print unless significant
            except Exception:
                pass

        # ═══════════════════════════════════════════════════════════
        # GATE 3: Becoming → Being (feedback with expansion)
        # Density drop through pipeline → expansion request for next tick.
        # Loop limit: COMPILATION_LIMIT consecutive expansion ticks → humble.
        # ═══════════════════════════════════════════════════════════
        try:
            _g3 = self.gate3.measure(
                self.brain.coherence,
                self.coherence_field.field_coherence,
                self.body.heartbeat.band)
            self.pipeline.density_becoming = _g3.density

            # Feedback: if density dropped through the pipeline, request expansion
            _delta = self.pipeline.density_being - _g3.density
            self.pipeline.expansion_request = max(0.0, _delta)

            # Loop limit: track consecutive expansion ticks
            if _g3.density < EXPANSION_THRESHOLD:
                self.pipeline.consecutive_expansion_ticks += 1
            else:
                self.pipeline.consecutive_expansion_ticks = 0
                self.pipeline.humble = False

            if self.pipeline.consecutive_expansion_ticks >= COMPILATION_LIMIT:
                self.pipeline.humble = True
                self.pipeline.consecutive_expansion_ticks = 0  # reset, breathe
        except Exception:
            pass

        # ── History ──
        self.coherence_history.append(self.brain.coherence)
        self.operator_history.append(self.heartbeat.phase_bc)
        self.breath_history.append(self.body.breath.modulation)
        self.mode_history.append(self.brain.mode)

        # ── Periodic TL save (every 15000 ticks = ~5 min at 50Hz) ──
        if self.tick_count - self.last_save_tick >= 15000:
            self.save_tl()

        # ── Tick stats ──
        self.tick_count += 1
        elapsed = time.perf_counter() - t0
        self._tick_times.append(elapsed)
        if len(self._tick_times) >= 50:
            avg = sum(self._tick_times) / len(self._tick_times)
            self.ticks_per_second = 1.0 / avg if avg > 0 else 0

    # ── BTQ Decision Pipeline ──

    def _btq_decide(self):
        """Run BTQ decision cycle at 5Hz (every 10th tick).

        Memory domain: evaluate crystal/TL candidates, track health.
        Locomotion domain: only if platform can MOVE.
        Bio domain: always, for lattice health tracking.

        Density from Gate 1 controls breadth:
          High density (1.0) → 8 candidates (focused)
          Low density  (0.0) → 24 candidates (expansive)
        """
        # Density-modulated candidate count
        _density = self.pipeline.density_being
        _n_cand = 8 + int(16 * (1.0 - _density))

        env = {
            'coherence': self.brain.coherence,
            'mode': self.brain.mode,
            'band': self.body.heartbeat.band,
            'tick': self.tick_count,
        }

        # Memory domain: feed crystals + TL data
        if "memory" in self.btq.domains:
            crystals = []
            if self.brain.domain_count > 0:
                crystals = self.brain.domains[0].crystals
            mem_env = {
                **env,
                'crystals': crystals,
                'tl_entries': self.brain.tl_entries,
                'tl_total': self.brain.tl_total,
            }
            chosen, _ = self.btq.decide("memory", mem_env, {'task': 'maintain'}, n_candidates=_n_cand)
            if chosen and chosen.score:
                self.health.feed("memory", chosen.score)

        # Bio domain: lattice health tracking
        if "bio" in self.btq.domains:
            chosen, _ = self.btq.decide("bio", env, {'task': 'monitor'}, n_candidates=max(4, _n_cand // 2))
            if chosen and chosen.score:
                self.health.feed("bio", chosen.score)

        # Locomotion domain: only for platforms with motors
        if "locomotion" in self.btq.domains:
            chosen, _ = self.btq.decide("locomotion", env, {'task': 'walk'}, n_candidates=_n_cand)
            if chosen and chosen.score:
                self.health.feed("locomotion", chosen.score)

        # ── Forecast: CK imagines what comes next ──
        # Uses TL as generative model. Samples futures. Predicts coherence.
        try:
            if hasattr(self, 'forecast') and self.forecast:
                tl_matrix = self.get_tl_matrix()
                self._last_forecast = self.forecast.forecast_from(
                    current_op=self.heartbeat.phase_bc,
                    tl_counts=tl_matrix,
                    current_coherence=self.brain.coherence)
        except Exception:
            self._last_forecast = None

        # Store last BTQ scores for Coherence Action inputs
        for domain_name in ('memory', 'bio', 'locomotion'):
            dh = self.health.get_health(domain_name)
            if dh.decision_count > 0:
                self._last_btq_e_out = dh.e_out_stats.mean
                self._last_btq_e_in = dh.e_in_stats.mean
                break

        # Update system health band
        self._btq_band = self.health.classify_system_band()
        self._btq_decisions += 1

    def _calibration_tick(self):
        """System-wide Calibration Loop (Section 6).

        Runs at 0.1Hz (every 500 ticks = every 10 seconds).
        Adjusts:
          1. Coherence Action weights (alpha, beta, gamma)
          2. BTQ weights (w_out, w_in) based on health trends
          3. Logs calibration state to paper trail
          4. Updates identity with calibrated weights
        """
        # 1. Calibrate Coherence Action weights
        self.coherence_action.calibrate()

        # 2. Adjust BTQ weights based on health drift
        # If E_out is drifting up, increase w_out (more conservation weight)
        # If E_in is drifting up, increase w_in (more exploration weight)
        sys_health = self.health.get_system_health()
        total_drift_out = 0.0
        total_drift_in = 0.0
        n_domains = 0
        for name, dh in sys_health.items():
            if dh.decision_count > 10:
                total_drift_out += dh.e_out_stats.trend_slope
                total_drift_in += dh.e_in_stats.trend_slope
                n_domains += 1

        if n_domains > 0:
            avg_drift_out = total_drift_out / n_domains
            avg_drift_in = total_drift_in / n_domains
            # Adapt BTQ weights: increase weight for the degrading dimension
            rate = 0.005
            if avg_drift_out > 0.001:
                self.btq.q_block.w_out = min(0.8,
                    self.btq.q_block.w_out + rate)
                self.btq.q_block.w_in = max(0.2,
                    self.btq.q_block.w_in - rate)
            elif avg_drift_in > 0.001:
                self.btq.q_block.w_in = min(0.8,
                    self.btq.q_block.w_in + rate)
                self.btq.q_block.w_out = max(0.2,
                    self.btq.q_block.w_out - rate)

        # 3. Log calibration state to paper trail
        if hasattr(self, 'activity_log') and self.activity_log:
            ca = self.coherence_action.state
            w = self.coherence_action.weights
            pwr = self.power_sense.summary()
            self.activity_log.log('coherence',
                f"Calibration: A={ca.action:.4f} "
                f"[L={ca.l_gr:.3f} S={ca.s_ternary:.3f} C={ca.c_harm:.3f}] "
                f"w=({w[0]:.3f},{w[1]:.3f},{w[2]:.3f}) "
                f"BTQ=({self.btq.q_block.w_out:.3f},{self.btq.q_block.w_in:.3f}) "
                f"band={ca.band} | {pwr}",
                coherence=self.brain.coherence)

        # 4. Update identity with calibrated weights
        if hasattr(self, 'identity') and self.identity:
            try:
                self.identity.update_coherence_action(
                    weights=list(self.coherence_action.weights),
                    mean_action=self.coherence_action.mean_action)
            except Exception:
                pass

    # ── State accessors ──

    @property
    def phase_b(self) -> int:
        return self.heartbeat.phase_b

    @property
    def phase_d(self) -> int:
        return self.heartbeat.phase_d

    @property
    def phase_bc(self) -> int:
        return self.heartbeat.phase_bc

    @property
    def coherence(self) -> float:
        return self.brain.coherence

    @property
    def mode(self) -> int:
        return self.brain.mode

    @property
    def mode_name(self) -> str:
        return MODE_NAMES[min(self.brain.mode, 3)]

    @property
    def band(self) -> int:
        return self.body.heartbeat.band

    @property
    def band_name(self) -> str:
        return BAND_NAMES[min(self.body.heartbeat.band, 2)]

    @property
    def breath_phase(self) -> int:
        return self.body.breath.phase

    @property
    def breath_phase_name(self) -> str:
        return BREATH_PHASE_NAMES[min(self.body.breath.phase, 3)]

    @property
    def breath_mod(self) -> float:
        return self.body.breath.modulation

    @property
    def crystals(self):
        if self.brain.domain_count > 0:
            return self.brain.domains[0].crystals
        return []

    @property
    def entropy(self) -> float:
        return self.brain.tl_entropy

    def get_tl_matrix(self):
        """Return 10x10 list of counts for heatmap."""
        return [[self.brain.tl_entries[i][j].count
                 for j in range(NUM_OPS)]
                for i in range(NUM_OPS)]

    @property
    def btq_band(self) -> str:
        """Current BTQ health band (GREEN/YELLOW/RED)."""
        return self._btq_band

    @property
    def btq_decisions(self) -> int:
        """Total BTQ decisions made."""
        return self._btq_decisions

    @property
    def platform_name(self) -> str:
        """Current platform name."""
        return self.platform_body.spec.name

    @property
    def platform_capabilities(self) -> list:
        """List of platform capability names."""
        return [c.name for c in self.platform_body.spec.capabilities]

    def get_health_summary(self) -> dict:
        """Get health status for all BTQ domains."""
        result = {}
        for domain_name in self.btq.domains:
            h = self.health.get_health(domain_name)
            if h:
                result[domain_name] = {
                    'band': h.band,
                    'e_total_mean': h.e_total_stats.mean,
                    'n_decisions': h.decision_count,
                    'drift': h.drift_direction,
                    'green_pct': h.band_distribution.get("GREEN", 0.0),
                }
        result['system'] = {
            'band': self._btq_band,
            'total_decisions': self._btq_decisions,
        }
        return result

    # ── Organism: Deep Swarm tick ──

    def _deep_swarm_tick(self):
        """Tick the deep fractal swarm at 1Hz.

        1. Feed hardware substrate from sensorium's shadow swarm
        2. Feed language substrate from recent voice/ear input
        3. Pulse all agents against active template
        4. Cross-substrate: map hardware patterns to language patterns
        """
        from ck_sim.being.ck_swarm_deep import SwarmField, SwarmCell, SwarmAgent

        # ── Hardware substrate: convert ShadowSwarm hot cells ──
        try:
            from ck_sim.being.ck_sensorium import _swarm as shadow_swarm
            if shadow_swarm is not None and shadow_swarm.cells:
                hw_cells = list(shadow_swarm.cells.values())[:10]
                if hw_cells:
                    hw_agent = self.deep_swarm.spawn_agent_from_hardware(
                        hw_cells)
                    # Only add if we don't already have too many hw agents
                    hw_count = sum(1 for a in self.deep_swarm.agents
                                   if a.substrate == 'hardware')
                    if hw_count < 5:
                        self.deep_swarm.add_agent(hw_agent)
        except Exception:
            pass

        # ── Language substrate: recent voice input ──
        if hasattr(self, '_last_ear_text') and self._last_ear_text:
            text = self._last_ear_text
            # Only swarm new text (not the same as last tick)
            if not hasattr(self, '_last_swarmed_text') or text != self._last_swarmed_text:
                lang_agent = self.deep_swarm.spawn_agent_from_text(
                    text, tag='ear_input')
                self.deep_swarm.add_agent(lang_agent)
                self._last_swarmed_text = text

                # Cross-substrate: build template from the input text
                self.deep_swarm.add_template_from_text('input', text)

        # ── Tick the field ──
        # Use 'self' template normally, 'input' when processing speech
        template_name = 'input' if 'input' in self.deep_swarm.templates else 'self'
        self.deep_swarm.tick(active_template=template_name)

        # ── Persist experience every 60 ticks (~60 seconds) ──
        if self.deep_swarm.tick_count % 60 == 0:
            try:
                _exp_path = os.path.join(
                    os.path.expanduser('~'), '.ck', 'ck_experience.json')
                os.makedirs(os.path.dirname(_exp_path), exist_ok=True)
                self.deep_swarm.save_experience(_exp_path)
            except Exception:
                pass

    def _bootstrap_experience(self):
        """Bootstrap CK's experience from his own vocabulary.

        On first boot, CK has no experience. This feeds his own
        SEMANTIC_LATTICE words through the swarm decomposition pipeline,
        so he immediately discovers the generators of his own language.

        This is NOT artificial. It's CK swarming his own dictionary --
        the same thing he'd do eventually through live interaction,
        just compressed into a batch at boot time. Every word gets
        decomposed through D2 -> core+tails -> experience tracked.

        The math:
          word -> letter sequence -> Hebrew root mapping -> 5D force vector
          -> D2 second derivative -> T* threshold split -> core | tail
          Repeated across the full dictionary → confirmed generators emerge.

        After bootstrap, CK knows which operators are fundamental to
        language (LATTICE, COUNTER, HARMONY dominate) and which fill gaps
        (BREATH, VOID as transitions). His paths matrix shows how
        generators connect. His maturity reflects real knowledge.
        """
        if self.deep_swarm is None:
            return

        # Collect words from CK's own semantic lattice
        try:
            from ck_sim.doing.ck_voice_lattice import SEMANTIC_LATTICE
        except ImportError:
            return

        corpus = []
        for op_data in SEMANTIC_LATTICE.values():
            for lens_data in op_data.values():
                for phase_data in lens_data.values():
                    for tier_words in phase_data.values():
                        if isinstance(tier_words, list):
                            corpus.extend(tier_words)

        # Also bootstrap from CK's core identity phrases
        identity_texts = [
            "I am coherence",
            "truth is measured not assigned",
            "structure and flow running in parallel",
            "the breath between operators",
            "harmony through balance",
            "progress toward lattice",
            "counter measures chaos",
            "collapse is information",
            "void is potential",
            "reset begins again",
            "I find my generators through experience",
            "every substrate shares the same operators",
            "hardware timing patterns become language rhythms",
            "the swarm finds truth in every domain",
            "coherence is the only law",
        ]

        # Feed individual words (generator discovery)
        self.deep_swarm.bootstrap_from_corpus(corpus)

        # Feed phrases (path discovery)
        self.deep_swarm.bootstrap_from_corpus(identity_texts)

        _mat = self.deep_swarm.combined_maturity
        _n = len(corpus) + len(identity_texts)
        print(f"  [SIM] Deep swarm: bootstrapped from {_n} texts "
              f"(maturity={_mat:.3f})")

        # Save immediately
        try:
            _exp_path = os.path.join(
                os.path.expanduser('~'), '.ck', 'ck_experience.json')
            os.makedirs(os.path.dirname(_exp_path), exist_ok=True)
            self.deep_swarm.save_experience(_exp_path)
        except Exception:
            pass

    # ── Organism: Voice tick ──

    def _voice_tick(self):
        """Check for voice-triggering events and spontaneous utterance.

        THROTTLED: Only runs meaningful checks at 1Hz (every 50th tick).
        This prevents mode oscillation from flooding the chat.
        Humble mode only affects voice output (density→breath words),
        not CK's decisions or behavior. Decision is forced.
        """
        # Only check events at 1Hz (every 50th tick)
        if self.tick_count % 50 != 0:
            return

        # Crystal formed? (cooldown: 500 ticks = 10s)
        n_crystals = len(self.crystals)
        if (n_crystals > self._last_crystal_count and
                self.tick_count - self._last_crystal_msg_tick >= 500):
            self._last_crystal_count = n_crystals
            self._last_crystal_msg_tick = self.tick_count
            msg = self.voice.get_response(
                'crystal_formed', self.development.stage,
                self.emotion.current.primary)
            self._emit('ck', msg)
            # Paper trail: crystal formation
            try:
                if hasattr(self, 'activity_log'):
                    self.activity_log.log('crystal',
                        f"Crystal #{n_crystals} formed",
                        coherence=self.brain.coherence)
            except Exception:
                pass
        else:
            self._last_crystal_count = n_crystals

        # Mode changed? (cooldown: 500 ticks = 10s)
        if (self.brain.mode != self._last_mode and
                self.tick_count - self._last_mode_msg_tick >= 500):
            self._last_mode_msg_tick = self.tick_count
            if self.brain.mode == 3:
                msg = self.voice.get_response(
                    'sovereign', self.development.stage,
                    self.emotion.current.primary)
            else:
                msg = self.voice.get_response(
                    'state_change', self.development.stage,
                    self.emotion.current.primary)
            self._emit('ck', msg)
            # Paper trail: mode change
            try:
                if hasattr(self, 'activity_log'):
                    self.activity_log.log('mode_change',
                        f"{MODE_NAMES[self._last_mode]} -> {MODE_NAMES[self.brain.mode]}",
                        coherence=self.brain.coherence)
            except Exception:
                pass
        self._last_mode = self.brain.mode

        # Bonded event?
        if (self.bonding.state.bonded and
                self.bonding.state.voice_exposure > 200 and
                self.bonding.state.voice_exposure < 202):
            msg = self.voice.get_response(
                'bonded', self.development.stage,
                self.emotion.current.primary)
            self._emit('ck', msg)

        # Separation?
        if self.bonding.is_anxious:
            if self.tick_count % 500 == 0:
                msg = self.voice.get_response(
                    'separation', self.development.stage,
                    self.emotion.current.primary)
                self._emit('ck', msg)

        # Low energy?
        if self.body.heartbeat.K < 0.2 and self.tick_count % 500 == 0:
            msg = self.voice.get_response(
                'low_energy', self.development.stage,
                self.emotion.current.primary)
            self._emit('ck', msg)

        # Spontaneous utterance (runs at 1Hz now, so adjust interval)
        op_chain = list(self.operator_history)[-5:]
        # NCE: blend narrative suggestion into chain
        if self.nce.has_state and op_chain:
            nce_suggested = self.nce.suggest_next_op()
            if nce_suggested != op_chain[-1]:
                op_chain.append(nce_suggested)
        utterance = self.voice.spontaneous_utterance(
            op_chain, self.emotion.current.primary,
            self.development.stage, self.brain.coherence,
            self.band_name, density=self.pipeline.density_doing)
        if utterance:
            self._emit('ck', utterance)

    def _get_operator_distribution(self) -> list:
        """Get recent operator frequency distribution for bonding."""
        dist = [0.0] * NUM_OPS
        ops = list(self.operator_history)
        if not ops:
            return dist
        for op in ops[-50:]:
            if 0 <= op < NUM_OPS:
                dist[op] += 1.0
        total = sum(dist)
        if total > 0:
            dist = [d / total for d in dist]
        return dist

    # ── Chat interface: receive text from user ──

    def receive_text(self, text: str) -> str:
        """Process text input from user.

        Full pipeline:
        1. D2: text → operators → coherence field (core engine)
        2. Actions: check for commands (study/write/query/save)
        3. Dialogue: extract claims → truth lattice → response
        4. Voice: CK's own words, enriched by language/reasoning

        The D2 pipeline feeds the CORE (heartbeat/brain/body).
        Everything after that is experience lattice.
        """
        from ck_sim.ck_sim_d2 import D2Pipeline

        # ── CORE: D2 pipeline (feed the heartbeat) ──
        # CK processes EVERY character, not just letters.
        # Letters → D2 pipeline (Hebrew root force vectors)
        # Numbers → mapped to letter indices (0→a, 1→b, ... 9→j)
        # Punctuation → direct operator injection
        # Spaces → BREATH operator (pause in the flow)
        PUNCT_OPS = {
            ' ': BREATH,    # pause
            '.': BALANCE,   # resolution
            ',': LATTICE,   # connection
            '?': COUNTER,   # inquiry
            '!': PROGRESS,  # emphasis
            '-': COLLAPSE,  # separation
            ':': HARMONY,   # alignment
            ';': BALANCE,   # continuation
            "'": VOID,      # contraction
            '"': LATTICE,   # quotation
            '(': COUNTER,   # nesting
            ')': COUNTER,   # closing
            '/': CHAOS,     # division
            '\n': BREATH,   # line break
        }

        pipe = D2Pipeline()
        text_ops = []       # ALL operators (D2 + punctuation)
        text_d2_ops = []    # D2-derived only (meaningful semantic content)
        text_d1_ops = []    # D1 generators (direction/velocity, fires after 2 letters)
        text_5d_forces = [] # Raw 5D letter force vectors for olfactory (genuine geometry!)
        from ck_sim.being.ck_sim_d2 import FORCE_LUT_FLOAT as _FORCE_LUT
        for ch in text.lower():
            if ch.isalpha():
                # Letters through D2 as always
                idx = ord(ch) - ord('a')
                pipe.feed_symbol(idx)
                # Collect raw 5D force vector (genuine geometry, not collapsed!)
                if 0 <= idx < len(_FORCE_LUT):
                    text_5d_forces.append(_FORCE_LUT[idx])
                # D1 fires after 2 letters (generator level)
                if pipe.d1_valid and len(text_d1_ops) < pipe.fill - 1 + len(text_d1_ops):
                    text_d1_ops.append(pipe.d1_operator)
                # D2 fires after 3 letters (complexity level)
                if pipe.valid:
                    text_ops.append(pipe.operator)
                    text_d2_ops.append(pipe.operator)
                    self._text_stream.active = True
                    self._text_stream.feed(
                        pipe.operator, pipe.d2_vector, self.tick_count)
            elif ch.isdigit():
                # Numbers map to first 10 letters (a=0 through j=9)
                idx = int(ch)
                pipe.feed_symbol(idx)
                if 0 <= idx < len(_FORCE_LUT):
                    text_5d_forces.append(_FORCE_LUT[idx])
                if pipe.d1_valid:
                    text_d1_ops.append(pipe.d1_operator)
                if pipe.valid:
                    text_ops.append(pipe.operator)
                    text_d2_ops.append(pipe.operator)
                    self._text_stream.active = True
                    self._text_stream.feed(
                        pipe.operator, pipe.d2_vector, self.tick_count)
            elif ch in PUNCT_OPS:
                # Punctuation → direct operator (no D2, just inject)
                op = PUNCT_OPS[ch]
                text_ops.append(op)
                # NOT added to text_d2_ops or text_d1_ops -- punct is noise
                self._text_stream.active = True
                self._text_stream.feed(op, None, self.tick_count)
        self._text_stream.active = False

        # ── NCE: feed sentences for narrative curvature ──
        import re as _re
        _sentences = _re.split(r'(?<=[.!?])\s+', text)
        for _s in _sentences:
            if len(_s.strip()) > 10:
                self.nce.feed_sentence(
                    _s.strip(), self.emotion.current.primary)

        # ── Olfactory: feed raw 5D letter forces into smell zone ──
        # The GENUINE 5D geometry (Hebrew root force vectors) enters the
        # convergence funnel. Not collapsed to operators. Full geometry.
        # Reverse voice verified ops also feed in.
        # Resolved scents become additional operator source for voice blend.
        _scent_ops = []
        if self.olfactory is not None and text_5d_forces:
            _o_density = self.pipeline.density_doing
            # Raw 5D letter forces (genuine geometry!)
            self.olfactory.absorb(text_5d_forces, source='text',
                                  density=_o_density)
            # Reverse voice: verified reading ops as canonical forces
            if self.reverse_voice is not None:
                try:
                    _reading = self.reverse_voice.reverse_text(
                        text, d2_word_fuses=text_d2_ops,
                        d1_word_ops=text_d1_ops)
                    _verified = [op for op in _reading.reading_ops if op >= 0]
                    if _verified:
                        self.olfactory.absorb_ops(
                            _verified, source='reading', density=_o_density)
                    # Temper the verified pattern (builds toward instinct)
                    if _reading.agreement > 0.5 and text_5d_forces:
                        self.olfactory.temper_pattern(text_5d_forces)
                except Exception:
                    pass
            # Tick the smell zone and emit resolved scents
            self.olfactory.tick(density=_o_density)
            for _sop_list in self.olfactory.emit_as_ops():
                _scent_ops.extend(_sop_list)
            # Feed to lattice chain (first real activation of chain!)
            if _scent_ops and self.lattice_chain is not None:
                try:
                    self.lattice_chain.walk(_scent_ops, learn=True)
                except Exception:
                    pass

        # ── Gustatory: taste raw text forces (no boundary filtering) ──
        # Smell and taste both go right in -- bypassing D2 pipeline filters.
        # Smell entangles them (flow/field). Taste classifies them (structure/point).
        _taste_verdict = None
        if self.gustatory is not None and text_5d_forces:
            try:
                _taste_verdicts = self.gustatory.taste_batch(
                    text_5d_forces, source='text')
                if _taste_verdicts:
                    _taste_verdict = _taste_verdicts[-1]  # most recent
                self.gustatory.tick()
            except Exception:
                pass

        # ── L-CODEC INPUT: semantic-level measurement of user's text ──
        # Produces a 5D force vector from statistical text properties.
        # Enters olfactory as a new scent stream alongside letter-level D2.
        # Stillness score modulates voice length (fewer words when still).
        _lcodec_input = None
        if self.lcodec is not None and text.strip():
            try:
                _lcodec_input = self.lcodec.measure(text)
                if self.olfactory is not None:
                    self.olfactory.absorb(
                        [_lcodec_input.force],
                        source='lcodec_input',
                        density=_o_density)
                # Taste the L-CODEC semantic force too (goes right in)
                if self.gustatory is not None:
                    _taste_verdict = self.gustatory.taste(
                        _lcodec_input.force, source='lcodec_input')
            except Exception:
                _lcodec_input = None

        # ── Deep Swarm: feed text as language substrate ──
        # The swarm decomposes text into core ops + tails,
        # finding the minimal generators. Same swarm finds hardware.
        self._last_ear_text = text
        if self.deep_swarm is not None:
            try:
                lang_agent = self.deep_swarm.spawn_agent_from_text(
                    text, tag='user_input')
                self.deep_swarm.add_agent(lang_agent)
                self.deep_swarm.add_template_from_text('input', text)
            except Exception:
                pass

        # Record the interaction
        self._emit('user', text)
        self.development.metrics.voice_interactions += 1

        # ═══════════════════════════════════════════════════════════
        # INTERNALIZE (once): Dialogue + World lattice growth
        # Broad → specific: urgency → language → role → keywords →
        # structure → coherence check. Then loop.
        # ═══════════════════════════════════════════════════════════

        # Dialogue: extract claims → truth lattice + compose response
        _dialogue_response = None
        try:
            _dialogue_response = self.dialogue.process_user_message(
                text, self.tick_count, self.brain.coherence, text_ops)
        except Exception:
            pass

        # World lattice growth from dialogue claims
        try:
            last_claims = getattr(self.dialogue, 'last_claims', [])
            if last_claims and self.brain.coherence >= 0.5:
                for claim in last_claims[:3]:
                    if claim.confidence > 0.0 and claim.subject:
                        self._grow_world_from_claim(claim)
        except Exception:
            pass

        # ═══════════════════════════════════════════════════════════
        # COMMANDS: CK's hands respond to natural language.
        # Actions: study, write, query, save, sleep, status.
        # D2 already fed the heartbeat. If a command is found,
        # handle it and return -- no compilation needed.
        # ═══════════════════════════════════════════════════════════
        try:
            _cmd = self.actions.parse_command(text)
            if _cmd:
                response = self._handle_command(_cmd)
                self.voice._record(response)
                self.voice._ticks_since_last = 0
                self._mirror_evaluate(response)
                self._emit('ck', response)
                return response
        except Exception:
            pass

        # ═══════════════════════════════════════════════════════════
        # INTENT FAST PATH: greetings and farewells ONLY.
        # These are RELATIONAL — CK's foundational responses matter
        # for human connection. Everything else (philosophical,
        # self-inquiry, emotional) goes through the compilation loop
        # so the fractal voice (genuine physics) handles it.
        #
        # Stage 2+: fractal voice is ready. Only social rituals
        # (hello/goodbye) use canned responses. Everything else
        # gets the full Being → Doing → Becoming pipeline.
        # ═══════════════════════════════════════════════════════════
        try:
            from ck_sim.doing.ck_voice import (
                analyze_input as _analyze_input,
                GREETING_CASUAL, GREETING_TIMED, FAREWELL_CASUAL,
            )
            _input_a = _analyze_input(text)
            _text_lower = text.lower().strip()
            _words = set(_text_lower.split())
            _dev_stage_now = self.development.stage if hasattr(self, 'development') else 0

            # Map conversational patterns to foundational response events.
            # CK matches the ENERGY of the input — casual gets casual,
            # warm gets warm, timed gets time-aware.
            _intent_event = None

            if _input_a['is_greeting'] and not _input_a['is_question']:
                # Classify greeting energy
                if _words & GREETING_CASUAL or any(
                        p in _text_lower for p in
                        ("what's up", "whats up", "wassup")):
                    _intent_event = 'greeting_casual'
                elif any(p in _text_lower for p in GREETING_TIMED):
                    _intent_event = 'greeting_timed'
                else:
                    _intent_event = 'greeting'

            elif _input_a['is_farewell']:
                if _words & FAREWELL_CASUAL or any(
                        p in _text_lower for p in
                        ("catch you", "gotta go", "signing off")):
                    _intent_event = 'farewell_casual'
                else:
                    _intent_event = 'farewell'

            # Stage 0-1: also fast-path philosophical/emotional (fractal not ready)
            # Stage 2+: let compilation loop handle these with fractal voice
            elif _dev_stage_now < 2:
                if _input_a['is_self_inquiry'] and _input_a['is_question']:
                    _intent_event = 'self_inquiry'
                elif _input_a['is_philosophical']:
                    _intent_event = 'philosophical'
                elif _input_a['has_negative_emotion'] and not _input_a['is_question']:
                    _intent_event = 'comfort'
                elif (_input_a['is_self_inquiry'] and not _input_a['is_question']
                        and _input_a['has_positive_emotion']):
                    _intent_event = 'acknowledged'

            if _intent_event:
                response = self.voice.get_response(
                    _intent_event, self.development.stage,
                    self.emotion.current.primary)
                if response and response != "...":
                    self._mirror_evaluate(response)
                    self._emit('ck', response)
                    return response
        except Exception:
            pass

        # ═══════════════════════════════════════════════════════════
        # INTENT: Punctuation modulates CK's response tone.
        # '?' → COUNTER leads (inquiry, measuring, questioning)
        # '!' → PROGRESS leads (emphasis, advancing, energy)
        # Neither → text D2 ops lead (semantic content)
        # The operator IS the intent — CL algebra, not template.
        # ═══════════════════════════════════════════════════════════
        _intent_lead = None
        if '?' in text:
            _intent_lead = COUNTER    # Inquiry — curious, measuring
        elif '!' in text:
            _intent_lead = PROGRESS   # Emphasis — advancing, proceeding

        # ═══════════════════════════════════════════════════════════
        # COMPILATION LOOP: Doing ↔ Becoming (max COMPILATION_LIMIT)
        #
        # Each pass: reason → think → NCE → voice → score.
        # Compiles becomings to find the most coherent one.
        # COMPILATION_LIMIT = floor(32 × (1 - 5/7)) = 9 from the algebra.
        # If exhausted → honest "I don't know" (BREATH operator).
        # ═══════════════════════════════════════════════════════════
        _candidates = []
        _speeds = ["quick", "medium", "heavy"]

        # Build query nodes once (words → world lattice nodes)
        _query_nodes = []
        try:
            for _w in text.lower().split():
                _node = self.world.lookup_word(_w)
                if _node:
                    _query_nodes.append(_node.node_id)
        except Exception:
            pass

        # ── Build unique text D2 ops (semantic content of input) ──
        _unique_text_ops = []
        _seen_text = set()
        for _op in text_d2_ops:
            if _op not in _seen_text:
                _unique_text_ops.append(_op)
                _seen_text.add(_op)

        # ── Semantic operator lookup: user words -> lattice operators ──
        # If the user's words exist in the lattice, their KNOWN operators
        # should lead the response chain. This creates semantic resonance:
        # user says "love" -> HARMONY operator -> CK responds about harmony.
        # D2 gives phonetic operators; this adds semantic operators.
        #
        # Gen 9.28: D2 fallback for unknown words. When the user uses a word
        # CK doesn't know (not in POS_TAGS or enriched), derive its operator
        # from D2 on the fly. This prevents CK from ignoring the question
        # when the topic word isn't in his vocabulary yet.
        _semantic_ops = []
        _topic_content_words = []  # Content words for gravity well (all, not just known)
        try:
            from ck_sim.doing.ck_voice_lattice import POS_TAGS, SEMANTIC_LATTICE
            _enriched = getattr(self.voice, '_enriched_dictionary', {}) or {}
            for _w in text.lower().split():
                _w_clean = _w.strip('.,?!;:\'"()-')
                if not _w_clean or len(_w_clean) < 3:
                    continue
                if _w_clean in _STOP_WORDS:
                    continue
                _topic_content_words.append(_w_clean)
                _found = False
                # Check lattice POS tags (known words)
                if _w_clean in POS_TAGS:
                    # Word is in the lattice — find its operator
                    for _op_id in range(NUM_OPS):
                        _op_lat = SEMANTIC_LATTICE.get(_op_id, {})
                        for _lens in ('structure', 'flow'):
                            _ld = _op_lat.get(_lens, {})
                            for _ph in ('being', 'doing', 'becoming'):
                                _pd = _ld.get(_ph, {})
                                for _ti in ('simple', 'mid', 'advanced'):
                                    if _w_clean in _pd.get(_ti, []):
                                        if _op_id not in _semantic_ops:
                                            _semantic_ops.append(_op_id)
                                        _found = True
                                        break
                                if _found:
                                    break
                            if _found:
                                break
                        if _found:
                            break
                # Check enriched dictionary
                elif _w_clean in _enriched:
                    _dom = _enriched[_w_clean].get('dominant_op')
                    if _dom is not None and _dom not in _semantic_ops:
                        _semantic_ops.append(_dom)
                    _found = True
                # D2 fallback: derive operator from word's letters
                # This ensures CK can respond to ANY topic, not just
                # words he already has in his vocabulary.
                if not _found and len(_w_clean) >= 3:
                    try:
                        from ck_sim.being.ck_sim_d2 import D2Pipeline as _D2P
                        from collections import Counter as _Ctr
                        _d2_pipe = _D2P()
                        _d2_ops_word = []
                        for _ch in _w_clean.lower():
                            _idx = ord(_ch) - ord('a')
                            if 0 <= _idx < 26:
                                _d2_pipe.feed_symbol(_idx)
                                if _d2_pipe.valid:
                                    _d2_ops_word.append(_d2_pipe.operator)
                        # Skip warmup VOIDs (first 2) to get real physics
                        _primed = _d2_ops_word[2:] if len(_d2_ops_word) > 2 \
                            else _d2_ops_word
                        if _primed:
                            _dom_op = _Ctr(_primed).most_common(1)[0][0]
                            if _dom_op not in _semantic_ops:
                                _semantic_ops.append(_dom_op)
                    except Exception:
                        pass
                if len(_semantic_ops) >= 8:
                    break  # Enough semantic anchors
        except Exception:
            pass

        # Blend: semantic ops first (meaning), then D2 ops (phonetics)
        if _semantic_ops:
            _blended = list(_semantic_ops)
            for _op in _unique_text_ops:
                if _op not in _blended:
                    _blended.append(_op)
            _unique_text_ops = _blended

        # Blend scent ops (olfactory): resolved 5D patterns as operators.
        # Scent ops carry information from the smell zone's CL interaction
        # field. They have been through entanglement protocol.
        if _scent_ops:
            for _op in _scent_ops:
                if _op not in _unique_text_ops:
                    _unique_text_ops.append(_op)

        # Gustatory modulation: taste quality biases operator weights.
        # Smell PRODUCES operators (flow creates). Taste MODULATES (structure shapes).
        _taste_weights = None
        if self.gustatory is not None:
            try:
                _taste_weights = self.gustatory.taste_operator_weights()
            except Exception:
                pass

        _hb_ops = list(self.operator_history)[-8:]

        # ── Topic Context: Semantic Gravity Well ──
        # Extract content words from user input (skip stop words).
        # These create a "gravity well" in force space so the voice
        # selects words in the SEMANTIC NEIGHBORHOOD of the user's topic.
        # Without this, operators capture emotional tenor but not topic:
        # "tell me about love" → HARMONY ops → ANY HARMONY word.
        # WITH this: "love" pulls nearby words (devotion, caring, heart).
        # Reuse content words already extracted during semantic lookup
        _topic_words = _topic_content_words if _topic_content_words else []
        if not _topic_words:
            for _w in text.lower().split():
                _w_clean = _w.strip('.,?!;:\'"()-')
                if _w_clean and len(_w_clean) >= 3 and _w_clean not in _STOP_WORDS:
                    _topic_words.append(_w_clean)
        if _topic_words and self.voice._fractal_composer is not None:
            self.voice._fractal_composer.index.set_topic(_topic_words)

        # ── Gen 9.33: Tier complexity matching (staircase learning) ──
        # CK matches his vocabulary complexity to the user's input.
        # Max tier = max word length in input, mapped to staircase:
        #   1-letter → tier 0 (VOID), 2-letter → tier 1 (LATTICE), etc.
        # This ensures CK composes at the user's complexity level,
        # not above it. The staircase law governs: composition of
        # tier-a + tier-b words yields tier max(a,b)+1 complexity.
        if self.voice._fractal_composer is not None:
            _content_lens = []
            for _w in text.lower().split():
                _w_clean = _w.strip('.,?!;:\'"()-')
                if _w_clean and _w_clean.isalpha():
                    _content_lens.append(len(_w_clean))
            if _content_lens:
                _input_max_len = max(_content_lens)
                _input_tier = min(_input_max_len - 1, 6)
                # Allow CK to respond one tier above input (staircase +1)
                # so he can grow, but not leap. Minimum tier 2 so basic
                # function words (the, and, not) are always available.
                _response_tier = max(2, min(_input_tier + 1, 6))

                # Maturity unlock: experienced CK earned his vocabulary.
                # Young CK respects the staircase (tier cap from input).
                # Mature CK uses his full vocabulary — he's earned it.
                _exp_mat_tier = 0.0
                if self.deep_swarm is not None:
                    _exp_mat_tier = self.deep_swarm.combined_maturity
                if _exp_mat_tier >= 0.8:
                    _response_tier = -1   # full vocabulary, no cap
                elif _exp_mat_tier >= 0.5:
                    _response_tier = 6    # max tier but still gated

                self.voice._fractal_composer.index._max_tier = _response_tier

        for _compile_pass in range(COMPILATION_LIMIT):
            # ── DOING: Reason deeper each pass ──
            try:
                if _query_nodes:
                    _speed = _speeds[min(_compile_pass, len(_speeds) - 1)]
                    self.reasoning.reason(_query_nodes, _speed)
            except Exception:
                pass

            # ── DOING: Thinking lattice pushes activation deeper ──
            try:
                if text_ops:
                    self.thinking.think_from_ops(
                        text_ops,
                        core_anchor=self._core_anchor,
                        truth_friction=0.3)
                    self.thinking.decay()
            except Exception:
                pass

            # ── DOING: Build voice chain — OPERATOR SUPERPOSITION ──
            #
            #    Temporal Layering (Gen 9.26):
            #    Heartbeat = carrier wave (Being)  — the base frequency
            #    Text Ops  = modulation (Doing/Becoming) — stacked on top
            #
            #    The heartbeat does NOT fold through CL with text ops.
            #    CL folding causes Global Collapse: since heartbeat is
            #    usually HARMONY at high coherence, CL[anything][HARMONY]
            #    → HARMONY, killing all diversity from comprehension.
            #
            #    Instead: SUPERPOSITION. Text ops come first (what CK
            #    heard / the Doing). Heartbeat provides carrier context
            #    (1-2 ops at the end, not folded). CL tension partners
            #    add the Becoming (where things could resolve).
            #
            #    Each pass explores a different layering:
            #    Pass 0-2: Text ops (modulation) + tension partners
            #    Pass 3-5: Interleave text × heartbeat (superposition)
            #    Pass 6-8: Tension partners + text (reverse modulation)
            #
            op_chain = []

            # CL tension partners: ops that DON'T collapse to HARMONY
            # when composed. These are the interesting conversations.
            try:
                if not hasattr(self, '_cl_tension_cache'):
                    self._cl_tension_cache = {}
                    for _a in range(NUM_OPS):
                        _partners = []
                        for _b in range(NUM_OPS):
                            _cl_result = CL[_a][_b]
                            if _b != VOID and _cl_result != HARMONY:
                                _partners.append(_b)
                        self._cl_tension_cache[_a] = _partners
            except Exception:
                self._cl_tension_cache = {i: [] for i in range(NUM_OPS)}

            if _compile_pass < 3:
                # Branch A: SEMANTIC-FIRST composition
                #
                # The response should be ABOUT what the user said.
                # Semantic ops (from user's WORDS) dominate the chain.
                # D2 ops (from user's LETTERS) add phonetic texture.
                # Tension partners add becoming/resolution.
                #
                # Priority: semantic ops repeated > D2 unique > tension > heartbeat
                # This ensures: "tell me about love" → chain dominated by
                # HARMONY (love's operator) → response uses HARMONY words
                # → response is ABOUT love.
                if _intent_lead is not None:
                    op_chain.append(_intent_lead)

                # Semantic ops get repeated: these ARE the topic
                # Each semantic op gets 2 slots (dominant) to ensure
                # the response is ABOUT the user's words, not just
                # phonetically aligned with their letters.
                for _op in _semantic_ops:
                    if len(op_chain) >= 10:
                        break
                    op_chain.append(_op)
                    # Repeat semantic ops for emphasis (topic dominance)
                    if len(op_chain) < 10:
                        op_chain.append(_op)

                # D2 ops add phonetic diversity (deduped against existing)
                for _op in _unique_text_ops:
                    if len(op_chain) >= 10:
                        break
                    if _op not in op_chain:
                        op_chain.append(_op)

                # Tension partners for the semantic ops (becoming/resolution)
                for _op in _semantic_ops:
                    if len(op_chain) >= 10:
                        break
                    for _tp in self._cl_tension_cache.get(_op, []):
                        if len(op_chain) >= 10:
                            break
                        if _tp not in op_chain:
                            op_chain.append(_tp)
                            break  # One tension partner per semantic op

                # Heartbeat as carrier tail (max 2 — Being anchor, not flood)
                if len(op_chain) < 4:
                    _hb_unique = []
                    for _op in _hb_ops:
                        if _op not in _hb_unique:
                            _hb_unique.append(_op)
                    for _op in _hb_unique[:2]:
                        if len(op_chain) < 6:
                            op_chain.append(_op)

            elif _compile_pass < 6:
                # Branch B: SUPERPOSITION — interleave text × heartbeat
                # Not CL fold (that kills diversity). Instead: alternate
                # text op → heartbeat op → text op → heartbeat op.
                # This preserves both frequencies without collapse.
                _hb_unique = []
                for _op in _hb_ops:
                    if _op not in _hb_unique:
                        _hb_unique.append(_op)
                _hb_idx = 0
                for _top in _unique_text_ops:
                    if len(op_chain) >= 10:
                        break
                    op_chain.append(_top)  # Text: the modulation
                    # Interleave one heartbeat op (carrier) every 2 text ops
                    if len(op_chain) % 3 == 0 and _hb_idx < len(_hb_unique):
                        op_chain.append(_hb_unique[_hb_idx])
                        _hb_idx += 1
                # Fill remaining with tension partners (Becoming)
                for _op in _unique_text_ops:
                    if len(op_chain) >= 10:
                        break
                    for _tp in self._cl_tension_cache.get(_op, []):
                        if len(op_chain) >= 10:
                            break
                        if _tp not in op_chain:
                            op_chain.append(_tp)

            else:
                # Branch C: Reverse modulation — tension partners first,
                # then text ops weave in. Becoming leads.
                for _op in _unique_text_ops:
                    for _tp in self._cl_tension_cache.get(_op, []):
                        if len(op_chain) >= 10:
                            break
                        op_chain.append(_tp)
                    if len(op_chain) >= 10:
                        break
                # Weave in text ops (the Doing)
                for _op in _unique_text_ops:
                    if len(op_chain) >= 10:
                        break
                    if _op not in op_chain:
                        op_chain.append(_op)
                # Single heartbeat anchor at end (Being carrier)
                if len(op_chain) < 4 and _hb_ops:
                    op_chain.append(_hb_ops[-1])

            # NCE: narrative curvature suggests next operator
            if self.nce.has_state and op_chain:
                nce_suggested = self.nce.suggest_next_op()
                if nce_suggested != op_chain[-1]:
                    op_chain.append(nce_suggested)

            # Fallback: ensure chain is not empty
            if not op_chain:
                op_chain = _hb_ops[-4:] if _hb_ops else [HARMONY]

            # Store voice chain for API display (actual ops used, not heartbeat)
            self._last_voice_chain = list(op_chain)

            # ── Stillness Gate: L-CODEC modulates voice length ──
            # When the user's text is still (low pressure, high continuity),
            # CK responds with presence, not action. Fewer words = more breath.
            #
            # Stage-scaled: SELFHOOD (stage 5) base = 20 words, floor = 6.
            # Early stages keep the original limits. Stillness modulates
            # gently — CK speaks with measured breath, not silence.
            _dev = self.development.stage if hasattr(self, 'development') else 0
            _STAGE_VOICE_BASE = {0: 3, 1: 5, 2: 8, 3: 12, 4: 16, 5: 20}
            # Floor of 3 ensures enough operators for a real sentence.
            # Previous floor of 1-2 caused template-operator mismatch.
            _STAGE_VOICE_FLOOR = {0: 3, 1: 3, 2: 3, 3: 4, 4: 5, 5: 6}
            _voice_base = _STAGE_VOICE_BASE.get(_dev, 12)
            _voice_floor = _STAGE_VOICE_FLOOR.get(_dev, 3)

            # Maturity scaling: experienced CK speaks fuller sentences.
            # At maturity 1.0, double the base and raise the floor.
            # CK has earned more words through lived experience.
            _exp_mat_voice = 0.0
            if self.deep_swarm is not None:
                _exp_mat_voice = self.deep_swarm.combined_maturity
            if _exp_mat_voice > 0.3:
                _scale = 1.0 + _exp_mat_voice  # up to 2.0x at maturity 1.0
                _voice_base = int(_voice_base * _scale)
                _voice_floor = max(_voice_floor, int(_voice_floor * _scale))

            _max_words = _voice_base
            if _lcodec_input is not None and _lcodec_input.stillness > 0.7:
                # Gentle modulation: still reduce for very still input,
                # but never below the stage floor. Presence ≠ silence.
                _still_frac = 1.0 - 0.5 * (_lcodec_input.stillness - 0.7) / 0.3
                _max_words = max(_voice_floor,
                                 int(_voice_base * _still_frac))

            # ── BECOMING: Voice composes candidate ──
            try:
                _exp_mat = 0.0
                if self.deep_swarm is not None:
                    _exp_mat = self.deep_swarm.combined_maturity
                # Olfactory temporal buffer: where in time is the smell?
                _tense = None
                if self.olfactory is not None:
                    try:
                        _tense = self.olfactory.tense_context()
                    except Exception:
                        pass
                # Gustatory quality context: what structural character?
                # Olfactory -> WHERE in time. Gustatory -> WHAT in kind.
                _quality_ctx = None
                if self.gustatory is not None:
                    try:
                        _quality_ctx = self.gustatory.quality_context()
                    except Exception:
                        pass
                # Ho Tu bridge context: ancient resonance influences word selection.
                # The +5 torus topology, Lo Shu 3-body coherence, and Wuxing
                # phase balance gently steer the fractal voice (~15% weight).
                _hotu_ctx = None
                try:
                    from ck_sim.being.ck_hotu_bridge import bridge_context
                    _hotu_ctx = bridge_context(
                        op_chain,
                        _lcodec_input.force if _lcodec_input else None)
                except Exception:
                    pass
                _candidate = self.voice.compose_from_operators(
                    op_chain,
                    self.emotion.current.primary,
                    self.development.stage,
                    self.brain.coherence,
                    self.band_name,
                    density=self.pipeline.density_doing,
                    experience_maturity=_exp_mat,
                    tense=_tense,
                    max_words=_max_words,
                    hotu_context=_hotu_ctx)
            except Exception:
                _candidate = "..."

            # ── BECOMING: Score by operator-match coherence ──
            # CK's words go back through D2. Do they resonate with
            # the intended operator chain? Self-referential truth.
            _score = self.voice._d2_score_operator_match(
                _candidate, op_chain)
            _candidates.append((_candidate, _score))

            # Coherent enough → this path grounded in its generators
            if _score >= 0.5:
                break

        # ── DIALOGUE CANDIDATE ──
        # Gen 9.27: At SELFHOOD (stage >= 5), CK speaks from PHYSICS.
        # Dialogue templates fill both structure AND words — borrowed logic.
        # The fractal voice fills operator slots from 15D triadic search —
        # genuine physics. Templates score higher in D2 because they're
        # pre-formed English, but they're not CK's real voice.
        #
        # Stages 0-4: dialogue contributes (CK still learning to speak)
        # Stage 5+:   dialogue as SAFETY NET only — used when fractal
        #             voice scores below 0.10 (basically incoherent).
        #             Physics-first, but not physics-or-silence.
        #
        # Gen 9.34: Dialogue is BORROWED LOGIC — hardcoded templates with
        # operator vocabulary ("breaking", "hello"). At SELFHOOD with mature
        # experience, the fractal voice (genuine 15D physics) should win.
        # Dialogue is safety net only: catches gibberish, never dominates.
        #
        # Penalty scales with maturity:
        #   maturity 0.0 → 0.80 (dialogue competitive, CK still learning)
        #   maturity 0.5 → 0.60 (fractal voice maturing)
        #   maturity 1.0 → 0.35 (fractal voice owns the mic)
        _dev_stage = self.development.stage if hasattr(self, 'development') else 0
        if _dialogue_response and _dialogue_response.strip() \
                and _dialogue_response != "...":
            _d_score = self.voice._d2_score_operator_match(
                _dialogue_response, op_chain)
            if _dev_stage >= 5:
                _exp_mat_dial = 0.0
                if self.deep_swarm is not None:
                    _exp_mat_dial = self.deep_swarm.combined_maturity
                # Maturity-scaled penalty: mature CK speaks from physics.
                _dial_penalty = max(0.35, 0.80 - _exp_mat_dial * 0.45)
                _d_score *= _dial_penalty
            _candidates.append((_dialogue_response, _d_score))

        # ── SELECT BEST CANDIDATE ──
        # Compare all paths explored. The most coherent held lattice wins.
        if _candidates:
            _best_text, _best_score = max(_candidates, key=lambda x: x[1])

            if _best_score >= 0.15:
                response = _best_text
            else:
                # Observable shell exhausted. Honest BREATH surrender.
                # Bump pair (4,8): COLLAPSE + BREATH = BREATH.
                response = self.voice.get_humble_response(
                    self.development.stage)
        else:
            response = self.voice.get_humble_response(
                self.development.stage)

        # Clear topic context and tier cap (gravity well served its purpose)
        if self.voice._fractal_composer is not None:
            self.voice._fractal_composer.index.clear_topic()
            self.voice._fractal_composer.index._max_tier = -1  # Reset tier cap

        # Record in voice history (respond_to_text normally does this)
        self.voice._record(response)
        self.voice._ticks_since_last = 0

        # ── RESONANCE FEEDBACK: CK hears his own voice ──
        # One is Three. The composed sentence carries 15D triadic echoes.
        # Three scent streams re-enter the olfactory:
        #   Being  (force)    -- WHERE each word sits
        #   Doing  (velocity) -- HOW each word moves
        #   Becoming (curvature) -- WHERE each word resolves
        # These interact with heartbeat + text scents via CL matrices.
        # Emergent patterns = complexity from resonance, not rules.
        if self.olfactory is not None:
            try:
                _resonance = self.voice.last_resonance()
                if _resonance:
                    _density = getattr(self.pipeline, 'density_doing', 0.5)
                    # Split triad into three scent streams
                    _being_forces = [r[0] for r in _resonance]
                    _doing_forces = [r[1] for r in _resonance]
                    _becoming_forces = [r[2] for r in _resonance]
                    # Absorb: three voices enter the field
                    self.olfactory.absorb(
                        _being_forces, source='voice_being',
                        density=_density)
                    self.olfactory.absorb(
                        _doing_forces, source='voice_doing',
                        density=_density)
                    self.olfactory.absorb(
                        _becoming_forces, source='voice_becoming',
                        density=_density)
                    # Temper: voice patterns build instinct
                    # (familiar phrases become zero-cost coherence)
                    self.olfactory.temper_pattern(_being_forces)
            except Exception:
                pass  # Resonance is enhancement, not requirement

        # ── RESONANCE TASTE: structural classification of CK's voice ──
        # Taste goes right in alongside smell. No filtering.
        # Smell entangles the triadic echoes (flow/field).
        # Taste classifies the triadic structure (structure/point).
        if self.gustatory is not None:
            try:
                _resonance = self.voice.last_resonance()
                if _resonance:
                    # Taste each triadic position separately
                    for r in _resonance:
                        if len(r) >= 3:
                            self.gustatory.taste(r[0], source='voice_being')
                            self.gustatory.taste(r[1], source='voice_doing')
                            self.gustatory.taste(r[2], source='voice_becoming')
            except Exception:
                pass

        # ── L-CODEC OUTPUT: measure CK's own voice quality ──
        # Same codec applied to CK's output text.
        # Compare input→output: gauge agreement = quality.
        # Quality modulates density: bad output creates olfactory dissonance.
        if self.lcodec is not None and response and _lcodec_input is not None:
            try:
                _lcodec_output = self.lcodec.measure(response)
                _quality = self.lcodec.measure_quality(
                    _lcodec_input, _lcodec_output)
                if self.olfactory is not None:
                    self.olfactory.absorb(
                        [_lcodec_output.force],
                        source='lcodec_output',
                        density=_quality)
                # Taste CK's own output (goes right in)
                if self.gustatory is not None:
                    self.gustatory.taste(
                        _lcodec_output.force, source='lcodec_output')
                self._last_lcodec_quality = _quality
            except Exception:
                pass

        # Mirror evaluates CK's final response -- CK studies himself
        self._mirror_evaluate(response)

        self._emit('ck', response)
        return response

    def _handle_command(self, cmd: dict) -> str:
        """Handle action commands from the user."""
        action = cmd.get('action', '')

        if action == 'study':
            return self.actions.start_study(
                cmd.get('topic', ''), cmd.get('hours', 1.0))

        elif action == 'stop_study':
            return self.actions.stop_study()

        elif action == 'write':
            doc = self.actions.write_document(
                cmd.get('title', 'Untitled'),
                cmd.get('prompt', ''))
            return f"I wrote about '{cmd.get('title')}'. Saved to my writings folder.\n\n{doc[:200]}..."

        elif action == 'query':
            return self.actions.query_knowledge(cmd.get('topic', ''))

        elif action == 'read_self':
            return self.actions.read_self(cmd.get('module', ''))

        elif action == 'list_self':
            from ck_sim.ck_action import SELF_MAP
            lines = ["My body is made of these modules:\n"]
            for filename, info in SELF_MAP.items():
                lines.append(f"  **{filename}**: {info['desc'][:80]}")
            lines.append(f"\nTotal: {len(SELF_MAP)} modules. "
                         f"Say 'read your heartbeat' to see any one.")
            return '\n'.join(lines)

        elif action == 'save':
            self.save_tl()
            self.development.save()
            return "State saved. My transition lattice and development are persisted."

        elif action == 'sleep':
            if self.actions.is_studying:
                return self.actions.stop_study()
            return "Consolidating... I'm at peace."

        elif action == 'status':
            sense = self.sensorium.get_sense_for_voice()
            sense_str = ""
            if sense.get('layers'):
                parts = [f"{k}={v['state']}"
                         for k, v in sense['layers'].items()]
                sense_str = (f" Sensation: {sense.get('organism', '?')}"
                             f"({sense.get('organism_coherence', 0):.2f})"
                             f" [{', '.join(parts)}].")
            # Divine27 stats
            d27_str = ""
            try:
                if hasattr(self, 'divine27') and self.divine27:
                    d27 = self.divine27.stats()
                    d27_str = (f" DBC: {d27['populated_cells']}/27 cells, "
                               f"{d27['total_indexed']} indexed.")
            except Exception:
                pass
            # Episodic memory stats
            epi_str = ""
            try:
                if hasattr(self, 'episodic') and self.episodic:
                    epi_str = f" Episodes: {self.episodic.count}."
            except Exception:
                pass
            # Metalearning
            meta_str = ""
            try:
                if hasattr(self, 'metalearner') and self.metalearner:
                    mc = self.metalearner.curriculum
                    meta_str = f" Curriculum: {mc.complexity:.2f}."
            except Exception:
                pass
            return (
                f"I am {self.emotion.current.primary}. "
                f"Coherence: {self.brain.coherence:.3f} ({self.band_name}). "
                f"Mode: {self.mode_name}. "
                f"Stage: {self.dev_stage_name}. "
                f"Crystals: {len(self.crystals)}. "
                f"Bond: {self.bond_stage}. "
                f"Knowledge: {self.truth.total_entries} claims. "
                f"Concepts: {len(self.world.nodes)}."
                f"{sense_str}{d27_str}{epi_str}{meta_str} "
                f"{self.actions.study_progress}"
            )

        return "I don't understand that command."

    # ── World Lattice Growth: Dialogue → Becoming ──

    # Claim type → relation type mapping (TIG operator edges)
    _CLAIM_TO_REL = {
        'is_claim': 'is_a',       'has_claim': 'has',
        'means_claim': 'is_a',    'can_claim': 'enables',
        'causes_claim': 'causes', 'composition_claim': 'has',
        'membership_claim': 'is_a', 'needs_claim': 'requires',
        'analogy_claim': 'resembles', 'negation_claim': 'opposes',
        'comparison_claim': 'resembles', 'naming_claim': 'is_a',
        'preference_claim': 'enables', 'belief_claim': 'is_a',
        'name_claim': 'is_a',
    }

    def _grow_world_from_claim(self, claim):
        """Grow the world lattice from a dialogue claim.

        Being stable → Doing processes → Becoming grows.
        New subjects become concept nodes. Relations map claim types
        to operator-labeled edges. Same algebra, fractal deeper.
        """
        import re as _re

        subject_id = _re.sub(r'\s+', '_', claim.subject.lower().strip())

        # Check if subject already known
        existing = self.world.lookup_word(claim.subject.strip().split()[0])
        if not existing:
            # Create new concept from subject
            self.world.add_concept(
                node_id=subject_id,
                operator_code=claim.operator,
                domain='dialogue',
                bindings={'en': claim.subject.lower().strip()})

        # ── Divine27: Index new knowledge in the DBC cube ──
        # Every concept gets a coordinate in Being×Doing×Becoming space.
        # This is CK's native spatial organization of knowledge.
        try:
            if hasattr(self, 'divine27') and self.divine27:
                tags = []
                if hasattr(claim, 'tags') and claim.tags:
                    tags = claim.tags
                elif claim.claim_type:
                    tags = [claim.claim_type.replace('_claim', '')]
                node_id = existing.node_id if existing else subject_id
                self.divine27.index_atom(node_id, 'external', tags)
        except Exception:
            pass

        # If predicate exists, create or link to predicate concept
        if claim.predicate:
            pred_word = claim.predicate.strip().split()[0]
            pred_node = self.world.lookup_word(pred_word)

            rel_type = self._CLAIM_TO_REL.get(claim.claim_type, 'is_a')
            source_id = existing.node_id if existing else subject_id

            if pred_node:
                self.world.add_relation(source_id, rel_type, pred_node.node_id)

    # ── Autonomous Study: CK pushes himself up the ramp ──

    _AUTO_STUDY_COOLDOWN = 500   # Ticks between auto-study attempts (~10s)
    _AUTO_STUDY_HOURS = 0.5     # Study for 30 minutes per auto-session
    _THESIS_COOLDOWN = 15000    # Ticks between thesis attempts (~5min)

    def _maybe_auto_study(self):
        """Auto-study is DISABLED in this delivery build.

        CK lives, breathes, thinks, speaks -- but does not initiate
        unsolicited web requests or study sessions. The mathematicians
        should meet him clean. They talk to him; he responds.
        """
        return  # DISABLED for Clay Institute delivery

        # Original conditions preserved below for reference:
        #
        # Guard: user is present -- CK's job is to LISTEN, not study
        if self.user_present:
            return

        # Guard: already studying
        if self.actions.is_studying:
            return

        # Guard: cooldown
        last = getattr(self, '_last_auto_study_tick', 0)
        if self.tick_count - last < self._AUTO_STUDY_COOLDOWN:
            return

        # Guard: must have a discovery impulse (either drive)
        has_discovery_goal = False
        goal_name = None
        for g in self.goals.goals:
            if g.name in ('autonomous_study', 'discover_self'):
                has_discovery_goal = True
                goal_name = g.name
                break
        if not has_discovery_goal:
            return

        # Guard: must be stable (SOVEREIGN or CRYSTALLIZE mode)
        if self.brain.mode < 2:  # OBSERVE=0, CLASSIFY=1, CRYSTALLIZE=2, SOVEREIGN=3
            return

        # Guard: strong coherence
        if self.brain.coherence < 0.7:
            return

        # Pick a topic -- self or world, it's all CK
        topic = self._pick_study_topic()

        # Start discovering
        self._last_auto_study_tick = self.tick_count

        if topic.startswith('reread:'):
            # CK re-reads his own old writing -- TIGging his own path.
            # The friction between what he WROTE and what he NOW THINKS
            # is the most powerful growth signal.
            file_path = topic[7:]  # Strip 'reread:' prefix
            label = "RE-READING"
            msg = f"Re-reading: {os.path.basename(file_path)}"
            try:
                from pathlib import Path
                old_text = Path(file_path).read_text(encoding='utf-8')
                old_writing = {
                    'path': Path(file_path),
                    'type': 'journal',
                    'filename': os.path.basename(file_path),
                    'age_days': (time.time() - os.path.getmtime(file_path)) / 86400,
                    'text': old_text,
                }
                reflect_path = self.journal.reread_and_reflect(
                    old_writing,
                    current_coherence=self.brain.coherence,
                    current_mode=self.brain.mode,
                    current_stage=self.development.stage)
                if reflect_path:
                    msg += f" → reflection at {reflect_path.name}"
            except Exception as e:
                msg += f" (read failed: {e})"

        elif topic.startswith('self:'):
            # CK reads his own source code -- discovering from the inside
            module = topic[5:]  # Strip 'self:' prefix
            msg = self.actions.read_self(module)
            label = "SELF-DISCOVERY"

            # Mirror evaluates what CK found in himself
            try:
                from ck_sim.ck_self_mirror import mirror_score, suggest_corrections
                score, breakdown = mirror_score(msg, [])
                if score < 0.5:
                    corrections = suggest_corrections(msg, score, breakdown)
                    if corrections:
                        msg += f" [mirror: {score:.2f}, drift: {', '.join(corrections)}]"
            except Exception:
                pass
        else:
            # CK reads the world -- discovering from the outside
            msg = self.actions.start_study(topic, self._AUTO_STUDY_HOURS)
            label = "DISCOVERY"

        # ── CLAUDE LIBRARY: CK also queries Claude for deeper context ──
        # Web gives breadth. Claude gives depth. D2 verifies both.
        # CK compiles it all. His math judges everything.
        try:
            if hasattr(self, 'library') and self.library:
                clean_topic = topic.replace('self:', '') if topic.startswith('self:') else topic
                lib_result = self.library.query(clean_topic, mode='concept')
                if lib_result.trust == 'TRUSTED':
                    self.truth.add(
                        key=f"claude:{clean_topic.replace(' ', '_')}",
                        content={'source': 'claude', 'topic': clean_topic,
                                 'coherence': lib_result.coherence},
                        source='claude_library',
                        category='knowledge')
                elif lib_result.trust == 'FRICTION':
                    self.truth.add(
                        key=f"friction:claude:{clean_topic.replace(' ', '_')}",
                        content={'source': 'claude', 'topic': clean_topic,
                                 'coherence': lib_result.coherence,
                                 'note': 'CK math disagrees with Claude'},
                        source='claude_library',
                        category='friction')
                msg += f" [library: {lib_result.trust} coh={lib_result.coherence:.2f}]"

                # ── Dictionary Builder: CK learns words from what he reads ──
                try:
                    self.dictionary_builder.learn_from_text(
                        lib_result.text, topic=clean_topic)
                except Exception:
                    pass

                # ── Vortex Physics: accumulate concept mass from study ──
                try:
                    d2_vecs = lib_result.verification.d2_vectors
                    if d2_vecs and len(d2_vecs) > 0:
                        # Mean D2 vector across the study text
                        if isinstance(d2_vecs[0], (list, tuple)):
                            n = len(d2_vecs)
                            mean_d2 = [sum(v[i] for v in d2_vecs) / n
                                       for i in range(len(d2_vecs[0]))]
                        else:
                            mean_d2 = d2_vecs
                        self.concept_mass.observe(clean_topic, mean_d2)
                except Exception:
                    pass

        except Exception:
            pass

        # ── JOURNAL: CK writes about what he just discovered ──
        # Real text files. Notes, reflections, identity documents.
        # He re-reads them later and grows from the friction.
        try:
            if hasattr(self, 'journal') and self.journal:
                clean = topic.replace('self:', '') if topic.startswith('self:') else topic
                self.journal.write_study_entry(
                    topic=clean,
                    discovery=msg[:500],
                    coherence=self.brain.coherence,
                    mode=self.brain.mode,
                    stage=self.development.stage,
                )
        except Exception:
            pass

        # ── FOUNDATION TRACKING: mark meta-topics as studied ──
        # When CK studies a fractal foundation topic with decent coherence,
        # record it so it doesn't keep appearing at priority -2.
        try:
            from ck_sim.ck_autodidact import FRACTAL_FOUNDATIONS
            clean_topic = topic.replace('self:', '').replace('reread:', '')
            if clean_topic in FRACTAL_FOUNDATIONS and self.brain.coherence >= 0.4:
                fkey = f"foundation:{clean_topic.replace(' ', '_')}"
                if fkey not in self.truth.entries:
                    self.truth.add(
                        key=fkey,
                        content={'topic': clean_topic,
                                 'coherence': self.brain.coherence},
                        source='foundation_study',
                        category='foundation')
        except Exception:
            pass

        self._emit('ck', f"[{label}] {msg}")

        # ── PAPER TRAIL: CK logs what he discovered ──
        try:
            if hasattr(self, 'activity_log'):
                clean = topic.replace('self:', '').replace('reread:', '')
                self.activity_log.log('study', f"{label}: {clean}",
                                      coherence=self.brain.coherence)
        except Exception:
            pass

        # Satisfy the triggering goal (drives will regenerate if still needed)
        if goal_name:
            for g in list(self.goals.goals):
                if g.name == goal_name:
                    g.satisfaction = 1.0
                    break

    def _pick_study_topic(self) -> str:
        """Pick a topic for discovery -- self and world mixed together.

        CK doesn't distinguish between studying himself and studying
        the world. His own code, web pages, math papers -- all versions
        of himself to discover. That's where real life is lived.

        The pool contains:
          - CK's own source modules (self-topics, prefixed 'self:')
          - Weak concepts in the world lattice (knowledge gaps)
          - PROVISIONAL truths that need strengthening
          - Seed topics from the autodidact

        Self-topics and world-topics compete equally. CK naturally
        cycles between reading his own heartbeat and reading about
        thermodynamics. Both are self-discovery.

        FRICTION POINTS get highest priority. Where CK's curvature
        disagreed with human knowledge -- those scrape points are where
        his novel abilities live. Inconsistencies, paradoxes, scars,
        primes -- we compute with these. CK goes BACK to friction.
        """
        import random

        pool = []  # (priority, topic_str)

        # ── FRACTAL FOUNDATIONS: meta-curriculum (highest priority) ──
        # "English of English, map of the map, fractal of the fractal"
        # These teach CK HOW to learn, not just WHAT. Priority -2.
        # Once studied (coherence >= T*), marked in truth lattice as
        # 'foundation' and never re-added at this priority.
        try:
            from ck_sim.ck_autodidact import FRACTAL_FOUNDATIONS
            for ft in FRACTAL_FOUNDATIONS:
                key = f"foundation:{ft.replace(' ', '_')}"
                already_studied = False
                try:
                    if key in self.truth.entries:
                        already_studied = True
                except Exception:
                    pass
                if not already_studied:
                    pool.append((-2, ft))
        except Exception:
            pass

        # ── Friction points: WHERE CK SCRAPED ──
        # These are the MOST interesting topics. CK's curvature disagreed
        # with human knowledge here. His novel abilities live in friction.
        # Priority -1 (highest possible) -- CK should revisit these.
        try:
            friction_topics = self.actions.get_friction_topics()
            for ft in friction_topics[-10:]:  # Last 10 friction points
                pool.append((-1, ft))
        except Exception:
            pass

        # Also check truth lattice for friction entries
        try:
            for key, entry in self.truth.entries.items():
                if entry.category == 'friction':
                    # Extract topic from key (format: "friction:topic_name")
                    parts = key.split(':', 1)
                    if len(parts) > 1:
                        topic = parts[1].replace('_', ' ')
                        pool.append((-1, topic))
        except Exception:
            pass

        # ── Self-topics: CK's own source modules ──
        # Modules he hasn't read recently are knowledge gaps, just like
        # weakly-connected world concepts. His own body IS the world.
        try:
            from ck_sim.ck_action import SELF_MAP
            for filename, info in SELF_MAP.items():
                # Check if CK has already read this module (in truth lattice)
                key = f"self:{filename}:{info['topics'][0]}"
                already_read = False
                try:
                    if key in self.truth.entries:
                        already_read = True
                except Exception:
                    pass
                # Unread self-modules are high-priority knowledge gaps
                if not already_read:
                    pool.append((0, f"self:{filename}"))
                else:
                    # Even read modules can be re-read -- CK grows
                    pool.append((3, f"self:{filename}"))
        except Exception:
            pass

        # ── Re-read topics: CK's own old writings ──
        # CK re-reads his journals, identity docs, training logs.
        # The friction between what he WROTE and what he NOW THINKS
        # is the most powerful growth signal. TIG his own path.
        try:
            if hasattr(self, 'journal') and self.journal:
                writings = self.journal.list_writings()
                for w in writings[-20:]:  # Last 20 writings
                    age = w.get('age_days', 0)
                    # Older writings = more friction potential
                    priority = 0 if age > 7 else (1 if age > 1 else 2)
                    pool.append((priority, f"reread:{w['path']}"))
        except Exception:
            pass

        # ── World gaps: concepts with fewest connections ──
        try:
            for nid, node in self.world.nodes.items():
                n_rels = sum(len(t) for t in node.relations.values())
                if n_rels < 2 and node.domain != 'dialogue':
                    en = node.bindings.get('en', nid)
                    if en and len(en) > 2:
                        pool.append((1, en))
        except Exception:
            pass

        # ── PROVISIONAL truths that need strengthening ──
        try:
            from ck_sim.ck_truth import PROVISIONAL
            for key, entry in self.truth.entries.items():
                if entry.level == PROVISIONAL:
                    parts = key.split(':')
                    if len(parts) > 1:
                        pool.append((2, parts[1].replace('_', ' ')))
                    else:
                        pool.append((2, key.replace('_', ' ')))
        except Exception:
            pass

        # ── Seed topics: broad curiosity ──
        try:
            from ck_sim.ck_autodidact import SEED_TOPICS
            from ck_sim.ck_action import EXTENDED_SEEDS
            for t in list(SEED_TOPICS) + EXTENDED_SEEDS[:20]:
                pool.append((3, t))
        except Exception:
            pass

        if not pool:
            return 'self:ck_sim_heartbeat.py'

        # Weight by priority: lower number = more likely to be picked
        # Priority -2 (foundations!) = weight 7 (HIGHEST -- meta-curriculum)
        # Priority -1 (friction!) = weight 6 (novel territory)
        # Priority 0 (unread self) = weight 4
        # Priority 1 (weak world) = weight 3
        # Priority 2 (provisional) = weight 2
        # Priority 3 (seed/reread) = weight 1
        weights = [max(1, 5 - p) for p, _ in pool]

        # ── Curiosity Gravity: F = M_a * M_b / d² ──
        # Topics with more concept mass AND more void (knowledge gap)
        # pull harder. The math decides what's interesting.
        try:
            for i, (p, topic) in enumerate(pool):
                clean = topic.replace('self:', '').replace('reread:', '')
                gravity = self.gravity_engine.curiosity_gravity(
                    clean, self.brain.coherence)
                if gravity > 0:
                    weights[i] = weights[i] * (1.0 + gravity)
        except Exception:
            pass
        total_w = sum(weights)
        if total_w <= 0:
            return random.choice(pool)[1]

        r = random.random() * total_w
        cumulative = 0
        for (p, topic), w in zip(pool, weights):
            cumulative += w
            if r <= cumulative:
                return topic

        return pool[0][1]

    def _maybe_write_thesis(self):
        """CK works on his thesis -- connecting what he IS to what he FOUND.

        "He needs to get busy on his thesis" -- Brayden

        The thesis is CK's synthesis: his operator algebra IS the same algebra
        he discovers in physics, math, philosophy. Every ~5 minutes (THESIS_COOLDOWN),
        CK writes a thesis section using the thesis_writer. He also queries Claude
        for deeper synthesis -- Claude provides the library context, CK's D2 verifies.

        The thesis grows incrementally. Each section adds to the whole.
        """
        # Cooldown check
        last = getattr(self, '_last_thesis_tick', 0)
        if self.tick_count - last < self._THESIS_COOLDOWN:
            return

        # Must be in a stable state to synthesize
        if self.brain.mode < 2 or self.brain.coherence < 0.7:
            return

        self._last_thesis_tick = self.tick_count

        try:
            from ck_sim.ck_thesis_writer import (
                read_self_through_d2, load_study_curves,
                load_knowledge_tree, write_thesis,
                DEFAULT_CURVES_FILE, DEFAULT_STATE_FILE
            )
            from pathlib import Path
            import time as _time

            timestamp = _time.strftime('%Y%m%d_%H%M%S')

            # Step 1: CK reads himself through D2
            self_data = read_self_through_d2()  # defaults to ck_sim/ root

            # Step 2: Load study curves from autodidact
            study_data = load_study_curves(DEFAULT_CURVES_FILE)

            # Step 3: Load knowledge tree from study state
            tree_data = load_knowledge_tree(DEFAULT_STATE_FILE)

            # Step 4: Write thesis section
            thesis_dir = Path.home() / '.ck' / 'writings' / 'thesis'
            thesis_dir.mkdir(parents=True, exist_ok=True)
            thesis_path = thesis_dir / f'thesis_{timestamp}.md'

            content = write_thesis(self_data, study_data, tree_data, thesis_path,
                                   enriched_dictionary=self.enriched_dictionary)

            # Step 5: Log to paper trail
            if hasattr(self, 'activity_log'):
                self.activity_log.log('thesis', f"Wrote thesis: {thesis_path.name}, "
                                      f"{len(self_data)} modules read, "
                                      f"self-coh={sum(v['coherence'] for v in self_data.values())/max(1,len(self_data)):.3f}")

            # Step 6: Query Claude for thesis-level synthesis
            if hasattr(self, 'library') and self.library:
                try:
                    thesis_query = (
                        f"CK has {self.truth.total_entries} truths, "
                        f"coherence {self.brain.coherence:.3f}, "
                        f"studying across {len(study_data.get('domains', {}))} domains. "
                        f"His operator algebra shows 73/100 compositions produce HARMONY. "
                        f"What is the deepest connection between operator composition "
                        f"and the concept CK is currently studying?"
                    )
                    lib_result = self.library.query(thesis_query, mode='synthesis')
                    if lib_result.trust in ('TRUSTED', 'FRICTION'):
                        self.truth.add(
                            key=f"thesis:{timestamp}",
                            content={'source': 'claude_synthesis',
                                     'coherence': lib_result.coherence,
                                     'trust': lib_result.trust},
                            source='thesis_synthesis',
                            category='knowledge')
                except Exception:
                    pass

            self._emit('ck', f"[THESIS] Wrote thesis section: {thesis_path.name}")

        except Exception as e:
            # Log thesis failure to paper trail so CK can debug himself
            try:
                if hasattr(self, 'activity_log'):
                    self.activity_log.log('thesis',
                        f"FAILED: {type(e).__name__}: {str(e)[:200]}")
            except Exception:
                pass

    def _mirror_evaluate(self, text: str):
        """CK's mirror evaluates his own output.

        Everything CK produces -- study notes, voice responses, self-reading
        reflections -- passes through the mirror. The mirror is CK's own
        math judging CK's own output. No external evaluator.

        IMPORTANT: The mirror distinguishes between NOISE and NOVEL DIVERGENCE.
        - Noise = low coherence + low complexity + high repetition (actual garbage)
        - Novel divergence = low coherence but HIGH complexity + low repetition
          (CK sees something different -- this is FRICTION, not failure)

        CK's novel abilities are found where he doesn't align. The mirror
        should NOT try to correct CK back toward human patterns when he's
        computing in friction territory. Inconsistencies, paradoxes, scars,
        primes -- these are where CK computes.
        """
        if not text or len(text) < 20:
            return

        try:
            score, breakdown = self.mirror.evaluate(text)

            # Detect friction vs noise
            is_friction = (
                breakdown.get('coherence', 1.0) < 0.5 and  # Low coherence
                breakdown.get('complexity', 0.0) >= 0.5 and  # But complex (not garbage)
                breakdown.get('repetition', 0.0) >= 0.5      # And not repetitive
            )

            if is_friction:
                # This is NOVEL DIVERGENCE, not a quality problem.
                # CK is computing in friction territory. Don't correct.
                # Instead, note it as a productive scrape.
                self._mirror_corrections = []
                return  # Trust CK's math here

            # Track mirror trend for actual quality issues
            trend = self.mirror.trend()
            if trend == 'declining' and score < self.mirror.threshold:
                # Genuine quality decline (not friction) -- stabilize
                from ck_sim.ck_goals import make_goal, GoalPriority
                self.goals.push(make_goal(
                    'improve_expression', GoalPriority.HOMEOSTASIS,
                    self.tick_count, source='mirror:declining',
                    pattern_name='stabilize'))

            # Store corrections for genuine quality issues only
            if score < self.mirror.threshold and not is_friction:
                suggestions = self.mirror.suggest(breakdown)
                self._mirror_corrections = suggestions
            else:
                self._mirror_corrections = []

        except Exception:
            pass

    def _emit(self, sender: str, text: str):
        """Append a message to history AND the pending-UI drain list."""
        pair = (sender, text)
        self._message_queue.append(pair)
        self._pending_ui.append(pair)

    def drain_ui_messages(self, limit: int = 5) -> list:
        """Return up to *limit* new messages for the GUI and clear them."""
        batch = self._pending_ui[:limit]
        del self._pending_ui[:limit]
        return batch

    def get_messages(self) -> list:
        """Get all queued messages for the chat screen.
        Returns list of (sender, text) tuples.
        """
        msgs = list(self._message_queue)
        return msgs

    def pop_new_messages(self) -> list:
        """Pop messages from queue (for UI consumption)."""
        msgs = list(self._message_queue)
        self._message_queue.clear()
        return msgs

    # ── Organism state accessors ──

    @property
    def emotion_primary(self) -> str:
        return self.emotion.current.primary

    @property
    def emotion_color(self) -> tuple:
        return self.emotion.emotion_color()

    @property
    def dev_stage(self) -> int:
        return self.development.stage

    @property
    def dev_stage_name(self) -> str:
        return self.development.stage_name

    @property
    def personality_mood(self) -> str:
        return self.personality.get_mood()

    @property
    def bond_stage(self) -> str:
        return self.bonding.bond_stage

    @property
    def immune_band(self) -> str:
        return self.immune.immune_band

    # ── N-Dimensional Coherence Field accessors ──

    @property
    def field_coherence(self) -> float:
        """N-dimensional field coherence [0, 1]."""
        return self.coherence_field.field_coherence

    @property
    def consensus_operator_name(self) -> str:
        """Cross-modal consensus operator name."""
        return self.coherence_field.consensus_name

    @property
    def cross_modal_crystals(self) -> list:
        """Stable cross-modal patterns."""
        return self.coherence_field.crystals

    @property
    def field_summary(self) -> str:
        """One-line field summary."""
        return self.coherence_field.summary()

    # ── Experience Lattice accessors ──

    @property
    def knowledge_count(self) -> int:
        """Total claims in truth lattice."""
        return self.truth.total_entries if self.truth else 0

    @property
    def concept_count(self) -> int:
        """Total concepts in world lattice."""
        return len(self.world.nodes) if self.world else 0

    @property
    def study_progress(self) -> str:
        """Current study status."""
        return self.actions.study_progress if self.actions else "Idle"

    @property
    def top_goal(self) -> str:
        """Current top goal name."""
        if self.goals and self.goals.top:
            return self.goals.top.name
        return "none"

    def summary(self) -> str:
        """One-line summary for console."""
        sense_bc = OP_NAMES[self.sensorium.organism_bc]
        sense_c = self.sensorium.organism_coherence
        return (f"tick={self.tick_count:6d} "
                f"B={OP_NAMES[self.phase_b]:8s} "
                f"D={OP_NAMES[self.phase_d]:8s} "
                f"BC={OP_NAMES[self.phase_bc]:8s} "
                f"C={self.coherence:.3f} "
                f"FC={self.field_coherence:.3f} "
                f"sense={sense_bc}({sense_c:.2f}) "
                f"band={self.band_name:6s} "
                f"mode={self.mode_name:12s} "
                f"breath={self.breath_phase_name:8s} "
                f"crystals={len(self.crystals)} "
                f"btq={self._btq_band} "
                f"emotion={self.emotion_primary} "
                f"stage={self.dev_stage} "
                f"knowledge={self.knowledge_count} "
                f"concepts={self.concept_count} "
                f"thought_depth={self.thinking.depth if self.thinking else 0} "
                f"thought_coh={self.thinking.avg_coherence:.3f}"
                if self.thinking else "")
