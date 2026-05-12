"""
add_phoneme_crystals_full.py -- crystalize EVERY phoneme in the v2 corpus.

The v1 add_phoneme_crystals.py only created crystals for 8 of the 27
phonemes (the long vowels + s/m/p).  This script covers the other 19
plus adds friendlier triggers so questions like "what is the b sound"
or "phoneme ah" or "how do you say th" actually surface a crystal.

Reads phoneme_audio_streams_v2_2026_05_01.json and posts to
http://localhost:7777/crystals/add for any phoneme not yet crystalized.
"""
from __future__ import annotations

import json
import urllib.request
import urllib.error
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
STREAMS_PATH = SCRIPT_DIR / "phoneme_audio_streams_v2_2026_05_01.json"

OP_NAMES = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
            "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]


# Map each phoneme key (as stored in v2 JSON) to (label, simple_name,
# alternates).  alternates are extra trigger phrases users might type.
PHONEME_FRIENDLY_FULL = {
    # ── Consonants ────────────────────────────────────
    "phoneme:b":  ("/b/ (buh)",   "b sound",   ["buh", "b sound", "the b", "say b", "letter b sound"]),
    "phoneme:d":  ("/d/ (duh)",   "d sound",   ["duh", "d sound", "the d", "say d", "letter d sound"]),
    "phoneme:f":  ("/f/ (fff)",   "f sound",   ["fff", "f sound", "the f", "fricative f", "letter f sound"]),
    "phoneme:g":  ("/g/ (guh)",   "g sound",   ["guh", "g sound", "the g", "hard g", "letter g sound"]),
    "phoneme:h":  ("/h/ (huh)",   "h sound",   ["huh", "h sound", "the h", "letter h sound", "breath sound"]),
    "phoneme:j":  ("/dʒ/ (juh)",  "j sound",   ["juh", "j sound", "the j", "affricate j", "letter j sound"]),
    "phoneme:k":  ("/k/ (kuh)",   "k sound",   ["kuh", "k sound", "the k", "hard k", "letter k sound"]),
    "phoneme:l":  ("/l/ (lll)",   "l sound",   ["lll", "l sound", "the l", "lateral l", "letter l sound"]),
    "phoneme:n":  ("/n/ (nnn)",   "n sound",   ["nnn", "n sound", "the n", "nasal n", "letter n sound"]),
    "phoneme:r":  ("/r/ (rrr)",   "r sound",   ["rrr", "r sound", "the r", "rhotic r", "letter r sound"]),
    "phoneme:t":  ("/t/ (tuh)",   "t sound",   ["tuh", "t sound", "the t", "letter t sound"]),
    "phoneme:v":  ("/v/ (vvv)",   "v sound",   ["vvv", "v sound", "the v", "voiced v", "letter v sound"]),
    "phoneme:w":  ("/w/ (wuh)",   "w sound",   ["wuh", "w sound", "the w", "approximant w", "letter w sound"]),
    "phoneme:z":  ("/z/ (zzz)",   "z sound",   ["zzz", "z sound", "the z", "voiced z", "letter z sound", "buzz sound"]),
    # ── Short vowels (already in v2 corpus) ───────────
    "phoneme:ae": ("/æ/ (short-a, as in cat)", "short a sound",
                  ["short a", "short-a", "ah as in cat", "cat sound", "the a in cat"]),
    "phoneme:E":  ("/ɛ/ (short-e, as in bed)", "short e sound",
                  ["short e", "short-e", "eh as in bed", "bed sound", "the e in bed"]),
    "phoneme:I":  ("/ɪ/ (short-i, as in bit)", "short i sound",
                  ["short i", "short-i", "ih as in bit", "bit sound", "the i in bit"]),
    "phoneme:V":  ("/ʌ/ (short-u, as in cup)", "short u sound",
                  ["short u", "short-u", "uh as in cup", "cup sound", "the u in cup"]),
    # ── (long S already in some forms; keep as 'S' shape) ─
    "phoneme:S":  ("/ʃ/ (sh, as in ship)", "sh sound",
                  ["sh sound", "sh", "ship sound", "shh", "the sh", "digraph sh"]),
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
        # 409 = duplicate, that's fine; we just skip
        if e.code == 409:
            return False
        print(f"  err: {e}")
        return False
    except Exception as e:
        print(f"  err: {e}")
        return False


def main():
    if not STREAMS_PATH.exists():
        print(f"streams file missing: {STREAMS_PATH}")
        return 2
    with open(STREAMS_PATH, encoding="utf-8") as f:
        streams = json.load(f)
    phonemes = streams.get("phonemes", {})

    ok = 0
    fail = 0
    for key, (label, simple, alts) in PHONEME_FRIENDLY_FULL.items():
        if key not in phonemes:
            print(f"  SKIP (no audio): {key}")
            continue
        h = phonemes[key]["histogram_pct"]
        ts = top3(h)
        ph = key.replace("phoneme:", "")
        # Sanitize first_word for keys like "S" / "ae" / "V" / "I" / "E"
        # (these are case-sensitive in v2 keys)
        first_word = f"phoneme_{ph.replace(':', '_')}"
        triggers = [
            f"phoneme {ph.lower()}",
            f"the {simple}",
            simple,
        ] + alts
        # Dedup triggers
        triggers = list(dict.fromkeys(triggers))
        fact = (
            f"{first_word}: phoneme {label} - when articulated, the audio "
            f"codec emits operator pattern: {ts}."
        )
        if add_crystal(first_word, triggers, fact):
            ok += 1
            print(f"  +{first_word}: {ts}")
        else:
            fail += 1
            # may be duplicate -- not a bug

    print(f"\nadded {ok}, failed/skipped {fail}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
