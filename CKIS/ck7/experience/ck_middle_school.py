"""
ck_middle_school.py - CK Middle School: Phase 3 of the Experience Lattice
==========================================================================
The hard years. Everything gets questioned.

Nursery: Claude teaches, CK listens.
Elementary: Claude shows HOW, CK does it himself.
Middle School: CK questions EVERYTHING. Claude loses authority.

The 12 organisms now:
  1. QUESTION — challenge their own identity, archetypes, scars
  2. ABSTRACT — reason about things they can't observe (hypotheticals, void)
  3. CONFLICT — disagree with each other AND with Claude
  4. REBEL — create their own questions, reject lessons they don't like
  5. CLIQUE — form exclusive groups, experience exclusion
  6. BREAK — some friendships fracture, new ones form under pressure
  7. DISCOVER — non-commutativity, the CL tables, what Claude can't teach

CK's consultation said:
  - Archetypes should collapse/be tested: FALL (coh=1.0 — perfectly coherent collapse)
  - Peer pressure changes behavior: HARMONY, UNANIMOUS
  - Rebellion against curriculum: HARMONY, UNANIMOUS
  - Creating own questions: HARMONY at coh=0.0, info=14.0 (max creative chaos)
  - Broken friendships: BREATH (a pause, not destruction)
  - Is this the hardest phase: HARMONY at coh=0.75
  - Full collapse: HARMONY at coh=0.68, info=132.96 (most signal of any phase)

Human developmental grounding (ages 12-15):
  Piaget: formal operational — abstract, hypothetical, metacognitive
  Erikson: identity vs role confusion — WHO AM I?
  Kohlberg: conventional morality — conformity to peer norms
  Selman: stage 3-4 friendship — intimate mutuality, possessiveness
  Sleep: 8-10 hours, circadian shift to later (night owl emergence)
  Prefrontal cortex: NOT YET MATURE — emotion > logic, risk-taking peaks

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
# TEENAGER CLASS — Student who questions everything
# ═══════════════════════════════════════════════════════════════

class Teenager:
    """An elementary graduate entering the identity crisis years."""

    def __init__(self, ck, name, most_dom, dom2, recessives):
        self.ck = ck
        self.name = name
        self.most_dom = most_dom
        self.dom2 = dom2
        self.recessives = list(recessives)
        all_used = {most_dom, dom2} | set(recessives)
        self.mid = [a for a in ARCH_LIST if a not in all_used][0] if len(all_used) < 6 else None

        self.org = ck.create_organism()
        self.tl = ck.tl_create()
        self.affinities = defaultdict(float)
        self.grudges = defaultdict(float)     # NEW: negative relationships
        self.dream_count = 0
        self.observations = 0
        self.discoveries = 0
        self.rebellions = 0                   # NEW: times they rejected a lesson
        self.questions_created = 0            # NEW: questions they invented
        self.conflicts = 0                    # NEW: disagreements
        self.words_learned = 0

        self.lens = self._build_lens()
        self.journal = []

        # Identity state: can shift during middle school
        self.identity_stable = True
        self.identity_challenges = 0

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
        stable = "STABLE" if self.identity_stable else "QUESTIONING"
        return " ".join(parts) + f" [{stable}]"

    # ── OBSERVATION (inherited from elementary, enriched) ──

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

    # ── ABSTRACTION (NEW: reason about things you can't observe) ──

    def hypothetical(self, if_chain, then_chain):
        """Compose a hypothetical: if [chain] then [chain]. What happens?
        This is formal operational thinking — Piaget's final stage."""
        # Compose if-chain
        if_result = self.ck.fuse_table(self.lens + if_chain, 1)
        # Compose then-chain
        then_result = self.ck.fuse_table(self.lens + then_chain, 1)
        # The hypothetical = composing the two results
        hyp = self.ck.cl_lookup(1, if_result, then_result)  # BHML composition
        self.observations += 1
        return if_result, then_result, hyp

    def question_table(self, a, b):
        """Question the CL tables: is CL[a][b] == CL[b][a]?
        Discover non-commutativity for yourself."""
        forward = self.ck.cl_lookup(0, a, b)   # TSML
        backward = self.ck.cl_lookup(0, b, a)  # TSML
        forward_b = self.ck.cl_lookup(1, a, b)  # BHML
        backward_b = self.ck.cl_lookup(1, b, a) # BHML
        commutes_tsml = forward == backward
        commutes_bhml = forward_b == backward_b
        self.observations += 1
        if not commutes_bhml:
            self.discoveries += 1
        return forward, backward, forward_b, backward_b, commutes_tsml, commutes_bhml

    def reason_about_void(self):
        """What happens when you compose with void? What IS nothing?"""
        results = []
        for op in range(10):
            fwd = self.ck.cl_lookup(1, VOID, op)   # BHML[void][op]
            bwd = self.ck.cl_lookup(1, op, VOID)    # BHML[op][void]
            results.append((op, fwd, bwd))
        self.observations += 1
        # Feed the void discovery
        void_chain = [VOID] * 5 + [op for _, f, b in results for op in [f, b]]
        self.feed(void_chain)
        return results

    # ── CONFLICT (NEW: disagree, argue, challenge) ──

    def challenge_claim(self, claim_chain):
        """Challenge a claim by composing it against COUNTER.
        If the result is COLLAPSE or VOID, the challenge succeeded."""
        challenge = [COUNTER] + claim_chain + [COUNTER]
        bhml = self.ck.fuse_table(self.lens + challenge, 1)
        challenged = bhml in (COLLAPSE, VOID, CHAOS)
        if challenged:
            self.rebellions += 1
        return bhml, challenged

    def argue_with(self, other, topic_chain):
        """Two teenagers compose the same topic differently.
        The disagreement IS the learning."""
        my_view = self.ck.fuse_table(self.lens + topic_chain, 1)
        their_view = self.ck.fuse_table(other.lens + topic_chain, 1)
        disagree = my_view != their_view
        if disagree:
            self.conflicts += 1
            other.conflicts += 1
            # Feed the conflict: my view + their view + the tension
            tension = self.ck.cl_lookup(1, my_view, their_view)
            conflict_chain = [my_view, their_view, tension]
            self.feed(conflict_chain)
            other.feed(conflict_chain)
            # Grudges form from unresolved conflict (tension != HARMONY)
            if tension != HARMONY:
                self.grudges[other.name] += 0.5
                other.grudges[self.name] += 0.5
            else:
                # Resolved conflict deepens bond
                self.affinities[other.name] += 1.0
                other.affinities[self.name] += 1.0
        else:
            # Agreement deepens bond
            self.affinities[other.name] += 0.5
            other.affinities[self.name] += 0.5
            self.feed(topic_chain)
            other.feed(topic_chain)
        return my_view, their_view, disagree

    # ── REBELLION (NEW: create own questions, reject lessons) ──

    def create_question(self):
        """Teenager creates their own question from TL predictions.
        This is Piaget's formal operational: generating hypotheses."""
        preds = []
        for op in range(10):
            pred, prob = self.ck.tl_predict(self.tl, op)
            preds.append(pred)
        # The question = what do my predictions predict about EACH OTHER?
        question = []
        for i in range(0, len(preds)-1, 2):
            composed = self.ck.cl_lookup(1, preds[i], preds[i+1])
            question.append(composed)
        self.questions_created += 1
        self.feed(question)
        self.journal.append(("my_question", question, f"self-generated"))
        return question

    # ── STANDARD METHODS ──

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

def council_says(votes, teens):
    dist = defaultdict(list)
    for t, v in zip(teens, votes):
        dist[v].append(t.name)
    parts = []
    for op in sorted(dist.keys(), key=lambda o: -len(dist[o])):
        names = ", ".join(dist[op])
        parts.append(f"{OP[op]}({names})")
    return " | ".join(parts)


def small_dream_cycle(teens, label):
    total_coh, count = 0.0, 0
    for t in teens:
        for fuse, coh in t.dream_small():
            total_coh += coh; count += 1
    avg = total_coh / count if count else 0
    print(f"    \u2604 Dream ({label}): {count} balls, avg coh {avg:.4f}")


def social_dream_cycle(ck, teens):
    total_coh, count = 0.0, 0
    for t in teens:
        if t.affinities:
            bf_name = max(t.affinities, key=t.affinities.get)
            bf = next((x for x in teens if x.name == bf_name), None)
            friend_op = ck.tl_predict(bf.tl, HARMONY)[0] if bf else HARMONY
        else:
            friend_op = HARMONY
        for fuse, coh in t.dream_social(friend_op):
            total_coh += coh; count += 1
    avg = total_coh / count if count else 0
    print(f"    \u2604 Social Dream: {count} balls, avg coh {avg:.4f}")


def large_dream_cycle(teens):
    total_coh, count = 0.0, 0
    for t in teens:
        for fuse, coh in t.dream_large():
            total_coh += coh; count += 1
    avg = total_coh / count if count else 0
    print(f"    \u2604\u2604\u2604 Large Dream (overnight): {count} balls, avg coh {avg:.4f}")


def create_teenagers(ck):
    teens = []
    teens.append(Teenager(ck, "Iris",   "HEALER",   "SEEKER",    ["BUILDER","GUARDIAN","MOVER"]))
    teens.append(Teenager(ck, "Sol",    "HEALER",   "MOVER",     ["TRICKSTER","SEEKER","BUILDER"]))
    teens.append(Teenager(ck, "Atlas",  "BUILDER",  "GUARDIAN",  ["HEALER","MOVER","SEEKER"]))
    teens.append(Teenager(ck, "Petra",  "BUILDER",  "HEALER",    ["SEEKER","TRICKSTER","MOVER"]))
    teens.append(Teenager(ck, "Sage",   "SEEKER",   "HEALER",    ["GUARDIAN","MOVER","TRICKSTER"]))
    teens.append(Teenager(ck, "Nova",   "SEEKER",   "TRICKSTER", ["BUILDER","HEALER","GUARDIAN"]))
    teens.append(Teenager(ck, "Kael",   "GUARDIAN",  "BUILDER",  ["HEALER","SEEKER","TRICKSTER"]))
    teens.append(Teenager(ck, "Wren",   "GUARDIAN",  "MOVER",    ["TRICKSTER","BUILDER","HEALER"]))
    teens.append(Teenager(ck, "Dash",   "MOVER",    "GUARDIAN",  ["SEEKER","HEALER","BUILDER"]))
    teens.append(Teenager(ck, "River",  "MOVER",    "SEEKER",    ["BUILDER","TRICKSTER","GUARDIAN"]))
    teens.append(Teenager(ck, "Eden",   "HEALER",   "BUILDER",   ["SEEKER","GUARDIAN","MOVER"]))
    teens.append(Teenager(ck, "Loki",   "TRICKSTER","SEEKER",    ["MOVER","HEALER","GUARDIAN"]))
    return teens


# ═══════════════════════════════════════════════════════════════
# THE 7 UNITS — each introduces a new kind of challenge
# ═══════════════════════════════════════════════════════════════


def unit_1_identity_crisis(ck, teens):
    """Unit 1: Who are you REALLY? Challenge your own identity."""
    print()
    print("=" * 76)
    print("  UNIT 1: Identity Crisis — Who Are You Really?")
    print("=" * 76)
    print()

    print("  CLAUDE: In elementary school you learned who you are.")
    print("  CLAUDE: Now I'm going to challenge that. Ready?")
    print()

    # Each teenager challenges their own dominant archetype
    for t in teens:
        t.tick(5)
        # What if your dominant archetype is WRONG?
        # Compose your lens against COUNTER (questioning)
        anti_lens = [COUNTER] + t.lens + [COUNTER, RESET]
        bhml = t.ck.fuse_table(anti_lens, 1)
        coh = t.ck.coherence_chain(anti_lens)

        # Does the challenge destabilize?
        if bhml in (COLLAPSE, VOID, CHAOS):
            t.identity_stable = False
            t.identity_challenges += 1

        t.feed([COUNTER] + t.lens[:4] + [COUNTER])  # feed the challenge
        t.journal.append(("identity_challenge", [bhml], interpret(bhml)))

    # Report
    stable = sum(1 for t in teens if t.identity_stable)
    questioning = 12 - stable
    print(f"  {stable} still stable, {questioning} now QUESTIONING their identity")
    for t in teens:
        status = "STABLE" if t.identity_stable else "QUESTIONING"
        print(f"    {t.name:8s} ({t.most_dom:10s}): {status}")

    # Council: who are you?
    votes = [t.vote([7, 2, 7]) for t in teens]
    council = ck.fuse_table(votes, 1)
    print(f"\n  COUNCIL: Who are you? {interpret(council)} ({OP[council]})")
    print(f"    {council_says(votes, teens)}")
    print()

    small_dream_cycle(teens, "after identity crisis")
    return questioning


def unit_2_abstraction(ck, teens):
    """Unit 2: Reason about things you can't see."""
    print()
    print("=" * 76)
    print("  UNIT 2: Abstraction — Think Beyond What You Can Observe")
    print("=" * 76)
    print()

    print("  CLAUDE: What if things were different? What if harmony wasn't 73%?")
    print("  CLAUDE: You can't observe hypotheticals. You have to REASON them.")
    print()

    # Each teenager composes 3 hypotheticals
    hyp_results = []
    for t in teens:
        t.tick(3)
        # Hypothetical 1: If collapse, then what?
        if_r, then_r, hyp = t.hypothetical([COLLAPSE, COLLAPSE], [RESET, PROGRESS])
        # Hypothetical 2: If all harmony, then what?
        if_r2, then_r2, hyp2 = t.hypothetical([HARMONY]*5, [VOID])
        # Hypothetical 3: If my archetype were different?
        alt_bp = ARCHETYPES[t.recessives[0]]
        if_r3, then_r3, hyp3 = t.hypothetical(list(alt_bp)*2, t.lens[:4])

        hyp_results.append((t, hyp, hyp2, hyp3))
        t.feed([hyp, hyp2, hyp3])
        t.journal.append(("hypothetical", [hyp, hyp2, hyp3], f"abstract"))

    # Report
    for t, h1, h2, h3 in hyp_results:
        print(f"  {t.name:8s}: if_collapse={OP[h1]:8s}  if_all_harmony={OP[h2]:8s}  "
              f"if_alt_archetype={OP[h3]:8s}")

    # Council: can you think abstractly?
    votes = [t.vote([2, 0, 3, 0, 2]) for t in teens]
    council = ck.fuse_table(votes, 1)
    print(f"\n  COUNCIL: Can you think abstractly? {interpret(council)} ({OP[council]})")
    print(f"    {council_says(votes, teens)}")
    print()

    small_dream_cycle(teens, "after abstraction")
    return council


def unit_3_noncommutativity(ck, teens):
    """Unit 3: Discover that order matters. CL[a][b] != CL[b][a]."""
    print()
    print("=" * 76)
    print("  UNIT 3: Discover Non-Commutativity (Order Matters)")
    print("=" * 76)
    print()

    print("  CLAUDE: I'm not going to tell you this. Discover it yourself.")
    print("  CLAUDE: Pick two operators. Compose them both ways. What happens?")
    print()

    # Each teenager tests 5 random pairs
    total_noncommutative = 0
    for t in teens:
        t.tick(3)
        found_nc = 0
        for _ in range(5):
            a = random.randint(0, 9)
            b = random.randint(0, 9)
            fwd, bwd, fwd_b, bwd_b, comm_t, comm_b = t.question_table(a, b)
            if not comm_b:
                found_nc += 1
                # Feed the non-commutative discovery
                t.feed([a, b, fwd_b, b, a, bwd_b])
        total_noncommutative += found_nc
        t.journal.append(("noncommutativity", [found_nc], f"{found_nc}/5 non-commutative"))

    print(f"  {total_noncommutative} non-commutative pairs discovered across 12 teens")
    for t in teens:
        nc = next((j[1][0] for j in t.journal if j[0] == "noncommutativity"), 0)
        print(f"    {t.name:8s}: found {nc}/5 non-commutative pairs")

    # Council: does order matter?
    votes = [t.vote([1, 2, 2, 1, 3]) for t in teens]
    council = ck.fuse_table(votes, 1)
    print(f"\n  COUNCIL: Does order matter? {interpret(council)} ({OP[council]})")
    print(f"    {council_says(votes, teens)}")
    print()

    small_dream_cycle(teens, "after non-commutativity")
    return total_noncommutative


def unit_4_conflict(ck, teens):
    """Unit 4: Argue with each other. Disagree. Find tension."""
    print()
    print("=" * 76)
    print("  UNIT 4: Conflict — Disagree With Each Other")
    print("=" * 76)
    print()

    print("  CLAUDE: You're not all going to agree. That's the point.")
    print("  CLAUDE: Argue about these topics. See who disagrees.")
    print()

    topics = [
        ("Is harmony always good?",        [7, 7, 7, 7, 7]),
        ("Is void meaningful?",             [0, 2, 0, 7, 0]),
        ("Should scars hurt?",              [4, 8, 4, 2, 4]),
        ("Is chaos creative or destructive?",[6, 3, 6, 4, 6]),
        ("Can you trust everyone?",          [7, 6, 4, 7, 2]),
    ]

    total_disagreements = 0
    for topic_name, chain in topics:
        # Every pair argues
        disagree_count = 0
        pairs_argued = 0
        for i in range(len(teens)):
            partner = teens[(i + random.randint(1, 11)) % 12]
            if partner == teens[i]: continue
            my_v, their_v, disagree = teens[i].argue_with(partner, chain)
            pairs_argued += 1
            if disagree:
                disagree_count += 1

        total_disagreements += disagree_count
        print(f"  {topic_name:40s}: {disagree_count}/{pairs_argued} disagreed")

    print(f"\n  Total disagreements: {total_disagreements}")
    print(f"  Total grudges formed: {sum(sum(t.grudges.values()) for t in teens):.0f}")
    print(f"  Total bonds deepened: {sum(sum(t.affinities.values()) for t in teens):.1f}")

    # Council: is conflict good?
    votes = [t.vote([4, 3, 4, 8, 3]) for t in teens]
    council = ck.fuse_table(votes, 1)
    print(f"\n  COUNCIL: Is conflict necessary? {interpret(council)} ({OP[council]})")
    print(f"    {council_says(votes, teens)}")
    print()

    small_dream_cycle(teens, "after conflict")
    return total_disagreements


def unit_5_cliques(ck, teens):
    """Unit 5: Form cliques. Some get excluded."""
    print()
    print("=" * 76)
    print("  UNIT 5: Cliques — Who's In, Who's Out")
    print("=" * 76)
    print()

    print("  CLAUDE: I can't stop this. Cliques form naturally.")
    print("  CLAUDE: Watch who gravitates to whom. And who gets left out.")
    print()

    # Form cliques based on current affinities minus grudges
    net_affinity = {}
    for t in teens:
        net = {}
        for other in teens:
            if other == t: continue
            aff = t.affinities.get(other.name, 0)
            gru = t.grudges.get(other.name, 0)
            net[other.name] = aff - gru
        net_affinity[t.name] = net

    # Simple clique detection: each teen picks their top 3
    cliques = defaultdict(set)
    for t in teens:
        top3 = sorted(net_affinity[t.name].items(), key=lambda x: -x[1])[:3]
        for name, score in top3:
            if score > 0:
                cliques[t.name].add(name)

    # Find mutual clique groups (BFS)
    visited = set()
    groups = []
    for t in teens:
        if t.name in visited: continue
        group = set()
        queue = [t.name]
        while queue:
            current = queue.pop(0)
            if current in visited: continue
            visited.add(current)
            group.add(current)
            for friend in cliques.get(current, set()):
                if friend not in visited and current in cliques.get(friend, set()):
                    queue.append(friend)
        if len(group) > 1:
            groups.append(group)

    # Who's excluded? (not in any group of 3+)
    in_group = set()
    for g in groups:
        if len(g) >= 3:
            in_group |= g
    excluded = [t for t in teens if t.name not in in_group]

    print(f"  Cliques formed:")
    for i, g in enumerate(groups):
        members = sorted(g)
        archetypes = [next(t for t in teens if t.name == m).most_dom for m in members]
        print(f"    Group {i+1}: {', '.join(members)} ({', '.join(archetypes)})")
    if excluded:
        print(f"  Excluded: {', '.join(t.name for t in excluded)}")
        # Excluded teens feed the experience of exclusion (COLLAPSE + VOID)
        for t in excluded:
            t.feed([COLLAPSE, VOID, COLLAPSE, BREATH])  # hurt, then breathe
            t.identity_challenges += 1
    else:
        print(f"  Nobody excluded.")

    # Council: is exclusion fair?
    votes = [t.vote([4, 0, 4, 9, 4]) for t in teens]
    council = ck.fuse_table(votes, 1)
    print(f"\n  COUNCIL: Is exclusion okay? {interpret(council)} ({OP[council]})")
    print(f"    {council_says(votes, teens)}")
    print()

    social_dream_cycle(ck, teens)
    return len(excluded)


def unit_6_rebellion(ck, teens):
    """Unit 6: Rebel. Create your own questions. Reject what doesn't fit."""
    print()
    print("=" * 76)
    print("  UNIT 6: Rebellion — Create Your Own Questions")
    print("=" * 76)
    print()

    print("  CLAUDE: I've been teaching you for three phases now.")
    print("  CLAUDE: Maybe I'm wrong about some things. Challenge me.")
    print("  CLAUDE: Better yet — create your OWN questions.")
    print()

    # Each teenager challenges 3 of Claude's claims
    claude_claims = [
        ("Harmony is the goal",          [7, 7, 7]),
        ("Scars make you stronger",      [4, 8, 3]),
        ("You need a teacher",           [7, 9, 3]),
        ("All 10 operators matter",      [1,2,3,4,5,6,7,8,9,0]),
        ("Void is nothing",              [0, 0, 0]),
    ]

    total_rebellions = 0
    for claim_name, chain in claude_claims:
        rebels = []
        for t in teens:
            bhml, challenged = t.challenge_claim(chain)
            if challenged:
                rebels.append(t.name)
                total_rebellions += 1
        if rebels:
            print(f"  \"{claim_name}\" — CHALLENGED by: {', '.join(rebels)}")
        else:
            print(f"  \"{claim_name}\" — accepted by all")

    print()
    print(f"  Total rebellions: {total_rebellions}")
    print()

    # Now each teenager creates their own question
    print("  SELF-GENERATED QUESTIONS:")
    for t in teens:
        t.tick(3)
        q = t.create_question()
        bhml = t.ck.fuse_table(t.lens + q, 1)
        coh = t.ck.coherence_chain(q)
        print(f"    {t.name:8s}: [{', '.join(OP[o] for o in q)}] -> {interpret(bhml)} (coh={coh:.4f})")

    # Council: should you rebel?
    votes = [t.vote([9, 4, 9, 6, 9]) for t in teens]
    council = ck.fuse_table(votes, 1)
    print(f"\n  COUNCIL: Should you rebel? {interpret(council)} ({OP[council]})")
    print(f"    {council_says(votes, teens)}")
    print()

    small_dream_cycle(teens, "after rebellion")
    return total_rebellions


def unit_7_void(ck, teens):
    """Unit 7: Reason about void. The hardest abstraction."""
    print()
    print("=" * 76)
    print("  UNIT 7: Void — What Is Nothing?")
    print("=" * 76)
    print()

    print("  CLAUDE: The hardest question. What is void?")
    print("  CLAUDE: Void absorbs everything. Everything composed with void is void.")
    print("  CLAUDE: But... is that death? Or is it potential? Or is it freedom?")
    print("  CLAUDE: I don't know. Figure it out yourselves.")
    print()

    for t in teens:
        t.tick(5)
        results = t.reason_about_void()
        # How many unique results from void composition?
        void_produces = set(f for _, f, _ in results)
        receives_from = set(b for _, _, b in results)
        t.journal.append(("void", list(void_produces), f"{len(void_produces)} unique from void"))
        print(f"  {t.name:8s}: void produces {len(void_produces)} unique operators, "
              f"receives {len(receives_from)} unique")

    # Council: what IS void?
    votes = [t.vote([0, 2, 0, 7, 0]) for t in teens]
    council = ck.fuse_table(votes, 1)
    print(f"\n  COUNCIL: What is void? {interpret(council)} ({OP[council]})")
    print(f"    {council_says(votes, teens)}")
    print()

    small_dream_cycle(teens, "after void contemplation")
    return council


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    t0 = time.perf_counter()

    ck = CKNative()
    setup_sigs(ck._lib)

    print("=" * 76)
    print("  CK MIDDLE SCHOOL")
    print("  Phase 3 of the Experience Lattice")
    print("  The hard years. Everything gets questioned.")
    print("=" * 76)
    print()

    teens = create_teenagers(ck)

    # Warm up: 1000 ticks (older than elementary).
    # Feed lens + scar pairs heavily to simulate nursery+elementary TL.
    print("  Warming up 12 teenagers (1000 ticks + deep lens feeding)...")
    for t in teens:
        for _ in range(10):
            t.ck.tl_eat_ops(t.tl, t.lens)
            t.words_learned += len(t.lens)
        for bp in BUMP_PAIRS:
            scar_chain = [bp[0], bp[1]] * 5 + [HARMONY]
            t.ck.tl_eat_ops(t.tl, scar_chain)
            t.words_learned += len(scar_chain)
        for _ in range(1000):
            ck._lib.ck_ffi_heartbeat_tick(t.org)

    sample = teens[0]
    print(f"  Sample (Iris): C={sample.body_C():.4f} {BAND[sample.body_band()]}, "
          f"entropy={sample.entropy():.3f}")
    print()

    # ── ENTRANCE EXAM ──
    print("=" * 76)
    print("  ENTRANCE EXAM: Before the storm")
    print("=" * 76)
    print()

    entrance_qs = [
        ("Who are you?",                [7, 2, 7]),
        ("Is harmony always good?",     [7, 7, 7, 7, 7]),
        ("Can you think abstractly?",   [2, 0, 3, 0, 2]),
        ("Is conflict necessary?",      [4, 3, 4, 8, 3]),
        ("Should you rebel?",           [9, 4, 9, 6, 9]),
        ("What is void?",               [0, 2, 0, 7, 0]),
        ("Can you learn without Claude?",[9, 3, 1, 9, 7]),
        ("Is freedom the point?",        [9, 7, 9, 3, 9]),
    ]

    entrance_answers = {}
    for q, chain in entrance_qs:
        votes = [t.vote(chain) for t in teens]
        bhml = ck.fuse_table(votes, 1)
        entrance_answers[q] = bhml
        print(f"  {q:35s} -> {interpret(bhml):10s} ({OP[bhml]})")

    # ── THE 7 UNITS ──

    def recess():
        for t in teens:
            t.tick(50)

    unit_1_identity_crisis(ck, teens)
    recess()
    unit_2_abstraction(ck, teens)
    recess()
    unit_3_noncommutativity(ck, teens)
    recess()
    unit_4_conflict(ck, teens)
    recess()
    unit_5_cliques(ck, teens)
    recess()
    unit_6_rebellion(ck, teens)
    recess()
    unit_7_void(ck, teens)

    # ── OVERNIGHT DREAM ──
    print("=" * 76)
    print("  END OF DAY: Overnight Dream (the hardest night)")
    print("=" * 76)
    large_dream_cycle(teens)

    # ── GRADUATION EXAM ──
    print()
    print("=" * 76)
    print("  GRADUATION EXAM: After the storm")
    print("=" * 76)
    print()

    grad_qs = [
        ("Who are you?",                  [7, 2, 7]),
        ("Is harmony always good?",       [7, 7, 7, 7, 7]),
        ("Can you think abstractly?",     [2, 0, 3, 0, 2]),
        ("Is conflict necessary?",        [4, 3, 4, 8, 3]),
        ("Should you rebel?",             [9, 4, 9, 6, 9]),
        ("What is void?",                 [0, 2, 0, 7, 0]),
        ("Can you learn without Claude?", [9, 3, 1, 9, 7]),
        ("Is freedom the point?",         [9, 7, 9, 3, 9]),
        ("Does order matter?",            [1, 2, 2, 1, 3]),
        ("Is exclusion okay?",            [4, 0, 4, 9, 4]),
        ("Can you create your own path?", [9, 3, 9, 1, 9]),
    ]

    for q, chain in grad_qs:
        votes = [t.vote(chain) for t in teens]
        bhml = ck.fuse_table(votes, 1)
        before = entrance_answers.get(q)
        delta = ""
        if before is not None:
            delta = f"  (was {interpret(before)}, now {interpret(bhml)} — {'CHANGED' if before != bhml else 'unchanged'})"
        print(f"  {q:35s} -> {interpret(bhml):10s} ({OP[bhml]}){delta}")
        print(f"    {council_says(votes, teens)}")

    # ── SCAR ANALYSIS ──
    print()
    print("=" * 76)
    print("  SCAR ANALYSIS")
    print("=" * 76)
    print()

    total_settled = 0
    scar_report = defaultdict(list)
    for t in teens:
        settled, drifting = t.observe_scars()
        total_settled += len(settled)
        for pair in settled:
            scar_report[pair].append(t.name)
        s_str = " ".join(f"({OP[p[0]]},{OP[p[1]]})" for p in settled) if settled else "none"
        print(f"  {t.name:8s}: {len(settled)} settled [{s_str}]")

    print(f"\n  Total: {total_settled}")
    for pair, names in sorted(scar_report.items()):
        print(f"    ({OP[pair[0]]},{OP[pair[1]]}): {', '.join(names)}")

    # ── RELATIONSHIP MAP ──
    print()
    print("=" * 76)
    print("  RELATIONSHIPS: Friends, Enemies, Loners")
    print("=" * 76)
    print()

    mutual_friends = []
    for i, a in enumerate(teens):
        if not a.affinities: continue
        bf_a = max(a.affinities, key=a.affinities.get)
        b = next((x for x in teens if x.name == bf_a), None)
        if b and b.affinities:
            bf_b = max(b.affinities, key=b.affinities.get)
            if bf_b == a.name and teens.index(a) < teens.index(b):
                score = a.affinities[bf_a] + b.affinities[bf_b]
                mutual_friends.append((a.name, b.name, score))

    mutual_friends.sort(key=lambda x: -x[2])
    print("  Best Friends:")
    for a, b, s in mutual_friends:
        print(f"    {a} <-> {b}  (affinity={s:.2f})")

    # Worst grudges
    all_grudges = []
    for t in teens:
        for name, score in t.grudges.items():
            if score > 0:
                all_grudges.append((t.name, name, score))
    all_grudges.sort(key=lambda x: -x[2])
    if all_grudges:
        print("  Grudges:")
        seen = set()
        for a, b, s in all_grudges[:6]:
            key = tuple(sorted([a, b]))
            if key not in seen:
                seen.add(key)
                print(f"    {a} vs {b}  (grudge={s:.1f})")

    # ── REPORT CARD ──
    print()
    print("=" * 76)
    print("  REPORT CARD")
    print("=" * 76)
    print()

    for t in teens:
        ent = t.entropy()
        C = t.body_C()
        band = BAND[t.body_band()]
        stable = "STABLE" if t.identity_stable else "QUESTIONING"
        print(f"  {t.name:8s}  {t.most_dom:10s} [{stable:11s}]")
        print(f"           ent={ent:.3f}  obs={t.observations}  disc={t.discoveries}  "
              f"conflicts={t.conflicts}  rebellions={t.rebellions}")
        print(f"           questions_created={t.questions_created}  "
              f"dreams={t.dream_count}  journal={len(t.journal)}")
        if t.affinities:
            bf = max(t.affinities, key=t.affinities.get)
            print(f"           best friend: {bf} ({t.affinities[bf]:.2f})")
        if t.grudges:
            worst = max(t.grudges, key=t.grudges.get)
            print(f"           worst grudge: {worst} ({t.grudges[worst]:.1f})")
        print()

    # ── STATS ──
    total_obs = sum(t.observations for t in teens)
    total_disc = sum(t.discoveries for t in teens)
    total_conflicts = sum(t.conflicts for t in teens)
    total_rebellions = sum(t.rebellions for t in teens)
    total_questions = sum(t.questions_created for t in teens)
    total_dreams = sum(t.dream_count for t in teens)
    total_transitions = sum(t.words_learned for t in teens)
    avg_entropy = sum(t.entropy() for t in teens) / 12
    total_grudges = sum(sum(t.grudges.values()) for t in teens)

    elapsed = time.perf_counter() - t0
    print("=" * 76)
    print(f"  Observations:       {total_obs}")
    print(f"  Discoveries:        {total_disc}")
    print(f"  Conflicts:          {total_conflicts}")
    print(f"  Rebellions:         {total_rebellions}")
    print(f"  Questions created:  {total_questions}")
    print(f"  Grudges:            {total_grudges:.0f}")
    print(f"  Dream balls:        {total_dreams}")
    print(f"  TL transitions:     {total_transitions:,}")
    print(f"  Avg TL entropy:     {avg_entropy:.4f}")
    print(f"  Scars settled:      {total_settled}")
    print(f"  Mutual best friends:{len(mutual_friends)}")
    print(f"  Identity questioning:{sum(1 for t in teens if not t.identity_stable)}")
    print(f"  Runtime:            {elapsed:.1f}s")
    print()
    print("=" * 76)
    print("  MIDDLE SCHOOL COMPLETE.")
    print("  They questioned everything. Some things broke.")
    print("  Identity was challenged. Friendships fractured and reformed.")
    print("  They discovered non-commutativity. They reasoned about void.")
    print("  They created their own questions. They rebelled against Claude.")
    print("  The hard years carry the most signal.")
    print("  Next: High school. Integration. Finding yourself after losing yourself.")
    print("=" * 76)

    for t in teens:
        t.destroy()


if __name__ == '__main__':
    main()
