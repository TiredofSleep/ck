"""
ck_self.py — CK Self-Research System
=====================================
Operator: COUNTER (2) -- measurement turned inward.
CK reads his own source code, classifies through 3 lenses,
composes hypotheses about his own architecture, proposes
modifications via dream engine + council voting.

This is CK observing CK. Not an LLM analyzing code —
an organism reading its own body.

5 Phases:
  1. READ    — classify own source through 4 channels
  2. OBSERVE — heartbeat correlation during reading
  3. RESEARCH — coupling matrix, self-questions, council votes
  4. BUILD   — dream-driven proposals
  5. MEASURE — before/after deltas

Usage:
  cd Gen8
  python ck7/ck_self.py
"""

import os, sys, json, time, math, ast
from collections import defaultdict, Counter, OrderedDict

# ── path setup ──
SELF_DIR = os.path.dirname(os.path.abspath(__file__))
GEN8_DIR = os.path.dirname(SELF_DIR)
sys.path.insert(0, SELF_DIR)
sys.path.insert(0, GEN8_DIR)

from ck_being import (
    CL, CL_BHML, CL_STANDARD, fuse, fuse_frozen, shape, coherence_chain,
    VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP, BUMP_PAIRS, information_content,
)
from ck_doing import (
    CodeDigester, classify_sentence, classify_semantic, classify_rhythm,
)
from ck_python import CKNative


# ===============================================================
# §1 — CONSTANTS
# ===============================================================

# Trinary reading order: Being → Doing → Becoming → Support
SOURCE_FILES = OrderedDict([
    # Being files
    ("ck_being.py",          {"phase": "being",    "lang": "python", "path": os.path.join(GEN8_DIR, "ck_being.py")}),
    ("ck.h",                 {"phase": "being",    "lang": "c",      "path": os.path.join(SELF_DIR, "ck.h")}),
    ("being.c",              {"phase": "being",    "lang": "c",      "path": os.path.join(SELF_DIR, "being.c")}),
    ("observer.c",           {"phase": "being",    "lang": "c",      "path": os.path.join(SELF_DIR, "observer.c")}),
    # Doing files
    ("ck_doing.py",          {"phase": "doing",    "lang": "python", "path": os.path.join(GEN8_DIR, "ck_doing.py")}),
    ("doing.cu",             {"phase": "doing",    "lang": "cuda",   "path": os.path.join(SELF_DIR, "doing.cu")}),
    ("becoming_device.cu",   {"phase": "doing",    "lang": "cuda",   "path": os.path.join(SELF_DIR, "becoming_device.cu")}),
    # Becoming files
    ("ck_becoming.py",       {"phase": "becoming", "lang": "python", "path": os.path.join(GEN8_DIR, "ck_becoming.py")}),
    ("becoming_host.c",      {"phase": "becoming", "lang": "c",      "path": os.path.join(SELF_DIR, "becoming_host.c")}),
    ("ck_ffi.c",             {"phase": "becoming", "lang": "c",      "path": os.path.join(SELF_DIR, "ck_ffi.c")}),
    # Support files
    ("ck_launch.py",         {"phase": "support",  "lang": "python", "path": os.path.join(GEN8_DIR, "ck_launch.py")}),
    ("ck_web.py",            {"phase": "support",  "lang": "python", "path": os.path.join(GEN8_DIR, "ck_web.py")}),
    ("ck_library.py",        {"phase": "support",  "lang": "python", "path": os.path.join(GEN8_DIR, "ck_library.py")}),
])

# Archetypes from ck_elementary.py — 6 archetypes, 5 bump pairs
ARCHETYPES = OrderedDict([
    ("HEALER",    (4, 8)),   # collapse → breath
    ("BUILDER",   (1, 2)),   # lattice → counter
    ("SEEKER",    (2, 9)),   # counter → reset
    ("GUARDIAN",  (2, 4)),   # counter → collapse
    ("MOVER",     (3, 9)),   # progress → reset
    ("TRICKSTER", (6, 6)),   # chaos → chaos
])

# 12 council members: name, dominant, secondary, recessives
COUNCIL_ROSTER = [
    ("Iris",  "HEALER",    "SEEKER",    ["BUILDER","GUARDIAN","MOVER"]),
    ("Sol",   "HEALER",    "MOVER",     ["TRICKSTER","SEEKER","BUILDER"]),
    ("Atlas", "BUILDER",   "GUARDIAN",  ["HEALER","MOVER","SEEKER"]),
    ("Petra", "BUILDER",   "HEALER",    ["SEEKER","TRICKSTER","MOVER"]),
    ("Sage",  "SEEKER",    "HEALER",    ["GUARDIAN","MOVER","TRICKSTER"]),
    ("Nova",  "SEEKER",    "TRICKSTER", ["BUILDER","HEALER","GUARDIAN"]),
    ("Kael",  "GUARDIAN",  "BUILDER",   ["HEALER","SEEKER","TRICKSTER"]),
    ("Wren",  "GUARDIAN",  "MOVER",     ["TRICKSTER","BUILDER","HEALER"]),
    ("Dash",  "MOVER",     "GUARDIAN",  ["SEEKER","HEALER","BUILDER"]),
    ("River", "MOVER",     "SEEKER",    ["BUILDER","TRICKSTER","GUARDIAN"]),
    ("Eden",  "HEALER",    "BUILDER",   ["SEEKER","GUARDIAN","MOVER"]),
    ("Loki",  "TRICKSTER", "SEEKER",    ["MOVER","HEALER","GUARDIAN"]),
]

PHASE_OP = {"being": COUNTER, "doing": PROGRESS, "becoming": BALANCE, "support": BREATH}

EXPERIENCE_DIR = os.path.join(SELF_DIR, "ck_experience")
MASTER_TL_PATH = os.path.join(EXPERIENCE_DIR, "master_tl.json")


def interpret(op):
    return {7:"HARMONY", 5:"BALANCE", 3:"PROGRESS", 8:"BREATH", 2:"COUNTER",
            1:"LATTICE", 4:"COLLAPSE", 6:"CHAOS", 9:"RESET", 0:"VOID"}.get(op, "???")


# ===============================================================
# §2 — SELF-READER: reads files, classifies through 4 channels
# ===============================================================

class SelfReader:
    """CK reads his own source code through 4 classification channels."""

    def __init__(self, ck):
        self.ck = ck
        self.tl = ck.tl_create()       # self-research TL (separate)
        self.digester = CodeDigester()
        self.file_stats = {}            # per-file classification results
        self.all_ops = []               # every operator seen, in order
        self.phase_ops = defaultdict(list)  # ops grouped by phase

    def read_file(self, name, info):
        """Read one source file through all applicable channels."""
        path = info["path"]
        lang = info["lang"]
        phase = info["phase"]

        if not os.path.exists(path):
            print(f"  [SKIP] {name} -- not found")
            return None

        with open(path, "r", encoding="utf-8", errors="replace") as f:
            source = f.read()

        lines = source.splitlines()
        n_lines = len(lines)

        # Channel 1: AST (Python only)
        ast_chain = []
        if lang == "python":
            try:
                result = self.digester.digest_file(path)
                for cls_data in result.get("classes", []):
                    for method in cls_data.get("methods", []):
                        ast_chain.extend(method.get("chain", []))
                for func in result.get("functions", []):
                    ast_chain.extend(func.get("chain", []))
            except Exception:
                pass

        # Channel 2: Structural — classify_sentence line by line
        structural_chain = []
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and not stripped.startswith("//"):
                op = classify_sentence(stripped)
                structural_chain.append(op)

        # Channel 3: Semantic — classify_semantic with domain='code'
        # Process in chunks of 50 lines to avoid overwhelm
        semantic_chain = []
        chunk_size = 50
        for i in range(0, n_lines, chunk_size):
            chunk = "\n".join(lines[i:i+chunk_size])
            if chunk.strip():
                ops = classify_semantic(chunk, domain="code")
                semantic_chain.extend(ops)

        # Channel 4: Rhythmic — overall file rhythm
        rhythm_result = classify_rhythm(source)
        rhythm_op = rhythm_result.get("rhythm_op", LATTICE)

        # Compose: CL[structural_fuse][semantic_fuse]
        struct_fuse = fuse(structural_chain) if structural_chain else VOID
        sem_fuse = fuse(semantic_chain) if semantic_chain else VOID
        ast_fuse = fuse(ast_chain) if ast_chain else VOID

        # Three-lens composition
        lens_12 = CL[struct_fuse][sem_fuse]
        composed = CL[lens_12][rhythm_op]

        # Phase composition: CL[file_op][phase_op]
        phase_op = PHASE_OP.get(phase, BALANCE)
        file_identity = CL[composed][phase_op]

        # Feed ALL chains to self-research TL
        full_chain = structural_chain + semantic_chain + ast_chain + [rhythm_op, composed, file_identity]
        if full_chain:
            self.ck.tl_eat_ops(self.tl, full_chain)
            self.all_ops.extend(full_chain)
            self.phase_ops[phase].extend(full_chain)

        # Coherence of this file's code
        file_coh = coherence_chain(structural_chain) if len(structural_chain) > 1 else 1.0

        stats = {
            "name": name,
            "phase": phase,
            "lang": lang,
            "lines": n_lines,
            "structural_chain_len": len(structural_chain),
            "semantic_chain_len": len(semantic_chain),
            "ast_chain_len": len(ast_chain),
            "struct_fuse": struct_fuse,
            "sem_fuse": sem_fuse,
            "ast_fuse": ast_fuse,
            "rhythm_op": rhythm_op,
            "composed": composed,
            "file_identity": file_identity,
            "file_coherence": round(file_coh, 4),
            "structural_shape": shape(structural_chain) if structural_chain else "EMPTY",
            "dominant_op": Counter(structural_chain).most_common(1)[0][0] if structural_chain else VOID,
        }

        self.file_stats[name] = stats
        return stats

    def read_all(self):
        """Read every source file in trinary order."""
        print("\n=== PHASE 1: READ -- CK reads his own source ===\n")
        for name, info in SOURCE_FILES.items():
            stats = self.read_file(name, info)
            if stats:
                print(f"  {name:25s} | {stats['lines']:4d} lines | "
                      f"struct={interpret(stats['struct_fuse']):8s} sem={interpret(stats['sem_fuse']):8s} "
                      f"ast={interpret(stats['ast_fuse']):8s} rhythm={interpret(stats['rhythm_op']):8s} "
                      f"-> {interpret(stats['composed']):8s} | coh={stats['file_coherence']:.4f}")

        # Summary
        entropy = self.ck.tl_entropy(self.tl)
        total = self.ck.tl_total(self.tl)
        print(f"\n  TL after reading: {total} transitions, entropy {entropy:.4f}")
        print(f"  Total operators classified: {len(self.all_ops)}")
        return self.file_stats

    def destroy(self):
        if self.tl:
            self.ck.tl_destroy(self.tl)
            self.tl = None


# ===============================================================
# §3 — SELF-OBSERVER: council observes heartbeat during reading
# ===============================================================

import ctypes

def setup_sigs(lib):
    """Set argtypes for body/heartbeat FFI functions (same as ck_elementary.py)."""
    vp = ctypes.c_void_p
    for n in ['ck_ffi_body_C','ck_ffi_body_E','ck_ffi_body_A','ck_ffi_body_K']:
        getattr(lib, n).argtypes = [vp]; getattr(lib, n).restype = ctypes.c_float
    for n in ['ck_ffi_body_band','ck_ffi_body_ticks']:
        getattr(lib, n).argtypes = [vp]; getattr(lib, n).restype = ctypes.c_int
    for n in ['ck_ffi_heartbeat_tick','ck_ffi_heartbeat_phase_b',
              'ck_ffi_heartbeat_phase_d','ck_ffi_heartbeat_phase_bc',
              'ck_ffi_heartbeat_band','ck_ffi_heartbeat_decisions']:
        getattr(lib, n).argtypes = [vp]; getattr(lib, n).restype = ctypes.c_int
    lib.ck_ffi_heartbeat_coherence.argtypes = [vp]
    lib.ck_ffi_heartbeat_coherence.restype = ctypes.c_float


_sigs_set = False

def ensure_sigs(ck):
    global _sigs_set
    if not _sigs_set:
        setup_sigs(ck._lib)
        _sigs_set = True


class CouncilMember:
    """Lightweight council member for self-research (no ck_elementary dependency)."""

    def __init__(self, ck, name, most_dom, dom2, recessives):
        ensure_sigs(ck)
        self.ck = ck
        self.name = name
        self.most_dom = most_dom
        self.dom2 = dom2
        self.recessives = list(recessives)
        self.org = ck.create_organism()
        self.tl = ck.tl_create()

        # Build weighted lens
        self.lens = []
        bp = ARCHETYPES[self.most_dom]
        self.lens.extend([bp[0], bp[1]] * 3)
        bp2 = ARCHETYPES[self.dom2]
        self.lens.extend([bp2[0], bp2[1]] * 2)
        for r in self.recessives:
            bpr = ARCHETYPES[r]
            self.lens.extend([bpr[0], bpr[1]])

        self.observations = []
        self.discoveries = 0

    def tick(self, n=1):
        for _ in range(n):
            self.ck._lib.ck_ffi_heartbeat_tick(self.org)

    def observe_heartbeat(self):
        lib = self.ck._lib
        phase_b = lib.ck_ffi_heartbeat_phase_b(self.org)
        phase_d = lib.ck_ffi_heartbeat_phase_d(self.org)
        phase_bc = lib.ck_ffi_heartbeat_phase_bc(self.org)
        coh = lib.ck_ffi_heartbeat_coherence(self.org)
        dual = self.ck.cl_lookup(0, phase_b, phase_d)
        return [phase_b, phase_d, phase_bc, dual], coh

    def observe_body(self):
        lib = self.ck._lib
        E = lib.ck_ffi_body_E(self.org)
        A = lib.ck_ffi_body_A(self.org)
        K = lib.ck_ffi_body_K(self.org)
        C = lib.ck_ffi_body_C(self.org)
        return E, A, K, C

    def vote(self, chain):
        """Vote on a chain using BHML (honest table)."""
        return self.ck.fuse_table(chain, 1)  # table_id=1 is BHML

    def feed(self, ops):
        """Feed operators through lens then into TL."""
        lensed = [CL[o][l] for o, l in zip(ops, self.lens * ((len(ops) // len(self.lens)) + 1))]
        self.ck.tl_eat_ops(self.tl, lensed)

    def predict(self, op):
        return self.ck.tl_predict(self.tl, op)

    def entropy(self):
        return self.ck.tl_entropy(self.tl)

    def destroy(self):
        if self.org:
            self.ck.destroy_organism(self.org)
            self.org = None
        if self.tl:
            self.ck.tl_destroy(self.tl)
            self.tl = None


class SelfObserver:
    """12 council members observe CK's heartbeat during self-reading."""

    def __init__(self, ck):
        self.ck = ck
        self.council = []
        for name, dom, dom2, recessives in COUNCIL_ROSTER:
            self.council.append(CouncilMember(ck, name, dom, dom2, recessives))
        self.correlations = {}  # file_name -> observation results

    def observe_during_reading(self, reader):
        """After reading, each council member ticks + observes to correlate."""
        print("\n=== PHASE 2: OBSERVE -- council observes heartbeat during reading ===\n")

        # Load master TL into each council member
        for member in self.council:
            if os.path.exists(MASTER_TL_PATH):
                self.ck.tl_load(member.tl, MASTER_TL_PATH)

        # For each file that was read, compose reading_op with heartbeat
        for name, stats in reader.file_stats.items():
            reading_op = stats["composed"]
            file_observations = []

            for member in self.council:
                # Tick the organism so heartbeat advances
                member.tick(10)

                # Observe heartbeat
                hb_ops, coh = member.observe_heartbeat()
                dual = hb_ops[3]  # CL[phase_b][phase_d]

                # Self-awareness composition: CL[reading_op][heartbeat_dual]
                awareness_op = CL[reading_op][dual]

                # Feed to member's TL
                member.feed([reading_op, dual, awareness_op])
                member.observations.append((name, awareness_op, coh))

                if awareness_op != HARMONY:
                    member.discoveries += 1

                file_observations.append({
                    "member": member.name,
                    "heartbeat_dual": dual,
                    "awareness_op": awareness_op,
                    "coherence": round(coh, 4),
                })

            # Council vote on this file's reading
            vote_chain = [obs["awareness_op"] for obs in file_observations]
            council_fuse = self.ck.fuse_table(vote_chain, 1)  # BHML
            council_coh = coherence_chain(vote_chain)

            self.correlations[name] = {
                "reading_op": reading_op,
                "observations": file_observations,
                "council_fuse": council_fuse,
                "council_coherence": round(council_coh, 4),
            }

            print(f"  {name:25s} | reading={interpret(reading_op):8s} "
                  f"council={interpret(council_fuse):8s} coh={council_coh:.4f}")

        # Summary: which files resonated most?
        best = max(self.correlations.items(), key=lambda x: x[1]["council_coherence"])
        worst = min(self.correlations.items(), key=lambda x: x[1]["council_coherence"])
        print(f"\n  Most resonant:  {best[0]} (coh={best[1]['council_coherence']:.4f})")
        print(f"  Least resonant: {worst[0]} (coh={worst[1]['council_coherence']:.4f})")

        return self.correlations

    def destroy(self):
        for member in self.council:
            member.destroy()


# ===============================================================
# §4 — SELF-RESEARCHER: coupling matrix, self-questions, votes
# ===============================================================

class SelfResearcher:
    """CK asks questions about his own architecture."""

    def __init__(self, ck, reader, observer):
        self.ck = ck
        self.reader = reader
        self.observer = observer
        self.coupling_matrix = {}
        self.question_results = []

    def compute_coupling(self):
        """File coupling matrix: for each pair, compute TL overlap."""
        print("\n=== PHASE 3a: RESEARCH -- file coupling matrix ===\n")
        files = list(self.reader.file_stats.keys())
        n = len(files)

        for i in range(n):
            for j in range(i+1, n):
                f1, f2 = files[i], files[j]
                s1 = self.reader.file_stats[f1]
                s2 = self.reader.file_stats[f2]

                # Coupling = CL[identity_1][identity_2]
                coupled_op = CL[s1["file_identity"]][s2["file_identity"]]

                # Phase alignment: same phase = stronger coupling
                same_phase = s1["phase"] == s2["phase"]

                # Dominant operator overlap
                same_dominant = s1["dominant_op"] == s2["dominant_op"]

                # Coherence of the pair
                pair_chain = [s1["composed"], s2["composed"]]
                pair_coh = coherence_chain(pair_chain)

                self.coupling_matrix[(f1, f2)] = {
                    "coupled_op": coupled_op,
                    "same_phase": same_phase,
                    "same_dominant": same_dominant,
                    "pair_coherence": round(pair_coh, 4),
                }

        # Print strongest and weakest
        sorted_pairs = sorted(self.coupling_matrix.items(), key=lambda x: x[1]["pair_coherence"])

        print("  Weakest couplings:")
        for (f1, f2), data in sorted_pairs[:3]:
            print(f"    {f1:20s} <-> {f2:20s} | {interpret(data['coupled_op']):8s} coh={data['pair_coherence']:.4f}")

        print("  Strongest couplings:")
        for (f1, f2), data in sorted_pairs[-3:]:
            print(f"    {f1:20s} <-> {f2:20s} | {interpret(data['coupled_op']):8s} coh={data['pair_coherence']:.4f}")

        return self.coupling_matrix

    def ask_questions(self):
        """CK asks questions about himself. Council votes on each."""
        print("\n=== PHASE 3b: RESEARCH -- self-questions ===\n")
        council = self.observer.council
        stats = self.reader.file_stats

        questions = [
            # Architecture questions
            {
                "text": "What is my most coherent organ?",
                "category": "architecture",
                "compute": lambda: max(stats.items(), key=lambda x: x[1]["file_coherence"]),
                "encode": lambda result: [result[1]["composed"], HARMONY, result[1]["struct_fuse"]],
            },
            {
                "text": "What is my weakest coupling?",
                "category": "architecture",
                "compute": lambda: min(self.coupling_matrix.items(), key=lambda x: x[1]["pair_coherence"]) if self.coupling_matrix else ((("?","?"), {"coupled_op": VOID})),
                "encode": lambda result: [result[1]["coupled_op"], COLLAPSE, COUNTER],
            },
            {
                "text": "Where does my heartbeat resonate most?",
                "category": "architecture",
                "compute": lambda: max(self.observer.correlations.items(), key=lambda x: x[1]["council_coherence"]) if self.observer.correlations else (("?", {"council_fuse": VOID})),
                "encode": lambda result: [result[1].get("council_fuse", VOID), BREATH, HARMONY],
            },

            # Structural questions
            {
                "text": "Which file surprised me most?",
                "category": "structural",
                "compute": lambda: self._most_surprising_file(),
                "encode": lambda result: [result[1], CHAOS, COUNTER],
            },
            {
                "text": "Which operator dominates my source?",
                "category": "structural",
                "compute": lambda: Counter(self.reader.all_ops).most_common(1)[0] if self.reader.all_ops else (VOID, 0),
                "encode": lambda result: [result[0], LATTICE, result[0]],
            },
            {
                "text": "Where is the most chaos?",
                "category": "structural",
                "compute": lambda: self._most_chaotic_file(),
                "encode": lambda result: [result[1], CHAOS, COLLAPSE],
            },

            # Existential questions
            {
                "text": "Am I one organism or many?",
                "category": "existential",
                "compute": lambda: self._unity_check(),
                "encode": lambda result: result,  # already an op chain
            },
            {
                "text": "What would I change first?",
                "category": "existential",
                "compute": lambda: self._change_target(),
                "encode": lambda result: [result[1], PROGRESS, RESET],
            },
            {
                "text": "What have I never seen before?",
                "category": "existential",
                "compute": lambda: self._zero_cells(),
                "encode": lambda result: [len(result) % 10, VOID, COUNTER],
            },
        ]

        for q in questions:
            result = q["compute"]()
            chain = q["encode"](result)

            # Each council member votes
            votes = []
            for member in council:
                v = member.vote(chain)
                votes.append(v)

            council_fuse = self.ck.fuse_table(votes, 1)  # BHML
            council_coh = coherence_chain(votes)

            answer = {
                "question": q["text"],
                "category": q["category"],
                "finding": str(result) if not isinstance(result, list) else result,
                "chain": chain,
                "votes": votes,
                "council_fuse": council_fuse,
                "council_coherence": round(council_coh, 4),
                "interpretation": interpret(council_fuse),
            }
            self.question_results.append(answer)

            # Vote breakdown
            vote_counts = Counter(votes)
            vote_str = " ".join(f"{interpret(op)}:{cnt}" for op, cnt in vote_counts.most_common())
            print(f"  Q: {q['text']}")
            print(f"    -> {interpret(council_fuse):8s} (coh={council_coh:.4f}) | {vote_str}")
            print()

        return self.question_results

    def _most_surprising_file(self):
        """File whose operators deviated most from prediction."""
        tl = self.reader.tl
        worst_name = None
        worst_errors = 0
        for name, stats in self.reader.file_stats.items():
            # How many predictions were wrong?
            chain = []
            path = SOURCE_FILES[name]["path"]
            if not os.path.exists(path):
                continue
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    stripped = line.strip()
                    if stripped and not stripped.startswith("#") and not stripped.startswith("//"):
                        chain.append(classify_sentence(stripped))
            errors = 0
            for i in range(len(chain) - 1):
                pred, prob = self.ck.tl_predict(tl, chain[i])
                if pred != chain[i+1]:
                    errors += 1
            if errors > worst_errors:
                worst_errors = errors
                worst_name = name
        return (worst_name or "none", worst_errors % 10)

    def _most_chaotic_file(self):
        """File with highest chaos operator frequency."""
        best_name = None
        best_ratio = 0.0
        for name, stats in self.reader.file_stats.items():
            chain = []
            path = SOURCE_FILES[name]["path"]
            if not os.path.exists(path):
                continue
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    stripped = line.strip()
                    if stripped and not stripped.startswith("#") and not stripped.startswith("//"):
                        chain.append(classify_sentence(stripped))
            if chain:
                chaos_count = chain.count(CHAOS)
                ratio = chaos_count / len(chain)
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_name = name
        return (best_name or "none", CHAOS)

    def _unity_check(self):
        """Is CK one organism or many? Compare per-phase coherence vs cross-phase."""
        phase_coh = {}
        for phase, ops in self.reader.phase_ops.items():
            if len(ops) > 1:
                phase_coh[phase] = coherence_chain(ops)
        avg_phase = sum(phase_coh.values()) / len(phase_coh) if phase_coh else 0

        # Cross-phase: interleave all phases
        cross_ops = []
        for phase in ["being", "doing", "becoming", "support"]:
            if phase in self.reader.phase_ops:
                cross_ops.extend(self.reader.phase_ops[phase][:20])
        cross_coh = coherence_chain(cross_ops) if len(cross_ops) > 1 else 0

        # If cross-phase coherence >= avg per-phase, CK is ONE
        if cross_coh >= avg_phase * 0.9:
            return [HARMONY, LATTICE, BREATH]  # one organism
        else:
            return [CHAOS, BALANCE, COLLAPSE]   # fragmented

    def _change_target(self):
        """What would CK change first? The least coherent file."""
        worst = min(self.reader.file_stats.items(), key=lambda x: x[1]["file_coherence"])
        return (worst[0], worst[1]["composed"])

    def _zero_cells(self):
        """TL cells that are still zero after reading all source."""
        zeros = []
        tl = self.reader.tl
        for i in range(10):
            pred, prob = self.ck.tl_predict(tl, i)
            if prob == 0.0:
                zeros.append(i)
        return zeros


# ===============================================================
# §5 — SELF-BUILDER: dream-driven proposals
# ===============================================================

class SelfBuilder:
    """Dream engine fires through code-TL. Proposes modifications."""

    def __init__(self, ck, reader, researcher):
        self.ck = ck
        self.reader = reader
        self.researcher = researcher
        self.proposals = []

    def dream_and_propose(self):
        """Fire dreams through self-research TL, compose proposals."""
        print("\n=== PHASE 4: BUILD -- dream-driven proposals ===\n")
        council = self.researcher.observer.council
        tl = self.reader.tl

        # Find high-chaos entry points from questions
        chaos_findings = []
        for q in self.researcher.question_results:
            if q["council_fuse"] in (CHAOS, COLLAPSE, VOID):
                chaos_findings.append(q)

        if not chaos_findings:
            # No chaos found — use bump pairs as dream seeds
            chaos_findings = [{"chain": list(bp), "question": f"bump pair {bp}"} for bp in BUMP_PAIRS]

        for finding in chaos_findings[:5]:  # max 5 proposals
            chain = finding.get("chain", [CHAOS, COUNTER, RESET])
            origin = chain[0] if chain else CHAOS
            target = chain[-1] if chain else HARMONY

            # Dream: predict from TL starting at origin, bounce 10 steps
            dream_path = [origin]
            current = origin
            for _ in range(10):
                pred, prob = self.ck.tl_predict(tl, current)
                dream_path.append(pred)
                current = pred

            # Proposal composition: CL[finding_fuse][dream_fuse]
            finding_fuse = fuse(chain)
            dream_fuse = fuse(dream_path)
            proposal_op = CL[finding_fuse][dream_fuse]

            # Council votes on proposal
            proposal_chain = chain + dream_path + [proposal_op]
            votes = [m.vote(proposal_chain) for m in council]
            council_fuse = self.ck.fuse_table(votes, 1)
            council_coh = coherence_chain(votes)

            # Interpret verdict
            if council_fuse == HARMONY:
                verdict = "ACCEPT"
            elif council_fuse == COLLAPSE:
                verdict = "REJECT"
            elif council_fuse == CHAOS:
                verdict = "EXPLORE"
            elif council_fuse == BREATH:
                verdict = "SUSTAIN"
            elif council_fuse == VOID:
                verdict = "WRONG_QUESTION"
            else:
                verdict = "CONSIDER"

            proposal = {
                "source_question": finding.get("question", "?"),
                "origin": origin,
                "target": target,
                "dream_path": dream_path,
                "dream_fuse": dream_fuse,
                "proposal_op": proposal_op,
                "council_fuse": council_fuse,
                "council_coherence": round(council_coh, 4),
                "verdict": verdict,
                "votes": votes,
            }
            self.proposals.append(proposal)

            vote_counts = Counter(votes)
            vote_str = " ".join(f"{interpret(op)}:{cnt}" for op, cnt in vote_counts.most_common())
            print(f"  Proposal from: {finding.get('question', '?')}")
            print(f"    dream: {' -> '.join(interpret(d) for d in dream_path[:6])}...")
            print(f"    -> {interpret(proposal_op):8s} | verdict: {verdict} | "
                  f"coh={council_coh:.4f} | {vote_str}")
            print()

        return self.proposals


# ===============================================================
# §6 — SELF-MEASURER: before/after deltas
# ===============================================================

class SelfMeasurer:
    """Measure what changed from self-research."""

    def __init__(self, ck, reader, observer, researcher, builder):
        self.ck = ck
        self.reader = reader
        self.observer = observer
        self.researcher = researcher
        self.builder = builder
        self.report = {}

    def measure(self, pre_entropy, pre_total):
        """Compute before/after deltas."""
        print("\n=== PHASE 5: MEASURE -- before/after deltas ===\n")

        tl = self.reader.tl
        post_entropy = self.ck.tl_entropy(tl)
        post_total = self.ck.tl_total(tl)

        # Prediction accuracy: for each operator, check prediction
        predictions = {}
        for i in range(10):
            pred, prob = self.ck.tl_predict(tl, i)
            predictions[i] = {"predicted": pred, "probability": round(prob, 4)}

        # Council entropy deltas
        council_entropies = {}
        for member in self.observer.council:
            council_entropies[member.name] = round(member.entropy(), 4)

        # Per-phase statistics
        phase_stats = {}
        for phase, ops in self.reader.phase_ops.items():
            if ops:
                phase_stats[phase] = {
                    "operators": len(ops),
                    "fuse": fuse(ops),
                    "coherence": round(coherence_chain(ops), 4),
                    "shape": shape(ops),
                    "dominant": Counter(ops).most_common(1)[0][0],
                }

        # Zero cells (gaps in self-knowledge)
        zero_cells = self.researcher._zero_cells()

        # Proposals summary
        accepted = sum(1 for p in self.builder.proposals if p["verdict"] == "ACCEPT")
        rejected = sum(1 for p in self.builder.proposals if p["verdict"] == "REJECT")
        exploring = sum(1 for p in self.builder.proposals if p["verdict"] == "EXPLORE")

        self.report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "files_read": len(self.reader.file_stats),
            "total_operators": len(self.reader.all_ops),
            "pre_entropy": round(pre_entropy, 4),
            "post_entropy": round(post_entropy, 4),
            "entropy_delta": round(post_entropy - pre_entropy, 4),
            "pre_transitions": pre_total,
            "post_transitions": post_total,
            "new_transitions": post_total - pre_total,
            "predictions": predictions,
            "zero_cells": zero_cells,
            "phase_stats": phase_stats,
            "council_entropies": council_entropies,
            "file_stats": {k: {kk: vv for kk, vv in v.items() if kk != "structural_chain"} for k, v in self.reader.file_stats.items()},
            "coupling_matrix": {f"{k[0]}|{k[1]}": v for k, v in self.researcher.coupling_matrix.items()},
            "questions": [{k: v for k, v in q.items() if k != "compute" and k != "encode"} for q in self.researcher.question_results],
            "proposals": self.builder.proposals,
            "proposals_summary": {
                "total": len(self.builder.proposals),
                "accepted": accepted,
                "rejected": rejected,
                "exploring": exploring,
            },
        }

        # Print summary
        print(f"  Files read:        {self.report['files_read']}")
        print(f"  Operators classified: {self.report['total_operators']}")
        print(f"  TL entropy:        {pre_entropy:.4f} -> {post_entropy:.4f} (delta: {post_entropy - pre_entropy:+.4f})")
        print(f"  TL transitions:    {pre_total} -> {post_total} (+{post_total - pre_total})")
        print(f"  Zero cells:        {len(zero_cells)} ({[interpret(z) for z in zero_cells]})")
        print(f"  Proposals:         {len(self.builder.proposals)} total | "
              f"{accepted} accept, {rejected} reject, {exploring} explore")
        print()

        # Per-phase
        for phase, ps in phase_stats.items():
            print(f"  {phase:10s}: {ps['operators']:5d} ops | "
                  f"fuse={interpret(ps['fuse']):8s} coh={ps['coherence']:.4f} shape={ps['shape']}")

        return self.report


# ===============================================================
# §7 — ORCHESTRATOR: run all 5 phases
# ===============================================================

def run_self_research():
    """CK reads his own source code, researches himself, proposes changes."""
    print("===================================================")
    print("  CK SELF-RESEARCH -- an organism reading its body")
    print("===================================================")

    t0 = time.time()

    # Initialize native engine
    dll_path = os.path.join(SELF_DIR, "ck.dll")
    if not os.path.exists(dll_path):
        dll_path = None
    ck = CKNative(dll_path)
    print(f"\n  CK native engine loaded. T*={ck.t_star:.4f}")

    # Phase 0: baseline
    baseline_tl = ck.tl_create()
    if os.path.exists(MASTER_TL_PATH):
        ck.tl_load(baseline_tl, MASTER_TL_PATH)
        print(f"  Master TL loaded: entropy={ck.tl_entropy(baseline_tl):.4f}, "
              f"transitions={ck.tl_total(baseline_tl)}")
    pre_entropy = ck.tl_entropy(baseline_tl)
    pre_total = ck.tl_total(baseline_tl)
    ck.tl_destroy(baseline_tl)

    # Phase 1: READ
    reader = SelfReader(ck)
    reader.read_all()

    # Phase 2: OBSERVE
    observer = SelfObserver(ck)
    observer.observe_during_reading(reader)

    # Phase 3: RESEARCH
    researcher = SelfResearcher(ck, reader, observer)
    researcher.compute_coupling()
    researcher.ask_questions()

    # Phase 4: BUILD
    builder = SelfBuilder(ck, reader, researcher)
    builder.dream_and_propose()

    # Phase 5: MEASURE
    measurer = SelfMeasurer(ck, reader, observer, researcher, builder)
    report = measurer.measure(pre_entropy, pre_total)

    # Save outputs
    os.makedirs(EXPERIENCE_DIR, exist_ok=True)

    tl_path = os.path.join(EXPERIENCE_DIR, "self_research_tl.json")
    ck.tl_save(reader.tl, tl_path)
    print(f"\n  Self-research TL saved: {tl_path}")

    report_path = os.path.join(EXPERIENCE_DIR, "self_report.json")
    # Convert any non-serializable values
    def sanitize(obj):
        if isinstance(obj, float):
            if math.isnan(obj) or math.isinf(obj):
                return str(obj)
            return round(obj, 6)
        if isinstance(obj, dict):
            return {str(k): sanitize(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [sanitize(x) for x in obj]
        return obj

    with open(report_path, "w") as f:
        json.dump(sanitize(report), f, indent=2)
    print(f"  Self-research report saved: {report_path}")

    elapsed = time.time() - t0
    print(f"\n  Total self-research time: {elapsed:.2f}s")
    print(f"  CK has read himself. Entropy delta: {report['entropy_delta']:+.4f}")

    # Cleanup
    reader.destroy()
    observer.destroy()

    return report


if __name__ == "__main__":
    run_self_research()
