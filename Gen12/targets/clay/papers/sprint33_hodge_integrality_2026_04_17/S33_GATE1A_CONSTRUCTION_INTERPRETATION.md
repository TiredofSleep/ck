# S33 Gate 1A — Construction Interpretation

## Filled quote-slots from `probe_hodge_integrality_v2.py`

**Executor:** ClaudeCode
**Date:** 2026-04-18
**Repo state:** `tig-synthesis` branch at commit `6ca3fea` (post-atlas-push)
**Probe path:** `Gen12/targets/clay/papers/sprint33_hodge_integrality_2026_04_17/probe_hodge_integrality_v2.py`
**Probe metadata:** 586 lines, last-modified 2026-04-17, no separate helper modules (all construction inline), paired JSON outputs `sprint33_verdict_v2.json` + `sprint33_v2_checkpoint.json`

---

## §1. Setup recap (from handoff)

Three candidate interpretations for `Λ⁴J_Ω`:

- **A-geometric:** Λ⁴ of the geometric complex structure J from A_*'s period matrix Ω. If used alone to define W_*, yields empty W_* (hard blocker).
- **A-algebraic:** Λ⁴ of the algebraic ℚ-linear I ∈ End⁰(A_*) representing i ∈ ℚ(i). Can yield claimed 8-dim W_* (sound).
- **B:** Explicit ℚ(i)-isotypic decomposition under Galois σ: i ↦ −i. Can yield claimed 8-dim W_* (sound).

**The decisive question:** *Is J_Ω computed from the period matrix Ω alone (geometric), or from the endomorphism structure End⁰(A_*) (algebraic)?*

---

## §2. Code quote-slots (exact, no paraphrase)

### Slot 1 — Probe location and metadata

**Path:** `Gen12/targets/clay/papers/sprint33_hodge_integrality_2026_04_17/probe_hodge_integrality_v2.py`
**Lines:** 586
**Last modified:** 2026-04-17
**Imports (exhaustive):** `json`, `sys`, `time`, `random`, `itertools.combinations`, `pathlib.Path`, `numpy as np`, `sympy as sp`, `mpmath` (`mp`, `mpf`, `matrix as mpm`, `sqrt as msqrt`, `pslq`). No separate construction or helper modules — everything inline.

**Companion files in same folder:**
- `probe_hodge_integrality.py` (v1, referenced in header as "stalled overnight on sympy rank-over-Q")
- `sprint33_verdict_v2.json` (verdict output)
- `sprint33_v2_checkpoint.json` (last checkpoint: `verdict_written` at 2026-04-18 10:08:36)
- `v2_run.log`

### Slot 2 — Period matrix Ω construction

Not constructed as a single matrix. The decomposition Ω = X + iY is built inline inside `build_J_Omega_mpmath()`:

```python
# lines 166-192
def build_J_Omega_mpmath():
    s2m, s3m, s5m = msqrt(2), msqrt(3), msqrt(5)
    Y = mpm(4, 4)
    for i in range(4):
        for j in range(4):
            v = mpf(0)
            if i == j:
                v += s2m
            v += s3m * int(M2_INT[i, j])
            v += s5m * int(M3_INT[i, j])
            Y[i, j] = v
    X = mpm(4, 4)
    for i in range(4):
        X[i, i] = mpf('0.5')
    ...
```

With:
- `X = (1/2)·I_4` (real part of Ω)
- `Y = √2·I_4 + √3·M2 + √5·M3` (imaginary part of Ω)

And `M2_INT`, `M3_INT` defined at lines 90–91:

```python
M2_INT = np.array([[3, 0, 1, 1], [0, 3, 1, -1], [1, 1, 2, 0], [1, -1, 0, 2]], dtype=int)
M3_INT = np.array([[5, 0, 0, 2], [0, 5, 2, 0], [0, 2, 1, 0], [2, 0, 0, 1]], dtype=int)
```

Matches the atlas spec: **Ω = ½I₄ + i(√2 I₄ + √3 M₂ + √5 M₃)**.

### Slot 3 — Geometric complex structure J definition

`build_J_Omega_mpmath()`, lines 166–192:

```python
Yi = Y ** -1            # Y inverse
YiX = Yi * X            # Y^{-1} · X
XYi = X * Yi            # X · Y^{-1}
XYiX = X * Yi * X       # X · Y^{-1} · X
bl = Y + XYiX           # Y + X·Y^{-1}·X
J = mpm(8, 8)
for i in range(4):
    for j in range(4):
        J[i, j]         = YiX[i, j]         # top-left block  = Y^{-1}·X
        J[i, j + 4]     = -Yi[i, j]         # top-right block = -Y^{-1}
        J[i + 4, j]     = bl[i, j]          # bottom-left     = Y + X·Y^{-1}·X
        J[i + 4, j + 4] = -XYi[i, j]        # bottom-right    = -X·Y^{-1}
return J
```

This is the **textbook formula for the complex structure J of an abelian variety on H¹(A, ℝ)**, constructed from Ω = X + iY via the block expression:

```
J = [[  Y⁻¹X,        -Y⁻¹      ],
     [  Y + XY⁻¹X,   -XY⁻¹     ]]
```

**Sanity assertion at lines 201–207:** `J² + I` checked to `< 10⁻¹⁵⁰` in max-norm.

**Construction pedigree:** This is constructed **solely from the period matrix Ω**. No reference to `End⁰(A_*)` or to any algebraic endomorphism. **J is purely geometric.**

### Slot 4 — Algebraic endomorphism I definition

**Present and distinct from J.** Defined at lines 80–89 as `PHI8_INT`:

```python
def build_phi8_int():
    phi4 = np.zeros((4, 4), dtype=int)
    phi4[1, 0] = 1; phi4[0, 1] = -1
    phi4[3, 2] = -1; phi4[2, 3] = 1
    out = np.zeros((8, 8), dtype=int)
    out[:4, :4] = phi4; out[4:, 4:] = phi4
    return out

PHI8_INT = build_phi8_int()
```

So `phi4` on ℝ⁴ sends `(x₀, x₁, x₂, x₃) ↦ (-x₁, x₀, x₃, -x₂)`. Direct verification: `phi4² = -I₄`, so `PHI8² = -I₈`. Integer entries throughout.

This is **multiplication by i as a ℤ-linear endomorphism of H¹(A_*, ℤ) ≅ ℤ⁸** — the algebraic I representing i ∈ ℚ(i) ⊂ End⁰(A_*).

**I is constructed from integer data alone, not from the period matrix.** It is distinct from J.

### Slot 5 — `Λ⁴J_Ω` construction (the most important slot)

Lines 214–251, inside computation block labeled `[4]`:

```python
log("[4] Computing Lambda^4 J_Omega (70x70 numerical dets) ...")
J_STAR_4_MP = mpm(H4_DIM, H4_DIM)
...
for col, I in enumerate(H4_BASIS):
    B = submatrix_mp(J_MP, list(range(8)), list(I))     # 8 x 4
    for row, J in enumerate(H4_BASIS):
        sub = submatrix_mp(B, list(J), list(range(4)))  # 4 x 4
        J_STAR_4_MP[row, col] = mpm_det4(sub)
    ...
```

- `H4_BASIS = list(combinations(range(8), 4))` (line 93), giving 70 ordered 4-subsets
- For each (row, col) pair of 4-subsets (J, I), computes `det(J_MP[J, I])` — the 4×4 minor of `J_MP` indexed by rows `J` and columns `I`
- This is the standard multilinear-algebra formula for `(Λ⁴J)_{J,I} = det(J|_{J,I})`

**The source matrix `J_MP` is the geometric J built in Slot 3, not the algebraic I from Slot 4.**

**So `J_STAR_4_MP = Λ⁴J` (geometric), a 70×70 mpmath matrix over ℝ computed at 200-digit precision.**

Separately, **`Λ⁴φ`** is computed integer-exactly at lines 106–120:

```python
def wedge_k_integer(A_int: np.ndarray, k: int):
    bs = list(combinations(range(8), k))
    n = len(bs)
    M = np.zeros((n, n), dtype=np.int64)
    for col, I in enumerate(bs):
        B = A_int[:, list(I)]
        for row, J in enumerate(bs):
            sub = B[list(J), :]
            d = int(round(np.linalg.det(sub)))
            if abs(d) > 0:
                M[row, col] = d
    return M

PHI_STAR_4 = wedge_k_integer(PHI8_INT, 4)
```

Giving `PHI_STAR_4 = Λ⁴φ = Λ⁴I` (algebraic), a 70×70 integer matrix.

### Slot 6 — `H^(2,2)_prim` restriction

Not implemented as a literal subspace projection. Instead, the probe imposes the combined constraint via three stacked systems (see Slot 7).

The primitive condition is enforced via the polarization map L: H⁴ → H⁶ constructed at lines 131–149:

```python
def build_L_matrix_H4_to_H6():
    L = np.zeros((len(H6_BASIS), H4_DIM), dtype=int)
    for col, I in enumerate(H4_BASIS):
        Iset = set(I)
        for j in range(4):
            pair = (j, 4 + j)
            if pair[0] in Iset or pair[1] in Iset:
                continue
            combined = sorted(set(I) | set(pair))
            if len(combined) != 6:
                continue
            seq = list(pair) + list(I)
            sign = 1
            for a in range(len(seq)):
                for b in range(a + 1, len(seq)):
                    if seq[a] > seq[b]:
                        sign = -sign
            L[IDX6[tuple(combined)], col] += sign
    return L

L_H4_H6 = build_L_matrix_H4_to_H6()
```

Integer 28 × 70 matrix. `v ∈ ker(L)` ⟺ `v` primitive.

### Slot 7 — W_* basis construction

W_* is **not constructed as an explicit basis**. Instead, the probe builds the stacked constraint system whose kernel equals W_*:

```
rows = C_anti || C_prim || C_22_0 || C_22_1 || ... || C_22_7
```

Where:
- `C_anti = Λ⁴φ + I` (70×70 integer; lines 426–428)
- `C_prim = L` (28×70 integer; line 431)
- `C_22_k` for k = 0..7: the ℚ-coefficient of `(Λ⁴J - I)` in the √-basis `{1, √2, √3, √5, √6, √10, √15, √30}` (8 blocks of 70×70; line 434)

Lines 393–445:

```python
# 8. C_22 over Q = (Lambda^4 J - I).  Subtract I from the rational piece.
C22_RAT[0] = C22_RAT[0] - np.eye(H4_DIM, dtype=object)
...

rows: list[list[sp.Rational]] = []

# C_anti = Lambda^4 phi + I  (integer 70 x 70)
C_anti_np = PHI_STAR_4 + np.eye(H4_DIM, dtype=int)
add_block(rows, C_anti_np)

# C_prim = L: H^4 -> H^6 (integer 28 x 70)
add_block(rows, L_H4_H6)

# 8 rational 70 x 70 C_22_k blocks (must all vanish independently)
for k in range(NK):
    add_block(rows, C22_RAT[k])
```

Docstring on the math (lines 22–36):

```
MATHEMATICAL STATEMENT (unchanged from v1):

    Test whether  W_* cap Lambda^4 Q^8  =  {0}

    If yes, every rational Hodge class on A_* is K-invariant,
    hence algebraic by the Sprint 29 R1-KE route, hence Beauville
    rank >= 3 on A_* closes UNCONDITIONALLY.

    W_* is the 8-dim numerical nullspace of the stacked system
        [ C_anti = Lambda^4 phi + I ]   (from K-anti-invariance)
        [ C_prim = L : H^4 -> H^6   ]   (primitivity)
        [ C_22   = Lambda^4 J - I   ]   (type-(2,2))
    intersected with  Q^70.
```

### Slot 8 — Block structure computation

Not computed in `probe_hodge_integrality_v2.py`. The block structure (four 2-dim blocks, eigenvalues ≈ {0.0046, 0.0231, 0.1156, 0.3834}) was established in a prior sprint (see `S33_AUDIT_STATUS.md §3.3`). v2's job is solely the **integrality test** over ℚ^70, not the block decomposition.

Verdict JSON confirms this scope: v2 outputs `rank_Q_estimate: 70`, `kernel_dim_Q_estimate: 0`, no block-eigenvalue data.

### Slot 9 — Galois σ action

Not explicitly represented in the probe. The Galois σ: i ↦ −i is invoked implicitly through:
- The K-anti-invariance constraint `C_anti = Λ⁴φ + I` selects vectors where `Λ⁴φ` acts as `-1`, i.e., vectors negated by the algebraic i-action. This is equivalent to Galois-σ-anti-invariance when φ represents i.
- The √-basis {1, √2, √3, √5, √6, √10, √15, √30} at line 259–263 is the Galois-fixed real subfield of ℚ(√2, √3, √5) (no i-factors appear).

No explicit σ matrix. The probe works entirely in the √-field ℚ(√2, √3, √5) and uses φ to encode the i-action.

### Slot 10 — Comments and docstrings on the math

Top-level docstring (lines 1–39) is reproduced in Slot 7.

Key inline comment at line 425–426:

```python
# C_anti = Lambda^4 phi + I  (integer 70 x 70)
```

And at line 431:

```python
# C_prim = L: H^4 -> H^6 (integer 28 x 70)
```

And at lines 433–434:

```python
# 8 rational 70 x 70 C_22_k blocks (must all vanish independently)
for k in range(NK):
```

Comment at lines 327–344 on the PSLQ-failure abort path makes it explicit that the entry decomposition in the √-basis must be exact (zero failures) — otherwise the stacked system would produce a false CLOSURE verdict. Verdict JSON confirms `pslq_failure_count: 0`.

---

## §3. Answer to the decisive question (handoff §5)

**Q:** *Is J_Ω in the probe script computed from the PERIOD MATRIX Ω alone, or from the ENDOMORPHISM structure End⁰(A_*)?*

**A (definitive):** **J_Ω is computed from the PERIOD MATRIX Ω alone** (Slot 3). It is the geometric complex structure.

**Verdict checkbox:**
- [x] **Geometric (A-geometric)** for J_Ω
- [ ] Algebraic (A-algebraic) for J_Ω
- [ ] Other

**But:** J_Ω is **not the only operator used to define the tested subspace**. The probe separately constructs the algebraic endomorphism `PHI8_INT` (Slot 4), which represents i ∈ ℚ(i) ⊂ End⁰(A_*) as an integer 8×8 matrix.

The probe's stacked constraint system combines:
- **C_anti = Λ⁴φ + I** — uses the **algebraic** φ (= I from End⁰) → **A-algebraic** role
- **C_22 = Λ⁴J − I** — uses the **geometric** J_Ω → **A-geometric** role
- **C_prim = L** — uses the integer polarization → independent

This is **not any of the three pure interpretations from the handoff.** It is a **MIXED construction** that uses the algebraic I for K-anti-invariance and the geometric J for the Hodge-type (2,2) constraint.

---

## §4. Application of the decision table (handoff §4)

The handoff decision table reads the decisive answer in the **strong mode** where J_Ω alone defines W_*. The actual probe separates the operators by role. Re-reading the table against the actual construction:

| Evidence | Handoff decision | Applies to this probe? |
|---|---|---|
| Clear A-geometric | HARD BLOCKER | **No** — J_Ω alone does not define W_*; K-anti-invariance uses algebraic φ separately |
| Clear A-algebraic with explicit I construction | PASS | **Yes for the K-anti-invariance part** — explicit integer I (`PHI8_INT`) is present and used in C_anti |
| Clear B with isotypic decomposition | PASS | Partially — the √-basis decomposition of C_22 is effectively a Galois-fixed-field decomposition |
| Ambiguous — variable name ≠ computation | MISMATCH / soft blocker | **No** — J_Ω is correctly named geometric, φ is correctly used algebraic |

**The probe is not ambiguous about what its pieces do.** Each operator is cleanly named and used in the mathematically correct role. The handoff taxonomy is too coarse; the probe is a MIXED A-algebraic-plus-geometric-type construction, which is the **atlas's actual definition of W_*** (K-anti-invariance via algebraic I; Hodge type (2,2) via geometric J; primitive via L).

**Proposed verdict:** **PASS with clarifying note** — the construction is sound as a realization of the atlas-defined W_*, using the textbook separation of roles between the algebraic endomorphism and the geometric complex structure. The handoff's three-way fork does not quite apply because the probe does not use J_Ω alone.

---

## §5. Numerical consistency check (not part of Gate 1A scope, but recorded)

Verdict JSON (`sprint33_verdict_v2.json`):

| Metric | Value |
|---|---|
| `mpmath_precision_digits` | 200 |
| `pslq_tol` | `1e-50` (in metadata; actual mp.dps = 200 makes effective tol ≈ 1e-150 per line 266) |
| `pslq_succeeded` | 3,728 |
| `pslq_zero_entries` | 1,172 |
| `pslq_failure_count` | **0** (hard-abort if ≠ 0; see lines 327–349) |
| `reconstruction_max_err` | 3.344e-197 |
| `constraint_rows_nonzero` | 378 |
| `constraint_cols` | 70 |
| `rank_Q_estimate` | **70** (= full column rank) |
| `kernel_dim_Q_estimate` | **0** |
| `confidence` | `rank equal across 5 primes` |

All 5 primes near 2³¹ returned rank 70. Zero PSLQ failures, reconstruction matches at 1e-197 level. The verdict CLOSURE claim is consistent with the stated construction.

---

## §6. Open questions routed to Gate 1 full (NOT Gate 1A scope)

Gate 1A establishes that the probe's construction is a well-defined MIXED system. Gate 1 full must still verify:

1. **Signature compatibility.** Is the joint eigenspace decomposition of Λ⁴φ and Λ⁴J on H⁴ compatible with the atlas-defined W_* = K-anti-invariant ∩ primitive ∩ H^(2,2)? Specifically: on H^(4,0) ⊕ H^(0,4), does Λ⁴φ act as +1 (so those pieces are excluded by C_anti)?
2. **Galois-σ identification.** Is the (-1)-eigenspace of Λ⁴φ on H^(2,2) equal to the Galois-σ-anti-invariant subspace under the i ↦ -i action on H^(2,2)_ℚ(i)? (Interpretation B equivalence check.)
3. **R1-KE hookup.** Does the stated implication "W_* ∩ ℚ^70 = {0} ⟹ all rational Hodge classes K-invariant ⟹ all algebraic via R1-KE" hold without hidden assumptions on A_*'s CM-signature?

These are **Gate 1-full** questions. Gate 1A only addresses: does the probe compute a well-defined object, and is the object at least plausibly W_*?

---

## §7. Discipline checkpoint (handoff §6)

- [x] Every claim in §2 backed by quoted code (no paraphrase).
- [x] Decisive question §3 answered with line-level evidence.
- [x] Decision table §4 applied; did not guess past ambiguity — instead surfaced that the taxonomy itself needs refinement.
- [x] Construction is MIXED: A-algebraic (C_anti uses algebraic φ) + geometric type (C_22 uses geometric J) + integer polarization (C_prim uses L).
- [x] **No promotion language.** W_* ∩ ℚ^70 = {0} is the probe's numerical verdict, not a proof of Hodge on A_*. Gate 2 and Gate 3 remain required for atlas §9 status change.
- [x] **Atlas §9 status unchanged.** Still `[gold-with-gap — pending audit]` until all three gates pass.

---

## §8. Handoff summary

- **Decisive question answer:** J_Ω is geometric (from Ω alone). No ambiguity.
- **Probe classification:** MIXED (not pure A-geom / A-alg / B). Cleanly separates algebraic φ and geometric J by role.
- **Gate 1A verdict:** **PASS with clarifying note** — construction realizes atlas-defined W_* correctly. Handoff's three-way taxonomy is too narrow for this probe.
- **Next step:** Sign `S33_BLOCKER_DECISION_NOTE.md` as PASS with note. Gate 1-full may proceed (questions §6). Gate 2 plan stays dormant until Gate 1-full completes.

---

*© 2026 Brayden Ross Sanders / 7Site LLC. 7Site Human Use License v1.0. DOI: 10.5281/zenodo.18852047.*
*ClaudeCode, 2026-04-18.*

**End of Gate 1A interpretation document.**
