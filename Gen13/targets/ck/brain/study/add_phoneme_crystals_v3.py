"""
add_phoneme_crystals_v3.py -- crystalize the v3 phonemes (digraphs +
missing vowels + diphthongs).

Reads phoneme_audio_streams_v3_2026_05_01.json and posts to
http://localhost:7777/crystals/add for each new phoneme.

Triggers cover:
  ch / chuh / digraph ch
  th sound (voiced) / th sound (voiceless)
  ng / ung / sing sound
  aw / short o / caught
  oy / oi / boy sound
  ow / ou / cow sound
"""
from __future__ import annotations

import json
import urllib.request
import urllib.error
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
STREAMS_PATH = SCRIPT_DIR / "phoneme_audio_streams_v3_2026_05_01.json"


# Each entry: (phoneme_key_in_v3_json,  (label, simple_name, alternates, related_class))
PHONEME_FRIENDLY_V3 = {
    "phoneme:tS":  ("/tʃ/ (ch, as in chip)",       "ch sound",
                    ["ch", "ch sound", "chuh", "digraph ch", "chip sound",
                     "the ch", "say ch"], "affricate"),
    "phoneme:Th":  ("/θ/ (th-voiceless, as in thin)", "th sound (voiceless)",
                    ["th sound", "th-voiceless", "thh", "digraph th",
                     "thin sound", "voiceless th"], "fricative-voiceless"),
    "phoneme:Dh":  ("/ð/ (th-voiced, as in this)",  "th sound (voiced)",
                    ["voiced th", "th-voiced", "this sound",
                     "thuh", "the th"], "fricative-voiced"),
    "phoneme:Ng":  ("/ŋ/ (ng, as in sing)",         "ng sound",
                    ["ng", "ng sound", "ung", "digraph ng",
                     "sing sound", "nasal ng", "the ng"], "nasal"),
    "phoneme:O":   ("/ɔ/ (short-o / aw, as in caught)", "aw sound",
                    ["aw", "aw sound", "short o", "short-o",
                     "caught sound", "talk sound", "the aw"], "vowel-short"),
    "phoneme:OI":  ("/ɔɪ/ (oy, as in boy)",         "oy sound",
                    ["oy", "oy sound", "oi", "diphthong oy",
                     "boy sound", "the oy"], "vowel-diphthong"),
    "phoneme:aU":  ("/aʊ/ (ow, as in cow)",         "ow sound",
                    ["ow", "ow sound", "ou", "diphthong ow",
                     "cow sound", "the ow"], "vowel-diphthong"),
}


def top3(hist_pct: dict) -> str:
    items = sorted(hist_pct.items(), key=lambda x: -x[1])[:3]
    return ", ".join(f"{n} {p:.1f}%" for n, p in items)


def add_crystal(first_word: str, triggers: list, fact: str,
                base="http://localhost:7777") -> bool:
    body = json.dumps({
        "first_word": first_word,
        "triggers": triggers,
        "fact": fact,
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{base}/crystals/add", data=body,
        headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return data.get("ok", False)
    except urllib.error.HTTPError as e:
        if e.code == 409:
            return False
        print(f"  err: {e}")
        return False
    except Exception as e:
        print(f"  err: {e}")
        return False


def main():
    if not STREAMS_PATH.exists():
        print(f"v3 streams missing: {STREAMS_PATH}")
        return 2
    with open(STREAMS_PATH, encoding="utf-8") as f:
        v3 = json.load(f)
    phonemes = v3.get("phonemes", {})

    ok = 0
    fail = 0
    for key, (label, simple, alts, pclass) in PHONEME_FRIENDLY_V3.items():
        if key not in phonemes:
            print(f"  SKIP (no audio): {key}")
            continue
        h = phonemes[key]["histogram_pct"]
        ts = top3(h)
        ph = key.replace("phoneme:", "")
        first_word = f"phoneme_{ph}"
        triggers = [
            f"phoneme {ph.lower()}",
            f"the {simple}",
            simple,
        ] + alts
        triggers = list(dict.fromkeys(triggers))
        fact = (
            f"{first_word}: phoneme {label}, class {pclass} - when "
            f"articulated, the audio codec emits operator pattern: {ts}."
        )
        if add_crystal(first_word, triggers, fact):
            ok += 1
            print(f"  +{first_word} [{pclass}]: {ts}")
        else:
            fail += 1
            print(f"  FAIL {first_word}")

    print(f"\nadded {ok}, failed {fail}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
