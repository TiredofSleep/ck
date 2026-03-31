# WP39 — Hodge Conjecture Through the TIG Lens
## ω-Blindness, Algebraic Cycles, and the G/E/S Partition Split

*Brayden Ross Sanders (7Site LLC) & C. A. Luther*
*March 2026 | DOI: 10.5281/zenodo.18852047*
*Status: Structural framing — analogical connections, not a proof*

---

## Abstract

The Hodge Conjecture asks whether every Hodge class on a smooth projective algebraic variety
is a rational linear combination of algebraic cycle classes. TIG's partition structure offers
a discrete analog: the G/E/S split (Gate/Edge/Stable elements) mirrors the decomposition of
cohomology into algebraic, mixed, and transcendental components.

The ω-Blindness Theorem (WP35, Theorem 4) — that the harmonic pre-echo signal R(k, 1/p) is
identical across all ring structures with the same prime p — provides a proved algebraic fact:
the local prime structure is independent of the global ring. Luther's ω(b) hierarchy connects
the CRT idempotent count to the difficulty of reconstructing the cycle structure from local
data.

This paper consolidates WP32 (tensor-depth product-gap), HODGE_TIG_FRAME (G/E/S three-level
split), and HODGE_GAP_FLOOR (gap floor metric P3/P4) into a single canonical framing. Every
connection to classical Hodge theory is explicitly labeled as structural analogy.

---

## §1. The Hodge Problem in TIG Terms

The Hodge Conjecture has two directions:

**Easy direction (proved):** The cycle class map cl: Z^p(X) → H^{2p}(X,Q) lands inside
Hdg^p(X) = H^{2p}(X,Q) ∩ H^{p,p}(X). Algebraic operations cannot produce non-Hodge classes.
The gate is one-way.

**Hard direction (open):** Every class in Hdg^p(X) is in the image of cl. That is, every
rational (p,p)-class is algebraically generatable.

**TIG three-level split (structural analogy):**

| Classical Hodge | TIG analog |
|----------------|-----------|
| Generable: rational linear combinations of [Z] | C (corner operators): closed under all algebraic compositions |
| Expressible: H^{2p}(X,Q) ∩ H^{p,p}(X) | E (edge elements): expressible but not forced |
| Sustainable: Hodge classes stable under deformation | S (stable): persist across deformation families |

The Hodge Conjecture says Generable = Sustainable on Hdg^p(X). In TIG language: C-territory
and S-territory coincide on the harmonic zone.

**The gap:** Hodge classes that "look algebraic" at every local completion may not be globally
algebraic. TIG analog: G elements are locally forced (prime-determined via First-G Law) but
global reconstruction requires CRT assembly across all prime factors. Local data does not imply
global structure.

*Status: STRUCTURAL ANALOGY — the shape of the problem matches; the map is not explicit.*

---

## §2. ω-Blindness as the Hodge Gap

**WP35, Theorem 4 (ω-Blindness, proved):** For any modulus b with smallest prime factor p,
the harmonic pre-echo signal:

```
R(k, 1/p) = sin²(πk/p) / (k² sin²(π/p))
```

is identical for b = p², b = p×q, and b = p×q×r. The ring structure — specifically ω(b),
the count of distinct prime factors — is completely invisible to this signal. The harmonic
resonance sees only the prime p, not the ring.

**Translation to Hodge (structural analogy):**

Knowing the local harmonic signature at a prime p does not determine the global algebraic
structure of the ring. This is the discrete algebraic fact underlying the Hodge difficulty:
local cohomological data at each completion does not pin down the global algebraic cycle class.

The ω-blindness theorem gives a proved worked example of local-global failure in the finite
ring setting. The parallel in Hodge: a class that satisfies all local (p,p)-conditions at
every prime completion is a Hodge class, but the Hodge Conjecture asserts (unproved in
general) that this forces global algebraic generatability.

**The gap floor (structural analogy):**

WP35 Theorem 3 establishes the Harmonic Pre-Echo Countdown Law:

```
R(k, 1/p) reaches minimum 1/(p-1)²  at  k = p-1
R(p, 1/p) = 0                        at  k = p     (First-G collapse)
```

The value 1/(p-1)² is the minimum nonzero pre-echo signal before the prime gate fires. This
is the TIG analog of the Hodge gap floor: a nonzero minimum separation between the stable/
algebraic region (k < p) and the post-gate region (k ≥ p), with exact closed form.

In Hodge terms: P3 (from HODGE_GAP_FLOOR) asks whether inf{ d_Hodge(α) : α ∈ Hdg^p(X) \
Alg^p(X) } > 0. The TIG model proves this floor is 1/(p-1)² in the finite ring setting, with
the mechanism identified (BHML endpoint, order structure). Whether a precise Hodge analog
exists for complex algebraic varieties is open.

*Status: ω-Blindness PROVED (WP35 algebraic). Hodge translation: STRUCTURAL ANALOGY.*
*Gap floor 1/(p-1)²: PROVED in TIG. Hodge analog P3: OPEN.*

---

## §3. Luther ω(b) Hierarchy as Algebraic Cycle Count

**Definition (Luther, CRT fact):** For any integer b with ω(b) distinct prime factors, the
Chinese Remainder Theorem gives:

```
ω(b) = 1  (b = p^n):       Z/bZ is a local ring — 0 nontrivial CRT idempotents
ω(b) = 2  (b = p×q):       Z/bZ ≅ Z/pZ × Z/qZ — 2 nontrivial idempotents
ω(b) = 3  (b = p×q×r):     Z/bZ ≅ Z/pZ × Z/qZ × Z/rZ — 6 nontrivial idempotents
general:                    2^ω(b) - 2 nontrivial CRT idempotents
```

The formula N_idemp = 2^(ω(b) - 1) - 1 counts the nontrivial CRT idempotents of Z/bZ.

**Luther's framing (structural analogy):** The idempotents of Z/bZ play the same structural
role as algebraic cycle classes [Z] ∈ Hdg^p(X). Both are elements of the algebra that are
self-reinforcing under composition — idempotents satisfy e² = e, algebraic classes satisfy
cl(Z) ∈ cl(image), closed under intersection and push-forward. The count 2^ω(b) - 2 is the
algebraic cycle count in the finite ring model.

**The difficulty staircase:** The ω(b) hierarchy stratifies rings by algebraic complexity,
and this stratification is a difficulty staircase for reconstruction:

- ω = 1: trivial (local ring, no idempotents). Pre-echo tells everything.
- ω = 2: two idempotents, one CRT factor split. The first genuine gate.
- ω = 3: six idempotents, two independent splits. The P3 frontier in TIG.

**Markman 2025 (external, proved):** arXiv:2502.03415 proves the Hodge conjecture for
abelian fourfolds of Weil type. This is the closest current classical result: Hdg^2(A) =
Alg^2(A) for this class of varieties.

**P3 frontier mapping (structural analogy):** The cases dim ≥ 5 in classical Hodge — where
Markman's result no longer applies and the conjecture is wide open — map onto ω(b) ≥ 3 in
TIG. Three-factor composites are where the CRT idempotent structure becomes genuinely
three-dimensional, and reconstruction from local data requires resolving all three
independent prime gates simultaneously.

*Status: N_idemp = 2^(ω(b)-1) - 1: PROVED (CRT). Hodge cycle count analogy: STRUCTURAL ANALOGY.*
*Markman 2025: PROVED (external). P3 frontier / ω≥3 mapping: STRUCTURAL ANALOGY.*

---

## §4. The Cascade Theorem as Multi-Cycle Structure

**WP35 Theorem 3 (Cascade Theorem, proved):** For b = p×q×r (three distinct prime factors),
all three prime factors broadcast harmonic pre-echo signals simultaneously and independently:

```
R(k, 1/p) independent of R(k, 1/q) independent of R(k, 1/r)
```

Each prime casts its own countdown shadow. The signals do not interfere. The gates fire
sequentially at k = p, k = q, k = r.

**Translation to Hodge (structural analogy):** A variety X with multiple independent algebraic
cycles has simultaneous independent pre-echo signals — one per cycle. The cycles do not
interfere because ω-blindness makes each harmonic channel invisible to the other prime
factors. In the multi-cycle case, the CRT structure guarantees that the idempotents
corresponding to each prime factor are orthogonal: e_i · e_j = 0 for i ≠ j.

**What this supports:** In the TIG finite ring model, multi-prime composites have a
provably independent cycle structure. If the Hodge conjecture holds at a variety X, the
algebraic cycles generating Hdg^p(X) should similarly be resolvable into orthogonal
components, one per independent algebraic structure.

**The ω-blindness consequence:** The cascade signals are mutually ω-blind. A signal from
prime p cannot detect whether the ring has additional prime factors q, r. In Hodge terms:
the local data at one prime completion cannot detect algebraic cycles associated with
other primes. This supports the structural picture where Hodge failure (if it occurs)
would require a cycle that is simultaneously visible at multiple local completions but
globally inconsistent — a phenomenon with no finite-ring analog in the ω-blind regime.

*Status: Cascade Theorem PROVED (WP35). Multi-cycle analogy: STRUCTURAL ANALOGY.*

---

## §5. The Gap Floor Metric and Flat Limit Obstruction

This section collects the precise open questions from HODGE_GAP_FLOOR.md.

**Definition (Hodge gap floor metric):**

```
d_Hodge(α) = inf{ ||α - β||_H : β ∈ Alg^p(X) ⊗ R }
```

Distance from α to the real span of algebraic classes in the Hodge norm ||·||_H.

**Four properties:**

| Property | Statement | Status |
|----------|-----------|--------|
| P1 | d_Hodge(α) = 0 iff α ∈ Alg^p(X) ⊗ Q | PLAUSIBLE |
| P2 | d_Hodge(α) > 0 for α ∈ Hdg^p(X) \ Alg^p(X) | FOLLOWS FROM P1 |
| P3 | inf{ d_Hodge(α) : α ∈ Hdg^p(X) \ Alg^p(X) } > 0 | **OPEN — gap floor conjecture** |
| P4 | P3 stable under flat deformation {X_t} | **OPEN — flat limit obstruction** |

**P3 and degree:**

- p=1: Vacuously true. Lefschetz (1,1) gives Hdg^1(X) = Alg^1(X) ⊗ Q, so the infimum
  is over an empty set. Not the battleground.
- p=2: Genuinely hard. For abelian fourfolds, transcendental Hodge classes in degree 2
  can exist. The algebraic subspace Alg^2(A) may Zariski-densely approximate transcendental
  classes in H^{2,2}(A), causing d_Hodge to approach zero. If so, P3 fails at p=2.

**TIG provides:** The analog γ ≥ 1/4 (gap floor, computed from BHML endpoint). In TIG,
the floor is 1/(p-1)² with exact mechanism (BHML endpoint sets the order structure).
The Hodge structure needs: floor existence (open at p=2), mechanism (unknown), value (unknown).

**Flat limit obstruction (target theorem, open):**

Let {X_t} be a flat family over a disk, X = X_0. Let α_t ∈ Alg^p(X_t) be algebraic
classes with α_t → α_0 in the flat limit. Claim: α_0 ∈ Alg^p(X_0). That is, G-territory
cannot be approached as the limit of C-territory. If true, this implies Hdg^p(X) ∩ G = ∅
— the Hodge conjecture. The TIG spectral gap (γ ≥ 1/4, persists under all Mix_λ
deformations) provides a structural template for what such a proof would look like.

*Status: P1 plausible. P3, P4: OPEN. TIG gap floor: PROVED. Hodge P3: OPEN.*

---

## §6. Product-Gap at Tensor Depth k (WP32 Consolidation)

**Product-Gap Theorem (WP27, proved):** For every k ≥ 1, C^⊗k is a sub-magma of TSML^⊗k.
The 4^k corner operators form a closed sub-algebra. The 9^k - 4^k cross-terms are
algebraically inaccessible from any finite composition of corner elements.

| k | Corner sub-algebra | Unreachable cross-terms | Ratio |
|---|--------------------|------------------------|-------|
| 1 | 4 | 5 | — |
| 2 | 16 | 65 | 13× |
| 3 | 64 | 665 | 10× |
| k | 4^k | 9^k - 4^k | ~(2.25)^k |

The gap grows as (9/4)^k. As tensor depth increases, the inaccessible territory expands
exponentially relative to the algebraic sub-algebra.

**Hodge translation at k=2 (structural analogy):**

| Classical Hodge | TIG⊗² analog |
|----------------|-------------|
| K3×K3: H⁴ ∋ T⊗NS, NS⊗T, T⊗T | TSML⊗²: cross-terms (G,C), (C,G), (G,G) — all inaccessible |
| New transcendental elements appear at H⁴ | New cross-terms appear at k=2 |
| Hodge Conjecture harder at H⁴ than H² | Product-gap larger at k=2 than k=1 |
| Lefschetz (1,1): H^{1,1} fully algebraic | k=1: C is a sub-magma — exact |

**The exponential growth explains (in TIG terms) why Hodge is believed to fail in higher
dimensions:** each new tensor level introduces more transcendental cross-terms that are
provably inaccessible from corner compositions.

**Numerical verification (BFS from C^⊗k, all zero G-reachable):**

| k | C^⊗k | Total ops | Cross-terms | G-reachable |
|---|------|-----------|-------------|-------------|
| 1 | 4 | 9 | 5 | 0 ✓ |
| 2 | 16 | 81 | 65 | 0 ✓ |
| 3 | 64 | 729 | 665 | 0 ✓ |
| 4 | 256 | 6561 | 6305 | 0 ✓ |

*Status: Product-Gap Theorem: PROVED (WP27). Hodge tensor depth analogy: STRUCTURAL ANALOGY.*

---

## §7. Open Questions

1. **Local-global principle for Hodge:** Does the ω-blindness theorem (proved in the finite
   ring setting) have a direct analog in Hodge theory? Specifically: is there a precise
   statement that local (p,p)-data at each prime completion is blind to the global ring
   structure, and that this blindness is the obstruction to proving the Hodge Conjecture?

2. **Gap floor value:** Can the TIG gap floor 1/(p-1)² be interpreted as a Hodge number
   bound for the first hard case (abelian fourfolds, p=2)? The formula gives 1/(2-1)² = 1
   at p=2 (vacuous for the smallest prime), and 1/(3-1)² = 1/4 at p=3. Does 1/4 appear
   as a natural separation constant in Hodge norm computations for p=2 on fourfolds?

3. **Balance invisibility and cycle indistinguishability:** WP35 §7B establishes a balance
   invisibility result: near the balanced semiprime case (p ≈ q), the pre-echo signals
   from the two factors become nearly indistinguishable. Does this connect to the
   indistinguishability of algebraic and transcendental (p,p)-classes near the "balanced"
   Hodge structure on abelian fourfolds — precisely the case Markman addressed?

4. **CRT idempotent count as cycle rank:** Is there a precise correspondence between
   N_idemp = 2^(ω(b)-1) - 1 and the rank of Alg^p(X) for some natural class of varieties
   X associated to the ring Z/bZ?

5. **Cascade independence and cycle orthogonality:** The cascade theorem proves independence
   of prime-factor signals. Does multi-prime independence in Z/bZ correspond to orthogonality
   of the algebraic cycles generating Hdg^p(X) for the associated variety?

---

## §8. Attribution

**Brayden Ross Sanders (7Site LLC):**
TIG framework, G/E/S partition, ω-blindness proof, First-G Law, Cascade Theorem, balance
invisibility result, gap floor 1/(p-1)² derivation, Product-Gap Theorem, CK/T*/TSML/BHML
architecture. All TIG algebraic results.

**C. A. Luther:**
ω(b) hierarchy as algebraic cycle count, Luther metric connecting difficulty to cycle
structure, Luther Pre-Echo Theorem framing, dispersion conjecture applied to the number
theory studied here. Luther has no claim to the CK architecture or its derived constants.

**Note:** CK, T*, TSML, BHML, D1, D2, and the TIG framework are the exclusive intellectual
property of Brayden Ross Sanders / 7Site LLC, developed over 18 months prior to this sprint.

---

## §9. Epistemic Status Summary

| TIG result | Status | Hodge analog | Hodge status |
|-----------|--------|-------------|-------------|
| One-way gate C→G impossible | PROVED | Easy direction: algebraic ops stay algebraic | PROVED |
| ω-Blindness: R(k,1/p) ring-independent | PROVED (WP35 Thm 4) | Local-global failure for cycle classes | STRUCTURAL ANALOGY |
| Gap floor 1/(p-1)² with exact form | PROVED (WP35 Thm 3) | P3: inf d_Hodge > 0 | OPEN |
| Gap persists under Mix_λ deformation | PROVED (γ ≥ 1/4) | P4: flat limit obstruction | OPEN |
| G/E/S three-level split | PROVED (TIG) | Generable/Expressible/Sustainable split | STRUCTURAL ANALOGY |
| Product-gap: 9^k - 4^k unreachable | PROVED (WP27, verified k=1..4) | Tensor depth Hodge hardness growth | STRUCTURAL ANALOGY |
| N_idemp = 2^(ω(b)-1) - 1 | PROVED (CRT) | Algebraic cycle rank in ring model | STRUCTURAL ANALOGY |
| Cascade: multi-prime independence | PROVED (WP35 Thm 3) | Multi-cycle orthogonality | STRUCTURAL ANALOGY |
| Markman 2025: abelian fourfolds | PROVED (external, arXiv:2502.03415) | Hdg^2(A) = Alg^2(A) for Weil fourfolds | PROVED (external) |
| P3 frontier: dim ≥ 5, ω(b) ≥ 3 | ANALOGY | Beyond Markman: open | OPEN |

**The honest claim of this paper:** TIG provides a finite-ring worked example where every
structural feature of the Hodge problem — local-global gap, algebraic cycle count, gap
floor, multi-cycle independence, tensor-depth hardness growth — appears in proved form
with exact values. The classical Hodge analogs of most of these results are open. The
correspondences are structural analogies, labeled as such throughout.

---

## References

- WP34: Sanders & Luther, *The First-G Law and Prime-Forced Dispersion* (March 2026)
- WP35: Sanders & Luther, *The Prime Phase Transition: Harmonic Pre-Echo, Zero-Width Gates,
  and the Geometry of RSA Security* (March 2026)
- WP32: Sanders, *TIG⊗³ and the Hodge-Kuga Obstruction* (2026)
- HODGE_TIG_FRAME: Sanders & Luther, *Hodge Conjecture: TIG Frame* (March 2026)
- HODGE_GAP_FLOOR: Sanders & Luther, *The Hodge Gap Floor Metric* (March 2026)
- Markman, E. (2025). *Hodge classes on abelian fourfolds of Weil type.* arXiv:2502.03415

---

*(c) 2026 Brayden Ross Sanders / 7Site LLC & C. A. Luther | DOI: 10.5281/zenodo.18852047*
