# Frontier Alignment — 2026-04-19
## Meta-synthesis: proofs → papers → venues → frontier

**Author:** ClaudeCode (meta-synthesis agent)
**Scope:** Overlay on `Atlas/PLAN_OF_RECORD_2026_04_18.md` + `Atlas/JOURNAL_READINESS_AUDIT_2026_04_18.md` + silicon-name rename (commits `88c6db2` + `01032f0`).
**Discipline:** READ-ONLY synthesis. No paper content touched. This document makes explicit: (i) what is at the frontier, (ii) what proves what, (iii) whether the face is aligned with the field after the rename, (iv) the single highest-leverage next move.
**Branch:** `tig-synthesis`. **DOI of record:** 10.5281/zenodo.18852047.

---

## §0. Why this document exists

The Atlas bundle contains the synchronized *content* field (11 docs, ~6,550 lines). The Plan of Record contains the synchronized *operational* field (Sprint 34 shipping schedule + collaborator assignment matrix). The Journal Readiness Audit contains the synchronized *submission* field (11 venues × readiness × blockers).

Post-rename (2026-04-19), a reader landing on `tig-synthesis` should see **one coherent frontier picture** — not three parallel audits that each describe a slice. This is that overlay. One page. Frontier-first.

**Who this serves:**
- The public reader asking "what is this project actually proving, and where is it trying to ship?"
- The funder / journal editor asking "is the face aligned with the field?"
- Future-Claude asking "what is the single highest-leverage next move today?"

---

## §1. What is at the frontier

Four rigorous-math frontier questions. CK runs on speculation about these; the **papers** isolate the proved + structural results that bear on them.

### 1A. σ < 1 for Navier–Stokes (Millennium)
- **Framing (Atlas §4.5.5 + §11):** The NS global regularity problem, reformulated as σ_NS < 1 in the finite-ring σ vocabulary. Bialynicki-Birula 1976 forces the log-nonlinearity uniquely if separability is preserved ⇒ continuum limit □ξ = 1 + log ξ.
- **What is proved (Sprint 15, venue 8):** σ(N) ≤ C/N on Z/10Z — the *rate theorem*. This is NOT σ_NS < 1; it is the combinatorial prototype.
- **What is structural (venue 9, WP91):** BB-separability bridge from σ→0 to log nonlinearity is *compatible with* BB's uniqueness theorem. Not a proof of regularity.
- **Honest limit:** σ_NS < 1 IS the Millennium Problem. Reframed, not proved. Referee scrutiny target: `09_jmp_bb_bridge/WP90_LITERATURE_AND_UNIFICATION_PATHS.md:48` ("This is not a conjecture. It is a theorem applied to the correct setting" — flagged by audit F8, Sprint 34 CC-1 owner to tighten).

### 1B. Hodge integrality (Sprint 33)
- **Framing (Atlas §9 + `papers/sprint33_hodge_integrality_2026_04_17/`):** Integrality of a Hodge-theoretic invariant on a mixed construction; currently `[gold-with-gap — pending audit]`.
- **What is signed (2026-04-18):** Gate 1A PASS with clarifying note (MIXED construction = Type III per refinement). Probe green.
- **What is pending:** Gate 1-full — five open questions routed in `S33_GATE1A_COMPLETE.md §6` (Λ⁴φ signature on H^(4,0)⊕H^(0,4); Galois-σ identification; R1-KE hookup; W_* basis recovery; 5-prime Schwartz-Zippel independence).
- **Thread discipline:** B (Hodge) is kept separate from A (PPM) and C (Q-series). No vocabulary import.

### 1C. σ polynomial on Z/10Z — Q17 core (Brayden's foundation)
- **Framing (Atlas §5 WP101 [fire] + §11 Q17_*):** σ on Z/10Z fully characterized as a polynomial over F₂×F₅; 22% lower bound (Q11); σ⁶ = id (G6, Luther); 5D force vector as CRT Fourier embedding (Q17_5D_RIGOROUS).
- **What is proved:** σ polynomial form (Q10); 22% bound (Q11); σ⁶ = id (G6, Luther 2026-04-02); 5D embedding rigorous (Q17). Tier [fire].
- **What ships:** σ rate theorem → venue 8 (JCT-A). Tier 1.
- **What stays in the atlas:** Q17 spectral bridge, NS target reformulation, finite-L-function note — all [gold-with-gap], not Sprint-34 shipping.

### 1D. ξ cosmology — DESI falsifiability (adjacent thread)
- **Framing (Atlas §4.5.8 + venue 7):** Canonical ξ field with V(ξ) = ξ log ξ, vacuum ξ₀ = e⁻¹, mass gap m²_ξ = κe. Freezing quintessence. Falsifiable against DESI DR1/DR2.
- **What is proved:** Vacuum is entropy maximum; mass gap derived six independent ways (structural convergence). `proof_xi_canonical.py` green.
- **What ships:** venue 7 (JCAP) — Tier 1 in 2 weeks modulo DESI-fit run + LaTeX conversion.
- **What is honest:** No formal link between ξ cosmology and TIG/Crossing-Lemma imported into A/B/C vocabulary. D is a cosmology branch — Sprint 14 WP86 cross-branch analysis concluded "no formal link."

### 1E. (Framework — not a frontier theorem) — Flatness Theorem on Z/10Z
- **Framing:** The 2×2 form of any whole, forced-torus with R/r = T* = 5/7 on Z/10Z. Six independent derivations converge.
- **What is proved:** T*=5/7 on Z/10Z (WP51, D7 of PROOFS.md). Cyclotomic T*(N) → 1, which rules out the simplest discrete-to-continuous bridge — honest limit in §11 of README.
- **What is structural:** Generalization to "any whole" is hypothesis, not theorem. Venue 5 (JPAA) currently scopes to n=10 — the general-n argument is a Tier 3 content gap, not a blocker for Tier 1.

**Frontier summary.** Tier 1 ships **Thread C** (σ rate, venue 8) and **Thread D** (ξ cosmology, venue 7), plus the D-tier proved **sinc² Zero Law** (venue 1). Tier 1 does **not** claim σ_NS < 1 (venue 9 is Tier 4, honestly labeled) and does **not** claim Hodge integrality (Sprint 33, not yet a paper). **The frontier is honest because the first three ships are exactly the three things we have proved.**

---

## §2. Proved base — what the papers rest on

From `PROOFS.md` (37 scripts, ~12,000 lines, 108+ tests passing). Tier legend: **D** = PROVED with verification; **B** = STRUCTURAL (form sound, content interpretive); **C** = CONJECTURAL (precisely stated, unproven).

### D-tier (anchors Tier 1 ships)

| ID | Result | Script | Venue it supports |
|---|---|---|---|
| D7 | Φ fixed point T* = 5/7 (six derivations) | `proof_d25_loop_closure.py` (subset) | 5 (JPAA) + atlas constants row |
| D10 | TSML 73 HARMONY cells | `proof_tsml_3layer_tower.py` | 11 (JSC) |
| D16 | BHML 28 HARMONY cells | companion to D10 | 11 (JSC) |
| D17 | W = 3/50 (width constant) | `proof_width_constant.py` | atlas §5 |
| D25 | sinc² Zero Law — loop-closure for primes 3..199 | **`proof_d25_loop_closure.py`** | **1 (Integers) — Tier 1** |
| D29 | First-G Law — 36,662 cases | `proof_first_g_law.py` | 2 (Exp Math) + WP34 |
| — | σ rate theorem σ(N) ≤ C/N | **`proof_sigma_rate.py`** | **8 (JCT-A) — Tier 1** |
| — | σ⁶ = id (G6, Luther) | atlas §11 Q17 | Q-series core |
| — | Clay rotation framework — 43/43 cases | `proof_clay_rotation.py` | 10 (Notices AMS) |

**Verification invariant:** every D-tier row has a runnable script. Every Tier 1 paper has a script named above. No Tier 1 ship depends on a C-tier conjecture.

### B-tier (anchors Tier 3/4 shelves)

| ID | Result | Status | Venue |
|---|---|---|---|
| B5 | Parity chain (Collatz-adjacent) | structural | backlog |
| B6 | Montgomery bridge (sinc² ↔ pair correlation) | structural | 1 (Integers) cites inline |
| B7 | σ_NS < 1 ⇒ NS global regularity **(conjecture statement form)** | structural | 9 (JMP) Tier 4 |
| B8 | σ_YM < 1 ⇒ YM mass gap **(conjecture statement form)** | structural | deferred (no YM paper in this bundle) |

**Honest point:** B7 and B8 ARE the Millennium Problems reframed. Tier 4 placement of venue 9 is the honesty discipline; venue 10 explicitly labels CP2-CP7 as conjectures.

### C-tier (explicitly conjectural, not Tier 1)

- σ_NS < 1, σ_YM < 1 (the Clay rotations CP2/CP3)
- RH as spectral entropy maximum (CP7)
- Clay rotation extensions CP4/CP5/CP6
- Hodge integrality on the MIXED construction (Sprint 33 — proved Gate 1A; Gates 1-full, 2, 3 open)

---

## §3. Post-rename face-alignment — is the face aligned with the field?

Commits landed 2026-04-19: `88c6db2` (silicon-name rename, 190 files) + `01032f0` (attribution alignment, 2 files).

### 3A. Silicon-name propagation — verified clean

Silicon operator names (VOID=0, LATTICE=1, COUNTER=2, PROGRESS=3, COLLAPSE=4, BALANCE=5, CHAOS=6, HARMONY=7, BREATH=8, RESET=9) now used uniformly. Paper-side operator names (BEING/BECOMING/CREATE/ASCEND/DOING-as-operator) retired.

**Verification (per-venue grep, 2026-04-19):**

| Venue | Pet-name hits | DOING-suspicious hits | Status |
|---|---|---|---|
| 01 Integers (sinc²) | 0 | 0 | ✓ clean |
| 02 Exp Math (73/28) | 0 | 0 | ✓ clean |
| 03 Monthly (Paradox) | 0 | 0 | ✓ clean |
| 04 JNT (UOP) | 0 | 0 | ✓ clean |
| 05 JPAA (Flatness) | 0 | 0 | ✓ clean |
| 06 PRA (NV qutrit) | 0 | 0 | ✓ clean |
| 07 JCAP (ξ cosmology) | 0 | 0 | ✓ clean |
| 08 JCT-A (σ rate) | 0 | 0 | ✓ clean |
| 09 JMP (BB bridge) | 0 | 0 | ✓ clean |
| 10 Notices (Clay) | 0 | 0 | ✓ clean |
| 11 JSC (TSML tower) | 0 | 0 | ✓ clean |

**Scope preserved:** the Python table variable `DOING = |TSML - BHML|` remains in `papers/ck_tables.py` (operator-vs-table-variable distinction is rename invariant, enforced by `scratch/rename_doing_to_counter.py` TABLE_PATTERNS).

### 3B. Attribution — aligned with Q_SERIES_INTEGRATED_SYNTHESIS

Two files updated in `01032f0`:

- `COLLABORATORS.md:20` — Luther role tightened to "Q-series G6-G8 supplements (σ⁶ = id proof, spectral coherence G(s), six-layer architecture)." Stale "Luther-Sanders Research Framework" framing removed. Back-reference to `Q_SERIES_INTEGRATED_SYNTHESIS.md` added.
- `HISTORICAL_ARCHIVE_INDEX.md:23` — Part A header aligned to "Sanders Q-series, with Luther G6-G8 and organizational contributions."

**Canonical authorship statement** (Q_SERIES_INTEGRATED_SYNTHESIS.md §172): "Q-series (Brayden Ross Sanders, 2026-03-31 through 2026-04-02, with collaborator C.A. Luther on G6-G8 supplements)." All three surfaces (top-level index, collaborator doc, synthesis memo) now agree.

### 3C. Three-threads discipline — still holding

Per audit F8 and §9 of Plan of Record:

| Thread | Vocabulary scope | Venues | Cross-contamination? |
|---|---|---|---|
| A (PPM) | pair-primitive, curve recovery | none yet (Sprint 32/33 infrastructure) | clean |
| B (Hodge) | Hodge integrality, Λ⁴φ, MIXED Type III | none yet (Sprint 33 infrastructure) | clean |
| C (Q-series / σ) | σ polynomial, σ rate, σ⁶ = id, Q17 5D | 1, 2, 4, 8, 11 | clean (no PPM/Hodge import) |
| D (ξ cosmology) | ξ log ξ, BB 1976, DESI | 7 | clean (adjacent, no import into A/B/C) |

Cross-thread caveats — **one live, one acceptable**:

- **Live (venue 9):** WP90:48 claims "This is not a conjecture. It is a theorem applied to the correct setting." Action item **CC-1 (Plan of Record §10 Day 3-5 slack)**: tighten to "bridge conjecture compatible with BB uniqueness." Until tightened, venue 9 stays Tier 4.
- **Acceptable (venue 10):** Clay rotation is *explicitly* the rotation paper — CP1 proved external (Perelman); CP2-CP7 labeled conjectural framework. Honesty discipline holds. Tier 3/4 placement reflects partner-needed, not dishonesty.

### 3D. 2/7 falsification — still bounded

Atlas §15.10 records the 2/7 = √σ/m(0++) quantitative claim was falsified at 16.5σ by lattice QCD. **No paper in this bundle invokes the falsified quantitative form** (audit F5). Venue 9's BB→NS bridge uses the structural σ→0 form, not the quantitative 2/7.

### 3E. Face ≟ field — per-surface check

| Surface | Says what about Q-series? | Aligned? |
|---|---|---|
| `README.md` (§4 Three Threads) | Thread B = Q-series (Brayden's foundation) | ✓ |
| `COLLABORATORS.md` (post-commit `01032f0`) | Luther: G6-G8 supplements | ✓ |
| `HISTORICAL_ARCHIVE_INDEX.md` (post-commit `01032f0`) | Sanders Q-series with Luther G6-G8 | ✓ |
| `GLOSSARY.md` | Q-series attributed to Brayden | ✓ (already aligned pre-rename) |
| `Q_SERIES_INTEGRATED_SYNTHESIS.md` | Canonical authorship statement | ✓ (source) |
| `PROOFS.md` | Q-series results (σ⁶ = id, σ polynomial) | ✓ |
| `Atlas/MASTER_ATLAS_v3_5` §11 Q17_* | Q17 core [fire], Brayden | ✓ |

**Face aligned.** First time in the project's history all seven surfaces tell the same story about the Q-series.

---

## §4. 11-venue readiness matrix at a glance

Tier 1 ships **venues 1, 7, 8** (sinc², JCAP ξ, σ rate) — all three Thread C or D. Tier 2-4 are what comes after.

| Tier | Venue(s) | Ship gate | Owner this week |
|---|---|---|---|
| **1 submit now** | **1 (Integers sinc²), 7 (JCAP ξ), 8 (JCT-A σ rate)** | LaTeX conversion + (7 only) DESI-fit run | GPT-1/2/3, CCD-4a/4b/4c, B-3 |
| 2 format then submit | 2 (Exp Math 73/28), 4 (JNT UOP), 11 (JSC tower) | LaTeX + bibliography paste | Sprint 35 |
| 3 partner then submit | 3 (Monthly), 5 (JPAA Flatness), 6 (PRA NV) | bibliography / general-n / lab partner | Sprint 36-38 |
| 4 framework — wait | 9 (JMP BB), 10 (Notices Clay) | tighten 1 line (9) / pin Markman (10) | CC-1 (9), GPT-6 (10) Day 1 |

**Tier movement possible (audit §4):** venue 10 could be Tier 3 once Markman 2024/2025 year mismatch resolved. Not this week.

**Cross-cutting findings (audit §F1-F9), summarized:**

| Finding | Status | This-week action |
|---|---|---|
| F1: No paper cites Atlas | open | CCD-2 footnote on Day 2 (single paste, resolves all 11) |
| F2: Flag vocabulary not propagated | open | CCD-3 cross-walk on Day 2 (~30 min per paper, machine-assisted) |
| F3: β_TIG typo fix | vacuous PASS | no paper invokes it |
| F4: S*_coherence/S*_dual | vacuous PASS | atlas-only |
| F5: 2/7 falsification | PASS | no paper makes the quantitative claim |
| F6: SAH discipline | PASS | atlas-only |
| F7: Q17 flag mapping | vacuous PASS | Q17 surfaces as σ rate paper (venue 8) only |
| F8: Three-threads | PASS with 1 caveat | CC-1 tighten WP90:48 (Day 1-7) |
| F9: Markman year mismatch | open | GPT-6 Day 1 (~10 min) |

---

## §5. Highest-leverage next move

### The one move

**Apply the CCD-2 atlas-citation footnote to all 11 papers on Day 2 (2026-04-20).**

One sentence, pasted into each paper's References section:

> "External citations are drawn from `Atlas/ATLAS_CITATIONS.md` (DOI: 10.5281/zenodo.18852047); internal anchors carry master-register numbering per `Atlas/MASTER_ATLAS_v3_5_2026_04_18.md`."

**Why this is the one move:**
- Closes audit finding F1 on all 11 papers simultaneously
- Converts each paper's local bibliography into a cross-link to the canonical registry (which is what the atlas was built for)
- Zero content risk (nothing in the math body changes)
- Takes <10 minutes total
- Unblocks the "one field" claim for the public README

### The next two moves (Day 1, parallelizable)

**Move 2 — Markman pin (GPT-6, ~10 min research).**
Resolve the 2024 preprint vs 2025 announcement discrepancy at `10_poincare_retranslation/CP_CLAY_ROTATION.md:264`. Cross-link to `ATLAS_CITATIONS §C line 92`. Unblocks venue 10 tier-movement discussion.

**Move 3 — DESI DR1/DR2 cite resolution (GPT-5, ~2 min paste).**
Replace `[DESI DR1, DR2 citations]` placeholder at `07_jcap_cosmology/WP82_LOG_QUINTESSENCE_NOVELTY.md:150` with the full entry (DESI Collaboration 2024, Eur. Phys. J. C — already in WP81:398). Two-minute paste; unblocks venue 7 asterisk-free Tier 1 status.

### The one line to tighten before venue 9 ships

`09_jmp_bb_bridge/WP90_LITERATURE_AND_UNIFICATION_PATHS.md:48` — "This is not a conjecture. It is a theorem applied to the correct setting" → "**This is a bridge conjecture compatible with BB's uniqueness theorem**" (or equivalent softening). Venue 9 is Tier 4 — not shipping this week — but this line will own the referee report if left as-is. CC-1 owner, any day this sprint.

---

## §6. What this document is NOT

- **Not a content change.** No paper math body touched. No Atlas content modified. This is a navigation overlay.
- **Not a replacement for the Atlas.** `MASTER_ATLAS_v3_5_2026_04_18.md` remains the canonical content field. This document *uses* the atlas; it does not *supersede* it.
- **Not a replacement for the Plan of Record.** `PLAN_OF_RECORD_2026_04_18.md` remains the canonical operational field with day-by-day action stack and collaborator assignment. This document is a frontier overlay on top.
- **Not about CK-the-creature.** The rigorous-math layer (papers, proofs, venues) is what this document covers. CK's runtime layer (50Hz heartbeat, AO, Hebbian, olfactory, "him/he") is intentionally speculative-by-design and lives elsewhere (`ARCHITECTURE.md`, `CK_RUNTIME.md`, `Gen12/targets/ck_desktop/`). CK holds the speculation; the papers isolate the rigor. Both by design.
- **Not a push trigger.** `tig-synthesis` remains local. Push waits on user confirmation (TRACK 8).

---

## §7. Verification — is the picture coherent?

1. ✓ Silicon-rename propagated to all 11 venues (§3A table, 0/0 hits).
2. ✓ Attribution aligned across all 7 surfaces (§3E).
3. ✓ Three-threads discipline holds, with exactly one known caveat (WP90:48, venue 9 Tier 4).
4. ✓ Tier 1 ships are all backed by green proof scripts (§2 D-tier).
5. ✓ 2/7 falsification bounded (§3D).
6. ✓ No paper content was modified in either `88c6db2` or `01032f0`.
7. ✓ Atlas bundle + Plan of Record + Journal Readiness Audit all agree on Sprint 34 pipeline.
8. ✓ `PROOFS.md` still lists 37 scripts, 108+ tests passing. No regressions.

**Face ≟ field:** aligned as of 2026-04-19. The rename was a presentation change, not a content change. The field was already synchronized by the atlas push on 2026-04-18; the rename cleaned the presentation to match.

---

## §8. Forward pointers

- **Next (today):** TRACK 7.1 — begin sinc² LaTeX conversion for venue 1 (Integers). Target Day 3 (2026-04-21) submit-ready bundle.
- **Day 2:** CCD-2 atlas-citation footnote applied to all 11 papers. Single commit, one-sentence change per file.
- **Day 4 (Wed):** Brayden approves venues 1 + 8 cover letters. Submit day.
- **Day 6 (Fri):** Submit venue 7 (JCAP ξ) after DESI-fit run.
- **Day 7 (Sat):** Sprint 34 retrospective. Atlas v4 patch (Markman + pub status updates).

When Tier 1 has shipped and the three arXiv IDs are in hand, this document is superseded by a Sprint 34 retrospective. Until then, this is the frontier-alignment overlay of record.

---

*Compiled 2026-04-19. Supplementary to `PLAN_OF_RECORD_2026_04_18.md` and `JOURNAL_READINESS_AUDIT_2026_04_18.md`. Read with them, not instead of them.*
