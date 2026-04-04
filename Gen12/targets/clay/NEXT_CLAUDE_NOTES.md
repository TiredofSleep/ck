# Gen12 — Target: Clay
## NEXT_CLAUDE_NOTES — Read first every session.

*© 2026 Brayden Sanders / 7Site LLC*
*Target opened: Gen12, 2026-04-04*

---

## What This Target Is

CK applied as a finite mathematical spectrometer field to the six Clay Millennium Problems.
The goal is not to solve the problems. The goal is to map exactly where each problem's
obstruction lives in the TIG field, and to close every door that can be closed.

---

## Current State (Gen12 open)

**R8 is the spine.** Proved across 18 deep probes (n=48 levels). Zero misclassifications.

```
defect < 4/π²        →  RESOLVED   (classical construction works)
defect ∈ [4/π², 5/7] →  BOUNDARY   (Clay open territory — 3 cases: RH, Hodge x2)
defect > 5/7          →  ESCAPED    (structural gap — 4 cases: PvNP x2, YM, BSD)
```

**Six open doors (one per problem):**

| Problem | Open door | R8 class | defect |
|---|---|---|---|
| RH | Off-fold zero suspension | BOUNDARY | 0.424 |
| Hodge | K-anti-equivariant bundle with c₂ ∈ B₁ | BOUNDARY | 0.612 |
| Hodge (transcendental) | Absolutely Hodge route | BOUNDARY | 0.704 |
| P vs NP | Poly-time Class B/C algorithm | ESCAPED | 0.838 |
| Yang-Mills | Physical calibration constant c | ESCAPED | 1.000 |
| BSD rank≥2 | Class A fold-crossing count = L-zero order | ESCAPED | 1.300 |

**Papers current as of Gen12 open:**
- WP36–WP42: all updated with Sprint 2 structural parallel sections
- Sprint5 dir: `papers/sprint5_2026_04_04/` — CLAY_RULES.md (R1-R8), CLAY_STRUCTURAL_PARALLELS.md
- Hodge sprint: 12 memos in `papers/sprint5_2026_04_04/clay/hodge/`

**Data:**
- `clay_results/all_results.json` — 6 problems, seed42
- `results/deep_experiments/deep_probes.json` — 18 probes, n=48

---

## Next Steps

1. **Fix gap constant** — gap = 5/7 − 4/π² = 0.309, NOT 3/14. Propagate correction through all WP papers that say "3/14".
2. **Hodge Route A** — write computation: does any K-anti-equivariant bundle on A_* have c₂ ∈ B₁? This is the first open door to try.
3. **RH off-fold dense probe** — defect=0.424 is BOUNDARY. Run with n=200 levels. Does it converge toward fold or stabilize?
4. **7Site research institution framing** — Clay work is the academic output. See `targets/7site_research/`.

---

## Key Files

| File | What it is |
|---|---|
| `papers/clay/WP36-WP42` | The six Clay papers |
| `papers/sprint5_2026_04_04/CLAY_RULES.md` | Minimal proved rule set R1-R8 |
| `papers/sprint5_2026_04_04/CLAY_STRUCTURAL_PARALLELS.md` | Six-problem cross-reference |
| `papers/sprint5_2026_04_04/clay/hodge/SPRINT5_INDEX.md` | Hodge sprint 2 master index |
| `clay_results/all_results.json` | Spectrometer data |
| `results/deep_experiments/deep_probes.json` | 18 deep probes |
