"""gen_curriculum_big.py -- background teacher run: grow a LARGER
conversational curriculum (Phi method, round 2). Seeds: the 10 anchor
facts x 6 styles + canon paragraphs rewritten conversationally.
Appends to synthetic_curriculum_big.json as it goes (resumable).
"""
import io
import json
import os
import re
import sys

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.join(HERE, "..", "extraction")
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, EXT)
from demo_facts_head import ANCHORS                        # noqa: E402

OUT = os.path.join(HERE, "synthetic_curriculum_big.json")

STYLES = [
 "Write 10 short casual questions a curious person might ask about this, "
 "each on its own line, everyday wording, no numbering:",
 "Write a friendly conversational explanation (6 plain sentences, like "
 "chatting with a friend over coffee) of this:",
 "Write 8 one-line informal ways someone might refer to or ask about "
 "this in conversation, one per line:",
 "Write a short dialogue (6 turns) between two friends where one "
 "explains this to the other in plain words:",
 "Explain this to a curious teenager in 5 simple sentences:",
 "Write 6 everyday analogies or comparisons someone might use to "
 "describe this, one per line:",
]


def ask(prompt):
    try:
        r = requests.post("http://localhost:11434/api/generate",
                          json={"model": "llama3.2", "prompt": prompt,
                                "stream": False}, timeout=180)
        return r.json().get("response", "")
    except Exception:
        return ""


def main():
    done = {}
    if os.path.exists(OUT):
        done = json.load(io.open(OUT, encoding="utf-8"))

    # part 1: anchors x styles
    for topic, anchors in ANCHORS.items():
        for si, style in enumerate(STYLES):
            key = f"{topic}|s{si}"
            if key in done:
                continue
            resp = ask(f"{style}\n\nFACT: {anchors[0]}")
            done[key] = [ln.strip(" -*•") for ln in resp.splitlines()
                         if len(ln.strip()) > 15]
            json.dump(done, io.open(OUT, "w", encoding="utf-8"), indent=0)
            print(f"{key}: {len(done[key])}", flush=True)

    # part 2: canon paragraphs -> conversational rewrites
    canon = io.open(os.path.join(ROOT, "FORMULAS_AND_TABLES.md"),
                    encoding="utf-8", errors="ignore").read()
    paras = [p.strip() for p in re.split(r"\n\s*\n", canon)
             if 200 < len(p.strip()) < 900][:60]
    for pi, para in enumerate(paras):
        key = f"canon|p{pi}"
        if key in done:
            continue
        resp = ask("Rewrite this technical note as a casual conversational "
                   "explanation between friends, 4-6 plain sentences, no "
                   "symbols:\n\n" + para)
        done[key] = [ln.strip() for ln in resp.splitlines()
                     if len(ln.strip()) > 15]
        json.dump(done, io.open(OUT, "w", encoding="utf-8"), indent=0)
        print(f"{key}: {len(done[key])}", flush=True)

    total = sum(len(v) for v in done.values())
    print(f"DONE: {total} conversational texts in {OUT}")


if __name__ == "__main__":
    main()
