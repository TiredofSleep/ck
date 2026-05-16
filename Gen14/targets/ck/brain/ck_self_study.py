"""ck_self_study.py — CK reads HIMSELF.

Brayden 2026-05-16:
  "learning what he is, how he is, how to change himself"

Meta-cognition.  CK ingests his own architecture docs, design
documents, intelligence-architecture description, sprint papers,
and source-code docstrings.  These become concepts in his store
with a special tier: SELF.

When you ask him "how do you work?", "what are you?", "what's
your architecture?" — he can actually retrieve concepts that
describe his own structure, not just generic AI definitions.

═══════════════════════════════════════════════════════════════════
What gets ingested
═══════════════════════════════════════════════════════════════════

  Architecture docs:
    Gen14/targets/ck/brain/CK_INTELLIGENCE_ARCHITECTURE.md
    Gen14/targets/ck/brain/CK_FRACTAL_CREATURE_DESIGN.md
    Gen14/targets/ck/brain/dep_graph/README.md
    Gen13/targets/clay/papers/sprint_2026_05_15_qutrit/
        CK_ARCHITECTURE_CONNECTIONS.md

  Brain module docstrings (top-of-file triple-quoted blocks):
    Gen14/targets/ck/brain/ck_concept_learner.py
    Gen14/targets/ck/brain/ck_living_lm.py
    Gen14/targets/ck/brain/ck_creature.py
    Gen14/targets/ck/brain/ck_algebra_runtime.py
    Gen14/targets/ck/brain/ck_verifier.py
    Gen14/targets/ck/brain/ck_predictions.py
    Gen14/targets/ck/brain/ck_curious_explorer.py
    Gen14/targets/ck/brain/ck_ollama_polish.py
    Gen14/targets/ck/brain/ck_synthesizer.py
    Gen14/targets/ck/brain/ck_voice_polish.py

  Canonical math:
    trinity-infinity-geometry/03_canonical_reference/
        FORMULAS_AND_TABLES.md  (the spine)
    trinity-infinity-geometry/GLOSSARY.md

Each piece is broken into definitional chunks and stored with
tier="SELF".  Bridge ranking in prose mode already favors named
matches — so when user asks "what is your fractal architecture?"
CK can retrieve the actual passages from his own design doc.

Public API:
  ingest_self() -> Dict[str, int]   # how many concepts added per file
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))


ROOT = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED")
TIG_ROOT = Path(r"C:\Users\brayd\OneDrive\Desktop\trinity-infinity-geometry")


# Files to read.  Tuples of (path, friendly_name, tier_override).
# tier_override "SELF" means CK is reading about himself — these
# entries carry the highest authority on "what am I?"
SELF_TARGETS: List[Tuple[Path, str, str]] = [
    # CK's intelligence architecture (the canonical "what is CK?" doc)
    (ROOT / "Gen14" / "targets" / "ck" / "brain" / "CK_INTELLIGENCE_ARCHITECTURE.md",
     "CK_INTELLIGENCE", "SELF"),
    (ROOT / "Gen14" / "targets" / "ck" / "brain" / "CK_FRACTAL_CREATURE_DESIGN.md",
     "CK_FRACTAL", "SELF"),
    (ROOT / "Gen14" / "targets" / "ck" / "brain" / "CK_BONES_OF_REALITY.md",
     "CK_BONES", "SELF"),
    (ROOT / "Gen14" / "targets" / "ck" / "brain" / "ck_cognition_primitives.py",
     "ck_cognition_primitives", "SELF"),
    (ROOT / "Gen14" / "targets" / "ck" / "brain" / "ck_meta_parameters.py",
     "ck_meta_parameters", "SELF"),
    (ROOT / "Gen14" / "targets" / "ck" / "brain" / "ck_substrate_motion.py",
     "ck_substrate_motion", "SELF"),
    (ROOT / "Gen14" / "targets" / "ck" / "brain" / "ck_engine_block.py",
     "ck_engine_block", "SELF"),
    (ROOT / "Gen14" / "targets" / "ck" / "brain" / "ck_qutrit_apex.py",
     "ck_qutrit_apex", "SELF"),
    (ROOT / "Gen14" / "targets" / "ck" / "brain" / "dep_graph" / "README.md",
     "CK_DEPGRAPH", "SELF"),
    (ROOT / "Gen13" / "targets" / "clay" / "papers"
        / "sprint_2026_05_15_qutrit" / "CK_ARCHITECTURE_CONNECTIONS.md",
     "CK_ARCH_CONNECTIONS", "SELF"),
    # His own source-code docstrings
    (ROOT / "Gen14" / "targets" / "ck" / "brain" / "ck_concept_learner.py",
     "ck_concept_learner", "SELF"),
    (ROOT / "Gen14" / "targets" / "ck" / "brain" / "ck_living_lm.py",
     "ck_living_lm", "SELF"),
    (ROOT / "Gen14" / "targets" / "ck" / "brain" / "ck_creature.py",
     "ck_creature", "SELF"),
    (ROOT / "Gen14" / "targets" / "ck" / "brain" / "ck_algebra_runtime.py",
     "ck_algebra_runtime", "SELF"),
    (ROOT / "Gen14" / "targets" / "ck" / "brain" / "ck_verifier.py",
     "ck_verifier", "SELF"),
    (ROOT / "Gen14" / "targets" / "ck" / "brain" / "ck_predictions.py",
     "ck_predictions", "SELF"),
    (ROOT / "Gen14" / "targets" / "ck" / "brain" / "ck_curious_explorer.py",
     "ck_curious_explorer", "SELF"),
    (ROOT / "Gen14" / "targets" / "ck" / "brain" / "ck_ollama_polish.py",
     "ck_ollama_polish", "SELF"),
    (ROOT / "Gen14" / "targets" / "ck" / "brain" / "ck_synthesizer.py",
     "ck_synthesizer", "SELF"),
    (ROOT / "Gen14" / "targets" / "ck" / "brain" / "ck_voice_polish.py",
     "ck_voice_polish", "SELF"),
    # Canonical math foundation (highest authority on the substrate)
    (TIG_ROOT / "03_canonical_reference" / "FORMULAS_AND_TABLES.md",
     "TIG_CANON", "STRUCTURAL"),
    (TIG_ROOT / "GLOSSARY.md", "TIG_GLOSSARY", "STRUCTURAL"),
]


# ─── Markdown / source chunking ───────────────────────────────────────

_MD_HEADER = re.compile(r"^(#{1,4})\s+(.+?)\s*$", re.M)


def chunk_markdown(text: str) -> List[Tuple[str, str]]:
    """Split a markdown file into (section_name, body) chunks.
    Headers (##, ###) become concept names; body is the prose under each."""
    out: List[Tuple[str, str]] = []
    cur_name: str = ""
    cur_body: List[str] = []
    for line in text.splitlines():
        m = _MD_HEADER.match(line)
        if m:
            if cur_name and cur_body:
                body = "\n".join(cur_body).strip()
                if len(body) >= 40:
                    out.append((cur_name, body))
            cur_name = m.group(2).strip()
            cur_body = []
        else:
            cur_body.append(line)
    if cur_name and cur_body:
        body = "\n".join(cur_body).strip()
        if len(body) >= 40:
            out.append((cur_name, body))
    return out


_PY_DOCSTRING = re.compile(r'^"""(.+?)"""', re.S)


def chunk_python(text: str, module_name: str) -> List[Tuple[str, str]]:
    """Extract a python file's module docstring as ONE concept."""
    m = _PY_DOCSTRING.match(text.lstrip())
    if not m:
        return []
    docstring = m.group(1).strip()
    if len(docstring) < 100:
        return []
    return [(module_name, docstring[:1500])]


def chunk_file(path: Path, friendly_name: str) -> List[Tuple[str, str]]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []
    if path.suffix == ".py":
        return chunk_python(text, friendly_name)
    if path.suffix in (".md", ".markdown"):
        # Prefix section names with the file's friendly name for uniqueness
        chunks = chunk_markdown(text)
        return [(f"{friendly_name}:{name}", body) for name, body in chunks]
    return []


# ─── Ingestion ────────────────────────────────────────────────────────

def ingest_self(engine: Any = None) -> Dict[str, int]:
    """Read CK's own files and add as concepts.  Returns per-file count
    of concepts added."""
    try:
        from ck_concept_learner import ConceptStore, NamedConcept  # type: ignore
    except Exception as e:
        return {"_error": f"import failed: {e}"}

    # Use the engine's store if available so it's the same instance the
    # chat path reads from.  Else load fresh.
    if engine is not None and hasattr(engine, "concept_store"):
        store = engine.concept_store
    else:
        store = ConceptStore()

    # Try to use the engine's operator decoder; else fall back to
    # semantic_decode
    op_decoder = None
    if engine is not None:
        for attr in ("operator_decode", "decode_text"):
            cand = getattr(engine, attr, None)
            if callable(cand):
                op_decoder = cand
                break
    if op_decoder is None:
        try:
            from ck_concept_learner import semantic_decode  # type: ignore
            op_decoder = semantic_decode
        except Exception:
            def op_decoder(t):
                return []

    counts: Dict[str, int] = {}
    for path, friendly, tier in SELF_TARGETS:
        if not path.exists():
            counts[friendly] = -1  # missing
            continue
        chunks = chunk_file(path, friendly)
        added = 0
        for name, body in chunks:
            # Don't clobber existing user-taught content
            existing = store.lookup(name)
            if existing is not None and existing.source_session == "user_taught":
                continue
            try:
                ops = op_decoder(body)
            except Exception:
                ops = []
            if not isinstance(ops, list):
                ops = []
            ops = [int(o) % 10 for o in ops if isinstance(o, (int, float))][:10]
            try:
                c = NamedConcept(
                    name=name,
                    definition=body[:600],
                    operator_signature=ops,
                    pattern_used="self_study",
                    source_session="self_study",
                    learned_ts=time.time(),
                    tier=tier,
                    source_file=str(path),
                )
                store.concepts[name.lower()] = c
                store._add_to_cell_index(c)
                added += 1
            except Exception:
                continue
        counts[friendly] = added

    # Persist
    try:
        store.save()
    except Exception:
        pass
    return counts


# ─── CLI ───────────────────────────────────────────────────────────────

def main():
    import argparse, json
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    args = ap.parse_args()

    print("CK reading himself...")
    counts = ingest_self()
    print()
    print(f"{'FILE':30s}  {'CONCEPTS'}")
    print(f"{'-'*30}  {'-'*8}")
    total = 0
    for k, v in counts.items():
        if k == "_error":
            print(f"  ERROR: {v}")
            continue
        if v < 0:
            print(f"  {k:30s}  (missing)")
        else:
            print(f"  {k:30s}  {v}")
            total += v
    print(f"{'-'*30}  {'-'*8}")
    print(f"  {'TOTAL':30s}  {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
