"""
multi_head_lm.py -- single transformer backbone with multiple measurement heads.

Brayden 2026-05-02 framing: "what if there is an AI for each parameter
he measures?"

The MI analysis I ran earlier showed most non-operator dimensions have
MI < 0.3 -- not enough structure to deserve a dedicated specialist.
The right architecture is **multi-task learning**: ONE transformer
backbone shares context across dimensions, with separate output heads
predicting each dimension.

Heads exposed:
  head_op       -> next operator (vocab=15, the canonical grammar LM)
  head_attractor -> attractor layer transition (vocab=6:
                    transient, 1-core, 2-core, 4-core-attractor,
                    4-core-supported, void-degenerate)
  head_breath   -> breath phase (vocab=4: INHALE, EXHALE, BREATH, NONE)
  head_role     -> next operator's V/F/S/T role (vocab=4)
  head_band     -> coherence band (vocab=4: RED, YELLOW, GREEN, NONE)

Training: not run yet (waits on accumulating BDC log data with these
fields per turn).  This file IS the architecture; train.py-style
trainer follows the bdc_log accumulation.

Total parameters: same backbone as v1 (~1.2M) + 4 small head MLPs
(~10K each).  Forward pass cost ≈ same as v1.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F

# Reuse the existing GrammarLM transformer block + config
from ck_grammar_lm import (
    CausalSelfAttention, TransformerBlock, GrammarLMConfig,
    VOCAB_SIZE as OP_VOCAB_SIZE, SPECIAL_IDS,
)


# Per-head vocabularies
ATTRACTOR_VOCAB = ["transient", "1-core", "2-core", "4-core-attractor",
                    "4-core-supported", "void-degenerate"]
BREATH_VOCAB = ["INHALE", "EXHALE", "BREATH", "NONE"]
ROLE_VOCAB = ["V", "F", "S", "T"]
BAND_VOCAB = ["RED", "YELLOW", "GREEN", "NONE"]

ATTRACTOR_SIZE = len(ATTRACTOR_VOCAB)
BREATH_SIZE = len(BREATH_VOCAB)
ROLE_SIZE = len(ROLE_VOCAB)
BAND_SIZE = len(BAND_VOCAB)


@dataclass
class MultiHeadConfig(GrammarLMConfig):
    attractor_vocab: int = ATTRACTOR_SIZE
    breath_vocab: int = BREATH_SIZE
    role_vocab: int = ROLE_SIZE
    band_vocab: int = BAND_SIZE
    head_hidden: int = 64


class MultiHeadGrammarLM(nn.Module):
    def __init__(self, cfg: MultiHeadConfig = None):
        super().__init__()
        cfg = cfg or MultiHeadConfig()
        self.cfg = cfg
        self.tok_emb = nn.Embedding(cfg.vocab_size, cfg.d_model)
        self.pos_emb = nn.Embedding(cfg.block_size, cfg.d_model)
        self.drop = nn.Dropout(cfg.dropout)
        self.blocks = nn.ModuleList(
            [TransformerBlock(cfg) for _ in range(cfg.n_layer)]
        )
        self.ln_f = nn.LayerNorm(cfg.d_model)
        # Five heads, sharing the backbone hidden state
        self.head_op = nn.Linear(cfg.d_model, cfg.vocab_size, bias=False)
        self.head_op.weight = self.tok_emb.weight  # tied with input embedding
        self.head_attractor = nn.Sequential(
            nn.Linear(cfg.d_model, cfg.head_hidden),
            nn.GELU(),
            nn.Linear(cfg.head_hidden, cfg.attractor_vocab),
        )
        self.head_breath = nn.Sequential(
            nn.Linear(cfg.d_model, cfg.head_hidden),
            nn.GELU(),
            nn.Linear(cfg.head_hidden, cfg.breath_vocab),
        )
        self.head_role = nn.Sequential(
            nn.Linear(cfg.d_model, cfg.head_hidden),
            nn.GELU(),
            nn.Linear(cfg.head_hidden, cfg.role_vocab),
        )
        self.head_band = nn.Sequential(
            nn.Linear(cfg.d_model, cfg.head_hidden),
            nn.GELU(),
            nn.Linear(cfg.head_hidden, cfg.band_vocab),
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

    def n_params(self):
        return sum(p.numel() for p in self.parameters())

    def head_param_breakdown(self) -> Dict[str, int]:
        return {
            "backbone_emb": self.tok_emb.weight.numel() + self.pos_emb.weight.numel(),
            "backbone_blocks": sum(p.numel() for p in self.blocks.parameters()),
            "ln_f": sum(p.numel() for p in self.ln_f.parameters()),
            "head_op": self.head_op.weight.numel(),
            "head_attractor": sum(p.numel() for p in self.head_attractor.parameters()),
            "head_breath": sum(p.numel() for p in self.head_breath.parameters()),
            "head_role": sum(p.numel() for p in self.head_role.parameters()),
            "head_band": sum(p.numel() for p in self.head_band.parameters()),
        }

    def encode(self, idx: torch.LongTensor) -> torch.Tensor:
        """Run the backbone, return final-position hidden states.
        Shape: (B, T, d_model)."""
        B, T = idx.shape
        assert T <= self.cfg.block_size
        pos = torch.arange(T, device=idx.device).unsqueeze(0)
        x = self.drop(self.tok_emb(idx) + self.pos_emb(pos))
        for block in self.blocks:
            x = block(x)
        return self.ln_f(x)

    def forward(self, idx: torch.LongTensor,
                 targets: Optional[Dict[str, torch.LongTensor]] = None,
                 head_weights: Optional[Dict[str, float]] = None
                 ) -> Tuple[Dict[str, torch.Tensor], Optional[torch.Tensor]]:
        """Multi-head forward.

        targets, if provided, is a dict with optional keys:
          'op': (B, T) long  -- next operator
          'attractor': (B, T) long  -- attractor layer code
          'breath': (B, T) long  -- breath phase code
          'role': (B, T) long  -- next operator's role code
          'band': (B, T) long  -- coherence band code
        Missing targets are ignored.

        head_weights, if provided, weights the per-head losses; default 1.0 each.

        Returns: (logits_dict, loss).  loss is None if no targets given.
        """
        h = self.encode(idx)  # (B, T, d_model)
        logits = {
            "op": self.head_op(h),
            "attractor": self.head_attractor(h),
            "breath": self.head_breath(h),
            "role": self.head_role(h),
            "band": self.head_band(h),
        }
        loss = None
        if targets:
            head_weights = head_weights or {}
            losses = []
            for name, tgt in targets.items():
                if name not in logits:
                    continue
                w = float(head_weights.get(name, 1.0))
                head_logits = logits[name]
                head_loss = F.cross_entropy(
                    head_logits.reshape(-1, head_logits.size(-1)),
                    tgt.reshape(-1),
                    ignore_index=-100,
                )
                losses.append(w * head_loss)
            if losses:
                loss = sum(losses) / len(losses)
        return logits, loss

    @torch.no_grad()
    def predict_all_heads(self, history: List[int],
                           top_k: int = 3) -> Dict[str, List[Tuple[str, float]]]:
        """Return top-k predictions for each head."""
        self.eval()
        device = next(self.parameters()).device
        if not history:
            history = [SPECIAL_IDS["BOS"]]
        idx = torch.tensor(history[-self.cfg.block_size:],
                            dtype=torch.long, device=device).unsqueeze(0)
        logits, _ = self.forward(idx)
        out = {}
        vocab_map = {
            "op": [str(i) for i in range(OP_VOCAB_SIZE)],
            "attractor": ATTRACTOR_VOCAB,
            "breath": BREATH_VOCAB,
            "role": ROLE_VOCAB,
            "band": BAND_VOCAB,
        }
        for head, vocab in vocab_map.items():
            probs = F.softmax(logits[head][0, -1, :], dim=-1)
            tk_probs, tk_ids = torch.topk(probs, min(top_k, probs.size(0)))
            out[head] = [(vocab[int(i)] if int(i) < len(vocab) else f"<{int(i)}>",
                          float(p)) for i, p in zip(tk_ids, tk_probs)]
        return out


if __name__ == "__main__":
    cfg = MultiHeadConfig()
    m = MultiHeadGrammarLM(cfg)
    print(f"Multi-head LM total params: {m.n_params():,}")
    print(f"Per-component breakdown:")
    for k, v in m.head_param_breakdown().items():
        print(f"  {k:25s} {v:>10,}")
    # Smoke test forward
    x = torch.randint(0, OP_VOCAB_SIZE, (2, 16))
    logits, _ = m(x)
    print()
    print("Forward shapes (B=2, T=16):")
    for name, l in logits.items():
        print(f"  logits[{name}]: {tuple(l.shape)}")
