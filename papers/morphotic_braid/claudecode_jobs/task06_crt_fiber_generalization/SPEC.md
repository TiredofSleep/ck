# Task 06 — CRT (1,1)-fiber avoidance: does it generalize?

**Tier:** 3 (research — days of setup)
**Parent handoff:** `../CLAUDECODE_HANDOFF_MIN_BUMP.md` §Task 6

## Goal

TSML avoids the (ε=1, ε=1) CRT fiber on ℤ/10 = ℤ/2 × ℤ/5. Test whether analogous TSML-like tables on N ∈ {14, 22, 34} (= 2p for small primes p) also consistently avoid the (1,1) fiber.

## Method

1. Build TSML analogues on N ∈ {14, 22, 34} using `FORMULAS_AND_TABLES.md` §7 construction rules **adapted for general N** (this adaptation is non-trivial; may require sprint-paper consultation or Jay's input).
2. Identify bump cells (cells where table deviates from pure C_0 on ℤ/N).
3. For each bump cell (a,b), compute (a mod 2, b mod p) and tabulate.
4. Check whether the (1,1) CRT fiber is consistently empty across all three N values.

## Success criterion

**Either:**
- **Generalization theorem:** "For N = 2p (p odd prime), the TSML construction avoids the (1 mod 2, 1 mod p) CRT fiber." — publishable structural law.
- **Counterexample:** a specific N and a specific bump cell in the (1,1) fiber — downgrades the observation to a N=10-specific coincidence.

## Expected runtime

Moderate compute, but the setup (extending §7 construction to general N) is the hard part. Days of reading and thinking before the compute is defined.

## Deliverable

`papers/morphotic_braid/results/task06_crt_fiber_result.md`:
- definition of TSML_N for each tested N
- bump cell list per table
- CRT fiber tally
- verdict (generalizes / counterexample)

## Note

This task may require consulting the sprint papers or additional Jay input to define the construction correctly for N > 10.

**Tag:** `[RESEARCH TASK — TIER 3]`
