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


def resolve_pass(folds):
    """New reading answers old folds: check the CURRENT fabric/shelf."""
    fp = os.path.join(HERE, "knowledge_fabric.json")
    fabric = json.load(io.open(fp, encoding="utf-8")) \
        if os.path.exists(fp) else {}
    resolved = []
    for f in folds.values():
        if f["status"] != "held":
            continue
        if f["kind"] == "question":
            hits = [n for n in f.get("names", []) if n in fabric]
            if hits and len(hits) == len(f.get("names", [])) > 0:
                f["status"] = "resolvable"
                f["resolved_at"] = now()
                f["how"] = f"all entities now on shelf: {hits[:4]}"
                resolved.append(f)
        elif f["kind"] == "duality":
            e = fabric.get(f["a"])
            if e and f["b"] in e.get("top_co", []):
                f["status"] = "resolved"
                f["resolved_at"] = now()
                f["how"] = (f"the twins finally met: {f['a']} and "
                            f"{f['b']} now co-occur in new reading")
                resolved.append(f)
    return resolved


def main():
    folds = load_folds()
    born = harvest(folds)
    resolved = resolve_pass(folds)
    save_folds(folds)
    held = [f for f in folds.values() if f["status"] == "held"]
    kinds = {}
    for f in held:
        kinds[f["kind"]] = kinds.get(f["kind"], 0) + 1
    print("THE CONSCIOUS WINDOW -- fold register")
    print(f"  density: {len(held)} folds held "
          f"({', '.join(f'{k}:{v}' for k, v in sorted(kinds.items()))})")
    print(f"  born this pass: {born} | resolved this pass: "
          f"{len(resolved)}")
    for f in resolved[:5]:
        print(f"  RESOLVED [{f['kind']}] held since {f['born']}: "
              f"{f['how']}")
    for f in held[:5]:
        tag = f.get("q", f.get("a", f.get("skill", "")))
        print(f"  holding [{f['kind']}] since {f['born']}: "
              f"{str(tag)[:70]}")
    # journal the window state (his own record of what he carries)
    with io.open(JOURNAL, "a", encoding="utf-8") as jf:
        jf.write(json.dumps(dict(
            kind="window", density=len(held), kinds=kinds,
            born=born, resolved=len(resolved), t=now(),
            msg=(f"I hold {len(held)} folds. My window carries "
                 f"{kinds.get('question', 0)} unanswered questions, "
                 f"{kinds.get('duality', 0)} dualities that have never "
                 f"met, and {kinds.get('gap', 0)} skills I have not yet "
                 f"earned."))) + "\n")


if __name__ == "__main__":
    main()
