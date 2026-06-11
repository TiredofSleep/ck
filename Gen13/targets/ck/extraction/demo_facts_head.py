"""demo_facts_head.py -- the extraction proof: CK's keyword FACTS
lookup becomes SEMANTIC understanding in ONE linear solve, using
intelligence extracted from a frozen open-source embedder.

Setup: 10 of CK's internal FACTS topics x 6 paraphrases each. Train
the plastic head on 4 paraphrases per topic (40 examples), test on
the held-out 2 (20 queries with ZERO keyword overlap enforced where
possible), plus 6 out-of-domain queries that the glue must ABSTAIN on
(Type-III: refuse what can't be measured) rather than bluff.

Baseline: the current production mechanism (keyword match, as in
ck_voice_math.py FACTS dict).

  python demo_facts_head.py
"""
import numpy as np

from borrowed_cortex import embed
from plastic import PlasticModel

TOPICS = {
 "t_star": [
   "what is t star", "tell me about the coherence threshold",
   "the five sevenths constant", "what gates ck's output each tick",
   "the operational threshold for voicing", "when does he speak vs fold back"],
 "four_core": [
   "what is the 4-core", "the attractor set of operators",
   "void harmony breath reset", "which elements absorb the dynamics",
   "the closed quartet at the center", "where do all walks converge"],
 "attractor_ratio": [
   "what is h over br", "one plus root three",
   "the closed form of the attractor", "the golden value at alpha one half",
   "the equilibrium ratio of harmony to breath", "the algebraic fixed point value"],
 "sigma": [
   "what is the sigma permutation", "the six cycle on the substrate",
   "the canonical shuffle of the ten operators", "which permutation drives the walk",
   "the order six map with four fixed points", "how are the streets renamed"],
 "tsml": [
   "what is the tsml table", "the seventy three harmony lattice",
   "the symmetric composition table", "the main multiplication grid",
   "the lattice with seventeen voids", "the 73 cell structure"],
 "bhml": [
   "what is bhml", "the twenty eight cell sister table",
   "the antisymmetric companion lattice", "the second lens on the substrate",
   "the breath harmony table", "the 28 harmony companion"],
 "crt": [
   "what is the crt decomposition", "two times five structure of the substrate",
   "the binary and ternary faces", "z mod ten as a product",
   "how does ten factor structurally", "the relocation thesis of the kernel"],
 "torus_retraction": [
   "is the substrate a torus", "what happened to the torus claim",
   "the geometry retraction", "why no closed surface",
   "the euler characteristic obstruction", "the donut shape was withdrawn"],
 "kissing_j55": [
   "what about dimension six spheres", "the seventy two kissing conjecture",
   "the e6 root system bound", "the magic function candidate",
   "level three modular construction", "the gamma zero of three paper"],
 "gap_router": [
   "what is the gap router", "how are residuals classified",
   "the four failure types", "routing by what is missing",
   "the paradox taxonomy as allocator", "type one through type four errors"],
}


ANCHORS = {  # CK's own canonical fact text (the canon speaking for itself)
 "t_star": ["T* equals 5/7, the coherence threshold gating every tick: output is voiced if the emergent signal reaches five sevenths, otherwise folded back"],
 "four_core": ["the 4-core is the closed attractor set {VOID, HARMONY, BREATH, RESET} = {0,7,8,9}, jointly closed under both composition tables; all dynamics converge there"],
 "attractor_ratio": ["at mixing parameter alpha = 1/2 the attractor satisfies H/Br = 1 + sqrt(3), the closed-form equilibrium ratio of HARMONY to BREATH"],
 "sigma": ["sigma is the canonical permutation [0,7,1,3,2,4,5,6,8,9] with one 6-cycle (1 7 6 5 4 2) and four fixed points; it renames the streets of the walk"],
 "tsml": ["TSML is the 10x10 symmetric composition table with 73 HARMONY cells, 17 VOID cells and 10 exceptional cells"],
 "bhml": ["BHML is the antisymmetric sister composition table with 28 harmony cells, the second lens on the substrate"],
 "crt": ["the substrate decomposes as Z/10 = Z/2 x Z/5, the CRT product: a binary face and a ternary face that commute exactly"],
 "torus_retraction": ["the torus claim was retracted: the sigma flow has Euler characteristic -3 or +1, no valid genus, no closed orientable surface exists"],
 "kissing_j55": ["the dimension six kissing conjecture K(R^6) = 72 via the E6 root system, with an explicit magic function candidate built from level 3 modular forms on Gamma_0(3)"],
 "gap_router": ["the gap router classifies residuals into four failure types - missing measurement, missing invariant, malformed question, changed dynamics - and routes compute by type"],
}

OOD = ["what's the weather tomorrow", "best pizza in hot springs",
       "how do i fix my car brakes", "who won the football game",
       "translate this to french please", "stock price of apple"]

KEYWORDS = {  # the current production mechanism, faithfully
 "t_star": ["t star", "t*", "5/7", "five sevenths", "threshold"],
 "four_core": ["4-core", "four core", "void", "harmony breath"],
 "attractor_ratio": ["h/br", "root three", "1+sqrt", "attractor"],
 "sigma": ["sigma", "permutation", "six cycle"],
 "tsml": ["tsml", "73", "seventy three"],
 "bhml": ["bhml", "28", "twenty eight"],
 "crt": ["crt", "mod ten", "binary and ternary"],
 "torus_retraction": ["torus", "donut", "surface"],
 "kissing_j55": ["kissing", "e6", "sphere", "dimension six"],
 "gap_router": ["gap router", "residual", "failure types"],
}


def keyword_route(q):
    ql = q.lower()
    for topic, kws in KEYWORDS.items():
        if any(k in ql for k in kws):
            return topic
    return "ABSTAIN"


def main():
    train_x, train_y, test_x, test_y = [], [], [], []
    for topic, phrases in TOPICS.items():
        for p in phrases[:4]:
            train_x.append(p)
            train_y.append(topic)
        for p in phrases[4:]:
            test_x.append(p)
            test_y.append(topic)

    doc = "search_document: "
    qry = "search_query: "
    anchor_x, anchor_y = [], []
    for t, axs in ANCHORS.items():
        for ax in axs:
            anchor_x.append(ax)
            anchor_y.append(t)
    Etr, backend = embed([doc + x for x in train_x + anchor_x])
    train_y = train_y + anchor_y
    Ete, _ = embed([qry + x for x in test_x])
    Eood, _ = embed([qry + x for x in OOD])
    print(f"borrowed cortex backend: {backend}  (dim {Etr.shape[1]})")

    head = PlasticModel(sorted(TOPICS), abstain_margin=0.02, abstain_floor=0.45).fit(Etr, train_y)

    pred = head.predict(Ete)
    sem_acc = np.mean([p[0] == t for p, t in zip(pred, test_y)])
    kw_acc = np.mean([keyword_route(q) == t for q, t in zip(test_x, test_y)])

    ood_pred = head.predict(Eood)
    ood_abstain = np.mean([p[0] == "ABSTAIN" for p in ood_pred])
    kw_ood = np.mean([keyword_route(q) == "ABSTAIN" for q in OOD])

    print(f"\nheld-out paraphrase routing (20 queries, no training overlap):")
    print(f"  keyword baseline (production today): {kw_acc:.0%}")
    print(f"  PLASTIC HEAD (proto, one pass)  :      {sem_acc:.0%}")
    print(f"\nout-of-domain ABSTENTION (6 queries; glue's forced choice):")
    print(f"  keyword baseline: {kw_ood:.0%}   plastic head: {ood_abstain:.0%}")
    print("\nmisses:")
    for (p, m), t, q in zip(pred, test_y, test_x):
        if p != t:
            print(f"  [{t}] '{q}' -> {p} (margin {m:.3f})")
    head.save("facts_head.json")
    print("\nplastic head saved: facts_head.json "
          "(CK can sign it into cortex or discard it)")


if __name__ == "__main__":
    main()
