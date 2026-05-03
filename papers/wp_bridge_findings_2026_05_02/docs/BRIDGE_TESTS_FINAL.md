# Bridge Tests: Final Honest Synthesis

**Date:** 2026-05-02
**Purpose:** Record everything that came out of the "out of rope" push, including all negative results from PSL(2,ℤ) lift attempts.

---

## §1 What was tested

The substrate has a per-digit integer invariant magnitude **±21 = ±3 × HARMONY** that survives two independent computations:

- **Ghys-analog v2** (TSML row vs BHML row asymmetry per digit, summed): **+21**
- **Period→trace bridge** (BHML self-period as candidate hyperbolic trace, with simple representative ((1,1),(t-2,t-1)) and classical Rademacher Ψ): **−21**

These are the same magnitude, opposite sign, derived two completely different ways from substrate self-iteration data.

The question: is ±21 a genuine Rademacher invariant for some hyperbolic conjugacy classes that BHML self-orbits naturally lift to, or is it a substrate-internal triangular number coincidence (T₅ + T₃ = 15 + 6 = 21)?

---

## §2 Five PSL(2,ℤ) lift strategies tested — all negative

For each digit n, take its BHML periodic orbit (e.g. digit 1: [2,3,4,5,6,7], period 6). Map the orbit to a PSL(2,ℤ) word via:

**(A.1) mod-3 letter map:** n%3=1 → T, n%3=2 → S, n%3=0 → identity. Sum Ψ = **−4**.

**(A.2) mod-2 letter map:** n odd → T, n even → S. Sum Ψ = **−1**.

**(A.3) σ-position T^k S:** map digit to T^k·S where k is its position in σ-cycle. Sum Ψ = **−1**.

**(B.1) up/down transition:** each step a → BHML(a,n), output > input → T, output < input → T⁻¹. Plus closing S. Sum Ψ = **0**.

**(B.2) T/T⁻¹ + S between:** transitions encoded as T or T⁻¹, with S inserted between every step. Sum Ψ = **0**.

**Substrate-native target:** ±21.

**No lift comes close.** Per-digit Ψ values from these lifts range from −2 to +3. The substrate's per-digit pattern (which gives ±21) is not reproduced by any of these natural encodings.

**Honest conclusion:** Naive operator-to-letter or transition-to-letter lifts don't capture the substrate's structure. The substrate's BHML self-orbits don't directly correspond to short S/T words in PSL(2,ℤ) under any of these encodings.

**File:** `/home/claude/tig_synthesis/orbit_to_psl2z.py`

---

## §3 Triangle group lift ruled out

The substrate has BHML period set {1, 2, 3, 4, 5, 6} (for digits 1-6) plus {4, 3, 2} (for digits 7-9). For these to be elliptic-element orders in some triangle group Γ_{p,q}, divisors of p and q together must cover {1, 2, 3, 4, 5, 6}.

**Tested coprime pairs (p, q) with p, q ≤ 9:** (2,3), (2,5), (2,7), (3,4), (3,5), (3,7), (3,8), (5,6), (5,7), (5,8), (5,9). 

**Result:** No small coprime (p, q) has divisors(p) ∪ divisors(q) ⊇ {1, 2, 3, 4, 5, 6}. Closest is (5, 6) which gives {1, 2, 3, 5, 6} — missing 4. And (5, 6) isn't coprime to itself wait — gcd(5,6) = 1, so it IS coprime, but order 4 is missing. Similarly (5, 8) covers {1, 2, 4, 5, 8} — missing 3 and 6.

**Sharpened observation:** BHML periods are NOT elliptic-element orders. They're trajectory periods of a dynamical system on Z/10Z. The correct modular correspondence is via Katok-Ugarcovici-style symbolic dynamics: each closed orbit of length L corresponds to a closed geodesic with L symbols in its coding (not to a finite-order group element).

So the bridge to PSL(2,ℤ) hyperbolic conjugacy classes goes through symbolic dynamics, NOT through the elliptic structure of any triangle group. This is consistent with Ghys's modular knot framework: the conjugacy classes are hyperbolic (closed geodesics), not elliptic.

**File:** `/home/claude/tig_synthesis/triangle_groups_test.py`

---

## §4 What the period→trace bridge actually says

The simple hyperbolic representative ((1,1),(t-2,t-1)) for trace t corresponds to the geodesic T^(t-1)·S in PSL(2,ℤ) — a cusp-passing geodesic with (t-1) cusp windings. Under this representative, Ψ = −(t-3) = −(period - 1).

For each digit n with period p(n) = 7-n (n in 1..6) or specific values for the 4-core, the period→trace bridge assigns:

- digit 1: trace 8, Ψ = -5 (would correspond to T^7·S geodesic, 7 cusp windings)
- digit 2: trace 7, Ψ = -4 (T^6·S, 6 cusp windings)
- ...
- digit 6: trace 3, Ψ = 0 (T^2·S, 2 cusp windings)
- digit 7: trace 6, Ψ = -3
- digit 8: trace 5, Ψ = -2
- digit 9: trace 4, Ψ = -1

**The interpretation requires:** that digit n's BHML self-orbit corresponds to the T^(p(n)+1)·S geodesic specifically. This is a hypothesis about how the substrate embeds in modular geodesic flow — not provable from substrate algebra alone.

If this hypothesis holds, ±21 IS a Rademacher invariant of substrate-natural hyperbolic conjugacy classes. If it doesn't, ±21 is a substrate-internal triangular-number coincidence (T₅ + T₃) along σ-orbit decomposition.

**The negative results above (§2-3) don't refute the hypothesis.** They just show that other natural lifts don't produce ±21. The simple-representative lift is special: it's the *one* lift under which the substrate's period structure naturally produces ±21 in a Rademacher framework. Whether this is contrived or whether it reflects the substrate's actual modular structure is unresolved.

---

## §5 What survives

The honest position after all the bridge tests:

**Empirically grounded:**

1. **Sharp trefoil characterization on corrected frame:** trefoil ⟺ multiset = {V, H, Br} or {V, Br, Br}. Nine triples total. Two multiset classes. (`trefoil_corrected_frame.py`, `trefoil_corrected_associativity.py`)

2. **Katok-Ugarcovici two-coding picture matches natively:** TSML_8 sends every digit to HARMONY in 1 step then escapes to flow (geometric coding); BHML_10 produces continued-fraction-like reduction with period(n) = 7-n encoding distance from cusp (arithmetic coding). (`reading_c_corrected.py`)

3. **±21 invariant survives two independent computations:** Ghys-analog v2 (+21), Period→trace under simple representative (-21). Decomposes as T₅ + T₃ along σ-orbits. (`rademacher_period_bridge.py`, `class_average_check.py`)

4. **Substrate doesn't factor through Z/2Z × Z/5Z:** Neither TSML nor BHML respects the Chinese Remainder decomposition. (`lacasa_corrected.py`)

5. **Forbidden patterns extremely strong:** 45/100 BHML output pairs forbidden, 46/64 TSML_8 output pairs forbidden. (`lacasa_corrected.py`)

**Honest negatives:**

1. **No naive PSL(2,ℤ) lift produces ±21.** Five strategies tested (mod-3 letter map, mod-2 letter map, σ-position T^k S, up/down transition, T/T⁻¹ + S between). Sums: -4, -1, -1, 0, 0. None match.

2. **No small triangle group Γ_{p,q} has elliptic orders covering substrate's period set.** {1,2,3,4,5,6} not realizable as divisors of any coprime pair (p,q) with p,q ≤ 9.

3. **TIG's grammar isn't a literal Borromean-prime condition** on any natural mod-k arithmetic.

4. **σ ↔ ST in SL(2,ℤ) gives elliptic elements, not hyperbolic ones** — wrong type for modular knots.

**Open hypothesis:**

The simple hyperbolic representative ((1,1),(t-2,t-1)) for trace t = period(n) + 2 might be the substrate-natural lift, in which case ±21 IS a Rademacher invariant of substrate-native hyperbolic conjugacy classes. This requires deriving the lift from substrate constraints rather than assuming it — an open research question.

---

## §6 Strategic position after all bridge tests

The framework's relationship to existing literature is now precise:

**TIG sits inside arithmetic-topology / modular-knot territory** with five empirically-grounded substrate-native facts (trefoil characterization, two-coding picture, ±21 invariant, irreducibility of 10, strong forbidden patterns). It uses arithmetic-topology *concepts* (paired magmas with cusp puncture, propagation grammar, two coding methods, triangular structures) without being reducible to arithmetic-topology *theorems* (Borromean density, Rademacher symbols on PSL(2,ℤ)).

**The arithmetic-topology bridge is conceptual, not literal.** TIG specifies admissibility on Z/10Z via substrate-internal composition rules; the literature specifies admissibility on Z (rational integers) via Legendre/Rédei symbols. They live in adjacent territory.

**For bridge papers and IHÉS pitch:** lead with the conceptual scaffolding (Morishita 2024 2nd ed, Ghys ICM 2007, Katok-Ugarcovici 2007, Matsusaka-Ueki 2023, Burrin-von Essen 2024) but be careful not to overclaim equivalence with their theorems. The ±21 invariant is the strongest substrate-native integer pattern; describe it as "an integer invariant that equals 3 × HARMONY in magnitude and decomposes as T₅ + T₃ along σ-orbits, with a hypothesis (not theorem) of Rademacher correspondence under the simple hyperbolic representative."

**For Faggin outreach:** present TIG as a substrate-native realization of Katok-Ugarcovici's two coding methods on Z/10Z, with a sharp trefoil characterization and a substrate-internal ±21 invariant. The conceptual framework draws on arithmetic-topology; the substrate is a new specific construction within that framework.

---

## §7 Files

All in `/home/claude/tig_synthesis/` and `/mnt/user-data/outputs/tig_synthesis/`.

**New in this push (after frame correction):**
- `trefoil_corrected_frame.py` — corrected trefoil set (9 triples, 2 multiset classes)
- `trefoil_corrected_associativity.py` — verifies trefoil = {V,H,Br} ∪ {V,Br,Br}
- `reading_c_corrected.py` — TSML_8 self-iteration shows interior-to-cusp dynamics
- `rademacher_period_bridge.py` — Ψ via period structure, sum = -21
- `lacasa_corrected.py` — substrate doesn't factor through CRT
- `orbit_to_psl2z.py` — five PSL(2,ℤ) lift strategies, all negative
- `triangle_groups_test.py` — no small Γ_{p,q} matches BHML period set

**Documents:**
- `CORRECTED_FRAME_BRIDGES.md` — synthesis of corrected-frame results
- `BRIDGE_TESTS_FINAL.md` — this document

---

## §8 Closing note on what was honest about this push

You said "forget my intuitions and stick with the math you produced." That meant stripping out:
- The (p,q) winding readings (Reading A's q-rule)
- Heuristic "every digit is a torus knot" framings
- Burrin-von Essen "matches" claim that I had overstated

What replaced them: only the canonical math (TSML_8, BHML_10, σ permutation, V/H flow cells, BHML self-iteration periods, propagation grammar from FORMULAS_AND_TABLES.md).

You also said "are you using the full torus function through TSML_8 and BHML_10?" — and I had not been. The trefoil-22 result was on the wrong frame. On the correct frame (TSML_8 + flow cells + BHML_10), the trefoil set is 9 triples in 2 multiset classes, and the algebraic characterization is sharp.

The bridge tests in §2 and §3 give honest negative results. The PSL(2,ℤ) lift question is unresolved — the substrate's structure doesn't naively map to S/T words. The ±21 invariant remains real on the substrate but its modular interpretation is a hypothesis pending a principled lift.

This is what the rope had left. The framework is now described precisely enough that the open questions are sharp, and the closed questions are settled.
