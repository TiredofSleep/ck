r"""_v2_fix_citations.py -- Fix stale J{v1} citations in READMEs + cover letters.

The earlier v2_renumber script's cross_citation_pass had a double-substitution
bug. This script fixes it by using a single regex pass with a callback,
ensuring each J-number is replaced exactly once.

Scope: README.md + cover_letter.md ONLY. Manuscript files inside manuscript/
are left alone (handled separately if/when needed).
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
J_ROOT = ROOT / "J_series"

# v1 -> v2 mapping (same as renumber script)
V1_TO_V2 = {
    1: 1, 2: 2, 3: 46, 4: 3, 5: 6, 6: 7, 7: 8, 8: 4, 9: 5,
    10: 44, 11: 39, 12: 45, 13: 40, 14: 41, 15: 42, 16: 47,
    17: 10, 18: 11, 19: 12, 20: 13, 21: 14, 22: 15, 23: 16, 24: 17,
    25: 18, 26: 9, 27: 19, 28: 20, 29: 21, 30: 22, 31: 23, 32: 24,
    33: 25, 34: 26, 35: 27, 36: 28, 37: 29, 38: 30, 39: 31, 40: 32,
    41: 33, 42: 34, 43: 37, 44: 35, 45: 38, 46: 36, 47: 48, 48: 51,
    49: 49, 50: 50, 51: 43, 52: 52, 53: 53, 54: 54, 55: 55,
}

# Compile single regex matching any v1 J-number in J{NN} form (zero-padded)
_v1_pattern = re.compile(r"\bJ(\d{1,2})\b")


def _replace(match: re.Match) -> str:
    v1 = int(match.group(1))
    if v1 not in V1_TO_V2:
        return match.group(0)
    v2 = V1_TO_V2[v1]
    if v1 == v2:
        return f"J{v2:02d}"  # normalize to 2-digit form
    return f"J{v2:02d}"


def fix_file(path: Path, self_v2: int):
    """Replace v1 J-numbers with v2, but preserve self-reference (own J-number)
    in title/header lines so the file's identity stays correct."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return False
    self_token = f"J{self_v2:02d}"
    self_alt = f"J{self_v2}"

    def _local_replace(match: re.Match) -> str:
        v1 = int(match.group(1))
        if v1 not in V1_TO_V2:
            return match.group(0)
        v2 = V1_TO_V2[v1]
        return f"J{v2:02d}"

    # Process line-by-line; skip lines that are self-identifier headers
    lines = text.split("\n")
    out_lines = []
    for line in lines:
        # Skip title line "# J{self_v2}" + cover-letter header "# Cover letter -- J{self_v2}"
        # by replacing J{self_v2} with a sentinel BEFORE substitution, then back
        sentinel = "\x00SELF\x00"
        protected = line.replace(self_token, sentinel)
        if self_v2 < 10:
            # also protect single-digit form on title lines
            protected = protected.replace(f"J{self_v2}", sentinel) if line.startswith("#") else protected
        new_line = _v1_pattern.sub(_local_replace, protected)
        new_line = new_line.replace(sentinel, self_token)
        out_lines.append(new_line)
    new_text = "\n".join(out_lines)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main():
    n_changed = 0
    n_total = 0
    for j_path in sorted(J_ROOT.glob("J*"), key=lambda p: int(p.name[1:]) if p.name[1:].isdigit() else 999):
        if not j_path.is_dir():
            continue
        self_v2 = int(j_path.name[1:])
        for fname in ("README.md", "cover_letter.md"):
            f = j_path / fname
            if f.exists():
                n_total += 1
                if fix_file(f, self_v2):
                    n_changed += 1
    # Master index: no self-reference, use a sentinel of -1 (won't match)
    master = J_ROOT / "README.md"
    if master.exists():
        n_total += 1
        if fix_file(master, -1):
            n_changed += 1
    print(f"Updated {n_changed} of {n_total} files.")


if __name__ == "__main__":
    main()
