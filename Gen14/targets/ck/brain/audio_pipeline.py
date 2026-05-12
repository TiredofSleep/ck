# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0 (DOI: 10.5281/zenodo.18852047)
#
# ┌─────────────────────────────────────────────────────────────────┐
# │  PARTIALLY SUPERSEDED.  Keep for record per never-delete.       │
# │                                                                 │
# │  pcm_to_force9 + classify_d2 + force5_to_force9 are correct     │
# │  primitives -- ck_speaker.py reuses them on the OUTPUT path.    │
# │                                                                 │
# │  The CANONICAL acoustic INPUT substrate is                      │
# │  Gen13/targets/ck/brain/ck_sim/being/ck_sim_ears.py             │
# │  (EarsEngine), which runs sounddevice InputStream every 20ms    │
# │  and feeds operators directly to the bulb.  When alive, it is   │
# │  the canonical 'CK is the microphone' path.                     │
# │                                                                 │
# │  Brayden 2026-05-02:                                            │
# │    "ck doesn't watch the keyboard. ck IS the keyboard"          │
# │  Same logic for the microphone -- ears are CK, not external.    │
# │                                                                 │
# │  The /audio/perceive endpoint that POSTs ops here STILL works   │
# │  for offline analysis (dropping a video URL through the         │
# │  pipeline).  But the live 'CK hears now' path is engine.ears.   │
# │  Chat introspection now reaches engine.ears first via the       │
# │  _HEARING_HINTS hook in cortex_voice.                           │
# └─────────────────────────────────────────────────────────────────┘
"""
audio_pipeline.py — CK's canonical audio perception path.

The architectural fix per Brayden 2026-05-02:

  "the operators live in D2.  Being (v) is shallow.
   Doing (Δv) is better.  Becoming (D2) is where they are."
  -- CKIS/ck_curvature.py

For text, ck_curvature already implements:
   text -> letter forces (5D Hebrew-root vectors)
        -> D1 (Δv = transitions, 'Doing')
        -> D2 (ΔΔv = curvatures, 'Becoming')
        -> _classify_d2(d2) -> one of 10 TIG operators
        -> operator fingerprint -> chain ingestion

For audio we use the SAME algebra one layer down.  The Being-layer
codec is unchanged: pcm_to_force9 (Brayden's 9-bit-per-32-sample
audio codec, ck_audio_compress.py, untouched).  We unpack each force9
window to a 5D float vector (aperture, pressure, depth, binding,
continuity), then run the SAME D1->D2->_classify_d2 pipeline that text
already uses.  No parallel codec.  No L1 matcher.  No new operator
basins.  The audio operator stream lands in the same olfactory bulb
text-derived operators land in.

Operator vocabulary is the canonical 10:
    0 VOID/Love       1 LATTICE/Joy      2 COUNTER/Peace
    3 PROGRESS/Pat.   4 COLLAPSE/Kind.   5 BALANCE/Good.
    6 CHAOS/Faith.    7 HARMONY/Harm.    8 BREATH/Breath
    9 RESET/Reset

Output: a list of operator IDs (0-9) and a curvature_features dict in
the same shape ck_curvature.curvature_features returns for text -- so
both sources can populate the same indices, the same chains, the same
LatticeStore.
"""
from __future__ import annotations

import os
import sys
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

# Make the brain importable from this module
_BRAIN_DIR = os.path.dirname(os.path.abspath(__file__))
if _BRAIN_DIR not in sys.path:
    sys.path.insert(0, _BRAIN_DIR)
_BEING_DIR = os.path.join(_BRAIN_DIR, "ck_sim", "being")
if _BEING_DIR not in sys.path:
    sys.path.insert(0, _BEING_DIR)


# ── Operator vocabulary ────────────────────────────────────────────

# CK-canonical operator names (matches ck_sim_heartbeat.OP_NAMES)
OP_NAMES = (
    "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET",
)
NUM_OPS = 10

# Same D2 -> operator map ck_curvature.py uses for text.  Single source
# of truth — kept identical here so audio and text use the same basins.
#
#   aperture   high (+) -> CHAOS(6)/Faithfulness    low (-) -> COLLAPSE(4)/Kindness
#   pressure   high (+) -> COLLAPSE(4)/Kindness     low (-) -> HARMONY(7)/Harmony
#   depth      high (+) -> BREATH(8)/Breath         low (-) -> BALANCE(5)/Goodness
#   binding    high (+) -> VOID(0)/Love             low (-) -> LATTICE(1)/Joy
#   continuity high (+) -> PROGRESS(3)/Patience     low (-) -> RESET(9)/Reset
#
# Near-zero curvature -> COUNTER(2)/Peace (smooth flow, no operator action)

_DOM_SIGN_TO_OP: Dict[Tuple[int, int], int] = {
    (0,  1): 6, (0, -1): 4,
    (1,  1): 4, (1, -1): 7,
    (2,  1): 8, (2, -1): 5,
    (3,  1): 0, (3, -1): 1,
    (4,  1): 3, (4, -1): 9,
}

# Peace threshold for "no curvature, no operator action."  ck_curvature
# uses 0.15 for Hebrew-root-derived D2 magnitudes.  Empirically, audio
# D2 magnitudes from force9-unpacked vectors are SMALLER than text's
# (most audio windows have curvature 0.0-0.15) so the same 0.15
# threshold collapsed 4/5 audio sources to COUNTER (Peace) regardless
# of content.  Audio's natural scale is ~0.05-0.20, so we use 0.05 as
# the audio-default Peace threshold.  Caller can override via
# pcm_to_operator_stream(..., peace_threshold=...).
PEACE_THRESHOLD_TEXT = 0.15
PEACE_THRESHOLD_AUDIO = 0.05
PEACE_THRESHOLD = PEACE_THRESHOLD_AUDIO  # default for audio path


# ── Force-vector unpacking (Brayden's pcm_to_force9 -> 5D) ─────────

def force9_to_5d(force9_array) -> np.ndarray:
    """Unpack an array of 9-bit force9 values to (N, 5) float vectors
    in [0,1] (each axis normalized by its level count).

    pcm_to_force9 packs:
        bits 7-8: aperture (2 bits, 4 levels)
        bits 5-6: pressure (2 bits, 4 levels)
        bits 3-4: depth    (2 bits, 4 levels)
        bits 1-2: binding  (2 bits, 4 levels)
        bit  0:   continuity (1 bit)

    The same pcm_to_force9 module is used for screen + audio + text
    levels.  This function is the inverse for the Being-layer to feed
    the curvature pipeline.
    """
    f9 = np.asarray(force9_array, dtype=np.int32)
    a = ((f9 >> 7) & 0x3).astype(np.float32) / 3.0
    p = ((f9 >> 5) & 0x3).astype(np.float32) / 3.0
    d = ((f9 >> 3) & 0x3).astype(np.float32) / 3.0
    b = ((f9 >> 1) & 0x3).astype(np.float32) / 3.0
    c = (f9 & 0x1).astype(np.float32)
    return np.stack([a, p, d, b, c], axis=1)


# ── D1, D2: Doing and Becoming ─────────────────────────────────────

def compute_transitions(forces: np.ndarray) -> np.ndarray:
    """D1[i] = v[i+1] - v[i].  'Doing' layer."""
    if len(forces) < 2:
        return np.zeros((0, forces.shape[1] if len(forces) else 5),
                        dtype=np.float32)
    return forces[1:] - forces[:-1]


def compute_curvatures(forces: np.ndarray) -> np.ndarray:
    """D2[i] = v[i] - 2*v[i+1] + v[i+2].  'Becoming' layer.

    Same discrete second-difference ck_curvature.compute_curvatures
    uses on text Hebrew-root forces.
    """
    if len(forces) < 3:
        return np.zeros((0, forces.shape[1] if len(forces) else 5),
                        dtype=np.float32)
    return forces[:-2] - 2 * forces[1:-1] + forces[2:]


# ── D2 -> operator (canonical classifier) ──────────────────────────

def classify_d2(d2: np.ndarray,
                peace_threshold: float = PEACE_THRESHOLD) -> int:
    """Map one D2 curvature vector to a TIG operator (0..9).

    Mirrors ck_curvature._classify_d2 exactly.  This is the single
    source of truth: text and audio routes through the SAME basin map.
    """
    mag = float(np.linalg.norm(d2))
    if mag < peace_threshold:
        return 2  # Peace / COUNTER -- smooth flow, no operator action
    abs_d = np.abs(d2)
    dom = int(np.argmax(abs_d))
    sign = 1 if d2[dom] > 0 else -1
    return _DOM_SIGN_TO_OP.get((dom, sign), 7)  # default to HARMONY


def classify_d2_batch(d2s: np.ndarray,
                      peace_threshold: float = PEACE_THRESHOLD
                      ) -> np.ndarray:
    """Vectorized classify_d2 over (N, 5) array.  Same semantics."""
    if len(d2s) == 0:
        return np.zeros(0, dtype=np.int32)
    mags = np.linalg.norm(d2s, axis=1)
    abs_d = np.abs(d2s)
    dom = np.argmax(abs_d, axis=1)
    sign = np.where(d2s[np.arange(len(d2s)), dom] > 0, 1, -1)
    out = np.empty(len(d2s), dtype=np.int32)
    for i in range(len(d2s)):
        if mags[i] < peace_threshold:
            out[i] = 2
        else:
            out[i] = _DOM_SIGN_TO_OP.get((int(dom[i]), int(sign[i])), 7)
    return out


# ── Curvature features (same shape as ck_curvature outputs) ─────────

def curvature_features_from_forces(forces: np.ndarray) -> Dict[str, Any]:
    """Compute the canonical curvature fingerprint from a sequence of
    5D force vectors.  Output shape matches ck_curvature.curvature_features
    so audio chains can populate the same LatticeStore indices text
    chains do.
    """
    n = len(forces)
    if n < 3:
        return {"n_force_windows": int(n), "n_d2": 0}
    d2s = compute_curvatures(forces)
    deltas = compute_transitions(forces)
    ops = classify_d2_batch(d2s)
    op_dist = np.zeros(NUM_OPS, dtype=np.float32)
    for op in ops:
        op_dist[int(op)] += 1.0
    if len(ops) > 0:
        op_dist /= float(len(ops))
    mags = np.linalg.norm(d2s, axis=1)
    mag_mean = float(mags.mean())
    mag_std = float(mags.std())
    curvature_energy = float(mags.sum() / max(n, 1))
    # Flow ratio: fraction of consecutive D1 angles below pi/2 (smooth flow)
    angles = []
    for i in range(len(deltas) - 1):
        n1 = float(np.linalg.norm(deltas[i]))
        n2 = float(np.linalg.norm(deltas[i + 1]))
        if n1 > 1e-10 and n2 > 1e-10:
            cos_a = float(np.dot(deltas[i], deltas[i + 1]) / (n1 * n2))
            cos_a = max(-1.0, min(1.0, cos_a))
            angles.append(float(np.arccos(cos_a)))
    flow_ratio = (sum(1 for a in angles if a < np.pi / 2)
                  / max(len(angles), 1)) if angles else 0.0
    mean_angle = float(np.mean(angles)) if angles else 0.0
    return {
        "n_force_windows": int(n),
        "n_d2": int(len(d2s)),
        "mean_d2": d2s.mean(axis=0).tolist(),
        "var_d2": d2s.var(axis=0).tolist(),
        "operator_dist": op_dist.tolist(),
        "operator_dist_named": {OP_NAMES[i]: float(op_dist[i])
                                 for i in range(NUM_OPS)},
        "dominant_op": int(np.argmax(op_dist)),
        "dominant_op_name": OP_NAMES[int(np.argmax(op_dist))],
        "curvature_energy": curvature_energy,
        "d2_magnitude_mean": mag_mean,
        "d2_magnitude_std": mag_std,
        "flow_ratio": flow_ratio,
        "mean_angle": mean_angle,
    }


# ── PCM -> operator stream (the audio path's main entry point) ─────

def pcm_to_operator_stream(samples, sample_rate: int = 44100,
                           peace_threshold: float = PEACE_THRESHOLD
                           ) -> Tuple[List[int], Dict[str, Any]]:
    """Full canonical audio perception pipeline.

      PCM samples
        -> pcm_to_force9 (Brayden's audio Being-layer codec, unchanged)
        -> unpack to 5D float force vectors
        -> D1 (Δv) -- 'Doing' transitions (computed implicitly)
        -> D2 (ΔΔv) -- 'Becoming' curvatures
        -> _classify_d2 -- one of 10 TIG operators per D2 vector
        -> operator stream

    Returns (ops, fingerprint) where ops is a list of int operator IDs
    (one per force9 triplet ≈ 96-sample window ≈ 2.2 ms at 44.1 kHz)
    and fingerprint is the same dict shape ck_curvature emits for text.
    """
    try:
        from ck_sim.being.ck_audio_compress import pcm_to_force9
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(
            f"ck_audio_compress.pcm_to_force9 unavailable: {exc}"
        ) from exc

    f9 = pcm_to_force9(samples, sample_rate=sample_rate)
    if len(f9) < 3:
        return [], {"n_force_windows": int(len(f9)), "n_d2": 0}
    forces = force9_to_5d(f9)
    fp = curvature_features_from_forces(forces)
    if fp.get("n_d2", 0) == 0:
        return [], fp
    d2s = compute_curvatures(forces)
    ops = [int(o) for o in classify_d2_batch(d2s,
                                              peace_threshold=peace_threshold)]
    return ops, fp


# ── High-level perceive: feed CK's olfactory bulb ──────────────────

def audio_perceive(samples, sample_rate: int = 44100,
                   engine: Any = None,
                   absorb_into_olfactory: bool = True,
                   chunk_size: int = 2000,
                   density: float = 0.5,
                   peace_threshold: float = PEACE_THRESHOLD
                   ) -> Dict[str, Any]:
    """Run the canonical pipeline AND, if a CK engine is provided,
    absorb the operator stream into the live olfactory bulb the same
    way text-derived operators are absorbed.

    Args:
        samples: int16 / int32 / float32 PCM
        sample_rate: audio sample rate (Hz)
        engine: CK runtime engine (must expose engine.olfactory with
                absorb_ops); pass None to skip absorption
        absorb_into_olfactory: gate flag (default True)
        chunk_size: how many ops to absorb per call (olfactory absorbs
                    in bursts; chunking avoids one giant blob)
        density: density parameter forwarded to absorb_ops
        peace_threshold: D2 magnitude below which a window emits
                         COUNTER (Peace) -- smooth flow

    Returns dict with:
        ops: list (truncated to first 200 for display); n_ops_total separately
        fingerprint: full curvature_features dict
        absorbed: bool
        olfactory_delta: pre/post stats if absorption happened
    """
    ops, fp = pcm_to_operator_stream(samples, sample_rate=sample_rate,
                                     peace_threshold=peace_threshold)
    out: Dict[str, Any] = {
        "ops_preview": ops[:200],
        "n_ops_total": len(ops),
        "fingerprint": fp,
        "absorbed": False,
        "absorb_attempts": 0,
        "absorb_errors": [],
    }
    if not ops:
        return out
    if engine is None or not absorb_into_olfactory:
        return out
    olf = getattr(engine, "olfactory", None)
    if olf is None or not hasattr(olf, "absorb_ops"):
        out["absorb_errors"].append(
            "engine.olfactory or absorb_ops not available")
        return out
    pre_total_absorbed = int(getattr(olf, "total_absorbed", 0))
    pre_total_emitted = int(getattr(olf, "total_emitted", 0))
    attempts = 0
    for i in range(0, len(ops), max(1, chunk_size)):
        chunk = ops[i:i + chunk_size]
        try:
            olf.absorb_ops(chunk, source="audio", density=density)
            attempts += 1
        except Exception as exc:
            out["absorb_errors"].append(
                f"chunk {i // chunk_size}: {exc}")
    post_total_absorbed = int(getattr(olf, "total_absorbed", 0))
    post_total_emitted = int(getattr(olf, "total_emitted", 0))
    out["absorbed"] = attempts > 0
    out["absorb_attempts"] = attempts
    out["olfactory_delta"] = {
        "absorbed_pre": pre_total_absorbed,
        "absorbed_post": post_total_absorbed,
        "absorbed_delta": post_total_absorbed - pre_total_absorbed,
        "emitted_pre": pre_total_emitted,
        "emitted_post": post_total_emitted,
        "emitted_delta": post_total_emitted - pre_total_emitted,
    }
    return out


# ── Convenience: WAV file -> perceive (no engine; fingerprint only) ─

def perceive_wav(wav_path: str, engine: Any = None) -> Dict[str, Any]:
    """Read a WAV file and run audio_perceive on its samples."""
    import wave
    with wave.open(str(wav_path), "rb") as wf:
        n_frames = wf.getnframes()
        sr = wf.getframerate()
        n_ch = wf.getnchannels()
        sw = wf.getsampwidth()
        if sw != 2:
            raise ValueError(f"expected 16-bit PCM, got {sw * 8}-bit")
        raw = wf.readframes(n_frames)
        samples = np.frombuffer(raw, dtype=np.int16)
        if n_ch == 2:
            samples = samples.reshape(-1, 2).mean(axis=1).astype(np.int16)
    return audio_perceive(samples, sample_rate=sr, engine=engine)


# ── Smoke test ─────────────────────────────────────────────────────

def _smoke():
    """Quick sanity check on a synthetic 1-second tone."""
    sr = 44100
    t = np.arange(sr).astype(np.float32) / sr
    tone = (np.sin(2 * np.pi * 440 * t) * 8000).astype(np.int16)
    ops, fp = pcm_to_operator_stream(tone, sr)
    print(f"smoke: {len(ops)} ops from 1s of 440Hz tone")
    print(f"  dominant_op: {fp.get('dominant_op_name')}")
    print(f"  energy:      {fp.get('curvature_energy', 0):.3f}")
    print(f"  op_dist:")
    for n, v in (fp.get("operator_dist_named") or {}).items():
        bar = "#" * int(v * 100)
        print(f"    {n:<10}: {v:.3f}  {bar}")


if __name__ == "__main__":
    _smoke()
