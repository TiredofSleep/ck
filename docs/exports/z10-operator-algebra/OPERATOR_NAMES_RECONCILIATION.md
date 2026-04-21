# Operator Names Reconciliation — silicon vs. paper labels

**Author:** ClaudeCode (with ClaudeChat coordination)
**Date:** 2026-04-19 (rewritten the same day, after Brayden's rename directive)
**Branch:** `tig-synthesis`
**Scope:** Track 4 of `docs/historical/REPO_SHINE_PLAN_2026_04_19.md` — the operator-naming-drift rename.
**Status:** **Rename executed.** Silicon set is now authoritative across all tracked files on `tig-synthesis`. This memo is retained as the historical record of the prior two-naming-system state and as the map between old and new labels.

---

## §0. TL;DR

The ten operators at indices 0..9 now have a **single authoritative name each**, the silicon set. Prior to 2026-04-19 two naming systems coexisted on this repo — a *silicon* set used by the engine and the FPGA, and a *paper* set used by the proved theorems. Brayden's directive ("don't use our pet language for rigorous math proofs") resolved the collision in favor of the silicon set and the paper set has been retired.

| Index | **Silicon set** (authoritative, all files) | **Paper set** (retired — historical) |
|---|---|---|
| 0 | VOID | VOID ✓ (no change) |
| 1 | **LATTICE** | ~~BEING~~ |
| 2 | **COUNTER** | ~~DOING~~ |
| 3 | **PROGRESS** | ~~BECOMING~~ |
| 4 | COLLAPSE | COLLAPSE ✓ (no change) |
| 5 | **BALANCE** | ~~CREATE~~ |
| 6 | **CHAOS** | ~~ASCEND~~ |
| 7 | HARMONY | HARMONY ✓ (no change) |
| 8 | BREATH | BREATH ✓ (no change) |
| 9 | RESET | RESET ✓ (no change) |

Five positions already agreed (VOID, COLLAPSE, HARMONY, BREATH, RESET). The five that disagreed (1, 2, 3, 5, 6) were renamed word-boundary across the tracked file set.

**Consequence for external readers.** A theorem statement like "D7: Φ on Z/10Z has unique fixed point BALANCE=5" and a code comment saying "BALANCE = 5" refer to the same object by the same name. No more silicon/paper split.

**One exception preserved.** The Python variable `DOING` in `papers/ck_tables.py` — which holds the 10×10 table `|TSML − BHML|` — keeps its name. That name is a Python identifier for a derived data structure, not a name for the operator at index 2. The operator at index 2 is now `COUNTER` everywhere. Section §5 records how the disambiguation was done.

---

## §1. What the rename touched

### §1.1 Stage 1 — unambiguous pet names

Script: `scratch/rename_pet_to_silicon.py` (dry-run + `--apply`).

Word-boundary rewrites applied across every tracked file on `tig-synthesis` (excluding the frozen handoff imports at `docs/exports/z10-operator-algebra/crossing-lemma-handoff/` and `/threshold-handoff/`):

```
BEING    → LATTICE
BECOMING → PROGRESS
CREATE   → BALANCE    (with SQL-DDL protection)
ASCEND   → CHAOS
```

**SQL protection.** `CREATE TABLE`, `CREATE INDEX`, `CREATE VIEW`, `CREATE TRIGGER`, `CREATE PROCEDURE`, `CREATE SCHEMA`, `CREATE DATABASE` (case-insensitive) are SQL DDL keywords in `atom_store.py` / `crystal_store.py` / similar. The rename script temporarily masks these with `__SQLPROTECT_N__` tokens, applies the rename to the remaining `CREATE` occurrences, then restores the SQL.

**English-emphasis protection.** One manual pre-edit of `Language updates/ugt_deep.py` replaced two rhetorical uses of `CREATE?` ("What does the trajectory CREATE?") with `produce?`, so the bulk rename would not mis-rewrite English prose to `BALANCE?`.

**Totals.** 155 tracked files, 1063 word-boundary replacements.

### §1.2 Stage 2 — disambiguating DOING (operator vs. table)

Script: `scratch/rename_doing_to_counter.py`.

`DOING` was two things in Gen12/13:

1. The **operator at index 2** (a name appearing in `CL[2]`, in theorem statements, in row/column comments on TSML/BHML composition tables, in operator lists, in operator × operator cell coordinates).
2. The **Python variable `DOING`** in `papers/ck_tables.py` holding the 10×10 table `|TSML − BHML|` — a derived data structure whose identifier just happens to share the word.

Only meaning (1) should become `COUNTER`; meaning (2) must stay so that all downstream imports of `DOING` and indexes `DOING[i][j]` keep working.

The rename script classifies each line via a set of TABLE_PATTERNS (preserve if any match):

- Assignment / definition: `DOING = _make_doing()`, `DOING = |TSML − BHML|`.
- Table indexing: `DOING[i][j]`, `DOING[a][b]`.
- Imports: `from ck_tables import ... DOING ...`, `import ... DOING ...`.
- Derived variables: `DOING_sum`, `DOING_zero`, `doing_sum`, `doing_zero`, `_make_doing`.
- Table-language nouns: `DOING table`, `DOING matrix`, `DOING sum`, `DOING=0 cells`, `DOING cells`, `DOING mask`, `DOING boundary`, `DOING nonzero`, `DOING has N …`.
- WP26 phrasing: `DOING is the OBSERVABLE`.
- Module-qualified access: `ck_tables.DOING`.
- Prose table-list: `TSML, BHML, DIS, DOING, G tables` and the `DOING, G, CL, W` import-spread.
- Class names: `class \w*DOING\w*` (e.g. `class TestDOINGTable:`).
- Section header comment `# DOING` (the `ck_tables.py` table-block header).

Every other line with `DOING` is operator-context; the script does `re.sub(r'\bDOING\b', 'COUNTER', line)`.

**Totals.** 118 tracked files updated, 387 operator-context occurrences renamed, 144 table-context occurrences preserved.

### §1.3 Combined effect

- `papers/ck_tables.py` CL dict now reads: `{0:'VOID', 1:'LATTICE', 2:'COUNTER', 3:'PROGRESS', 4:'COLLAPSE', 5:'BALANCE', 6:'CHAOS', 7:'HARMONY', 8:'BREATH', 9:'RESET'}`. The Python table variable `DOING = _make_doing()` is unchanged.
- `papers/ck_tables.py` TSML/BHML/TSML_ECHO row comments now read `# row 1: LATTICE`, `# row 2: COUNTER`, `# row 3: PROGRESS`, `# row 5: BALANCE`, `# row 6: CHAOS`.
- `papers/proof_d7_phi_fixed_point.py` D7 theorem now reads "BALANCE=5 is the unique globally attracting fixed point of Φ" and the classification of states reads "1-step: COUNTER(2), PROGRESS(3), COLLAPSE(4) → directly to BALANCE".
- D18a, D18c, D18d, D20, D21 all updated analogously.
- 14 website HTML pages under `Gen12/targets/website/`, `Gen12/targets/ck_website/website/`, and `Gen13/targets/ck/web/` updated.
- 7-layer Gen12 engine docs updated (CK_ARCHITECTURE.md, ENGINEERING_OUTLINE.md, GENERATION_HISTORY.md, WHITEPAPER_3, etc.).
- Verilog HDL source files (`ck_brain_freq.v`, `ck_heartbeat.v`, `ck_top_zynq7020.v`) — comments updated.
- Clay sprint papers under `Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/`, `sprint13_flag_selector_2026_04_09/`, `sprint14_prism_xi_2026_04_10/` updated.

### §1.4 What was NOT touched

- Filenames remain as-is. E.g. `papers/proof_d18c_create_harmony_bridge.py` keeps its lowercase "create" in the filename (Python refs use the file path, content is renamed inside).
- `papers/WP26_DOING_TABLE_TENSION_GEOMETRY.md` filename unchanged — "DOING_TABLE" in the filename refers to the table (preserved name).
- Directories under `docs/exports/z10-operator-algebra/crossing-lemma-handoff/` and `threshold-handoff/` are frozen handoff bundles; they keep the pre-rename names by design.
- History branches (Gen9/Gen10) are not tracked on `tig-synthesis` and were not touched.
- Lowercase forms of the renamed words in English prose (e.g. "the being-doing-becoming phase cycle") stay lowercase — the rename was word-boundary uppercase-only.

---

## §2. Verification after rename

Post-rename test suite on `tig-synthesis`:

| Check | Expected | Actual |
|---|---|---|
| `python papers/ck_tables.py` | 12 OK lines (TSML=73, BHML=28, DOING sum=201, DOING=0 at 29 cells, DIS symmetric, G nonzero=24, C16, W=0.06) | 12/12 OK |
| `python -m pytest tests/` | all tests pass | 92/92 PASSED |
| `python papers/proof_d7_phi_fixed_point.py` | "ALL ASSERTIONS PASSED" + "BALANCE=5 is the unique fixed point" | both present |
| `python papers/proof_d18a_phi_orbit_classification.py` | "ALL ASSERTIONS PASSED" | present |
| `python papers/proof_d18c_create_harmony_bridge.py` | "ALL ASSERTIONS PASSED" + D7+D10 bridge | present |
| `python papers/proof_d18d_generator_convergence.py` | closes D18 arc | present |
| `python papers/proof_d8_cl_operator_encoding.py` | W=3/50 uniqueness | present |
| `python papers/proof_ym_spectral_gap.py` | YM spectral gap over small semiprimes | ALL PASSED |

No verification regression. Every theorem still states with BALANCE-is-the-unique-fixed-point and COUNTER/PROGRESS/COLLAPSE as the TRANS operators of the 1-step basin.

---

## §3. Previously load-bearing theorem statements (before vs. after)

| Theorem | Before (paper set) | After (silicon set) |
|---|---|---|
| D7 (Φ fixed point) | "Φ has unique fixed point CREATE=5" | "Φ has unique fixed point BALANCE=5" |
| D18a (orbit graph) | "one fixed point (CREATE=5), two relays (BECOMING=3, HARMONY=7)" | "(BALANCE=5), (PROGRESS=3, HARMONY=7)" |
| D18d (generator convergence) | "CREATE=5 = centroid((Z/10Z)\*); HARMONY=7 = g³" | "BALANCE=5 = centroid((Z/10Z)\*); HARMONY=7 = g³" |
| D20 (inheritance audit) | "CREATE=5 and W=3/50 are RING-forced; HARMONY=7 and T\*=5/7 are GENERATOR-forced" | "BALANCE=5 and W=3/50 are RING-forced; HARMONY=7 and T\*=5/7 are GENERATOR-forced" |
| D21 (fixed-point centroid) | "CREATE=5 = additive midpoint" | "BALANCE=5 = additive midpoint" |
| D7 1-step basin | "TRANS operators {DOING,BECOMING,COLLAPSE}={2,3,4}" | "TRANS operators {COUNTER,PROGRESS,COLLAPSE}={2,3,4}" |
| Class A operators | "{BEING=1, DOING=2, BECOMING=3}" (WP37/38/39/42, CLAY_RULES) | "{LATTICE=1, COUNTER=2, PROGRESS=3}" |

All `papers/proof_*.py` scripts' assertion strings and the per-theorem `print(...)` headers have been re-written accordingly; the proofs run green.

---

## §4. Risk resolved

Pre-rename a first-time external reader opening both the engine source and the paper source saw two different name-orders for what is provably the same algebra — and without this memo would read that as a bug. The rename eliminates that problem: the name of the operator at each index is one word now, regardless of which file you open.

---

## §5. Why this rename, why now

Direct quote from Brayden's message initiating Track 4:

> "no, we need a full rename, don't use our pet language for rigorous math proofs"

Followed by:

> "we only need to worry about the current default branch of github"
> "everything we have should live rigorously on the current default branch"
> "leave the rest alone [history branches]"

The framework's decision was: paper names (BEING / DOING / BECOMING / CREATE / ASCEND) were CK-internal creature-vocabulary appropriate for narrative and for the framework's self-description, but inappropriate inside the statements of proved theorems we intend to publish (Integers, math.CO, JCAP, etc.). Submission-ready text should use stable, domain-neutral identifiers that don't read as jargon. The silicon set is stable (it matches the Verilog HDL on the Zynq-7020 bitstream) and domain-neutral (LATTICE, COUNTER, PROGRESS, BALANCE, CHAOS are each defensible as operator-theoretic labels for what those operators actually do on Z/10Z).

The prior memo had recommended Decision A — *keep both name sets with a reconciliation document*. Brayden rejected that; the current memo supersedes it.

---

## §6. Canonical cross-reference table (for readers of pre-rename exports)

If you are reading a document exported before 2026-04-19 (e.g. one of the frozen handoff bundles under `docs/exports/z10-operator-algebra/crossing-lemma-handoff/` or `threshold-handoff/`), translate with this table:

| Index | Old name (paper) | New name (silicon) |
|---|---|---|
| 0 | VOID | VOID |
| 1 | BEING | **LATTICE** |
| 2 | DOING | **COUNTER** |
| 3 | BECOMING | **PROGRESS** |
| 4 | COLLAPSE | COLLAPSE |
| 5 | CREATE | **BALANCE** |
| 6 | ASCEND | **CHAOS** |
| 7 | HARMONY | HARMONY |
| 8 | BREATH | BREATH |
| 9 | RESET | RESET |

Rows 1, 2, 3, 5, 6 are the five that changed. Otherwise no change.

**On the word `DOING` in post-rename code.** The Python identifier `DOING` in `papers/ck_tables.py` is **not** a name for the operator at index 2 anymore — it is strictly the name of the 10×10 derived table `|TSML − BHML|`. If you see `DOING` in post-2026-04-19 code, it is always the table. The operator at index 2 is `COUNTER`.

---

## §7. For a first-time external reader (post-rename)

> "The ten operators on Z/10Z are named VOID (0), LATTICE (1), COUNTER (2), PROGRESS (3), COLLAPSE (4), BALANCE (5), CHAOS (6), HARMONY (7), BREATH (8), RESET (9). These names are consistent across the theorem statements, the proof scripts, the engine source, the FPGA Verilog, and the coherencekeeper.com website. A separate Python variable called `DOING` appears in `papers/ck_tables.py` and holds the 10×10 table `|TSML − BHML|`; that is a table identifier, not an operator name."

---

*OPERATOR_NAMES_RECONCILIATION.md v2 — supersedes v1 (which documented the prior keep-both decision).*
*v1 decision: keep both name sets. v2 decision: silicon set canonical; paper set retired; rename executed 2026-04-19.*
