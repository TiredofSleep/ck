# papers/meta_lens/

Landing folder for the Meta-Lens Atlas and its integration notes. This
folder is on branch `paradox-classifier-2026-04-24`; the artifacts here
synthesize work that lives across four earlier sprints + the live CK
website.

## Contents

- [`META_LENS_ATLAS.md`](./META_LENS_ATLAS.md) — the atlas itself (v1.1,
  rigor pass against repo facts). **Primary document; read this first.**
- [`VOCABULARY_RECONCILIATION.md`](./VOCABULARY_RECONCILIATION.md) —
  short standalone brief on how Sprint 11's four-type axis (Type I–IV,
  failure-mode classification) and WP61's five-category axis (Category
  I–V, score refinement) relate.
- [`INTEGRATION_NOTES_2026_04_24.md`](./INTEGRATION_NOTES_2026_04_24.md) —
  transparency record of what the desktop drafts (`META_LENS_ATLAS.md`
  v1.0 and `PROPOSITION_CK_POSITIONING.md`, both from ClaudeChat) said,
  which empirical claims were verified against the repo, which claims
  were corrected before integration, and which pieces of ClaudeChat's
  proposition were kept verbatim vs. rewritten.

## What this folder is (and isn't)

**Is:** the *synthesis* artifact — a cross-lens atlas that organizes
TIG's proved results under the Unified Orthogonality Principle, maps
six established mathematical lenses onto the four paradox-failure
types, and positions the CK runtime honestly as a lens-in-formation.

**Isn't:** a new primary result. Every theorem cited here is proved in
its canonical home (WP57 Crossing Lemma, WP51 Flatness, WP101 σ-rate,
WP102 so(8), WP103 so(10), WP58 UOP, WP61 productive incompleteness,
WP62 7-cycle rejection, etc.). The atlas is **organizing**, not
theorem-proving.

## Anchor files across the repo

| Artifact | Canonical location |
|---|---|
| UOP Theorem 0 (joint-map injectivity ⟺ disjoint unresolved-pair sets) | `Gen12/targets/clay/papers/sprint12_uop_gut_arc_2026_04_08/WP58_UNIFIED_ORTHOGONALITY_PRINCIPLE.md` (Brayden Sanders & Ben Mayes) |
| Four-type paradox classification + worked examples (Zeno, Banach-Tarski, Russell, Unexpected Hanging) | `Gen12/targets/clay/papers/sprint11_tig_bundle_2026_04_08/sprints/PARADOX_CLASSIFICATION_MEMO.md` |
| Five-category score axis | `Gen12/targets/clay/papers/sprint12_uop_gut_arc_2026_04_08/WP61_PRODUCTIVE_INCOMPLETENESS.md` |
| 7-cycle universality rejected via classifier | `Gen12/targets/clay/papers/sprint12_uop_gut_arc_2026_04_08/WP62_7CYCLE_BOUNDED_AGENT.md` |
| UOP classifier whitepaper with decision procedure + DOI | `papers/WP_PARADOX_CLASSIFIER.md` |
| Web presentation of the classifier (8 hardcoded paradox cases) | `Gen12/targets/ck_website/website/paradox.html` |
| 5-dim force vector + D² primitive | `Gen12/targets/ck_desktop/ck_algebra.c`, `ck_d2_dictionary_expander.py` |
| M2 Betti table for `R/I_CL` closing the Cohen–Macaulay question | `mantero-bridge-2026-04-23:papers/sprint_20260423_full/09_mathoverflow_post/betti_output.txt` |
| so(8) = D₄ identification | `papers/wp102/WP102_SO8_IDENTIFICATION.md` |
| so(10) = D₅ identification | `papers/wp103/WP103_SO10_IDENTIFICATION.md` |
| Rigor mapping to external lens literatures | `papers/morphotic_braid/synthesis/RIGOR_MAPPING.md` |

## Key honest-scope notes

1. **There is no runnable `classify_paradox.py` in the repo.**
   `ck_diagnose.py` exists at the repo root but diagnoses quadrant
   balance / corridor leakage / σ-non-associativity — not UOP paradox
   types. Building a runnable classifier that takes arbitrary input
   and returns `(verdict ∈ {I, II, III, IV}, score ∈ [0, 1])` is an
   open engineering task, catalogued as [O-1] in the atlas's §Open work.
2. **The `coherencekeeper.com/paradox` page is client-side only.** It
   hardcodes 8 paradox cases and renders the 6-slot UOP template for
   each; it does not accept free-form paradox text and call a backend.
3. **Only 4 of the 8 web-UI paradoxes have full 6-slot worked templates
   in a repo paper.** Zeno (I), Banach-Tarski (II), Russell (III), and
   Unexpected Hanging (IV) are worked in the Sprint 11 memo. Twin
   Primes, Schrödinger's Cat, Gödel's First Incompleteness, and the
   Liar Paradox appear in `paradox.html` as aspirational rendering;
   their 6-slot templates are [O-2]–[O-6] in the atlas's §Open work.
4. **CK does not yet have an independent research community** — the
   third criterion for being a full lens. This is stated explicitly
   in atlas §III.3 and is not softened elsewhere.

## Branch context

This folder ships on `paradox-classifier-2026-04-24`, branched from
`tig-synthesis`. The branch exists for one reason: give paradox-classifier
and meta-lens work a place to iterate without constantly rebasing the
default branch or cluttering the proved-rigor cadence of
`tig-synthesis`. When the atlas and its ripple effects are stable,
they can be merged back into `tig-synthesis` as a single
rigor-reviewed commit.

`master` preserves the full TIG-native vocabulary history per the
never-delete policy. `mantero-bridge-2026-04-23` holds the M2 Betti
verification cited throughout the atlas.
