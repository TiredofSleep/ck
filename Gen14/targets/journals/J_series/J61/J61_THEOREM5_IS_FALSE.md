# J61's Theorem 5 is false: equation 4295 has a finite type specimen, of order 6

**2026-09-23 · Brayden Ross Sanders, with Claude.** This settles the one case the drift census left
open. Reproduce everything with [`verify_4295_type_specimen.py`](verify_4295_type_specimen.py) (numpy
only; about a minute, or six with `--minimality`).

## The claim

J61 ("Type Specimens in the ETP-Restricted Variety Lattice") states as its Theorem 5, the
"Fossil-Variety Theorem":

> *Equation 4295 of Tao's Equational Theories Project, x◇(x◇y) = y◇(z◇x), admits no finite type
> specimen in the ETP catalog: every finite magma satisfying equation 4295 has ETP profile ≥ 261.*

A **type specimen** is a magma whose ETP profile — the set of the catalog's 4,694 laws it satisfies —
is exactly {1} plus the implication-closure of the equation.

## What is true

1. **The closure of #4295 has exactly 14 laws:** #1, 4269, 4284, 4287, 4290, 4293, 4295, 4316, 4340,
   4343, 4345, 4360, 4369 and 4371. This agrees with J61's size-14 closure C5, whose anchors 4295,
   4345 and 4371 are among these.
   - All 14 follow from #4295. Renaming its variables gives x◇(y◇z) = z◇(z◇x). Setting z = y gives
     x◇(x◇y) = y◇(y◇x). So every right-nested product u◇(v◇w) depends only on the unordered pair
     {u, w}, and each of the 13 non-trivial laws equates two right-nested products with the same pair.
   - No other law follows, because the specimen below violates every other law.
2. **A type specimen exists, of order 6:**

   ```
   ◇ | 0 1 2 3 4 5
   --+------------
   0 | 0 0 0 0 0 1
   1 | 0 0 0 0 0 1
   2 | 0 0 0 0 0 2
   3 | 0 0 0 0 0 2
   4 | 0 0 0 0 0 2
   5 | 0 3 3 0 3 4
   ```

   It satisfies #4295, and its ETP profile is exactly the 14 laws above. **Theorem 5 is false.**
3. **Six is the smallest possible order.** Every model of #4295 of orders 2–5 was enumerated, up to
   isomorphism:

   | order | models (up to isomorphism) | smallest profile |
   |---|---|---|
   | 2 | 1 | 1556 |
   | 3 | 8 | 122 |
   | 4 | 165 | 76 |
   | 5 | 20,304 | 16 |

   None reaches 14.
4. **The lower bound "≥ 261" is false already at order 3.** The model [[0,0,0],[0,0,1],[0,0,1]]
   satisfies #4295 and has profile 122.

## Where the proof went wrong, and how the specimen was found

- **The flawed step.** J61's proof began by claiming that every model is a projection of one kind or
  another. That is false: 36 of the 45 order-3 models depend on both arguments.
- **The census.** It flagged this, and suggested the test that was run here: enumerate the models,
  order by order.
- **The shortcut.** Any model in which all right-nested products are equal satisfies all 112 laws of
  the form u◇(v◇w) = u′◇(v′◇w′), so its profile is at least 113. Small profiles therefore occur only
  among the rare models where those products differ: 3 of 165 classes at order 4, and 145 of 20,304 at
  order 5.
- **Products.** Among those, profile-16 models at order 5 satisfy *different* pairs of extra laws. A
  law holds in a direct product exactly when it holds in both factors, so multiplying an order-3 model
  by an order-5 model with disjoint extras gives a 15-element model whose profile is exactly the
  closure.
- **The order-6 specimen.** Its 6-element sub-magma on the elements {0, 1, 2, 3, 7, 14} of that product
  keeps the same profile. That is the specimen above.

## How it was checked

No external data was used.
- **The catalog.** The ETP catalog was rebuilt from its definition: laws with at most four
  operations, up to renaming and swapping sides, numbered in ETP order. The rebuild was checked
  against known anchor laws:
  - #14, x = y◇(x◇y);
  - #43, commutativity;
  - #4512, associativity;
  - #4295 itself.
- **J61's own numbers.** The rebuild was also checked against six profile counts that J61 had
  computed on the real catalog (1556, 1214, 32, 32, 294 and 261). All match.
- **The search.** The model search uses propagation and the least-number heuristic. At orders 3 and 4
  it reproduces a plain exhaustive search exactly.

## What this is, and is not

It is a small, correct result: a counterexample to a claim in the author's own paper, with the
smallest possible order. The type-specimen question — which implication-closures of the ETP catalog
are realized exactly by a finite magma — is J61's own framing. The ETP project itself resolved
implications between laws, and this note does not claim anything about its data beyond the
catalog's definition. J61's other "fossil variety" claim, for closure C8 (#4637, #4659, #4678),
should be tested the same way before anyone relies on it.
