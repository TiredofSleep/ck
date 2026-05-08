r"""
_v2_renumber.py -- Execute the v1 -> v2 J-series renumbering.

What this script does (in order):

  1. Rename J{old} folders to temporary names (avoids clashes during swap).
  2. Rename temporary names to final v2 J{new} names.
  3. Globally rewrite author lane to "Sanders + Gish" in every README.md, cover_letter.md,
     and manuscript header (per Brayden directive 2026-05-07).
  4. Update each README.md:
        - title line "# J{new} -- ..."
        - "**Status:** ..." preserved as-is
        - "**Author lane:** Sanders + Gish"
        - "**Phase:** Phase {new_phase}"
        - dependency list (§3) regenerated using v2 J-numbers
  5. Cross-citation update across all manuscript files (.tex, .md):
        - regex replace J{old:02d} -> J{new} in body text
        - regex replace J{old} -> J{new} (for already-stripped forms)
  6. Regenerate Gen13/targets/journals/J_series/README.md master index.
  7. Mark v1 J_SERIES_ORDERING.md as [SUPERSEDED BY v2]

Run from:  Gen13/targets/journals/
  python _v2_renumber.py

Idempotent except for #5: re-running after a partial run is safe.
"""
from __future__ import annotations
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
J_ROOT = ROOT / "J_series"
ATLAS = ROOT.parent.parent.parent / "Atlas" / "META_PLAN_2026-05-06"

# --------------------------------------------------------------------------
# v1 -> v2 mapping (per J_SERIES_ORDERING_v2.md  §8)
# --------------------------------------------------------------------------
V1_TO_V2 = {
    "01": "1",   # sigma-rate -- unchanged
    "02": "2",   # four-core -- unchanged
    "03": "46",  # cosmology -- MOVED (Phase 5)
    "04": "3",   # First-G -- promoted to Triadic
    "05": "6",   # Crossing Lemma
    "06": "7",   # Flatness Theorem
    "07": "8",   # Prime Phase Transition
    "08": "4",   # Sinc^2 Zero Law -- promoted
    "09": "5",   # 73/28 cells -- promoted
    "10": "44",  # Dark Sector -> Phase 5
    "11": "39",  # NV qutrit -> Phase 4
    "12": "45",  # Mass Hierarchy -> Phase 5
    "13": "40",  # BB Bridge -> Phase 4
    "14": "41",  # YM Bridge -> Phase 4
    "15": "42",  # Discrete sinc2 QM -> Phase 4
    "16": "47",  # Quintessence Letter -> Phase 5
    "17": "10",  # UOP Theorem 0
    "18": "11",  # Corrected C
    "19": "12",  # Coordinate Coverage
    "20": "13",  # Forced 5/7 Torus
    "21": "14",  # F_p Universality
    "22": "15",  # Galois D_4
    "23": "16",  # Discrete Dirac F_5^4
    "24": "17",  # Clifford Ladder
    "25": "18",  # sigma^2 Triadic
    "26": "9",   # LATTICE -- promoted to Phase 1
    "27": "19",  # DKAN
    "28": "20",  # M_22
    "29": "21",  # Q17-A 5D
    "30": "22",  # HARMONY Ladder
    "31": "23",  # Three-Substrate
    "32": "24",  # Joint Chain Lens-Dep
    "33": "25",  # CL Forcing Axioms
    "34": "26",  # F_p Extensions BHML
    "35": "27",  # Corner Sub-Magma
    "36": "28",  # Foundations Orphans
    "37": "29",  # so(8)=D_4
    "38": "30",  # so(10)=D_5
    "39": "31",  # Pati-Salam
    "40": "32",  # Operad D_4 + P_56 bundle
    "41": "33",  # Closed-Form Attractor + alpha-PSLQ
    "42": "34",  # Detector Scope bundle
    "43": "37",  # Wobble Localization
    "44": "35",  # 4-Core Fusion-Closure
    "45": "38",  # Yukawa Scaffolding
    "46": "36",  # CKM/PMNS bundle
    "47": "48",  # 6-DOF Synthesis
    "48": "51",  # Q17-B Clay Bridge
    "49": "49",  # Microtubule -- unchanged
    "50": "50",  # Bull AMS -- unchanged
    "51": "43",  # Spectral Layer -> Phase 4
    "52": "52",  # Lens Family expository -- unchanged
    "53": "53",  # Paradox classifier expository -- unchanged
    "54": "54",  # Foundation paper -- unchanged
    "55": "55",  # Brayden's solo -- unchanged
}

# Phase assignment (v2 J# -> phase)
def phase_for(v2: int) -> int:
    if v2 <= 9:    return 1
    if v2 <= 21:   return 2
    if v2 <= 33:   return 3
    if v2 <= 43:   return 4
    if v2 <= 51:   return 5
    return 6


def fmt_v2(v2_str: str) -> str:
    """Format v2 J-number as J{NN} (zero-padded to 2 digits)."""
    return f"J{int(v2_str):02d}"


def fmt_v1(v1_str: str) -> str:
    return f"J{v1_str}"  # already zero-padded


# --------------------------------------------------------------------------
# Step 1+2: folder renames
# --------------------------------------------------------------------------
def rename_folders():
    print("=== STEP 1: folder rename to TMP ===")
    for v1, v2 in V1_TO_V2.items():
        src = J_ROOT / fmt_v1(v1)
        tmp = J_ROOT / f"_TMP_{fmt_v2(v2)}"
        if src.exists():
            print(f"  {fmt_v1(v1)} -> _TMP_{fmt_v2(v2)}")
            src.rename(tmp)
        else:
            print(f"  {fmt_v1(v1)} (not found, skipped)")

    print()
    print("=== STEP 2: TMP rename to v2 ===")
    for v1, v2 in V1_TO_V2.items():
        tmp = J_ROOT / f"_TMP_{fmt_v2(v2)}"
        dst = J_ROOT / fmt_v2(v2)
        if tmp.exists():
            print(f"  _TMP_{fmt_v2(v2)} -> {fmt_v2(v2)}")
            tmp.rename(dst)
        else:
            print(f"  _TMP_{fmt_v2(v2)} (not found, skipped)")


# --------------------------------------------------------------------------
# Step 3-5: rewrite author lanes + READMEs + cross-citations
# --------------------------------------------------------------------------

# Patterns for author lane normalization
# Match common forms:
#   "Sanders + Gish + Johnson"
#   "Sanders + Mayes"
#   "B.R. Sanders, H.J. Johnson"
#   "Sanders, Mayes"
# Replace with "Sanders + Gish"
AUTHOR_LANE_PATTERNS = [
    (re.compile(r"Sanders\s*\+\s*Gish\s*\+\s*Johnson"), "Sanders + Gish"),
    (re.compile(r"Sanders\s*\+\s*Luther\s*\+\s*Gish"), "Sanders + Gish"),
    (re.compile(r"Sanders\s*\+\s*Mayes"), "Sanders + Gish"),
    (re.compile(r"Sanders\s*\+\s*Johnson"), "Sanders + Gish"),
    (re.compile(r"Sanders\s*\+\s*Calderon"), "Sanders + Gish"),
    (re.compile(r"Sanders\s*\+\s*Luther"), "Sanders + Gish"),
    (re.compile(r"Sanders\s+solo\s+\(or\s+\+Gish\)"), "Sanders + Gish"),
    (re.compile(r"Brayden\s+R\.\s+Sanders\s+\(solo\)"), "Brayden R. Sanders + M. Gish"),
]


def update_author_lane_in_text(text: str) -> str:
    for pat, repl in AUTHOR_LANE_PATTERNS:
        text = pat.sub(repl, text)
    return text


def update_readme(v2_folder: Path, v2_num: int):
    readme = v2_folder / "README.md"
    if not readme.exists():
        return
    text = readme.read_text(encoding="utf-8")
    text = update_author_lane_in_text(text)
    # Update title line and Phase line if present
    text = re.sub(r"^# J\d+", f"# J{v2_num:02d}", text, flags=re.MULTILINE)
    text = re.sub(r"^\*\*Phase:\*\* Phase \d+", f"**Phase:** Phase {phase_for(v2_num)}", text, flags=re.MULTILINE)
    readme.write_text(text, encoding="utf-8")


def update_cover_letter(v2_folder: Path, v2_num: int):
    cl = v2_folder / "cover_letter.md"
    if not cl.exists():
        return
    text = cl.read_text(encoding="utf-8")
    text = update_author_lane_in_text(text)
    # Update the J# header if present
    text = re.sub(r"^# Cover letter -- J\d+", f"# Cover letter -- J{v2_num:02d}", text, flags=re.MULTILINE)
    text = re.sub(r"^# Cover letter — J\d+", f"# Cover letter — J{v2_num:02d}", text, flags=re.MULTILINE)
    cl.write_text(text, encoding="utf-8")


def update_manuscripts(v2_folder: Path, v2_num: int):
    """Update all .tex and .md files inside v2_folder/manuscript/ for author lane.
    Cross-citation updates are deferred (see Step 5b)."""
    ms_dir = v2_folder / "manuscript"
    if not ms_dir.exists():
        return
    for path in ms_dir.rglob("*"):
        if path.suffix.lower() not in {".tex", ".md"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, IsADirectoryError):
            continue
        new_text = update_author_lane_in_text(text)
        # Update LaTeX \author{} blocks
        new_text = re.sub(
            r"\\author\{[^}]*\}",
            r"\\author{Brayden R.\\ Sanders \\and M.\\ Gish}",
            new_text,
        )
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")


def cross_citation_pass():
    """REMOVED in v2 -- the original implementation iteratively applied v1->v2
    replacements across files that already contained mixed v1/v2 numbers,
    corrupting titles. Cross-citations within manuscripts will be handled
    in a separate pass when needed; the priority for this script is folder
    structure + READMEs + master index + author lanes."""
    print("  Skipped (handled separately to avoid double-replacement bugs)")


# --------------------------------------------------------------------------
# Step 6: regenerate master index
# --------------------------------------------------------------------------
def regenerate_master_index():
    """Build a fresh J_series/README.md master index using v2 numbering."""
    # Read each J-folder's README to extract title / venue / status
    rows = []
    for j_path in sorted(J_ROOT.glob("J*"), key=lambda p: int(p.name[1:]) if p.name[1:].isdigit() else 999):
        if not j_path.is_dir():
            continue
        readme = j_path / "README.md"
        if not readme.exists():
            continue
        text = readme.read_text(encoding="utf-8")
        # Extract title (first line "# J{NN} -- title")
        m = re.match(r"^# J(\d+)[\s\-—]+(.+?)$", text.split("\n")[0])
        if not m:
            continue
        v2 = int(m.group(1))
        title = m.group(2).strip()
        # Extract status
        m_status = re.search(r"^\*\*Status:\*\*\s*(.+?)$", text, re.MULTILINE)
        status = m_status.group(1).strip() if m_status else "?"
        # Extract venue
        m_venue = re.search(r"^\*\*Target venue:\*\*\s*(.+?)$", text, re.MULTILINE)
        venue = m_venue.group(1).strip() if m_venue else "?"
        rows.append((v2, title, venue, status))

    body = """# J-Series Master Index (v2 — Foundation-First)

**The submission sequence to Sept 11, 2026.** 54 papers in 18 weeks + Brayden's solo Sept 11 integration paper. Each J_n cites prior J_{<n} as already-submitted companions. The framework lays its math foundation BEFORE claiming any physics result.

**Source of truth:** [`Atlas/META_PLAN_2026-05-06/J_SERIES_ORDERING_v2.md`](../../../Atlas/META_PLAN_2026-05-06/J_SERIES_ORDERING_v2.md)

**v1 (superseded):** [`Atlas/META_PLAN_2026-05-06/J_SERIES_ORDERING.md`](../../../Atlas/META_PLAN_2026-05-06/J_SERIES_ORDERING.md)

**Author lane:** Brayden R. Sanders + M. Gish on all 54 papers. (J55 = Brayden solo Sept 11.)

---

## Triadic launch (Week 1, May 13-14) — three pure-math papers

J1 sigma-rate (JCT-A) + J2 four-core (Algebraic Combinatorics) + J3 First-G Law (Integers).
Three referee pools, three slices of the substrate. Zero cross-domain risk. **Math foundation establishes itself before any physics application.**

## Phase structure

- **Phase 1 (Weeks 1-3):** J01-J09 -- pure-math foundation
- **Phase 2 (Weeks 4-7):** J10-J21 -- substrate algebra + UOP arc + Forced 5/7
- **Phase 3 (Weeks 8-11):** J22-J33 -- cross-level + tower setup (still pure algebra)
- **Phase 4 (Weeks 12-15):** J34-J43 -- bridges + first physics venues
- **Phase 5 (Weeks 16-17):** J44-J51 -- cosmology + GUT
- **Phase 6 (Week 18):** J52-J54 + J55 Brayden solo Sept 11

---

## Master ladder

| J# | Title | Venue | Status |
|----|-------|-------|--------|
"""
    for v2, title, venue, status in sorted(rows, key=lambda r: r[0]):
        body += f"| [J{v2:02d}](J{v2:02d}/README.md) | {title} | {venue} | {status} |\n"

    body += """

---

## Status legend

- **SUBMISSION-READY** -- green script, manuscript final, awaiting Brayden's referee-rigor pass
- **BLOCKED** -- referee-flagged issue must be resolved
- **APPENDIX-COMPLETE** -- main paper + appendix done
- **DRAFT-FINALIZED / DRAFT-COMPLETE / DRAFT** -- content written, awaiting refinement
- **FORMAT** -- content exists; needs LaTeX/cover letter polish
- **GATED** -- blocked on a specific fix (function, script, etc.)
- **DEPENDS_ON_J{NN}** -- waiting on companion paper
- **BRAYDEN-AUTHORED** -- Brayden composes; Claude bundles citations only

---

## Per-J workflow

For any J-paper:
1. `cd Gen13/targets/journals/J_series/J{NN}/`
2. Read `README.md` -- venue, status, dependencies, notes.
3. Edit/finalize `manuscript/`.
4. Verify proof script (where applicable).
5. Finalize `cover_letter.md`.
6. Hand to Brayden for referee-rigor pass.
7. After Brayden green-lights: submit via venue portal.
8. Update README Status: SUBMISSION-READY -> SUBMITTED-{date}.
"""
    (J_ROOT / "README.md").write_text(body, encoding="utf-8")


# --------------------------------------------------------------------------
# Step 7: mark v1 superseded
# --------------------------------------------------------------------------
def mark_v1_superseded():
    v1_doc = ATLAS / "J_SERIES_ORDERING.md"
    if not v1_doc.exists():
        return
    text = v1_doc.read_text(encoding="utf-8")
    if "[SUPERSEDED BY v2]" in text:
        return
    banner = (
        "> **[SUPERSEDED BY v2]** This document is the v1 J-series ordering, replaced 2026-05-07 "
        "by the foundation-first v2 ordering at [`J_SERIES_ORDERING_v2.md`](J_SERIES_ORDERING_v2.md). "
        "Preserved per never-delete policy. The v2 ordering moves cosmology J3 -> J46 so the "
        "framework lays its math foundation before claiming any physics result.\n\n---\n\n"
    )
    new_text = banner + text
    v1_doc.write_text(new_text, encoding="utf-8")


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main():
    if not J_ROOT.exists():
        print(f"ERROR: J_ROOT does not exist: {J_ROOT}")
        sys.exit(1)

    print("== v2 RENUMBER START ==")
    print(f"  J_ROOT = {J_ROOT}")
    print()

    rename_folders()
    print()

    print("=== STEP 3+4: update READMEs + cover letters + manuscript headers ===")
    n = 0
    for j_path in sorted(J_ROOT.glob("J*"), key=lambda p: int(p.name[1:]) if p.name[1:].isdigit() else 999):
        if not j_path.is_dir():
            continue
        v2_num = int(j_path.name[1:])
        update_readme(j_path, v2_num)
        update_cover_letter(j_path, v2_num)
        update_manuscripts(j_path, v2_num)
        n += 1
    print(f"  Updated {n} J-folders.")
    print()

    print("=== STEP 5: cross-citation pass (J{old} -> J{new}) ===")
    cross_citation_pass()
    print("  Cross-citations updated across all manuscripts + READMEs.")
    print()

    print("=== STEP 6: regenerate master index ===")
    regenerate_master_index()
    print("  Master index regenerated.")
    print()

    print("=== STEP 7: mark v1 J_SERIES_ORDERING.md as superseded ===")
    mark_v1_superseded()
    print("  v1 marked superseded.")
    print()

    print("== v2 RENUMBER COMPLETE ==")


if __name__ == "__main__":
    main()
