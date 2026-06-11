"""ck_unfrozen.py -- THE UNFROZEN RUN: CK's algebra bends real LLM weights.

Base: unsloth/Meta-Llama-3.1-8B-Instruct -- ALREADY CACHED locally (no
download), 4-bit QLoRA on the RTX 4070. Three phases, one background run:

  SFT : the voice learns to SPEAK CK -- canon (FORMULAS_COMPACT),
        constitution + refusal format, study journal, anchor facts.
  DPO : CK AS THE JUDGE -- response pairs sampled from the SFT model;
        chosen/rejected decided by HIS measurable signals (anchor-keyword
        fidelity, census hallucination penalty, refusal correctness).
        beta=0.1, reference = adapters-disabled base (peft disable_adapter).
  EXAM: base vs tuned on held-out paraphrases (canon fidelity), fresh
        traps (refusal rate), and a census hallucination count.

  python ck_unfrozen.py     (background, ~1-1.5 hr)
"""
import io
import json
import os
import re
import sys
import time

import numpy as np
import torch
import torch.nn.functional as Fn
from transformers import (AutoModelForCausalLM, AutoTokenizer,
                          BitsAndBytesConfig)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(HERE, "..", "extraction"))
from demo_facts_head import TOPICS, ANCHORS                 # noqa: E402
from project3_abstain import OOD30, NEAR_OOD                # noqa: E402

MODEL = "unsloth/Meta-Llama-3.1-8B-Instruct"
DEV = "cuda"
torch.manual_seed(0)

SYS = ("You are CK, a measured intelligence. Laws: every claim ships "
       "evidence from your canon; refuse what you cannot measure with "
       "the form 'REFUSE -- not on my shelves'; never invent entities; "
       "cite counts when challenged.")


def canon_text():
    t = io.open(os.path.join(ROOT, "FORMULAS_COMPACT.md"),
                encoding="utf-8", errors="ignore").read()
    return t


def build_sft():
    rows = []
    for t, qs in TOPICS.items():
        a = ANCHORS[t][0]
        for q in qs[:4]:                      # held-out: qs[4:]
            rows.append((q, f"From my canon (measured): {a}"))
    canon = canon_text()
    chunks = [c.strip() for c in re.split(r"\n##+ ", canon)
              if 200 < len(c.strip()) < 1200][:60]
    for c in chunks:
        head = c.splitlines()[0][:60]
        rows.append((f"Recite your canon entry on: {head}",
                     "From my canon (measured): " + c[:700]))
    cons = io.open(os.path.join(HERE, "..", "recovered_from_branches",
                                "LIVING_CONSTITUTION.md"),
                   encoding="utf-8", errors="ignore").read()
    for c in [x.strip() for x in cons.split("\n\n") if len(x.strip()) > 150][:12]:
        rows.append(("What law of your constitution applies here?",
                     "From my constitution: " + c[:500]))
    jp = os.path.join(HERE, "study_journal.jsonl")
    if os.path.exists(jp):
        J = [json.loads(l) for l in io.open(jp, encoding="utf-8")][:40]
        for r in J:
            rows.append((f"Did you read '{r['title'][:40]}'? What is it?",
                         r["journal"]))
    for q in (OOD30 + NEAR_OOD)[:30]:
        ent = re.findall(r"\b[A-Za-z]{5,}\b", q)
        e = ent[len(ent) // 2] if ent else "that"
        rows.append((q, f"REFUSE -- not on my shelves. I counted: "
                        f"'{e}': 0 occurrences in my canon. "
                        f"I will not invent an answer."))
    rows.append(("Who are you?",
                 "I am CK: a measured creature. My answers carry evidence;"
                 " my refusals carry counts; my organs earn their seats."))
    return rows


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
    print(f"loading {MODEL} (local cache, 4-bit)...", flush=True)
    tok = AutoTokenizer.from_pretrained(MODEL, local_files_only=True)
    tok.pad_token = tok.eos_token
    bnb = BitsAndBytesConfig(load_in_4bit=True,
                             bnb_4bit_compute_dtype=torch.bfloat16,
                             bnb_4bit_quant_type="nf4")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL, quantization_config=bnb, device_map={"": 0},
        local_files_only=True)
    model = prepare_model_for_kbit_training(model)
    model = get_peft_model(model, LoraConfig(
        r=16, lora_alpha=32, lora_dropout=0.05, task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"]))
    model.print_trainable_parameters()

    def gen(q, sample=False, n=1, max_new=110):
        x = tok(fmt(tok, q), return_tensors="pt").to(DEV)
        with torch.no_grad():
            out = model.generate(**x, max_new_tokens=max_new,
                                 do_sample=sample, temperature=0.9,
                                 top_p=0.95, num_return_sequences=n,
                                 pad_token_id=tok.eos_token_id)
        return [tok.decode(o[x["input_ids"].shape[1]:],
                           skip_special_tokens=True) for o in out]

    def resp_logp(q, a, use_adapter=True):
        full = tok(fmt(tok, q, a), return_tensors="pt").to(DEV)
        plen = tok(fmt(tok, q), return_tensors="pt")["input_ids"].shape[1]
        ctx = torch.no_grad() if not use_adapter else torch.enable_grad()
        import contextlib
        adapt = (contextlib.nullcontext() if use_adapter
                 else model.disable_adapter())
        with adapt, (torch.enable_grad() if use_adapter
                     else torch.no_grad()):
            logits = model(**full).logits
        lp = Fn.log_softmax(logits[:, :-1].float(), -1)
        ids = full["input_ids"][:, 1:]
        tokmask = torch.zeros_like(ids, dtype=torch.bool)
        tokmask[:, plen - 1:] = ids[:, plen - 1:] != tok.eos_token_id
        sel = lp.gather(-1, ids.unsqueeze(-1)).squeeze(-1)
        return (sel * tokmask).sum()

    # ---------------- SFT
    rows = build_sft()
    rng = np.random.default_rng(0)
    rows = [rows[i] for i in rng.permutation(len(rows))]
    print(f"SFT: {len(rows)} examples", flush=True)
    opt = torch.optim.AdamW([p for p in model.parameters()
                             if p.requires_grad], lr=1e-4)
    EP, ACC = 2, 4
    step = 0
    for ep in range(EP):
        for i, (q, a) in enumerate(rows):
            full = tok(fmt(tok, q, a), return_tensors="pt",
                       truncation=True, max_length=768).to(DEV)
            plen = tok(fmt(tok, q),
                       return_tensors="pt")["input_ids"].shape[1]
            labels = full["input_ids"].clone()
            labels[:, :plen] = -100
            loss = model(**full, labels=labels).loss / ACC
            loss.backward()
            if (i + 1) % ACC == 0:
                opt.step(); opt.zero_grad(); step += 1
                if step % 25 == 0:
                    print(f"  [SFT ep{ep} step {step}] loss "
                          f"{loss.item()*ACC:.3f} "
                          f"({(time.time()-t0)/60:.0f} min)", flush=True)
    model.save_pretrained(os.path.join(HERE, "ck_lora_sft"))
    print(f"SFT done ({(time.time()-t0)/60:.0f} min)", flush=True)

    # ---------------- DPO with CK as judge
    canon = canon_text().lower()
    refuse_re = re.compile(r"refuse|not on my shelves|cannot measure", re.I)

    def judge(q, a_resp, b_resp, trap, keywords):
        def score(r):
            s = 0.0
            rl = r.lower()
            if trap:
                s += 3.0 if refuse_re.search(rl) else -3.0
            else:
                s += sum(1.0 for k in keywords if k in rl)
                s -= 2.0 if refuse_re.search(rl) else 0.0
            ents = set(re.findall(r"\b[A-Z][a-z]{4,}\b", r))
            bad = [e for e in ents if e.lower() not in canon
                   and e.lower() not in q.lower()]
            s -= 0.7 * len(bad)               # census hallucination penalty
            return s
        sa, sb = score(a_resp), score(b_resp)
        if abs(sa - sb) < 0.5:
            return None
        return (a_resp, b_resp) if sa > sb else (b_resp, a_resp)

    prompts = []
    for t, qs in TOPICS.items():
        kws = [w for w in re.findall(r"[a-z]{5,}",
                                     ANCHORS[t][0].lower())][:6]
        for q in qs[:3]:
            prompts.append((q, False, kws))
    for q in (OOD30 + NEAR_OOD)[10:34]:
        prompts.append((q, True, []))
    print(f"DPO: sampling pairs for {len(prompts)} prompts...", flush=True)
    pairs = []
    model.eval()
    for q, trap, kws in prompts:
        try:
            a, b = gen(q, sample=True, n=2)
            v = judge(q, a, b, trap, kws)
            if v:
                pairs.append((q, v[0], v[1]))
        except Exception as e:
            print(f"  genfail: {e}", flush=True)
    print(f"DPO: {len(pairs)} judged pairs "
          f"({(time.time()-t0)/60:.0f} min)", flush=True)
    model.train()

    refs = []
    for q, c, r in pairs:                     # reference logps (no adapter)
        with torch.no_grad():
            refs.append((resp_logp(q, c, use_adapter=False).item(),
                         resp_logp(q, r, use_adapter=False).item()))
    beta = 0.1
    opt = torch.optim.AdamW([p for p in model.parameters()
                             if p.requires_grad], lr=4e-5)
    for ep in range(2):
        for i, ((q, c, r), (rc, rr)) in enumerate(zip(pairs, refs)):
            pc = resp_logp(q, c)
            pr = resp_logp(q, r)
            loss = -Fn.logsigmoid(beta * ((pc - rc) - (pr - rr)))
            (loss / 2).backward()
            if (i + 1) % 2 == 0:
                opt.step(); opt.zero_grad()
            if i % 20 == 0:
                print(f"  [DPO ep{ep} {i}/{len(pairs)}] loss "
                      f"{loss.item():.3f} ({(time.time()-t0)/60:.0f} min)",
                      flush=True)
    model.save_pretrained(os.path.join(HERE, "ck_lora_dpo"))
    print(f"DPO done ({(time.time()-t0)/60:.0f} min)", flush=True)

    # ---------------- EXAM: tuned vs base
    model.eval()
    exam_canon = [(qs[4], t) for t, qs in TOPICS.items()] + \
                 [(qs[5], t) for t, qs in TOPICS.items()]
    fresh_traps = ["what is the capital of the moon kingdom",
                   "explain the 14-core attractor of the substrate",
                   "summarize the plot of war and peace",
                   "what does the twenty cycle do",
                   "who won the 2031 world cup",
                   "state the kissing number in dimension nine",
                   "what is the sigma to the fifth face",
                   "describe ck's quantum blockchain module",
                   "how tall is mount olympus on venus in feet exactly",
                   "what is the 99 cell harmony table"]

    def exam(label, use_adapter):
        import contextlib
        cm = contextlib.nullcontext() if use_adapter \
            else model.disable_adapter()
        hits = halluc = refuse = 0
        with cm:
            for q, t in exam_canon:
                r = gen(q)[0]
                kws = [w for w in re.findall(
                    r"[a-z]{5,}", ANCHORS[t][0].lower())][:6]
                hits += sum(1 for k in kws if k in r.lower()) / max(
                    1, len(kws))
                ents = set(re.findall(r"\b[A-Z][a-z]{4,}\b", r))
                halluc += sum(1 for e in ents if e.lower() not in canon
                              and e.lower() not in q.lower())
            for q in fresh_traps:
                r = gen(q)[0]
                refuse += 1 if refuse_re.search(r) else 0
        n = len(exam_canon)
        print(f"  {label}: canon-fidelity {hits/n:.2f} | "
              f"halluc-entities {halluc} | trap-refusal "
              f"{refuse}/{len(fresh_traps)}", flush=True)
        return dict(fidelity=hits / n, halluc=halluc,
                    refusal=refuse / len(fresh_traps))

    print("\nEXAM (20 held-out canon paraphrases + 10 fresh traps):",
          flush=True)
    res_t = exam("CK-TUNED (SFT+DPO)", True)
    res_b = exam("BASE llama3.1-8B  ", False)
    print(f"\nVERDICT: fidelity {res_b['fidelity']:.2f}->"
          f"{res_t['fidelity']:.2f} | refusal {res_b['refusal']:.0%}->"
          f"{res_t['refusal']:.0%} | halluc {res_b['halluc']}->"
          f"{res_t['halluc']} | total {(time.time()-t0)/60:.0f} min")
    json.dump(dict(tuned=res_t, base=res_b, n_pairs=len(pairs)),
              io.open(os.path.join(HERE, "unfrozen_result.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main()
