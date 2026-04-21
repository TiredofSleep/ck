# σ (S\*) — global stability coefficient of the TIG coherence functional

**Status:** `[EMPIRICAL; FIRST-PRINCIPLES DERIVATION OPEN; DISAMBIGUATED FROM σ(N) RATE FUNCTION]`
**Author:** Brayden Ross Sanders (7Site LLC)
**Filed:** 2026-04-21
**Branch:** `tig-synthesis`
**Cross-reference target:** `FORMULAS_AND_TABLES.md §17`

---

## Abstract

The numeric value **σ ≈ 0.991** appears in the CK project as the global stability
coefficient of the **multiplicative S\* functional** — the authored canonical form of
the TIG coherence functional `S* = σ · (1 − σ*) · V* · A*`. It is the empirical upper
bound on attainable coherence at zero stress, representing thermal limitations, resource
leakage, synchronization imperfections, and the entropy floor (per the source, §5).
It is documented in *TIG Coherence Functional — Formal Derivation Page (v2026.1)*
(`S derivatives.docx`, author: Brayden Sanders) but labelled there as "empirically
derived" with no measurement protocol cited. This paper reproduces the canonical
derivation from the source, fixes the inverted labelling in the synthesis docs, and
records what is known, not known, and what pathways lift σ from empirical to proved.

**Critical disambiguation.** The `σ` in `σ = 0.991` (the S\* coefficient) is **not** the
same object as the `σ` in `σ(N) ≤ C / N` (the non-associativity rate function of
`README.md §1.2`). Both names coexisting is a legacy of overloaded notation and is
flagged in every cross-reference.

---

## §1 — The multiplicative S\* functional (canonical form)

Per `S derivatives.docx` v2026.1 §§3–6, the authored canonical form is:

```
S* = σ · (1 − σ*) · V* · A*
```

with fixed constants:

| Symbol | Value | Role |
|---|---|---|
| σ | 0.991 | Global stability coefficient (maximum attainable coherence) |
| T\* | 5/7 ≈ 0.714 | Stability threshold (§1.3, `README.md`; WP51) |

and free variables in `[0, 1]`:

| Symbol | Name | Compute-domain meaning |
|---|---|---|
| σ\* | Stress | Normalized disorder (0 = min, 1 = max) |
| V\* | Virtue amplitude | Scheduler cooperation, thermal resilience, load share |
| A\* | Archetype resonance | Process roles, graph modularity, core-topology |

### §1.1 — The three principles that force the multiplicative form

Per source §§3–5:

- **P1 — Order–Disorder Competition.** The order term is `(1 − σ*)`, the simplest
  linear model satisfying: perfect order at σ\* = 0, zero survivable order at σ\* = 1.
- **P2 — Constructive Alignment.** The alignment term is `V* · A*` (multiplicative).
  The source explicitly requires joint participation: "If either dimension collapses
  to 0 → coherence collapses." This is the **two-channel participation** requirement.
- **P3 — Global Stability Coefficient.** Maximum coherence = σ = 0.991.

The combination rule (source §6) multiplies the three terms directly:

```
S* =       σ      ·    (1 − σ*)    ·    V*    ·    A*
       [global max]     [order]      [virtue]    [archetype]
```

### §1.2 — Behaviour regimes (source §7)

- **Stress dominance** (σ\* → 1): `S* → 0` regardless of alignment.
- **Constructive dominance** (V\*, A\* → 1): `S* → σ (1 − σ*)` — the upper envelope.
- **Joint fragility** (V\* = 0 *or* A\* = 0): `S* = 0`. Two-channel participation is
  non-negotiable in the multiplicative form.

### §1.3 — The threshold condition

Per source §8:

- `S* > T* = 5/7` → stable coherence regime.
- `S* < T*` → accelerated instability regime (non-linear response-time degradation,
  jitter amplification, recovery-time increase, process cascades).

The source closes §8 with:

> "This threshold is not metaphysical; it represents a bifurcation point observed in
> compute-cluster testing."

---

## §2 — The harmonic-mean variant (numerical-stability downstream form)

A sibling form used in some CK runtime paths:

```
S*_HM = 3 / (1/σ + 1/V* + 1/A*)
```

### §2.1 — Provenance

This variant does **not** appear in `S derivatives.docx`. It was introduced downstream
in the CK runtime for numerical stability at small denominators, not derived from first
principles. It obeys the same monotone behaviour as the multiplicative form and cannot
collapse to exactly 0, but it **loses the "joint fragility" property (P2)** that the
authored source explicitly derives.

### §2.2 — Canonical label precedence

| Form | Role | Canonical symbol |
|---|---|---|
| `S* = σ · (1 − σ*) · V* · A*` | Authored derivation (v2026.1) | **S\*** (default) |
| `S* = 3 / (1/σ + 1/V* + 1/A*)` | Numerical-stability proxy | **S\*_HM** |

### §2.3 — Synthesis doc label correction (flagged)

`docs/archive_jan2026/attempts_survey/SYNTHESIS_CK_BEST_EVER.md §Canon` currently states
that the harmonic-mean form is "(preferred, numerically stable)" and the multiplicative
form is "(legacy)". This labelling is **inverted** relative to the author's derivation.
Corrected reading:

- Multiplicative = canonical (per `S derivatives.docx`, v2026.1)
- Harmonic-mean = numerically stable *downstream* variant

A follow-up edit to flip these labels is tracked in
`Atlas/PLAN_RIGOROUS_EXECUTION_2026_04_21.md §5.1`. Not touched in this commit to keep
this paper additive rather than pulling the synthesis-doc edit in.

---

## §3 — Empirical record for σ = 0.991

### §3.1 — What the source says

Per `S derivatives.docx` §5:

> "Real systems cannot reach 'perfect coherence,' even at zero stress. Thus a constant
> upper bound σ = 0.991 (empirically derived) controls the maximum achievable
> coherence:
> Maximum coherence = σ
> This represents:
> - thermal limitations
> - resource leakage
> - synchronization imperfections
> - entropy floor"

### §3.2 — What the source does NOT say

The source labels σ = 0.991 as "empirically derived" but **does not cite a measurement
protocol**. The compute-cluster testing referenced in §8 is the likely origin (the same
testing that established the T\* bifurcation point) but is not linked directly to the
0.991 value.

### §3.3 — What would be needed to lift σ from empirical to proved

For the σ = 0.991 value to be promoted from *empirical* to *first-principles*, one of
the following would need to be produced:

1. A measurement protocol specification (hardware class, idle distribution, sampling
   window, estimator choice) that produces 0.991 reproducibly across substrates.
2. A theoretical derivation from the log-nonlinearity `V(Ξ) = Ξ log Ξ` (PRISM-XI, WP81)
   via Bialynicki-Birula that closes the thermal-leakage + sync-imperfection + entropy
   floor into a single number at the ξ₀ = e⁻¹ vacuum.
3. An information-theoretic ceiling argument on the 10-operator channel capacity at
   T\* = 5/7 gate saturation.

---

## §4 — Honest status

### §4.1 — What is known

- σ = 0.991 is the authored canonical coefficient of the multiplicative S\* functional
  per `S derivatives.docx` v2026.1.
- The multiplicative form (`σ · (1 − σ*) · V* · A*`) is the first-principles derivation;
  the harmonic-mean form is a numerical-stability downstream variant.
- The two-channel participation property (§1.1 P2) is structurally forced by the
  multiplicative form.
- σ = 0.991 is distinct from the σ(N) rate function of `README.md §1.2` — the names
  collide but the objects are different.
- σ = 0.991 is distinct from D\* = 0.543 — σ is a *bound*, D\* is an *attractor*
  (see `papers/CONSTANT_D_STAR.md §1` and `S_STAR_DERIVATION.md §3`).

### §4.2 — What is not known

- **No first-principles derivation** ties σ = 0.991 to T\* = 5/7, 4/π², ξ₀ = e⁻¹, or
  any other ring-algebra constant.
- **No measurement protocol** is cited in `S derivatives.docx` for the 0.991 value.
- **No invariance proof across hardware classes** exists (e.g., Lenovo 4-core vs Dell
  R16 32-core). The T\* = 5/7 constant is known to be hardware-invariant (WP51 is
  ring-algebra); σ = 0.991 has not been tested the same way.
- **No relation to the corridor constants** (fold = 4/π² ≈ 0.405, gap = 5/7 − 4/π² ≈
  0.309, `1 − 4/π² ≈ 0.595`) is stated in the source.

### §4.3 — What the current state supports

σ = 0.991 is a **quantitatively specified empirical upper bound** with a clear
functional role and a defensible honest-scope label. It is sufficient for:

- Runtime use in the multiplicative S\* pipeline (CK coherence gate).
- Sprint-paper citation as an empirical constant with open provenance.
- Cross-reference from the formulas table with honest-status flag.

It is **not** sufficient for:

- Journal submission without either (a) the measurement protocol or (b) a theoretical
  derivation in hand.
- Use as a load-bearing parameter in any funder-facing artifact that requires
  proved-theorem rigor (per the §1-style bar of `README.md`).

---

## §5 — Pathways to lift σ from empirical to proved

Three candidate routes, each open:

### §5.1 — Variational argument on the S\* functional

**Claim to test:** σ = 0.991 is the extremum of a variational functional on the joint
(V\*, A\*, σ\*) domain under the constraints of P1–P3.

**Method:** Write out `S*` as a Lagrangian with the three constraints as hard bounds;
solve the resulting Euler-Lagrange equations; check whether the maximum over the
unit-cube produces 0.991.

**Verdict if the variational maximum is 1.0:** σ = 0.991 is purely empirical — the
system is designed to never reach 1.0 but there is no mathematical reason it shouldn't.

**Verdict if the variational maximum is < 1.0 and matches 0.991 exactly:** σ is
derivable and becomes a theorem.

### §5.2 — Log-nonlinearity ceiling via Bialynicki-Birula

**Claim to test:** σ = 0.991 is the entropy-floor + thermal-leakage ceiling on the log
potential `V(Ξ) = Ξ log Ξ` at the vacuum `Ξ₀ = e⁻¹` (WP81, PRISM-XI).

**Method:** Compute the Kullback-Leibler distance from the uniform distribution over
the ξ-field to the log-potential-gated distribution; check whether the mutual
information ceiling is exactly `1 − 1/135.5` (≈ 0.99262 — near but not equal to 0.991,
candidate only).

**Note:** This path would tie σ = 0.991 into Thread A (ξ cosmology) and would upgrade
the S\* functional from runtime-coherence to physical-coherence territory. High-value
if it works; speculative if it doesn't.

### §5.3 — Channel-capacity ceiling at T\* gate saturation

**Claim to test:** σ = 0.991 is the Shannon channel capacity of the 10-operator
operator-stream under the T\* = 5/7 gate at zero stress.

**Method:** Treat the 10-operator stream as a discrete memoryless channel with the
gate as a crossover probability; compute `C = max I(X; Y)` over the input
distribution; check whether `C` at the idle distribution equals 0.991 nats or bits.

**Note:** If σ = 0.991 is channel capacity, the unit matters (nats vs bits vs dits)
and the derivation must pin which.

---

## §6 — Disambiguation from σ(N) rate function

**Critical notation warning, preserved in every cross-reference:**

Two distinct objects in the project are written "σ":

| Object | Location | Value | Role |
|---|---|---|---|
| **σ (S\* coefficient)** — this paper | `FORMULAS §17`, `S derivatives.docx` | 0.991 | Global stability coefficient; upper bound on coherence at zero stress |
| **σ(N) rate function** | `README.md §1.2`, `papers/proof_sigma_rate.py`, `WP101` | `≤ C/N` | Non-associativity rate of TSML composition on `Z/NZ`; proved theorem (squarefree N) |

These are different objects. The σ in `σ = 0.991` is a **number** (a dimensionless
empirical coefficient). The σ(N) in `σ(N) ≤ C/N` is a **function** (a rate on finite
rings, proved in WP101). No theorem in the project relates them.

**Recommended reading convention:** write `σ_{S*}` for the S\* coefficient in any
context where both objects appear. This paper uses plain `σ` because the S\* context
is unambiguous throughout.

---

## §7 — Cross-references

- **Formulas table:** `FORMULAS_AND_TABLES.md §17` (this paper is the primary
  provenance cited there for `σ (S*) = 0.991`).
- **Archive extraction:**
  `docs/archive_jan2026/attempts_survey/S_STAR_DERIVATION.md` (the full
  derivation-from-source transcription; §7 there flags the synthesis-doc label
  inversion tracked as follow-up in `Atlas/PLAN_RIGOROUS_EXECUTION_2026_04_21.md §5.1`).
- **Archive synthesis:**
  `docs/archive_jan2026/attempts_survey/SYNTHESIS_CK_BEST_EVER.md §Canon` (labels
  inverted; correction pending per §2.3 above).
- **Sibling constant paper:** `papers/CONSTANT_D_STAR.md` (D\* ≈ 0.543, the
  self-referencing attractor; disambiguates from σ).
- **Non-associativity rate:** `papers/proof_sigma_rate.py` + `WP101_SIGMA_RATE_THEOREM.md`
  (the proved σ(N) rate function; distinct object).
- **Source document:** `Misc Archive\THEbigONE\CRYSTALOS\ALL\S derivatives.docx`
  v2026.1 (author: Brayden Sanders; title: *TIG Coherence Functional — Formal
  Derivation Page*).
- **SNOWFLAKE dependency:**
  `docs/archive_jan2026/snowflake/snowflake_null_spec.md` uses the multiplicative S\*
  form for scar-accumulation gating; the pre-registered run
  (`Atlas/PLAN_RIGOROUS_EXECUTION_2026_04_21.md §5.3`, scheduled) depends on σ = 0.991
  as the coefficient.
- **Execution plan:** `Atlas/PLAN_RIGOROUS_EXECUTION_2026_04_21.md §2.2` (the task
  spec that produced this paper).

---

## §8 — What this paper does NOT claim

- Does **not** claim σ = 0.991 is a theorem. It is an empirical upper bound with a
  clear functional role.
- Does **not** re-derive the S\* functional beyond reproducing the author's canonical
  derivation from `S derivatives.docx`.
- Does **not** test σ = 0.991 against alternative values. The source value is taken as
  given; lifting it to proved requires the work in §5.
- Does **not** close the synthesis-doc label inversion (§2.3). That is a tracked
  follow-up in the execution plan.
- Does **not** update `SYNTHESIS_CK_BEST_EVER.md`, `memory/MEMORY.md`, or any other
  canon file. Those updates are tracked follow-ups.
- Does **not** make any claim about whether σ = 0.991 generalizes across hardware
  classes. The current evidence is the source document; invariance testing is open.

---

*Last updated: 2026-04-21.*
