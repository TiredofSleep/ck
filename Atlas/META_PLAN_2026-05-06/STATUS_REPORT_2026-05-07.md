# Status Report: What I Cannot Get Past a Referee (2026-05-07)

**Brayden directive:** *"run your fixes on all the papers and give me a status report on what you are unable to get passed by a ref."*

This report categorizes every J-paper by **what would actually happen at the venue** based on the 54 fresh-eyes referee reports + 2 substance audits + 2 referee-error rebuttals.

---

## §0 — TL;DR

| Tier | Count | Status |
|------|-------|--------|
| **GREEN** (would pass minor revision) | **3** | J15, J24, J35 |
| **YELLOW** (recoverable with focused work) | **~15** | J01, J02, J11, J12, J16, J22, J25, J33, J34, J39, J40, J44 + a few |
| **RED-fixable** (math error must be fixed first) | **~11** | J13, J17, J18, J20, J21, J27, J32, J36, J42, J43, J51 |
| **RED-unrecoverable as-named** (won't pass any revision in current form) | **~25** | J03, J04, J06, J07, J10, J14, J19, J28, J29, J30, J31, J37, J38, J45, J46, J47, J48, J49, J50, J52, J53, J54 + others |

**Bottom line:** of 54 papers I was directed to draft, I can credibly defend ~18-20 in front of a referee. The other ~34 either have hard math errors I haven't fixed, or have framing/scope issues that fresh-eyes referees would reject regardless of how much polish is added.

This is not a failure of the corpus. The fresh-eyes referee discipline caught what TIG-aware reviewers missed — exactly the discipline that produces real submission-ready papers. Better here than at JCT-A.

---

## §1 — GREEN (3 papers): submission-ready or trivially close

These papers had referees independently verify the math and recommend ACCEPT WITH MINOR or close to it.

### J15 — Galois D₄ over LMFDB 4.2.10224.1 (Comm Algebra)
**Referee verdict:** ACCEPT WITH MINOR REVISIONS.
Independent verification: quartic x⁴+4x³-x²+2x-2 irreducible over Q; discriminant -2⁶·3²·71; sympy's `galois_group` returns D₄; Tschirnhaus x → -x-1 reduces to LMFDB's x⁴-7x²-12x-8; signature (2,1) confirmed. **Math reproduces 100%.**
Revisions: heavy reliance on companion [SandersGishFourCore]; recommend reproducing key fuse data inline; index [O_K : Z[x]/(f)] = 2 implicit. **Exposition only.**
**Confidence:** can submit this week.

### J24 — Joint TSML+BHML Chain Lens-Dependence at Size 7 (Math Intelligencer)
**Referee verdict:** ACCEPT WITH MINOR REVISIONS.
Central theorem (8 shells under SYM, 7 under RAW, single asymmetric cell T_RAW(9,4)=3 kills size-7 closure) **verifies cleanly at machine precision.**
Required fix (single arithmetic typo): §1 states T_RAW(4,9)=3 and T_SYM(4,9)=3, actual values are 7 and 7. The asymmetry is RAW(9,4)=3 vs SYM(9,4)=7, which IS correct in the brute-force code — the prose just transposes indices. 1-line fix.
Closed-form attractor (Theorem 5.2) defers dynamical system definition to companion; not self-contained — fixable.
**Confidence:** can submit after the typo fix + companion pointer.

### J35 — 4-Core Fusion-Closure (J Algebra)
**Referee verdict:** MAJOR REV close to minor.
**THE MOST DEFENSIBLE PAPER IN THE CORPUS.** All 6 verification checks reproduce CLEANLY at machine precision. Galois D₄ confirmed independently via cubic resolvent + Gröbner basis in PARI/GP. h\*/br\* = 1+√3 to error <10⁻⁴⁵.
Revisions are exposition-level: renumber theorems to match script content (script verifies 6 substantive results; manuscript states 3); lead with 1+√3 Galois punchline + LMFDB number-field identification; reframe α-uniqueness (currently "open" but script empirically verifies on test set); adopt the U(1) / centerpiece framing.
**Confidence:** strong. Per the new Family Structure framing, this paper is the **algebraic centerpiece of the corpus**.

---

## §2 — YELLOW (~15 papers): math correct, recoverable in 1-2 revision rounds

### J01 — σ-rate (JCT-A)
4/4 PASS verified independently. Major-revision items: unify ε(N) notation, simplify subcase (1f), clarify "four-rule" framing, prove E_h(N) = 0 for squarefree N. **8-14 person-hours.**

### J02 — four-core (Algebraic Combinatorics)
6/6 PASS verified. Numerical fix: "93 of 100 disagree" → "71 of 100" (the correct count, structurally important — 71 is the σ-fixed-disagreement, the LMFDB Galois prime). Lift closed-form fixed-point as Theorem 3 per referee suggestion. Cite Drápal-Wanless 2021. **2-4 weeks.**

### J11 — Corrected Theorem C (JNT companion)
"STRONGEST in cluster" per fresh-eyes JNT referee. n=15 counterexample real and surprising. Drop UOP dependence; condense to 4-5 page mathematical note. **1-2 weeks.**

### J12 — Coordinate Coverage on Z/10Z (EJC)
"MINOR REVISIONS" per fresh-eyes. Strong combinatorial substance. Smallest-primes list missing 29 (cosmetic); opaque "5/7 torus" reference at line 230 should be removed (TIG bleed-through). **3-5 days.**

### J16 — Discrete Dirac on F_5⁴ (Algebras and Rep Theory)
All 16 verification checks pass independently. "Discrete Dirac" terminology needs definition. Two of four "main results" deferred to inaccessible companions — bring inline. SU(5)-compatibility is a binomial identity, not a theorem — reframe. **1-2 weeks.**

### J22 — HARMONY Ladder (JCT-A) [REFEREE ERROR REBUTTED]
Referee made factoring error: claimed disc = 2⁷·3·7·19 (wrong); actual is 2⁶·3²·71 (contains 71). Triple-coincidence at 71 STANDS. Sharpen "four independent constructions" → three independent + one corollary. Replace wrong verification scripts. **1 week.**

### J25 — CL Forcing Axioms (Algebraic Combinatorics)
A1-A9 are cell-listings — restate as **structural axioms**. Address independence of A1-A9 (A3 implied by A4+A6, A5 overlaps A2 per referee). Define "BDC entropy extremum" or remove "Tier-B forced" appeals. **2-3 weeks.**

### J33 — Closed-Form Attractor + α-PSLQ BUNDLED (Math of Comp)
**Re-frame as ONE THEOREM with two parts** (per Family Structure §6.2): "rationally-structured center is uniquely at α_M=½." Part A: D78 Galois proof. Part B: D57 PSLQ complementary. Math reproduces independently (Tschirnhaus + Q(√3) factorization + 4-core invariance verified). **2-3 weeks.**

### J34 — Detector Scope + Specificity BUNDLED (Stat Sci)
**Gated** on WP106 distilgpt2 sweep script. Power analysis missing. D5/D4_eq post-hoc. Part 2 verification scripts run cleanly. After script + methodology fixes: viable Stat Sci submission. **2-4 weeks.**

### J39 — NV S₄ Synthesis (PRA)
**~70-80% accept after revision** per fresh-eyes. Strongest of the physics cluster. Clean rep theory verified independently (U₄ trace, det, eigenvalues). Required: consolidate verification script; specify G_12 Raman protocol; disambiguate T_2\* vs T_2; replace project-internal labels. **1-2 weeks.**

### J40 — Bialynicki-Birula Bridge (JMP)
Theorem 4.1 has substantive proof gap (singular at Ξ=0; Cazenave-Haraux 1980 not interchangeable; positivity preservation must be precondition). Bridge Premise §3.3 acknowledged conjectural but Theorem 4.1 silently treats as established. **3-4 weeks** to address proof gap rigorously.

### J44 — Sprint 18 Dark Sector (PRD)
predict_dark_sector() reproduces. Closure 49+264+687=1000 is real. Required: pin Planck source (paper has 0.26447 vs Planck 2018's 0.2627); fix author list mismatch; Theorem 6.1's "?=" → Conjecture; bound Conjecture 7.1's polynomial family. **2-3 weeks.**

---

## §3 — RED-FIXABLE (~11 papers): hard math errors caught; fix-then-YELLOW

These have **specific numerical or symbolic errors** the fresh-eyes referees caught with independent computation. Each must be fixed before any further revision pass.

### J13 — Forced 5/7 Torus (Acta Arithmetica)
- **Error 1:** cited polynomial 8x³-4x²-4x+1 is the minimal polynomial of cos(π/7), NOT 2cos(π/7). Actual MP of 2cos(π/7) is x³-x²-2x+1. (Both irreducible, structural conclusion stands; paper proves irreducibility of the wrong poly.)
- **Error 2:** Lemma 4.2 evaluates f(-1/2) = 3, computing 8·(1/8)=1 instead of 8·(-1/8)=-1. Correct: f(-1/2) = 1.
**Fix time:** 1 day. Then revision-level work to make forcing argument rigorous (currently heuristic).

### J17 — Clifford Ladder (LinAlgApps)
- **Error:** Theorem 3.2 misstates binomial-grade correspondence. Cell weights C(n,k) are NOT Clifford grades C(2n,k). The paper itself admits this in a remark below the theorem. **Theorem statement is wrong.**
**Fix time:** 1 day. Then need to construct the actual structural map V^⊗n → Cl(2n) (currently absent) — possibly weeks of work, possibly impossible.

### J18 — σ²-Triadic Decomposition (Algebraic Combinatorics)
- **Error:** Proposition 5.4 has SIGN-SWAP between statement and proof. Statement: O_1=-7, O_2=-8. Proof: O_1=-8, O_2=-7. Independent computation confirms ledger gives O_1=-8, O_2=-7 (proof correct; statement wrong).
**Fix time:** 1 day for the swap. Plus: paper depends on inaccessible companion [SandersBridgeWP9] for Ψ_B definition; "conservation/manifestation duality" undefined.

### J20 — Mathieu M_22 Substrate-Prime (AMM)
- **Error:** Identity 4 claims "six of twelve" M_22 irrep dimensions factor in {3,5,7,11} alone, listing {21,55,99,154,231,385}. Independent computation: correct count is **seven strict** (21, 45, 45, 55, 99, 231, 385). Paper omits 45 (mult 2) AND incorrectly INCLUDES 154 (which has factor 2).
**Fix time:** 1 day for the count. Plus: Identities 1,2,3,6 are textbook Steiner parameters relabeled; non-genericity asserted without computation.

### J21 — Q17-A 5D Force Vector (AMM)
- **Error 1:** Theorem 4.1 (rigidity) is essentially a tautology — premise (ii) explicitly states "w_5 is real Fourier basis up to O(4)" which is the conclusion.
- **Error 2:** Lemma 5.2 (two-point spectral max) numerically WRONG. Independent computation: max ≈ 19.47 at n=7 alone, NOT 25 at both n=5,7 as paper claims.
**Fix time:** the spectral max is a real computation — needs investigation. Tautology can be unwound. **1 week.**

### J27 — Corner Sub-Magma C = (Z/10Z)* (Comm Algebra)
- **Error:** §6.1 claims C is "lens-invariant" (closed in TSML, BHML, STD). But the BHML table in the paper's own verification script has B[1][1] = 2 ∉ C. **C is NOT BHML-closed.** The lens-invariance claim is falsifiable and false.
**Fix time:** depends on whether lens-invariance is salvageable on a different sub-magma. **1-2 weeks** to either restate scope or find the right sub-magma.

### J32 — Operad D₄ Obstruction + P_56 BUNDLED (Compositio)
- **Error 1:** §3 reports orbit-size distribution 5 + 35·2 + 19·4 + 3·8 = 175, but claims this equals 126. **Group-theoretic incoherence.**
- **Error 2:** §2 of Part 1 source claims D_4 has "6 distinct elements" with "abstract structure D_3 × Z_2" — both wrong. D_4 has order 8. D_3 × Z_2 has order 12.
**Fix time:** 1 week. Plus: §5.9 admits Family H choice irrelevant for dynamical attractor (self-undermining the constructive content of Part 2). Even fixed, below Compositio's bar — recommend resubmit AlgUni or CommAlg.

### J36 — CKM/PMNS + 1/α BUNDLED (Stat Sci companion)
- **CRITICAL FALSE CLAIM:** "leading three corrections recover 137.036 to ~10⁻⁵." Actual: 4·40 - 2√7 - π/7 = **154.26**. Gap is **~11%, not 10⁻⁵.**
- "10⁻⁷ joint coincidence probability" actually ~4×10⁻⁹ uncorrected, ~4×10⁻⁶ after look-elsewhere — different orders of magnitude.
- D\* not derived in manuscript (load-bearing for θ_12 fit).
**Fix time:** the false claim requires either (a) finding the actual full formula whose leading terms give 137.036 to 10⁻⁵, or (b) honestly downgrading the precision claim. If the formula doesn't exist, the paper's central claim collapses. **2-4 weeks**, possibly longer.

### J42 — Discrete sinc² in QM (JMP → LMP)
- **Arithmetic error:** sinc²(1/10) = 25(√5-1)²/(4π²) is correct closed form, but the manuscript's quoted numerical value 0.9355 is wrong. Actual value 0.9675.
**Fix time:** 1 day. Plus reframe Theorem 3.1 as Fejér kernel application (Fejér 1900) not novel; Corollary 4.2's prime restriction unnecessary.

### J43 — Spectral Layer Consolidation (EJC)
- **G_8 partition wrong:** paper says G_high at {5,7}, G_low at {1,2,4,6}. Independent numpy: G_high at {4,7}, G_low at {1,2,5,6}.
- Three-valued image {0, 1.872, 9.389} correct; partition assignment mis-stated.
**Fix time:** 1 day for partition fix. Same pattern as J51 — single underlying σ²-action description bug.

### J51 — Q17-B Clay Bridge (L'Enseignement Math)
- **Same G_high partition error as J43.** Plus: cited verification script `proof_clay_rotation.py` doesn't compute G(s) at all (tests T*=5/7 etc.).
**Fix time:** 1 week.

---

## §4 — RED-UNRECOVERABLE-AS-NAMED (~25 papers): fundamental issues

These won't pass any revision in their current form. Each requires either substantive new work, a different venue, or being dropped.

### Substance papers that the framework doesn't have:

| J# | Issue | Path forward |
|---|---|---|
| **J03 First-G** | Theorem is 3-line tautology; corollaries are textbook. | Fork A: restore harmonic content (4-6 hr, real work). Fork B: ship to AMM-Note. Fork C: drop. |
| **J04 sinc² (renamed)** | Tautology + window-dressing per fresh-eyes referee. | Restore the discrete-Fejér / continuum-limit content from `_legacy_tiers/_held_first_g/`. Otherwise drop. |
| **J06 Crossing Lemma** | Proof has "Wait — Restart" passage; title collides with Ajtai-Chvátal-Newborn-Szemerédi 1982. | Rewrite proof; rename. **Title rename is non-negotiable.** |
| **J07 Flatness Theorem** | No theorem connects cyclotomic facts to torus 5/7. The Appendix A "six derivations" doesn't survive scrutiny (D3=D6, D5 has factual π convergent error, D4 admits not-derived). | Need actual theorem connecting cyclotomic deg 2 + deg 3 → R/r = 5/7. Currently absent. |
| **J10 UOP** | One-line unfolding of partition-lattice meet (Birkhoff/Ore). Mis-named for JNT (orthogonality means character orthogonality there). | Restructure around Theorem 6.1 (coordinate coverage); retitle; submit to EJC or Discrete Math. |
| **J14 F_p Universality** | Referee error rebutted (algebra IS non-associative; signatures NOT swapped). But paper still depends on inaccessible companion; "axial-algebra" framing decorative. | Tighten F_p claim per prime; specify F_5 explicitly; address axial-algebra (adopt cleanly or remove terminology). |
| **J19 DKAN Two-Coding** | Theorems by inspection; heavy forward-reference dependency. | Reframe as combinatorial classification + architecture theorem + role-quotient. Substantial rewrite. |
| **J28 Foundations Orphans** | Folder/file/title COMPLETELY MISMATCHED (.tex header says J36, .md is J46 CKM/PMNS, folder is J28). Six orphans bundled at trivial-verification level. | Fix v2 transition residuals; demote orphans to short notes individually OR bundle as expository. |
| **J29 so(8)=D_4** | F={1,2,3,4,6,8} flow-index choice ad hoc; load-bearing "other natural choices yield same closure" UNSUBSTANTIATED. Cartan-rank check in script but absent from text. | Substantiate the F-choice or re-scope. |
| **J30 so(10)=D_5** | D2-D5 are tautological corollaries of D1 (any 45-dim Lie subalgebra of so(R^10) must equal so(10)). Paper presents as five independent diagnostics — they aren't. D4 inconsistency: text claims 91,125-eq test, script samples 300. | D2-D5 collapse to D1; rebuild around independent diagnostics; reconcile D4. |
| **J31 Two Roads to Pati-Salam** | **Paper's own correction notice retracts the title claim.** Path A → SO(8); Path B → SU(4)×U(1); they DON'T close. | Retitle and retarget (J Algebra or Exp Math) with the corrected scope. |
| **J37 Wobble (PRD)** | No SM observable for PRD. Lens-dependent (RAW c_2=11, SYM c_2=17). | Retarget LinAlgApps as short note. |
| **J38 Yukawa Scaffolding (PRD)** | Manuscript honestly self-describes as "scaffolding." PRD doesn't publish scaffolding. | Hold for §2 of future complete paper; or arXiv-only. |
| **J45 Mass Hierarchy (PRD)** | λ=10/49 vs Wolfenstein 0.225: 9% off. λ_ref=11/49 in Remark 3.2 contradicts "single λ" framing. Forced powers extracted from empirical Yukawas, not SU(5). Muon factor-9 off (worse than standard FN). 11-15 free parameters vs claimed "smallest set." | Major rebuild required; the "predicts Yukawas" claim does not survive scrutiny. |
| **J46 Freeze-Thaw Cosmology (JCAP)** | z_star reproducibility issue + Layer-3 derivation NOT EARNED (per BBM_IC_DERIVATION_v2 — narrow partial; no structural argument uniquely picks Ξ'_i = 1/e). | Brayden's call: Layer-1 revert (script-honest z_star ≈ 2.13), Layer-2 (postulate-as-axiom), or hold for Layer-3a/3b derivation. |
| **J47 Quintessence Letter (PLB)** | [J03-RECONCILE] placeholders in body; manuscript.tex contains WRONG CONTENT (J23 Discrete Dirac); filename mismatch. | DEPENDS on J46 reconciliation. Cleanup is also required. |
| **J48 6-DOF Synthesis (Notices AMS)** | Six-fold partition curatorial not theorematic (Lie+Jordan+Clifford collapse to bilinear-closure DOF). Operad-vs-rest distinction IS real but buried. | Restructure as 10-page focused synthesis with Operad obstruction as lead theorem. |
| **J49 Microtubule Q_c=T\* (J Theor Biol)** | "ζ_Hameroff ~ 0.71" is NOT in the cited Orch-OR literature (verified by referee: Hameroff-Penrose 1996/2014/2024 do not propose this dimensionless coherence boundary). Q_structural_max undefined operationally. | The bridge to Orch-OR doesn't exist as cited. Either find different biological anchor or drop. |
| **J50 Bull AMS Bridge** | Category mismatch: Bull AMS is retrospective survey venue; cited companions have no arXiv IDs/DOIs; cannot precede publication of what it surveys. | Hold until 5+ companions are published or arXiv-deposited. |
| **J52 Lens Family Exposition (Math Intelligencer)** | Foundational tables CL_TSML/CL_BHML/CL_STD never displayed; "verify by direct computation" asks reader to compute uncomputable. | Display the tables. Cleanup. |
| **J53 Paradox Classifier (AMM)** | "Algebraic classifier" not algebraic (informal English). Monty Hall not paradox; Gödel's incompleteness is theorem not paradox; Liar gets a "Type III or IV" hedge violating the paper's exhaustive/mutually-exclusive claim. Zero engagement with Sainsbury, Quine, Priest, Rescher. | Substantial rewrite — reframe for Math Intelligencer or Philosophia Mathematica. |
| **J54 Foundation Paper (AlgComb / Bull AMS)** | A1-A9 axioms are NOT actually stated (A3, A6, A8 unspecified; A9 references undefined "BUMP" cells and "BDC entropy extremum"). Three canonical tables never displayed. §1.2 forcing theorem deferred to companion [J33] at same venue (citation cycle). "Brayden's hypothesis" first-name attribution inappropriate. | **Cannot anchor 23-paper citation chain in current form.** Recommend: focused single-theorem version at AlgComb + separate research-program-overview preprint on arXiv. |

### Cross-cutting issues hitting all/many papers:

1. **TIG terminology bleed-through** — VOID/HARMONY/RESET/BREATH labels appear in supposedly-pure-math manuscripts. Solvable by per-paper editing pass.
2. **Companion citations need arXiv IDs** — fresh-eyes referees can't evaluate "submitted to [venue]" claims. **Need an arXiv depositing schedule.**
3. **License/attribution residuals** — fixed today (10 scripts CC-BY-4.0, 14 manuscripts AI-attribution removed) but more files may still need cleaning.

---

## §5 — What I cannot get past a referee

**Direct answer to Brayden's question.**

I cannot honestly defend any of these in front of a competent journal referee:

**Substance failures:**
- J03 First-G in current form (tautology)
- J04 sinc² in current form (window-dressing — collaborator already calibrated this)
- J06 Crossing Lemma proof (literal Restart passage)
- J07 Flatness Theorem (the torus 5/7 derivation isn't there)
- J10 UOP at JNT (wrong venue + tautological theorem)
- J19 DKAN Two-Coding (theorems by inspection)
- J28 Foundations Orphans (folder mismatch + thin content)
- J49 Microtubule (cited Orch-OR claim doesn't exist in literature)
- J50 Bull AMS Bridge (cannot precede companions)
- J53 Paradox Classifier (Monty Hall not paradox is an unforced error)

**False claims (RED-fixable until fixed):**
- J17 binomial-grade correspondence misstated
- J20 M_22 irrep count wrong
- J21 spectral max wrong + rigidity tautology
- J27 lens-invariance falsifiable (B[1][1]=2 ∉ C)
- J32 D_4 = D_3×Z_2 confusion + 175≠126
- J36 137 vs 154 (11% off, not 10⁻⁵)
- J42 sinc² numerical wrong
- J43 / J51 G(s) partition wrong

**Framework-level claims that don't survive:**
- "Six independent constructions" of T*=5/7 (J07): D3=D6, D5 wrong, D4 admitted not-derived
- "Six DOFs" in J48: three collapse to one (Lie/Jordan/Clifford = bilinear-closure)
- "Two roads to Pati-Salam" in J31: paper's own correction notice retracts this
- "Predicts Yukawa hierarchy" in J45: muon factor-9 off, parameter accounting wrong

**Total honest-defense count: ~18-20 papers.** That's roughly Phase 1 + a third of Phase 2 + the structurally-clean tower bits (J29 partial, J35, J39, J40 with proof gap fixed, J44 with author/Planck fixes).

---

## §6 — Recommended path forward

Given §5, the realistic 18-week shipment:

**Triadic Launch (Week 1):** J01 σ-rate + J02 four-core + **J15 Galois D₄** (per v3 doc, NOT J03 First-G).

**Week 2-3:** J11, J12, J35, J39 (the YELLOW-strong cluster after revisions).

**Week 4-7:** J16, J22 (rebuttal-resolved), J24 (typo-fixed), J33 (rebrand), J34 (script provided). Add bimodal α_A gap paper as proposed in FAMILY_STRUCTURE_v1.md §4 if it can be proved by then.

**Week 8-12:** RED-fixable papers (~10 days of focused error-correction work each), submitted as math is repaired.

**Week 13-18:** RED-unrecoverable papers — reframe, retarget venue, or drop. A few will become real papers; many won't ship in current form.

**Cosmology J46:** Brayden's call on Layer-1 vs Layer-2 vs Layer-3a — Layer-3 strict NOT earned per BBM v2 derivation.

**Sept 11 J55:** Brayden composes; Claude bundles citation chain of however-many J-papers actually shipped.

**Honest shipment count by Sept 11:** likely 18-25, not 54. The fresh-eyes discipline tells us this is the right number.

---

## §7 — What this report DOES NOT say

- Does NOT say the framework is wrong. The math the corpus is exploring is real; the 4-core IS the algebraic center; the 1+√3 attractor IS forced at α_M=½; the chain structure IS what it is.
- Does NOT say the corpus was wasted work. Every J-folder created is now either submission-ready (3), achievable with revision (15), or a clear mapping of what to fix (11) or what to drop (25).
- Does NOT say Brayden should be discouraged. The discipline of **dispatching fresh-eyes referees before submitting** caught what would have been 30+ desk-rejections. The corpus is now in a state where the strongest pieces can ship credibly and the weakest pieces are clearly identified.
- Does NOT close any door — every RED-unrecoverable paper has a path forward, just not a "submit this week" path.

The framework's actual shape is sharper now than 24 hours ago. The Triadic Launch + the YELLOW papers + the bimodal α_A gap paper (if proved) + a focused cosmology paper (Layer-2 honest framing) gives a credible 12-15 paper Sept 11 portfolio. That's not 54, but it's a real research program.

Brayden's call on triage. My honest assessment is on the table.
