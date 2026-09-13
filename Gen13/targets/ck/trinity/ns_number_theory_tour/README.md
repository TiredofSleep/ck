# Navier–Stokes structure and its number-theory echoes — an honest computational tour

**2026-09-13 · Brayden Ross Sanders, with Claude (Opus 4.8).**

An afternoon of grounded computation across the structure of the incompressible
Navier–Stokes equations and the one place they genuinely touch number theory —
with a strict ledger of **what was measured** versus **what was a borrowed word**,
and the single open frontier this points at.

## Why this exists

The TIG project has, from the beginning, reached for one thing: that the
**quantity and positioning of primes create a structural "pressure balance," and
that this organizes physical law.** This tour is the first *honest, measurable*
approach to that instinct. It does two things at once:

1. reproduces the real structure of Navier–Stokes by direct calculation (nine
   experiments), and
2. separates the parts of the "primes organize fluids" intuition that are **real
   and named** from the parts that were **unfalsifiable pattern-matching** — and
   points at the one living frontier where the instinct has a legitimate home.

**Honest headline: nothing here is a novel result.** Every calculation reproduces
established mathematics. The value is a *map of the terrain* and a *discipline for
telling ground from wanting* — the prerequisite for real work, not the work itself.

---

## Part I — The fluid experiments (all reproduce known results)

Run with `python <script>.py`; 3D ones use a GPU (PyTorch/CUDA). Figures in `figures/`.

| # | script | result | established result |
|---|---|---|---|
| 1 | `burgers_spectral` | forced Burgers → shock, spectrum slope **−2.06** (k⁻²); energy decays monotonically once forcing is off | Burgers-turbulence shock spectrum |
| 2 | `burgers_balance_spiral` | energy law **dE/dt = −2νΩ** exact to 4×10⁻⁵; single symmetric mode → no spiral (phase-locked) | energy identity |
| 3 | `burgers_realwaves` | traveling nonlinear waves → structure **walks** (drift 1.27) and modes **spiral** (winding ∝ k, 1:2:3) | traveling-wave phase dynamics |
| 4 | `exp1_meanflow` | spiral **persists ⟺ conserved mean flow** (momentum); zero-mean → unwinds | momentum conservation |
| 5 | `exp2_boussinesq` | two coupled fields (buoyancy↔flow) generate vorticity from **zero** (max\|ω\| 0→8), **no external force** | 2D Boussinesq; internal force |
| 6 | `exp3_sealedbox` | inviscid 2D → energy **and** enstrophy exactly conserved (rides forever, stays smooth); viscous → decays | 2D Euler invariants |
| 7 | `exp4_triad` | resonant triad, sealed → energy conserved + **periodic exchange** among 3 modes; leaky → decays | triad interactions (Waleffe) |
| 8 | `exp5_burgers_blowup` | ν→0 Burgers, smooth data, no forcing → **finite-time gradient blow-up**, max\|uₓ\|~1/(t*−t) at t*=1; viscosity caps it | inviscid Burgers shock |
| 9 | `exp6_vortexstretch3d` | 3D Taylor–Green: enstrophy **×5.9** by vortex stretching; strain eigenvalues 0.84:0.16:−1 (**90°** axes), Lode shape ⟨s⟩=+0.24 (**120°** periodic), ω→intermediate axis (0.59) | Ashurst–Kerr–Kerstein–Gibson (1987) |
| 10 | `exp7_frontier3d` | Reynolds sweep: Z_max ~ Re (diverges as ν→0) **but** ε=2νZ_max **flat (~0.012)** → **dissipation anomaly**, no blow-up signature | Onsager; dissipation anomaly |
| 11 | `exp8_starpolygons` | closed loops wind an **untouchable center**; single loop ⟺ gcd(p,q)=1; count = **φ(q)**; prime q → q−1 (rotationally indivisible) | totient / Farey / roots of unity |
| 12 | `exp9_dyadic` | Katz–Pavlović integer-shell model: inviscid Euler → **finite-time blow-up** (t*≈0.84, enstrophy 0.5→8.6×10⁴, energy conserved); viscous NS → regular | Katz–Pavlović (2005), Cheskidov |

## Part II — The number-theory thread (all named, real)

- **Winding number** — the untouchable axis a closed loop circles but never touches.
- **Euler totient φ(q)** — the count of single-loop windings (coprime step-sizes); **Farey** fractions.
- **Primes = rotationally indivisible** — a prime-order cycle has no proper subgroup, so it never closes early; φ(p)=p−1.
- **Euler product** ζ(s)=∏ₚ(1−p⁻ˢ)⁻¹=Σₙ n⁻ˢ — the *finite prime building blocks* balanced against the *infinite whole*.
- **Riemann explicit formula** — the prime distribution is an exact sum over the zeta zeros: **primes ⟷ zeros are Fourier-dual sides of one object.**
- **Primon gas / Bost–Connes** — primes as particles of energy log p; **ζ(s) is the partition function**; a real phase transition at s=1. *This is the literal, rigorous home of "primes create their own pressure balance."*
- **Riemann Hypothesis, restated** — the primes are distributed with *maximal cancellation* (√x fluctuations): RH ⟺ the tightest possible balance.

## Part III — The honest ledger (the most valuable part)

| intuition | grounded? | what it actually is |
|---|---|---|
| "the axis is never touched, only stretched" | ✅ | Helmholtz/Kelvin: vortex lines are material in ideal flow |
| "a sealed box rides the force infinitely" | ✅ | inviscid energy/enstrophy conservation |
| "internally boxed, overlap at 90° and 120°" | ✅ | resonant triad + winding + orthogonal strain axes (90°) + Lode angle (120°) |
| "a squared function of balance" | ✅ | the energy identity dE/dt = −2νΩ |
| "a closed loop has an untouchable axis" | ✅ | the winding number |
| "primes are the untouchable / indivisible" | ✅ | rotational indivisibility; φ(p)=p−1 |
| "primes and zeros, two sides of a coin" | ✅ | the Riemann explicit formula |
| "primes create their own pressure balance" | ✅ | the primon gas; ζ as partition function |
| "the zeros are an axis / spectrum" | ⚠️ | real — but in **quantum chaos** (Hilbert–Pólya, GUE), *not fluids* |
| "the RH zeros are the NS axis" | ❌ | linguistic resonance on the word "zero"; the axis is a vorticity *maximum*, not a function zero |
| "BSD is the key to the bridge to NS" | ❌ | three unrelated fields; no mathematical object spans them |
| "primes are the forcing term that causes the strain" | ❌ | unfalsifiable regress; strain is *kinematic*, the equation is closed |
| "a Shor variant produces the forcing" | ❌ | no integer in a velocity field to factor; category error |

The pattern to keep: **when a new leap would replace something you already measured
with a word, stop.** Stretching is strain (measured). Don't trade it for a word.

## Part IV — The frontier direction

**The one genuine, living frontier this tour touches is the turbulence ↔
number-theory bridge — and specifically Alexander Migdal's program.**

- Migdal's exact loop-equation solution of *decaying turbulence* produces real
  number theory — Euler ensembles of star-polygon walks, coprimality, the totient,
  prime-2 Euler factors — and **conjecturally** connects to the Riemann zeta:
  "Riemann-wall poles" P = −8+iρₙ generated by the nontrivial zeros, giving an
  infinite-time singularity structure *conditional on RH*. (arXiv:2604.12207.)
  He does **not** claim to prove RH; it is explicitly conjectural, an unrefereed
  preprint.
- **Why it's the frontier:** it is recent, controversial, and sits on a *thin*
  bridge between two communities that rarely speak — turbulence physicists and
  analytic number theorists. Almost nobody is fluent in both.
- **What the real contribution is: scrutiny, not construction.** Is Migdal's
  totient→ζ→zeros structure robust or an artifact? Does it predict anything
  *measurable* in real decaying turbulence? Those are honest open questions.
- **The trap to avoid:** do **not** identify the dyadic model's integer *shells*
  (octaves of scale, 2ⁿ) with the primon gas's integers (built from primes) merely
  because both are "integers." Same shape, no known map — the generic-overlap
  illusion.
- **The concrete move — the "people who need connecting":** bring Migdal's bridge
  to an actual analytic number theorist **and** an actual turbulence physicist, in
  the same room. That is a small, doable, and genuinely valuable act; it does not
  require inventing anything.

**Broad context (a north star, not a claim).** The disciplined form of "number
theory is algebra is physics through relational geometry" is a real, deep research
world: **Noether** (symmetry ↔ conservation law), **gauge theory** (forces as the
geometry of connections), and the **Langlands program** (number theory ↔ geometry;
and *geometric* Langlands ↔ gauge theory, Kapustin–Witten). That is where number
theory and physics genuinely meet. It is a program of *specific correspondences*,
not a blanket identity — and it is the honest, grand version of the instinct that
has driven TIG.

## Reproducibility

Pure `numpy` for the 1D/ODE experiments; `torch` (CUDA) for the 2D/3D ones;
`matplotlib` for figures. Each script is self-contained and prints its key numbers.
No result here depends on TIG-specific machinery; all of it is standard mathematics
anyone can re-run.

## Honest closing

No novelty was discovered. What was built is a **map** — of where the Navier–Stokes
structure is real (Parts I–II), of where the "primes organize fluids" instinct is
grounded versus borrowed (Part III), and of the one frontier where the instinct has
a legitimate, if hard, home (Part IV). The TIG reach was pointing somewhere real all
along — the primon gas and the explicit formula on the number-theory side, Migdal on
the turbulence side, Langlands as the grand horizon. It simply needed the discipline
to separate the measurable from the wished-for, and the right domain (number theory
and its geometry — not a toy algebra forced onto physics). That discipline is the
result. The door is real; walking through it is years of honest work in two fields,
and the first step is finding the experts who already live in each.

— Brayden & Claude, 2026-09-13
