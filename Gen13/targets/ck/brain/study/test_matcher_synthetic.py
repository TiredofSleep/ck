"""
test_matcher_synthetic.py — verify match_audio_to_phonics on a controlled,
TTS-generated phonics recital.

We synthesize a few different scripts that we already know the phonetic
content of, run the matcher, and check it surfaces the right phonemes
near the top.

Scripts tested:
  alphabet_full   "ay bee see dee ee ef jee aitch eye jay kay el em en
                   oh pee queue ar es tee you vee double-you eks why zee"
  vowels_only     "ay ee eye oh you ee ay oh you eye"
  fricatives      "fff sssss vvv zzz huh"
  plosives        "puh tuh kuh buh duh guh"
  consonant_blends "blah brah cluh strah"
"""
from __future__ import annotations

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

from match_audio_to_phonics import (
    OP_NAMES, force9_to_operators_balanced, read_pcm,
    trim_silence, load_phonics_corpus, top_matches, class_summary,
)


def synthesize_via_subproc(text: str, voice_id: str, out_path: Path,
                           rate: int = 100) -> bool:
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
    except Exception as e:
        print(f"  TTS error: {e}", file=sys.stderr, flush=True)
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
    "alphabet_full": ("ay. bee. see. dee. ee. ef. jee. aitch. eye. jay. "
                      "kay. el. em. en. oh. pee. queue. ar. es. tee. you. "
                      "vee. double you. eks. why. zee.",
                      "all 26 letter names; expect letter_/phoneme matches "
                      "across many classes"),
    "vowels_only":   ("ay. ee. eye. oh. you. ee. ay. oh. you. eye. "
                      "ay. ee. eye. oh. you.",
                      "long vowels only; expect vowel-long / vowel-diphthong / "
                      "vowel-long-glide near top"),
    "fricatives":    ("fff. sssss. vvv. zzz. huh. shhh. fff. sssss. "
                      "vvv. zzz. huh. shhh.",
                      "fricatives only; expect fricative-* classes near top"),
    "plosives":      ("puh. tuh. kuh. buh. duh. guh. puh. tuh. kuh. "
                      "buh. duh. guh.",
                      "plosives only; expect plosive-* classes near top"),
    "blends":        ("blah. brah. cluh. spah. strah. trah. shrah.",
                      "consonant blends; expect cluster / blend-* classes "
                      "near top"),
}


def measure_audio(wav_path: Path, trim: bool = True):
    samples, sr = read_pcm(wav_path)
    original_sec = len(samples) / sr
    if trim:
        samples = trim_silence(samples, sr, threshold_rel=0.04, pad_ms=20)
    from ck_audio_compress import pcm_to_force9
    forces = pcm_to_force9(samples, sample_rate=sr)
    ops = force9_to_operators_balanced(forces)
    if not ops:
        return None
    hist = Counter(ops)
    total = len(ops)
    return {
        "original_sec": original_sec,
        "trimmed_sec": len(samples) / sr,
        "n_ops": total,
        "histogram_pct": {OP_NAMES[i]: round(hist.get(i, 0) / total * 100, 1)
                          for i in range(10)},
    }


def run_one_script(name: str, text: str, voice_id: str, expectation: str,
                   corpus: dict, top_k: int = 8):
    print()
    print("=" * 70)
    print(f"SCRIPT: {name}")
    print(f"  text: {text!r}")
    print(f"  expecting: {expectation}")
    print("=" * 70)

    with tempfile.TemporaryDirectory() as td:
        raw = Path(td) / "raw.wav"
        clean = Path(td) / "clean.wav"
        if not synthesize_via_subproc(text, voice_id, raw, rate=110):
            print("  TTS FAILED", flush=True)
            return None
        if not ensure_pcm_format(raw, clean):
            print("  ffmpeg FAILED", flush=True)
            return None
        meas = measure_audio(clean, trim=True)

    if not meas:
        print("  measure FAILED")
        return None

    print(f"  audio: {meas['trimmed_sec']:.2f}s, "
          f"{meas['n_ops']:,} operators")
    print(f"  histogram:")
    for op in OP_NAMES:
        pct = meas["histogram_pct"][op]
        bar = "#" * int(pct / 2)
        print(f"    {op:<10}: {pct:5.1f}%  {bar}")

    matches = top_matches(meas["histogram_pct"], corpus, top=top_k)
    print(f"  top {top_k} matches:")
    for rank, (d, key, info) in enumerate(matches, 1):
        print(f"    {rank:2d}. L1={d:5.1f}  {key:18}  "
              f"({info['class']:20} {info['ipa']})")

    cs = class_summary(meas["histogram_pct"], corpus, top_per_class=1)
    classes_ranked = sorted(
        ((items[0][0], pclass, items[0])
         for pclass, items in cs.items()),
        key=lambda t: t[0])
    print(f"  TOP-3 classes (by class-best L1):")
    for d, pclass, (_, key, info) in classes_ranked[:3]:
        print(f"    L1={d:5.1f}  class={pclass:20}  best-member={key}")
    return meas


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
        print(f"voice: {voice_id}", flush=True)
    except Exception as e:
        print(f"TTS init failed: {e}", file=sys.stderr, flush=True)
        return 2

    corpus = load_phonics_corpus()
    print(f"corpus: {len(corpus)} entries (letters + phonemes + "
          f"clusters + r-controlled + teams)", flush=True)

    for name, (text, expectation) in SCRIPTS.items():
        run_one_script(name, text, voice_id, expectation, corpus)

    return 0


if __name__ == "__main__":
    sys.exit(main())
