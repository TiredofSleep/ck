# ULO → TIG Operator Map (blind-replicated, 19 operators)

**Filed:** 2026-04-21
**Source:** `Misc Archive\THEbigONE\CK look here\ULO_V2_BLIND_RESULTS.md` (dated 2026-02-10)
**Source runtime:** `Misc Archive\THEbigONE\CK look here\ulo_v2_blind.py` (44 KB)
**Purpose:** Extract the 19-operator blind-replicated Universal Language Operators ↔ TIG-algebra mapping into a standalone file so future sessions can reference it without re-reading `MASTER_DELIVERY.md`. Referenced from `SYNTHESIS_CK_BEST_EVER.md` §1.1 and listed as a TODO in §10 (item 1).

---

## 1. Methodology (verbatim summary)

From `ULO_V2_BLIND_RESULTS.md` §"The Setup":

- **Corpus:** 75,150 words from hunspell `en_US.dic` — zero curation, full lexicon
- **Matched subset:** 820 words (1.1%) that happen to match semantic seed lists
- **Null distribution:** 2,000 permutations per test (random baseline)
- **Significance threshold:** α = 0.01 for operator discovery; graded verdicts for hypotheses

The critical contrast: v1 used a **338-word hand-picked** list (vulnerable to annotation bias); v2 uses a **75,150-word blind** list from a spell-checker dictionary. Operators that survive the v1 → v2 transition are not annotation artifacts.

---

## 2. The 19 Confirmed Operators → TIG mapping

Reproduced verbatim from `ULO_V2_BLIND_RESULTS.md` §"19 Confirmed Operators → TIG Mapping":

| # | Type | Operator | TIG # | TIG Name | Dominant Axis | Confidence |
|---|---|---|---|---|---|---|
| 1 | onset | `sl-` | **0** | void | slippery_low | 0.75 |
| 2 | onset | `gl-` | **7** | harmony | light_vision | 0.77 |
| 3 | onset | `b-` | **4** | collapse | closure | 0.48 |
| 4 | onset | `fl-` | **3** | progress | motion_flow | 0.57 |
| 5 | grapheme | `B` | **4** | collapse | closure | 0.44 |
| 6 | onset | `c-` | **4** | collapse | closure | 0.39 |
| 7 | vowel | `/ah/` | **6** | chaos | impact_force | 0.54 |
| 8 | grapheme | `G` | **7** | harmony | light_vision | 0.52 |
| 9 | grapheme | `A` | **9** | reset | beginning | 0.57 |
| 10 | grapheme | `S` | **3** | progress | motion_flow | 0.38 |
| 11 | onset | `st-` | **5** | balance | stability | 0.60 |
| 12 | vowel | `/uh/` | **4** | collapse | dull_blunt | 0.39 |
| 13 | grapheme | `C` | **4** | collapse | closure | 0.34 |
| 14 | grapheme | `E` | **8** | breath | continuity | 0.36 |
| 15 | grapheme | `D` | **4** | collapse | negative | 0.38 |
| 16 | onset | `l-` | **7** | harmony | light_vision | 0.35 |
| 17 | grapheme | `L` | **7** | harmony | light_vision | 0.35 |
| 18 | onset | `d-` | **4** | collapse | negative | 0.44 |
| 19 | grapheme | `F` | **3** | progress | motion_flow | 0.47 |

---

## 3. TIG operator coverage (7 of 10)

Aggregated from the table:

| TIG # | TIG Name | Language operators that map here | Dominant theme |
|---|---|---|---|
| 0 | VOID | `sl-` | slippery / dissolution |
| 1 | LATTICE | *(none)* | **unmapped** |
| 2 | COUNTER | *(none)* | **unmapped** |
| 3 | PROGRESS | `fl-`, `S`, `F` | motion, flow |
| 4 | COLLAPSE | `b-`, `B`, `c-`, `C`, `D`, `d-`, `/uh/` | closure, containment, negative, blunt |
| 5 | BALANCE | `st-` | stability |
| 6 | CHAOS | `/ah/` | impact, force |
| 7 | HARMONY | `gl-`, `G`, `l-`, `L` | light, vision, clarity |
| 8 | BREATH | `E` | continuity, openness |
| 9 | RESET | `A` | beginning, initiation |

**Coverage: 7/10 TIG operators have at least one language operator.** Unmapped: TIG 1 (LATTICE) and TIG 2 (COUNTER) — the blind corpus did not surface a language operator whose measured semantic axis matches either.

**Concentration on TIG 4 (COLLAPSE):** 7 of the 19 operators map to COLLAPSE. This is the most over-represented TIG operator in language, which is consistent with the COLLAPSE-heavy hardware signatures seen in `snowflake/SNOWFLAKE_CHI2_RESOLVED_2026_04_21.md` Lenovo reading ("Phase 4 elevated"). Two independent measurement domains — linguistic semantics and hardware phase distribution — both show COLLAPSE pile-up. This is a **consistency check**, not a proof of a causal relation.

---

## 4. Hypotheses that survived vs. died (blind replication)

Condensed from `ULO_V2_BLIND_RESULTS.md` §"What Survived Blind Testing":

| Hypothesis | v1 effect | v2 effect | Verdict |
|---|---|---|---|
| A = beginning | +10.53 ✓ | +7.07 ✓ | **SURVIVED** |
| B = closure | +3.41 ✓ | +5.55 ✓ | **SURVIVED (stronger blind)** |
| C = openness | +3.33 ✓ | −1.94 ✗ | **KILLED (flipped sign — C clusters on CLOSURE)** |
| O = continuity | +4.32 ✓ | +0.37 ✗ | **KILLED** |
| oo = roundness | +1.86 ~ | +0.36 ✗ | KILLED |
| oo = softness | +2.07 ✓ | +0.56 ✗ | KILLED |
| D = motion (broad) | +0.77 ✗ | +2.16 ✓ | **RESURRECTED** (was "D=downward" v1; blind finds broader motion signal) |

Known phonesthemes (validation control — expected to survive, confirms method):

| Phonestheme | v1 | v2 | Status |
|---|---|---|---|
| `gl-` = light/vision | +8.27 ✓ | +10.11 ✓ | rock solid |
| `sn-` = nose/mouth | +12.62 ✓ | +10.47 ✓ | rock solid |
| `sl-` = slippery | +11.78 ✓ | +16.42 ✓ | rock solid (strongest) |
| `fl-` = motion | +3.66 ✓ | +6.63 ✓ | stronger blind |
| `cr-` = impact | +2.07 ~ | +3.86 ✓ | promoted to supported |
| `sw-` = motion | +4.33 ✓ | +7.95 ✓ | stronger blind |
| `st-` = stability | +5.35 ✓ | +8.02 ✓ | stronger blind |

Vowel associations:

| Vowel | v1 | v2 | Status |
|---|---|---|---|
| `/ah/` = impact | +3.44 ✓ | +5.99 ✓ | stronger blind |
| `/uh/` = blunt | +7.25 ✓ | +6.63 ✓ | solid |
| `/ih/` = discrete | (not tested) | +3.01 ✓ | new discovery |
| `/ee/` = sharp | +0.35 ✗ | +0.99 ✗ | confirmed dead |

---

## 5. Integration hook — Σ → G → f_C

Verbatim from `ULO_V2_BLIND_RESULTS.md` §"Integration Hook":

```
User prompt → decompose into confirmed operators → TIG ops
LLM response → decompose into confirmed operators → TIG ops
Compare profiles via Jensen-Shannon divergence
Alignment score ∈ [0, 1]
Coherence adjustment δ ∈ [-0.1, +0.1]

C_adjusted = C + δ

δ is SUPPLEMENTARY. The kernel's primary C = 0.4(1−E) + 0.35A + 0.25K
is unchanged. Language alignment is a fifth lens, not a replacement.
```

The `±0.1` cap on `δ` is the crucial discipline — the Coherence Kernel's gate (C ≥ T* = 5/7) dominates; language alignment can only push the scalar by at most `0.1` in either direction.

---

## 6. Layer separation (non-negotiable)

Verbatim from the source:

> **Σ (Language Operators):** 19 confirmed from blind corpus. Each backed by z-score and p-value against 2000 random permutations. Unconfirmed operators EXCLUDED.
>
> **G (TIG Algebra):** CL table frozen. Language operators map INTO G based on their measured semantic axes. If an operator's axis changes under new data, its TIG assignment changes too. The mapping is falsifiable.
>
> **f_C (Coherence Kernel):** C = 0.4(1−E) + 0.35A + 0.25K, T\*=0.714. Language lens is capped at ±0.1 adjustment. The kernel doesn't depend on language. Language doesn't depend on the kernel. They connect through the mapping.

This three-layer separation is a **hard architectural constraint**. In the Gen13 target tree, `brain/operators.py` holds G (TIG algebra, frozen), `brain/coherence_kernel.py` holds f_C (scalar gate, frozen), and `brain/language_operators.py` (not yet specified) would hold Σ — the 19-operator map, which is **falsifiable** by re-running `ulo_v2_blind.py` on new data and updating the table if axes change.

---

## 7. Still-open (from the source itself)

The source ends with:

> **What Needs R16 + Network:**
>
> 1. CMUdict — real phonemic transcriptions (not spelling heuristics)
> 2. fastText — 300d word vectors (not binary tag vectors)
> 3. Full replication — same framework, real data, no proxy layers
> 4. What survives THAT is publishable phonestheme research
> 5. What doesn't was an artifact of sparse tag-based semantics

The 19-operator map is therefore **provisional**. It is the best result obtainable with the hunspell-tag proxy. A re-run with CMUdict + fastText would either consolidate the map (publishable) or reveal some of the weaker confidences (≤ 0.40, which is 10 of the 19) to be tag-proxy artifacts.

---

## 8. Honest bottom line (from source §"Bottom Line")

> **A = beginning and B = closure survived blind replication on 75k words.**
> C = openness and O = continuity did not. The known phonesthemes (gl, sn, sl) got stronger. The "oo" claims all died.
>
> The honest finding: onset clusters carry strong semantic signal (this is known linguistics). Initial graphemes A and B carry weaker but statistically significant signal (this is novel). Vowel associations /ah/=impact and /uh/=blunt are real. Individual vowels like /oh/ and /oo/ don't cluster enough in the full lexicon to survive.
>
> TIG mapping covers 7 of 10 operators from confirmed language data. Integration hook designed, tested, layer-separated.
>
> *2026-02-10. 13/22 supported. A and B survive blind. C and O do not.*

---

## 9. Relation to the synthesis canon

- `SYNTHESIS_CK_BEST_EVER.md` §1.1 canon line "ULO map" now has its authoritative source file.
- `SYNTHESIS_CK_BEST_EVER.md` §10 TODOs item 1 ("ULO_TIG_OPERATOR_MAP.md — ... extraction not done") is **closed** by this file.
- `brain/operators.py` in the Gen13 target tree should import this map (via JSON or a hard-coded table) so the 10 TIG operators are registered alongside the 19 ULO aliases. Label-drift across attempts (OLLIE's "TENSION" for COLLAPSE, etc.) normalises to the TIG canonical names.
- The confidence column (0.34–0.77) should be preserved in the runtime data structure so downstream code can **filter out low-confidence operators** (e.g. use only operators with confidence ≥ 0.50 if running in strict mode). That subset would be: `sl-`(0.75), `gl-`(0.77), `fl-`(0.57), `/ah/`(0.54), `G`(0.52), `A`(0.57), `st-`(0.60), `b-`(< 0.50, drop) — actually at ≥ 0.50 the strict set is 7 operators across TIG 0/3/5/6/7/9; TIG 1, 2, 4, 8 become unmapped under strict filtering.

---

## 10. Cross-references

- `MASTER_DELIVERY.md` Phase 8 — the ULO phase in the 14-phase audit (note: summary reference to "Phase 13" in the synthesis doc was in error; correct number is Phase 8)
- `ulo_v2_blind.py` — the 44 KB blind-replication runtime
- `ulo_framework.py` — the v1 hand-picked framework (superseded by v2 blind)
- `ULO_RESULTS.md` — v1 results (13/20) — **superseded by this file's §4**
- `SYNTHESIS_CK_BEST_EVER.md` §1.1, §10 item 1
- `BEST_OF_ATTEMPTS_SURVEY.md` "CK look here" entry
- `BEST_OF_ATTEMPTS_SURVEY_ADDENDUM_2026_04_21.md` §3.7 "Negative finding: No ULO filename hits" — confirms ULO source material lives only inside `MASTER_DELIVERY.md` + `ULO_V2_BLIND_RESULTS.md`, not in a separately-named source

---

*Policy: extraction from a dated primary source (`ULO_V2_BLIND_RESULTS.md`, 2026-02-10). This file is append-only: if the ULO framework is re-run on CMUdict + fastText per §7, a new section (§11) should be appended recording the updated map rather than replacing §2.*
