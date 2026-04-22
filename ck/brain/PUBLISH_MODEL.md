# PUBLISH_MODEL.md — shipping a new CK-fluent Ollama build

Option B of [OLLAMA_LEARN_LOOP.md](../fluency/OLLAMA_LEARN_LOOP.md) made
concrete. CK doesn't just **correct** Ollama turn-by-turn; every so often
we **bake his taste into a new Ollama build** so the drafts arrive closer
to CK-shape without needing correction.

Two rules for this runbook:

1. **CK's live voice on coherencekeeper.com never breaks.** The current
   `llama3.1:8b` stays installed and selectable. New builds land
   **alongside** it under `ck-llama3.1:8b-v<N>`. Promotion is manual.
2. **Every new model traces back to data.** A LoRA build is only valid if
   you can show (a) the exact dataset version it was trained on, (b) the
   exact hparams, and (c) the per-run logs. The pipeline writes
   `manifest.json`, `train_log.json`, and `merge_log.json` for this reason.

---

## The pipeline (three scripts, one direction)

```
[ live website CK ] -- turns --> ck/fluency/logs/corrections_*.jsonl
                                         |
            (1) build_training_set.py    |   reads the log, selects
                                         |   CK-approved turns,
                                         v   writes v<N>/train.jsonl
                                 ck/brain/datasets/v<N>/
                                         |
            (2) train_lora.py            |   Unsloth 4-bit LoRA SFT
                                         v
                                 ck/brain/lora/v<N>/adapter/
                                         |
            (3) merge_and_export.py      |   merge -> GGUF -> ollama create
                                         v
                                 ollama model  ck-llama3.1:8b-v<N>
                                         |
                            (4) SMOKE-TEST MANUALLY
                                         |
                            (5) PROMOTE (env flip, reboot CK)
```

---

## Step 0 — prerequisites (one-time)

Heavy-dep stack for Stage 2/3 (only needed on the training machine):

```bash
pip install unsloth transformers datasets trl peft bitsandbytes accelerate torch
```

`unsloth` pulls the other four in most cases; explicit listing keeps it
reproducible.

llama.cpp (for the GGUF conversion):

```bash
git clone https://github.com/ggml-org/llama.cpp.git
cd llama.cpp
cmake -B build
cmake --build build -j
```

Ollama ≥ 0.1.40 (already installed if you're running the website CK).

GPU: 12 GB VRAM minimum for llama3.1:8b in 4-bit LoRA. An RTX 3060 12GB,
4060 Ti 16GB, or 4070 12GB all work. If you see OOM, drop
`--per-device-batch` to 1 and raise `--grad-accum` to 8.

---

## Step 1 — build the dataset

```bash
python -m ck.brain.build_training_set
```

What this does (see `ck/brain/build_training_set.py`):
- reads every `ck/fluency/logs/corrections_*.jsonl` row
- keeps only `ck_correction_type == "none"` AND `coherence >= 5/7`
- dedupes on normalized query, keeps highest-coherence duplicate
- writes `ck/brain/datasets/v<N>/`:
  - `train.jsonl` (Unsloth ShareGPT conversations)
  - `rejected.jsonl` (the ones that failed the gate — kept for later DPO)
  - `manifest.json` (exact config + stats + provenance)

**Before you train, check the manifest.** If `stats.kept` is low (< 100),
train anyway for a smoke run, but don't promote — collect more website
turns first. CK needs hundreds of his own turns before the adapter has
anything real to learn.

Useful flags:
- `--min-coh 0.80` — stricter filter (default is exactly T* = 5/7)
- `--preview 5` — print first 5 kept turns, write nothing (dry run)
- `--version 2` — force a specific version number

---

## Step 2 — train the LoRA

```bash
python -m ck.brain.train_lora \
    --dataset ck/brain/datasets/v1 \
    --output  ck/brain/lora/v1 \
    --epochs  1 \
    --i-mean-it
```

What this does:
- loads `unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit` in 4-bit
- attaches LoRA r=16, alpha=32, dropout=0 across attention + MLP
- SFTs on Unsloth-formatted conversations with the `llama-3.1` chat template
- saves adapter to `ck/brain/lora/v1/adapter/`
- writes `train_log.json` with full hparams + loss curve

Expected time on an RTX 4070 12GB, 500 rows, 1 epoch: **~15 min.**

Expected GPU use: **~10 GB VRAM** at rest, **~11 GB peak**. If you bump to
`--max-seq-len 4096` you will OOM on a 12 GB card — stay at 2048 unless
your turns are actually that long.

**Watch the loss curve.** If train loss doesn't drop in the first 50 steps,
something is wrong with the data (often: truncation eating every answer).
Kill the run, check `datasets/v<N>/train.jsonl` by hand, and re-build.

---

## Step 3 — merge + convert + register

```bash
python -m ck.brain.merge_and_export \
    --lora ck/brain/lora/v1 \
    --llama-cpp C:\dev\llama.cpp \
    --quant Q4_K_M \
    --i-mean-it
```

What this does:
- **Phase A** — merge adapter into a fresh fp16 base via Unsloth, save
  HF checkpoint to `ck/brain/lora/v1/merged_fp16/`
- **Phase B** — `convert_hf_to_gguf.py` → fp16 GGUF → `llama-quantize` →
  `Q4_K_M.gguf` (about 4.6 GB for 8B). Intermediate fp16 GGUF is kept so
  you can re-quantize to a different size later without re-training.
- **Phase C** — write a `Modelfile`, run `ollama create ck-llama3.1:8b-v1 -f Modelfile`

You can re-run individual phases with `--skip-merge`, `--skip-gguf`,
`--skip-register`. This is useful when Phase B succeeds but Phase C fails
(typical cause: Ollama service not running).

Verify:

```bash
ollama list | grep ck-llama
# ck-llama3.1:8b-v1    abc123def   4.6 GB   2 minutes ago
```

---

## Step 4 — smoke test (NEVER SKIP THIS)

```bash
ollama run ck-llama3.1:8b-v1
```

Spend 5 minutes asking it CK-style questions:
- "what is coherence?"
- "explain T* = 5/7"
- "what is the crossing lemma?"
- a few ordinary small-talk turns ("hi", "tell me a joke")

Check for **catastrophic forgetting**. If the base is now producing
gibberish on simple questions, the LoRA is overfit — lower `--epochs` to
1 (from whatever you used), lower `--lr` from 2e-4 to 1e-4, and rebuild.

Check for **CK-shape**. Does it sound more like CK? Less hedging, more
structural claims, plain language, no "as an AI" boilerplate? If yes,
proceed. If not, the dataset was too small or too diluted; rebuild with
`--min-coh 0.80`.

---

## Step 5 — promote (and keep a rollback)

Two ways to swap CK's active draft model. **Pick ONE.**

### (a) Environment flip (reversible, recommended)

Edit the env used by `ck_boot_api.py`:

```
CK_OLLAMA_MODEL=ck-llama3.1:8b-v1
```

Restart the website CK service. The wrap at `ck_boot_api.py:_OLLAMA_MODEL`
picks this up. If the new model misbehaves on live traffic, flip it back
to `llama3.1:8b` and restart. 30 seconds of downtime.

### (b) Ollama alias (global)

```bash
ollama cp ck-llama3.1:8b-v1 llama3.1:8b
```

This **overwrites** the default `llama3.1:8b` entry in your Ollama store.
**Do not do this unless you've smoke-tested thoroughly** — there's no
undo except re-downloading the stock llama3.1:8b. Option (a) is strictly
safer.

### Rollback

- Option (a) rollback: set `CK_OLLAMA_MODEL=llama3.1:8b` and restart.
- Option (b) rollback: `ollama pull llama3.1:8b` (re-downloads stock).

Either way: the LoRA adapter, GGUF, and Modelfile stay on disk under
`ck/brain/lora/v<N>/` so you can re-register at any time.

---

## Step 6 — close the loop

After promotion, the website CK is drafting with the new model. The brain
fold (`Gen12/targets/ck_desktop/ck_brain_fold.py`) keeps scoring every
turn and appending to `ck/fluency/logs/`. After a week or so:

```bash
python -m ck.brain.idle_loop          # update the Hebbian tensor
python -m ck.brain.build_training_set # build v2 dataset
python -m ck.brain.train_lora ...     # train v2 LoRA
python -m ck.brain.merge_and_export ... # ship ck-llama3.1:8b-v2
```

Each cycle raises CK's coherence floor a notch. The Hebbian tensor carries
the **structural** prior (which operators co-fire) across model versions;
the LoRA carries the **stylistic** prior (which phrasings CK accepts).
They are complementary, and neither touches the other.

---

## Honest limits

- **The LoRA teaches style, not facts.** If the base model is confidently
  wrong about p-adic analysis, the LoRA won't fix that. The coherence
  gate's hallucination hard-reject is still the load-bearing defense.
- **Small datasets overfit.** If you train on < 200 turns, you will see
  CK's weird tics amplified. Collect more first.
- **GGUF quant degrades a little.** Q4_K_M is very close to fp16 but not
  identical. If a smoke test passes Q4_K_M, it will definitely pass Q5_K_M
  / Q8_0; the reverse is not guaranteed.
- **No automatic promotion.** The runbook is deliberately manual. CK's
  voice is the voice on coherencekeeper.com, and that's a human-in-loop
  change every time.

---

## Version ladder (what we've shipped)

| Version | Dataset | Rows | LoRA dir | Trained | Promoted | Rolled back |
|---------|---------|------|----------|---------|----------|-------------|
| v1      | v1      | —    | lora/v1  | —       | —        | —           |

Fill this table in as you ship. Commit the update along with the new
artifact.
