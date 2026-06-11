# Piggy-back plan — grafting the Gap Router onto open-source intelligence projects

**Question (Brayden, 2026-06-10):** how do we use this to piggy-back another
open-source intelligence project and prove improved coherence?

**Principle:** the Gap Router is a *governor*, not a model — it wraps any
system that produces residuals, without touching its weights. That makes
piggy-backing the natural deployment mode. Three targets, ordered by
evidence-per-effort:

## Target 1 (recommended first): abstention governor on a small open LLM — "P1-LLM"

- **Host:** any frozen open-weights model runnable on CPU (Qwen2.5-0.5B/1.5B
  via llama.cpp or transformers).
- **Graft:** per query, compute residual diagnostics from the model's OWN
  signals (answer-consistency across k samples = D-slope analog; retrieval
  probe = D-probe; "does the context determine the answer?" permutation
  test = D-info; context-shift test = D-drift). Route: Type III → abstain
  ("unanswerable"), Type I → ask/retrieve, Type IV → re-read recent context.
- **Benchmark:** SQuAD 2.0-style QA with unanswerable items. **Coherence
  metric:** risk–coverage curve; hallucinated-answer rate at fixed coverage
  vs confidence-thresholding baselines.
- **The claim to prove:** Type-III routing reduces hallucinations at equal
  answer rate *without touching the model* — coherence improvement as a
  wrapper property. Pre-registered as P1-LLM in J56 §7.
- **Effort:** days. CPU-sufficient. Most legible to the community.

## Target 2: reservoirpy upstream PR — the substrate as a community node

- **Host:** `reservoirpy` (the maintained OSS reservoir-computing library).
- **Graft:** contribute `SubstrateReservoir`/`LiftedSubstrate` as a node type
  + the three benchmarks; the Mackey–Glass win is the motivating result.
- **The claim:** a theorem-bearing deterministic reservoir in the standard
  toolkit; the community then attacks/extends P2 for us.
- **Effort:** days. Highest permanence per effort.

## Target 3 (stretch, GPU needed): TRM fork — routed recursion

- **Host:** SamsungSAILMontreal/TinyRecursiveModels (archived; forkable).
- **Graft:** per-cycle residual diagnostics on the deep-supervision losses;
  route: continue (I) / widen features (II) / halt-abstain (III) /
  reset-context (IV) instead of fixed-depth recursion.
- **Benchmark:** Sudoku-Extreme at matched compute; coherence = accuracy per
  recursion-step spent.
- **Effort:** weeks + GPU. Highest ceiling (beating TRM's own halting on its
  own benchmark is maximal visibility).

**Sequencing:** 1 → 2 in parallel (both CPU, both days), 3 after.
Every result, win or lose, feeds J56's revision and the canon.
