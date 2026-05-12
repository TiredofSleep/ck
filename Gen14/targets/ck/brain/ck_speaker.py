# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
"""
ck_speaker.py -- CK's voice as his own substrate rendered to audio.

NOT a TTS module.  TTS would synthesize audio from a text template.
This module synthesizes audio from CK's actual operator stream:
    operator stream
      -> reverse the canonical 5D classification (op_id -> 5D force)
      -> repack the 5D force into 9-bit force9
      -> ck_audio_compress.force9_to_pcm   (Brayden's lossy decoder)
      -> sounddevice playback to the default output device

The audio that comes out is what CK's substrate sounded like.  When
CK "speaks," what you hear IS his own force-vector trajectory rendered
as sound.  Different operator streams produce different timbres
because the canonical force vectors are different.

Brayden 2026-05-02:
  "he needs to be a speaker output"

This is the one piece that genuinely didn't exist yet.  pcm_to_force9
(input direction) and force9_to_pcm (output direction) both exist in
ck_audio_compress.  The forward path (audio in -> operator) has been
wired through the canonical pipeline.  This is the reverse: operator
stream -> audio out, through the same algebra.
"""
from __future__ import annotations

import os
import sys
import threading
from typing import Iterable, List, Optional, Sequence

import numpy as np

_BRAIN_DIR = os.path.dirname(os.path.abspath(__file__))
if _BRAIN_DIR not in sys.path:
    sys.path.insert(0, _BRAIN_DIR)
_BEING_DIR = os.path.join(_BRAIN_DIR, "ck_sim", "being")
if _BEING_DIR not in sys.path:
    sys.path.insert(0, _BEING_DIR)


# Canonical 10-op vocabulary (matches ck_sim_heartbeat.OP_NAMES)
OP_NAMES = (
    "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET",
)


# Canonical (a, b, c, d, e) Force5D representatives for each operator,
# in the [0, 1] range pcm_to_force9 emits.  Each operator dominates
# ONE dim and sits at the half on the others -- mirrors
# ck_olfactory.CANONICAL_FORCE.
_OP_TO_FORCE5 = {
    0: (0.50, 0.05, 0.50, 0.50, 0.50),  # VOID
    1: (0.05, 0.50, 0.50, 0.50, 0.50),  # LATTICE
    2: (0.50, 0.50, 0.50, 0.05, 0.50),  # COUNTER
    3: (0.50, 0.50, 0.95, 0.50, 0.50),  # PROGRESS
    4: (0.50, 0.95, 0.50, 0.50, 0.50),  # COLLAPSE
    5: (0.50, 0.50, 0.50, 0.50, 0.95),  # BALANCE
    6: (0.95, 0.50, 0.50, 0.50, 0.50),  # CHAOS
    7: (0.50, 0.50, 0.50, 0.95, 0.50),  # HARMONY
    8: (0.50, 0.50, 0.50, 0.50, 0.05),  # BREATH
    9: (0.50, 0.50, 0.05, 0.50, 0.50),  # RESET
}


def force5_to_force9(force5: Sequence[float]) -> int:
    """Pack a 5D float force in [0,1] back into the 9-bit force9 layout
    pcm_to_force9 produces:

        bits 7-8 aperture (2 bits, 4 levels)
        bits 5-6 pressure (2 bits, 4 levels)
        bits 3-4 depth    (2 bits, 4 levels)
        bits 1-2 binding  (2 bits, 4 levels)
        bit  0   continuity (1 bit)
    """
    a, p, d, b, c = force5
    qa = int(round(max(0, min(1, a)) * 3)) & 0x3
    qp = int(round(max(0, min(1, p)) * 3)) & 0x3
    qd = int(round(max(0, min(1, d)) * 3)) & 0x3
    qb = int(round(max(0, min(1, b)) * 3)) & 0x3
    qc = 1 if c >= 0.5 else 0
    return ((qa << 7) | (qp << 5) | (qd << 3) | (qb << 1) | qc)


def operator_stream_to_force9(ops: Iterable[int]) -> np.ndarray:
    """Map an operator stream back to a force9 array via canonical
    OPS_TO_FORCE5.  One force9 window per operator."""
    out = np.empty(0, dtype=np.uint16)
    out_list = []
    for op in ops:
        op = int(op) % 10
        f5 = _OP_TO_FORCE5[op]
        out_list.append(force5_to_force9(f5))
    if out_list:
        out = np.array(out_list, dtype=np.uint16)
    return out


def operator_stream_to_pcm(ops: Iterable[int],
                            sample_rate: int = 44100) -> np.ndarray:
    """Full reverse path: operator stream -> force9 -> PCM samples.

    Each operator becomes one 32-sample window of audio (~0.7ms at
    44.1kHz).  A second of audio = ~1,400 operators.  That's why
    CK's voice modulates so finely -- each operator change shifts
    the audio character within ~ms.
    """
    from ck_audio_compress import force9_to_pcm
    f9 = operator_stream_to_force9(ops)
    if len(f9) == 0:
        return np.zeros(0, dtype=np.int16)
    return force9_to_pcm(f9, sample_rate=sample_rate)


# ── Output: speak the stream through the default audio device ──────

_HAS_SD = None

def _ensure_sounddevice():
    global _HAS_SD
    if _HAS_SD is None:
        try:
            import sounddevice as _sd  # noqa: F401
            _HAS_SD = True
        except Exception:
            _HAS_SD = False
    return _HAS_SD


def speak_operator_stream(ops: Iterable[int],
                           sample_rate: int = 44100,
                           blocking: bool = True) -> dict:
    """Render an operator stream to PCM and play it through the
    default sound device.

    Returns dict with n_ops, duration_sec, played (bool), error (opt).
    blocking=True waits for playback to finish; False returns immediately.
    """
    pcm = operator_stream_to_pcm(ops, sample_rate=sample_rate)
    if len(pcm) == 0:
        return {"n_ops": 0, "duration_sec": 0.0, "played": False,
                "error": "empty stream"}
    duration = len(pcm) / sample_rate
    if not _ensure_sounddevice():
        return {"n_ops": len(list(ops)) if hasattr(ops, "__len__")
                else None,
                "duration_sec": duration, "played": False,
                "error": "sounddevice not available; no audio output"}
    import sounddevice as sd
    try:
        # sd.play takes float [-1,1] OR int16 [-32768,32767]
        sd.play(pcm, samplerate=sample_rate, blocking=blocking)
        if blocking:
            sd.wait()
        return {"n_ops": int(len(pcm) // 32),
                "duration_sec": duration, "played": True}
    except Exception as exc:
        return {"n_ops": int(len(pcm) // 32),
                "duration_sec": duration,
                "played": False, "error": str(exc)}


def speak_text_as_operators(text: str,
                              sample_rate: int = 44100) -> dict:
    """Bridge: take TEXT, run it through CK's text curvature pipeline
    to get an operator sequence, then SPEAK that operator sequence as
    audio through CK's reverse codec.  Round-trip:
        text -> letter_force -> D2 -> classify_d2 -> ops -> force9 -> PCM
    The audio is what the text SOUNDS LIKE in CK's substrate.  Not a
    TTS rendering of the words; an audio rendering of the operator
    trajectory the words traced.
    """
    try:
        # ck_curvature lives in CKIS for the formal TIG distribution
        sys.path.insert(0, os.path.join(
            os.path.dirname(_BRAIN_DIR), "..", "..", "..", "CKIS"))
        from ck_curvature import operator_sequence as _opseq
    except Exception:
        # Fallback: project text through the audio_pipeline classifier
        # using a simple letter-position vector (audio-grade approx)
        try:
            from audio_pipeline import classify_d2_batch
        except Exception:
            return {"error": "no operator classifier available"}
        # naive 5D per char then D2
        chars = [c.lower() for c in text if c.isalpha()]
        if len(chars) < 3:
            return {"n_ops": 0, "duration_sec": 0.0, "played": False,
                    "error": "text too short"}
        pos = np.array(
            [[ord(c) - ord("a"), len(c.encode()), (ord(c) % 7) / 6,
              (ord(c) % 5) / 4, ord(c) % 2] for c in chars],
            dtype=np.float32) / 26.0
        d2 = pos[:-2] - 2 * pos[1:-1] + pos[2:]
        ops = list(classify_d2_batch(d2))
    else:
        ops = [op_idx for op_idx, _ in _opseq(text)]
    return speak_operator_stream(ops, sample_rate=sample_rate)


# ── Smoke test ─────────────────────────────────────────────────────

def _smoke():
    """Render each operator alone for ~0.2s -- you should hear ten
    distinct timbres, one per operator."""
    print("CK speaker smoke test -- 10 operators, 0.2s each")
    for op in range(10):
        ops = [op] * 280  # 280 windows * 32 samples / 44.1kHz ~= 0.2s
        res = speak_operator_stream(ops, blocking=True)
        print(f"  op {op:2} {OP_NAMES[op]:<10}: "
              f"{res.get('duration_sec', 0):.2f}s "
              f"played={res.get('played')} "
              + (f"err={res.get('error')}" if res.get('error') else ""))


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--smoke", action="store_true")
    p.add_argument("--text", help="say this text in CK's substrate voice")
    p.add_argument("--ops",
                   help="comma-separated op ids (0..9) to speak as a stream")
    a = p.parse_args()
    if a.smoke:
        _smoke()
    elif a.text:
        r = speak_text_as_operators(a.text)
        print(r)
    elif a.ops:
        ops = [int(x) for x in a.ops.split(",") if x.strip()]
        r = speak_operator_stream(ops)
        print(r)
    else:
        _smoke()
