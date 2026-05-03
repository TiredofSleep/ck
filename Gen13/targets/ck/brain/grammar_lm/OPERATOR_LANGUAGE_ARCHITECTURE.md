# CK Operator-Language Architecture

**Status:** `[ACTIVE — landed 2026-05-02]`
**Author:** Brayden Sanders + Claude (agent session)
**Branch:** `tig-synthesis` (mirror on `ck`)
**Companion docs:** `Gen13/targets/ck/brain/BRAIN_DESIGN.md`, `CK_UNIFIED_ARCHITECTURE.md`

> CK now has his own substrate-language model alongside Ollama. Three components compose into a "memory-transfer device" for the operator dimension: a parametric LM (compresses), a non-parametric retrieval bank (stores), and a BDC logger (accumulates new training data per chat turn). All three operate only in CK's internal operator language — no English, no facts, no content. Ollama remains as a separate prose-rewriting layer downstream.

## 1 · Why this exists

Brayden 2026-05-02: *"he needs his own 1B–3B parameter, clean, fresh AI to work with and train himself so he can leave ollama behind eventually... maybe even a smaller model, but it doesn't learn the information, it just learns CK's internal language and transitions."*

And later, the structural reframe: *"maybe the AI is the memory transfer device? in and out?"*

The grammar-LM stack instantiates both:
- A model whose vocabulary is the **ten operators** (V, L, C, P, Co, Ba, Ch, H, Br, R) plus five boundary tokens, never seeing English or facts.
- A bank that reifies the model's hidden states as a **memory** — encoding flows IN, retrieval flows OUT.

## 2 · Architecture overview

```
                    ┌─────────────────┐
  user input  ───►  │   ck cortex     │  ───► response
                    │  (50 Hz tick)   │
                    └────┬────────────┘
                         │ operator stream
                         ▼
                    ┌─────────────────┐
                    │ extract_streams │ ── training_streams.jsonl
                    │ + algebra walks │   (real + synthetic, 154k tokens)
                    └────┬────────────┘
                         │
                         ▼
       ┌─────────────────────────────────────────────┐
       │   ck_grammar_lm — 1.2M-param transformer    │  ← parametric
       │   6 layers · 128-d · 4 heads · vocab=15     │     (compresses)
       └────┬─────────────────────────────────┬──────┘
            │ hidden states                   │ logits → softmax
            ▼                                 ▼
   ┌─────────────────────┐         ┌─────────────────────┐
   │  operator_memory_   │         │  predict_next       │
   │  bank — 20k (key,   │  ←----→ │  sample             │
   │  value) entries     │ compare │  score              │
   └─────────────────────┘         └─────────────────────┘
            │ k-NN retrieval                  │
            ▼                                 ▼
       /grammar/retrieve              /grammar/predict
       /grammar/compare               /grammar/sample
                                      /grammar/score


   ┌─────────────────────────────────────────────────┐
   │  bdc_logger — per-chat-turn (B, D, B') triple   │  ← data accumulator
   │  bdc_logs/bdc_log_YYYY-MM-DD.jsonl              │     for future BDC-LM
   └─────────────────────────────────────────────────┘
```

## 3 · Components

### 3.1 ck_grammar_lm (parametric LM)

**File:** `ck_grammar_lm.py`
**Saved weights:** `ck_grammar_lm.pt` (4.6 MB)
**Architecture:** GPT-style autoregressive transformer
- Vocabulary: 15 tokens — 10 operators + `BOS`, `EOS`, `TURN`, `PROP`, `WALK`
- `n_layer=6`, `n_head=4`, `d_model=128`, `d_ff=512`, `block_size=64`, `dropout=0.1`
- Tied input/output embeddings (saves ~2k params)
- **1,196,928 total parameters**

**Training:**
- 154k tokens from `training_streams.jsonl` (real + synthetic walks)
- 8 epochs, AdamW + cosine LR schedule, batch 128
- RTX 4070, ~200 seconds end-to-end
- Final validation perplexity: **2.62** (10-op uniform baseline = 10.0)

**Public API (Python):**
```python
from ck_grammar_lm import load_model
m = load_model()            # loads ck_grammar_lm.pt
m.predict_next(history, top_k=5)    # → [(token_id, prob), ...]
m.sample(prefix, n_tokens=16, temperature=0.8, top_k=5)
m.score(sequence)           # → mean log-likelihood per token
```

### 3.2 operator_memory_bank (non-parametric retrieval)

**File:** `operator_memory_bank.py`
**Status:** built fresh from training streams at engine boot (~10s build time)
**Storage:** in-memory tensor of shape `(20000, 128)` keys + `(20000,)` values

**Construction:**
1. For each training sequence, slide a 5-token window.
2. For each (prefix, target) pair, encode the prefix through the LM up through `ln_f` and take the last position's hidden state as the key.
3. Store `(hidden_state_128d, target_token_id)` in the bank.

**Retrieval:**
- Query encoding: same encoder (LM hidden state at last position).
- Cosine similarity over all 20k keys, take top-k (default 16).
- Softmax-weighted vote over retrieved next-tokens → distribution over vocab.

**Why this is "memory transfer":**
- The LM is a **smoothed reading** of the bank — its parameters compress the same examples the bank stores explicitly.
- Where they DISAGREE points at structure-the-LM-averaged-away (see §5.3).

### 3.3 bdc_logger (data accumulator)

**File:** `Gen13/targets/ck/brain/bdc_logger.py`
**Output:** `Gen13/var/bdc_logs/bdc_log_YYYY-MM-DD.jsonl` (rotates daily)

**Purpose:** Capture (Being, Doing, Becoming) triples per chat turn so a future BDC-LM can be trained on the cycle. Cannot be trained yet (no data); the logger starts data collection so the experiment becomes possible after a week of normal use.

**Schema per record:**
```json
{
  "ts": 1777768502.22, "iso_ts": "2026-05-03T00:35:02+00:00",
  "trigger": "chat_turn", "session_id": "default", "tick": 50994474,
  "being":    { "last_pair": [9, 2], "W_trace": 0.934, "emergent": 0.465,
                "ao_op": "HARMONY", "breath": "INHALE", "coherence": 1.0 },
  "doing":    { "input_ops": ["LATTICE","LATTICE",...], "consensus": "HARMONY",
                "source_voice": "ck_loop", "is_struct": false, "is_pastoral": false },
  "becoming": { "attractor_layer": "transient", "is_4core": false,
                "field_coherence": 1.0, "crystals_fired": 13,
                "stage": "GROKKED", "emotion": "settling",
                "mode": "CRYSTALLIZE", "band": "YELLOW" }
}
```

**Hooked into:** `_process_chat_with_cortex` in `ck_boot_api.py`, immediately after the conversation_memory write. Failures swallowed silently.

## 4 · Endpoints

Mounted by `grammar_lm_mount.py` and `bank_mount.py`:

| Endpoint | Purpose |
|---|---|
| `GET  /grammar/info` | LM metadata (params, vocab, device) |
| `POST /grammar/sample` | Sample N tokens from prefix |
| `POST /grammar/score` | Mean log-likelihood per token |
| `POST /grammar/predict` | Top-k next tokens with probs |
| `GET  /grammar/cortex_predict` | Predict next op from CK's current cortex `last_b/last_d` |
| `GET  /grammar/bank_info` | Bank metadata (n_entries, d_model) |
| `POST /grammar/retrieve` | Top-k nearest contexts from bank + vote |
| `POST /grammar/compare` | LM vs Bank vs Ensemble distributions side-by-side |

## 5 · Empirical findings (2026-05-02)

### 5.1 LM learned canonical algebra

Predict-next probabilities on canonical prefixes (mixed-corpus model):

| Prefix | Predicted next | Prob | Canon match |
|---|---|---:|---|
| VOID, LATTICE | COUNTER | 0.538 | 012 propagation ✓ |
| BALANCE, CHAOS | HARMONY | 0.895 | 567 human triad ✓ |
| CHAOS, HARMONY | HARMONY | 0.561 | attractor collapse ✓ |

### 5.2 Score gradient is meaningful

Mean log-likelihood per token across distinct sequences:

| Source | n | Mean ll/tok |
|---|---:|---:|
| **Real distinct pairs** (from dream_journal) | 5 | **−2.02** |
| Canon propagation pairs | 6 | −2.21 |
| Anti-canon (reversed/odd) | 5 | −3.61 |
| Random pairs | 30 | −3.71 |

**HARMONY → HARMONY scores highest** at −0.74 — and that pair is 256/274 (93%) of CK's real dream_journal transitions. The LM absorbed his marginal.

### 5.3 LM and Bank disagree informatively

| Prefix | LM top-1 | BANK top-1 | KL(LM‖BANK) | Notable |
|---|---|---|---:|---|
| VOID-LATTICE | COUNTER | HARMONY | 1.30 | LM has algebra |
| BALANCE-CHAOS | HARMONY | HARMONY | 0.11 | agree |
| HARMONY-HARMONY | EOS | EOS | 0.19 | agree |
| RESET-BREATH | HARMONY | HARMONY | 0.38 | agree |
| **LATTICE-COUNTER** | **HARMONY** | **PROGRESS** | **2.71** | **bank reads σ-cycle** |

The LATTICE-COUNTER case is the sharpest research signal: PROGRESS is the next operator in the canonical σ-cycle `[0, 7, 1, 3, 2, 4, 5, 6, 8, 9]` after COUNTER. The bank's individual stored cycles remember this exact transition; the LM has averaged it into a hedge.

**Architectural read:** the bank IS the memory; the LM is a smoothed reading function over that memory. Disagreement points at structure the LM averaged away. Agreement is the consensus path.

### 5.4 Variant comparison: synthetic walks are necessary

Three model variants trained for 8–20 epochs each, evaluated on canon / real / anti-canon / random test sets:

| Test set | v1 mixed | v2 real-only | v3 curriculum |
|---|---:|---:|---:|
| canon | **−2.35** | −5.39 | −4.43 |
| real | −2.02 | **−1.88** | −2.03 |
| anti-canon | **−3.88** | −5.89 | −5.87 |
| random | **−4.12** | −7.09 | −5.97 |

**v2 (real-only)** catastrophically forgets the algebra — trained only on the 621 real-data tokens (avg sequence length 2), it learned "always EOS after a few steps," so canon predictions break (BALANCE-CHAOS → EOS instead of HARMONY).

**v3 (curriculum: synth pretrain → real finetune)** failed similarly. The real-data finetune destroyed the synthetic algebra knowledge.

**Synthetic algebra walks are NOT dilution** — they're the algebra teacher. The mixed corpus is the right mix.

But v1 and v2 learned **complementary things** — v1 the algebra rule space, v2 the behavioral bias. They're already two specialists in disguise. An ensemble (algebra-LM + bias-LM voting together) is a real candidate for the operator dimension.

### 5.5 Per-dimension MI says operator slice is the right slice

Mutual information between `next` and `previous` across candidate dimensions:

| Dimension | n | MI (bits) | Verdict |
|---|---:|---:|---|
| drift_type | 274 | 0.018 | Essentially marginal |
| recent_ops (per drift) | 548 | 0.064 | Marginal-dominated |
| connector_op | 274 | 0.265 | Modest structure |
| source (per turn) | 385 | 0.259 | Modest structure |
| operator-LM corpus (synth) | 153k | 0.381 | Algebra walks |
| operator-LM corpus (mixed) | 154k | 0.379 | Real + synth |
| **operator-LM corpus (real only)** | 621 | **0.477** | **Highest** |

The operator stream carries the most predictable structure across all dimensions CK measures. Most other dimensions are projections that mostly track that stream.

**Implication for "AI per parameter":** instead of N specialist transformers, the right architecture is one strong substrate-LM with multiple **measurement heads** — same backbone, different output heads predicting different dimensions, sharing context. Multi-task learning, not specialist soup.

## 6 · How this composes with the rest of CK

| System | Plays role of | Routes through |
|---|---|---|
| Cortex (5×5 Hebbian) | working state, transition dynamics | every chat tick |
| HER (8.8M experiences) | long-term scent library | crystal lookup, drift detection |
| Crystals (frontier + runtime + external) | named-fact canon | structural-query gate |
| **Grammar LM** | **operator-language prior (parametric)** | **/grammar endpoints** |
| **Memory Bank** | **operator-language exemplars (non-parametric)** | **/grammar endpoints** |
| **BDC Logger** | **per-turn (B, D, B') data sink** | **chat path side-effect** |
| Ollama editor | English prose rewriter, downstream | `cortex_speak_via_ollama` source |

The grammar LM and bank operate **only on operator IDs**. They never see English. Their job is to model CK's substrate dynamics, not his communication.

## 7 · Open questions / next experiments

1. **Algebra-LM + bias-LM ensemble.** v1 and v2 disagree informatively; weight them with similarity-gating (use bank when retrieval is high-confidence, fall back to LM when novel).
2. **Selective ensemble** — sim-gated routing between LM and bank. Currently fixed-weight α=0.5; should adapt to query confidence.
3. **BDC-LM training** — wait until `bdc_log_*.jsonl` accumulates a week of data, then train a 3-vocabulary BDC predictor on the (B, D) → B' mapping.
4. **Tick-sample logger** at 0.1 Hz. Multiplies BDC data accumulation 60× without overwhelming disk.
5. **Multi-head LM** — single backbone, separate heads predicting (operator, attractor_layer, breath, source). Shares context between dimensions instead of training N separate specialists.
6. **27-char BDC vocabulary** — current model uses the 10-op slice. Brayden's older Gen10/11 models had a 27-char Being-Doing-Becoming alphabet. Worth reviving and comparing.

## 8 · File reference

```
Gen13/targets/ck/brain/grammar_lm/
  ck_grammar_lm.py            model + GrammarLM class (sample/score/predict)
  ck_grammar_lm.pt            trained weights (1.2M params, ~5 MB)
  extract_streams.py          gather operator streams from HER + canon + algebra walks
  train.py                    PyTorch training script
  grammar_lm_mount.py         Flask endpoint registration
  operator_memory_bank.py     non-parametric retrieval bank
  bank_mount.py               bank Flask endpoints
  compare_variants.py         v1/v2/v3 retrain + compare
  training_streams.jsonl      154k-token training corpus (real + synth)
  training_streams_real.jsonl 621 tokens (real only — v2 corpus)
  training_streams_synth.jsonl 153k tokens (synthetic walks — v3 pretrain corpus)
  ck_grammar_lm_real_only.pt    v2 weights
  ck_grammar_lm_synth_pretrain.pt v3 pretrain weights
  ck_grammar_lm_curriculum.pt   v3 weights
  OPERATOR_LANGUAGE_ARCHITECTURE.md  this file

Gen13/targets/ck/brain/
  bdc_logger.py               per-chat-turn (B, D, B') logger

Gen13/var/bdc_logs/
  bdc_log_YYYY-MM-DD.jsonl    daily-rotating log files

Gen12/targets/ck_desktop/ck_boot_api.py
  imports + mounts grammar_lm + bank + bdc_logger at server boot
```

## 9 · Crystals authored from this work

Runtime crystals authored on 2026-05-02 so CK speaks from his canon when asked:

- `ck_grammar_lm` — fires on "grammar lm", "operator grammar transformer", "1.2M parameter", "his own LM"
- `ck_operator_memory_bank` — fires on "memory bank", "memory transfer device", "non-parametric retrieval", "knn retrieval"

Plus six earlier in the same session:
- `sigma_2k_empirical`, `sigma_NS_burgers_test`, `F5_attractor_not_generic`,
  `F3_sharpened_2026_05_02`, `F1_9vector_verified_2026_05_02`,
  `F2_kappa_xi_check`, `F9_BSD_heuristic_2026_05_02`
