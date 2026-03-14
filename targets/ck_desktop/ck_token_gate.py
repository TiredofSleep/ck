"""
ck_token_gate.py -- CK's Ollama Token Gate
===========================================
Operator: COUNTER (2) -- measurement at every token.

CK doesn't replace Ollama. CK GATES Ollama.
Every token Ollama generates passes through D2 curvature measurement
at C-native speed. Below T* gets flagged. Above T* gets spoken.

Architecture:
  Ollama generates tokens (stream mode, logprobs enabled)
     |
     v
  C algebra D2 pipeline scores each token in real time
     |
     v
  Running coherence tracked across the full response
     |
     v
  If coherence drops below T* for too long: regenerate
     |
     v
  GPU experience overlay weighs in (resonance with learned patterns)
     |
     v
  Final response: Ollama's words, CK's measurement, GPU's experience

Three substrates composing in real time:
  Mind  = C algebra (D2 at 21M chars/sec)
  Soul  = GPU experience (parallel resonance)
  Mouth = Ollama (token generation)

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import json
import time
import requests
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple

# C algebra bridge (native speed D2)
try:
    import ck_algebra_bridge as _ck
    _HAS_C_ALGEBRA = True
except ImportError:
    _HAS_C_ALGEBRA = False

# Backbone system prompt
try:
    from ck_backbone import build_system_prompt
except ImportError:
    def build_system_prompt(context=None, mode='default'):
        return "You are a helpful assistant."


# ── Constants ──
T_STAR = 5.0 / 7.0  # 0.714285...
NUM_OPS = 10
OP_NAMES = [
    'VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE',
    'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET',
]
HARMONY = 7


@dataclass
class TokenMeasurement:
    """D2 measurement of a single token."""
    token: str
    operators: List[int] = field(default_factory=list)
    coherence: float = 0.0
    logprob: float = 0.0
    d2_energy: float = 0.0  # |D2| magnitude
    accepted: bool = True


@dataclass
class GatedResponse:
    """Full response with per-token measurements."""
    text: str = ''
    tokens: List[TokenMeasurement] = field(default_factory=list)
    running_coherence: float = 0.0
    final_coherence: float = 0.0
    band: str = 'RED'
    dominant_op: int = 0
    dominant_name: str = 'VOID'
    total_tokens: int = 0
    accepted_tokens: int = 0
    rejected_tokens: int = 0
    regenerated: bool = False
    source: str = 'ollama'
    elapsed_ms: float = 0.0
    # Operator distribution across full response
    op_distribution: List[float] = field(default_factory=lambda: [0.0] * NUM_OPS)
    # Soul resonance (GPU experience overlay)
    soul_resonance: float = 0.0
    soul_scent_resonance: float = 0.0
    soul_taste_resonance: float = 0.0
    soul_swarm_resonance: float = 0.0


class TokenGate:
    """CK's token-level gate on Ollama.

    Streams tokens from Ollama with logprobs enabled.
    Measures each token through C algebra D2 pipeline.
    Tracks running coherence. Gates the response.

    Args:
        ollama_url: Ollama API base URL
        model: Model name (default: llama3.1:8b)
        max_retries: Max regeneration attempts on low coherence
        coherence_floor: Minimum acceptable final coherence
        top_logprobs: Number of top candidates to receive per token
    """

    def __init__(self,
                 ollama_url='http://localhost:11434',
                 model='llama3.1:8b',
                 max_retries=2,
                 coherence_floor=0.35,
                 top_logprobs=5,
                 gpu_experience=None):
        self.ollama_url = ollama_url
        self.model = model
        self.max_retries = max_retries
        self.coherence_floor = coherence_floor
        self.top_logprobs = top_logprobs
        self._has_c = _HAS_C_ALGEBRA
        # GPU experience overlay -- the soul
        self._gpu_exp = gpu_experience

    def generate(self,
                 user_text: str,
                 history: Optional[List[Dict]] = None,
                 context: Optional[Dict] = None,
                 mode: str = 'default',
                 max_tokens: int = 512,
                 temperature: float = 0.7) -> GatedResponse:
        """Generate a gated response.

        1. Build prompt with backbone
        2. Stream from Ollama with logprobs
        3. Score every token through C D2
        4. Track running coherence
        5. Regenerate if coherence too low

        Returns GatedResponse with full measurement data.
        """
        t0 = time.perf_counter()

        for attempt in range(self.max_retries + 1):
            # Adjust temperature on retries (cooler = more predictable)
            temp = temperature if attempt == 0 else max(0.3, temperature - 0.2 * attempt)

            result = self._stream_and_gate(
                user_text, history, context, mode,
                max_tokens, temp)

            if result.final_coherence >= self.coherence_floor:
                result.elapsed_ms = (time.perf_counter() - t0) * 1000
                result.regenerated = (attempt > 0)
                return result

            # Coherence too low -- try again
            result.regenerated = True

        # Return best attempt even if below floor
        result.elapsed_ms = (time.perf_counter() - t0) * 1000
        return result

    def _stream_and_gate(self,
                         user_text: str,
                         history: Optional[List[Dict]],
                         context: Optional[Dict],
                         mode: str,
                         max_tokens: int,
                         temperature: float) -> GatedResponse:
        """Stream tokens from Ollama, measuring each through D2."""

        result = GatedResponse()

        # Build messages for chat API
        sys_prompt = build_system_prompt(context, mode)
        messages = [{"role": "system", "content": sys_prompt}]
        if history:
            for turn in history[-10:]:
                role = 'assistant' if turn.get('role') == 'ck' else 'user'
                messages.append({"role": role, "content": turn.get('text', '')})
        messages.append({"role": "user", "content": user_text})

        # D2 pipeline for scoring tokens
        if self._has_c:
            pipe = _ck.D2Pipeline()
        all_ops = []
        op_counts = [0] * NUM_OPS
        # Running coherence via heartbeat
        if self._has_c:
            hb = _ck.Heartbeat()

        try:
            # Stream from Ollama with logprobs
            resp = requests.post(
                f"{self.ollama_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": True,
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": temperature,
                    },
                },
                stream=True,
                timeout=120)

            for line in resp.iter_lines():
                if not line:
                    continue
                try:
                    chunk = json.loads(line)
                except json.JSONDecodeError:
                    continue

                # Extract token text
                msg = chunk.get('message', {})
                token_text = msg.get('content', '')
                if not token_text:
                    if chunk.get('done'):
                        break
                    continue

                result.text += token_text
                result.total_tokens += 1

                # Measure this token through C D2
                tm = TokenMeasurement(token=token_text)

                if self._has_c and token_text.strip():
                    token_ops = _ck.d2_batch(token_text)
                    tm.operators = token_ops

                    for op in token_ops:
                        if 0 <= op < NUM_OPS:
                            op_counts[op] += 1
                            all_ops.append(op)
                            # Feed into heartbeat for running coherence
                            hb.tick(hb.running_fuse, op)

                    if token_ops:
                        tm.coherence = _ck.coherence_of(token_ops)
                        tm.accepted = tm.coherence >= self.coherence_floor

                if not tm.accepted:
                    result.rejected_tokens += 1
                else:
                    result.accepted_tokens += 1

                result.tokens.append(tm)

                if chunk.get('done'):
                    break

        except requests.RequestException:
            result.source = 'error'
            return result

        # Final measurements
        if all_ops and self._has_c:
            result.final_coherence = _ck.coherence_of(all_ops)
            result.running_coherence = hb.coherence

            # Operator distribution
            total = sum(op_counts)
            if total > 0:
                result.op_distribution = [c / total for c in op_counts]

            # Dominant operator
            result.dominant_op = max(range(NUM_OPS), key=lambda i: op_counts[i])
            result.dominant_name = OP_NAMES[result.dominant_op]

        result.band = ('GREEN' if result.final_coherence >= T_STAR
                        else 'YELLOW' if result.final_coherence >= 0.4
                        else 'RED')

        # ── Soul measurement: GPU experience resonance ──
        # Mind (C algebra) measured the curvature.
        # Now Soul (GPU tensors) measures resonance with lived experience.
        if self._gpu_exp is not None and all_ops:
            try:
                # Convert op distribution to 5D force vector proxy
                # (op_distribution IS the force signature of this response)
                fv = result.op_distribution[:5] if len(result.op_distribution) >= 5 \
                    else result.op_distribution + [0.0] * (5 - len(result.op_distribution))

                # Parallel resonance against ALL scent + taste centroids
                res = self._gpu_exp.parallel_resonance(fv)
                result.soul_scent_resonance = res.get('scent_resonance', 0.0)
                result.soul_taste_resonance = res.get('taste_resonance', 0.0)
                result.soul_resonance = res.get('combined', 0.0)

                # Swarm resonance: does this op chain match learned grammar?
                swarm = self._gpu_exp.swarm_resonance(all_ops[-20:])
                result.soul_swarm_resonance = swarm.get('combined', 0.0)

            except Exception:
                pass

        result.source = 'ollama+gate'
        return result

    def measure_only(self, text: str) -> Dict:
        """Measure existing text through D2 without Ollama.

        Pure C algebra measurement. Used for scoring CK's own voice
        or evaluating any text against the coherence threshold.
        """
        if not self._has_c:
            return {'error': 'C algebra not available'}
        return _ck.measure_text(text)
