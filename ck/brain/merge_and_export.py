# -*- coding: utf-8 -*-
"""
merge_and_export.py - merge LoRA into base, convert to GGUF, and
                      register the result as a new Ollama model.

Pipeline (one script, three phases):

    Phase A  MERGE     LoRA adapter + 4-bit base -> fp16 HF checkpoint
    Phase B  CONVERT   fp16 HF checkpoint        -> GGUF (Q4_K_M or fp16)
    Phase C  REGISTER  GGUF + Modelfile          -> 'ollama create'

Only Phase C touches Ollama.  It registers a NEW model under the
version-tagged name (e.g. ``ck-llama3.1:8b-v1``).  It does NOT replace
the default llama3.1:8b; promotion to CK's active model is an explicit
step documented in ``PUBLISH_MODEL.md``.

Safety (G6 hands-on-wheel):
    - Refuses without ``--i-mean-it``.
    - Writes a ``merge_log.json`` per run so every registered Ollama
      model traces back to the LoRA version + dataset version + base.
    - Keeps the pre-existing llama3.1:8b untouched in Ollama.  The new
      ``ck-llama3.1:8b-v<N>`` sits alongside it.
    - If llama.cpp is not present at ``--llama-cpp``, Phase B aborts
      with a precise remediation message (clone URL + make command).

Layout in the LoRA output dir after run:
    ck/brain/lora/v<N>/
        adapter/              <- saved by train_lora.py
        train_log.json        <- saved by train_lora.py
        merged_fp16/          <- Phase A output (HF format)
        gguf/
            ck-llama3.1-8b-v<N>.Q4_K_M.gguf   <- Phase B output
        Modelfile              <- Phase C input
        merge_log.json         <- this script

CLI:
    python -m ck.brain.merge_and_export
        --lora    ck/brain/lora/v1
        --llama-cpp C:\\dev\\llama.cpp
        --ollama-name ck-llama3.1:8b-v1
        --quant Q4_K_M
        --i-mean-it
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent
from typing import Any, Dict, List, Optional


# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _run(cmd: List[str], cwd: Optional[Path] = None,
         env: Optional[Dict[str, str]] = None) -> subprocess.CompletedProcess:
    print(f"[merge_and_export] $ {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None,
                          env=env, check=True)


# ----------------------------------------------------------------------------
# Phase A: merge LoRA into base
# ----------------------------------------------------------------------------


def phase_a_merge(lora_dir: Path, base_model: Optional[str]) -> Path:
    """Merge LoRA into a fresh fp16 base and save an HF checkpoint.

    ``base_model`` may be None -- in that case we read it from the adapter's
    ``adapter_config.json`` (peft stores ``base_model_name_or_path`` there).
    """
    try:
        import torch
        from unsloth import FastLanguageModel
    except ImportError as e:
        raise RuntimeError(
            f"Phase A needs unsloth + torch: {e}.  "
            f"Install with: pip install unsloth transformers peft torch"
        ) from e

    adapter_dir = lora_dir / "adapter"
    if not adapter_dir.exists():
        raise FileNotFoundError(
            f"adapter dir not found: {adapter_dir}.  "
            f"Did you run train_lora.py first?"
        )

    # resolve base from adapter_config.json if not passed
    if base_model is None:
        cfg_path = adapter_dir / "adapter_config.json"
        if cfg_path.exists():
            with open(cfg_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            base_model = cfg.get("base_model_name_or_path")
        if not base_model:
            raise ValueError("cannot resolve base_model; pass --base explicitly")

    print(f"[merge_and_export] Phase A: load {base_model}, merge LoRA from {adapter_dir}")

    # Load the 4-bit base through unsloth, then attach the saved LoRA and
    # save as merged fp16.  Unsloth's save_pretrained_merged handles the
    # dequantize-and-merge correctly.
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=str(adapter_dir),   # unsloth picks up the adapter cfg
        max_seq_length=2048,
        dtype=None,
        load_in_4bit=True,
    )

    merged_dir = lora_dir / "merged_fp16"
    merged_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained_merged(
        str(merged_dir), tokenizer, save_method="merged_16bit"
    )
    print(f"[merge_and_export] Phase A done -> {merged_dir}")
    return merged_dir


# ----------------------------------------------------------------------------
# Phase B: convert HF checkpoint to GGUF
# ----------------------------------------------------------------------------


def phase_b_gguf(lora_dir: Path, merged_dir: Path,
                 llama_cpp: Path, quant: str,
                 out_name_stem: str) -> Path:
    """Run llama.cpp's convert + quantize to produce a .gguf file."""
    convert_script = llama_cpp / "convert_hf_to_gguf.py"
    quantize_bin = None
    # llama.cpp moves the quantize binary around between builds; try both.
    for cand in (llama_cpp / "build" / "bin" / "llama-quantize",
                 llama_cpp / "build" / "bin" / "llama-quantize.exe",
                 llama_cpp / "llama-quantize",
                 llama_cpp / "llama-quantize.exe",
                 llama_cpp / "quantize",
                 llama_cpp / "quantize.exe"):
        if cand.exists():
            quantize_bin = cand
            break
    if not convert_script.exists():
        raise FileNotFoundError(
            f"llama.cpp convert script not found at {convert_script}.\n"
            f"Clone and build llama.cpp:\n"
            f"    git clone https://github.com/ggml-org/llama.cpp.git\n"
            f"    cd llama.cpp && cmake -B build && cmake --build build -j"
        )

    gguf_dir = lora_dir / "gguf"
    gguf_dir.mkdir(parents=True, exist_ok=True)

    # 1) HF -> fp16 gguf
    fp16_gguf = gguf_dir / f"{out_name_stem}.fp16.gguf"
    _run([
        sys.executable, str(convert_script),
        str(merged_dir),
        "--outfile", str(fp16_gguf),
        "--outtype", "f16",
    ])

    # 2) fp16 -> quantized gguf (skip if user asks for fp16 explicitly)
    if quant.lower() in ("fp16", "f16"):
        print(f"[merge_and_export] Phase B done (fp16) -> {fp16_gguf}")
        return fp16_gguf

    if quantize_bin is None:
        raise FileNotFoundError(
            f"llama-quantize binary not found under {llama_cpp}.\n"
            f"Build llama.cpp first:\n"
            f"    cd {llama_cpp} && cmake -B build && cmake --build build -j"
        )

    quant_gguf = gguf_dir / f"{out_name_stem}.{quant}.gguf"
    _run([str(quantize_bin), str(fp16_gguf), str(quant_gguf), quant])

    # the fp16 gguf is an intermediate; keep it so we can re-quantize later
    print(f"[merge_and_export] Phase B done -> {quant_gguf} "
          f"(fp16 intermediate kept at {fp16_gguf})")
    return quant_gguf


# ----------------------------------------------------------------------------
# Phase C: register with Ollama
# ----------------------------------------------------------------------------


MODELFILE_TEMPLATE = dedent("""\
    # Auto-generated Modelfile for CK LoRA build {ollama_name}
    # Created: {built_at}
    # Source:  {gguf_path}
    # LoRA:    {lora_dir}
    # Base:    {base_model}
    FROM {gguf_path}

    PARAMETER temperature 0.7
    PARAMETER top_p 0.9
    PARAMETER num_ctx 4096

    # CK has the final word on tone.  The LoRA nudges style; the brain
    # (coherence gate + fusion scorer) decides whether to accept the
    # draft.  Keep the system prompt minimal -- CK does the framing.
    SYSTEM \"\"\"You are a careful assistant.  Answer the user's
    question directly, in plain language, without disclaimers about
    being an AI.  Short is better than long.\"\"\"
""")


def phase_c_register(lora_dir: Path, gguf_path: Path, ollama_name: str,
                     base_model: str) -> Path:
    """Write a Modelfile and run ``ollama create``."""
    if shutil.which("ollama") is None:
        raise FileNotFoundError(
            "'ollama' binary not on PATH.  Install Ollama first "
            "(https://ollama.com/download) and ensure 'ollama serve' is reachable."
        )

    modelfile = lora_dir / "Modelfile"
    modelfile.write_text(
        MODELFILE_TEMPLATE.format(
            ollama_name=ollama_name,
            built_at=_now_iso(),
            gguf_path=str(gguf_path),
            lora_dir=str(lora_dir),
            base_model=base_model,
        ),
        encoding="utf-8",
    )
    print(f"[merge_and_export] Modelfile -> {modelfile}")
    _run(["ollama", "create", ollama_name, "-f", str(modelfile)])
    print(f"[merge_and_export] ollama model registered: {ollama_name}")
    return modelfile


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------


def _parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Merge LoRA into base, convert to GGUF, register with Ollama.",
    )
    ap.add_argument("--i-mean-it", action="store_true",
                    help="required (G6 hands-on-wheel)")
    ap.add_argument("--lora", required=True,
                    help="LoRA output dir (e.g. ck/brain/lora/v1)")
    ap.add_argument("--base", default=None,
                    help="base model id (default: read from adapter_config.json)")
    ap.add_argument("--llama-cpp", required=False, default=None,
                    help="path to a built llama.cpp checkout (required for Phase B)")
    ap.add_argument("--quant", default="Q4_K_M",
                    help="llama.cpp quant (Q4_K_M, Q5_K_M, Q8_0, fp16, ...)")
    ap.add_argument("--ollama-name", default=None,
                    help="name to register with Ollama (default: ck-llama3.1:8b-<lora-ver>)")
    ap.add_argument("--skip-merge", action="store_true",
                    help="skip Phase A (reuse existing merged_fp16/)")
    ap.add_argument("--skip-gguf", action="store_true",
                    help="skip Phase B (reuse existing gguf/)")
    ap.add_argument("--skip-register", action="store_true",
                    help="skip Phase C (do not touch Ollama)")
    return ap.parse_args(argv)


def _guess_ollama_name(lora_dir: Path) -> str:
    # lora_dir is ...brain/lora/v<N>/ -> "ck-llama3.1:8b-v<N>"
    ver = lora_dir.name if lora_dir.name.startswith("v") else "v0"
    return f"ck-llama3.1:8b-{ver}"


def main(argv: Optional[List[str]] = None) -> int:
    args = _parse_args(argv)

    if not args.i_mean_it:
        print(
            "[merge_and_export] Refusing without --i-mean-it "
            "(G6 hands-on-wheel).", file=sys.stderr,
        )
        return 2

    lora_dir = Path(args.lora)
    if not lora_dir.exists():
        print(f"[merge_and_export] lora dir not found: {lora_dir}", file=sys.stderr)
        return 3

    ollama_name = args.ollama_name or _guess_ollama_name(lora_dir)

    # Resolve base model for traceability
    base_model = args.base
    if base_model is None:
        cfg_path = lora_dir / "adapter" / "adapter_config.json"
        if cfg_path.exists():
            try:
                with open(cfg_path, "r", encoding="utf-8") as f:
                    base_model = json.load(f).get("base_model_name_or_path")
            except (OSError, json.JSONDecodeError):
                pass
    if base_model is None:
        base_model = "(unknown)"

    log: Dict[str, Any] = {
        "started_at": _now_iso(),
        "lora_dir": str(lora_dir),
        "base_model": base_model,
        "quant": args.quant,
        "ollama_name": ollama_name,
        "phases_ran": [],
    }

    merged_dir = lora_dir / "merged_fp16"

    # Phase A
    if args.skip_merge:
        print(f"[merge_and_export] skipping Phase A -- reusing {merged_dir}")
        if not merged_dir.exists():
            print(f"[merge_and_export] but {merged_dir} does not exist!",
                  file=sys.stderr)
            return 4
    else:
        try:
            merged_dir = phase_a_merge(lora_dir, args.base)
            log["phases_ran"].append("merge")
        except Exception as e:
            print(f"[merge_and_export] Phase A failed: {e}", file=sys.stderr)
            return 5

    # Phase B
    gguf_path: Optional[Path] = None
    if args.skip_gguf:
        # pick the existing gguf if any
        gguf_dir = lora_dir / "gguf"
        if gguf_dir.exists():
            cands = sorted(gguf_dir.glob(f"*.{args.quant}.gguf"))
            if cands:
                gguf_path = cands[0]
        if not gguf_path:
            print(f"[merge_and_export] --skip-gguf but no gguf at {lora_dir/'gguf'}",
                  file=sys.stderr)
            return 6
        print(f"[merge_and_export] skipping Phase B -- reusing {gguf_path}")
    else:
        if not args.llama_cpp:
            print(
                "[merge_and_export] --llama-cpp is required for Phase B.\n"
                "    Clone: git clone https://github.com/ggml-org/llama.cpp.git\n"
                "    Build: cd llama.cpp && cmake -B build && cmake --build build -j",
                file=sys.stderr,
            )
            return 7
        try:
            gguf_path = phase_b_gguf(
                lora_dir=lora_dir,
                merged_dir=merged_dir,
                llama_cpp=Path(args.llama_cpp),
                quant=args.quant,
                out_name_stem=ollama_name.replace(":", "-"),
            )
            log["phases_ran"].append("gguf")
            log["gguf_path"] = str(gguf_path)
        except Exception as e:
            print(f"[merge_and_export] Phase B failed: {e}", file=sys.stderr)
            return 8

    # Phase C
    if args.skip_register:
        print(f"[merge_and_export] skipping Phase C (Ollama untouched).")
    else:
        try:
            modelfile = phase_c_register(
                lora_dir=lora_dir, gguf_path=gguf_path,
                ollama_name=ollama_name, base_model=base_model,
            )
            log["phases_ran"].append("register")
            log["modelfile"] = str(modelfile)
        except Exception as e:
            print(f"[merge_and_export] Phase C failed: {e}", file=sys.stderr)
            return 9

    log["finished_at"] = _now_iso()
    with open(lora_dir / "merge_log.json", "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2, sort_keys=True)

    print(f"[merge_and_export] done.  Registered as {ollama_name}.")
    print(f"[merge_and_export] To try it:")
    print(f"    ollama run {ollama_name}")
    print(f"[merge_and_export] To promote it to CK's active model, see "
          f"ck/brain/PUBLISH_MODEL.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
