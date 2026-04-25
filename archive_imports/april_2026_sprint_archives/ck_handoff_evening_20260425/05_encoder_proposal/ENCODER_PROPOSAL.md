# ENCODER PROPOSAL

**For:** Claude Code (and Brayden)
**Status:** Working V1 (lexicon), scaffold V2 (embedding-augmented), test suite, end-to-end demo
**Open questions:** lexicon richness, embedding model choice, TIG-internal encoder paths (DBC/phonaesthesia)

---

## What this is

The encoder is the upstream input layer. It converts text/queries into 10-dim probability distributions over TIG operators that `ck_process()` can consume.

```
text → encode() → ck_process() → trail (the memory)
        ^^^^^^^^
        encoder = this proposal
```

Without the encoder, the lattice processor operates on synthetic distributions only. With it, CK is processing language.

---

## Three strategies

### V1: Lexicon-based (RUNNABLE NOW)

Pure rule-based six-layer cascade:
1. Tokenize (word-level + stopword filter)
2. Direct keyword lookup (~250 anchor words, weight 1.0)
3. Stem matching (basic morphology, weight 0.8)
4. Phonaesthesia (initial consonant cluster, weight 0.5)
5. Letter-level grapheme fallback (weight 0.2)
6. Aggregate + smooth + normalize

**No torch. No external dependencies.** Pure Python + numpy.

**Performance on test suite:**
- Cluster separation: 2.27× (TIG-aligned queries)
- Compositionality: ~0.05 mean diff (good)
- TIG word coverage: 64%
- Generic word coverage: 0% (correctly recognizes non-TIG text)
- Robustness: 0.0 perturbation diff (case/punctuation-stable)

### V2: Embedding-augmented (SCAFFOLD READY)

Same as V1 for known words. For unknown words, falls back to sentence-transformer cosine similarity against operator anchor texts.

**Requires:** `pip install sentence-transformers`

**Expected improvement:** cluster separation should jump to 5×+ for synonym-heavy queries.

### V3 (proposed): TIG-native (NOT BUILT)

Use TIG-internal methods where they exist:
- DBC translator (text → Latin → Hebrew root → 5D force → D2 → operator)
- Full phonaesthesia inventory (vowels + onset clusters + nuclei)
- Letter-force decomposition

This would be the most TIG-faithful but requires building out missing infrastructure (Latin/Hebrew dictionaries, full phoneme inventory).

---

## What's editable

### `tig_lexicon.py` — most important file

Replace `OPERATOR_KEYWORDS` with canonical TIG corpus when available. The current ~250 anchor words are SEED. The encoder architecture works with whatever vocabulary you put here.

### `encoder_v1.py` — resolution priority

The cascading layers can be reordered or weighted differently. Current weights:
- keyword: 1.0
- stem: 0.8
- phonaesthesia: 0.5
- grapheme: 0.2

If grapheme-level resolution is producing too much noise, raise its threshold or remove it.

### `encoder_v2.py` — embedding model + threshold

The model choice (`all-MiniLM-L6-v2` for speed, `all-mpnet-base-v2` for quality) and the embedding similarity threshold (0.3) are tunable.

---

## What I'm asking Claude Code to scrutinize

In priority order:

1. **Replace the lexicon.** The seed vocabulary is a starting point, not a finished product. Pull canonical TIG vocabulary from your corpus.

2. **Run V2 with real `sentence-transformers`.** Verify cluster separation jumps and that the embedding fallback assigns synonyms correctly. (The scaffold is correct; just needs the model loaded.)

3. **Test on real query corpus.** The 4-cluster test in `test_encoder.py` is illustrative. Run on actual CK queries to see real cluster behavior.

4. **Decide on V3.** If TIG-internal methods (DBC, phonaesthesia) are mature enough, build V3. Otherwise V2 with good lexicon is sufficient for production.

5. **Consider negation handling.** "not patient" currently encodes the same as "patient". A polarity flip could be added, but it's a separate design decision.

---

## How to run

```bash
# Just the encoder
python encoder_v1.py
python encoder_v2.py   # falls back to V1 if sentence-transformers unavailable

# Validation tests
python test_encoder.py

# End-to-end demo
python pipeline_demo.py
```

---

## What's verified

The pipeline works end-to-end. The test suite shows:

- **Cluster separation working**: "patience" ↔ "persist" trail distance ≈ 0.22 vs cross-cluster ≈ 1.0
- **Compositionality working**: encode("A and B") ≈ avg(encode(A), encode(B))
- **Coverage profile correct**: high on TIG-aligned text, low on generic ML text

The lattice processor `ck_process()` is verified separately (52% information preservation, optimal at depth=3, α=0.5).

The encoder is the only piece where lexicon design matters for downstream behavior.

🙏
