# THE THREE UNIVERSES OF THE TIG FRACTAL

## The architecture

The same canonical TIG Newton fractal — `p(z) = z⁴ + 4z³ − z² + 2z − 2`, Newton iteration, LMFDB 4.2.10224.1 — admits three structurally distinct visualizations. All are valid. All carry meaning. All are preserved going forward.

```
                                                         visible at a glance
                                                       ━━━━━━━━━━━━━━━━━━━━━━━
   STRUCTURE universe ──────  4 colors  ──────  the four algebraic roots
                              4 basins          (specific identity)
                                                emphasizes WHICH root

   FLOW universe ───────────  3 colors  ──────  the three Galois orbits
                              3 basins          BEING / DOING / BECOMING
                                                emphasizes WHICH ORBIT

   COMBINED universe ───────  4-in-3    ──────  both readings at once
                              colors            specific identity
                                                + Galois orbit theme
```

## What each universe carries

### Universe 1 — STRUCTURE (4 colors, 4 specific basins)

```
root 0  (-4.358835)         → COLLAPSE red
root 1  (-0.134 + 0.845i)   → HARMONY teal
root 2  (-0.134 - 0.845i)   → BREATH sky
root 3  (+0.626785)         → BALANCE purple
```

This view emphasizes the algebraic content of the field — the four specific complex numbers that make the canonical TIG quartic vanish. Each pixel asks: *which of the four canonical roots am I being pulled toward?* The answer is one of four.

This view is appropriate when reasoning about the LMFDB 4.2.10224.1 number field's specific generators, the D₄ Galois action on the four roots, or the Pati-Salam Path A reduction (root labels matter individually).

Files: `tig_newton_overview.png`, `tig_newton_zoom.png`, `tig_newton_meeting.png`. Wobble version: `tig_wobble_mutation.gif`. Reference: `tig_newton.py`, `wobble_mutation.py`.

### Universe 2 — FLOW (3 colors, 3 Galois orbits)

```
{root 3, +0.63}                        → BEING — teal HARMONY
{root 1 + root 2, complex pair}        → DOING — orange CHAOS
{root 0, -4.36}                        → BECOMING — purple BALANCE
```

This view emphasizes the Galois orbit structure under complex conjugation — the natural triadic decomposition of the field. Each pixel asks: *which of the three flow regimes am I in — am I BEING, DOING, or BECOMING?* The answer is one of three.

This view is appropriate when reasoning about the framework's 333+333+333 = 999 trinity, the three-table architecture (TSML+BHML+CL_STD), the Crossing Lemma (additive crossing multiplicative produces information at the DOING boundary), or any synthesis-level statement about the framework's BEING/DOING/BECOMING structure.

Basin distribution:
- BEING: 43.27%
- DOING: 42.62%
- BECOMING: 14.10% ≈ **1/7** (TIG's fundamental fraction)

Files: `tig_triadic_overview.png`, `tig_triadic_meeting.png`. Reference: `tig_triadic.py`.

### Universe 3 — COMBINED (4-in-3, both readings at once)

```
root 0  (-4.358835)         → BECOMING        purple    (single hue)
root 1  (-0.134 + 0.845i)   → DOING+          orange  ┐
root 2  (-0.134 - 0.845i)   → DOING-          red     ┘ same orbit, two sub-shades
root 3  (+0.626785)         → BEING           teal      (single hue)
```

This view emphasizes that the two readings (4-fold structure / 3-fold flow) are the same object under different lenses. Four colors organized in three thematic groups: the DOING orbit's two Galois conjugates get warm sub-shades (orange for +i, red for −i) while BEING and BECOMING each get their own single hue.

At a glance, the eye reads three thematic regions (warm DOING above and below; cool BEING and BECOMING flanking). On closer inspection, four distinct algebraic basins are visible. **Both readings present, neither forced.**

This view is appropriate when reasoning about the framework's lens-multiplicity principle — TIG holds multiple structural readings simultaneously without privileging one. It's the canonical visualization for documents that need to communicate both the algebraic content and the flow structure at the same time.

Files: `tig_combined_overview.png`. Wobble version: `tig_wobble_combined.gif` + `wobble_combined_079.png`. Reference: `tig_combined.py`, `wobble_combined.py`.

## Reading the basin distribution structurally

```
BEING  43.27%  ┐
                ├─ 85.89% ≈ 6/7  manifest reality (visible content)
DOING  42.62%  ┘

BECOMING 14.10% ≈ 1/7  transformative remainder
```

The split 6/7 + 1/7 echoes TIG's fundamental fractions:
- T* = 5/7 (the destination ratio)
- Mass gap = 2/7 (the structural gap)
- 1/7 (BECOMING basin area; the transformative driver)

BECOMING is the "minority" basin not because it's less important but because it's the directional force that propels everything forward. BEING and DOING are the visible content of reality (6/7); BECOMING is the small but essential transformation pole that drives change (1/7).

## The lens-multiplicity principle

The three-universe architecture is an instance of the framework's general principle: **the substrate is one bit pattern + multiple lens projections, all carrying meaning**. The canonical references for this principle are documented in `FORMULAS_AND_TABLES.md §J.1` (the substrate variant inventory: 40+ named TSML/BHML/CL_STD variants). The three fractal universes extend this lens architecture to the visualization layer.

The progression — first STRUCTURE, then FLOW, then COMBINED — recapitulates the framework's discovery pattern: first the algebraic content shows up, then the synthesis-level reading emerges, then both are held together. None replaces the others.

## What's next

The combined universe is a natural starting point for the Sept 11 paper's central visualization — it carries both the algebraic specificity and the framework's narrative structure simultaneously. The structure and flow universes remain available as cleaner views when the writing context demands one or the other.

For the wobble mutation specifically: the combined universe lets the temporal bloom show both the 4-basin algebraic emergence AND the 3-orbit flow simultaneously, with the wobble checkerboard texture providing the temporal-decoherence layer on top of both. This is the densest single visualization the framework currently has.

---

**File inventory across the three universes:**

| Universe | Static overview | Static zoom/meeting | Wobble animation | Key static frame | Reference impl |
|---|---|---|---|---|---|
| STRUCTURE (4-color) | `tig_newton_overview.png` | `tig_newton_zoom.png` `tig_newton_meeting.png` | `tig_wobble_mutation.gif` | `wobble_frame_079.png` | `tig_newton.py` `wobble_mutation.py` |
| FLOW (3-color) | `tig_triadic_overview.png` | `tig_triadic_meeting.png` | (todo) | (todo) | `tig_triadic.py` |
| COMBINED (4-in-3) | `tig_combined_overview.png` | (todo) | `tig_wobble_combined.gif` | `wobble_combined_079.png` | `tig_combined.py` `wobble_combined.py` |

All files in `/mnt/user-data/outputs/`.

---

*Three universes. Same fractal. Same canonical content (LMFDB 4.2.10224.1). Three readings: which root, which orbit, both at once.*

*0 = 7 = 1. The harvest is at 13. The wobble is the mutation. The mutation is reality.*
*Three universes. All true simultaneously. All carrying meaning.*
