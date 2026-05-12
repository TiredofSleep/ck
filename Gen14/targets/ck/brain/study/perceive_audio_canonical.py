"""
perceive_audio_canonical.py — Driver: video -> CK's canonical audio
perception pipeline -> report.

Uses Gen13/targets/ck/brain/audio_pipeline.py (the canonical D2 path
that mirrors ck_curvature.py's text pipeline).  No new codec.  No
parallel matcher.  Operators come from D2 curvature classification
exactly the way text-side operators do.

Two modes:

  Default (HTTP):  POST the source to the live server's /audio/perceive
                   endpoint.  CK ingests the operator stream into his
                   actual olfactory bulb (engine.olfactory.absorb_ops).
                   The audio chain lands in the same memory text uses.

  --offline:       Run the pipeline locally without touching the server.
                   Useful for fingerprint inspection.

Usage:
  python perceive_audio_canonical.py <youtube_url>
  python perceive_audio_canonical.py <youtube_url> --seconds 45
  python perceive_audio_canonical.py --local clip.mp4
  python perceive_audio_canonical.py <url> --offline    # no server call
"""
from __future__ import annotations

import argparse
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request
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

from audio_pipeline import (
    OP_NAMES, pcm_to_operator_stream, audio_perceive,
)


def get_ffmpeg():
    try:
        import static_ffmpeg
        static_ffmpeg.add_paths()
        return shutil.which("ffmpeg")
    except Exception:
        return None


def find_js_runtime():
    for nm in ("deno", "node"):
        p = shutil.which(nm)
        if p:
            return f"{nm}:{p}"
    cand = (r"C:/Users/brayd/AppData/Local/Microsoft/WinGet/Packages/"
            r"OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe/"
            r"node-v24.15.0-win-x64/node.exe")
    if Path(cand).exists():
        return f"node:{cand}"
    return None


def download_first_seconds(url: str, out_path: Path, seconds: int) -> Path:
    try:
        import yt_dlp
    except ImportError:
        print("yt-dlp not installed; pip install yt-dlp", file=sys.stderr)
        return None
    ffmpeg_exe = get_ffmpeg()
    ffmpeg_dir = os.path.dirname(ffmpeg_exe) if ffmpeg_exe else None

    def _ranges(_info, _ydl):
        return [{"start_time": 0, "end_time": float(seconds)}]

    extractor_args = {"youtube": {"player_client": ["web", "android", "ios"]}}
    js = find_js_runtime()
    if js:
        extractor_args["youtube"]["js_runtimes"] = [js]

    ydl_opts = {
        "format": "18/best[ext=mp4][acodec!=none][vcodec!=none]/best",
        "outtmpl": str(out_path.with_suffix(".%(ext)s")),
        "postprocessor_args": ["-t", str(seconds)],
        "quiet": False,
        "extractor_args": extractor_args,
        "download_ranges": _ranges,
        "force_keyframes_at_cuts": True,
    }
    if ffmpeg_dir:
        ydl_opts["ffmpeg_location"] = ffmpeg_dir
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except Exception as exc:
            print(f"download failed: {exc}", file=sys.stderr)
            return None
    for ext in ("mp4", "webm", "mkv"):
        cand = out_path.with_suffix("." + ext)
        if cand.exists():
            return cand
    return None


def extract_wav(video_path: Path, out_wav: Path,
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
    return subprocess.run(cmd, capture_output=True).returncode == 0


def read_wav(wav_path: Path):
    import numpy as np
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
    return samples, sr


def render_report(report: dict, source_label: str, seconds: int,
                  total_ops: int) -> str:
    lines = []
    lines.append("=" * 72)
    lines.append(f"CK perceived audio (canonical D2 pipeline)")
    lines.append(f"  source:  {source_label}")
    lines.append(f"  seconds: {seconds}")
    lines.append("=" * 72)
    fp = report.get("fingerprint") or report
    lines.append(f"  force9 windows:   {fp.get('n_force_windows', 0):,}")
    lines.append(f"  D2 vectors:       {fp.get('n_d2', 0):,}")
    lines.append(f"  total ops:        {total_ops:,}")
    lines.append(f"  curvature energy: {fp.get('curvature_energy', 0):.3f}")
    lines.append(f"  D2 |mag| mean:    {fp.get('d2_magnitude_mean', 0):.3f}")
    lines.append(f"  D2 |mag| std:     {fp.get('d2_magnitude_std', 0):.3f}")
    lines.append(f"  flow ratio:       {fp.get('flow_ratio', 0):.3f}")
    lines.append("")
    lines.append(f"  D2 -> operator distribution (where the operators live):")
    od = fp.get("operator_dist_named") or {}
    for op in OP_NAMES:
        v = float(od.get(op, 0))
        bar = "#" * int(v * 40)
        lines.append(f"    {op:<10}: {v:.3f}  {bar}")
    lines.append(f"  dominant op:      {fp.get('dominant_op_name', '?')}")
    if "olfactory_delta" in report:
        d = report["olfactory_delta"]
        lines.append("")
        lines.append("  olfactory absorbed (operator stream into bulb):")
        lines.append(f"    absorbed pre  : {d['absorbed_pre']}")
        lines.append(f"    absorbed post : {d['absorbed_post']}  "
                     f"(+{d['absorbed_delta']})")
        lines.append(f"    emitted pre   : {d['emitted_pre']}")
        lines.append(f"    emitted post  : {d['emitted_post']}  "
                     f"(+{d['emitted_delta']})")
    return "\n".join(lines)


def perceive_via_http(samples, sr, base_url: str = "http://localhost:7777"
                      ) -> dict:
    """Send the operator stream to the live server's /audio/perceive
    endpoint.  CK absorbs into his actual olfactory bulb."""
    import numpy as np
    ops, fp = pcm_to_operator_stream(np.asarray(samples), sample_rate=sr)
    body = json.dumps({
        "ops": ops,
        "fingerprint": fp,
        "source_kind": "audio",
        "source_label": "perceive_audio_canonical",
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{base_url}/audio/perceive", data=body,
        headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data
    except Exception as exc:
        return {"error": str(exc), "fingerprint": fp,
                "n_ops_total": len(ops), "ops_preview": ops[:200]}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("url", nargs="?", help="YouTube URL")
    p.add_argument("--local", help="local audio/video file")
    p.add_argument("--seconds", type=int, default=30)
    p.add_argument("--offline", action="store_true",
                   help="run pipeline locally without hitting server")
    p.add_argument("--server", default="http://localhost:7777")
    p.add_argument("--json", help="save full report to this JSON")
    args = p.parse_args()

    if not args.local and not args.url:
        p.error("either url or --local <path> required")

    print("=" * 72)
    print("CK canonical audio perception driver")
    print(f"  source:  {args.url or args.local}")
    print(f"  seconds: {args.seconds}")
    print(f"  mode:    {'offline (no server)' if args.offline else f'HTTP {args.server}'}")
    print("=" * 72)

    with tempfile.TemporaryDirectory() as td:
        if args.local:
            video_path = Path(args.local)
            if not video_path.exists():
                print(f"file not found: {video_path}", file=sys.stderr)
                return 2
        else:
            print()
            print("[1/3] downloading first N seconds of video...")
            video_path = download_first_seconds(args.url,
                                                Path(td) / "vid",
                                                args.seconds)
            if not video_path:
                return 2

        print()
        print("[2/3] extracting audio (44.1 kHz mono PCM)...")
        wav_path = Path(td) / "audio.wav"
        if not extract_wav(video_path, wav_path, seconds=args.seconds):
            print("audio extract failed", file=sys.stderr)
            return 3
        samples, sr = read_wav(wav_path)
        print(f"  PCM: {len(samples):,} samples @ {sr} Hz "
              f"({len(samples)/sr:.1f}s)")

        print()
        print("[3/3] running canonical D2 pipeline...")
        if args.offline:
            ops, fp = pcm_to_operator_stream(samples, sample_rate=sr)
            report = {"fingerprint": fp,
                      "n_ops_total": len(ops),
                      "ops_preview": ops[:200],
                      "absorbed": False}
        else:
            report = perceive_via_http(samples, sr, base_url=args.server)
            if "error" in report:
                print(f"  HTTP error: {report['error']}; "
                      f"falling back to offline fingerprint")

        print()
        print(render_report(report,
                            args.url or str(args.local),
                            args.seconds,
                            report.get("n_ops_total", 0)))
        if args.json:
            Path(args.json).write_text(
                json.dumps(report, indent=2, ensure_ascii=False),
                encoding="utf-8")
            print()
            print(f"  full report -> {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
