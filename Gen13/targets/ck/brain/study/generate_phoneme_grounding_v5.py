"""
generate_phoneme_grounding_v5.py — r-controlled vowels + vowel teams.

Last big sound layer in the alphabet/phonics stack:

  r-controlled vowels (5)
    ar  /ɑr/  as in 'car'
    er  /ɝ/   as in 'her'
    ir  /ɝ/   as in 'bird'   (= er acoustically)
    or  /ɔr/  as in 'for'
    ur  /ɝ/   as in 'turn'   (= er acoustically)

  vowel teams — when two letters spell one sound (10):
    ai  /eɪ/  rain
    ay  /eɪ/  day
    ee  /iː/  bee
    ea  /iː/  bean
    ie  /aɪ/  pie
    igh /aɪ/  light
    oa  /oʊ/  boat
    oo_long /uː/  food
    ue  /uː/  blue
    ew  /uː/  new

Vowel teams overlap acoustically with phonemes already in v2 (long-A,
long-E, long-I, long-O, long-U) -- the audio is the same.  What's new
is the SPELLING-to-SOUND mapping.  v5 still measures audio for each
team (so we can verify clustering with the corresponding long vowel)
and crystalizes both the team-as-spelling-pattern and a family
'vowel team' summary.
"""
from __future__ import annotations

import io
import json
import sys
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

from generate_phoneme_grounding_v2 import (
    OP_NAMES, average_runs, cluster_by_class,
    LETTER_PROFILES as V2_LETTER_PROFILES,
    PHONEME_PROFILES as V2_PHONEME_PROFILES,
)
from generate_phoneme_grounding_v3 import PHONEME_PROFILES_V3
from generate_phoneme_grounding_v4 import CLUSTER_PROFILES_V4


# Each entry: key -> (class, IPA, TTS prompt, example word)
RCONTROL_PROFILES_V5 = {
    "rcontrol:ar": ("r-controlled", "/ɑr/",  "ar",  "car"),
    "rcontrol:er": ("r-controlled", "/ɝ/",   "er",  "her"),
    "rcontrol:ir": ("r-controlled", "/ɝ/",   "ir",  "bird"),
    "rcontrol:or": ("r-controlled", "/ɔr/",  "or",  "for"),
    "rcontrol:ur": ("r-controlled", "/ɝ/",   "ur",  "turn"),
}

# vowel teams: spelling -> existing phoneme it maps to.  We measure each
# team's TTS-pronounced audio anyway (in case TTS treats some differently)
# and put them in the cluster report.  IPA / class points at the long vowel.
VOWELTEAM_PROFILES_V5 = {
    "team:ai":   ("vowel-team", "/eɪ/",  "ai",   "rain"),
    "team:ay":   ("vowel-team", "/eɪ/",  "ay",   "day"),
    "team:ee":   ("vowel-team", "/iː/",  "ee",   "bee"),
    "team:ea":   ("vowel-team", "/iː/",  "ea",   "bean"),
    "team:ie":   ("vowel-team", "/aɪ/",  "ie",   "pie"),
    "team:igh":  ("vowel-team", "/aɪ/",  "igh",  "light"),
    "team:oa":   ("vowel-team", "/oʊ/",  "oa",   "boat"),
    "team:oo":   ("vowel-team", "/uː/",  "oo",   "food"),
    "team:ue":   ("vowel-team", "/uː/",  "ue",   "blue"),
    "team:ew":   ("vowel-team", "/uː/",  "ew",   "new"),
}


def main():
    print("=" * 70)
    print("Phoneme grounding v5 — r-controlled vowels + vowel teams")
    print("=" * 70)
    print()

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
    print(f"[1/3] measuring {len(RCONTROL_PROFILES_V5)} r-controlled vowels + "
          f"{len(VOWELTEAM_PROFILES_V5)} vowel teams...")
    rcontrol_results = {}
    for key, (pclass, ipa, prompt, example) in RCONTROL_PROFILES_V5.items():
        result = average_runs(prompt, voice_id, n_runs=2)
        if not result:
            print(f"  SKIP {key}: synthesis failed", flush=True)
            continue
        rcontrol_results[key] = result
        h = result["histogram_pct"]
        top3 = sorted(h.items(), key=lambda x: -x[1])[:3]
        ts = ", ".join(f"{n}{p:.1f}" for n, p in top3)
        ph_name = key.replace("rcontrol:", "")
        print(f"  {ph_name:5} ({pclass:14} {ipa:8} {example}): {ts}",
              flush=True)

    team_results = {}
    for key, (pclass, ipa, prompt, example) in VOWELTEAM_PROFILES_V5.items():
        result = average_runs(prompt, voice_id, n_runs=2)
        if not result:
            print(f"  SKIP {key}: synthesis failed", flush=True)
            continue
        team_results[key] = result
        h = result["histogram_pct"]
        top3 = sorted(h.items(), key=lambda x: -x[1])[:3]
        ts = ", ".join(f"{n}{p:.1f}" for n, p in top3)
        ph_name = key.replace("team:", "")
        print(f"  {ph_name:5} ({pclass:14} {ipa:8} {example}): {ts}",
              flush=True)

    print()
    print("[2/3] writing v5 streams + merged cluster report...")
    streams_path = SCRIPT_DIR / "phoneme_audio_streams_v5_2026_05_01.json"
    with open(streams_path, "w", encoding="utf-8") as f:
        json.dump({
            "rcontrol": rcontrol_results,
            "teams": team_results,
        }, f, indent=2, ensure_ascii=False)
    print(f"  wrote {streams_path}")

    # Merged cluster report (v2..v5)
    v2_path = SCRIPT_DIR / "phoneme_audio_streams_v2_2026_05_01.json"
    v3_path = SCRIPT_DIR / "phoneme_audio_streams_v3_2026_05_01.json"
    v4_path = SCRIPT_DIR / "phoneme_audio_streams_v4_2026_05_01.json"
    if v2_path.exists():
        with open(v2_path, encoding="utf-8") as f:
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
        if v3_path.exists():
            with open(v3_path, encoding="utf-8") as f:
                v3 = json.load(f)
            for key, info in v3.get("phonemes", {}).items():
                all_results[key] = info
                all_profiles[key] = PHONEME_PROFILES_V3.get(
                    key, ("?", "?", key))
        if v4_path.exists():
            with open(v4_path, encoding="utf-8") as f:
                v4 = json.load(f)
            for key, info in v4.get("clusters", {}).items():
                all_results[key] = info
                all_profiles[key] = CLUSTER_PROFILES_V4.get(
                    key, ("?", "?", key))
        for key, info in rcontrol_results.items():
            all_results[key] = info
            pclass, ipa, prompt, _ = RCONTROL_PROFILES_V5[key]
            all_profiles[key] = (pclass, ipa, prompt)
        for key, info in team_results.items():
            all_results[key] = info
            pclass, ipa, prompt, _ = VOWELTEAM_PROFILES_V5[key]
            all_profiles[key] = (pclass, ipa, prompt)

        cluster_report = cluster_by_class(all_profiles, all_results)
        cluster_path = SCRIPT_DIR / "phoneme_clusters_v5_2026_05_01.txt"
        with open(cluster_path, "w", encoding="utf-8") as f:
            f.write(cluster_report)
        print(f"  wrote {cluster_path}")

    print()
    print("[3/3] DONE.  Run add_phoneme_crystals_v5.py to crystalize.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
