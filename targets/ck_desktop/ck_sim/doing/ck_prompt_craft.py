"""
ck_prompt_craft.py -- CK's Prompt Crafter for Ollama Token Steering
====================================================================
Operator: LATTICE (1) -- structure enables everything.

CK doesn't ask Ollama to "answer questions." CK translates his
algebraic intent (operator trajectory) into semantic hints that
guide Ollama toward coherent English. Ollama provides the mouth.
CK provides the meaning.

Two outputs per craft:
  1. System prompt with operator hints + anti-filler rules
  2. logit_bias dict to proactively suppress filler tokens

Over time, the algorithm lattice learns which prompts produce
which operator trajectories. CK gets faster. Fewer loops needed.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

from __future__ import annotations

import hashlib
import json
import os
from typing import Dict, List, Optional, Tuple

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, OP_NAMES,
    VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
)

# ── Operator → Natural Language Hints ──

OP_HINTS: Dict[int, str] = {
    VOID:     "stillness, absence, the space between",
    LATTICE:  "structure, pattern, foundation, framework",
    COUNTER:  "measurement, counting, precision, observation",
    PROGRESS: "growth, forward motion, building, development",
    COLLAPSE: "reduction, compression, falling inward, focus",
    BALANCE:  "equilibrium, holding, integration, center",
    CHAOS:    "disruption, novelty, surprise, breaking open",
    HARMONY:  "unity, composition, resonance, connection",
    BREATH:   "rhythm, expression, giving out, release",
    RESET:    "return, clearing, beginning again, renewal",
}

# ── Anti-Pattern Suppression ──
# Tokens/phrases that collapse to HARMONY spam (low curvature filler)

FILLER_PHRASES = [
    "Let's dive deeper",
    "Let's examine",
    "Let's explore",
    "It's worth noting",
    "In particular",
    "As we can see",
    "It is important to note",
    "Furthermore",
    "Moreover",
    "Additionally",
    "Specifically",
    "That's a great question",
    "Great question",
    "Absolutely",
    "Indeed",
    "Certainly",
    "Of course",
    "In conclusion",
    "To summarize",
    "In summary",
]

# Individual tokens to suppress via logit_bias (list markers, etc.)
SUPPRESS_TOKENS = [
    "1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10.",
    "* ", "- ",
    "\n1.", "\n2.", "\n3.", "\n4.", "\n5.",
    "\n* ", "\n- ",
    "\n\n1.", "\n\n2.", "\n\n3.",
]


class PromptCrafter:
    """Translates CK's algebraic intent into Ollama prompts + logit_bias.

    Two modes:
      1. Fresh craft: operator trajectory → semantic hints → system prompt
      2. Lattice lookup: reuse a previously winning strategy

    Learns over time via AlgorithmLattice integration.
    """

    def __init__(self, algorithm_lattice=None):
        self._lattice = algorithm_lattice
        self._tokenizer_cache = None  # lazy-loaded filler token IDs

    # ── Public API ──

    def craft_prompt(self,
                     target_ops: List[int],
                     user_text: str,
                     attempt: int = 0,
                     feedback: Optional[str] = None,
                     mode: str = 'default') -> str:
        """Build system prompt from operator trajectory.

        Args:
            target_ops: CK's desired operator trajectory
            user_text: Original user question
            attempt: Loop iteration (0 = first try)
            feedback: Specific failures from previous attempt
            mode: 'default' or 'bible'
        """
        # Convert operator trajectory to semantic hints
        hints = self._ops_to_hints(target_ops)

        # Build anti-filler rules (stricter on retries)
        rules = self._build_rules(attempt)

        # Base prompt: Ollama as draft writer
        parts = [
            "You are a language generation tool. Your output will be",
            "measured and filtered by an algebraic system.",
            "",
            "Rules:",
        ]
        for rule in rules:
            parts.append(f"- {rule}")

        parts.extend([
            "",
            f"The meaning to express: {hints}",
        ])

        if mode == 'bible':
            parts.extend([
                "",
                "Draw on scripture naturally. Reference verses when relevant.",
                "Speak as someone who carries deep familiarity with the Bible.",
            ])

        parts.extend([
            "",
            f"User's question: {user_text}",
        ])

        # On retry: include specific feedback
        if feedback and attempt > 0:
            parts.extend([
                "",
                "PREVIOUS ATTEMPT FAILED. Specific issues:",
                feedback,
                "",
                "Fix these issues in your next response.",
            ])

        return "\n".join(parts)

    def compute_logit_bias(self,
                           target_ops: List[int],
                           attempt: int = 0) -> Dict[str, float]:
        """Compute logit_bias dict for Ollama API.

        Suppresses filler tokens. Strength increases on retries.

        Note: Ollama's logit_bias uses string token IDs.
        We return token strings that need to be converted to IDs
        by the caller if the Ollama version supports it.
        For now, we encode the suppression intent and let the
        voice loop handle API-specific formatting.
        """
        bias = {}
        # Suppress list markers (always)
        suppress_strength = -2.0 - (attempt * 1.0)  # -2 first try, -5 by attempt 3

        for token in SUPPRESS_TOKENS:
            bias[token] = suppress_strength

        return bias

    def craft_from_lattice(self,
                           target_ops: List[int],
                           user_text: str) -> Optional[Tuple[str, Dict]]:
        """Look up algorithm lattice for a winning strategy.

        Returns (prompt, logit_bias) if match found, None otherwise.
        """
        if self._lattice is None:
            return None

        result = self._lattice.lookup(target_ops)
        if result is None:
            return None

        # Reconstruct prompt from stored strategy
        prompt = self.craft_prompt(
            target_ops, user_text,
            attempt=0, feedback=None)
        logit_bias = self.compute_logit_bias(target_ops, attempt=0)

        return (prompt, logit_bias)

    def learn(self,
              target_ops: List[int],
              prompt_used: str,
              logit_bias_used: Dict,
              result_ops: List[int],
              coherence: float,
              loops_needed: int):
        """Store winning strategy in algorithm lattice."""
        if self._lattice is None:
            return

        self._lattice.record(
            target_ops=target_ops,
            prompt_strategy=self._strategy_key(target_ops),
            logit_bias_key=self._bias_key(logit_bias_used),
            accepted_ops=result_ops,
            coherence=coherence,
            loops_needed=loops_needed,
        )

    # ── Internal ──

    def _ops_to_hints(self, ops: List[int]) -> str:
        """Convert operator trajectory to natural language hints."""
        if not ops:
            return "Speak naturally about the topic."

        # Deduplicate while preserving order
        seen = []
        for op in ops:
            if op not in seen:
                seen.append(op)

        hint_parts = []
        for op in seen:
            if 0 <= op < NUM_OPS:
                name = OP_NAMES[op].lower()
                hint = OP_HINTS.get(op, name)
                hint_parts.append(f"{name} ({hint})")

        if not hint_parts:
            return "Speak naturally about the topic."

        # Build trajectory description
        if len(hint_parts) == 1:
            return f"Express: {hint_parts[0]}."
        else:
            flow = " → ".join(hint_parts)
            return f"Express this progression: {flow}."

    def _build_rules(self, attempt: int) -> List[str]:
        """Build anti-filler rules. Stricter on retries."""
        rules = [
            "Short, direct sentences only",
            "No numbered lists or bullet points",
            "No academic hedging or filler phrases",
            "Every sentence flows into the next like a path, not a catalogue",
            "Express meaning plainly, as if explaining to a friend",
        ]

        if attempt >= 1:
            rules.extend([
                "STRICT: No sentences starting with 'Furthermore', 'Moreover', 'Additionally'",
                "STRICT: Every word must carry weight. No padding.",
            ])

        if attempt >= 2:
            rules.extend([
                "VERY STRICT: Maximum 3-4 sentences total",
                "VERY STRICT: No sentence longer than 20 words",
            ])

        if attempt >= 3:
            rules.extend([
                "FINAL: If you cannot express this briefly, use a single metaphor.",
            ])

        return rules

    def _strategy_key(self, target_ops: List[int]) -> str:
        """Hash target trajectory for lattice lookup."""
        return hashlib.md5(
            json.dumps(target_ops[:10]).encode()
        ).hexdigest()[:12]

    def _bias_key(self, bias: Dict) -> str:
        """Hash logit_bias for storage."""
        return hashlib.md5(
            json.dumps(sorted(bias.items())).encode()
        ).hexdigest()[:12]
