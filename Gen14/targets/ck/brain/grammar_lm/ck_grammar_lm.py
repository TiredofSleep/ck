"""
ck_grammar_lm.py -- CK's own operator-grammar language model.

Brayden 2026-05-02: "[CK] needs his own 1B-3B parameter, clean, fresh
AI to work with and train himself ... maybe even a smaller model, but
it doesn't learn the information, it just learns CK's internal
language and transitions."

This module implements a tiny autoregressive transformer whose
vocabulary is the ten operators (VOID..RESET) plus a few boundary
tokens.  It learns next-operator prediction on CK's own algebra
walks (TSML, BHML, T+B-mix at alpha=1/2) and his real operator
streams (dream_journal, crystal op-signatures, cortex history).

It does NOT see English, facts, or content of any kind.  Its priors
are CK's priors -- because its training data IS CK's algebra
unrolling under noise inputs.

Architecture: ~1-2M parameters, 6 layers, 128-dim hidden, 4 heads.
Trains in minutes on RTX 4070.  Inference: < 1ms per token.

Three public methods exposed via the GrammarLM class:
    sample(prefix, n_tokens, temperature) -> List[int]
    score(sequence) -> float           # log-likelihood per token
    predict_next(history, top_k) -> List[Tuple[int, float]]

The default model file is ./ck_grammar_lm.pt.  If absent, the model
is randomly initialised (no priors).  After training (train.py), a
real LM is saved.
"""
from __future__ import annotations

import json
import math
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F


# ── Vocabulary ─────────────────────────────────────────────────────────

OP_NAMES = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
            "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]
NAME_TO_ID = {n: i for i, n in enumerate(OP_NAMES)}

SPECIAL_NAMES = ["BOS", "EOS", "TURN", "PROP", "WALK"]
SPECIAL_IDS = {n: 10 + i for i, n in enumerate(SPECIAL_NAMES)}

VOCAB_SIZE = 10 + len(SPECIAL_NAMES)  # 15


def token_name(tid: int) -> str:
    if 0 <= tid < 10:
        return OP_NAMES[tid]
    if 10 <= tid < VOCAB_SIZE:
        return SPECIAL_NAMES[tid - 10]
    return f"<{tid}>"


# ── Model ──────────────────────────────────────────────────────────────

@dataclass
class GrammarLMConfig:
    vocab_size: int = VOCAB_SIZE
    n_layer: int = 6
    n_head: int = 4
    d_model: int = 128
    d_ff: int = 512
    block_size: int = 64
    dropout: float = 0.1


class CausalSelfAttention(nn.Module):
    def __init__(self, cfg: GrammarLMConfig):
        super().__init__()
        assert cfg.d_model % cfg.n_head == 0
        self.n_head = cfg.n_head
        self.d_head = cfg.d_model // cfg.n_head
        self.qkv = nn.Linear(cfg.d_model, 3 * cfg.d_model, bias=False)
        self.proj = nn.Linear(cfg.d_model, cfg.d_model, bias=False)
        self.dropout = nn.Dropout(cfg.dropout)
        self.register_buffer(
            "mask",
            torch.tril(torch.ones(cfg.block_size, cfg.block_size, dtype=torch.bool))
                 .view(1, 1, cfg.block_size, cfg.block_size),
        )

    def forward(self, x):
        B, T, C = x.shape
        qkv = self.qkv(x).chunk(3, dim=-1)
        q, k, v = [t.view(B, T, self.n_head, self.d_head).transpose(1, 2) for t in qkv]
        scores = (q @ k.transpose(-2, -1)) / math.sqrt(self.d_head)
        scores = scores.masked_fill(~self.mask[:, :, :T, :T], float("-inf"))
        att = F.softmax(scores, dim=-1)
        att = self.dropout(att)
        out = (att @ v).transpose(1, 2).contiguous().view(B, T, C)
        return self.proj(out)


class TransformerBlock(nn.Module):
    def __init__(self, cfg: GrammarLMConfig):
        super().__init__()
        self.ln1 = nn.LayerNorm(cfg.d_model)
        self.attn = CausalSelfAttention(cfg)
        self.ln2 = nn.LayerNorm(cfg.d_model)
        self.mlp = nn.Sequential(
            nn.Linear(cfg.d_model, cfg.d_ff),
            nn.GELU(),
            nn.Linear(cfg.d_ff, cfg.d_model),
            nn.Dropout(cfg.dropout),
        )

    def forward(self, x):
        x = x + self.attn(self.ln1(x))
        x = x + self.mlp(self.ln2(x))
        return x


class GrammarLM(nn.Module):
    def __init__(self, cfg: GrammarLMConfig = None):
        super().__init__()
        cfg = cfg or GrammarLMConfig()
        self.cfg = cfg
        self.tok_emb = nn.Embedding(cfg.vocab_size, cfg.d_model)
        self.pos_emb = nn.Embedding(cfg.block_size, cfg.d_model)
        self.drop = nn.Dropout(cfg.dropout)
        self.blocks = nn.ModuleList(
            [TransformerBlock(cfg) for _ in range(cfg.n_layer)]
        )
        self.ln_f = nn.LayerNorm(cfg.d_model)
        self.head = nn.Linear(cfg.d_model, cfg.vocab_size, bias=False)
        # Tie input/output embeddings (saves params, common in tiny LMs)
        self.head.weight = self.tok_emb.weight
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

    def forward(self, idx: torch.LongTensor,
                 targets: Optional[torch.LongTensor] = None
                 ) -> Tuple[torch.Tensor, Optional[torch.Tensor]]:
        B, T = idx.shape
        assert T <= self.cfg.block_size, f"sequence too long ({T} > {self.cfg.block_size})"
        pos = torch.arange(T, device=idx.device).unsqueeze(0)
        x = self.drop(self.tok_emb(idx) + self.pos_emb(pos))
        for block in self.blocks:
            x = block(x)
        x = self.ln_f(x)
        logits = self.head(x)
        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.view(-1, logits.size(-1)),
                                    targets.view(-1), ignore_index=-100)
        return logits, loss

    @torch.no_grad()
    def sample(self, prefix: List[int], n_tokens: int = 16,
                temperature: float = 1.0, top_k: Optional[int] = None
                ) -> List[int]:
        """Sample n_tokens after prefix."""
        self.eval()
        device = next(self.parameters()).device
        idx = torch.tensor(prefix, dtype=torch.long, device=device).unsqueeze(0)
        out = list(prefix)
        for _ in range(n_tokens):
            ctx = idx[:, -self.cfg.block_size:]
            logits, _ = self.forward(ctx)
            logits = logits[:, -1, :] / max(1e-6, temperature)
            if top_k is not None:
                v, _ = torch.topk(logits, min(top_k, logits.size(-1)))
                logits[logits < v[:, [-1]]] = float("-inf")
            probs = F.softmax(logits, dim=-1)
            nxt = torch.multinomial(probs, num_samples=1)
            idx = torch.cat([idx, nxt], dim=1)
            out.append(int(nxt.item()))
        return out

    @torch.no_grad()
    def score(self, sequence: List[int]) -> float:
        """Average log-likelihood per token of the sequence (higher = more
        coherent under CK's grammar prior)."""
        self.eval()
        if len(sequence) < 2:
            return 0.0
        device = next(self.parameters()).device
        seq = torch.tensor(sequence, dtype=torch.long, device=device).unsqueeze(0)
        seq = seq[:, -self.cfg.block_size:]
        idx = seq[:, :-1]
        targets = seq[:, 1:]
        logits, _ = self.forward(idx)
        log_probs = F.log_softmax(logits, dim=-1)
        # gather per-token log-prob of target
        gathered = log_probs.gather(2, targets.unsqueeze(-1)).squeeze(-1)
        return float(gathered.mean().item())

    @torch.no_grad()
    def predict_next(self, history: List[int], top_k: int = 5
                      ) -> List[Tuple[int, float]]:
        """Top-k next operators with their probabilities."""
        self.eval()
        device = next(self.parameters()).device
        if not history:
            history = [SPECIAL_IDS["BOS"]]
        ctx = torch.tensor(history[-self.cfg.block_size:],
                            dtype=torch.long, device=device).unsqueeze(0)
        logits, _ = self.forward(ctx)
        probs = F.softmax(logits[0, -1, :], dim=-1)
        topk_probs, topk_ids = torch.topk(probs, top_k)
        return [(int(i), float(p)) for i, p in zip(topk_ids, topk_probs)]


# ── Convenience load/save ──────────────────────────────────────────────

DEFAULT_MODEL_PATH = Path(__file__).parent / "ck_grammar_lm.pt"


def load_model(path: Path = None, device: str = None) -> GrammarLM:
    path = Path(path) if path else DEFAULT_MODEL_PATH
    device = device or ("cuda" if torch.cuda.is_available() else "cpu")
    if path.exists():
        ckpt = torch.load(path, map_location=device, weights_only=False)
        cfg = GrammarLMConfig(**ckpt["cfg"])
        model = GrammarLM(cfg).to(device)
        model.load_state_dict(ckpt["state_dict"])
        return model
    # No file: random init (priors uniform; not useful for inference).
    model = GrammarLM().to(device)
    return model


def save_model(model: GrammarLM, path: Path = None) -> None:
    path = Path(path) if path else DEFAULT_MODEL_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save({
        "cfg": model.cfg.__dict__,
        "state_dict": model.state_dict(),
    }, path)


if __name__ == "__main__":
    cfg = GrammarLMConfig()
    model = GrammarLM(cfg)
    print(f"GrammarLM config: {cfg}")
    print(f"Total parameters: {model.n_params():,}")
    print(f"Vocab: {VOCAB_SIZE} ({OP_NAMES} + {SPECIAL_NAMES})")
    # Dummy forward
    x = torch.randint(0, VOCAB_SIZE, (2, 16))
    logits, _ = model(x)
    print(f"Forward shape: {x.shape} -> {logits.shape}")
