"""
add_phoneme_crystals_v5.py -- crystalize r-controlled vowels + vowel teams.

Per-item crystals (15) + 2 family-summary crystals (r-controlled,
vowel-team).  Each per-item crystal carries the spelling-to-sound rule
(e.g., 'ai = long-A sound = /eɪ/, as in rain') plus the measured codec
operator pattern.
"""
from __future__ import annotations

import json
import urllib.request
import urllib.error
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
STREAMS_PATH = SCRIPT_DIR / "phoneme_audio_streams_v5_2026_05_01.json"

OP_NAMES = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
            "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]


# r-controlled vowel friendly map: key -> (label, IPA, alts, example)
RCONTROL_FRIENDLY = {
    "rcontrol:ar": ("ar (as in 'car')", "/ɑr/",
                    ["ar", "ar sound", "the ar", "ar as in car",
                     "r-controlled ar", "car sound"],
                    "car"),
    "rcontrol:er": ("er (as in 'her')", "/ɝ/",
                    ["er", "er sound", "the er", "er as in her",
                     "r-controlled er", "her sound"],
                    "her"),
    "rcontrol:ir": ("ir (as in 'bird')", "/ɝ/",
                    ["ir", "ir sound", "the ir", "ir as in bird",
                     "r-controlled ir", "bird sound"],
                    "bird"),
    "rcontrol:or": ("or (as in 'for')", "/ɔr/",
                    ["or sound", "the or", "or as in for",
                     "r-controlled or", "for sound"],
                    "for"),
    "rcontrol:ur": ("ur (as in 'turn')", "/ɝ/",
                    ["ur", "ur sound", "the ur", "ur as in turn",
                     "r-controlled ur", "turn sound"],
                    "turn"),
}


# vowel team friendly map: key -> (label, IPA, alts, example, "long-X" tag)
TEAM_FRIENDLY = {
    "team:ai":  ("ai (as in 'rain')",   "/eɪ/", ["ai", "ai sound", "ai team",
                 "vowel team ai", "rain sound", "ai = long a"],   "rain",  "long-a"),
    "team:ay":  ("ay (as in 'day')",    "/eɪ/", ["ay sound", "ay team",
                 "vowel team ay", "day sound", "ay = long a"],    "day",   "long-a"),
    "team:ee":  ("ee (as in 'bee')",    "/iː/", ["ee", "ee sound", "ee team",
                 "vowel team ee", "bee sound", "ee = long e"],    "bee",   "long-e"),
    "team:ea":  ("ea (as in 'bean')",   "/iː/", ["ea", "ea sound", "ea team",
                 "vowel team ea", "bean sound", "ea = long e"],   "bean",  "long-e"),
    "team:ie":  ("ie (as in 'pie')",    "/aɪ/", ["ie", "ie sound", "ie team",
                 "vowel team ie", "pie sound", "ie = long i"],    "pie",   "long-i"),
    "team:igh": ("igh (as in 'light')", "/aɪ/", ["igh", "igh sound",
                 "igh team", "vowel team igh", "light sound",
                 "igh = long i"],                                 "light", "long-i"),
    "team:oa":  ("oa (as in 'boat')",   "/oʊ/", ["oa", "oa sound", "oa team",
                 "vowel team oa", "boat sound", "oa = long o"],   "boat",  "long-o"),
    "team:oo":  ("oo (as in 'food')",   "/uː/", ["oo team",
                 "vowel team oo", "food sound", "oo = long u"],   "food",  "long-u"),
    "team:ue":  ("ue (as in 'blue')",   "/uː/", ["ue", "ue sound", "ue team",
                 "vowel team ue", "blue sound", "ue = long u"],   "blue",  "long-u"),
    "team:ew":  ("ew (as in 'new')",    "/uː/", ["ew", "ew sound", "ew team",
                 "vowel team ew", "new sound", "ew = long u"],    "new",   "long-u"),
}


# Family summaries
FAMILY_TRIGGERS = {
    "r-controlled": (
        ["r-controlled vowel", "r controlled vowel", "r-controlled vowels",
         "what is an r-controlled vowel", "bossy r", "vowel + r"],
        "R-controlled vowels are vowels followed by R, where the R changes "
        "the vowel sound. Members: ar /ɑr/ (car), er /ɝ/ (her), "
        "ir /ɝ/ (bird), or /ɔr/ (for), ur /ɝ/ (turn). er, ir, ur are "
        "acoustically the same /ɝ/ — only the spelling differs."
    ),
    "vowel-team": (
        ["vowel team", "vowel teams", "what is a vowel team", "vowel pair",
         "vowel digraph", "spelling pattern vowel"],
        "Vowel teams are two letters that spell one vowel sound. Long-a "
        "team: ai (rain), ay (day). Long-e: ee (bee), ea (bean). Long-i: "
        "ie (pie), igh (light). Long-o: oa (boat). Long-u: oo (food), "
        "ue (blue), ew (new)."
    ),
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
        print(f"v5 streams missing: {STREAMS_PATH}")
        return 2
    with open(STREAMS_PATH, encoding="utf-8") as f:
        v5 = json.load(f)
    rcontrol = v5.get("rcontrol", {})
    teams = v5.get("teams", {})

    ok = 0
    fail = 0

    # r-controlled vowels
    for key, (label, ipa, alts, example) in RCONTROL_FRIENDLY.items():
        if key not in rcontrol:
            print(f"  SKIP (no audio): {key}")
            continue
        h = rcontrol[key]["histogram_pct"]
        ts = top3(h)
        rc_short = key.replace("rcontrol:", "")
        first_word = f"rcontrol_{rc_short}"
        triggers = [
            f"rcontrol {rc_short}",
            f"the {rc_short} sound",
            label.split()[0],  # bare 'ar', 'er', 'ir', 'or', 'ur'
        ] + alts
        triggers = list(dict.fromkeys(triggers))
        fact = (
            f"{first_word}: r-controlled vowel {label}, IPA {ipa} - audio "
            f"codec emits operator pattern: {ts}. Example word: {example}."
        )
        if add_crystal(first_word, triggers, fact):
            ok += 1
            print(f"  +{first_word}: {ts}")
        else:
            fail += 1
            print(f"  FAIL {first_word}")

    # Vowel teams
    for key, (label, ipa, alts, example, vowel_class) in TEAM_FRIENDLY.items():
        if key not in teams:
            print(f"  SKIP (no audio): {key}")
            continue
        h = teams[key]["histogram_pct"]
        ts = top3(h)
        team_short = key.replace("team:", "")
        first_word = f"team_{team_short}"
        triggers = [
            f"team {team_short}",
            f"the {team_short} team",
            f"{team_short} as in {example}",
        ] + alts
        triggers = list(dict.fromkeys(triggers))
        fact = (
            f"{first_word}: vowel team {label} = {vowel_class} sound, IPA "
            f"{ipa} - audio codec emits operator pattern: {ts}. Example "
            f"word: {example}."
        )
        if add_crystal(first_word, triggers, fact):
            ok += 1
            print(f"  +{first_word} [{vowel_class}]: {ts}")
        else:
            fail += 1
            print(f"  FAIL {first_word}")

    # Family summaries
    if rcontrol:
        avg = {op: 0.0 for op in OP_NAMES}
        for _, info in rcontrol.items():
            for op in OP_NAMES:
                avg[op] += info["histogram_pct"][op]
        n = len(rcontrol)
        for op in OP_NAMES:
            avg[op] = round(avg[op] / n, 1)
        ts = top3(avg)
        triggers, desc = FAMILY_TRIGGERS["r-controlled"]
        first_word = "rcontrolled_family"
        fact = (
            f"{first_word}: {desc} Average audio operator pattern across "
            f"{n} members: {ts}."
        )
        if add_crystal(first_word, triggers, fact):
            ok += 1
            print(f"  +{first_word}: {ts}")

    if teams:
        avg = {op: 0.0 for op in OP_NAMES}
        for _, info in teams.items():
            for op in OP_NAMES:
                avg[op] += info["histogram_pct"][op]
        n = len(teams)
        for op in OP_NAMES:
            avg[op] = round(avg[op] / n, 1)
        ts = top3(avg)
        triggers, desc = FAMILY_TRIGGERS["vowel-team"]
        first_word = "vowelteam_family"
        fact = (
            f"{first_word}: {desc} Average audio operator pattern across "
            f"{n} members: {ts}."
        )
        if add_crystal(first_word, triggers, fact):
            ok += 1
            print(f"  +{first_word}: {ts}")

    print(f"\nadded {ok}, failed {fail}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
