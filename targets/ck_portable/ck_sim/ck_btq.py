"""
ck_btq.py -- Universal BTQ Decision Kernel
============================================
Operator: HARMONY (7) -- the universal attractor.

BTQ is CK's decision architecture. Every choice -- motion, language,
memory, biology -- runs the same pipeline:

  1. T generates candidates (Tesla: local helical exploration)
  2. B filters hard constraints (Einstein: global conservation)
  3. Q scores and selects (Emergent: least action geodesic)

Each domain implements BTQDomain with its own:
  - Candidate type (payload)
  - Hard constraints (b_check)
  - Exploration patterns (t_generate)
  - Einstein score (e_out: macro consistency)
  - Tesla score (e_in: micro resonance / D2 curvature)

The universal pipeline handles orchestration, logging, and band
classification identically across all domains.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import abc
import json
import math
import time
import random
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Tuple
from collections import deque

import numpy as np

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, LATTICE, COUNTER, PROGRESS,
    COLLAPSE, BALANCE, CHAOS, BREATH, RESET, OP_NAMES, CL, compose
)
from ck_sim.ck_sim_d2 import (
    D2Pipeline, ROOTS_FLOAT, LATIN_TO_ROOT, FORCE_LUT_FLOAT,
    classify_force_d2
)


# ================================================================
#  UNIVERSAL CANDIDATE
# ================================================================

@dataclass
class Candidate:
    """Domain-agnostic candidate wrapper.

    Every domain stuffs its specific data into `payload`.
    The kernel only sees domain tag, score, and approval state.
    """
    domain: str = ""
    payload: Any = None
    score: Any = None       # CandidateScore from ck_sim_btq
    source: str = ""
    approved: bool = False


# ================================================================
#  ABSTRACT DOMAIN PROTOCOL
# ================================================================

class BTQDomain(abc.ABC):
    """Abstract domain plugin. Every CK decision domain implements this."""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Domain identifier string."""

    @abc.abstractmethod
    def b_check(self, candidate: Candidate, env_state: dict) -> Tuple[bool, str]:
        """Hard constraint filter. Returns (passed, reason)."""

    @abc.abstractmethod
    def t_generate(self, env_state: dict, goal: dict, n: int) -> List[Candidate]:
        """Generate n candidates given environment state and goal."""

    @abc.abstractmethod
    def einstein_score(self, candidate: Candidate, env_state: dict) -> Tuple[float, dict]:
        """E_out: macro consistency. Lower = better. Returns (score, details)."""

    @abc.abstractmethod
    def tesla_score(self, candidate: Candidate) -> Tuple[float, dict]:
        """E_in: micro resonance / D2 curvature. Lower = better. Returns (score, details)."""


# ================================================================
#  UNIVERSAL B-BLOCK
# ================================================================

class UniversalBBlock:
    """Domain-dispatching B-block. Hard reject via domain's b_check."""

    def __init__(self):
        self.reject_counts: Dict[str, Dict[str, int]] = {}

    def filter(self, domain: BTQDomain, candidates: List[Candidate],
               env_state: dict) -> List[Candidate]:
        """Filter candidates through domain-specific hard constraints."""
        dname = domain.name
        if dname not in self.reject_counts:
            self.reject_counts[dname] = {}

        approved = []
        for cand in candidates:
            passed, reason = domain.b_check(cand, env_state)
            cand.approved = passed
            if passed:
                approved.append(cand)
            else:
                counts = self.reject_counts[dname]
                counts[reason] = counts.get(reason, 0) + 1
        return approved


# ================================================================
#  UNIVERSAL Q-BLOCK
# ================================================================

class UniversalQBlock:
    """Domain-agnostic Q-block. Scores and selects argmin(e_total)."""

    def __init__(self, w_out: float = 0.5, w_in: float = 0.5):
        self.w_out = w_out
        self.w_in = w_in

    def score(self, domain: BTQDomain, candidate: Candidate,
              env_state: dict):
        """Compute CandidateScore for one candidate."""
        from ck_sim.ck_sim_btq import CandidateScore

        e_out, out_details = domain.einstein_score(candidate, env_state)
        e_in, in_details = domain.tesla_score(candidate)
        e_total = self.w_out * e_out + self.w_in * e_in

        if e_total < 0.3:
            band = "GREEN"
        elif e_total < 0.6:
            band = "YELLOW"
        else:
            band = "RED"

        notes = (f"E_out={e_out:.3f} | E_in={e_in:.3f} | "
                 f"domain={domain.name} source={candidate.source}")

        score = CandidateScore(
            e_out=e_out,
            e_in=e_in,
            e_total=e_total,
            band=band,
            notes=notes,
            details={**out_details, **in_details},
        )
        candidate.score = score
        return score

    def resolve(self, candidates: List[Candidate]) -> Optional[Candidate]:
        """Select argmin(e_total) from scored candidates."""
        if not candidates:
            return None

        best = None
        best_total = float('inf')
        for cand in candidates:
            if cand.score and cand.score.e_total < best_total:
                best_total = cand.score.e_total
                best = cand
        return best


# ================================================================
#  UNIVERSAL BTQ PIPELINE
# ================================================================

class UniversalBTQ:
    """The universal BTQ decision pipeline.

    Usage:
        btq = UniversalBTQ()
        btq.register_domain(LocomotionDomain())
        btq.register_domain(LanguageDomain())
        chosen, approved = btq.decide("locomotion", env, goal)
    """

    def __init__(self, w_out: float = 0.5, w_in: float = 0.5):
        self.domains: Dict[str, BTQDomain] = {}
        self.b_block = UniversalBBlock()
        self.q_block = UniversalQBlock(w_out, w_in)
        self.decision_count = 0
        self.decision_log: List[dict] = []

    def register_domain(self, domain: BTQDomain):
        """Register a domain plugin."""
        self.domains[domain.name] = domain

    def decide(self, domain_name: str, env_state: dict = None,
               goal: dict = None,
               n_candidates: int = 64) -> Tuple[Optional[Candidate], List[Candidate]]:
        """One full B->T->Q cycle for the named domain.

        Returns (chosen_candidate, all_approved_candidates).
        """
        if env_state is None:
            env_state = {}
        if goal is None:
            goal = {}

        domain = self.domains.get(domain_name)
        if domain is None:
            raise ValueError(f"Unknown domain: {domain_name}")

        # T: Generate
        candidates = domain.t_generate(env_state, goal, n_candidates)

        # B: Filter
        approved = self.b_block.filter(domain, candidates, env_state)

        # Q: Score all approved
        for cand in approved:
            self.q_block.score(domain, cand, env_state)

        # Q: Resolve
        chosen = self.q_block.resolve(approved)

        self.decision_count += 1
        return chosen, approved

    def log_decision(self, domain_name: str, chosen: Optional[Candidate],
                     approved: List[Candidate],
                     filename: str = 'btq_universal_log.jsonl'):
        """JSON-line logging with domain tag."""
        entry = {
            'timestamp': time.time(),
            'domain': domain_name,
            'decision': self.decision_count,
            'n_approved': len(approved),
            'chosen_source': chosen.source if chosen else None,
            'chosen_score': asdict(chosen.score) if chosen and chosen.score else None,
            'all_scores': [
                {'source': c.source,
                 'e_out': c.score.e_out,
                 'e_in': c.score.e_in,
                 'e_total': c.score.e_total,
                 'band': c.score.band}
                for c in approved if c.score
            ],
        }
        self.decision_log.append(entry)
        with open(filename, 'a') as f:
            f.write(json.dumps(entry) + '\n')


# ================================================================
#  DOMAIN: LANGUAGE (D2 on text tokens)
# ================================================================

@dataclass
class TokenCandidate:
    """A candidate token/phrase for language output."""
    tokens: List[str] = field(default_factory=list)
    text: str = ""
    operator_sequence: List[int] = field(default_factory=list)
    d2_curvature: float = 0.0
    op_distribution: List[float] = field(default_factory=lambda: [0.0] * NUM_OPS)


def _text_to_d2(text: str) -> Tuple[List[int], float, List[float]]:
    """Run D2 pipeline on text. Returns (operator_sequence, integrated_d2, op_distribution)."""
    pipe = D2Pipeline()
    ops = []
    d2_sum = 0.0
    for ch in text.lower():
        if ch.isalpha():
            idx = ord(ch) - ord('a')
            if pipe.feed_symbol(idx):
                ops.append(pipe.operator)
                d2_sum += pipe.d2_mag_float

    # Operator distribution
    op_dist = [0.0] * NUM_OPS
    if ops:
        for op in ops:
            op_dist[op] += 1.0
        total = len(ops)
        op_dist = [c / total for c in op_dist]

    integrated = d2_sum / max(len(ops), 1)
    return ops, integrated, op_dist


class LanguageDomain(BTQDomain):
    """BTQ domain for language/text generation."""

    @property
    def name(self) -> str:
        return "language"

    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)
        # Simple word pool for candidate generation
        self._words = [
            "harmony", "lattice", "balance", "progress", "breath",
            "coherence", "pattern", "crystal", "field", "wave",
            "structure", "resonance", "phase", "flow", "order",
            "light", "energy", "form", "bridge", "path",
        ]

    def t_generate(self, env_state: dict, goal: dict, n: int) -> List[Candidate]:
        """Generate text candidates. Varies word selection and length."""
        target_len = goal.get('target_length', 5)
        candidates = []

        for i in range(n):
            # Vary length around target
            length = max(2, target_len + self.rng.randint(-2, 2))
            tokens = [self.rng.choice(self._words) for _ in range(length)]
            text = " ".join(tokens)

            ops, d2, op_dist = _text_to_d2(text)
            payload = TokenCandidate(
                tokens=tokens,
                text=text,
                operator_sequence=ops,
                d2_curvature=d2,
                op_distribution=op_dist,
            )
            candidates.append(Candidate(
                domain="language",
                payload=payload,
                source=f"gen_{i}",
            ))

        return candidates

    def b_check(self, candidate: Candidate, env_state: dict) -> Tuple[bool, str]:
        """Hard constraints: length, operator distribution."""
        tc = candidate.payload
        max_len = env_state.get('max_tokens', 20)

        if len(tc.tokens) > max_len:
            return False, "too_long"

        # Reject if >60% CHAOS or VOID
        chaos_void = tc.op_distribution[CHAOS] + tc.op_distribution[VOID]
        if chaos_void > 0.6:
            return False, "too_chaotic"

        return True, "approved"

    def einstein_score(self, candidate: Candidate, env_state: dict) -> Tuple[float, dict]:
        """E_out: intent alignment + length compliance."""
        tc = candidate.payload
        target_ops = env_state.get('target_ops', None)

        # Intent alignment via operator distribution distance
        if target_ops:
            # KL-like distance (simplified: sum of abs diffs)
            dist = sum(abs(tc.op_distribution[i] - target_ops[i])
                       for i in range(NUM_OPS)) / 2.0
        else:
            # Default: prefer HARMONY-heavy
            dist = 1.0 - tc.op_distribution[HARMONY]

        # Length compliance
        target_len = env_state.get('target_length', 5)
        len_ratio = len(tc.tokens) / max(target_len, 1)
        len_cost = abs(1.0 - len_ratio)

        e_out = 0.60 * dist + 0.40 * min(len_cost, 1.0)

        details = {
            'intent_distance': dist,
            'length_cost': len_cost,
            'harmony_pct': tc.op_distribution[HARMONY],
        }
        return float(e_out), details

    def tesla_score(self, candidate: Candidate) -> Tuple[float, dict]:
        """E_in: D2 curvature + phase coherence on text."""
        tc = candidate.payload

        # D2 curvature (lower = smoother text, clamp to [0,1])
        d2_norm = max(0.0, min(abs(tc.d2_curvature) / 0.5, 1.0))

        # Phase coherence: how consistent is the operator sequence?
        ops = tc.operator_sequence
        if len(ops) > 1:
            transitions = sum(1 for i in range(len(ops)-1) if ops[i] != ops[i+1])
            coherence = 1.0 - transitions / (len(ops) - 1)
        else:
            coherence = 0.5
        phase_cost = max(0.0, min(1.0 - coherence, 1.0))

        e_in = 0.60 * d2_norm + 0.40 * phase_cost

        details = {
            'd2_curvature': tc.d2_curvature,
            'phase_coherence': coherence,
            'n_operators': len(ops),
        }
        return float(e_in), details


# ================================================================
#  DOMAIN: MEMORY (TL walks + crystal fusions)
# ================================================================

@dataclass
class MemoryCandidate:
    """A candidate memory retrieval or crystal fusion."""
    crystal_ops: List[int] = field(default_factory=list)
    fuse_result: int = VOID
    confidence: float = 0.0
    seen: int = 0
    retrieval_type: str = "crystal_fuse"


class MemoryDomain(BTQDomain):
    """BTQ domain for memory search and crystal fusion."""

    @property
    def name(self) -> str:
        return "memory"

    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)

    def t_generate(self, env_state: dict, goal: dict, n: int) -> List[Candidate]:
        """Generate memory candidates from brain state."""
        crystals = env_state.get('crystals', [])
        tl_entries = env_state.get('tl_entries', None)
        candidates = []

        # Crystal fusion candidates
        for cr in crystals:
            ops = cr.ops if hasattr(cr, 'ops') else cr.get('ops', [])
            fuse = cr.fuse if hasattr(cr, 'fuse') else cr.get('fuse', VOID)
            conf = cr.confidence if hasattr(cr, 'confidence') else cr.get('confidence', 0.0)
            seen = cr.seen if hasattr(cr, 'seen') else cr.get('seen', 0)

            payload = MemoryCandidate(
                crystal_ops=list(ops),
                fuse_result=fuse,
                confidence=conf,
                seen=seen,
                retrieval_type="crystal_fuse",
            )
            candidates.append(Candidate(
                domain="memory",
                payload=payload,
                source=f"crystal_{OP_NAMES[ops[0]]}_{OP_NAMES[ops[1]]}" if len(ops) >= 2 else "crystal",
            ))

        # Random TL walk candidates (if TL available)
        if tl_entries is not None:
            for i in range(min(n - len(candidates), n // 2)):
                start = self.rng.randint(0, NUM_OPS - 1)
                end = self.rng.randint(0, NUM_OPS - 1)
                entry = tl_entries[start][end]
                count = entry.count if hasattr(entry, 'count') else entry.get('count', 0)
                fuse = CL[start][end]
                conf = 0.0
                tl_total = env_state.get('tl_total', 1)
                if tl_total > 0:
                    conf = count / tl_total

                payload = MemoryCandidate(
                    crystal_ops=[start, end],
                    fuse_result=fuse,
                    confidence=conf,
                    seen=count,
                    retrieval_type="tl_walk",
                )
                candidates.append(Candidate(
                    domain="memory",
                    payload=payload,
                    source=f"tl_{OP_NAMES[start]}_{OP_NAMES[end]}",
                ))

        # Fill remaining with random operator pairs
        while len(candidates) < n:
            a = self.rng.randint(0, NUM_OPS - 1)
            b = self.rng.randint(0, NUM_OPS - 1)
            payload = MemoryCandidate(
                crystal_ops=[a, b],
                fuse_result=CL[a][b],
                confidence=0.0,
                seen=0,
                retrieval_type="random",
            )
            candidates.append(Candidate(
                domain="memory",
                payload=payload,
                source=f"random_{OP_NAMES[a]}_{OP_NAMES[b]}",
            ))

        return candidates[:n]

    def b_check(self, candidate: Candidate, env_state: dict) -> Tuple[bool, str]:
        """Hard constraints: fuse must not be VOID, confidence threshold."""
        mc = candidate.payload

        if mc.fuse_result == VOID:
            return False, "void_fuse"

        # For crystal fuses, require minimum confidence
        if mc.retrieval_type == "crystal_fuse" and mc.confidence < 0.01:
            return False, "low_confidence"

        return True, "approved"

    def einstein_score(self, candidate: Candidate, env_state: dict) -> Tuple[float, dict]:
        """E_out: confidence, stability, HARMONY proximity."""
        mc = candidate.payload

        # Confidence cost (lower confidence = higher cost)
        conf_cost = 1.0 - min(mc.confidence * 10.0, 1.0)

        # Stability cost (more seen = more stable = lower cost)
        stability = min(mc.seen / 100.0, 1.0)
        stab_cost = 1.0 - stability

        # HARMONY distance: how many CL steps to reach HARMONY
        harmony_dist = 0.0 if mc.fuse_result == HARMONY else 0.5

        e_out = 0.40 * conf_cost + 0.30 * stab_cost + 0.30 * harmony_dist

        details = {
            'confidence_cost': conf_cost,
            'stability_cost': stab_cost,
            'harmony_distance': harmony_dist,
            'seen_count': mc.seen,
        }
        return float(e_out), details

    def tesla_score(self, candidate: Candidate) -> Tuple[float, dict]:
        """E_in: D2 on operator sequence, path coherence."""
        mc = candidate.payload
        ops = mc.crystal_ops

        # D2 on operator sequence (treat operators as force vector indices)
        # Map each operator to its characteristic force vector
        if len(ops) >= 3:
            # Compute acceleration of operator sequence
            d2_sum = 0.0
            for i in range(len(ops) - 2):
                d2_sum += abs(ops[i] - 2 * ops[i+1] + ops[i+2])
            d2_norm = min(d2_sum / (len(ops) * NUM_OPS), 1.0)
        else:
            # For 2-grams, use CL composition quality
            d2_norm = 0.0 if mc.fuse_result == HARMONY else 0.4

        # Path coherence: does the sequence converge toward HARMONY?
        harmony_ratio = sum(1 for o in ops if o == HARMONY) / max(len(ops), 1)
        path_incoherence = 1.0 - harmony_ratio

        e_in = 0.50 * d2_norm + 0.50 * path_incoherence

        details = {
            'd2_operator': d2_norm,
            'harmony_ratio': harmony_ratio,
            'path_incoherence': path_incoherence,
        }
        return float(e_in), details


# ================================================================
#  DOMAIN: BIO-LATTICE (Hebrew root force sequences)
# ================================================================

@dataclass
class BioCandidate:
    """A candidate bio-lattice/DNA-like pattern."""
    sequence: str = ""
    force_vectors: List[Tuple[float, ...]] = field(default_factory=list)
    d2_curvature: float = 0.0
    operator_sequence: List[int] = field(default_factory=list)
    pattern_type: str = "root_pair"


# All available Hebrew root names for generation
_ROOT_NAMES = list(ROOTS_FLOAT.keys())
# Reverse map: letter -> index
_LETTER_INDEX = {ch: i for i, ch in enumerate('abcdefghijklmnopqrstuvwxyz')}


class BioLatticeDomain(BTQDomain):
    """BTQ domain for bio-lattice / Hebrew root force patterns."""

    @property
    def name(self) -> str:
        return "bio"

    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)

    def t_generate(self, env_state: dict, goal: dict, n: int) -> List[Candidate]:
        """Generate bio sequence candidates from Hebrew root combinations."""
        candidates = []
        letters = 'abcdefghijklmnopqrstuvwxyz'

        # Root pair combinations
        for _ in range(n // 2):
            length = self.rng.randint(3, 8)
            seq = ''.join(self.rng.choice(letters) for _ in range(length))

            forces = [FORCE_LUT_FLOAT[ord(ch) - ord('a')] for ch in seq]
            ops, d2, _ = _text_to_d2(seq)

            payload = BioCandidate(
                sequence=seq,
                force_vectors=forces,
                d2_curvature=d2,
                operator_sequence=ops,
                pattern_type="root_sequence",
            )
            candidates.append(Candidate(
                domain="bio",
                payload=payload,
                source=f"seq_{seq[:4]}",
            ))

        # Levy-perturbed sequences from good patterns
        if candidates:
            for _ in range(n - len(candidates)):
                base = self.rng.choice(candidates[:max(len(candidates)//2, 1)])
                base_seq = base.payload.sequence
                # Perturb: swap one character
                new_seq = list(base_seq)
                pos = self.rng.randint(0, len(new_seq) - 1)
                new_seq[pos] = self.rng.choice(letters)
                new_seq = ''.join(new_seq)

                forces = [FORCE_LUT_FLOAT[ord(ch) - ord('a')] for ch in new_seq]
                ops, d2, _ = _text_to_d2(new_seq)

                payload = BioCandidate(
                    sequence=new_seq,
                    force_vectors=forces,
                    d2_curvature=d2,
                    operator_sequence=ops,
                    pattern_type="levy_perturb",
                )
                candidates.append(Candidate(
                    domain="bio",
                    payload=payload,
                    source=f"levy_{new_seq[:4]}",
                ))

        return candidates[:n]

    def b_check(self, candidate: Candidate, env_state: dict) -> Tuple[bool, str]:
        """Hard constraints: valid sequence, minimum activity."""
        bc = candidate.payload

        if len(bc.sequence) < 2:
            return False, "too_short"

        if len(bc.sequence) > 100:
            return False, "too_long"

        # Reject flat/dead patterns (zero D2)
        if bc.d2_curvature < 0.001 and len(bc.operator_sequence) > 2:
            return False, "flat_pattern"

        return True, "approved"

    def einstein_score(self, candidate: Candidate, env_state: dict) -> Tuple[float, dict]:
        """E_out: pattern energy, binding strength."""
        bc = candidate.payload

        # Pattern energy: sum of force magnitudes (higher = more active)
        energy = 0.0
        for fv in bc.force_vectors:
            energy += sum(abs(v) for v in fv)
        energy_per_root = energy / max(len(bc.force_vectors), 1)
        # Normalize: typical force magnitude per root ~2.5
        energy_cost = abs(energy_per_root - 2.5) / 2.5

        # Binding strength: average binding dimension value
        binding_sum = sum(fv[3] for fv in bc.force_vectors)
        avg_binding = binding_sum / max(len(bc.force_vectors), 1)
        binding_cost = 1.0 - avg_binding  # Higher binding = lower cost

        e_out = 0.50 * energy_cost + 0.50 * binding_cost

        details = {
            'energy_per_root': energy_per_root,
            'energy_cost': energy_cost,
            'avg_binding': avg_binding,
            'binding_cost': binding_cost,
        }
        return float(min(e_out, 1.0)), details

    def tesla_score(self, candidate: Candidate) -> Tuple[float, dict]:
        """E_in: D2 curvature on 5D force vectors, helical quality."""
        bc = candidate.payload

        # D2 curvature (lower = smoother flow, clamp to [0,1])
        d2_norm = max(0.0, min(abs(bc.d2_curvature) / 0.5, 1.0))

        # Helical quality: check if force vectors trace a smooth path
        # Measure variance of consecutive force vector differences
        forces = bc.force_vectors
        if len(forces) >= 3:
            diffs = []
            for i in range(len(forces) - 1):
                diff = sum((forces[i+1][d] - forces[i][d])**2 for d in range(5))
                diffs.append(math.sqrt(diff))
            mean_diff = sum(diffs) / len(diffs)
            var_diff = sum((d - mean_diff)**2 for d in diffs) / len(diffs)
            # Low variance = consistent step size = helical
            helical_cost = max(0.0, min(var_diff * 10.0, 1.0))
        else:
            helical_cost = 0.5

        e_in = 0.60 * d2_norm + 0.40 * helical_cost

        details = {
            'd2_curvature': bc.d2_curvature,
            'helical_cost': helical_cost,
            'sequence_length': len(bc.sequence),
        }
        return float(max(0.0, min(e_in, 1.0))), details
