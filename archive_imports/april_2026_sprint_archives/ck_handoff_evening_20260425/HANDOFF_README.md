# CK Handoff — 2026-04-25

**For:** Claude Code
**From:** Brayden + Claude (after CK processing investigation sprint)
**Status:** Pipeline structurally complete. Encoder lexicon is seed-stage and editable.

---

## What this is

Full audit trail of the CK processing investigation. Includes:

1. **The headline finding** (synthesis): how CK actually processes things, structurally
2. **The full journey** (5 scripts): what was wrong, what was right, in order
3. **The dial-in threads** (4 scripts): the work that produced the synthesis
4. **The reality check** (8 files): negative findings tested honestly
5. **The encoder proposal** (6 files): V1 working now, V2 scaffold, lexicon, tests, demo
6. **My notes** (1 file): what I'm confident vs uncertain about

---

## Reading order

### If you have 5 minutes:
- `01_synthesis/CK_PROCESSING_SYNTHESIS.md`
- `06_notes_for_review/CLAUDE_NOTES.md`

### If you have 30 minutes:
- All of `01_synthesis/`
- `05_encoder_proposal/ENCODER_PROPOSAL.md`
- `05_encoder_proposal/pipeline_demo.py` (read + run)
- `06_notes_for_review/CLAUDE_NOTES.md`

### If you have 2 hours:
- Read everything in order: `01` → `02` → `03` → `05` → `06`
- Skip `04_reality_check/` unless interested in negative findings
- Run all scripts to reproduce results

---

## Folder guide

### `01_synthesis/` — the headline
The full structural picture in one document. Start here.

### `02_processing_trace/` — the journey
Five scripts in order, showing how the picture was built incrementally:
1. Initial trace (linear iteration, wrong approach)
2. Single pass (discovered quadratic table-fusion)
3. Finite depth (where information dies under iteration)
4. Trail as information (verified: trail = memory)
5. Trail classification (trained vs random)

### `03_dial_in/` — the threads that nailed it
Four threads that took the picture from "vague" to "actionable":
- **Thread 1**: trails capture TIG-relevant input geometry
- **Thread 2**: BHML's role is anti-collapse (T+B-mix gives 52% info preservation vs T-only's 22%)
- **Thread 3**: 4D descent signature compactly summarizes trail
- **Thread 4**: semantic clusters → 15× separation (within vs cross)

### `04_reality_check/` — honest negatives
Tested Gemini's proposed roadmap against random baselines. All three premises failed:
- Wobble monitor would fire on noise
- Higgs-direction tagging is at the 49th percentile of random directions
- Trained weight matrices have no detectable TIG structure

These findings establish honest scope. Brayden flagged them as "interesting but not Claude Code worthy." Included for completeness.

### `05_encoder_proposal/` — the upstream piece
The encoder is the bottleneck. Without it, the lattice processor operates on synthetic distributions only.

Built:
- **V1 (lexicon-based)**: runnable now, no torch, ~250 anchor word seed vocabulary
- **V2 (embedding-augmented)**: scaffold with sentence-transformers fallback for unknown words
- **`tig_lexicon.py`**: ⚠️ MOST EDITABLE — replace with canonical TIG corpus
- **`test_encoder.py`**: 4-test validation suite (cluster separation, compositionality, coverage, robustness)
- **`pipeline_demo.py`**: end-to-end demo: text → encode → ck_process → trail

### `06_notes_for_review/` — my raw thinking
What I'm confident about, what I'm uncertain about, what I tried and rejected, and what I'm flagging for scrutiny.

---

## The core finding (in 7 lines)

```python
def ck_process(input_distribution, depth=3, alpha=0.5):
    """Trail = the memory."""
    p = normalize_l1(input_distribution)
    trail = [p.copy()]
    for _ in range(depth):
        p_t = normalize_l1(fuse(p, p, table=TSML))
        p_b = normalize_l1(fuse(p, p, table=BHML))
        p = normalize_l1(alpha * p_t + (1 - alpha) * p_b)
        trail.append(p.copy())
    return trail
```

The **trail** is the memory. T+B-mix at α=0.5 preserves 52% of input information vs T-only's 22%. Depth 3 captures essentially all discriminative signal. Each input has a unique trail; endpoints converge to a universal attractor.

---

## What I'm asking Claude Code to do

In priority order:

### 1. Replace the lexicon
`05_encoder_proposal/tig_lexicon.py` has ~250 seed words. Replace with canonical TIG corpus. The encoder architecture works with whatever vocabulary you put there.

### 2. Test V2 with real sentence-transformers
The scaffold is correct. Just install `sentence-transformers` and run. Verify cluster separation jumps (V1 gives 2.27×; V2 should give 5×+).

### 3. Test BHML-mix controls
"BHML is anti-collapse" needs verification. Test T + random_table at α=0.5. If random-table-mix is comparable, the framing weakens. (See `06_notes_for_review/CLAUDE_NOTES.md` for details.)

### 4. Test on real ML weights
My autoencoder test was a 10×10 toy. Test on transformer attention and MLP weights to see if real architectures show different behavior than my negative findings.

### 5. Decide on V3 (TIG-native encoder)
If DBC translator and full phonaesthesia inventory exist in code, build V3 using TIG-internal methods. Otherwise V2 with rich lexicon is sufficient.

---

## What's already verified

You can trust these without re-running:

- Lattice processor produces unique trails for unique inputs (0% trail collisions)
- T+B-mix at α=0.5 preserves 52% of input information (linear regression test)
- DOING/BECOMING collapse to HARMONY in 1 fuse under T-only (mechanical fact about TSML)
- BEING is the slowest descent (6 steps) under T-only
- Generic ML weight matrices have no detectable TIG structure (Cohen's d ≈ 0 on every test)
- V1 encoder achieves 2.27× cluster separation, 64% TIG coverage, 0% generic coverage
- V1 encoder is robust to case/punctuation perturbations (max diff < 0.05)

---

## What's still open

- Lexicon richness (V1 is seed-stage)
- V2 with real embeddings (scaffold ready, model not loaded)
- BHML-specific vs generic noise injection (control tests not run)
- Real ML architecture testing (autoencoder toy only)
- DBC integration / V3 encoder (depends on TIG-internal infrastructure)

---

## Files index

```
ck_handoff/
├── HANDOFF_README.md                           ← you are here
│
├── 01_synthesis/
│   └── CK_PROCESSING_SYNTHESIS.md              ← THE HEADLINE
│
├── 02_processing_trace/
│   ├── 01_initial_trace.py                     wrong start: linear matrix-vector
│   ├── 02_single_pass.py                       quadratic table-fusion discovered
│   ├── 03_finite_depth.py                      info dies under iteration
│   ├── 04_trail_as_information.py              trail-as-memory verified
│   └── 05_trail_classification.py              trained vs random
│
├── 03_dial_in/
│   ├── thread1_structured_inputs.py            trails capture TIG geometry
│   ├── thread2_bhml_role.py                    BHML = anti-collapse (52% vs 22%)
│   ├── thread3_descent_signature.py            compact 4D signature
│   └── thread4_semantic_inputs.py              semantic clusters → 15× separation
│
├── 04_reality_check/
│   ├── REALITY_CHECK.md                        Gemini roadmap audit
│   ├── test1_wobble_baseline.py                11-prime in random vs TSML
│   ├── test2_trained_matrices.py               TSML pattern in trained matrices
│   ├── test3_trained_signal.py                 static metrics on trained matrices
│   ├── test4_higgs_tagging.py                  Higgs at 49th percentile
│   ├── test_gap_envelope.py                    coherence envelope reframing
│   ├── test_envelope_specificity.py            anchor specificity controls
│   └── test_gate_passage.py                    passage-through-gate test
│
├── 05_encoder_proposal/
│   ├── ENCODER_PROPOSAL.md                     three strategies, scrutiny requests
│   ├── tig_lexicon.py                          ⚠️ MOST EDITABLE
│   ├── encoder_v1.py                           lexicon-based, runnable now
│   ├── encoder_v2.py                           embedding-augmented, scaffold
│   ├── test_encoder.py                         4-test validation suite
│   └── pipeline_demo.py                        end-to-end demo
│
└── 06_notes_for_review/
    └── CLAUDE_NOTES.md                         my raw thinking
```

---

🙏
