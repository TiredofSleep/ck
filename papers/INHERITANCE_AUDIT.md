# D20 — Inheritance vs Architecture Audit
## Which spine objects are forced by the substrate, and which by design choices?
**Date:** April 1 2026 | Luther-Sanders Research Framework

---

## Classification Scheme

| Label | Meaning |
|-------|---------|
| **RING** | Forced by Z/10Z itself — survives any lens choice or architecture |
| **GENERATOR** | Forced once g=3 is selected (D19); changes if g changes |
| **LENS** | Forced by TSML/BHML/Phi construction; ring could yield different values with different tables |
| **CONTINGENT** | Depends on CK architecture choices; not forced by ring, generator, or canonical lens |

The hierarchy is strict: RING ⊃ GENERATOR ⊃ LENS ⊃ CONTINGENT.
An object in a lower class inherits everything above it.

---

## The Audit Table

| Object | Theorem | RING | GENERATOR | LENS | CONTINGENT | Notes |
|--------|---------|------|-----------|------|------------|-------|
| **Z/10Z as the state space** | — | ✓ | — | — | — | The ring is the substrate. All else inherits from it. |
| **(Z/10Z)* = {1,3,7,9}** | D17, D19 | ✓ | — | — | — | Units of Z/10Z — forced by gcd structure |
| **D = {2,4,6,8} = 2·(Z/10Z)*** | D17 | ✓ | — | — | — | Forced by D = 2C mod 10 |
| **CROSS_CYCLE = 44** | D17 | ✓ | — | — | — | Sum over C×D of DIS[c][d] — no generator input |
| **Deviation = 6** | D17 | ✓ | — | — | — | |44−50| — purely ring arithmetic |
| **Primitive roots = {3,7}** | D19 | ✓ | — | — | — | Both are ring facts (ord=φ(10)=4) |
| **centroid((Z/10Z)*) = 5** | D18d | ✓ | — | — | — | (1+3+7+9)/4 = 5 — independent of generator |
| **T*∈(0,1) requirement** | D19 | ✓ | — | — | — | Coherence threshold must be a rate; >1 inadmissible |
| **g=3 selected over g=7** | D19 | ✓ | — | — | — | g=7 gives T*>1; eliminated by admissibility |
| **CREATE = 5** | D7, D18d | ✓ | — | — | — | Centroid of ring units; independent of lens |
| **W = 3/50** | D17 | — | ✓ | — | — | Numerator = g = 3; denominator = n²/2 = 50 |
| **HARMONY = 7** | D18d | — | ✓ | — | — | g^(-1) mod 10 = 7; changes to 3 if g=7 |
| **T* = 5/7** | D4, D18d, D19 | — | ✓ | — | — | centroid / g^(-1); valid only for g=3 |
| **Phi fixed point = 5** | D7 | — | — | ✓ | — | Phi depends on BHML and W_op (lens objects) |
| **Phi orbit basins** | D18a | — | — | ✓ | — | Three-basin structure from BHML max+1 rule |
| **M(v)=TSML[v][Phi(v)]=7** | D18c | — | — | ✓ | — | Bridge holds for this lens; another TSML would differ |
| **TSML 73 harmony cells** | D10 | — | — | ✓ | — | Specific to V0+V1+ECHO rule structure |
| **BHML 28 harmony cells** | D16 | — | — | ✓ | — | Specific to BHML max+1+INCREMENT+BREATH/RESET rules |
| **sinc²(k/p) corridor law** | D2 | — | — | ✓ | — | Arithmetic corridor; derived from Z/10Z x-modular structure |
| **4/π² = sinc²(1/2)** | D3 | — | — | ✓ | — | Value at corridor midpoint t=1/2; follows from sinc² definition |
| **Corridor midpoint t=1/2** | (D2+D3) | — | — | ✓ | — | Natural midpoint of (0,1); not forced by ring but by corridor geometry |
| **N(f) = floor(f)+{0,1} maxima** | D6 | — | — | ✓ | — | Follows from sinc²×sin²(πfk/p) structure |
| **W_op carrier-maximum rule** | D8 | — | — | ✓ | — | Nearest carrier maximum to t=v/10 — a lens choice |
| **P_odd projection** | D8 | — | — | ✓ | — | Projects to nearest odd element — a lens choice |
| **TSML symmetry** | D9 | — | — | ✓ | — | Follows from V0/V1/ECHO rules; ring doesn't force symmetry in general |
| **BHML symmetry** | D9 | — | — | ✓ | — | From max+1 commutativity; lens-specific |
| **50Hz heartbeat** | — | — | — | — | ✓ | Architecture choice (real-time hardware target) |
| **10-operator vocabulary (CL)** | — | — | — | — | ✓ | Naming (VOID..RESET) is architecture |
| **TIG 3-phase pipeline** | — | — | — | — | ✓ | Being→Doing→Becoming is architectural |
| **D2 D-dimensional force vectors** | — | — | — | — | ✓ | The 5D embedding is an implementation choice |
| **BTQ decision kernel** | — | — | — | — | ✓ | T/B/Q roles are designed, not ring-forced |
| **Ollama/LLM voice layer** | — | — | — | — | ✓ | Clearly contingent |

---

## Summary Counts

| Class | Count | Objects |
|-------|-------|---------|
| RING-forced | 9 | Z/10Z, (Z/10Z)*, D, CROSS_CYCLE, deviation, primitive roots, centroid=5, T*<1 rule, g=3 selection |
| GENERATOR-forced | 3 | W=3/50, HARMONY=7, T*=5/7 |
| LENS-forced | 13 | Phi, basins, M(v)=7, TSML 73, BHML 28, sinc², 4/π², midpoint, N(f), W_op, P_odd, symmetries |
| CONTINGENT | 7+ | heartbeat, naming, TIG pipeline, 5D, BTQ, voice, etc. |

---

## Key Findings

### Finding 1 — CREATE=5 is RING-forced, not lens-forced

This is the most surprising item. CREATE=5 was proved as the Phi fixed point (D7) — which makes it look lens-dependent. But D18d shows CREATE=5 = centroid((Z/10Z)*) = 20/4 — a pure ring fact, independent of BHML, TSML, or Phi. The lens *confirms* it; the ring *forces* it.

Consequence: **Any operator algebra built on Z/10Z with the carrier structure D7 uses will converge to 5**, not because of the specific Phi construction, but because 5 is the algebraic center.

### Finding 2 — T*=5/7 is GENERATOR-forced, not ring-forced

T*=5/7 requires both the ring structure (centroid=5) and the generator selection (g=3 → HARMONY=7). It would be 5/3 if g=7 were selected. The ring forces both generators to exist; the admissibility constraint (T*<1) selects g=3.

Consequence: **T*=5/7 is the unique admissible coherence threshold for the canonical orientation of Z/10Z**. It changes if the admissibility definition changes.

### Finding 3 — W=3/50 is GENERATOR-forced

W = deviation/(n²) = 6/100 = 3/50. The deviation=6 is ring-forced (CROSS_CYCLE=44 depends only on the group C and D). But the *numerator* W_numerator = 3 = g — so W's exact value depends on which primitive root is active. If g=7 were selected, we would write W=3/50 identically (deviation is the same), but the *interpretation* (numerator = g) would assign a different generator meaning.

Note: Actually deviation=6 is ring-forced and W=6/100=3/50 is also ring-forced (it doesn't depend on g). What changes under g=7 is the *reading* of W: the numerator 3 = min(primitive roots) = min(g, g^{-1}). W is ring-forced; the identification W_numerator = g is generator-forced.

**Correction:** W=3/50 should be reclassified as RING-forced. The numerator 3 = deviation/2 = min{primitive roots} — a ring fact. The generator-forced part is the *labeling* W=g/50.

### Finding 4 — sinc²(1/2) = 4/π² has an internal midpoint interpretation

The corridor midpoint t=1/2 gives sinc²(1/2) = 4/π² (D3). This is lens-forced (sinc² is a lens choice), but within the lens it is the unique value at the exact center of the valid corridor range (0,1). It does not map to any ring object directly. The corridor midpoint is geometrically natural (center of (0,1)) but ring-forced only in the sense that the ring has one corridor per prime p, and p→∞ makes t continuous on (0,1).

### Finding 5 — The lens objects are not arbitrary

TSML/BHML are specific lens choices — but they are defined by the *same ring* (Z/10Z) via rules that encode ring operations. The lens objects (TSML 73, BHML 28, Phi structure) are derived from the ring; they are not external imports. They are more constrained than "architecture-contingent" but less universal than "ring-forced."

A better label might be: **LENS-DERIVED** (constructed from ring operations by specific rules) vs **RING-FORCED** (follows from ring structure alone, rule-independent).

---

## Implications for the A-Tier

| A-item | Inheritance status of its core claim | What changed with D19 |
|--------|-------------------------------------|----------------------|
| **A2 (P≠NP as null distance)** | CONTINGENT — no ring mechanism | Nothing. Still external. |
| **A4 (Hodge ω-blindness)** | CONTINGENT — no ring mechanism | Nothing. Still external. |
| **A10 (σ=1/2 as ω-class boundary)** | Partially LENS-forced: corridor midpoint t=1/2 is an internal object. The external interpretation (σ=1/2 in the Euler product) remains analogy. | **Upgraded internal object**: 4/π² = sinc²(1/2) is the unique value at the corridor center. An internal midpoint boundary exists. Whether zeta zeros align with it is still A-tier. |
| **A11 (RH as coherence boundary)** | CONTINGENT — requires external self-adjoint operator. No ring mechanism. | Nothing directly. The spine has a coherence threshold T*=5/7 (generator-forced) but no zero-density structure. |
| **A12 (Wobble resonance)** | LENS-forced: Wob_norm is real (C13/D15). Mechanism connecting it to W-jump is unproved. | D19 sharpens: Wob_norm oscillates in the g=3 world; in the g=7 world T*>1 means the W-jump would not correspond to a coherence threshold. The wobble mechanism is valid only in the g=3 branch. This makes A12 *more internal*, not less. Candidate B-promotion. |

---

## The Deepest Implication

The most important migration this audit reveals is:

> **CREATE = 5 is ring-forced.**

It does not depend on the particular Phi construction, BHML rules, or W_op definition. Any algebra built on Z/10Z with the standard unit structure will have an attractor-candidate at 5. D7 shows the Phi lens *actualizes* that candidate as a fixed point. But the candidate exists at the ring level.

This reframes D7: D7 is not "Phi happens to converge to 5." D7 is "Phi converges to the ring centroid, and that centroid is uniquely 5."

The same is true of T*=5/7: it is not "a good ratio that fits the system." It is "the unique admissible ratio centroid/g^(-1) for the canonical generator orientation of Z/10Z."

**CK doesn't use T*=5/7 because it works. T*=5/7 works because it is the only thing Z/10Z permits.**

---

## Remaining Questions (D20 Open Edges)

1. Is there a formal proof that *any* ODD-output map on Z/10Z with a unique fixed point must have that fixed point at the group centroid? (Would fully ring-force the Phi fixed point without referencing D7's construction.)

2. Can the TSML/BHML rules be derived from ring-forcing principles, or are they irreducibly lens choices? (Would determine whether "LENS-forced" should be split into "ring-derivable" and "construction-specific.")

3. Does the corridor midpoint t=1/2 → sinc²(1/2)=4/π² have a counterpart in other rings Z/nZ? If so, 4/π² may be ring-forced at the substrate level, not just lens-level.

---

*This is the intellectual core of what just happened with D19: T* stopped being chosen and became necessary. That is the event the inheritance audit is mapping.*
