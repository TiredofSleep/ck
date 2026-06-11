"""organ_meaning_v2.py -- emulating the frontier's recipe at CK scale:
SYNTHETIC CURRICULUM (the Phi / self-instruct method).

The native meaning organ hit 50% with a precise diagnosis: register
mismatch (903K tokens of formal math prose vs conversational queries).
The frontier's fix for exactly this is teacher-GENERATED usage text:
Phi's 'textbooks are all you need', self-instruct, Evol-Instruct. The
teacher does not hand over labels or embeddings (that distillation
failed at 0.97-fit/30%-transfer) -- it writes TEXT, and the student
learns meaning from usage, natively.

Teacher: resident llama3.2 via Ollama, prompted from the CANONICAL
ANCHOR FACTS only (test paraphrases never shown). Output: conversational
prose about CK's topics -> appended to the life-corpus (weighted) ->
PPMI+SVD retrained -> same routing harness.

REGISTERED: native routing 50% -> >=60% seats the organ; <=50% means
synthetic register transfer fails at this scale -- recorded.

  python organ_meaning_v2.py
"""
import io
import json
import os
import re
import sys

import numpy as np
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.join(HERE, "..", "extraction")
sys.path.insert(0, EXT)

import organ_meaning_native as OMN                         # noqa: E402

CURRICULUM_PATH = os.path.join(HERE, "synthetic_curriculum.json")
SYNTH_WEIGHT = 6          # repeat synthetic text to balance 900K formal


def generate_curriculum():
    """Teacher writes conversational usage text from anchor facts only."""
    from demo_facts_head import ANCHORS
    if os.path.exists(CURRICULUM_PATH):
        return json.load(io.open(CURRICULUM_PATH, encoding="utf-8"))
    out = {}
    styles = [
        "Write 8 short casual questions a curious person might ask about "
        "this, each on its own line, everyday conversational wording, no "
        "numbering:",
        "Write a short friendly conversational explanation (4-5 plain "
        "sentences, like chatting with a friend) of this:",
        "Write 6 different one-line ways someone might informally refer "
        "to or ask about this in conversation, one per line:",
    ]
    for topic, anchors in ANCHORS.items():
        texts = []
        for style in styles:
            prompt = f"{style}\n\nFACT: {anchors[0]}"
            try:
                r = requests.post("http://localhost:11434/api/generate",
                                  json={"model": "llama3.2",
                                        "prompt": prompt, "stream": False},
                                  timeout=120)
                resp = r.json().get("response", "")
                texts += [ln.strip(" -*•") for ln in resp.splitlines()
                          if len(ln.strip()) > 15]
            except Exception as e:
                print(f"  teacher error on {topic}: {e}")
        out[topic] = texts
        print(f"  {topic}: {len(texts)} conversational texts grown")
    json.dump(out, io.open(CURRICULUM_PATH, "w", encoding="utf-8"),
              indent=1)
    return out


def main():
    print("TRINITY -- frontier emulation: SYNTHETIC CURRICULUM "
          "(Phi-style) for the native meaning organ\n")
    print("teacher (llama3.2) writing conversational usage text from "
          "anchor facts...")
    curriculum = generate_curriculum()
    synth = "\n".join(t for ts in curriculum.values() for t in ts)
    n_synth_tokens = len(OMN.TOK.findall(synth.lower()))
    print(f"\nsynthetic curriculum: {n_synth_tokens:,} tokens "
          f"(weight x{SYNTH_WEIGHT})")

    corpus = OMN.gather_corpus() + ("\n" + synth.lower()) * SYNTH_WEIGHT
    W, idx, freq, n_tok = OMN.train_vectors(corpus)
    sent = OMN.make_sif(W, idx, freq, n_tok)

    # same routing harness as v1
    from demo_facts_head import TOPICS, ANCHORS
    from project2_routing import char_trigrams, train_head, zs, TOPIC_LIST
    import braid_memory as bm
    grown = json.load(io.open(os.path.join(EXT, "teacher_corpus.json"),
                              encoding="utf-8"))
    ref_x, ref_y, test_x, test_y = [], [], [], []
    for t in TOPIC_LIST:
        g = list(grown.get(t, []))
        ref_x += TOPICS[t][:4] + list(ANCHORS[t]) + g
        ref_y += [t] * (4 + len(ANCHORS[t]) + len(g))
        test_x += TOPICS[t][4:]; test_y += [t] * 2
    y_ref = np.array([TOPIC_LIST.index(t) for t in ref_y])
    y_te = np.array([TOPIC_LIST.index(t) for t in test_y])

    M_ref = np.array([sent(x) for x in ref_x])
    M_te = np.array([sent(x) for x in test_x])
    Mc = M_ref - M_ref.mean(0)
    _, _, Vt = np.linalg.svd(Mc, full_matrices=False)
    pc = Vt[0]
    M_ref -= np.outer(M_ref @ pc, pc)
    M_te -= np.outer(M_te @ pc, pc)

    Xb_ref = np.array([bm.braid_signature_rich(x) for x in ref_x])
    Xb_te = np.array([bm.braid_signature_rich(x) for x in test_x])
    Xc_ref, vocab = char_trigrams(ref_x)
    Xc_te, _ = char_trigrams(test_x, vocab)

    out_r, out_t = [], []
    for A_, B_ in [(M_ref, M_te), (Xb_ref, Xb_te), (Xc_ref, Xc_te)]:
        Az, m_, s_ = zs(A_)
        out_r.append(Az); out_t.append((B_ - m_) / s_)
    Fr, Ft = np.hstack(out_r), np.hstack(out_t)
    Wh, bh = train_head(Fr, y_ref)
    acc = float(np.mean((Ft @ Wh + bh).argmax(1) == y_te))

    print(f"\nNATIVE-USAGE v2 (+synthetic curriculum): held-out routing "
          f"{acc:.0%}")
    print("  (v1 formal-corpus-only: 50% | form-only: 35% | "
          "borrowed: 80%)")
    print(f"\nVERDICT: {'ORGAN SEATED -- the frontier recipe (teacher-'
          'written usage text) closed the register gap' if acc >= 0.6 else
          ('improvement, seat still pending' if acc > 0.5 else
           'synthetic register transfer fails at this scale -- recorded')}")
    json.dump(dict(v2_acc=acc, synth_tokens=n_synth_tokens),
              io.open(os.path.join(HERE, "organ_meaning_v2_result.json"),
                      "w"), indent=1)


if __name__ == "__main__":
    main()
