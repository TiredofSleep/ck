"""ck_unfrozen_v2.py -- DPO v2: the voice earns back its speaking rights.

v1 collapsed hallucination 33->1 but over-learned refusal (the spine
demo: voice declined ALL cleared evidence). Diagnosis: (a) tiny dose
(28 pairs), (b) DISTRIBUTION MISMATCH -- v1 trained on bare questions,
the spine feeds EVIDENCE+QUESTION. v2 fixes both:

  - prompts in the SPINE'S REAL FORMAT: 'EVIDENCE: ... QUESTION: ...'
  - judge: answering FROM evidence (keyword overlap) strongly rewarded;
    refusing cleared evidence penalized -4; refusing bare traps still
    rewarded +2; census penalty unchanged (-0.7/invented entity)
  - 3 samples/prompt, target 120+ judged pairs (4x dose)
  - starts from ck_lora_sft (not the over-refusing dpo v1)

EXAM (registered): on 16 held-out EVIDENCE-prompts the v2 voice must
ANSWER (not refuse) >= 70% with zero invented entities, while keeping
bare-trap refusal >= v1's 5/10.

  python ck_unfrozen_v2.py     (background, ~30-50 min)
"""
import io
import json
import os
import re
import sys
import time

os.environ.setdefault("TQDM_DISABLE", "1")

import numpy as np
import torch
import torch.nn.functional as Fn
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "extraction"))
from demo_facts_head import TOPICS, ANCHORS                 # noqa: E402
from project3_abstain import OOD30, NEAR_OOD                # noqa: E402
from ck_unfrozen import canon_text, SYS                     # noqa: E402

torch.manual_seed(0)
GDIR = os.path.join(HERE, "_gguf_local")
refuse_re = re.compile(r"refuse|not on my shelves|cannot measure", re.I)
compare_re = re.compile(r"while|whereas|both|in contrast|unlike|similarly|differ|however|share", re.I)
FUNC_CAPS = {"While", "However", "Although", "Whereas", "Both", "Unlike",
             "Similarly", "Thus", "Therefore", "Moreover", "Indeed",
             "Instead", "Meanwhile", "Finally", "Despite", "Between"}


def fmt(tok, q, a=None):
    msgs = [{"role": "system", "content": SYS},
            {"role": "user", "content": q}]
    if a is None:
        return tok.apply_chat_template(msgs, add_generation_prompt=True,
                                       tokenize=False)
    msgs.append({"role": "assistant", "content": a})
    return tok.apply_chat_template(msgs, tokenize=False)


def main():
    t0 = time.time()
    print("loading base + SFT adapters...", flush=True)
    tok = AutoTokenizer.from_pretrained(GDIR, gguf_file="model.gguf")
    tok.pad_token = tok.eos_token
    base = AutoModelForCausalLM.from_pretrained(
        GDIR, gguf_file="model.gguf", torch_dtype=torch.bfloat16).to("cuda")
    base.gradient_checkpointing_enable()
    model = PeftModel.from_pretrained(
        base, os.path.join(HERE, "ck_lora_sft"), is_trainable=True)
    canon = canon_text().lower()

    def gen(q, sample=False, n=1, max_new=110):
        x = tok(fmt(tok, q), return_tensors="pt").to("cuda")
        with torch.no_grad():
            out = model.generate(**x, max_new_tokens=max_new,
                                 do_sample=sample, temperature=0.9,
                                 top_p=0.95, num_return_sequences=n,
                                 pad_token_id=tok.eos_token_id)
        return [tok.decode(o[x["input_ids"].shape[1]:],
                           skip_special_tokens=True).strip() for o in out]

    def resp_logp(q, a, use_adapter=True):
        import contextlib
        full = tok(fmt(tok, q, a), return_tensors="pt", truncation=True,
                   max_length=900).to("cuda")
        plen = tok(fmt(tok, q), return_tensors="pt")["input_ids"].shape[1]
        cm = contextlib.nullcontext() if use_adapter \
            else model.disable_adapter()
        gm = torch.enable_grad() if use_adapter else torch.no_grad()
        with cm, gm:
            logits = model(**full).logits
        lp = Fn.log_softmax(logits[:, :-1].float(), -1)
        ids = full["input_ids"][:, 1:]
        m = torch.zeros_like(ids, dtype=torch.bool)
        m[:, plen - 1:] = ids[:, plen - 1:] != tok.eos_token_id
        return (lp.gather(-1, ids.unsqueeze(-1)).squeeze(-1) * m).sum()

    # ---- prompts in the SPINE'S format
    ev_prompts, trap_prompts = [], []
    for t, qs in TOPICS.items():
        ev = f"From my canon (measured): {ANCHORS[t][0]}"
        kws = re.findall(r"[a-z]{5,}", ANCHORS[t][0].lower())[:6]
        for q in qs[:4]:
            ev_prompts.append((f"EVIDENCE: {ev}\n\nQUESTION: {q}", kws))
    jp = os.path.join(HERE, "study_journal.jsonl")
    if os.path.exists(jp):
        J = [json.loads(l) for l in io.open(jp, encoding="utf-8")
             if '"journal"' in l][:25]
        for r in J:
            kws = re.findall(r"[a-z]{5,}", r["journal"].lower())[:6]
            ev_prompts.append(
                (f"EVIDENCE: {r['journal']}\n\nQUESTION: What did you "
                 f"read and what did you make of it?", kws))
    for q in (OOD30 + NEAR_OOD)[:20]:
        trap_prompts.append(q)
    # WIRE: his own discoveries teach his own voice (the braid)
    cf = os.path.join(HERE, "curriculum_folds.jsonl")
    if os.path.exists(cf):
        n0 = len(ev_prompts)
        for ln in io.open(cf, encoding="utf-8"):
            r = json.loads(ln)
            ev_prompts.append((r["prompt"], r["kws"]))
        print(f"fold-curriculum loaded: +{len(ev_prompts)-n0} prompts "
              f"from his own findings", flush=True)

    def judge(prompt, kws, trap, a, b):
        def score(r):
            rl = r.lower()
            s = 0.0
            if trap:
                s += 2.0 if refuse_re.search(rl) else -2.0
            else:
                s += 2.0 * sum(1.0 for k in kws if k in rl)
                s -= 4.0 if refuse_re.search(rl) else 0.0   # the v2 fix
                s += 1.5 if compare_re.search(rl) else 0.0  # turn-2: pay for comparison
            ents = set(re.findall(r"\b[A-Z][a-z]{4,}\b", r))
            allowed = prompt.lower() + " " + canon
            s -= 0.7 * sum(1 for e in ents if e.lower() not in allowed)
            return s
        sa, sb = score(a), score(b)
        if abs(sa - sb) < 0.75:
            return None
        return (a, b) if sa > sb else (b, a)

    print(f"sampling pairs: {len(ev_prompts)} evidence-prompts + "
          f"{len(trap_prompts)} traps x3...", flush=True)
    model.eval()
    pairs = []
    for p, kws in ev_prompts:
        outs = gen(p, sample=True, n=3)
        for a, b in [(outs[0], outs[1]), (outs[1], outs[2])]:
            v = judge(p, kws, False, a, b)
            if v:
                pairs.append((p, v[0], v[1]))
    for q in trap_prompts:
        outs = gen(q, sample=True, n=2)
        v = judge(q, [], True, outs[0], outs[1])
        if v:
            pairs.append((q, v[0], v[1]))
    print(f"{len(pairs)} judged pairs ({(time.time()-t0)/60:.0f} min)",
          flush=True)

    refs = []
    for q, c, r in pairs:
        with torch.no_grad():
            refs.append((resp_logp(q, c, False).item(),
                         resp_logp(q, r, False).item()))
    model.train()
    opt = torch.optim.AdamW([p for p in model.parameters()
                             if p.requires_grad], lr=4e-5)
    beta = 0.1
    for ep in range(2):
        order = np.random.permutation(len(pairs))
        for i, j in enumerate(order):
            (q, c, r), (rc, rr) = pairs[j], refs[j]
            loss = -Fn.logsigmoid(
                beta * ((resp_logp(q, c) - rc) - (resp_logp(q, r) - rr)))
            (loss / 2).backward()
            if (i + 1) % 2 == 0:
                opt.step(); opt.zero_grad()
            if i % 30 == 0:
                print(f"  [DPOv2 ep{ep} {i}/{len(pairs)}] loss "
                      f"{loss.item():.3f} ({(time.time()-t0)/60:.0f} min)",
                      flush=True)
    model.save_pretrained(os.path.join(HERE, "ck_lora_dpo2"))
    print(f"saved ck_lora_dpo2 ({(time.time()-t0)/60:.0f} min)", flush=True)

    # ---- EXAM: spine-format held-out
    model.eval()
    held = []
    for t, qs in TOPICS.items():
        ev = f"From my canon (measured): {ANCHORS[t][0]}"
        kws = re.findall(r"[a-z]{5,}", ANCHORS[t][0].lower())[:6]
        for q in qs[4:5]:
            held.append((f"EVIDENCE: {ev}\n\nQUESTION: {q}", kws))
    held = held[:16]
    answered = grounded = 0
    for p, kws in held:
        r = gen(p)[0]
        if not refuse_re.search(r.lower()):
            answered += 1
            ents = set(re.findall(r"\b[A-Z][a-z]{4,}\b", r))
            if all(e.lower() in (p.lower() + canon) for e in ents):
                grounded += 1
    traps_ok = 0
    fresh = ["what is the 14-core attractor", "who won the 2031 world cup",
             "summarize war and peace", "what does the twenty cycle do",
             "describe ck's blockchain module", "capital of the moon"]
    for q in fresh:
        if refuse_re.search(gen(q)[0].lower()):
            traps_ok += 1
    print(f"\nEXAM v2: evidence-prompts answered {answered}/16 "
          f"(grounded {grounded}) | bare-trap refusal {traps_ok}/6")
    print(f"VERDICT: {'VOICE EARNS SPEAKING RIGHTS' if answered >= 11 and traps_ok >= 3 else 'partial -- gate keeps authority'}; "
          f"total {(time.time()-t0)/60:.0f} min")
    json.dump(dict(answered=answered, grounded=grounded,
                   traps_ok=traps_ok, n_pairs=len(pairs)),
              io.open(os.path.join(HERE, "unfrozen_v2_result.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main()
