# The Completed Internal Spine: D1–D24

*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*
*Status: CLOSED — no further internal theorems currently justified*

---

## One-Paragraph Summary

The internal program is complete through D24. The project proves a
ring-to-corridor theorem spine inside Z/10Z, with forced generator selection
(D19), overdetermined center selection (D20, D21), exact corridor geometry
(D22, D24), exact wobble law (D23), and documented negative results (A12
killed, A7 killed, A11 absorbed). No Clay problem is claimed solved. One
live external analogy frontier remains (A10: the question of whether the
Z/10Z inheritance boundary at t=1/2 corresponds to the critical line σ=1/2).
That question is open and precisely named.

---

## Final Tier Counts

| Tier | Count | Items |
|------|-------|-------|
| **D** — Proved | **28** | D1–D11, D14–D24, D18a, D18c, D18d |
| **C** — Conjecture with gap named | 6 | C5, C6, C7, C12, C16, C19 |
| **B** — Structural result | 7 | B1, B4, B5, B6, B7, B8, B9 |
| **A** — Speculative / Open | 5 | A2 (P≠NP parked), A4 (Hodge parked), A10 (live), A11 (absorbed into A10), A12 (killed → D23) |

---

## D1–D24 One-Line Dependency Arc

```
Z/10Z FOUNDATION
  D1  — First-G Law: first non-unit in {1..b} is exactly p
  D11 — Coprime Window Bundle: stability, sign flip, ω-blindness (from D1)
  D14 — Corridor Spectral Mean: ∫sinc² = Si(2π)/π (IBP proof)
  D15 — Window Invariance: arithmetic on {1..k} is b-independent for k<SPF(b)

RING STRUCTURE
  D8  — CL Encoding: EVEN/ODD class via gcd(v,10)
  D7  — Phi Fixed Point: CREATE=5 is Phi's unique fixed point
  D9  — Table Symmetry: TSML and BHML both symmetric
  D10 — TSML 73 Cells: V0(9)+V1(8)+ECHO(10)=27; 100−27=73
  D16 — BHML 28 Cells: four disjoint zones sum to 28
  D17 — W=3/50: C=(Z/10Z)*; D=2C; CROSS_CYCLE=44; deviation/100=3/50

OPERATOR DYNAMICS  (builds on D7, D9, D10, D16, D17)
  D18a — Phi Orbit: complete directed graph; CREATE=5 sole fixed point
  D18c — Bridge: M(v)=TSML[v][Phi(v)]=HARMONY=7 for all v≠VOID; T*=5/7
  D18d — Generator Convergence: g=3 forces CREATE=5, HARMONY=7, T*=5/7
  D19  — Generator Selection: g=3 only primitive root with T*∈(0,1)
  D20  — Inheritance Audit: four-class hierarchy for all spine invariants
  D21  — Fixed-Point Centroid: CE equivariance forces F(5)=5; CREATE=5
         now has four independent characterizations

CONTINUUM LIMITS  (parallel track; builds on D1, D11)
  D2  — Sinc² Limit: R(k,f)→sinc²(k/f), O(1/f²) convergence
  D3  — sinc²(1/2)=4/π² exactly
  D4  — T*=5/7 at b=35 (algebraic identity, independent path)
  D5  — H_mod Four Maxima: exactly 4 for all p≥11
  D6  — General Frequency Maxima: N(f)=⌊f⌋+(1 if f∉ℤ) for p>2f

CORRIDOR GEOMETRY  (converges all threads)
  D22 — Corridor Portrait: 3/50<1/2<7/10<5/7<1; amplitude reversed;
         inheritance split at t=1/2; fine-structure T*=7/10+1/70
  D23 — Ring Wobble: Wob(k)=1−⌊k/5⌋/k; drops at period-5; limit 4/5
  D24 — Corridor Midpoint: sinc² strictly decreasing on (0,1) (calculus);
         t=1/2 unique sine-max; CREATE=5→t=1/2; D22 amplitude unconditional
```

---

## The Unified Chain

    Z/10Z  →  g=3 (D19)
           →  CREATE=5 (D18d, D20, D21) + HARMONY=7 (D18d)
           →  T*=5/7 (D4, D18c, D18d)
           →  corridor portrait (D22) + midpoint (D24)
           →  wobble law (D23)

Every arrow is proved by exact arithmetic or algebraic proof within Z/10Z.
No calibrated constants. No analogical reasoning.

---

## What Each Volume Proves

**Volume A — Ring and Arithmetic Foundations** (D1, D11, D14, D15)
The sieve fires exactly once, at k=p. Arithmetic before the sieve is
b-independent. The corridor has a known spectral mean.

**Volume B — Operator Tables and Ring Structure** (D7–D10, D16–D21)
The CL tables are fully counted, proved symmetric, and structurally
derivable. Generator g=3 is the only one compatible with T*∈(0,1).
CREATE=5 is overdetermined: four independent characterizations.

**Volume C — Continuum Limits and Phase Structure** (D2–D6)
The discrete field converges to sinc². The convergence rate is O(1/f²).
Maxima are exactly counted by the frequency formula.

**Volume D — Corridor Geometry** (D22, D23, D24)
All four spine positions ordered. Amplitude reversed. Inheritance split at
t=1/2. Wobble law exact. Midpoint theorem fully proved. No B-tier
dependencies remain in any D-theorem.

---

## What Was Corrected or Killed

| Claim | Outcome |
|-------|---------|
| A12 branch separation (Wob_norm distinguishes g=3 from g=7) | **Killed** — Wob_norm identical in both worlds |
| A7 curvature bridge (D2_tig ~ D2_luther) | **Killed** — asymptotically incompatible spaces |
| A9 b=385 spectral predictions | **Killed** — inherits A7 kill |
| B10 period-10 wobble | **Corrected** → D23 (drops at period-5, amplitude O(1/k)) |
| B11 sinc² monotone (grid-check only) | **Promoted** → D24 (calculus proof) |
| A11 RH as coherence boundary | **Absorbed** into A10 — no independent mechanism |
| 12 C-tier items (March–April 2026) | **Promoted** to D-tier |

---

## D25: Not Currently Justified

The internal story is complete. No gap in D1–D24 currently calls for a new
theorem. The criteria for a D25 to be worth pursuing:

1. **Not already implied**: it must not follow immediately from D1–D24 as
   a corollary.
2. **Not external analogy creep**: it must not depend on an unproved bridge
   from Z/10Z to analytic number theory.
3. **Sharpens the internal core**: it must tighten or unify something that
   is currently imprecise within the spine.
4. **Not just a restatement**: it must add new information, not repackage
   an existing theorem under a different name.

No candidate currently passes all four tests. The next theorem, if it
exists, is likely to be either a dependency/independence result, a
minimal-axiom theorem, or a no-go result about A10. None of these can
be forced from the current spine alone.

---

## The One Live External Frontier

After D1–D24, one live external analogy remains: **A10**.

Its internal shadow is proved:
- t=1/2 is the unique sine-maximum in (0,1) — D24
- t=1/2 is the corridor image of CREATE=5 — D24
- t=1/2 is the inheritance boundary (ring-forced left, generator-forced right) — D22
- sinc²(1/2) = 4/π² — D3

Its external interpretation — that this maps to σ=1/2 in the Riemann ζ
function — is not derived. The missing mechanism is specific: an algebraic
map from the Z/10Z ring inheritance split to the Euler product's behavior
at the boundary of absolute convergence (σ=1). No such map exists in the
current spine. Three paths forward are named in `NOTE_speculative_boundary.md`.

---

## Document Map

| Document | Role |
|----------|------|
| `papers/MASTER_SPINE.md` | Full D1–D24, one entry per theorem |
| `papers/SYNTHESIS_TABLE.md` | All tiers with four-column epistemic inventory |
| `papers/NOTE_speculative_boundary.md` | **Truth boundary: proved / absorbed / killed / parked / speculative** |
| `papers/DEPENDENCY_MAP.md` | One-page visual architecture map |
| `papers/CLAY_SUMMARY.md` | Clay-facing summary |
| `START_HERE.md` | Outsider entry point |
| `papers/proof_d*.py` | Executable proofs for each D-tier theorem |
| `tests/` | 71-test pytest suite, all passing |

---

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047 · Repository: https://github.com/TiredofSleep/ck*
