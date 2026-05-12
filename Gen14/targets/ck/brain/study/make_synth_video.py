"""
make_synth_video.py — build a local synthetic test video with known audio.

We know what's in it (we made it), so we can verify watch_and_summarize
classifies it correctly.

Default: alphabet recital + cycling color frames.
"""
from __future__ import annotations

import io
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


def get_ffmpeg():
    try:
        import static_ffmpeg
        static_ffmpeg.add_paths()
        import shutil
        return shutil.which("ffmpeg")
    except Exception:
        return None


def synth_alphabet_wav(out_path: Path, voice_id: str) -> bool:
    """Synthesize a 30-second alphabet recital."""
    helper = (
        "import pyttsx3\n"
        f"text = 'ay. bee. see. dee. ee. ef. jee. aitch. eye. jay. kay. el. em. en. oh. pee. queue. ar. es. tee. you. vee. double you. eks. why. zee.'\n"
        f"out = {str(out_path)!r}\n"
        f"voice = {voice_id!r}\n"
        "e = pyttsx3.init()\n"
        "e.setProperty('voice', voice)\n"
        "e.setProperty('rate', 110)\n"
        "e.save_to_file(text, out)\n"
        "e.runAndWait()\n"
    )
    rc = subprocess.run([sys.executable, "-c", helper],
                        capture_output=True, text=True, timeout=60)
    if rc.returncode != 0:
        print(f"TTS fail: {rc.stderr[:300]}", file=sys.stderr)
        return False
    return out_path.exists()


def make_color_frames(out_dir: Path, n: int = 30, size: int = 96):
    """Make N PNG frames cycling through hues at uniform brightness so
    the edge encoder gets distinct colored regions per frame."""
    from PIL import Image
    import numpy as np
    import colorsys
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for i in range(n):
        # Hue cycles over the full circle across frames; within a frame,
        # quadrants get four different hues so encode_edges sees boundaries.
        hue_base = i / n  # 0 .. 1
        rgb_quad = []
        for q in range(4):
            h = (hue_base + q * 0.25) % 1.0
            r, g, b = colorsys.hsv_to_rgb(h, 0.9, 0.9)
            rgb_quad.append((int(r*255), int(g*255), int(b*255)))
        img = np.zeros((size, size, 3), dtype=np.uint8)
        half = size // 2
        img[:half, :half] = rgb_quad[0]   # top-left
        img[:half, half:] = rgb_quad[1]   # top-right
        img[half:, :half] = rgb_quad[2]   # bottom-left
        img[half:, half:] = rgb_quad[3]   # bottom-right
        p = out_dir / f"frame_{i:04d}.png"
        Image.fromarray(img).save(p)
        paths.append(p)
    return paths


def assemble_video(audio_wav: Path, frames_dir: Path, out_video: Path,
                   fps_in: float = 1.0):
    ffmpeg_exe = get_ffmpeg()
    if not ffmpeg_exe:
        return False
    cmd = [
        ffmpeg_exe,
        "-framerate", str(fps_in),
        "-i", str(frames_dir / "frame_%04d.png"),
        "-i", str(audio_wav),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-shortest",
        "-y", "-loglevel", "error",
        str(out_video),
    ]
    rc = subprocess.run(cmd, capture_output=True, text=True)
    if rc.returncode != 0:
        print(f"ffmpeg assemble failed: {rc.stderr[:300]}", file=sys.stderr)
        return False
    return out_video.exists()


def main():
    out_video = SCRIPT_DIR / "synth_alphabet_clip.mp4"
    print(f"target: {out_video}")
    try:
        import pyttsx3
        tmp = pyttsx3.init()
        voices = [v for v in tmp.getProperty("voices")
                  if "EN-US" in v.id.upper()]
        if not voices:
            voices = tmp.getProperty("voices")
        voice_id = voices[0].id
        del tmp
        print(f"voice: {voice_id}")
    except Exception as e:
        print(f"TTS init fail: {e}", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory() as td:
        wav = Path(td) / "alphabet.wav"
        print("[1/3] TTS alphabet recital...")
        if not synth_alphabet_wav(wav, voice_id):
            return 3
        print(f"  {wav.name} ({wav.stat().st_size} bytes)")
        print("[2/3] generating 30 cycling-color frames...")
        frames_dir = Path(td) / "frames"
        frames = make_color_frames(frames_dir, n=30, size=96)
        print(f"  {len(frames)} frames")
        print("[3/3] assembling MP4...")
        ok = assemble_video(wav, frames_dir, out_video, fps_in=1.0)
        if not ok:
            return 4

    if out_video.exists():
        print(f"DONE: {out_video} ({out_video.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
