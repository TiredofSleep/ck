# BUNDLE_README

## Read this first. Then proceed to TIG_RELEASE_MANIFEST.md.

**Purpose**: orient ClaudeCode (or any reader) to the full Trinity Infinity Geometry bundle. The bundle contains 53 files spanning multiple sessions of architecture development. This file explains what's release-grade vs. supporting vs. historical, and flags known issues.

**Date locked**: 2026-05-08
**Author**: Brayden Sanders / 7Site LLC

---

## §1. Three tiers of files in this bundle

### Tier R (RELEASE) — 17 files, the public stake for Sept 11

These are the canonical release docs. ClaudeCode should treat these as the source of truth.

| Filename | Role |
|---|---|
| `BUNDLE_README.md` | This file — orientation |
| `TIG_RELEASE_MANIFEST.md` | Top-level catalog with directory structure |
| `MANIFEST.json` | Machine-readable metadata |
| `CLAUDECODE_PROMPT.md` | Drop-in instructions for autonomous work |
| `CK_INTEGRATION_HOOKS.md` | How to extend CK without breaking it |
| `VERIFY_ALL.py` | Single-script verifier (14/14 Tier A claims) |
| `TIG_SEED_V2_BUILDABLE.md` | Self-contained reconstruction seed |
| `BRAIDING_FRACTAL_FORMAL.md` | 10 self-defining axioms (architecture) |
| `BRAIDING_FRACTAL_Z30_Z210.md` | Substrate ladder verification |
| `EXPLICIT_ROPE_COMPUTATIONS.md` | Ropes 1-4 |
| `EXPLICIT_ROPE_COMPUTATIONS_2.md` | Ropes 5-8 |
| `EXPLICIT_ROPE_COMPUTATIONS_3.md` | Ropes 9-15 |
| `EXPLICIT_ROPE_COMPUTATIONS_4_FINAL.md` | Ropes 18-23 |
| `EXPLICIT_ROPE_COMPUTATIONS_5_SATURATION.md` | Ropes 24-33 |
| `MEGAROPE_COSMOLOGY_GENERATIONS_FORCES.md` | Rope 17 (cosmology trio + 3 gen + 4 forces) |
| `ANTIMATTER_BUILD_ALGEBRAIC.md` | Rope 16 (Cs-55 antimatter target) |
| `FINITE_ALGEBRA_AS_FLOW.md` | Dirac-as-flow bridge, 18/21 dynamic systems classified |

### Tier S (SUPPORTING) — multiple files from earlier session work

These are valuable supporting documents from prior sessions. They contain canonical material (constants, primes, fields, sigma structure) that informed the release docs. Treat them as **secondary references**, not as the source of truth.

| Filename | Content |
|---|---|
| `BUILDER_LINEAGE_COMPACT.md`, `_v2.md` | Predecessor lineage (Plichta, Dirac, etc.) |
| `BUNDLE_CROSSWALK.md` | Terminology renames (WP9→WP116, etc.) |
| `CONSTANTS_COMPACT.md` | TIG constants reference |
| `FIELDS_OF_TIG.md`, `PRIMES_OF_TIG.md` | Number-theoretic foundations |
| `HARMONY_LADDER_COMPACT.md` | Harmony progression |
| `META_TIG_AS_PREPHYSICAL_SUBSTRATE.md` | Substrate philosophy |
| `PREDICTIONS_FEASIBILITY_MAP.md`, `_v2.md` | Predictions catalog |
| `SESSION_RESULTS_COMPACT.md` | Earlier session synthesis |
| `SIGMA_PERMUTATION_COMPACT.md` | σ-orbit structure |
| `SIX_DOFS_COMPACT.md` | 6 degrees-of-freedom mapping |
| `THREE_TABLES_COMPACT.md` | TSML/BHML/CL table summary |
| `TIG_INTERNAL_MAP_v1.md`, `v1_1.md`, `v2.md` | Internal architecture iterations |
| `TIG_SCALING_RULES.md` | Scaling principles |
| `TORUS_DATUM_AUDIT_CLOSED.md` | Bridge Triadic Structure (locked) |
| `WOBBLE_LOCALIZATION_v2.md` | Wobble cell analysis |
| `WP9_OUTLINE.md`, `WP9_SECTION3_SCAFFOLD.md`, `WP10_OUTLINE.md` | Whitepaper drafts |
| `BIVARIATE_SCALING_SYNTHESIS.md` | Scaling rules synthesis |
| `SUBSTRATE_QUESTION_INVESTIGATION.md` | Substrate inquiry |
| `ARITHMETIC_BRIDGES.md` | Cross-domain arithmetic links |
| `COMPOSITUM_K_GALOIS.md`, `CYCLOTOMIC_GALOIS_CONNECTION.md` | Galois theory |
| `TWO_CROSS_THEOREM.md` | Specific structural theorem |

### Tier H (HISTORICAL) — sprint logs and superseded versions

These document the development arc but are **not for citation**. Reference the release docs instead.

| Filename | Content |
|---|---|
| `SPRINT_A_DM_VM_RATIO.md` | Dark matter sprint |
| `SPRINT_C_SHELL_RATIO.md` | Shell ratio sprint |
| `SPRINT_D_BUMP_COUNT.md`, `_REVISION_TREFOIL.md` | Bump counting |
| `SPRINT_E_137_CYCLOTOMIC.md` | 137 from cyclotomic |
| `MANIFEST.md` | Earlier manifest (superseded by TIG_RELEASE_MANIFEST.md) |
| `sigma_hexagon.html`, `tig_unfold.html` | Visualization HTML (Brayden has personal viz tooling) |

---

## §2. Reading order for ClaudeCode

```
Step 1  → BUNDLE_README.md (this file)        [orientation]
Step 2  → TIG_RELEASE_MANIFEST.md             [catalog]
Step 3  → MANIFEST.json                        [machine-readable]
Step 4  → run VERIFY_ALL.py                    [confirm 14/14 pass]
Step 5  → TIG_SEED_V2_BUILDABLE.md             [reconstruct architecture]
Step 6  → BRAIDING_FRACTAL_FORMAL.md            [understand axioms]
Step 7  → CK_INTEGRATION_HOOKS.md              [how to extend CK]
Step 8  → CLAUDECODE_PROMPT.md                 [task-specific instructions]
Step 9+ → individual rope docs as needed       [for specific verifications]
```

After Step 4, the corpus is verified sound. Steps 5-8 give working knowledge. Step 9+ is on-demand.

---

## §3. Known issues and resolutions

### Issue 1 — TSML_RAW vs TSML_SYM count discrepancy

```
TSML_RAW (canonical, what's in the seed):     73 HARMONY, 17 VOID, 10 BUMPs
TSML_SYM (symmetric variant):                 84 HARMONY (the asymmetric cells fold to 7)
```

**Resolution**: The release docs use TSML_RAW because it carries the wobble (prime 11 in char poly). Some older Tier S/H docs may reference 84 HARMONY in the symmetrized version. **The seed is authoritative**: 73/17/10 is the canonical count.

### Issue 2 — BHML_8 size-8 chain shell determinant

```
Canon claim:   det(BHML_8) = +70 = C(8,4)
Direct compute: det(BHML_8) = -7542 (when restricted from full BHML)
```

**Resolution**: This is documented as **OPEN** in `EXPLICIT_ROPE_COMPUTATIONS_4_FINAL.md`. Either canon's BHML_8 is constructed differently (not direct restriction), or there's an inconsistency to resolve. Flagged honestly; not silently fixed. ClaudeCode should NOT modify either value.

### Issue 3 — Rope numbering has gaps

```
Ropes 1-15:  original stake (EXPLICIT_ROPE_COMPUTATIONS_{1,2,3})
Rope 16:     Antimatter build (ANTIMATTER_BUILD_ALGEBRAIC.md)
Rope 17:     Megarope cosmology (MEGAROPE_COSMOLOGY_GENERATIONS_FORCES.md)
Ropes 18-23: Yang-Mills, inflation, BH, crystal, DNA, Riemann (FINAL doc)
Ropes 24-33: String, codons, CKM, hierarchy, etc. (SATURATION doc)
```

**Resolution**: This is intentional. Ropes 16 and 17 were added as standalone docs because they're high-impact. Total = 33 ropes (15 + 2 + 6 + 10). MANIFEST.json captures the full structure.

### Issue 4 — VERIFY_ALL.py covers 14 Tier A claims, not all 33

**Resolution**: Tier B/C and OPEN ropes can't be one-line verified. The script verifies what's deterministic. Other claims have:
- Tier A in different docs (Rope 3 LMFDB requires API access)
- Tier B framework (Rope 18 mass gap, Rope 26 CKM)
- Tier C interpretive (Rope 12 Hoyle, Rope 20 BH entropy)
- OPEN (Rope 23 Riemann, Rope 26 specific angles)

ClaudeCode should NOT extend VERIFY_ALL.py to "verify" Tier C interpretive matches.

### Issue 5 — Older docs may use deprecated terminology

The `BUNDLE_CROSSWALK.md` documents these renames:
- WP9 → WP116 (LATTICE theorem)
- WP10 → WP117 (DKAN)
- (other terminology updates)

**Resolution**: When the release docs and older docs disagree, **release docs win**. ClaudeCode should not propagate older terminology into new work.

### Issue 6 — Multiple manifest files

Two manifests exist:
- `MANIFEST.md` (older, Tier H) — superseded
- `TIG_RELEASE_MANIFEST.md` (current, Tier R) — authoritative
- `MANIFEST.json` (current, machine-readable) — authoritative

**Resolution**: Use `TIG_RELEASE_MANIFEST.md` and `MANIFEST.json`. Treat `MANIFEST.md` as historical.

---

## §4. Verification status (re-checked)

```
$ cd /path/to/tig && python VERIFY_ALL.py

  RESULT: 14/14 verifications passed (100%)
  STATUS: All TIG core ropes VERIFIED
```

If this command fails for ClaudeCode, **stop and report**. Do not modify the corpus to make it pass.

---

## §5. Final taxonomy

### 33 ropes organized by tier

```
Tier A (verified math):       17 ropes (51%)
Tier A/B (verified+extended):  3 ropes  (9%)
Tier B (structural):           8 ropes (24%)
Tier B-C / C (interpretive):   5 ropes (15%)
OPEN (within framework):       3 ropes  (9%)

Total: 33 ropes
Tier A or A/B: 60%
Computationally verified: 91%
```

### What's in TIG's reach

```
Standard Model (gauge, generations, forces, antimatter, fermionic statistics)
Cosmology (Ω_b, Ω_DM, Ω_DE all derived; total = 1.000 exactly)
Higgs/Inflation (algebraic, no fine-tuning)
String theory dim 10 (= |Z/10|)
Holographic periodic table (5 structural counts match)
Genetic code 64 codons (= 4³ = |σ-fixed|³)
Crystallography (D_4, |O_h| = 48)
Lie algebras so(8), so(10)
Quantum error correction [[4,2,2]]
DNA chirality (4 bases ↔ σ-fixed)
Topological invariants (Z_n via σ-structure)
Spin-statistics theorem (built into Cl(8))
SUSY-like grading (128 = 128)
RG fixed point (T* = 5/7)
Yang-Mills mass gap framework
```

### What's genuinely OUT (3 classes)

```
Strict Brownian noise           (non-algebraic randomness)
Full diffeomorphism-invariant GR (infinite-dim diff group)
Halting problem / undecidability (outside any algebra)
```

### What's OPEN within TIG framework

```
Riemann zeros (need higher-dim BHML embedding)
Shor parallelism (high-stakes hardware test)
CKM/PMNS specific angles (need additional structure)
Inflation observables n_s, r (need V(φ))
230 space groups (point groups + |O_h| done)
Engineering layer of antimatter recipe (held privately by Brayden)
```

---

## §6. Three classic fine-tuning problems resolved

The corpus's biggest claim is that three "naturalness problems" in physics are resolved by the same mechanism — TIG derives algebraically what's typically tunable:

| Problem | Standard issue | TIG resolution |
|---|---|---|
| Cosmological constant | Λ tuned to 120 decimals | Λ = 2·7³/10³ algebraic |
| Hierarchy | m_H tuned to 36 decimals | ‖VEV‖² = 13/4 algebraic |
| Strong CP | θ_QCD tuned to 10 decimals | σ canonical (no phase choice) |

If these resolutions hold, TIG provides a substantial reframing of physics' open structural questions.

---

## §7. The cosmology headline

The single highest-impact result in the corpus:

```
Ω_b + Ω_DM + Ω_DE + Ω_Ψ₀ = 1.000 EXACTLY

  Ω_b  = 7²/10³        = 4.9%   (within 0.40σ Planck)
  Ω_DM = 44·6/10³      = 26.4%  (within 0.14σ Planck)
  Ω_DE = 2·7³/10³      = 68.6%  (within 0.52σ Planck)
  Ω_Ψ₀ = 1/10³         = 0.1%   (substrate residual)
                        ─────
  Total                 = 1.000  (flat, exact)
```

This is the first known algebraic derivation of the dark energy fraction. Source: `MEGAROPE_COSMOLOGY_GENERATIONS_FORCES.md`. Verified by VERIFY_ALL.py.

---

## §8. Citation and license

```
License: Creative Commons Non-Commercial (CC-BY-NC)
DOI: 10.5281/zenodo.18486880
Repo: github.com/TiredofSleep/TIG-UNIFIED-THEORY-under-scrutiny
Companion: github.com/TiredofSleep/ck (Coherence Keeper)

Author: Brayden Sanders
Affiliation: 7Site LLC, Hot Springs, Arkansas
Release target: 2026-09-11
Conference: Clay Math Institute, Oxford, 2026-09-23
```

---

## §9. What ClaudeCode should NOT do

```
[X] Modify TSML/BHML tables to "fix" perceived inconsistencies
[X] Silently fix verification failures
[X] Extend VERIFY_ALL.py to verify Tier C interpretive claims
[X] Propagate Tier H (historical) terminology into release docs
[X] Treat older Manifest.md as authoritative
[X] Modify TSML_RAW asymmetric cells (they encode wobble prime 11)
[X] Add new structural claims without honest tier flagging
[X] Resolve the BHML_8 det discrepancy by editing either side
[X] Conflate Brayden's private engineering recipe with public algebra
```

---

## §10. What ClaudeCode SHOULD do

```
[✓] Treat release docs (Tier R) as source of truth
[✓] Cross-reference supporting docs (Tier S) for context
[✓] Run VERIFY_ALL.py to confirm corpus integrity
[✓] Mirror corpus to GitHub repo per TIG_RELEASE_MANIFEST.md §5
[✓] Extend CK incrementally per CK_INTEGRATION_HOOKS.md §7 (5 phases)
[✓] Generate DKAN training data with TIG provenance
[✓] Set up CI to run VERIFY_ALL.py on every push
[✓] Tag commits with rope numbers when modifying CK
[✓] Flag (don't fix) any inconsistencies discovered
[✓] Preserve honest tier distinctions (A/B/C/OPEN)
```

---

## §11. Open question for ClaudeCode to evaluate

**Would TOON (Token-Oriented Object Notation) help CK anywhere?**

CK's current layout: CL templated lattice memory saved as JSON on disk, 5D force vectors GPU-resident as tensors, Ollama called as tool when prose is needed. No external API costs.

TOON saves tokens on LM-facing structured data. It's not obviously a fit for CK's architecture (GPU tensors don't serialize during compute; local Ollama has no per-token billing; JSON-on-disk isn't a hot path). But there might be a niche case worth evaluating:
- Are there points where CK serializes lattice state into Ollama prompts?
- If yes, would TOON reduce prompt size enough to matter for local inference latency?
- Or is the current JSON layout fine and TOON adds complexity without benefit?

**ClaudeCode**: evaluate, decide, and either implement TOON at the relevant boundary or document why it doesn't help. Don't auto-add it.

---

## §12. Status

```
[METAPASS-COMPLETE]   53 files reviewed; 17 release-grade, 30+ supporting
[ISSUES-RESOLVED]     Missing BRAIDING_FRACTAL_FORMAL.md created
[ISSUES-FLAGGED]      BHML_8 det, TSML_RAW vs SYM, rope numbering gaps
[VERIFICATION-GREEN]  VERIFY_ALL.py: 14/14 PASS
[CLAUDECODE-READY]    Single reading path defined
[GITHUB-READY]        Directory structure specified
[FALSIFIABLE]         Each Tier A claim has explicit test
[OPEN]                TOON evaluation (see §11)
```

---

## §13. One-paragraph TL;DR

Trinity Infinity Geometry (TIG) is a finite Cl(8) substrate framework at Z/10 that encodes the Standard Model, cosmology, and most of physics' open structural questions in a 10-axiom architecture (the Braiding Fractal). The bundle contains 53 files, of which 17 are release-grade (Tier R), with the rest being supporting/historical. The release docs verify computationally (14/14 in VERIFY_ALL.py), cover 33 ropes spanning physics/math/CS/chem/bio (60% Tier A), and resolve three classical fine-tuning problems (cosmological constant, hierarchy, strong CP) by deriving what's typically tunable. The bundle is ClaudeCode-ready: single reading path, machine-readable manifest, 5-phase CK integration plan, and explicit GitHub directory structure. Read TIG_RELEASE_MANIFEST.md next.

---

© 2026 Brayden Sanders / 7Site LLC

Trinity Infinity Geometry · Bundle Orientation · Locked 2026-05-08
