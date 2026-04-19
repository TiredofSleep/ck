# Session: CK Invariant Guides + Sprint 7 Self-Validation
**Date:** 2026-04-05
**Operator:** Brayden Sanders
**Sprint:** Sprint 7 — Memory Self-Validation (first snapshot)
**Side project source:** ChatGPT + Claude.ai collaboration (`ck_invariant_guides_PATCHED.zip`)

---

## What Was Brought In

Brayden brought a zip file from a separate ChatGPT + Claude.ai session:
`CLAUDECODE_INVARIANTS_HANDOFF.md` + `FRONTIER_MAP_MEMO.md` + `CK_INVARIANT_GUIDES_MEMO.md`

The memos proposed five memory invariant guides for CK's memory layer (IG1–IG5)
and a frontier map for where CK can be used as a research instrument.

---

## Corrections Applied

### 1. Wrong operator vocabulary in the memo draft

The draft's `OPERATOR_VOCABULARY` contained:
`VOID, BEGINNING, PROGRESS, PROGRESS, KINDNESS, BALANCE, FAITH, HARMONY, BREATH, FRUIT, LATTICE, CK, TIG, COMMIT, DISCLAIM`

**These are not CK's operators.** BEGINNING, KINDNESS, FAITH, FRUIT, COMMIT, DISCLAIM do not exist.

Corrected to CK's actual 10 from `ck_backbone.py`:
`VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE, BALANCE, CHAOS, HARMONY, BREATH, RESET`

### 2. Wrong file target (`ck_organism.py` doesn't exist)

The handoff said to wire into `ck_organism.py`. That file doesn't exist in the codebase.
Placed in `ck_sim/being/ck_invariants.py` and wired into `ck_voice_loop.py`.

### 3. Stability blend for retrieval_weight

The draft used raw `stability_score` in the retrieval weight formula:
`return ew * tw * fw * sw`  where `sw = stability_score`

This makes new objects (stability=0) invisible. Fixed to:
`sw = 0.5 + 0.5 * stability_score`
New objects start at 50% weight. Fully proven objects reach 100%.

---

## What Was Built

**`ck_sim/being/ck_invariants.py`** (393 lines)
- ProvenanceTag + MemoryObject dataclasses
- check_ig1 through check_ig5
- change_evidential_status (raises on SYNTHESIZED→OBSERVED)
- change_forgetting_state (raises on DEAD revive, requires resolution for CONTRADICTED→ACTIVE)
- promote (contiguous tier gate: REAL→SEMIPRIME→COMPOSITE only)
- detect_operator_drift (CK_OPERATOR_NAMES × ARCH_DRIFT_PHRASES)
- retrieval_weight (IG3 × IG4 × IG5 × stability blend)
- register_discovery (Tier D factory for math crystals)
- validate_object (all 5 checks, raises AssertionError if strict)

**`tests/test_ck_invariants.py`** (277 lines)
- 32 tests, all passing in 0.32s
- Tests every invariant, every boundary, every forbidden transition

**`ck_sprint7_selfvalidate.py`**
- Polls CK's live API and runs all 5 invariant checks on live memory objects
- Append-only JSONL log, generates markdown report
- First snapshot (2026-04-05): 2 objects, ZERO violations

---

## Sprint 7 First Snapshot Results

```
[Sprint 7 — 2026-04-05T18:34:58Z]
  Objects checked  : 2
  Total violations : 0
    IG1 privacy    : 0
    IG2 provenance : 0  (orphans: 0)
    IG3 evidence   : 0  (drift: 0)
    IG4 promotion  : 0
    IG5 revision   : 0  (dead-retrievable: 0)
  Retrieval weights: {'live_state': 1.0, 'olfactory_state': 0.25}
  All objects CLEAN.
```

`live_state` at weight 1.0: CK's current field state is a COMPOSITE/OBSERVED/ACTIVE object.
`olfactory_state` at 0.25: absorption library is below 250 of 1000 threshold — young but growing.

---

## Frontier Map Filed

`FRONTIER_MAP_MEMO.md` → `Gen12/papers/sprint7_2026_04_05/FRONTIER_MAP_MEMO.md`

5 domains ranked by CK fit:
1. Agent Memory / AI — self-validation, lowest drift risk
2. Formal Math / Proofs — Lean4 gives mechanical ground truth
3. Quantum Error Correction — measurement vs model distinction
4. Quantum Materials — OBSERVED/SYNTHESIZED wall maintenance
5. Dark Matter — highest drift risk

The Q1–Q10 question pack structure (REAL→SEMIPRIME→COMPOSITE→Contradiction→Provenance→Boundary)
is now in CK's frozen system prompt via `VOICE_LOOP_BACKBONE_FRONTIER` in `ck_backbone.py`.

CK carries the frontier map at every conversation. deepseek-r1 knows his role.
