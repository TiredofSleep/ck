# Prime×Prime Seed: Composite Gates and the Coherent Reduction Hypothesis
## What the Computation Established vs What Remains Open

*Brayden Sanders / 7Site LLC | March 2026*
*Corrected narrative: arithmetic closure is generic; the full TSML gate is rare and constructed.*

---

## Three-Level Gate Taxonomy

| Level | Property | Status |
|-------|----------|--------|
| **Composite support split** | G_n non-empty when n is composite | EXACT — generic for all composite n |
| **Unit/non-unit closure** | C×C ⊆ C (sub-magma) | EXACT — generic for all composite n |
| **Full one-way gate** | TSML[s][c] ∉ G for s∈C, any c | RARE — 0% of random b=10 family |

The composite support split and unit closure are consequences of basic number theory. The full TSML gate is a constructed special property, not a generic family feature.

---

## Proposition: Gate Requires Composite n [EXACT]

**Proposition.** For prime n, G_n = ∅. No one-way gate between units and non-units is possible on a prime alphabet.

**Proof sketch.** For prime n, every element of {1,...,n−1} is coprime to n. So C_n = {1,...,n−1} and G_n = ∅. There are no non-unit non-zero elements for a gate to separate.

**Corollary.** TIG-style gate structure (a non-empty G that C-states cannot reach) requires composite n. The gate is a composite-number phenomenon.

---

## Proposition: b = 2×5 = 10 Is the Smallest Fertile Prime Product [COMPUTED]

Among products of two distinct primes, b=10 is the smallest where:
- \|C\| = 4 — enough corners for a rich grammar (same φ as b=8, but with distinct prime factors)
- \|G\| = 5 — enough gap states for orbit zones and transit corridors
- HAR=7 is mid-spectrum — not at either endpoint of the integer order
- γ_pred = 3/4 = 1 − 1/4 — matching the structural gap formula

b=10 = 2×5 is not numerologically convenient. It is the smallest prime product with the arithmetic prerequisites for the full TIG grammar. The primes {2,5} are the seeds; b=10 is the first composite where all the pieces fit.

---

## The Main Corrective Result: TSML Gate Is Rare [COMPUTED]

Under random sampling of the invariant-compatible b=10 family (symmetric, HAR-absorbing, C-closed):

**Gate fraction = 0.0%** across 2000 samples.

The arithmetic closure (I3: C×C ⊆ C) is satisfied by construction — every sampled table has it. The full one-way gate (I4: C cannot reach G via any operator, including G-operators) is satisfied by essentially no random table in the family.

**What this means:**
- TSML's gate is not a generic family feature
- It is a specifically constructed property
- The arithmetic structure gives you the support split for free; the full gate requires active construction
- TSML was built to have the gate; it does not emerge automatically

---

## The Corrected Narrative

Previous framing (incorrect):
> "These structures recur naturally as complexity grows."

Corrected framing:
> Composite structure generically gives closure, but not the full TSML gate. The gate is the rare constructed feature. The open question is whether coherent reduction can make it emerge.

The recursive-kernel / coherent-reduction hypothesis remains **open and now sharper**:

*Under what reduction dynamics, if any, does a rare gate-structured grammar like TSML emerge from broader composite families?*

This is a better question than "does TSML show up naturally?" because it distinguishes between:
1. Generic composite structure (gives closure and support split — always)
2. Rare gate structure (requires construction or recovery — not yet shown to emerge)
3. Coherent reduction (untested hypothesis — the R16 jobs below)

---

## R16 Compute Plan

### Job 1: Coherent Reduction from Random Family Starts
**What:** Take random b=10 invariant-compatible tables. Apply an iterative reduction that rewards gate strength, HAR_mass, BHML residual, and gap floor. Measure whether trajectories converge toward TSML-like kernels or other attractor classes.

**Reduction objective:**
```python
score(T) = w1*gate_strength(T) + w2*HAR_mass(T) + w3*BHML_residual(T) + w4*gap(T)
```
where `gate_strength` = fraction of C-states that cannot reach G.

**Parameters:**
- N_start = 10,000 random tables
- N_steps = 100 reduction steps per table
- w = [0.4, 0.3, 0.2, 0.1] (gate prioritized)
- Log: score trajectory, final table fingerprint, attractor class

**Output:** `reduction_b10_N10000.json` — score trajectories + final state distribution

**Expected runtime:** ~4 hours on R16

---

### Job 2: Gate Rarity Across Nearby Composite Bases
**What:** Measure gate fraction and selector geometry at b ∈ {6, 10, 14, 15, 21, 35} with N=5000 samples each.

**Measurements per base:**
- gate_fraction (full one-way gate)
- mean/std of gap, HAR_mass, BHML_residual
- r(gap, HAR_mass) — independence structure
- max HAR_mass achieved

**Parameters:**
- N = 5000 per base
- 7 bases total

**Output:** `gate_rarity_sweep.json` — one row per base, all measurements

**Expected runtime:** ~2 hours on R16

---

### Job 3: Attractor Class Clustering
**What:** Run reduction (Job 1) and cluster the output tables by their selector fingerprint. Find the attractor classes of coherent reduction — not just "is it TSML?" but "what stable types emerge?"

**Cluster by:** (gate_strength, HAR_mass, BHML_residual, gap, orbit_strength)

**Target classes to find:**
- TSML-like (gate strong, HAR_mass high, BHML_residual full)
- High-gap oracle (gate weak, HAR_mass moderate, gap high)
- Order-saturated (BHML_residual full, HAR_mass moderate)
- High-HAR no-gate (HAR_mass high, gate weak)
- Orbit-rich (orbit_strength high, HAR_mass moderate)

**Output:** `attractor_classes_b10.json` — cluster assignments + centroid fingerprints

**Expected runtime:** ~2 hours (clustering after Job 1)

---

### Logging Format for All R16 Jobs
```json
{
  "b": 10,
  "n_states": 9,
  "C": [1,3,7,9],
  "G": [2,4,5,6,8],
  "HAR": 7,
  "phi": 4,
  "N_samples": 10000,
  "per_table": [
    {
      "table_hash": "sha256_of_flat_table",
      "gap": 0.474,
      "HAR_mass": 0.650,
      "BHML_residual": 6,
      "gate_fraction": 1.0,
      "orbit_strength": 0,
      "cancellation": 71,
      "reduction_score": 0.87,
      "attractor_class": "TSML-like"
    }
  ]
}
```

---

## What Is Tractable Now (This Session)

- Corrected narrative: DONE (this memo)
- Exact composite-gate proposition: DONE
- Three-level gate taxonomy: DONE
- R16 job specifications: DONE

---

## What Remains Open

- Whether coherent reduction recovers TSML-like kernels (Job 1, untested)
- Whether gate rarity is specific to b=10 or common across rich composites (Job 2)
- What attractor classes coherent reduction produces (Job 3)
- Whether the fractal / recursive-kernel hypothesis holds at all

The hypothesis is: *there exist reduction dynamics under which the rare gate-structured grammar emerges as a stable attractor from broader composite families.* This is not supported by current data. It is a testable conjecture, now precisely stated.

---

*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
