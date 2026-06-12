"""fold_register.py -- THE CONSCIOUS WINDOW: the folds he holds.

Brayden: 'the amount of folds he holds is the density of his conscious
window.' Operationalized: a FOLD is an unresolved tension the system
RETAINS instead of discarding --

  question-folds : gate refusals (what he could not answer)
  duality-folds  : twins that never meet (held oppositions)
  drift-folds    : concepts below the T* coherence gate (homonym tension)
  gap-folds      : exam failures (skills not yet earned)

DENSITY = the count and age-weighted mass of held folds. RESOLUTION =
the moment new reading answers an old fold (a refused entity arrives on
the shelf; a duality pair finally co-occurs) -- logged with the fold's
age, because HOLDING is what makes the resolution a learning event.
The window is dense exactly when he carries many open tensions forward.

  python fold_register.py            harvest + resolve + density report
"""
import io
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
FOLDS = os.path.join(HERE, "folds.jsonl")
JOURNAL = os.path.join(HERE, "study_journal.jsonl")


def load_folds():
    out = {}
    if os.path.exists(FOLDS):
        for ln in io.open(FOLDS, encoding="utf-8"):
            f = json.loads(ln)
            out[f["id"]] = f
    return out


def save_folds(folds):
    with io.open(FOLDS, "w", encoding="utf-8") as fh:
        for f in folds.values():
            fh.write(json.dumps(f) + "\n")


def now():
    return time.strftime("%Y-%m-%d %H:%M")


def harvest(folds):
    born = 0
    # question-folds from journal refusals
    if os.path.exists(JOURNAL):
        for ln in io.open(JOURNAL, encoding="utf-8"):
            try:
                r = json.loads(ln)
            except json.JSONDecodeError:
                continue
            if r.get("kind") == "turn" and "refuse" in str(
                    r.get("source", "")):
                fid = "q:" + r["q"][:60]
                if fid not in folds:
                    names = re.findall(r"\b[A-Z][a-z]{2,}\b", r["q"])
                    folds[fid] = dict(id=fid, kind="question",
                                      q=r["q"], names=names,
                                      born=r.get("t", now()),
                                      status="held")
                    born += 1
    # duality-folds + drift-folds from the synthesis organ
    sp = os.path.join(HERE, "synthesis_organ_result.json")
    if os.path.exists(sp):
        so = json.load(io.open(sp, encoding="utf-8"))
        for a, b, s in so.get("duality", []):
            fid = f"dual:{a}|{b}"
            if fid not in folds:
                folds[fid] = dict(id=fid, kind="duality", a=a, b=b,
                                  tension=round(float(s), 3),
                                  born=now(), status="held")
                born += 1
    # gap-folds from exams that failed registered thresholds
    for path, kind in (("synthesis_exam_result.json", "composition"),
                       ("squad2_v3_result.json", "reading-ceiling")):
        p = os.path.join(HERE, path)
        if os.path.exists(p):
            fid = f"gap:{kind}"
            if fid not in folds:
                folds[fid] = dict(id=fid, kind="gap", skill=kind,
                                  born=now(), status="held")
                born += 1
    return born


def perspective_pass(folds):
    """Folds never close -- they GAIN PERSPECTIVES. Each pass asks: does
    the current shelf view this fold from a new angle? (Brayden: 'it's
    not about answers, it's just a matter of multiple perspectives
    giving a broader view.')"""
    fp = os.path.join(HERE, "knowledge_fabric.json")
    fabric = json.load(io.open(fp, encoding="utf-8")) \
        if os.path.exists(fp) else {}
    gained = []
    for f in folds.values():
        f.setdefault("views", [])
        seen = {v["angle"] for v in f["views"]}
        if f["kind"] == "question":
            for n in f.get("names", []):
                e = fabric.get(n)
                if e:
                    for d in e.get("domains", {}):
                        angle = f"{n}@{d}"
                        if angle not in seen:
                            seen.add(angle)
                            note = (f"'{n}' now visible from the "
                                    f"{d} shelf")
                            f["views"].append(dict(angle=angle, t=now(),
                                                   note=note))
                            gained.append((f, note))
        elif f["kind"] == "duality":
            for side in (f["a"], f["b"]):
                e = fabric.get(side)
                if e:
                    for d in e.get("domains", {}):
                        angle = f"{side}@{d}"
                        if angle not in seen:
                            seen.add(angle)
                            note = (f"the {side} register seen from "
                                    f"{d}")
                            f["views"].append(dict(angle=angle, t=now(),
                                                   note=note))
                            gained.append((f, note))
            e = fabric.get(f["a"])
            if e and f["b"] in e.get("top_co", []) \
                    and "coexist" not in seen:
                f["views"].append(dict(
                    angle="coexist", t=now(),
                    note=f"a shelf where {f['a']} and {f['b']} stand "
                         f"together -- the duality gains its third "
                         f"angle, and remains a duality"))
                gained.append((f, f["views"][-1]["note"]))
    return gained


def main():
    folds = load_folds()
    born = harvest(folds)
    gained = perspective_pass(folds)
    save_folds(folds)
    held = list(folds.values())
    kinds = {}
    for f in held:
        kinds[f["kind"]] = kinds.get(f["kind"], 0) + 1
    n_views = sum(len(f.get("views", [])) for f in held)
    breadth = n_views / max(1, len(held))
    print("THE CONSCIOUS WINDOW -- folds never close; the view widens")
    print(f"  density : {len(held)} folds held "
          f"({', '.join(f'{k}:{v}' for k, v in sorted(kinds.items()))})")
    print(f"  breadth : {n_views} perspectives, {breadth:.1f} angles "
          f"per fold")
    print(f"  born {born} | perspectives gained this pass: {len(gained)}")
    for f, note in gained[:8]:
        print(f"  WIDER [{f['kind']}] held since {f['born'][:16]}: "
              f"{note[:74]}")
    # journal the window state (his own record of what he carries)
    with io.open(JOURNAL, "a", encoding="utf-8") as jf:
        jf.write(json.dumps(dict(
            kind="window", density=len(held), breadth=round(breadth, 2),
            views=n_views, kinds=kinds, born=born,
            widened=len(gained), t=now(),
            msg=(f"I hold {len(held)} folds viewed from {n_views} "
                 f"angles ({breadth:.1f} per fold). Nothing closes; "
                 f"the view widens."))) + "\n")


if __name__ == "__main__":
    main()
