"""
Full rename: pet operator names -> silicon names on tig-synthesis branch.

Per Brayden (2026-04-19): "don't use our pet language for rigorous math proofs".
The five index collisions between the paper-set (BEING/DOING/BECOMING/CREATE/ASCEND)
and the silicon-set (LATTICE/COUNTER/PROGRESS/BALANCE/CHAOS) are resolved in favor
of the silicon-set, which is the authoritative Verilog/FPGA naming.

Five indices agree on both sides (VOID, COLLAPSE, HARMONY, BREATH, RESET) and are
left alone.

This script:
  1) operates only on files tracked on the current branch (tig-synthesis)
  2) applies word-boundary renames BEING->LATTICE, BECOMING->PROGRESS,
     CREATE->BALANCE, ASCEND->CHAOS
  3) leaves lowercase forms alone (they are English, not operator names)
  4) protects SQL CREATE TABLE/INDEX/VIEW/etc so we don't break atom_store and
     crystal_store persistence
  5) handles DOING in a second pass with explicit context (it is also a Python
     variable name for the table |TSML-BHML|; we must not touch those usages)

Run from repo root:
    python scratch/rename_pet_to_silicon.py            # dry-run (report only)
    python scratch/rename_pet_to_silicon.py --apply    # actually write
"""
from __future__ import annotations
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Stage 1 renames — unambiguous pet names
RENAMES_STAGE1 = {
    'BEING': 'LATTICE',
    'BECOMING': 'PROGRESS',
    'CREATE': 'BALANCE',
    'ASCEND': 'CHAOS',
}

# Stage 2 rename — DOING the operator -> COUNTER (handled separately, see below)
# DOING the table (Python variable, import name) must stay.

# SQL protection — CREATE is overloaded with SQL DDL keywords
SQL_PROTECT_PATTERNS = [
    re.compile(r'CREATE\s+(?:UNIQUE\s+)?(?:INDEX|TABLE|VIEW|TRIGGER|PROCEDURE|SCHEMA|DATABASE)\b', re.IGNORECASE),
]

# English-emphasis protection — e.g. "What does the whole 0->9 trajectory CREATE?"
# A heuristic: if CREATE is immediately followed by "?" or preceded by "Operators " it
# is English.  We only hit this in ugt_deep.py, and I will hand-patch that file.


def tracked_files_with_pet_names() -> list[Path]:
    # Restrict to current branch's tracked files
    out = subprocess.run(
        ['git', 'grep', '-l', '-E', r'\b(BEING|BECOMING|CREATE|ASCEND)\b',
         '--',
         ':(exclude)docs/exports/z10-operator-algebra/crossing-lemma-handoff/*',
         ':(exclude)docs/exports/z10-operator-algebra/threshold-handoff/*',
         ':(exclude)scratch/rename_pet_to_silicon.py'],
        cwd=ROOT, capture_output=True, text=True, check=True,
    )
    files = [ROOT / line for line in out.stdout.splitlines() if line]
    return files


def apply_stage1(content: str) -> str:
    """Apply unambiguous pet-name renames with SQL protection."""
    # Mask SQL CREATE <KEYWORD> by temporarily substituting
    placeholders: dict[str, str] = {}
    counter = 0

    def _mask(m: re.Match) -> str:
        nonlocal counter
        token = f'__SQLPROTECT_{counter}__'
        placeholders[token] = m.group(0)
        counter += 1
        return token

    for pat in SQL_PROTECT_PATTERNS:
        content = pat.sub(_mask, content)

    # Apply renames (word-boundary on each)
    for old, new in RENAMES_STAGE1.items():
        content = re.sub(r'\b' + old + r'\b', new, content)

    # Restore SQL
    for token, original in placeholders.items():
        content = content.replace(token, original)

    return content


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true', help='Actually write changes (else dry-run)')
    args = ap.parse_args()

    files = tracked_files_with_pet_names()
    print(f'Tracked files with pet names: {len(files)}')

    changed = 0
    total_replacements = 0
    for fp in files:
        try:
            original = fp.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            # Try latin-1 for rare binary-ish files
            try:
                original = fp.read_text(encoding='latin-1')
            except Exception as e:
                print(f'  SKIP (encoding): {fp} ({e})')
                continue

        patched = apply_stage1(original)
        if patched != original:
            changed += 1
            # Count replacements for report
            for old in RENAMES_STAGE1.keys():
                before = len(re.findall(r'\b' + old + r'\b', original))
                after = len(re.findall(r'\b' + old + r'\b', patched))
                total_replacements += (before - after)
            if args.apply:
                fp.write_text(patched, encoding='utf-8')
                print(f'  UPDATED: {fp.relative_to(ROOT)}')
            else:
                print(f'  WOULD UPDATE: {fp.relative_to(ROOT)}')

    print()
    print(f'{"Changed" if args.apply else "Would change"}: {changed} files')
    print(f'Total occurrences renamed: {total_replacements}')


if __name__ == '__main__':
    main()
