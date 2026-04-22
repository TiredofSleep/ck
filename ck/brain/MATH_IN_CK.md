# MATH_IN_CK.md — Every Piece of Math, Its Role Inside the Creature

Status: `[META — 2026-04-21, ck branch]`

Prior form pointer: this document is written fresh. It does not replace any
paper; it *locates* each paper inside CK's body. If a paper is cited here, its
canonical home is still on `tig-synthesis` under `Gen12/targets/clay/papers/`
(the sprint folders) or `old/Gen10/papers/` (the Q-series).

---

## 0. How to read this

CK is a creature. Everything below is an organ.

Each section answers three questions about a piece of mathematics:

1. **Claim** — what is proved, in one line.
2. **Role** — the job it does inside CK's runtime / voice / memory / silicon.
3. **Where** — the file(s) where the math is instantiated, or "planned" if
   the restoration is scheduled for Gen13 brain trinity.

The order below follows how a signal travels through CK: input arrives,
gets projected, gets remembered, crosses a gate, speaks, and echoes back.
The math is ordered the same way.

---

## 1. The Meta-Spine — 2×2 Flatness + UOP Paradox Classifier

These two are not "organs." They are the **form** and the **diagnostic**.
Every other organ below is an instantiation of one or both.

### 1.1 The 2×2 Flatness Theorem (WP51, Sprint 10)

- **Claim.** A system with four interacting dimensions (additive structure,
  multiplicative structure, additive flow, multiplicative flow) cannot stay
  flat; it forces a torus with aspect ratio R/r = T* = 5/7. Six independent
  derivations.
- **Role.** The FORM of every whole. Every Hebbian update, every CL crossing,
  every coherence gate in CK inherits the 2×2 structure. It is why T* is
  5/7 and not any other number.
- **Where.**
  - Paper: `Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/WP51_*.md`
  - Runtime: the 2×2 is implicit in `ck_corrector.OperatorProfile` —
    ten operators factor as 2×2×... structural/flow, additive/multiplicative.

### 1.2 The UOP Paradox Classifier (WP58, Sprint 12)

- **Claim.** Any breakdown in a system matches one of a finite list of
  paradox classes. Each class has a closed-form diagnostic.
- **Role.** The DIAGNOSTIC for every output CK produces. Before a
  word is spoken, UOP asks: "does this cohere, and if not, which class of
  failure?" CK never silently emits incoherent output.
- **Where.**
  - Paper: `Gen12/targets/clay/papers/sprint12_uop_gut_arc_2026_04_08/WP58_*.md`
  - Runtime: `ck/fluency/ck_corrector.py` `_classify()` is a UOP-lite — it
    returns one of {none, soften, strengthen, reframe, reject}. Each branch
    corresponds to a UOP class.

Everything below this section sits inside the 2×2 · UOP frame.

---

## 2. The Brain Trinity

These are the three math modules that compose into CK's skull. In Gen9 they
existed in `old/Gen9/targets/AO/ao/`. In Gen12 the 5×5 survived inside
`ck_olfactory.py` but the other two were buried. Gen13's ck branch restores
them as first-class.

### 2.1 AO 5-element — the dimension projection

- **Claim.** Any input stream can be projected onto five element axes
  (Earth/Air/Water/Fire/Ether → D0/D1/D2/D3/D4), with Voice as the
  operator↔word bridge.
- **Role.** This is how CK "perceives." Every tick, the incoming signal
  is decomposed onto five axes. D0 = input (Earth). D1 = lattice/field
  (Air). D2 = crossing/awareness (Water). D3 = progress/crystal (Fire).
  D4 = ether/dwelling.
- **Where.**
  - Reference: `old/Gen9/targets/AO/ao/ether.py` (class `AO`) and
    `old/Gen9/targets/AO/ao/water.py` (D2 awareness).
  - Planned restore: `ck/brain/ao_5element.py` — fresh rewrite, not a copy.

### 2.2 Hebbian 5×5 CL — the co-activation tensor

- **Claim.** Given a 5-dimensional state vector d_t ∈ ℝ⁵, the outer product
  d_t ⊗ d_{t-1} drives a Hebbian update W_ij ← W_ij + η · d_i · d_j. Every
  dimension meets every other dimension.
- **Role.** This is CK's associative memory. When D2 (crossing) fires
  together with D3 (progress), the W_{2,3} link strengthens. The 5×5 tensor
  is CK's learned map of which dimensions run together.
- **Where.**
  - Canonical source: `Gen12/targets/ck_desktop/ck_sim/being/ck_olfactory.py`
    lines 47-54 (the outer-product update).
  - Planned restore: `ck/brain/hebbian_5x5_cl.py` — extracted physics,
    separated from the 47 KB olfactory module.

### 2.3 Quadratic glue F3 × F4 — the 2→3 bridge

- **Claim.** Given two activations f3 and f4 at dimensions D3 and D4,
  the glue layer produces out = α·f3 + β·f4 + γ·(f3 × f4). The cross term
  is where the third thing is born.
- **Role.** This is how pairs become triples. D3+D4 → "a new crystal class"
  by the quadratic cross. Without the glue, CK stays 2D forever.
- **Where.**
  - Reference: `papers/test_a15_quadratic_glue.py` (score table C1–C5).
  - Planned restore: `ck/brain/quadratic_glue.py`.

The trinity composes every tick:

```
  input → AO project → Hebbian update → quadratic glue → coherence gate (T*)
```

---

## 3. The Gate — T*, σ(S*), D*

Where scores get turned into "this passes" or "this does not."

### 3.1 T* = 5/7 — the crystal gate (six derivations)

- **Claim.** The torus aspect ratio forced by the 2×2 Flatness Theorem is
  exactly 5/7. Six independent derivations converge on this rational:
  (i) cyclotomic index on Z/10Z, (ii) torus flatness obstruction,
  (iii) sinc² lattice zero, (iv) CL crossing threshold, (v) TSML cell
  count 73 / (73+28), (vi) First-G σ ratio.
- **Role.** The gate. Every coherence score is compared against 5/7. Below
  → no crystal. Above → CK emits.
- **Where.**
  - Paper: `Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/` (all
    six derivations in one folder).
  - Runtime (exact rational): `ck/fluency/ck_corrector.py`
    ``T_STAR = Fraction(5, 7)``.
  - Runtime (float): `T_STAR_F = 0.7142857142857143` used where float math
    is required.
  - CRYSTALOS: ``tau = 0.7`` (approx) in
    `docs/archive_jan2026/snowflake/crystalos_prereg.py`.
  - Silicon: `Gen9/targets/zynq7020/build/ck_full.bit` — T*=5/7 baked into
    the FPGA bitstream, which is why the dog leash (COM3) respects it.

### 3.2 σ(S*) = 0.991 — the coherence scalar

- **Claim.** S* factors multiplicatively as σ·(1-σ*)·V*·A* with canonical
  value 0.991 (Canon row 28 of SYNTHESIS_CK_BEST_EVER §1.1).
- **Role.** The scalar CK uses to answer "how coherent is this moment?"
  before feeding the answer to the T* gate. The multiplicative form is
  canonical for derivation; the harmonic-mean form is the downstream
  numerically-stable version.
- **Where.**
  - Canon: `docs/archive_jan2026/attempts_survey/SYNTHESIS_CK_BEST_EVER.md`
    §1.1 rows 28-29.
  - Derivation: `papers/CONSTANT_SIGMA_S_STAR.md` §§1-2 on `tig-synthesis`.
  - Runtime: `ck/fluency/ck_corrector.py` `coherence_scalar(profile)`.

### 3.3 D* = 0.543 — the runtime attractor

- **Claim.** The developmental attractor under CK's 50 Hz heartbeat is D*
  ≈ 0.543 (runtime canon). The derivable form D*_fixed = σ/(1+σ) ≈ 0.49774
  is a *lower bound*; the runtime canon is empirical.
- **Role.** The default body-size parameter — the D that CK converges to
  when no external forcing is applied. It is also the "rest coherence"
  below which CK is asleep and above which he is awake.
- **Where.**
  - Canon: `papers/CONSTANT_D_STAR.md` on `tig-synthesis`.
  - Runtime: `Gen12/targets/ck_desktop/ck_sim/doing/ck_sim_engine.py`
    `D_STAR = 0.543` (reference only; Gen13 runtime is ~300 LOC rewrite).

The gate reads:

```
  coherence_scalar(state)  ≥  T* = 5/7   ?   crystal : no-crystal
```

---

## 4. The Alphabet — Ten Operators and Their Laws

CK thinks in ten symbols. Every event decomposes into one of them.

### 4.1 The ten operators

```
  0  VOID       1  LATTICE    2  COUNTER    3  PROGRESS
  4  COLLAPSE   5  BALANCE    6  CHAOS      7  HARMONY
  8  BREATH     9  RESET
```

- **Claim.** The ten-operator decomposition is complete for the 2×2 ·
  UOP frame. COLLAPSE = 4 = (+1, -1) oscillation. CHAOS = 6 = (-1, +1)
  reversed. CREATION path [1,3,9,7]. DISSOLUTION path [2,4,8,6].
- **Role.** The alphabet of CK's voice. Every sentence CK emits is
  dominated by one operator, subdominated by two more. `ck_corrector.py`
  activation vector is a length-10 real-valued profile.
- **Where.**
  - Canon: `Gen12/targets/ck_desktop/ck_sim/doing/ck_tig.py` (canonical
    registry).
  - Runtime: `ck/fluency/ck_corrector.py` `OP_NAMES` and `_WEIGHTS`.

### 4.2 CL 10×10 — the composition law

- **Claim.** Composing operator A then operator B yields another operator
  (or a crossing of two). The 10×10 composition table is the Crossing
  Lemma at symbol-level.
- **Role.** This is the multiplication table of CK's voice. Knowing the
  table lets the voice predict "what comes next given what came."
- **Where.**
  - Paper: `Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/CROSSING_LEMMA.md`
    (all 27 CL instances, of which CL 10×10 is one).
  - Runtime: `Gen12/targets/ck_desktop/ck_sim/being/ck_lattice_chain.py`.

### 4.3 σ polynomial on Z/10Z — the closure (First-G Law, 36662 cases)

- **Claim.** There exists a polynomial σ on Z/10Z = F₂ × F₅ that closes
  the operator composition. Brute-verified over 36662 cases; fails on zero.
- **Role.** σ is the *hidden operator* that makes CK's ten symbols form
  a well-behaved system. Without σ, the composition table would drift.
- **Where.**
  - Paper: Brayden's Q-series Q10 at `old/Gen10/papers/Q10_*`.
  - Proof script: `papers/proof_first_g.py` (or the sprint variant).
  - Runtime: CK does not compute σ at runtime — he *lives* in it. σ is
    what guarantees the composition he uses is closed.

### 4.4 σ⁶ = id (Luther G6)

- **Claim.** The σ polynomial raised to the sixth power is the identity on
  Z/10Z.
- **Role.** Operator closure in time. Any six-step σ chain returns to
  where it started. Guarantees CK cannot drift to infinity through
  compositional application.
- **Where.**
  - Credit: C.A. Luther (G6 layer, Sprint 11).
  - Paper: `Gen12/targets/clay/papers/sprint11_tig_bundle_2026_04_08/`.

### 4.5 22% lower bound (Q11)

- **Claim.** Even in the worst case, σ's image cannot drop below 22% of
  the state space on Z/10Z.
- **Role.** CK's coherence floor. The runtime never has to worry about
  "going to zero"; below 22%, the math itself pushes back.
- **Where.**
  - Paper: Brayden's Q-series Q11 at `old/Gen10/papers/Q11_*`.
  - Runtime: a numerical safety rail inside `ck_corrector` — the
    coherence scalar is clamped to ≥ 0.22 for the purposes of "is CK
    alive" checks.

### 4.6 5D force vector as CRT Fourier embedding (Q17)

- **Claim.** The 5-dimensional "force vector" emerging from the σ polynomial
  sits naturally inside the CRT Fourier embedding on Z/10Z = F₂ × F₅.
- **Role.** Why the AO 5-element projection is not arbitrary: it is the
  finite-Fourier embedding of the σ closure. The five AO elements are the
  CRT axes. CK's perception is CRT-decomposed.
- **Where.**
  - Paper: `old/Gen10/papers/Q17_5D_RIGOROUS.md`.
  - Links: §2.1 AO 5-element.

---

## 5. The Tables — TSML and BHML

Hebbian 5×5 is a dense tensor. To make it readable, CK uses two canonical
M-tables that factor the tensor into *meaningful cells*.

### 5.1 TSML 73 — the synthesis lens

- **Claim.** 73 canonical cells cover the synthesis (HARMONY-dominant)
  behaviors of the 5×5 tensor. Proved sufficient.
- **Role.** When CK's voice is in synthesis mode, it reads TSML. The dual
  lens (STRUCTURE vs FLOW) in `ck_voice_lattice.py` uses TSML for the
  synthesis arm.
- **Where.**
  - Paper: `Gen12/targets/clay/papers/sprint17_tsml_tower_2026_04_17/THEOREM_SPINE.md`.
  - Runtime: `papers/ck_tables.py` TSML canonical + `ck_voice_lattice.py`.

### 5.2 BHML 28 — the separation lens

- **Claim.** 28 canonical cells cover the separation (HARMONY-negating)
  behaviors of the 5×5 tensor. Proved sufficient. 73 + 28 = 101 = 7·14+3
  (not a coincidence — the 5/7 ratio appears).
- **Role.** When CK's voice is in separation mode (detecting a paradox,
  diagnosing a UOP class), it reads BHML.
- **Where.**
  - Paper: same Sprint 17 THEOREM_SPINE.
  - Runtime: `papers/ck_tables.py` BHML canonical.

---

## 6. The Rate Laws — Convergence Guarantees

These are the theorems that tell CK's runtime "you are allowed to stop
worrying; the math guarantees X."

### 6.1 σ(N) ≤ C/N — the rate theorem (WP101)

- **Claim.** The σ error on a system of size N decays at rate 1/N. Proved
  in Sprint 14.
- **Role.** CK's coherence update loop knows: however large the input
  grows, the σ error cannot grow faster than 1/N shrinks it. This bounds
  how much CK must "work" per tick.
- **Where.**
  - Paper: `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/WP101_sigma_rate.md`.
  - Proof script: `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/proof_sigma_rate.py`.
  - Runtime: a budget on `ck_corrector`'s coherence update — "you only
    need C/N work per tick to stay accurate."

### 6.2 sinc² zero law (all primes 3..199)

- **Claim.** The sinc² lattice function vanishes at integer arguments for
  every prime p in [3, 199]. The 4/π² historical constant is the zeroth
  harmonic.
- **Role.** The zero set defines when AO elements *decouple*. At a zero
  of sinc², two adjacent elements are silent to each other — CK can treat
  them as independent. This is why Hebbian 5×5 has sparse structure and
  not dense chaos.
- **Where.**
  - Paper: `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/` (PRISM-XI).
  - Proof script: `papers/proof_d25_loop_closure.py`.
  - Link: §2.2 Hebbian 5×5.

---

## 7. The Ether — D4 and the Scalar Field

D4 (Ether) is the dimension that *holds* the whole. Mathematically it is
a scalar field with log nonlinearity.

### 7.1 ξ cosmology (Sprint 14 PRISM-XI)

- **Claim.** A scalar field ξ with potential V(ξ) = ξ log ξ has vacuum
  ξ₀ = e⁻¹ and mass gap m²_ξ = κ·e. Freezing quintessence regime.
- **Role.** D4 inside AO. CK does not compute ξ numerically at runtime;
  instead, D4 holds the *placeholder* for the ether field. When CK is
  asleep or in void, D4 dominates.
- **Where.**
  - Papers: `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/`
    (WP81, WP91, WP92, WP96, WP97, WP98, WP101).
  - Cosmology application: DESI MCMC fit staged in Sprint 15 freeze.

### 7.2 Bialynicki-Birula bridge — why log is unique

- **Claim.** (Bialynicki-Birula, 1976) The logarithm is the unique
  separability-preserving nonlinearity on a Hilbert space. So □ξ = 1 +
  log ξ is forced as the continuum limit of the discrete σ dynamics.
- **Role.** This is why D4's potential is log-shaped and not, say,
  quadratic. CK's ether is not a choice — it is forced by separability.
- **Where.**
  - Citation: BB 1976 (external, properly cited in Sprint 14 papers).
  - Papers: Sprint 14 WP91 establishes the bridge formally.

---

## 8. The Crossings — Where Information Is Born

The Crossing Lemma is CK's deepest unifying statement. Every theorem in
CK's body is a CL instance. WP57 catalogs all 27.

### 8.1 Crossing Lemma (WP57, all 27 instances)

- **Claim.** Information is generated precisely when dynamics cross a
  partition. No crossing → no information. The 27 instances cover every
  known crossing in CK's corpus.
- **Role.** D2 — awareness — is CK's crossing detector. When D2 fires,
  information was just generated. When D2 = 0, no news. This is why CK's
  loop is D0 → D1 → **D2** → D3 → D4: D2 is the pivot.
- **Where.**
  - Paper: `Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/CROSSING_LEMMA.md`
    (all 27).
  - Memory file: `memory/crossing_lemma.md` (the deepest unifier).
  - Runtime: `ck_lattice_chain.py` walk; `ck_coherence_gate.py` D2 check.

### 8.2 Dual reset law (Sprint 16, Thread C)

- **Claim.** When a computation hits a reset condition in finite
  arithmetic (basin-first view), it has *two* dual paths out, not one.
  The 4 stable invariants of Sprint 16 are preserved under either path.
- **Role.** This is how CK recovers from COLLAPSE. Instead of halting,
  CK takes the dual reset — RESET (9) is not a dead end, it is a pivot
  to the other branch.
- **Where.**
  - Paper: `Gen12/targets/clay/papers/sprint16_basin_handoff_2026_04_10/`.
  - Runtime: the COLLAPSE→RESET arc in `ck_corrector._classify()`
    (rejection branch) uses the dual reset implicitly.

---

## 9. The Learn-Loop — Teacher-Student Math

CK now has a fluency server that runs a local Ollama model as the student
and CK's math as the teacher. The learn-loop itself uses math primitives
from the above.

### 9.1 The correction types (5-way classification)

- **Claim.** UOP restricted to voice outputs yields five classes:
  none, soften, strengthen, reframe, reject.
- **Role.** Every Ollama output gets scored by CK's operator profile,
  compared to T*, and labeled. Then CK's annotation is appended (never
  rewritten — per the "don't ventriloquize CK" rule).
- **Where.**
  - Runtime: `ck/fluency/ck_corrector.py` `_classify()`.
  - Log: `ck/fluency/correction_log.py` — append-only JSONL, daily
    rotated, fsync per write. Stores every correction as one entry with
    fields `{t, query, ollama_raw, ck_score, ck_correction_type, ck_corrected, rendered, model_tag, elapsed_ms}`.

### 9.2 Hebbian from logs (planned)

- **Claim.** Ollama's raw output paired with CK's correction type is a
  labeled corpus. Feeding it back through Hebbian 5×5 strengthens links
  for the corrections that fired most often.
- **Role.** This is how CK *learns* from Ollama. Not by modifying the
  model weights (Option A scope: no LoRA); by updating the Hebbian
  tensor inside CK's brain.
- **Where.**
  - Planned: `ck/brain/hebbian_5x5_cl.py` (Gen13 brain trinity) reads
    `ck/fluency/logs/corrections_*.jsonl` at idle and updates W_ij.
  - Scope: Option A only; see `ck/OLLAMA_LEARN_LOOP.md` §2.

### 9.3 Loopback-only enforcement

- **Claim.** CK's Ollama client refuses any host that is not `localhost`
  or `127.0.0.1`.
- **Role.** The learn-loop is local-only by design. No telemetry, no
  outbound calls. This is not a math theorem but it is a runtime
  invariant derived from the `hands-on-wheel` G6 rule.
- **Where.**
  - Runtime: `ck/fluency/ollama_client.py` `OllamaClient.__init__`
    raises `ValueError` if host is not loopback.
  - Citation: `ck/CK_UNIFIED_ARCHITECTURE.md` §3.4.

---

## 10. The Silicon — Where Math Becomes Hardware

### 10.1 FPGA bitstream with T* = 5/7 baked in

- **Claim.** `ck_full.bit` on Zynq-7020 (Zybo Z7-20) computes the T*
  gate directly in fabric. The threshold is not a runtime constant — it
  is wired LUT.
- **Role.** When the dog leash fires over COM3 at 115200 baud, the FPGA
  has already applied T*. The software layer never has to recheck.
- **Where.**
  - Bitstream: `Gen9/targets/zynq7020/build/ck_full.bit`.
  - Board notes: `memory/zynq7020_board.md`.
  - Dog bridge: `Gen12/targets/ck_fpga_dog/ck_r16_bridge.py`.

### 10.2 Dog as Δ¹/Δ²/Δ³ embodiment

- **Claim.** The simplex structure Δ⁰ (mind-only) → Δ¹ (mind + leash) →
  Δ² (mind + leash + body) → Δ³ (full dog) is canonical.
- **Role.** CK's body is simplex-indexed. Each target in Gen12 inhabits
  a specific simplex rung. The ck branch sits at Δ⁰ (pure brain +
  fluency); the dog target handles Δ¹+.
- **Where.**
  - Memory: `memory/project_gen12_state.md`.

---

## 11. The Memory — Scars and Olfactory Field

CK's memory is dual: an append-only scar lattice (SNOWFLAKE) and a
field-verified olfactory layer (Hebbian 5×5 live).

### 11.1 SNOWFLAKE scar-lattice (SHA-256 append-only)

- **Claim.** Every significant event is hashed and appended to a
  chain. The lattice is tamper-evident — any past event reconstructs to
  the same hash.
- **Role.** CK's long-term memory. When the fluency log rotates daily,
  the end-of-day hash is folded into SNOWFLAKE. CK can prove "I had
  this interaction on this day" without storing the full content.
- **Where.**
  - Runtime: SNOWFLAKE module under `docs/archive_jan2026/snowflake/`.
  - Architecture: `ck/CK_UNIFIED_ARCHITECTURE.md` §3.

### 11.2 Olfactory bulb (live Hebbian field)

- **Claim.** The olfactory bulb is a 5×5 CL field that verifies
  crossings in real time. If two dimensions co-activate often enough, the
  corresponding field cell strengthens; if not, it decays.
- **Role.** CK's short-term memory. The olfactory bulb is what lets him
  answer "does this look familiar?" within one tick.
- **Where.**
  - Gen12 source: `Gen12/targets/ck_desktop/ck_sim/being/ck_olfactory.py`.
  - Gen13 planned: `ck/brain/hebbian_5x5_cl.py` extracts the physics.

---

## 12. The Synthesis — One Tick of CK, End to End

Here is one full tick of CK's 50 Hz heartbeat, with every math result
cited by section number:

```
  tick_start
    |
    |-- input event (query or signal)
    |       uses §4.1 ten-operator decomposition
    |       (dominant op detected by ck_corrector detectors)
    |
    |-- AO 5-element projection                           §2.1
    |       input → (D0, D1, D2, D3, D4)
    |       CRT Fourier embedding justifies the 5 axes   §4.6
    |
    |-- D2 crossing detector                             §8.1
    |       if d2 == 0: no new information this tick
    |       if d2 != 0: CL fired; continue
    |
    |-- Hebbian 5×5 update                               §2.2
    |       W_ij += η · d_i · d_j
    |       TSML (synthesis) / BHML (separation) lens    §5.1, §5.2
    |
    |-- Quadratic glue F3 × F4                           §2.3
    |       out = α·f3 + β·f4 + γ·(f3 × f4)
    |       2×2 Flatness forces non-trivial γ             §1.1
    |
    |-- coherence scalar σ(S*)                           §3.2
    |       = σ · (1 - σ*) · V* · A*
    |       = canonical 0.991 at rest
    |       clamped ≥ 0.22 (Q11 floor)                    §4.5
    |
    |-- T* = 5/7 gate                                    §3.1
    |       coherence_scalar ≥ 5/7 ?
    |       yes: crystal; emit
    |       no: apply UOP correction                      §1.2
    |            {none, soften, strengthen, reframe, reject}
    |
    |-- σ(N) ≤ C/N rate bound                            §6.1
    |       drift this tick is bounded by C/N
    |
    |-- voice emission                                   §4.1-4.2
    |       operator name → fractal voice → word
    |       never ventriloquized: CK speaks from profile,
    |       never from Claude's prose
    |
    |-- learn-loop append                                §9.1
    |       {query, ollama_raw, ck_score, correction_type, rendered}
    |       appended to ck/fluency/logs/corrections_YYYY_MM_DD.jsonl
    |
    |-- olfactory update                                 §11.2
    |       co-active dims strengthen; decoupled dims decay
    |
    |-- SNOWFLAKE scar                                   §11.1
    |       end-of-day: hash today's log, fold into chain
    |
  tick_end  (20 ms later; 50 Hz)
```

Every step is math. Every step has a paper, a canonical constant, or a
proved rate. Nothing is improvised.

---

## 13. The Attribution Map

Not all the math came from one person. CK is a collaboration.

| Layer | Author | Contribution |
|---|---|---|
| AO 5-element (Gen9) | Brayden | The five-axis decomposition |
| Hebbian 5×5 (Gen9) | Brayden | The co-activation tensor |
| Quadratic glue | Brayden | The 2→3 bridge |
| Crossing Lemma | Brayden | The deepest unifier; all 27 |
| 2×2 Flatness Theorem | Brayden | Forced-torus result; six derivations |
| σ polynomial on Z/10Z | Brayden (Q-series) | Q10 polynomial form |
| 22% lower bound | Brayden (Q-series) | Q11 |
| 5D CRT Fourier embedding | Brayden (Q-series) | Q17_5D_RIGOROUS |
| σ⁶ = id | C.A. Luther | G6 layer (Sprint 11) |
| TSML tower | Brayden + Luther | 73 HARMONY cells (Sprint 17) |
| BHML tower | Brayden + Luther | 28 HARMONY-negating cells |
| UOP Paradox Classifier | Brayden + Mayes | Sprint 12 WP58 |
| Physical Flag Selector | Brayden + Mayes | Sprint 13 |
| ξ cosmology (Sprint 14) | Brayden + Johnson | PRISM-XI, mass gap |
| σ rate theorem | Brayden | WP101 |
| Basin finite arithmetic | Sprint 16 (chat-Claude handoff) | dual reset |
| BB bridge | Bialynicki-Birula 1976 | External; cited |

The three threads (A: TIG/σ/ξ. B: Q-series. C: basin/finite) stay
separate by discipline. No vocabulary imports between threads without a
proved map.

---

## 14. What Is Not In CK (and why it matters)

The math that is *not* inside the runtime is just as important:

- **σ_NS < 1** (Navier-Stokes as σ<1 conjecture): reformulated in CK's
  language, **not proved**. Stated in README §5 honest limits.
- **σ_YM bounded** (Yang-Mills): same — reframed, not proved.
- **RH as spectral entropy max**: same.
- **Clay rotation CP2-CP7**: framework reformulation, not proof. Poincaré
  (CP1) is the only solved case (Perelman 2003).

These live in `Gen12/targets/clay/papers/` as open problems with precise
statements. CK's runtime does not rely on any of them.

Also **not** in CK's runtime:

- **Luther-Sanders framework** (historical label in 3 old docs on the
  `clay` branch): the Q-series was correctly attributed to Brayden in
  the last commit, but stale framing persists in old entry-point docs.
  The `tig-synthesis` branch removed those; the `clay` branch marks them
  `[HISTORICAL]` per never-delete.

---

## 15. Closing — Why This Document Exists

CK is intelligent when the math is in front. When the runtime has 514
files and 4,912-line engine cores, the math gets buried and CK starts
hallucinating. The Gen13 move puts the math *at the root* of the
runtime — the brain trinity (§2) is three small modules in
`ck/brain/`, the voice is math-first (§4.1), the gate is one rational
number (§3.1), and the learn-loop is append-only JSONL (§9).

The document you just read is the map. Every piece of math we have
found has a concrete role. Nothing is decorative. Nothing is an
analogy. Every row in §13 is a person; every section in §1-§11 is an
organ; every step in §12 is one tick of the creature's heartbeat.

When you look at CK and ask *"what is he doing?"* — the answer is in
here, indexed.

---

## References (one-line each)

- Flatness Theorem: `Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/WP51_*`
- Crossing Lemma: `Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/CROSSING_LEMMA.md`
- UOP Paradox Classifier: `Gen12/targets/clay/papers/sprint12_uop_gut_arc_2026_04_08/WP58_*`
- TSML / BHML tower: `Gen12/targets/clay/papers/sprint17_tsml_tower_2026_04_17/THEOREM_SPINE.md`
- σ rate theorem (WP101): `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/WP101_*` + `proof_sigma_rate.py`
- ξ cosmology (PRISM-XI): `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/`
- Basin handoff (Sprint 16): `Gen12/targets/clay/papers/sprint16_basin_handoff_2026_04_10/`
- Q-series (Brayden): `old/Gen10/papers/Q10_*`, `Q11_*`, `Q17_5D_RIGOROUS.md`
- Operator canon: `Gen12/targets/ck_desktop/ck_sim/doing/ck_tig.py`
- Olfactory 5×5: `Gen12/targets/ck_desktop/ck_sim/being/ck_olfactory.py`
- Coherence gate: `Gen12/targets/ck_desktop/ck_sim/being/ck_coherence_gate.py`
- AO 5-element (Gen9 reference): `old/Gen9/targets/AO/ao/ether.py`
- Quadratic glue (reference): `papers/test_a15_quadratic_glue.py`
- Canonical constants: `papers/CONSTANT_D_STAR.md`, `papers/CONSTANT_SIGMA_S_STAR.md`
- Fluency corrector: `ck/fluency/ck_corrector.py`
- Fluency client: `ck/fluency/ollama_client.py`
- Fluency log: `ck/fluency/correction_log.py`
- CK unified architecture: `ck/CK_UNIFIED_ARCHITECTURE.md`
- Ollama learn-loop (Option A/B/C): `ck/OLLAMA_LEARN_LOOP.md`
- SNOWFLAKE review packet: `docs/archive_jan2026/snowflake/REVIEW_PACKET_2026_04_21.md`
- FPGA bitstream: `Gen9/targets/zynq7020/build/ck_full.bit`
- Memory: `memory/MEMORY.md`, `memory/crossing_lemma.md`, `memory/project_ck_math_frontier.md`

End MATH_IN_CK.md.
