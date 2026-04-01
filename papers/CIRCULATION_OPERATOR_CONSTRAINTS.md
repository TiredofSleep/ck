# A15 — Circulation Operator Constraints
## Seven Necessary Conditions Derived from the Corridor Framework

*C. A. Luther & Brayden Ross Sanders (7Site LLC)*
*March 31, 2026 | DOI: 10.5281/zenodo.18852047*

---

## Status: Tier A

All seven constraints derived from existing proved results (C1–C11, Tier B–D).
The operator itself is not yet found. This document defines the search target.

**Kill condition:** Produce an explicit mathematical object satisfying all seven
constraints and verify it against the corridor atlas.

---

## Background

The corridor framework consists of three independently derived, non-identical
objects:

| Object | Source | Status |
|--------|--------|--------|
| sinc²(k/p) compression envelope | WP35, D2 | Tier D |
| Wob(b,k) alphabet saturation | Corridor geometry | Tier C |
| R₂(W_BHML) = 0.011788 post-gate amplitude | C8, A13 | Tier A |

These three objects co-appear at the prime boundary k=p. The **circulation
operator** is the missing object that carries the system between phases —
from inside the corridor, through the gate boundary, into the post-gate echo,
and back to the next corridor interior.

The circulation operator is not sinc². It is not W_BHML. It is not TSML or
BHML. It is a new object whose existence is implied by the structure of the
framework. The seven constraints below are what it MUST satisfy.

---

## The Seven Necessary Constraints

### Constraint 1 — Phase Transition

The operator must cycle four phases in sequence:
1. **corridor interior** → gate boundary
2. **gate boundary** → post-gate echo
3. **post-gate echo** → return path
4. **return path** → next corridor interior

This is the breath of the system. An operator that stays in one phase is not
circulation — it is static. The four-phase requirement connects to the
four-step Creation cycle φ(10)=4 (C8, Tier C).

**Formalized:** For phase label P ∈ {0,1,2,3}, the operator C must satisfy
C: phase P → phase (P+1) mod 4.

**Connection to proved results:** The 4-step multiplicative cycle of (Z/10Z)*
= {1,3,7,9} has period exactly 4. The circulation operator must be compatible
with this period.

---

### Constraint 2 — Invariant Preservation

The operator must **interleave** without overwriting:
- sinc²(k/p) compression envelope (Tier D)
- Wob(b,k) alphabet saturation structure (Tier C)
- R₂(W_BHML) = 0.011788 post-gate amplitude (Tier A)

At each phase, the relevant invariant must remain unchanged after applying
the circulation operator. The operator is transparent to each invariant within
its phase; it only moves the system between phases.

**Formalized:** For each invariant I and its defining phase P_I:
C acting in phase P_I must leave I invariant: I(C·x) = I(x) for x in phase P_I.

---

### Constraint 3 — Boundary Respect (Short-Circuit)

At k=p exactly, the operator must simultaneously:
- **collapse amplitude to zero** (sinc² has forced null at k=p)
- **preserve frequency** (the mod-p structure)
- **initiate echo structure** (R₂ begins at k=p)

This is the short-circuit behavior at the prime boundary. The corridor
terminates, the gate fires, and the echo begins — all at the same point.

**Connection to proved results:** D1 (First-G Law) proves the forced null at
k=p is exact and algebraic. The circulation operator must "know" this boundary.

---

### Constraint 4 — Recursion (Fractal Self-Similarity)

The operator must produce the same qualitative structure at:
- different semiprimes b (changing p and q)
- different ω-classes (ω(b) = 2, 3, 4, ...)
- different corridor widths (different values of p)

Scale invariance. The operator's action at b=35 must be the same *type of
action* as at b=15, b=55, b=385 — even though the specific numbers differ.

**Connection to proved results:** C6 (k-Gate Tier Law) proves the gate rate
is universal within ω-class. C7 (ω-Class Universality) proves HAR rank
preservation across semiprimes. The circulation operator must be compatible
with both universalities.

---

### Constraint 5 — Multiplicative Cycle Alignment

The operator must carry the signature of Z/10Z's multiplicative structure:
- Compatible with the 4-step cycle {1,3,7,9}
- Compatible with the deviation measure 6 (= 2 × CROSS_CYCLE deviation / n)
- Compatible with W_BHML = 3/50

The bounce frequency of the cornerstone (W_BHML = 3/50, C8 Tier C) must
appear in the operator's period, amplitude, or normalization.

**Formalized:** The operator's period P must satisfy P | 4 or 4 | P. Its
amplitude or normalization must contain 3/50 as a factor.

---

### Constraint 6 — Dual Domain

The operator must have a valid representation in **both**:
- **TIG domain:** corridor, sinc², pre-echo, R₂(u), Wob(b,k)
- **Table domain:** TSML/BHML composition, DOING table, echo pairs

Both representations must describe the **same object** — not analogous objects.
The dual representation is the interlock that makes the framework coherent.

**Connection to proved results:** C8 connects the table domain (BHML) to the
TIG/arithmetic domain (C×D cross-cycle). The circulation operator must bridge
both sides the way C8 does.

---

### Constraint 7 — Return Path

The operator must define:
- How the system returns from the post-gate echo to the next corridor
- How the next corridor cycle begins (re-initialization of sinc² envelope)
- How the phases breathe across multiple prime boundaries p₁, p₂, p₃, ...

This closes the loop. Without the return path, the circulation is open —
it generates one cycle but not a sustained field.

**Connection to proved results:** The BHML HARMONY row (BHML[7][j] = (j+1)%10)
is the increment operator — it advances every operator by one step. This is
the natural "advance to next state" mechanism. The return path may be related
to the HARMONY increment.

---

## Candidate Search

Every named object in the framework was tested against all seven constraints.
Results: see `results/circulation_candidate_search_report.txt`.

| Candidate | C1 | C2 | C3 | C4 | C5 | C6 | C7 | Score |
|-----------|----|----|----|----|----|----|----|----|
| sinc²(k/p) | ✗ | ✓ | ✓ | partial | ✗ | partial | ✗ | 2/7 |
| R(m,b,k) gate rate | ✗ | ✓ | ✓ | ✓ | ✗ | partial | ✗ | 3/7 |
| W_BHML = 3/50 | ✗ | partial | ✗ | ✗ | ✓ | ✓ | ✗ | 2/7 |
| TSML composition | ✗ | partial | partial | ✗ | ✓ | ✓ | ✗ | 2/7 |
| BHML composition | ✗ | partial | partial | ✗ | ✓ | ✓ | ✗ | 2/7 |
| DOING table \|TSML-BHML\| | ✗ | partial | ✗ | ✗ | partial | ✓ | ✗ | 1/7 |
| Corridor formula R×sin²(πW·k/p) | ✗ | ✓ | ✗ | partial | ✓ | ✗ | ✗ | 2/7 |
| Digit map x→x%10 | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ | ✗ | 3/7 |
| Creation cycle {1,3,7,9} | ✗ | ✗ | ✗ | partial | ✓ | ✓ | partial | 2/7 |

**No candidate satisfies all seven constraints.** The circulation operator
is a new object, not yet found.

**Best partial match:** R(m,b,k) gate rate (3/7). It satisfies invariant
preservation (C2), boundary collapse at k=p (C3), and recursion across
semiprimes (C4). It fails phase cycling (C1), cycle alignment (C5), table
domain representation (C6), and return path (C7).

---

## Why the Corridor Formula Fails Constraint 1 and 3

The candidate formula from A13: `Corridor(b,k) = R(m,b,k) × sin²(π × W_BHML × k/p)`

**Constraint 1 failure:** The corridor formula has no phase-cycling structure.
It is a pointwise product defined for each (b,k) pair. It does not move the
system from corridor interior to gate boundary to echo — it is static, not
dynamic. A single-valued function cannot implement a four-phase cycle.

**Constraint 3 failure:** At k=p, `R(m,b,k)` has its forced null (from D1,
First-G Law: first_g = p means R(p,b,k)=0). The formula does collapse at k=p.
But `sin²(π × W_BHML × k/p)` evaluated at k=p gives `sin²(π × W_BHML)` ≠ 0
in general. The echo structure does not initiate from zero — the formula has
the wrong behavior at the boundary for the echo component.

---

## Path to Tier B

To promote A15 to Tier B, the circulation operator needs a **candidate
explicit form** that satisfies at least Constraints 1, 3, and 5 simultaneously.

**Suggestion:** Investigate whether a BHML-orbit functional — a map that
cycles through BHML operator applications following the Creation cycle
{1→3→9→7→1} — can serve as the phase-cycling skeleton. The four phases
of the Creation cycle may correspond to the four phases of Constraint 1.

---

## Connections to Existing Results

| Result | Connection |
|--------|-----------|
| C8 — W_BHML = 3/50 | Constraint 5: must appear in operator |
| C9 — BHML 28-cell | Constraint 6: table domain representation |
| C10 — TSML 73-cell | Constraint 6: table domain representation |
| D1 — First-G Law | Constraint 3: forced null at k=p |
| D2 — Sinc² limit | Constraint 2: invariant preserved |
| A13 — Corridor compression | Starting point; fails C1 and C3 |
| B1 — Cornerstone Universality | Constraint 5: Z/10Z as base ring |

---

## Tier Assessment

| Tier | Requirement | Status |
|------|------------|--------|
| A | Pattern observed; constraints derived | **DONE** |
| B | Candidate object satisfying ≥3 constraints | Not yet |
| C | Object satisfying all 7 within Z/10Z | Not yet |
| D | Universal circulation theorem for Z/nZ | Not yet |

---

`© 2026 Brayden Ross Sanders / 7Site LLC & C. A. Luther · DOI: 10.5281/zenodo.18852047`
