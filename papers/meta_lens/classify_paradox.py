#!/usr/bin/env python3
"""
classify_paradox.py — runnable UOP classifier (atlas open item [O-1])

Status: stub-but-real.
  - Not an LLM call, not a heuristic. It is a rule-based dispatcher
    over the 6-slot UOP schema.
  - It reads the markdown templates in worked_paradoxes/ as its
    template corpus and exposes a CLI + Python API.
  - It accepts either a template name ("godel", "liar", "schrodinger")
    or a JSON instance conforming to the 6-slot schema
    (see worked_paradoxes/README.md for the schema).

What it does NOT do (honest limits):
  - Does not parse a natural-language paradox statement. That is an
    NLP problem the atlas deliberately leaves open.
  - Does not compute Slot 3 for you. The verdict is rule-based on
    the USER-PROVIDED Slot-3 structure ("where did separation fail:
    object / invariant / joint-map / dynamics?"). If you fill Slot 3
    wrong, the classifier will faithfully return the wrong type.
  - Does not score confidence from the markdown body; if confidence
    is provided in the JSON input it is echoed through unchanged.

Usage:
  $ python classify_paradox.py --list
  $ python classify_paradox.py --template godel
  $ python classify_paradox.py --json my_paradox.json

JSON input schema (minimum):
  {
    "name": "string",
    "slot3_failure_stage": "admissibility" | "invariant" | "joint_map" | "dynamics",
    "confidence": float in [0,1]   (optional, default 1.0)
  }

Output:
  {"type": "I"|"II"|"III"|"IV", "fix_family": str, "confidence": float}

The four-type axis is from:
  Gen12/targets/clay/papers/sprint11_tig_bundle_2026_04_08/sprints/
    PARADOX_CLASSIFICATION_MEMO.md (Sanders, Mayes)
  papers/meta_lens/META_LENS_ATLAS.md (atlas v1.1)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent
TEMPLATE_DIR = HERE / "worked_paradoxes"

# ---------------------------------------------------------------------------
# Decision procedure — Slot-3 failure stage -> Slot-4 type
#
# This is the core rule. It is deliberately simple: the UOP six-slot
# template is already designed so that Slot-3 forces Slot-4. The
# classifier does not invent type; it enforces the forcing.
# ---------------------------------------------------------------------------

STAGE_TO_TYPE = {
    "joint_map":    ("I",   "add observable / refine symbolic powers / coordinate extension"),
    "invariant":    ("II",  "accept gap / relativize / change category / climb ordinal tower"),
    "admissibility":("III", "narrow admissible class / change logic / ascend type hierarchy"),
    "dynamics":     ("IV",  "single-valued dynamics via decoherence / MWI / GRW / Bohm / QBism"),
}

TYPE_LONG_NAME = {
    "I":   "Injectivity Failure",
    "II":  "Missing Invariant",
    "III": "Admissibility Failure",
    "IV":  "Time-Consistency Failure",
}

# ---------------------------------------------------------------------------
# Template parsing
# ---------------------------------------------------------------------------

@dataclass
class TemplateHeader:
    name: str                # display name from H1
    file: Path
    atlas_id: str            # e.g. "[O-3]", or "" if not numbered
    type_code: str           # "I" | "II" | "III" | "IV"

    def as_dict(self) -> dict:
        return {
            "name": self.name,
            "file": str(self.file.relative_to(HERE)),
            "atlas_id": self.atlas_id,
            "type": self.type_code,
            "type_long": TYPE_LONG_NAME[self.type_code],
        }


CLASSIFICATION_RE = re.compile(
    r"Classification:\s*UOP\s+Type\s+(I{1,3}|IV|V?)\b", re.IGNORECASE
)
ATLAS_ID_RE = re.compile(r"\[O-(\d+)\]")


def _parse_header(path: Path) -> TemplateHeader | None:
    """Extract name, atlas ID, and type from a template markdown file.

    We do not parse the whole template body; we just confirm it
    advertises itself correctly. Templates are the source of truth.
    """
    text = path.read_text(encoding="utf-8", errors="replace")
    # First H1 line becomes display name
    h1_match = re.search(r"^#\s+(.+?)\s*$", text, re.MULTILINE)
    name = h1_match.group(1).strip() if h1_match else path.stem
    # Atlas ID (first [O-N] occurrence in the first 40 lines)
    head = "\n".join(text.splitlines()[:40])
    atlas_id_match = ATLAS_ID_RE.search(head)
    atlas_id = f"[O-{atlas_id_match.group(1)}]" if atlas_id_match else ""
    # Type code from Classification line
    cls_match = CLASSIFICATION_RE.search(text)
    if not cls_match:
        return None
    type_code = cls_match.group(1).upper()
    # Normalize: "II" / "III" / "IV" stay; "I" stays; reject anything else
    if type_code not in TYPE_LONG_NAME:
        return None
    return TemplateHeader(name=name, file=path, atlas_id=atlas_id, type_code=type_code)


def discover_templates() -> list[TemplateHeader]:
    """Return all parseable templates under worked_paradoxes/."""
    if not TEMPLATE_DIR.is_dir():
        return []
    out: list[TemplateHeader] = []
    for md in sorted(TEMPLATE_DIR.glob("paradox_*.md")):
        hdr = _parse_header(md)
        if hdr is not None:
            out.append(hdr)
    return out


# ---------------------------------------------------------------------------
# Classification — the two public entry points
# ---------------------------------------------------------------------------

def classify_from_template(slug: str) -> dict:
    """Look up a shipped template by slug (e.g. "godel", "liar",
    "schrodinger") and return its stored verdict.
    """
    slug = slug.lower().strip()
    for hdr in discover_templates():
        fname = hdr.file.stem.lower()
        if slug in fname:
            type_code = hdr.type_code
            # fix-family string derived by reverse lookup from STAGE_TO_TYPE
            fix = next(
                (fx for (ty, fx) in STAGE_TO_TYPE.values() if ty == type_code),
                "",
            )
            return {
                "source": "template",
                "paradox": hdr.name,
                "atlas_id": hdr.atlas_id,
                "type": type_code,
                "type_long": TYPE_LONG_NAME[type_code],
                "fix_family": fix,
                "confidence": 1.0,
                "template_file": str(hdr.file.relative_to(HERE)),
            }
    raise KeyError(
        f"No template matching slug {slug!r}. "
        f"Known slugs: {[h.file.stem for h in discover_templates()]}"
    )


def classify_from_json(obj: dict) -> dict:
    """Classify a paradox described as a JSON 6-slot instance.

    Required keys:
      slot3_failure_stage ∈ {admissibility, invariant, joint_map, dynamics}

    Optional keys:
      name, confidence, slot1_objects, slot2_observables, …
    """
    stage = obj.get("slot3_failure_stage", "").strip().lower()
    if stage not in STAGE_TO_TYPE:
        raise ValueError(
            f"slot3_failure_stage must be one of "
            f"{sorted(STAGE_TO_TYPE)}, got {stage!r}"
        )
    type_code, fix = STAGE_TO_TYPE[stage]
    return {
        "source": "json",
        "paradox": obj.get("name", "<unnamed>"),
        "atlas_id": obj.get("atlas_id", ""),
        "type": type_code,
        "type_long": TYPE_LONG_NAME[type_code],
        "fix_family": fix,
        "confidence": float(obj.get("confidence", 1.0)),
        "slot3_failure_stage": stage,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _cmd_list() -> int:
    templates = discover_templates()
    if not templates:
        print("No templates found under", TEMPLATE_DIR)
        return 1
    print(f"Templates in {TEMPLATE_DIR.relative_to(HERE.parent)}:")
    print()
    width = max(len(h.name) for h in templates)
    for h in templates:
        aid = h.atlas_id or "     "
        print(f"  {aid:6s}  Type {h.type_code:<3s}  {h.name:<{width}s}  "
              f"({h.file.name})")
    print()
    print("Slots I / II / III / IV correspond to failure stages:")
    for stage, (ty, _fix) in STAGE_TO_TYPE.items():
        print(f"  {stage:16s} -> Type {ty}  ({TYPE_LONG_NAME[ty]})")
    return 0


def _cmd_template(slug: str) -> int:
    try:
        verdict = classify_from_template(slug)
    except KeyError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(verdict, indent=2))
    return 0


def _cmd_json(path: str) -> int:
    p = Path(path)
    if not p.is_file():
        print(f"error: {p} is not a file", file=sys.stderr)
        return 2
    try:
        obj = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"error: could not parse JSON: {exc}", file=sys.stderr)
        return 2
    try:
        verdict = classify_from_json(obj)
    except (ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(verdict, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="classify_paradox",
        description=(
            "UOP paradox classifier. Enforces the forcing from the "
            "6-slot template's Slot-3 failure stage to the Slot-4 "
            "type verdict."
        ),
    )
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--list", action="store_true",
                   help="list shipped templates under worked_paradoxes/")
    g.add_argument("--template", metavar="SLUG",
                   help="classify a shipped template by slug, e.g. godel")
    g.add_argument("--json", metavar="PATH",
                   help="classify a 6-slot JSON instance at PATH")
    ns = ap.parse_args(argv)

    if ns.list:
        return _cmd_list()
    if ns.template:
        return _cmd_template(ns.template)
    if ns.json:
        return _cmd_json(ns.json)
    ap.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
