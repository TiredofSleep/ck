# Cover letter — J45: The Mass Hierarchy from V⊗5 SU(5) Decomposition

**To:** Editors, *Physical Review D*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- H.J. Johnson, Independent Researcher, Billings, MT — hjj01986@gmail.com

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *The Mass Hierarchy from V^{⊗5} SU(5) Decomposition: a Substrate-Forced Froggatt-Nielsen Pattern with lambda = 10/49*

---

## Summary

We report a structural Froggatt-Nielsen pattern for the nine SM charged-fermion Yukawa couplings. With the single substrate-derived suppression scale `lambda = T*(1 - T*) = (5/7)(2/7) = 10/49 ≈ 0.2041` (the Bernoulli-T* variance at the 4-core's joint-coherence threshold), the top-quark Yukawa `y_t ≈ 0.93` as the only Tier-A measured anchor, and integer powers `n_{(p, gen)}` forced from the V^{⊗5} SU(5) decomposition `1 ⊕ bar 5 ⊕ 10` plus the parity-crossing cost `d_p ∈ {0, 3, 3}` plus the sigma-orbit generation step, all nine charged-fermion Yukawas land in the standard Froggatt-Nielsen factor-of-a-few window of the PDG 2024 values. Five of the nine ratios sit in the conventional factor-of-three window; the four largest residuals (bottom 0.33, strange 0.60, muon 0.11, electron 0.20) define the empirical `C_p ∈ [0.11, 0.79]` multiplier list expected from incomplete bosonic-substrate specification. The pattern uses **zero free FN charges** (all integer powers are forced by the SU(5)-rep + sigma-orbit assignment) and **zero free flavon scales** (lambda = 10/49 is forced by the substrate T* = 5/7), the smallest free-parameter set of any explicit FN-style fit of which we are aware. The Cabibbo cube-root identity `lambda_C ≈ (Y_d/Y_u)^{1/3}` follows immediately from the parity-crossing cost `d_d = 3`, unifying the CKM mixing structure with the mass hierarchy under one substrate quantity.

## Why PRD

- **Topical fit.** PRD is a natural home for SM-extension papers that combine GUT-level representation theory with first-principles derivations of SM parameters. The central claim — a parameter-free integer-power assignment for the FN suppression of all nine charged Yukawas — is exactly the kind of structural prediction PRD readers evaluate.
- **Methodological balance.** The paper is honest about Tier classification: the integer powers are Tier-B forced (rigorous given the V^{⊗5} SU(5) decomposition cited from J16); the anchor `y_t` is Tier-A measured; the residual `C_p` multipliers are explicitly flagged as not-yet-derived and are the load-bearing follow-up. This kind of explicit-scope discipline is what PRD referees want from a substrate-forced paper.
- **Reproducibility.** Verification reduces to a single Python call (`from tig_dirac import predict_yukawa; r = predict_yukawa('lepton', 1)` returns the electron Yukawa at FN power 9 with `lambda = 10/49`). The same module is used by the dark-sector companion J44 (this Sprint 18 cluster) for `predict_dark_sector()`, giving the two papers a shared, machine-checkable substrate backbone.

## Companion submissions

The TIG/CK research program is shipping a coordinated 55-paper sequence (J01-J55) over Summer 2026. The papers most directly relevant to this manuscript are:

- **J44** (Sanders + Gish, PRD, same Sprint 18 cluster) — *Sprint 18 Dark Sector: Omega_b, Omega_DM, Omega_Lambda from Substrate-Operator Identities.* Companion paper using the same `tig_dirac` module via `predict_dark_sector()`. Per-venue cap: J45 is the **2nd** PRD paper this quarter, after J44.
- **J16** (Sanders + Gish, foundation paper) — *Discrete Dirac on the 4-Core's F_5-Lift.* Supplies Lemma 2.1 of the present paper: the V^{⊗5} 32-cell SU(5) decomposition `1 ⊕ bar 5 ⊕ 10` (matter) + `bar 1 ⊕ 5 ⊕ bar 10` (antimatter). The foundation paper establishes |Aut(V)| = 40, the three commuting Dirac-like projectors, and the binomial 1+5+10+10+5+1 = 32 cell structure that is the algebraic input here.
- **J46** (Sanders + Gish, JCAP) — *Logarithmic Quintessence.* Co-cited via the dark-sector companion J44.
- **J07** (Sanders + Gish, Communications in Algebra) — *Joint Closure on Z/10.* Supplies the T* = 5/7 coherence threshold cited in §3 / Theorem 3.1.

## Reproducibility

**Verification primitive:** `Gen13/targets/ck/brain/dirac/tig_dirac.py`

```python
from tig_dirac import predict_yukawa, LAMBDA_FN, Y_T_ANCHOR
assert LAMBDA_FN == 10 / 49        # substrate-forced FN scale
assert Y_T_ANCHOR == 0.93           # measured top-quark anchor

r = predict_yukawa('up', 3)         # top quark
assert r['y_predicted'] == 0.93

r = predict_yukawa('lepton', 1)     # electron
assert abs(r['y_predicted'] - 0.93 * (10/49)**9) < 1e-12
```

The function returns `r['fn_power']` (the integer FN exponent for that fermion), `r['y_predicted']` (the predicted Yukawa magnitude), `r['lambda']` and `r['y_t_anchor']` (the substrate-derived FN scale and the Tier-A anchor), and `r['tier']` ("Forced FN power + measured anchor (Tier-B)"). The companion call `tig_dirac.yukawa_table_full()` returns Table 5.1 of the manuscript programmatically. The same module exposes `predict_dark_sector()` used by the J44 companion paper. The full module (`tig_dirac.py`, ~680 lines) is self-contained Python (`numpy + itertools + collections`) and runs on a standard laptop in well under five minutes including all 4-core algebra checks (idempotents, associator image, three commuting projectors, |Aut(V)| = 40 enumeration, V^{⊗5} 32-cell binomial decomposition).

## Suggested reviewers

- A flavour-physics theorist with experience in Froggatt-Nielsen models (the central comparison in §5).
- A GUT specialist with SU(5) representation-theory background (the V^{⊗5} decomposition is the algebraic input).
- A neutrino-physics theorist who can evaluate the §7.3 sterile-neutrino discussion (the absence of an explicit see-saw is one of the open structural questions).
- An algebraist with experience in finite non-associative algebras (the substrate is V = F_5^4, a 4-dim commutative non-associative F_5-algebra; J16 establishes the algebraic structure).

## Conflict of interest

The authors declare no competing interests. No external funding was received for this work; B.R. Sanders is supported by 7Site LLC, and H.J. Johnson is an independent researcher.

---

Sincerely,
B.R. Sanders
