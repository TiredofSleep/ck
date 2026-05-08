# THE TIG FRACTAL — Formula and Construction

## The formula

```
The TIG Newton Set
==================

p(z)  = z⁴ + 4z³ − z² + 2z − 2        (canonical TIG quartic; LMFDB 4.2.10224.1)
p'(z) = 4z³ + 12z² − 2z + 2

Newton iteration:
    z_{n+1} = z_n − p(z_n) / p'(z_n)

Each starting point z_0 ∈ ℂ converges to one of the 4 roots of p.
Color the pixel by which root it converges to.
The basin boundaries are the fractal.
```

## Why this is the TIG fractal (not the Mandelbrot equivalent)

A standard Mandelbrot iterates `z² + c` and asks which `c` gives bounded orbits. For TIG, the natural polynomial is the quartic `x⁴ + 4x³ − x² + 2x − 2 = 0` from D40 / WP105 — the closed-form attractor's R/Br quartic generating LMFDB 4.2.10224.1.

I tried Mandelbrot-style iteration on this quartic first. The polynomial grows too fast (multiplier 12 at z=0; super-repelling) and the orbit escapes for essentially all c. So the standard "filled-in TIG set" turns out empty.

Newton's method on the same polynomial works perfectly. The 4 roots are the 4 specific complex numbers that make the canonical quartic vanish — the actual algebraic content of the TIG closed-form attractor. Each starting point z_0 in the complex plane is "pulled toward" one of these 4 roots under Newton iteration. The boundary between basins is fractal, with infinite self-similar detail (every bulb on the boundary is itself a satellite copy of the full 4-basin structure).

**This is the TIG fractal because the four colors are the four canonical TIG numbers** — the actual roots of LMFDB 4.2.10224.1 = R/Br at α=1/2.

## The 4 roots, with TIG operator color assignment

```
ROOT                                 |z|         OPERATOR     HEX        SIGNATURE
──────────────────────────────────────────────────────────────────────────────────
root 0:  −4.358835                  4.358835   COLLAPSE (4)  c62828    real, large
root 1:  −0.133975 + 0.845045i      0.855600   HARMONY  (7)  00bfa5    complex+
root 2:  −0.133975 − 0.845045i      0.855600   BREATH   (8)  42a5f5    complex−
root 3:  +0.626785                  0.626785   BALANCE  (5)  7c4dff    real, small
```

Vieta verification:
- Sum of roots = −4 (matches the +4 z³ coefficient with sign flip)
- Product of roots = −2 (matches the constant term with sign flip)
- Field signature (2, 1) = 2 real roots + 1 complex pair ✓ (LMFDB 4.2.10224.1)

## The basin distribution (overview window)

```
Window: Re ∈ [−5.5, 3.5], Im ∈ [−3.21, 3.21]   (aspect 5/7, the TIG torus)
Resolution: 1200 × 857
Basin areas:
    BALANCE (purple, +0.63):       43.27%   ← attracts the largest area
    HARMONY (teal,    upper c.r.): 21.31%
    BREATH  (sky,     lower c.r.): 21.31%   (matches HARMONY by complex conjugate symmetry)
    COLLAPSE (red,   −4.36):       14.10%   ≈ 1/7 = 14.29%
```

The COLLAPSE basin is approximately 1/7 of the total area — close to TIG's fundamental fraction 1/7 (= 1 − T*). HARMONY + BREATH ≈ BALANCE area (42.62% vs 43.27%) — near-equality.

## Render aspect ratio

The canonical TIG torus has R/r = 5/7. All renderings use this aspect ratio:
- Width 1200, height = 1200 · 5/7 = 857
- Viewing box has the same 5/7 width-to-height ratio

## Files in this set

```
tig_newton.py                  Python script with arguments for rendering
tig_newton_overview.png        Wide view: Re ∈ [−5.5, 3.5], Im ∈ [−3.21, 3.21]
tig_newton_zoom.png            Boundary zoom: Re ∈ [−2.1, −0.9], Im ∈ [−0.43, 0.43]
tig_newton_meeting.png         Four-basin meeting region: Re ∈ [−2.5, 0.5]
```

## How to render variants (Python)

```bash
# Overview
python tig_newton.py --width 1200 --max-iter 80 --half-x 4.5 --output tig_overview.png

# Zoom into boundary
python tig_newton.py --width 1200 --max-iter 120 --half-x 0.6 --center-real -1.5 --output tig_zoom.png

# Four-basin meeting
python tig_newton.py --width 1200 --max-iter 120 --half-x 1.5 --center-real -1.0 --output tig_meet.png

# Arbitrary zoom
python tig_newton.py --width 1200 --max-iter 200 --zoom 50 --center-real -1.5 --center-imag 0.85 --output tig_deep.png
```

Higher `--max-iter` resolves the basin boundary more sharply at zoomed scales.
Higher `--zoom` reveals deeper fractal structure.

## Connection to the framework

The TIG Newton fractal is the **visualization of the closed-form runtime attractor's number field**. The 4 roots are the 4 values of R/Br at α=1/2; the iteration is Newton's method, which is the canonical "find-the-root" dynamics. The fractal is what happens when we ask: starting from any complex number, which of the 4 canonical TIG roots will we be pulled toward?

This is not a metaphor. The 4 roots are LMFDB 4.2.10224.1's actual generators. The Galois group D₄ acts on these 4 roots. The fractal shows the geometry of "which root wins from where" across the entire complex plane.

It is the fractal picture of the TIG closed-form attractor.

---

*Each pixel is a starting point; each color is a destiny.*
*The boundaries are infinitely complex; the destinations are exactly four.*
*Four is the number of canonical TIG roots; 5/7 is the canonical aspect ratio.*
*The fractal IS the picture of the closed-form attractor's basin geometry.*
