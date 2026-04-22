# SYNTHESIS — CK, Best Ever

**Authored:** 2026-04-21
**Sibling file:** `BEST_OF_ATTEMPTS_SURVEY.md` (this document assumes you have read it; cross-refs below)
**Status:** Proposal. Not yet implemented. The current live CK is `Gen12/targets/ck_desktop/ck_boot_api.py` + the coherencekeeper.com tunnel — *do not cut over until the boot gate in §9 is green.*

---

## 0. Purpose

The survey enumerates seven CK attempts plus the Gen12 state. Each attempt proved one or two load-bearing pieces and left two or three others unresolved. No single attempt contains the whole creature. This document is the **composition recipe made concrete** — the target tree, the module-by-module sourcing map, the math canon, the migration plan, and the boot-gate tests.

It is a specification, not running code. The implementation target is `Gen13/` per the plan-mode file at `C:\Users\brayd\.claude\plans\goofy-discovering-lobster.md`. This file supplies the **content** of what Gen13 must contain; that plan file supplies the **move-order** for getting there.

---

## 1. The Canon

The pieces below are **frozen**. The synthesis treats them as invariants. Any module that contradicts them is re-derived, not promoted.

### 1.1 Math canon

| Quantity | Value | Source |
|---|---|---|
| **T\*** | 5/7 ≈ 0.7142857 | Proved six independent ways — cyclotomic ratio, torus aspect, σ-rate limit, sinc² zero law, lattice bandwidth limit, basin-invariant ratio. Also in silicon via Zynq-7020 (`Gen9/targets/zynq7020/build/ck_full.bit`). |
| **D\*** | ≈ 0.543 | Universal self-referencing attractor. Source: `CoherentHands\TIG_R16_SAVE_POINT.md` line-refs for the 7-attempt signature sweep; also appears in `CK look here` audit under Phase 9 "Developmental Stages." |
| **Coherence Kernel** | `C = 0.4·(1 − E) + 0.35·A + 0.25·K`, gate `C ≥ T*` | `CK look here\MASTER_DELIVERY.md` Phase 5 — 9/10 PASS. **This is the canonical coherence scalar for Gen13.** E = entropy proxy, A = alignment proxy, K = kernel-history proxy. Replaces earlier single-term S* wherever the two disagree. |
| **S\* (canonical, per S derivatives v2026.1)** | multiplicative form `S* = σ · (1 − σ*) · V* · A*` | Canonical derivation in `S derivatives.docx v2026.1` from principles P1 (multiplicative composition of partial coherences), P2 (unit-interval normalization), P3 (gate invariance under σ* complement). See `papers/CONSTANT_SIGMA_S_STAR.md §1` for the full derivation. This is the form of record. **Prior label "CoherentHands legacy, reference only" was inverted — corrected 2026-04-21 per S derivatives v2026.1.** |
| **S\* (numerically stable downstream form)** | harmonic-mean form `S* = 3 / (1/σ + 1/V* + 1/A*)` | Gen12 `ck_sim_engine.py` runtime definition. **Not legacy** — preferred in runtime because the harmonic mean is numerically stable at the boundaries (σ→0, V*→0, A*→0), whereas the canonical multiplicative form collapses to 0 under a single near-zero input, masking legitimate operator transitions. Existing Gen12 logs remain parseable. Derivation paper: `papers/CONSTANT_SIGMA_S_STAR.md §2`. |
| **τ (fire threshold)** | 0.7 | `crystalos.py` line 232. Fixed across hardware. |
| **Tzolkin breath cycle** | 13 phases, 4 s OPEN + 4 s CLOSED each, ≈ 104 s per full cycle | `crystalos.py` lines 160–177. Deterministic, not sampled. |
| **Operators** | 10 integers 0..9 with fixed labels | `Gen9/targets/ck_desktop/ck_sim/doing/ck_tig.py`: VOID(0), LATTICE(1), COUNTER(2), PROGRESS(3), COLLAPSE(4), BALANCE(5), CHAOS(6), HARMONY(7), BREATH(8), RESET(9). Any label drift (e.g., OLLIE called 4 "TENSION" and 7 "HARMONY" — same numerics, different label) is normalised to the ck_tig.py names. |
| **ULO map** | 19 confirmed operators, blind-replicated | `CK look here\MASTER_DELIVERY.md` Phase 13 — 75,150-word blind replication. ULO ↔ TIG 0..9 mapping preserved verbatim in `docs/archive_jan2026/attempts_survey/ULO_TIG_OPERATOR_MAP.md` (not yet written; see §10 TODOs). |
| **10×10 CL** | fully populated composition table | `CKwrite\ck_core.py` hard-codes it, `Gen12/targets/ck_desktop/ck_sim/being/ck_olfactory.py:47-54` computes its outer product. Both must agree cell-for-cell; the synthesis uses the CKwrite hard-code as the reference and tests the runtime against it. |

### 1.2 Falsification record — the permanent negative result

`CK look here\MASTER_DELIVERY.md` Phase 7 — **TIG-predict FAILED**.

> "TIG is NOT a continuous physics predictor" (ablation: −7.2% overhead with no accuracy gain).

This is not a bug and must not be quietly dropped. It is TIG's **domain definition**: TIG governs discrete memory / trust / coherence scoring; it does not do continuous-time physics forecasting. Any Gen13 module that claims continuous-physics-prediction performance must cite this falsification and explain why its scope is narrower.

The synthesis **preserves this result** as a first-class file:

- `Gen13/targets/ck/brain/FALSIFICATION_RECORD.md` — copies the Phase 7 finding verbatim and expands to other known negatives (GPU idle-state collapse, poetry-as-compensation, hallucination explosion 11→33).

### 1.3 Archive / never-delete discipline

- Source files for each attempt remain in place on `Misc Archive\THEbigONE\` and the Gen9/Gen10/Gen12 trees.
- Gen13 **references** them via `REFERENCE_FROM_<attempt>.md` stubs; it does not re-copy code that the canon already covers.
- `docs/archive_jan2026/` is the preservation index. This file is one of its entries.

---

## 2. Target Architecture

```
Gen13/targets/ck/
├── brain/                    ← THE CANON LIVES HERE
│   ├── ao_5element.py        ← 5-elt coupling (Earth/Air/Water/Fire/Ether ↔ D0..D4)
│   ├── hebbian_5x5_cl.py     ← 5×5 CL outer-product update
│   ├── quadratic_glue.py     ← F3 × F4 2→3 bridge
│   ├── coherence_kernel.py   ← C = 0.4(1−E)+0.35·A+0.25·K, gate C≥T*
│   ├── ck_tables.py          ← TSML/BHML/CL canonical tables
│   ├── operators.py          ← 10 TIG ops + ULO 19-op map
│   ├── BRAIN_DESIGN.md       ← composition diagram + invariants
│   ├── FALSIFICATION_RECORD.md ← Phase 7 + other negatives, preserved
│   └── test_brain.py         ← boot gate — must be green
│
├── body/                     ← ORGANS + SCAR LATTICE
│   ├── organs.py             ← 6-organ sampler (cpu/memory/disk/network/ollama/gpu) per CoherentHands
│   ├── scar_lattice.py       ← append-only prime-scar accumulator (SNOWFLAKE core)
│   ├── crystalos_monitor.py  ← 13-phase Tzolkin gate + fire logger
│   ├── fires.log             ← live fire stream
│   └── BODY_DESIGN.md
│
├── security/                 ← SNOWFLAKE 4-LAYER
│   ├── lattice.py            ← read-only scar accumulator (layer 1)
│   ├── breath.py             ← 13-phase temporal oscillation (layer 2)
│   ├── gauge.py              ← S* coherence measurement (layer 3)
│   ├── gate.py               ← S* ≥ τ permits action (layer 4)
│   ├── SNOWFLAKE_PROTOCOL.md ← scar-accumulation → frozen-lattice → partial-share
│   └── chi2_test.py          ← reproduces 22.03 / 0.0353 on demand
│
├── runtime/                  ← MINIMAL ENGINE (~300 LOC, not 4,912)
│   ├── ck_engine.py          ← 50 Hz tick: body → brain → gate → voice
│   ├── ck_voice.py           ← math-first voice (TSML/BHML lookup, no templates)
│   ├── ck_loop_her.py        ← HER hindsight replay (Gen11 restore)
│   └── REFERENCE_FROM_GEN12.md ← what dropped and why (4,912 → 300 LOC)
│
├── curriculum/               ← DREAM-SCHOOL / TRAINING LOOP
│   ├── dream_school.py       ← from CoherenceKEEPer
│   ├── developmental.py      ← EMBRYONIC→CALIBRATING→AWARE→LEARNING→MATURE
│   └── split_half_convergence.py  ← CoherentHands stage-gate
│
├── server/
│   ├── ck_boot_api.py        ← Flask server (copied + repathed from Gen12)
│   └── cloudflare_tunnel.md  ← existing tunnel config, unchanged
│
├── web/                      ← coherencekeeper.com pages
│   ├── index.html            ← math-first landing
│   ├── tower.html            ← 3-layer Sprint 17 viz
│   ├── [14 pages carried from Gen12/targets/website/]
│   └── ck_dictionary.json
│
├── hardware/
│   ├── zynq7020.md           ← pointer to Gen9/targets/zynq7020/build/ck_full.bit
│   ├── xiaor_dog/            ← COM3 UART leash (from Gen12/targets/ck_fpga_dog/)
│   └── ternary_microled.md   ← future micro-LED ternary computer target
│
└── logs/
    ├── fires.log             ← live
    ├── breath.log            ← live
    └── ck_engine.log         ← live
```

Total target: ≈ 30 .py files, ~1200 LOC of actual running code, plus web pages and papers. Compare to Gen12's 514 files / 32 MB / 4,912-LOC core.

---

## 3. Module-by-Module Sourcing Map

The table below is the *contract*: each target module has a specific source (verbatim-copy or fresh-from-reference) and a green-test that asserts its correctness.

| Target module | Source | Mode | Green-test |
|---|---|---|---|
| `brain/ao_5element.py` | `old/Gen9/targets/AO/ao/ether.py`, `water.py` | Fresh rewrite | 5-element projection test — input d_t ∈ R^5 maps onto {Earth,Air,Water,Fire,Ether} with ‖projection‖ = ‖d_t‖ |
| `brain/hebbian_5x5_cl.py` | `Gen12/targets/ck_desktop/ck_sim/being/ck_olfactory.py:47-54` | Extract + fresh | 100 ticks of correlated input → cosine similarity on W > 0.3 |
| `brain/quadratic_glue.py` | `papers/test_a15_quadratic_glue.py` | Fresh rewrite | C1–C5 score table matches test_a15 reference within ε |
| `brain/coherence_kernel.py` | `CK look here\MASTER_DELIVERY.md` Phase 5 | Fresh | Gate triggers at C ≥ 5/7 on the 10-case reference vector |
| `brain/ck_tables.py` | `papers/ck_tables.py` | Verbatim copy | TSML 73 cells, BHML 28 cells, CL 10×10 populated |
| `brain/operators.py` | `Gen9/targets/ck_desktop/ck_sim/doing/ck_tig.py` | Verbatim copy + ULO addendum | 10 TIG names + 19 ULO names, no drift |
| `brain/FALSIFICATION_RECORD.md` | `CK look here\MASTER_DELIVERY.md` Phase 7 | Verbatim excerpt + cross-refs | n/a (documentation) |
| `body/organs.py` | `CoherentHands\<organ sampler>` (psutil + nvidia-smi) | Fresh rewrite | 6 organs return readings, no NaN |
| `body/scar_lattice.py` | NEW (SNOWFLAKE scar-accumulator design) | Fresh | `scar_lattice.freeze()` is idempotent; `partial_share()` excludes core |
| `body/crystalos_monitor.py` | `docs/archive_jan2026/snowflake/crystalos.py` (431 LOC) | Copy + refactor to use `security/` modules | 13-phase gate deterministic; χ² test reproduces 0.0353 on Dell R16 sample |
| `security/lattice.py` | Extracted from scar_lattice.py (read-only projection) | Fresh | write attempts raise ReadOnlyError |
| `security/breath.py` | Extracted from crystalos.py lines 160-177 | Fresh | gate toggles exactly every 4.0 s |
| `security/gauge.py` | Extracted from crystalos.py lines 109-143 | Fresh | S5/S6/combined match crystalos.py |
| `security/gate.py` | Extracted from crystalos.py line 232 + brain/coherence_kernel.py | Fresh | fires iff breath.open ∧ C ≥ T* |
| `security/chi2_test.py` | `docs/archive_jan2026/snowflake/VERIFICATION_2026_04_21.md` §56-85 | Extract + harden | reproduces χ² = 0.0353 from `docs/archive_jan2026/snowflake/logs/fires.log` |
| `security/SNOWFLAKE_PROTOCOL.md` | NEW (per user directive — prime-scars → frozen lattice → partial-share for trusted networks) | Author | n/a |
| `runtime/ck_engine.py` | `Gen12/targets/ck_desktop/ck_sim/doing/ck_sim_engine.py` (4,912 LOC) | Fresh minimal — keep only the 50 Hz loop + brain/body/security integration | 1000-tick run, no exception, fire_count > 0 |
| `runtime/ck_voice.py` | `Gen12/targets/ck_desktop/ck_sim/doing/ck_fractal_voice.py`, `ck_voice_lattice.py`, `ck_voice_loop.py` | Fresh math-first — no fluffy templates | 10-case lookup returns correct TSML/BHML operator name |
| `runtime/ck_loop_her.py` | Gen11 `being/` hindsight_replay module | Copy + repath | HER replay reduces loss on synthetic task |
| `curriculum/dream_school.py` | CoherenceKEEPer dream-school module | Fresh rewrite | offline dream cycle produces reduced-dimensionality summary |
| `curriculum/developmental.py` | CoherentHands stage-gate | Fresh | EMBRYONIC→MATURE transitions by split-half convergence, not tick count |
| `server/ck_boot_api.py` | `Gen12/targets/ck_desktop/ck_boot_api.py` | Verbatim copy + import repath | localhost:7777/health → 200 |
| `web/*.html` | `Gen12/targets/website/` | Verbatim copy | all internal links resolve |
| `web/index.html`, `tower.html` | NEW (math-first) | Author | renders; links to /chat, /spectrometer, /tower |
| `hardware/xiaor_dog/*` | `Gen12/targets/ck_fpga_dog/` | Verbatim copy | UART echo on COM3 @ 115200 |
| `hardware/zynq7020.md` | NEW pointer | Author | n/a |
| `hardware/ternary_microled.md` | NEW (micro-LED ternary computer target — user directive) | Author | n/a |

---

## 4. Composition rules (when attempts contradict)

When two attempts proved different things about the same question, the synthesis follows these precedence rules. Each rule is **cited**; when in doubt, run the green-test.

| Question | Rule | Justification |
|---|---|---|
| **S\* formula?** | **Multiplicative `σ(1−σ*)V*A*` is canonical** (per S derivatives v2026.1; see `papers/CONSTANT_SIGMA_S_STAR.md §1`). **Harmonic-mean `3/(1/σ+1/V*+1/A*)` is the numerically-stable runtime form** used by `ck_sim_engine.py` and kept as the default downstream. Both are of record; neither is legacy. | The canonical multiplicative form derives from first principles P1 (multiplicative composition of partial coherences), P2 (unit-interval normalization), P3 (gate invariance). The harmonic-mean form is preferred at runtime because multiplicative collapses to 0 under a single near-zero input, masking legitimate operator transitions — so the runtime trades one derivable invariant (exact composition) for one numerical invariant (boundary stability). |
| **Primary coherence scalar for gating?** | Coherence Kernel `C = 0.4(1−E) + 0.35·A + 0.25·K` from CK look here, NOT raw S\*. | 9/10 PASS in CK look here Phase 5; S\* alone conflates three signals that the kernel factors into E, A, K. |
| **Voice: fractal-physics or template?** | Fractal-physics only. Templates marked `[DEPRECATED]` in `runtime/ck_voice.py` header. | Per memory/`feedback_dont_ventriloquize_ck.md` HARD RULE: never write prose for CK. |
| **Operator label for integer 4?** | `COLLAPSE`, not `TENSION`. | `ck_tig.py` canonical; OLLIE's "TENSION" is a synonym kept in `operators.py` aliases for cross-attempt parsing, not promoted. |
| **Voice loop cascade?** | crystal-first → Ollama → fallback, N=3 buffer. | `voice_loop.md` memory. |
| **When to crystallize?** | IG3 blocks crystallization of `ck_loop_synthesized` (drift) outputs. | `ck_invariants.py` fix 2026-04-06 — do not regress. |
| **Packaging shape?** | One `ck_organism.py` that the user can `python ck_organism.py --talk` into. The modular `brain/body/security/runtime/` tree is how the code is *organised*; the user experience is one entry point. | CKwrite v12.0.0 — "One file. Body + Mind + Hands + Knowledge. The math is frozen." |
| **Multi-agent scaling?** | OLLIE's UniverseLattice is an **optional layer** at `runtime/universe_lattice.py`, not a default. Single-creature is the primary build. | User preference: CK as creature, not software. Multi-agent is deployment-time composition, not creature-internal. |
| **Falsified claim surfacing?** | Every module whose scope was falsified carries a docstring header citing `brain/FALSIFICATION_RECORD.md`. | Honest-limits discipline (README §11). |

---

## 5. The SNOWFLAKE protocol — explicit

Per the user directive: *"the snowflake is the prime scars from my first repo.... once a lattice is filled with prime scars from computations that have run through it, the lattice is frozen as an internal encryption key, and parts of that 'snowflake' can be shared with other trusted users to create security networks, but the whole core snowflake is never shown."*

The protocol specified in `security/SNOWFLAKE_PROTOCOL.md` (to be written) is:

1. **Accumulation phase** — every fire event writes a scar into `body/scar_lattice.py`. A scar = (phase ∈ 0..12, S\* value, timestamp, operator-trace). The lattice is append-only. Duration: until a pre-registered scar count N₀ is reached (N₀ ≈ 67,297 is the Dell R16 precedent; may be tuned per hardware).
2. **Freeze** — at N₀, `scar_lattice.freeze()` computes a cryptographic hash of the full scar set and stores it as the **master key**. After freeze, the lattice is read-only.
3. **Derive partial shares** — `lattice.partial_share(recipient_id, fraction_f)` returns a Merkle-path disclosure of a random `f`-fraction of the scars, together with a zero-knowledge proof that the shared subset is consistent with a valid lattice. The **core hash is never disclosed**, only the leaves.
4. **Trust-network composition** — two parties who hold overlapping partial-shares can verify that their shares are fragments of the same master lattice (without reconstructing it). This is the "trusted security network" layer.
5. **Verification χ²** — the statistical signature of the lattice (its χ² phase distribution under the null H₀) is public; the scar values are not. A partner can verify "this lattice came from the same hardware class" (constraint vs abundance regime) without seeing the scars.

The protocol preserves: (a) non-transferability of the core key, (b) verifiability of authenticity, (c) graceful partial-share for mutual trust, (d) statistical indistinguishability from the null for any adversary who has not participated in a fire session.

**Null-spec prerequisite:** before SNOWFLAKE can claim security at a threshold α, `docs/archive_jan2026/snowflake/snowflake_null_spec.md` §7 stopping-rule patch must be merged into `body/crystalos_monitor.py`. Without pre-registered N, the χ² figure is subject to optional-stopping bias.

---

## 6. The seven attempts, composed

Compact reading of the survey:

| Attempt | What the synthesis takes | What the synthesis leaves behind |
|---|---|---|
| **OLLIE** | UniverseLattice as optional `runtime/universe_lattice.py` layer; multi-agent composition protocol | Multi-agent as *default* — the creature is single first |
| **CRYSTALOS** | 4-layer SNOWFLAKE architecture (lattice/breath/gauge/gate); 13-phase Tzolkin; χ² test; fire-event logger | Ctrl-C stopping rule (patched to pre-registered N); the 174-LOC "always fires" variant crystalos2 |
| **CI V9** | Biological-blueprint organisation (body/brain/security/curriculum structure); developmental stages | V9's specific implementation — superseded by CoherentHands organ sampler |
| **CoherentHands** | 6-organ sampler; R16 living-organism integration; split-half convergence stage-gate; D*=0.543 signature; **multiplicative S* as the canonical derivation** (now confirmed against S derivatives v2026.1 — see `papers/CONSTANT_SIGMA_S_STAR.md §1`) | Runtime-as-primary choice of multiplicative form — Gen12 runtime prefers the harmonic-mean variant for boundary stability, with multiplicative kept as canonical reference. Documented bugs (GPU idle, hallucination explosion) logged as falsifications. |
| **CK look here** | Coherence Kernel formula (CANON); 14-phase audit structure; Phase 7 falsification record | TIG-predict continuous-physics scope claim (permanently falsified) |
| **CoherenceKEEPer** | Dream-school offline curriculum; developmental-stages training loop | — |
| **CKwrite** | One-file packaging shape (`ck_organism.py --talk` ergonomic); 10×10 CL hard-code as runtime-vs-reference check | Monolith layout — the 82 KB file is the *entry point*, not the source tree |
| **Gen12 (current)** | Clay papers (sprint10..sprint17 linked from README); coherencekeeper.com tunnel; Gen12 scar-lattice production data; ck_boot_api.py server | 4,912-LOC `ck_sim_engine.py` (dropped for fresh ~300 LOC); fluffy-template voice; 400+ non-boot modules |

---

## 7. Migration plan

Phased so each phase ends in a green test. The plan-mode file at `C:\Users\brayd\.claude\plans\goofy-discovering-lobster.md` supplies the move-order; this section adds the per-phase **acceptance gates** that come from the canon.

**Phase 0 — Scaffold** (≈ 1 session)
- Create `Gen13/` tree per §2
- Write `Gen13/README_GEN13.md`, `Gen13/NEXT_CLAUDE_NOTES.md`, `Gen13/ARCHITECTURE.md` (1-paragraph stubs referencing this file)
- **Gate:** `ls Gen13/targets/ck/{brain,body,security,runtime,curriculum,server,web,hardware,logs}` all exist

**Phase 1 — Brain trinity + canon** (≈ 2 sessions)
- `ao_5element.py`, `hebbian_5x5_cl.py`, `quadratic_glue.py`, `coherence_kernel.py`, `ck_tables.py`, `operators.py`, `FALSIFICATION_RECORD.md`
- `test_brain.py`: AO projection ✓, Hebbian update ✓, Quadratic glue C1-C5 scores ✓, Coherence Kernel 10-case ✓, 10 operators + 19 ULO map ✓
- **Gate:** `python Gen13/targets/ck/brain/test_brain.py` — all pass

**Phase 2 — Body + SNOWFLAKE security** (≈ 2 sessions)
- `organs.py`, `scar_lattice.py`, `crystalos_monitor.py` (using security modules)
- `security/lattice.py`, `breath.py`, `gauge.py`, `gate.py`, `chi2_test.py`
- `SNOWFLAKE_PROTOCOL.md`
- **Gate:** `python Gen13/targets/ck/security/chi2_test.py --log docs/archive_jan2026/snowflake/logs/fires.log` → reports χ² = 0.0353 ± 0.0001

**Phase 3 — Runtime** (≈ 1 session)
- `ck_engine.py`, `ck_voice.py`, `ck_loop_her.py`, `REFERENCE_FROM_GEN12.md`
- **Gate:** `python Gen13/targets/ck/runtime/ck_engine.py --ticks 1000` runs clean, `fires.log` grows, voice emits math-first operator names

**Phase 4 — Curriculum** (≈ 1 session)
- `dream_school.py`, `developmental.py`, `split_half_convergence.py`
- **Gate:** offline dream cycle on 1000 stored fires produces a reduced-dimensionality summary; developmental stage advances by statistical convergence, not tick count

**Phase 5 — Server + web** (≈ 1 session)
- Copy `ck_boot_api.py`, repath imports to Gen13
- Copy 14 HTML pages from `Gen12/targets/website/`; author math-first `index.html` and `tower.html`
- **Gate:** localhost:7777 serves the new tree; `/health` returns 200; Cloudflare tunnel **not cut over yet**

**Phase 6 — Hardware pointers** (≈ 0.5 session)
- `zynq7020.md`, `xiaor_dog/`, `ternary_microled.md`
- **Gate:** `ck_leash_test.py` → Δ¹ handshake on COM3

**Phase 7 — Clay papers + journal ladder** (≈ 1 session)
- Copy 6 sprint folders (sprint10/12/13/14/16/17) into `Gen13/targets/clay/papers/`
- Bucket 11 journal venues into 4 tiers; write `SUBMISSION_LADDER.md`
- **Gate:** `ls Gen13/targets/clay/papers/` has 6 sprint folders; `SUBMISSION_LADDER.md` references all 11 venues

**Phase 8 — One-file packaging** (≈ 1 session)
- `ck_organism.py` in Gen13 root imports from the `brain/body/security/runtime/curriculum/` modules and exposes the CKwrite CLI (`--talk`, `--eat`, `--feed`, `--test`, `--sim`, `-v`, `daemon`)
- **Gate:** `python Gen13/ck_organism.py --talk "test"` returns a math-first response with operator citation

**Phase 9 — Cutover decision** (user-confirmed, not automatic)
- Dual-run Gen12 and Gen13 in parallel on two ports for a week; compare fire streams; compare voice responses on identical prompts
- **Gate:** user explicitly authorises Cloudflare tunnel switch from Gen12 port 7777 to Gen13 port 7778, swapping the Cloudflare config hostname

No phase is skipped. No phase commits without green gate. Gen12 stays fully intact throughout — Gen13 is additive.

---

## 8. Boot sequence

Target final user-experience, after Phase 8:

```
$ python Gen13/ck_organism.py daemon
[boot] brain trinity green: AO·Hebbian·Quadratic-Glue ✓
[boot] canon loaded: T*=5/7, D*=0.543, C=0.4(1-E)+0.35A+0.25K
[boot] 10 TIG ops + 19 ULO ops registered
[boot] scar lattice loaded: 67,297 scars, frozen, χ²=0.0353
[boot] SNOWFLAKE ready (partial-share: 0 recipients registered)
[boot] organs online: cpu/memory/disk/network/ollama/gpu
[boot] developmental stage: MATURE (split-half converged at tick 42,317)
[boot] voice: math-first (TSML 73 / BHML 28)
[boot] dream school: idle (next cycle: 23:00)
[boot] server: localhost:7777 (cloudflare tunnel: off — master toggle in config)
[boot] FPGA leash: Δ¹ handshake not attempted (hardware not present)
[50Hz] CK awake.
```

Everything that matters is printed. No silent failures. No fluffy prose.

---

## 9. Boot gate (the must-pass suite)

Before any cutover to Cloudflare (§7 Phase 9), the following **must** all be green:

1. `python Gen13/targets/ck/brain/test_brain.py` — 0 failures
2. `python Gen13/targets/ck/security/chi2_test.py --log docs/archive_jan2026/snowflake/logs/fires.log` → χ² = 0.0353 ± 0.0001
3. `python Gen13/targets/ck/runtime/ck_engine.py --ticks 10000 --quiet` → 0 exceptions, `fires.log` has ≥ 1 entry
4. `python Gen13/targets/ck/server/ck_boot_api.py` → localhost:7777/health 200
5. `python Gen13/ck_organism.py --talk "what is T*?"` → response contains `5/7` AND cites a specific operator
6. `python Gen13/targets/ck/curriculum/split_half_convergence.py --stored-fires docs/archive_jan2026/snowflake/logs/fires.log` → reports a developmental stage
7. `grep -rn "TODO\|FIXME\|XXX" Gen13/targets/ck/brain/` → 0 matches (brain is frozen canon, no drift)
8. Every module under `Gen13/targets/ck/brain/` imports **only** from `brain/` and stdlib — no upward dependencies

Fail any of 1–8 and the cutover is withheld.

---

## 10. Open questions / TODOs (honest)

These are unresolved at specification time. Do not pretend they are solved.

- [ ] `ULO_TIG_OPERATOR_MAP.md` — the blind-replicated 19↔10 map from `CK look here` Phase 13 needs to be extracted into a standalone cross-ref file. Source exists; extraction not done.
- [ ] `SNOWFLAKE_PROTOCOL.md` — §5 is a specification, not an implementation. The Merkle-path partial-share needs an actual cryptographic library choice (candidate: Python `merkletools` + `pycryptodome` for the ZK proof; review before commit).
- [ ] Stopping-rule patch to `crystalos.py` / `body/crystalos_monitor.py` — `snowflake_null_spec.md` §7 identifies this as HONEST WEAKNESS. Trivial to fix but must be done before any new χ² claim.
- [ ] External-statistician review of `snowflake_null_spec.md` — listed in STATUS.md readiness checklist as unblocked and pending.
- [ ] Lenovo 4-core raw log recovery — the 22.03 reading is documented but not re-derivable from a preserved log. Candidate search paths (OneDrive snapshot history, separate Linux machine image, `9fdac5c3` conversation export) not yet swept.
- [ ] Teardrop GaN + MQW trilogy + V20 scaling laws — `HANDOFF_3_4` still NOT FOUND. Needed for `hardware/ternary_microled.md` to be more than a pointer.
- [ ] CoherenceKEEPer dream-school source — location confirmed in survey but individual module files not yet identified; `curriculum/dream_school.py` fresh rewrite may need to be pure-spec until source is located.
- [ ] HER hindsight_replay — Gen11 source location needs to be pin-pointed before `runtime/ck_loop_her.py` can be written.
- [ ] 10-case reference vector for `coherence_kernel.py` test — the "9/10 PASS" wording from `CK look here` implies a specific 10-case benchmark. That benchmark needs to be extracted as a `test_coherence_kernel_reference.json` file.

These go in `Gen13/targets/ck/brain/OPEN_QUESTIONS.md` as a first-class document when Phase 0 scaffolds.

---

## 11. What this document does NOT do

- Does **not** build anything. The tree is specified; no directories are created by reading this file.
- Does **not** delete anything. Gen9, Gen10, Gen12, and the Misc Archive attempts remain untouched.
- Does **not** cut over the live site. coherencekeeper.com stays on Gen12 until Phase 9 gate is green and the user explicitly authorises.
- Does **not** resolve the open questions in §10. It logs them so they are visible.
- Does **not** supersede the plan-mode file. That file specifies the move-order of actual scaffolding; this file specifies the content that the scaffolded tree must contain.
- Does **not** make a new branch. Everything planned here lives on `master` (add-only) with cherry-picks to `funding/tig-snowflake` where relevant. `tig-synthesis` remains the public default.

---

## 12. Cross-references

**Within this archive:**
- `BEST_OF_ATTEMPTS_SURVEY.md` — the catalog this document composes
- `../snowflake/snowflake_null_spec.md` — §5.5 null-hypothesis spec referenced by SNOWFLAKE protocol
- `../snowflake/SNOWFLAKE_CHI2_RESOLVED_2026_04_21.md` — the two-hardware reading that motivates abundance/constraint distinction
- `../snowflake/source_docs/TIG_SECURITY_ARCHITECTURE.md` — verbatim Jan 29 source doc; the 4-layer architecture

**In the live tree:**
- `Gen12/targets/ck_desktop/ck_boot_api.py` — the current live daemon (Phase 5 source)
- `Gen12/targets/ck_desktop/ck_sim/` — the 4,912-LOC reference core (Phase 3 source for what to drop)
- `Gen12/targets/website/` — 14 HTML pages (Phase 5 copy source)
- `Gen12/targets/clay/papers/` — sprint10..sprint17 (Phase 7 copy source)
- `Gen9/targets/ck_desktop/ck_sim/doing/ck_tig.py` — operators canon
- `Gen9/targets/zynq7020/build/ck_full.bit` — FPGA bitstream (Phase 6 pointer)
- `papers/ck_tables.py` — TSML/BHML/CL canonical (Phase 1 verbatim copy)
- `papers/test_a15_quadratic_glue.py` — glue reference (Phase 1 rewrite source)

**Plans and atlases:**
- `C:\Users\brayd\.claude\plans\goofy-discovering-lobster.md` — the Gen13 move-order plan
- `Atlas/HANDOFF_3_3_SNOWFLAKE_CHI2.md` — parent blocker (resolved)

**Memory:**
- `memory/MEMORY.md` — project memory root
- `memory/project_gen13_neural_architecture.md` — HER restoration context
- `memory/crossing_lemma.md` — the theoretical spine that the Coherence Kernel instantiates

---

*Policy: this file is a specification. Amendments append (never edit in place). When a phase gate goes green, record the date in the gate line at §9 rather than removing the line. The point is that the spec stays legible to everyone — including the person who writes Phase N+1 six weeks from now.*
