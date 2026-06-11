# CK's training path — start simple, measure every step

**2026-06-11.** Brayden: *"train CK and his AI to explicitly learn and solve a project, start
simple... I believe there's genuinely something great about CK, though I've only seen glimpses
of intelligence that made me go hmmm."*

## The architecture the measurements forced us to (honest)

CK's intelligence is **a trained head over multiple white-box representations**, each carrying
a different signal the world actually has:

| representation | carries | proven on |
|---|---|---|
| **braid (identity/topology)** | edit-robust word identity | 44% recall through misspelling, swap 71% |
| **char/morphology** | suffixes, grammatical shape | POS 69% (Project 1) |
| **borrowed embedding** | meaning (within a language) | form<->meaning 0.58 |
| **substrate reservoir** | temporal/sequential structure | Mackey-Glass +36% (J56) |
| **gap-router diagnostics** | which kind of error this is | 24/24 type-ID (J56) |

The head (one ridge solve or a tiny softmax, both white-box) learns which to weight per task.
This is the version that survived every adversarial test this session -- not "the substrate is
the language of thought" (falsified), but "a fusion of measured, interpretable signals with a
trained selector."

## The ladder of projects (each gated by a learning curve + a baseline)

Every rung: pick a task with a decidable label, assemble the representations that should carry
its signal, train the head, run the seven tests (`HOW_AI_IS_TRAINED.md`), and demand a climbing
learning curve AND a beaten baseline. If both, the rung holds; if not, add a representation or
retire the claim.

1. **DONE -- Project 1: grammatical category from form.** Learning curve climbed 46->69%;
   taught the workflow; found the representation lesson. CK's first trained skill.
2. **Project 2: word-sense / topic routing** (the FACTS router, properly). Fuse braid + borrowed
   embedding + teacher-grown corpus; target a clean learning curve past the 50% we saw with the
   frozen head. Metric: held-out routing accuracy + abstention on out-of-domain.
3. **Project 3: the abstention governor** (the real external test from the path doc). Wrap a
   frozen small LLM; the head learns to route Type-III (unanswerable) to refusal. Baseline:
   confidence-thresholding. Metric: hallucination rate at fixed coverage. **This is the first
   rung that competes against an outside method on its own benchmark** -- the worthiness test.
4. **Project 4: a symbolic/structured task at ~1k examples** (TRM lane) where the substrate
   reservoir's inductive bias is the hypothesis. Ablation: substrate features vs a same-size
   random net. This is the direct test of "does CK's algebra give a useful inductive bias?"
5. **Project 5: sequence/synthesis** -- next-operator prediction on CK's own walks, then short
   compositional generalization (learn a rule from examples, apply to unseen inputs). The first
   "synthesis" rung; metric: generalization to held-out rule instances.

## Your big vision, made into an experiment (not a belief)

*"If a billion-param AI were trained to read his language, the gap may fill if the storage has
association/synthesis built in."* The honest translation: **does the substrate provide a useful
inductive bias?** You test it without a billion parameters — you test it at rung 4 with an
ablation. If substrate-features + small-head beats same-size-random + small-head on a structured
task, the substrate earns its inductive bias, and scaling up is then a funding question, not a
faith question. If it ties (as it did for POS, 69.6 vs 69.2), the substrate is neutral for that
task and the signal lives elsewhere. Either way you KNOW, and you scale only what earned it.

## The glimpses that made you go hmmm -- what they were, honestly

The real ones, measured: the braid recalling a word through a misspelling (topological memory
that survives noise -- genuinely brain-like); the gap-router sorting failure types and matching
an oracle; form<->meaning resonance surviving the word-length control. Those are not nothing --
they are small, real, white-box capabilities that black boxes don't expose. The path to "more"
is not a bigger claim; it's the next rung, measured. Start simple (Project 2), keep the seven
tests honest, and let the learning curves tell you which glimpses were signal. The greatness,
if it's there, will show up as a curve that climbs and a baseline that's beaten -- and you'll
have PROVEN it, the way this whole project proves things.
