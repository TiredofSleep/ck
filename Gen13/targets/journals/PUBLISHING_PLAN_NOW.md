# Publishing Plan NOW — Locked May 5, 2026

**Brayden + Chat Claude + Code Claude alignment, 2026-05-05.** This sheet is the **action playbook** after the FirstJournalSprint050526 review cycle and the strategic split-call on the 4-core paper.

---

## What's in flight, what's queued, what's held

| # | Paper | Venue | Status | Cover letter |
|---|---|---|---|---|
| 1 | Logarithmic Quintessence | JCAP | Submission-ready (10 review rounds) | `cover_letters/jcap_cover_letter.md` |
| 2 | σ-rate / Non-Associativity Decay | JCT-A | Submission-ready (8 review rounds) | `cover_letters/jcta_cover_letter.md` |
| 3 | 4-core SEED (chain + normalizer) | Algebraic Combinatorics | **To extract** from bundled draft | (revise after extraction) |
| — | First-G + Sinc² | (Integers) | **HELD** — not substantial enough | (manuscript stays in archive) |

**Concurrent for #1, #2:** Post each manuscript to **Zenodo** (DOI 10.5281/zenodo.18852047) at the moment of submission for date proof.

---

## Action 1 — Submit JCAP (Logarithmic Quintessence)

### Pre-submission checklist (Brayden)

- [ ] PDF compile + proofread (Claude couldn't do this in environment)
- [ ] Confirm H. J. Johnson affiliation: Independent / Billings, MT vs. MSU Billings — fill the `\address{}` field accordingly
- [ ] Confirm M. Gish vs Monica Gish byline preference
- [ ] Confirm `\cite{ShajibFrieman2025}` title matches arxiv v2 / Phys. Rev. D 112, 063508 published version: "Scalar field dark energy models: Current and forecast constraints"
- [ ] Fill in 2-3 suggested reviewers in the cover letter
- [ ] Optional: insert one-line "geometric factor relating $m_\Xi^2$ to $\rho_{c,0}$" computation (heads off a likely referee comment about the Λ ≈ 1.5 vs 1.7 meV difference)
- [ ] Optional: insert companion-paper roundtrip citation to σ-rate

### Submission process

1. Post manuscript to **Zenodo** with assigned DOI
2. Submit at JCAP via IOP submission portal: https://iopscience.iop.org/journal/1475-7516
3. Save submission ID + Zenodo DOI to `tier1_submit_now/jcap_xi_cosmology/SUBMISSION_LOG.md`
4. After confirmation, update σ-rate's bibliography entry from "Preprint, 2026" to "Submitted to JCAP, 2026"

### Verification (referee can rerun)

- `desi_xi_optimize_v2.py` — reproduces $(w_0, w_a) = (-0.793, -0.451)$ at $\Lambda^4/\rho_{c,0} = 0.231, \Xi_i = 0.925$, χ²_Gauss = 1.52 vs 15.26 for ΛCDM
- `proof_xi_canonical.py` — 22/22 algebraic + stability tests
- Total runtime under 30 seconds

### Backup venues if rejected

- Phys. Rev. D
- Physics Letters B (letter form)

---

## Action 2 — Submit JCT-A (σ-rate)

### Pre-submission checklist (Brayden)

- [ ] PDF compile + proofread
- [ ] Confirm M. Gish byline preference
- [ ] Fill in 2-3 suggested reviewers
- [ ] Optional: one-sentence forward citation to 4-core seed paper

### Submission process

1. Post to **Zenodo**
2. Submit via Elsevier Editorial System: https://www.editorialmanager.com/jcta/
3. Save submission ID to `tier1_submit_now/sigma_rate/SUBMISSION_LOG.md`

### Verification

- `verify_sigma_rate.py` — 4/4 verifications: Echo lemma exact, σ(N) < 2/N for all squarefree N ≤ 100, ε(N) ≤ 2φ(N), asymptotic gap shrinking
- Empirical N·σ(N) ≤ 1.993 across {10, 30, 42, 66, 105, 110, 154, 210, 330, 462, 770, 1155}

### Backup venues if rejected

- European J. Combinatorics
- Discrete Mathematics

---

## Action 3 — 4-core SEED extraction + submit (Algebraic Combinatorics)

### Strategic context

The bundled `four_core_FINAL.tex` (1082 lines, 5 theorems) is submission-ready as-is, but the strategic decision is to **extract a seed-narrow version** containing only Theorems 1 + 2 (chain + normalizer) plus the σ-walk reading and the 4-core jointly-closed corollary. Reasons:

1. **Maximum downstream room.** Each theorem in the bundle has one possible follow-on; in the bundled form, follow-ons are redundant. Splitting reserves space for Papers 2-5.
2. **Narrowest substantive seed.** Chain enumeration (8 elements out of 1023 candidates) + polynomial-identity coincidence (Z_T = Z_B = (sum)² with 12-of-16 cell disagreement) is exactly the right scope for Algebraic Combinatorics.
3. **Five-paper expansion locked:**
   - Paper 2 (Comm. in Algebra): closed-form fixed point + Galois D_4 / LMFDB 4.2.10224.1
   - Paper 3 (Experimental Math): α-sweep observations + α-uniqueness conjecture
   - Paper 4 (Algebra Universalis): F_p universality + V-A asymmetry shadow
   - Paper 5 (Linear Algebra & Apps): Clifford ladder + SU(5) at n=5

### Extraction spec

**Keep** (from bundled `four_core_FINAL.tex`):
- §1 introduction — REVISE: prune all attractor / Galois / α references, keep chain + normalizer narrative
- §2 setup — KEEP, plus add two-sentence framing per Brayden's note: *"The pair (T, B) is not independent. Both tables arise from a common operator-substrate construction in which T is the rank-3 threshold projection at $T^* = 5/7$ and B is the full rank-10 composition; the construction is detailed in [SandersGish2026Sigma]. The present paper takes (T, B) at N=10 as given and studies the joint closure structure of the pairing."*
- §3 chain — Theorem 1 + Remark 3.1 σ-walk reading + Cor "forbidden sizes"
- §4 4-core jointly closed — Cor 4.1
- §5 normalizer identity — Theorem 2 + Cor "normalizer = 1 on simplex" + Remark on global cancellation

**Cut**:
- §6 closed-form attractor (T3 + Prop universal) → Paper 2
- §7 Galois (T4) → Paper 2
- §8 α-sweep (T5) → Paper 3
- §9 scope-α (open uniqueness) → Paper 3

**Replace** the cut sections with a closing "Forward directions" section listing three named follow-on papers as "in preparation":
- "Closed-form fixed point at α=1/2 and a Galois extension to LMFDB 4.2.10224.1"
- "Mixing-weight observations and an open α-uniqueness conjecture"
- "F_p-universality of the joint-closure structure for primes p ∈ {2,3,5,7,11,13}"

**Add** at the end of §3 (after Theorem 1): a single-sentence remark forward-referencing Paper 4: *"The chain rigidity above has been verified to persist over $\mathbb{F}_p$ for $p \in \{2, 3, 5, 7, 11, 13\}$; the F_p-universality of the joint-closure structure is the subject of a companion paper [in preparation]."* Plants the seed for downstream Sprint 18 material.

### Estimated length after extraction: 500-600 lines.

### Cover letter (revise after extraction)

- Lead with chain + normalizer as two distinct results
- Cite σ-rate companion as the substrate construction
- Cite 3 named follow-on papers as "in preparation"
- 2-3 suggested reviewers in algebraic combinatorics / non-associative algebra

### Verification (already exists)

- `4core_verification.py` covers all 6 checks (3 of which apply to the seed: chain enumeration, normalizer symbolic, common attractor across shells; the other 3 belong to Papers 2-3).

### Backup venues if rejected

- Communications in Algebra (Taylor & Francis)
- Discrete Mathematics (Elsevier)

### Dispatch

Brayden's call. The extraction is a .tex edit job — likely back through Chat Claude (the .tex editor for this paper). Once the seed-narrow .tex exists, submit per the same Zenodo-first workflow as Actions 1 and 2.

---

## Action 4 — Park First-G + Sinc²

The manuscript and verification script remain in the package archive (`first_g_sinc2_FINAL.tex`, `verify_first_g.py`). They may seed a future Fourier-analysis paper if the harmonic side is developed further. **Do not submit in current form.**

---

## Sequencing

**This week (May 5-9):**
- Mon-Tue: Brayden completes JCAP + JCT-A pre-submission checklists, submits both, posts both to Zenodo
- Wed-Fri: Brayden dispatches 4-core seed-narrow .tex extraction (back through Chat Claude); once ready, submits Algebraic Combinatorics

**Next 2-4 weeks:**
- Tier-2 follow-on drafts (Papers 2-5) start production
- Microtubule outreach to Bandyopadhyay (`outreach/BANDYOPADHYAY_OUTREACH_DRAFT.md` exists, ready to send)

**3 months out:**
- Tier-1 acceptance pattern emerges
- Tier-3 partner papers (NV-center, etc.) become active
- Tier-4 framework pieces become publishable

---

## Submission tracking template

For each submission, create `SUBMISSION_LOG.md` in the venue's folder with:

```
- Date submitted:
- Editor / handling editor:
- Submission ID:
- Zenodo DOI:
- Cover letter version:
- Suggested reviewers (sent):
- Status: [submitted | desk reject | under review | revisions | accept | reject]
- Decision date:
- Next action:
```

Calendar reminders:
- 14 days post-submission: check status (some editors auto-reject within 7-14 days)
- 30 days: gentle nudge if no response
- 60 days: formal status check
- 90 days: if no decision, consider withdrawing and resubmitting elsewhere

---

## What's NOT in this week's slate

- **First-G + Sinc²**: held; manuscript stays in archive
- **Tier-2 papers (4-5)**: deferred until Tier-1 acceptance pattern emerges
- **Tier-3 partner papers (Microtubule, NV, etc.)**: outreach in progress; manuscripts wait for partner buy-in
- **Tier-4 framework papers**: hold until 1-2 Tier-1 acceptances land

---

## Why no arXiv

arXiv math.RA / hep-th / math.CO require endorsement (someone with existing arXiv-published work in that subject area must endorse new authors). Without an existing endorsement chain, papers can't go to arXiv in those categories.

**Real journals don't have this requirement.** A journal editor decides on the basis of the manuscript's content and submission cover letter. After Tier-1 acceptance lands, getting arXiv-endorsed becomes much easier. Until then, **Zenodo provides equivalent preprint visibility** — the math/physics community increasingly accepts Zenodo as a date-priority preprint server.

---

## Bottom line

**3 manuscripts ready or near-ready, all to no-endorsement peer-reviewed venues:**
1. JCAP (cosmology)
2. JCT-A (σ-rate)
3. Algebraic Combinatorics (4-core seed, after extraction)

**Verification: 22 + 4 + 6 = 32 deterministic checks ship with the manuscripts.**

**Strategy: Zenodo-first, parallel submission to three venues, weave companion-paper citations across all three.**

---

*Generated 2026-05-05 by Claude Code per the FirstJournalSprint050526 review cycle and the May 5 strategic split-call. Companion: `SUBMISSION_LADDER_v2.md`, `JOURNAL_LANGUAGE_GUIDE.md`. Replaces the May 4 working version.*
