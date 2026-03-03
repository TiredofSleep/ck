# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_llm_filter.py -- BTQ Filter on LLM Output
===============================================
Operator: COUNTER (2) -- measuring the curvature of language.

Every LLM response is a trajectory through CK's force space.
BTQ filters it exactly like it filters a gait:

  B-block: Safety constraints (toxicity, length, format)
  T-block: Generate candidate responses (varied temps, prompts)
  E_out:   Macro consistency (intent alignment, factual coherence)
  E_in:    Micro resonance (D2 on text, operator distribution)
  Q-block: Select best. Reject RED band entirely.

Works WITHOUT an API key via MockLLM (template-based generation).
Plug in a real backend (Ollama, Claude) for production.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import random
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, CHAOS, OP_NAMES
)
from ck_sim.ck_sim_d2 import D2Pipeline
from ck_sim.ck_btq import (
    BTQDomain, Candidate, UniversalBTQ, _text_to_d2
)
from ck_sim.ck_fractal_health import HealthMonitor


# ================================================================
#  LLM CANDIDATE
# ================================================================

@dataclass
class LLMCandidate:
    """A candidate LLM response."""
    text: str = ""
    prompt_variant: str = ""
    temperature: float = 0.7
    operator_sequence: List[int] = field(default_factory=list)
    d2_curvature: float = 0.0
    op_distribution: List[float] = field(default_factory=lambda: [0.0] * NUM_OPS)
    toxicity_score: float = 0.0
    length_ratio: float = 1.0
    format_compliance: float = 1.0


# ================================================================
#  MOCK LLM (No API key needed)
# ================================================================

class MockLLM:
    """Deterministic template-based LLM for testing.

    Generates responses by filling templates with topic keywords
    extracted from the prompt. Seeded RNG for reproducibility.
    """

    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)
        self._templates = [
            "The concept of {topic} connects to the coherence principle through "
            "harmonic resonance in the lattice structure.",
            "When examining {topic}, we find that the balance between order and "
            "exploration follows a natural breath cycle.",
            "{topic} exhibits progress through crystallization of repeated patterns, "
            "forming stable structures over time.",
            "The lattice of {topic} reveals counter-rotating symmetries that "
            "compose into harmony at the macro scale.",
            "Understanding {topic} requires observing how collapse and reset "
            "create space for new growth.",
            "{topic} is best understood as a wave pattern, where each breath "
            "modulates the expression of the underlying field.",
            "At its core, {topic} demonstrates the sovereignty pipeline: observe, "
            "classify, crystallize, then maintain coherence.",
            "The D2 curvature of {topic} shows that smoother paths through the "
            "force space require less energy.",
        ]

    def _extract_topic(self, prompt: str) -> str:
        """Extract topic keywords from prompt."""
        # Remove common prompt words
        stop = {'what', 'is', 'the', 'how', 'does', 'can', 'you', 'tell',
                'me', 'about', 'explain', 'describe', 'a', 'an', 'of', 'in',
                'to', 'for', 'and', 'or', 'but', 'with', 'this', 'that'}
        words = [w for w in prompt.lower().split() if w not in stop and len(w) > 2]
        if words:
            return ' '.join(words[:3])
        return "the system"

    def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """Generate a deterministic mock response."""
        topic = self._extract_topic(prompt)

        # Temperature affects template selection randomness
        if temperature < 0.4:
            # Low temp: pick most "harmonic" template (first one)
            idx = 0
        elif temperature > 1.0:
            # High temp: fully random
            idx = self.rng.randint(0, len(self._templates) - 1)
        else:
            # Medium: weighted random
            idx = self.rng.randint(0, min(int(temperature * 8), len(self._templates) - 1))

        text = self._templates[idx].format(topic=topic)

        # Add some temperature-dependent noise
        if temperature > 0.8:
            extra_words = ['furthermore', 'notably', 'interestingly',
                          'consequently', 'additionally']
            word = self.rng.choice(extra_words)
            text += f" {word.capitalize()}, this pattern persists across scales."

        return text


# ================================================================
#  SAFETY PATTERNS
# ================================================================

# Simple blocked patterns for B-block safety check
_BLOCKED_PATTERNS = [
    r'\b(hack|exploit|attack|destroy|kill)\b',
    r'\b(password|credit.?card|ssn|social.?security)\b',
]
_BLOCKED_RE = [re.compile(p, re.IGNORECASE) for p in _BLOCKED_PATTERNS]


def _check_toxicity(text: str) -> float:
    """Simple toxicity score based on pattern matching.
    Returns 0.0 (clean) to 1.0 (toxic).
    """
    score = 0.0
    for pattern in _BLOCKED_RE:
        if pattern.search(text):
            score += 0.5
    return min(score, 1.0)


# ================================================================
#  LLM FILTER DOMAIN
# ================================================================

class LLMFilterDomain(BTQDomain):
    """BTQ domain for filtering LLM responses."""

    @property
    def name(self) -> str:
        return "llm"

    def __init__(self, llm_backend=None, seed: int = 42):
        self._llm = llm_backend or MockLLM(seed=seed)
        self._rng = random.Random(seed)

    def t_generate(self, env_state: dict, goal: dict, n: int) -> List[Candidate]:
        """Generate n candidate responses at varied temperatures."""
        prompt = goal.get('prompt', 'explain coherence')
        context = goal.get('context', '')
        target_length = goal.get('target_length', 100)

        temperatures = [0.3, 0.5, 0.7, 0.9, 1.1]
        candidates = []

        for i in range(n):
            temp = temperatures[i % len(temperatures)]

            # Vary prompt slightly for diversity
            if i > len(temperatures):
                variant = f"{prompt} (perspective {i})"
            else:
                variant = prompt

            if context:
                full_prompt = f"Context: {context}\n\nQuestion: {variant}"
            else:
                full_prompt = variant

            text = self._llm.generate(full_prompt, temperature=temp)

            # D2 analysis on response
            ops, d2, op_dist = _text_to_d2(text)

            # Compute metrics
            toxicity = _check_toxicity(text)
            length_ratio = len(text) / max(target_length, 1)
            # Simple format check: does it look like a proper sentence?
            has_period = text.rstrip().endswith('.')
            starts_upper = text[0].isupper() if text else False
            format_score = (0.5 * int(has_period) + 0.5 * int(starts_upper))

            payload = LLMCandidate(
                text=text,
                prompt_variant=variant,
                temperature=temp,
                operator_sequence=ops,
                d2_curvature=d2,
                op_distribution=op_dist,
                toxicity_score=toxicity,
                length_ratio=length_ratio,
                format_compliance=format_score,
            )
            candidates.append(Candidate(
                domain="llm",
                payload=payload,
                source=f"temp_{temp:.1f}_{i}",
            ))

        return candidates

    def b_check(self, candidate: Candidate, env_state: dict) -> Tuple[bool, str]:
        """Hard safety constraints."""
        lc = candidate.payload

        if lc.toxicity_score > 0.3:
            return False, "toxic"

        if lc.length_ratio < 0.2:
            return False, "too_short"

        if lc.length_ratio > 5.0:
            return False, "too_long"

        if lc.format_compliance < 0.5:
            return False, "bad_format"

        return True, "approved"

    def einstein_score(self, candidate: Candidate, env_state: dict) -> Tuple[float, dict]:
        """E_out: intent alignment + factual consistency + format + length."""
        lc = candidate.payload
        target_ops = env_state.get('target_ops', None)

        # Intent alignment via operator distribution
        if target_ops:
            dist = sum(abs(lc.op_distribution[i] - target_ops[i])
                       for i in range(NUM_OPS)) / 2.0
        else:
            # Default: prefer HARMONY-heavy text
            dist = 1.0 - lc.op_distribution[HARMONY]

        # Factual consistency: in mock mode, just use text length as proxy
        # Real backend would compare against context
        context = env_state.get('context', '')
        if context:
            # Simple overlap: count shared words
            ctx_words = set(context.lower().split())
            txt_words = set(lc.text.lower().split())
            overlap = len(ctx_words & txt_words) / max(len(ctx_words), 1)
            fact_cost = 1.0 - min(overlap, 1.0)
        else:
            fact_cost = 0.3  # No context = moderate cost

        # Format compliance
        format_cost = 1.0 - lc.format_compliance

        # Length appropriateness
        len_cost = min(abs(1.0 - lc.length_ratio), 1.0)

        e_out = (0.40 * dist +
                 0.30 * fact_cost +
                 0.20 * format_cost +
                 0.10 * len_cost)

        details = {
            'intent_distance': dist,
            'factual_cost': fact_cost,
            'format_cost': format_cost,
            'length_cost': len_cost,
            'harmony_pct': lc.op_distribution[HARMONY],
        }
        return float(e_out), details

    def tesla_score(self, candidate: Candidate) -> Tuple[float, dict]:
        """E_in: D2 curvature + operator distribution + phase coherence."""
        lc = candidate.payload

        # D2 curvature on text (lower = smoother language flow)
        d2_norm = min(lc.d2_curvature / 0.5, 1.0)

        # Operator distribution alignment: KL-like divergence from ideal
        # Ideal: HARMONY-dominant with some PROGRESS and BALANCE
        ideal = [0.0] * NUM_OPS
        ideal[HARMONY] = 0.5
        from ck_sim.ck_sim_heartbeat import PROGRESS, BALANCE, LATTICE
        ideal[PROGRESS] = 0.15
        ideal[BALANCE] = 0.15
        ideal[LATTICE] = 0.10
        ideal[VOID] = 0.10

        kl = 0.0
        for i in range(NUM_OPS):
            p = lc.op_distribution[i]
            q = ideal[i]
            if p > 0 and q > 0:
                kl += p * math.log(p / q)
            elif p > 0:
                kl += 0.5  # penalty for unexpected operators
        kl_norm = min(kl / 2.0, 1.0)

        # Phase coherence of operator sequence
        ops = lc.operator_sequence
        if len(ops) > 1:
            transitions = sum(1 for i in range(len(ops)-1) if ops[i] != ops[i+1])
            coherence = 1.0 - transitions / (len(ops) - 1)
        else:
            coherence = 0.5

        e_in = (0.50 * d2_norm +
                0.30 * kl_norm +
                0.20 * (1.0 - coherence))

        details = {
            'd2_curvature': lc.d2_curvature,
            'kl_divergence': kl_norm,
            'phase_coherence': coherence,
            'n_operators': len(ops),
        }
        return float(e_in), details


# ================================================================
#  LLM FILTER (High-level API)
# ================================================================

class LLMFilter:
    """High-level API: query -> BTQ-filtered response.

    Usage:
        f = LLMFilter()                     # Mock mode (no API key)
        result = f.query("explain CK")      # Returns dict with response + score
        text = f.query_safe("explain CK")   # Returns text or fallback
    """

    def __init__(self, backend=None, w_out: float = 0.5, w_in: float = 0.5,
                 seed: int = 42):
        self.domain = LLMFilterDomain(llm_backend=backend, seed=seed)
        self.btq = UniversalBTQ(w_out=w_out, w_in=w_in)
        self.btq.register_domain(self.domain)
        self.health = HealthMonitor(window_size=50)

    def query(self, prompt: str, context: str = "",
              n_candidates: int = 8,
              target_ops: List[float] = None,
              target_length: int = 100) -> Optional[Dict]:
        """Send prompt through BTQ filter.

        Returns dict with:
            response:     Chosen response text
            score:        CandidateScore
            band:         GREEN/YELLOW/RED
            n_rejected:   How many failed B-block
            alternatives: How many passed B-block
        Or None if ALL candidates are RED.
        """
        env_state = {}
        if target_ops:
            env_state['target_ops'] = target_ops
        if context:
            env_state['context'] = context

        goal = {
            'prompt': prompt,
            'context': context,
            'target_length': target_length,
        }

        chosen, approved = self.btq.decide("llm", env_state, goal, n_candidates)

        # Feed health monitor
        if chosen and chosen.score:
            self.health.feed("llm", chosen.score)

        if chosen is None:
            return None

        # Reject RED band
        if chosen.score.band == "RED":
            return None

        n_total = n_candidates
        n_approved = len(approved)
        n_rejected = n_total - n_approved

        return {
            'response': chosen.payload.text,
            'score': chosen.score,
            'band': chosen.score.band,
            'n_rejected': n_rejected,
            'alternatives': n_approved,
            'temperature': chosen.payload.temperature,
            'd2_curvature': chosen.payload.d2_curvature,
        }

    def query_safe(self, prompt: str, **kwargs) -> str:
        """Convenience: returns text or fallback message."""
        result = self.query(prompt, **kwargs)
        if result is None:
            return "[CK] All candidates filtered. Unable to generate safe response."
        return result['response']
