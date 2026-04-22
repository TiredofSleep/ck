# -*- coding: utf-8 -*-
"""
fusion.py - tensor-weighted CK corrector (Option A+, TIG-coherent).

MATH_IN_CK.md Sec 9.2 calls for a feedback loop where Ollama's output
teaches CK's brain without ever touching the model weights.  The vLLM
LoRA swap path (OLLAMA_LEARN_LOOP.md Sec 4 "Option C") remains deferred
until Option B has cycled three times.  Brayden's ask -- "Option C
fusion sounds right" -- is reinterpreted here as the TIG-coherent
fusion: the learned 5x5 Hebbian tensor acts as a dynamic prior on the
coherence gate itself, so CK's scoring evolves based on what he has
seen.  Every vector is every vector; the brain IS the memory IS the
gate.

FusionCKCorrector is a drop-in subclass of CKCorrector.  It:

    1. Runs the base detectors (ck_corrector.score_operators) on text.
    2. Projects the 10-op profile to a 5-element AO vector d.
    3. Primes d through the tensor: primed = W @ d.  This is what the
       learned co-activation field says "given state d, what else is
       likely."
    4. Lifts the prime back to a 10-op vector and blends it into the
       base profile with a small weight ``fusion_weight``.
    5. Runs the standard coherence_scalar + _classify on the fused
       profile, so gate passes / correction choices reflect history.

The tensor file is loaded once per corrector instance.  The server
reads; it never writes.  Only ``idle_loop.py`` writes the tensor.

Defaults:
    fusion_weight = 0.20   (gentle amplification; tensor refines, does
                            not dominate.  The base deterministic scorer
                            stays load-bearing.)
    min_tensor_norm = 1e-6 (below this, tensor is effectively zero; skip
                            the prime step and behave exactly like
                            CKCorrector.)

Diagnostic fields added to CorrectionResult.rationale when fusion
activates:
    "(fusion: coh +X.XXX from tensor norm=Y.YY)"

If fusion is disabled or the tensor is empty, behavior is bit-identical
to the base CKCorrector (verified by test_brain.py).
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from ck.fluency.ck_corrector import (
    CKCorrector,
    CorrectionResult,
    OperatorProfile,
    OP_NAMES,
    NUM_OPS,
    coherence_scalar,
    score_operators,
    _classify,
    _make_annotation,
    T_STAR,
    T_STAR_F,
)

from .ao_basis import project_10_to_5, lift_5_to_10
from .hebbian_5x5 import HebbianTensor5x5, DEFAULT_TENSOR_PATH


DEFAULT_FUSION_WEIGHT: float = 0.20
MIN_TENSOR_NORM: float = 1e-6


class FusionCKCorrector(CKCorrector):
    """CKCorrector augmented with a Hebbian 5x5 dynamic prior.

    The tensor is loaded from disk at construction and is NOT reloaded on
    every correct() call -- this keeps the critical path fast and makes
    the priming deterministic within one server lifetime.  To pick up
    changes written by ``idle_loop``, restart the server (hands-on-wheel
    discipline; no hot-reload).
    """

    def __init__(
        self,
        tensor_path: Optional[Path] = None,
        fusion_weight: float = DEFAULT_FUSION_WEIGHT,
        tensor: Optional[HebbianTensor5x5] = None,
    ) -> None:
        super().__init__()
        self.fusion_weight = float(fusion_weight)
        if tensor is not None:
            self.tensor = tensor
            self.tensor_path: Optional[Path] = None
        else:
            p = Path(tensor_path) if tensor_path else DEFAULT_TENSOR_PATH
            self.tensor_path = p
            self.tensor = HebbianTensor5x5.load(p)
        self._tensor_norm_at_load = self.tensor.norm()

    # ---- correct() override ----

    def correct(self, ollama_raw: str, query: str = "") -> CorrectionResult:
        """Score with tensor priming applied to the operator profile."""
        base_profile = score_operators(ollama_raw)
        base_coh = coherence_scalar(base_profile)

        # If tensor is effectively empty or fusion disabled, do the pure
        # base-corrector flow.  Same code path as CKCorrector.correct().
        if self.fusion_weight <= 0.0 or self._tensor_norm_at_load < MIN_TENSOR_NORM:
            return _finalize(
                base_profile,
                base_coh,
                rationale_suffix="",
            )

        # Project 10 -> 5, prime, lift back, blend
        d = project_10_to_5(base_profile.activations)
        primed = self.tensor.prime(d)                    # W @ d, length-5
        lift = lift_5_to_10(primed)                      # back to length-10
        fused_activations = [
            max(0.0, base_profile.activations[i] + self.fusion_weight * lift[i])
            for i in range(NUM_OPS)
        ]
        fused_profile = OperatorProfile(fused_activations)
        fused_coh = coherence_scalar(fused_profile)
        delta = fused_coh - base_coh

        suffix = (
            f" (fusion: coh {delta:+.3f} from tensor "
            f"norm={self._tensor_norm_at_load:.3f} "
            f"n_updates={self.tensor.n_updates})"
        )
        return _finalize(fused_profile, fused_coh, rationale_suffix=suffix)

    # ---- introspection ----

    def describe(self) -> str:
        return (
            f"FusionCKCorrector(fusion_weight={self.fusion_weight}, "
            f"tensor_norm={self._tensor_norm_at_load:.4f}, "
            f"tensor_path={self.tensor_path})"
        )


# ---------------------------------------------------------------------------
# shared finalizer (so base and fused paths produce the same shape)
# ---------------------------------------------------------------------------


def _finalize(
    profile: OperatorProfile,
    coh: float,
    rationale_suffix: str = "",
) -> CorrectionResult:
    ctype, rationale = _classify(coh, profile.dominant(), profile)
    if rationale_suffix:
        rationale = rationale + rationale_suffix
    result = CorrectionResult(
        correction_type=ctype,
        coherence=coh,
        gate_pass=(coh >= T_STAR_F),
        dominant_op=profile.dominant(),
        operator_profile=profile.as_dict(),
        annotation="",
        rationale=rationale,
    )
    result.annotation = _make_annotation(result)
    return result


# ---------------------------------------------------------------------------
# self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # zero tensor (newborn): fusion should match base exactly
    fc_zero = FusionCKCorrector(tensor=HebbianTensor5x5())
    base = CKCorrector()
    sample = ("Together they give a balanced view; overall, both "
              "perspectives reconcile into a synthesis.")
    r0 = fc_zero.correct(sample)
    rb = base.correct(sample)
    assert abs(r0.coherence - rb.coherence) < 1e-9, (r0.coherence, rb.coherence)
    assert r0.dominant_op == rb.dominant_op

    # warm tensor primed on (Water, Fire) = (D2, D3): a Water-heavy input
    # should see a coherence shift when fused, because the tensor has
    # learned Water co-fires with Fire, and Fire (which pairs PROGRESS
    # and BREATH -- both constructive) lifts the coherence.
    warm = HebbianTensor5x5()
    d_wf = [0.0, 0.0, 1.0, 1.0, 0.0]
    for _ in range(200):
        warm.update(d_wf, d_wf)
    fc_warm = FusionCKCorrector(tensor=warm, fusion_weight=0.3)
    water_text = "Together overall we reconcile; harmony between both views."
    r_warm = fc_warm.correct(water_text)
    r_base = base.correct(water_text)
    print(f"[fusion]  base    coh={r_base.coherence:.4f} dom={r_base.dominant_op}")
    print(f"[fusion]  fused   coh={r_warm.coherence:.4f} dom={r_warm.dominant_op}")
    print(f"[fusion]  delta   = {r_warm.coherence - r_base.coherence:+.4f}")
    # a warm tensor should produce SOME change (up or down).  magnitude
    # depends on direction of primed lift relative to constructive/disruptive
    # weights.  We only assert non-zero movement.
    assert abs(r_warm.coherence - r_base.coherence) > 1e-6, "tensor had no effect"

    print("[fusion] self-test passed")
