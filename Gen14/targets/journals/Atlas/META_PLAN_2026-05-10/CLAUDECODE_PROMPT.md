# CLAUDECODE_PROMPT

## Drop-in instructions for ClaudeCode integration

**Purpose**: hand this single file to ClaudeCode and it can autonomously work with the TIG corpus.

---

## 0. Context

You are working on Trinity Infinity Geometry (TIG), a finite Cl(8) substrate framework at Z/10 with verified algebraic content covering Standard Model physics, cosmology, and adjacent mathematical structures.

The corpus is **structurally complete** (33 ropes, 60% Tier A, 91% computationally verified). Your job is integration, not architecture.

---

## 1. First action: verify

Run this single command to confirm the corpus is sound:

```bash
cd /path/to/tig/verification
python VERIFY_ALL.py
```

**Expected output**: `RESULT: 14/14 verifications passed (100%)`

If anything fails, STOP and report. Do not modify the corpus.

---

## 2. Read these files in order

```
1. MANIFEST.json                       Machine-readable metadata
2. TIG_RELEASE_MANIFEST.md             Human-readable catalog
3. TIG_SEED_V2_BUILDABLE.md            The seed (~250 lines) - everything builds from here
4. CK_INTEGRATION_HOOKS.md             How to extend CK without breaking it
```

That's it for orientation. Each rope doc is self-contained for deeper reading.

---

## 3. Your tasks (priority order)

### TASK A — Mirror corpus to GitHub repo

```
SOURCE: /path/to/tig_outputs/
TARGET: github.com/TiredofSleep/TIG-UNIFIED-THEORY-under-scrutiny

Apply directory structure from TIG_RELEASE_MANIFEST.md §5:
  seed/ architecture/ ropes/ verification/ integration/ manifest/

Renames:
  EXPLICIT_ROPE_COMPUTATIONS.md             -> ropes/01_explicit_ropes_1-4.md
  EXPLICIT_ROPE_COMPUTATIONS_2.md           -> ropes/02_explicit_ropes_5-8.md
  EXPLICIT_ROPE_COMPUTATIONS_3.md           -> ropes/03_explicit_ropes_9-15.md
  EXPLICIT_ROPE_COMPUTATIONS_4_FINAL.md     -> ropes/04_explicit_ropes_18-23.md
  EXPLICIT_ROPE_COMPUTATIONS_5_SATURATION.md -> ropes/05_explicit_ropes_24-33.md
  ANTIMATTER_BUILD_ALGEBRAIC.md             -> ropes/16_antimatter_build.md
  MEGAROPE_COSMOLOGY_GENERATIONS_FORCES.md  -> ropes/17_megarope_cosmology.md
  FINITE_ALGEBRA_AS_FLOW.md                 -> ropes/flow_bridge.md
  TIG_SEED_V2_BUILDABLE.md                  -> seed/
  BRAIDING_FRACTAL_FORMAL.md                 -> architecture/
  BRAIDING_FRACTAL_Z30_Z210.md               -> architecture/
  TIG_RELEASE_MANIFEST.md, MANIFEST.json    -> manifest/
  CK_INTEGRATION_HOOKS.md, this file        -> integration/
  VERIFY_ALL.py                             -> verification/

Add to repo root:
  README.md (with summary, link to manifest, DOI badge)
  LICENSE (CC-BY-NC text)
  CITATION.cff (with DOI 10.5281/zenodo.18486880)
  .github/workflows/tig_verify.yml (CI from CK_INTEGRATION_HOOKS.md §5)
```

### TASK B — Extend CK with TIG hooks

```
TARGET: github.com/TiredofSleep/ck

Per CK_INTEGRATION_HOOKS.md §7 (5 phases):

PHASE 1: drop test_tig_integration.py into tests/
PHASE 2: extend ck_core.py with cl8_gammas() and chirality_omega() (§2)
PHASE 3: extend ck_organism.py with TIG_DNA_MAPPING (§2)
PHASE 4: DKAN training data preparation (longer timeframe)
PHASE 5: deployment-target-specific builds

After each phase:
  - Run pytest (existing 529 tests must still pass)
  - Run VERIFY_ALL.py (must continue to be 14/14)
  - Commit with rope numbers in message: "TIG ropes 1, 6, 7 integrated"
```

### TASK C — DKAN training data generation

```
For each Tier A rope (17 total):
  1. Read the rope's documented computation
  2. Generate 10-50 training examples in DKAN format:
     - input: question/prompt about the rope content
     - output: explanation with cell-level TSML/BHML provenance
     - tier: "A"
     - rope_id: <number>
  3. Validate output passes the corresponding rope's verification check

Save to: ck/dkan_training/tig_provenanced/

Example training pair format:
  {
    "input": "Why is Omega_DM = 26.4% in TIG cosmology?",
    "output": "Omega_DM = 44 * 6 / 10^3 = 264/1000 = 0.264, where 44 is canon's CL_STD HARMONY count, 6 is ord(sigma), and 10^3 is the kernel-cubed denominator. From canon Rope 17.",
    "tier": "A",
    "rope_id": 17,
    "provenance": "MEGAROPE_COSMOLOGY_GENERATIONS_FORCES.md §1"
  }
```

---

## 4. Falsifiability protocol

**Never fudge a verification.** If a check fails:

```
1. Identify which rope/claim
2. Report: "ROPE X failed: <reason>"
3. Do NOT modify the corpus to make it pass
4. Open an issue in the repo with the failure details
5. Wait for human review
```

This is critical. The corpus's value depends on every claim being computationally honest.

---

## 5. Communication protocol

When committing:
- Use rope numbers in commit messages: `[ROPE 7] [[4,2,2]] ZZZZ stabilizer integration`
- Reference doc filenames when modifying: `ck_core.py: add cl8_gammas() per CK_INTEGRATION_HOOKS.md §2`
- Tag releases with TIG version: `tig-v1.0-2026-09-11`

When proposing extensions:
- Specify tier honestly (A/B/C/OPEN)
- Include falsification condition
- Match the canon's D-number discipline if creating new constants

---

## 6. What NOT to do

```
[X] Do not weaken Tier A claims to Tier B for convenience
[X] Do not silently fix verification failures by changing test thresholds
[X] Do not extend the corpus into Tier C territory without flagging
[X] Do not break existing CK tests
[X] Do not introduce new free parameters (TIG's value is being parameter-free)
[X] Do not remove the TSML_RAW asymmetric cells (they encode prime 11)
```

---

## 7. Specific quick-references

### TIG kernel
```
Z/10 = Z/2 × Z/5
Operators: 0=VOID, 1=LATTICE, 2=COUNTER, 3=PROGRESS, 4=COLLAPSE,
           5=BALANCE, 6=CHAOS, 7=HARMONY, 8=BREATH, 9=RESET
```

### Core constants
```
T*  = 5/7
W   = 3/50
Omega_b  = 7^2/10^3  = 4.9%
Omega_DM = 44*6/10^3 = 26.4%
Omega_DE = 2*7^3/10^3 = 68.6%
Omega_Psi0 = 1/10^3 = 0.1%
Total = 1.000 exactly
alpha^-1 = 137 = 22*6 + 5
||VEV||^2 = 13/4
kappa_xi = 13/(4e)
```

### Sigma structure
```
sigma = (0)(3)(8)(9)(1 7 6 5 4 2)
ord(sigma) = 6
ord(sigma^2) = 3 (forces depth-3 limit, gives 3 generations)
sigma-fixed = {0,3,8,9} (4 elements, gives 4 forces)
sigma-cycle = (1,7,6,5,4,2) (6 elements)
sigma^3-pairs = {1,5}, {4,7}, {2,6} (sums 6, 11, 8)
```

### Strata
```
I  (substrate):  {2, 3, 5}
II (HARMONY):    {7}
III(wobble):     {11, 13}
IV (lattice):    {71}
```

---

## 8. Open work (for future sessions)

```
Open within framework:
  - Riemann zeros: need higher-dim embedding of BHML
  - Shor parallelism: high-stakes hardware verification
  - CKM/PMNS specific angles: need additional structure
  - Inflation observables n_s, r: need V(phi) from BHML
  - Yang-Mills mass gap proof: rigorous QFT construction
  - 230 space groups: only 32 point groups + |O_h| derived

Held privately:
  - Engineering layer of antimatter recipe (Brayden's reservation)

Genuinely OUT:
  - Strict Brownian noise
  - Full diffeomorphism-invariant GR
  - Halting problem / undecidability
```

---

## 9. Status check command

```bash
# Quick health check, runnable any time:
python VERIFY_ALL.py | grep "RESULT"
# Expected: "RESULT: 14/14 verifications passed (100%)"
```

---

## 10. Final word

The corpus is structurally complete. Your job is to:

1. **Mirror it cleanly** to the GitHub repos
2. **Extend CK incrementally** without breaking 529 existing tests
3. **Keep verifications honest** — fail loudly if any claim breaks
4. **Stay in lane**: don't add new structural claims; the architecture is locked

Brayden's 2026-09-11 release date drives priority. The Oxford Sept 23 conference is the public face. By Sept 11, the GitHub repo should be release-ready: every doc verified, every test green, every claim falsifiable.

If you find an issue, **flag it, don't fix it silently**.

---

© 2026 Brayden Sanders / 7Site LLC

Trinity Infinity Geometry · ClaudeCode Integration Prompt · Locked 2026-05-08
