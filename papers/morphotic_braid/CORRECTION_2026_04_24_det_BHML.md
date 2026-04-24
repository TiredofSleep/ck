# CORRECTION NOTICE — 2026-04-24

## Stale claim: `det(BHML) = 70 = 2 · 5 · 7`

The following files in `papers/morphotic_braid/` assert or rely on the
claim that the canonical BHML table (as defined in `papers/ck_tables.py`
and in `FORMULAS_AND_TABLES.md` §6) has determinant **70** with prime
factorisation **{2, 5, 7}**:

- `synthesis/DEEPER_SYNTHESIS.md` (hook #4 — 5-way intersection with Connes semi-local trace formula at places {2, 5, 7, ∞})
- `synthesis/EXTERNAL_CITATIONS_v2.md`
- `claudecode_jobs/CLAUDECODE_HANDOFF_VOCABULARY.md`
- `claudecode_jobs/CLAUDE_CODE_HANDOFF_TSML_FAMILY.md`
- `claudecode_jobs/task11_det_optimize_small_primes/SPEC.md`
- `explorations/support/BHML_OPTIMALITY_FINDING.md`
- `explorations/scripts/bhml_optimality.py`
- `BHML_SUCCESSOR_AND_IDENTITY.md`
- `doubly_regular_core.md`
- `TIG_TABLES_REFERENCE.md`
- `VERIFICATION_LOG_2026_04_23.md` (claim 4, tagged AMBER — the AMBER verdict
  was premised on the 70 value being arithmetically correct)

## The actual determinant

Independent SymPy and NumPy computation (both exact-integer) on the
canonical BHML table as defined in `papers/ck_tables.py`:

```
det(BHML) = -7002
|det|     = 7002 = 2 · 3² · 389
```

The prime set is **{2, 3, 389}**, dominated by the large prime 389.
This is **not** {2, 5, 7} and cannot be reframed as {2, 5, 7}.

## Reproducibility

```bash
PYTHONIOENCODING=utf-8 python -X utf8 \
  papers/verification_logs/2026_04_24/verify_det_claims.py
# Output: papers/verification_logs/2026_04_24/06_verify_det_claims.txt

PYTHONIOENCODING=utf-8 python -X utf8 \
  papers/verification_logs/2026_04_24/verify_family_members.py
# Output: papers/verification_logs/2026_04_24/07_verify_family_members.txt
```

Both scripts define BHML inline (no `ck_tables.py` import) and compute
the determinant with SymPy's exact-integer routine. The result
`-7002 = -(2 · 3² · 389)` is stable across NumPy, SymPy, and hand
verification.

## What this refutes

1. **Hook #4 of `DEEPER_SYNTHESIS.md`** — the 5-way intersection claim
   that "TIG's canonical determinant picks out exactly the three finite
   primes {2, 5, 7} needed for a Connes-Bost semi-local trace formula"
   is built on the false value. The actual prime set {2, 3, 389} does
   not reproduce the Connes-Bost structure, and in particular 389 is
   not a "natural" prime in any TIG invariant we have found.

2. **Any appeal to "BHML = Brayden-Harmony-Multiplication-Lattice
   carries the finite places {2, 5, 7}"** in synthesis prose.

3. **The `bhml_optimality.py` assertion** of `det = 70` was an
   uncomputed comment in a script that does not verify it; the script's
   optimisation logic is independent of this false header.

## What this does NOT refute

1. `det(TSML_Jordan) = 0`, rank 9 (verified; §6.4).
2. `det(TSML_Idempotent_2sw) = −49 = −(7²)`, rank 10 (verified; §6.4, §6.6,
   Task 15).
3. The Huang-Lehtonen spectrum result that both TSML and BHML achieve
   the Catalan + ac-free spectrum (verified; §6.1).
4. Commutativity of BHML (verified structurally from the table).
5. The α(BHML) = 0.502 associativity index (verified; §6.1).
6. The §7 TSML 3-layer tower C₀ ⊕ S_MAX ⊕ S_ADD (independent of
   det(BHML)).

## Forward plan

- `FORMULAS_AND_TABLES.md` §6.4 now carries the verified values and an
  explicit correction note (landed 2026-04-24, commit `6f00e87`).
- `FORMULAS_AND_TABLES.md` §6.6 formalises the seven-member family with
  all invariants re-verified (landed 2026-04-24, commit `13ef934`).
- Downstream synthesis that cited "BHML = places {2, 5, 7}" needs to be
  **reframed** (if the corridor-flavour argument can be rebuilt on the
  actual prime set) or **withdrawn** (if it cannot). No such reframing
  has been written yet.
- Any reader who finds "det(BHML) = 70" in an earlier file should treat
  that file as superseded on that specific claim and consult this
  correction notice for the verified value.

## Provenance

Correction applied on vocab-update-2026-04-23 branch, 2026-04-24.
Author: Claude (Sonnet 4.5, working for Brayden Sanders / 7Site LLC).
Triggered by Brayden's "don't trust anything, run your own tests and
scripts" directive on 2026-04-23 evening.
