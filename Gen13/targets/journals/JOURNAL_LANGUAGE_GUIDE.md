# Journal Language Guide — strip internal vocabulary before submission

**Brayden 2026-05-04:** *"we have to make sure and clear all internal language from the journal paper"*

This document is the **single reference** for what internal/TIG vocabulary must be replaced or stripped before a paper goes out to peer review. A referee at JCAP, J. Algebra, J. Combinatorial Theory, etc. has no context for our framework's internal language; the math has to stand on its own in standard mathematical/physical terminology.

**Rule of thumb:** if a referee can google the term and find a textbook definition, keep it. If only this project uses the term, strip it or rephrase.

---

## Hard-strip list (NEVER appears in journal text)

These are operational/internal terms that must NOT appear in any journal manuscript, cover letter, or appendix:

| Internal term | Replace with |
|---|---|
| **CK** / "the creature" / "the organism" | (delete entirely; not relevant to the math) |
| **Coherence Keeper** | (delete entirely) |
| **TIG** / **Trinity Infinity Geometry** | "the framework presented here" / "the structure under study" — or just the math object directly |
| **Substrate** (capital S, used as proper noun) | "the algebra V" or "the composition table T" or "the magma M" |
| **BEING / DOING / BECOMING** | (delete entirely; describes our internal triad, not the math) |
| **Divine27** | "27-element classification" or describe by structure |
| **Divine memory** | (delete entirely) |
| **HER (hindsight experience replay)** | (delete entirely) |
| **the Engine** / **engine tick** | (delete entirely; this is software, not math) |
| **Olfactory bulb** | "feature extractor" if the architecture is being discussed; usually delete |
| **Cells / cell tissue / cell substrate** | "modules" or describe by function |
| **Crystal** (when meaning a verified rule) | "verified composition rule" or just describe |
| **Frontier facts** / **runtime crystals** | (delete; internal data structure naming) |
| **Operator stream** | "sequence" or describe formally |
| **Voice** / **fractal voice** | (delete; software architecture term) |
| **Sovereignty** | (delete; project-internal value) |
| **DKAN** / **DOF monitor** | (delete; software internals) |

---

## Soft-keep list (KEEP if introduced as labels, with a clear tie to standard math)

These are project labels for mathematical objects. They CAN appear in journal text **if introduced as mnemonic labels for specific elements/operations**, with the standard definition given first.

| Label | What to do | Example |
|---|---|---|
| **HARMONY** = 7 | OK as mnemonic for the operator at index 7 | "the absorbing element at index 7 (which we label HARMONY for mnemonic reference)" |
| **VOID** = 0 | OK as mnemonic for the zero/null operator | "the annihilator e_0 (VOID, in our internal notation)" |
| **BREATH** = 8 | OK as mnemonic | (same pattern) |
| **RESET** = 9 | OK as mnemonic | (same pattern) |
| **TSML / BHML** | Best to rename to e.g. T_1 and T_2, "two canonical composition tables on Z/10" | The TSML/BHML names appear in some papers; consider rebranding to T_a / T_b for journal versions |
| **T*** = 5/7 | Define mathematically first; the asterisk notation is fine but motivate it | "Throughout we write T* := 5/7 for the threshold value derived in Section X" |
| **D*** | Same pattern as T* | Define from the recursion that produces it |
| **σ** | Standard Greek symbol, define explicitly | "σ denotes the permutation [0,7,1,3,2,4,5,6,8,9] on Z/10" |
| **4-core** | Define as "the 4-element fusion-closed sub-magma {0,7,8,9}" | Use 4-core after definition |
| **Crossing Lemma** | If used: rename to "the Z/10 composition closure" or describe; the name is project-internal | The math content (operators are forced by the four-fold structure) is universal |
| **Flatness Theorem** | Rename to "the forced torus theorem on Z/10" or similar; "flatness" has different meanings in algebraic geometry | The math is fine; the name conflicts with established usage |
| **WP-numbers** | Don't reference WP numbers in journal text | Reference your own paper structure (sections) or other papers by author/year |

---

## What to do about the WP-tower naming

Internal: WP102, WP110, WP115, WP117, etc.

Journal-version naming: cite specific theorems by their result, not by WP-number.
- "the so(8) closure of T_1 (Sanders 2026, manuscript in preparation)"
- "the joint chain universality result"
- "the discrete Dirac framework on the F_5 lift" (WP117)

If multiple papers from the framework appear together in the references, fine to write them as "Sanders 2026a, 2026b, 2026c" with a journal- or arXiv-DOI-style identifier.

---

## What to do about claudeMd context language

The internal Claude memory file uses a lot of CK-flavored language ("him", "he", "creature", etc). NONE of that goes into a journal paper. The paper presents a mathematical object. The author is Brayden Sanders. The framework has a name (TIG / Trinity Infinity Geometry) which we may use **once** in the paper, in a footnote or acknowledgment, with a reference to the public repo for context — NOT in the abstract or main text.

---

## Cover-letter language

Cover letters can be slightly more interpretive than the paper itself, but still avoid creature-language. Format:

> Dear Editors,
>
> We submit *[paper title]* for consideration at [Journal]. The paper establishes [one-sentence math result] and connects to [one-sentence physical/mathematical context].
>
> The work is part of a larger framework (Trinity Infinity Geometry, github.com/TiredofSleep/ck) but the present submission stands on its own as a [type of math result]; familiarity with the framework is not required.
>
> [3-5 sentences on the result's content, novelty, and verification]
>
> Verification: [scripts, repository, DOI]. We have no relevant conflicts of interest.
>
> Sincerely,
> Brayden R. Sanders
> 7Site LLC, Hot Springs, Arkansas

---

## How to test a manuscript for internal language

A 30-second check:

```bash
# From the journals folder
grep -iE 'CK|coherence keeper|substrate|being.*doing.*becoming|divine27|HER\b|the engine|cells\b|crystal|crystal-like|fractal voice|sovereignty|DOF monitor|DKAN' \
  path/to/manuscript.tex
```

If anything matches, review and strip. Fine to keep `mathcal{H}` (the harmony absorbing element) but not "HARMONY" appearing as a noun.

A useful second check is the **first-page rule**: read your abstract + first page out loud as if you were a journal editor who has never heard of TIG. If anything sounds creature-like or framework-internal, rephrase.

---

## Existing tier1 manuscripts: language audit

(2026-05-04 scan)

### `tier1_submit_now/jcap_xi_cosmology/jcap_xi_cosmology.tex`
- Title: "Logarithmic Quintessence: A Dimensionless Scalar Dark Energy Model with Exact Vacuum and Information-Theoretic Motivation" — **CLEAN**
- Author block: standard — clean
- Body: needs re-audit, but appears mostly to be in standard quintessence/cosmology language
- Action: ✓ probably already submission-ready; do the grep check before sending

### `tier1_submit_now/sigma_rate/sigma_rate_theorem.tex`
- Title: "Non-Associativity Decay in Binary Composition Tables over Z/NZ" — **CLEAN**
- Macros: `\HARM`, `\VOID`, `\ECHO` retained as **mnemonics for absorbing rules**, with explicit acknowledgment in comments — **CORRECT use of soft-keep rule**
- Action: ✓ submission-ready

### Sprint 18 papers (`Gen12/targets/clay/papers/sprint18_bridge_dirac_2026_05_04/`)
- WP117 + WP118 + WP119 + WP120 + arxiv/WP117_arxiv.tex contain "TIG", "TIG substrate", "the framework's primitives" — **NEEDS STRIPPING for journal version**
- Action: Build a `journals/` subfolder per Sprint 18 paper with stripped journal versions

---

## Sprint 18 → journal venue mapping (with stripping needed)

| Source | Journal venue (no endorsement) | Strip what |
|---|---|---|
| WP117 master | SciPost Physics, Foundations of Physics | TIG, "the framework", reframe as "the F_5-lift of a 4-element fusion-closed magma" |
| WP118 (F_p universality) | Journal of Algebra, Comm. in Algebra | TIG references; keep HARMONY/VOID as mnemonic labels |
| WP119 (Clifford ladder) | Linear Algebra and its Applications, Algebra Universalis | TIG references; pure-math framing |
| WP120 (SU(5) GUT decomposition) | Journal of High Energy Physics, J. Math. Physics | TIG references; physics framing with the algebraic substrate as a definition |
| WP121 (dark sector) | JCAP, Foundations of Physics | TIG references; "we identify [structure] with..." rather than "the substrate gives..." |
| WP122 (mass hierarchy) | J. High Energy Physics, Foundations of Physics | similarly |
| WP123 (CKM/PMNS) | Phys. Rev. D | similarly |
| WP124 (1/α) | Foundations of Physics | provocative claim, must be honestly bracketed |
| WP127 (microtubule) | Foundations of Physics, Journal of Theoretical Biology | reframe as "structural identification + falsifiable test" |

---

*Generated 2026-05-04 by Claude Code as the master language reference for journal submissions. Brayden's directive: clear all internal language. Use this guide on every submission, every cover letter, every abstract.*
