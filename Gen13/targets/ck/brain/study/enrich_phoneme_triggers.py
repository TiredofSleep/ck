"""
enrich_phoneme_triggers.py -- broaden the trigger lists on phoneme/letter
runtime crystals so natural-language queries fire them.

Problem the v1 add_phoneme_crystals.py didn't catch:
  user query                       had no matching trigger
  ---------------------------------+--------------------------
  what is a fricative              triggers were 'fricative-voiceless',
                                   'fricative-voiced', etc; bare
                                   'fricative' was never registered
  what is a plosive                same; only 'plosive-voiced' etc.
  what is a vowel                  same; only 'vowel-long' etc.
  tell me about long vowels        only had 'vowel long', not 'long vowel'
  how do plosives sound (plural)   word-boundary regex now blocks the
                                   bare 'plosive'->'plosives' jump

Fix: extend each crystal's triggers list with:
  - bare class word ('fricative', 'plosive', 'vowel')
  - plural ('fricatives', 'plosives', 'vowels')
  - common alternate orders ('long vowel', 'long vowels',
    'voiced fricative', 'voiceless plosive', etc.)

We edit the on-disk runtime_crystals.json directly because
add_crystal_runtime() blocks duplicate first_words by design. After
the file is rewritten the server reloads on next module import or via
a /crystals/reload endpoint.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import List, Tuple

CRYSTALS_PATH = (
    Path(__file__).parent.parent.parent.parent.parent
    / "var" / "runtime_crystals.json"
).resolve()


# ── Per-class extra triggers ─────────────────────────────────────────
# When the crystal first_word is 'phonetic_class_<class>', we add these
# triggers so users can ask in everyday English.

CLASS_EXTRA_TRIGGERS = {
    "vowel-long":            ["long vowel", "long vowels", "vowel", "vowels",
                              "long a", "long e", "long i", "long o",
                              "long-a sound", "long-e sound"],
    "vowel-short":           ["short vowel", "short vowels", "vowel", "vowels"],
    "vowel-diphthong":       ["diphthong", "diphthongs", "vowel transition",
                              "vowel", "vowels"],
    "vowel-long-glide":      ["glide vowel", "long glide", "yu sound",
                              "vowel", "vowels"],
    "plosive-voiced":        ["plosive", "plosives", "voiced plosive",
                              "voiced plosives", "stop consonant",
                              "b sound", "d sound", "g sound"],
    "plosive-voiceless":     ["plosive", "plosives", "voiceless plosive",
                              "voiceless plosives", "stop consonant",
                              "p sound", "t sound", "k sound"],
    "plosive-fricative-mix": ["plosive", "fricative", "mixed sound"],
    "fricative-voiced":      ["fricative", "fricatives", "voiced fricative",
                              "voiced fricatives", "v sound", "z sound"],
    "fricative-voiceless":   ["fricative", "fricatives", "voiceless fricative",
                              "voiceless fricatives", "f sound", "s sound",
                              "h sound"],
    "fricative-cluster":     ["fricative", "fricatives", "consonant cluster",
                              "x sound"],
    "affricate":             ["affricate", "affricates", "j sound"],
    "nasal":                 ["nasal", "nasals", "nasal sound", "nasal sounds",
                              "m sound", "n sound", "nose sound"],
    "liquid-lateral":        ["liquid", "lateral", "l sound"],
    "liquid-rhotic":         ["liquid", "rhotic", "r sound"],
    "approximant":           ["approximant", "approximants", "w sound",
                              "glide consonant"],
    "approximant-vowel":     ["approximant", "y sound", "yi sound"],
}


# ── Per-letter extra triggers ────────────────────────────────────────
# Add the simple English form ('a sound', 'sound a', 'pronounce a') so
# more natural queries fire each letter.

def letter_extra_triggers(letter: str) -> List[str]:
    L = letter.lower()
    return [
        f"how to pronounce {L}",
        f"how do you say {L}",
        f"pronounce {L}",
        f"say the letter {L}",
        f"say {L}",
        f"the letter {L}",
        f"speak {L}",
        f"how is {L} pronounced",
    ]


# ── Per-phoneme extra triggers ───────────────────────────────────────

PHONEME_EXTRA = {
    "phoneme_eI": ["long a sound", "say long a", "pronounce long a", "ay sound"],
    "phoneme_i":  ["long e sound", "say long e", "pronounce long e", "ee sound"],
    "phoneme_aI": ["long i sound", "say long i", "pronounce long i", "eye sound"],
    "phoneme_oU": ["long o sound", "say long o", "pronounce long o", "oh sound"],
    "phoneme_u":  ["long u sound", "say long u", "pronounce long u", "oo sound"],
    "phoneme_s":  ["sss", "hiss", "snake sound"],
    "phoneme_m":  ["mmm", "humming sound"],
    "phoneme_p":  ["puh", "p sound"],
}


def first_word(fact: str) -> str:
    return fact.split(":", 1)[0].strip()


def main() -> int:
    if not CRYSTALS_PATH.exists():
        print(f"runtime crystals not found: {CRYSTALS_PATH}")
        return 2
    with open(CRYSTALS_PATH, encoding="utf-8") as f:
        data = json.load(f)

    enriched = 0
    skipped = 0

    for entry in data:
        fw = first_word(entry["fact"])
        existing = list(entry.get("triggers", []))
        existing_set = set(existing)
        new_triggers: List[str] = []

        # phonetic_class_<class>
        if fw.startswith("phonetic_class_"):
            # the class string is everything after the prefix, with _ -> -
            cls_key_underscored = fw[len("phonetic_class_"):]
            cls_key = cls_key_underscored.replace("_", "-")
            extras = CLASS_EXTRA_TRIGGERS.get(cls_key, [])
            for t in extras:
                if t not in existing_set:
                    new_triggers.append(t)
                    existing_set.add(t)

        # letter_<x>_sound
        elif fw.startswith("letter_") and fw.endswith("_sound"):
            letter = fw[len("letter_"):-len("_sound")]
            for t in letter_extra_triggers(letter):
                if t not in existing_set:
                    new_triggers.append(t)
                    existing_set.add(t)

        # phoneme_<x>
        elif fw.startswith("phoneme_"):
            extras = PHONEME_EXTRA.get(fw, [])
            for t in extras:
                if t not in existing_set:
                    new_triggers.append(t)
                    existing_set.add(t)

        else:
            skipped += 1
            continue

        if new_triggers:
            entry["triggers"] = existing + new_triggers
            enriched += 1
            print(f"  +{len(new_triggers)} triggers -> {fw}")

    # Save
    with open(CRYSTALS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\nenriched {enriched} crystals; skipped {skipped} (not phoneme/letter/class)")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
