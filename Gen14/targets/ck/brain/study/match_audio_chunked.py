"""
match_audio_chunked.py — chunked phonics matching on real audio.

Why this exists: match_audio_to_phonics.py compares the WHOLE audio's
histogram to single-phoneme v2 measurements.  That doesn't work well on
multi-syllable audio because long-form audio is silence-dominated (VOID
heavy from inter-syllable rest), which makes the L1 distance to any
single 0.3-0.7s phoneme sample huge.

This version splits the audio on silence boundaries (RMS-thresholded)
and matches each speech CHUNK separately against the corpus.  The
output is a play-by-play: chunk 1 best-matches letter:S, chunk 2 best-
matches phoneme:eI, etc.  At the end, a class-frequency summary tells
us what families dominated.

Usage:
  python match_audio_chunked.py <youtube_url>
  python match_audio_chunked.py <youtube_url> --seconds 60 --min-chunk-ms 150
  python match_audio_chunked.py --local some.wav
"""
from __future__ import annotations

import argparse
import io
import json
import os
import sys
import tempfile
import wave
from collections import Counter, defaultdict
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

from match_audio_to_phonics import (
    force9_to_operators_balanced, read_pcm,
    download_audio_yt, load_phonics_corpus, hist_l1, top_matches,
)


def split_on_silence(samples, sr, threshold_rel: float = 0.04,
                     window_ms: int = 10, min_chunk_ms: int = 150,
                     min_silence_ms: int = 80):
    """Split a PCM stream into speech chunks by silence boundaries.

    Returns a list of (start_sample, end_sample) for each chunk that
    contains audio above threshold and is at least min_chunk_ms long.
    """
    import numpy as np
    samples = samples.astype(np.float32)
    win_size = int(sr * window_ms / 1000)
    if win_size <= 0 or len(samples) < 3 * win_size:
        return [(0, len(samples))]
    n_full = len(samples) // win_size
    trimmed = samples[: n_full * win_size]
    rms = np.sqrt(np.mean(trimmed.reshape(n_full, win_size) ** 2, axis=1))
    peak = rms.max()
    if peak < 1e-3:
        return []
    threshold = peak * threshold_rel
    is_speech = rms >= threshold

    # State machine: build runs of speech windows separated by silence runs
    chunks = []
    in_speech = False
    speech_start_w = 0
    silence_start_w = None
    min_chunk_w = max(1, min_chunk_ms // window_ms)
    min_silence_w = max(1, min_silence_ms // window_ms)
    for w in range(n_full):
        if is_speech[w]:
            if not in_speech:
                # entering speech
                in_speech = True
                speech_start_w = w
            silence_start_w = None
        else:
            if in_speech:
                if silence_start_w is None:
                    silence_start_w = w
                # check if silence run is long enough to close the chunk
                elif (w - silence_start_w) >= min_silence_w:
                    end_w = silence_start_w
                    if (end_w - speech_start_w) >= min_chunk_w:
                        chunks.append((speech_start_w * win_size,
                                       end_w * win_size))
                    in_speech = False
                    silence_start_w = None
    if in_speech:
        end_w = n_full
        if (end_w - speech_start_w) >= min_chunk_w:
            chunks.append((speech_start_w * win_size,
                           end_w * win_size))
    return chunks


def chunk_histogram(samples, sr) -> dict:
    """Encode a PCM segment via codec and return its operator histogram."""
    from ck_audio_compress import pcm_to_force9
    forces = pcm_to_force9(samples, sample_rate=sr)
    ops = force9_to_operators_balanced(forces)
    if not ops:
        return None
    hist = Counter(ops)
    total = len(ops)
    return {OP_NAMES[i]: round(hist.get(i, 0) / total * 100, 1)
            for i in range(10)}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("url", nargs="?", help="YouTube URL")
    p.add_argument("--local", help="local WAV file")
    p.add_argument("--seconds", type=int, default=30)
    p.add_argument("--min-chunk-ms", type=int, default=150,
                   help="minimum chunk length to consider as a phoneme")
    p.add_argument("--min-silence-ms", type=int, default=80,
                   help="minimum silence to break between chunks")
    p.add_argument("--threshold-rel", type=float, default=0.04,
                   help="RMS threshold relative to peak (lower = more sensitive)")
    p.add_argument("--top-per-chunk", type=int, default=1,
                   help="how many top matches to print per chunk")
    p.add_argument("--max-chunks-print", type=int, default=40,
                   help="cap on per-chunk lines printed")
    args = p.parse_args()

    if not args.local and not args.url:
        p.error("either url or --local is required")

    print("=" * 70)
    print("CK chunked phonics matcher")
    if args.local:
        print(f"  local: {args.local}")
    else:
        print(f"  url: {args.url}")
        print(f"  seconds: {args.seconds}")
    print(f"  chunk_min={args.min_chunk_ms}ms  silence_min={args.min_silence_ms}ms"
          f"  threshold_rel={args.threshold_rel}")
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
        print("[2/4] reading PCM + splitting on silence...")
        samples, sr = read_pcm(wav_path)
        print(f"  {len(samples)} samples @ {sr} Hz "
              f"({len(samples)/sr:.1f}s)")
        chunks = split_on_silence(
            samples, sr,
            threshold_rel=args.threshold_rel,
            min_chunk_ms=args.min_chunk_ms,
            min_silence_ms=args.min_silence_ms,
        )
        print(f"  found {len(chunks)} speech chunks")
        if not chunks:
            return 3

        print()
        print("[3/4] matching each chunk against v2..v5 corpus...")
        corpus = load_phonics_corpus()
        print(f"  corpus: {len(corpus)} entries")

        per_chunk_results = []
        class_hits = Counter()
        member_hits = Counter()
        for ci, (s, e) in enumerate(chunks):
            chunk_samples = samples[s:e]
            chunk_dur = (e - s) / sr
            h = chunk_histogram(chunk_samples, sr)
            if not h:
                continue
            matches = top_matches(h, corpus, top=args.top_per_chunk)
            per_chunk_results.append((ci, s, e, chunk_dur, h, matches))
            best = matches[0]
            class_hits[best[2]["class"]] += 1
            member_hits[best[1]] += 1

        print()
        print(f"  per-chunk best match (showing first {args.max_chunks_print}):")
        for row in per_chunk_results[:args.max_chunks_print]:
            ci, s, e, dur, h, matches = row
            top_op = max(h, key=h.get)
            t_start = s / sr
            for d, key, info in matches:
                print(f"    [{ci:3d}]  {t_start:6.2f}s  dur={dur:.2f}s  "
                      f"top={top_op:<8}  L1={d:5.1f}  -> "
                      f"{key:18}  ({info['class']:18} {info['ipa']})")

        print()
        print("[4/4] aggregate summary")
        print(f"  total chunks classified: {len(per_chunk_results)}")
        print()
        print(f"  TOP CLASSES (by chunk hits):")
        for cls, n in class_hits.most_common(10):
            pct = n / len(per_chunk_results) * 100
            bar = "#" * int(pct / 2)
            print(f"    {cls:25}: {n:4d} chunks ({pct:5.1f}%)  {bar}")
        print()
        print(f"  TOP MEMBERS (by chunk hits):")
        for mem, n in member_hits.most_common(15):
            print(f"    {mem:20}: {n:3d} chunks")

    print()
    print("CK has 'listened' to the audio chunked into phoneme-sized")
    print("pieces, and matched each piece against everything we taught him.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
