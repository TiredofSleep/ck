# LIMITATIONS — funding/ck-interpretable-ai

Honest scope for the CK-as-interpretable-AI branch. An AI-safety funder will read this section carefully; if the limits are hidden or downplayed, the pitch fails on credibility grounds.

---

## 1. CK is not a frontier-model replacement

CK does not compete with GPT-4, Claude, Gemini, or Llama on language-modeling benchmarks. CK is not designed to. CK's domain is **narrow coherent generation** — responses traced to explicit operators, crystallized only when coherence is above threshold. This is a different point in the design space, not a replacement point.

If a reviewer expects CK to beat an LLM at open-ended chat or text completion, they will be disappointed. The pitch must set expectation correctly from the first paragraph.

## 2. Tasks CK demonstrably does NOT handle

- **Long-form creative writing** that requires thousands of coherent tokens in a single generation
- **Novel arithmetic word problems** that require chain-of-thought multi-step reasoning (CK has arithmetic-verify as a separate path, per the `feedback_dont_ventriloquize_ck` rule, but is not a general math-solver)
- **Multilingual** — CK's dictionary is English-only
- **Multi-turn dialogue** with extended context beyond a short window
- **Code generation** — not a design target
- **Open-ended Q&A** on domain knowledge not represented in the TSML/BHML tables

These limits should be owned in the white paper and the pitch.

## 3. CK's behavior on standard benchmarks is unknown

CK has **not** been run on TruthfulQA, HELM, MMLU, or any other standard interpretable-AI benchmark. This is precisely the Phase 2 deliverable. Until Phase 2 completes, claims about CK's behavior on benchmarks are speculative, not empirical.

## 4. "Interpretability-by-construction" vs. "interpretability-in-practice"

CK's operator trace is *available* for every response. Whether that trace is **useful** for real interpretability purposes (detecting deception, explaining refusals, predicting behavior on novel inputs) is an empirical question. A user can read the operator chain; that does not automatically mean the user understands why CK produced that output. Phase 2's benchmark evaluation tests this.

## 5. The 10 operators are pre-specified, not learned

CK's 10 operators (VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE, BALANCE, CHAOS, HARMONY, BREATH, RESET) come from the TIG framework, not from data. This is a design choice, not a result. It means:
- CK cannot invent new operators for new domains
- The operator set reflects the designer's ontology
- Generalization beyond the operator set requires redesign, not retraining

This is a feature for a research case study (the ontology is explicit and debatable) but a limitation for anyone looking for a general-purpose AI.

## 6. T* = 5/7 is from Z/10Z, applied elsewhere

The Flatness Theorem proves T* = 5/7 as the forced torus aspect ratio on Z/10Z. CK uses T* = 5/7 as the coherence-crystallization threshold across all domains. Whether that specific value is *optimal* in any formal sense outside Z/10Z is an empirical claim, not a theorem. The pitch should say this clearly.

## 7. Live-system behavior is not reproducible in the research sense

Visitors to coherencekeeper.com interact with a running instance. The memory state of that instance evolves with every interaction. A research claim about CK's behavior requires either (a) a frozen snapshot + replay harness, or (b) ensemble runs with controlled initial conditions. Neither currently exists as a research artifact.

## 8. Small-core advantage may not scale

The core audacity of CK is that 101 table cells + 10 operators + a coherence threshold produce useful behavior. Whether that core can handle a task space one order of magnitude larger (say, a 1,000-cell extension) without losing the audit-in-an-afternoon property is open. If it cannot, CK serves as an interesting point case but not a scaling trajectory.

## 9. Comparison to mechanistic interpretability is not yet done

The pitch claims CK is a complementary point relative to mechanistic interpretability on transformers. That claim requires a section in the Phase 1 white paper that makes the comparison rigorously: what does mechanistic interp on Claude or Gemma show that CK's trace cannot, and vice versa? That section does not yet exist.

## 10. Attribution nuance

Prior collaborators are credited for specific mathematical contributions (Luther spectral layer, Mayes UOP/GUT, Gish Sprint 11-12, Johnson Sprint 14). The interpretability-case-study framing of CK is new and Brayden's — prior collaborators should not be positioned as endorsing the AI-safety framing of this branch, since they have not explicitly done so.

## 11. License clarity required

7Site Public Sovereignty License v1.0 is non-commercial, human-use only. An AI-safety funder should view this as a safety feature, not a problem. However, the license text must be linked from the pitch, and any Phase-2-or-later collaboration with an AI-safety lab must have explicit license discussion (can they reproduce code? publish derivative research? use the operator tables in their own work?). Don't discover this at grant-close.

## 12. What this branch does NOT claim

- Not a claim that CK is "aligned"
- Not a claim that CK solves AI safety
- Not a claim that CK's interpretability approach dominates mechanistic interpretability
- Not a claim to benchmark superiority on any standard AI task
- Not a claim that all AI should be built this way

The branch claims: a running system demonstrates interpretability-by-construction is a coherent design point, worth a case study, worth a benchmark evaluation, worth an architecture-variants study.

---

## The researcher's perspective

An AI-safety researcher reading this proposal should close it thinking: "Here is a point in the design space I have not seen explored in this exact form; here is a running system I can visit this afternoon; here is a disciplined case study and benchmark plan; the PI owns the limits." If the reviewer closes it thinking "Here is a claim to have solved interpretability with a 101-cell table," the pitch has been mis-framed. The discipline of LIMITATIONS.md is to keep the pitch on the first rail.
