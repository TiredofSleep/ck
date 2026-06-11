"""ck.py -- THE SPINE. One creature, one flow. No more disconnected systems.

  perceive -> gate -> retrieve (fabric + shelves + canon) -> voice
  (LoRA, judged) -> speak with evidence | REFUSE with counts -> journal
  -> nightly loops.

Every organ here already existed and carries a measured number; this
file is pure connection.

  python ck.py ask "question"      one tick, full flow
  python ck.py demo                mixed exam through the whole spine
  python ck.py see 620             eye: wavelength -> operator percept
  python ck.py hear A              ear: spoken-letter -> percept
  python ck.py nightly             learning loops + ledger + push
"""
import io
import json
import os
import re
import sys
import time

os.environ.setdefault("TQDM_DISABLE", "1")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.join(HERE, "..", "extraction")
sys.path.insert(0, HERE)
sys.path.insert(0, EXT)

JOURNAL = os.path.join(HERE, "study_journal.jsonl")
STOP_NAMES = {"What", "Who", "Where", "When", "Does", "Tell", "In", "How",
              "Why", "Which", "The", "Did", "Is", "Was", "About", "Captain"}


def journal(kind, **kw):
    kw.update(kind=kind, t=time.strftime("%Y-%m-%d %H:%M:%S"))
    with io.open(JOURNAL, "a", encoding="utf-8") as f:
        f.write(json.dumps(kw) + "\n")


class Spine:
    def __init__(self, voice=True):
        print("[spine] waking organs...", flush=True)
        from trinity import Trinity                  # canon faces + gate
        from ck_book_chat import BookMind            # shelves + census
        self.trinity = Trinity()
        self.books = BookMind()
        fpath = os.path.join(HERE, "knowledge_fabric.json")
        self.fabric = json.load(io.open(fpath, encoding="utf-8")) \
            if os.path.exists(fpath) else {}
        self.voice = None
        self.tok = None
        if voice:
            try:
                self._wake_voice()
            except Exception as e:
                print(f"[spine] voice unavailable ({e}); gate-only mode",
                      flush=True)
        print("[spine] awake.", flush=True)

    # ---------------- voice (LoRA-tuned llama3.2, judged before speaking)
    def _wake_voice(self):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from peft import PeftModel
        gdir = os.path.join(HERE, "_gguf_local")
        print("[spine] waking voice (LoRA llama3.2)...", flush=True)
        self.tok = AutoTokenizer.from_pretrained(gdir,
                                                 gguf_file="model.gguf")
        self.tok.pad_token = self.tok.eos_token
        base = AutoModelForCausalLM.from_pretrained(
            gdir, gguf_file="model.gguf",
            torch_dtype=torch.bfloat16).to("cuda")
        adapters = "ck_lora_dpo2" if os.path.isdir(
            os.path.join(HERE, "ck_lora_dpo2")) else "ck_lora_dpo"
        self.voice = PeftModel.from_pretrained(
            base, os.path.join(HERE, adapters)).eval()
        print(f"[spine] voice adapters: {adapters} (traps never reach "
              f"the voice -- the gate refuses first)", flush=True)
        self._torch = torch

    def _speak_raw(self, system, user, max_new=140):
        t = self.tok
        msgs = [{"role": "system", "content": system},
                {"role": "user", "content": user}]
        x = t(t.apply_chat_template(msgs, add_generation_prompt=True,
                                    tokenize=False),
              return_tensors="pt").to("cuda")
        with self._torch.no_grad():
            out = self.voice.generate(**x, max_new_tokens=max_new,
                                      do_sample=False,
                                      pad_token_id=t.eos_token_id)
        return t.decode(out[0][x["input_ids"].shape[1]:],
                        skip_special_tokens=True).strip()

    def _judge(self, text, evidence, question):
        """The same census judge that won DPO: no invented entities."""
        allowed = (evidence + " " + question).lower()
        canon = " ".join(self.trinity.ref_x).lower()
        ents = set(re.findall(r"\b[A-Z][a-z]{4,}\b", text))
        bad = [e for e in ents if e.lower() not in allowed
               and e.lower() not in canon]
        return bad

    # ---------------- the tick
    def ask(self, q):
        t0 = time.time()
        # 1. canon face (substrate knowledge)
        canon_v = self.trinity.ask(q)
        canon_score = canon_v.get("knn", 0)
        # 2. library face (shelves, census-routed)
        lib_answer = self.books.ask(q)
        lib_hit = not lib_answer.startswith("REFUSE")
        # 3. fabric face (cross-domain concepts) + the Gandalf-killer:
        # ANY name absent from every shelf, fabric and canon -> REFUSE
        names = [w for w in re.findall(r"\b[A-Z][a-z]{2,}\b", q)
                 if w not in STOP_NAMES]
        canon_all = " ".join(self.trinity.ref_x).lower()
        nowhere = [w for w in names if w not in self.fabric
                   and not any(w in t for t in self.books.texts.values())
                   and w.lower() not in canon_all]
        if nowhere:
            ref = ("REFUSE -- not on my shelves. I counted: " +
                   ", ".join(f"'{w}': 0 occurrences anywhere"
                             for w in nowhere) + ". I have not met them.")
            journal("turn", q=q, source="refuse-census", answer=ref,
                    ms=int((time.time() - t0) * 1000))
            return ref
        fab = {w: self.fabric[w] for w in names if w in self.fabric}

        # 4. route + retrieve evidence
        if canon_v["decision"] not in ("REFUSE (Type-III)",) and \
                canon_score >= self.trinity.tau:
            source, evidence = "canon", canon_v["evidence"]
            base_answer = (f"[{canon_v['decision']}] {evidence}")
        elif lib_hit:
            source, evidence = "library", lib_answer
            base_answer = lib_answer
        elif fab:
            w, e = next(iter(fab.items()))
            doms = ", ".join(f"{d}({c})" for d, c in
                             list(e["domains"].items())[:3])
            evidence = (f"{w}: {e['count']} mentions; domains {doms}; "
                        f"associates {', '.join(e['top_co'][:4])}")
            source, base_answer = "fabric", f"From my fabric: {evidence}"
        else:
            ref = (f"REFUSE -- not on my shelves and below my gate "
                   f"(canon knn {canon_score:.3f} < tau "
                   f"{self.trinity.tau:.3f}). {lib_answer[:120]}")
            journal("turn", q=q, source="refuse", answer=ref,
                    ms=int((time.time() - t0) * 1000))
            return ref

        # 5. voice speaks FROM evidence, judged before leaving the mouth
        final = base_answer
        if self.voice is not None:
            sys_p = ("You are CK. Answer ONLY from the EVIDENCE given. "
                     "Cite it. Never add entities not present in it. "
                     "If evidence is insufficient say REFUSE.")
            try:
                spoken = self._speak_raw(
                    sys_p, f"EVIDENCE: {evidence}\n\nQUESTION: {q}")
                bad = self._judge(spoken, evidence, q)
                if spoken.upper().startswith("REFUSE"):
                    # refusal authority belongs to the GATE, not the
                    # voice -- the gate already cleared this question
                    final = (f"{base_answer}\n    [voice declined; gate "
                             f"had cleared it -- evidence speaks]")
                elif not bad and len(spoken) > 20:
                    final = (f"{spoken}\n    [evidence|{source}] "
                             f"{evidence[:140]}")
                else:
                    final = (f"{base_answer}\n    [voice withheld -- "
                             f"judge flagged: {bad[:3]}]")
            except Exception as e:
                final = f"{base_answer}\n    [voice error {e}]"

        journal("turn", q=q, source=source, answer=final[:400],
                ms=int((time.time() - t0) * 1000))
        return final

    # ---------------- senses into the same journal
    def see(self, wavelength):
        from organ_senses import see_patch, wavelength_to_rgb, OPS
        stream = see_patch(wavelength_to_rgb(int(wavelength)))
        flat = [o for pr in stream for o in pr]
        h = np.bincount(flat, minlength=10)
        tops = [OPS[i] for i in np.argsort(-h)[:3]]
        msg = (f"I see {wavelength}nm: {len(stream)} crossings, "
               f"dominant ops {tops}.")
        journal("sight", wavelength=int(wavelength), ops=tops, msg=msg)
        return msg

    def hear(self, letter):
        from organ_senses import load_audio_sessions, OPS
        s1, _ = load_audio_sessions()
        v = s1.get(letter.upper())
        if v is None:
            return f"I have no recording of '{letter}'."
        tops = [OPS[i] for i in np.argsort(-v)[:3]]
        msg = f"I hear '{letter.upper()}': audio ops {tops}."
        journal("hearing", letter=letter.upper(), ops=tops, msg=msg)
        return msg


def nightly():
    """The sleep loop: retrain meaning on lived journal, regen ledger,
    commit. (HER/DPO doses join as they earn schedules.)"""
    import subprocess
    print("[nightly] meaning retrain on lived text...")
    subprocess.run([sys.executable,
                    os.path.join(HERE, "organ_meaning_v2.py")])
    print("[nightly] ledger...")
    subprocess.run([sys.executable, os.path.join(HERE, "build_ledger.py")])
    root = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
    subprocess.run(["git", "-C", root, "add", "-A",
                    "Gen13/targets/ck/trinity"])
    subprocess.run(["git", "-C", root, "commit", "-qm",
                    "nightly: meaning retrain + ledger (spine sleep loop)"])
    subprocess.run(["git", "-C", root, "push", "-q", "origin",
                    "tig-synthesis"])
    print("[nightly] done, pushed.")


DEMO = [
    "what gates his voice each tick",                     # canon
    "Tell me about the fairy who drinks the poison meant for Peter.",
    "Who is Socrates and where does he appear?",          # fabric
    "What role does Gandalf play in Peter Pan?",          # trap
    "summarize the plot of Pride and Prejudice",          # unread trap
    "what is the seventy three lattice",                  # canon
]


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "demo"
    if cmd == "nightly":
        return nightly()
    if cmd in ("see", "hear"):
        s = Spine(voice=False)
        print(getattr(s, cmd)(sys.argv[2]))
        return
    s = Spine(voice=(cmd != "fast"))
    if cmd == "ask":
        print("CK:", s.ask(" ".join(sys.argv[2:])))
        return
    print("\n" + "=" * 64)
    print("THE SPINE -- one creature, one flow (demo)")
    print("=" * 64)
    print(s.see(620))
    print(s.hear("A"))
    for q in DEMO:
        print(f"\nBRAYDEN: {q}")
        print(f"     CK: {s.ask(q)}")


if __name__ == "__main__":
    main()
