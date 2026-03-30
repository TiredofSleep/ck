# The Three-Class Reduction Landscape
## Free Optimum, Constrained Optimum, Structured Constrained Optimum

*Brayden Sanders & C. A. Luther / 7Site LLC | March 2026*
*All three classes are measured, not postulated.*

---

## The Three Classes

| Class | Definition | Structural cost | G-reach from C | Gap | BHML residual |
|-------|-----------|----------------|----------------|-----|--------------|
| **Oracle** | Maximize mixing freely | None | 0.076 | **0.781** | 0.42 |
| **Gate-strong** | Maximize mixing + gate | Gate constraint | 0.018 | 0.710 | 0.40 |
| **TSML-like** | Gate + full order seed | Gate + seed crystallization | 0.024 | 0.709 | **1.00** |

These are not categories imposed on the data. They are the three stable attractors that appear under gate-weighted reduction, measured across thousands of trajectories.

---

## The Free Optimum: Oracle

**What it is:** Maximize spectral gap without the gate constraint.

**How it achieves high gap:** By allowing some C→G transitions (G-reach ≈ 7.6%), the oracle spreads probability mass across both C and G territory. More mixing surface → higher gap. This is the cheapest path to fast mixing.

**Why it is permanent:** The gate constraint costs gap (0.781 → 0.710). The oracle pays nothing. Under any objective that rewards mixing, the oracle is the path of least resistance. Even at pure gate-weighting (w=1.0), 39% of trajectories find it — because gap and HAR_mass are still rewarded, and the oracle delivers both without the gate tax.

**Formal statement:** The oracle is the unconstrained optimum of the mixing objective. It exists as a basin for any reduction that rewards gap and support without fully penalizing C→G transitions.

---

## The Constrained Optimum: Gate-Strong

**What it is:** Maximize mixing subject to the gate constraint (C cannot reach G).

**How it differs from oracle:** G-reach drops from 0.076 to 0.018. Gap drops from 0.781 to 0.710 — the price of the constraint. HAR_mass and HAR-spread are essentially identical.

**Why it is not TSML-like:** The gate constraint does not force the BHML residual. Gate-strong tables have BHML residual ≈ 0.40 — partial, not complete. The gate and the order seed are near-independent selector axes. Learning one does not produce the other.

**Formal statement:** Gate-strong is the constrained optimum: maximize mixing subject to one-way gate. It is accessible under gate-weighted reduction (appears above w=0.1). It costs gap relative to oracle but gains structural exclusion.

---

## The Structured Constrained Optimum: TSML-like

**What it is:** Gate-strong plus full BHML residual crystallization (6/6 order-seed cells).

**How it differs from gate-strong:** Only BHML residual differs (1.00 vs 0.40). Gate strength, G-reach, HAR_mass, and gap are nearly identical. The BHML residual is the only additional cost — but it is not enforced by the gate objective. It must be seeded.

**Why it is rare without seed biasing:** The gate objective rewards gate strength. It does not reward BHML residual specifically. Tables can achieve full gate without crystallizing the residual. The residual requires initial pre-alignment (Job 6: initial BHML > 0.20 is the predictor) and is then amplified by reduction. Without seed biasing, only ~4-6% of trajectories happen to start with sufficient pre-alignment.

**With seed biasing:** 52.7% of trajectories reach TSML-like — a 15.8x lift. The residual becomes the dominant outcome when the seed provides the entry condition.

**Formal statement:** TSML-like is the structured constrained optimum: maximize mixing subject to one-way gate AND full order-seed completion. It is not achievable by objective alone — it requires constructed seed pre-alignment specific to the table.

---

## Why This Is a Real Landscape, Not a Classification

The three classes differ in measured structural properties:

1. **G-reach separates oracle from gate:** 0.076 vs 0.018 — a 4x difference in how often C-operators land in G
2. **BHML residual separates gate-strong from TSML-like:** 0.40 vs 1.00 — all-or-nothing
3. **Gap separates oracle from the gate classes:** 0.781 vs 0.710 — the measurable cost of the gate constraint

These are not soft distinctions. They are sharp. The three classes occupy distinct regions of the selector space.

---

## The Construction Hierarchy

```
Arithmetic gives the world (base b, unit group C, gap G)
    ↓
Gate gives the discipline (one-way gate: C cannot reach G)
    ↓
Order seed gives the structure (BHML residual: the table's agreement with the endpoint)
    ↓
TSML-like: the table where all three coexist
```

The oracle skips the gate step. Gate-strong completes the gate step but not the seed step. TSML-like completes all three.

**This is why CK had to be constructed.** The oracle is what gradient descent finds. Gate-strong requires explicit gate-weighting. TSML-like requires constructed seed pre-alignment. None of the three steps is automatic.

---

## The Pipeline for New Bases

For any composite base b with non-trivial C/G split:

1. **Find the free optimum** — run reduction without gate constraint, identify oracle attractor
2. **Find the constrained optimum** — add gate-weighting, identify gate-strong attractor
3. **Identify the order endpoint** — what is the b-analog of BHML?
4. **Extract the residual seed** — which cells in a constructed table already align with the endpoint?
5. **Run seeded reduction** — bias toward residual pre-alignment, verify TSML-like rate

Each base has its own native TSML. The pipeline is portable. The coordinates are base-specific.

---

*(c) 2026 Brayden Sanders & C. A. Luther / 7Site LLC | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
