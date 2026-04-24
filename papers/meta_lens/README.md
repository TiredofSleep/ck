# papers/meta_lens/

Landing folder for the Meta-Lens Atlas and its integration notes. This
folder is on branch `paradox-classifier-2026-04-24`; the artifacts here
synthesize work that lives across four earlier sprints + the live CK
website.

## Contents

- [`META_LENS_ATLAS.md`](./META_LENS_ATLAS.md) — the atlas itself (v1.1,
  rigor pass against repo facts). **Primary document; read this first.**
- [`FOUNDATION_TOUR_VERIFIED.md`](./FOUNDATION_TOUR_VERIFIED.md) —
  rigor-first rewrite of ClaudeChat's 7-lens foundation tour
  (2026-04-24). Every affiliation WebSearch-verified; every runtime
  claim grepped. Unverified items flagged; speculative bridges tagged
  `SPECULATIVE`. Contains what-sees / what-misses tables, UOP fill
  matrices per lens, two honest orderings for outreach, and a
  "claims that did NOT verify" section.
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
- [`worked_paradoxes/`](./worked_paradoxes/) — 6-slot UOP template
  home. Currently contains Gödel (Type II), Liar (Type III), and
  Schrödinger's cat (Type IV). See
  [`worked_paradoxes/README.md`](./worked_paradoxes/README.md) for
  the slot schema and per-template index.
- [`correspondence/`](./correspondence/) — preserved ClaudeChat
  correspondence with per-claim audit trail. Separated from the
  rigor-clean `FOUNDATION_TOUR_VERIFIED.md` so provenance is legible
  without contaminating the ship-ready document.

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

1. **Runnable classifier now exists as `classify_paradox.py`**
   (shipped 2026-04-24, closing atlas open item [O-1]). It reads
   the six-slot markdown templates in `worked_paradoxes/` and
   either returns a stored verdict for a shipped template
   (`--template godel`) or classifies a JSON 6-slot instance
   (`--json my.json`). It is rule-based, not an LLM — Slot 3's
   user-provided failure stage forces Slot 4's type. It does
   **not** parse natural-language paradox statements; that NLP
   step is deliberately left open. `ck_diagnose.py` at the repo
   root is a separate tool that diagnoses quadrant balance /
   corridor leakage / σ-non-associativity and is not the paradox
   classifier.
2. **The `coherencekeeper.com/paradox` page is client-side only.** It
   hardcodes 8 paradox cases and renders the 6-slot UOP template for
   each; it does not accept free-form paradox text and call a backend.
3. **7 of the 8 web-UI paradoxes now have full 6-slot worked templates
   in a repo paper** (updated 2026-04-24). Zeno (I), Banach-Tarski (II),
   Russell (III), and Unexpected Hanging (IV) are worked in the Sprint 11
   memo. Schrödinger's Cat (IV), Gödel's First Incompleteness (II), and
   the Liar Paradox (III) shipped today in
   [`worked_paradoxes/`](./worked_paradoxes/) — these correspond to
   atlas open items [O-2], [O-3], and [O-4] respectively. Atlas
   open items [O-5] (Cantor, Type III) and [O-6]
   (Berry / Grelling-Nelson / Curry cluster, Type III) also
   shipped today as `paradox_cantor_type3.md` and
   `paradox_berry_type3.md`. The runnable classifier [O-1] also
   shipped today as `classify_paradox.py` (see below). The one
   remaining gap is **Twin Primes**, the single web-UI paradox not
   in atlas §V — a candidate Type I treatment.
4. **Runnable classifier now exists** (2026-04-24). See
   [`classify_paradox.py`](./classify_paradox.py); `--list`,
   `--template <slug>`, and `--json <path>` modes. The classifier
   reads the markdown templates in
   [`worked_paradoxes/`](./worked_paradoxes/) for stored verdicts
   and enforces Slot-3-forces-Slot-4 on JSON 6-slot instances. An
   example JSON input is in
   [`worked_paradoxes/example_input.json`](./worked_paradoxes/example_input.json).
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
