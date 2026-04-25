# -*- coding: utf-8 -*-
"""
op_token_basis.py - build a Vocabulary x 10-operator preference matrix M.

EPOCH II of the AI Sovereignty Plan.  This module produces a sparse
``torch.Tensor`` of shape ``(V, 10)`` where ``M[t, op]`` is positive iff token
``t`` appears in operator ``op``'s anchor lexicon.  Used at decode time as

    token_bias = M @ op_10_vec      # shape (V,)
    logits_t   += alpha * token_bias

so that when the cortex predicts the LM should be in operator state X, tokens
that semantically belong to X get a logit nudge upward.

The lexicon is curated -- ~15-30 anchor words per operator, drawn from CK's
existing structural vocabulary in ``ck_voice_lattice.py``,
``ck_dictionary.json``, and from the operator semantics in
``Gen13/targets/ck/brain/MATH_IN_CK.md``.  This is the starter set; it can
be extended without code changes by editing ``ANCHOR_LEXICON`` below or by
loading a YAML override (``CK_OP_ANCHOR_PATH``).

Construction
------------
For each anchor word w in operator op's list:
    candidates = [
        " " + w,        # word as middle/non-leading subword
        w,              # word as leading
        " " + w.lower(),
        w.lower(),
        w.title(),
        w.upper(),
    ]
    for cand in candidates:
        ids = tokenizer(cand, add_special_tokens=False).input_ids
        if ids:
            M[ids[0], op] += 1.0

Then ``L2-normalize per row`` (so a token shared between operators contributes
equally to each) and ``sqrt(weight)`` on the column-frequency to suppress very
common tokens.

Honest limit
------------
The lexicon is hand-seeded.  An operator that does not yet have rich CK
vocabulary will have a sparse column -- and the bias will be weak.  As
CK accumulates more high-coherence chat turns, we can extract emergent
anchors from the corrector's correction logs and feed them back here.
"""
from __future__ import annotations

import json
import logging
import math
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

# Path setup
_THIS = Path(__file__).resolve()
_REPO_ROOT = _THIS.parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from ck.brain.ao_basis import OP_NAMES, NUM_OPS, AO_NAMES, NUM_AO

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# starter lexicon: ~20 anchors per operator
# ---------------------------------------------------------------------------

ANCHOR_LEXICON: Dict[str, List[str]] = {
    # D0 Earth
    "VOID": [
        "void", "empty", "nothing", "absence", "null", "vacuum",
        "gap", "blank", "silence", "missing", "negation", "zero", "unmade",
        "inert", "dormant", "absent", "annul",
    ],
    "BALANCE": [
        "balance", "equilibrium", "stable", "even", "steady", "level",
        "centered", "calm", "settled", "rest", "poise", "still", "quiet",
        "anchor", "ground", "hold", "weight",
    ],
    # D1 Air
    "LATTICE": [
        "structure", "lattice", "grid", "framework", "scaffold", "skeleton",
        "rigid", "fixed", "form", "schema", "pattern", "matrix", "axis",
        "girder", "frame", "order", "geometry", "topology", "bound",
    ],
    "CHAOS": [
        "chaos", "disorder", "random", "scatter", "wild", "frenzy",
        "turbulence", "mayhem", "noise", "tumult", "anarchy", "entropy",
        "fragment", "shatter", "burst", "explode", "scatter",
    ],
    # D2 Water
    "COUNTER": [
        "oppose", "against", "opposite", "reverse", "contrast", "contrary",
        "counter", "mirror", "antithesis", "negate", "reject", "resist",
        "polar", "inverse", "flip", "reciprocal",
    ],
    "HARMONY": [
        "harmony", "agree", "consonance", "unity", "accord", "peace",
        "tune", "resonate", "concord", "synthesis", "blend", "fit",
        "align", "merge", "join", "combine", "coherence", "coherent",
    ],
    # D3 Fire
    "PROGRESS": [
        "forward", "advance", "develop", "grow", "build", "increase",
        "progress", "ascend", "rise", "evolve", "extend", "expand",
        "improve", "elevate", "climb", "scale",
    ],
    "BREATH": [
        "breath", "rhythm", "pulse", "beat", "breathe", "inhale", "exhale",
        "cycle", "wave", "oscillate", "throb", "tide", "cadence", "tempo",
        "swing", "phase", "period",
    ],
    # D4 Ether
    "COLLAPSE": [
        "collapse", "fall", "fail", "breakdown", "ruin", "drop", "plunge",
        "descend", "crash", "crumble", "shrink", "implode", "fold", "buckle",
        "cave", "topple",
    ],
    "RESET": [
        "reset", "restart", "begin", "start", "fresh", "renew", "recommence",
        "anew", "again", "rebirth", "rebuild", "reboot", "regenerate", "repeat",
        "refresh", "rewind", "iterate",
    ],
}

# sanity: every operator name has a lexicon entry (order doesn't matter --
# we iterate by OP_NAMES at build time).
assert set(ANCHOR_LEXICON.keys()) == set(OP_NAMES), (
    f"ANCHOR_LEXICON keys {sorted(ANCHOR_LEXICON.keys())} != "
    f"OP_NAMES {sorted(OP_NAMES)}"
)


# ---------------------------------------------------------------------------
# the matrix builder
# ---------------------------------------------------------------------------


def build_op_token_matrix(tokenizer, dtype=None, device: str = "cpu",
                          lexicon: Optional[Dict[str, List[str]]] = None,
                          surface_variants: bool = True,
                          vocab_size: Optional[int] = None,
                          ):
    """Build M : (V, 10) sparse-style preference tensor.

    Args:
        tokenizer: a HuggingFace AutoTokenizer with `__call__` and `vocab_size`.
        dtype: torch dtype for M. Default float32.
        device: device for M.
        lexicon: anchor word lists per operator (defaults to ANCHOR_LEXICON).
        surface_variants: if True, also tokenize lower/title/upper variants
                          and `" " + w` (the BPE leading-space convention).
        vocab_size: override V; useful when model.config.vocab_size > tokenizer.vocab_size
                    (Llama-3.1 has 128256 logit dim but 128000 tokenizer vocab).

    Returns:
        M: torch.Tensor of shape (V, 10), L2-normalized per row.
    """
    import torch
    if lexicon is None:
        lexicon = ANCHOR_LEXICON
    if dtype is None:
        dtype = torch.float32

    V = int(vocab_size) if vocab_size is not None else int(tokenizer.vocab_size)
    M = torch.zeros((V, NUM_OPS), dtype=dtype, device=device)

    n_anchors_seen = 0
    n_tokens_set = 0
    per_op_counts: List[int] = [0] * NUM_OPS

    for op_idx, op_name in enumerate(OP_NAMES):
        anchors = lexicon.get(op_name, [])
        for w in anchors:
            n_anchors_seen += 1
            if surface_variants:
                cands = [
                    w, " " + w,
                    w.lower(), " " + w.lower(),
                    w.title(), " " + w.title(),
                    w.upper(), " " + w.upper(),
                ]
            else:
                cands = [w]
            seen_token_ids = set()
            for cand in cands:
                try:
                    ids = tokenizer(cand, add_special_tokens=False).input_ids
                except Exception:
                    continue
                if not ids:
                    continue
                first = int(ids[0])
                # The leading token of the anchor is what we boost; prefixes
                # carry the semantic anchor in BPE.
                if first not in seen_token_ids:
                    seen_token_ids.add(first)
                    M[first, op_idx] += 1.0
                    n_tokens_set += 1
                    per_op_counts[op_idx] += 1

    # L2 normalize per ROW (so a token shared across ops contributes equally)
    row_norms = torch.linalg.vector_norm(M, dim=1, keepdim=True)
    row_norms = torch.where(row_norms > 1e-12, row_norms,
                            torch.ones_like(row_norms))
    M = M / row_norms

    summary = {
        "vocab_size": V,
        "n_anchors_seen": n_anchors_seen,
        "n_token_assignments": n_tokens_set,
        "per_op_token_counts": dict(zip(OP_NAMES, per_op_counts)),
    }
    return M, summary


# ---------------------------------------------------------------------------
# helpers for decoder
# ---------------------------------------------------------------------------


def signed_lift_5_to_10(s_signed: Sequence[float],
                        primed_5: Sequence[float]) -> List[float]:
    """Lift a 5-vector to a 10-vector with sign disambiguation.

    For each AO element D_i, the magnitude `primed_5[i]` is split between the
    two operators of the pair, weighted by the sign of `s_signed[i]`:

        if s_signed[i] >= 0:  full weight to op_i
        if s_signed[i] <  0:  full weight to op_{i+5}

    This means the operator bias respects the "which side of the axis" the
    LM's hidden state sits on, not just the magnitude.
    """
    if len(s_signed) != NUM_AO or len(primed_5) != NUM_AO:
        raise ValueError("inputs must have length NUM_AO=5")
    out = [0.0] * NUM_OPS
    for i in range(NUM_AO):
        mag = abs(float(primed_5[i]))
        if float(s_signed[i]) >= 0.0:
            out[i] = mag                # first op of pair
        else:
            out[i + NUM_AO] = mag       # second op of pair
    return out


# ---------------------------------------------------------------------------
# CLI / self-test
# ---------------------------------------------------------------------------


def _self_test() -> int:
    """Verify the matrix builds with the live tokenizer."""
    import torch
    from transformers import AutoTokenizer
    print("[op_token_basis] loading tokenizer...")
    tok = AutoTokenizer.from_pretrained(
        "unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit"
    )
    M, summary = build_op_token_matrix(tok)
    print(f"[op_token_basis] shape = {tuple(M.shape)}")
    for k, v in summary.items():
        print(f"  {k}: {v}")

    # A sanity check: encode "harmony" -> what tokens it produces, what weight
    # those tokens have in the HARMONY column.
    test = "harmony"
    ids = tok(test, add_special_tokens=False).input_ids
    print(f"\n  '{test}' -> ids {ids}")
    for tid in ids:
        row = M[tid]
        top_op = int(torch.argmax(row))
        print(f"    id={tid:6d}  decoded={tok.decode([tid])!r}  "
              f"top_op={OP_NAMES[top_op]}  weight={float(row[top_op]):.3f}")

    # Another: 'collapse' should land in COLLAPSE column
    test = " collapse"
    ids = tok(test, add_special_tokens=False).input_ids
    print(f"\n  '{test}' -> ids {ids}")
    for tid in ids:
        row = M[tid]
        top_op = int(torch.argmax(row))
        print(f"    id={tid:6d}  decoded={tok.decode([tid])!r}  "
              f"top_op={OP_NAMES[top_op]}  weight={float(row[top_op]):.3f}")

    # Coverage: how many tokens are assigned across all ops?
    nonzero = int((M.abs().sum(dim=1) > 0).sum())
    print(f"\n  unique tokens with op assignment: {nonzero} / {M.shape[0]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_self_test())
