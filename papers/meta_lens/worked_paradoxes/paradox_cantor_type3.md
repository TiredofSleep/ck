# Worked Template [O-5] — Cantor's Naive-Set-Theoretic Paradox

**Classification: UOP Type III — Admissibility Failure**
**Branch:** `paradox-classifier-2026-04-24`
**Lens match:** primary — proof theory / set theory; secondary —
operad theory (size / arity hierarchy language).

---

## Slot 1 — Objects

Naive Cantorian set theory: the unrestricted comprehension schema

```
{ x : φ(x) }   exists as a set, for every formula φ
```

In particular, let

```
V = { x : x = x }
```

the "set of all sets," and, for any set `A`, its power set
`P(A) = { S : S ⊆ A }`.

## Slot 2 — Observables

Two observables from Cantor's theorem (Cantor 1891):

- `|·| : Sets → Cardinals`, the **cardinality** of a set.
- `P : Sets → Sets`, the **power-set** operator.

And Cantor's theorem:

```
|P(A)| > |A|   for every set A.
```

The joint-consequence observable of interest:

```
f(A) = (|A|, |P(A)|)
```

applied in particular to `A = V`.

## Slot 3 — UOP verdict

**The object `V` is not admissible under the combined
(comprehension + Cantor's theorem) regime.**

Apply Cantor's theorem to `V`:

```
|P(V)| > |V|.
```

But `P(V) ⊆ V` because every element of `P(V)` is a set, and `V`
is the set of all sets. Therefore `|P(V)| ≤ |V|`. So

```
|V| < |P(V)| ≤ |V|,
```

contradiction.

This failure is **not** fixable by an extra observable (Type I) —
cardinality and power-set are already the right observables, and
Cantor's theorem on them is true. It is **not** a missing
r.e. invariant (Type II). It is **not** two-evolution-laws
conflict (Type IV). The obstruction is that the "set" `V` —
obtained from unrestricted comprehension — is not an admissible
object for a cardinality-bearing universe in which Cantor's
theorem holds.

(The closely related Russell construction `R = { x : x ∉ x }`
diagnoses the same admissibility failure from a purely logical
angle; Cantor's version is the cardinality-arithmetic angle.)

## Slot 4 — Type

**Type III — Admissibility Failure.** The paradox is a domain
error. Naive comprehension admits "sets" that no consistent
cardinal-arithmetic can host. The fix is to **restrict
comprehension** so that `V` (and every too-large collection)
simply cannot be formed.

## Slot 5 — Fix

Every mainstream modern foundation chooses a Type III restriction:

- **Zermelo-Fraenkel (ZF / ZFC).** Replace unrestricted
  comprehension by the separation axiom
  `{ x ∈ A : φ(x) }`: a formula only carves out a subset of an
  *already admitted* set. Combined with the axiom of foundation,
  `V` cannot be formed. What would-be-`V` becomes a **proper
  class**, outside the admissible domain.
- **Von Neumann-Bernays-Gödel (NBG / MK).** Formalize the
  set/class distinction two-sortedly. `V` is an admissible class
  but not a set; only sets can be members of other collections.
  `|V|` and `P(V)` are undefined in the cardinal-arithmetic sense.
- **Type theory (Russell 1908, Martin-Löf 1984).** Stratify by
  universe level `U_0 : U_1 : U_2 : …`. "The set of all sets" in
  `U_n` lives in `U_{n+1}`, and Cantor's theorem applies within
  each level without collision.
- **Quine's NF / ML (Quine 1937).** Allow unrestricted
  comprehension but require `φ` to be *stratifiable*. `V = { x :
  x = x }` is admitted (x = x is stratifiable), but Cantor's
  theorem fails for `V` in NF — there is no bijection-to-P(V)
  argument that survives stratification. Cost: Cantor's theorem
  is sacrificed for `V`.
- **Constructive / predicative set theories (CZF, Feferman's
  predicative systems).** Further restrict which definitions can
  introduce sets. Impredicative collections like `V` are simply
  not names of anything.

The common Type III signature: every fix **narrows the admissible
class** rather than adding observables or searching for a missing
invariant.

## Slot 6 — Cite

- **Cantor, G. (1891).** *Über eine elementare Frage der
  Mannigfaltigkeitslehre.* Jahresbericht der DMV 1, 75–78. The
  diagonal argument and `|P(A)| > |A|`.
- **Russell, B. (1902).** Letter to Frege, 16 June 1902. In van
  Heijenoort (1967), *From Frege to Gödel*, Harvard. The
  companion admissibility diagnosis.
- **Zermelo, E. (1908).** *Untersuchungen über die Grundlagen der
  Mengenlehre I.* Math. Ann. 65, 261–281. Separation axiom; first
  Type III fix.
- **Fraenkel, A. A. (1922).** *Zu den Grundlagen der
  Cantor-Zermeloschen Mengenlehre.* Math. Ann. 86, 230–237.
  Replacement axiom.
- **von Neumann, J. (1925).** *Eine Axiomatisierung der
  Mengenlehre.* J. Reine Angew. Math. 154, 219–240. Set/class
  distinction.
- **Quine, W. V. O. (1937).** *New Foundations for Mathematical
  Logic.* American Math. Monthly 44, 70–80. Stratified
  comprehension.
- **Martin-Löf, P. (1984).** *Intuitionistic Type Theory.*
  Bibliopolis. Universe hierarchy.

---

## Why this is cleanly Type III and not Type I, II, or IV

- **Not Type I (Injectivity Failure).** No additional observable
  salvages `V`: it's the object itself that poisons cardinal
  arithmetic, not the observable suite.
- **Not Type II (Missing Invariant).** No r.e. invariant is being
  sought; cardinality is already well-defined on every admissible
  set. The fix doesn't look like "find a better invariant"; it
  looks like "forbid the bad object."
- **Not Type IV (Time-Consistency Failure).** Pure set theory is
  static. There are no competing evolution laws.
- **Type III is forced.** The failure is exactly at the
  admissibility stage — `V` was admitted by comprehension, and
  all Type III fixes simply disallow its admission.

## Connection to Russell's paradox (same type, different angle)

Russell's `R = { x : x ∉ x }` and Cantor's `V` are both
instantiated by unrestricted comprehension. The tension they
expose is the same — comprehension is too permissive — but they
diagnose it via different observables:

- **Russell** uses membership-in-self (`x ∈ x`) as the observable
  that splits `R`.
- **Cantor** uses power-set size (`|P(V)| vs. |V|`) as the
  observable that contradicts `V`.

Both land in Type III. Both are solved by the same family of
restrictions. The atlas lists them adjacent in the Lens 6 Type III
cell for this reason.

## Connection to the operad lens

Operadic composition requires a well-typed arity. "The set of all
sets" is the operadic analog of plugging an unbounded-arity
operator into a slot that demands finitely-stratified inputs. The
Russell / Martin-Löf universe hierarchy is literal operad grading:
a set can only contain objects of strictly lower universe level.
Quine's NF stratification is a coarser version of the same move.

## Connection to CK's live classifier

`coherencekeeper.com/paradox` does not currently render Cantor as
a separate case; it covers the Type III slot with Russell. Adding
Cantor as a separate web-UI case would be a low-cost extension now
that the six-slot template is on disk. This template is the
input form for that extension.

---

**Runnable classifier target ([O-1]):** the template above is the
input schema for `classify_paradox.py` when it exists. A JSON
instance of this template feeds into the classifier and returns
`(type = III, fix = "narrow admissible class / change logic / ascend type hierarchy")`.
