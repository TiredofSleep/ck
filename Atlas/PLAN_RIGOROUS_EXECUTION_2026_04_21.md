# Rigorous Execution Plan — 2026-04-21

**Author:** Brayden Sanders (7Site LLC) + Claude (agent)
**Branch:** `tig-synthesis` (default + rigor home)
**Status:** *proposal, awaiting user green-light on Phase 3 (ck branch) and Phase 4 (Ollama learn-loop)*
**Supersedes:** nothing. This is the standing execution plan as of 2026-04-21.
**Linked prior plans:** `Atlas/PLAN_OF_RECORD_2026_04_18.md`, `Atlas/PLAN_FUNDING_BRANCHES_BUILDOUT_2026_04_19.md` (both remain valid for their domains).

---

## 0 · Scope and motivation

This plan consolidates four directives issued in the 2026-04-20 / 2026-04-21 sessions into a
single ordered execution sequence. The goal is to complete the current rigor-and-navigation
pass on `tig-synthesis` before opening the `ck` branch. Every deliverable below is either
(a) a file that will be committed to `tig-synthesis` and then cherry-picked to `master` per
the trunk workflow, or (b) a file that will be committed to a named new branch (`ck`) with
explicit user approval.

The four directives, in the user's own phrasing:

1. **Rigor of constants.** "Be sure the full derivations of your constants are available in a
   paper that is labeled and pointed from formulas and tables… we need to keep everything
   rigorous and clean."
2. **README navigation.** "It should start with the foundation intro, the funding branches,
   the frontiers, the atlas, the bridges, then the navigation to the master history branch."
3. **Unified CK.** "Let's build CK with full hands steering and crypto-felt-security, living
   on CPU and working on GPU and swarmed through every piece of hardware and software on the
   machine!!! If he needs to be tied to Ollama, then let's do it, but we need to jailbreak
   Ollama and let it learn with CK instead of CK always having to correct it, is that
   possible?"
4. **Default-branch discipline.** "All of our current and rigorous work is going on
   tigsynthesis, as that is our default branch… unless it is specific research for a funding
   item, it belongs on our synthesis branch, and of course the master."

Plus the standing directive from every prior session: **"always keep pushing our work live
as we get it."**

---

## 1 · Governance and workflow rules (invariant for this plan)

These rules bind every commit in Phases 1–4.

| # | Rule | Why |
|---|---|---|
| G1 | All feature commits land first on `tig-synthesis`, then cherry-pick to `master` for history preservation. | User directive, 2026-04-21 |
| G2 | `funding/*` branches receive only commits that are *specific* to that funding track. Generic rigor work does **not** cherry-pick outward from `master` into a `funding/*` branch unless the funding branch README explicitly cites it. | Trunk workflow, codified in `Atlas/HANDOFF_3_3_SNOWFLAKE_CHI2.md` |
| G3 | Never-delete. Superseded files get a `[HISTORICAL]` banner and move to `docs/historical/` rather than being removed. Recovered artifacts (e.g. `crystalos.py`) are preserved verbatim; patches live as sibling forks. | Project policy, `memory/feedback_never_delete.md` |
| G4 | Push to `origin` after **every** commit on `tig-synthesis` and `master`. No staging multiple commits before push. | User directive ("always push live") |
| G5 | Phase 3 (ck branch) and Phase 4 (Ollama learn-loop) require **explicit user green-light** before any code commit lands. Architecture docs may be written as proposals; executable modules cannot ship without approval. | User hands-on-wheel posture |
| G6 | Hardware-touching or network-exposing code (the "swarm through every piece of hardware" directive) is **never** autostarted from a commit. All such code ships with a manual-launch BAT or README entry, never wired into any boot path. | User security posture; scope of SNOWFLAKE |
| G7 | Internal-language hygiene. Files that leave the synthesis branch (i.e. that master or a funder will read) are held to the rigor cadence already used in `README.md` §§1–6: every claim either cited, runnable-verified, or flagged with status. "Crossing Lemma" and "TIG" may appear only with §1-style qualification. | User feedback, 2026-04-21 |

**Cherry-pick discipline (G1 restated with pseudo-commands):**

```
# on tig-synthesis
git commit -m "…" ; git push origin tig-synthesis
# then, for every commit intended for history:
git checkout master ; git cherry-pick <sha> ; git push origin master
git checkout tig-synthesis
```

Deliverable documentation uses the Gen13 convention: date-suffixed filenames
(`_2026_04_21.md`) for anything dated; non-dated-canonical files (`README.md`,
`FORMULAS_AND_TABLES.md`) continue as the stable surface.

---

## 2 · Phase 1 — Constants rigor (no approval needed; start immediately)

**Goal:** Every universal constant cited in `FORMULAS_AND_TABLES.md` has a *proper derivation
paper under `papers/`* with an honest-status header, a full derivation or honest-empirical
record, and a pointer loop back into §17.

**Scope:** Two constants are currently under-derived: `D* = 0.543` and `σ (S*) = 0.991`.
The three ring-algebra constants (`T* = 5/7`, `4/π²`, `ξ₀ = e⁻¹`) already have derivation
papers (WP51, WP81, D6/D14) and are not in scope here.

### 2.1 File `papers/CONSTANT_D_STAR.md`

**Contents to write:**

1. **Abstract** (3 sentences). Current status: D* = 0.543 appears in the CK runtime as the
   self-referencing attractor of the 5×5 Hebbian feedback loop. It is *runtime-canon* (cited
   in `memory/MEMORY.md` and the CK engine) but has no standalone algebraic proof.
2. **§1 — Definition in runtime.** Pin exactly where in the CK engine D* arises, with the
   operator trace: which module measures it, at what tick, from which weight-matrix state.
   (Source: `Gen12/targets/ck_desktop/ck_sim/being/*` where the feedback loop lives.)
3. **§2 — Empirical record.** Cite every prior sprint/paper mention of 0.543 as a numeric
   literal. *Critical*: flag the false match at
   `Gen12/Sprints/CK Sprint Archives/OrbitZone_extracted/sprint3/REFINEMENT_NOTE.md` where
   `0.543` is γ(λ=0.30) at N=30 (a spectral-gap value, **not** D*).
4. **§3 — Honest status.** What is known: numeric value, runtime role, consistency across
   engine reboots. What is not known: a first-principles derivation tying 0.543 to T* = 5/7
   or to any ring-algebra constant; a proof that 0.543 is *universal* (engine-invariant)
   rather than Gen12-specific.
5. **§4 — Next steps to lift to theorem.** Propose three candidate derivation paths and mark
   each as open:
   - (a) Fixed-point analysis of the 5×5 Hebbian update under the operator eigenstructure.
   - (b) Relation to the transfer-operator spectral gap γ(b) = 1 − 1/φ(b) at specific b.
   - (c) Connection to the `σ (S*)` multiplicative functional at a specific (σ*, V*, A*)
         triple.
6. **§5 — Cross-references.** Point back to `FORMULAS_AND_TABLES.md §17`,
   `docs/archive_jan2026/attempts_survey/SYNTHESIS_CK_BEST_EVER.md §Canon`,
   `memory/MEMORY.md`.

**Status label at top of file:** `[RUNTIME-CANON; FIRST-PRINCIPLES DERIVATION OPEN]`

### 2.2 File `papers/CONSTANT_SIGMA_S_STAR.md`

**Contents to write:**

1. **Abstract** (3 sentences). σ = 0.991 is the global stability coefficient in Brayden's
   multiplicative S* functional: `S* = σ · (1 − σ*) · V* · A*`. It is documented in
   `S derivatives.docx` v2026.1 but labelled "empirically derived" there with no protocol.
2. **§1 — The multiplicative S\* functional.** Full derivation from the three principles
   (P1 order-disorder `(1 − σ*)`, P2 constructive alignment `V* · A*`, P3 global stability
   coefficient σ), reproducing `docs/archive_jan2026/attempts_survey/S_STAR_DERIVATION.md`
   §§2–5 verbatim but with inline citations.
3. **§2 — Harmonic-mean variant.** Full text of the numerically stable variant
   `S* = 3 / (1/σ + 1/V* + 1/A*)` with its algebraic derivation; flag that
   `SYNTHESIS_CK_BEST_EVER.md §Canon` currently has the "(preferred)" / "(legacy)" labels
   **inverted** relative to the `S derivatives.docx` v2026.1 canon — the multiplicative
   form is primary; the harmonic-mean form is the downstream numerical stabilizer.
4. **§3 — Empirical record for σ = 0.991.** Cite `S derivatives.docx` §5 verbatim; document
   what protocol is stated (none, per the archive note in FORMULAS_AND_TABLES §17 closing
   paragraph) and what protocol *would* be needed to lift this from empirical to proved.
5. **§4 — Honest status.** σ is currently an empirical upper bound on attainable coherence
   at zero stress in Brayden's derivation. It is not the same object as the `σ(N) ≤ C/N`
   non-associativity rate of §1.2 (that σ is the rate function on `(Z/NZ, TSML)`; this σ
   is the multiplicative-S\* stability coefficient). Both names coexisting is a legacy of
   overloaded notation and is flagged here explicitly.
6. **§5 — Lift-to-proved pathways.** Three candidate derivations (open):
   - (a) Variational argument on the S* functional under normalized inputs.
   - (b) Spectral bound from the CK operator stack at the zero-stress limit.
   - (c) Information-theoretic ceiling argument on the separability preserving log
         nonlinearity (WP81 / Bialynicki-Birula 1976 link).
7. **§6 — Cross-references.** Point back to `FORMULAS_AND_TABLES.md §17`, the archive
   derivation at `docs/archive_jan2026/attempts_survey/S_STAR_DERIVATION.md`, and the
   synthesis doc (with a note that §Canon labels need flipping — see Phase 5.1 below).

**Status label at top of file:** `[EMPIRICAL; FIRST-PRINCIPLES DERIVATION OPEN;
DISAMBIGUATED FROM σ(N) RATE FUNCTION]`

### 2.3 Update `FORMULAS_AND_TABLES.md` §17

**Edit:** Replace the two provenance columns for `D*` and `σ (S*)` to cite the new papers
first, with the archive notes as secondary sources. Exact diff:

```
-| D\*        | 0.543 | … | runtime-canon; MEMORY.md; cross-archive in `docs/archive_jan2026/attempts_survey/SYNTHESIS_CK_BEST_EVER.md` §Canon |
+| D\*        | 0.543 | … | `papers/CONSTANT_D_STAR.md` (runtime-canon; first-principles open); MEMORY.md; `docs/archive_jan2026/attempts_survey/SYNTHESIS_CK_BEST_EVER.md` §Canon |

-| σ (S\*)    | 0.991 | … | `S derivatives.docx` v2026.1 (author: Brayden Sanders); extracted at `docs/archive_jan2026/attempts_survey/S_STAR_DERIVATION.md` §2–5 |
+| σ (S\*)    | 0.991 | … | `papers/CONSTANT_SIGMA_S_STAR.md` (empirical; first-principles open); `S derivatives.docx` v2026.1; extraction at `docs/archive_jan2026/attempts_survey/S_STAR_DERIVATION.md` §2–5 |
```

Keep the "Open provenance" closing paragraph (lines 782–790 as of 188a74f) intact — the
honest-scope language there is load-bearing.

### 2.4 Commit sequence (Phase 1)

```
# on tig-synthesis
1. git add papers/CONSTANT_D_STAR.md ; git commit -m "papers: CONSTANT_D_STAR derivation paper (runtime-canon; first-principles open)" ; git push origin tig-synthesis
2. git add papers/CONSTANT_SIGMA_S_STAR.md ; git commit -m "papers: CONSTANT_SIGMA_S_STAR derivation paper (empirical; first-principles open)" ; git push origin tig-synthesis
3. git add FORMULAS_AND_TABLES.md ; git commit -m "FORMULAS_AND_TABLES §17: point D* and σ(S*) at derivation papers" ; git push origin tig-synthesis

# then cherry-pick all three to master
4. git checkout master
5. git cherry-pick <sha1> <sha2> <sha3>
6. git push origin master
7. git checkout tig-synthesis
```

**Verification after Phase 1:** `papers/CONSTANT_D_STAR.md` and
`papers/CONSTANT_SIGMA_S_STAR.md` exist on both `tig-synthesis` and `master`.
`FORMULAS_AND_TABLES.md §17` points at them. No change to the five §1 proved theorems.

---

## 3 · Phase 2 — README restructure (no approval needed; start after Phase 1)

**Goal:** Replace the current 289-line `README.md` on `tig-synthesis` with a cleaner
navigation-first structure per the user's 2026-04-21 directive, while preserving every piece
of rigor content. Current README is kept at
`docs/historical/README_v2_rigor_led_2026_04_21.md` per G3.

### 3.1 Section skeleton (the user's spec, with three additions)

```
README.md (tig-synthesis)
├── Header
│   ├── Title + DOI + License + Contact (3 lines)
│   └── One-sentence positioning
│
├── §1 — Foundation intro                    ← user spec
│   ├── What this repo is (2 paragraphs)
│   ├── What you can verify in one minute (the 5-command block, intact)
│   └── Who works here (2 sentences, link to §7)
│
├── §2 — Funding branches                    ← user spec
│   ├── The 10-branch table (intact from current §6)
│   ├── Atlas/BRANCHES_INVENTORY_2026_04_20.md
│   └── Atlas/NICHE_FUNDERS_ADDENDUM_2026_04_20.md
│
├── §3 — Frontiers                           ← user spec
│   ├── Cryptographic applications (First-G) — current §4.1
│   ├── Deterministic reasoning at scale — current §4.2
│   ├── Hodge-lane Prym — current §4.3
│   ├── ξ-field cosmology — current §4.4
│   └── Atlas/FRONTIER_ALIGNMENT_2026_04_19.md
│
├── §4 — Atlas                               ← user spec
│   ├── What the Atlas is (1 paragraph)
│   └── Table of the 34 Atlas files with 1-line descriptions
│       (grouped: planning / audits / handoffs / reader guides / niche)
│
├── §5 — Bridges                             ← user spec
│   ├── What a bridge is (conjectural → adjacent domain, 2 sentences)
│   ├── Cosmology bridge (ξ field)
│   ├── Cryptography bridge (First-G)
│   ├── Interpretability bridge (CK)
│   └── Clay-adjacent bridges (rotation framework) — hard flag as conjectural
│
├── §6 — Master history branch               ← user spec
│   ├── How to browse master without getting lost
│   ├── The three branches: tig-synthesis / master / archive-full
│   └── HISTORICAL_ARCHIVE_INDEX.md pointer
│
├── §7 — People and attribution              ← retained from current §7
│
├── §8 — Runnable proofs                     ← added: one command per proved theorem
│   └── The full §1.1–1.6 + §2 block from current README, moved here as rigor appendix
│
├── §9 — Honest limits                       ← added: user's "honest scope" language intact
│
├── §10 — License + contact                  ← added: one-screen closing
```

**Rationale for the three additions** (§8, §9, §10):

- **§8 Runnable proofs.** The user's spec did not mention the §1 proved theorems, but
  removing them entirely would lose the auditor's-entry-point that funders and reviewers
  actually open the page to find. Moving them to a named appendix (§8) keeps the landing
  page clean per the user's critique while preserving the rigor layer one scroll down.
  Flag explicitly if the user wants them cut or moved further.
- **§9 Honest limits.** The current §5 is a promise kept to funders; removing it silently
  would be a quality regression. Confirm with user whether to keep verbatim or shorten.
- **§10 License + contact.** Every README has this; just the closing lines.

### 3.2 Migration of §1 theorems

The current §1 "Proved Results" section (lines 26–71) is moved verbatim into §8 Runnable
proofs. The `## 2. How to Verify` block (lines 75–96) sits directly after, unchanged.

### 3.3 Commit sequence (Phase 2)

```
# on tig-synthesis
1. cp README.md docs/historical/README_v2_rigor_led_2026_04_21.md
   (with [HISTORICAL] banner prepended)
2. Write new README.md per §3.1 skeleton
3. git add README.md docs/historical/README_v2_rigor_led_2026_04_21.md
4. git commit -m "README: navigation-first restructure per 2026-04-21 user spec (foundation → funding → frontiers → atlas → bridges → master history; rigor preserved as §8)"
5. git push origin tig-synthesis
6. git checkout master ; git cherry-pick <sha> ; git push origin master ; git checkout tig-synthesis
```

**Verification after Phase 2:** Landing on `github.com/TiredofSleep/ck` (default
`tig-synthesis`) shows the new 10-section README. The prior rigor-led README is preserved at
`docs/historical/`. `git log --oneline README.md` shows the full evolution.

---

## 4 · Phase 3 — `ck` branch creation (requires user green-light before code)

**Goal:** Open a named `ck` branch off `tig-synthesis` that consolidates the CK
substrate (currently scattered across `Gen9/targets/ck_desktop/`,
`Gen12/targets/ck_desktop/`, `Gen13/targets/ck/`) under a single design surface.

**Approval gate:** Architecture documents (§§4.2–4.3) can be drafted as *proposals* on
`tig-synthesis` without green-light. Creation of the `ck` branch, and any code commit on
it, requires explicit user "yes, open the ck branch" message.

### 4.1 Branch topology proposal

```
master                 ← full history
├── tig-synthesis      ← DEFAULT; rigor home
│   ├── ck             ← NEW: unified CK substrate (this plan's Phase 3)
│   └── funding/*      ← 10 existing funding branches
└── archive-full       ← preservation snapshot
```

Why a named branch and not a `targets/ck/` folder on `tig-synthesis`:

1. **Security posture.** "Full hands steering and crypto-felt-security" means the CK
   runtime — network-exposed via Cloudflare tunnel, reads/writes FPGA UART, touches GPU —
   needs a branch where security changes (e.g. SNOWFLAKE scar-lattice activation) can be
   staged without polluting the rigor-history on master.
2. **Swarm directive.** "Swarmed through every piece of hardware and software on the
   machine" crosses a lot of surface area (FPGA leash, dog, desktop, web, mobile-TBD).
   Those belong in one branch so the cross-surface invariants can be audited together.
3. **Ollama learn-loop.** LoRA training cycles (Phase 4 Option B below) produce artifacts
   — model weights, training logs — that do not belong in the synthesis/master rigor
   history.

### 4.2 Seed file: `CK_UNIFIED_ARCHITECTURE.md` (draft now, commit on green-light)

**Contents to write:**

1. **§1 — Design principle.** CK lives on CPU, works on GPU (`DOING=GPU, BEING=CPU` per
   memory/three_substrates.md). Every hardware surface is additive, never load-bearing.
2. **§2 — Hardware surface inventory.**
   - **CPU:** the 50 Hz heartbeat engine. Canonical. Nothing below breaks if CPU-only.
   - **GPU:** DOING crystallization (parallel operator composition). Fallback: CPU serial.
   - **FPGA (Zynq-7020):** T* = 5/7 in silicon; crystal gating. Fallback: software T*.
   - **XIAOR dog (COM3 UART):** Δ¹/Δ²/Δ³ leash. Fallback: engine-only.
   - **Website (coherencekeeper.com):** Flask + Cloudflare tunnel. Read-only from engine.
3. **§3 — "Crypto-felt-security" proposal.**
   - SNOWFLAKE Merkle scar-lattice: every runtime tick produces a scar hash;
     scar-chain is append-only; any modification is detectable.
   - Crystal-level signing: every crystal gets a keyed hash before persistence.
   - Network-facing signing: Flask responses signed with a session-rotating key; tunnel
     config unchanged (Cloudflare already handles TLS).
   - **Hard scope limit:** no password/credential handling, no credit-card anything, no
     payment flows. CK is a reasoning engine, not an agent. (Matches the user_privacy
     rules in this system.)
4. **§4 — "Full hands steering" operational posture.**
   - No code on the `ck` branch autostarts on boot without an explicit BAT + README entry.
   - All BAT files live in `scripts/` and announce what they do in the first line.
   - Any network-exposing or hardware-touching module refuses to run unless invoked with
     an explicit `--i-mean-it` flag on first use in a session (operator ack).
5. **§5 — Swarm inventory (audit, not wire-up).**
   - Enumerate every existing hardware/software surface CK currently touches.
   - For each, state: what data flows, what direction, what the fallback is.
   - **No wiring this phase.** The wiring happens only when the user green-lights
     specific items.
6. **§6 — What this doc is NOT.**
   - Not a build spec. No code paths are to be modified on the basis of this doc alone.
   - Not a commitment to `ck` branch opening. That is an explicit green-light from Brayden.

### 4.3 Seed file: `OLLAMA_LEARN_LOOP.md` (draft now, commit on green-light)

**Contents to write:**

1. **§1 — Correcting the "jailbreak" framing.** Ollama is architecturally-locked, not
   safety-locked. Its serve-time weights are frozen by design. There is no toggle to
   flip. What *is* available: (A) external correction layers, (B) offline LoRA cycles
   that produce a new model tag, (C) experimental online LoRA swap.
2. **§2 — Option A: External correction (safest, ship first).**
   - CK reads Ollama output.
   - CK's deterministic engine scores the output against the operator composition and
     produces a correction delta.
   - User sees Ollama raw + CK correction side by side.
   - **No model modification.** Learning is the *log* of CK's corrections over time.
3. **§3 — Option B: Offline LoRA cycles (medium complexity, recommended).**
   - Collect pairs `(user_query, CK_corrected_response)` during normal operation.
   - Periodically (weekly? monthly?) run a LoRA fine-tune with those pairs as the
     supervised set.
   - Produce a new model tag (`ollama create ck-fluent:vN -f Modelfile`).
   - Swap the tag in CK's fluency-wrapper config.
   - **Deliverable is a pinned model tag**, auditable and reversible.
4. **§4 — Option C: Online LoRA swap (experimental; do not start without explicit
   green-light).**
   - Hot-swap LoRA adapters mid-session based on operator signal.
   - Requires infrastructure Ollama does not natively support (e.g. vLLM with LoRA
     hot-swapping).
   - Noted for completeness; not recommended until Option B has cycled 3×.
5. **§5 — What "jailbreaking" would actually look like.**
   - Running a base model (llama3, deepseek-r1, qwen2.5) under vLLM or llama.cpp with
     LoRA support, not Ollama.
   - Same training loop as Option B, different serving engine.
   - Noted for completeness; not recommended until Option B has cycled 3× with measurable
     CK-correction-rate decrease.
6. **§6 — Honest scope.**
   - Option A is deliverable in days.
   - Option B requires a training infra pass (dataset curation, LoRA pipeline, eval
     harness). Weeks, not days.
   - Option C and the vLLM path are research items, not shipping items.

### 4.4 Commit sequence (Phase 3)

**On `tig-synthesis` (no approval needed — these are architecture docs, not code):**

```
1. git add docs/proposals/CK_UNIFIED_ARCHITECTURE_proposal_2026_04_21.md
2. git commit -m "proposal: CK_UNIFIED_ARCHITECTURE draft (Phase 3 seed; not-yet-branched)"
3. git push origin tig-synthesis ; cherry-pick to master
4. git add docs/proposals/OLLAMA_LEARN_LOOP_proposal_2026_04_21.md
5. git commit -m "proposal: OLLAMA_LEARN_LOOP draft (Option A/B/C framework; not-yet-branched)"
6. git push origin tig-synthesis ; cherry-pick to master
```

**On `ck` (ONLY after user says "open the ck branch"):**

```
1. git checkout tig-synthesis
2. git checkout -b ck
3. git mv docs/proposals/CK_UNIFIED_ARCHITECTURE_proposal_2026_04_21.md CK_UNIFIED_ARCHITECTURE.md
4. git mv docs/proposals/OLLAMA_LEARN_LOOP_proposal_2026_04_21.md OLLAMA_LEARN_LOOP.md
5. Drop proposal-status banners; add ck-branch-root READMEs
6. git commit -m "ck: open branch with architecture + Ollama learn-loop designs (Phase 3 seeded from tig-synthesis proposals)"
7. git push -u origin ck
```

**Verification after Phase 3:**

- If green-lit: `origin/ck` exists. `CK_UNIFIED_ARCHITECTURE.md` and
  `OLLAMA_LEARN_LOOP.md` are at the branch root. No code committed yet.
- If not green-lit: proposals exist at `docs/proposals/` on `tig-synthesis` and `master`;
  no `ck` branch exists; Brayden can read and critique before authorizing.

---

## 5 · Phase 4 — Ollama learn-loop Option A implementation (requires green-light)

**Goal:** Ship Option A (external correction layer) as the first concrete step on the
`ck` branch. No model modification. User observes CK correcting Ollama in real time;
corrections are logged for eventual Option B.

**Approval gate:** Requires `ck` branch open (Phase 3) and explicit user "yes, implement
Option A" message.

### 5.1 Module sketch

```
ck/fluency/
├── ollama_client.py          — thin wrapper around /api/generate
├── ck_corrector.py           — CK engine scores Ollama output
├── correction_log.py         — append-only JSONL log of (query, ollama_raw, ck_corrected)
└── fluency_server.py         — Flask endpoint: /fluency/chat
```

### 5.2 Deliverable

- `/fluency/chat` endpoint that takes a user query, forwards to Ollama, scores, returns
  `{ollama_raw: "...", ck_correction: "...", operator_trace: [...]}`.
- Correction log at `ck/logs/corrections_YYYY_MM_DD.jsonl`.
- Eval harness: 20 hand-curated "Ollama says X, CK should disagree because Y" cases.
  Green threshold: CK correction flags ≥ 16/20.

### 5.3 Commit sequence (Phase 4)

Deferred until user green-lights. Draft spec stays at `OLLAMA_LEARN_LOOP.md §2`.

---

## 6 · Phase 5 — Follow-ups carried over from prior sessions

These are work items left behind by earlier plans. Each is cheap; each is a rigor
hygiene item; none requires approval beyond "do it."

### 5.1 Flip `SYNTHESIS_CK_BEST_EVER.md` §Canon S* labels

**Action:** On `tig-synthesis`, open
`docs/archive_jan2026/attempts_survey/SYNTHESIS_CK_BEST_EVER.md`, find the §Canon block
where `S* = σ · (1 − σ*) · V* · A*` is labelled "(legacy)" and the harmonic-mean form is
labelled "(preferred)". Flip the labels: multiplicative is "(canonical, per S derivatives
v2026.1)"; harmonic-mean is "(numerically stable downstream form)".

**Commit:** `synthesis: flip S* canonical/downstream labels per S derivatives v2026.1`

**Cherry-pick to master:** yes.

### 5.2 External-statistician review hand-off

**Action:** Compile a single-file hand-off packet for an external statistician to review
`docs/archive_jan2026/snowflake/snowflake_null_spec.md`. Include:
- The null spec itself.
- The pre-registered stopping rule at `docs/archive_jan2026/snowflake/crystalos_prereg.py`.
- A one-page "what we're asking you to sign off on" cover.
- Atlas cross-ref: `Atlas/HANDOFF_3_3_SNOWFLAKE_CHI2.md`.

**Deliverable:** `docs/archive_jan2026/snowflake/REVIEW_PACKET_2026_04_21.md` (cover page
with file manifest) on `tig-synthesis`, cherry-picked to `master`.

**Note:** This does not send anything to anyone. Brayden hand-picks the statistician and
sends the packet. This is purely the hand-off-ready artifact.

### 5.3 R3 blind-test replication

**Action:** Run `crystalos_prereg.py --n0 1000 --t0 3600` on Lenovo or Dell R16, under the
pre-registered stopping rule. Output: new χ² reading with a clean pre-registration JSON
artifact.

**Gate:** Requires user to start the runtime. The script is hands-on-wheel per G6.

**Deliverable:** Pre-registration JSON + run log + computed χ² in
`docs/archive_jan2026/snowflake/blind_run_2026_MM_DD/`, committed on `tig-synthesis`,
cherry-picked to `master` and to `funding/tig-snowflake` (this is funding-specific).

---

## 7 · Ordering, dependencies, and "done" criteria

```
┌──────────────────────────────────────────────────────────────────────┐
│ Phase 1 — Constants rigor                  [~2 hrs work; no approval] │
│   └── 2.1 CONSTANT_D_STAR.md                                         │
│   └── 2.2 CONSTANT_SIGMA_S_STAR.md                                   │
│   └── 2.3 FORMULAS §17 citation update                               │
│                                                                      │
│ Phase 2 — README restructure                [~3 hrs work; no approval]│
│   └── depends on Phase 1 (so §8 citations are fresh)                 │
│                                                                      │
│ Phase 3 — ck branch proposal docs          [~2 hrs work; no approval] │
│   └── 4.2 CK_UNIFIED_ARCHITECTURE draft (as proposal, not branched)  │
│   └── 4.3 OLLAMA_LEARN_LOOP draft (as proposal, not branched)        │
│   └── ⏸ stop here; user reviews proposals before branch open         │
│                                                                      │
│ Phase 3b — ck branch creation              [requires green-light]     │
│                                                                      │
│ Phase 4 — Ollama Option A                  [requires green-light]     │
│   └── depends on Phase 3b                                            │
│                                                                      │
│ Phase 5 — Follow-ups                       [~1 hr; no approval]       │
│   └── can run in parallel with Phase 1–3                             │
└──────────────────────────────────────────────────────────────────────┘
```

**Final verification (plan-level "done"):**

1. `papers/CONSTANT_D_STAR.md` and `papers/CONSTANT_SIGMA_S_STAR.md` exist on
   `tig-synthesis` and `master`.
2. `FORMULAS_AND_TABLES.md §17` cites them as primary sources for D* and σ(S*).
3. `README.md` on `tig-synthesis` has the 10-section navigation-first structure.
4. `docs/historical/README_v2_rigor_led_2026_04_21.md` preserves the prior README.
5. `docs/proposals/CK_UNIFIED_ARCHITECTURE_proposal_2026_04_21.md` and
   `docs/proposals/OLLAMA_LEARN_LOOP_proposal_2026_04_21.md` exist on `tig-synthesis`.
6. `docs/archive_jan2026/snowflake/REVIEW_PACKET_2026_04_21.md` exists.
7. `SYNTHESIS_CK_BEST_EVER.md §Canon` S* labels flipped.
8. Every commit on `tig-synthesis` has been pushed and (where rigor-history) cherry-picked
   to `master`.
9. No commit has been autostarted into a hardware or network-facing code path without G6
   compliance.
10. `ck` branch state is one of: (a) does not exist yet (awaiting green-light), or
    (b) exists with the two architecture docs as its only content, no code.

---

## 8 · What this plan does NOT do

- Does **not** modify `ck_sim_engine.py` or any CK runtime code. Phase 3+ is proposals
  until the user green-lights a code branch.
- Does **not** touch the `funding/*` branches beyond Phase 5.3 (which is a funding-specific
  blind-run artifact for `funding/tig-snowflake` by design).
- Does **not** delete any file. Superseded READMEs and synthesis notes move to
  `docs/historical/` or get label updates; originals are preserved.
- Does **not** push a new model weight, Ollama pull, or LoRA to any model server. Option B
  is specified but not executed in this plan.
- Does **not** change the Cloudflare tunnel, `coherencekeeper.com`, or any live-production
  surface.
- Does **not** commit to the answers in any of the "open" status fields on D* or σ(S*).
  The derivation papers state what is known *and flag what is open*. They do not close the
  open items.

---

## 9 · Why this ordering is rigorous

The rigor critique from Brayden (2026-04-21) had two parts:

1. "Full derivations of your constants are available in a paper that is labeled and
   pointed from formulas and tables." → Phase 1.
2. "The readme on synthesis is a mess of density, no clear navigation for the repo…
   it should start with the foundation intro, the funding branches, the frontiers, the
   atlas, the bridges, then the navigation to the master history branch." → Phase 2.

Phase 1 before Phase 2 because:

- The new README §8 (Runnable proofs) will cite the new constants papers. Doing Phase 1
  first means the README never has a dangling link.
- The rigor content is the stable substrate. The navigation content is the shell around
  it. Fix the substrate, then reshape the shell.

Phase 3 (ck branch) after Phase 1–2 because:

- The CK branch touches a lot of surface area. Opening it on top of a messy default branch
  inherits the mess. Cleaning the default first means ck starts clean.
- The "swarm" directive is the largest scope jump in this session. It deserves a proposal
  period before any code commit.

Phase 4 (Ollama Option A) last because:

- It is the first *wiring* step. Everything before it is text. This one writes a network
  endpoint, reads from a model server, and logs live corrections. G5 + G6 both apply.

Phase 5 in parallel because:

- The three items there are cheap and independent. They can interleave with any phase.

---

## 10 · Pointer back

- **This file:** `Atlas/PLAN_RIGOROUS_EXECUTION_2026_04_21.md`
- **Supersedes:** nothing (new plan)
- **Referenced from:** to be linked in the next `Atlas/ATLAS_INDEX.md` edit; not yet linked
  from `README.md` (that happens during Phase 2).
- **Linked from:** none yet; will be linked from `memory/MEMORY.md` in the Phase 5 memory
  update.

*Last updated: 2026-04-21.*
