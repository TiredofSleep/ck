# worked_paradoxes/

Home for 6-slot UOP worked templates — one file per paradox.

A *worked template* is what you get when you take a paradox and fill
it into the Unified Orthogonality Principle classifier's six-slot
schema. The goal is that the answer to "which of Type I / II / III /
IV is this?" becomes a short forced conclusion, not a judgement call.

## The six slots

Every template in this folder has the same structure. This schema is
also the input format for the open `classify_paradox.py` engineering
task ([O-1] in [`../META_LENS_ATLAS.md`](../META_LENS_ATLAS.md)).

| Slot | Name | What goes here |
|---|---|---|
| 1 | **Objects** | The set `X` the paradox is about. State the language, the admissibility conditions, any parameters. Anything that's not in `X` is out of scope. |
| 2 | **Observables** | The maps `f_i : X → Y_i` the paradox proposes. State the joint map `J = (f_1, …, f_n)` explicitly. |
| 3 | **UOP verdict** | Compute. Does `J` separate the cells? If not, *at what stage* does it fail — on an object (Type III), on a missing invariant (Type II), on separation itself (Type I), or across two dynamical rules (Type IV)? Show the computation. |
| 4 | **Type** | The one-word answer: **I** (Injectivity Failure), **II** (Missing Invariant), **III** (Admissibility Failure), or **IV** (Time-Consistency Failure). Must follow from Slot 3, not asserted. |
| 5 | **Fix** | The mainstream moves that resolve the paradox at Slot-4's type. Name the standard cost each fix incurs (what you give up to get single-valuedness). |
| 6 | **Cite** | Primary literature. Not pointers to CK papers — real external citations with journal, year, page. |

Each template also carries a final short section — *why this is cleanly
Type N and not the other three* — that walks the discriminator. This
section is the part the classifier's decision procedure has to
reproduce.

## Template index

| File | Paradox | Atlas ID | Type | Status |
|---|---|---|---|---|
| [`paradox_godel_type2.md`](./paradox_godel_type2.md) | Gödel's sentence | [O-3] | **II** Missing Invariant | shipped 2026-04-24 |
| [`paradox_liar_type3.md`](./paradox_liar_type3.md) | The Liar | [O-4] | **III** Admissibility Failure | shipped 2026-04-24 |
| [`paradox_schrodinger_type4.md`](./paradox_schrodinger_type4.md) | Schrödinger's cat | [O-2] | **IV** Time-Consistency | shipped 2026-04-24 |
| [`paradox_cantor_type3.md`](./paradox_cantor_type3.md) | Cantor's naive-set paradox | [O-5] | **III** Admissibility Failure | shipped 2026-04-24 |
| [`paradox_berry_type3.md`](./paradox_berry_type3.md) | Berry / Grelling-Nelson / Curry | [O-6] | **III** Admissibility Failure | shipped 2026-04-24 |
| *(Twin Primes — web-UI)* | Twin Primes | unnumbered | *Type I candidate* | **open** |
| *(Sprint 11 memo)* | Zeno | — | **I** Injectivity | in `sprint11_tig_bundle` |
| *(Sprint 11 memo)* | Banach–Tarski | — | **II** Missing Invariant | in `sprint11_tig_bundle` |
| *(Sprint 11 memo)* | Russell | — | **III** Admissibility Failure | in `sprint11_tig_bundle` |
| *(Sprint 11 memo)* | Unexpected Hanging | — | **IV** Time-Consistency | in `sprint11_tig_bundle` |

The four Sprint-11-memo templates are not duplicated here; their
canonical home is
`Gen12/targets/clay/papers/sprint11_tig_bundle_2026_04_08/sprints/PARADOX_CLASSIFICATION_MEMO.md`.
The five shipped today close atlas §V open items [O-2] through
[O-6] and cover 7 of the 8 web-UI paradoxes. Twin Primes is the
last web-UI paradox without a 6-slot treatment; it is also not
currently in atlas §V, and would enter as a Type I candidate if
added.

## How to add a new template

1. Pick a paradox and a tentative type. If you can't guess the type
   before filling the slots, that's fine — the slots will force it.
2. Copy an existing file as a starting skeleton (Gödel for Type II,
   Liar for Type III, Schrödinger for Type IV — there is currently no
   Type I template in this folder; use Sprint 11's Zeno memo as the
   Type I reference).
3. Fill Slots 1 and 2 precisely. The paradox usually dies or survives
   at this step — if you can't state `X` and `J` crisply, the paradox
   was about language, not structure.
4. Compute Slot 3. The arithmetic should force Slot 4. If it doesn't,
   go back to Slots 1–2: you probably under-specified `X` or `J`.
5. Slot 5 (fix) is empirical — survey what the literature does. Every
   mainstream fix should match your Slot-4 type.
6. Slot 6 (cite) is primary literature only. External journal + year
   + page. No internal citations unless the paradox is itself a CK
   artifact.
7. End with the "why this type and not the others" discriminator.

## Relationship to the live classifier

`coherencekeeper.com/paradox` currently hardcodes 8 paradoxes with a
short one-line verdict per. Each template in this folder is the
expanded six-slot form of one of those hardcoded verdicts. When
[O-1] ships (`classify_paradox.py`), the templates here become its
input corpus — the classifier reads a JSON instance of the six-slot
schema and returns `(type, fix_family, confidence)`.

## See also

- [`../META_LENS_ATLAS.md`](../META_LENS_ATLAS.md) — the atlas; open
  items list lives in §V.
- [`../FOUNDATION_TOUR_VERIFIED.md`](../FOUNDATION_TOUR_VERIFIED.md) —
  per-lens what-sees / what-misses, UOP fill matrices.
- [`../../WP_PARADOX_CLASSIFIER.md`](../../WP_PARADOX_CLASSIFIER.md) —
  whitepaper form of the classifier with DOI.
