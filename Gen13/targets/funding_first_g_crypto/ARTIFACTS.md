# ARTIFACTS — funding/first-g-crypto

Exact file paths and verification status. This branch is distinct from SNOWFLAKE in that the core mathematical results are **already proved and in the repo** — the thread-facing work is assembling them into a crypto-research narrative, not recovering anything.

---

> **Note (2026-04-25 revision).** This file was originally drafted as part of a pitch-style packet. Per the operator-of-record's actual stance documented at [`FUNDING.md`](../../../FUNDING.md) (root) and [`INTENT_STATEMENT.md`](../../../INTENT_STATEMENT.md), this is **thread documentation**, not a fundraising pitch. The operator-of-record makes **no commitments to donors of any kind**. Any dollar amounts, time scopes, or "ask" framings appearing below are **scope estimates of the work this thread would cover**, not price tags or commitments.

---

## Runnable proof scripts (already in repo)

### 1. First-G Law verification
- **Path**: `papers/proof_first_g_law.py`
- **Status**: runnable, green
- **Output**: 36,662 cases verified
- **Run time**: ~2 minutes on R16
- **Invocation**: `python papers/proof_first_g_law.py`

### 2. sinc² Zero Law (all primes 3..199)
- **Path**: `papers/proof_d25_loop_closure.py`
- **Status**: runnable, green
- **Output**: verification across all primes in 3..199
- **Invocation**: `python papers/proof_d25_loop_closure.py`

### 3. σ rate theorem
- **Path**: `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/proof_sigma_rate.py`
- **Status**: runnable, green
- **Claim**: σ(N) ≤ C/N
- **Invocation**: `python Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/proof_sigma_rate.py`

### 4. Clay rotation framework
- **Path**: `papers/proof_clay_rotation.py`
- **Status**: runnable, green
- **Output**: 43/43 framework items verified
- **Invocation**: `python papers/proof_clay_rotation.py`

---

## Mathematical source documents (already in repo)

### 5. σ polynomial on F₂ × F₅ (Z/10Z) — Q10
- **Path**: `old/Gen10/papers/Q10_sigma_polynomial_characterization.md` (or variant filename)
- **Status**: proved writeup
- **Attribution**: **Brayden + C.A. Luther collaboration** (σ polynomial form on F₂ × F₅; Q-series foundation; Luther contributed spectral-layer / algebraic-structure work on the characterization)

### 6. 22% lower bound — Q11
- **Path**: `old/Gen10/papers/Q11_lower_bound_22pct.md` (or variant filename)
- **Status**: proved writeup
- **Attribution**: **Brayden + C.A. Luther collaboration** (lower-bound argument drew on the spectral structure from the Luther-collaboration thread)

### 7. σ⁶ = id for G6 — Luther spectral layer
- **Path**: referenced in `old/Gen10/` Luther archive; specific filename in Luther spectral-layer folder
- **Status**: proved
- **Attribution**: **C.A. Luther** (G6 identity is the cleanest-demarcated Luther-origin result within the broader Brayden/Luther collaboration; Luther previously-credited; no longer actively collaborating as of April 2026)

### 8. Q17_5D_RIGOROUS (5D force vector as CRT Fourier embedding)
- **Path**: `old/Gen10/papers/Q17_5D_RIGOROUS.md` (or equivalent)
- **Status**: proved
- **Relevance**: this is the connection point to lattice cryptography — the CRT embedding gives a natural way to sit First-G inside ring-LWE-adjacent territory

### 9. Coprimality + First-G Localization — Sprint 35
- **Path**: `Gen12/targets/clay/papers/sprint35_first_g_event_2026_04_17/`
- **Status**: proved (2026-04-17)
- **Content**: for squarefree b with smallest prime factor p₁, |G_k(b)| = 0 for k < p₁
- **Attribution**: Brayden (post-Luther-collaboration extension; extends the Brayden + Luther collaborative First-G Law to a tighter structural statement. Any co-authors listed in the sprint folder's authors list apply.)

### 10. Canonical tables (TSML / BHML / CL)
- **Path**: `papers/ck_tables.py`
- **Status**: reference data, not a proof
- **Use**: the 73-cell TSML and 28-cell BHML tables are the operational side of the First-G structure; any crypto pitch will want to quote counts from these tables

---

## Verification checklist (before any pitch)

- [ ] Run all four proof scripts on a fresh environment, confirm all pass
- [ ] Record exact output (case counts, runtime) in a reproduction log
- [ ] Locate Luther's G6 writeup in `old/Gen10/` and confirm provenance header is present
- [ ] **Reconstruct the First-G / Q10 / Q11 collaboration boundary**: locate Brayden/Luther correspondence or commit history from late 2025 / early 2026 that distinguishes which specific lemmas / proof steps / polynomial forms came from which collaborator. This matters because the thread-facing Phase 1 literature-embedding report must cite the Luther contributions at the lemma level, not just as a general acknowledgement.
- [ ] Confirm Q17_5D_RIGOROUS filename and path; if filename drifts during archive cleanup, update this doc
- [ ] Write a one-page literature-embedding doc mapping First-G structure to existing crypto hardness landscape (discrete log, factoring, lattice, coding)
- [ ] Verify Sprint 35 theorem statement matches what is in the paper (the "for squarefree b, smallest prime factor p₁" statement above)

---

## Line-count summary

| File | LOC / pages | Status |
|---|---|---|
| `papers/proof_first_g_law.py` | ~300 lines (to verify) | runnable |
| `papers/proof_d25_loop_closure.py` | ~200 lines (to verify) | runnable |
| `Gen12/targets/clay/papers/sprint14_.../proof_sigma_rate.py` | ~250 lines (to verify) | runnable |
| `papers/proof_clay_rotation.py` | ~400 lines (to verify) | runnable |
| Sprint 35 folder | (multiple files, to inventory) | proved |
| Q10 / Q11 / Q17_5D_RIGOROUS | (markdown writeups) | proved |
| Luther G6 | (markdown in old/Gen10/) | proved |

Exact LOC numbers to be filled in during Phase 1 verification run; the numbers will go into PITCH_DRAFT.

## Missing from repo (blockers for Phase 1)

- **Literature-embedding doc**: does not yet exist. Must be written.
- **Dissertation-grade narrative**: does not yet exist. Must be written as part of PITCH_DRAFT Phase 1.
- **External cryptographer's opinion**: no academic has yet read the First-G theorem and offered an evaluation. Even an informal email from a senior cryptographer is high-value for the pitch.
- **Lemma-level Brayden/Luther attribution reconstruction**: see Verification Checklist item above. The broader collaboration is known, but the Phase 1 report should cite Luther contributions at the lemma/proof-step level where recoverable, to avoid either understating or overstating Luther's specific role.
