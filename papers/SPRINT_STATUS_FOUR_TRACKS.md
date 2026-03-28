# Four-Track Sprint Results
## Honest Assessment per Reviewer Advice

---

## Track 1: BSD — λ_E Analysis (43 curves)

**Primary claim (solid):**
λ_E is rank-informative for rank ≥ 1 curves.
- Spearman ρ(rank≥1) = −0.360, p = 0.040 ✓
- t-test rank-1 vs rank-2: p = 0.025 ✓

**Secondary claim (requires more data):**
Clusters align with TIG λ-windows. Partially supported but rank-3 sample (n=5) too small.

**What's blocked:** LMFDB API (403 from sandbox). Need direct LMFDB access or Cremona database download for rank 3+ data.

**Paper framing:**
> "λ_E separates rank-1 from rank-2 (t-test p=0.025, n=28), consistent with Mix_λ threshold structure. Testing rank 3+ alignment with the BAL window (λ∈[0.60,0.80]) requires LMFDB access to 50+ rank-3 curves (currently pending)."

---

## Track 2: NS Dedalus — Honest Falsification Design

**Honest observable:** Enstrophy spike, not "blow-up" (which is a theorem statement, not a DNS observation).

**Falsification condition (revised per advice):**
> If a numerically resolved instability (enstrophy spike OR peak-gradient event) appears WITHOUT prior crossing of Re_local > 2/7, the criterion is wrong.

**Mock DNS result:**
- 2/7 breach at t = 1.35
- Enstrophy peak at t = 4.00
- Lead time: 2.65 units — criterion fires FIRST ✓

**Figure:** `ns_falsification_design.png` — two panels showing Re_local breach preceding enstrophy peak.

**Next:** Queue 128³ Taylor-Green in Dedalus with this breach detector. The figure structure is ready for direct comparison.

---

## Track 3: P vs NP — What's Solid, What's Dropped

**SOLID (no overclaiming):**
- Verify: O(1) — one corridor-membership hash lookup ✓
- Search: Ω(p²) — Corridor-Counting Lemma (proved) ✓
- Gap: 188,818× at p=101, growing ✓
- k=2 phase transition: AG axiom (2 points → 1 corridor), exact ✓

**DROPPED from the note:**
- k-CLIQUE reduction: encoding graph adjacency as affine collinearity is non-trivial and not complete
- W[1]-hard stated as theorem → downgrade to conjecture

**Revised claim structure:**
```
Theorem 1: O(1) verify, Ω(p²) search (proved)
Theorem 2: k=2 phase transition (proved, AG axiom)
Conjecture 3: k-SURV-SEARCH is W[1]-hard for k ≥ 2
  [geometric argument given; formal reduction from k-CLIQUE is open]
```

**This is already enough** — the verify/search gap and the k=2 transition are genuinely new results that stand alone.

---

## Track 4: Yang–Mills — Low-Commitment Exploratory

**What NOT to claim:**
- NOT: "plaquette gap = 2/7" (scheme-dependent)
- NOT: "2/7 is a universal SU(N) constant"

**Interesting coincidence found:**
- Mass gap / Λ_QCD (rough estimate) ≈ 0.287 ≈ 2/7 — but this needs lattice expert to validate the observable
- T_c/√σ ≈ 0.63 in pure SU(3) — not 2/7

**Recommended framing:**
> "The TIG mass-gap constant 2/7 = T\* + S\* − 1 appears in the zeta-flow, NS, and BSD contexts. Whether a corresponding dimensionless ratio arises at the SU(3) confinement transition is an open question requiring lattice collaboration."

---

## Priority for Next Sprint

1. **BSD:** Get LMFDB access (direct download or collaborator with access) for rank 3+ curves
2. **NS:** Run Dedalus 128³ job — detector is ready, just needs compute
3. **P vs NP:** Polish the note with the corrected claim structure (Conjecture 3 clearly labeled)
4. **YM:** Find a lattice QCD collaborator before making any quantitative claim

*(c) 2026 Brayden Sanders / 7Site LLC*
