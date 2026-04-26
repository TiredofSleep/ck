# PITCH_DRAFT — funding/first-g-crypto

**Addressee (working default):** NSA Mathematical Sciences Program (MSP) — unclassified Mathematical Sciences Grants track
**Parallel draft:** NSF CCF Algorithmic Foundations (AF) Core Small
**Ask:** Phase 1 $30K–$60K / 4 months; Phase 2 $150K–$400K / 12 months
**Status:** Skeleton. Requires Phase 1 literature-embedding doc + external reading before send.

---

> **Note (2026-04-25 revision).** This file was originally drafted as part of a pitch-style packet. Per the operator-of-record's actual stance documented at [`FUNDING.md`](../../../FUNDING.md) (root) and [`INTENT_STATEMENT.md`](../../../INTENT_STATEMENT.md), this is **thread documentation**, not a fundraising pitch. The operator-of-record makes **no commitments to donors of any kind**. Any dollar amounts, time scopes, or "ask" framings appearing below are **scope estimates of the work this thread would cover**, not price tags or commitments.

---

## Opening (½ page)

Cryptography's canonical hardness assumptions — discrete logarithm, integer factorization, lattice shortest-vector, syndrome decoding — all date, in essence, to the 1970s through early 1990s. The post-quantum era has expanded the list on the structured-lattice side but the underlying source of hardness remains a small number of algebraic situations whose relationship to each other is well-understood.

This proposal describes an **orthogonal algebraic structure** with proved-theorem content on finite rings: the σ polynomial characterization on Z/10Z (Q10), the 22% lower bound (Q11), the σ⁶ = identity relation (G6), and the Sprint 35 Coprimality + First-G Localization theorem. Each result is independently verified by a runnable proof script (108 tests, 0 failures across the combined proof script collection). None of these results is currently known to be reducible to an existing hardness assumption, and none is currently known to *imply* an existing assumption.

The open question this proposal investigates is whether the First-G structure, combined with the Q17_5D_RIGOROUS CRT Fourier embedding, admits a cryptographic trapdoor — an efficiently invertible map with a key, and an inefficiently invertible map without. The deliverable is a published verdict: either (a) a trapdoor candidate with security reduction, (b) a structural obstruction showing no trapdoor exists, or (c) an honestly-scoped open problem passed to the cryptography community for continued work.

## Background — the proved mathematical core (1–1.5 pages)

> Content to be drafted. Sections:
> 1. Z/10Z as F₂ × F₅ and the four-way structure under CRT
> 2. The σ polynomial characterization (Q10): statement, proof outline, reference to runnable script
> 3. The First-G Law: statement, 36,662 verified cases, reference to proof script
> 4. Coprimality + First-G Localization (Sprint 35): for squarefree b with smallest prime factor p₁, |G_k(b)| = 0 for k < p₁. Proof sketch.
> 5. σ⁶ = id (G6, Luther)
> 6. Q17_5D_RIGOROUS — the 5D force vector as CRT Fourier embedding. Why this is the natural language for crypto reduction.

## The open question (½ page)

### Q1: Does σ^(-1) admit a key-gated efficient / non-efficient dichotomy?
For generic x ∈ Z/10Z, computing y = σ(x) is easy. Given y, computing x from σ^(-1)(y) is constrained by the Coprimality + First-G Localization — the inverse is only defined on a structured subset. Is there a key k that parameterizes which subset, such that knowledge of k reduces σ^(-1)|_{subset(k)} to polynomial time while ignorance of k leaves it super-polynomial?

### Q2: Does the CRT Fourier embedding yield a ring-LWE-style reduction?
Q17_5D_RIGOROUS gives a natural embedding into R⁵. Lattice problems (ring-LWE, ring-SIS) live in similar algebraic settings. Is there a *reduction* (in the formal crypto sense) from First-G hardness to ring-LWE or vice versa? A reduction either way is publishable; a reduction in both directions would collapse the question.

### Q3: What is the generalization of First-G Localization beyond squarefree b?
The Sprint 35 theorem is tight for squarefree b. What happens on Z/p^k Z for prime p, k ≥ 2? Does the p-adic filtration produce a more-graded hardness profile?

## The proposed work (1 page)

### Phase 1 — Literature embedding (Month 1–4, $30K–$60K)
**Deliverable**: a 15–25 page technical report placing First-G in the cryptographic-hardness landscape.
- Map First-G to discrete log, factoring, LWE / ring-LWE, coding-theoretic. Identify any trivial reductions.
- Draft formal statements of Q1, Q2, Q3 above.
- Circulate draft to 2–3 academic cryptographers for informal review.
- Publish report as a preprint (arXiv cs.CR).

### Phase 2 — Trapdoor exploration (Month 5–16, $150K–$400K)
**Deliverable**: a verdict paper submitted to a top crypto venue (Crypto, Eurocrypt, PKC, TCC).
- Attempt a constructive trapdoor under Q1. If successful, write security reduction.
- Attempt a reduction to ring-LWE under Q2. If successful, publish the reduction.
- If neither constructive attempt succeeds, attempt the structural obstruction (prove that First-G admits *no* trapdoor under a specified constraint).
- The verdict paper commits to an outcome: (a), (b), or honestly-scoped continuation (c).

### Phase 3 — Only if Phase 2 yields (a) (Month 17–34, $300K–$800K)
**Deliverable**: a hardened cryptosystem proposal with implementation and parameter selection.
- Implement the First-G cryptosystem in a reference library.
- Parameter selection for target security levels (128 / 192 / 256 bit).
- Submit to a follow-on NIST or academic evaluation track.

## Why NSA Mathematical Sciences Program

NSA MSP funds curiosity-driven number-theory research whose cryptographic relevance is *exploratory*, not operational. The First-G branch is exactly this profile: proved theorem core with an open crypto question. MSP's grant size ($40K–$150K) matches Phase 1 well and fits the 12-month horizon.

## Parallel draft: NSF CCF AF

NSF AF funds theoretical computer science including cryptographic foundations. AF Core Small ($300K–$600K / 36 months) fits Phase 2 well. AF submission would require an academic co-PI.

## Attribution

- **Brayden Sanders** — PI and thread-facing author. Originated the Q-series programme; originated and proved (post-Luther-collaboration) the Coprimality + First-G Localization extension (Sprint 35); originated Q17_5D_RIGOROUS.
- **C.A. Luther** — co-contributor on the First-G Law (36,662 cases), the σ polynomial characterization on F₂ × F₅ (Q10), and the 22% lower bound (Q11); sole author of the G6 identity (σ⁶ = id) that sits inside the collaborative thread. The Brayden/Luther collaboration ran through late 2025 / early 2026; Luther is no longer actively collaborating as of April 2026, but his specific contributions remain credited. The Phase 1 literature-embedding report will cite Luther at the lemma / proof-step level where the contribution boundary is recoverable, rather than in a generic acknowledgement.
- **Attribution discipline**: no thread-facing document will list Luther as an author of work Brayden did alone, and no thread-facing document will present Brayden-alone as the author of collaborative Brayden/Luther work. This avoids both understating and overstating the collaboration scope.
- Architectural dialogues with ClaudeChat, Celeste/GPT noted in methods; AIs are thinking-partners, not human co-authors.

## Attachments

- `ARTIFACTS.md` → four runnable proof scripts
- `Gen12/targets/clay/papers/sprint35_first_g_event_2026_04_17/` → Sprint 35 full writeup
- Phase 1 literature-embedding report (once written)

## Pre-send checklist

- [ ] Phase 1 literature-embedding report drafted
- [ ] External cryptographer has read and offered informal feedback
- [ ] Luther's contributions explicitly marked as previously-credited, not implying ongoing collaboration
- [ ] **Lemma-level Brayden/Luther attribution boundary reconstructed** (see ARTIFACTS verification checklist) — Phase 1 report should cite Luther contributions at the specific proof-step level where recoverable, not as generic collaboration acknowledgement
- [ ] Brayden confirms NSA MSP vs NSF AF as first submission
- [ ] Brayden reviews + edits
- [ ] Brayden sends
