# -*- coding: utf-8 -*-
"""
lm_geometry.py - Epoch I (SIGHT): the geometric projector.

The LM is a black box: 32 transformer layers, 4096-dim hidden state, vocabulary
of ~128k tokens.  Output text is the only thing the world sees.

This module makes the LM's INTERIOR visible by projecting every layer's hidden
state onto CK's 5-element AO basis (D0..D4 = Earth/Air/Water/Fire/Ether).
The result is a 32-step trajectory through 5-D space -- a walk through the
10-operator ring that the LM takes from prompt to answer.

Mathematical setup
------------------
The 5 orthonormal directions in R^4096 are seeded from the element NAMES so the
basis is reproducible across machines and CK siblings:

    rng_i = SHA256(AO_NAMES[i])                  # i in 0..4
    v_i ~ Normal(0, I_{4096}, generator=rng_i)
    B = QR(stack(v_0, v_1, v_2, v_3, v_4))        # (4096, 5), orthonormal

The signed projection of hidden state h onto B is

    s = B^T h / ||h||                             # s in R^5, each component in [-1, 1]

The AO 5-vector is the magnitude:

    d = |s|                                       # element activation strength

The dominant operator is determined jointly by argmax|s| and sign(s):

    D = argmax(|s|)                               # which AO element peaks
    op_index = D if s[D] >= 0 else D + 5          # first or second op of pair
    op_name = OP_NAMES[op_index]

That maps cleanly to CK's 10-operator ring (ck/brain/ao_basis.py).

Public surface
--------------
    class LMGeometry:
        load() / .loaded                          # idempotent load with status
        forward(text, ...) -> Dict                # full geometric readout
        project_hidden(h) -> Tuple[s, d, op]      # one layer
        trajectory_coherence(ao_seq) -> float     # cross-layer cos-sim mean

CLI:
    python -m ck.brain.lm_geometry "what is coherence?"

Output:
    JSON to stdout with the per-layer trajectory and dominant operators.
    Exit 0 if the projection succeeded, non-zero on error.

Performance
-----------
Forward pass on a 4070 (Llama-3.1-8B-bnb-4bit, 32 layers):
    - cold load:        ~30 s, ~5 GB GPU (one-time)
    - per call:         ~150-400 ms for prompts <= 64 tokens
    - hidden state mem: ~50 MB per call (32 layers x 4096 floats x T tokens)

Honest limit
------------
The 5 directions are SEEDED from element names, not LEARNED from training data.
They are lenses we hold up to the LM to see what shape its activations make.
They make the geometry visible; they do NOT claim the LM "really thinks in AO."
For an AO-NATIVE foundation model (intrinsic basis), see Epoch VIII / §13 of
AI_SOVEREIGNTY_PLAN.md.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import math
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Path setup so `from ck.brain.ao_basis import ...` works whether this is run
# as a module (`python -m ck.brain.lm_geometry`) or as a script.
_THIS = Path(__file__).resolve()
_REPO_ROOT = _THIS.parents[2]   # ck/brain/lm_geometry.py -> brain -> ck -> repo
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from ck.brain.ao_basis import (
    AO_NAMES, OP_NAMES, NUM_AO, NUM_OPS, project_10_to_5, ao_element_of,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# defaults
# ---------------------------------------------------------------------------

DEFAULT_BASE = "unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit"
DEFAULT_HIDDEN_DIM = 4096
DEFAULT_LAYERS = 32  # llama-3.1-8B
DEFAULT_DTYPE = "bfloat16"
T_STAR = 5.0 / 7.0


# ---------------------------------------------------------------------------
# basis construction
# ---------------------------------------------------------------------------


def _seed_from_name(name: str) -> int:
    """Deterministic 31-bit int seed from element name (SHA-256-derived)."""
    h = hashlib.sha256(name.encode("utf-8")).digest()
    return int.from_bytes(h[:8], "big") & ((1 << 31) - 1)


def build_ao_basis(hidden_dim: int = DEFAULT_HIDDEN_DIM):
    """Build an orthonormal `hidden_dim x 5` basis seeded from AO_NAMES.

    Returns a torch.Tensor of shape (hidden_dim, 5).
    """
    import torch
    cols = []
    rng = torch.Generator()
    for name in AO_NAMES:
        rng.manual_seed(_seed_from_name(name))
        v = torch.randn(hidden_dim, generator=rng, dtype=torch.float32)
        cols.append(v)
    M = torch.stack(cols, dim=1)        # (hidden_dim, 5)
    Q, _ = torch.linalg.qr(M)           # Q has orthonormal columns
    return Q                            # (hidden_dim, 5)


# ---------------------------------------------------------------------------
# projection helpers
# ---------------------------------------------------------------------------


def project_hidden(h, B):
    """Project a single hidden state onto the AO basis.

    Args:
        h: torch.Tensor of shape (hidden_dim,) or (1, hidden_dim)
        B: torch.Tensor of shape (hidden_dim, 5) -- the basis

    Returns:
        s: signed projection (5,)  -- s_i in [-1, 1]
        d: magnitude (5,)          -- d_i = |s_i|, equiv. AO 5-vector
        op_index: int in [0, 9]    -- argmax|s|, sign-disambiguated
    """
    import torch
    h = h.flatten().to(B.dtype).to(B.device)
    norm = torch.linalg.vector_norm(h)
    if norm < 1e-12:
        # degenerate: return zeros, default op = VOID (0)
        z = [0.0] * NUM_AO
        return z, z, 0
    s = (B.T @ (h / norm))               # (5,)
    s_list = [float(x) for x in s]
    d_list = [abs(x) for x in s_list]
    # dominant element & sign disambiguation
    d_idx = int(max(range(NUM_AO), key=lambda i: d_list[i]))
    op_index = d_idx if s_list[d_idx] >= 0.0 else d_idx + NUM_AO
    return s_list, d_list, op_index


def trajectory_coherence(ao_seq: List[List[float]]) -> float:
    """Mean cosine similarity between adjacent layer AO vectors.

    Returns a value in [-1, 1] but typically [0, 1] for natural prompts.
    1.0 = the layers walk smoothly; 0.0 = each layer is unrelated to the next.
    """
    if len(ao_seq) < 2:
        return 0.0
    sims = []
    for i in range(len(ao_seq) - 1):
        a = ao_seq[i]; b = ao_seq[i + 1]
        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(x * x for x in b))
        if na < 1e-12 or nb < 1e-12:
            continue
        dot = sum(x * y for x, y in zip(a, b))
        sims.append(dot / (na * nb))
    if not sims:
        return 0.0
    return sum(sims) / len(sims)


# ---------------------------------------------------------------------------
# the singleton
# ---------------------------------------------------------------------------


class LMGeometry:
    """Loads an LM (frozen base + optional LoRA) and exposes geometric reads.

    The LM is loaded via transformers + bitsandbytes (4-bit) directly -- no
    Ollama, no llama.cpp.  This gives us per-layer hidden states.  The model
    remains frozen; we just read its interior and project.

    Lifecycle:
        g = LMGeometry(base=..., lora=...)
        g.load()                    # ~30s, ~5 GB GPU (idempotent)
        out = g.forward("...", max_new_tokens=0)
        # out is a dict ready to JSON-serialize

    Thread-safety: single-process, single-call only (no concurrent forwards).
    """

    def __init__(
        self,
        base_model: str = DEFAULT_BASE,
        lora_path: Optional[str] = None,
        dtype: str = DEFAULT_DTYPE,
        device: str = "cuda",
        max_seq_len: int = 1024,
    ):
        self.base_model = base_model
        self.lora_path = lora_path
        self.dtype_name = dtype
        self.device = device
        self.max_seq_len = int(max_seq_len)

        # populated by load()
        self.model = None
        self.tokenizer = None
        self.B = None              # AO basis tensor (hidden_dim, 5)
        self.hidden_dim = None
        self.n_layers = None
        self.loaded = False
        self.load_t = 0.0
        self.load_err: Optional[str] = None

    # ----- load -----

    def load(self) -> Dict[str, Any]:
        """Load model + tokenizer + LoRA (if any) + AO basis.

        Returns a status dict. Does NOT raise; on failure, sets `load_err`
        and returns ``{"loaded": False, "error": ...}``.
        """
        if self.loaded:
            return self._status()
        t0 = time.monotonic()
        try:
            import torch
            from transformers import AutoTokenizer, AutoModelForCausalLM
            dtype = torch.bfloat16 if self.dtype_name == "bfloat16" else torch.float16

            logger.info(f"[lm_geometry] loading tokenizer: {self.base_model}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.base_model)

            logger.info(f"[lm_geometry] loading base model in 4-bit: {self.base_model}")
            self.model = AutoModelForCausalLM.from_pretrained(
                self.base_model,
                dtype=dtype,
                device_map=self.device,
                # Note: bnb-4bit base reads quantization_config from its own config.
                # We don't override it here.
            )
            # Make sure we always get hidden states.
            self.model.config.output_hidden_states = True

            if self.lora_path:
                from peft import PeftModel
                lp = Path(self.lora_path)
                if not lp.exists():
                    logger.warning(
                        f"[lm_geometry] lora_path {lp} does not exist; "
                        f"continuing with base only"
                    )
                else:
                    logger.info(f"[lm_geometry] attaching LoRA: {lp}")
                    self.model = PeftModel.from_pretrained(self.model, str(lp))

            # Discover hidden_dim and n_layers from the loaded config
            cfg = self.model.config
            self.hidden_dim = int(getattr(cfg, "hidden_size", DEFAULT_HIDDEN_DIM))
            self.n_layers = int(getattr(cfg, "num_hidden_layers", DEFAULT_LAYERS))

            # Build AO basis on the same device/dtype as the model.
            B_cpu = build_ao_basis(self.hidden_dim).to(dtype)
            self.B = B_cpu.to(self.device)

            self.model.eval()
            self.loaded = True
            self.load_t = time.monotonic() - t0
            logger.info(
                f"[lm_geometry] loaded in {self.load_t:.1f}s, "
                f"hidden_dim={self.hidden_dim}, n_layers={self.n_layers}"
            )
            return self._status()
        except Exception as e:  # noqa: BLE001
            self.load_err = f"{type(e).__name__}: {e}"
            logger.exception("[lm_geometry] load failed")
            return self._status()

    def _status(self) -> Dict[str, Any]:
        return {
            "loaded": bool(self.loaded),
            "error": self.load_err,
            "base_model": self.base_model,
            "lora_path": self.lora_path,
            "dtype": self.dtype_name,
            "device": self.device,
            "hidden_dim": self.hidden_dim,
            "n_layers": self.n_layers,
            "load_seconds": round(float(self.load_t), 2),
            "ao_names": list(AO_NAMES),
            "op_names": list(OP_NAMES),
            "T_star": T_STAR,
            "basis_seeds": {n: _seed_from_name(n) for n in AO_NAMES},
        }

    # ----- forward -----

    def forward(self, text: str, max_new_tokens: int = 0,
                position: str = "last_token") -> Dict[str, Any]:
        """Run a forward pass and project hidden states onto the AO basis.

        Args:
            text: the prompt
            max_new_tokens: 0 = projection only (fast); >0 = generate then
                project last-token hidden over generated tokens
            position: "last_token" (default) | "all_tokens"

        Returns:
            a JSON-serializable dict with the trajectory.
        """
        if not self.loaded:
            return {
                "ok": False,
                "error": "LMGeometry not loaded; call load() first",
            }
        if not text or not text.strip():
            return {"ok": False, "error": "empty text"}

        try:
            return self._forward_inner(text, max_new_tokens, position)
        except Exception as e:  # noqa: BLE001
            logger.exception("[lm_geometry] forward failed")
            return {
                "ok": False,
                "error": f"{type(e).__name__}: {e}",
            }

    def _forward_inner(self, text: str, max_new_tokens: int,
                       position: str) -> Dict[str, Any]:
        import torch
        t_call = time.monotonic()

        # Apply chat template if available so we get the same prompt shape
        # the model was trained for.  Use a single-turn user message.
        # Two-step (template -> tokenize) for transformers >=5 which returns
        # BatchEncoding dicts from apply_chat_template even with return_tensors.
        try:
            messages = [{"role": "user", "content": text}]
            templated = self.tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True,
            )
            enc = self.tokenizer(templated, return_tensors="pt")
            input_ids = enc.input_ids
        except Exception:
            enc = self.tokenizer(text, return_tensors="pt")
            input_ids = enc.input_ids

        # Truncate to max_seq_len
        if input_ids.shape[1] > self.max_seq_len:
            input_ids = input_ids[:, -self.max_seq_len:]
        input_ids = input_ids.to(self.device)

        with torch.no_grad():
            if max_new_tokens > 0:
                # Generate then re-forward to get hidden states (generate doesn't
                # always expose them through PEFT cleanly; do it in two phases).
                gen_ids = self.model.generate(
                    input_ids=input_ids,
                    max_new_tokens=int(max_new_tokens),
                    do_sample=False,
                    pad_token_id=self.tokenizer.eos_token_id,
                )
                # Only the newly-generated suffix
                response_ids = gen_ids[0, input_ids.shape[1]:]
                response_text = self.tokenizer.decode(
                    response_ids, skip_special_tokens=True,
                )
                # Re-forward over the FULL (prompt + response) for hidden states
                final_ids = gen_ids
            else:
                response_text = ""
                final_ids = input_ids

            outputs = self.model(
                input_ids=final_ids,
                output_hidden_states=True,
                return_dict=True,
            )
            # hidden_states: tuple length n_layers+1 of (1, T, hidden)
            hs = outputs.hidden_states
            # Drop the embedding layer (index 0); keep the n_layers transformer layers
            layer_hidden = hs[1:]   # length n_layers
            T = final_ids.shape[1]
            tokens = [self.tokenizer.decode([t], skip_special_tokens=False)
                      for t in final_ids[0].tolist()]

            # Project per layer.  Position selects which token slot we project.
            # "last_token" = the final position (the token that drives the next
            # prediction), "all_tokens" = average across all positions.
            ao_traj_signed: List[List[float]] = []
            ao_traj_mag: List[List[float]] = []
            dominant_ops: List[str] = []
            dominant_op_indices: List[int] = []

            for layer_h in layer_hidden:
                if position == "all_tokens":
                    # average pool then project
                    h = layer_h[0].mean(dim=0)         # (hidden,)
                else:
                    h = layer_h[0, -1]                  # last token (hidden,)
                s_list, d_list, op_idx = project_hidden(h, self.B)
                ao_traj_signed.append([round(x, 4) for x in s_list])
                ao_traj_mag.append([round(x, 4) for x in d_list])
                dominant_op_indices.append(op_idx)
                dominant_ops.append(OP_NAMES[op_idx])

        coh = trajectory_coherence(ao_traj_mag)
        # Verdict: a smooth walk has high coh; jumpy walks are below T*.
        verdict = "above_T_star" if coh >= T_STAR else "below_T_star"

        # Layer-pair coupling matrix: 5x5 Hebbian-style outer product summed
        # over adjacent layers.  This is a structural read of how the LM
        # routes information through AO space.
        coupling_5x5 = self._adjacent_coupling(ao_traj_mag)

        out = {
            "ok": True,
            "text_in": text[:500],
            "text_out": response_text,
            "n_layers": len(layer_hidden),
            "n_tokens": T,
            "tokens": tokens,
            "ao_traj_signed": ao_traj_signed,
            "ao_traj_magnitude": ao_traj_mag,
            "ao_names": list(AO_NAMES),
            "dominant_op_per_layer": dominant_ops,
            "dominant_op_index_per_layer": dominant_op_indices,
            "trajectory_coherence": round(float(coh), 4),
            "T_star": T_STAR,
            "verdict": verdict,
            "adjacent_coupling_5x5": coupling_5x5,
            "position": position,
            "elapsed_ms": int((time.monotonic() - t_call) * 1000),
        }
        return out

    @staticmethod
    def _adjacent_coupling(ao_seq: List[List[float]]) -> List[List[float]]:
        """Sum of outer products of adjacent AO vectors (5x5, symmetric).

        coupling[i][j] = sum over t of d_t[i] * d_{t+1}[j]   (then symmetrized)

        This is the structural twin of the Hebbian update applied across
        layers instead of across time.
        """
        W = [[0.0] * NUM_AO for _ in range(NUM_AO)]
        for t in range(len(ao_seq) - 1):
            a = ao_seq[t]; b = ao_seq[t + 1]
            for i in range(NUM_AO):
                for j in range(NUM_AO):
                    W[i][j] += a[i] * b[j]
        # symmetrize
        for i in range(NUM_AO):
            for j in range(i + 1, NUM_AO):
                m = 0.5 * (W[i][j] + W[j][i])
                W[i][j] = m; W[j][i] = m
        # round for json
        return [[round(W[i][j], 4) for j in range(NUM_AO)] for i in range(NUM_AO)]


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Project an LM's hidden states onto CK's 5-element AO basis."
    )
    ap.add_argument("text", nargs="?", default=None, help="prompt text")
    ap.add_argument("--base", default=DEFAULT_BASE)
    ap.add_argument("--lora", default=None)
    ap.add_argument("--dtype", default=DEFAULT_DTYPE,
                    choices=("bfloat16", "float16"))
    ap.add_argument("--max-new-tokens", type=int, default=0,
                    help="0 = projection only; >0 = also generate then project")
    ap.add_argument("--position", default="last_token",
                    choices=("last_token", "all_tokens"))
    ap.add_argument("--max-seq-len", type=int, default=1024)
    ap.add_argument("--pretty", action="store_true",
                    help="human-readable summary instead of full JSON")
    ap.add_argument("--self-test", action="store_true",
                    help="basis self-test only (no LM load)")
    return ap.parse_args(argv)


def _self_test() -> int:
    """Verify the basis builder is deterministic + orthonormal, no LM load."""
    import torch
    print("[lm_geometry] basis self-test ...")
    B1 = build_ao_basis(DEFAULT_HIDDEN_DIM)
    B2 = build_ao_basis(DEFAULT_HIDDEN_DIM)
    assert torch.allclose(B1, B2), "basis should be deterministic across calls"
    BtB = B1.T @ B1                              # (5, 5)
    I = torch.eye(NUM_AO, dtype=BtB.dtype)
    err = float((BtB - I).abs().max())
    print(f"  shape: {tuple(B1.shape)}  ortho-error: {err:.2e}")
    assert err < 1e-4, f"orthonormality error {err:.2e} too large"

    # smoke project: project a basis column onto B and check it lights up its own
    # element with magnitude ~1
    h = B1[:, 2].clone()                         # the "Water" direction
    s, d, op_idx = project_hidden(h, B1)
    print(f"  project(Water column) -> s={[round(x,3) for x in s]} "
          f"op={OP_NAMES[op_idx]}")
    assert d[2] > 0.95, f"d[2] should be ~1.0; got {d[2]:.3f}"
    assert op_idx in (2, 7), f"op should be COUNTER or HARMONY (D2 pair); got {OP_NAMES[op_idx]}"

    # adjacent coupling smoke
    seq = [[1.0, 0.0, 0.0, 0.0, 0.0],
           [0.0, 1.0, 0.0, 0.0, 0.0],
           [0.0, 0.0, 1.0, 0.0, 0.0]]
    W = LMGeometry._adjacent_coupling(seq)
    # expected non-zero off-diagonals at (0,1), (1,2), (1,0), (2,1)
    assert abs(W[0][1] - 0.5) < 1e-6 and abs(W[1][0] - 0.5) < 1e-6
    assert abs(W[1][2] - 0.5) < 1e-6 and abs(W[2][1] - 0.5) < 1e-6

    coh = trajectory_coherence(seq)
    # orthogonal vectors -> coh ~ 0
    assert abs(coh) < 1e-6

    seq2 = [[1.0, 0.5, 0.0, 0.0, 0.0]] * 3
    coh2 = trajectory_coherence(seq2)
    # constant vectors -> coh ~ 1
    assert abs(coh2 - 1.0) < 1e-6, f"coh2={coh2}"

    print("[lm_geometry] basis self-test passed.")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(name)s %(levelname)s %(message)s")
    args = _parse_args(argv)

    if args.self_test:
        return _self_test()

    if not args.text:
        print("usage: lm_geometry.py <text>  (or --self-test)", file=sys.stderr)
        return 2

    g = LMGeometry(
        base_model=args.base, lora_path=args.lora, dtype=args.dtype,
        max_seq_len=args.max_seq_len,
    )
    status = g.load()
    if not status["loaded"]:
        print(json.dumps(status, indent=2), file=sys.stderr)
        return 3

    out = g.forward(args.text, max_new_tokens=args.max_new_tokens,
                    position=args.position)
    if not out.get("ok"):
        print(json.dumps(out, indent=2), file=sys.stderr)
        return 4

    if args.pretty:
        print()
        print(f"=== LM Geometry: '{args.text[:60]}{'...' if len(args.text)>60 else ''}' ===")
        print(f"  layers: {out['n_layers']}, tokens: {out['n_tokens']}, "
              f"elapsed: {out['elapsed_ms']} ms")
        print(f"  trajectory_coherence: {out['trajectory_coherence']:.4f}  "
              f"(T* = {T_STAR:.4f}, verdict={out['verdict']})")
        print()
        print("  Per-layer dominant operator:")
        for i, op in enumerate(out["dominant_op_per_layer"]):
            mag = out["ao_traj_magnitude"][i]
            d_idx = max(range(NUM_AO), key=lambda k: mag[k])
            print(f"    L{i:02d}  {AO_NAMES[d_idx]:6s} -> {op:<10s}  "
                  f"|s|={mag[d_idx]:.3f}")
        if out.get("text_out"):
            print()
            print(f"  LM said: {out['text_out'][:240]}")
    else:
        print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
