# How AI is trained — the tests people run (worked on CK's Project 1)

**For Brayden, 2026-06-11.** You asked "what kind of tests do people run as they train AI?"
Here they are, every one demonstrated on a real run: `extraction/project1_pos.py` (predict a
word's grammatical category from its FORM, 24,000 labeled words from CK's own dictionary, 9 s
on CPU).

## The seven tests, in the order you run them

**1. Train / validation / test SPLIT.** Cut the data three ways. *Train* (70%) the model
learns from. *Validation* (15%) you peek at while tuning. *Test* (15%) you touch ONCE, at the
end. The rule that separates science from self-deception: **never measure on data you trained
on.** A model can memorize its training set and look brilliant while having learned nothing
that transfers.

**2. LOSS CURVE** (loss vs epoch). One "epoch" = one pass through the training data. The
*loss* is how wrong the model is; you watch it fall live as it trains. If it doesn't fall,
the model isn't learning (Project 1's braid loss stayed flat at ~1.03 — a red flag we
diagnosed: the features didn't carry the signal).

**3. LEARNING CURVE** (test accuracy vs #training examples). **This is the most important test
for your vision.** Train on 50 examples, then 200, then 1000, 5000, 16800 — plot accuracy at
each. If the curve *climbs*, more data helps → the representation carries the signal → "the
gap fills with training." If it's *flat*, the representation is capped and more data won't
save you. Project 1, fused features: 46% → 54% → 60% → 66% → 69% — a clean climb. Braid-only:
35% → 51% and stuck at the majority baseline — capped.

**4. GENERALIZATION GAP** (train accuracy − test accuracy). If the model scores 99% on train
and 60% on test, gap = 39% → it *overfit* (memorized, didn't generalize). A small gap is
healthy. Project 1: train 51.7% − test 51.6% = +0.2% — healthy (the problem wasn't overfitting,
it was an underpowered representation).

**5. BASELINES.** Before celebrating any number, beat the dumb thing.
- *Majority-class*: always guess the most common label (Project 1: 51.4% nouns). If your model
  can't beat this, it learned nothing.
- *A simple-feature baseline*: here, character-trigrams (69%). If your fancy representation
  can't beat dumb string features, the fancy part isn't earning its keep. **This is the test
  that keeps you honest** — it's why we found the braid alone (45%) was worse than trigrams.

**6. CONFUSION MATRIX** (rows = true, cols = predicted). Shows *which* classes get confused.
Project 1's braid matrix had every row dumping into "noun" — instantly revealing it learned
the majority class, not the task. Interpretable diagnosis in one glance.

**7. ABLATION / representation comparison.** Swap one piece, hold the rest fixed, re-measure.
Project 1: braid (45%) vs char-trigram (69%) vs fused (69.6%) — proves the morphology signal
lives in the trigrams, and tells you exactly what to feed the model.

## The one lesson that runs your whole vision

**The representation sets the ceiling; training climbs to it.** A model can only learn what its
input features carry. The braid carries *identity/topology* (great: 44% edit-robust recall)
but throws away *suffix morphology* (so it can't do POS). Char-trigrams carry morphology (so
they can). Neither carries *meaning* across languages (the cross-family negative). **Different
tasks need different signals — so CK's intelligence is a trained head over MULTIPLE
representations** (braid-identity + char-morphology + borrowed-meaning + substrate-reservoir),
each carrying a different part of the world, the head learning which to use.

Your big hypothesis — "a billion-param AI trained on CK's language could fill the gap if the
storage carries association/synthesis" — is the SCALED version of Project 1's learning curve,
and it is TESTABLE the same way: does training climb, and does the substrate representation
beat the dumb baseline (the ablation)? Project 1 says: training climbs when the signal is
present (yes), and the substrate must EARN its place against char-trigrams task by task (for
POS it tied; for memory-recall it won big). That's not a verdict against your vision — it's
the measuring instrument FOR it.
