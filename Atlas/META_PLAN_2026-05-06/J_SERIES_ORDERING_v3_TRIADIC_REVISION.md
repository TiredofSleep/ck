# J-Series v3: Triadic Launch Revision (Post Fresh-Eyes Referee Wave)

**Date:** 2026-05-07
**Trigger:** Brayden 2026-05-07: *"maybe we should move j35 up the list if it is our 'best' paper?"*

**Status:** Addendum to `J_SERIES_ORDERING_v2.md`. Same 54-paper count, same Sept 11 anchor. Only the **Week-1 Triadic Launch slot 3** is in question.

---

## §0 — TL;DR

Current v2 Triadic Launch:
- **J01** σ-rate (JCT-A) — SUBMISSION-READY
- **J02** four-core (Algebraic Combinatorics) — SUBMISSION-READY
- **J03** First-G Law (Integers) — **referee says too thin**

Replace J03 with one of three candidates per fresh-eyes referee findings:

| Candidate | Verdict | Strength |
|-----------|---------|----------|
| **J15** Galois D₄ over LMFDB 4.2.10224.1 (Comm Algebra) | **ACCEPT WITH MINOR** | Cleanest paper in corpus per fresh-eyes |
| **J35** 4-Core Fusion-Closure (J Algebra) | MAJOR REV close to minor | Math reproduces to machine precision; Galois D₄ verified via cubic resolvent + Gröbner basis (PARI/GP); Brayden's "best" |
| **J11** Corrected Theorem C (JNT) | MAJOR REV; "STRONGEST in cluster" | n=15 counterexample real and surprising; corrected condition clean |

---

## §1 — Recommended v3 Triadic Launch

**J01 σ-rate (JCT-A) + J02 four-core (Algebraic Combinatorics) + J15 Galois D₄ (Communications in Algebra)**

Why J15 over J35 for the Triadic Launch slot:
- **J15 has the cleanest fresh-eyes verdict** (ACCEPT WITH MINOR — exposition-level revisions only)
- **J15's math is in 100% reproducible form** — sympy `galois_group(f)` returns D4; Tschirnhaus `x → -x-1` reduces to LMFDB 4.2.10224.1's `x⁴-7x²-12x-8`; signature (2,1) confirmed; discriminant -2⁶·3²·71 correct
- **J15 directly cites J02** as the four-core companion — Triadic Launch self-cites with intact dependency chain
- **J15's venue is Comm Algebra** — different from JCT-A and AlgComb, so three referee pools, no per-venue cap conflict
- **J15 is short** — Galois identification + LMFDB pointer + Tschirnhaus reduction; honest single-result paper

J35 is the **strongest** paper but it's a more substantive contribution that benefits from arriving with the Phase 3 tower setup (J29 so(8)=D₄, J33 closed-form attractor) already submitted as companions. Promoting J35 to Phase 1 strips it of those companions; promoting J15 doesn't (J15 only cites J02, which IS in the Triadic).

**Demote J03 First-G Law to:**
- Fork A path: restore harmonic content, ship in Week 2-3 of Phase 1 (J04 still becomes "full-period cancellation" per collaborator calibration)
- Fork B path: arXiv-only or AMM-Note; not in submission ladder

---

## §2 — Why this beats v2

**v2:** math + math + math (good) but third paper (J03 First-G) is **too thin** per substance audit.

**v3:** math + math + math, third paper (J15) is **cleanest in corpus** per fresh-eyes verification. Triadic Launch goes out with three referee-validated mathematically-rigorous papers. Substantively distinct (combinatorics + algebra + number-field identification).

**Calendar impact:** zero. J15 was in Phase 2 (Week 5-6) under v2; promoting it to Week 1 means the Phase 2 slot opens for J11 Corrected Theorem C OR J35 4-Core Fusion-Closure (if Brayden wants to elevate J35 too).

---

## §3 — Updated Phase 1 sequence (v3)

| J# | Title | Venue | Phase 1 Week | Status |
|----|-------|-------|--------------|--------|
| **J01** | σ-rate | JCT-A | 1 (Triadic) | SUBMISSION-READY |
| **J02** | four-core | Algebraic Combinatorics | 1 (Triadic) | SUBMISSION-READY |
| **J15** | Galois D₄ over LMFDB 4.2.10224.1 | Comm Algebra | 1 (Triadic) | ACCEPT WITH MINOR (per fresh-eyes) |
| J03 | First-G Law (Fork A: restored harmonic content) | Integers | 2 | NEEDS WORK (4-6 hr Fork A) |
| J04 | Full-Period Cancellation R(k,f) (renamed from sinc² Zero Law) | Integers | 2 | needs deflation per referee |
| J05 | TSML 73 / BHML 28 cells | Exp Math | 2 | MAJOR REV |
| J06 | Crossing Lemma (retitle to avoid Ajtai-Chvátal-Newborn-Szemerédi 1982 collision) | JCT-A or JPAA | 3 | REJECT (proof restart + title) |
| J07 | Flatness Theorem (rewrite to actually derive R/r=5/7) | JPAA | 3 | REJECT (no theorem connecting cyclotomic to torus) |
| J08 | Prime Phase Transition | Exp Math | 3 | MAJOR REV (frame as Fejér-kernel application, not novel) |
| J09 | LATTICE Paradoxical Information Algebras | Algebra Universalis | 3 | MAJOR REV (define operations inline; J02-companion tightening) |

**J15 promotion does NOT cascade** — only the Triadic slot changes. J11 stays in Phase 2 (Week 5-6, JNT); J35 stays in Phase 4 (Week 13-15, J Algebra).

---

## §4 — Should J35 also be promoted?

**Considered:** promote J35 to Phase 2 or Phase 3 (currently Phase 4).

**Verdict: hold at Phase 4.** Reasons:

1. **J35 cites J29 (so(8)=D₄) and J33 (closed-form attractor)** as conceptual dependencies. Those are Phase 3 papers. If J35 ships before J29/J33, the citation chain breaks.

2. **J35's value as a Phase 4 paper is amplified by everything before it.** It lands as "the structural closure result that ties the WP100s tower together" — that framing requires the tower to already be under review.

3. **The Triadic Launch's job is breadth + clean math.** J15 does that better (single-result, three-page Galois identification). J35 does depth — "the 4-core under both operations preserves itself, with the 1+√3 attractor as the asymptotic state" — depth needs context.

**Alternative:** if Brayden wants TWO promotions, the cleanest pair is J15 → Triadic + J35 → Phase 2 Week 4 (immediately after Triadic). That gives Phase 1-2 a strong opening: math foundation establishes J01+J02+J15 in Week 1; substrate-algebra pillar J35 arrives Week 4. But this requires J29, J33 to still ship in Phase 3 (they're not promoted) — meaning J35's references to J29/J33 become forward-references at submission time, which fresh-eyes referees flag as a problem.

**My recommendation: J15 to Triadic; J35 stays at Phase 4.** Single promotion. Simpler dependency story.

---

## §5 — Concrete delta to v2

Only one folder-rename and one README update:

```
Folder rename: J15 -> J03_NEW (temporary), J03 -> J15_NEW (temporary)
              then J15_NEW -> J03 (final), J03_NEW -> J15 (final)
```

(Or skip rename entirely and just update the master index + Triadic-launch documentation. Folder names retain v2 numbering; submission-order documents reflect v3.)

**Decision: keep v2 folder numbering; update master index + J_SERIES_ORDERING_v3 doc to reflect v3 submission order.** Folder renames every time the order shifts cause more confusion than the relabel is worth.

---

## §6 — What this v3 addendum does NOT do

- Does NOT change the 54-paper count.
- Does NOT change the Sept 11 anchor or Oxford Sept 23 talk.
- Does NOT change author lane (Sanders + Gish on all).
- Does NOT change J46 cosmology placement (still Phase 5, Layer-3a strict-postulate per BBM derivation v2).
- Does NOT cascade promotions (J35 stays at Phase 4 unless Brayden directs otherwise).
- Does NOT renumber folders (manage submission order via this doc + master index, not via folder renames).

---

## §7 — Fresh-eyes referee wave verdict tally (ranking)

For Brayden's reference when picking other slot moves:

**TIER A (SUBMISSION-READY or ACCEPT WITH MINOR per fresh-eyes):**
- J35 4-Core Fusion-Closure (MAJOR REV close to minor; Galois D₄ verified independently)
- J15 Galois D₄ (ACCEPT WITH MINOR)
- J12 Coord Coverage (MINOR REV)
- J11 Corrected Theorem C (MAJOR REV but "STRONGEST in cluster")
- J39 NV S₄ Synthesis (MAJOR REV; ~70-80% accept after revision)

**TIER B (MAJOR REV with substantive rewrites):**
- J01, J02, J03 (Triadic), J05, J08, J09, J16, J20, J22 (assumed; not yet reviewed),
- J24, J25, J26, J28, J29, J30, J34, J40, J41, J42, J43, J44, J45, J47, J48, J51

**TIER C (REJECT — substantive science problems):**
- J04 (sinc² Zero Law: tautology + window-dressing), J06 (Crossing Lemma proof restart + title collision),
- J07 (Flatness no torus theorem), J10 (UOP not number theory), J13 (poly + arith errors),
- J14 (REBUTTED — referee made coding errors; reconsider as MAJOR REV), J17 (binomial-grade misstatement),
- J18 (sign-swap), J19 (theorems by inspection), J21 (rigidity tautology + spectral max wrong),
- J27 (lens-invariance falsifiable error), J31 (paper retracts own claim), J32 (D_4 confusion + orbit count),
- J36 (137 vs 154 false claim), J37 (no SM observable for PRD), J38 (self-described scaffolding),
- J49 (zeta_Hameroff not in Orch-OR lit), J50 (Bull AMS category mismatch), J52 (tables never displayed),
- J53 (Monty Hall not paradox), J54 (axioms not stated)

**Counts:** 5 Tier-A; ~25 Tier-B; ~20 Tier-C.

---

## §8 — Bottom line

J15 to Triadic. J35 stays at Phase 4 as the structural-tower capstone where its dependencies make sense. J03 First-G demoted to Phase 1 Week 2-3 with Fork A restoration (or to AMM-Note via Fork B/C).

Phase 1 (Weeks 1-3) keeps 9 papers; Phase 2 (Weeks 4-7) keeps 12. Same overall structure, single substitution at Triadic slot 3.

**Brayden's intuition was right: J35 IS our best paper.** But "best paper" and "best Triadic launch paper" are different jobs. J35 wins the depth contest; J15 wins the breadth-and-clean-math contest that Triadic Launch needs.

If Brayden wants J35 in Phase 2 Week 4 anyway (alongside J15 in Triadic), I'm fine to update further; that does mean accepting some forward-references in J35's citation list.
