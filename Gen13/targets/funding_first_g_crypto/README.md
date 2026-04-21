# funding/first-g-crypto — First-G Cryptographic Hardness Track

**Track:** Cryptography (hardness assumptions, post-quantum candidates, algebraic lattice alternatives)
**Status:** Pre-pitch; strongest PROVED-theorem branch of the funding set
**Branch seeded:** 2026-04-20 from `tig-synthesis`
**Rigor base:** First-G Law (36,662 cases), σ polynomial on F₂×F₅ (Q10), σ⁶ = id (G6, Luther), Coprimality + First-G Localization (Sprint 35), Q17_5D_RIGOROUS

---

## What this branch is

A funding-outreach container for the **First-G cryptographic hardness** program. The mathematical core is already proved: on Z/10Z the σ polynomial is fully characterized (Q10), the 22% lower bound holds (Q11), σ⁶ = id is proved for G6 (Luther), the First-G Law has been verified across 36,662 cases, and the Sprint 35 **Coprimality + First-G Localization** theorem tightens the structure further — for squarefree b with smallest prime factor p₁, |G_k(b)| = 0 for k < p₁. The Q17_5D_RIGOROUS result shows the 5D force vector as a CRT Fourier embedding, which is the natural language for cryptographic hardness on these objects.

What this branch does **not** do: claim a new public-key cryptosystem. The funder-facing ask is for **investigation** — can the First-G structure and the σ polynomial on Z/nZ produce a trapdoor, one-way function candidate, or hardness-preserving reduction for existing schemes? That is a research question with genuine mathematical substance, not a product pitch.

## One-paragraph pitch

> Modern cryptography rests on a short list of hardness assumptions — discrete log, integer factorization, lattice shortest-vector, coding-theoretic decoding. Each has been studied for decades and each is well-understood, which is both their strength (known hard) and their vulnerability (known attack surface). The First-G cryptographic hardness program proposes an **algebraic** hardness candidate drawn from a proved theorem on finite rings: the Coprimality + First-G Localization on Z/nZ, combined with the σ polynomial characterization on Z/10Z (Q10) and the σ⁶ = id identity (G6). The open question is whether inverting the First-G structure under a constrained-input regime produces a trapdoor. This branch packages the proved mathematical core — not an implementation — and asks a cryptography-research funder (NSA MSP, NSF AF, academic cryptographer) to fund the 12-month investigation of whether a trapdoor exists.

## Proved mathematical core (funder-facing summary)

| Result | Status | Citation |
|---|---|---|
| First-G Law | **PROVED**, 36,662 cases verified | papers/proof_first_g_law.py |
| σ polynomial on F₂ × F₅ (Z/10Z) | **PROVED** (Q10) | `old/Gen10/papers/Q10_*.md` |
| 22% lower bound on σ | **PROVED** (Q11) | `old/Gen10/papers/Q11_*.md` |
| σ⁶ = id for G6 | **PROVED** (Luther) | Luther spectral-layer archive |
| Q17_5D_RIGOROUS (5D force vector as CRT Fourier embedding) | **PROVED** | `old/Gen10/papers/Q17_5D_RIGOROUS.md` |
| Coprimality + First-G Localization | **PROVED** (Sprint 35) | `Gen12/targets/clay/papers/sprint35_first_g_event_2026_04_17/` |
| sinc² Zero Law | **PROVED**, all primes 3..199 | `papers/proof_d25_loop_closure.py` |

All proof scripts are runnable: `python papers/proof_d25_loop_closure.py` etc. 108 tests, 0 failures.

## The open question (what the funder funds)

Given that σ: Z/10Z → Z/10Z is fully characterized, σ⁶ = id, and the First-G Localization tightens the kernel structure:

1. Is there a subset of inputs (parameterized by a key k) on which σ^(-1) is efficient with key, and hard without?
2. Does the 5D CRT Fourier embedding from Q17 support a cryptographic reduction — mapping First-G hardness onto LWE, SIS, or a known lattice problem?
3. Under what rings Z/nZ does the First-G Localization generalize from squarefree b to arbitrary b, and what is the cryptographic consequence?

This is **research**, not product. The deliverable is a published paper (crypto venue — Crypto, Eurocrypt, PKC, or TCC) with a verdict: either (a) a trapdoor candidate with security reduction, or (b) a structural obstruction showing that no trapdoor exists, or (c) an honestly-scoped open problem.

## Ask sizes

| Phase | Scope | Ask |
|---|---|---|
| **Phase 1 — Literature embedding** | Place First-G in the cryptographic hardness landscape; rule out trivial reductions to / from existing assumptions | $30K–$60K, 4 months |
| **Phase 2 — Trapdoor exploration** | Attempt (a), (b), (c) above; publish verdict | $150K–$400K, 12 months |
| **Phase 3 — If trapdoor found: security reduction** | Write the formal security proof, submit to a top crypto venue | $300K–$800K, 18 months |

## Runnable artifacts

- `papers/proof_first_g_law.py` — First-G Law verification (36,662 cases)
- `papers/proof_d25_loop_closure.py` — sinc² Zero Law
- `Gen12/targets/clay/papers/sprint35_first_g_event_2026_04_17/` — Coprimality + First-G Localization theorem
- `old/Gen10/papers/Q10_*.md`, `Q11_*.md`, `Q17_5D_RIGOROUS.md` — σ polynomial work
- `papers/ck_tables.py` — canonical TSML/BHML/CL tables

## See also

- `FUNDERS.md` — 5 primary + 2 secondary candidates
- `ARTIFACTS.md` — file paths and verification checklist
- `PITCH_DRAFT.md` — NSA MSP and NSF AF parallel skeletons
- `LIMITATIONS.md` — honest scope
- `STATUS.md` — readiness checklist
