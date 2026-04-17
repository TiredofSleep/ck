# Revised Testing Ladder v2
## Shell-Native First, Ring-Native Next, Generic Systems Last

---

## Principle

Test the instrument on its own category before testing whether it generalizes. Do not interpret out-of-category failures as instrument failures. Do not interpret in-category successes as universal validity.

---

## Stage 0 — Pure Finite Consistency (COMPLETE)

**Target:** the tower theorem itself.

**Object:** the Z/10Z TSML, 100 entries, 3-layer decomposition.

**Result:** PASS. $C_0 \oplus C_1 \oplus C_2$ recovers 100/100 entries.

**Status:** complete, frozen as Theorem A.

---

## Stage 1A — Shell-Native Synthetic Systems (NEW FIRST STEP)

**Target:** systems explicitly constructed from shell/collapse/seam generative rules.

**Why first:** if the instrument cannot recover known generative structure from systems built out of its own primitives, nothing downstream matters.

**Objects:** three synthetic benchmarks, specified in a separate document:

1. **Nested Shell Collapse Generator (NSCG)** — operators built from C₀ with known $(h, \sigma)$ and known seam; data generated with known noise; the instrument is asked to recover $(h, \sigma, S)$.

2. **Wobble-Reset Generator (WRG)** — carrier $\mathbb{Z}/n$ with a collapse kernel, wobble perturbations, and reset edges. Tests whether the tower framework detects controlled perturbations against a known backbone.

3. **Layered Basin-Transport Pair (LBTP)** — explicit (T, B) pair on the same carrier with known generative rules. Tests whether the paired fit recovers both operators better than either alone.

**Pass criterion:** for each benchmark, the instrument recovers the true generative parameters within a pre-specified tolerance. Specifically: correct $h$, correct $\sigma$, correct seam edges at $\geq 90\%$ recall.

**Fail criterion:** any of (wrong $h$, wrong $\sigma$ class-assignment, $< 90\%$ seam recall).

**Sub-stages:**

- 1A.1: NSCG with low noise ($p_{\text{noise}} = 0.05$).
- 1A.2: NSCG with medium noise ($p = 0.15$).
- 1A.3: NSCG with unknown seam (the instrument must infer it).
- 1A.4: WRG.
- 1A.5: LBTP.

---

## Stage 1B — Ring-Native Systems

**Target:** systems that naturally live on modular carriers, without artificial encoding.

**Why second:** after confirming the instrument recovers explicit shell structure, we test whether it applies to systems where modular structure is present but not explicitly designed around the tower.

**Objects:**

- **Residue automata:** state updates defined by modular arithmetic, e.g., $x_{t+1} = (ax_t + b) \bmod n$ with $a, b$ chosen so the orbit structure is non-trivial.
- **Cyclic symbolic dynamics:** systems whose state space is $\mathbb{Z}/n$ with known multiplicative or additive structure.
- **Finite-group controllers:** state machines where transitions correspond to group elements; output modulo a normal subgroup produces a shell-like quotient.
- **Finite-state error-correcting codes:** state codes over $\mathbb{Z}/n$ with known syndrome structure.

**Pass criterion:** the instrument recovers the attractor behavior of the system (e.g., in a linear congruential generator, detects the fixed points) and distinguishes seam-like edge cases from bulk behavior.

**Fail criterion:** the instrument gives no better than baseline on any of these.

---

## Stage 1C — Generic Toy Systems (LOWER PRIORITY NOW)

**Target:** generic dynamical systems with possible symbolic structure.

**Why later:** these require a coarse-graining that is not natively aligned with the tower's category. Testing requires either:

- A principled justification for why a specific $\Phi$ connects the system's dynamics to modular/shell structure.
- Acceptance that the test measures compatibility of the encoding with the instrument, not the system itself.

**Objects (when appropriate):**

- Rule 110 (with a principled encoding, not arbitrary windows).
- Logistic map (if a symbolic partition aligns with modular structure — e.g., via rotation number).
- Ising lattice (near phase transition, if order parameters can be discretized modularly).

**Pass criterion at this stage:** the instrument detects structure better than trivial baselines AND the encoding is principled (derived, not tuned).

---

## Stage 2 — Controlled Lattice/Automaton Analogs (UNCHANGED)

After Stages 1A, 1B pass. Reserved for well-controlled lattice or automaton systems where the instrument has demonstrated success in category.

---

## Stage 3 — Real Measured Symbolic Data (UNCHANGED)

After Stage 2. Applications to actual measurements, with pre-specified encoding and comparison against domain-standard baselines.

---

## Stage 4 — Deeper Interpretation (UNCHANGED)

Reserved. Only after Stage 3 accumulates positive evidence.

---

## Summary Diagram

```
Stage 0 (complete)
  → Theorem on Z/10Z

Stage 1A (NEW — first)
  → Shell-native synthetic benchmarks
  → Calibration: does the instrument recover known structure?

Stage 1B (revised position)
  → Ring-native systems
  → Scope: does the instrument work beyond its explicit construction?

Stage 1C (formerly Stage 1 — deprioritized)
  → Generic toy systems
  → Only with principled encodings

Stage 2
  → Controlled analogs

Stage 3
  → Real data

Stage 4
  → Interpretation (gated behind all prior stages)
```

---

## What Changed

- Rule 110 and similar systems are moved to Stage 1C, not Stage 1.
- Stage 1A is new and comes before any other testing.
- The "does it recover its own structure?" test is now prerequisite to "does it detect structure elsewhere?"
- No instrument revision; only re-sequencing of test targets.

---

## Discipline Statement

**The theorem spine is not loosened. The test sequence is re-ordered.**

If Stage 1A fails — if the instrument cannot recover known shell-native generative structure — then the instrument has a genuine problem and must be revised or retracted.

If Stage 1A succeeds, we proceed to 1B. We do not skip to 1C or later. We do not claim generalization without evidence.
