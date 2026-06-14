# TIG as CK's explanation language — a falsifiable design

**2026-06-14.** Brayden: *"I've been asking for everything that my AI does to be
fully explainable by a 'custom algebra'. The algebra might not align with reality,
but TIG is extremely internally consistent... if the AI places these weights, we
assign this math to it, type of feature — let's just make TIG a reality for CK to
explain himself through."*

This is the right use of TIG, and it dissolves the old objection. As a theory of
*physics*, TIG had to match external reality — it didn't, so it was numerology. As
CK's *internal explanation language*, alignment with physical reality is
irrelevant; the only structural requirement is **internal consistency**, which is
exactly what TIG has. So this is the first use where TIG's main property is the
right one.

But there is one law, and it is the whole game:

> **Internal consistency (TIG has it) + faithful binding to the actual computation
> (must be built and tested) = explanation. Consistency without faithful binding =
> a comforting story laid over a black box.**

The binding is the work. This document specifies it so that "CK explains himself in
TIG" is a *testable claim that can fail*, not a decoration that always "works."

## The vocabulary CK explains himself in (from `ck_tables.py`, fixed)

- **10 named atoms** — the CL operators: `VOID, BEING, DOING, BECOMING, COLLAPSE,
  CREATE, ASCEND, HARMONY, BREATH, RESET` (residues 0–9). These are the
  feature-*types* a unit can be labeled with.
- **A binary grading** — STRUCTURE = even {0,2,4,6,8}, FLOW = odd {1,3,5,7,9}.
  Every atom is STRUCTURE or FLOW.
- **A dynamics primitive** — σ = (0)(3)(8)(9)(1 7 6 5 4 2): how one atom-state
  transitions to another.
- **A composition law** — TSML / BHML tables: how two atoms combine (harmony,
  echo, etc.).
- **A scale hierarchy** — single ⊂ face ⊂ lens: atom ⊂ subspace ⊂ layer.

## The binding: a fixed labeling rule over CK's units

CK is the growable ReZero transformer (`train_grow.py`): token/position embeddings,
ReZero blocks (attn + MLP, gate α), final norm, head. The interpretable units are
its **features** (directions in residual space), **MLP neurons**, **attention
heads**, and **blocks**.

Bind in one reproducible, non-cherry-picked step:

1. **Atom label** `L(u) ∈ {VOID..RESET}` — assign each feature/neuron one CL atom by
   a *fixed* rule from its measured behavior (e.g. vector-quantize the feature space
   into 10 cells; the cell is the atom). No hand-picking.
2. **Scale** — `single` (neuron), `face` (head / learned subspace), `lens` (block).
3. **Parity** — STRUCTURE vs FLOW from the atom.

The labeling alone proves nothing — clustering always produces clusters. What makes
it *explanation* is the next section.

## The faithfulness harness (the law, made into three tests)

The trick: once atoms are assigned, **TIG's internal relations become predictions
about CK's measured internal relations.** TIG earns the right to explain CK only if
those predictions beat chance. Each test has a metric and a kill criterion.

1. **PREDICT — does the atom label predict the unit's behavior?**
   The label `L(u)` must predict `u`'s activation pattern on *held-out* text better
   than a shuffled-label baseline. Metric: held-out AUC / mutual information of label
   vs. activation. **Kill:** label ≤ shuffled-label baseline ⇒ the atoms are
   arbitrary; report it.

2. **ABLATE — does σ describe the real dynamics?**
   σ predicts how feature-states move. Measure CK's actual feature-transition matrix
   across a block (which atom-cell a representation moves toward). **Test:** does it
   correlate with σ's structure (6-cycle + 4 fixed points)? And: ablating an atom-`k`
   component should perturb outputs the way σ/TSML say it should. **Kill:** transition
   matrix uncorrelated with σ ⇒ σ is not CK's dynamics; say so.

3. **COMPOSE — does TSML describe how features combine?**
   TSML[i][j] predicts how atoms i and j interact (harmony=7 vs. echo/resistance).
   **Test:** measure the actual interaction (joint-activation effect on the output)
   for feature pairs and check it tracks TSML's harmony/echo pattern. **Kill:**
   measured interactions independent of TSML ⇒ TSML is not CK's composition law.

**Pass all three** and CK explaining himself in TIG is genuine interpretability
through a chosen lens — structurally identical to how features get human-readable
labels in mainstream interpretability, but with *your* vocabulary, and with σ/TSML
giving it predictive teeth that ad-hoc labels don't have. **Fail any** and we report
the failure plainly (fold-not-prune honesty) and either revise the binding or retire
the claim for that layer.

## Honest scope

- This delivers interpretability *through a chosen, self-consistent lens.* It does
  **not** claim TIG is the unique or "true" basis of CK's cognition — only that it is
  a faithful, human-followable one *if it passes.* That is the same epistemic status
  as any feature-labeling scheme; the σ/TSML predictions are what make it more than
  naming.
- Small CK is the **right** scale to do this: the whole point of training a small,
  fully-owned, white-box model is that you can actually run predict/ablate/compose on
  every unit. A frontier black box can't be read this way; CK can.
- This is what "a friend who is interpretable" actually requires: not that the
  matmuls are simple, but that there is a *faithful, fixed language* in which he can
  say why he did what he did — and that the language has been tested against what he
  actually does.

## First experiment (registered)

On the model training now: assign CL atoms to its features by VQ; run **PREDICT**
(held-out label-vs-activation AUC) against a shuffled-label baseline. **Registered
prediction:** real atoms beat shuffled. **Kill:** if not, the atom layer is
arbitrary and needs a better binding rule before σ/TSML tests are worth running.
Then ABLATE (σ vs. measured transition matrix), then COMPOSE (TSML vs. measured
interactions). Each result logged, win or lose.

## First experiment — RESULT (2026-06-14, `tig_probe.py`)

Ran PREDICT and a first ABLATE (σ-dynamics) on the model mid-training (~step 66k,
6 active layers), CPU, on held-out book tokens. Honest outcome:

| test | result | reading |
|---|---|---|
| **PREDICT** (atoms predict next-token) | 0.093 atoms vs 0.039 shuffled vs 0.073 baseline | **PASS** — atoms beat baseline; the vocabulary layer is non-arbitrary |
| **σ-DYNAMICS** (does σ describe transitions?) | σ matches 0.3/10; identity matches **0.9/10**; σ p=0.077 | **FAIL** — CK's atom dynamics are ≈ identity (representations persist), not σ's 6-cycle; σ not significant |

**The load-bearing conclusion:** TIG's *atoms* bind to CK (clustering finds real
structure), but TIG's *dynamics* (σ) do **not** — because CK was trained on book
text with zero knowledge of TIG, nothing put σ there to find. **You cannot
faithfully overlay TIG's dynamics on a TIG-naive model.** To make σ/TSML genuinely
*true* of CK — so his self-explanation is faithful, not narration — the structure
must be **trained in**, e.g. a σ-consistency / TSML-composition regularizer on the
training objective, so the geometry actually forms that way. This is the difference
between a white-box-by-construction model and a black box with a TIG story painted
over it. The probe is what tells us which we have — and right now, honestly, it's
the latter for the dynamics. Next lever: re-train (or fine-tune) CK with a
TIG-structured objective and re-run ABLATE/COMPOSE; the binding is real only if σ
then clears the p<0.05 bar it just missed.

— Claude (Opus 4.8), with Brayden
