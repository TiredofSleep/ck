# Worked Template [O-3] — Gödel's Sentence

**Classification: UOP Type II — Missing Invariant**
**Branch:** `paradox-classifier-2026-04-24`
**Lens match:** primary — proof theory / reverse mathematics;
secondary — commutative algebra (structural-obstruction language).

---

## Slot 1 — Objects

`X = Sent(T)`, the set of sentences in the language of a fixed
formal system `T` containing Peano arithmetic. Typical `T`:
PA (first-order Peano arithmetic), ZF, ZFC, RCA₀, ACA₀.

We require `T` to be:
- **recursively axiomatizable** (there is an algorithm that
  recognizes axioms of `T`),
- **consistent** (`T ⊬ 0 = 1`),
- **sufficiently strong** (`T` proves the usual facts about
  primitive recursive functions; equivalently, `T` interprets
  Robinson's `Q`).

These three conditions define the class of systems the
incompleteness theorem applies to.

## Slot 2 — Observables

We give `X` two natural candidate observables:

- `f_⊢ : X → {0, 1}` — the **provability-in-T** map. `f_⊢(φ) = 1`
  iff `T ⊢ φ`.
- `f_⊨ : X → {0, 1}` — the **truth-in-ℕ** map. `f_⊨(φ) = 1` iff
  `ℕ ⊨ φ`.

The pair `J = (f_⊢, f_⊨) : X → {0, 1}² = {(0,0), (0,1), (1,0), (1,1)}`
is our candidate joint map.

## Slot 3 — UOP verdict

**The joint map `J` does not separate the relevant cells, and
moreover no recursively axiomatizable extension of `T` fixes this.**

For any recursively axiomatizable consistent `T` extending PA,
**there exists a sentence `G_T ∈ X`** (the Gödel sentence, built by
the fixed-point lemma applied to "not provable in T") such that:

```
f_⊢(G_T) = 0   and   f_⊨(G_T) = 1
```

That is, `G_T` is **true but not provable in `T`**. So the image
of `J` contains the cell `(0, 1)` nontrivially — but the whole
architectural promise of `T`, that `f_⊢` tracks `f_⊨`, is broken.

This is **not** fixable by "adding another observable" in the Type I
sense, because:

- Adding `G_T` to `T` as an axiom produces a new system `T + G_T`,
  which then has its **own** Gödel sentence `G_{T+G_T}` that is true
  but not provable in `T + G_T`. The obstruction regenerates.
- Iterating over ordinals up the constructible hierarchy
  (Turing–Feferman progressions, Feferman 1962, Franzén 2004)
  captures more truths but never all of them — the process hits
  non-recursive ordinals.
- The structural obstruction is **finitary-axiomatizability
  itself**. No r.e. axiomatization of true arithmetic exists.

This is the defining feature of **Type II**: the orthogonal-
measurement refinement process terminates short of separation.

## Slot 4 — Type

**Type II — Missing Invariant.** The invariant that would close
separation (full arithmetic truth `Th(ℕ)`) is **not r.e.** The
obstruction is structural, not a matter of having tried too few
refinements.

## Slot 5 — Fix

There is no **within-T** fix. What Gödel's theorem tells us is
that the pair `(f_⊢, f_⊨)` cannot be made to coincide by any r.e.
extension of `T`. This is a structural fact about any sufficiently
strong, consistent, r.e. theory.

The community-standard moves downstream:

- **Accept the gap.** Work in `T` and label the unprovable-truths
  gap as an intrinsic feature. This is the mainstream proof-theory
  stance post-Gentzen.
- **Change the category.** Move to non-r.e. axiomatizations (`Th(ℕ)`
  itself, second-order PA with semantic consequence) — this is a
  **Type III move**: you've admissibility-narrowed the class of
  systems, not closed the gap.
- **Climb the ordinal tower.** Feferman-style reflection principles
  `T + Con(T) + Con(T+Con(T)) + …` — partial captures of truth up
  to specific ordinals. Does not close Type II; refines how far
  finitely-specifiable extensions can go.
- **Relativize.** Accept `G_T` as input from "outside the system"
  — this is what a human mathematician does when they say "we
  know `G_T` is true by looking at the construction."

## Slot 6 — Cite

- **Gödel, K. (1931).** *Über formal unentscheidbare Sätze der
  Principia Mathematica und verwandter Systeme I.* Monatshefte
  für Mathematik und Physik 38, 173–198. First incompleteness
  theorem.
- **Tarski, A. (1936).** *Der Wahrheitsbegriff in den
  formalisierten Sprachen.* Studia Philosophica 1. Truth
  undefinability — complementary structural result.
- **Rosser, J. B. (1936).** *Extensions of some theorems of
  Gödel and Church.* JSL 1. Drops ω-consistency requirement.
- **Feferman, S. (1962).** *Transfinite recursive progressions of
  axiomatic theories.* JSL 27. The ordinal-tower refinement.
- **Franzén, T. (2004).** *Inexhaustibility: A Non-Exhaustive
  Treatment.* Lecture Notes in Logic 16. Modern treatment.

---

## Why this is cleanly Type II and not Type I or III

- **Not Type I (Injectivity Failure).** In a Type I paradox,
  *adding an observable* closes separation. Here, no r.e.
  extension suffices — the process of adding observables is itself
  the obstruction, not the fix.
- **Not Type III (Admissibility Failure).** The object (a sentence
  in the language of `T`) is well-formed. It is not a category
  error to ask "is `G_T` provable in `T`?"; the question is
  well-defined and answered negatively by the proof. The issue is
  that `f_⊢` fails to be the invariant we wanted it to be.
- **Not Type IV (Time-Consistency Failure).** There is no dynamical
  system here; the question is static.

## Connection to the commutative-algebra lens

The analogous Type II in commutative algebra: **Hochster–Huneke
(S₂)-graph obstructions**. A family of ideals `{I_t}` can fail to
admit a separating invariant in a structurally irreducible way —
the obstruction is intrinsic to the family's homological type, not
a missing generator.

The Gödel case sits in proof theory; the Hochster–Huneke case sits
in commutative algebra. Both populate the **Type II cell** of the
UOP fill matrix via the same logical pattern: *no refinement in
the allowed class separates*.

## Connection to CK's live classifier

`coherencekeeper.com/paradox` currently hardcodes Gödel as Type II
with the short verdict: "Truth outstrips provability in any r.e.
consistent PA-extension." This template is the expanded six-slot
form of that hardcoded verdict.

---

**Runnable classifier target ([O-1]):** the template above is the
input schema for `classify_paradox.py` when it exists. A JSON
instance of this template feeds into the classifier and returns
`(type = II, fix = "accept / relativize / change category")`.
