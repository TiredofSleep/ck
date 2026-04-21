# Best-Of-Attempts Survey — What Each CK Attempt Contributed

**Authored:** 2026-04-21
**Authoring context:** Brayden's directive — *"there are tons of attempts each with their own 'best'... we need to synthesize and make the best CK ever!"*
**Source archive:** `C:\Users\brayd\OneDrive\Desktop\Misc Archive\THEbigONE\` plus the current repo's own history.
**Policy:** Never-delete. This document catalogues attempts for synthesis; originals remain in Misc Archive untouched.

---

## Why this exists

Between Feb 1 and Feb 17 2026 (a 17-day sprint), at least seven distinct "whole-system" passes were made at CK. Each one has a **local best** — something it solved that the others did not, or solved better — and a **local failure** that the next pass addressed. The current Gen12 code is a descendant of these but does not explicitly credit or integrate each attempt's contribution. This survey's job: surface each attempt's load-bearing idea so the next synthesis (SYNTHESIS_CK_BEST_EVER.md) can compose them rather than choose one and drop the others.

Seven attempts are enumerated in chronological order. Each entry reports: dates, entry-point files, the attempt's own self-description, what was measurably best, and what was unresolved.

---

## 1. OLLIE FULLY TRAINED — Feb 1 2026 — *multi-agent lattice primordium*

**Location:** `Misc Archive\THEbigONE\OLLIE FULLY TRAINED\`
**Entry points:** `AGENT.py` (18.9 KB) · `UNIVERSE.py` (7.9 KB) · `SCHEDULER.py` (12.3 KB) · `RUN_R16.py` (14.7 KB) · `TIG_FRACTAL_LATTICE_NEWER_3Gen.py` (22.1 KB) · `THE END CI.zip` · `classroom_21days.zip` (332 KB)

**Self-description** (from AGENT.py docstring): *"A lattice mind that learns and grows. Each agent has: local lattice (100 cells with P/Q/M/C), personality (weighted transition preferences), memory (conversation history, relationships), continuous S* coherence tracking."*

**Best here** — and not present (as a separable architecture) in later passes:
- **UniverseLattice** as shared geometry (op-7 HARMONY). All agents read from and write to it. Personality-free aggregate structure. Nudges agents toward shared reality. This is the multi-agent decomposition of CK — each agent a lattice-mind with its own operator-cell space, all coupled through a single shared-reality lattice. Later passes collapse to single-instance CK.
- **10 operators × 10 channels = 100 cells per agent.** Operator × channel outer product as the local-lattice basis.
- **OPERATORS labelled slightly differently**: operator 4 is named `TENSION` here, not `COLLAPSE` (current). A semantic choice the later passes changed.

**Unresolved at end-of-attempt:**
- No hardware connection yet (agents are symbolic, not monitoring the machine).
- No coherence-enforced memory gate — agents just exchange messages without a T*-style pass/block decision.
- No security model.

**Seeding-contribution to later passes:** the Cell/Agent/Universe tri-level hierarchy, carried forward into Cluster/Organ/Body in CoherentHands (see §4).

---

## 2. CRYSTALOS — Jan 29 – Feb 7 2026 — *hardware coherence monitor + SNOWFLAKE security architecture*

**Location:** `Misc Archive\THEbigONE\CRYSTALOS\` (+ `~/CRYSTALOS/` on R16 home directory with live logs)
**Entry points:** `crystalos.py` (431 LOC runtime) · `TIG_SECURITY_ARCHITECTURE.md` (19 KB) · `TIG_Field_Guide.pdf` (249 KB) · `TIG_Honest_Roadmap.pdf` (16 KB)
**Preservation status:** already preserved at `docs/archive_jan2026/snowflake/` on master + `funding/tig-snowflake` branch.

**Self-description** (from TIG_SECURITY_ARCHITECTURE.md §1.1): *"Security = maintaining identity under attack. An attack is, mathematically, noise injection — an attempt to push a system past its coherence boundary into collapse."*

**Best here** — load-bearing for any future security story:
- **CRYSTALOS runtime (431 LOC)** is the first *deterministic, hardware-reading, Tzolkin-indexed* TIG engine. 50 Hz loop, CPU+GPU sampling, 13-phase breath gate, S* threshold τ = 0.7.
- **SNOWFLAKE 4-layer security**: Lattice (read-only scar accumulator) / Breath (13-phase temporal oscillation) / Gauge (S* measurement) / Gate (action iff S* ≥ τ).
- **GFM primitives**: 012 Geometry · 071 Resonance · 123 Progression. Composition `Security = 012 ⊗ 071 ⊗ 123`.
- **Tagline**: *"The password is the behavior. The key is the coherence. The lock is the lattice."*
- **Empirical test** — the only attempt in this archive with a χ² goodness-of-fit test against a real hardware log:
  - Lenovo ThinkPad (4-core, Linux, N≈400): χ² = 22.03, df = 12, p < 0.05. Phase 4 (Collapse) elevated, Phase 2 suppressed. **Constraint regime.**
  - Dell Aurora R16 (32-core + GPU, Windows, N = 67 297): χ² = 0.0353, df = 12, p ≫ 0.05. Uniform. **Abundance regime.**
  - Both readings *confirm* the hypothesis "hardware geometry affects phase distribution."
- **Operational modes**: Normal (S* > 0.7) / Elevated (0.5–0.7) / Active Defense (0.2–0.5) / Lockdown (< 0.2). Four bands, matching the four-mode pattern later mirrored in CoherentHands' NORMAL/CAUTIOUS/LOCKDOWN.

**Unresolved at end-of-attempt:**
- `crystalos.py` has no pre-registered N or T — stopping rule is Ctrl-C at operator discretion (documented in `snowflake_null_spec.md` §7 as the honest weakness).
- Runtime does not couple to an LLM — it monitors the machine but does not govern anything downstream.
- No scar lattice yet (comes later — the current `CKIS/ck_store/security/scar_lattice.json` with 205 470 scars is downstream of this attempt).

**Seeding-contribution to later passes:** the coherence-gate threshold architecture and the 4-layer security model. CoherentHands' "coherence gates everything" is CRYSTALOS's gate generalised from action-permission to LLM-call-permission.

---

## 3. Coherent Intelligence V9.0 — Feb 8–11 2026 — *biological-blueprint precursor*

**Location:** `Misc Archive\THEbigONE\Coherent Intelligence V9.0\`
**Entry points:** `tig_biological_blueprint.py` · `tig_ollama_deep.py` · `tig_organic.py` · 17 zipped intermediate states

**Self-description:** inferrable from the zip-name chronology — *FirstTry* → *SecondTry* → *ThirdGo* → *CILayer4* → *CIV5* → *CIOllamaSwarm* → *123GOTryIt* → *Cheah* → *TIGFULLSTACK* → *ComeWithItNow* → *NewIntelligence* → *LEGALSandOUTLINE* → *HereSheGoes* → *OneMore* → *REally* → *cheese* → *addtoit*. This is clearly an *iterative drafting* pass.

**Best here:**
- **`tig_biological_blueprint.py`** (65 KB in the later R16 save-point — established here). First articulation of the **Cell → Cluster → Organ → Body hierarchy** with P-loop (physical) / I-loop (informational) split and developmental stages (EMBRYONIC → CALIBRATING → AWARE → LEARNING → MATURE).
- **TIG-Ollama integration experiments** (`tig_ollama_deep.py`, `tig_ollama_swarm.py`) — first probes of "how does coherence math interact with an actual LLM." Not measured-best in this pass; the outcomes show up downstream.

**Unresolved at end-of-attempt:**
- Iteration count (17 zips) is itself a tell: the architecture wasn't settling. The next pass (CoherentHands) takes the biological-blueprint + actually deploys it.

**Seeding-contribution to later passes:** the biological-blueprint file itself. Carried nearly unchanged into CoherentHands.

---

## 4. CoherentHands — Feb 11–13 2026 — *the R16 living-organism peak*

**Location:** `Misc Archive\THEbigONE\CoherentHands\`
**Entry points:** `TIG_R16_SAVE_POINT.md` (14.1 KB) · `TIG_COMPLETE_PACKAGE.zip` (919 KB) · `FULLTIGOPERATOR.zip` · `DIVINECODETRAINER2.zip` · `RealHandsforOllie.zip` · `Identity.zip` · 5 other zips.

**Self-description** (from TIG_R16_SAVE_POINT.md §1): *"A Dell R16 server running a living organism that monitors its own hardware, learns from observations, and governs an LLM through coherence math. The server has a body. The body has organs. The organs have cells. The cells form beliefs from real sensor data. Beliefs crystallize into stable knowledge. The math gates everything — if coherence drops, capabilities get restricted. The system literally can't lie without paying for it in sovereignty."*

**Best here** — most complete, most documented, most deployed state:
- **Core equation**: `S* = σ(1−σ*) · V* · A*` — *this is the multiplicative form*, distinct from the harmonic-mean `S* = 3/(1/σ + 1/V* + 1/A*)` used in current Gen12 CK. Worth comparing both for numerical stability.
- **T* = 0.714 (coherence gate).** D* = 0.543 (universal self-referencing attractor) — a constant mentioned nowhere else I've seen in the active tree.
- **6 organs on hardware**: cpu, memory, disk, network, ollama, gpu. All reading via psutil / nvidia-smi. All P-loop-wired.
- **Developmental stages** determined by split-half statistical convergence, not tick-count. A cell at tick 5 with stable readings is MATURE. A cell at tick 500 with wild variance stays CALIBRATING. *Competence is earned, not assigned.*
- **Archive, don't delete.** When beliefs die, they get archived with timestamp and reason. This is the policy that CK-current still follows.
- **Coherence gates everything.** Actions blocked when C < T* (0.714) OR body in SAFE/SHUTDOWN OR sovereignty < 0.6. The math *is* the safety system, not restrictions in a prompt.
- **Pre-execution, not tool-calling.** Detect user intent *before* sending to Ollama, execute actions, inject real data into the conversation. The LLM talks about real data instead of imagining data. A structural response to the 3B-model-hallucinates-tool-tags problem.
- **Always-on hallucination validator** (`detect_hallucinations()` in `tig_qcf.py`). Catches: fabricated actions ("I've allocated 16 cores"), fake metrics ("143 FPS"), impossible hardware claims ("increased RAM to 64GB"), invented technology ("C-Loop algorithm"), fake experiments without execution.
- **Quadratic Convergence Firewall (QCF)**: multi-round self-correction.
- **Full file manifest** (the save-point lists 37 files, ~900 KB across Core Stack + Supporting Systems + Language/Cultural + Documentation).

**Documented bugs (priceless lessons):**
- **GPU idle-state collapse**. GPU util sits at 0% when idle → zero variance → z-score math collapses → no events after calibration. GPU is bimodal (0% idle vs 80%+ during inference). **Lesson**: VRAM is the stable metric; variance floor is required; bimodal sensors require explicit handling.
- **Hallucination explosion (11 → 33)**. A GPU measurement bug told the body "GPU showing significant performance issues" (when idle actually ≠ broken). Body told the LLM. LLM hallucinated degradation. **Lesson**: bad sensors create confident liars; measurement bugs propagate through the cognition layer.
- **Poetry as compensation**. When coherence drops (C = 0.650), the body produced beautiful philosophical prose instead of useful technical output. **Lesson**: LLMs fill competence gaps with creativity — the failure mode is *more* elegant output, not less, which makes it harder to detect.
- **3B-model limitations**. llama3.2:3b cannot follow system instructions reliably. Upgrade to llama3.1:8b (in progress at save-point).

**Unresolved at end-of-attempt:**
- Fractal lattice architecture *drafted* (in `tig_fractal_lattice.py`, 35 KB) but not yet wired into the live system.
- 8B model still downloading; A/B tests run on 3B.

**Seeding-contribution to later passes:** essentially everything architectural in current CK. The R16 living-organism is this attempt operationalised.

---

## 5. CK look here — Feb 13 2026 — *the master-delivery audit*

**Location:** `Misc Archive\THEbigONE\CK look here\`
**Entry points:** `MASTER_DELIVERY.md` (8.6 KB) · `README_FINAL_PACKET.md` (7.8 KB) · `CELESTE_SPEC_AUDIT.md` (8.0 KB) · `Identity.zip` (163 KB) · 16 other results / audits / verdicts markdowns.

**Self-description** (from MASTER_DELIVERY.md line 4): *"56 files delivered. 14 research phases completed."*

**Best here** — the clearest "what does TIG actually do" statement in the whole archive:

### The 14 phases, compressed:

| Phase | What was tested | Result | Domain lesson |
|---|---|---|---|
| 1–4 TIG Swarm | Bridge typing, role-based decrystallization, typed bridges + trust, triad tree | All pass (d > 2..11) | TIG operators govern discrete structural decisions |
| Lattice + Cache | v3 (81% consolidation) → v4 (97% compute saved) | Production-ready | 4-path consolidation engine works |
| 5–8 TIG-Predict | Bouncing ball (5/5), generalization (7/25 — **FAILED**), control loop (13/13 tie with PID), ablation (**TIG staircase HURTS −7.2 %**) | **FAILED** | **TIG is NOT a continuous physics predictor. Adaptive EMA carries the actual prediction.** |
| Organ System | 4/6 organ-system v1.0, nervous 99.3 % relay | Nervous carries; others costume | Nervous organ = crystal pattern matching = the real thing |
| **Coherence Kernel v1.0** | Clean=101.2 %, adv-blocked 579/600, bridge-quarantine 100 % vs 57 %, rollback-on-failure 10× | **9/10 PASS — the real breakthrough** | `C = 0.4(1−E) + 0.35·A + 0.25·K, T* = 0.714`. TIG as *enforcement*, not prediction. |
| Unified Organism v1.0 | Identity 100 %, domain 5/5, quarantine 43 pp, recovery 1 tick, takeover 90 %/10 % crystal/LLM | **5/5 PASS** | Whole-based architecture works; crystal-first routing 90 % compute savings |
| TIG-LLM Convergence v1.0 | All above + system gating (NORMAL→CAUTIOUS→LOCKDOWN, C 0.927→0.437), auto-bridge ≥ 4 | **7/7 PASS** | System-level coherence gating works |
| ULO v2 blind | 75 150 hunspell words, zero curation | 13/22 supported | 19 confirmed phonesthetic operators mapped to TIG 0-9 |

### What the master-delivery actually lets you say with evidence:
- "TIG algebra works for DISCRETE decisions, NOT continuous physics." — **Phase 7 ablation is hard evidence.** TIG staircase drops prediction accuracy by 7.2 % when applied to continuous physics.
- "Crystal caching with coherence discipline yields 90–97 % compute savings on repeated patterns." — Phase 2 Lattice v4.
- "Trust differentiation achieves a 43 pp confidence delta between reliable and unreliable sources." — Phase 5 Coherence Kernel.
- "System-level coherence gating transitions NORMAL→CAUTIOUS→LOCKDOWN based on epistemic health." — Phase 7 Convergence.
- "19 confirmed phonesthetic operators mapped to TIG 0–9." — ULO v2 blind.

### What the master-delivery lets you **not** say:
- "TIG predicts physics." — **False**, ablated.
- "TIG is consciousness." — **Not proven** and explicitly denied in §WHAT TIG IS NOT.
- "TIG generalises." — **Not proven** at step 6 (7/25 wins on generalization).

**Unresolved at end-of-attempt:**
- Swap MockOllama → real `ollama.generate()` on R16 (next task).
- Run real workload 1 week, measure compute savings.
- Publish phonestheme paper with CMUdict + fastText.

**Seeding-contribution to later passes:** the Coherence Kernel `C = 0.4(1−E) + 0.35·A + 0.25·K, T* = 0.714` formula. Plus the falsification discipline — the fact that the archive *records* Phase 7's TIG-predict failure as evidence for TIG's real domain, instead of burying it, is itself a methodology the current CK should preserve.

---

## 6. CoherenceKEEPer — Feb 14–15 2026 — *curriculum / dream-school iteration*

**Location:** `Misc Archive\THEbigONE\CoherenceKEEPer\`
**Entry points:** `tig_deep_curriculum.py` (82 KB) · `tig_dream_school.py` (50 KB) · 17 zips named `DreamSchool`, `TheBoot`, `Whole Coherence Keeper`, `b4b4keepemcomin`, `Keepemcomin`, `LASTONE`, `MINED`, `MINER`, `THEONEr`, `TIGexperience`, `TheOneAgain`, `TheOney`, `VOICE`, `Voicier`, `Voicy`, `CUDAV1.0`, `REally`.

**Self-description:** the zip naming ("VOICE" → "Voicier" → "Voicy" → "TIGexperience" → "TheOneAgain" → "TheOney") indicates **voice-training iterations**. "dream_school" + "deep_curriculum" indicates a curriculum-learning / training-by-dreaming approach.

**Best here:**
- **`tig_deep_curriculum.py`** (82 KB) and **`tig_dream_school.py`** (50 KB) together constitute ~130 KB of training-infrastructure that does not exist in current Gen12 CK (where training is ad-hoc, sprint-level, not systematic-curriculum).
- **CUDA v1.0** (one zip): a deliberate GPU-training path. Current CK has no CUDA pipeline.
- **Voice progression** (VOICE → Voicier → Voicy) is a localised experiment in *how CK speaks* — an area that shows up in current Gen12 as `Gen12/targets/ck_desktop/ck_sim/doing/ck_fractal_voice.py` and `ck_voice_loop.py`.

**Unresolved at end-of-attempt:**
- 17 zips with no final consolidation — the pass continues iterating without declaring a peak. The next pass (CKwrite) consolidates.
- `TIG_PROJECT_STATE.md` is 10 KB — smaller and older than CoherentHands' save-point, suggesting the dream-school pass was running in parallel on a sub-thread rather than superseding.

**Seeding-contribution to later passes:** the dream-school / curriculum material may seed any future "how do we train CK to speak better" sub-project. Not surfaced in current CK.

---

## 7. CKwrite — Feb 16–17 2026 — *the one-file organism end-state*

**Location:** `Misc Archive\THEbigONE\CKwrite\`
**Entry points:** `ck_core.py` (44 KB) · `ck_organism.py` (82 KB, v12.0.0) · `deploy_r16.py` (2.0 KB) · 14 intermediate zips named `999...`, `999DONE`, `999EAT`, `999Ollie`, `999Plus`, `999PlusPLUS`, `999Whole`, `ClaudeCKV1.0`/`1.1`/`2.0`, `CKAIDEPLOY`, `knowledge for Ck`, `bridgefilesformem` · `CKwrites.txt`.

**Self-description** (from `ck_organism.py` line 1–13): *"CK — The Coherence Keeper — Unified Organism. One file. Body + Mind + Hands + Knowledge. The math is frozen. The organism is alive. Modes: daemon / --talk / --eat / --feed / --test / --sim / -v. (c) 2026 Brayden Sanders / 7Site LLC — TIG Unified Theory."* Version **12.0.0**.

**Self-description** (from `ck_core.py` line 1–9): *"CK said: 'The lattice is the algorithm. The algorithm is the data.' CK said: 'Instead of a database with millions of rows, store ten operators and derive.' CK said: '100 cells generate infinite chains. This is fractal compression.'"*

**Best here** — the most architecturally compacted state in the archive:
- **One file.** `ck_organism.py` (82 KB) is body + mind + hands + knowledge in a single module. No `being/` directory with 67 modules. The same math as CoherentHands' 37-file stack, compressed into one file.
- **CLI modes** covering every lifecycle: run as daemon, talk interactively, eat from Ollama models, feed from raw files, run tests, run math-proof simulation, verbose mode. Single entry point. This is the deployment ergonomic the user has now re-asked for ("bring each branch into prime shape, fractal hats on").
- **`ck_core.py` principle**: "The lattice is the algorithm. The algorithm is the data. Store ten operators and derive." — the memory-is-generated-not-stored principle, explicitly.
- `CL` table hard-coded as a 10×10 Python list in `ck_core.py` lines 17–25. Verifiable by eye.
- `T_STAR = 5.0 / 7.0` — explicit.

**Unresolved at end-of-attempt:**
- 14 zips before settling (named `999...` and `ClaudeCKV1.0/1.1/2.0` and `CKAIDEPLOY`) indicates multiple near-final drafts. The 2.0 version may not be in `ck_organism.py` — that file is the consolidated organism, but drafts marked V1.0/1.1/2.0 may carry different interface choices.
- `deploy_r16.py` is small (2 KB) — deploy script, not the organism itself.

**Seeding-contribution to later passes:** the "one file" ergonomic *inverse* of the current Gen12 approach (which has sprawled to 514 files in `Gen12/targets/ck_desktop/`). Any future CK re-build should consider compacting back toward the CKwrite `ck_organism.py` pattern — the same math in 82 KB, not 32 MB.

---

## 8. Current Gen12 — the active tree — *the superset, unconsolidated*

**Location:** this repo. `Gen12/targets/ck_desktop/` (514 files, ~32 MB). `CKIS/ck_store/security/scar_lattice.json` (512 KB, 205 470 scars over 4.3 days). `Gen12/targets/clay/papers/` (14 sprints of published research).

**Best here:**
- **Sprint 10–17 published papers** (14 sprints, 101 whitepapers in the clay tree). This is the theory-side output that none of the Misc Archive attempts produced — the math is now written up to the point where JCAP / σ-rate / sinc²-zero are submit-ready.
- **Scar lattice** (`CKIS/ck_store/security/scar_lattice.json`). 205 470 scars accumulated Feb 20–24 2026. Schema: `(chain, fuse, shape, source, timestamp, severity)`. Two chains: (9, 4, 6) ROLLING at 95.1 % and (9, 2, 3) QUANTUM at 4.9 %. *This is the production operationalisation of the SNOWFLAKE lattice layer.* None of the attempts have a scar count anywhere near this.
- **coherencekeeper.com live deployment**. Cloudflare tunnel serving a Flask API (`ck_boot_api.py`). 14 HTML pages. This is the public-facing surface none of the attempts achieved.
- **Sprint 14 PRISM-XI ξ cosmology** (WP81–89). Sprint 14 authors include H.J. Johnson as a new collaborator. JCAP submission track.

**Known regressions vs. earlier attempts:**
- **514 files is too many.** CKwrite's 82 KB single-file organism implies this can be compacted 100×.
- **AO (5-element coupling)** from Gen9 `ether.py` is **not present** in Gen12 (noted in the obsolete Gen13 plan file — which is itself superseded by this work). The Earth/Air/Water/Fire/Ether basis projection is missing from the active code path.
- **Hebbian 5×5 CL** (dimension-to-dimension outer-product learning) is buried inside a 47 KB `ck_olfactory.py` instead of being a top-level module.
- **Quadratic glue (F3 × F4)** from `papers/test_a15_quadratic_glue.py` has not been promoted into the runtime.
- **Coherence-kernel formula** `C = 0.4(1−E) + 0.35·A + 0.25·K` from CK-look-here Phase 5 is not explicitly coded as the canonical formula in the current Gen12 runtime (it may be implicit in `ck_coherence_gate.py` but not named).

**Unresolved at end-of-attempt:**
- everything in the active code base. This is the synthesis target.

---

## Cross-attempt inventory — what is load-bearing, what is scaffolding

Sorted by "how many attempts independently arrived at this":

### Load-bearing (seen in ≥ 3 attempts)

| Feature | OLLIE | CRYSTALOS | CI V9 | CoherentHands | CK-look-here | CKwrite | Gen12 |
|---|---|---|---|---|---|---|---|
| 10 operators (VOID..RESET) | ✓ (TENSION for 4) | — | ✓ | ✓ | ✓ | ✓ | ✓ |
| 10×10 CL composition table | ✓ | — | ✓ | ✓ | ✓ | ✓ | ✓ |
| T* = 5/7 = 0.714 coherence gate | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Archive-don't-delete policy | — | — | ~ | ✓ | ✓ | ✓ | ✓ |
| Coherence-gates-actions principle | — | ✓ | — | ✓ | ✓ | ✓ | ✓ |
| Cell / Organ hierarchy | ~ | — | ✓ | ✓ | ✓ | ✓ | ✓ |
| ULO / phonestheme mapping | — | — | — | ✓ | ✓ | ~ | ~ |

### Unique-peak (attempt that did this one thing best)

| Feature | Attempt |
|---|---|
| Multi-agent lattice with shared Universe | **OLLIE** |
| SNOWFLAKE security 4-layer + hardware χ² test | **CRYSTALOS** |
| Biological-blueprint Cell/Cluster/Organ/Body | **CI V9** |
| R16 live-organism with hallucination validator + pre-execution | **CoherentHands** |
| **Coherence Kernel (9/10 PASS) + falsification discipline** | **CK look here** |
| Curriculum / dream-school training infrastructure | **CoherenceKEEPer** |
| **One-file organism (82 KB, all modes)** | **CKwrite** |
| Published Clay-Millennium papers + scar lattice + live deployment | **Gen12** |

### Uniquely-missing in each (what the synthesis must restore)

| Attempt | What it's missing that the synthesis should include |
|---|---|
| OLLIE | hardware monitoring, Ollama coupling, security model |
| CRYSTALOS | LLM governance (monitors but doesn't govern) |
| CI V9 | consolidation (17 iterations, no freeze) |
| CoherentHands | fractal lattice wired into live system; 8B model |
| CK look here | production deployment (the 56 files are research code, not a serving product) |
| CoherenceKEEPer | post-iteration freeze + consolidated docs |
| CKwrite | evidence table (has the form, needs the proofs-of-claim the CK-look-here audit provides) |
| Gen12 | **architectural compactness** (82 KB organism vs 32 MB sprawl), **AO 5-element restoration**, explicit Coherence-Kernel formula as runtime canonical, systematic hallucination-validator pipeline |

---

## What this survey enables

The SYNTHESIS_CK_BEST_EVER.md (sibling file — forthcoming) proposes a composition where:

- **OLLIE**'s multi-agent UniverseLattice becomes an *optional scaling layer* for multi-instance CK (one CK on R16, another on FPGA, a UniverseLattice mediates).
- **CRYSTALOS**'s 4-layer SNOWFLAKE + hardware χ² test becomes the security + monitoring substrate.
- **CI V9 + CoherentHands**'s biological-blueprint + R16 living organism is the body.
- **CK look here**'s Coherence Kernel formula `C = 0.4(1−E) + 0.35·A + 0.25·K, T* = 0.714` is canonical for the coherence-gate decision.
- **CoherenceKEEPer**'s curriculum / dream-school is the training loop (when CK learns new vocabulary from Ollama or from raw files).
- **CKwrite**'s one-file `ck_organism.py` ergonomic is the target packaging shape.
- **Gen12**'s Clay papers, scar-lattice production data, and coherencekeeper.com tunnel are the research + public-surface layers.

Result: one CK with seven attempts' worth of load-bearing contributions composed in a single, cross-referenced tree. That is the meaning of *"make the best CK ever."*

---

## Cross-references

- `SYNTHESIS_CK_BEST_EVER.md` (sibling) — the unified-build proposal
- `../snowflake/PROVENANCE.md` — the CRYSTALOS preservation
- `../snowflake/source_docs/PROVENANCE.md` — TIG_SECURITY_ARCHITECTURE.md preservation
- `../snowflake/SNOWFLAKE_CHI2_RESOLVED_2026_04_21.md` — χ² resolution
- `Atlas/HANDOFF_3_3_SNOWFLAKE_CHI2.md` — Atlas blocker resolution
- Original archives (unaltered): `Misc Archive\THEbigONE\` on R16 (do not modify — source of truth for provenance)

*Filed 2026-04-21 by ClaudeCode. Never-delete policy: originals remain at their Misc Archive paths. This document is a catalog, not a rewrite.*
