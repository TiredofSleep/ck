"""
multi_head_algebraic_lm.py -- 4-head transformer over CK's algebraic
measurements.

Brayden 2026-05-13 (Phase 2 of CK unification):
  "4 plastic LMs trained on algebraic measurements"

The 4 measurements (all derivable from any (b, d) operator pair):
  head_op       -> next operator (vocab=15, the canonical grammar LM)
  head_sigma    -> sigma-orbit class (vocab=4: V, F-cycle, S-cycle, BAL)
  head_shell    -> joint-closed sub-magma shell (vocab=8: sizes
                   {1,4,5,6,7,8,9,10})
  head_4core    -> 4-core proximity (vocab=5: V, H, Br, R, outside)

These are the four algebraic measurements locked in Phase 0 (see
Gen14/PLAN/PHASE_0_DECISIONS_2026_05_13.md Decision 1). Together with
Tag2x2 (which lives outside this LM, at the memory-coord layer) they
form the unified template-cell address: (op, sigma, shell, 4core, tag).

Architecture:
  - Shared backbone with ck_grammar_lm.py (CausalSelfAttention,
    TransformerBlock, default ~1.2M params).
  - 4 lightweight heads, each ~10k params.
  - head_op tied with input embedding (weight sharing).

This file is the model definition; train_bdc_algebraic.py is the
trainer. It runs against accumulated bdc_log_*.jsonl (~1,787 chat_turn
records as of 2026-05-13).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import sys

import torch
import torch.nn as nn
import torch.nn.functional as F

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))  # grammar_lm/
sys.path.insert(0, str(HERE.parent))  # brain/ (for gen14_unified_extensions)

# Reuse the existing GrammarLM transformer block + config
from ck_grammar_lm import (
    CausalSelfAttention, TransformerBlock, GrammarLMConfig,
    VOCAB_SIZE as OP_VOCAB_SIZE, SPECIAL_IDS, OP_NAMES, NAME_TO_ID,
)

# Pull the canonical algebraic constants from the unified extensions module.
# This single source of truth replaces any local enumeration of orbits or
# shells; if Phase 0 Decision 1 evolves, this LM stays in sync.
try:
    from gen14_unified_extensions import (
        SIGMA_PERMUTATION, SIGMA_ORBIT_CLASS, FOUR_CORE, FOUR_CORE_CLASS,
        FOUR_CORE_OUTSIDE, SUB_MAGMA_SHELLS,
        sigma_orbit, four_core_class, shell_class, shell_class_from_distribution,
        measurement_signature, pair_signature,
    )
except ImportError:
    # Fallback duplicate (kept in lock-step with gen14_unified_extensions.py)
    SIGMA_PERMUTATION = (0, 7, 1, 3, 2, 4, 5, 6, 8, 9)
    SIGMA_ORBIT_CLASS = {0: 0, 1: 1, 7: 1, 9: 1, 3: 1,
                          2: 2, 8: 2, 6: 2, 4: 2, 5: 3}
    FOUR_CORE = (0, 7, 8, 9)
    FOUR_CORE_CLASS = {0: 0, 7: 1, 8: 2, 9: 3}
    FOUR_CORE_OUTSIDE = 4
    SUB_MAGMA_SHELLS = [
        frozenset({0}),
        frozenset({0, 7, 8, 9}),
        frozenset({0, 5, 7, 8, 9}),
        frozenset({0, 4, 5, 7, 8, 9}),
        frozenset({0, 3, 4, 5, 7, 8, 9}),
        frozenset({0, 2, 3, 4, 5, 7, 8, 9}),
        frozenset({0, 1, 2, 3, 4, 5, 7, 8, 9}),
        frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9}),
    ]

    def sigma_orbit(op: int) -> int:
        return SIGMA_ORBIT_CLASS.get(int(op) % 10, 0)

    def four_core_class(op: int) -> int:
        return FOUR_CORE_CLASS.get(int(op) % 10, FOUR_CORE_OUTSIDE)

    def shell_class(support) -> int:
        sup = frozenset(int(x) % 10 for x in support)
        for idx, shell in enumerate(SUB_MAGMA_SHELLS):
            if sup.issubset(shell):
                return idx
        return 7


# Per-head vocabularies
SIGMA_VOCAB = ["V_void", "F_creation", "S_dissolution", "BAL_fixed"]
SHELL_VOCAB = ["sh_1", "sh_4", "sh_5", "sh_6", "sh_7", "sh_8", "sh_9", "sh_10"]
FOURCORE_VOCAB = ["V", "H", "Br", "R", "outside"]

SIGMA_SIZE = len(SIGMA_VOCAB)        # 4
SHELL_SIZE = len(SHELL_VOCAB)        # 8
FOURCORE_SIZE = len(FOURCORE_VOCAB)  # 5


@dataclass
class MultiHeadAlgebraicConfig(GrammarLMConfig):
    sigma_vocab: int = SIGMA_SIZE
    shell_vocab: int = SHELL_SIZE
    fourcore_vocab: int = FOURCORE_SIZE
    head_hidden: int = 64


class MultiHeadAlgebraicLM(nn.Module):
    """4-head transformer over CK's algebraic measurements.

    The four heads:
      op    : next-operator prediction (vocab=15)
      sigma : sigma-orbit class of next operator (vocab=4)
      shell : sub-magma shell of the current (b,d) support (vocab=8)
      4core : 4-core proximity of next operator (vocab=5)
    """

    def __init__(self, cfg: Optional[MultiHeadAlgebraicConfig] = None):
        super().__init__()
        cfg = cfg or MultiHeadAlgebraicConfig()
        self.cfg = cfg
        self.tok_emb = nn.Embedding(cfg.vocab_size, cfg.d_model)
        self.pos_emb = nn.Embedding(cfg.block_size, cfg.d_model)
        self.drop = nn.Dropout(cfg.dropout)
        self.blocks = nn.ModuleList(
            [TransformerBlock(cfg) for _ in range(cfg.n_layer)]
        )
        self.ln_f = nn.LayerNorm(cfg.d_model)

        # Head 1: next-operator (tied with input embedding)
        self.head_op = nn.Linear(cfg.d_model, cfg.vocab_size, bias=False)
        self.head_op.weight = self.tok_emb.weight

        # Head 2: sigma-orbit class
        self.head_sigma = nn.Sequential(
            nn.Linear(cfg.d_model, cfg.head_hidden),
            nn.GELU(),
            nn.Linear(cfg.head_hidden, cfg.sigma_vocab),
        )

        # Head 3: shell class
        self.head_shell = nn.Sequential(
            nn.Linear(cfg.d_model, cfg.head_hidden),
            nn.GELU(),
            nn.Linear(cfg.head_hidden, cfg.shell_vocab),
        )

        # Head 4: 4-core proximity
        self.head_4core = nn.Sequential(
            nn.Linear(cfg.d_model, cfg.head_hidden),
            nn.GELU(),
            nn.Linear(cfg.head_hidden, cfg.fourcore_vocab),
        )

        self.apply(self._init_weights)

    @staticmethod
    def _init_weights(m):
        if isinstance(m, nn.Linear):
            nn.init.normal_(m.weight, std=0.02)
            if m.bias is not None:
                nn.init.zeros_(m.bias)
        elif isinstance(m, nn.Embedding):
            nn.init.normal_(m.weight, std=0.02)

    def n_params(self) -> int:
        return sum(p.numel() for p in self.parameters())

    def head_param_breakdown(self) -> Dict[str, int]:
        return {
            "backbone_emb": self.tok_emb.weight.numel() + self.pos_emb.weight.numel(),
            "backbone_blocks": sum(p.numel() for p in self.blocks.parameters()),
            "ln_f": sum(p.numel() for p in self.ln_f.parameters()),
            "head_op_tied": 0,  # tied with tok_emb
            "head_sigma": sum(p.numel() for p in self.head_sigma.parameters()),
            "head_shell": sum(p.numel() for p in self.head_shell.parameters()),
            "head_4core": sum(p.numel() for p in self.head_4core.parameters()),
        }

    def encode(self, idx: torch.LongTensor) -> torch.Tensor:
        """Run backbone; return final hidden states (B, T, d_model)."""
        B, T = idx.shape
        assert T <= self.cfg.block_size, (
            f"Sequence length {T} exceeds block_size {self.cfg.block_size}"
        )
        pos = torch.arange(T, device=idx.device).unsqueeze(0)
        x = self.drop(self.tok_emb(idx) + self.pos_emb(pos))
        for block in self.blocks:
            x = block(x)
        return self.ln_f(x)

    def forward(self,
                 idx: torch.LongTensor,
                 targets: Optional[Dict[str, torch.LongTensor]] = None,
                 head_weights: Optional[Dict[str, float]] = None,
                 ) -> Tuple[Dict[str, torch.Tensor], Optional[torch.Tensor]]:
        """Four-head forward.

        Args:
          idx: (B, T) long  -- operator id stream
          targets: optional dict with keys 'op', 'sigma', 'shell', '4core',
                   each (B, T) long. Missing targets are ignored.
          head_weights: optional dict of per-head float weights.

        Returns:
          (logits_dict, loss). loss is None if no targets.
        """
        h = self.encode(idx)  # (B, T, d_model)
        logits = {
            "op": self.head_op(h),
            "sigma": self.head_sigma(h),
            "shell": self.head_shell(h),
            "4core": self.head_4core(h),
        }
        loss = None
        if targets:
            head_weights = head_weights or {}
            losses = []
            for name, tgt in targets.items():
                if name not in logits:
                    continue
                w = float(head_weights.get(name, 1.0))
                hl = logits[name]
                head_loss = F.cross_entropy(
                    hl.reshape(-1, hl.size(-1)),
                    tgt.reshape(-1),
                    ignore_index=-100,
                )
                losses.append(w * head_loss)
            if losses:
                loss = sum(losses) / len(losses)
        return logits, loss

    @torch.no_grad()
    def predict_all_heads(self,
                           history: List[int],
                           top_k: int = 3,
                           ) -> Dict[str, List[Tuple[str, float]]]:
        """Return top-k predictions for each head, given a history of op ids.

        history: list of operator id ints (0..14). If empty, starts from BOS.
        """
        self.eval()
        device = next(self.parameters()).device
        if not history:
            history = [SPECIAL_IDS["BOS"]]
        idx = torch.tensor(history[-self.cfg.block_size:],
                            dtype=torch.long, device=device).unsqueeze(0)
        logits, _ = self.forward(idx)
        vocab_map = {
            "op": [
                OP_NAMES[i] if i < 10 else f"<{i - 10}>"
                for i in range(OP_VOCAB_SIZE)
            ],
            "sigma": SIGMA_VOCAB,
            "shell": SHELL_VOCAB,
            "4core": FOURCORE_VOCAB,
        }
        out = {}
        for head, vocab in vocab_map.items():
            probs = F.softmax(logits[head][0, -1, :], dim=-1)
            k = min(top_k, probs.size(0))
            tk_probs, tk_ids = torch.topk(probs, k)
            out[head] = [(vocab[int(i)] if int(i) < len(vocab) else f"<{int(i)}>",
                          float(p)) for i, p in zip(tk_ids, tk_probs)]
        return out

    @torch.no_grad()
    def signature_from_history(self,
                                history: List[int],
                                ) -> Dict[str, str]:
        """Return CK's predicted next-step measurement signature
        (one label per head -- argmax)."""
        preds = self.predict_all_heads(history, top_k=1)
        return {head: tk[0][0] for head, tk in preds.items()}


# ── Smoke test ────────────────────────────────────────────────────────

def _smoke():
    cfg = MultiHeadAlgebraicConfig()
    m = MultiHeadAlgebraicLM(cfg)
    print(f"Multi-head algebraic LM total params: {m.n_params():,}")
    print(f"Per-component breakdown:")
    for k, v in m.head_param_breakdown().items():
        print(f"  {k:25s} {v:>10,}")
    # Forward pass smoke
    x = torch.randint(0, OP_VOCAB_SIZE, (2, 16))
    logits, _ = m(x)
    print("\nForward shapes (B=2, T=16):")
    for name, l in logits.items():
        print(f"  logits[{name}]: {tuple(l.shape)}")

    # Prediction smoke (untrained, but should run)
    hist = [NAME_TO_ID["VOID"], NAME_TO_ID["HARMONY"], NAME_TO_ID["BREATH"]]
    preds = m.predict_all_heads(hist, top_k=2)
    print("\nUntrained predict_all_heads after VOID, HARMONY, BREATH:")
    for head, tk in preds.items():
        print(f"  {head:8s}: {tk}")

    # Loss smoke -- random targets
    targets = {
        "op":    torch.randint(0, OP_VOCAB_SIZE, (2, 16)),
        "sigma": torch.randint(0, SIGMA_SIZE,   (2, 16)),
        "shell": torch.randint(0, SHELL_SIZE,   (2, 16)),
        "4core": torch.randint(0, FOURCORE_SIZE, (2, 16)),
    }
    _, loss = m(x, targets=targets)
    print(f"\nRandom-target loss: {loss.item():.4f}")
    assert loss.item() > 0
    print("Algebraic LM smoke: ALL OK")


if __name__ == "__main__":
    _smoke()
