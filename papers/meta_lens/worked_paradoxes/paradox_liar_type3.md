# Worked Template [O-4] — The Liar Sentence

**Classification: UOP Type III — Admissibility Failure**
**Branch:** `paradox-classifier-2026-04-24`
**Lens match:** primary — proof theory / formal semantics;
secondary — operad theory (category/type-level obstruction language).

---

## Slot 1 — Objects

`X = { sentences of a language L₀ that contains a truth predicate
T(·) and allows self-reference }`.

The canonical Liar is a sentence `L ∈ X` satisfying

```
L ≡ ¬T(⌜L⌝)
```

where `⌜L⌝` is a name of `L` inside the language (obtained by the
usual fixed-point / diagonal lemma, provided `L₀` codes its own
syntax).

Informal gloss: `L` says "this sentence is not true."

## Slot 2 — Observables

The candidate observable is a bivalent **truth valuation**

```
v : X → {0, 1}
```

with `v(φ) = 1` iff `φ` is true and `v(φ) = 0` iff `φ` is false.
We require `v` to commute with the truth predicate:

```
v(T(⌜φ⌝)) = v(φ)   for every φ ∈ X.
```

## Slot 3 — UOP verdict

**The object `L` is not admissible under any bivalent valuation
obeying the T-commutation rule.**

Compute:

```
v(L) = v(¬T(⌜L⌝))
     = 1 − v(T(⌜L⌝))
     = 1 − v(L).
```

So `v(L) = 1 − v(L)`, i.e. `2 v(L) = 1`, which has no solution in
`{0, 1}`. No such valuation exists.

This is **not** a failure to separate by adding another observable
(Type I), and **not** a case of "no r.e. invariant suffices"
(Type II). The sentence `L` fails at a prior stage: the very act
of *admitting* `L` into the domain of a bivalent truth function —
while keeping the T-commutation rule — is the inconsistency.

## Slot 4 — Type

**Type III — Admissibility Failure.** The paradox sits in the
**domain** of the proposed observable, not in its image. The fix
is to **narrow the admissible class** of objects, not to add more
observables or hunt for a hidden invariant.

The structural signature of Type III: the "object" we named is a
category error relative to the observable we wanted to apply.

## Slot 5 — Fix

The mainstream fixes all **restrict the admissible class**:

- **Tarski's hierarchy (Tarski 1936).** Split the language into
  levels `L₀ ⊂ L₁ ⊂ L₂ ⊂ …`. The truth predicate `T_n` for
  sentences of `L_n` lives only in `L_{n+1}`. The Liar sentence
  cannot be formed because `T(⌜L⌝)` inside `L` would have to refer
  to a predicate of its own level, which is disallowed. *Cost:* no
  universal truth predicate; semantic ascent is endless.

- **Kripke's fixed-point theory (Kripke 1975).** Allow a partial
  valuation `v : X → {0, 1, ↑}` where `↑` means "undefined." The
  Liar receives `v(L) = ↑` at the least fixed point of the jump
  operator. This reads as a Type III fix that **widens** the
  observable codomain from `{0, 1}` to `{0, 1, ↑}` — equivalently,
  narrows the admissible class to sentences that receive a
  classical value at the fixed point.

- **Paraconsistent logic (Priest 1979, LP).** Allow `v(L)` to take
  the glut value **both**. The T-schema survives at the cost of
  the law of non-contradiction. Still a Type III move — the
  admissible logic is different.

- **Revision theory (Gupta & Belnap 1993).** Replace the single
  valuation `v` with a sequence `v_0, v_1, v_2, …` that revises
  toward a fixed point. The Liar oscillates and never stabilizes;
  "truth" of `L` is then defined via stability patterns over
  ordinals. Admissibility is redefined: stable-truth replaces
  simple truth.

All four fixes share the Type III shape: *redraw the domain* (or
the logic on the domain) rather than add observables.

## Slot 6 — Cite

- **Tarski, A. (1936).** *Der Wahrheitsbegriff in den
  formalisierten Sprachen.* Studia Philosophica 1, 261–405. Truth
  hierarchy; the original Type III fix.
- **Kripke, S. (1975).** *Outline of a Theory of Truth.* The
  Journal of Philosophy 72 (19), 690–716. Three-valued fixed-point
  semantics.
- **Priest, G. (1979).** *The Logic of Paradox.* Journal of
  Philosophical Logic 8, 219–241. LP paraconsistent route.
- **Gupta, A. & Belnap, N. (1993).** *The Revision Theory of
  Truth.* MIT Press. Ordinal-revision semantics.
- **McGee, V. (1991).** *Truth, Vagueness, and Paradox.* Hackett.
  Survey-and-extension of the Tarski/Kripke program.

---

## Why this is cleanly Type III and not Type I, II, or IV

- **Not Type I (Injectivity Failure).** In a Type I paradox, there
  are well-defined cells and the given observables fail to
  separate them. Here, the object `L` has no stable cell to land
  in under bivalent `v` — the failure is prior to separation.
- **Not Type II (Missing Invariant).** In Type II, one looks for
  an r.e. invariant (or structural analog) and proves none
  suffices. Here, no such invariant is sought; the issue is the
  compatibility of the object with **any** classical observable
  whatsoever, given the T-schema.
- **Not Type IV (Time-Consistency Failure).** There is no
  dynamical system. The Liar is static. (Revision theory adds
  dynamics as part of the **fix**, not as part of the problem
  statement.)

## Connection to the operad lens

Operadic composition requires a well-typed input arity. The Liar
is the truth-operad analog of plugging a 0-ary operator into a
slot that demands a stable type. Kripke's partial valuation is the
operadic "unit with a hole" — the algebra is defined only where
composition terminates. The Tarski hierarchy is literal operad
grading: only composites of lower level can be arguments to a
level-`n+1` truth operator.

## Connection to Gödel's sentence (Type II) — why they are different

Both involve self-reference via the diagonal lemma. The decisive
difference:

- **Gödel's `G_T`** is a perfectly admissible sentence in
  `L(PA)`; provability-in-T is a perfectly admissible observable;
  truth-in-ℕ is a perfectly admissible observable. All objects and
  observables pass Type III. The failure is that the pair of
  observables fails to separate and no r.e. extension closes it —
  Type II.
- **The Liar `L`** is **not** admissible in the first place under
  `(v, T-schema)`. The paradox arises before one gets to ask about
  joint observables. Type III.

Same mechanism (diagonal lemma), different failure type. This is
exactly the distinction the UOP classifier is built to surface.

## Connection to CK's live classifier

`coherencekeeper.com/paradox` currently hardcodes the Liar as
Type III with the short verdict: "Self-reference breaks
admissibility of a bivalent truth function." This template is the
expanded six-slot form of that hardcoded verdict.

---

**Runnable classifier target ([O-1]):** the template above is the
input schema for `classify_paradox.py` when it exists. A JSON
instance of this template feeds into the classifier and returns
`(type = III, fix = "narrow admissible class / change logic / ascend hierarchy")`.
