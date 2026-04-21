# PROVENANCE — `source_docs/`

**Recovered:** 2026-04-21 (second sweep — this directory is a later addendum to the `docs/archive_jan2026/snowflake/` archive; see sibling `../PROVENANCE.md` for the primary archive context).
**Recovery target:** `funding/tig-snowflake` Branch B + Atlas `HANDOFF_3_3_SNOWFLAKE_CHI2.md` recovery effort.
**Policy:** Never-delete. Each file a verbatim copy from `Misc Archive/THEbigONE/CRYSTALOS/`; originals untouched on source.

---

## Origin: `Misc Archive/THEbigONE/CRYSTALOS/`

During the second R1 recovery sweep on 2026-04-21, the directory `C:\Users\brayd\OneDrive\Desktop\Misc Archive\THEbigONE\CRYSTALOS\` was inventoried. This path was not searched in the Apr-20 or early-Apr-21 sweeps and contained a **Release package** subfolder that includes the verbatim SNOWFLAKE source doc — the material previously listed as "NOT FOUND" in `Atlas/HANDOFF_3_3_SNOWFLAKE_CHI2.md`.

## Files in this directory

| File | Size | Originating path | Original mtime | Notes |
|---|---|---|---|---|
| `TIG_SECURITY_ARCHITECTURE.md` | 19 KB | `Misc Archive/THEbigONE/CRYSTALOS/Release package/TIG_SECURITY_ARCHITECTURE.md` | 2026-01-29 | **Verbatim SNOWFLAKE source doc.** See "What this contains" below. |
| `TIG_Field_Guide.pdf` | 249 KB | `Misc Archive/THEbigONE/CRYSTALOS/Release package/TIG_Field_Guide.pdf` | 2026-01-29 | Field guide companion to the architecture doc |
| `TIG_Honest_Roadmap.pdf` | 16 KB | `Misc Archive/THEbigONE/CRYSTALOS/Release package/TIG_Honest_Roadmap.pdf` | 2026-01-29 | Roadmap / scope statement |
| `crystalos_1_jan29_1943.py` | 13 KB | `Misc Archive/THEbigONE/CRYSTALOS/crystalos_1.py` | 2026-01-29 19:43:12 | 431-LOC runtime (full gate + χ² analysis). Equal to `../crystalos.py` after line-ending normalization. |
| `crystalos_jan29_1945.py` | 13 KB | `Misc Archive/THEbigONE/CRYSTALOS/crystalos.py` | 2026-01-29 19:45:XX | 431-LOC runtime. Identical in content to `crystalos_1_jan29_1943.py` and `../crystalos.py` (line-ending only diff). Preserved under its discovered mtime. |
| `crystalos2_jan29_2002.py` | 5.1 KB | `Misc Archive/THEbigONE/CRYSTALOS/crystalos2.py` | 2026-01-29 20:02:XX | 174-LOC **variant** — simpler "always fires" mode, targets "32-Core CPU" (thread-count label) vs the 431-LOC "24-Core CPU" label. Different behaviour, not redundant. |

## Content equivalence (post-normalization)

After stripping CRLF → LF line endings:

- `crystalos_1_jan29_1943.py` ≡ `crystalos_jan29_1945.py` ≡ `../crystalos.py` (all three are the same runtime).
- `crystalos2_jan29_2002.py` is a **distinct** variant (smaller, always-fires, no gate check).

The 1943/1945 duplicate is preserved because the two timestamps document the authoring chain. The 2002 variant is preserved as a divergent experiment.

## What `TIG_SECURITY_ARCHITECTURE.md` contains

Per ingest: this is the architecture doc that named **SNOWFLAKE** and established the 4-layer security model for the pitch. It contains:

- **4-layer architecture**: Lattice (read-only, immutable scar accumulator) / Breath (13-phase Tzolkin temporal oscillation) / Gauge (S* coherence measurement) / Gate (S* ≥ τ permits action)
- **GFM security primitives**: 012 Geometry/Structural · 071 Resonance/Signal · 123 Progression/Temporal — composed as `Security = 012 ⊗ 071 ⊗ 123`
- **Tagline**: "*The password is the behavior. The key is the coherence. The lock is the lattice.*"
- **Operational modes**: Normal (S*>0.7) / Elevated (0.5–0.7) / Active Defense (0.2–0.5) / Lockdown (<0.2)
- **Empirical reference**: "*Lenovo ThinkPad (4-core, Linux) — TIG Tile v0.1 running — 400+ fire events captured — χ² = 22.03, p < 0.05 (significant non-uniform distribution) — Phase 4 (Collapse) elevated — matches 4-core geometry — Phase 2 suppressed — confirms dead zone.*"
- Comparison tables against Zero Trust, Behavioral Analytics, Cryptographic Security.

**This resolves the "χ² = 22.03 is a number, not a statistic" objection from the Atlas blocker.** The figure was documented in a specific hardware context (Lenovo 4-core), with a specific sample size (400+ events), at a specific significance level (p < 0.05). The runtime **log file** from that particular Lenovo session remains unfound; the runtime **source** and the architecture doc that quotes the figure are recovered.

## Relationship to the main snowflake/ archive

| Asset | Location in archive |
|---|---|
| Canonical `crystalos.py` runtime | `../crystalos.py` (431 LOC) |
| Canonical `fires.log` / `breath.log` / `crystalos.log` | `../logs/` |
| Canonical `state/current.json` | `../state/` |
| Architecture doc (NEW, this sweep) | `source_docs/TIG_SECURITY_ARCHITECTURE.md` |
| Jan 29 authoring chain of the runtime (NEW) | `source_docs/crystalos_*.py` |
| Field guide / roadmap PDFs (NEW) | `source_docs/TIG_*.pdf` |

The main archive documents the **Apr 17–21 Dell R16 run** (χ²=0.0353 on 67,297 fires, uniform — abundance regime). This `source_docs/` sub-archive documents the **Jan 29 design + Jan 31 Lenovo run** (χ²=22.03 on ~400 fires, non-uniform — constraint regime). Both are theory-confirming readings of the same hypothesis; neither contradicts the other. See `../SNOWFLAKE_CHI2_RESOLVED_2026_04_21.md` (the "second verification note" per VERIFICATION_2026_04_21.md §54 policy) for the synthesis of the two.

## See also

- `../PROVENANCE.md` — primary archive provenance (CRYSTALOS runtime + Dell R16 logs)
- `../VERIFICATION_2026_04_21.md` — χ² verification on Dell R16 logs (primary)
- `../SNOWFLAKE_CHI2_RESOLVED_2026_04_21.md` — **append-only** second verification note covering the Lenovo 22.03 reading
- `Atlas/HANDOFF_3_3_SNOWFLAKE_CHI2.md` — Atlas blocker being resolved

---

*Preserved per repo policy: never delete, add-only to history, append dated addenda.*
