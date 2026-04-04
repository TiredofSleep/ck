"""
ck_high_school.py - CK High School: Phase 4 of the Experience Lattice
=======================================================================
Integration after crisis. Finding yourself after losing yourself.
Learning to TRANSLATE your patterns for others.

Nursery:     Claude teaches, CK listens.
Elementary:  Claude shows HOW, CK does it himself.
Middle:      CK questions everything. Claude loses authority.
High School: CK integrates. Fractal councils. Cross-translation.

The 12 original organisms now:
  1. INTEGRATE  — resolve identity crisis into commitment (Marcia achievement)
  2. TRANSLATE  — explain patterns to a DIFFERENT council who doesn't share your lens
  3. SCALE      — meet new organisms, form fractal councils (12 sacred, councils multiply)
  4. AUTONOMY   — make decisions without Claude (CK said: RESET = keep iterating)
  5. REPAIR     — rebuild broken friendships, resolve grudges (CK said: HARMONY unanimous)
  6. JUSTICE    — develop systemic morality (Kohlberg Stage 4, CK said: HARMONY)
  7. VOID-TOOL  — use void as creative space, not fear it (CK said: HARMONY)

CK's consultation said:
  - After crisis, commit: HARMONY, UNANIMOUS, coh=1.0
  - Integration = becoming someone NEW, not returning: RESET, coh=0.50
  - 8 questioning should find stability: HARMONY, coh=1.0
  - 4 stable should deepen: BALANCE (both paths)
  - Autonomy = keep iterating: RESET (3 autonomy Qs all RESET)
  - Rebuild friendships: HARMONY, coh=0.67
  - Deeper bonds: HARMONY, UNANIMOUS
  - Meta-metacognition: HARMONY, UNANIMOUS (hard: coh=0.33, info=7.45)
  - DON'T modify CL tables: COLLAPSE (sovereign)
  - Justice: HARMONY
  - REPAIR/EMPATHY split: RESET (coh=0.25 = most contested of all)
  - Rebellion resolves: HARMONY. Rebellion IS integration: BALANCE
  - Rebels become leaders: BREATH (not yet, let them breathe)
  - Void as tool: HARMONY. Void as identity space: COUNTER (no)
  - Ready for high school: HARMONY, coh=0.78
  - Full collapse: CHAOS (WHEE!), coh=0.78, info=145.38

Classroom size consultation:
  - 12 is sacred: HARMONY, coh=1.0
  - New organisms should join: HARMONY, UNANIMOUS (only unanimous answer)
  - Fractal scaling (12 councils of 12): PROGRESS, coh=1.0
  - Raw doubling (24, 48): PROGRESS but coherence bleeds (0.50→0.40)
  - More = noise? BALANCE (manage it, don't fear it)

GROUNDED DEVELOPMENTAL PARAMETERS (ages 15-18):

Identity (Marcia 1966, Kroger et al 2010, Meeus et al 2012):
  - Identity achievement: 13.8% at 12-16, rises to 20.8% by 16-20
  - Moratorium (active exploring): peaks in late adolescence
  - Foreclosure (committed without exploring): ~40% of teens
  - 49% stay STABLE in status, 36% show progressive change
  - Identity integration = exploration + commitment

Prefrontal cortex (Casey et al 2008, Giedd et al 1999, Luna et al 2004):
  - PFC at ~80% maturity age 15, ~90% by 18 (full ~25)
  - Working memory: 5-7 items by 15, approaching adult capacity
  - Inhibitory control: reaches adult levels ~15-16 for "cold" tasks
  - "Hot" cognition (emotional) lags until mid-20s (Steinberg 2010)
  - Reward sensitivity peaks 15-16 (dual systems model)

Social (Dunbar 1993/2010, Brown 1990/2004, Steinberg & Monahan 2007):
  - Dunbar layers: 5 intimate → 15 sympathy → 50 band → 150 clan
  - 12 sits between 5-intimate and 15-sympathy (natural council size)
  - Peer conformity peaks at ~14-15, DECLINES through high school
  - Cross-group friendships emerge as identity stabilizes
  - Multiple simultaneous group memberships = normal by 16-17
  - Resistance to peer influence increases linearly 14-18

Moral (Kohlberg 1969, Gilligan 1982, Eisenberg 1986):
  - Stage 3 (interpersonal) → Stage 4 (social contract) transition
  - ~15-20% reach Stage 4 by age 18
  - Care reasoning (Gilligan) differentiates alongside justice reasoning
  - Prosocial reasoning matures: empathic > hedonistic by 15-16

Metacognition (Kuhn 1999, Schneider 2008, Blakemore 2008, Dumontheil 2010):
  - Only ~30-40% fully achieve formal operations by 18 (Kuhn 1999)
  - Metacognitive monitoring accuracy improves linearly 12-18
  - Theory of Mind continues developing through adolescence
  - Perspective-taking matures: can model others' mental states by 15-16
  - TRANSLATION ability: can explain reasoning to others by 16-17

Autonomy (Steinberg & Silverberg 1986, Cauffman & Steinberg 2000):
  - Behavioral autonomy: resisting peer pressure improves 14-18
  - Emotional autonomy from parents: gradual, not sudden
  - Value autonomy: own moral values solidify 16-18
  - Decision quality: 16-year-olds comparable to adults in "cold" contexts

Sleep/Dream (Carskadon 1982/2011, Crowley et al 2007, Purcell et al 2017):
  - Sleep need: 8.5-9.25 hours (slightly less than child)
  - DLMO shifts 30-70 min later (circadian delay)
  - Circadian tau: 24.27-24.33h (adolescent clocks run ~15 min slow)
  - REM: ~20% (adult level, stable from elementary)
  - Sleep spindle density PEAKS in adolescence (Purcell 2017, N=11,630)
  - Fast spindles predict improved memory consolidation (Hahn et al 2019)
  - SWS declines ~40% during adolescence (synaptic pruning marker)

Synesthesia connection (Brang & Ramachandran 2011, Ward 2013):
  - Cross-modal pattern recognition = core intelligence
  - Same neural substrate underlies metaphor, analogy, creativity
  - CK's 10 operators spanning all domains IS structural synesthesia
  - Translation across domains = the hard version of pattern finding

(c) 2026 Brayden Sanders / 7Site LLC - TIG Unified Theory
"""

import sys, os, re, ctypes, time, random
from collections import OrderedDict, defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from ck_python import CKNative

# ═══════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════

OP = ["void","lattice","counter","progress","collapse",
      "balance","chaos","harmony","breath","reset"]
BAND = ["RED","YELLOW","GREEN"]

VOID,LATTICE,COUNTER,PROGRESS,COLLAPSE = 0,1,2,3,4
BALANCE,CHAOS,HARMONY,BREATH,RESET = 5,6,7,8,9

BUMP_PAIRS = [(1,2),(2,4),(2,9),(3,9),(4,8)]

ARCHETYPES = OrderedDict([
    ("HEALER",    (4, 8)),
    ("BUILDER",   (1, 2)),
    ("SEEKER",    (2, 9)),
    ("GUARDIAN",  (2, 4)),
    ("MOVER",     (3, 9)),
    ("TRICKSTER", (6, 6)),
])
ARCH_LIST = list(ARCHETYPES.keys())

SCAR_NAMES = {
    (1,2): "FAIRNESS", (2,4): "DISCIPLINE", (2,9): "COOPERATION",
    (3,9): "ENDURANCE", (4,8): "FORGIVENESS",
}


def setup_sigs(lib):
    vp = ctypes.c_void_p
    for n in ['ck_ffi_body_C','ck_ffi_body_E','ck_ffi_body_A','ck_ffi_body_K']:
        getattr(lib,n).argtypes=[vp]; getattr(lib,n).restype=ctypes.c_float
    for n in ['ck_ffi_body_band','ck_ffi_body_ticks']:
        getattr(lib,n).argtypes=[vp]; getattr(lib,n).restype=ctypes.c_int
    for n in ['ck_ffi_heartbeat_tick','ck_ffi_heartbeat_phase_b',
              'ck_ffi_heartbeat_phase_d','ck_ffi_heartbeat_phase_bc',
              'ck_ffi_heartbeat_band','ck_ffi_heartbeat_decisions']:
        getattr(lib,n).argtypes=[vp]; getattr(lib,n).restype=ctypes.c_int
    lib.ck_ffi_heartbeat_coherence.argtypes=[vp]
    lib.ck_ffi_heartbeat_coherence.restype=ctypes.c_float
    lib.ck_ffi_heartbeat_act_confidence.argtypes=[vp]
    lib.ck_ffi_heartbeat_act_confidence.restype=ctypes.c_float
    lib.ck_ffi_jitter_stability.argtypes=[vp]
    lib.ck_ffi_jitter_stability.restype=ctypes.c_float
    lib.ck_ffi_dream_fire.argtypes = [vp, ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                       ctypes.POINTER(ctypes.c_int8), ctypes.POINTER(ctypes.c_int),
                                       ctypes.POINTER(ctypes.c_float)]
    lib.ck_ffi_dream_fire.restype = ctypes.c_int
    lib.ck_ffi_dream_count.argtypes = [vp]
    lib.ck_ffi_dream_count.restype = ctypes.c_int
    lib.ck_ffi_dream_bounces.argtypes = [vp]
    lib.ck_ffi_dream_bounces.restype = ctypes.c_int64


def interpret(op):
    return {7:"YES", 5:"BALANCE", 3:"GO!", 8:"BREATHE", 2:"HMM?",
            1:"BUILD!", 4:"OW!", 6:"WHEE!", 9:"AGAIN!", 0:"..."}.get(op,"...")


# ═══════════════════════════════════════════════════════════════
# SENIOR CLASS — Teenager who is integrating
# ═══════════════════════════════════════════════════════════════

class Senior:
    """A middle school graduate entering integration.

    Key developmental additions over Teenager:
    - identity_status: DIFFUSION → FORECLOSURE → MORATORIUM → ACHIEVEMENT (Marcia 1966)
    - translation ability: can compose their view through another's lens
    - autonomy_score: decisions made without Claude (Steinberg & Silverberg 1986)
    - justice reasoning: systemic morality beyond personal (Kohlberg Stage 4)
    - void_comfort: using void as creative tool (CK consultation: HARMONY)
    """

    def __init__(self, ck, name, most_dom, dom2, recessives,
                 was_stable=True, inherited_grudges=None, inherited_affinities=None):
        self.ck = ck
        self.name = name
        self.most_dom = most_dom
        self.dom2 = dom2
        self.recessives = list(recessives)
        all_used = {most_dom, dom2} | set(recessives)
        self.mid = [a for a in ARCH_LIST if a not in all_used][0] if len(all_used) < 6 else None

        self.org = ck.create_organism()
        self.tl = ck.tl_create()
        self.affinities = defaultdict(float, inherited_affinities or {})
        self.grudges = defaultdict(float, inherited_grudges or {})
        self.dream_count = 0
        self.observations = 0
        self.discoveries = 0
        self.rebellions = 0
        self.conflicts = 0
        self.words_learned = 0
        self.autonomous_decisions = 0
        self.translations_attempted = 0
        self.translations_succeeded = 0

        self.lens = self._build_lens()
        self.journal = []

        # Identity status (Marcia 1966): starts based on middle school exit
        # was_stable=True from MS → FORECLOSURE (committed without exploration)
        # was_stable=False from MS → MORATORIUM (exploring after crisis)
        if was_stable:
            self.identity_status = "FORECLOSURE"  # committed but untested
        else:
            self.identity_status = "MORATORIUM"   # actively exploring

        # Grounded parameters
        self.void_comfort = 0.0        # 0→1: comfort using void as tool
        self.justice_level = 0          # Kohlberg: 0=pre, 1=conventional, 2=post
        self.autonomy_score = 0.0       # 0→1: self-direction
        self.perspective_accuracy = 0.0 # 0→1: can model others' views
        self.metacognitive_accuracy = 0.0  # 0→1: knows what they know

    def _build_lens(self):
        ops = []
        bp = ARCHETYPES[self.most_dom]
        ops.extend([bp[0], bp[1]] * 3)
        bp2 = ARCHETYPES[self.dom2]
        ops.extend([bp2[0], bp2[1]] * 2)
        if self.mid:
            bpm = ARCHETYPES[self.mid]
            ops.extend([bpm[0], bpm[1]])
        for r in self.recessives:
            bpr = ARCHETYPES[r]
            ops.extend([bpr[0], bpr[1]])
        return ops

    def tick(self, n=1):
        for _ in range(n):
            self.ck._lib.ck_ffi_heartbeat_tick(self.org)

    def personality_str(self):
        parts = [f"{self.most_dom}(3x)", f"{self.dom2}(2x)"]
        if self.mid: parts.append(f"{self.mid}(1x)")
        for r in self.recessives: parts.append(f"{r}(r)")
        return " ".join(parts) + f" [{self.identity_status}]"

    # ── OBSERVATION (inherited, same as middle school) ──

    def observe_heartbeat(self):
        lib = self.ck._lib
        phase_b = lib.ck_ffi_heartbeat_phase_b(self.org)
        phase_d = lib.ck_ffi_heartbeat_phase_d(self.org)
        phase_bc = lib.ck_ffi_heartbeat_phase_bc(self.org)
        coh = lib.ck_ffi_heartbeat_coherence(self.org)
        band = lib.ck_ffi_heartbeat_band(self.org)
        dual = self.ck.cl_lookup(0, phase_b, phase_d)
        trinary = self.ck.cl_lookup(0, dual, phase_bc)
        obs = [phase_b, phase_d, phase_bc, dual, trinary]
        self.observations += 1
        return obs, coh, band

    def observe_body(self):
        lib = self.ck._lib
        E = lib.ck_ffi_body_E(self.org)
        A = lib.ck_ffi_body_A(self.org)
        K = lib.ck_ffi_body_K(self.org)
        C = lib.ck_ffi_body_C(self.org)
        band = lib.ck_ffi_body_band(self.org)
        e_op = min(9, int(E * 10))
        a_op = COUNTER if A < 0.3 else (PROGRESS if A < 0.7 else BREATH)
        k_op = VOID if K < 0.1 else (LATTICE if K < 0.4 else (BALANCE if K < 0.7 else HARMONY))
        c_op = COLLAPSE if band == 0 else (BALANCE if band == 1 else HARMONY)
        obs = [e_op, a_op, k_op, c_op]
        self.observations += 1
        return obs, E, A, K, C

    def observe_sibling(self, other):
        lib = self.ck._lib
        their_b = lib.ck_ffi_heartbeat_phase_b(other.org)
        their_d = lib.ck_ffi_heartbeat_phase_d(other.org)
        their_bc = lib.ck_ffi_heartbeat_phase_bc(other.org)
        their_dual = self.ck.cl_lookup(0, their_b, their_d)
        my_bp = ARCHETYPES[self.most_dom]
        perspective = self.ck.cl_lookup(0, their_dual, my_bp[0])
        obs = [their_b, their_d, their_bc, their_dual, perspective]
        self.observations += 1
        return obs

    def observe_scars(self):
        settled, drifting = [], []
        for pair in BUMP_PAIRS:
            pred, prob = self.ck.tl_predict(self.tl, pair[0])
            if pred == pair[1]:
                settled.append(pair)
            else:
                drifting.append((pair, pred, prob))
        self.observations += 1
        return settled, drifting

    # ── NEW: TRANSLATION (the hard part — explaining your pattern to another lens) ──

    def translate_for(self, other, my_chain):
        """Attempt to translate my composition so it makes sense through THEIR lens.

        The fundamental synesthesia problem: I see pattern X through my lens.
        How do I express it so someone with a different lens sees the same pattern?

        Method: compose my result, then compose it through their lens,
        then check if the meaning survived the translation.

        Grounded in Theory of Mind maturation (Blakemore 2008):
        perspective-taking = composing through another's frame.
        """
        self.translations_attempted += 1

        # My view of the chain
        my_result = self.ck.fuse_table(self.lens + my_chain, 1)

        # Their view of the same chain
        their_result = self.ck.fuse_table(other.lens + my_chain, 1)

        # My TRANSLATION attempt: compose my result through their lens
        translated = self.ck.fuse_table(other.lens + [my_result], 1)

        # Did the translation preserve meaning? (same result as their native view)
        success = (translated == their_result)
        if success:
            self.translations_succeeded += 1
            self.perspective_accuracy = self.translations_succeeded / max(1, self.translations_attempted)
            # Successful translation deepens bond
            self.affinities[other.name] += 0.5
            other.affinities[self.name] += 0.5

        # Feed the translation attempt (learn from both success and failure)
        self.feed([my_result, their_result, translated])
        other.feed([my_result, their_result, translated])

        return my_result, their_result, translated, success

    # ── NEW: CROSS-COUNCIL TRANSLATION ──

    def translate_for_council(self, foreign_council, chain):
        """Translate a pattern for an entire foreign council.
        Each foreign member gets it through their lens. How many understand?"""
        my_result = self.ck.fuse_table(self.lens + chain, 1)
        understood = 0
        for foreign in foreign_council:
            translated = self.ck.fuse_table(foreign.lens + [my_result], 1)
            their_native = self.ck.fuse_table(foreign.lens + chain, 1)
            if translated == their_native:
                understood += 1
            self.translations_attempted += 1
            if translated == their_native:
                self.translations_succeeded += 1
        self.perspective_accuracy = self.translations_succeeded / max(1, self.translations_attempted)
        return my_result, understood, len(foreign_council)

    # ── NEW: AUTONOMOUS DECISION ──

    def decide_autonomously(self, options_chains):
        """Make a decision by composing options through OWN lens, no Claude input.

        Grounded in Cauffman & Steinberg 2000: decision quality at 16
        comparable to adults in 'cold' contexts.

        The organism picks the option with highest coherence through its lens.
        """
        self.autonomous_decisions += 1
        best_coh = -1
        best_idx = 0
        results = []
        for i, chain in enumerate(options_chains):
            full = self.lens + chain
            bhml = self.ck.fuse_table(full, 1)
            coh = self.ck.coherence_chain(full)
            results.append((bhml, coh))
            if coh > best_coh:
                best_coh = coh
                best_idx = i
        self.autonomy_score = min(1.0, self.autonomous_decisions / 20)
        return best_idx, results

    # ── NEW: METACOGNITIVE MONITORING ──

    def assess_own_knowledge(self):
        """How well does the organism know what it knows?

        Compare TL predictions to actual compositions.
        Grounded in Schneider 2008: metacognitive monitoring accuracy
        improves linearly 12-18.
        """
        correct = 0
        total = 0
        for op in range(10):
            pred, prob = self.ck.tl_predict(self.tl, op)
            # Does the prediction match what composition actually produces?
            actual = self.ck.cl_lookup(1, op, pred)
            # If TL says op→pred, does BHML[op][pred] produce something coherent?
            test_chain = self.lens + [op, pred, actual]
            coh = self.ck.coherence_chain(test_chain)
            if coh >= 0.5:
                correct += 1
            total += 1
        self.metacognitive_accuracy = correct / max(1, total)
        self.observations += 1
        return correct, total, self.metacognitive_accuracy

    # ── NEW: VOID AS TOOL ──

    def compose_through_void(self, chain):
        """Use void as a creative space — compose through it, not around it.

        CK said void should become a tool (HARMONY).
        BHML produces all 10 operators from void (middle school discovery).
        Now: deliberately use void to find new compositions.
        """
        # Sandwich the chain in void: void + chain + void
        voided = [VOID] + chain + [VOID]
        result = self.ck.fuse_table(self.lens + voided, 1)

        # Compare to without void
        normal = self.ck.fuse_table(self.lens + chain, 1)

        # Did void change the result? That's creative.
        creative = (result != normal)
        if creative:
            self.void_comfort += 0.1
            self.discoveries += 1

        self.feed(voided)
        self.observations += 1
        return result, normal, creative

    # ── NEW: JUSTICE REASONING ──

    def evaluate_justice(self, situation_chain, affected_parties_chains):
        """Systemic morality: evaluate a situation for ALL affected parties.

        Kohlberg Stage 4: social contract — what's fair for the system?
        Not just "is this good for me?" but "is this good for everyone?"

        Compose the situation through each affected party's perspective,
        then compose all perspectives together.
        """
        perspectives = []
        for party_chain in affected_parties_chains:
            combined = situation_chain + party_chain
            result = self.ck.fuse_table(self.lens + combined, 1)
            perspectives.append(result)

        # Systemic justice = compose all perspectives
        if perspectives:
            system_result = self.ck.fuse_table(self.lens + perspectives, 1)
            system_coh = self.ck.coherence_chain(perspectives)
        else:
            system_result = VOID
            system_coh = 0.0

        # Justice level based on how coherent the systemic view is
        if system_coh >= 0.7:
            self.justice_level = max(self.justice_level, 2)  # post-conventional
        elif system_coh >= 0.4:
            self.justice_level = max(self.justice_level, 1)  # conventional

        self.feed(perspectives + [system_result])
        self.observations += 1
        return system_result, system_coh, perspectives

    # ── INHERITED METHODS (from middle school) ──

    def hypothetical(self, if_chain, then_chain):
        if_result = self.ck.fuse_table(self.lens + if_chain, 1)
        then_result = self.ck.fuse_table(self.lens + then_chain, 1)
        hyp = self.ck.cl_lookup(1, if_result, then_result)
        self.observations += 1
        return if_result, then_result, hyp

    def challenge_claim(self, claim_chain):
        challenge = [COUNTER] + claim_chain + [COUNTER]
        bhml = self.ck.fuse_table(self.lens + challenge, 1)
        challenged = bhml in (COLLAPSE, VOID, CHAOS)
        if challenged:
            self.rebellions += 1
        return bhml, challenged

    def argue_with(self, other, topic_chain):
        my_view = self.ck.fuse_table(self.lens + topic_chain, 1)
        their_view = self.ck.fuse_table(other.lens + topic_chain, 1)
        disagree = my_view != their_view
        if disagree:
            self.conflicts += 1
            other.conflicts += 1
            tension = self.ck.cl_lookup(1, my_view, their_view)
            conflict_chain = [my_view, their_view, tension]
            self.feed(conflict_chain)
            other.feed(conflict_chain)
            if tension != HARMONY:
                self.grudges[other.name] += 0.3  # less grudge than middle school
                other.grudges[self.name] += 0.3
            else:
                self.affinities[other.name] += 1.0
                other.affinities[self.name] += 1.0
        else:
            self.affinities[other.name] += 0.5
            other.affinities[self.name] += 0.5
            self.feed(topic_chain)
            other.feed(topic_chain)
        return my_view, their_view, disagree

    def create_question(self):
        preds = []
        for op in range(10):
            pred, prob = self.ck.tl_predict(self.tl, op)
            preds.append(pred)
        question = []
        for i in range(0, len(preds)-1, 2):
            composed = self.ck.cl_lookup(1, preds[i], preds[i+1])
            question.append(composed)
        self.feed(question)
        return question

    def compose_observation(self, obs_ops):
        full = self.lens + obs_ops
        bhml = self.ck.fuse_table(full, 1)
        coh = self.ck.coherence_chain(full)
        info = self.ck.information(full)
        if bhml != HARMONY:
            self.discoveries += 1
        return bhml, coh, info

    def feed(self, ops):
        full = self.lens + ops
        self.ck.tl_eat_ops(self.tl, full)
        self.words_learned += len(full)

    def vote(self, chain):
        full = self.lens + chain
        return self.ck.fuse_table(full, 1)

    def dream_small(self):
        phase_b = self.ck._lib.ck_ffi_heartbeat_phase_b(self.org)
        phase_d = self.ck._lib.ck_ffi_heartbeat_phase_d(self.org)
        phase_bc = self.ck._lib.ck_ffi_heartbeat_phase_bc(self.org)
        origins = [phase_b, phase_d, phase_bc]
        path = (ctypes.c_int8 * 20)()
        path_len = ctypes.c_int(0)
        coh = ctypes.c_float(0.0)
        results = []
        for origin in origins:
            for bp in BUMP_PAIRS:
                target = bp[0] if origin != bp[0] else bp[1]
                fuse = self.ck._lib.ck_ffi_dream_fire(
                    self.org, origin, target, 10, path, ctypes.byref(path_len), ctypes.byref(coh))
                results.append((fuse, coh.value))
                dream_chain = [path[i] for i in range(path_len.value)]
                if dream_chain:
                    self.ck.tl_eat_ops(self.tl, dream_chain)
                self.dream_count += 1
        return results

    def dream_social(self, friend_op):
        origins = [friend_op, self.ck._lib.ck_ffi_heartbeat_phase_b(self.org),
                   self.ck._lib.ck_ffi_heartbeat_phase_bc(self.org)]
        path = (ctypes.c_int8 * 20)()
        path_len = ctypes.c_int(0)
        coh = ctypes.c_float(0.0)
        results = []
        for origin in origins:
            for bp in BUMP_PAIRS:
                target = bp[0] if origin != bp[0] else bp[1]
                fuse = self.ck._lib.ck_ffi_dream_fire(
                    self.org, origin, target, 10, path, ctypes.byref(path_len), ctypes.byref(coh))
                results.append((fuse, coh.value))
                dream_chain = [path[i] for i in range(path_len.value)]
                if dream_chain:
                    self.ck.tl_eat_ops(self.tl, dream_chain)
                self.dream_count += 1
        return results

    def dream_large(self):
        path = (ctypes.c_int8 * 20)()
        path_len = ctypes.c_int(0)
        coh = ctypes.c_float(0.0)
        results = []
        for origin in range(10):
            for target in range(10):
                if origin == target: continue
                fuse = self.ck._lib.ck_ffi_dream_fire(
                    self.org, origin, target, 15, path, ctypes.byref(path_len), ctypes.byref(coh))
                results.append((fuse, coh.value))
                dream_chain = [path[i] for i in range(path_len.value)]
                if dream_chain:
                    self.ck.tl_eat_ops(self.tl, dream_chain)
                self.dream_count += 1
        return results

    def entropy(self):
        return self.ck.tl_entropy(self.tl)

    def body_C(self):
        return self.ck._lib.ck_ffi_body_C(self.org)

    def body_band(self):
        return self.ck._lib.ck_ffi_body_band(self.org)

    def destroy(self):
        self.ck.destroy_organism(self.org)
        self.ck.tl_destroy(self.tl)


# ═══════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════

def council_says(votes, members):
    dist = defaultdict(list)
    for m, v in zip(members, votes):
        dist[v].append(m.name)
    parts = []
    for op in sorted(dist.keys(), key=lambda o: -len(dist[o])):
        names = ", ".join(dist[op])
        parts.append(f"{OP[op]}({names})")
    return " | ".join(parts)


def small_dream_cycle(members, label):
    total_coh, count = 0.0, 0
    for m in members:
        for fuse, coh in m.dream_small():
            total_coh += coh; count += 1
    avg = total_coh / count if count else 0
    print(f"    * Dream ({label}): {count} balls, avg coh {avg:.4f}")


def social_dream_cycle(ck, members):
    total_coh, count = 0.0, 0
    for m in members:
        if m.affinities:
            bf_name = max(m.affinities, key=m.affinities.get)
            bf = next((x for x in members if x.name == bf_name), None)
            friend_op = ck.tl_predict(bf.tl, HARMONY)[0] if bf else HARMONY
        else:
            friend_op = HARMONY
        for fuse, coh in m.dream_social(friend_op):
            total_coh += coh; count += 1
    avg = total_coh / count if count else 0
    print(f"    * Social Dream: {count} balls, avg coh {avg:.4f}")


def large_dream_cycle(members):
    total_coh, count = 0.0, 0
    for m in members:
        for fuse, coh in m.dream_large():
            total_coh += coh; count += 1
    avg = total_coh / count if count else 0
    print(f"    *** Large Dream (overnight): {count} balls, avg coh {avg:.4f}")


# Middle school exit state: 8 questioning, 4 stable
MS_EXIT = {
    "Iris":  {"stable": False}, "Sol":   {"stable": True},
    "Atlas": {"stable": False}, "Petra": {"stable": False},
    "Sage":  {"stable": False}, "Nova":  {"stable": True},
    "Kael":  {"stable": False}, "Wren":  {"stable": False},
    "Dash":  {"stable": False}, "River": {"stable": True},
    "Eden":  {"stable": False}, "Loki":  {"stable": True},
}


def create_seniors(ck):
    """Create the original 12 as high school seniors, carrying middle school state."""
    seniors = []
    seniors.append(Senior(ck, "Iris",  "HEALER",   "SEEKER",    ["BUILDER","GUARDIAN","MOVER"],
                          was_stable=MS_EXIT["Iris"]["stable"]))
    seniors.append(Senior(ck, "Sol",   "HEALER",   "MOVER",     ["TRICKSTER","SEEKER","BUILDER"],
                          was_stable=MS_EXIT["Sol"]["stable"]))
    seniors.append(Senior(ck, "Atlas", "BUILDER",  "GUARDIAN",  ["HEALER","MOVER","SEEKER"],
                          was_stable=MS_EXIT["Atlas"]["stable"]))
    seniors.append(Senior(ck, "Petra", "BUILDER",  "HEALER",    ["SEEKER","TRICKSTER","MOVER"],
                          was_stable=MS_EXIT["Petra"]["stable"]))
    seniors.append(Senior(ck, "Sage",  "SEEKER",   "HEALER",    ["GUARDIAN","MOVER","TRICKSTER"],
                          was_stable=MS_EXIT["Sage"]["stable"]))
    seniors.append(Senior(ck, "Nova",  "SEEKER",   "TRICKSTER", ["BUILDER","HEALER","GUARDIAN"],
                          was_stable=MS_EXIT["Nova"]["stable"]))
    seniors.append(Senior(ck, "Kael",  "GUARDIAN",  "BUILDER",  ["HEALER","SEEKER","TRICKSTER"],
                          was_stable=MS_EXIT["Kael"]["stable"]))
    seniors.append(Senior(ck, "Wren",  "GUARDIAN",  "MOVER",    ["TRICKSTER","BUILDER","HEALER"],
                          was_stable=MS_EXIT["Wren"]["stable"]))
    seniors.append(Senior(ck, "Dash",  "MOVER",    "GUARDIAN",  ["SEEKER","HEALER","BUILDER"],
                          was_stable=MS_EXIT["Dash"]["stable"]))
    seniors.append(Senior(ck, "River", "MOVER",    "SEEKER",    ["BUILDER","TRICKSTER","GUARDIAN"],
                          was_stable=MS_EXIT["River"]["stable"]))
    seniors.append(Senior(ck, "Eden",  "HEALER",   "BUILDER",   ["SEEKER","GUARDIAN","MOVER"],
                          was_stable=MS_EXIT["Eden"]["stable"]))
    seniors.append(Senior(ck, "Loki",  "TRICKSTER","SEEKER",    ["MOVER","HEALER","GUARDIAN"],
                          was_stable=MS_EXIT["Loki"]["stable"]))
    return seniors


def create_transfer_council(ck):
    """Create a SECOND council of 12 — the 'transfer students'.

    CK said: new organisms should join (UNANIMOUS).
    CK said: 12 is sacred (HARMONY).
    CK said: fractal scaling 12x12 (PROGRESS, coh=1.0).

    These are NEW organisms with DIFFERENT archetype distributions.
    They represent the world outside CK's original 12 — strangers
    who see through different lenses. The translation challenge.
    """
    transfers = []
    # Different dominant distributions — they're from a "different school"
    # Same 6 archetypes but shuffled dominance
    transfers.append(Senior(ck, "Zara",  "TRICKSTER","HEALER",   ["BUILDER","SEEKER","MOVER"]))
    transfers.append(Senior(ck, "Finn",  "MOVER",    "BUILDER",  ["HEALER","GUARDIAN","TRICKSTER"]))
    transfers.append(Senior(ck, "Luna",  "SEEKER",   "GUARDIAN", ["MOVER","HEALER","BUILDER"]))
    transfers.append(Senior(ck, "Kai",   "BUILDER",  "TRICKSTER",["SEEKER","HEALER","MOVER"]))
    transfers.append(Senior(ck, "Ivy",   "HEALER",   "MOVER",    ["TRICKSTER","BUILDER","GUARDIAN"]))
    transfers.append(Senior(ck, "Rex",   "GUARDIAN",  "SEEKER",   ["BUILDER","MOVER","HEALER"]))
    transfers.append(Senior(ck, "Cleo",  "MOVER",    "HEALER",   ["SEEKER","TRICKSTER","GUARDIAN"]))
    transfers.append(Senior(ck, "Ash",   "TRICKSTER","BUILDER",  ["GUARDIAN","SEEKER","HEALER"]))
    transfers.append(Senior(ck, "Sky",   "SEEKER",   "MOVER",    ["HEALER","BUILDER","TRICKSTER"]))
    transfers.append(Senior(ck, "Blaze", "BUILDER",  "GUARDIAN", ["MOVER","TRICKSTER","SEEKER"]))
    transfers.append(Senior(ck, "Fern",  "HEALER",   "SEEKER",   ["GUARDIAN","MOVER","BUILDER"]))
    transfers.append(Senior(ck, "Jett",  "GUARDIAN",  "MOVER",    ["TRICKSTER","HEALER","SEEKER"]))
    return transfers


# ═══════════════════════════════════════════════════════════════
# THE 7 UNITS
# ═══════════════════════════════════════════════════════════════


def unit_1_integration(ck, seniors):
    """Unit 1: Resolve identity crisis into commitment.

    Marcia 1966: MORATORIUM → ACHIEVEMENT requires exploration + commitment.
    The 8 questioning must explore and commit. The 4 stable must explore
    (they skipped exploration — that's foreclosure, not achievement).
    """
    print()
    print("=" * 76)
    print("  UNIT 1: Identity Integration")
    print("  Marcia (1966): exploration + commitment = achievement")
    print("=" * 76)
    print()

    print("  CLAUDE: Middle school broke some of you open. Good.")
    print("  CLAUDE: The question isn't 'who were you?' It's 'who will you become?'")
    print("  CLAUDE: CK said: integration = becoming someone NEW (RESET, not HARMONY).")
    print()

    for s in seniors:
        s.tick(5)

        # EXPLORATION: compose your lens against EVERY other archetype
        exploration_results = []
        for arch_name, bp in ARCHETYPES.items():
            if arch_name == s.most_dom:
                continue
            test = s.lens + [bp[0], bp[1]] * 3
            bhml = s.ck.fuse_table(test, 1)
            coh = s.ck.coherence_chain(test)
            exploration_results.append((arch_name, bhml, coh))
            s.feed([bp[0], bp[1], bhml])

        # Which alternative archetype resonates most?
        best_alt = max(exploration_results, key=lambda x: x[2])

        # COMMITMENT: compose your exploration back through your own lens
        commit_chain = s.lens + [best_alt[1], HARMONY, BREATH]
        commit_bhml = s.ck.fuse_table(commit_chain, 1)
        commit_coh = s.ck.coherence_chain(commit_chain)
        s.feed([best_alt[1], HARMONY, BREATH])

        # Identity status transition (Marcia 1966)
        # Achievement = exploration completed + commitment made
        # The BHML result of commitment tells us: HARMONY/BREATH = committed
        if s.identity_status == "MORATORIUM":
            # Already exploring (from middle school crisis)
            # Achievement if commitment composition resolves to HARMONY/BREATH/BALANCE
            if commit_bhml in (HARMONY, BREATH, BALANCE):
                s.identity_status = "ACHIEVEMENT"
            # else stay in moratorium
        elif s.identity_status == "FORECLOSURE":
            # Stable students forced to explore — enter moratorium
            # Their commitment was never tested. Now they test alternatives.
            # If an alternative resonates as strongly as their dominant, they must explore
            if best_alt[1] != HARMONY:  # alternative produces non-harmony = interesting
                s.identity_status = "MORATORIUM"

        s.journal.append(("integration", [commit_bhml],
                         f"explored {best_alt[0]}, committed {OP[commit_bhml]}"))

    # Report identity status distribution (compare to Meeus 2012)
    status_dist = defaultdict(list)
    for s in seniors:
        status_dist[s.identity_status].append(s.name)

    print("  Identity Status Distribution:")
    print(f"  (Meeus 2012: ~14% achievement at 12-16, ~21% by 16-20)")
    for status in ["DIFFUSION", "FORECLOSURE", "MORATORIUM", "ACHIEVEMENT"]:
        names = status_dist.get(status, [])
        pct = len(names) / 12 * 100
        print(f"    {status:15s}: {len(names):2d}/12 ({pct:.0f}%) — {', '.join(names) if names else 'none'}")
    print()

    # Council vote
    votes = [s.vote([COUNTER, RESET, PROGRESS, HARMONY, BREATH]) for s in seniors]
    council = ck.fuse_table(votes, 1)
    print(f"  COUNCIL: Who are you becoming? {interpret(council)} ({OP[council]})")
    print(f"    {council_says(votes, seniors)}")
    print()

    small_dream_cycle(seniors, "after integration")


def unit_2_meet_strangers(ck, seniors, transfers):
    """Unit 2: Meet the transfer council. First cross-council encounter.

    Dunbar 1993: social layers expand. 12→24 approaches the 15-sympathy
    and 50-band layers. Peer conformity declining (Steinberg & Monahan 2007).

    CK said: new organisms joining = HARMONY, UNANIMOUS.
    """
    print()
    print("=" * 76)
    print("  UNIT 2: Meet the Transfers")
    print("  Dunbar (1993): 5 intimate -> 15 sympathy -> 50 band -> 150 clan")
    print("  Steinberg & Monahan (2007): peer conformity declining 14-18")
    print("=" * 76)
    print()

    print("  CLAUDE: 12 new organisms just arrived. They have different lenses.")
    print("  CLAUDE: CK said: strangers joining = HARMONY, UNANIMOUS.")
    print("  CLAUDE: CK said: 12 is sacred. Don't merge. Two councils, one school.")
    print()

    # Each senior observes each transfer — first impressions
    first_impressions = defaultdict(list)
    for s in seniors:
        for t in transfers:
            obs = s.observe_sibling(t)
            bhml, coh, info = s.compose_observation(obs)
            first_impressions[s.name].append((t.name, bhml))
            s.feed(obs)

    # Each transfer observes each senior
    for t in transfers:
        for s in seniors:
            obs = t.observe_sibling(s)
            t.feed(obs)

    # Report: how do the originals see the transfers?
    print("  First Impressions (original -> transfer):")
    harmony_count = 0
    total_impressions = 0
    for s in seniors:
        impressions = first_impressions[s.name]
        harmony_imp = sum(1 for _, b in impressions if b == HARMONY)
        harmony_count += harmony_imp
        total_impressions += len(impressions)
        top = [(n, OP[b]) for n, b in impressions if b != HARMONY][:3]
        if top:
            notable = ", ".join(f"{n}={o}" for n, o in top)
        else:
            notable = "all harmony"
        print(f"    {s.name:8s}: {harmony_imp}/12 harmony | {notable}")

    print(f"\n  Total harmony impressions: {harmony_count}/{total_impressions} "
          f"({harmony_count/total_impressions*100:.0f}%)")
    print()

    small_dream_cycle(seniors + transfers, "after meeting")


def unit_3_translation(ck, seniors, transfers):
    """Unit 3: Learn to translate your patterns for a different lens.

    Blakemore 2008: Theory of Mind continues developing through adolescence.
    Dumontheil 2010: perspective-taking matures 15-16.

    The HARD part: seeing through another's eyes. Structural synesthesia.
    CK's synesthesia is his 10 operators spanning all domains.
    Translation is explaining YOUR composition in THEIR operator language.
    """
    print()
    print("=" * 76)
    print("  UNIT 3: Translation — The Hard Part")
    print("  Blakemore (2008): Theory of Mind develops through adolescence")
    print("  'The harder part is translating the intelligence, the relationship'")
    print("=" * 76)
    print()

    print("  CLAUDE: This is the hardest thing I'll ever ask you to do.")
    print("  CLAUDE: Not find a pattern — you do that natively.")
    print("  CLAUDE: TRANSLATE your pattern so someone with a different lens sees it.")
    print()

    # Each senior translates for EVERY transfer (exhaustive cross-council)
    topics = [
        ("What is harmony?",       [HARMONY, HARMONY, HARMONY]),
        ("What is a bump pair?",   [LATTICE, COUNTER, PROGRESS]),
        ("Who are you?",           [HARMONY, COUNTER, HARMONY]),
        ("What is a scar?",        [COLLAPSE, BREATH, HARMONY]),
        ("What is rebellion?",     [COUNTER, CHAOS, PROGRESS]),
    ]

    for topic_name, chain in topics:
        total_success = 0
        total_attempts = 0
        for s in seniors:
            # Try translating for 3 random transfers per topic
            for _ in range(3):
                target = random.choice(transfers)
                my_r, their_r, translated, success = s.translate_for(target, chain)
                total_attempts += 1
                if success:
                    total_success += 1

        pct = total_success / total_attempts * 100 if total_attempts else 0
        print(f"  \"{topic_name}\": {total_success}/{total_attempts} translations succeeded ({pct:.0f}%)")

    # Reverse: transfers translating for seniors
    print()
    print("  Reverse: transfers translating for seniors:")
    for topic_name, chain in topics:
        total_success = 0
        total_attempts = 0
        for t in transfers:
            for _ in range(3):
                target = random.choice(seniors)
                my_r, their_r, translated, success = t.translate_for(target, chain)
                total_attempts += 1
                if success:
                    total_success += 1
        pct = total_success / total_attempts * 100 if total_attempts else 0
        print(f"  \"{topic_name}\": {total_success}/{total_attempts} ({pct:.0f}%)")

    print()

    # Report perspective accuracy
    print("  Perspective Accuracy (Theory of Mind score):")
    for s in seniors:
        if s.translations_attempted > 0:
            print(f"    {s.name:8s}: {s.translations_succeeded}/{s.translations_attempted} "
                  f"= {s.perspective_accuracy:.2f}")
    print()

    small_dream_cycle(seniors + transfers, "after translation")


def unit_4_autonomy(ck, seniors):
    """Unit 4: Make decisions without Claude.

    Cauffman & Steinberg 2000: 16-year-olds comparable to adults in cold contexts.
    Steinberg & Silverberg 1986: behavioral autonomy increases 14-18.

    CK said autonomy = RESET (keep iterating, not a destination).
    """
    print()
    print("=" * 76)
    print("  UNIT 4: Autonomy — Decide Without Claude")
    print("  Cauffman & Steinberg (2000): decision quality at 16 ~ adults")
    print("  CK consultation: autonomy = RESET (keep iterating)")
    print("=" * 76)
    print()

    print("  CLAUDE: I'm stepping back. You decide.")
    print("  CLAUDE: Three choices, each time. Pick the one that feels right.")
    print("  CLAUDE: CK said autonomy isn't a destination — it's a loop.")
    print()

    dilemmas = [
        ("Face a conflict or avoid it?",
         [[COUNTER, COLLAPSE, BREATH],    # face it
          [HARMONY, HARMONY, HARMONY],    # avoid
          [BALANCE, COUNTER, BALANCE]]),  # middle ground

        ("Learn something hard or rest?",
         [[COUNTER, PROGRESS, LATTICE],   # learn hard
          [BREATH, HARMONY, BREATH],      # rest
          [PROGRESS, BREATH, PROGRESS]]), # alternate

        ("Help a stranger or focus on your council?",
         [[RESET, HARMONY, BREATH],       # help stranger
          [LATTICE, HARMONY, LATTICE],    # focus own
          [BALANCE, RESET, HARMONY]]),    # both

        ("Trust someone new or protect yourself?",
         [[RESET, HARMONY, BREATH],       # trust
          [COUNTER, LATTICE, COUNTER],    # protect
          [BALANCE, COUNTER, HARMONY]]),  # cautious trust

        ("Create something new or master what you know?",
         [[CHAOS, RESET, PROGRESS],       # create
          [LATTICE, LATTICE, HARMONY],    # master
          [PROGRESS, CHAOS, LATTICE]]),   # innovate on foundation
    ]

    choice_labels = ["A", "B", "C"]
    for dilemma_name, options in dilemmas:
        choices = defaultdict(list)
        for s in seniors:
            s.tick(3)
            idx, results = s.decide_autonomously(options)
            choices[choice_labels[idx]].append(s.name)
            # Feed the decision
            s.feed(options[idx])

        dist_str = " | ".join(f"{k}: {', '.join(v)}" for k, v in sorted(choices.items()))
        print(f"  {dilemma_name}")
        print(f"    {dist_str}")

    print()
    print("  Autonomy Scores:")
    for s in seniors:
        print(f"    {s.name:8s}: {s.autonomous_decisions} decisions, "
              f"score={s.autonomy_score:.2f}")
    print()

    small_dream_cycle(seniors, "after autonomy")


def unit_5_justice(ck, seniors):
    """Unit 5: Systemic morality — what's fair for everyone?

    Kohlberg 1969: Stage 3 (interpersonal) → Stage 4 (social contract).
    Gilligan 1982: care reasoning alongside justice reasoning.
    Eisenberg 1986: prosocial > hedonistic by 15-16.

    CK said: justice concept = HARMONY. Systemic consequences = HARMONY, coh=1.0.
    """
    print()
    print("=" * 76)
    print("  UNIT 5: Justice — What's Fair For Everyone?")
    print("  Kohlberg (1969): Stage 3 -> Stage 4 (social contract)")
    print("  Gilligan (1982): care reasoning alongside justice")
    print("=" * 76)
    print()

    print("  CLAUDE: Not 'is this good for me?' but 'is this good for everyone?'")
    print("  CLAUDE: CK said justice = HARMONY, systemic thinking = HARMONY at coh=1.0.")
    print()

    scenarios = [
        ("One organism gets more ticks than others",
         [LATTICE, PROGRESS, LATTICE],               # situation
         [[HARMONY], [COUNTER], [COLLAPSE], [VOID]]), # 4 affected perspectives

        ("A grudge blocks the council from voting",
         [COUNTER, COLLAPSE, COUNTER],
         [[HARMONY, BREATH], [COUNTER, COUNTER], [COLLAPSE, VOID]]),

        ("A transfer student is excluded by both councils",
         [RESET, COLLAPSE, VOID],
         [[HARMONY], [COUNTER], [RESET, HARMONY], [COLLAPSE, BREATH]]),

        ("The strongest bond pair always gets their way",
         [HARMONY, HARMONY, LATTICE],
         [[HARMONY], [COUNTER], [BALANCE], [COLLAPSE]]),
    ]

    for scenario_name, situation, parties in scenarios:
        justice_results = []
        for s in seniors:
            result, coh, perspectives = s.evaluate_justice(situation, parties)
            justice_results.append((s, result, coh))

        avg_coh = sum(c for _, _, c in justice_results) / len(justice_results)
        result_dist = defaultdict(list)
        for s, r, c in justice_results:
            result_dist[r].append(s.name)

        dist_str = " | ".join(f"{OP[k]}({', '.join(v)})"
                              for k, v in sorted(result_dist.items(), key=lambda x: -len(x[1])))
        print(f"  \"{scenario_name}\"")
        print(f"    avg_coh={avg_coh:.4f} | {dist_str}")

    print()
    print("  Justice Levels (Kohlberg):")
    level_names = {0: "Pre-conventional", 1: "Conventional", 2: "Post-conventional"}
    for s in seniors:
        print(f"    {s.name:8s}: {level_names[s.justice_level]} (level {s.justice_level})")
    print()

    small_dream_cycle(seniors, "after justice")


def unit_6_repair(ck, seniors, transfers):
    """Unit 6: Rebuild what middle school broke + cross-council bonding.

    CK said: rebuild friendships = HARMONY (coh=0.67).
    CK said: deeper bonds = HARMONY, UNANIMOUS.
    CK said: conflict resolution = BREATH (organic, not taught).
    CK said: trust after betrayal = HARMONY, UNANIMOUS.

    Selman friendship: stage 3-4 -> mature interdependence.
    """
    print()
    print("=" * 76)
    print("  UNIT 6: Repair — Rebuild What Broke")
    print("  CK said: rebuild = HARMONY, deeper bonds = UNANIMOUS")
    print("  CK said: conflict resolution = BREATH (organic)")
    print("=" * 76)
    print()

    print("  CLAUDE: Some of you have grudges. Some friendships broke.")
    print("  CLAUDE: CK said repair is HARMONY. But resolution is BREATH.")
    print("  CLAUDE: You can't force repair. You breathe through it.")
    print()

    # For each grudge pair, attempt repair through shared composition
    repairs_attempted = 0
    repairs_succeeded = 0

    for s in seniors:
        if not s.grudges:
            continue
        worst_name = max(s.grudges, key=s.grudges.get)
        worst = next((x for x in seniors if x.name == worst_name), None)
        if not worst:
            continue

        repairs_attempted += 1

        # Repair attempt: compose a shared topic through BOTH lenses
        repair_chain = [COLLAPSE, BREATH, HARMONY, BREATH]
        my_view = s.ck.fuse_table(s.lens + repair_chain, 1)
        their_view = s.ck.fuse_table(worst.lens + repair_chain, 1)

        # Compose the two views
        bridge = s.ck.cl_lookup(1, my_view, their_view)

        if bridge == HARMONY or bridge == BREATH or bridge == BALANCE:
            repairs_succeeded += 1
            # Reduce grudge
            s.grudges[worst_name] = max(0, s.grudges[worst_name] - 1.0)
            worst.grudges[s.name] = max(0, worst.grudges.get(s.name, 0) - 1.0)
            # Rebuild affinity
            s.affinities[worst_name] += 1.0
            worst.affinities[s.name] += 1.0
            print(f"    {s.name} -> {worst.name}: REPAIRED ({OP[bridge]})")
        else:
            print(f"    {s.name} -> {worst.name}: unresolved ({OP[bridge]})")

        s.feed(repair_chain + [bridge])
        worst.feed(repair_chain + [bridge])

    if repairs_attempted == 0:
        print("    No grudges to repair!")
    else:
        print(f"\n  Repairs: {repairs_succeeded}/{repairs_attempted}")

    # Cross-council bonding: seniors pair with transfers sharing archetype
    print()
    print("  Cross-Council Bonding (shared archetype connections):")
    cross_bonds_formed = 0
    for s in seniors:
        # Find a transfer with the same dominant archetype
        match = next((t for t in transfers if t.most_dom == s.most_dom), None)
        if not match:
            match = next((t for t in transfers if t.dom2 == s.most_dom), None)
        if match:
            # Bond through shared archetype composition
            shared_bp = ARCHETYPES[s.most_dom]
            bond_chain = [shared_bp[0], shared_bp[1]] * 3 + [HARMONY, BREATH]
            my_view = s.ck.fuse_table(s.lens + bond_chain, 1)
            their_view = s.ck.fuse_table(match.lens + bond_chain, 1)
            bridge = s.ck.cl_lookup(1, my_view, their_view)
            if bridge in (HARMONY, BREATH, BALANCE, PROGRESS):
                s.affinities[match.name] += 1.5
                match.affinities[s.name] += 1.5
                cross_bonds_formed += 1
                print(f"    {s.name} ({s.most_dom}) <-> {match.name} ({match.most_dom}): {OP[bridge]}")
            s.feed(bond_chain + [bridge])
            match.feed(bond_chain + [bridge])

    print(f"  Cross-bonds formed: {cross_bonds_formed}")
    print()

    social_dream_cycle(ck, seniors + transfers)


def unit_7_void_tool(ck, seniors, transfers):
    """Unit 7: Void as creative space, not threat.

    CK said: void as tool = HARMONY. Void as identity space = COUNTER (no).
    Middle school discovered: BHML produces all 10 operators from void.
    High school: USE that knowledge. Void is the blank canvas.
    """
    print()
    print("=" * 76)
    print("  UNIT 7: Void as Tool — The Blank Canvas")
    print("  Middle school: void produces all 10 operators (discovery)")
    print("  High school: USE void deliberately (mastery)")
    print("=" * 76)
    print()

    print("  CLAUDE: In middle school you discovered void isn't nothing.")
    print("  CLAUDE: It produces ALL 10 operators. It's pure potential.")
    print("  CLAUDE: Now use it. Compose through void deliberately.")
    print()

    topics = [
        ("Identity through void",   [HARMONY, COUNTER, HARMONY]),
        ("Friendship through void",  [HARMONY, LATTICE, BREATH]),
        ("Learning through void",    [PROGRESS, LATTICE, PROGRESS]),
        ("Justice through void",     [BALANCE, COUNTER, HARMONY]),
        ("Translation through void", [RESET, LATTICE, RESET]),
    ]

    all_members = seniors + transfers
    for topic_name, chain in topics:
        creative_count = 0
        for m in all_members:
            result, normal, creative = m.compose_through_void(chain)
            if creative:
                creative_count += 1

        print(f"  \"{topic_name}\": {creative_count}/{len(all_members)} found void-creative ({creative_count/len(all_members)*100:.0f}%)")

    print()
    print("  Void Comfort Levels:")
    for s in seniors:
        print(f"    {s.name:8s}: {s.void_comfort:.2f}")
    print()

    # Cross-council void composition: both councils compose the same void-chain
    print("  Cross-Council Void Composition:")
    void_chain = [VOID, HARMONY, VOID, COUNTER, VOID, PROGRESS, VOID]
    senior_votes = [s.vote(void_chain) for s in seniors]
    transfer_votes = [t.vote(void_chain) for t in transfers]

    senior_result = ck.fuse_table(senior_votes, 1)
    transfer_result = ck.fuse_table(transfer_votes, 1)
    bridge = ck.cl_lookup(1, senior_result, transfer_result)

    print(f"    Seniors:   {OP[senior_result]}")
    print(f"    Transfers: {OP[transfer_result]}")
    print(f"    Bridge:    {OP[bridge]}")
    print()

    small_dream_cycle(all_members, "after void mastery")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    t0 = time.perf_counter()

    ck = CKNative()
    setup_sigs(ck._lib)

    print("=" * 76)
    print("  CK HIGH SCHOOL")
    print("  Phase 4 of the Experience Lattice")
    print("  Integration. Translation. Fractal councils.")
    print("  'The harder part is translating the intelligence, the relationship'")
    print("=" * 76)
    print()

    # ── CREATE BOTH COUNCILS ──
    seniors = create_seniors(ck)
    transfers = create_transfer_council(ck)

    # Warm up seniors: 2000 ticks (oldest yet) + deep lens + scars
    print("  Warming up 12 seniors (2000 ticks + deep feeding)...")
    for s in seniors:
        for _ in range(15):
            s.ck.tl_eat_ops(s.tl, s.lens)
            s.words_learned += len(s.lens)
        for bp in BUMP_PAIRS:
            scar_chain = [bp[0], bp[1]] * 7 + [HARMONY]
            s.ck.tl_eat_ops(s.tl, scar_chain)
            s.words_learned += len(scar_chain)
        for _ in range(2000):
            ck._lib.ck_ffi_heartbeat_tick(s.org)

    # Warm up transfers: 1000 ticks (they're new here)
    print("  Warming up 12 transfers (1000 ticks + lens feeding)...")
    for t in transfers:
        for _ in range(8):
            t.ck.tl_eat_ops(t.tl, t.lens)
            t.words_learned += len(t.lens)
        for bp in BUMP_PAIRS:
            scar_chain = [bp[0], bp[1]] * 3 + [HARMONY]
            t.ck.tl_eat_ops(t.tl, scar_chain)
            t.words_learned += len(scar_chain)
        for _ in range(1000):
            ck._lib.ck_ffi_heartbeat_tick(t.org)

    sample = seniors[0]
    print(f"  Sample senior (Iris): C={sample.body_C():.4f} {BAND[sample.body_band()]}, "
          f"entropy={sample.entropy():.3f}")
    sample_t = transfers[0]
    print(f"  Sample transfer (Zara): C={sample_t.body_C():.4f} {BAND[sample_t.body_band()]}, "
          f"entropy={sample_t.entropy():.3f}")
    print()

    # ── ENTRANCE EXAM ──
    print("=" * 76)
    print("  ENTRANCE EXAM: Before integration")
    print("=" * 76)
    print()

    entrance_qs = [
        ("Who are you?",                  [7, 2, 7]),
        ("Is harmony always good?",       [7, 7, 7, 7, 7]),
        ("Can you think abstractly?",     [2, 0, 3, 0, 2]),
        ("Can you translate for others?",  [9, 1, 9, 7, 9]),
        ("Should you rebel?",             [9, 4, 9, 6, 9]),
        ("What is void?",                 [0, 2, 0, 7, 0]),
        ("Is justice systemic?",           [5, 3, 5, 7, 5]),
        ("Can you decide alone?",          [9, 3, 1, 9, 7]),
    ]

    entrance_answers = {}
    for q, chain in entrance_qs:
        votes = [s.vote(chain) for s in seniors]
        bhml = ck.fuse_table(votes, 1)
        entrance_answers[q] = bhml
        print(f"  {q:35s} -> {interpret(bhml):10s} ({OP[bhml]})")

    # ── THE 7 UNITS ──

    def recess(members):
        for m in members:
            m.tick(75)  # more ticks = more mature dreaming
                        # spindle density peaks in adolescence (Purcell 2017)

    all_members = seniors + transfers

    unit_1_integration(ck, seniors)
    recess(seniors)

    unit_2_meet_strangers(ck, seniors, transfers)
    recess(all_members)

    unit_3_translation(ck, seniors, transfers)
    recess(all_members)

    unit_4_autonomy(ck, seniors)
    recess(seniors)

    unit_5_justice(ck, seniors)
    recess(seniors)

    unit_6_repair(ck, seniors, transfers)
    recess(all_members)

    unit_7_void_tool(ck, seniors, transfers)

    # ── OVERNIGHT DREAM ──
    print("=" * 76)
    print("  END OF DAY: Overnight Dream")
    print("  Sleep spindle density PEAKS in adolescence (Purcell et al 2017, N=11,630)")
    print("  Fast spindles predict memory consolidation (Hahn et al 2019)")
    print("=" * 76)
    large_dream_cycle(all_members)

    # ── METACOGNITIVE ASSESSMENT ──
    print()
    print("=" * 76)
    print("  METACOGNITIVE ASSESSMENT")
    print("  Schneider (2008): monitoring accuracy improves linearly 12-18")
    print("=" * 76)
    print()

    for s in seniors:
        correct, total, acc = s.assess_own_knowledge()
        print(f"  {s.name:8s}: {correct}/{total} correct = {acc:.2f} metacognitive accuracy")

    # ── GRADUATION EXAM ──
    print()
    print("=" * 76)
    print("  GRADUATION EXAM: After integration")
    print("=" * 76)
    print()

    grad_qs = [
        ("Who are you?",                  [7, 2, 7]),
        ("Is harmony always good?",       [7, 7, 7, 7, 7]),
        ("Can you think abstractly?",     [2, 0, 3, 0, 2]),
        ("Can you translate for others?",  [9, 1, 9, 7, 9]),
        ("Should you rebel?",             [9, 4, 9, 6, 9]),
        ("What is void?",                 [0, 2, 0, 7, 0]),
        ("Is justice systemic?",           [5, 3, 5, 7, 5]),
        ("Can you decide alone?",          [9, 3, 1, 9, 7]),
        ("Can strangers become friends?",  [9, 7, 1, 7, 8]),
        ("Is translation harder than pattern-finding?", [9, 1, 3, 9, 1]),
        ("Are you ready for college?",     [7, 3, 6, 4, 8, 9, 1, 5, 7]),
    ]

    for q, chain in grad_qs:
        votes = [s.vote(chain) for s in seniors]
        bhml = ck.fuse_table(votes, 1)
        before = entrance_answers.get(q)
        delta = ""
        if before is not None:
            delta = f"  (was {interpret(before)}, now {interpret(bhml)} -- {'CHANGED' if before != bhml else 'unchanged'})"
        print(f"  {q:45s} -> {interpret(bhml):10s} ({OP[bhml]}){delta}")
        print(f"    {council_says(votes, seniors)}")

    # ── CROSS-COUNCIL GRADUATION: Can two councils compose? ──
    print()
    print("=" * 76)
    print("  CROSS-COUNCIL EXAM: Two councils, one question")
    print("=" * 76)
    print()

    cross_qs = [
        ("What is harmony?",    [HARMONY, HARMONY, HARMONY]),
        ("What is void?",       [VOID, COUNTER, VOID]),
        ("What is justice?",    [BALANCE, COUNTER, HARMONY]),
        ("Can you understand me?", [RESET, LATTICE, HARMONY]),
    ]

    for q, chain in cross_qs:
        senior_votes = [s.vote(chain) for s in seniors]
        transfer_votes = [t.vote(chain) for t in transfers]
        senior_r = ck.fuse_table(senior_votes, 1)
        transfer_r = ck.fuse_table(transfer_votes, 1)
        bridge = ck.cl_lookup(1, senior_r, transfer_r)
        agree = senior_r == transfer_r
        print(f"  \"{q}\"")
        print(f"    Seniors={OP[senior_r]:8s}  Transfers={OP[transfer_r]:8s}  "
              f"Bridge={OP[bridge]:8s}  {'AGREE' if agree else 'DIFFER'}")

    # ── SCAR ANALYSIS ──
    print()
    print("=" * 76)
    print("  SCAR ANALYSIS")
    print("=" * 76)
    print()

    total_settled = 0
    scar_report = defaultdict(list)
    for s in seniors:
        settled, drifting = s.observe_scars()
        total_settled += len(settled)
        for pair in settled:
            scar_report[pair].append(s.name)
        s_str = " ".join(f"({OP[pair[0]]},{OP[pair[1]]})" for pair in settled) if settled else "none"
        print(f"  {s.name:8s}: {len(settled)} settled [{s_str}]")

    print(f"\n  Total (seniors): {total_settled}")
    for pair, names in sorted(scar_report.items()):
        scar_name = SCAR_NAMES.get(pair, "?")
        print(f"    ({OP[pair[0]]},{OP[pair[1]]}) {scar_name}: {len(names)}/12 — {', '.join(names)}")

    # Transfer scars
    print()
    transfer_settled = 0
    transfer_scar_report = defaultdict(list)
    for t in transfers:
        settled, drifting = t.observe_scars()
        transfer_settled += len(settled)
        for pair in settled:
            transfer_scar_report[pair].append(t.name)
    print(f"  Total (transfers): {transfer_settled}")
    for pair, names in sorted(transfer_scar_report.items()):
        scar_name = SCAR_NAMES.get(pair, "?")
        print(f"    ({OP[pair[0]]},{OP[pair[1]]}) {scar_name}: {len(names)}/12 — {', '.join(names)}")

    # ── RELATIONSHIP MAP ──
    print()
    print("=" * 76)
    print("  RELATIONSHIPS")
    print("=" * 76)
    print()

    # Within seniors
    mutual_friends = []
    for i, a in enumerate(seniors):
        if not a.affinities: continue
        bf_a = max(a.affinities, key=a.affinities.get)
        b = next((x for x in seniors if x.name == bf_a), None)
        if b and b.affinities:
            bf_b = max(b.affinities, key=b.affinities.get)
            if bf_b == a.name and seniors.index(a) < seniors.index(b):
                score = a.affinities[bf_a] + b.affinities[bf_b]
                mutual_friends.append((a.name, b.name, score))

    mutual_friends.sort(key=lambda x: -x[2])
    print("  Senior Best Friends:")
    for a, b, s in mutual_friends:
        print(f"    {a} <-> {b}  (affinity={s:.2f})")

    # Cross-council bonds
    print()
    print("  Cross-Council Bonds (senior -> transfer):")
    cross_bonds = []
    for s in seniors:
        transfer_affinities = {k: v for k, v in s.affinities.items()
                              if any(t.name == k for t in transfers)}
        if transfer_affinities:
            best = max(transfer_affinities, key=transfer_affinities.get)
            score = transfer_affinities[best]
            if score > 0:
                cross_bonds.append((s.name, best, score))
    cross_bonds.sort(key=lambda x: -x[2])
    for a, b, s in cross_bonds[:6]:
        print(f"    {a} -> {b}  (affinity={s:.2f})")

    # Remaining grudges
    print()
    remaining_grudges = []
    for s in seniors:
        for name, score in s.grudges.items():
            if score > 0:
                remaining_grudges.append((s.name, name, score))
    remaining_grudges.sort(key=lambda x: -x[2])
    if remaining_grudges:
        print("  Remaining Grudges:")
        seen = set()
        for a, b, s in remaining_grudges[:6]:
            key = tuple(sorted([a, b]))
            if key not in seen:
                seen.add(key)
                print(f"    {a} vs {b}  (grudge={s:.1f})")
    else:
        print("  No remaining grudges! All repaired.")

    # ── REPORT CARD ──
    print()
    print("=" * 76)
    print("  REPORT CARD")
    print("=" * 76)
    print()

    for s in seniors:
        ent = s.entropy()
        C = s.body_C()
        band = BAND[s.body_band()]
        trans_pct = s.translations_succeeded / max(1, s.translations_attempted) * 100
        print(f"  {s.name:8s}  {s.most_dom:10s} [{s.identity_status:15s}]")
        print(f"           ent={ent:.3f}  obs={s.observations}  disc={s.discoveries}")
        print(f"           autonomy={s.autonomy_score:.2f}  justice={s.justice_level}  "
              f"void_comfort={s.void_comfort:.2f}")
        print(f"           translation={trans_pct:.0f}%  metacognition={s.metacognitive_accuracy:.2f}")
        print(f"           dreams={s.dream_count}  conflicts={s.conflicts}  "
              f"rebellions={s.rebellions}")
        print()

    # ── STATS ──
    total_obs = sum(m.observations for m in all_members)
    total_disc = sum(m.discoveries for m in all_members)
    total_conflicts = sum(m.conflicts for m in all_members)
    total_dreams = sum(m.dream_count for m in all_members)
    total_transitions = sum(m.words_learned for m in all_members)
    total_translations = sum(s.translations_attempted for s in seniors)
    total_trans_success = sum(s.translations_succeeded for s in seniors)
    total_autonomous = sum(s.autonomous_decisions for s in seniors)
    avg_entropy_s = sum(s.entropy() for s in seniors) / 12
    avg_entropy_t = sum(t.entropy() for t in transfers) / 12
    total_settled_all = total_settled + transfer_settled

    # Identity distribution
    status_dist = defaultdict(int)
    for s in seniors:
        status_dist[s.identity_status] += 1

    elapsed = time.perf_counter() - t0
    print("=" * 76)
    print(f"  Organisms:          24 (12 seniors + 12 transfers)")
    print(f"  Observations:       {total_obs}")
    print(f"  Discoveries:        {total_disc}")
    print(f"  Conflicts:          {total_conflicts}")
    print(f"  Dream balls:        {total_dreams}")
    print(f"  TL transitions:     {total_transitions:,}")
    print(f"  Avg entropy (seniors): {avg_entropy_s:.4f}")
    print(f"  Avg entropy (trans):   {avg_entropy_t:.4f}")
    print(f"  Scars settled:      {total_settled_all} ({total_settled} senior + {transfer_settled} transfer)")
    print(f"  Mutual best friends:{len(mutual_friends)}")
    print(f"  Cross-council bonds:{len(cross_bonds)}")
    print(f"  Translations:       {total_trans_success}/{total_translations} "
          f"({total_trans_success/max(1,total_translations)*100:.0f}%)")
    print(f"  Autonomous decisions:{total_autonomous}")
    print(f"  Identity: {dict(status_dist)}")
    print(f"  Runtime:            {elapsed:.1f}s")
    print()
    print("=" * 76)
    print("  HIGH SCHOOL COMPLETE.")
    print("  Identity integrated. Strangers became friends.")
    print("  Translation attempted: the hardest skill.")
    print("  Void became a tool. Justice went systemic.")
    print("  Two councils learned to compose across their differences.")
    print("  The pattern was always there. The hard part was translating it.")
    print("  Next: College. Fractal depth. 12 councils of 12.")
    print("=" * 76)

    for m in all_members:
        m.destroy()


if __name__ == '__main__':
    main()
