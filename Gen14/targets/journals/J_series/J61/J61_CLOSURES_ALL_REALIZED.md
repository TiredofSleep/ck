# All eight of J61's closures have finite type specimens

**2026-09-23 · Brayden Ross Sanders, with Claude.** This follows
[the Theorem 5 correction](J61_THEOREM5_IS_FALSE.md). Reproduce everything with
[`verify_j61_closures.py`](verify_j61_closures.py) (numpy only; about two minutes, or three with
`--minimality`).

J61 §6 lists the eight implication-closures of size 14 in the catalog of Tao's Equational Theories
Project (ETP). It "proves" that one of them has no finite type specimen (Theorem 5), labels a second
one a "fossil variety" with no specimen, and conjectures the same for the rest. A **type specimen** of a
closure is a finite magma whose ETP profile — the set of the catalog's 4,694 laws that it satisfies — is
exactly that closure.

**Every one of the eight has a finite type specimen.**

## The result

| closure | anchor law | J61 said | specimen | smallest order |
|---|---|---|---|---|
| C1 | #40 x◇x = y◇y | realized | 3 elements | 3 |
| C2 | #43 x◇y = y◇x | realized | 3 elements | 3 |
| C3 | #1312 x = y◇(((y◇x)◇x)◇x) | open | 32 elements | open: 7 to 32 |
| C4 | #2241 x = (x◇(x◇(x◇y)))◇y | open | the mirror image of C3's | as C3 |
| C5 | #4295 x◇(x◇y) = y◇(z◇x) | none exists (Theorem 5) | 6 elements | 6 |
| C6 | #4303 x◇(x◇y) = z◇(y◇x) | open | 5 elements | 5 |
| C7 | #4610 (x◇x)◇y = (y◇z)◇x | open | the mirror image of C5's | 6 |
| C8 | #4637 (x◇y)◇x = (y◇x)◇z | **"fossil variety"** | the mirror image of C6's | 5 |

J61's conjecture that C3–C8 have no finite type specimen is false for all six of them.

## The mirror does half the work

Read a table the other way round, x∗y := y◇x, and you get the *opposite* magma. This is a flip, and
it turns every law into its mirror image: (x◇y)◇z becomes z◇(y◇x). Of the 4,694 laws, 84 are their own
mirror image and the other 4,610 pair off.

J61's eight closures fall the same way. C1 and C2 are their own mirror images. C3 and C4, C5 and C7,
and C6 and C8 are mirror pairs. So the transpose of a specimen for one side of a pair is a specimen for
the other side, and C4, C7 and C8 come for free.

In this program's language, the mirror is a coin: two sides and an edge. It settles nothing by itself.
What it does is show which questions are really the same question.

## The specimens

**C1 (all squares equal).** Every square is 0:

```
◇ | 0 1 2
--+------
0 | 0 0 1
1 | 1 0 2
2 | 1 1 0
```

**C2 (commutativity).** The table is symmetric:

```
◇ | 0 1 2
--+------
0 | 0 0 1
1 | 0 2 0
2 | 1 0 0
```

**C6.** Its transpose is the specimen for C8:

```
◇ | 0 1 2 3 4
--+----------
0 | 0 0 0 1 1
1 | 0 0 0 0 1
2 | 0 0 4 0 1
3 | 0 0 0 0 1
4 | 0 0 0 0 1
```

**C5.** This is the 6-element specimen from [the Theorem 5 correction](J61_THEOREM5_IS_FALSE.md). Its
transpose is the specimen for C7.

**C3.** This one is a product of two models of #1312:

- **The first factor is the "affine mean" over the field with eight elements.** In that field
  t³ = t² + 1, and the operation is x◇y = t·x + (1+t)·y. The two weights add up to 1, so x◇y is a
  weighted average of x and y. Up to renaming, this is the ETP's own 8-element example showing that
  #1312 does not imply x = y◇(y◇x).
- **The second factor is a 4-element model:**

  ```
  ◇ | 0 1 2 3
  --+--------
  0 | 0 1 3 2
  1 | 1 0 3 2
  2 | 0 1 3 2
  3 | 1 0 3 2
  ```

- **Why the product works.** The affine mean satisfies 87 laws beyond C3, and the small model violates
  every one of them. A law holds in a product exactly when it holds in both factors. So the 32-element
  product satisfies C3 and nothing else.

The transpose of the product is the specimen for C4.

## Why these laws follow, and nothing else does

For C1, C2, C5 and C6, short arguments show that every law of the closure follows from its anchor:

- **#40 (C1): all squares are equal.** Replace every square by one constant. Both sides of each C1
  law then become the same.
- **#43 (C2): factors can be swapped.** Put the two factors of every product in a fixed order. Both
  sides of each C2 law then become the same.
- **#4295 (C5).** Setting z = y gives x◇(x◇y) = y◇(y◇x), and renaming gives a◇(v◇w) = w◇(w◇a).
  Together they say that a◇(v◇w) depends only on the unordered pair {a, w}. Each C5 law equates two
  such products with the same pair.
- **#4303 (C6).** In the same way, a◇(v◇w) depends only on the unordered pair {v, w}.
- **#1312 (C3).** The ETP proves, in Lean, that #1312 implies the other 12 non-trivial laws of C3.

Mirroring carries each of these arguments over to C4, C7 and C8.

The other direction comes from the specimens: each one violates every law outside its closure, so
nothing else follows from any of the anchors. As a cross-check, the ETP's Equation Explorer lists
exactly these implications for #1312, #4295 and #4303 (checked 2026-09-23).

## Why C3 needs so many elements

- **In a finite model of #1312, every row of the table is a permutation.** The law writes each x as
  y◇(something), so left multiplication by y reaches every element. On a finite set, that makes it
  one-to-one as well.
- **Up to five elements, every model also satisfies x = y◇(y◇x):** each row is its own inverse.
  #1312 does not imply that law, but only a larger model can show it.
- **At six elements, ten models (up to renaming) break it.** That is smaller than the ETP's own
  8-element example. Each of the ten still satisfies at least 29 laws, though, so none is a specimen.
- **The smallest possible specimen therefore has between 7 and 32 elements.** Its exact size is open.

## Two more claims in J61, corrected

- **J61 says "At order 3, no magma realizes Family C exactly".** Family C is C2, the
  commutativity closure. J61 also says that the σ-magma, at order 10, is "the smallest-known Family C
  realizer". Both are false:
  - 120 of the 729 commutative magmas of order 3 realize Family C exactly;
  - so did all 10 of 10 random commutative magmas of order 10.

  Realizing Family C exactly is simply what a commutative table does, unless something special stops
  it. So the σ-magma's "Family C" status is generic, as the census already found its rigidity to be.
- **J61 says Family C realization "requires non-linear σ_n constructions".** It requires no special
  construction at all; see above.

## How it was checked

- **The catalog.** It was rebuilt from its definition, as in the Theorem 5 correction, and checked
  against eleven anchor laws and against J61's own profile counts.
- **The searches.** They use propagation and the least-number heuristic, and they were checked
  against brute force:
  - C6 at order 3, over all 19,683 magmas;
  - C3 at orders 2–4.
- **The specimens.** Each one was checked law by law. The 32-element C3 specimen was checked on the
  product itself: every C3 law at every assignment, and every other law at an assignment where it
  fails.

## What this is, and is not

These are small, correct results. They correct J61's account of its own eight closures:

- J61's two "fossil variety" claims (C5, as its Theorem 5, and C8, in its table) are false, and so
  is its conjecture that none of C3–C8 has a specimen.
- Every closure it listed has a finite type specimen.
- The smallest specimen size is now known for six of the eight.
- What remains open is the smallest specimen for C3 and C4: between 7 and 32 elements.

The question of which ETP closures have finite type specimens is J61's framing. The ETP itself settles
implications between laws, and this note uses nothing from the ETP beyond the catalog's definition and
its explorer's implication lists.
