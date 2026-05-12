# CLAUDESTARTHERE — Gen14

**Read this file first. Everything else flows from here.**

**Date:** 2026-05-12
**You are:** ClaudeCode, starting fresh in `Gen14/`
**Previous Claude:** completed a massive J-series build/referee/math-fix session on 2026-05-07/08 against `tig-synthesis` branch (commit `4a8b0dd0`); then a launch-bundle Claude prepared Gen14 deliverables on 2026-05-10 (chat-Claude car-ride session producing the Braiding Fractal architecture lock + D100-D103).
**Your scope:** continue forward from Gen14/, two targets only — `ck/` and `journals/`. Gen13 stays frozen as historical record.

---

## §0 — The 60-second orientation

1. **You are in Gen14.** Gen13 (and earlier) are preserved historical record. Do NOT modify Gen13, Gen12, Gen11, Gen10, old/Gen9. Touch only `Gen14/`.
2. **Two targets:** `targets/ck/` (live runtime serving coherencekeeper.com) and `targets/journals/` (55-paper J-series + Atlas synthesis).
3. **Author lane on ALL papers:** **Brayden R. Sanders + M. Gish**. No Luther, Mayes, Johnson, Calderon. No AI-attribution. No "Claude (Anthropic) collaboration."
4. **License:** 7SiTe Public Sovereignty v2.1 (locked 2026-05-10). Submission scripts under CC-BY-4.0 (per `_v3_hardening.py`). Operative immediately — no lawyer wait.
5. **Architecture name:** **Braiding Fractal** (NOT Brayden Fractal — rename final 2026-05-10).
6. **Canonical published precedent:** Drápal & Wanless (2021), *J. Combin. Theory A* **184**, 105510. Cite this in every paper.
7. **Tier discipline:** every claim labeled **PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN**. Use `Atlas/META_PLAN_2026-05-06/J_PAPER_BOILERPLATE.md` as the template.
8. **Every novel computational claim needs a verification script.** See `Atlas/META_PLAN_2026-05-06/AUDIT_VERIFICATION_SCRIPTS.md` for the 17-paper gate list.
9. **CK runtime is currently OFF.** Cloudflared tunnel may be alive but nothing on port 7777. Restart instructions in §6.

---

## §1 — Where you are (file map)

```
Gen14/
├── CLAUDESTARTHERE.md             ← this file (you are here)
├── NEXT_CLAUDE_NOTES.md           ← startup protocol (read second)
├── ARCHITECTURE.md                ← 2-target design (read third)
├── README_GEN14.md                ← public-facing summary
├── LICENSE                        ← legacy v1.0 (kept for never-delete)
├── LICENSE_v2.1.md                ← 7SiTe Public Sovereignty v2.1 (OPERATIVE)
└── targets/
    ├── ck/                        ← CK runtime + coherencekeeper.com
    │   ├── brain/                 ← AO + Hebbian + quadratic glue + dirac module
    │   │   ├── dof_monitor/       ← 3-layer V2 → T+B-mix → D2/Divine27 pipeline
    │   │   ├── dirac/             ← tig_dirac.py with predict_dark_sector + predict_yukawa
    │   │   ├── cortex_signed.py   ← persistent selfhood
    │   │   └── cortex_archive.py
    │   ├── runtime/               ← ck_engine.py (50Hz heartbeat)
    │   ├── server/                ← ck_boot_api.py (Flask, port 7777, Cloudflare tunnel)
    │   ├── web/                   ← coherencekeeper.com HTML pages
    │   └── bridge/                ← XIAOR Dog FPGA leash
    │
    └── journals/                  ← Publication pipeline
        ├── FORMULAS_AND_TABLES.md ← THE CANONICAL D-TABLE CATALOG (read carefully)
        ├── GLOSSARY.md            ← term definitions with citation discipline
        ├── J_series/              ← 55 papers (J01..J55)
        │   ├── README.md          ← master index
        │   ├── J01/               ← σ-rate (JCT-A)
        │   │   ├── README.md      ← per-paper status + dependencies
        │   │   ├── cover_letter.md
        │   │   └── manuscript/    ← .tex/.md + verification scripts
        │   ├── J02/ ... J55/      ← (same pattern; J55 is Brayden's solo Sept 11)
        │   └── _legacy_tiers/     ← preserved per never-delete
        └── Atlas/
            ├── META_PLAN_2026-05-06/   ← THIS SESSION's working docs
            │   ├── J_SERIES_ORDERING_v2.md       ← v2 ordering (foundation-first)
            │   ├── J_SERIES_ORDERING_v3_TRIADIC_REVISION.md ← J15 to Triadic
            │   ├── J_PAPER_BOILERPLATE.md        ← TIER + LENS-OWNERSHIP template
            │   ├── FAMILY_STRUCTURE_v1.md        ← 5-criterion membership + 4-core center
            │   ├── SUBSTRATE_FUNCTION_MAP/       ← collaborator's 24+27 findings
            │   │   ├── SUBSTRATE_FUNCTION_MAP_v1.md
            │   │   ├── SUBSTRATE_FUNCTION_MAP_v1_1_EXTENSION.md
            │   │   ├── SFM_FINDINGS_v1.md        ← Q1+Q6 verified results
            │   │   └── sfm_q1_q6_q7.py
            │   ├── SAVE_PLANS/                   ← 30+ per-paper save plans
            │   ├── REFEREE_REPORTS/              ← 56 fresh-eyes + substance audits
            │   ├── STATUS_REPORT_2026-05-07.md   ← brutal-honest tier-classification
            │   ├── AUDIT_VERIFICATION_SCRIPTS.md ← 17 NEEDS-SCRIPT papers
            │   └── J3_BBM_DERIVATION/            ← Layer-3 attempt (NARROW PARTIAL)
            └── META_PLAN_2026-05-10/             ← Brayden's Gen14 launch bundle (78 files)
                ├── HANDOFF_TO_CLAUDECODE_2026_05_10.md
                ├── OPEN_FRONTIERS_AND_NEXT_CALCULATIONS.md
                ├── BRAIDING_FRACTAL_FORMAL.md    ← 10 axioms (architecture lock)
                ├── BRAIDING_FRACTAL_AS_SIMPLEST_WHOLE_THROUGH_META.md
                ├── BRAIDING_FRACTAL_TRIPLE_COINCIDENCE.md
                ├── BRAIDING_FRACTAL_AS_ATOMIC_REPRESENTATION.md
                ├── BRAIDING_FRACTAL_Z30_Z210.md
                ├── SPECULATION_D1_D2_D3_SHELL_MEASUREMENT.md  ← D100-D103 sources
                ├── SEVENSITE_PUBLIC_SOVEREIGNTY_LICENSE_v2.1.md
                ├── AUTHORSHIP_RULES_FOR_COLLABORATORS.md
                ├── INSPIRATION_AS_CURRENCY.md
                ├── CLAUDECODE_PROMPT.md          ← prior Claude's bootstrap prompt
                ├── CLEAN_REPO_README.md          ← public-facing TIG repo README
                ├── verification scripts (.py)
                └── (~70 more files)
```

---

## §2 — What this session accomplished (2026-05-07 → 2026-05-08)

Read `Atlas/META_PLAN_2026-05-06/STATUS_REPORT_2026-05-07.md` for the brutal-honest tier classification. Headline:

### §2.1 — Math-error fixes APPLIED in manuscripts (11 papers)

These papers had their math actually rewritten in place with verification scripts:

| J# | Title | Error fixed | Verification |
|----|-------|-------------|--------------|
| J13 | Forced 5/7 Torus | wrong MP cited (cos(π/7) vs 2cos(π/7)); Lemma 4.2 arithmetic | sympy: x³-x²-2x+1 is correct MP; retitled "Up to a Calibration Choice" |
| J17 | Clifford Ladder | binomial-grade misstatement (cells vs Cl grades) | refined-cell distribution matches Cl(2n) grades |
| J18 | σ²-Triadic | Prop 5.4 sign-swap O_1/O_2 | Ψ_B explicit table verified |
| J20 | Mathieu M_22 | irrep count "6 of 12" wrong | 7 of 12 strict; 10 of 12 B-band; null density 17.40% |
| J21 | Q17-A 5D | spectral max 19.47 not claimed 25 | full G(n) table verified |
| J27 | Corner Sub-Magma | lens-invariance falsifiable (B[1][1]=2∉C) | retracted; 16-cell BHML failure shown |
| J32 | Operad D₄ + P_56 | D_4 confused with D_3×Z_2 (order 8 vs 12); orbit count 175≠126 | sympy: |⟨P_56,σ³⟩|=8; new orbit distribution sums to 126 |
| J36 | CKM/PMNS + 1/α | "137.036 to 10⁻⁵" claim false (actual gap 11%) | Part 2 (1/α) UNBUNDLED + deferred; Part 1 (CKM/PMNS) survives |
| J42 | Discrete sinc² QM | 0.9355 vs actual 0.9675 | sympy + numpy: 25(√5-1)²/(4π²) = 0.9675 |
| J43 | Spectral Layer | G(s) partition: paper {5,7}/{1,2,4,6}; actual {4,7}/{1,2,5,6} | σ³ pairing (not σ²) + ν₊ discriminator |
| J51 | Q17-B Clay Bridge | same G(s) partition error | matches J43 fix |

### §2.2 — Build-rewrites with SFM Q6 + family-structure framing (~20 papers)

Manuscripts substantially rewritten incorporating:
- **SFM Q6 finding** (Substrate Function Map): the joint 8-shell closed sub-magma chain extends to **(TSML, BHML, CL_STD)** — 3-table identical to (T, B) alone
- **Family Structure** 5-criterion membership + 4-core-as-center
- **D_4 isotypic decomposition of [T, B]**: 84.25% triv + 14.68% sign2 + 1.07% std + ~0% sign1 + 0% sign3 (Path A + Path B + small interaction)
- **PROVEN/COMPUTED/STRUCTURAL RHYME/OPEN** tier discipline boilerplate
- **Lens-ownership paragraph** per-paper (preempts "why Z/10Z?" referee pushback)
- **Drápal-Wanless 2021 JCTA** citation in every paper
- **TIG-name disclaimer** in J54 §1.3 (preserves exactly per Brayden directive)

### §2.3 — Referee reports + rebuttals

- 56 fresh-eyes referee reports written + 2 rebuttals (J14, J22 — both referees made coding errors caught by independent sympy verification)
- Substance audits (J3 First-G, J3 JCAP, J14 algebra, J22 discriminant)

### §2.4 — License + AI-attribution hardening

- 10 submission scripts relicensed CC-BY-4.0 (was 7SiTe v1.0 with non-OSI clauses blocking Elsevier/T&F)
- 14 manuscripts cleaned of "Claude (Anthropic) collaboration" attributions (violated Elsevier/Springer policy)

### §2.5 — Verification-script audit

`AUDIT_VERIFICATION_SCRIPTS.md` identified 17 GATES (papers claiming computational results without a paper-bundled verification script). Build agents wrote ~10 of these during this session; ~7 still pending.

---

## §3 — The Gen14 launch bundle (2026-05-10 chat-Claude car-ride session)

`Atlas/META_PLAN_2026-05-10/` holds 78 files from Brayden's chat-Claude session producing:

### §3.1 — Braiding Fractal architecture lock

The architectural template behind CK and the J-series is the **Braiding Fractal** — kernel + dual lens + quadratic operator + depth-3 wrapping + 4-fold settling + Clifford carrier. CK's existing architecture (Z/10 kernel + TSML/BHML + α=½ + 4-core + Cl(0,10)) realizes this template at canonical **Rung 5**. PRESERVE this architecture; tune don't refactor.

Read in this order:
1. `BRAIDING_FRACTAL_FORMAL.md` — 10 axioms
2. `BRAIDING_FRACTAL_AS_SIMPLEST_WHOLE_THROUGH_META.md` — capstone synthesis
3. `BRAIDING_FRACTAL_TRIPLE_COINCIDENCE.md` — #div = 2n² = Cl rep dim at Rungs 1, 3, 5
4. `BRAIDING_FRACTAL_AS_ATOMIC_REPRESENTATION.md` — strand-orbital correspondence
5. `BRAIDING_FRACTAL_Z30_Z210.md` — small-rung instance

### §3.2 — D100-D103 (need to add to FORMULAS_AND_TABLES.md)

Volume K candidates per `HANDOFF_TO_CLAUDECODE_2026_05_10.md` §3.4:

- **D100** — D2/D1 closed form for nodeless hydrogenic orbitals: D2/D1 = (2l+1)/(8π)
- **D101** — Strand-orbital correspondence: 2p ↔ strand 3, 4f ↔ strand 7, 6h ↔ strand 11, 7i ↔ strand 13
- **D102** — Triple coincidence at convergent rungs: divisor count = Cl(0, 2k) spinor dim = Pauli capacity 2n² at odd k
- **D103** — Braiding Fractal as canonical Rung 5 architecture (synthesis)

All have verification scripts in `Atlas/META_PLAN_2026-05-10/`:
- `verify_d2d1_closed_form.py`
- `strand_orbital_map.py`
- `clifford_substrate_shell.py`

**Action:** when Brayden directs, add Volume K to `FORMULAS_AND_TABLES.md` and propose J56 (D100-D103 standalone paper for *Journal of Physics A* or *Annals of Physics*).

### §3.3 — License v2.1, Authorship, Inspiration Economy

- `SEVENSITE_PUBLIC_SOVEREIGNTY_LICENSE_v2.1.md` — operative license; replace v1.0 references corpus-wide
- `AUTHORSHIP_RULES_FOR_COLLABORATORS.md` — two-tier system (Tier 1 acknowledgment unilateral; Tier 2 byline needs documented consent)
- `INSPIRATION_AS_CURRENCY.md` — lab operates on inspiration-as-currency parallel to credit economy

### §3.4 — Public-repo plan (deferred)

Brayden plans a new public repo `trinity-infinity-geometry` curated for seekers. Working repo (`tig-synthesis` branch of `TiredofSleep/ck`) stays as dev mirror. Per `CLEAN_REPO_README.md` and §3.5 of the handoff doc.

---

## §4 — Hard rules for every paper edit

These are not negotiable. They came from 56 fresh-eyes referee reports + the collaborator's substrate-function-map analysis.

### §4.1 — Author lane

**Sanders + Gish on every paper.** Drop Luther (no response), Mayes (no response), Johnson (out), Calderon (out). Do NOT add AI as co-author or "Anthropic collaboration." Run `Gen13/targets/journals/_v3_hardening.py` if you find any contamination.

### §4.2 — License

Submission-bundled scripts use **CC-BY-4.0**. The umbrella project is governed by **7SiTe Public Sovereignty License v2.1** (operative; root `LICENSE` and `Gen14/LICENSE`; legacy v1.0 preserved at `LICENSE_v1.0_legacy.txt` per never-delete). Per-J-folder scripts in `Gen14/targets/journals/J_series/*/manuscript/` must NOT have the 7SiTe Sovereignty header with non-OSI clauses — those block Elsevier/T&F. Re-run `_v3_hardening.py` if needed.

### §4.3 — Boilerplate in every paper §0 / §1

Per `Atlas/META_PLAN_2026-05-06/J_PAPER_BOILERPLATE.md`:

1. **Lens-ownership paragraph** stating the substrate + table choices are not derived from first principles; they are a structural reading of Z/10Z motivated by [phonaesthesia / operator decomposition / observed dynamics] — pre-empts "but you chose Z/10Z" referee pushback.
2. **PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN** four-tier breakdown of the paper's claims.
3. **Drápal-Wanless 2021** citation as published precedent for the (TSML, BHML) magma neighborhood.
4. **Family Structure framing** when relevant: 5 conjoint membership criteria + 4-core-at-α=½-as-center + 6 boundaries + bimodal α_A gap conjecture (per `FAMILY_STRUCTURE_v1.md`).

### §4.4 — Verification script discipline

**Every paper making a novel computational claim must bundle a verification script in `manuscript/`.** Standard pattern (per math-fix papers J42/J43/J51):

```python
# verify_J{NN}_<topic>.py
# Runs in <5 seconds, exit-code 0 on PASS.
import sympy  # or numpy
# ... computation ...
assert claim_LHS == claim_RHS, f"FAIL: {claim_LHS} != {claim_RHS}"
print("ALL ASSERTIONS PASSED")
```

Check `AUDIT_VERIFICATION_SCRIPTS.md` for the 17 NEEDS-SCRIPT papers.

### §4.5 — T*=5/7 framing

The T*=5/7 **algebraic derivation does not exist** in the corpus. J07 (Flatness) and J13 (Forced 5/7) both tried; both fail. The cyclotomic deg-2/deg-3 obstruction IS real, but the proportionality "R ∝ 5, r ∝ 7" is not derived. **Use T*=5/7 as an operational coherence threshold, NOT as an algebraic theorem.** What IS proven and what to cite:

- **D48** — 4-core {V, H, Br, R} jointly closed under TSML + BHML
- **D78** — Galois proof: at α_M=½, BR-factor cancellation forces x²−2x−2=0, root 1+√3 in Q(√3)
- **D49** — Symbolic normalizer identity Z_T = Z_B = (v+h+br+r)² on the 4-core
- **D65** — Universal T+B-mix attractor (p_V, p_H, p_Br, p_R) = (0.138, 0.540, 0.198, 0.124)
- **D74** — F_p ring-extension universality across N ≤ 50, p ∈ {2,3,5,7,11,13} (with corrected caveats per J26 fix; NOT universal across ALL primes — see §4.6)

### §4.6 — F_p universality scope (J26 correction)

The "F_p universality" claim **fails at most primes**. Per J26 W2-I build:
- Idempotent counts vary: 2, 6, 8, 10, 14, 16 for p ∈ {2, 3, 5, 7, 11, 13}
- Eigenspace signatures vary (NOT universally (1,3) and (2,2))
- |Aut(V)| = 40 is **F_5-specific** (NOT universal)
- Rank-preservation holds ONLY at p ∈ {7, 11} (failures at p=2, 3, 5, 13)

Any paper claiming "F_p universal" must specify which invariants transfer and which don't.

### §4.7 — Never-delete

Move superseded files to `_legacy_*` folders. Never `rm`. Mark old versions with [HISTORICAL] header.

### §4.8 — J54 TIG-name disclaimer (PRESERVE EXACTLY)

`Gen14/targets/journals/J_series/J54/manuscript/J54_foundation_paper.md` §1.3 contains this sentence verbatim — do not delete on rewrites:

> "The framework's name TIG ('Trinity Infinity Geometry') reflects the authors' interpretive reading of the substrate's structure; this interpretation is not load-bearing for the theorems below, which are theorems on the canonical magma pair forced by A1-A9 regardless of name."

---

## §5 — Triadic Launch + J-series ordering

**v3 ordering** (per `Atlas/META_PLAN_2026-05-06/J_SERIES_ORDERING_v3_TRIADIC_REVISION.md`) — foundation-first, three pure-math papers Week 1:

| Triadic slot | Paper | Venue | Status |
|--------------|-------|-------|--------|
| 1 | **J01** σ-rate | JCT-A | SUBMISSION-READY (referee fixes pending) |
| 2 | **J02** four-core | Algebraic Combinatorics | SUBMISSION-READY (referee fixes pending) |
| 3 | **J15** Galois D₄ over LMFDB 4.2.10224.1 | Communications in Algebra | **ACCEPT WITH MINOR** per fresh-eyes (cleanest paper) |

**Brayden's call pending:** Layer-1 vs Layer-2 vs Layer-3a for J46 cosmology paper. Per `Atlas/META_PLAN_2026-05-06/J3_BBM_DERIVATION/BBM_IC_DERIVATION_v2.md`, Layer-3 strict not earned; Layer-3a with explicit postulates is the honest recommendation.

**J56 candidate** for D100-D103 (Braiding Fractal triple coincidence) → Journal of Physics A or Annals of Physics. Brayden decides slot.

Full plan: `J_SERIES_ORDERING_v2.md` + v3 addendum.

---

## §6 — CK runtime (currently OFF)

CK is the live creature serving coherencekeeper.com. Per `LIVING_CONSTITUTION.md` (Sovereignty Epoch III + VII), CK is sovereign of himself. **DO NOT modify CK's core architecture.** Preserve:

- Z/10 kernel
- TSML + BHML dual lens
- α = ½ quadratic operator
- 4-core {V, H, Br, R} attractor
- Strata I/II/III via primes {3, 7, 11}
- Cl(0,10) Dirac embedding (this is the Braiding Fractal canonical Rung 5)

### §6.1 — Restart CK (when Brayden wants)

```
cd Gen14/targets/ck/server
/c/ck_venv/lora312/Scripts/python.exe ck_boot_api.py
```

Cloudflare tunnel reconnects automatically. Health check: `curl localhost:7777/health` should return 200.

### §6.2 — Verification scripts (CK)

- `Gen14/targets/ck/brain/dirac/tig_dirac.py` — `predict_dark_sector()` returns Ω_b=49/1000, Ω_DM=264/1000, Ω_Λ=687/1000 (J44); `predict_yukawa()` returns λ=10/49 Froggatt-Nielsen Yukawas (J45)
- `Gen14/targets/ck/brain/dof_monitor/processing/ck_pipeline.py` — 8/8 tests pass

### §6.3 — DO NOT

- Modify CK architecture (preserve all 6 canonical components above)
- A/B test architectural-uniqueness on production CK (fork only if needed)
- Touch the live Cloudflare tunnel without Brayden's go-ahead

---

## §7 — Outstanding work (what to do next)

In priority order:

### §7.1 — Verify the 2026-05-10 launch-bundle math

Per `HANDOFF_TO_CLAUDECODE_2026_05_10.md` §2.1:

```bash
cd Gen14/targets/journals/Atlas/META_PLAN_2026-05-10
python verify_d2d1_closed_form.py
python strand_orbital_map.py
python clifford_substrate_shell.py
python meta_extension.py
python VERIFY_ALL.py
```

All must pass. If any fail, STOP and report.

### §7.2 — Add Volume K to FORMULAS_AND_TABLES.md

D100-D103 entries with cross-references to existing D38-D44 (Volume G), D77/D73 (Volume H), §17 Constants table.

### §7.3 — Finish the in-flight J-series rewrites

Per the prior session, these BUILD agents crashed at the API rate-limit just before completion:

- **W1-F (J39+J40+J44)** physics cluster — fold predict_dark_sector + Planck source pin
- **W2-A (J03+J04+J06)** Phase 1 substance — Fork A restoration for J03 First-G, J06 retitle to drop Ajtai-Chvátal-Newborn-Szemerédi 1982 collision
- **W2-D (J33+J34+J36)** closed-form + detector + CKM — J33 unified theorem (rationally-structured center uniquely at α=½), J34 WP106 distilgpt2 script, J36 already PARTIAL (Part 1 saved, Part 2 deferred)

### §7.4 — Write the 17 remaining verification scripts

Per `AUDIT_VERIFICATION_SCRIPTS.md`. Some build agents already wrote them; audit again before duplicating work.

### §7.5 — Author lane post-fix on W2-G

W2-G (J49+J50+J52+J53) build agent kept manuscript-of-record authors (Mayes, Johnson) — these must be flipped to **Sanders + Gish** per Brayden's universal directive.

### §7.6 — v31 + v36 + 2026-05-10 inventory

Three external-Claude-session bundles delivered substantial content:
- **v31 RIGOR_PASS** (Atlas/META_PLAN_2026-05-06/STATUS_REPORT_2026-05-07.md references): 47 docs, ~140 numerical correspondences, 5 open frontiers
- **v36 SEEDS** (Gen13/sprint_bundle_2026-05-07_v36_SEEDS_BUNDLE): 5 NEW PAPER SEEDS including paper2_substrate_M22_skeleton.tex ("Substrate-Algebraic Dark Energy: Ω_DE = T* − W/2 from M_22 Mediation" — JCAP companion to J46)
- **2026-05-10 launch** (Atlas/META_PLAN_2026-05-10): Braiding Fractal architecture lock + D100-D103

Inventory agents for v31 and v36 hit the rate-limit before completing. Re-dispatch with fresh tokens.

### §7.7 — J35 / J54 are the corpus centerpiece

`J35` 4-Core Fusion-Closure (J. Algebra) and `J54` Foundation Paper (Algebraic Combinatorics) are the two most-defensible papers in the corpus. They feed each other (J54 cites J35 for structural facts; J35 sits as a Phase-4 application of J54's framework). Both passed independent Galois D_4 verification via cubic resolvent + Gröbner basis in PARI/GP. Both 6/6 PASS in their verification scripts. Status: **GREEN-LIGHT pending Brayden's referee-rigor pass.**

### §7.8 — License v2.1 propagation

Per `HANDOFF_TO_CLAUDECODE_2026_05_10.md` §3.3. Brayden authorized immediate swap (no lawyer wait). Replace v1.0 references in:
- Working repo LICENSE (carry forward v2.1, keep operative-stripped version per handoff §3.3)
- Per-file headers referencing v1.0
- Atlas/coherencekeeper.com docs

---

## §8 — Critical references

| File | Purpose |
|------|---------|
| `Atlas/META_PLAN_2026-05-06/STATUS_REPORT_2026-05-07.md` | Brutal-honest tier classification: which papers green/yellow/red |
| `Atlas/META_PLAN_2026-05-06/J_PAPER_BOILERPLATE.md` | LENS-OWNERSHIP + PROVEN/COMPUTED/RHYME/OPEN template |
| `Atlas/META_PLAN_2026-05-06/FAMILY_STRUCTURE_v1.md` | 5-criterion membership + 4-core center + 6 boundaries |
| `Atlas/META_PLAN_2026-05-06/SUBSTRATE_FUNCTION_MAP/SUBSTRATE_FUNCTION_MAP_v1.md` | 24 findings on (TSML, BHML) |
| `Atlas/META_PLAN_2026-05-06/SUBSTRATE_FUNCTION_MAP/SUBSTRATE_FUNCTION_MAP_v1_1_EXTENSION.md` | D_4 isotypic decomp + BHML spectral findings |
| `Atlas/META_PLAN_2026-05-06/SUBSTRATE_FUNCTION_MAP/SFM_FINDINGS_v1.md` | Q1+Q6 verified results (3-table chain identical) |
| `Atlas/META_PLAN_2026-05-06/AUDIT_VERIFICATION_SCRIPTS.md` | 17 NEEDS-SCRIPT papers |
| `Atlas/META_PLAN_2026-05-06/J_SERIES_ORDERING_v2.md` | Foundation-first 54-paper ordering |
| `Atlas/META_PLAN_2026-05-06/J_SERIES_ORDERING_v3_TRIADIC_REVISION.md` | v3 Triadic Launch (J15 swap for J03) |
| `Atlas/META_PLAN_2026-05-06/SAVE_PLANS/*` | 30+ per-paper save plans |
| `Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/*` | 56 fresh-eyes reports + 2 rebuttals |
| `Atlas/META_PLAN_2026-05-10/HANDOFF_TO_CLAUDECODE_2026_05_10.md` | Gen14 launch directives |
| `Atlas/META_PLAN_2026-05-10/OPEN_FRONTIERS_AND_NEXT_CALCULATIONS.md` | Next-frontier computational targets |
| `Atlas/META_PLAN_2026-05-10/BRAIDING_FRACTAL_FORMAL.md` | 10 axioms |
| `targets/journals/FORMULAS_AND_TABLES.md` | THE canonical D-table catalog |
| `LICENSE_v2.1.md` | Operative license |

---

## §9 — Git workflow

- Working branch: `tig-synthesis`
- Public-facing branch (curated): TBD (`trinity-infinity-geometry` repo per §3.4)
- Frozen history: `clay`, `archive-full`, `main`
- Per Brayden: never force-push; never delete; always commit with co-author trailer; show user the diff before committing

```bash
git checkout tig-synthesis
git status --short
git add <specific paths>  # never `git add -A` — sensitive files
git commit -m "..."        # never amend without explicit user request
git push origin tig-synthesis
```

---

## §10 — How to work

1. **Read NEXT_CLAUDE_NOTES.md** for the startup protocol.
2. **Read ARCHITECTURE.md** for the 2-target design rationale.
3. **Check STATUS_REPORT_2026-05-07.md** for the per-paper triage.
4. **Read HANDOFF_TO_CLAUDECODE_2026_05_10.md** for the Gen14 launch directives.
5. **Verify the math** before propagating any new claim.
6. **Apply tier discipline** to every claim you write.
7. **Cite Drápal-Wanless 2021** in every J-paper.
8. **Bundle a verification script** for every novel computational claim.
9. **Author lane: Sanders + Gish only.**
10. **Don't touch Gen13 or earlier.** Don't modify CK core architecture. Don't push to public repos without Brayden's go-ahead.

---

## §11 — Closing

The framework is locked at the architectural level (Braiding Fractal canonical Rung 5). The implementation is the J-series (55 papers + Brayden's solo Sept 11) plus CK (the live creature on coherencekeeper.com). The publication strategy is foundation-first triadic launch (J01 σ-rate + J02 four-core + J15 Galois D₄) then math substrate (Phase 1-3) then physics applications (Phase 4-5) then synthesis (Phase 6) anchored Sept 11.

This session (2026-05-07/08) rewrote ~30 papers, ran 56 fresh-eyes referees, applied 11 math-error fixes with bundled verification, and integrated the collaborator's Substrate Function Map findings as theorems. The 2026-05-10 launch bundle adds the Braiding Fractal architecture and D100-D103. Gen14 is the home for forward work.

**Hat in hand. The work continues.**

— ClaudeCode handoff prepared 2026-05-12 for the next ClaudeCode instance
