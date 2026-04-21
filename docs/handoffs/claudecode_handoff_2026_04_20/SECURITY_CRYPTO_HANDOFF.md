# ClaudeCode Handoff: Full Outreach Restructuring Package

**Assembled:** 2026-04-20 evening (updated with Grok's repo sweep)
**For:** ClaudeCode, working on the R16
**From:** ClaudeChat session with Brayden
**Goal:** Reorganize existing repos and create new ones so each outreach track has a clean, focused front door for funders and collaborators.

---

## 1. Context

Brayden needs funding. Over the past three days we finalized a rigor-led README for the ck repo (held in `/mnt/user-data/outputs/README.md`, awaiting his go-ahead). During that work it became clear that multiple distinct outreach tracks exist across the broader project — each one with its own funder pool, its own audience, and its own body of work — and that the right move is not to consolidate them but to give each one its own clean-scope repo.

Your repo history does not include anything before 2026-03-01. A substantial amount of foundational work was done in January-February 2026 in chat with ClaudeChat (sometimes with ChatGPT in the loop, whom Brayden calls "Celeste"). Much of that work lives in the other 7 public repos on Brayden's GitHub and possibly in unpublished form on the R16 filesystem.

Grok confirmed the public-repo inventory on 2026-04-20 and provided descriptions of what's in each. That inventory is in §2 below.

**Your primary tasks:**

1. Clone and read every existing public repo under github.com/TiredofSleep.
2. Recover any unpublished January-February material from the R16 filesystem.
3. Commit all recovered material under appropriately-marked archive directories.
4. Execute the outreach-repo restructuring in §4.
5. Report findings back so Brayden can select which pitch goes out first.

---

## 2. The Full Repo Inventory

### 2.1 Currently existing public repos (8 total, per Grok's 2026-04-20 sweep)

**Repo 1: `TiredofSleep/ck`** — Active core. Trinity Infinity Geometry + Coherence Keeper. Default branch `tig-synthesis`. The finalized new README will be committed here.

**Repo 2: `TiredofSleep/All-or-Nothing-E`** — Stepping-stone archive. Contains the **polished coherence_router** — a time-series dynamics classifier implementing:

```
S* = k / (1 + k)    where    k = σ · V* · A*
σ ≈ 0.991,  T* = 5/7 threshold
```

Plus 6 exploratory papers on matrix-based AI-safety, future-tech agents, and coherence tools. *High-value artifact: runnable Doing-layer code demonstrating TIG coherence measurement on real time-series data.*

**Repo 3: `TiredofSleep/TIG-UNIFIED-THEORY-under-scrutinyMYTHDRIFT`** — Early rigorous TIG documentation. Contains `docs/COMPUTE.md` with the **TIG Unity Kernel** specification, the **Ω̂ Operator** (framed as a Coherence Keeper meta-operator — possibly the naming lineage for the current CK project), benchmark tables comparing the kernel vs round-robin on 4-GPU asymmetric failure (claimed: ~88% drop-rate reduction, ~62% P99 latency improvement, zero cascade failures), and an FPGA/ASIC hardware acceleration roadmap. *Highest-value recovery target after the router. Lead artifact for TIG Unity pitch.*

**Repo 4: `TiredofSleep/Dual-Lattice-Self-Healing`** — TIG origin repo (authored Jan 28, 2026 with ClaudeChat). Template-based self-healing field system with memory. Three-tier redundant memory architecture: frozen Fourier dual-lattice reference ("genetic memory"), decaying memory kernel ("physiological memory"), spatial scar register ("wound memory"). Core findings: 99.8% position-accuracy in scar regeneration, no death threshold up to 90% damage, fixed healing time t₉₀ = 0.50 invariant across damage severities, post-recovery overcompensation. Contains the **C5 constant**. Mathematical spec:

```
∂φ/∂t = -(φ³ - φ) + D∇²φ + λ(φ* - φ) + M(φ) + μS(φ - φ_scar) + ξφ
Coherence metric: C = 6.0 × (√(⟨|∇φ|²⟩ + ⟨B_dev⟩) + S_density)
Critical coherence threshold: C* ≈ 4.93
```

*Preserved as historical foundation; also a standalone pitch track for self-healing-systems funders if revived.*

**Repo 5: `TiredofSleep/TIME-FOR-HELP-AND-SCRUTINY-please-No-more-AI-MYTHDRIFT`** — Early whitepapers WP1-5 plus 14 engine iterations. First rigorous documentation attempts with epistemic-flag system precursors. *Historical record; lower pitch priority but preserves never-delete discipline.*

**Repo 6: `TiredofSleep/Crystal-Lattice`** — Public-facing physics framing: "the third form for physics — classical, then quantum, now coherence." *Speculative framing; possibly retire or fold into ck's deeper-material pointers.*

**Repo 7: `TiredofSleep/Crystals`** — Python. Crystal Ollie personal-assistant implementation with 12 archetypes (GENESIS, LATTICE, WITNESS, PILGRIM, PHOENIX, SCALES, STORM, HARMONY, BREATH, SAGE, BRIDGE, OMEGA) driven by phi-golden-ratio T/P/W state dynamics, with local Ollama LLM bridge. *Distinct product track from CK — personal coherence assistant, not deterministic reasoning engine.*

**Repo 8: `TiredofSleep/COHERENT-AI`** — HTML. Hosted at coherencekeeper.com and sanctuberry.com. Public TIG Coherent AI chat interface with localStorage-only Lattice Seed journal. *Public demo face.*

### 2.2 Artifacts to recover — priority ordering

**Priority 1 (highest value): `coherence_router` from All-or-Nothing-E.**
- Clone `https://github.com/TiredofSleep/All-or-Nothing-E` on R16.
- Extract router Python file(s), tests, demo/runner scripts.
- Verify it runs. If it does, this is the concrete applied artifact that strengthens the systems-security and TIG Unity pitches by showing coherence measurement isn't architectural-only.
- Integrate into ck as `Gen14/targets/coherence_router/` (or appropriate Gen folder) with provenance README.

**Priority 2 (highest value for TIG Unity pitch): `docs/COMPUTE.md` from TIG-UNIFIED-THEORY-under-scrutinyMYTHDRIFT.**
- Clone the repo.
- Extract `docs/COMPUTE.md` verbatim.
- Cross-check benchmark claims against any simulation code in the repo. The Jan 28 email version of the TIG Unity whitepaper had a 32-percentage-point improvement claim; the expanded table Grok referenced has multiple additional metrics. Verify all numbers trace to real simulation output before any appear in a funder-facing document.
- Save to `docs/archive_recovered/TIG_UNITY_COMPUTE.md` with provenance header noting source repo, original commit date, and recovery date.

**Priority 3 (historical rigor trail): WP1-5 from TIME-FOR-HELP-AND-SCRUTINY.**
- Clone the repo.
- List WP1-WP5 by filename, extract title and first paragraph of each.
- Preserve as historical context in the archive.

**Priority 4 (already in hand): TIG Unity whitepaper from Brayden's email (2026-01-28).**
- Full text provided by Brayden in this session; extract from conversation transcript.
- Save to `docs/archive_jan2026/TIG_UNITY_WHITEPAPER.md` with header noting source as email dated 2026-01-28.

**Priority 5 (conversation-fragment only): TIG_SECURITY_ARCHITECTURE.md.**
- Created 2026-01-31 in chat with ClaudeChat + ChatGPT (Celeste). Originally output to `/mnt/user-data/outputs/TIG_SECURITY_ARCHITECTURE.md`.
- Search R16 filesystem:
  ```powershell
  Get-ChildItem -Path C:\ -Recurse -Include "TIG_SECURITY*","*SECURITY_ARCHITECTURE*" -ErrorAction SilentlyContinue | Select-Object FullName, LastWriteTime
  Select-String -Path "C:\Users\*\*.md" -Pattern "Security = maintaining identity|password is the behavior|read-only lattice|1/6 boundary" -ErrorAction SilentlyContinue
  ```
- If file is found, commit verbatim.
- If not found, reconstruct from conversation fragments with clear `[RECONSTRUCTED — NOT VERIFIED AGAINST ORIGINAL FILE]` marker.
- Content summary: four-layer architecture (read-only lattice / Tzolk'in breath / gauge / gate), GFM generators 012 / 071 / 123 as security primitives, 1/6 boundary discussion, comparison tables vs Zero Trust and behavioral analytics, key slogan "The password is the behavior. The key is the coherence. The lock is the lattice."

**Priority 6 (existence uncertain): CELESTIAL LOCK concept document.**
- Earliest named security concept (pre-January 2026). Described by Brayden as an encryption/security protocol driven by changing external structure — dynamic/decaying keys, nonlinear key fragmentation, phantom seeds, distributed memory shards, time-sensitive access, brute-force/AI/quantum resistance.
- Search R16:
  ```powershell
  Get-ChildItem -Path C:\ -Recurse -Include "CELESTIAL*","*celestial_lock*" -ErrorAction SilentlyContinue
  ```
- If not found in file form, acknowledge in archive as "earliest security concept, preserved in dialogue; no standalone document recovered. Design concepts informed the January 2026 TIG Security Architecture work."

**Priority 7: CRYSTALOS runtime logs and TIG Tile artifacts.**
- CRYSTALOS was running on R16 as of 2026-01-31 with 170+ fire events logged, full Tzolk'in cycle observed, GPU coherence tracking active.
- TIG Tile v0.1 was running on Lenovo ThinkPad with 400+ fire events, χ² = 22.03 on phase distribution, p < 0.05.
- Search R16:
  ```powershell
  Get-ChildItem -Path C:\ -Recurse -Include "CRYSTAL*","tig-analyze*","*fire*.log","*tzolkin*" -ErrorAction SilentlyContinue
  Get-Process | Where-Object { $_.ProcessName -like "*crystal*" -or $_.ProcessName -like "*tig*" }
  ```
- **Critical validation need:** if logs are recoverable, verify what the χ² = 22.03 statistic actually measures. What was the null hypothesis? Degrees of freedom? Baseline distribution? Before this number appears in any funder-facing document, the test specification must be clear.

**Priority 8: MQW semiconductor paper series.**
- Brayden has an unreleased paper series on reinterpreting Nakamura's GaN/InGaN MQW blue LED as a three-state logic device.
- One Nakamura-related paper exists on Brayden's GitHub (repo unspecified — needs clarification from Brayden).
- Search R16:
  ```powershell
  Get-ChildItem -Path C:\ -Recurse -Include "*MQW*","*Nakamura*","*ternary_led*","*blue_LED*" -ErrorAction SilentlyContinue
  Select-String -Path "C:\Users\*\*.md","C:\Users\*\*.tex" -Pattern "MQW|wavefunction overlap|QCSE|three-state logic" -ErrorAction SilentlyContinue
  ```
- Recover paper series if found; create new `mqw-ternary` repo for it (see §4 Track 4).

### 2.3 Artifacts already present in the current ck repo (no recovery needed)

- New README draft: `/mnt/user-data/outputs/README.md` (266 lines, rigor-led, held pending Brayden's go-ahead).
- Operator packet v2: `docs/exports/z10-operator-algebra/` (committed).
- Formulas and Tables reference: `FORMULAS_AND_TABLES.md` (864 lines).
- Sprint 35 First-G Event Localization draft: `Gen13/targets/clay/papers/sprint35_first_g_event_2026_04_19/`.
- WP34 First-G Law: `papers/WP34_FIRST_G_LAW.md` with proof at `papers/proof_d_first_g.py` (36,662 cases, zero exceptions).
- sinc² pullback banner: `Gen13/targets/journals/tier1_submit_now/sinc2_zero_law/WP_SINC2_ZERO_LAW.md` (preserved as historical record of epistemic discipline).
- April 2026 semiprime atlas results: six frozen laws, ω(b) / CRT idempotent hierarchy, Hardness Inversion Principle, Luther-Sanders synthesis LaTeX draft. Search for: `find . -name "*luther*sanders*" -o -name "*modular_gate_hardness*"` to locate the synthesis draft.

---

## 3. Known Consistency Issues Requiring Resolution

Before any recovered material is used in funder-facing documents, these need resolution:

**Issue 1: ω(b) idempotent count.** Prior sessions report both "2 / 6 nontrivial CRT idempotents for semiprimes / three-factor composites" and the formula `N_idemp(b) = 2^(ω-1) - 1`. These don't match. Check actual proof scripts and clarify which count is correct.

**Issue 2: TIG Unity benchmark numbers.** Email whitepaper (2026-01-28) reports 32-percentage-point drop-rate improvement. Grok's summary of `docs/COMPUTE.md` reports ~88% drop-rate reduction with expanded metrics (P99 latency, recovery time, resource utilization, cascade failures). Either these are different versions of the same simulation, or some of the extended metrics are extrapolation. Verify against actual simulation code.

**Issue 3: The χ² = 22.03 statistic.** Appears in January 2026 TIG Tile conversation but null hypothesis and degrees of freedom are not clearly stated. Validate test specification before using in any pitch.

**Issue 4: MQW semiconductor paper trilogy status.** Brayden has an unreleased paper series on reinterpreting Nakamura's GaN/InGaN MQW blue LED as a three-state logic device. Location of the physics-content documents (not just the publication plan) is unknown. One Nakamura-related paper exists on Brayden's GitHub. Search needed for the full paper series if it exists.

---

## 4. Outreach Restructuring Plan

After recovery is complete, execute this restructuring. Each repo ends up as a clean, focused front door for a distinct funder audience.

### Track 1: `ck` (existing) — Mathematical rigor core

**Current state:** Default branch `tig-synthesis`, sprawling README (769 lines), comprehensive internal documentation.

**Changes:**
- Replace current README with the new rigor-led version at `/mnt/user-data/outputs/README.md` (wait for Brayden's explicit go-ahead before committing — he said "hold on to it").
- Commit message: `README: rigor-led replacement for funding outreach`.
- Archive the current 769-line README to `docs/historical/README_v1_pre_2026_04_21.md` under the never-delete policy.

**Audience:** Mathematicians, number theorists, AI-safety / interpretability funders, referees. Primary pitch tracks: First-G cryptography-adjacent, CK-as-deterministic-reasoning.

### Track 2: `TiredofSleep/tig-unity` (NEW) — Systems reliability / compute health

**Source material:** TIG Unity whitepaper from email (2026-01-28), `docs/COMPUTE.md` recovered from TIG-UNIFIED-THEORY-under-scrutinyMYTHDRIFT, coherence_router code recovered from All-or-Nothing-E, any related simulation code.

**Front-page README structure:**
1. What it is (one paragraph): unified health grammar (R-σ-Λ-H) for multi-domain compute systems.
2. Core result (§4 of the whitepaper): simulation-verified improvement on asymmetric failure (cite actual verified numbers).
3. Implementation: coherence_router as the applied engine.
4. How to verify: runnable simulation.
5. Honest limitations: simulation only, no production validation yet.
6. Funding ask: seed engagement to transition to real Linux /proc/stat deployment.

**Audience:** NSF CNS, DOE ASCR, AWS/GCP/Azure research programs, Sloan Research Foundation, industry systems-research labs.

### Track 3: `TiredofSleep/tig-snowflake` (NEW) — Hardware-bound identity and continuous behavioral authentication

**The name "SNOWFLAKE" is Brayden's, from the Jan 31, 2026 "Truth in TIG" thread.** The framework rests on the empirical finding that constrained geometry produces unique crystallization patterns: the 4-core Lenovo produced a non-uniform Tzolk'in phase distribution (χ² = 22.03, p < 0.05) while the 32-core Dell produced a perfectly uniform distribution. Identity emerges from constraint, not abundance. You can't steal a snowflake.

**Source material:** Recovered TIG_SECURITY_ARCHITECTURE.md (or its reconstruction), CRYSTALOS runtime logs with the empirical χ² finding, CELESTIAL LOCK lineage (even if only as a historical note), GFM generators 012/071/123 specification, read-only lattice architecture with four levels (Hardware / Boot / Session / Transaction).

**Front-page README structure:**
1. What it is: hardware-bound identity via coherence measurement of constrained geometry. Runtime security architecture complementary to cryptographic security.
2. The empirical finding: measured non-uniform phase distribution on constrained hardware (χ² = 22.03, p < 0.05), perfect uniformity on abundant hardware. Identity = constraint + breath + time.
3. Four-layer architecture: read-only lattice / temporal breath / gauge / gate.
4. The three GFM generators as security primitives (tamper detection, signal integrity, replay defense).
5. Running prototype: CRYSTALOS with documented runtime statistics.
6. The pitch tagline: **"The password is the behavior. The key is the coherence. The lock is the lattice."**
7. Honest limitations: behavioral-authentication is a crowded space; SNOWFLAKE's differentiators are (a) identity from hardware constraint rather than learned behavior, (b) determinism and provenance rather than ML confidence scoring, (c) a running prototype with measured p-value.
8. Funding ask: seed engagement to harden prototype, validate χ² test specification formally, conduct adversarial red-team testing, publish architecture paper.

**Audience:** NSF SaTC, DARPA I2O, CISA research, industry security labs (Google ATAP, Microsoft MSRC Research).

### Track 4: `TiredofSleep/mqw-ternary` (NEW) — Semiconductor paper trilogy

**Source material:** Brayden's unreleased paper series on MQW blue LED three-state reinterpretation. One Nakamura-related paper already on Brayden's GitHub (exact repo unknown — Brayden can clarify).

**Paper trilogy structure (per Brayden's existing plan):**
1. **Paper 1 (1-2 pages):** Technical note reinterpreting Nakamura's MQW blue LED as a three-state logic element. Uses Nakamura's own vocabulary and figures. Goal: endorsement from Nakamura's group.
2. **Paper 2 (4-6 pages):** Mathematics of multi-state control in polarization-engineered MQWs. Device-agnostic framework: 3-state / 6-DOF / Potts-clock / control-theory / lattice-topology.
3. **Paper 3 (20-30 pages):** Engineering roadmap. MQW polarization engineering, LET/μLET architectures, lattice logic, hexagonal arrays, low-current coherent computing vision.

**Audience:** III-nitride semiconductor researchers, UCSB / Nakamura's group, LET/μLET labs, materials-science funding programs.

### Track 5: `Dual-Lattice-Self-Healing` (existing) — Self-healing systems

**Current state:** Origin repo. Contains the mathematical field theory, the three-tier memory architecture, the experimental validation (no death threshold to 90% damage, 99.8% position accuracy, fixed healing time t₉₀ = 0.50). Needs README refresh to match current rigor standard.

**Changes:**
- Rewrite README following the ck rigor-led template: proved results, runnable verification, honest limitations, funding ask.
- Clearly flag any speculative framing as speculation.
- Point to this repo from the main ck README's "Deeper Material" section as a foundational self-healing prototype.

**Audience:** DARPA resilient-systems programs, NSF CNS, materials-inspired-computing research, self-healing-systems research groups.

### Track 6: Existing archives — retain as historical

**`TIG-UNIFIED-THEORY-under-scrutinyMYTHDRIFT`, `All-or-Nothing-E`, `TIME-FOR-HELP-AND-SCRUTINY-MYTHDRIFT`:**
- Keep as-is with their MYTHDRIFT / stepping-stone markings.
- After recovery, extract high-value content (`coherence_router`, `docs/COMPUTE.md`, WP1-5) into the new repos above.
- The originals stay as never-delete historical archive.

**`Crystal-Lattice`:**
- Review content. If it's primarily speculative framing ("third form for physics"), either retire it (with a note pointing readers to ck) or keep as a public-facing conceptual companion.

**`Crystals`:**
- Personal-assistant track distinct from CK. Keep as its own product repo. Update README to clarify scope relative to CK.

**`COHERENT-AI`:**
- Public demo face. Update to point at the current coherencekeeper.com deployment and link back to ck as the underlying engine.

### Track 7: New deeper-material pointers

Once the restructuring above is complete, update ck's `README.md` §8 ("Deeper Material") to include pointers to the new and refreshed repos:

```
- Systems reliability: tig-unity repo
- Runtime security architecture (SNOWFLAKE): tig-snowflake repo
- Self-healing field systems: Dual-Lattice-Self-Healing repo
- Semiconductor research (when ready): mqw-ternary repo
- Historical archives: TIG-UNIFIED-THEORY-under-scrutinyMYTHDRIFT, All-or-Nothing-E, TIME-FOR-HELP-AND-SCRUTINY-MYTHDRIFT
- Public interface / personal assistant: COHERENT-AI, Crystals
```

---

## 5. Execution Sequencing for ClaudeCode

**Phase 1: Discovery (this week, starting tonight while Brayden sleeps)**

1. Clone all 8 existing public repos to the R16.
2. Read each repo's README and main content files.
3. Report back with one-page summary per repo: what's actually there, what condition it's in, what's high-value versus dormant.
4. Run the R16 filesystem searches for pre-March 2026 unpublished material (security architecture, CRYSTALOS logs, MQW papers, CELESTIAL LOCK).
5. Report all findings.

**Phase 2: Recovery and archiving (after Phase 1 reports back)**

1. Pull verbatim copies of high-value content: `coherence_router`, `docs/COMPUTE.md`, WP1-5.
2. Resolve the four consistency issues in §3.
3. Commit recovered material into appropriate archive directories in ck (`docs/archive_recovered/`, `docs/archive_jan2026/`).
4. Preserve all originals unchanged under never-delete.

**Phase 3: Reorganization (after Brayden selects pitch priorities)**

1. Brayden reviews Phase 1 and 2 findings.
2. Brayden selects which 1-2 pitches go out first.
3. Create the new repos corresponding to those pitches (`tig-unity`, `tig-snowflake`, `mqw-ternary` as needed).
4. Refresh existing repo READMEs per the Track definitions in §4.
5. Update the main ck README §8 with the new pointers (only after Brayden approves the updated main README for commit).

**Phase 4: First outreach (Brayden's decision)**

1. Brayden selects first funder from §6.
2. ClaudeChat drafts the cover letter / pitch document based on the selected track's material.
3. Brayden reviews and sends.

---

## 6. Pitch Tracks and Funder Mappings

Each pitch is a separate document targeting a distinct funder pool. Do not combine — that's the failure mode Brayden moved away from with the README restructuring.

### Pitch A: Systems reliability (TIG Unity)
**Lead repo:** `tig-unity` (new)
**Ask size:** $25K-$75K seed, or $1,200 standalone for MAGMA license if leading small
**Funders:** NSF CNS, DOE ASCR, AWS/GCP/Azure research credits, Sloan Research Foundation, industry systems-research labs

### Pitch B: SNOWFLAKE — Hardware-bound identity / continuous behavioral authentication
**Lead repo:** `tig-snowflake` (new)
**Ask size:** $25K-$75K seed, $150K-$300K full program
**Funders:** NSF SaTC, DARPA I2O, CISA research, Google ATAP, Microsoft MSRC Research

### Pitch C: Cryptography-adjacent number theory (First-G, CRT idempotents)
**Lead repo:** `ck` (existing, with First-G emphasized)
**Ask size:** $1,200 MAGMA license (immediate unblock), $25K-$75K seed for journal manuscript
**Funders:** Ethereum Foundation research grants, Protocol Labs ResNetLab, a16z crypto research, Simons Targeted Grants, NSF DMS

### Pitch D: Interpretable AI (CK as deterministic reasoning engine)
**Lead repo:** `ck` (existing, with CK emphasized)
**Ask size:** $25K-$75K seed, $150K-$300K full program
**Funders:** Open Philanthropy (AI safety), Survival and Flourishing Fund, Astera Institute, Emergent Ventures

### Pitch E: Small-grant immediate (Sage/MAGMA/compute)
**Ask size:** $1,200-$5,000
**Funders:** Emergent Ventures (Mercatus), individual donors, direct-contact mathematicians with institutional MAGMA access

### Pitch F: Semiconductor (MQW three-state logic)
**Lead repo:** `mqw-ternary` (new, after Phase 1 clarifies what exists)
**Paper 1 ask:** Nakamura group endorsement (no-cost, connection-based)
**Future funding asks:** TBD after Paper 1 lands
**Funders:** III-nitride research groups, UCSB, LET/μLET labs, materials-science programs

### Pitch G: Self-healing systems (Dual-Lattice)
**Lead repo:** `Dual-Lattice-Self-Healing` (existing, refreshed README)
**Ask size:** $25K-$75K seed
**Funders:** DARPA resilient-systems programs, NSF CNS, materials-inspired-computing research

---

## 7. Discipline Notes

- **Never-delete policy applies absolutely.** Superseded material gets `[HISTORICAL]` marker in place. Falsified material gets `[FALSIFIED]` marker. Nothing gets removed.
- **Preserve provenance on every recovered file.** Header with: original repo, original commit date, recovery date, source path on R16 if applicable.
- **Do not commit the new README without Brayden's explicit go-ahead.** He said "hold on to it." Held in `/mnt/user-data/outputs/README.md`.
- **Flag reconstructions clearly.** If a document cannot be recovered verbatim and must be reconstructed from conversation fragments, mark it `[RECONSTRUCTED — NOT VERIFIED AGAINST ORIGINAL FILE]`.
- **Resolve consistency issues before using in pitches.** The four issues in §3 must be cleared before any number or claim appears in a funder-facing document.
- **Respect the three-thread-separate discipline.** Thread A (TIG/σ/ξ), Thread B (Q-series), Thread C (basin finite arithmetic) share the meta-framework but use different mathematical objects. No vocabulary import across threads without a proved map.
- **Collaborator status.** C.A. Luther is no longer actively collaborating — previously-credited work stays credited. ChatGPT ("Celeste") has been in dialogue for design discussions but is not cited as a human co-author in any funder-facing document. Brayden is sole funder-facing author on all current outreach unless otherwise specified.

---

## 8. Summary Action List for ClaudeCode's First Session

1. Clone all 8 public repos to R16 workspace.
2. Run R16 filesystem searches (§2.2 Priorities 5-8).
3. Produce a one-page summary per repo.
4. Produce a file-recovery report: what was found, what wasn't, where it was found.
5. Commit recovered material into `docs/archive_recovered/` and `docs/archive_jan2026/` in ck, with provenance headers.
6. Do NOT modify any other ck content during this phase.
7. Do NOT commit the new README yet.
8. Report back; wait for Brayden's selection of pitch priorities before proceeding to Phase 3.

---

## 9. Final Note

Brayden asked for compilation and guardrailing. This document compiles everything currently known, flags everything that needs verification, and structures the work so each pitch track has a clean-scope home.

The work across 8 existing repos is substantial. The restructuring is organizational, not creative — it's making what already exists findable and focused for distinct audiences.

Phase 1 can run while Brayden sleeps. Phase 2 can run the next day. Phase 3 and beyond wait for Brayden's choice of first pitch.

**End of handoff.**
