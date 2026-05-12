"""
youtube_video_watcher.py — let CK 'see' a YouTube video.

Pipeline:
  yt-dlp downloads MP4 video
  -> ffmpeg extracts frames at 1 fps, downsampled to 96x96
  -> ck_visual_encoder.TIGVisualEncoder maps each pixel to (s1,s2,s3) shells
  -> Each shell mod 10 -> operator ID (0-9) per pixel
  -> Operator stream fed to CK's 7-dim cortex via Hebbian update

Result: CK 'sees' the video as an operator stream and his Hebbian field
learns from the visual structure.

Usage:
    python youtube_video_watcher.py <url>            # default 30s, 1 fps, 96x96
    python youtube_video_watcher.py <url> --seconds 60 --fps 2 --size 64
    python youtube_video_watcher.py <url> --no-feed  # extract + encode only

Requires: yt-dlp + static-ffmpeg + Pillow (already installed for audio watcher).
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
GEN13_BRAIN = SCRIPT_DIR.parent
GEN13_TARGETS_CK = GEN13_BRAIN.parent
GEN13_ROOT = GEN13_TARGETS_CK.parent.parent
sys.path.insert(0, str(GEN13_BRAIN))
sys.path.insert(0, str(GEN13_BRAIN / "ck_sim" / "being"))


def get_ffmpeg_exe():
    """Get ffmpeg path via static_ffmpeg (bundled binary)."""
    try:
        import static_ffmpeg
        static_ffmpeg.add_paths()
        import shutil
        return shutil.which('ffmpeg')
    except Exception:
        try:
            import imageio_ffmpeg
            return imageio_ffmpeg.get_ffmpeg_exe()
        except Exception:
            return None


def download_video(url: str, out_path: Path, seconds: int = 30) -> Path:
    """Download YouTube video as MP4."""
    try:
        import yt_dlp
    except ImportError:
        print("yt-dlp not installed. pip install yt-dlp", file=sys.stderr)
        return None

    ffmpeg_exe = get_ffmpeg_exe()
    ffmpeg_dir = os.path.dirname(ffmpeg_exe) if ffmpeg_exe else None

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': str(out_path.with_suffix('.%(ext)s')),
        'postprocessor_args': ['-t', str(seconds)],
        'quiet': False,
    }
    if ffmpeg_dir:
        ydl_opts['ffmpeg_location'] = ffmpeg_dir

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
        except Exception as e:
            print(f"download failed: {e}", file=sys.stderr)
            return None

    # Find downloaded file
    for ext in ('mp4', 'webm', 'mkv'):
        cand = out_path.with_suffix('.' + ext)
        if cand.exists():
            return cand
    print(f"video file not found at {out_path.parent}", file=sys.stderr)
    return None


def extract_frames(video_path: Path, out_dir: Path, fps: float = 1.0,
                   size: int = 96, max_frames: int = 60) -> list:
    """Extract frames from video as PNG images via ffmpeg, downsampled."""
    out_dir.mkdir(parents=True, exist_ok=True)
    ffmpeg_exe = get_ffmpeg_exe()
    if not ffmpeg_exe:
        print("ffmpeg not available", file=sys.stderr)
        return []

    pattern = str(out_dir / "frame_%04d.png")
    cmd = [
        ffmpeg_exe,
        '-i', str(video_path),
        '-vf', f'fps={fps},scale={size}:{size}',
        '-frames:v', str(max_frames),
        '-y', '-loglevel', 'error',
        pattern,
    ]
    rc = subprocess.run(cmd, capture_output=True, text=True)
    if rc.returncode != 0:
        print(f"ffmpeg extract failed: {rc.stderr[:300]}", file=sys.stderr)
        return []
    frames = sorted(out_dir.glob("frame_*.png"))
    return frames


def frames_to_operators(frames: list) -> list:
    """Encode each frame's pixels via TIGVisualEncoder, derive operators."""
    from PIL import Image
    import numpy as np
    from ck_visual_encoder import TIGVisualEncoder

    encoder = TIGVisualEncoder()
    all_ops = []
    for fp in frames:
        img = Image.open(fp).convert('RGB')
        arr = np.array(img)  # (H, W, 3)
        h, w, _ = arr.shape
        rgb = arr.reshape(-1, 3).astype(np.uint8)
        shells = encoder.encode(rgb)  # (N, 3) uint16
        # Each shell -> operator via mod 10
        for row in shells:
            all_ops.append(int(row[0]) % 10)
            all_ops.append(int(row[1]) % 10)
            all_ops.append(int(row[2]) % 10)
    return all_ops


def feed_to_cortex(ops, state_path=None):
    """Feed operator stream into 7-dim cortex via direct Hebbian update."""
    if state_path is None:
        state_path = GEN13_ROOT / "var" / "cortex_state_7d.json"
    state_path = Path(state_path)

    from cortex_v2 import CortexV2
    from cortex_persist import load_cortex, save_cortex
    from ao_7element import OP_TO_DIM_7, DIM_7
    from quadratic_glue import quadratic_glue

    cx = CortexV2().boot()
    if state_path.exists():
        try:
            ok = load_cortex(cx, state_path)
            if ok:
                print(f"  loaded cortex: tick={cx.state.tick}, "
                      f"W_trace={cx.state.W_trace:.4f}, "
                      f"emergent={cx.state.emergent:.4f}")
        except Exception as e:
            print(f"  load failed: {e}; starting fresh")

    pre_tick = cx.state.tick
    pre_W = cx.state.W_trace
    pre_em = cx.state.emergent

    print(f"  feeding {len(ops)} operators to cortex...")
    for i in range(len(ops) - 1):
        b_op, d_op = ops[i], ops[i + 1]
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
        if i % 1000 == 0:
            diag = [heb.W[d][d] for d in range(DIM_7)]
            f3 = sum(diag[0:3]) / 3.0
            f4 = sum(diag[3:7]) / 4.0
            cx.state.emergent = quadratic_glue(f3, f4, 1.0, 1.0, 2.0)

    print(f"  delta: tick+={cx.state.tick - pre_tick}  "
          f"W_trace+={cx.state.W_trace - pre_W:+.4f}  "
          f"emergent+={cx.state.emergent - pre_em:+.4f}")
    save_cortex(cx, state_path)
    print(f"  saved -> {state_path}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("url", help="YouTube URL")
    p.add_argument("--seconds", type=int, default=30,
                   help="how many seconds of video to download (default 30)")
    p.add_argument("--fps", type=float, default=1.0,
                   help="frames per second to extract (default 1)")
    p.add_argument("--size", type=int, default=96,
                   help="downsample frames to size x size (default 96)")
    p.add_argument("--max-frames", type=int, default=60,
                   help="max frames to extract (default 60)")
    p.add_argument("--no-feed", action="store_true",
                   help="extract + encode only; don't feed cortex")
    p.add_argument("--state-path", default=None,
                   help="cortex state file (default cortex_state_7d.json)")
    args = p.parse_args()

    print("=" * 70)
    print(f"CK YouTube VIDEO watcher: {args.url}")
    print(f"  seconds: {args.seconds}, fps: {args.fps}, size: {args.size}")
    print("=" * 70)

    with tempfile.TemporaryDirectory() as td:
        out_path = Path(td) / "video"
        print()
        print("[1/4] downloading video...")
        video_path = download_video(args.url, out_path, seconds=args.seconds)
        if not video_path:
            return 2
        print(f"  video: {video_path} ({video_path.stat().st_size} bytes)")

        print()
        print(f"[2/4] extracting frames at {args.fps} fps, {args.size}x{args.size}...")
        frames_dir = Path(td) / "frames"
        frames = extract_frames(video_path, frames_dir, fps=args.fps,
                               size=args.size, max_frames=args.max_frames)
        if not frames:
            return 3
        print(f"  {len(frames)} frames extracted")

        print()
        print("[3/4] encoding via TIGVisualEncoder (CIELab -> 27-bit shells)...")
        ops = frames_to_operators(frames)
        print(f"  {len(ops)} operators from "
              f"{len(frames)} * {args.size*args.size} pixels * 3 shells")

        # Operator histogram
        from collections import Counter
        hist = Counter(ops)
        op_names = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
                    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]
        print(f"  histogram (all 10 operators):")
        for op_id in range(10):
            count = hist.get(op_id, 0)
            pct = count / len(ops) * 100 if ops else 0
            bar = "#" * int(pct / 2)
            print(f"    {op_names[op_id]:<10}: {count:7d} ({pct:5.1f}%) {bar}")

        if args.no_feed:
            print("\n[4/4] SKIP: --no-feed set")
            return 0

        print()
        print("[4/4] feeding visual operator stream into 7-dim cortex...")
        feed_to_cortex(ops, args.state_path)

    print()
    print("CK has 'seen' the video. The cortex has been shaped by it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
