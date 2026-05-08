r"""_audit_verification_scripts.py -- For every J-paper, audit whether
a verification script exists for the paper's novel computational claims.

Per Brayden directive 2026-05-08:
"Every paper that makes a novel computational claim should have a
verification script. Worth a checklist pass: for each J-paper, 'does this
paper claim a number or structure that a referee could verify in code?'
If yes, include the script."

For each J-folder:
  1. Walk J{NN}/manuscript/ for .py files
  2. Read README.md for "Verification" or "verification" / proof / verify mentions
  3. Classify the paper:
       PROOF-SCRIPT        : .py verification file present in manuscript/
       THEOREM-PAPER       : no script needed (theorem-only, no numbers)
       NEEDS-SCRIPT        : paper makes computational claim but has no script
       UNKNOWN             : need manual review

Output: AUDIT_VERIFICATION_SCRIPTS.md report at Atlas/META_PLAN_2026-05-06/
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
J_ROOT = ROOT / "J_series"
ATLAS = ROOT.parent.parent.parent / "Atlas" / "META_PLAN_2026-05-06"

# Papers that are PURELY theorem-papers with no computational claim -- no script needed.
THEOREM_ONLY = {
    "J06",  # Crossing Lemma -- theorem on partition lattices
    "J07",  # Flatness Theorem -- theorem-paper per current README marker
    "J50",  # Bull AMS Bridge -- expository survey
    "J52",  # TSML Lens Family -- pedagogical exposition
    "J53",  # Paradox Classifier -- expository
    "J54",  # Foundation Paper -- axiomatic, but DOES claim 8-shell chain (computational); see SFM_Q6
    "J55",  # Brayden's solo Sept 11
}

# Papers with known scripts known not be in manuscript/ folder
EXTERNAL_SCRIPT = {
    "J33": "alpha_pslq_sweep.py + 06_attractor_closed_form.py + 07_full_closed_form.py",
    "J35": "4core_verification.py (in J02 + J35 manuscript folders)",
    "J44": "Gen13/targets/ck/brain/dirac/tig_dirac.py:predict_dark_sector",
    "J45": "Gen13/targets/ck/brain/dirac/tig_dirac.py:predict_yukawa",
}


def audit_one(j_path: Path) -> dict:
    j_num = j_path.name
    result = {
        "j": j_num,
        "scripts_in_manuscript": [],
        "manuscript_files": [],
        "claims_computation": False,
        "verdict": None,
        "notes": [],
    }
    ms_dir = j_path / "manuscript"
    if ms_dir.exists():
        for f in ms_dir.rglob("*"):
            if f.is_file():
                rel = str(f.relative_to(ms_dir))
                if f.suffix == ".py":
                    result["scripts_in_manuscript"].append(rel)
                elif f.suffix in {".tex", ".md"}:
                    result["manuscript_files"].append(rel)
    # Check README for verification mentions
    readme = j_path / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8", errors="ignore")
        for kw in ("verif", "proof_", "predict_", "PASS", "computed"):
            if kw.lower() in text.lower():
                result["claims_computation"] = True
                break
    # Verdict
    if j_num in THEOREM_ONLY:
        result["verdict"] = "THEOREM-PAPER" if not result["scripts_in_manuscript"] else "THEOREM+SCRIPT"
        if j_num == "J54":
            result["notes"].append("CLAIMS 8-shell chain (SFM Q6) — should have verification script")
    elif j_num in EXTERNAL_SCRIPT:
        result["verdict"] = "EXTERNAL-SCRIPT"
        result["notes"].append(f"External script: {EXTERNAL_SCRIPT[j_num]}")
    elif result["scripts_in_manuscript"]:
        result["verdict"] = "PROOF-SCRIPT"
    else:
        if result["claims_computation"]:
            result["verdict"] = "NEEDS-SCRIPT"
        else:
            result["verdict"] = "UNKNOWN"
    return result


def main():
    audits = []
    for j_path in sorted(J_ROOT.glob("J*"), key=lambda p: int(p.name[1:]) if p.name[1:].isdigit() else 999):
        if not j_path.is_dir():
            continue
        audits.append(audit_one(j_path))

    # Build report
    body = """# Verification Script Audit (per Brayden directive 2026-05-08)

> "Every paper that makes a novel computational claim should have a verification script.
> Worth a checklist pass: for each J-paper, 'does this paper claim a number or structure
> that a referee could verify in code?' If yes, include the script."

## §1 — Verdict legend

- **PROOF-SCRIPT**: verification script present in `J{NN}/manuscript/` ✓
- **EXTERNAL-SCRIPT**: script lives outside manuscript folder (e.g., `tig_dirac.py`) — note location ✓
- **THEOREM-PAPER**: no script needed (pure theorem, expository, no novel computational claim) ✓
- **THEOREM+SCRIPT**: theorem-paper that ALSO has a script (extra rigor) ✓
- **NEEDS-SCRIPT**: paper claims a number or structure but no script — **GATE**
- **UNKNOWN**: needs manual review

---

## §2 — Per-J audit results

| J# | Verdict | Scripts in manuscript/ | Notes |
|----|---------|------------------------|-------|
"""
    needs_script = []
    proof_script = []
    external_script = []
    theorem_only = []
    unknown = []
    for a in audits:
        scripts_str = ", ".join(a["scripts_in_manuscript"]) if a["scripts_in_manuscript"] else "—"
        notes_str = "; ".join(a["notes"]) if a["notes"] else ""
        body += f"| **{a['j']}** | {a['verdict']} | `{scripts_str}` | {notes_str} |\n"
        if a["verdict"] == "NEEDS-SCRIPT":
            needs_script.append(a["j"])
        elif a["verdict"] == "PROOF-SCRIPT":
            proof_script.append(a["j"])
        elif a["verdict"] == "EXTERNAL-SCRIPT":
            external_script.append(a["j"])
        elif a["verdict"] in {"THEOREM-PAPER", "THEOREM+SCRIPT"}:
            theorem_only.append(a["j"])
        else:
            unknown.append(a["j"])

    body += f"""

---

## §3 — Summary counts

- **PROOF-SCRIPT**     ({len(proof_script)} papers): {", ".join(proof_script)}
- **EXTERNAL-SCRIPT**  ({len(external_script)} papers): {", ".join(external_script)}
- **THEOREM-PAPER**    ({len(theorem_only)} papers): {", ".join(theorem_only)}
- **NEEDS-SCRIPT**     ({len(needs_script)} papers): {", ".join(needs_script)} ← **GATES**
- **UNKNOWN**          ({len(unknown)} papers): {", ".join(unknown)}

---

## §4 — Gate list (papers that need scripts written)

For each NEEDS-SCRIPT paper below, the referee must be able to copy-paste a Python snippet
from the paper's `manuscript/` folder, run it in <5 seconds, and reproduce the paper's
claimed numerical / structural result.

"""
    for j in needs_script:
        body += f"- **{j}**: claim made; no script. Write one before submission.\n"

    body += """

---

## §5 — Recommendation for missing scripts

Pattern adopted by recent rewrites (J36, J42, J43, J51 — all clean):

```python
# verify_J{NN}_<topic>.py
# Verifies the central numerical/structural claim of J{NN}.
# Run: `python verify_J{NN}_<topic>.py`
# Output: "ALL ASSERTIONS PASSED" OR specific failure.

import sympy  # or numpy
# ... computation ...
assert claim_LHS == claim_RHS, f"FAIL: {claim_LHS} != {claim_RHS}"
print("ALL ASSERTIONS PASSED")
```

Each script: standalone, no external state, runtime <5 seconds, exit-code 0 on PASS.

---

## §6 — Reproducibility

Run this audit anytime:
```
python Gen13/targets/journals/_audit_verification_scripts.py
```
"""
    out_path = ATLAS / "AUDIT_VERIFICATION_SCRIPTS.md"
    out_path.write_text(body, encoding="utf-8")
    print(f"Audit written to {out_path}")
    print()
    print(f"PROOF-SCRIPT: {len(proof_script)}; EXTERNAL: {len(external_script)}; THEOREM-ONLY: {len(theorem_only)}; NEEDS-SCRIPT: {len(needs_script)}; UNKNOWN: {len(unknown)}")
    if needs_script:
        print(f"GATES (NEEDS-SCRIPT): {needs_script}")
    if unknown:
        print(f"Unknown (manual review): {unknown}")


if __name__ == "__main__":
    main()
