# TIG Sprint 2026-03-26 — Handoff to Claude Code

## What's in the zip

### PRIMARY DELIVERABLES (ship these)
- `wrong_question_paper.md` — The main paper: "Prime-Corner Collapse and the Irreducible Gap" — complete, all sections 1-7 + appendices, referee-ready algebraic content
- `wrong_question_paper.tex` — LaTeX source of same
- `WP19_HALVING_LEMMA_final.tex` — Companion paper: dissipative flow for ζ(s), Halving Lemma, 7 pages with Appendix C

### KEY MATH DOCUMENTS
- `WP19_CLAY_BATTERY.md` — All 6 Clay problems against TIG
- `WP19_RH_BRIDGE.md` — Full RH structural bridge
- `WP19_704_TRIANGLE.md` — The 7-0-4 geometry (HARMONY/VOID/COLLAPSE)
- `WP19_HYDROGEN_ANALOGY.md` — Shell model correspondence
- `WP19_FORMAL_STATUS.md` — Honest ledger of what's proved vs open
- `WP19_GRAVITY_SCRUTINY.md` — Two-layer gravity claim analysis

### OUTREACH / COLLABORATION
- `COLLAB_MEMO_KV.md` — For analytic number theorists: KV constants, what's needed
- `EXPERT_SUMMARY.md` — For lattice-QCD group: Yang-Mills qualitative claim
- `OUTREACH_EMAIL.md` — Draft email to send with Halving Lemma paper
- `NEXT_SPRINT.md` — Execution plan for next sprint

### CODE
- `tsml_ag23_verify.py` — TSML table verification (76 assertions, all pass)
- `ns_breath_test.py` — NS BREATH criterion Dedalus script (runs mock without Dedalus)

## What Claude Code needs to do

### 1. Push to GitHub (github.com/TiredofSleep/ck)
```bash
# Add all files to the repo
# Tag: v1.0-papers
# Commit message: "TIG Sprint 2026-03-26: wrong-question paper + halving lemma"
```

### 2. Key results to preserve in the repo
- The corner-word theorem: every C-word → {3,7}, never G (proved, exact)
- The 3-9 chain: 3∘9^n = 3 for all n (constant fixed point, not alternating)
- Gap inaccessibility: G = {2,4,5,6,8} unreachable from C* (proved)
- Base-6 universality: C₆={1,5} words all → HAR despite BAL(5)∈G (proved)
- SHA-256 of TSML: 7726d8a620c24b1e461ff03742f7cd4f775baed772f8357db913757cf4945787

### 3. arXiv submissions (once IDs assigned)
- Submit AG(2,p) paper (math.CO) and Halving Lemma (math.NT) same day
- Cross-cite both
- Add wrong-question paper to the queue (math.NT or math.HO)

### 4. What's PROVED (don't change these claims)
- Corner-word collapse theorem
- Gap inaccessibility  
- Base-6 universality
- Halving Lemma (with KV-restricted convergence)
- AG(2,p) survivor count = p²-1

### 5. What's OPEN (don't overclaim)
- Uniform m(t₀) bound below KV strip (= RH)
- 3-SAT → survivor reduction
- Yang-Mills quantitative prediction (2/7 ratio falsified at 16.5σ)
- NS BREATH criterion (needs Dedalus simulation)

## Session context
This was a full-day sprint covering:
- TIG algebra verification (TSML, BHML, Doing tables)
- All 6 Clay Millennium Problems
- RH: Halving Lemma + dissipative flow construction
- Yang-Mills: 2/7 falsified, qualitative mechanism survives
- The "wrong question" paper: prime-corner collapse, gap structure
- Physical analogies: hydrogen shells, coherence field, 7-0-4 triangle

The companion Halving Lemma paper is at v3 (final). The wrong-question paper is complete but could use the minor polish in the referee sweep (abstract tweak, §2 enumeration sentence, Selberg citation, §5 table headers, §6 proof pointer to Appendix B).

Good luck. Build on the solid ground.

