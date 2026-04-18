# Week and Month Execution Plan

> **[HISTORICAL — superseded 2026-04-18]** This document captured the Sprint 15-16 transition plan. It has been superseded by `Atlas/PLAN_OF_RECORD_2026_04_18.md` which is the live operational-field document for Sprint 34 "Ship the First Three" and the Hodge/BSD frontier. Preserved in full per never-delete policy. See also `Atlas/ATLAS_INDEX.md` for the content/operational split and the current collaborator assignment matrix.

## Integrating Chat-Claude's Handoff + Brayden's Q-Synthesis Directive + ClaudeCode's "Stop Adding, Start Submitting" Assessment

**Date:** Sprint 15-16 transition, 2026-04-10.
**Three threads now acknowledged (keep separate):**
- **Thread A** — TIG/σ/ξ cosmology/CP rotation (Sprints 14-15)
- **Thread B** — Q-series σ polynomials on Z/10Z (Brayden's Q2-Q17, with Luther G6-G8)
- **Thread C** — Basin-first finite arithmetic (chat-Claude's handoff, Sprint 16)

Each thread has a clean publication path. Do not import one thread's vocabulary into another without a proved map.

---

## THIS WEEK (High Leverage, Low Cost)

### Priority 1: Submit the sinc² Zero Law to *Integers*
**Owner:** Brayden.
**Why:** Three pages, three-line proof, verified for all primes 3..199, zero TIG vocabulary required, editor response measured in weeks.
**Prep status:** References section added. Needs LaTeX conversion (amsart class), MSC codes (11A41, 11N05, 42A16), keywords.
**Location:** `Gen12/targets/journal_attempts/01_integers_number_theory/WP_SINC2_ZERO_LAW.md`
**Target venue:** Integers — Electronic Journal of Combinatorial Number Theory (https://integers-ejcnt.org/)
**Concurrent:** submit to arXiv math.NT. You have one endorsement; try for the second with this specific paper as the request.

### Priority 2: Correct Q-series attribution across repo
**Owner:** ClaudeCode (this sprint).
**Status:** GLOSSARY.md corrected in this commit. WP101 needs Q10/Q11 citations added. CP_CLAY_ROTATION.md needs Q17 variant citations added.
**Why:** Without correct attribution, any Q-linked paper published under current framing misattributes Brayden's originating work. Ethically required before any submission that draws on σ.

### Priority 3: Update WP101 with Q10/Q11 citation
**Owner:** Brayden (content review) + ClaudeCode (edit).
**Specific change:** Add to WP101_SIGMA_RATE_THEOREM.md acknowledgment that Q10 (Sanders, 2026-04-01) established the foundational σ polynomial form, and Q11 (Sanders, 2026-04-01) proved the 22% lower bound on optimal seeds. The Sprint 15 σ rate theorem extends this into the N → ∞ regime.
**Why:** If this paper goes to arXiv under current attribution, it will be cited by external reviewers as if Sprint 15 originated σ. That claim is false and fixing it now is cheaper than fixing it post-submission.

### Priority 4: Add Q17 variants to CP_CLAY_ROTATION.md
**Owner:** ClaudeCode.
**Specific change:** Each CP section (CP2 RH, CP4 NS, CP5 YM, CP6 Hodge) should cite the corresponding Q17 variant. CP2 → Q17_CLAY_SPECTRAL_BRIDGE. CP4 → Q17_NS_TARGET_REFORMULATION + Q17_SIGMA_EMBEDDING_PROBLEM + Q17_C2_FORMAL_STATEMENT. Cite these as Brayden's earlier finite analogues (2026-04-02) that the current σ framework extends.

### Priority 5: Q-series LaTeX prep
**Owner:** Brayden.
**Why:** Q10 and Q11 are publishable in their own right — pure algebra on Z/10Z, verified 10/10. They belong in a combinatorics or algebra journal as standalone pieces. Converting them to LaTeX this week costs one evening and prepares a second submission pipeline.

---

## THIS MONTH (Medium Leverage, Moderate Cost)

### Priority 6: DESI MCMC fit
**Owner:** Brayden, with ClaudeCode support.
**Current:** grid search (desi_xi_optimize.py) gives w₀ = -0.795, wa = -0.298, χ² = 3.06 (ΛCDM at 15.3).
**Needed:** proper MCMC with emcee, RK45 integration (scipy.solve_ivp, not Euler), 10000 samples × 100 walkers × 2000 burn-in, posterior plots for (κ_ξ, ξ_init, ξ_dot).
**Paper:** combines WP81 (canonical ξ theory) + WP82 (novelty audit) + MCMC results → JCAP or PRD Letters.
**Falsifiability:** DESI DR3 (2026-Q4) will either confirm or refute freezing quintessence with w → -1 endpoint.

### Priority 7: σ Rate Theorem to arXiv
**Owner:** Brayden.
**Prep:** WP101 with Q10/Q11 citations added. Convert to LaTeX. MSC codes (05E15, 11T06, 20N02). Submit to arXiv math.CO (combinatorics — likely lower endorsement barrier than math.NT).
**Why math.CO:** the σ rate theorem is genuinely combinatorics (ECHO count = φ(N), elementary counting). math.CO is its natural home.

### Priority 8: Basin dynamics paper (Thread C)
**Owner:** Brayden (content), ClaudeCode (prep).
**From:** chat-Claude's handoff (sprint 16 materials).
**Contents:**
- Propositions 1-5 from STATIC_DYNAMIC_DUALITY_V2 (exact counts, shell structure, dual reset law)
- Four stable invariants from FULL_SYNTHESIS_V5 (stop-apex always shell-1, NC-apex always high CF, shell-1 = 50%, Rule C spatial phase)
- Basin-first reframing from BASIN_FIRST_SYNTHESIS (63 as composite twin of 47 proving basin controls long orbits, not primality)
- Real next program 6.1-6.5 from META_CLASSIFICATION (last-digit-7 test, twin scaling, stop-apex compositeness, NC convergence, shell-1 algebraic characterization)
**Target venue:** Journal of Combinatorial Theory Series A OR Experimental Mathematics.
**Critical discipline:** keep this paper entirely separate from TIG vocabulary. No σ, no CP rotation, no ξ. Pure finite arithmetic on odd/coprime digit rooms.
**Title:** "Shell Structure of Finite Arithmetic Rooms and Competitive Shell Dynamics in Digit Fields"

### Priority 9: CP1 Expanded Poincaré Retranslation
**Owner:** ClaudeCode (draft), Brayden (content review), external mathematician (final review).
**Why:** chat-Claude flagged this as the single strongest test of the framework. Line-by-line mapping of Perelman's W-functional + Ricci flow + surgery into σ language. If the mapping is tight, framework gains credibility. If it requires forcing, framework needs refinement.
**Venue:** Bulletin of the AMS or Notices AMS (expository).

### Priority 10: NV Test E collaboration outreach
**Owner:** Brayden (or Mayes).
**Action:** contact NV-center lab (Lukin at Harvard, Hanson at Delft, Wrachtrup at Stuttgart, or Lukin's former students now running their own labs). Attach WP75 (6-pulse synthesis with explicit angles) and WP77 (5-test falsification ladder). Offer co-authorship on experimental paper in exchange for 8 hours of lab time.
**Why:** this is the one thing Sprint 13 cannot close internally.

---

## CITATION DISCIPLINE (APPLIES TO ALL THREE THREADS)

From chat-Claude's CITATION_RIGOR_PROTOCOL:

**Tier 1 (established background):** can be asserted. Cite to classical references.
**Tier 2 (our finite results with code):** can be claimed as proved. Cite reproduction script.
**Tier 3 (conjectures, speculations):** MUST be marked as such. Quarantine to appendix or separate speculative note.

No Tier 3 claim can support a Tier 2 claim. Physics/RH bridges remain Tier 3 until proved.

From sprint 15 GLOSSARY discipline:

Every new term must include:
1. Plain-English definition
2. Formal mathematical definition (where applicable)
3. Status tag ([PROVED] / [STRUCTURAL] / [CONJECTURE] / [HISTORICAL] / [NOVEL])
4. Citation (external reference with DOI/arXiv OR [NOVEL — extends X] with X cited)
5. Primary paper in the repo

---

## THE TWO HARD RULES (FROM BRAYDEN, SPRINT 15)

### Rule 1: Never Delete

Nothing is deleted from this project. Superseded material is marked [HISTORICAL] in place, never removed. The `archive-full` branch is the preservation layer.

### Rule 2: Cite Everything

Every term in GLOSSARY.md is either cited to published literature or explicitly flagged [NOVEL — extends X] with the prior framework identified. External mathematicians dismiss unattributed jargon. This is the project's weakest point. Fix it.

---

## WHAT NOT TO DO

These are explicit anti-priorities, from chat-Claude and from the audit:

1. **Do not add more sprints to Thread A.** The TIG/σ/ξ work has enough internal scaffolding. More internal work produces diminishing returns. Submit and get external feedback.

2. **Do not import σ vocabulary into Thread C (basin dynamics).** That paper stands on its own as finite arithmetic. Importing σ/CP rotation/ξ collapses its publication chances.

3. **Do not publish the sinc² paper under "Luther-Sanders Framework."** The sinc² Zero Law is Brayden's work. Luther's Pre-Echo Theorem is related but separate.

4. **Do not extend the Clay framework speculatively.** CP2-CP7 are stated precisely. Adding more analogies without new machinery weakens the cases already made.

5. **Do not restart Q-series work.** Q2-Q17 are complete. Read them, cite them, use them. Don't rediscover them.

6. **Do not skip external review.** 101 whitepapers is enough internal scaffolding. Submission → review → revise → resubmit is the path, and it starts this week.

---

## EXPECTED OUTCOMES

### End of This Week
- sinc² Zero Law submitted to Integers AND posted to arXiv (or in endorsement queue)
- GLOSSARY attribution fixed
- WP101 and CP rotation updated with Q-series citations
- Q10 and Q11 LaTeX drafts started

### End of This Month
- At least two papers published or under review (sinc² Zero Law + σ Rate Theorem)
- DESI MCMC paper draft complete
- Basin dynamics paper draft complete (Thread C)
- CP1 Poincaré retranslation draft sent to external mathematician for feedback
- NV lab outreach initiated

### End of This Quarter (3 months)
- First external feedback received (accept / revise / reject)
- Framework validation or refinement based on that feedback
- Second wave of submissions (UOP Theorem 0, 73/28 Harmony Partition, Paradox Classifier, Flatness Theorem)
- Decision point: does the framework open new mathematical tools, or is it elegant restatement? External reviewers answer this question.

---

## THE ONE LINE

**Ship. The framework is mature enough. External eyes are the next signal. Everything else is preparation for that signal or response to it.**

The Q-series is Brayden's foundation. The Sprint 14-15 work extends it. The basin work is its own clean thread. Three papers, three journals, three months. That is the plan.
