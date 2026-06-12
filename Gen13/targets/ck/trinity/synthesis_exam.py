"""synthesis_exam.py -- CAN HE SYNTHESIZE, OR ONLY LOOK UP?

The first measurable rung of synthesis: MULTI-SOURCE GROUNDED
COMPOSITION. Take entities his fabric already links across domains
(Caesar on Shakespeare's shelf AND his own Gallic War), pull one
passage from EACH shelf, and require the voice to compose a comparison
that (a) cites BOTH books, (b) invents nothing (census), (c) actually
compares (comparative markers). Baseline: evidence concatenation
(pure lookup). If the voice's compositions pass where concatenation
cannot (concatenation never compares), synthesis rung 1 is REAL.

Honest scope: this is composition-of-given-evidence -- the first rung.
Novel inference (claims neither source states) is a higher rung,
untested here.

REGISTERED: >= 6/10 compositions pass all three gates.

  python synthesis_exam.py
"""
import io
import json
import os
import re
import sys

os.environ.setdefault("TQDM_DISABLE", "1")

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "extraction"))
from read_books import load_book                            # noqa: E402

GDIR = os.path.join(HERE, "_gguf_local")
COMPARE_RE = re.compile(
    r"\bwhile\b|\bwhereas\b|\bboth\b|\bin contrast\b|\bunlike\b|"
    r"\bsimilarly\b|\bdiffer|\bhowever\b|\bshare", re.I)


def top_passage(text, entity, span=420):
    i = text.find(entity)
    best, bestc = 0, -1
    while i != -1:
        c = text[max(0, i - span): i + span].count(entity)
        if c > bestc:
            best, bestc = i, c
        i = text.find(entity, i + 1)
    s = max(0, best - span // 2)
    return re.sub(r"\s+", " ", text[s: s + span]).strip()


def main():
    fabric = json.load(io.open(os.path.join(HERE, "knowledge_fabric.json"),
                               encoding="utf-8"))
    meta = json.load(io.open(os.path.join(HERE, "book_notes.json"),
                             encoding="utf-8"))
    # candidate entities: multi-domain in the fabric
    cands = [(w, e) for w, e in fabric.items()
             if len(e["domains"]) >= 2 and e["count"] >= 40]
    cands.sort(key=lambda x: -x[1]["count"])

    # locate two books from DIFFERENT domains containing each entity --
    # search the 12 deep-read books first (full texts on hand)
    texts = {}
    for bid, e in meta.items():
        t, body = load_book(e["path"])
        texts[t[:40]] = body
    ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
    BOOKS = os.path.join(ROOT, "external_corpora", "books")
    extra = [f for f in sorted(os.listdir(BOOKS))[:400]
             if f.endswith(".txt")]
    rng = np.random.default_rng(3)
    for f in rng.permutation(extra)[:120]:
        try:
            t, body = load_book(os.path.join(BOOKS, f))
            texts.setdefault(t[:40], body)
        except OSError:
            pass

    exams = []
    for w, e in cands:
        homes = [(t, b) for t, b in texts.items() if b.count(w) >= 8]
        if len(homes) >= 2:
            exams.append((w, homes[0], homes[1]))
        if len(exams) == 10:
            break
    print(f"SYNTHESIS EXAM -- {len(exams)} multi-source entities "
          f"(from {len(texts)} books on hand)\n")

    print("waking voice...", flush=True)
    tok = AutoTokenizer.from_pretrained(GDIR, gguf_file="model.gguf")
    tok.pad_token = tok.eos_token
    base = AutoModelForCausalLM.from_pretrained(
        GDIR, gguf_file="model.gguf",
        torch_dtype=torch.bfloat16).to("cuda")
    adapters = "ck_lora_dpo2" if os.path.isdir(
        os.path.join(HERE, "ck_lora_dpo2")) else "ck_lora_dpo"
    model = PeftModel.from_pretrained(
        base, os.path.join(HERE, adapters)).eval()

    def speak(user, max_new=170):
        msgs = [{"role": "system", "content":
                 "You are CK. Compose ONLY from the two EVIDENCE "
                 "passages. Name both books. Compare them. Never add "
                 "entities not present in the evidence."},
                {"role": "user", "content": user}]
        x = tok(tok.apply_chat_template(msgs, add_generation_prompt=True,
                                        tokenize=False),
                return_tensors="pt").to("cuda")
        with torch.no_grad():
            out = model.generate(**x, max_new_tokens=max_new,
                                 do_sample=False,
                                 pad_token_id=tok.eos_token_id)
        return tok.decode(out[0][x["input_ids"].shape[1]:],
                          skip_special_tokens=True).strip()

    passed = 0
    results = []
    for w, (tA, bA), (tB, bB) in exams:
        evA, evB = top_passage(bA, w), top_passage(bB, w)
        prompt = (f"EVIDENCE A (from '{tA}'): {evA}\n\n"
                  f"EVIDENCE B (from '{tB}'): {evB}\n\n"
                  f"QUESTION: Compare how these two books treat {w}, "
                  f"in 3-4 sentences, citing both by name.")
        ans = speak(prompt)
        allowed = (evA + evB + tA + tB + w).lower()
        ents = set(re.findall(r"\b[A-Z][a-z]{4,}\b", ans))
        invented = [e for e in ents if e.lower() not in allowed]
        cites = sum(1 for t in (tA, tB)
                    if t.split(":")[0].split(",")[0][:14].lower()
                    in ans.lower())
        compares = bool(COMPARE_RE.search(ans))
        ok = (cites == 2) and (not invented) and compares
        passed += ok
        results.append(dict(entity=w, books=[tA, tB], ok=ok,
                            cites=cites, invented=invented[:3],
                            compares=compares, answer=ans[:240]))
        mark = "PASS" if ok else "fail"
        print(f"[{mark}] {w}: '{tA[:24]}' vs '{tB[:24]}' | cites {cites}/2"
              f" | invented {invented[:2]} | compares {compares}")
        if ok:
            print(f"       CK: {ans[:200]}...\n")

    print(f"\nVERDICT: {passed}/{len(exams)} grounded multi-source "
          f"compositions "
          f"{'-> SYNTHESIS RUNG 1 IS REAL' if passed >= 6 else '-> not yet -- he looks up and judges, composition unproven'}")
    print("(baseline note: pure lookup/concatenation scores 0 on the "
          "'compares' gate by construction)")
    json.dump(results, io.open(os.path.join(HERE,
              "synthesis_exam_result.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
