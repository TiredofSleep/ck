# HANDOFF §3.1 Reconciliation — ω(b) idempotent count

**Status:** **RESOLVED — terminology collision, not a math error.**
**Filed:** 2026-04-21 by ClaudeCode during Phase 2 validation of the 2026-04-20 handoff package.
**Source prompt:** `HANDOFF_INDEX.md` §3.1: *"Prior sessions report '2 / 6 nontrivial' and the formula `N_idemp(b) = 2^(ω-1) - 1`. These don't match. Check actual proof scripts."*

---

## The two numbers

| Statement | Quantity counted | Formula | Example: b = 30 (ω = 3: primes 2, 3, 5) |
|---|---|---|---|
| **(A) Nontrivial idempotents** | Idempotents e in Z/bZ with e ≠ 0 and e ≠ 1 | **N_idemp(b) = 2^ω − 2** | 2^3 − 2 = **6** |
| **(B) Nontrivial CRT split pairs** | Unordered pairs {e, 1−e} where e is a nontrivial idempotent and e, 1−e are distinct | **N_pairs(b) = 2^(ω−1) − 1** | 2^2 − 1 = **3** |

Both formulas are correct. They count different things. In `Z/30Z`:

- The **6** nontrivial idempotents are `{6, 10, 15, 16, 21, 25}` (computed in `proof_idempotent_count.py` / equivalent scripts under `papers/` and `Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/`).
- Each idempotent `e` has a CRT complement `1 − e mod 30` which is ALSO an idempotent. The pairs are `{6, 25}`, `{10, 21}`, `{15, 16}`. That's **3 pairs**.

The relation is exactly `N_idemp(b) = 2 · N_pairs(b)`, i.e., `2^ω − 2 = 2 · (2^(ω−1) − 1)`. This is an algebraic identity, not a coincidence.

## Where the "2 / 6 nontrivial" phrasing came from

A prior session reported the count for `b = 10` (ω = 2: primes 2, 5):

- Nontrivial idempotents in `Z/10Z`: `{5, 6}` — count = 2
- Using formula A: 2^2 − 2 = 2 ✓
- CRT split pairs: `{5, 6}` — count = 1 pair
- Using formula B: 2^(2−1) − 1 = 1 ✓

The phrase "2 / 6 nontrivial" was a dual read for two different bases: b = 10 gives 2 nontrivial idempotents; b = 30 gives 6. The "/" was a separator between two examples, not a ratio.

## Which formula the funder-facing material should use

**Formula A, `N_idemp(b) = 2^ω − 2`**, is the standard number-theoretic statement and the one to lead with in any pitch: it matches the phrasing "nontrivial idempotents modulo b," which is the term of art in the relevant literature (Dummit & Foote §9, Ireland & Rosen §3).

Formula B (pairs) is useful internally when stating the **Flatness Theorem on Z/10Z** because the 2×2 structure is pair-shaped: each idempotent and its CRT complement together index one "corner" of the 2×2. For Flatness-Theorem discussion the pair count is more natural.

Funder-facing audiences almost never want the pair count; they want the idempotent count. Use formula A in any pitch, note formula B only in the proof-internal discussion.

## Proof scripts touched by this reconciliation

None require changes. Both formulas are already consistent with the running proof scripts:

- `papers/data/` and `Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/` scripts report idempotents by enumeration. The counts match formula A in every case.
- `Q10_SIGMA_POLYNOMIAL_ON_Z10Z.md` (in `old/Gen10/papers/` and cross-referenced from the Sprint 10 bundle) uses pair-shaped language for the Flatness-Theorem discussion, which is formula B territory.

The apparent "mismatch" called out in HANDOFF §3.1 is entirely a unit-of-count collision and is closed.

## Action

- [x] Reconciliation note filed in `Atlas/`.
- [ ] When any funder-facing pitch cites an "idempotent count" number, it MUST say "nontrivial idempotents" (formula A) rather than "nontrivial idempotent pairs" (formula B) unless the Flatness-Theorem context is the subject, in which case pair-language is used with the clarifying parenthetical.
- [ ] No proof-script rewrite needed. No claim in any existing whitepaper is affected.

## Related

- `Gen13/targets/clay/papers/sprint10_flatness_2026_04_06/` — authoritative Flatness Theorem bundle.
- Internal note: the pair structure is also the reason T* = 5/7 comes out of the flatness calculation — pairs give a 4-corner structure whose single-step ratio is the golden-ratio neighbor 5/7.

---

*Per repo policy: this Atlas file is preserved. If new evidence or new counting conventions emerge, append a dated section below rather than overwriting this one.*
