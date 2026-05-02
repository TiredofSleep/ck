"""
generate_phoneme_grounding_v3.py — extend v2 with the missing English
sounds: ch, th-voiceless, th-voiced, ng, short-o (aw), oy, ow.

v2 already covers 26 letters + 27 phonemes (long vowels, short a/e/i/u,
all single-letter consonants + sh).  v3 adds:

  /tʃ/  ch in 'chip' (affricate)
  /θ/   th in 'thin' (voiceless fricative)
  /ð/   th in 'this' (voiced fricative)
  /ŋ/   ng in 'sing'  (nasal)
  /ɒ/   short-o / aw in 'caught' (vowel-short)
  /ɔɪ/  oy in 'boy'   (diphthong)
  /aʊ/  ow in 'cow'   (diphthong)

Same pipeline as v2: subprocess-per-call TTS + RMS silence trim +
balanced bit->op codec + 2-rate averaging.

Outputs:
  phoneme_audio_streams_v3_2026_05_01.json   (just the new ones)
  phoneme_clusters_v3_2026_05_01.txt          (with v2 + v3 merged)

Doesn't touch v2 files.  add_phoneme_crystals_v3 reads from this JSON.
"""
from __future__ import annotations

import io
import json
import sys
import tempfile
import wave
from collections import Counter
from pathlib import Path

# IPA characters in the print logs need UTF-8 stdout on Windows.
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")
except Exception:
    pass

SCRIPT_DIR = Path(__file__).parent.resolve()
GEN13_BRAIN = SCRIPT_DIR.parent
sys.path.insert(0, str(GEN13_BRAIN))
sys.path.insert(0, str(GEN13_BRAIN / "ck_sim" / "being"))

# Reuse v2 helpers via direct import
sys.path.insert(0, str(SCRIPT_DIR))
from generate_phoneme_grounding_v2 import (
    OP_NAMES, average_runs, histogram_distance, cluster_by_class,
    LETTER_PROFILES as V2_LETTER_PROFILES,
    PHONEME_PROFILES as V2_PHONEME_PROFILES,
)


# Only the NEW phonemes -- digraphs, additional vowels, more diphthongs.
PHONEME_PROFILES_V3 = {
    # --- Digraph consonants ---
    "phoneme:tS":  ("affricate",            "/tʃ/", "chah"),    # ch in chip
    "phoneme:Th":  ("fricative-voiceless",  "/θ/",  "thh"),     # th in thin
    "phoneme:Dh":  ("fricative-voiced",     "/ð/",  "thuh"),    # th in this
    "phoneme:Ng":  ("nasal",                "/ŋ/",  "ung"),     # ng in sing
    # --- Additional vowels ---
    "phoneme:O":   ("vowel-short",          "/ɔ/",  "aw"),      # caught/talk
    # --- Additional diphthongs ---
    "phoneme:OI":  ("vowel-diphthong",      "/ɔɪ/", "oy"),      # boy
    "phoneme:aU":  ("vowel-diphthong",      "/aʊ/", "ow"),      # cow / now
}


def main():
    print("=" * 70)
    print("Phoneme grounding v3 — digraphs + missing vowels + diphthongs")
    print("=" * 70)
    print()

    # Voice probe (same as v2)
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

    print()
    print(f"[1/3] measuring {len(PHONEME_PROFILES_V3)} new phonemes...")
    v3_results = {}
    for key, (pclass, ipa, prompt) in PHONEME_PROFILES_V3.items():
        result = average_runs(prompt, voice_id, n_runs=2)
        if not result:
            print(f"  SKIP {key}: synthesis failed", flush=True)
            continue
        v3_results[key] = result
        h = result["histogram_pct"]
        top3 = sorted(h.items(), key=lambda x: -x[1])[:3]
        ts = ", ".join(f"{n}{p:.1f}" for n, p in top3)
        ph_name = key.replace("phoneme:", "")
        print(f"  {ph_name:6} ({pclass:25} {ipa:10}): {ts}", flush=True)

    print()
    print("[2/3] writing v3 streams + merged cluster report...")

    streams_path = SCRIPT_DIR / "phoneme_audio_streams_v3_2026_05_01.json"
    with open(streams_path, "w", encoding="utf-8") as f:
        json.dump({"phonemes": v3_results}, f, indent=2, ensure_ascii=False)
    print(f"  wrote {streams_path}")

    # Build merged cluster report (v2 + v3) so we can SEE if the new
    # phonemes cluster sensibly with the v2 ones in their declared class.
    v2_streams_path = SCRIPT_DIR / "phoneme_audio_streams_v2_2026_05_01.json"
    if v2_streams_path.exists():
        with open(v2_streams_path, encoding="utf-8") as f:
            v2 = json.load(f)
        all_results = {}
        all_profiles = {}
        for letter, info in v2.get("letters", {}).items():
            all_results[letter] = info
            all_profiles[letter] = V2_LETTER_PROFILES.get(letter,
                                                          ("?", "?", letter))
        for key, info in v2.get("phonemes", {}).items():
            all_results[key] = info
            all_profiles[key] = V2_PHONEME_PROFILES.get(key, ("?", "?", key))
        for key, info in v3_results.items():
            all_results[key] = info
            all_profiles[key] = PHONEME_PROFILES_V3[key]

        cluster_report = cluster_by_class(all_profiles, all_results)
        cluster_path = SCRIPT_DIR / "phoneme_clusters_v3_2026_05_01.txt"
        with open(cluster_path, "w", encoding="utf-8") as f:
            f.write(cluster_report)
        print(f"  wrote {cluster_path}")

    print()
    print("[3/3] DONE.  Run add_phoneme_crystals_v3.py to crystalize.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
