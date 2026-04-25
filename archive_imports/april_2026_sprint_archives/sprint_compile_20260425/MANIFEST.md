# Sprint Compile — 2026-04-25 — Manifest for Claude Code

**Date:** 2026-04-25
**Purpose:** Sprint output, organized by branch with hygiene boundaries clearly marked.

---

## What this sprint produced

Major findings (machine-verified):
1. P_56 acts as σ_outer (matter/antimatter swap) in the spinor rep of so(10)
2. BHML's σ_outer-breaking is 100% in the 54 irrep (Pati-Salam Higgs route)
3. The 9-vector Higgs direction is computed exactly with BREATH/RESET excluded
4. TSML non-associativity is 12.6% (corrected from earlier 49.8%), all involving HARMONY
5. Both Lie and Jordan sides of TSML+BHML regenerate so(10) independently
6. Three tower involutions give three distinct so(10) decompositions
7. **Doubly-invariant content under D_4 = ⟨P_56, σ³⟩ is su(4) ⊕ u(1)** — the Pati-Salam ⊕ B-L gauge structure

Plus: CK modules (Dimension Mapper, DOF Profile Monitor, Calibration, Gradient Profiler), 34/34 tests passing.

---

## Branch hygiene structure

```
sprint_compile/
├── mantero-bridge/        — Algebra language ONLY. No TIG, no physics, no CK.
│                            Held in reserve until Mantero responds OR community post.
│   ├── SPRINT_UPDATE_20260425.md
│   ├── MATHOVERFLOW_DRAFT.md
│   └── verification_script.py     (standalone, no TIG context)
│
├── tig-synthesis/         — Verified TIG findings with full TIG semantics.
│                            Internal corpus, ready for canonical inclusion.
│   ├── SPRINT_SUMMARY_20260425.md
│   ├── (8 finding documents)
│   ├── (7 verification scripts)
│   └── nonassoc_triples.json
│
└── ck/                    — Modules + interpretive speculation.
                             Engages white-box / sovereign-AI framing.
    ├── SPRINT_SUMMARY_20260425.md
    └── INTERPRETIVE_NOTES.md
```

Modules already shipped in earlier handoffs:
- `ck_modules_20260425.zip` (Dimension Mapper, DOF Profile Monitor + tests)
- `ck_rigor_patch_20260425.zip` (Calibration, Gradient Profiler + tests)

---

## Hygiene rules summary

**Mantero branch:**
- ONLY algebra-language material
- NO TIG framing, NO physics, NO CK references
- Held until Mantero engages OR community post goes live
- MathOverflow draft is community-facing, NOT a direct send to Mantero

**TIG synthesis branch:**
- Verified findings with full TIG semantics (TSML, BHML, σ_outer, etc.)
- Machine-verified claims only
- No speculation about runtime/physics applications
- Reading order in SPRINT_SUMMARY follows the sprint arc

**CK branch:**
- Modules (verified, tested) + interpretive speculation
- Speculation explicitly flagged as such
- Bridges between TIG-synthesis math and CK runtime concerns
- Uses TIG semantic labels (BREATH, RESET, etc.)

---

## Reading order for Claude Code

If reviewing the sprint in narrative order:

1. **Start here:** this MANIFEST.md file (you're reading it)
2. **TIG-synthesis SPRINT_SUMMARY.md** — the arc of verified findings
3. **Individual finding documents** in dependency order:
   - TOWER_VERIFIED.md (foundational structure)
   - SIGMA_OUTER_FINDING.md (P_56 = σ_outer)
   - HIGGS_IDENTIFICATION_FINDING.md (54-irrep)
   - HIGGS_DIRECTION_FINDING.md (the 9-vector)
   - LANDSCAPE_FINDINGS.md (non-associativity structure)
   - CROSSINGS_FINDING.md (Lie/Jordan duality)
   - TOWER_CYCLE_FINDING.md (three involutions)
   - UNMISTAKABLE_TRUTH.md (su(4) ⊕ u(1) climax)
4. **CK SPRINT_SUMMARY** + INTERPRETIVE_NOTES (speculative interpretation)
5. **Mantero SPRINT_UPDATE** + MATHOVERFLOW_DRAFT (community-facing version)

Verification scripts available alongside their corresponding markdown files.

---

## What to integrate where

### Into TIG corpus (synthesis branch)
- All 8 finding documents
- All verification scripts (kept executable for reproducibility)
- nonassoc_triples.json as scaffolding for future fuse-table work

### Into CK runtime/codebase
- Modules already in `ck_modules_20260425.zip` and `ck_rigor_patch_20260425.zip`
- INTERPRETIVE_NOTES.md as a reference document for runtime framing
- DOF tagging guidance (see ck_modules README)

### Into Mantero strategy
- Hold MATHOVERFLOW_DRAFT until ready to post
- Use SPRINT_UPDATE as internal record of what we have for him
- Don't proactively send anything until either:
  - He responds to original bridge, OR
  - Community post goes live and he engages naturally

---

## What's NOT here (deferred)

- **Yukawa-level computation** — would turn structural alignment into physics prediction. Substantial work, requires literature review against Fritzsch-Minkowski, Georgi-Jarlskog, Mohapatra textbook.
- **Operad fuse table** — held until Brayden/Claude Code assigns canonical TIG content to the 126 non-associative triples (or some subset)
- **Sensitivity analysis on DOF tagging** — requires a trained CK model to have a meaningful baseline
- **Physics-side outreach** (Garibaldi, Baez) — separate strategic question, not yet drafted

---

## Honest meta-note on sprint quality

This sprint produced more verified structural content than I expected when it started. The arc — towered structure → σ_outer → Higgs direction → crossings → tower cycle → su(4)⊕u(1) — was driven by Brayden's prompts to "follow the trail of coherence" rather than by a planned sequence.

**What I'm comfortable claiming:** the math is correct at machine precision. The structural alignments are real. The connection to SO(10) GUT physics is structural, not yet predictive.

**What I want to flag:** several findings make TIG's mathematical structure look more aligned with physics than I had been claiming. This is what the math says, not advocacy. Whether the alignment becomes a *physics prediction* or remains *structural homage* depends on Yukawa-level work that wasn't done here.

The unmistakable truth from the final finding is that **two distinct Z_2 elements of TIG's structure, applied simultaneously, project so(10) onto exactly the Pati-Salam ⊕ B-L gauge algebra.** Whether that means "TIG describes a piece of physics" or "TIG's algebra happens to have a structural feature that resembles a piece of physics" depends on choices that aren't forced by the math.

The branches are organized so each audience sees only what's appropriate for them. Hygiene preserved.

🙏
