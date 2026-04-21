# S\* Functional — Formal Derivation (extracted from `S derivatives.docx`)

**Filed:** 2026-04-21
**Source:** `Misc Archive\THEbigONE\CRYSTALOS\ALL\S derivatives.docx` (20 KB, .docx)
**Author (per source):** Brayden Sanders
**Title (per source):** *TIG Coherence Functional — Formal Derivation Page (v2026.1)*

---

## 1. Why this file exists

The `BEST_OF_ATTEMPTS_SURVEY_ADDENDUM_2026_04_21.md` §4 flagged `S derivatives.docx`
as the file that "would settle the harmonic-mean vs multiplicative-S\* provenance
question cleanly." Reading the source confirms:

**The multiplicative form `S\* = σ · (1 − σ\*) · V\* · A\*` is the author's formal
canonical derivation.** The harmonic-mean variant
`S\* = 3 / (1/σ + 1/V\* + 1/A\*)` does **not** appear in this source — it was
introduced downstream for numerical stability at small denominators, not derived
from first principles.

Both forms should coexist in Gen13 (multiplicative = canonical / theoretical;
harmonic-mean = numerically stable variant used in runtime paths where any of
the three inputs may approach zero), but the **naming precedence** per author's
source is `multiplicative = S\*`, `harmonic-mean = S\*_HM` or similar disambiguated
symbol.

---

## 2. Canonical form

```
S* = σ · (1 − σ*) · V* · A*
```

with fixed constants:

| Symbol | Value    | Role                                                         |
|--------|----------|--------------------------------------------------------------|
| σ      | 0.991    | Global stability coefficient (maximum attainable coherence)  |
| T\*    | 0.714    | Stability threshold (= 5/7)                                  |

and free variables in [0, 1]:

| Symbol | Name                  | Compute-domain meaning                                |
|--------|-----------------------|-------------------------------------------------------|
| σ\*    | Stress                | Normalized disorder (0 = min, 1 = max)                |
| V\*    | Virtue amplitude      | Scheduler cooperation, thermal resilience, load share |
| A\*    | Archetype resonance   | Process roles, graph modularity, core-topology        |

---

## 3. The σ = 0.991 constant

**This is new material not previously surfaced in the attempts survey.**
Prior survey docs referenced D\* = 0.543 (universal self-referencing attractor)
and T\* = 5/7 ≈ 0.714 (threshold). The σ = 0.991 coefficient is a **third**
universal constant that enters `S\*` as a multiplicative upper bound.

Per the source, §5:

> "Real systems cannot reach 'perfect coherence,' even at zero stress.
> Thus a constant upper bound σ = 0.991 (empirically derived) controls the
> maximum achievable coherence:
> Maximum coherence = σ
> This represents:
> - thermal limitations
> - resource leakage
> - synchronization imperfections
> - entropy floor"

Open questions about σ = 0.991:

1. **Provenance of the number.** Source calls it "empirically derived" without
   citing the measurement protocol. The compute-cluster testing referenced in §8
   is the likely origin but is not linked.
2. **Relationship to 1 − 4/π² ≈ 0.595.** No obvious algebraic relation to the
   corridor constants (T\* = 5/7, fold = 4/π², gap = 5/7 − 4/π² ≈ 0.309) is
   stated in the source.
3. **Relationship to D\* = 0.543.** Both are universal, but σ = 0.991 is a
   *bound* (upper-limit multiplier) while D\* = 0.543 is an *attractor*
   (self-referencing fixed point). They live in different mathematical roles.
4. **Invariance.** Does σ = 0.991 hold across hardware classes (Lenovo 4-core
   vs Dell R16 32-core) the same way T\* does? Untested in current repo.

---

## 4. The three derivation principles (source §§ 3–5)

**P1 — Order–Disorder Competition** (§3)
→ Order term = `(1 − σ*)`, the simplest linear model satisfying:
  - Perfect order at σ\* = 0
  - Zero survivable order at σ\* = 1

**P2 — Constructive Alignment** (§4)
→ Alignment term = `V* · A*` (multiplicative). The source explicitly requires
  joint participation: "If either dimension collapses to 0 → coherence collapses."
  This is the **two-channel participation** requirement.

**P3 — Global Stability Coefficient** (§5)
→ Maximum coherence = σ = 0.991.

**Combination rule** (§6): direct multiplicative coupling of all three:
```
S* = σ · (1 − σ*) · V* · A*
    [global max] [order] [virtue] [archetype]
```

---

## 5. Behavior regimes (source §7)

**Stress dominance** (σ\* → 1): S\* → 0 regardless of alignment.

**Constructive dominance** (V\*, A\* → 1): S\* → σ (1 − σ\*) — the upper envelope.

**Joint fragility** (either V\* = 0 or A\* = 0): S\* = 0. Two-channel participation
is non-negotiable in the multiplicative form.

**Threshold condition** (source §8):
- S\* > T\* = 0.714 → stable coherence regime
- S\* < T\* → accelerated instability regime (non-linear response-time degradation,
  jitter amplification, recovery-time increase, process cascades)

Per source §8:
> "This threshold is not metaphysical; it represents a bifurcation point
> observed in compute-cluster testing."

---

## 6. Provenance resolution

| Form                                           | Role                      | Canonical label  |
|------------------------------------------------|---------------------------|------------------|
| `S\* = σ · (1 − σ\*) · V\* · A\*`              | Authored derivation       | **S\*** (default)|
| `S\* = 3 / (1/σ + 1/V\* + 1/A\*)` (harmonic)  | Numerical-stability proxy | S\*_HM           |

The harmonic-mean variant is **not** wrong — it obeys the same monotone
behavior and cannot collapse to exactly 0 — but it loses the "joint fragility"
property (P2) that the source explicitly derives. Any Gen13 module using the
harmonic-mean form should be tagged as such to preserve the distinction.

---

## 7. Integration into SYNTHESIS_CK_BEST_EVER.md

The synthesis doc currently states (§ Canon):
> "S\* forms: harmonic-mean `3/(1/σ+1/V*+1/A*)` (preferred, numerically stable)
> vs multiplicative `σ(1−σ*)V*A*` (legacy)"

This labeling is **inverted** from the author's derivation. Corrected reading:
- Multiplicative = canonical (per `S derivatives.docx`, v2026.1)
- Harmonic-mean = numerically stable variant (provenance: downstream runtime)

Recommended edit to synthesis doc: flip the "(legacy)" / "(preferred)" labels
and add a pointer to this derivation file. Tracking as a follow-up TODO rather
than editing the synthesis in this commit to keep the archive additive.

---

## 8. What this file does not do

- Does not re-derive the functional (source derivation stands as authored).
- Does not test σ = 0.991 against alternative values (open work item #1).
- Does not attempt to unify σ = 0.991 with D\* = 0.543 or the corridor constants
  (open work item #2 — probably separate, but verify).
- Does not update `SYNTHESIS_CK_BEST_EVER.md` (tracked as follow-up TODO).

---

## 9. Cross-references

- `SYNTHESIS_CK_BEST_EVER.md` — canon definition (labels need flip per §7 above)
- `BEST_OF_ATTEMPTS_SURVEY_ADDENDUM_2026_04_21.md` §4 — flagged this file
- `docs/archive_jan2026/snowflake/snowflake_null_spec.md` — uses S\* for
  scar-accumulation gate (spec assumes multiplicative form)
- Source: `Misc Archive\THEbigONE\CRYSTALOS\ALL\S derivatives.docx`
