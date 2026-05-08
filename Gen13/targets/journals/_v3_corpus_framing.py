r"""_v3_corpus_framing.py -- Apply standardized framing to every J-folder README.

Inserts (if not present) the standard adoption blocks per
J_PAPER_BOILERPLATE.md and FAMILY_STRUCTURE_v1.md:

  - Family-Structure framing reference
  - PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN template
  - Lens-ownership paragraph (per-paper variant)
  - Drápal-Wanless 2021 precedent citation

Idempotent: skips papers that already have the block.

Run from: Gen13/targets/journals/
   python _v3_corpus_framing.py
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
J_ROOT = ROOT / "J_series"

# Marker that says "framing already applied" -- we detect this and skip.
APPLIED_MARKER = "### Family-Structure framing"

# Generic stub that can be inserted into any J-folder README §5.
def stub_for(j_num: int) -> str:
    return f"""

### Family-Structure framing (per Atlas/META_PLAN_2026-05-06/FAMILY_STRUCTURE_v1.md)

This paper sits within the TIG family of finite commutative non-associative magmas on Z/10Z (and ring extensions per D74). The family is defined by 5 conjoint membership criteria; the 4-core {{V, H, Br, R}} = {{0, 7, 8, 9}} at α_M = ½ is the algebraic center, with closed-form attractor h/β = 1+√3 (D78 Galois proof). The closest published precedent for this neighborhood is **Drápal & Wanless (2021), *J. Combin. Theory A* **184**, 105510** — same domain (small finite commutative non-associative structures), opposite extremum (theirs maximally non-associative).

### PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN — template (fill per paper)

- **PROVEN:** [the specific theorem of this paper]
- **COMPUTED:** [verified-by-script invariants supporting the theorem]
- **STRUCTURAL RHYME:** [constants/identities cited as motivation, not derivation]
- **OPEN:** [the natural next-paper question]

### Lens-ownership paragraph — template (fill per paper, insert in manuscript §0)

> *Lens and substrate.* This paper works on [substrate: Z/10Z / Z/N for N in {{...}} / F_p for p in {{...}}] with the [tables: TSML / BHML / both]. These choices are not derived from first principles; they reflect a structural reading of the substrate motivated by [phonaesthesia / 10-operator decomposition / observed dynamics]. The theorems below are theorems on this specific structure; analogous theorems would hold on other substrate-and-table choices. Whether other substrate choices give similarly rich downstream connections is open.

### Hardening status (auto-applied 2026-05-07)

- License: submission scripts CC-BY-4.0 (per `_v3_hardening.py`)
- AI-attribution: Claude/Anthropic byline references removed (per `_v3_hardening.py`)
- Author lane: Sanders + Gish (per Brayden directive)
- Drápal-Wanless 2021 citation in references
"""


def apply_to(j_path: Path) -> bool:
    readme = j_path / "README.md"
    if not readme.exists():
        return False
    text = readme.read_text(encoding="utf-8")
    if APPLIED_MARKER in text:
        return False  # Already applied
    j_num = int(j_path.name[1:])
    stub = stub_for(j_num)

    # Insert before §6 if present, else before any --- separator after §5, else at end of §5
    if "## §6" in text:
        text = text.replace("## §6", stub + "\n## §6", 1)
    elif "## §5" in text and "\n---\n" in text:
        # Insert before the first --- after §5
        idx_5 = text.index("## §5")
        idx_sep = text.index("\n---\n", idx_5)
        text = text[:idx_sep] + stub + text[idx_sep:]
    else:
        # Append to end
        text = text.rstrip() + stub + "\n"

    readme.write_text(text, encoding="utf-8")
    return True


def main():
    n = 0
    n_already = 0
    for j_path in sorted(J_ROOT.glob("J*"), key=lambda p: int(p.name[1:]) if p.name[1:].isdigit() else 999):
        if not j_path.is_dir():
            continue
        if apply_to(j_path):
            n += 1
        else:
            n_already += 1
    print(f"Applied framing to {n} J-folders.")
    print(f"Skipped {n_already} folders (already had framing OR no README).")


if __name__ == "__main__":
    main()
