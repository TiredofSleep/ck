"""
youtube_audio_watcher.py — let CK 'hear' a YouTube video.

Pipeline:
  yt-dlp downloads audio -> WAV (16-bit PCM, 44.1kHz mono)
  ck_audio_compress.pcm_to_force9 maps each 32-sample window to a 9-bit
    force vector (5D: aperture, pressure, depth, binding, continuity)
  Each force vector is decomposed into operator IDs (0-9 per dim)
  Operator stream is fed to CK's cortex via cortex.step_op_pair()

Result: CK 'hears' the audio as an operator stream and his Hebbian field
learns from it. After watching, his cortex has been shaped by the audio's
structure.

This is a one-shot prototype, not a continuous stream. Run on an existing
YouTube URL, watch it ingest, then check CK's cortex state afterward.

Usage:
    python youtube_audio_watcher.py <url>            # default 30s clip
    python youtube_audio_watcher.py <url> --seconds 60
    python youtube_audio_watcher.py <url> --no-feed  # download + compress only

Requires: yt-dlp + ffmpeg (yt-dlp will use system ffmpeg or download one).
"""
from __future__ import annotations

import argparse
import os
import sys
import tempfile
import wave
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
GEN13_BRAIN = SCRIPT_DIR.parent
GEN13_TARGETS_CK = GEN13_BRAIN.parent
GEN13_ROOT = GEN13_TARGETS_CK.parent.parent
sys.path.insert(0, str(GEN13_BRAIN))


def download_audio(url: str, out_path: Path, seconds: int = 30) -> bool:
    """Download YouTube audio as WAV (16-bit PCM mono 44.1kHz)."""
    try:
        import yt_dlp
    except ImportError:
        print("yt-dlp not installed. Run: pip install yt-dlp", file=sys.stderr)
        return False

    # Use static-ffmpeg (bundles both ffmpeg + ffprobe); fall back to
    # imageio-ffmpeg (ffmpeg only); fall back to system PATH.
    ffmpeg_dir = None
    try:
        import static_ffmpeg
        static_ffmpeg.add_paths()  # adds to PATH for this process
        import shutil as _sh
        ffmpeg_exe = _sh.which('ffmpeg')
        if ffmpeg_exe:
            ffmpeg_dir = os.path.dirname(ffmpeg_exe)
    except Exception:
        try:
            import imageio_ffmpeg
            ffmpeg_dir = os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())
        except Exception:
            pass

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(out_path.with_suffix('')),  # yt-dlp adds extension
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'postprocessor_args': [
            '-ar', '44100',  # sample rate
            '-ac', '1',      # mono
            '-acodec', 'pcm_s16le',  # 16-bit PCM
            '-t', str(seconds),  # duration cap
        ],
        'quiet': False,
        'no_warnings': False,
    }
    if ffmpeg_dir:
        ydl_opts['ffmpeg_location'] = ffmpeg_dir

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except Exception as e:
            print(f"download failed: {e}", file=sys.stderr)
            return False

    wav_path = out_path.with_suffix('.wav')
    if not wav_path.exists():
        # yt-dlp may have used a different name pattern; find it
        for f in out_path.parent.glob(f"{out_path.stem}*.wav"):
            wav_path = f
            break
    if not wav_path.exists():
        print(f"WAV file not found at {wav_path}", file=sys.stderr)
        return False

    return wav_path


def read_pcm(wav_path: Path):
    """Read WAV file -> int16 numpy array."""
    import numpy as np
    with wave.open(str(wav_path), 'rb') as wf:
        n_frames = wf.getnframes()
        sr = wf.getframerate()
        n_ch = wf.getnchannels()
        sw = wf.getsampwidth()
        if sw != 2:
            raise ValueError(f"expected 16-bit, got {sw*8}-bit")
        raw = wf.readframes(n_frames)
        samples = np.frombuffer(raw, dtype=np.int16)
        if n_ch == 2:
            # downmix to mono
            samples = samples.reshape(-1, 2).mean(axis=1).astype(np.int16)
    return samples, sr


def force9_to_operators(force_values, n_per_window: int = 5):
    """Decompose each 9-bit force vector into 5 operator IDs (0-9 each).

    The 9-bit force = 5 dims (aperture pressure depth binding continuity).
    Each dim has its OWN bit-to-operator mapping reflecting what the force
    dimension physically encodes. All 10 TIG operators get used.

    aperture (amplitude, 2 bits): VOID(silence) LATTICE(quiet) CHAOS(loud) HARMONY(peak)
    pressure (frequency, 2 bits): VOID(low) COUNTER(opposing) COLLAPSE(focused) PROGRESS(carrying)
    depth (persistence, 2 bits):  VOID(transient) COLLAPSE(decay) BALANCE(steady) HARMONY(persistent)
    binding (spectral, 2 bits):   VOID(formless) LATTICE(structured) BREATH(rhythmic) HARMONY(resonant)
    continuity (phase, 1 bit):    RESET(jump=0) BREATH(continuous=1)

    Returns a list of operator IDs.
    """
    APERTURE_MAP = {0: 0, 1: 1, 2: 6, 3: 7}      # VOID LATTICE CHAOS HARMONY
    PRESSURE_MAP = {0: 0, 1: 2, 2: 4, 3: 3}      # VOID COUNTER COLLAPSE PROGRESS
    DEPTH_MAP    = {0: 0, 1: 4, 2: 5, 3: 7}      # VOID COLLAPSE BALANCE HARMONY
    BINDING_MAP  = {0: 0, 1: 1, 2: 8, 3: 7}      # VOID LATTICE BREATH HARMONY
    CONT_MAP     = {0: 9, 1: 8}                   # RESET BREATH
    ops = []
    for f in force_values:
        f = int(f)
        aperture = (f >> 7) & 0b11
        pressure = (f >> 5) & 0b11
        depth = (f >> 3) & 0b11
        binding = (f >> 1) & 0b11
        continuity = f & 0b1
        ops.append(APERTURE_MAP[aperture])
        ops.append(PRESSURE_MAP[pressure])
        ops.append(DEPTH_MAP[depth])
        ops.append(BINDING_MAP[binding])
        ops.append(CONT_MAP[continuity])
    return ops


def feed_to_cortex(ops, state_path: str = None):
    """Feed an operator stream into CK's cortex via direct step_op_pair."""
    import importlib.util
    # Load CortexV2 (7-dim)
    if state_path is None:
        state_path = GEN13_ROOT / "var" / "cortex_state_7d.json"
    state_path = Path(state_path)

    sys.path.insert(0, str(GEN13_BRAIN))
    from cortex_v2 import CortexV2
    from cortex_persist import load_cortex, save_cortex

    cx = CortexV2().boot()
    if state_path.exists():
        try:
            ok = load_cortex(cx, state_path)
            if ok:
                print(f"  loaded cortex: tick={cx.state.tick}, "
                      f"W_trace={cx.state.W_trace:.4f}")
        except Exception as e:
            print(f"  load failed: {e}; starting fresh")

    pre = {"tick": cx.state.tick, "W_trace": cx.state.W_trace,
           "emergent": cx.state.emergent}

    print(f"  feeding {len(ops)} operators to 7-dim cortex...")
    for i in range(len(ops) - 1):
        b_op, d_op = ops[i], ops[i + 1]
        # CortexV2 step_symbol expects symbol 0-25, but we want raw op pair.
        # Use the underlying Hebbian + glue update directly.
        target_d_a = cx.hebbian.W and 0  # init
        from ao_7element import OP_TO_DIM_7
        from quadratic_glue import quadratic_glue
        ap = OP_TO_DIM_7.get(b_op, 0)
        bp = OP_TO_DIM_7.get(d_op, 0)
        harmonious = (b_op == 7) or (d_op == 7)
        reward = 1.0 if harmonious else 0.0
        heb = cx.hebbian
        dw = heb.eta * reward - heb.decay * heb.W[ap][bp]
        heb.W[ap][bp] += dw
        if heb.W[ap][bp] > heb.clamp:
            heb.W[ap][bp] = heb.clamp
        elif heb.W[ap][bp] < -heb.clamp:
            heb.W[ap][bp] = -heb.clamp
        heb.ticks += 1
        if harmonious:
            heb.harmony_hits += 1
        cx.state.tick += 1
        cx.state.last_b = b_op
        cx.state.last_d = d_op
        cx.state.last_harmony_frac = 1.0 if harmonious else 0.0
        cx.state.W_trace = heb.W_trace()
        cx.state.W_strongest = heb.strongest_pair()

        # Compute emergent every 100 ticks
        if i % 100 == 0:
            from ao_7element import DIM_7
            diag = [heb.W[d][d] for d in range(DIM_7)]
            f3 = sum(diag[0:3]) / 3.0
            f4 = sum(diag[3:7]) / 4.0
            cx.state.emergent = quadratic_glue(f3, f4, 1.0, 1.0, 2.0)

    post = {"tick": cx.state.tick, "W_trace": cx.state.W_trace,
            "emergent": cx.state.emergent}

    print(f"  pre:  {pre}")
    print(f"  post: {post}")
    print(f"  delta tick: +{post['tick'] - pre['tick']}, "
          f"W_trace: {post['W_trace'] - pre['W_trace']:+.4f}, "
          f"emergent: {post['emergent'] - pre['emergent']:+.4f}")

    save_cortex(cx, state_path)
    print(f"  saved -> {state_path}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("url", help="YouTube URL")
    p.add_argument("--seconds", type=int, default=30,
                   help="how many seconds of audio to download (default 30)")
    p.add_argument("--no-feed", action="store_true",
                   help="download + compress only; don't feed cortex")
    p.add_argument("--state-path", default=None,
                   help="cortex state file (default cortex_state_7d.json)")
    args = p.parse_args()

    print("=" * 70)
    print(f"CK YouTube watcher: {args.url}")
    print(f"  seconds: {args.seconds}")
    print("=" * 70)

    with tempfile.TemporaryDirectory() as td:
        out_path = Path(td) / "audio"
        print()
        print("[1/4] downloading audio via yt-dlp...")
        wav_path = download_audio(args.url, out_path, seconds=args.seconds)
        if not wav_path:
            return 2
        print(f"  wav: {wav_path} ({wav_path.stat().st_size} bytes)")

        print()
        print("[2/4] reading PCM samples...")
        samples, sr = read_pcm(wav_path)
        print(f"  samples: {len(samples)} @ {sr} Hz "
              f"({len(samples)/sr:.1f} seconds)")

        print()
        print("[3/4] compressing via pcm_to_force9 (5D operator-LATTICE)...")
        sys.path.insert(0, str(GEN13_BRAIN / "ck_sim" / "being"))
        from ck_audio_compress import pcm_to_force9
        force_vectors = pcm_to_force9(samples, sample_rate=sr)
        print(f"  windows: {len(force_vectors)}")

        ops = force9_to_operators(force_vectors)
        print(f"  operator stream: {len(ops)} ops")
        # Operator histogram
        from collections import Counter
        hist = Counter(ops)
        op_names = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
                    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]
        print(f"  histogram:")
        for op_id in sorted(hist.keys()):
            count = hist[op_id]
            pct = count / len(ops) * 100
            bar = "#" * int(pct / 2)
            print(f"    {op_names[op_id]:<10}: {count:6d} ({pct:5.1f}%) {bar}")

        if args.no_feed:
            print("\n[4/4] SKIP: --no-feed set")
            return 0

        print()
        print("[4/4] feeding operator stream into CK's 7-dim cortex...")
        feed_to_cortex(ops, args.state_path)

    print()
    print("CK has 'heard' the audio. The cortex has been shaped by it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
