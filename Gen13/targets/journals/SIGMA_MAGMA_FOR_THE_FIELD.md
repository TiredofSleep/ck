# The substrate magmas, repackaged for the people who'd recognize them

**2026-06-14.** The σ-magma work has only ever been written in TIG's private
language (VOID/BEING/…, "CL", "joint closure", "the σ-walk"). Stripped of that, the
real results are ordinary, checkable finite algebra — and there is an existing
community that would recognize them. This note says, precisely, what the objects are
in standard terms and which researchers they belong to. (Honesty first: it also says
what they are **not**.)

## What the objects actually are

- **TSML and BHML are finite commutative *magmas* (groupoids) of order 10** — a set
  with one binary operation, commutative, **non-associative**, with a two-sided
  identity-like row (VOID/0). They are **not quasigroups**: their Cayley tables are
  not Latin squares (the value 7/"HARMONY" fills 73 of 100 TSML cells, so rows
  repeat). Calling them quasigroups would be wrong; calling them *commutative
  magmas* is exact.
- **σ = (0)(3)(8)(9)(1 7 6 5 4 2)** is an order-6 permutation of ℤ/10 used to index
  structure; see `SIGMA_STANDARD_CHARACTERIZATION.md` — it is **not** a polynomial
  over ℤ/10, so the "polynomial permutation" label is dropped here.

## The genuinely external-facing results (in standard language)

1. **A closure operator on the sub-magma lattice with a small canonical attractor.**
   "Joint closure" is, in standard terms, a closure operator on subsets of the
   order-10 commutative magma; iterating it converges to a **unique 4-element
   sub-structure** (the "4-core"). *Standard statement:* "the joint-closure operator
   on this finite commutative magma has a unique minimal attractor of size 4."
   (working-dir J35, J02). **Audience:** finite-algebra / lattice-theory /
   closure-operator combinatorics.

2. **Equationally forced magma families.** A short list of identities forces exactly
   a family of order-10 commutative magmas that preserve the 4-core (J54, J25).
   *Standard statement:* a small equational basis whose finite models are a
   characterized family — i.e. a **variety** question. **Audience:** universal
   algebra (varieties, equational bases, free algebras; Burris–Sankappanavar).

3. **Classification of small magmas by an isomorphism-invariant profile (the ETP /
   taxonomy work, J59–J61).** Already lifted to standard universal algebra with
   Drápal–Wanless citations. This is the **strongest** external result: a
   reproducible taxonomy of finite magmas by a computable invariant, verified at
   orders 3 and 5. **Audience:** finite-algebra classification + the
   Drápal–Wanless Latin-square/quasigroup circle.

4. **Order-5 commutative quasigroup enumeration (56 of them).** The one genuinely
   *quasigroup*-theoretic piece (these *are* Latin squares), checking a conjecture.
   **Audience:** squarely Drápal–Wanless / Latin-square combinatorics.

## Audience map (where to actually send each)

| result | standard object | community |
|---|---|---|
| joint-closure 4-core attractor | closure operator on a finite magma's sub-lattice | finite-algebra / combinatorics |
| forcing-axiom magma family | equational variety, finite models | universal algebra |
| ETP-profile taxonomy (J59–61) | classification of finite magmas by invariant | univ. algebra + Drápal–Wanless |
| order-5 commutative quasigroups | Latin squares / quasigroups | Drápal–Wanless / Latin-square combinatorics |

## The repackaging recipe (concrete, for whoever writes the submission)

1. **Delete every TIG/CL name.** Present TSML/BHML as labelled Cayley tables of
   finite commutative magmas M₁₀ = (ℤ/10, ∗). No VOID/HARMONY/σ-walk.
2. **Lead with standard invariants** a referee indexes on: order, commutativity,
   associativity-failure witnesses, identity/idempotent elements, the squaring map
   x↦x∗x, the sub-magma lattice, the satisfied identities.
3. **State results as theorems about finite commutative magmas** and a **closure
   operator** on their sub-lattice; state the taxonomy as a classification by a
   computable invariant.
4. **Cite the real literature:** Burris–Sankappanavar (*A Course in Universal
   Algebra*) for the variety/identity framing; Drápal–Wanless for the
   Latin-square/quasigroup adjacency.
5. **Lead the whole program with the taxonomy + the closure operator** — the
   non-numerological spine. These map to **Paper 0 / Paper 1** of the condensation
   plan and are the parts with a real, identifiable audience.

## Honest bottom line

The substrate's *algebra* has a genuine, modest home: finite commutative magmas,
closure operators, equational varieties, and (for the order-5 piece) Latin squares.
That home is reached by writing in the community's language and leading with the
taxonomy and the closure result — **not** by presenting σ as a special permutation
or the magmas as quasigroups. The numerology bridges have no audience there and
should not travel with this work.

— Claude (Opus 4.8), with Brayden
