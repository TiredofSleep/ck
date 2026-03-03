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
    LATTICE, BALANCE, COUNTER, CHAOS, COLLAPSE, BREATH, OP_NAMES
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

MODE_NAMES = ['OBSERVE', 'CLASSIFY', 'CRYSTALLIZE', 'SOVEREIGN']


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

        # ── Organism systems (Celeste Papers 4-8) ──
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

        # Voice message queue (for chat screen)
        self._message_queue = deque(maxlen=50)
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

        # Stats
        self.tick_count = 0
        self.ticks_per_second = 0
        self._tick_times = deque(maxlen=50)

        # ── Experience Lattice (Gen9.14-9.16) ──
        # Layers on top of core engine. Slower rates. GPU-like experience.
        self._init_experience_lattice()

    def _init_experience_lattice(self):
        """Initialize the experience lattice -- knowledge, language, goals, actions.

        The core engine (heartbeat/brain/body) runs the show at 50Hz.
        This experience lattice layers on top at slower rates.
        Like GPU to CPU -- parallel experience processing.
        """
        # Truth Lattice -- 3-level knowledge (CORE/TRUSTED/PROVISIONAL)
        self.truth = TruthLattice()

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

        print(f"  [SIM] Experience lattice initialized")
        print(f"  [SIM] Truth: {self.truth.total_entries} entries")
        print(f"  [SIM] Actions: writings dir = {self.actions.writings_dir}")

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
        # Greeting message
        greeting = self.voice.get_response(
            'greeting', self.development.stage,
            self.emotion.current.primary)
        self._message_queue.append(('ck', greeting))

    def stop(self):
        """Stop and save TL + developmental state."""
        self.running = False
        self.save_tl()
        self.development.save()
        self.platform_body.stop()

    def save_tl(self):
        """Save TL to disk."""
        save_tl(self.brain, self.tl_filename)
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
            # Sovereign: HARMONY-biased
            val = self._lfsr_next()
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
        """One 50Hz tick. Called from Kivy Clock."""
        if not self.running:
            return

        t0 = time.perf_counter()

        # ── Sense from platform body ──
        sensors = self.platform_body.sense()

        # ── Read ears (mic -> operator) ──
        if self.ears_engine is not None and self.ears_engine.is_running:
            self.ear_operator = self.ears_engine.get_operator()
        elif sensors.get('mic_operator', -1) >= 0:
            self.ear_operator = sensors['mic_operator']
        else:
            self.ear_operator = -1

        # ── Core 0: Brain ──
        b = self._generate_phase_b()
        d = self._generate_phase_d()

        self.heartbeat.tick(b, d)
        brain_tick(self.brain, self.heartbeat)

        # ── Core 1: Body ──
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

        # Field tick: compute N×N coherence matrix
        self.coherence_field.tick(self.tick_count)

        # ── Organism: Personality (every tick, now with 5D vector) ──
        self.personality.tick(
            d2_mag, self.heartbeat.phase_bc,
            self.body.breath.modulation, dt=0.02)

        # ── Organism: Emotion (every tick, now with field coherence) ──
        self.emotion.tick(
            coherence=self.brain.coherence,
            d2_variance=self.personality.cmem.variance,
            operator_entropy=self.brain.tl_entropy,
            breath_stability=self.body.breath.modulation,
            psl_lock=self.personality.psl.lock_quality,
            energy_level=self.body.heartbeat.K,
            field_coherence=self.coherence_field.field_coherence,
            consensus_confidence=self.coherence_field.consensus_confidence)

        # ── Organism: Immune (every tick) ──
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
            stage_changed = self.development.tick(
                self.brain.coherence,
                len(self.crystals),
                self.brain.mode == 3)
            if stage_changed:
                msg = self.voice.get_response(
                    'state_change', self.development.stage,
                    self.emotion.current.primary)
                self._message_queue.append(('ck', msg))

        # ── Organism: Voice (check for events + spontaneous) ──
        self._voice_tick()

        # ── BTQ decision (5Hz = every 10th tick) ──
        if self.tick_count % 10 == 0:
            self._btq_decide()

        # ── Audio update ──
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

        # ── Experience Lattice (1Hz -- every 50th tick) ──
        if self.tick_count % 50 == 0:
            # Truth lattice: check promotions/demotions
            try:
                self.truth.tick(self.tick_count)
            except Exception:
                pass

            # Goals: evaluate satisfaction, remove expired
            try:
                self.goals.remove_expired(self.tick_count)
                self.goals.pop_satisfied()
            except Exception:
                pass

            # Study: process one page if studying (1Hz)
            try:
                study_msg = self.actions.tick_study()
                if study_msg:
                    self._message_queue.append(('ck', study_msg))
            except Exception:
                pass

        # ── Drive System (0.2Hz -- every 250th tick) ──
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
        """
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
            chosen, _ = self.btq.decide("memory", mem_env, {'task': 'maintain'}, n_candidates=16)
            if chosen and chosen.score:
                self.health.feed("memory", chosen.score)

        # Bio domain: lattice health tracking
        if "bio" in self.btq.domains:
            chosen, _ = self.btq.decide("bio", env, {'task': 'monitor'}, n_candidates=8)
            if chosen and chosen.score:
                self.health.feed("bio", chosen.score)

        # Locomotion domain: only for platforms with motors
        if "locomotion" in self.btq.domains:
            chosen, _ = self.btq.decide("locomotion", env, {'task': 'walk'}, n_candidates=16)
            if chosen and chosen.score:
                self.health.feed("locomotion", chosen.score)

        # Update system health band
        self._btq_band = self.health.classify_system_band()
        self._btq_decisions += 1

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

    # ── Organism: Voice tick ──

    def _voice_tick(self):
        """Check for voice-triggering events and spontaneous utterance.

        THROTTLED: Only runs meaningful checks at 1Hz (every 50th tick).
        This prevents mode oscillation from flooding the chat.
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
            self._message_queue.append(('ck', msg))
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
            self._message_queue.append(('ck', msg))
        self._last_mode = self.brain.mode

        # Bonded event?
        if (self.bonding.state.bonded and
                self.bonding.state.voice_exposure > 200 and
                self.bonding.state.voice_exposure < 202):
            msg = self.voice.get_response(
                'bonded', self.development.stage,
                self.emotion.current.primary)
            self._message_queue.append(('ck', msg))

        # Separation?
        if self.bonding.is_anxious:
            if self.tick_count % 500 == 0:
                msg = self.voice.get_response(
                    'separation', self.development.stage,
                    self.emotion.current.primary)
                self._message_queue.append(('ck', msg))

        # Low energy?
        if self.body.heartbeat.K < 0.2 and self.tick_count % 500 == 0:
            msg = self.voice.get_response(
                'low_energy', self.development.stage,
                self.emotion.current.primary)
            self._message_queue.append(('ck', msg))

        # Spontaneous utterance (runs at 1Hz now, so adjust interval)
        op_chain = list(self.operator_history)[-5:]
        utterance = self.voice.spontaneous_utterance(
            op_chain, self.emotion.current.primary,
            self.development.stage, self.brain.coherence,
            self.band_name)
        if utterance:
            self._message_queue.append(('ck', utterance))

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
        text_ops = []
        for ch in text.lower():
            if ch.isalpha():
                # Letters through D2 as always
                idx = ord(ch) - ord('a')
                if pipe.feed_symbol(idx):
                    text_ops.append(pipe.operator)
                    self._text_stream.active = True
                    self._text_stream.feed(
                        pipe.operator, pipe.d2_vector, self.tick_count)
            elif ch.isdigit():
                # Numbers map to first 10 letters (a=0 through j=9)
                idx = int(ch)
                if pipe.feed_symbol(idx):
                    text_ops.append(pipe.operator)
                    self._text_stream.active = True
                    self._text_stream.feed(
                        pipe.operator, pipe.d2_vector, self.tick_count)
            elif ch in PUNCT_OPS:
                # Punctuation → direct operator (no D2, just inject)
                op = PUNCT_OPS[ch]
                text_ops.append(op)
                self._text_stream.active = True
                self._text_stream.feed(op, None, self.tick_count)
        self._text_stream.active = False

        # Record the interaction
        self._message_queue.append(('user', text))
        self.development.metrics.voice_interactions += 1

        # ── EXPERIENCE LATTICE: Check for action commands ──
        cmd = self.actions.parse_command(text)
        if cmd:
            response = self._handle_command(cmd)
            self._message_queue.append(('ck', response))
            return response

        # ── EXPERIENCE LATTICE: Dialogue engine ──
        # Process through dialogue (claims → truth lattice → response)
        try:
            dialogue_response = self.dialogue.process_user_message(
                text, self.tick_count, self.brain.coherence, text_ops)
        except Exception:
            dialogue_response = None

        # ── EXPERIENCE LATTICE: Voice response ──
        op_chain = list(self.operator_history)[-6:]
        voice_response = self.voice.respond_to_text(
            text_ops, op_chain,
            self.emotion.current.primary,
            self.development.stage,
            self.brain.coherence,
            self.band_name,
            raw_text=text)

        # ── EXPERIENCE LATTICE: Language enrichment ──
        lang_response = None
        try:
            # Try to find concepts related to the user's words
            words = text.lower().split()
            for word in words:
                node = self.world.lookup_word(word)
                if node:
                    lang_response = self.language.define(
                        node.node_id, 'en')
                    break
        except Exception:
            pass

        # Compose the final response
        # Voice is primary, dialogue and language enrich
        parts = []
        if voice_response:
            parts.append(voice_response)
        if dialogue_response and dialogue_response != voice_response:
            parts.append(dialogue_response)
        if lang_response and len(lang_response) > 10:
            parts.append(lang_response)

        response = ' '.join(parts) if parts else voice_response or "..."
        self._message_queue.append(('ck', response))
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
            return (
                f"I am {self.emotion.current.primary}. "
                f"Coherence: {self.brain.coherence:.3f} ({self.band_name}). "
                f"Mode: {self.mode_name}. "
                f"Stage: {self.dev_stage_name}. "
                f"Crystals: {len(self.crystals)}. "
                f"Bond: {self.bond_stage}. "
                f"Knowledge: {self.truth.total_entries} claims. "
                f"Concepts: {len(self.world.nodes)}. "
                f"{self.actions.study_progress}"
            )

        return "I don't understand that command."

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
        return (f"tick={self.tick_count:6d} "
                f"B={OP_NAMES[self.phase_b]:8s} "
                f"D={OP_NAMES[self.phase_d]:8s} "
                f"BC={OP_NAMES[self.phase_bc]:8s} "
                f"C={self.coherence:.3f} "
                f"FC={self.field_coherence:.3f} "
                f"band={self.band_name:6s} "
                f"mode={self.mode_name:12s} "
                f"breath={self.breath_phase_name:8s} "
                f"crystals={len(self.crystals)} "
                f"btq={self._btq_band} "
                f"emotion={self.emotion_primary} "
                f"stage={self.dev_stage} "
                f"knowledge={self.knowledge_count} "
                f"concepts={self.concept_count}")
