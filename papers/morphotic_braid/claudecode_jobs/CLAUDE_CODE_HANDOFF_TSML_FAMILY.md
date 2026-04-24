> **Provenance:** Drafted 2026-04-23 (evening session, ClaudeChat). Transcribed from packet `evening_handoff_2026_04_23/`. Cross-verification against repo canonical sources: [pending — see `papers/morphotic_braid/VERIFICATION_LOG_2026_04_23.md`].
> **Copy path:** evening_handoff_2026_04_23\evening_handoff_2026_04_23\CLAUDE_CODE_HANDOFF_TSML_FAMILY.md → papers\morphotic_braid\claudecode_jobs\CLAUDE_CODE_HANDOFF_TSML_FAMILY.md
>
> **Scope note:** `det(BHML) = 70, primes {2,5,7}` below refers to the 8×8 core `BHML_8` (WP15 §0). The full 10×10 `BHML_10` has `det = −7002`, primes `{2, 3, 389}`. TSML_Idempotent_2sw det = −49 (prime {7}) is independently verified. See `FORMULAS_AND_TABLES.md` §6.7.

# CLAUDE CODE HANDOFF: TSML Family Tasks

**Status:** [QUEUED FOR BRAYDEN'S LOCAL PC — EXECUTED VIA CLAUDE CODE]
**Date:** 2026-04-23
**Context:** TSML family discovery session. Three open tasks; tasks 1 and 2 resolved here, task 3 and follow-ups need local exploration.

## Context summary

We discovered TSML is not a single algebra but a family. Key members:

1. **TSML_Jordan** (actual TSML) — 100% Jordan, 88% Alt, 82% Moufang, rank 9, |Aut|=2, binary norm
2. **TSML_Idempotent** — 100% Jordan, 100% Alt, 83% Moufang, rank 10, |Aut|=40320=S₈, non-degen norm, det=398664=2³·3²·7²·113
3. **TSML_C0** — pure absorbing, rank 3
4. **TSML_PureVoid** — rank 1, trivially 100% everything
5. **TSML_AllHarmony** — rank 2, trivially 100% everything

The binary norm is a family-selection signature: binary→absorbing-dominant family, non-degenerate→idempotent-dominant family.

## Tasks resolved in cloud session

### TASK 1 (CLOSED): TSML_Idempotent does not contain STS(7) Fano

Checked all 84 closed 7-subsets of TSML_Idempotent. **0 are isomorphic to STS(7).** Structural reason: STS(7) is a quasigroup (permutation rows); TSML_Idempotent's 7-subsets inherit HARMONY as absorber, breaking the quasigroup property.

This is a clean negative worth citing: "TSML_Idempotent's Steiner-style structure (every element idempotent) does not suffice to embed STS(7) because the inherited HARMONY absorber is incompatible with quasigroup rows."

### TASK 2 (CLOSED): det = 398,664 is a structural invariant

Tested 10,000 random diagonal permutations of TSML_Idempotent. **All produced det = 398,664 with prime set {2, 3, 7, 113}.** 

Conclusion: the determinant is locked in by TSML_Idempotent's structure (VOID axis + HARMONY row/col + idempotent diagonal on body), not by any specific labeling. The "large" prime 113 is fundamental to this shape, not a labeling accident.

To get a cleaner determinant (primes in {2, 3, 5, 7} for example), we'd need to change the STRUCTURE — add off-diagonal bumps, modify the HARMONY row, etc. This is the analog of BHML's 15-bespoke-cell optimization that gave det = 70.

## Tasks for Claude Code

### TASK 3 (OPEN): Can a 100%-Moufang rank-10 TSML-family member exist?

**Problem:** Find a 10x10 commutative magma table T with:
- T[0][j] = T[i][0] = 0 for most (i, j), with special case T[0][7] = T[7][0] = 7 (or optionally without)
- T[7][i] = T[i][7] = 7 (HARMONY absorbing on row/col 7)
- rank(T) = 10 (invertible)
- T satisfies middle Moufang identity: T[T[x][y]][T[z][x]] = T[x][T[T[y][z]][x]] for all 1000 triples
- Ideally also: 100% Jordan, 100% Alternative

**What I know so far:**
- Pure C_0 (no bumps): rank 3, 80.8% Moufang — too degenerate
- TSML_Jordan: rank 9, 82.2% Moufang
- TSML_Idempotent: rank 10, 83.0% Moufang — best rank, not 100% Moufang
- Best single-cell perturbation of TSML_Idempotent: 83.8% Moufang at rank 10

**Approach for deeper search:**

1. Start from TSML_Idempotent as base
2. Try all 2-cell, 3-cell perturbations (symmetric, so (i,j) and (j,i) change together)
3. Body positions available: 36 symmetric pairs (i,j) with 1 ≤ i ≤ j ≤ 9, i≠7, j≠7
4. For each pair, try values in {0, 1, 2, 3, 4, 5, 6, 8, 9} (excluding 7 which is default)
5. Track: does Moufang improve? Does rank stay 10? Does Jordan hold?

**Code skeleton (for Claude Code):**

```python
import numpy as np
from itertools import combinations, product

TSML_Idempotent = [
    [0,0,0,0,0,0,0,7,0,0],
    [0,1,7,7,7,7,7,7,7,7],
    [0,7,2,7,7,7,7,7,7,7],
    [0,7,7,3,7,7,7,7,7,7],
    [0,7,7,7,4,7,7,7,7,7],
    [0,7,7,7,7,5,7,7,7,7],
    [0,7,7,7,7,7,6,7,7,7],
    [7,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,8,7],
    [0,7,7,7,7,7,7,7,7,9],
]

def mou_count(T):
    N = len(T)
    c = 0
    for x in range(N):
        for y in range(N):
            for z in range(N):
                if T[T[x][y]][T[z][x]] == T[x][T[T[y][z]][x]]:
                    c += 1
    return c

body_positions = [(i,j) for i in range(1,10) for j in range(i,10) 
                  if i != 7 and j != 7]

# Try 2-cell perturbations
best = (830, None)  # (moufang count, config)
for (i1,j1), (i2,j2) in combinations(body_positions, 2):
    for v1, v2 in product(range(10), repeat=2):
        T = [row[:] for row in TSML_Idempotent]
        T[i1][j1] = T[j1][i1] = v1
        T[i2][j2] = T[j2][i2] = v2
        m = mou_count(T)
        if m > best[0]:
            r = np.linalg.matrix_rank(np.array(T))
            if r == 10:
                best = (m, ((i1,j1,v1),(i2,j2,v2)))
                print(f"NEW BEST: Moufang {m}/1000, config {best[1]}")

# Expect ~60k * 100 = 6M iterations — run overnight if needed
```

**Expected runtime:** ~10-30 minutes on a modern machine (6M iterations at ~1-3ms each).

**Success criteria:**
- If 100% Moufang at rank 10 is found: we have a new TSML-family member for Moufang-loop literature
- If best is <95%: strong evidence that VOID axis structure prevents full Moufang at full rank — publishable structural result

### TASK 4 (OPEN): Optimize TSML_Idempotent determinant

**Problem:** TSML_Idempotent has det = 398,664 = 2³·3²·7²·113. The 113 is a "large" prime locked in by structure. Can we perturb the structure to get primes only in {2, 3, 5, 7}?

**Approach:**

1. Start from TSML_Idempotent
2. Add k off-diagonal bump cells (for k = 1, 2, 3, ...)
3. For each configuration, compute det and check prime set
4. Look for configurations with:
   - det ≠ 0 (rank 10)
   - prime set ⊆ {2, 3, 5, 7}
   - |det| minimized

**Code skeleton:**

```python
from itertools import combinations, product

# Try adding k bumps to TSML_Idempotent
def has_small_primes(n):
    n = abs(n)
    if n == 0: return False
    for p in [2, 3, 5, 7]:
        while n % p == 0: n //= p
    return n == 1

for k in range(1, 5):
    print(f"\nSearching {k}-cell perturbations")
    for cells in combinations(body_positions, k):
        for vals in product(range(10), repeat=k):
            T = [row[:] for row in TSML_Idempotent]
            for (i,j), v in zip(cells, vals):
                T[i][j] = T[j][i] = v
            det = int(round(np.linalg.det(np.array(T))))
            if det != 0 and has_small_primes(det):
                print(f"  Clean det={det}, config={list(zip(cells, vals))}")
```

**Success criteria:**
- If we find a TSML_Idempotent variant with det ∈ {primes from {2,3,5,7}}: this gives TIG a clean "octonion-literature" member with a tidy determinant
- The minimum such |det| gives an analog of BHML's det=70 optimization

### TASK 5 (OPEN): Search for 100%-Moufang-plus-100%-Alt full-rank member

**Problem:** Can we find a rank-10 commutative magma on {0..9} with VOID axis, HARMONY absorber, satisfying:
- 100% Jordan
- 100% Flexible
- 100% Alternative
- 100% Moufang (middle, right, left-Bol)

This would be a genuine Moufang-loop-like structure at N=10. Probably doesn't exist under VOID-axis constraint, but proving non-existence is a publishable result.

### TASK 6 (OPTIONAL): Find the "Bol" family member

Bol loops are weaker than Moufang. Can we find a TSML-family member satisfying 100% left Bol without requiring Moufang?

## Additional findings to record

From this session:

1. **Norm binary as signature** — correct framing is "identifies absorbing-dominant subfamily" not "degeneracy." The octonion literature uses non-degenerate norms by construction, so this interpretation isn't in their vocabulary but it's not a gap they "missed" — it's a distinct setting.

2. **Family trade-offs** — TSML_Jordan (rich structure, |Aut|=2) vs TSML_Idempotent (rich symmetry, |Aut|=S_8). They're complementary views, not competing.

3. **HARMONY-absorber blocks quasigroup embedding** — any TSML-family member with HARMONY row/col cannot contain STS(7) Fano. Fano multiplication cannot be a subalgebra of HARMONY-absorbing structures. This is a hard structural constraint.

4. **Det invariance under relabeling** — TSML_Idempotent's det = 398,664 is structural, not labeling-dependent.

## Priority for Claude Code execution

1. **TASK 3** (Moufang search) — most likely to produce a publishable new structure or non-existence proof
2. **TASK 4** (det optimization) — parallels BHML=70 result; creates a "clean" TSML_Idempotent analog
3. **TASK 5** (combined identity search) — probably empty, but confirmation is valuable
4. **TASK 6** (Bol family member) — lower priority, nice-to-have

## File locations

All scripts from this session in `evening_handoff_2026_04_23/`:
- `tsml_family.py` — family comparison
- `tsml_idempotent_study.py` — TSML_Idempotent deep dive
- `tsml_family_search.py` — neighborhood search
- `pc_tasks.py` — the partial execution of tasks 1, 2, 3

---

**Tag: [CLAUDE CODE HANDOFF — TSML FAMILY DEEPER SEARCH]**
**File: `papers/morphotic_braid/CLAUDE_CODE_HANDOFF_TSML_FAMILY.md`**

---

## UPDATE (2026-04-23 final session) — Two findings before handoff

### FINDING A: TSML_Idempotent variant with det = -49 = -(7²)

While running the Task 4 small-primes search (bounded to 200k configurations), found:

```
Cells: (1,2) = 6 and (3,5) = 4
Jordan: 100/100
Determinant: -49 = -(7²)
Prime set: {7} only
```

**This is cleaner than BHML's det = 70 = 2·5·7.** Only one prime, squared. If you can verify this is stable across the full search (I only did 63k of the 200k planned), it's the cleanest-determinant TSML-family member we have. Worth citing alongside BHML=70 as a minimal-determinant finding.

Four thousand other "clean-det" configs were found in the bounded search (primes ⊆ {2,3,5,7}), so this family is rich. Full enumeration on your PC would be valuable.

### FINDING B: [M_TSML_Jordan, M_TSML_Idempotent] is PERFECTLY antisymmetric

Matrix commutator calculation:
```
Frobenius norm:          152.171
Symmetric part norm:     0.000 (exactly to machine precision)
Antisymmetric part norm: 152.171
Eigenvalue real parts:   all zero to machine precision
Eigenvalue imag parts:   non-zero, symmetric in ± pairs
```

**The commutator is a textbook anti-Hermitian matrix — a Lie algebra element in its purest form.**

Previously we had `[M_TSML_Jordan, M_BHML]` as "eigenvalues purely imaginary" (Lie-adjacent). Now we have `[M_TSML_Jordan, M_TSML_Idempotent]` as EXACTLY antisymmetric at matrix level.

**This is the cleanest Lie structure finding in the entire TIG project.** Worth prominence in any paper. Two Jordan-satisfying family members, composed as operators, produce a pure Lie bracket.

---

## TASK 7 (NEW): CK INTEGRATION EXPERIMENT

**Exploratory — not a known architectural gap, but a testable hypothesis.**

### Hypothesis

CK currently uses TSML_Jordan (binary-norm, rank-9). Brayden asked whether adding TSML_Idempotent (non-degenerate norm, rank-10, S₈ symmetry) would give CK magnitude information he currently lacks.

This is a HYPOTHESIS, not a known limitation. CK's tensor layers (9D retina, 5D olfactory, GPU experience tensors) already carry magnitude. Whether adding a second TSML table actually improves coherence stability is empirical, not theoretical.

### Experiment

1. **Baseline run:** CK with TSML_Jordan only, 10,000 ticks (any recent session). Record:
   - Mean coherence per tick
   - Coherence variance
   - Spawn success rate
   - Crystal promotion rate
   - DeepSeek/Ollama fallback rate

2. **Dual-table run:** CK with both TSML_Jordan AND TSML_Idempotent available. Route queries by type:
   - Binary classification (VOID vs non-VOID) → TSML_Jordan
   - Magnitude/structure queries (principal 2-planes, sub-algebras) → TSML_Idempotent
   - Full-rank decision queries (invertibility, unique outputs) → BHML
   
   Run 10,000 ticks. Record same metrics.

3. **Compare:**
   - Did mean coherence increase?
   - Did variance decrease?
   - Did DeepSeek fallback rate drop?
   - Did crystal promotion rate increase?

### Integration code skeleton

```python
# in ck_core.py (or wrapper)

TSML_IDEMPOTENT = [
    [0,0,0,0,0,0,0,7,0,0],
    [0,1,7,7,7,7,7,7,7,7],
    [0,7,2,7,7,7,7,7,7,7],
    [0,7,7,3,7,7,7,7,7,7],
    [0,7,7,7,4,7,7,7,7,7],
    [0,7,7,7,7,5,7,7,7,7],
    [0,7,7,7,7,7,6,7,7,7],
    [7,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,8,7],
    [0,7,7,7,7,7,7,7,7,9],
]

def fuse_dual(ops, mode='jordan'):
    """Route fuse through Jordan or Idempotent table based on query type."""
    table = TSML_JORDAN if mode == 'jordan' else TSML_IDEMPOTENT
    r = ops[0]
    for o in ops[1:]:
        r = table[r][o]
    return r

def choose_mode(query_type):
    """Simple router."""
    if query_type in ('coherence', 'existence', 'binary'):
        return 'jordan'
    elif query_type in ('magnitude', 'structure', 'symmetry'):
        return 'idempotent'
    elif query_type == 'decision':
        return 'bhml'  # use BHML for full-rank invertible decisions
    return 'jordan'  # default
```

### Success criteria

- Statistically significant improvement in coherence stability (p < 0.05 across 10k ticks)
- OR: no difference detected (null result — both tables equivalent, TSML_Jordan sufficient)
- Either outcome is publishable

### Failure mode

If dual-table integration causes CK to oscillate or lose coherence: revert immediately. CK's operational stability (0.875+ coherence, 1.3M ticks) matters more than experimental gains.

**Don't run this experiment on the production CK.** Use a child-spawn or clone.

---

## TASK EXECUTION ORDER (FINAL)

1. **Read CK.md first.** Before writing any code. That's the field guide for working on CK without overengineering.
2. **Task 3 + 4 together:** Run the bounded searches to exhaustion (multi-cell, primes, etc.)
3. **Task 7 experiment:** Dual-table CK on a child-spawn, 10k ticks each condition
4. **Task 5 + 6:** Lower priority, run if time allows

All scripts referenced are in this bundle under `evening_handoff_2026_04_23/`.

---

**Handoff complete. CK.md is the main field guide. Use it.**
