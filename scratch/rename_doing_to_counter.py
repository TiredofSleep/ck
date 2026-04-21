"""
Stage 2 rename: DOING operator -> COUNTER, preserving DOING as table variable.

The word DOING has two meanings in this codebase:
  (1) the OPERATOR at index 2 of Z/10Z — renamed to COUNTER
  (2) the derived TABLE |TSML - BHML| — stays as DOING (it's a Python variable name)

This script walks each tracked file, and for each line, checks whether DOING is
used in an operator-name context or a table-variable context. Only operator-context
uses are renamed.

Usage:
    python scratch/rename_doing_to_counter.py            # dry-run
    python scratch/rename_doing_to_counter.py --apply    # execute
"""
from __future__ import annotations
import argparse
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# If a line matches ANY of these, DOING on that line is the table variable — do NOT rename.
# Tuned from a manual audit of tracked files on tig-synthesis — only keep patterns
# that match clearly-table contexts, never operator-list prose.
TABLE_PATTERNS = [
    # Python variable assignment / definition
    re.compile(r'^\s*DOING\s*=\s*_make_doing'),            # DOING = _make_doing()
    re.compile(r'^\s*DOING\s*=\s*\|'),                     # DOING = |TSML - BHML| (definition)
    re.compile(r'\bDOING\s*=\s*\|'),                       # DOING=|TSML-BHML| (definition, anywhere)
    re.compile(r'\bDOING\['),                              # DOING[i][j] (table indexing)
    # Imports
    re.compile(r'from\s+\S+\s+import.*\bDOING\b'),         # from X import ... DOING
    re.compile(r'\bimport\s[^\n]*\bDOING\b'),              # import DOING
    # Derived variables
    re.compile(r'DOING_sum'),                              # doing-table sum variable
    re.compile(r'DOING_zero'),
    re.compile(r'doing_sum|doing_zero'),
    re.compile(r'_make_doing'),                            # table factory function
    # Explicit "DOING <noun>" table phrasings
    re.compile(r'\bDOING\s+sum\b'),                        # "DOING sum"
    re.compile(r'DOING=0\s+cells'),                        # "DOING=0 cells" (table print)
    re.compile(r'\bDOING\s+cells\b'),                      # "DOING cells"
    re.compile(r'\bDOING\s+mask\b'),
    re.compile(r'\bDOING\s+table\b'),                      # "DOING table"
    re.compile(r'\bDOING\s+tables?\b'),
    re.compile(r'\bDOING\s+matrix\b'),                     # "DOING matrix" (the |TSML-BHML| matrix)
    re.compile(r'\bDOING\s+has\s+\d'),                     # "DOING has 71 nonzero cells"
    re.compile(r'\bDOING\s+is\s+the\s+OBSERVABLE'),        # WP26 phrasing
    re.compile(r'\bDOING\s+boundary\b'),                   # "DOING boundary" (table geometry)
    re.compile(r'\bDOING\s+nonzero\b'),                    # "DOING nonzero cells"
    # Module / attribute access
    re.compile(r'ck_tables\.DOING'),                       # module-qualified access
    # Function calls that take the table as arg
    re.compile(r'CROSS_CYCLE\(DOING'),                     # CROSS_CYCLE(DOING, C×D)
    # NOTE: the `'doing': DOING` dict pattern appears only in verify_ck_core.py, where
    # the local DOING (line 659) is defined as (2,3,4,5) — an operator-phase tuple.
    # That file should rename consistently to COUNTER = (2,3,4,5) + 'doing': COUNTER.
    # Prose table-list: "TSML, BHML, DIS, DOING, G tables" / "DOING, G tables"
    re.compile(r'(?:TSML|BHML|DIS)\s*,\s*DOING'),          # prose: "TSML, DOING" or "BHML, DIS, DOING"
    re.compile(r'\bDOING\s*,\s*G\s+tables?'),              # prose: "DOING, G tables"
    re.compile(r'\bDOING\s*,\s*G\s*,\s*CL\s*,'),           # prose: "DOING, G, CL, W"
    # Test file: class names
    re.compile(r'class\s+\w*DOING\w*'),                    # class TestDOINGTable:
    # Definition "DOING = |TSML - BHML|" inside a string or docstring
    re.compile(r'\bDOING\b.*\|\s*TSML'),                   # line contains DOING and |TSML
    # Section header comment in ck_tables.py
    re.compile(r'^\s*#\s*DOING\s*$'),                      # bare "# DOING" header
    # Absolute-value/definition line "DOING = |TSML-BHML|" in comments
    re.compile(r'#\s*DOING\s*=\s*\|'),                     # # DOING = |TSML - BHML| (comment)
    # |TSML ... | numeric on the line (the definition literal)
    re.compile(r'\bDOING\s*=\s*\|TSML\b'),
    # Stats-context: DOING sum=201, DOING=0 non-harmony, etc
    re.compile(r'\bDOING\b[^,\n]*(?:sum|non-harmony|nonzero|frozen)'),
    # Indexing description: DOING[i][j]= ... in docstrings
    re.compile(r'DOING\[i\]\[j\]'),
    # Python canonical-index access
    re.compile(r'DOING\[\d'),                              # DOING[0] ...
]

# If a line matches ANY of these, DOING is the operator — rename to COUNTER.
# (Used only as a positive indicator in doubt, not as the source of truth.)
OP_PATTERNS = [
    re.compile(r"'\s*DOING\s*'"),                          # 'DOING' string literal
    re.compile(r'\bDOING\s*=\s*\d'),                       # DOING=2 style
    re.compile(r'DOING\s*\(\s*\d+\s*\)'),                  # DOING(2)
    re.compile(r'\bDOING\s*[x×]\s*\w+'),                   # DOING × OTHER
    re.compile(r'\brow\s+2\s*:\s*DOING'),                  # row 2: DOING comment
    re.compile(r'2\s*:\s*DOING'),                          # 2: DOING (dict)
]


def tracked_files_with_doing() -> list[Path]:
    out = subprocess.run(
        ['git', 'grep', '-l', r'\bDOING\b', '--',
         ':(exclude)docs/exports/z10-operator-algebra/crossing-lemma-handoff/*',
         ':(exclude)docs/exports/z10-operator-algebra/threshold-handoff/*',
         ':(exclude)scratch/rename_doing_to_counter.py',
         ':(exclude)scratch/rename_pet_to_silicon.py'],
        cwd=ROOT, capture_output=True, text=True, check=True,
    )
    return [ROOT / line for line in out.stdout.splitlines() if line]


def is_table_line(line: str) -> bool:
    return any(p.search(line) for p in TABLE_PATTERNS)


def rename_line(line: str) -> tuple[str, int]:
    """Return (new_line, n_replacements_on_this_line)."""
    if is_table_line(line):
        return line, 0
    new = re.sub(r'\bDOING\b', 'COUNTER', line)
    n = line.count('DOING') - new.count('DOING')
    return new, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    files = tracked_files_with_doing()
    print(f'Files with DOING: {len(files)}')

    total_ops, total_tabs, total_files = 0, 0, 0
    for fp in files:
        try:
            original = fp.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            original = fp.read_text(encoding='latin-1')
        lines = original.splitlines(keepends=True)
        new_lines = []
        file_ops = 0
        file_tabs = 0
        for line in lines:
            if is_table_line(line):
                new_lines.append(line)
                file_tabs += line.count('DOING')
            else:
                new, n = rename_line(line)
                new_lines.append(new)
                file_ops += n
        if file_ops > 0:
            total_files += 1
            total_ops += file_ops
            total_tabs += file_tabs
            patched = ''.join(new_lines)
            if args.apply:
                fp.write_text(patched, encoding='utf-8')
                print(f'  UPDATED: {fp.relative_to(ROOT)}  ({file_ops} op, {file_tabs} tab preserved)')
            else:
                print(f'  WOULD UPDATE: {fp.relative_to(ROOT)}  ({file_ops} op, {file_tabs} tab preserved)')

    print()
    print(f'{"Changed" if args.apply else "Would change"}: {total_files} files')
    print(f'Operator DOING -> COUNTER: {total_ops}')
    print(f'Table DOING preserved:     {total_tabs}')


if __name__ == '__main__':
    main()
