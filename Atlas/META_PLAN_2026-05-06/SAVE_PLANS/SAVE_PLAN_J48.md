# SAVE PLAN — J48: 6-DOF Synthesis (Notices AMS)

**Date:** 2026-05-07
**Directive:** Brayden 2026-05-07: "find a reason to keep and fix every paper."
**Referee verdict:** MAJOR REV pre-submission; CONDITIONAL ACCEPT after restructuring around the Operad obstruction as headline (J48_NoticesAMS_FreshEyes.md)
**Save mode:** ACCEPT THE COLLAPSE + PROMOTE OPERAD + restructure to 10-page focused synthesis

---

## §1 — Why save?

J48 carries one structurally forced and genuinely original mathematical claim that has not appeared in the algebra literature in this form:

> **The bilinear closure of the canonical $10 \times 10$ TSML and BHML composition tables on $\mathbb{Z}/10\mathbb{Z}$ — viewed as Lie, Jordan, and spinor-representation structures jointly — respects the dihedral symmetry $D_4 = \langle P_{56}, \sigma^3 \rangle$. The arity-3 closure (canonical fuse) does not. There is no $D_4$-equivariant canonical fuse rule taking values in the natural $\{a, b, c, L, R\}$ space; the $\sigma^3$ obstruction localizes to exactly one $P_{56}$-orbit. This is a structural distinction at the symmetry-group level between the bilinear and the operadic algebraic content of a finite commutative non-associative magma.**

The referee's fresh-eyes verdict identifies the Operad-vs-the-rest distinction as the strongest result in the paper and notes that it is currently buried as §6 of an 11-section paper. The save path is **to promote the Operad obstruction to the lead theorem**, accept the referee's reduction of the six-DOF taxonomy to a 3-or-4-DOF taxonomy (because Lie + Jordan + spinor-representation collapse to one bilinear-closure DOF), and reframe the paper as a focused 10-page synthesis organized around a single forced theorem with the other DOFs as supporting framing.

The current six-DOF framing is rhetorically convenient (each constituent companion gets its own §) but technically loose. Under the referee's correct critique, Lie/Jordan/Clifford are three presentations of one bilinear-closure DOF (with $\dim 45 = \dim \mathfrak{so}(10)$ shared across all three; the $P_{56} = \sigma_{\rm outer}$ identification is real cross-content but lives at the Permutation/spinor boundary, not as a separate Clifford DOF). The honest count is **3-DOF or 4-DOF**: (i) Bilinear closure (Lie + Jordan + spinor rep), (ii) Permutation, (iii) Lattice, (iv) Operad. The Operad obstruction is what makes the picture interesting — the other three respect $D_4$, the Operad does not.

A *Notices AMS*-class synthesis built around this structural distinction, with the right expository scaffolding for non-specialist AMS readers, is achievable. The referee's recommendation (10-page paper, lead with Operad, demote six-DOF framing) is the save plan. Survival probability under *Notices AMS* editorial filter after restructuring per referee §9 + §8 package cleanup: moderate (20% accept minor revision, 35% major revision, 30% reject-with-referral to specialty algebra venue, 15% desk reject).

---

## §2 — Specific fixes

**Fix-1 (Restructure around the Operad obstruction as lead theorem).** Per referee §9 proposed structure:

| § | Content | Pages |
|---|---------|-------|
| 1 | Motivation and background ($\mathbb{Z}/10\mathbb{Z}$, canonical tables, $\sigma$, $P_{56}$) | 2 |
| 2 | The two canonical tables and their bilinear closure (merged Lie/Jordan/spinor) | 1 |
| 3 | **The Operad obstruction theorem (LEAD RESULT)** | 3 |
| 4 | The four-fold $D_4$-equivariant layer (Bilinear + Permutation + Lattice) | 2 |
| 5 | The runtime attractor (Lattice DOF + LMFDB 4.2.10224.1 connection) | 1 |
| 6 | Cross-structural identifications (4 of 6 from current §9) | 1 |
| 7 | Honest scope and open questions | 1 |
| 8 | References (~30 entries) | 1 |

**Total: 10 pages focused.** Trim from current 11 sections + 12 entries to a 7-section + 1-references structure.

**Fix-2 (Accept the Lie/Jordan/Clifford collapse).** Merge current §1 (Lie), §2 (Jordan), §3 (Clifford / Dirac) into one *Bilinear-Closure DOF* section. State explicitly that Lie-closure-via-commutator and Jordan-closure-via-symmetric-product reach the same dimension 45 = $\dim \mathfrak{so}(10)$, that this is the Lie-Jordan duality $xy = \tfrac{1}{2}([x,y] + \{x,y\})$ of a single underlying associative algebra, and that the spinor representation builds on $\mathrm{Cl}(0,10)$ over the same $\mathfrak{so}(10)$. The $P_{56} = \sigma_{\rm outer}$ identification (currently §3) lives in §6 (cross-structural identifications), not as a separate DOF.

**Fix-3 (Demote six-DOF framing to "categorical decomposition for organizing the corpus").** Replace abstract framing of "six computationally-irreducible DOFs" with: "the algebraic substrate exhibits a structural distinction at the symmetry-group level — the bilinear closure respects $D_4$, the operadic closure does not. We organize the supporting evidence into [3 or 4] structural axes (bilinear / permutation / lattice / operad). The categorical decomposition is convenient for organizing the corpus but is not itself a forced theorem." The honest count is whatever survives the merge; the referee's analysis suggests 4 DOFs (Bilinear + Permutation + Lattice + Operad).

**Fix-4 (Promote LMFDB 4.2.10224.1 connection in §5).** The runtime attractor at $H/Br = 1+\sqrt{3}$, with $r/br$ the unique real root of $x^4 + 4x^3 - x^2 + 2x - 2$ in LMFDB 4.2.10224.1 (Galois group $D_4$), is a real external-validation handle that the current paper underuses. Expand by one paragraph on what LMFDB 4.2.10224.1 is, why it shows up here (the Galois $D_4$ is the same $D_4$ as the symmetry group of the bilinear closure — this is the **non-trivial cross-substrate-and-runtime resonance**), and how $D_4$ rationality at $\alpha = 1/2$ (D78 Galois proof, BR-factor cancellation) sets the runtime apart from generic $\alpha$.

**Fix-5 (Add 2 pages of motivation and expository scaffolding).** Currently §0 is two sentences. *Notices AMS* requires a hook for the general AMS membership. Open with: "When two canonical composition tables on $\mathbb{Z}/10\mathbb{Z}$ are jointly closed under commutator, the resulting Lie algebra is exactly $\mathfrak{so}(10)$. When the same tables are queried at arity 3, no canonical composition law is equivariant under the dihedral symmetry that generates the bilinear closure. This paper synthesizes the algebraic content of these two facts and shows how the bilinear-arity-3 mismatch organizes into a structural-distinction theorem." Then 1–2 pages on what TSML and BHML are, where they come from, why this neighborhood matters (Drápal-Wanless 2021 cited as the closest published precedent — same domain, opposite extremum: theirs maximally non-associative, ours $D_4$-bilinear-closed).

**Fix-6 (Define HARMONY, wobble, Family H, LMFDB, P_56, σ inline).** Per referee §6:
- HARMONY = operator 7 in the 10-operator alphabet $\{V, L, C, P, O, B, H, Br, R, U\}$ — define on first use.
- Wobble = the cells $(3,9)$ and $(4,9)$ where TSML_RAW differs from TSML_SYM, carriers of the prime-11 obstruction in the characteristic polynomial — define when "wobble" first appears.
- Family H = the 8 surveyed canonical fuse rule families per WP112 (D63 in `FORMULAS_AND_TABLES.md`); H is the attractor-4-core preference family, the canonical choice. Define the family taxonomy briefly.
- LMFDB 4.2.10224.1 = number field of degree 4, signature $[2, 1]$, discriminant 10224, defining polynomial $x^4 + 4x^3 - x^2 + 2x - 2$, Galois group $D_4$ — give the field's defining data in the body.
- $P_{56}$ = the $5 \leftrightarrow 6$ swap on $\mathbb{Z}/10\mathbb{Z}$ — define on first use.
- $\sigma = (0)(3)(8)(9)(1\;7\;6\;5\;4\;2)$ — define on first use; explain why this specific cycle structure (it's the canonical permutation generated by the σ-walk on the chain of joint-closed sub-magmas, per WP115).

**Fix-7 (Separate textbook integers from framework integers in §7 signature table).** Currently the table mixes well-known Lie-theoretic dimensions ($\dim \mathfrak{so}(8) = 28$, $\dim \mathfrak{so}(10) = 45$) with framework-specific structural integers ($\|\text{antisym}\|^2 = 81 = 9^2$, TSML char poly $c_2 = 33 = 3 \cdot 11$, 73-cell HARMONY count). Restructure into two sub-tables: (a) Lie-theoretic dimensions (well-known); (b) framework-specific structural integers (new content). One-sentence gloss for each (b)-entry — what it means, where it's verified.

**Fix-8 (Tighten §9 cross-DOF identities to the 4 genuine ones).** Per referee §3.2: Lie ↔ Clifford (= $P_{56} = \sigma_{\rm outer}$, machine precision 0.0), Lie ↔ Lattice (doubly-invariant $\mathfrak{su}(4) \oplus \mathfrak{u}(1)$), Lie ↔ Operad (structurally orthogonal under $D_4$), Lattice ↔ Operad (4-core support fusion-closed). Drop the two tautological identities (Lie ↔ Jordan = duality of presentation; Permutation ↔ Lattice = $\sigma$-fixed lattice is by definition $\sigma$-fixed).

**Fix-9 (Soften "computationally-irreducible" claim in abstract).** Per referee §3.3: "irreducibility" is the absence of a counterexample under chosen diagnostics, not a uniqueness theorem. Reframe abstract as: "we organize the algebraic content into [3 or 4] structural axes that have not been observed to reduce to one another under the diagnostics applied. The structural distinction at the symmetry-group level (bilinear respects $D_4$, operad does not) is a forced theorem."

**Fix-10 (Drop "exhaust" claim).** Per referee §3.4: there is no proof in the paper or cited corpus that the listed DOFs are *all* the algebraic structure on the magma. Cohomological / derived / $A_\infty$ / higher-operadic structures are unexplored. Replace "exhaust" with "cover the algebraic structures probed by the WP100s tower companions [J37]–[J44]."

**Fix-11 (Drop "first explicit naming of TIG framework" framing).** Per referee §8.5: this is internal-track and self-referential. The cover letter announces it; the manuscript can introduce "TIG framework" without making the announcement.

**Fix-12 (Resolve dependency-label inconsistency).** Per referee §8.1: README says "J29, J30, J31, J32, J35"; manuscript body says "[J37], [J38], [J39], [J40], [J44]"; cover letter says "J29, J30, J31, J32, J35"; bibtex says "[J37–J44]." **Pick one.** Per the v3 triadic ordering, the current J-series numbering uses J37/J38/J39/J40/J44 — adopt this consistently across README + cover letter + manuscript + bibtex. The J29-J35 numbering is from a stale version of the ordering.

**Fix-13 (Resolve author-lane inconsistency).** Per referee §8.4: README/cover-letter `lane` line says "Sanders + Gish"; the byline is "Sanders + Mayes." Per directive: Sanders + Gish. Fix byline to match.

**Fix-14 (Deposit J37–J44 on arXiv before submission).** Per referee §4 (the single biggest problem): citing five papers as "submitted to [venue]" with no public copy is *Notices*-rejection-blocking. arXiv-deposit J37, J38, J39, J40, J44 before J48 submission; cite by arXiv ID in the body.

**Fix-15 (Expand external references).** Current bibliography: 5 companions + 5 textbook + 1 LMFDB = 11 entries. Target 30+ for *Notices* synthesis. Per referee §11 suggested additions: Hall-Rehren-Shpectorov (axial algebras), Conway-Sloane (lattice and code), McKay's E_8 correspondence, Borcherds (vertex operator algebras), Loday-Vallette (operads), Markl-Shnider-Stasheff (operads), Loday (cyclic homology), Slansky (group theory for unified models), Mohapatra-Sakita and Wilczek-Zee (outer automorphism of $\mathfrak{so}(10)$).

---

## §3 — Revision time

**Estimate:** 3–4 weeks of focused editing.

- Restructure to 10-page focused synthesis (Fix-1 through Fix-3): 1 week.
- Add motivation/expository scaffolding (Fix-5): 4 days.
- Inline definitions (Fix-6): 2 days.
- Signature table restructure (Fix-7): 1 day.
- §9 tighten + abstract softening (Fix-8 through Fix-10): 2 days.
- Package cleanup (Fix-11 through Fix-13): 1 day.
- arXiv-deposit companion papers (Fix-14): 4 days (depends on companion-paper readiness; the J37–J44 papers must be arXiv-ready independently).
- External references expansion (Fix-15): 2 days.
- Internal review pass: 3 days.

**Calendar fit:** within Phase 5 window. J48 was scheduled as Phase 5 opener (2026-09-02 per current README); the restructuring extends this by 2–3 weeks but stays in Phase 5.

---

## §4 — PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN

- **PROVEN:** Operad $D_4$ obstruction theorem (no $D_4$-equivariant canonical fuse rule on the 126 non-associative TSML triples; cited from [J40]/WP109). 8/8 surveyed rule families are $P_{56}$-equivariant; 0/8 are $\sigma^3$-equivariant ([J40]/WP112). Lie/Jordan closure of TSML+BHML reaches $\dim 45 = \dim \mathfrak{so}(10)$ ([J37]/[J38]/WP102/WP103). Doubly-invariant subalgebra under $D_4$ is $\mathfrak{su}(4) \oplus \mathfrak{u}(1)$ ([J39]/WP104). $P_{56} = \sigma_{\rm outer}$ on spinors at machine precision ([J39] §2.1). 4-core $\{V, H, Br, R\}$ fusion-closed under TSML and BHML ([J44]/WP110). Runtime attractor at $\alpha = 1/2$ has $H/Br = 1+\sqrt{3}$ exactly, $r/br$ in LMFDB 4.2.10224.1 with Galois $D_4$ ([J35]/WP105 + D78 Galois proof from FAMILY_STRUCTURE_v1.md).

- **COMPUTED:** Killing spectrum on doubly-invariant subalgebra is $(-4)^{15} \oplus (0)^1$ (machine-verified). $\|\text{antisym}\|^2 = 81 = 9^2$ (exact). TSML char poly coefficient $c_2 = 33 = 3 \cdot 11$, $c_8 = -2^5 \cdot 7^3 \cdot 11$ (exact, prime-11 wobble localization). 126 non-associative TSML triples reduce to 67 $D_4$-orbits, 16 incoherent orbits; reduce further to 98 $P_{56}$-orbits (70 singletons + 28 doubletons), all $P_{56}$-coherent ([J40]/WP112). $\sigma^3$ obstruction localizes to exactly one triple (3, 9, 9). Family H maps to $\{0:108, 7:18\}$, image entirely in 4-core $\{V, H\}$.

- **STRUCTURAL RHYME:** The integer **16** appears as both $\dim D_4$-invariant Lie subalgebra and $\dim$ chiral spinor irrep of $\mathrm{Spin}(10)$ — structural correspondence via the 16-spinor rep. The integer **11** appears at the coefficient level of TSML's char poly only (not in the 16-dim doubly-invariant subalgebra, which is wobble-free) — wobble-localization signature. The integer **13** appears across BHML's $\sigma_{\rm outer}$-asymmetric cell count and the 9-vector VEV norm. The Galois $D_4$ in LMFDB 4.2.10224.1 matches the bilinear-closure $D_4$ — substrate-and-runtime resonance.

- **OPEN:** (a) Whether the 6-DOF (or 4-DOF) decomposition is unique — alternative classifications could exist; the irreducibility is computational, not a uniqueness theorem. (b) Whether cohomological / derived / $A_\infty$ / higher-operadic structures on the magma are nontrivial — unexplored. (c) Whether the bimodal $\alpha_A$ gap (TSML $\alpha_A \in [0.87, 0.89]$ vs BHML $\alpha_A \approx 0.502$, empty band $\alpha_A \in (0.5, 0.87)$) is structural — open per FAMILY_STRUCTURE_v1.md §4 conjecture. (d) Whether CL_STD admits a joint-closed sub-magma chain analogous to TSML+BHML — unexplored. (e) The substrate origin of the prime-11 wobble at the char-poly level (lives in cell $(3,9)$ of TSML_RAW only; cleared in TSML_SYM and BHML).

---

## §5 — Lens-ownership paragraph (insert in §0 of revised manuscript)

> *Lens and substrate.* This paper works on $\mathbb{Z}/10\mathbb{Z}$ with the canonical TSML and BHML composition tables in their TSML_SYM (commutative) lens. The Lie/Jordan content (§§2–3) is lens-invariant — both TSML_SYM and TSML_RAW give identical antisymmetrization (since RAW differs from SYM only at the wobble cells $(3,9)$ and $(4,9)$, which lie outside the antisymmetric closure's support indices). The runtime attractor (§5) is also lens-invariant. The Operad obstruction (§3, lead theorem) is computed on TSML_SYM; the analogous obstruction holds for TSML_RAW with the same $D_4$-non-equivariance verdict. The five-criterion membership statement (FAMILY_STRUCTURE_v1.md §1) applies: substrate $\mathbb{Z}/10\mathbb{Z}$, commutative under SYM lens, 4-core preserved, $\alpha_A$-bounded non-associativity at $\sim 0.87$, HARMONY-attracting iteration. The 4-core $\{V, H, Br, R\}$ is the algebraic center of the family per §2 of that document; this paper situates the WP100s tower's algebraic content as structures on or around that center. Closest published precedent: Drápal & Wanless (2021), *J. Combin. Theory A* **184**, 105510 — same domain (small finite commutative non-associative magmas), opposite extremum.

---

## §6 — Retitle / retarget options

**Option A (preferred — retitle for Operad-headline framing, keep Notices AMS).** Retitle to: *"An Operadic Obstruction in a Bilinear-Closed Magma on $\mathbb{Z}/10\mathbb{Z}$: A Synthesis."* Lead with the $D_4$-obstruction theorem (§3 of restructured paper). Demote six-DOF framing throughout. 10-page focused synthesis. Survival probability under *Notices* editorial filter after restructuring: moderate (20% accept minor revision, 35% major revision, 30% reject-with-referral, 15% desk reject for non-self-contained citations).

**Option B (retarget to Bull. AMS or AMS Notices "What is..." column).** *Bull. AMS* and the "What is..." column are more selective but the synthesis-class bar is similar. Same content; same restructuring required. Recommendation: not better than Option A; pursue Option A first, fallback to Bull. AMS only if *Notices* desk-rejects.

**Option C (retarget to specialty algebra venue — Adv. Math, Comm. Algebra, J. Pure Appl. Algebra).** Per referee §7 (30% reject-with-referral risk to specialty algebra venue is real). At Adv. Math or J. Pure Appl. Algebra, the synthesis can be pitched in research-mode rather than expository-mode, lowering the audience-mismatch barrier. Survival probability higher (~50–60% for Adv. Math after restructuring), but the prestige is lower than *Notices*. **Recommendation:** prepare Option A submission; if *Notices* desk-rejects or refers, pivot to Option C.

**Option D (split into two papers).** Paper 1: the Operad obstruction theorem alone, as a focused research paper to *Compositio* or *Adv. Math* (this is essentially [J40] standalone, deduplicated). Paper 2: the bilinear-closure synthesis on its own, as a *Notices* expository paper. Risk: doubles the workload. Reward: each paper has higher venue-fit. **Recommendation:** don't pursue unless Option A fails after one revision round.

**Recommendation:** **Option A** (preferred — retitle, restructure to lead with Operad, ship to *Notices AMS*). **Option C** (Adv. Math / J. Pure Appl. Algebra) as fallback.

---

## §7 — Brayden-decision items

1. **Retitle decision.** "An Operadic Obstruction in a Bilinear-Closed Magma" framing vs cosmetic-only retitle of "The Six DOFs."

2. **DOF count.** 3-DOF (Bilinear + Permutation+Lattice merged + Operad), 4-DOF (Bilinear + Permutation + Lattice + Operad), or keep 6-DOF with honest framing? Recommendation: 4-DOF with explicit acknowledgment that the count is curatorial, not theorematic. Lie+Jordan+Clifford collapse to bilinear closure DOF; Permutation, Lattice, Operad each genuinely separate.

3. **Companion-paper arXiv deposit timeline.** J37, J38, J39, J40, J44 must be arXiv-ready before J48 submits. Confirm this aligns with Phase 4 → Phase 5 transition.

4. **Author lane resolution.** Per directive: Sanders + Gish. Fix the Sanders + Mayes byline currently in the manuscript.

---

## §8 — Bottom line

J48's load-bearing content — the Operad-vs-the-rest distinction at the symmetry-group level, with the bilinear closure respecting $D_4$ and the operadic closure not — is a genuinely original mathematical claim that survives unchanged through the referee's critique. The save path is **accept the collapse + promote the Operad + restructure**: merge Lie/Jordan/Clifford into one bilinear-closure DOF (the referee is correct that they are duality-of-presentation, not separate content), promote the Operad obstruction to the lead theorem of the paper, demote the six-DOF framing to a "categorical decomposition for organizing the corpus," add 2 pages of expository scaffolding for non-specialist AMS readers, define HARMONY/wobble/Family H/LMFDB inline, deposit J37–J44 on arXiv, and restructure to a 10-page focused synthesis.

The paper survives. It survives by accepting that three of its six "DOFs" are one DOF in three presentations, and that the real content is the structural distinction between the bilinear and operadic algebraic layers under $D_4$. The Operad obstruction is a *Notices*-class result.

Survival probability under *Notices AMS* editorial filter after restructuring per referee §9 + §8 package cleanup: **moderate** (20% accept minor revision, 35% major revision, 30% reject-with-referral to Adv. Math or specialty venue, 15% desk reject). The reject-with-referral outcome is a real risk and would be *acceptable* — the paper lands somewhere; the science is published. Adv. Math fallback works.

---

**Files referenced:**
- This plan: `Atlas/META_PLAN_2026-05-06/SAVE_PLANS/SAVE_PLAN_J48.md`
- Manuscript: `Gen13/targets/journals/J_series/J48/manuscript/J47_six_dof_synthesis.md`
- Referee: `Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J48_NoticesAMS_FreshEyes.md`
- Family structure: `Atlas/META_PLAN_2026-05-06/FAMILY_STRUCTURE_v1.md`
- Companion citations (need arXiv deposit): J37 (J Algebra), J38 (Israel J Math), J39 (Adv Math), J40 (Compositio), J44 (J Algebra)
- D-numbers cited via FORMULAS_AND_TABLES.md: D48 (binary 4-core closure), D49 (symbolic normalizer Z_T = Z_B), D55 (arity-3 closure), D56 (universal HARMONY attractor), D63 (8-canonical-fuse families), D65 (universal 4-core attractor), D78 (Galois proof BR-factor cancellation)
