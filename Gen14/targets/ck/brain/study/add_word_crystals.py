"""
add_word_crystals.py — author runtime crystals for the word vocabulary.

Each kids-vocab word becomes a runtime crystal whose:
  - first_word: word_<word>
  - triggers:   the word itself + 'word <X>' + 'spell <X>' + 'sounds in <X>'
  - fact:       lists the phoneme sequence + IPA-ish breakdown
  - op_signature: combined op_signature of the word's phonemes (for state-aware
                  surfacing -- when CK's cortex is in a phonics-favoring state,
                  these crystals can volunteer)
  - related:    bridges back to the phoneme/letter/cluster crystals the word
                is built from.  This is paper 4 step 3 in action: when
                'cat' fires, related crystals letter_c_sound / phoneme_ae /
                phoneme_t are scored against state and may surface alongside.

The bridges are the bridge.  Once these crystals are in the runtime
store, asking CK 'what is the word cat' surfaces:
    word_cat: cat = /k/ + /ae/ + /t/ ...
    + (related, if state matches) phoneme_k, phoneme_ae, phoneme_t

i.e. CK answers a word query by lighting up its phoneme components --
the inverse of how he'd answer a phoneme query by lighting up the word
crystals that contain that phoneme.
"""
from __future__ import annotations

import json
import sys
import urllib.request
import urllib.error
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
GEN13_BRAIN = SCRIPT_DIR.parent
sys.path.insert(0, str(GEN13_BRAIN))
sys.path.insert(0, str(SCRIPT_DIR))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from kids_word_vocab import WORD_VOCAB


# Map each phoneme corpus key to its corresponding crystal first_word
# (mirrors the assignment used by the v2..v6 add_*.py scripts).
def crystal_for_key(key: str) -> str:
    if key.startswith("letter:"):
        return f"letter_{key.split(':',1)[1].lower()}_sound"
    if key.startswith("phoneme:"):
        return f"phoneme_{key.split(':',1)[1]}"
    if key.startswith("cluster:"):
        return f"cluster_{key.split(':',1)[1]}"
    if key.startswith("rcontrol:"):
        return f"rcontrol_{key.split(':',1)[1]}"
    if key.startswith("team:"):
        return f"team_{key.split(':',1)[1]}"
    return None


# Pretty IPA for facts.  Same mapping the v2..v5 generators used.
_IPA = {
    "phoneme:eI": "/eɪ/", "phoneme:i": "/iː/", "phoneme:aI": "/aɪ/",
    "phoneme:oU": "/oʊ/", "phoneme:u": "/uː/",
    "phoneme:ae": "/æ/", "phoneme:E": "/ɛ/", "phoneme:I": "/ɪ/",
    "phoneme:V": "/ʌ/", "phoneme:O": "/ɔ/",
    "phoneme:OI": "/ɔɪ/", "phoneme:aU": "/aʊ/",
    "phoneme:tS": "/tʃ/", "phoneme:Th": "/θ/", "phoneme:Dh": "/ð/",
    "phoneme:Ng": "/ŋ/", "phoneme:S": "/ʃ/",
    "team:ai": "/eɪ/", "team:ay": "/eɪ/", "team:ee": "/iː/",
    "team:ea": "/iː/", "team:ie": "/aɪ/", "team:igh": "/aɪ/",
    "team:oa": "/oʊ/", "team:oo": "/uː/", "team:ue": "/uː/",
    "team:ew": "/uː/",
    "rcontrol:ar": "/ɑr/", "rcontrol:er": "/ɝ/", "rcontrol:ir": "/ɝ/",
    "rcontrol:or": "/ɔr/", "rcontrol:ur": "/ɝ/",
    "cluster:bl": "/bl/", "cluster:cl": "/kl/", "cluster:fl": "/fl/",
    "cluster:gl": "/gl/", "cluster:pl": "/pl/", "cluster:sl": "/sl/",
    "cluster:br": "/br/", "cluster:cr": "/kr/", "cluster:dr": "/dr/",
    "cluster:fr": "/fr/", "cluster:gr": "/gr/", "cluster:pr": "/pr/",
    "cluster:tr": "/tr/", "cluster:sk": "/sk/", "cluster:sm": "/sm/",
    "cluster:sn": "/sn/", "cluster:sp": "/sp/", "cluster:st": "/st/",
    "cluster:sw": "/sw/", "cluster:spr": "/spr/", "cluster:str": "/str/",
    "cluster:thr": "/θr/",
}
def _ipa(key: str) -> str:
    if key in _IPA:
        return _IPA[key]
    if key.startswith("phoneme:"):
        ph = key.split(":", 1)[1]
        return f"/{ph}/"
    if key.startswith("letter:"):
        return f"({key.split(':',1)[1]})"
    return key


def add_crystal(first_word, triggers, fact,
                op_signature=None, related=None,
                base="http://localhost:7777") -> tuple:
    """Returns (success, status_str)."""
    body = json.dumps({
        "first_word": first_word,
        "triggers": list(triggers),
        "fact": fact,
        "op_signature": list(op_signature) if op_signature else None,
        "related": list(related) if related else None,
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{base}/crystals/add", data=body,
        headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return data.get("ok", False), str(data)
    except urllib.error.HTTPError as e:
        if e.code == 409:
            return False, "duplicate"
        return False, f"HTTPError {e.code}"
    except Exception as e:
        return False, str(e)


def get_phoneme_op_signature(crystal_first_word: str) -> tuple:
    """Look up an existing phoneme/cluster/team crystal's op_signature
    from the runtime crystals JSON.  Returns empty tuple if not found.
    """
    path = (SCRIPT_DIR.parent.parent.parent / "var"
            / "runtime_crystals.json").resolve()
    if not path.exists():
        return ()
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return ()
    for entry in data:
        fw = entry["fact"].split(":", 1)[0].strip()
        if fw == crystal_first_word:
            sig = entry.get("op_signature") or []
            return tuple(sig)
    return ()


def main():
    ok = 0
    skip = 0
    fail = 0
    print(f"authoring {len(WORD_VOCAB)} word crystals...")
    print()
    for word, pattern in WORD_VOCAB.items():
        # Build IPA-ish breakdown
        ipa_parts = " + ".join(_ipa(k) for k in pattern)
        # Sequence of corpus keys, human-readable
        key_seq = " -> ".join(pattern)
        # related = the phoneme/letter/cluster crystals
        related = []
        for k in pattern:
            cf = crystal_for_key(k)
            if cf and cf not in related:
                related.append(cf)
        # op_signature = union of related crystals' op_signatures
        op_sig = set()
        for cf in related:
            for op in get_phoneme_op_signature(cf):
                op_sig.add(op)
        op_signature = tuple(sorted(op_sig)) if op_sig else None

        # Triggers: the word + a few natural phrases
        # Don't trigger on bare 1-2 letter words (would collide constantly);
        # for those use only phrase forms.
        first_word = f"word_{word}"
        triggers = [
            f"word {word}",
            f"the word {word}",
            f"spell {word}",
            f"sounds in {word}",
            f"how do you spell {word}",
        ]
        if len(word) >= 3:
            triggers.insert(0, word)
            triggers.insert(0, f"say {word}")

        fact = (
            f"{first_word}: word '{word}' = {ipa_parts}.  Phoneme sequence: "
            f"{key_seq}.  CK can recognize this when its phoneme components "
            f"appear in the audio operator stream in order."
        )

        success, status = add_crystal(first_word, triggers, fact,
                                       op_signature=op_signature,
                                       related=related)
        if success:
            ok += 1
            print(f"  +{first_word:20} <- {ipa_parts}")
        elif status == "duplicate":
            skip += 1
        else:
            fail += 1
            print(f"  FAIL {first_word}: {status}")

    print()
    print(f"added {ok}, skipped {skip} (duplicates), failed {fail}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
