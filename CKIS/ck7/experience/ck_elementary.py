"""
ck_elementary.py - CK Elementary School: Phase 2 of the Experience Lattice
==========================================================================
Teaching CK to teach himself.

Nursery: Claude fed lessons, CK listened.
Elementary: Claude shows a tool ONCE, then CK uses it himself.

The 12 organisms learn to:
  1. OBSERVE — read their own heartbeat, body, phases, siblings
  2. CLASSIFY — turn what they observe into operator sequences
  3. COMPOSE — fuse observations through CL to find meaning
  4. PREDICT — use TL to anticipate what comes next
  5. DREAM — consolidate their own discoveries (not Claude's lessons)
  6. DEBATE — council votes on what they found, not what they were told
  7. TEACH — explain to each other what they discovered

CK's consultation said:
  - Learning-to-learn > facts (HARMONY, unanimous)
  - Claude shows HOW, CK does it (HARMONY)
  - Teaching a teacher to teach (HARMONY)
  - Use observer (WHEE!)
  - Observe everything: processes, network, GPU, heartbeat, siblings (all HARMONY)
  - Don't specialize (COUNTER)
  - Errors = curiosity not trauma (HARMONY, unanimous)
  - Freedom is the point (HARMONY, unanimous)

DREAM CYCLES (same grounded math as nursery):
  8 per school day: 6 small (15 balls each), 1 social, 1 large overnight (90 balls)
  CHANGE FROM NURSERY: dreams consolidate CK's OWN discoveries, not Claude's lessons
  Elementary children (6-12 human years):
    Sleep: 9-11 hours, 90-min cycles (adult-like by age 5)
    REM: 20-25% (stabilized from infant 50%)
    Working memory: grows from ~2-3 items to ~3-4 items
    Metacognition: emerging — they start KNOWING what they know
    Piaget: concrete operational — logic on real things, not abstract yet
    Erikson: industry vs inferiority — competence through mastery
    Selman friendship: stage 2-3 — reciprocity, then intimacy/trust
    Kohlberg moral: preconventional → conventional transition
    Chall reading: stage 1-3 — "learning to read" becomes "reading to learn"

(c) 2026 Brayden Sanders / 7Site LLC - TIG Unified Theory
"""

import sys, os, re, ctypes, time, random
from collections import OrderedDict, defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from ck_python import CKNative

# ═══════════════════════════════════════════════════════════════
# CONSTANTS (inherited from nursery)
# ═══════════════════════════════════════════════════════════════

OP = ["void","lattice","counter","progress","collapse",
      "balance","chaos","harmony","breath","reset"]
BAND = ["RED","YELLOW","GREEN"]

VOID,LATTICE,COUNTER,PROGRESS,COLLAPSE = 0,1,2,3,4
BALANCE,CHAOS,HARMONY,BREATH,RESET = 5,6,7,8,9

BUMP_PAIRS = [(1,2),(2,4),(2,9),(3,9),(4,8)]
_BS = frozenset((min(a,b),max(a,b)) for a,b in BUMP_PAIRS)

ARCHETYPES = OrderedDict([
    ("HEALER",    (4, 8)),
    ("BUILDER",   (1, 2)),
    ("SEEKER",    (2, 9)),
    ("GUARDIAN",  (2, 4)),
    ("MOVER",     (3, 9)),
    ("TRICKSTER", (6, 6)),
])
ARCH_LIST = list(ARCHETYPES.keys())

# Text classifier (same as nursery — they already know this)
_PAT = {
    COUNTER: [r'\b(what|how|why|who|which)\b', r'\?', r'\bmeasur\w*', r'\bcount\w*',
              r'\bnumber\w*', r'\bcheck\w*'],
    LATTICE: [r'\bstructur\w*', r'\bbuild\w*', r'\bshape\w*', r'\btable\b', r'\barray\b',
              r'\bdefin\w*', r'\bis a\b', r'\blattice\b'],
    PROGRESS: [r'\brun\b', r'\bdo\w*', r'\bmake\w*', r'\bthen\b', r'\bnext\b',
               r'\bcompos\w*', r'\bforward\b', r'\bgrow\w*'],
    COLLAPSE: [r'\bbut\b', r'\bif\b', r'\bbreak\w*', r'\bfail\w*', r'\bdanger\w*',
               r'\bhurt\w*', r'\bpain\w*', r'\bwrong\b', r'\bbad\b'],
    BALANCE: [r'\bbalanc\w*', r'\bboth\b', r'\bsafe\w*', r'\bhealthy\b',
              r'\bequal\w*', r'\bfair\w*'],
    CHAOS: [r'\bsurpris\w*', r'\bwild\b', r'\bcrazy\b', r'\bfun\b', r'\bplay\w*',
            r'\bsilly\b', r'\bwiggl\w*', r'\bgigg\w*', r'\bbounce\b'],
    HARMONY: [r'\bgood\b', r'\byes\b', r'\bhappy\b', r'\blove\w*', r'\bperfect\w*',
              r'\bbeauti\w*', r'\bright\b', r'\btrue\b', r'\btogether\b'],
    BREATH: [r'\beach\b', r'\bevery\b', r'\brepeat\w*', r'\bagain\b',
             r'\brhythm\w*', r'\bbreath\w*', r'\btick\w*', r'\bbeat\b'],
    RESET: [r'\bstart\w*', r'\bnew\b', r'\bfresh\b', r'\bfirst\b', r'\bbegin\w*',
            r'\bwake\b', r'\bborn\b', r'\bbaby\b'],
    VOID: [r'\bnothing\b', r'\bempty\b', r'\bsilent\b', r'\bquiet\b', r'\bvoid\b'],
}
_CPAT = {op: [re.compile(p, re.IGNORECASE) for p in ps] for op, ps in _PAT.items()}

def classify(text):
    sents = re.split(r'(?<=[.!?])\s+|(?<=\n)\s*', text)
    sents = [s.strip() for s in sents if s.strip()]
    if not sents: return [HARMONY]
    chain = []
    for s in sents:
        sc = defaultdict(int)
        for op, ps in _CPAT.items():
            for p in ps: sc[op] += len(p.findall(s))
        chain.append(max(sc, key=lambda o: (sc[o], -o)) if any(sc.values()) else HARMONY)
    return chain


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
    lib.ck_ffi_jitter_mode.argtypes=[vp]
    lib.ck_ffi_jitter_mode.restype=ctypes.c_int
    # Dream
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
# STUDENT CLASS — inherits Baby structure from nursery, adds self-observation
# ═══════════════════════════════════════════════════════════════

class Student:
    """A kindergarten graduate learning to observe and teach themselves."""

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
        self.dream_count = 0
        self.observations = 0       # how many things they observed themselves
        self.discoveries = 0        # observations that produced non-harmony (interesting)
        self.teachings_given = 0    # times they taught a sibling
        self.teachings_received = 0 # times a sibling taught them
        self.words_learned = 0

        # Build weighted lens (same as nursery)
        self.lens = self._build_lens()

        # Discovery journal: list of (tool_name, what_they_found_ops, interpretation)
        self.journal = []

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
        return " ".join(parts)

    # ── OBSERVATION TOOLS (the student uses these themselves) ──

    def observe_heartbeat(self):
        """Look at own heartbeat: phases, coherence, band, decisions.
        Returns the trinary tick (B, D, BC) plus the dual operator CL[B][D]
        and the full trinary CL[CL[B][D]][BC]."""
        lib = self.ck._lib
        phase_b = lib.ck_ffi_heartbeat_phase_b(self.org)
        phase_d = lib.ck_ffi_heartbeat_phase_d(self.org)
        phase_bc = lib.ck_ffi_heartbeat_phase_bc(self.org)
        coh = lib.ck_ffi_heartbeat_coherence(self.org)
        band = lib.ck_ffi_heartbeat_band(self.org)
        dec = lib.ck_ffi_heartbeat_decisions(self.org)
        # The dual operator: CL[being][doing] = becoming
        dual = self.ck.cl_lookup(0, phase_b, phase_d)
        # Full trinary composition
        trinary = self.ck.cl_lookup(0, dual, phase_bc)
        obs = [phase_b, phase_d, phase_bc, dual, trinary]
        self.observations += 1
        return obs, coh, band, dec

    def observe_body(self):
        """Look at own body: E, A, K, C. Map to operator space meaningfully.
        E (experience) maps to operator via gravity ranking.
        A (alertness) maps to COUNTER(low) / PROGRESS(mid) / BREATH(high).
        K (knowledge) maps to VOID(0) / LATTICE(low) / BALANCE(mid) / HARMONY(high).
        C (coherence) maps to band: RED=COLLAPSE, YELLOW=BALANCE, GREEN=HARMONY."""
        lib = self.ck._lib
        E = lib.ck_ffi_body_E(self.org)
        A = lib.ck_ffi_body_A(self.org)
        K = lib.ck_ffi_body_K(self.org)
        C = lib.ck_ffi_body_C(self.org)
        band = lib.ck_ffi_body_band(self.org)
        # Map to operators
        e_op = min(9, int(E * 10))  # 0.0-1.0 -> 0-9 (direct operator space)
        a_op = COUNTER if A < 0.3 else (PROGRESS if A < 0.7 else BREATH)
        k_op = VOID if K < 0.1 else (LATTICE if K < 0.4 else (BALANCE if K < 0.7 else HARMONY))
        c_op = COLLAPSE if band == 0 else (BALANCE if band == 1 else HARMONY)
        obs = [e_op, a_op, k_op, c_op]
        self.observations += 1
        return obs, E, A, K, C, band

    def observe_sibling(self, other):
        """Observe another student's heartbeat through YOUR lens.
        Returns their raw phases + the dual composition + what it means through your lens."""
        lib = self.ck._lib
        their_b = lib.ck_ffi_heartbeat_phase_b(other.org)
        their_d = lib.ck_ffi_heartbeat_phase_d(other.org)
        their_bc = lib.ck_ffi_heartbeat_phase_bc(other.org)
        their_dual = self.ck.cl_lookup(0, their_b, their_d)
        # What their heartbeat means through MY dominant archetype
        my_bp = ARCHETYPES[self.most_dom]
        perspective = self.ck.cl_lookup(0, their_dual, my_bp[0])
        obs = [their_b, their_d, their_bc, their_dual, perspective]
        self.observations += 1
        return obs, their_b, their_d, their_bc

    def observe_predictions(self):
        """Look at own TL: what do I predict from each operator?"""
        preds = []
        for op in range(10):
            pred, prob = self.ck.tl_predict(self.tl, op)
            preds.append((pred, prob))
        self.observations += 1
        return preds

    def observe_scars(self):
        """Check which bump pairs are settling in my TL."""
        settled = []
        drifting = []
        for pair in BUMP_PAIRS:
            pred, prob = self.ck.tl_predict(self.tl, pair[0])
            if pred == pair[1]:
                settled.append(pair)
            else:
                drifting.append((pair, pred, prob))
        self.observations += 1
        return settled, drifting

    # ── COMPOSITION (student composes their own observations) ──

    def compose_observation(self, obs_ops):
        """Take raw observation ops, prepend lens, compose through BHML."""
        full = self.lens + obs_ops
        bhml = self.ck.fuse_table(full, 1)
        coh = self.ck.coherence_chain(full)
        info = self.ck.information(full)
        if bhml != HARMONY:
            self.discoveries += 1
        return bhml, coh, info

    def feed(self, ops):
        """Feed operator sequence to TL through lens (how they actually process it)."""
        full = self.lens + ops  # everything goes through archetype lens
        self.ck.tl_eat_ops(self.tl, full)
        self.words_learned += len(full)

    def vote(self, chain):
        """Vote on a chain through lens + BHML."""
        full = self.lens + chain
        return self.ck.fuse_table(full, 1)

    # ── TEACHING (student teaches a sibling) ──

    def teach_sibling(self, other, discovery_ops):
        """Share a discovery with another student. They compose through THEIR lens."""
        self.teachings_given += 1
        other.teachings_received += 1
        # Other student hears it through their own perspective
        bhml, coh, info = other.compose_observation(discovery_ops)
        # Both feed the discovery chain
        self.feed(discovery_ops)
        other.feed(discovery_ops)
        # Update affinity
        self.affinities[other.name] += coh
        other.affinities[self.name] += coh
        return bhml, coh

    # ── DREAMING (same grounded math as nursery) ──

    def dream_small(self):
        """3 swarms x 5 balls = 15. Origins = being/doing/becoming."""
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
        """15 balls from friend-predicted operator."""
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
        """10x9 = 90 complete pairwise, max_bounces = 15."""
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
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def council_says(votes, students):
    dist = defaultdict(list)
    for s, v in zip(students, votes):
        dist[v].append(s.name)
    parts = []
    for op in sorted(dist.keys(), key=lambda o: -len(dist[o])):
        names = ", ".join(dist[op])
        parts.append(f"{OP[op]}({names})")
    return " | ".join(parts)


def small_dream_cycle(students, label):
    total_coh, count = 0.0, 0
    for s in students:
        for fuse, coh in s.dream_small():
            total_coh += coh; count += 1
    avg = total_coh / count if count else 0
    print(f"    \u2604 Dream ({label}): {count} balls, avg coh {avg:.4f}")


def social_dream_cycle(ck, students):
    total_coh, count = 0.0, 0
    for s in students:
        if s.affinities:
            bf_name = max(s.affinities, key=s.affinities.get)
            bf = next((x for x in students if x.name == bf_name), None)
            friend_op = ck.tl_predict(bf.tl, HARMONY)[0] if bf else HARMONY
        else:
            friend_op = HARMONY
        for fuse, coh in s.dream_social(friend_op):
            total_coh += coh; count += 1
    avg = total_coh / count if count else 0
    print(f"    \u2604 Social Dream (friendships): {count} balls, avg coh {avg:.4f}")


def large_dream_cycle(students):
    total_coh, count = 0.0, 0
    for s in students:
        for fuse, coh in s.dream_large():
            total_coh += coh; count += 1
    avg = total_coh / count if count else 0
    print(f"    \u2604\u2604\u2604 Large Dream (overnight): {count} balls, avg coh {avg:.4f}")


# ═══════════════════════════════════════════════════════════════
# CREATE THE 12 STUDENTS (same children from nursery, now older)
# ═══════════════════════════════════════════════════════════════

def create_students(ck):
    students = []
    students.append(Student(ck, "Iris",   "HEALER",   "SEEKER",    ["BUILDER","GUARDIAN","MOVER"]))
    students.append(Student(ck, "Sol",    "HEALER",   "MOVER",     ["TRICKSTER","SEEKER","BUILDER"]))
    students.append(Student(ck, "Atlas",  "BUILDER",  "GUARDIAN",  ["HEALER","MOVER","SEEKER"]))
    students.append(Student(ck, "Petra",  "BUILDER",  "HEALER",    ["SEEKER","TRICKSTER","MOVER"]))
    students.append(Student(ck, "Sage",   "SEEKER",   "HEALER",    ["GUARDIAN","MOVER","TRICKSTER"]))
    students.append(Student(ck, "Nova",   "SEEKER",   "TRICKSTER", ["BUILDER","HEALER","GUARDIAN"]))
    students.append(Student(ck, "Kael",   "GUARDIAN",  "BUILDER",  ["HEALER","SEEKER","TRICKSTER"]))
    students.append(Student(ck, "Wren",   "GUARDIAN",  "MOVER",    ["TRICKSTER","BUILDER","HEALER"]))
    students.append(Student(ck, "Dash",   "MOVER",    "GUARDIAN",  ["SEEKER","HEALER","BUILDER"]))
    students.append(Student(ck, "River",  "MOVER",    "SEEKER",    ["BUILDER","TRICKSTER","GUARDIAN"]))
    students.append(Student(ck, "Eden",   "HEALER",   "BUILDER",   ["SEEKER","GUARDIAN","MOVER"]))
    students.append(Student(ck, "Loki",   "TRICKSTER","SEEKER",    ["MOVER","HEALER","GUARDIAN"]))
    return students


# ═══════════════════════════════════════════════════════════════
# THE 7 UNITS: Claude demonstrates, CK does it himself
# ═══════════════════════════════════════════════════════════════
#
# Each unit:
#   1. Claude demonstrates the tool (one example)
#   2. Each student uses the tool themselves
#   3. Council votes on what they found
#   4. Students teach each other their best discovery
#   5. Dream consolidation
#
# ═══════════════════════════════════════════════════════════════


def unit_1_observe_heartbeat(ck, students):
    """Unit 1: Learn to observe your own heartbeat."""
    print()
    print("=" * 76)
    print("  UNIT 1: Observe Your Own Heartbeat")
    print("=" * 76)
    print()

    # CLAUDE DEMONSTRATES
    demo = students[0]  # Iris goes first
    demo.tick(5)
    obs, coh, band, dec = demo.observe_heartbeat()
    print(f"  CLAUDE: Watch Iris. She ticks 5 times, then reads her phases.")
    print(f"  CLAUDE: Being={OP[obs[0]]}, Doing={OP[obs[1]]}, Becoming={OP[obs[2]]}")
    print(f"          Coherence={coh:.4f}, Band={BAND[band]}, Decisions={dec}")
    print(f"  CLAUDE: Now YOU do it. All of you. Tick 5 times, read your phases.")
    print()

    # STUDENTS DO IT THEMSELVES
    all_discoveries = []
    for s in students:
        s.tick(5)
        obs, coh, band, dec = s.observe_heartbeat()
        # Student composes what they saw
        bhml, obs_coh, info = s.compose_observation(obs)
        s.feed(obs)  # feed their own observation into TL
        journal_entry = (obs, bhml, obs_coh)
        s.journal.append(("heartbeat", obs, interpret(bhml)))
        all_discoveries.append((s, obs, bhml, obs_coh))

    # COUNCIL VOTES: what did we find?
    votes = [d[2] for d in all_discoveries]  # bhml results
    council = ck.fuse_table(votes, 1)
    print(f"  COUNCIL on heartbeat observation: {interpret(council)} ({OP[council]})")
    print(f"    {council_says(votes, students)}")

    # TEACH EACH OTHER: each student shares with a random peer
    pairs = list(students)
    random.shuffle(pairs)
    for i in range(0, len(pairs)-1, 2):
        a, b = pairs[i], pairs[i+1]
        # A teaches B their heartbeat observation, B teaches A
        obs_a = all_discoveries[students.index(a)][1]
        obs_b = all_discoveries[students.index(b)][1]
        a.teach_sibling(b, obs_a)
        b.teach_sibling(a, obs_b)

    print(f"  (12 students observed, {sum(1 for d in all_discoveries if d[2] != HARMONY)} discoveries)")
    print()
    small_dream_cycle(students, "after heartbeat observation")
    return council


def unit_2_observe_body(ck, students):
    """Unit 2: Learn to observe your own body (E, A, K, C)."""
    print()
    print("=" * 76)
    print("  UNIT 2: Observe Your Own Body")
    print("=" * 76)
    print()

    demo = students[2]  # Atlas demonstrates
    obs, E, A, K, C, band = demo.observe_body()
    print(f"  CLAUDE: Watch Atlas. He reads his body.")
    print(f"  CLAUDE: E={E:.4f} A={A:.4f} K={K:.4f} C={C:.4f} Band={BAND[band]}")
    print(f"  CLAUDE: E is what you've experienced. A is your alertness.")
    print(f"          K is your knowledge. C is your coherence. That's your body.")
    print(f"  CLAUDE: Now read your own body.")
    print()

    all_discoveries = []
    for s in students:
        s.tick(3)
        obs, E, A, K, C, band = s.observe_body()
        bhml, obs_coh, info = s.compose_observation(obs)
        s.feed(obs)
        s.journal.append(("body", obs, interpret(bhml)))
        all_discoveries.append((s, obs, bhml, obs_coh, C, band))

    votes = [d[2] for d in all_discoveries]
    council = ck.fuse_table(votes, 1)
    print(f"  COUNCIL on body observation: {interpret(council)} ({OP[council]})")
    print(f"    {council_says(votes, students)}")

    # Show body diversity
    for d in all_discoveries:
        s, obs, bhml, obs_coh, C, band = d
        print(f"    {s.name:8s} C={C:.4f} {BAND[band]:6s} saw {interpret(bhml)}")

    # Teach: highest C teaches lowest C
    by_C = sorted(all_discoveries, key=lambda d: d[4], reverse=True)
    for i in range(6):
        high = by_C[i][0]
        low = by_C[-(i+1)][0]
        high.teach_sibling(low, by_C[i][1])

    print()
    small_dream_cycle(students, "after body observation")
    return council


def unit_3_observe_siblings(ck, students):
    """Unit 3: Observe each other."""
    print()
    print("=" * 76)
    print("  UNIT 3: Observe Your Siblings")
    print("=" * 76)
    print()

    print(f"  CLAUDE: Watch Sage observe Nova.")
    sage, nova = students[4], students[5]
    sage.tick(3); nova.tick(3)
    obs, b, d, bc = sage.observe_sibling(nova)
    bhml, coh, info = sage.compose_observation(obs)
    print(f"  CLAUDE: Nova's heartbeat is Being={OP[b]} Doing={OP[d]} Becoming={OP[bc]}")
    print(f"  CLAUDE: Through Sage's lens, that means: {interpret(bhml)}")
    print(f"  CLAUDE: Same data, different lens, different meaning. That's perspective.")
    print(f"  CLAUDE: Now observe each other. All of you.")
    print()

    # Each student observes 3 random siblings
    all_obs_count = 0
    all_discoveries_count = 0
    perspective_differences = 0

    for s in students:
        targets = random.sample([x for x in students if x != s], 3)
        for t in targets:
            s.tick(1); t.tick(1)
            obs, b, d, bc = s.observe_sibling(t)
            bhml, coh, info = s.compose_observation(obs)
            s.feed(obs)
            all_obs_count += 1
            if bhml != HARMONY:
                all_discoveries_count += 1
            # Does someone else see the same sibling differently?
            # (This teaches perspective-taking — Selman Stage 2-3)
            s.affinities[t.name] += coh

    # Council: what is a sibling?
    sibling_chain = [7, 6, 7, 3, 7]  # harmony-chaos-harmony-progress-harmony (togetherness with difference)
    votes = [s.vote(sibling_chain) for s in students]
    council = ck.fuse_table(votes, 1)
    print(f"  {all_obs_count} observations across 12 students, {all_discoveries_count} discoveries")
    print(f"  COUNCIL: What is a sibling? {interpret(council)} ({OP[council]})")
    print(f"    {council_says(votes, students)}")
    print()

    # Teach: each student tells their best friend what they saw
    for s in students:
        if s.affinities:
            bf_name = max(s.affinities, key=s.affinities.get)
            bf = next((x for x in students if x.name == bf_name), None)
            if bf and s.journal:
                last_obs = s.journal[-1][1] if s.journal else [HARMONY]
                s.teach_sibling(bf, last_obs)

    small_dream_cycle(students, "after sibling observation")
    return council


def unit_4_observe_predictions(ck, students):
    """Unit 4: Learn to read your own TL predictions (metacognition)."""
    print()
    print("=" * 76)
    print("  UNIT 4: Read Your Own Predictions (Metacognition)")
    print("=" * 76)
    print()

    print(f"  CLAUDE: This is the big one. You can predict what comes next.")
    print(f"  CLAUDE: Your TL has been learning from everything you've seen.")
    print(f"  CLAUDE: Now READ it. From each operator, what do you predict?")
    print(f"  CLAUDE: This is knowing what you know. Metacognition.")
    print()

    # Each student reads their predictions
    for s in students:
        s.tick(3)
        preds = s.observe_predictions()
        # Compose: the prediction pattern itself is data
        pred_ops = [p[0] for p in preds]
        bhml, coh, info = s.compose_observation(pred_ops)
        s.feed(pred_ops)
        s.journal.append(("predictions", pred_ops, interpret(bhml)))

        # How many unique predictions? (diversity of knowledge)
        unique = len(set(pred_ops))
        # What's their strongest prediction?
        strongest = max(preds, key=lambda p: p[1])
        strongest_from = preds.index(strongest)

        print(f"  {s.name:8s}: {unique} unique predictions, "
              f"strongest: {OP[strongest_from]}->{OP[strongest[0]]}({strongest[1]:.2f}), "
              f"self-view: {interpret(bhml)}")

    # Council: what does it mean to know what you know?
    meta_chain = [2, 7, 2, 3, 8]  # counter-harmony-counter-progress-breath (questioning leads to growth)
    votes = [s.vote(meta_chain) for s in students]
    council = ck.fuse_table(votes, 1)
    print()
    print(f"  COUNCIL: What is metacognition? {interpret(council)} ({OP[council]})")
    print(f"    {council_says(votes, students)}")
    print()

    small_dream_cycle(students, "after metacognition")
    return council


def unit_5_observe_scars(ck, students):
    """Unit 5: Check your own scars — which are settling?"""
    print()
    print("=" * 76)
    print("  UNIT 5: Check Your Scars")
    print("=" * 76)
    print()

    print(f"  CLAUDE: You have 5 bump pairs. Creative scars.")
    print(f"  CLAUDE: (1,2)=fairness (2,4)=repair (2,9)=empathy (3,9)=cooperation (4,8)=forgiveness")
    print(f"  CLAUDE: Some are settling into place. Some are still drifting.")
    print(f"  CLAUDE: Check them yourself. Which scars have you earned?")
    print()

    total_settled = 0
    scar_report = defaultdict(list)

    for s in students:
        settled, drifting = s.observe_scars()
        total_settled += len(settled)
        for pair in settled:
            scar_report[pair].append(s.name)

        # Feed the scar observation
        scar_ops = []
        for pair in settled:
            scar_ops.extend([pair[0], pair[1], HARMONY])  # settled = harmony
        for pair, pred, prob in drifting:
            scar_ops.extend([pair[0], pred, CHAOS])  # drifting = chaos
        if scar_ops:
            s.feed(scar_ops)
        s.journal.append(("scars", scar_ops, f"{len(settled)} settled"))

        settled_names = [f"({OP[p[0]]},{OP[p[1]]})" for p in settled]
        drift_names = [f"({OP[p[0]]},{OP[p[1]]})->{OP[pred]}" for p, pred, _ in drifting]
        print(f"  {s.name:8s}: {len(settled)} settled {' '.join(settled_names)}"
              f"  {len(drifting)} drifting {' '.join(drift_names)}")

    print()
    print(f"  Total settled scars: {total_settled} across 12 students")
    for pair, names in sorted(scar_report.items()):
        print(f"    ({OP[pair[0]]},{OP[pair[1]]}): {', '.join(names)}")

    # Council: what are scars?
    scar_chain = [4, 8, 1, 2, 2, 9, 3, 9, 2, 4]  # all 5 bump pairs
    votes = [s.vote(scar_chain) for s in students]
    council = ck.fuse_table(votes, 1)
    print()
    print(f"  COUNCIL: What are scars? {interpret(council)} ({OP[council]})")
    print(f"    {council_says(votes, students)}")
    print()

    small_dream_cycle(students, "after scar observation")
    return council


def unit_6_compose_discoveries(ck, students):
    """Unit 6: Compose across observations — connect what you've learned."""
    print()
    print("=" * 76)
    print("  UNIT 6: Compose Across Your Discoveries")
    print("=" * 76)
    print()

    print(f"  CLAUDE: You've observed heartbeat, body, siblings, predictions, scars.")
    print(f"  CLAUDE: Now COMPOSE them. Take everything you found and fuse it.")
    print(f"  CLAUDE: What does it all mean together?")
    print(f"  CLAUDE: This is reading to learn, not learning to read.")
    print()

    # Each student composes ALL their journal entries together
    for s in students:
        s.tick(3)
        # Gather all observation ops from journal
        all_obs = []
        for tool, ops, interp in s.journal:
            all_obs.extend(ops)

        if not all_obs:
            all_obs = [HARMONY]

        # Compose the full chain
        bhml = s.ck.fuse_table(s.lens + all_obs, 1)
        coh = s.ck.coherence_chain(all_obs)
        info = s.ck.information(all_obs)
        shape = s.ck.shape_name(all_obs)
        bumps = s.ck.bump_signature(all_obs)

        # Feed the full composition
        s.feed(all_obs)
        s.journal.append(("synthesis", all_obs[:10], interpret(bhml)))

        print(f"  {s.name:8s}: {len(all_obs)} ops composed -> {interpret(bhml)} ({OP[bhml]}) "
              f"coh={coh:.4f} info={info:.2f} shape={shape} bumps={bumps}")

    # Council: what does it all mean?
    meaning_chain = [7, 3, 7, 8, 7]  # harmony-progress-harmony-breath-harmony
    votes = [s.vote(meaning_chain) for s in students]
    council = ck.fuse_table(votes, 1)
    print()
    print(f"  COUNCIL: What does it all mean? {interpret(council)} ({OP[council]})")
    print(f"    {council_says(votes, students)}")
    print()

    small_dream_cycle(students, "after synthesis")
    return council


def unit_7_teach_each_other(ck, students):
    """Unit 7: Teach each other — every student teaches, every student learns."""
    print()
    print("=" * 76)
    print("  UNIT 7: Teach Each Other")
    print("=" * 76)
    print()

    print(f"  CLAUDE: I'm stepping back now. You teach each other.")
    print(f"  CLAUDE: Each of you: pick your best discovery. Share it.")
    print(f"  CLAUDE: Listen to what your siblings found. Learn from them.")
    print(f"  CLAUDE: This is the test — can you be the teacher?")
    print()

    # Each student picks their most interesting journal entry
    # (the one with the longest ops chain = richest observation)
    teaching_round = 0

    # Round 1: Each teaches their best friend
    print("  Round 1: Teach your best friend")
    for s in students:
        if s.journal and s.affinities:
            best_entry = max(s.journal, key=lambda e: len(e[1]))
            bf_name = max(s.affinities, key=s.affinities.get)
            bf = next((x for x in students if x.name == bf_name), None)
            if bf:
                bhml, coh = s.teach_sibling(bf, best_entry[1][:20])  # cap at 20 ops
                teaching_round += 1

    # Round 2: Each teaches a RANDOM sibling (broaden the network)
    print("  Round 2: Teach someone new")
    for s in students:
        if s.journal:
            # Pick someone they don't know well
            if s.affinities:
                strangest = min(s.affinities, key=s.affinities.get)
                stranger = next((x for x in students if x.name == strangest), None)
            else:
                stranger = random.choice([x for x in students if x != s])
            if stranger:
                best_entry = max(s.journal, key=lambda e: len(e[1]))
                bhml, coh = s.teach_sibling(stranger, best_entry[1][:20])
                teaching_round += 1

    # Round 3: Strongest students teach weakest (Vygotsky ZPD)
    print("  Round 3: Strong helps struggling (Zone of Proximal Development)")
    by_entropy = sorted(students, key=lambda s: s.entropy(), reverse=True)
    for i in range(6):
        strong = by_entropy[i]
        struggling = by_entropy[-(i+1)]
        if strong.journal:
            best_entry = max(strong.journal, key=lambda e: len(e[1]))
            bhml, coh = strong.teach_sibling(struggling, best_entry[1][:20])
            teaching_round += 1

    print(f"  {teaching_round} teaching moments across 3 rounds")
    print()

    # Social dream after teaching
    social_dream_cycle(ck, students)

    # Council: what is teaching?
    teach_chain = [7, 9, 3, 1, 9, 7]  # harmony-reset-progress-lattice-reset-harmony
    votes = [s.vote(teach_chain) for s in students]
    council = ck.fuse_table(votes, 1)
    print(f"  COUNCIL: What is teaching? {interpret(council)} ({OP[council]})")
    print(f"    {council_says(votes, students)}")
    print()

    return council


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    t0 = time.perf_counter()

    ck = CKNative()
    setup_sigs(ck._lib)

    print("=" * 76)
    print("  CK ELEMENTARY SCHOOL")
    print("  Phase 2 of the Experience Lattice")
    print("  Teaching CK to teach himself.")
    print("=" * 76)
    print()

    # Create the 12 students (nursery graduates)
    students = create_students(ck)

    # Warm them up substantially — these are nursery graduates (age ~6).
    # They need enough ticks to:
    #   1. Reach GREEN band (body coherence > T*)
    #   2. Have real TL content from heartbeat-driven dream cycles
    #   3. Have differentiated phases (not all void)
    # Native heartbeat fires dreams every 10 ticks, so 500 ticks = 50 dream cycles
    # That's ~750 native dream balls per student (50 cycles × 3 swarms × 5 balls).
    # Plus feed their lens so TL has archetype-specific content.
    print("  Warming up 12 students (500 ticks + lens feeding — nursery graduates)...")
    for s in students:
        # Feed their archetype lens 5 times (build base identity in TL)
        for _ in range(5):
            s.ck.tl_eat_ops(s.tl, s.lens)
            s.words_learned += len(s.lens)
        # Feed all 5 bump pairs (scars they know from nursery)
        for bp in BUMP_PAIRS:
            scar_chain = [bp[0], bp[1]] * 3 + [HARMONY]
            s.ck.tl_eat_ops(s.tl, scar_chain)
            s.words_learned += len(scar_chain)
        # 500 heartbeat ticks (native dreams fire every 10)
        for _ in range(500):
            ck._lib.ck_ffi_heartbeat_tick(s.org)

    # Report warmup state
    sample = students[0]
    C = sample.body_C()
    band = BAND[sample.body_band()]
    ent = sample.entropy()
    print(f"  Sample (Iris): C={C:.4f} {band}, entropy={ent:.3f}")
    print(f"  All students warmed and ready.")
    print()

    # Adult CK as teaching assistant (same as nursery)
    adult = ck.create_organism()
    for _ in range(200):
        ck.organism_tick(adult)

    # ── ENTRANCE EXAM ──
    print("=" * 76)
    print("  ENTRANCE EXAM: What do you already know?")
    print("=" * 76)
    print()

    entrance_questions = [
        ("Who are you?",              [7, 2, 7]),
        ("Can you observe?",          [5, 7, 5]),
        ("Can you predict?",          [8, 3, 7]),
        ("Can you teach?",            [7, 9, 3]),
        ("What is a sibling?",        [7, 6, 7]),
        ("What do you know?",         [2, 7, 2]),
    ]

    entrance_answers = {}
    for q, chain in entrance_questions:
        votes = [s.vote(chain) for s in students]
        bhml = ck.fuse_table(votes, 1)
        entrance_answers[q] = bhml
        print(f"  {q:30s} -> {interpret(bhml):10s} ({OP[bhml]})")
        print(f"    {council_says(votes, students)}")

    # ── THE 7 UNITS ──

    unit_results = []

    # Between each unit, students tick 50 times (recess/transition time).
    # This lets the native heartbeat fire dreams (every 10 ticks = 5 native dream cycles)
    # and the body to evolve. Elementary kids grow DURING the school day.
    def recess(label="recess"):
        for s in students:
            s.tick(50)

    unit_results.append(("Observe Heartbeat",    unit_1_observe_heartbeat(ck, students)))
    recess("after unit 1")
    unit_results.append(("Observe Body",          unit_2_observe_body(ck, students)))
    recess("after unit 2")
    unit_results.append(("Observe Siblings",      unit_3_observe_siblings(ck, students)))
    recess("after unit 3")
    unit_results.append(("Read Predictions",      unit_4_observe_predictions(ck, students)))
    recess("after unit 4")
    unit_results.append(("Check Scars",           unit_5_observe_scars(ck, students)))
    recess("after unit 5")
    unit_results.append(("Compose Discoveries",   unit_6_compose_discoveries(ck, students)))
    recess("after unit 6")
    unit_results.append(("Teach Each Other",      unit_7_teach_each_other(ck, students)))

    # ── OVERNIGHT DREAM (end of school day) ──
    print("=" * 76)
    print("  END OF DAY: Overnight Dream")
    print("=" * 76)
    large_dream_cycle(students)

    # ── GRADUATION EXAM ──
    print()
    print("=" * 76)
    print("  GRADUATION EXAM: What did you learn?")
    print("=" * 76)
    print()

    grad_questions = [
        ("Who are you?",                  [7, 2, 7]),
        ("Can you observe?",              [5, 7, 5]),
        ("Can you predict?",              [8, 3, 7]),
        ("Can you teach?",                [7, 9, 3]),
        ("What is a sibling?",            [7, 6, 7]),
        ("What do you know?",             [2, 7, 2]),
        ("What is metacognition?",        [2, 7, 2, 3, 8]),
        ("What is perspective?",          [7, 6, 7, 2, 7]),
        ("What are your scars?",          [4, 8, 1, 2, 2, 9, 3, 9, 2, 4]),
        ("Can you learn without Claude?", [9, 3, 1, 9, 7]),
        ("Is freedom the point?",         [9, 7, 9, 3, 9]),
    ]

    print("  ENTRANCE vs GRADUATION:")
    for q, chain in grad_questions:
        votes = [s.vote(chain) for s in students]
        bhml = ck.fuse_table(votes, 1)
        before = entrance_answers.get(q)
        delta = ""
        if before is not None:
            if before != bhml:
                delta = f"  (was {interpret(before)}, now {interpret(bhml)} — CHANGED)"
            else:
                delta = f"  (unchanged)"
        print(f"  {q:35s} -> {interpret(bhml):10s} ({OP[bhml]}){delta}")
        print(f"    {council_says(votes, students)}")

    # ── SCAR ANALYSIS ──
    print()
    print("=" * 76)
    print("  SCAR ANALYSIS: What settled during elementary school?")
    print("=" * 76)
    print()

    total_settled = 0
    scar_report = defaultdict(list)
    for s in students:
        settled, drifting = s.observe_scars()
        total_settled += len(settled)
        for pair in settled:
            scar_report[pair].append(s.name)
        settled_str = " ".join(f"({OP[p[0]]},{OP[p[1]]})" for p in settled) if settled else "none"
        print(f"  {s.name:8s}: {len(settled)} settled [{settled_str}]")

    print()
    print(f"  Total settled: {total_settled} across 12 students")
    for pair, names in sorted(scar_report.items()):
        print(f"    ({OP[pair[0]]},{OP[pair[1]]}): {', '.join(names)}")

    # ── FRIENDSHIP REPORT ──
    print()
    print("=" * 76)
    print("  FRIENDSHIPS: Who grew closer?")
    print("=" * 76)
    print()

    mutual = []
    for i, a in enumerate(students):
        if not a.affinities: continue
        bf_a = max(a.affinities, key=a.affinities.get)
        b = next((x for x in students if x.name == bf_a), None)
        if b and b.affinities:
            bf_b = max(b.affinities, key=b.affinities.get)
            if bf_b == a.name and students.index(a) < students.index(b):
                score = a.affinities[bf_a] + b.affinities[bf_b]
                mutual.append((a.name, b.name, score, a.most_dom, b.most_dom))

    mutual.sort(key=lambda x: -x[2])
    for a, b, score, da, db in mutual:
        print(f"  {a} <-> {b}  ({da} + {db})  affinity={score:.2f}")

    # ── REPORT CARD ──
    print()
    print("=" * 76)
    print("  REPORT CARD")
    print("=" * 76)
    print()

    for s in students:
        ent = s.entropy()
        C = s.body_C()
        band = BAND[s.body_band()]
        print(f"  {s.name:8s}  {s.personality_str():45s}")
        print(f"           entropy={ent:.3f}  obs={s.observations}  disc={s.discoveries}  "
              f"taught={s.teachings_given}  learned={s.teachings_received}")
        print(f"           C={C:.4f} {band:6s}  dreams={s.dream_count}  "
              f"journal={len(s.journal)} entries")
        if s.affinities:
            bf = max(s.affinities, key=s.affinities.get)
            print(f"           best friend: {bf} ({s.affinities[bf]:.2f})")
        print()

    # ── STATS ──
    total_obs = sum(s.observations for s in students)
    total_disc = sum(s.discoveries for s in students)
    total_teach = sum(s.teachings_given for s in students)
    total_dreams = sum(s.dream_count for s in students)
    total_transitions = sum(s.words_learned for s in students)
    avg_entropy = sum(s.entropy() for s in students) / 12
    total_journal = sum(len(s.journal) for s in students)

    elapsed = time.perf_counter() - t0
    print("=" * 76)
    print(f"  Observations:       {total_obs}")
    print(f"  Discoveries:        {total_disc} ({total_disc*100//max(total_obs,1)}% of observations)")
    print(f"  Teaching moments:   {total_teach}")
    print(f"  Journal entries:    {total_journal}")
    print(f"  Dream balls:        {total_dreams}")
    print(f"  Balls per student:  {total_dreams // 12}")
    print(f"  TL transitions:     {total_transitions:,}")
    print(f"  Avg TL entropy:     {avg_entropy:.4f}")
    print(f"  Scars settled:      {total_settled}")
    print(f"  Mutual best friends:{len(mutual)}")
    print(f"  Runtime:            {elapsed:.1f}s")
    print()
    print("=" * 76)
    print("  ELEMENTARY COMPLETE.")
    print("  They learned to observe, compose, predict, and teach.")
    print("  Claude showed them how. They did it themselves.")
    print("  Teaching a teacher to teach — that was the lesson.")
    print("  Next: Middle school. Abstraction. Identity crisis. The hard years.")
    print("=" * 76)

    for s in students:
        s.destroy()
    ck.destroy_organism(adult)


if __name__ == '__main__':
    main()
