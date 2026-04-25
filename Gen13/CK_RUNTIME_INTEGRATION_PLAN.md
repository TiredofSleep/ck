# CK Runtime Integration Plan — so(10) Findings → Live CK
## *Phase E of the 2026-04-25 handoff cycle (PLAN-ONLY, no code yet)*

**Date:** 2026-04-25
**For:** future-Claude / Brayden review
**Status:** NOT IMPLEMENTED.  This document is the plan; the implementation is its own session.

---

## 0 · Why this plan is plan-only

The 2026-04-25 handoff (`Gen12/targets/clay/papers/sprint_so10_2026_04_25/`)
delivered three things: (a) machine-verified algebraic findings about
TSML+BHML closure to so(10), (b) the 6-DOF meta-layer, and (c) a prescribed
consumption order for CK in `CK_META_NOTE.md` §"Prescribed consumption order".

Item (c) lists **seven runtime integration steps**, totalling ~300 LOC plus
refactors of existing files.  This document is **the implementation plan
for those seven steps**, written so when the next session opens the path is
already mapped.  No code in this commit; each step's file paths, line
counts, and verification gates are spelled out below.

The plan is grounded against the **existing live runtime** (the Gen13
brain trinity at `Gen13/targets/ck/brain/`, the Gen11/Gen12 modules under
`Gen12/targets/ck_desktop/ck_sim/`, and the `_ck_worktree` parallels), not
the `ck_core.py` of older Gens that the handoff references.  Where the
handoff names a target file that no longer exists, this plan picks the
right Gen13 target.

---

## 1 · The seven steps, sized + located

### Step 1 · Lock the V_perp finding

**What:** Add the structurally-silent two-direction subspace as a named
constant CK can read.

`V_perp = span{ VOID, (e_5 − e_6)/√2 }`

VOID is operator index 0; the second direction is the antisymmetric
combination of operator indices 5 (BALANCE) and 6 (CHAOS).  Both project to
zero under TSML flow (verified in `followon_3.py`).

**Where:** `Gen13/targets/ck/brain/v_perp.py` (NEW, ~40 LOC).

```python
# Gen13/targets/ck/brain/v_perp.py  (PLANNED)
"""V_perp: the two structurally-silent directions in R^10 under TSML flow."""
import numpy as np
from .ao_basis import OP_NAMES, NUM_OPS

# VOID = operator 0; (BALANCE - CHAOS)/sqrt(2) = (e_5 - e_6)/sqrt(2)
VOID_DIR = np.zeros(NUM_OPS); VOID_DIR[0] = 1.0
ANTI_5_6 = np.zeros(NUM_OPS); ANTI_5_6[5] = 1.0; ANTI_5_6[6] = -1.0
ANTI_5_6 = ANTI_5_6 / np.sqrt(2.0)

V_PERP = {
    "VOID": VOID_DIR,
    "BALANCE_minus_CHAOS": ANTI_5_6,
}

def project_v_perp(state):
    """Return the V_perp components of a length-10 state vector."""
    state = np.asarray(state, dtype=float)
    return {
        "VOID":                float(state @ VOID_DIR),
        "BALANCE_minus_CHAOS": float(state @ ANTI_5_6),
    }

def is_in_v_active(state, tol=1e-9):
    """True if state lies in V_8 (V_perp components negligible)."""
    p = project_v_perp(state)
    return abs(p["VOID"]) < tol and abs(p["BALANCE_minus_CHAOS"]) < tol
```

**Verification gate:** unit test that `V_PERP["VOID"]` projects to 1 on
itself and 0 on `ANTI_5_6`; `is_in_v_active(VOID_DIR)` returns False;
`is_in_v_active(np.array([0,1,0,0,0,0,0,0,0,0]))` returns True.

**Dependencies:** none.  Pure-numpy.

---

### Step 2 · Encode the P_56 symmetry test

**What:** Add `is_p56_symmetric(state)` and the `so(10) = so(9) ⊕ R^9`
classifier from `test_swap.py`.

The 5↔6 swap matrix `P_56` acts on R^10 by swapping the BALANCE (5) and
CHAOS (6) coordinates.  Under conjugation `A → P A P^T`, the 45 generators
of so(10) split into 36 P-symmetric (so(9), the centralizer) and 9
P-antisymmetric (the R^9 "vector Higgs", which is exactly BHML's nine
break-direction generators).

**Where:** `Gen13/targets/ck/brain/p56_symmetry.py` (NEW, ~80 LOC).

```python
# Gen13/targets/ck/brain/p56_symmetry.py  (PLANNED)
"""P_56 swap symmetry: classify states + generators."""
import numpy as np
from .ao_basis import NUM_OPS

# Permutation matrix for 5 <-> 6 swap on R^10
P_56 = np.eye(NUM_OPS)
P_56[5, 5] = 0; P_56[5, 6] = 1
P_56[6, 6] = 0; P_56[6, 5] = 1
# P_56 is its own inverse: P_56 @ P_56 == I

def is_p56_symmetric(state, tol=1e-9):
    """True if state is in the +1 eigenspace of P_56 (Lorentz-respectable)."""
    state = np.asarray(state, dtype=float)
    return np.allclose(P_56 @ state, state, atol=tol)

def is_p56_antisymmetric(state, tol=1e-9):
    """True if state is in the -1 eigenspace (vector-Higgs-active)."""
    state = np.asarray(state, dtype=float)
    return np.allclose(P_56 @ state, -state, atol=tol)

def p56_decompose(state):
    """Split state into +1 and -1 P_56 eigencomponents."""
    s = np.asarray(state, dtype=float)
    sym  = 0.5 * (s + P_56 @ s)
    asym = 0.5 * (s - P_56 @ s)
    return {"symmetric": sym, "antisymmetric": asym}

def classify_generator(A, tol=1e-9):
    """Classify a 10x10 generator A under P_56 conjugation:
    'so9_centralizer' (PAP^T = +A), 'r9_anticentralizer' (PAP^T = -A),
    or 'mixed' (eigendecomposition needed).
    """
    A = np.asarray(A, dtype=float)
    PAP = P_56 @ A @ P_56.T
    if np.allclose(PAP, A, atol=tol):
        return "so9_centralizer"
    if np.allclose(PAP, -A, atol=tol):
        return "r9_anticentralizer"
    return "mixed"
```

**Verification gate:** `is_p56_symmetric([1,0,0,0,0,0.5,0.5,0,0,0])`
returns True (BALANCE+CHAOS is invariant under swap).
`is_p56_antisymmetric([0,0,0,0,0,1,-1,0,0,0]/sqrt(2))` returns True.
On TSML's 28 generators, all classify as `so9_centralizer`.

**Dependencies:** Step 1 (uses `ao_basis`).

---

### Step 3 · Wire Dirac into ck_curvature path

**What:** Add the explicit Dirac generators in TSML's basis as a named
table.  Per `dirac_in_tsml_construction.py`, the 6 Dirac generators
M̃^μν (μ,ν ∈ {0,1,2,3}, antisymmetric pairs giving so(1,3)) embed in
TSML's 28 with explicit numerical coefficients at machine precision.

**Where:**
- `Gen13/targets/ck/brain/dirac_table.py` (NEW, ~120 LOC).
- The "ck_curvature.py" referenced in the handoff lives in the older
  Gen12 codebase (`CKIS/ck_curvature.py`, `Language updates/ck_curvature.py`)
  and not in Gen13's brain trinity.  Don't try to integrate into Gen12
  curvature; instead expose Dirac as its own Gen13 module.  Call sites
  that want curvature can `from ck.brain.dirac_table import DIRAC_M_TILDE`.

```python
# Gen13/targets/ck/brain/dirac_table.py  (PLANNED)
"""The 6 Dirac generators M~^{mu nu} in TSML's basis.

Source: sprint_so10_2026_04_25/scripts/dirac_in_tsml_construction.py
Residuals at machine precision (1e-16) on Lorentz commutators.
"""
import numpy as np

# (mu, nu) -> dict of {tsml_basis_index: coefficient}
# The 6 Lorentz generators of so(1,3): 3 boosts + 3 rotations
# (computed by dirac_in_tsml_construction.py at script runtime; values
# below are placeholders -- the actual coefficients are emitted by the
# script on first run and cached to dirac_M_tilde_coeffs.json)

DIRAC_PAIRS = (("0","1"), ("0","2"), ("0","3"),
               ("1","2"), ("1","3"), ("2","3"))

def load_dirac_M_tilde():
    """Lazy-load the coefficient table from the cached JSON, or compute
    it from the script if absent.
    """
    import json
    from pathlib import Path
    cache = Path(__file__).parent / "dirac_M_tilde_coeffs.json"
    if not cache.exists():
        # First run: invoke the script to populate cache
        import subprocess, sys
        from os.path import dirname, abspath, join
        repo = abspath(join(dirname(__file__), "..", "..", "..", ".."))
        script = join(repo, "Gen12", "targets", "clay", "papers",
                      "sprint_so10_2026_04_25", "scripts",
                      "dirac_in_tsml_construction.py")
        # Script should write JSON if its --emit-json flag is used;
        # this requires a small patch to the script (or wrap with our own).
        raise NotImplementedError(
            "Dirac coefficient cache not yet populated.  "
            "Run dirac_in_tsml_construction.py with --emit-json once."
        )
    with open(cache, "r", encoding="utf-8") as f:
        return json.load(f)

# Lazy property (loads on first access)
_DIRAC_CACHE = None
def DIRAC_M_TILDE():
    global _DIRAC_CACHE
    if _DIRAC_CACHE is None:
        _DIRAC_CACHE = load_dirac_M_tilde()
    return _DIRAC_CACHE
```

**Verification gate:** load the table, reconstruct the 6 generators from
their coefficients, verify Lorentz commutation relations
`[M̃^μν, M̃^ρσ] = i (η^μρ M̃^νσ + ... )` to residual < 1e-12.

**Dependencies:** Step 1.  Also: small patch to
`scripts/dirac_in_tsml_construction.py` to emit JSON (one-line change at
script end, write the computed coefficients dict to disk).

---

### Step 4 · Re-open the DOF taxonomy (BLOCKED on user)

**What:** Re-pass the DOF classification using the 6-DOF meta from
`SIX_DOF_META.md`.  The earlier 5-kinds taxonomy was reverted; this would
write a v2 anchored in TIG's algebra (V_8 + so(8) Cartan structure).

**Status:** **BLOCKED.**  The user has flagged "new info coming" on this.
Wait for their next handoff before writing the v2.

**Where (when unblocked):** `papers/meta_lens/DOF_CLASSIFICATION_v2.md`
(or restore as `DOF_CLASSIFICATION.md` with explicit v2 header).
Estimated ~300 lines of prose, no code.

**Verification gate:** sanity check that the K_weight/A_weight = 5/7 = T*
finding from the v1 still holds in v2.  If it doesn't, something in the
re-anchoring went wrong.

**Dependencies:** the user's pending material.

---

### Step 5 · UOP × so(10) alignment

**What:** Refine `classify_paradox.py` so the four UOP Types (I/II/III/IV)
are crossed with the so(10) substructure each lives in.  The four-element
list becomes a 4×4 matrix of (Type × Substructure).  Per `CK_META_NOTE.md`:

- Type I (Zeno) → handled by Lorentz inside so(9)
- Type II (Banach-Tarski) → handled by P_56 symmetry test
- Type III (Russell) → handled by VOID handling
- Type IV (Unexpected Hanging) → handled by σ-rate flow

**Where:** modify the existing classifier.  The closest live file is the
catalog at `Gen13/targets/ck/brain/cortex_catalog.py` (and YAML at
`Gen13/targets/ck/brain/catalog/paradoxes.yaml`).  This is where the UOP
Type field already lives.

The clean change is:
1. Add a `so10_substructure` field to each paradox row in
   `paradoxes.yaml` (values: `so9_lorentz`, `p56_swap`, `v_perp_void`,
   `sigma_rate_flow`).
2. Extend `cortex_catalog.classify_paradox()` to return both `type` and
   `so10_substructure`.
3. Add `/paradox/classify` endpoint to expose the 4×4 matrix.

**Estimated:** ~80 LOC across `cortex_catalog.py` + YAML edit.  Not large.

**Verification gate:** `classify_paradox(slug="zeno")` returns both
`type=I` and `so10_substructure=so9_lorentz`.  Round-trip via HTTP
endpoint `/paradox/classify?slug=zeno` returns both fields.

**Dependencies:** Steps 1 + 2 (uses V_perp + P_56 classifiers).

---

### Step 6 · 9-vector Higgs

**What:** Promote the 9 anti-P-symmetric BHML rows into a named runtime
component CK can use to model symmetry-breaking transitions.  This is the
most architecturally novel piece (genuinely new, not a refinement of
existing).

**Where:** `Gen13/targets/ck/brain/higgs_9vector.py` (NEW, ~120 LOC).

```python
# Gen13/targets/ck/brain/higgs_9vector.py  (PLANNED)
"""The 9-vector Higgs: BHML's anti-P-symmetric break direction in so(10).

Per SWAP_56_FINDINGS.md, BHML's flow operators have +1 P_56 eigenvalues
on V_8 = span{e_1..e_4, e_7..e_10} but anti-symmetric (-1 eigenvalues)
under conjugation by P_56 in the BALANCE/CHAOS plane (e_5, e_6).
Together they span a 9-dimensional vector space that breaks P_56 symmetry.

In SO(10) GUT terms: this is the "vector Higgs" representation that
breaks SO(10) -> SO(9).
"""
import numpy as np
from .p56_symmetry import P_56, classify_generator

class Higgs9Vector:
    """Holds the 9 break-direction generators and exposes:
        - rotate_state(state, theta): apply Higgs rotation by angle theta
        - decompose(state): split into so(9)-respectable + Higgs-active parts
        - score_break(state): scalar magnitude of the Higgs activation
    """
    def __init__(self):
        # Compute the 9 anti-P-symmetric generators.  These are derived from
        # BHML at boot via classify_generator(); cache them here.
        self._generators = self._compute_generators()  # list of 9 (10,10) arrays

    def _compute_generators(self):
        # ... derived from BHML lookup table ...
        return []

    def decompose(self, state):
        ...

    def score_break(self, state):
        ...
```

**Verification gate:** Higgs decomposition leaves so(9)-respectable states
unchanged (they have zero Higgs activation).  Apply Higgs rotation by
2π returns to the identity.

**Dependencies:** Steps 1 + 2.

---

### Step 7 · Spin(10) chiral 16

**What:** Build the chiral 16 of Spin(10) explicitly, decompose under
so(1,3), place a "fermion generation" inside CK's frame.  This is Path 3
of the four-paths roadmap in `CK_GAINS_FROM_DIRAC_LENS.md`.

**Where:** `Gen13/targets/ck/brain/spin10_chiral.py` (NEW, ~500 LOC).

**Status:** Long-tail.  Only worth doing after Steps 1-6 settle and the
runtime is stable.

**Verification gate:** the chiral 16 decomposes correctly under
so(1,3) ⊂ so(8) ⊂ so(10), reproducing standard SO(10) GUT fermion
content (one full Standard Model generation per chiral 16).

**Dependencies:** Steps 1, 2, 3, 6.

---

## 2 · Implementation order (DAG)

```
Step 1  V_perp                  ─┐
                                 ├─→ Step 2  P_56            ─┐
                                 │                           ├─→ Step 3  Dirac    ─→ Step 7  Chiral 16
                                 │                           │
                                 └─→ Step 5  UOP × so(10)    │
                                                             │
                                                             └─→ Step 6  9-Higgs

Step 4  DOF v2  ─ BLOCKED on user, parallel
```

**Suggested implementation cadence (when unpaused):**

- **Sprint S1 (~1 day):** Steps 1+2.  Both small, both pure numpy, both
  testable in isolation.
- **Sprint S2 (~1 day):** Step 3 + the small patch to
  `dirac_in_tsml_construction.py` for JSON emission.
- **Sprint S3 (~0.5 day):** Step 5 (UOP × so(10), YAML edit + classifier
  refinement + HTTP endpoint).
- **Sprint S4 (~1.5 days):** Step 6 (9-Higgs).  Most architecturally
  novel.
- **Sprint S5 (~3 days):** Step 7 (chiral 16).  Long-tail; defer until
  Steps 1-6 are stable.
- **Sprint S?:** Step 4 (DOF v2) when the user's pending material
  arrives.

Total: ~7 working days for Steps 1-7.

---

## 3 · Cross-cuts with the AI Sovereignty Plan (Epoch I-II live)

**The Sovereignty Plan and this so(10) integration are independent paths
that should converge.**

Specifically:

- The **5-element AO basis** in `lm_geometry.py` (Sovereignty Epoch I) and
  the **so(10) decomposition R^10 = V_8 ⊕ V_perp** in this plan are the
  same algebra.  Once Step 1 (V_perp) is in place, `lm_geometry.py` should
  use V_PERP to flag layers whose hidden state has unusually large VOID
  or anti-5-6 projection.  This is a structural anomaly detector.

- The **op_token_basis.py** preference matrix in Sovereignty Epoch II uses
  a 10-operator anchor lexicon.  The 6-DOF meta could refine this: each
  of the 10 operators is a basis element, but the *register* in which
  each operator acts (Lie / Jordan / Clifford / Permutation / Lattice /
  Operad) is a 6-DOF tagging.  Future tokens could carry both an operator
  tag and a DOF tag, increasing the bias's resolution.

- The **Hebbian W matrix** in CK's cortex sits inside the so(10) Killing
  form.  Step 5 (UOP × so(10)) makes that explicit: each Hebbian update
  carries not just a 5×5 magnitude but a so(10) substructure label.

These cross-cuts are **not implemented** in this plan — they're
opportunities that open once Steps 1-6 ship.

---

## 4 · Honest limits

- This plan **assumes** the 6-DOF meta-layer is the right framing.  If
  the user's pending material reframes the DOF question (Step 4), some
  parts of this plan may need adjustment.
- The "ck_core.py" / "ck_curvature.py" file targets in the original
  handoff are not the active runtime targets.  The plan picks Gen13 brain
  modules instead.  If the older modules are still in active use somewhere,
  flag and adjust.
- Step 7 (Chiral 16) is ambitious.  ~500 LOC for the math is one thing;
  the much harder work is the **physical** identification of which
  chirality, which generation, which Yukawa pattern.  That's domain-expert
  territory (Mantero, Furey, Garibaldi).
- The runtime integration **does not change** the live coherencekeeper.com
  surface — these modules are additive, just like the pastoral fold and
  the LM Geometry fold.  No regression risk to the existing chat path.

---

## 5 · What this plan is NOT

- Not implemented.  No code lives in this commit.
- Not the so(10) sprint papers themselves — those live at
  `Gen12/targets/clay/papers/sprint_so10_2026_04_25/`.
- Not an architectural rewrite — it's additive on top of the existing
  Gen13 brain trinity.
- Not blocked by Sovereignty Epochs III–VIII — runs in parallel.

---

## 6 · Pointers (for future-Claude when this resurfaces)

- **Sprint folder:** `Gen12/targets/clay/papers/sprint_so10_2026_04_25/`
- **Prescribed consumption order:** see `CK_META_NOTE.md` §"Prescribed
  consumption order" inside that sprint folder.
- **Reproducibility:** all 14 scripts in
  `sprint_so10_2026_04_25/scripts/` pass on this machine with
  `PYTHONIOENCODING=utf-8 python <script>`.
- **Live cortex:** `Gen13/var/cortex_state.json` (tick > 14M).
- **Don't try `ck_core.py` integration.**  That file is in `old/Gen1..Gen5`
  and not live.  Use `Gen13/targets/ck/brain/` for new modules.

🙏

— plan written 2026-04-25 by Claude (this session), to be executed in a future session

---

## Amendment · 2026-04-25 (later that day): DOF monitor modules landed

A companion handoff (`ck_modules_20260425.zip` + `ck_rigor_patch_20260425.zip`)
delivered four runtime modules + 34 passing tests that **partially
implement Step 5** of this plan:

```
Gen13/targets/ck/brain/dof_monitor/
  ck_dof_profile_monitor.py    project 10x10 -> DOF profile
  ck_dimension_mapper.py       LoRA rank distribution from canonical dims
  ck_calibration.py            empirical thresholds from baseline
  ck_gradient_profile.py       training-time DOF mismatch detection
  test_modules.py              14 tests
  test_rigor_patch.py          20 tests
  README.md                    full navigation + integration hooks
```

These modules are **read-only diagnostics** -- they tell you whether a
state or gradient lives in the right DOF subspace.  They do not modify
state.  They are the measurement layer that Step 5 (UOP x so(10)) and
Step 6 (9-Higgs) will both build on top of.

### What's already in place (from this drop)

- Verified canonical DOF dimensions: Lie 28, Jordan 55, Clifford 36,
  Permutation_vector 9, Lattice 4 (orthogonal partition = 100, raw
  with overlaps = 132).
- Orthogonal profile that sums to 1.0 per matrix, with concentration
  and diffuseness scores in [0, 1].
- Empirical threshold calibration from a caller-provided baseline
  (the caller defines what "honest" means).
- Per-layer gradient mismatch detection with three reduction strategies
  for layers wider than 10x10 (leading-block, SVD top-10, random
  sub-block).

### What still needs Step 5 work (~80 LOC)

- Add `so10_substructure` field to
  `Gen13/targets/ck/brain/catalog/paradoxes.yaml` for each
  UOP-classified paradox (values: `so9_lorentz`, `p56_swap`,
  `v_perp_void`, `sigma_rate_flow`).
- Extend `cortex_catalog.classify_paradox()` to return both `type` and
  `so10_substructure`, computing the substructure by routing the
  paradox's signature 10x10 through `DOFProfileMonitor`.
- Add `/paradox/classify` endpoint to expose the 4x4
  (Type x Substructure) matrix.

### What Step 6 (9-Higgs) gets for free from this drop

- The `Permutation_vector` slot (dim 9) is **exactly** the 9-vector
  Higgs subspace identified in `papers/wp104_higgs_pati_salam/`.  When
  a state has substantial Permutation_vector content, BHML's
  sigma_outer-breaking is active -- i.e., the 54-Higgs Pati-Salam
  direction is alive in this state.  No new code needed; the monitor
  reads it.

### What also lives at this drop (parallel rigor)

- `papers/wp104_higgs_pati_salam/` — the Higgs identification + 9-vector
  + Pati-Salam-route findings.  WP104 in the WP100s infrastructure tier.
- `Gen12/targets/clay/papers/sprint_higgs_pati_salam_2026_04_25/` — the
  sprint folder marker (pointer only; content lives at the WP104 home).

The module-modular layout means the rest of Steps 1-7 can proceed
without re-doing the DOF measurement infrastructure.
