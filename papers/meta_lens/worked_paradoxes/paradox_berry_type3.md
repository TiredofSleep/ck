# Worked Template [O-6] — Berry / Grelling-Nelson / Curry Cluster

**Classification: UOP Type III — Admissibility Failure**
**Branch:** `paradox-classifier-2026-04-24`
**Lens match:** primary — proof theory / formal semantics;
secondary — operad theory (definability / type stratification).

This template treats three closely related paradoxes together
because they share the Type III structure and the same family of
fixes. Each gets its own Slot 1–3; the shared slots 4–6 follow.

---

## Slot 1 — Objects

**Berry (1906, via Russell).**
`X_Berry = ` positive integers `n ∈ N`, together with English-
language noun phrases of the form "the smallest positive integer
not definable in under twenty words."

**Grelling-Nelson (1908).**
`X_GN = ` adjectives of English. An adjective is *autological* if
it applies to itself ("polysyllabic" is polysyllabic), and
*heterological* otherwise ("monosyllabic" is not monosyllabic).

**Curry (1942).**
`X_Curry = ` sentences of a logic with a truth predicate that
satisfies the conditional form of the T-schema,
`T(⌜φ⌝) → φ`, and which allows self-reference. A Curry sentence
is

```
C ≡ T(⌜C⌝) → ⊥
```

i.e., "if this sentence is true, then contradiction." (`⊥` may be
replaced by any target sentence `ψ` — the paradox lets us derive
an arbitrary `ψ` from a trivial schema.)

## Slot 2 — Observables

**Berry.** Definability observable
`Def : X_Berry × Strings → {0, 1}`, `Def(n, s) = 1` iff string `s`
is a definition of `n`. Word-count observable
`|·| : Strings → N`. Combined: "is `n` definable by a string of
fewer than 20 words?"

**Grelling-Nelson.** Self-application observable
`σ : X_GN → {0, 1}`, `σ(w) = 1` iff adjective `w` applies to
itself.

**Curry.** Truth valuation `v : Sentences → {0, 1}` compatible
with the conditional T-schema.

## Slot 3 — UOP verdict

In each case, a concrete object of the proposed domain proves the
domain is not admissible under the regime defined by the
observables.

**Berry.** Let `B = "the smallest positive integer not definable
in under twenty words."` This string is itself under 20 words (13
words, in fact). By construction `B` defines an integer `n_B`.
But `n_B` is the smallest integer *not* definable in under 20
words — contradicted by its own definition in under 20 words.
Contradiction. Therefore the informal "definable in under 20
words" is not an admissible observable on `N` — it presupposes a
closed, precise definability relation, which informal English
does not supply.

**Grelling-Nelson.** Consider the adjective "heterological."
Is it autological or heterological?
- If autological, it applies to itself, hence it *is*
  heterological. Contradiction.
- If heterological, it does not apply to itself, hence it is
  autological. Contradiction.

Same arithmetic as the Liar. The defect is the admissibility of
"heterological" as a uniformly-defined adjective on all adjectives
— it is not.

**Curry.** The paradox derives any target `ψ`:

```
1. C ≡ T(⌜C⌝) → ψ           (definition, fixed-point)
2. Assume T(⌜C⌝).            (for conditional proof)
3. From T-schema: C.          (T(⌜C⌝) → C)
4. From 2, 3, def of C: ψ.    (detachment)
5. From 2 ⊢ ψ: T(⌜C⌝) → ψ.   (discharge)
6. That is: C.                (def of C)
7. Therefore T(⌜C⌝).          (T-schema, reverse)
8. From 7, 5: ψ.              (MP)
```

`ψ` was arbitrary. Therefore the system is trivial. As with Liar
and Grelling, the failure is admissibility: the Curry sentence `C`
is not admissible under the conditional T-schema plus contraction.

All three failures are at **Slot 1** (the object is ill-formed
under the stated admissibility rules). They are **not** Type I
(no observable refinement fixes them), **not** Type II (no missing
r.e. invariant is being sought), **not** Type IV (no dynamics).

## Slot 4 — Type

**Type III — Admissibility Failure.** In each paradox, the
offending object (`B`, "heterological," `C`) is constructed by
a naive principle (definability-within-English, uniform
predicate-formation, contraction-on-self-reference) that admits
more than the ambient semantic apparatus can coherently carry.

The three paradoxes cluster because they all instantiate the same
abstract shape: **self-applicable predicate + no stratification
= admissibility overflow.**

## Slot 5 — Fix

Same family of Type III fixes as Liar + Cantor: restrict the
admissible class.

- **Berry.** Formalize "definable." Once "definable in language
  `L` with bound `k`" is a precise predicate of a formal
  metalanguage, Berry's `B` can no longer be stated in `L`; it
  lives in the metalanguage. Tarski (1936) hierarchy. Specific
  formalization: finite-word definability relative to a fixed
  formal system `T` (Chaitin 1974: the minimum size of a
  `T`-description defines incompressibility, which is itself
  non-computable — the "informal English" admissibility has been
  replaced by a precise, weaker predicate).
- **Grelling-Nelson.** Either (i) stratify the adjective lexicon
  so that "autological" is at a higher type than the adjectives
  it can apply to (Russell 1908 simple theory of types), or (ii)
  accept gappy valuations (Kripke 1975 partial-truth
  construction): "heterological" receives no stable truth value
  when applied to itself.
- **Curry.** Drop contraction (substructural logics: linear
  logic, affine logic, Girard 1987; Mares-Meyer relevant logic);
  or drop the conditional T-schema; or ascend a Tarski hierarchy
  so that `T(⌜C⌝)` is at a higher level than `C`. Each fix
  **narrows the admissible class** of inferences or objects.

## Slot 6 — Cite

- **Russell, B. (1906).** *Les paradoxes de la logique.* Revue de
  métaphysique et de morale 14, 627–650. Introduces Berry (attributed to G. G. Berry).
- **Grelling, K. & Nelson, L. (1908).** *Bemerkungen zu den
  Paradoxien von Russell und Burali-Forti.* Abh. Fries'schen
  Schule, NF 2, 301–334. Original heterological paradox.
- **Curry, H. B. (1942).** *The Inconsistency of Certain Formal
  Logics.* JSL 7, 115–117. Original Curry paradox.
- **Russell, B. (1908).** *Mathematical Logic as Based on the
  Theory of Types.* American Journal of Mathematics 30, 222–262.
  Type hierarchy.
- **Tarski, A. (1936).** *Der Wahrheitsbegriff in den
  formalisierten Sprachen.* Studia Philosophica 1. Hierarchy for
  all three of these.
- **Kripke, S. (1975).** *Outline of a Theory of Truth.* JPhil 72,
  690–716. Partial-valuation fix.
- **Chaitin, G. J. (1974).** *Information-Theoretic Limitations
  of Formal Systems.* JACM 21, 403–424. Formalization of
  Berry-like definability.
- **Girard, J.-Y. (1987).** *Linear Logic.* Theoretical Computer
  Science 50, 1–101. Substructural fix for Curry.
- **Meyer, R. K. & Routley, R. (1977).** *Extensional reduction.*
  Relevance Logic and Entailment, Ridgeview. Relevant-logic fix
  for Curry.

---

## Why this is cleanly Type III and not Type I, II, or IV

- **Not Type I (Injectivity Failure).** Adding more observables
  doesn't rescue `B`, "heterological," or `C`. The observables on
  offer are fine; the objects are the problem.
- **Not Type II (Missing Invariant).** No r.e. invariant is being
  hunted. The formalizations don't ask "what invariant did we
  miss?"; they ask "which objects should we refuse to admit?"
- **Not Type IV (Time-Consistency Failure).** Static paradoxes.
  No evolution laws in conflict. (Revision-theoretic treatments
  add dynamics as part of the **fix**, not part of the problem —
  same move as with the Liar.)
- **Type III is forced.** Every fix is "restrict what you admit,"
  whether that means formalizing definability (Berry), stratifying
  predicates (Grelling), or dropping structural rules (Curry).

## Cluster note: why three-in-one

Berry, Grelling-Nelson, and Curry share the same abstract
structure: **a self-applicable naming / definability / truth
device + a naive universal principle (informal definability /
uniform predication / conditional T-schema) = admissibility
failure.** The cluster lands in a single template because
separating them would triplicate the Slot 5 literature with no
marginal clarity: each is mentioned individually, the fix family
is identical.

If a future treatment wants per-paradox precision, split this
file into
`paradox_berry_type3.md`, `paradox_grelling_type3.md`,
`paradox_curry_type3.md` — the Slot 1/2/3 blocks above already
factor cleanly.

## Connection to Liar and Cantor (adjacent Type III cases)

- **Liar:** bivalent truth + self-reference.
- **Cantor:** unrestricted comprehension + Cantor's theorem.
- **Berry / Grelling / Curry:** definability / predication /
  conditional T-schema + self-application.

All five instantiate the same deep admissibility failure: a naive
semantic closure principle combined with self-reference. The
Russell-Tarski hierarchy is the single meta-move that resolves all
five by stratification; substructural logic is the orthogonal
meta-move that resolves the Curry sub-family.

## Connection to CK's live classifier

`coherencekeeper.com/paradox` does not currently render Berry,
Grelling-Nelson, or Curry as separate web-UI cases. The six-slot
template is now on disk; adding them as UI extensions is
low-cost. This template is the input form for that extension.

---

**Runnable classifier target ([O-1]):** the template above is the
input schema for `classify_paradox.py`. A JSON instance of this
template (with `slot3_failure_stage = "admissibility"`) feeds into
the classifier and returns
`(type = III, fix = "narrow admissible class / change logic / ascend type hierarchy")`.
