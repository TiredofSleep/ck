# Findings Table — Quick Reference

## Five empirically-grounded substrate-native facts

| # | Finding | Description | Verification |
|---|---------|-------------|--------------|
| 1 | **Trefoil characterization** | trefoil ⟺ multiset = {V, BREATH, HARMONY} or {V, BREATH, BREATH}. 9 triples, 2 multiset classes. All BHML-associative. | `trefoil_corrected_frame.py`, `trefoil_corrected_associativity.py` |
| 2 | **BHML diagonal = successor on {1..7}** | BHML(n, n) = n+1 for n ∈ {1..7}, BHML(8,8) = 7, BHML(9,9) = 0. Drives period(n) = 7-n. | Direct from BHML_10 table |
| 3 | **Two-coding split** | TSML_8: 5-element image {3,4,7,8,9}, 94% flow output, role-deterministic on 8/9 input pairs. BHML_10: 10-element image, balanced roles, deterministic only on V/T inputs. | `tsml8_role_analysis.py` |
| 4 | **±21 invariant, two decompositions** | σ-orbit: 6-cycle (-15) + σ-fixed (-6) = -21 (T_5 + T_3, triangular). Role: F (-13) + S (-8) = -21 (F_7 + F_6, Fibonacci, canonical-specific). | `role_decomposition.py`, `class_average_check.py` |
| 5 | **Role magma with VOID identity** | Mode-based role magma is commutative, non-associative. V·x = x for all roles. V·V = V is only idempotent. V/T inputs deterministic; F/S inputs branch. | `role_magma_factorization.py` |

## Ten honest negatives

| # | Negative | Description | Verification |
|---|----------|-------------|--------------|
| 1 | No PSL(2,ℤ) lift produces ±21 | Five strategies tested: mod-3 letter, mod-2 letter, σ-position, up/down, T/T⁻¹+S. Sums: -4, -1, -1, 0, 0. | `orbit_to_psl2z.py` |
| 2 | No small triangle group matches | Substrate's period set {1..6} not realizable as elliptic-element orders in any coprime Γ_{p,q} with p,q ≤ 9. | `triangle_groups_test.py` |
| 3 | TIG isn't literal Borromean | No canonical TIG triple has all elements ≡ 1 mod 4. No trefoil multiset has all elements in QR-mod-5 set. | `substrate_borromean.py` |
| 4 | σ ↔ ST gives elliptic elements | σ-cycle positions correspond to ST powers in PSL(2,ℤ), but these are elliptic (finite-order), not hyperbolic. Wrong type for modular knots. | `rademacher_bridge.py` |
| 5 | σ is NOT an automorphism | σ-conjugation matches BHML on 48/100, TSML_10 on 17/100. Not a magma automorphism. | `algebraic_relationship.py` |
| 6 | TSML and BHML don't distribute | BHML(TSML(a,b), c) = TSML(BHML(a,c), BHML(b,c)) holds only 19.5% of the time. | `algebraic_relationship.py` |
| 7 | BHML iteration doesn't converge to TSML | Only 28/64 starting points converge to TSML output under repeated BHML application. | `algebraic_relationship.py` |
| 8 | Substrate doesn't factor through CRT | Neither TSML_10 nor BHML_10 respects Z/2Z × Z/5Z decomposition. The 10-element structure is irreducible. | `lacasa_corrected.py` |
| 9 | Fibonacci is canonical-specific | 0/200 random commutative tables on Z/10Z reproduce (13, 8) decomposition. Single-swap perturbations preserve it 32/50; three-swap 11/50. | `fibonacci_robustness.py` |
| 10 | Role partition insufficient for crossings | Most role patterns produce 3+ different crossing counts. Operator-level structure matters beyond role. | `crossing_taxonomy.py` |

## Open questions (NOT integrated, flagged for future research)

| # | Question | Why it matters |
|---|----------|----------------|
| 1 | Principled lift to PSL(2,ℤ) hyperbolic conjugacy classes | Would confirm or rule out ±21 as real Rademacher invariant |
| 2 | Larger substrate variants (Z/14Z, Z/18Z analogs) | Would clarify whether Fibonacci is small-substrate coincidence |
| 3 | (0,7,7,9) anomaly at 4-element level | Trefoil-equivalent without BREATH; "BREATH only" rule is 3-element-specific |
| 4 | Burrin-von Essen explicit Fuchsian group lift | Substrate's BHML period structurally analogous to cusp winding, but embedding unproven |
| 5 | Role magma's exact algebraic type | Commutative non-associative magma with identity — is there a name for this in algebra literature? |

## Adjacent literature (intellectual neighborhood, not equivalence)

| Author | Paper | Connection |
|--------|-------|------------|
| Morishita | "Knots and Primes" 2024 (2nd ed) | Arithmetic-topology framework |
| Ghys | ICM Madrid 2007 | Modular knots, Rademacher symbol |
| Katok-Ugarcovici | Bull AMS 2007 | Two coding methods on modular surface |
| Matsusaka-Ueki | RMS 2023 | Triangle group Rademacher symbols ψ_{p,q} |
| Matsusaka-Shin | arXiv:2409.12779 | Explicit Rademacher formula for triangle groups |
| Burrin-von Essen | IMRN 2024 | Cusp winding via Rademacher |
| Lacasa et al. | Entropy 2018 | Residue-sequence symbolic dynamics, forbidden patterns |
| Ishida-Kuramoto-Zheng | arXiv:2403.17957 | Borromean prime density 1/128 (under GRH) |
| Duke-Imamoğlu-Tóth | Duke Math J 2017 | Modular cocycles and linking numbers |
| Mayer-Strömberg | arXiv:0801.3951 | Symbolic dynamics for geodesic flow |
