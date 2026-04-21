# funding/first-g-crypto

**Track C — First-G Cryptographic Hardness**
**Primary funder pool:** NSA MSP · NSF AF (Algorithmic Foundations) · Simons Foundation · academic cryptographer partnerships
**Status:** Pre-pitch. **Strongest PROVED-theorem branch** of the funding set: First-G Law (36,662 cases), σ polynomial on F₂×F₅ (Q10), 22% lower bound (Q11), σ⁶ = id (G6), Q17 5D force vector as CRT Fourier embedding, Coprimality + First-G Localization (Sprint 35). All runnable; 108 tests, 0 failures.
**Branch accumulates to:** `master` (every commit cherry-picked) · **Rigor base:** `tig-synthesis` (the GitHub default branch)

---

## One-paragraph pitch

Modern cryptography rests on a short list of hardness assumptions — discrete log, integer factorization, lattice shortest-vector, coding-theoretic decoding. Each has been studied for decades and each is well-understood, which is both their strength (known hard) and their vulnerability (known attack surface). The **First-G cryptographic hardness program** proposes an *algebraic* hardness candidate drawn from proved theorems on finite rings: the Coprimality + First-G Localization on $\mathbb{Z}/n\mathbb{Z}$, combined with the σ polynomial characterization on $\mathbb{Z}/10\mathbb{Z}$ (Q10) and the σ⁶ = id identity (G6). The open question is whether inverting the First-G structure under a constrained-input regime produces a trapdoor. This branch packages the proved mathematical core — not an implementation — and asks a cryptography-research funder to fund the **12-month investigation of whether a trapdoor exists**.

## Proved mathematical core (funder-facing)

| Result | Status | Attribution | Verification |
|---|---|---|---|
| First-G Law | **PROVED**, 36,662 cases verified | Brayden + Luther collaboration | `papers/proof_first_g_law.py` |
| σ polynomial on $F_2 \times F_5$ | **PROVED** (Q10) | Brayden + Luther collaboration | `old/Gen10/papers/Q10_*.md` |
| 22% lower bound on σ | **PROVED** (Q11) | Brayden + Luther collaboration | `old/Gen10/papers/Q11_*.md` |
| σ⁶ = id for G6 | **PROVED** (G6) | Luther (spectral layer) | Luther spectral-layer archive |
| Q17 5D force vector as CRT Fourier embedding | **PROVED** | Brayden (post-collaboration) | `old/Gen10/papers/Q17_5D_RIGOROUS.md` |
| Coprimality + First-G Localization | **PROVED** (Sprint 35) | Brayden (post-collaboration) | `Gen12/targets/clay/papers/sprint35_first_g_event_2026_04_17/` |
| sinc² Zero Law | **PROVED**, all primes 3..199 | Brayden | `papers/proof_d25_loop_closure.py` |

All proof scripts run in under a second: `python papers/proof_first_g_law.py`, `python papers/proof_d25_loop_closure.py`, `python papers/proof_sigma_rate.py`, etc.

## Attribution note

The First-G Law and the Q-series polynomial characterization (Q10, Q11) are products of a **Brayden Sanders / C. A. Luther collaboration** that ran from late March 2026 through mid-April 2026. G6 (σ⁶ = id) is the most cleanly-demarcated Luther-origin result. Luther is no longer actively collaborating as of April 2026; contributions remain credited per the never-delete policy. Sprint 35's Coprimality + First-G Localization tightening is Brayden's post-collaboration extension (2026-04-17).

## What this branch does NOT claim

- A new public-key cryptosystem (the ask is for *investigation*, not a product pitch).
- Quantum-resistance without explicit reduction (the structural hardness question is open; no hardness-preserving reduction has been published).
- A finished cryptanalytic attack on existing schemes (the Q17 Fourier embedding *is* a genuine structural result but its cryptographic consequences are the object of the funded study).

## What's in this branch

Branch-specific funder-pitch files under [`Gen13/targets/funding_first_g_crypto/`](Gen13/targets/funding_first_g_crypto/):

- [`README.md`](Gen13/targets/funding_first_g_crypto/README.md) — deep pitch document
- [`FUNDERS.md`](Gen13/targets/funding_first_g_crypto/FUNDERS.md) — prioritized funder list with contact notes
- [`ARTIFACTS.md`](Gen13/targets/funding_first_g_crypto/ARTIFACTS.md) — runnable proof scripts + papers
- [`PITCH_DRAFT.md`](Gen13/targets/funding_first_g_crypto/PITCH_DRAFT.md) — full pitch draft (NSA MSP primary + NSF AF parallel)
- [`LIMITATIONS.md`](Gen13/targets/funding_first_g_crypto/LIMITATIONS.md) — honest-scope items
- [`STATUS.md`](Gen13/targets/funding_first_g_crypto/STATUS.md) — readiness checklist + blockers

## The project this branch is a track of

Branch C of the 10-branch funding architecture. For the full project overview, see **`tig-synthesis`**:

→ https://github.com/TiredofSleep/ck/tree/tig-synthesis

## License

7Site Public Sovereignty License v1.0 — human use only, no commercial, no military, free forever. Full text in [`LICENSE`](LICENSE).

---

*Branch maintained as part of the 10-branch funding architecture. Commits here get cherry-picked to master per the trunk workflow. Branch-level changes do not propagate to `tig-synthesis` unless they are referee-ready.*
