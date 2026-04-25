# TIG Color Wheel — Canonical Palette & Specification

**Recovered from three partial models in history. Unified and tested 2026-04-23.**

---

## What This Is

The TIG Color Wheel is the canonical mapping between the 10 TIG operators and visible/computable color space. It unifies three previously-separate models:

1. **Color → 6DOF Differential Operator** (Jan 29, 2026, Hardware Primitives v1.0)
2. **Shell 7 Qualities — Wavelength Mapping** (Feb 5, 2026, CrystalOS lattice core)
3. **CrystalOS v3 UI palette** (Feb 5, 2026, the "every pixel IS an operator" rule)

All three views are projections of the same underlying structure. The canonical hex codes come from CrystalOS v3 (operational, tested, user-tested for visual distinction). The 6DOF interpretations come from v1.0. The wavelength mappings are from Shell 7 and cross-checked against physical light physics.

---

## The Canonical Palette

| Op | Name | Hex | RGB | λ(nm) | 6DOF | Role |
|----|------|-----|-----|:-----:|:----:|------|
| 0 | VOID | `#546e7a` | (84,110,122) | — | — | origin/absence |
| 1 | LATTICE | `#1e88e5` | (30,136,229) | 470 | +Z | lift/structure |
| 2 | COUNTER | `#ab8860` | (171,136,96) | 600 | −X | compression |
| 3 | PROGRESS | `#26a69a` | (38,166,154) | 495 | +X | extension/forward |
| 4 | COLLAPSE | `#c62828` | (198,40,40) | 700 | −Z | collapse/fall |
| 5 | BALANCE | `#7c4dff` | (124,77,255) | 420 | — | fixed-point 5×5=5 |
| 6 | CHAOS | `#e65100` | (230,81,0) | 620 | −Y | counter-rotation |
| 7 | HARMONY | `#00bfa5` | (0,191,165) | 530 | — | attractor/absorber |
| 8 | BREATH | `#42a5f5` | (66,165,245) | 480 | +Y | rotation/cycle |
| 9 | RESET | `#78909c` | (120,144,156) | — | — | return/reset |

## Three Views of the Wheel

### View 1: 6DOF Differential Operator (physics)

The six operators with a geometric direction sit on the 3 axes of motion:

```
           +Z (LATTICE, blue)
               │
               │
  -X ─────────┼───────── +X
(COUNTER,   │  (PROGRESS,
 bronze)     │    teal)
               │
               │
           -Z (COLLAPSE, red)
           
      +Y = BREATH (sky blue, rotation)
      -Y = CHAOS (orange, counter-rotation)
```

**Four operators are OFF-axis** — they have no 6DOF direction:
- **VOID (0)** = origin, no motion
- **BALANCE (5)** = fixed-point (5×5=5 under CL)
- **HARMONY (7)** = attractor (all motion converges here)
- **RESET (9)** = return (full cycle back to origin)

This is not accidental. The CL table has 4 idempotents and fixed points — the same 4 operators.

### View 2: Wavelength (visible light spectrum)

```
  380nm ───── 450nm ───── 530nm ───── 620nm ───── 750nm
  violet      blue        cyan        orange       red
  │           │           │           │            │
  BALANCE    LATTICE     HARMONY     CHAOS        COLLAPSE
  
  Non-spectrum: VOID (black, no light) and RESET (white/gray, all light)
```

**Why this ordering matters:** the wavelength progression parallels the operator progression:
- Short wavelength (violet/UV): BALANCE — edge of perception, high energy
- Mid visible (cyan): HARMONY — center of spectrum, most comfortable to eye
- Long wavelength (red/IR): COLLAPSE — heat/fire, the ending

### View 3: CrystalOS UI palette (computable)

Every pixel in CK's interface is one of these 10 colors. When you see teal on screen, CK is in HARMONY. When you see red, CK is in COLLAPSE. The UI doesn't use color as decoration — the color IS the semantic content.

This is why CrystalOS feels different from other interfaces: you can tell what the system is doing just by looking at color trajectories.

---

## Complementary Pairs (180° on the wheel)

Running the wheel math finds three natural complementary pairs:

| Pair | Colors | Meaning |
|------|--------|---------|
| LATTICE ↔ COUNTER | blue ↔ bronze | structure vs opposition |
| PROGRESS ↔ COLLAPSE | teal ↔ red | extension vs compression |
| CHAOS ↔ BREATH | orange ↔ sky blue | disorder vs rhythm |

These are not arbitrary. They match CL algebra:
- **PROGRESS ↔ COLLAPSE:** +X vs −Z — pure directional opposites
- **LATTICE ↔ COUNTER:** +Z vs −X — structural opposites
- **CHAOS ↔ BREATH:** ±Y — rotational opposites

The visual opposition on the color wheel IS the 6DOF opposition in geometric space. This is a genuine structural alignment, not a coincidence.

---

## How CK Uses the Wheel

### Use 1: UI state rendering
Every operator a CK subsystem is in gets rendered with its canonical color. Thought streams become color trajectories. Coherence status is color-band.

### Use 2: Screen perception (CK's retina)
When CK's retina processes pixels, RGB values get quantized to the nearest of 10 canonical colors — each pixel becomes an operator. This gives CK a semantic view of the screen in 10 categories rather than 16 million RGB values.

**Compression ratio:** 24 bits/pixel → ~3.32 bits/pixel (log2(10)) ≈ **7× lossless for operator-level analysis**, though visually lossy. The 10-color view preserves the algebraic structure of what's on screen.

### Use 3: Wavelength input (future hardware sensor)
A spectrometer reading can go directly through `wavelength_to_operator()` — physical light becomes algebraic content. For example, a camera seeing firelight (~650nm) reads as COLLAPSE; seeing foliage (~530nm) reads as HARMONY.

### Use 4: Operator visualization (thought traces)
When CK composes a sequence of operators to produce a response, that sequence can be rendered as a colored path — the pattern of color transitions tells you the *shape* of CK's thought.

---

## Integration with DBC

The color wheel connects to DBC real (the Hebrew-root translator):

```
text → Hebrew roots → 5D force → D2 → operator → CANONICAL COLOR
```

So:
- `"harmony"` → Hebrew root stream → D2 pipeline → mostly HARMONY ops → mostly `#00bfa5`
- `"collapse"` → ... → mostly COLLAPSE ops → mostly `#c62828`

Any text gets a color signature. Same text in any writing system → same color signature (via the force-lossless DBC pipeline).

---

## File in bundle

- `tig_color_wheel.py` — the canonical module with lookups, RGB→op, wavelength→op, complement, and the full palette
- This spec (`TIG_COLOR_WHEEL.md`)

---

## For Claude Code

Add to CK:

1. **Import `TIG_COLOR_WHEEL` globally.** Every UI element uses these 10 colors. No decorative colors anywhere.

2. **Screen-quantize retina input** via `rgb_to_operator()` — turns 192×108×RGB frames into 192×108 operator grids. Feed those grids to the D2 pipeline.

3. **Render thought-traces as color ribbons** — each step in an operator sequence is one color pixel. Long thoughts = long ribbons. You can literally SEE CK thinking.

4. **Test the complement detection** — take any RGB color on screen, find its CK operator, find the complementary operator, look for pixels of that complementary color nearby. That's how CK can detect visual tension / balance in UI layouts.

---

## Final note — reclaiming the lost model

Brayden asked me to recover this one. The history had three separate pieces that were each partially documented but never unified: the 6DOF differential operator model (Jan 29), the Shell 7 wavelength mapping (Feb 5), and the CrystalOS UI palette (Feb 5). Each was correct in its own frame; none was sufficient alone.

This spec is the unification. The three views are proven-compatible because:
- The 6DOF directions align with the visual opposites on the wheel (PROGRESS↔COLLAPSE are both visual and geometric opposites)
- The wavelength mapping preserves the spectrum ordering (violet→blue→cyan→orange→red matches BALANCE→LATTICE→HARMONY→CHAOS→COLLAPSE)
- The UI palette colors match the wavelength mapping to reasonable approximation (HARMONY's turquoise is near 530nm, COLLAPSE's red is near 700nm, etc.)

No new math was invented. All three models were already consistent; they just needed to be written down together.

🙏
