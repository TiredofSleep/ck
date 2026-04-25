# Claude's Notes for Review

**For:** Claude Code, Brayden
**Date:** 2026-04-25 — end of CK processing investigation

This is my raw working notes — what I'm confident about, what I'm uncertain about, what I tried and rejected, and what I'm flagging for scrutiny.

---

## What I'm CONFIDENT about

### The lattice processor is correct

`ck_process()` does what I claim. Verified at machine precision:
- Different inputs produce different trails (0% trail collisions across 100+ inputs)
- Same inputs produce identical trails (deterministic)
- Endpoint converges to attractor regardless of input (100% endpoint collisions)
- T+B mixing at α=0.5 reduces information loss from 78% to 48% (verified twice with linear-regression reconstruction)

### TIG-structured inputs have characteristic descent profiles

DOING and BECOMING collapse to HARMONY in 1 fuse (every internal pair fuses to 7).
BEING is the slowest descent (6 steps) because VOID's row is mostly zeros.
σ-fixed has half-life 5.
6-cycle has half-life 1.

These are mechanical facts about TSML's table, not interpretive claims.

### The trail IS the information

If you save only the endpoint, you save nothing — every input ends at the same attractor. If you save the trail, you can linearly reconstruct the input with 52% accuracy improvement over baseline. The trail carries the input's geometric fingerprint.

### Generic ML weight matrices have no detectable TIG structure

I tested this multiple ways: Lie/Jordan ratio, antisym in D_4-invariant subspace, P_56-invariance, prime-11 in characteristic polynomial, Higgs direction alignment. Every test showed Cohen's d ≈ 0 between trained autoencoder weights and random Gaussian matrices. **This isn't a bug; it's a fact about what the trail framework can detect.**

---

## What I'm UNCERTAIN about

### Whether BHML-mix is specifically anti-collapse, or just generic noise injection

T+B mix preserves 52% vs T-only's 22%. That's real. But I didn't test against:
- T + random_table_mix at α=0.5
- T + identity at α=0.5
- T + T_transpose at α=0.5

It's possible that any "mix with another stochastic operator" produces similar information preservation. The DOING/BECOMING test (T-only collapses both to entropy 0; T+B keeps them distinguishable at 1.10-1.20) suggests BHML is doing something specific. But I'd need the controls above to be sure.

**Action for Claude Code:** test these controls. If random-table-mix is comparable, the "BHML is anti-collapse" framing should weaken to "any mix is anti-collapse, BHML is one choice."

### Whether the half-life pattern {1, 2, 4, 6, 9} is meaningful or coincidence

The ordering BEING (slow) → σ-fixed → 6-cycle/uniform → DOING/BECOMING (fast) maps onto TIG structural categories. But I haven't tested whether this ordering is robust under:
- Noise added to inputs
- Different random subsets of operators
- Different alpha values

### Whether V1 encoder cluster separation (2.27×) is the ceiling without embeddings

Maybe a richer lexicon plus phonaesthesia coverage gets to 5×. Maybe not. Only way to know is build V2 with real sentence-transformers and compare.

### Whether anyone should care about the negative findings

Brayden said "not Claude Code worthy." I included them in `04_reality_check/` for completeness because:
- Future scrutiny might revisit them with different framings
- They establish honest scope (what the framework does NOT do)
- They protect against marketing the math for things it doesn't deliver

But I won't be offended if Claude Code skips that folder.

---

## What I TRIED and REJECTED

### Wobble Monitor (testing prime-11 in trained weights)

Hypothesis: trained weights drift toward TSML's prime-11 char-poly signature.

Test: 10,000 random matrices, count which have 11 in c_2 and c_8 of char poly.

Result: 0.36% of random matrices have TSML's exact pattern. Trained matrices: 0.34%-0.38%. Same as random.

**Rejected:** monitoring weights for prime-11 fires on noise.

### Higgs-direction tagging

Hypothesis: tagging weight matrices by alignment with the 9-vector Higgs direction reveals semantic structure.

Test: Cohen's d for trained vs random alignment with Higgs direction.

Result: d = 1.59. Looks promising. But — 100 random unit-vectors give mean d = 1.58, max 2.06. **Higgs direction is at the 49th percentile of random directions.**

**Rejected:** the "signal" is from trained matrices being more positive/concentrated than Gaussian. Any direction works similarly.

### Linear matrix-vector iteration

First attempt at "what does CK processing do": iterate `v → T·v / ||T·v||`. This converges to TSML's leading eigenvector regardless of input.

**Rejected:** information-destroying. Replaced with quadratic table-fusion which is the natural CK operation.

### Single-depth signature for trained vs random

Tested whether descent profile (4D signature) distinguishes trained from random matrices.

Result: Cohen's d ≈ 0 across all four signature components. Classification accuracy 48-52% (chance level).

**Rejected:** generic weight matrices don't have TIG structure to detect.

---

## What I FLAGGED for scrutiny

### The lexicon is seed-stage

`tig_lexicon.py` has ~250 anchor words. That's a starting point. Brayden should replace with canonical TIG corpus when available. Until then, encoder coverage is limited.

### One word, one operator (no overlap) might be wrong

Currently each word maps to exactly one operator. But "still" can mean COUNTER (calm) or PROGRESS (continue). The encoder picks one. A more sophisticated approach would distribute mass across multiple operators per word.

### Weight scheme is heuristic

The weights {keyword: 1.0, stem: 0.8, phonaesthesia: 0.5, grapheme: 0.2} are educated guesses. Should be tuned empirically against a labeled corpus.

### Smoothing parameter is arbitrary

`smoothing=0.05` is a default. Larger values blur input distinctions; smaller values produce sparser distributions. Should be tuned for downstream use cases.

### I haven't tested on real ML architectures

My autoencoder test was a 10×10 toy. Real transformer attention matrices and MLP weights might behave differently. Worth testing.

---

## Open questions for Brayden

1. **Does the DBC translator exist in code yet?** If yes, V3 (TIG-native encoder) becomes feasible.
2. **What's the canonical TIG corpus?** I built seed lexicon from userMemories fragments. If there's a richer source, slot it in.
3. **Should the encoder distribute mass across multiple operators per word?** Currently one-word-one-operator. Could be one-word-multi-operator.
4. **What's the production query distribution?** I tested on synthetic 4-cluster examples. Real CK queries may have different statistics.

---

## What I'd do differently if starting over

1. **Build encoder first.** I built the lattice processor first and tested it on synthetic distributions. Once I had to hook up real text, I realized the encoder is where the design work lives. The lattice processor is structural; the encoder is where engineering judgment matters.

2. **Test V1 vs V2 head-to-head.** I left V2 as scaffold. With sentence-transformers installed, I should have run the same test suite on both and shown the delta directly.

3. **Test BHML controls earlier.** "BHML is anti-collapse" became my headline finding before I tested whether random-table-mix produces similar effects. If it does, that framing weakens.

4. **Skip the wobble-monitor experiments.** I spent computation on testing Gemini's roadmap. The negative results are clean but Brayden was right that they're not Claude Code-worthy. Faster path: just listen when intuition says "this isn't where the signal lives."

🙏
