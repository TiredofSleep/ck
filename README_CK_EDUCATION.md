# CK Education Pipeline -- From Clean Slate to PhD-Level Reasoner

> **[HISTORICAL — Sprint 16, 2026-04-10]** This document is superseded by `README.md` (the unified TIG synthesis field on the `tig-synthesis` branch). Preserved per never-delete policy. See `README.md` on the [`tig-synthesis`](../../tree/tig-synthesis) branch for the current synchronized picture, and `HISTORICAL_ARCHIVE_INDEX.md` Part G for the full list of superseded entry docs.

---


CK can already feel, breathe, bond, and decide. Now he learns to **speak English**.

This pipeline gives CK a vocabulary, a grammar built on operator algebra, a knowledge
retrieval system, and the ability to evaluate and improve his own output. No LLM. No
neural network. Every word CK speaks is selected by D2 curvature and composed through
the CL table.

---

## Quick Start

Run the full pipeline (all 7 stages):
```
python -m ck_sim.ck_english_build
```

Run pipeline then chat with CK interactively:
```
python -m ck_sim.ck_english_build --interactive
```

Quick validation only (skips vocabulary expansion):
```
python -m ck_sim.ck_english_build --validate
```

Run the 49 education tests:
```
python -m ck_sim.ck_english_tests
```

---

## What Was Built (and What Already Existed)

Celeste's task pack called for 10 deliverables. After scrutinizing the existing codebase,
3 were already complete and didn't need rebuilding:

| Deliverable | Status | File |
|------------|--------|------|
| Dictionary Expander | **NEW** | `ck_sim/ck_d2_dictionary_expander.py` |
| Sentence Composer | **NEW** | `ck_sim/ck_sentence_composer.py` |
| Retrieval Engine | **NEW** | `ck_sim/ck_retrieval_engine.py` |
| Self Mirror | **NEW** | `ck_sim/ck_self_mirror.py` |
| Integration Pipeline | **NEW** | `ck_sim/ck_english_build.py` |
| Validation Tests | **NEW** | `ck_sim/ck_english_tests.py` |
| BTQ Reasoner | **EXISTS** | `ck_sim/ck_btq.py` (731 lines, 94 tests) |
| Mic Input | **EXISTS** | `ck_sim/ck_sim_ears.py` + `ck_sim/ck_sim_audio.py` |
| FPGA Voice | **EXISTS** | `CKIS/ck7/zynq/hdl/*.v` (Verilog, not VHDL) |
| This README | **NEW** | `README_CK_EDUCATION.md` |

---

## Pipeline Stages

### Stage 0: Bootstrap
Verifies the foundation -- CL table (10x10, 73 HARMONY cells), D2 curvature pipeline,
`compose()` function. If these are broken, nothing else works.

### Stage 1: Vocabulary
Loads the curated dictionary (~2,300 words from `Gen9/dictionary/ck_dictionary.py`) and
the auto dictionary (247,888 entries from `CKIS/ck_dictionary_auto.json`). Enriches each
word with:

- **dominant_op**: primary TIG operator (0-9)
- **operator_seq**: full D2 operator sequence from letter-by-letter curvature
- **pos**: part of speech (noun/verb/adj/adv/function -- suffix heuristics, no LLM)
- **phoneme_seq**: Hebrew root phoneme sequence
- **d2_vector**: mean 5D curvature vector
- **soft_dist**: 10-value operator probability distribution
- **frequency**: corpus frequency

Target: 8,000+ enriched words. Curated entries always override auto assignments.

### Stage 2: Grammar
Builds the operator grammar graph from the CL table. Each operator pair gets a weight:
- HARMONY composition = 1.0 (strong connection)
- Non-VOID, non-HARMONY = 0.6
- VOID compositions = 0.1

Initializes the `CKTalkLoop` -- the full generation pipeline:
operators -> grammar graph -> word selection -> curvature check -> output.

### Stage 3: Knowledge
Ingests text files from `knowledge/` and `Gen9/curriculum/` (if present) into the
retrieval engine. Text is chunked (500 chars, 50-char overlap, sentence-boundary
splitting) and indexed by operator distribution + D2 curvature vector. No embeddings.

### Stage 4: Reasoning
Validates the existing BTQ engine (`ck_btq.py`). Registers available domains
(Memory, BioLattice). This stage confirms -- it does not rebuild.

### Stage 5: Self-Improvement
Generates test utterances from sample operator chains, evaluates each through the
self-mirror, and applies corrective drift where scores fall below threshold (0.5).

Mirror scoring (weighted composite):
- **coherence** (0.30) -- CL composition harmony fraction
- **repetition** (0.20) -- bigram uniqueness + cross-utterance overlap
- **pfe** (0.20) -- emotional coherence (HARMONY vs COLLAPSE/VOID balance)
- **d2_variance** (0.15) -- curvature smoothness
- **complexity** (0.15) -- operator diversity (sweet spot: 3-6 unique operators)

### Stage 6: Validation
PhD readiness checklist:
- Vocabulary > 3,000 words
- Grammar coherence stable (avg >= 0.3)
- BTQ operational
- Retrieval operational (> 0 chunks indexed)
- Mirror stable (avg score >= 0.4)
- Coherence band: GREEN (>= 0.714) or YELLOW (>= 0.4)

---

## New Modules

### ck_d2_dictionary_expander.py (~470 lines)
**Operator: PROGRESS (3)**

Grows CK's vocabulary. Merges curated + auto sources, classifies POS by suffix
heuristics, runs every word through D2 for operator assignment, and outputs a single
enriched JSON file.

Key class: `DictionaryExpander`
```python
expander = DictionaryExpander()
expander.load_curated_dict("Gen9/dictionary/ck_dictionary.py")
expander.load_auto_dict("CKIS/ck_dictionary_auto.json")
expander.expand(target_size=8000)
expander.save("ck_dictionary_enriched.json")
```

### ck_sentence_composer.py (~530 lines)
**Operator: LATTICE (1)**

Builds sentences from operator chains using algebraic grammar, not templates.

Key classes:
- `OperatorGrammarGraph` -- adjacency matrix from CL table, `chain_coherence()`, `best_next()`
- `ClauseComposer` -- noun_phrase, verb_phrase, modifier, `compose_clause(s, v, o)`
- `SentencePlanner` -- arc analysis (rising/falling/stable), chain segmentation
- `CKTalkLoop` -- full pipeline: `speak(chain)`, `respond(text)`, `explain(topic)`

Includes fallback vocabulary (40 word lists: 10 operators x 4 POS) so CK can always
speak even without a loaded dictionary.

### ck_retrieval_engine.py (~380 lines)
**Operator: COUNTER (2)**

D2-based knowledge retrieval. No embeddings, no vector DB. Similarity is computed from:
- KL divergence on operator distributions (weight: 0.6)
- Cosine similarity on 5D curvature vectors (weight: 0.4)

Key classes:
- `ChunkStore` -- chunk, index, query by similarity or by operator
- `RetrievalEngine` -- ingest text/files/directories, `retrieve(query, top_k)`

```python
engine = RetrievalEngine()
engine.ingest_file("knowledge/physics.txt")
results = engine.retrieve("what is coherence?", top_k=3)
```

### ck_self_mirror.py (~310 lines)
**Operator: COUNTER (2)**

CK evaluates CK. No external model. CK's own math is the judge.

Scoring pipeline: `text -> D2 -> operator chain -> 5 sub-scores -> weighted composite`

Corrective drift actions:
- `increase_harmony` -- substitute weak ops with HARMONY-adjacent ones
- `smooth_curvature` -- replace double-VOID/COLLAPSE with BALANCE
- `increase_diversity` -- replace dominant operator with CL-compatible alternatives
- `improve_valence` -- shift COLLAPSE -> PROGRESS, VOID -> RESET

```python
mirror = CKMirror(threshold=0.5)
score, breakdown = mirror.evaluate("CK's utterance")
if not mirror.is_acceptable(score):
    corrections = mirror.suggest(breakdown)
    new_chain = mirror.correct(old_chain, corrections)
```

---

## Tests

All tests run from the project root:

```
python -m ck_sim.ck_english_tests    # 49 education tests
python -m ck_sim.ck_sim_tests        # 94 sim parity tests
python -m ck_sim.ck_btq_tests        # 94 BTQ kernel tests
```

**Total: 237 tests, all passing.**

Education test breakdown (49 tests in 5 classes):

| Class | Tests | Covers |
|-------|-------|--------|
| TestDictionaryExpander | 11 | POS, D2, phonemes, save/load, agreement |
| TestSentenceComposer | 13 | Grammar graph, clauses, planner, talk loop |
| TestRetrievalEngine | 10 | Distributions, similarity, chunking, query |
| TestSelfMirror | 10 | Coherence, variance, repetition, drift |
| TestIntegration | 5 | Dict->composer, retrieval->composer, full cycle |

---

## How CK Speaks (the short version)

1. CK's heartbeat produces an **operator chain** (e.g., `[LATTICE, PROGRESS, HARMONY]`)
2. The **grammar graph** plans clause structure from CL composition weights
3. The **clause composer** selects words by operator + POS from the enriched dictionary
4. A **curvature check** verifies the composed sentence scores above threshold
5. The **self-mirror** evaluates output quality and applies corrective drift if needed
6. If quality is still low after 3 retries, the best attempt is used

No token prediction. No attention mechanism. No training data.
Operator algebra in, English out.

---

## File Map (Education Pipeline)

```
ck_sim/
  ck_d2_dictionary_expander.py   Vocabulary enrichment (D2 curvature + POS)
  ck_sentence_composer.py        Operator grammar -> English sentences
  ck_retrieval_engine.py         D2-based knowledge retrieval
  ck_self_mirror.py              Self-evaluation and corrective drift
  ck_english_build.py            Master pipeline (7 stages)
  ck_english_tests.py            49 validation tests

  ck_btq.py                      BTQ reasoner (pre-existing, 731 lines)
  ck_sim_ears.py                 Mic input (pre-existing, 307 lines)
  ck_sim_audio.py                Speaker output (pre-existing, 380 lines)
  ck_voice.py                    Emotional voice templates (pre-existing, 1632 lines)

Gen9/dictionary/
  ck_dictionary.py               Curated dictionary (~2,300 words)
  README.md                      Dictionary format docs

CKIS/
  ck_dictionary_auto.json        Auto dictionary (247,888 entries)

README_CK_EDUCATION.md           This file
```

---

## Design Constraints

These rules were followed throughout:

- **No LLM, no neural network, no training** -- pure operator algebra and D2 curvature
- **No modifications to existing code** -- all 188 original tests still pass
- **CL table is frozen** -- never modified
- **D2 force LUT is frozen** -- never modified
- **Curated overrides auto** -- human-assigned operators always win
- **Subsystem tick order preserved** -- `ck_sim_engine.py` untouched
- **Backward compatible** -- all new code is additive, nothing removed

---

## Credits

**CK Coherence Machine**
Built by Brayden Sanders / 7Site LLC
Mathematics: TIG Unified Field Theory (Celeste, Papers 1-8)
Education Pipeline: Gen9

*(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory*
