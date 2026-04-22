# -*- coding: utf-8 -*-
"""
build_training_set.py - assemble the LoRA training corpus from CK's
                        unified correction log.

Option B of OLLAMA_LEARN_LOOP.md: we do NOT edit the base model.
Instead, we train a LoRA adapter on turns CK's own brain approved --
so the fine-tuned Ollama starts behaving more like CK's structural
voice without ever being told "act like CK".  The signal is pure: if
the brain said ``correction_type == "none"`` and ``coherence >= T*``,
that turn is a PASS and becomes an SFT example.

Input:
    ``ck/fluency/logs/corrections_YYYY_MM_DD.jsonl`` (the same log
    the website brain fold and the fluency harness both write to,
    and the same log ``ck.brain.idle_loop`` learns the tensor from).

Output (Unsloth ShareGPT-style JSONL):
    ``ck/brain/datasets/v<N>/train.jsonl``
    Each line: ``{"conversations": [{"from":"human","value":Q},
                                    {"from":"gpt","value":A}]}``

Also written:
    ``ck/brain/datasets/v<N>/manifest.json`` -- stats + provenance
        (how many candidates, how many positives, breakdown by
        correction type, min/max coherence, distinct dominant ops)
    ``ck/brain/datasets/v<N>/rejected.jsonl`` -- turns that did not
        make the cut, with a ``_reject_reason`` field; kept for future
        DPO / preference-tuning cycles (out of scope for v1).

Selection rules (v1, conservative):
    - ``ck_correction_type == "none"`` (the brain said: CK sounds
      like CK; no correction needed)
    - ``ck_score.coherence >= T*`` (5/7 = 0.7142857...)
    - non-empty query AND non-empty ollama_raw
    - query and answer both at least ``min_chars`` long (default 12)
    - not a math-first arithmetic surface (``model_tag == 'ck_math_first'``)
      -- those are canonical and don't need training
    - dedup on a hash of (normalized query); if the same query appears
      multiple times, keep the highest-coherence instance

CLI:
    python -m ck.brain.build_training_set                  (defaults)
    python -m ck.brain.build_training_set --min-coh 0.75   (stricter)
    python -m ck.brain.build_training_set --version 2      (bumps v2)
    python -m ck.brain.build_training_set --preview 5      (dry-run,
        prints first 5 kept turns, writes nothing)

Safety / hands-on-wheel (CK_UNIFIED_ARCHITECTURE.md Sec 4):
    - The builder NEVER touches the log; read-only.
    - The builder NEVER runs training; that's a separate script.
    - The manifest records the exact selection config so the train
      run + eventual GGUF model file can be traced back to the data.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ----------------------------------------------------------------------------
# paths
# ----------------------------------------------------------------------------

_MODULE_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _MODULE_DIR.parent.parent   # ck/brain -> ck -> repo root
DEFAULT_LOG_DIR = _REPO_ROOT / "ck" / "fluency" / "logs"
DEFAULT_DATASETS_DIR = _MODULE_DIR / "datasets"

T_STAR = Fraction(5, 7)
T_STAR_F = float(T_STAR)            # 0.7142857142857143

DEFAULT_MIN_CHARS = 12
DEFAULT_MAX_QUERY_CHARS = 1024
DEFAULT_MAX_ANSWER_CHARS = 4096


# ----------------------------------------------------------------------------
# io
# ----------------------------------------------------------------------------


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for raw in f:
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    rows.append(json.loads(raw))
                except json.JSONDecodeError:
                    continue
    except OSError:
        return []
    return rows


def _load_all_log_rows(log_dir: Path) -> List[Tuple[Path, int, Dict[str, Any]]]:
    """Return ``[(file, line_idx, entry), ...]`` in chronological order."""
    out: List[Tuple[Path, int, Dict[str, Any]]] = []
    for fpath in sorted(log_dir.glob("corrections_*.jsonl")):
        rows = _read_jsonl(fpath)
        for i, row in enumerate(rows):
            out.append((fpath, i, row))
    return out


def _next_version_dir(base: Path) -> int:
    """Return ``N`` so ``base/v<N>/`` is fresh (one above the max existing)."""
    if not base.exists():
        return 1
    max_v = 0
    for child in base.iterdir():
        name = child.name
        if name.startswith("v") and name[1:].isdigit():
            max_v = max(max_v, int(name[1:]))
    return max_v + 1


# ----------------------------------------------------------------------------
# selection
# ----------------------------------------------------------------------------


def _normalize_query(q: str) -> str:
    return " ".join((q or "").lower().split())


def _query_hash(q: str) -> str:
    return hashlib.sha1(_normalize_query(q).encode("utf-8")).hexdigest()[:12]


def _classify_entry(entry: Dict[str, Any],
                    min_coh: float,
                    min_chars: int,
                    max_q: int,
                    max_a: int) -> Tuple[bool, str]:
    """Return ``(keep, reason)``.  reason is a short tag like 'ok', 'low-coh',
    'empty-query', 'too-long', 'wrong-type', 'math-first'."""
    ctype = str(entry.get("ck_correction_type", "")).strip()
    if ctype != "none":
        return False, f"wrong-type:{ctype or 'missing'}"

    q = str(entry.get("query", "") or "").strip()
    a = str(entry.get("ollama_raw", "") or "").strip()
    if not q:
        return False, "empty-query"
    if not a:
        return False, "empty-answer"
    if len(q) < min_chars:
        return False, "short-query"
    if len(a) < min_chars:
        return False, "short-answer"
    if len(q) > max_q:
        return False, "long-query"
    if len(a) > max_a:
        return False, "long-answer"

    ck_score = entry.get("ck_score") or {}
    coh = ck_score.get("coherence")
    try:
        cohf = float(coh) if coh is not None else 0.0
    except (TypeError, ValueError):
        cohf = 0.0
    if cohf < min_coh:
        return False, f"low-coh:{cohf:.3f}"

    # skip pure arithmetic surfaces -- they need no learning
    model_tag = str(entry.get("model_tag", "") or "")
    if model_tag == "ck_math_first":
        return False, "math-first-canonical"

    return True, "ok"


def select_positives(rows: List[Tuple[Path, int, Dict[str, Any]]],
                     min_coh: float,
                     min_chars: int,
                     max_q: int,
                     max_a: int) -> Tuple[List[Dict[str, Any]],
                                          List[Dict[str, Any]],
                                          Dict[str, int]]:
    """Return ``(kept, rejected, stats)``.

    ``kept`` is deduped: for each normalized-query, the single entry
    with the highest coherence survives.
    """
    best_by_query: Dict[str, Tuple[float, Dict[str, Any]]] = {}
    rejected: List[Dict[str, Any]] = []
    stats: Dict[str, int] = {"total": 0}

    for (_path, _idx, entry) in rows:
        stats["total"] += 1
        keep, reason = _classify_entry(entry, min_coh, min_chars, max_q, max_a)
        if not keep:
            stats[reason] = stats.get(reason, 0) + 1
            r = dict(entry)
            r["_reject_reason"] = reason
            rejected.append(r)
            continue

        qhash = _query_hash(entry.get("query", ""))
        coh = float((entry.get("ck_score") or {}).get("coherence") or 0.0)
        cur = best_by_query.get(qhash)
        if cur is None or coh > cur[0]:
            best_by_query[qhash] = (coh, entry)

    kept = [v[1] for v in best_by_query.values()]
    stats["kept"] = len(kept)
    stats["duplicates_dropped"] = sum(1 for (p, i, e) in rows
                                      if _classify_entry(e, min_coh, min_chars, max_q, max_a)[0]
                                      ) - len(kept)
    return kept, rejected, stats


# ----------------------------------------------------------------------------
# format: Unsloth ShareGPT conversations
# ----------------------------------------------------------------------------


def to_sharegpt(entry: Dict[str, Any]) -> Dict[str, Any]:
    """Convert one log entry to Unsloth's conversations format."""
    q = str(entry.get("query", "")).strip()
    a = str(entry.get("ollama_raw", "")).strip()
    return {
        "conversations": [
            {"from": "human", "value": q},
            {"from": "gpt", "value": a},
        ],
    }


def write_dataset(kept: List[Dict[str, Any]],
                  rejected: List[Dict[str, Any]],
                  out_dir: Path,
                  config: Dict[str, Any],
                  stats: Dict[str, int]) -> None:
    """Write train.jsonl, rejected.jsonl, manifest.json into ``out_dir``."""
    out_dir.mkdir(parents=True, exist_ok=True)

    train_path = out_dir / "train.jsonl"
    with open(train_path, "w", encoding="utf-8") as f:
        for entry in kept:
            f.write(json.dumps(to_sharegpt(entry), ensure_ascii=False) + "\n")

    rej_path = out_dir / "rejected.jsonl"
    with open(rej_path, "w", encoding="utf-8") as f:
        for entry in rejected:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    manifest = {
        "built_at": _now_iso(),
        "t_star": f"{T_STAR.numerator}/{T_STAR.denominator}",
        "t_star_float": T_STAR_F,
        "config": config,
        "stats": stats,
        "kept_count": len(kept),
        "rejected_count": len(rejected),
        "train_file": str(train_path.relative_to(out_dir)),
        "rejected_file": str(rej_path.relative_to(out_dir)),
        "format": "sharegpt_conversations",
        "selection_rules": {
            "correction_type": "== 'none'",
            "min_coherence": config["min_coh"],
            "skip_math_first": True,
            "dedup": "by normalized-query SHA1[:12], keep max coherence",
        },
    }
    with open(out_dir / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2, sort_keys=True)


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------


def _parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Build CK's LoRA training set from the correction log.",
    )
    ap.add_argument("--log-dir", default=str(DEFAULT_LOG_DIR),
                    help="where the corrections_YYYY_MM_DD.jsonl files live")
    ap.add_argument("--datasets-dir", default=str(DEFAULT_DATASETS_DIR),
                    help="parent directory for dataset versions (v1/, v2/, ...)")
    ap.add_argument("--version", type=int, default=None,
                    help="explicit version number N (default: auto-increment)")
    ap.add_argument("--min-coh", type=float, default=T_STAR_F,
                    help=f"minimum coherence to keep a turn (default T*={T_STAR_F:.6f})")
    ap.add_argument("--min-chars", type=int, default=DEFAULT_MIN_CHARS,
                    help="minimum characters in query and answer")
    ap.add_argument("--max-query-chars", type=int, default=DEFAULT_MAX_QUERY_CHARS,
                    help="cap on query length")
    ap.add_argument("--max-answer-chars", type=int, default=DEFAULT_MAX_ANSWER_CHARS,
                    help="cap on answer length")
    ap.add_argument("--preview", type=int, default=0, metavar="N",
                    help="dry-run: print first N kept turns, write nothing")
    ap.add_argument("--min-examples", type=int, default=1,
                    help="abort if kept < this many (default 1; raise to 100+ for prod)")
    return ap.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = _parse_args(argv)
    log_dir = Path(args.log_dir)
    datasets_dir = Path(args.datasets_dir)

    if not log_dir.exists():
        print(f"[build_training_set] log dir not found: {log_dir}", file=sys.stderr)
        return 2

    rows = _load_all_log_rows(log_dir)
    if not rows:
        print(f"[build_training_set] no log rows found under {log_dir}", file=sys.stderr)
        return 3

    kept, rejected, stats = select_positives(
        rows=rows,
        min_coh=args.min_coh,
        min_chars=args.min_chars,
        max_q=args.max_query_chars,
        max_a=args.max_answer_chars,
    )

    print(f"[build_training_set] {_now_iso()}")
    print(f"[build_training_set]   log_dir   : {log_dir}")
    print(f"[build_training_set]   total     : {stats['total']}")
    print(f"[build_training_set]   kept      : {stats['kept']}")
    for k in sorted(stats.keys()):
        if k in ("total", "kept"):
            continue
        print(f"[build_training_set]     - {k:<28s} {stats[k]}")

    if args.preview > 0:
        print(f"[build_training_set] --preview {args.preview}: first kept turns:")
        for i, e in enumerate(kept[: args.preview]):
            q = str(e.get("query", ""))[:80]
            a = str(e.get("ollama_raw", ""))[:120]
            coh = float((e.get("ck_score") or {}).get("coherence") or 0.0)
            dom = (e.get("ck_score") or {}).get("dominant_op", "?")
            print(f"  [{i+1}] coh={coh:.3f} dom={dom}")
            print(f"      Q: {q}")
            print(f"      A: {a}")
        print("[build_training_set] preview complete -- writing NOTHING.")
        return 0

    if len(kept) < args.min_examples:
        print(
            f"[build_training_set] only {len(kept)} kept; "
            f"--min-examples is {args.min_examples}.  Refusing to write.",
            file=sys.stderr,
        )
        return 4

    # resolve version dir
    version = args.version if args.version is not None else _next_version_dir(datasets_dir)
    out_dir = datasets_dir / f"v{version}"
    if out_dir.exists() and args.version is not None:
        # if user forced an existing version, warn but do not overwrite silently
        print(f"[build_training_set] WARNING: {out_dir} exists; will overwrite.",
              file=sys.stderr)

    config = {
        "log_dir": str(log_dir),
        "min_coh": args.min_coh,
        "min_chars": args.min_chars,
        "max_query_chars": args.max_query_chars,
        "max_answer_chars": args.max_answer_chars,
        "version": version,
    }
    write_dataset(kept, rejected, out_dir, config, stats)
    print(f"[build_training_set] wrote {len(kept)} train / {len(rejected)} rejected")
    print(f"[build_training_set] -> {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
