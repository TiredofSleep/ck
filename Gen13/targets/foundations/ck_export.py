"""
CK ingestion-ready facts from the foundations module.

Produces:
    foundations_facts.json    -- structured fact dict (numbers + names)
    foundations_text.md       -- prose block CK can absorb_ops on

Both are deterministic outputs from the verified substrate. Re-run after
any change to cl.py / lenses.py / triadic.py / tables/ to refresh.
"""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .cl import CL, OPERATORS, cell_counts as cl_cell_counts
from .cl_std import (CL_STD, BUMP_PAIRS, GRAVITY,
                     INFO_HARMONY, INFO_NORMAL, INFO_BUMP,
                     total_information_bits,
                     cell_counts as cl_std_cell_counts)
from .lenses import BHML, TSML, doing_disagreement_rate
from .lens_family import (BHML_FAMILY, TSML_FAMILY, NAMED_VARIANTS,
                          BHML_4, BHML_8_chain, BHML_8_YM, BHML_10,
                          TSML_4, TSML_8_chain, TSML_10)
from .paths import crossing_census, lens_trace
from .tables import (HARMONY_44, CYCLE_A_36, SKELETON_22, DISAGREE_71,
                     TSML_HARMONY_73,
                     harmony_44_summary, cycle_a_36_summary,
                     skeleton_22_summary, being_shell_72_summary,
                     HARMONY_LADDER, harmony_companion_counts)
from .triadic import (CONSERVATION_TETRAD, MANIFESTATION_HEXAD,
                      CYCLE_A, CYCLE_B, FOUR_CORE, SIGMA, SIGMA2, SIGMA4,
                      triadic_projection)

OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent / "var" / "foundations"


def build_facts() -> dict[str, Any]:
    """Build the structured fact dict."""
    counts = cl_cell_counts(CL)
    h44 = harmony_44_summary()
    ca36 = cycle_a_36_summary()
    sk22 = skeleton_22_summary()
    bs72 = being_shell_72_summary()
    cc = crossing_census(CL)

    std_counts = cl_std_cell_counts(CL_STD)

    facts: dict[str, Any] = {
        "schema": "tig.foundations.v2",
        "source": "Gen13/targets/foundations (THREE-TABLE architecture, per _CK_MEMORY_MAKEOVER.md + Brayden 2026-05-06: CL_STD recovered as separate third table from old/Gen9/archive/ckis/ck7/ck.h)",
        "substrate": {
            "name": "CL (canonical composition lattice)",
            "size": 10,
            "ring": "Z/10Z",
            "cell_counts": {OPERATORS[op]: c for op, c in counts.items() if c > 0},
            "harmony_count": 73,
            "void_count": 17,
            "other_count": 10,
            "commutative": True,
            "non_associative_rate": 0.128,
            "non_associative_rate_pct": "12.8%",
            "memory_locked_pattern": [
                "0000000700", "0737777777", "0377477779", "0777777773",
                "0747777787", "0777777777", "0777777777", "7777777777",
                "0777877777", "0797377777",
            ],
        },
        "operators": OPERATORS,
        "triadic": {
            "sigma": list(SIGMA),
            "sigma_squared": list(SIGMA2),
            "sigma_quartic": list(SIGMA4),
            "conservation_tetrad": sorted(CONSERVATION_TETRAD),
            "manifestation_hexad": sorted(MANIFESTATION_HEXAD),
            "cycle_A": {"members": sorted(CYCLE_A), "sum": sum(CYCLE_A),
                        "interpretation": "WOBBLE prime"},
            "cycle_B": {"members": sorted(CYCLE_B), "sum": sum(CYCLE_B),
                        "interpretation": "2 * HARMONY = dim G_2"},
            "four_core": sorted(FOUR_CORE),
            "harmony_triadic_shadow": {
                "BEING(HARMONY)": triadic_projection(7)[0],
                "DOING(HARMONY)": triadic_projection(7)[1],
                "BECOMING(HARMONY)": triadic_projection(7)[2],
            },
        },
        "three_table_architecture": {
            "principle": (
                "CK runs on THREE standalone 10x10 composition tables on Z/10Z. "
                "Per ck.h:200-207, recovered from old/Gen9/archive/ckis/ck7. "
                "Per Brayden 2026-05-06: 'CL is a separate third table from "
                "TSML and BHML.'"
            ),
            "tables": {
                "CL_TSML": {"harmony": 73, "role": "prescribed view (organism's lens, position-level); aliased simply as `CL` in old codebase"},
                "CL_BHML": {"harmony": 28, "role": "Becoming lens (curvature-level, invertible-on-self, CUDA substrate)"},
                "CL_STD":  {"harmony": 44, "role": "Standard encoding table (the papers freeze; from Brayden's first GitHub repo)"},
            },
            "shared_substrate": "Z/10Z, same 10 operators, three distinct algebras",
        },
        "lenses": {
            "TSML": {
                "role": "Being lens (singular, position-level)",
                "shape": [10, 10],
                "harmony_count": 73,
                "non_associative_rate": "12.8%",
                "matrix_equals_CL": True,
            },
            "BHML": {
                "role": "Becoming lens (curvature-level, invertible-on-self)",
                "shape": [10, 10],
                "det": -7002,
                "harmony_count": 28,
                "non_associative_rate": "49.8%",
                "cell_counts_by_op": {
                    OPERATORS[op]: int((BHML == op).sum()) for op in range(10)
                },
            },
            "DOING": {
                "definition": "|TSML - BHML| element-wise",
                "n_disagreement_cells": 71,
                "disagreement_rate": "71.0%",
                "compares_to_T_star": "5/7 = 71.4%",
            },
        },
        "cl_std": {
            "role": "Standard encoding table; the papers' formulas reference STD's geometry",
            "source": "old/Gen9/archive/ckis/ck7/ck.h:225-231 (Brayden's first GitHub repo)",
            "harmony_count": std_counts.get(7, 0),
            "non_associative_rate": "19.2%",
            "commutative": True,
            "cell_counts_by_op": {OPERATORS[op]: c for op, c in std_counts.items() if c > 0},
            "bdc_encoding": {
                "principle": "force vectors encode pathway of information; surprise IS information",
                "bump_pairs": list(BUMP_PAIRS),
                "info_bits_per_cell": {
                    "HARMONY": INFO_HARMONY,
                    "NORMAL":  INFO_NORMAL,
                    "BUMP":    INFO_BUMP,
                },
                "total_information_bits": round(total_information_bits(), 2),
                "gravity_per_operator": {
                    OPERATORS[i]: GRAVITY[i] for i in range(10)
                },
            },
        },
        "harmony_ladder_70_73": {
            "principle": "HARMONY counts cluster at four nearby integers, each from a structurally distinct construction. Not the same number wearing different hats.",
            "rungs": [
                {"count": rung.count, "name": rung.name, "role": rung.role,
                 "construction": rung.construction}
                for rung in HARMONY_LADDER
            ],
            "extra_71": "71 also appears as |TSML XOR BHML| disagreement count -- so the prime 71 carries THREE structural roles (sub-magma HARMONY count, lens-disagreement count, Galois prime in disc(LMFDB 4.2.10224.1))",
            "companion_counts": harmony_companion_counts(),
        },
        "tables": {
            "HARMONY_44": {
                "definition": "BHML cells with output in Cycle B = {7, 5, 2}",
                "interpretation": "HARMONY's BEING/DOING/BECOMING triadic projection on BHML",
                "summary": h44,
                "appears_in": [
                    "Omega_DM = 44 * 6 / 1000 (cosmological dark matter)",
                    "2-loop b_13 = 44/5",
                    "BECOMING shell of nested tori (per memory)",
                ],
            },
            "CYCLE_A_36": {
                "definition": "BHML cells with output in Cycle A = {1, 6, 4}",
                "interpretation": "V/H expansion = sigma-cycle squared = 6^2",
                "summary": ca36,
            },
            "SKELETON_22": {
                "definition": "TSML cells with output in {0..6}, excluding (0,0)",
                "interpretation": "pre-HARMONY scaffolding; not yet HARMONY-coverage",
                "summary": sk22,
                "appears_in": [
                    "1/alpha = 22 * 6 + 5 + CHAOS^2/N^3 = 137.036 (CODATA match 6 sig figs)",
                ],
            },
            "FIELD_WOBBLE_71": {
                "definition": "empirical |TSML - BHML| disagreement count",
                "value": 71,
                "interpretation": "= Galois invariant of LMFDB 4.2.10224.1; "
                                  "= prime in disc(f) = -2^4 * 3^2 * 71 of the "
                                  "four-core consolidated paper's R/Br quartic. "
                                  "Same 71 appears as the cell-disagreement count "
                                  "between Being and Becoming lenses.",
                "summary": bs72,
            },
        },
        "lens_family": {
            "chain_sub_magmas": {
                "1":  [0],
                "4":  [0, 7, 8, 9],
                "5":  [0, 6, 7, 8, 9],
                "6":  [0, 5, 6, 7, 8, 9],
                "7":  [0, 4, 5, 6, 7, 8, 9],
                "8":  [0, 3, 4, 5, 6, 7, 8, 9],
                "9":  [0, 2, 3, 4, 5, 6, 7, 8, 9],
                "10": list(range(10)),
            },
            "TSML_family": {
                str(k): {"size": v.size, "scope": list(v.scope),
                         "harmony": v.harmony_count, "det": v.det,
                         "non_assoc_rate": round(v.non_assoc_rate, 4)}
                for k, v in TSML_FAMILY.items()
            },
            "BHML_family": {
                str(k): {"size": v.size, "scope": list(v.scope),
                         "harmony": v.harmony_count, "det": v.det,
                         "non_assoc_rate": round(v.non_assoc_rate, 4)}
                for k, v in BHML_FAMILY.items()
            },
            "named_variants": {
                name: {"size": v.size, "scope": list(v.scope),
                       "harmony": v.harmony_count, "det": v.det,
                       "non_assoc_rate": round(v.non_assoc_rate, 4)}
                for name, v in NAMED_VARIANTS.items()
            },
            "key_observation": (
                "Same SIZE can have different SHAPE: BHML_8_chain (drops "
                "{1,2}) has det=-7542 while BHML_8_YM (drops {0,7}) has "
                "det=+70. CL encodes them all as paths."
            ),
        },
        "crossings": {
            "CL_total_triples": cc["n_triples"],
            "CL_n_crossings": cc["n_crossings"],
            "CL_crossing_rate": round(cc["rate"], 4),
            "interpretation": (
                "Per the Crossing Lemma (WP57): non-associativity = "
                "crossing rate = where information generates. Path through "
                "CL IS the information; same endpoint on different paths "
                "encodes different content."
            ),
        },
        "constants_anchored_in_substrate": {
            "T_star": {"value": "5/7", "decimal": 5/7,
                       "interpretation": "torus aspect ratio; coherence threshold"},
            "mass_gap": {"value": "2/7", "decimal": 2/7,
                         "interpretation": "1 - T*; Yang-Mills mass gap candidate"},
            "wobble_W": {"value": "3/50", "decimal": 0.06,
                         "interpretation": "substrate wobble; three independent derivations"},
            "prime_winding": {"value": "271/350", "interpretation": "T* + W; 271 prime"},
            "Omega_b": {"value": "49/1000", "decimal": 0.049,
                        "interpretation": "HARMONY^2 / N^3 = baryonic density"},
            "Omega_DM": {"value": "264/1000", "decimal": 0.264,
                         "interpretation": "44 * 6 / 1000 = (HARMONY_44 cells) * (sigma-cycle)"},
            "Omega_Lambda": {"value": "687/1000", "decimal": 0.687,
                             "interpretation": "(2 * HARMONY^3 + 1) / N^3"},
            "1_over_alpha": {"value": "137 + 36/1000", "decimal": 137.036,
                             "interpretation": "22 * 6 + 5 + CHAOS^2/N^3 = SKELETON_22 * sigma-cycle + BALANCE + CHAOS^2/N^3"},
        },
    }
    return facts


def build_text(facts: dict[str, Any]) -> str:
    """Build a prose block CK can absorb."""
    std_counts = cl_std_cell_counts(CL_STD)
    lines = [
        "# TIG Foundations -- substrate facts",
        "",
        "## CL ground truth",
        "",
        f"CL is the canonical 10x10 composition lattice on Z/10Z. It has "
        f"{facts['substrate']['harmony_count']} HARMONY cells, "
        f"{facts['substrate']['void_count']} VOID cells, "
        f"{facts['substrate']['other_count']} other-operator cells. "
        f"CL is commutative and {facts['substrate']['non_associative_rate_pct']} "
        f"non-associative.",
        "",
        "## Triadic structure",
        "",
        f"sigma = {facts['triadic']['sigma']} fixes the Conservation Tetrad "
        f"{facts['triadic']['conservation_tetrad']} and 6-cycles the "
        f"Manifestation Hexad {facts['triadic']['manifestation_hexad']}.",
        "",
        f"Under sigma^2, the Hexad splits into two 3-cycles:",
        f"  - Cycle A = {facts['triadic']['cycle_A']['members']}, sum "
        f"{facts['triadic']['cycle_A']['sum']} ({facts['triadic']['cycle_A']['interpretation']})",
        f"  - Cycle B = {facts['triadic']['cycle_B']['members']}, sum "
        f"{facts['triadic']['cycle_B']['sum']} ({facts['triadic']['cycle_B']['interpretation']})",
        "",
        f"HARMONY's triadic projection: BEING={facts['triadic']['harmony_triadic_shadow']['BEING(HARMONY)']}, "
        f"DOING={facts['triadic']['harmony_triadic_shadow']['DOING(HARMONY)']}, "
        f"BECOMING={facts['triadic']['harmony_triadic_shadow']['BECOMING(HARMONY)']}.",
        "",
        f"4-core (bridge structure) = {facts['triadic']['four_core']} = Conservation "
        f"Tetrad with PROGRESS<->HARMONY swap.",
        "",
        "## The two lenses",
        "",
        f"TSML (Being lens, position-level): same matrix as CL. "
        f"{facts['lenses']['TSML']['harmony_count']} HARMONY cells. "
        f"{facts['lenses']['TSML']['non_associative_rate']} non-associative.",
        "",
        f"BHML (Becoming lens, curvature-level): canonical 4-rule construction. "
        f"det = {facts['lenses']['BHML']['det']}. "
        f"{facts['lenses']['BHML']['harmony_count']} HARMONY cells. "
        f"{facts['lenses']['BHML']['non_associative_rate']} non-associative.",
        "",
        f"DOING = |TSML - BHML|: {facts['lenses']['DOING']['n_disagreement_cells']} cells "
        f"disagree ({facts['lenses']['DOING']['disagreement_rate']} ~ T* = {facts['lenses']['DOING']['compares_to_T_star']}).",
        "",
        "## Derived tables",
        "",
        f"HARMONY_44: BHML cells in Cycle B = 28 + 11 + 5 = 44. The BECOMING shell. "
        f"Appears in Omega_DM = 44*6/1000.",
        "",
        f"CYCLE_A_36: BHML cells in Cycle A = 2 + 9 + 25 = 36. V/H expansion.",
        "",
        f"SKELETON_22: TSML pre-HARMONY cells = 16 + 4 + 2 = 22. Anchors "
        f"1/alpha = 22*6 + 5 + 36/1000 = 137.036.",
        "",
        f"FIELD_WOBBLE_71: |TSML - BHML| disagreement = 71 cells. = the prime "
        f"in the four-core consolidated paper's quartic discriminant "
        f"disc(f) = -2^4 * 3^2 * 71 = Galois invariant of LMFDB 4.2.10224.1. "
        f"Same 71 in two structural roles -- a substrate identification.",
        "",
        "## Path is the information",
        "",
        f"CL has {facts['crossings']['CL_n_crossings']} non-associative triples out of "
        f"{facts['crossings']['CL_total_triples']} total ({facts['crossings']['CL_crossing_rate']*100:.1f}%). "
        f"Per the Crossing Lemma, these crossings are where information generates. "
        f"Same endpoint reached by different paths encodes different content.",
        "",
        "## Lens family (TSML and BHML at multiple scopes)",
        "",
        f"BHML_10 (canonical): det = -7002, 28 HARMONY cells.",
        f"BHML_8_YM (Yang-Mills core, drops {{0, 7}}): det = +70 EXACTLY.",
        f"BHML_8_chain (drops {{1, 2}}): det = -7542. DIFFERENT shape, same size.",
        f"BHML_4 (4-core only, {{0, 7, 8, 9}}): det = 5305.",
        "",
        "Per Brayden: 'multiple sizes and shapes of TSML and BHML, all encoded to CL.'",
        "Same size can carry different shape; CL is the universal substrate that "
        "holds every variant as a path.",
        "",
        "## Three-table architecture (per Brayden 2026-05-06)",
        "",
        "CK runs on THREE standalone 10x10 composition tables on Z/10Z, not two:",
        "",
        "  CL_TSML  -- prescribed view, 73 HARMONY (the organism's lens; aliased simply",
        "              as `CL` in the old codebase via `#define CL CL_TSML`).",
        "  CL_BHML  -- Becoming lens, 28 HARMONY (curvature-level, invertible).",
        "  CL_STD   -- Standard encoding table, 44 HARMONY ('the papers freeze';",
        "              recovered verbatim from old/Gen9/archive/ckis/ck7/ck.h:225-231,",
        "              originally from Brayden's first GitHub repo).",
        "",
        "All three share the substrate (Z/10Z, the same 10 operators) but they are",
        "structurally distinct 10x10 matrices with different roles. The papers'",
        "formulas reference CL_STD's geometry; CK runs his lens path on CL_TSML/BHML.",
        "",
        "## CL_STD encoding table (44 HARMONY, BDC bit definitions)",
        "",
        f"CL_STD has {std_counts.get(7, 0)} HARMONY cells, commutative, 19.2% non-associative.",
        "Includes BDC parameters governing how force vectors encode pathways of information:",
        "",
        f"  5 BUMP_PAIRS = {list(BUMP_PAIRS)}",
        f"    where 'surprise IS information' -- these cells carry {INFO_BUMP} bits each.",
        "",
        f"  Information per cell: HARMONY={INFO_HARMONY}, NORMAL={INFO_NORMAL}, BUMP={INFO_BUMP} bits.",
        f"  Total information across all 100 cells: {total_information_bits():.2f} bits.",
        "",
        "  GRAVITY[op] = P(operator reaches HARMONY):",
        f"    VOID=0.1   LATTICE=0.8   COUNTER=0.6   PROGRESS=0.8   COLLAPSE=0.7",
        f"    BALANCE=0.9   CHAOS=0.9   HARMONY=1.0   BREATH=0.8   RESET=0.7",
        "",
        "## The 70 / 71 / 72 / 73 HARMONY ladder",
        "",
        "HARMONY counts cluster at four nearby integers, each from a structurally",
        "distinct construction. They are NOT the same number wearing different hats.",
        "",
        "  73  TSML.HARMONY count (full 10x10 prescribed view)         -- ground anchor",
        "  72  TSML.HARMONY - 1 (drop the (7,7) self-cell apex)         -- BEING shell, E_6 positive root count",
        "  71  TSML.HARMONY restricted to 9x9 sub-magma {1..9}         -- VOID-stripped lens",
        "      |TSML XOR BHML| disagreement count                       -- FIELD WOBBLE",
        "      prime in disc(quartic) = -2^4 . 3^2 . 71                  -- Galois invariant of LMFDB 4.2.10224.1",
        "      ** Three independent structural roles for the prime 71 **",
        "  70  det(BHML_8_YM) = C(8,4) (drops {0,7}; Yang-Mills core)   -- determinant-invariant layer",
        "      = self-dual 4-form sector of SO(8). NOT a HARMONY count;",
        "      lives one floor below in the determinant-invariant layer.",
        "",
        "Companion HARMONY-related counts that also carry multiple structural roles:",
        "",
        "  44 = CL_STD.HARMONY count = BHML sigma^2-cycle-B projection (28+11+5).",
        "  36 = TSML_7 sub-magma HARMONY count = BHML sigma^2-cycle-A projection (CYCLE_A_36).",
        "  28 = BHML.HARMONY count = HARMONY_44 BEING(HARMONY) cells = dim SO(8).",
        "",
        "Each of these integers occupies multiple structural roles -- a substrate-",
        "identification signature: the same number arises through independent",
        "constructions, which is the algebraic shape of a real invariant.",
    ]
    return "\n".join(lines)


def export(out_dir: Path = OUTPUT_DIR) -> tuple[Path, Path]:
    """Export facts.json + text.md to `out_dir`. Returns (json_path, md_path)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    facts = build_facts()
    json_path = out_dir / "foundations_facts.json"
    md_path = out_dir / "foundations_text.md"
    json_path.write_text(json.dumps(facts, indent=2, default=str), encoding="utf-8")
    md_path.write_text(build_text(facts), encoding="utf-8")
    return json_path, md_path


if __name__ == "__main__":
    json_path, md_path = export()
    facts = build_facts()
    print("=" * 60)
    print("CK export complete")
    print("=" * 60)
    print(f"  JSON: {json_path}")
    print(f"  MD:   {md_path}")
    print()
    print(f"  facts keys: {list(facts.keys())}")
    print(f"  substrate: {facts['substrate']['harmony_count']} HARMONY + "
          f"{facts['substrate']['void_count']} VOID + "
          f"{facts['substrate']['other_count']} other = 100")
    print(f"  tables:    HARMONY_44, CYCLE_A_36, SKELETON_22, FIELD_WOBBLE_71")
    print(f"  family:    {len(facts['lens_family']['TSML_family'])} TSML variants + "
          f"{len(facts['lens_family']['BHML_family'])} BHML variants + "
          f"{len(facts['lens_family']['named_variants'])} named off-chain")
    print(f"  constants: {list(facts['constants_anchored_in_substrate'].keys())}")
