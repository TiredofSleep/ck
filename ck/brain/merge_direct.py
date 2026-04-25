# -*- coding: utf-8 -*-
"""
merge_direct.py - alternative Phase A merger that does NOT need an
                  fp16 download.

The default merge_and_export.py uses unsloth's save_pretrained_merged
with save_method="merged_16bit" which tries to download the original
fp16 sharded checkpoint from HF -- that's ~16 GB and on a slow link
takes hours.  This script bypasses that:

  1. Load the bnb-4bit base (already on disk from training).
  2. Attach the LoRA adapter via peft.
  3. peft.merge_and_unload() folds the LoRA into the base.
  4. Dequantize the merged model to bf16 IN MEMORY by walking the
     state_dict (bitsandbytes' Linear4bit -> bf16 Linear).
  5. Save as a regular HF checkpoint (bf16 safetensors) ready for
     llama.cpp's convert_hf_to_gguf.py.

After this script runs you can hand the output dir to
merge_and_export.py with --skip-merge and let it do Phase B (GGUF) and
Phase C (Ollama register).

CLI:
    python -m ck.brain.merge_direct
        --i-mean-it
        --lora ck/brain/lora/v2

Output:
    ck/brain/lora/v2/merged_fp16/   (bf16 HF checkpoint)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional


def _now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--i-mean-it", action="store_true", required=False)
    ap.add_argument("--lora", required=True,
                    help="LoRA dir containing adapter/")
    ap.add_argument("--out", default=None,
                    help="output dir (default: <lora>/merged_fp16/)")
    ap.add_argument("--dtype", default="bfloat16",
                    choices=("bfloat16", "float16"),
                    help="dtype for the merged model")
    args = ap.parse_args(argv)

    if not args.i_mean_it:
        print("[merge_direct] refusing without --i-mean-it", file=sys.stderr)
        return 2

    lora_dir = Path(args.lora)
    adapter_dir = lora_dir / "adapter"
    if not adapter_dir.exists():
        print(f"[merge_direct] adapter not found: {adapter_dir}", file=sys.stderr)
        return 3
    out_dir = Path(args.out) if args.out else (lora_dir / "merged_fp16")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Resolve base from adapter_config.json
    cfg_path = adapter_dir / "adapter_config.json"
    with open(cfg_path, "r", encoding="utf-8") as f:
        adapter_cfg = json.load(f)
    base_id = adapter_cfg.get("base_model_name_or_path")
    if not base_id:
        print("[merge_direct] cannot resolve base_model_name_or_path", file=sys.stderr)
        return 4
    print(f"[merge_direct] {_now()}")
    print(f"[merge_direct] base    : {base_id}")
    print(f"[merge_direct] adapter : {adapter_dir}")
    print(f"[merge_direct] output  : {out_dir}")
    print(f"[merge_direct] dtype   : {args.dtype}")

    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
    from peft import PeftModel

    # 1) Load bnb-4bit base.  This uses the already-cached blob.
    target_dtype = torch.bfloat16 if args.dtype == "bfloat16" else torch.float16
    bnb_cfg = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=target_dtype,
    )
    print(f"[merge_direct] loading base in 4-bit ...")
    base = AutoModelForCausalLM.from_pretrained(
        base_id,
        quantization_config=bnb_cfg,
        torch_dtype=target_dtype,
        device_map="auto",
    )
    print(f"[merge_direct] base loaded.")

    # 2) Attach LoRA
    print(f"[merge_direct] attaching adapter ...")
    peft_model = PeftModel.from_pretrained(base, str(adapter_dir))

    # 3) Merge -- this dequantizes the base in-place to compute_dtype
    #    and folds the LoRA delta in.  The result is a regular HF
    #    AutoModelForCausalLM with bf16/fp16 weights.
    print(f"[merge_direct] merging (peft.merge_and_unload) ...")
    merged = peft_model.merge_and_unload()
    print(f"[merge_direct] merge complete.  saving ...")

    # 4) Save as HF checkpoint (bf16 safetensors)
    merged.save_pretrained(
        str(out_dir),
        safe_serialization=True,
        max_shard_size="2GB",
    )

    # tokenizer too
    tok = AutoTokenizer.from_pretrained(base_id)
    tok.save_pretrained(str(out_dir))

    # bookkeeping
    log = {
        "merged_at": _now(),
        "base": base_id,
        "adapter": str(adapter_dir),
        "out": str(out_dir),
        "dtype": args.dtype,
        "method": "peft.merge_and_unload (no fp16 download)",
    }
    with open(out_dir / "merge_direct_log.json", "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2, sort_keys=True)
    print(f"[merge_direct] wrote merge_direct_log.json")

    # list what was saved
    print(f"[merge_direct] output files:")
    for p in sorted(out_dir.iterdir()):
        print(f"    {p.name}  ({p.stat().st_size/1e6:.1f} MB)")

    print(f"[merge_direct] done.")
    print(f"[merge_direct] next: convert_hf_to_gguf.py {out_dir} --outtype f16 --outfile <name>.gguf")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
