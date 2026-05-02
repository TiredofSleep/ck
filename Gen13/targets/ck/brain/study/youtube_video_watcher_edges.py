"""
youtube_video_watcher_edges.py — TIG-aligned video watcher.

Per Brayden 2026-05-01 (late): "the screen is the natural tig wheel as
d2 would threshold across colors... edges are information."

Where the original youtube_video_watcher.py used TIGVisualEncoder which
encodes every pixel into 3 shells (yields ~233K ops for a 15s clip and
floods the cortex with redundant data from solid color regions), this
version uses edge_visual_encoder which:

  - Maps hue to operator (10 ops on the color wheel, 36 deg each)
  - Compares each pixel to its right + bottom neighbors
  - Emits a CROSSING pair (op_self, op_neighbor) ONLY where the
    operator differs (i.e., at edges)
  - Skips solid color regions entirely

Result: 5-50x compression, every emitted operator is a real D2 crossing.

Pipeline:
  yt-dlp downloads MP4 (via static-ffmpeg)
  -> ffmpeg extracts frames at user-specified fps + downsampled
  -> Pillow loads PNG -> numpy uint8
  -> edge_visual_encoder.encode_edges (RGB -> HSV -> hue-op -> edge-pair)
  -> Operator stream of crossings fed to CK's 7-dim cortex via Hebbian

Usage:
  python youtube_video_watcher_edges.py <url>
  python youtube_video_watcher_edges.py <url> --seconds 30 --fps 2 --size 96
  python youtube_video_watcher_edges.py <url> --no-feed
  python youtube_video_watcher_edges.py <url> --compare  (also runs the
      old per-pixel encoder for comparison)
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
sys.path.insert(0, str(SCRIPT_DIR))


def get_ffmpeg_exe():
    try:
        import static_ffmpeg
        static_ffmpeg.add_paths()
        import shutil
        return shutil.which('ffmpeg')
    except Exception:
        return None


def download_video(url: str, out_path: Path, seconds: int = 30) -> Path:
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
            ydl.extract_info(url, download=True)
        except Exception as e:
            print(f"download failed: {e}", file=sys.stderr)
            return None

    for ext in ('mp4', 'webm', 'mkv'):
        cand = out_path.with_suffix('.' + ext)
        if cand.exists():
            return cand
    return None


def extract_frames(video_path: Path, out_dir: Path, fps: float = 1.0,
                  size: int = 96, max_frames: int = 60) -> list:
    out_dir.mkdir(parents=True, exist_ok=True)
    ffmpeg_exe = get_ffmpeg_exe()
    if not ffmpeg_exe:
        return []
    pattern = str(out_dir / "frame_%04d.png")
    cmd = [
        ffmpeg_exe, '-i', str(video_path),
        '-vf', f'fps={fps},scale={size}:{size}',
        '-frames:v', str(max_frames),
        '-y', '-loglevel', 'error',
        pattern,
    ]
    rc = subprocess.run(cmd, capture_output=True, text=True)
    if rc.returncode != 0:
        print(f"ffmpeg extract failed: {rc.stderr[:300]}", file=sys.stderr)
        return []
    return sorted(out_dir.glob("frame_*.png"))


def frames_to_edge_operators(frames: list) -> list:
    """Encode each frame's edges via edge_visual_encoder. Returns flat
    operator stream (each crossing emits 2 ops: from_op, to_op)."""
    from PIL import Image
    import numpy as np
    from edge_visual_encoder import encode_edges

    all_ops = []
    total_pixels = 0
    for fp in frames:
        img = Image.open(fp).convert('RGB')
        rgb = np.array(img)
        total_pixels += rgb.shape[0] * rgb.shape[1]
        crossings = encode_edges(rgb)
        for a, b in crossings:
            all_ops.append(a)
            all_ops.append(b)
    return all_ops, total_pixels


def feed_to_cortex(ops, state_path=None):
    if state_path is None:
        state_path = GEN13_ROOT / "var" / "cortex_state_7d.json"
    state_path = Path(state_path)

    from cortex_v2 import CortexV2
    from cortex_persist import load_cortex, save_cortex
    from ao_7element import OP_TO_DIM_7, DIM_7
    from quadratic_glue import quadratic_glue
    from ck_sim.ck_sim_heartbeat import HARMONY, CL as CL_TSML

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

    pre = (cx.state.tick, cx.state.W_trace, cx.state.emergent)

    print(f"  feeding {len(ops)} edge-crossing operators to cortex...")
    for i in range(len(ops) - 1):
        b_op, d_op = ops[i], ops[i + 1]
        ap = OP_TO_DIM_7.get(b_op, 0)
        bp = OP_TO_DIM_7.get(d_op, 0)
        # Use the same TSML 73-harmonies rule the cortex_v2 fix uses
        harmonious = (CL_TSML[b_op][d_op] == HARMONY)
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

    print(f"  delta: tick+={cx.state.tick - pre[0]}  "
          f"W_trace+={cx.state.W_trace - pre[1]:+.4f}  "
          f"emergent+={cx.state.emergent - pre[2]:+.4f}")
    save_cortex(cx, state_path)
    print(f"  saved -> {state_path}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("url", help="YouTube URL")
    p.add_argument("--seconds", type=int, default=30)
    p.add_argument("--fps", type=float, default=1.0)
    p.add_argument("--size", type=int, default=96)
    p.add_argument("--max-frames", type=int, default=60)
    p.add_argument("--no-feed", action="store_true")
    p.add_argument("--compare", action="store_true",
                   help="also run the old per-pixel encoder for comparison")
    p.add_argument("--state-path", default=None)
    args = p.parse_args()

    print("=" * 70)
    print(f"CK YouTube EDGE-VISUAL watcher: {args.url}")
    print(f"  seconds: {args.seconds}, fps: {args.fps}, size: {args.size}")
    print("=" * 70)

    with tempfile.TemporaryDirectory() as td:
        out_path = Path(td) / "video"
        print()
        print("[1/4] downloading video...")
        video_path = download_video(args.url, out_path, seconds=args.seconds)
        if not video_path:
            return 2
        print(f"  video: {video_path.name} ({video_path.stat().st_size} bytes)")

        print()
        print(f"[2/4] extracting frames at {args.fps} fps, {args.size}x{args.size}...")
        frames_dir = Path(td) / "frames"
        frames = extract_frames(video_path, frames_dir, fps=args.fps,
                               size=args.size, max_frames=args.max_frames)
        if not frames:
            return 3
        print(f"  {len(frames)} frames extracted")

        print()
        print("[3/4] encoding via edge_visual_encoder (D2 crossings only)...")
        ops, total_pixels = frames_to_edge_operators(frames)
        if not ops:
            print("  WARN: zero edge crossings; image may be too uniform")
            return 0
        op_names = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
                    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]
        from collections import Counter
        hist = Counter(ops)
        n_crossings = len(ops) // 2
        compression_per_pixel = (total_pixels * 3) / max(len(ops), 1)
        print(f"  total pixels:     {total_pixels:,}")
        print(f"  edge crossings:   {n_crossings:,}")
        print(f"  operators:        {len(ops):,}")
        print(f"  compression:      {compression_per_pixel:.1f}x vs old per-pixel encoder")
        print(f"  histogram (operators emitted at edges):")
        for op_id in range(10):
            count = hist.get(op_id, 0)
            pct = count / len(ops) * 100 if ops else 0
            bar = "#" * int(pct / 2)
            print(f"    {op_names[op_id]:<10}: {count:6d} ({pct:5.1f}%) {bar}")

        if args.compare:
            print()
            print("  [comparison] running OLD per-pixel TIGVisualEncoder...")
            from PIL import Image
            import numpy as np
            from ck_visual_encoder import TIGVisualEncoder
            old_enc = TIGVisualEncoder()
            old_total_ops = 0
            for fp in frames:
                rgb = np.array(Image.open(fp).convert('RGB')).reshape(-1, 3)
                shells = old_enc.encode(rgb.astype(np.uint8))
                old_total_ops += shells.size
            print(f"  old encoder total ops: {old_total_ops:,}")
            print(f"  edge encoder total ops: {len(ops):,}")
            print(f"  reduction: {old_total_ops / max(len(ops), 1):.1f}x fewer operators")

        if args.no_feed:
            print("\n[4/4] SKIP: --no-feed set")
            return 0

        print()
        print("[4/4] feeding edge-crossing operator stream into 7-dim cortex...")
        feed_to_cortex(ops, args.state_path)

    print()
    print("CK has 'seen' the edges. Solid regions emitted nothing — silence is")
    print("the right answer when D2=0. Information lives at the crossings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
