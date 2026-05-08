r"""Fix J-folder README paths after copying legacy content into J{NN}/manuscript/.

For each J that has content in manuscript/, replace the legacy ../../tierN.../  pointer
with manuscript/ pointing at local files.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
J = ROOT / "J_series"

# (J#, manuscript_file_in_local, script_file_in_local)
# If script is None, it stays as-is.
LOCAL = {
    1:  ("manuscript/WP101_SIGMA_RATE_THEOREM.md", "manuscript/master/proof_sigma_rate.py"),
    2:  ("manuscript/four_core_consolidated.tex", "manuscript/4core_verification.py"),
    4:  ("manuscript/", None),
    6:  ("manuscript/WP51_FLATNESS_THEOREM.md", None),
    8:  ("manuscript/", None),
    9:  ("manuscript/", None),
    10: ("manuscript/", None),
    11: ("manuscript/", None),
    13: ("manuscript/", None),
    17: ("manuscript/", None),
    28: ("manuscript/", None),
    37: ("manuscript/", None),
    48: ("manuscript/", None),
}

PATH_PATTERNS = [
    re.compile(r'\*\*Path:\*\* `[^`]+`'),
]

def list_manuscript_files(j_num: int) -> str:
    """Return a markdown bullet list of files in the J{NN}/manuscript/ folder."""
    folder = J / f"J{j_num:02d}" / "manuscript"
    if not folder.exists():
        return "(empty)"
    items = []
    for p in sorted(folder.iterdir()):
        if p.is_file():
            items.append(f"- `{p.name}`")
        elif p.is_dir():
            items.append(f"- `{p.name}/` (subfolder)")
    return "\n".join(items) if items else "(empty)"

def fix_readme(j_num: int, ms_path: str, script_path: str | None):
    folder = J / f"J{j_num:02d}"
    readme = folder / "README.md"
    if not readme.exists():
        return
    text = readme.read_text(encoding="utf-8")

    # Update manuscript path
    file_listing = list_manuscript_files(j_num)
    new_ms_block = f"""## §1 — Manuscript

**Local path:** `{ms_path}`

Files in this J-folder's `manuscript/`:

{file_listing}

The submission package lives in this J-folder. Edit + verify here; submit from here."""
    text = re.sub(
        r"## §1 — Manuscript\n.+?(?=## §2)",
        new_ms_block + "\n\n",
        text,
        flags=re.DOTALL,
    )

    # Update script path if specified
    if script_path:
        new_script_block = f"""## §2 — Verification script

**Local path:** `{script_path}`

The proof script is the green-light gate before submission. Run from this J-folder."""
        text = re.sub(
            r"## §2 — Verification script\n.+?(?=## §3)",
            new_script_block + "\n\n",
            text,
            flags=re.DOTALL,
        )

    readme.write_text(text, encoding="utf-8")

def main():
    for j_num, (ms, script) in LOCAL.items():
        fix_readme(j_num, ms, script)
        print(f"Fixed J{j_num:02d}")

if __name__ == "__main__":
    main()
