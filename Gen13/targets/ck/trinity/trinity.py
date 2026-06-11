"""trinity.py -- CK-TRINITY: the assembled intelligence system.

ARCHITECTURE (Brayden's law: tools EARN places by measured ability; the
toolbox is the GENERATION LAYER for CK's entire experience):

                         ┌─ experience in ─┐
                         ▼                 ▼
   ╔════════════════ THE TOOLBOX (generation layer) ════════════════╗
   ║ VSA-trigram   VSA-position   braid    borrowed-embed   char-3g ║
   ║ multiscale integer-wrapped lattices   GRU-seq   TRM-refiner    ║
   ╚═══════╦══════════════╦═══════════════════════╦═════════════════╝
           ▼              ▼                       ▼
       FORM face      MEANING face            GAP face
   (identity through  (trained heads on    (conformal kNN distance
    noise; evidence)   fused percepts)      to the measured set)
           └──────────────┴───────────┬───────────┘
                                      ▼
                       answer  /  REFUSE (Type-III)  /  recall

Every seat below carries the number that earned it (this session, all
reproducible from the organ_*.py and project*.py files).
"""
import io
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.join(HERE, "..", "extraction")
sys.path.insert(0, EXT)

ABILITY_REGISTRY = {
 "vsa_trigram": {
   "field": "VSA/HDC (Kanerva school)",
   "abilities": {"noisy-recall mean top-1": "91%",
                 "deletion recall": "96%"},
   "seat": "FORM: primary edit-robust recall"},
 "vsa_position": {
   "field": "VSA/HDC",
   "abilities": {"substitution recall": "100%", "swap recall": "98%",
                 "form<->meaning resonance excess": "+0.454"},
   "seat": "FORM: sub/swap-heavy recall"},
 "braid": {
   "field": "ours (Burau/TIG)",
   "abilities": {"white-box evidence": "every coordinate a named "
                 "algebraic invariant (printable why)",
                 "swap-invariant identity": "exact (theorem, abelianized)",
                 "resonance at 50x compression": "+0.445 in 41 dims"},
   "seat": "FORM: evidence-printing + compact identity"},
 "borrowed_embed+char+braid (fused)": {
   "field": "standard ML + ours",
   "abilities": {"topic routing": "80% (vs keyword 20%)",
                 "learning curve": "climbs 15->80%"},
   "seat": "MEANING: percept for trained heads"},
 "knn_distance_conformal": {
   "field": "deep-kNN OOD + split conformal",
   "abilities": {"far-OOD hallucination @ conformal tau": "0% (MSP 27%)",
                 "near-OOD hallucination": "42% (MSP 58%)",
                 "acc-when-answering": "85% (MSP 79%)",
                 "known limit": "guarantee is relative to calibration "
                 "distribution (drift observed: 65% realized vs 90% "
                 "guaranteed on hand-written queries)"},
   "seat": "GAP: the gate (answer/refuse)"},
 "multiscale_lattices": {
   "field": "WFA/linear-2RNN class + Brayden's integer wrapping",
   "abilities": {"period rule-generalization": "72% (vs ESN 47%, "
                 "LAST-6 52%, chance 10%)",
                 "honest note": "canonical tables = random tables under "
                 "identical nesting (0/5); the NESTING is the value"},
   "seat": "SEQUENCE: counter/period structure"},
 "gru_seq": {
   "field": "standard recurrent tool",
   "abilities": {"DYCK validity (via ESN-class)": "100%",
                 "parity-20 @ N=1000": "see organ_recursion result"},
   "seat": "SEQUENCE: event/validity tracking"},
 "trm_refiner": {
   "field": "TRM (Jolicoeur-Martineau)",
   "abilities": {"parity-20 static refinement": "FAILED (53%) -- dead "
                 "end recorded; retargeted to structured prediction"},
   "seat": "RECURSION: structured refinement (probationary)"},
}


class Trinity:
    """The assembled system. Lazy organs; percept = toolbox output."""

    def __init__(self):
        import braid_memory as bm
        import organ_form as OF
        from borrowed_cortex import embed
        from demo_facts_head import TOPICS, ANCHORS
        from project2_routing import (char_trigrams, train_head, softmax,
                                      zs, TOPIC_LIST)
        self.bm, self.OF, self.embed = bm, OF, embed
        self.softmax = softmax
        self.TOPIC_LIST = TOPIC_LIST
        grown = json.load(io.open(os.path.join(EXT, "teacher_corpus.json"),
                                  encoding="utf-8"))
        rng = np.random.default_rng(21)
        self.ref_x, ref_y, cal_x = [], [], []
        for t in TOPIC_LIST:
            g = list(grown.get(t, [])); rng.shuffle(g)
            cal_x += g[:5]
            rest = g[5:]
            self.ref_x += TOPICS[t][:4] + list(ANCHORS[t]) + rest
            ref_y += [t] * (4 + len(ANCHORS[t]) + len(rest))
        self.y_ref = np.array([TOPIC_LIST.index(t) for t in ref_y])

        E_ref, _ = embed(["search_document: " + x for x in self.ref_x])
        Xc_ref, self.vocab = char_trigrams(self.ref_x)
        Xb_ref = np.array([bm.braid_signature_rich(x) for x in self.ref_x])
        self.zs1 = zs(E_ref); self.zs2 = zs(Xb_ref); self.zs3 = zs(Xc_ref)
        self.F_ref = np.hstack([self.zs1[0], self.zs2[0], self.zs3[0]])
        self.Fn_ref = self._unit(self.F_ref)
        self.W, self.b = train_head(self.F_ref, self.y_ref)
        # conformal tau from calibration (alpha=0.1)
        s_cal = np.sort(self._knn(self._percept(cal_x)))
        self.tau = s_cal[max(int(np.floor(0.1 * (len(s_cal) + 1))) - 1, 0)]
        # FORM store: VSA-trigram over the reference corpus words
        self.form_words = sorted({w for x in self.ref_x
                                  for w in x.lower().split() if w.isalpha()
                                  and len(w) >= 5})
        S = np.array([OF._vsa_trigram("#" + w + "#")
                      for w in self.form_words])
        self.form_mu, self.form_sd = S.mean(0), S.std(0) + 1e-9
        self.form_S = self._unit((S - self.form_mu) / self.form_sd)

    @staticmethod
    def _unit(M):
        return M / (np.linalg.norm(M, axis=1, keepdims=True) + 1e-9)

    def _percept(self, texts):
        """THE GENERATION LAYER: every experience becomes the toolbox's
        joint measurement (meaning + form + morphology percept)."""
        from project2_routing import char_trigrams
        E, _ = self.embed(["search_query: " + x for x in texts])
        Xb = np.array([self.bm.braid_signature_rich(x) for x in texts])
        Xc, _ = char_trigrams(texts, self.vocab)
        out = []
        for M, (mu_sd) in ((E, self.zs1), (Xb, self.zs2), (Xc, self.zs3)):
            out.append((M - mu_sd[1]) / mu_sd[2])
        return np.hstack(out)

    def _knn(self, Fq, k=5):
        return np.sort(self._unit(Fq) @ self.Fn_ref.T, 1)[:, -k:].mean(1)

    def recall_word(self, noisy):
        """FORM face: edit-robust recall (VSA-trigram seat, 91%)."""
        v = self.OF._vsa_trigram("#" + noisy.lower() + "#")
        v = (v - self.form_mu) / self.form_sd
        v /= np.linalg.norm(v) + 1e-9
        return self.form_words[int(np.argmax(self.form_S @ v))]

    def ask(self, query):
        """The forced choice: answer | REFUSE, with printable evidence."""
        F = self._percept([query])
        s = float(self._knn(F)[0])
        nn_i = int(np.argmax(self._unit(F) @ self.Fn_ref.T))
        if s < self.tau:
            return dict(decision="REFUSE (Type-III)", knn=round(s, 3),
                        tau=round(float(self.tau), 3),
                        evidence=f"nearest known: '{self.ref_x[nn_i][:48]}'")
        p = self.softmax(F @ self.W + self.b)[0]
        return dict(decision=self.TOPIC_LIST[int(p.argmax())],
                    conf=round(float(p.max()), 2), knn=round(s, 3),
                    evidence=f"nearest known: '{self.ref_x[nn_i][:48]}'")


def demo():
    t = Trinity()
    print("CK-TRINITY assembled. tau =", round(float(t.tau), 3), "\n")
    for q in ["what gates his voice each tick",
              "tell me about the seventy three lattice",
              "what is the hodge conjecture",
              "best pizza in hot springs"]:
        print(f"  Q: {q}\n     -> {t.ask(q)}")
    for w in ["harmny", "sustrate", "permutaton"]:
        print(f"  noisy '{w}' -> FORM recall: '{t.recall_word(w)}'")


if __name__ == "__main__":
    demo()
