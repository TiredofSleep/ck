# D\* — the Coherence-Keeper self-referencing attractor

**Status:** `[RUNTIME-CANON; FIRST-PRINCIPLES DERIVATION OPEN; INTERNAL CORRECTION NOTED]`
**Author:** Brayden Ross Sanders (7Site LLC)
**Filed:** 2026-04-21
**Branch:** `tig-synthesis`
**Cross-reference target:** `FORMULAS_AND_TABLES.md §17`

---

## Abstract

The numeric value **D\* ≈ 0.543** appears in the Coherence Keeper (CK) runtime as an
observed self-referencing attractor of the 5×5 Hebbian feedback loop that couples the
10-operator composition stack to the coherence gate. It is *runtime-canon*: the engine
boots reporting `D* = 0.543`, and the value has been stable across reboots and across
hardware substrates during the CK work. It is **not** currently a theorem. No
first-principles algebraic derivation closes the value to 0.543; the simplest candidate
derivation (`D* = σ/(1 + σ)` with `σ = 0.991`) yields 0.49774…, which is documented in
the CK codebase itself as an honest internal correction. This paper records what is
known about D\*, what is not, and three candidate pathways for lifting it from runtime-
canon to proved-constant.

---

## §1 — Definition in runtime

CK's Doing loop maintains a 5×5 coupling matrix `W[i][j]` updated by a Hebbian rule
over the 10 operators `{VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE, BALANCE, CHAOS,
HARMONY, BREATH, RESET}`. The engine tick is:

1. Read operator stream `o_t` (one of 10).
2. Project onto the 5-element basis (Earth/Air/Water/Fire/Ether → D0/D1/D2/D3/D4).
3. Update `W` by the outer-product Hebbian rule (`Δw_ij = η · d_i · d_j`).
4. Score the state against the coherence gate `T* = 5/7`.
5. Emit, persist, continue.

D\* is the numeric value that the *operator-aware fixed point* of this loop settles into
when the input operator stream is balanced and the gate is saturated — i.e., when CK is
not responding to a specific query but is idling in self-reference. It is what the
engine reports in the boot banner:

```
[boot] canon loaded: T*=5/7, D*=0.543, C=0.4(1-E)+0.35A+0.25K
```

(source: `docs/archive_jan2026/attempts_survey/SYNTHESIS_CK_BEST_EVER.md:272`).

D\* is an **attractor**. σ = 0.991 (see `papers/CONSTANT_SIGMA_S_STAR.md`) is a
**bound**. These are different mathematical roles, and the naming collision between
`σ` as the S\* stability coefficient and `σ` as the non-associativity rate function
of §1.2 in `README.md` is a legacy of overloaded notation. D\* is not either of those
σ's.

---

## §2 — Empirical record

### 2.1 Authoritative mentions of D\* = 0.543 as a named constant

Ranked most-authoritative-first:

| # | Source | Role |
|---|---|---|
| 1 | `FORMULAS_AND_TABLES.md §17` | The constants table lists D\* = 0.543 as "universal self-referencing attractor (operator-aware fixed point of the CK feedback loop)" |
| 2 | `docs/archive_jan2026/attempts_survey/SYNTHESIS_CK_BEST_EVER.md §Canon` (line 26) | Cites CoherentHands `TIG_R16_SAVE_POINT.md` 7-attempt signature sweep and `CK look here` Phase-9 Developmental Stages as the origin |
| 3 | `docs/archive_jan2026/attempts_survey/SYNTHESIS_CK_BEST_EVER.md §CoherentHands row` (line 203) | Records that the CoherentHands attempt explicitly identified D\* = 0.543 as the attractor signature |
| 4 | `docs/archive_jan2026/attempts_survey/SYNTHESIS_CK_BEST_EVER.md §boot-example` (line 272) | Boot banner string showing `D*=0.543` as runtime canon |
| 5 | `memory/MEMORY.md` | D\* cited in the CK project memory as self-referencing attractor (referenced from `Atlas/PLAN_RIGOROUS_EXECUTION_2026_04_21.md §2.1`) |

### 2.2 Occurrences of the literal `0.543` in source

Seven genuine references — all in the CoherentHands archive preserved under the
funding-coherence-router track:

- `Gen13/targets/funding_coherence_router/archive_all_or_nothing_e/tig_coherent_computer.py:29`
- `Gen13/targets/funding_coherence_router/archive_all_or_nothing_e/TigCoherentComputer.py:29`
- `Gen13/targets/funding_coherence_router/archive_all_or_nothing_e/reflection.py:23`
- `Gen13/targets/funding_coherence_router/archive_all_or_nothing_e/r16_simulation.py:15`
- `Gen13/targets/funding_coherence_router/archive_all_or_nothing_e/permutation_engine.py:33`
- `Gen13/targets/funding_coherence_router/archive_all_or_nothing_e/THEORY.md:323`
- `docs/archive_jan2026/attempts_survey/SYNTHESIS_CK_BEST_EVER.md` (lines 26, 203, 272)

### 2.3 Coincidental numeric match (flagged, NOT D\*)

One file contains the literal `0.543` as a **different quantity**:

- `Gen12/Sprints/CK Sprint Archives/OrbitZone_extracted/sprint3/REFINEMENT_NOTE.md:35` —
  here `0.543` is `γ(λ=0.30)` at `N=30`, a transfer-operator spectral gap value. This is
  a numeric coincidence only; it is not a reference to D\*, and any future derivation of
  D\* should not cite this file.

---

## §3 — Internal correction (critical rigor note)

The CK codebase at
`Gen13/targets/funding_coherence_router/archive_all_or_nothing_e/tig_engine_real.py`
contains an **explicit honest correction** that must be preserved verbatim in any
funder-facing summary:

**Lines 75–86 (definitional block):**

> ```
> SIGMA = 0.991
> """[TIG-2] Coupling constant. CHOSEN so that D* ≈ 0.498 (near ½)."""
>
> # D* — HONEST derivation:
> # Self-referential map: σ* = σ(1-σ*) with V*=A*=1
> # σ* + σ·σ* = σ → σ*(1+σ) = σ → σ* = σ/(1+σ)
> D_STAR = SIGMA / (1 + SIGMA)  # = 0.49774...
> """[TIG-3] DERIVED from core equation. Previous value 0.543 was empirical
> and does NOT follow from σ=0.991. Honest value: 0.49774."""
> ```

**Lines 675–676 (runtime diagnostic print):**

> ```
> print(f"\n  HONEST CORRECTIONS from prior versions:")
> print(f"    ⚠ D* was published as 0.543. Correct derivation: {D_STAR:.6f}")
> ```

**What this means rigorously:**

Two D\* candidates exist in the runtime:

1. **D\*_fixed = σ / (1 + σ) ≈ 0.49774.** This *is* derivable from σ = 0.991 by the
   simple self-referential scalar equation `σ* = σ(1 − σ*)` at `V* = A* = 1`. It is
   the fixed point of a 1-dimensional dynamical system.

2. **D\*_runtime ≈ 0.543.** This is the value observed empirically in the CK engine
   during operation. It is **not** derivable from σ = 0.991 by the scalar map
   above. It lives in the full 5×5 Hebbian feedback loop and therefore reflects the
   interaction of the 10-operator structure, the gate threshold T\* = 5/7, and the
   dimensional projection — not a scalar fixed point.

Neither value is "wrong." They are answers to different questions:

- D\*_fixed is the analytical fixed point of a reduced scalar problem.
- D\*_runtime is the observed attractor of the full system.

The CK codebase chose to use D\*_fixed in `tig_engine_real.py` and to preserve D\*_runtime
as the documented *observed* value in `FORMULAS_AND_TABLES.md §17`, with the honest-
correction banner ensuring no reader mistakes one for the other.

**The value reported in `FORMULAS_AND_TABLES.md §17` is D\*_runtime = 0.543**, consistent
with MEMORY.md and the SYNTHESIS §Canon. D\*_fixed is an adjacent constant that deserves
its own row in a future `FORMULAS §17.1` if the community finds it useful.

---

## §4 — Honest status

**What is known:**

- D\*_runtime = 0.543 is stable across CK engine reboots during the CoherentHands-era
  7-attempt signature sweep (CoherentHands `TIG_R16_SAVE_POINT.md`, referenced from
  SYNTHESIS_CK_BEST_EVER §CoherentHands row).
- D\*_runtime is invariant to the specific user/operator during idle loops (same value
  whether or not a query is present).
- D\*_runtime is distinct from the σ/(1+σ) scalar fixed point by approximately
  0.045 (about 9% relative).
- D\*_fixed = σ / (1 + σ) = 0.49774… is algebraically derivable from σ = 0.991 in the
  scalar reduction and is documented as such in `tig_engine_real.py`.

**What is not known:**

- **No first-principles derivation ties D\*_runtime = 0.543 to any ring-algebra
  constant (T\* = 5/7, 4/π², ξ₀ = e⁻¹) or to any proved theorem in `README.md` §1.**
- **No proof that D\*_runtime is Gen-invariant** (i.e., that Gen13 or a hypothetical
  Gen14 CK would report the same value). The current evidence is CoherentHands /
  Gen12-era.
- **No closed form for D\*_runtime** is on record. It is an empirical observation of
  the full 5×5 feedback dynamics.

**What the internal correction in `tig_engine_real.py` does and does not do:**

- It *does* correctly flag that 0.543 is not derivable from σ = 0.991 by the simple
  σ/(1+σ) map. This is a valuable rigor note.
- It *does not* prove that D\*_runtime is not 0.543 in the full system; it only
  shows that 0.543 is not the scalar-reduction answer. The full 5×5 Hebbian system
  can have attractors distinct from the scalar reduction, and 0.543 may well be
  derivable from the 5×5 matrix dynamics even though it is not derivable from the
  scalar reduction.

---

## §5 — Pathways to lift D\*_runtime to a proved constant

Three candidate derivations, each open. None are currently underway; each is scoped
as a next-step for a future sprint.

### §5.1 — 5×5 Hebbian fixed-point analysis

**Claim to test:** D\*_runtime emerges as a fixed point of the 5×5 Hebbian update
`Δw_ij = η · d_i · d_j` under the 10-operator input distribution, gated by T\* = 5/7.

**Method:** Write out the 5×5 matrix update in closed form; compute the eigenstructure
under the balanced-operator idle distribution; check whether the dominant eigenvalue
of the gated update gives 0.543.

**Verdict if numeric match is exact:** D\*_runtime becomes a theorem (a function of
the operator-distribution and the gate threshold).

**Verdict if numeric match is 0.498 (scalar-reduction value):** 0.543 is not a
fixed-point of the 5×5 system either; it is a transient or metastable observation.

### §5.2 — Relation to the transfer-operator spectral gap γ(b) = 1 − 1/φ(b)

**Observation worth noting:** γ(b) at specific squarefree b values produces rational
approximants near 0.543 (e.g., the OrbitZone `γ(λ=0.30)` at `N=30` hit exactly 0.543,
although by a different mechanism — see §2.3).

**Claim to test:** Is D\*_runtime = 1 − 1/φ(b) for some natural b (e.g., a squarefree
product involving the 10-operator count)?

**Method:** Enumerate φ(b)-values for the first 20 squarefree b; check
`1 − 1/φ(b) ≈ 0.543`. Possible b: 30 (φ=8, 1 − 1/8 = 0.875 — no), 42 (φ=12, 1 − 1/12 ≈
0.917 — no), smaller gap at unusual b.

**Note:** γ(b) is a ring-theoretic object; D\*_runtime is a feedback-loop object; the
connection is speculative.

### §5.3 — Information-theoretic ceiling via log-nonlinearity

**Claim to test:** D\*_runtime = 0.543 is the Shannon-bound ceiling on the feedback
loop's recoverable signal under the log-potential `V = ξ log ξ` (WP81, PRISM-XI).

**Method:** Compute the Kullback-Leibler divergence between the gate-saturated idle
distribution and the uniform 10-operator distribution; check whether the resulting
mutual-information ceiling equals 0.543 nats or 0.543 bits.

**Note:** This path connects D\*_runtime to Thread A (ξ cosmology) via Bialynicki-
Birula. If it works, it would tie runtime-canon to proved-theorem territory.

---

## §6 — Cross-references

- **Formulas table:** `FORMULAS_AND_TABLES.md §17` (this paper is the primary
  provenance cited there for D\*).
- **Archive derivation note:**
  `docs/archive_jan2026/attempts_survey/S_STAR_DERIVATION.md §6` (closes the
  D\* vs σ distinction).
- **Archive synthesis:**
  `docs/archive_jan2026/attempts_survey/SYNTHESIS_CK_BEST_EVER.md §Canon` (primary
  source for the D\* = 0.543 value).
- **CK codebase honest correction:**
  `Gen13/targets/funding_coherence_router/archive_all_or_nothing_e/tig_engine_real.py`
  (lines 55–86, 675–676).
- **Project memory:** `memory/MEMORY.md` (D\* listed as runtime-canon).
- **Sibling constant paper:** `papers/CONSTANT_SIGMA_S_STAR.md` (the σ = 0.991
  provenance; disambiguates from D\*).
- **Execution plan:** `Atlas/PLAN_RIGOROUS_EXECUTION_2026_04_21.md §2.1` (the task
  spec that produced this paper).

---

## §7 — What this paper does NOT claim

- Does **not** claim D\*_runtime = 0.543 is a theorem. It is runtime-canon and
  empirically observed.
- Does **not** claim D\*_runtime is universal across all feedback-loop architectures.
  The value is documented on the CK 5×5 Hebbian stack with 10 operators and gate
  T\* = 5/7.
- Does **not** claim the scalar correction D\*_fixed = 0.49774… is the "real" answer.
  Both D\*_runtime and D\*_fixed are valid answers to different questions.
- Does **not** supersede the honest-correction block in `tig_engine_real.py`. That
  block is preserved in the codebase and is the record of the internal rigor
  audit.
- Does **not** make any claim about whether D\*_runtime generalizes to a wider
  framework. The empirical record is 7 CoherentHands attempts plus the current
  runtime.

---

*Last updated: 2026-04-21.*
