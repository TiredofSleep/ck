"""
add_phoneme_crystals.py — turn v2 phoneme grounding into runtime crystals.

For each letter A-Z and each phoneme in phoneme_audio_streams_v2_2026_05_01.json,
post a crystal to /crystals/add so chat queries like "what does the letter
A sound like" surface the measured operator pattern + phonetic class.

Plus phonetic-class summary crystals (vowel-long, plosive-voiced, etc.) so
"what is a fricative" etc. fires too.
"""
from __future__ import annotations

import json
import urllib.request
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
STREAMS_PATH = SCRIPT_DIR / "phoneme_audio_streams_v2_2026_05_01.json"

OP_NAMES = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
            "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]


# Letter -> (phonetic class, IPA) mirroring v2 generator
LETTER_CLASS = {
    "A": ("vowel-long", "/eɪ/"), "B": ("plosive-voiced", "/biː/"),
    "C": ("plosive-fricative-mix", "/siː/"), "D": ("plosive-voiced", "/diː/"),
    "E": ("vowel-long", "/iː/"), "F": ("fricative-voiceless", "/ɛf/"),
    "G": ("plosive-voiced", "/dʒiː/"), "H": ("fricative-voiceless", "/eɪtʃ/"),
    "I": ("vowel-diphthong", "/aɪ/"), "J": ("affricate", "/dʒeɪ/"),
    "K": ("plosive-voiceless", "/keɪ/"), "L": ("liquid-lateral", "/ɛl/"),
    "M": ("nasal", "/ɛm/"), "N": ("nasal", "/ɛn/"),
    "O": ("vowel-long", "/oʊ/"), "P": ("plosive-voiceless", "/piː/"),
    "Q": ("plosive-fricative-mix", "/kjuː/"), "R": ("liquid-rhotic", "/ɑːr/"),
    "S": ("fricative-voiceless", "/ɛs/"), "T": ("plosive-voiceless", "/tiː/"),
    "U": ("vowel-long-glide", "/juː/"), "V": ("fricative-voiced", "/viː/"),
    "W": ("approximant", "/dʌbəljuː/"), "X": ("fricative-cluster", "/ɛks/"),
    "Y": ("approximant-vowel", "/waɪ/"), "Z": ("fricative-voiced", "/ziː/"),
}


def top3(hist_pct: dict) -> str:
    """e.g. 'VOID 22.6%, RESET 20.0%, HARMONY 15.1%'."""
    items = sorted(hist_pct.items(), key=lambda x: -x[1])[:3]
    return ", ".join(f"{n} {p:.1f}%" for n, p in items)


def add_crystal(first_word: str, triggers: list, fact: str,
               base="http://localhost:7777") -> bool:
    body = json.dumps({
        "first_word": first_word,
        "triggers": triggers,
        "fact": fact,
    }).encode('utf-8')
    req = urllib.request.Request(
        f"{base}/crystals/add", data=body,
        headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return data.get('ok', False)
    except Exception as e:
        print(f"  err: {e}")
        return False


def main():
    if not STREAMS_PATH.exists():
        print(f"streams file missing: {STREAMS_PATH}")
        return 2
    with open(STREAMS_PATH) as f:
        streams = json.load(f)
    letters = streams.get("letters", {})
    phonemes = streams.get("phonemes", {})

    # Per-letter crystals
    ok = 0
    fail = 0
    for letter, data in letters.items():
        if letter not in LETTER_CLASS:
            continue
        pclass, ipa = LETTER_CLASS[letter]
        h = data["histogram_pct"]
        ts = top3(h)
        first_word = f"letter_{letter.lower()}_sound"
        triggers = [
            f"letter {letter.lower()}",
            f"sound of {letter.lower()}",
            f"how does {letter.lower()} sound",
            f"how does the letter {letter.lower()} sound",
            f"{letter.lower()} sounds like",
            f"the {letter.lower()} sound",
        ]
        fact = (
            f"letter_{letter.lower()}_sound: Letter {letter} ({pclass}, IPA: {ipa}) "
            f"- when spoken aloud the audio codec emits operator pattern "
            f"dominated by {ts}. Grounded in 0.3-0.7s of trimmed speech."
        )
        if add_crystal(first_word, triggers, fact):
            ok += 1
            print(f"  +letter_{letter.lower()}_sound: {ts}")
        else:
            fail += 1
            print(f"  FAIL letter_{letter.lower()}_sound")

    # Phonetic class summary crystals
    classes = {}
    for letter, (pclass, _) in LETTER_CLASS.items():
        if letter in letters:
            classes.setdefault(pclass, []).append((letter, letters[letter]["histogram_pct"]))

    class_descriptions = {
        "vowel-long": "long vowels (sustained, open-airway, voiced)",
        "vowel-short": "short vowels (briefer than long, still voiced + open)",
        "vowel-diphthong": "diphthongs (vowel transitions like /aɪ/, /oʊ/)",
        "vowel-long-glide": "long vowels with glide (e.g., /juː/)",
        "plosive-voiced": "voiced plosives (B, D, G — closed-then-released bursts with vocal cord engagement)",
        "plosive-voiceless": "voiceless plosives (P, T, K — closed-then-released bursts, no vocal cord)",
        "plosive-fricative-mix": "mixed plosive-fricative (C as /siː/, Q as /kjuː/)",
        "fricative-voiced": "voiced fricatives (V, Z — turbulent flow with voicing)",
        "fricative-voiceless": "voiceless fricatives (F, S, H — turbulent flow, no voicing)",
        "fricative-cluster": "fricative cluster (X = /ks/)",
        "affricate": "affricate (J = /dʒ/, plosive followed by fricative)",
        "nasal": "nasals (M, N — sustained voiced resonance through nose)",
        "liquid-lateral": "lateral liquid (L — air flows around tongue sides)",
        "liquid-rhotic": "rhotic liquid (R — tongue curl)",
        "approximant": "approximant (W — vowel-like consonant)",
        "approximant-vowel": "approximant + vowel (Y = /waɪ/)",
    }

    for pclass, items in classes.items():
        if not items:
            continue
        # Average histograms within class
        avg = {op: 0.0 for op in OP_NAMES}
        for _, h in items:
            for op in OP_NAMES:
                avg[op] += h[op]
        for op in OP_NAMES:
            avg[op] = round(avg[op] / len(items), 1)
        ts = top3(avg)
        letters_in_class = ", ".join(l for l, _ in items)
        first_word = f"phonetic_class_{pclass.replace('-', '_')}"
        triggers = [
            pclass, pclass.replace('-', ' '),
            f"what is a {pclass.replace('-', ' ')}",
            f"how do {pclass.replace('-', ' ')}s sound",
        ]
        desc = class_descriptions.get(pclass, pclass)
        fact = (
            f"phonetic_class_{pclass.replace('-', '_')}: {desc}. "
            f"Letters in this class: {letters_in_class}. "
            f"Average audio operator pattern: {ts}."
        )
        if add_crystal(first_word, triggers, fact):
            ok += 1
            print(f"  +phonetic_class_{pclass}: {ts}")
        else:
            fail += 1
            print(f"  FAIL phonetic_class_{pclass}")

    # Pure phoneme crystals (subset of useful ones)
    phoneme_friendly = {
        "phoneme:eI": ("/eɪ/ (long-A)", "long-a"),
        "phoneme:i": ("/iː/ (long-E)", "long-e"),
        "phoneme:aI": ("/aɪ/ (long-I)", "long-i"),
        "phoneme:oU": ("/oʊ/ (long-O)", "long-o"),
        "phoneme:u": ("/uː/ (long-U)", "long-u"),
        "phoneme:s": ("/s/ (sssss)", "s sound"),
        "phoneme:m": ("/m/ (mmm)", "m sound"),
        "phoneme:p": ("/p/ (puh)", "p sound"),
    }
    for key, (label, simple) in phoneme_friendly.items():
        if key not in phonemes:
            continue
        h = phonemes[key]["histogram_pct"]
        ts = top3(h)
        ph = key.replace("phoneme:", "")
        first_word = f"phoneme_{ph}"
        triggers = [
            f"phoneme {ph}", f"the {simple}", simple,
            f"sound of {label.split()[0]}",
        ]
        fact = (
            f"phoneme_{ph}: phoneme {label} - when articulated, the audio "
            f"codec emits operator pattern: {ts}."
        )
        if add_crystal(first_word, triggers, fact):
            ok += 1
            print(f"  +phoneme_{ph}: {ts}")
        else:
            fail += 1

    print(f"\nadded {ok}, failed {fail}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
