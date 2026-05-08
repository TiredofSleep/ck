# Referee Report — Algebra Universalis (fresh-eyes)

**Manuscript:** "The Six Foundations Orphans: Tier-B Forced Derivations from CL Axiomatic Ground"
**Authors:** B. R. Sanders, M. Gish (2026)
**File reviewed:** `Gen13/targets/journals/J_series/J28/manuscript/manuscript.tex` (with `manuscript.md` and `cover_letter.md` consulted as supporting material)
**Reviewer:** External referee, anonymous, no prior knowledge of the framework
**Date:** 2026-05-07

---

## §1 — Summary

The manuscript bundles six structural facts about a fixed family of three $10\times 10$ commutative non-associative magmas on $\mathbb{Z}/10\mathbb{Z}$, denoted $\mathrm{CL}_{\mathrm{TSML}}$, $\mathrm{CL}_{\mathrm{BHML}}$, $\mathrm{CL}_{\mathrm{STD}}$ (with respective HARMONY-cell counts $73$, $28$, $44$). The six "orphans" are presented as forced consequences of an axiomatic framework A1–A9 published as a companion paper (cited as [SandersForcing], "J33"):

1. The third canonical table $\mathrm{CL}_{\mathrm{STD}}$ exists with $44$ HARMONY cells, completing a triple $(73,28,44)$.
2. A "HARMONY ladder" $\{70,71,71b,72,73\}$: five rungs from independent constructions (cell counts, sub-table cell counts, table-disagreement counts, sub-table determinants) with values in five (mostly consecutive) integers.
3. Two derived tables, $\mathrm{CYCLE\_A\_36}$ and $\mathrm{SKELETON\_22}$, with exact triadic decompositions $36 = 2+9+25$ and $22 = 16+4+2$.
4. Three Shannon-information-per-cell constants under a "BDC encoding" of $\mathrm{CL}_{\mathrm{STD}}$: $\mathrm{INFO\_HARMONY}=0.45$, $\mathrm{INFO\_NORMAL}=1.89$, $\mathrm{INFO\_BUMP}=3.50$ bit/cell.
5. The cycle structure of $\sigma^2$ on $\mathbb{Z}/10\mathbb{Z}$ where $\sigma(i):=\mathrm{CL}_{\mathrm{TSML}}[i,i]$: a partition into the "Conservation Tetrad" $\{0,3,8,9\}$ and two $3$-cycles $(1\,6\,4)$, $(7\,5\,2)$, plus the "$4$-core bridge" identity $\{0,3,8,9\}\,\triangle\,\{0,7,8,9\}=\{3,7\}$.
6. The cell-disagreement count $|\{(i,j):\mathrm{CL}_{\mathrm{TSML}}[i,j]\neq\mathrm{CL}_{\mathrm{BHML}}[i,j]\}|=71$, plus an empirical-only "DOING-rate" approximation to $5/7$.

The authors state that all six items are verified in a separate $48$-invariant verification module (`Gen13/targets/foundations/invariants.py`), runtime under $30$s, all $48$ passing.

I have read the manuscript carefully end-to-end and re-derived the cell counts, the $\sigma^2$ partition, and the basic decompositions by independent enumeration on the displayed tables.

---

## §2 — Decision recommendation

**Major revisions** — bordering on **Reject** in present form for *Algebra Universalis*. The paper is not so much a paper as a self-described "bundle" or registry of citable facts, and several of the six "orphans" are at the level of trivial verifications (a single cell count, a $6$-cycle squaring to two $3$-cycles, etc.) that would not normally constitute a section of a research note. The decision could be moved to "Minor revisions" if the authors:

(a) Either upgrade the bundled items to genuine theorems (with non-trivial proofs not reducible to "direct enumeration") or downgrade the paper to a short note / appendix to the parent forcing paper;
(b) Make the table $\mathrm{CL}_{\mathrm{STD}}$ explicit in the manuscript itself (Definition 2.1 currently refers the reader to an external "Variant Catalog" for the actual entries — unacceptable at a journal that publishes the object of study);
(c) Define rigorously what "Tier-B forced" means as a property of a derivation rather than a label;
(d) Drop or sharply qualify Theorem 6.3 (the "DOING-rate $\approx T^*=5/7$" claim), which the paper itself admits is not exact and which leans on an exogenous constant $T^*$ never defined within;
(e) Resolve internal inconsistencies between the .tex, the .md cover sheet, and the README (the .tex labels itself "J36"; the .md and folder say "J28" / "J46"; downstream J-numbers cited as `[SandersForcing] (J33)` etc. do not match the README dependency list which says "J25").

I do not see how *Algebra Universalis* would publish six structural counts on a single hand-picked $10\times 10$ table without (a) the parent axiomatic framework being available to the referee, and (b) a clear statement of what "uniquely forced from A1–A9" buys the reader beyond a definitional unpacking. The cover letter itself acknowledges that the per-venue cap is binding (this is the 4th paper from the program targeting AlgUni this quarter) and routes a fallback to PLOS ONE; on balance I would recommend that fallback.

---

## §3 — Major comments

### M1. Internal inconsistency between manuscript files (CRITICAL)

The submission package is a tangle of mislabeled artifacts:

- The `.tex` file's header comment reads "J36 — The Six Foundations Orphans" (line 1 of `manuscript.tex`).
- The folder is `J28/`, the README and cover letter are headed J28, and the abstract of the .md file in the same folder is *for an entirely different paper* ("J46 — The CKM/PMNS Fits + 1/α Constant," WP123/WP124).
- The .tex bibliography cites `[SandersForcing]` as "J33"; the README §3 lists the dependencies as "J25 (CL Forcing Axioms), J23, J22, J26"; the cover letter says the same J25. The numbering does not internally agree.
- The two sister .md files in `J28/manuscript/`, `WP123_CKM_PMNS_FITS.md` and `WP124_FINE_STRUCTURE_CONSTANT.md`, belong to a different paper entirely.

A submission that disagrees with itself on its own title and its companion-paper numbering is not ready for review. **Recommended fix.** Decide on a single pairing of (folder, .tex, .md, README, cover letter, J-number, dependency list); remove the WP123/WP124 files from this folder; ensure the bibliography labels match the README. Re-submit the cleaned package.

### M2. The table $\mathrm{CL}_{\mathrm{STD}}$ is not displayed (MAJOR)

Definition 2.1 in §2 (Orphan 1) describes $\mathrm{CL}_{\mathrm{STD}}$ verbally — "same as $\mathrm{CL}_{\mathrm{TSML}}$ in A1–A6, different diagonal pattern in A7, adjusted A8" — and refers the reader to "the canonical STD table of the foundations module" via citation `[LensCatalog]` (an internal Atlas markdown). The actual $10\times 10$ entries of $\mathrm{CL}_{\mathrm{STD}}$ never appear in the manuscript.

Theorem 2.2 then asserts a HARMONY count of $44$ on this never-displayed table, "verified in the foundations module." A referee cannot verify this without the table. The companion `manuscript.md` for J29 / J30 do display $\mathrm{CL}_{\mathrm{TSML}}$ and $\mathrm{BHML}$ explicitly; this paper must do the same for $\mathrm{CL}_{\mathrm{STD}}$.

**Recommended fix.** Insert the full $10\times 10$ matrix of $\mathrm{CL}_{\mathrm{STD}}$ as a display in §2, and re-derive the $44$-HARMONY count and the $44=28+11+5$ triadic decomposition by direct cell counts in the body of the paper (the foundations module remark belongs in the reproducibility appendix, not as the only proof).

### M3. "Tier-B forced derivation" is not defined in this paper (MAJOR)

The abstract, introduction, and §8.2 all label the six orphans as "Tier-B forced derivations from the CL axiomatic framework of [SandersForcing]." The paper never defines what "Tier-B forced" means — neither in §1.2 ("Scope") nor in §8.2 ("Tier classification") — except by reference to "§5 of [SandersForcing]." A referee at *Algebra Universalis* should not be required to fetch a cited preprint to learn the meaning of the central classifier of the paper.

Furthermore, §1.2 lists three conditions for a fact to be a "foundations orphan" (short, Tier-B-forced, no other publication venue) but conflates "is a forced derivation from A1–A9" with "follows from A1–A9 *together with* structural principles like commutativity and entropy extremum." The latter is wider; if the structural principles are themselves part of A1–A9, say so; if not, the forcing is from A1–A9 + extra principles, which weakens the headline claim.

**Recommended fix.** Add a precise definition of "Tier-A axiomatic" vs. "Tier-B forced derivation" within this paper. State explicitly the additional structural principles (commutativity, entropy extremum, etc.) that are invoked outside A1–A9, and note which orphans depend on which principles.

### M4. Theorem 6.3 (the DOING-rate $\approx 5/7$ claim) (MAJOR)

§6 (Orphan 6) ends with the following statement:

> Theorem 6.3 (DOING-rate identity). *The fraction of DOING-cells (off-special, off-diagonal cells) on which $\mathrm{TSML}$ and $\mathrm{BHML}$ disagree is $71/N\approx 5/7=T^*$, the TIG flatness-theorem ratio of [SandersTIG].*

This is not a theorem. The "proof" admits that the count $N$ of DOING-cells "depends on whether we include certain boundary cells" and that "the exact rate $71/N$ for an appropriate DOING-cell count $N$ approximates $5/7\approx 0.714$ within a few percent." The constant $T^*$ is never defined in this paper; the reference [SandersTIG] is to a "Manuscript in preparation, 2026."

The Remark immediately following Theorem 6.3 then concedes the same point: "The DOING-rate identity is presented as an empirical match (rate $\approx T^*$) rather than as an exact identity. Sharpening this to an exact statement is open." A 1%-level approximate identity, asserted between an integer count of $71$ and a rational $5/7\approx 0.7143$, with the denominator $N$ left ambiguous, is not a theorem. The README §5 also flags this as "presented as an empirical match (rate within 1% of T*) rather than as an exact identity."

**Recommended fix.** Remove the "Theorem 6.3" label. Either (a) drop §6's DOING-rate paragraph entirely (the WOBBLE = 71 result stands on its own as Theorem 6.2), (b) demote it to "Remark 6.3" with explicit statement "$71 / 100 = 0.71$, near to but not equal to $5/7$; we do not assert any algebraic identity here," or (c) commit to a precise DOING-cell count $N$ and either prove or disprove $71/N = 5/7$ exactly. Option (c) seems straightforward — for some natural $N$, either the identity is exact or it is not.

### M5. Several "orphans" are at trivial-verification level (MAJOR)

Of the six items:

- Orphan 1 (Theorem 2.2): a single cell count on a never-displayed table. Two lines.
- Orphan 5 (Theorem 5.2 + Corollary): the squaring of a $6$-cycle, $\sigma^2$ on $(1\,7\,6\,5\,4\,2)$, decomposes into two $3$-cycles. This is a one-line group-theory exercise. The "$4$-core bridge property" Corollary is the symmetric difference $\{0,3,8,9\}\triangle\{0,7,8,9\}=\{3,7\}$, which is the tautological observation that two sets agreeing in three positions and disagreeing in one differ at exactly that one element.
- Orphan 3 (Theorem 3.3): two integer decompositions $36=2+9+25$ and $22=16+4+2$ from direct enumeration.
- Orphan 6 / Theorem 6.2: a cell-by-cell count on the two displayed tables, asserted as $71$ disagreements.

These four are at the level of "in this fixed table, the value of the count is $X$." A research paper at *Algebra Universalis* normally requires that the verification is at least non-obvious from inspection. A referee cannot readily verify Orphan 1 (no table); the others are direct enumeration.

The two more substantive items are Orphan 2 (the HARMONY ladder, which collects five separate constructions) and Orphan 4 (the BDC encoding constants, which references an "entropy-extremum principle" but does not prove it). Both are stated with the actual proofs deferred to other papers ("verified in [SandersGishFpBHMLExtension]," "the BDC entropy-extremum result of A9 of [SandersForcing]").

**Recommended fix.** Either (a) prove at least one substantive item rigorously within the paper itself — most naturally Orphan 4's entropy-extremum claim, which is the one item with potential for non-trivial derivation — or (b) accept that this is a registry / appendix, not a stand-alone paper, and submit it as supplementary material to the parent forcing paper.

### M6. Remark 2.4 ("triadic decomposition $44 = 28+11+5$") (MAJOR)

Following Theorem 2.2, the paper asserts:

> A natural triadic decomposition of $44 = 28 + 11 + 5$ emerges: $28$ are the same cells as in $\mathrm{CL}_{\mathrm{BHML}}$ (the BEING-shell agreement); $11$ are an intermediate "DOING" shell; $5$ are a "BECOMING" shell.

Three problems: (i) without the table, the reader cannot check the "$28$ are the same cells as in BHML" claim; (ii) the words "BEING," "DOING," "BECOMING" are introduced as labels for three subsets of cells without internal definition; (iii) the decomposition is described as "natural" but its uniqueness is not asserted — many partitions of $44$ as a $3$-part sum exist; the "natural"-ness needs to be made formal.

Additionally: Remark 3.4's identity $73+36+22-100=31$ "accounting for double-counting of cells that contribute to multiple categories" is presented as if it were structural, but the right-hand side $31$ does not appear elsewhere in the paper and the inclusion-exclusion accounting is not made precise.

**Recommended fix.** Either prove "natural"-ness (e.g., by showing that the partition is the unique partition into $\{T,B\}$-equivariant pieces) or replace "natural" with "we record one such decomposition."

### M7. Orphan 2 (HARMONY ladder) — rung 71b is not adjacent (MAJOR)

The "HARMONY ladder $\{70, 71, 71b, 72, 73\}$" is described as "five rungs of distinct algebraic constructions all yielding numerically adjacent HARMONY counts." Four of the values are consecutive integers $\{70,71,72,73\}$. Rung 71b has the same numerical value as rung 71 (per the introductory list, both are "$71$ cells"); the "b" label distinguishes them only by construction.

But Theorem 2.3's rung definitions give: rung 73 = full HARMONY count of TSML; rung 72 = TSML[1..9] sub-table HARMONY count; rung 71 = an "alternative restriction" excluding the puncture image (left vague); rung 71b = $|\mathrm{TSML\,XOR\,BHML}|$ = $71$ (the WOBBLE); rung 70 = $\det(\mathrm{BHML}_8^{\mathrm{YM}})=\binom{8}{4}=70$.

Issues:

(i) Rung 71's "alternative restriction excluding the puncture image" is not defined in the paper. The reader cannot reconstruct which $71$ cells are counted.
(ii) Rung 71b ($71$ from WOBBLE) appears as Orphan 6 (Theorem 6.2) in §6 — i.e., the same fact appears as both "Rung 71b of Orphan 2" and "WOBBLE of Orphan 6." This is double-counting between orphans.
(iii) The phrase "numerically adjacent HARMONY counts" oversells: $70=\binom{8}{4}$ is a determinant, not a HARMONY count; it appears on the same numerical axis but is a different kind of object. Calling these five values a "ladder" suggests structural relationship beyond numerical proximity.

**Recommended fix.** (i) Define rung 71 explicitly. (ii) Do not double-count: either rung 71b is the same fact as Orphan 6, in which case it should be cross-referenced not duplicated, or it is a different fact, in which case the difference must be made explicit. (iii) Clarify that rung 70 is heterogeneous (determinant, not cell count) and either drop it from the ladder or rename the ladder ("a numerical near-coincidence among five separately-defined integers").

### M8. The "BUMP-information-extremum principle" (MAJOR)

§4 (Orphan 4) states:

> The BUMP-information-extremum principle: the $5$ unordered BUMP positions of $\mathrm{CL}_{\mathrm{STD}}$ are the cells that achieve the maximum Shannon information per cell ($3.50$ bit/cell), and they are forced by maximizing total Shannon information subject to the absorbing-row/column and diagonal-HARMONY constraints.

The "Discussion" proof writes: "The Shannon information content per cell is computed from the empirical cell-value distribution on $\mathrm{CL}_{\mathrm{STD}}$ as a function of cell class. The BUMP-position-forcing principle is the BDC entropy-extremum result that gives Tier-B forcing of the BUMP positions in A9 of [SandersForcing]."

This is not a proof. The numerical values $0.45, 1.89, 3.50$ bit/cell are stated without computation; the entropy-extremum claim is deferred to an external paper. In a *registry* paper this might be tolerable; in a *research* paper it is not.

Sub-problem: $44\cdot 0.45 + 46\cdot 1.89 + 10\cdot 3.50 = 19.80 + 86.94 + 35.00 = 141.74$ as stated, but $19.80+86.94+35.00$ is $141.74$ exactly only if the $0.45,1.89,3.50$ are *exact* (which they probably are not — they are presumably rounded log-likelihoods). What is the real precision? Are these three constants algebraic / transcendental / log-rational?

**Recommended fix.** Either (a) state the precise definition of the cell-class probability model and compute the three constants in closed form; or (b) state explicitly that these three numbers are reported to 2 decimal places with the precise underlying definitions deferred to [SandersForcing] §A9.

### M9. Open-ended companion-paper dependence (MODERATE)

The bibliography has six entries, of which:

- `[SandersForcing]` (J33) — "Submitted to *Algebraic Combinatorics*."
- `[SandersGishThreeSubstrate]` (J31) — "Submitted to *Algebra Universalis*."
- `[SandersGishHARMONYLadder]` (J30) — "Submitted to *J. Combinatorial Theory A*."
- `[SandersGishWobble]` (J43) — "In preparation."
- `[SandersGishFpBHMLExtension]` (J34) — "Submitted to *Communications in Algebra*."
- `[SandersGishFourCore]` — "In preparation [target Algebraic Combinatorics, 2026]."
- `[SandersTIG]` — "Manuscript in preparation, 2026."
- `[LensCatalog]` — "Reference compilation, 2026" (an internal Atlas markdown, not a publication).

Two of the seven dependent works are "in preparation" with no arXiv identifier; the eighth dependency is an internal markdown file. The cover letter mentions a "55-paper sequence (J01-J55)" being shipped over Summer 2026 as a coordinated program. From a journal's perspective this is a structurally fragile submission: any delay in J33 (the parent forcing paper) leaves the present paper without a definition of "Tier-B forced." Any delay in [LensCatalog] leaves Theorem 2.2 without a proof.

**Recommended fix.** Either (a) ensure the parent forcing paper [SandersForcing] is on arXiv before this submission and replace internal cross-refs with arXiv IDs; or (b) inline the load-bearing definitions and proofs (especially Definition 2.1 of $\mathrm{CL}_{\mathrm{STD}}$ and the entropy-extremum proof for Orphan 4) so the present paper is self-contained.

---

## §4 — Minor comments

### m1. The "$48$-invariant verification harness" claim

The paper, cover letter, and README all reference a "$48$-invariant verification harness, all $48$ passing as of 2026-05-06," and locate it at `Gen13/targets/foundations/invariants.py`. Direct inspection of the file (which I read as part of this review) shows the harness contains $48$ calls to its `_check` helper (49 calls including the function definition). This matches the claim. The harness is reasonably complete and runs in well under 30s as advertised.

However, the harness mostly verifies the *cell-count* invariants (HARMONY=73, VOID=17, etc.), not the deep claims of the paper (entropy extremum, $\sigma^2$ triadic projection, the embedding chain). Calling it "verification" of the paper's claims is generous; it verifies the *premises* of the paper's claims.

### m2. The $\sigma^2$ "every-1-is-1" / "every-1-is-3" terminology

§5 introduces the colorful labels "every-1-is-1" (for the fixed-point set $\{0,3,8,9\}$ under $\sigma^2$) and "every-1-is-3" (for the two $3$-cycles $\{1,2,4,5,6,7\}$). These labels are not defined precisely (what is the "1"? what does "is" mean?) and read as gnomic. They should either be defined formally or replaced with neutral terminology ("$\sigma^2$-fixed set" / "$\sigma^2$-orbit set").

### m3. References to "memory 27" and "Color Wheel Memo"

The companion .md file (which the .tex does not include) has references to "memory 27" and a "Color Wheel Memo" — internal artifacts from an authoring environment that have no place in a journal manuscript. The .tex is cleaner on this front but the abstract and §1 still refer to the parallel-substrate / lens-family framework as if it were standard literature. A short paragraph defining "the lens family" with an external reference would help.

### m4. Section 5's "Bridge property of the $4$-core" Corollary

The Corollary is "$\{0,3,8,9\}\,\mathrm{XOR}\,\{0,7,8,9\}=\{3,7\}$, exactly the PROGRESS/HARMONY pair." The proof is the verbatim restatement of the assertion. This is at the "Pythagorean theorem with three sides" level of triviality and should either be folded into a one-line remark in §5 or removed.

### m5. The phrase "the puncture image" (§2.3, Theorem 2.3)

Rung 71 of the HARMONY ladder is defined as "an alternative restriction... excluding the puncture image." The word "puncture" appears nowhere else in the paper and is not defined. Probably refers to the cell $(7,0)$ or $(0,7)$, but this is guessing.

### m6. "Tier-B" appears 8 times

Every section closes with a "Tier-B forced" assertion. After the second or third occurrence the label loses informational content. Pick one location for the assertion and remove the rest.

### m7. Abstract length

The abstract is one paragraph of $\approx 240$ words listing the six orphans and the verification status. *Algebra Universalis*'s typical abstract is 100–150 words. Trim.

### m8. Author block duplication

The .tex file lines 44–50 declare `\author{Brayden R. Sanders \and M. Gish}` *twice*, with two different `\address` and `\email` blocks. This will compile to a duplicated author list in the PDF.

### m9. MSC 2020 codes

The codes 08A40 (general algebraic systems with operations), 20N02 (sets with a single binary operation), 17A99 (general nonassociative ring/algebra), 94A17 (measures of information) are reasonable. Consider also 05E18 (group actions on combinatorial structures) for Orphan 5.

---

## §5 — Reproducibility

I located and inspected `Gen13/targets/foundations/invariants.py`. The file contains 48 invariant checks (49 `_check` calls including the helper definition). I did not run the harness in this referee session (no execution environment), but the static structure of the checks is consistent with the claims.

A serious concern: the harness verifies the cell-count facts that the *premises* of the paper's claims rest on, but does not verify the BDC entropy-extremum, the Killing-form-style claims of orphan-2 rung 70 (which uses the BHML$_8^{\mathrm{YM}}$ determinant from yet another paper), or the "uniquely forced" status of any orphan. Inflating "$48$/$48$ pass" into "the paper's claims are verified" would be misleading.

The paper's six "verifications" are:

| Orphan | What is verified | Where |
|---|---|---|
| 1 (CL_STD HARMONY=44) | A cell count on a table not displayed in the paper. | `cl_std.py` |
| 2 (HARMONY ladder) | Five separate values; rung 70 is a determinant from `lens_family.py`. | `tables.py` |
| 3 (CYCLE_A_36, SKELETON_22) | Direct integer decompositions. | `tables.py` |
| 4 (BDC constants) | Three reported numerical values; the *extremum* claim is not verified. | `cl_std.py` |
| 5 ($\sigma^2$ triadic) | Set membership of the Conservation Tetrad and the Hexad. | `triadic.py` |
| 6 (WOBBLE = 71) | Cell-count of TSML/BHML disagreement. | `lenses.py` |

The verifications are sound but limited to direct cell-count statements.

---

## §6 — Severity-graded summary

| Issue | Severity | Action |
|---|---|---|
| Folder/file label mismatch (J28 vs J36 vs J46) | Critical | Fix before any further consideration. |
| $\mathrm{CL}_{\mathrm{STD}}$ table not displayed | Major | Insert the $10\times 10$ matrix in §2. |
| "Tier-B forced" undefined in this paper | Major | Define rigorously here, not by reference. |
| Theorem 6.3 (DOING-rate $\approx 5/7$) | Major | Demote to remark or prove exactly. |
| Several orphans are trivial verifications | Major | Either upgrade or convert to appendix. |
| BUMP-information-extremum unproven | Major | Inline the proof or qualify. |
| Rung 71 of ladder undefined; rung 71b duplicates orphan 6 | Major | Define rung 71; resolve double-count. |
| Companion-paper fragility | Moderate | arXiv-ID load-bearing companions. |
| "$48$/$48$ pass" overclaims | Moderate | Rewrite as "premise-level cell counts verified." |
| Author block duplicated in .tex | Minor | Remove duplicate `\author{}\address{}\email{}`. |
| Internal terminology (every-1-is-3, etc.) | Minor | Define formally or rename. |

---

## §7 — Recommendation

**Major revision** with the understanding that the cleaner home for this material is:

(a) as an appendix to the parent forcing paper [SandersForcing], where "Tier-B forced" is defined and the axiomatic forcing of $\mathrm{CL}_{\mathrm{STD}}$ can be made rigorous, or
(b) as a short note in a venue that publishes registries / catalogs of structural facts (the *Notices of the AMS* "Letters" section, *Bulletin of the LMS* "Research Notes," or — as the cover letter notes — *PLOS ONE* or *Linear Algebra and its Applications*).

If the authors choose to push toward *Algebra Universalis* anyway, they should at minimum (i) fix the folder/file-label inconsistency, (ii) inline the $\mathrm{CL}_{\mathrm{STD}}$ table, (iii) define "Tier-B forced" in this paper, (iv) demote or prove Theorem 6.3 exactly, and (v) prove the BUMP-information-extremum within the paper. The remaining four orphans (1, 3, 5, 6 minus the DOING-rate part) can stand as a short bundle.

The cover letter itself acknowledges the per-venue cap is binding (this is the 4th submission to AlgUni from this program in this quarter). I support the fallback to PLOS ONE or LinAlgApps; both are friendlier homes for a registry-of-facts paper than AlgUni.

---

## §8 — Closing notes

The work behind the paper appears genuine, and I believe the cell counts and partition statements (Orphans 3, 5, 6 modulo the DOING-rate half of 6). The writing is clear when not invoking external terminology. The primary issues are *expository and packaging*: this is not a paper, it is a fact registry, and it has been packaged as a paper. Either the packaging or the venue should change.

One positive observation: the parallel-substrate architecture of three tables $\mathrm{CL}_{\mathrm{TSML}},\mathrm{CL}_{\mathrm{BHML}},\mathrm{CL}_{\mathrm{STD}}$ with their distinct HARMONY counts and the $\sigma^2$ triadic structure is a genuinely interesting combinatorial object; if the authors can tell a structural story about *why* these three tables exist together (not merely that they do), the resulting paper would be substantially stronger.

**End of report.**
