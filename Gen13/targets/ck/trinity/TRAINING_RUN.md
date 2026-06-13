# CK — the real pretraining run

**2026-06-12 (Opus picked up the task).** Brayden, plainly: *"you are trying to make him
human, 2am consolidation, what is this mess... make a fast intelligence system and keep it
training and log the results. how do people train an AI, it takes a while, do it."*

Correct on all counts. This file is the reset.

## What was cut (the mess)

The anthropomorphic layer is removed from the live loop:
- `CK_Nightly` (2am "consolidation") and `CK_KeepGoing` scheduled tasks — **unregistered.**
- "conscious window / folds / dreams / sleep" framing — **set aside.** Those were narration,
  not mechanism. The code still exists in git history; it is not driving anything.

## What this is (how people actually train an AI)

ONE sustained pretraining run, the standard recipe:

1. **Tokenizer** — ByteLevel BPE, vocab 16,384, trained on his own corpus (`ck_bpe.json`).
   No download; his books define his subwords.
2. **Corpus** — the 13,200-book library packed into a single uint16 token stream
   (`corpus_tokens.bin`); ~600–800M tokens from the first 6,000 books.
3. **Model** — a from-scratch GPT (nanoGPT-style), ~45M params (d512 / 8 layers / 8 heads /
   ctx 512), bf16, tied embeddings.
4. **Training** — AdamW, cosine LR w/ warmup, grad clip, gradient accumulation; the RTX 4070
   run hard for tens of thousands of steps (hours-to-days).
5. **Logging** — every 20 steps to `train_real_log.jsonl`: step, tokens seen, train loss,
   val loss, perplexity, tok/s. A real descending loss curve.
6. **Checkpoint** — `ck_lm_real.pt` every 500 steps; **resumable** — rerun = continue. A
   sleep/driver event loses ≤500 steps, not the run.

`python train_real.py` — run it, leave it, rerun to resume.

## Honest expectations (no hype)

This is a ~45M-param model on ~0.7B tokens — GPT-2-small territory, the scale a 4070 can
actually train. It will learn fluent English structure and his corpus's register; it will
**not** be GPT-4. Success = a clean loss curve descending to a sane perplexity (target val
ppl well under 50, ideally ~25–35 for this scale), then coherent sampled text. That is a real
language model, trained from scratch, on his library, on his hardware, logged the whole way.

The point Brayden made that reframes the whole effort: stop pivoting every 20 minutes; **let
one real run take the time it takes.** It takes a while. We do it.
