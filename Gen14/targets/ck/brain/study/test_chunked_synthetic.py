"""
test_chunked_synthetic.py — verify chunked matcher on TTS scripts.

Same scripts as test_matcher_synthetic, but processed through the
silence-split + per-chunk matcher.  Prints aggregate class / member
hits and a short play-by-play of the first chunks.
"""
from __future__ import annotations

import io
import json
import subprocess
import sys
import tempfile
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

from match_audio_to_phonics import (
    OP_NAMES, read_pcm, load_phonics_corpus, top_matches,
)
from match_audio_chunked import split_on_silence, chunk_histogram


def synthesize_via_subproc(text: str, voice_id: str, out_path: Path,
                           rate: int = 110) -> bool:
    helper = (
        "import pyttsx3\n"
        f"text = {text!r}\n"
        f"out  = {str(out_path)!r}\n"
        f"voice = {voice_id!r}\n"
        f"rate  = {rate}\n"
        "e = pyttsx3.init()\n"
        "e.setProperty('voice', voice)\n"
        "e.setProperty('rate', rate)\n"
        "e.save_to_file(text, out)\n"
        "e.runAndWait()\n"
    )
    try:
        rc = subprocess.run([sys.executable, "-c", helper],
                            capture_output=True, text=True, timeout=30)
        return rc.returncode == 0 and out_path.exists() \
            and out_path.stat().st_size > 100
    except Exception:
        return False


def ensure_pcm_format(wav_in: Path, wav_out: Path) -> bool:
    try:
        import static_ffmpeg
        static_ffmpeg.add_paths()
        cmd = ["ffmpeg", "-i", str(wav_in),
               "-acodec", "pcm_s16le", "-ac", "1", "-ar", "44100",
               "-y", "-loglevel", "error", str(wav_out)]
        rc = subprocess.run(cmd, capture_output=True, text=True)
        return rc.returncode == 0 and wav_out.exists()
    except Exception:
        return False


SCRIPTS = {
    "alphabet_full": "ay. bee. see. dee. ee. ef. jee. aitch. eye. jay. "
                     "kay. el. em. en. oh. pee. queue. ar. es. tee. you. "
                     "vee. double you. eks. why. zee.",
    "vowels":        "ay. ee. eye. oh. you. ay. ee. eye. oh. you.",
    "fricatives":    "fff. sssss. vvv. zzz. huh. shhh. fff. sssss. "
                     "vvv. zzz. huh. shhh.",
    "plosives":      "puh. tuh. kuh. buh. duh. guh.",
    "blends":        "blah. brah. cluh. spah. strah. trah. shrah.",
}


def run_one(name: str, text: str, voice_id: str, corpus: dict):
    print()
    print("=" * 70)
    print(f"SCRIPT: {name}")
    print(f"  text: {text!r}")
    print("=" * 70)

    with tempfile.TemporaryDirectory() as td:
        raw = Path(td) / "raw.wav"
        clean = Path(td) / "clean.wav"
        if not synthesize_via_subproc(text, voice_id, raw):
            print("  TTS FAILED")
            return
        if not ensure_pcm_format(raw, clean):
            print("  ffmpeg FAILED")
            return
        samples, sr = read_pcm(clean)
        chunks = split_on_silence(samples, sr,
                                   threshold_rel=0.04,
                                   min_chunk_ms=120,
                                   min_silence_ms=60)
        print(f"  audio: {len(samples)/sr:.1f}s -> {len(chunks)} chunks")

        class_hits = Counter()
        member_hits = Counter()
        for ci, (s, e) in enumerate(chunks):
            seg = samples[s:e]
            h = chunk_histogram(seg, sr)
            if not h:
                continue
            top = top_matches(h, corpus, top=1)[0]
            d, key, info = top
            class_hits[info["class"]] += 1
            member_hits[key] += 1
            if ci < 12:
                t = s / sr
                print(f"    [{ci:2d}] {t:5.2f}s dur={(e-s)/sr:.2f}s "
                      f"L1={d:5.1f} -> {key:18} ({info['class']})")

    print(f"  classes (by chunk hits):")
    for cls, n in class_hits.most_common(5):
        pct = n / max(len(chunks), 1) * 100
        print(f"    {cls:25}: {n:2d} ({pct:5.1f}%)")
    print(f"  top members:")
    for mem, n in member_hits.most_common(5):
        print(f"    {mem:20}: {n:2d}")


def main():
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
        print(f"TTS init failed: {e}", file=sys.stderr)
        return 2

    corpus = load_phonics_corpus()
    print(f"corpus: {len(corpus)} entries")
    for name, text in SCRIPTS.items():
        run_one(name, text, voice_id, corpus)
    return 0


if __name__ == "__main__":
    sys.exit(main())
