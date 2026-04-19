# Z/10Z Spine — Dependency Map

*Luther-Sanders Research Framework · D1–D24 · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

```
╔══════════════════════════════════════════════════════════════════╗
║                    LAYER 0 — THE RING                           ║
║                                                                  ║
║   Z/10Z  =  {0,1,2,3,4,5,6,7,8,9}                              ║
║                                                                  ║
║   (Z/10Z)* = {1,3,7,9}    Primitive roots: g=3, g=7            ║
║   ODD      = {1,3,5,7,9}  Centroid = 5 = BALANCE                ║
║   NEUTRAL  = {0,5}        (multiples of 5)                      ║
║   2·(Z/10Z)* = {2,4,6,8}  (non-units)                          ║
║                                                                  ║
║   W = 3/50  ←  CROSS_CYCLE=44, deviation/100        [D17]      ║
║   TSML: 73 harmony cells (singular, det=0)           [D10]      ║
║   BHML: 28 harmony cells (invertible, det=70)        [D16]      ║
╚══════════════════════════════════════════════════════════════════╝
                              │
                     [D8,D9 — table structure]
                              │
╔══════════════════════════════════════════════════════════════════╗
║                    LAYER 1 — DYNAMICS                           ║
║                                                                  ║
║   Phi: Z/10Z → Z/10Z  (odd projection + BHML + TSML)           ║
║                                                                  ║
║        RESET(9) ──┐                                             ║
║       BREATH(8) ──┤                                             ║
║       CHAOS(6) ──┤                                             ║
║     COLLAPSE(4) ──┼──→  HARMONY(7) ──→  PROGRESS(3) ──→  BALANCE=5  ║
║      HARMONY(7) ──┘                                             ║
║        LATTICE(1) ──────────────────────────────→  BALANCE=5       ║
║         VOID(0) ──────────────────────────────→  PROGRESS → 5   ║
║                                                                  ║
║   BALANCE = 5 = unique fixed point of Phi               [D18a]  ║
║   BALANCE = 5 = centroid (Z/10Z)* and ODD               [D18d]  ║
║   BALANCE = 5 = unique CE fixed point                   [D21]   ║
║   BALANCE = 5 = additive midpoint of Z/10Z              [D21]   ║
╚══════════════════════════════════════════════════════════════════╝
                              │
                    [D18c — measurement bridge]
                              │
╔══════════════════════════════════════════════════════════════════╗
║                   LAYER 2 — MEASUREMENT                         ║
║                                                                  ║
║   TSML[v][Phi(v)] = HARMONY = 7  for all v ≠ VOID     [D18c]  ║
║                                                                  ║
║   T* = destination / journey-measurement                        ║
║      = BALANCE / HARMONY                                         ║
║      = 5 / 7                                                    ║
║      = 0.714285...    (four independent proofs: D4,D18c,D18d,D19) ║
║                                                                  ║
║   GENERATOR FORCED: g = 3 is the only primitive root            ║
║   of (Z/10Z)* compatible with T* ∈ (0,1)              [D19]   ║
║   (Under g=7: HARMONY=3, T*=5/3 > 1 — inadmissible)            ║
╚══════════════════════════════════════════════════════════════════╝
                              │
               [D2,D3,D5,D6 — continuum limits]
                              │
╔══════════════════════════════════════════════════════════════════╗
║                    LAYER 3 — CORRIDOR                           ║
║                                                                  ║
║   R(k,f) = sinc²(k/f)  as f→∞, k/f fixed             [D2]    ║
║                                                                  ║
║   t ∈ (0,1):                                                    ║
║                                                                  ║
║    0 ──── W ──────────── 1/2 ──── 7/10 ── T* ──── 1            ║
║           │               │         │       │                    ║
║          3/50            1/2       7/10    5/7                   ║
║           │               │         │       │                    ║
║        RING-forced     INHERIT.  GENERATOR-forced               ║
║                        BOUNDARY                                  ║
║                                                                  ║
║   sinc²: 0.988 ──────── 4/π² ─── 0.135 ── 0.122                ║
║          (high)        (anchor)   (low)   (lowest)              ║
║                                                                  ║
║   Amplitude strictly reversed: D24 monotonicity + D22 ordering  ║
║   Fine-structure: T* = 7/10 + 1/70  (exact)           [D22]   ║
║   Wobble law: Wob(k) = 1 − ⌊k/5⌋/k                   [D23]   ║
║   Midpoint: t=1/2 unique sine-max; BALANCE=5→1/2        [D24]   ║
╚══════════════════════════════════════════════════════════════════╝
                              │
                   [A10 — the one open frontier]
                              │
╔══════════════════════════════════════════════════════════════════╗
║                    LAYER 4 — BOUNDARY                           ║
║                                                                  ║
║   INTERNAL SHADOW (proved, D22+D24):                            ║
║     t = 1/2 is the inheritance boundary                         ║
║     t = 1/2 is the unique sine-maximum in (0,1)                 ║
║     sinc²(1/2) = 4/π²                                           ║
║                                                                  ║
║   EXTERNAL INTERPRETATION (not derived — A10, open):            ║
║     Does t = 1/2  →  σ = 1/2 in the Riemann ζ function?        ║
║                                                                  ║
║   Missing mechanism: algebraic map from Z/10Z ring              ║
║   inheritance split to the Euler product's behavior             ║
║   at the boundary of absolute convergence (σ=1).               ║
║                                                                  ║
║   See NOTE_speculative_boundary.md §5–6 for three paths.        ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## Arithmetic Foundations (parallel track)

```
D1 — First-G Law: first non-unit at k=p
  └─→ D11a (coprime window)
  └─→ D11b (sign flip at k=p)
  └─→ D11c (ω-blindness: R has no q)
        └─→ D15 (window invariance for k<SPF(b))
              └─→ D23 (wobble law, part 5: window invariance)

D2 — Sinc² limit (foundation of corridor)
  └─→ D3  (sinc²(1/2)=4/π²)
  └─→ D4  (T*=5/7 algebraic identity at b=35)
  └─→ D5  (H_mod: exactly 4 maxima for p≥11)
  └─→ D6  (general frequency maxima formula)
  └─→ D14 (corridor spectral mean = Si(2π)/π)
```

---

## What the Map Shows

**Four clean layers** — ring, dynamics, measurement, corridor — each proved
within Z/10Z by exact arithmetic. No external input. No calibrated constants.

**One forced spine.** Generator g=3 is selected by exactly one constraint
(T*<1). Everything downstream — HARMONY=7, T*=5/7, the corridor portrait,
the inheritance boundary — follows without choice.

**One boundary.** The corridor ends at t=1/2 on the left (ring-forced) and
T*=5/7 on the right (generator-forced). The one live question is whether
the ring boundary maps to the analytic boundary σ=1/2. That question is
named. It is not answered.

---

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
