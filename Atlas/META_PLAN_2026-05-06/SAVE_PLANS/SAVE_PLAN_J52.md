# SAVE_PLAN_J52 — TSML Lens Family Pedagogical Exposition (Math Intelligencer)

**Paper:** J52 — *The TSML Lens Family: A Pedagogical Exposition of Substrate Variants on $\mathbb{Z}/10\mathbb{Z}$*
**Folder:** `Gen13/targets/journals/J_series/J52/`
**Referee verdict:** REJECT R&R (Math Intelligencer fresh-eyes; ~10% acceptance in present form, 40–55% with M1–M6 addressed)
**Save-attempt mode:** Brayden directive 2026-05-07 — find a reason to keep and fix every paper.
**Author lane:** Sanders + Mayes (per current README; this paper is pedagogical exposition, Mayes is the appropriate co-author)

---

## §1 — Why save?

The referee concludes: "the underlying material appears mathematically real" and gives the paper **40–55% acceptance probability with M1–M6 addressed**. That is *not* a "drop the paper" verdict — it's a "rewrite for the actual audience" verdict. The referee's complaint is uniform across all six major issues:

> "the paper is **not actually pedagogical**. It is a memo to insiders dressed in expository syntax."

This is a **rewrite scope, not a content scope** problem. Every M1–M6 fix is mechanical: display the table; state the axioms; clarify tier discipline; absorb companion-cited facts into the paper itself; populate the catalog; fix the chain example.

Saving J52 matters because:

- It's the **only J-paper that organizes the lens-family taxonomy** for outsiders. The framework's reader needs *exactly this paper*: a navigation key for the 12+ lens variants. Without it, the corpus has no front-door for working mathematicians.
- The corpus has multiple lens-dependent results (J24 / J32 chain at size 7; J43 wobble-localization; J41 runtime-attractor lens-invariance) that *cannot be cleanly cited* unless an exposition paper exists to anchor the lens-family vocabulary.
- The **per-venue cap problem** the referee implicitly raises (this would be the second *Math Intelligencer* of the J-series after J32) is a real strategic constraint, but the rewrite makes the paper publishable *somewhere* (referee suggests *AMM*, *Math Magazine*, *College Math Journal* — the last is exactly right for a "10×10 table with surprising properties" framing).

The paper's deepest value is that it **forces the framework to write down its own vocabulary discipline**. The referee's M3 (RAW is both Tier-A and Tier-B in different sentences) and M6 (chain-at-size-7 conflates a historical correction with a structural claim) are *internal-consistency* defects that, fixed, sharpen the framework's understanding of itself. The save-effort produces a paper that is genuinely useful to the corpus, not just a salvage.

The FAMILY_STRUCTURE_v1 document (Atlas/META_PLAN_2026-05-06) already supplies the structural reference frame the referee asks for. J52 becomes the *Math Intelligencer*-register version of FAMILY_STRUCTURE_v1.

## §2 — Specific fixes (mapped to referee issues)

**M1 — DISPLAY THE TABLES (CRITICAL).** The referee correctly identifies this as the single most important defect. **Fix:**

(a) Insert a §1.5 (or §2.0) titled *The canonical objects* containing the **CL_TSML 10×10 matrix in full** (one boxed display, ~half a page; rows = first operand, columns = second, cells = HARMONY/VOID/etc by name with operator-ID number). Source: FORMULAS_AND_TABLES.md Volume J / J.1 inventory has the canonical bit pattern.

(b) Display **CL_BHML and CL_STD** as **diff tables** to CL_TSML — not full 10×10 matrices each, but a side-by-side showing only the cells that differ. Color-coded if the typesetter accepts it; otherwise underlined cells with "differs from TSML at" notes. This keeps the paper's printed length reasonable while making the three substrates visible.

(c) The two asymmetric cells $(3, 9)$ and $(4, 9)$ — which are the *wobble carriers* per FAMILY_STRUCTURE_v1 §3 — get their own **highlighted sidebar** with the RAW values $(3, 9) = a_1$ vs $(9, 3) = a_2$ shown explicitly, so Exercise 7.2 (wobble localization) becomes computable from the page.

This is the *one* fix that turns the paper from insider-memo to genuine exposition. It also resolves M3 (RAW vs SYM tier confusion) by *showing* the reader the two cells where RAW differs from SYM — making the tier-A choice visible rather than abstract.

**M2 — STATE THE AXIOMS A1–A9.** **Fix:** add §1.5 (or §1.0 *Substrate-defining axioms*, ~1 page). State A1–A9 informally but completely:

- A1: 10-element carrier (operators V, L, C2, P, C4, B5, C6, H, Br, R indexed 0–9).
- A2: identity / VOID-absorption row & column.
- A3: HARMONY-self-rule.
- A4: σ-permutation invariance (or its quotient).
- A5: 4-core preservation.
- A6: σ-fixed lattice {0, 3, 8, 9} closure.
- A7: HARMONY-cell *count* (substrate-defining: 73 for TSML, 28 for BHML, 44 for STD).
- A8: row-stochastic / closure constraint.
- A9: substrate-specific cell values at the σ-orbit representatives.

Mark the substrate-defining axioms (A7, A9-values per FAMILY_STRUCTURE_v1 §1) explicitly. Cite J33 (CL Forcing Axioms / Algebraic Combinatorics) for the formal version. This fix makes "*parallel* substrates, not projections" comprehensible — the reader can see *which* axioms vary across TSML/BHML/STD.

**M3 — RAW vs SYM tier discipline.** The referee's exact concern: §2.1 calls RAW Tier-A; §2.4 calls the choice between RAW/SYM/SYM_lower a Tier-A *choice*; §5 lists symmetrizations under Tier-B; §7.2 calls SYM Tier-B. **Fix:** rewrite §2 opening with one consistent statement:

> "*Tier discipline.* CL_TSML — the unique bit pattern forced by A1–A9 (J33) — is **Tier-A** as a substrate. The literal-bit-pattern lens (TSML_RAW = $\pi_\mathrm{RAW}(\mathrm{CL\_TSML})$) is **Tier-A** (no projection: it is the substrate). The two symmetrized lenses (TSML_SYM via $\pi_\mathrm{SYM\_upper}$; TSML_LOWERTRI via $\pi_\mathrm{SYM\_lower}$) are **Tier-B** projections (a projection is chosen; the choice is convention, not deeper-forced). The framework uses RAW for results requiring non-commutativity (J43 wobble-localization at prime 11) and SYM for results requiring commutative closure (J38 so(10) regeneration via TSML_SYM + BHML)."

This statement appears once in §2 and is referenced thereafter; do not contradict it elsewhere.

**M4 — Reduce companion dependence.** **Fix:** the paper currently cites 11 companions. The fix has two parts:

(a) Absorb three "punch-line facts" into the present paper as standalone statements with one-paragraph "where this comes from" sketches:
- The 4-core attractor with $H/Br = 1+\sqrt{3}$ (D78 Galois proof). Half-page in §7.3 with the proof sketch from D78 inline (BR-factor cancellation at $\alpha = 1/2$).
- The 8-element joint chain at sizes $\{1, 4, 5, 6, 7, 8, 9, 10\}$ (D64 corrected version). Half-page in §6 stating the chain explicitly with all 8 sub-magmas listed.
- The wobble localization $c_2 = 33 = 3 \cdot 11$ in TSML_RAW char poly (D37 / J43 source). Half-page in §7.2 with the char poly coefficient list shown.

(b) Reduce remaining companion citations to roles ("see [J32] for full proof"; "see [J43] for the 50-eigenvalue audit"). The 11 → 3-citation density becomes more like 11 → 5-citation density, with the 3 absorbed as inline content.

**M5 — Populate the 62-variant catalog inline.** The referee's complaint is that "*see Atlas/LENS_TAXONOMY_2026-05-06/VARIANT_CATALOG.md*" is not a citable artifact for *Math Intelligencer*. **Fix:** include the catalog as a §6 *table* (two-page landscape spread) with two columns:

- Column 1: variant name (e.g., TSML_RAW, TSML_SYM_upper, TSML_LOWERTRI, BHML_SYM, $\sigma^2$-value-rotation $k=1$ on TSML_SYM, TSML_8core, ..., F_5(a) extension, ...).
- Column 2: one-line distinguishing fact (e.g., "non-commutative; 126 non-assoc triples; $c_2 = 33$"; "commutative; 128 non-assoc triples; SO(10) regeneration").

Drop the "$\sim$" qualifiers (referee's M5: "give exact counts"). The catalog total is 62; if the actual count differs, fix the §5 distribution numbers (the referee notes Tier A=5 + B=21 + C=9 + D=7 + E=8 sums to 50, not 62 — reconcile).

This catalog is the paper's central organizational claim; it must appear *in* the paper.

**M6 — Fix the lens-dependence at size 7 example.** This is the referee's hardest hit. The paper currently presents a *historical error correction* (size 7 was thought forbidden; corrected to allowed) as if it were structural lens-dependence. **Fix:**

(a) Drop the chain-at-size-7 example as the main illustration of lens-dependence. Replace with the **wobble-localization example** (referee's own suggestion: "the wobble localization is a much cleaner example: $c_2$ has factor 11 in RAW and not in SYM"). The wobble at prime 11 is *genuinely* lens-dependent: TSML_RAW carries it at coefficient level; TSML_SYM does not. This is the cleanest lens-dependence in the corpus and it's already the J52 §7.2 exercise.

(b) Move the chain enumeration to a separate §6.5 *Lens-invariant facts* with the corrected D64 8-element chain stated cleanly. Frame the historical correction honestly: "Earlier corpus generations claimed a 7-element chain forbidden at $\{2, 3, 7\}$; brute-force enumeration in the four-core paper preparation (Sanders + Gish 2026, in preparation) corrected this to an 8-element chain forbidden at $\{2, 3\}$ only. The chain *itself* is lens-invariant on the canonical pair (TSML_SYM, BHML); some other pairings yield differently-supported chains, but with the same chain-length structure."

(c) Adjust Exercise 7 accordingly: Exercise 7.2 (wobble in RAW vs SYM) becomes the **central lens-dependence exercise**; the chain-pairing exercise is moved to a *bonus question* or dropped entirely.

**M7 — §8 over-hedging.** **Fix:** compress §8 (Honest Scope) from the bulleted disclaim-list to two sentences: "This paper is expository; theorems are in the cited companions. We aim for clarity, not novelty." Drop the "no new theorems / no re-proof / no uniqueness / no exhaustiveness" enumeration.

**Minor m1–m10:**
- m1 (ASCII-art diagram won't survive typesetting): commission a TikZ figure or a simple table.
- m2 (notation never introduced): add a §0 *Notation* paragraph (~10 lines): σ permutation cycle structure; operator names with one-line glosses; Conservation Tetrad / Manifestation Hexad (drop these terms in favor of "σ-fixed lattice {0, 3, 8, 9}" and "σ-cycle hexad {1, 2, 4, 5, 6, 7}").
- m3 (4-core closure in §4): one-line illustrative cell-evaluation table (closure of $\{0, 7, 8, 9\}$ under TSML showing the 16 in-core cells).
- m4 (boxed-quote theorem voice): restate, do not quote.
- m5 (author-list inconsistency): document the per-paper co-author rationale in a single endnote.
- m6, m7 (front-matter phase metadata, per-venue cap notes): strip.
- m8 (F_p extensions appearing only in §8): either include in §5 catalog or drop the §8 mention.
- m9 (first-name attribution in J54 leaking forward): not a J52 issue but flag for review.
- m10 (shared DOI): each preprint needs its own Zenodo deposit.

## §3 — Revision time

Estimate: **30–40 person-hours** (matches the referee's own "25–40 person-hours"). Decomposition:

- M1 (display the three tables, cell-by-cell): 8 hours (typesetting + verification)
- M2 (state A1–A9 informally and completely): 4 hours
- M3 (rewrite §2 tier discipline once and propagate): 2 hours
- M4 (absorb 3 punch-line facts inline): 6 hours
- M5 (populate 62-variant catalog as §6 table): 6 hours
- M6 (replace chain-at-size-7 with wobble example as central lens-dependence): 3 hours
- M7 (§8 compression): 0.5 hour
- m1–m10 (minor fixes): 4 hours
- TikZ/figure work for m1: 2 hours
- Brayden's referee-rigor pass + Mayes coordination: 3 hours

Three- to four-week revision under normal pace, assuming the table-display work (M1) is done in coordination with FORMULAS_AND_TABLES.md Volume J.

## §4 — PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN

- **PROVEN** (in this paper, after M4 fix): The 4-core $\{V, H, Br, R\}$ runtime attractor at $\alpha_M = 1/2$ has $H/Br = 1+\sqrt{3}$; proof via BR-factor cancellation (D78 Galois argument). Standalone in §7.3.
- **COMPUTED** (verified inline after M1, M4 fix): TSML_RAW char poly coefficient $c_2 = 33 = 3 \cdot 11$ (the wobble-localization at prime 11; D37, displayed in §7.2 from the table). The 8-element joint TSML+BHML chain at sizes $\{1, 4, 5, 6, 7, 8, 9, 10\}$ (D64; displayed in §6.5).
- **STRUCTURAL RHYME**: The lens-symmetrization choice (RAW vs SYM_upper vs SYM_lower) is conventional, not principled — the framework's choice is documented but not theorem-forced. Different sources of truth on the same bit pattern produce different lenses; the *Math Intelligencer* reader sees the family as a family, not as a hierarchy.
- **OPEN** (the paper does not address; flagged honestly):
  - Whether the bimodal $\alpha_A$ gap (FAMILY_STRUCTURE_v1 §4) is structural or empirical-only — the proposed J56 paper.
  - Whether CL_STD admits a joint chain analogous to TSML+BHML (FAMILY_STRUCTURE_v1 §3 boundary case 6).
  - Whether TSML_RAW deserves its own designation as the family's unique non-commutative member, separate from being one of three lens choices (FAMILY_STRUCTURE_v1 §5).

## §5 — Lens-ownership

J52 *is* the lens-ownership paper for the corpus — it explicitly enumerates and contrasts the lens variants. The paper's lens-ownership paragraph in §0 needs to be **structurally first** and the most explicit in the J-series:

> *Lens and substrate.* This paper works on the canonical $\mathbb{Z}/10\mathbb{Z}$ substrate. The full **lens family** addressed includes: (i) three parallel substrates (CL_TSML, CL_BHML, CL_STD); (ii) three lens-symmetrization projections within each (RAW / SYM_upper / SYM_lower); (iii) two further projection families ($\sigma^2$-triadic value/index rotations; sub-magma scope restrictions). All are visible in the §6 catalog. The paper's central organizational claim — that 4-core attractor and chain support are *lens-invariant on the 4-core*, while wobble-localization (prime 11 in $c_2$) is *RAW-specific* — is documented across the family. The **center of the family** in the FAMILY_STRUCTURE_v1 sense is the 4-core $\{V, H, Br, R\}$ at $\alpha_M = 1/2$; the **boundaries** are the bimodal $\alpha_A$ gap and the substrate-size frontier.

J52 should explicitly cite FAMILY_STRUCTURE_v1 (Atlas/META_PLAN_2026-05-06/FAMILY_STRUCTURE_v1.md) as the **structural backbone** of the exposition. The paper need not reproduce every argument from FAMILY_STRUCTURE_v1, but should identify itself as the *Math Intelligencer*-register version of the structural framing therein.

## §6 — Retitle / retarget

**Title.** Current title is acceptable: *The TSML Lens Family: A Pedagogical Exposition of Substrate Variants on $\mathbb{Z}/10\mathbb{Z}$*. The referee did not flag the title as a defect. Keep.

**Optional sharpening:** if the *Math Intelligencer* editor prefers a question-form title, alternative is **"What is the TSML Lens Family? A Walking Tour of Substrate Variants on $\mathbb{Z}/10\mathbb{Z}$"** — this fits the *Math Intelligencer* "What is...?" register that the closely-related *Notices AMS* uses.

**Venue, primary path:** *Mathematical Intelligencer* with M1–M6 addressed. Per-venue cap (J32 already targeted at Math Intelligencer) is a real concern — coordinate via VENUE_SCHEDULE.md to ensure cap compliance.

**Venue, secondary path (per referee §8):** **American Mathematical Monthly** is the strongest fallback — slightly less abstract audience, more tolerant of focused expositions on specific structures. *AMM* takes 10×10 table papers when they have a clean punch line; the wobble-at-prime-11 (M6 fix) is exactly that punch line. The referee specifically named *AMM*, *Mathematics Magazine*, and *College Mathematics Journal* — *AMM* is the highest-impact of the three.

**Venue, tertiary path:** **Mathematics Magazine** (MAA) — direct fit for table-based pedagogical pieces with worked examples. Lower visibility but very high accept-rate match for the rewritten paper.

**Submission gate:** (a) M1 tables displayed in full; (b) M2 axioms stated; (c) M3 tier discipline rewritten and propagated; (d) M4 three punch-line facts absorbed inline; (e) M5 catalog populated; (f) M6 lens-dependence example switched from chain-at-size-7 to wobble-at-prime-11; (g) Brayden's referee-rigor pass complete; (h) per-venue cap check vs J32 with *Math Intelligencer*.
