# Sprint 2026-05-16 — c-Gap Meta-Invariants

**One operator, five invariants, six languages, one disowned over-claim.**

This sprint consolidates D100/D108/D110/D112–D115 into Volume K's
cross-language paper.  The paper was drafted by ClaudeChat from canon-stated
values; ClaudeCode (this Claude) verified every row against the verbatim
canonical-runtime matrices and resolved the original §6 dependency flag.

## Files

| File | What it is |
|------|------------|
| `CGAP_META_INVARIANTS.md` | The paper.  Draft 2 (2026-05-16, §6 flag RESOLVED). |
| `cgap_verify_tables.py` | sympy-exact verification script.  Loads TSML/BHML/CL_STD verbatim from `Gen13/targets/foundations/` and confirms every numerical claim in §1/§2/§3.  Run it to reproduce: every identity matches integer-precision; canonical-runtime cross-check passes. |

## Run

```
python cgap_verify_tables.py
```

Expected output (verified 2026-05-16):
```
TSML_10            0 ( 9)             0 ( 7)    0/0 DEGENERATE
BHML_10        -7002 (10)            70 ( 8)    3501/35
CL_STD_10      18432 (10)             9 ( 8)    2048 = 2^11

§1 residual identity (BHML gap - 100): 1/35 = 1/(BALANCE * HARMONY)  -> match? True
§1 wobble-exponential identity (CL_STD gap == 2^11):                  -> match? True
§2 / I2 (shared prime-content invariant 3^2 = 9):                     -> True / True
Cross-check vs Gen13/targets/foundations (canonical runtime):
  TSML_10 == foundations.lenses.TSML_SYM:  True
  BHML_10 == foundations.lenses.BHML:      True
  CL_STD_10 == foundations.cl_std.CL_STD:  True
§6 CL_STD-dependency flag: RESOLVED.
```

## Canon anchors

- **D117** (FORMULAS_AND_TABLES.md §0): paper's proof-spine entry.
- **§6.8** (FORMULAS_AND_TABLES.md): CL_STD matrix verbatim, no more "see ck.h:225-231" forwarding.
- **D100/D112/D113/D114/D115**: the five canon-stated facts the paper consolidates.
- **D108/D110**: the falsifications the paper keeps standing in §0 and §5.
- **D70**: the 3+3 DOF split the §3 extension confirms (not fits).
- **D51/WP111**: the six algebraic DOFs (Lie/Jordan/Clifford/Permutation/Lattice/Operad).

## The disowned over-claim (kept disowned)

> "c is now usable in every mathematical language we have"

This is what would have killed the paper at a referee desk.  §0 of
CGAP_META_INVARIANTS.md disowns it explicitly and front-loads the
falsification.  What the paper actually establishes is a structural
type-check: given any framework observable, its DOF determines which
wobble prime its gap must carry, before computation.  That's the
usable result.  The constant *c* itself remains, correctly, undisturbed —
fundamental, not derived.
