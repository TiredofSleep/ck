"""
add_phoneme_crystals_v6.py -- spelling-pattern crystals (text-only).

The previous layers (v2..v5) all measured TTS audio for the sound and
crystalized the codec's operator pattern.  v6 covers spelling patterns
where the audio MAPS TO an already-measured phoneme so no new audio
measurement is needed -- just the spelling rule:

  Silent-letter patterns (5)
    kn = /n/      (silent k)        knee, knot
    gn = /n/      (silent g)        gnat, gnome
    wr = /r/      (silent w)        write, wrong
    mb = /m/      (silent b)        comb, climb
    gh-silent     (often silent)     light, though, thought

  Consonant digraphs that map to single phonemes (4)
    ph = /f/      photo, phone
    ck = /k/      duck, sock
    wh = /w/      what, white
    gh = /f/ or silent  laugh / cough vs light/though

  Soft-c / soft-g (2)
    soft c = /s/ before e/i/y      cell, city, cycle
    soft g = /dʒ/ before e/i/y     gem, giant, gym

  Magic-e (silent-e / VCe / open syllable) (1)
    The 'magic e' at the end of a word makes the preceding vowel say
    its long name and itself stays silent.  cap -> cape, hop -> hope.

  Schwa /ə/ (1)
    The most common vowel sound in English.  Any unstressed vowel can
    reduce to schwa: about, sofa, taken.
"""
from __future__ import annotations

import json
import urllib.request
import urllib.error
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()


# Each entry: first_word -> (triggers list, fact text)
PATTERN_CRYSTALS = {
    # ── Silent letters ────────────────────────────────
    "spelling_kn": (
        ["kn", "kn pattern", "silent k", "kn = n", "knee sound",
         "knot sound", "kn as in knee"],
        "spelling_kn: kn = /n/ (silent k). Examples: knee, knot, knife, "
        "knight, know, knock. The k stays silent; the word starts with "
        "the /n/ sound. Audio operator pattern same as phoneme_n."
    ),
    "spelling_gn": (
        ["gn", "gn pattern", "silent g", "gn = n", "gnat sound",
         "gn as in gnat", "gnome sound"],
        "spelling_gn: gn = /n/ (silent g). Examples: gnat, gnome, gnaw, "
        "sign, design (final gn). Audio operator pattern same as phoneme_n."
    ),
    "spelling_wr": (
        ["wr", "wr pattern", "silent w", "wr = r", "write sound",
         "wr as in write", "wrong sound", "wrist sound"],
        "spelling_wr: wr = /r/ (silent w). Examples: write, wrong, "
        "wrist, wrap, wrench. Audio operator pattern same as phoneme_r."
    ),
    "spelling_mb": (
        ["mb", "mb pattern", "silent b", "mb = m", "comb sound",
         "mb as in comb", "climb sound", "thumb sound"],
        "spelling_mb: word-final mb = /m/ (silent b). Examples: comb, "
        "climb, thumb, lamb, dumb, bomb. Audio operator pattern same as "
        "phoneme_m."
    ),
    "spelling_gh_silent": (
        ["gh silent", "silent gh", "gh as silent", "though sound",
         "thought sound", "light spelling"],
        "spelling_gh_silent: in many words gh is silent; the surrounding "
        "vowel team controls the sound. Examples: light /aɪ/, night /aɪ/, "
        "though /oʊ/, thought /ɔ/, thorough /ə/. Compare gh-as-/f/: "
        "laugh, cough, enough, rough, tough."
    ),
    # ── Digraphs that map to existing phonemes ──────
    "spelling_ph": (
        ["ph", "ph pattern", "ph = f", "ph as in phone", "phone sound",
         "photo sound", "ph spelling"],
        "spelling_ph: ph = /f/. Examples: phone, photo, phonics, graph, "
        "alphabet, elephant. Greek-origin spelling. Audio operator "
        "pattern same as phoneme_f."
    ),
    "spelling_ck": (
        ["ck", "ck pattern", "ck = k", "ck as in duck", "duck sound",
         "back sound", "rock sound"],
        "spelling_ck: ck = /k/ (after a short vowel at the end of a "
        "syllable). Examples: duck, back, rock, click, lock, sick. "
        "Never starts a word; only after short vowels. Audio operator "
        "pattern same as phoneme_k."
    ),
    "spelling_wh": (
        ["wh", "wh pattern", "wh as in what", "what sound", "where sound",
         "wh spelling"],
        "spelling_wh: wh = /w/ in modern American English (older "
        "pronunciation /hw/). Examples: what, when, where, why, white, "
        "wheel. Exception: wh = /h/ in 'who', 'whom', 'whose', 'whole'. "
        "Audio operator pattern same as phoneme_w."
    ),
    "spelling_gh_f": (
        ["gh as f", "laugh sound", "cough sound", "rough sound",
         "tough sound", "enough sound"],
        "spelling_gh_f: gh = /f/ in a small set of words. Examples: "
        "laugh, cough, enough, rough, tough. Audio operator pattern same "
        "as phoneme_f. Compare spelling_gh_silent for the silent case."
    ),
    # ── Soft c / soft g ─────────────────────────────
    "spelling_soft_c": (
        ["soft c", "c = s", "c as s", "ce gives s", "ci gives s",
         "cy gives s", "city sound", "cell sound"],
        "spelling_soft_c: c = /s/ before e, i, or y (soft-c rule). "
        "Examples: cell, city, cycle, face, peace, mice, ice. Otherwise "
        "c = /k/ (cat, cup, comb, public). Audio of soft c same as "
        "phoneme_s."
    ),
    "spelling_soft_g": (
        ["soft g", "g = j", "g as j", "ge gives j", "gi gives j",
         "gy gives j", "gem sound", "giant sound", "gym sound"],
        "spelling_soft_g: g = /dʒ/ before e, i, or y (soft-g rule). "
        "Examples: gem, giant, gym, age, magic, page, gentle. Otherwise "
        "g = /g/ (go, gum, dog, get, give -- exceptions). Audio of "
        "soft g same as phoneme_j (the J letter / /dʒ/)."
    ),
    # ── Magic-e ─────────────────────────────────────
    "spelling_magic_e": (
        ["magic e", "silent e", "vowel consonant e", "vce", "long vowel rule",
         "what is magic e", "cake rule", "bike rule", "long vowel pattern",
         "cvce"],
        "spelling_magic_e: word-final silent e makes the preceding "
        "vowel say its long name. cap -> cape (a -> /eɪ/), hop -> hope "
        "(o -> /oʊ/), bit -> bite (i -> /aɪ/), tub -> tube (u -> /uː/), "
        "pet -> Pete (e -> /iː/). The e itself stays silent. Pattern: "
        "vowel + consonant + silent-e (VCe). Foundational for reading "
        "long-vowel words."
    ),
    # ── Schwa ──────────────────────────────────────
    "spelling_schwa": (
        ["schwa", "uh sound", "what is schwa", "unstressed vowel",
         "neutral vowel", "about sound", "sofa sound"],
        "spelling_schwa: schwa /ə/ is the neutral, unstressed vowel "
        "sound -- the most common vowel in English. Any vowel letter "
        "can reduce to schwa in unstressed syllables: about /ə/, "
        "sofa /ə/, taken /ə/, pencil /ə/, lemon /ə/, supply /ə/. "
        "Acoustically very close to phoneme_V (short-u /ʌ/)."
    ),
}


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
    ok = 0
    fail = 0
    for first_word, (triggers, fact) in PATTERN_CRYSTALS.items():
        if add_crystal(first_word, triggers, fact):
            ok += 1
            print(f"  +{first_word}")
        else:
            fail += 1
            print(f"  FAIL/dup {first_word}")

    print(f"\nadded {ok}, failed {fail}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
