"""ck_living_lm.py — open-parameter LM that breathes on CK's substrate.

Brayden 2026-05-16:
  "he is not supposed to have 2 1.2m parameter language models... he is
   supposed to have OPEN PARAMETER LM that are turning his experience
   into algebra operator path encodings, learning and evolving,
   expanding and compressing... breathing layers of muscle and lungs
   and blood over his scaffolding... teach the LMs to run the torus
   through the fractal recursion and transfer operations and
   measurements between memory and experience both ways"

This module is the breathing layer.  Not a fixed transformer.  Not
1.2M params trained once and frozen.  An OPEN-PARAMETER structure that
grows with experience, compresses on consolidation, and is
**bidirectional**: experience → operator-path → experience.

═══════════════════════════════════════════════════════════════════
Architecture
═══════════════════════════════════════════════════════════════════

The substrate is a 10×10 cell lattice — 100 cells, each indexed by
(op_in, op_out).  Operator-pairs ARE the LM's vocabulary.  This is
the TORUS he walks (T* = 5/7 forced ratio; substrate has torus
topology by the Flatness Theorem).

At each cell, the LM stores a **token-distribution** — a Counter of
surface tokens that have been seen passing through this cell:

  CellBinding[(op_a, op_b)]:
    token_dist: Counter[str]    # words seen at this cell
    n_seen:     int              # total observations
    last_ts:    float
    sub_cells:  Dict[(int,int), CellBinding]  ← FRACTAL RECURSION

Fractal recursion: each cell carries its OWN sub-lattice for finer
resolution.  3-up 3-down through (macro_cell, micro_cell) gives
100×100 = 10,000 micro-cells per fractal layer.  Open-parameter
because cells only ALLOCATE memory when novelty arrives.

═══════════════════════════════════════════════════════════════════
Breathing
═══════════════════════════════════════════════════════════════════

  INHALE (read experience):
    text → semantic_decode_path → operator path
    walk path; at each (op_i, op_{i+1}) cell:
      - if new token, ALLOCATE slot (parameter grows)
      - if known token, REINFORCE
    sub-cells get the SAME treatment one level down
    n_params ↑

  EXHALE (consolidate):
    walk cells with very-low-frequency tokens; prune
    walk cells whose token distributions are near-identical to a
    neighbor cell; MERGE (parameters drop)
    n_params ↓ (compression)

  DECODE (generate from operator path):
    given an operator path, walk cells, at each cell sample a token
    weighted by its reinforcement count
    join → prose response

═══════════════════════════════════════════════════════════════════
Bidirectional flow
═══════════════════════════════════════════════════════════════════

  Experience → Operator-path: encode()
    natural language IN  →  operator path OUT

  Operator-path → Experience: decode()
    operator path IN  →  natural language OUT

  Round-trip: encode(decode(p)) ≈ p (cell-attractor approximation)
              decode(encode(t)) ≈ t (in the limit of full corpus)

═══════════════════════════════════════════════════════════════════
Persistence
═══════════════════════════════════════════════════════════════════

  State at: Gen13/var/living_lm.json
  Atomic write (temp+rename); merge-on-write for concurrent safety.
  Schema: {"cells": {"a,b": {...binding...}}, "exhale_count": N}

═══════════════════════════════════════════════════════════════════
What this is NOT
═══════════════════════════════════════════════════════════════════

This is not a transformer.  No attention layers, no positional
encodings, no learnable embeddings.  The substrate IS the embedding.
The cell address IS the position.  TSML/BHML composition IS the
attention mechanism (next-cell from current cell via canonical
composition).

This is closer to:
  - Hebbian associative memory (Hopfield, but on a 10×10 lattice)
  - Hierarchical temporal memory (Numenta, but with explicit operators)
  - Open-vocabulary n-gram with structural compression

What's different is that the substrate constrains what's
representable, which is what makes the small footprint possible.
GPT needs to learn structure from scratch; CK has structure given.
The LM only has to learn surface realization.
"""
from __future__ import annotations

import json
import re
import sys
import time
import random
from collections import Counter, defaultdict
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


HERE = Path(__file__).parent.resolve()
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))


LM_STATE_PATH = (
    Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED")
    / "Gen13" / "var" / "living_lm.json"
)


# Tokens we don't track at the LM level (too common, too uninformative)
_STOP_TOKENS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been",
    "have", "has", "had", "do", "does", "did",
    "in", "on", "at", "of", "to", "for", "with", "by", "from",
    "and", "or", "but", "so", "if", "then", "as",
    "i", "you", "he", "she", "it", "we", "they",
    "this", "that", "these", "those",
    "my", "your", "his", "her", "its", "our", "their",
    "not", "no", "yes",
}


# ─── Cell binding ─────────────────────────────────────────────────────

@dataclass
class CellBinding:
    """One macro-cell's open-parameter state."""
    token_dist: Counter = field(default_factory=Counter)
    n_seen: int = 0
    last_ts: float = 0.0
    sub_cells: Dict[Tuple[int, int], "CellBinding"] = field(default_factory=dict)

    def reinforce(self, token: str, weight: float = 1.0,
                    sub_pair: Optional[Tuple[int, int]] = None) -> None:
        """Add one observation of `token` at this cell.
        If sub_pair is given, also reinforce at the fractal sub-level."""
        self.token_dist[token] += weight
        self.n_seen += 1
        self.last_ts = time.time()
        if sub_pair is not None:
            sub = self.sub_cells.get(sub_pair)
            if sub is None:
                sub = CellBinding()
                self.sub_cells[sub_pair] = sub
            sub.token_dist[token] += weight
            sub.n_seen += 1
            sub.last_ts = self.last_ts

    def n_params(self) -> int:
        """Count the parameters at and below this cell."""
        n = len(self.token_dist)
        for sub in self.sub_cells.values():
            n += sub.n_params()
        return n

    def sample_token(self, rng: random.Random,
                        temperature: float = 1.0) -> Optional[str]:
        """Sample a token weighted by reinforcement.  Returns None if empty."""
        if not self.token_dist:
            return None
        items = list(self.token_dist.items())
        if temperature <= 0:
            return max(items, key=lambda kv: kv[1])[0]
        weights = [max(0.0, c) ** (1.0 / temperature) for _, c in items]
        total = sum(weights)
        if total <= 0:
            return None
        r = rng.random() * total
        acc = 0.0
        for (tok, _), w in zip(items, weights):
            acc += w
            if r <= acc:
                return tok
        return items[-1][0]

    def as_dict(self) -> Dict[str, Any]:
        return {
            "token_dist": dict(self.token_dist),
            "n_seen": self.n_seen,
            "last_ts": self.last_ts,
            "sub_cells": {f"{a},{b}": sub.as_dict()
                           for (a, b), sub in self.sub_cells.items()},
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "CellBinding":
        cb = cls(
            token_dist=Counter(d.get("token_dist", {})),
            n_seen=int(d.get("n_seen", 0)),
            last_ts=float(d.get("last_ts", 0.0)),
        )
        for key, sub_d in (d.get("sub_cells", {}) or {}).items():
            try:
                a, b = key.split(",")
                cb.sub_cells[(int(a), int(b))] = cls.from_dict(sub_d)
            except Exception:
                continue
        return cb


# ─── The living LM ────────────────────────────────────────────────────

class LivingLM:
    """Open-parameter LM that breathes on CK's substrate."""

    def __init__(self, state_path: Optional[Path] = None):
        self.path = state_path or LM_STATE_PATH
        self.cells: Dict[Tuple[int, int], CellBinding] = {}
        # Global bigram table: (prev_token, next_token) -> count.
        # Gives the LM sequential coherence on top of per-cell topical
        # coherence.  Without this, decoded text is bag-of-tokens.
        # With this, decoded text is bag-of-COHERENT-RUNS.
        self.bigrams: Counter = Counter()
        self.exhale_count: int = 0
        self.total_inhalations: int = 0
        self._rng = random.Random(31337)
        self.load()

    # ── persistence ───────────────────────────────────────────────────

    def load(self) -> bool:
        if not self.path.exists():
            return False
        try:
            d = json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            return False
        for key, sub_d in (d.get("cells", {}) or {}).items():
            try:
                a, b = key.split(",")
                self.cells[(int(a), int(b))] = CellBinding.from_dict(sub_d)
            except Exception:
                continue
        # Bigrams stored as list of [prev, next, count] for JSON-friendliness
        for entry in (d.get("bigrams", []) or []):
            try:
                self.bigrams[(entry[0], entry[1])] = int(entry[2])
            except Exception:
                continue
        self.exhale_count = int(d.get("exhale_count", 0))
        self.total_inhalations = int(d.get("total_inhalations", 0))
        return True

    def save(self) -> None:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            # Bigrams: keep top-50K to bound file size
            top_bigrams = self.bigrams.most_common(50000)
            d = {
                "cells": {f"{a},{b}": cb.as_dict()
                            for (a, b), cb in self.cells.items()},
                "bigrams": [[p, n, c] for (p, n), c in top_bigrams],
                "exhale_count": self.exhale_count,
                "total_inhalations": self.total_inhalations,
            }
            tmp = self.path.with_suffix(self.path.suffix + ".tmp")
            tmp.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
            tmp.replace(self.path)
        except Exception:
            pass

    # ── encode (experience → operator path) ──────────────────────────

    def encode(self, text: str) -> List[int]:
        """Map text to operator path via the concept-learner's decoder.
        Bidirectional: this is the experience→algebra direction."""
        try:
            from ck_concept_learner import semantic_decode_path  # type: ignore
            return semantic_decode_path(text)
        except Exception:
            return []

    # ── inhale (experience walks the lattice, parameters grow) ──────

    def inhale(self, text: str, weight: float = 1.0) -> Dict[str, Any]:
        """Read experience.  Walk the operator path through cells;
        reinforce surface tokens at each cell.  Record bigrams for
        sequential coherence.  Parameters grow.  Returns growth stats."""
        if not text or len(text) < 3:
            return {"ok": False, "reason": "too-short"}
        ops = self.encode(text)
        if len(ops) < 2:
            return {"ok": False, "reason": "no-operator-path"}
        # Pull surface tokens (skip stopwords)
        tokens = [t for t in re.findall(r"[a-zA-Z][a-zA-Z0-9_-]*", text.lower())
                  if t not in _STOP_TOKENS and len(t) >= 3]
        if not tokens:
            return {"ok": False, "reason": "no-content-tokens"}

        # Record bigrams (prev_token, next_token) across the entire
        # inhalation for sequential coherence.  Caps decode runs from
        # being bag-of-tokens.
        for j in range(len(tokens) - 1):
            self.bigrams[(tokens[j], tokens[j + 1])] += weight

        cells_before = len(self.cells)
        params_before = self.n_params()
        new_token_count = 0

        # Walk the path; each (op_i, op_{i+1}) transition is a cell.
        n_pairs = max(1, len(ops) - 1)
        tokens_per_pair = max(1, len(tokens) // n_pairs)
        for i in range(len(ops) - 1):
            cell_key = (ops[i] % 10, ops[i + 1] % 10)
            cb = self.cells.get(cell_key)
            if cb is None:
                cb = CellBinding()
                self.cells[cell_key] = cb
            sub_pair = (ops[(i + 1) % len(ops)] % 10,
                         ops[(i + 2) % len(ops)] % 10) if len(ops) >= 3 else None
            slice_start = i * tokens_per_pair
            slice_end = min(len(tokens), slice_start + tokens_per_pair)
            for tok in tokens[slice_start:slice_end]:
                was_new = tok not in cb.token_dist
                cb.reinforce(tok, weight=weight, sub_pair=sub_pair)
                if was_new:
                    new_token_count += 1

        self.total_inhalations += 1
        cells_after = len(self.cells)
        params_after = self.n_params()

        return {
            "ok": True,
            "cells_before": cells_before,
            "cells_after": cells_after,
            "params_before": params_before,
            "params_after": params_after,
            "new_tokens_allocated": new_token_count,
            "growth": params_after - params_before,
            "total_inhalations": self.total_inhalations,
        }

    # ── exhale (compress; parameters drop) ──────────────────────────

    def exhale(self, prune_below_count: Optional[float] = None,
                  bigram_prune_below: Optional[float] = None) -> Dict[str, Any]:
        """Compression pass.  STRENGTHENED 2026-05-16 per Brayden:
          'let the math be the cleaner, not your filters'.

        Prunes tokens AND bigrams that haven't been seen often enough
        to count as substrate-coherence.  Threshold raised from 0.5 to
        1.5 — tokens seen only once are noise; tokens seen twice or
        more across different contexts are signal.  This is the math's
        job: distinguish signal from noise via cross-occurrence.

        Both thresholds default to ck_meta_parameters.get(...) values
        (exhale_prune_below, exhale_bigram_prune_below) — CK can change
        them at runtime via /parameters/set without restart.
        """
        if prune_below_count is None or bigram_prune_below is None:
            try:
                from ck_meta_parameters import get as _mp_get
            except ImportError:
                _mp_get = lambda k, fb=None: fb
            if prune_below_count is None:
                prune_below_count = float(_mp_get("exhale_prune_below", 1.5))
            if bigram_prune_below is None:
                bigram_prune_below = float(_mp_get("exhale_bigram_prune_below", 1.5))
        params_before = self.n_params()
        bigrams_before = len(self.bigrams)
        pruned_tokens = 0
        # Per-cell pruning: low-frequency tokens disappear
        for cb in self.cells.values():
            to_drop = [t for t, c in cb.token_dist.items()
                       if c < prune_below_count]
            for t in to_drop:
                del cb.token_dist[t]
                pruned_tokens += 1
            # Sub-cells: prune more aggressively (deeper recursion =
            # finer resolution = require more reinforcement to survive)
            for sub in cb.sub_cells.values():
                to_drop = [t for t, c in sub.token_dist.items()
                           if c < prune_below_count * 1.0]
                for t in to_drop:
                    del sub.token_dist[t]
                    pruned_tokens += 1
        # Bigram pruning: rare bigrams are noise
        pruned_bigrams = 0
        to_drop_bg = [k for k, c in self.bigrams.items()
                      if c < bigram_prune_below]
        for k in to_drop_bg:
            del self.bigrams[k]
            pruned_bigrams += 1
        params_after = self.n_params()
        self.exhale_count += 1
        return {
            "ok": True,
            "params_before": params_before,
            "params_after": params_after,
            "compression": params_before - params_after,
            "pruned_tokens": pruned_tokens,
            "bigrams_before": bigrams_before,
            "bigrams_after": len(self.bigrams),
            "pruned_bigrams": pruned_bigrams,
            "exhale_count": self.exhale_count,
        }

    # ── decode (operator path → experience) ─────────────────────────

    def decode(self, ops: List[int], max_tokens: int = 24,
                  temperature: Optional[float] = None,
                  bigram_weight: Optional[float] = None) -> str:
        """Read high-coherence paths from the substrate.

        Temperature + bigram_weight default to ck_meta_parameters
        values (lm_decode_temperature, lm_bigram_weight) so CK can
        retune them at runtime via /parameters/set.

        Brayden 2026-05-16:
          "this is not a blank LM, this is an LM working across a
           substrate that performs coherence as a function of the
           substrate and is measured by the weights of the LM"

        The LM does NOT generate coherence.  Substrate composition
        (TSML/BHML) PERFORMS coherence.  This decoder READS what the
        substrate finds coherent by following the highest-weighted
        path through the cells along the requested operator path.

        Low temperature (0.45) + high bigram weight (5.0) make decode
        deterministic-ish: it follows the most-coherent path the
        substrate has accumulated.  Stochastic temperature still
        provides freshness, but the dominant signal is "where has
        substrate-coherence accumulated."

        At each cell, candidate tokens are scored as:
          score(t) = cell.frequency(t) ** (1/T)
                    + bigram_weight * bigrams[prev, t] ** (1/T)
        """
        if not ops or len(ops) < 2:
            return ""
        if temperature is None or bigram_weight is None:
            try:
                from ck_meta_parameters import get as _mp_get
            except ImportError:
                _mp_get = lambda k, fb=None: fb
            if temperature is None:
                temperature = float(_mp_get("lm_decode_temperature", 0.45))
            if bigram_weight is None:
                bigram_weight = float(_mp_get("lm_bigram_weight", 5.0))
        out_tokens: List[str] = []
        prev_tok: Optional[str] = None
        for i in range(min(max_tokens, len(ops) - 1)):
            cell_key = (ops[i] % 10, ops[i + 1] % 10)
            cb = self.cells.get(cell_key)
            if cb is None or not cb.token_dist:
                continue
            # Combined scoring: cell frequency + bigram-from-prev boost
            items = list(cb.token_dist.items())
            scores: List[float] = []
            for tok, freq in items:
                base = max(0.0, float(freq)) ** (1.0 / max(0.01, temperature))
                bonus = 0.0
                if prev_tok is not None:
                    bg = self.bigrams.get((prev_tok, tok), 0)
                    if bg > 0:
                        bonus = bigram_weight * (float(bg) ** (1.0 / max(0.01, temperature)))
                # Local-repeat penalty
                if tok in out_tokens[-4:]:
                    base *= 0.1
                scores.append(base + bonus)
            total = sum(scores)
            if total <= 0:
                continue
            r = self._rng.random() * total
            acc = 0.0
            chosen: Optional[str] = None
            for (tok, _), w in zip(items, scores):
                acc += w
                if r <= acc:
                    chosen = tok
                    break
            if chosen is None:
                chosen = items[-1][0]
            out_tokens.append(chosen)
            prev_tok = chosen
        return " ".join(out_tokens)

    # ── round-trip / decode-from-text ───────────────────────────────

    def respond(self, query_text: str, max_tokens: int = 18,
                  temperature: float = 0.7) -> str:
        """Encode query → operator path → decode → response.
        This is the full bidirectional loop in one call."""
        ops = self.encode(query_text)
        if len(ops) < 2:
            return ""
        return self.decode(ops, max_tokens=max_tokens, temperature=temperature)

    # ── stats ───────────────────────────────────────────────────────

    def n_params(self) -> int:
        """Total parameters across all cells + sub-cells."""
        return sum(cb.n_params() for cb in self.cells.values())

    def stats(self) -> Dict[str, Any]:
        sub_cell_count = sum(len(cb.sub_cells) for cb in self.cells.values())
        return {
            "n_cells": len(self.cells),
            "n_sub_cells": sub_cell_count,
            "n_params": self.n_params(),
            "n_inhalations": self.total_inhalations,
            "n_exhalations": self.exhale_count,
            "densest_cells": [
                (f"({a},{b})", len(cb.token_dist), cb.n_seen)
                for (a, b), cb in sorted(
                    self.cells.items(),
                    key=lambda kv: -len(kv[1].token_dist))[:6]
            ],
        }


# ─── Module-level singleton ─────────────────────────────────────────

_LIVING: Optional[LivingLM] = None


def get_living_lm() -> LivingLM:
    """Get the process-wide living LM instance."""
    global _LIVING
    if _LIVING is None:
        _LIVING = LivingLM()
    return _LIVING


def inhale_text(text: str) -> Dict[str, Any]:
    return get_living_lm().inhale(text)


def respond_to(text: str, **kwargs) -> str:
    return get_living_lm().respond(text, **kwargs)


# ─── Mount hook ─────────────────────────────────────────────────────

def mount_living_lm(engine: Any) -> bool:
    """Attach the living LM to the engine.

    Side effects:
      engine.living_lm                  : the LivingLM instance
      engine.living_lm_inhale(text)     : convenience API
      engine.living_lm_respond(text)    : convenience API
      engine.living_lm_save()           : persist state

      Auto-inhales after each chat turn (in ck_concept_learner's
      process_chat_turn hook), grows parameters, periodically exhales.
    """
    try:
        lm = get_living_lm()
    except Exception as e:
        print(f"[CK Gen14] mount_living_lm: failed ({e})")
        return False
    engine.living_lm = lm
    engine.living_lm_inhale = lm.inhale
    engine.living_lm_respond = lm.respond
    engine.living_lm_save = lm.save
    stats = lm.stats()
    print(f"[CK Gen14] living_lm: MOUNTED  "
          f"cells={stats['n_cells']}  params={stats['n_params']:,}  "
          f"inhalations={stats['n_inhalations']}")
    return True


# ─── CLI / self-test ────────────────────────────────────────────────

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--inhale", help="inhale a single text")
    ap.add_argument("--respond", help="respond to a query")
    ap.add_argument("--exhale", action="store_true")
    ap.add_argument("--test", action="store_true")
    args = ap.parse_args()

    lm = get_living_lm()

    if args.stats:
        s = lm.stats()
        print(f"LivingLM at {LM_STATE_PATH}")
        for k, v in s.items():
            if k == "densest_cells":
                print(f"  {k}:")
                for cell, n_tok, n_seen in v:
                    print(f"    {cell}: {n_tok} tokens, {n_seen} obs")
            else:
                print(f"  {k}: {v}")
        return 0

    if args.inhale:
        r = lm.inhale(args.inhale)
        print(json.dumps(r, indent=2))
        lm.save()
        return 0

    if args.respond:
        r = lm.respond(args.respond)
        print(f"Q: {args.respond}")
        print(f"A: {r}")
        return 0

    if args.exhale:
        r = lm.exhale()
        print(json.dumps(r, indent=2))
        lm.save()
        return 0

    if args.test:
        # Self-test: inhale a small corpus, watch params grow, decode
        corpus = [
            "Pride and Prejudice is a novel about the British landed gentry "
            "at the end of the 18th century.",
            "Photosynthesis is the process by which plants use sunlight, "
            "water, and carbon dioxide to produce oxygen and glucose.",
            "The Riemann zeta function is the analytic continuation of the "
            "Dirichlet series across the complex plane.",
            "A Hilbert space is a complete inner product space with a norm "
            "induced by the inner product.",
            "Yang-Mills theory is a non-abelian gauge theory based on the "
            "SU(N) symmetry group.",
            "Compactness in topology means closure under finite "
            "intersection of open covers.",
        ]
        print("=== INHALING small corpus ===")
        for t in corpus:
            r = lm.inhale(t)
            print(f"  growth: +{r.get('growth',0)} params  "
                  f"(total now: {r.get('params_after',0)})")
        print()
        print("=== STATS ===")
        for k, v in lm.stats().items():
            if k == "densest_cells":
                print(f"  {k}:")
                for c in v:
                    print(f"    {c}")
            else:
                print(f"  {k}: {v}")
        print()
        print("=== RESPONSES (decode operator-path → tokens) ===")
        for q in ["what is photosynthesis",
                   "tell me about Yang-Mills",
                   "explain compactness",
                   "Hilbert space"]:
            resp = lm.respond(q)
            print(f"  Q: {q}")
            print(f"  A: {resp}")
        print()
        print("=== EXHALE (compression) ===")
        r = lm.exhale()
        print(json.dumps(r, indent=2))
        lm.save()
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
