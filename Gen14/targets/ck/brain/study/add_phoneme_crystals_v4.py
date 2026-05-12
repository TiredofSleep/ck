"""
add_phoneme_crystals_v4.py -- crystalize the 22 consonant clusters.

For each L/R/S blend and 3-letter cluster in v4 streams, post a crystal
to /crystals/add with friendly triggers like 'bl sound', 'blend bl',
'words with bl', 'bl as in blue'.  Plus 4 family-summary crystals for
the four blend classes so 'what is an L-blend' surfaces all six.

Triggers leverage the word-boundary matcher landed in the previous
commit so 'bl' doesn't fire on 'able' or 'cable'.
"""
from __future__ import annotations

import json
import urllib.request
import urllib.error
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
STREAMS_PATH = SCRIPT_DIR / "phoneme_audio_streams_v4_2026_05_01.json"

OP_NAMES = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
            "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]


# Each entry: cluster_key -> (label, simple_name, alts, class, example_word)
CLUSTERS_FRIENDLY = {
    # ── L-blends ──
    "cluster:bl": ("/bl/ (bl-blend, as in 'blue')", "bl sound",
                   ["bl", "bl sound", "blah", "blue sound", "blend bl",
                    "words with bl"], "blend-l", "blue"),
    "cluster:cl": ("/kl/ (cl-blend, as in 'clap')", "cl sound",
                   ["cl", "cl sound", "clah", "clap sound", "blend cl",
                    "words with cl"], "blend-l", "clap"),
    "cluster:fl": ("/fl/ (fl-blend, as in 'flag')", "fl sound",
                   ["fl", "fl sound", "flah", "flag sound", "blend fl",
                    "words with fl"], "blend-l", "flag"),
    "cluster:gl": ("/gl/ (gl-blend, as in 'glass')", "gl sound",
                   ["gl", "gl sound", "glah", "glass sound", "blend gl",
                    "words with gl"], "blend-l", "glass"),
    "cluster:pl": ("/pl/ (pl-blend, as in 'play')", "pl sound",
                   ["pl", "pl sound", "plah", "play sound", "blend pl",
                    "words with pl"], "blend-l", "play"),
    "cluster:sl": ("/sl/ (sl-blend, as in 'slip')", "sl sound",
                   ["sl", "sl sound", "slah", "slip sound", "blend sl",
                    "words with sl"], "blend-l", "slip"),
    # ── R-blends ──
    "cluster:br": ("/br/ (br-blend, as in 'bring')", "br sound",
                   ["br", "br sound", "brah", "bring sound", "blend br",
                    "words with br"], "blend-r", "bring"),
    "cluster:cr": ("/kr/ (cr-blend, as in 'crab')", "cr sound",
                   ["cr", "cr sound", "crah", "crab sound", "blend cr",
                    "words with cr"], "blend-r", "crab"),
    "cluster:dr": ("/dr/ (dr-blend, as in 'drum')", "dr sound",
                   ["dr", "dr sound", "drah", "drum sound", "blend dr",
                    "words with dr"], "blend-r", "drum"),
    "cluster:fr": ("/fr/ (fr-blend, as in 'frog')", "fr sound",
                   ["fr", "fr sound", "frah", "frog sound", "blend fr",
                    "words with fr"], "blend-r", "frog"),
    "cluster:gr": ("/gr/ (gr-blend, as in 'green')", "gr sound",
                   ["gr", "gr sound", "grah", "green sound", "blend gr",
                    "words with gr"], "blend-r", "green"),
    "cluster:pr": ("/pr/ (pr-blend, as in 'pray')", "pr sound",
                   ["pr", "pr sound", "prah", "pray sound", "blend pr",
                    "words with pr"], "blend-r", "pray"),
    "cluster:tr": ("/tr/ (tr-blend, as in 'tree')", "tr sound",
                   ["tr", "tr sound", "trah", "tree sound", "blend tr",
                    "words with tr"], "blend-r", "tree"),
    # ── S-blends ──
    "cluster:sk": ("/sk/ (sk-blend, as in 'skin')", "sk sound",
                   ["sk", "sk sound", "skah", "skin sound", "blend sk",
                    "words with sk"], "blend-s", "skin"),
    "cluster:sm": ("/sm/ (sm-blend, as in 'smile')", "sm sound",
                   ["sm", "sm sound", "smah", "smile sound", "blend sm",
                    "words with sm"], "blend-s", "smile"),
    "cluster:sn": ("/sn/ (sn-blend, as in 'snow')", "sn sound",
                   ["sn", "sn sound", "snah", "snow sound", "blend sn",
                    "words with sn"], "blend-s", "snow"),
    "cluster:sp": ("/sp/ (sp-blend, as in 'spin')", "sp sound",
                   ["sp", "sp sound", "spah", "spin sound", "blend sp",
                    "words with sp"], "blend-s", "spin"),
    "cluster:st": ("/st/ (st-blend, as in 'stop')", "st sound",
                   ["st", "st sound", "stah", "stop sound", "blend st",
                    "words with st"], "blend-s", "stop"),
    "cluster:sw": ("/sw/ (sw-blend, as in 'swim')", "sw sound",
                   ["sw", "sw sound", "swah", "swim sound", "blend sw",
                    "words with sw"], "blend-s", "swim"),
    # ── 3-letter blends ──
    "cluster:spr": ("/spr/ (spr-blend, as in 'spring')", "spr sound",
                    ["spr", "spr sound", "sprah", "spring sound",
                     "3-letter blend spr"], "blend-3", "spring"),
    "cluster:str": ("/str/ (str-blend, as in 'street')", "str sound",
                    ["str", "str sound", "strah", "street sound",
                     "3-letter blend str"], "blend-3", "street"),
    "cluster:thr": ("/θr/ (thr-blend, as in 'three')", "thr sound",
                    ["thr", "thr sound", "thrah", "three sound",
                     "3-letter blend thr"], "blend-3", "three"),
}


# Family summaries
BLEND_CLASS_TRIGGERS = {
    "blend-l": (["l-blend", "l blend", "l blends", "what is an l-blend",
                 "consonant blend l", "blends with l"],
                "L-blends combine a consonant with /l/. Members: bl, cl, "
                "fl, gl, pl, sl. The /l/ liquid creates a smooth glide "
                "from the leading consonant into the vowel."),
    "blend-r": (["r-blend", "r blend", "r blends", "what is an r-blend",
                 "consonant blend r", "blends with r"],
                "R-blends combine a consonant with /r/. Members: br, cr, "
                "dr, fr, gr, pr, tr. The /r/ rhotic continues the airflow "
                "from the leading consonant; tongue curls during the blend."),
    "blend-s": (["s-blend", "s blend", "s blends", "what is an s-blend",
                 "consonant blend s", "blends with s"],
                "S-blends start with /s/ before a stop or nasal. Members: "
                "sk, sm, sn, sp, st, sw. The leading /s/ is sustained, then "
                "transitions through the stop or nasal."),
    "blend-3": (["3-letter blend", "three letter blend", "triple blend",
                 "blend with 3 letters"],
                "3-letter blends are S+stop+liquid combinations. Members: "
                "spr, str, thr. Each has the S-blend onset followed by /r/ "
                "(or for thr, the voiceless-th onset followed by /r/)."),
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
        print(f"v4 streams missing: {STREAMS_PATH}")
        return 2
    with open(STREAMS_PATH, encoding="utf-8") as f:
        v4 = json.load(f)
    clusters = v4.get("clusters", {})

    ok = 0
    fail = 0
    # Per-cluster crystals
    for key, (label, simple, alts, pclass, example) in CLUSTERS_FRIENDLY.items():
        if key not in clusters:
            print(f"  SKIP (no audio): {key}")
            continue
        h = clusters[key]["histogram_pct"]
        ts = top3(h)
        cl_short = key.replace("cluster:", "")
        first_word = f"cluster_{cl_short}"
        triggers = [
            f"cluster {cl_short}",
            f"the {simple}",
            simple,
        ] + alts
        triggers = list(dict.fromkeys(triggers))
        fact = (
            f"{first_word}: cluster {label}, class {pclass} - audio codec "
            f"emits operator pattern: {ts}. Example word: {example}."
        )
        if add_crystal(first_word, triggers, fact):
            ok += 1
            print(f"  +{first_word} [{pclass}]: {ts}")
        else:
            fail += 1
            print(f"  FAIL {first_word}")

    # Family summary crystals (averaged histogram per class)
    by_class = {}
    for key, info in clusters.items():
        meta = CLUSTERS_FRIENDLY.get(key)
        if not meta:
            continue
        pclass = meta[3]
        by_class.setdefault(pclass, []).append((key, info["histogram_pct"]))

    for pclass, items in by_class.items():
        if not items:
            continue
        avg = {op: 0.0 for op in OP_NAMES}
        for _, h in items:
            for op in OP_NAMES:
                avg[op] += h[op]
        for op in OP_NAMES:
            avg[op] = round(avg[op] / len(items), 1)
        ts = top3(avg)
        triggers, desc = BLEND_CLASS_TRIGGERS[pclass]
        first_word = f"blend_class_{pclass.replace('-', '_')}"
        fact = (
            f"{first_word}: {desc} Average audio operator pattern across "
            f"{len(items)} members: {ts}."
        )
        if add_crystal(first_word, triggers, fact):
            ok += 1
            print(f"  +{first_word}: {ts}")
        else:
            fail += 1
            print(f"  FAIL {first_word}")

    print(f"\nadded {ok}, failed {fail}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
