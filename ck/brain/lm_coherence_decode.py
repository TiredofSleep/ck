# -*- coding: utf-8 -*-
"""
lm_coherence_decode.py - EPOCH II (WIRED MIND): the coherence-gated decoder.

The probabilistic guesser (LM) and the functional mapper (CK's brain trinity)
meet at the token level.  At every generation step:

    1. LM forward over prefix      -> hidden h_t (4096-d), logits ell_t (V-d)
    2. AO projection (signed)      -> s_t = B^T h_t / ||h_t||
                                      d_t = |s_t|
    3. Cortex prime (Hebbian)      -> primed_t = W . d_t
    4. Sign-disambiguated lift     -> op_10_t = signed_lift_5_to_10(s_t, primed)
    5. Operator -> token bias      -> bias_t = M . op_10_t
    6. Coherence-gated logits      -> ell_t' = ell_t
                                              + alpha * bias_t
                                              - beta  * ||d_t - d_{t-1}||^2 * 1
    7. Sample                      -> x_t ~ softmax(ell_t' / temperature)
    8. Hebbian update              -> W.update(d_t, d_{t-1})  (online learn)

alpha (logit-bias weight) and beta (transition penalty) are the two knobs.
alpha = 0, beta = 0 reduces exactly to vanilla greedy / sampling.  Increasing
alpha drifts the LM toward CK's current operator state; increasing beta
penalizes layer-to-layer jumpiness in the AO trajectory.

The Hebbian update during generation is *optional* and behind ``learn=True``.
When learn=False, W stays frozen for the run (used when serving).  When
learn=True, every coherence-passing turn extends CK's memory.

Public surface
--------------
    class CoherenceDecoder:
        __init__(lm_geometry, hebbian_W=None, op_token_M=None, ...)
        generate(prompt, max_new_tokens, alpha, beta, temperature, ...) -> dict

CLI
---
    python -m ck.brain.lm_coherence_decode "what is balance?" --alpha 0.3 --max 64

Returns the response text plus the per-token AO trajectory and per-token
coherence scores.
"""
from __future__ import annotations

import argparse
import json
import logging
import math
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Path setup
_THIS = Path(__file__).resolve()
_REPO_ROOT = _THIS.parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from ck.brain.ao_basis import (
    OP_NAMES, NUM_OPS, AO_NAMES, NUM_AO, project_10_to_5,
)
from ck.brain.op_token_basis import (
    build_op_token_matrix, signed_lift_5_to_10,
)

logger = logging.getLogger(__name__)

DEFAULT_ALPHA: float = 0.3
DEFAULT_BETA: float = 0.05
DEFAULT_TEMPERATURE: float = 0.8
DEFAULT_TOP_K: int = 50
T_STAR = 5.0 / 7.0


# ---------------------------------------------------------------------------
# the decoder
# ---------------------------------------------------------------------------


class CoherenceDecoder:
    """Wraps an LMGeometry singleton with a coherence-gated generation loop.

    Holds a reference to the loaded model + tokenizer + AO basis from
    LMGeometry, plus the V-x-10 op_token_M and the 5x5 Hebbian W.

    Thread-safety: single-process; do not call generate() concurrently.
    """

    def __init__(self, lm_geometry, hebbian_W=None,
                 op_token_M=None, op_token_summary: Optional[Dict] = None):
        if lm_geometry is None or not getattr(lm_geometry, "loaded", False):
            raise ValueError("lm_geometry must be a loaded LMGeometry")
        self.lm = lm_geometry

        # 5x5 Hebbian (cortex prior).  Keep as a python list of lists for now;
        # we'll torch-it at use sites.
        if hebbian_W is None:
            self.W = [[0.0] * NUM_AO for _ in range(NUM_AO)]
        else:
            self.W = [[float(hebbian_W[i][j]) for j in range(NUM_AO)]
                      for i in range(NUM_AO)]

        # Operator -> token preference matrix.
        if op_token_M is None:
            logger.info(
                "[coherence_decode] building op_token_basis "
                "(this may take a few seconds)..."
            )
            # Use the model's config vocab_size; for Llama-3.1 it is 128256
            # while tokenizer.vocab_size is 128000.  We need M to match the
            # logit dimension exactly.
            cfg_vocab = int(getattr(self.lm.model.config, "vocab_size", 0)) or None
            op_token_M, op_token_summary = build_op_token_matrix(
                self.lm.tokenizer,
                device=str(self.lm.B.device),
                dtype=self.lm.B.dtype,
                vocab_size=cfg_vocab,
            )
        self.M = op_token_M                       # (V, 10)
        self.op_token_summary = dict(op_token_summary or {})

        logger.info(
            f"[coherence_decode] ready: V={self.M.shape[0]}, "
            f"|W|_F={math.sqrt(sum(self.W[i][j]**2 for i in range(NUM_AO) for j in range(NUM_AO))):.3f}"
        )

    # ----- internal helpers -----

    def _W_mul_d(self, d):
        """Compute primed = W @ d (as Python floats; d is list[5])."""
        out = [0.0] * NUM_AO
        for i in range(NUM_AO):
            s = 0.0
            row = self.W[i]
            for j in range(NUM_AO):
                s += row[j] * d[j]
            out[i] = s
        return out

    def _hebbian_update(self, d_now, d_prev, eta: float = 0.05,
                        clamp_abs: float = 5.0):
        """Symmetric Hebbian update on self.W (in-place).

        delta_ij = 0.5 * (d_now[i] * d_prev[j] + d_now[j] * d_prev[i])
        W_ij <- clamp(W_ij + eta * delta_ij, +/-clamp_abs)
        Symmetric (W_ij = W_ji preserved).
        """
        for i in range(NUM_AO):
            for j in range(i, NUM_AO):
                delta = 0.5 * (d_now[i] * d_prev[j] + d_now[j] * d_prev[i])
                w = self.W[i][j] + eta * delta
                if w > clamp_abs: w = clamp_abs
                elif w < -clamp_abs: w = -clamp_abs
                self.W[i][j] = w
                self.W[j][i] = w

    # ----- the loop -----

    def generate(self, prompt: str, max_new_tokens: int = 64,
                 alpha: float = DEFAULT_ALPHA,
                 beta: float = DEFAULT_BETA,
                 temperature: float = DEFAULT_TEMPERATURE,
                 top_k: int = DEFAULT_TOP_K,
                 learn: bool = False,
                 stop_on_eos: bool = True,
                 random_seed: Optional[int] = None) -> Dict[str, Any]:
        """Coherence-gated generation.  Returns text + per-token diagnostics."""
        if not self.lm.loaded:
            return {"ok": False, "error": "LMGeometry not loaded"}
        if not prompt or not prompt.strip():
            return {"ok": False, "error": "empty prompt"}

        try:
            return self._generate_inner(prompt, max_new_tokens, alpha, beta,
                                        temperature, top_k, learn,
                                        stop_on_eos, random_seed)
        except Exception as e:  # noqa: BLE001
            logger.exception("[coherence_decode] generate crashed")
            return {"ok": False, "error": f"{type(e).__name__}: {e}"}

    def _generate_inner(self, prompt: str, max_new_tokens: int,
                        alpha: float, beta: float,
                        temperature: float, top_k: int,
                        learn: bool, stop_on_eos: bool,
                        random_seed: Optional[int]) -> Dict[str, Any]:
        import torch
        from ck.brain.lm_geometry import project_hidden

        t_start = time.monotonic()
        if random_seed is not None:
            torch.manual_seed(int(random_seed))

        tok = self.lm.tokenizer
        model = self.lm.model
        B = self.lm.B
        device = B.device
        eos_id = int(tok.eos_token_id) if tok.eos_token_id is not None else -1

        # Prepare prompt with chat template (single-turn)
        try:
            messages = [{"role": "user", "content": prompt}]
            templated = tok.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True,
            )
        except Exception:
            templated = prompt
        enc = tok(templated, return_tensors="pt").to(device)
        prompt_len = int(enc.input_ids.shape[1])
        cur_ids = enc.input_ids                          # (1, T)

        # Per-step diagnostics
        traj_signed: List[List[float]] = []
        traj_mag:    List[List[float]] = []
        traj_op:     List[str] = []
        traj_coh:    List[float] = []
        traj_op_idx: List[int] = []
        token_strs:  List[str] = []
        token_ids:   List[int] = []

        d_prev: Optional[List[float]] = None

        with torch.no_grad():
            for step in range(int(max_new_tokens)):
                # Forward pass on full prefix.  We use the full prefix every
                # step (no KV cache for this prototype) -- correct, but slower.
                # ~50-100ms per step on a 4070 for short prefixes.
                outputs = model(
                    input_ids=cur_ids,
                    output_hidden_states=True,
                    return_dict=True,
                )
                # Last layer, last token
                last_hidden = outputs.hidden_states[-1][0, -1]   # (4096,)
                logits = outputs.logits[0, -1]                   # (V,)

                # Project to AO
                s_signed, d_now, op_idx = project_hidden(last_hidden, B)

                # Cortex prime
                primed = self._W_mul_d(d_now)
                op_10  = signed_lift_5_to_10(s_signed, primed)

                # Token bias = M . op_10  (V-vector).  Auto-scale so that
                # a meaningful alpha is in [0, 1].  Without scaling, |bias|_max
                # ~ 0.01 vs |logits|_max ~ 30, so alpha would need to be 1000+
                # to matter.  We rescale bias to have max == one std of logits.
                op_10_t = torch.tensor(op_10, dtype=B.dtype, device=device)  # (10,)
                token_bias = self.M @ op_10_t                               # (V,)
                bias_max = float(token_bias.abs().max())
                if bias_max > 1e-9:
                    logits_std = float(logits.float().std())
                    # scale so max |bias| = logits_std (so alpha=1 shifts top
                    # tokens by ~one std, alpha=0.3 by ~0.3 std).  This is the
                    # "alpha is a fraction of LM's natural spread" convention.
                    token_bias = token_bias * (logits_std / bias_max)

                # Transition penalty -- scalar, broadcast subtract
                if d_prev is None:
                    trans_penalty = 0.0
                else:
                    diff = sum((d_now[i] - d_prev[i]) ** 2 for i in range(NUM_AO))
                    trans_penalty = float(diff)

                # Reshape logits
                logits_g = logits + alpha * token_bias - beta * trans_penalty

                # Sample with optional top-k truncation
                if top_k and top_k > 0 and top_k < int(logits_g.shape[0]):
                    topk_vals, topk_idx = torch.topk(logits_g, top_k)
                    # mask out everything else
                    masked = torch.full_like(logits_g, float("-inf"))
                    masked.scatter_(0, topk_idx, topk_vals)
                    logits_g = masked

                if temperature and temperature > 0:
                    probs = torch.softmax(logits_g / float(temperature), dim=-1)
                    next_id = int(torch.multinomial(probs, num_samples=1).item())
                else:
                    next_id = int(torch.argmax(logits_g).item())

                # Coherence with current cortex (d^T W d / ||d||^2)
                norm_d = sum(x*x for x in d_now)
                if norm_d > 1e-12:
                    coh = sum(d_now[i] * primed[i] for i in range(NUM_AO)) / norm_d
                else:
                    coh = 0.0

                # Record
                traj_signed.append([round(x, 4) for x in s_signed])
                traj_mag.append([round(x, 4) for x in d_now])
                traj_op.append(OP_NAMES[op_idx])
                traj_op_idx.append(op_idx)
                traj_coh.append(round(float(coh), 4))
                token_ids.append(next_id)
                token_strs.append(tok.decode([next_id], skip_special_tokens=False))

                # Hebbian update during generation (optional)
                if learn and d_prev is not None:
                    self._hebbian_update(d_now, d_prev)

                d_prev = d_now

                # Append next token to running prefix
                cur_ids = torch.cat(
                    [cur_ids,
                     torch.tensor([[next_id]], dtype=cur_ids.dtype, device=device)],
                    dim=1,
                )

                if stop_on_eos and next_id == eos_id:
                    break

        # Decode the generated text only (skip prompt)
        gen_text = tok.decode(cur_ids[0, prompt_len:].tolist(),
                              skip_special_tokens=True)

        # Trajectory coherence: average cosine similarity between adjacent
        # token AO magnitudes (same definition as Epoch I forward())
        from ck.brain.lm_geometry import trajectory_coherence
        traj_coh_overall = float(trajectory_coherence(traj_mag))

        # Average cortex coherence (d^T W d / ||d||^2 averaged over tokens)
        if traj_coh:
            mean_cortex_coh = sum(traj_coh) / len(traj_coh)
        else:
            mean_cortex_coh = 0.0

        # Most-frequent operator in the generation
        from collections import Counter
        op_counts = Counter(traj_op)

        out = {
            "ok": True,
            "prompt": prompt[:500],
            "text": gen_text,
            "n_new_tokens": len(token_ids),
            "tokens_generated": token_strs,
            "token_ids": token_ids,
            "traj_op_per_token": traj_op,
            "traj_op_idx_per_token": traj_op_idx,
            "traj_coh_per_token": traj_coh,
            "traj_signed": traj_signed,
            "traj_mag": traj_mag,
            "trajectory_coherence": round(traj_coh_overall, 4),
            "mean_cortex_coh": round(mean_cortex_coh, 4),
            "T_star": T_STAR,
            "above_T_star": bool(traj_coh_overall >= T_STAR),
            "alpha": alpha,
            "beta": beta,
            "temperature": temperature,
            "top_k": top_k,
            "learn": learn,
            "op_counts": dict(op_counts),
            "elapsed_ms": int((time.monotonic() - t_start) * 1000),
        }
        return out


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Coherence-gated LM generation (EPOCH II of Sovereignty Plan)."
    )
    ap.add_argument("prompt")
    ap.add_argument("--base", default="unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit")
    ap.add_argument("--lora", default=None)
    ap.add_argument("--max", dest="max_new_tokens", type=int, default=64)
    ap.add_argument("--alpha", type=float, default=DEFAULT_ALPHA)
    ap.add_argument("--beta", type=float, default=DEFAULT_BETA)
    ap.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE)
    ap.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    ap.add_argument("--learn", action="store_true",
                    help="apply Hebbian update during generation")
    ap.add_argument("--cortex-state", default=None,
                    help="optional path to cortex_state.json to seed W")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--pretty", action="store_true")
    return ap.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(name)s %(levelname)s %(message)s")
    args = _parse_args(argv)

    from ck.brain.lm_geometry import LMGeometry
    g = LMGeometry(base_model=args.base, lora_path=args.lora)
    st = g.load()
    if not st["loaded"]:
        print(json.dumps(st, indent=2), file=sys.stderr)
        return 2

    # Optional cortex state.  Supports several storage shapes:
    #   {"W": [[...]]}                              (worktree hebbian_5x5.py)
    #   {"hebbian_W": [[...]]}                      (legacy alias)
    #   {"hebbian": {"W": [[...]]}}                 (Gen13 cortex_state.json)
    #   {"cortex": {"W": [[...]]}}                  (alt)
    W = None
    if args.cortex_state:
        try:
            with open(args.cortex_state, "r", encoding="utf-8") as f:
                cs = json.load(f)
            W = cs.get("W") or cs.get("hebbian_W")
            if W is None and isinstance(cs.get("hebbian"), dict):
                W = cs["hebbian"].get("W") or cs["hebbian"].get("matrix")
            if W is None and isinstance(cs.get("cortex"), dict):
                W = cs["cortex"].get("W")
            if W is not None:
                print(f"[coherence_decode] loaded W from {args.cortex_state}")
        except Exception as e:
            print(f"[coherence_decode] could not load cortex_state: {e}",
                  file=sys.stderr)

    dec = CoherenceDecoder(g, hebbian_W=W)
    out = dec.generate(
        args.prompt,
        max_new_tokens=args.max_new_tokens,
        alpha=args.alpha, beta=args.beta,
        temperature=args.temperature, top_k=args.top_k,
        learn=args.learn,
        random_seed=args.seed,
    )

    if not out.get("ok"):
        print(json.dumps(out, indent=2), file=sys.stderr)
        return 3

    if args.pretty:
        print()
        print(f"=== Coherence-gated generation ===")
        print(f"  prompt: {args.prompt!r}")
        print(f"  alpha={args.alpha}  beta={args.beta}  temp={args.temperature}")
        print(f"  generated tokens: {out['n_new_tokens']}, elapsed: {out['elapsed_ms']} ms")
        print(f"  trajectory_coherence: {out['trajectory_coherence']:.4f}  "
              f"(T*={T_STAR:.4f}, above={out['above_T_star']})")
        print(f"  mean_cortex_coh: {out['mean_cortex_coh']:.4f}")
        print(f"  op_counts: {out['op_counts']}")
        print()
        print(f"  CK said: {out['text']}")
        print()
        print("  Per-token op trail:")
        toks = out["tokens_generated"]
        ops = out["traj_op_per_token"]
        cohs = out["traj_coh_per_token"]
        for tk, op, coh in zip(toks, ops, cohs):
            print(f"    {tk!r:30s} -> {op:<10s}  coh={coh:.3f}")
    else:
        print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
