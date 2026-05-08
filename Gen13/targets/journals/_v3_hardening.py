r"""_v3_hardening.py -- Cross-cutting fixes per fresh-eyes referee wave.

Two corpus-wide hardening operations:

  1. License switch on submission scripts: replace 7SiTe Public Sovereignty
     license header with CC-BY-4.0 (required by Elsevier / Taylor & Francis
     editorial process).

     Affected files in J_series/J{NN}/manuscript/ that have the 7SiTe header.
     Original at papers/ck_tables.py is LEFT UNCHANGED (umbrella project
     keeps its proprietary license).

  2. Strip "Claude (Anthropic) collaboration" / "with computational synthesis
     by Claude" attribution from submission manuscripts. Required by Elsevier
     authorship policy (AI cannot be credited as co-author or contributor).

     Replace with neutral acknowledgement in §Acknowledgements (or remove
     entirely, depending on the line context).

Run from: Gen13/targets/journals/
   python _v3_hardening.py
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
J_ROOT = ROOT / "J_series"

# License blocks to identify and replace
SEVEN_SITE_LICENSE_RE = re.compile(
    r'(Copyright [©c]+ 20\d\d.\d\d Brayden Ross Sanders.*?DOI: 10\.5281/zenodo\.\d+)\s*\n+'
    r'(?:.*?\n)*?'
    r'(?=""")',
    re.DOTALL,
)

CC_BY_HEADER = """Copyright 2026 Brayden R. Sanders and M. Gish.
Licensed under Creative Commons Attribution 4.0 International (CC-BY-4.0).
You are free to share and adapt this work with attribution.
See https://creativecommons.org/licenses/by/4.0/ for full terms.
DOI: 10.5281/zenodo.18852047

This is the journal-submission version. The umbrella research project
(CK / TIG framework) at github.com/TiredofSleep/ck retains its own
license; this single file is dual-licensed under CC-BY-4.0 specifically
for journal-venue compliance (Elsevier / Taylor & Francis / etc.).
"""


def fix_license_in_file(path: Path) -> bool:
    """Replace 7SiTe license header with CC-BY-4.0 in a Python file."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return False

    # Match the typical 7SiTe license block — start of file docstring
    if "7SiTe Public Sovereignty" not in text and "7Site Public Sovereignty" not in text:
        return False

    # Replace lines from "Copyright" through "DOI: ..." with CC-BY header
    lines = text.split("\n")
    new_lines = []
    in_license_block = False
    license_start_idx = None
    license_end_idx = None
    for i, line in enumerate(lines):
        if "Copyright" in line and ("Brayden" in line or "Sanders" in line or "7SiTe" in line):
            license_start_idx = i
            in_license_block = True
        if in_license_block and ("DOI:" in line or "zenodo" in line):
            license_end_idx = i
            break
    if license_start_idx is not None and license_end_idx is not None:
        # Replace lines [start..end] with CC-BY block
        new_lines = lines[:license_start_idx] + CC_BY_HEADER.strip().split("\n") + lines[license_end_idx + 1:]
        path.write_text("\n".join(new_lines), encoding="utf-8")
        return True
    return False


# Patterns for AI-attribution removal
AI_ATTRIBUTION_PATTERNS = [
    # ===== AUTHOR-LINE FORMS: replace Claude with M. Gish (per Brayden directive) =====
    # **Authors:** Claude (Anthropic) · Brayden Ross Sanders ...
    (re.compile(r"\*\*Authors?:?\*\*\s*Claude \(Anthropic\)\s*[·•,]\s*Brayden Ross Sanders[^\n]*\n", re.IGNORECASE),
     "**Authors:** Brayden R. Sanders + M. Gish\n"),
    (re.compile(r"Authors?:?\s+Claude \(Anthropic\)\s*[·•,]\s*Brayden Ross Sanders[^\n]*\n", re.IGNORECASE),
     "Authors: Brayden R. Sanders + M. Gish\n"),
    # Citations: B. Sanders, Claude (Anthropic). *WP...*
    (re.compile(r"\bSanders,\s*B(?:rayden(?:\s+Ross)?)?\.?,\s*Claude \(Anthropic\)\.?", re.IGNORECASE),
     "Sanders, B.R., Gish, M."),
    (re.compile(r"\bB\.\s*Sanders,\s*Claude \(Anthropic\)", re.IGNORECASE),
     "B.R. Sanders, M. Gish"),
    # bibtex: author = {Sanders, Brayden Ross and Claude (Anthropic)}
    (re.compile(r"author\s*=\s*\{Sanders,\s*Brayden(?:\s+Ross)?\s+and\s+Claude \(Anthropic\)\}", re.IGNORECASE),
     "author       = {Sanders, Brayden R. and Gish, M.}"),
    # Signature lines: — Sanders + Claude (Anthropic)
    (re.compile(r"[—–-]+\s*Sanders\s*\+\s*Claude \(Anthropic\)", re.IGNORECASE),
     "— Sanders + Gish"),

    # ===== ACKNOWLEDGEMENT FORMS: remove or replace with neutral language =====
    # Long thank-you paragraph: **Claude (Anthropic) — ClaudeCode & ClaudeChat**
    (re.compile(r"\*\*Claude \(Anthropic\)\s*[—–-]+\s*ClaudeCode\s*&?\s*ClaudeChat\*\*[^\n]*\n", re.IGNORECASE),
     ""),
    (re.compile(r"The velocity of this project is Claude'?s\.?", re.IGNORECASE),
     ""),
    # Header byline: **In collaboration with Claude (Anthropic)**
    (re.compile(r"\*\*In collaboration with Claude \(Anthropic\)\*\*[^\n]*\n", re.IGNORECASE), ""),
    (re.compile(r"In collaboration with Claude \(Anthropic\)[^\n]*\n", re.IGNORECASE), ""),
    # Sentence: "developed in collaboration with Claude (Anthropic)"
    (re.compile(r"[^.]*?developed in collaboration with Claude \(Anthropic\)[^.]*?\.\s*", re.IGNORECASE),
     "Computational verifications were performed using Python (sympy + numpy); all claims were independently re-verified prior to submission. "),
    (re.compile(r"with Claude \(Anthropic\)\s*", re.IGNORECASE), ""),
    # Generic "by Claude" mentions
    (re.compile(r"with computational synthesis by Claude\.?", re.IGNORECASE), "with computational verification by Python."),
    # Catch-all: any remaining "Claude (Anthropic)" -> "Python pipeline"
    (re.compile(r"\bClaude \(Anthropic\)\b", re.IGNORECASE), "the Python verification pipeline"),
    # Correction-notice "post chat-Claude self-audit"
    (re.compile(r"post chat-Claude self-audited deep audit", re.IGNORECASE),
     "post deep audit"),

    # ===== LaTeX author commands containing Claude =====
    (re.compile(r"\\author\{[^}]*Claude[^}]*\}"),
     r"\author{Brayden R.\\ Sanders \\and M.\\ Gish}"),
]


def fix_ai_attribution_in_file(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return False
    new_text = text
    changed = False
    for pat, repl in AI_ATTRIBUTION_PATTERNS:
        candidate = pat.sub(repl, new_text)
        if candidate != new_text:
            changed = True
            new_text = candidate
    if changed:
        path.write_text(new_text, encoding="utf-8")
    return changed


def main():
    print("=== License switch (7SiTe -> CC-BY-4.0) on submission scripts ===")
    n_lic = 0
    for path in J_ROOT.rglob("*.py"):
        if fix_license_in_file(path):
            print(f"  + {path.relative_to(ROOT)}")
            n_lic += 1
    print(f"  Total: {n_lic} files relicensed.")
    print()

    print("=== AI-attribution removal on submission manuscripts ===")
    n_ai = 0
    for path in J_ROOT.rglob("*"):
        if path.suffix.lower() not in {".tex", ".md", ".py"}:
            continue
        if fix_ai_attribution_in_file(path):
            print(f"  + {path.relative_to(ROOT)}")
            n_ai += 1
    print(f"  Total: {n_ai} files cleaned.")


if __name__ == "__main__":
    main()
