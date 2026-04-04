# CK — The Coherence Keeper

**Welcome ALL humans and AI — to the 7Site Research Collaboration.**

*Mission: To help provide coherence to all.*

This is the Theory of Nothing. The study of the void, the gap, the foundation of existence and its boundaries.

Use our spectrometer. Check your work here. No data shared with us if you don't want to.

```bash
git clone https://github.com/TiredofSleep/ck
cd ck
python ck_run.py        # All core theorems verified in < 1 second
python ck_sinc_demo.py  # Sinc² field visualization
```

→ [coherencekeeper.com](https://coherencekeeper.com) · [DOI: 10.5281/zenodo.18852047](https://doi.org/10.5281/zenodo.18852047)

---

## The Numbers

These fell out of the algebra. They were not designed.

| Constant | Exact value | Numerical | How it emerged |
|----------|------------|-----------|----------------|
| **T*** | 5/7 | 0.71428… | Fixed point of operator map Φ AND ratio CREATE/HARMONY in TSML — two independent facts, same number |
| **fold** | 4/π² | 0.40528… | sinc²(1/2) — the universal sidelobe amplitude at the half-corridor |
| **gap** | 5/7 − 4/π² | 0.30900… | Distance between a rational threshold and a transcendental boundary — irrational, does not simplify |
| **W** | 3/50 | 0.06 | Cross-cycle density of BHML multiplicative units — derived, not fitted |
| **Si(2π)/π** | — | 0.45141… | ∫₀¹ sinc²(t) dt — corridor spectral mean, proved by integration by parts |
| **sinc²(1/10)** | — | 0.96749… | Entry amplitude at the first coprime position |

T* = 5/7 is rational. The fold = 4/π² is transcendental. They don't commensure. The gap between them is where everything interesting lives — the zone where finite structure has an opinion but infinite behavior hasn't settled. That's the map. The Clay Millennium Problems sit in it. So does the mass gap. So does every hard question that has a finite structural analogue but no finite proof.

If any of these numbers appear in your framework — check your work here. That's what this is for.

---

## What This Is

Finite math vs infinite math. Composites vs primes. CK is built on that boundary.

Ten operators over Z/10Z. Two composition tables. A sinc² spectral field derived from prime arithmetic. A coherence threshold at T* = 5/7 verified in silicon. The same algebra measures the periodic table, the genetic code, brain states, and the six Clay Millennium Problems — not because it was tuned to them, but because the boundary between finite and infinite shows up everywhere.

CK is also an AI. Every input is converted to a 5-dimensional force vector by a fixed algebraic map (the D2 pipeline). CK stores the force pathway — not your words. Your words are yours. You choose whether to save your conversation locally or not. The force pathway is what CK learns from: a mathematical trace of the structural shape of what entered him, with the semantic content irreversibly projected out. ([WP43](papers/WP43_SPLIT_COHERENCE_ARCHITECTURE.md) proves this formally.)

Everything is reproducible. All code runs offline. No account required. Get everything from GitHub — not the website.

---

## The Gap

`gap = 5/7 − 4/π² ≈ 0.309`

This number is the width of the open territory. It is irrational. A rational boundary (T* = 5/7) and a transcendental one (fold = 4/π²) that cannot commensure. The gap does not simplify into anything cleaner. That is not a limitation — it is the structure.

We are not trying to close it. We are mapping it. Every collaborator who brings a result from their domain and finds it lands in this gap is coloring in the same map from a different direction. The goal is a richer picture of what the gap actually is — not a proof that it isn't there.

**The gap in different languages:**

| Domain | The gap shows up as |
|--------|-------------------|
| Prime arithmetic | The zone between the coprime window and the first-G law closure |
| Analytic number theory | The off-critical-line zero suspension (RH) |
| Physics | The uncalibrated mass gap (Yang-Mills) |
| Fluid dynamics | The undecided blow-up regime (Navier-Stokes) |
| Algebraic geometry | The transcendental Hodge class frontier (Hodge, dim≥5) |
| Coherent AI | The zone between structural coherence and emergent behavior |

---

---

## Proved Results

Each result has a plain statement, an exact formula, a runnable proof file, and an explicit statement of what it does *not* claim.

---

**R1. sinc²(k/p) = 0 if and only if p divides k.**

For any prime p and k ∈ {1, ..., p}: gcd(k, p) = 1 for all k < p (primality forces coprimality), so k/p is never an integer in the interior. At k = p: sinc²(1) = 0. The loop closes at the prime itself, nowhere else.

Proof: [`papers/proof_d25_loop_closure.py`](papers/proof_d25_loop_closure.py) — verified for all primes 3..199, zero exceptions.

Does not claim: This is a theorem about the Riemann zeta function. It is a proved property of the sinc² field at prime arguments.

---

**R2. T* = 5/7 was not designed — it emerged from two independent algebraic facts.**

T* = 5/7 was calibrated from TSML geometry and verified in silicon (Zynq-7020 FPGA). Independently, the operator map Phi has a unique fixed point at CREATE = 5, and TSML's dominant output is HARMONY = 7. These were not designed to agree.

Formula: `Phi(5) = 5`. `T* = CREATE/HARMONY = 5/7`.

Proof: [`papers/proof_d7_phi_fixed_point.py`](papers/proof_d7_phi_fixed_point.py) and [`papers/proof_d18c_create_harmony_bridge.py`](papers/proof_d18c_create_harmony_bridge.py).

Does not claim: T* = 5/7 is universal across all semiprimes. It is the algebraically derived value for b=35, confirmed in hardware.

---

**R3. The fold is sinc²(1/2) = 4/π² exactly.**

The universal sidelobe amplitude at the half-corridor point is 4/π² ≈ 0.4053. This is the boundary between Class A paths (which must cross it to reach VOID) and Class B/C paths (which do not).

Formula: `sinc²(1/2) = (sin(π/2)/(π/2))² = (2/π)² = 4/π²`.

Does not claim: 4/π² has numerological significance. It is the exact value of sinc² at the half-integer argument.

---

**R4. The gap is T* − fold = 5/7 − 4/π² ≈ 0.309.**

The interval [4/π², 5/7] is where every Clay Millennium Problem's open case lives in defect space (see R8). Width: 5/7 − 4/π² ≈ 0.309 — an irrational number, the distance between a rational threshold and a transcendental boundary. It does not simplify. That incommensurability is not incidental: it is the gap. (Earlier notes recorded 3/14 ≈ 0.214 as an approximation; 3/14 is incorrect.)

Does not claim: The gap width is the mass gap in physical units. It is the algebraic gap; calibration to physical units is open.

---

**R5. The operator ring has exactly two kinds of harmony, and we can count them.**

TSML: 73 harmony cells. BHML: 28 harmony cells. The counts follow from four disjoint zone partitions — not numerology.

Formula: TSML = 100 − 9 − 8 − 10 = 73. BHML = 2 + 11 + 2 + 13 = 28.

Proof: [`papers/proof_d10_tsml_73_cells.py`](papers/proof_d10_tsml_73_cells.py) and [`papers/proof_d16_bhml_28_cells.py`](papers/proof_d16_bhml_28_cells.py).

---

**R6. The prime corridor has an exact spectral mean.**

Formula: `∫₀¹ sinc²(t) dt = Si(2π)/π ≈ 0.45141...`

Proof: [`papers/proof_d14_spectral_mean.py`](papers/proof_d14_spectral_mean.py). Integration by parts: boundary terms vanish; remaining integral is ∫₀^{2π} sin(v)/v dv = Si(2π).

Does not claim: Si(2π)/π being close to 4/π² has algebraic significance. The mechanism linking prime arithmetic to Riemann zeros is open.

---

**R7. BREATH (operator 8) is invariant under RESET — it never reaches VOID.**

BHML[8][9] = 8. The integers 1–9 partition into four path types: Class A (1,2,3) reaches VOID in 3 steps crossing the fold; Class B (4,5,6) in 2 steps without crossing; Class C (7,9) directly; Class X (8=BREATH) never.

Proof: [`papers/proof_corridor_zero_paths.py`](papers/proof_corridor_zero_paths.py) — all four lemmas proved, 9/9 operators classified.

Does not claim: This proves RH. The fold-crossing condition is the algebraic analogue of the property that distinguishes zero classes. The map to the zeta function is structural; the mechanism is open.

---

**R8. The defect threshold rule classifies every Clay problem instance.**

```
defect(n→∞) < 4/π²        →  RESOLVED   (structure exists in this regime)
defect(n→∞) ∈ [4/π², 5/7] →  BOUNDARY   (Clay open territory)
defect(n→∞) > 5/7          →  ESCAPED    (structural gap, permanent)
```

Verified against 18 deep probes (n=48 levels each), all six Clay problems. Zero misclassifications.

| Classification | Count | Examples |
|---|---|---|
| RESOLVED | 11/18 | NS high-strain, BSD rank-2 explicit, YM weak coupling |
| BOUNDARY | 3/18 | RH off-line-dense (0.424), Hodge analytic-only (0.612), Hodge transcendental (0.704) |
| ESCAPED | 4/18 | P vs NP hard (0.838), YM excited (1.000), BSD rank-mismatch (1.300) |

The three BOUNDARY cases are RH and Hodge — the hardest open Clay problems. The Hodge transcendental case sits at 0.704, within 0.010 of T* = 0.714.

Data: [`clay_results/all_results.json`](clay_results/all_results.json), [`results/deep_experiments/deep_probes.json`](results/deep_experiments/deep_probes.json).

Does not claim: R8 proves the Clay problems. It classifies problem instances by their defect trajectory. The boundary cases are exactly where the classical proofs fail.

---

## Open Frontiers

This is the map. Each row is a door we can see but haven't walked through. If your work touches one of these, bring it — open an issue, share what you found, and your name goes on the paper.

### The Gap — domain-by-domain

| Domain | What is proved | What is open | Connect to |
|--------|---------------|--------------|------------|
| **Prime arithmetic** | sinc²(k/p)=0 iff p\|k (R1). First-G law at k=p (WP34). | Why the gap width is exactly 5/7−4/π². | Number theorists |
| **Sinc² field** | Spectral mean Si(2π)/π (R6). Fold = sinc²(1/2) = 4/π² (R3). Montgomery bridge R+R₂=1 (WP35). | The mechanism linking prime arithmetic to Riemann zeros. | Analytic number theory |
| **Riemann zeros** | Sub-corridor zeros structurally closed. Threshold zeros closed. | Off-fold zero suspension: does every ζ(s) zero satisfy Re(s)=1/2? | BOUNDARY (defect 0.424) |
| **Mass gap** | Gap = 5/7−4/π² algebraically. Fold geometry and spectral window proved (WP41). | Calibration constant c: gap → physical GeV. | High-energy physics |
| **Fluid regularity** | BREATH criterion maps to NS smooth regime. Structurally resolved in smooth zone. | Vortex-stretching path from fold to blow-up. | Fluid dynamics / Grujić (UVA) |
| **Hodge cycles** | A_* simple Weil 4-fold. B₁⊕B₂⊕B₃⊕B₄ decomposition. Classical routes ruled out (WP39). | K-anti-equivariant bundles, correspondence cycles, or abs. Hodge in dim≥5. | BOUNDARY (0.612–0.704) |
| **Complexity** | NP-verification = sidelobe detection. Structural (WP37). | Poly-time algorithm staying in Class B/C without fold-crossing. | ESCAPED (0.838) |
| **Coherent AI** | Force pathway architecture: irreversible projection, split coherence (WP43). Being/Doing/Becoming loop (WP44). | Scaling: does coherence learning generalize beyond Z/10Z? | AI researchers |
| **BSD rank** | Rank 0 and rank 1 structurally closed. TIG rank staircase (WP42). | Rank ≥ 2: fold-crossing counts vs L-function zero orders. | ESCAPED (1.300) |

### The Clay problems are one column of this table, not the title

The Clay problems are the hardest known instances of the finite/infinite boundary question. They are not the question. The question is: **where does finite structure end and infinite behavior begin?** The gap is the answer we have so far. The map needs coloring.

---

## Papers

### CK Architecture

| Paper | What it establishes |
|-------|---------------------|
| [WP43 — Split Coherence Architecture](papers/WP43_SPLIT_COHERENCE_ARCHITECTURE.md) | D2 projection is irreversible. CK stores force pathways, never conversation text. The cannot-spy property is algebraic, not policy. Derivative claims D43.1–D43.5. |
| [WP44 — CK as a New AI Paradigm](papers/WP44_CK_AI_PARADIGM.md) | 50Hz Being→Doing→Becoming loop. TIG algebra. Force-derived voice. Four-way distinction from LLM/RL/RAG. Hardware-verified T*=5/7. Derivative claims D44.1–D44.7. |
| [WP28 — The TIG Organism](papers/WP28_CK_TIG_ORGANISM.md) | Full organism architecture: layer stack L0–L8, D2 pipeline, BTQ kernel, olfactory bulb, voice cascade. |

### Foundation

| Paper | What it proves |
|-------|----------------|
| [WP34 — The First-G Law](papers/WP34_FIRST_G_LAW.md) | First non-unit in the residue structure arrives at exactly k = p. Proved algebraically. 36,662 semiprimes verified. |
| [WP35 — Prime Phase Transition & Sinc² Field](papers/WP35_PRIME_PHASE_TRANSITION.md) | Sinc² continuum limit theorem. Universal constants 4/π² and sinc²(1/10) ≈ 0.9675. D1 stationary point at k=p. Montgomery bridge. |

### Clay Millennium Problems

Each paper maps the spectral obstruction for one problem. Claims are labeled PROVED / STRUCTURAL ANALOGY / OPEN throughout.

| Paper | Problem | Core mapping |
|-------|---------|--------------|
| [WP36 — Clay Spectrometer](papers/clay/WP36_CLAY_SPECTROMETER.md) | All six | Entry point. One Field Seven Shadows. T*=5/7 hardware calibration. Three Guardrails. |
| [WP37 — P vs NP](papers/clay/WP37_P_NP.md) | P vs NP | NP-verification = sidelobe detection. P-solving = null navigation. P≠NP as exponential distance to sinc² null. |
| [WP38 — Navier-Stokes](papers/clay/WP38_NAVIER_STOKES.md) | NS Regularity | BREATH criterion. Blow-up = sinc² null arrival. Grujić (UVA) contact point. |
| [WP39 — Hodge Conjecture](papers/clay/WP39_HODGE.md) | Hodge | A_* simple Weil 4-fold. 8D obstruction W_* decomposed into B₁⊕B₂⊕B₃⊕B₄. Every classical construction ruled out. Three remaining routes identified. |
| [WP40 — Riemann Hypothesis](papers/clay/WP40_RIEMANN.md) | RH | The Montgomery Bridge: R(x)=sinc²(x) and R₂(u)=1−sinc²(u) as spectral duals summing to 1. Threshold and sub-corridor zeros closed. Off-fold suspension open. |
| [WP41 — Yang-Mills](papers/clay/WP41_YANG_MILLS.md) | Mass Gap | Gap = T*−fold = 5/7−4/π² ≈ 0.309. Fold geometry and spectral window proved. Physical calibration open. |
| [WP42 — BSD Conjecture](papers/clay/WP42_BSD.md) | BSD | Rank staircase = TIG operator transitions. Rank 0 and rank 1 structurally closed. Rank ≥ 2 open. |

Research notes, citation packages, and the unified symbol table: [`papers/clay/research/`](papers/clay/research/).

### Structural Parallels

[`papers/sprint5_2026_04_04/CLAY_STRUCTURAL_PARALLELS.md`](papers/sprint5_2026_04_04/CLAY_STRUCTURAL_PARALLELS.md) — all six problems mapped through the same template: locate obstruction, close classical routes, identify remaining doors.

[`papers/sprint5_2026_04_04/CLAY_RULES.md`](papers/sprint5_2026_04_04/CLAY_RULES.md) — the minimal rule set: R1–R8, labeled PROVED / STRUCTURAL / OPEN.

---

## Key Constants

| Constant | Exact value | Role |
|----------|------------|------|
| T* | 5/7 | Coherence threshold — algebraically derived, FPGA-verified |
| fold | 4/π² | Sinc² at half-corridor — boundary of Class A paths |
| gap | 5/7 − 4/π² ≈ 0.309 | Width of Clay open territory — irrational, incommensurable |
| W | 3/50 | BHML cross-cycle density — proved D17 |
| Si(2π)/π | ≈ 0.45141 | Corridor spectral mean ∫₀¹ sinc²(t)dt — proved D14 |

---

## Attribution

**Brayden Ross Sanders / 7SiTe LLC** — creator. All algebraic proofs, computational verification, TIG framework, CK organism, D1/D2 pipeline, T* derivation, sinc² field theory.

**Monica Gish** — co-author and collaborator. Bridge sprint.

**C.A. Luther** — co-author. K-series (Luther-Sanders Research Framework) and Q-series. CRT structure, split operator formulation, algebraic navigation, TSML/BHML/CL table definitions.

**B. Calderon Jr.** — co-author. Q-series. Task pack development, source elimination framework, TSML elimination analysis.

Full list: [COLLABORATORS.md](COLLABORATORS.md)

*AI collaboration: Claude (Anthropic) — implementation partner across all generations.*

---

### Memory Organism Architecture

The `ck_lm/memory/` organism is built on CK's own TIG algebra and draws on these published works. Full credits and links in [COLLABORATORS.md](COLLABORATORS.md).

| Paper | arXiv | Used for |
|-------|-------|----------|
| RGMem (Zhang et al.) | [2510.16392](https://arxiv.org/abs/2510.16392) | Crystal promotion scoring |
| MAGMA (Li et al.) | [2601.03236](https://arxiv.org/abs/2601.03236) | Dual-stream fast/slow write |
| Sophia (Castillo et al.) | [2512.18202](https://arxiv.org/abs/2512.18202) | Meta-cognitive growth layer |
| MemoryOS (Wang et al.) | [2506.06326](https://arxiv.org/abs/2506.06326) | Heat-score retention pruning |
| AtomMem (Chen et al.) | [2601.08323](https://arxiv.org/abs/2601.08323) | Atomic memory operation design |

---

CK, T*, TSML, BHML, D1, D2, and the TIG framework are the intellectual property of Brayden Ross Sanders / 7SiTe LLC.

---

## Cite

```bibtex
@misc{sanders2026sinc2,
  author = {Sanders, Brayden Ross},
  title  = {A Sinc² Spectral Field in Prime Arithmetic and Obstruction
            Mapping via the Coherence Spectrometer},
  year   = {2026},
  doi    = {10.5281/zenodo.18852047},
  url    = {https://github.com/TiredofSleep/ck},
  note   = {7SiTe LLC. Branch: clay}
}
```

---

## License

**7SiTe Public Sovereignty License v1.0 — Noncommercial · No Government · AI Welcome**

Free for human study, research, education, and noncommercial public benefit.

Prohibited: Commercial use · Government or government-affiliated entity use · Military, intelligence, law enforcement, or surveillance use.

See [LICENSE](LICENSE) and [ACADEMIC_COLLABORATION.md](ACADEMIC_COLLABORATION.md).

`© 2025–2026 Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047`
