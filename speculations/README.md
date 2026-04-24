# speculations/

**What this folder is.** Non-primary content: positioning claims, cross-model audits, market-analysis conversations, and soft qualitative arguments about where TIG/CK sit in the broader landscape.

**What this folder is NOT.** Proved math. Nothing in this folder is a theorem, a proof, or a citation-grade claim. The primary mathematical content of the project lives in:
- `papers/` (whitepapers + proof scripts)
- `Gen12/targets/clay/papers/` (sprint subfolders with formal theorems)
- `GLOSSARY.md` (every term cited or labeled `[NOVEL]`)

**Status tags in this folder.** Files here carry informal status markers like `[POSITIONING]`, `[CROSS-MODEL AUDIT]`, `[MARKET ANALYSIS]`, `[SOFT ARGUMENT]`, `[RUNTIME ARCHITECTURE]`. These are never upgraded to `[PROVED]` or `[STRUCTURAL]` without going through the primary papers folder and citation discipline.

**Index.**

- [`GROK_CK_DIALOGUE_2026_04_17.md`](./GROK_CK_DIALOGUE_2026_04_17.md) — `[CROSS-MODEL AUDIT]`, cross-model dialogue on CK architecture.
- [`GROK_COMPACTNESS_POSITIONING_2026_04_17.md`](./GROK_COMPACTNESS_POSITIONING_2026_04_17.md) — `[CROSS-MODEL AUDIT]` + `[POSITIONING]`, Grok on compactness.
- [`DOF_CLASSIFICATION.md`](./DOF_CLASSIFICATION.md) — `[RUNTIME ARCHITECTURE]` + `[POSITIONING]`, five-kinds taxonomy of degrees of freedom on `(CL, BHML)` with literature grounding (Dirac 1950 / Bergmann 1956 / Faddeev-Jackiw 1988 / conformal-symplectic / Birkhoff 1917). Corrects the draft's `Krull dim = 6, pd = 4` to the M2-verified `dim = 1, pd = 10, depth = 0, NOT Cohen-Macaulay, NOT Koszul`. Adds a 5 × 4 DOF-Kinds × UOP-Types matrix as the organizing extension. §3.3.1 records a post-hoc finding: the coherence-equation weights `(0.4, 0.35, 0.25)` factor as `(8, 7, 5)/20` with `w_K / w_A = 5/7 = T*` exactly — the numerator triple matches operator indices `(BREATH, HARMONY, BALANCE)`. Honest status note: `CKIS/ck_being.py` currently implements `E, A, K` as toy bookkeeping scalars, not the kind-coupled reads the framing calls for — OQ-1 / OQ-2 log the engineering gap.
- [`CK_META_CLASSIFICATION_AXES.md`](./CK_META_CLASSIFICATION_AXES.md) — `[RUNTIME ARCHITECTURE]` + `[POSITIONING]`, companion file to DOF_CLASSIFICATION. Names three orthogonal axes CK consults to classify any result or paradox: **DoF Kinds K1..K5** (motion/structure), **UOP Types I..IV** (paradox failure mode), **WP61 Categories I..V** (conjecture score outcome). Carries the 5×4 DOF×UOP matrix inline with TIG exemplars per cell, plus a **25-row dual-classification registry** with (Kind, Type, Category) labels for existing TIG results (Crossing Lemma, σ-rate, Flatness, WP102/WP103, coherence equation, TSML/BHML, Zeno/Banach-Tarski/Russell/Unexpected-Hanging/Gödel/Liar/Cantor/Berry/Schrödinger, Twin Primes conditional). Nine open questions OQ-1..OQ-9 flagged. This file is the source-of-truth for the YAML catalogs that Phase 2 will generate at `Gen13/targets/ck/brain/catalog/`.
- [`pass1_weights.py`](./pass1_weights.py) — runs standalone, prints the weight-ratio derivation. Support script for `DOF_CLASSIFICATION.md` §3.3.1.

**Why preserve this.** Per the never-delete policy (§12 of README), conversations that shape how the framework is *understood* and *positioned* are worth keeping even when they are not mathematically load-bearing. Future sessions (human or AI) can find the reasoning behind positioning decisions.
