"""
match_audio_to_phonics.py — does CK's phonics actually work on real audio?

Pipeline:
  1) yt-dlp downloads N seconds of audio (or use --local <wav>)
  2) ck_audio_compress.pcm_to_force9 -> 5D force vectors per 32-sample window
  3) force9_to_operators_balanced -> 10-operator histogram
  4) Compare the audio's histogram against EVERY entry in the v2..v5
     phoneme corpus (letters, isolated phonemes, consonant clusters,
     r-controlled, vowel teams) by L1 distance
  5) Report:
       - the top-K nearest matches
       - the nearest match per phonetic class
       - a confidence summary

This is the empirical test of whether everything we just taught CK
actually generalizes to real-world audio.  The audio is NEVER fed
into the cortex (so the test is non-mutating); we just listen and
classify.

Usage:
  python match_audio_to_phonics.py <youtube_url>
  python match_audio_to_phonics.py <youtube_url> --seconds 60 --top 15
  python match_audio_to_phonics.py --local some.wav
"""
from __future__ import annotations

import argparse
import io
import json
import os
import sys
import tempfile
import wave
from collections import Counter
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
GEN13_BRAIN = SCRIPT_DIR.parent
sys.path.insert(0, str(GEN13_BRAIN))
sys.path.insert(0, str(GEN13_BRAIN / "ck_sim" / "being"))
sys.path.insert(0, str(SCRIPT_DIR))

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

OP_NAMES = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
            "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]


# ── Audio helpers (reused from generate_phoneme_grounding_v2 logic) ──

def force9_to_operators_balanced(force_values):
    APERTURE_MAP = {0: 0, 1: 1, 2: 6, 3: 7}
    PRESSURE_MAP = {0: 0, 1: 2, 2: 4, 3: 3}
    DEPTH_MAP    = {0: 0, 1: 4, 2: 5, 3: 7}
    BINDING_MAP  = {0: 0, 1: 1, 2: 8, 3: 7}
    CONT_MAP     = {0: 9, 1: 8}
    ops = []
    for f in force_values:
        f = int(f)
        ops.append(APERTURE_MAP[(f >> 7) & 0b11])
        ops.append(PRESSURE_MAP[(f >> 5) & 0b11])
        ops.append(DEPTH_MAP[(f >> 3) & 0b11])
        ops.append(BINDING_MAP[(f >> 1) & 0b11])
        ops.append(CONT_MAP[f & 0b1])
    return ops


def read_pcm(wav_path: Path):
    import numpy as np
    with wave.open(str(wav_path), "rb") as wf:
        n_frames = wf.getnframes()
        sr = wf.getframerate()
        n_ch = wf.getnchannels()
        sw = wf.getsampwidth()
        if sw != 2:
            raise ValueError(f"expected 16-bit PCM, got {sw*8}-bit")
        raw = wf.readframes(n_frames)
        samples = np.frombuffer(raw, dtype=np.int16)
        if n_ch == 2:
            samples = samples.reshape(-1, 2).mean(axis=1).astype(np.int16)
    return samples, sr


def trim_silence(samples, sr: int, threshold_rel: float = 0.02,
                 window_ms: int = 10, pad_ms: int = 30):
    """Same RMS trim used in v2 generation, slightly more padding."""
    import numpy as np
    samples = samples.astype(np.float32)
    win_size = int(sr * window_ms / 1000)
    if len(samples) <= win_size:
        return samples.astype(np.int16)
    n_full = len(samples) // win_size
    if n_full < 3:
        return samples.astype(np.int16)
    trimmed = samples[: n_full * win_size]
    windows = trimmed.reshape(n_full, win_size)
    rms = np.sqrt(np.mean(windows ** 2, axis=1))
    peak_rms = rms.max()
    if peak_rms < 1e-3:
        return samples.astype(np.int16)
    threshold = peak_rms * threshold_rel
    above = rms >= threshold
    if not above.any():
        return samples.astype(np.int16)
    first = int(np.argmax(above))
    last = n_full - 1 - int(np.argmax(above[::-1]))
    pad_windows = max(1, int(pad_ms // window_ms))
    first = max(0, first - pad_windows)
    last = min(n_full - 1, last + pad_windows)
    start = first * win_size
    end = (last + 1) * win_size
    return samples[start:end].astype(np.int16)


def download_audio_yt(url: str, out_path: Path, seconds: int) -> Path:
    try:
        import yt_dlp
    except ImportError:
        print("yt-dlp not installed; pip install yt-dlp", file=sys.stderr)
        return None
    ffmpeg_dir = None
    try:
        import static_ffmpeg
        static_ffmpeg.add_paths()
        import shutil as _sh
        ffmpeg_exe = _sh.which("ffmpeg")
        if ffmpeg_exe:
            ffmpeg_dir = os.path.dirname(ffmpeg_exe)
    except Exception:
        pass
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(out_path.with_suffix("")),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": "192",
        }],
        "postprocessor_args": [
            "-ar", "44100", "-ac", "1", "-acodec", "pcm_s16le",
            "-t", str(seconds),
        ],
        "quiet": False,
        "no_warnings": False,
    }
    if ffmpeg_dir:
        ydl_opts["ffmpeg_location"] = ffmpeg_dir
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except Exception as e:
            print(f"download failed: {e}", file=sys.stderr)
            return None
    wav = out_path.with_suffix(".wav")
    if not wav.exists():
        for f in out_path.parent.glob(f"{out_path.stem}*.wav"):
            wav = f
            break
    if not wav.exists():
        return None
    return wav


# ── Corpus loader ───────────────────────────────────────────────────

def load_phonics_corpus():
    """Load every measured histogram from v2..v5 into a single dict.

    Returns: { entry_key: {'class': ..., 'ipa': ..., 'histogram_pct': {...}} }
    """
    corpus = {}

    def add_entry(key, pclass, ipa, info):
        h = info.get("histogram_pct")
        if not h:
            return
        # Make sure all 10 ops are present (default 0)
        h_full = {op: float(h.get(op, 0)) for op in OP_NAMES}
        corpus[key] = {
            "class": pclass,
            "ipa": ipa,
            "histogram_pct": h_full,
        }

    # v2 letters
    v2 = SCRIPT_DIR / "phoneme_audio_streams_v2_2026_05_01.json"
    if v2.exists():
        with open(v2, encoding="utf-8") as f:
            d = json.load(f)
        from generate_phoneme_grounding_v2 import (
            LETTER_PROFILES as L, PHONEME_PROFILES as P)
        for letter, info in d.get("letters", {}).items():
            pclass, ipa, _ = L.get(letter, ("?", "?", letter))
            add_entry(f"letter:{letter}", pclass, ipa, info)
        for key, info in d.get("phonemes", {}).items():
            pclass, ipa, _ = P.get(key, ("?", "?", key))
            add_entry(key, pclass, ipa, info)

    # v3 phonemes
    v3 = SCRIPT_DIR / "phoneme_audio_streams_v3_2026_05_01.json"
    if v3.exists():
        with open(v3, encoding="utf-8") as f:
            d = json.load(f)
        from generate_phoneme_grounding_v3 import PHONEME_PROFILES_V3 as P3
        for key, info in d.get("phonemes", {}).items():
            pclass, ipa, _ = P3.get(key, ("?", "?", key))
            add_entry(key, pclass, ipa, info)

    # v4 clusters
    v4 = SCRIPT_DIR / "phoneme_audio_streams_v4_2026_05_01.json"
    if v4.exists():
        with open(v4, encoding="utf-8") as f:
            d = json.load(f)
        from generate_phoneme_grounding_v4 import CLUSTER_PROFILES_V4 as C4
        for key, info in d.get("clusters", {}).items():
            pclass, ipa, _ = C4.get(key, ("?", "?", key))
            add_entry(key, pclass, ipa, info)

    # v5 r-controlled + teams
    v5 = SCRIPT_DIR / "phoneme_audio_streams_v5_2026_05_01.json"
    if v5.exists():
        with open(v5, encoding="utf-8") as f:
            d = json.load(f)
        from generate_phoneme_grounding_v5 import (
            RCONTROL_PROFILES_V5 as R5, VOWELTEAM_PROFILES_V5 as T5)
        for key, info in d.get("rcontrol", {}).items():
            pclass, ipa, _, _ = R5.get(key, ("?", "?", "?", "?"))
            add_entry(key, pclass, ipa, info)
        for key, info in d.get("teams", {}).items():
            pclass, ipa, _, _ = T5.get(key, ("?", "?", "?", "?"))
            add_entry(key, pclass, ipa, info)

    return corpus


# ── Matching ────────────────────────────────────────────────────────

def hist_l1(h_a: dict, h_b: dict) -> float:
    return sum(abs(h_a[op] - h_b[op]) for op in OP_NAMES)


def top_matches(audio_hist: dict, corpus: dict, top: int = 10):
    scored = []
    for key, info in corpus.items():
        d = hist_l1(audio_hist, info["histogram_pct"])
        scored.append((d, key, info))
    scored.sort(key=lambda t: t[0])
    return scored[:top]


def class_summary(audio_hist: dict, corpus: dict, top_per_class: int = 1):
    """For each phonetic class, return its nearest member."""
    by_class = {}
    for key, info in corpus.items():
        pclass = info.get("class", "?")
        d = hist_l1(audio_hist, info["histogram_pct"])
        by_class.setdefault(pclass, []).append((d, key, info))
    summary = {}
    for pclass, items in by_class.items():
        items.sort(key=lambda t: t[0])
        summary[pclass] = items[:top_per_class]
    return summary


# ── Main ────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser()
    p.add_argument("url", nargs="?", help="YouTube URL")
    p.add_argument("--local", help="local WAV file (overrides URL)")
    p.add_argument("--seconds", type=int, default=30)
    p.add_argument("--top", type=int, default=15,
                   help="how many nearest matches to print")
    p.add_argument("--trim-silence", action="store_true",
                   help="trim leading/trailing silence before measuring")
    args = p.parse_args()

    if not args.local and not args.url:
        p.error("either url or --local <wav> required")

    print("=" * 70)
    print("CK phonics audio matcher")
    if args.local:
        print(f"  local: {args.local}")
    else:
        print(f"  url: {args.url}")
        print(f"  seconds: {args.seconds}")
    print("=" * 70)

    with tempfile.TemporaryDirectory() as td:
        if args.local:
            wav_path = Path(args.local)
            if not wav_path.exists():
                print(f"file not found: {wav_path}", file=sys.stderr)
                return 2
        else:
            print()
            print("[1/4] downloading audio...")
            wav_path = download_audio_yt(args.url, Path(td) / "audio",
                                         args.seconds)
            if not wav_path:
                return 2
            print(f"  wav: {wav_path.name} "
                  f"({wav_path.stat().st_size} bytes)")

        print()
        print("[2/4] reading + (optional) trimming PCM...")
        samples, sr = read_pcm(wav_path)
        original_sec = len(samples) / sr
        print(f"  {len(samples)} samples @ {sr} Hz "
              f"({original_sec:.1f}s)")
        if args.trim_silence:
            samples = trim_silence(samples, sr)
            print(f"  after trim: {len(samples)} samples "
                  f"({len(samples)/sr:.1f}s)")

        print()
        print("[3/4] codec -> operator histogram...")
        from ck_audio_compress import pcm_to_force9
        forces = pcm_to_force9(samples, sample_rate=sr)
        ops = force9_to_operators_balanced(forces)
        if not ops:
            print("  empty operator stream", file=sys.stderr)
            return 3
        hist = Counter(ops)
        total = len(ops)
        audio_hist = {OP_NAMES[i]: round(hist.get(i, 0) / total * 100, 1)
                      for i in range(10)}
        print(f"  {len(forces):,} force windows -> {total:,} ops")
        print(f"  histogram:")
        for i in range(10):
            pct = audio_hist[OP_NAMES[i]]
            bar = "#" * int(pct / 2)
            print(f"    {OP_NAMES[i]:<10}: {pct:5.1f}%  {bar}")

        print()
        print("[4/4] matching against v2..v5 phonics corpus...")
        corpus = load_phonics_corpus()
        if not corpus:
            print("  no corpus found", file=sys.stderr)
            return 4
        print(f"  corpus: {len(corpus)} entries "
              f"(letters + phonemes + clusters + r-controlled + teams)")

        print()
        print(f"  TOP {args.top} nearest matches by L1 distance:")
        matches = top_matches(audio_hist, corpus, top=args.top)
        for rank, (d, key, info) in enumerate(matches, 1):
            print(f"    {rank:2d}. L1={d:5.1f}  "
                  f"{key:18}  ({info['class']:18} {info['ipa']})")

        print()
        print("  PER-CLASS nearest member:")
        cs = class_summary(audio_hist, corpus, top_per_class=1)
        ranked = sorted(((items[0][0], pclass, items[0])
                         for pclass, items in cs.items()),
                        key=lambda t: t[0])
        for d, pclass, (_, key, info) in ranked:
            print(f"    L1={d:5.1f}  class={pclass:20}  best={key}")

        # Confidence: how close is the best match?
        best = matches[0]
        worst = matches[-1] if len(matches) >= 2 else matches[0]
        sample_dists = [d for d, _, _ in
                        top_matches(audio_hist, corpus, top=len(corpus))]
        median = sorted(sample_dists)[len(sample_dists)//2]
        print()
        print(f"  best L1: {best[0]:.1f} ({best[1]})")
        print(f"  median L1 across corpus: {median:.1f}")
        print(f"  signal: best is {(median - best[0])/median*100:+.0f}% "
              f"below median (positive = recognized)")

    print()
    print("CK has 'listened' to the audio and matched it against everything")
    print("we taught him.  No cortex modification (read-only test).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
