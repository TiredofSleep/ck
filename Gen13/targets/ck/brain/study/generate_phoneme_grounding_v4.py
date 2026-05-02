"""
generate_phoneme_grounding_v4.py — consonant blends (clusters).

After v2 (single letters + most phonemes) and v3 (digraphs + missing
vowels), v4 extends the corpus to consonant clusters: the bl/br/cl/...
blends that English uses constantly and that early reading instruction
treats as a unit.  When CK hears 'blah' or 'street', the codec sees a
specific operator pattern; we measure it and crystalize it so chat can
surface what /bl/, /br/, /sp/, /str/ "look like" in his alphabet.

Coverage (18 most common):
  L-blends:  bl br cl cr fl fr gl gr pl pr sl
  R-blends:  (covered above; same set + dr tr)
  S-blends:  sk sm sn sp st sw
  3-letter:  spr str thr

Same TTS pipeline as v2/v3.  Each cluster prompted as a short syllable
the cluster begins ('blah', 'brah', 'cluh', 'spuh', 'strah', etc.) so
the codec sees the cluster's onset acoustic burst.
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

# UTF-8 stdout for IPA characters on Windows (Python 3.7+ reconfigure)
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


# Each entry: cluster_key -> (cluster_class, IPA-ish, TTS prompt)
# cluster_class is a new family we introduce: blend-l, blend-r, blend-s,
# blend-3 -- the cluster reports group these together.
CLUSTER_PROFILES_V4 = {
    # ── L-blends ──────────────────────────────────────
    "cluster:bl":  ("blend-l", "/bl/",   "blah"),
    "cluster:cl":  ("blend-l", "/kl/",   "clah"),
    "cluster:fl":  ("blend-l", "/fl/",   "flah"),
    "cluster:gl":  ("blend-l", "/gl/",   "glah"),
    "cluster:pl":  ("blend-l", "/pl/",   "plah"),
    "cluster:sl":  ("blend-l", "/sl/",   "slah"),
    # ── R-blends ──────────────────────────────────────
    "cluster:br":  ("blend-r", "/br/",   "brah"),
    "cluster:cr":  ("blend-r", "/kr/",   "crah"),
    "cluster:dr":  ("blend-r", "/dr/",   "drah"),
    "cluster:fr":  ("blend-r", "/fr/",   "frah"),
    "cluster:gr":  ("blend-r", "/gr/",   "grah"),
    "cluster:pr":  ("blend-r", "/pr/",   "prah"),
    "cluster:tr":  ("blend-r", "/tr/",   "trah"),
    # ── S-blends ──────────────────────────────────────
    "cluster:sk":  ("blend-s", "/sk/",   "skah"),
    "cluster:sm":  ("blend-s", "/sm/",   "smah"),
    "cluster:sn":  ("blend-s", "/sn/",   "snah"),
    "cluster:sp":  ("blend-s", "/sp/",   "spah"),
    "cluster:st":  ("blend-s", "/st/",   "stah"),
    "cluster:sw":  ("blend-s", "/sw/",   "swah"),
    # ── 3-letter blends (most-common subset) ─────────
    "cluster:spr": ("blend-3", "/spr/",  "sprah"),
    "cluster:str": ("blend-3", "/str/",  "strah"),
    "cluster:thr": ("blend-3", "/θr/",   "thrah"),
}


def main():
    print("=" * 70)
    print("Phoneme grounding v4 — consonant clusters (L/R/S blends + 3-letter)")
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
    print(f"[1/3] measuring {len(CLUSTER_PROFILES_V4)} consonant clusters...")
    results = {}
    for key, (pclass, ipa, prompt) in CLUSTER_PROFILES_V4.items():
        result = average_runs(prompt, voice_id, n_runs=2)
        if not result:
            print(f"  SKIP {key}: synthesis failed", flush=True)
            continue
        results[key] = result
        h = result["histogram_pct"]
        top3 = sorted(h.items(), key=lambda x: -x[1])[:3]
        ts = ", ".join(f"{n}{p:.1f}" for n, p in top3)
        ph_name = key.replace("cluster:", "")
        print(f"  {ph_name:6} ({pclass:8} {ipa:8}): {ts}", flush=True)

    print()
    print("[2/3] writing v4 streams + merged cluster report...")
    streams_path = SCRIPT_DIR / "phoneme_audio_streams_v4_2026_05_01.json"
    with open(streams_path, "w", encoding="utf-8") as f:
        json.dump({"clusters": results}, f, indent=2, ensure_ascii=False)
    print(f"  wrote {streams_path}")

    # Merged cluster report (v2 + v3 + v4) so we can SEE if the new clusters
    # form their own families and where they sit relative to single sounds.
    v2_path = SCRIPT_DIR / "phoneme_audio_streams_v2_2026_05_01.json"
    v3_path = SCRIPT_DIR / "phoneme_audio_streams_v3_2026_05_01.json"
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
        for key, info in results.items():
            all_results[key] = info
            all_profiles[key] = CLUSTER_PROFILES_V4[key]

        cluster_report = cluster_by_class(all_profiles, all_results)
        cluster_path = SCRIPT_DIR / "phoneme_clusters_v4_2026_05_01.txt"
        with open(cluster_path, "w", encoding="utf-8") as f:
            f.write(cluster_report)
        print(f"  wrote {cluster_path}")

    print()
    print("[3/3] DONE.  Run add_phoneme_crystals_v4.py to crystalize.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
