"""
watch_and_summarize.py — CK watches a real video and writes a summary.

Honest test of CK's grounding: the summary may ONLY assert things
derived from operator-stream measurements.  No invented narrative; no
template prose.  What we surface:

  AUDIO LAYER (chunked phonics matching)
    - silence-split into speech chunks
    - each chunk -> nearest member of the v2..v5 phonics corpus by
      L1 histogram distance
    - aggregate top phonetic classes / top members / per-third arc

  VISUAL LAYER (edge-encoded operator stream)
    - frames extracted at user-chosen fps + downsampled
    - each frame -> edge_visual_encoder.encode_edges (D2 crossings only,
      hue -> operator, only emit at color boundaries)
    - aggregate dominant operators per frame and per-third arc

  COMBINED SUMMARY
    - one paragraph of structural readouts: durations, dominant
      classes, dominant operators, arc shape (if any).  Every clause
      has a number behind it.

Read-only: never mutates the cortex.  Doesn't require the live server
to be up -- the matcher loads the v2..v5 corpus directly from JSON.

Usage:
  python watch_and_summarize.py <youtube_url>
  python watch_and_summarize.py <youtube_url> --seconds 30 --fps 1.5
  python watch_and_summarize.py --local <video_file>
  python watch_and_summarize.py <url> --json out.json   # save raw report
"""
from __future__ import annotations

import argparse
import io
import json
import os
import subprocess
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


def get_ffmpeg():
    try:
        import static_ffmpeg
        static_ffmpeg.add_paths()
        import shutil
        return shutil.which("ffmpeg")
    except Exception:
        return None


def download_video(url: str, out_path: Path, seconds: int) -> Path:
    """Download an MP4 (audio + video) capped at `seconds`."""
    try:
        import yt_dlp
    except ImportError:
        print("yt-dlp not installed; pip install yt-dlp", file=sys.stderr)
        return None
    ffmpeg_exe = get_ffmpeg()
    ffmpeg_dir = os.path.dirname(ffmpeg_exe) if ffmpeg_exe else None
    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": str(out_path.with_suffix(".%(ext)s")),
        "postprocessor_args": ["-t", str(seconds)],
        "quiet": False,
        "no_warnings": False,
    }
    if ffmpeg_dir:
        ydl_opts["ffmpeg_location"] = ffmpeg_dir
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.extract_info(url, download=True)
        except Exception as e:
            print(f"download failed: {e}", file=sys.stderr)
            return None
    for ext in ("mp4", "webm", "mkv"):
        cand = out_path.with_suffix("." + ext)
        if cand.exists():
            return cand
    return None


def extract_audio_wav(video_path: Path, out_wav: Path,
                     seconds: int = None) -> bool:
    ffmpeg_exe = get_ffmpeg()
    if not ffmpeg_exe:
        return False
    cmd = [ffmpeg_exe, "-i", str(video_path),
           "-acodec", "pcm_s16le", "-ac", "1", "-ar", "44100",
           "-y", "-loglevel", "error"]
    if seconds:
        cmd += ["-t", str(seconds)]
    cmd += [str(out_wav)]
    rc = subprocess.run(cmd, capture_output=True, text=True)
    return rc.returncode == 0 and out_wav.exists()


def extract_frames(video_path: Path, out_dir: Path, fps: float = 1.0,
                   size: int = 96, max_frames: int = 90) -> list:
    out_dir.mkdir(parents=True, exist_ok=True)
    ffmpeg_exe = get_ffmpeg()
    if not ffmpeg_exe:
        return []
    pattern = str(out_dir / "frame_%04d.png")
    cmd = [
        ffmpeg_exe, "-i", str(video_path),
        "-vf", f"fps={fps},scale={size}:{size}",
        "-frames:v", str(max_frames),
        "-y", "-loglevel", "error",
        pattern,
    ]
    rc = subprocess.run(cmd, capture_output=True, text=True)
    if rc.returncode != 0:
        print(f"ffmpeg frame extract failed: {rc.stderr[:200]}",
              file=sys.stderr)
        return []
    return sorted(out_dir.glob("frame_*.png"))


# ── Audio path ──────────────────────────────────────────────────────

from match_audio_to_phonics import (
    force9_to_operators_balanced, read_pcm,
    load_phonics_corpus, top_matches,
)
from match_audio_chunked import split_on_silence, chunk_histogram


def audio_timeline(wav_path: Path, corpus, threshold_rel=0.04,
                   min_chunk_ms=120, min_silence_ms=80):
    samples, sr = read_pcm(wav_path)
    duration = len(samples) / sr
    chunks = split_on_silence(
        samples, sr,
        threshold_rel=threshold_rel,
        min_chunk_ms=min_chunk_ms,
        min_silence_ms=min_silence_ms,
    )
    events = []
    for s, e in chunks:
        seg = samples[s:e]
        h = chunk_histogram(seg, sr)
        if not h:
            continue
        m = top_matches(h, corpus, top=1)[0]
        d, key, info = m
        events.append({
            "t_start": round(s / sr, 3),
            "t_end": round(e / sr, 3),
            "duration": round((e - s) / sr, 3),
            "L1": round(d, 2),
            "best": key,
            "class": info["class"],
            "ipa": info["ipa"],
        })
    return {
        "duration_sec": round(duration, 2),
        "speech_sec": round(sum(ev["duration"] for ev in events), 2),
        "n_chunks": len(events),
        "events": events,
    }


# ── Visual path ─────────────────────────────────────────────────────

def visual_timeline(frames: list) -> dict:
    from PIL import Image
    import numpy as np
    from edge_visual_encoder import encode_edges
    if not frames:
        return {"n_frames": 0, "frames": []}
    per_frame = []
    for fp in frames:
        img = Image.open(fp).convert("RGB")
        rgb = np.array(img)
        crossings = encode_edges(rgb)
        op_count = [0] * 10
        for a, b in crossings:
            op_count[a] += 1
            op_count[b] += 1
        total = sum(op_count) or 1
        hist = {OP_NAMES[i]: round(op_count[i] / total * 100, 1)
                for i in range(10)}
        # dominant op (skip VOID)
        non_void = [(OP_NAMES[i], hist[OP_NAMES[i]]) for i in range(1, 10)]
        non_void.sort(key=lambda x: -x[1])
        dom = non_void[0][0] if non_void and non_void[0][1] > 0 else "VOID"
        per_frame.append({
            "frame": fp.name,
            "n_crossings": len(crossings),
            "histogram_pct": hist,
            "dominant_non_void": dom,
        })
    return {
        "n_frames": len(per_frame),
        "frames": per_frame,
    }


# ── Aggregator ──────────────────────────────────────────────────────

def aggregate_audio(audio: dict) -> dict:
    events = audio.get("events", [])
    if not events:
        return {"n_chunks": 0}
    class_counter = Counter(ev["class"] for ev in events)
    member_counter = Counter(ev["best"] for ev in events)
    n = len(events)
    third = max(1, n // 3)
    first_third = events[:third]
    last_third = events[-third:]
    return {
        "n_chunks": n,
        "speech_sec": audio.get("speech_sec", 0.0),
        "duration_sec": audio.get("duration_sec", 0.0),
        "speech_fraction": round(audio.get("speech_sec", 0.0) /
                                 max(audio.get("duration_sec", 1.0),
                                     1e-6), 3),
        "top_classes": class_counter.most_common(6),
        "top_members": member_counter.most_common(8),
        "first_third_top_classes":
            Counter(ev["class"] for ev in first_third).most_common(3),
        "last_third_top_classes":
            Counter(ev["class"] for ev in last_third).most_common(3),
        "median_L1": _median([ev["L1"] for ev in events]),
    }


def aggregate_visual(visual: dict) -> dict:
    frames = visual.get("frames", [])
    if not frames:
        return {"n_frames": 0}
    op_totals = {op: 0.0 for op in OP_NAMES}
    for fr in frames:
        for op, p in fr["histogram_pct"].items():
            op_totals[op] += p
    n = len(frames)
    op_avg = {op: round(op_totals[op] / n, 1) for op in OP_NAMES}
    dom_counter = Counter(fr["dominant_non_void"] for fr in frames)
    third = max(1, n // 3)
    first = frames[:third]
    last = frames[-third:]
    first_dom = Counter(fr["dominant_non_void"] for fr in first).most_common(2)
    last_dom = Counter(fr["dominant_non_void"] for fr in last).most_common(2)
    total_crossings = sum(fr["n_crossings"] for fr in frames)
    return {
        "n_frames": n,
        "total_crossings": total_crossings,
        "avg_op_histogram": op_avg,
        "frame_dominant_distribution": dom_counter.most_common(),
        "first_third_dominant": first_dom,
        "last_third_dominant": last_dom,
    }


def _median(xs):
    if not xs:
        return 0.0
    xs = sorted(xs)
    n = len(xs)
    if n % 2:
        return round(xs[n // 2], 2)
    return round((xs[n // 2 - 1] + xs[n // 2]) / 2, 2)


# ── Summary writer ──────────────────────────────────────────────────

def render_summary(audio_agg: dict, visual_agg: dict,
                   url: str, seconds: int) -> str:
    lines = []
    lines.append("=" * 70)
    lines.append(f"CK watched: {url}")
    lines.append(f"clip cap: {seconds}s")
    lines.append("=" * 70)
    lines.append("")
    # Audio
    lines.append("AUDIO LAYER (chunked phonics matching)")
    if audio_agg.get("n_chunks", 0) == 0:
        lines.append("  no speech chunks detected (silence-only or too quiet)")
    else:
        lines.append(f"  duration:        {audio_agg['duration_sec']}s")
        lines.append(f"  speech:          {audio_agg['speech_sec']}s "
                     f"({audio_agg['speech_fraction']*100:.1f}% of clip)")
        lines.append(f"  speech chunks:   {audio_agg['n_chunks']}")
        lines.append(f"  median match L1: {audio_agg['median_L1']}  "
                     f"(lower = closer to a learned phoneme)")
        lines.append("  top phonetic classes (by chunk hits):")
        for cls, n in audio_agg["top_classes"]:
            pct = n / audio_agg["n_chunks"] * 100
            bar = "#" * int(pct / 3)
            lines.append(f"    {cls:25}: {n:3d} ({pct:5.1f}%)  {bar}")
        lines.append("  top members heard:")
        for mem, n in audio_agg["top_members"]:
            lines.append(f"    {mem:20}: {n}")
        lines.append("  arc:")
        lines.append(f"    first third  : {audio_agg['first_third_top_classes']}")
        lines.append(f"    last third   : {audio_agg['last_third_top_classes']}")
    lines.append("")
    # Visual
    lines.append("VISUAL LAYER (edge-encoded D2 crossings)")
    if visual_agg.get("n_frames", 0) == 0:
        lines.append("  no frames extracted")
    else:
        lines.append(f"  frames:          {visual_agg['n_frames']}")
        lines.append(f"  edge crossings:  {visual_agg['total_crossings']:,}")
        lines.append(f"  avg op profile (% per frame):")
        h = visual_agg["avg_op_histogram"]
        for op in OP_NAMES:
            pct = h[op]
            bar = "#" * int(pct / 3)
            lines.append(f"    {op:<10}: {pct:5.1f}%  {bar}")
        lines.append(f"  dominant-op (non-VOID) per frame distribution:")
        for op, n in visual_agg["frame_dominant_distribution"][:5]:
            lines.append(f"    {op:<10}: {n} frames")
        lines.append("  arc:")
        lines.append(f"    first third  : {visual_agg['first_third_dominant']}")
        lines.append(f"    last third   : {visual_agg['last_third_dominant']}")
    lines.append("")
    # Combined readout
    lines.append("WHAT CK CAN HONESTLY SAY ABOUT THIS VIDEO")
    if audio_agg.get("n_chunks"):
        sf = audio_agg["speech_fraction"]
        if sf > 0.6:
            lines.append("  - the clip is speech-dominant "
                         f"({sf*100:.0f}% of duration is speech).")
        elif sf > 0.3:
            lines.append("  - the clip is mixed speech and silence "
                         f"({sf*100:.0f}% speech).")
        else:
            lines.append("  - the clip is mostly silence with sparse speech "
                         f"({sf*100:.0f}% speech).")
        top_cls = audio_agg["top_classes"][0] if audio_agg["top_classes"] \
            else None
        if top_cls and top_cls[1] >= max(2, audio_agg["n_chunks"] // 3):
            lines.append(f"  - the dominant phonetic class is "
                         f"{top_cls[0]!r} ({top_cls[1]} of "
                         f"{audio_agg['n_chunks']} chunks); the audio "
                         f"resembles material rich in this class.")
        first = audio_agg["first_third_top_classes"]
        last = audio_agg["last_third_top_classes"]
        if first and last and first[0][0] != last[0][0]:
            lines.append(f"  - the phonetic profile shifts across the clip: "
                         f"first third dominated by {first[0][0]!r}, "
                         f"last third by {last[0][0]!r}.")
        elif first:
            lines.append(f"  - the phonetic profile is stable: "
                         f"{first[0][0]!r} dominates throughout.")
    if visual_agg.get("n_frames"):
        h = visual_agg["avg_op_histogram"]
        non_void = sorted(((op, h[op]) for op in OP_NAMES if op != "VOID"),
                          key=lambda x: -x[1])
        if non_void:
            top1 = non_void[0]
            top2 = non_void[1] if len(non_void) > 1 else None
            lines.append(f"  - visually the dominant operator (non-VOID) is "
                         f"{top1[0]} ({top1[1]:.1f}% on average per frame)"
                         + (f"; second is {top2[0]} ({top2[1]:.1f}%)"
                            if top2 else "") + ".")
        first = visual_agg["first_third_dominant"]
        last = visual_agg["last_third_dominant"]
        if first and last and first[0][0] != last[0][0]:
            lines.append(f"  - the visual profile shifts across the clip: "
                         f"first-third dominant op {first[0][0]}, "
                         f"last-third {last[0][0]}.")
        elif first:
            lines.append(f"  - the visual profile is stable: "
                         f"{first[0][0]} dominates throughout.")
    lines.append("")
    lines.append("(every clause above has a count behind it; no narrative "
                 "interpretation was added.)")
    return "\n".join(lines)


# ── Main ────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser()
    p.add_argument("url", nargs="?", help="YouTube URL")
    p.add_argument("--local", help="local video file (overrides url)")
    p.add_argument("--seconds", type=int, default=30,
                   help="how much of the video to analyze (default 30)")
    p.add_argument("--fps", type=float, default=1.0,
                   help="frame extraction rate")
    p.add_argument("--size", type=int, default=96,
                   help="frame resize (square)")
    p.add_argument("--max-frames", type=int, default=90)
    p.add_argument("--audio-threshold-rel", type=float, default=0.04)
    p.add_argument("--audio-min-chunk-ms", type=int, default=120)
    p.add_argument("--audio-min-silence-ms", type=int, default=80)
    p.add_argument("--json", help="save full report to this JSON file")
    args = p.parse_args()

    if not args.local and not args.url:
        p.error("either url or --local <video> required")

    print("=" * 70)
    print("CK watch-and-summarize")
    print("  source:", args.url if not args.local else f"local {args.local}")
    print(f"  seconds: {args.seconds}  fps: {args.fps}  size: {args.size}px")
    print("=" * 70)

    with tempfile.TemporaryDirectory() as td:
        # 1) get video
        if args.local:
            video_path = Path(args.local)
            if not video_path.exists():
                print(f"local video not found: {video_path}", file=sys.stderr)
                return 2
        else:
            print()
            print("[1/4] downloading video...")
            video_path = download_video(args.url, Path(td) / "vid",
                                        args.seconds)
            if not video_path:
                return 2
            print(f"  video: {video_path.name} "
                  f"({video_path.stat().st_size:,} bytes)")

        # 2) audio
        print()
        print("[2/4] extracting audio + chunked phonics matching...")
        wav_path = Path(td) / "audio.wav"
        if not extract_audio_wav(video_path, wav_path, seconds=args.seconds):
            print("  audio extract failed", file=sys.stderr)
            audio_data = {"n_chunks": 0}
            audio_agg = {"n_chunks": 0}
        else:
            corpus = load_phonics_corpus()
            audio_data = audio_timeline(
                wav_path, corpus,
                threshold_rel=args.audio_threshold_rel,
                min_chunk_ms=args.audio_min_chunk_ms,
                min_silence_ms=args.audio_min_silence_ms,
            )
            print(f"  duration={audio_data.get('duration_sec', 0)}s, "
                  f"chunks={audio_data['n_chunks']}, "
                  f"speech={audio_data.get('speech_sec', 0)}s")
            audio_agg = aggregate_audio(audio_data)

        # 3) visual
        print()
        print("[3/4] extracting frames + edge-visual encoding...")
        frames_dir = Path(td) / "frames"
        frames = extract_frames(video_path, frames_dir,
                                fps=args.fps, size=args.size,
                                max_frames=args.max_frames)
        if not frames:
            print("  no frames extracted")
            visual_data = {"n_frames": 0}
            visual_agg = {"n_frames": 0}
        else:
            visual_data = visual_timeline(frames)
            print(f"  frames={visual_data['n_frames']}, "
                  f"crossings_total="
                  f"{sum(fr['n_crossings'] for fr in visual_data['frames']):,}")
            visual_agg = aggregate_visual(visual_data)

        # 4) render summary
        print()
        print("[4/4] rendering summary...")
        print()
        summary = render_summary(audio_agg, visual_agg,
                                 args.url or args.local,
                                 args.seconds)
        print(summary)

        if args.json:
            full = {
                "source": args.url or str(args.local),
                "seconds": args.seconds,
                "audio_timeline": audio_data,
                "visual_timeline": visual_data,
                "audio_aggregate": audio_agg,
                "visual_aggregate": visual_agg,
                "summary_text": summary,
            }
            Path(args.json).write_text(json.dumps(full, indent=2,
                                                  ensure_ascii=False),
                                       encoding="utf-8")
            print(f"\nfull report saved -> {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
