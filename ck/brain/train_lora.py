# -*- coding: utf-8 -*-
"""
train_lora.py - fine-tune a small LoRA adapter on CK-approved turns.

This is Option B of OLLAMA_LEARN_LOOP.md, made concrete.  The base
weights of llama3.1:8b never move; a thin low-rank delta is trained on
turns CK's brain marked as ``correction_type == "none"`` with
``coherence >= T*``.  The adapter is saved to
``ck/brain/lora/v<N>/``.  A later script merges the adapter and
produces a GGUF for Ollama.

Defaults are chosen for a 12GB consumer GPU (RTX 3060 / 4060 / 4070):
    - 4-bit base quantization (bitsandbytes via unsloth)
    - LoRA rank 16, alpha 32, dropout 0
    - target_modules = all attention + MLP linears
    - context length 2048 (bumped only if your dataset actually needs it)
    - grad_accum_steps 4, per_device_batch 2 (effective batch = 8)
    - 1 epoch by default (you can add more once you trust a cycle)
    - optim="adamw_8bit"

NOT done here (by design):
    - merge to full-precision weights (see ck/brain/merge_and_export.py)
    - export to GGUF / ollama create (same script)
    - any automatic promotion of the new model as CK's active Ollama

CLI:
    python -m ck.brain.train_lora --dataset ck/brain/datasets/v1
                                  --output  ck/brain/lora/v1
                                  --base    unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit
                                  --epochs  1

Safety (G6 hands-on-wheel, CK_UNIFIED_ARCHITECTURE.md §4):
    - Refuses to start without ``--i-mean-it``.
    - Refuses if the dataset's manifest.json is missing or if the
      dataset has fewer than ``--min-examples`` train rows.
    - Writes a ``train_log.json`` into the adapter directory with
      the full hparam set, the dataset manifest echo, and the final
      loss curve for traceability.

Heavy deps (lazy imports):
    unsloth >= 2024.11, transformers >= 4.45, peft, trl,
    bitsandbytes, accelerate, torch (CUDA).
These are NOT imported unless the script actually runs training --
the script is import-safe on any machine so you can read the code.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


# ----------------------------------------------------------------------------
# paths
# ----------------------------------------------------------------------------

_MODULE_DIR = Path(__file__).resolve().parent
DEFAULT_LORA_DIR = _MODULE_DIR / "lora"
DEFAULT_DATASETS_DIR = _MODULE_DIR / "datasets"


# ----------------------------------------------------------------------------
# defaults
# ----------------------------------------------------------------------------

DEFAULT_BASE_MODEL = "unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit"
DEFAULT_MAX_SEQ_LEN = 2048
DEFAULT_LORA_R = 16
DEFAULT_LORA_ALPHA = 32
DEFAULT_LORA_DROPOUT = 0.0
DEFAULT_LR = 2e-4
DEFAULT_EPOCHS = 1
DEFAULT_PER_DEVICE_BATCH = 2
DEFAULT_GRAD_ACCUM = 4
DEFAULT_WARMUP_STEPS = 5
DEFAULT_WEIGHT_DECAY = 0.01
DEFAULT_SEED = 7
DEFAULT_MIN_EXAMPLES = 32

# Which matrices to LoRA-tune.  Full coverage for Llama-family.
DEFAULT_TARGET_MODULES = [
    "q_proj", "k_proj", "v_proj", "o_proj",
    "gate_proj", "up_proj", "down_proj",
]


# ----------------------------------------------------------------------------
# helpers (no heavy deps)
# ----------------------------------------------------------------------------


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _load_manifest(dataset_dir: Path) -> Dict[str, Any]:
    mpath = dataset_dir / "manifest.json"
    if not mpath.exists():
        raise FileNotFoundError(
            f"manifest.json not found at {mpath}.  "
            f"Run ``python -m ck.brain.build_training_set`` first."
        )
    with open(mpath, "r", encoding="utf-8") as f:
        return json.load(f)


def _count_train_rows(dataset_dir: Path) -> int:
    tpath = dataset_dir / "train.jsonl"
    if not tpath.exists():
        return 0
    n = 0
    with open(tpath, "r", encoding="utf-8") as f:
        for raw in f:
            if raw.strip():
                n += 1
    return n


# ----------------------------------------------------------------------------
# the training step (heavy imports happen here and only here)
# ----------------------------------------------------------------------------


def run_training(args: argparse.Namespace) -> Dict[str, Any]:
    """Execute the LoRA SFT run.  Returns a summary dict for the caller."""
    # Heavy imports.  Deferred so the module is import-safe without CUDA/unsloth.
    try:
        import torch  # noqa: F401
        from unsloth import FastLanguageModel, is_bfloat16_supported
        from unsloth.chat_templates import get_chat_template, standardize_sharegpt
        from datasets import load_dataset
        from trl import SFTTrainer
        from transformers import TrainingArguments
    except ImportError as e:
        raise RuntimeError(
            f"Heavy deps not installed: {e}.  Install with:\n"
            f"  pip install unsloth transformers datasets trl peft "
            f"bitsandbytes accelerate"
        ) from e

    dataset_dir = Path(args.dataset)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest = _load_manifest(dataset_dir)
    n_rows = _count_train_rows(dataset_dir)
    if n_rows < args.min_examples:
        raise RuntimeError(
            f"dataset {dataset_dir} has only {n_rows} rows; "
            f"--min-examples is {args.min_examples}.  "
            f"Collect more CK-approved turns before training."
        )

    print(f"[train_lora] {_now_iso()}")
    print(f"[train_lora]   dataset    : {dataset_dir} ({n_rows} rows)")
    print(f"[train_lora]   base_model : {args.base}")
    print(f"[train_lora]   output     : {out_dir}")
    print(f"[train_lora]   max_seq_len: {args.max_seq_len}")
    print(f"[train_lora]   LoRA r={args.lora_r} alpha={args.lora_alpha} "
          f"drop={args.lora_dropout}")
    print(f"[train_lora]   epochs={args.epochs} lr={args.lr} "
          f"batch={args.per_device_batch} accum={args.grad_accum}")

    # 1) load base + attach LoRA
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=args.base,
        max_seq_length=args.max_seq_len,
        dtype=None,            # auto (bf16 if supported, else fp16)
        load_in_4bit=True,
    )
    model = FastLanguageModel.get_peft_model(
        model,
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        lora_dropout=args.lora_dropout,
        target_modules=list(DEFAULT_TARGET_MODULES),
        bias="none",
        use_gradient_checkpointing="unsloth",
        random_state=args.seed,
        use_rslora=False,
        loftq_config=None,
    )

    # 2) tokenize sharegpt conversations with llama-3.1 chat template
    tokenizer = get_chat_template(tokenizer, chat_template="llama-3.1")

    def _format(examples):
        convos = examples["conversations"]
        texts = [
            tokenizer.apply_chat_template(c, tokenize=False, add_generation_prompt=False)
            for c in convos
        ]
        return {"text": texts}

    ds = load_dataset("json", data_files=str(dataset_dir / "train.jsonl"),
                      split="train")
    ds = standardize_sharegpt(ds)
    ds = ds.map(_format, batched=True)

    # 3) trainer
    training_args = TrainingArguments(
        per_device_train_batch_size=args.per_device_batch,
        gradient_accumulation_steps=args.grad_accum,
        warmup_steps=args.warmup_steps,
        num_train_epochs=args.epochs,
        learning_rate=args.lr,
        fp16=not is_bfloat16_supported(),
        bf16=is_bfloat16_supported(),
        logging_steps=1,
        optim="adamw_8bit",
        weight_decay=args.weight_decay,
        lr_scheduler_type="linear",
        seed=args.seed,
        output_dir=str(out_dir / "ckpt"),
        report_to="none",
        save_strategy="no",
    )
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=ds,
        dataset_text_field="text",
        max_seq_length=args.max_seq_len,
        dataset_num_proc=2,
        packing=False,
        args=training_args,
    )

    # 4) train
    result = trainer.train()
    print(f"[train_lora] train complete.  loss curve in trainer.state.log_history")

    # 5) save LoRA adapter only (small; merge happens in merge_and_export.py)
    adapter_dir = out_dir / "adapter"
    model.save_pretrained(str(adapter_dir))
    tokenizer.save_pretrained(str(adapter_dir))
    print(f"[train_lora] saved adapter -> {adapter_dir}")

    # 6) traceability: write train_log.json
    summary = {
        "trained_at": _now_iso(),
        "base_model": args.base,
        "dataset_dir": str(dataset_dir),
        "dataset_manifest": manifest,
        "n_train_rows": n_rows,
        "hparams": {
            "max_seq_len": args.max_seq_len,
            "lora_r": args.lora_r,
            "lora_alpha": args.lora_alpha,
            "lora_dropout": args.lora_dropout,
            "target_modules": list(DEFAULT_TARGET_MODULES),
            "lr": args.lr,
            "epochs": args.epochs,
            "per_device_batch": args.per_device_batch,
            "grad_accum": args.grad_accum,
            "warmup_steps": args.warmup_steps,
            "weight_decay": args.weight_decay,
            "seed": args.seed,
            "optim": "adamw_8bit",
        },
        "final_metrics": (result.metrics if hasattr(result, "metrics") else {}),
        "log_history_tail": trainer.state.log_history[-10:] if trainer.state.log_history else [],
        "adapter_dir": str(adapter_dir),
    }
    with open(out_dir / "train_log.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2, sort_keys=True)
    print(f"[train_lora] wrote train_log.json")
    return summary


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------


def _next_lora_version(base: Path) -> int:
    if not base.exists():
        return 1
    mv = 0
    for c in base.iterdir():
        if c.name.startswith("v") and c.name[1:].isdigit():
            mv = max(mv, int(c.name[1:]))
    return mv + 1


def _parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Fine-tune a LoRA adapter on CK-approved turns.",
    )
    ap.add_argument("--i-mean-it", action="store_true",
                    help="required: prevents accidental starts (G6 hands-on-wheel)")
    ap.add_argument("--dataset", required=True,
                    help="path to dataset dir (contains train.jsonl + manifest.json)")
    ap.add_argument("--output", default=None,
                    help="LoRA output dir (default: ck/brain/lora/v<auto>/)")
    ap.add_argument("--base", default=DEFAULT_BASE_MODEL,
                    help=f"base model (default {DEFAULT_BASE_MODEL})")

    ap.add_argument("--max-seq-len", type=int, default=DEFAULT_MAX_SEQ_LEN)
    ap.add_argument("--lora-r", type=int, default=DEFAULT_LORA_R)
    ap.add_argument("--lora-alpha", type=int, default=DEFAULT_LORA_ALPHA)
    ap.add_argument("--lora-dropout", type=float, default=DEFAULT_LORA_DROPOUT)

    ap.add_argument("--lr", type=float, default=DEFAULT_LR)
    ap.add_argument("--epochs", type=int, default=DEFAULT_EPOCHS)
    ap.add_argument("--per-device-batch", type=int, default=DEFAULT_PER_DEVICE_BATCH)
    ap.add_argument("--grad-accum", type=int, default=DEFAULT_GRAD_ACCUM)
    ap.add_argument("--warmup-steps", type=int, default=DEFAULT_WARMUP_STEPS)
    ap.add_argument("--weight-decay", type=float, default=DEFAULT_WEIGHT_DECAY)
    ap.add_argument("--seed", type=int, default=DEFAULT_SEED)

    ap.add_argument("--min-examples", type=int, default=DEFAULT_MIN_EXAMPLES,
                    help=f"abort if train.jsonl has fewer rows (default {DEFAULT_MIN_EXAMPLES})")
    return ap.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = _parse_args(argv)

    if not args.i_mean_it:
        print(
            "[train_lora] Refusing to start without --i-mean-it.\n"
            "            Training writes large artifacts (the LoRA) and\n"
            "            consumes GPU.  Pass --i-mean-it explicitly.",
            file=sys.stderr,
        )
        return 2

    if args.output is None:
        v = _next_lora_version(DEFAULT_LORA_DIR)
        args.output = str(DEFAULT_LORA_DIR / f"v{v}")

    try:
        run_training(args)
    except RuntimeError as e:
        print(f"[train_lora] {e}", file=sys.stderr)
        return 3
    except Exception as e:  # noqa: BLE001
        print(f"[train_lora] training failed: {type(e).__name__}: {e}",
              file=sys.stderr)
        return 4

    print("[train_lora] done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
